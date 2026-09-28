"""ROUND4 completeness critic, check CR4-A: arithmetic audit of the synthesis's headline numbers, from JSON already on
disk (no dynamics; < 1 CPU-s).  Writes critic/critic_arith.json.

A1  FT-QPU cost of the 40 us echo at the program's own 'generous' logical T/Toffoli time (10 ns, as used by K-101,
    K-107 and K-117), not only at the 1 us T layer used in spindmft/verify_resource/breakeven_40us.json.
A2  Visible share (reversal envelope x classical spread) at 40/80/120 us using the DIRECTOR's cross-family spreads
    (director/cross_family.json) instead of the spinDMFT relevance verifier's smaller pre-merge spreads.
A3  Where 40 us sits relative to the PE / LE reversal horizons for the T2 values the program uses.
A4  Pairwise thermodynamic-vs-exact agreement at 40 us (the '<= 0.0096' in SYNTHESIS §0.2 / §5) and the dynamic range
    1 - F of the 8 series at 40 us; exact-family agreement count at 80 us (SYNTHESIS §0.5 / §2 item 2 wording).
A5  K-109 under the local (site-resolved) DQ envelope with secular transfer on the classical side, t_cl = 0 and 40
    (redteam_kills/profiled_extensions.json): the t_cl-independent analogue of K-105's arm.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.dirname(HERE)
SIG = 0.01
out = {}

# ---------------------------------------------------------------------------------------------- A1
be = json.load(open(os.path.join(R4, "spindmft", "verify_resource", "breakeven_40us.json")))
q40 = be["quantum_one_time_point"]["40"]
cl = be["classical_pipeline_40us"]
cl_total_all8 = cl["total_all_8_series_s_(b-aware N20 x8 + spinDMFT; 40/80/120 us in one pass)"]
cl_exact_only = cl["exact_only_b-aware_N18_x8_s"]
rows = []
for r in q40:
    lab = f"N={r['N']}" + (f" ({r['note']})" if "note" in r else "")
    tdepth = r["T_depth"]
    per_probe = {k: tdepth * v for k, v in (("10ns", 1e-8), ("100ns", 1e-7), ("1us", 1e-6))}
    rows.append(dict(circuit=lab, T_depth=tdepth, wall_s_per_circuit=per_probe))
# quantum for all 8 series: 2 probes x (one 629-qubit circuit reads 4 sites) ; cluster circuits: one per series
A1 = dict(rows=rows, classical_all8_single_core_s=dict(full_pipeline=cl_total_all8, exact_only_N18=cl_exact_only))
cmp = {}
for r in q40:
    if r["N"] == 629 and r.get("trotter_steps_per_shot") == 40.0:
        key = "629_dense" if "dense" in r["note"] else "629_cut30"
        n_circ = 2
    elif r["N"] == 20:
        key, n_circ = "cluster20", 8
    else:
        continue
    for tt, v in (("10ns", 1e-8), ("1us", 1e-6)):
        qs = n_circ * r["T_depth"] * v
        cmp[f"{key}@{tt}"] = dict(quantum_s_all8=qs, ratio_quantum_over_classical_pipeline=qs / cl_total_all8,
                                  ratio_quantum_over_exact_only=qs / cl_exact_only)
A1["all8_comparison"] = cmp
out["A1_qpu_cost_40us"] = A1

# ---------------------------------------------------------------------------------------------- A2/A3
cf = json.load(open(os.path.join(R4, "director", "cross_family.json")))


def env_gauss(x, c):
    return math.exp(-math.log(2) * (x / c) ** 2)


def env_logistic(x, c, lam_frac=0.25):
    l = lam_frac * c
    return (1 + math.exp(-c / l)) / (1 + math.exp((x - c) / l))


T2s = {"1UBQ_rotoravg_physical": 9.7707, "1UBQ_network_static": 8.0427}
A3 = {}
for nm, T2 in T2s.items():
    A3[nm] = dict(T3_PE_halfmax_us=4 * T2, T3_LE_midpoint_us=T2 / 0.15,
                  A_PE={t: env_gauss(t / T2, 4.0) for t in (40, 50, 60, 80, 120)},
                  A_LE={t: env_logistic(t / T2, 1 / 0.15, 0.25) for t in (40, 50, 60, 80, 120)})
out["A3_40us_vs_horizons"] = A3
A2 = {}
for nm, T2 in T2s.items():
    per_t = {}
    for t in (40, 80, 120):
        spreads_all = [c["spread_all"] for k, c in cf["cells"].items() if k.endswith(f"_t{t}")]
        spreads_ex = [c["spread_exact_baware"] for k, c in cf["cells"].items() if k.endswith(f"_t{t}")]
        aL, aP = env_logistic(t / T2, 1 / 0.15, 0.25), env_gauss(t / T2, 4.0)
        per_t[t] = dict(max_spread_all=max(spreads_all), max_spread_exact_baware=max(spreads_ex),
                        visible_LE_sigma_all=aL * max(spreads_all) / SIG, visible_PE_sigma_all=aP * max(spreads_all) / SIG,
                        visible_LE_sigma_exact=aL * max(spreads_ex) / SIG, visible_PE_sigma_exact=aP * max(spreads_ex) / SIG,
                        n_series_visible_LE_ge_1sigma=sum(aL * s / SIG >= 1 for s in spreads_all))
    A2[nm] = per_t
A2["relevance_verifier_quoted"] = dict(raw_max_spread_80=0.039, raw_max_spread_120=0.106,
                                       visible_80_LE_PE_sigma=(1.18, 0.22), visible_120_LE_PE_sigma=(0.40, 0.02))
out["A2_visible_share"] = A2

# ---------------------------------------------------------------------------------------------- A4
th_keys, ex_keys = ("E1", "E2", "DMFT"), ("SA2", "SA4", "PB20", "FEPB", "PP")
A4 = dict(t40={}, t80_exact_pairs={})
worst = (0, None)
for k, c in cf["cells"].items():
    if not k.endswith("_t40"):
        continue
    e = c["estimates"]
    th = {a: e[a] for a in th_keys if a in e}
    ex = {a: e[a] for a in ex_keys if a in e}
    d_te = max(abs(th[a] - ex[b]) for a in th for b in ex)
    d_tt = max(abs(th[a] - th[b]) for a in th for b in th)
    med_ex = sorted(ex.values())[len(ex) // 2]
    A4["t40"][k] = dict(max_thermo_vs_exact=d_te, max_thermo_vs_thermo=d_tt, one_minus_F=1 - med_ex,
                        one_minus_F_over_sigma=(1 - med_ex) / SIG)
    if d_te > worst[0]:
        worst = (d_te, k)
A4["t40_worst_thermo_vs_exact"] = dict(value=worst[0], cell=worst[1])
A4["t40_n_series_1minusF_ge_0.1"] = sum(v["one_minus_F"] >= 0.1 for v in A4["t40"].values())
for k, c in cf["cells"].items():
    if k.endswith("_t80"):
        A4["t80_exact_pairs"][k] = dict(spread_exact_baware=c["spread_exact_baware"],
                                        exact_families_within_sigma=c["spread_exact_baware"] <= SIG)
A4["t80_n_exact_within_sigma"] = sum(v["exact_families_within_sigma"] for v in A4["t80_exact_pairs"].values())
out["A4_agreement"] = A4

# ---------------------------------------------------------------------------------------------- A5
ext = json.load(open(os.path.join(R4, "redteam_kills", "profiled_extensions.json")))["dq_plus_secS"]
A5 = {}
for job, v in ext.items():
    for case in ("DQ_local_7.5T2|moderate", "DQ_local_7.5T2|none", "DQ_local_7.5T2|tight"):
        if case in v:
            A5[f"{job}|{case}"] = {t: v[case]["g_med_at"][t] for t in ("0", "40", "60")}
out["A5_K109_local_envelope"] = A5

json.dump(out, open(os.path.join(HERE, "critic_arith.json"), "w"), indent=1)
print(json.dumps(out["A1_qpu_cost_40us"]["all8_comparison"], indent=1))
print(json.dumps(out["A3_40us_vs_horizons"], indent=1))
for nm in T2s:
    print(nm, json.dumps(out["A2_visible_share"][nm], indent=1))
print(json.dumps({k: v for k, v in out["A4_agreement"].items() if k != "t80_exact_pairs"}, indent=1))
print(json.dumps(out["A5_K109_local_envelope"], indent=1))
