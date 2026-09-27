"""G1 (H-006) classical-first kill test, one crop: sample the learned-energy posterior with NRPT along the
prior->posterior path; record communication barrier, round trips, cost per independent sample, and structural
readouts (posterior expected RMSD, medoid, lowest-energy polished) against the native (evaluation only).

Usage: python scripts/g1_sample_crop.py --crop 5O37A_60 --T 1.0 --scans 3000 --seed 0 --out research/results/RAW/g1
Native coordinates are loaded ONLY for evaluation after sampling (never inside the sampler or its tuning).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.protein import energy as EN  # noqa: E402
from qapf.sampling import hrex as H    # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    d = np.sign(np.linalg.det(U @ Vt))
    S[-1] *= d
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crop", required=True)
    ap.add_argument("--T", type=float, default=1.0)
    ap.add_argument("--scans", type=int, default=3000)
    ap.add_argument("--leap", type=int, default=8)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--rung-factor", type=float, default=2.5)
    ap.add_argument("--max-rungs", type=int, default=96)
    ap.add_argument("--time-budget", type=float, default=None, help="seconds for production")
    ap.add_argument("--pivot", type=int, default=4, help="prior-proposal pivot moves per scan per rung")
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "g1"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.crop}_T{a.T:g}_s{a.seed}"
    fjson = os.path.join(a.out, tag + ".json")
    if os.path.exists(fjson):
        print("exists", fjson); return
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", a.crop + ".npz"))
    L = len(str(z["seq"]))
    out = dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"])
    en = EN.Energy(out, L)
    logs = []
    lg = lambda m: (logs.append(m), print(m, flush=True))
    t0 = time.time()
    # stage 1: pilot to estimate Lambda with 16 rungs
    pilot = H.run_nrpt(en, T=a.T, n_rungs=16, n_scans=0, n_leap=a.leap, tune_rounds=3, tune_scans=120,
                       seed=a.seed, log=lg, n_pivot=a.pivot)
    Lam0 = pilot["Lambda_tune"][-1]
    N = int(min(a.max_rungs, max(16, math.ceil(a.rung_factor * Lam0) + 2)))
    lg(f"pilot Lambda={Lam0:.2f} -> rungs N={N}")
    # stage 2: production with N rungs (fresh tuning of schedule at N)
    r = H.run_nrpt(en, T=a.T, n_rungs=N, n_scans=a.scans, n_leap=a.leap, tune_rounds=3, tune_scans=150,
                   seed=a.seed + 1000, log=lg, time_budget_s=a.time_budget, n_pivot=a.pivot)
    # penetration: deepest rung reached by any replica that started (production) at rung 0, and scans to reach top
    th = r["track_hist"]
    if len(th):
        lab0 = int(th[0][0])
        rung_of = np.array([int(np.where(row == lab0)[0][0]) for row in th])
        deepest = int(rung_of.max())
        first_top = int(np.argmax(rung_of == N - 1)) if (rung_of == N - 1).any() else None
    else:
        deepest, first_top = None, None
    # ---- evaluation (native used ONLY here)
    nat = np.asarray(z["ca"], float)
    S = r["samples"]
    nburn = len(S) // 5
    S = S[nburn:]
    X = en.coords(S) if len(S) else np.zeros((0, L, 3))
    rm = np.array([kabsch_rmsd(Xk, nat) for Xk in X]) if len(X) else np.array([])
    Etot = en(S, grad=False)[0] if len(S) else np.array([])
    ev = {}
    if len(X):
        k = min(len(X), 200)
        idx = np.linspace(0, len(X) - 1, k).astype(int)
        D = np.array([[kabsch_rmsd(X[i], X[j]) if j > i else 0.0 for j in idx] for i in idx])
        D = D + D.T
        med = idx[np.argmin(D.mean(1))]
        ibest = int(np.argmin(Etot))
        xpol, epol = EN.relax(en, S[ibest:ibest + 1], iters=200)
        Xpol = en.coords(xpol)[0]
        ev = dict(post_expected_rmsd=float(rm.mean()), post_rmsd_sd=float(rm.std()), post_best_rmsd=float(rm.min()),
                  medoid_rmsd=float(rm[med]), lowestE_rmsd=float(rm[ibest]), lowestE_polished_rmsd=kabsch_rmsd(Xpol, nat),
                  lowestE=float(Etot.min()), polishedE=float(np.asarray(epol).ravel()[0]),
                  pairwise_rmsd_mean=float(D[np.triu_indices(len(idx), 1)].mean()), n_samples_eval=int(len(X)))
    res = dict(crop=a.crop, L=L, T=a.T, seed=a.seed, rungs=N, Lambda_pilot=Lam0, Lambda=r["Lambda"],
               Lambda_tune=r["Lambda_tune"], rej=r["rej"].tolist(), lams=r["lams"].tolist(), hmc_acc=r["hmc_acc"].tolist(),
               eps=r["eps"].tolist(), round_trips=r["round_trips"], trip_scans=r["trip_scans"], scans=r["scans"],
               grad_evals_total=int(pilot["grad_evals"] + r["grad_evals"]), grad_evals_production=int(r["grad_evals"] - r["tune_grad_evals"]),
               cost_per_trip=(float(r["grad_evals"] - r["tune_grad_evals"]) / r["round_trips"]) if r["round_trips"] else None,
               upflow=r["upflow"].tolist(), pivot=a.pivot, deepest_rung_label0=deepest, first_top_scan_label0=first_top,
               secs=time.time() - t0, eval=ev, log=logs)
    np.savez_compressed(os.path.join(a.out, tag + ".npz"), samples=r["samples"], E_top=r["E_top"],
                        pair_trace=r["pair_trace"].astype(np.float32), track_hist=r["track_hist"])
    json.dump(res, open(fjson, "w"))
    print(json.dumps({k: res[k] for k in ("crop", "rungs", "Lambda", "round_trips", "scans", "cost_per_trip", "secs")}))
    print(json.dumps(ev))


if __name__ == "__main__":
    main()
