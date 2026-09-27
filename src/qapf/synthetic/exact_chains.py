"""Exact spectral analysis of classical Markov chains and their Szegedy quantisations on small state spaces.

Purpose (Program B, mechanism lab): quantify, EXACTLY, how the spectral gap of the best classical chain behaves on
tunable landscapes (funnel, golf course, hide-and-seek, persistence, spin glass, learned-protein-derived) and what
quantum simulated annealing (QSA) would save in walk steps, before any resource accounting.

Facts used (standard):
  * For a reversible chain P with stationary pi, the Szegedy walk W(P) has eigenphases +-theta with cos(theta) = lambda
    for each eigenvalue lambda of P (Szegedy 2004), so its phase gap is Delta = arccos(lambda_2) ~ sqrt(2 delta),
    delta = 1 - lambda_2 (spectral gap of a lazy/positive chain).
  * Classical annealing/tempering cost ~ sum_k t_rel(P_k) log(1/eps); QSA cost ~ sum_k 1/Delta_k (Somma et al. 2008;
    Wocjan & Abeyesinghe 2008) provided consecutive stationary states overlap by a constant (we compute the overlaps).
All matrices are built explicitly (sparse); sizes up to ~2^17 states (or states x temperatures for tempering).
"""
from __future__ import annotations

import math

import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla


# ----------------------------------------------------------------------------- landscapes on {0,1}^n
def hypercube_neighbors(n):
    N = 1 << n
    idx = np.arange(N)
    return np.stack([idx ^ (1 << b) for b in range(n)], 1)          # (N, n)


def popcount(a):
    a = np.asarray(a, np.int64)
    c = np.zeros_like(a)
    while np.any(a):
        c += a & 1
        a >>= 1
    return c


def landscape(kind, n, rng, **kw):
    """Energies E(x) for x in {0,1}^n (index = integer bitstring).  All scaled so that typical barriers ~ O(n)."""
    N = 1 << n
    x = np.arange(N)
    target = int(rng.integers(N))
    ham = popcount(x ^ target)
    if kind == "funnel":                     # smooth bias toward the target + weak roughness
        return -kw.get("J", 1.0) * (n - ham) + kw.get("rough", 0.3) * rng.standard_normal(N)
    if kind == "golf":                       # flat except a single deep hole (unstructured search)
        E = np.zeros(N); E[target] = -kw.get("depth", 1.5 * n); return E
    if kind == "hideseek":                   # weak funnel toward a DECOY + narrow deep well (Hamming radius r) at target
        decoy = int(rng.integers(N)); hd = popcount(x ^ decoy)
        E = -kw.get("J", 0.5) * (n - hd)
        r = kw.get("r", 1)
        E = np.where(ham <= r, -kw.get("depth", 1.2 * n) + 0.5 * ham, E)
        return E.astype(float)
    if kind == "persistence":                # wide shallow basin (decoy) + narrow deep basin (target), comparable mass
        decoy = int(rng.integers(N)); hd = popcount(x ^ decoy)
        Ew = -kw.get("Jw", 0.6) * np.maximum(n / 2 - hd, 0)
        En = -kw.get("Jn", 3.0) * np.maximum(kw.get("rn", 2) - ham, 0) - kw.get("depth", 0.35 * n) * (ham == 0)
        return np.minimum(Ew, En).astype(float)
    if kind == "sk":                         # Sherrington-Kirkpatrick spin glass
        J = rng.standard_normal((n, n)) / math.sqrt(n); J = np.triu(J, 1); J = J + J.T
        s = 2.0 * ((x[:, None] >> np.arange(n)[None]) & 1) - 1.0
        return -0.5 * np.einsum("ai,ij,aj->a", s, J, s)
    raise ValueError(kind)


# ----------------------------------------------------------------------------- chains
def metropolis_single_flip(E, nbr, beta, lazy=0.5):
    """Lazy single-site Metropolis on a graph with uniform proposal over neighbours (nbr: (N,k) indices)."""
    N, k = nbr.shape
    rows = np.repeat(np.arange(N), k)
    cols = nbr.ravel()
    a = np.minimum(1.0, np.exp(-beta * (E[cols] - E[rows]))) / k
    P = sp.csr_matrix(((1 - lazy) * a, (rows, cols)), shape=(N, N))
    stay = 1.0 - np.asarray(P.sum(1)).ravel()
    return P + sp.diags(stay)


def gibbs(E, beta):
    w = -beta * (E - E.min())
    p = np.exp(w - w.max())
    return p / p.sum()


def spectral_gap(P, pi):
    """delta = 1 - lambda_2 of a reversible P (via the symmetrised matrix); also returns |lambda|_max excluding 1."""
    d = np.sqrt(pi)
    S = sp.diags(d) @ P @ sp.diags(1.0 / d)
    S = 0.5 * (S + S.T)
    N = S.shape[0]
    if N <= 3000:
        w = np.linalg.eigvalsh(S.toarray())
        w = np.sort(w)
        lam2 = w[-2]
    else:
        # deflate the top eigenvector (known: sqrt(pi)) and find the largest remaining eigenvalue
        u = d / np.linalg.norm(d)
        op = spla.LinearOperator((N, N), matvec=lambda v: S @ v - u * (u @ (S @ v)), dtype=float)
        lam2 = float(spla.eigsh(op, k=1, which="LA", tol=1e-9, maxiter=20000)[0][0])
    return 1.0 - lam2


