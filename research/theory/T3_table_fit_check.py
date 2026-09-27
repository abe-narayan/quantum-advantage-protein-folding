"""T3 small checks on the real A80 tables (esmprior_v1 predictions stored in data/instruments/ladder/<crop>.npz).

(1) Piecewise-cubic segment count: max error of a per-segment least-squares cubic for each pair potential
    f_ij(d) = -log(sum_k P_ijk S_k(d) + 1e-6) over all pairs |i-j| >= 3.
      mode "s"  : v1 grid, uniform in s = d^2 over [2.5^2, 43.5^2] A^2 (h = 1.8418 A^2 at g = 1024; NOT bit-aligned,
                  s = 16 A^2 is NOT a knot -- review objection, kept for the record);
      mode "s2" : v2 grid, bit-aligned, s in [0, 2048) A^2 with h = 2048/g A^2 (h = 2 A^2 at g = 1024), so s = 16 A^2
                  IS a knot and the segment index / local coordinate are bits of s; the steric term w_s relu(4 - d)^2
                  is FOLDED INTO the CA spline, whose tabulated function is clamped at d = 2 A (s = 4, also a knot);
                  errors are reported over segments with s >= 6 A^2 (d >= 2.45 A) for comparability with mode "s".
                  The energy-level checks (4)-(5) add a 64-segment sub-grid of h = 1/16 A^2 on s < 4 A^2 (class Spline),
                  needed for the CB channel's sqrt(s) cusp at s = 0;
      mode "d"  : uniform in d over [2.5, 43.5] A.
(2) Global shared low-rank basis: max reconstruction error of f_ij on a 0.05 A grid from the top-R SVD components.
(3) --timing: quick single-core timing of the classical energy(+gradient) (NOT the G1 measurement).
(4) --energy-error: pair-energy error (CA + CB + sterics) on PILOT posterior samples of
      (a) the v2 float spline (sterics folded) vs the smooth function it approximates, and
      (b) the classical 0.05 A grid table (what the classical sampler uses) vs the same smooth function.
(5) --fixed-point: FIXED-POINT EMULATION of the whole quantum pair-energy pipeline (review objection 2): lattice angles
    (b = 10 bits), sequential frame build F_k = F_{k-1} Rx(tau_k) Rz(pi - theta_k) with every product quantised,
    coordinates in Angstrom (bond increment 3.8*col0(F_k) as a constant multiply), virtual CB = X_i + F_{i+1} v(theta),
    coordinate differences, saturating squared distance s, v2 spline segment/local coordinate taken from the bits of s,
    quantised spline coefficients, fixed-point Horner.  Formats (sign bit included in the b_w bits):
      frame entries / trig / v(theta)  : 1 sign + 1 integer + (b_w + g - 2) fractional bits
      coordinates (A)                  : 1 sign + IX integer + (b_w + g - 1 - IX) fractional, IX = ceil(log2(3.8(L-1)+2));
                                         rounded to b_w bits (drop the g guard bits) before differencing
      s = |dX|^2 (A^2), unsigned       : 11 integer + (b_w - 11) fractional; |dX_c| >= 64 A or s >= 2048 saturates to
                                         the top of the grid (d > 45.25 A, where every A80 pair potential is flat)
      spline local coordinate u        : low bits of s ((s/2) mod 1), exact
      coefficients, Horner accumulator : 1 sign + 7 integer + (b_w - 8) fractional bits   (b_c = b_w)
    Rounding convention of every product: 'round' (to nearest) or 'trunc' (floor, two's complement truncation).
    Reported per L: sd / max over samples of dE = E_fixed - E_ref (E_ref = float64 smooth function at the SAME lattice
    angles), and of the move error ddE = dE(x') - dE(x) for single-angle moves of one lattice unit.
Run:  python research/theory/T3_table_fit_check.py [crop ...] [--timing] [--energy-error] [--fixed-point] [--no-fit]
      [--s2-only]
      (fit: 1-3 min/crop; --fixed-point: ~2-6 min in total on one core)
"""
from __future__ import annotations

import math
import os
import sys
import time

