"""R1_fi_method / test NUIS: are the gate's parameters structurally meaningful, and does the echo hard window still add
information once the analyst must also estimate what a real analysis cannot know exactly?
Cluster 1UBQ p19, N = 10, dense, orientation 0, gamma = 0 (the flagship C1 job).  Exact model only (FI is a property of the
data; the classical failure times are taken from the gate: transfer t_c = 17 (never fails, eps = 1e-4), echo t_c = 4
(80 us, best adversary of the gate panel); variant with no hard window for transfer).
Jacobians (central differences): the 4 gate parameters (h = 0.05 A), the 27 Cartesian coordinates of the 9 non-probe
protons (h = 0.02 A; the probe is the origin, which fixes translations), a global coupling scale s (motional order
parameter, h = 0.01 relative) and two B0 tilt angles (h = 0.01 rad).
Nuisance sets:  N0 none (the gate);  N1 s;  N2 s + B0 (2);  N3 s + all 27 coordinates orthogonal to the parameter direction
(B0 known; the exact null mode = rotation about B0 through the probe is projected out of the parameter direction).
For each gate parameter: marginal FI (Schur complement) with the easy data (S all + F[t < t_c]) and with all data
(S all + F all); gain = FI_all / FI_easy; CRB sd (A).  Also the generalised-eigenvalue gain spectrum of the 27-coordinate
Fisher matrix (all vs easy, S+F), after removing the null mode.
Attenuation variants (echo rows weighted by A(t) = 1, exp(-t/130 us), exp(-t/85 us); T3 ~ T2/0.15 with T2 from M2, see
t2_estimate.py; the easy/hard partition is kept at the constant-sigma t_c, which favours the quantum side).
Jacobians saved to nuisance_jacobians.npz.
"""
from __future__ import annotations

import json
import time

import numpy as np

import os

from fi_common import OUT, RAW, SP, dump, exact, setup

SIG = 0.01
DT, STEPS, REC = 2e-6, 160, 10


def rot(v, axis, ang):
    axis = axis / np.linalg.norm(axis)
    return v * np.cos(ang) + np.cross(axis, v) * np.sin(ang) + axis * (axis @ v) * (1 - np.cos(ang))


