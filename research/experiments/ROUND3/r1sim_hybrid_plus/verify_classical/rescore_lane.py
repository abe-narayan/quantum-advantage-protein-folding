"""Noise-aware re-score of the lane's 37 CQC run files (../out/*.json): per (b, t) in [80, 320] us,
LB = |F_method - F_ref| - 2.5 * sqrt(SE_method^2 + SD_ref^2), SD_ref = 0.64 * 2^{-N/2} (the larger measured rms/SD
ratio, noise_floor.json).  max LB > sigma means the method's bias exceeds sigma at >= 2.5 combined SE somewhere."""
import glob, json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subcluster as S
rows = []
for f in sorted(glob.glob(os.path.join(os.path.dirname(HERE), "out", "*.json"))):
    d = json.load(open(f))
    tt, R = S.ref(d["probe"], d["N"])
    sdref = 0.64 * 2 ** (-d["N"] / 2)
    for est in ("F_tdh", "F_core"):
        e, lb = [], []
        for k, t in zip(d["ks"], d["times_us"]):
            if not (79.9 <= t <= 320.1):
                continue
            ti = int(np.argmin(abs(tt - t)))
            for b, v in d["res"][str(k)][est].items():
                se = v[1] if v[1] == v[1] else 0.0
                e.append(abs(v[0] - R[int(b)][ti])); lb.append(abs(v[0] - R[int(b)][ti]) - 2.5 * np.hypot(se, sdref))
        rows.append(dict(file=os.path.basename(f), est=est, probe=d["probe"], N=d["N"], max_err=round(float(max(e)), 4),
                         max_lb=round(float(max(lb)), 4)))
best = {}
for r in rows:
    k = (r["probe"], r["N"])
    if k not in best or r["max_err"] < best[k]["max_err"]:
        best[k] = r
out = dict(n_rows=len(rows), n_significant=int(sum(r["max_lb"] > 0.01 for r in rows)),
           best_per_cell={f"p{k[0]}_N{k[1]}": v for k, v in sorted(best.items())}, rows=rows)
json.dump(out, open(os.path.join(HERE, "rescore_lane.json"), "w"), indent=1)
print(out["n_significant"], "of", out["n_rows"], "lane rows fail at >= 2.5 combined SE")
for k, v in out["best_per_cell"].items():
    print(k, v["file"], v["est"], "max_err", v["max_err"], "LB", v["max_lb"])
