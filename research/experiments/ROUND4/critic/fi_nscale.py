"""ROUND4 completeness critic, check CR4-B: does the load-bearing K-105 (and K-109) value arm depend on the N = 10
Fisher model's missing butterfly partners?

Round 4's central lesson (C-R4-1, K-120) is that a probe-centred cluster that omits a butterfly site's dominant dipolar
partner can be 2.5-7 sigma off at that site.  The red team's re-based K-105 arm (profiled median gain g <= 1.6 under the
site-resolved PE envelope, even at t_cl = 0) and K-109's value numbers are computed on the SAME probe-centred N = 10
clusters (amp_lib.job_geometry).  In those clusters 2-3 of the 4 butterflies per probe have < 25% of their M2 inside.

Test: rebuild the red team's forward model (rotor-averaged couplings, base 1 kHz offsets, same structural parameters,
same Trotter circuit, dt = 2 us, sigma = 0.01) on
  base10  : the red team's N = 10 cluster (control; must reproduce redteam_kills/out/pg_sec_k1_*.npz exactly),
  baware12: N = 10 + the 2 strongest missing butterfly partners (b-aware, the round-4 remedy),
  probe12 : N = 12 probe-centred (size-only control),
compute Jacobian columns for the structural parameters, eps0 and the rotor-group eps_g (FD, same steps as the red
team), and evaluate the red team's own gain functions (analyze_profiled.gains) for the PE and LE envelopes at physical
T2, priors 'known' (nuisances fixed) and 'moderate_partial' (eps0/eps_g profiled with moderate priors; offsets and eta
fixed), t_cl = 0 and 40 us.  The red team's full 'moderate' profile at N = 10 is recomputed from its npz with the
Omega/eta columns dropped, to calibrate the partial profile against the full one.

Echo rows are computed for t <= ECHO_TMAX_US only (transfer rows at all 33 times); the effect of this truncation is
measured at N = 10 against the red team's full npz.
Checkpoint: critic/out/fi_<variant>_<pdb>_p<probe>.{npz,json} after every column (atomic tmp+replace); resumes.
Usage: OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python fi_nscale.py --pdb 1PGA --probe 390 --variant baware12
"""
from __future__ import annotations

import os
import sys

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
sys.dont_write_bytecode = True          # do not create __pycache__ in folders outside critic/

import argparse
import json
import math
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.dirname(HERE)
RT = os.path.join(R4, "redteam_kills")
sys.path.insert(0, RT)
import profiled_gain as PG      # noqa: E402  (read-only reuse; its OUT dir already exists, nothing is written there)
import analyze_profiled as AP   # noqa: E402  (read-only reuse)

L, SC, SP = PG.L, PG.SC, PG.SP
ROOT = PG.ROOT
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)
DT = PG.DT
SIG = PG.SIGMA
STEPS, REC = 160, 5
ECHO_TMAX_US = 160.0


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    PG._replace(tmp, path)


def atomic_npz(path, **arrs):
    tmp = path + ".tmp.npz"
    np.savez(tmp, **arrs)
    PG._replace(tmp, path)


# ------------------------------------------------------------------------------------------------ geometry
def partners(G):
    g = G["g"]
    xyz = np.asarray(g["xyz"])
    Dall = SP.couplings(xyz, G["b0"])
    idx = [int(i) for i in G["idx"]]
    out = []
    for b in G["bs"]:
        gb = idx[b]
        row = Dall[gb] ** 2
        row[gb] = 0.0
        tot = float(row.sum())
        for j in np.argsort(-row):
            j = int(j)
            if j in idx:
                continue
            out.append(dict(b=int(b), b_name=g["names"][gb], j=j, j_name=g["names"][j], share=float(row[j] / tot)))
            if len([o for o in out if o["b"] == b]) >= 3:
                break
    cov = {}
    for b in G["bs"]:
        gb = idx[b]
        row = Dall[gb] ** 2
        row[gb] = 0.0
        cov[g["names"][gb]] = float(row[idx].sum() / row.sum())
    return out, cov


