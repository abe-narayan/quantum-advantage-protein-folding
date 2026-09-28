"""ROUND3 / hardness_what_it_takes, part (2): independent replication of distance-geometry (DG) seeding on the A80
learned energy (DEP path: native-free; the native CA trace is read ONLY to attach an ORACLE RMSD label afterwards).

Arms per crop (all relaxed with the SAME batched L-BFGS, 200 iterations, as scripts/g1_mode_census.py):
  DG-E0   expected-distance matrix (npz field 'expected' = distogram mean) -> classical MDS (3-D) -> both chiralities
  DG-E1   same matrix -> classical MDS -> weighted SMACOF (W = 1/(sd^2 + 0.25), sd = npz field 'sd') -> both chiralities
  DG-Dk   K distance matrices drawn per pair from the 28-bin CA distogram -> cMDS + weighted SMACOF -> both chiralities
Every arm is costed separately in energy+gradient evaluations (the Energy.n_grad counter, which includes line-search
trials exactly as the census counter does) and in wall-clock (embedding and relaxation timed separately).

Checkpointing: results are appended per crop and written atomically (tmp + os.replace) after each crop; a crop already
present in the output is skipped, so the script resumes after a kill.  Endpoints (internal coordinates) are saved per
crop to <out_dir>/endpoints/<crop>.npz for native-free basin-identity checks.

Usage: OMP_NUM_THREADS=1 python dg_replicate.py --crops 5O37A_60,5O37A_100 --K 10 --out dg_results.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np  # noqa: E402

REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))
from qapf.protein import energy as EN          # noqa: E402
from qapf.protein import esmprior_v1 as EP     # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
# finite proxy bin edges for sampling distances from the 28-bin distogram (bin 0: [2,4), last bin: [40,44))
EDG = np.concatenate([[2.0], EP.EDGES, [44.0]])
TH_LO, TH_HI = np.radians(61.0), np.radians(169.0)   # inside the theta wall (60..170 deg) of the energy


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def cmds(D):
    """Classical (Torgerson) MDS to 3-D."""
    n = len(D)
    J = np.eye(n) - 1.0 / n
    B = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(B)
    idx = np.argsort(w)[::-1][:3]
    return V[:, idx] * np.sqrt(np.maximum(w[idx], 1e-9))


def smacof(D, W, X, iters=300):
    """Weighted SMACOF stress majorisation (Guttman transform with the weighted Laplacian pseudo-inverse)."""
    V = -W.copy(); np.fill_diagonal(V, 0.0); np.fill_diagonal(V, -V.sum(1))
    Vp = np.linalg.pinv(V)
    for _ in range(iters):
        dX = np.sqrt(((X[:, None] - X[None]) ** 2).sum(-1)) + 1e-9
        Bm = -W * D / dX; np.fill_diagonal(Bm, 0.0); np.fill_diagonal(Bm, -Bm.sum(1))
        X = Vp @ Bm @ X
    return X


def clean(D, W):
    L = len(D)
    D = 0.5 * (D + D.T); W = 0.5 * (W + W.T)
    for i in range(L - 1):
        D[i, i + 1] = D[i + 1, i] = EN.BOND
        W[i, i + 1] = W[i + 1, i] = 100.0
    np.fill_diagonal(D, 0.0); np.fill_diagonal(W, 0.0)
    return D, W


def to_internal(X):
    th, ta = EN.angles_of(X)
    th = np.clip(th, TH_LO, TH_HI)
    return np.concatenate([th, ta])


def both_chiralities(X):
    out = []
    for s in (1.0, -1.0):
        Xs = X.copy(); Xs[:, 2] *= s
        out.append(to_internal(Xs))
    return out


def seeds_for_crop(z, K, rng):
    """Returns list of (arm, x0) and embedding seconds per arm."""
    Dexp = np.asarray(z["expected"], np.float64).copy()
    sd = np.asarray(z["sd"], np.float64)
    W0 = 1.0 / (sd ** 2 + 0.25)
    D0, W = clean(Dexp.copy(), W0.copy())
    seeds, t_emb = [], {}
    t = time.time()
    X0 = cmds(D0)
    for x in both_chiralities(X0):
        seeds.append(("DG-E0", x))
    t_emb["DG-E0"] = time.time() - t
    t = time.time()
    X1 = smacof(D0, W, cmds(D0))
    for x in both_chiralities(X1):
        seeds.append(("DG-E1", x))
    t_emb["DG-E1"] = time.time() - t
    t = time.time()
    P = np.asarray(z["prob"], np.float64)
    L = P.shape[0]
    c = P.reshape(-1, P.shape[-1]).cumsum(1); c /= c[:, -1:]
    for k in range(K):
        u = rng.random((L * L, 1)); b = (u > c).sum(1).clip(0, P.shape[-1] - 1)
        Dk = (EDG[b] + rng.random(L * L) * (EDG[b + 1] - EDG[b])).reshape(L, L)
        Dk = np.triu(Dk, 1); Dk = Dk + Dk.T
        Dk, Wk = clean(Dk, W0.copy())
        Xk = smacof(Dk, Wk, cmds(Dk))
        for x in both_chiralities(Xk):
            seeds.append(("DG-D", x))
    t_emb["DG-D"] = time.time() - t
    return seeds, t_emb


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f)
    os.replace(tmp, path)


def run_crop(crop, K, seed, ep_dir):
    z = np.load(os.path.join(REPO, "data", "instruments", "ladder", crop + ".npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    rng = np.random.default_rng(seed)
    t0 = time.time()
    seeds, t_emb = seeds_for_crop(z, K, rng)
    arms = [a for a, _ in seeds]
    x0 = np.stack([x for _, x in seeds])
    E0 = en(x0, grad=False)[0]
    # relax arm by arm so that the gradient-evaluation cost of each arm is recorded separately
    xr = np.empty_like(x0); Er = np.empty(len(x0)); cost, t_rel = {}, {}
    for arm in ("DG-E0", "DG-E1", "DG-D"):
        idx = [i for i, a in enumerate(arms) if a == arm]
        g0 = en.n_grad; t = time.time()
        xa, Ea = EN.relax(en, x0[idx], iters=200)
        xr[idx] = xa; Er[idx] = np.asarray(Ea).ravel()
        cost[arm] = int(en.n_grad - g0); t_rel[arm] = time.time() - t
    C = en.coords(xr)
    # native-free clustering of DG endpoints (2 A CA-RMSD, energy order), as in the census
    order = np.argsort(Er); reps, assign = [], np.full(len(Er), -1)
    for i in order:
        for ci, rp in enumerate(reps):
            if kabsch_rmsd(C[i], C[rp]) < 2.0:
                assign[i] = ci; break
        else:
            assign[i] = len(reps); reps.append(int(i))
    # ORACLE label only (evaluation): RMSD of every endpoint to the native CA trace
    nat = np.asarray(z["ca"], float)
    rm = [kabsch_rmsd(c, nat) for c in C]
    # native-free confidence descriptors of the distogram (for the hardness-vs-information analysis)
    P = np.asarray(z["prob"], np.float64)
    iu = np.triu_indices(L, 3)
    conf = dict(mean_maxbin=float(P[iu].max(-1).mean()), mean_sd=float(np.asarray(z["sd"])[iu].mean()),
                mean_entropy=float((-(P[iu] * np.log(P[iu] + 1e-12)).sum(-1)).mean()),
                frac_contact_confident=float((np.asarray(z["contact_prob"])[iu] > 0.5).mean()))
    np.savez_compressed(os.path.join(ep_dir, crop + ".npz"), x=xr, E=Er, arms=np.array(arms), x0=x0)
    return dict(crop=crop, L=L, K=K, seed=seed, arms=arms, E_pre=[float(e) for e in E0], E=[float(e) for e in Er],
                rmsd_native_ORACLE=rm, cluster=[int(a) for a in assign], n_clusters=len(reps),
                E_min=float(Er.min()), arm_of_min=arms[int(np.argmin(Er))],
                E_min_by_arm={a: float(Er[[i for i, b in enumerate(arms) if b == a]].min()) for a in cost},
                grad_evals_by_arm=cost, relax_secs_by_arm=t_rel, embed_secs_by_arm=t_emb,
                grad_evals_total=int(en.n_grad), secs_total=time.time() - t0, confidence=conf)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crops", required=True)
    ap.add_argument("--K", type=int, default=10)
    ap.add_argument("--seed", type=int, default=20260928)
    ap.add_argument("--out", default=os.path.join(HERE, "dg_results.json"))
    ap.add_argument("--max-secs", type=float, default=480.0, help="stop starting new crops after this wall time")
    a = ap.parse_args()
    ep_dir = os.path.join(os.path.dirname(os.path.abspath(a.out)), "endpoints")
    os.makedirs(ep_dir, exist_ok=True)
    res = json.load(open(a.out)) if os.path.exists(a.out) else []
    done = {r["crop"] for r in res}
    t_start = time.time()
    for crop in a.crops.split(","):
        if crop in done:
            print("skip", crop, flush=True); continue
        if time.time() - t_start > a.max_secs:
            print("time budget reached; stopping before", crop, flush=True); break
        r = run_crop(crop, a.K, a.seed, ep_dir)
        res.append(r)
        atomic_json(res, a.out)
        print(json.dumps({k: r[k] for k in ("crop", "E_min", "arm_of_min", "E_min_by_arm", "grad_evals_by_arm",
                                            "secs_total")}), flush=True)


if __name__ == "__main__":
    main()
