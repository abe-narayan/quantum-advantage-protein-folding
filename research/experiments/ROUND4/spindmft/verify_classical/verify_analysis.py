"""Classical verifier analysis for the ROUND4 spindmft lane (reads JSON/NPZ only; < 5 CPU-s).
Inputs: the lane's analysis.json / out/*.json (read-only) and this folder's out/*.json.
Output: verify_summary.json (+ stdout)."""
import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import analyze as A  # noqa: E402  (read-only helpers; its main() is NOT called)
import sdmft as S  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

SIG = 0.01
T = [40, 80, 120]
SER = [(19, 1), (19, 7), (19, 8), (19, 9), (245, 1), (245, 7), (245, 8), (245, 9)]
BREM = [(19, 8), (19, 9), (245, 7)]
O = os.path.join(HERE, "out")
lane = json.load(open(os.path.join(LANE, "analysis.json")))
rows = {(r["probe"], r["t_us"], r["site"]): r for r in lane["echo_rows"]}
out = {}

# ---------------------------------------------------------------- 1. flat-X test, independent re-computation
fx = {}
rng = np.random.default_rng(1)
for tt in T:
    per = []
    for p, b in SER:
        L = [r for r in A.exact_ladder(p, tt, b) if r["N"] in (14, 16, 18, 20)]
        per.append((np.array([r["H"] + r["floor"] for r in L]), np.array([r["F"] for r in L])))

    def pooled(ix, Ns_drop=None):
        xs, ys = [], []
        for i in ix:
            x, y = per[i]
            xs.append(x - x.mean()); ys.append(y - y.mean())
        X_ = np.concatenate(xs); Y_ = np.concatenate(ys)
        return float((X_ * Y_).sum() / (X_ ** 2).sum())
    s = pooled(range(8))
    boots = [pooled(rng.integers(0, 8, 8)) for _ in range(4000)]
    # direct test: mean dF(14->20) vs the hybrid's prediction dF = d(H+floor)
    dF = np.array([y[-1] - y[0] for x, y in per]); dHF = np.array([x[-1] - x[0] for x, y in per])
    resid = dF - dHF
    fx[str(tt)] = dict(pooled_slope=s, bootstrap_series_se=float(np.std(boots)),
                       bootstrap_95=[float(np.percentile(boots, 2.5)), float(np.percentile(boots, 97.5))],
                       mean_dF_14_20=float(dF.mean()), mean_hybrid_pred_dF=float(dHF.mean()),
                       mean_dF_minus_pred=float(resid.mean()), se_dF_minus_pred=float(resid.std(ddof=1) / math.sqrt(8)),
                       z=float(resid.mean() / (resid.std(ddof=1) / math.sqrt(8))))
out["flatX_recomputed"] = fx

# ---------------------------------------------------------------- 2. independent exact b-aware family (fastecho kernel)
def fe(p, b, N):
    for R, dt in ((2, "complex128"), (1, "complex64")):
        f = os.path.join(O, f"fe_pairb_p{p}_b{b}_N{N}_R{R}_{dt}.json")
        if os.path.exists(f):
            return json.load(open(f))
    return None


def lane_exact_pairb(p, b, N):
    f = os.path.join(LANE, "out", f"exact_pairb_p{p}_b{b}_N{N}.json")
    return json.load(open(f)) if os.path.exists(f) else None


bl = {}
for p, b in SER:
    d = {}
    for N in (16, 18, 20):
        r = fe(p, b, N)
        if r:
            d[str(N)] = dict(F=[round(x, 4) for x in r["F"]], H=[round(x, 4) for x in r["H"]],
                             floor=[round(x, 4) for x in r["floor"]], X=[round(x, 4) for x in r["X"]],
                             cpu_s=round(r["cpu_s"], 1), err_typ=round(r["err_typ"], 4))
    ln = lane_exact_pairb(p, b, 16)
    if ln:
        d["lane_N16_F"] = [round(x, 4) for x in ln["F"][1:]]
        d["indep_minus_lane_N16"] = [round(a_ - b_, 4) for a_, b_ in zip(fe(p, b, 16)["F"], ln["F"][1:])]
    bl[f"p{p}_b{b}"] = d
