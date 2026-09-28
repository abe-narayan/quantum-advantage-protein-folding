"""Round-3 completeness critic: two cheap checks + one derivation (no new dynamics).

C1  Early-window (t <= T3) convergence audit of the dipolar echo, from files already on disk
    (r1sim_exact_reach/verify_classical/verify_summary.json).  Question: inside the physical reversal
    horizon (T3 ~ 30-70 us physical-feasibility lens; <= ~123 us most generous), is the converged echo
    classically reproduced to sigma?  Uses the exact decomposition F = H + floor + X.
C2  Methyl-rotor (NA-2 / K-111) observability re-derivation, from new_mechanisms_A/t2_methyl_rotor JSONs:
    convert splittings and couplings to frequency units; express the many-body (mean-field) error as an
    equivalent barrier shift.
D1  Generalised floor B*_s, T*_Q,s (hardness lane formula) applied to a physics-based all-atom explicit-solvent
    MD comparator (parameters are stated assumptions, INFERENCE).

Single-threaded, < 1 CPU-s.  Output: critic_checks.json (atomic write).
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R3 = os.path.dirname(HERE)
SIGMA = 0.01
UEV_TO_HZ = 1e-6 / 4.135667696e-15  # 1 ueV in Hz (241.8 MHz)

out = {}

# ------------------------------------------------------------------ C1
vs = json.load(open(os.path.join(R3, "r1sim_exact_reach", "verify_classical", "verify_summary.json")))
T = vs["times_us"]
c1 = {"times_us_checked": [40, 80, 120], "sigma": SIGMA, "rows": [], "notes": []}
for pr in ("p19", "p245"):
    p = vs[pr]
    hinf = p["H_inf"]
    for t in (40, 80, 120):
        it = T.index(t)
        H_by_N = {int(N): p["H"][N][it] for N in p["H"]}
        fl_by_N = {int(N): p["floor"][N][it] for N in p["floor"]}
        Hinf, se, off = hinf["H_inf"][it], hinf["se"][it], hinf["offset"][it]
        for b in (1, 7, 8, 9):
            key = f"t{t}_b{b}"
            s = p["series"][key]
            he = p["hybrid_estimates"][key]
            Ns, F, X, dX = s["N"], s["F"], s["X"], s["dX"]
            Nl = Ns[-1]
            step_F = abs(F[-1] - F[-2])
            gap_to_inf = F[-1] - he["F_inf_hybrid"]
            two_flat = len(dX) >= 2 and abs(dX[-1]) <= 0.005 and abs(dX[-2]) <= 0.005
            c1["rows"].append(dict(
                probe=pr, t_us=t, site=b, N_last=Nl,
                F_last=round(F[-1], 4), step_F_last=round(step_F, 4),
                floor_last=round(fl_by_N[Nl], 4), H_last=round(H_by_N[Nl], 4), H_inf=round(Hinf, 4),
                F_last_minus_Finf_hybrid=round(gap_to_inf, 4), in_sigma=round(gap_to_inf / SIGMA, 1),
                dX_last=round(dX[-1], 4), dX_prev=round(dX[-2], 4) if len(dX) >= 2 else None,
                X_two_consecutive_steps_le_0p005=two_flat, verifier_flag_X_flat=he["X_flat"],
                hybrid_H_error_budget=round(math.hypot(se, off), 4),
            ))
rows = c1["rows"]
c1["summary"] = dict(
    n_series=len(rows),
    step_statistic_passes_sigma=sum(r["step_F_last"] < SIGMA for r in rows),
    finite_N_F_more_than_3sigma_from_hybrid_Finf=sum(abs(r["F_last_minus_Finf_hybrid"]) > 3 * SIGMA for r in rows),
    range_F_last_minus_Finf=[min(r["F_last_minus_Finf_hybrid"] for r in rows),
                             max(r["F_last_minus_Finf_hybrid"] for r in rows)],
    floor_range=[min(r["floor_last"] for r in rows), max(r["floor_last"] for r in rows)],
    X_two_step_flat=sum(r["X_two_consecutive_steps_le_0p005"] for r in rows),
    verifier_X_flat=sum(bool(r["verifier_flag_X_flat"]) for r in rows),
    hybrid_H_error_budget_range=[min(r["hybrid_H_error_budget"] for r in rows),
                                 max(r["hybrid_H_error_budget"] for r in rows)],
    t40_only=dict(
        step_passes=sum(r["step_F_last"] < SIGMA for r in rows if r["t_us"] == 40),
        gt3sigma_from_Finf=sum(abs(r["F_last_minus_Finf_hybrid"]) > 3 * SIGMA for r in rows if r["t_us"] == 40),
        X_two_step_flat=sum(r["X_two_consecutive_steps_le_0p005"] for r in rows if r["t_us"] == 40),
    ),
)
# p245 t=40 common-mode X shift (b-independent drift leaking into X)
c1["p245_t40_dX_last_by_site"] = [r["dX_last"] for r in rows if r["probe"] == "p245" and r["t_us"] == 40]
c1["notes"].append("F_inf_hybrid = H_inf(CSD N_c>=80 + exact-CSD offset at N=20) + X_last (floor -> 0); this is the "
                   "verification lane's own estimator, not a new one. The floor term is exact and b-independent.")
out["C1_early_window"] = c1

# ------------------------------------------------------------------ C2
st = json.load(open(os.path.join(R3, "new_mechanisms_A", "t2_methyl_rotor", "summary_t2.json")))
sr = {float(k): v for k, v in st["single_rotor_splitting_ueV_B0.655"].items()}
Vs = sorted(sr)
dlnD = {}
for i in range(1, len(Vs) - 1):
    v0, v1, v2 = Vs[i - 1], Vs[i], Vs[i + 1]
    dlnD[v1] = -(math.log(sr[v2]) - math.log(sr[v0])) / (v2 - v0)  # per meV (positive number)
c2 = {"single_rotor": {str(v): dict(Delta_ueV=sr[v], Delta_Hz=sr[v] * UEV_TO_HZ) for v in Vs},
      "dlnDelta_dV3_per_meV": {str(k): round(v, 4) for k, v in dlnD.items()}}
per_v3 = {}
for v3 in (30, 60, 100):
    s = st[f"V3_{v3}"]
    lo, hi = s["Delta_exact_ueV_min_max"]
    mf = s["median_rel_mf_err"]
    slope = dlnD.get(float(v3)) or dlnD[min(dlnD, key=lambda k: abs(k - v3))]
    per_v3[str(v3)] = dict(
        dressed_Delta_Hz_range=[lo * UEV_TO_HZ, hi * UEV_TO_HZ],
        max_abs_J_Hz=s["max_abs_J_ueV"] * UEV_TO_HZ,
        median_rel_mf_err=mf,
        equivalent_barrier_shift_meV_of_median_mf_err=round(math.log(1 + mf) / slope, 2),
    )
c2["per_V3"] = per_v3
c2["notes"] = [
    "Kill clause (i) used backscattering-INS resolution (~0.1-1 ueV = 24-240 MHz) as the observability limit.",
    "Dressed splittings at V3 = 100 meV reach ~13 MHz; NMR-based tunnelling spectroscopy works in the kHz-MHz "
    "range at cryogenic temperature [LITERATURE, recalled; one supporting arXiv abstract: cond-mat/0701201].",
    "The many-body correction that matters (mean-field error) is 13-40% of Delta, i.e. an equivalent barrier "
    "shift of only a few meV; compare with force-field barrier uncertainty and glass disorder [INFERENCE].",
]
out["C2_methyl_rotor"] = c2

# ------------------------------------------------------------------ D1
# Generalised floor (hardness lane): X = A rho K n_b G t_T / c ; B*_s = X^(s/(s-1)) ; T*_Q,s = K n_b G t_T X^(1/(s-1))
scen = {
    "A80_L100_MO (lane check)": dict(K=10, n_b=1, A=1, rho=1, G=9.3e7, c=1.6e-3),
    "allatom_explicit_30k_atoms_GPU_optimistic": dict(K=10, n_b=1, A=1, rho=1, G=1e9, c=2e-4),
    "allatom_explicit_30k_atoms_GPU_central": dict(K=10, n_b=1, A=1, rho=1, G=1e10, c=2e-4),
}
d1 = {"assumptions": "t_T = 1 us; MO overheads (K=10, n_b=1, A=rho=1) as in hardness_what_it_takes. All-atom G is an "
                     "order-of-magnitude INFERENCE (3e4 atoms x ~300 cutoff neighbours x 1e2-1e3 Toffolis per pair "
                     "term, PME ignored); c ~ 0.2 ms per MD step for ~3e4 atoms on one modern GPU (INFERENCE).",
      "classical_md_reference": "fast folders ~1e9 steps per folding event; ms folders ~1e11-1e12 steps "
                                "(2-4 fs steps) [INFERENCE, order of magnitude]",
      "rows": {}}
tT = 1e-6
for name, q in scen.items():
    X = q["A"] * q["rho"] * q["K"] * q["n_b"] * q["G"] * tT / q["c"]
    row = {"X": X}
    for s in (2, 3, 4):
        B = X ** (s / (s - 1))
        TQ = q["K"] * q["n_b"] * q["G"] * tT * X ** (1 / (s - 1))
        row[f"s{s}"] = dict(B_star_steps=B, T_Q_star_s=TQ, T_Q_star_yr=TQ / 3.156e7)
    d1["rows"][name] = row
out["D1_allatom_floor"] = d1

tmp = os.path.join(HERE, "critic_checks.json.tmp")
with open(tmp, "w") as f:
    json.dump(out, f, indent=1)
os.replace(tmp, os.path.join(HERE, "critic_checks.json"))
print(json.dumps(c1["summary"], indent=1))
print("p245 t40 dX_last:", c1["p245_t40_dX_last_by_site"])
for r in rows:
    print(r["probe"], r["t_us"], r["site"], "N", r["N_last"], "stepF", r["step_F_last"], "F-Finf", r["F_last_minus_Finf_hybrid"],
          "floor", r["floor_last"], "dX", r["dX_prev"], r["dX_last"], "2flat", r["X_two_consecutive_steps_le_0p005"])
print(json.dumps(c2["per_V3"], indent=1))
print(json.dumps(c2["dlnDelta_dV3_per_meV"]))
for k, v in d1["rows"].items():
    print(k, "X=%.2e" % v["X"], {s: ("B*=%.1e" % v[s]["B_star_steps"], "T*=%.2g yr" % v[s]["T_Q_star_yr"]) for s in ("s2", "s3", "s4")})
