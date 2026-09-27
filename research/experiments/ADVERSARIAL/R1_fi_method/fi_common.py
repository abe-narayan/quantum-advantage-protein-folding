"""R1_fi_method: shared helpers.  Reproduces the cluster / B0 / parameter / observable construction of
scripts/nmr_gate.py (v2) EXACTLY (checked against the stored FI in research/results/RAW/nmr_gate by check_replication()),
and provides the improved Fisher-information statistics used by this adversarial audit.

Statistics (sigma = per-time-point white-noise std; J = exact-model Jacobian d m / d phi (n_obs x p); b = classical-model
bias m_c(phi0) - m_exact(phi0) over the same data points):
  * gate criterion (as in nmr_gate.py):   t_c = first recorded time with max_b |b_b(t)| > sigma
  * linearised estimator bias of a least-squares fit of the (biased) classical model to exact data over a window W:
        dphi(W) = -(J_W' J_W)^-1 J_W' b_W           (Angstrom; uses J_exact as proxy for J_classical, checked at N=8)
    single-parameter version dphi_k = -(J_k' b)/(J_k' J_k), CRB sd_k = sigma / ||J_k||
  * Mahalanobis bias  D(W) = sqrt(dphi' F_W dphi) = || P_J b_W || / sigma   (P_J = projector onto span J_W):
    the bias in units of the parameter standard error along the worst direction.  D <= 0.5: RMSE inflation <= 12%.
  * nuisance-augmented fit: regressors G (n_obs x q) for the model error are fitted jointly; the phi-block of the
    information is the Schur complement J'(I - P_G)J/sigma^2 and the bias uses (I - P_G) b.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

OUT = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(ROOT, "research", "results", "RAW")


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def setup(pdb="1UBQ", probe=19, N=10, orient=0, K=3, hn_only=False):
    """Cluster, B0, observed spins bs and the C1 v2 parameter list (identical logic to scripts/nmr_gate.py)."""
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    if hn_only:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        names = [names[i] for i in keep]; xyz = xyz[keep]; resid = np.asarray(resid)[keep]
        probe = keep.index(probe)
    idx = SP.cluster(xyz, probe, N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    params = []
    for k in far:
        u = (X0[k] - X0[0]) / dist[k]
        params.append(dict(name=f"radial_{names[idx[k]]}", move=[(int(k), u)], r=float(dist[k])))
    pres = resid[idx[0]]
    cnt = {}
    for i in range(N):
        cnt[resid[idx[i]]] = cnt.get(resid[idx[i]], 0) + 1
    kfar = next((int(k) for k in np.argsort(-dist) if resid[idx[k]] != pres and cnt[resid[idx[k]]] >= 2), None)
    if kfar is not None:
        kres = resid[idx[kfar]]
        grp = [int(i) for i in range(N) if resid[idx[i]] == kres]
        ug = (X0[kfar] - X0[0]) / dist[kfar]
        params.append(dict(name=f"rigid_res{kres}", move=[(i, ug) for i in grp], r=float(dist[kfar]), n_moved=len(grp)))
    return dict(pdb=pdb, probe=probe, N=N, orient=orient, names=[names[i] for i in idx], resid=[int(resid[i]) for i in idx],
                idx=[int(i) for i in idx], X0=X0, b0=b0, dist=dist, bs=bs, params=params)


def geom(cfg, p, delta):
    X = cfg["X0"].copy()
    for (i, u) in p["move"]:
        X[i] = X[i] + delta * np.asarray(u)
    return X


def exact(cfg, X, dt=2e-6, steps=160, rec=10, gamma=0.0, otoc=True, b0=None, scale=1.0):
    """sector-exact S_ab, F_ab (dict b -> array) for coordinates X; scale multiplies every coupling (order parameter)."""
    dm = SP.couplings(X, cfg["b0"] if b0 is None else b0) * scale
    tt, S, F = SP.sector_exact_correlators(dm, dt, steps, 0, cfg["bs"], gamma=gamma, record_every=rec, otoc=otoc)
    return tt, S, F


def vec(d, bs, n=None):
    """stack a dict b -> series into one data vector ordered (b, t)."""
    return np.concatenate([np.asarray(d[b] if b in d else d[str(b)], float)[:n] for b in bs])


def fd_jacobian(fun, deltas, h):
    """central differences; fun(delta_vector) -> (S_vec, F_vec)."""
    JS, JF = [], []
    for k in range(len(deltas)):
        e = np.zeros(len(deltas)); e[k] = h
        Sp, Fp = fun(e); Sm, Fm = fun(-e)
        JS.append((Sp - Sm) / (2 * h)); JF.append((Fp - Fm) / (2 * h))
    return np.array(JS).T, np.array(JF).T


def mask_window(nb, nt, t_end, t_start=0):
    """boolean mask over the stacked (b, t) data vector selecting t_start <= t_index < t_end."""
    m = np.zeros(nt, bool); m[t_start:t_end] = True
    return np.tile(m, nb)


def lin_bias(J, b, sigma, G=None, rcond=1e-10):
    """linearised LS estimator bias and Mahalanobis bias; optional nuisance regressors G (projected out)."""
    if G is not None and G.shape[1]:
        Q, _ = np.linalg.qr(G)
        J = J - Q @ (Q.T @ J)
        b = b - Q @ (Q.T @ b)
    Fm = J.T @ J / sigma ** 2
    dphi = -np.linalg.lstsq(J, b, rcond=rcond)[0]
    D = math.sqrt(max(float(dphi @ Fm @ dphi), 0.0))
    single = []
    for k in range(J.shape[1]):
        jk = J[:, k]
        nn = float(jk @ jk)
        single.append(dict(dphi=float(-(jk @ b) / nn) if nn > 0 else float("nan"),
                           crb_sd=float(sigma / math.sqrt(nn)) if nn > 0 else float("inf")))
    return dict(dphi=dphi.tolist(), D=D, F=Fm.tolist(), single=single,
                crb_sd_joint=np.sqrt(np.clip(np.diag(np.linalg.pinv(Fm)), 0, None)).tolist())


def unique_cols(J, names, tol=1e-9):
    keep, seen = [], []
    for k in range(J.shape[1]):
        v = J[:, k]
        if any(np.allclose(v, w, rtol=tol, atol=1e-12) for w in seen):
            continue
        seen.append(v); keep.append(k)
    return keep


def dump(obj, name):
    def _np(o):
        if isinstance(o, np.integer):
            return int(o)
        if isinstance(o, np.floating):
            return float(o)
        if isinstance(o, np.ndarray):
            return o.tolist()
        raise TypeError(type(o))
    p = os.path.join(OUT, name)
    json.dump(obj, open(p, "w"), indent=1, default=_np)
    return p
