"""Resource auditor: re-run the lane's CQC method (../cqc_echo.py, unmodified) at new (probe, N, partition) points,
writing ONLY under verify_resource/out_cqc/.  Purpose: does the exact-core size k needed for a given error grow with N
(the lane's 'exact simulation in disguise' inference), i.e. is kls12 at N = 18 as good as kls12 at N = 16 (0.035)?
Checkpoint after every echo time (atomic, via cqc_echo.echo(save=...)).
Usage: python cqc_run.py --probe 19 --N 18 --bath kls12 --M 48
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import cqc_echo as C  # noqa: E402


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--core", default="x")
    ap.add_argument("--bath", default="kls12")
    ap.add_argument("--ba", default="none")
    ap.add_argument("--M", type=int, default=48)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--times-us", default="80,160,240,320")
    ap.add_argument("--dt", type=float, default=2e-6)
    a = ap.parse_args()
    dm, bs, _ = C.setup("1UBQ", a.probe, a.N)
    groups = C.partition(dm, bs, a.core, a.bath)
    q = C.CQC(dm, groups, a.dt, a.ba)
    ks = [int(round(float(t) * 1e-6 / a.dt)) for t in a.times_us.split(",")]
    od = os.path.join(HERE, "out_cqc"); os.makedirs(od, exist_ok=True)
    fj = os.path.join(od, f"1UBQ_p{a.probe}_N{a.N}_{a.bath}_{a.ba}_M{a.M}_s{a.seed}.json")
    if os.path.exists(fj):
        print("exists", fj); return
    ck = fj + ".ckpt.json"
    state = json.load(open(ck)) if os.path.exists(ck) else {}

    def save(res):
        json.dump(res, open(ck + ".tmp", "w")); os.replace(ck + ".tmp", ck)
    t0 = time.process_time(); w0 = time.time()
    print(json.dumps({"groups": groups, "sizes": [len(g) for g in groups]}), flush=True)
    res = C.echo(q, bs, ks, a.M, a.seed, state=state, save=save)
    d2 = dm ** 2
    intra = sum(d2[i, j] for g in groups for i in g for j in g if i < j)
    tot = sum(d2[i, j] for i in range(a.N) for j in range(i + 1, a.N))
    out = dict(probe=a.probe, N=a.N, bath=a.bath, ba=a.ba, M=a.M, seed=a.seed, bs=bs, groups=groups,
               group_sizes=[len(g) for g in groups], intra_d2_fraction=intra / tot, ks=ks,
               times_us=[k * a.dt * 1e6 for k in ks], res=res,
               secs_total=float(sum(res[str(k)]["secs"] for k in ks)),
               cpu_this_call=time.process_time() - t0, wall_this_call=time.time() - w0)
    json.dump(out, open(fj + ".tmp", "w"), indent=1); os.replace(fj + ".tmp", fj)
    os.remove(ck)
    print(json.dumps({"file": os.path.basename(fj), "secs": round(out["secs_total"], 1), "sizes": out["group_sizes"],
                      "intra_d2": round(intra / tot, 3)}))


if __name__ == "__main__":
    main()
