"""Score every R1-SIM polynomial adversary in this lane against the exact typicality echoes (N = 12..18).

Metric (lane kill rule): max over b in bs and t in [80, 320] us of |F_method - F_exact|; pass iff <= sigma = 0.01 on
BOTH probes at N = 16 AND 18.  Reference noise: single typicality vector, err ~ 2^{-N/2} (0.0039 at N=16, 0.002 at
N=18).  Method statistical error: reported SE (max over b,t in the window).
Also evaluates zero-compute adversaries built from existing data (hybrid_echo.py outputs + exact cone):
  Z2  F_hyb(N) + [F_exact(N-2) - F_hyb(N-2)]         (exact-difference correction, one rung down)
  Z3  F_hyb(Nc=12) + 2 [F_hyb(Nc=12) - F_hyb(Nc=10)]  (linear extrapolation in core size to Nc = Ntot = 16)
  Z4  F_exact(N-2) (plain smaller exact cluster) and 2 F_exact(N-2) - F_exact(N-4) (linear-in-N extrapolation)
Writes summary.json.
"""
from __future__ import annotations

import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REF = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
HYB = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1SIM_hybrid", "out")
SIG = 0.01
WIN = (80.0, 320.0)


def ref(p, N):
    f = os.path.join(REF, f"1UBQ_p{p}_N{N}.json")
    if not os.path.exists(f):
        return None
    d = json.load(open(f))
    return {round(t): {b: d["F"][b][i] for b in d["F"]} for i, t in enumerate(d["times_us"])}


def hyb(p, Nc, Ntot):
    f = os.path.join(HYB, f"1UBQ_p{p}_Nc{Nc}_Ntot{Ntot}.json")
    if not os.path.exists(f):
        return None
    d = json.load(open(f))
    return {round(t): {b: d["F"][b][i] for b in d["F"]} for i, t in enumerate(d["times_us"])}


def score(est, exact, se=None):
    """est/exact: {t: {b: F}}; returns max abs err in window, per-time max err, max se."""
    errs, pert = [], {}
    for t in sorted(exact):
        if not (WIN[0] - 1e-6 <= t <= WIN[1] + 1e-6) or t not in est:
            continue
        e = max(abs(est[t][b] - exact[t][b]) for b in exact[t])
        pert[t] = round(e, 4)
        errs.append(e)
    if not errs:
        return None
    out = dict(max_err=round(max(errs), 4), err_by_t=pert, n_t=len(errs))
    if se is not None:
        out["max_se"] = round(max(se[t][b] for t in pert for b in se[t]), 4)
    return out


def load_runs():
    rows = []
    for f in sorted(glob.glob(os.path.join(HERE, "out", "*.json"))):
        if f.endswith(".ckpt.json"):
            continue
        d = json.load(open(f))
        for est in ("F_tdh", "F_core"):
            F, S = {}, {}
            for k, t in zip(d["ks"], d["times_us"]):
                r = d["res"][str(k)][est]
                F[round(t)] = {b: v[0] for b, v in r.items()}
                S[round(t)] = {b: v[1] for b, v in r.items()}
            rows.append(dict(file=os.path.basename(f), probe=d["probe"], N=d["N"], core=d["core"], bath=d["bath"],
                             ba=d["ba"], M=d["M"], est=est, sizes=d["group_sizes"], secs=round(d["secs_total"], 1),
                             F=F, SE=S))
    return rows


