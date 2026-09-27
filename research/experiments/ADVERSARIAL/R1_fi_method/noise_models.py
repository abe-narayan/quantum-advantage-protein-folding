"""R1_fi_method / test NOISE: is the constant-sigma white-noise model what makes the echo window valuable?
Zero-cost reanalysis of every gamma = 0 C1 job with echo FI (research/results/RAW/nmr_gate/*_g0.json, nmr_gate_hn/*.json).

Physical echo measurement: the echo requires reversing the dipolar evolution.  The reversal is imperfect and the measured
echo is A(t) F(t) + noise(sigma), where A(t) is the Loschmidt-echo attenuation.  LITERATURE (arXiv:2112.00607, Sanchez,
Chattah, Pastawski, PRA 105, 052232 (2022), abstract verified 2026-09-27): in the reversible-dominated regime the NMR
Loschmidt echo decays within T3 ~ T2 / R, R = 0.15 +- 0.01, i.e. T3 ~ 6.7 T2 (T2 = time scale of the reversed dipolar
interaction), independent of the perturbation.  The analyst normalises by the measured Loschmidt echo (Z_b -> 1):
R = (A F + n1) / (A + n2)  ->  sd(R) = (sigma / A) sqrt(1 + F^2)  (gamma = 0, so the ideal L = 1).
Models (echo only; the transfer S keeps constant sigma, which favours neither side in the S-vs-F comparison and is
generous to the classical S baseline):
  M0          constant sigma (the gate; reproduces the stored f_hard and gain)
  EXP(T3)     sd_F(t) = sigma / exp(-t/T3)
  GAU(T3)     sd_F(t) = sigma / exp(-(t/T3)^2)
  RATIO(T3)   sd_F(t) = sigma sqrt(1 + F_b(t)^2) / exp(-t/T3)        (per observed spin b)
For each model the classical failure time is recomputed with the noise-aware threshold bias > sigma / A(t) (the smaller,
b-independent threshold, which is conservative in favour of the quantum claim), taking the latest failure over the stored
adversaries (plain and norm-corrected); f_hard, gain = FI_tot/FI_easy, and the JOINT gain (S all + F all)/(S easy + F easy)
(the classical analyst also has the classically-exact transfer data) are reported per parameter; medians over
(job, unique parameter).  T3 grid in microseconds.  C3 kill threshold: median f_hard^OTOC < 0.3.
"""
from __future__ import annotations

import glob
import json
import os

import numpy as np

from fi_common import RAW, dump

SIG = 0.01
T3S = [None, 3000, 1000, 500, 300, 200, 130, 100, 70, 50, 30]


def load_jobs():
    out = []
    for f in sorted(glob.glob(os.path.join(RAW, "nmr_gate", "*_g0.json")) + glob.glob(os.path.join(RAW, "nmr_gate_hn", "*.json"))):
        r = json.load(open(f))
        if r.get("version") != 2 or not r.get("F_exact"):
            continue
        if not any("FI_otoc_t" in p for p in r["params"]):
            continue
        out.append((os.path.basename(f), r))
    return out


def unique(r):
    ps, seen = [], []
    for p in r["params"]:
        if "dF" not in p:
            continue
        v = np.concatenate([np.asarray(p["dF"][b]) for b in sorted(p["dF"])])
        if any(np.allclose(v, w, rtol=1e-9, atol=1e-12) for w in seen):
            continue
        seen.append(v); ps.append(p)
    return ps


def c2_eps3e5_bias(r):
    """echo bias of the C2 eps = 3e-5 sparse run when the C2 job has the same cluster (1UBQ p19/p245, N=10, dense)."""
    tag = f"{r['pdb']}_p{r['probe']}_N{r['N']}_o{r['orient']}_g0.json"
    f = os.path.join(RAW, "nmr_sparse", tag)
    if not os.path.exists(f) or r["dt"] != 2e-6:
        return None
    c = json.load(open(f))
    if c["bs"] != r["bs"]:
        return None
    for x in c["runs"]:
        if abs(x["eps"] - 3e-5) < 1e-12:
            n = len(x["times"])
            return np.max([np.abs(np.asarray(x["F"][str(b)]) - np.asarray(r["F_exact"][str(b)])[:n]) for b in r["bs"]], 0)
    return None


