"""ROUND4 red team, RT-A analysis: profiled joint gains of the echo over classically usable data, with the forward-model
nuisances (site offsets, reversal mismatch, global and per-rotor-group order parameters) profiled out, as a function of
  * t_cl  : the converged-size classical reach time of the echo (UNKNOWN; ROUND3/CRITIC C1 says unresolved at <= T3).
            classical route = transfer S (all t; two-point, classically computable at converged size, K-104)
                              + echo for t < t_cl;   quantum route = transfer + echo at all t.
            t_cl = 0 is the extreme pro-quantum assumption (the whole echo is beyond classical reach).
  * envelope A(t) of the physical reversal (literature anchors; t in units of T2 = 1/sqrt(M2); generous time argument
            = forward time only).  Echo rows are multiplied by A(t) (fixed noise sigma), transfer rows are not.
  * nuisance priors: none / moderate / tight / known (nuisances fixed = the old unprofiled accounting).
Outputs per (ham, probe, prior, T2 choice, envelope, t_cl): median and max per-parameter g = CRB_cl^2 / CRB_q^2
(marginal CRBs, other structural params and all nuisances profiled), and the largest generalised eigenvalue of
F_eff,q vs F_eff,cl.  Also: retained structural FI after profiling (hard window) for the cross-check against
R1_physics_feasibility, and a linearised misspecification test (truth with per-pair order parameters S_ij ~ U[0.85,1],
outside the nuisance family; profiled fit bias / CRB).
Pure post-processing of out/pg_*.npz (seconds).  Output: profiled_summary.json
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np
from scipy.linalg import eigh

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
DQDIR = os.path.join(ROOT, "research", "experiments", "ROUND3", "dq_echo_envelope", "out")
SIG = 0.01
HZ_PER_PPM = 800.0          # 1H at 800 MHz
PRIORS = {
    "none": None,
    "moderate": dict(Omega=2 * math.pi * 0.2 * HZ_PER_PPM, eta=0.02, eps0=0.03, epsg=0.10),
    "tight": dict(Omega=2 * math.pi * 0.05 * HZ_PER_PPM, eta=0.005, eps0=0.01, epsg=0.03),
    "known": "drop",
    "offsets_known": "drop_omega",   # optimistic DQ proxy: offsets compensated/known; other nuisances free
}


def env_logistic(x, c, lam_frac=0.25):
    l = lam_frac * c
    return (1 + math.exp(-c / l)) / (1 + np.exp((x - c) / l))


def env_gauss(x, c):
    return np.exp(-math.log(2) * (x / c) ** 2)


ENVS = {
    "sec": {
        "ideal": lambda x: np.ones_like(x),
        "PE_gauss_4T2": lambda x: env_gauss(x, 4.0),                     # Sanchez 2022, local polarization echo
        "LE_logistic_6.7T2": lambda x: env_logistic(x, 1 / 0.15, 0.25),  # Sanchez 2022, best XXZ Loschmidt echo
        "hyp_15T2": lambda x: env_logistic(x, 15.0, 0.25),
        "hyp_20T2": lambda x: env_logistic(x, 20.0, 0.25),
        "hyp_50T2": lambda x: env_logistic(x, 50.0, 0.25),
    },
    "dq": {
        "ideal": lambda x: np.ones_like(x),
        "DQ_local_7.5T2": lambda x: env_logistic(x, 7.5, 0.23),
        "DQ_LE_12.5T2": lambda x: env_logistic(x, 12.5, 0.23),           # Rufeil-Fiori 2009 / Sanchez 2022 anchor
        "DQ_LE_19T2": lambda x: env_logistic(x, 19.0, 0.23),             # upper end of the adamantane T2 readings
        "hyp_50T2": lambda x: env_logistic(x, 50.0, 0.23),
    },
}
TCL = [0, 10, 20, 30, 40, 50, 60, 80, 100, 120, 160, 200, 240, 1e9]


def load(tag):
    m = json.load(open(os.path.join(HERE, "out", tag + ".json")))
    z = np.load(os.path.join(HERE, "out", tag + ".npz"))
    return m, z


def build(m, z):
    cols, kinds = m["columns"], m["col_kinds"]
    t = z["times"] * 1e6
    nt, nb = z["S0"].shape
    JS = np.stack([z["dS_" + c].reshape(-1) for c in cols], axis=1)     # rows (t, b) row-major
    JG = np.stack([z["dG_" + c].reshape(-1) for c in cols], axis=1)
    trow = np.repeat(t, nb)
    return dict(cols=cols, kinds=kinds, t=t, JS=JS / SIG, JG=JG / SIG, trow=trow, nt=nt, nb=nb)


def prior_vec(kinds, prior):
    p = np.zeros(len(kinds))
    if isinstance(prior, dict):
        for k, kind in enumerate(kinds):
            if kind in prior:
                p[k] = 1.0 / prior[kind] ** 2
    return p


def keep_cols(kinds, prior):
    if prior == "drop":
        return [k for k, kd in enumerate(kinds) if kd == "struct"]
    if prior == "drop_omega":
        return [k for k, kd in enumerate(kinds) if kd != "Omega"]
    return list(range(len(kinds)))


def eff_struct(F, kinds_kept):
    s = [k for k, kd in enumerate(kinds_kept) if kd == "struct"]
    n = [k for k, kd in enumerate(kinds_kept) if kd != "struct"]
    Fss = F[np.ix_(s, s)]
    if not n:
        return Fss
    Fsn = F[np.ix_(s, n)]
    Fnn = F[np.ix_(n, n)]
    return Fss - Fsn @ np.linalg.pinv(Fnn, rcond=1e-12, hermitian=True) @ Fsn.T


def crb_marg(Fe):
    """Marginal CRB (sqrt diag of the inverse); inf for a parameter with weight in a numerically null direction."""
    Fe = 0.5 * (Fe + Fe.T)
    w, V = np.linalg.eigh(Fe)
    wmax = max(float(w.max()), 1e-300)
    bad = w <= 1e-10 * wmax
    var = (V[:, ~bad] ** 2) @ (1.0 / w[~bad])
    if bad.any():
        var = np.where((V[:, bad] ** 2).sum(axis=1) > 1e-6, np.inf, var)
    return np.sqrt(var)


def fisher_rows(B, cols, A_row, rows_S, rows_G, prior):
    kk = keep_cols(B["kinds"], prior)
    JS = B["JS"][rows_S][:, kk]
    JG = (B["JG"][rows_G] * A_row[rows_G][:, None])[:, kk]
    F = JS.T @ JS + JG.T @ JG
    F = F + np.diag(prior_vec([B["kinds"][k] for k in kk], prior))
    return F, [B["kinds"][k] for k in kk]


def gains(B, A_row, tcl, prior):
    allS = np.ones(len(B["trow"]), bool)
    Fq, kinds = fisher_rows(B, None, A_row, allS, np.ones(len(B["trow"]), bool), prior)
    Fc, _ = fisher_rows(B, None, A_row, allS, B["trow"] < tcl - 1e-9, prior)
    Eq, Ec = eff_struct(Fq, kinds), eff_struct(Fc, kinds)
    cq, cc = crb_marg(Eq), crb_marg(Ec)
    with np.errstate(invalid="ignore", divide="ignore"):
        g = (cc / cq) ** 2
    g = np.where(np.isnan(g), np.nan, g)
    try:
        ge = float(eigh(Eq, Ec + 1e-12 * np.trace(Ec) * np.eye(len(Ec)), eigvals_only=True).max())
    except Exception:
        ge = float("nan")
    return g, ge, cq, cc


def T2s(m):
    f = os.path.join(DQDIR, f"fi_{m['pdb']}_p{m['probe']}.json")
    if os.path.exists(f):
        T = json.load(open(f))["T2"]
        return dict(physical=T["T2_rotoravg_us"], cluster=T["T2_cluster_us"], network_static=T["T2_network_us"])
    # fallback (same conventions as dq_lib.t2_info / R1_physics_feasibility.scales): the network T2 is protein-level
    # for a fixed orientation; the cluster T2 is recomputed from the job geometry.
    import sys
    sys.path.insert(0, os.path.join(ROOT, "src"))
    sys.path.insert(0, os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_amplify"))
    import amp_lib as L
    from qapf.nmr import spins as SP
    other = [g for g in glob.glob(os.path.join(DQDIR, f"fi_{m['pdb']}_p*.json"))]
    if not other:
        return None
    T = json.load(open(other[0]))["T2"]
    g = L.job_geometry(m["pdb"], m["probe"], 10, 0, hn_only=False)
    Dc = SP.couplings(g["X0"], g["b0"])
    m2 = 9.0 / 4.0 * float(np.mean(np.sum(Dc ** 2, axis=1)))
    return dict(physical=T["T2_rotoravg_us"], cluster=1e6 / math.sqrt(m2), network_static=T["T2_network_us"])


def misspec(B, z, A_row, prior):
    """Linearised profiled fit of the per-pair order-parameter truth with the nuisance-complete model."""
    kk = keep_cols(B["kinds"], prior)
    kinds = [B["kinds"][k] for k in kk]
    J = np.vstack([B["JS"][:, kk], B["JG"][:, kk] * A_row[:, None]])
    P = np.diag(prior_vec(kinds, prior))
    F = J.T @ J + P
    Finv = np.linalg.pinv(F, rcond=1e-12, hermitian=True)
    s = [k for k, kd in enumerate(kinds) if kd == "struct"]
    crb = np.sqrt(np.maximum(np.diag(Finv)[s], 1e-300))
    out = []
    for key in sorted(k for k in z.files if k.startswith("misS_")):
        seed = key.split("_")[1]
        dy = np.concatenate([z[key].reshape(-1), z["misG_" + seed].reshape(-1) * A_row]) / SIG
        th = Finv @ (J.T @ dy)
        res = dy - J @ th
        out.append(dict(seed=int(seed), misfit_before_max_sigma=float(np.abs(dy).max()),
                        misfit_after_max_sigma=float(np.abs(res).max()),
                        chi2_before=float(dy @ dy), chi2_after=float(res @ res), n_data=int(len(dy)),
                        struct_bias_over_crb=[float(abs(th[k]) / c) for k, c in zip(s, crb)],
                        struct_bias_A=[float(th[k]) for k in s]))
    return out


def main():
    res = dict(note=__doc__.split("\n")[0], sigma=SIG, priors={k: (v if not isinstance(v, dict) else
                                                                  {kk: float(vv) for kk, vv in v.items()})
                                                              for k, v in PRIORS.items()},
               tcl_grid_us=[t if t < 1e8 else "inf" for t in TCL], jobs={})
    for f in sorted(glob.glob(os.path.join(HERE, "out", "pg_*.json"))):
        tag = os.path.basename(f)[:-5]
        m, z = load(tag)
        if not m.get("complete"):
            continue
        B = build(m, z)
        ham = m["ham"]
        T2 = T2s(m)
        struct = [c for c, k in zip(B["cols"], B["kinds"]) if k == "struct"]
        job = dict(ham=ham, pdb=m["pdb"], probe=m["probe"], struct_params=struct, T2_us=T2,
                   base_vs_static_offsetfree_max_over_sigma=m["base_vs_static_offsetfree_max_over_sigma"],
                   validation=dict(static=m["validation_static_vs_amp_lib"], eta_path=m["validation_eta_path_vs_fast"]),
                   rotor_groups_in_cluster=m["rotor_groups_in_cluster"], cases={})
        ones = np.ones(len(B["trow"]))
        # --- cross-check with R1_physics_feasibility: retained hard-window structural FI (trace), Omega + eta only
        hard = B["trow"] >= 80 - 1e-9
        xc = {}
        for pn, pr in (("none", None), ("moderate", PRIORS["moderate"]), ("tight", PRIORS["tight"])):
            kk = [k for k, kd in enumerate(B["kinds"]) if kd in ("struct", "Omega", "eta")]
            kinds = [B["kinds"][k] for k in kk]
            J = B["JG"][hard][:, kk]
            F = J.T @ J + np.diag(prior_vec(kinds, pr))
            s = [k for k, kd in enumerate(kinds) if kd == "struct"]
            Fe = eff_struct(F, kinds)
            xc[pn] = float(np.trace(Fe) / np.trace(F[np.ix_(s, s)]))
        job["xcheck_retained_hard_trace_Omega_eta"] = xc
        # full nuisance family, retained FI (all echo rows, ideal)
        rt = {}
        for pn in ("none", "moderate", "tight"):
            pr = PRIORS[pn]
            kinds = B["kinds"]
            for win, rows in (("hard_ge80", hard), ("all", ones.astype(bool)), ("early_lt80", ~hard)):
                J = B["JG"][rows]
                F = J.T @ J + np.diag(prior_vec(kinds, pr))
                s = [k for k, kd in enumerate(kinds) if kd == "struct"]
                rt[f"{pn}|{win}"] = float(np.trace(eff_struct(F, kinds)) / np.trace(F[np.ix_(s, s)]))
        job["retained_echo_struct_FI_trace_full_family"] = rt
        if T2 is None:
            res["jobs"][tag] = job
            continue
        for T2name in ("physical", "cluster"):
            x = B["trow"] / T2[T2name]
            for ename, ef in ENVS[ham].items():
                A_row = ef(x)
                for pn, pr in PRIORS.items():
                    if ham == "sec" and pn == "offsets_known":
                        continue
                    rows = []
                    for tcl in TCL:
                        g, ge, cq, cc = gains(B, A_row, tcl, pr)
                        fin = g[np.isfinite(g)]
                        gv = g[~np.isnan(g)]
                        rows.append(dict(tcl=tcl if tcl < 1e8 else "inf",
                                         g_med=float(np.median(gv)) if len(gv) else None,
                                         g_max=float(np.max(fin)) if len(fin) else None,
                                         g_min=float(np.min(gv)) if len(gv) else None,
                                         n_inf=int(np.sum(np.isinf(g))),
                                         gen_eig_max=ge, crb_q_A=cq.tolist(), crb_cl_A=cc.tolist()))
                    ok2 = [r["tcl"] for r in rows if r["tcl"] != "inf" and r["g_med"] is not None and r["g_med"] >= 2]
                    ok10 = [r["tcl"] for r in rows if r["tcl"] != "inf" and r["g_med"] is not None and r["g_med"] >= 10]
                    okmax2 = [r["tcl"] for r in rows if r["tcl"] != "inf" and r["g_max"] is not None and r["g_max"] >= 2]
                    job["cases"][f"{T2name}|{ename}|{pn}"] = dict(
                        rows=rows, tcl_max_gmed_ge2=max(ok2) if ok2 else None,
                        tcl_max_gmed_ge10=max(ok10) if ok10 else None, tcl_max_gmax_ge2=max(okmax2) if okmax2 else None,
                        g_med_at={str(r["tcl"]): r["g_med"] for r in rows})
            # misspecification test at physical T2
        mis = {}
        for ename in (("ideal", "LE_logistic_6.7T2") if ham == "sec" else ("ideal", "DQ_LE_12.5T2")):
            A_row = ENVS[ham][ename](B["trow"] / T2["physical"])
            for pn in ("none", "moderate", "known"):
                mis[f"{ename}|{pn}"] = misspec(B, z, A_row, PRIORS[pn])
        job["misspecification_perpair_S"] = mis
        res["jobs"][tag] = job
        print(tag, "done", flush=True)
    # ------------------------------------------------------------- headline table
    head = []
    for tag, j in res["jobs"].items():
        for key, c in j["cases"].items():
            T2name, ename, pn = key.split("|")
            if T2name != "physical" or pn not in ("none", "moderate", "tight", "known", "offsets_known"):
                continue
            head.append(dict(job=tag, env=ename, prior=pn, g_med_tcl0=c["g_med_at"]["0"], g_med_tcl40=c["g_med_at"]["40"],
                             g_med_tcl80=c["g_med_at"]["80"], tcl_max_gmed_ge2=c["tcl_max_gmed_ge2"],
                             tcl_max_gmax_ge2=c["tcl_max_gmax_ge2"], tcl_max_gmed_ge10=c["tcl_max_gmed_ge10"]))
    res["headline_physicalT2"] = head
    tmp = os.path.join(HERE, "profiled_summary.json.tmp")
    json.dump(res, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "profiled_summary.json"))
    # console table
    print(f"{'job':26s} {'env':18s} {'prior':13s} {'g0':>7s} {'g40':>7s} {'g80':>7s} {'tcl*2':>6s} {'tclmax2':>7s}")
    for h in head:
        f = lambda v: "   -  " if v is None else f"{v:7.2f}"
        print(f"{h['job']:26s} {h['env']:18s} {h['prior']:13s} {f(h['g_med_tcl0'])} {f(h['g_med_tcl40'])} "
              f"{f(h['g_med_tcl80'])} {str(h['tcl_max_gmed_ge2']):>6s} {str(h['tcl_max_gmax_ge2']):>7s}")


if __name__ == "__main__":
    main()


# =============================================================================== extensions (RT-A2, RT-A3)
def _fit(Jrows, dy, kinds, prior):
    P = np.diag(prior_vec(kinds, prior))
    F = Jrows.T @ Jrows + P
    Finv = np.linalg.pinv(F, rcond=1e-12, hermitian=True)
    th = Finv @ (Jrows.T @ dy)
    s = [k for k, kd in enumerate(kinds) if kd == "struct"]
    Fe = eff_struct(F, kinds)
    return th[s], crb_marg(Fe)


def accuracy_gain(B, z, A_row, tcl, prior, extraS=None, extra_z=None):
    """Bias-inclusive gain: g_acc = (CRB_cl^2 + b_cl^2) / (CRB_q^2 + b_q^2) per structural parameter, where b is the
    linearised profiled-fit bias under the per-pair order-parameter truth (outside the nuisance family), for the
    classical route (transfer [+ extraS] + echo t < t_cl) and the quantum route (transfer [+ extraS] + echo all t)."""
    kk = keep_cols(B["kinds"], prior)
    kinds = [B["kinds"][k] for k in kk]
    JS = B["JS"][:, kk]
    JG = B["JG"][:, kk] * A_row[:, None]
    if extraS is not None:
        JS = np.vstack([JS, extraS["JS"][:, kk]])
    early = B["trow"] < tcl - 1e-9
    out = []
    for key in sorted(k for k in z.files if k.startswith("misS_")):
        seed = key.split("_")[1]
        dS = z[key].reshape(-1) / SIG
        if extraS is not None:
            dS = np.concatenate([dS, extra_z[key].reshape(-1) / SIG])
        dG = z["misG_" + seed].reshape(-1) * A_row / SIG
        bq, cq = _fit(np.vstack([JS, JG]), np.concatenate([dS, dG]), kinds, prior)
        bc, cc = _fit(np.vstack([JS, JG[early]]), np.concatenate([dS, dG[early]]), kinds, prior)
        with np.errstate(invalid="ignore", divide="ignore"):
            g = (cc ** 2 + bc ** 2) / (cq ** 2 + bq ** 2)
        out.append(dict(seed=int(seed), g_acc=g.tolist(), bias_q_over_crb_q=(np.abs(bq) / cq).tolist(),
                        bias_cl_over_crb_cl=(np.abs(bc) / cc).tolist()))
    allg = np.array([x for o in out for x in o["g_acc"]], float)
    allg = allg[~np.isnan(allg)]
    return dict(g_acc_med=float(np.median(allg)) if len(allg) else None,
                g_acc_max=float(np.max(allg[np.isfinite(allg)])) if np.isfinite(allg).any() else None, draws=out)


def extensions():
    res = json.load(open(os.path.join(HERE, "profiled_summary.json")))
    ext = dict(note="RT-A2: DQ echo gain with the SECULAR transfer also on the classical side (joint profiling over the "
                    "shared nuisances). RT-A3: bias-inclusive accuracy gain under per-pair order-parameter truth.",
               dq_plus_secS={}, accuracy={})
    for f in sorted(glob.glob(os.path.join(HERE, "out", "pg_*.json"))):
        tag = os.path.basename(f)[:-5]
        m, z = load(tag)
        if not m.get("complete"):
            continue
        B = build(m, z)
        T2 = T2s(m)
        x = B["trow"] / T2["physical"]
        ham = m["ham"]
        # RT-A2
        if ham == "dq":
            stag = tag.replace("pg_dq_k1_", "pg_sec_k1_")
            if os.path.exists(os.path.join(HERE, "out", stag + ".json")):
                ms, zs = load(stag)
                Bs = build(ms, zs)
                assert Bs["cols"] == B["cols"], (Bs["cols"], B["cols"])
                d = {}
                for ename in ("ideal", "DQ_local_7.5T2", "DQ_LE_12.5T2", "DQ_LE_19T2"):
                    A_row = ENVS["dq"][ename](x)
                    for pn in ("none", "moderate", "tight", "offsets_known"):
                        pr = PRIORS[pn]
                        kk = keep_cols(B["kinds"], pr)
                        kinds = [B["kinds"][k] for k in kk]
                        rows = []
                        for tcl in TCL:
                            JSall = np.vstack([B["JS"][:, kk], Bs["JS"][:, kk]])
                            JG = B["JG"][:, kk] * A_row[:, None]
                            early = B["trow"] < tcl - 1e-9
                            Fq = JSall.T @ JSall + JG.T @ JG + np.diag(prior_vec(kinds, pr))
                            Fc = JSall.T @ JSall + JG[early].T @ JG[early] + np.diag(prior_vec(kinds, pr))
                            cq, cc = crb_marg(eff_struct(Fq, kinds)), crb_marg(eff_struct(Fc, kinds))
                            with np.errstate(invalid="ignore", divide="ignore"):
                                g = (cc / cq) ** 2
                            gv = g[~np.isnan(g)]
                            rows.append(dict(tcl=tcl if tcl < 1e8 else "inf", g_med=float(np.median(gv)),
                                             g_max=float(np.max(gv[np.isfinite(gv)])) if np.isfinite(gv).any() else None))
                        ok2 = [r["tcl"] for r in rows if r["tcl"] != "inf" and r["g_med"] >= 2]
                        d[f"{ename}|{pn}"] = dict(g_med_at={str(r["tcl"]): r["g_med"] for r in rows},
                                                  g_max_at={str(r["tcl"]): r["g_max"] for r in rows},
                                                  tcl_max_gmed_ge2=max(ok2) if ok2 else None)
                ext["dq_plus_secS"][tag] = d
        # RT-A3
        envs = ("ideal", "PE_gauss_4T2", "LE_logistic_6.7T2") if ham == "sec" else ("ideal", "DQ_LE_12.5T2", "DQ_LE_19T2")
        acc = {}
        for ename in envs:
            A_row = ENVS[ham][ename](x)
            for pn in ("moderate", "known"):
                for tcl in (0, 40, 80):
                    r = accuracy_gain(B, z, A_row, tcl, PRIORS[pn])
                    acc[f"{ename}|{pn}|tcl{tcl}"] = r
        ext["accuracy"][tag] = acc
        print(tag, "ext done", flush=True)
    tmp = os.path.join(HERE, "profiled_extensions.json.tmp")
    json.dump(ext, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "profiled_extensions.json"))
    for tag, d in ext["dq_plus_secS"].items():
        for k, v in d.items():
            ga = v["g_med_at"]
            print(f"{tag:22s} {k:28s} g0={ga['0']:.2f} g40={ga['40']:.2f} g60={ga['60']:.2f} g80={ga['80']:.2f} tcl*={v['tcl_max_gmed_ge2']}")
    for tag, d in ext["accuracy"].items():
        for k, v in d.items():
            print(f"ACC {tag:22s} {k:34s} g_acc_med={v['g_acc_med']:.2f} max={v['g_acc_max']}")


if __name__ == "__main__" and os.environ.get("RT_EXT", "0") == "1":
    extensions()
