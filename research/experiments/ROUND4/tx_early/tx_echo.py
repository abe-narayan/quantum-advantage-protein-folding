"""T-X-early exact typicality driver: echo F_ab, two-point G_aj (-> H, floor) and X = F - H - floor.

Circuit, instrument and estimator are those of ROUND3/r1sim_exact_reach (fastecho / echo2 / verify_classical
decomp_echo): 1UBQ probe-centred N-proton cluster, b0 = random_b0(1000), reference first-order Trotter circuit
(spins.pair_list, dt = 2 us, fused pair gates in the order (0,1),(0,2),...), gamma = 0, sites b = instrument_bs.
Flip-folded sector typicality: sectors k <= N/2, R random vectors per sector drawn from
default_rng(seed + 7919 N) in the SAME order as decomp_echo.run(family='probe') (so equal seeds give equal vectors),
weight w_k = m_k D_k / 2^N (m_k = 2 for k < N/2, 1 for k = N/2).

Modes
  echo  : per echo time n: S_ab = w Re<Z_a U^n x | U^n Z_b x>, W x = U^-n Z_a U^n x,
          g_j = w Re<x|Z_j W|x>  (-> G_j = sum_k g_j, H = sum_j G_j^2, floor),
          F_ab = w Re<Z_b W x | W Z_b x>.
          Time-major: phase n = each echo time in ascending order; the forward vectors (U^n x, U^n Z_b x) of every
          (sector, vector) are stored on disk between phases (forward reuse), so early times finish first.
  honly : g_j(n) = w Re<U^-n Z_a x | Z_j | U^-n x>  (two inverse passes; decomp_echo 'honly').
Post-processing (H unbiased over vector pairs if R >= 2; floor = sum_k m_k (1-2k/N)^2 tau_k(W_rest^2)) is copied
from decomp_echo.run (validated there to 1e-14 against dense traces).

Checkpointing: JSON state after every leg (forward advance, W x leg, each W Z_b x leg), forward/partial vectors in
per-(sector, vector) .npz files; all writes atomic (tmp + os.replace).  Re-running the same command resumes.
--budget-s stops cleanly (checkpoint kept) once the CPU time of this invocation exceeds it.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

import kernels as KR
from kernels import FE, SP

HERE = os.path.dirname(os.path.abspath(__file__))
DT = 2e-6


def _replace(src, dst, tries=40):
    """os.replace with retries (Windows: transient 'Access is denied' while a scanner holds the new file)."""
    for i in range(tries):
        try:
            os.replace(src, dst)
            return
        except PermissionError:
            if i == tries - 1:
                raise
            time.sleep(0.05 * (1 + i))


def atomic_json(obj, path):
    with open(path + ".tmp", "w") as f:
        json.dump(obj, f)
    _replace(path + ".tmp", path)


def atomic_npz(path, **arrs):
    tmp = path + ".tmp.npz"
    np.savez(tmp, **arrs)
    _replace(tmp, path)


def load_npz(path, dtype):
    with np.load(path) as z:
        return {k: (int(z[k]) if k == "pos" else np.array(z[k], dtype=dtype)) for k in z.files}


def draws(N, R, seed):
    rng = np.random.default_rng(seed + 7919 * N)
    out = {}
    for k in range(N // 2 + 1):
        Dk = math.comb(N, k)
        xs = []
        for _ in range(R):
            x = rng.standard_normal(Dk) + 1j * rng.standard_normal(Dk)
            xs.append(x / np.linalg.norm(x))
        out[k] = xs
    return out


def zsign(idx, q):
    return (1.0 - 2.0 * ((idx >> q) & 1)).astype(np.float64)


def gvec(idx, N, y):
    """sum_i z_j(i) y_i for all j (y real, float64)."""
    tot = float(y.sum())
    return np.array([tot - 2.0 * float(y[((idx >> j) & 1).astype(bool)].sum()) for j in range(N)])


def zz_offdiag_mean(N, k):
    M = N - 2 * k
    return (M * M - N) / (N * (N - 1.0))


def postprocess(N, R, g, Fres, T, bs, Cres=None, Mres=None):
    """g: dict k -> array (R, T, N) (weighted); Fres: dict k -> array (R, T, B) or None.  Copied from decomp_echo.
    Cres: dict k -> (R, T, B, N) weighted Re<Z_j x|Z_b W Z_b x>;  Mres: dict k -> (R, N, N) weighted <x|Z_i Z_j|x>.
    With them: direct single-vector estimate of R_ab = Tr[W' Z_b W' Z_b]/2^N, W' = W - sum_j G^_j Z_j (G^ from the
    same vector; the O(dG) term vanishes exactly because Tr[Z_j W_rest] = 0):
        R^ = F^ - sum_j G^_j^2 - sum_j G^_j C^_bj + G^' M^ G^ ,   X_direct = R^ - floor  (no H noise)."""
    ks = list(range(N // 2 + 1))
    garr = np.array([g[k] for k in ks])                 # (K, R, T, N)
    G_r = garr.sum(0)
    G = G_r.mean(0)
    if R >= 2:
        prs = [(i, j) for i in range(R) for j in range(i + 1, R)]
        H = np.mean([np.sum(G_r[i] * G_r[j], axis=1) for i, j in prs], axis=0)
    else:
        H = np.sum(G ** 2, axis=1)
    floor = np.zeros(T)
    for kk, k in enumerate(ks):
        Dk = math.comb(N, k)
        mult = 1.0 if 2 * k == N else 2.0
        tauI = Dk / float(1 << N)
        gk = garr[kk].mean(0) / mult
        e = zz_offdiag_mean(N, k)
        sumG = G.sum(1)
        zz = tauI * (e * (sumG ** 2 - np.sum(G ** 2, 1)) + np.sum(G ** 2, 1))
        tw = tauI - 2 * np.sum(G * gk, 1) + zz
        m = (N - 2 * k) / N
        floor += mult * m * m * tw
    out = dict(G=G.tolist(), H=H.tolist(), floor=floor.tolist(), sumG=G.sum(1).tolist())
    if Fres is not None:
        Farr = np.array([Fres[k] for k in ks]).sum(0)    # (R, T, B)
        F = Farr.mean(0)
        out["F"] = {str(b): F[:, bi].tolist() for bi, b in enumerate(bs)}
        out["X"] = {str(b): (F[:, bi] - H - floor).tolist() for bi, b in enumerate(bs)}
        out["F_r"] = Farr.tolist()
        if Cres is not None and Mres is not None:
            Carr = np.array([Cres[k] for k in ks]).sum(0)          # (R, T, B, N)
            Marr = np.array([Mres[k] for k in ks]).sum(0)          # (R, N, N)
            Rr = np.zeros((R, T, len(bs)))
            for r in range(R):
                Gr = G_r[r]                                        # (T, N)
                quad = np.einsum("ti,ij,tj->t", Gr, Marr[r], Gr)
                Rr[r] = (Farr[r] - np.sum(Gr ** 2, 1)[:, None] - np.einsum("tj,tbj->tb", Gr, Carr[r])
                         + quad[:, None])
            Rm = Rr.mean(0)
            out["Rdirect"] = {str(b): Rm[:, bi].tolist() for bi, b in enumerate(bs)}
            out["Xdirect"] = {str(b): (Rm[:, bi] - floor).tolist() for bi, b in enumerate(bs)}
            out["Xdirect_r"] = (Rr - floor[None, :, None]).tolist()
            out["M_trace_check"] = [float(np.trace(Marr[r])) for r in range(R)]     # -> N (sum_i <x|x> weights)
    if R >= 2:
        out["H_r"] = [np.sum(G_r[r] ** 2, 1).tolist() for r in range(R)]
    return out


class Ctx:
    def __init__(self, N, pairs, dtype):
        self.N = N; self.pairs = pairs; self.dtype = dtype
        self.pc = FE.popcounts(N)
        self.k = None; self.K = None; self.idx = None

    def sector(self, k):
        if self.k != k:
            self.K = None
            self.idx = np.nonzero(self.pc == k)[0]
            self.K = KR.ClipSectorKernel(self.N, self.idx, self.pairs, self.dtype)
            self.k = k
        return self.idx, self.K


def run(pdb, probe, N, mode, steps, R, dtype, seed, tag, budget_s=None, log=print, wall_s=None, max_phase=None):
    dm, bs, names, _ = FE.load_instance(pdb, probe, N)
    pairs = SP.pair_list(dm, DT)
    steps = sorted(steps)
    T = len(steps)
    base = os.path.join(HERE, "runs", tag)
    ck = base + ".ckpt.json"
    st = None
    if os.path.exists(ck):
        with open(ck) as f:
            st = json.load(f)
    st = st if st is not None else dict(
        pdb=pdb, probe=probe, N=N, mode=mode, steps=steps, R=R, dtype=np.dtype(dtype).name, seed=seed, bs=bs,
        names_bs=names, g={}, F={}, S={}, C={}, M={}, fpos={}, pe=None, cpu_s=0.0, vector_steps=0)
    X0 = draws(N, R, seed)
    ctx = Ctx(N, pairs, dtype)
    c0 = time.process_time()
    w0 = time.time()
    tick = [time.process_time()]
    partial = False

    def save():
        st["cpu_s"] += time.process_time() - tick[0]
        tick[0] = time.process_time()
        atomic_json(st, ck)

    def over():
        return ((budget_s is not None and time.process_time() - c0 > budget_s)
                or (wall_s is not None and time.time() - w0 > wall_s))

    st.setdefault("C", {}); st.setdefault("M", {})
    ks = list(range(N // 2 + 1))
    if mode == "honly":
        nmax = max(steps)
        for k in ks:
            for r in range(R):
                key = f"{k}_{r}"
                if key in st["g"]:
                    continue
                if over():
                    partial = True; break
                idx, K = ctx.sector(k)
                Dk = len(idx)
                w = (1.0 if 2 * k == N else 2.0) * Dk / float(1 << N)
                za = zsign(idx, 0)
                x = X0[k][r].astype(dtype)
                phi = x.copy(); chi = (za * x).astype(dtype)
                gl = []
                for n in range(1, nmax + 1):
                    K.step(phi, inverse=True); K.step(chi, inverse=True)
                    st["vector_steps"] += 2
                    if n in steps:
                        y = np.real(np.conj(chi.astype(np.complex128)) * phi.astype(np.complex128))
                        gl.append((w * gvec(idx, N, y)).tolist())
                st["g"][key] = gl
                save()
                log(json.dumps(dict(k=k, r=r, Dk=Dk, cpu=round(st["cpu_s"], 1))))
            if partial:
                break
    else:
        for n in steps:
            if max_phase is not None and n > max_phase:
                break
            for k in ks:
                for r in range(R):
                    key = f"{n}_{k}_{r}"
                    if key in st["F"] and len(st["F"][key]) == len(bs):
                        continue
                    if over():
                        partial = True; break
                    idx, K = ctx.sector(k)
                    Dk = len(idx)
                    w = (1.0 if 2 * k == N else 2.0) * Dk / float(1 << N)
                    za = zsign(idx, 0)
                    zb = {b: zsign(idx, b) for b in bs}
                    fkey = f"{k}_{r}"
                    fpath = f"{base}.fwd_{fkey}.npz"
                    if os.path.exists(fpath):                    # the forward position lives in the npz itself
                        vec = load_npz(fpath, dtype)
                        pos = vec.pop("pos")
                    else:
                        x = X0[k][r].astype(dtype)
                        vec = dict(phi=x.copy(), **{f"chi{b}": (zb[b] * x).astype(dtype) for b in bs})
                        pos = 0
                    if pos < n:                                  # forward advance to n (reused by later phases)
                        for _ in range(n - pos):
                            K.step(vec["phi"])
                            for b in bs:
                                K.step(vec[f"chi{b}"])
                        st["vector_steps"] += (n - pos) * (1 + len(bs))
                        atomic_npz(fpath, pos=np.array(n), **vec)
                        st["fpos"][fkey] = n
                        save()
                    assert pos <= n, (fkey, pos, n)
                    st["fpos"][fkey] = n
                    ppath = f"{base}.pe_{k}_{r}.npz"                # overwritten each phase; st['pe'] says which
                    if st["pe"] != key:                          # W x leg
                        u = (za * vec["phi"]).astype(dtype)
                        st["S"][key] = {str(b): w * float(np.real(np.vdot(u, vec[f"chi{b}"]))) for b in bs}
                        for _ in range(n):
                            K.step(u, inverse=True)
                        st["vector_steps"] += n
                        x = X0[k][r]
                        y = np.real(np.conj(x) * u.astype(np.complex128))
                        st["g"][key] = (w * gvec(idx, N, y)).tolist()
                        if fkey not in st["M"]:
                            pz = np.abs(x) ** 2
                            Zs = np.stack([zsign(idx, q) for q in range(N)])
                            st["M"][fkey] = (w * ((Zs * pz[None, :]) @ Zs.T)).tolist()
                            del Zs, pz
                        atomic_npz(ppath, **{f"zub{b}": (zb[b] * u).astype(dtype) for b in bs})
                        st["pe"] = key
                        st["F"][key] = {}
                        save()
                        del u
                    zub = load_npz(ppath, dtype)
                    for b in bs:                                 # W Z_b x legs
                        if str(b) in st["F"][key]:
                            continue
                        vb = (za * vec[f"chi{b}"]).astype(dtype)
                        for _ in range(n):
                            K.step(vb, inverse=True)
                        st["vector_steps"] += n
                        st["F"][key][str(b)] = w * float(np.real(np.vdot(zub[f"zub{b}"], vb)))
                        yb = np.real(np.conj(X0[k][r]) * (zb[b] * vb.astype(np.complex128)))
                        st["C"].setdefault(key, {})[str(b)] = (w * gvec(idx, N, yb)).tolist()
                        save()
                        del vb
                        if over() and len(st["F"][key]) < len(bs):
                            partial = True; break
                    if partial:
                        break
                    st["pe"] = None
                    save()
                    del zub, vec
                    log(json.dumps(dict(n=n, k=k, r=r, Dk=Dk, cpu=round(st["cpu_s"], 1),
                                        vs=st["vector_steps"])))
                if partial:
                    break
            if partial:
                break
    save()
    # assemble whatever phases are complete
    res = dict(pdb=pdb, probe=probe, N=N, mode=mode, R=R, dtype=np.dtype(dtype).name, seed=seed, bs=bs,
               names_bs=names, steps=steps, cpu_s=st["cpu_s"], vector_steps=st["vector_steps"])
    try:
        import psutil
        res["peak_rss_GB"] = psutil.Process().memory_info().peak_wset / 1e9
    except Exception:
        pass
    if mode == "honly":
        done = all(f"{k}_{r}" in st["g"] for k in ks for r in range(R))
        res["complete"] = done
        if done:
            g = {k: np.array([st["g"][f"{k}_{r}"] for r in range(R)]) for k in ks}
            res.update(times_us=[n * 2.0 for n in steps], **postprocess(N, R, g, None, T, bs))
    else:
        ok = [n for n in steps if all(f"{n}_{k}_{r}" in st["F"] and len(st["F"][f"{n}_{k}_{r}"]) == len(bs)
                                      for k in ks for r in range(R))]
        res["steps_done"] = ok
        res["complete"] = len(ok) == T
        if ok:
            g = {k: np.array([[st["g"][f"{n}_{k}_{r}"] for n in ok] for r in range(R)]) for k in ks}
            Fr = {k: np.array([[[st["F"][f"{n}_{k}_{r}"][str(b)] for b in bs] for n in ok] for r in range(R)])
                  for k in ks}
            haveC = all(f"{n}_{k}_{r}" in st["C"] and len(st["C"][f"{n}_{k}_{r}"]) == len(bs)
                        for n in ok for k in ks for r in range(R)) and all(f"{k}_{r}" in st["M"] for k in ks for r in range(R))
            Cr = Mr = None
            if haveC:
                Cr = {k: np.array([[[st["C"][f"{n}_{k}_{r}"][str(b)] for b in bs] for n in ok] for r in range(R)])
                      for k in ks}
                Mr = {k: np.array([st["M"][f"{k}_{r}"] for r in range(R)]) for k in ks}
            res.update(times_us=[n * 2.0 for n in ok], **postprocess(N, R, g, Fr, len(ok), bs, Cr, Mr))
            res["S"] = {str(b): [float(np.mean([sum(st["S"][f"{n}_{k}_{r}"][str(b)] for k in ks) for r in range(R)]))
                                 for n in ok] for b in bs}
    res["partial"] = partial or not res["complete"]
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--mode", default="echo", choices=["echo", "honly"])
    ap.add_argument("--steps", type=int, nargs="+", default=[20, 40, 60])
    ap.add_argument("--R", type=int, default=1)
    ap.add_argument("--dtype", default="complex64")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--budget-s", type=float, default=None, help="CPU seconds for this invocation")
    ap.add_argument("--wall-s", type=float, default=None, help="wall seconds for this invocation")
    ap.add_argument("--max-phase", type=int, default=None, help="echo mode: do not start phases (steps) beyond this")
    a = ap.parse_args()
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    tag = (f"{a.pdb}_p{a.probe}_N{a.N}_{a.mode}_R{a.R}_{a.dtype}_s{a.seed}_t{'-'.join(map(str, sorted(a.steps)))}")
    out = os.path.join(HERE, "runs", tag + ".json")
    res = run(a.pdb, a.probe, a.N, a.mode, a.steps, a.R, np.dtype(a.dtype), a.seed, tag, a.budget_s, wall_s=a.wall_s,
              max_phase=a.max_phase)
    atomic_json(res, out)          # rewritten after every invocation; 'complete'/'steps_done' say what is final
    print(json.dumps(dict(out=os.path.basename(out), complete=res["complete"], steps_done=res.get("steps_done"),
                          cpu_s=round(res["cpu_s"], 1), vs=res["vector_steps"],
                          rss=round(res.get("peak_rss_GB", 0), 3))))


if __name__ == "__main__":
    main()
