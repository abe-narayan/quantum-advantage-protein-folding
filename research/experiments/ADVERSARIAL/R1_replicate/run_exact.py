"""R1 replicate: independent exact S_ab(t), F_ab(t) and per-time Fisher information for
research/results/RAW/nmr_gate/1UBQ_p19_N10_o0_g0.json, compared against the stored numbers.

Parameters are re-derived from the definition in scripts/nmr_gate.py.  The stored file was produced by the version at
git 92bb4eb, whose rigid shift picks the farthest proton of a different residue (-> rigid_res16, 1 proton, identical to
radial_HA/GLU16).  The current script (50e0c9e) additionally requires >= 2 cluster protons in that residue
(-> rigid_res2, 3 protons).  Both are computed.

Usage (single-threaded, ~4 CPU-min for --mode trotter, ~3 for --mode continuous):
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python run_exact.py --mode trotter
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python run_exact.py --mode continuous
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
import repl_lib as L  # noqa: E402
from qapf.nmr.spins import read_h_coords, cluster  # noqa: E402  (geometry only)

STORED = os.path.join(ROOT, "research", "results", "RAW", "nmr_gate", "1UBQ_p19_N10_o0_g0.json")
ALIASES = {}


def setup(probe=19, N=10, orient=0, K=3):
    names, xyz, resid = read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    idx = cluster(xyz, probe, N)
    X0 = xyz[idx].copy()
    b0 = L.random_b0(1000 + orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    params = []
    for k in far:
        u = (X0[k] - X0[0]) / dist[k]
        params.append(dict(name=f"radial_{names[idx[k]]}", move=[(k, u)], r=float(dist[k]), n_moved=1))
    pres = resid[idx[0]]
    cnt = {}
    for i in range(N):
        cnt[resid[idx[i]]] = cnt.get(resid[idx[i]], 0) + 1
    for label, rule in (("v2_early(92bb4eb)", lambda k: resid[idx[k]] != pres),
                        ("v2_current(50e0c9e)", lambda k: resid[idx[k]] != pres and cnt[resid[idx[k]]] >= 2)):
        kfar = next((int(k) for k in np.argsort(-dist) if rule(k)), None)
        kres = resid[idx[kfar]]
        grp = [i for i in range(N) if resid[idx[i]] == kres]
        ug = (X0[kfar] - X0[0]) / dist[kfar]
        nm = f"rigid_res{kres}"
        if any(p["name"] == nm for p in params):
            continue
        dup = next((p["name"] for p in params if len(grp) == 1 and p["move"][0][0] == grp[0]
                    and np.allclose(p["move"][0][1], ug)), None)
        if dup is not None:                      # identical geometry move -> alias only (the stored duplicate)
            ALIASES[nm] = dup
            continue
        params.append(dict(name=nm, move=[(i, ug) for i in grp], r=float(dist[kfar]), n_moved=len(grp), rule=label))
    return dict(names=names, idx=idx, X0=X0, b0=b0, dist=dist, bs=bs, params=params)


def geom(X0, p, sgn, h):
    X = X0.copy()
    for (i, u) in p["move"]:
        X[i] = X[i] + sgn * h * np.asarray(u)
    return X


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="trotter", choices=["trotter", "continuous"])
    ap.add_argument("--hlist", default="0.05,0.02")
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--rec", type=int, default=10)
    ap.add_argument("--sigma", type=float, default=0.01)
    a = ap.parse_args()
    t0 = time.process_time()
    G = setup()
    bs = G["bs"]
    st = json.load(open(STORED))
    assert [int(i) for i in G["idx"]] == st["cluster"], "cluster mismatch"
    assert bs == st["bs"], "bs mismatch"
    assert np.allclose(G["b0"], st["b0"], atol=1e-15)
    run = L.exact_trotter if a.mode == "trotter" else L.exact_continuous

    def corr(X):
        S, F, info = run(L.my_couplings(X, G["b0"]), a.dt, a.steps, a.rec, 0, bs)
        return S, F, info

    S0, F0, info0 = corr(G["X0"])
    res = dict(mode=a.mode, dt=a.dt, steps=a.steps, rec=a.rec, sigma=a.sigma, bs=bs,
               cluster=[int(i) for i in G["idx"]], b0=G["b0"].tolist(), info_base=info0,
               S_exact={str(b): S0[b].tolist() for b in bs}, F_exact={str(b): F0[b].tolist() for b in bs},
               params=[])
    for h in [float(x) for x in a.hlist.split(",")]:
        for p in G["params"]:
            Sp, Fp, _ = corr(geom(G["X0"], p, +1, h))
            Sm, Fm, _ = corr(geom(G["X0"], p, -1, h))
            dS = {b: (Sp[b] - Sm[b]) / (2 * h) for b in bs}
            dF = {b: (Fp[b] - Fm[b]) / (2 * h) for b in bs}
            fi = sum(dS[b] ** 2 for b in bs) / a.sigma ** 2
            fo = sum(dF[b] ** 2 for b in bs) / a.sigma ** 2
            res["params"].append(dict(name=p["name"], h=h, r=p["r"], n_moved=p["n_moved"], rule=p.get("rule"),
                                      FI_t=fi.tolist(), FI_otoc_t=fo.tolist(), FI_total=float(fi.sum()),
                                      FI_otoc_total=float(fo.sum()),
                                      dS={str(b): dS[b].tolist() for b in bs}, dF={str(b): dF[b].tolist() for b in bs}))
            print(json.dumps(dict(p=p["name"], h=h, FI=round(float(fi.sum()), 3), FIo=round(float(fo.sum()), 3),
                                  cpu=round(time.process_time() - t0, 1))), flush=True)

    # ---------------------------------------------------------------- comparison with the stored file
    cmp = {}
    cmp["S_exact_maxabs"] = max(float(np.abs(S0[b] - np.asarray(st["S_exact"][str(b)])).max()) for b in bs)
    cmp["F_exact_maxabs"] = max(float(np.abs(F0[b] - np.asarray(st["F_exact"][str(b)])).max()) for b in bs)
    cmp["params"] = {}
    for sp in st["params"]:
        tgt = ALIASES.get(sp["name"], sp["name"])
        mine = next((q for q in res["params"] if q["h"] == st["h"] and q["name"] == tgt), None)
        if mine is None:
            continue
        d = {}
        for key in ("FI_t", "FI_otoc_t"):
            A = np.asarray(mine[key]); B = np.asarray(sp[key])
            d[key + "_maxabs"] = float(np.abs(A - B).max())
            d[key + "_maxrel_of_peak"] = float(np.abs(A - B).max() / max(np.abs(B).max(), 1e-300))
        for key in ("dS", "dF"):
            d[key + "_maxabs"] = max(float(np.abs(np.asarray(mine[key][str(b)]) - np.asarray(sp[key][str(b)])).max())
                                     for b in bs)
        d["FI_total_mine"] = mine["FI_total"]; d["FI_total_stored"] = sp["FI_total"]
        d["FI_otoc_total_mine"] = mine["FI_otoc_total"]; d["FI_otoc_total_stored"] = sp["FI_otoc_total"]
        d["matched_to"] = mine["name"]
        cmp["params"][sp["name"]] = d
    # FD-step robustness (h=0.05 vs h=0.02), own numbers
    hs = sorted({q["h"] for q in res["params"]})
    if len(hs) > 1:
        rob = {}
        for p in G["params"]:
            q1 = next(q for q in res["params"] if q["name"] == p["name"] and q["h"] == 0.05)
            q2 = next(q for q in res["params"] if q["name"] == p["name"] and q["h"] == hs[0])
            rob[p["name"]] = dict(FI_total_ratio=q2["FI_total"] / q1["FI_total"],
                                  FI_otoc_total_ratio=q2["FI_otoc_total"] / q1["FI_otoc_total"],
                                  FI_otoc_t_maxrel_of_peak=float(np.abs(np.asarray(q2["FI_otoc_t"]) - np.asarray(q1["FI_otoc_t"])).max()
                                                                 / max(q1["FI_otoc_t"])))
        cmp["fd_step_robustness_h%.2f_vs_0.05" % hs[0]] = rob
    res["compare_stored"] = cmp
    res["aliases"] = ALIASES
    res["cpu_s"] = time.process_time() - t0
    fn = os.path.join(HERE, f"exact_{a.mode}.json")
    json.dump(res, open(fn, "w"), indent=0)
    print(json.dumps(cmp, indent=1))


if __name__ == "__main__":
    main()
