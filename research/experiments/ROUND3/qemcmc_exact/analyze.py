"""ROUND3 lane qemcmc_exact: summarise exact gaps, fit scaling exponents, and cost the quantum step against K-101.

Chain classes (absolute spectral gap, Layden's metric):
  local            single-flip Metropolis
  classical_plain  best of {local, uniform, mix(p), pflip(q)} per instance and T (no global preprocessing)
  classical_best   best of {classical_plain, mean-field independence mixture, ST (exact weights) per-target gap = joint gap / K}
                   (conservative for classical: the ST joint gap is divided by the number of rungs)
  classical_joint  as classical_best but ST counted at its joint gap (generous to classical)
  q_layden         Layden protocol: Q averaged over gamma in [0.25, 0.6] x t in [2, 20] (grid points), best of raw/clip H_E
  q_tuned          best single (gamma, t) on the grid per instance and T, best of raw/clip  (oracle-tuned: favourable to quantum)
Scaling: <delta> ∝ 2^{-k n}, fitted to the geometric mean over instances (arithmetic mean also reported), n = 6..nmax.
Super-quadratic over classical iff k_q < k_c / 2 (equivalently alpha = log delta_q / log delta_c < 1/2).
Writes summary.json.
"""
from __future__ import annotations

import glob
import json
import math
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TS = ("1.0", "2.0", "4.0")

# ---- K-101 cost constants (research/theory/BREAK_EVEN.md; T3 RESOURCE_MODELS) ----
G_PER_L2 = 3.0e4          # Toffolis per coherent A80 energy evaluation / L^2 (T3 central, D2)
G_PER_L2_OPT = 1.0e3      # hypothetical 30x-cheaper discrete-instance oracle (optimistic sensitivity)
T_TOF = 1e-6              # s per logical Toffoli (K-101 "most optimistic")
C_CLASSICAL = 2.3e-3      # s per classical E-only evaluation at L = 30 (MEASURED here, one core, under load)
DT_TROTTER = 0.8          # Layden hardware Trotter step (normalised units)
L_CROP = 30


def chain_values(rec, T):
    c = rec["classical"][T]
    loc = c["local"]["abs"]
    plain = max([loc, c["uniform"]["abs"]] + [v["abs"] for v in c["mix"].values()] +
                [v["abs"] for v in c["pflip"].values()])
    st_pt = max(v["per_target"] for v in c["ST"].values())
    st_j = max(v["abs"] for v in c["ST"].values())
    best = max(plain, c["mf"]["abs"], st_pt)
    joint = max(plain, c["mf"]["abs"], st_j)
    q = rec["quantum"]
    q_tuned = max(q[m][T]["best"] for m in q)
    q_raw = q["raw"][T]["best"]
    q_lay = max(q[m][T].get("avg_layden", q[m][T]["avg_grid"]) for m in q)
    arg = max(((q[m][T]["best"], m, q[m][T]["arg"]) for m in q))
    return dict(local=loc, local_censored=c["local"].get("censored", False), plain=plain, st_pt=st_pt, st_joint=st_j,
                best=best, joint=joint, q_tuned=q_tuned, q_raw=q_raw, q_layden=q_lay, q_arg=f"{arg[1]}:{arg[2]}",
                uniform=c["uniform"]["abs"],
                pflip_best=max(v["abs"] for v in c["pflip"].values()))


def fit_k(ns, vals):
    ns = np.asarray(ns, float); y = np.log2(np.asarray(vals, float))
    if len(ns) < 3:
        return None
    p = np.polyfit(ns, y, 1)
    return float(-p[0])


