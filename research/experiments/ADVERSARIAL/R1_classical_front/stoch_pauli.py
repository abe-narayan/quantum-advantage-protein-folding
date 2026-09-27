"""E3: sparse Pauli propagation with UNBIASED stochastic reinsertion of the discarded weight (Monte-Carlo Pauli paths).

Heisenberg evolution of Z_a through the SAME Trotter circuit with qapf.nmr.spins.conj_pair (exact pair conjugation),
followed after every pair by stochastic rounding (FCIQMC-style integer-walker compression):
        |c| >= eps : kept exactly
        |c| <  eps : c -> sign(c) eps with probability |c|/eps, else dropped         (E[c'] = c)
Each step is linear + unbiased rounding => every replica r gives an unbiased operator estimate E[O_r(t)] = O(t).
The echo is QUADRATIC in O, so it is estimated from INDEPENDENT replica pairs (U-statistic):
        F_ab ~ mean_{r<s} sum_P c^r_P c^s_P s_b(P)           (unbiased)
        F_ab ~ [same] / mean_{r<s} sum_P c^r_P c^s_P         (ratio / norm-corrected; consistent, lower variance)
The deterministic eps-truncation of the panel (pauli_eps1e-4, fails at 80 us) is the biased limit of the same scheme.
Cost per replica ~ #kept strings per step, polynomial if eps is fixed (the needed eps is the question).

usage: python stoch_pauli.py eps R M cpu_budget_s [pdb probe]
  (first attempt, eps=1e-3 fixed, R=4, no cap, was stopped at the 10 CPU-min limit before the first 20 us record:
   stochastic reinsertion keeps ~||O||_1/eps strings and the L1 norm grows with scrambling)
"""
from __future__ import annotations

import itertools
import sys
import time

import numpy as np

import common as C
from qapf.nmr import spins as SP


def sround(op, eps, rng):
    c = op.c
    small = np.abs(c) < eps
    if small.any():
        u = rng.random(int(small.sum()))
        cs = c[small]
        keep_s = u < np.abs(cs) / eps
        c = c.copy()
        c[small] = np.where(keep_s, np.sign(cs) * eps, 0.0)
        keep = c != 0.0
        op.x, op.z, op.c = op.x[keep], op.z[keep], c[keep]
    return op


def adaptive_eps(c, M):
    """eps such that E[#strings after stochastic rounding] = #(|c|>=eps) + sum_{|c|<eps} |c|/eps = M."""
    a = np.sort(np.abs(c))[::-1]
    n = len(a)
    tail = np.concatenate([np.cumsum(a[::-1])[::-1], [0.0]])        # tail[k] = sum_{i>=k} a_i
    k = np.arange(0, min(M, n))
    epsk = tail[k] / (M - k)
    ok = (a[k] < epsk) & ((k == 0) | (a[np.maximum(k - 1, 0)] >= epsk))
    idx = np.nonzero(ok)[0]
    return float(epsk[idx[0]]) if len(idx) else float(a[min(M, n) - 1])


def keys(op):
    return (op.x << np.uint64(32)) | op.z


