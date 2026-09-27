"""C2 (PREREG_G1_C1_Q4.md): cost scaling of the best classical adversary (sparse Pauli dynamics) for protein 1H
dipolar dynamics.  One job = (pdb, probe, N, orient, gamma).  Same cluster / observables / Trotter circuit as
scripts/nmr_gate.py.  Runs a descending eps ladder (coefficient-threshold truncation, no weight cap) and records, per
eps, the transfer signal S_ab(t), string counts, peak strings, cap/budget flags and wall-clock.  Reference: sector-exact
(N <= 14 at gamma = 0, N <= 12 at gamma > 0), else none (the analysis uses the smallest converged eps).
Output: research/results/RAW/nmr_sparse/<tag>.json
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

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--gamma", type=float, default=0.0)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--nt", type=int, default=16)
    ap.add_argument("--K", type=int, default=3)
    ap.add_argument("--eps", default="1e-2,3e-3,1e-3,3e-4,1e-4,3e-5")
    ap.add_argument("--max-strings", type=int, default=4_000_000)
    ap.add_argument("--budget", type=float, default=3600.0, help="seconds per eps run")
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "nmr_sparse"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.pdb}_p{a.probe}_N{a.N}_o{a.orient}_g{int(a.gamma)}"
    fj = os.path.join(a.out, tag + ".json")
    if os.path.exists(fj):
        print("exists"); return
    t0 = time.time()
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    idx = SP.cluster(xyz, a.probe, a.N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + a.orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:a.K]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    rec = max(1, a.steps // a.nt)
    dm = SP.couplings(X0, b0)
    res = dict(pdb=a.pdb, probe=a.probe, probe_name=names[a.probe], N=a.N, orient=a.orient, gamma=a.gamma, dt=a.dt,
               steps=a.steps, rec=rec, sigma=a.sigma, bs=bs, dist_bs=[float(dist[b]) for b in bs],
               max_strings=a.max_strings, budget=a.budget, runs=[], exact=None)
    exact_ok = (a.N <= 14 and a.gamma == 0) or (a.N <= 12)
    if exact_ok:
        te = time.time()
        do_f = a.gamma == 0
        tt, S0, F0 = SP.sector_exact_correlators(dm, a.dt, a.steps, 0, bs, gamma=a.gamma, record_every=rec, otoc=do_f)
        res["exact"] = dict(times=tt.tolist(), S={str(b): S0[b].tolist() for b in bs},
                            F=({str(b): F0[b].tolist() for b in bs} if F0 else None), secs=time.time() - te)
        print(json.dumps({"exact_secs": round(time.time() - te, 1)}), flush=True)
    for e in [float(v) for v in a.eps.split(",") if v]:
        st = {}
        tt_, Sw, Fw, nstr, norm2 = SP.pauli_correlators(dm, a.dt, a.steps, 0, bs, wmax=None, eps=e, gamma=a.gamma,
                                                       record_every=rec, max_strings=a.max_strings,
                                                       time_budget_s=a.budget, stats=st)
        run = dict(eps=e, times=np.asarray(tt_).tolist(), S={str(b): np.asarray(Sw[b]).tolist() for b in bs},
                   F={str(b): np.asarray(Fw[b]).tolist() for b in bs},
                   n_strings=np.asarray(nstr).tolist(), kept_norm2=np.asarray(norm2).tolist(), **st)
        if res["exact"]:
            n = len(tt_)
            bias = np.max(np.stack([np.abs(np.asarray(Sw[b]) - np.asarray(res["exact"]["S"][str(b)])[:n]) for b in bs]), 0)
            run["max_bias"] = bias.tolist()
        res["runs"].append(run)
        print(json.dumps({"eps": e, "peak": st.get("peak_strings"), "capped": st.get("capped"),
                          "steps_done": st.get("steps_done"), "secs": round(st.get("secs", 0), 1),
                          "maxbias": (round(max(run["max_bias"]), 4) if "max_bias" in run else None)}), flush=True)
        tmp = fj + ".partial"
        json.dump(res, open(tmp, "w"))
        if st.get("capped") or st.get("steps_done", a.steps) < a.steps:
            break
    res["secs"] = time.time() - t0
    json.dump(res, open(fj + ".tmp", "w"))
    os.replace(fj + ".tmp", fj)
    if os.path.exists(fj + ".partial"):
        os.remove(fj + ".partial")
    print(json.dumps({"tag": tag, "secs": round(res["secs"]), "n_runs": len(res["runs"])}))


if __name__ == "__main__":
    main()
