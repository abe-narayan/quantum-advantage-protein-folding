"""Brute-force validation of qd_fisher.py building blocks at N = 3-4 (explicit Kronecker products, scipy expm)."""
import os
for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import itertools
import json
import sys

import numpy as np
from scipy.linalg import expm, sqrtm

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import qd_fisher as Q  # noqa: E402

P1 = [np.eye(2), np.array([[0, 1], [1, 0]]), np.array([[0, -1j], [1j, 0]]), np.diag([1.0, -1.0])]


def pauli(digits):
    """digits[q] for qubit q (q = bit q of the basis index) -> dense operator."""
    M = np.array([[1.0]])
    for q in reversed(range(len(digits))):          # most significant bit (qubit n-1) first in kron
        M = np.kron(M, P1[digits[q]])
    return M


def flat_index(digits):
    return sum(dq * 4 ** q for q, dq in enumerate(digits))


out = {}
rng = np.random.default_rng(3)
n = 4
d = 2 ** n
# random dipolar-like couplings
dm = rng.normal(size=(n, n)) * 2 * np.pi * 5e3
dm = np.triu(dm, 1)
dm = dm + dm.T
Hd = np.zeros((d, d), complex)
for i in range(n):
    for j in range(i + 1, n):
        for (k, s) in ((3, 2.0), (1, -1.0), (2, -1.0)):
            dg = [0] * n
            dg[i] = dg[j] = k
            Hd += dm[i, j] / 4 * s * pauli(dg)
secs = Q.sectors(n)
dyn = Q.Dyn(dm, n, 0, secs)
t = 37e-6
U = expm(-1j * Hd * t)
Za = pauli([3] + [0] * (n - 1))
Xd = U @ Za @ U.conj().T
Xb = dyn.X_blocks(t)
M = np.zeros((d, d), complex)
for B, idx in zip(Xb, secs):
    M[np.ix_(idx, idx)] = B
out["X_sector_vs_expm_maxerr"] = float(np.max(np.abs(M - Xd)))
c, im = Q.pauli_from_blocks(Xb, secs, n)
cb = np.zeros(4 ** n)
for dg in itertools.product(range(4), repeat=n):
    cb[flat_index(dg)] = np.real(np.trace(pauli(list(dg)) @ Xd)) / d
out["pauli_transform_maxerr"] = float(np.max(np.abs(c - cb)))
out["pauli_imag_max"] = im

# QFI identity: exact SLD QFI of rho = (I + p X)/d for a parameter moving coupling (0,2)
h = 1e-3
def Xof(scale):
    dm2 = dm.copy()
    dm2[0, 2] *= scale
    dm2[2, 0] *= scale
    Hs = np.zeros((d, d), complex)
    for i in range(n):
        for j in range(i + 1, n):
            for (k, s) in ((3, 2.0), (1, -1.0), (2, -1.0)):
                dg = [0] * n
                dg[i] = dg[j] = k
                Hs += dm2[i, j] / 4 * s * pauli(dg)
    Us = expm(-1j * Hs * t)
    return Us @ Za @ Us.conj().T
dX = (Xof(1 + h) - Xof(1 - h)) / (2 * h)
g = np.zeros(4 ** n)
for dg in itertools.product(range(4), repeat=n):
    g[flat_index(dg)] = np.real(np.trace(pauli(list(dg)) @ dX)) / d
for p in (0.3, 1.0):
    rho = (np.eye(d) + p * Xd) / d
    drho = p * dX / d
    lam, V = np.linalg.eigh(rho)
    Dm = V.conj().T @ drho @ V
    F = 0.0
    for a_ in range(d):
        for b_ in range(d):
            s_ = lam[a_] + lam[b_]
            if s_ > 1e-14:
                F += 2 * abs(Dm[a_, b_]) ** 2 / s_
    out[f"QFI_exact_p{p}"] = float(F)
    out[f"QFI_formula_p{p}"] = float(p * p * np.sum(g * g))

# Bell probabilities for rho (n = 4 => 256 outcomes): direct vs symplectic transform
p = 0.8
rho = (np.eye(d) + p * Xd) / d
phi = np.eye(d).reshape(-1) / np.sqrt(d)            # |Phi+> = sum_i |i>|i>/sqrt(d)
rr = np.kron(rho, rho)
qd = np.zeros(4 ** n)
for dg in itertools.product(range(4), repeat=n):
    v = np.kron(pauli(list(dg)), np.eye(d)) @ phi
    qd[flat_index(dg)] = np.real(v.conj() @ rr @ v)
w, ny, zt = Q.digit_arrays(n)
sy = np.where(ny % 2 == 1, -1.0, 1.0)
r2 = (p * c) ** 2
r2[0] = 1.0
qt = Q.omega_transform(sy * r2, n) / d ** 2
out["bell_prob_maxerr"] = float(np.max(np.abs(qt - qd)))
out["bell_prob_sum"] = float(qt.sum())

# local-basis exact distribution for one random basis vs direct projective measurement
Bq = np.array([1, 2, 3, 1])
Sidx = np.arange(d)
Sbits = (Sidx[:, None] >> np.arange(n)) & 1
fl = (Sbits * (Bq[None, :] * 4 ** np.arange(n)[None, :])).sum(axis=1)
gc = Q.fwht(c[fl][None, :])[0]
q_fast = (1 + p * gc) / d
# direct: rotate each qubit to measure B_q in the computational basis
Hh = np.array([[1, 1], [1, -1]]) / np.sqrt(2)
Sdg = np.diag([1, -1j])
rot1 = {1: Hh, 2: Hh @ Sdg, 3: np.eye(2)}
R = np.array([[1.0]])
for q in reversed(range(n)):
    R = np.kron(R, rot1[int(Bq[q])])
q_dir = np.real(np.diag(R @ rho @ R.conj().T))
# outcome o (bit q = 1 means eigenvalue -1 of B_q): H maps |+>->|0>; H S^dag maps |+i>->|0>
out["local_basis_prob_maxerr"] = float(np.max(np.abs(q_fast - q_dir)))
json.dump(out, open(os.path.join(HERE, "validate.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
