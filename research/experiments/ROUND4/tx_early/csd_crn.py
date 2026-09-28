"""Classical spin dynamics (CSD) for the two-point part H(t) = sum_j G_aj(t)^2 with COMMON RANDOM NUMBERS across
nested probe-centred clusters.

Model and estimator exactly as ROUND3/r1sim_exact_reach/verify_classical/csd_hydro.py (Elsayed-Fine-type classical
spins, |S| = sqrt(3)/2, H = sum_{i<j} d_ij (2 SzSz - SxSx - SySy), RK4, h = 1 us, isotropic initial conditions,
symmetrised correlator G_aj = [<S_a(t)S_j(0)> + <S_j(t)S_a(0)>]/2 / (s^2/3)), same couplings (b0 = random_b0(1000)).
New here: one batch of initial spins is drawn for the largest cluster N_big and the SAME vectors (first N_q spins) start
every nested sub-cluster N_q (the probe-centred clusters are distance-ordered prefixes of each other), so differences
H_big - H_q have strongly reduced variance.  Per-batch sums are stored, so H and differences get jackknife SEs.

H estimator (unbiased): split batches into G >= 2 groups, H = mean_{g != g'} sum_j Gbar^g_j Gbar^g'_j.
Checkpoint: per-batch sums after every batch (atomic JSON); rerun the same command to resume.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

from kernels import FE, SP
import tx_echo as TX

HERE = os.path.dirname(os.path.abspath(__file__))
S_LEN = math.sqrt(3) / 2


def rhs(S, J, out):
    hx = -(S[:, :, 0] @ J)
    hy = -(S[:, :, 1] @ J)
    hz = 2.0 * (S[:, :, 2] @ J)
    sx, sy, sz = S[:, :, 0], S[:, :, 1], S[:, :, 2]
    np.multiply(hy, sz, out=out[:, :, 0]); out[:, :, 0] -= hz * sy
    np.multiply(hz, sx, out=out[:, :, 1]); out[:, :, 1] -= hx * sz
    np.multiply(hx, sy, out=out[:, :, 2]); out[:, :, 2] -= hy * sx
    return out


def evolve(S, J, h, nsteps, rec_every):
    """returns per-record batch sums of the symmetrised correlator Y_j(t) (nrec, Nc), of the control-variate cross
    moment Y_j(t) C_j with C_j = Y_j(0) = S_a^z(0) S_j^z(0) (nrec, Nc), and sum_traj C_j^2 (Nc)."""
    z0 = S[:, :, 2].copy(); za0 = z0[:, 0].copy()
    C = za0[:, None] * z0                                   # (batch, Nc), E[C_j] = delta_aj s^2/3
    k1 = np.empty_like(S); k2 = np.empty_like(S); k3 = np.empty_like(S); k4 = np.empty_like(S)
    rec = []; cross = []
    for n in range(nsteps + 1):
        if n % rec_every == 0:
            za = S[:, 0, 2]; zj = S[:, :, 2]
            Y = 0.5 * (za[:, None] * z0 + za0[:, None] * zj)
            rec.append(Y.sum(0)); cross.append((Y * C).sum(0))
        if n == nsteps:
            break
        rhs(S, J, k1)
        rhs(S + (0.5 * h) * k1, J, k2)
        rhs(S + (0.5 * h) * k2, J, k3)
        rhs(S + h * k3, J, k4)
        S += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    return (np.array(rec), np.array(cross), (C * C).sum(0),
            float(np.max(np.abs(np.linalg.norm(S, axis=-1) - S_LEN))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--Nbig", type=int, required=True)
    ap.add_argument("--Nq", type=int, nargs="*", default=[18, 20, 22])
    ap.add_argument("--batches", type=int, default=32)
    ap.add_argument("--batch", type=int, default=1000)
    ap.add_argument("--tmax-us", type=float, default=120.0)
    ap.add_argument("--rec-us", type=float, default=40.0)
    ap.add_argument("--h-us", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=515)
    ap.add_argument("--wall-s", type=float, default=520)
    a = ap.parse_args()
    tag = f"csdcrn_1UBQ_p{a.probe}_Nbig{a.Nbig}_q{'-'.join(map(str, a.Nq))}_B{a.batches}x{a.batch}_s{a.seed}"
    out = os.path.join(HERE, "runs", tag + ".json")
    ck = out + ".ckpt.json"
    names, xyz, _ = SP.read_h_coords(os.path.join(FE.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    idx = SP.cluster(xyz, a.probe, a.Nbig)
    for q in a.Nq:                                   # nesting check: prefix of the big cluster == reference cluster
        assert np.array_equal(SP.cluster(xyz, a.probe, q), idx[:q]), q
    sizes = sorted(set(a.Nq + [a.Nbig]))
    Js = {}
    for n in sizes:
        dm = SP.couplings(xyz[idx[:n]], FE.random_b0(1000))
        J = np.asarray(dm, float); np.fill_diagonal(J, 0.0)
        Js[n] = J
    h = a.h_us * 1e-6
    nsteps = int(round(a.tmax_us / a.h_us)); rec_every = int(round(a.rec_us / a.h_us))
    st = dict(done=0, sums={str(n): [] for n in sizes}, cross={str(n): [] for n in sizes},
              csq={str(n): [] for n in sizes}, cpu_s=0.0, norm_drift=0.0)
    if os.path.exists(ck):
        with open(ck) as f:
            st = json.load(f)
    rng = np.random.default_rng(a.seed + 31 * a.Nbig + 7 * a.probe)
    w0 = time.time()
    for ib in range(a.batches):
        v = rng.standard_normal((a.batch, a.Nbig, 3))        # drawn in order -> resume reproducible
        if ib < st["done"]:
            continue
        if time.time() - w0 > a.wall_s:
            break
        c0 = time.process_time()
        v /= np.linalg.norm(v, axis=-1, keepdims=True)
        S0 = v * S_LEN
        for n in sizes:
            rec, cr, csq, dr = evolve(S0[:, :n, :].copy(), Js[n], h, nsteps, rec_every)
            st["sums"][str(n)].append(rec.tolist())
            st["cross"][str(n)].append(cr.tolist())
            st["csq"][str(n)].append(csq.tolist())
            st["norm_drift"] = max(st["norm_drift"], dr)
        st["done"] = ib + 1
        st["cpu_s"] += time.process_time() - c0
        TX.atomic_json(st, ck)
        print(json.dumps(dict(batch=ib, cpu=round(st["cpu_s"], 1))), flush=True)
    complete = st["done"] >= a.batches
    res = dict(probe=a.probe, Nbig=a.Nbig, Nq=a.Nq, sizes=sizes, batch=a.batch, batches_done=st["done"],
               M_done=st["done"] * a.batch, h_us=a.h_us, times_us=[i * a.rec_us for i in range(nsteps // rec_every + 1)],
               seed=a.seed, cpu_s=st["cpu_s"], norm_drift=st["norm_drift"], complete=complete,
               sums_file=os.path.basename(ck))
    TX.atomic_json(res, out)
    print(json.dumps(dict(out=os.path.basename(out), complete=complete, M=res["M_done"], cpu=round(st["cpu_s"], 1))))


if __name__ == "__main__":
    main()
