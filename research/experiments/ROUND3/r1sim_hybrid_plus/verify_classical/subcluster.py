"""Classical adversary for the r1sim_hybrid_plus claim: per-(a,b) path-aware EXACT subclusters and an exact-base
spin-addition cluster expansion (first-order CCE with a deterministic exact base), no mean-field bath.

Target (identical to the lane and to scripts/nmr_cone.py): 1UBQ, probe p in {19, 245}, nested N-cluster (N = 16, 18),
b0 = random_b0(1000), fused-pair Trotter circuit dt = 2 us, a = 0, bs = instrument_bs = [1, 7, 8, 9];
    F_ab(t) = Tr[W Z_b W Z_b]/2^N,  W = U(t)^dag Z_a U(t).
Reference: exact typicality cone typicality_cone/1UBQ_p{p}_N{N}.json (one random vector; SD ~ 2^{-N/2}).
Metric: max over b and t in [80, 320] us of |F_method - F_ref|;  sigma = 0.01.

Methods (all deterministic, sector-exact on a SUBCLUSTER of the N-cluster; dropped spins' gates are deleted, the
remaining pair gates keep their order, so a subcluster run is exactly the reference circuit restricted to it):
  sub_<sel><k>   exact F_ab on a k-spin subcluster chosen per b by selector <sel>:
                   g2   greedy from {a, b}: add argmax_j sum_{i in S} d_ij^2   (strongest total coupling to the set)
                   near the k spins nearest the probe (the nested cluster; = the lane's "exact(N-2) predictor" at k=N-2)
  add1_<k>       first-order spin-addition expansion around the g2 core C (|C| = k), every other spin j of the
                 N-cluster added one at a time (|C u {j}| = k+1):
                   additive        F ~ F(C) + sum_j [F(C u j) - F(C)]
                   multiplicative  F ~ F(C) * prod_j F(C u j)/F(C)
                 cost: (N - k) + 1 exact runs of <= k+1 spins, i.e. polynomial in N at fixed k.

Every subcluster result is cached (atomic tmp+replace) in cache.json keyed by the sorted global index tuple, so the run
is resumable and nothing is lost if killed.  Usage:
  OMP_NUM_THREADS=1 python subcluster.py --stage sub --kmax 12
  OMP_NUM_THREADS=1 python subcluster.py --stage add1 --kbase 10
  OMP_NUM_THREADS=1 python subcluster.py --stage report
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, LANE)
from qapf.nmr import spins as SP  # noqa: E402
import cqc_echo as C  # noqa: E402  (setup(): identical geometry to scripts/nmr_cone.py)

REF = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
CACHE = os.path.join(HERE, "cache.json")
DT, STEPS, EVERY = 2e-6, 160, 20
SIG, WIN = 0.01, (80.0, 320.0)


def load_cache():
    return json.load(open(CACHE)) if os.path.exists(CACHE) else {}


def save_cache(c):
    json.dump(c, open(CACHE + ".tmp", "w"))
    os.replace(CACHE + ".tmp", CACHE)


def key(p, sel, b):
    return f"p{p}|{','.join(map(str, sel))}|b{b}"


def exact_sub(cache, p, dmN, sel, b):
    """Exact F_ab(t) (9 times, 0..320 us) on subcluster sel (global indices within the probe's nested cluster)."""
    sel = sorted(set(sel))
    k_ = key(p, sel, b)
    if k_ in cache:
        return np.array(cache[k_]["F"])
    assert 0 in sel and b in sel
    dm = dmN[np.ix_(sel, sel)]
    t0 = time.time()
    _, _, F = SP.sector_exact_correlators(dm, DT, STEPS, 0, [sel.index(b)], record_every=EVERY, otoc=True)
    f = F[sel.index(b)]
    cache[k_] = dict(F=[float(x) for x in f], secs=time.time() - t0, k=len(sel))
    save_cache(cache)
    return f


def select(dm, b, k, how):
    N = len(dm)
    if how == "near":
        s = list(range(k))
        return s if b in s else None
    if how == "g2":
        S = [0, b]
        while len(S) < k:
            rest = [j for j in range(N) if j not in S]
            sc = [np.sum(dm[j, S] ** 2) for j in rest]
            S.append(rest[int(np.argmax(sc))])
        return sorted(S)
    raise ValueError(how)


def ref(p, N):
    d = json.load(open(os.path.join(REF, f"1UBQ_p{p}_N{N}.json")))
    return np.array(d["times_us"]), {int(b): np.array(v) for b, v in d["F"].items()}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="sub")
    ap.add_argument("--kmin", type=int, default=10)
    ap.add_argument("--kmax", type=int, default=12)
    ap.add_argument("--kbase", type=int, default=10)
    ap.add_argument("--probes", default="19,245")
    ap.add_argument("--Ns", default="16,18")
    ap.add_argument("--budget", type=float, default=840.0)
    a = ap.parse_args()
    cache = load_cache()
    t_start = time.time()
    probes = [int(x) for x in a.probes.split(",")]
    Ns = [int(x) for x in a.Ns.split(",")]
    setups = {}
    for p in probes:
        dm18, bs, names = C.setup("1UBQ", p, 18)
        setups[p] = (dm18, bs, names)
    if a.stage in ("sub", "add1", "add2"):
        for p in probes:
            dm18, bs, _ = setups[p]
            for N in Ns:
                dmN = dm18[:N, :N]                          # nested cluster: N-cluster is the prefix of the 18-cluster
                for b in bs:
                    if a.stage == "sub":
                        for k in range(a.kmin, a.kmax + 1):
                            for how in ("g2", "near"):
                                s = select(dmN, b, k, how)
                                if s is None:
                                    continue
                                if time.time() - t_start > a.budget:
                                    print("budget reached"); return
                                exact_sub(cache, p, dm18, s, b)
                    else:
                        Cb = select(dmN, b, a.kbase, "g2")
                        exact_sub(cache, p, dm18, Cb, b)
                        rest = [j for j in range(N) if j not in Cb]
                        subs = [[j] for j in rest]
                        if a.stage == "add2":
                            subs += [[j, l] for ii, j in enumerate(rest) for l in rest[ii + 1:]]
                        for extra in subs:
                            if time.time() - t_start > a.budget:
                                print("budget reached"); return
                            exact_sub(cache, p, dm18, Cb + extra, b)
                print(json.dumps(dict(stage=a.stage, p=p, N=N, secs=round(time.time() - t_start))), flush=True)
    # ------------------------------------------------------------------ report
    rep = dict(sigma=SIG, window_us=WIN, rows=[])
    for p in probes:
        dm18, bs, names = setups[p]
        for N in (16, 18):
            tt, R = ref(p, N)
            w = (tt >= WIN[0] - 1e-6) & (tt <= WIN[1] + 1e-6)
            dmN = dm18[:N, :N]
            methods = {}
            for k in range(8, 15):
                for how in ("g2", "near"):
                    est, ok = {}, True
                    for b in bs:
                        s = select(dmN, b, k, how)
                        kk = key(p, sorted(s), b) if s is not None else None
                        if kk is None or kk not in cache:
                            ok = False; break
                        est[b] = np.array(cache[kk]["F"])
                    if ok:
                        methods[f"sub_{how}{k}"] = est
                for kb in range(8, 13):
                    add, mul, ok = {}, {}, True
                    for b in bs:
                        Cb = select(dmN, b, kb, "g2")
                        k0 = key(p, Cb, b)
                        if k0 not in cache:
                            ok = False; break
                        f0 = np.array(cache[k0]["F"])
                        inc, lr = np.zeros_like(f0), np.zeros_like(f0)
                        for j in range(N):
                            if j in Cb:
                                continue
                            kj = key(p, sorted(Cb + [j]), b)
                            if kj not in cache:
                                ok = False; break
                            fj = np.array(cache[kj]["F"])
                            inc += fj - f0
                            lr += np.log(np.clip(fj, 1e-6, None)) - np.log(np.clip(f0, 1e-6, None))
                        if not ok:
                            break
                        add[b] = f0 + inc
                        mul[b] = f0 * np.exp(lr)
                    if ok:
                        methods[f"add1_additive_base{kb}"] = add
                        methods[f"add1_multiplicative_base{kb}"] = mul
                    # second order: pair increments (inclusion-exclusion) on top of first order
                    add2, mul2, ok2 = {}, {}, ok
                    for b in (bs if ok else []):
                        Cb = select(dmN, b, kb, "g2")
                        f0 = np.array(cache[key(p, Cb, b)]["F"])
                        rest = [j for j in range(N) if j not in Cb]
                        f1 = {j: np.array(cache[key(p, sorted(Cb + [j]), b)]["F"]) for j in rest}
                        inc, lr = np.zeros_like(f0), np.zeros_like(f0)
                        for ii, j in enumerate(rest):
                            for l in rest[ii + 1:]:
                                kjl = key(p, sorted(Cb + [j, l]), b)
                                if kjl not in cache:
                                    ok2 = False; break
                                fjl = np.array(cache[kjl]["F"])
                                inc += fjl - f1[j] - f1[l] + f0
                                L = lambda x: np.log(np.clip(x, 1e-6, None))
                                lr += L(fjl) - L(f1[j]) - L(f1[l]) + L(f0)
                            if not ok2:
                                break
                        if not ok2:
                            break
                        add2[b] = add[b] + inc
                        mul2[b] = mul[b] * np.exp(lr)
                    if ok and ok2:
                        methods[f"add2_additive_base{kb}"] = add2
                        methods[f"add2_multiplicative_base{kb}"] = mul2
            for m, est in methods.items():
                per_b = {int(b): float(np.max(np.abs(est[b][w] - R[b][w]))) for b in bs}
                signed = float(np.mean([np.mean(est[b][w] - R[b][w]) for b in bs]))
                rep["rows"].append(dict(probe=p, N=N, method=m, max_err=round(max(per_b.values()), 4),
                                        per_b={k_: round(v, 4) for k_, v in per_b.items()},
                                        mean_signed=round(signed, 4),
                                        F={int(b): [round(float(x), 4) for x in est[b]] for b in bs}))
    rep["cache_secs_total"] = round(sum(v["secs"] for v in cache.values()), 1)
    rep["cache_entries"] = len(cache)
    json.dump(rep, open(os.path.join(HERE, "subcluster_report.json.tmp"), "w"), indent=1)
    os.replace(os.path.join(HERE, "subcluster_report.json.tmp"), os.path.join(HERE, "subcluster_report.json"))
    for r in sorted(rep["rows"], key=lambda r: (r["method"], r["probe"], r["N"])):
        print(f"p{r['probe']:<3} N{r['N']} {r['method']:<30} max_err {r['max_err']:.3f}  bias {r['mean_signed']:+.3f}"
              f"  per_b {r['per_b']}")
    print("cache CPU-s", rep["cache_secs_total"], "entries", rep["cache_entries"])


if __name__ == "__main__":
    main()