def run(dm, bs, eps, R, seed=0, a=0, max_strings=3_000_000, M=None, cpu_budget=None):
    """eps > 0: fixed rounding threshold.  M: string budget (adaptive eps per pair, eps = max(eps, eps_M)).
    cpu_budget (s): abort cleanly; only the time points reached are returned."""
    N = len(dm)
    pairs = SP.pair_list(dm, C.DT)
    rngs = [np.random.default_rng(seed + 1000 * r) for r in range(R)]
    ops = [SP.PauliOp.single_z(N, a) for _ in range(R)]
    snaps = []
    nstr = []
    epsmax = [0.0]
    t0 = time.process_time()
    for k in range(C.STEPS + 1):
        if cpu_budget and time.process_time() - t0 > cpu_budget:
            break
        if k % C.REC == 0:
            snaps.append([(keys(o), o.c.copy(), o.x.copy()) for o in ops])
            nstr.append([len(o.c) for o in ops])
        if k == C.STEPS:
            break
        for r in range(R):
            o = ops[r]
            for (i, j, ddt) in reversed(pairs):
                o = SP.conj_pair(o, i, j, ddt, None, 0.0)
                e_ = eps
                if M and len(o.c) > M:
                    e_ = max(eps, adaptive_eps(o.c, M))
                    epsmax[0] = max(epsmax[0], e_)
                o = sround(o, e_, rngs[r])
                if len(o.c) > max_strings:
                    raise RuntimeError("string cap")
            ops[r] = o
    # estimators
    F_u = {b: [] for b in bs}
    F_r = {b: [] for b in bs}
    F_pairs = {b: [] for b in bs}
    norms = []
    for snap in snaps:
        acc = {b: [] for b in bs}
        nn = []
        for r, s in itertools.combinations(range(R), 2):
            k1, c1, x1 = snap[r]
            k2, c2, _ = snap[s]
            _, i1, i2 = np.intersect1d(k1, k2, assume_unique=True, return_indices=True)
            pr = c1[i1] * c2[i2]
            xx = x1[i1]
            nn.append(float(pr.sum()))
            for b in bs:
                sb = np.where(((xx >> np.uint64(b)) & np.uint64(1)).astype(bool), -1.0, 1.0)
                acc[b].append(float((pr * sb).sum()))
        norms.append(nn)
        for b in bs:
            F_u[b].append(float(np.mean(acc[b])))
            F_r[b].append(float(np.mean(acc[b]) / np.mean(nn)))
            F_pairs[b].append(acc[b])
    return ({b: np.array(v) for b, v in F_u.items()}, {b: np.array(v) for b, v in F_r.items()},
            dict(n_strings=nstr, pair_norms=norms, F_pairs={str(b): v for b, v in F_pairs.items()}, eps_max=epsmax[0],
                 n_rec=len(snaps)))


def main():
    eps = float(sys.argv[1]); R = int(sys.argv[2]); M = int(float(sys.argv[3])); budget = float(sys.argv[4])
    clusters = C.CLUSTERS if len(sys.argv) < 7 else [(sys.argv[5], int(sys.argv[6]))]
    for pdb, probe in clusters:
        tt, S0, F0, ref = C.load_or_make_ref(pdb, probe, 10)
        c = C.setup(pdb, probe, 10)
        t0 = time.process_time()
        Fu, Fr, st = run(c["dm"], c["bs"], eps, R, M=M, cpu_budget=budget)
        cpu = time.process_time() - t0
        nr = st["n_rec"]
        tt = tt[:nr]; F0 = {b: F0[b][:nr] for b in c["bs"]}
        iu, tu, eu = C.t_c(Fu, F0, c["bs"], tt)
        ir, tr, er = C.t_c(Fr, F0, c["bs"], tt)
        # statistical error of the pair mean (naive SE across the R(R-1)/2 pair products; pairs are not independent,
        # so this under-states the error ~ by <= sqrt(R/2); reported as a diagnostic only)
        se = {b: [float(np.std(v) / np.sqrt(len(v))) for v in st["F_pairs"][str(b)]] for b in c["bs"]}
        rec = dict(pdb=pdb, probe=probe, N=10, eps=eps, R=R, M=M, cpu_budget=budget, n_rec=nr, eps_max=st["eps_max"],
                   bs=c["bs"], cpu=cpu,
                   unbiased=dict(t_c_index=iu, t_c_us=tu, max_err=eu.tolist(), F_est={str(b): Fu[b].tolist() for b in c["bs"]}),
                   ratio=dict(t_c_index=ir, t_c_us=tr, max_err=er.tolist(), F_est={str(b): Fr[b].tolist() for b in c["bs"]}),
                   pair_se=se, n_strings=st["n_strings"], pair_norms=st["pair_norms"])
        C.dump(rec, f"stoch_{pdb}_p{probe}_eps{eps:g}_M{M}_R{R}.json")
        mx = [max(len(v) for v in st["n_strings"]), int(np.mean([max(v) for v in st["n_strings"]]))]
        print(pdb, probe, "eps", eps, "M", M, "eps_max", st["eps_max"], "n_rec", nr, "R", R, "t_c unbiased", tu, "ratio", tr, "cpu", round(cpu, 1), "peak strings",
              max(max(v) for v in st["n_strings"]), flush=True)
        print("   err_unb", " ".join(f"{e:.3f}" for e in eu))
        print("   err_rat", " ".join(f"{e:.3f}" for e in er))
        print("   se_max ", " ".join(f"{max(se[b][t] for b in c['bs']):.3f}" for t in range(len(tt))))


if __name__ == "__main__":
    main()
