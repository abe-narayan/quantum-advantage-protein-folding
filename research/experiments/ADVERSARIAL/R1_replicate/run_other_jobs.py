"""R1 replicate, extension: apply the next rung of the sparse-Pauli ladder (eps = 3e-5, per-pair truncation; my PTM
engine) to OTHER stored N=10, gamma=0 C1 gate jobs, against the STORED exact F/S and STORED per-time echo FI of each
job.  Question: is the N=10 echo window (f_hard^OTOC 0.49-1.0) an artefact of the adversary panel stopping at 1e-4?

Geometry is rebuilt from the PDB exactly as scripts/nmr_gate.py does (hn-only -> backbone amide H only), then checked
against the stored cluster names.  ~2.7 CPU-min per job.
Usage: OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python run_other_jobs.py 1PGA_p325_N10_o0_g0 [...]
"""
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
from qapf.nmr.spins import read_h_coords  # noqa: E402  (geometry only)


def load_job(tag):
    d = "nmr_gate_hn" if "HN_" in tag else "nmr_gate"
    st = json.load(open(os.path.join(ROOT, "research", "results", "RAW", d, tag + ".json")))
    pdb = st["pdb"]
    names, xyz, resid = read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    if "HN_" in tag:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        names = [names[i] for i in keep]; xyz = xyz[keep]
    X = xyz[st["cluster"]]
    assert [names[i] for i in st["cluster"]] == st["cluster_names"], "cluster name mismatch"
    return st, X


def main():
    eps = 3e-5
    tags = []
    for x in sys.argv[1:]:
        if x.startswith("--eps="):
            eps = float(x.split("=", 1)[1])
        else:
            tags.append(x)
    for tag in tags:
        t0 = time.process_time()
        st, X = load_job(tag)
        bs = st["bs"]; b0 = np.asarray(st["b0"])
        dm = L.my_couplings(X, b0)
        rec = st["steps"] // (len(st["times"]) - 1)
        P = L.pauli_propagate(dm, st["dt"], st["steps"], rec, 0, bs, eps=eps, trunc="pair")
        nrm = np.maximum(np.asarray(P["norm2"]), 1e-12)
        bF = np.max([np.abs(np.asarray(P["F"][b]) - np.asarray(st["F_exact"][str(b)])) for b in bs], axis=0)
        bFn = np.max([np.abs(np.asarray(P["F"][b]) / nrm - np.asarray(st["F_exact"][str(b)])) for b in bs], axis=0)
        bS = np.max([np.abs(np.asarray(P["S"][b]) - np.asarray(st["S_exact"][str(b)])) for b in bs], axis=0)
        thr = st["thr"]; n = len(bF)
        ff = lambda x: int(np.nonzero(x > thr)[0][0]) if (x > thr).any() else n  # noqa: E731
        tcF, tcFn, tcS = ff(bF), ff(bFn), ff(bS)
        tco = max(tcF, tcFn)
        fh = {}
        for p in st["params"]:
            if "FI_otoc_t" not in p:
                continue
            fo = np.asarray(p["FI_otoc_t"])
            fh[p["name"]] = dict(frac_hard_otoc_stored_panel=float(fo[st["best_t_c_otoc_index"]:].sum() / fo.sum()),
                                 frac_hard_otoc_eps3e5=float(fo[tco:].sum() / fo.sum()))
        out = dict(tag=tag, eps=eps, stored_best_adversary_otoc=st["best_adversary_otoc"],
                   stored_best_t_c_otoc_index=st["best_t_c_otoc_index"], t_c_otoc_plain=tcF, t_c_otoc_normcorr=tcFn,
                   t_c_transfer=tcS, n_rec=n, max_bias_otoc=bF.tolist(), max_bias_otoc_normcorr=bFn.tolist(),
                   max_bias=bS.tolist(), n_strings=P["n_strings"], kept_norm2=P["norm2"],
                   frac_hard=fh, cpu_s=time.process_time() - t0)
        json.dump(out, open(os.path.join(HERE, f"other_{tag}_eps{eps:g}.json"), "w"), indent=0)
        print(json.dumps(dict(tag=tag, stored_tco=st["best_t_c_otoc_index"], tcF=tcF, tcFn=tcFn, tcS=tcS,
                              max_biasF=round(float(bF.max()), 4), max_str=max(P["n_strings"]),
                              fh={k: (round(v["frac_hard_otoc_stored_panel"], 2), round(v["frac_hard_otoc_eps3e5"], 2))
                                  for k, v in fh.items()}, cpu=round(out["cpu_s"]))), flush=True)


if __name__ == "__main__":
    main()
