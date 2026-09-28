"""Exponential-cost (NOT polynomial) adversary for the T-A side, from cached data only: exact(N-2) reference corrected by
the change of the first-order multiplicative spin-addition estimate (base 10, per-b g2 core) between N-2 and N:
    mult:  F_N ~ F_ref(N-2) * M_N / M_{N-2}          add:  F_N ~ F_ref(N-2) + (M_N - M_{N-2})
M_N from subcluster.py cache.  Compared with the lane's Z4a (plain exact(N-2)) and Z2 (hybrid difference correction)."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subcluster as S

cache = S.load_cache()


def mult_add1(p, dm18, bs, N, kb=10):
    dmN = dm18[:N, :N]
    out = {}
    for b in bs:
        Cb = S.select(dmN, b, kb, "g2")
        f0 = np.array(cache[S.key(p, Cb, b)]["F"])
        lr = np.zeros_like(f0)
        for j in range(N):
            if j in Cb:
                continue
            fj = np.array(cache[S.key(p, sorted(Cb + [j]), b)]["F"])
            lr += np.log(np.clip(fj, 1e-6, None)) - np.log(np.clip(f0, 1e-6, None))
        out[b] = f0 * np.exp(lr)
    return out


rows = []
for p in (19, 245):
    dm18, bs, _ = S.C.setup("1UBQ", p, 18)
    for N in (16, 18):
        tt, R = S.ref(p, N)
        _, Rm = S.ref(p, N - 2)
        w = (tt >= 79.9) & (tt <= 320.1)
        MN, Mm = mult_add1(p, dm18, bs, N), mult_add1(p, dm18, bs, N - 2)
        for name, est in (("Z4a exact(N-2)", {b: Rm[b] for b in bs}),
                          ("exact(N-2) * M_N/M_(N-2)", {b: Rm[b] * MN[b] / Mm[b] for b in bs}),
                          ("exact(N-2) + M_N - M_(N-2)", {b: Rm[b] + MN[b] - Mm[b] for b in bs}),
                          ("M_N alone (add1 mult base10)", MN)):
            e = max(float(np.abs(est[b][w] - R[b][w]).max()) for b in bs)
            rows.append(dict(probe=p, N=N, method=name, max_err=round(e, 4)))
            print(f"p{p:<3} N{N} {name:<32} max_err {e:.3f}")
json.dump(rows, open(os.path.join(HERE, "delta_correction.json"), "w"), indent=1)
