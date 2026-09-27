"""G1 companion: mode census of the learned-energy posterior by multistart decoding (the strongest classical counter to
tempering bottlenecks: find the modes by optimisation, then sample each locally and reweight).

For one crop: R restarts drawn from the exact learned prior (lam=0 distribution, T), each relaxed with the vendored
batched L-BFGS (A80 decoder) on the full energy; minima clustered by CA-RMSD (threshold --clust).  Records the
discovery curve (#distinct modes within dE of the best vs #restarts), energies, basin sizes, Laplace log-volumes
(log det of the Hessian of E in internal coordinates at each minimum -> relative mode masses at temperature T), and
the RMSD of each mode to the native (evaluation only).

Usage: python scripts/g1_mode_census.py --crop 5O37A_60 --restarts 256
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np
import torch

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.protein import energy as EN   # noqa: E402
from qapf.sampling import hrex as H     # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def hessian_logdet(en, x):
    """log det of the Hessian of E (internal coordinates) at x via autograd (dense; D = 2L-5)."""
    xt = torch.as_tensor(x[None], dtype=torch.float64)
    f = lambda z: en.energy_t(z)[0]
    Hm = torch.autograd.functional.hessian(f, xt)[0, :, 0, :].numpy()
    Hm = 0.5 * (Hm + Hm.T)
    w = np.linalg.eigvalsh(Hm)
    npos = int((w > 1e-6).sum())
    return float(np.sum(np.log(np.clip(w, 1e-6, None)))), int((w <= 1e-6).sum())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crop", required=True)
    ap.add_argument("--restarts", type=int, default=256)
    ap.add_argument("--iters", type=int, default=200)
    ap.add_argument("--T", type=float, default=1.0)
    ap.add_argument("--clust", type=float, default=2.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--hess-top", type=int, default=12, help="Laplace volumes for the best K modes")
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "g1_modes"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.crop}_R{a.restarts}_s{a.seed}"
    fj = os.path.join(a.out, tag + ".json")
    if os.path.exists(fj):
        print("exists", fj); return
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", a.crop + ".npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    rng = np.random.default_rng(a.seed)
    t0 = time.time()
    prior = H.ExactPrior(en, a.T)
    x0 = prior.sample(a.restarts, rng)
    xs, Es = [], []
    for s in range(0, a.restarts, 64):
        xr, er = EN.relax(en, x0[s:s + 64], iters=a.iters)
        xs.append(np.asarray(xr)); Es.append(np.asarray(er).ravel())
    X = np.concatenate(xs); E = np.concatenate(Es)
    C = en.coords(X)
    order = np.argsort(E)
    # greedy clustering in energy order; discovery curve in restart order
    reps, rep_E, members = [], [], []
    assign = np.full(len(E), -1)
    for i in order:
        for c, r in enumerate(reps):
            if kabsch_rmsd(C[i], C[r]) < a.clust:
                assign[i] = c; members[c].append(int(i)); break
        else:
            assign[i] = len(reps); reps.append(int(i)); rep_E.append(float(E[i])); members.append([int(i)])
    Emin = E.min()
    curve = {}
    for dE in (1.0, 5.0, 20.0, 1e9):
        seen, cnt = set(), []
        for i in range(len(E)):
            if E[i] <= Emin + dE:
                seen.add(int(assign[i]))
            cnt.append(len(seen))
        curve[str(dE)] = cnt
    first_best = int(np.argmax(np.array([assign[i] == assign[order[0]] for i in range(len(E))])))
    p_hit_best = float(np.mean(assign == assign[order[0]]))
    within = {str(d): float(np.mean(E <= Emin + d)) for d in (1.0, 5.0, 20.0)}
    nat = np.asarray(z["ca"], float)
    k = min(a.hess_top, len(reps))
    laplace = []
    for c in range(k):
        ld, nzero = hessian_logdet(en, X[reps[c]])
        laplace.append(dict(mode=c, E=rep_E[c], logdetH=ld, n_nonpos=nzero, size=len(members[c]),
                            rmsd_native=kabsch_rmsd(C[reps[c]], nat)))
    # NOTE: Laplace masses are NOT computed: the learned energy has flat directions (tail bins, termini), so
    # the Hessian at L-BFGS endpoints has non-positive eigenvalues (n_nonpos) and Laplace volumes are ill-defined.
    # evaluation only: RMSD of every mode representative to the native; transmission = Spearman(E, RMSD) over modes
    mode_rmsd = [kabsch_rmsd(C[r], nat) for r in reps]
    from scipy.stats import spearmanr
    rho = float(spearmanr(rep_E, mode_rmsd).correlation) if len(reps) > 3 else None
    best_rmsd_mode = int(np.argmin(mode_rmsd))
    res_extra = dict(mode_rmsd=mode_rmsd[:2000], spearman_E_rmsd_modes=rho, rank_of_best_rmsd_mode_by_E=best_rmsd_mode,
                     min_mode_rmsd=float(min(mode_rmsd)))
    res = dict(crop=a.crop, L=L, T=a.T, restarts=a.restarts, iters=a.iters, clust=a.clust, n_modes=len(reps), **res_extra,
               E_best=float(Emin), mode_E=rep_E[:2000], mode_sizes=[len(m) for m in members[:2000]],
               first_seen_restart=[int(min(m)) for m in members[:2000]],
               discovery_curve=curve, first_hit_best_mode=first_best, p_hit_best_mode=p_hit_best,
               frac_within_dE=within, laplace=laplace,
               best_mode_rmsd_native=kabsch_rmsd(C[order[0]], nat),
               grad_evals=int(en.n_grad), secs=time.time() - t0)
    json.dump(res, open(fj, "w"))
    print(json.dumps({k: res[k] for k in ("crop", "n_modes", "E_best", "first_hit_best_mode", "best_mode_rmsd_native", "secs")}))


if __name__ == "__main__":
    main()
