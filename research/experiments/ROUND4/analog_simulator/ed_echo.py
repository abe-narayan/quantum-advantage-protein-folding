"""Exact continuous-time echo for the protein 1H secular dipolar network, with forward/backward Hamiltonians that
may differ (imperfect analog reversal).  Library for the ROUND4 analog_simulator lane.

Target model (identical to src/qapf/nmr/spins.py, continuous time instead of the dt = 2 us Trotter circuit):
    H_dd = sum_{i<j} (d_ij/4) (2 Z_i Z_j - X_i X_j - Y_i Y_j)
Generic Z-conserving pair Hamiltonian used for perturbed/engineered models:
    H = sum_{i<j} [ Jxy_ij (X_i X_j + Y_i Y_j) + Jz_ij Z_i Z_j ] + sum_i h_i Z_i
Heisenberg component with the same spatial pattern (the part an electric-dipole platform cannot remove by global
rotations):  H_S = sum_{i<j} (d_ij/4)(XX + YY + ZZ).  ||per-pair coefficient|| of H_S equals that of H_dd, so a
relative admixture lambda is a relative-norm error.

Measured signal of the echo protocol (infinite temperature; butterfly = pi_z pulse on probe a; read Z_b):
    S_ab(t) = Tr[ Z_b V Z_a U Z_b U^dag Z_a V^dag ] / 2^N,  U = exp(-i H_f t),  V = exp(+i H_b t)
With H_b = H_f this is F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b]/2^N (the repo's OTOC(1)).
No-butterfly reference (Loschmidt-type normaliser): R_b(t) = Tr[Z_b V U Z_b U^dag V^dag]/2^N (= 1 if V = U^dag).

Evaluation: per magnetisation sector k, dense eigendecomposition H_k = Q E Q^T (real symmetric), then
    S_k = Tr[C_b K C_f K^T],  C = e^{-iEt} (Q^T Z_b Q) e^{+iEt},  K = Q_b^T Z_a Q_f      (DERIVED; validated vs repo)
Global spin-flip symmetry (valid when h = 0) halves the sector work.
"""
from __future__ import annotations

import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "experiments", "ROUND3", "r1sim_exact_reach"))
from qapf.nmr import spins as SP  # noqa: E402
import fastecho as FE  # noqa: E402

_PC16 = np.array([bin(i).count("1") for i in range(1 << 16)], np.int64)


def load(pdb, probe, N):
    """(dm [rad/s], bs, xyz [A], b0) exactly as the ROUND3 reference instrument (probe = cluster index 0)."""
    if N < 10:      # FE.load_instance indexes instrument sites of the N0 = 10 cluster; take the nearest-N subset
        dm, bs, names, xyz = FE.load_instance(pdb, probe, 10)
        return dm[:N, :N].copy(), [b for b in bs if b < N], xyz[:N].copy(), FE.random_b0(1000)
    dm, bs, names, xyz = FE.load_instance(pdb, probe, N)
    return dm, bs, xyz, FE.random_b0(1000)


def couplings(xyz, b0):
    return SP.couplings(xyz, b0)


def pair_params(dm, lam=0.0):
    """(Jxy, Jz) matrices for H_dd + lam * H_S."""
    return (-1.0 + lam) * dm / 4.0, (2.0 + lam) * dm / 4.0


