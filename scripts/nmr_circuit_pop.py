"""Program C minimal quantum proof-of-principle + hardware-noise attack (STEP 9 / section 46 of the sprint brief).

Runs the OTOC(1) forward model as a shot-based quantum circuit (src/qapf/nmr/circuit_pop.py) on the same cluster as a
C1 job, at several echo times and depolarising noise levels, with and without echo-normalisation mitigation
(F_mit = F / f, f = the echo without butterfly).  The noisy quantum simulator is then treated exactly like a classical
adversary: its failure time t_c(p) = first time |F_est - F_exact| exceeds sigma + 2 SE (shot error).  Compares with the
best classical OTOC failure time from the C1 job.
Usage: python scripts/nmr_circuit_pop.py --probe 19 --N 10
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.nmr import spins as SP  # noqa: E402
from qapf.nmr import circuit_pop as CP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--N", type=int, default=10)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--ks", default="10,20,40,60,80")
    ap.add_argument("--pvals", default="0,1e-3,3e-3,1e-2")
    ap.add_argument("--shots", type=int, default=2048)
    ap.add_argument("--nb", type=int, default=2, help="observe the nb farthest cluster protons")
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "nmr_pop"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    fj = os.path.join(a.out, f"{a.pdb}_p{a.probe}_N{a.N}_o{a.orient}.json")
    if os.path.exists(fj):
        print("exists"); return
    _cancel = os.path.join(ROOT, "research", "results", "RAW", "master", "cancel.txt")
    if os.path.exists(_cancel) and f"{a.pdb}_p{a.probe}_N{a.N}_o{a.orient}" in open(_cancel).read().split():
        print("cancelled"); return
    t0 = time.time()
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    idx = SP.cluster(xyz, a.probe, a.N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + a.orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    bs = sorted(int(k) for k in np.argsort(-dist)[:a.nb])
    dm = SP.couplings(X0, b0)
    ks = [int(v) for v in a.ks.split(",")]
    kmax = max(ks)
    tt, _, F = SP.sector_exact_correlators(dm, a.dt, kmax, 0, bs, record_every=1, otoc=True)
    res = dict(pdb=a.pdb, probe=a.probe, N=a.N, orient=a.orient, bs=bs, ks=ks, shots=a.shots, sigma=a.sigma,
               exact={str(b): [float(F[b][k]) for k in ks] for b in bs}, noise={})
    for p in [float(v) for v in a.pvals.split(",")]:
        rows = {}
        for b in bs:
            rb = []
            for k in ks:
                vF = CP.shots(dm, a.dt, k, 0, b, a.shots, seed=100 + k, p_step=p, otoc=True, return_values=True)
                if p > 0:
                    vf = CP.shots(dm, a.dt, k, 0, b, a.shots, seed=100 + k, p_step=p, otoc=True, butterfly=False,
                                  return_values=True)
                    f_ref = float(vf.mean())
                else:
                    f_ref = 1.0
                mF, sF = float(vF.mean()), float(vF.std(ddof=1) / np.sqrt(len(vF)))
                ex = float(F[b][k])
                mit = mF / f_ref if abs(f_ref) > 0.05 else float("nan")
                rb.append(dict(k=k, t_us=k * a.dt * 1e6, exact=ex, raw=mF, se=sF, ref=f_ref, mitigated=mit,
                               bias_raw=abs(mF - ex), bias_mit=abs(mit - ex) if np.isfinite(mit) else None))
            rows[str(b)] = rb
        # failure time: first k where any observable's bias exceeds sigma + 2 SE
        def tc(key):
            for i, k in enumerate(ks):
                for b in bs:
                    r = rows[str(b)][i]
                    bb = r[key]
                    if bb is None or bb > a.sigma + 2 * r["se"] / max(abs(r["ref"]), 0.05):
                        return k
            return None
        res["noise"][str(p)] = dict(rows=rows, tc_raw_k=tc("bias_raw"), tc_mit_k=tc("bias_mit"))
        print(json.dumps({"p_step": p, "tc_raw_k": res["noise"][str(p)]["tc_raw_k"],
                          "tc_mit_k": res["noise"][str(p)]["tc_mit_k"], "secs": round(time.time() - t0)}), flush=True)
        json.dump(res, open(fj + ".partial", "w"))
    res["secs"] = time.time() - t0
    json.dump(res, open(fj + ".tmp", "w"))
    os.replace(fj + ".tmp", fj)
    if os.path.exists(fj + ".partial"):
        os.remove(fj + ".partial")


if __name__ == "__main__":
    main()
