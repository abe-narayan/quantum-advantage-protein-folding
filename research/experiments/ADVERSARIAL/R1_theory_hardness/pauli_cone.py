"""R1 theory_hardness, step D: cluster-size convergence of the echo F_ab(t) at EARLY times on larger nested clusters,
using coefficient-truncated (sparse) Pauli dynamics with a discarded-norm certificate.

Same circuit/cluster/b0 as the instrument (qapf.nmr.spins.pair_list order, Heisenberg order reversed(pairs)).
For N in the ladder, evolve Z_a to t_max (default 60 us) with threshold eps; record, for the FIRST 12 sites j (common
to all nested clusters), F_aj(t) = sum_P c_P^2 s_P(j) and the lost norm L(t) = 1 - sum_K c_P^2.
Certificate (DERIVED, heuristic): the truncated F differs from the exact F of the SAME N-spin cluster by the signed
lost weight plus the effect of truncation on later dynamics; empirically |dF| <~ L (checked here at N = 12 against the
exact sector result in front/). A cluster-size change |F^(N') - F^(N)| > sigma + L(N) + L(N') is therefore a certified
(heuristic) non-convergence.
Usage: python pauli_cone.py --probe 19 --Ns 12,16,20,24 --eps 3e-4 --tmax-us 60 --budget 240
Output: pauli_cone_<pdb>_p<probe>.json
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
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def run(dm, dt, n_steps, rec, eps, budget, n_obs, max_strings):
    N = len(dm)
    pairs = SP.pair_list(dm, dt)
    op = SP.PauliOp.single_z(N, 0)
    out = dict(steps=[], F=[], lost=[], n_strings=[], size=[])
    t0 = time.time()
    done = True
    for k in range(n_steps + 1):
        if k % rec == 0:
            c2 = op.c ** 2
            out["steps"].append(k); out["lost"].append(float(1 - c2.sum())); out["n_strings"].append(int(len(c2)))
            Fj = []
            for b in range(n_obs):
                sb = np.where(((op.x >> np.uint64(b)) & np.uint64(1)).astype(bool), -1.0, 1.0)
                Fj.append(float((c2 * sb).sum()))
            out["F"].append(Fj)
            w = SP._popcount(op.x | op.z).astype(float)
            out["size"].append(float((w * c2).sum() / max(c2.sum(), 1e-300)))
        if k == n_steps:
            break
        if time.time() - t0 > budget:
            done = False
            break
        for (i, j, ddt) in reversed(pairs):
            op = SP.conj_pair(op, i, j, ddt, None, eps)
            if len(op.c) > max_strings:
                done = False
                break
        if not done:
            break
    out["complete"] = done
    out["secs"] = time.time() - t0
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--Ns", default="12,16,20,24")
    ap.add_argument("--eps", type=float, default=3e-4)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--tmax-us", type=float, default=60.0)
    ap.add_argument("--rec", type=int, default=5)
    ap.add_argument("--budget", type=float, default=240.0)
    ap.add_argument("--max-strings", type=int, default=2_000_000)
    ap.add_argument("--hn-only", type=int, default=0, help="1 = amide-only (perdeuterated) network, as nmr_gate --hn-only")
    a = ap.parse_args()
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    probe = a.probe
    if a.hn_only:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        xyz = xyz[keep]; probe = keep.index(a.probe)
    b0 = random_b0(1000)
    n_steps = int(round(a.tmax_us * 1e-6 / a.dt))
    res = dict(pdb=a.pdb, probe=a.probe, eps=a.eps, dt=a.dt, b0=b0.tolist(), runs={})
    for N in [int(x) for x in a.Ns.split(",")]:
        idx = SP.cluster(xyz, probe, N)
        dm = SP.couplings(xyz[idx], b0)
        r = run(dm, a.dt, n_steps, a.rec, a.eps, a.budget, 12, a.max_strings)
        r["times_us"] = [s * a.dt * 1e6 for s in r["steps"]]
        r["cluster"] = [int(i) for i in idx]
        r["r_max_A"] = float(np.linalg.norm(xyz[idx] - xyz[probe], axis=1).max())
        res["runs"][str(N)] = r
        print(json.dumps(dict(N=N, complete=r["complete"], secs=round(r["secs"], 1), r_max=round(r["r_max_A"], 2),
                              lost=[round(x, 4) for x in r["lost"]], nstr=r["n_strings"],
                              size=[round(x, 2) for x in r["size"]])), flush=True)
        json.dump(res, open(os.path.join(HERE, f"pauli_cone_{a.pdb}{'HN' if a.hn_only else ''}_p{a.probe}.json"), "w"))
    # bias check at N = 12 against the exact sector result
    fe = os.path.join(HERE, "front", f"{a.pdb}{'HN' if a.hn_only else ''}_p{a.probe}_N12_o0.json")
    if os.path.exists(fe) and "12" in res["runs"]:
        ex = json.load(open(fe)); te = np.array(ex["times_us"]); FZ = np.array(ex["FZ"])
        r = res["runs"]["12"]
        dev = []
        for ti, t in enumerate(r["times_us"]):
            i = int(np.argmin(abs(te - t)))
            if abs(te[i] - t) < 0.5:
                dev.append(dict(t=t, max_abs_dF=float(np.max(np.abs(np.array(r["F"][ti]) - FZ[i, :12]))), lost=r["lost"][ti]))
        res["bias_check_N12"] = dev
        print("bias check N=12:", [(round(d["t"]), round(d["max_abs_dF"], 4), round(d["lost"], 4)) for d in dev])
    json.dump(res, open(os.path.join(HERE, f"pauli_cone_{a.pdb}{'HN' if a.hn_only else ''}_p{a.probe}.json"), "w"))


if __name__ == "__main__":
    main()