class Sectors:
    def __init__(self, N, use_flip=True):
        self.N = N
        x = np.arange(1 << N, dtype=np.int64)
        pc = _PC16[x & 0xFFFF] + _PC16[(x >> 16) & 0xFFFF]
        self.use_flip = use_flip
        ks = range(N // 2 + 1) if use_flip else range(N + 1)
        self.ks = list(ks)
        self.idx = {k: np.nonzero(pc == k)[0] for k in self.ks}
        self.wt = {k: ((1.0 if 2 * k == N else 2.0) if use_flip else 1.0) for k in self.ks}
        self.pos = {}
        for k in self.ks:
            p = np.full(1 << N, -1, np.int64)
            p[self.idx[k]] = np.arange(len(self.idx[k]))
            self.pos[k] = p

    def z(self, k, q):
        return (1.0 - 2.0 * ((self.idx[k] >> q) & 1)).astype(float)

    def hamiltonian(self, k, Jxy, Jz, h=None):
        N = self.N
        idx = self.idx[k]
        D = len(idx)
        H = np.zeros((D, D))
        s = [(1.0 - 2.0 * ((idx >> q) & 1)) for q in range(N)]
        diag = np.zeros(D)
        for i in range(N):
            if h is not None:
                diag += h[i] * s[i]
            for j in range(i + 1, N):
                if Jz[i, j] != 0.0:
                    diag += Jz[i, j] * s[i] * s[j]
                if Jxy[i, j] != 0.0:
                    bi = (idx >> i) & 1
                    bj = (idx >> j) & 1
                    r = np.nonzero(bi != bj)[0]
                    q = self.pos[k][idx[r] ^ ((1 << i) | (1 << j))]
                    H[r, q] += 2.0 * Jxy[i, j]
        H[np.arange(D), np.arange(D)] += diag
        return H


def eig_model(sec, Jxy, Jz, h=None):
    out = {}
    for k in sec.ks:
        H = sec.hamiltonian(k, Jxy, Jz, h)
        E, Q = np.linalg.eigh(H)
        out[k] = (E, Q)
    return out


def _cmul(C, R):
    """complex C @ real R via two real matmuls."""
    return (C.real @ R) + 1j * (C.imag @ R)


def echo(sec, model_f, a, bs, times_s, model_b=None, want_R=False):
    """S_ab(t) (and R_b(t)) for all b in bs, t in times_s (seconds). model_* = eig_model(...) output."""
    N = sec.N
    same = model_b is None
    S = {b: np.zeros(len(times_s)) for b in bs}
    R = {b: np.zeros(len(times_s)) for b in bs} if (want_R and not same) else None
    for k in sec.ks:
        Ef, Qf = model_f[k]
        if len(Ef) == 0:
            continue
        w = sec.wt[k]
        za = sec.z(k, a)
        if same:
            Zaq = Qf.T @ (za[:, None] * Qf)
        else:
            Eb, Qb = model_b[k]
            K = Qb.T @ (za[:, None] * Qf)
            L = Qb.T @ Qf if want_R else None
        for b in bs:
            zb = sec.z(k, b)
            Zbf = Qf.T @ (zb[:, None] * Qf)
            if not same:
                Zbb = Qb.T @ (zb[:, None] * Qb)
            for it, t in enumerate(times_s):
                pf = np.exp(-1j * Ef * t)
                Cf = pf[:, None] * Zbf * pf.conj()[None, :]
                if same:
                    X = _cmul(Cf, Zaq)
                    S[b][it] += w * float(np.real(np.sum(X * X.T)))
                else:
                    pb = np.exp(-1j * Eb * t)
                    Cb = pb[:, None] * Zbb * pb.conj()[None, :]
                    A = _cmul(Cb, K)
                    B = _cmul(Cf, K.T)
                    S[b][it] += w * float(np.real(np.sum(A * B.T)))
                    if R is not None:
                        A2 = _cmul(Cb, L)
                        B2 = _cmul(Cf, L.T)
                        R[b][it] += w * float(np.real(np.sum(A2 * B2.T)))
    norm = float(1 << N)
    S = {b: (v / norm).tolist() for b, v in S.items()}
    if R is not None:
        R = {b: (v / norm).tolist() for b, v in R.items()}
    return S, R


def two_point_H(sec, model, a, times_s):
    """H(t) = sum_j G_aj(t)^2 with G_aj = Tr[Z_a(t) Z_j]/2^N (the b-independent two-point part of F)."""
    N = sec.N
    G = np.zeros((N, len(times_s)))
    for k in sec.ks:
        E, Q = model[k]
        w = sec.wt[k]
        za = sec.z(k, a)
        Zaq = Q.T @ (za[:, None] * Q)
        for j in range(N):
            zj = sec.z(k, j)
            Zjq = Q.T @ (zj[:, None] * Q)
            for it, t in enumerate(times_s):
                p = np.exp(-1j * E * t)
                C = p[:, None] * Zaq * p.conj()[None, :]
                G[j, it] += w * float(np.real(np.sum(C * Zjq.T)))
    G /= float(1 << N)
    return (G ** 2).sum(0).tolist()