import numpy as np
from scipy.special import ndtr

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EDGES = np.concatenate([np.arange(4.0, 20.0 + 1e-9, 1.0), np.arange(22.0, 40.0 + 1e-9, 2.0)])   # esmprior_v1 bins
LO = np.concatenate([[0.0], EDGES])
HI = np.concatenate([EDGES, [np.inf]])
SIG, EPS, WS, R0 = 0.5, 1e-6, 10.0, 4.0                                                          # energy.DEFAULT_W
BOND = 3.80
S2_LO, S2_SPAN = 0.0, 2048.0          # v2 bit-aligned grid: s in [0, 2048) A^2; CA(+sterics) clamped at d = 2 A
D_CLAMP_CA = 2.0
PILOT = (("5O37A_45_T1_s0", "5O37A_45"), ("3GAHA_60_T1_s0", "3GAHA_60"), ("5O37A_100_T1_s0", "5O37A_100"),
         ("4LPQA_120_T1_s0", "4LPQA_120"), ("5O37A_150_T1_s0", "5O37A_150"))


def f_pair(P, d, ster):
    """P (n,28), d (m,) -> (n,m): the smooth function the classical 0.05 A table samples (+ sterics if ster)."""
    S = ndtr((HI[None, :] - d[:, None]) / SIG) - ndtr((LO[None, :] - d[:, None]) / SIG)
    S[:, -1] = ndtr((d - LO[-1]) / SIG)
    f = -np.log(P @ S.T + EPS)
    if ster:
        f = f + WS * np.maximum(R0 - d, 0.0) ** 2
    return f


def seg_fit_err(P, ster, g, mode, dlo=2.5, dhi=43.5, npts=24, deg=3):
    if mode == "s":
        b = np.linspace(dlo ** 2, dhi ** 2, g + 1)
    elif mode == "s2":
        b = S2_LO + np.arange(g + 1) * (S2_SPAN / g)
    else:
        b = np.linspace(dlo, dhi, g + 1)
    emax = np.zeros(len(P))
    u = np.linspace(-1, 1, npts)
    V = np.vander(u, deg + 1)
    for k in range(g):
        if mode == "s2" and b[k + 1] <= 6.0 + 1e-9:
            continue                                     # d < 2.45 A: not reported (see docstring)
        x = 0.5 * (b[k] + b[k + 1]) + 0.5 * (b[k + 1] - b[k]) * u
        d = np.sqrt(x) if mode in ("s", "s2") else x
        if mode == "s2" and ster:
            d = np.maximum(d, D_CLAMP_CA)
        F = f_pair(P, d, ster)
        C, *_ = np.linalg.lstsq(V, F.T, rcond=None)
        emax = np.maximum(emax, np.abs(V @ C - F.T).max(0))
    return emax


def fit_checks(crop, s2_only=False):
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", crop + ".npz"))
    L = len(str(z["seq"]))
    I, J = np.triu_indices(L, k=3)
    for name, key, ster in (("CA", "prob", False), ("CB", "prob_cb", False), ("CA+sterics", "prob", True)):
        P = np.asarray(z[key], np.float64)[I, J]
        for mode, gs in (("s", (512, 1024, 2048)), ("s2", (512, 1024, 2048)), ("d", (64, 128))):
            if (ster and mode == "d") or (s2_only and mode != "s2"):
                continue
            cells = []
            for g in gs:
                e = seg_fit_err(P, ster, g, mode)
                cells.append(f"g={g}: max {e.max():.1e} p99 {np.quantile(e, 0.99):.1e} med {np.median(e):.1e}")
            print(f"{crop} L={L} {name} cubic uniform-{mode}: " + " | ".join(cells), flush=True)
        if ster or s2_only:
            continue
        d = np.arange(2.5, 43.5 + 1e-9, 0.05)
        F = f_pair(P, d, False)
        mu = F.mean(0)
        U, s, Vt = np.linalg.svd(F - mu, full_matrices=False)
        cells = []
        for R in (4, 8, 16, 28, 40, 64):
            err = np.abs(mu + (U[:, :R] * s[:R]) @ Vt[:R] - F).max(1)
            cells.append(f"R={R}: max {err.max():.1e} p99 {np.quantile(err, 0.99):.1e}")
        print(f"{crop} L={L} {name} shared rank-R basis: " + " | ".join(cells), flush=True)