def setup_ext(pdb, probe, variant):
    G0 = PG.setup(pdb, probe)
    g = G0["g"]
    xyz = np.asarray(g["xyz"])
    base = [int(i) for i in G0["idx"]]
    part, cov0 = partners(G0)
    if variant == "base10":
        extra = []
    elif variant == "baware12":
        extra = []
        for o in sorted(part, key=lambda o: -o["share"]):
            if o["j"] not in extra:
                extra.append(o["j"])
            if len(extra) == 2:
                break
    elif variant == "probe12":
        extra = [int(i) for i in SP.cluster(xyz, int(np.asarray(g["idx"])[0]), 12)[10:12]]
    else:
        raise ValueError(variant)
    idx = base + extra
    pdbf = os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb")
    atoms = SC.read_all_atoms(pdbf)
    hk = [k for k, a in enumerate(atoms) if a[3] == "H"]
    groups, _ = SC.rotor_groups(atoms, {k: i for i, k in enumerate(hk)})
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
    lab = np.full(len(idx), -1, int)
    for li, gi in enumerate(touched):
        for k, i in enumerate(idx):
            if gof.get(i) == gi:
                lab[k] = li
    params = []
    for p in g["params"]:
        mv, axis = {}, False
        for (k, u) in p["move"]:
            i = base[int(k)]
            if i in gof:
                axis = True
                for h in groups[gof[i]]:
                    mv[pos[int(h)]] = np.asarray(u, float)
            else:
                mv[pos[i]] = np.asarray(u, float)
        params.append(dict(name=p["name"] + ("_axis" if axis else ""), r=p["r"], move=mv))
    G = dict(g=g, idx=idx, sub=sub, groups_local=groups_local, lab=lab, params=params, Xsub=xyz[sub].copy(),
             b0=g["b0"], bs=list(G0["bs"]), names=[g["names"][i] for i in idx],
             rotor_groups_in_cluster=[[g["names"][int(h)] for h in groups[gi]] for gi in touched])
    Dall = SP.couplings(xyz, G["b0"])
    cov = {}
    for b in G["bs"]:
        gb = idx[b]
        row = Dall[gb] ** 2
        row[gb] = 0.0
        cov[g["names"][gb]] = float(row[idx].sum() / row.sum())
    return G, dict(extra=[g["names"][e] for e in extra], M2b_coverage_N10=cov0, M2b_coverage=cov,
                   missing_partners_N10=part)


