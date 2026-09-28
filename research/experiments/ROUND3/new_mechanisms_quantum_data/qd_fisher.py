"""ROUND3 lane new_mechanisms_quantum_data: learning protein 1H-network geometry from QUANTUM DATA,
with vs without quantum memory, on a protein-derived instance (1UBQ / 1PGA dense 1H clusters, N = 10-12).

State family (NMR selective-polarisation experiment, the repo's Program-C setting):
    rho(theta, t) = (I + p X)/d,   X = U Z_a U^dag,   U = exp(-i H_dd(theta) t),   d = 2^N,
p = polarisation of the probe proton a (thermal 1H at 14.1 T / 298 K: p ~ 4.8e-5; p = 1 is the best physical case),
all other protons at infinite temperature (the high-temperature NMR regime).  H_dd = secular homonuclear dipolar
Hamiltonian from qapf.nmr.spins.couplings (same geometry, B0 orientation and parameters as scripts/nmr_gate.py).
theta = structural parameters (radial shift of the K most distant cluster protons; rigid shift of one residue).

Exact identities used (DERIVED, see README):
  X^2 = I and X dX + dX X = 0  =>  SLD L_i = p dX_i exactly;  QFI_ij = (p^2/d) tr(dX_i dX_j) = p^2 sum_P g_iP g_jP,
  with X = sum_P c_P P, g_iP = d c_P / d theta_i  (Pauli coefficients, real).
  Holevo incompatibility D_ij = (p^3/d) Im tr(X dX_i dX_j).
Per-copy classical Fisher information of measurement protocols (leading order in p unless marked exact):
  optimal single copy, one parameter (SLD eigenbasis, Braunstein-Caves): = QFI (exact, all p)
  optimal collective / quantum memory, one parameter: = QFI (QFI additivity) -> memory gain exactly 1
  random local Pauli bases (classical shadows):        p^2 sum_P 3^-|P| g^2          (exact MC over bases also)
  computational (all-Z) basis, all spins:              p^2 sum_{P in {I,Z}^N} g^2   (exact also)
  site-resolved magnetisation <Z_k> only (transfer):   p^2 sum_k g_{Z_k}^2
  random global Clifford (2-design):                   QFI/(d+1)
  two-copy Bell sampling (quantum memory; the HKP / Chen-Gong-Ye protocol), per PAIR of copies:
                                                        p^4 * 4 sum_P c_P^2 g^2      (exact at p = 1, 0.1 also)
  single-copy time-reversed echo with butterfly Z_b (NMR OTOC):  p^2 (dF_ab)^2/(1-p^2 F_ab^2),
                                                        F_ab = sum_P c_P^2 s_b(P), dF = 2 sum c g s_b.
Exact Bell FI via the symplectic transform q_b = d^-2 sum_P (-1)^{omega(b,P)+#Y(P)} tr(P rho)^2.
Exact local-Pauli FI via Monte-Carlo over bases + Walsh-Hadamard of the compatible coefficients.
Transduction noise: per-qubit depolarising channel with Pauli shrink lambda applied to each copy before the
Bell measurement: c_P -> lambda^|P| c_P.

Single-threaded, checkpointed per time point (atomic tmp+replace).  Usage:
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python qd_fisher.py --pdb 1UBQ --probe 19 --N 10
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse  # noqa: E402
import json  # noqa: E402
import math  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

# single-qubit Pauli order 0=I 1=X 2=Y 3=Z ; combined matrix index 2r+c = (00,01,10,11)
W_PAULI = np.array([[0.5, 0, 0, 0.5],
                    [0, 0.5, 0.5, 0],
                    [0, 0.5j, -0.5j, 0],
                    [0.5, 0, 0, -0.5]], dtype=complex)
# symplectic character (-1)^{omega(a,b)}: +1 if the single-qubit Paulis commute
OMEGA = np.array([[1, 1, 1, 1], [1, 1, -1, -1], [1, -1, 1, -1], [1, -1, -1, 1]], dtype=float)


def _np(o):
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, default=_np)
    os.replace(tmp, path)


def random_b0(seed):                                   # identical to scripts/nmr_gate.py
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


# ----------------------------------------------------------------------------------------------- sector dynamics
def sectors(n):
    pc = np.array([bin(i).count("1") for i in range(2 ** n)])
    return [np.nonzero(pc == m)[0] for m in range(n + 1)]


def sector_H(dmat, idx, n):
    """H = sum_{i<j} (d_ij/4)(2 Z_i Z_j - X_i X_j - Y_i Y_j) restricted to one total-Z sector (qubit q = bit q)."""
    dim = len(idx)
    pos = -np.ones(2 ** n, dtype=np.int64)
    pos[idx] = np.arange(dim)
    bits = (idx[:, None] >> np.arange(n)) & 1
    z = 1.0 - 2.0 * bits
    H = np.zeros((dim, dim))
    du = np.triu(dmat, 1)
    H[np.arange(dim), np.arange(dim)] = 0.5 * np.einsum("ai,ij,aj->a", z, du, z)
    for i in range(n):
        for j in range(i + 1, n):
            src = np.nonzero(bits[:, i] != bits[:, j])[0]
            dst = pos[idx[src] ^ ((1 << i) | (1 << j))]
            H[src, dst] += -0.5 * dmat[i, j]
    return H


class Dyn:
    """exp(-i H t) per total-Z sector; Schroedinger-picture X(t) = U Z_a U^dag as sector blocks."""

    def __init__(self, dmat, n, a, secs):
        self.eig = []
        for idx in secs:
            E, V = np.linalg.eigh(sector_H(dmat, idx, n))
            za = 1.0 - 2.0 * ((idx >> a) & 1)
            self.eig.append((E, V, (V.T * za) @ V))

    def X_blocks(self, t):
        out = []
        for (E, V, Zt) in self.eig:
            ph = np.exp(-1j * E * t)
            out.append(V @ ((ph[:, None] * Zt) * ph.conj()[None, :]) @ V.T)
        return out


# ----------------------------------------------------------------------------------------------- Pauli transforms
def pauli_from_blocks(blocks, secs, n):
    """c_P = tr(P M)/d for all 4^n Paulis of the block-diagonal Hermitian M; flat index = sum_q digit_q 4^q
    (digit 0=I 1=X 2=Y 3=Z).  Builds the dense matrix, transposes, frees it, then transforms qubit by qubit."""
    d = 2 ** n
    M = np.zeros((d, d), dtype=complex)
    for B, idx in zip(blocks, secs):
        M[np.ix_(idx, idx)] = B
    perm = [x for k in range(n) for x in (k, n + k)]
    T = np.ascontiguousarray(M.reshape([2] * (2 * n)).transpose(perm)).reshape([4] * n)
    del M
    for k in range(n):
        T = np.moveaxis(np.tensordot(W_PAULI, T, axes=([1], [k])), 0, k)
    out = np.ascontiguousarray(T).reshape(-1)
    del T
    im = float(np.max(np.abs(out.imag)))
    return out.real.copy(), im


def omega_transform(v, n):
    T = v.reshape([4] * n)
    for k in range(n):
        T = np.moveaxis(np.tensordot(OMEGA, T, axes=([1], [k])), 0, k)
    return np.ascontiguousarray(T).reshape(-1)


def digit_arrays(n):
    """weight |P|, number of Y factors, Z-type mask, for the flat Pauli index."""
    idx = np.arange(4 ** n, dtype=np.int64)
    w = np.zeros(4 ** n, dtype=np.uint8)
    ny = np.zeros(4 ** n, dtype=np.uint8)
    ztype = np.ones(4 ** n, dtype=bool)
    for q in range(n):
        dq = (idx // (4 ** q)) % 4
        w += (dq != 0)
        ny += (dq == 2)
        ztype &= (dq == 0) | (dq == 3)
    del idx
    return w, ny, ztype


def fwht(a):
    """Walsh-Hadamard over the last axis (length 2^m), unnormalised: out_o = sum_S (-1)^{popcount(o&S)} a_S."""
    a = np.array(a, dtype=np.float64, copy=True)
    L = a.shape[-1]
    h = 1
    while h < L:
        a = a.reshape(a.shape[:-1] + (L // (2 * h), 2, h))
        x, y = a[..., 0, :].copy(), a[..., 1, :].copy()
        a[..., 0, :], a[..., 1, :] = x + y, x - y
        a = a.reshape(a.shape[:-3] + (L,))
        h *= 2
    return a


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--N", type=int, default=10)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--K", type=int, default=3, help="distant radial parameters (+ rigid residue shift)")
    ap.add_argument("--all-radial", type=int, default=0, help="1 = radial parameter for every non-probe proton")
    ap.add_argument("--h", type=float, default=0.05)
    ap.add_argument("--times", default="5,10,20,40,80,160,320", help="microseconds")
    ap.add_argument("--nbases", type=int, default=400, help="MC bases for the exact local-Pauli FI")
    ap.add_argument("--exact-bell", type=int, default=1)
    ap.add_argument("--out", default=os.path.join(HERE, "out"))
    a = ap.parse_args()
    t_start = time.time()
    n = a.N
    d = 2 ** n
    tag = f"{a.pdb}_p{a.probe}_N{n}_o{a.orient}" + ("_allrad" if a.all_radial else "")
    os.makedirs(a.out, exist_ok=True)
    fj = os.path.join(a.out, tag + ".json")
    fp = fj + ".partial.json"
    if os.path.exists(fj):
        print("exists", fj)
        return
    res = json.load(open(fp)) if os.path.exists(fp) else None

    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    idx = SP.cluster(xyz, a.probe, n)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + a.orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    params = []
    if a.all_radial:
        for k in range(1, n):
            u = (X0[k] - X0[0]) / dist[k]
            params.append(dict(name=f"radial_{names[idx[k]]}", move=[(k, u.tolist())], r=float(dist[k])))
    else:
        far = [int(k) for k in np.argsort(-dist)[:a.K]]
        for k in far:
            u = (X0[k] - X0[0]) / dist[k]
            params.append(dict(name=f"radial_{names[idx[k]]}", move=[(k, u.tolist())], r=float(dist[k])))
        pres = resid[idx[0]]
        cnt = {}
        for i in range(n):
            cnt[resid[idx[i]]] = cnt.get(resid[idx[i]], 0) + 1
        kfar = next((int(k) for k in np.argsort(-dist) if resid[idx[k]] != pres and cnt[resid[idx[k]]] >= 2), None)
        if kfar is not None:
            kres = resid[idx[kfar]]
            grp = [int(i) for i in range(n) if resid[idx[i]] == kres]
            ug = (X0[kfar] - X0[0]) / dist[kfar]
            params.append(dict(name=f"rigid_res{kres}", move=[(i, ug.tolist()) for i in grp], r=float(dist[kfar]),
                               n_moved=len(grp)))
    kpar = len(params)

    def geom(p, sgn):
        X = X0.copy()
        for (i, u) in p["move"]:
            X[i] = X[i] + sgn * a.h * np.asarray(u)
        return X

    secs = sectors(n)
    dm0 = SP.couplings(X0, b0)
    dyn0 = Dyn(dm0, n, 0, secs)
    dyn_pm = [(Dyn(SP.couplings(geom(p, +1), b0), n, 0, secs), Dyn(SP.couplings(geom(p, -1), b0), n, 0, secs))
              for p in params]
    if res is None:
        res = dict(tag=tag, pdb=a.pdb, probe=a.probe, probe_name=names[a.probe], N=n, orient=a.orient,
                   b0=b0.tolist(), h=a.h, params=[{k: v for k, v in p.items() if k != "move"} for p in params],
                   cluster_names=[names[i] for i in idx], dist=dist.tolist(),
                   max_abs_d_kHz=float(np.max(np.abs(dm0)) / (2 * math.pi) / 1e3),
                   cluster_sqrtM2_probe_kHz=float(math.sqrt(np.sum(dm0[0] ** 2) * 9 / 16) / (2 * math.pi) / 1e3),
                   times_us=[], per_time={})

    w, ny, ztype = digit_arrays(n)
    lambdas = [1.0, 0.99, 0.95, 0.9, 0.8, 0.5]
    zq_idx = [3 * 4 ** q for q in range(n)]
    rng = np.random.default_rng(12345)
    bases = rng.integers(1, 4, size=(a.nbases, n))       # random local Pauli bases (1=X,2=Y,3=Z per qubit)
    pw = 4 ** np.arange(n, dtype=np.int64)
    Sidx = np.arange(d, dtype=np.int64)
    Sbits = ((Sidx[:, None] >> np.arange(n)) & 1).astype(np.int64)
    pvals = [1.0, 0.1, 1e-2, 4.8e-5]
    LUT3 = (1.0 / 3.0) ** np.arange(n + 1)
    CH = 1 << 20
    SB = np.array([1.0, -1.0, -1.0, 1.0])                 # does the digit commute with Z_b ?

    def gram(G_arr, wfun):
        """sum_P wfun(P) g_iP g_jP, chunked, float64 accumulation."""
        L = G_arr.shape[1]
        out = np.zeros((kpar, kpar))
        for s_ in range(0, L, CH):
            e_ = min(L, s_ + CH)
            blk = G_arr[:, s_:e_].astype(np.float64)
            out += (blk * wfun(s_, e_)) @ blk.T
        return out

    def axis_sum(v, q, other=None):
        """sum over all Paulis grouped by the digit of qubit q (of v, or of v*other) -> length-4 vector."""
        A, Bb = 4 ** (n - 1 - q), 4 ** q
        if other is None:
            return v.reshape(A, 4, Bb).sum(axis=(0, 2))
        return np.einsum("abc,abc->b", v.reshape(A, 4, Bb), other.reshape(A, 4, Bb))

    for t_us in [float(x) for x in a.times.split(",")]:
        key = f"{t_us:g}"
        if key in res["per_time"]:
            continue
        t = t_us * 1e-6
        t0 = time.time()
        Xb0 = dyn0.X_blocks(t)
        c, im0 = pauli_from_blocks(Xb0, secs, n)
        dXb = []
        g = np.empty((kpar, 4 ** n), dtype=np.float32 if n >= 12 else np.float64)
        ims = [im0]
        for i, (dp, dmn) in enumerate(dyn_pm):
            Bp, Bm = dp.X_blocks(t), dmn.X_blocks(t)
            blocks = [(x - y) / (2 * a.h) for x, y in zip(Bp, Bm)]
            dXb.append(blocks)
            gi, imi = pauli_from_blocks(blocks, secs, n)
            g[i] = gi
            del gi
            ims.append(imi)
        c2 = c * c
        # ---- Gram matrices (per unit p^2; Bell per unit p^4 per PAIR of copies)
        G_Q = gram(g, lambda s_, e_: 1.0)
        G_loc = gram(g, lambda s_, e_: LUT3[w[s_:e_]])
        gz = g[:, ztype].astype(np.float64)
        G_Z = gz @ gz.T
        gm = g[:, zq_idx].astype(np.float64)
        G_mag = gm @ gm.T
        G_bell = {f"{lam:g}": gram(g, lambda s_, e_, lam=lam: 4.0 * c2[s_:e_] * lam ** (4.0 * w[s_:e_]))
                  for lam in lambdas}
        wdist_c = np.bincount(w, weights=c2, minlength=n + 1)
        wdist_g = [np.bincount(w, weights=g[i].astype(np.float64) ** 2, minlength=n + 1) for i in range(kpar)]
        wdist_bell = [np.bincount(w, weights=4 * c2 * g[i].astype(np.float64) ** 2, minlength=n + 1)
                      for i in range(kpar)]
        # ---- single-copy time-reversed echo (NMR OTOC) with butterfly Z_b
        echo = {}
        for b in range(1, n):
            F = float(axis_sum(c2, b) @ SB)
            dF = [2.0 * float(axis_sum(c, b, g[i].astype(np.float64)) @ SB) for i in range(kpar)]
            echo[str(b)] = dict(F=F, dF=dF)
        supp = {f"{thr:g}": int(np.sum(np.abs(c) > thr)) for thr in (1e-1, 1e-2, 1e-3)}
        m90 = []
        for i in range(kpar):
            s = np.sort(g[i].astype(np.float64) ** 2)[::-1]
            cs = np.cumsum(s)
            m90.append(int(np.searchsorted(cs, 0.9 * cs[-1]) + 1))
            del s, cs
        # ---- exact local-Pauli FI (MC over random local bases) and exact all-Z basis, at several p
        loc_exact = {f"{p:g}": np.zeros((kpar, kpar)) for p in pvals}
        zb_exact = {}
        loc_lead = np.zeros((kpar, kpar))
        for B in list(bases) + [None]:
            Bq = np.full(n, 3) if B is None else B
            fl = (Sbits * (Bq[None, :] * pw[None, :])).sum(axis=1)
            gc = fwht(c[fl][None, :])[0]
            gd = fwht(g[:, fl].astype(np.float64))
            for p in pvals:
                den = 1.0 + p * gc
                ok = den > 1e-12
                Fm = (p * p / d) * (gd[:, ok] / den[ok]) @ gd[:, ok].T
                if B is None:
                    zb_exact[f"{p:g}"] = Fm
                else:
                    loc_exact[f"{p:g}"] += Fm / len(bases)
            if B is not None:
                loc_lead += (gd @ gd.T) / d / len(bases)
        # ---- exact two-copy Bell-sampling FI (symplectic transform); full matrix for n <= 10, diagonal otherwise
        bell_exact = {}
        if a.exact_bell:
            sy = np.where(ny % 2 == 1, -1.0, 1.0)
            for p in (1.0, 0.1):
                r2 = (p * p) * c2
                r2[0] = 1.0
                q = omega_transform(sy * r2, n) / d ** 2
                del r2
                ok = q > 1e-18
                qmin, qsum = float(q.min()), float(q.sum())
                if n <= 10:
                    dq_ = np.array([omega_transform(sy * (2.0 * p * p * c * g[i]), n) / d ** 2 for i in range(kpar)])
                    Fb = (dq_[:, ok] / q[ok]) @ dq_[:, ok].T
                    del dq_
                else:
                    Fb = np.full((kpar, kpar), np.nan)
                    for i in range(kpar):
                        dqi = omega_transform(sy * (2.0 * p * p * c * g[i].astype(np.float64)), n) / d ** 2
                        Fb[i, i] = float(np.sum(dqi[ok] ** 2 / q[ok]))
                        del dqi
                bell_exact[f"{p:g}"] = dict(F=Fb, qmin=qmin, qsum=qsum)
                del q, ok
            del sy
        # ---- multi-parameter: split-SLD single-copy protocol and Holevo incompatibility
        Fsplit = []
        xdmax = 0.0
        for i in range(kpar):
            Fi = np.zeros((kpar, kpar))
            for m_ in range(len(secs)):
                A = dXb[i][m_]
                ev, V = np.linalg.eigh((A + A.conj().T) / 2)
                diag = np.array([np.real(np.sum(V.conj() * (dXb[j][m_] @ V), axis=0)) for j in range(kpar)])
                xd = np.real(np.sum(V.conj() * (Xb0[m_] @ V), axis=0))
                nz = np.abs(ev) > 1e-8 * max(1.0, float(np.max(np.abs(ev))))
                if np.any(nz):
                    xdmax = max(xdmax, float(np.max(np.abs(xd[nz]))))
                Fi += diag @ diag.T
            Fsplit.append(Fi / d)
        Dt = np.zeros((kpar, kpar))
        for i in range(kpar):
            Y = [Xb0[m_] @ dXb[i][m_] for m_ in range(len(secs))]
            for j in range(kpar):
                Dt[i, j] = sum(float(np.imag(np.sum(Y[m_] * dXb[j][m_].T))) for m_ in range(len(secs))) / d
        res["per_time"][key] = dict(
            t_us=t_us, im_max=max(ims), G_Q=G_Q, G_loc=G_loc, G_loc_MC_leading=loc_lead, G_Z=G_Z, G_mag=G_mag,
            G_bell=G_bell, loc_exact=loc_exact, zbasis_exact=zb_exact, bell_exact=bell_exact, wdist_c=wdist_c,
            wdist_g=[x.tolist() for x in wdist_g], wdist_bell=[x.tolist() for x in wdist_bell], echo=echo,
            support=supp, m90=m90, Fsplit_unit=[x.tolist() for x in Fsplit], Dtilde=Dt, sld_basis_max_abs_X=xdmax,
            c_norm=float(np.sum(c2)), sec=time.time() - t0)
        res["times_us"].append(t_us)
        atomic_json(fp, res)
        print(f"{tag} t={t_us:g}us {time.time() - t0:.1f}s  QFI/p^2 diag={np.round(np.diag(G_Q), 3)}", flush=True)
        del c, g, c2, gz, gm, dXb, Xb0
    res["wall_s"] = time.time() - t_start
    atomic_json(fj, res)
    if os.path.exists(fp):
        os.replace(fp, fj + ".partial.done.json")
    print("wrote", fj)


if __name__ == "__main__":
    main()
