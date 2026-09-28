"""S5 (glued-trees / hierarchical-graph / white-box traversal precondition) on a discretised A80 conformation graph.

Exponential quantum-walk traversal (Childs et al. welded trees; Balasubramanian-Li-Harrow CMP 406:209; GHV/LWWZ
stoquastic paths) needs the walk from ENTRANCE to stay in a poly-dimensional invariant subspace (column /
supervertex structure: an equitable partition with exponentially large cells) while classical walkers need
exponentially long to reach EXIT.  Test on a window of s consecutive tau's of a DEP level-1 minimum x* (L=30),
discretised to k bins (centred on x*), all other coordinates fixed; graph = Z_k^s torus nearest-neighbour moves.
  (a) coarsest equitable partition (1-WL colour refinement) with the ENTRANCE individualised, energy colours at
      several resolutions; bare lattice for reference;
  (b) Krylov dimension of H = -A + gamma * diag(E - Emin) from ENTRANCE (Lanczos, full reorthogonalisation);
  (c) classical adversary: discrete steepest descent and Metropolis (T = 1 energy unit) hitting times of the
      discrete global minimum from random starts.
"""
from __future__ import annotations

import os

import numpy as np

from common import HERE, Timer, atomic_json, load_crop, load_json, make_energy, x_from_ca

OUT = os.path.join(HERE, "s5_graph_krylov.json")
COORDS = os.path.join(HERE, "s4_coords.npz")


def neighbours(k, s):
    N = k ** s
    idx = np.arange(N)
    digits = np.stack([(idx // k ** a) % k for a in range(s)], 1)
    nb = []
    for a in range(s):
        for dlt in (-1, 1):
            d2 = digits.copy(); d2[:, a] = (d2[:, a] + dlt) % k
            nb.append((d2 * (k ** np.arange(s))).sum(1))
    return np.stack(nb, 1), digits


def refine(colors, nb, max_iter=200):
    c = np.unique(colors, return_inverse=True)[1]
    ncell = c.max() + 1
    for _ in range(max_iter):
        sig = np.concatenate([c[:, None], np.sort(c[nb], 1)], 1)
        c2 = np.unique(sig, axis=0, return_inverse=True)[1].ravel()
        n2 = c2.max() + 1
        c = c2
        if n2 == ncell:
            break
        ncell = n2
    return int(ncell)


def krylov_dim(nb, diag, s0, kmax=1000, tol=1e-9):
    N = len(diag)

    def H(v):
        return -v[nb].sum(1) + diag * v
    Q = np.zeros((kmax + 1, N))
    q = np.zeros(N); q[s0] = 1.0
    Q[0] = q
    beta_hist = []
    for j in range(kmax):
        w = H(Q[j])
        w -= Q[:j + 1].T @ (Q[:j + 1] @ w)
        w -= Q[:j + 1].T @ (Q[:j + 1] @ w)
        b = np.linalg.norm(w)
        beta_hist.append(float(b))
        if b < tol * (1 + np.abs(diag).max() + nb.shape[1]):
            return j + 1, True, beta_hist
        Q[j + 1] = w / b
    return kmax, False, beta_hist


def main():
    res = load_json(OUT, {"runs": {}})
    coords = np.load(COORDS)
    T = Timer()
    for crop, t0 in (("2AB0A_30", 10), ("8AXJA_30", 10), ("5O37A_30", 4)):
        key = f"{crop}|t0={t0}"
        if key in res["runs"]:
            continue
        z, L = load_crop(crop)
        en = make_energy(z, L)
        xs = x_from_ca(coords[crop])
        s, k = 6, 6
        nb, digits = neighbours(k, s)
        N = k ** s
        X = np.repeat(xs[None], N, 0)
        X[:, (L - 2) + t0 + np.arange(s)] = xs[(L - 2) + t0 + np.arange(s)] + 2 * np.pi * digits / k
        E = np.concatenate([en(X[a:a + 8192], grad=False)[0] for a in range(0, N, 8192)])
        Emin = E.min(); gmin = int(np.argmin(E))
        entrance = int(np.argmax(E))
        rec = dict(crop=crop, L=L, t0=t0, s=s, k=k, N=N, E_range=[float(Emin), float(E.max())],
                   E_at_xstar=float(E[0]), global_min_is_xstar=bool(gmin == 0))
        # (a) equitable partitions
        base = np.zeros(N, int); base[entrance] = 1
        rec["cells_bare_entrance"] = refine(base, nb)
        for res_e in (1e-6, 1.0, 5.0, 20.0):
            col = np.round((E - Emin) / res_e).astype(np.int64) * 2
            col[entrance] += 1
            rec[f"cells_energy_res{res_e:g}"] = refine(col, nb)
        # (b) Krylov dimensions
        kd = {}
        for gam in (0.0, 0.1, 1.0):
            dim, term, bh = krylov_dim(nb, gam * (E - Emin), entrance)
            kd[str(gam)] = dict(dim=dim, terminated=term, beta_last=bh[-1])
        rec["krylov_from_entrance"] = kd
        # (c) classical adversary on the same graph
        rng = np.random.default_rng(3)
        starts = rng.integers(0, N, 400)
        mins = set(np.where(E <= np.min(E[nb], 1))[0].tolist())       # discrete local minima
        hit = 0
        for st in starts:
            v = st
            while True:
                nv = nb[v][np.argmin(E[nb[v]])]
                if E[nv] >= E[v]:
                    break
                v = nv
            hit += int(v == gmin)
        rec["n_discrete_local_minima"] = len(mins)
        rec["steepest_descent_p_hit_global"] = hit / len(starts)
        hts = []
        for w in range(200):
            v = int(rng.integers(0, N)); tt = 0
            while v != gmin and tt < 200000:
                u = nb[v][rng.integers(0, nb.shape[1])]
                if rng.random() < np.exp(-(E[u] - E[v])):
                    v = u
                tt += 1
            hts.append(tt)
        hts = np.array(hts)
        rec["metropolis_T1_hit_steps_median"] = float(np.median(hts))
        rec["metropolis_T1_hit_steps_mean"] = float(hts.mean())
        rec["metropolis_T1_censored_frac"] = float((hts >= 200000).mean())
        rec["cpu_s"] = T.cpu()
        res["runs"][key] = rec
        atomic_json(OUT, res)
        print(key, {kk: v for kk, v in rec.items() if kk not in ("E_range",)}, flush=True)
    atomic_json(OUT, res)


if __name__ == "__main__":
    main()
