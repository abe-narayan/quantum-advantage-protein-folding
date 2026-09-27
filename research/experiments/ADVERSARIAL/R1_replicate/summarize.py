"""Collect the R1 replicate outputs into summary.json (read-only over stored RAW; no heavy compute).
Run after selftest.py, run_exact.py (both modes) and run_pauli.py (eps 1e-4 pair, 3e-5 pair, 0 pair to60, 1e-4 step to60)."""
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
J = lambda f: json.load(open(os.path.join(HERE, f)))  # noqa: E731

ex = J("exact_trotter.json"); co = J("exact_continuous.json")
p4 = J("pauli_eps0.0001_pair.json"); p35 = J("pauli_eps3e-05_pair.json")
p0 = J("pauli_eps0_pair_to60.json"); p4s = J("pauli_eps0.0001_step_to60.json")
st = J("selftest.json")
bs = [str(b) for b in ex["bs"]]
fi = {q["name"]: q for q in ex["params"] if q["h"] == 0.05}


def frac_after(name, tc, key="FI_otoc_t"):
    v = np.asarray(fi[name][key]); return float(v[tc:].sum() / v.sum())


S = {}
S["replication_exact_vs_stored"] = dict(
    S_exact_maxabs=ex["compare_stored"]["S_exact_maxabs"], F_exact_maxabs=ex["compare_stored"]["F_exact_maxabs"],
    per_param={k: {kk: v[kk] for kk in ("FI_t_maxrel_of_peak", "FI_otoc_t_maxrel_of_peak", "dS_maxabs", "dF_maxabs",
                                        "FI_total_mine", "FI_total_stored", "FI_otoc_total_mine", "FI_otoc_total_stored")}
               for k, v in ex["compare_stored"]["params"].items()})
S["replication_sparse_eps1e-4_vs_stored"] = {k: p4["compare_stored"][k] for k in
                                             ("t_c_index_stored", "t_c_otoc_index_stored", "n_strings_max_absdiff",
                                              "kept_norm2_maxabs", "max_bias_maxabs", "max_bias_otoc_maxabs")}
S["replication_sparse_eps1e-4_vs_stored"].update(t_c_index_mine=p4["t_c_index"],
                                                 t_c_otoc_index_mine_plain=p4["t_c_otoc_index_plain"],
                                                 t_c_otoc_index_mine_normcorr=p4["t_c_otoc_index_normcorr"],
                                                 frac_hard_otoc_mine=p4["FI_split_mine"],
                                                 frac_hard_otoc_stored=p4["compare_stored"]["frac_hard_otoc_stored"])
S["sparse_eps3e-5"] = dict(t_c_index=p35["t_c_index"], t_c_otoc_plain=p35["t_c_otoc_index_plain"] or "no failure (17/17)",
                           t_c_otoc_normcorr=p35["t_c_otoc_index_normcorr"], max_bias_otoc_max=max(p35["max_bias_otoc"]),
                           n_strings_max=max(p35["n_strings"]), compare_stored_C2=p35.get("compare_stored_C2"),
                           frac_hard=p35["FI_split_mine"])
S["engine_crosscheck_eps0_N10_to60steps"] = dict(max_bias_S=max(p0["max_bias"]), max_bias_F=max(p0["max_bias_otoc"]),
                                                 n_strings=p0["n_strings"], note="dense-matrix vs PTM engines")
tc_step = p4s["t_c_otoc_index_plain"]
S["truncation_granularity_eps1e-4"] = dict(
    per_pair_t_c_otoc=p4["t_c_otoc_index_plain"], per_step_t_c_otoc=tc_step,
    frac_hard_otoc_per_pair={n: frac_after(n, p4["t_c_otoc_index_plain"]) for n in fi},
    frac_hard_otoc_per_step={n: frac_after(n, tc_step) for n in fi},
    frac_hard_otoc_if_tc3={n: frac_after(n, 3) for n in fi})
