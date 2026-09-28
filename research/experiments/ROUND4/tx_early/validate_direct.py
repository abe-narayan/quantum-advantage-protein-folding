"""Validate the direct X estimator (X_direct = R^ - floor) against EXACT traces at N = 12 and compare its noise with
the plain estimator (X = F^ - H^ - floor).  Exact: dense per-sector Trotter-step unitaries (spins.sector_step_unitaries,
the reference circuit), W = U^-n Z_a U^n per sector, F = Tr[W Z_b W Z_b]/2^N, G_j = Tr[W Z_j]/2^N, floor by the exact
per-sector formula.  Estimators: tx_echo echo mode, complex128, 24 seeds.  Writes validate_direct.json."""
import json
import math
import os

import numpy as np

import tx_echo as TX
from kernels import FE, SP

HERE = os.path.dirname(os.path.abspath(__file__))
N, steps = 12, [20, 40, 60]
out = {}
for probe in (19, 245):
    dm, bs, names, _ = FE.load_instance("1UBQ", probe, N)
    F = {b: np.zeros(3) for b in bs}
    G = np.zeros((3, N))
    gk = {}
    for idx, Uk in SP.sector_step_unitaries(dm, 2e-6):
        k = int(bin(int(idx[0])).count("1"))
        za = TX.zsign(idx, 0)
        Zs = np.stack([TX.zsign(idx, q) for q in range(N)])
        gk[k] = np.zeros((3, N))
        for ti, n in enumerate(steps):
            Un = np.linalg.matrix_power(Uk, n)
            W = Un.conj().T @ (za[:, None] * Un)
            dW = np.real(np.diag(W))
            gk[k][ti] = Zs @ dW / 2.0 ** N          # tau_k(Z_j W)
            for b in bs:
                A = W * TX.zsign(idx, b)[None, :]
                F[b][ti] += float(np.real(np.trace(A @ A))) / 2.0 ** N
    for k in gk:
        G += gk[k]
    H = np.sum(G ** 2, 1)
    floor = np.zeros(3)
    for k in range(N + 1):
        tauI = math.comb(N, k) / 2.0 ** N
        e = TX.zz_offdiag_mean(N, k)
        sumG = G.sum(1)
        zz = tauI * (e * (sumG ** 2 - np.sum(G ** 2, 1)) + np.sum(G ** 2, 1))
        tw = tauI - 2 * np.sum(G * gk[k], 1) + zz
        floor += ((N - 2 * k) / N) ** 2 * tw
    Xex = {b: F[b] - H - floor for b in bs}
    ep, ed, fl = [], [], []
    for seed in range(1, 25):
        r = TX.run("1UBQ", probe, N, "echo", steps, 1, np.complex128, 1000 + seed, f"VALD_p{probe}_N12_s{seed}",
                   log=lambda s: None)
        for b in bs:
            ep.append(np.array(r["X"][str(b)]) - Xex[b])
            ed.append(np.array(r["Xdirect"][str(b)]) - Xex[b])
        fl.append(np.array(r["floor"]) - floor)
    ep, ed, fl = np.array(ep), np.array(ed), np.array(fl)
    out[f"p{probe}"] = dict(
        X_exact={str(b): Xex[b].tolist() for b in bs}, H_exact=H.tolist(), floor_exact=floor.tolist(),
        F_exact={str(b): F[b].tolist() for b in bs},
        rms_err_X_plain=float(np.sqrt(np.mean(ep ** 2))), rms_err_X_direct=float(np.sqrt(np.mean(ed ** 2))),
        mean_err_X_plain=float(np.mean(ep)), mean_err_X_direct=float(np.mean(ed)),
        max_abs_mean_err_direct_per_cell=float(np.max(np.abs(ed.reshape(24, len(bs), 3).mean(0)))),
        se_of_mean_per_cell=float(np.sqrt(np.mean(ed ** 2)) / math.sqrt(24)),
        rms_err_floor=float(np.sqrt(np.mean(fl ** 2))),
        typ_scale=2.0 ** (-N / 2))
    print(probe, json.dumps({k: v for k, v in out[f"p{probe}"].items() if not isinstance(v, (dict, list))}), flush=True)
json.dump(out, open(os.path.join(HERE, "validate_direct.json"), "w"), indent=1)