def main():
    t0 = time.time()
    cfg = setup("1UBQ", 19, 10, 0)
    bs = cfg["bs"]; nb = len(bs); N = cfg["N"]
    g = json.load(open(f"{RAW}/nmr_gate/1UBQ_p19_N10_o0_g0.json"))
    tcF = g["best_t_c_otoc_index"]; tcS = g["best_t_c_index"]
    X0, b0 = cfg["X0"], cfg["b0"]

    def data(X=None, b=None, scale=1.0):
        _, S, F = exact(cfg, X0 if X is None else X, dt=DT, steps=STEPS, rec=REC, b0=b, scale=scale)
        return np.concatenate([S[q] for q in bs]), np.concatenate([F[q] for q in bs])
    nt = STEPS // REC + 1

    def fd(fun, h):
        Sp, Fp = fun(+h); Sm, Fm = fun(-h)
        return (Sp - Sm) / (2 * h), (Fp - Fm) / (2 * h)
    # coordinates
    JxS, JxF = [], []
    for i in range(1, N):
        for c in range(3):
            def f(d, i=i, c=c):
                X = X0.copy(); X[i, c] += d
                return data(X)
            a, b_ = fd(f, 0.02); JxS.append(a); JxF.append(b_)
    JxS = np.array(JxS).T; JxF = np.array(JxF).T                       # (n_obs, 27)
    sS, sF = fd(lambda d: data(scale=1.0 + d), 0.01)
    e1 = np.cross(b0, [1.0, 0, 0]); e1 /= np.linalg.norm(e1); e2 = np.cross(b0, e1)
    bS1, bF1 = fd(lambda d: data(b=rot(b0, e1, d)), 0.01)
    bS2, bF2 = fd(lambda d: data(b=rot(b0, e2, d)), 0.01)
    secs_jac = time.time() - t0
    np.savez_compressed(os.path.join(OUT, "nuisance_jacobians.npz"), JxS=JxS, JxF=JxF, sS=sS, sF=sF, bS1=bS1, bF1=bF1, bS2=bS2, bF2=bF2,
                        X0=X0, b0=b0, bs=np.array(bs), times=np.arange(nt) * REC * DT)
    tus = np.tile(np.arange(nt) * REC * DT * 1e6, nb)
    ATT = {"none": np.ones(nb * nt), "EXP_T3=130us": np.exp(-tus / 130.0), "EXP_T3=85us": np.exp(-tus / 85.0)}
    JxF_raw, sF_raw, bF1_raw, bF2_raw = JxF, sF, bF1, bF2
    # parameter directions in the 27-coordinate space
    rvec = np.concatenate([np.cross(b0, X0[i] - X0[0]) for i in range(1, N)]); rhat = rvec / np.linalg.norm(rvec)
    null_check = float(np.linalg.norm(JxF @ rhat) / np.linalg.norm(JxF, 2))
    easyF = np.tile(np.arange(nt) < tcF, nb); allm = np.ones(nb * nt, bool)
    res = dict(cluster="1UBQ_p19_N10_o0_g0", tcF=tcF, tcS=tcS, secs_jacobians=secs_jac, null_mode_rel_norm=null_check)

    def schur(Jp, Jn):
        """marginal FI of the parameter column(s) Jp given nuisance columns Jn."""
        if Jn is None or Jn.shape[1] == 0:
            return float(Jp @ Jp) / SIG ** 2
        U, s, _ = np.linalg.svd(Jn, full_matrices=False)
        U = U[:, s > 1e-9 * s.max()]
        r = Jp - U @ (U.T @ Jp)
        return float(r @ r) / SIG ** 2

    for att, A in ATT.items():
        JxF, sF, bF1, bF2 = JxF_raw * A[:, None], sF_raw * A, bF1_raw * A, bF2_raw * A
        res.setdefault("attenuation", {})[att] = {}
        print("######## attenuation", att)
        for p in cfg["params"]:
            v = np.zeros(3 * (N - 1))
            for (i, u) in p["move"]:
                v[3 * (i - 1):3 * i] = u
            vp = v - (v @ rhat) * rhat
            lin_check = float(np.linalg.norm(JxF @ v - JxF @ vp) / max(np.linalg.norm(JxF @ v), 1e-30))
            # complement basis of vp
            Q, _ = np.linalg.qr(np.column_stack([vp / np.linalg.norm(vp), np.eye(len(v))]))
            C = Q[:, 1:len(v)]                                              # 26 directions orthogonal to vp
            out = {}
            for dset in ("F", "S+F"):
                for win, mF in (("easy", easyF), ("all", allm)):
                    def stack(JS, JF):
                        if dset == "F":
                            return JF[mF]
                        return np.concatenate([JS, JF[mF]])                 # transfer: all points (classically exact)
                    Jp = stack(JxS @ vp, JxF @ vp)
                    nuis = {"N0": None,
                            "N1": stack(sS[:, None], sF[:, None]),
                            "N2": stack(np.column_stack([sS, bS1, bS2]), np.column_stack([sF, bF1, bF2])),
                            "N3": stack(np.column_stack([sS, JxS @ C]), np.column_stack([sF, JxF @ C]))}
                    for nk, Jn in nuis.items():
                        out[f"{dset}|{win}|{nk}"] = schur(Jp, Jn)
            summ = {}
            for dset in ("F", "S+F"):
                for nk in ("N0", "N1", "N2", "N3"):
                    fa, fe = out[f"{dset}|all|{nk}"], out[f"{dset}|easy|{nk}"]
                    summ[f"{dset}|{nk}"] = dict(FI_all=fa, FI_easy=fe, gain=fa / max(fe, 1e-300),
                                               sd_all_A=float(1 / np.sqrt(fa)) if fa > 0 else None,
                                               sd_easy_A=float(1 / np.sqrt(fe)) if fe > 0 else None)
            res["attenuation"][att][p["name"]] = dict(raw=out, summary=summ, v_null_overlap=float(v @ rhat), lin_check=lin_check)
            print(f"== {p['name']}  (v.rhat = {v @ rhat:+.3f})")
            for k, z in summ.items():
                print(f"   {k:8s} FI all {z['FI_all']:10.1f} easy {z['FI_easy']:10.1f} gain {z['gain']:8.2f}  sd all {z['sd_all_A']:.4f} A  easy "
                      f"{z['sd_easy_A'] if z['sd_easy_A'] is None else round(z['sd_easy_A'], 4)} A")
        # gain spectrum over the 27 coordinates (S+F), null mode removed, plus s as a coordinate
        B = np.linalg.qr(np.column_stack([rhat, np.eye(len(rhat))]))[0][:, 1:len(rhat)]
        for nk, extra in (("coords", None), ("coords+s", (sS, sF))):
            JS_ = JxS @ B; JF_ = JxF @ B
            if extra is not None:
                JS_ = np.column_stack([JS_, extra[0]]); JF_ = np.column_stack([JF_, extra[1]])
            Fall = (JS_.T @ JS_ + JF_.T @ JF_) / SIG ** 2
            Feasy = (JS_.T @ JS_ + JF_[easyF].T @ JF_[easyF]) / SIG ** 2
            FS = JS_.T @ JS_ / SIG ** 2
            reg = 1e-12 * np.trace(Fall)
            L = np.linalg.cholesky(Feasy + reg * np.eye(len(Feasy)))
            Li = np.linalg.inv(L)
            w = np.sort(np.linalg.eigvalsh(Li @ Fall @ Li.T))[::-1]
            ev_all = np.sort(np.linalg.eigvalsh(Fall))[::-1]; ev_easy = np.sort(np.linalg.eigvalsh(Feasy))[::-1]
            ev_S = np.sort(np.linalg.eigvalsh(FS))[::-1]
            res["attenuation"][att][f"gain_spectrum_{nk}"] = dict(gains=w.tolist(), n_dirs_gain_gt2=int((w > 2).sum()), n_dirs_gain_gt10=int((w > 10).sum()),
                                              eig_all=ev_all.tolist(), eig_easy=ev_easy.tolist(), eig_S_only=ev_S.tolist(),
                                              n_identified_sd_lt_0p1A_all=int((ev_all > 100).sum()), n_identified_sd_lt_0p1A_easy=int((ev_easy > 100).sum()),
                                              n_identified_sd_lt_0p1A_S_only=int((ev_S > 100).sum()))
            z = res["attenuation"][att][f"gain_spectrum_{nk}"]
            print(f"gain spectrum ({nk}, S+F, dim {len(w)}): top {np.round(w[:6], 1).tolist()}  #>2: {z['n_dirs_gain_gt2']}  #>10: {z['n_dirs_gain_gt10']}  "
                  f"#dirs with sd<0.1A: all {z['n_identified_sd_lt_0p1A_all']} easy {z['n_identified_sd_lt_0p1A_easy']} S-only {z['n_identified_sd_lt_0p1A_S_only']}")
    res["secs"] = time.time() - t0
    print("secs", round(res["secs"], 1), "null-mode check", null_check)
    dump(res, "nuisance.json")


if __name__ == "__main__":
    main()
