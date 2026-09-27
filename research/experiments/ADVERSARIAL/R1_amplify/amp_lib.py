"""R1 amplify lens: shared library.

Goal: evaluate richer echo observables of the SAME protein 1H dipolar Trotter circuit as scripts/nmr_gate.py, exactly and
under the classical adversaries, from ONE simulation per geometry.

Observable families (Z_a(t) = O, all infinite-temperature, normalised by 2^N):
  S_b     = Tr[O Z_b]                      transfer (C1 baseline)
  F1_b    = Tr[O Z_b O Z_b]                first-order OTOC, local butterfly Z_b (C1 baseline "echo")
  F1_T    = Tr[O Z_T O Z_T], T subset of S multi-site butterflies (Z_T = prod_{s in T} Z_s)
  MQC_S,q = sum_{ij: m_S(i)-m_S(j)=q} |O_ij|^2   coherence-order spectrum w.r.t. the labelled subset S (the Fourier
            transform of the phase-multiplexed echo Tr[O e^{i phi M_S} O e^{-i phi M_S}])
  F2_b    = Tr[(O Z_b)^4]                  second-order OTOC (4 evolution segments)
All diagonal-butterfly observables on S follow from P_delta(t) = sum over (i,j) with bit-difference vector
delta = bits_S(i) - bits_S(j) in {-1,0,1}^|S| of |O_ij|^2 / 2^N (3^|S| bins).  F1_T = sum_delta P_delta prod_{s in T}
(+1 if delta_s = 0 else -1); MQC_q = sum_{delta: sum delta = q} P_delta.

Engines:
  exact_sector   : total-Z sector blocks of the Trotter step (same circuit as qapf.nmr.spins), eigendecomposition,
                   exact deterministic; validated against the stored C1 RAW S/F (see selftest in obs_amplify.py).
  exact_parity   : generic engine for Hamiltonians that conserve only popcount parity (double-quantum H_DQ); dense
                   blocks of 2^(N-1).
  pauli_matrix   : Heisenberg Pauli propagation with coefficient truncation eps (and/or weight cap), identical gate
                   order to qapf.nmr.spins.pauli_correlators; at recorded steps the truncated operator is converted to a
                   dense 2^N matrix by a Walsh-Hadamard transform per X-pattern (O(4^N N)), and ALL observables are
                   evaluated from it (plain, norm-corrected, and total-Z-sector-projected estimators; the adversary may
                   pick the best).
Tags: code, not claims.  Single-threaded use only (set OMP/MKL/OPENBLAS_NUM_THREADS=1 before import).
"""
from __future__ import annotations

import itertools
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

PC16 = SP._PC16


def popcount(a):
    a = np.asarray(a, np.int64)
    return PC16[a & 0xFFFF] + PC16[(a >> 16) & 0xFFFF]