def main():
    summ = dict(sigma=SIG, window_us=WIN, runs=[], zero_compute=[])
    for r in load_runs():
        ex = ref(r["probe"], r["N"])
        if ex is None:
            continue
        sc = score(r["F"], ex, r["SE"])
        if sc is None:
            continue
        summ["runs"].append(dict({k: r[k] for k in ("file", "probe", "N", "core", "bath", "ba", "M", "est", "sizes",
                                                    "secs")}, **sc,
                                 F_est={t: {b: round(v, 4) for b, v in r["F"][t].items()} for t in r["F"]}))
    # CCE with hybrid base (cce_hybrid.py)
    summ["cce"] = []
    for f in sorted(glob.glob(os.path.join(HERE, "out_cce", "*.json"))):
        if f.endswith(".ckpt.json"):
            continue
        d = json.load(open(f))
        ex = ref(d["probe"], d["N"])
        for name, e in d["est"].items():
            if not e:
                continue
            F, S = {}, {}
            for kb, v in e.items():
                k, b = kb.split("_")
                t = round(int(k) * 2.0)
                F.setdefault(t, {})[b] = v[0]
                S.setdefault(t, {})[b] = v[1] if v[1] == v[1] else 0.0
            sc = score(F, ex, S)
            if sc is None:
                continue
            sgn = [F[t][b] - ex[t][b] for t in F if WIN[0] <= t <= WIN[1] for b in F[t]]
            summ["cce"].append(dict(file=os.path.basename(f), probe=d["probe"], N=d["N"], base=d["base"],
                                    est=name, M=d["M"], n_subruns=d["n_subruns"], n_pairs=d["n_pairs"],
                                    cpu_secs=round(d["cpu_secs"], 1), max_core=d["max_core"],
                                    mean_signed=round(float(np.mean(sgn)), 4), **sc))
    # zero-compute adversaries from existing data
    for p in (19, 245):
        for N in (16, 18):
            ex = ref(p, N)
            h = hyb(p, 10, N)
            if h is not None:
                summ["zero_compute"].append(dict(method="Z1 hybrid Nc10 (existing)", probe=p, N=N, **score(h, ex)))
            hm, em = hyb(p, 10, N - 2), ref(p, N - 2)
            if h is not None and hm is not None and em is not None:
                est = {t: {b: h[t][b] + em[t][b] - hm[t][b] for b in h[t]} for t in h if t in em and t in hm}
                summ["zero_compute"].append(dict(method="Z2 hybrid + exact(N-2)-hybrid(N-2)", probe=p, N=N,
                                                 **score(est, ex)))
            h12 = hyb(p, 12, N)
            if h is not None and h12 is not None:
                est = {t: {b: h12[t][b] + (N - 12) / 2 * (h12[t][b] - h[t][b]) for b in h[t]} for t in h if t in h12}
                summ["zero_compute"].append(dict(method="Z3 core-size linear extrapolation Nc10,12 -> Ntot", probe=p,
                                                 N=N, **score(est, ex)))
            e2, e4 = ref(p, N - 2), ref(p, N - 4)
            if e2 is not None:
                summ["zero_compute"].append(dict(method="Z4a exact(N-2) as predictor", probe=p, N=N, **score(e2, ex)))
            if e2 is not None and e4 is not None:
                est = {t: {b: 2 * e2[t][b] - e4[t][b] for b in e2[t]} for t in e2}
                summ["zero_compute"].append(dict(method="Z4b linear-in-N extrapolation exact(N-4,N-2)", probe=p, N=N,
                                                 **score(est, ex)))
    json.dump(summ, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
    print("CCE (hybrid base):")
    for c in summ["cce"]:
        print(f"  p{c['probe']:<3} N{c['N']} base={c['base']:<5} {c['est']:<6} M{c['M']} err {c['max_err']:.3f} "
              f"se {c.get('max_se', 0):.3f} bias {c['mean_signed']:+.3f} subruns {c['n_subruns']} pairs {c['n_pairs']} "
              f"max_core {c['max_core']} cpu {c['cpu_secs']}s by_t {c['err_by_t']}")
    print("zero-compute adversaries (max |err| over b and t in [80,320] us; sigma = 0.01):")
    for z in summ["zero_compute"]:
        print(f"  p{z['probe']:>3} N{z['N']}  {z['max_err']:.3f}  {z['method']}")
    print("runs (err = max |F - F_exact| over b, t in [80,320] us; bias = mean signed F - F_exact in window):")
    for r in sorted(summ["runs"], key=lambda r: (r["N"], r["probe"], r["core"], r["bath"], r["ba"], r["est"])):
        ex = ref(r["probe"], r["N"])
        sgn = [r["F_est"][t][b] - ex[round(float(t))][b] for t in r["F_est"] if WIN[0] <= float(t) <= WIN[1]
               for b in r["F_est"][t]]
        r["mean_signed"] = round(float(np.mean(sgn)), 4)
        print(f"  p{r['probe']:<3} N{r['N']} {r['core']:<7} {r['bath']:<5} {r['ba']:<5} {r['est']:<6} M{r['M']:<3} "
              f"err {r['max_err']:.3f} se {r.get('max_se', 0):.3f} bias {r['mean_signed']:+.3f} "
              f"cpu {r['secs']:>6}s sizes {r['sizes']}")
    json.dump(summ, open(os.path.join(HERE, "summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
