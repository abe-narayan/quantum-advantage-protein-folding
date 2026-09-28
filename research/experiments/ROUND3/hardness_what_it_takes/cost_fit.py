"""ROUND3 / hardness_what_it_takes, part (1): classical cost-to-solution C_c(L) from the measured G1 data, with honest
censoring, for every classical method measured, and the best classical method per task.

Tasks (all native-free; RMSD is an ORACLE label only):
  T-own   hit the multistart census' OWN best 2-A cluster (the G1 metric; p_hit ~ exp(-0.028 L) in g1_summary.json)
  T-ref   reach E <= E_ref + 20, E_ref = lowest energy found on the crop by ANY method (census, NRPT, DG)
  T-fold  land within 3 A CA-RMSD of the best-known polished fold (ms_polish_fold.json, 4 crops)
  T-samp  one decorrelated T=1 posterior sample (NRPT round trip; right-censored lower bounds only)

Censoring: a p_hit at the census floor (1 hit in R restarts, which is the best itself) is treated as right-censored in
cost (p <= 1/R); 0 hits in n attempts gives p < 3/n (95%); 0 NRPT round trips in N production evaluations gives cost per
trip > N/3 (95%, Poisson).  Fits: Tobit (censored normal) regression of log p on L (exponential law) and on log L (power
law), compared by BIC.

Inputs: research/results/PROCESSED/g1_summary.json; research/results/RAW/g1_tscan, g1_pilot (NRPT production counts);
this folder: dg_summary.json, ms_polish_results.json, ms_polish_fold.json, polish_results.json.
Output: cost_fit.json
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np
from scipy import optimize, stats

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def tobit(y, X, cens):
    """Censored normal regression: y = X b + e, e ~ N(0, s^2); cens[i] = True means y_i is an UPPER bound (y <= y_i).
    Returns (b, s, loglik)."""
    y = np.asarray(y, float); X = np.asarray(X, float); cens = np.asarray(cens, bool)

    def nll(th):
        b, ls = th[:-1], th[-1]
        s = math.exp(ls)
        mu = X @ b
        ll = np.where(cens, stats.norm.logcdf((y - mu) / s), stats.norm.logpdf((y - mu) / s) - ls)
        return -ll.sum()
    b0 = np.linalg.lstsq(X, y, rcond=None)[0]
    th0 = np.concatenate([b0, [math.log(max(np.std(y - X @ b0), 1e-3))]])
    r = optimize.minimize(nll, th0, method="Nelder-Mead", options=dict(maxiter=20000, xatol=1e-8, fatol=1e-10))
    return r.x[:-1], math.exp(r.x[-1]), -r.fun


def fit_both(Ls, logp, cens):
    Ls = np.asarray(Ls, float)
    n = len(Ls)
    out = {}
    for name, X in (("exponential", np.c_[np.ones(n), Ls]), ("power", np.c_[np.ones(n), np.log(Ls)])):
        b, s, ll = tobit(logp, X, cens)
        out[name] = dict(a=float(b[0]), b=float(b[1]), sigma=float(s), loglik=float(ll), BIC=float(-2 * ll + 3 * math.log(n)))
    out["dBIC_power_minus_exp"] = out["power"]["BIC"] - out["exponential"]["BIC"]
    return out


def main():
    g1 = json.load(open(os.path.join(REPO, "research", "results", "PROCESSED", "g1_summary.json")))
    res = {}

    # ---------------- T-own: multistart to its own best 2-A cluster (census 256; 2048 where available)
    rows = []
    c2k = {r["crop"]: r for r in g1["census2k"]}
    for r in g1["census256"]:
        R, p = r["R"], r["p_hit"]
        n_per = r["grad_evals"] / R
        rows.append(dict(crop=r["crop"], L=r["L"], R=R, p=p, cens=bool(p <= 1.0 / R + 1e-12), n_per=n_per,
                         C=n_per / p, src="census256"))
    y = [math.log(r["p"]) for r in rows]
    f256 = fit_both([r["L"] for r in rows], y, [r["cens"] for r in rows])
    per_L = {}
    for L in sorted({r["L"] for r in rows}):
        rs = [r for r in rows if r["L"] == L]
        per_L[str(L)] = dict(n=len(rs), n_censored=int(sum(r["cens"] for r in rs)),
                             gmean_p=float(np.exp(np.mean([math.log(r["p"]) for r in rs]))),
                             median_C=float(np.median([r["C"] for r in rs])), n_per_restart=float(np.mean([r["n_per"] for r in rs])))
    # the same crops at R = 2048 (moving-target check: the 'best' basin changes with R when the census is unsaturated)
    mt = []
    for crop, r2 in c2k.items():
        r1 = next((r for r in g1["census256"] if r["crop"] == crop), None)
        if r1:
            mt.append(dict(crop=crop, L=r2["L"], p256=r1["p_hit"], p2048=r2["p_hit"],
                           best_changed=bool(r2["p_hit"] < r1["p_hit"] / 4)))
    ex = f256["exponential"]
    res["T_own"] = dict(definition="multistart (exact prior, 200 L-BFGS its) hits its own best 2-A cluster", fit=f256,
                        per_L=per_L, moving_target_2048=mt,
                        extrapolated_C={str(L): float(np.mean([r["n_per"] for r in rows if r["L"] == 150]) *
                                                     math.exp(-(ex["a"] + ex["b"] * L))) for L in (100, 150, 200, 300, 500)},
                        note="p at 1/R is the order-statistic floor of an unsaturated census (new-mode rate ~1): the "
                             "best-of-R cluster is hit once by construction, so C_own grows with R itself (moving target)")

    # ---------------- T-ref: best-known energy (all methods) within 20 nats
    dg = json.load(open(os.path.join(HERE, "dg_summary.json")))
    tr = []
    for r in dg["rows"]:
        R = r.get("ms_R"); n_per = r.get("ms_evals_per_restart")
        p = r.get("ms_p_emp_d20")
        ms_cens = (p == 0)
        C_ms = (n_per / p) if p else (n_per * R / 3.0)       # censored: C > R n / 3 (95%)
        dg_hit = r["DG_E1_hit_d20"]
        # portfolio: DG-E1 first (2 descents); on failure, DG draws; on failure, the multistart census
        if dg_hit:
            C_port, port_cens = r["cost_E1"], False
        elif r["DG_D_p_d20"] > 0:
            C_port, port_cens = r["cost_E1"] + r["cost_D"] * 1.0, False
        elif ms_cens and any(x["polishedE"] <= r["E_ref"] + 20 for x in r.get("nrpt", [])):
            # E_ref reached only by NRPT: the portfolio needs an NRPT run (its total evaluations)
            C_port = r["cost_E1"] + r["cost_D"] + min(x["grad"] for x in r["nrpt"] if x["polishedE"] <= r["E_ref"] + 20)
            port_cens = False
        else:
            C_port, port_cens = r["cost_E1"] + r["cost_D"] + C_ms, ms_cens
        tr.append(dict(crop=r["crop"], L=r["L"], C_ms=C_ms, ms_censored=bool(ms_cens), dg_E1_hit=bool(dg_hit),
                       C_DG_E1=r["cost_E1"], C_portfolio=float(C_port), portfolio_censored=bool(port_cens),
                       E_ref_setter=("DG" if r["E_DG_all"] <= r["E_ref"] + 1e-6 else r["other_method"])))
    trL = {}
    for L in sorted({r["L"] for r in tr}):
        rs = [r for r in tr if r["L"] == L]
        trL[str(L)] = dict(n=len(rs), DG_E1_success=int(sum(r["dg_E1_hit"] for r in rs)),
                           ms_success_any=int(sum(not r["ms_censored"] for r in rs)),
                           median_C_ms=float(np.median([r["C_ms"] for r in rs])),
                           frac_C_ms_censored=float(np.mean([r["ms_censored"] for r in rs])),
                           median_C_portfolio=float(np.median([r["C_portfolio"] for r in rs])),
                           max_C_portfolio=float(np.max([r["C_portfolio"] for r in rs])),
                           mean_C_portfolio=float(np.mean([r["C_portfolio"] for r in rs])),
                           E_ref_set_by={m: int(sum(r["E_ref_setter"] == m for r in rs)) for m in ("DG", "census256", "census2048", "nrpt")})
    # power / exponential fit of the portfolio cost (uncensored except where noted)
    yl = [math.log(r["C_portfolio"]) for r in tr]
    Xe = np.c_[np.ones(len(tr)), [r["L"] for r in tr]]; Xp = np.c_[np.ones(len(tr)), np.log([r["L"] for r in tr])]
    be = np.linalg.lstsq(Xe, yl, rcond=None)[0]; bp = np.linalg.lstsq(Xp, yl, rcond=None)[0]
    res["T_ref"] = dict(definition="reach E <= E_ref + 20 (E_ref = lowest energy found by any method on the crop)",
                        rows=tr, per_L=trL,
                        portfolio_fit=dict(exp_rate_per_residue=float(be[1]), power_exponent=float(bp[1])),
                        caveat="E_ref is the best KNOWN energy, not a certified global minimum; 200-iteration endpoints "
                               "are under-relaxed by 0-450 nats (polish_results.json), comparable to many gaps")

    # ---------------- symmetric polish check and fold-level success
    msp = json.load(open(os.path.join(HERE, "ms_polish_results.json")))
    fold = json.load(open(os.path.join(HERE, "ms_polish_fold.json")))
    res["symmetric_polish"] = [dict(crop=r["crop"], L=r["L"], dE_DGpol_minus_MS64pol=r["dE_DGpol_minus_MSpol"],
                                    rmsd_DGpol_vs_MS64pol=r["rmsd_DGpol_vs_MSpol"],
                                    cost_DG_E1_plus_polish=None, cost_MS64_plus_polish=r["cost_ms_restarts"] + r["cost_ms_polish"],
                                    rmsd_DGpol_ORACLE=r["rmsd_DGpol_ORACLE"], rmsd_MSpol_ORACLE=r["rmsd_MSpol_ORACLE"])
                               for r in msp + [f for f in fold if f["crop"] not in {m["crop"] for m in msp}]]
    pol = {r["crop"]: r for r in json.load(open(os.path.join(HERE, "polish_results.json")))}
    dgc = {r["crop"]: r for r in dg["rows"]}
    for s in res["symmetric_polish"]:
        s["cost_DG_E1_plus_polish"] = dgc[s["crop"]]["cost_E1"] + pol[s["crop"]]["extra_evals_DG"]
    tf = []
    for r in fold:
        n_per = r["cost_ms_restarts"] / r["R"]
        best_is_dg = r["dE_DGpol_minus_MSpol"] <= 0
        ref = "fold_frac_vs_DGpol" if best_is_dg else "fold_frac_vs_MSpol"
        for rr in ("3.0", "4.0"):
            p = r[ref][rr]
            tf.append(dict(crop=r["crop"], L=r["L"], radius=float(rr), best_known_fold=("DG" if best_is_dg else "MS64"),
                           p_fold_per_restart=p, C_ms_fold=(n_per / p if p > 0 else None),
                           C_ms_fold_censored_gt=(None if p > 0 else n_per * r["R"] / 3.0),
                           C_DG_fold=(dgc[r["crop"]]["cost_E1"] if best_is_dg else None)))
    res["T_fold"] = dict(definition="land within r = 3 (4) A CA-RMSD of the best-known polished fold", rows=tf)

    # ---------------- T-samp: NRPT decorrelated-sample cost (round trips), right-censored
    ns = []
    for d in ("g1_tscan", "g1_pilot"):
        for f in sorted(glob.glob(os.path.join(REPO, "research", "results", "RAW", d, "*.json"))):
            try:
                r = json.load(open(f))
            except Exception:
                continue
            if "round_trips" not in r:
                continue
            N = r.get("grad_evals_production") or r.get("grad_evals_total")
            k = r["round_trips"]
            if k == 0:
                lo = N / 3.0; est = None
            else:
                lo = N / stats.chi2.ppf(0.975, 2 * (k + 1)) * 2; est = N / k
            ns.append(dict(crop=r["crop"], L=r["L"], T=r["T"], trips=k, N_prod=N, cost_per_trip_lower95=float(lo),
                           cost_per_trip_est=est, src=d))
    res["T_samp"] = dict(definition="one lambda-path NRPT round trip (a decorrelated T-posterior sample)", rows=ns,
                         lower95_by_L={str(L): float(min(x["cost_per_trip_lower95"] for x in ns if x["L"] == L and x["T"] == 1.0))
                                       for L in sorted({x["L"] for x in ns})},
                         note="0 trips at L >= 80 for every T: cost per sample right-censored; no upper bound exists "
                              "for T=1 posterior samples at L >= 80 from any measured method")
    tmp = os.path.join(HERE, "cost_fit.json.tmp")
    json.dump(res, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "cost_fit.json"))
    print("T_own fit:", json.dumps(f256))
    print("T_own per L:", json.dumps(per_L))
    print("T_own extrapolated C:", json.dumps(res["T_own"]["extrapolated_C"]))
    print("moving target:", json.dumps(mt))
    print("T_ref per L:", json.dumps(trL))
    print("T_ref portfolio fit:", json.dumps(res["T_ref"]["portfolio_fit"]))
    print("symmetric polish:", json.dumps(res["symmetric_polish"]))
    print("T_fold:", json.dumps(tf))
    print("T_samp lower95 by L (T=1):", json.dumps(res["T_samp"]["lower95_by_L"]))


if __name__ == "__main__":
    main()
