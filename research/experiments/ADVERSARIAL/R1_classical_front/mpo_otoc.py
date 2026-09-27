"""E4: matrix-product-operator (MPO / operator-TEBD) adversary for the echo F_ab(t).

The Heisenberg operator O(t) = U(t)^dag Z_a U(t) is stored as a real MPS in the orthonormal Pauli basis {I,X,Y,Z}
(local dim 4) along a chain.  Every pair gate of the SAME Trotter circuit (same order: Heisenberg = reversed pair list per
step) is applied as its exact 16x16 real orthogonal Pauli-transfer matrix on two ADJACENT chain sites; non-adjacent pairs
are made adjacent by SWAPs of the moving qubit (positions tracked, no swap-back).  After each 2-site update the bond is
truncated to at most chi singular values (mixed-canonical form, orthogonality centre at the updated bond, so the
truncation is locally optimal in Frobenius norm).
    F_ab(t) = sum_P c_P^2 s_b(P) / sum_P c_P^2,    s_b = diag(+1,-1,-1,+1) on the Pauli index of qubit b
(normalised: the truncation loses norm; the normalised form is the standard, stronger estimator).
Initial chain order: spectral (Fiedler) ordering of the |d_ij| graph.
Cost per step: O(#gates + #swaps) SVDs of (4 chi x 4 chi) -> polynomial in N at fixed chi (the needed chi is the question).

usage: python mpo_otoc.py chi [pdb probe] [N]
"""
from __future__ import annotations

import sys
import time

import numpy as np
import scipy.linalg as sla

import common as C
from qapf.nmr import spins as SP

PAULI = [np.eye(2, dtype=complex), np.array([[0, 1], [1, 0]], complex), np.array([[0, -1j], [1j, 0]]),
         np.array([[1, 0], [0, -1]], complex)]
P2 = [np.kron(PAULI[p], PAULI[q]) for p in range(4) for q in range(4)]
SB = np.array([1.0, -1.0, -1.0, 1.0])


def ptm_pair(ddt):
    """16x16 real PTM of O -> g^dag O g, g = exp(-i ddt (1/4)(2ZZ - XX - YY))."""
    H = 0.25 * (2 * P2[15] - P2[5] - P2[10])
    g = sla.expm(-1j * ddt * H)
    T = np.empty((16, 16))
    for b in range(16):
        Ob = g.conj().T @ P2[b] @ g
        for al in range(16):
            T[al, b] = np.real(np.trace(P2[al] @ Ob)) / 4.0
    return T


SWAP = np.zeros((16, 16))
for p in range(4):
    for q in range(4):
        SWAP[4 * q + p, 4 * p + q] = 1.0


