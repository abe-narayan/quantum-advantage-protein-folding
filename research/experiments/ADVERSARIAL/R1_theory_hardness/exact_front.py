"""R1 theory_hardness, step B: exact operator front of Z_a(t) in protein 1H clusters (all sites, deterministic).

For the SAME Trotter circuit, cluster construction and field direction as scripts/nmr_gate.py / nmr_sparse_scaling.py
(dt = 2 us, first-order fused pair gates, b0 = random_b0(1000 + orient)), compute for EVERY spin j of the cluster:

  F^Z_aj(t) = 2^-N Tr[O Z_j O Z_j]      (the echo / first-order OTOC of the instrument)
  F^X_aj(t) = 2^-N Tr[O X_j O X_j]      (= F^Y by U(1) symmetry of O = Z_a(t))
  S_aj(t)   = 2^-N Tr[O Z_j]            (transfer)
  W_j(t)    = (1 - F^Z_aj)/2            (weight of O with X/Y at j)
  p_j(t)    = (3 - 2 F^X_aj - F^Z_aj)/4 (probability that the Pauli string of O is non-identity at j: support)
  size(t)   = sum_j p_j(t)              (operator size = c^2-weighted mean Pauli weight; exact, no truncation)

Derivation (DERIVED): sum_{s in I,X,Y,Z} s_j P s_j = 4 P if P_j = I else 0, so sum_s F^s_j = 4 Pr(P_j = I).

Method: sector-exact. U restricted to each magnetisation sector is diagonalised once (qapf.nmr.spins helpers), then
O_k(t) = Q conj(L)^n A L^n Q^dag per sector; F^Z via |O_k|^2, F^X via the sector-(k, k+1) index map.
Validated in-script against the RAW F curves of research/results/RAW/nmr_embed (N=10 and N=12, same b's).

Usage:  python exact_front.py --pdb 1UBQ --probe 19 --N 12 [--hn-only 1 --dt 5e-6 --steps 200]
Output: research/experiments/ADVERSARIAL/R1_theory_hardness/front/<tag>.json
Single-threaded (set OMP/MKL/OPENBLAS_NUM_THREADS=1). N=12 ~ 2-4 min, < 300 MB.
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


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def build_cluster(pdb, probe, N, orient, hn_only):
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    if hn_only:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        assert probe in keep
        names = [names[i] for i in keep]; xyz = xyz[keep]
        probe = keep.index(probe)
    idx = SP.cluster(xyz, probe, N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + orient)
    return names, idx, X0, b0


def exact_front(dm, dt, steps_list, a=0):
    N = len(dm)
    D = 1 << N
    blocks = []
    zs = np.stack([SP.zsign(N, j) for j in range(N)], 1)       # (D, N) signs
    posg = np.full(D, -1, np.int64)
    for idx, Uk in SP.sector_step_unitaries(dm, dt):
        Q, lam = SP._unitary_eig(Uk)
        del Uk
        za = SP.zsign(N, a)[idx]
        A = (Q.conj().T * za) @ Q
        posg[idx] = np.arange(len(idx))
        blocks.append((idx, Q, lam, A))
    # sector-(k,k+1) maps for F^X: for sector k and site j, local rows with bit j = 0 and their partners in k+1
    xmap = []
    for k in range(N):
        idx = blocks[k][0]
        mk = []
        for j in range(N):
            r0 = np.nonzero(((idx >> j) & 1) == 0)[0]
            p = posg[idx[r0] ^ (1 << j)]
            mk.append((r0, p))
        xmap.append(mk)
    res = dict(steps=[], FZ=[], FX=[], S=[])
    for n in steps_list:
        Os = []
        FZ = np.zeros(N); S = np.zeros(N)
        for (idx, Q, lam, A) in blocks:
            ln = lam ** n
            O = (Q * ln.conj()) @ A @ (Q.conj().T * ln[:, None])   # Q conj(L)^n A L^n Q^dag
            Zk = zs[idx]
            M = (np.abs(O) ** 2) @ Zk
            FZ += (Zk * M).sum(0)
            S += (np.real(np.diag(O))[:, None] * Zk).sum(0)
            Os.append(O)
        FX = np.zeros(N)
        for k in range(N):
            Ok, Ok1 = Os[k], Os[k + 1]
            for j in range(N):
                r0, p = xmap[k][j]
                if len(r0) == 0:
                    continue
                FX[j] += 2.0 * float(np.real((Ok[np.ix_(r0, r0)] * Ok1[np.ix_(p, p)].conj()).sum()))
        del Os
        res["steps"].append(int(n)); res["FZ"].append((FZ / D).tolist()); res["FX"].append((FX / D).tolist())
        res["S"].append((S / D).tolist())
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--hn-only", type=int, default=0)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--fine-until", type=int, default=100, help="record every 5 steps up to this, then every 10")
    a = ap.parse_args()
    t0 = time.time()
    names, idx, X0, b0 = build_cluster(a.pdb, a.probe, a.N, a.orient, a.hn_only)
    dm = SP.couplings(X0, b0)
    fine = max(1, a.fine_until // 20)
    steps_list = sorted(set(list(range(0, a.fine_until + 1, fine)) + list(range(0, a.steps + 1, max(1, a.steps // 16)))))
    r = exact_front(dm, a.dt, steps_list, 0)
    FZ = np.array(r["FZ"]); FX = np.array(r["FX"])
    p = (3 - 2 * FX - FZ) / 4
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    out = dict(pdb=a.pdb, probe=a.probe, hn_only=a.hn_only, N=a.N, orient=a.orient, dt=a.dt, b0=b0.tolist(),
               cluster=[int(i) for i in idx], names=[names[i] for i in idx], dist_A=dist.tolist(),
               omega_loc_kHz=(np.sqrt((dm ** 2).sum(1)) / 2 / math.pi / 1e3).tolist(),
               times_us=[s * a.dt * 1e6 for s in r["steps"]], FZ=r["FZ"], FX=r["FX"], S=r["S"],
               support_p=p.tolist(), size=p.sum(1).tolist(), W=((1 - FZ) / 2).tolist(),
               checks=dict(p_a_t0=float(p[0, 0]), size_t0=float(p[0].sum()), FX_self_t0=float(FX[0, 0])),
               secs=time.time() - t0)
    os.makedirs(os.path.join(HERE, "front"), exist_ok=True)
    tag = f"{a.pdb}{'HN' if a.hn_only else ''}_p{a.probe}_N{a.N}_o{a.orient}"
    # validation against the instrument's own RAW exact echo (same cluster, same b0, same circuit)
    emb = os.path.join(ROOT, "research", "results", "RAW", "nmr_embed", f"{a.pdb}_p{a.probe}_core10_o{a.orient}.json")
    if not a.hn_only and os.path.exists(emb) and a.N in (10, 12):
        e = json.load(open(emb))["envs"]["iso" if a.N == 10 else "exact_N12"]
        te = np.round(np.array(e["times"]) * 1e6).astype(int)
        mine = {int(round(t)): i for i, t in enumerate(out["times_us"])}
        dev = 0.0
        for b, Fb in e["F"].items():
            for ti, t in enumerate(te):
                if int(t) in mine:
                    dev = max(dev, abs(Fb[ti] - FZ[mine[int(t)], int(b)]))
        out["checks"]["max_dev_vs_RAW_embed_F"] = dev
    json.dump(out, open(os.path.join(HERE, "front", tag + ".json"), "w"))
    print(json.dumps(dict(tag=tag, secs=round(out["secs"], 1), checks=out["checks"],
                          size=[round(s, 2) for s in out["size"]][::3])))


if __name__ == "__main__":
    main()
