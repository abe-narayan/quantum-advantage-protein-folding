"""ROUND3 lane qemcmc_exact: exact spectral gaps of classical and quantum-enhanced MCMC chains on tabulated energies.

Every chain is Metropolis-Hastings with target pi(s) ∝ exp(-E(s)/T) over s in {0,1}^n.  For a proposal Q the
pi-symmetrised generator is
    Lsym[s,s'] = - min(pi_s Q(s'|s), pi_s' Q(s|s')) / sqrt(pi_s pi_s')          (s != s')
    Lsym[s,s]  =   sum_{s'!=s} min(pi_s Q(s'|s), pi_s' Q(s|s')) / pi_s
(built in log space; no cancellation in the diagonal).  Eigenvalues mu_k = 1 - lambda_k of the transition matrix.
    spectral gap          delta_spec = mu_1
    absolute gap (Layden) delta_abs  = 1 - max_{k>=1} |lambda_k| = min(mu_1, 2 - mu_max)

Chains
  local    single-bit-flip Metropolis (Q = 1/n on Hamming-1 neighbours)
  uniform  Q = 1/N (Layden's "uniform")
  mix(p)   p*uniform + (1-p)*local
  pflip(q) every bit flipped independently with prob. q (= the gamma = 1 pure-mixer quench, classical)
  mf       0.5 * independence proposal from a naive mean-field product fit + 0.5 * local   (idealised: exact MF fit)
  ST       simulated tempering, exact weights (log Z_k from the table; idealised), ladder T_k = T * r^k, K rungs;
           joint chain: w.p. 1/2 a local flip at the current rung, w.p. 1/2 a rung move k -> k +- 1.
  quantum  Layden et al. (Nature 619, 282 (2023)): Q(s'|s) = |<s'| exp(-i H t) |s>|^2,
           H = (1-gamma) * alpha * H_E + gamma * sum_i X_i,  alpha = ||sum X||_F / ||H_E - mean||_F,
           H_E = diag(f(E)), f = identity ("raw") or min(E - Emin, cap) ("clip"; a free design choice since MH corrects).
           U = U^T so Q is symmetric.  Exact U (no Trotter error, no noise): favourable to quantum.

Sparse gaps (local, ST): the grounded pseudo-inverse.  Remove one row/column j of Lsym (v_j = sqrt(pi_j) > 0), LU the
remainder, and run Lanczos on P Lsym^+ P (P projects out v = sqrt(pi)); its top eigenvalue is 1/mu_1.  Validated against
dense eigvalsh.  Values below FLOOR are reported as censored (float64 cannot resolve them reliably).
"""
from __future__ import annotations

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.special import logsumexp

FLOOR = 1e-12


# ------------------------------------------------------------------------------------------- helpers
def popcount(a):
    a = np.asarray(a, np.int64)
    c = np.zeros_like(a)
    while np.any(a):
        c += a & 1
        a >>= 1
    return c


def hamming_matrix(n):
    idx = np.arange(2 ** n)
    return popcount(idx[:, None] ^ idx[None, :])


def logpi(E, T):
    lp = -(E - E.min()) / T
    return lp - logsumexp(lp)


# ------------------------------------------------------------------------------------------- dense generators
def gen_symmetric(Q, E, T):
    """Lsym for a symmetric proposal matrix Q (dense).  Q may include a diagonal (self-proposals are no-ops)."""
    dE = E[None, :] - E[:, None]                      # E_s' - E_s
    off = Q * np.exp(-np.abs(dE) / (2.0 * T))
    np.fill_diagonal(off, 0.0)
    acc = Q * np.exp(-np.maximum(dE, 0.0) / T)          # Q(s'|s) min(1, pi_s'/pi_s)
    np.fill_diagonal(acc, 0.0)
    L = -off
    L[np.diag_indices_from(L)] = acc.sum(1)
    return L


def gen_general(logQ, lp):
    """Lsym for a general proposal (dense), logQ[s, s'] = log Q(s'|s) (may be -inf)."""
    w1 = lp[:, None] + logQ                            # log pi_s Q(s'|s)
    w2 = lp[None, :] + logQ.T                          # log pi_s' Q(s|s')
    m = np.minimum(w1, w2)
    off = np.exp(m - 0.5 * (lp[:, None] + lp[None, :]))
    np.fill_diagonal(off, 0.0)
    rate = np.exp(m - lp[:, None])
    np.fill_diagonal(rate, 0.0)
    L = -off
    L[np.diag_indices_from(L)] = rate.sum(1)
    return L


def gaps_dense(L):
    mu = np.linalg.eigvalsh(L)
    mu1 = float(mu[1]); mumax = float(mu[-1])
    return dict(spec=mu1, abs=min(mu1, 2.0 - mumax), mumax=mumax, mu0=float(mu[0]))


# ------------------------------------------------------------------------------------------- sparse generators
def local_sparse(E, T, n):
    N = 2 ** n
    idx = np.arange(N)
    rows, cols, vals = [], [], []
    diag = np.zeros(N)
    for j in range(n):
        nb = idx ^ (1 << j)
        dE = E[nb] - E
        rows.append(idx); cols.append(nb); vals.append(-(1.0 / n) * np.exp(-np.abs(dE) / (2 * T)))
        diag += (1.0 / n) * np.exp(-np.maximum(dE, 0) / T)
    rows.append(idx); cols.append(idx); vals.append(diag)
    return sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N, N))


