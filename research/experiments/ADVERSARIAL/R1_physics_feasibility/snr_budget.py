"""R1 physics-feasibility audit, part 4: measurement-time budget for the site-resolved echo (analytic).

sigma = 0.01 per time point is the noise the RAW Fisher information assumes, in units of the FULL polarization of the
single probe proton at t = 0.  Static 1H lines of a protonated protein are 35-47 kHz wide (scales.json, Gaussian FWHM
from the computed Van Vleck M2), i.e. wider than the whole 1H chemical-shift range, so a single-proton signal can only be
prepared/read through a site-specific heteronuclear label (13C or 15N; the polarization-echo protocol of
Zhang-Meier-Ernst 1992 used by the Pastawski group and, with a single 13C, by Zhang et al. arXiv:2510.19550).
Assumptions (INFERENCE, stated as ranges, not measured here):
  s1   per-scan SNR of the full single-site polarization after injection (13C/15N -> 1H) and read-back (1H -> 13C/15N),
       for a ~10-20 mg protein sample (~1e18 molecules, ONE labelled site per molecule): 0.1, 0.3, 1, 3.
  Trec recycle delay (1H T1 of a protein solid; longer when frozen): 2 s.
Required scans for sigma at time t with reversal envelope A(t):  n = (1 / (sigma * s1 * A(t)))^2.
We report (i) days per time point at A = 1, (ii) days per point at the echo-FI midpoint t50 under the literature
envelopes (generous: T2 = isolated-cluster T2, forward time only), (iii) days to recover the ideal hard-window FI of one probe
(all n_b butterfly label patterns, each a separately labelled sample) = (ideal time for all hard points) / retention.
Output: snr_budget.json.  No simulation; milliseconds.
"""
from __future__ import annotations

import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    env = json.load(open(os.path.join(HERE, "reversal_envelope.json")))
    sc = {r["file"]: r for r in json.load(open(os.path.join(HERE, "scales.json")))["jobs"]}
    sigma, Trec = 0.01, 2.0
    s1_list = [0.1, 0.3, 1.0, 3.0]
    out = dict(assumptions=dict(sigma=sigma, Trec_s=Trec, s1=s1_list), jobs=[])
    for r in env:
        s = sc[r["file"]]
        sub = "nmr_gate_hn" if s["hn_only"] else "nmr_gate"
        n_b = len(json.load(open(os.path.join(HERE, "..", "..", "..", "results", "RAW", sub, r["file"])))["bs"])
        n_hard = (17 if not s["hn_only"] else 21) - int(round(r["t_c_us"] / (20 if not s["hn_only"] else 50)))
        row = dict(file=r["file"], n_hard_points=n_hard, n_butterfly_label_patterns=n_b, per_s1={})
        for s1 in s1_list:
            n0 = (1.0 / (sigma * s1)) ** 2
            d = dict(days_per_point_A1=n0 * Trec / 86400)
            for key in ("cluster|generous|PE_gauss_T3=4T2", "cluster|generous|LE_logistic_T3=6.7T2",
                        "network|generous|LE_logistic_T3=6.7T2"):
                c = r["cases"][key]
                A50 = c["A_at_t50"]
                d[f"days_per_point_at_t50|{key}"] = n0 / max(A50, 1e-300) ** 2 * Trec / 86400
                d[f"days_to_recover_ideal_hardFI|{key}"] = n_b * n_hard * n0 * Trec / 86400 / max(c["hard_retained"], 1e-300)
            row["per_s1"][str(s1)] = d
        out["jobs"].append(row)
        d1 = row["per_s1"]["1.0"]
        print(r["file"], "A=1: %.2f d/pt" % d1["days_per_point_A1"],
              "| t50 PE4: %.3g d/pt" % d1["days_per_point_at_t50|cluster|generous|PE_gauss_T3=4T2"],
              "| t50 LE6.7: %.3g d/pt" % d1["days_per_point_at_t50|cluster|generous|LE_logistic_T3=6.7T2"],
              "| recover hard FI (LE6.7, cluster): %.3g d" % d1["days_to_recover_ideal_hardFI|cluster|generous|LE_logistic_T3=6.7T2"],
              "| (PE4): %.3g d" % d1["days_to_recover_ideal_hardFI|cluster|generous|PE_gauss_T3=4T2"])
    json.dump(out, open(os.path.join(HERE, "snr_budget.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
