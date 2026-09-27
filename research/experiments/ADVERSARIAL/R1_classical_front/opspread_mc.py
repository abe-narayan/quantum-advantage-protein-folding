"""E2: operator-spreading stochastic model (incoherent Pauli-path Markov chain) for the echo F_ab(t).

Heisenberg evolution of Z_a through the SAME Trotter circuit, but every Pauli rotation U = exp(-i theta G) acting on an
anticommuting string P is replaced by the classical Markov move
        P -> P        with probability cos^2(2 lam theta)
        P -> G.P      with probability sin^2(2 lam theta)       (phases dropped),
i.e. the exact evolution of the squared amplitudes c_P^2 when all cross-terms between Pauli paths are discarded
(random-phase / random-circuit operator-spreading approximation; its coarse-grained limit is the FKPP / biased-diffusion
picture of operator weight with rates ~ d_ij^2).  Then F_ab(t) ~ E[ s_b(P(t)) ], s_b = -1 if P has X or Y at b.
Cost: O(M x (#gates) x steps) for M trajectories -- polynomial in N (M set by the target statistical error only).
lam = 1: parameter-free.  lam fitted: one scalar per probe, least squares on the N=8 exact echo of the SAME probe
(a fixed-size exact classical computation; no N=10 reference used) -> 'transfer' calibration, as in the task card.
Also a mean-field (product-state) closure of the same chain: site occupations only (N x 4 numbers) -> FKPP-like ODE.

usage: python opspread_mc.py [M]
"""
from __future__ import annotations

import math
import sys
import time

import numpy as np

import common as C
from qapf.nmr import spins as SP


def rotations(dm):
    """Heisenberg-ordered list of (i, j, gx, gz, theta) for one Trotter step (reversed pair order; within a pair the
    order of qapf.nmr.spins.conj_pair: YY, XX, ZZ)."""
    rots = []
    for (i, j, ddt) in reversed(SP.pair_list(dm, C.DT)):
        a = ddt / 2.0
        m = (1 << i) | (1 << j)
        rots.append((i, j, m, m, -a / 2))      # YY
        rots.append((i, j, m, 0, -a / 2))      # XX
        rots.append((i, j, 0, m, a))           # ZZ
    return rots


def mc_chain(dm, bs, M, lam=1.0, seed=0, a=0, nc=1):
    """nc = coherence (memory) block: the phases are randomised only every nc Trotter steps; within a block the pair
    rotation angle is nc * theta (coarse-grained Markov chain, memory time tau = nc * dt)."""
    N = len(dm)
    assert C.REC % nc == 0
    rng = np.random.default_rng(seed)
    x = np.zeros(M, np.int64)
    z = np.full(M, 1 << a, np.int64)
    rots = [(i, j, gx, gz, math.sin(2 * lam * nc * th) ** 2) for (i, j, gx, gz, th) in rotations(dm)]
    out = {b: [] for b in bs}
    for k in range(0, C.STEPS + 1, nc):
        if k % C.REC == 0:
            for b in bs:
                out[b].append(1.0 - 2.0 * float(((x >> b) & 1).mean()))
        if k == C.STEPS:
            break
        for (i, j, gx, gz, p) in rots:
            v = (x & gz) ^ (z & gx)
            anti = ((v >> i) ^ (v >> j)) & 1
            flip = (anti == 1) & (rng.random(M) < p)
            x[flip] ^= gx
            z[flip] ^= gz
    return {b: np.array(v) for b, v in out.items()}


