"""Echo driver v2 (supersedes fastecho.echo_sector): time subsets, resume-safe per-sector random draws, and two
propagation backends on the same sector-restricted, flip-folded, forward-reusing typicality estimator:
  backend='trotter' : the reference first-order Trotter circuit (spins.pair_list / apply_step), dt = 2 us
  backend='cheb'    : exact continuous-time exp(-iHt) (Chebyshev series on the real sparse sector Hamiltonian),
                      propagated in segments of `every` * dt (the echo times must be multiples of the segment).
Estimators (DERIVED in fastecho.py docstring):
  mode='reference' : psi0 = the reference draw (seed 12345, full space), all sectors -> identical to the reference
                     estimator up to rounding
  mode='flip'      : independent normalised complex-normal x_k per sector k <= N/2,
                     F = sum_k m_k (D_k / 2^N) <x_k| W Z_b W Z_b |x_k>,  m_k = 2 (k < N/2), 1 (k = N/2)
"""
from __future__ import annotations

import json
import math
import os
import time

import numpy as np

import fastecho as FE
from fastecho import SP


class ChebKernel:
    """Exact exp(-i H tau) in one magnetisation sector (no Trotter error).
    H = sum_{i<j} d_ij/4 (2 Z_i Z_j - X_i X_j - Y_i Y_j): diagonal sum_{i<j} d_ij/2 z_i z_j, flip-flop element -d_ij/2
    (consistent with the fused pair gate exp(-i dt H_ij) of spins.apply_step)."""

    def __init__(self, N, idx, dm, tau, tol=1e-14):
        import scipy.sparse as sps
        import scipy.sparse.linalg as spl
        from scipy.special import jv
        pos = np.full(1 << N, -1, dtype=np.int64)
        pos[idx] = np.arange(len(idx))
        Dk = len(idx)
        diag = np.zeros(Dk)
        rows, cols, vals = [], [], []
        for i in range(N):
            zi = 1.0 - 2.0 * ((idx >> i) & 1)
            for j in range(i + 1, N):
                d = dm[i, j]
                zj = 1.0 - 2.0 * ((idx >> j) & 1)
                diag += 0.5 * d * zi * zj
                bi = (idx >> i) & 1
                bj = (idx >> j) & 1
                r = np.nonzero(bi != bj)[0]
                q = pos[idx[r] ^ ((1 << i) | (1 << j))]
                rows.append(r); cols.append(q); vals.append(np.full(len(r), -0.5 * d))
        rows.append(np.arange(Dk)); cols.append(np.arange(Dk)); vals.append(diag)
        H = sps.csr_matrix((np.concatenate(vals), (np.concatenate(rows), np.concatenate(cols))), shape=(Dk, Dk))
        H.sum_duplicates()
        if Dk > 200:
            emax = float(spl.eigsh(H, k=1, which="LA", return_eigenvectors=False, tol=1e-8)[0])
            emin = float(spl.eigsh(H, k=1, which="SA", return_eigenvectors=False, tol=1e-8)[0])
        else:
            ev = np.linalg.eigvalsh(H.toarray())
            emin, emax = float(ev[0]), float(ev[-1])
        half = 0.5 * (emax - emin) * 1.02 + 1e-9
        self.b = 0.5 * (emax + emin)
        self.a = half
        self.H = ((H - self.b * sps.identity(Dk, format="csr")) / half).tocsr()
        self.nnz = int(self.H.nnz)
        self.nbytes = int(self.H.data.nbytes + self.H.indices.nbytes + self.H.indptr.nbytes)
        self.tau = tau
        x = half * tau
        nmax = int(x + 20 * max(x, 1.0) ** (1 / 3) + 40)
        c = jv(np.arange(nmax + 1), x)
        keep = np.nonzero(np.abs(c) > tol)[0]
        self.nterms = int(keep[-1]) + 1
        self.c = c[:self.nterms]
        self.matvecs = 0
        self.spectral_halfwidth = half

    def step(self, v, inverse=False):
        s = -1.0 if inverse else 1.0                 # exp(-i s H tau)
        H = self.H
        ph = -1j * s
        t0 = v.copy()
        t1 = H @ v
        out = self.c[0] * t0 + (2 * self.c[1] * ph) * t1
        for n in range(2, self.nterms):
            t2 = 2 * (H @ t1) - t0
            out += (2 * self.c[n] * ph ** n) * t2
            t0, t1 = t1, t2
        self.matvecs += self.nterms - 1
        v[...] = out * np.exp(-1j * s * self.b * self.tau)
        return v


