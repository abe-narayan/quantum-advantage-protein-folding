"""Warm-start diagnostic: the spectral gap is a worst-case (any-start) rate.  A classical user of the A80 energy starts
from x* (the multistart minimum = state 0 of every table; DEP, native-free).  For the largest-n instances of the relaxed
families, compare the TV mixing time from x* (eps = 0.01) of the best plain classical chain and of the tuned quantum
proposal (both rebuilt from results/*.json).  Also: where does the slowest mode live? (L2(pi) weight of the slowest
eigenfunction on states with E - Emin > 10 T.)  Writes diag_warm.json (atomic)."""
import glob
import json
import os

import numpy as np

import qemcmc as QM

HERE = os.path.dirname(os.path.abspath(__file__))


def P_from_Q(Q, E, T):
    dE = E[None, :] - E[:, None]
    P = Q * np.exp(-np.maximum(dE, 0.0) / T)
    np.fill_diagonal(P, 0.0)
    P[np.diag_indices_from(P)] = 1.0 - P.sum(1)
    return P


def tmix(P, mu, pi, eps=0.01, cap=2 ** 22):
    """TV mixing time from mu: dyadic search by squaring, then stepwise refinement (<= 4096 steps)."""
    def tv(x):
        return 0.5 * np.abs(x - pi).sum()
    if tv(mu) <= eps:
        return 0
    Pk = P.copy(); t = 1; prev_mu = mu.copy(); cur = mu @ P
    while tv(cur) > eps and t < cap:
        prev_mu = cur.copy() if False else prev_mu
        Pk = Pk @ Pk
        prev_mu = cur
        cur = mu @ Pk
        t *= 2
        if tv(cur) <= eps:
            break
    if tv(cur) > eps:
        return float("inf")
    # refine between t/2 and t
    x = prev_mu if t > 1 else mu
    tt = t // 2 if t > 1 else 0
    steps = 0
    while tv(x) > eps and steps < 4096:
        x = x @ P; tt += 1; steps += 1
    return tt if tv(x) <= eps else t


def slow_mode_high_weight(P, E, T, pi):
    d = np.sqrt(pi)
    S = (d[:, None] * P) / d[None, :]
    S = 0.5 * (S + S.T)
    w, U = np.linalg.eigh(S)
    k = np.argsort(np.abs(1 - w))[1]          # slowest non-stationary mode by |1 - lambda| (spectral)
    f = U[:, k]
    high = (E - E.min()) > 10 * T
    return float((f[high] ** 2).sum()), float(1 - w[k])


def rebuild_best_plain(rec, E, n, T):
    c = rec["classical"][str(T)]
    cands = [("local", c["local"]["abs"]), ("uniform", c["uniform"]["abs"])]
    cands += [(f"mix_{p}", v["abs"]) for p, v in c["mix"].items()]
    cands += [(f"pflip_{q}", v["abs"]) for q, v in c["pflip"].items()]
    name, gap = max(cands, key=lambda z: z[1])
    N = 2 ** n
    Hm = QM.hamming_matrix(n)
    Ql = (Hm == 1).astype(float) / n
    if name == "local":
        Q = Ql
    elif name == "uniform":
        Q = np.full((N, N), 1.0 / N)
    elif name.startswith("mix"):
        p = float(name.split("_")[1]); Q = p / N + (1 - p) * Ql
    else:
        Q = QM.Q_pflip(Hm, n, float(name.split("_")[1]))
    return name, gap, Q


def main():
    out = []
    files = sorted(glob.glob(os.path.join(HERE, "results", "*relaxed*_n9.json")) +
                   glob.glob(os.path.join(HERE, "results", "*relaxed_n10.json")))
    for f in files:
        rec = json.load(open(f))
        if rec["grid"] != "coarse":
            continue
        tb = rec["meta"]["E_table"]
        n = rec["n"]
        E = np.load(os.path.join(HERE, "instances", tb + ".npz"))["E"][: 2 ** n].astype(float)
        for T in (1.0, 2.0):
            lp = QM.logpi(E, T); pi = np.exp(lp)
            mu = np.zeros(2 ** n); mu[0] = 1.0                     # x*
            muU = np.full(2 ** n, 1.0 / 2 ** n)                    # uniform start
            name, gc, Qc = rebuild_best_plain(rec, E, n, T)
            q = rec["quantum"]
            mode = max(q, key=lambda m: q[m][str(T)]["best"])
            g, t = q[mode][str(T)]["arg"].split("_")
            qp = QM.QuantumProposal(E, n, mode=mode); qp.set_gamma(float(g)); Qq = qp.Q(float(t))
            Pc = P_from_Q(Qc, E, T); Pq = P_from_Q(Qq, E, T)
            hc, gc2 = slow_mode_high_weight(Pc, E, T, pi)
            hq, gq2 = slow_mode_high_weight(Pq, E, T, pi)
            row = dict(table=tb, n=n, T=T, classical=name, gap_c=gc, gap_q=q[mode][str(T)]["best"], q_arg=f"{mode}:{g}_{t}",
                       tmix_warm_c=tmix(Pc, mu, pi), tmix_warm_q=tmix(Pq, mu, pi),
                       tmix_unif_c=tmix(Pc, muU, pi), tmix_unif_q=tmix(Pq, muU, pi),
                       pi_x0=float(pi[0]), slow_mode_highE_weight_c=hc, slow_mode_highE_weight_q=hq)
            out.append(row)
            print(json.dumps(row), flush=True)
    tmp = os.path.join(HERE, "diag_warm.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "diag_warm.json"))


if __name__ == "__main__":
    main()
