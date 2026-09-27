"""R1_fi_method / zero-cost summary of all tests -> summary.json (numbers quoted in README.md).
Adds three derived statistics:
  (1) N=8 fits: slope-calibrated classical estimator error.  A classical model with derivative J_c responds to a true change
      of phi with slope (J_c.J_e)/(J_c.J_c); the noise-equivalent sd of a calibrated estimate is sd_exact / cos(J_c, J_e) >=
      sd_exact.  RMSE_eff = sqrt(phi_hat^2 + sd_eff^2); gain_eff = (min over {full-window fit, easy-window fit} RMSE_eff /
      sd_exact)^2 = repetitions factor the exact (quantum) forward model saves.
  (2) per-job literature-anchored attenuation: T3 = T2_env / 0.15 (t2_estimate.json), EXP model, t_c recomputed and frozen;
      also 0.5x and 2x the anchor.
  (3) experiment accounting: the echo F_ab needs one perturbation experiment per butterfly spin b (n_b = 4 here) while all
      transfer S_ab(t) are read out in one experiment per time point; FI per experiment -> echo FI / n_b.
"""
from __future__ import annotations

import json
import os

import numpy as np

from fi_common import OUT, dump
import noise_models as NM

J = lambda n: json.load(open(os.path.join(OUT, n)))


def n8_fits():
    out = {}
    for lab in ("eps1e-3", "eps3e-4", "w4"):
        f = os.path.join(OUT, f"n8_fit_{lab}.json")
        if not os.path.exists(f):
            continue
        r = json.load(open(f))
        rows = {}
        for pn, d in r["params"].items():
            for key in ("S", "F"):
                z = d[key]
                cos = max(z["cos_Jc_Je"], 1e-6)
                sd_eff = z["sd_exact_full"] / cos
                rm_full = float(np.hypot(z["phi_hat"], sd_eff))
                # easy-window fit, same calibration (cos over the full window is used as a proxy)
                rm_easy = float(np.hypot(z["phi_lin_Jc_easy"], z["sd_exact_easy"] / cos)) if np.isfinite(z["sd_exact_easy"]) else float("inf")
                rows[f"{pn}|{key}"] = dict(tc_gate=z["tc_gate"], phi_hat_A=z["phi_hat"], sd_exact_A=z["sd_exact_full"],
                                           bias_over_sd=abs(z["phi_hat"]) / z["sd_exact_full"], cos_Jc_Je=z["cos_Jc_Je"],
                                           gain_gate=z["gain_gate"], gain_eff=(min(rm_full, rm_easy) / z["sd_exact_full"]) ** 2,
                                           best_window="full" if rm_full <= rm_easy else "easy")
        out[lab] = rows
    return out


def anchored():
    t2 = {z["job"]: z for z in J("t2_estimate.json")["T2"]}
    jobs = NM.load_jobs()
    res = {}
    for fac in (0.5, 1.0, 2.0):
        rows = []
        for name, r in jobs:
            hn = "HN" in name
            key = name.split("_N")[0] + f"_o{r['orient']}"   # file name carries the original probe index
            T3 = t2[key]["T3_anchor_us"]["env"] * fac
            rec = NM.analyse("EXP", T3, [(name, r)])
            base = {z["param"]: z["tcF"] for z in NM.analyse("EXP", None, [(name, r)])}
            t = np.asarray(r["times"]) * 1e6
            A = np.exp(-t / T3)
            for z in rec:
                p = next(p for p in NM.unique(r) if p["name"] == z["param"])
                fiF = sum((np.asarray(p["dF"][b]) * A) ** 2 for b in p["dF"]) / NM.SIG ** 2
                fiS = np.asarray(p["FI_t"]); tcS = r.get("best_t_c_index", len(t)); tcf = base[z["param"]]
                nb = len(p["dF"])
                gj_frozen = (fiS.sum() + fiF.sum()) / max(fiS[:tcS].sum() + fiF[:tcf].sum(), 1e-300)
                gj_frozen_perexp = (fiS.sum() + fiF.sum() / nb) / max(fiS[:tcS].sum() + fiF[:tcf].sum() / nb, 1e-300)
                rows.append(dict(job=name, param=z["param"], T3_us=T3, gain_joint_recomputed_tc=z["gain_joint"],
                                 gain_joint_frozen_tc=float(gj_frozen), gain_joint_frozen_tc_per_experiment=float(gj_frozen_perexp),
                                 frac_hard_recomputed=z["frac_hard"], FI_F_over_S=z["ratio_FI_F_over_S"], hn=hn))
        def med(k, sel):
            v = [z[k] for z in rows if sel(z)]
            return float(np.median(v)), float(np.max(v))
        res[f"T3=anchor*{fac}"] = dict(rows=rows, **{f"{grp}_{k}_median_max": med(k, s) for grp, s in
                                                     (("dense", lambda z: not z["hn"]), ("HN", lambda z: z["hn"]), ("all", lambda z: True))
                                                     for k in ("gain_joint_recomputed_tc", "gain_joint_frozen_tc",
                                                               "gain_joint_frozen_tc_per_experiment", "FI_F_over_S")})
    return res


