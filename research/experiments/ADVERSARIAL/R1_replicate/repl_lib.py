"""Independent re-implementation (R1 replicate lens) of the NMR echo-window instrument.

Written from the physical specification only.  It does NOT import any correlator/propagator code from
src/qapf/nmr/spins.py.  Only the geometry readers read_h_coords / cluster are reused, and couplings() is
re-derived here and cross-checked against the original.

Conventions (from the spec):
  H = sum_{i<j} (d_ij/4) (2 Z_i Z_j - X_i X_j - Y_i Y_j),
  d_ij = 2 pi * 120.1 kHz * (1 A / r_ij)^3 * (3 cos^2 beta_ij - 1)/2   [rad/s].
  qubit q = bit q of the computational-basis index.
  Trotter step U = g_M ... g_1, with g_k = exp(-i dt H_{i_k j_k}) (an exact 4x4 pair propagator) and the pairs in
  lexicographic order (0,1),(0,2),...,(N-2,N-1); g_1 = pair (0,1) acts first on a state.
  S_ab(t) = Tr[Z_a(t) Z_b]/2^N,  F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b]/2^N,  Z_a(t) = U(t)^dag Z_a U(t).

Two independent engines:
  (1) dense: builds the 2^N x 2^N step unitary from scipy.linalg.expm of each 4x4 pair Hamiltonian embedded by
      bit manipulation, then Heisenberg-evolves Z_a with dense matrix products (checked against a full Kronecker-product
      expm for one pair);
  (2) Pauli-transfer-matrix (PTM) Heisenberg propagation: the coefficient vector over ALL 4^N Pauli strings is
      stored densely (N=10: 4^10 = 1,048,576 doubles = 8 MB) and each pair gate acts as its exact 16x16 PTM on two
      tensor axes.  Coefficient-threshold truncation ("sparse Pauli dynamics") zeroes every |c| <= eps after each pair
      gate (or after each step).  Dense storage of a sparse algorithm is mathematically identical to a hash-map
      implementation; it is simply cheap at N=10.
"""
from __future__ import annotations

import math

import numpy as np
import scipy.linalg as sla
import scipy.sparse as sps

D1A = 2 * math.pi * 120.1e3          # rad/s at 1 A (1H-1H), from the spec

P_I = np.eye(2, dtype=complex)
P_X = np.array([[0, 1], [1, 0]], dtype=complex)
P_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
P_Z = np.array([[1, 0], [0, -1]], dtype=complex)
PAULIS = [P_I, P_X, P_Y, P_Z]        # digit convention for the PTM engine: 0=I 1=X 2=Y 3=Z


def random_b0(seed):
    """identical definition to scripts/nmr_gate.py::random_b0 (copied, 3 lines)."""
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def my_couplings(X, b0):
    X = np.asarray(X, float)
    b0 = np.asarray(b0, float) / np.linalg.norm(b0)
    N = len(X)
    d = np.zeros((N, N))
    for i in range(N):
        for j in range(i + 1, N):
            v = X[j] - X[i]
            r = float(np.sqrt(v @ v))
            cb = float(v @ b0) / r
            d[i, j] = d[j, i] = D1A / r ** 3 * (3 * cb * cb - 1) / 2
    return d


def pair_hamiltonian_local(dij):
    """4x4 H_ij in the local basis kron(qubit i, qubit j), local index l = 2*b_i + b_j."""
    return (dij / 4.0) * (2 * np.kron(P_Z, P_Z) - np.kron(P_X, P_X) - np.kron(P_Y, P_Y))


def pair_unitary_local(dij, dt):
    return sla.expm(-1j * dt * pair_hamiltonian_local(dij))


def embed_local(Mloc, i, j, N):
    """sparse 2^N x 2^N embedding of a 4x4 operator on qubits (i, j), local index l = 2*b_i + b_j."""
    D = 1 << N
    s = np.arange(D, dtype=np.int64)
    bi = (s >> i) & 1
    bj = (s >> j) & 1
    lin = 2 * bi + bj
    base = s & ~((1 << i) | (1 << j))
    rows, cols, vals = [], [], []
    for lout in range(4):
        sout = base | ((lout >> 1) << i) | ((lout & 1) << j)
        rows.append(sout); cols.append(s); vals.append(Mloc[lout, lin])
    M = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(D, D))
    M.eliminate_zeros()
    return M


def full_single(P, q, N):
    """dense 2^N operator P on qubit q via Kronecker products (qubit N-1 = most significant = leftmost factor)."""
    out = np.array([[1.0 + 0j]])
    for k in range(N - 1, -1, -1):
        out = np.kron(out, P if k == q else P_I)
    return out


def pairs_lex(N):
    return [(i, j) for i in range(N) for j in range(i + 1, N)]


def trotter_step_unitary(dmat, dt):
    """U = g_M ... g_1 (dense), pairs lexicographic, g_1 = (0,1) first."""
    N = len(dmat)
    U = np.eye(1 << N, dtype=complex)
    for (i, j) in pairs_lex(N):
        G = embed_local(pair_unitary_local(dmat[i, j], dt), i, j, N)
        U = G @ U
    return np.asarray(U)


def full_hamiltonian_sparse(dmat):
    N = len(dmat)
    H = sps.csr_matrix((1 << N, 1 << N), dtype=complex)
    for (i, j) in pairs_lex(N):
        H = H + embed_local(pair_hamiltonian_local(dmat[i, j]), i, j, N)
    return H


