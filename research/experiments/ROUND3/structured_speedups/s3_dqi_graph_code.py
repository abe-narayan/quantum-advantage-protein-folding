"""S3 (DQI precondition, Cartesian encoding): the most DQI-friendly exact encoding of the pair part of the A80 task.

Encoding (DERIVED).  Put residue positions on a periodic lattice x_i in Z_P^3 (additively isomorphic to F_{P^3}).
Every pair term depends on x only through the linear form x_i - x_j, so the pair objective IS max-LINSAT over
F_q (q = P^3) with B = signed vertex-edge incidence matrix of the constraint graph (one row per pair).  The DQI dual
code C_perp = {y in F_q^m : B^T y = 0} is the CYCLE SPACE (circulations) of that graph, so d_perp = girth.
Jordan et al. (arXiv:2408.08292v5, Thm 4.1, verified) require 2*l + 1 < d_perp for the semicircle law
    <s>/m = ( sqrt(l/m (1-rho)) + sqrt(rho (1-l/m)) )^2        (rho = r/p = allowed fraction)
Beyond half-distance (imperfect decoding), any decoder -- even an unbounded one -- can recover a weight-l error of
generic values only if its support S is (i) a forest and (ii) a FLAT of the graphic matroid (no other graph edge
joins two vertices of the same tree of S).  [DERIVED: for large q a generic syndrome in span(S) lies in span(T),
|T|<=|S|, iff span(S) is contained in span(T); uniqueness <=> S is the unique basis of its closure.]
We Monte-Carlo P_dec(l) = Pr[random l-subset is a flat forest] -> l90, l50 (upper bounds on any decoder).

Constraint graphs (DEP, from the ESM distogram only):
  full      : all pairs |i-j|>=3 (the A80 pair support) + chain bonds
  conf      : pairs whose distogram max-bin prob >= 0.5  + chain bonds
  contact   : pairs |i-j|>=3 with contact_prob >= 0.5 + chain bonds
  contact0  : contacts only (sparsest, most generous to DQI)
  ER(null)  : Erdos-Renyi graph with the same n, m as `contact`
Constraint semantics: pair (i,j) satisfied iff d_ij lies in its distogram central 68% credible interval
[q16, q84] (bonds: 3.8 +- 0.2 A).  rho_ij = shell volume / box^3, box = 2*max q84 (no aliasing).
Classical comparator (DEP): fraction satisfied by the S4 level-1 + A80-relaxed structure (a valid chain, i.e. a
LOWER bound on the classical optimum of the DQI objective) and by 64 prior samples (baseline).
ORACLE (labelled): fraction satisfied by the native.
"""
from __future__ import annotations

import os

import numpy as np

from common import (HERE, CHAINS, Timer, atomic_json, load_crop, load_json, make_energy, oracle_native)
from qapf.protein import esmprior_v1 as EP
from qapf.sampling import hrex as H

OUT = os.path.join(HERE, "s3_dqi_graph_code.json")
COORDS = os.path.join(HERE, "s4_coords.npz")
RNG = np.random.default_rng(20260928)


def semicircle(mu, rho):
    mu = np.asarray(mu, float)
    val = (np.sqrt(mu * (1 - rho)) + np.sqrt(rho * (1 - mu))) ** 2
    return np.where(rho <= 1 - mu, val, 1.0)


def mu_needed(target, rho):
    """smallest l/m at which the semicircle value reaches `target`."""
    if target <= rho:
        return 0.0
    lo, hi = 0.0, 1.0 - rho
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if semicircle(mid, rho) >= target:
            hi = mid
        else:
            lo = mid
    return hi


def credible(P):
    """P (..., 28) bin probs -> (q16, q84) distances by linear interpolation of the CDF inside bins."""
    lo = EP.BINS[:-1].copy(); hi = EP.BINS[1:].copy(); hi[-1] = 44.0; lo[0] = 3.0
    c = np.cumsum(P, -1)
    out = []
    for q in (0.16, 0.84):
        k = np.argmax(c >= q, axis=-1)
        cprev = np.where(k > 0, np.take_along_axis(c, np.maximum(k - 1, 0)[..., None], -1)[..., 0], 0.0)
        pk = np.take_along_axis(P, k[..., None], -1)[..., 0]
        f = np.clip((q - cprev) / np.maximum(pk, 1e-12), 0, 1)
        out.append(lo[k] + f * (hi[k] - lo[k]))
    return out


def girth(n, E):
    adj = [[] for _ in range(n)]
    for u, v in E:
        adj[u].append(v); adj[v].append(u)
    best = np.inf
    for s in range(n):
        dist = {s: 0}; par = {s: -1}; q = [s]; h = 0
        while h < len(q):
            u = q[h]; h += 1
            for w in adj[u]:
                if w not in dist:
                    dist[w] = dist[u] + 1; par[w] = u; q.append(w)
                elif par[u] != w:
                    best = min(best, dist[u] + dist[w] + 1)
            if best == 3:
                return 3
    return best


def n_triangles(n, E):
    A = np.zeros((n, n))
    A[E[:, 0], E[:, 1]] = A[E[:, 1], E[:, 0]] = 1
    return int(round(np.trace(A @ A @ A) / 6))


def decodable(n, E, S):
    parent = list(range(n))

    def find(a):
        while parent[a] != a:
            parent[a] = parent[parent[a]]; a = parent[a]
        return a
    for e in S:
        u, v = find(E[e, 0]), find(E[e, 1])
        if u == v:
            return False
        parent[u] = v
    touched = np.zeros(n, bool); touched[E[S].ravel()] = True
    comp = np.array([find(v) if touched[v] else n + v for v in range(n)])
    inS = np.zeros(len(E), bool); inS[S] = True
    bad = (comp[E[:, 0]] == comp[E[:, 1]]) & ~inS
    return not bad.any()


