"""QM-04 cooperativity test, one crop: temperature replica exchange at lam=1 on the learned energy; saves per-rung
energy traces for heat capacity / histogram bimodality / Lee-Kosterlitz barrier analysis, and round trips.
Usage: python scripts/tpt_crop.py --crop 5O37A_60 --tmax 40 --rungs 24 --budget 1200"""
from __future__ import annotations
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.protein import energy as EN  # noqa: E402
from qapf.sampling import tpt as TP    # noqa: E402
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crop", required=True)
    ap.add_argument("--tmin", type=float, default=1.0)
    ap.add_argument("--tmax", type=float, default=40.0)
    ap.add_argument("--rungs", type=int, default=24)
    ap.add_argument("--budget", type=float, default=1200.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "tpt"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.crop}_R{a.rungs}_s{a.seed}"
    fj = os.path.join(a.out, tag + ".json")
    if os.path.exists(fj):
        print("exists"); return
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", a.crop + ".npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    Ts = np.geomspace(a.tmin, a.tmax, a.rungs)
    r = TP.run_tpt(en, Ts, n_scans=10 ** 7, tune_scans=200, seed=a.seed, time_budget_s=a.budget)
    E = r["E"]
    burn = len(E) // 5
    Eb = E[burn:]
    C = Eb.var(0) / Ts ** 2
    res = dict(crop=a.crop, L=L, Ts=Ts.tolist(), scans=r["scans"], trips=r["trips"], rej=r["rej"].tolist(),
               meanE=Eb.mean(0).tolist(), sdE=Eb.std(0).tolist(), C=C.tolist(), Cmax_per_res=float(C.max() / L),
               T_Cmax=float(Ts[int(np.argmax(C))]), grad_evals=int(r["grad_evals"]), secs=r["secs"])
    np.savez_compressed(os.path.join(a.out, tag + ".npz"), E=E.astype(np.float32), Ts=Ts, samples_low=r["samples_low"])
    tmp = fj + ".tmp"; json.dump(res, open(tmp, "w")); os.replace(tmp, fj)
    print(json.dumps({k: res[k] for k in ("crop", "scans", "trips", "Cmax_per_res", "T_Cmax", "secs")}))


if __name__ == "__main__":
    main()
