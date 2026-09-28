"""Operator-size growth K(t) of the probe operator Z_a(t) in LARGER protein 1H clusters (N up to 30), for the secular
and the PHYSICAL double-quantum Hamiltonian, to feed the K(t)-dependent decoherence model
Gamma(t) = Gamma_1 K(t)^alpha  (Dominguez et al. PRA 104, 012402 (2021): decay rate of the Loschmidt-echo fidelity
grows as K^alpha with the number K of correlated spins; alpha ~ 0.48 at weak, ~0.96 at strong perturbation).

K(t) := norm-weighted mean Pauli weight of the kept strings (the 'average Hamming weight' reading of the cluster size;
MQC-based K differs by an O(1) factor, Alvarez & Suter PRA 84, 012320 (2011) Sec. III.C).  Truncated sparse-Pauli
propagation (|c| <= eps once per pair group, plus a string cap) drops small high-weight strings, so K(t) here is a
LOWER bound once the kept norm falls below 1; the kept norm is recorded and runs stop when it drops below --norm-stop.
Pairs with |d|/2pi < --dcut kHz are dropped (recorded).  Checkpoint after every record.
Usage: python run_kgrowth.py --pdb 1UBQ --probe 19 --ham dq --N 30 --eps 3e-4 --budget 150
Output: out/kgrowth_<pdb>_p<probe>_<ham>_N<N>.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

import dq_lib as D


def seq_for(ham, dm, dt, dcut):
    N = len(dm)
    seq = []
    for i in range(N):
        for j in range(i + 1, N):
            d = dm[i, j]
            if abs(d) < dcut:
                continue
            m = np.uint64((1 << i) | (1 << j)); z0 = np.uint64(0)
            if ham == "dq":
                seq.append([(m, z0, dt * d / 4), (m, m, -dt * d / 4)])
            else:
                a = d * dt / 2.0
                seq.append([(m, m, -a / 2), (m, z0, -a / 2), (z0, m, a)])
    return seq


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--ham", default="dq", choices=["dq", "sec"])
    ap.add_argument("--N", type=int, default=30)
    ap.add_argument("--eps", type=float, default=3e-4)
    ap.add_argument("--max-strings", type=int, default=150000)
    ap.add_argument("--dcut", type=float, default=0.3, help="kHz")
    ap.add_argument("--tmax", type=float, default=300.0)
    ap.add_argument("--budget", type=float, default=150.0)
    ap.add_argument("--norm-stop", type=float, default=0.6)
    a = ap.parse_args()
    names, xyz, resid = D.SP.read_h_coords(os.path.join(D.ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    idx = D.SP.cluster(xyz, a.probe, a.N)
    b0 = D.L.random_b0(1000)                       # orientation 0, as C1 / R1_amplify
    dm = D.SP.couplings(xyz[idx], b0)
    dcut = 2 * math.pi * a.dcut * 1e3
    seq = seq_for(a.ham, dm, D.DT, dcut)
    path = os.path.join(D.OUT, f"kgrowth_{a.pdb}_p{a.probe}_{a.ham}_N{a.N}.json")
    st = json.load(open(path)) if os.path.exists(path) else None
    if st and st.get("done"):
        print("already done"); return
    op = D.SP.PauliOp.single_z(a.N, 0)
    recs = []
    c0 = time.process_time()
    steps = int(round(a.tmax * 1e-6 / D.DT))
    for k in range(steps + 1):
        if k % 5 == 0:
            mw, n2, wh = D.mean_weight(op)
            dist = np.linalg.norm(xyz[idx] - xyz[idx[0]], axis=1)
            # support radius: norm-weighted fraction of strings touching each site -> sites with p > 0.5 / p > 0.1
            recs.append(dict(t_us=k * D.DT * 1e6, n_strings=int(len(op.c)), kept_norm2=n2, mean_weight=mw,
                             weight_hist=wh.tolist(), cpu=time.process_time() - c0))
            done = (n2 < a.norm_stop) or (time.process_time() - c0 > a.budget) or k == steps
            D.atomic_json(dict(pdb=a.pdb, probe=a.probe, ham=a.ham, N=a.N, eps=a.eps, max_strings=a.max_strings,
                               dcut_kHz=a.dcut, n_pairs=len(seq), n_pairs_total=a.N * (a.N - 1) // 2,
                               cluster=[names[i] for i in idx], records=recs, done=bool(done),
                               cpu_s=time.process_time() - c0), path)
            print(json.dumps(dict(t=round(k * D.DT * 1e6), str=len(op.c), n2=round(n2, 3), K=round(mw, 2),
                                  cpu=round(time.process_time() - c0))), flush=True)
            if done:
                break
        for grp in reversed(seq):
            for (gx, gz, th) in grp:
                op = D.SP.conj_rotation(op, gx, gz, th, None, 0.0, compact=False)
            op = op.compact(a.eps)
            if len(op.c) > a.max_strings:
                o = np.argpartition(-np.abs(op.c), a.max_strings)[:a.max_strings]
                op.x, op.z, op.c = op.x[o], op.z[o], op.c[o]


if __name__ == "__main__":
    main()