def f_pair_own(P, d):
    """P (n,28), d (..., n): each pair's smooth potential at its own distance -> (..., n)."""
    S = ndtr((HI - d[..., None]) / SIG) - ndtr((LO - d[..., None]) / SIG)
    S[..., -1] = ndtr((d - LO[-1]) / SIG)
    return -np.log((P * S).sum(-1) + EPS)


# ============================================================================ v2 spline (bit-aligned, sterics folded)
class Spline:
    """Per-pair cubic in the local coordinate u in [0,1) of segment k of the v2 grid: s in [0, 2048) A^2 with g
    coarse segments (h = 2048/g A^2) plus, if fine, a sub-grid of NF = 64 segments of h_f = 1/16 A^2 on s < 4 A^2
    (d < 2 A; needed for the CB channel, whose potential has a sqrt(s) cusp at s = 0 from the Phi(-d/sigma) edge of
    bin 0).  Segment k and u are bits of s in both regions.  Coefficients are fitted lazily for the (pair, segment)
    combinations actually used."""
    NF, HF = 64, 1.0 / 16

    def __init__(self, P, ster, g=1024, npts=24, fine=True):
        self.P, self.ster, self.g, self.h, self.fine = P, ster, g, S2_SPAN / g, fine
        self.G = g + (self.NF if fine else 0)
        self.u = np.linspace(0.0, 1.0, npts)
        self.Vp = np.linalg.pinv(np.vander(self.u, 4))        # (4, npts): c3, c2, c1, c0
        self.keys = np.zeros(0, np.int64)
        self.C = np.zeros((0, 4))

    def _fit(self, keys):
        out = np.empty((len(keys), 4))
        for a in range(0, len(keys), 20000):
            kk = keys[a:a + 20000]
            p, k = kk // self.G, kk % self.G
            lo = np.where(k < self.g, S2_LO + self.h * k, self.HF * (k - self.g))
            hh = np.where(k < self.g, self.h, self.HF)
            x = lo[:, None] + hh[:, None] * self.u[None, :]                      # (n, npts)
            d = np.sqrt(x)
            if self.ster:
                d = np.maximum(d, D_CLAMP_CA)
            f = f_pair_own(self.P[p][:, None, :], d)
            if self.ster:
                f = f + WS * np.maximum(R0 - d, 0.0) ** 2
            out[a:a + 20000] = f @ self.Vp.T
        return out

    def coef(self, pidx, seg):
        keys = pidx.astype(np.int64) * self.G + seg
        uk = np.unique(keys)
        new = np.setdiff1d(uk, self.keys, assume_unique=True)
        if len(new):
            allk = np.concatenate([self.keys, new])
            allC = np.concatenate([self.C, self._fit(new)])
            o = np.argsort(allk)
            self.keys, self.C = allk[o], allC[o]
        return self.C[np.searchsorted(self.keys, keys)]

    def seg_u(self, s):
        s = np.clip(s, S2_LO, S2_LO + S2_SPAN - 1e-9)
        t = (s - S2_LO) / self.h
        k = np.floor(t).astype(np.int64)
        u = t - k
        if self.fine:
            m = s < self.NF * self.HF
            tf = s / self.HF
            kf = np.floor(tf).astype(np.int64)
            k = np.where(m, self.g + kf, k)
            u = np.where(m, tf - kf, u)
        return k, u

    def eval_float(self, s):
        """s (N, npairs) float -> spline values (N, npairs), unquantised coefficients."""
        k, u = self.seg_u(s)
        C = self.coef(np.broadcast_to(np.arange(s.shape[1]), s.shape).ravel(), k.ravel()).reshape(*s.shape, 4)
        return ((C[..., 0] * u + C[..., 1]) * u + C[..., 2]) * u + C[..., 3]


# ============================================================================ builders
def lattice(x, L, b=10):
    step = 2 * math.pi / 2 ** b
    return np.round(x / step) * step


def angles_ak(x, L):
    th, ta = x[:, :L - 2], x[:, L - 2:]
    N = len(x)
    a = np.concatenate([np.zeros((N, 1)), math.pi - th], 1)       # a_k, k = 1..L-1
    t = np.concatenate([np.zeros((N, 2)), ta], 1)                 # t_k
    return a, t


