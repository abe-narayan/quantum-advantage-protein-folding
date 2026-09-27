"""Minimal quantum proof-of-principle for Program C: the NMR forward model as an explicit shot-based quantum circuit.

Infinite-temperature correlators are estimated the way a quantum computer would: random computational-basis input
|z> (uniform, i.e. the maximally mixed state), a Trotterised dipolar evolution built from the same fused pair gates as
the classical instrument, a single-qubit phase gate, and a projective Z measurement.  Every shot returns +-1.
    transfer  S_ab(t):  |z> -> U^k -> measure Z_a                 estimator  m * z_b
    OTOC(1)   F_ab(t):  |z> -> U^k -> Z_a -> (U^dag)^k -> measure Z_b   estimator  m * z_b
(F_ab = 2^-N sum_z z_b <z| W Z_b W |z>, W = U^-k Z_a U^k, since Z_b|z> = z_b|z>.)
Hardware noise: local depolarising noise after every Trotter step (and every inverse step), probability p_step per
qubit (X, Y, Z with p_step/3 each; Y implemented as XZ up to a global phase), plus symmetric readout error p_ro.
Shots are batched along a trailing axis; noise trajectories are sampled per shot.  Common random numbers (same z, same
noise draws, same measurement uniforms) can be reused across geometries through the seed.
"""
from __future__ import annotations

import numpy as np

from qapf.nmr.spins import apply_step, pair_list, zmul


def _flip_subset(T, N, q, mask):
    ax = N - 1 - q
    return np.where(mask, np.flip(T, axis=ax), T)


def _z_subset(T, N, q, mask):
    k = [slice(None)] * N
    k[N - 1 - q] = 1
    T[tuple(k)] *= np.where(mask, -1.0, 1.0)
    return T


def _noise(T, N, B, p, rng):
    if p <= 0:
        return T
    for q in range(N):
        u = rng.random(B)
        mx = u < 2 * p / 3                   # X or Y  -> X part
        mz = (u >= p / 3) & (u < p)          # Y or Z  -> Z part  (Y ~ XZ)
        if mz.any():
            T = _z_subset(T, N, q, mz)
        if mx.any():
            T = _flip_subset(T, N, q, mx)
    return T


def shots(dmat, dt, k, a, b, n_shots, seed=0, p_step=0.0, p_ro=0.0, otoc=True, batch=256, butterfly=True,
          return_values=False):
    """Mean and standard error of the shot estimator of F_ab (otoc) or S_ab at time k*dt.
    butterfly=False (otoc only): skip Z_a -> the Loschmidt-echo reference f_b(t) (= 1 without noise), used for the
    standard echo-normalisation mitigation F_mit = F / f."""
    N = len(dmat)
    D = 1 << N
    pairs = pair_list(dmat, dt)
    rng = np.random.default_rng(seed)
    vals = []
    done = 0
    while done < n_shots:
        B = min(batch, n_shots - done)
        z = rng.integers(0, D, size=B)
        T = np.zeros((D, B), complex)
        T[z, np.arange(B)] = 1.0
        T = T.reshape((2,) * N + (B,))
        for _ in range(k):
            apply_step(T, N, pairs)
            T = _noise(T, N, B, p_step, rng)
        if otoc:
            if butterfly:
                zmul(T, N, a)
            for _ in range(k):
                apply_step(T, N, pairs, inverse=True)
                T = _noise(T, N, B, p_step, rng)
            q = b
        else:
            q = a
        P = np.abs(T) ** 2
        sl = [slice(None)] * N
        sl[N - 1 - q] = 0
        p0 = P[tuple(sl)].reshape(-1, B).sum(0)
        u = rng.random(B)
        m = np.where(u < p0, 1.0, -1.0)
        flip = rng.random(B) < p_ro
        m = np.where(flip, -m, m)
        zb = 1.0 - 2.0 * ((z >> b) & 1)
        vals.append(m * zb)
        done += B
    v = np.concatenate(vals)
    if return_values:
        return v
    return float(v.mean()), float(v.std(ddof=1) / np.sqrt(len(v)))
