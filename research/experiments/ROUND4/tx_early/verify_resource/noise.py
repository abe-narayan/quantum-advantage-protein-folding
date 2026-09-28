"""Typicality-noise check at 40 us (step 20) for the ladder regressors dH, dfloor and for F.

Question: are the per-step H changes that the lane's N = 14..22 ladder samples (|dH| <= 0.0076 for N >= 14) real
cluster-size drift or typicality noise?  If they are noise, the ladder cannot show that F is insensitive to genuine
H drift (only to the floor).
Runs the lane's validated driver (tx_echo.run, unchanged; imported) with extra seeds, R = 1, complex64, steps = [20]
only.  Outputs go to verify_resource/runs (tx_echo.HERE is redirected); tx_echo checkpoints after every leg and
resumes.  Cost: ~5-6 CPU-min total, single-threaded, < 0.4 GB.
Usage: python noise.py [--budget-s S]   (re-run to resume; writes noise.json when complete)."""
import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import tx_echo as TX  # noqa: E402

TX.HERE = HERE                                  # redirect runs/ to verify_resource/runs
os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)

SEEDS = [9101, 9102, 9103, 9104]
PLAN = ([("honly", N, s) for N in (14, 16, 18, 20) for s in SEEDS]
        + [("echo", N, s) for N in (16, 18) for s in SEEDS[:3]])


def atomic(obj, path):
    with open(path + ".tmp", "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(path + ".tmp", path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget-s", type=float, default=1500.0)
    a = ap.parse_args()
    c0 = time.process_time()
    res = {}
    complete = True
    for p in (19, 245):
        for mode, N, s in PLAN:
            tag = f"VR_1UBQ_p{p}_N{N}_{mode}_R1_complex64_s{s}_t20"
            out = os.path.join(HERE, "runs", tag + ".json")
            if os.path.exists(out):
                with open(out) as f:
                    r = json.load(f)
                if r.get("complete"):
                    res[tag] = r
                    continue
            if time.process_time() - c0 > a.budget_s:
                complete = False
                continue
            r = TX.run("1UBQ", p, N, mode, [20], 1, np.dtype("complex64"), s, tag,
                       budget_s=a.budget_s - (time.process_time() - c0), log=lambda *_: None)
            TX.atomic_json(r, out)
            if not r.get("complete"):
                complete = False
                continue
            res[tag] = r
            print(tag, "H", round(r["H"][0], 4), "floor", round(r["floor"][0], 4),
                  "F", {b: round(v[0], 4) for b, v in r.get("F", {}).items()}, "cpu", round(r["cpu_s"], 1), flush=True)
    if not complete:
        print("INCOMPLETE: re-run to resume")
        return
    summ = dict(seeds=SEEDS, per_probe={})
    for p in (19, 245):
        pp = {}
        for N in (14, 16, 18, 20):
            Hs = [res[f"VR_1UBQ_p{p}_N{N}_honly_R1_complex64_s{s}_t20"]["H"][0] for s in SEEDS]
            fls = [res[f"VR_1UBQ_p{p}_N{N}_honly_R1_complex64_s{s}_t20"]["floor"][0] for s in SEEDS]
            pp[f"N{N}"] = dict(H=Hs, floor=fls, H_mean=float(np.mean(Hs)), sd_H_R1=float(np.std(Hs, ddof=1)),
                               floor_mean=float(np.mean(fls)), sd_floor_R1=float(np.std(fls, ddof=1)))
        for N in (16, 18):
            Fs = {b: [res[f"VR_1UBQ_p{p}_N{N}_echo_R1_complex64_s{s}_t20"]["F"][b][0] for s in SEEDS[:3]]
                  for b in ("1", "7", "8", "9")}
            pp[f"N{N}"].update(F=Fs, sd_F_R1={b: float(np.std(v, ddof=1)) for b, v in Fs.items()},
                               F_mean={b: float(np.mean(v)) for b, v in Fs.items()})
        summ["per_probe"][f"p{p}"] = pp
    summ["cpu_s_total"] = float(sum(r["cpu_s"] for r in res.values()))
    summ["peak_rss_GB"] = float(max(r.get("peak_rss_GB", 0) for r in res.values()))
    atomic(summ, os.path.join(HERE, "noise.json"))
    for p in (19, 245):
        for N in (14, 16, 18, 20):
            d = summ["per_probe"][f"p{p}"][f"N{N}"]
            print(f"p{p} N{N}: H {d['H_mean']:.4f} sd(R=1) {d['sd_H_R1']:.4f} floor {d['floor_mean']:.4f} sd {d['sd_floor_R1']:.5f}"
                  + (f" sdF {[round(v, 4) for v in d['sd_F_R1'].values()]}" if "sd_F_R1" in d else ""))
    print("cpu_s_total", round(summ["cpu_s_total"], 1), "peak GB", round(summ["peak_rss_GB"], 3))


if __name__ == "__main__":
    main()
