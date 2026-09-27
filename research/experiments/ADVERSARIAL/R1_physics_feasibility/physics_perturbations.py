"""R1 physics-feasibility audit, part 3: in-model tests of physical effects the isolated-cluster echo model omits.

Reuses the exact geometry, B0 orientation, cluster, observed spins, structural parameters, Trotter circuit and time
grid of a RAW C1 job (scripts/nmr_gate.py v2 conventions), N = 10, sector-exact (deterministic).

Tests (each is a question about the PHYSICAL forward model, not about classical hardness):
  rotor    Fast 3-site methyl/NH3 rotation (present in any protein above ~100 K) replaces the static couplings of the
           cluster's rotor protons by their jump averages.  Metric: max_t |F_rotor - F_static| / sigma, easy vs hard
           window (model error of the static-H forward model the RAW runs used).
  nuis     Unknown per-site Zeeman offsets Omega_i (chemical shift + CSA + heteronuclear local fields; the model sets
           them to 0) and an imperfect backward leg -(1+eta) H_dip (the scaling mismatch measured by Sanchez et al.
           2022 is ~15% between +k and -k slopes).  Echo protocol simulated explicitly:
               G_ab(t) = 2^-N Tr[ Z_b W Z_a U Z_b U^dag Z_a W^dag ],  U = S(d, Omega)^n,  W = (S((1+eta) d, Omega)^n)^dag
           (W = U^dag reproduces F_ab of the RAW run exactly).  Reports (i) |G(Omega0) - F| / sigma (model error from
           ignoring offsets of realistic size), (ii) the echo attenuation vs eta, (iii) the Fisher matrix over
           (structure, eta, Omega_1..N) and the structural information left after the nuisances are profiled out
           (Schur complement), with and without priors.
  disorder Static conformational heterogeneity (frozen protein ensemble: independent rigid translations of every
           residue, sigma_res in A) and mosaic spread of the alignment (B0 tilt, sigma_theta in degrees).  The measured
           echo is the ENSEMBLE average; its derivative w.r.t. the structural parameter is the ensemble mean of the
           per-member derivatives.  Metric: FI of the ensemble-mean signal / FI of the single structure, easy vs hard
           window; and |<F> - F(x0)| / sigma.
Single-threaded, budgeted (prints wall time per test).  Output: physics_<job>.json
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
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, HERE)
from qapf.nmr import spins as SP  # noqa: E402
import scales as SC  # noqa: E402


# ------------------------------------------------------------------------------------------------ job reconstruction
def load_job(fn):
    sub = "nmr_gate_hn" if "HN_" in fn else "nmr_gate"
    d = json.load(open(os.path.join(ROOT, "research", "results", "RAW", sub, fn)))
    hn = "HN_" in fn
    pdbf = os.path.join(ROOT, "data", "instruments", "nmr", f"{d['pdb']}_H.pdb")
    names, xyz, resid = SP.read_h_coords(pdbf)
    full = dict(names=list(names), xyz=xyz.copy(), resid=np.asarray(resid).copy())
    if hn:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        names = [names[i] for i in keep]; xyz = xyz[keep]; resid = np.asarray(resid)[keep]
    idx = d["cluster"]
    X0 = xyz[idx].copy()
    b0 = np.array(d["b0"])
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    N = d["N"]
    K = 3
    far = [int(k) for k in np.argsort(-dist)[:K]]
    params = []
    for k in far:
        u = (X0[k] - X0[0]) / dist[k]
        params.append(dict(name=f"radial_{names[idx[k]]}", move=[(int(k), u)]))
    # rigid parameter: reproduce exactly what the RAW job used (some RAW jobs predate the ">= 2 protons" rule, so the
    # residue is read from the RAW parameter name; direction = probe -> farthest cluster proton of that residue)
    for pr in d["params"][K:]:
        assert pr["name"].startswith("rigid_res"), pr["name"]
        kres = int(pr["name"][len("rigid_res"):])
        grp = [int(i) for i in range(N) if resid[idx[i]] == kres]
        kfar = max(grp, key=lambda i: dist[i])
        ug = (X0[kfar] - X0[0]) / dist[kfar]
        params.append(dict(name=pr["name"], move=[(i, ug) for i in grp]))
    assert [p["name"] for p in params] == [p["name"] for p in d["params"]], ([p["name"] for p in params], [p["name"] for p in d["params"]])
    rec = max(1, d["steps"] // (len(d["times"]) - 1))
    return dict(d=d, hn=hn, names=names, xyz=xyz, resid=resid, idx=idx, X0=X0, b0=b0, params=params, rec=rec,
                full=full)


def geom(X0, p, sgn, h):
    X = X0.copy()
    for (i, u) in p["move"]:
        X[i] = X[i] + sgn * h * np.asarray(u)
    return X


# ------------------------------------------------------------------------------------------------ echo engine
def _blocks(dmat, dt, offsets):
    """per-sector (idx, Q, lam) of the Trotter step S = diag(exp(-i dt sum_i Omega_i Z_i / 2)) * S_dip."""
    out = []
    N = len(dmat)
    for idx, Uk in SP.sector_step_unitaries(dmat, dt):
        if offsets is not None:
            ph = np.zeros(len(idx))
            for i in range(N):
                ph += offsets[i] * (1.0 - 2.0 * ((idx >> i) & 1)) / 2.0
            Uk = np.exp(-1j * dt * ph)[:, None] * Uk
        Q, lam = SP._unitary_eig(Uk)
        out.append((idx, Q, lam))
    return out


def echo(dmat, dt, n_steps, rec, a, bs, offsets=None, eta=0.0):
    """G_ab(t_n) = 2^-N Tr[Z_b W Z_a U Z_b U^dag Z_a W^dag] with U = S^n, W = (S_eta^n)^dag (see module doc)."""
    N = len(dmat)
    fw = _blocks(dmat, dt, offsets)
    bw = fw if eta == 0.0 else _blocks(dmat * (1.0 + eta), dt, offsets)
    times = list(range(0, n_steps + 1, rec))
    G = {b: np.zeros(len(times)) for b in bs}
    for (idx, Q, lam), (_, Qb, lamb) in zip(fw, bw):
        za = 1.0 - 2.0 * ((idx >> a) & 1)
        Qh = Q.conj().T
        Qbh = Qb.conj().T
        for b in bs:
            zb = 1.0 - 2.0 * ((idx >> b) & 1)
            ZbQ = Qh * zb[None, :] @ Q                        # Q^dag Z_b Q (eigenbasis of forward step)
            for ti, n in enumerate(times):
                ln = lam ** n
                M1 = Q @ ((ln[:, None] * ZbQ) * ln.conj()[None, :]) @ Qh       # U Z_b U^dag
                A_ = za[:, None] * M1 * za[None, :]                            # Z_a (.) Z_a
                lb = lamb.conj() ** n                                          # W = Qb diag(lamb^-n) Qb^dag
                Wm = (Qb * lb[None, :]) @ Qbh
                B = Wm @ A_ @ Wm.conj().T
                G[b][ti] += float(np.real(np.sum(zb * np.diag(B))))
    return np.array(times) * dt, {b: G[b] / (1 << N) for b in bs}


def fvec(G, bs):
    return np.concatenate([G[b] for b in bs])


# ------------------------------------------------------------------------------------------------ tests
def test_rotor(J, sigma):
    d = J["d"]
    if J["hn"]:
        return dict(skipped="amide-only network has no methyl/NH3 rotors")
    full = J["full"]
    pdbf = os.path.join(ROOT, "data", "instruments", "nmr", f"{d['pdb']}_H.pdb")
    atoms = SC.read_all_atoms(pdbf)
    hk = [k for k, a in enumerate(atoms) if a[3] == "H"]
    groups, _ = SC.rotor_groups(atoms, {k: i for i, k in enumerate(hk)})
    Dfull = SC.averaged_couplings(full["xyz"], J["b0"], groups)
    cl = J["idx"]
    Dr = Dfull[np.ix_(cl, cl)]
    Ds = SP.couplings(J["X0"], J["b0"])
    tt, S0, F0 = SP.sector_exact_correlators(Ds, d["dt"], d["steps"], 0, d["bs"], record_every=J["rec"], otoc=True)
    _, S1, F1 = SP.sector_exact_correlators(Dr, d["dt"], d["steps"], 0, d["bs"], record_every=J["rec"], otoc=True)
    tc = d["best_t_c_otoc_index"]
    dF = np.max(np.stack([np.abs(F1[b] - F0[b]) for b in d["bs"]]), axis=0)
    dS = np.max(np.stack([np.abs(S1[b] - S0[b]) for b in d["bs"]]), axis=0)
    first = np.nonzero(dF > sigma)[0]
    return dict(rotor_protons_in_cluster=[J["names"][cl[i]] for i in range(len(cl))
                                          if any(cl[i] in g for g in groups)],
                max_dF_over_sigma_easy=float(dF[:tc].max() / sigma), max_dF_over_sigma_hard=float(dF[tc:].max() / sigma),
                max_dS_over_sigma=float(dS.max() / sigma),
                first_time_dF_exceeds_sigma_us=None if not len(first) else float(tt[first[0]] * 1e6),
                t_c_us=float(tt[tc] * 1e6))


def test_nuisance(J, sigma, omega_sd_hz, seed=3):
    d = J["d"]
    dt, n, rec, bs = d["dt"], d["steps"], J["rec"], d["bs"]
    X0, b0 = J["X0"], J["b0"]
    N = len(X0)
    Dm = SP.couplings(X0, b0)
    rng = np.random.default_rng(seed)
    Om0 = 2 * math.pi * omega_sd_hz * rng.standard_normal(N)
    t0 = time.time()
    tt, Gid = echo(Dm, dt, n, rec, 0, bs)                                # no offsets, perfect reversal
    Fraw = {b: np.array(d["F_exact"][str(b)]) for b in bs}
    check = max(float(np.abs(Gid[b] - Fraw[b]).max()) for b in bs)
    _, G0 = echo(Dm, dt, n, rec, 0, bs, offsets=Om0)
    tc = d["best_t_c_otoc_index"]
    dOm = np.max(np.stack([np.abs(G0[b] - Gid[b]) for b in bs]), axis=0)
    # attenuation vs eta (no butterfly-free LE here: report the echo itself and its deviation)
    eta_scan = {}
    for eta in (0.005, 0.02, 0.05, 0.15):
        _, Ge = echo(Dm, dt, n, rec, 0, bs, offsets=Om0, eta=eta)
        dev = np.max(np.stack([np.abs(Ge[b] - G0[b]) for b in bs]), axis=0)
        eta_scan[str(eta)] = dict(max_dev_over_sigma_easy=float(dev[:tc].max() / sigma),
                                  max_dev_over_sigma_hard=float(dev[tc:].max() / sigma),
                                  first_time_dev_exceeds_sigma_us=(None if not np.any(dev > sigma)
                                                                   else float(tt[np.argmax(dev > sigma)] * 1e6)))
    # Fisher matrix over structure + (eta, Omega_1..N)
    h = d["h"]
    cols, names = [], []
    for p in J["params"]:
        _, Gp = echo(SP.couplings(geom(X0, p, +1, h), b0), dt, n, rec, 0, bs, offsets=Om0)
        _, Gm = echo(SP.couplings(geom(X0, p, -1, h), b0), dt, n, rec, 0, bs, offsets=Om0)
        cols.append((fvec(Gp, bs) - fvec(Gm, bs)) / (2 * h)); names.append(p["name"])
    he = 0.01
    _, Gp = echo(Dm, dt, n, rec, 0, bs, offsets=Om0, eta=he)
    _, Gm = echo(Dm, dt, n, rec, 0, bs, offsets=Om0, eta=-he)
    cols.append((fvec(Gp, bs) - fvec(Gm, bs)) / (2 * he)); names.append("eta")
    hw = 2 * math.pi * 100.0
    for i in range(N):
        e = np.zeros(N); e[i] = hw
        _, Gp = echo(Dm, dt, n, rec, 0, bs, offsets=Om0 + e)
        _, Gm = echo(Dm, dt, n, rec, 0, bs, offsets=Om0 - e)
        cols.append((fvec(Gp, bs) - fvec(Gm, bs)) / (2 * hw)); names.append(f"Omega_{i}")
    Jm = np.stack(cols, axis=1) / sigma                         # rows: (b, t) blocks
    nt = len(tt)
    rows_hard = np.concatenate([np.arange(k * nt + tc, (k + 1) * nt) for k in range(len(bs))])
    rows_easy = np.concatenate([np.arange(k * nt, k * nt + tc) for k in range(len(bs))])
    ns = len(J["params"])

    def schur(rows, prior_eta=None, prior_om_hz=None):
        Jr = Jm[rows]
        Fm = Jr.T @ Jr
        Fss = Fm[:ns, :ns]; Fsn = Fm[:ns, ns:]; Fnn = Fm[ns:, ns:].copy()
        if prior_eta is not None:
            Fnn[0, 0] += 1.0 / prior_eta ** 2
        if prior_om_hz is not None:
            Fnn[1:, 1:] += np.eye(N) / (2 * math.pi * prior_om_hz) ** 2
        Feff = Fss - Fsn @ np.linalg.pinv(Fnn, rcond=1e-12, hermitian=True) @ Fsn.T
        return dict(trace_Fss=float(np.trace(Fss)), trace_Feff=float(np.trace(Feff)),
                    retained_trace=float(np.trace(Feff) / max(np.trace(Fss), 1e-300)),
                    retained_diag=[float(Feff[k, k] / max(Fss[k, k], 1e-300)) for k in range(ns)])
    ppm = 0.8e3                                                # Hz per ppm at 800 MHz 1H
    fis = {}
    for lab, rows in (("hard", rows_hard), ("easy", rows_easy), ("all", np.arange(Jm.shape[0]))):
        fis[lab] = dict(
            no_prior=schur(rows),
            prior_eta_0p02_omega_0p2ppm=schur(rows, 0.02, 0.2 * ppm),
            prior_eta_0p005_omega_0p05ppm=schur(rows, 0.005, 0.05 * ppm),
            eta_only_no_prior=_schur_subset(Jm, rows, ns, [ns]),
            omegas_only_no_prior=_schur_subset(Jm, rows, ns, list(range(ns + 1, ns + 1 + N))))
    # cross-check: structural FI hard/easy for the offset-free model (should match RAW FI_otoc_t split)
    raw_hard = float(sum(np.sum(np.array(p["FI_otoc_t"])[tc:]) for p in d["params"]))
    return dict(check_perfect_reversal_vs_RAW=check, omega_sd_hz=omega_sd_hz,
                offsets_model_error=dict(max_over_sigma_easy=float(dOm[:tc].max() / sigma),
                                         max_over_sigma_hard=float(dOm[tc:].max() / sigma),
                                         first_time_exceeds_sigma_us=(None if not np.any(dOm > sigma)
                                                                      else float(tt[np.argmax(dOm > sigma)] * 1e6))),
                eta_scan=eta_scan, fisher=fis, param_names=names[:ns], RAW_FI_echo_hard_no_offsets=raw_hard,
                t_c_us=float(tt[tc] * 1e6), secs=time.time() - t0)


def _schur_subset(Jm, rows, ns, nuis):
    Jr = Jm[rows]
    Fm = Jr.T @ Jr
    Fss = Fm[:ns, :ns]
    Fsn = Fm[np.ix_(range(ns), nuis)]
    Fnn = Fm[np.ix_(nuis, nuis)]
    Feff = Fss - Fsn @ np.linalg.pinv(Fnn, rcond=1e-12, hermitian=True) @ Fsn.T
    return dict(retained_trace=float(np.trace(Feff) / max(np.trace(Fss), 1e-300)),
                retained_diag=[float(Feff[k, k] / max(Fss[k, k], 1e-300)) for k in range(ns)])


def test_disorder(J, sigma, M, sig_res_list, mosaic_deg_list, pidx=None, seed=11):
    """Ensemble average over rigid residue translations (sigma_res, A) and B0 tilts (sigma_theta, deg)."""
    d = J["d"]
    dt, n, rec, bs, h = d["dt"], d["steps"], J["rec"], d["bs"], d["h"]
    X0, b0 = J["X0"], J["b0"]
    tc = d["best_t_c_otoc_index"]
    if pidx is None:                                           # parameter with the largest hard-window echo FI
        pidx = int(np.argmax([np.sum(np.array(p["FI_otoc_t"])[tc:]) for p in d["params"]]))
    p = J["params"][pidx]
    resl = J["resid"][J["idx"]]
    ures = sorted(set(resl.tolist()))
    rng = np.random.default_rng(seed)
    Zres = rng.standard_normal((M, len(ures), 3))             # common random numbers across sigma settings
    Ztilt = rng.standard_normal((M, 2))
    e1 = np.cross(b0, [1.0, 0, 0]); e1 = e1 / np.linalg.norm(e1) if np.linalg.norm(e1) > 1e-6 else np.array([0, 1.0, 0])
    e2 = np.cross(b0, e1)

    def run(X, bb):
        _, _, F = SP.sector_exact_correlators(SP.couplings(X, bb), dt, n, 0, bs, record_every=rec, otoc=True)
        return fvec(F, bs)
    t0 = time.time()
    F0 = run(X0, b0)
    D0 = (run(geom(X0, p, +1, h), b0) - run(geom(X0, p, -1, h), b0)) / (2 * h)
    nt = len(d["times"])
    hard = np.concatenate([np.arange(k * nt + tc, (k + 1) * nt) for k in range(len(bs))])
    easy = np.concatenate([np.arange(k * nt, k * nt + tc) for k in range(len(bs))])
    fi = lambda D, rows: float(np.sum(D[rows] ** 2) / sigma ** 2)
    out = dict(param=p["name"], FI_single_hard=fi(D0, hard), FI_single_easy=fi(D0, easy), settings={})
    settings = [("res", s) for s in sig_res_list] + [("mosaic", m) for m in mosaic_deg_list]
    for kind, val in settings:
        Fs, Ds = [], []
        for k in range(M):
            X = X0.copy(); bb = b0.copy()
            if kind == "res":
                for r_i, r in enumerate(ures):
                    X[resl == r] += val * Zres[k, r_i]
            else:
                th = math.radians(val)
                v = b0 + th * (Ztilt[k, 0] * e1 + Ztilt[k, 1] * e2)
                bb = v / np.linalg.norm(v)
            Fs.append(run(X, bb))
            # the structural parameter moves the same protons along the same directions in every member
            Xp = X.copy(); Xm = X.copy()
            for (i, u) in p["move"]:
                Xp[i] += h * np.asarray(u); Xm[i] -= h * np.asarray(u)
            Ds.append((run(Xp, bb) - run(Xm, bb)) / (2 * h))
        Fbar = np.mean(Fs, axis=0); Dbar = np.mean(Ds, axis=0)
        Dsd = np.std(Ds, axis=0, ddof=1) / math.sqrt(M)           # MC standard error of the mean derivative
        # bias-corrected FI of the mean derivative: E[Dbar^2] = mu^2 + se^2
        fi_bc = lambda rows: float(np.sum(np.maximum(Dbar[rows] ** 2 - Dsd[rows] ** 2, 0.0)) / sigma ** 2)
        out["settings"][f"{kind}={val}"] = dict(
            FI_ens_hard=fi(Dbar, hard), FI_ens_easy=fi(Dbar, easy), FI_ens_hard_biascorr=fi_bc(hard),
            FI_ens_easy_biascorr=fi_bc(easy),
            retained_hard=fi_bc(hard) / out["FI_single_hard"], retained_easy=fi_bc(easy) / out["FI_single_easy"],
            ensmean_vs_single_max_over_sigma_easy=float(np.abs(Fbar - F0)[easy].max() / sigma),
            ensmean_vs_single_max_over_sigma_hard=float(np.abs(Fbar - F0)[hard].max() / sigma),
            member_spread_hard_over_sigma=float(np.median(np.std(Fs, axis=0)[hard]) / sigma), M=M)
        print(json.dumps({"disorder": f"{kind}={val}", **{k: round(v, 3) if isinstance(v, float) else v
                                                          for k, v in out["settings"][f"{kind}={val}"].items()},
                          "secs": round(time.time() - t0, 1)}), flush=True)
    out["secs"] = time.time() - t0
    return out


def test_powder(J, sigma, M, pidx=None, seed=21):
    """Powder (microcrystalline, unoriented) sample: the measured signal is the orientation average.  Compares the FI
    of the powder-averaged signal with the mean single-orientation FI over the same M random orientations
    (cancellation factor), for echo F and transfer S, in the easy/hard windows of the RAW job."""
    d = J["d"]
    dt, n, rec, bs, h = d["dt"], d["steps"], J["rec"], d["bs"], d["h"]
    X0 = J["X0"]
    tc = d["best_t_c_otoc_index"]
    if pidx is None:
        pidx = int(np.argmax([np.sum(np.array(p["FI_otoc_t"])[tc:]) for p in d["params"]]))
    p = J["params"][pidx]
    rng = np.random.default_rng(seed)
    V = rng.standard_normal((M, 3)); V /= np.linalg.norm(V, axis=1)[:, None]
    nt = len(d["times"])
    hard = np.concatenate([np.arange(k * nt + tc, (k + 1) * nt) for k in range(len(bs))])
    easy = np.concatenate([np.arange(k * nt, k * nt + tc) for k in range(len(bs))])
    t0 = time.time()
    DF, DS = [], []
    for k in range(M):
        _, Sp, Fp = SP.sector_exact_correlators(SP.couplings(geom(X0, p, +1, h), V[k]), dt, n, 0, bs,
                                                 record_every=rec, otoc=True)
        _, Sm, Fm = SP.sector_exact_correlators(SP.couplings(geom(X0, p, -1, h), V[k]), dt, n, 0, bs,
                                                 record_every=rec, otoc=True)
        DF.append((fvec(Fp, bs) - fvec(Fm, bs)) / (2 * h)); DS.append((fvec(Sp, bs) - fvec(Sm, bs)) / (2 * h))
    DF = np.array(DF); DS = np.array(DS)
    out = dict(param=p["name"], M=M)
    for lab, Dm in (("echo", DF), ("transfer", DS)):
        mean = Dm.mean(axis=0); se = Dm.std(axis=0, ddof=1) / math.sqrt(M)
        for wn, rows in (("easy", easy), ("hard", hard)):
            single = float(np.mean(np.sum(Dm[:, rows] ** 2, axis=1)) / sigma ** 2)
            powder = float(np.sum(np.maximum(mean[rows] ** 2 - se[rows] ** 2, 0.0)) / sigma ** 2)
            out[f"{lab}_{wn}"] = dict(mean_single_orientation_FI=single, powder_FI_biascorr=powder,
                                      retained=powder / max(single, 1e-300))
    out["secs"] = time.time() - t0
    print(json.dumps(out), flush=True)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True)
    ap.add_argument("--tests", default="rotor,nuis")
    ap.add_argument("--omega-sd-hz", type=float, default=1000.0)
    ap.add_argument("--M", type=int, default=8)
    ap.add_argument("--sig-res", default="0.05,0.1,0.2")
    ap.add_argument("--mosaic", default="2")
    a = ap.parse_args()
    J = load_job(a.job)
    sigma = J["d"]["sigma"]
    outf = os.path.join(HERE, f"physics_{a.job.replace('.json', '')}.json")
    res = json.load(open(outf)) if os.path.exists(outf) else {}
    res["job"] = a.job
    for t in a.tests.split(","):
        t0 = time.time()
        if t == "rotor":
            res["rotor"] = test_rotor(J, sigma)
        elif t == "nuis":
            res["nuisance"] = test_nuisance(J, sigma, a.omega_sd_hz)
        elif t == "disorder":
            res["disorder"] = test_disorder(J, sigma, a.M, [float(v) for v in a.sig_res.split(",") if v],
                                            [float(v) for v in a.mosaic.split(",") if v])
        elif t == "powder":
            res["powder"] = test_powder(J, sigma, a.M)
        print(t, "secs", round(time.time() - t0, 1), flush=True)
        json.dump(res, open(outf, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else float(o))
    print(json.dumps({k: v for k, v in res.items() if k != "disorder"}, default=str)[:4000])


if __name__ == "__main__":
    main()
