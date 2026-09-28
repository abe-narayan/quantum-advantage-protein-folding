"""Resource auditor, statistical-power audit of the lane kill rule (pure analysis of existing JSONs, no simulation).

Lane metric: E = max over b in {1,7,8,9}, t in {80,160,240,320} us of |F_method - F_ref|; pass iff E <= sigma = 0.01.
Two noise sources enter E even for a PERFECT (unbiased) method:
  * method sampling noise (reported per-point SE at M = 48);
  * reference noise: one Haar typicality vector, SE_ref = sqrt((1 - F^2)/(2^N + 1)).
For every run we report
  floor50/floor95: median / 95th pct of max_bt |N(0, SE_tot,bt)| (independent-point Monte Carlo, 20000 draws)
                   = the E a zero-bias method would show at this M against this reference;
  lcb:            Bonferroni lower confidence bound on the true max |bias|: max_bt(|err| - z SE_tot), z = 2.96
                   (family-wise 95 %, two-sided, 16 points);
  resolved_fail:  lcb > sigma  (the method is outside the band beyond noise);
  M_needed_exact: M a zero-bias method would need for floor95 <= sigma given its per-sample SD (inf if the reference
                  noise alone already exceeds the budget).
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
REF = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
SIG = 0.01
WIN = (80.0, 320.0)
Z = 2.96
rng = np.random.default_rng(0)


def ref(p, N):
    d = json.load(open(os.path.join(REF, f"1UBQ_p{p}_N{N}.json")))
    return {round(t): {b: d["F"][b][i] for b in d["F"]} for i, t in enumerate(d["times_us"])}


def floor(se, n=20000):
    se = np.asarray(se)
    x = np.abs(rng.standard_normal((n, se.size)) * se).max(1)
    return float(np.median(x)), float(np.quantile(x, 0.95))


def audit(F, S, p, N, M):
    ex = ref(p, N)
    err, se_m, se_r = [], [], []
    for t in sorted(F):
        if not (WIN[0] - 1e-6 <= t <= WIN[1] + 1e-6) or t not in ex:
            continue
        for b in F[t]:
            fx = ex[t][b]
            err.append(F[t][b] - fx)
            se_m.append(S[t][b])
            se_r.append(math.sqrt(max(1 - fx * fx, 0.0) / (2 ** N + 1)))
    err, se_m, se_r = map(np.asarray, (err, se_m, se_r))
    se = np.sqrt(se_m ** 2 + se_r ** 2)
    f50, f95 = floor(se)
    rf50, rf95 = floor(se_r)
    lcb = float((np.abs(err) - Z * se).max())
    # M needed for a zero-bias method with this per-sample SD to reach floor95 <= SIG
    sd = se_m * math.sqrt(M)
    Mneed = None
    if rf95 < SIG:
        for Mt in [48 * 2 ** k for k in range(0, 12)]:
            if floor(np.sqrt(sd ** 2 / Mt + se_r ** 2), 4000)[1] <= SIG:
                Mneed = Mt; break
    return dict(E=round(float(np.abs(err).max()), 4), max_se_method=round(float(se_m.max()), 4),
                max_se_ref=round(float(se_r.max()), 4), floor50=round(f50, 4), floor95=round(f95, 4),
                ref_only_floor50=round(rf50, 4), ref_only_floor95=round(rf95, 4), lcb=round(lcb, 4),
                resolved_fail=bool(lcb > SIG), z_excess=round(float(((np.abs(err) - SIG) / se).max()), 2),
                M_needed_zero_bias=Mneed if Mneed is not None else "unreachable(ref noise)")


def main():
    rows = []
    for f in sorted(glob.glob(os.path.join(LANE, "out", "*.json"))):
        d = json.load(open(f))
        F, S = {}, {}
        for k, t in zip(d["ks"], d["times_us"]):
            r = d["res"][str(k)]["F_core"]
            F[round(t)] = {b: v[0] for b, v in r.items()}
            S[round(t)] = {b: v[1] for b, v in r.items()}
        a = audit(F, S, d["probe"], d["N"], d["M"])
        rows.append(dict(file=os.path.basename(f), probe=d["probe"], N=d["N"], sizes=d["group_sizes"],
                         bath=d["bath"], ba=d["ba"], secs=round(d["secs_total"], 1), **a))
    for f in sorted(glob.glob(os.path.join(LANE, "out_cce", "*.json"))):
        if f.endswith(".ckpt.json"):
            continue
        d = json.load(open(f))
        for name, e in d["est"].items():
            F, S = {}, {}
            for kb, v in e.items():
                k, b = kb.split("_")
                t = round(int(k) * 2.0)
                F.setdefault(t, {})[b] = v[0]
                S.setdefault(t, {})[b] = v[1] if v[1] == v[1] else 0.0
            a = audit(F, S, d["probe"], d["N"], d["M"])
            rows.append(dict(file=os.path.basename(f) + ":" + name, probe=d["probe"], N=d["N"], sizes=[d["max_core"]],
                             bath="cce", ba=name, secs=round(d["cpu_secs"], 1), **a))
    # reference-only floors (what an exact method with its own single Haar vector would score vs the reference)
    refonly = {}
    for p in (19, 245):
        for N in (14, 16, 18):
            ex = ref(p, N)
            se = [math.sqrt(2 * max(1 - ex[t][b] ** 2, 0) / (2 ** N + 1)) for t in (80, 160, 240, 320) for b in ex[t]]
            f50, f95 = floor(se)
            refonly[f"p{p}_N{N}"] = dict(exact_vs_ref_floor50=round(f50, 4), exact_vs_ref_floor95=round(f95, 4))
    out = dict(sigma=SIG, z_bonferroni=Z, window_us=WIN, reference_only_independent_exact=refonly, runs=rows)
    json.dump(out, open(os.path.join(HERE, "power_audit.json") + ".tmp", "w"), indent=1)
    os.replace(os.path.join(HERE, "power_audit.json") + ".tmp", os.path.join(HERE, "power_audit.json"))
    print("exact(own vector) vs reference, independent-point floors:", json.dumps(refonly))
    print(f"{'file':52s} {'E':>6} {'seM':>6} {'f50':>6} {'f95':>6} {'lcb':>7} {'fail?':>5} {'Mneed':>8}")
    for r in sorted(rows, key=lambda r: r["E"]):
        print(f"{r['file'][:52]:52s} {r['E']:6.3f} {r['max_se_method']:6.3f} {r['floor50']:6.3f} {r['floor95']:6.3f} "
              f"{r['lcb']:7.3f} {str(r['resolved_fail']):>5} {str(r['M_needed_zero_bias']):>8}")


if __name__ == "__main__":
    main()
