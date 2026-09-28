"""Shared helpers for the ROUND3 structured_speedups lane.

All energies are the production A80 learned energy (qapf.protein.energy, esmprior_v1 tables) on ladder crops
data/instruments/ladder/<chain>_<L>.npz.  DEP code paths use only the ESM outputs (prob, prob_cb, theta_tau_prob,
contact_prob, expected, sd).  The native CA trace (`ca`) is touched ONLY by functions whose name starts with
`oracle_` and their outputs are labelled ORACLE.
"""
from __future__ import annotations

import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ[_v] = "1"

import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))

import torch  # noqa: E402

torch.set_num_threads(1)
from qapf.protein import energy as EN  # noqa: E402

LADDER = os.path.join(ROOT, "data", "instruments", "ladder")
CHAINS = sorted({f.rsplit("_", 1)[0] for f in os.listdir(LADDER) if f.endswith(".npz")})
LENGTHS = (30, 45, 60, 80, 100, 120, 150)


def load_crop(crop):
    z = np.load(os.path.join(LADDER, crop + ".npz"))
    L = len(str(z["seq"]))
    return z, L


def make_energy(z, L):
    return EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=1, default=float)
    os.replace(tmp, path)


def load_json(path, default=None):
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return default


def mds_coords(D):
    """Classical MDS (level-1 spectral method) of a distance matrix -> (L,3) coords, eigenvalues of the Gram."""
    D = np.asarray(D, float)
    L = len(D)
    J = np.eye(L) - 1.0 / L
    G = -0.5 * J @ (D ** 2) @ J
    w, V = np.linalg.eigh(G)
    w, V = w[::-1], V[:, ::-1]
    X = V[:, :3] * np.sqrt(np.clip(w[:3], 1e-9, None))
    return X, w


def fix_bonds(X, b=EN.BOND):
    """Rescale consecutive CA-CA vectors to the ideal bond length (keeps directions)."""
    X = np.asarray(X, float)
    d = np.diff(X, axis=0)
    d = d / np.linalg.norm(d, axis=1, keepdims=True).clip(1e-9) * b
    return np.concatenate([X[:1], X[:1] + np.cumsum(d, 0)])


def x_from_ca(X):
    th, ta = EN.angles_of(X)
    th = np.clip(th, np.radians(61.0), np.radians(169.0))
    return np.concatenate([th, ta])


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def oracle_native(z):
    """ORACLE: native CA trace. Evaluation-only."""
    return np.asarray(z["ca"], float)


class Timer:
    def __init__(self):
        self.t0 = time.time(); self.c0 = time.process_time()

    def wall(self):
        return time.time() - self.t0

    def cpu(self):
        return time.process_time() - self.c0
