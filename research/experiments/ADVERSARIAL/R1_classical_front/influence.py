"""Light-cone diagnostic for the echo F_ab(t): which spins does F_ab depend on, and from when?

(i) leave-one-out: for every cluster spin c != a, exact F on the N-1 spins without c (same circuit, gates on c deleted);
    t_infl(c) = first recorded time where max_b |F_{-c} - F_N| > 0.01 (b in bs, b != c).
    If every spin has t_infl <= T, no sub-cluster simulation (and no finite-order CCE) can be within 0.01 after T.
(ii) add-one / add-two: exact F for the SAME (a, b) pairs on the N+1 and N+2 nearest-proton clusters;
    t_embed = first time max_b |F_{N+k} - F_N| > 0.01 (the finite-cluster model itself is not converged after t_embed).
usage: python influence.py [Nextra_max]
"""
from __future__ import annotations

import sys
import time

import numpy as np

import common as C
from qapf.nmr import spins as SP


def main():
    kmax = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    N = 10
    res = dict(N=N, thr=C.THR, clusters={})
    for pdb, probe in C.CLUSTERS:
        tt, S0, F0, ref = C.load_or_make_ref(pdb, probe, N)
        c = C.setup(pdb, probe, N)
        bs, dm = c["bs"], c["dm"]
        ent = dict(bs=bs, leave_one_out={}, add={})
        for cc in range(1, N):
            keep = [i for i in range(N) if i != cc]
            bl = [b for b in bs if b != cc]
            _, _, F = SP.sector_exact_correlators(dm[np.ix_(keep, keep)], C.DT, C.STEPS, 0, [keep.index(b) for b in bl],
                                                  record_every=C.REC, otoc=True)
            Fe = {b: F[keep.index(b)] for b in bl}
            i, tus, err = C.t_c(Fe, F0, bl, tt)
            ent["leave_one_out"][str(cc)] = dict(spin=c["names"][cc], r=float(c["dist"][cc]), in_bs=cc in bs,
                                                t_infl_us=tus, max_err=err.tolist())
        for k in range(1, kmax + 1):
            ck = C.setup(pdb, probe, N + k)
            t0 = time.process_time()
            _, _, Fk = SP.sector_exact_correlators(ck["dm"], C.DT, C.STEPS, 0, bs, record_every=C.REC, otoc=True)
            cpu = time.process_time() - t0
            i, tus, err = C.t_c(Fk, F0, bs, tt)
            ent["add"][str(k)] = dict(N=N + k, t_embed_us=tus, max_err=err.tolist(), cpu=cpu,
                                      F={str(b): Fk[b].tolist() for b in bs},
                                      new_spin_r=[float(x) for x in ck["dist"][N:]])
        res["clusters"][f"{pdb}_p{probe}"] = ent
        loo = sorted(ent["leave_one_out"].values(), key=lambda v: v["r"])
        print(pdb, probe, "leave-one-out t_infl (r, us):", [(round(v["r"], 2), v["t_infl_us"]) for v in loo], flush=True)
        print("   add:", {k: (v["t_embed_us"], round(v["cpu"], 1), [round(x, 3) for x in v["max_err"]]) for k, v in
                          ent["add"].items()}, flush=True)
    C.dump(res, f"influence_N{N}.json")


if __name__ == "__main__":
    main()
