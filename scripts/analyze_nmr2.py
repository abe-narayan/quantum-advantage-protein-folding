"""Analyse NMR gate v2 results (Program C / QM-19..21) against PREREG_G1_C1_Q4.md (C1) and the stricter best-adversary
panel.  Per job: t_c for every classical adversary, per-parameter FI split, the full Fisher MATRIX (from the saved
derivatives dS) split into easy (t < t_c*) and hard (t >= t_c*) windows, and the information-gain spectrum
    g_max = max_v (v' F_total v) / (v' F_easy v)     (generalised eigenvalue; F_easy regularised by 1e-9 tr F_total)
which is the largest factor in repetitions a quantum forward model saves for SOME parameter combination.
Writes research/results/PROCESSED/nmr_gate2_summary.json and prints the pre-registered decision statistics."""
from __future__ import annotations

import glob
import json
import os
import sys
from collections import defaultdict

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def fisher(r, t0, t1):
    P = [p for p in r["params"] if "dS" in p]
    if not P:
        return None
    bs = sorted(P[0]["dS"])
    J = np.array([np.concatenate([np.asarray(p["dS"][b])[t0:t1] for b in bs]) for p in P])
    return J @ J.T / r["sigma"] ** 2


def gain_spectrum(Ft, Fe):
    if Ft is None:
        return None
    reg = 1e-9 * max(np.trace(Ft), 1e-30)
    A = Fe + reg * np.eye(len(Fe))
    L = np.linalg.cholesky(A)
    Li = np.linalg.inv(L)
    w = np.linalg.eigvalsh(Li @ Ft @ Li.T)
    return w


def analyse(dirs):
    rows = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(ROOT, d, "*.json"))):
            r = json.load(open(f))
            if r.get("version") != 2:
                continue
            nt = len(r["times"])
            adv = r["adversaries"]
            best = r.get("best_adversary")
            tcb = r.get("best_t_c_index", nt)
            Ft = fisher(r, 0, nt)
            Fe = fisher(r, 0, tcb)
            g = gain_spectrum(Ft, Fe)
            ev_t = np.linalg.eigvalsh(Ft) if Ft is not None else None
            ev_e = np.linalg.eigvalsh(Fe) if Fe is not None else None
            row = dict(file=os.path.basename(f), pdb=r["pdb"], probe=r["probe"], probe_name=r["probe_name"], N=r["N"],
                       orient=r["orient"], gamma=r["gamma"], nt=nt, best=best, best_tc=tcb,
                       tc={k: v["t_c_index"] for k, v in adv.items()},
                       params=[dict(name=p["name"], r=p["r"], FI_total=p["FI_total"],
                                    frac_hard={k: v["FI_split"][p["name"]]["frac_hard"] for k, v in adv.items()},
                                    frac_hard_best=r["best_split"][p["name"]]["frac_hard"] if best else None,
                                    gain_best=r["best_split"][p["name"]]["gain"] if best else None)
                               for p in r["params"]],
                       FI_eig_total=ev_t.tolist() if ev_t is not None else None,
                       FI_eig_easy=ev_e.tolist() if ev_e is not None else None,
                       gain_spectrum=g.tolist() if g is not None else None,
                       secs=r["secs"])
            rows.append(row)
    return rows


def med(x):
    x = [v for v in x if v is not None]
    return float(np.median(x)) if x else float("nan")


def main():
    dirs = sys.argv[1:] or ["research/results/RAW/nmr_gate"]
    rows = analyse(dirs)
    out = dict(rows=rows)
    # ---- pre-registered C1 statistics (truncated Pauli w=4 as registered) and the stricter best-adversary versions
    by = defaultdict(list)
    for x in rows:
        by[(x["N"], x["gamma"])].append(x)
    dec = {}
    for (N, g), xs in sorted(by.items()):
        fh4 = [p["frac_hard"].get("pauli_w4") for x in xs for p in x["params"]]
        fhb = [p["frac_hard_best"] for x in xs for p in x["params"]]
        fi1 = np.mean([p["FI_total"] >= 1.0 for x in xs for p in x["params"]])
        gmax = [max(x["gain_spectrum"]) for x in xs if x["gain_spectrum"]]
        bests = defaultdict(int)
        for x in xs:
            bests[x["best"]] += 1
        dec[f"N{N}_g{int(g)}"] = dict(n_jobs=len(xs), median_frac_hard_w4=med(fh4), median_frac_hard_best=med(fhb),
                                      frac_params_FI_ge_1=float(fi1), median_gain_max=med(gmax),
                                      best_adversary_counts=dict(bests),
                                      median_tc={k: med([x["tc"].get(k) for x in xs]) for k in xs[0]["tc"]})
    out["by_N_gamma"] = dec
    os.makedirs(os.path.join(ROOT, "research", "results", "PROCESSED"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "research", "results", "PROCESSED", "nmr_gate2_summary.json"), "w"), indent=1)
    for k, v in dec.items():
        print(k, json.dumps(v))


if __name__ == "__main__":
    main()
