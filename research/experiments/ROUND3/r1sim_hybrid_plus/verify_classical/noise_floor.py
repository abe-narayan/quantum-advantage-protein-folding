"""Noise floor of the lane's kill rule.  The reference F_ref is ONE Haar typicality vector (scripts/nmr_cone.py,
rng seed 12345), so even the exact answer differs from it by ~2^{-N/2} per point.  Here: deterministic sector-exact F
for the full N = 12 nested cluster (all four instrument sites) vs the N = 12 typicality reference (same seed/code), max
over the lane's window (80-320 us, 7 times x 4 sites = 28 points), in units of 2^{-N/2}; then the implied max-norm
floor at N = 16 / 18.  Uses the subcluster.py cache (near12 = full N=12 cluster), computing it if missing."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subcluster as S

cache = S.load_cache()
out = dict(rows=[])
for p in (19, 245):
    dm18, bs, _ = S.C.setup("1UBQ", p, 18)
    tt, R = S.ref(p, 12)
    w = (tt >= 79.9) & (tt <= 320.1)
    diffs = []
    for b in bs:
        f = S.exact_sub(cache, p, dm18, list(range(12)), b)
        diffs.append(f[w] - R[b][w])
    d = np.array(diffs)
    sd = 2 ** (-12 / 2)
    out["rows"].append(dict(probe=p, N=12, max_abs=float(np.abs(d).max()), rms=float(np.sqrt((d ** 2).mean())),
                            max_over_sd=float(np.abs(d).max() / sd), rms_over_sd=float(np.sqrt((d ** 2).mean()) / sd),
                            diffs=[[round(float(x), 4) for x in r] for r in d]))
    print(p, "N12 exact-vs-typicality: max", round(float(np.abs(d).max()), 4), "rms", round(float(np.sqrt((d**2).mean())), 4),
          "max/SD", round(float(np.abs(d).max() / sd), 2), "rms/SD", round(float(np.sqrt((d**2).mean()) / sd), 2))
ratio = float(np.mean([r["max_over_sd"] for r in out["rows"]]))
rms = float(np.mean([r["rms_over_sd"] for r in out["rows"]]))
for N in (16, 18):
    out[f"implied_ref_floor_N{N}"] = dict(sd=2 ** (-N / 2), rms=rms * 2 ** (-N / 2), max_28pts=ratio * 2 ** (-N / 2))
    print(f"N={N}: per-point SD 2^-N/2 = {2**(-N/2):.4f}; measured-ratio rms {rms*2**(-N/2):.4f}; implied max over 28 pts {ratio*2**(-N/2):.4f}")
json.dump(out, open(os.path.join(HERE, "noise_floor.json"), "w"), indent=1)
