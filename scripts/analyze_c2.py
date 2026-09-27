"""Analyse C2 (PREREG_G1_C1_Q4.md): classical cost of sparse Pauli dynamics vs cluster size N.

For each (probe, gamma, N): reference = sector-exact if stored, else the smallest completed (uncapped, full-length) eps
run, accepted only if it agrees with the next-smallest completed run to < sigma/3 over the window (else "unconverged").
M*(N, t) = peak string count of the LARGEST eps whose bias stays < sigma for all recorded times <= t.  Censored
(lower bound) when no run is accurate.  The pre-registered window is t_50 (half of the exact per-parameter FI accrued,
from the C1 job at the same probe/gamma, N=10 by default).  Fits ln M* = a + kappa N  vs  ln M* = a + k ln N (Gaussian
residuals, BIC) and extrapolates to N = 60.  Writes research/results/PROCESSED/c2_summary.json.
"""
from __future__ import annotations

import glob
import json
import math
import os
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research", "results", "RAW")


def t50_index(probe, gamma, obs="S"):
    """median over params of the time index by which half of the exact FI (transfer) has accrued (C1, N=10)."""
    for N in (10, 12, 14):
        f = os.path.join(RAW, "nmr_gate", f"1UBQ_p{probe}_N{N}_o0_g{int(gamma)}.json")
        if os.path.exists(f):
            r = json.load(open(f))
            idx = []
            key = "FI_otoc_t" if obs.startswith("F") else "FI_t"
            for p in r["params"]:
                if key not in p:
                    continue
                c = np.cumsum(p[key]) / max(sum(p[key]), 1e-30)
                idx.append(int(np.searchsorted(c, 0.5)))
            if idx:
                return int(np.median(idx)), N
    return 8, None


ALPHA = {}          # calibrated mixing weight per (probe, gamma), fitted on N = 8 exact data (see calibrate_alpha)


def f_alpha(x, alpha):
    """alpha-mixture OTOC estimator: F_plain + alpha (1 - N_k) F_plain / N_k  (alpha = 0: plain; 1: norm-corrected)."""
    nk = np.maximum(np.asarray(x["kept_norm2"], float), 1e-12)
    return {b: np.asarray(u, float) + alpha * (1 - nk[:len(u)]) * np.asarray(u, float) / nk[:len(u)] for b, u in x["F"].items()}


def calibrate_alpha(r):
    """least-squares alpha on an exact-referenced job (all eps runs, all times)."""
    ex = r.get("exact") or {}
    if not ex.get("F"):
        return None
    num = den = 0.0
    for x in r["runs"]:
        if "F" not in x:
            continue
        nk = np.maximum(np.asarray(x["kept_norm2"], float), 1e-12)
        for b, u in x["F"].items():
            u = np.asarray(u, float); n = len(u)
            e = np.asarray(ex["F"][b])[:n]
            d = (1 - nk[:n]) * u / nk[:n]
            num += float((d * (e - u)).sum()); den += float((d * d).sum())
    return num / den if den > 0 else None


def job_summary(r, t50, obs="S", normcorr=False):
    """obs = 'S' (transfer), 'F' (OTOC) or 'Fa' (alpha-calibrated OTOC).  normcorr: divide the truncated OTOC by the
    kept norm (gamma = 0)."""
    sig = r["sigma"]
    key = "F" if obs == "Fa" else obs
    runs = [x for x in r["runs"] if key in x]

    def series(x):
        if obs == "Fa":
            return f_alpha(x, ALPHA.get((r["probe"], r["gamma"]), 0.0))
        v = {b: np.asarray(u, float) for b, u in x[key].items()}
        if obs == "F" and normcorr:
            nk = np.maximum(np.asarray(x["kept_norm2"], float), 1e-12)
            v = {b: u / nk[:len(u)] for b, u in v.items()}
        return v
    ref, ref_kind = None, None
    ex = r.get("exact")
    if ex and ex.get(key):
        ref = {b: np.asarray(v) for b, v in ex[key].items()}
        ref_kind = "exact"
    else:
        done = [x for x in runs if not x.get("capped") and x.get("steps_done", 0) >= r["steps"]]
        if len(done) >= 2:
            a_, b_ = series(done[-1]), series(done[-2])
            diff = max(np.max(np.abs(a_[b] - b_[b])) for b in a_)
            if diff < sig / 3:
                ref = a_
                ref_kind = f"eps{done[-1]['eps']:g} (conv. diff {diff:.4f})"
            else:
                ref_kind = f"unconverged (diff {diff:.4f})"
        else:
            ref_kind = "none"
    rows = []
    for x in runs:
        v = series(x)
        n = len(x["times"])
        if ref is not None:
            bias = np.max(np.stack([np.abs(v[b] - ref[b][:n]) for b in ref]), 0)
            ok = np.nonzero(bias > sig)[0]
            t_ok = int(ok[0]) if len(ok) else n
        else:
            bias, t_ok = None, None
        rows.append(dict(eps=x["eps"], peak=x.get("peak_strings"), capped=x.get("capped"), steps_done=x.get("steps_done"),
                         secs=x.get("secs"), t_ok=t_ok, max_bias=(float(bias.max()) if bias is not None else None)))
    acc = [y for y in rows if y["t_ok"] is not None and y["t_ok"] > t50]
    if acc:
        best = max(acc, key=lambda y: y["eps"])
        Mstar, cens = best["peak"], False
    else:
        Mstar = max([y["peak"] or 0 for y in rows] + [1])
        cens = True
    return dict(ref=ref_kind, runs=rows, Mstar=Mstar, censored=cens)


