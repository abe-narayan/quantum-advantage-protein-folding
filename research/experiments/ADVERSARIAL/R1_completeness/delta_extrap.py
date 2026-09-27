"""R1_completeness: lost-norm (delta) extrapolation adversary for the echo, from EXISTING C2 sparse-Pauli rungs (no new
simulation).  R1_amplify measured bias_F1 ~ c*delta with log-log slope ~1 (delta = 1 - kept_norm2).  If so, two cheap rungs
(eps1 > eps2) give F_ext(t) = F2 - delta2*(F1 - F2)/(delta1 - delta2) (linear Richardson in delta; per site and time).
Also: norm-corrected F/kept_norm2 and its extrapolation.  Reference = sector-exact F stored in the same file.
Failure time = first record with max_b |err| > sigma = 0.01.  Reports string cost of the rungs used vs the rung that
first reproduces the echo on its own.
"""
import glob, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "..", "..", "results", "RAW", "nmr_sparse")
SIG = 0.01
res = []
for fn in sorted(glob.glob(os.path.join(RAW, "*_g0.json*"))):
    if fn.endswith(".running"):
        continue
    g = json.load(open(fn)); bs = [str(b) for b in g["bs"]]
    if not g.get("exact") or not g["exact"].get("F"):
        continue
    Fex = np.array([g["exact"]["F"][b] for b in bs]); t = np.array(g["exact"]["times"]) * 1e6
    runs = [r for r in g["runs"] if r.get("steps_done", g["steps"]) == g["steps"] and not r.get("capped")]
    R = {r["eps"]: r for r in runs}

    def tfail(err):
        e = np.abs(err).max(0); i = np.where(e > SIG)[0]
        return (float(t[i[0]]) if len(i) else None), float(e[4:].max())
    rows = []
    for r in runs:
        F = np.array([r["F"][b] for b in bs]); k2 = np.array(r["kept_norm2"])
        rows.append(dict(method="plain", eps=[r["eps"]], peak_strings=r["peak_strings"], t_fail=tfail(F - Fex)[0], maxerr_80_320=tfail(F - Fex)[1]))
        rows.append(dict(method="normcorr", eps=[r["eps"]], peak_strings=r["peak_strings"], t_fail=tfail(F / k2 - Fex)[0], maxerr_80_320=tfail(F / k2 - Fex)[1]))
    eps_sorted = sorted(R, reverse=True)
    for e1, e2 in zip(eps_sorted[:-1], eps_sorted[1:]):
        r1, r2 = R[e1], R[e2]
        F1 = np.array([r1["F"][b] for b in bs]); F2 = np.array([r2["F"][b] for b in bs])
        d1 = 1 - np.array(r1["kept_norm2"]); d2 = 1 - np.array(r2["kept_norm2"])
        den = np.where(np.abs(d1 - d2) > 1e-12, d1 - d2, np.inf)
        Fext = F2 - d2 * (F1 - F2) / den
        k1 = 1 - d1; k2 = 1 - d2
        G1, G2 = F1 / k1, F2 / k2
        Gext = G2 - d2 * (G1 - G2) / den
        ps = max(r1["peak_strings"], r2["peak_strings"])
        for name, X in (("extrap_plain", Fext), ("extrap_normcorr", Gext)):
            tf, me = tfail(X - Fex)
            rows.append(dict(method=name, eps=[e1, e2], peak_strings=ps, t_fail=tf, maxerr_80_320=me))
    job = os.path.basename(fn)
    res.append(dict(job=job, N=g["N"], rows=rows))
    print("==", job)
    for r in rows:
        print(f"   {r['method']:16s} eps={str(r['eps']):22s} peak={r['peak_strings']:>8d}  t_fail={r['t_fail']}  maxerr[80,320]={r['maxerr_80_320']:.4f}")
json.dump(res, open(os.path.join(HERE, "out", "delta_extrap.json"), "w"), indent=1)
