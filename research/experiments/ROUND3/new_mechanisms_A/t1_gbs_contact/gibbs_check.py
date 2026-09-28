"""Check heat-bath sampler mixing: coverage/precision vs sweeps per sample, vs thin=400 Metropolis."""
import json, os, sys, time, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gbs_lib import load_crop, native_contacts, haf_gibbs, metrics, atomic_json
from run_value import CHAINS
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_gibbs_check.json")
res = json.load(open(OUT)) if os.path.exists(OUT) else {}
t0 = time.time()
for ch in CHAINS[:8]:
    W, ca = load_crop(ch, 100); native = native_contacts(ca)
    for sweeps in (1, 3, 10):
        key = f"{ch}|100|3|beta2|sweeps{sweeps}"
        if key in res: continue
        rng = np.random.default_rng(zlib.crc32(key.encode()))
        props = haf_gibbs(W, 3, 2.0, 200, sweeps, 20, rng)
        res[key] = metrics(props, native, 3, np.random.default_rng(7), W=W)
        atomic_json(OUT, res)
    print(ch, f"{time.time()-t0:.0f}s", flush=True)
thin = json.load(open(os.path.join(HERE, "results_thin_check.json")))
for ch in CHAINS[:8]:
    print(ch, [res[f"{ch}|100|3|beta2|sweeps{s}"]["cov"] for s in (1,3,10)], thin[f"{ch}|100|3|beta2|thin400"]["cov"],
          [round(res[f"{ch}|100|3|beta2|sweeps{s}"]["prec"],3) for s in (1,3,10)], round(thin[f"{ch}|100|3|beta2|thin400"]["prec"],3))
