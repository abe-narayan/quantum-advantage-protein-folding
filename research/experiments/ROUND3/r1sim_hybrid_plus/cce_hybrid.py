"""Lane methods (b)/(d): cluster-correlation expansion (CCE) of the echo with the HYBRID as base, i.e. classical spins
with successive quantum corrections (order 1 = one bath spin promoted to the quantum core = a 'quantum two-spin'-type
correction per bath spin; order 2 = pair corrections).

    F^(0)   = F_hyb(Q0)                                    Q0 = {a} u bs (+ optional strongest spins), bath classical
    d_j     = F_hyb(Q0 u {j}) - F_hyb(Q0)
    d_jk    = F_hyb(Q0 u {j,k}) - F_hyb(Q0 u {j}) - F_hyb(Q0 u {k}) + F_hyb(Q0)
    F^(1)   = F^(0) + sum_j d_j ;   F^(2) = F^(1) + sum_{j<k in screened set} d_jk
(additive link; exact when every bath spin is promoted).  Also a multiplicative link on the means.
Hybrid = cqc_echo.CQC with one quantum core group + one-spin bath groups (classical spins |s| = sqrt(3)/2), back-action
'none' (reversible external classical field; the only hybrid variant that does not collapse the echo, see README).
Common random numbers: product-state initial ensemble in global spin order (cqc_echo.CQC.init(product=True)), so every
sub-run sees identical initial spin states; combinations are formed per sample and the SE is computed from them.
Checkpoint after every sub-run (atomic).  Usage: python cce_hybrid.py --probe 19 --N 16 --screen 6
"""
from __future__ import annotations

import argparse
import itertools
import json
import math
import os
import time

import numpy as np

import cqc_echo as C

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--base", default="pin", help="pin = {a} u bs; str<k> = grown to k by coupling")
    ap.add_argument("--M", type=int, default=48)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--screen", type=int, default=6, help="order-2 pairs among the top-K bath spins by |d_j|; 0 = all")
    ap.add_argument("--order", type=int, default=2)
    ap.add_argument("--times-us", default="40,80,160,240,320")
    ap.add_argument("--dt", type=float, default=2e-6)
    a = ap.parse_args()
    dm, bs, _ = C.setup("1UBQ", a.probe, a.N)
    Q0 = sorted(set([0] + bs)) if a.base == "pin" else C.core_set(dm, bs, a.base)
    bath = [j for j in range(a.N) if j not in Q0]
    ks = [int(round(float(t) * 1e-6 / a.dt)) for t in a.times_us.split(",")]
    od = os.path.join(HERE, "out_cce"); os.makedirs(od, exist_ok=True)
    tag = f"1UBQ_p{a.probe}_N{a.N}_{a.base}_M{a.M}_s{a.seed}_scr{a.screen}"
    ck = os.path.join(od, tag + ".ckpt.json")
    st = json.load(open(ck)) if os.path.exists(ck) else {"runs": {}, "secs": {}}

    def save():
        json.dump(st, open(ck + ".tmp", "w")); os.replace(ck + ".tmp", ck)

    def run(extra):
        key = ",".join(map(str, sorted(extra)))
        if key in st["runs"]:
            return
        groups = [sorted(Q0 + list(extra))] + [[j] for j in bath if j not in extra]
        q = C.CQC(dm, groups, a.dt, "none")
        smp = {}
        t0 = time.process_time()
        C.echo(q, bs, ks, a.M, a.seed, product=True, samples=smp)
        st["runs"][key] = {f"{k}_{b}": smp[(k, b)].tolist() for (k, b) in smp}
        st["secs"][key] = time.process_time() - t0
        save()

    def arr(extra):
        r = st["runs"][",".join(map(str, sorted(extra)))]
        return {kb: np.array(v) for kb, v in r.items()}

    run([])
    for j in bath:
        run([j])
    F0 = arr([])
    kbs = list(F0)
    win = [kb for kb in kbs if 80 <= int(kb.split("_")[0]) * a.dt * 1e6 <= 320]
    dj = {j: {kb: arr([j])[kb] - F0[kb] for kb in kbs} for j in bath}
    rank = sorted(bath, key=lambda j: -max(abs(dj[j][kb].mean()) for kb in win))
    scr = rank if a.screen == 0 else rank[:a.screen]
    pairs = list(itertools.combinations(sorted(scr), 2)) if a.order >= 2 else []
    for (j, k) in pairs:
        run([j, k])
    # combinations
    est = {"order0": {}, "order1": {}, "order2": {}, "mult1": {}, "mult2": {}}
    for kb in kbs:
        f0 = F0[kb]
        f1 = f0 + sum(dj[j][kb] for j in bath)
        f2 = f1 + sum(arr([j, k])[kb] - arr([j])[kb] - arr([k])[kb] + f0 for (j, k) in pairs)
        for name, v in (("order0", f0), ("order1", f1), ("order2", f2)):
            est[name][kb] = [float(v.mean()), float(v.std(ddof=1) / math.sqrt(len(v)))]
        m0 = f0.mean()
        if m0 > 0 and all(arr([j])[kb].mean() > 0 for j in bath):
            lg1 = math.log(m0) + sum(math.log(arr([j])[kb].mean()) - math.log(m0) for j in bath)
            est["mult1"][kb] = [math.exp(lg1), float("nan")]
            ok = all(arr([j, k])[kb].mean() > 0 for (j, k) in pairs)
            if ok:
                lg2 = lg1 + sum(math.log(arr([j, k])[kb].mean()) - math.log(arr([j])[kb].mean())
                                - math.log(arr([k])[kb].mean()) + math.log(m0) for (j, k) in pairs)
                est["mult2"][kb] = [math.exp(lg2), float("nan")]
    out = dict(probe=a.probe, N=a.N, base=a.base, Q0=Q0, bath=bath, M=a.M, seed=a.seed, screen=a.screen,
               screened=scr, n_pairs=len(pairs), ks=ks, times_us=[k * a.dt * 1e6 for k in ks], bs=bs, est=est,
               n_subruns=len(st["runs"]), cpu_secs=float(sum(st["secs"].values())),
               max_core=len(Q0) + (2 if pairs else 1),
               dj_window_max={str(j): float(max(abs(dj[j][kb].mean()) for kb in win)) for j in bath})
    fj = os.path.join(od, tag + ".json")
    json.dump(out, open(fj + ".tmp", "w"), indent=1); os.replace(fj + ".tmp", fj)
    print(json.dumps(dict(file=os.path.basename(fj), cpu=round(out["cpu_secs"], 1), subruns=out["n_subruns"],
                          screened=scr)))


if __name__ == "__main__":
    main()