def cb_offset(a):
    """v(a) in the frame F_{i+1}: CB_i = X_i + F_{i+1} v(a_{i+1}) (derived from energy.virtual_cb_t)."""
    ca, sa = np.cos(a), np.sin(a)
    u1 = np.stack([ca, -sa, np.zeros_like(a)], -1)
    u2 = np.stack([np.ones_like(a), np.zeros_like(a), np.zeros_like(a)], -1)
    nz = lambda v: v / np.maximum(np.linalg.norm(v, axis=-1, keepdims=True), 1e-9)
    m, n, t = nz(u1 - u2), nz(np.cross(u1, u2)), nz(u1 + u2)
    return 1.0977 * m - 0.9601 * n + 0.1616 * t


def build(x, L, fmt=None):
    """Sequential frame build.  fmt None -> float64; else dict(bw, g, mode) -> fixed-point emulation.
    Returns X (N, L, 3), CB (N, L, 3) in Angstrom."""
    a, t = angles_ak(x, L)
    N = len(x)
    if fmt is None:
        q = qF = qX = lambda v: v
    else:
        bw, g, mode = fmt["bw"], fmt["g"], fmt["mode"]
        rnd = np.round if mode == "round" else np.floor
        IX = math.ceil(math.log2(BOND * (L - 1) + 2))
        fF, fX = bw + g - 2, bw + g - 1 - IX
        q = lambda v, f: rnd(v * 2.0 ** f) / 2.0 ** f
        qF = lambda v: q(v, fF)
        qX = lambda v: q(v, fX)
        tab = lambda v: np.round(v * 2.0 ** fF) / 2.0 ** fF           # classical table data: round to nearest
    ca_, sa_, ct, st = np.cos(a), np.sin(a), np.cos(t), np.sin(t)
    v = cb_offset(a)                                                   # (N, L-1, 3)
    if fmt is not None:
        ca_, sa_, ct, st, v = tab(ca_), tab(sa_), tab(ct), tab(st), tab(v)
    F = np.broadcast_to(np.eye(3), (N, 3, 3)).copy()                  # columns f0, f1, f2
    X = np.zeros((N, L, 3))
    Fs = np.zeros((N, L, 3, 3))
    Fs[:, 0] = F
    for k in range(1, L):
        c_t, s_t, c_a, s_a = ct[:, k - 1, None], st[:, k - 1, None], ca_[:, k - 1, None], sa_[:, k - 1, None]
        f0, f1, f2 = F[:, :, 0], F[:, :, 1], F[:, :, 2]
        m1 = qF(c_t * f1) + qF(s_t * f2)                               # F Rx(t): col1
        m2 = qF(c_t * f2) - qF(s_t * f1)                               #          col2
        n0 = qF(c_a * f0) + qF(s_a * m1)                               # (F Rx) Rz(a): col0
        n1 = qF(c_a * m1) - qF(s_a * f0)                               #               col1
        F = np.stack([n0, n1, m2], -1)
        Fs[:, k] = F
        X[:, k] = X[:, k - 1] + qX(BOND * n0)
    CB = X.copy()
    for i in range(1, L - 1):                                          # CB_i = X_i + F_{i+1} v(a_{i+1})
        vv = v[:, i]                                                   # a index i  <->  a_{i+1}
        Fi = Fs[:, i + 1]
        CB[:, i] = X[:, i] + sum(qX(Fi[:, :, j] * vv[:, j, None]) for j in range(3))
    if fmt is not None and fmt["g"]:
        IX = math.ceil(math.log2(BOND * (L - 1) + 2))
        fXo = fmt["bw"] - 1 - IX
        X, CB = np.round(X * 2.0 ** fXo) / 2.0 ** fXo, np.round(CB * 2.0 ** fXo) / 2.0 ** fXo
    return X, CB


def sqdist(A, I, J, fmt=None):
    D = A[:, I] - A[:, J]
    if fmt is None:
        return (D * D).sum(-1)
    fs = fmt["bw"] - 11
    rnd = np.round if fmt["mode"] == "round" else np.floor
    sat = (np.abs(D) >= 64.0).any(-1)
    s = (rnd(D * D * 2.0 ** fs) / 2.0 ** fs).sum(-1)
    top = S2_LO + S2_SPAN - 2.0 ** -fs
    return np.where(sat | (s > top), top, s)


