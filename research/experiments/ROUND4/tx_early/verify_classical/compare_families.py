"""Verifier: cross-family comparison of the exact finite-cluster echo F_ab(t) (no dynamics; -> verify_summary.json).

Families (all: same reference Trotter circuit, dt = 2 us unless noted, b0 = random_b0(1000), typicality, complex64):
  probe     lane / reference family (N nearest to the probe a): F_16, F_18 (typicality_cone), F_20 (typicality_cone
            checkpoint; lane R = 2 at 40 us), F_22 (lane, 40 us only)
  SA2_N     'bpart:(N-2):2'  probe ranks 0..N-3 + the 2 strongest-|d_bc| partners c of site b not yet included
  SA4_20    'bpart:16:4'     probe ranks 0..15 + 4 strongest missing partners of b (N = 20)
  pairb_20  ROUND3 decomp_echo 'pairb' family: 20 nearest to {a, b} (metric min(d_ia, d_ib))
  dt1       SA2_20 and probe_20 re-run with dt = 1 us (Trotter check), 40 us
Claim models evaluated against the b-aware families at 40 us: 'F converged' (probe F_22) and the T-X hybrid
(H_inf + X_22, from the lane's summary).
"""
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
EXP = os.path.abspath(os.path.join(LANE, "..", ".."))
TC = os.path.join(EXP, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
RUNS = os.path.join(HERE, "runs")
SIG = 0.01
SITES = [1, 7, 8, 9]
TIMES = [40, 80, 120]


def J(p):
    with open(p) as f:
        return json.load(f)


def mine(p, spec, b, N, dt=None):
    sp = spec.replace(":", "-")
    pat = f"1UBQ_p{p}_{sp}_b{b}_N{N}_R1_complex64_s4242_t{'40' if dt else '20-40-60'}{'_dt1' if dt else ''}.json"
    f = os.path.join(RUNS, pat)
    if not os.path.exists(f):
        return None
    d = J(f)
    key = "1" if spec.startswith("pairb") else str(b)
    vals = d["F"][key]
    return dict(zip([int(round(t)) for t in d["times_us"]], vals)) if not dt else {40: vals[0]}, d


geo = J(os.path.join(HERE, "geometry.json"))
lane = J(os.path.join(LANE, "tx_early_summary.json"))
out = dict(sigma=SIG, series={}, tables={})
for p in (19, 245):
    ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json"))["F"] for N in (16, 18)}
    r20 = J(os.path.join(TC, f"1UBQ_p{p}_N20.json.ckpt.json"))["done"]
    n22 = J(os.path.join(LANE, "runs", f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    n20 = J(os.path.join(LANE, "runs", f"1UBQ_p{p}_N20_echo_R2_complex64_s4242_t20-40-60.json"))
    Hinf40 = lane["per_probe"][f"p{p}"]["H_inf"][0]
    for b in SITES:
        s = dict(probe=p, site=b, t={})
        g = geo[f"p{p}"]["sites"][f"site{b}"]
        s["b_name"] = g["name"]
        s["b_M2_frac_inside_probe_N"] = g["frac_M2_inside_N"]
        s["b_strongest_partner"] = g["strongest"][0]
        fam = {}
        for spec, N, tag in (("bpart:16:2", 18, "SA2_18"), ("bpart:18:2", 20, "SA2_20"), ("bpart:20:2", 22, "SA2_22"),
                             ("bpart:16:4", 20, "SA4_20"), ("pairb:20", 20, "pairb_20")):
            r = mine(p, spec, b, N)
            if r:
                fam[tag] = r[0]
                s.setdefault("clusters", {})[tag] = dict(spec=spec, ranks=r[1]["cluster"]["ranks"],
                                                          H=r[1]["H"], floor=r[1]["floor"], cpu_s=r[1]["cpu_s"])
        for spec, N, tag in (("bpart:18:2", 20, "SA2_20_dt1"), ("probe:20", 20, "probe_20_dt1")):
            r = mine(p, spec, b, N, dt=1)
            if r:
                fam[tag] = r[0]
        for ti, t in enumerate(TIMES):
            c = {}
            c["probe_16"] = ref[16][str(b)][ti + 1]
            c["probe_18"] = ref[18][str(b)][ti + 1]
            if str(20 * (ti + 1)) in r20:
                c["probe_20_ref"] = r20[str(20 * (ti + 1))][str(b)]
            if t == 40:
                c["probe_20_lane"] = n20["F"][str(b)][0]
                c["probe_22"] = n22["F"][str(b)][0]
            for tag, v in fam.items():
                if t in v:
                    c[tag] = v[t]
            probe_best = c.get("probe_22", c.get("probe_20_ref", c["probe_18"]))
            probe_best_N = 22 if "probe_22" in c else (20 if "probe_20_ref" in c else 18)
            baware = [c[k] for k in ("SA2_22", "SA2_20", "SA4_20", "pairb_20") if k in c]
            sa_best = c.get("SA2_22", c.get("SA2_20", c.get("SA2_18")))
            c.update(probe_best=probe_best, probe_best_N=probe_best_N, SA_best=sa_best,
                     delta_SA_minus_probe=sa_best - probe_best,
                     delta_in_sigma=(sa_best - probe_best) / SIG,
                     baware_spread=(max(baware) - min(baware)) if len(baware) > 1 else None,
                     SA2_step_18_20=(c["SA2_20"] - c["SA2_18"]) if "SA2_20" in c and "SA2_18" in c else None)
            if "SA2_22" in c:
                c["SA2_step_20_22"] = c["SA2_22"] - c["SA2_20"]
            if "SA2_20_dt1" in c:
                c["trotter_check"] = dict(delta_dt2=c["SA2_20"] - c["probe_20_lane"],
                                          delta_dt1=c["SA2_20_dt1"] - c["probe_20_dt1"])
            if t == 40:
                X22 = n22["X"][str(b)][0]
                c["claim_flat_F_err_vs_SA"] = probe_best - sa_best
                c["claim_hybrid"] = Hinf40 + X22
                c["claim_hybrid_err_vs_SA"] = Hinf40 + X22 - sa_best
            s["t"][t] = c
        out["series"][f"p{p}_b{b}"] = s

# headline tables
for t in TIMES:
    rows = []
    for k, s in out["series"].items():
        c = s["t"][t]
        rows.append(dict(series=k, probe_best=c["probe_best"], N=c["probe_best_N"], SA_best=c["SA_best"],
                         delta=c["delta_SA_minus_probe"], delta_sigma=c["delta_in_sigma"],
                         pairb=c.get("pairb_20"), SA4=c.get("SA4_20"), SA_step=c.get("SA2_step_18_20")))
    out["tables"][f"t{t}"] = rows
    d = np.array([r["delta"] for r in rows])
    out["tables"][f"t{t}_counts"] = dict(n_abs_delta_gt_sigma=int(np.sum(np.abs(d) > SIG)),
                                         n_abs_delta_gt_2sigma=int(np.sum(np.abs(d) > 2 * SIG)),
                                         max_abs_delta=float(np.max(np.abs(d))),
                                         max_abs_SA_step=float(np.nanmax([abs(r["SA_step"]) for r in rows if r["SA_step"] is not None])))
fe = np.array([out["series"][k]["t"][40]["claim_flat_F_err_vs_SA"] for k in out["series"]])
he = np.array([out["series"][k]["t"][40]["claim_hybrid_err_vs_SA"] for k in out["series"]])
out["claim_models_vs_baware_40us"] = dict(flat_F_rms=float(np.sqrt(np.mean(fe ** 2))), flat_F_max=float(np.max(np.abs(fe))),
                                          hybrid_rms=float(np.sqrt(np.mean(he ** 2))), hybrid_max=float(np.max(np.abs(he))),
                                          n_flat_within_sigma=int(np.sum(np.abs(fe) <= SIG)),
                                          n_hybrid_within_sigma=int(np.sum(np.abs(he) <= SIG)))
cpu = sum(J(f)["cpu_s"] for f in glob.glob(os.path.join(RUNS, "*.json")) if not f.endswith("ckpt.json"))
out["cpu_s_all_runs"] = cpu
with open(os.path.join(HERE, "verify_summary.json.tmp"), "w") as f:
    json.dump(out, f, indent=1)
os.replace(os.path.join(HERE, "verify_summary.json.tmp"), os.path.join(HERE, "verify_summary.json"))

for t in TIMES:
    print(f"== t = {t} us  (delta = SA_best - probe_best)")
    for r in out["tables"][f"t{t}"]:
        print(f"  {r['series']:8s} probe_N{r['N']} {r['probe_best']:.4f} | SA {r['SA_best']:.4f} SA4 "
              f"{'' if r['SA4'] is None else format(r['SA4'], '.4f'):6s} pairb {'' if r['pairb'] is None else format(r['pairb'], '.4f'):6s}"
              f" | delta {r['delta']:+.4f} ({r['delta_sigma']:+.1f} sig) SA step18-20 "
              f"{'' if r['SA_step'] is None else format(r['SA_step'], '+.4f')}")
    print("  ", out["tables"][f"t{t}_counts"])
for k, s in out["series"].items():
    c = s["t"][40]
    if "trotter_check" in c:
        print(k, "Trotter:", {a: round(v, 4) for a, v in c["trotter_check"].items()}, "SA2 N18/20/22:",
              round(c["SA2_18"], 4), round(c["SA2_20"], 4), round(c.get("SA2_22", float('nan')), 4))
print("claim models at 40 us vs b-aware:", out["claim_models_vs_baware_40us"])
print("cpu_s all verifier runs:", round(cpu, 1))
