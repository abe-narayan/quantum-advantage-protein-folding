"""Solver-vs-model decomposition for active-site structural questions, plus a literature-
anchored fault-tolerant (FT) cost model. Lane ROUND3/new_mechanisms_intrinsic.

Question: when an active-site structural question (which isomer / spin state / protonation
state / ligand, and hence which geometry) is decided by computed relative energies, how
much does replacing the best CLASSICAL electronic-structure solver by an EXACT (quantum,
QPE) solver reduce the structural error, given that other ("model") errors remain?

Model (DERIVED, stated here):
  candidates A, B; true gap D >= 0 (A lower); structural lever dq (A) = |q_A - q_B|.
  computed gap D_hat = D + e_s + e_m, e_s ~ N(0, s_s^2) solver error, e_m ~ N(0, s_m^2)
  model error (environment/QM-region, thermal/conformational averaging, geometry, basis,
  active-space definition). An exact solver sets s_s = 0; it does not touch s_m.
  Readout 1 (argmin):     E|dq_err| = dq * Phi(-D / s),  s = sqrt(s_s^2 + s_m^2)
  Readout 2 (Boltzmann):  E|dq_err| = dq * E_eps |w(D + eps) - w(D)|, w(x) = 1/(1+e^{x/kT})
  Value of the exact solver: VOI = E_err(s_s, s_m) - E_err(0, s_m).
  Closed form (argmin, fixed D): max_D [Phi(D/a) - Phi(D/b)], a = s_m, b = sqrt(s_s^2+s_m^2),
  attained at D* = a b sqrt(2 ln(b/a) / (b^2 - a^2)).

Energies in kcal/mol, lengths in Angstrom, T = 300 K. Single-threaded, seconds of CPU.
Output: ../results/decision_value.json (atomic write).
"""
from __future__ import annotations

import json
import math
import os

import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results")
KT = 0.0019872 * 300.0  # kcal/mol

GH_X, GH_W = np.polynomial.hermite_e.hermegauss(80)  # probabilists' Hermite: E[f(Z)] = sum w f(x) / sqrt(2 pi)
GH_W = GH_W / math.sqrt(2 * math.pi)


def w_min(D):
    return 1.0 / (1.0 + np.exp(np.clip(D / KT, -700, 700)))


def err_argmin(D, s):
    return norm.cdf(-D / s) if s > 0 else (D < 0).astype(float)


def err_boltz(D, s):
    if s == 0:
        return np.zeros_like(D)
    eps = s * GH_X[None, :]
    return (np.abs(w_min(D[:, None] + eps) - w_min(D[:, None])) * GH_W[None, :]).sum(1)


def prior_avg(fun, tau, s):
    D = np.linspace(0, 8 * tau, 4001)
    pdf = 2 * norm.pdf(D, scale=tau)
    pdf /= np.trapezoid(pdf, D)
    return float(np.trapezoid(fun(D, s) * pdf, D))


def max_gain_closed_form(s_s, s_m):
    a, b = s_m, math.hypot(s_s, s_m)
    if s_s == 0:
        return 0.0, 0.0
    Dst = a * b * math.sqrt(2 * math.log(b / a) / (b * b - a * a))
    return float(norm.cdf(Dst / a) - norm.cdf(Dst / b)), float(Dst)


def grid():
    rows = []
    for s_m in (0.5, 1.0, 2.0, 3.0, 5.0):
        for s_s in (0.0, 0.5, 1.0, 2.0, 3.0, 5.0, 10.0):
            for tau in (1.0, 3.0, 10.0):
                s_b = math.hypot(s_s, s_m)
                pa_b = prior_avg(err_argmin, tau, s_b)
                pa_x = prior_avg(err_argmin, tau, s_m)
                pb_b = prior_avg(err_boltz, tau, s_b)
                pb_x = prior_avg(err_boltz, tau, s_m)
                g, Dst = max_gain_closed_form(s_s, s_m)
                rows.append(dict(sigma_model=s_m, sigma_solver=s_s, tau_gap=tau,
                                 P_wrong_best=pa_b, P_wrong_exact=pa_x, dP_exact_minus_best=pa_b - pa_x,
                                 boltz_popErr_best=pb_b, boltz_popErr_exact=pb_x,
                                 max_dP_over_gap=g, gap_at_max=Dst))
    return rows


