"""E1: cluster-correlation expansion (CCE) of the echo / first-order OTOC  F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b] / 2^N.

For an observed spin b let R = cluster \\ {a, b}.  For every subset C of R, F_C(t) = exact OTOC of the SAME Trotter circuit
restricted to the spins {a, b} u C (all gates touching spins outside the subsystem deleted; gate order kept).
Cluster increments (Moebius inversion) with a link function g:
    g~_C = sum_{C' subset C} (-1)^{|C|-|C'|} g(F_C'),      F_est^(k) = g^{-1}( sum_{|C| <= k} g~_C ).
g = identity   -> additive CCE          (exact when k = |R|)
g = log        -> multiplicative CCE    (the standard Yang-Liu CCE for decoherence functions; needs F_C > 0)
g = log(F-Fp)  -> not used (F crosses the plateau).
Cost of order k: sum_{j<=k} C(N-2, j) exact simulations of <= k+2 spins, i.e. O(N^k 4^{k+2}) -- polynomial in N at fixed k.
All subsystems containing a are simulated once (2^(N-1) of them; cheap for N <= 12), then every order is assembled.
Also: 'nested' = the plain sub-cluster (order-k truncation with the k most strongly coupled spins, i.e. the panel's
sub-cluster adversary but choosing spins by coupling to {a,b}) for comparison.

usage: python cce_otoc.py [N] [maxsize]
"""
from __future__ import annotations

import itertools
import sys
import time

import numpy as np

import common as C
from qapf.nmr import spins as SP


def subsystem_table(dm, bs, a=0, maxsize=None):
    """F for every subsystem S containing a (and >= 1 observed b), |S| <= maxsize. key = frozenset(S)."""
    N = len(dm)
    others = [i for i in range(N) if i != a]
    maxsize = maxsize or N
    tab = {}
    for k in range(1, maxsize):
        for comb in itertools.combinations(others, k):
            S = (a,) + comb
            bl = [b for b in bs if b in comb]
            if not bl:
                continue
            sub = list(S)
            dms = dm[np.ix_(sub, sub)]
            _, _, F = SP.sector_exact_correlators(dms, C.DT, C.STEPS, 0, [sub.index(b) for b in bl], gamma=0.0,
                                                  record_every=C.REC, otoc=True)
            tab[frozenset(S)] = {b: F[sub.index(b)] for b in bl}
    return tab


def cce(tab, b, R, a, kmax, link="add"):
    """F_est^(k) for k = 0..kmax (list)."""
    g = (lambda F: F) if link == "add" else (lambda F: np.log(np.maximum(F, 1e-6)))
    ginv = (lambda x: x) if link == "add" else np.exp
    gt = {}
    out = []
    acc = None
    for k in range(0, kmax + 1):
        for Cc in itertools.combinations(R, k):
            key = frozenset((a, b) + Cc)
            if key not in tab:
                break
            val = g(tab[key][b]).copy()
            for j in range(0, k):
                for Cp in itertools.combinations(Cc, j):
                    val -= gt[frozenset(Cp)]
            gt[frozenset(Cc)] = val
            acc = val.copy() if acc is None else acc + val
        out.append(ginv(acc))
    return out


def main():
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    maxsize = int(sys.argv[2]) if len(sys.argv) > 2 else N
    res = dict(N=N, maxsize=maxsize, thr=C.THR, clusters={})
    for pdb, probe in C.CLUSTERS:
        tt, S0, F0, ref = C.load_or_make_ref(pdb, probe, N)
        c = C.setup(pdb, probe, N)
        bs, dm = c["bs"], c["dm"]
        t0 = time.process_time()
        tab = subsystem_table(dm, bs, 0, maxsize)
        cpu_tab = time.process_time() - t0
        entry = dict(bs=bs, cpu_table=cpu_tab, n_subsystems=len(tab), orders={})
        Kmax = min(N - 2, maxsize - 2)
        for link in ("add", "mul"):
            ests = {}
            for b in bs:
                R = [i for i in range(N) if i not in (0, b)]
                ests[b] = cce(tab, b, R, 0, Kmax, link)
            for k in range(Kmax + 1):
                Fe = {b: ests[b][k] for b in bs}
                i, tus, err = C.t_c(Fe, F0, bs, tt)
                # cost: number and size of exact sub-simulations needed for order k (all b together)
                nsim = sum(sum(1 for _ in itertools.combinations(range(N - 2), j)) for j in range(k + 1)) * len(bs)
                entry["orders"][f"{link}_k{k}"] = dict(link=link, k=k, max_sub_size=k + 2, t_c_index=i,
                                                       t_c_us=tus, max_err=err.tolist(), n_sub_sims=nsim,
                                                       F_est={str(b): Fe[b].tolist() for b in bs})
        # nested sub-cluster baseline: the k spins most strongly coupled to {a} u bs (single sub-simulation)
        strength = np.abs(dm[[0] + bs]).sum(0)
        rest = [int(i) for i in np.argsort(-strength) if i != 0 and i not in bs]
        for k in range(0, N - len(bs)):
            S = [0] + bs + rest[:k]
            key = frozenset(S)
            if key in tab:
                Fe = {b: tab[key][b] for b in bs}
            else:
                dms = dm[np.ix_(S, S)]
                _, _, Fs = SP.sector_exact_correlators(dms, C.DT, C.STEPS, 0, [S.index(b) for b in bs],
                                                       record_every=C.REC, otoc=True)
                Fe = {b: Fs[S.index(b)] for b in bs}
            i, tus, err = C.t_c(Fe, F0, bs, tt)
            entry["orders"][f"nested_n{len(S)}"] = dict(link="nested", k=k, max_sub_size=len(S), t_c_index=i,
                                                        t_c_us=tus, max_err=err.tolist())
        res["clusters"][f"{pdb}_p{probe}"] = entry
        summ = {kk: (v["t_c_us"] if v["t_c_us"] is not None else "none") for kk, v in entry["orders"].items()}
        print(pdb, probe, N, "cpu_table", round(cpu_tab, 1), "nsub", len(tab), flush=True)
        print("   ", summ, flush=True)
    C.dump(res, f"cce_N{N}.json")


if __name__ == "__main__":
    main()