# ------------------------------------------------------------------------------------------------ dynamics
def observe_fast(D, offsets, bs, a=0):
    """eta = 0 path of profiled_gain.observe (identical circuit and estimator); transfer at all record times via the
    O(d^2) eigenbasis trace, echo only for t <= ECHO_TMAX_US (rows beyond are left 0)."""
    N = len(D)
    times = list(range(0, STEPS + 1, REC))
    nt, nb = len(times), len(bs)
    S = np.zeros((nt, nb))
    Gm = np.zeros((nt, nb))
    za_full = SP.zsign(N, a)
    zb_full = [SP.zsign(N, b) for b in bs]
    nmax_echo = int(round(ECHO_TMAX_US * 1e-6 / DT))
    for idx, Uk in SP.sector_step_unitaries(D, DT):
        if offsets is not None:
            ph = np.zeros(len(idx))
            for i in range(N):
                ph += offsets[i] * (1.0 - 2.0 * ((idx >> i) & 1)) / 2.0
            Uk = np.exp(-1j * DT * ph)[:, None] * Uk
        Q, lam = SP._unitary_eig(Uk)
        Qh = Q.conj().T
        za = za_full[idx]
        zb = [z[idx] for z in zb_full]
        A = (Qh * za) @ Q
        BT = [((Qh * z) @ Q).T for z in zb]
        lc = lam.conj()
        for ti, n_ in enumerate(times):
            M = A * np.outer(lc ** n_, lam ** n_)
            for bi in range(nb):
                S[ti, bi] += float(np.real(np.sum(M * BT[bi])))
            if n_ <= nmax_echo:
                Oc = Q @ M @ Qh
                A2 = np.abs(Oc) ** 2
                for bi in range(nb):
                    Gm[ti, bi] += float((zb[bi][:, None] * A2 * zb[bi][None, :]).sum())
    Dd = float(1 << N)
    return np.array(times) * DT, S / Dd, Gm / Dd


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1PGA")
    ap.add_argument("--probe", type=int, default=390)
    ap.add_argument("--variant", default="baware12", choices=["base10", "baware12", "probe12"])
    ap.add_argument("--budget", type=float, default=1500.0)
    a = ap.parse_args()
    t0 = time.process_time()
    G, info = setup_ext(a.pdb, a.probe, a.variant)
    N = len(G["idx"])
    ng = len(G["groups_local"])
    Om0 = 2 * math.pi * 1000.0 * np.random.default_rng(3).standard_normal(N)   # prefix-identical to the red team's draw
    tag = f"fi_{a.variant}_{a.pdb}_p{a.probe}"
    fj, fn = os.path.join(OUT, tag + ".json"), os.path.join(OUT, tag + ".npz")
    meta = json.load(open(fj)) if os.path.exists(fj) else {}
    arr = dict(np.load(fn)) if os.path.exists(fn) else {}
    cols = [("struct", p["name"]) for p in G["params"]] + [("eps0", "eps0")] + \
        [("epsg", f"epsg_{j}") for j in range(ng)]
    meta.update(pdb=a.pdb, probe=a.probe, variant=a.variant, N=N, names=G["names"], bs=G["bs"],
                rotor_groups_in_cluster=G["rotor_groups_in_cluster"], columns=[c[1] for c in cols],
                col_kinds=[c[0] for c in cols], echo_tmax_us=ECHO_TMAX_US, **info)
    meta.setdefault("cpu_s", 0.0)
    meta.setdefault("done", [])

    def save():
        atomic_npz(fn, **arr)
        atomic_json(meta, fj)

    def run(D):
        return observe_fast(D, Om0, G["bs"])

    D0 = PG.couplings(G, G["Xsub"], 0.0, np.zeros(ng))
    if "S0" not in arr:
        te = time.process_time()
        tt, S0, G0 = run(D0)
        arr.update(times=tt, S0=S0, G0=G0)
        meta["cpu_base_s"] = time.process_time() - te
        meta["cpu_s"] += meta["cpu_base_s"]
        if a.variant == "base10":        # validation against the red team's stored base run
            z = np.load(os.path.join(RT, "out", f"pg_sec_k1_{a.pdb}_p{a.probe}.npz"))
            ne = int(round(ECHO_TMAX_US * 1e-6 / DT)) // REC + 1
            meta["validation_vs_redteam"] = dict(S=float(np.abs(S0 - z["S0"]).max()),
                                                 G_echo_rows=float(np.abs(G0[:ne] - z["G0"][:ne]).max()))
        save()
        print(json.dumps(dict(stage="base", N=N, cpu=round(meta["cpu_base_s"], 1), **info.get("M2b_coverage", {}))),
              flush=True)
    for kind, name in cols:
        if name in meta["done"]:
            continue
        if time.process_time() - t0 > a.budget:
            print("budget reached; resume later", flush=True)
            break
        te = time.process_time()
        if kind == "struct":
            p = next(q for q in G["params"] if q["name"] == name)
            rp = run(PG.couplings(G, PG.moved(G["Xsub"], p, +1, PG.H_FD), 0.0, np.zeros(ng)))
            rm = run(PG.couplings(G, PG.moved(G["Xsub"], p, -1, PG.H_FD), 0.0, np.zeros(ng)))
            h = PG.H_FD
        elif kind == "eps0":
            rp = run(PG.couplings(G, G["Xsub"], +PG.H_EPS0, np.zeros(ng)))
            rm = run(PG.couplings(G, G["Xsub"], -PG.H_EPS0, np.zeros(ng)))
            h = PG.H_EPS0
        else:
            j = int(name.split("_")[1])
            e = np.zeros(ng)
            e[j] = PG.H_EPSG
            rp = run(PG.couplings(G, G["Xsub"], 0.0, e))
            rm = run(PG.couplings(G, G["Xsub"], 0.0, -e))
            h = PG.H_EPSG
        arr["dS_" + name] = (rp[1] - rm[1]) / (2 * h)
        arr["dG_" + name] = (rp[2] - rm[2]) / (2 * h)
        meta["done"].append(name)
        meta["cpu_s"] += time.process_time() - te
        save()
        print(json.dumps(dict(col=name, cpu=round(time.process_time() - te, 1))), flush=True)
    meta["complete"] = all(c[1] in meta["done"] for c in cols)
    save()
    print(json.dumps(dict(tag=tag, complete=meta["complete"], cpu_run=round(time.process_time() - t0, 1))), flush=True)


if __name__ == "__main__":
    main()
