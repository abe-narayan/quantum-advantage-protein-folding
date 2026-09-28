"""R1-SIM follow-up (PREREG_G1_C1_Q4.md): hybrid quantum-core + classical-spin-bath adversary for the protein 1H echo
F_ab(t) = Tr[W Z_b W Z_b]/2^N, W = U(t)^dag Z_a U(t)  (Starkov & Fine, PRB 98, 214421 (2018)-type, with back-action).

Core: the N_c protons nearest the probe (contains a and the instrument sites b), treated exactly (state vector).
Bath: the next N_b protons (up to the reference cluster size), treated as classical spin vectors |S| = sqrt(3)/2.
Coupling (secular dipolar, spin units I = sigma/2):
    H = sum_{i<j} d_ij (2 I_z^i I_z^j - I_x^i I_x^j - I_y^i I_y^j)
    core feels local fields h_i = sum_{j in bath} d_ij (-S_x^j, -S_y^j, 2 S_z^j)  ->  exp(-i dt h_i . I^i)
    bath spin j feels h_j = sum_{k in bath} d_jk(-S^k_x,-S^k_y,2S^k_z) + sum_{i in core} d_ij(-<I_x^i>,-<I_y^i>,2<I_z^i>)
    (back-action through the core's expectation values), dS_j/dt = h_j x S_j.
Splitting per step dt (Strang): half bath step -> core field rotations(dt/2) -> core pair gates (dt) -> core field
rotations(dt/2) -> half bath step.  Backward evolution = the same map with dt -> -dt (exact reversal when unperturbed).
Echo estimator per sample (random core state psi, random bath B0):  A = W[psi], B = W[Z_b psi] (each W is: joint
forward to t from (state, B0), Z_a on the core, joint backward to 0), F_est = Re <A| Z_b |B>.
Averaged over M samples.  Reference: typicality cone results at N = N_c + N_b (same nested cluster, same b0).
Usage: python hybrid_echo.py --probe 19 --Nc 10 --Ntot 16 --M 200
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

S_LEN = math.sqrt(3) / 2


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def instrument_bs(xyz, probe, K=3, N0=10):
    idx = SP.cluster(xyz, probe, N0)
    X0 = xyz[idx]
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    return sorted(set(far + [int(np.argsort(dist)[1])]))


def single_rotation(T, N, q, h, dt):
    """T <- exp(-i dt h.I_q) T on qubit q (axis N-1-q), h = (hx,hy,hz) real, I = sigma/2 (batched over trailing axis)."""
    hn = math.sqrt(h[0] ** 2 + h[1] ** 2 + h[2] ** 2)
    if hn == 0:
        return T
    th = 0.5 * hn * dt
    c, s = math.cos(th), math.sin(th)
    nx, ny, nz = h[0] / hn, h[1] / hn, h[2] / hn
    # exp(-i th n.sigma) = c I - i s (n.sigma)
    u00 = complex(c, -s * nz); u11 = complex(c, s * nz)
    u01 = complex(-s * ny, -s * nx); u10 = complex(s * ny, -s * nx)
    k0 = [slice(None)] * T.ndim; k0[N - 1 - q] = 0
    k1 = [slice(None)] * T.ndim; k1[N - 1 - q] = 1
    a = T[tuple(k0)].copy(); b = T[tuple(k1)]
    T[tuple(k0)] = u00 * a + u01 * b
    T[tuple(k1)] = u10 * a + u11 * b
    return T


def core_expect(T, N):
    """<I_x>, <I_y>, <I_z> for each core qubit of a normalised state tensor (shape (2,)*N)."""
    out = np.zeros((N, 3))
    for q in range(N):
        ax = N - 1 - q
        a = np.take(T, 0, axis=ax); b = np.take(T, 1, axis=ax)
        ab = np.vdot(a, b)                      # <0|..|1> overlap
        out[q, 0] = ab.real                      # <I_x> = Re <psi|sigma_x|psi>/2 = Re(conj(a) b)
        out[q, 1] = ab.imag                      # <I_y>
        out[q, 2] = 0.5 * (np.vdot(a, a).real - np.vdot(b, b).real)
    return out


def bath_rhs(S, Jbb, Jcb, Icore):
    """dS/dt for bath spins S (Nb,3); Jbb (Nb,Nb), Jcb (Nc,Nb) couplings; Icore (Nc,3) core expectations."""
    h = np.stack([-(Jbb @ S[:, 0]), -(Jbb @ S[:, 1]), 2 * (Jbb @ S[:, 2])], 1)
    h += np.stack([-(Jcb.T @ Icore[:, 0]), -(Jcb.T @ Icore[:, 1]), 2 * (Jcb.T @ Icore[:, 2])], 1)
    return np.cross(h, S)


def bath_step(S, Jbb, Jcb, Icore, dt):
    k1 = bath_rhs(S, Jbb, Jcb, Icore); k2 = bath_rhs(S + 0.5 * dt * k1, Jbb, Jcb, Icore)
    k3 = bath_rhs(S + 0.5 * dt * k2, Jbb, Jcb, Icore); k4 = bath_rhs(S + dt * k3, Jbb, Jcb, Icore)
    return S + (dt / 6) * (k1 + 2 * k2 + 2 * k3 + k4)


def joint_step(T, S, Nc, pairs_fwd, Jcb, Jbb, dt, inverse):
    sg = -1.0 if inverse else 1.0
    h = sg * dt
    Ic = core_expect(T, Nc)
    S = bath_step(S, Jbb, Jcb, Ic, 0.5 * h)
    hf = np.stack([-(Jcb @ S[:, 0]), -(Jcb @ S[:, 1]), 2 * (Jcb @ S[:, 2])], 1)
    for q in range(Nc):
        single_rotation(T, Nc, q, hf[q], 0.5 * h)
    SP.apply_step(T, Nc, pairs_fwd, inverse=inverse)
    for q in range(Nc):
        single_rotation(T, Nc, q, hf[q], 0.5 * h)
    Ic = core_expect(T, Nc)
    S = bath_step(S, Jbb, Jcb, Ic, 0.5 * h)
    return T, S


def W_apply(psi, S0, k, a, Nc, pairs, Jcb, Jbb, dt):
    T = psi.copy(); S = S0.copy()
    for _ in range(k):
        T, S = joint_step(T, S, Nc, pairs, Jcb, Jbb, dt, inverse=False)
    SP.zmul(T, Nc, a)
    for _ in range(k):
        T, S = joint_step(T, S, Nc, pairs, Jcb, Jbb, dt, inverse=True)
    return T


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--Nc", type=int, default=10)
    ap.add_argument("--Ntot", type=int, required=True)
    ap.add_argument("--M", type=int, default=200)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--times-us", default="40,80,120,160,200,240,280,320")
    ap.add_argument("--seed", type=int, default=0)
    a_ = ap.parse_args()
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a_.pdb}_H.pdb"))
    bs = instrument_bs(xyz, a_.probe)
    idx = SP.cluster(xyz, a_.probe, a_.Ntot)
    dm = SP.couplings(xyz[idx], random_b0(1000))           # d_ij (rad/s), same convention as the reference
    Nc = a_.Nc
    Jcc = dm[:Nc, :Nc]; Jcb = dm[:Nc, Nc:]; Jbb = dm[Nc:, Nc:].copy()
    np.fill_diagonal(Jbb, 0.0)
    pairs = SP.pair_list(Jcc, a_.dt)
    rng = np.random.default_rng(a_.seed)
    ks = [int(round(float(t) * 1e-6 / a_.dt)) for t in a_.times_us.split(",")]
    acc = {b: np.zeros(len(ks)) for b in bs}
    t0 = time.time()
    for m in range(a_.M):
        psi = rng.standard_normal((2,) * Nc) + 1j * rng.standard_normal((2,) * Nc)
        psi /= np.linalg.norm(psi)
        v = rng.standard_normal((a_.Ntot - Nc, 3)); v /= np.linalg.norm(v, axis=1, keepdims=True); S0 = v * S_LEN
        for ti, k in enumerate(ks):
            A = W_apply(psi, S0, k, 0, Nc, pairs, Jcb, Jbb, a_.dt)
            for b in bs:
                B = W_apply(SP.zmul(psi.copy(), Nc, b), S0, k, 0, Nc, pairs, Jcb, Jbb, a_.dt)
                acc[b][ti] += float(np.real(np.vdot(A, SP.zmul(B.copy(), Nc, b))))
    F = {str(b): (acc[b] / a_.M).tolist() for b in bs}
    out = dict(pdb=a_.pdb, probe=a_.probe, Nc=Nc, Ntot=a_.Ntot, M=a_.M, bs=bs, times_us=[k * a_.dt * 1e6 for k in ks],
               F=F, se_est=float(1 / math.sqrt(a_.M) * 2 ** (-Nc / 2)), secs=time.time() - t0)
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "out", f"{a_.pdb}_p{a_.probe}_Nc{Nc}_Ntot{a_.Ntot}.json"), "w"))
    print(json.dumps(dict(Nc=Nc, Ntot=a_.Ntot, secs=round(out["secs"], 1))))


if __name__ == "__main__":
    main()
