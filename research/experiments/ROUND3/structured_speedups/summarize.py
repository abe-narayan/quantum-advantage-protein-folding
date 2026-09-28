"""Aggregate S1-S6 JSON outputs into summary.json (read-only over the per-check files)."""
import json, os
import numpy as np
from common import HERE, atomic_json

def J(n): return json.load(open(os.path.join(HERE, n), encoding="utf-8"))
out = {}
# ---- S4 level-1
s4 = J("s4_planted_level1.json")["crops"]
t = {}
for L in (30, 60, 100, 150):
    rs = [r for r in s4.values() if r["L"] == L]
    dE = np.array([r["dE_level1_minus_census"] for r in rs])
    t[L] = dict(n=len(rs), reach_best_known=int(sum(r["level1_reaches_best_known"] for r in rs)),
                beats_census=int(sum(r["level1_beats_census"] for r in rs)),
                dE_median=float(np.median(dE)), dE_min=float(dE.min()), dE_max=float(dE.max()),
                grad_evals_level1_median=float(np.median([r["grad_evals_level1"] for r in rs])),
                grad_evals_census_median=float(np.median([r["census_grad_evals"] for r in rs])),
                lam3_over_lam4_median=float(np.median([r["lam3_over_lam4"] for r in rs])),
                ORACLE_rmsd_level1_median=float(np.median([r["ORACLE"]["rmsd_level1_best_by_E"] for r in rs])),
                ORACLE_rmsd_census_best_median=float(np.median([r["ORACLE"]["census_best_mode_rmsd"] for r in rs])))
out["S4_level1_vs_census"] = t
# ---- S3 DQI graph code
s3 = J("s3_dqi_graph_code.json")["crops"]
t = {}
for L in (30, 60, 100, 150):
    for var in ("full", "conf", "contact", "contact0", "ER_null"):
        vs = [r["variants"][var] for r in s3.values() if r["L"] == L and not r["variants"][var].get("empty")]
        if not vs: continue
        cyc = [v for v in vs if np.isfinite(v["girth"])]
        t[f"L{L}_{var}"] = dict(n=len(vs), n_acyclic=len(vs) - len(cyc), m_median=float(np.median([v["m"] for v in vs])),
            girth_values=sorted(set(float(v["girth"]) for v in vs)),
            triangles_median=float(np.median([v["triangles"] for v in vs])),
            l_thm41_max=int(max(v["l_thm41"] for v in cyc)) if cyc else None,
            l90_median=float(np.median([v["l90"] for v in cyc])) if cyc else None,
            l50_median=float(np.median([v["l50"] for v in cyc])) if cyc else None,
            l50_over_m_median=float(np.median([v["l50_over_m"] for v in cyc])) if cyc else None,
            rho_bar_median=float(np.median([v["rho_bar"] for v in vs])),
            dqi_thm41_median=float(np.median([v["dqi_frac_thm41"] for v in cyc])) if cyc else None,
            dqi_l50_median=float(np.median([v["dqi_frac_l50"] for v in cyc])) if cyc else None,
            dqi_l50_max=float(np.max([v["dqi_frac_l50"] for v in cyc])) if cyc else None,
            classical_level1_median=float(np.median([v["classical_frac_level1_relaxed"] for v in cyc])) if cyc else None,
            classical_level1_min=float(np.min([v["classical_frac_level1_relaxed"] for v in cyc])) if cyc else None,
            classical_prior_median=float(np.median([v["classical_frac_prior_mean"] for v in cyc])) if cyc else None,
            l_needed_over_l50_median=float(np.median([v["l_needed_over_l50"] for v in cyc if "l_needed_over_l50" in v])) if cyc else None,
            ORACLE_native_median=float(np.median([v["ORACLE_frac_native"] for v in vs])),
            n_cases_dqi_l50_ge_classical=int(sum(v["dqi_frac_l50"] >= v["classical_frac_level1_relaxed"] for v in cyc)))
out["S3_dqi_graph_code"] = t
# ---- S1 torsion lines
s1 = J("s1_torsion_lines.json")
t = {}
for s in (1, 2, 3, 4, 5):
    ps = [r for r in s1["pairs"] if r.get("s") == s and not r.get("skipped")]
    if ps:
        t[f"pair_s{s}"] = dict(n=len(ps), p=ps[0]["p"], best_line_median=float(np.median([r["frac_best_line"] for r in ps])),
            best_line_range=[float(min(r["frac_best_line"] for r in ps)), float(max(r["frac_best_line"] for r in ps))],
            axis_median=float(np.median([r["frac_axis_lines"] for r in ps])),
            n_lines_90_median=float(np.median([r["n_lines_90"] for r in ps])),
            n_lines_99_median=float(np.median([r["n_lines_99"] for r in ps])), n_lines_total=ps[0]["n_lines_total"])
    ws = [r for r in s1["windows"] if r["s"] == s]
    if ws:
        c = [w["clipped99"] for w in ws]; rw = [w["raw"] for w in ws]
        t[f"window_s{s}"] = dict(n=len(ws), p=c[0]["p"], best_line_median=float(np.median([x["frac_best_line"] for x in c])),
            axis_median=float(np.median([x["frac_axis_lines"] for x in c])),
            n_lines_90_median=float(np.median([x["n_lines_90"] for x in c])),
            n_lines_99_range=[int(min(x["n_lines_99"] for x in c)), int(max(x["n_lines_99"] for x in c))],
            frac_lines_needed_99_median=float(np.median([x["frac_lines_needed_99"] for x in c])),
            raw_n_lines_99_range=[int(min(x["n_lines_99"] for x in rw)), int(max(x["n_lines_99"] for x in rw))],
            n_lines_total=c[0]["n_lines_total"])
t["pairs_skipped_span_gt5"] = int(sum(1 for r in s1["pairs"] if r.get("skipped")))
out["S1_torsion_lines"] = t
# ---- S2 / S2b
s2 = J("s2_anova_arity.json")["runs"]
t = {}
for L in (30, 60, 100):
    for m in ("local10", "local30", "prior"):
        rs = [r for r in s2.values() if r["L"] == L and r["measure"] == m]
        t[f"L{L}_{m}"] = dict(mean_dim=[round(r["mean_dim"], 2) for r in rs],
                              mean_dim_ci_lo_min=float(min(r["mean_dim_ci"][0] for r in rs)),
                              groups_T_gt_1pct=[f'{r["n_groups_T_gt_1pct"]}/{r["d"]}' for r in rs])
out["S2_mean_dimension"] = t
s2b = J("s2b_additive_fit_v2.json")["runs"]
t = {}
for L in (30, 60):
    for m in ("local10", "local30", "prior"):
        rs = [r for r in s2b.values() if r["L"] == L and r["measure"] == m]
        t[f"L{L}_{m}"] = dict(R2_additive=[round(r["R2_additive_raw"], 3) for r in rs],
                              R2_add_plus_nn=[round(r["R2_add_plus_nn_raw"], 3) for r in rs])
out["S2b_additive_R2"] = t
out["S5_graph"] = J("s5_graph_krylov.json")["runs"]
s6 = J("s6_exponents.json")
out["S6_exponents"] = dict(alpha_c=s6["classical"]["fit_ln_cost"]["alpha_c"], summary=s6["summary_median_min_max"],
                           ratio=s6["ratio_quantum_exp_to_alpha_c"], jump=s6["jump_to_end"],
                           classical_cost=s6["classical"]["cost_per_hit_grad_evals"])
atomic_json(os.path.join(HERE, "summary.json"), out)
print(json.dumps(out, indent=1, default=float)[:12000])