S["trotter_vs_continuous"] = dict(
    S_maxabs=max(float(np.abs(np.asarray(co["S_exact"][b]) - np.asarray(ex["S_exact"][b])).max()) for b in bs),
    F_maxabs=max(float(np.abs(np.asarray(co["F_exact"][b]) - np.asarray(ex["F_exact"][b])).max()) for b in bs),
    per_param={q["name"]: dict(FI_ratio=q["FI_total"] / fi[q["name"]]["FI_total"],
                               FI_otoc_ratio=q["FI_otoc_total"] / fi[q["name"]]["FI_otoc_total"],
                               late_frac_otoc_idx4_cont=float(np.sum(q["FI_otoc_t"][4:]) / q["FI_otoc_total"]),
                               late_frac_otoc_idx4_trot=frac_after(q["name"], 4))
               for q in co["params"]})
S["fd_step_robustness"] = ex["compare_stored"].get("fd_step_robustness_h0.02_vs_0.05")
S["rigid_param_provenance"] = dict(
    stored="rigid_res16 (git 92bb4eb rule), n_moved=1, identical to radial_HA/GLU16 (dS/dF equal to 1e-13)",
    current="rigid_res2 (git 50e0c9e rule), n_moved=3, moves HA/GLN2 = the probe's nearest proton (2.16 A)",
    rigid_res2_FI_total=fi["rigid_res2"]["FI_total"], rigid_res2_FI_otoc_total=fi["rigid_res2"]["FI_otoc_total"])
# C2 saturation: M*(eps=3e-5) relative to the parity-allowed Pauli space 4^N/2 (read-only over stored C2 RAW)
sat = {}
for f in sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_sparse", "*_g0.json"))):
    r = json.load(open(f)); N = r["N"]
    e = min(r["runs"], key=lambda x: x["eps"])
    ex_ = r.get("exact") or {}
    ok = None
    if ex_.get("F"):
        m = min(len(e["F"][str(r["bs"][0])]), len(ex_["F"][str(r["bs"][0])]))
        ok = bool(max(float(np.abs(np.asarray(e["F"][str(b)][:m]) - np.asarray(ex_["F"][str(b)][:m])).max())
                      for b in r["bs"]) <= r["sigma"])
    sat[os.path.basename(f)] = dict(N=N, eps=e["eps"], peak_strings=e["peak_strings"],
                                    frac_of_parity_space=e["peak_strings"] / (4 ** N / 2),
                                    echo_within_sigma_all_times=ok)
S["C2_pauli_space_saturation"] = sat
oth = {}
allv = []
for f in sorted(glob.glob(os.path.join(HERE, "other_*_eps3e-05.json"))):
    o = json.load(open(f))
    oth[o["tag"]] = dict(stored_t_c_otoc=o["stored_best_t_c_otoc_index"], t_c_otoc_eps3e5=max(o["t_c_otoc_plain"], o["t_c_otoc_normcorr"]),
                         n_rec=o["n_rec"], max_bias_otoc=max(o["max_bias_otoc"]), max_strings=max(o["n_strings"]),
                         frac_hard=o["frac_hard"], cpu_s=o["cpu_s"])
    allv += [(v["frac_hard_otoc_stored_panel"], v["frac_hard_otoc_eps3e5"]) for v in o["frac_hard"].values()]
# add the main job (unique params of the stored file: 3 radial; rigid_res16 is a duplicate)
for nm in ("radial_HA/GLU16", "radial_HG22/ILE3", "radial_HG3/GLN2"):
    allv.append((frac_after(nm, 4), 0.0))
allv = np.asarray(allv)
S["eps3e-5_on_other_jobs"] = dict(jobs=oth, n_params=len(allv),
                                  median_frac_hard_stored_panel=float(np.median(allv[:, 0])),
                                  median_frac_hard_with_eps3e5=float(np.median(allv[:, 1])),
                                  n_params_closed=int((allv[:, 1] == 0).sum()),
                                  note="subset: 1UBQ_p19_o0 + the 4 jobs in other_*.json; 6 further N=10 gamma=0 jobs untested")
S["cpu_seconds"] = dict(other_jobs=sum(v["cpu_s"] for v in oth.values()),selftest_dense_N10_one_geometry=st["cpu_s_dense_N10"], exact_trotter=ex["cpu_s"],
                        exact_continuous=co["cpu_s"], pauli_eps1e4=p4["cpu_s"], pauli_eps3e5=p35["cpu_s"],
                        pauli_eps0_60=p0["cpu_s"], pauli_eps1e4_step_60=p4s["cpu_s"])
json.dump(S, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
print(json.dumps(S, indent=1))