out["baware_exact_independent"] = bl

# ---------------------------------------------------------------- 3. bath corrections: sr (lane) vs CSD (here), probe family
def embcsd(p, W):
    f = os.path.join(O, f"embcsd_p{p}_W{W}_nc10_probeb_M512_s7.json")
    return json.load(open(f)) if os.path.exists(f) else None


bc = {}
for p in (19, 245):
    eP, e18 = embcsd(p, "protein"), embcsd(p, "18")
    for k, b in enumerate(eP["bs_world"]):
        for i, tt in enumerate(T):
            dcsd = eP["F"][i][k] - e18["F"][i][k]
            dsr = rows[(p, tt, b)]["bathcorr_nc10"]
            bc[f"p{p}_b{b}_t{tt}"] = dict(sr=round(dsr, 4), csd=round(dcsd, 4), diff=round(dcsd - dsr, 4),
                                          csd_abs_err_W18=round(e18["F"][i][k] - rows[(p, tt, b)]["F18"], 4))
out["bathcorr_sr_vs_csd_probeb"] = bc
for tt in T:
    dd = [abs(v["diff"]) for k, v in bc.items() if k.endswith(f"t{tt}")]
    out.setdefault("bathcorr_sr_vs_csd_max", {})[str(tt)] = round(max(dd), 4)

# ---------------------------------------------------------------- 4. E2 = exact b-aware + CSD-bath correction; E1 = lane F_corr
def embb(p, b, Nref, W, nc=10, M=512):
    f = os.path.join(O, f"embb_p{p}_b{b}_Nref{Nref}_W{W}_nc{nc}_M{M}_s7.json")
    return json.load(open(f)) if os.path.exists(f) else None


cmp_ = {str(tt): [] for tt in T}
for p, b in SER:
    Nref = 20 if (p, b) in BREM else 18
    ex = fe(p, b, Nref)
    eW, eP = embb(p, b, Nref, "Wb"), embb(p, b, Nref, "protein")
    for i, tt in enumerate(T):
        r = rows[(p, tt, b)]
        dW = eP["F"][i] - eW["F"][i]
        E2 = ex["F"][i] + dW
        E1 = r["Fcorr_nc10"]
        E1b = r.get("Fcorr20_nc10")
        Fprobe = r.get("F20", r["F18"])
        rec = dict(probe=p, site=b, Nref=Nref, exact_baware=round(ex["F"][i], 4), dW_b_csd=round(dW, 4),
                   E2=round(E2, 4), E1_lane_Fcorr=round(E1, 4), E1_lane_Fcorr20=(round(E1b, 4) if E1b else None),
                   exact_probe_last=round(Fprobe, 4), hybrid=round(r["Fhyb"], 4),
                   E2_minus_E1=round(E2 - E1, 4), E2_minus_hybrid=round(E2 - r["Fhyb"], 4),
                   emb_Wb_abs_err=round(eW["F"][i] - ex["F"][i], 4),
                   baware_minus_probe_exact=round(ex["F"][i] - Fprobe, 4),
                   within_sigma=bool(abs(E2 - E1) <= SIG))
        if (p, b) in BREM:
            pb = lane["pairb_nc10"][f"p{p}_b{b}_Wprotein"][str(tt)]["F"]
            rec["lane_spinDMFT_baware_pred"] = round(pb, 4)
            rec["exact_baware_minus_lane_pred"] = round(ex["F"][i] - pb, 4)
        cmp_[str(tt)].append(rec)
