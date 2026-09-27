"""Vendored copy of the predecessor's A80 learned folding energy + batched L-BFGS decoder (S33 lane D_decoder).

PROVENANCE: C:/Users/abena/cvar-vqe-protein-folding-v3/s33/EXPERIMENTS/D_decoder_lib.py (repo pinned 3d5b2d25),
lines for constants, soft tables, builder, Energy, lbfgs, relax copied verbatim; only imports changed
(esmprior -> qapf.protein.esmprior_v1).  Registers/VQE code NOT copied (killed family, DNR-01..DNR-08).

ENERGY (native-free): E(x) = w_ca sum_{|i-j|>=3} -log p~_ij^CA(d_ij) + w_cb sum -log p~_ij^CB(d^cb_ij)
    + w_tt sum_i -log P~_i(theta_i, tau_i) + w_s sum relu(r0-d_ij)^2 + w_w wall(theta);  x = (theta (L-2), tau (L-3)) rad.
"""
from __future__ import annotations

import math
import os

import numpy as np

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import torch  # noqa: E402

torch.set_num_threads(int(os.environ.get("QAPF_TORCH_THREADS", "1")))

from qapf.protein import esmprior_v1 as EP  # noqa: E402

BOND = 3.80
DEG = math.pi / 180.0
GRID_H = 0.05
GRID_MAX = 50.0
EDGES_CA = np.concatenate([[0.0], EP.EDGES, [np.inf]])     # 29 edges -> 28 bins
TH_LO = np.concatenate([[0.0], EP.TH_EDGES])                # 9 theta bins (deg)
TH_HI = np.concatenate([EP.TH_EDGES, [180.0]])
TA_C = EP.TA_CENTRES                                        # 24 tau centres (deg), width 15
THETA_LAST = 110.0                                          # theta_{L-2}: not predicted by the head

DEFAULT_W = dict(w_ca=1.0, w_cb=1.0, w_tt=1.0, w_s=10.0, r0=4.0, w_w=0.01, sigma=0.5, sig_th=4.0, sig_ta=6.0,
                 min_sep=3)


# ============================================================================ soft-bin tables
def _Phi(x):
    from scipy.special import ndtr
    return ndtr(x)


def soft_table(P, sigma=0.5, eps=1e-6):
    """P (np, 28) bin probabilities -> (np, G) table of -log p~(d) on the grid 0..GRID_MAX step GRID_H."""
    g = np.arange(0.0, GRID_MAX + GRID_H / 2, GRID_H)
    lo, hi = EDGES_CA[:-1], EDGES_CA[1:]
    S = _Phi((hi[None, :] - g[:, None]) / sigma) - _Phi((lo[None, :] - g[:, None]) / sigma)   # (G, 28)
    S = np.where(np.isfinite(S), S, 0.0)
    S[:, -1] = _Phi((g - lo[-1]) / sigma)
    p = np.asarray(P, np.float64) @ S.T                                                          # (np, G)
    return -np.log(p + eps)


def tt_soft_weights(th_deg, ta_deg, sig_th=4.0, sig_ta=6.0):
    """torch: soft memberships (..., 9) for theta and (..., 24) for tau (periodic)."""
    thlo = torch.as_tensor(TH_LO); thhi = torch.as_tensor(TH_HI)
    nd = torch.special.ndtr
    st = nd((thhi - th_deg[..., None]) / sig_th) - nd((thlo - th_deg[..., None]) / sig_th)
    st = torch.cat([nd((thhi[0] - th_deg) / sig_th)[..., None], st[..., 1:-1],
                    nd((th_deg - thlo[-1]) / sig_th)[..., None]], -1)       # open lower / upper bins
    c = torch.as_tensor(TA_C)
    dl = torch.remainder(ta_deg[..., None] - c + 180.0, 360.0) - 180.0
    sa = nd((7.5 - dl) / sig_ta) - nd((-7.5 - dl) / sig_ta)
    return st, sa


