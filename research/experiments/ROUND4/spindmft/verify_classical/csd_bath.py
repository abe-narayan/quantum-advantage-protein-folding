"""Classical verifier (ROUND4 spindmft lane): classical-spin-dynamics (CSD) bath autocorrelations.

Replaces the lane's sr-spinDMFT bath autocorrelations g_j^z, g_j^perp (which fail on this network: p19 G_aa(80 us)
0.21 vs 0.36 exact) by those of classical spin dynamics on the SAME Hamiltonian
    H = sum_{i<j} d_ij (2 S_i^z S_j^z - S_i^x S_j^x - S_i^y S_j^y),  |S| = sqrt(3)/2,  dS_i/dt = h_i x S_i,
    h_i = sum_j d_ij (-S_j^x, -S_j^y, 2 S_j^z)
(the round-3 CSD model, validated there against exact H to <= 0.012).  Infinite temperature: S_i uniform on the sphere.
g_j^z(tau) = 4 <S_j^z(t0+tau) S_j^z(t0)>,  g_j^perp(tau) = 2 <S_j^x S_j^x + S_j^y S_j^y> (so g(0) = 1), averaged over
samples and over start times t0 in {0, 10, ..., 60} us (stationarity).  RK4, 2 substeps per 1-us grid point.
World: 'protein' (all 629 1UBQ protons, global order) or a closed N-spin probe cluster (probe-rank order).
Checkpoint every sample batch (atomic npz tmp + replace); resumable.  Single-threaded.
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import sdmft as S  # noqa: E402  (read-only import of the lane's instance helpers)
from qapf.nmr import spins as SP  # noqa: E402

T_LAG = 120
T0S = list(range(0, 61, 10))


def rhs(Sv, D):
    # Sv: (3, N, M)
    hx = -(D @ Sv[0]); hy = -(D @ Sv[1]); hz = 2.0 * (D @ Sv[2])
    return np.stack([hy * Sv[2] - hz * Sv[1], hz * Sv[0] - hx * Sv[2], hx * Sv[1] - hy * Sv[0]])


def run_batch(D, M, rng, sub=2):
    N = len(D)
    v = rng.standard_normal((3, N, M))
    Sv = v / np.linalg.norm(v, axis=0, keepdims=True) * (np.sqrt(3.0) / 2.0)
    h = 1e-6 / sub
    nT = T0S[-1] + T_LAG
    acc_z = np.zeros((N, T_LAG + 1)); acc_p = np.zeros((N, T_LAG + 1)); cnt = np.zeros(T_LAG + 1)
    starts = {}
    for t in range(nT + 1):
        if t in T0S:
            starts[t] = Sv.copy()
        for t0, S0 in starts.items():
            lag = t - t0
            if 0 <= lag <= T_LAG:
                acc_z[:, lag] += 4.0 * (Sv[2] * S0[2]).sum(-1)
                acc_p[:, lag] += 2.0 * (Sv[0] * S0[0] + Sv[1] * S0[1]).sum(-1)
                cnt[lag] += M
        if t == nT:
            break
        for _ in range(sub):
            k1 = rhs(Sv, D); k2 = rhs(Sv + 0.5 * h * k1, D); k3 = rhs(Sv + 0.5 * h * k2, D); k4 = rhs(Sv + h * k3, D)
            Sv = Sv + (h / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
    norm_drift = float(np.abs(np.linalg.norm(Sv, axis=0) - np.sqrt(3.0) / 2.0).max())
    return acc_z, acc_p, cnt, norm_drift


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--world", default="protein")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--M", type=int, default=512)
    ap.add_argument("--batch", type=int, default=64)
    ap.add_argument("--seed", type=int, default=424242)
    a = ap.parse_args()
    names, xyz, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    if a.world == "protein":
        D = SP.couplings(xyz, S.random_b0(1000)); tag = f"csd_protein_M{a.M}"
    else:
        w = S.load_world("1UBQ", a.probe, int(a.world)); D = w["D"]; tag = f"csd_p{a.probe}_N{a.world}_M{a.M}"
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    ck = os.path.join(HERE, "out", tag + ".ckpt.npz")
    N = len(D)
    st = dict(done=0, az=np.zeros((N, T_LAG + 1)), ap=np.zeros((N, T_LAG + 1)), cnt=np.zeros(T_LAG + 1), cpu=0.0,
              drift=0.0)
    if os.path.exists(ck):
        z = np.load(ck)
        st = dict(done=int(z["done"]), az=z["az"], ap=z["ap"], cnt=z["cnt"], cpu=float(z["cpu"]), drift=float(z["drift"]))
    nb = a.M // a.batch
    for ib in range(st["done"], nb):
        c0 = time.process_time()
        az, ap_, cnt, dr = run_batch(D, a.batch, np.random.default_rng([a.seed, ib]))
        st["az"] += az; st["ap"] += ap_; st["cnt"] += cnt; st["done"] = ib + 1
        st["cpu"] += time.process_time() - c0; st["drift"] = max(st["drift"], dr)
        np.savez(ck + ".tmp.npz", **st)
        os.replace(ck + ".tmp.npz", ck)
        print(json.dumps(dict(batch=ib, cpu=round(st["cpu"], 1), drift=dr)), flush=True)
    gz = st["az"] / st["cnt"]; gp = st["ap"] / st["cnt"]
    np.savez(os.path.join(HERE, "out", tag + ".npz"), gz=gz, gp=gp)
    out = dict(tag=tag, world=a.world, probe=a.probe, M=a.M, t0s=T0S, cpu_s=st["cpu"], norm_drift=st["drift"],
               note="gz/gp for all sites in <tag>.npz; order = global PDB-H order (protein) or probe rank (closed world)")
    if a.world == "protein":
        for p in (19, 245):
            out[f"g_p{p}"] = dict(gz=[round(gz[p, t], 4) for t in (0, 40, 80, 120)],
                                  gp=[round(gp[p, t], 4) for t in (0, 40, 80, 120)])
    else:
        out["g_probe"] = dict(gz=[round(gz[0, t], 4) for t in (0, 40, 80, 120)],
                              gp=[round(gp[0, t], 4) for t in (0, 40, 80, 120)])
    tmp = os.path.join(HERE, "out", tag + ".json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "out", tag + ".json"))
    print(json.dumps(out))


if __name__ == "__main__":
    main()
