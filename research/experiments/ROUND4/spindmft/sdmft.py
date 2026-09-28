"""spinDMFT adversary for the protein 1H dipolar network (ROUND4 lane `spindmft`).

Model (identical to qapf.nmr.spins): H = sum_{i<j} d_ij (2 S_i^z S_j^z - S_i^x S_j^x - S_i^y S_j^y), S = sigma/2,
d_ij from SP.couplings, b0 = random_b0(1000).  Infinite temperature.

1. sr-spinDMFT (site-resolved spinDMFT; Graesser et al. PRR 3, 043168 (2021), arXiv:2107.07821, in its disordered
   form): spin i sees a classical Gaussian field V_i(t) with
       <V_i^z(t) V_i^z(t')> = sum_j d_ij^2 g_j^z(t-t'),   <V_i^x V_i^x> = <V_i^y V_i^y> = (1/4) sum_j d_ij^2 g_j^perp,
   (field coefficients c_z = 2, c_perp = -1; <S^a S^a> = g^a / 4), single spin-1/2 dynamics dS/dt = V x S (exact for
   a spin-1/2 in a classical field), g_i^z(t) = E[R_zz(t)], g_i^perp(t) = E[R_xx(t)]; iterate to self-consistency.
2. nl-spinDMFT (Graesser, Hahn, Uhrig, SSNMR 132, 101936 (2024), arXiv:2403.10465, in the form "cluster coupled to
   the spinDMFT mean fields"): cluster C (n_c spins, C[0] = probe a) solved exactly with typicality vectors, the SAME
   fused pair gates in the SAME order as the reference Trotter circuit (dt = 2 us), each cluster spin q driven by
   V_q = sum_{j not in C} c_a d_qj xi_j(t), xi_j independent Gaussian processes with covariance g_j/4 (bath-bath
   cross-correlations neglected: approximation A2).  Fields of different cluster spins are correlated through shared
   bath spins.  Noise is split symmetrically around the pair layer: step = N(2k+1) P N(2k), each N a 1-us rotation
   with the field at its midpoint.
3. OTOC extension (derived here; approximation A3 "quenched Gaussian bath"): F_ab = E_xi Tr[W Z_b W Z_b]/2^n_c,
   W = U_xi^dag Z_a U_xi with the SAME realisation xi in both branches.

Estimators per sample m (one bath realisation + one random unit vector psi_m in C^{2^n_c}):
   G_ja(t) = Re <U psi|Z_j|U Z_a psi>  (-> Tr[Z_j(t) Z_a]/2^n),  G_ab(t) = Re <U psi|Z_a|U Z_b psi>
   F_ab(t) = Re <W psi|Z_b|W Z_b psi>.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np
import scipy.linalg as sla

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

DT = 2e-6          # reference Trotter step (s)
H_US = 1.0         # field grid spacing (us) = DT/2


# ----------------------------------------------------------------------------- instance (as the round-3 reference)
def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def instrument_bs(xyz, probe, K=3, N0=10):
    idx = SP.cluster(xyz, probe, N0)
    X0 = xyz[idx]
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    return sorted(set(far + [int(np.argsort(dist)[1])]))


def load_world(pdb, probe, world):
    """world = 'protein' (all protons, probe-distance order) or an int N (closed probe cluster of N spins).
    World index k = probe-cluster rank k, so C = range(n_c) is the reference probe-cluster family."""
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    n = len(xyz) if world == "protein" else int(world)
    idx = SP.cluster(xyz, probe, len(xyz))[:n]
    D = SP.couplings(xyz[idx], random_b0(1000))
    return dict(D=D, idx=idx, names=[names[i] for i in idx], xyz=xyz[idx], bs=instrument_bs(xyz, probe))


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


# ----------------------------------------------------------------------------- Gaussian processes
def toeplitz_factor(c):
    """L with L L^T = Toeplitz(c) (negative eigenvalues of a noisy estimate clipped to 0)."""
    w, U = np.linalg.eigh(sla.toeplitz(c))
    return U * np.sqrt(np.clip(w, 0.0, None))


def _rodrigues(u, nx, ny, nz, cth, sth):
    """rotate vectors u = (ux, uy, uz) about unit axis n by angle th (right-handed): in place-free."""
    ux, uy, uz = u
    ndot = nx * ux + ny * uy + nz * uz
    cx = ny * uz - nz * uy
    cy = nz * ux - nx * uz
    cz = nx * uy - ny * ux
    om = 1.0 - cth
    return (ux * cth + cx * sth + nx * ndot * om, uy * cth + cy * sth + ny * ndot * om,
            uz * cth + cz * sth + nz * ndot * om)


def single_spin_track(Vx, Vy, Vz, h):
    """Vx.. shape (T, ...) field on grid midpoints; returns E-ready arrays Rzz(t_k), Rxx(t_k), k = 0..T (shape (T+1, ...))."""
    T = Vx.shape[0]
    shp = Vx.shape[1:]
    u = (np.zeros(shp), np.zeros(shp), np.ones(shp))
    w = (np.ones(shp), np.zeros(shp), np.zeros(shp))
    rzz = np.empty((T + 1,) + shp); rxx = np.empty((T + 1,) + shp)
    rzz[0] = 1.0; rxx[0] = 1.0
    for k in range(T):
        vx, vy, vz = Vx[k], Vy[k], Vz[k]
        nrm = np.sqrt(vx * vx + vy * vy + vz * vz) + 1e-300
        th = nrm * h
        c, s = np.cos(th), np.sin(th)
        nx, ny, nz = vx / nrm, vy / nrm, vz / nrm
        u = _rodrigues(u, nx, ny, nz, c, s)
        w = _rodrigues(w, nx, ny, nz, c, s)
        rzz[k + 1] = u[2]; rxx[k + 1] = w[0]
    return rzz, rxx


def sr_spindmft(D, T, M, n_iter, seed, h_us=H_US, chunk=48, g0=None, log=print, sites_out=None):
    """Site-resolved spinDMFT.  Field grid: midpoints (k + 1/2) h, k < T; g on t = k h, k = 0..T.
    Returns dict(gz, gp (N, T+1), history, se of the last iteration for sites_out)."""
    N = len(D)
    h = h_us * 1e-6
    D2 = D ** 2
    np.fill_diagonal(D2, 0.0)
    gz = np.ones((N, T + 1)) if g0 is None else np.array(g0[0], float)
    gp = np.ones((N, T + 1)) if g0 is None else np.array(g0[1], float)
    hist = []
    se_last = {}
    for it in range(n_iter):
        t0 = time.time()
        rng = np.random.default_rng([seed, it])
        covz = D2 @ gz[:, :T]
        covp = 0.25 * (D2 @ gp[:, :T])
        nz_ = np.empty((N, T + 1)); np_ = np.empty((N, T + 1))
        for s0 in range(0, N, chunk):
            s1 = min(N, s0 + chunk)
            n = s1 - s0
            Lz = np.stack([toeplitz_factor(covz[i]) for i in range(s0, s1)])
            Lp = np.stack([toeplitz_factor(covp[i]) for i in range(s0, s1)])
            Vz = np.einsum("ikl,ilm->kim", Lz, rng.standard_normal((n, T, M)), optimize=True)
            Vx = np.einsum("ikl,ilm->kim", Lp, rng.standard_normal((n, T, M)), optimize=True)
            Vy = np.einsum("ikl,ilm->kim", Lp, rng.standard_normal((n, T, M)), optimize=True)
            rzz, rxx = single_spin_track(Vx, Vy, Vz, h)          # (T+1, n, M)
            nz_[s0:s1] = rzz.mean(-1).T
            np_[s0:s1] = rxx.mean(-1).T
            if sites_out is not None and it == n_iter - 1:
                for i in sites_out:
                    if s0 <= i < s1:
                        se_last[int(i)] = dict(se_z=(rzz[:, i - s0].std(-1) / math.sqrt(M)).tolist(),
                                               se_p=(rxx[:, i - s0].std(-1) / math.sqrt(M)).tolist())
        dz = float(np.abs(nz_ - gz).max()); dp = float(np.abs(np_ - gp).max())
        dz_mean = float(np.abs(nz_ - gz).mean())
        gz, gp = nz_, np_
        hist.append(dict(it=it, max_dgz=dz, max_dgp=dp, mean_dgz=dz_mean, secs=time.time() - t0))
        if log:
            log(json.dumps(hist[-1]))
    return dict(gz=gz, gp=gp, history=hist, se_last=se_last)


# ----------------------------------------------------------------------------- embedded exact cluster
def cluster_field_factors(D, C, gz, gp, T):
    """Joint Gaussian field of the cluster spins from the bath B = complement(C):
    cov(V_q^z(t), V_p^z(s)) = sum_{j in B} d_qj d_pj gz_j(|t-s|);  perp: (1/4) sum d d gp_j.
    Returns (Lz, Lp) with L L^T = joint covariance, index (q, t) -> q*T + t."""
    N = len(D)
    C = list(C)
    B = np.array([j for j in range(N) if j not in set(C)], int)
    n = len(C)
    if len(B) == 0:
        return None, None
    Dcb = D[np.ix_(C, B)]
    lag = np.abs(np.arange(T)[:, None] - np.arange(T)[None, :])
    out = []
    for g, fac in ((gz, 1.0), (gp, 0.25)):
        K = fac * np.einsum("qj,pj,jk->qpk", Dcb, Dcb, g[B][:, :T], optimize=True)   # (n, n, T)
        big = K[:, :, lag].transpose(0, 2, 1, 3).reshape(n * T, n * T)
        w, U = np.linalg.eigh(big)
        out.append(U * np.sqrt(np.clip(w, 0.0, None)))
    return out[0], out[1]


class Cluster:
    """Exact n_c-spin cluster with per-sample bath fields.  State array: (B, S, 2^n), bit q of the last index =
    cluster qubit q (same convention as spins.zsign).  Pair layer = the reference fused-pair Trotter step restricted
    to C (SP.sector_step_unitaries, same gate order), applied as total-Z sector blocks (BLAS).  Noise = per-sample
    SU(2) rotations exp(-i h V.S) on each cluster qubit."""

    def __init__(self, D, C, dt=DT, cdtype=np.complex64):
        self.C = list(C)
        self.n = len(C)
        Dc = D[np.ix_(self.C, self.C)]
        self.cdtype = cdtype
        self.z = np.stack([SP.zsign(self.n, q) for q in range(self.n)])       # (n, 2^n)
        perm, blocks, offs = [], [], [0]
        for idx, Uk in SP.sector_step_unitaries(Dc, dt):
            perm.append(idx)
            blocks.append((np.ascontiguousarray(Uk.T.astype(cdtype)), np.ascontiguousarray(Uk.conj().astype(cdtype))))
            offs.append(offs[-1] + len(idx))
        self.perm = np.concatenate(perm)
        self.blocks = blocks
        self.offs = offs

    def pair_layer(self, X, inverse=False):
        B, S, dim = X.shape
        Y = X.reshape(B * S, dim)[:, self.perm]
        for k, (fw, bw) in enumerate(self.blocks):
            a, b = self.offs[k], self.offs[k + 1]
            Y[:, a:b] = Y[:, a:b] @ (bw if inverse else fw)
        X.reshape(B * S, dim)[:, self.perm] = Y
        return X

    def rotate(self, X, R):
        """R: (n, B, 2, 2) per-qubit per-sample unitaries (acting on column vectors)."""
        B, S, dim = X.shape
        n = self.n
        for q in range(n):
            T = X.reshape(B, S * (1 << (n - 1 - q)), 2, 1 << q)
            r = R[q]
            p0 = T[:, :, 0, :].copy()
            p1 = T[:, :, 1, :]
            new1 = r[:, 1, 0, None, None] * p0 + r[:, 1, 1, None, None] * p1
            T[:, :, 0, :] = r[:, 0, 0, None, None] * p0 + r[:, 0, 1, None, None] * p1
            T[:, :, 1, :] = new1
        return X


def su2(V, h, cdtype=np.complex64):
    """V: (3, ...) field (rad/s) -> exp(-i h V.S) = cos(th/2) - i sin(th/2) n.sigma, shape (..., 2, 2)."""
    vx, vy, vz = V
    nrm = np.sqrt(vx * vx + vy * vy + vz * vz) + 1e-300
    c = np.cos(0.5 * nrm * h); s = np.sin(0.5 * nrm * h)
    nx, ny, nz = vx / nrm, vy / nrm, vz / nrm
    u = np.empty(vx.shape + (2, 2), np.complex128)
    u[..., 0, 0] = c - 1j * s * nz
    u[..., 1, 1] = c + 1j * s * nz
    u[..., 0, 1] = -1j * s * (nx - 1j * ny)
    u[..., 1, 0] = -1j * s * (nx + 1j * ny)
    return u.astype(cdtype)


def run_embedded(D, C, bs_local, gz, gp, n_steps, otoc_steps, M, batch, seed, ckpt=None, log=print,
                 budget_s=None, rec=5, Lz=None, Lp=None, cdtype=np.complex64):
    """Embedded-cluster (nl-spinDMFT) two-point and quenched-OTOC estimates.
    C: world indices, C[0] = a.  bs_local: cluster-local indices of the butterfly sites.
    Step k (2 us): u[2k+1] P u[2k]; u[m] = exp(-i h V(m h + h/2).S), h = 1 us.  Two-point recorded every `rec` steps
    and at the OTOC steps.  Returns accumulator dict (sums and sums of squares over samples)."""
    n = len(C)
    T = 2 * n_steps
    h = H_US * 1e-6
    cl = Cluster(D, C, cdtype=cdtype)
    if Lz is None:
        Lz, Lp = cluster_field_factors(D, C, gz, gp, T)
    nb = len(bs_local)
    nbx = max(nb, 1)
    otoc_steps = sorted(otoc_steps)
    rsteps = sorted(set(list(range(0, n_steps + 1, rec)) + otoc_steps + [n_steps]))
    nr = len(rsteps)
    st = dict(done=0, n=0, rsteps=rsteps, G1=np.zeros((nr, n)).tolist(), G2=np.zeros((nr, n)).tolist(),
              Gab1=np.zeros((nr, nbx)).tolist(),
              F1=np.zeros((len(otoc_steps), nbx)).tolist(), F2=np.zeros((len(otoc_steps), nbx)).tolist(),
              secs=0.0, cpu=0.0)
    if ckpt and os.path.exists(ckpt):
        st = json.load(open(ckpt))
    acc = {k: np.array(st[k]) for k in ("G1", "G2", "Gab1", "F1", "F2")}
    acc["F1"] = acc["F1"].reshape(len(otoc_steps), nbx); acc["F2"] = acc["F2"].reshape(len(otoc_steps), nbx)
    nbatch = M // batch
    t_start = time.time()
    dim = 1 << n
    za = cl.z[0].astype(np.float32)
    zf = cl.z.astype(np.float32)
    for ib in range(nbatch):
        if ib < st["done"]:
            continue
        if budget_s is not None and time.time() - t_start > budget_s:
            break
        ts = time.time(); tc = time.process_time()
        rng = np.random.default_rng([seed, ib])
        psi = rng.standard_normal((batch, dim)) + 1j * rng.standard_normal((batch, dim))
        psi /= np.linalg.norm(psi, axis=1, keepdims=True)
        if Lz is not None:
            Vz = (Lz @ rng.standard_normal((n * T, batch))).reshape(n, T, batch)
            Vx = (Lp @ rng.standard_normal((n * T, batch))).reshape(n, T, batch)
            Vy = (Lp @ rng.standard_normal((n * T, batch))).reshape(n, T, batch)
        else:
            Vz = Vx = Vy = np.zeros((n, T, batch))
        u = su2(np.stack([Vx, Vy, Vz]).transpose(0, 2, 1, 3), h, cdtype)     # (T, n, batch, 2, 2)
        A = np.matmul(u[2:T:2], u[1:T - 1:2])                              # A_k = u[2k+2] u[2k+1], k = 0..n_steps-2
        uH = np.conj(np.swapaxes(u, -1, -2)); AH = np.conj(np.swapaxes(A, -1, -2))
        X = np.empty((batch, 2 + nb, dim), cdtype)
        X[:, 0] = psi
        X[:, 1] = cl.z[0] * psi
        for k, b in enumerate(bs_local):
            X[:, 2 + k] = cl.z[b] * psi
        G = np.zeros((nr, n, batch)); Gab = np.zeros((nr, nbx, batch))
        Fs = np.zeros((len(otoc_steps), nbx, batch))
        ri = 0; oi = 0
        s = 0
        while True:
            if s == rsteps[ri]:
                prod = np.conj(X[:, 0]) * X[:, 1]
                G[ri] = np.real(zf @ prod.T)
                pa = np.conj(X[:, 0]) * za
                for k in range(nb):
                    Gab[ri, k] = np.real(np.einsum("md,md->m", pa, X[:, 2 + k]))
                ri += 1
                if oi < len(otoc_steps) and s == otoc_steps[oi]:
                    Y = np.concatenate([X[:, :1], X[:, 2:]], axis=1)
                    Y *= za
                    if s > 0:          # U(s)^dag = u0^+ P^+ A_0^+ P^+ ... A_{s-2}^+ P^+ u_{2s-1}^+ (rightmost first)
                        cl.rotate(Y, uH[2 * s - 1])
                        for k in range(s - 1, -1, -1):
                            cl.pair_layer(Y, inverse=True)
                            cl.rotate(Y, AH[k - 1] if k >= 1 else uH[0])
                    y0c = np.conj(Y[:, 0])
                    for k, b in enumerate(bs_local):
                        Fs[oi, k] = np.real(np.einsum("md,md->m", y0c * zf[b], Y[:, 1 + k]))
                    oi += 1
            if s == n_steps:
                break
            s1 = rsteps[ri]           # forward to the next recorded boundary, merging rotations in between
            cl.rotate(X, u[2 * s])
            for k in range(s, s1):
                cl.pair_layer(X)
                cl.rotate(X, A[k] if k < s1 - 1 else u[2 * k + 1])
            s = s1
        acc["G1"] += G.sum(-1); acc["G2"] += (G ** 2).sum(-1)
        acc["Gab1"] += Gab.sum(-1)
        acc["F1"] += Fs.sum(-1); acc["F2"] += (Fs ** 2).sum(-1)
        st["n"] += batch
        st["done"] = ib + 1
        st["secs"] += time.time() - ts
        st["cpu"] = st.get("cpu", 0.0) + time.process_time() - tc
        for k in acc:
            st[k] = acc[k].tolist()
        if ckpt:
            atomic_json(st, ckpt)
        if log:
            log(json.dumps(dict(batch=ib, secs=round(time.time() - ts, 2), cpu=round(st["cpu"], 1))))
    return st


def summarize(st):
    m = st["n"]
    if m == 0:
        return None
    G = np.array(st["G1"]) / m
    Gse = np.sqrt(np.maximum(np.array(st["G2"]) / m - G ** 2, 0) / m)
    F = np.array(st["F1"]) / m
    Fse = np.sqrt(np.maximum(np.array(st["F2"]) / m - F ** 2, 0) / m)
    Gab = np.array(st["Gab1"]) / m
    H_C = (G ** 2).sum(1) - (Gse ** 2).sum(1)          # bias-corrected sum of squares over j in C
    return dict(M=m, times_us=[2.0 * s for s in st["rsteps"]], G=G.tolist(), G_se=Gse.tolist(),
                Gaa=G[:, 0].tolist(), Gaa_se=Gse[:, 0].tolist(), H_C=H_C.tolist(), sumG_C=G.sum(1).tolist(),
                Gab_direct=Gab.tolist(), F=F.tolist(), F_se=Fse.tolist(), secs=st["secs"], cpu=st.get("cpu"))