# ============================================================================ builder
def build_ca(th, ta, b=BOND):
    """th (B, L-2) rad, ta (B, L-3) rad -> CA (B, L, 3), torch, differentiable.  Parallel-prefix transform scan."""
    B, Lm2 = th.shape
    L = Lm2 + 2
    dt = th.dtype
    # a_k, t_k for k = 1..L-1 : T_k = Rx(t_k) Rz(a_k) Tx(b)
    a = torch.cat([torch.zeros(B, 1, dtype=dt), math.pi - th], 1)                 # (B, L-1)
    t = torch.cat([torch.zeros(B, 2, dtype=dt), ta], 1)                            # (B, L-1)
    ca_, sa_ = torch.cos(a), torch.sin(a)
    ct, st = torch.cos(t), torch.sin(t)
    z = torch.zeros_like(ca_); o = torch.ones_like(ca_)
    R = torch.stack([torch.stack([ca_, -sa_, z], -1),
                     torch.stack([ct * sa_, ct * ca_, -st], -1),
                     torch.stack([st * sa_, st * ca_, ct], -1)], -2)                # (B, L-1, 3, 3)
    tr = b * torch.stack([ca_, ct * sa_, st * sa_], -1)                            # (B, L-1, 3)
    # inclusive scan of affine maps (R, tr): compose (R1,t1)o(R2,t2) = (R1 R2, R1 t2 + t1)  [earlier on the left]
    n = L - 1
    s = 1
    while s < n:
        R1, t1 = R[:, :-s], tr[:, :-s]
        R2, t2 = R[:, s:], tr[:, s:]
        Rn = R1 @ R2
        tn = (R1 @ t2[..., None])[..., 0] + t1
        R = torch.cat([R[:, :s], Rn], 1)
        tr = torch.cat([tr[:, :s], tn], 1)
        s *= 2
    return torch.cat([torch.zeros(B, 1, 3, dtype=dt), tr], 1)


def virtual_cb_t(X):
    """torch version of EP.virtual_cb, (B, L, 3)."""
    b1 = X[:, 1:-1] - X[:, :-2]
    b2 = X[:, 2:] - X[:, 1:-1]
    u1 = b1 / b1.norm(dim=-1, keepdim=True)
    u2 = b2 / b2.norm(dim=-1, keepdim=True)
    m = u1 - u2; m = m / m.norm(dim=-1, keepdim=True).clamp_min(1e-9)
    nn_ = torch.cross(u1, u2, dim=-1); nn_ = nn_ / nn_.norm(dim=-1, keepdim=True).clamp_min(1e-9)
    tt = u1 + u2; tt = tt / tt.norm(dim=-1, keepdim=True).clamp_min(1e-9)
    mid = X[:, 1:-1] + 1.0977 * m - 0.9601 * nn_ + 0.1616 * tt
    return torch.cat([X[:, :1], mid, X[:, -1:]], 1)


def angles_of(X):
    """numpy CA (L,3) -> (theta (L-2,), tau (L-3,)) radians in the builder's parameterisation."""
    th, ta = EP.theta_tau(np.asarray(X, np.float64))
    L = len(X)
    return np.radians(th[1:L - 1]), np.radians(ta[1:L - 2])