def spline_fixed(sp, s, fmt):
    """Fixed-point Horner with quantised coefficients; u = low bits of s (exact)."""
    fE = fmt["bw"] - 8
    rnd = np.round if fmt["mode"] == "round" else np.floor
    k, u = sp.seg_u(s)
    C = sp.coef(np.broadcast_to(np.arange(s.shape[1]), s.shape).ravel(), k.ravel()).reshape(*s.shape, 4)
    C = np.round(C * 2.0 ** fE) / 2.0 ** fE                        # classical coefficient data
    qE = lambda v: rnd(v * 2.0 ** fE) / 2.0 ** fE
    acc = C[..., 0]
    for j in (1, 2, 3):
        acc = qE(acc * u) + C[..., j]
    return acc


def load_pilot(tag, crop, nmax):
    fs = os.path.join(ROOT, "research", "results", "RAW", "g1_pilot", tag + ".npz")
    if not os.path.exists(fs):
        return None
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", crop + ".npz"))
    L = len(str(z["seq"]))
    X = np.load(fs)["samples"]
    if len(X) > nmax:
        X = X[np.linspace(0, len(X) - 1, nmax).astype(int)]
    return z, L, X


def check_build_against_code():
    """The float sequential build and the CB offset formula reproduce energy.build_ca / virtual_cb_t."""
    import torch
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from qapf.protein import energy as EN
    z, L, X = load_pilot(*PILOT[0], 4)
    Xa, CBa = build(X, L)
    with torch.no_grad():
        Xb = EN.build_ca(torch.as_tensor(X[:, :L - 2]), torch.as_tensor(X[:, L - 2:])).numpy()
        CBb = EN.virtual_cb_t(torch.as_tensor(Xb)).numpy()
    print(f"build check: max|X - build_ca| = {np.abs(Xa - Xb).max():.1e} A; max|CB - virtual_cb_t| = "
          f"{np.abs(CBa - CBb).max():.1e} A", flush=True)


def energy_error(g=1024, nmax=60, variants=((512, True), (1024, False), (1024, True), (2048, True))):
    """(4) Pair-energy error on PILOT posterior samples: v2 spline (sterics folded) vs the smooth function, and the
    classical 0.05 A grid table vs the smooth function."""
    import torch
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from qapf.protein import energy as EN
    for tag, crop in PILOT:
        r = load_pilot(tag, crop, nmax)
        if r is None:
            continue
        z, L, X = r
        en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
        with torch.no_grad():
            T = en.terms(torch.as_tensor(X))
            e_table = (T["ca"] + T["cb"] + en.w["w_s"] * T["st"]).numpy()
        Xc, CB = build(X, L)
        I, J = np.triu_indices(L, k=3)
        ref = np.zeros(len(X))
        cells = []
        spl = {gg: np.zeros(len(X)) for gg in variants}
        for key, A, ster in (("prob", Xc, True), ("prob_cb", CB, False)):
            P = np.asarray(z[key], np.float64)[I, J]
            s = sqdist(A, I, J)
            d = np.sqrt(s)
            ref += f_pair_own(P, d).sum(1) + (WS * np.maximum(R0 - d, 0.0) ** 2).sum(1) * ster
            for gg in spl:
                spl[gg] += Spline(P, ster, gg[0], fine=gg[1]).eval_float(s).sum(1)
        for gg, v in spl.items():
            dd = v - ref
            cells.append(f"v2 spline g={gg[0]}{'+64' if gg[1] else ''}: mean {dd.mean():+.1e} sd {dd.std():.1e} "
                         f"max|.| {np.abs(dd).max():.1e}")
        d2 = e_table - ref
        print(f"{crop}: {len(X)} PILOT samples, E_pair ~ {ref.mean():.0f} nats | " + " | ".join(cells) +
              f" | classical 0.05 A table: mean {d2.mean():+.1e} sd {d2.std():.1e} max|.| {np.abs(d2).max():.1e}",
              flush=True)


