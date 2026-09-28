"""Error/resource budget: can a programmable analog dipolar simulator reproduce the protein-derived echo F_ab(t)
to sigma = 0.01 at t = 40-120 us (protein time) for N = 20-100 spins?

Combines (i) MEASURED sensitivities of F to each error channel (sens_*.json via sens_summary.json; exact, N = 10/12[/14]),
(ii) MEASURED Floquet-composite errors (floquet_*.json: cycle-time error, pulse-error bias, C3-ratio miscalibration),
(iii) platform parameters, each tagged LIT (verified this session), INF (inference) or REQ (back-solved requirement).

Key scaling (DERIVED): the number of Floquet cycles per leg is platform-independent,
    n_c = J_m t / (2 pi x*),  J_m = median per-spin sum_j |g_ij|,  x* = cycle parameter meeting the Magnus-error budget,
so every per-cycle error (pulse, swap, decay, motion) is multiplied by the same n_c; the simulated duration is
T_sim = 2 n_c t_c,min, and the geometric scale follows from J_m^sim = 2 pi x*/t_c,min and C3.
Writes budget.json.  Pure arithmetic on files already on disk (< 1 CPU-s).
"""
import json
import math
import os

import numpy as np

import ed_echo as EE

HERE = os.path.dirname(os.path.abspath(__file__))
SIGMA = 0.01
TIMES = [40.0, 80.0, 120.0]
PROBES = [19, 245]
NSIM = [20, 50, 100]
EVENTS_PER_CYCLE = 6          # 4 frame pulses + 2 encoding swaps (floquet_composite.py cycle)


def jm_prot(probe, N):
    dm, bs, xyz, b0 = EE.load("1UBQ", probe, N)
    return float(np.median(np.abs(dm).sum(1)))           # rad/s


def floor_est(H, N):
    return (1.0 - H) / N


def load_floquet():
    out = {}
    for p in PROBES:
        d = json.load(open(os.path.join(HERE, f"floquet_1UBQ_p{p}_N8.json")))
        ex = d["exact"]
        det = {}
        for x in (0.2, 0.1, 0.05, 0.025):
            for kerr in (0.0, 0.01, 0.03):
                u = d["units"].get(f"x{x}|k{kerr}|d0.0|s0")
                if u:
                    det[f"x{x}|k{kerr}"] = max(abs(u["res"][t][b][0] - ex[t][b]) for t in ex for b in ex[t])
        pulse = {}
        for dth in (0.003, 0.01, 0.03, 0.06):
            us = [d["units"].get(f"x0.05|k0.0|d{dth}|s{s}") for s in range(8)]
            us = [u for u in us if u]
            if not us:
                continue
            rows = {}
            for t in ex:
                ncyc = us[0]["ncyc_per_leg"][t]
                for b in ex[t]:
                    S = np.mean([u["res"][t][b][0] for u in us]); R = np.mean([u["res"][t][b][1] for u in us])
                    rows[f"{t}|{b}"] = dict(bias_raw=float(S - ex[t][b]), bias_norm=float(S / R - ex[t][b]),
                                            n_events=2 * ncyc * EVENTS_PER_CYCLE)
            pulse[str(dth)] = rows
        out[p] = dict(det=det, pulse=pulse, Jm_native=d["Jm_native_rad_s"])
    return out


