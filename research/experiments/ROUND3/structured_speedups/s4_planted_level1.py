"""S4 (planted-inference / Kikuchi precondition): does a LEVEL-1 (pairwise, spectral / stress) classical method already
recover the planted structure of the A80 learned-energy task?

Kikuchi-type quartic speedups (Schmidhuber et al. PRX 15 021077; Schmidhuber-Hastings 2607.29672) live only in the
regime where the level-1 spectral method FAILS but a level-l>1 Kikuchi method succeeds (signal between the
information and the level-1 computational threshold).  If level 1 already reaches the deepest known basin of the
energy, the task is outside that regime.

DEP arm (native-free): seeds from the ESM distogram only
  S0 classical MDS of `expected` distances; S1 its mirror image;
  S2 weighted stress majorisation (SMACOF, weights 1/max(sd,0.5)^2) from S0; S3 its mirror.
  Each seed -> ideal bonds -> internal coords -> the census relaxer (EN.relax, L-BFGS, 200 iters, same as the census).
  Compared (by ENERGY only) with the pre-registered G1 census (256 prior restarts, research/results/RAW/g1_modes).
ORACLE arm (labelled, evaluation only): CA-RMSD of seeds / relaxed seeds to the native; census best-mode RMSD.

Checkpoints per crop to s4_planted_level1.json (atomic).  Relaxed DEP coordinates -> s4_coords.npz (for S3).
"""
from __future__ import annotations

import argparse
import os

import numpy as np

from common import (EN, HERE, ROOT, CHAINS, Timer, atomic_json, fix_bonds, kabsch_rmsd, load_crop, load_json,
                    make_energy, mds_coords, oracle_native, x_from_ca)

OUT = os.path.join(HERE, "s4_planted_level1.json")
OUTC = os.path.join(HERE, "s4_coords.npz")
CENSUS = os.path.join(ROOT, "research", "results", "RAW", "g1_modes")


def smacof(D, W, X0, iters=150):
    L = len(D)
    V = -W.copy(); np.fill_diagonal(V, 0.0); np.fill_diagonal(V, -V.sum(1))
    Vp = np.linalg.pinv(V)
    X = X0.copy()
    for _ in range(iters):
        d = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)); np.fill_diagonal(d, 1.0)
        B = -W * D / np.maximum(d, 1e-6); np.fill_diagonal(B, 0.0); np.fill_diagonal(B, -B.sum(1))
        X = Vp @ B @ X
    return X


def census_record(crop):
    f = os.path.join(CENSUS, f"{crop}_R256_s0.json")
    if not os.path.exists(f):
        return None
    return load_json(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lengths", default="30,60,100,150")
    ap.add_argument("--budget-cpu", type=float, default=600.0, help="stop after this many CPU seconds")
    a = ap.parse_args()
    res = load_json(OUT, {"crops": {}})
    coords = dict(np.load(OUTC)) if os.path.exists(OUTC) else {}
    T = Timer()
    for Lr in [int(v) for v in a.lengths.split(",")]:
        for ch in CHAINS:
            crop = f"{ch}_{Lr}"
            if crop in res["crops"]:
                continue
            if T.cpu() > a.budget_cpu:
                print("budget reached"); atomic_json(OUT, res); return
            t = Timer()
            z, L = load_crop(crop)
            en = make_energy(z, L)
            D = np.asarray(z["expected"], float); D = 0.5 * (D + D.T); np.fill_diagonal(D, 0.0)
            sd = np.asarray(z["sd"], float); sd = 0.5 * (sd + sd.T)
            X0, lam = mds_coords(D)
            W = 1.0 / np.maximum(sd, 0.5) ** 2; np.fill_diagonal(W, 0.0)
            idx = np.arange(L - 1)
            W[idx, idx + 1] = W[idx + 1, idx] = 100.0
            Dm = D.copy(); Dm[idx, idx + 1] = Dm[idx + 1, idx] = EN.BOND
            X2 = smacof(Dm, W, X0)
            mir = np.array([-1.0, 1.0, 1.0])
            seeds = [X0, X0 * mir, X2, X2 * mir]
            xs = np.stack([x_from_ca(fix_bonds(S)) for S in seeds])
            E0, _ = en(xs, grad=False)
            ng0 = en.n_grad
            xr, Er = EN.relax(en, xs, iters=200)
            ngrad = en.n_grad - ng0
            Er = np.asarray(Er).ravel()
            kbest = int(np.argmin(Er))
            Cr = en.coords(xr)
            cen = census_record(crop)
            rec = dict(crop=crop, L=L, gram_top6=[float(v) for v in lam[:6]],
                       gram_neg_frac=float(-lam[lam < 0].sum() / np.abs(lam).sum()),
                       lam3_over_lam4=float(lam[2] / lam[3]),
                       frac_pos_mass_top3=float(lam[:3].sum() / lam[lam > 0].sum()),
                       E_seed_raw=[float(v) for v in E0], E_seed_relaxed=[float(v) for v in Er],
                       E_level1_best=float(Er[kbest]), best_seed=kbest, grad_evals_level1=int(ngrad),
                       cpu_s=t.cpu())
            if cen is not None:
                mE = np.asarray(cen["mode_E"], float); ms = np.asarray(cen["mode_sizes"], float)
                Eb = float(cen["E_best"])
                rec.update(census_E_best=Eb, census_n_modes=int(cen["n_modes"]),
                           census_p_hit_best=float(cen["p_hit_best_mode"]),
                           census_grad_evals=int(cen["grad_evals"]),
                           dE_level1_minus_census=float(Er[kbest] - Eb),
                           census_frac_restarts_leq_level1=float(ms[mE <= Er[kbest] + 1e-9].sum() / ms.sum()),
                           level1_reaches_best_known=bool(Er[kbest] <= Eb + 1.0),
                           level1_beats_census=bool(Er[kbest] < Eb - 1.0),
                           census_rank_of_level1=int((mE < Er[kbest] - 1.0).sum()))
            # ---------------- ORACLE (evaluation only; never used above) ----------------
            nat = oracle_native(z)
            rec["ORACLE"] = dict(rmsd_seed_raw=[kabsch_rmsd(fix_bonds(S), nat) for S in seeds],
                                 rmsd_seed_relaxed=[kabsch_rmsd(C, nat) for C in Cr],
                                 rmsd_level1_best_by_E=kabsch_rmsd(Cr[kbest], nat),
                                 census_best_mode_rmsd=(cen or {}).get("best_mode_rmsd_native"))
            res["crops"][crop] = rec
            coords[crop] = Cr[kbest]
            atomic_json(OUT, res)
            tmp = OUTC + ".tmp.npz"
            np.savez_compressed(tmp, **coords); os.replace(tmp, OUTC)
            print(crop, L, "E_l1", round(Er[kbest], 1), "census", rec.get("census_E_best"),
                  "dE", round(rec.get("dE_level1_minus_census", np.nan), 1),
                  "l3/l4", round(rec["lam3_over_lam4"], 2), "rmsd(ORACLE)", round(rec["ORACLE"]["rmsd_level1_best_by_E"], 2),
                  "cen_rmsd", rec["ORACLE"]["census_best_mode_rmsd"], f"{t.cpu():.1f}s", flush=True)
    atomic_json(OUT, res)


if __name__ == "__main__":
    main()
