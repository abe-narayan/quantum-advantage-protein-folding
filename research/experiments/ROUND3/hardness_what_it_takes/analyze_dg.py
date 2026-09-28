"""ROUND3 / hardness_what_it_takes, part (2) analysis: DG seeding vs random-prior multistart vs NRPT on the same crops.

Inputs (read-only): dg_results_A.json (this folder), research/results/RAW/g1_modes (census, 256 restarts),
research/results/RAW/g1_modes2k (2048 restarts), research/results/RAW/g1_tscan + g1_pilot (lambda-path NRPT).
Native structures enter only as ORACLE labels (rmsd_* fields), never in any selection or success criterion.

Success criterion (native-free): an arm "reaches the best-known basin" on a crop if it reaches an energy
E <= E_ref + delta, where E_ref is the lowest energy found on that crop by ANY method in this program (census 256,
census 2048, NRPT polished minima at T = 1..8, the DG arms here).  delta in {5, 20, 50} (energy units = nats at T=1);
delta = 20 is the primary threshold (the census' own coarsest frac_within_dE level).
Cost-to-solution: C = (evaluations per attempt) / p(success per attempt); for 0 successes the cost is right-censored
at > n_attempts * evals_per_attempt (95% Poisson/binomial bound: p < 3/n).
Tail extrapolation for multistart (INFERENCE): lower tail of the per-restart endpoint energies fitted by an
exponential tail (the heavier, multistart-favourable model) and by a normal quantile fit; reported separately.

Also (native-free) basin identity: CA-RMSD between the DG-E1 minimum and NRPT's polished lowest-energy structure on the
crops that have both (the polished structure is recomputed from the stored top-rung samples exactly as
scripts/g1_sample_crop.py does, and checked against the stored polishedE).

Usage: OMP_NUM_THREADS=1 python analyze_dg.py   -> dg_summary.json
"""
from __future__ import annotations

import glob
import json
import math
import os
import sys

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402
from scipy import stats  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
RAW = os.path.join(REPO, "research", "results", "RAW")
sys.path.insert(0, os.path.join(REPO, "src"))
DELTAS = (5.0, 20.0, 50.0)


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def restart_energies(c):
    """Per-restart endpoint energies reconstructed from the census (each restart assigned its cluster
    representative's energy = the lowest energy in its cluster, which favours multistart).  Files written by the
    early census version keep only the lowest 50 clusters: then only the lower tail is known (n_known < R)."""
    E = np.repeat(np.asarray(c["mode_E"], float), np.asarray(c["mode_sizes"], int))
    return np.sort(E), int(c["restarts"])


def tail_prob(Esorted, R, x, k=None):
    """Per-restart P(E <= x) for x below the observed minimum.  Exponential lower-tail (POT) fit on the lowest k
    order statistics, and a normal fit to the lower-tail quantiles.  Returns (p_exp, p_norm)."""
    n = len(Esorted)
    k = k or min(n, 30)
    lo = Esorted[:k]
    if x >= lo[0]:
        return float(np.mean(Esorted <= x) * n / R), float(np.mean(Esorted <= x) * n / R)
    xk = lo[-1]
    beta = max(float(np.mean(xk - lo)), 1e-9)
    p_exp = (k / R) * math.exp(-(xk - x) / beta)
    q = stats.norm.ppf((np.arange(1, k + 1) - 0.5) / R)
    sl, ic = np.polyfit(q, lo, 1)            # lo ~ mu + sigma * q
    p_norm = float(stats.norm.cdf((x - ic) / max(sl, 1e-9)))
    return float(p_exp), p_norm


def nrpt_runs():
    runs = {}
    for d in ("g1_tscan", "g1_pilot"):
        for f in sorted(glob.glob(os.path.join(RAW, d, "*.json"))):
            if f.endswith("governor.jsonl"):
                continue
            try:
                r = json.load(open(f))
            except Exception:
                continue
            if "eval" not in r or "polishedE" not in r.get("eval", {}):
                continue
            runs.setdefault(r["crop"], []).append(dict(file=os.path.relpath(f, REPO), T=r["T"],
                                                       polishedE=r["eval"]["polishedE"],
                                                       rmsd_ORACLE=r["eval"]["lowestE_polished_rmsd"],
                                                       grad=r.get("grad_evals_total"), trips=r.get("round_trips"),
                                                       npz=f[:-5] + ".npz"))
    return runs


