"""Classical verifier: replicate the lane's flat-X test on the two replication probes (1UBQ p487, 1PGA p390).
F_N (N = 14, 16, 18) from the finished reference typicality cones (ADVERSARIAL/.../typicality_cone, read-only);
exact H_N and floor_N from ROUND3 decomp_echo.run in 'honly' mode (two inverse passes), probe family, same circuit.
Hybrid premise (X_N flat) <=> dF = d(H + floor).  Checkpoint per sector (atomic); resumable.  Output: flatx_replication.json"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..", "ROUND3", "r1sim_exact_reach", "verify_classical")))
import decomp_echo as DE  # noqa: E402

CONE = os.path.abspath(os.path.join(HERE, "..", "..", "..", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone"))
O = os.path.join(HERE, "out")
T = [40, 80, 120]
res = {}
for pdb, p in (("1UBQ", 487), ("1PGA", 390)):
    lad = {}
    for N in (14, 16, 18):
        R = 2 if N < 18 else 1
        fo = os.path.join(O, f"honly_{pdb}_p{p}_N{N}_R{R}.json")
        if os.path.exists(fo):
            h = json.load(open(fo))
        else:
            r = DE.run(pdb, p, N, "probe", None, "honly", [20, 40, 60], R, np.dtype("complex128"), 2718, fo + ".ckpt.json",
                       log=None, time_budget_s=1200)
            assert r["complete"]
            h = dict(H=r["H"], floor=r["floor"], Gaa=[g[0] for g in r["G"]], cpu_s=r["cpu_secs"], names=r["names"])
            json.dump(h, open(fo + ".tmp", "w")); os.replace(fo + ".tmp", fo)
        c = json.load(open(os.path.join(CONE, f"{pdb}_p{p}_N{N}.json")))
        tt = [round(x) for x in c["times_us"]]
        for b in c["F"]:
            for i, t in enumerate(T):
                lad.setdefault((b, t), []).append(dict(N=N, F=c["F"][b][tt.index(t)], H=h["H"][i], floor=h["floor"][i]))
        print(pdb, p, N, "H", [round(x, 4) for x in h["H"]], "floor", [round(x, 4) for x in h["floor"]],
              "cpu", round(h["cpu_s"], 1), flush=True)
    for t in T:
        xs, ys, per = [], [], []
        for (b, tq), L in lad.items():
            if tq != t:
                continue
            x = np.array([r["H"] + r["floor"] for r in L]); y = np.array([r["F"] for r in L])
            xs.append(x - x.mean()); ys.append(y - y.mean())
            per.append(dict(site=b, F=[round(v, 4) for v in y], X=[round(r["F"] - r["H"] - r["floor"], 4) for r in L],
                            dF=round(float(y[-1] - y[0]), 4), dHfloor=round(float(x[-1] - x[0]), 4)))
        X_ = np.concatenate(xs); Y_ = np.concatenate(ys)
        s = float((X_ * Y_).sum() / (X_ ** 2).sum())
        rr = np.array([d["dF"] - d["dHfloor"] for d in per])
        res[f"{pdb}_p{p}_t{t}"] = dict(pooled_slope=round(s, 3), mean_dF_minus_hybrid_pred=round(float(rr.mean()), 4),
                                       se=round(float(rr.std(ddof=1) / math.sqrt(len(rr))), 4),
                                       n_dX_positive=int(sum(d["X"][-1] > d["X"][0] for d in per)), n=len(per), per_series=per)
json.dump(res, open(os.path.join(HERE, "flatx_replication.json"), "w"), indent=1)
for k, v in res.items():
    print(k, {kk: vv for kk, vv in v.items() if kk != "per_series"}, [(d["site"], d["F"], d["dF"], d["dHfloor"]) for d in v["per_series"]])
