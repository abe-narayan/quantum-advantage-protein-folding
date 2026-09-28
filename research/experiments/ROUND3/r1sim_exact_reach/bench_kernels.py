"""Correctness check (one Trotter step vs spins.apply_step, up to the factored global phase) and per-step wall-clock /
memory benchmark of the kernels vs N.  Single-threaded.  Writes bench_kernels.json (atomic, after every row).
Usage: python bench_kernels.py --Ns 12 14 16 18 20 22 --reps 2
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
import tracemalloc

import numpy as np

import fastecho as FE
from fastecho import SP

HERE = os.path.dirname(os.path.abspath(__file__))


def check_step(N=10, probe=19):
    dm, bs, _, _ = FE.load_instance("1UBQ", probe, N)
    pairs = SP.pair_list(dm, 2e-6)
    psi = FE.reference_psi0(N)
    ref = SP.apply_step(psi.copy().reshape((2,) * N), N, pairs).reshape(-1)
    ph = np.prod([complex(math.cos(p[2] / 2), -math.sin(p[2] / 2)) for p in pairs])
    full = FE.FullKernel(N, pairs).step(psi.copy()) * ph
    pc = FE.popcounts(N)
    sec = np.zeros_like(psi)
    for k in range(N + 1):
        idx = np.nonzero(pc == k)[0]
        K = FE.SectorKernel(N, idx, pairs)
        v = psi[idx].copy()
        sec[idx] = K.step(v) * ph
    inv = FE.FullKernel(N, pairs).step(FE.FullKernel(N, pairs).step(psi.copy()), inverse=True)
    return dict(full_vs_ref=float(np.abs(full - ref).max()), sector_vs_ref=float(np.abs(sec - ref).max()),
                inverse_roundtrip=float(np.abs(inv - psi).max()))


def time_kernel(kind, N, dtype, reps, probe=19):
    dm, _, _, _ = FE.load_instance("1UBQ", probe, N)
    pairs = SP.pair_list(dm, 2e-6)
    tracemalloc.start()
    t_build = time.time()
    if kind == "full":
        K = FE.FullKernel(N, pairs, dtype)
        v = (np.random.default_rng(1).standard_normal(1 << N) + 0j).astype(dtype)
        dim = 1 << N
    else:
        k = N // 2
        idx = FE.sector_index(N, k)
        K = FE.SectorKernel(N, idx, pairs, dtype, itype=np.intp if kind == "sector" else np.int32)
        v = (np.random.default_rng(1).standard_normal(len(idx)) + 0j).astype(dtype)
        dim = len(idx)
    t_build = time.time() - t_build
    v /= np.linalg.norm(v)
    K.step(v)                                      # warm-up
    ts = []
    for _ in range(reps):
        t = time.perf_counter(); K.step(v); ts.append(time.perf_counter() - t)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    sec = min(ts)
    return dict(kind=kind, N=N, dtype=np.dtype(dtype).name, dim=int(dim), n_pairs=len(pairs), sec_per_step=sec,
                ns_per_pair_elem=1e9 * sec / (len(pairs) * dim / 2), build_s=t_build, peak_traced_MB=peak / 1e6,
                norm_err=float(abs(np.linalg.norm(v) - 1)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--Ns", type=int, nargs="+", default=[12, 14, 16, 18, 20])
    ap.add_argument("--reps", type=int, default=2)
    ap.add_argument("--kinds", nargs="+", default=["sector", "sector32", "full"])
    ap.add_argument("--dtypes", nargs="+", default=["complex128", "complex64"])
    ap.add_argument("--out", default=os.path.join(HERE, "bench_kernels.json"))
    a = ap.parse_args()
    res = json.load(open(a.out)) if os.path.exists(a.out) else dict(rows=[])
    if "check" not in res:
        res["check"] = check_step()
        print(res["check"], flush=True)
    for N in a.Ns:
        for kind in a.kinds:
            for dt in a.dtypes:
                if any(r["kind"] == kind and r["N"] == N and r["dtype"] == dt for r in res["rows"]):
                    continue
                r = time_kernel(kind, N, np.dtype(dt), a.reps)
                res["rows"].append(r)
                print(json.dumps(r), flush=True)
                json.dump(res, open(a.out + ".tmp", "w"), indent=1)
                os.replace(a.out + ".tmp", a.out)


if __name__ == "__main__":
    main()
