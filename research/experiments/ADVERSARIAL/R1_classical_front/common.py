"""Shared setup for the R1 classical-front adversaries (echo / first-order OTOC F_ab(t)).

Cluster, field orientation, observed spins b and Trotter circuit are IDENTICAL to scripts/nmr_gate.py:
  cluster  = N protons nearest the probe (qapf.nmr.spins.cluster), probe = local index 0
  b0       = random_b0(1000 + orient)
  bs       = 3 farthest cluster protons + the nearest one
  circuit  = first-order Trotter, dt = 2 us, 160 steps, fixed pair order (i<j lexicographic), record every 10 steps.
Reference = qapf.nmr.spins.sector_exact_correlators (deterministic, validated 1e-15 vs dense matrix).
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

DT = 2e-6
STEPS = 160
REC = 10
THR = 0.01
CLUSTERS = [("1UBQ", 19), ("1UBQ", 245), ("1PGA", 390)]
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def setup(pdb, probe, N, orient=0, K=3):
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    idx = SP.cluster(xyz, probe, N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    dm = SP.couplings(X0, b0)
    return dict(pdb=pdb, probe=probe, N=N, X=X0, b0=b0, dm=dm, bs=bs, dist=dist,
                names=[names[i] for i in idx])


def exact_F(dm, bs, a=0, steps=STEPS, rec=REC):
    tt, S, F = SP.sector_exact_correlators(dm, DT, steps, a, bs, gamma=0.0, record_every=rec, otoc=True)
    return tt, S, F


def ref_path(pdb, probe, N):
    return os.path.join(OUT, f"ref_{pdb}_p{probe}_N{N}.json")


def load_or_make_ref(pdb, probe, N):
    """Exact reference (cached)."""
    p = ref_path(pdb, probe, N)
    if os.path.exists(p):
        r = json.load(open(p))
        return np.array(r["times"]), {int(k): np.array(v) for k, v in r["S"].items()}, \
            {int(k): np.array(v) for k, v in r["F"].items()}, r
    c = setup(pdb, probe, N)
    t0 = time.process_time()
    tt, S, F = exact_F(c["dm"], c["bs"])
    secs = time.process_time() - t0
    r = dict(pdb=pdb, probe=probe, N=N, bs=c["bs"], dist_bs=[float(c["dist"][b]) for b in c["bs"]],
             times=tt.tolist(), S={str(b): S[b].tolist() for b in c["bs"]}, F={str(b): F[b].tolist() for b in c["bs"]},
             cpu_secs=secs)
    json.dump(r, open(p, "w"))
    return tt, S, F, r


def t_c(Fest, Fex, bs, times, thr=THR):
    """first recorded time where max_b |Fest - Fex| > thr (returns (index, time_us or None, maxerr per t))."""
    err = np.max(np.stack([np.abs(np.asarray(Fest[b]) - np.asarray(Fex[b])) for b in bs]), axis=0)
    bad = np.nonzero(err > thr)[0]
    i = int(bad[0]) if len(bad) else len(times)
    return i, (round(float(times[i]) * 1e6, 3) if i < len(times) else None), err


def tc_us(i, times):
    return float(times[i]) * 1e6 if i < len(times) else float("inf")


def dump(obj, name):
    def _np(o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    p = os.path.join(OUT, name)
    json.dump(obj, open(p + ".tmp", "w"), default=_np, indent=1)
    os.replace(p + ".tmp", p)
    return p
