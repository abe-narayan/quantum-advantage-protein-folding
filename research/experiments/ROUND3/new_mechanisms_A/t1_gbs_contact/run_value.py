"""T1 value test: is the squared-hafnian (GBS, beta=2) proposal distribution privileged
against classically efficient samplers for contact-pair proposals? Checkpointed per cell.

usage: OMP_NUM_THREADS=1 python run_value.py [--quick]
"""
import os
import sys
import time
import zlib
import numpy as np

sys.path.insert(0, os.path.dirname(__file__))
from gbs_lib import (load_crop, native_contacts, haf_mcmc, greedy_matching, perturb_and_map,
                     edge_sampler, metrics, atomic_json)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_value.json")
CHAINS = ["2AB0A", "3BHLA", "3GAHA", "3M3PA", "3S0QA", "3TE4A", "3W42A", "4LPQA",
          "4PF3A", "5EMIA", "5O37A", "5QHWA", "7B4RA", "8AXJA", "9IXCA", "9PGXA"]
LS = [60, 100]
KS = [3, 5]
BETAS = [0.0, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 8.0]
TAUS = [0.1, 0.2, 0.3, 0.5, 0.75, 1.0, 1.5, 2.0]
N, THIN, BURN = 200, 20, 2000


def seed(*parts):
    return zlib.crc32("|".join(map(str, parts)).encode())


def main():
    quick = "--quick" in sys.argv
    res = {}
    if os.path.exists(OUT):
        import json
        with open(OUT) as f:
            res = json.load(f)
    chains = CHAINS[:1] if quick else CHAINS
    t0 = time.time()
    for L in LS:
        for ch in chains:
            W, ca = load_crop(ch, L)
            logW = np.log(W)
            native = native_contacts(ca)  # ORACLE
            for k in KS:
                key = f"{ch}|{L}|{k}"
                if key in res:
                    continue
                cell = {"n_native": len(native)}
                tc = time.time()
                for beta in BETAS:
                    rng = np.random.default_rng(seed(key, "beta", beta))
                    props, acc = haf_mcmc(logW, k, beta, N, THIN, BURN, rng)
                    m = metrics(props, native, k, np.random.default_rng(seed(key, "boot", beta)), W=W)
                    m["acc"] = acc
                    cell[f"beta{beta:g}"] = m
                g = greedy_matching(logW, k)
                cell["greedy"] = metrics([g] * N, native, k, np.random.default_rng(1), W=W)
                for tau in TAUS:
                    rng = np.random.default_rng(seed(key, "pam", tau))
                    cell[f"pam{tau:g}"] = metrics(perturb_and_map(logW, k, N, tau, rng), native, k,
                                                  np.random.default_rng(seed(key, "bootp", tau)), W=W)
                for gam in (1.0, 2.0, 3.0, 4.0):
                    rng = np.random.default_rng(seed(key, "edge", gam))
                    cell[f"edge{gam:g}"] = metrics(edge_sampler(W, k, N, gam, rng), native, k,
                                                   np.random.default_rng(seed(key, "boote", gam)), W=W)
                cell["secs"] = time.time() - tc
                res[key] = cell
                atomic_json(OUT, res)
                print(f"{key} done in {cell['secs']:.1f}s  b2 prec={cell['beta2']['prec']:.3f} cov={cell['beta2']['cov']}"
                      f"  b1 prec={cell['beta1']['prec']:.3f} cov={cell['beta1']['cov']}"
                      f"  pam1 prec={cell['pam1']['prec']:.3f} cov={cell['pam1']['cov']}"
                      f"  greedy prec={cell['greedy']['prec']:.3f}  [{time.time()-t0:.0f}s]", flush=True)


if __name__ == "__main__":
    main()
