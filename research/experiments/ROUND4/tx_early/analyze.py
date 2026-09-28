"""T-X-early analysis -> tx_early_summary.json.  Reads only files on disk (no dynamics).

Sources per (probe p, time t, site b):
  N = 22  F, X (plain F-H-floor), Xdirect           : runs/1UBQ_p*_N22_echo_R1_complex64_s4242_t20-40-60.json (t = 40 us)
          H_22, floor_22 (all t)                     : runs/1UBQ_p*_N22_honly_R1_complex64_s4242_t20-40-60.json
  N = 20  F, X, Xdirect (R = 2)                      : runs/1UBQ_p*_N20_echo_R2_complex64_s4242_t20-40-60.json (t = 40 us)
          mixed X_20 (all t where available)         : reference F_20 checkpoint (typicality_cone) - VC honly H_20/floor_20
  N <= 18 reference F (typicality_cone), VC honly H/floor (ROUND3 verify_classical)
  CSD     runs/csdcrn_1UBQ_p*_Nbig80_q22_B48x1000_s616.json.ckpt.json (48k trajectories, CV + CRN)
Pre-registered rule (PREREG Round 4, operationalised in README section 0).
"""
import glob
import json
import math
import os

import numpy as np

import csd_stats as CS

HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.abspath(os.path.join(HERE, "..", ".."))
TC = os.path.join(EXP, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
VC = os.path.join(EXP, "ROUND3", "r1sim_exact_reach", "verify_classical", "runs")
SIG = 0.01
TOL = 0.005
TIMES = [40, 80, 120]
SITES = ["1", "7", "8", "9"]


def J(p):
    with open(p) as f:
        return json.load(f)


def vc_H(p, N):
    d = J(glob.glob(os.path.join(VC, f"1UBQ_p{p}_N{N}_probe_honly_*.json"))[0])
    return np.array(d["H"][:3]), np.array(d["floor"][:3])


def main():
    S = dict(sigma=SIG, tol_dX=TOL, times_us=TIMES, sites=SITES, cells={}, per_probe={})
    for p in (19, 245):
        n22 = J(os.path.join(HERE, "runs", f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
        h22 = J(os.path.join(HERE, "runs", f"1UBQ_p{p}_N22_honly_R1_complex64_s4242_t20-40-60.json"))
        n20 = J(os.path.join(HERE, "runs", f"1UBQ_p{p}_N20_echo_R2_complex64_s4242_t20-40-60.json"))
        ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json")) for N in (12, 14, 16, 18)}
        ref20 = J(os.path.join(TC, f"1UBQ_p{p}_N20.json.ckpt.json"))["done"]
        H18, f18 = vc_H(p, 18)
        H20v, f20v = vc_H(p, 20)
        cs = CS.stats(os.path.join(HERE, "runs", f"csdcrn_1UBQ_p{p}_Nbig80_q22_B48x1000_s616.json.ckpt.json"), 1000, True)
        csp = CS.stats(os.path.join(HERE, "runs", f"csdcrn_1UBQ_p{p}_Nbig80_q22_B48x1000_s616.json.ckpt.json"), 1000, False)
        # CSD record times 0, 40, 80, 120 -> index 1..3
        H22x = np.array(h22["H"]); fl22 = np.array(h22["floor"])
        H22csd = np.array(cs["H_22"][1:]); seH22csd = np.array(cs["se_H_22"][1:])
        H80 = np.array(cs["H_80"][1:]); seH80 = np.array(cs["se_H_80"][1:])
        D = np.array(cs["D_80_22"][1:]); seD = np.array(cs["se_D_80_22"][1:])
        # typicality noise of exact H_22 (empirical: |honly - echo| at 40 us, floor at 5e-4)
        seH22x = max(5e-4, abs(n22["H"][0] - H22x[0]))
        offset = H22x - H22csd
        H_inf = H22x + D
        se_H = np.sqrt(seD ** 2 + seH22x ** 2)
        # verifier-style alternative: independent CSD runs (existing Nc >= 80 + this lane's H_80) + offset at 22
        indep = [(H80, seH80)]
        for f in glob.glob(os.path.join(VC, f"csd_1UBQ_p{p}_Nc*_M*_h1.0.json")):
            d = J(f)
            if d["Nc"] >= 80 and "custom" not in f:
                indep.append((np.array(d["H_unbiased"])[1:4], np.array(d["H_se_est"])[1:4]))
        w = np.array([1 / s ** 2 for _, s in indep])
        Hbig_v = np.sum([h / s ** 2 for h, s in indep], axis=0) / w.sum(0)
        seHbig_v = 1 / np.sqrt(w.sum(0))
        H_inf_v = Hbig_v + offset
        se_H_v = np.sqrt(seHbig_v ** 2 + seH22csd ** 2)
        B0 = np.sqrt(se_H ** 2 + offset ** 2)
        S["per_probe"][f"p{p}"] = dict(
            H22_exact=H22x.tolist(), floor22_exact=fl22.tolist(), H22_echo_40us=n22["H"][0], se_H22_exact=seH22x,
            H20_R2_40us=n20["H"][0], floor20_R2_40us=n20["floor"][0], H22_csd=H22csd.tolist(), se_H22_csd=seH22csd.tolist(),
            H80_csd=H80.tolist(), se_H80_csd=seH80.tolist(), D_80_22_crn=D.tolist(), se_D=seD.tolist(),
            offset_exact_minus_csd_22=offset.tolist(), H_inf=H_inf.tolist(), se_H=se_H.tolist(),
            H_inf_verifier_style=H_inf_v.tolist(), se_H_inf_verifier_style=se_H_v.tolist(),
            n_indep_csd_runs=len(indep), budget_without_dX=B0.tolist(),
            max_dX_allowed_by_budget=[float(math.sqrt(max(SIG ** 2 - b ** 2, 0))) for b in B0],
            csd_M=cs["M"], csd_cpu_s=cs["cpu_s"], csd_plain_se_H80=csp["se_H_80"][1:])
        for ti, t in enumerate(TIMES):
            st = 20 * (ti + 1)
            for b in SITES:
                c = dict(probe=p, t_us=t, site=int(b))
                Fl = {N: ref[N]["F"][b][ti + 1] for N in (12, 14, 16, 18)}
                if str(st) in ref20:
                    c["F20_ref"] = ref20[str(st)][b]
                    c["X20_mixed"] = ref20[str(st)][b] - H20v[ti] - f20v[ti]
                c["X18_mixed"] = Fl[18] - H18[ti] - f18[ti]
                c["F_ladder_ref"] = Fl
                c["H_inf"] = float(H_inf[ti]); c["se_H"] = float(se_H[ti]); c["offset"] = float(offset[ti])
                c["budget_without_dX"] = float(B0[ti])
                if ti == 0:
                    X22 = n22["X"][b][0]; X20 = n20["X"][b][0]
                    Xd22 = n22["Xdirect"][b][0]; Xd20 = n20["Xdirect"][b][0]
                    F22 = n22["F"][b][0]; F20 = n20["F"][b][0]
                    dX = X22 - X20
                    budget = math.sqrt(se_H[ti] ** 2 + offset[ti] ** 2 + dX ** 2)
                    # typicality noise of dX: per-vector spread at N = 20 (R = 2) and 0.84 * 2^-N/2 scaling (validated N = 12)
                    xr = np.array(n20["Xdirect_r"])[:, 0, n20["bs"].index(int(b))]
                    noise = math.sqrt((0.84 * 2 ** -11) ** 2 + ((0.84 * 2 ** -10) / math.sqrt(2)) ** 2)
                    Ns = [16, 18, 20, 22]
                    Fs = [Fl[16], Fl[18], F20, F22]
                    A = np.vstack([np.ones(4), 1.0 / np.array(Ns, float)]).T
                    coef, *_ = np.linalg.lstsq(A, np.array(Fs), rcond=None)
                    c.update(F22=F22, F20=F20, dF_22_20=F22 - F20, X22=X22, X20=X20, dX=dX, Xdirect22=Xd22,
                             Xdirect20=Xd20, dXdirect=Xd22 - Xd20, X20_vector_spread=float(abs(xr[0] - xr[1])),
                             dX_noise_est=noise, budget=budget,
                             pass_dX=bool(abs(dX) <= TOL), pass_budget=bool(budget <= SIG),
                             pass_cell=bool(abs(dX) <= TOL and budget <= SIG),
                             pass_dX_noise_robust=bool(abs(dX) - 2 * noise <= TOL),
                             F_inf_hybrid=float(H_inf[ti] + X22), F_inf_hybrid_err=budget,
                             F_inf_hybrid_minus_F22=float(H_inf[ti] + X22 - F22),
                             F_ladder_16_22=dict(zip(Ns, Fs)), max_abs_F_N_minus_F22_16to20=float(max(abs(f - F22) for f in Fs[:3])),
                             F_inf_invN_fit_16_22=float(coef[0]), invN_c=float(coef[1]),
                             invN_rms=float(np.sqrt(np.mean((A @ coef - Fs) ** 2))),
                             H_plus_floor_drift_22_20=float((n22["H"][0] + n22["floor"][0]) - (n20["H"][0] + n20["floor"][0])))
                else:
                    c.update(measured_N22_F=False, note="F_22 not computed at this time (CPU budget); rule cell undetermined")
                    if "X20_mixed" in c:
                        c["dX_20_18_mixed"] = c["X20_mixed"] - c["X18_mixed"]
                        c["dF_20_18"] = c["F20_ref"] - Fl[18]
                S["cells"][f"p{p}_t{t}_b{b}"] = c
    # rule evaluation (README section 0)
    series = {}
    for p in (19, 245):
        for b in SITES:
            cells = [S["cells"][f"p{p}_t{t}_b{b}"] for t in TIMES]
            if any(c.get("pass_cell") is False for c in cells):
                series[f"p{p}_b{b}"] = "FAIL"
            elif all(c.get("pass_cell") is True for c in cells):
                series[f"p{p}_b{b}"] = "PASS"
            else:
                series[f"p{p}_b{b}"] = "PASS_AT_40us_ONLY(80/120 undetermined)"
    n_fail = sum(v == "FAIL" for v in series.values())
    n_pass = sum(v == "PASS" for v in series.values())
    n_undet = 8 - n_fail - n_pass
    per_time_40 = sum(S["cells"][f"p{p}_t40_b{b}"]["pass_cell"] for p in (19, 245) for b in SITES)
    S["rule"] = dict(
        series=series, n_pass_all_times=n_pass, n_fail=n_fail, n_undetermined=n_undet,
        kill_possible_if_undetermined_pass=bool(n_pass + n_undet >= 6), kill_fired=bool(n_pass >= 6),
        outcome="KILL" if n_pass >= 6 else "KEEP OPEN",
        reason=("strict reading: >= 6/8 series must pass at 40, 80 and 120 us; 80/120 us not measured at N = 22, so the "
                "KILL condition cannot be demonstrated -> KEEP OPEN (rule's else-branch)"),
        per_time_40us_pass=f"{per_time_40}/8",
        supports_criterion=("X drift >= 0.01 on >= 2 series per probe: " +
                            str({p: sum(abs(S['cells'][f'p{p}_t40_b{b}']['dX']) >= 0.01 for b in SITES) for p in (19, 245)})))
    with open(os.path.join(HERE, "tx_early_summary.json.tmp"), "w") as f:
        json.dump(S, f, indent=1)
    os.replace(os.path.join(HERE, "tx_early_summary.json.tmp"), os.path.join(HERE, "tx_early_summary.json"))
    # console table
    for p in (19, 245):
        pp = S["per_probe"][f"p{p}"]
        print(f"== p{p}: H22 {np.round(pp['H22_exact'], 4)} floor22 {np.round(pp['floor22_exact'], 4)} "
              f"H22csd {np.round(pp['H22_csd'], 4)} D {np.round(pp['D_80_22_crn'], 4)}+-{np.round(pp['se_D'], 4)}")
        print(f"   H_inf {np.round(pp['H_inf'], 4)} se {np.round(pp['se_H'], 4)} offset {np.round(pp['offset_exact_minus_csd_22'], 4)} "
              f"B0 {np.round(pp['budget_without_dX'], 4)} maxdX {np.round(pp['max_dX_allowed_by_budget'], 4)} "
              f"H_inf(verifier) {np.round(pp['H_inf_verifier_style'], 4)}")
        for b in SITES:
            c = S["cells"][f"p{p}_t40_b{b}"]
            print(f"   40us b{b}: F16-22 {[round(v, 4) for v in c['F_ladder_16_22'].values()]} dF {c['dF_22_20']:+.4f} | "
                  f"X20 {c['X20']:.4f} X22 {c['X22']:.4f} dX {c['dX']:+.4f} (direct {c['dXdirect']:+.4f}) budget {c['budget']:.4f} "
                  f"pass {c['pass_cell']} | F_inf hyb {c['F_inf_hybrid']:.4f} (-F22 {c['F_inf_hybrid_minus_F22']:+.4f}) "
                  f"F_inf 1/N {c['F_inf_invN_fit_16_22']:.4f}")
        for t in (80, 120):
            for b in SITES:
                c = S["cells"][f"p{p}_t{t}_b{b}"]
                print(f"   {t}us b{b}: F14-18 {[round(c['F_ladder_ref'][N], 4) for N in (14, 16, 18)]} F20ref {c.get('F20_ref', float('nan')):.4f} "
                      f"dX(18->20,mixed) {c.get('dX_20_18_mixed', float('nan')):+.4f} B0 {c['budget_without_dX']:.4f}")
    print(json.dumps(S["rule"], indent=1))


if __name__ == "__main__":
    main()
