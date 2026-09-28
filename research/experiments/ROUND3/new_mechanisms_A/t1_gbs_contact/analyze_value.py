"""Analyse T1 value test against the pre-registered kill rule (prereg.json, T1)."""
import json
import math
import os
import numpy as np
from scipy.stats import wilcoxon, spearmanr

HERE = os.path.dirname(os.path.abspath(__file__))
res = json.load(open(os.path.join(HERE, "results_value.json")))
TAUS = [0.1, 0.2, 0.3, 0.5, 0.75, 1, 1.5, 2]
GAMS = [1, 2, 3, 4]
BETAS = [0, 0.5, 1, 1.5, 2, 3, 4, 8]


def matches_or_dominates(c, g):
    """comparator c Pareto-matches-or-dominates GBS g within 95% CI (unpaired)."""
    dp = c["prec"] - g["prec"]
    sp = 1.96 * math.hypot(c["prec_se"], g["prec_se"])
    dc = c["cov"] - g["cov"]
    sc = 1.96 * math.hypot(c["cov_se"], g["cov_se"])
    return (dp >= -sp) and (dc >= -sc)


def calibrated(cell, fam, grid, target):
    keys = [f"{fam}{x:g}" for x in grid]
    return min(keys, key=lambda k_: abs(cell[k_]["mpp"] - target))


rows = []
for key, cell in res.items():
    ch, L, k = key.split("|")
    g = cell["beta2"]
    pam_c = calibrated(cell, "pam", TAUS, g["mpp"])
    edge_c = calibrated(cell, "edge", GAMS, g["mpp"])
    eff = {"uniform": cell["beta0"], "beta1": cell["beta1"], "greedy": cell["greedy"],
           "pam_cal": cell[pam_c], "edge_cal": cell[edge_c]}
    fam_all = {**eff, **{f"pam{t:g}": cell[f"pam{t:g}"] for t in TAUS},
               **{f"edge{x:g}": cell[f"edge{x:g}"] for x in GAMS}}
    who = [n for n, c in eff.items() if matches_or_dominates(c, g)]
    who_front = [n for n, c in fam_all.items() if matches_or_dominates(c, g)]
    bprec = [cell[f"beta{b:g}"]["prec"] for b in BETAS]
    bcov = [cell[f"beta{b:g}"]["cov"] for b in BETAS]
    rows.append({
        "cell": key, "L": int(L), "k": int(k), "n_native": cell["n_native"],
        "gbs": {x: g[x] for x in ("prec", "cov", "allc", "mpp")},
        "pam_cal": pam_c, "pam_cal_m": {x: cell[pam_c][x] for x in ("prec", "cov", "allc", "mpp")},
        "edge_cal": edge_c, "edge_cal_m": {x: cell[edge_c][x] for x in ("prec", "cov", "allc", "mpp")},
        "beta1_m": {x: cell["beta1"][x] for x in ("prec", "cov", "allc", "mpp")},
        "greedy_prec": cell["greedy"]["prec"],
        "matched_by_efficient": who, "matched_by_classical_front": who_front,
        "gbs_privileged_prereg": len(who) == 0, "gbs_privileged_vs_front": len(who_front) == 0,
        "beta_prec_spearman": spearmanr(BETAS, bprec).statistic,
        "beta_cov_spearman": spearmanr(BETAS, bcov).statistic,
    })

n = len(rows)
npriv = sum(r["gbs_privileged_prereg"] for r in rows)
npriv_f = sum(r["gbs_privileged_vs_front"] for r in rows)
# pooled paired tests: GBS vs calibrated perturb-and-MAP (same native-free concentration)
d_prec = [r["gbs"]["prec"] - r["pam_cal_m"]["prec"] for r in rows]
d_cov = [r["gbs"]["cov"] - r["pam_cal_m"]["cov"] for r in rows]
d_allc = [r["gbs"]["allc"] - r["pam_cal_m"]["allc"] for r in rows]
d_mpp = [r["gbs"]["mpp"] - r["pam_cal_m"]["mpp"] for r in rows]
e_prec = [r["gbs"]["prec"] - r["edge_cal_m"]["prec"] for r in rows]
e_cov = [r["gbs"]["cov"] - r["edge_cal_m"]["cov"] for r in rows]


def summ(x):
    x = np.array(x, float)
    try:
        p = wilcoxon(x).pvalue
    except ValueError:
        p = float("nan")
    return {"mean": float(x.mean()), "median": float(np.median(x)), "wilcoxon_p": float(p),
            "n_pos": int((x > 0).sum()), "n_neg": int((x < 0).sum())}


out = {
    "n_cells": n,
    "gbs_privileged_cells_prereg_comparators": npriv,
    "frac_privileged_prereg": npriv / n,
    "gbs_privileged_cells_vs_full_classical_front": npriv_f,
    "prereg_kill_threshold": "privileged on >= 75% of cells needed to survive",
    "kill_fired": npriv / n < 0.75,
    "gbs_minus_pam_calibrated": {"prec": summ(d_prec), "cov": summ(d_cov), "allc": summ(d_allc), "mpp": summ(d_mpp)},
    "gbs_minus_edge_calibrated": {"prec": summ(e_prec), "cov": summ(e_cov)},
    "beta_monotonicity": {
        "median_spearman_prec_vs_beta": float(np.nanmedian([r["beta_prec_spearman"] for r in rows])),
        "median_spearman_cov_vs_beta": float(np.nanmedian([r["beta_cov_spearman"] for r in rows])),
    },
    "matched_by_counts": {nm: sum(nm in r["matched_by_efficient"] for r in rows)
                          for nm in ["uniform", "beta1", "greedy", "pam_cal", "edge_cal"]},
    "rows": rows,
}
json.dump(out, open(os.path.join(HERE, "analysis_value.json"), "w"), indent=1)
print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
for r in rows:
    print(r["cell"], "GBS", r["gbs"], "| pam", r["pam_cal"], r["pam_cal_m"], "| matched:", r["matched_by_efficient"])
