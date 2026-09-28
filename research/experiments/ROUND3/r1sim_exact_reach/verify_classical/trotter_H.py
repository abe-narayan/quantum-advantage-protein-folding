"""Deterministic exact G_aj(t) and H(t) = sum_j G_aj^2 for (i) the reference Trotter circuit (spins.sector_step_unitaries)
and (ii) exact continuous time exp(-iHt) (dense eigh of each sector Hamiltonian), N = 12, 14.  Purpose: the size of the
Trotter offset on the two-point part H (CSD is continuous time) and a noise-free H ladder anchor.
Output: trotter_H.json"""
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decomp_echo as DE  # noqa: E402
from decomp_echo import SP  # noqa: E402


def sector_H(N, idx, dm):
    D = 1 << N
    pos = np.full(D, -1, dtype=np.int64)
    pos[idx] = np.arange(len(idx))
    Dk = len(idx)
    Hm = np.zeros((Dk, Dk))
    for i in range(N):
        zi = 1.0 - 2.0 * ((idx >> i) & 1)
        for j in range(i + 1, N):
            d = dm[i, j]
            zj = 1.0 - 2.0 * ((idx >> j) & 1)
            Hm[np.arange(Dk), np.arange(Dk)] += 0.5 * d * zi * zj
            bi = (idx >> i) & 1
            bj = (idx >> j) & 1
            r = np.nonzero(bi != bj)[0]
            q = pos[idx[r] ^ ((1 << i) | (1 << j))]
            Hm[r, q] += -0.5 * d
    return Hm


def G_from_eig(Q, lam, N, idx, a, steps):
    Qh = Q.conj().T
    A = (Qh * (1.0 - 2.0 * ((idx >> a) & 1))) @ Q
    out = np.zeros((len(steps), N))
    lc = lam.conj()
    for j in range(N):
        B = (Qh * (1.0 - 2.0 * ((idx >> j) & 1))) @ Q
        M = A * B.T
        for ti, n in enumerate(steps):
            out[ti, j] = float(np.real((M * np.outer(lc ** n, lam ** n)).sum()))
    return out


def main():
    t0 = time.time()
    steps = list(range(20, 161, 20))
    rep = dict(times_us=[2 * s for s in steps])
    for probe in (19, 245):
        for N in (12, 14):
            dm, bs, names, xyz, gidx = DE.load_cluster("1UBQ", probe, N, "probe")
            Gt = np.zeros((len(steps), N)); Gc = np.zeros((len(steps), N))
            for idx, Uk in SP.sector_step_unitaries(dm, DE.DT):
                Q, lam = SP._unitary_eig(Uk)
                Gt += G_from_eig(Q, lam, N, idx, 0, steps)
                E, V = np.linalg.eigh(sector_H(N, idx, dm))
                Gc += G_from_eig(V.astype(complex), np.exp(-1j * E * DE.DT), N, idx, 0, steps)
            Gt /= 2 ** N; Gc /= 2 ** N
            Ht = (Gt ** 2).sum(1); Hc = (Gc ** 2).sum(1)
            rep[f"p{probe}_N{N}"] = dict(H_trotter=Ht.tolist(), H_cont=Hc.tolist(),
                                         maxdiff_H=float(np.max(np.abs(Ht - Hc))),
                                         maxdiff_G=float(np.max(np.abs(Gt - Gc))),
                                         sumG_trotter=Gt.sum(1).tolist(), G_trotter=Gt.tolist(), G_cont=Gc.tolist())
            print(probe, N, "H_trot", np.round(Ht, 4), "\n        H_cont", np.round(Hc, 4),
                  "maxdiff H %.4f G %.4f" % (np.max(np.abs(Ht - Hc)), np.max(np.abs(Gt - Gc))), flush=True)
    rep["secs"] = time.time() - t0
    json.dump(rep, open(os.path.join(HERE, "trotter_H.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
