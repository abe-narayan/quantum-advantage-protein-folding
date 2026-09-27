"""R1 amplify, test A/B: do richer echo observables (multi-site butterflies, subset coherence-order spectra, second-order
OTOC) or a pulse-engineered double-quantum Hamiltonian strengthen the classically-hard echo window?

One job = (protein, probe, N, orientation, network, Hamiltonian).  Same cluster, parameters, FD step h, sigma, time grid
and Trotter circuit as scripts/nmr_gate.py (C1 v2).
  exact     : amp_lib.exact_sector (secular) or amp_lib.exact_parity (dq) for base and +-h geometries of each parameter.
  adversary : (a) sparse Pauli dynamics |c| > eps (plain / norm-corrected / total-Z-projected estimators; the adversary
              takes the best per family) run to --pauli-max-steps under --budget seconds;
              (b) exact sub-cluster simulation (n_c in --subs): probe + observed spins + nearest others.
  Per family: bias vs exact at the base geometry -> failure index t_c (first recorded time with max |bias| > sigma),
  best adversary = latest t_c (censored if the adversary run stopped before failing).  Fisher matrix from the exact
  FD Jacobian (sigma per scalar per time point), FI_hard (t >= t_c), frac_hard, and the quantum-only gain
     g_par  = CRB_cl^2 / CRB_q^2 per parameter, classical route = transfer S (all t; MEASURED classically reproducible
              at N=10 by sparse Pauli, C1) + family (t < t_c);  quantum route = S (all t) + family (all t);
     g_max  = largest generalised eigenvalue of (F_q, F_cl).
Output: out/<tag>.json.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import amp_lib as L  # noqa: E402


def _pad(x, n):
    x = np.asarray(x)
    return x if x.shape[1] >= n else np.concatenate([x, np.zeros((x.shape[0], n - x.shape[1]))], axis=1)


def families(obs, nS, ham, n_mq=None):
    """observable dict (times x ...) -> dict family -> array (nt, n_scalars).  MQC_tot padded to n_mq orders
    (a sub-cluster has fewer coherence orders)."""
    der = L.derived_from_pdelta(obs["P"], nS)
    fam = dict(S=obs["S"], F1=obs["F1"], F1_multi=der["F1_multi"], MQC_S=der["MQC"])
    if obs.get("F2") is not None:
        fam["F2"] = obs["F2"]
    if obs.get("MQC_tot") is not None:
        fam["MQC_tot"] = obs["MQC_tot"][:, 1:]
    if obs.get("MQ") is not None:
        fam["MQC_tot"] = obs["MQ"][:, 1:]
    if "MQC_tot" in fam and n_mq:
        fam["MQC_tot"] = _pad(fam["MQC_tot"], n_mq)
    return fam


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--N", type=int, default=10)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--hn", type=int, default=0)
    ap.add_argument("--ham", default="secular", choices=["secular", "dq"])
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--nt", type=int, default=16)
    ap.add_argument("--h", type=float, default=0.05)
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--eps", type=float, default=1e-4)
    ap.add_argument("--eps-list", default="", help="comma list; overrides --eps (one Pauli adversary per eps)")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--pauli-max-steps", type=int, default=110)
    ap.add_argument("--budget", type=float, default=360.0)
    ap.add_argument("--subs", default="8,9")
    ap.add_argument("--f2", type=int, default=1)
    a = ap.parse_args()
    t0 = time.time()
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    tag = f"obs_{a.pdb}{'HN' if a.hn else ''}_p{a.probe}_N{a.N}_o{a.orient}_{a.ham}{a.suffix}"
    g = L.job_geometry(a.pdb, a.probe, a.N, a.orient, hn_only=bool(a.hn))
    bs = g["bs"]; nS = len(bs)
    rec = max(1, a.steps // a.nt)
    want_f2 = bool(a.f2) and a.ham == "secular"

    def run_exact(X, nspin=None, sub_bs=None):
        dm = L.SP.couplings(X, g["b0"])
        bb = bs if sub_bs is None else sub_bs
        if a.ham == "secular":
            return L.exact_sector(dm, a.dt, a.steps, 0, bb, rec, want_F2=want_f2)
        return L.exact_parity(len(X), L.dq_pair_terms(dm), a.dt, a.steps, 0, bb, rec, want_F2=False)

    te = time.time()
    base = run_exact(g["X0"])
    fam0 = families(base, nS, a.ham)
    tt = base["times"]
    jac = {k: [] for k in fam0}
    for p in g["params"]:
        op_ = run_exact(L.displaced(g["X0"], p, +1, a.h))
        om_ = run_exact(L.displaced(g["X0"], p, -1, a.h))
        fp, fm = families(op_, nS, a.ham), families(om_, nS, a.ham)
        for k in fam0:
            jac[k].append((fp[k] - fm[k]) / (2 * a.h))          # (nt, n_scalars)
    secs_exact = time.time() - te
    print(json.dumps({"tag": tag, "exact_secs": round(secs_exact, 1)}), flush=True)

    # ---------------------------------------------------------------- adversaries on the base geometry
    adv = {}
    dm0 = L.SP.couplings(g["X0"], g["b0"])
    seq = L.secular_gate_seq(dm0, a.dt) if a.ham == "secular" else L.dq_gate_seq(dm0, a.dt)
    ta = time.time()
    adv_meta = dict()
    for eps_ in ([float(v) for v in a.eps_list.split(",") if v] or [a.eps]):
      pr, st = L.pauli_run(a.N, seq, a.steps, 0, bs, rec, eps=eps_, time_budget_s=a.budget,
                           max_steps=a.pauli_max_steps, want_F2=want_f2, want_MQtot=(a.ham == "dq"),
                           proj_kind=("z" if a.ham == "secular" else "parity"))
      n_rec = len(st["steps"])
      n2 = np.asarray(st["norm2"])
      plain = families(dict(S=pr["plain"]["S"], F1=pr["plain"]["F1"], F2=pr["plain"]["F2"], P=pr["plain"]["P"],
                            MQ=pr["plain"]["MQ"]), nS, a.ham)
      proj = families(dict(S=pr["proj"]["S"], F1=pr["proj"]["F1"], F2=pr["proj"]["F2"], P=pr["proj"]["P"],
                           MQ=pr["proj"]["MQ"]), nS, a.ham)
      # norm-corrected estimator = plain rescaled by the kept norm (degree of each observable in O)
      deg = dict(S=1, F1=2, F1_multi=2, MQC_S=2, F2=4, MQC_tot=2)
      normc = {k: v / (n2[:, None] ** (deg[k] / 2.0)) for k, v in plain.items()}
      for lab, fam in ((f"pauli_eps{eps_:g}_plain", plain), (f"pauli_eps{eps_:g}_normcorr", normc),
                       (f"pauli_eps{eps_:g}_proj", proj)):
          adv[lab] = dict(n_rec=n_rec, censored_after_index=n_rec,
                          bias={k: np.max(np.abs(fam[k] - fam0[k][:n_rec]), axis=1) for k in fam0})
      adv_meta[f"pauli_eps{eps_:g}"] = dict(secs=st["secs"], n_strings=st["n_strings"], norm2=st["norm2"],
                                             last_step=st["last_step"], steps=st["steps"])
      print(json.dumps({"pauli_secs": round(st["secs"], 1), "n_rec": n_rec, "strings": st["n_strings"][-1]}), flush=True)
    for nc in [int(v) for v in a.subs.split(",") if v]:
        if nc >= a.N:
            continue
        others = [int(k) for k in np.argsort(g["dist"]) if k != 0 and k not in bs]
        sub = [0] + bs + others[:nc - 1 - nS]
        sub_bs = [sub.index(b) for b in bs]
        so = run_exact(g["X0"][sub], sub_bs=sub_bs)
        fs = families(so, nS, a.ham, n_mq=a.N)
        adv[f"sub_n{nc}"] = dict(n_rec=len(tt), censored_after_index=len(tt),
                                 bias={k: np.max(np.abs(fs[k] - fam0[k]), axis=1) for k in fam0})
    secs_adv = time.time() - ta

    # ---------------------------------------------------------------- per-family failure and Fisher analysis
    nt = len(tt)
    res = dict(tag=tag, pdb=a.pdb, probe=a.probe, N=a.N, orient=a.orient, hn=a.hn, ham=a.ham, dt=a.dt, steps=a.steps,
               rec=rec, sigma=a.sigma, h=a.h, eps=a.eps, bs=bs, names_bs=[g["names"][g["idx"][b]] for b in bs],
               params=[dict(name=p["name"], r=p["r"]) for p in g["params"]], times_us=(tt * 1e6).tolist(),
               secs_exact=secs_exact, secs_adv=secs_adv, adv_meta=adv_meta, families={})
    for k in fam0:
        J = np.stack(jac[k])                                   # (np, nt, ns)
        ns = J.shape[2]
        tc_by = {}
        for lab, v in adv.items():
            b = v["bias"][k]
            tc = L.first_fail(b, a.sigma)
            tc_by[lab] = dict(t_c_index=tc, censored=(tc == len(b) and len(b) < nt), max_bias=b)
        best = max(tc_by, key=lambda x: tc_by[x]["t_c_index"])
        tcb = tc_by[best]["t_c_index"]
        fi_t = (J ** 2).sum(axis=(0, 2)) / a.sigma ** 2      # per time point, summed over params and scalars
        Ffull = L.fisher(J.reshape(len(J), -1), a.sigma)
        Fhard = L.fisher(J[:, tcb:, :].reshape(len(J), -1), a.sigma)
        res["families"][k] = dict(n_scalars=ns, t_c=tc_by, best_adversary=best, best_t_c_index=int(tcb),
                                  best_t_c_us=(float(tt[tcb] * 1e6) if tcb < nt else None),
                                  best_censored=bool(tc_by[best]["censored"]),
                                  FI_trace=float(np.trace(Ffull)), FI_hard_trace=float(np.trace(Fhard)),
                                  frac_hard=float(np.trace(Fhard) / max(np.trace(Ffull), 1e-300)),
                                  FI_per_scalar=float(np.trace(Ffull) / ns),
                                  FI_hard_per_scalar=float(np.trace(Fhard) / ns),
                                  FI_t=fi_t, signal=fam0[k], dsig=J)
    # gains: classical route = S(all) + X(t < t_c,X); quantum = S(all) + X(all)
    JS = np.stack(jac["S"]).reshape(len(g["params"]), -1)
    FS = L.fisher(JS, a.sigma)
    for k in fam0:
        if k == "S":
            continue
        J = np.stack(jac[k]); tcb = res["families"][k]["best_t_c_index"]
        Fq = FS + L.fisher(J.reshape(len(J), -1), a.sigma)
        Fc = FS + L.fisher(J[:, :tcb, :].reshape(len(J), -1), a.sigma)
        cq, cc = L.crb(Fq), L.crb(Fc)
        ge = L.gen_eigs(Fq, Fc)
        res["families"][k].update(CRB_q=cq, CRB_cl=cc, g_par=(cc / np.maximum(cq, 1e-300)) ** 2, g_max=float(ge.max()))
    # combined designs
    combos = {"F1": ["F1"], "F1+F1_multi": ["F1", "F1_multi"], "F1+MQC_S": ["F1", "MQC_S"],
              "F1+F1_multi+MQC_S": ["F1", "F1_multi", "MQC_S"]}
    if "F2" in fam0:
        combos.update({"F1+F2": ["F1", "F2"], "all": ["F1", "F1_multi", "MQC_S", "F2"]})
    if "MQC_tot" in fam0:
        combos.update({"F1+MQC_tot": ["F1", "MQC_tot"], "all": ["F1", "F1_multi", "MQC_S", "MQC_tot"]})
    res["combos"] = {}
    for cname, ks in combos.items():
        Fq, Fc = FS.copy(), FS.copy()
        for k in ks:
            J = np.stack(jac[k]); tcb = res["families"][k]["best_t_c_index"]
            Fq += L.fisher(J.reshape(len(J), -1), a.sigma)
            Fc += L.fisher(J[:, :tcb, :].reshape(len(J), -1), a.sigma)
        cq, cc = L.crb(Fq), L.crb(Fc)
        res["combos"][cname] = dict(CRB_q=cq, CRB_cl=cc, g_par=(cc / np.maximum(cq, 1e-300)) ** 2,
                                    g_par_median=float(np.median((cc / np.maximum(cq, 1e-300)) ** 2)),
                                    g_max=float(L.gen_eigs(Fq, Fc).max()),
                                    n_scalars=int(sum(res["families"][k]["n_scalars"] for k in ks)))
    res["secs"] = time.time() - t0
    json.dump(L.jsonable(res), open(os.path.join(HERE, "out", tag + ".json"), "w"))
    summ = {k: dict(tc=v["best_t_c_index"], cens=v["best_censored"], best=v["best_adversary"],
                    FIps=round(v["FI_per_scalar"]), FIhps=round(v["FI_hard_per_scalar"]), fh=round(v["frac_hard"], 3),
                    gmed=(round(float(np.median(v["g_par"])), 2) if "g_par" in v else None))
            for k, v in res["families"].items()}
    print(json.dumps(dict(tag=tag, secs=round(res["secs"]), fam=summ,
                          combos={k: (round(v["g_par_median"], 2), round(v["g_max"], 1)) for k, v in res["combos"].items()})),
          flush=True)


if __name__ == "__main__":
    main()
