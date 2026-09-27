"""R2-T (PREREG_G1_C1_Q4.md): does posterior averaging (what a better sampler would buy) improve structure accuracy
over the argmin, for the learned A80/esmprior energy?  Classical, exact-in-the-Laplace-limit posterior mixture.

For one crop: R restarts from the exact prior, L-BFGS to convergence (tol / --iters), 2 A greedy clustering, each mode
representative's Hessian (autograd, internal coordinates), Laplace log-mass on a temperature ladder
    log w_k(T) = -E_k/T + sum_i log min( sqrt(2 pi T / lambda_i), 2 pi )     (truncated-Gaussian width per direction:
                 flat / negative directions are bounded by the 2 pi torus length instead of diverging)
[v2: Laplace volumes replaced -- A80 is piecewise smooth; weights (a) exp(-E_k/T), (b) n_k exp(-E_k/T)]
soft structure(T) = w-weighted average of mode CA coordinates, each superposed on the argmin mode (Kabsch).
Records per T: ESS, RMSD(soft) - RMSD(argmin) to the native (ORACLE label, evaluation only), and the native-free T*
(smallest T with ESS >= 3).  Output: research/results/RAW/g1_transmission/<crop>.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.protein import energy as EN   # noqa: E402
from qapf.sampling import hrex as H     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TS = (1.0, 2.0, 4.0, 8.0, 16.0, 32.0)


def kabsch(A, B):
    """superpose A onto B; returns (A_aligned, rmsd)."""
    ca, cb = A.mean(0), B.mean(0)
    A0, B0 = A - ca, B - cb
    U, S, Vt = np.linalg.svd(A0.T @ B0)
    d = np.sign(np.linalg.det(U @ Vt))
    Dm = np.diag([1, 1, d])
    R = U @ Dm @ Vt
    Aa = A0 @ R + cb
    return Aa, float(np.sqrt(((Aa - B) ** 2).sum(1).mean()))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crop", required=True)
    ap.add_argument("--restarts", type=int, default=64)
    ap.add_argument("--iters", type=int, default=2000)
    ap.add_argument("--clust", type=float, default=2.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--max-modes", type=int, default=40)
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "g1_transmission"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fj = os.path.join(a.out, a.crop + ".json")
    if os.path.exists(fj):
        print("exists"); return
    t0 = time.time()
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", a.crop + ".npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    rng = np.random.default_rng(a.seed)
    x0 = H.ExactPrior(en, 1.0).sample(a.restarts, rng)
    X = x0
    for _ in range(3):                                   # memory restarts (A80 is piecewise smooth; see prereg R2-T)
        X, E, _ = EN.lbfgs(en, X, iters=400, tol=1e-12)
    E = np.asarray(E).ravel()
    C = en.coords(X)
    order = np.argsort(E)
    reps, counts = [], []
    for i in order:
        hit = next((c for c, r in enumerate(reps) if kabsch(C[i], C[r])[1] < a.clust), None)
        if hit is None:
            if len(reps) < a.max_modes:
                reps.append(int(i)); counts.append(1)
        else:
            counts[hit] += 1
    nat = np.asarray(z["ca"], float)
    modes = []
    for r in reps:
        xt = torch.as_tensor(X[r][None], dtype=torch.float64)
        Hm = torch.autograd.functional.hessian(lambda q: en.energy_t(q)[0], xt)[0, :, 0, :].numpy()
        lam = np.linalg.eigvalsh(0.5 * (Hm + Hm.T))
        g = float(np.linalg.norm(en(X[r][None], grad=True)[1])) if callable(en) else None
        modes.append(dict(idx=r, E=float(E[r]), lam=lam, n_nonpos=int((lam <= 0).sum()), grad_norm=g,
                          rmsd=kabsch(C[r], nat)[1]))
    ref = C[reps[0]]
    aligned = [kabsch(C[m["idx"]], ref)[0] for m in modes]
    rmsd_arg = modes[0]["rmsd"]
    perT = {}
    Ek = np.array([m["E"] for m in modes]); nk = np.array(counts[:len(modes)], float)
    for T in TS:
        for wname, lw in (("energy", -Ek / T), ("hits", -Ek / T + np.log(nk))):
            w = np.exp(lw - lw.max()); w /= w.sum()
            ess = float(1.0 / np.sum(w ** 2))
            soft = np.tensordot(w, np.stack(aligned), axes=1)
            rmsd_soft = kabsch(soft, nat)[1]
            perT[f"{wname}_{T}"] = dict(ess=ess, w_top=float(w.max()), rmsd_soft=rmsd_soft, gain=rmsd_arg - rmsd_soft,
                                        rmsd_wmode=float(np.dot(w, [m["rmsd"] for m in modes])))
    Tstar = {wn: next((T for T in TS if perT[f"{wn}_{T}"]["ess"] >= 3.0), TS[-1]) for wn in ("energy", "hits")}
    res = dict(crop=a.crop, L=L, restarts=a.restarts, iters=a.iters, n_modes=len(modes), E_best=modes[0]["E"],
               rmsd_argmin=rmsd_arg, min_mode_rmsd=float(min(m["rmsd"] for m in modes)),
               modes=[dict(E=m["E"], n_nonpos=m["n_nonpos"], rmsd=m["rmsd"], grad_norm=m["grad_norm"]) for m in modes],
               cluster_counts=counts, perT=perT, T_star_ess=Tstar,
               gain_Tstar={wn: perT[f"{wn}_{Tstar[wn]}"]["gain"] for wn in Tstar}, grad_evals=int(en.n_grad),
               secs=time.time() - t0)
    json.dump(res, open(fj + ".tmp", "w"))
    os.replace(fj + ".tmp", fj)
    print(json.dumps({k: res[k] for k in ("crop", "n_modes", "rmsd_argmin", "T_star_ess", "gain_Tstar", "secs")}))


if __name__ == "__main__":
    main()
