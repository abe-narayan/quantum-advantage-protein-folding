"""Verifier: independent re-derivation of the tx_early headline numbers from the raw run files (no dynamics).

Reads only: tx_early/runs/*.json (N = 20 / 22 echo + honly), the reference typicality cone (N = 12..20) and the ROUND3
verify_classical honly H/floor ladders.  Writes recheck_numbers.json next to this script.  Does not import the lane's
analysis code (analyze.py / backtest.py), so a bug there would show up as a mismatch here.
"""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
EXP = os.path.abspath(os.path.join(LANE, "..", ".."))
TC = os.path.join(EXP, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
VC = os.path.join(EXP, "ROUND3", "r1sim_exact_reach", "verify_classical", "runs")
SITES = ["1", "7", "8", "9"]


def J(p):
    with open(p) as f:
        return json.load(f)


def vc(p, N):
    d = J(glob.glob(os.path.join(VC, f"1UBQ_p{p}_N{N}_probe_honly_*.json"))[0])
    return np.array(d["H"][:3]), np.array(d["floor"][:3]), d


out = dict(cells={}, ladders={}, backtest={}, hybrid={}, checks={})
lane = J(os.path.join(LANE, "tx_early_summary.json"))
for p in (19, 245):
    n22 = J(os.path.join(LANE, "runs", f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    h22 = J(os.path.join(LANE, "runs", f"1UBQ_p{p}_N22_honly_R1_complex64_s4242_t20-40-60.json"))
    n20 = J(os.path.join(LANE, "runs", f"1UBQ_p{p}_N20_echo_R2_complex64_s4242_t20-40-60.json"))
    assert n22["steps_done"] == [20] and n20["steps_done"] == [20], (n22["steps_done"], n20["steps_done"])
    ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json")) for N in (12, 14, 16, 18)}
    r20 = J(os.path.join(TC, f"1UBQ_p{p}_N20.json.ckpt.json"))["done"]
    HF = {N: vc(p, N)[:2] for N in (12, 14, 16, 18, 20)}
    # ---- 40 us rule cells
    per = lane["per_probe"][f"p{p}"]
    se_H = per["se_H"][0]; off = per["offset_exact_minus_csd_22"][0]
    for b in SITES:
        F22 = n22["F"][b][0]; F20 = n20["F"][b][0]
        X22 = F22 - n22["H"][0] - n22["floor"][0]
        X20 = F20 - n20["H"][0] - n20["floor"][0]
        dX = X22 - X20
        bud = math.sqrt(se_H ** 2 + off ** 2 + dX ** 2)
        lad = {N: ref[N]["F"][b][1] for N in (12, 14, 16, 18)}
        lad[20] = F20; lad[22] = F22
        lad["20ref"] = r20["20"][b]
        out["cells"][f"p{p}_b{b}"] = dict(F22=F22, F20=F20, dF=F22 - F20, X22=X22, X20=X20, dX=dX, budget=bud,
                                          pass_=bool(abs(dX) <= 0.005 and bud <= 0.01),
                                          dHF=(n22["H"][0] + n22["floor"][0]) - (n20["H"][0] + n20["floor"][0]),
                                          lane_dX=lane["cells"][f"p{p}_t40_b{b}"]["dX"],
                                          max_abs_FN_minus_F22_N18to20=max(abs(lad[N] - F22) for N in (18, 20, "20ref")),
                                          max_abs_FN_minus_F22_N16to20=max(abs(lad[N] - F22) for N in (16, 18, 20, "20ref")),
                                          hybrid_minus_F22=per["H_inf"][0] + X22 - F22,
                                          H_inf_minus_H22_minus_floor22=per["H_inf"][0] - n22["H"][0] - n22["floor"][0])
        out["ladders"][f"p{p}_b{b}_40us"] = {str(k): v for k, v in lad.items()}
        # the same ladder at 80 / 120 us (N <= 20 reference only)
        for ti, t in ((2, 80), (3, 120)):
            L = {N: ref[N]["F"][b][ti] for N in (12, 14, 16, 18)}
            if str(20 * ti) in r20:
                L[20] = r20[str(20 * ti)][b]
            out["ladders"][f"p{p}_b{b}_{t}us"] = {str(k): v for k, v in L.items()}
    # ---- H + floor ladder (40/80/120) incl. N = 22
    out["checks"][f"p{p}_H_plus_floor"] = {str(N): (HF[N][0] + HF[N][1]).tolist() for N in HF}
    out["checks"][f"p{p}_H_plus_floor"]["22"] = (np.array(h22["H"]) + np.array(h22["floor"])).tolist()
    out["checks"][f"p{p}_floor"] = {str(N): HF[N][1].tolist() for N in HF}
    out["checks"][f"p{p}_floor"]["22"] = h22["floor"]
    out["checks"][f"p{p}_H"] = {str(N): HF[N][0].tolist() for N in HF}
    out["checks"][f"p{p}_H"]["22"] = h22["H"]
    # ---- (1 - H)/N versus the exact floor
    out["checks"][f"p{p}_floor_over_(1-H)/N"] = {str(N): (HF[N][1] / ((1 - HF[N][0]) / N)).tolist() for N in HF}

# ---- back-test, re-derived
rows = []
for p in (19, 245):
    n22 = J(os.path.join(LANE, "runs", f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json"))["F"] for N in (14, 16, 18)}
    HF = {N: vc(p, N)[:2] for N in (14, 16, 18)}
    for b in SITES:
        Ft = n22["F"][b][0]
        for Ns in (14, 16, 18):
            Xs = ref[Ns][b][1] - HF[Ns][0][0] - HF[Ns][1][0]
            rows.append((Ns, n22["H"][0] + n22["floor"][0] + Xs - Ft, ref[Ns][b][1] - Ft))
for Ns in (14, 16, 18):
    eh = np.array([r[1] for r in rows if r[0] == Ns]); ef = np.array([r[2] for r in rows if r[0] == Ns])
    out["backtest"][f"Ns{Ns}"] = dict(rms_hybrid=float(np.sqrt(np.mean(eh ** 2))), rms_flat=float(np.sqrt(np.mean(ef ** 2))),
                                      mean_hybrid=float(eh.mean()), mean_flat=float(ef.mean()),
                                      flat_better=int(np.sum(np.abs(ef) < np.abs(eh))),
                                      identity_check="err_hybrid - err_flat = (H+floor)_22 - (H+floor)_Ns",
                                      mean_err_hybrid_minus_err_flat=float((eh - ef).mean()))
with open(os.path.join(HERE, "recheck_numbers.json"), "w") as f:
    json.dump(out, f, indent=1)
for k, c in out["cells"].items():
    print(f"{k}: F20 {c['F20']:.4f} F22 {c['F22']:.4f} dF {c['dF']:+.4f} dX {c['dX']:+.4f} (lane {c['lane_dX']:+.4f}) "
          f"-d(H+fl) {-c['dHF']:+.4f} budget {c['budget']:.4f} pass {c['pass_']} | max|FN-F22| 18-20 "
          f"{c['max_abs_FN_minus_F22_N18to20']:.4f} 16-20 {c['max_abs_FN_minus_F22_N16to20']:.4f} | hyb-F22 {c['hybrid_minus_F22']:+.4f}")
for k, v in out["backtest"].items():
    print(k, {a: round(b, 4) if isinstance(b, float) else b for a, b in v.items()})
for p in (19, 245):
    print(p, "H+floor", {N: [round(x, 4) for x in v] for N, v in out["checks"][f"p{p}_H_plus_floor"].items()})
    print(p, "floor/((1-H)/N)", {N: [round(x, 3) for x in v] for N, v in out["checks"][f"p{p}_floor_over_(1-H)/N"].items()})
for k, v in out["ladders"].items():
    print(k, {a: round(b, 4) for a, b in v.items()})