# ----------------------------------------------------------------------------------------
# Scenario table: each structural question with literature-anchored ranges.
# dq: MEASURED in pdb_census.json where marked; sigma values: see README (tags per row).
# sigma_solver_best = best CLASSICAL method demonstrated/feasible for that site size.
# ----------------------------------------------------------------------------------------
SCEN = [
    dict(id="S1_heme_spin_state_Mb", question="deoxy-heme Fe(II) spin state -> Fe out-of-plane / proximal His",
         dq=(0.34, 0.34), dq_tag="MEASURED 1A6N vs 1A6M Fe-oop(N4) 0.364 vs 0.023 A",
         gap_tau=(3.0, 5.0), s_dft=(5.0, 10.0), s_best=(1.5, 3.0), s_model=(1.5, 3.0),
         AS=(9, 43), bypass="Mossbauer / magnetic susceptibility fix the spin state (S=2) experimentally"),
    dict(id="S2_P450_CpdI_doublet_quartet", question="P450 Cpd I doublet vs quartet",
         dq=(0.0, 0.02), dq_tag="INFERENCE: same Fe=O/porphyrin-radical geometry (spin-coupling isomers)",
         gap_tau=(0.02, 1.0), s_dft=(3.0, 5.0), s_best=(1.0, 2.0), s_model=(1.0, 3.0),
         AS=(43, 58), bypass="EPR/Mossbauer of trapped Cpd I; structure does not depend on it"),
    dict(id="S3_FeMoco_resting_spin_isomers", question="FeMoco resting-state BS7 vs BS8 spin isomer",
         dq=(0.02, 0.05), dq_tag="INFERENCE: broken-symmetry isomers differ by ~0.01-0.05 A Fe-Fe",
         gap_tau=(1.6, 1.6), s_dft=(5.0, 15.0), s_best=(1.0, 5.0), s_model=(1.0, 2.0),
         AS=(70, 76), bypass="Mossbauer/ENDOR constrain Fe1 spin alignment"),
    dict(id="S4_FeMoco_E4_hydride_protonation_isomers", question="FeMoco E4 (Janus) hydride/protonation/belt-S isomer",
         dq=(0.8, 1.5), dq_tag="MEASURED analogues: 4TKV CO replaces S2B (ligand identity); 3MIN/2MIN ligand switch 0.8-1.2 A",
         gap_tau=(3.0, 10.0), s_dft=(10.0, 30.0), s_best=(1.0, 5.0), s_model=(2.0, 4.0),
         AS=(70, 404), bypass="ENDOR (hydride couplings) constrains but does not fix the full isomer"),
    dict(id="S5_Pcluster_redox_ligand_switch", question="P-cluster PN vs POX ligand switch (Ser188 O, Cys88 N)",
         dq=(0.8, 1.2), dq_tag="MEASURED 3MIN vs 2MIN: Fe-OG(Ser b188) 2.80-2.84 -> 1.90-2.07 A; Fe-N(Cys a88) 3.3-3.4 -> 2.15-2.19 A",
         gap_tau=(3.0, 10.0), s_dft=(5.0, 15.0), s_best=(1.0, 3.0), s_model=(2.0, 4.0),
         AS=(67, 73), bypass="crystallography of both redox states (done, 2.03 A)"),
    dict(id="S6_OEC_S2_open_closed_cubane", question="OEC S2 open vs closed cubane (O5 position)",
         dq=(0.8, 1.2), dq_tag="LITERATURE (recalled, UNVERIFIED): O5 shifts ~1 A between Mn1/Mn4 bonding",
         gap_tau=(1.0, 3.0), s_dft=(3.0, 8.0), s_best=(1.0, 3.0), s_model=(1.5, 3.0),
         AS=(35, 44), bypass="EPR g=2 multiline vs g=4.1 signals report the isomer directly"),
    dict(id="S7_Cu2O2_peroxo_vs_bisoxo", question="type-3 Cu2O2: side-on peroxo vs bis(mu-oxo) (Cu-Cu)",
         dq=(0.8, 0.8), dq_tag="MEASURED side-on Cu-Cu 3.59 A (1OXY) vs deoxy 4.61 (1LLA); bis-mu-oxo ~2.8 A (LITERATURE recalled)",
         gap_tau=(3.0, 10.0), s_dft=(5.0, 15.0), s_best=(1.0, 2.0), s_model=(1.5, 3.0),
         AS=(16, 32), bypass="resonance Raman O-O stretch, EXAFS Cu-Cu"),
    dict(id="S8_LBHB_proton_position", question="proton position in short H-bond (KSI Tyr16-Tyr57, PYP Tyr42/Glu46-pCA)",
         dq=(0.1, 0.4), dq_tag="MEASURED O...O 2.49-2.58 A (1OH0, 1NWZ); proton shift between donors 0.1-0.4 A (INFERENCE)",
         gap_tau=(1.0, 3.0), s_dft=(1.0, 3.0), s_best=(0.3, 1.0), s_model=(1.0, 2.0),
         AS=(0, 0), bypass="neutron crystallography; NQE by PIMD is classical-exact (sign-free)"),
]