def echo(dm, dt, a, bs, otimes, every=20, mode="flip", dtype=np.complex64, seed=12345, backend="trotter",
         ckpt=None, log=None, sectors=None, time_budget_s=None):
    """F_ab and S_ab at the echo times `otimes` (Trotter steps).  Returns a dict; if time_budget_s is exceeded the
    run stops after the current sector (checkpoint kept) and returns partial=True."""
    N = len(dm)
    pairs = SP.pair_list(dm, dt)
    otimes = sorted(set([0] + list(otimes)))
    steps = max(otimes)
    unit = 1 if backend == "trotter" else every
    assert all(t % unit == 0 for t in otimes)
    pc = FE.popcounts(N)
    psi_full = FE.reference_psi0(N, seed) if mode == "reference" else None
    all_sectors = list(range(N + 1)) if mode == "reference" else list(range(N // 2 + 1))
    sectors = all_sectors if sectors is None else [k for k in sectors if k in all_sectors]
    st = dict(done={}, secs=0.0)
    if ckpt and os.path.exists(ckpt):
        st = json.load(open(ckpt))
    t_run = time.time()
    rng = np.random.default_rng(seed + 7919 * N)
    stats = dict(sector_secs={}, peak_sector_dim=0, aux_bytes=0, vector_steps=0, cheb_matvecs=0, cheb_terms={})
    partial = False
    for k in range(N + 1):
        x = None
        if mode == "flip" and k <= N // 2:           # draw in order for every sector -> resume-reproducible
            Dk_ = math.comb(N, k)
            x = rng.standard_normal(Dk_) + 1j * rng.standard_normal(Dk_)
            x /= np.linalg.norm(x)
        if k not in sectors or str(k) in st["done"]:
            continue
        if time_budget_s is not None and time.time() - t_run > time_budget_s:
            partial = True
            break
        ts = time.time()
        idx = np.nonzero(pc == k)[0]
        Dk = len(idx)
        if mode == "reference":
            psi = psi_full[idx].astype(dtype); wgt = 1.0
        else:
            psi = x.astype(dtype); wgt = (1.0 if 2 * k == N else 2.0) * Dk / float(1 << N)
        za = FE._zs(N, a, idx)
        zb = {b: FE._zs(N, b, idx) for b in bs}
        if backend == "trotter":
            K = FE.SectorKernel(N, idx, pairs, dtype)
            aux = K.nbytes_maps
        else:
            K = ChebKernel(N, idx, dm, every * dt)
            aux = K.nbytes
            stats["cheb_terms"][str(k)] = K.nterms
        stats["aux_bytes"] = max(stats["aux_bytes"], aux)
        stats["peak_sector_dim"] = max(stats["peak_sector_dim"], Dk)
        phi = psi.copy()
        chi = {b: (zb[b] * psi).astype(dtype) for b in bs}
        Fk = {b: [] for b in bs}
        Sk = {b: [] for b in bs}
        nvs = 0
        for n in range(0, steps + 1, unit):
            if n in otimes:
                u = (za * phi).astype(dtype)
                for b in bs:
                    Sk[b].append(float(np.real(np.vdot(u, chi[b]))) * wgt)
                if n == 0:
                    for b in bs:
                        Fk[b].append(float(np.real(np.vdot(psi, psi))) * wgt)
                else:
                    ub = u.copy()
                    for _ in range(n // unit):
                        K.step(ub, inverse=True); nvs += 1
                    zub = {b: zb[b] * ub for b in bs}
                    del ub
                    for b in bs:
                        vb = (za * chi[b]).astype(dtype)
                        for _ in range(n // unit):
                            K.step(vb, inverse=True); nvs += 1
                        Fk[b].append(float(np.real(np.vdot(zub[b], vb))) * wgt)
                        del vb
                    del zub
            if n == steps:
                break
            K.step(phi); nvs += 1
            for b in bs:
                K.step(chi[b]); nvs += 1
        if backend == "cheb":
            stats["cheb_matvecs"] += K.matvecs
        stats["vector_steps"] += nvs
        st["done"][str(k)] = dict(F={str(b): Fk[b] for b in bs}, S={str(b): Sk[b] for b in bs}, Dk=int(Dk),
                                  secs=time.time() - ts, vector_steps=nvs)
        stats["sector_secs"][str(k)] = time.time() - ts
        st["secs"] = st.get("secs", 0.0) + (time.time() - ts)
        if ckpt:
            json.dump(st, open(ckpt + ".tmp", "w"))
            os.replace(ckpt + ".tmp", ckpt)
        if log:
            log(dict(sector=k, Dk=int(Dk), secs=round(time.time() - ts, 2), cum_secs=round(st["secs"], 1)))
        del K, phi, chi, psi
    done = [k for k in all_sectors if str(k) in st["done"]]
    complete = all(str(k) in st["done"] for k in all_sectors)
    F = {str(b): np.sum([st["done"][str(k)]["F"][str(b)] for k in done], axis=0).tolist() for b in bs} if done else {}
    S = {str(b): np.sum([st["done"][str(k)]["S"][str(b)] for k in done], axis=0).tolist() for b in bs} if done else {}
    return dict(N=N, mode=mode, backend=backend, dtype=np.dtype(dtype).name, times_us=[n * dt * 1e6 for n in otimes],
                otimes_steps=otimes, F=F, S=S, complete=complete, partial=partial or not complete,
                sectors_done=done, cpu_secs_total=st.get("secs", 0.0),
                sector_secs={k: v["secs"] for k, v in st["done"].items()},
                vector_steps_total=int(sum(v.get("vector_steps", 0) for v in st["done"].values())), stats=stats)


# ============================================================================= union-of-sectors driver (v3)
def union_basis(N, sectors):
    pc = FE.popcounts(N)
    return np.nonzero(np.isin(pc, list(sectors)))[0], pc


def echo_union(dm, dt, a, bs, otimes, every=20, mode="flip", dtype=np.complex64, seed=12345, backend="trotter",
               ckpt_prefix=None, log=None, time_budget_s=None, stop_at_step=None):
    """Same estimator as echo(), but all folded sectors are evolved as ONE vector on their union (the union of
    magnetisation sectors is invariant under every pair gate), with the sector weights folded into the amplitudes:
        psi = (+)_k sqrt(w_k) x_k,  F = Re <Z_b W psi, W Z_b psi>  (block-diagonal operators => sum_k w_k <x_k|.|x_k>)
    This removes the per-sector Python overhead.  Random draws are identical to echo() (same rng stream), so the
    two drivers give the same numbers up to rounding.  Checkpoint after every echo time: forward vectors (.npz) +
    accumulated F/S (.json), atomic replace; a restarted run resumes from the last completed echo time."""
    N = len(dm)
    pairs = SP.pair_list(dm, dt)
    otimes = sorted(set([0] + list(otimes)))
    steps = max(otimes)
    unit = 1 if backend == "trotter" else every
    sectors = list(range(N + 1)) if mode == "reference" else list(range(N // 2 + 1))
    idx, pc = union_basis(N, sectors)
    pcu = pc[idx]
    if mode == "reference":
        psi = FE.reference_psi0(N, seed)[idx].astype(np.complex128)
    else:
        rng = np.random.default_rng(seed + 7919 * N)
        psi = np.zeros(len(idx), np.complex128)
        for k in range(N // 2 + 1):
            Dk = math.comb(N, k)
            x = rng.standard_normal(Dk) + 1j * rng.standard_normal(Dk)
            x /= np.linalg.norm(x)
            w = (1.0 if 2 * k == N else 2.0) * Dk / float(1 << N)
            psi[pcu == k] = math.sqrt(w) * x          # idx is sorted, pc==k subset is sorted: same order as echo()
    psi = psi.astype(dtype)
    del pc
    za = FE._zs(N, a, idx)
    zb = {b: FE._zs(N, b, idx) for b in bs}
    t_build = time.time()
    if backend == "trotter":
        K = FE.SectorKernel(N, idx, pairs, dtype)
        aux = K.nbytes_maps
    else:
        raise NotImplementedError("use echo() for the Chebyshev backend (per-sector H)")
    t_build = time.time() - t_build
    ck_json = (ckpt_prefix + ".ckpt.json") if ckpt_prefix else None
    ck_npz = (ckpt_prefix + ".ckpt.npz") if ckpt_prefix else None
    st = dict(F={str(b): {} for b in bs}, S={str(b): {} for b in bs}, pos=0, pe=None, secs=0.0, vector_steps=0)
    phi = psi.copy()
    chi = {b: (zb[b] * psi).astype(dtype) for b in bs}
    zub = None
    if ck_json and os.path.exists(ck_json) and os.path.exists(ck_npz):
        st = json.load(open(ck_json))
        with np.load(ck_npz) as z:                      # context manager: release the file (Windows replace)
            phi = np.array(z["phi"], dtype=dtype)
            chi = {b: np.array(z[f"chi{b}"], dtype=dtype) for b in bs}
            if st.get("pe"):
                zub = {b: np.array(z[f"zub{b}"], dtype=dtype) for b in bs}
        if log:
            log(dict(resumed_at_step=st["pos"], partial_echo=st.get("pe")))
    tick = [time.time()]

    def save(with_zub):
        st["secs"] += time.time() - tick[0]
        tick[0] = time.time()
        if not ck_json:
            return
        arrs = dict(phi=phi, **{f"chi{b}": chi[b] for b in bs})
        if with_zub:
            arrs.update({f"zub{b}": zub[b] for b in bs})
        np.savez(ck_npz + ".tmp.npz", **arrs)
        os.replace(ck_npz + ".tmp.npz", ck_npz)
        json.dump(st, open(ck_json + ".tmp", "w"))
        os.replace(ck_json + ".tmp", ck_json)

    def save_json():
        st["secs"] += time.time() - tick[0]
        tick[0] = time.time()
        if ck_json:
            json.dump(st, open(ck_json + ".tmp", "w"))
            os.replace(ck_json + ".tmp", ck_json)

    t_run = time.time()
    partial = False
    n = int(st["pos"])
    while True:
        if n in otimes and not all(str(n) in st["F"][str(b)] for b in bs):
            ts = time.time()
            if n == 0:
                u = (za * phi).astype(dtype)
                for b in bs:
                    st["S"][str(b)][str(n)] = float(np.real(np.vdot(u, chi[b])))
                    st["F"][str(b)][str(n)] = float(np.real(np.vdot(psi, psi)))
            else:
                if not st.get("pe") or st["pe"]["n"] != n:
                    ub = (za * phi).astype(dtype)
                    for b in bs:
                        st["S"][str(b)][str(n)] = float(np.real(np.vdot(ub, chi[b])))
                    for _ in range(n // unit):
                        K.step(ub, inverse=True)
                    st["vector_steps"] += n // unit
                    zub = {b: zb[b] * ub for b in bs}
                    del ub
                    st["pe"] = dict(n=n, bs_done=[])
                    st["pos"] = n                               # phi/chi on disk are at step n
                    save(True)                                  # leg-level checkpoint
                for b in bs:
                    if b in st["pe"]["bs_done"]:
                        continue
                    vb = (za * chi[b]).astype(dtype)
                    for _ in range(n // unit):
                        K.step(vb, inverse=True)
                    st["vector_steps"] += n // unit
                    st["F"][str(b)][str(n)] = float(np.real(np.vdot(zub[b], vb)))
                    del vb
                    st["pe"]["bs_done"].append(b)
                    save_json()                                 # leg-level checkpoint (zub already on disk)
                    if time_budget_s is not None and time.time() - t_run > time_budget_s and len(st["pe"]["bs_done"]) < len(bs):
                        partial = True
                        break
                if partial:
                    break
            st["pe"] = None
            zub = None
            st["pos"] = n
            st.setdefault("point_secs", {})[str(n)] = time.time() - ts
            save(False)
            if log:
                log(dict(t_step=n, t_us=n * dt * 1e6, secs=round(time.time() - ts, 1), cum=round(st["secs"], 1),
                         F={b: round(st["F"][str(b)][str(n)], 4) for b in bs}))
        if n == steps:
            break
        if time_budget_s is not None and time.time() - t_run > time_budget_s and n in otimes:
            partial = True
            break
        if stop_at_step is not None and n >= stop_at_step and n in otimes:
            partial = True
            break
        K.step(phi)
        for b in bs:
            K.step(chi[b])
        st["vector_steps"] += 1 + len(bs)
        n += unit
    complete = all(str(t) in st["F"][str(b)] for t in otimes for b in bs)
    F = {str(b): [st["F"][str(b)].get(str(t)) for t in otimes] for b in bs}
    S = {str(b): [st["S"][str(b)].get(str(t)) for t in otimes] for b in bs}
    return dict(N=N, mode=mode, backend=backend, dtype=np.dtype(dtype).name, driver="union",
                times_us=[t * dt * 1e6 for t in otimes], otimes_steps=otimes, F=F, S=S, complete=complete,
                partial=partial or not complete, cpu_secs_total=st["secs"], vector_steps_total=st["vector_steps"],
                union_dim=int(len(idx)), aux_bytes=int(aux), build_s=t_build, point_secs=st.get("point_secs", {}))
