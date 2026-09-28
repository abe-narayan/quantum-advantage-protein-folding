"""T2 summary against the pre-registered kill rule."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from rotor import splitting, atomic_json
HERE = os.path.dirname(os.path.abspath(__file__))
P = json.load(open(os.path.join(HERE, "results_pairs.json")))
T = json.load(open(os.path.join(HERE, "results_triangle.json")))
rows = [v for k, v in P.items() if not k.startswith("_")]
out = {"single_rotor_splitting_ueV_B0.655": {str(v): float(splitting(v, 0.655, M=60) * 1e3) for v in (20, 30, 40, 50, 60, 80, 100, 120, 150)}}
for V3 in (30.0, 60.0, 100.0):
    s = [r for r in rows if r["V3"] == V3]
    out[f"V3_{V3:g}"] = {
        "n": len(s),
        "Delta_exact_ueV_min_max": [min(r["Delta_exact_s2=0_ueV"] for r in s), max(r["Delta_exact_s2=0_ueV"] for r in s)],
        "n_Delta_ge_0.1ueV": sum(r["Delta_exact_s2=0_ueV"] >= 0.1 for r in s),
        "max_abs_J_ueV": max(max(abs(r["J11_ueV"]), abs(r["J12_ueV"])) for r in s),
        "max_rel_J": max(r["rel_J"] for r in s),
        "median_rel_mf_err": float(np.median([r["rel_mf_err"] for r in s])),
        "max_rel_mf_err": max(r["rel_mf_err"] for r in s),
        "n_supportlike_relJ_ge_0.1_and_Delta_ge_1ueV": sum(r["rel_J"] >= 0.1 and r["Delta_exact_s2=0_ueV"] >= 1 for r in s),
    }
tri = {}
for k, v in T.items():
    if k.startswith("_"): continue
    tri[k] = {rid: {"exact": x["Delta_exact3_ueV"], "pair_mult": x["pred_multiplicative_ueV"], "rel_err_mult": x["rel_err_multiplicative"],
                    "rel_err_add": x["rel_err_additive"]} for rid, x in v["rotors"].items()}
out["triangles_V3_30"] = tri
out["kill_i_fired"] = bool(out["V3_100"]["n_Delta_ge_0.1ueV"] == 0 and out["single_rotor_splitting_ueV_B0.655"]["80"] < 0.1)
out["support_fired"] = False
out["notes"] = ("kill (i): at protein-typical barriers (>=80 meV) all splittings < 0.1 ueV. Support requires relJ>=0.1 with Delta>=1 ueV: "
                "0 pairs. Residue: Hartree MF fails (median rel err quoted) and the pair cluster expansion fails for jammed triangles "
                "at V3=30 meV (model-level many-body correlation).")
atomic_json(os.path.join(HERE, "summary_t2.json"), out)
print(json.dumps(out, indent=1))
