"""R1-SIM exact classical reach: fast exact (typicality) evaluation of the protein 1H first-order echo
    F_ab(t) = Tr[W Z_b W Z_b] / 2^N,   W = U(t)^dag Z_a U(t),
and the transfer S_ab(t) = Tr[Z_a(t) Z_b]/2^N, for the SAME first-order Trotter circuit as
src/qapf/nmr/spins.pair_list/apply_step (dt = 2 us, fused exact pair propagators in the fixed order (0,1),(0,2),...),
plus a continuous-time (Chebyshev, exact exp(-iHt)) variant for the Trotter-error audit.

Engineering levers relative to the reference (scripts/nmr_cone.py, which applies apply_step on a (2,)*N tensor):
  L1  sector restriction: H, every pair gate, Z_a and Z_b conserve total Z, so every vector lives in magnetisation
      sectors; each sector is evolved separately (peak memory = largest sector C(N, N/2), not 2^N).
  L2  global spin-flip symmetry P = X^{(x)N}: P commutes with every pair gate and anticommutes with Z_a, Z_b, so
      Tr_k[W Z_b W Z_b] = Tr_{N-k}[...] and Tr_k[Z_a(t) Z_b] = Tr_{N-k}[...]  (DERIVED); only sectors k <= N/2 are
      evolved (weight 2 for k < N/2).
  L3  forward reuse: U(t_k) psi and U(t_k) Z_b psi are propagated once through all echo times (the reference
      recomputes the forward leg for every time point); only the backward legs are per time point.
      Trotter steps per vector: n_steps + sum_k k  (880 for 160 steps, echo every 20) vs 2 sum_k k (1440) + forward.
  L4  global-phase factoring: each fused pair gate is e^{-ia} * [1 on |00>,|11>;  e^{2ia}[[c, is],[is, c]] on
      {|01>,|10>}]; the scalar e^{-ia} cancels exactly in W and in S, so only the flip-flop subspace is touched.
  L5  precision: complex64 option (error budget checked against complex128).
Kernels: 'sector' (numpy gather/scatter with precomputed int index arrays, per sector) and 'full' (numpy strided
5-D views on the full 2^N vector, no index memory).  Both reproduce the reference circuit exactly.

Reference-psi mode: with psi0 drawn exactly as the reference (rng seed 12345, standard complex normal on (2,)*N,
normalised on the full space) and all sectors evolved, the estimator is algebraically identical to the reference
(full-space vdot = sum of sector vdots), so results must agree to rounding (validation).
"""
from __future__ import annotations

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

_PC16 = np.array([bin(i).count("1") for i in range(1 << 16)], np.int64)


# ----------------------------------------------------------------------------- instrument definition (as reference)
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


def load_instance(pdb, probe, N):
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    bs = instrument_bs(xyz, probe)
    idx = SP.cluster(xyz, probe, N)
    dm = SP.couplings(xyz[idx], random_b0(1000))
    return dm, bs, [names[idx[b]] for b in bs], xyz[idx]


def reference_psi0(N, seed=12345):
    """exactly the reference draw (scripts/nmr_cone.py / spins.exact_correlators with n_rand=1)."""
    rng = np.random.default_rng(seed)
    shape = (2,) * N
    psi0 = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    psi0 /= np.linalg.norm(psi0)
    return psi0.reshape(-1)          # flat index = sum_q bit_q 2^q (axis N-1-q <-> qubit q)


# ----------------------------------------------------------------------------- sectors
def popcounts(N):
    x = np.arange(1 << N, dtype=np.int64)
    return _PC16[x & 0xFFFF] + _PC16[(x >> 16) & 0xFFFF]


def sector_index(N, k, pc=None):
    pc = popcounts(N) if pc is None else pc
    return np.nonzero(pc == k)[0]


def sector_pair_maps(N, idx, pairs, itype=np.intp):
    """for each pair (i,j): positions r (bit i = 0, bit j = 1) and partner positions q (bit i = 1, bit j = 0)
    inside the sector with sorted basis idx."""
    D = 1 << N
    pos = np.full(D, -1, dtype=np.int64)
    pos[idx] = np.arange(len(idx))
    maps = []
    for (i, j, _) in pairs:
        bi = (idx >> i) & 1
        bj = (idx >> j) & 1
        r = np.nonzero((bi == 0) & (bj == 1))[0]
        q = pos[idx[r] ^ ((1 << i) | (1 << j))]
        maps.append((r.astype(itype), q.astype(itype)))
    del pos
    return maps