def eval_scen(sc):
    out = dict(sc)
    res = {}
    for label, pick in (("favourable_to_quantum", lambda r: (r[1], r[0])), ("central", lambda r: (0.5 * (r[0] + r[1]),) * 2)):
        # favourable: large classical solver error, small model error, gap near the worst case
        s_b = pick(sc["s_best"])[0] if label == "central" else sc["s_best"][1]
        s_m = pick(sc["s_model"])[0] if label == "central" else sc["s_model"][0]
        s_d = pick(sc["s_dft"])[0] if label == "central" else sc["s_dft"][1]
        tau = 0.5 * (sc["gap_tau"][0] + sc["gap_tau"][1]) if label == "central" else sc["gap_tau"][0]
        dq = 0.5 * (sc["dq"][0] + sc["dq"][1]) if label == "central" else sc["dq"][1]
        r = {}
        for name, ss in (("dft", s_d), ("best_classical", s_b), ("exact_solver", 0.0)):
            s = math.hypot(ss, s_m)
            r[name] = dict(P_wrong=prior_avg(err_argmin, tau, s), E_struct_err_argmin=dq * prior_avg(err_argmin, tau, s),
                           E_struct_err_boltz=dq * prior_avg(err_boltz, tau, s))
        g, Dst = max_gain_closed_form(s_b, s_m)
        r["VOI_exact_vs_best_A_argmin"] = r["best_classical"]["E_struct_err_argmin"] - r["exact_solver"]["E_struct_err_argmin"]
        r["VOI_exact_vs_best_A_boltz"] = r["best_classical"]["E_struct_err_boltz"] - r["exact_solver"]["E_struct_err_boltz"]
        r["max_dP_any_gap"] = g
        r["max_VOI_A_any_gap"] = g * dq
        r["inputs"] = dict(sigma_best=s_b, sigma_model=s_m, sigma_dft=s_d, tau=tau, dq=dq)
        r["solver_limited_beyond_classical"] = bool(r["VOI_exact_vs_best_A_argmin"] >= 0.05 and
                                                    r["exact_solver"]["E_struct_err_argmin"] <= 0.1 < r["best_classical"]["E_struct_err_argmin"])
        res[label] = r
    out["results"] = res
    return out


