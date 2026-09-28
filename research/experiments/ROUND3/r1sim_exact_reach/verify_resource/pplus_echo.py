"""Single-site exact-typicality echo F_ab(t) = Tr[Z_b W Z_b W]/2^N, W = U(t)^dag Z_a U(t), on the lane's reference
Trotter circuit (spins.pair_list, dt = 2 us, fused pair gates, fastecho.SectorKernel), with ONE vector per sector.

Identity (DERIVED here): with X = W Z_b W and P_+ = projector on bit_b = 0 (Z_b = +1),
    Tr_k[Z_b X] = 2 Tr_k[P_+ X] - Tr_k[X],   Tr_k[X] = Tr_k[Z_b] = C(N-1,k) - C(N-1,k-1)   (W unitary, sector-preserving)
and the global flip P (P X P = -X, P P_+^{(N-k)} P = P_-^{(k)}) gives Tr_{N-k}[P_+ X] = Tr_k[P_+ X] - Tr_k[Z_b], so
    F = { sum_{k<N/2} (4 T_k - 2 Tr_k[Z_b]) + T_{N/2} * 2 } / 2^N,    T_k = Tr_k[P_+ X].
T_k is estimated by typicality: T_k ~ d_k+ <psi|X|psi> = d_k+ <W psi|Z_b|W psi>, psi uniform in P_+ within sector k
(d_k+ = C(N-1, k)).  This is exactly the quantum-circuit protocol (U, Z_a, U^dag, measure Z_b), so it also serves
as a classical twin of the quantum estimator.  Cost per sector: n_max forward + sum(n) backward vector-steps.
--exact_trace replaces the random vector by all basis states of P_+ (exact trace; small N only) for validation.
Checkpoint: JSON after every sector (atomic tmp + replace); rerun the same command to resume.
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


def mat_step(V, maps, coefs, inverse=False):
    """same fused pair gates as SectorKernel.step, on a (dim, m) block (exact-trace validation only)."""
    seq = zip(reversed(maps), reversed(coefs)) if inverse else zip(maps, coefs)
    for (r, q), (al, be) in seq:
        if len(r) == 0:
            continue
        xr = V[r].copy()
        xq = V[q].copy()
        V[r] = al * xr + be * xq
        V[q] = al * xq + be * xr
    return V


def trzb(N, k):
    return math.comb(N - 1, k) - (math.comb(N - 1, k - 1) if k >= 1 else 0)


def assemble(N, done, steps):
    F = {}
    for n in steps:
        s = 0.0
        for k in range(N // 2 + 1):
            T = done[str(k)]["T"][str(n)]
            if 2 * k < N:
                s += 4 * T - 2 * trzb(N, k)
            else:
                s += 2 * T - trzb(N, k)
        F[str(n)] = s / 2.0 ** N
    return F


def run(N, probe, site, steps, seed, out, budget, exact_trace=False, dtype=np.complex64):
    assert N % 2 == 0
    dm, bs, names, _ = FE.load_instance("1UBQ", probe, N)
    assert site in bs, (site, bs)
    pairs = SP.pair_list(dm, 2e-6)
    pc = FE.popcounts(N)
    st = json.load(open(out)) if os.path.exists(out) else dict(done={}, N=N, probe=probe, site=site, steps=steps,
                                                               seed=seed, exact_trace=exact_trace,
                                                               dtype=np.dtype(dtype).name, bs=bs, names_bs=names)
    t_run = time.process_time()
    nmax = max(steps)
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
                mat_step(V, maps, cf)
                if n in steps:
                    Uv = za[:, None] * V
                    for _ in range(n):
                        mat_step(Uv, maps, ci, inverse=True)
                    T[str(n)] = float(np.sum(zb[:, None] * (Uv.real ** 2 + Uv.imag ** 2)))
        else:
            rng = np.random.default_rng([seed, N, k, site, probe])
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
                    T[str(n)] = dplus * float(np.sum(zb_ * (u.real.astype(np.float64) ** 2 + u.imag.astype(np.float64) ** 2)))
                    del u
            del K, phi
        st["done"][str(k)] = dict(T=T, dplus=dplus, dim=int(len(idx)), trZb=trzb(N, k), cpu_s=time.process_time() - t0)
        st["cpu_s_total"] = sum(v["cpu_s"] for v in st["done"].values())
        try:
            import psutil
            st["peak_rss_GB"] = max(st.get("peak_rss_GB", 0), psutil.Process().memory_info().peak_wset / 1e9)
        except Exception:
            pass
        if len(st["done"]) == N // 2 + 1:
            st["F"] = assemble(N, st["done"], steps)
            st["times_us"] = {str(n): 2.0 * n for n in steps}
            st["typicality_err_est"] = None if exact_trace else 2.0 * 2.0 ** (-N / 2)
        json.dump(st, open(out + ".tmp", "w"), indent=1)
        os.replace(out + ".tmp", out)
        print(f"N={N} sector {k} dim {len(idx)} d+ {dplus} cpu {st['done'][str(k)]['cpu_s']:.1f}s  T {T}", flush=True)
    if "F" in st:
        print("F", st["F"], "cpu_total", st["cpu_s_total"], flush=True)
    return st


def exact_dense(N, probe, site, steps):
    """reference exact F from dense per-sector Trotter-step unitaries (the lane's validate_flip method)."""
    dm, bs, _, _ = FE.load_instance("1UBQ", probe, N)
    tot = {n: 0.0 for n in steps}
    for idx, Uk in SP.sector_step_unitaries(dm, 2e-6):
        za = FE._zs(N, 0, idx)
        zb = FE._zs(N, site, idx)
        for n in steps:
            Un = np.linalg.matrix_power(Uk, n)
            W = Un.conj().T @ (za[:, None] * Un)
            A = W * zb[None, :]
            tot[n] += float(np.real(np.trace(A @ A)))
    return {str(n): tot[n] / 2.0 ** N for n in steps}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--site", type=int, default=8)
    ap.add_argument("--steps", type=int, nargs="+", default=[80, 160])
    ap.add_argument("--seed", type=int, default=2026)
    ap.add_argument("--budget", type=float, default=780.0, help="CPU seconds per invocation (resume to continue)")
    ap.add_argument("--exact_trace", action="store_true")
    ap.add_argument("--validate_dense", action="store_true")
    a = ap.parse_args()
    tag = "exact" if a.exact_trace else f"seed{a.seed}"
    out = os.path.join(HERE, "runs", f"pplus_1UBQ_p{a.probe}_N{a.N}_site{a.site}_{tag}.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    st = run(a.N, a.probe, a.site, a.steps, a.seed, out, a.budget, exact_trace=a.exact_trace,
             dtype=np.complex128 if a.exact_trace else np.complex64)
    if a.validate_dense and "F" in st:
        ref = exact_dense(a.N, a.probe, a.site, a.steps)
        st["dense_reference_F"] = ref
        st["max_abs_dev_vs_dense"] = max(abs(st["F"][k] - ref[k]) for k in ref)
        json.dump(st, open(out + ".tmp", "w"), indent=1)
        os.replace(out + ".tmp", out)
        print("dense ref", ref, "max dev", st["max_abs_dev_vs_dense"])
