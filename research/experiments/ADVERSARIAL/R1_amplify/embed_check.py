"""R1 amplify, robustness to embedding (base geometry only; MEASURED): how much do the core-10 observables of
1UBQ probe 19 (o0) move when the 2 next-nearest protons are added (N_env = 12, as in R1-E), for
  secular dipolar: S, F1, F2        (sector-exact)
  double-quantum : S, F1            (parity-exact, pair norm matched s = sqrt 3)
Misfit(t) = max_b |X_env12(t) - X_core10(t)| / sigma.  0-100 us, 20 us grid.  Writes embed_check.json."""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import amp_lib as L  # noqa: E402

SIG = 0.01
g10 = L.job_geometry("1UBQ", 19, 10, 0)
g12 = L.job_geometry("1UBQ", 19, 12, 0)
assert list(g12["idx"][:10]) == list(g10["idx"]), "core must be the first 10 of the 12-cluster"
bs = g10["bs"]
dt, steps, rec = 2e-6, 50, 10
out = dict(bs=bs, names_env_added=[g12["names"][i] for i in g12["idx"][10:]], sigma=SIG, times_us=None, runs={})
for ham in ("secular", "dq"):
    res = {}
    for lab, g in (("core10", g10), ("env12", g12)):
        t0 = time.time()
        dm = L.SP.couplings(g["X0"], g10["b0"])
        if ham == "secular":
            o = L.exact_sector(dm, dt, steps, 0, bs, rec, want_F2=True, want_P=False)
        else:
            o = L.exact_parity(len(dm), L.dq_pair_terms(dm), dt, steps, 0, bs, rec, want_P=False, want_F2=False)
        res[lab] = dict(S=o["S"], F1=o["F1"], F2=o["F2"], secs=time.time() - t0)
        out["times_us"] = (o["times"] * 1e6).tolist()
        print(ham, lab, round(time.time() - t0, 1), flush=True)
    mis = {}
    for k in ("S", "F1", "F2"):
        if res["core10"][k] is None:
            continue
        mis[k] = (np.max(np.abs(res["env12"][k] - res["core10"][k]), axis=1) / SIG).tolist()
    out["runs"][ham] = dict(misfit_sigma=mis, core10=res["core10"], env12=res["env12"])
json.dump(L.jsonable(out), open(os.path.join(HERE, "embed_check.json"), "w"), indent=1)
for ham, r in out["runs"].items():
    print(ham, {k: [round(x, 2) for x in v] for k, v in r["misfit_sigma"].items()})