def gate_coefs(pairs, inverse=False):
    """(alpha, beta) per pair for the phase-factored flip-flop block e^{2ia}[[c, is],[is, c]] (a -> -a if inverse)."""
    out = []
    for (_, _, ddt) in pairs:
        a = (-1.0 if inverse else 1.0) * ddt / 2.0
        e2 = complex(math.cos(2 * a), math.sin(2 * a))
        out.append((e2 * math.cos(a), e2 * 1j * math.sin(a)))
    return out


class SectorKernel:
    """Trotter step restricted to one magnetisation sector (gather/scatter)."""

    def __init__(self, N, idx, pairs, dtype=np.complex128, itype=np.intp):
        self.maps = sector_pair_maps(N, idx, pairs, itype)
        cf = gate_coefs(pairs)
        ci = gate_coefs(pairs, inverse=True)
        cdt = np.dtype(dtype)
        self.fwd = [(cdt.type(a), cdt.type(b)) for a, b in cf]
        self.inv = [(cdt.type(a), cdt.type(b)) for a, b in ci]
        m = max((len(r) for r, _ in self.maps), default=0)
        self.b1 = np.empty(m, dtype); self.b2 = np.empty(m, dtype); self.b3 = np.empty(m, dtype)
        self.nbytes_maps = sum(r.nbytes + q.nbytes for r, q in self.maps)

    def step(self, v, inverse=False):
        if inverse:
            seq = zip(reversed(self.maps), reversed(self.inv))
        else:
            seq = zip(self.maps, self.fwd)
        for (r, q), (al, be) in seq:
            n = len(r)
            if n == 0:
                continue
            xr = self.b1[:n]; xq = self.b2[:n]; t = self.b3[:n]
            np.take(v, r, out=xr)
            np.take(v, q, out=xq)
            np.multiply(xr, al, out=t)
            t += be * xq               # one temporary
            v[r] = t
            np.multiply(xq, al, out=t)
            t += be * xr
            v[q] = t
        return v


class FullKernel:
    """Trotter step on the full 2^N vector with strided 5-D views (no index memory)."""

    def __init__(self, N, pairs, dtype=np.complex128):
        self.N = N
        self.pairs = pairs
        cdt = np.dtype(dtype)
        self.fwd = [(cdt.type(a), cdt.type(b)) for a, b in gate_coefs(pairs)]
        self.inv = [(cdt.type(a), cdt.type(b)) for a, b in gate_coefs(pairs, inverse=True)]
        self.buf = np.empty(1 << max(N - 2, 0), dtype)

    def step(self, v, inverse=False):
        N = self.N
        if inverse:
            seq = zip(reversed(self.pairs), reversed(self.inv))
        else:
            seq = zip(self.pairs, self.fwd)
        for (i, j, _), (al, be) in seq:
            V = v.reshape(1 << (N - 1 - j), 2, 1 << (j - i - 1), 2, 1 << i)
            x01 = V[:, 1, :, 0, :]          # bit j = 1, bit i = 0
            x10 = V[:, 0, :, 1, :]
            t = self.buf.reshape(x01.shape)
            np.multiply(x01, al, out=t)
            t += be * x10
            x10 *= al
            x10 += be * x01
            x01[...] = t
        return v


# ----------------------------------------------------------------------------- echo drivers
def _zs(N, q, idx):
    return (1.0 - 2.0 * ((idx >> q) & 1)).astype(np.float64)


