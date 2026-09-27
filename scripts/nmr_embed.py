"""R1-E (PREREG_G1_C1_Q4.md): does the late-window structural Fisher information of an isolated NMR cluster survive
embedding in more of the protein?

Core = N_core protons nearest the probe; parameters = C1 v2 parameters built on the core (radial moves of its 3 farthest
protons + rigid shift of a >= 2-proton residue other than the probe's), identical for every environment.
Environments (all gamma = 0 intrinsic):
  iso        exact, N_core spins (the isolated cluster)
  exact_N    exact, the N nearest protons (core + next N - N_core), N in --envs
  deph       exact core + per-spin dephasing gamma_i = sqrt(M2_out,i), M2_out,i = sum_j d_ij^2 over protons within
             --bath-r of the probe that are outside the core (Gaussian-bath proxy; transfer S only)
For each: S_ab(t) (and OTOC F_ab(t) when --otoc-max >= N) for the core's observed spins, and FD derivatives.
Output: research/results/RAW/nmr_embed/<tag>.json with per-environment per-parameter derivative series.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.nmr import spins as SP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--Ncore", type=int, default=10)
    ap.add_argument("--envs", default="12,14")
    ap.add_argument("--otoc-max", type=int, default=12)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--nt", type=int, default=16)
    ap.add_argument("--h", type=float, default=0.05)
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--bath-r", type=float, default=12.0)
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "nmr_embed"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.pdb}_p{a.probe}_core{a.Ncore}_o{a.orient}"
    fj = os.path.join(a.out, tag + ".json")
    if os.path.exists(fj):
        print("exists"); return
    t0 = time.time()
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    b0 = random_b0(1000 + a.orient)
    order = SP.cluster(xyz, a.probe, len(xyz))                 # all protons by distance to the probe
    core = order[:a.Ncore]
    Xc = xyz[core]
    dist = np.linalg.norm(Xc - Xc[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:3]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    rec = max(1, a.steps // a.nt)
    params = []
    for k in far:
        u = (Xc[k] - Xc[0]) / dist[k]
        params.append(dict(name=f"radial_{names[core[k]]}", move=[(int(k), u.tolist())]))
    cnt = {}
    for i in range(a.Ncore):
        cnt[resid[core[i]]] = cnt.get(resid[core[i]], 0) + 1
    pres = resid[core[0]]
    kfar = next((int(k) for k in np.argsort(-dist) if resid[core[k]] != pres and cnt[resid[core[k]]] >= 2), None)
    if kfar is not None:
        ug = (Xc[kfar] - Xc[0]) / dist[kfar]
        grp = [int(i) for i in range(a.Ncore) if resid[core[i]] == resid[core[kfar]]]
        params.append(dict(name=f"rigid_res{resid[core[kfar]]}", move=[(i, ug.tolist()) for i in grp]))

    def geom(X, p, sgn):
        X = X.copy()
        for (i, u) in p["move"]:
            X[i] = X[i] + sgn * a.h * np.asarray(u)            # core indices are the first N_core rows of any env
        return X

    res = dict(pdb=a.pdb, probe=a.probe, Ncore=a.Ncore, orient=a.orient, bs=bs, sigma=a.sigma, h=a.h,
               params=[p["name"] for p in params], envs={})

    def run_env(label, X, gamma=0.0, otoc=False):
        te = time.time()
        dm = SP.couplings(X, b0)
        tt, S0, F0 = SP.sector_exact_correlators(dm, a.dt, a.steps, 0, bs, gamma=gamma, record_every=rec, otoc=otoc)
        env = dict(N=len(X), times=tt.tolist(), S={str(b): S0[b].tolist() for b in bs},
                   F=({str(b): F0[b].tolist() for b in bs} if F0 else None), dS={}, dF={})
        for p in params:
            _, Sp, Fp = SP.sector_exact_correlators(SP.couplings(geom(X, p, +1), b0), a.dt, a.steps, 0, bs, gamma=gamma,
                                                   record_every=rec, otoc=otoc)
            _, Sm, Fm = SP.sector_exact_correlators(SP.couplings(geom(X, p, -1), b0), a.dt, a.steps, 0, bs, gamma=gamma,
                                                   record_every=rec, otoc=otoc)
            env["dS"][p["name"]] = {str(b): ((Sp[b] - Sm[b]) / (2 * a.h)).tolist() for b in bs}
            if otoc and Fp:
                env["dF"][p["name"]] = {str(b): ((np.asarray(Fp[b]) - np.asarray(Fm[b])) / (2 * a.h)).tolist() for b in bs}
        env["secs"] = time.time() - te
        res["envs"][label] = env
        print(json.dumps({"env": label, "N": len(X), "otoc": otoc, "secs": round(env["secs"], 1)}), flush=True)
        json.dump(res, open(fj + ".partial", "w"))

    run_env("iso", xyz[core], otoc=a.Ncore <= a.otoc_max)
    # dephasing embedding: bath = protons within bath_r of the probe outside the core
    dpr = np.linalg.norm(xyz - xyz[a.probe], axis=1)
    bath = [int(j) for j in order[a.Ncore:] if dpr[j] <= a.bath_r]
    Xall = np.vstack([xyz[core], xyz[bath]])
    dfull = SP.couplings(Xall, b0)
    m2 = (dfull[:a.Ncore, a.Ncore:] ** 2).sum(1)
    gam = np.sqrt(m2)
    res["deph_gamma"] = gam.tolist()
    res["n_bath"] = len(bath)
    run_env("deph", xyz[core], gamma=gam, otoc=False)
    for N in [int(v) for v in a.envs.split(",") if v]:
        run_env(f"exact_N{N}", xyz[order[:N]], otoc=N <= a.otoc_max)
    res["secs"] = time.time() - t0
    json.dump(res, open(fj + ".tmp", "w"))
    os.replace(fj + ".tmp", fj)
    if os.path.exists(fj + ".partial"):
        os.remove(fj + ".partial")


if __name__ == "__main__":
    main()
