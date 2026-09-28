"""ROUND3 / hardness_what_it_takes: calibration of the energy threshold (how much of an energy gap is just incomplete
200-iteration L-BFGS relaxation?).  Native-free.

For every crop in dg_results_A.json: take the DG-E1 minimum endpoint and polish it with +800 further L-BFGS iterations
(same routine), recording the energy drop and the extra gradient evaluations.  On the crops that also have NRPT runs,
do the same for NRPT's polished lowest-energy T=1 structure (symmetric treatment), and record the CA-RMSD between the
two polished structures (basin identity, native-free).  Checkpoints after each crop (atomic tmp + replace).

Usage: OMP_NUM_THREADS=1 python polish_check.py -> polish_results.json
"""
from __future__ import annotations

import glob
import json
import os
import sys
import time

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS", "NUMEXPR_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import numpy as np  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(REPO, "src"))
from qapf.protein import energy as EN  # noqa: E402

EXTRA = 800


def kabsch_rmsd(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B)
    S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S.sum(), 0) / len(A)))


def main():
    out = os.path.join(HERE, "polish_results.json")
    res = json.load(open(out)) if os.path.exists(out) else []
    done = {r["crop"] for r in res}
    dg = json.load(open(os.path.join(HERE, "dg_results_A.json")))
    t_start = time.time()
    for r in dg:
        crop, L = r["crop"], r["L"]
        if crop in done:
            continue
        if time.time() - t_start > 480:
            print("time budget reached", flush=True); break
        z = np.load(os.path.join(REPO, "data", "instruments", "ladder", crop + ".npz"))
        en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
        ep = np.load(os.path.join(HERE, "endpoints", crop + ".npz"))
        arms = ep["arms"]; E = ep["E"]
        i = np.where(arms == "DG-E1")[0][np.argmin(E[arms == "DG-E1"])]
        g0 = en.n_grad; t = time.time()
        xp, Ep = EN.relax(en, ep["x"][i:i + 1], iters=EXTRA)
        row = dict(crop=crop, L=L, E_DG_E1_200=float(E[i]), E_DG_E1_polished=float(np.asarray(Ep).ravel()[0]),
                   extra_evals_DG=int(en.n_grad - g0), secs_DG=time.time() - t)
        Xdg = en.coords(xp)[0]
        # symmetric treatment of NRPT T=1 polished structures (pilot s0 and tscan s1), if present
        pts = []
        for f in sorted(glob.glob(os.path.join(REPO, "research", "results", "RAW", "g1_*", f"{crop}_T1_s*.npz"))):
            zz = np.load(f)
            S = zz["samples"]; S = S[len(S) // 5:]
            Es = en(S, grad=False)[0]
            k = int(np.argmin(Es))
            x1, E1 = EN.relax(en, S[k:k + 1], iters=200)
            g0 = en.n_grad
            x2, E2 = EN.relax(en, x1, iters=EXTRA)
            pts.append(dict(file=os.path.relpath(f, REPO), E_pt_200=float(np.asarray(E1).ravel()[0]),
                            E_pt_polished=float(np.asarray(E2).ravel()[0]), extra_evals=int(en.n_grad - g0),
                            rmsd_polishedDG_vs_polishedPT=kabsch_rmsd(Xdg, en.coords(x2)[0])))
        row["nrpt_T1"] = pts
        res.append(row)
        tmp = out + ".tmp"
        json.dump(res, open(tmp, "w"), indent=1)
        os.replace(tmp, out)
        print(json.dumps({k: (round(v, 1) if isinstance(v, float) else v) for k, v in row.items() if k != "nrpt_T1"}),
              [(round(p["E_pt_200"], 1), round(p["E_pt_polished"], 1), round(p["rmsd_polishedDG_vs_polishedPT"], 2)) for p in pts],
              flush=True)


if __name__ == "__main__":
    main()