# ----------------------------------------------------------------------------------------
# FT cost model, anchored ONLY on numbers verified this session (lit/*.txt):
#  Low et al. 2502.15882 Table (DFTHC+BLISS+SA): Fe2S2-20 3.97e7, Fe4S4-36 1.72e8,
#  FeMoco-54 3.41e8, CPD1-P450X-58 4.91e8, FeMoco-76 9.99e8 Toffolis; FeMoco-76:
#  4.5 M physical qubits, 8.6 h (1 us cycle, 10 us reaction time).
#  Lee et al. 2011.03494 Table III (THC): FeMoco-54 5.3e9, FeMoco-76 3.2e10; ~4 M qubits, < 4 days.
#  Berry et al. 2409.11748: FeMoco incl. MPS state prep + filtering 7.3e10 Toffolis (overlap^2 ~0.9).
#  Kanasugi et al. 2603.22778 (early-FT, STAR): [4Fe-4S]-36o 1.6e5 phys. qubits, 42-49 days single QPU;
#  P450 Cpd I (43o) 2.24e5 qubits, 84 days single QPU.
#  Classical (Zhai et al. 2601.04621): FeMoco-76 UCCSDTQ composite 4.0e4 core-h; UDMRG D=18k 2.77e6 core-h;
#  ideal-Frontier D=393k variational DMRG 22.9 h.  Goings 2202.01244: P450 X (58o) DMRG M=3000 est. 36,564 CPU-h.
# ----------------------------------------------------------------------------------------
SA_PTS = [(20, 3.97e7), (36, 1.72e8), (54, 3.41e8), (58, 4.91e8), (76, 9.99e8)]
SA_RATE = 9.99e8 / (8.6 * 3600)  # Toffoli / s implied by the FeMoco-76 estimate


def ft_model():
    n = np.log([p[0] for p in SA_PTS])
    t = np.log([p[1] for p in SA_PTS])
    alpha, logc = np.polyfit(n, t, 1)
    resid = t - (alpha * n + logc)

    def toff(N, a=alpha):
        return float(np.exp(logc) * N ** a) if a == alpha else float(9.99e8 * (N / 76.0) ** a)

    sites = {"Cu2O2 (AS_dp 16)": 16, "[2Fe-2S] (20)": 20, "[4Fe-4S] (32-36)": 36, "OEC Mn4CaO5 (35-44)": 44,
             "P450 Cpd I (58)": 58, "H-cluster 6Fe (54)": 54, "P-cluster (67-73)": 73, "FeMoco (70-76)": 76,
             "FeMoco + dynamic corr. (404o, as in 2601.04621)": 404}
    tab = {}
    for k, N in sites.items():
        lo = toff(N, 2.4) if N > 76 else toff(N)
        hi = toff(N, 2.7) if N > 76 else toff(N)
        tab[k] = dict(N_orb=N, toffoli_SA=(lo, hi), hours_per_energy_SA=(lo / SA_RATE / 3600, hi / SA_RATE / 3600),
                      toffoli_THC_like=toff(N) * 32.0, note="THC-like = x32 (FeMoco-76: 3.2e10 / 9.99e8)")
    # structural-question multiplicity (INFERENCE; see README)
    E4 = dict(n_isomers=(10, 50), n_spin_families=(3, 10), n_env=(1, 10))
    per = tab["FeMoco (70-76)"]["hours_per_energy_SA"][0]
    per404 = tab["FeMoco + dynamic corr. (404o, as in 2601.04621)"]["hours_per_energy_SA"]
    e4 = dict(
        energies=(E4["n_isomers"][0] * E4["n_spin_families"][0] * E4["n_env"][0],
                  E4["n_isomers"][1] * E4["n_spin_families"][1] * E4["n_env"][1]),
    )
    e4["QPU_days_76o_SA_perfect_overlap"] = (e4["energies"][0] * per / 24, e4["energies"][1] * per / 24)
    e4["QPU_days_76o_with_state_prep_x2.3"] = (2.3 * e4["QPU_days_76o_SA_perfect_overlap"][0], 2.3 * e4["QPU_days_76o_SA_perfect_overlap"][1])
    e4["QPU_days_404o_SA"] = (e4["energies"][0] * per404[0] / 24, e4["energies"][1] * per404[1] / 24)
    # classical per-energy costs at FeMoco-76 (verified) and break-even price ratio rho*
    cls = dict(UCCSDTQ_composite_core_h=4.0e4, UDMRG_D18k_core_h=2.768994e6)
    rho = {k: v * 3600 / (per * 3600) for k, v in cls.items()}  # core-seconds per QPU-second at parity
    return dict(alpha_fit=float(alpha), fit_resid_max=float(np.abs(resid).max()), SA_rate_toffoli_per_s=SA_RATE,
                sites=tab, E4_question=e4, classical_femoco76=cls, rho_star_core_equiv_per_QPU=rho)