def pt_polished_structure(en, npz, L):
    """Recompute NRPT's polished lowest-energy structure from the stored top-rung samples (as g1_sample_crop.py)."""
    from qapf.protein import energy as EN
    z = np.load(npz)
    S = z["samples"]
    S = S[len(S) // 5:]
    E = en(S, grad=False)[0]
    i = int(np.argmin(E))
    xp, ep = EN.relax(en, S[i:i + 1], iters=200)
    return en.coords(xp)[0], float(np.asarray(ep).ravel()[0])


def main():
    dg = json.load(open(os.path.join(HERE, "dg_results_A.json")))
    c256 = {json.load(open(f))["crop"]: json.load(open(f)) for f in glob.glob(os.path.join(RAW, "g1_modes", "*_R256_s0.json"))}
    c2k = {json.load(open(f))["crop"]: json.load(open(f)) for f in glob.glob(os.path.join(RAW, "g1_modes2k", "*_R2048_s1.json"))}
    nr = nrpt_runs()
    rows = []
    for r in dg:
        crop, L = r["crop"], r["L"]
        E = np.asarray(r["E"]); arms = np.asarray(r["arms"]); rm = np.asarray(r["rmsd_native_ORACLE"])
        eE1 = E[arms == "DG-E1"]; eE0 = E[arms == "DG-E0"]; eD = E[arms == "DG-D"]
        other = {}
        if crop in c256:
            other["census256"] = c256[crop]["E_best"]
        if crop in c2k:
            other["census2048"] = c2k[crop]["E_best"]
        if crop in nr:
            other["nrpt"] = min(x["polishedE"] for x in nr[crop])
        E_other = min(other.values()) if other else None
        E_ref = min([E.min()] + list(other.values()))
        row = dict(crop=crop, L=L, E_ref=float(E_ref), E_other_best=E_other,
                   other_method=min(other, key=other.get) if other else None, E_other=other,
                   E_DG_E1=float(eE1.min()), E_DG_E0=float(eE0.min()), E_DG_D=float(eD.min()), E_DG_all=float(E.min()),
                   dE_E1_vs_other=(float(eE1.min() - E_other) if E_other is not None else None),
                   dE_all_vs_other=(float(E.min() - E_other) if E_other is not None else None),
                   cost_E1=r["grad_evals_by_arm"]["DG-E1"], cost_E0=r["grad_evals_by_arm"]["DG-E0"],
                   cost_D=r["grad_evals_by_arm"]["DG-D"], n_D=int((arms == "DG-D").sum()),
                   secs_E1=r["relax_secs_by_arm"]["DG-E1"] + r["embed_secs_by_arm"]["DG-E1"],
                   embed_secs_E1=r["embed_secs_by_arm"]["DG-E1"], confidence=r["confidence"],
                   rmsd_DG_E1_ORACLE=float(rm[arms == "DG-E1"][np.argmin(eE1)]),
                   rmsd_DG_all_ORACLE=float(rm[np.argmin(E)]))
        # multistart (census) per-restart success probability to reach E_ref + delta, empirical and extrapolated
        cen = c2k.get(crop) or c256.get(crop)
        if cen is not None:
            Es, R = restart_energies(cen)
            row["ms_R"] = R
            row["ms_evals_per_restart"] = cen["grad_evals"] / R
            row["rmsd_census_best_ORACLE"] = cen["best_mode_rmsd_native"]
            for d in DELTAS:
                x = E_ref + d
                p_emp = float(np.sum(Es <= x) / R)
                p_exp, p_norm = tail_prob(Es, R, x)
                row[f"ms_p_emp_d{int(d)}"] = p_emp
                row[f"ms_p_tailexp_d{int(d)}"] = p_exp
                row[f"ms_p_tailnorm_d{int(d)}"] = p_norm
        for d in DELTAS:
            x = E_ref + d
            row[f"DG_E1_hit_d{int(d)}"] = bool(eE1.min() <= x)
            row[f"DG_E0_hit_d{int(d)}"] = bool(eE0.min() <= x)
            row[f"DG_D_p_d{int(d)}"] = float(np.mean(eD <= x))
            row[f"DG_any_hit_d{int(d)}"] = bool(E.min() <= x)
            if E_other is not None:
                row[f"DG_E1_le_other_d{int(d)}"] = bool(eE1.min() <= E_other + d)
                row[f"DG_all_le_other_d{int(d)}"] = bool(E.min() <= E_other + d)
        if crop in nr:
            row["nrpt"] = [dict(T=x["T"], polishedE=x["polishedE"], rmsd_ORACLE=x["rmsd_ORACLE"], grad=x["grad"],
                                trips=x["trips"]) for x in nr[crop]]
        rows.append(row)

    # ---- native-free basin identity DG-E1 vs NRPT polished (crops with both)
    from qapf.protein import energy as EN
    for row in rows:
        crop = row["crop"]
        if crop not in nr:
            continue
        z = np.load(os.path.join(REPO, "data", "instruments", "ladder", crop + ".npz"))
        L = row["L"]
        en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
        ep = np.load(os.path.join(HERE, "endpoints", crop + ".npz"))
        arms = ep["arms"]; Ed = ep["E"]
        iE1 = np.where(arms == "DG-E1")[0][np.argmin(Ed[arms == "DG-E1"])]
        Xdg = en.coords(ep["x"][iE1:iE1 + 1])[0]
        Xall = en.coords(ep["x"])
        ident = []
        for x in nr[crop]:
            if not os.path.exists(x["npz"]):
                continue
            Xpt, Epol = pt_polished_structure(en, x["npz"], L)
            ident.append(dict(T=x["T"], polishedE_stored=x["polishedE"], polishedE_recomputed=Epol,
                              rmsd_DGE1_vs_PT=kabsch_rmsd(Xdg, Xpt),
                              min_rmsd_anyDG_vs_PT=float(min(kabsch_rmsd(Xk, Xpt) for Xk in Xall))))
        row["basin_identity_vs_nrpt"] = ident

    # ---- aggregates per L
    agg = {}
    for L in sorted({r["L"] for r in rows}):
        rs = [r for r in rows if r["L"] == L]
        a = dict(n=len(rs))
        for d in DELTAS:
            k = int(d)
            a[f"DG_E1_hit_d{k}"] = int(sum(r[f"DG_E1_hit_d{k}"] for r in rs))
            a[f"DG_any_hit_d{k}"] = int(sum(r[f"DG_any_hit_d{k}"] for r in rs))
            a[f"DG_E1_le_other_d{k}"] = int(sum(r.get(f"DG_E1_le_other_d{k}", False) for r in rs))
            a[f"DG_all_le_other_d{k}"] = int(sum(r.get(f"DG_all_le_other_d{k}", False) for r in rs))
            a[f"DG_D_p_mean_d{k}"] = float(np.mean([r[f"DG_D_p_d{k}"] for r in rs]))
            ms = [r.get(f"ms_p_emp_d{k}") for r in rs if r.get(f"ms_p_emp_d{k}") is not None]
            a[f"ms_p_emp_mean_d{k}"] = float(np.mean(ms)) if ms else None
            a[f"ms_crops_with_any_hit_d{k}"] = int(sum(p > 0 for p in ms))
            te = [r.get(f"ms_p_tailexp_d{k}") for r in rs if r.get(f"ms_p_tailexp_d{k}") is not None]
            tn = [r.get(f"ms_p_tailnorm_d{k}") for r in rs if r.get(f"ms_p_tailnorm_d{k}") is not None]
            # medians (not geometric means): the tail fits degenerate to ~0 when the lowest restarts share one
            # cluster energy (L = 60), which would dominate a geometric mean
            a[f"ms_p_tailexp_median_d{k}"] = float(np.median(te)) if te else None
            a[f"ms_p_tailnorm_median_d{k}"] = float(np.median(tn)) if tn else None
        a["dE_E1_vs_other_median"] = float(np.median([r["dE_E1_vs_other"] for r in rs if r["dE_E1_vs_other"] is not None]))
        a["dE_all_vs_other_median"] = float(np.median([r["dE_all_vs_other"] for r in rs if r["dE_all_vs_other"] is not None]))
        a["cost_E1_mean"] = float(np.mean([r["cost_E1"] for r in rs]))
        a["cost_D_per_seed_mean"] = float(np.mean([r["cost_D"] / r["n_D"] for r in rs]))
        a["ms_evals_per_restart_mean"] = float(np.mean([r["ms_evals_per_restart"] for r in rs if "ms_evals_per_restart" in r]))
        a["secs_E1_mean"] = float(np.mean([r["secs_E1"] for r in rs]))
        # ORACLE transmission labels
        a["rmsd_DG_E1_mean_ORACLE"] = float(np.mean([r["rmsd_DG_E1_ORACLE"] for r in rs]))
        a["rmsd_census_best_mean_ORACLE"] = float(np.mean([r["rmsd_census_best_ORACLE"] for r in rs if "rmsd_census_best_ORACLE" in r]))
        # DG success vs native-free distogram confidence
        x = [r["confidence"]["mean_maxbin"] for r in rs if r["dE_E1_vs_other"] is not None]
        y = [r["dE_E1_vs_other"] for r in rs if r["dE_E1_vs_other"] is not None]
        a["spearman_conf_vs_dE_E1"] = float(stats.spearmanr(x, y).correlation) if len(x) > 3 else None
        agg[str(L)] = a
    # pooled confidence analysis
    x = [r["confidence"]["mean_maxbin"] for r in rows if r["dE_E1_vs_other"] is not None]
    y = [r["dE_E1_vs_other"] / r["L"] for r in rows if r["dE_E1_vs_other"] is not None]
    rmsd = [r["rmsd_DG_E1_ORACLE"] for r in rows if r["dE_E1_vs_other"] is not None]
    sp = stats.spearmanr(x, y)
    sp2 = stats.spearmanr(rmsd, y)
    out = dict(rows=rows, per_L=agg,
               pooled=dict(spearman_conf_vs_dE_per_res=float(sp.correlation), p=float(sp.pvalue),
                           spearman_rmsdORACLE_vs_dE_per_res=float(sp2.correlation), p_rmsd=float(sp2.pvalue),
                           n=len(x)))
    tmp = os.path.join(HERE, "dg_summary.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "dg_summary.json"))
    for L, a in agg.items():
        print(L, json.dumps(a))
    print("pooled", json.dumps(out["pooled"]))
    for r in rows:
        print(r["crop"], "Eref=%.1f other=%s(%s) dE1=%s dAll=%s rmsdE1=%.2f cens=%s" % (
            r["E_ref"], r["other_method"], None if r["E_other_best"] is None else round(r["E_other_best"], 1),
            None if r["dE_E1_vs_other"] is None else round(r["dE_E1_vs_other"], 1),
            None if r["dE_all_vs_other"] is None else round(r["dE_all_vs_other"], 1), r["rmsd_DG_E1_ORACLE"],
            None if "rmsd_census_best_ORACLE" not in r else round(r["rmsd_census_best_ORACLE"], 2)),
            "ms_p20=%s tail=%s/%s" % (r.get("ms_p_emp_d20"), r.get("ms_p_tailexp_d20"), r.get("ms_p_tailnorm_d20")),
            "ident=%s" % [(b["T"], round(b["rmsd_DGE1_vs_PT"], 2), round(b["polishedE_recomputed"] - b["polishedE_stored"], 2))
                          for b in r.get("basin_identity_vs_nrpt", [])])


if __name__ == "__main__":
    main()
