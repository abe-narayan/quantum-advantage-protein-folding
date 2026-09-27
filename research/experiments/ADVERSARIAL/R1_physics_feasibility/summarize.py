"""Collect the decisive numbers of the R1 physics-feasibility audit into summary.json (reads the other outputs)."""
from __future__ import annotations

import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def stats(v):
    v = np.array([x for x in v if x is not None], float)
    return dict(median=float(np.median(v)), min=float(v.min()), max=float(v.max()), n=int(len(v)))


def main():
    sc = json.load(open(os.path.join(HERE, "scales.json")))
    env = json.load(open(os.path.join(HERE, "reversal_envelope.json")))
    jobs = sc["jobs"]
    dense = [j for j in jobs if not j["hn_only"]]
    hn = [j for j in jobs if j["hn_only"]]
    out = dict(
        m2_formula_check=sc["check"],
        powder_T2_us=sc["powder_average"],
        dense=dict(T2_cluster_us=stats([j["T2_cluster_us"] for j in dense]),
                   T2_network_us=stats([j["T2_network_static_us"] for j in dense]),
                   T2_network_rotoravg_us=stats([j["T2_network_rotoravg_us"] for j in dense]),
                   gaussFWHM_network_kHz=stats([j["gauss_FWHM_network_kHz"] for j in dense]),
                   dmax_cluster_kHz=stats([j["dmax_cluster_kHz"] for j in dense]),
                   tc_over_T2_cluster=stats([j["tc_over_T2_cluster"] for j in dense]),
                   t50_over_T2_cluster=stats([j["t50_over_T2_cluster"] for j in dense]),
                   tc_over_T2_network=stats([j["tc_over_T2_network_static"] for j in dense]),
                   t50_over_T2_network=stats([j["t50_over_T2_network_static"] for j in dense])),
        amide_only=dict(T2_cluster_us=stats([j["T2_cluster_us"] for j in hn]),
                        T2_network_us=stats([j["T2_network_static_us"] for j in hn]),
                        gaussFWHM_network_kHz=stats([j["gauss_FWHM_network_kHz"] for j in hn]),
                        dmax_cluster_kHz=stats([j["dmax_cluster_kHz"] for j in hn]),
                        homo_loc_sqrtM2_kHz=stats([j["homo_loc_sqrtM2_kHz"] for j in hn]),
                        hetero_N15_sqrtM2_kHz=stats([j["hetero_sqrtM2_kHz"]["N15_uniform"] for j in hn]),
                        hetero_N14_sqrtM2_kHz=stats([j["hetero_sqrtM2_kHz"]["N14_natural"] for j in hn]),
                        hetero_H2_sqrtM2_kHz=stats([j["hetero_sqrtM2_kHz"]["H2_perdeut"] for j in hn]),
                        tc_over_T2_cluster=stats([j["tc_over_T2_cluster"] for j in hn]),
                        t50_over_T2_cluster=stats([j["t50_over_T2_cluster"] for j in hn]),
                        t50_over_T2_network=stats([j["t50_over_T2_network_static"] for j in hn])),
    )
    keys = ["cluster|generous|PE_gauss_T3=4T2", "cluster|generous|LE_logistic_T3=6.7T2",
            "network|generous|LE_logistic_T3=6.7T2", "cluster|literal|LE_logistic_T3=6.7T2",
            "cluster|generous|hypothetical_logistic_T3=20T2"]
    out["envelope"] = dict(ideal_gain=stats([r["ideal"]["gain_vs_classical"] for r in env]),
                           ideal_hard_over_transfer=stats([r["ideal"]["hard_over_transfer"] for r in env]))
    for k in keys:
        out["envelope"][k] = dict(gain=stats([r["cases"][k]["gain_vs_classical"] for r in env]),
                                  hard_retained=stats([r["cases"][k]["hard_retained"] for r in env]),
                                  n_jobs_gain_ge_2=int(sum(r["cases"][k]["gain_vs_classical"] >= 2 for r in env)))
    for k in ("cluster|generous|required", "network|generous|required", "cluster|literal|required"):
        out["envelope"][k] = stats([r["cases"][k]["T3_over_T2_for_gain_2.0"] for r in env])
        out["envelope"][k]["n_never"] = int(sum(r["cases"][k]["T3_over_T2_for_gain_2.0"] is None for r in env))
    phys = {}
    for f in sorted(glob.glob(os.path.join(HERE, "physics_*.json"))):
        p = json.load(open(f))
        rec = {}
        if "rotor" in p and "skipped" not in p["rotor"]:
            rec["rotor_maxdF_over_sigma"] = dict(easy=p["rotor"]["max_dF_over_sigma_easy"],
                                                 hard=p["rotor"]["max_dF_over_sigma_hard"])
        if "nuisance" in p:
            n = p["nuisance"]
            rec["offsets_1kHz_model_error_over_sigma"] = n["offsets_model_error"]
            rec["eta_scan"] = n["eta_scan"]
            rec["hard_FI_retained_after_profiling"] = {k: v["retained_trace"] for k, v in n["fisher"]["hard"].items()}
            rec["easy_FI_retained_after_profiling"] = {k: v["retained_trace"] for k, v in n["fisher"]["easy"].items()}
        if "disorder" in p:
            rec["disorder_retained_hard"] = {k: v["retained_hard"] for k, v in p["disorder"]["settings"].items()}
            rec["disorder_ensmean_vs_single_over_sigma_hard"] = {
                k: v["ensmean_vs_single_max_over_sigma_hard"] for k, v in p["disorder"]["settings"].items()}
        if "powder" in p:
            rec["powder_retained"] = {k: p["powder"][k]["retained"] for k in
                                      ("echo_easy", "echo_hard", "transfer_easy", "transfer_hard")}
        phys[p["job"]] = rec
    out["physics"] = phys
    json.dump(out, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
    print(json.dumps(out["envelope"], indent=1))


if __name__ == "__main__":
    main()