# ============================================================================ energy
class Energy:
    """Batched torch energy over internal coordinates x = [theta (L-2), tau (L-3)] (radians)."""

    def __init__(self, out, L, w=None, oracle_P=None, oracle_Pcb=None, oracle_tt=None):
        self.L = L
        self.w = dict(DEFAULT_W)
        if w:
            self.w.update(w)
        w = self.w
        ms = int(w["min_sep"])
        I, J = np.triu_indices(L, k=ms)
        self.I = torch.as_tensor(I); self.J = torch.as_tensor(J)
        self.flat = torch.as_tensor(I * L + J)
        self.np_ = len(I)
        P = np.asarray(out["prob"], np.float64)[I, J] if oracle_P is None else oracle_P
        Pb = np.asarray(out["prob_cb"], np.float64)[I, J] if oracle_Pcb is None else oracle_Pcb
        self.Tca = torch.as_tensor(soft_table(P, w["sigma"]))
        self.Tcb = torch.as_tensor(soft_table(Pb, w["sigma"]))
        self.G = self.Tca.shape[1]
        self.off = torch.arange(self.np_, dtype=torch.int64) * self.G
        tt = np.asarray(out["theta_tau_prob"], np.float64) if oracle_tt is None else oracle_tt   # (L, 9, 24)
        self.PT = torch.as_tensor(tt[1:L - 2])                                                   # residues 1..L-3
        self.n_eval = 0              # number of single-structure energy evaluations (incl. inside relaxations)
        self.n_grad = 0

    # --------------------------------------------------------------- pieces
    def _interp(self, T, D):
        g = (D / GRID_H).clamp(0.0, self.G - 1 - 1e-6)
        i0 = g.floor().long()
        f = g - i0
        Tf = T.reshape(-1)
        idx = self.off[None, :] + i0
        return Tf[idx] * (1 - f) + Tf[idx + 1] * f

    def _pd(self, X):
        B, L = X.shape[0], self.L
        G = X @ X.transpose(1, 2)
        n2 = (X * X).sum(-1)
        D2 = (n2[:, :, None] + n2[:, None, :] - 2 * G).reshape(B, L * L)[:, self.flat]
        return torch.sqrt(D2.clamp_min(1e-8))

    def terms(self, x):
        L = self.L
        th = x[:, :L - 2]; ta = x[:, L - 2:]
        X = build_ca(th, ta)
        X = X - X.mean(1, keepdim=True)
        D = self._pd(X)
        w = self.w
        e_ca = self._interp(self.Tca, D).sum(1)
        CB = virtual_cb_t(X)
        Dcb = self._pd(CB)
        e_cb = self._interp(self.Tcb, Dcb).sum(1)
        thd = th[:, :L - 3] / DEG; tad = ta / DEG
        st, sa = tt_soft_weights(thd, tad, w["sig_th"], w["sig_ta"])
        p = torch.einsum("bia,iac,bic->bi", st, self.PT, sa)
        e_tt = -torch.log(p + 1e-6).sum(1)
        e_s = (torch.relu(w["r0"] - D) ** 2).sum(1)
        thall = th / DEG
        e_w = (torch.relu(thall - 170.0) ** 2 + torch.relu(60.0 - thall) ** 2).sum(1)
        return dict(ca=e_ca, cb=e_cb, tt=e_tt, st=e_s, wall=e_w, X=X)

    def energy_t(self, x):
        T = self.terms(x)
        w = self.w
        return w["w_ca"] * T["ca"] + w["w_cb"] * T["cb"] + w["w_tt"] * T["tt"] + w["w_s"] * T["st"] + w["w_w"] * T["wall"]

    def __call__(self, x, grad=True):
        """x numpy/torch (B, P) -> (E (B,) numpy, G (B,P) numpy or None)."""
        xt = torch.as_tensor(np.asarray(x, np.float64)).clone()
        self.n_eval += xt.shape[0]
        if not grad:
            with torch.no_grad():
                return self.energy_t(xt).numpy(), None
        xt.requires_grad_(True)
        E = self.energy_t(xt)
        g, = torch.autograd.grad(E.sum(), xt)
        self.n_grad += xt.shape[0]
        return E.detach().numpy(), g.numpy()

    def coords(self, x):
        L = self.L
        xt = torch.as_tensor(np.asarray(x, np.float64))
        with torch.no_grad():
            return build_ca(xt[:, :L - 2], xt[:, L - 2:]).numpy()

    def energy_of_ca(self, X):
        """Energy of arbitrary CA traces (K, L, 3) via their internal coordinates (bonds are ignored: the energy is
        evaluated on the IDEALISED-bond rebuild, which preserves theta/tau)."""
        xs = np.stack([np.concatenate(angles_of(Xk)) for Xk in np.asarray(X, float)])
        return self(xs, grad=False)[0], xs

    def energy_cart(self, X):
        """Energy terms evaluated directly on CA coordinates (no rebuild), numpy (K,L,3) -> dict of (K,) arrays."""
        Xt = torch.as_tensor(np.asarray(X, np.float64))
        L = self.L
        with torch.no_grad():
            D = (Xt[:, self.I] - Xt[:, self.J]).norm(dim=-1)
            e_ca = self._interp(self.Tca, D).sum(1)
            CB = virtual_cb_t(Xt)
            e_cb = self._interp(self.Tcb, (CB[:, self.I] - CB[:, self.J]).norm(dim=-1)).sum(1)
            ths, tas = [], []
            for Xk in np.asarray(X, float):
                a, b = angles_of(Xk)
                ths.append(a); tas.append(b)
            th = torch.as_tensor(np.stack(ths)); ta = torch.as_tensor(np.stack(tas))
            st, sa = tt_soft_weights(th[:, :L - 3] / DEG, ta / DEG, self.w["sig_th"], self.w["sig_ta"])
            p = torch.einsum("bia,iac,bic->bi", st, self.PT, sa)
            e_tt = -torch.log(p + 1e-6).sum(1)
            e_s = (torch.relu(self.w["r0"] - D) ** 2).sum(1)
        w = self.w
        tot = w["w_ca"] * e_ca + w["w_cb"] * e_cb + w["w_tt"] * e_tt + w["w_s"] * e_s
        return dict(total=tot.numpy(), ca=e_ca.numpy(), cb=e_cb.numpy(), tt=e_tt.numpy(), st=e_s.numpy())


