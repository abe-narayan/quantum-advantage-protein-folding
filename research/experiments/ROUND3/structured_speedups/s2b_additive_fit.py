"""S2b: stable estimate of the additive (block-separable) share of A80 variance.

The best L2 approximation of f by a sum of single-group functions has explained variance W_1/Var (Efron-Stein).
A ridge fit with a finite per-group basis LOWER-bounds W_1/Var; we report held-out R^2 of
  (i) additive-in-groups model (group = (theta_r, tau_r); per group: degree-4 poly in each coordinate offset,
      cos/sin(k tau) k=1..3, and 3 within-group cross terms),
 (ii) the same plus nearest-neighbour group products (r, r+1) of the linear/cos/sin features (a 'chain-local
      2-body' model),
on the same measures as S2 (local30, local10, prior).  Heavy-tailed clash energies are also fitted after clipping
at the 99th percentile (reported separately).
"""
from __future__ import annotations

import os

import numpy as np

from common import HERE, Timer, atomic_json, load_crop, load_json, make_energy, x_from_ca
from qapf.sampling import hrex as H

OUT = os.path.join(HERE, "s2b_additive_fit_v2.json")   # v1 (fixed lambda=1e-3, overfits at L>=60) kept in s2b_additive_fit.json
COORDS = os.path.join(HERE, "s4_coords.npz")


def feats(X, xs, L):
    th = X[:, :L - 2] - xs[:L - 2]; ta = X[:, L - 2:]
    dta = np.angle(np.exp(1j * (ta - xs[L - 2:])))
    F, lin = [], []
    for r in range(L - 3):
        t = th[:, r] * 5.0; u = dta[:, r]
        cols = [t, t ** 2, t ** 3, t ** 4, u, u ** 2, u ** 3, u ** 4]
        cols += [np.cos(k * ta[:, r]) for k in (1, 2, 3)] + [np.sin(k * ta[:, r]) for k in (1, 2, 3)]
        cols += [t * u, t * t * u, t * u * u]
        F += cols
        lin.append(np.stack([t, np.cos(ta[:, r]), np.sin(ta[:, r])], 1))
    t = th[:, L - 3] * 5.0
    F += [t, t ** 2, t ** 3]
    A = np.stack(F, 1)
    P = []
    for r in range(L - 4):
        a, b = lin[r], lin[r + 1]
        P.append((a[:, :, None] * b[:, None, :]).reshape(len(X), -1))
    return A, np.concatenate([A] + P, 1)


def _fit(A, y, lam):
    ym = y.mean()
    w = np.linalg.solve(A.T @ A + lam * len(A) * np.eye(A.shape[1]), A.T @ (y - ym))
    return w, ym


def ridge_r2(Ftr, ytr, Fte, yte, lams=(1e-3, 1e-2, 1e-1, 1.0, 10.0)):
    """ridge with lambda chosen on a validation split (last 20% of train); returns held-out test R^2."""
    mu, sd = Ftr.mean(0), Ftr.std(0) + 1e-12
    A = (Ftr - mu) / sd; B = (Fte - mu) / sd
    nv = len(A) // 5
    best = None
    for lam in lams:
        w, ym = _fit(A[:-nv], ytr[:-nv], lam)
        r2v = 1 - np.mean((ytr[-nv:] - (A[-nv:] @ w + ym)) ** 2) / np.var(ytr[-nv:])
        if best is None or r2v > best[0]:
            best = (r2v, lam)
    w, ym = _fit(A, ytr, best[1])
    return float(1 - np.mean((yte - (B @ w + ym)) ** 2) / np.var(yte))


def main():
    res = load_json(OUT, {"runs": {}})
    coords = np.load(COORDS)
    T = Timer()
    for L in (30, 60):
        for ch in ("2AB0A", "8AXJA", "5O37A", "3M3PA"):
            crop = f"{ch}_{L}"
            z, L_ = load_crop(crop)
            en = make_energy(z, L_)
            xs = x_from_ca(coords[crop])
            rng = np.random.default_rng(5)
            prior = None
            ntr, nte = 5000, 1500
            for meas in ("local30", "local10", "prior"):
                key = f"{crop}|{meas}"
                if key in res["runs"]:
                    continue
                if T.cpu() > 600:
                    atomic_json(OUT, res); print("budget"); return
                t = Timer()
                n = ntr + nte
                if meas.startswith("local"):
                    dt, dth = (30.0, 10.0) if meas == "local30" else (10.0, 3.0)
                    half = np.concatenate([np.full(L_ - 2, np.radians(dth)), np.full(L_ - 3, np.radians(dt))])
                    X = xs[None] + rng.uniform(-1, 1, (n, len(xs))) * half
                else:
                    prior = prior or H.ExactPrior(en, 1.0)
                    X = prior.sample(n, rng)
                y = np.concatenate([en(X[a:a + 4096], grad=False)[0] for a in range(0, n, 4096)])
                Fa, Fn = feats(X, xs, L_)
                out = dict(crop=crop, L=L_, measure=meas, n_train=ntr, n_test=nte, n_feat_add=Fa.shape[1],
                           n_feat_nn=Fn.shape[1])
                for tag, yy in (("raw", y), ("clip99", np.minimum(y, np.percentile(y[:ntr], 99)))):
                    out[f"R2_additive_{tag}"] = ridge_r2(Fa[:ntr], yy[:ntr], Fa[ntr:], yy[ntr:])
                    out[f"R2_add_plus_nn_{tag}"] = ridge_r2(Fn[:ntr], yy[:ntr], Fn[ntr:], yy[ntr:])
                out["cpu_s"] = t.cpu()
                res["runs"][key] = out
                atomic_json(OUT, res)
                print(key, {k: round(v, 3) for k, v in out.items() if k.startswith("R2")}, f"{t.cpu():.1f}s", flush=True)
    atomic_json(OUT, res)


if __name__ == "__main__":
    main()
