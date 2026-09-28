"""ROUND3 lane qemcmc_exact: exact gaps of classical chains vs the Layden quantum-enhanced proposal on A80 instances.

One JSON per (table, n) in results/ (atomic tmp+replace), so a killed run loses at most one instance.
Stops cleanly when --budget seconds are used.

Usage: python run_gaps.py --tables 5O37A_30_amb_2_relaxed ... --ns 6 7 8 9 10 --budget 700 [--grid coarse|fine|small]
       python run_gaps.py --sk --ns 4 5 6 7 8 9 --sk-instances 12      (Layden SK control with the ST adversary)
"""
from __future__ import annotations

import argparse
import json
import os
import time

import numpy as np

import qemcmc as QM

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
TS = (1.0, 2.0, 4.0)
GRIDS = {
    "fine": ([0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9], [1, 1.5, 2, 3, 4, 5, 7, 9, 12, 15, 20]),
    "coarse": ([0.2, 0.35, 0.5, 0.65, 0.8], [2, 4, 7, 12, 20]),
    "small": ([0.35, 0.5, 0.65], [4, 7, 12]),
}
LAYDEN_G = (0.25, 0.6)
LAYDEN_T = (2.0, 20.0)


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


def classical(E, n, T, dense_ok=True):
    N = 2 ** n
    out = {}
    lp = QM.logpi(E, T)
    out["local"] = QM.gaps_sparse(QM.local_sparse(E, T, n), lp)
    Hm = QM.hamming_matrix(n)
    Ql = (Hm == 1).astype(float) / n
    Qu = np.full((N, N), 1.0 / N)
    out["uniform"] = QM.gaps_dense(QM.gen_symmetric(Qu, E, T))
    mix = {}
    for p in (0.05, 0.2, 0.5):
        mix[str(p)] = QM.gaps_dense(QM.gen_symmetric(p * Qu + (1 - p) * Ql, E, T))
    out["mix"] = mix
    pf = {}
    for q in (0.05, 0.1, 0.2, 0.3):
        pf[str(q)] = QM.gaps_dense(QM.gen_symmetric(QM.Q_pflip(Hm, n, q), E, T))
    out["pflip"] = pf
    qv, logq = QM.mean_field(E, T, n)
    with np.errstate(divide="ignore"):
        logQ = np.logaddexp(np.log(0.5) + logq[None, :], np.log(0.5) + np.log(np.maximum(Ql, 0)))
    out["mf"] = QM.gaps_dense(QM.gen_general(logQ, lp))
    out["mf"]["q"] = qv.tolist()
    st = {}
    for K in (3, 5, 8):
        for ratio in (8.0, 64.0):
            r = ratio ** (1.0 / (K - 1))
            L, lpj = QM.st_sparse(E, T, n, K, r)
            g = QM.gaps_sparse(L, lpj)
            g["per_target"] = g["abs"] / K
            st[f"K{K}_R{int(ratio)}"] = g
    out["ST"] = st
    return out


def quantum(E, n, grid, modes=("raw", "clip")):
    gam, ts = GRIDS[grid]
    out = {}
    for mode in modes:
        qp = QM.QuantumProposal(E, n, mode=mode)
        tab = {str(T): {} for T in TS}
        avg_all = 0.0; avg_L = 0.0; nL = 0
        for g in gam:
            qp.set_gamma(g)
            for t in ts:
                Q = qp.Q(t)
                avg_all = avg_all + Q
                if LAYDEN_G[0] <= g <= LAYDEN_G[1] and LAYDEN_T[0] <= t <= LAYDEN_T[1]:
                    avg_L = avg_L + Q; nL += 1
                for T in TS:
                    tab[str(T)][f"{g}_{t}"] = QM.gaps_dense(QM.gen_symmetric(Q, E, T))["abs"]
        avg_all = avg_all / (len(gam) * len(ts))
        res = {}
        for T in TS:
            d = tab[str(T)]
            kbest = max(d, key=d.get)
            res[str(T)] = dict(grid=d, best=d[kbest], arg=kbest,
                               avg_grid=QM.gaps_dense(QM.gen_symmetric(avg_all, E, T))["abs"])
            if nL:
                res[str(T)]["avg_layden"] = QM.gaps_dense(QM.gen_symmetric(avg_L / nL, E, T))["abs"]
        out[mode] = res
    return out


def run_one(E_full, n, tag, grid, modes, meta):
    f = os.path.join(RES, f"{tag}_n{n}.json")
    if os.path.exists(f):
        return False
    t0 = time.time()
    E = np.asarray(E_full[: 2 ** n], float)
    rec = dict(tag=tag, n=n, grid=grid, meta=meta, E_min=float(E.min()),
               E_sorted_head=np.sort(E - E.min())[:16].tolist(), classical={}, quantum=None)
    for T in TS:
        rec["classical"][str(T)] = classical(E, n, T)
    tq = time.time()
    rec["quantum"] = quantum(E, n, grid, modes)
    rec["secs_classical"] = tq - t0
    rec["secs_quantum"] = time.time() - tq
    rec["secs"] = time.time() - t0
    atomic_json(rec, f)
    print(f"{tag} n={n} secs={rec['secs']:.1f}", flush=True)
    return True


def sk_energy(n, rng):
    J = np.triu(rng.standard_normal((n, n)), 1)
    h = rng.standard_normal(n)
    idx = np.arange(2 ** n)
    S = 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)
    return -np.einsum("si,ij,sj->s", S, J, S) - S @ h


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tables", nargs="*", default=[])
    ap.add_argument("--ns", nargs="+", type=int, required=True)
    ap.add_argument("--budget", type=float, default=700.0)
    ap.add_argument("--grid", default=None)
    ap.add_argument("--modes", nargs="+", default=["raw", "clip"])
    ap.add_argument("--sk", action="store_true")
    ap.add_argument("--sk-instances", type=int, default=12)
    ap.add_argument("--suffix", default="")
    a = ap.parse_args()
    os.makedirs(RES, exist_ok=True)
    t0 = time.time()
    jobs = []
    if a.sk:
        for n in a.ns:
            for i in range(a.sk_instances):
                E = sk_energy(n, np.random.default_rng(1000 * n + i))
                jobs.append((E, n, f"SK_i{i}" + a.suffix, a.grid or "coarse", a.modes, dict(family="SK", seed=1000 * n + i)))
    for n in a.ns:
        for tb in a.tables:
            d = np.load(os.path.join(HERE, "instances", tb + ".npz"))
            meta = json.loads(str(d["meta"]))
            if meta["alph"] == 4 and n % 2:
                continue
            grid = a.grid or ("fine" if n <= 8 else "coarse")
            jobs.append((d["E"], n, tb + a.suffix, grid, a.modes, dict(meta, E_table=tb)))
    for E, n, tag, grid, modes, meta in jobs:
        if time.time() - t0 > a.budget:
            print("budget reached; stopping", flush=True)
            break
        run_one(E, n, tag, grid, modes, meta)
    print("done secs", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
