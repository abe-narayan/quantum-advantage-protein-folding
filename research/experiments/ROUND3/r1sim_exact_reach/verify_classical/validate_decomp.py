"""Validation of decomp_echo.py against an independent dense computation (N = 10, reference apply_step).
Checks: (1) the identity F = H + R exactly (dense); (2) decomp_echo (basis mode = exact sector traces, flip folding,
phase-factored SectorKernel) reproduces dense F, G, H, floor; (3) honly mode (two inverse passes) gives the same G.
Output: validate_decomp.json"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import decomp_echo as DE  # noqa: E402
from decomp_echo import SP  # noqa: E402


def dense(dm, a, bs, steps_list):
    N = len(dm)
    D = 1 << N
    pairs = SP.pair_list(dm, DE.DT)
    S = np.zeros((D, D), complex)
    for c in range(D):
        e = np.zeros(D, complex); e[c] = 1
        T = e.reshape((2,) * N)
        SP.apply_step(T, N, pairs)
        S[:, c] = T.reshape(-1)
    x = np.arange(D)
    Z = [1.0 - 2.0 * ((x >> q) & 1) for q in range(N)]
    Mz = sum(Z) / N
    out = []
    for n in steps_list:
        U = np.linalg.matrix_power(S, n)
        W = U.conj().T @ (Z[a][:, None] * U)
        G = np.array([np.real(np.trace(W * Z[j][None, :])) / D for j in range(N)])   # Tr[W Z_j]
        Wr = W - np.diag(sum(G[j] * Z[j] for j in range(N)))
        F = {b: np.real(np.trace(W @ (Z[b][:, None] * W) * Z[b][None, :])) / D for b in bs}
        # Tr[W Zb W Zb] = sum_xy W_xy zb_y W_yx zb_x
        F = {b: float(np.real(np.einsum("xy,y,yx,x->", W, Z[b], W, Z[b]))) / D for b in bs}
        R = {b: float(np.real(np.einsum("xy,y,yx,x->", Wr, Z[b], Wr, Z[b]))) / D for b in bs}
        fl = float(np.real(np.einsum("xy,y,yx,x->", Wr, Mz, Wr, Mz))) / D
        out.append(dict(n=n, G=G.tolist(), H=float(np.sum(G ** 2)), F=F, R=R, floor=fl,
                        identity_err=max(abs(F[b] - np.sum(G ** 2) - R[b]) for b in bs)))
    return out


def main():
    t0 = time.time()
    N, probe = 10, 19
    steps = [4, 12]
    dm, bs, names, xyz, gidx = DE.load_cluster("1UBQ", probe, N, "probe")
    dn = dense(dm, 0, bs, steps)
    ec = DE.run("1UBQ", probe, N, "probe", None, "echo", steps, 1, np.complex128, 1, None, log=None, basis=True)
    ho = DE.run("1UBQ", probe, N, "probe", None, "honly", steps, 1, np.complex128, 1, None, log=None, basis=True)
    rep = dict(N=N, probe=probe, steps=steps, bs=bs)
    rep["identity_F_eq_H_plus_R_dense_maxerr"] = max(d["identity_err"] for d in dn)
    rep["echo_vs_dense_F_maxerr"] = max(abs(ec["F"][str(b)][i] - dn[i]["F"][b]) for i in range(len(steps)) for b in bs)
    rep["echo_vs_dense_G_maxerr"] = float(np.max(np.abs(np.array(ec["G"]) - np.array([d["G"] for d in dn]))))
    rep["honly_vs_dense_G_maxerr"] = float(np.max(np.abs(np.array(ho["G"]) - np.array([d["G"] for d in dn]))))
    rep["echo_vs_dense_H_maxerr"] = float(np.max(np.abs(np.array(ec["H"]) - np.array([d["H"] for d in dn]))))
    rep["echo_vs_dense_floor_maxerr"] = float(np.max(np.abs(np.array(ec["floor"]) - np.array([d["floor"] for d in dn]))))
    rep["echo_vs_dense_R_maxerr"] = max(abs(ec["R_"][str(b)][i] - dn[i]["R"][b]) for i in range(len(steps)) for b in bs)
    rep["sumG_dense"] = [float(np.sum(d["G"])) for d in dn]
    rep["dense_values"] = [dict(n=d["n"], H=d["H"], floor=d["floor"], F=d["F"], R=d["R"]) for d in dn]
    rep["secs"] = time.time() - t0
    json.dump(rep, open(os.path.join(HERE, "validate_decomp.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in rep.items() if k != "dense_values"}, indent=1))


if __name__ == "__main__":
    main()
