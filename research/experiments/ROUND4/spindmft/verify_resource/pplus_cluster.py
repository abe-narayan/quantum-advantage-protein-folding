"""Independent exact-typicality echo F_ab(t) on an ARBITRARY cluster family (resource verifier, ROUND4 spindmft).

Same estimator as ROUND3/r1sim_exact_reach/verify_resource/pplus_echo.py (single site b, one random vector per
magnetisation sector restricted to Z_b = +1, global-flip folding; validated there to 7e-14 vs dense unitaries), same
fused-pair first-order Trotter circuit (spins.pair_list, dt = 2 us, fastecho.SectorKernel), but the cluster is built
from a family spec:
  --family probe : the reference probe-centred cluster (fastecho.load_instance; = typicality_cone reference family)
  --family pairb : {a, b} U protons nearest to a or b (min distance) -- identical construction to the lane's
                   exact_pairb.py / run_emb.py 'pairb' family (b is the probe-cluster rank, as in the lane).
It is independent of the lane's exact_pairb.py (different kernel: sector-restricted fastecho vs full-space
spins.exact_correlators; different random vectors; different estimator).
Checkpoint: JSON after every sector (atomic tmp + replace); re-run the same command to resume.
--exact_trace: all P+ basis states instead of random vectors (exact; small N only) for validation.
Run single-threaded: OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
R3 = os.path.join(ROOT, "research", "experiments", "ROUND3", "r1sim_exact_reach")
sys.path.insert(0, R3)
sys.path.insert(0, os.path.join(R3, "verify_resource"))
sys.path.insert(0, os.path.join(ROOT, "src"))
import fastecho as FE  # noqa: E402
import pplus_echo as PP  # noqa: E402  (trzb, assemble, mat_step: read-only reuse)
from qapf.nmr import spins as SP  # noqa: E402


def build_cluster(family, probe, b, N):
    names, xyz_all, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    order = SP.cluster(xyz_all, probe, len(xyz_all))            # world index -> global index
    X = xyz_all[order]
    if family == "probe":
        C = list(range(N))
    elif family == "pairb":
        dmin = np.minimum(np.linalg.norm(X - X[0], axis=1), np.linalg.norm(X - X[b], axis=1))
        rest = [int(i) for i in np.argsort(dmin, kind="stable") if i not in (0, b)]
        C = sorted([0, b] + rest[: N - 2])
    else:
        raise ValueError(family)
    assert C[0] == 0 and b in C
    b0 = FE.random_b0(1000)
    D = SP.couplings(X[C], b0)
    Dall = SP.couplings(X, b0)
    m2 = float((Dall[b, C] ** 2).sum() / (Dall[b] ** 2).sum())
    return D, C, C.index(b), [names[order[i]] for i in C], m2


def run(family, probe, b, N, steps, seed, out, budget, exact_trace=False):
    assert N % 2 == 0
    D, C, site, cnames, m2 = build_cluster(family, probe, b, N)
    pairs = SP.pair_list(D, 2e-6)
    pc = FE.popcounts(N)
    st = json.load(open(out)) if os.path.exists(out) else dict(
        done={}, family=family, N=N, probe=probe, b_world=b, site_local=site, C_world=C, C_names=cnames,
        M2_fraction_b_in_cluster=m2, steps=steps, seed=seed, exact_trace=exact_trace,
        dtype="complex128" if exact_trace else "complex64")
    assert st["C_world"] == C and st["steps"] == steps
    t_run = time.process_time()
    nmax = max(steps)
    dtype = np.complex128 if exact_trace else np.complex64
    for k in range(N // 2, -1, -1):
        if str(k) in st["done"]:
            continue
        if time.process_time() - t_run > budget:
            print(f"budget reached before sector {k}; checkpoint kept", flush=True)
            break
        t0 = time.process_time()
        idx = np.nonzero(pc == k)[0]
        plus = ((idx >> site) & 1) == 0
        dplus = int(plus.sum())
        za = FE._zs(N, 0, idx)
        zb = FE._zs(N, site, idx)
        T = {}
        if exact_trace:
            maps = FE.sector_pair_maps(N, idx, pairs)
            cf = FE.gate_coefs(pairs)
            ci = FE.gate_coefs(pairs, inverse=True)
            cols = np.nonzero(plus)[0]
            V = np.zeros((len(idx), len(cols)), np.complex128)
            V[cols, np.arange(len(cols))] = 1.0
            for n in range(1, nmax + 1):
                PP.mat_step(V, maps, cf)
                if n in steps:
                    Uv = za[:, None] * V
                    for _ in range(n):
                        PP.mat_step(Uv, maps, ci, inverse=True)
                    T[str(n)] = float(np.sum(zb[:, None] * (Uv.real ** 2 + Uv.imag ** 2)))
        else:
            rng = np.random.default_rng([seed, N, k, site, probe, 7 if family == "pairb" else 3])
            x = np.zeros(len(idx), np.complex128)
            x[plus] = rng.standard_normal(dplus) + 1j * rng.standard_normal(dplus)
            x /= np.linalg.norm(x)
            K = FE.SectorKernel(N, idx, pairs, dtype)
            za_ = za.astype(np.float32)
            zb_ = zb.astype(np.float32)
            phi = x.astype(dtype)
            del x
            for n in range(1, nmax + 1):
                K.step(phi)
                if n in steps:
                    u = za_ * phi
                    for _ in range(n):
                        K.step(u, inverse=True)
                    T[str(n)] = dplus * float(np.sum(zb_ * (u.real.astype(np.float64) ** 2
                                                             + u.imag.astype(np.float64) ** 2)))
                    del u
            del K, phi
        st["done"][str(k)] = dict(T=T, dplus=dplus, dim=int(len(idx)), trZb=PP.trzb(N, k),
                                  cpu_s=time.process_time() - t0)
        st["cpu_s_total"] = sum(v["cpu_s"] for v in st["done"].values())
        try:
            import psutil
            st["peak_rss_GB"] = max(st.get("peak_rss_GB", 0), psutil.Process().memory_info().peak_wset / 1e9)
        except Exception:
            pass
        if len(st["done"]) == N // 2 + 1:
            st["F"] = PP.assemble(N, st["done"], steps)
            st["times_us"] = {str(n): 2.0 * n for n in steps}
            st["typicality_err_est"] = None if exact_trace else 2.0 * 2.0 ** (-N / 2)
        json.dump(st, open(out + ".tmp", "w"), indent=1)
        os.replace(out + ".tmp", out)
        print(f"{family} p{probe} b{b} N={N} sector {k} dim {len(idx)} cpu {st['done'][str(k)]['cpu_s']:.1f}s", flush=True)
    if "F" in st:
        print("F", {k: round(v, 4) for k, v in st["F"].items()}, "cpu_total", round(st["cpu_s_total"], 1),
              "peak_rss_GB", round(st.get("peak_rss_GB", 0), 3), "M2_in", round(m2, 3), flush=True)
    return st


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--family", required=True, choices=["probe", "pairb"])
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--b", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--steps", type=int, nargs="+", default=[20, 40, 60])
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--budget", type=float, default=600.0, help="CPU seconds per invocation (resume to continue)")
    ap.add_argument("--exact_trace", action="store_true")
    a = ap.parse_args()
    tag = "exact" if a.exact_trace else f"seed{a.seed}"
    stp = "-".join(str(s) for s in a.steps)
    out = os.path.join(HERE, "runs", f"pp_{a.family}_p{a.probe}_b{a.b}_N{a.N}_s{stp}_{tag}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    run(a.family, a.probe, a.b, a.N, a.steps, a.seed, out, a.budget, exact_trace=a.exact_trace)
