"""Classical-spin-dynamics (CSD) estimate of the TWO-POINT part of the echo, H(t) = sum_j G_aj(t)^2,
G_aj(t) = Tr[Z_a(t) Z_j]/2^N, on clusters far beyond exact reach.

Model (as spins.classical_spin_correlators): classical vectors |S| = sqrt(3)/2, H = sum_{i<j} d_ij (2 S_i^z S_j^z -
S_i^x S_j^x - S_i^y S_j^y), dS_i/dt = h_i x S_i, RK4, infinite-temperature (isotropic) initial conditions.
G_aj^cl(t) = <S_a^z(t) S_j^z(0)> / (s^2/3), symmetrised with <S_j^z(t) S_a^z(0)> (time-reversal symmetry of a
quadratic Hamiltonian) to cut variance.  H is estimated UNBIASED from two independent halves: H = sum_j G^A_j G^B_j.
Continuous time (no Trotter); the Trotter offset of the reference circuit is measured separately (trotter_H.py).
Checkpoint: accumulators after every batch (atomic JSON).  Single-threaded BLAS expected (OMP/MKL/OPENBLAS=1).
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
sys.path.insert(0, HERE)
import decomp_echo as DE  # noqa: E402

S_LEN = math.sqrt(3) / 2


def rhs(S, J, out):
    # h = (-(Sx J), -(Sy J), 2 (Sz J));  dS/dt = h x S
    hx = -(S[:, :, 0] @ J)
    hy = -(S[:, :, 1] @ J)
    hz = 2.0 * (S[:, :, 2] @ J)
    sx, sy, sz = S[:, :, 0], S[:, :, 1], S[:, :, 2]
    np.multiply(hy, sz, out=out[:, :, 0]); out[:, :, 0] -= hz * sy
    np.multiply(hz, sx, out=out[:, :, 1]); out[:, :, 1] -= hx * sz
    np.multiply(hx, sy, out=out[:, :, 2]); out[:, :, 2] -= hy * sx
    return out


def run(probe, Nc, M, batch, h_us, rec_us, t_max_us, seed, ckpt, dtype=np.float64, log=print, budget_s=None,
        family="probe"):
    dm, bs, names, xyz, gidx = DE.load_cluster("1UBQ", probe, Nc, family)
    J = np.asarray(dm, dtype)
    np.fill_diagonal(J, 0.0)
    h = h_us * 1e-6
    nsteps = int(round(t_max_us / h_us))
    rec_every = int(round(rec_us / h_us))
    nrec = nsteps // rec_every + 1
    st = dict(done=0, acc=[np.zeros((nrec, Nc)).tolist(), np.zeros((nrec, Nc)).tolist()], n=[0, 0], secs=0.0)
    if ckpt and os.path.exists(ckpt):
        st = json.load(open(ckpt))
    acc = [np.array(st["acc"][0]), np.array(st["acc"][1])]
    nb_total = M // batch
    rng = np.random.default_rng(seed + 31 * Nc + 7 * probe)
    t0 = time.time()
    for ib in range(nb_total):
        v = rng.standard_normal((batch, Nc, 3))          # drawn in order -> resume reproducible
        if ib < st["done"]:
            continue
        if budget_s is not None and time.time() - t0 > budget_s:
            break
        ts = time.time()
        v /= np.linalg.norm(v, axis=-1, keepdims=True)
        S = (v * S_LEN).astype(dtype)
        z0 = S[:, :, 2].copy()
        za0 = z0[:, 0].copy()
        k1 = np.empty_like(S); k2 = np.empty_like(S); k3 = np.empty_like(S); k4 = np.empty_like(S)
        half = ib % 2
        loc = np.zeros((nrec, Nc))
        ri = 0
        for n in range(nsteps + 1):
            if n % rec_every == 0:
                za = S[:, 0, 2]
                zj = S[:, :, 2]
                # symmetrised: <S_a(t) S_j(0)> + <S_j(t) S_a(0)>
                loc[ri] = 0.5 * (za @ z0 + za0 @ zj)
                ri += 1
            if n == nsteps:
                break
            rhs(S, J, k1)
            rhs(S + (0.5 * h) * k1, J, k2)
            rhs(S + (0.5 * h) * k2, J, k3)
            rhs(S + h * k3, J, k4)
            S += (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        acc[half] += loc
        st["n"][half] += batch
        st["done"] = ib + 1
        st["secs"] += time.time() - ts
        st["acc"] = [acc[0].tolist(), acc[1].tolist()]
        st["norm_drift"] = float(np.max(np.abs(np.linalg.norm(S, axis=-1) - S_LEN)))
        if ckpt:
            json.dump(st, open(ckpt + ".tmp", "w"))
            os.replace(ckpt + ".tmp", ckpt)
        if log:
            log(json.dumps(dict(batch=ib, secs=round(time.time() - ts, 1), cum=round(st["secs"], 1))))
    norm = S_LEN ** 2 / 3.0
    nA, nB = st["n"]
    complete = st["done"] >= nb_total
    res = dict(probe=probe, Nc=Nc, family=family, M_done=nA + nB, h_us=h_us, times_us=[i * rec_us for i in range(nrec)],
               complete=complete, cpu_secs=st["secs"], norm_drift=st.get("norm_drift"))
    if nA > 0 and nB > 0:
        GA = acc[0] / (nA * norm)
        GB = acc[1] / (nB * norm)
        G = (acc[0] + acc[1]) / ((nA + nB) * norm)
        res.update(G=G.tolist(), H_unbiased=np.sum(GA * GB, axis=1).tolist(), H_biased=np.sum(G ** 2, axis=1).tolist(),
                   sumG=G.sum(1).tolist(),
                   H_se_est=(np.sqrt(np.sum(G ** 2, 1) * 2.0 / (nA + nB)) + np.sqrt(Nc) / (nA + nB)).tolist())
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--Nc", type=int, required=True)
    ap.add_argument("--M", type=int, default=8000)
    ap.add_argument("--batch", type=int, default=1000)
    ap.add_argument("--h-us", type=float, default=1.0)
    ap.add_argument("--rec-us", type=float, default=40.0)
    ap.add_argument("--tmax-us", type=float, default=320.0)
    ap.add_argument("--seed", type=int, default=99)
    ap.add_argument("--budget-s", type=float, default=780)
    ap.add_argument("--family", default="probe")
    a = ap.parse_args()
    tag = f"csd_1UBQ_p{a.probe}_Nc{a.Nc}_M{a.M}_h{a.h_us}" + ("" if a.family == "probe" else "_" + a.family.replace(":", "-").replace(",", "_"))
    out = os.path.join(HERE, "runs", tag + ".json")
    if os.path.exists(out):
        print("exists", out); return
    res = run(a.probe, a.Nc, a.M, a.batch, a.h_us, a.rec_us, a.tmax_us, a.seed, out + ".ckpt.json",
              budget_s=a.budget_s, family=a.family)
    if res["complete"]:
        json.dump(res, open(out + ".tmp", "w"), indent=1)
        os.replace(out + ".tmp", out)
        os.remove(out + ".ckpt.json")
        print(json.dumps(dict(done=tag, cpu=round(res["cpu_secs"], 1), H=[round(x, 4) for x in res["H_unbiased"]])))
    else:
        print(json.dumps(dict(partial=True, M_done=res["M_done"])))


if __name__ == "__main__":
    main()
