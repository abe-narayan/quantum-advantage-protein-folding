"""Validation of qemcmc.py: (1) sparse grounded-LU gaps == dense eigvalsh gaps (local, ST); (2) quantum proposal
rows sum to 1 and Q is symmetric; (3) reproduction of Layden et al. (2023) Fig. 2 on SK instances at T = 1
(J_jk, h_j ~ N(0,1), fully connected), with Q averaged over gamma in [0.25, 0.6] (8 midpoints) x t in [2, 20] (10 points).
Published fits (verified from arXiv:2203.12497 Table S3, T = 1): quantum k = 0.264(4), local 0.94(4), uniform 0.948(7).
Writes validate.json."""
import json
import os
import time

import numpy as np

import qemcmc as QM

HERE = os.path.dirname(os.path.abspath(__file__))


def sk_energy(n, rng):
    J = np.triu(rng.standard_normal((n, n)), 1)
    h = rng.standard_normal(n)
    idx = np.arange(2 ** n)
    S = 1 - 2 * ((idx[:, None] >> np.arange(n)[None, :]) & 1)
    return -np.einsum("si,ij,sj->s", S, J, S) - S @ h


def main():
    out = {}
    rng = np.random.default_rng(7)
    # (1) sparse vs dense
    chk = []
    for n in (5, 6, 7):
        E = sk_energy(n, rng) * 3.0
        for T in (0.5, 1.0):
            Ld = QM.gen_symmetric(QM.Q_local(n), E, T).copy()
            gd = QM.gaps_dense(Ld)
            gs = QM.gaps_sparse(QM.local_sparse(E, T, n), QM.logpi(E, T))
            Lst, lpj = QM.st_sparse(E, T, n, 4, 2.0)
            gsd = QM.gaps_dense(Lst.toarray())
            gss = QM.gaps_sparse(Lst, lpj)
            chk.append(dict(n=n, T=T, local_dense=gd["spec"], local_sparse=gs["spec"],
                            st_dense=gsd["spec"], st_sparse=gss["spec"]))
    out["sparse_vs_dense"] = chk
    out["sparse_vs_dense_max_rel_err"] = max(max(abs(c["local_dense"] - c["local_sparse"]) / c["local_dense"],
                                                 abs(c["st_dense"] - c["st_sparse"]) / c["st_dense"]) for c in chk)
    # (2) quantum proposal sanity
    n = 6
    E = sk_energy(n, rng)
    qp = QM.QuantumProposal(E, n)
    qp.set_gamma(0.4)
    Q = qp.Q(7.0)
    out["Q_rowsum_err"] = float(np.abs(Q.sum(1) - 1).max())
    out["Q_asym"] = float(np.abs(Q - Q.T).max())
    # (3) Layden reproduction
    gam = 0.25 + (np.arange(8) + 0.5) * (0.35 / 8)
    ts = np.linspace(2, 20, 10)
    res = {}
    t0 = time.time()
    for n in (4, 5, 6, 7, 8):
        dl, du, dq = [], [], []
        for inst in range(24):
            E = sk_energy(n, rng)
            T = 1.0
            dl.append(QM.gaps_dense(QM.gen_symmetric(QM.Q_local(n), E, T))["abs"])
            du.append(QM.gaps_dense(QM.gen_symmetric(QM.Q_uniform(2 ** n), E, T))["abs"])
            qp = QM.QuantumProposal(E, n)
            Qa = np.zeros((2 ** n, 2 ** n))
            for g in gam:
                qp.set_gamma(g)
                for t in ts:
                    Qa += qp.Q(t)
            Qa /= len(gam) * len(ts)
            dq.append(QM.gaps_dense(QM.gen_symmetric(Qa, E, T))["abs"])
        res[n] = dict(local=float(np.mean(dl)), uniform=float(np.mean(du)), quantum=float(np.mean(dq)))
    ns = np.array(sorted(res))
    fits = {}
    for key in ("local", "uniform", "quantum"):
        y = np.log2([res[m][key] for m in ns])
        k = -np.polyfit(ns, y, 1)[0]
        fits[key] = float(k)
    out["layden_repro"] = dict(mean_abs_gap=res, k_fit=fits, instances_per_n=24, T=1.0, secs=time.time() - t0,
                               published=dict(quantum=0.264, local=0.94, uniform=0.948))
    json.dump(out, open(os.path.join(HERE, "validate.json"), "w"), indent=1)
    print(json.dumps({k: out[k] for k in ("sparse_vs_dense_max_rel_err", "Q_rowsum_err", "Q_asym")}))
    print(json.dumps(out["layden_repro"]["k_fit"]), json.dumps(res))


if __name__ == "__main__":
    main()