def meanfield(dm, bs, lam=1.0, a=0, nc=1):
    """Product-state closure: each site carries a distribution over {I, X, Y, Z}; a pair rotation acts on the joint
    2-site distribution (product of marginals) exactly as the Markov move, then is re-factorised into marginals."""
    N = len(dm)
    P = np.zeros((N, 4)); P[:, 0] = 1.0; P[a] = [0, 1.0, 0, 0]     # index = 2*xbit + zbit -> I=0, Z=1, X=2, Y=3
    rots = [(i, j, gx, gz, math.sin(2 * lam * nc * th) ** 2) for (i, j, gx, gz, th) in rotations(dm)]
    loc = [(xb, zb) for xb in (0, 1) for zb in (0, 1)]
    out = {b: [] for b in bs}
    for k in range(0, C.STEPS + 1, nc):
        if k % C.REC == 0:
            for b in bs:
                out[b].append(1.0 - 2.0 * (P[b, 2] + P[b, 3]))
        if k == C.STEPS:
            break
        for (i, j, gx, gz, p) in rots:
            gxi, gzi = (gx >> i) & 1, (gz >> i) & 1
            gxj, gzj = (gx >> j) & 1, (gz >> j) & 1
            J = np.outer(P[i], P[j])
            Jn = np.zeros((4, 4))
            for si, (xi, zi) in enumerate(loc):
                for sj, (xj, zj) in enumerate(loc):
                    anti = ((xi & gzi) ^ (zi & gxi) ^ (xj & gzj) ^ (zj & gxj)) & 1
                    w = J[si, sj]
                    if anti:
                        ti = 2 * (xi ^ gxi) + (zi ^ gzi); tj = 2 * (xj ^ gxj) + (zj ^ gzj)
                        Jn[si, sj] += (1 - p) * w; Jn[ti, tj] += p * w
                    else:
                        Jn[si, sj] += w
            P[i] = Jn.sum(1); P[j] = Jn.sum(0)
            P[i] /= P[i].sum(); P[j] /= P[j].sum()        # renormalise (the product update squares round-off)
    return {b: np.array(v) for b, v in out.items()}


def fit_lam(pdb, probe, M, lams=(0.5, 0.75, 1.0, 1.5, 2.0, 3.0), ncs=(1, 2, 5, 10)):
    """least-squares (nc, lam) on the N=8 exact echo of the same probe (small-cluster calibration; no N=10 data)."""
    tt, _, F8, _ = C.load_or_make_ref(pdb, probe, 8)
    c8 = C.setup(pdb, probe, 8)
    best = None
    for nc in ncs:
        for lam in lams:
            Fe = mc_chain(c8["dm"], c8["bs"], M, lam, seed=99, nc=nc)
            r = sum(float(((Fe[b] - F8[b]) ** 2).sum()) for b in c8["bs"])
            if best is None or r < best[2]:
                best = (nc, lam, r)
    return best


def main():
    M = int(sys.argv[1]) if len(sys.argv) > 1 else 200000
    res = dict(M=M, thr=C.THR, clusters={})
    for pdb, probe in C.CLUSTERS:
        tt, S0, F0, ref = C.load_or_make_ref(pdb, probe, 10)
        c = C.setup(pdb, probe, 10)
        bs, dm = c["bs"], c["dm"]
        ent = dict(bs=bs, runs={})
        t0 = time.process_time()
        Fe = mc_chain(dm, bs, M, 1.0, seed=1)
        cpu = time.process_time() - t0
        i, tus, err = C.t_c(Fe, F0, bs, tt, C.THR)
        se = 1.0 / math.sqrt(M)
        ent["runs"]["markov_lam1"] = dict(t_c_index=i, t_c_us=tus, max_err=err.tolist(), cpu=cpu, stat_se_max=se,
                                          F_est={str(b): Fe[b].tolist() for b in bs})
        t0 = time.process_time()
        nc, lam, rss = fit_lam(pdb, probe, 5000)
        Fe = mc_chain(dm, bs, M, lam, seed=2, nc=nc)
        i, tus, err = C.t_c(Fe, F0, bs, tt, C.THR)
        ent["runs"]["markov_fit_N8"] = dict(lam=lam, nc=nc, rss_N8=rss, t_c_index=i, t_c_us=tus, max_err=err.tolist(),
                                            cpu=time.process_time() - t0, F_est={str(b): Fe[b].tolist() for b in bs})
        t0 = time.process_time()
        Fe = meanfield(dm, bs, 1.0)
        i, tus, err = C.t_c(Fe, F0, bs, tt, C.THR)
        ent["runs"]["meanfield_lam1"] = dict(t_c_index=i, t_c_us=tus, max_err=err.tolist(),
                                             cpu=time.process_time() - t0, F_est={str(b): Fe[b].tolist() for b in bs})
        Fe = meanfield(dm, bs, lam, nc=nc)
        i, tus, err = C.t_c(Fe, F0, bs, tt, C.THR)
        ent["runs"]["meanfield_fit_N8"] = dict(lam=lam, nc=nc, t_c_index=i, t_c_us=tus, max_err=err.tolist(),
                                               F_est={str(b): Fe[b].tolist() for b in bs})
        res["clusters"][f"{pdb}_p{probe}"] = ent
        print(pdb, probe, {k: (v["t_c_us"], round(max(v["max_err"]), 3), v.get("lam"), v.get("nc")) for k, v in ent["runs"].items()},
              flush=True)
    C.dump(res, "opspread_N10.json")


if __name__ == "__main__":
    main()
