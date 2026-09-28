"""Summarise the double-dimer emulation runs (exact validation + large-k value/mixing)."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, "results_emulation.json")))
lg = json.load(open(os.path.join(HERE, "results_emulation_long.json")))
out = {"exact_validation": {k: v for k, v in r.items() if k.startswith("exact")}, "large_k": [], "long_chains": lg}
dom = 0; n = 0
for k, v in r.items():
    if not k.startswith("large"): continue
    g, p = v["gbs_dd"], v["pam"][v["pam_cal"]]
    d = p["prec"] >= g["prec"] and p["cov"] >= g["cov"]
    dom += d; n += 1
    out["large_k"].append({"case": k, "photons": v["photons"], "rhat": v["rhat_logweight"], "dmarg_2chains_400k": v["max_abs_marg_diff_2chains"],
                           "gbs_prec": g["prec"], "gbs_cov": g["cov"], "gbs_mpp": g["mpp"], "pam_cal": v["pam_cal"],
                           "pam_prec": p["prec"], "pam_cov": p["cov"], "pam_mpp": p["mpp"],
                           "beta1_prec": v["beta1"]["prec"], "beta1_cov": v["beta1"]["cov"], "pam_dominates": bool(d)})
out["pam_cal_dominates_gbs_cases"] = f"{dom}/{n}"
json.dump(out, open(os.path.join(HERE, "analysis_emulation.json"), "w"), indent=1)
print(out["pam_cal_dominates_gbs_cases"])
for x in out["large_k"]: print(x["case"], x["photons"], round(x["rhat"],3), x["gbs_prec"], x["gbs_cov"], round(x["gbs_mpp"],3), x["pam_cal"], x["pam_prec"], x["pam_cov"], round(x["pam_mpp"],3))
