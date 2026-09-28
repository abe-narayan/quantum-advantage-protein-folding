"""T1 production v2 (supersedes the Metropolis beta-runs of run_value.py, which under-mixed:
acceptance 2-5%, coverage biased low for peaked beta; see results_thin_check.json).
Heat-bath hafnian sampler, near-i.i.d. samples. Classical i.i.d. comparators (greedy, perturb-and-MAP,
edge samplers) are reused from results_value.json (unchanged, i.i.d. by construction)."""
import json, os, sys, time, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gbs_lib import load_crop, native_contacts, haf_gibbs, metrics, atomic_json
from run_value import CHAINS
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_value_gibbs.json")
PLAN = {3: ([0.0, 0.5, 1.0, 2.0, 4.0, 8.0], 10), 5: ([0.0, 1.0, 2.0, 4.0], 5)}
def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    t0 = time.time()
    for L in (60, 100):
        for ch in CHAINS:
            W, ca = load_crop(ch, L); native = native_contacts(ca)  # native: ORACLE evaluation only
            for k, (betas, sweeps) in PLAN.items():
                for beta in betas:
                    key = f"{ch}|{L}|{k}|beta{beta:g}"
                    if key in res: continue
                    rng = np.random.default_rng(zlib.crc32(key.encode()))
                    props = haf_gibbs(W, k, beta, 200, sweeps, 20, rng)
                    m = metrics(props, native, k, np.random.default_rng(zlib.crc32((key + "b").encode())), W=W)
                    m["sweeps"] = sweeps
                    res[key] = m
                    atomic_json(OUT, res)
            print(L, ch, f"{time.time()-t0:.0f}s", flush=True)
if __name__ == "__main__":
    main()