out["E1_vs_E2"] = cmp_
summ = {}
for tt in T:
    rr = cmp_[str(tt)]
    summ[str(tt)] = dict(n_within_sigma=int(sum(r["within_sigma"] for r in rr)), n=len(rr),
                         max_abs=round(max(abs(r["E2_minus_E1"]) for r in rr), 4),
                         E2_minus_hybrid_range=[round(min(r["E2_minus_hybrid"] for r in rr), 4),
                                                round(max(r["E2_minus_hybrid"] for r in rr), 4)],
                         brem_exact_vs_lane_pred=[r["exact_baware_minus_lane_pred"] for r in rr if "lane_spinDMFT_baware_pred" in r],
                         brem_exact_vs_lane_pred_within_sigma=int(sum(abs(r["exact_baware_minus_lane_pred"]) <= SIG for r in rr
                                                                      if "lane_spinDMFT_baware_pred" in r)),
                         exact_family_spread_gt_sigma=int(sum(abs(r["baware_minus_probe_exact"]) > SIG for r in rr)))
out["E1_vs_E2_summary"] = summ

# n_c stability of the b-aware correction (p19 b1)
e10 = (embb(19, 1, 18, "protein")["F"], embb(19, 1, 18, "Wb")["F"])
e12 = (embb(19, 1, 18, "protein", 12, 256)["F"], embb(19, 1, 18, "Wb", 12, 256)["F"])
out["nc_stability_p19_b1"] = dict(dW_nc10=[round(a_ - b_, 4) for a_, b_ in zip(*e10)],
                                  dW_nc12=[round(a_ - b_, 4) for a_, b_ in zip(*e12)],
                                  Wb_abs_err_nc12=[round(x - y, 4) for x, y in zip(e12[1], fe(19, 1, 18)["F"])])

# ---------------------------------------------------------------- 5. two-point sanity: CSD bath G_aa vs exact and vs sr
csd18 = {p: json.load(open(os.path.join(O, f"csd_p{p}_N18_M8192.json")))["g_probe"]["gz"][1:] for p in (19, 245)}
out["Gaa_N18_world"] = {str(p): dict(csd=csd18[p], exact=[round(A.exact_H(p, 18)[tt]["Gaa"], 4) for tt in T],
                                     sr=[round(x, 4) for x in [lane["two_point"][str(p)]["sr_W18"][str(tt)]["Gaa"] for tt in T]])
                        for p in (19, 245)}

# ---------------------------------------------------------------- 6. z_eff median (lane: 3.15)
names, xyz, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
D = SP.couplings(xyz, S.random_b0(1000))
d2 = D ** 2
zeff = (d2.sum(1) ** 2) / (d2 ** 2).sum(1)
out["z_eff"] = dict(median=round(float(np.median(zeff)), 3), p19=round(float(zeff[19]), 2), p245=round(float(zeff[245]), 2))

# ---------------------------------------------------------------- compute ledger
tot = 0.0
for f in glob.glob(os.path.join(O, "*.json")):
    if f.endswith("ckpt.json"):
        continue
    d = json.load(open(f))
    tot += d.get("cpu_s") or d.get("cpu") or 0.0
out["cpu_logged_min"] = round(tot / 60, 1)
json.dump(out, open(os.path.join(HERE, "verify_summary.json"), "w"), indent=1)

print("flatX:", json.dumps(fx, indent=0))
for p, b in SER:
    print(f"p{p} b{b} b-aware:", json.dumps(bl[f"p{p}_b{b}"]))
print("bathcorr sr vs csd max |diff| by t:", out["bathcorr_sr_vs_csd_max"])
for k, v in bc.items():
    print(" ", k, v)
for tt in T:
    print("t=%d E1 vs E2:" % tt, json.dumps(summ[str(tt)]))
    for r in cmp_[str(tt)]:
        print("   ", json.dumps(r))
print("nc stability p19 b1:", out["nc_stability_p19_b1"])
print("Gaa N18 world:", out["Gaa_N18_world"])
print("z_eff:", out["z_eff"], "cpu_logged_min:", out["cpu_logged_min"])