def zdiag(q, N):
    return 1.0 - 2.0 * ((np.arange(1 << N) >> q) & 1)


def dense_correlators(V, a, bs, n_rec, N):
    """V = propagator for ONE recording interval.  Returns S[b], F[b] (arrays of length n_rec+1) and the max
    imaginary parts (sanity)."""
    D = 1 << N
    za = zdiag(a, N)
    W = np.eye(D, dtype=complex)
    S = {b: np.zeros(n_rec + 1) for b in bs}
    F = {b: np.zeros(n_rec + 1) for b in bs}
    imax = 0.0
    zbs = {b: zdiag(b, N) for b in bs}
    for k in range(n_rec + 1):
        O = W.conj().T @ (za[:, None] * W)                # Z_a(t) = W^dag Z_a W
        OT = O.T
        for b in bs:
            zb = zbs[b]
            s = np.sum(np.diag(O) * zb) / D
            f = np.sum(O * OT * zb[:, None] * zb[None, :]) / D   # Tr[(O Zb)(O Zb)] = sum_rc O_rc zb_c O_cr zb_r
            S[b][k] = s.real; F[b][k] = f.real
            imax = max(imax, abs(s.imag), abs(f.imag))
        if k < n_rec:
            W = V @ W
    return S, F, imax


def exact_trotter(dmat, dt, steps, rec, a, bs):
    N = len(dmat)
    U = trotter_step_unitary(dmat, dt)
    V = np.linalg.matrix_power(U, rec)
    S, F, im = dense_correlators(V, a, bs, steps // rec, N)
    unit_err = float(np.abs(U.conj().T @ U - np.eye(1 << N)).max())
    return S, F, dict(imag_max=im, unitarity_err=unit_err)


def exact_continuous(dmat, dt, steps, rec, a, bs):
    """no Trotterisation: V = expm(-i H rec*dt) of the full Hamiltonian (dense expm)."""
    N = len(dmat)
    H = full_hamiltonian_sparse(dmat).toarray()
    V = sla.expm(-1j * H * (rec * dt))
    S, F, im = dense_correlators(V, a, bs, steps // rec, N)
    return S, F, dict(imag_max=im)


# ============================================================================ PTM Pauli propagation
def pair_ptm(Uloc):
    """R[g,d,a,b] with U^dag (P_a x P_b) U = sum_{g,d} R[g,d,a,b] (P_g x P_d); real for Hermitian Paulis."""
    R = np.zeros((4, 4, 4, 4))
    imx = 0.0
    for a_ in range(4):
        for b_ in range(4):
            Q = Uloc.conj().T @ np.kron(PAULIS[a_], PAULIS[b_]) @ Uloc
            for g in range(4):
                for d in range(4):
                    v = np.trace(np.kron(PAULIS[g], PAULIS[d]) @ Q) / 4.0
                    R[g, d, a_, b_] = v.real
                    imx = max(imx, abs(v.imag))
    assert imx < 1e-12, imx
    return R


def pauli_propagate(dmat, dt, steps, rec, a, bs, eps=0.0, trunc="pair", max_steps=None):
    """Heisenberg evolution of Z_a through the SAME Trotter circuit as trotter_step_unitary, in the Pauli basis.
    c has shape (4,)*N with axis q <-> qubit q.  U^dag O U = g_1^dag...g_M^dag O g_M...g_1  => within a step the
    pair gates are applied to the operator in REVERSED lexicographic order.
    trunc = 'pair': zero |c| <= eps after every pair gate (as in sparse Pauli dynamics);  'step': after each step.
    Returns per recorded time: S_b = c(Z_b), F_b = sum_P c_P^2 s_P (s_P = -1 iff P has X or Y on b),
    norm2 = sum c^2 (= Tr[O^2]/2^N), n_strings = #nonzero."""
    N = len(dmat)
    prs = pairs_lex(N)
    Rs = [pair_ptm(pair_unitary_local(dmat[i, j], dt)) for (i, j) in prs]
    c = np.zeros((4,) * N)
    idx0 = [0] * N; idx0[a] = 3
    c[tuple(idx0)] = 1.0
    last = steps if max_steps is None else min(steps, max_steps)
    out = dict(steps=[], S={b: [] for b in bs}, F={b: [] for b in bs}, norm2=[], n_strings=[])
    zb_idx = {}
    for b in bs:
        k = [0] * N; k[b] = 3; zb_idx[b] = tuple(k)

    def record(k):
        c2 = c * c
        tot = float(c2.sum())
        out["steps"].append(k); out["norm2"].append(tot); out["n_strings"].append(int(np.count_nonzero(c)))
        for b in bs:
            out["S"][b].append(float(c[zb_idx[b]]))
            xy = float(np.take(c2, [1, 2], axis=b).sum())
            out["F"][b].append(tot - 2 * xy)

    for k in range(last + 1):
        if k % rec == 0:
            record(k)
        if k == last:
            break
        for n in range(len(prs) - 1, -1, -1):
            i, j = prs[n]
            c = np.moveaxis(np.tensordot(Rs[n], c, axes=([2, 3], [i, j])), [0, 1], [i, j])
            c = np.ascontiguousarray(c)
            if eps > 0 and trunc == "pair":
                c[np.abs(c) <= eps] = 0.0
        if eps > 0 and trunc == "step":
            c[np.abs(c) <= eps] = 0.0
    return out
