"""Run one fast exact echo (checkpointed per sector; resumable; stops cleanly at --budget-s wall seconds).
Output: runs/<pdb>_p<probe>_N<N>_<mode>_<backend>_<dtype>_t<times>.json (+ .ckpt.json while partial).
Usage examples:
  python run_echo.py --probe 19 --N 14 --mode reference --dtype complex128                (all 8 echo times)
  python run_echo.py --probe 245 --N 20 --mode flip --dtype complex64 --times 80 160 --budget-s 800
  python run_echo.py --probe 19 --N 12 --mode reference --backend cheb --dtype complex128
Times are given in Trotter steps of dt = 2 us (reference grid: every 20 steps up to 160 = 320 us).
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np

import echo2
import fastecho as FE

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--mode", default="flip", choices=["flip", "reference"])
    ap.add_argument("--backend", default="trotter", choices=["trotter", "cheb"])
    ap.add_argument("--dtype", default="complex64")
    ap.add_argument("--times", type=int, nargs="*", default=None)
    ap.add_argument("--seed", type=int, default=12345)
    ap.add_argument("--budget-s", type=float, default=None)
    ap.add_argument("--driver", default="union", choices=["union", "sector"])
    ap.add_argument("--stop-at-step", type=int, default=None)
    a = ap.parse_args()
    times = a.times or list(range(20, 161, 20))
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    tag = f"{a.pdb}_p{a.probe}_N{a.N}_{a.mode}_{a.backend}_{a.dtype}_t{'-'.join(map(str, times))}"
    if a.driver == "union" and a.backend == "trotter":
        tag += "_U"
    if a.seed != 12345:
        tag += f"_s{a.seed}"
    out = os.path.join(HERE, "runs", tag + ".json")
    if os.path.exists(out):
        print("exists", out); return
    dm, bs, names, _ = FE.load_instance(a.pdb, a.probe, a.N)
    t0 = time.time()
    if a.driver == "union" and a.backend == "trotter":
        res = echo2.echo_union(dm, 2e-6, 0, bs, times, every=20, mode=a.mode, dtype=np.dtype(a.dtype), seed=a.seed,
                               ckpt_prefix=out, time_budget_s=a.budget_s, stop_at_step=a.stop_at_step,
                               log=lambda d: print(json.dumps(d), flush=True))
    else:
        res = echo2.echo(dm, 2e-6, 0, bs, times, every=20, mode=a.mode, dtype=np.dtype(a.dtype), seed=a.seed,
                         backend=a.backend, ckpt=out + ".ckpt.json", time_budget_s=a.budget_s,
                         log=lambda d: print(json.dumps(d), flush=True))
    try:
        import psutil
        res["peak_rss_GB"] = psutil.Process().memory_info().peak_wset / 1e9
    except Exception:
        pass
    res.update(pdb=a.pdb, probe=a.probe, bs=bs, names_bs=names, wall_this_invocation_s=time.time() - t0,
               err_typ_est=float((2.0 if a.mode == "flip" else 1.0) ** 0.5 * 2 ** (-a.N / 2)))
    if res["complete"]:
        json.dump(res, open(out + ".tmp", "w"), indent=1)
        os.replace(out + ".tmp", out)
        for ext in (".ckpt.json", ".ckpt.npz"):
            if os.path.exists(out + ext):
                os.remove(out + ext)
        print(json.dumps(dict(done=out, cpu_secs=round(res["cpu_secs_total"], 1),
                              peak_rss_GB=round(res.get("peak_rss_GB", 0), 3))))
    else:
        print(json.dumps(dict(partial=True, ckpt=out + ".ckpt.json")))


if __name__ == "__main__":
    main()
