"""T1 analysis v2 (supersedes analyze_value.py): beta-samplers from the heat-bath production run
(results_value_gibbs.json), i.i.d. classical comparators from results_value.json. Pre-registered rule."""
import json, math, os
import numpy as np
from scipy.stats import wilcoxon, spearmanr
HERE = os.path.dirname(os.path.abspath(__file__))
g2 = json.load(open(os.path.join(HERE, "results_value_gibbs.json")))
v1 = json.load(open(os.path.join(HERE, "results_value.json")))
TAUS = [0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2]; GAMS = [1, 2, 3, 4]
F = ("prec", "cov", "allc", "mpp")
def mod(c, g):
    dp = c["prec"] - g["prec"]; sp = 1.96 * math.hypot(c["prec_se"], g["prec_se"])
    dc = c["cov"] - g["cov"]; sc = 1.96 * math.hypot(c["cov_se"], g["cov_se"])
    return dp >= -sp and dc >= -sc
def strictly_dominates(c, g):
    dp = c["prec"] - g["prec"]; sp = 1.96 * math.hypot(c["prec_se"], g["prec_se"])
    dc = c["cov"] - g["cov"]; sc = 1.96 * math.hypot(c["cov_se"], g["cov_se"])
    return (dp >= -sp and dc >= -sc) and (dp > sp or dc > sc)
def cal(cell, fam, grid, t):
    return min([f"{fam}{x:g}" for x in grid], key=lambda k_: abs(cell[k_]["mpp"] - t))
rows = []
for key, cell in v1.items():
    ch, L, k = key.split("|")
    g = g2[f"{key}|beta2"]
    pc = cal(cell, "pam", TAUS, g["mpp"]); ec = cal(cell, "edge", GAMS, g["mpp"])
    eff = {"uniform": g2[f"{key}|beta0"], "beta1": g2[f"{key}|beta1"], "greedy": cell["greedy"],
           "pam_cal": cell[pc], "edge_cal": cell[ec]}
    front = {**eff, **{f"pam{t:g}": cell[f"pam{t:g}"] for t in TAUS}, **{f"edge{x:g}": cell[f"edge{x:g}"] for x in GAMS}}
    betas = [b for b in (0, 0.5, 1, 2, 4, 8) if f"{key}|beta{b:g}" in g2]
    bp = [g2[f"{key}|beta{b:g}"]["prec"] for b in betas]; bc = [g2[f"{key}|beta{b:g}"]["cov"] for b in betas]
    rows.append({"cell": key, "L": int(L), "k": int(k),
                 "gbs": {x: g[x] for x in F}, "pam_cal": pc, "pam_cal_m": {x: cell[pc][x] for x in F},
                 "edge_cal": ec, "edge_cal_m": {x: cell[ec][x] for x in F},
                 "beta1_m": {x: g2[f"{key}|beta1"][x] for x in F}, "beta4_m": {x: g2[f"{key}|beta4"][x] for x in F},
                 "matched_by_efficient": [n for n, c in eff.items() if mod(c, g)],
                 "strictly_dominated_by_efficient": [n for n, c in eff.items() if strictly_dominates(c, g)],
                 "gbs_dominates": [n for n, c in eff.items() if strictly_dominates(g, c)],
                 "matched_by_front": [n for n, c in front.items() if mod(c, g)],
                 "rho_prec_beta": spearmanr(betas, bp).statistic, "rho_cov_beta": spearmanr(betas, bc).statistic})
def summ(x):
    x = np.array(x, float)
    try: p = float(wilcoxon(x).pvalue)
    except ValueError: p = float("nan")
    lo, hi = np.percentile([np.mean(np.random.default_rng(i).choice(x, len(x))) for i in range(2000)], [2.5, 97.5])
    return {"mean": float(x.mean()), "ci95_mean": [float(lo), float(hi)], "median": float(np.median(x)),
            "wilcoxon_p": p, "n_pos": int((x > 0).sum()), "n_neg": int((x < 0).sum())}
n = len(rows); npriv = sum(not r["matched_by_efficient"] for r in rows)
out = {"n_cells": n, "gbs_privileged_cells": npriv, "frac_privileged": npriv / n,
       "kill_rule": "survive only if privileged on >= 75% of cells", "kill_fired": npriv / n < 0.75,
       "gbs_privileged_vs_full_front": sum(not r["matched_by_front"] for r in rows),
       "cells_gbs_strictly_dominated_by_an_efficient_sampler": sum(bool(r["strictly_dominated_by_efficient"]) for r in rows),
       "matched_counts": {nm: sum(nm in r["matched_by_efficient"] for r in rows) for nm in ["uniform", "beta1", "greedy", "pam_cal", "edge_cal"]},
       "gbs_minus_pam_cal": {x: summ([r["gbs"][x] - r["pam_cal_m"][x] for r in rows]) for x in F},
       "gbs_minus_edge_cal": {x: summ([r["gbs"][x] - r["edge_cal_m"][x] for r in rows]) for x in F},
       "gbs_minus_beta1": {x: summ([r["gbs"][x] - r["beta1_m"][x] for r in rows]) for x in F},
       "median_rho_prec_vs_beta": float(np.nanmedian([r["rho_prec_beta"] for r in rows])),
       "median_rho_cov_vs_beta": float(np.nanmedian([r["rho_cov_beta"] for r in rows])),
       "by_L_k": {}, "rows": rows}
for L in (60, 100):
    for k in (3, 5):
        sub = [r for r in rows if r["L"] == L and r["k"] == k]
        out["by_L_k"][f"L{L}_k{k}"] = {"privileged": sum(not r["matched_by_efficient"] for r in sub), "n": len(sub),
            "d_prec_vs_pam": float(np.mean([r["gbs"]["prec"] - r["pam_cal_m"]["prec"] for r in sub])),
            "d_cov_vs_pam": float(np.mean([r["gbs"]["cov"] - r["pam_cal_m"]["cov"] for r in sub]))}
json.dump(out, open(os.path.join(HERE, "analysis_value_v2.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
