"""Classical-adversary verification of the r1sim_exact_reach claim.

Exact identity (DERIVED here; checked numerically below):
    W = Z_a(t) = sum_j G_j Z_j + W_rest,   G_j = Tr[W Z_j]/2^N   (the two-point transfer a->j, incl. j = a)
    [Z_j, Z_b] = 0  and  Tr[Z_j W_rest] = 0   =>   cross terms vanish exactly, so
    F_ab(t) = H(t) + R_ab(t),   H(t) = sum_j G_j(t)^2   (b-independent, TWO-POINT only),
                               R_ab(t) = Tr[W_rest Z_b W_rest Z_b]/2^N.
Sector-structure piece of R (conserved-charge fluctuation inside the finite cluster):
    floor(t) = Tr[W_rest (Z_tot/N) W_rest (Z_tot/N)]/2^N = sum_k m_k^2 tau_k(W_rest^2),   m_k = (N-2k)/N,
    tau_k(W_rest^2) = tau_k(I) - 2 sum_j G_j tau_k(Z_j W) + sum_ij G_i G_j tau_k(Z_i Z_j)   (exact combinatorics).
X_ab(t) = F_ab - H - floor  is what is left.

Same reference circuit (spins.pair_list, first-order Trotter, dt = 2 us, b0 = random_b0(1000)) and the lane's validated
SectorKernel (fastecho.py).  Flip-folded sector typicality (k <= N/2, multiplicity 2 for k < N/2).

Cluster families:
  probe : N protons nearest to the probe (the reference / lane family; b indices = instrument_bs)
  pairb : for ONE instrument site b, N protons nearest to {a, b} (metric min(d_ia, d_ib)); a -> 0, b -> 1
Modes:
  echo  : F_ab for the requested bs + G_j for all j (G from W psi, computed anyway)
  honly : G_j for all j only, via two inverse passes  G_j(n) = <S^-n Z_a x| Z_j |S^-n x>   (2 * n_max vector-steps)
Checkpoint: per sector, atomic JSON (tmp + os.replace); a rerun resumes.
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
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import fastecho as FE  # noqa: E402
from fastecho import SP  # noqa: E402

DT = 2e-6


def load_cluster(pdb, probe, N, family="probe", b_std=None):
    names, xyz, _ = SP.read_h_coords(os.path.join(FE.ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    bs_std = FE.instrument_bs(xyz, probe)
    std10 = SP.cluster(xyz, probe, 10)
    if family == "probe":
        idx = SP.cluster(xyz, probe, N)
        bs = bs_std
    elif family.startswith("custom"):
        # custom:<n0>:<r1>,<r2>,...  -> first n0 probe-cluster ranks plus the listed ranks (b indices unchanged)
        _, n0, extra = family.split(":")
        full = SP.cluster(xyz, probe, 200)
        ranks = list(range(int(n0))) + [int(r) for r in extra.split(",") if r]
        idx = np.array([int(full[r]) for r in ranks])
        assert len(idx) == N, (len(idx), N)
        bs = bs_std
    elif family == "pairb":
        gb = int(std10[b_std])
        da = np.linalg.norm(xyz - xyz[probe], axis=1)
        db = np.linalg.norm(xyz - xyz[gb], axis=1)
        order = [int(i) for i in np.argsort(np.minimum(da, db), kind="stable") if i not in (probe, gb)]
        idx = np.array([probe, gb] + order[:N - 2])
        bs = [1]
    else:
        raise ValueError(family)
    dm = SP.couplings(xyz[idx], FE.random_b0(1000))
    return dm, bs, [names[i] for i in idx], xyz[idx], idx


def zz_offdiag_mean(N, k):
    M = N - 2 * k
    return (M * M - N) / (N * (N - 1.0))


def run(pdb, probe, N, family, b_std, mode, otimes, R, dtype, seed, ckpt, log=print, time_budget_s=None, basis=False):
    """basis=True: every sector uses its full orthonormal basis instead of R random vectors -> EXACT traces
    (validation only; cost x D_k)."""
    dm, bs, names, xyz, gidx = load_cluster(pdb, probe, N, family, b_std)
    pairs = SP.pair_list(dm, DT)
    otimes = sorted(otimes)
    nmax = max(otimes)
    pc = FE.popcounts(N)
    st = dict(done={}, secs=0.0)
    if ckpt and os.path.exists(ckpt):
        st = json.load(open(ckpt))
    rng = np.random.default_rng(seed + 7919 * N + 104729 * (0 if family == "probe" else (1 + b_std if family == "pairb" else 999)))
    t_run = time.time()
    partial = False
    for k in range(N // 2 + 1):
        Dk = math.comb(N, k)
        xs = []
        for r in range(R):                      # draw in order -> resume-reproducible
            x = rng.standard_normal(Dk) + 1j * rng.standard_normal(Dk)
            xs.append(x / np.linalg.norm(x))
        if basis:
            xs = [np.eye(Dk, dtype=complex)[:, i] for i in range(Dk)]
        if str(k) in st["done"]:
            continue
        if time_budget_s is not None and time.time() - t_run > time_budget_s:
            partial = True
            break
        ts = time.time()
        idx = np.nonzero(pc == k)[0]
        mult = 1.0 if 2 * k == N else 2.0
        w = mult * Dk / float(1 << N)
        K = FE.SectorKernel(N, idx, pairs, dtype)
        zmat = np.stack([FE._zs(N, q, idx) for q in range(N)]).astype(np.float64)   # (N, Dk)
        za = zmat[0]
        Rk = len(xs)
        g = np.zeros((Rk, len(otimes), N))      # per-sector G_j contributions (weighted by w)
        Fk = np.zeros((Rk, len(otimes), len(bs)))
        nvs = 0
        for r in range(Rk):
            x = xs[r].astype(dtype)
            if mode == "honly":
                phi = x.copy()
                chi = (za * x).astype(dtype)
                ti = 0
                for n in range(1, nmax + 1):
                    K.step(phi, inverse=True); K.step(chi, inverse=True); nvs += 2
                    if n in otimes:
                        y = np.real(np.conj(chi) * phi).astype(np.float64)
                        g[r, ti] = w * (zmat @ y)
                        ti += 1
            else:
                phi = x.copy()
                chi = {b: (zmat[b] * x).astype(dtype) for b in bs}
                ti = 0
                for n in range(1, nmax + 1):
                    K.step(phi); nvs += 1
                    for b in bs:
                        K.step(chi[b]); nvs += 1
                    if n in otimes:
                        ub = (za * phi).astype(dtype)
                        for _ in range(n):
                            K.step(ub, inverse=True); nvs += 1
                        y = np.real(np.conj(x) * ub).astype(np.float64)
                        g[r, ti] = w * (zmat @ y)
                        for bi, b in enumerate(bs):
                            vb = (za * chi[b]).astype(dtype)
                            for _ in range(n):
                                K.step(vb, inverse=True); nvs += 1
                            Fk[r, ti, bi] = w * float(np.real(np.vdot(zmat[b] * ub, vb)))
                            del vb
                        del ub
                        ti += 1
        if basis:
            g = g.mean(0, keepdims=True); Fk = Fk.mean(0, keepdims=True)
        st["done"][str(k)] = dict(g=g.tolist(), F=Fk.tolist(), Dk=Dk, w=w, mult=mult, secs=time.time() - ts,
                                  vector_steps=nvs)
        st["secs"] = st.get("secs", 0.0) + time.time() - ts
        if ckpt:
            json.dump(st, open(ckpt + ".tmp", "w"))
            os.replace(ckpt + ".tmp", ckpt)
        if log:
            log(json.dumps(dict(sector=k, Dk=Dk, secs=round(time.time() - ts, 2), cum=round(st["secs"], 1))))
        del K, zmat
    complete = all(str(k) in st["done"] for k in range(N // 2 + 1))
    out = dict(pdb=pdb, probe=probe, N=N, family=family, b_std=b_std, mode=mode, R=R, dtype=np.dtype(dtype).name,
               seed=seed, times_us=[n * DT * 1e6 for n in otimes], otimes=otimes, bs=bs, names=names,
               global_idx=[int(i) for i in gidx], complete=complete, cpu_secs=st.get("secs", 0.0),
               vector_steps=int(sum(v["vector_steps"] for v in st["done"].values())))
    if not complete:
        out["partial"] = True
        return out
    ks = list(range(N // 2 + 1))
    g = np.array([st["done"][str(k)]["g"] for k in ks])          # (K, R, T, N)
    G_r = g.sum(0)                                               # (R, T, N)
    G = G_r.mean(0)                                              # (T, N)
    if R >= 2 and not basis:
        pairs_r = [(i, j) for i in range(R) for j in range(i + 1, R)]
        H = np.mean([np.sum(G_r[i] * G_r[j], axis=1) for i, j in pairs_r], axis=0)   # unbiased
    else:
        H = np.sum(G ** 2, axis=1)
    # floor = sum_k mult m_k^2 tau_k(W_rest^2)
    floor = np.zeros(len(otimes))
    for kk, k in enumerate(ks):
        d = st["done"][str(k)]
        tauI = d["Dk"] / float(1 << N)                          # one sector's tau (not multiplied)
        gk = g[kk].mean(0) / d["mult"]                           # per-sector (single k) tau_k(Z_j W), (T, N)
        e = zz_offdiag_mean(N, k)
        sumG = G.sum(1)
        zz = tauI * (e * (sumG ** 2 - np.sum(G ** 2, 1)) + np.sum(G ** 2, 1))
        tw = tauI - 2 * np.sum(G * gk, 1) + zz
        m = (N - 2 * k) / N
        floor += d["mult"] * m * m * tw
    out.update(G=G.tolist(), H=H.tolist(), sumG=G.sum(1).tolist(), floor=floor.tolist(),
               floor_free=float(1.0 / N))
    if mode == "echo":
        Fk = np.array([st["done"][str(k)]["F"] for k in ks]).sum(0)   # (R, T, B)
        F = Fk.mean(0)
        out.update(F={str(b): F[:, bi].tolist() for bi, b in enumerate(bs)},
                   F_r=Fk.tolist(),
                   R_=({str(b): (F[:, bi] - H).tolist() for bi, b in enumerate(bs)}),
                   X={str(b): (F[:, bi] - H - floor).tolist() for bi, b in enumerate(bs)})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--family", default="probe")
    ap.add_argument("--b", type=int, default=None, help="instrument site (standard index) for family pairb")
    ap.add_argument("--mode", default="honly", choices=["honly", "echo"])
    ap.add_argument("--times", type=int, nargs="*", default=None, help="Trotter steps (dt = 2 us)")
    ap.add_argument("--R", type=int, default=1)
    ap.add_argument("--dtype", default="complex128")
    ap.add_argument("--seed", type=int, default=2718)
    ap.add_argument("--budget-s", type=float, default=None)
    a = ap.parse_args()
    times = a.times or list(range(20, 161, 20))
    fam = a.family.replace(":", "-").replace(",", "_") + (f"b{a.b}" if a.family == "pairb" else "")
    tag = f"{a.pdb}_p{a.probe}_N{a.N}_{fam}_{a.mode}_R{a.R}_{a.dtype}_t{'-'.join(map(str, times))}"
    out = os.path.join(HERE, "runs", tag + ".json")
    if os.path.exists(out):
        print("exists", out)
        return
    t0 = time.time()
    res = run(a.pdb, a.probe, a.N, a.family, a.b, a.mode, times, a.R, np.dtype(a.dtype), a.seed, out + ".ckpt.json",
              time_budget_s=a.budget_s)
    try:
        import psutil
        res["peak_rss_GB"] = psutil.Process().memory_info().peak_wset / 1e9
    except Exception:
        pass
    res["wall_s"] = time.time() - t0
    if res["complete"]:
        json.dump(res, open(out + ".tmp", "w"), indent=1)
        os.replace(out + ".tmp", out)
        if os.path.exists(out + ".ckpt.json"):
            os.remove(out + ".ckpt.json")          # finished result supersedes its own checkpoint
        print(json.dumps(dict(done=os.path.basename(out), cpu_s=round(res["cpu_secs"], 1),
                              rss=round(res.get("peak_rss_GB", 0), 3))))
    else:
        print(json.dumps(dict(partial=True, ckpt=out + ".ckpt.json")))


if __name__ == "__main__":
    main()
