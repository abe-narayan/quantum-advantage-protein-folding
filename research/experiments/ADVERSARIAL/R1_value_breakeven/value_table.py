"""R1 value lens, part 5: the echo window next to the classical ways of getting the same structural information.

Merges MEASURED-derived numbers (fi_value.json, model_bias.json, lightcone.json, breakeven.json) with a comparator
table of established methods.  Comparator figures are typical textbook / domain values and are tagged
INFERENCE-unverified unless a source was checked this session (checked: Zhang et al. arXiv:2510.19550 abstract;
O'Brien et al. PRX Quantum 3, 030345 abstract; Haener & Steiger arXiv:1704.01127 abstract).
Also: sigma sweep (CRB is linear in sigma) and the fraction of parameters whose CRB improves > 2x with the hard window.
Output: value_table.json.  Cost: < 1 s.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    fv = json.load(open(os.path.join(HERE, "fi_value.json")))
    mb = json.load(open(os.path.join(HERE, "model_bias.json")))
    lc = json.load(open(os.path.join(HERE, "lightcone.json")))
    be = json.load(open(os.path.join(HERE, "breakeven.json")))
    out = {}
    # ---------------------------------------------------------------- sigma sweep of median CRBs (DERIVED: linear in sigma)
    sweep = {}
    for net in ("dense", "amide-only"):
        a = fv["aggregate"][net]
        sweep[net] = {f"sigma={s}": dict(classical_route_median_A=a["CRB_classical_marg"]["median"] * s / 0.01,
                                          quantum_median_A=a["CRB_quantum_marg"]["median"] * s / 0.01,
                                          transfer_only_median_A=a["CRB_transfer_marg"]["median"] * s / 0.01)
                      for s in (0.01, 0.03, 0.1)}
        g = [x for r in fv["rows"] if r["network"] == net and "g_param" in r for x in r["g_param"]]
        sweep[net]["frac_params_CRB_gain_gt_2x (g>4)"] = float(np.mean(np.asarray(g) > 4))
        sweep[net]["frac_params_CRB_gain_gt_3x (g>9)"] = float(np.mean(np.asarray(g) > 9))
        eo = [x for r in fv["rows"] if r["network"] == net and "FI_echo_over_transfer" in r for x in r["FI_echo_over_transfer"]]
        sweep[net]["diag_FI_echo_over_transfer"] = dict(min=float(min(eo)), median=float(np.median(eo)), max=float(max(eo)))
    out["sigma_sweep"] = sweep
    # ---------------------------------------------------------------- truncation bias summary (MEASURED-derived)
    bias = {}
    for fn, rec in mb.items():
        for k, v in rec.items():
            if isinstance(v, dict) and "_all_" in k:
                bias[f"{fn}|{k}"] = dict(max_abs_bias_A=float(np.max(np.abs(v["bias_A"]))),
                                         max_bias_over_crb=float(np.max(v["bias_over_crb"])),
                                         max_misfit_sigma=v["max_misfit_over_sigma"])
    out["truncation_bias"] = bias
    # ---------------------------------------------------------------- light cone summary (INFERENCE, calibrated heuristic)
    lcs = {}
    for net in ("dense", "amide-only"):
        js = [j for j in lc["jobs"] if j["network"] == net]
        lcs[net] = {q: dict(median_calibration=[min(j[f"Neff_at_{q}_infl_med"] for j in js), max(j[f"Neff_at_{q}_infl_med"] for j in js)],
                            full_bracket=[min(j[f"Neff_at_{q}_infl_slow"] for j in js), max(j[f"Neff_at_{q}_infl_fast"] for j in js)])
                    for q in ("t50", "t90")}
    out["light_cone_Neff"] = lcs
    # ---------------------------------------------------------------- comparator table
    d, h = fv["aggregate"]["dense"], fv["aggregate"]["amide-only"]
    out["comparators"] = [
        dict(method="1H dipolar echo (OTOC), static oriented sample, exact forward model [this program]",
             distances=f"{d['r']['min']:.1f}-{d['r']['max']:.1f} A (dense), {h['r']['min']:.1f}-{h['r']['max']:.1f} A (amide-only); MEASURED parameter set",
             precision=f"CRB median {d['CRB_quantum_marg']['median']:.3f} A dense / {h['CRB_quantum_marg']['median']:.3f} A amide at sigma=0.01 "
                       f"(classical-route {d['CRB_classical_marg']['median']:.3f} / {h['CRB_classical_marg']['median']:.3f} A); "
                       "truncation bias of the N=10 model 0.06-0.6 A (MEASURED-derived)",
             throughput="3-4 local parameters per probe data set (n_b x n_t = 63-84 site-resolved points at SNR 100); site resolution "
                        "in a static dense 1H network is not available without isotopic dilution (INFERENCE)",
             interpretation="needs quantum forward model only if N_eff > ~47-51 (exact-classical memory wall)",
             tag="MEASURED/DERIVED (model); physical data never acquired for a protein"),
        dict(method="Classical twin: transfer S_ab(t) + echo before t_c* on the same sample", distances="same",
             precision=f"median {d['CRB_classical_marg']['median']:.3f} A dense / {h['CRB_classical_marg']['median']:.3f} A amide at sigma=0.01; "
                       f"reaches the quantum CRB with g x more scans (g median {d['g_param']['median']:.1f} / {h['g_param']['median']:.1f})",
             throughput="same", interpretation="classical (sparse Pauli exact for S at N=10; exact to N~47)", tag="MEASURED-derived"),
        dict(method="NOESY build-up (solution; 15N/13C-edited; deuterated for large proteins)", distances="<= 5-6 A (1H-1H)",
             precision="bounds 2.5/3.5/5-6 A classes, ~0.3-1 A effective; exact-NOE protocols ~0.1-0.2 A",
             throughput="~10-20 restraints per residue per 1-3 days of 3D spectra", interpretation="classical (relaxation matrix)",
             tag="INFERENCE-unverified (domain values)"),
        dict(method="MAS ssNMR 1H-1H / 13C-13C contacts (RFDR, CHHC, DARR), REDOR 13C-15N", distances="<= 6-8 A",
             precision="REDOR isolated pairs ~0.1 A; contacts ~1 A bins", throughput="days per 2D/3D", interpretation="classical",
             tag="INFERENCE-unverified"),
        dict(method="19F-1H / 19F-19F REDOR, CODEX", distances="up to ~15 A (value from task brief)", precision="~0.5-1 A",
             throughput="1 label pair per sample, days", interpretation="classical", tag="task-brief value, unverified"),
        dict(method="PRE (paramagnetic tag)", distances="up to ~25-35 A", precision="~2-4 A (tag flexibility)",
             throughput="one tag site per sample, all backbone amides at once, hours-days", interpretation="classical",
             tag="INFERENCE (Clore & Iwahara, Chem. Rev. 2009, cited from memory, not re-verified)"),
        dict(method="DEER/PELDOR (spin labels)", distances="~18-80 A (longer when deuterated)",
             precision="distribution; mean ~1-3 A including label rotamers", throughput="hours per distance (Q-band)",
             interpretation="classical", tag="INFERENCE-unverified"),
        dict(method="RDCs (weak alignment)", distances="orientational (no range limit)", precision="few degrees per bond vector",
             throughput="hundreds of couplings per day", interpretation="classical", tag="INFERENCE-unverified"),
        dict(method="Cross-linking MS", distances="Calpha-Calpha <= ~25-35 A (DSS/BS3)", precision="binary contact",
             throughput="tens-hundreds of links per experiment", interpretation="classical", tag="INFERENCE-unverified"),
        dict(method="AlphaFold-class prediction", distances="all pairs", precision="median backbone ~1 A RMSD on CASP14 targets; "
                                                                             "short-range H-H distances in confident regions well under 1 A",
             throughput="minutes per protein on one GPU", interpretation="classical",
             tag="LITERATURE-SUPPORTED from memory (Jumper et al. Nature 2021, 0.96 A median backbone RMSD95), not re-verified"),
        dict(method="Small-molecule OTOC NMR + Willow simulation (Zhang et al. arXiv:2510.19550)",
             distances="one H-H distance, one dihedral", precision="'similar accuracy and precision to independent spectroscopic measurements'",
             throughput="-", interpretation="quantum processor used; not beyond classical",
             tag="LITERATURE-SUPPORTED (abstract verified 2026-09-27)"),
    ]
    out["quantum_inversion_costs"] = be["tasks"]
    json.dump(out, open(os.path.join(HERE, "value_table.json"), "w"), indent=1)
    print(json.dumps(dict(sigma_sweep=sweep, light_cone_Neff=lcs), indent=1))
    for k, v in bias.items():
        print(k, v)


if __name__ == "__main__":
    main()
