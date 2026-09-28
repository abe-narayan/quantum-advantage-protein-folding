"""ROUND3 / hardness_what_it_takes: symmetric adversarial check of the DG result.

The census minima (200 L-BFGS iterations) are under-relaxed; so are the DG minima.  polish_check.py showed that +800
iterations lower an endpoint by 0-450 nats.  To make sure that "DG reaches energies ~10^3 nats below 256 random-prior
restarts at L=150" is not an artefact of unequal relaxation, this script runs a fresh random-prior multistart
(exact learned prior, T=1, same sampler and L-BFGS as scripts/g1_mode_census.py, a different seed) with R restarts,
polishes the n_pol lowest endpoints with +800 iterations (exactly the DG polish), and compares the best polished
restart with the polished DG-E1 minimum (polish_results.json).  Native-free; RMSD to native is an ORACLE label.
Checkpoints after each crop (atomic tmp + replace).

Usage: OMP_NUM_THREADS=1 python ms_polish.py --crops 2AB0A_150,3GAHA_150 --R 64
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))
from qapf.protein import energy as EN  # noqa: E402
from qapf.sampling import hrex as H  # noqa: E402


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crops", required=True)
    ap.add_argument("--R", type=int, default=64)
    ap.add_argument("--n-pol", type=int, default=4)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--max-secs", type=float, default=470.0)
    ap.add_argument("--out", default="ms_polish_results.json")
    ap.add_argument("--fold", action="store_true", help="also save endpoints and fold-level hit fractions")
    a = ap.parse_args()
    out = os.path.join(HERE, a.out)
    res = json.load(open(out)) if os.path.exists(out) else []
    done = {r["crop"] for r in res}
    pol = {r["crop"]: r for r in json.load(open(os.path.join(HERE, "polish_results.json")))}
    t_start = time.time()
    for crop in a.crops.split(","):
        if crop in done:
            continue
        if time.time() - t_start > a.max_secs:
            print("time budget reached; stopping before", crop, flush=True); break
        t0 = time.time()
        z = np.load(os.path.join(REPO, "data", "instruments", "ladder", crop + ".npz"))
        L = len(str(z["seq"]))
        en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
        rng = np.random.default_rng(a.seed)
        x0 = H.ExactPrior(en, 1.0).sample(a.R, rng)
        xs, Es = [], []
        for s in range(0, a.R, 64):
            xr, er = EN.relax(en, x0[s:s + 64], iters=200)
            xs.append(np.asarray(xr)); Es.append(np.asarray(er).ravel())
        X = np.concatenate(xs); E = np.concatenate(Es)
        cost_ms = int(en.n_grad)
        idx = np.argsort(E)[:a.n_pol]
        g0 = en.n_grad
        xp, Ep = EN.relax(en, X[idx], iters=800)
        Ep = np.asarray(Ep).ravel()
        cost_pol = int(en.n_grad - g0)
        ib = int(np.argmin(Ep))
        # polished DG-E1 structure (recomputed deterministically from the stored endpoint, +800 iterations)
        ep = np.load(os.path.join(HERE, "endpoints", crop + ".npz"))
        arms = ep["arms"]; Ed = ep["E"]
        i = np.where(arms == "DG-E1")[0][np.argmin(Ed[arms == "DG-E1"])]
        xd, Edp = EN.relax(en, ep["x"][i:i + 1], iters=800)
        Xd = en.coords(xd)[0]; Xm = en.coords(xp[ib:ib + 1])[0]
        nat = np.asarray(z["ca"], float)
        row = dict(crop=crop, L=L, R=a.R, seed=a.seed, E_ms_200_best=float(E.min()), E_ms_200_sorted=[float(e) for e in np.sort(E)[:10]],
                   E_ms_polished=[float(e) for e in Ep], E_ms_polished_best=float(Ep.min()), cost_ms_restarts=cost_ms,
                   cost_ms_polish=cost_pol, E_DG_E1_polished=float(np.asarray(Edp).ravel()[0]),
                   E_DG_E1_polished_prev=pol.get(crop, {}).get("E_DG_E1_polished"),
                   dE_DGpol_minus_MSpol=float(np.asarray(Edp).ravel()[0] - Ep.min()),
                   rmsd_DGpol_vs_MSpol=kabsch_rmsd(Xd, Xm), rmsd_DGpol_ORACLE=kabsch_rmsd(Xd, nat),
                   rmsd_MSpol_ORACLE=kabsch_rmsd(Xm, nat), secs=time.time() - t0)
        if a.fold:
            # fold-level (structure-basin) multistart success: fraction of the R 200-iteration endpoints whose CA-RMSD
            # to the polished DG-E1 structure (resp. the best polished restart) is below r.  Native-free.
            C = en.coords(X)
            dD = np.array([kabsch_rmsd(c, Xd) for c in C]); dM = np.array([kabsch_rmsd(c, Xm) for c in C])
            row["fold_frac_vs_DGpol"] = {str(r): float(np.mean(dD < r)) for r in (2.0, 3.0, 4.0)}
            row["fold_frac_vs_MSpol"] = {str(r): float(np.mean(dM < r)) for r in (2.0, 3.0, 4.0)}
            row["rmsd_DG_E1_200_vs_DGpol"] = kabsch_rmsd(en.coords(ep["x"][i:i + 1])[0], Xd)
            os.makedirs(os.path.join(HERE, "endpoints_ms"), exist_ok=True)
            np.savez_compressed(os.path.join(HERE, "endpoints_ms", f"{crop}_R{a.R}_s{a.seed}.npz"), x=X, E=E,
                                x_pol=xp, E_pol=Ep, x_dgpol=xd)
        res.append(row)
        tmp = out + ".tmp"
        json.dump(res, open(tmp, "w"), indent=1)
        os.replace(tmp, out)
        print(json.dumps({k: (round(v, 2) if isinstance(v, float) else v) for k, v in row.items()
                          if k not in ("E_ms_200_sorted", "E_ms_polished")}), flush=True)


if __name__ == "__main__":
    main()
