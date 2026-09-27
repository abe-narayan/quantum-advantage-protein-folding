"""R1_fi_method / T2 anchor for the echo-attenuation model.
Van Vleck second moment of the probe proton's dipolar line (like spins, secular):  M2_a = (9/4) sum_j d_aj^2  with d_aj as
in qapf.nmr.spins.couplings (rad/s; H = sum d (3 IzIz - I.I)); Gaussian FID time constant T2 = 1/sqrt(M2) (DERIVED,
standard; the exact T2 convention of arXiv:2112.00607 was NOT verified, so T3 = T2/0.15 is an order-of-magnitude anchor).
Computed (a) over the model cluster only (sets the time scale of the simulated dynamics) and (b) over every proton of the
protein within 12 A (sets the real line width), at the job's B0 orientation and powder-averaged (200 random B0).
Also re-runs the noise-model analysis with the classical failure time FROZEN at its constant-sigma value, to separate
FI attenuation from the later classical failure.
"""
from __future__ import annotations

import json
import os

import numpy as np

from fi_common import ROOT, RAW, SP, dump, random_b0, setup
import noise_models as NM

JOBS = [("1PGA", 325, 0, False), ("1PGA", 390, 0, False), ("1UBQ", 19, 0, False), ("1UBQ", 19, 1, False),
        ("1PGA", 260, 0, True), ("1PGA", 325, 0, True), ("1PGA", 390, 0, True), ("1UBQ", 19, 0, True), ("1UBQ", 359, 0, True),
        ("1UBQ", 487, 0, True), ("1UBQ", 548, 0, True)]


def m2(Xa, Xo, b0):
    v = Xo - Xa
    r = np.linalg.norm(v, axis=1)
    c = (v @ b0) / r
    d = SP.D1A / r ** 3 * (3 * c ** 2 - 1) / 2
    return 2.25 * float((d ** 2).sum())


def main():
    rng = np.random.default_rng(5)
    B = rng.standard_normal((200, 3)); B /= np.linalg.norm(B, axis=1, keepdims=True)
    rows = []
    for pdb, probe, orient, hn in JOBS:
        cfg = setup(pdb, probe, 10, orient, hn_only=hn)
        names, xyz, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
        if hn:
            keep = [i for i, n in enumerate(names) if n.startswith("H/")]
            xyz = xyz[keep]
            pr = keep.index(probe)
        else:
            pr = probe
        Xa = xyz[pr]
        dd = np.linalg.norm(xyz - Xa, axis=1)
        env = xyz[(dd > 1e-6) & (dd < 12.0)]
        X0 = cfg["X0"]
        m_cl = m2(X0[0], X0[1:], cfg["b0"]); m_env = m2(Xa, env, cfg["b0"])
        m_env_pow = float(np.mean([m2(Xa, env, b) for b in B]))
        T2c, T2e, T2p = 1 / np.sqrt(m_cl), 1 / np.sqrt(m_env), 1 / np.sqrt(m_env_pow)
        rows.append(dict(job=f"{pdb}{'HN' if hn else ''}_p{probe}_o{orient}", T2_cluster_us=T2c * 1e6, T2_env12A_us=T2e * 1e6,
                         T2_env12A_powder_us=T2p * 1e6, T3_anchor_us=dict(cluster=T2c / 0.15 * 1e6, env=T2e / 0.15 * 1e6,
                                                                           env_powder=T2p / 0.15 * 1e6)))
        print(f"{rows[-1]['job']:18s} T2 cluster {T2c*1e6:6.1f} us  env(12A) {T2e*1e6:6.1f} us  env powder {T2p*1e6:6.1f} us  "
              f"-> T3 ~ T2/0.15 = {T2c/0.15*1e6:6.0f} / {T2e/0.15*1e6:6.0f} / {T2p/0.15*1e6:6.0f} us")
    # frozen-t_c variant of the noise models
    jobs = NM.load_jobs()
    frozen = {}
    orig_thr_analyse = NM.analyse

    def analyse_frozen(model, T3, jobs_, include_c2=False):
        # compute t_c with T3=None (constant sigma), then FI with attenuation
        base = {(z["job"], z["param"]): z["tcF"] for z in orig_thr_analyse(model if model != "GAU" else "EXP", None, jobs_, include_c2)}
        rows_ = orig_thr_analyse(model, T3, jobs_, include_c2)
        out = []
        for z in rows_:
            tco = base[(z["job"], z["param"])]
            name, r = next((n, r) for n, r in jobs_ if n == z["job"])
            p = next(p for p in NM.unique(r) if p["name"] == z["param"])
            t = np.asarray(r["times"]) * 1e6
            A = np.ones_like(t) if T3 is None else (np.exp(-(t / T3) ** 2) if model == "GAU" else np.exp(-t / T3))
            Fex = {b: np.asarray(r["F_exact"][b]) for b in r["F_exact"]}
            if model == "RATIO":
                fiF = sum((np.asarray(p["dF"][b]) * A / np.sqrt(1 + Fex[b] ** 2)) ** 2 for b in p["dF"]) / NM.SIG ** 2
            else:
                fiF = sum((np.asarray(p["dF"][b]) * A) ** 2 for b in p["dF"]) / NM.SIG ** 2
            fiS = np.asarray(p["FI_t"]); tcS = r.get("best_t_c_index", len(t))
            z = dict(z); z.update(tcF=tco, frac_hard=float(fiF[tco:].sum() / max(fiF.sum(), 1e-300)),
                                  gain=float(fiF.sum() / max(fiF[:tco].sum(), 1e-300)),
                                  gain_joint=float((fiS.sum() + fiF.sum()) / max(fiS[:tcS].sum() + fiF[:tco].sum(), 1e-300)))
            out.append(z)
        return out
    for model in ("EXP", "RATIO"):
        for T3 in NM.T3S:
            rr = analyse_frozen(model, T3, jobs)
            s = NM.summarise(rr)
            frozen[f"{model}_T3={T3}_frozen_tc"] = s
            print(f"FROZEN t_c {model:5s} T3={str(T3):5s} f_hard med dense {s['dense']['median_frac_hard']:.3f} HN {s['hn']['median_frac_hard']:.3f} | "
                  f"joint gain med dense {s['dense']['median_gain_joint']:.2f} HN {s['hn']['median_gain_joint']:.2f} | FI_F/FI_S dense "
                  f"{s['dense']['median_ratio_FI_F_over_S']:.2f} HN {s['hn']['median_ratio_FI_F_over_S']:.2f}")
    print("wrote", dump(dict(T2=rows, frozen_tc=frozen), "t2_estimate.json"))


if __name__ == "__main__":
    main()