def pdec_curve(n, E, trials=300, stop=0.2, lmax=400):
    m = len(E); curve = {}
    for l in range(1, min(lmax, m) + 1):
        ok = sum(decodable(n, E, RNG.choice(m, l, replace=False)) for _ in range(trials))
        curve[l] = ok / trials
        if curve[l] < stop:
            break
    ls = np.array(sorted(curve)); ps = np.array([curve[l] for l in ls])
    l90 = int(ls[ps >= 0.9].max()) if (ps >= 0.9).any() else 0
    l50 = int(ls[ps >= 0.5].max()) if (ps >= 0.5).any() else 0
    return curve, l90, l50


def frac_sat(X, E, lo, hi):
    d = np.linalg.norm(X[E[:, 0]] - X[E[:, 1]], axis=-1)
    return float(np.mean((d >= lo) & (d <= hi)))


def main():
    res = load_json(OUT, {"crops": {}})
    coords = np.load(COORDS) if os.path.exists(COORDS) else {}
    T = Timer()
    for Lr in (30, 60, 100, 150):
        for ch in CHAINS:
            crop = f"{ch}_{Lr}"
            if crop in res["crops"]:
                continue
            t = Timer()
            z, L = load_crop(crop)
            P = np.asarray(z["prob"], float); P = 0.5 * (P + P.transpose(1, 0, 2))
            q16, q84 = credible(P)
            cp = np.asarray(z["contact_prob"], float); cp = 0.5 * (cp + cp.T)
            I, J = np.triu_indices(L, k=3)
            chain = np.stack([np.arange(L - 1), np.arange(1, L)], 1)
            conf = P[I, J].max(-1) >= 0.5
            cont = cp[I, J] >= 0.5
            pairs_all = np.stack([I, J], 1)
            variants = dict(full=np.concatenate([pairs_all, chain]),
                            conf=np.concatenate([pairs_all[conf], chain]),
                            contact=np.concatenate([pairs_all[cont], chain]),
                            contact0=pairs_all[cont])
            m_c = len(variants["contact"])
            allp = np.stack(np.triu_indices(L, k=1), 1)
            variants["ER_null"] = allp[RNG.choice(len(allp), m_c, replace=False)]
            box = 2.0 * float(q84[I, J].max())
            en = make_energy(z, L)
            prior = H.ExactPrior(en, 1.0)
            xp = prior.sample(64, np.random.default_rng(1))
            Xp = en.coords(xp)
            Xl1 = coords[crop] if crop in coords else None
            nat = oracle_native(z)
            rec = dict(crop=crop, L=L, box_A=box, variants={})
            for name, E in variants.items():
                E = np.asarray(E, int).reshape(-1, 2)
                if len(E) == 0:
                    rec["variants"][name] = dict(n=L, m=0, empty=True)
                    continue
                lo = np.where(np.abs(E[:, 1] - E[:, 0]) == 1, 3.6, q16[E[:, 0], E[:, 1]])
                hi = np.where(np.abs(E[:, 1] - E[:, 0]) == 1, 4.0, q84[E[:, 0], E[:, 1]])
                rho = (4 / 3 * np.pi * (hi ** 3 - lo ** 3)) / box ** 3
                rbar = float(rho.mean())
                g = girth(L, E); tri = n_triangles(L, E)
                curve, l90, l50 = pdec_curve(L, E)
                m = len(E)
                lthm = max(0, int(np.ceil((g - 1) / 2)) - 1) if np.isfinite(g) else None
                fs_prior = float(np.mean([frac_sat(X, E, lo, hi) for X in Xp]))
                fs_l1 = frac_sat(Xl1, E, lo, hi) if Xl1 is not None else None
                v = dict(n=L, m=m, girth=float(g), triangles=tri, d_perp=float(g), l_thm41=lthm,
                         l90=l90, l50=l50, l90_over_m=l90 / m, l50_over_m=l50 / m, rho_bar=rbar,
                         dqi_frac_thm41=float(semicircle(lthm / m, rbar)) if lthm is not None else None,
                         dqi_frac_l90=float(semicircle(l90 / m, rbar)), dqi_frac_l50=float(semicircle(l50 / m, rbar)),
                         classical_frac_prior_mean=fs_prior, classical_frac_level1_relaxed=fs_l1,
                         mu_needed_to_match_level1=(mu_needed(fs_l1, rbar) if fs_l1 is not None else None),
                         pdec_curve={str(k): v_ for k, v_ in curve.items()},
                         ORACLE_frac_native=frac_sat(nat, E, lo, hi))
                if fs_l1 is not None and l50 > 0:
                    v["l_needed_over_l50"] = v["mu_needed_to_match_level1"] * m / l50
                rec["variants"][name] = v
            rec["cpu_s"] = t.cpu()
            res["crops"][crop] = rec
            atomic_json(OUT, res)
            vv = rec["variants"]
            vv = {k: v for k, v in vv.items() if not v.get("empty")}
            print(crop, " ".join(f"{k}:m={v['m']},g={v['girth']:.0f},l90={v['l90']},l50={v['l50']},"
                                f"DQI50={v['dqi_frac_l50']:.3f},cl={v['classical_frac_level1_relaxed'] or float('nan'):.3f}"
                                for k, v in vv.items()), f"{t.cpu():.1f}s", flush=True)
            if T.cpu() > 500:
                print("budget"); return


if __name__ == "__main__":
    main()
