"""R1 value lens, part 6: the 'dynamics floor' -- bias of a rigid-lattice forward model when the real couplings are
motionally averaged.

Real protein protons move (backbone NH libration, side-chain and methyl motions): each dipolar coupling is scaled by an
order parameter, d_ij -> S_ij d_ij (S_ij ~ 0.8-0.95 for rigid backbone sites, far lower for side chains/methyls;
INFERENCE, textbook Lipari-Szabo ranges, not re-verified).  A static-geometry forward model that ignores this is biased.
Here: exact (sector) N = 10 dynamics of the SAME cluster, probe, orientation and observables as a MEASURED C1 job, with
couplings scaled (a) uniformly by S = 0.95, 0.90 and (b) per pair S_ij ~ U[0.85, 1.0] (3 seeds).  The linearised
parameter bias of fitting a rigid model to these 'motional' data is delta = (J J^T)^-1 J (s_S - s_1), with J the job's
stored Jacobian, for echo data, transfer data and both.  Compared with the job's CRBs (fi_value.json).
Validation: the unscaled run must reproduce the job's stored S_exact / F_exact to < 1e-9.
Cost: ~2-10 s per exact run, 12 runs.  Output: dynamics_floor.json.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

JOBS = [("research/results/RAW/nmr_gate/1UBQ_p19_N10_o0_g0.json", False),
        ("research/results/RAW/nmr_gate_hn/1UBQHN_p487_N10_o0_g0.json", True)]


def vec(dct, bs):
    return np.concatenate([np.asarray(dct[b] if b in dct else dct[str(b)], float) for b in bs])


def main():
    fv = {r["file"]: r for r in json.load(open(os.path.join(HERE, "fi_value.json")))["rows"]}
    out = {}
    for rel, hn in JOBS:
        d = json.load(open(os.path.join(ROOT, rel)))
        names, xyz, res = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{d['pdb']}_H.pdb"))
        if hn:
            keep = [i for i, n in enumerate(names) if n.startswith("H/")]
            names = [names[i] for i in keep]; xyz = xyz[keep]
        probe = [i for i, n in enumerate(names) if n == d["probe_name"]][0]
        idx = SP.cluster(xyz, probe, d["N"])
        assert [names[i] for i in idx] == d["cluster_names"]
        X0 = xyz[idx]
        b0 = np.asarray(d["b0"])
        bs = d["bs"]
        rec = max(1, d["steps"] // (len(d["times"]) - 1))
        dm0 = SP.couplings(X0, b0)

        def run(dm):
            t0 = time.time()
            _, S, F = SP.sector_exact_correlators(dm, d["dt"], d["steps"], 0, bs, gamma=0.0, record_every=rec, otoc=True)
            return vec(S, bs), vec(F, bs), time.time() - t0

        S1, F1, secs = run(dm0)
        err = max(np.max(np.abs(S1 - vec(d["S_exact"], bs))), np.max(np.abs(F1 - vec(d["F_exact"], bs))))
        print(f"{rel}: validation max |diff| = {err:.2e} ({secs:.1f} s)")
        # Jacobians (de-duplicated parameter list as in fi_value.py)
        row = fv[rel]
        P = [p for p in d["params"] if p["name"] in row["params"]]
        seen, Pk = [], []
        for p in P:
            if p["name"] in seen:
                continue
            seen.append(p["name"]); Pk.append(p)
        JS = np.array([vec(p["dS"], bs) for p in Pk])
        JF = np.array([vec(p["dF"], bs) for p in Pk])
        JB = np.hstack([JS, JF])
        rng = np.random.default_rng(7)
        cases = [("uniform_S0.95", np.full_like(dm0, 0.95)), ("uniform_S0.90", np.full_like(dm0, 0.90))]
        for s in range(3):
            M = rng.uniform(0.85, 1.0, dm0.shape)
            M = np.triu(M, 1); M = M + M.T
            cases.append((f"pairwise_U0.85-1.0_seed{s}", M))
        recs = {}
        for lab, scale in cases:
            Ss, Fs, secs = run(dm0 * scale)
            r = {}
            for obs, J, ds in (("transfer", JS, Ss - S1), ("echo", JF, Fs - F1), ("both", JB, np.concatenate([Ss - S1, Fs - F1]))):
                bias = np.linalg.solve(J @ J.T, J @ ds)
                r[obs] = dict(bias_A=bias.tolist(), max_abs_bias_A=float(np.max(np.abs(bias))),
                              max_misfit_sigma=float(np.max(np.abs(ds)) / d["sigma"]))
            crbq = np.asarray(row["CRB_quantum_marg"])
            r["both"]["bias_over_quantum_CRB"] = (np.abs(np.asarray(r["both"]["bias_A"])) / crbq).tolist()
            recs[lab] = r
            print(f"  {lab:28s} misfit echo {r['echo']['max_misfit_sigma']:5.1f} sigma, transfer {r['transfer']['max_misfit_sigma']:5.1f} sigma | "
                  f"bias(both) " + " ".join(f"{x:+.3f}" for x in r["both"]["bias_A"]) + " A | /CRB_q "
                  + " ".join(f"{x:.0f}" for x in r["both"]["bias_over_quantum_CRB"]) + f"  ({secs:.1f} s)")
        out[rel] = dict(params=[p["name"] for p in Pk], validation_max_abs=err, CRB_quantum=row["CRB_quantum_marg"],
                        CRB_classical=row["CRB_classical_marg"], cases=recs)
    json.dump(out, open(os.path.join(HERE, "dynamics_floor.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
