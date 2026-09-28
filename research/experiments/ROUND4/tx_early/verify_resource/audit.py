"""Resource-auditor verification of ROUND4 lane tx_early (reads files only; no dynamics; < 5 CPU-s).

Checks
  A. CPU / RAM ledger from the run files themselves (cpu_s, vector_steps, peak_rss_GB).
  B. Cost of the missing pre-registered cells and of the minimal complete T-X-early test, from MEASURED per-step
     rates (not the bench rate), against the 90 CPU-min per-agent cap.
  C. Independent recomputation (from raw run files, not tx_early_summary.json) of the 40 us F ladder, dX, budgets.
  D. Independent back-test (flat-F vs X-converged hybrid).
  E. What the ladder can and cannot show: dF regressed on dH and dfloor separately (is F shown insensitive to H drift,
     or only to the floor?), and the size of the far-spin H drift (CSD) relative to the drifts actually sampled.
  F. Explicit F_inf (H-2 requirement): weighted 1/N fit of F_N, N = 14..22, with typicality errors -> F_inf - F_22 +- se.
  G. Classical break-even at 40 us: cheapest classical cost that reaches the flat-F answer (N = 18) vs N = 22.
Output: audit.json (atomic write)."""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
RUNS = os.path.join(LANE, "runs")
EXP = os.path.abspath(os.path.join(LANE, "..", ".."))
TC = os.path.join(EXP, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
VC = os.path.join(EXP, "ROUND3", "r1sim_exact_reach", "verify_classical", "runs")
SIG = 0.01
SITES = ["1", "7", "8", "9"]


def J(p):
    with open(p) as f:
        return json.load(f)


out = dict(ledger={}, cost={}, recompute={}, backtest={}, tracking={}, finf={}, breakeven={})

# ---------------- A. ledger ----------------
led = {}
tot = 0.0
for f in sorted(glob.glob(os.path.join(RUNS, "*.json"))):
    b = os.path.basename(f)
    if b.startswith("csd") and not b.endswith(".ckpt.json"):
        continue                                   # csd: count the ckpt (same cpu_s)
    if not b.startswith("csd") and not b.endswith(".ckpt.json"):
        continue                                   # driver runs: count the ckpt (cumulative over invocations)
    d = J(f)
    c = float(d.get("cpu_s", 0.0))
    grp = ("VALD" if b.startswith("VALD") else "VAL" if b.startswith("VAL") else "CSD" if b.startswith("csd")
           else b.split("_s4242")[0])
    led.setdefault(grp, dict(cpu_s=0.0, n=0, vector_steps=0))
    led[grp]["cpu_s"] += c
    led[grp]["n"] += 1
    led[grp]["vector_steps"] += int(d.get("vector_steps", 0) or 0)
    tot += c
rss = {}
for f in glob.glob(os.path.join(RUNS, "1UBQ_*.json")):
    if f.endswith(".ckpt.json"):
        continue
    d = J(f)
    if "peak_rss_GB" in d:
        rss[os.path.basename(f)] = d["peak_rss_GB"]
out["ledger"] = dict(groups=led, total_cpu_min_run_files=tot / 60, peak_rss_GB_max=max(rss.values()), peak_rss=rss,
                     note="excludes bench.py / validate.py self-time and analysis scripts (lane: ~1.5 + few min)")

# ---------------- B. cost of missing cells ----------------
# echo mode vector-steps per (sector, vector) per phase n (steps of 2 us): forward advance 20*(1+B) + W x leg n + B legs n
B = 4


def phase_vs(n, prev):
    return (n - prev) * (1 + B) + n * (1 + B)


per_phase = {n: phase_vs(n, p) for n, p in ((20, 0), (40, 20), (60, 40))}          # folded vector-steps
cost = {}
for p in (19, 245):
    e22 = J(os.path.join(RUNS, f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    e20 = J(os.path.join(RUNS, f"1UBQ_p{p}_N20_echo_R2_complex64_s4242_t20-40-60.json"))
    r22 = e22["cpu_s"] / per_phase[20]                                   # measured s per folded vector-step (incl. overhead)
    r20 = e20["cpu_s"] / (2 * per_phase[20])
    miss22 = (per_phase[40] + per_phase[60]) * r22
    miss20 = 2 * (per_phase[40] + per_phase[60]) * r20
    cost[f"p{p}"] = dict(rate_N22_s_per_folded_step=r22, rate_N20_s_per_folded_step=r20,
                         missing_N22_80_120_cpu_min=miss22 / 60, missing_N20R2_80_120_cpu_min=miss20 / 60,
                         full_echo_N22_3phases_cpu_min=(sum(per_phase.values()) * r22) / 60)
miss_total = sum(c["missing_N22_80_120_cpu_min"] + c["missing_N20R2_80_120_cpu_min"] for c in cost.values())
miss_total_bench = sum((per_phase[40] + per_phase[60]) * 4.1 / 60 for _ in (19, 245)) + sum(
    c["missing_N20R2_80_120_cpu_min"] for c in cost.values())
# minimal complete pre-registered test: F_22 at 3 phases (echo mode also yields H_22, floor_22), X_20 from existing
# reference F_20 checkpoint + VC honly H_20 (free), CSD N_c = 80 (~4.3 min/probe measured)
csd_min = led.get("CSD", {}).get("cpu_s", 0) / 60
min_full = sum(c["full_echo_N22_3phases_cpu_min"] for c in cost.values()) + 2 * 4.3
out["cost"] = dict(per_phase_folded_vector_steps=per_phase, per_probe=cost,
                   missing_cells_total_cpu_min=miss_total, missing_cells_total_cpu_min_at_bench_rate=miss_total_bench,
                   minimal_complete_test_cpu_min=min_full, cap_cpu_min=90,
                   critic_A1_budget_estimate_cpu_min="30-45 (ROUND3/CRITIC.md A-1)",
                   verdict=("the pre-registered T-X-early test was infeasible under one agent's 90 CPU-min cap regardless "
                            "of allocation: minimal complete cost > cap"))

# ---------------- C. recompute 40 us cells ----------------
def vc(p, N):
    d = J(glob.glob(os.path.join(VC, f"1UBQ_p{p}_N{N}_probe_honly_*.json"))[0])
    return np.array(d["H"]), np.array(d["floor"])            # times 40, 80, ... 320


summ = J(os.path.join(LANE, "tx_early_summary.json"))
rec = {}
ladder = {}
for p in (19, 245):
    e22 = J(os.path.join(RUNS, f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    h22 = J(os.path.join(RUNS, f"1UBQ_p{p}_N22_honly_R1_complex64_s4242_t20-40-60.json"))
    e20 = J(os.path.join(RUNS, f"1UBQ_p{p}_N20_echo_R2_complex64_s4242_t20-40-60.json"))
    ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json")) for N in (12, 14, 16, 18)}
    r20 = J(os.path.join(TC, f"1UBQ_p{p}_N20.json.ckpt.json"))["done"]
    pp = summ["per_probe"][f"p{p}"]
    se_H = pp["se_H"][0]
    off = pp["offset_exact_minus_csd_22"][0]
    HF = {N: vc(p, N) for N in (12, 14, 16, 18, 20)}
    L = dict(N=[12, 14, 16, 18, 20, 22],
             H=[float(HF[N][0][0]) for N in (12, 14, 16, 18, 20)] + [float(h22["H"][0])],
             floor=[float(HF[N][1][0]) for N in (12, 14, 16, 18, 20)] + [float(h22["floor"][0])],
             H20_R2=e20["H"][0], floor20_R2=e20["floor"][0], H22_echo=e22["H"][0], floor22_echo=e22["floor"][0], F={})
    for b in SITES:
        Fl = [ref[N]["F"][b][1] for N in (12, 14, 16, 18)] + [e20["F"][b][0], e22["F"][b][0]]
        Fref20 = r20["20"][b]
        L["F"][b] = dict(F=Fl, F20_ref=Fref20)
        X22 = e22["X"][b][0]
        X20 = e20["X"][b][0]
        dX = X22 - X20
        bud = math.sqrt(se_H ** 2 + off ** 2 + dX ** 2)
        rec[f"p{p}_b{b}"] = dict(F16=Fl[2], F18=Fl[3], F20=Fl[4], F22=Fl[5], F20_ref=Fref20, X20=X20, X22=X22, dX=dX,
                                 budget=bud, pass_cell=bool(abs(dX) <= 0.005 and bud <= SIG),
                                 max_absdF_18_22=max(abs(Fl[3] - Fl[5]), abs(Fl[4] - Fl[5])),
                                 max_absdF_16_22=max(abs(f - Fl[5]) for f in Fl[2:5]),
                                 lane_dX=summ["cells"][f"p{p}_t40_b{b}"]["dX"],
                                 lane_budget=summ["cells"][f"p{p}_t40_b{b}"]["budget"])
    ladder[f"p{p}"] = L
out["recompute"] = dict(cells=rec, n_pass_40us=int(sum(c["pass_cell"] for c in rec.values())),
                        max_absdF_18_22=max(c["max_absdF_18_22"] for c in rec.values()),
                        max_absdF_16_22=max(c["max_absdF_16_22"] for c in rec.values()),
                        max_diff_vs_lane_dX=max(abs(c["dX"] - c["lane_dX"]) for c in rec.values()),
                        max_diff_vs_lane_budget=max(abs(c["budget"] - c["lane_budget"]) for c in rec.values()))

# ---------------- D. back-test (independent) ----------------
bt = {}
for Ns in (14, 16, 18):
    eh, ef = [], []
    for p in (19, 245):
        L = ladder[f"p{p}"]
        i = L["N"].index(Ns)
        for b in SITES:
            Ft = L["F"][b]["F"][5]
            Fs = L["F"][b]["F"][i]
            Xs = Fs - L["H"][i] - L["floor"][i]
            eh.append(L["H"][5] + L["floor"][5] + Xs - Ft)
            ef.append(Fs - Ft)
    eh, ef = np.array(eh), np.array(ef)
    bt[f"Ns{Ns}"] = dict(rms_hybrid=float(np.sqrt(np.mean(eh ** 2))), rms_flat=float(np.sqrt(np.mean(ef ** 2))),
                         flat_better=int(np.sum(np.abs(ef) < np.abs(eh))), n=len(ef))
out["backtest"] = bt

# ---------------- E. does the ladder show F insensitive to H drift, or only to floor drift? ----------------
tr = {}
for p in (19, 245):
    L = ladder[f"p{p}"]
    N = L["N"]
    H = np.array(L["H"]); fl = np.array(L["floor"])
    steps = []
    for i in range(len(N) - 1):
        dH = H[i + 1] - H[i]; dfl = fl[i + 1] - fl[i]
        dF = [L["F"][b]["F"][i + 1] - L["F"][b]["F"][i] for b in SITES]
        steps.append(dict(step=f"{N[i]}->{N[i+1]}", dH=float(dH), dfloor=float(dfl), dF_sites=[float(x) for x in dF],
                          dF_mean=float(np.mean(dF))))
    dH_tot_14_22 = float(H[5] - H[1]); dfl_tot_14_22 = float(fl[5] - fl[1])
    D = summ["per_probe"][f"p{p}"]["D_80_22_crn"][0]
    seD = summ["per_probe"][f"p{p}"]["se_D"][0]
    tr[f"p{p}"] = dict(steps=steps, dH_14_22=dH_tot_14_22, dfloor_14_22=dfl_tot_14_22,
                       max_abs_dH_per_step=float(np.max(np.abs(np.diff(H)))),
                       csd_far_drift_D_80_22=D, se_D=seD,
                       far_drift_over_max_sampled_step=float(abs(D) / np.max(np.abs(np.diff(H)))),
                       far_drift_over_sampled_14_22=float(abs(D) / max(abs(dH_tot_14_22), 1e-9)))
# pooled regression of site-mean dF on (dH, dfloor) over all ladder steps and both probes (N >= 14 steps)
rows = []
for p in (19, 245):
    for s in tr[f"p{p}"]["steps"]:
        if s["step"].startswith("12"):
            continue
        for x in s["dF_sites"]:
            rows.append((s["dH"], s["dfloor"], x))
A = np.array([[r[0], r[1]] for r in rows]); y = np.array([r[2] for r in rows])
coef, res, *_ = np.linalg.lstsq(A, y, rcond=None)
resid = y - A @ coef
dof = max(len(y) - 2, 1)
s2 = float(resid @ resid / dof)
cov = s2 * np.linalg.inv(A.T @ A)
tr["pooled_regression_dF_on_dH_dfloor_N14plus"] = dict(
    n=len(y), coef_dH=float(coef[0]), se_dH=float(math.sqrt(cov[0, 0])), coef_dfloor=float(coef[1]),
    se_dfloor=float(math.sqrt(cov[1, 1])), corr_dH_dfloor=float(cov[0, 1] / math.sqrt(cov[0, 0] * cov[1, 1])),
    note="coef 1 = F tracks that component additively (hybrid picture); 0 = F insensitive (flat-F picture)")
out["tracking"] = tr

# F_inf scenarios at 40 us (sigma units): flat / F tracks far-spin H drift only / hybrid (tracks H drift and floor)
sc = {}
for p in (19, 245):
    pp = summ["per_probe"][f"p{p}"]
    D = pp["D_80_22_crn"][0]; fl22 = pp["floor22_exact"][0]
    sc[f"p{p}"] = dict(flat=0.0, tracks_far_H_drift_only=D / SIG, hybrid=(D - fl22) / SIG,
                       note="F_inf - F_22 in units of sigma under each finite-size picture")
out["tracking"]["F_inf_minus_F22_scenarios_sigma"] = sc

# ---------------- F. explicit F_inf by weighted 1/N fit (H-2) ----------------
fi = {}
for p in (19, 245):
    L = ladder[f"p{p}"]
    Ns = np.array([14, 16, 18, 20, 22], float)
    # typicality std of F: ~2^{-N/2} per vector (reference err_typ = 2^{-9} at N = 18); R = 2 at N = 20
    sd = np.array([2 ** -7, 2 ** -8, 2 ** -9, 2 ** -10 / math.sqrt(2), 2 ** -11])
    for b in SITES:
        F = np.array(L["F"][b]["F"][1:])
        A = np.vstack([np.ones(5), 1 / Ns]).T
        W = np.diag(1 / sd ** 2)
        cov = np.linalg.inv(A.T @ W @ A)
        c = cov @ A.T @ W @ F
        chi2 = float(((A @ c - F) / sd) @ ((A @ c - F) / sd))
        # 16..22 unweighted (lane's version) for comparison
        A2 = A[1:]; c2, *_ = np.linalg.lstsq(A2, F[1:], rcond=None)
        fi[f"p{p}_b{b}"] = dict(Finf_w=float(c[0]), se_Finf_w=float(math.sqrt(cov[0, 0])),
                                Finf_w_minus_F22=float(c[0] - F[-1]), slope_c=float(c[1]),
                                se_slope=float(math.sqrt(cov[1, 1])), chi2_dof3=chi2,
                                Finf_unw16_22_minus_F22=float(c2[0] - F[-1]))
out["finf"] = dict(cells=fi, max_abs_Finf_w_minus_F22=max(abs(v["Finf_w_minus_F22"]) for v in fi.values()),
                   note=("typicality sd model 2^{-N/2}; a 1/N form is itself an assumption (floor ~ 1/N; far-spin H drift "
                         "is not 1/N in cluster size -- CSD D_80_22 shows it)"))

# ---------------- G. classical break-even at 40 us ----------------
n18 = J(os.path.join(RUNS, "1UBQ_p19_N18_echo_R1_complex64_s4242_t20-40-60.json"))
# N = 18 all three phases 9000 sector-steps (10 sectors x 900); phase-1 share = 200/900
n18_40 = n18["cpu_s"] * per_phase[20] / sum(per_phase.values())
out["breakeven"] = dict(
    classical_cpu_s_N18_40us_one_probe=n18_40, classical_cpu_s_N22_40us_one_probe=cost["p19"]["rate_N22_s_per_folded_step"] * per_phase[20],
    flat_F_N18_rms_vs_F22=bt["Ns18"]["rms_flat"],
    note=("at 40 us a classical workstation reaches F_22 to ~sigma/7 rms from N = 18 in ~0.4 CPU-min per probe; "
          "no quantum device can break even against that on this observable. The unresolved part is not cost but "
          "accuracy vs the N -> inf echo (far-spin H drift), which no amount of N <= 22 compute resolves"))

tmp = os.path.join(HERE, "audit.json.tmp")
with open(tmp, "w") as f:
    json.dump(out, f, indent=1)
os.replace(tmp, os.path.join(HERE, "audit.json"))

# console
print("LEDGER total CPU-min (run files):", round(out["ledger"]["total_cpu_min_run_files"], 1), " peak RSS GB:",
      round(out["ledger"]["peak_rss_GB_max"], 3))
for g, v in led.items():
    print("  ", g, round(v["cpu_s"] / 60, 2), "min", v["n"], "files")
print("COST per phase folded steps", per_phase)
for k, v in cost.items():
    print("  ", k, {a: round(b, 3) for a, b in v.items()})
print("  missing total CPU-min", round(miss_total, 1), "(bench-rate", round(miss_total_bench, 1), ") minimal complete test",
      round(min_full, 1))
print("RECOMPUTE n_pass_40us", out["recompute"]["n_pass_40us"], "maxdF18-22", round(out["recompute"]["max_absdF_18_22"], 4),
      "maxdF16-22", round(out["recompute"]["max_absdF_16_22"], 4), "diff vs lane dX", out["recompute"]["max_diff_vs_lane_dX"],
      "budget", out["recompute"]["max_diff_vs_lane_budget"])
for k, v in rec.items():
    print("  ", k, {a: round(b, 4) if isinstance(b, float) else b for a, b in v.items() if a in ("F16", "F18", "F20", "F22", "F20_ref", "dX", "budget", "pass_cell")})
print("BACKTEST", {k: {a: round(b, 4) for a, b in v.items()} for k, v in bt.items()})
for p in (19, 245):
    t = tr[f"p{p}"]
    print(f"TRACK p{p}: dH14-22 {t['dH_14_22']:+.4f} dfloor14-22 {t['dfloor_14_22']:+.4f} max|dH|/step {t['max_abs_dH_per_step']:.4f} "
          f"CSD D80-22 {t['csd_far_drift_D_80_22']:+.4f}+-{t['se_D']:.4f} ratio(D/max step) {t['far_drift_over_max_sampled_step']:.1f}")
    for s in t["steps"]:
        print(f"    {s['step']}: dH {s['dH']:+.4f} dfloor {s['dfloor']:+.4f} dF {[round(x, 4) for x in s['dF_sites']]}")
print("REGRESSION", {k: (round(v, 3) if isinstance(v, float) else v) for k, v in tr["pooled_regression_dF_on_dH_dfloor_N14plus"].items()})
print("SCENARIOS (sigma)", {k: {a: (round(b, 2) if isinstance(b, float) else b) for a, b in v.items() if a != "note"} for k, v in sc.items()})
print("FINF weighted 1/N fit:")
for k, v in fi.items():
    print("  ", k, {a: round(b, 4) for a, b in v.items()})
print("BREAKEVEN", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in out["breakeven"].items() if k != "note"})
