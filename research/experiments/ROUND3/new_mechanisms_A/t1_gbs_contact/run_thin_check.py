"""Attack on T1: is the GBS coverage deficit an MCMC-autocorrelation artefact?
A physical GBS device emits i.i.d. samples. Re-run beta=2 and beta=1 with 5x and 20x thinning
on all 16 chains (L=100, k=3) and compare coverage/precision with the thin=20 production run."""
import json
import os
import sys
import time
import zlib
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from gbs_lib import load_crop, native_contacts, haf_mcmc, metrics, atomic_json
from run_value import CHAINS

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_thin_check.json")


def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    t0 = time.time()
    L, k, N = 100, 3, 200
    for ch in CHAINS:
        W, ca = load_crop(ch, L)
        logW = np.log(W)
        native = native_contacts(ca)
        for beta in (1.0, 2.0):
            for thin in (100, 400):
                key = f"{ch}|{L}|{k}|beta{beta:g}|thin{thin}"
                if key in res:
                    continue
                rng = np.random.default_rng(zlib.crc32(key.encode()))
                props, acc = haf_mcmc(logW, k, beta, N, thin, 2000, rng)
                m = metrics(props, native, k, np.random.default_rng(7), W=W)
                m["acc"] = acc
                res[key] = m
                atomic_json(OUT, res)
        print(ch, f"{time.time()-t0:.0f}s", flush=True)


if __name__ == "__main__":
    main()