def analyse(model, T3, jobs, include_c2=False):
    rows = []
    for name, r in jobs:
        t = np.asarray(r["times"]) * 1e6
        if T3 is None:
            A = np.ones_like(t)
        elif model == "GAU":
            A = np.exp(-(t / T3) ** 2)
        else:
            A = np.exp(-t / T3)
        A = np.maximum(A, 1e-300)
        thr = SIG / A
        # classical failure time for the echo (latest over adversaries; plain and norm-corrected biases)
        tcs = {}
        for k, v in r["adversaries"].items():
            cands = []
            for key in ("max_bias_otoc", "max_bias_otoc_normcorr"):
                if key in v:
                    bo = np.asarray(v[key])
                    bad = np.nonzero(bo > thr[:len(bo)])[0]
                    cands.append(int(bad[0]) if len(bad) else len(t))
            if cands:
                tcs[k] = max(cands)
        if include_c2:
            b5 = c2_eps3e5_bias(r)
            if b5 is not None:
                bad = np.nonzero(b5 > thr)[0]
                tcs["c2_eps3e-05"] = int(bad[0]) if len(bad) else len(t)
        if not tcs:
            continue
        best = max(tcs, key=tcs.get); tco = tcs[best]
        tcS = r.get("best_t_c_index", len(t))
        Fex = {b: np.asarray(r["F_exact"][b]) for b in r["F_exact"]}
        for p in unique(r):
            fiS = np.asarray(p["FI_t"])
            if model == "RATIO" and T3 is not None or model == "RATIO":
                fiF = sum((np.asarray(p["dF"][b]) * A / np.sqrt(1 + Fex[b] ** 2)) ** 2 for b in p["dF"]) / SIG ** 2
            else:
                fiF = sum((np.asarray(p["dF"][b]) * A) ** 2 for b in p["dF"]) / SIG ** 2
            totF, easyF = fiF.sum(), fiF[:tco].sum()
            totS, easyS = fiS.sum(), fiS[:tcS].sum()
            rows.append(dict(job=name, param=p["name"], tcF=tco, tcF_us=float(t[tco]) if tco < len(t) else None, best=best,
                             frac_hard=float(1 - easyF / max(totF, 1e-300)), gain=float(totF / max(easyF, 1e-300)),
                             gain_joint=float((totS + totF) / max(easyS + easyF, 1e-300)),
                             FI_F=float(totF), FI_S=float(totS), ratio_FI_F_over_S=float(totF / max(totS, 1e-300)),
                             hn=("HN" in name)))
    return rows


def summarise(rows):
    def med(k, sel=lambda z: True):
        v = [z[k] for z in rows if sel(z)]
        return float(np.median(v)) if v else None
    return dict(n=len(rows), median_frac_hard=med("frac_hard"), median_gain=med("gain"), median_gain_joint=med("gain_joint"),
                median_ratio_FI_F_over_S=med("ratio_FI_F_over_S"),
                dense=dict(median_frac_hard=med("frac_hard", lambda z: not z["hn"]), median_gain_joint=med("gain_joint", lambda z: not z["hn"]),
                           median_ratio_FI_F_over_S=med("ratio_FI_F_over_S", lambda z: not z["hn"])),
                hn=dict(median_frac_hard=med("frac_hard", lambda z: z["hn"]), median_gain_joint=med("gain_joint", lambda z: z["hn"]),
                        median_ratio_FI_F_over_S=med("ratio_FI_F_over_S", lambda z: z["hn"])),
                min_frac_hard=float(min(z["frac_hard"] for z in rows)), max_frac_hard=float(max(z["frac_hard"] for z in rows)))


def main():
    jobs = load_jobs()
    print("jobs:", [n for n, _ in jobs])
    res = dict(jobs=[n for n, _ in jobs], T3_grid_us=T3S, models={})
    for inc in (False, True):
        for model in ("EXP", "GAU", "RATIO"):
            for T3 in T3S:
                if T3 is None and model != "EXP" and model != "RATIO":
                    continue
                rows = analyse(model, T3, jobs, include_c2=inc)
                s = summarise(rows)
                key = f"{model}_T3={T3}{'_withC2eps3e-5' if inc else ''}"
                res["models"][key] = dict(summary=s, rows=rows)
                print(f"{key:34s} n={s['n']:2d} f_hard med {s['median_frac_hard']:.3f} (dense {s['dense']['median_frac_hard']:.3f}, "
                      f"HN {s['hn']['median_frac_hard']:.3f})  gain med {s['median_gain']:.2f}  joint gain med {s['median_gain_joint']:.2f} "
                      f"(dense {s['dense']['median_gain_joint']:.2f}, HN {s['hn']['median_gain_joint']:.2f})  FI_F/FI_S med {s['median_ratio_FI_F_over_S']:.1f}")
    print("wrote", dump(res, "noise_models.json"))


if __name__ == "__main__":
    main()
