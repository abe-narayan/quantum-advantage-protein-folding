"""Classical verifier (ROUND4 spindmft lane): INDEPENDENT exact b-aware echoes.

Independent of the lane's exact_pairb.py in three ways:
  * kernel: ROUND3 fastecho SectorKernel via ROUND3 verify_classical/decomp_echo.run (flip-folded sectors, forward reuse)
    instead of qapf.nmr.spins.exact_correlators;
  * cluster ORDER (Trotter pair order): a -> 0, b -> 1, rest by min(d_ia, d_ib) (decomp_echo 'pairb'), instead of the
    lane's probe-rank order;
  * typicality vectors: different RNG streams.
Same physics: same 1UBQ protons, b0 = random_b0(1000), dt = 2 us first-order fused-pair Trotter circuit.
Also returns exact H, floor, X for the b-aware family (decomp_echo identity F = H + floor + X).

Families:
  pairb        : {a, b} U nearest to min(d_a, d_b)                     (the lane's b-aware family)
  greedy       : start {a, b}; repeatedly add the proton with the largest sum_{c in C} d_jc^2 (coupling-greedy family)
Checkpoint per magnetisation sector (decomp_echo, atomic tmp+replace); resumable.  Output: out/<tag>.json
Single-threaded: run with OMP_NUM_THREADS=MKL_NUM_THREADS=OPENBLAS_NUM_THREADS=1.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.abspath(os.path.join(HERE, "..", "..", "..", "ROUND3", "r1sim_exact_reach", "verify_classical"))
sys.path.insert(0, R3)
import decomp_echo as DE  # noqa: E402
from decomp_echo import FE, SP  # noqa: E402

_orig_load = DE.load_cluster


def greedy_cluster(pdb, probe, N, b_std):
    names, xyz, _ = SP.read_h_coords(os.path.join(FE.ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    std10 = SP.cluster(xyz, probe, 10)
    gb = int(std10[b_std])
    Dall = SP.couplings(xyz, FE.random_b0(1000))
    D2 = Dall ** 2
    C = [probe, gb]
    score = D2[probe] + D2[gb]
    score[C] = -1
    while len(C) < N:
        j = int(np.argmax(score))
        C.append(j)
        score = score + D2[j]
        score[C] = -1
    idx = np.array(C)
    dm = SP.couplings(xyz[idx], FE.random_b0(1000))
    return dm, [1], [names[i] for i in idx], xyz[idx], idx


def patched_load(pdb, probe, N, family="probe", b_std=None):
    if family == "greedy":
        return greedy_cluster(pdb, probe, N, b_std)
    return _orig_load(pdb, probe, N, family, b_std)


DE.load_cluster = patched_load


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--series", default="245:7,19:8,19:9")
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--family", default="pairb")
    ap.add_argument("--R", type=int, default=1)
    ap.add_argument("--dtype", default="complex64")
    ap.add_argument("--seed", type=int, default=90210)
    ap.add_argument("--budget-s", type=float, default=1500.0)
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    for ser in a.series.split(","):
        p, b = (int(x) for x in ser.split(":"))
        tag = f"fe_{a.family}_p{p}_b{b}_N{a.N}_R{a.R}_{a.dtype}"
        fo = os.path.join(HERE, "out", tag + ".json")
        if os.path.exists(fo):
            print("exists", tag)
            continue
        t0 = time.time(); c0 = time.process_time()
        res = DE.run("1UBQ", p, a.N, a.family, b, "echo", [20, 40, 60], a.R, np.dtype(a.dtype), a.seed,
                     fo + ".ckpt.json", log=None, time_budget_s=a.budget_s)
        if not res["complete"]:
            print(json.dumps(dict(partial=True, tag=tag, cpu=round(time.process_time() - c0, 1))), flush=True)
            return
        # compact output
        F = res["F"]["1"]
        out = dict(tag=tag, probe=p, b_std=b, N=a.N, family=a.family, R=a.R, dtype=a.dtype, times_us=res["times_us"],
                   names=res["names"], global_idx=res["global_idx"], F=F, H=res["H"], floor=res["floor"],
                   X=res["X"]["1"], G_ab=[g[1] for g in res["G"]], G_aa=[g[0] for g in res["G"]],
                   sumG=res["sumG"], cpu_s_sectors=res["cpu_secs"], cpu_s=time.process_time() - c0,
                   wall_s=time.time() - t0, vector_steps=res["vector_steps"],
                   err_typ=float(2.0 ** (-a.N / 2) * np.sqrt(2.0) / np.sqrt(a.R)))
        tmp = fo + ".tmp"
        json.dump(out, open(tmp, "w"), indent=1)
        os.replace(tmp, fo)
        print(json.dumps(dict(tag=tag, F=[round(x, 4) for x in F], H=[round(x, 4) for x in res["H"]],
                              floor=[round(x, 4) for x in res["floor"]], cpu=round(out["cpu_s"], 1))), flush=True)


if __name__ == "__main__":
    main()
