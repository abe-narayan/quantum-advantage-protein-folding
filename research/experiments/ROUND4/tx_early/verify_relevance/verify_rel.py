"""Relevance/novelty verifier for ROUND4 lane tx_early (no dynamics; < 5 CPU-s; -> verify_rel.json).

Checks
 A. Re-read the lane's own 40 us F ladders (N = 12..22) and 1/N fits (stored in tx_early_summary.json but not reported
    in the README). Quantify F_inf(1/N) - F_22 per series, and an extrapolation back-test: does a 1/N fit on
    N in {14,16,18} predict F_22 better or worse than flat F_18?
 B. Separate 'informative' series (1 - F_22 >= 0.1: the operator front has reached b) from near-trivial ones
    (F_22 >= 0.95), because convergence of F ~ 1 at sites the front has barely reached is close to automatic.
 C. Local-field coverage: fraction of the full-protein second moment M2_b = sum_j d_bj^2 (same b0, all 1UBQ protons)
    that lies inside the probe-centred N-cluster, N = 10..22 and 80. A low coverage at N = 22 for a site b means
    the flat F ladder over 16..22 is not evidence about spins that matter to b (the lane's UNPROVEN step).
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import kernels as KR  # noqa: E402  (imports ROUND3 fastecho as FE, spins as SP)

FE, SP = KR.FE, KR.SP
SIG = 0.01

S = json.load(open(os.path.join(LANE, "tx_early_summary.json")))
out = dict(A_extrapolation={}, B_classes={}, C_coverage={})

# ---------------------------------------------------------------- A/B
for key, c in S["cells"].items():
    if "F22" not in c:
        continue
    lad = {int(n): v for n, v in c["F_ladder_ref"].items()}
    lad[20] = c["F20"]
    lad[22] = c["F22"]
    Ns = np.array(sorted(lad))
    F = np.array([lad[n] for n in Ns])

    def fit(sel):
        A = np.vstack([np.ones(len(sel)), 1.0 / sel]).T
        coef, *_ = np.linalg.lstsq(A, np.array([lad[n] for n in sel]), rcond=None)
        return coef  # F_inf, c

    r = {}
    for lo in (14, 16):
        sel = Ns[Ns >= lo]
        Finf, cc = fit(sel)
        r[f"Finf_invN_{lo}_22"] = float(Finf)
        r[f"gap_invN_{lo}_22_over_sigma"] = float((Finf - lad[22]) / SIG)
    # extrapolation back-test from N_s window {14,16,18}
    Finf, cc = fit(np.array([14, 16, 18]))
    pred_invN = Finf + cc / 22.0
    r["backtest_F22_err_invN_from_14_18"] = float(pred_invN - lad[22])
    r["backtest_F22_err_flat_F18"] = float(lad[18] - lad[22])
    r["F22"] = lad[22]
    r["one_minus_F22"] = 1 - lad[22]
    r["class"] = "informative" if 1 - lad[22] >= 0.1 else "near-trivial (front barely at b)"
    r["F12_minus_F22_over_sigma"] = float((lad[12] - lad[22]) / SIG)
    out["A_extrapolation"][key] = r

inf = [k for k, r in out["A_extrapolation"].items() if r["class"] == "informative"]
out["B_classes"] = dict(informative=inf, n_informative=len(inf),
                        n_near_trivial=len(out["A_extrapolation"]) - len(inf))
e_inv = np.array([r["backtest_F22_err_invN_from_14_18"] for r in out["A_extrapolation"].values()])
e_flat = np.array([r["backtest_F22_err_flat_F18"] for r in out["A_extrapolation"].values()])
out["A_summary"] = dict(
    rms_invN_extrap=float(np.sqrt(np.mean(e_inv ** 2))), rms_flat=float(np.sqrt(np.mean(e_flat ** 2))),
    invN_better=int(np.sum(np.abs(e_inv) < np.abs(e_flat))), n=len(e_inv),
    max_abs_gap_invN_16_22_sigma=float(max(abs(r["gap_invN_16_22_over_sigma"]) for r in out["A_extrapolation"].values())),
    gaps_invN_16_22_sigma={k: round(r["gap_invN_16_22_over_sigma"], 2) for k, r in out["A_extrapolation"].items()},
    gaps_invN_14_22_sigma={k: round(r["gap_invN_14_22_over_sigma"], 2) for k, r in out["A_extrapolation"].items()},
)

# ---------------------------------------------------------------- C
names, xyz, _ = SP.read_h_coords(os.path.join(KR.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
b0 = FE.random_b0(1000)
for p in (19, 245):
    bs = FE.instrument_bs(xyz, p)
    order = SP.cluster(xyz, p, len(xyz))  # all protons ordered by distance to probe
    dm_all = SP.couplings(xyz[order], b0)  # full protein, probe-ordered (index 0 = probe)
    M2_tot = (dm_all ** 2).sum(axis=1)
    cov = {}
    for site in [0] + list(bs):
        row = {}
        for N in (10, 12, 14, 16, 18, 20, 22, 30, 40, 80):
            row[N] = float((dm_all[site, :N] ** 2).sum() / M2_tot[site])
        cov["a(probe)" if site == 0 else f"b{site}"] = row
    # also: nearest out-of-cluster neighbours of each b at N = 22 (distance, share of M2_b)
    miss = {}
    for site in bs:
        w = dm_all[site, 22:] ** 2 / M2_tot[site]
        top = np.argsort(-w)[:3]
        miss[f"b{site}"] = [dict(rank_from_probe=int(22 + t), share_M2=float(w[t]),
                                 r_to_b_A=float(np.linalg.norm(xyz[order[22 + t]] - xyz[order[site]]))) for t in top]
    out["C_coverage"][f"p{p}"] = dict(n_protons_protein=int(len(xyz)), bs=list(map(int, bs)), coverage=cov,
                                      top_missing_at_N22=miss)

with open(os.path.join(HERE, "verify_rel.json.tmp"), "w") as f:
    json.dump(out, f, indent=1)
os.replace(os.path.join(HERE, "verify_rel.json.tmp"), os.path.join(HERE, "verify_rel.json"))

print("A. 1/N gaps (F_inf - F22)/sigma, fit 16-22:", out["A_summary"]["gaps_invN_16_22_sigma"])
print("   fit 14-22:", out["A_summary"]["gaps_invN_14_22_sigma"])
print("   extrap back-test F22 from 14-18: rms invN %.4f vs flat %.4f; invN better %d/%d" % (
    out["A_summary"]["rms_invN_extrap"], out["A_summary"]["rms_flat"], out["A_summary"]["invN_better"], out["A_summary"]["n"]))
for k, r in out["A_extrapolation"].items():
    print("  ", k, r["class"], "1-F22=%.3f" % r["one_minus_F22"], "F12-F22=%.1f sigma" % r["F12_minus_F22_over_sigma"],
          "err invN %+.4f flat %+.4f" % (r["backtest_F22_err_invN_from_14_18"], r["backtest_F22_err_flat_F18"]))
for p, d in out["C_coverage"].items():
    print("C.", p, "protons", d["n_protons_protein"], "bs", d["bs"])
    for s, row in d["coverage"].items():
        print("    %-9s" % s, " ".join("N%d=%.2f" % (n, v) for n, v in row.items()))
    for s, m in d["top_missing_at_N22"].items():
        print("    missing@22", s, [(x["rank_from_probe"], round(x["share_M2"], 3), round(x["r_to_b_A"], 2)) for x in m])
