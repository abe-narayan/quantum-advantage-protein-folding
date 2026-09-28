"""ROUND3 / hardness_what_it_takes: single-thread micro-benchmark of c(L), seconds per energy+gradient evaluation of the
A80 energy (src/qapf/protein/energy.py), batched (B = 64, as in every L-BFGS call of the census/DG) and single-structure.
Synthetic Dirichlet distogram / head tables of the right shapes (timing depends only on L).  NOTE: run on a LOADED
machine (governor at ~95% CPU), so times are upper bounds on an idle core; T2's A-c values are the reference.
Output: bench_c.json.  L capped at 200 to respect the 2 GB per-run memory limit (tables are ~2*n_pairs*1001 doubles).
"""
from __future__ import annotations

import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))
from qapf.protein import energy as EN  # noqa: E402


def main():
    rng = np.random.default_rng(1)
    out = []
    for L in (60, 100, 150, 200):
        P = rng.dirichlet(np.ones(28), size=(L, L)).astype(np.float32)
        Pb = rng.dirichlet(np.ones(28), size=(L, L)).astype(np.float32)
        tt = rng.dirichlet(np.ones(9 * 24), size=L).reshape(L, 9, 24).astype(np.float32)
        en = EN.Energy(dict(prob=P, prob_cb=Pb, theta_tau_prob=tt), L)
        D = 2 * L - 5
        x = np.concatenate([np.radians(rng.uniform(80, 150, (64, L - 2))), np.radians(rng.uniform(-180, 180, (64, L - 3)))], 1)
        en(x[:4])  # warm-up
        tb, ts = [], []
        for _ in range(5):
            t = time.perf_counter(); en(x); tb.append((time.perf_counter() - t) / 64)
        for _ in range(10):
            t = time.perf_counter(); en(x[:1]); ts.append(time.perf_counter() - t)
        row = dict(L=L, D=D, c_batched64_s=float(min(tb)), c_batched64_median_s=float(np.median(tb)),
                   c_single_s=float(min(ts)), c_single_median_s=float(np.median(ts)))
        out.append(row)
        print(json.dumps(row), flush=True)
        del en
    rows = list(out)
    Ls = np.array([r["L"] for r in rows], float)
    for key in ("c_batched64_s", "c_single_s"):
        y = np.array([r[key] for r in rows])
        b, a = np.polyfit(np.log(Ls), np.log(y), 1)
        out.append(dict(fit=key, exponent=float(b), prefactor=float(np.exp(a))))
        print(key, "exponent", round(b, 2))
    tmp = os.path.join(HERE, "bench_c.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "bench_c.json"))


if __name__ == "__main__":
    main()