# ============================================================================ batched L-BFGS
def lbfgs(f, x0, iters=100, m=8, c1=1e-4, max_ls=12, tol=1e-6, step0=None):
    """Batched L-BFGS: f(x (B,P)) -> (E (B,), G (B,P)).  Per-element two-loop recursion and Armijo backtracking.
    Returns (x, E, n_iter_done)."""
    x = np.array(x0, np.float64, copy=True)
    B, P = x.shape
    E, G = f(x)
    S, Y, RHO = [], [], []
    active = np.ones(B, bool)
    for it in range(iters):
        q = G.copy()
        al = []
        for s, y, rho in zip(reversed(S), reversed(Y), reversed(RHO)):
            a = rho * (s * q).sum(1)
            q -= a[:, None] * y
            al.append(a)
        if S:
            s, y = S[-1], Y[-1]
            yy = (y * y).sum(1)
            gam = np.where(yy > 1e-12, (s * y).sum(1) / np.maximum(yy, 1e-12), 1.0)
            gam = np.where(gam > 0, gam, 1.0)
        else:
            gn = np.linalg.norm(G, axis=1)
            gam = (step0 if step0 is not None else 0.1) / np.maximum(gn, 1e-12)   # first step: 0.1 rad total
        r = gam[:, None] * q
        for (s, y, rho), a in zip(zip(S, Y, RHO), reversed(al)):
            bb = rho * (y * r).sum(1)
            r += s * (a - bb)[:, None]
        d = -r
        gd = (G * d).sum(1)
        bad = gd >= 0
        if bad.any():
            d[bad] = -G[bad] * (0.1 / np.maximum(np.linalg.norm(G[bad], axis=1, keepdims=True), 1e-12))
            gd[bad] = (G[bad] * d[bad]).sum(1)
        t = np.ones(B)
        acc = ~active
        xn, En, Gn = x.copy(), E.copy(), G.copy()
        for _ in range(max_ls):
            todo = ~acc
            if not todo.any():
                break
            idx = np.where(todo)[0]
            xt = x[idx] + t[idx, None] * d[idx]
            Et, Gt = f(xt)
            ok = Et <= E[idx] + c1 * t[idx] * gd[idx]
            good = idx[ok]
            xn[good], En[good], Gn[good] = xt[ok], Et[ok], Gt[ok]
            acc[good] = True
            t[idx[~ok]] *= 0.3
        moved = acc & active
        s = xn - x; y = Gn - G
        sy = (s * y).sum(1)
        rho = np.where(moved & (sy > 1e-10), 1.0 / np.maximum(sy, 1e-10), 0.0)
        dE = E - En
        x, E, G = xn, En, Gn
        S.append(np.where(rho[:, None] > 0, s, 0.0)); Y.append(np.where(rho[:, None] > 0, y, 0.0)); RHO.append(rho)
        if len(S) > m:
            S.pop(0); Y.pop(0); RHO.pop(0)
        # convergence: no Armijo step found or negligible decrease
        active &= acc
        active &= ~(dE < tol * np.maximum(1.0, np.abs(E)))
        if not active.any():
            break
    return x, E, it + 1


def relax(energy, x0, iters=100, chunk=256):
    """Relax a batch of internal-coordinate vectors under `energy`; returns (x, E)."""
    x0 = np.asarray(x0, np.float64)
    xs, Es = [], []
    for s in range(0, len(x0), chunk):
        x, E, _ = lbfgs(energy, x0[s:s + chunk], iters=iters)
        xs.append(x); Es.append(E)
    return np.concatenate(xs), np.concatenate(Es)


