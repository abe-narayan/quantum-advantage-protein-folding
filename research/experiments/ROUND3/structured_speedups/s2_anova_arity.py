"""S2 (planted-kXOR arity / block-separability preconditions): ANOVA (Efron-Stein / Sobol) structure of A80.

Groups = residues: factor r = (theta_r, tau_r) (last theta alone).  Under a product measure mu on the factors the
Efron-Stein decomposition f = sum_S f_S gives W_k = sum_{|S|=k} Var f_S.  We estimate, with Saltelli/Jansen
pick-freeze estimators (N base pairs, N(d+2) evaluations):
  first-order fraction  W_1/Var = sum_r S_r          (1.0  <=> block-separable / additive: RsAA-type and QHD-type
                                                       separations are for (near-)separable families; classically
                                                       trivial by coordinate-wise optimisation)
  mean dimension       sum_k k W_k / Var = sum_r T_r (average interaction order: the effective 'arity')
Measures: LOCAL  = uniform box around the DEP level-1 minimum x* (tau +-30 deg, theta +-10 deg; and +-10/+-3 deg)
          PRIOR  = the census restart distribution (qapf.sampling.hrex.ExactPrior at T=1: product over residues).
Bootstrap (200) CIs over base pairs.  Checkpoint per (crop, measure).
"""
from __future__ import annotations

import os

import numpy as np

from common import HERE, Timer, atomic_json, load_crop, load_json, make_energy, x_from_ca
from qapf.sampling import hrex as H

OUT = os.path.join(HERE, "s2_anova_arity.json")
COORDS = os.path.join(HERE, "s4_coords.npz")
N_OF_L = {30: 512, 60: 256, 100: 128}


def groups(L):
    g = [[k, (L - 2) + k] for k in range(L - 3)]
    g.append([L - 3])
    return g


def evalE(en, X, chunk=4096):
    return np.concatenate([en(X[a:a + chunk], grad=False)[0] for a in range(0, len(X), chunk)])


def sobol(en, A, B, G, rng, nboot=200):
    N, d = len(A), len(G)
    fA = evalE(en, A); fB = evalE(en, B)
    fAB = np.empty((d, N))
    for r, cols in enumerate(G):
        X = A.copy(); X[:, cols] = B[:, cols]
        fAB[r] = evalE(en, X)
    V = np.var(np.concatenate([fA, fB]))

    def est(idx):
        v = np.var(np.concatenate([fA[idx], fB[idx]]))
        S = (fB[idx][None] * (fAB[:, idx] - fA[idx][None])).mean(1) / v
        Tt = 0.5 * ((fA[idx][None] - fAB[:, idx]) ** 2).mean(1) / v
        return S, Tt
    S, Tt = est(np.arange(N))
    bs = []
    for _ in range(nboot):
        idx = rng.integers(0, N, N)
        s_, t_ = est(idx)
        bs.append((s_.sum(), t_.sum()))
    bs = np.array(bs)
    return dict(N=N, d=d, n_evals=int(N * (d + 2)), var=float(V), sum_S=float(S.sum()), mean_dim=float(Tt.sum()),
                sum_S_ci=[float(v) for v in np.percentile(bs[:, 0], [2.5, 97.5])],
                mean_dim_ci=[float(v) for v in np.percentile(bs[:, 1], [2.5, 97.5])],
                max_T=float(Tt.max()), n_groups_T_gt_1pct=int((Tt > 0.01).sum()),
                frac_var_heaviest_group=float(Tt.max() / max(Tt.sum(), 1e-12)))


def main():
    res = load_json(OUT, {"runs": {}})
    coords = np.load(COORDS)
    T = Timer()
    for L in (30, 60, 100):
        for ch in ("2AB0A", "8AXJA", "5O37A", "3M3PA"):
            crop = f"{ch}_{L}"
            z, L_ = load_crop(crop)
            en = make_energy(z, L_)
            xs = x_from_ca(coords[crop])
            G = groups(L_)
            N = N_OF_L[L]
            rng = np.random.default_rng(11)
            prior = None
            for meas in ("local30", "local10", "prior"):
                key = f"{crop}|{meas}"
                if key in res["runs"]:
                    continue
                if T.cpu() > 800:
                    atomic_json(OUT, res); print("budget"); return
                t = Timer()
                if meas.startswith("local"):
                    dt, dth = (30.0, 10.0) if meas == "local30" else (10.0, 3.0)
                    half = np.concatenate([np.full(L_ - 2, np.radians(dth)), np.full(L_ - 3, np.radians(dt))])
                    A = xs[None] + rng.uniform(-1, 1, (N, len(xs))) * half
                    B = xs[None] + rng.uniform(-1, 1, (N, len(xs))) * half
                else:
                    prior = prior or H.ExactPrior(en, 1.0)
                    A = prior.sample(N, rng); B = prior.sample(N, rng)
                r = sobol(en, A, B, G, rng)
                r.update(crop=crop, L=L_, measure=meas, cpu_s=t.cpu())
                res["runs"][key] = r
                atomic_json(OUT, res)
                print(key, f"sumS={r['sum_S']:.3f} {np.round(r['sum_S_ci'],3)} meanDim={r['mean_dim']:.2f} "
                           f"{np.round(r['mean_dim_ci'],2)} groups>1%={r['n_groups_T_gt_1pct']}/{r['d']} {t.cpu():.1f}s", flush=True)
    atomic_json(OUT, res)


if __name__ == "__main__":
    main()
