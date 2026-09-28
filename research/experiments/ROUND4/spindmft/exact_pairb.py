"""Test E-B (PREREG Addendum B): EXACT typicality echoes on b-aware clusters {a, b} U nearest-to-(a or b), N = 12..16,
same fused-pair Trotter circuit (dt = 2 us) as the reference (qapf.nmr.spins.exact_correlators), F_ab at 40/80/120 us.
One JSON per (probe, b, N); existing outputs are skipped (resumable).  Single-threaded."""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sdmft as S  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--series", default="245:7,19:8,19:9")
ap.add_argument("--Ns", default="12,14,16")
ap.add_argument("--R", default="12:8,14:4,16:2,18:1")
a = ap.parse_args()
Rmap = {int(k): int(v) for k, v in (x.split(":") for x in a.R.split(","))}
names, xyz_all, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
for ser in a.series.split(","):
    p, b = (int(x) for x in ser.split(":"))
    order = SP.cluster(xyz_all, p, len(xyz_all))
    X = xyz_all[order]
    dmin = np.minimum(np.linalg.norm(X - X[0], axis=1), np.linalg.norm(X - X[b], axis=1))
    rest = [int(i) for i in np.argsort(dmin, kind="stable") if i not in (0, b)]
    for N in (int(x) for x in a.Ns.split(",")):
        fo = os.path.join(HERE, "out", f"exact_pairb_p{p}_b{b}_N{N}.json")
        if os.path.exists(fo):
            print("exists", fo); continue
        C = sorted([0, b] + rest[: N - 2])
        D = SP.couplings(X[C], S.random_b0(1000))
        bl = C.index(b)
        t0 = time.time(); c0 = time.process_time()
        tt, Sab, ot, F = SP.exact_correlators(D, S.DT, 60, 0, [bl], n_rand=Rmap[N], rng=np.random.default_rng(2718 + N),
                                              otoc=True, record_every=20, otoc_every=20)
        out = dict(probe=p, b_world=b, N=N, C_world=C, C_names=[names[order[i]] for i in C], n_rand=Rmap[N],
                   err_typ=float(2.0 ** (-N / 2) / np.sqrt(Rmap[N])), times_us=[float(x * 1e6) for x in ot],
                   F=[float(x) for x in F[bl]], S=[float(x) for x in Sab[bl]],
                   M2_fraction_b_in_cluster=float((SP.couplings(X, S.random_b0(1000))[b, C] ** 2).sum()
                                                  / (SP.couplings(X, S.random_b0(1000))[b] ** 2).sum()),
                   wall_s=time.time() - t0, cpu_s=time.process_time() - c0)
        S.atomic_json(out, fo)
        print(json.dumps(dict(p=p, b=b, N=N, F=[round(x, 4) for x in out["F"]], cpu=round(out["cpu_s"], 1),
                              M2_in=round(out["M2_fraction_b_in_cluster"], 3))), flush=True)
