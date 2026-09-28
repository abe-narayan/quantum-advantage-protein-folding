"""Analysis of the spinDMFT adversary (reads JSON only; < 1 CPU-s).  Applies PREREG_spindmft.md."""
import glob
import math
import json
import os

import numpy as np

HERE = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
OUTD = os.path.dirname(os.path.abspath(__file__))
R = os.path.abspath(os.path.join(HERE, "..", ".."))                      # research/experiments
CONE = os.path.join(R, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
VC = os.path.join(R, "ROUND3", "r1sim_exact_reach", "verify_classical", "runs")
CRIT = os.path.join(R, "ROUND3", "critic", "critic_checks.json")
SIG = 0.01
TIMES = [40, 80, 120]
SITES = [1, 7, 8, 9]
PROBES = [19, 245]


def load(p):
    return json.load(open(p))


def exact_F(p, N):
    f = os.path.join(CONE, f"1UBQ_p{p}_N{N}.json")
    if not os.path.exists(f):
        return None
    d = load(f)
    t = [round(x) for x in d["times_us"]]
    return {b: {tt: d["F"][str(b)][t.index(tt)] for tt in TIMES} for b in SITES}, d.get("err_typ")


def exact_H(p, N):
    fs = glob.glob(os.path.join(VC, f"1UBQ_p{p}_N{N}_probe_honly_*.json"))
    if not fs:
        return None
    d = load(fs[0])
    t = [round(x) for x in d["times_us"]]
    G = np.array(d["G"])
    return {tt: dict(H=d["H"][t.index(tt)], floor=d["floor"][t.index(tt)], Gaa=float(G[t.index(tt), 0]),
                     sumG=d["sumG"][t.index(tt)]) for tt in TIMES}


def csd(p):
    out = {}
    for f in glob.glob(os.path.join(VC, f"csd_1UBQ_p{p}_Nc*_M*_h1.0.json")):
        d = load(f)
        if "G" not in d:
            continue
        t = [round(x) for x in d["times_us"]]
        G = np.array(d["G"])
        out[f"Nc{d['Nc']}_M{d['M_done']}"] = {tt: dict(Gaa=float(G[t.index(tt), 0]), H=d["H_unbiased"][t.index(tt)])
                                              for tt in TIMES if tt in t}
    return out


def hybrid():
    rows = load(CRIT)["C1_early_window"]["rows"]
    out = {}
    for r in rows:
        p = int(r["probe"][1:])
        out[(p, r["t_us"], r["site"])] = dict(F18=r["F_last"], H18=r["H_last"], floor18=r["floor_last"],
                                              X18=r["F_last"] - r["H_last"] - r["floor_last"], Hinf=r["H_inf"],
                                              Fhyb=r["F_last"] - r["F_last_minus_Finf_hybrid"],
                                              Hbudget=r["hybrid_H_error_budget"])
    return out


def emb(p, W, nc, family="probeb", bath="sr"):
    fs = sorted(glob.glob(os.path.join(HERE, "out", f"emb_p{p}_W{W}_nc{nc}_{family}_{bath}_M*_s*.json")))
    fs = [f for f in fs if not f.endswith(".ckpt.json")]
    if not fs:
        return None
    d = load(fs[-1])
    t = [round(x) for x in d["times_us"]]
    oi = {tt: k for k, tt in enumerate(round(x) for x in [2 * s for s in [20, 40, 60]])}
    res = dict(M=d["M"], cpu=d.get("cpu"), complete=d.get("complete"), bath_M2_fraction=d["bath_M2_fraction"])
    for tt in TIMES:
        i = t.index(tt)
        res[tt] = dict(Gaa=d["Gaa"][i], Gaa_se=d["Gaa_se"][i], H_C=d["H_C"][i], sumG_C=d["sumG_C"][i])
        res[tt]["H_upper"] = res[tt]["H_C"] + max(0.0, 1.0 - res[tt]["sumG_C"]) ** 2
        for k, b in enumerate(d["bs_world"]):
            res[tt][f"F{b}"] = d["F"][oi[tt]][k]
            res[tt][f"F{b}_se"] = d["F_se"][oi[tt]][k]
    return res


def exact_ladder(p, tt, b):
    """exact F_N, H_N, floor_N, X_N for N = 12..20 (F_20 from the partial reference checkpoint where present)."""
    rows = []
    for N in (12, 14, 16, 18, 20):
        if N < 20:
            e = exact_F(p, N)
            F = e[0][b][tt] if e else None
        else:
            f = os.path.join(CONE, f"1UBQ_p{p}_N20.json.ckpt.json")
            dn = load(f)["done"] if os.path.exists(f) else {}
            F = dn.get(str(tt // 2), {}).get(str(b))
        h = exact_H(p, N)
        if F is None or h is None:
            continue
        rows.append(dict(N=N, F=F, H=h[tt]["H"], floor=h[tt]["floor"], X=F - h[tt]["H"] - h[tt]["floor"]))
    return rows


def flat_x_test(Ns=(14, 16, 18, 20)):
    """Hybrid premise: X_N converged, so F_N moves 1:1 with H_N + floor_N (slope s = 1).  Fit F_N = c + s (H_N + floor_N)
    per series over N in Ns, and pooled (series-specific intercepts) per time."""
    res = {}
    for tt in TIMES:
        per = []; xs = []; ys = []
        for p in PROBES:
            for b in SITES:
                L = [r for r in exact_ladder(p, tt, b) if r["N"] in Ns]
                if len(L) < 3:
                    continue
                x = np.array([r["H"] + r["floor"] for r in L]); y = np.array([r["F"] for r in L])
                s = float(np.polyfit(x, y, 1)[0]) if np.ptp(x) > 0 else float("nan")
                per.append(dict(probe=p, site=b, Ns=[r["N"] for r in L], slope=s, dF=float(y[-1] - y[0]),
                                d_H_plus_floor=float(x[-1] - x[0]), dX=float(L[-1]["X"] - L[0]["X"])))
                xs.append(x - x.mean()); ys.append(y - y.mean())
        X_ = np.concatenate(xs); Y_ = np.concatenate(ys)
        s = float((X_ * Y_).sum() / (X_ ** 2).sum())
        resid = Y_ - s * X_
        dof = max(1, len(X_) - 1 - len(xs))
        se = float(math.sqrt((resid ** 2).sum() / dof / (X_ ** 2).sum()))
        res[str(tt)] = dict(pooled_slope=s, pooled_slope_se=se, n_series=len(per), per_series=per)
    return res


def world_ladder(nc=10, Ns=(14, 16, 18, 20)):
    """Does spinDMFT reproduce the exact N-dependence of F_N?  dF_exact(N) = F_N - F_18 vs dF_dmft(N) = F^emb(W_N) - F^emb(W_18)
    (same n_c, same family).  Also the spinDMFT bath correction to the protein, F^emb(protein) - F^emb(W_18)."""
    res = {}
    for tt in TIMES:
        rows = []
        for p in PROBES:
            e18 = emb(p, "18", nc)
            eP = emb(p, "protein", nc)
            if not e18:
                continue
            for b in SITES:
                L = {r["N"]: r["F"] for r in exact_ladder(p, tt, b)}
                for N in Ns:
                    if N == 18 or N not in L:
                        continue
                    eN = emb(p, str(N), nc)
                    if not eN:
                        continue
                    dex = L[N] - L[18]
                    ddm = eN[tt][f"F{b}"] - e18[tt][f"F{b}"]
                    rows.append(dict(probe=p, site=b, N=N, dF_exact=dex, dF_dmft=ddm, err=ddm - dex,
                                     abs_err_dmft_vs_exact=eN[tt][f"F{b}"] - L[N]))
                if eP:
                    rows.append(dict(probe=p, site=b, N="protein", dF_dmft=eP[tt][f"F{b}"] - e18[tt][f"F{b}"]))
        e = [abs(r["err"]) for r in rows if "err" in r]
        dx = [abs(r["dF_exact"]) for r in rows if "err" in r]
        res[str(tt)] = dict(rows=rows, n=len(e), n_err_within_sigma=int(sum(x <= SIG for x in e)),
                            median_abs_err=float(np.median(e)) if e else None, max_abs_err=float(max(e)) if e else None,
                            median_abs_dF_exact=float(np.median(dx)) if dx else None,
                            protein_bath_corr=[(r["probe"], r["site"], round(r["dF_dmft"], 4)) for r in rows
                                               if r["N"] == "protein"])
    return res


def eb_test(hyb):
    """Addendum B: exact b-aware clusters vs the spinDMFT (b-aware, protein) prediction and the probe-family F_18."""
    res = {}
    for tt in TIMES:
        rows = []
        for (p, b) in ((245, 7), (19, 8), (19, 9)):
            r = emb(p, "protein", 10, family=f"pairb{b}")
            if not r:
                continue
            pred = r[tt][f"F{b}"]
            f18 = hyb[(p, tt, b)]["F18"]
            ex = {}
            for N in (12, 14, 16, 18):
                f = os.path.join(HERE, "out", f"exact_pairb_p{p}_b{b}_N{N}.json")
                if os.path.exists(f):
                    d = load(f)
                    ex[N] = d["F"][[round(x) for x in d["times_us"]].index(tt)]
            if not ex:
                continue
            Nmax = max(ex)
            shift = pred - f18
            counts = abs(shift) >= 2 * SIG
            moved = (ex[Nmax] - f18) / shift if shift != 0 else float("nan")
            rows.append(dict(probe=p, site=b, spinDMFT_pred=pred, F18_probe_family=f18, Fhyb=hyb[(p, tt, b)]["Fhyb"],
                             exact_baware={str(k): v for k, v in ex.items()}, N_used=Nmax, predicted_shift=shift,
                             counts=bool(counts), fraction_of_shift_realised=moved,
                             closer_to_spinDMFT=bool(abs(ex[Nmax] - pred) < abs(ex[Nmax] - f18)),
                             exact_minus_spinDMFT=ex[Nmax] - pred, exact_minus_hybrid=ex[Nmax] - hyb[(p, tt, b)]["Fhyb"]))
        cnt = [r_ for r_ in rows if r_["counts"]]
        res[str(tt)] = dict(rows=rows, n_counting=len(cnt), n_closer_to_spinDMFT=int(sum(r_["closer_to_spinDMFT"] for r_ in cnt)),
                            corroborated=bool(len(cnt) >= 2 and sum(r_["closer_to_spinDMFT"] for r_ in cnt) >= 2))
    return res


def main():
    hyb = hybrid()
    out_eb = eb_test(hyb)
    for tt in TIMES:
        e = out_eb[str(tt)]
        print("E-B t=%d corroborated=%s (%d/%d counting series closer to spinDMFT)" % (
            tt, e["corroborated"], e["n_closer_to_spinDMFT"], e["n_counting"]),
            [(r["probe"], r["site"], "N%d" % r["N_used"], round(r["exact_baware"][str(r["N_used"])], 4),
              "pred", round(r["spinDMFT_pred"], 4), "F18", round(r["F18_probe_family"], 4), "hyb", round(r["Fhyb"], 4))
             for r in e["rows"]])
    out = dict(sigma=SIG, times_us=TIMES, sites=SITES)
    out["EB_exact_baware"] = out_eb
    out["flat_X_test"] = flat_x_test()
    out["exact_ladders"] = {f"p{p}_t{tt}_b{b}": exact_ladder(p, tt, b) for p in PROBES for tt in TIMES for b in SITES}
    out["world_ladder_nc10"] = world_ladder(10)
    for tt in TIMES:
        wl = out["world_ladder_nc10"][str(tt)]
        print("worldladder t=%d: n=%d within sigma %d, median|err| %s max %s, median|dF_exact| %s; protein bath corr %s" % (
            tt, wl["n"], wl["n_err_within_sigma"], wl["median_abs_err"], wl["max_abs_err"], wl["median_abs_dF_exact"],
            wl["protein_bath_corr"]))
    pb = {}
    for (p, b) in ((19, 8), (19, 9), (245, 7)):
        for W in ("protein", "18"):
            r = emb(p, W, 10, family=f"pairb{b}")
            if r:
                pb[f"p{p}_b{b}_W{W}"] = {tt: dict(F=r[tt][f"F{b}"], F_se=r[tt][f"F{b}_se"], Gaa=r[tt]["Gaa"]) for tt in TIMES}
    out["pairb_nc10"] = pb
    if pb:
        print("pairb:", json.dumps({k: {t: round(v[t]["F"], 4) for t in TIMES} for k, v in pb.items()}))
    for tt in TIMES:
        ft = out["flat_X_test"][str(tt)]
        print("flatX t=%d pooled slope dF/d(H+floor) = %.2f +- %.2f" % (tt, ft["pooled_slope"], ft["pooled_slope_se"]),
              [(d["probe"], d["site"], round(d["dF"], 4), round(d["d_H_plus_floor"], 4)) for d in ft["per_series"]])
    # ---------------- two-point table
    tp = {}
    for p in PROBES:
        e = {N: exact_H(p, N) for N in (12, 14, 16, 18, 20)}
        tp[p] = dict(exact={N: v for N, v in e.items() if v}, csd=csd(p))
        for W in ("protein", "18"):
            for nc in (1, 10, 12, 14):
                r = emb(p, W, nc)
                if r:
                    tp[p][f"nl_W{W}_nc{nc}"] = {tt: r[tt] for tt in TIMES}
        for W, fn in (("protein", "sr_protein_T120_M384.json"), ("18", f"sr_1UBQ_p{p}_N18_T120_M4096.json")):
            f = os.path.join(HERE, "out", fn)
            if os.path.exists(f):
                d = load(f)
                g = d["g_sites"][str(p) if W == "protein" else "0"]["gz"]
                tp[p][f"sr_W{W}"] = {tt: dict(Gaa=g[tt]) for tt in TIMES}
    out["two_point"] = {str(k): v for k, v in tp.items()}
    # ---------------- echo tables
    ncs = [10]                                   # common to both probes; larger n_c reported per probe below
    ncs18 = [10]
    rows = []
    for p in PROBES:
        for tt in TIMES:
            for b in SITES:
                h = hyb[(p, tt, b)]
                row = dict(probe=p, t_us=tt, site=b, **{k: round(v, 5) for k, v in h.items()})
                row["F18_minus_floor"] = round(h["F18"] - h["floor18"], 5)
                for nc in ncs18:
                    v = emb(p, "18", nc)[tt]
                    row[f"emb18_nc{nc}"] = round(v[f"F{b}"], 5)
                    row[f"emb18_nc{nc}_se"] = round(v[f"F{b}_se"], 5)
                    row[f"val_err_nc{nc}_vs_F18mf"] = round(v[f"F{b}"] - (h["F18"] - h["floor18"]), 5)
                    row[f"val_err_nc{nc}_vs_F18"] = round(v[f"F{b}"] - h["F18"], 5)
                for nc in ncs:
                    v = emb(p, "protein", nc)[tt]
                    row[f"embP_nc{nc}"] = round(v[f"F{b}"], 5)
                    row[f"embP_nc{nc}_se"] = round(v[f"F{b}_se"], 5)
                    row[f"kill_diff_nc{nc}"] = round(v[f"F{b}"] - h["Fhyb"], 5)
                    if nc in ncs18:
                        dW = v[f"F{b}"] - emb(p, "18", nc)[tt][f"F{b}"]
                        row[f"bathcorr_nc{nc}"] = round(dW, 5)
                        # primary (deviation D1): F_corr = F_18 + spinDMFT bath correction (no floor subtraction)
                        row[f"Fcorr_nc{nc}"] = round(h["F18"] + dW, 5)
                        row[f"Fcorr_nc{nc}_minus_hyb"] = round(h["F18"] + dW - h["Fhyb"], 5)
                        # pre-registered convention (floor subtracted), kept for the record
                        row[f"Fcorrmf_nc{nc}"] = round(h["F18"] - h["floor18"] + dW, 5)
                        row[f"Fcorrmf_nc{nc}_minus_hyb"] = round(h["F18"] - h["floor18"] + dW - h["Fhyb"], 5)
                    L20 = {r_["N"]: r_["F"] for r_ in exact_ladder(p, tt, b)}
                    e20 = emb(p, "20", nc)
                    if 20 in L20 and e20:
                        dW20 = v[f"F{b}"] - e20[tt][f"F{b}"]
                        row[f"F20"] = round(L20[20], 5)
                        row[f"Fcorr20_nc{nc}"] = round(L20[20] + dW20, 5)
                        row[f"Fcorr20_nc{nc}_minus_hyb"] = round(L20[20] + dW20 - h["Fhyb"], 5)
                for nc in (12, 14):                       # per-probe larger clusters where run
                    vP = emb(p, "protein", nc); v18 = emb(p, "18", nc)
                    if vP:
                        row[f"embP_nc{nc}"] = round(vP[tt][f"F{b}"], 5)
                        row[f"kill_diff_nc{nc}"] = round(vP[tt][f"F{b}"] - h["Fhyb"], 5)
                    if v18:
                        row[f"emb18_nc{nc}"] = round(v18[tt][f"F{b}"], 5)
                        row[f"val_err_nc{nc}_vs_F18"] = round(v18[tt][f"F{b}"] - h["F18"], 5)
                    if vP and v18:
                        row[f"bathcorr_nc{nc}"] = round(vP[tt][f"F{b}"] - v18[tt][f"F{b}"], 5)
                rows.append(row)
    out["echo_rows"] = rows
    # ---------------- decisions
    dec = {}
    ncP = max(ncs) if ncs else None
    nc18 = max(ncs18) if ncs18 else None
    for tt in TIMES:
        rr = [r for r in rows if r["t_us"] == tt]
        d = {}
        if ncP:
            diffs = [abs(r[f"kill_diff_nc{ncP}"]) for r in rr]
            d["literal_rule_nc"] = ncP
            d["n_agree_within_sigma"] = int(sum(x <= SIG for x in diffs))
            d["n_series"] = len(rr)
            d["median_abs_diff"] = float(np.median(diffs))
            d["max_abs_diff"] = float(np.max(diffs))
            d["literal_KILL_fires"] = d["n_agree_within_sigma"] >= 7
        if nc18:
            v1 = [abs(r[f"val_err_nc{nc18}_vs_F18mf"]) for r in rr]
            v2 = [abs(r[f"val_err_nc{nc18}_vs_F18"]) for r in rr]
            d["validation_nc"] = nc18
            d["val_n_within_sigma_vs_F18_minus_floor"] = int(sum(x <= SIG for x in v1))
            d["val_n_within_sigma_vs_F18"] = int(sum(x <= SIG for x in v2))
            d["val_max_err_vs_F18_minus_floor"] = float(max(v1))
            d["val_max_err_vs_F18"] = float(max(v2))
            d["validated_primary"] = d["val_n_within_sigma_vs_F18_minus_floor"] >= 6
        if ncP and nc18 and f"Fcorr_nc{min(ncP, nc18)}_minus_hyb" in rr[0]:
            nn = min(ncP, nc18)
            c = [abs(r[f"Fcorr_nc{nn}_minus_hyb"]) for r in rr]
            d["bathcorr_estimator_nc"] = nn
            d["bathcorr_n_agree_with_hyb"] = int(sum(x <= SIG for x in c))
            d["bathcorr_median_abs_diff"] = float(np.median(c))
            d["bathcorr_signed_diffs"] = [round(r[f"Fcorr_nc{nn}_minus_hyb"], 4) for r in rr]
            c20 = [r[f"Fcorr20_nc{nn}_minus_hyb"] for r in rr if f"Fcorr20_nc{nn}_minus_hyb" in r]
            d["bathcorr20_signed_diffs"] = [round(x, 4) for x in c20]
            d["bathcorr_abs"] = [round(r[f"bathcorr_nc{nn}"], 4) for r in rr]
            d["n_bathcorr_le_sigma"] = int(sum(abs(r[f"bathcorr_nc{nn}"]) <= SIG for r in rr))
        if len(ncs) >= 2:
            a_, b_ = ncs[-2], ncs[-1]
            ch = [abs(r[f"embP_nc{b_}"] - r[f"embP_nc{a_}"]) for r in rr]
            d["nc_step"] = [a_, b_]
            d["nc_step_n_within_sigma"] = int(sum(x <= SIG for x in ch))
            d["nc_step_max"] = float(max(ch))
        if len(ncs18) >= 2:
            a_, b_ = ncs18[-2], ncs18[-1]
            e1 = [abs(r[f"val_err_nc{a_}_vs_F18mf"]) for r in rr]
            e2 = [abs(r[f"val_err_nc{b_}_vs_F18mf"]) for r in rr]
            d["val_err_median_nc"] = {str(a_): float(np.median(e1)), str(b_): float(np.median(e2))}
            e1 = [abs(r[f"val_err_nc{a_}_vs_F18"]) for r in rr]
            e2 = [abs(r[f"val_err_nc{b_}_vs_F18"]) for r in rr]
            d["val_err_median_nc_vs_F18"] = {str(a_): float(np.median(e1)), str(b_): float(np.median(e2))}
        dec[str(tt)] = d
    out["decisions"] = dec
    json.dump(out, open(os.path.join(OUTD, "analysis_rerun.json"), "w"), indent=1)
    # ---------------- print
    for tt in TIMES:
        print(tt, json.dumps(dec[str(tt)]))
    hdr = ["probe", "t_us", "site", "F18", "F18_minus_floor", "Fhyb"]
    keys = ["emb18_nc10", "embP_nc10", "embP_nc12", "Fcorr_nc10", "F20", "Fcorr20_nc10"]
    print(" ".join(f"{h[:10]:>10s}" for h in hdr + keys))
    for r in rows:
        print(" ".join((f"{r[h]:10.4f}" if isinstance(r[h], float) else f"{r[h]:>10}") if h in r else f"{'--':>10}"
                       for h in hdr + keys))


if __name__ == "__main__":
    main()