def per_experiment_no_attenuation():
    jobs = NM.load_jobs()
    rows = []
    for name, r in jobs:
        tcS = r.get("best_t_c_index", len(r["times"]))
        tcF = r.get("best_t_c_otoc_index")
        for p in NM.unique(r):
            fiS = np.asarray(p["FI_t"]); fiF = np.asarray(p["FI_otoc_t"]); nb = len(p["dF"])
            rows.append(dict(job=name, param=p["name"], FI_F_over_S=float(fiF.sum() / fiS.sum()),
                             FI_F_over_S_per_experiment=float(fiF.sum() / nb / fiS.sum()),
                             gain_joint=float((fiS.sum() + fiF.sum()) / (fiS[:tcS].sum() + fiF[:tcF].sum())),
                             gain_joint_per_experiment=float((fiS.sum() + fiF.sum() / nb) / (fiS[:tcS].sum() + fiF[:tcF].sum() / nb)),
                             gain_F_only=float(fiF.sum() / max(fiF[:tcF].sum(), 1e-300))))
    keys = ("FI_F_over_S", "FI_F_over_S_per_experiment", "gain_joint", "gain_joint_per_experiment", "gain_F_only")
    return dict(rows=rows, **{f"{k}_min_median_max": [float(np.min([z[k] for z in rows])), float(np.median([z[k] for z in rows])),
                                                     float(np.max([z[k] for z in rows]))] for k in keys})


def dephasing_gate_panel():
    d = J("dephased_echo.json")
    out = {}
    for g, z in d["gammas"].items():
        adv = z["adversaries"]
        gate_panel = {k: v for k, v in adv.items() if "3e-05" not in k}
        best = max(gate_panel, key=lambda k: gate_panel[k]["tcF"]); tcF = gate_panel[best]["tcF"]
        rows = {}
        for n, p in z["params"].items():
            fS, fF = np.asarray(p["FI_t_S"]), np.asarray(p["FI_t_F"])
            rows[n] = dict(frac_hard_F=float(fF[tcF:].sum() / max(fF.sum(), 1e-300)),
                           gain_joint_F=float((fS.sum() + fF.sum()) / max(fS.sum() + fF[:tcF].sum(), 1e-300)),
                           FI_F_over_S=float(fF.sum() / fS.sum()))
        out[g] = dict(best_gate_panel=best, tcF_gate_panel=tcF, best_all=z["best_F"], tcF_all=z["tcF"], rows=rows)
    return out


def main():
    s = dict(n8_fits=n8_fits(), anchored_attenuation=anchored(), per_experiment_no_attenuation=per_experiment_no_attenuation(),
             dephasing_gate_panel=dephasing_gate_panel())
    for lab, rows in s["n8_fits"].items():
        for k, z in rows.items():
            print(f"N8 fit {lab:7s} {k:22s} tc {z['tc_gate']:2d} phi_hat {z['phi_hat_A']:+.4f} A  |bias|/sd {z['bias_over_sd']:6.1f}  cos {z['cos_Jc_Je']:+.2f} "
                  f" gain_gate {z['gain_gate']:10.1f}  gain_eff {z['gain_eff']:8.2f} ({z['best_window']})")
    for k, v in s["anchored_attenuation"].items():
        print(k, {kk: [round(x, 2) for x in vv] for kk, vv in v.items() if kk != "rows"})
    pe = s["per_experiment_no_attenuation"]
    print("no attenuation, per experiment:", {k: [round(x, 2) for x in v] for k, v in pe.items() if k != "rows"})
    for g, z in s["dephasing_gate_panel"].items():
        print("dephasing gamma", g, "gate-panel best", z["best_gate_panel"], "tcF", z["tcF_gate_panel"], "| all-adversary best", z["best_all"], z["tcF_all"],
              {n: (round(r["frac_hard_F"], 3), round(r["gain_joint_F"], 2), round(r["FI_F_over_S"], 2)) for n, r in z["rows"].items()})
    dump(s, "summary.json")


if __name__ == "__main__":
    main()