def main():
    ss = json.load(open(os.path.join(HERE, "sens_summary.json")))
    fl = load_floquet()
    res = dict(sigma=SIGMA, notes=[], inputs={}, scenarios={}, requirements={})

    # ---------------------------------------------------------------- measured sensitivities (N = 12, worst probe)
    tolN12 = {}
    for ch in ("iid_shared", "iid_indep", "pos_shared", "pos_indep", "scale", "heis_rev", "heis_nonrev",
               "onsite_nonrev"):
        vals = [ss[f"1UBQ_p{p}_N12"]["channels"][ch]["eps_star_rms"] for p in PROBES]
        tolN12[ch] = dict(eps_star_rms_by_probe=vals, eps_star_rms_worst=min(vals),
                          eps_star_rms_N10=[ss[f"1UBQ_p{p}_N10"]["channels"][ch]["eps_star_rms"] for p in PROBES])
    res["inputs"]["tolerances_MEASURED"] = tolN12

    # delete_j: signed sum over j of dF_j (atom missing for the whole sequence), per (b, t), N = 12
    leak = {}
    for p in PROBES:
        d = json.load(open(os.path.join(HERE, f"sens_1UBQ_p{p}_N12.json")))
        F0 = d["baseline"]["F"]
        sums = {}
        for b in F0:
            s = np.zeros(len(d["times_us"]))
            for key, u in d["units"].items():
                if key.startswith("delete_j|"):
                    s += np.array(u["S"][b]) - np.array(F0[b])
            sums[b] = s.tolist()
        leak[p] = dict(signed_sum=sums, max_abs_signed_sum=float(max(np.abs(v).max() for v in sums.values())),
                       F0=F0, H=d["baseline"]["H"], times=d["times_us"])
    res["inputs"]["missing_atom_sum_MEASURED_N12"] = {p: dict(max_abs_signed_sum=leak[p]["max_abs_signed_sum"])
                                                      for p in PROBES}

    # pulse-error accumulation coefficient beta: bias_norm ~ beta * n_events * dtheta^2 (fit at dtheta = 0.01)
    betas = []
    for p in PROBES:
        for key, r in fl[p]["pulse"].get("0.01", {}).items():
            betas.append(abs(r["bias_norm"]) / (r["n_events"] * 0.01 ** 2))
    beta = float(max(betas))
    res["inputs"]["floquet_MEASURED_N8"] = {p: dict(det=fl[p]["det"]) for p in PROBES}
    res["inputs"]["pulse_beta_MEASURED"] = dict(beta_max=beta, beta_median=float(np.median(betas)),
                                               form="bias_norm ~ beta * n_events * dtheta^2 (N = 8, x = 0.05)")
    xstar = 0.05
    res["inputs"]["x_star"] = dict(value=xstar, basis="MEASURED: deterministic Magnus error at x = 0.05 is "
                                   "0.0016-0.0048 (N = 8) and 0.0026 (N = 10, p19); x = 0.1 gives 0.005-0.019")

    # ---------------------------------------------------------------- geometry / time scale
    C3 = 3.2e9          # Hz um^3, 61S-61P (LIT: Geier et al. 2402.13873)
    jm = {p: {N: jm_prot(p, N) for N in NSIM} for p in PROBES}
    res["inputs"]["Jm_prot_Hz"] = {p: {N: jm[p][N] / (2 * math.pi) for N in NSIM} for p in PROBES}
    rmin_A = 1.62       # smallest H-H distance in the N = 100 clusters (MEASURED from PDB clusters, 1.62-1.66 A)
    kc = 1.1
    c = (1 + kc) / (2 * kc)

    scen = {
        "S0_demonstrated": dict(
            tc_min_us=0.7, tc_tag="INF from LIT: Scholl 2107.14459 t_c = 0.3 us for 4 pi/2 pulses (Omega/2pi = 7 MHz, "
                                 "finite-pulse errors already significant); +2 swaps of 2 pi-transfers at Omega/2pi = 9-11 MHz "
                                 "(Geier 2402.13873) ~ 0.1 us each",
            dtheta=0.06, dtheta_tag="LIT: Scholl 2107.14459 App. A, 0.06 +- 0.01 rad per pulse",
            kcal=0.03, kcal_tag="INF: k theory 1.1 vs measured 1.03 (LIT Geier); assume calibrated to 3%",
            swap_leak=0.02, swap_leak_tag="INF: Geier revival bounded by transfer efficiency (no number given)",
            prep_loss=0.05, prep_tag="LIT: Scholl, STIRAP efficiency ~95%",
            tau_us=105.0, tau_tag="LIT formula: Beterov 0810.0339 Eq.16, Rb 61S, 300 K",
            v_um_per_us=0.05, v_tag="LIT: Geier 2402.13873, ~50 nm per us (gas); INF for tweezers at 10-20 uK",
            pos_cal_um=0.1, pos_cal_tag="UNPROVEN: 3D holographic trap placement accuracy not verified",
            spam_rel=0.01, spam_tag="INF: residual after S/R and t = 0 normalisation (raw: 5%/3.5% detection, LIT Scholl)",
            n3d=72, n3d_tag="LIT: Barredo 1712.02727, 72 atoms in arbitrary 3D"),
        "S1_optimistic_near_term": dict(
            tc_min_us=0.1, tc_tag="INF: Omega/2pi ~ 50 MHz microwaves, duty <= 20%",
            dtheta=0.005, dtheta_tag="INF: 12x better than Scholl 2022",
            kcal=0.005, kcal_tag="INF",
            swap_leak=1e-3, swap_leak_tag="INF",
            prep_loss=0.005, prep_tag="INF",
            tau_us=450.0, tau_tag="LIT formula (Beterov Eq.16): Rb 61P at 4 K (cryogenic)",
            v_um_per_us=0.01, v_tag="INF: ~1 uK (Raman-sideband cooled)",
            pos_cal_um=0.03, pos_cal_tag="INF",
            spam_rel=0.003, spam_tag="INF",
            n3d=300, n3d_tag="INF (no verified 3D array beyond 72)"),
    }
    s1b = dict(scen["S1_optimistic_near_term"])
    s1b.update(route="native", route_tag="UNPROVEN: native traceless dipolar coupling (Delta m = +-1 encoding plus "
               "DC-Stark permanent dipoles, J_z/J_xy = -2) so that no encoding swaps are needed; reversal by a "
               "magic-echo-type -H/2 Floquet leg; not demonstrated on any programmable-geometry platform",
               swap_leak=0.0)
    scen["S1b_optimistic_native_traceless"] = s1b

    for name, P in scen.items():
        rows = []
        for p in PROBES:
            L = leak[p]
            for N in NSIM:
                Jm_nat = c * jm[p][N]                                    # rad/s (native per-spin sum, composite)
                Jsim = 2 * math.pi * xstar / (P["tc_min_us"] * 1e-6)     # rad/s
                kappa = Jsim / Jm_nat
                s_um_per_A = (C3 / (kappa * c * 120.1e3)) ** (1 / 3)
                rmin_um = rmin_A * s_um_per_A
                for it, t in enumerate(TIMES):
                    nc = Jm_nat * t * 1e-6 / (2 * math.pi * xstar)
                    n_ev = 2 * nc * EVENTS_PER_CYCLE
                    Tsim = 2 * nc * P["tc_min_us"]                          # us
                    # per-channel predicted errors on F (absolute)
                    route = P.get("route", "composite")
                    if route == "native":          # forward leg native (no pulses), reverse leg -H/2 Floquet (2x longer)
                        n_ev = 2 * nc * 4
                        Tsim = 3 * nc * P["tc_min_us"]
                        n_swaps = 0
                    else:
                        n_swaps = 2 * nc * 2
                    e_pulse = min(1.0, beta * n_ev * P["dtheta"] ** 2)
                    p_mid = min(1.0, Tsim / P["tau_us"] + n_swaps * P["swap_leak"])     # loss at a random time
                    p_leak = min(1.0, p_mid + P["prep_loss"])
                    p_eff = P["prep_loss"] + 0.5 * p_mid
                    Fmax = max(v[it] for v in L["F0"].values())
                    # p_eff already carries the 0.5 random-time weight; per site b: deleted-spin sum + butterfly-atom loss
                    coef = max(abs(L["signed_sum"][b][it] + (1 - L["F0"][b][it])) for b in L["F0"])
                    e_leak = min(1.0, p_eff * coef)
                    motion = P["v_um_per_us"] * (Tsim / 2) / math.sqrt(2) / rmin_um    # pos_indep-equivalent level
                    tolm = tolN12["pos_indep"]["eps_star_rms_worst"]
                    e_motion = min(1.0, SIGMA * (motion / tolm) ** 1.16)        # MEASURED slope ~1.16 (pos_indep)
                    posc = P["pos_cal_um"] / rmin_um
                    tolp = tolN12["pos_shared"]["eps_star_rms_worst"]
                    e_pos = min(1.0, SIGMA * (posc / tolp))
                    e_k = 0.003 if P["kcal"] <= 0.01 else 0.028 * (P["kcal"] / 0.03)   # MEASURED N = 8 (kerr 0.01/0.03)
                    e_mag = 0.0048                                              # MEASURED x = 0.05 (N = 8 worst)
                    e_spam = P["spam_rel"] * Fmax
                    H = L["H"][it]
                    e_floor = floor_est(H, N)                                    # finite-cluster floor (needs classical H)
                    terms = dict(pulse=e_pulse, leak_decay=e_leak, motion=e_motion, pos_cal=e_pos, k_cal=e_k,
                                 magnus=e_mag, spam=e_spam)
                    tot_lin = min(1.0, sum(terms.values()))
                    tot_q = min(1.0, math.sqrt(sum(v ** 2 for v in terms.values())))
                    rows.append(
                                dict(probe=p, N=N, t_us=t, kappa=kappa, scale_um_per_A=s_um_per_A, rmin_um=rmin_um,
                                     n_cycles_per_leg=nc, n_events=n_ev, T_sim_us=Tsim, p_leak=p_leak,
                                     motion_rel=motion, poscal_rel=posc, terms=terms, total_linear=tot_lin,
                                     total_quadrature=tot_q, total_over_sigma=tot_q / SIGMA,
                                     finite_cluster_floor=e_floor, fits_3d_demonstrated=N <= P["n3d"]))
        res["scenarios"][name] = dict(params=P, rows=rows,
                                      min_total_over_sigma=min(r["total_over_sigma"] for r in rows),
                                      max_total_over_sigma=max(r["total_over_sigma"] for r in rows))

    # ---------------------------------------------------------------- requirements (each channel <= sigma/sqrt(7))
    alloc = SIGMA / math.sqrt(7)
    req = {}
    for p in PROBES:
        L = leak[p]
        for N in (50, 100):
            for t in (40.0, 120.0):
                it = TIMES.index(t)
                Jm_nat = c * jm[p][N]
                nc = Jm_nat * t * 1e-6 / (2 * math.pi * xstar)
                coef = max(abs(L["signed_sum"][b][it] + (1 - L["F0"][b][it])) for b in L["F0"])
                p_eff_req = alloc / coef                     # prep_loss + 0.5 * mid-sequence loss, per atom per shot
                for route, n_ev, Tfac, nsw in (("composite", 2 * nc * EVENTS_PER_CYCLE, 2 * nc, 4 * nc),
                                               ("native", 2 * nc * 4, 3 * nc, 0)):
                    dth_req = math.sqrt(alloc / (beta * n_ev))
                    # split the loss allocation equally between prep, decay and (if any) swaps
                    parts = 3 if nsw else 2
                    prep_req = p_eff_req / parts
                    decay_req = 2 * p_eff_req / parts                 # T_sim/tau (mid-sequence, weight 0.5)
                    swap_req = (2 * p_eff_req / parts) / nsw if nsw else None
                    req[f"p{p}_N{N}_t{int(t)}_{route}"] = dict(
                        n_cycles_per_leg=nc, n_events=n_ev, loss_coef=coef, p_eff_req=p_eff_req,
                        dtheta_req_rad=dth_req, prep_loss_req=prep_req, Tsim_over_tau_req=decay_req,
                        swap_leak_req=swap_req,
                        tc_min_req_ns_300K=1e3 * decay_req * 105.0 / Tfac,
                        tc_min_req_ns_4K=1e3 * decay_req * 450.0 / Tfac,
                        pos_static_req_rel=tolN12["pos_shared"]["eps_star_rms_worst"] / math.sqrt(7),
                        motion_req_rel=tolN12["pos_indep"]["eps_star_rms_worst"] / math.sqrt(7),
                        kcal_req="<= 0.01 (MEASURED: 0.01 -> 0.003; 0.03 -> 0.013-0.028)")
    res["requirements"] = req
    res["notes"] = [
        "Errors from different channels are combined in quadrature (optimistic) and linearly (conservative).",
        "Pulse-error accumulation fitted at N = 8 (bias_norm ~ beta n_ev dtheta^2) and extrapolated in n_events; "
        "valid only while the result is << 1 [INFERENCE].",
        "Missing/decayed-atom bias uses the N = 12 signed sum over deleted spins (7 spins) as a LOWER bound for larger "
        "clusters and a factor 0.5 for decay at a uniformly random time [INFERENCE].",
        "Motion is modelled as the pos_indep channel with displacement v*T_sim/2 between legs [INFERENCE].",
        "The finite-cluster floor (1-H)/N is listed separately: it is b-independent and needs a classical H estimate "
        "to subtract, exactly as for the classical finite-cluster route.",
    ]
    json.dump(res, open(os.path.join(HERE, "budget.json"), "w"), indent=1, default=float)
    for name, sc in res["scenarios"].items():
        print("==", name, "total/sigma range %.1f .. %.1f" % (sc["min_total_over_sigma"], sc["max_total_over_sigma"]))
        for r in sc["rows"]:
            if r["t_us"] in (40.0, 120.0) and r["N"] in (20, 100):
                print("  p%d N=%d t=%d nc=%.0f Tsim=%.1fus rmin=%.0fum pleak=%.2f motion=%.4f | %s | tot/sig=%.1f floor=%.4f" % (
                    r["probe"], r["N"], r["t_us"], r["n_cycles_per_leg"], r["T_sim_us"], r["rmin_um"], r["p_leak"],
                    r["motion_rel"], " ".join("%s=%.3f" % (k, v) for k, v in r["terms"].items()),
                    r["total_over_sigma"], r["finite_cluster_floor"]))
    for k, v in req.items():
        print("REQ", k, {kk: (round(vv, 6) if isinstance(vv, float) else vv) for kk, vv in v.items()})


if __name__ == "__main__":
    main()