def nqe_exchange():
    """Thermal de Broglie wavelength and exchange factor exp(-2 pi d^2/lambda^2) for H/D at 300 K."""
    h, kB, amu = 6.62607015e-34, 1.380649e-23, 1.66053907e-27
    out = {}
    for iso, m in (("H", 1.00784), ("D", 2.01410)):
        lam = h / math.sqrt(2 * math.pi * m * amu * kB * 300.0) * 1e10
        out[iso] = dict(lambda_th_A=lam, exchange_factor={f"{d}A": math.exp(-2 * math.pi * d * d / lam / lam) for d in (1.5, 2.0, 2.5)})
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    res = dict(kT_kcal=KT, grid=grid(), scenarios=[eval_scen(s) for s in SCEN], ft=ft_model(), nqe=nqe_exchange(),
               closed_form_examples={f"s_s/s_m={r}": max_gain_closed_form(r, 1.0)[0] for r in (0.25, 0.5, 1.0, 2.0, 5.0)})
    p = os.path.join(OUT, "decision_value.json")
    with open(p + ".tmp", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1)
    os.replace(p + ".tmp", p)
    print("closed-form max dP (exact vs best) by s_s/s_m:", {k: round(v, 3) for k, v in res["closed_form_examples"].items()})
    for s in res["scenarios"]:
        for lab in ("favourable_to_quantum", "central"):
            r = s["results"][lab]
            print(f"{s['id']:<42} {lab:<22} Pw dft/best/exact = {r['dft']['P_wrong']:.3f}/{r['best_classical']['P_wrong']:.3f}/{r['exact_solver']['P_wrong']:.3f}  "
                  f"Err(A) best/exact = {r['best_classical']['E_struct_err_argmin']:.3f}/{r['exact_solver']['E_struct_err_argmin']:.3f}  "
                  f"VOI={r['VOI_exact_vs_best_A_argmin']:.3f} (boltz {r['VOI_exact_vs_best_A_boltz']:.3f}) maxVOI={r['max_VOI_A_any_gap']:.3f} SL={r['solver_limited_beyond_classical']}")
    ft = res["ft"]
    print("FT alpha fit", round(ft["alpha_fit"], 3), "max resid", round(ft["fit_resid_max"], 3), "rate", round(ft["SA_rate_toffoli_per_s"]))
    for k, v in ft["sites"].items():
        print(f"  {k:<48} N={v['N_orb']:<4} Toff={v['toffoli_SA'][0]:.2e}-{v['toffoli_SA'][1]:.2e}  h/energy={v['hours_per_energy_SA'][0]:.2f}-{v['hours_per_energy_SA'][1]:.2f}")
    print("E4:", {k: v for k, v in ft["E4_question"].items()})
    print("rho*:", ft["rho_star_core_equiv_per_QPU"])
    print("NQE:", res["nqe"])


if __name__ == "__main__":
    main()
