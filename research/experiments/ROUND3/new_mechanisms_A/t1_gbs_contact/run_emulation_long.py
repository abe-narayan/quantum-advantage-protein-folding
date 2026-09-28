"""Follow-up to run_emulation.py: do the two double-dimer chains converge in vertex marginals
with longer runs (is the 0.1-0.35 max-marginal gap MC noise / slow mixing)? dmarg vs chain length."""
import json, os, sys, time, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gbs_lib import load_crop, MultiDimer, atomic_json
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_emulation_long.json")
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
CHECK = [250000, 500000, 1000000, 2000000, 4000000]
for ch, L, k in (("2AB0A", 100, 10), ("8AXJA", 150, 30)):
    key = f"{ch}|{L}|{k}"
    if key in res: continue
    t0 = time.time()
    W, _ = load_crop(ch, L); logW = np.log(W)
    mds = []
    for c in range(2):
        rng = np.random.default_rng(zlib.crc32(f"long|{key}|{c}".encode()))
        init = None
        if c == 1:
            v = rng.permutation(L)[:2 * k]; init = [tuple(sorted((int(v[2*i]), int(v[2*i+1])))) for i in range(k)]
        mds.append(MultiDimer(logW, k, 2, rng, init))
    burn = 200000
    for md in mds:
        for _ in range(burn): md.step()
    occ = [np.zeros(L), np.zeros(L)]; n = [0, 0]; rows = []; t = 0
    for target in CHECK:
        while t < target:
            for c, md in enumerate(mds):
                md.step()
                if t % 50 == 0:
                    occ[c][md.S] += 1; n[c] += 1
            t += 1
        m0, m1 = occ[0] / n[0], occ[1] / n[1]
        rows.append({"steps": target, "max_abs_marg_diff": float(np.abs(m0 - m1).max()),
                     "mean_abs_marg_diff": float(np.abs(m0 - m1).mean()), "secs": time.time() - t0})
        print(key, rows[-1], flush=True)
    res[key] = rows
    atomic_json(OUT, res)
