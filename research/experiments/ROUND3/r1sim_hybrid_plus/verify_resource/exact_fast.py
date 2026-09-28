"""Resource auditor: an EFFICIENT exact typicality echo (same circuit/geometry/metric as scripts/nmr_cone.py), used for
  (1) an exact-vs-reference noise floor of the lane kill rule (independent Haar vectors, seeds != 12345), and
  (2) a like-for-like wall-clock of exact simulation vs the lane's CQC k=12 run on the same loaded host.
Differences from nmr_cone.py (cost only, same numbers): only the 4 window times (80/160/240/320 us), forward evolution
is incremental (shared by all times), all columns (R vectors x (1 + |bs|) branches) are evolved as one batched array
with the vectorised pair kernel of ../cqc_echo.py (`pair_gates`, identical convention to spins.apply_step).
Seed 12345 reproduces the reference vector exactly (validation).  Checkpoint after every time point (atomic).
Usage: python exact_fast.py --probe 19 --N 16 --seeds 1,2
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cqc_echo as C  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--seeds", default="1,2")
    ap.add_argument("--ks", default="40,80,120,160")
    ap.add_argument("--dt", type=float, default=2e-6)
    a = ap.parse_args()
    seeds = [int(s) for s in a.seeds.split(",")]
    ks = [int(k) for k in a.ks.split(",")]
    dm, bs, _ = C.setup("1UBQ", a.probe, a.N)
    N, D = a.N, 1 << a.N
    pairs = SP.pair_list(dm, a.dt)
    nb = 1 + len(bs)
    tag = f"1UBQ_p{a.probe}_N{N}_seeds{'-'.join(map(str, seeds))}"
    fj = os.path.join(HERE, "out_exact", tag + ".json")
    os.makedirs(os.path.dirname(fj), exist_ok=True)
    if os.path.exists(fj):
        print("exists", fj); return
    ck = fj + ".ckpt.json"
    st = json.load(open(ck)) if os.path.exists(ck) else {"done": {}, "secs": {}}

    def save():
        json.dump(st, open(ck + ".tmp", "w")); os.replace(ck + ".tmp", ck)

    idx = np.arange(D)

    def zs(q):                                                 # diagonal of Z_q (qubit q = bit q of the row index)
        return 1.0 - 2.0 * ((idx >> q) & 1)

    X = np.empty((D, len(seeds) * nb), complex)
    for r, s in enumerate(seeds):
        rng = np.random.default_rng(s)
        v = rng.standard_normal((2,) * N) + 1j * rng.standard_normal((2,) * N)
        v = (v / np.linalg.norm(v)).reshape(D)
        for q in range(nb):
            X[:, r * nb + q] = v * (zs(bs[q - 1]) if q else 1.0)
    t_all = time.time()
    kcur, fwd_secs = 0, 0.0
    for k in ks:
        t0 = time.time()
        while kcur < k:                                        # incremental forward
            C.pair_gates(X, N, pairs); kcur += 1
        fwd_secs += time.time() - t0
        if str(k) in st["done"]:
            continue
        t1 = time.time()
        Y = X.copy()
        C.zmul_rows(Y, N, 0)
        for _ in range(k):
            C.pair_gates(Y, N, pairs, inverse=True)
        vals = {}
        for r, s in enumerate(seeds):
            y0 = Y[:, r * nb].copy()
            for q, b in enumerate(bs, start=1):
                lhs = y0 * zs(b)
                vals.setdefault(str(s), {})[str(b)] = float(np.real(np.vdot(lhs, Y[:, r * nb + q])))
        st["done"][str(k)] = vals
        st["secs"][str(k)] = dict(backward=time.time() - t1, forward_cum=fwd_secs)
        save()
        print(json.dumps({"k": k, "t_us": k * a.dt * 1e6, "vals": vals, "bwd_s": round(time.time() - t1, 1),
                          "fwd_cum_s": round(fwd_secs, 1)}), flush=True)
    out = dict(probe=a.probe, N=N, bs=bs, seeds=seeds, ks=ks, times_us=[k * a.dt * 1e6 for k in ks], D=D,
               n_pairs=len(pairs), columns=X.shape[1], F=st["done"], secs=st["secs"],
               wall_total_this_call=time.time() - t_all,
               step_applications=dict(forward=ks[-1], backward=sum(ks), columns=X.shape[1]))
    json.dump(out, open(fj + ".tmp", "w"), indent=1); os.replace(fj + ".tmp", fj)
    os.remove(ck)
    print(json.dumps({"file": os.path.basename(fj), "wall": round(out["wall_total_this_call"], 1)}))


if __name__ == "__main__":
    main()
