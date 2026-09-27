"""Collect t_c (first time max_b |F_est - F_exact| > 0.01) for every estimator/cluster into out/summary.json."""
import glob
import json
import os

import common as C

S = {}
cce = json.load(open(os.path.join(C.OUT, "cce_N10.json")))
for cl, e in cce["clusters"].items():
    for k, v in e["orders"].items():
        S.setdefault(f"E1_cce_{k}", {})[cl] = dict(t_c_us=v["t_c_us"], max_sub=v["max_sub_size"],
                                                   n_sub_sims=v.get("n_sub_sims"))
op = json.load(open(os.path.join(C.OUT, "opspread_N10.json")))
for cl, e in op["clusters"].items():
    for k, v in e["runs"].items():
        S.setdefault(f"E2_{k}", {})[cl] = dict(t_c_us=v["t_c_us"], max_err=max(v["max_err"]), lam=v.get("lam"),
                                               nc=v.get("nc"))
for f in sorted(glob.glob(os.path.join(C.OUT, "mpo_*_N10_*.json"))):
    v = json.load(open(f))
    S.setdefault(f"E4_mpo_chi{v['chi']}", {})[f"{v['pdb']}_p{v['probe']}"] = dict(
        t_c_us=v["t_c_us"], err_60us=v["max_err"][3], err_80us=v["max_err"][4], cpu=v["cpu"], disc=v["disc"])
for f in sorted(glob.glob(os.path.join(C.OUT, "stoch_*.json"))):
    v = json.load(open(f))
    S.setdefault(f"E3_stochpauli_M{v['M']}_R{v['R']}", {})[f"{v['pdb']}_p{v['probe']}"] = dict(
        t_c_us_unbiased=v["unbiased"]["t_c_us"], t_c_us_ratio=v["ratio"]["t_c_us"],
        err_40us_unbiased=v["unbiased"]["max_err"][2], err_40us_ratio=v["ratio"]["max_err"][2], cpu=v["cpu"])
inf = json.load(open(os.path.join(C.OUT, "influence_N10.json")))
L = {}
for cl, e in inf["clusters"].items():
    t = [v["t_infl_us"] for v in e["leave_one_out"].values()]
    L[cl] = dict(leave_one_out_min_us=min(t), leave_one_out_max_us=max(t),
                 t_embed_N11_us=e["add"]["1"]["t_embed_us"], t_embed_N12_us=e["add"]["2"]["t_embed_us"],
                 max_dev_N11_80to320=max(e["add"]["1"]["max_err"][4:]), max_dev_N12_80to320=max(e["add"]["2"]["max_err"][4:]))
out = dict(threshold=C.THR, grid_us="0..320 step 20", kill_rule="t_c >= 160 us on all 3 clusters at poly cost",
           panel_best_otoc_us=80.0, estimators=S, light_cone=L)
best = {k: min((x.get("t_c_us") if "t_c_us" in x else x.get("t_c_us_ratio")) or 1e9 for x in v.values())
        for k, v in S.items() if len(v) == 3}
out["worst_cluster_t_c_us"] = best
C.dump(out, "summary.json")
for k, v in sorted(best.items(), key=lambda kv: -kv[1]):
    print(f"{k:32s} min over clusters t_c = {v}")
print(json.dumps(L, indent=1))
