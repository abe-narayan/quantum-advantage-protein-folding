"""Compare the N = 22 single-site echo (p19, site 8, 320 us) with the model predictions made from the lane's N = 12-20
ladder (lane N = 20 value and this audit's independent N = 20 replication).  Also reports sector-resolved
microcanonical values f_k = T_k / d_k+ against N = 20 for completed sectors.  Writes n22_summary.json (atomic)."""
from __future__ import annotations

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = os.path.join(HERE, "runs")
LADDER = {12: 0.4054, 14: 0.4093, 16: 0.2867, 18: 0.2713, 20: 0.2451}      # lane ladder, p19 site 8, 320 us
PRED_N22 = {  # from resource_audit.json -> D (fits on N = 12..20); see README section 4
    "lane exponential (all 5 points)": 0.202,
    "c/N through origin (F20*20/22)": LADDER[20] * 20 / 22,
    "1/N with offset, last 3": 0.084 + 3.28 / 22,
    "1/N^2 with offset, last 3": 0.176 + 28.89 / 22 ** 2,
    "exponential without N=14 (best fit)": 0.239,
}


def main():
    n20 = json.load(open(os.path.join(R, "pplus_1UBQ_p19_N20_site8_seed2026.json")))
    n22 = json.load(open(os.path.join(R, "pplus_1UBQ_p19_N22_site8_seed2026.json")))
    out = dict(ladder_lane=LADDER, N20_this_audit=n20["F"], predictions_N22=PRED_N22)
    sec = {}
    for k, v in sorted(n22["done"].items(), key=lambda kv: -int(kv[0])):
        f22 = v["T"]["160"] / v["dplus"]
        k20 = int(k) - 1                     # same magnetisation offset from half filling
        f20 = (n20["done"][str(k20)]["T"]["160"] / n20["done"][str(k20)]["dplus"]) if str(k20) in n20["done"] else None
        sec[k] = dict(dim=v["dim"], dplus=v["dplus"], f22=f22, f20_same_offset=f20, cpu_s=v["cpu_s"])
    out["sector_resolved"] = sec
    # partial-information bracket (INFERENCE): missing sectors k take the N = 20 value at the same offset from half
    # filling, shifted by delta in [min observed shift, 0] (observed shifts are negative and grow with the offset)
    N = 22
    shifts = [v["f22"] - v["f20_same_offset"] for v in sec.values() if v["f20_same_offset"] is not None]
    brackets = {}
    for lab, dlt in (("shift_0", 0.0), ("shift_min_observed", min(shifts) if shifts else 0.0),
                     ("shift_2x_min_observed", 2 * min(shifts) if shifts else 0.0)):
        s = 0.0
        for k in range(N // 2 + 1):
            dplus = math.comb(N - 1, k)
            z = math.comb(N - 1, k) - (math.comb(N - 1, k - 1) if k >= 1 else 0)
            if str(k) in n22["done"]:
                f = n22["done"][str(k)]["T"]["160"] / dplus
            else:
                k20 = k - 1
                f20 = n20["done"][str(k20)]["T"]["160"] / n20["done"][str(k20)]["dplus"] if k20 >= 0 else 1.0
                f = min(1.0, f20 + dlt)
            s += (4 * dplus * f - 2 * z) if 2 * k < N else (2 * dplus * f - z)
        brackets[lab] = s / 2.0 ** N
    out["F22_estimate_if_incomplete"] = brackets
    out["observed_sector_shifts"] = shifts
    out["cpu_s_N22"] = sum(v["cpu_s"] for v in n22["done"].values())
    out["sectors_done"] = len(n22["done"])
    if "F" in n22:
        F22 = n22["F"]["160"]
        out["F22"] = F22
        out["typicality_err"] = 2 * 2 ** (-11)
        out["residual_vs_prediction"] = {k: F22 - p for k, p in PRED_N22.items()}
        out["Delta20_lane"] = F22 - LADDER[20]
        out["Delta20_audit"] = F22 - n20["F"]["160"]
        out["F_times_N"] = {"20_lane": LADDER[20] * 20, "20_audit": n20["F"]["160"] * 20, "22": F22 * 22}
        # refits with N = 22 added (1/N all-from-16, 1/N last 3, exp without 14)
        import numpy as np
        Ns = [16, 18, 20, 22]
        F = [LADDER[16], LADDER[18], LADDER[20], F22]
        for lab, f in (("invN_16_22", lambda n: 1.0 / n), ("invN2_16_22", lambda n: 1.0 / n ** 2)):
            A = np.vstack([np.ones(4), f(np.asarray(Ns, float))]).T
            c, *_ = np.linalg.lstsq(A, np.asarray(F), rcond=None)
            rms = float(np.sqrt(np.mean((A @ c - F) ** 2)))
            Nsig = abs(c[1]) / 0.01 if lab.startswith("invN_") else math.sqrt(abs(c[1]) / 0.01)
            out[lab] = dict(Finf=float(c[0]), c=float(c[1]), rms=rms, N_sigma=Nsig)
    if "F22" in out:
        import importlib.util
        spec = importlib.util.spec_from_file_location("ra", os.path.join(HERE, "resource_audit.py"))
        ra = importlib.util.module_from_spec(spec); spec.loader.exec_module(ra)
        fits = {}
        for lab, Ns in (("exp_12_22", [12, 14, 16, 18, 20, 22]), ("exp_drop14", [12, 16, 18, 20, 22]),
                        ("exp_16_22", [16, 18, 20, 22])):
            F = [LADDER[n] for n in Ns if n != 22] + [out["F22"]]
            Finf, A, xi, rms = ra.fit_exp(Ns, F)
            fits[lab] = dict(Finf=Finf, A=A, xi=xi, rms_over_sigma=rms / 0.01, N_sigma=ra.n_sigma_exp(A, xi))
        for lab, Ns, f, p in (("invN_18_22", [18, 20, 22], lambda n: 1.0 / n, 1), ("invN_12_22", [12, 14, 16, 18, 20, 22], lambda n: 1.0 / n, 1),
                              ("invN2_18_22", [18, 20, 22], lambda n: 1.0 / n ** 2, 2)):
            F = [LADDER[n] for n in Ns if n != 22] + [out["F22"]]
            Finf, c, rms = ra.fit_lin(Ns, F, f)
            fits[lab] = dict(Finf=Finf, c=c, rms_over_sigma=rms / 0.01,
                             N_sigma=(abs(c) / 0.01) if p == 1 else math.sqrt(abs(c) / 0.01))
        out["refits_with_N22"] = fits
        out["preregistered_step_N20_to_22"] = dict(delta=abs(out["Delta20_lane"]), thr=0.01 + 2 * (2 ** -10 * 2 ** 0.5 + 2 * 2 ** -11),
                                                    note="single site only; threshold as lane (sigma + 2(err_N + err_N+2))")
    json.dump(out, open(os.path.join(HERE, "n22_summary.json.tmp"), "w"), indent=1)
    os.replace(os.path.join(HERE, "n22_summary.json.tmp"), os.path.join(HERE, "n22_summary.json"))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
