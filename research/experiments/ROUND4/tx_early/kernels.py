"""Sector Trotter-step kernels for the T-X-early lane.

`ClipSectorKernel` applies exactly the same fused pair gates, in the same order, as
ROUND3/r1sim_exact_reach/fastecho.SectorKernel (the reference first-order Trotter circuit of spins.pair_list /
apply_step, global phase factored out), but with
  * np.take / np.put in mode='clip' (no per-element bounds check; indices are valid by construction),
  * preallocated temporaries (no per-gate allocation of be * x),
so the arithmetic per element is identical (c * x_r + s * x_q, same operand order) and results agree with
SectorKernel to rounding.  Validated in `validate.py`.
"""
from __future__ import annotations

import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
LANE3 = os.path.join(ROOT, "research", "experiments", "ROUND3", "r1sim_exact_reach")
sys.path.insert(0, LANE3)
import fastecho as FE  # noqa: E402
from fastecho import SP  # noqa: E402,F401


class ClipSectorKernel:
    def __init__(self, N, idx, pairs, dtype=np.complex64):
        self.maps = FE.sector_pair_maps(N, idx, pairs, np.intp)
        cdt = np.dtype(dtype)
        self.fwd = [(cdt.type(a), cdt.type(b)) for a, b in FE.gate_coefs(pairs)]
        self.inv = [(cdt.type(a), cdt.type(b)) for a, b in FE.gate_coefs(pairs, inverse=True)]
        m = max((len(r) for r, _ in self.maps), default=0)
        self.b1 = np.empty(m, dtype); self.b2 = np.empty(m, dtype)
        self.b3 = np.empty(m, dtype); self.b4 = np.empty(m, dtype)
        self.nbytes_maps = sum(r.nbytes + q.nbytes for r, q in self.maps)

    def step(self, v, inverse=False):
        if inverse:
            seq = zip(reversed(self.maps), reversed(self.inv))
        else:
            seq = zip(self.maps, self.fwd)
        take, put, mul, add = np.take, np.put, np.multiply, np.add
        for (r, q), (al, be) in seq:
            n = len(r)
            if n == 0:
                continue
            xr = self.b1[:n]; xq = self.b2[:n]; t = self.b3[:n]; u = self.b4[:n]
            take(v, r, out=xr, mode="clip")
            take(v, q, out=xq, mode="clip")
            mul(xr, al, out=t)
            mul(xq, be, out=u)
            add(t, u, out=t)
            put(v, r, t, mode="clip")
            mul(xq, al, out=t)
            mul(xr, be, out=u)
            add(t, u, out=t)
            put(v, q, t, mode="clip")
        return v
