"""Self-test of amp_lib engines (MEASURED checks, seconds of CPU).
 1. exact_sector (1UBQ p19 N=10 o0, base geometry) reproduces the stored C1 RAW S_exact / F_exact.
 2. P_delta-derived F1 equals the direct F1; P_delta sums to 1 (unitarity).
 3. exact_parity with the SECULAR pair terms equals exact_sector (validates the generic engine used for H_DQ).
 4. Pauli propagation with eps = 0 (no truncation) + WHT dense reconstruction equals exact for S, F1, F2, P_delta,
    for the secular and the DQ circuits on a 6-spin sub-cluster.
 5. pauli_run(eps=1e-4) F1 on N=10 reproduces the stored C1 RAW pauli_eps0.0001 OTOC bias for the first 4 points.
Writes selftest.json."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import amp_lib as L  # noqa: E402

out = {}
g = L.job_geometry("1UBQ", 19, 10, 0)
raw = json.load(open(os.path.join(L.ROOT, "research/results/RAW/nmr_gate/1UBQ_p19_N10_o0_g0.json")))
assert raw["bs"] == g["bs"], (raw["bs"], g["bs"])
dm = L.SP.couplings(g["X0"], g["b0"])
ex = L.exact_sector(dm, 2e-6, 160, 0, g["bs"], 10)
dS = max(np.max(np.abs(ex["S"][:, i] - np.asarray(raw["S_exact"][str(b)]))) for i, b in enumerate(g["bs"]))
dF = max(np.max(np.abs(ex["F1"][:, i] - np.asarray(raw["F_exact"][str(b)]))) for i, b in enumerate(g["bs"]))
der = L.derived_from_pdelta(ex["P"], len(g["bs"]))
out["1_raw_match"] = dict(max_abs_dS=float(dS), max_abs_dF=float(dF))
out["2_pdelta"] = dict(max_abs_F1_from_P=float(np.max(np.abs(der["F1_single"] - ex["F1"]))),
                       max_abs_norm_minus_1=float(np.max(np.abs(der["norm"] - 1))))
exp_ = L.exact_parity(10, L.secular_pair_terms(dm), 2e-6, 160, 0, g["bs"], 10, want_F2=True)
out["3_parity_vs_sector"] = {k: float(np.max(np.abs(exp_[k] - ex[k]))) for k in ("S", "F1", "F2", "P")}
out["3_parity_vs_sector"]["MQC_tot_nonzero_q"] = float(exp_["MQC_tot"][:, 1:].sum())   # secular: q = 0 only

# 4. small cluster, eps = 0
sub = [0] + g["bs"] + [2, 3][:1]
Xs = g["X0"][sub]; bs_s = [1, 2, 3, 4]
dms = L.SP.couplings(Xs, g["b0"])
for label, seq, terms in (("secular", L.secular_gate_seq(dms, 2e-6), L.secular_pair_terms(dms)),
                          ("dq", L.dq_gate_seq(dms, 2e-6), L.dq_pair_terms(dms))):
    e6 = L.exact_parity(6, terms, 2e-6, 40, 0, bs_s, 10, want_F2=True)
    pr, st = L.pauli_run(6, seq, 40, 0, bs_s, 10, eps=0.0, want_F2=True, want_MQtot=True)
    p = pr["plain"]
    out[f"4_pauli_eps0_{label}"] = dict(S=float(np.max(np.abs(p["S"] - e6["S"]))),
                                       F1=float(np.max(np.abs(p["F1"] - e6["F1"]))),
                                       F2=float(np.max(np.abs(p["F2"] - e6["F2"]))),
                                       P=float(np.max(np.abs(p["P"] - e6["P"]))),
                                       MQC_tot=float(np.max(np.abs(p["MQ"] - e6["MQC_tot"]))),
                                       strings_final=int(st["n_strings"][-1]))

# 5. eps = 1e-4 on N=10 for 4 recorded points (80 steps would be long; use 40 steps = index 0..4)
pr, st = L.pauli_run(10, L.secular_gate_seq(dm, 2e-6), 40, 0, g["bs"], 10, eps=1e-4, want_F2=False)
bias = np.max(np.abs(pr["plain"]["F1"] - ex["F1"][:5]), axis=1)
out["5_pauli_eps1e-4_F1_bias"] = dict(mine=bias.tolist(), raw=raw["adversaries"]["pauli_eps0.0001"]["max_bias_otoc"][:5],
                                      secs=st["secs"], n_strings=st["n_strings"])
json.dump(L.jsonable(out), open(os.path.join(HERE, "selftest.json"), "w"), indent=1)
print(json.dumps(L.jsonable(out), indent=1))
