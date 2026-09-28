"""Exact check of the DERIVED spin-flip folding identity Tr_k[W Z_b W Z_b] = Tr_{N-k}[W Z_b W Z_b] (and the same for
the transfer Tr_k[Z_a(t) Z_b]) with dense per-sector Trotter-step unitaries at N = 10 (1UBQ p19 and p245, the
reference circuit).  Writes validate_flip.json."""
from __future__ import annotations

import json
import os

import numpy as np

import fastecho as FE
from fastecho import SP

HERE = os.path.dirname(os.path.abspath(__file__))


def sector_traces(dm, a, bs, n_list, dt=2e-6):
    N = len(dm)
    out = {}
    for idx, Uk in SP.sector_step_unitaries(dm, dt):
        k = int(bin(int(idx[0])).count("1"))
        za = FE._zs(N, a, idx)
        rows = {}
        for n in n_list:
            Un = np.linalg.matrix_power(Uk, n)
            W = Un.conj().T @ (za[:, None] * Un)
            for b in bs:
                zb = FE._zs(N, b, idx)
                A = W * zb[None, :]                    # W Z_b
                rows.setdefault(str(b), []).append((float(np.real(np.trace(A @ A))),
                                                    float(np.real(np.trace(W * zb[None, :])))))
        out[k] = rows
    return out


def main():
    res = {}
    for probe in (19, 245):
        dm, bs, _, _ = FE.load_instance("1UBQ", probe, 10)
        n_list = [20, 80, 160]
        tr = sector_traces(dm, 0, bs, n_list)
        N = 10
        dev_F = max(abs(tr[k][str(b)][i][0] - tr[N - k][str(b)][i][0]) for k in tr for b in bs for i in range(len(n_list)))
        dev_S = max(abs(tr[k][str(b)][i][1] - tr[N - k][str(b)][i][1]) for k in tr for b in bs for i in range(len(n_list)))
        scale = max(abs(tr[k][str(b)][i][0]) for k in tr for b in bs for i in range(len(n_list)))
        res[f"p{probe}"] = dict(max_abs_dev_F=dev_F, max_abs_dev_S=dev_S, max_abs_trace=scale, n_list=n_list)
        print(probe, res[f"p{probe}"], flush=True)
    json.dump(res, open(os.path.join(HERE, "validate_flip.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
