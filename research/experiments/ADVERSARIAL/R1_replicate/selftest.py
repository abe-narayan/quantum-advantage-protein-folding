"""Internal consistency checks of repl_lib (no stored data involved) + timing at N=10.
Run:  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python selftest.py"""
import json
import os
import sys
import time

import numpy as np
import scipy.linalg as sla

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
import repl_lib as L  # noqa: E402
from qapf.nmr.spins import read_h_coords, cluster, couplings as orig_couplings  # noqa: E402  (geometry only)

out = {}
# 1. couplings vs original geometry code
names, xyz, resid = read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
idx = cluster(xyz, 19, 10)
X0 = xyz[idx]
b0 = L.random_b0(1000)
dm = L.my_couplings(X0, b0)
out["couplings_maxdiff_rel"] = float(np.abs(dm - orig_couplings(X0, b0)).max() / np.abs(dm).max())
out["max_abs_d_kHz"] = float(np.abs(dm).max() / (2 * np.pi) / 1e3)
out["max_abs_d_dt_rad"] = float(np.abs(dm).max() * 2e-6)

# 2. embedding vs full Kronecker expm (N=6, several pairs incl. non-adjacent)
N = 6
rng = np.random.default_rng(5)
errs = []
for (i, j) in [(0, 1), (2, 5), (1, 4), (3, 5)]:
    d = rng.normal() * 1e5
    Hf = (d / 4) * (2 * L.full_single(L.P_Z, i, N) @ L.full_single(L.P_Z, j, N)
                    - L.full_single(L.P_X, i, N) @ L.full_single(L.P_X, j, N)
                    - L.full_single(L.P_Y, i, N) @ L.full_single(L.P_Y, j, N))
    Uf = sla.expm(-1j * 2e-6 * Hf)
    Ue = L.embed_local(L.pair_unitary_local(d, 2e-6), i, j, N).toarray()
    errs.append(float(np.abs(Uf - Ue).max()))
out["embed_vs_kron_expm_maxerr"] = max(errs)

# 3. PTM propagation (eps=0) vs dense Heisenberg, random N=6 cluster, 30 steps, record every 5
dm6 = rng.normal(size=(6, 6)) * 5e4; dm6 = np.triu(dm6, 1); dm6 = dm6 + dm6.T
S, F, info = L.exact_trotter(dm6, 2e-6, 30, 5, 0, [1, 3, 5])
P = L.pauli_propagate(dm6, 2e-6, 30, 5, 0, [1, 3, 5], eps=0.0)
out["ptm_vs_dense_N6_S_maxerr"] = max(float(np.abs(np.array(P["S"][b]) - S[b]).max()) for b in [1, 3, 5])
out["ptm_vs_dense_N6_F_maxerr"] = max(float(np.abs(np.array(P["F"][b]) - F[b]).max()) for b in [1, 3, 5])
out["ptm_norm2_drift_N6"] = float(np.abs(np.array(P["norm2"]) - 1).max())
out["dense_imag_unit"] = info

# 4. timing at N=10 (one geometry, dense) and one PTM step
t = time.process_time()
S10, F10, info10 = L.exact_trotter(dm, 2e-6, 160, 10, 0, [1, 7, 8, 9])
out["cpu_s_dense_N10"] = time.process_time() - t
out["dense_N10_info"] = info10
t = time.process_time()
P10 = L.pauli_propagate(dm, 2e-6, 160, 10, 0, [1, 7, 8, 9], eps=1e-4, max_steps=10)
out["cpu_s_ptm_N10_10steps"] = time.process_time() - t
out["ptm_N10_first_record"] = dict(n_strings=P10["n_strings"], S={b: P10["S"][b] for b in [1, 7, 8, 9]})
print(json.dumps(out, indent=1))
json.dump(out, open(os.path.join(HERE, "selftest.json"), "w"), indent=1)
