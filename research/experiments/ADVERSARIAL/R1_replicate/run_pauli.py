"""R1 replicate: independent coefficient-threshold ("sparse") Heisenberg Pauli propagation through the same Trotter
circuit, and the echo/transfer failure times t_c versus the independently computed exact reference (exact_trotter.json,
run run_exact.py --mode trotter first).  Compared with the stored adversary 'pauli_eps0.0001' of
research/results/RAW/nmr_gate/1UBQ_p19_N10_o0_g0.json.

Failure-time definition (from scripts/nmr_gate.py): t_c = first recorded index where max_b |model_b - exact_b| > thr,
thr = max(sigma, 3 SE_typ) = 0.01 here (deterministic reference).  Echo estimators: 'plain' F = sum c^2 s_P and
'normcorr' F / sum c^2 (the later C3 estimator; not in the stored file).

Usage (single-threaded; ~2.4 CPU-min per 160 steps):
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python run_pauli.py --eps 1e-4 --trunc pair
  ... --eps 0            (no truncation: must equal the exact reference -> validates the propagator at N=10)
  ... --eps 1e-4 --trunc step --max-steps 80
  ... --eps 1e-5 --trunc pair
"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "src"))
import repl_lib as L  # noqa: E402
from run_exact import setup, STORED  # noqa: E402


def first_fail(bias, thr):
    bad = np.nonzero(np.asarray(bias) > thr)[0]
    return int(bad[0]) if len(bad) else len(bias)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--eps", type=float, default=1e-4)
    ap.add_argument("--trunc", default="pair", choices=["pair", "step"])
    ap.add_argument("--max-steps", type=int, default=None)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--rec", type=int, default=10)
    ap.add_argument("--thr", type=float, default=0.01)
    a = ap.parse_args()
    t0 = time.process_time()
    G = setup()
    bs = G["bs"]
    ex = json.load(open(os.path.join(HERE, "exact_trotter.json")))
    st = json.load(open(STORED))
    dm = L.my_couplings(G["X0"], G["b0"])
    P = L.pauli_propagate(dm, a.dt, a.steps, a.rec, 0, bs, eps=a.eps, trunc=a.trunc, max_steps=a.max_steps)
    n = len(P["steps"])
    E_S = {b: np.asarray(ex["S_exact"][str(b)])[:n] for b in bs}
    E_F = {b: np.asarray(ex["F_exact"][str(b)])[:n] for b in bs}
    S = {b: np.asarray(P["S"][b]) for b in bs}
    F = {b: np.asarray(P["F"][b]) for b in bs}
    nrm = np.maximum(np.asarray(P["norm2"]), 1e-12)
    bias_S = np.max(np.stack([np.abs(S[b] - E_S[b]) for b in bs]), axis=0)
    bias_F = np.max(np.stack([np.abs(F[b] - E_F[b]) for b in bs]), axis=0)
    bias_Fn = np.max(np.stack([np.abs(F[b] / nrm - E_F[b]) for b in bs]), axis=0)
    tc_S, tc_F, tc_Fn = first_fail(bias_S, a.thr), first_fail(bias_F, a.thr), first_fail(bias_Fn, a.thr)
    res = dict(eps=a.eps, trunc=a.trunc, steps_run=P["steps"], n_rec=n, thr=a.thr,
               n_strings=P["n_strings"], kept_norm2=P["norm2"],
               S={str(b): P["S"][b] for b in bs}, F={str(b): P["F"][b] for b in bs},
               max_bias=bias_S.tolist(), max_bias_otoc=bias_F.tolist(), max_bias_otoc_normcorr=bias_Fn.tolist(),
               t_c_index=tc_S if n == len(ex["S_exact"][str(bs[0])]) or tc_S < n else None,
               t_c_otoc_index_plain=tc_F if tc_F < n else None,
               t_c_otoc_index_normcorr=tc_Fn if tc_Fn < n else None,
               truncated_run=n < len(ex["S_exact"][str(bs[0])]))
    # echo FI beyond the failure time (my exact FI, h = 0.05); both estimators
    fh = {}
    for q in ex["params"]:
        if q["h"] != 0.05:
            continue
        fo = np.asarray(q["FI_otoc_t"]); fs = np.asarray(q["FI_t"])
        fh[q["name"]] = dict(frac_hard_otoc_plain=float(fo[tc_F:].sum() / fo.sum()),
                             frac_hard_otoc_normcorr=float(fo[tc_Fn:].sum() / fo.sum()),
                             frac_hard_transfer=float(fs[tc_S:].sum() / fs.sum()) if res["t_c_index"] is not None else None,
                             gain_otoc_best=float(fo.sum() / max(fo[:max(tc_F, tc_Fn)].sum(), 1e-30)))
    res["FI_split_mine"] = fh
    # comparison with the stored adversary of the same label
    lab = {1e-4: "pauli_eps0.0001", 1e-3: "pauli_eps0.001"}.get(a.eps)
    if lab and a.trunc == "pair" and lab in st["adversaries"]:
        sa = st["adversaries"][lab]
        m = min(n, len(sa["max_bias"]))
        res["compare_stored"] = dict(
            label=lab,
            t_c_index_stored=sa["t_c_index"], t_c_otoc_index_stored=sa.get("t_c_otoc_index"),
            n_strings_stored=sa["n_strings"][:m], n_strings_mine=P["n_strings"][:m],
            n_strings_max_absdiff=int(np.abs(np.asarray(sa["n_strings"][:m]) - np.asarray(P["n_strings"][:m])).max()),
            kept_norm2_maxabs=float(np.abs(np.asarray(sa["kept_norm2"][:m]) - np.asarray(P["norm2"][:m])).max()),
            max_bias_maxabs=float(np.abs(np.asarray(sa["max_bias"][:m]) - bias_S[:m]).max()),
            max_bias_otoc_maxabs=float(np.abs(np.asarray(sa["max_bias_otoc"][:m]) - bias_F[:m]).max()),
            frac_hard_otoc_stored={k: v["frac_hard"] for k, v in sa["FI_split_otoc"].items()})
    # comparison with the stored C2 eps-ladder run (research/results/RAW/nmr_sparse), same eps, if present
    c2f = os.path.join(ROOT, "research", "results", "RAW", "nmr_sparse", "1UBQ_p19_N10_o0_g0.json")
    if os.path.exists(c2f) and a.trunc == "pair":
        c2 = json.load(open(c2f))
        run = next((e for e in c2["runs"] if abs(e["eps"] - a.eps) <= 1e-12 * max(a.eps, 1e-30)), None)
        if run is not None:
            m = min(n, len(run["n_strings"]))
            res["compare_stored_C2"] = dict(
                eps=run["eps"], peak_strings_stored=run["peak_strings"],
                n_strings_max_absdiff=int(np.abs(np.asarray(run["n_strings"][:m]) - np.asarray(P["n_strings"][:m])).max()),
                F_maxabs=max(float(np.abs(np.asarray(run["F"][str(b)][:m]) - F[b][:m]).max()) for b in bs),
                S_maxabs=max(float(np.abs(np.asarray(run["S"][str(b)][:m]) - S[b][:m]).max()) for b in bs))
    res["cpu_s"] = time.process_time() - t0
    tag =f"pauli_eps{a.eps:g}_{a.trunc}" + (f"_to{a.max_steps}" if a.max_steps else "")
    json.dump(res, open(os.path.join(HERE, tag + ".json"), "w"), indent=0)
    short = {k: v for k, v in res.items() if k not in ("S", "F", "steps_run")}
    print(json.dumps(short, indent=1))


if __name__ == "__main__":
    main()