def main():
    allrecs = [json.load(open(f)) for f in glob.glob(os.path.join(HERE, "results", "*.json"))]
    # one record per (base tag, n): the COARSE-grid record (same (gamma,t) grid at every n); fine-grid records
    # (n <= 8) are kept only for the tuning-penalty diagnostic.
    prim, fine = {}, {}
    for r in allrecs:
        base = r["tag"].replace("_cg", "")
        r["tag"] = base
        (prim if r["grid"] == "coarse" else fine)[(base, r["n"])] = r
    penalty = []
    for key, rf in fine.items():
        if key in prim:
            for T in TS:
                a = max(rf["quantum"][m][T]["best"] for m in rf["quantum"])
                b = max(prim[key]["quantum"][m][T]["best"] for m in prim[key]["quantum"])
                penalty.append(a / b)
    for key, rf in fine.items():
        if key not in prim:
            prim[key] = rf          # fallback (flagged by grid field)
    recs = list(prim.values())
    fam = defaultdict(lambda: defaultdict(list))        # family -> n -> [(rec)]
    for r in recs:
        if r["tag"].startswith("SK_"):
            key = "SK"
        else:
            m = r["meta"]
            key = f"{m['variant']}_alph{m['alph']}" + ("_b10" if m.get("nbits", 12) == 10 else "")
        fam[key][r["n"]].append(r)
    out = dict(families={}, fine_over_coarse_q_tuned=dict(n=len(penalty), median=float(np.median(penalty)) if penalty else None,
                                                          max=float(np.max(penalty)) if penalty else None),
               grids_used=sorted({r["grid"] for r in recs}))
    chains = ("local", "plain", "best", "joint", "q_layden", "q_tuned", "q_raw")
    for key, byn in sorted(fam.items()):
        F = {}
        for T in TS:
            ns = sorted(byn)
            table = {}
            for n in ns:
                vals = [chain_values(r, T) for r in byn[n]]
                row = {"count": len(vals)}
                for ch in chains:
                    arr = np.array([v[ch] for v in vals])
                    arr = np.maximum(arr, 1e-300)
                    row[ch + "_gmean"] = float(np.exp(np.mean(np.log(arr))))
                    row[ch + "_mean"] = float(np.mean(arr))
                row["local_censored"] = int(sum(v["local_censored"] for v in vals))
                # per-instance exponent alpha: delta_q = delta_c^alpha
                al = [math.log(v["q_tuned"]) / math.log(v["best"]) for v in vals if v["best"] < 0.5]
                al_l = [math.log(v["q_layden"]) / math.log(v["best"]) for v in vals if v["best"] < 0.5]
                row["alpha_tuned_vs_best"] = al
                row["alpha_layden_vs_best"] = al_l
                row["ratio_q_tuned_over_best"] = [v["q_tuned"] / v["best"] for v in vals]
                row["ratio_q_tuned_over_sqrt_best"] = [v["q_tuned"] / math.sqrt(v["best"]) for v in vals]
                row["q_args"] = [v["q_arg"] for v in vals]
                table[str(n)] = row
            # fits over n with >= 2 instances (all n for SK)
            maxc = max(len(byn[n]) for n in ns)
            nfit = [n for n in ns if len(byn[n]) == maxc]      # only n covered by every instance
            fits = {}
            # per-instance slopes over nfit
            per_tag = defaultdict(dict)
            for tg in sorted({r["tag"] for n in nfit for r in byn[n]}):
                for ch in ("best", "plain", "q_tuned", "q_layden", "local"):
                    ys = [chain_values(r, T)[ch] for n in nfit for r in byn[n] if r["tag"] == tg]
                    if len(ys) == len(nfit):
                        per_tag[tg][ch] = fit_k(nfit, np.maximum(ys, 1e-300))
            ratio_tags = [v["q_tuned"] / v["best"] for v in per_tag.values() if v.get("best") and v["best"] > 0.05]
            ratio_tags_L = [v["q_layden"] / v["best"] for v in per_tag.values() if v.get("best") and v["best"] > 0.05]
            fits["per_instance"] = dict(k=per_tag, kq_over_kc_tuned=ratio_tags, kq_over_kc_layden=ratio_tags_L,
                                        frac_superquadratic_tuned=float(np.mean(np.array(ratio_tags) < 0.5)) if ratio_tags else None,
                                        frac_superquadratic_layden=float(np.mean(np.array(ratio_tags_L) < 0.5)) if ratio_tags_L else None)
            for ch in chains:
                fits[ch] = dict(k_gmean=fit_k(nfit, [table[str(n)][ch + "_gmean"] for n in nfit]),
                                k_mean=fit_k(nfit, [table[str(n)][ch + "_mean"] for n in nfit]))
            # bootstrap over instances (tags) for k(q_tuned) and k(best)
            tags = sorted({r["tag"] for n in ns for r in byn[n]})
            rng = np.random.default_rng(0)
            bs = defaultdict(list)
            if len(tags) >= 3:
                for _ in range(400):
                    pick = list(rng.choice(tags, len(tags), replace=True))
                    for ch in ("best", "plain", "q_tuned", "q_layden", "local"):
                        ys = []
                        okn = []
                        for n in nfit:
                            v = [chain_values(r, T)[ch] for t in pick for r in byn[n] if r["tag"] == t]
                            if v:
                                ys.append(float(np.exp(np.mean(np.log(np.maximum(v, 1e-300))))))
                                okn.append(n)
                        k = fit_k(okn, ys)
                        if k is not None:
                            bs[ch].append(k)
                for ch, v in bs.items():
                    fits[ch]["k_gmean_ci90"] = [float(np.percentile(v, 5)), float(np.percentile(v, 95))]
                dk = []
            F[T] = dict(table=table, fits=fits, ns=nfit)
        out["families"][key] = F
    # ---- K-101 costing of the quantum step ----
    G = G_PER_L2 * L_CROP ** 2
    cost = {}
    for label, g in (("central", G), ("optimistic_oracle", G_PER_L2_OPT * L_CROP ** 2)):
        for r_steps in (1, 3, 10, 25):
            cq = 2 * r_steps * g * T_TOF + C_CLASSICAL
            cost[f"{label}_r{r_steps}"] = dict(G_toffoli=g, trotter_steps=r_steps, quantum_step_s=cq,
                                              classical_step_s=C_CLASSICAL, breakeven_gap_ratio=cq / C_CLASSICAL)
    out["cost_model"] = cost
    # extrapolated break-even n* and quantum wall-clock per sample, from fitted k (geometric-mean fits)
    ext = {}
    for key, F in out["families"].items():
        for T in TS:
            f = F[T]["fits"]; tab = F[T]["table"]; ns = F[T]["ns"]
            kq, kc = f["q_tuned"]["k_gmean"], f["best"]["k_gmean"]
            if kq is None or kc is None:
                continue
            nmax = str(max(ns))
            ratio0 = tab[nmax]["q_tuned_gmean"] / tab[nmax]["best_gmean"]
            d = dict(k_q=kq, k_c=kc, super_quadratic=bool(kq < kc / 2), ratio_at_nmax=ratio0, nmax=int(nmax))
            for lab, cm in cost.items():
                R = cm["breakeven_gap_ratio"]
                if kc > kq and ratio0 < R:
                    dn = math.log2(R / ratio0) / (kc - kq)
                    nstar = int(nmax) + dn
                    dq = tab[nmax]["q_tuned_gmean"] * 2 ** (-kq * dn)
                    d[lab] = dict(n_star=nstar, quantum_s_per_relaxation=cm["quantum_step_s"] / dq,
                                  classical_s_per_relaxation=C_CLASSICAL / (tab[nmax]["best_gmean"] * 2 ** (-kc * dn)))
                elif ratio0 >= R:
                    d[lab] = dict(n_star=int(nmax), note="already past break-even")
                else:
                    d[lab] = dict(n_star=None, note="k_q >= k_c: never")
            ext[f"{key}_T{T}"] = d
    out["breakeven_extrapolation"] = ext
    tmp = os.path.join(HERE, "summary.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "summary.json"))
    # console digest
    for key, F in out["families"].items():
        for T in TS:
            f = F[T]["fits"]
            pi = f["per_instance"]
            s = f"kq/kc(tuned) med={np.median(pi['kq_over_kc_tuned']) if pi['kq_over_kc_tuned'] else float('nan'):.2f} superq_frac={pi['frac_superquadratic_tuned']} (layden med={np.median(pi['kq_over_kc_layden']) if pi['kq_over_kc_layden'] else float('nan'):.2f}) | " + " ".join(f"{ch}={f[ch]['k_gmean']:.3f}" + (f"[{f[ch]['k_gmean_ci90'][0]:.2f},{f[ch]['k_gmean_ci90'][1]:.2f}]" if 'k_gmean_ci90' in f[ch] else "")
                         for ch in chains if f[ch]["k_gmean"] is not None)
            print(f"{key:22s} T={T} n={F[T]['ns']}  k: {s}")
        for T in TS:
            tab = F[T]["table"]
            print("   T", T, " ".join(f"n{n}:best={tab[n]['best_gmean']:.2e}/q={tab[n]['q_tuned_gmean']:.2e}/qL={tab[n]['q_layden_gmean']:.2e}/loc={tab[n]['local_gmean']:.1e}" for n in sorted(tab, key=int)))


if __name__ == "__main__":
    main()
