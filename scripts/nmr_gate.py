"""Program C gate (discovery cards P1/P2/P3): is there Fisher information about protein geometry that lives ONLY in the
part of the NMR spin dynamics that the best classical approximation cannot reproduce?

One job = one (protein, probe proton, cluster size N, B0 orientation, dephasing gamma).
  1. Cluster: N protons nearest the probe a (OpenMM hydrogens on PDB structures in data/instruments/nmr).
  2. Parameters phi_k: radial displacement (+-h along the a->k direction) of each of the K most distant cluster
     protons (the "long-range geometry" the S33 program found missing), plus one rigid shift of all cluster protons of
     the residue of the farthest proton whose residue differs from the probe's residue.
  3. Exact model: v2 default = deterministic sector-exact (total-Z blocks; qapf.nmr.spins.sector_exact_correlators;
     validated to 1e-14 against the dense Heisenberg matrix); 'typ' = statevector typicality (for N > 14).
  4. Classical adversaries (all through the SAME Trotter circuit where applicable):
     (a) Heisenberg Pauli propagation truncated at weight <= w;
     (b) sparse Pauli dynamics: coefficient-threshold truncation |c| < eps, no weight cap (Begusic-Chan-style);
     (c) classical-spin dynamics (Elsayed-Fine 2015), continuous time, RK4;
     (d) exact simulation of a sub-cluster of n_c < N spins containing the probe and all observed spins
         (cluster truncation, CCE-like).
     The best adversary (latest failure time) defines t_c*.
  5. Fisher information with white noise sigma per time point:  FI = sum_t (d s/d phi)^2 / sigma^2 (exact model),
     t_c(m) = first recorded time the model-m signal deviates from exact by > thr = max(sigma, 3 SE_typ) (bias),
     FI_hard(m) = information carried by time points t >= t_c(m), FI_easy(m) = the rest,
     gain G = FI_total / FI_easy(best) = factor in measurement repetitions a quantum forward model would save if the
     classical model must discard t >= t_c*.
v2 change log: rigid-shift parameter no longer can move the probe's own residue (v1 moved the probe's geminal partner,
unphysical, FI ~ 1e6); deterministic reference; noise-aware threshold; four adversaries; FI_easy and gain.
Output JSON per job under research/results/RAW/nmr_gate/.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "src"))
from qapf.nmr import spins as SP  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def _np(o):
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    raise TypeError(type(o))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True, help="index of the probe proton in the H list")
    ap.add_argument("--N", type=int, default=14)
    ap.add_argument("--orient", type=int, default=0)
    ap.add_argument("--gamma", type=float, default=0.0, help="dephasing rate (1/s)")
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--nt", type=int, default=16, help="recorded time points")
    ap.add_argument("--K", type=int, default=3, help="number of distant protons perturbed")
    ap.add_argument("--h", type=float, default=0.05, help="finite-difference displacement (A)")
    ap.add_argument("--sigma", type=float, default=0.01)
    ap.add_argument("--nrand", type=int, default=4)
    ap.add_argument("--otoc", type=int, default=-1, help="-1 auto (N <= 12 and gamma = 0)")
    ap.add_argument("--wlist", default="2,3,4,5")
    ap.add_argument("--epslist", default="1e-3,1e-4")
    ap.add_argument("--sublist", default="-4,-2", help="sub-cluster sizes relative to N")
    ap.add_argument("--cspin", type=int, default=40000, help="classical-spin samples (0 = off)")
    ap.add_argument("--own-fi", type=int, default=-1, help="adversary's own FI via FD: -1 auto (N <= 10), 0, 1")
    ap.add_argument("--max-strings", type=int, default=3_000_000)
    ap.add_argument("--exact", default="auto", help="sector (deterministic) | typ | matrix (alias of sector) | auto")
    ap.add_argument("--out", default=os.path.join(ROOT, "research", "results", "RAW", "nmr_gate"))
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    tag = f"{a.pdb}_p{a.probe}_N{a.N}_o{a.orient}_g{int(a.gamma)}"
    fj = os.path.join(a.out, tag + ".json")
    if os.path.exists(fj):
        print("exists"); return
    t0 = time.time()
    names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    idx = SP.cluster(xyz, a.probe, a.N)
    X0 = xyz[idx].copy()
    b0 = random_b0(1000 + a.orient)
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:a.K]]            # cluster-local indices of the most distant protons
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))        # observe transfer to the perturbed protons + nearest
    rec = max(1, a.steps // a.nt)
    params = []
    for k in far:
        u = (X0[k] - X0[0]) / dist[k]
        params.append(dict(name=f"radial_{names[idx[k]]}", move=[(int(k), u.tolist())], r=float(dist[k])))
    pres = resid[idx[0]]
    # farthest proton whose residue differs from the probe's AND has >= 2 protons in the cluster (a rigid shift of a
    # single proton would duplicate a radial parameter)
    cnt = {}
    for i in range(a.N):
        cnt[resid[idx[i]]] = cnt.get(resid[idx[i]], 0) + 1
    kfar = next((int(k) for k in np.argsort(-dist) if resid[idx[k]] != pres and cnt[resid[idx[k]]] >= 2), None)
    if kfar is not None:
        kres = resid[idx[kfar]]
        grp = [int(i) for i in range(a.N) if resid[idx[i]] == kres]
        ug = (X0[kfar] - X0[0]) / dist[kfar]
        params.append(dict(name=f"rigid_res{kres}", move=[(i, ug.tolist()) for i in grp], r=float(dist[kfar]),
                           n_moved=len(grp)))

    def geom(p, sgn):
        X = X0.copy()
        for (i, u) in p["move"]:
            X[i] = X[i] + sgn * a.h * np.asarray(u)
        return X

    mode = "sector" if a.exact == "matrix" else a.exact
    if mode == "auto":
        mode = "sector" if a.N <= 14 else "typ"
    do_otoc = (a.otoc == 1) or (a.otoc == -1 and a.N <= 12 and a.gamma == 0)

    def run_exact(X, seed, otoc=False):
        dm = SP.couplings(X, b0)
        if mode == "sector":
            return SP.sector_exact_correlators(dm, a.dt, a.steps, 0, bs, gamma=a.gamma, record_every=rec, otoc=otoc)
        tt_, S_, _, F_ = SP.exact_correlators(dm, a.dt, a.steps, 0, bs, n_rand=a.nrand, gamma=a.gamma,
                                              rng=np.random.default_rng(seed), otoc=otoc and a.gamma == 0,
                                              record_every=rec, otoc_every=rec)
        return tt_, S_, F_

    se_typ = 0.0 if mode == "sector" else 2 ** (-a.N / 2) / math.sqrt(a.nrand)
    thr = max(a.sigma, 3 * se_typ)
    te = time.time()
    tt, S0, F0 = run_exact(X0, 7, otoc=do_otoc)
    res = dict(version=2, pdb=a.pdb, probe=a.probe, probe_name=names[a.probe], N=a.N, orient=a.orient, b0=b0.tolist(),
               exact_mode=mode, gamma=a.gamma, dt=a.dt, steps=a.steps, sigma=a.sigma, h=a.h, nrand=a.nrand, thr=thr,
               bs=bs, names_bs=[names[idx[b]] for b in bs], dist_bs=[float(dist[b]) for b in bs], times=tt.tolist(),
               cluster=[int(i) for i in idx], cluster_names=[names[i] for i in idx],
               S_exact={str(b): S0[b].tolist() for b in bs},
               F_exact={str(b): F0[b].tolist() for b in bs} if F0 else None, params=[], adversaries={})
    for p in params:
        _, Sp, Fp = run_exact(geom(p, +1), 11, otoc=do_otoc)
        _, Sm, Fm = run_exact(geom(p, -1), 11, otoc=do_otoc)
        d = {b: (Sp[b] - Sm[b]) / (2 * a.h) for b in bs}
        fi_t = sum(d[b] ** 2 for b in bs) / a.sigma ** 2      # per time point FI (sum over observed b)
        pr_ = dict(name=p["name"], r=p["r"], n_moved=p.get("n_moved", 1), FI_total=float(fi_t.sum()),
                   FI_t=fi_t.tolist(), dS={str(b): d[b].tolist() for b in bs})
        if do_otoc and Fp:                                     # OTOC (echo) observables: F_ab(t), same noise model
            dF = {b: (Fp[b] - Fm[b]) / (2 * a.h) for b in bs}
            fo_t = sum(dF[b] ** 2 for b in bs) / a.sigma ** 2
            pr_.update(FI_otoc_total=float(fo_t.sum()), FI_otoc_t=fo_t.tolist(), dF={str(b): dF[b].tolist() for b in bs})
        res["params"].append(pr_)
    res["secs_exact"] = time.time() - te
    print(json.dumps({"exact_secs": round(res["secs_exact"], 1), "mode": mode}), flush=True)

    own_default = (a.own_fi == 1) or (a.own_fi == -1 and a.N <= 10)

    def evaluate(label, runner, own_fi=None):
        own_fi = own_default if own_fi is None else own_fi
        tw = time.time()
        out = runner(X0)
        Sw = out[0]
        Fw = out[1].pop("_F", None) if len(out) > 1 else None
        bias = np.max(np.stack([np.abs(Sw[b] - S0[b]) for b in bs]), axis=0)
        bad = np.nonzero(bias > thr)[0]
        tc = int(bad[0]) if len(bad) else len(tt)
        fr = {}
        for pr in res["params"]:
            fi_t = np.asarray(pr["FI_t"])
            tot = max(fi_t.sum(), 1e-30)
            fr[pr["name"]] = dict(FI_hard=float(fi_t[tc:].sum()), FI_easy=float(fi_t[:tc].sum()),
                                  frac_hard=float(fi_t[tc:].sum() / tot))
        own = {}
        if own_fi:                                             # the adversary's OWN sensitivity (is it informative?)
            for p in params:
                Sp = runner(geom(p, +1))[0]
                Sm = runner(geom(p, -1))[0]
                dw = sum(((Sp[b] - Sm[b]) / (2 * a.h)) ** 2 for b in bs) / a.sigma ** 2
                own[p["name"]] = np.asarray(dw).tolist()
        rec_ = dict(t_c_index=tc, t_c=float(tt[tc]) if tc < len(tt) else None, max_bias=bias.tolist(), FI_split=fr,
                    FI_own_t=own, secs=time.time() - tw)
        if Fw is not None and F0:
            def _tc(Fx):
                bo_ = np.max(np.stack([np.abs(np.asarray(Fx[b]) - F0[b]) for b in bs]), axis=0)
                bad_ = np.nonzero(bo_ > thr)[0]
                return (int(bad_[0]) if len(bad_) else len(tt)), bo_
            tco, bo = _tc(Fw)
            est = "plain"
            nk = rec_.get("kept_norm2") or (out[1].get("kept_norm2") if len(out) > 1 else None)
            if nk is not None and a.gamma == 0:            # norm-corrected estimator (C3), adversary's choice
                nk = np.maximum(np.asarray(nk, float), 1e-12)
                tcc, boc = _tc({b: np.asarray(Fw[b]) / nk for b in bs})
                rec_.update(t_c_otoc_index_plain=tco, t_c_otoc_index_normcorr=tcc, max_bias_otoc_normcorr=boc.tolist())
                if tcc > tco:
                    tco, bo, est = tcc, boc, "normcorr"
            rec_.update(t_c_otoc_index=tco, max_bias_otoc=bo.tolist(), otoc_estimator=est,
                        FI_split_otoc={pr["name"]: dict(frac_hard=float(np.sum(pr["FI_otoc_t"][tco:]) /
                                                                         max(pr["FI_otoc_total"], 1e-30)))
                                       for pr in res["params"] if "FI_otoc_t" in pr})
        if len(out) > 1:
            rec_.update(out[1])
        res["adversaries"][label] = rec_
        print(json.dumps({"adv": label, "t_c_index": tc, "secs": round(rec_["secs"], 1)}), flush=True)

    def pauli_runner(w, eps):
        def r(X):
            dm = SP.couplings(X, b0)
            _, Sw, Fw, nstr, norm2 = SP.pauli_correlators(dm, a.dt, a.steps, 0, bs, wmax=w, eps=eps, gamma=a.gamma,
                                                         record_every=rec, max_strings=a.max_strings)
            return Sw, dict(n_strings=np.asarray(nstr).tolist(), kept_norm2=np.asarray(norm2).tolist(), _F=Fw)
        return r

    for w in [int(v) for v in a.wlist.split(",") if v]:
        evaluate(f"pauli_w{w}", pauli_runner(w, 1e-9), own_fi=(w == 4 and own_default))
    for e in [float(v) for v in a.epslist.split(",") if v]:
        evaluate(f"pauli_eps{e:g}", pauli_runner(None, e), own_fi=False)
    for rel in [int(v) for v in a.sublist.split(",") if v]:
        nc = a.N + rel
        if nc < len(bs) + 2:
            continue
        others = [int(k) for k in np.argsort(dist) if k != 0 and k not in bs]
        sub = [0] + bs + others[:nc - 1 - len(bs)]
        sub_bs = [sub.index(b) for b in bs]

        def sub_runner(X, sub=sub, sub_bs=sub_bs, nc=nc):
            dm = SP.couplings(X[sub], b0)
            _, Ss, Fs = SP.sector_exact_correlators(dm, a.dt, a.steps, 0, sub_bs, gamma=a.gamma, record_every=rec,
                                                    otoc=do_otoc)
            return {b: Ss[sb] for b, sb in zip(bs, sub_bs)}, dict(n_c=nc, _F=({b: Fs[sb] for b, sb in zip(bs, sub_bs)}
                                                                           if Fs else None))
        evaluate(f"sub_n{nc}", sub_runner, own_fi=True)
    if a.cspin > 0:
        def cs_runner(X):
            dm = SP.couplings(X, b0)
            _, Sc = SP.classical_spin_correlators(dm, a.dt, a.steps, 0, bs, n_samples=a.cspin, record_every=rec,
                                                  gamma=a.gamma, rng=np.random.default_rng(123))
            return Sc, dict(n_samples=a.cspin)
        evaluate("cspin", cs_runner, own_fi=False)
    # best classical adversary = latest failure time
    if res["adversaries"]:
        best = max(res["adversaries"], key=lambda k: res["adversaries"][k]["t_c_index"])
        tc = res["adversaries"][best]["t_c_index"]
        res["best_adversary"] = best
        res["best_t_c_index"] = tc
        res["best_split"] = {p["name"]: dict(frac_hard=float(np.sum(p["FI_t"][tc:]) / max(p["FI_total"], 1e-30)),
                                             gain=float(p["FI_total"] / max(np.sum(p["FI_t"][:tc]), 1e-30)))
                             for p in res["params"]}
        oadv = [k for k, v in res["adversaries"].items() if "t_c_otoc_index" in v]
        if oadv:
            bo = max(oadv, key=lambda k: res["adversaries"][k]["t_c_otoc_index"])
            tco = res["adversaries"][bo]["t_c_otoc_index"]
            res["best_adversary_otoc"] = bo
            res["best_t_c_otoc_index"] = tco
            res["best_split_otoc"] = {p["name"]: dict(frac_hard=float(np.sum(p["FI_otoc_t"][tco:]) / max(p["FI_otoc_total"], 1e-30)),
                                                      gain=float(p["FI_otoc_total"] / max(np.sum(p["FI_otoc_t"][:tco]), 1e-30)))
                                      for p in res["params"] if "FI_otoc_t" in p}
    res["secs"] = time.time() - t0
    tmp = fj + ".tmp"
    json.dump(res, open(tmp, "w"), default=_np)
    os.replace(tmp, fj)
    print(json.dumps({"tag": tag, "secs": round(res["secs"]), "best": res.get("best_adversary"),
                      "params": [(p["name"], round(p["FI_total"], 1)) for p in res["params"]],
                      "tc": {k: v["t_c_index"] for k, v in res["adversaries"].items()}}))


if __name__ == "__main__":
    main()
