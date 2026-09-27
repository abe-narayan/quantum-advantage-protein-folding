"""Program B: exact mechanism lab.  For landscape families (funnel, golf, hide-and-seek, persistence, SK) and sizes n,
compute EXACTLY: (i) the single-flip Metropolis relaxation time at the target temperature, (ii) the optimal simulated-
tempering relaxation time (a strong classical chain, exact log Z weights), (iii) the Szegedy phase gap of the best
classical chain, and (iv) classical vs QSA walk-step costs along a beta schedule (with the minimum consecutive
overlap QSA needs).  Then (v) apply the landscape-independent break-even: a quadratic speedup pays only when the
classical cost K exceeds K* = (a * C_q / C_c)^2; report K and the ratio K / K* for per-step cost ratios R = C_q/C_c
in {1e4, 1e6, 1e8} (placeholders to be replaced by research/theory/RESOURCE_MODELS.md numbers).

Usage: python scripts/synthetic_lab.py --family golf --nmax 14 --seeds 3
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.synthetic import exact_chains as X  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True)
    ap.add_argument("--nmin", type=int, default=6)
    ap.add_argument("--nmax", type=int, default=14)
    ap.add_argument("--seeds", type=int, default=3)
    ap.add_argument("--beta", type=float, default=1.0)
    ap.add_argument("--nbeta", type=int, default=12)
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "synthetic"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fj = os.path.join(a.out, f"{a.family}_n{a.nmin}-{a.nmax}.json")
    rows = []
    for n in range(a.nmin, a.nmax + 1, 2):
        nbr = X.hypercube_neighbors(n)
        for s in range(a.seeds):
            t0 = time.time()
            E = X.landscape(a.family, n, np.random.default_rng(1000 * n + s))
            P = X.metropolis_single_flip(E, nbr, a.beta); pi = X.gibbs(E, a.beta)
            d_m = X.spectral_gap(P, pi)
            betas = np.linspace(0.0, a.beta, a.nbeta)
            lz = X.log_partition(E, betas)
            Pst, pist = X.simulated_tempering(E, nbr, betas, lz)
            d_st = X.spectral_gap(Pst, pist)
            ann = X.annealing_costs(E, nbr, betas)
            best = max(d_m, d_st)
            K = 1.0 / best                                   # classical relaxation (walk steps) of best chain
            Kq = 1.0 / X.szegedy_phase_gap(best)
            row = dict(n=n, seed=s, t_rel_metropolis=1 / d_m, t_rel_st=1 / d_st, best_classical_steps=K,
                       qwalk_steps=Kq, speedup=K / Kq, anneal_classical=ann["classical"], anneal_quantum=ann["quantum"],
                       anneal_min_overlap2=ann["min_overlap2"],
                       K_over_Kstar={str(R): K / R ** 2 for R in (1e4, 1e6, 1e8)}, secs=time.time() - t0)
            rows.append(row)
            print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in row.items() if k != "K_over_Kstar"}), flush=True)
    json.dump(dict(family=a.family, beta=a.beta, rows=rows), open(fj, "w"))


if __name__ == "__main__":
    main()