class MPS:
    def __init__(self, N, a, order, chi, cut=1e-13):
        self.N, self.chi, self.cut = N, chi, cut
        self.order = list(order)                 # order[k] = qubit at chain position k
        self.pos = {q: k for k, q in enumerate(self.order)}
        self.A = []
        for k in range(N):
            t = np.zeros((1, 4, 1)); t[0, 3 if self.order[k] == a else 0, 0] = 1.0
            self.A.append(t)
        self.c = 0
        self.disc = 0.0
        self.nsvd = 0
        self.maxchi = 1

    def move(self, p):
        A = self.A
        while self.c < p:
            l, d, r = A[self.c].shape
            Q, R = np.linalg.qr(A[self.c].reshape(l * d, r))
            A[self.c] = Q.reshape(l, d, -1)
            A[self.c + 1] = np.tensordot(R, A[self.c + 1], axes=(1, 0))
            self.c += 1
        while self.c > p:
            l, d, r = A[self.c].shape
            Q, R = np.linalg.qr(A[self.c].reshape(l, d * r).T)
            A[self.c] = Q.T.reshape(-1, d, r)
            A[self.c - 1] = np.tensordot(A[self.c - 1], R.T, axes=(2, 0))
            self.c -= 1

    def apply2(self, p, T):
        """apply 16x16 T to chain sites (p, p+1); T index = 4*s_p + s_{p+1}."""
        self.move(p)
        A0, A1 = self.A[p], self.A[p + 1]
        l, r = A0.shape[0], A1.shape[2]
        th = np.tensordot(A0, A1, axes=(2, 0))                 # l, 4, 4, r
        th = np.tensordot(T.reshape(4, 4, 4, 4), th, axes=([2, 3], [1, 2]))   # 4,4,l,r
        th = th.transpose(2, 0, 1, 3).reshape(l * 4, 4 * r)
        try:
            U, s, Vt = np.linalg.svd(th, full_matrices=False)
        except np.linalg.LinAlgError:
            U, s, Vt = sla.svd(th, full_matrices=False, lapack_driver="gesvd")
        self.nsvd += 1
        s2 = s ** 2
        tot = s2.sum()
        k = min(self.chi, int(np.sum(s2 > self.cut * tot)) or 1)
        self.disc += float(s2[k:].sum() / max(tot, 1e-300))
        self.maxchi = max(self.maxchi, k)
        self.A[p] = U[:, :k].reshape(l, 4, k)
        self.A[p + 1] = (s[:k, None] * Vt[:k]).reshape(k, 4, r)
        self.c = p + 1

    def swap_adjacent(self, p):
        self.apply2(p, SWAP)
        qa, qb = self.order[p], self.order[p + 1]
        self.order[p], self.order[p + 1] = qb, qa
        self.pos[qa], self.pos[qb] = p + 1, p

    def gate(self, i, j, T):
        while abs(self.pos[i] - self.pos[j]) > 1:
            pi = self.pos[i]
            self.swap_adjacent(pi if self.pos[j] > pi else pi - 1)
        p = min(self.pos[i], self.pos[j])
        self.apply2(p, T)                                     # T symmetric under qubit exchange (H_ij symmetric)

    def otoc(self, bs):
        out = {}
        for b in bs:
            p = self.pos[b]
            self.move(p)
            A = self.A[p]
            w = (A ** 2).sum(axis=(0, 2))
            out[b] = float((w * SB).sum() / w.sum())
        return out


def fiedler_order(dm):
    W = np.abs(dm)
    L = np.diag(W.sum(1)) - W
    _, v = np.linalg.eigh(L)
    return list(np.argsort(v[:, 1]))


def run(dm, bs, chi, a=0, order=None):
    N = len(dm)
    pairs = SP.pair_list(dm, C.DT)
    Ts = {(i, j): ptm_pair(ddt) for (i, j, ddt) in pairs}
    m = MPS(N, a, order or fiedler_order(dm), chi)
    F = {b: [] for b in bs}
    nsw = 0
    for k in range(C.STEPS + 1):
        if k % C.REC == 0:
            f = m.otoc(bs)
            for b in bs:
                F[b].append(f[b])
        if k == C.STEPS:
            break
        for (i, j, ddt) in reversed(pairs):
            n0 = m.nsvd
            m.gate(i, j, Ts[(i, j)])
            nsw += m.nsvd - n0 - 1
    return {b: np.array(v) for b, v in F.items()}, dict(nsvd=m.nsvd, nswaps=nsw, disc=m.disc, maxchi=m.maxchi)


def main():
    chi = int(sys.argv[1])
    clusters = C.CLUSTERS if len(sys.argv) < 4 else [(sys.argv[2], int(sys.argv[3]))]
    N = int(sys.argv[4]) if len(sys.argv) > 4 else 10
    for pdb, probe in clusters:
        tt, S0, F0, ref = C.load_or_make_ref(pdb, probe, N)
        c = C.setup(pdb, probe, N)
        t0 = time.process_time()
        Fe, st = run(c["dm"], c["bs"], chi)
        cpu = time.process_time() - t0
        i, tus, err = C.t_c(Fe, F0, c["bs"], tt)
        rec = dict(pdb=pdb, probe=probe, N=N, chi=chi, bs=c["bs"], t_c_index=i, t_c_us=tus, max_err=err.tolist(),
                   cpu=cpu, F_est={str(b): Fe[b].tolist() for b in c["bs"]}, **st)
        C.dump(rec, f"mpo_{pdb}_p{probe}_N{N}_chi{chi}.json")
        print(pdb, probe, N, "chi", chi, "t_c_us", tus, "err@t:", " ".join(f"{e:.3f}" for e in err), "cpu",
              round(cpu, 1), st, flush=True)


if __name__ == "__main__":
    main()
