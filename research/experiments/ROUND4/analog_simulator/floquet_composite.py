"""Floquet construction of the protein secular dipolar Hamiltonian on a Rydberg (electric-dipole, XY-native) platform,
and its echo error budget.  Full-space exact simulation (N <= 10).

Why a composite is needed (DERIVED, see README): the native resonant-exchange Hamiltonian of one encoding is
H1 = sum g_ij (XX + YY), a pair tensor with trace 2 g_ij.  Global rotations preserve the trace, so every Floquet
average of H1 has the Heisenberg component (2/3) sum g_ij S_ij; the protein target H_dd = sum (d/4)(2ZZ - XX - YY)
is traceless.  A second encoding with a Delta m = +-1 transition has the SAME spatial pattern with opposite sign,
H2 = -k H1 (Geier et al. 2402.13873: C3 = 3.2 vs -2.8 GHz um^3, k = 1.1 theory, 1.03 measured).  Time-sharing
    forward cycle (symmetric):  z(E1, k w) | swap | x(E2, w/2) | y(E2, w) | x(E2, w/2) | swap | z(E1, k w),  w = 1/(2(1+k))
gives H_eff = k c w sum d (A_x + A_y - 2 A_z) = H_dd for c = (1+k)/(2k), where A_z = XX+YY, A_x = YY+ZZ, A_y = XX+ZZ.
    reverse cycle:  z(E2, v/2) | swap | x(E1, u/2) | y(E1, u) | x(E1, u/2) | swap | z(E2, v/2),  u = k/(2(1+k)), v = 1/(1+k)
gives -H_dd.  Two encoding swaps and four frame pulses per cycle.

Errors simulated: finite cycle time (Magnus terms), random global pulse errors (every frame change and every swap is
followed by a random global rotation with independent N(0, dtheta) components, the Scholl et al. 2107.14459 model with
measured dtheta = 0.06 rad), and C3-ratio miscalibration (true k differs from the k used for the timing).
Pulses are instantaneous (optimistic: finite-duration pulses were a leading error in Scholl et al.).
Output: floquet.json (checkpointed per configuration; resumable).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

import ed_echo as EE

HERE = os.path.dirname(os.path.abspath(__file__))
PX = np.array([[0, 1], [1, 0]], complex)
PY = np.array([[0, -1j], [1j, 0]], complex)
PZ = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)


def op1(N, q, P):
    """P on qubit q (bit q of the index; kron order: qubit N-1 leftmost)."""
    out = np.array([[1.0 + 0j]])
    for p in range(N - 1, -1, -1):
        out = np.kron(out, P if p == q else I2)
    return out


def zdiag(N, q):
    x = np.arange(1 << N)
    return (1.0 - 2.0 * ((x >> q) & 1)).astype(float)


def global_rot(N, axis_vec, theta):
    """exp(-i theta/2 n.sigma) on every qubit."""
    n = np.asarray(axis_vec, float)
    nn = np.linalg.norm(n)
    if nn == 0 or theta == 0:
        return np.eye(1 << N, dtype=complex)
    n = n / nn
    s = n[0] * PX + n[1] * PY + n[2] * PZ
    u = math.cos(theta / 2) * I2 - 1j * math.sin(theta / 2) * s
    out = np.array([[1.0 + 0j]])
    for _ in range(N):
        out = np.kron(out, u)
    return out


def err_rot(N, rng, dth):
    if dth == 0:
        return None
    v = rng.normal(0.0, dth, 3)
    return global_rot(N, v, float(np.linalg.norm(v)))


def build(N, dm):
    X = [op1(N, q, PX) for q in range(N)]
    Y = [op1(N, q, PY) for q in range(N)]
    Az = np.zeros((1 << N, 1 << N), complex)
    Hdd = np.zeros_like(Az)
    for i in range(N):
        for j in range(i + 1, N):
            xy = X[i] @ X[j] + Y[i] @ Y[j]
            Az += dm[i, j] * xy
            zz = np.diag(zdiag(N, i) * zdiag(N, j))
            Hdd += dm[i, j] / 4.0 * (2 * zz - xy)
    return Az, Hdd


def frames(N):
    """Global pulses P_f with P_f^dag A_z P_f = A_f (checked numerically in main)."""
    return dict(z=np.eye(1 << N, dtype=complex), x=global_rot(N, [0, 1, 0], math.pi / 2),
                y=global_rot(N, [1, 0, 0], math.pi / 2))


def expm_h(E, Q, tau):
    return (Q * np.exp(-1j * E * tau)[None, :]) @ Q.conj().T


def cycle_segments(k, reverse):
    """list of (encoding, frame, weight) for one symmetric cycle; weights sum to 1."""
    if not reverse:
        w = 1.0 / (2 * (1 + k))
        return [("E1", "z", k * w), ("E2", "x", w / 2), ("E2", "y", w), ("E2", "x", w / 2), ("E1", "z", k * w)]
    u = k / (2 * (1 + k)); v = 1.0 / (1 + k)
    return [("E2", "z", v / 2), ("E1", "x", u / 2), ("E1", "y", u), ("E1", "x", u / 2), ("E2", "z", v / 2)]


def leg_unitary(N, eig, Pf, k_design, reverse, tc, ncyc, rng, dth, t_marks):
    """Product of ncyc cycles; returns dict {cycle_count: U} at the requested marks (prefix sharing)."""
    segs = cycle_segments(k_design, reverse)
    D = 1 << N
    useg = []
    for (enc, fr, wgt) in segs:
        E, Q = eig[enc]
        P = Pf[fr]
        useg.append(P.conj().T @ expm_h(E, Q, wgt * tc) @ P)
    U = np.eye(D, dtype=complex)
    out = {}
    prev = None
    for c in range(1, ncyc + 1):
        for si, (enc, fr, wgt) in enumerate(segs):
            if prev is not None and (prev != (enc, fr)):
                # frame change (and swap if the encoding changes): ideal pulses are folded into the toggling frame;
                # each error is a random global rotation (isotropic, so its toggling-frame image has the same law)
                n_err = 1 + (1 if prev[0] != enc else 0)
                for _ in range(n_err):
                    R = err_rot(N, rng, dth)
                    if R is not None:
                        U = R @ U
            U = useg[si] @ U
            prev = (enc, fr)
        if c in t_marks:
            out[c] = U.copy()
    return out


def signal(N, U, V, a, b):
    za = zdiag(N, a); zb = zdiag(N, b)
    M = U @ (zb[:, None] * U.conj().T)                    # U Z_b U^dag
    A = V @ ((za[:, None] * M) * za[None, :]) @ V.conj().T
    S = float(np.real(np.sum(zb * np.diag(A)))) / (1 << N)
    Bm = V @ M @ V.conj().T
    R = float(np.real(np.sum(zb * np.diag(Bm)))) / (1 << N)
    return S, R


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--N", type=int, default=8)
    ap.add_argument("--times", type=float, nargs="*", default=[40, 80, 120])
    ap.add_argument("--xs", type=float, nargs="*", default=[0.2, 0.1, 0.05], help="J_m t_c / 2pi values")
    ap.add_argument("--dths", type=float, nargs="*", default=[0.0])
    ap.add_argument("--kerrs", type=float, nargs="*", default=[0.0])
    ap.add_argument("--shots", type=int, default=8)
    ap.add_argument("--k", type=float, default=1.1)
    ap.add_argument("--tag", default="")
    ap.add_argument("--budget-cpu-s", type=float, default=900)
    a = ap.parse_args()
    c0 = time.process_time()
    path = os.path.join(HERE, f"floquet_{a.pdb}_p{a.probe}_N{a.N}{a.tag}.json")
    st = json.load(open(path)) if os.path.exists(path) else dict(units={})
    dm, bs, xyz, b0 = EE.load(a.pdb, a.probe, a.N)
    N = a.N
    bs = [b for b in bs if b < N] or [1]
    Az, Hdd = build(N, dm)
    Pf = frames(N)
    # frame check: P_f^dag A_z P_f must equal A_f
    Xs = [op1(N, q, PX) for q in range(N)]; Ys = [op1(N, q, PY) for q in range(N)]
    Zs = [np.diag(zdiag(N, q)).astype(complex) for q in range(N)]
    chk = {}
    for fr, (P1, P2) in dict(x=(Ys, Zs), y=(Xs, Zs)).items():
        Af = sum(dm[i, j] * (P1[i] @ P1[j] + P2[i] @ P2[j]) for i in range(N) for j in range(i + 1, N))
        chk[fr] = float(np.abs(Pf[fr].conj().T @ Az @ Pf[fr] - Af).max())
    # effective-Hamiltonian check (zeroth order): sum_w P^dag H P must equal H_dd
    c = (1 + a.k) / (2 * a.k)
    H1 = -c * Az; H2 = a.k * c * Az
    Heff = sum(wgt * Pf[fr].conj().T @ (H1 if enc == "E1" else H2) @ Pf[fr] for enc, fr, wgt in cycle_segments(a.k, False))
    Hrev = sum(wgt * Pf[fr].conj().T @ (H1 if enc == "E1" else H2) @ Pf[fr] for enc, fr, wgt in cycle_segments(a.k, True))
    st["checks"] = dict(frame_maxabs=chk, Heff_minus_Hdd=float(np.abs(Heff - Hdd).max() / np.abs(Hdd).max()),
                        Hrev_plus_Hdd=float(np.abs(Hrev + Hdd).max() / np.abs(Hdd).max()))
    print(json.dumps(st["checks"]), flush=True)
    # exact target
    Ed, Qd = np.linalg.eigh(Hdd)
    if "exact" not in st:
        ex = {}
        for t in a.times:
            U = expm_h(Ed, Qd, t * 1e-6)
            ex[str(t)] = {str(b): signal(N, U, U.conj().T, 0, b)[0] for b in bs}
        st["exact"] = ex
    Jm = float(np.median(np.abs(c * dm).sum(1)))           # native per-spin sum |g| (rad/s)
    st.update(N=N, bs=bs, k_design=a.k, Jm_native_rad_s=Jm, times_us=a.times)
    for x in a.xs:
        tc0 = 2 * math.pi * x / Jm                         # J_m t_c = 2 pi x (nominal)
        tq = min(a.times)
        m0 = max(1, int(round(tq * 1e-6 / tc0)))
        tc = tq * 1e-6 / m0                                # exact commensurate cycle time
        marks = {int(round(t / tq)) * m0: t for t in a.times}
        ncyc = max(marks)
        for kerr in a.kerrs:
            ktrue = a.k * (1 + kerr)
            eig = {"E1": np.linalg.eigh(-c * Az), "E2": np.linalg.eigh(ktrue * c * Az)}
            for dth in a.dths:
                nsh = 1 if dth == 0 else a.shots
                for sh in range(nsh):
                    key = f"x{x}|k{kerr}|d{dth}|s{sh}"
                    if key in st["units"]:
                        continue
                    if time.process_time() - c0 > a.budget_cpu_s:
                        json.dump(st, open(path + ".tmp", "w")); os.replace(path + ".tmp", path)
                        print("budget stop", flush=True); return
                    rng = np.random.default_rng(12345 + 1009 * sh + int(1e4 * dth) + int(1e5 * kerr) + int(100 * x))
                    Uf = leg_unitary(N, eig, Pf, a.k, False, tc, ncyc, rng, dth, set(marks))
                    Vb = leg_unitary(N, eig, Pf, a.k, True, tc, ncyc, rng, dth, set(marks))
                    res = {}
                    for m, t in marks.items():
                        res[str(t)] = {str(b): signal(N, Uf[m], Vb[m], 0, b) for b in bs}
                    st["units"][key] = dict(res=res, ncyc_per_leg={str(t): m for m, t in marks.items()},
                                            tc_us=tc * 1e6, x_actual=Jm * tc / (2 * math.pi))
                    st["cpu_s"] = st.get("cpu_s", 0) + 0
                    json.dump(st, open(path + ".tmp", "w")); os.replace(path + ".tmp", path)
                    dmax = max(abs(res[str(t)][str(b)][0] - st["exact"][str(t)][str(b)]) for t in a.times for b in bs)
                    print(json.dumps(dict(key=key, ncyc=ncyc, maxabs_dS=round(dmax, 4))), flush=True)
    st["cpu_s_last_invocation"] = time.process_time() - c0
    json.dump(st, open(path + ".tmp", "w")); os.replace(path + ".tmp", path)
    print("done", round(time.process_time() - c0, 1), flush=True)


if __name__ == "__main__":
    main()
