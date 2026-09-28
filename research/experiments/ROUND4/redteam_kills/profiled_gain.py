"""ROUND4 red team (redteam_kills), test RT-A: PROFILED joint gain of the protein 1H echo with forward-model
nuisances included in the model (K-105 secular OTOC(1); K-109 physical double-quantum echo).

Question (pro-quantum): K-105's "load-bearing" arm (ROUND3/CRITIC C1) is the forward-model error of 5-66 sigma from
methyl rotation, 1 kHz site offsets and reversal mismatch (R1_physics_feasibility, MEASURED for the STATIC,
offset-free model).  A misspecification bias is not a limit if the omitted effects are put into the model as nuisance
parameters.  What survives is (a) the structural Fisher information after the nuisances are profiled out, and (b) its
value against the classically usable data.  This script builds the nuisance-complete forward model and its full
Jacobian so that analyze_profiled.py can compute profiled gains as a function of the (unknown) converged classical
reach time t_cl and of the reversal envelope.

Forward model (N = 10 cluster, same geometry/butterflies/params/dt as R1_amplify + dq_echo_envelope, job_geometry):
  couplings  D = rotor-AVERAGED secular couplings (fast 3-site jumps of every CH3/NH3 group whose protons are in
             the cluster, jump sites from the full protein; R1_physics_feasibility/scales.averaged_couplings) --
             i.e. the physically correct fast-limit model, not the static one the RAW data used;
             then D_ij *= (1+eps0) * (1+eps_g(i)) * (1+eps_g(j)) (g(i) = rotor group of i, eps = 0 for non-rotor);
             for i, j in the SAME group only one factor (1+eps_g).
  offsets    Omega_i Z_i / 2 added to every Trotter step (diagonal phase after the dipolar step);
             base Omega0 = 1 kHz RMS random (seed 3), exactly as R1_physics_feasibility test_nuisance.
  transfer   S_ab(t)  = 2^-N Tr[Z_a(t) Z_b]                 (forward only; no reversal)
  echo       G_ab(t)  = 2^-N Tr[Z_b W Z_a U Z_b U^dag Z_a W^dag], U = S^n, W = (S_eta^n)^dag, S_eta = step with
             D*(1+eta) (reversal scaling mismatch) and the same offsets.  eta = 0 gives F_ab of RAW.
  ham        'sec': H = sum d_ij (2IzIz - IxIx - IyIy) (qapf.nmr.spins fused-pair Trotter circuit, sectors)
             'dq' : physical DQ H = -sum d_ij (IxIx - IyIy) (amp_lib.dq_pair_terms s = 1, parity blocks).
             For 'dq', --kappa scales the offsets (kappa = 1: offsets fully present in the DQ frame, pessimistic;
             kappa = 0: offsets compensated to all orders by the pulse sequence, optimistic).
Parameters:  structural (job_geometry params; a parameter that moves a proton of a rotor group moves the WHOLE group,
             i.e. a rotor-axis displacement, named *_axis) + nuisances Omega_0..N-1 (kappa > 0), eta, eps0, eps_g.
Also:        misspecification draws: truth with per-PAIR order parameters S_ij ~ U[0.85, 1] (outside the nuisance
             family) -> y_true - y_base, for a linearised profiled-fit bias test.
Checkpoint:  out/pg_<ham>_k<kappa>_<pdb>_p<probe>.npz + .json after every column (atomic tmp+replace); resumes.
Usage:       OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python profiled_gain.py --ham sec --pdb 1UBQ --probe 19
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import math
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
AMP = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_amplify")
PHYS = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_physics_feasibility")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, AMP)
sys.path.insert(0, PHYS)
import amp_lib as L  # noqa: E402  (read-only reuse)
import scales as SC  # noqa: E402  (read-only reuse)
from qapf.nmr import spins as SP  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
DT = 2e-6
SIGMA = 0.01
H_FD = 0.05                  # A, structural FD step (same as C1 / R1_amplify)
H_OM = 2 * math.pi * 100.0   # rad/s, offset FD step (same as R1_physics_feasibility)
H_ETA = 0.01
H_EPS0 = 0.01
H_EPSG = 0.02


def _replace(tmp, path, tries=20):
    """os.replace with retries (Windows: a scanner/indexer can hold the target for a moment -> WinError 5)."""
    for k in range(tries):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.25 * (k + 1))
    os.replace(tmp, path)


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    _replace(tmp, path)


def atomic_npz(path, **arrs):
    tmp = path + ".tmp.npz"
    np.savez(tmp, **arrs)
    _replace(tmp, path)


# --------------------------------------------------------------------------------------------- geometry + rotors
def setup(pdb, probe, orient=0):
    g = L.job_geometry(pdb, probe, 10, orient, hn_only=False)
    pdbf = os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb")
    atoms = SC.read_all_atoms(pdbf)
    hk = [k for k, a in enumerate(atoms) if a[3] == "H"]
    groups, _ = SC.rotor_groups(atoms, {k: i for i, k in enumerate(hk)})
    assert len(hk) == len(g["xyz"]), "H ordering mismatch between scales and spins readers"
    idx = [int(i) for i in g["idx"]]
    gof = {}
    for gi, hl in enumerate(groups):
        for h in hl:
            gof[int(h)] = gi
    touched = sorted({gof[i] for i in idx if i in gof})
    sub = list(idx)
    for gi in touched:
        for h in groups[gi]:
            if int(h) not in sub:
                sub.append(int(h))
    pos = {h: k for k, h in enumerate(sub)}
    groups_local = [[pos[int(h)] for h in groups[gi]] for gi in touched]
    # cluster-local rotor-group label (-1 = none)
    lab = np.full(len(idx), -1, int)
    for li, gi in enumerate(touched):
        for k, i in enumerate(idx):
            if gof.get(i) == gi:
                lab[k] = li
    # structural parameters as moves on the SUB coordinate set (rotor protons move with their whole group)
    params = []
    for p in g["params"]:
        mv, axis = {}, False
        for (k, u) in p["move"]:
            i = idx[int(k)]
            if i in gof:
                axis = True
                for h in groups[gof[i]]:
                    mv[pos[int(h)]] = np.asarray(u, float)
            else:
                mv[pos[i]] = np.asarray(u, float)
        params.append(dict(name=p["name"] + ("_axis" if axis else ""), r=p["r"], move=mv))
    Xsub = np.asarray(g["xyz"])[sub].copy()
    names = [g["names"][i] for i in idx]
    return dict(g=g, idx=idx, sub=sub, groups_local=groups_local, lab=lab, params=params, Xsub=Xsub, b0=g["b0"],
                bs=list(g["bs"]), names=names, rotor_groups_in_cluster=[[g["names"][int(h)] for h in groups[gi]]
                                                                       for gi in touched])


def couplings(G, Xsub, eps0=0.0, epsg=None):
    N = len(G["idx"])
    Dsub = SC.averaged_couplings(Xsub, G["b0"], G["groups_local"]) if G["groups_local"] else SP.couplings(Xsub, G["b0"])
    D = Dsub[:N, :N].copy() * (1.0 + eps0)
    if epsg is not None and len(epsg):
        lab = G["lab"]
        f = np.ones(N)
        for k in range(N):
            if lab[k] >= 0:
                f[k] = 1.0 + epsg[lab[k]]
        F = np.outer(f, f)
        same = (lab[:, None] == lab[None, :]) & (lab[:, None] >= 0)
        F[same] = f[np.nonzero(same)[0]]
        D = D * F
    np.fill_diagonal(D, 0.0)
    return 0.5 * (D + D.T)


def moved(Xsub, p, sgn, h):
    X = Xsub.copy()
    for k, u in p["move"].items():
        X[k] = X[k] + sgn * h * u
    return X


# --------------------------------------------------------------------------------------------- dynamics
def _blocks(ham, D, offsets, kappa):
    N = len(D)
    out = []
    if ham == "sec":
        gen = SP.sector_step_unitaries(D, DT)
    else:
        pc = L.popcount(np.arange(1 << N))
        terms = L.dq_pair_terms(D, s=1.0)
        gen = ((idx, L.build_step_unitary_generic(N, terms, DT, idx))
               for idx in (np.nonzero(pc % 2 == par)[0] for par in (0, 1)))
    for idx, Uk in gen:
        if offsets is not None and kappa != 0.0:
            ph = np.zeros(len(idx))
            for i in range(N):
                ph += kappa * offsets[i] * (1.0 - 2.0 * ((idx >> i) & 1)) / 2.0
            Uk = np.exp(-1j * DT * ph)[:, None] * Uk
        Q, lam = SP._unitary_eig(Uk)
        out.append((idx, Q, lam))
    return out


def observe(ham, D, offsets, kappa, eta, steps, rec, bs, a=0):
    """Returns S (nt, nb), G (nt, nb).  eta = 0: fast path (G = F1); eta != 0: explicit mismatched echo."""
    N = len(D)
    times = list(range(0, steps + 1, rec))
    nt, nb = len(times), len(bs)
    S = np.zeros((nt, nb)); G = np.zeros((nt, nb))
    fw = _blocks(ham, D, offsets, kappa)
    bw = fw if eta == 0.0 else _blocks(ham, D * (1.0 + eta), offsets, kappa)
    za_full = SP.zsign(N, a)
    zb_full = [SP.zsign(N, b) for b in bs]
    for (idx, Q, lam), (_, Qb, lamb) in zip(fw, bw):
        Qh = Q.conj().T
        za = za_full[idx]
        zb = [z[idx] for z in zb_full]
        A = (Qh * za) @ Q
        lc = lam.conj()
        if eta != 0.0:
            Bq = [(Qh * z) @ Q for z in zb]
            Qbh = Qb.conj().T
        for ti, n_ in enumerate(times):
            ph = np.outer(lc ** n_, lam ** n_)
            Oc = Q @ (A * ph) @ Qh                              # U^-n Z_a U^n (computational block)
            dg = np.real(np.diag(Oc))
            if eta == 0.0:
                A2 = np.abs(Oc) ** 2
            else:
                Wm = (Qb * (lamb.conj() ** n_)[None, :]) @ Qbh   # W = (S_eta^n)^dag
                Wc = Wm.conj()
            for bi in range(nb):
                S[ti, bi] += float((dg * zb[bi]).sum())
                if eta == 0.0:
                    G[ti, bi] += float((zb[bi][:, None] * A2 * zb[bi][None, :]).sum())
                else:
                    M1 = Q @ (Bq[bi] * ph.T) @ Qh               # U^n Z_b U^-n
                    Am = za[:, None] * M1 * za[None, :]
                    dB2 = np.sum((Wm @ Am) * Wc, axis=1)        # diag(W Am W^dag)
                    G[ti, bi] += float(np.real(np.sum(zb[bi] * dB2)))
    Dd = float(1 << N)
    return np.array(times) * DT, S / Dd, G / Dd


# --------------------------------------------------------------------------------------------- driver
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--ham", default="sec", choices=["sec", "dq"])
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--kappa", type=float, default=1.0)
    ap.add_argument("--nmis", type=int, default=2, help="misspecification draws (per-pair order parameters)")
    ap.add_argument("--budget", type=float, default=1500.0, help="CPU-s budget for this invocation")
    a = ap.parse_args()
    t0 = time.process_time()
    steps = 160 if a.ham == "sec" else 150
    rec = 5
    G = setup(a.pdb, a.probe)
    N = len(G["idx"])
    ng = len(G["groups_local"])
    rng = np.random.default_rng(3)
    Om0 = 2 * math.pi * 1000.0 * rng.standard_normal(N)       # identical draw to R1_physics_feasibility
    tag = f"pg_{a.ham}_k{a.kappa:g}_{a.pdb}_p{a.probe}"
    fj, fn = os.path.join(OUT, tag + ".json"), os.path.join(OUT, tag + ".npz")
    meta = json.load(open(fj)) if os.path.exists(fj) else {}
    arr = dict(np.load(fn)) if os.path.exists(fn) else {}
    use_om = a.kappa != 0.0
    base_off = Om0 if use_om else None
    cols = [("struct", p["name"]) for p in G["params"]] + \
        ([("Omega", f"Omega_{i}") for i in range(N)] if use_om else []) + \
        [("eta", "eta"), ("eps0", "eps0")] + [("epsg", f"epsg_{j}") for j in range(ng)]
    meta.update(ham=a.ham, pdb=a.pdb, probe=a.probe, kappa=a.kappa, bs=G["bs"], names=G["names"],
                rotor_groups_in_cluster=G["rotor_groups_in_cluster"], cluster_rotor_label=G["lab"].tolist(),
                params=[dict(name=p["name"], r=p["r"]) for p in G["params"]], columns=[c[1] for c in cols],
                col_kinds=[c[0] for c in cols], sigma=SIGMA, dt=DT, steps=steps, rec=rec,
                fd=dict(h_struct=H_FD, h_omega=H_OM, h_eta=H_ETA, h_eps0=H_EPS0, h_epsg=H_EPSG),
                Omega0_hz=(Om0 / (2 * math.pi)).tolist() if use_om else None)
    meta.setdefault("cpu_s", 0.0)
    meta.setdefault("done", [])

    def save():
        meta["cpu_s_last"] = time.process_time() - t0
        atomic_npz(fn, **arr)
        atomic_json(meta, fj)

    def run(D, off=base_off, eta=0.0):
        return observe(a.ham, D, off, a.kappa, eta, steps, rec, G["bs"])

    D0 = couplings(G, G["Xsub"], 0.0, np.zeros(ng))
    if "S0" not in arr:
        te = time.process_time()
        tt, S0, G0 = run(D0)
        arr.update(times=tt, S0=S0, G0=G0)
        # validation 1: static couplings, no offsets, eta = 0 must reproduce the stored exact engine (amp_lib)
        Dst = SP.couplings(G["g"]["X0"], G["b0"])
        if a.ham == "sec":
            ref = L.exact_sector(Dst, DT, steps, 0, G["bs"], rec, want_F2=False, want_P=False)
        else:
            ref = L.exact_parity(N, L.dq_pair_terms(Dst, s=1.0), DT, steps, 0, G["bs"], rec, want_P=False)
        _, Sv, Gv = observe(a.ham, Dst, None, 0.0, 0.0, steps, rec, G["bs"])
        meta["validation_static_vs_amp_lib"] = dict(S=float(np.abs(Sv - ref["S"]).max()),
                                                     F1=float(np.abs(Gv - ref["F1"]).max()))
        # validation 2: explicit mismatched-echo path at eta -> 0 equals the fast path
        _, _, Ge = observe(a.ham, D0, base_off, a.kappa, 1e-12, steps, rec, G["bs"])
        meta["validation_eta_path_vs_fast"] = float(np.abs(Ge - G0).max())
        # model-error scale (what K-105's 5-66 sigma measures): static offset-free vs this base
        meta["base_vs_static_offsetfree_max_over_sigma"] = dict(S=float(np.abs(S0 - Sv).max() / SIGMA),
                                                                G=float(np.abs(G0 - Gv).max() / SIGMA))
        meta["cpu_base_s"] = time.process_time() - te
        save()
        print(json.dumps(dict(stage="base", **{k: meta[k] for k in ("validation_static_vs_amp_lib",
              "validation_eta_path_vs_fast", "base_vs_static_offsetfree_max_over_sigma", "cpu_base_s")})), flush=True)
    for kind, name in cols:
        if name in meta["done"]:
            continue
        if time.process_time() - t0 > a.budget:
            print("budget reached; resume later", flush=True)
            meta["cpu_s"] += time.process_time() - t0
            save()
            return
        te = time.process_time()
        if kind == "struct":
            p = next(q for q in G["params"] if q["name"] == name)
            rp = run(couplings(G, moved(G["Xsub"], p, +1, H_FD), 0.0, np.zeros(ng)))
            rm = run(couplings(G, moved(G["Xsub"], p, -1, H_FD), 0.0, np.zeros(ng)))
            h = H_FD
        elif kind == "Omega":
            i = int(name.split("_")[1])
            e = np.zeros(N); e[i] = H_OM
            rp = run(D0, off=Om0 + e); rm = run(D0, off=Om0 - e)
            h = H_OM
        elif kind == "eta":
            rp = run(D0, eta=+H_ETA); rm = run(D0, eta=-H_ETA)
            h = H_ETA
        elif kind == "eps0":
            rp = run(couplings(G, G["Xsub"], +H_EPS0, np.zeros(ng))); rm = run(couplings(G, G["Xsub"], -H_EPS0, np.zeros(ng)))
            h = H_EPS0
        else:
            j = int(name.split("_")[1])
            e = np.zeros(ng); e[j] = H_EPSG
            rp = run(couplings(G, G["Xsub"], 0.0, e)); rm = run(couplings(G, G["Xsub"], 0.0, -e))
            h = H_EPSG
        arr["dS_" + name] = (rp[1] - rm[1]) / (2 * h)
        arr["dG_" + name] = (rp[2] - rm[2]) / (2 * h)
        meta["done"].append(name)
        save()
        print(json.dumps(dict(col=name, cpu=round(time.process_time() - te, 1))), flush=True)
    # misspecification draws: per-pair order parameters outside the nuisance family
    mis = meta.setdefault("mis_seeds", [])
    for s in range(a.nmis):
        seed = 100 + s
        if seed in mis:
            continue
        if time.process_time() - t0 > a.budget:
            break
        r2 = np.random.default_rng(seed)
        Sij = r2.uniform(0.85, 1.0, size=(N, N)); Sij = np.triu(Sij, 1); Sij = Sij + Sij.T
        rt = run(D0 * Sij)
        arr[f"misS_{seed}"] = rt[1] - arr["S0"]
        arr[f"misG_{seed}"] = rt[2] - arr["G0"]
        mis.append(seed)
        save()
        print(json.dumps(dict(mis=seed)), flush=True)
    meta["cpu_s"] += time.process_time() - t0
    meta["complete"] = all(c[1] in meta["done"] for c in cols) and len(mis) >= a.nmis
    save()
    print(json.dumps(dict(tag=tag, complete=meta["complete"], cpu_total=round(meta["cpu_s"], 1))), flush=True)


if __name__ == "__main__":
    main()
