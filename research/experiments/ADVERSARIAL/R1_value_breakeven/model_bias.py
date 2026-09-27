"""R1 value lens, part 2: how large is the forward-model (cluster-truncation) bias compared with the CRB?

Uses the MEASURED R1-E embedding runs (research/results/RAW/nmr_embed/*.json): the same 10-proton core, same
parameters, same observed pairs (a, b), simulated exactly as an isolated core (iso), inside the 12 and 14 nearest
protons (exact_N12, exact_N14) and with the Gaussian-bath dephasing proxy (deph).

Question: if the real protein behaves like the larger embedding, and you fit it with the isolated 10-spin forward model,
what parameter bias do you incur?  Linearised (Gauss-Newton) bias of the weighted least-squares estimate:
    delta_theta = (J J^T)^-1 J (s_env - s_iso)      (J = isolated-core Jacobian; sigma cancels)
and the data misfit max_t |s_env - s_iso| / sigma.  Compared with the isolated-core CRB at sigma = 0.01.
The bias is a LOWER BOUND on the truncation error of an N=10 model (N_env = 12, 14 are still far from the ~600-proton
protein).  Transfer: envs 12, 14, deph.  Echo: env 12 only (the only exact echo embedding measured).
Also: the same for the late window only (t >= 80 us), where the echo information lives.
Output: model_bias.json.
"""
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def vec(dct, bs, sl=slice(None)):
    return np.concatenate([np.asarray(dct[str(b)], float)[sl] for b in bs])


def main():
    out = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_embed", "*.json"))):
        d = json.load(open(f))
        bs, sig = d["bs"], d["sigma"]
        iso = d["envs"]["iso"]
        tt = np.asarray(iso["times"]) * 1e6
        pnames = list(iso["dS"].keys())
        # de-duplicate parameters
        keep, seen = [], []
        for p in pnames:
            v = vec(iso["dS"][p], bs)
            if any(np.allclose(v, s) for s in seen):
                continue
            seen.append(v); keep.append(p)
        rec = dict(params=keep, bs=bs)
        for obs, key, dkey in (("transfer", "S", "dS"), ("echo", "F", "dF")):
            if iso.get(key) is None:
                continue
            for win, sl in (("all", slice(None)), ("late_ge_80us", slice(int(np.searchsorted(tt, 80 - 1e-6)), None))):
                J = np.array([vec(iso[dkey][p], bs, sl) for p in keep])
                F = J @ J.T / sig ** 2
                crb = np.sqrt(np.diag(np.linalg.inv(F)))
                s0 = vec(iso[key], bs, sl)
                for env in ("exact_N12", "exact_N14", "deph"):
                    e = d["envs"].get(env)
                    if e is None or e.get(key) is None:
                        continue
                    ds = vec(e[key], bs, sl) - s0
                    bias = np.linalg.solve(J @ J.T, J @ ds)
                    resid = ds - J.T @ bias
                    rec[f"{obs}_{win}_{env}"] = dict(
                        max_misfit_over_sigma=float(np.max(np.abs(ds)) / sig),
                        rms_misfit_over_sigma=float(np.sqrt(np.mean(ds ** 2)) / sig),
                        bias_A=bias.tolist(), crb_A=crb.tolist(),
                        bias_over_crb=(np.abs(bias) / crb).tolist(),
                        unexplained_rms_over_sigma=float(np.sqrt(np.mean(resid ** 2)) / sig))
        out[os.path.basename(f)] = rec
    json.dump(out, open(os.path.join(HERE, "model_bias.json"), "w"), indent=1)
    for fn, rec in out.items():
        print("==", fn, rec["params"])
        for k, v in rec.items():
            if isinstance(v, dict):
                print(f"  {k:32s} misfit max {v['max_misfit_over_sigma']:6.1f} sigma | bias(A) "
                      + " ".join(f"{x:+.3f}" for x in v["bias_A"]) + " | CRB(A) "
                      + " ".join(f"{x:.3f}" for x in v["crb_A"]) + " | |bias|/CRB "
                      + " ".join(f"{x:.1f}" for x in v["bias_over_crb"])
                      + f" | unexplained {v['unexplained_rms_over_sigma']:.1f} sigma")


if __name__ == "__main__":
    main()
