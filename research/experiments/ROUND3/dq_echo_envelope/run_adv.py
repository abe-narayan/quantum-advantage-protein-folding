"""Sparse-Pauli adversary (coefficient truncation eps) on the PHYSICAL double-quantum echo at N = 10.
Same Trotter circuit (dt = 2 us, pair order) as the exact parity engine used in run_fi.py; record grid 10 us.
Failure = first recorded time with max_b |F1_pauli - F1_exact| > sigma for BOTH the plain and the norm-corrected
estimator (the adversary may pick the better one).  Checkpointed every record (JSON + NPZ operator); resumable.
Usage: python run_adv.py --pdb 1UBQ --probe 19 --eps 1e-4 --budget 400 [--tmax 300]
Output: out/adv_<pdb>_p<probe>_dq_eps<eps>.json
"""
from __future__ import annotations

import argparse
import json
import os

import numpy as np

import dq_lib as D


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--eps", type=float, default=1e-4)
    ap.add_argument("--budget", type=float, default=400.0, help="CPU seconds")
    ap.add_argument("--tmax", type=float, default=300.0, help="us")
    ap.add_argument("--stop-after-fail", type=int, default=1)
    a = ap.parse_args()
    fi = json.load(open(os.path.join(D.OUT, f"fi_{a.pdb}_p{a.probe}.json")))
    g = D.geometry(a.pdb, a.probe)
    assert g["bs"] == fi["bs"]
    dm = D.SP.couplings(g["X0"], g["b0"])
    seq = D.L.dq_gate_seq(dm, D.DT, s=1.0)
    ex = dict(S=np.array(fi["dq"]["S"]), F1=np.array(fi["dq"]["F1"]))
    steps = int(round(a.tmax * 1e-6 / D.DT))
    ck = os.path.join(D.OUT, f"adv_{a.pdb}_p{a.probe}_dq_eps{a.eps:g}")
    st = D.pauli_adversary(10, seq, steps, 5, g["bs"], ex, a.eps, ck, budget_s=a.budget,
                           stop_after_fail=a.stop_after_fail)
    fails = [r["t_us"] for r in st["records"] if r["fail_F1"]]
    print(json.dumps(dict(done=st["done_reason"], first_fail_us=(fails[0] if fails else None),
                          last_t_us=st["records"][-1]["t_us"], cpu=round(st["cpu_s"]))), flush=True)


if __name__ == "__main__":
    main()
