"""Analyse NMR gate results (Program C / QM-19..21): for each job and truncation weight w, the classical-failure time
t_c(w) = first recorded time the truncated-model bias exceeds thr = max(sigma, k_se * SE_typ), SE_typ = 2^{-N/2}/sqrt(nrand)
(typicality noise of the exact reference), and the fraction of structural Fisher information carried at t >= t_c(w)
("hard" information: present in the exact dynamics where the weight-<=w classical model is already wrong).
Writes research/results/PROCESSED/nmr_gate_summary.json and prints a table."""
from __future__ import annotations
import glob, json, math, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def analyse(dirs, k_se=3.0):
    rows = []
    for d in dirs:
        for f in sorted(glob.glob(os.path.join(ROOT, d, "*.json"))):
            r = json.load(open(f))
            N, nr, sig = r["N"], r["nrand"], r["sigma"]
            se = 2 ** (-N / 2) / math.sqrt(nr)
            thr = max(sig, k_se * se)
            for w, tr in r["truncation"].items():
                bias = np.asarray(tr["max_bias"])
                bad = np.nonzero(bias > thr)[0]
                tc = int(bad[0]) if len(bad) else len(bias)
                for p in r["params"]:
                    fi_t = np.asarray(p["FI_t"])
                    tot = fi_t.sum()
                    rows.append(dict(file=os.path.basename(f), pdb=r["pdb"], probe=r["probe"], N=N, gamma=r["gamma"],
                                     orient=r["orient"], w=int(w), param=p["name"], r=p["r"], thr=thr, t_c_index=tc,
                                     t_c_us=(r["times"][tc] * 1e6 if tc < len(r["times"]) else None),
                                     FI_total=float(tot), FI_hard=float(fi_t[tc:].sum()),
                                     frac_hard=float(fi_t[tc:].sum() / tot) if tot > 0 else None,
                                     final_kept_norm2=tr["kept_norm2"][-1], final_strings=tr["n_strings"][-1]))
    return rows


def main():
    dirs = sys.argv[1:] or ["research/results/RAW/nmr_pilot", "research/results/RAW/nmr_gate"]
    rows = analyse(dirs)
    os.makedirs(os.path.join(ROOT, "research", "results", "PROCESSED"), exist_ok=True)
    json.dump(rows, open(os.path.join(ROOT, "research", "results", "PROCESSED", "nmr_gate_summary.json"), "w"), indent=0)
    print(f"{'file':34s} {'w':>2s} {'param':26s} {'r':>5s} {'t_c(us)':>8s} {'FI_tot':>9s} {'frac_hard':>9s} {'norm2':>6s}")
    for x in rows:
        print(f"{x['file'][:34]:34s} {x['w']:2d} {x['param'][:26]:26s} {x['r']:5.2f} {str(x['t_c_us'])[:8]:>8s} "
              f"{x['FI_total']:9.1f} {('%.3f' % x['frac_hard']) if x['frac_hard'] is not None else 'nan':>9s} {x['final_kept_norm2']:.4f}")


if __name__ == "__main__":
    main()