def echo_sector(dm, dt, steps, every, a, bs, mode="reference", dtype=np.complex128, seed=12345, ckpt=None,
                log=None, sectors=None):
    """Sector-restricted typicality echo with forward reuse.
    mode='reference': psi0 = reference draw, all sectors 0..N (must reproduce the reference to rounding).
    mode='flip'     : independent complex-normal vector per sector k <= N/2, flip-symmetry weights
                      (estimator sum_k m_k (D_k/2^N) <x_k|A|x_k>, m_k = 2 for k < N/2 else 1).
    ckpt: path of a JSON checkpoint; completed sectors are stored and skipped on restart."""
    N = len(dm)
    pairs = SP.pair_list(dm, dt)
    otimes = list(range(0, steps + 1, every))
    pc = popcounts(N)
    psi_full = reference_psi0(N, seed) if mode == "reference" else None
    if sectors is None:
        sectors = list(range(N + 1)) if mode == "reference" else list(range(N // 2 + 1))
    st = dict(done={}, secs=0.0)
    if ckpt and os.path.exists(ckpt):
        st = json.load(open(ckpt))
    t0 = time.time() - st.get("secs", 0.0)
    rng = np.random.default_rng(seed + 7919 * N)
    stats = dict(sector_secs={}, peak_sector_dim=0, map_bytes=0)
    for k in sectors:
        # independent per-sector draws (drawn in order so a resumed run reproduces the same vectors)
        idx = np.nonzero(pc == k)[0]
        Dk = len(idx)
        if mode == "flip":
            x = rng.standard_normal(Dk) + 1j * rng.standard_normal(Dk)
            x /= np.linalg.norm(x)
            m = 1.0 if (2 * k == N) else 2.0
            wgt = m * Dk / float(1 << N)
        if str(k) in st["done"]:
            continue
        ts = time.time()
        if mode == "reference":
            psi = psi_full[idx].astype(dtype)
            wgt = 1.0
        else:
            psi = x.astype(dtype)
        za = _zs(N, a, idx)
        zb = {b: _zs(N, b, idx) for b in bs}
        K = SectorKernel(N, idx, pairs, dtype)
        stats["peak_sector_dim"] = max(stats["peak_sector_dim"], Dk)
        stats["map_bytes"] = max(stats["map_bytes"], K.nbytes_maps)
        phi = psi.copy()
        chi = {b: zb[b] * psi for b in bs}
        Fk = {b: [] for b in bs}
        Sk = {b: [] for b in bs}
        for n in range(steps + 1):
            if n in otimes:
                u = za * phi
                for b in bs:
                    Sk[b].append(float(np.real(np.vdot(u, chi[b]))) * wgt)
                if n == 0:
                    for b in bs:
                        Fk[b].append(float(np.real(np.vdot(psi, psi))) * wgt)
                else:
                    ub = u.copy()
                    for _ in range(n):
                        K.step(ub, inverse=True)
                    ub *= 1.0                      # (keeps dtype)
                    for b in bs:
                        vb = za * chi[b]
                        for _ in range(n):
                            K.step(vb, inverse=True)
                        Fk[b].append(float(np.real(np.vdot(zb[b] * ub, vb))) * wgt)
                    del ub, vb
            if n == steps:
                break
            K.step(phi)
            for b in bs:
                K.step(chi[b])
        st["done"][str(k)] = dict(F={str(b): Fk[b] for b in bs}, S={str(b): Sk[b] for b in bs}, Dk=int(Dk),
                                  secs=time.time() - ts)
        stats["sector_secs"][str(k)] = time.time() - ts
        st["secs"] = time.time() - t0
        if ckpt:
            json.dump(st, open(ckpt + ".tmp", "w"))
            os.replace(ckpt + ".tmp", ckpt)
        if log:
            log(dict(sector=k, Dk=int(Dk), secs=round(time.time() - ts, 2), total=round(st["secs"], 1)))
        del K, phi, chi, psi
    F = {str(b): np.sum([st["done"][str(k)]["F"][str(b)] for k in sectors], axis=0).tolist() for b in bs}
    S = {str(b): np.sum([st["done"][str(k)]["S"][str(b)] for k in sectors], axis=0).tolist() for b in bs}
    return dict(times_us=[n * dt * 1e6 for n in otimes], F=F, S=S, secs=time.time() - t0, stats=stats)


def trotter_steps_per_run(steps, every, nb):
    otimes = list(range(every, steps + 1, every))
    return dict(reference=(1 + nb) * (2 * sum(otimes)) + (1 + nb) * steps,
                forward_reuse=(1 + nb) * (steps + sum(otimes)))
