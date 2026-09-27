"""Analyse R2-T (PREREG_G1_C1_Q4.md, v2 weightings): soft (posterior-averaged over modes) readout vs argmin.
Per L and weighting: paired gain = RMSD(argmin) - RMSD(soft) (positive = soft better), at the native-free T* (ESS >= 3)
and at each fixed T.  S33 statistical contract: MDE = 2.8016 * SE(mean gain); effect in MDE units = mean / MDE.
Kill (pre-registered): median gain at T* < 1.0 MDE at both L.   Writes research/results/PROCESSED/transmission_summary.json
"""
from __future__ import annotations

import glob
import json
import os
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def stats(g):
    g = np.asarray(g, float)
    if len(g) < 2:
        return dict(n=len(g), mean=float(g.mean()) if len(g) else None)
    se = g.std(ddof=1) / np.sqrt(len(g))
    mde = 2.8016 * se
    return dict(n=len(g), mean=float(g.mean()), median=float(np.median(g)), se=float(se), mde=float(mde),
                mean_over_mde=float(g.mean() / mde) if mde > 0 else None, median_over_mde=float(np.median(g) / mde) if mde > 0 else None,
                frac_positive=float((g > 0).mean()))


def main():
    rows = [json.load(open(f)) for f in glob.glob(os.path.join(ROOT, "research", "results", "RAW", "g1_transmission", "*.json"))]
    rows = [r for r in rows if isinstance(r.get("T_star_ess"), dict)]
    by = defaultdict(list)
    for r in rows:
        by[r["L"]].append(r)
    out = {}
    for L, rs in sorted(by.items()):
        o = dict(n_crops=len(rs), argmin_rmsd_median=float(np.median([r["rmsd_argmin"] for r in rs])),
                 best_mode_rmsd_median=float(np.median([r["min_mode_rmsd"] for r in rs])))
        for wn in ("energy", "hits"):
            o[f"{wn}_Tstar"] = stats([r["gain_Tstar"][wn] for r in rs])
            o[f"{wn}_fixedT"] = {T: stats([r["perT"][f"{wn}_{T}"]["gain"] for r in rs]) for T in ("1.0", "2.0", "4.0", "8.0", "16.0", "32.0")}
        o["kill_fires"] = all((o[f"{wn}_Tstar"].get("median_over_mde") or -1) < 1.0 for wn in ("energy", "hits"))
        out[str(L)] = o
        print(f"L={L} n={len(rs)} argmin RMSD median {o['argmin_rmsd_median']:.2f}  best-mode {o['best_mode_rmsd_median']:.2f}")
        for wn in ("energy", "hits"):
            s = o[f"{wn}_Tstar"]
            print(f"   {wn:6s} T*: mean gain {s.get('mean', float('nan')):+.3f} median {s.get('median', float('nan')):+.3f} "
                  f"MDE {s.get('mde', float('nan')):.3f} median/MDE {s.get('median_over_mde') or float('nan'):+.2f} frac+ {s.get('frac_positive', float('nan')):.2f}")
        print("   kill fires:", o["kill_fires"])
    os.makedirs(os.path.join(ROOT, "research", "results", "PROCESSED"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "research", "results", "PROCESSED", "transmission_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