def fixed_point(nmax=60, bws=(16, 20, 22, 24, 26, 28), seed=0,
                configs=(("round", 0), ("round", 4), ("trunc", 0)), gseg=1024, crops=None):
    """(5) Fixed-point emulation of the quantum pair-energy pipeline on PILOT samples (see module docstring)."""
    rng = np.random.default_rng(seed)
    for tag, crop in PILOT:
        if crops and crop not in crops:
            continue
        r = load_pilot(tag, crop, nmax)
        if r is None:
            continue
        z, L, X0 = r
        x = lattice(X0, L)
        # single-angle move of one lattice unit on a random angle (for the move error ddE)
        xm = x.copy()
        ai = rng.integers(0, 2 * L - 5, len(x))
        xm[np.arange(len(x)), ai] += rng.choice((-1.0, 1.0), len(x)) * 2 * math.pi / 1024
        I, J = np.triu_indices(L, k=3)
        chans = []
        for key, ster in (("prob", True), ("prob_cb", False)):
            P = np.asarray(z[key], np.float64)[I, J]
            chans.append((Spline(P, ster, gseg), P, ster))

        def e_ref(xx):
            A = build(xx, L)
            tot = np.zeros(len(xx))
            for (sp, P, ster), Ak in zip(chans, A):
                d = np.sqrt(sqdist(Ak, I, J))
                tot += f_pair_own(P, d).sum(1) + (WS * np.maximum(R0 - d, 0.0) ** 2).sum(1) * ster
            return tot

        def e_fix(xx, fmt):
            A = build(xx, L, fmt)
            tot = np.zeros(len(xx))
            geo = np.zeros(len(xx))
            for (sp, P, ster), Ak in zip(chans, A):
                s = sqdist(Ak, I, J, fmt)
                tot += spline_fixed(sp, s, fmt).sum(1)
                d = np.sqrt(s)
                geo += f_pair_own(P, d).sum(1) + (WS * np.maximum(R0 - d, 0.0) ** 2).sum(1) * ster
            return tot, geo

        E0, E0m = e_ref(x), e_ref(xm)
        print(f"\n{crop} (L={L}, {len(x)} PILOT samples on the b=10 lattice; E_pair ~ {E0.mean():.0f} nats; "
              f"|dE_move| median {np.median(np.abs(E0m - E0)):.2g} nats)", flush=True)
        print("| b_w | guard | rounding | geometry-only sd | full pipeline: mean | sd | max abs | move error ddE: sd "
              "| max abs |")
        print("|---|---|---|---|---|---|---|---|---|")
        for mode, g in configs:
                for bw in bws:
                    fmt = dict(bw=bw, g=g, mode=mode)
                    E, G = e_fix(x, fmt)
                    Em, _ = e_fix(xm, fmt)
                    dE, dG = E - E0, G - E0
                    ddE = (Em - E0m) - dE
                    print(f"| {bw} | {g} | {mode} | {dG.std():.1e} | {dE.mean():+.1e} | {dE.std():.1e} | "
                          f"{np.abs(dE).max():.1e} | {ddE.std():.1e} | {np.abs(ddE).max():.1e} |", flush=True)


def timing():
    os.environ["QAPF_TORCH_THREADS"] = "1"
    sys.path.insert(0, os.path.join(ROOT, "src"))
    from qapf.protein import energy as EN
    rng = np.random.default_rng(0)
    for L in (30, 45, 60, 80, 100, 120, 150):
        z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", f"2AB0A_{L}.npz"))
        en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
        th, ta = EN.angles_of(z["ca"])
        x0 = np.concatenate([th, ta])[None]
        res = {}
        for B in (1, 64):
            x = x0 + 0.05 * rng.standard_normal((B, x0.shape[1]))
            en(x); en(x)
            n = max(3, int(200 / B))
            t = time.perf_counter()
            for _ in range(n):
                en(x)
            res[B] = (time.perf_counter() - t) / (n * B) * 1e3
        print(f"L={L}: energy+gradient per structure  batch1 {res[1]:.3f} ms  batch64 {res[64]:.3f} ms", flush=True)


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if "--timing" in sys.argv:
        timing()
    if "--energy-error" in sys.argv:
        check_build_against_code()
        energy_error()
    if "--fixed-point" in sys.argv:
        fixed_point()
    if "--no-fit" not in sys.argv:
        for c in (args or ["2AB0A_150"]):
            fit_checks(c, s2_only="--s2-only" in sys.argv)