# ============================================================================ geometry (replicates scripts/nmr_gate.py)
def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def job_geometry(pdb="1UBQ", probe=19, N=10, orient=0, hn_only=False, K=3):
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    if hn_only:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        names = [names[i] for i in keep]; xyz = xyz[keep]; resid = np.asarray(resid)[keep]
        probe = keep.index(probe)
    idx = SP.cluster(xyz, probe, N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    params = []
    for k in far:
        u = (X0[k] - X0[0]) / dist[k]
        params.append(dict(name=f"radial_{names[idx[k]]}", move=[(int(k), u.tolist())], r=float(dist[k])))
    pres = resid[idx[0]]
    cnt = {}
    for i in range(N):
        cnt[resid[idx[i]]] = cnt.get(resid[idx[i]], 0) + 1
    kfar = next((int(k) for k in np.argsort(-dist) if resid[idx[k]] != pres and cnt[resid[idx[k]]] >= 2), None)
    if kfar is not None:
        kres = resid[idx[kfar]]
        grp = [int(i) for i in range(N) if resid[idx[i]] == kres]
        ug = (X0[kfar] - X0[0]) / dist[kfar]
        params.append(dict(name=f"rigid_res{kres}", move=[(i, ug.tolist()) for i in grp], r=float(dist[kfar]),
                           n_moved=len(grp)))
    # drop exact duplicates (rigid shift of a single-proton residue == radial move)
    uniq, seen = [], []
    for p in params:
        key = sorted((i, tuple(np.round(u, 12))) for i, u in p["move"])
        if key in seen:
            continue
        seen.append(key); uniq.append(p)
    return dict(names=names, xyz=xyz, resid=resid, idx=idx, X0=X0, b0=b0, dist=dist, far=far, bs=bs, params=uniq,
                probe_local=probe, cluster_names=[names[i] for i in idx])


def displaced(X0, p, sgn, h):
    X = X0.copy()
    for (i, u) in p["move"]:
        X[i] = X[i] + sgn * h * np.asarray(u)
    return X


# ============================================================================ P_delta helpers
def delta_codes(rows, cols, S):
    """code(i,j) = sum_s 3^s (bit_s(i) - bit_s(j) + 1) for label arrays rows (n,) cols (m,)."""
    code = np.zeros((len(rows), len(cols)), np.int64)
    for s_i, s in enumerate(S):
        bi = (rows >> s) & 1
        bj = (cols >> s) & 1
        code += (3 ** s_i) * (bi[:, None] - bj[None, :] + 1)
    return code


def delta_table(nS):
    """array (3^nS, nS) of delta vectors in {-1,0,1} for each code."""
    return np.array(list(itertools.product(*([(-1, 0, 1)] * nS))))[:, ::-1]  # code = sum 3^s (d_s+1), s = column


def derived_from_pdelta(P, nS):
    """P: (nt, 3^nS).  Returns dict of families: F1_single (nt,nS), F1_multi (nt, 2^nS-1-nS), MQC (nt, nS) for q=1..nS
    (one-sided; I_-q = I_q), plus the check sum (total norm)."""
    D = delta_table(nS)
    Z = np.where(D == 0, 1.0, -1.0)                       # per-site sign factor
    subsets = [T for r in range(1, nS + 1) for T in itertools.combinations(range(nS), r)]
    FT = np.stack([P @ np.prod(Z[:, list(T)], axis=1) for T in subsets], axis=1)
    single = FT[:, :nS]
    multi = FT[:, nS:]
    q = D.sum(1)
    MQC = np.stack([P[:, q == k].sum(1) for k in range(1, nS + 1)], axis=1)
    return dict(F1_single=single, F1_multi=multi, MQC=MQC, norm=P.sum(1), subsets=[list(T) for T in subsets])


# ============================================================================ exact engine: total-Z sectors
def exact_sector(dmat, dt, n_steps, a, bs, rec, want_F2=True, want_P=True):
    """Exact observables for the SAME fused-pair Trotter circuit (qapf.nmr.spins.sector_step_unitaries).
    Returns dict(times, S (nt, nb), F1 (nt, nb), F2 (nt, nb) or None, P (nt, 3^nb) or None)."""
    N = len(dmat)
    D = 1 << N
    times = list(range(0, n_steps + 1, rec))
    nt, nb = len(times), len(bs)
    S = np.zeros((nt, nb)); F1 = np.zeros((nt, nb)); F2 = np.zeros((nt, nb)) if want_F2 else None
    P = np.zeros((nt, 3 ** nb)) if want_P else None
    za_full = SP.zsign(N, a)
    for idx, Uk in SP.sector_step_unitaries(dmat, dt):
        Q, lam = SP._unitary_eig(Uk)
        del Uk
        Qh = Q.conj().T
        A = (Qh * za_full[idx]) @ Q
        lc = lam.conj()
        Bm = [(Qh * SP.zsign(N, b)[idx]) @ Q for b in bs]
        zb = [SP.zsign(N, b)[idx] for b in bs]
        codes = delta_codes(idx, idx, bs) if want_P else None
        for ti, n_ in enumerate(times):
            ph = np.outer(lc ** n_, lam ** n_)
            Ot = A * ph                                    # eigenbasis
            Oc = Q @ Ot @ Qh                               # computational basis block
            dg = np.real(np.diag(Oc))
            A2 = np.abs(Oc) ** 2
            for bi in range(nb):
                S[ti, bi] += float((dg * zb[bi]).sum())
                F1[ti, bi] += float((zb[bi][:, None] * A2 * zb[bi][None, :]).sum())
                if want_F2:
                    PB = Ot @ Bm[bi]
                    PB2 = PB @ PB
                    F2[ti, bi] += float(np.real((PB2 * PB2.T).sum()))
            if want_P:
                P[ti] += np.bincount(codes.ravel(), weights=A2.ravel(), minlength=3 ** nb)
    out = dict(times=np.array(times) * dt, S=S / D, F1=F1 / D, F2=(F2 / D if want_F2 else None),
               P=(P / D if want_P else None))
    return out


# ============================================================================ generic parity-conserving engine (DQ etc.)
def build_step_unitary_generic(N, pair_terms, dt, block_idx):
    """pair_terms: list of (i, j, cxx, cyy, czz) (rad/s) meaning H_ij = cxx XX + cyy YY + czz ZZ.  Each pair factor
    exp(-i dt H_ij) is exact (the three commute).  Step U = prod over pairs in list order (first applied first).
    Restricted to the basis states block_idx (must be invariant).  Returns dense U (n x n)."""
    n = len(block_idx)
    pos = np.full(1 << N, -1, np.int64); pos[block_idx] = np.arange(n)
    U = np.eye(n, dtype=complex)
    for (i, j, cxx, cyy, czz) in pair_terms:
        # 4x4 in basis |b_j b_i> ordering via masks.  H_ij on |00>,|11> (same bits): czz on diag; XX,YY couple 00<->11
        # with amplitude (cxx - cyy); on |01>,|10>: -czz diag, coupling (cxx + cyy).
        bi = (block_idx >> i) & 1; bj = (block_idx >> j) & 1
        m = (1 << i) | (1 << j)
        # same-parity pair (00 <-> 11): 2x2 [[czz, cxx-cyy],[cxx-cyy, czz]]
        for sel, off, diag in (((bi == 0) & (bj == 0), cxx - cyy, czz), ((bi == 0) & (bj == 1), cxx + cyy, -czz)):
            r = np.nonzero(sel)[0]
            if not len(r):
                continue
            p = pos[block_idx[r] ^ m]
            if (p < 0).any():
                raise ValueError("block not invariant")
            # exp(-i dt [[diag, off],[off, diag]]) = e^{-i dt diag} [[cos(dt off), -i sin(dt off)], [.., cos]]
            ph = complex(math.cos(dt * diag), -math.sin(dt * diag))
            c, s = math.cos(dt * off), math.sin(dt * off)
            x0 = U[r].copy(); x1 = U[p]
            U[r] = ph * (c * x0 - 1j * s * x1)
            U[p] = ph * (-1j * s * x0 + c * x1)
    return U


def exact_parity(N, pair_terms, dt, n_steps, a, bs, rec, want_P=True, want_F2=False):
    """Exact observables for a pair Hamiltonian that conserves popcount parity (e.g. double-quantum).  Same outputs as
    exact_sector plus MQC_tot (nt, N+1): total coherence-order spectrum |q| = 0..N (one-sided, I_q + I_-q for q>0)."""
    D = 1 << N
    times = list(range(0, n_steps + 1, rec))
    nt, nb = len(times), len(bs)
    S = np.zeros((nt, nb)); F1 = np.zeros((nt, nb)); F2 = np.zeros((nt, nb)) if want_F2 else None
    P = np.zeros((nt, 3 ** nb)) if want_P else None
    MQ = np.zeros((nt, N + 1))
    pcall = popcount(np.arange(D))
    za_full = SP.zsign(N, a)
    for par in (0, 1):
        idx = np.nonzero(pcall % 2 == par)[0]
        U = build_step_unitary_generic(N, pair_terms, dt, idx)
        Q, lam = SP._unitary_eig(U)
        del U
        Qh = Q.conj().T
        A = (Qh * za_full[idx]) @ Q
        lc = lam.conj()
        zb = [SP.zsign(N, b)[idx] for b in bs]
        Bm = [(Qh * zb_) @ Q for zb_ in zb] if want_F2 else None
        codes = delta_codes(idx, idx, bs) if want_P else None
        dq = np.abs(pcall[idx][:, None] - pcall[idx][None, :])
        for ti, n_ in enumerate(times):
            ph = np.outer(lc ** n_, lam ** n_)
            Ot = A * ph
            Oc = Q @ Ot @ Qh
            dg = np.real(np.diag(Oc))
            A2 = np.abs(Oc) ** 2
            for bi in range(nb):
                S[ti, bi] += float((dg * zb[bi]).sum())
                F1[ti, bi] += float((zb[bi][:, None] * A2 * zb[bi][None, :]).sum())
                if want_F2:
                    PB = Ot @ Bm[bi]; PB2 = PB @ PB
                    F2[ti, bi] += float(np.real((PB2 * PB2.T).sum()))
            if want_P:
                P[ti] += np.bincount(codes.ravel(), weights=A2.ravel(), minlength=3 ** nb)
            MQ[ti] += np.bincount(dq.ravel(), weights=A2.ravel(), minlength=N + 1)
    return dict(times=np.array(times) * dt, S=S / D, F1=F1 / D, F2=(F2 / D if want_F2 else None),
                P=(P / D if want_P else None), MQC_tot=MQ / D)


# ============================================================================ Pauli adversary -> dense matrix
def pauli_to_matrix(op):
    """Dense 2^N matrix of sum_P c_P P(x,z), P(x,z) = i^{x.z} X^x Z^z.  M[r ^ x, r] = sum_z c i^{x.z} (-1)^{z.r}
    = WHT_z(v_x)[r].  O(4^N N)."""
    N = op.N
    D = 1 << N
    x = op.x.astype(np.int64); z = op.z.astype(np.int64); c = op.c
    ph = (1j) ** (popcount(x & z) % 4)
    V = np.zeros((D, D), complex)                         # V[x, z]
    np.add.at(V, (x, z), c * ph)
    # Walsh-Hadamard along axis 1 (z -> r): W[x, r] = sum_z V[x,z] (-1)^{popcount(z & r)}
    W = V.reshape((D,) + (2,) * N)
    for ax in range(1, N + 1):
        a0 = np.take(W, 0, axis=ax); a1 = np.take(W, 1, axis=ax)
        W = np.stack([a0 + a1, a0 - a1], axis=ax)
    W = W.reshape(D, D)
    r = np.arange(D)
    M = np.zeros((D, D), complex)
    xs = np.arange(D)
    M[(r[None, :] ^ xs[:, None]), r[None, :]] = W
    return M


def matrix_observables(M, N, a, bs, want_F2=True, want_P=True, proj=False, want_MQtot=False):
    """Observables from a dense operator matrix M (approximating O = Z_a(t)).  proj: False | 'z' (total-Z blocks) |
    'parity' (popcount-parity blocks) symmetry projection of M before evaluation."""
    D = 1 << N
    if proj:
        pc = popcount(np.arange(D))
        if proj == "parity":
            M = M * ((pc[:, None] % 2) == (pc[None, :] % 2))
        else:
            M = M * (pc[:, None] == pc[None, :])
    dg = np.real(np.diag(M))
    A2 = np.abs(M) ** 2
    zb = [SP.zsign(N, b) for b in bs]
    S = np.array([(dg * z).sum() / D for z in zb])
    F1 = np.array([(z[:, None] * A2 * z[None, :]).sum() / D for z in zb])
    F2 = None
    if want_F2:
        F2 = []
        for z in zb:
            MB = M * z[None, :]
            M2 = MB @ MB
            F2.append(float(np.real((M2 * M2.T).sum())) / D)
        F2 = np.array(F2)
    P = None
    if want_P:
        r = np.arange(D)
        P = np.bincount(delta_codes(r, r, bs).ravel(), weights=A2.ravel(), minlength=3 ** len(bs)) / D
    MQ = None
    if want_MQtot:
        pc = popcount(np.arange(D))
        MQ = np.bincount(np.abs(pc[:, None] - pc[None, :]).ravel(), weights=A2.ravel(), minlength=N + 1) / D
    return S, F1, F2, P, MQ, float(A2.sum() / D)


def pauli_run(N, gate_seq, n_steps, a, bs, rec, eps=1e-4, wmax=None, time_budget_s=None, max_steps=None,
              want_F2=True, want_MQtot=False, max_strings=None, proj_kind="z"):
    """Heisenberg evolution of Z_a through the gate sequence (per Trotter step: list of pair groups, each a list of
    commuting (gx, gz, theta) Pauli rotations exp(-i theta G); groups applied in list order, first applied first),
    truncated by |c| <= eps and weight <= wmax once per group.
    At recorded steps: dense matrix -> observables for three estimators: plain, normcorr (M / sqrt(Tr M^2 / 2^N)),
    proj (total-Z block projection; only meaningful for Z-conserving circuits).
    Returns dict of estimator -> dict(times, S, F1, F2, P, MQ) and stats."""
    op = SP.PauliOp.single_z(N, a)
    ests = {k: dict(S=[], F1=[], F2=[], P=[], MQ=[]) for k in ("plain", "proj")}   # normcorr = plain / norm^deg
    times, nstr, norm2 = [], [], []
    t0 = time.time()
    last = n_steps if max_steps is None else min(n_steps, max_steps)
    k = 0
    for k in range(last + 1):
        if k % rec == 0:
            M = pauli_to_matrix(op)
            n2 = float((op.c ** 2).sum())
            times.append(k); nstr.append(len(op.c)); norm2.append(n2)
            for est in ests:
                Mx, pj = M, (proj_kind if est == "proj" else False)
                S_, F1_, F2_, P_, MQ_, _ = matrix_observables(Mx, N, a, bs, want_F2=want_F2, proj=pj,
                                                              want_MQtot=want_MQtot)
                e = ests[est]
                e["S"].append(S_); e["F1"].append(F1_); e["F2"].append(F2_); e["P"].append(P_); e["MQ"].append(MQ_)
            del M
        if k == last:
            break
        if time_budget_s and time.time() - t0 > time_budget_s:
            break
        # Heisenberg: conjugate by the LAST pair group of the step first.  Within a group (commuting rotations of one
        # pair) no truncation; weight cap + |c| <= eps compaction once per group (identical to spins.conj_pair).
        for grp in reversed(gate_seq):
            for (gx, gz, th) in grp:
                op = SP.conj_rotation(op, gx, gz, th, None, 0.0, compact=False)
            if wmax is not None:
                w = SP._popcount(op.x | op.z)
                keep = w <= wmax
                op.x, op.z, op.c = op.x[keep], op.z[keep], op.c[keep]
            op = op.compact(eps)
            if max_strings and len(op.c) > max_strings:
                o = np.argsort(-np.abs(op.c))[:max_strings]
                op.x, op.z, op.c = op.x[o], op.z[o], op.c[o]
    out = {}
    for est, e in ests.items():
        out[est] = dict(S=np.array(e["S"]), F1=np.array(e["F1"]),
                        F2=(np.array(e["F2"]) if want_F2 else None), P=np.array(e["P"]),
                        MQ=(np.array(e["MQ"]) if want_MQtot else None))
    return out, dict(steps=np.array(times), n_strings=nstr, norm2=norm2, secs=time.time() - t0, last_step=k)


def secular_gate_seq(dmat, dt):
    """Pauli-rotation sequence equal to qapf.nmr.spins fused pairs: per pair (in pair_list order) the fused propagator
    exp(-i a ZZ) exp(+i a/2 XX) exp(+i a/2 YY), a = d dt/2 (commuting).  As rotations exp(-i theta G):
    ZZ theta = a, XX theta = -a/2, YY theta = -a/2."""
    seq = []
    for (i, j, ddt) in SP.pair_list(dmat, dt):
        a = ddt / 2.0
        m = np.uint64((1 << i) | (1 << j)); z0 = np.uint64(0)
        seq.append([(m, m, -a / 2), (m, z0, -a / 2), (z0, m, a)])   # YY, XX, ZZ (commuting; spins.conj_pair order)
    return seq


def dq_gate_seq(dmat, dt, s=math.sqrt(3.0)):
    """Double-quantum H_DQ = sum (s d/4)(XX - YY) (pair Frobenius norm matched to the secular form at s = sqrt 3)."""
    seq = []
    N = len(dmat)
    for i in range(N):
        for j in range(i + 1, N):
            d = dmat[i, j]
            m = np.uint64((1 << i) | (1 << j)); z0 = np.uint64(0)
            seq.append([(m, z0, dt * s * d / 4), (m, m, -dt * s * d / 4)])   # XX, YY (commuting)
    return seq


def dq_pair_terms(dmat, s=math.sqrt(3.0)):
    N = len(dmat)
    return [(i, j, s * dmat[i, j] / 4, -s * dmat[i, j] / 4, 0.0) for i in range(N) for j in range(i + 1, N)]


def secular_pair_terms(dmat):
    N = len(dmat)
    return [(i, j, -dmat[i, j] / 4, -dmat[i, j] / 4, dmat[i, j] / 2) for i in range(N) for j in range(i + 1, N)]


# ============================================================================ Fisher tools
def fisher(J, sigma):
    """J: (n_params, n_data) derivative matrix -> Fisher matrix."""
    return J @ J.T / sigma ** 2


def crb(F, reg=1e-12):
    Fr = F + reg * max(np.trace(F), 1e-30) * np.eye(len(F))
    return np.sqrt(np.clip(np.diag(np.linalg.inv(Fr)), 0, None))


def gen_eigs(Ft, Fe, reg=1e-9):
    A = Fe + reg * max(np.trace(Ft), 1e-30) * np.eye(len(Fe))
    L = np.linalg.cholesky(A)
    Li = np.linalg.inv(L)
    return np.linalg.eigvalsh(Li @ Ft @ Li.T)


def first_fail(bias, thr):
    """index of first time with bias > thr (bias: (nt,) ); len if never."""
    bad = np.nonzero(bias > thr)[0]
    return int(bad[0]) if len(bad) else len(bias)


def jsonable(o):
    if isinstance(o, dict):
        return {str(k): jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)):
        return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray):
        return jsonable(o.tolist())
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, float) and not math.isfinite(o):
        return None
    return o
