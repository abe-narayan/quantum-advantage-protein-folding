"""R1-SIM (PREREG_G1_C1_Q4.md): cluster-size convergence of the protein 1H echo F_ab(t) at the instrument's sites b.
Reads research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone/<pdb>_p<probe>_N<N>.json and computes
    Delta_N(t) = max_b |F^(N+2)(t) - F^(N)(t)|,   threshold(N, t) = sigma + 2 (err_N + err_{N+2})
Pre-registered verdict per probe:
    KILL      : exists N <= 18 such that Delta_{N'}(t) <= threshold for all N' >= N in the ladder and all t <= 320 us
    SUPPORT   : Delta_18(t) > 3 sigma at some t >= 160 us
    otherwise INCONCLUSIVE.   Overall KILL / SUPPORT only if both probes agree.
Writes research/results/PROCESSED/cone_summary.json.
"""
from __future__ import annotations

import glob
import json
import os
import re
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
SIGMA = 0.01


def main():
    runs = defaultdict(dict)
    for f in glob.glob(os.path.join(D, "*.json")):
        m = re.match(r"(\w+)_p(\d+)_N(\d+)\.json", os.path.basename(f))
        if not m:
            continue
        r = json.load(open(f))
        runs[(m.group(1), int(m.group(2)))][int(m.group(3))] = r
    out = {}
    for (pdb, probe), byN in sorted(runs.items()):
        Ns = sorted(byN)
        rows = []
        for a, b in zip(Ns, Ns[1:]):
            ra, rb = byN[a], byN[b]
            ta, tb = np.array(ra["times_us"]), np.array(rb["times_us"])
            common = [t for t in ta if np.min(np.abs(tb - t)) < 0.5 and t > 0]
            d = []
            for t in common:
                ia = int(np.argmin(np.abs(ta - t))); ib = int(np.argmin(np.abs(tb - t)))
                d.append(max(abs(ra["F"][k][ia] - rb["F"][k][ib]) for k in ra["F"] if k in rb["F"]))
            thr = SIGMA + 2 * (ra["err_typ"] + rb["err_typ"])
            rows.append(dict(N=a, N_next=b, times_us=common, delta=d, thr=thr,
                             converged_all_t=bool(all(x <= thr for x in d))))
        # KILL: exists N <= 18 from which every later step is converged at all t
        kill = False
        for i, r in enumerate(rows):
            if r["N"] <= 18 and all(rr["converged_all_t"] for rr in rows[i:]):
                kill = True; break
        support = any(r["N"] == 18 and any(x > 3 * SIGMA for t, x in zip(r["times_us"], r["delta"]) if t >= 160)
                      for r in rows)
        verdict = "KILL" if kill and not support else ("SUPPORT" if support else "INCONCLUSIVE")
        out[f"{pdb}_p{probe}"] = dict(Ns=Ns, steps=rows, verdict=verdict)
        print(f"{pdb} p{probe}: N ladder {Ns} -> {verdict}")
        for r in rows:
            print(f"   {r['N']:2d}->{r['N_next']:2d} thr {r['thr']:.4f} max-delta by t: " +
                  " ".join(f"{t:.0f}:{x:.3f}" for t, x in zip(r["times_us"], r["delta"])))
    vs = [v["verdict"] for v in out.values()]
    overall = "KILL" if vs and all(v == "KILL" for v in vs) else ("SUPPORT" if vs and all(v == "SUPPORT" for v in vs) else "INCONCLUSIVE")
    out["overall"] = overall
    print("overall:", overall)
    os.makedirs(os.path.join(ROOT, "research", "results", "PROCESSED"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "research", "results", "PROCESSED", "cone_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
