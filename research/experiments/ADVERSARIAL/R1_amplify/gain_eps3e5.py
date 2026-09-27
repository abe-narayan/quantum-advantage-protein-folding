"""R1 amplify: quantum-only information gain of adding F2 when the classical twin is the strongest pre-registered
adversary (sparse Pauli eps = 3e-5): F1 and S reproduced over the full 320 us window (MEASURED by R1_replicate,
pauli_eps3e-05_pair.json: F1 max bias 0.0075 < sigma), F2 fails at 60 us (MEASURED here,
out/obs_1UBQ_p19_N10_o0_secular_eps3e-5.json; assumed to stay failed after 80 us: INFERENCE, lost norm keeps growing).
Classical route: S(all) + F1(all) + F2(t < 60 us).  Quantum route: S(all) + F1(all) + F2(all).
Jacobians from out/obs_1UBQ_p19_N10_o0_secular.json (exact, full window).  Writes gain_eps3e5.json."""
import json, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import amp_lib as L
r = json.load(open(os.path.join(HERE, "out", "obs_1UBQ_p19_N10_o0_secular.json")))
sig = r["sigma"]; t = np.asarray(r["times_us"])
J = {k: np.asarray(r["families"][k]["dsig"]) for k in ("S", "F1", "F2")}
F = lambda X: L.fisher(X.reshape(len(X), -1), sig)
tc2 = int(np.searchsorted(t, 60.0 - 1e-6))
base = F(J["S"]) + F(J["F1"])
Fq = base + F(J["F2"]); Fc = base + F(J["F2"][:, :tc2, :])
cq, cc = L.crb(Fq), L.crb(Fc); cb = L.crb(base)
out = dict(t_c_F2_us=float(t[tc2]), params=[p["name"] for p in r["params"]],
           CRB_classical_S_F1_all=cb, CRB_classical_route=cc, CRB_quantum=cq,
           g_par=(cc / cq) ** 2, g_par_median=float(np.median((cc / cq) ** 2)), g_max=float(L.gen_eigs(Fq, Fc).max()),
           frac_hard_F2=float(np.asarray(r["families"]["F2"]["FI_t"])[tc2:].sum() / np.sum(r["families"]["F2"]["FI_t"])),
           FI_trace=dict(S=float(np.trace(F(J["S"]))), F1=float(np.trace(F(J["F1"]))), F2=float(np.trace(F(J["F2"]))),
                         F2_hard=float(np.trace(F(J["F2"][:, tc2:, :])))))
json.dump(L.jsonable(out), open(os.path.join(HERE, "gain_eps3e5.json"), "w"), indent=1)
print(json.dumps(L.jsonable(out), indent=1))
