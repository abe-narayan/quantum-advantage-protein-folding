"""Exact echo/transfer signals and finite-difference Jacobians for the secular and the PHYSICAL double-quantum
Hamiltonian on the same N = 10 cluster, butterflies, parameters, FD step and sigma as C1 v2 / R1_amplify.

  secular : dt = 2 us, 0..320 us, record every 10 us (33 points)
  dq      : physical scaling (s = 1), dt = 2 us, 0..300 us, record every 10 us (31 points)
Validation (probe 1UBQ p19 only): the same engine at s = sqrt(3), 0..100 us, must reproduce the stored R1_amplify DQ
base signals (out/obs_1UBQ_p19_N10_o0_dq_fine.json) to ~1e-12.
Output: out/fi_<pdb>_p<probe>.json (checkpointed after each Hamiltonian).  Seconds to ~2 CPU-min per probe.
Usage: python run_fi.py --pdb 1UBQ --probe 19
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

import dq_lib as D


def jac(ham, g, steps, rec, bs, s_dq=1.0):
    base = D.exact_obs(ham, g["X0"], g["b0"], steps, rec, bs, s_dq)
    JS, JF = [], []
    for p in g["params"]:
        op = D.exact_obs(ham, D.L.displaced(g["X0"], p, +1, D.H_FD), g["b0"], steps, rec, bs, s_dq)
        om = D.exact_obs(ham, D.L.displaced(g["X0"], p, -1, D.H_FD), g["b0"], steps, rec, bs, s_dq)
        JS.append((op["S"] - om["S"]) / (2 * D.H_FD))
        JF.append((op["F1"] - om["F1"]) / (2 * D.H_FD))
    return base, np.array(JS), np.array(JF)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    a = ap.parse_args()
    t0 = time.process_time()
    path = os.path.join(D.OUT, f"fi_{a.pdb}_p{a.probe}.json")
    res = json.load(open(path)) if os.path.exists(path) else {}
    g = D.geometry(a.pdb, a.probe)
    bs = g["bs"]
    res.update(pdb=a.pdb, probe=a.probe, bs=bs, names_bs=[g["names"][g["idx"][b]] for b in bs],
               cluster=[g["names"][i] for i in g["idx"]],
               params=[dict(name=p["name"], r=p["r"], n_moved=len(p["move"])) for p in g["params"]],
               sigma=D.SIGMA, h=D.H_FD, dt=D.DT)
    if "T2" not in res:
        res["T2"] = D.t2_info(a.pdb, g)
    for ham, steps in (("sec", 160), ("dq", 150)):
        if ham in res:
            continue
        te = time.process_time()
        base, JS, JF = jac(ham, g, steps, 5, bs)
        res[ham] = dict(times_us=(base["times"] * 1e6).tolist(), S=base["S"], F1=base["F1"], J_S=JS, J_F1=JF,
                        MQC_tot=base.get("MQC_tot"), cpu_s=time.process_time() - te)
        D.atomic_json(res, path)
        print(json.dumps(dict(ham=ham, cpu=round(time.process_time() - te, 1))), flush=True)
    if a.pdb == "1UBQ" and a.probe == 19 and "validation" not in res:
        ref = json.load(open(os.path.join(D.AMP, "out", "obs_1UBQ_p19_N10_o0_dq_fine.json")))
        v = D.exact_obs("dq", g["X0"], g["b0"], 50, 5, bs, s_dq=math.sqrt(3.0))
        res["validation"] = dict(
            dq_matched_vs_R1_amplify_F1_maxabs=float(np.max(np.abs(v["F1"] - np.array(ref["families"]["F1"]["signal"])))),
            dq_matched_vs_R1_amplify_S_maxabs=float(np.max(np.abs(v["S"] - np.array(ref["families"]["S"]["signal"])))))
        D.atomic_json(res, path)
        print(json.dumps(res["validation"]), flush=True)
    res["cpu_total_s"] = res.get("cpu_total_s", 0.0) + time.process_time() - t0
    D.atomic_json(res, path)


if __name__ == "__main__":
    main()
