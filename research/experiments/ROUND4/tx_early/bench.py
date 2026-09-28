"""Micro-benchmark: fastecho.SectorKernel vs kernels.ClipSectorKernel on one sector (same vector, same gates).
Usage: python bench.py N k nsteps dtype   -> prints JSON (seconds per step, max |diff| between kernels)."""
import json
import sys
import time

import numpy as np

import kernels as KR
from kernels import FE, SP

N, k, ns, dt = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4]
dtype = np.dtype(dt)
dm, bs, names, _ = FE.load_instance("1UBQ", 19, N)
pairs = SP.pair_list(dm, 2e-6)
pc = FE.popcounts(N)
idx = np.nonzero(pc == k)[0]
del pc
rng = np.random.default_rng(1)
x = (rng.standard_normal(len(idx)) + 1j * rng.standard_normal(len(idx))).astype(dtype)
out = dict(N=N, k=k, dim=len(idx), dtype=dt, n_pairs=len(pairs))
ORDER = [("clip", KR.ClipSectorKernel), ("base", FE.SectorKernel)]
if len(sys.argv) > 5 and sys.argv[5] == "rev":
    ORDER = ORDER[::-1]
for name, cls in ORDER:
    t0 = time.process_time()
    K = cls(N, idx, pairs, dtype)
    out[name + "_build_s"] = time.process_time() - t0
    v = x.copy()
    t0 = time.process_time()
    for _ in range(ns):
        K.step(v)
    out[name + "_s_per_step"] = (time.process_time() - t0) / ns
    out[name + "_ns_per_pair_elem"] = out[name + "_s_per_step"] / (len(pairs) * len(idx) / 2) * 1e9
    out[name + "_v"] = v
    del K
out["max_abs_diff"] = float(np.max(np.abs(out.pop("clip_v") - out.pop("base_v"))))
try:
    import psutil
    out["peak_rss_GB"] = psutil.Process().memory_info().peak_wset / 1e9
except Exception:
    pass
print(json.dumps(out))