def simulated_tempering(E, nbr, betas, logZ, lazy=0.5, p_temp=0.5):
    """Simulated tempering on (state, level) with exact weights logZ (optimal ST: uniform level marginal).
    Moves: with prob p_temp propose level +-1 (Metropolis on the extended target), else single-flip Metropolis
    at the current level.  Returns (P, pi) on the product space (level-major)."""
    R = len(betas); N = len(E)
    blocks = []
    for r, b in enumerate(betas):
        blocks.append(metropolis_single_flip(E, nbr, b, lazy=lazy))
    rows, cols, vals = [], [], []
    stay = np.zeros(R * N)
    for r in range(R):
        Pr = blocks[r].tocoo()
        rows.append(Pr.row + r * N); cols.append(Pr.col + r * N); vals.append((1 - p_temp) * Pr.data)
        for dr in (-1, 1):
            q = r + dr
            if 0 <= q < R:
                # target pi(x, r) ∝ exp(-b_r E(x) - logZ_r)
                logacc = -(betas[q] - betas[r]) * (E - E.min()) - (logZ[q] - logZ[r])
                a = np.minimum(1.0, np.exp(np.minimum(logacc, 0.0))) * (p_temp / 2)
                rows.append(np.arange(N) + r * N); cols.append(np.arange(N) + q * N); vals.append(a)
    P = sp.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(R * N, R * N))
    diag = 1.0 - np.asarray(P.sum(1)).ravel()
    P = P + sp.diags(diag)
    pi = np.concatenate([gibbs(E, b) for b in betas]) / R
    return P, pi


def log_partition(E, betas):
    e = E - E.min()
    return np.array([np.log(np.exp(-b * e).sum()) for b in betas])


def szegedy_phase_gap(delta):
    return math.acos(max(-1.0, min(1.0, 1.0 - delta)))


def annealing_costs(E, nbr, betas):
    """Exact classical vs QSA walk-step costs along an inverse-temperature schedule (single-flip Metropolis):
    classical ~ sum_k 1/delta_k, quantum ~ sum_k 1/Delta_k (Delta = arccos(1-delta)); returns also the minimum
    squared overlap between consecutive stationary states (QSA requires it bounded below)."""
    deltas, ovl = [], []
    prev = None
    for b in betas:
        P = metropolis_single_flip(E, nbr, b)
        pi = gibbs(E, b)
        deltas.append(spectral_gap(P, pi))
        if prev is not None:
            ovl.append(float(np.sum(np.sqrt(prev * pi)) ** 2))
        prev = pi
    deltas = np.array(deltas)
    Dq = np.array([szegedy_phase_gap(d) for d in deltas])
    return dict(deltas=deltas, classical=float(np.sum(1.0 / deltas)), quantum=float(np.sum(1.0 / Dq)),
                min_overlap2=float(min(ovl)) if ovl else 1.0)


# ----------------------------------------------------------------------------- learned-protein-derived discrete landscapes
def kary_neighbors(n, k):
    """States of {0..k-1}^n (index = base-k number); neighbours differ in exactly one digit."""
    N = k ** n
    idx = np.arange(N)
    digits = (idx[:, None] // (k ** np.arange(n))[None]) % k
    nb = []
    for i in range(n):
        for dv in range(1, k):
            nd = digits.copy(); nd[:, i] = (nd[:, i] + dv) % k
            nb.append((nd * (k ** np.arange(n))[None]).sum(1))
    return np.stack(nb, 1), digits


def protein_register_landscape(out, L, window, k=3, T=1.0, batch=4096):
    """Discrete landscape from the learned A80 energy (qapf.protein.energy): residues i in `window` (a list of
    positions in 1..L-3) choose one of their top-k (theta,tau) head bins (bin-centre angles); all other residues are
    fixed at their MAP head bin.  E(state) = A80 energy of the built chain / T.  Exact enumeration of k^len(window).
    NOTE: an unrelaxed discrete PROXY of the continuous posterior (condition-C caveats of S29-S33 apply to accuracy;
    here only the landscape's sampling structure is studied)."""
    import torch
    from qapf.protein import energy as EN
    from qapf.protein import esmprior_v1 as EP
    en = EN.Energy(out, L)
    tt = np.asarray(out["theta_tau_prob"], float)          # (L, 9, 24)
    th_c = np.radians(EP.TH_CENTRES); ta_c = np.radians(EP.TA_CENTRES)
    base_th = np.full(L - 2, np.radians(110.0)); base_ta = np.zeros(L - 3)
    choices = {}
    for i in range(1, L - 2):
        flat = tt[i].ravel()
        order = np.argsort(-flat)[:max(k, 1)]
        a, c = np.divmod(order, 24)
        base_th[i - 1] = th_c[a[0]]; base_ta[i - 1] = ta_c[c[0]]
        choices[i] = (th_c[a], ta_c[c], flat[order])
    n = len(window)
    nbr, digits = kary_neighbors(n, k)
    N = k ** n
    E = np.empty(N)
    logprior = np.zeros(N)
    for s in range(0, N, batch):
        d = digits[s:s + batch]
        th = np.tile(base_th, (len(d), 1)); ta = np.tile(base_ta, (len(d), 1))
        for j, i in enumerate(window):
            th[:, i - 1] = choices[i][0][d[:, j]]; ta[:, i - 1] = choices[i][1][d[:, j]]
            logprior[s:s + batch] += np.log(choices[i][2][d[:, j]] + 1e-12)
        E[s:s + batch] = en(np.concatenate([th, ta], 1), grad=False)[0]
    return E / T, nbr, logprior