def fit(Ns, Ms):
    Ns = np.asarray(Ns, float); y = np.log(np.asarray(Ms, float))
    out = {}
    for name, X in (("exp", Ns), ("power", np.log(Ns))):
        A = np.vstack([np.ones_like(X), X]).T
        coef, *_ = np.linalg.lstsq(A, y, rcond=None)
        res = y - A @ coef
        n = len(y)
        s2 = max(float(res @ res) / n, 1e-12)
        bic = n * math.log(s2) + 2 * math.log(n)
        pred60 = float(coef[0] + coef[1] * (60 if name == "exp" else math.log(60)))
        out[name] = dict(a=float(coef[0]), slope=float(coef[1]), bic=bic, log10_M60=pred60 / math.log(10))
    out["dBIC_power_minus_exp"] = out["power"]["bic"] - out["exp"]["bic"]
    return out


def main():
    by = defaultdict(dict)
    files = sorted(glob.glob(os.path.join(RAW, "nmr_sparse", "*.json")))
    for f in files:                                      # alpha calibration on the N = 8 exact jobs
        r = json.load(open(f))
        if r["N"] == 8:
            al = calibrate_alpha(r)
            if al is not None:
                ALPHA[(r["probe"], r["gamma"])] = float(np.clip(al, 0.0, 1.0))
    print("alpha (N=8 calibration):", ALPHA)
    for f in files:
        r = json.load(open(f))
        for obs, nc in (("S", False), ("F", False), ("F", True), ("Fa", False)):
            if not any(("F" if obs == "Fa" else obs) in x for x in r["runs"]):
                continue
            t50, src = t50_index(r["probe"], r["gamma"], obs)
            s = job_summary(r, t50, obs, nc)
            s.update(t50=t50, t50_src_N=src)
            by[(r["probe"], r["gamma"], obs + ("_normcorr" if nc else ""))][r["N"]] = s
    out = {}
    for (p, g, obs), d in sorted(by.items()):
        Ns = sorted(d)
        key = f"p{p}_g{int(g)}_{obs}"
        out[key] = dict(per_N={str(N): d[N] for N in Ns})
        unc = [N for N in Ns if not d[N]["censored"]]
        if len(unc) >= 3:
            out[key]["fit_uncensored"] = fit(unc, [d[N]["Mstar"] for N in unc])
        print(key)
        for N in Ns:
            x = d[N]
            print(f"   N={N:2d} ref={x['ref']:28s} t50={x['t50']} M*={x['Mstar']:>9} {'(>= censored)' if x['censored'] else ''} "
                  + " ".join(f"[eps {y['eps']:g}: peak {y['peak']}, t_ok {y['t_ok']}, {'CAP' if y['capped'] else ''}{'' if (y['steps_done'] or 0) >= 160 else 'TRUNC'}]" for y in x["runs"]))
        if "fit_uncensored" in out[key]:
            fr = out[key]["fit_uncensored"]
            print(f"   fit: exp slope {fr['exp']['slope']:.3f}/spin (log10 M*(60) = {fr['exp']['log10_M60']:.1f}); "
                  f"power k = {fr['power']['slope']:.2f} (log10 M*(60) = {fr['power']['log10_M60']:.1f}); "
                  f"BIC(power) - BIC(exp) = {fr['dBIC_power_minus_exp']:.1f}")
    os.makedirs(os.path.join(ROOT, "research", "results", "PROCESSED"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "research", "results", "PROCESSED", "c2_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