def st_sparse(E, T, n, K, r):
    """Simulated tempering joint generator, exact weights. State index = k*N + s."""
    N = 2 ** n
    Ts = T * r ** np.arange(K)
    lz = np.array([logsumexp(-(E - E.min()) / t) for t in Ts])
    lpj = np.concatenate([-(E - E.min()) / Ts[k] - lz[k] for k in range(K)]) - np.log(K)   # joint log pi
    idx = np.arange(N)
    rows, cols, vals = [], [], []
    diag = np.zeros(N * K)
    for k in range(K):
        base = k * N
        for j in range(n):
            nb = idx ^ (1 << j)
            d = lpj[base + nb] - lpj[base + idx]
            q = 0.5 / n
            rows.append(base + idx); cols.append(base + nb); vals.append(-q * np.exp(-np.abs(d) / 2))
            diag[base + idx] += q * np.exp(np.minimum(d, 0))
        for dk in (-1, 1):
            k2 = k + dk
            if 0 <= k2 < K:
                d = lpj[k2 * N + idx] - lpj[base + idx]
                q = 0.25
                rows.append(base + idx); cols.append(k2 * N + idx); vals.append(-q * np.exp(-np.abs(d) / 2))
                diag[base + idx] += q * np.exp(np.minimum(d, 0))
    rows.append(np.arange(N * K)); cols.append(np.arange(N * K)); vals.append(diag)
    L = sp.csc_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(N * K, N * K))
    return L, lpj


def gaps_sparse(L, lp, tol=1e-10):
    """mu_1 via the grounded pseudo-inverse; mu_max via Lanczos."""
    M = L.shape[0]
    v = np.exp(0.5 * lp); v /= np.linalg.norm(v)
    j = int(np.argmax(v))
    keep = np.r_[0:j, j + 1:M]
    Lg = L[keep][:, keep].tocsc()
    lu = spla.splu(Lg)

    def op(x):
        x = np.asarray(x).ravel()
        x = x - v * (v @ x)
        y = np.zeros(M)
        y[keep] = lu.solve(x[keep])
        return y - v * (v @ y)

    A = spla.LinearOperator((M, M), matvec=op, dtype=float)
    rng = np.random.default_rng(0)
    v0 = rng.standard_normal(M); v0 -= v * (v @ v0)
    th = spla.eigsh(A, k=1, which="LA", tol=tol, v0=v0, maxiter=5000, return_eigenvectors=False)[0]
    mu1 = 1.0 / th
    mumax = spla.eigsh(L, k=1, which="LA", tol=1e-8, return_eigenvectors=False, maxiter=5000)[0]
    return dict(spec=float(mu1), abs=float(min(mu1, 2.0 - mumax)), mumax=float(mumax),
                censored=bool(mu1 < FLOOR))


# ------------------------------------------------------------------------------------------- proposals
def Q_uniform(N):
    return np.full((N, N), 1.0 / N)


def Q_local(n):
    Hm = hamming_matrix(n)
    return (Hm == 1).astype(float) / n


def Q_pflip(Hm, n, q):
    return (q ** Hm) * ((1 - q) ** (n - Hm))


def mean_field(E, T, n, sweeps=200, seed=0):
    """naive mean-field product fit q_i = P(bit i = 1) to pi (exact expectations over the table)."""
    N = 2 ** n
    idx = np.arange(N)
    B = ((idx[:, None] >> np.arange(n)[None, :]) & 1).astype(float)     # (N, n)
    q = np.full(n, 0.5)
    Ec = E - E.min()
    for _ in range(sweeps):
        qold = q.copy()
        for i in range(n):
            others = [k for k in range(n) if k != i]
            w = np.prod(np.where(B[:, others] == 1, q[others], 1 - q[others]), axis=1)
            m1 = B[:, i] == 1
            e1 = (w[m1] * Ec[m1]).sum() / w[m1].sum()
            e0 = (w[~m1] * Ec[~m1]).sum() / w[~m1].sum()
            q[i] = 1.0 / (1.0 + np.exp(np.clip((e1 - e0) / T, -700, 700)))
            q[i] = min(max(q[i], 1e-12), 1 - 1e-12)
        if np.max(np.abs(q - qold)) < 1e-10:
            break
    logq = (B * np.log(q) + (1 - B) * np.log(1 - q)).sum(1)
    return q, logq


def H_problem(E, n, mode="raw", cap=40.0):
    f = E - E.min()
    if mode == "clip":
        f = np.minimum(f, cap)
    f = f - f.mean()
    nrm = np.linalg.norm(f)
    N = 2 ** n
    alpha = np.sqrt(n * N) / nrm if nrm > 0 else 1.0
    return alpha * f


def mixer(n):
    N = 2 ** n
    idx = np.arange(N)
    X = np.zeros((N, N))
    for j in range(n):
        X[idx, idx ^ (1 << j)] += 1.0
    return X


class QuantumProposal:
    """Q(gamma, t) = |exp(-i H(gamma) t)|^2 via one eigendecomposition per gamma."""

    def __init__(self, E, n, mode="raw", cap=40.0):
        self.n = n
        self.hp = H_problem(E, n, mode, cap)
        self.X = mixer(n)
        self._g = None

    def set_gamma(self, g):
        Hm = g * self.X
        Hm[np.diag_indices_from(Hm)] += (1 - g) * self.hp
        self.w, self.V = np.linalg.eigh(Hm)
        self._g = g

    def Q(self, t):
        c = np.cos(self.w * t); s = np.sin(self.w * t)
        Re = (self.V * c) @ self.V.T
        Im = (self.V * s) @ self.V.T
        Q = Re * Re + Im * Im
        return 0.5 * (Q + Q.T)
