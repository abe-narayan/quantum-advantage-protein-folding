"""ROUND4 red team, RT-C: attack on the CRITIC-C2 re-basing of K-111 (coupled methyl-rotor tunnelling).

CRITIC C2 says: the many-body correction to a methyl's tunnelling splitting (13-40% of Delta) equals a 1.7-2.7 meV
shift of that methyl's own barrier V3, so it is NON-IDENTIFIABLE against per-methyl V3 nuisances.

Red-team point [DERIVED]: that holds for the partner-in-A-state (mean-field-like) shift of Delta, which is one number per
methyl.  It does NOT hold for the partner-state dependence J = Delta_1(partner in E) - Delta_1(partner in A) (the lane's
J11/J12): a coupled pair shows a DOUBLET of tunnelling lines per methyl, split by J, and a V3_1 shift moves both
components together.  So the coupling is identifiable in principle from the doublet splitting -- if J is resolved.

Test (pure post-processing of the lane's exact pair results, results_pairs.json; seconds):
  * inhomogeneous width of a tunnelling line from barrier disorder sigma_V3 (protein glass at cryogenic T):
        FWHM = 2.355 * Delta * |d ln Delta / d V3| * sigma_V3      (slope from the single-rotor Delta(V3) table)
  * doublet resolved if |J| > FWHM; observable if Delta lies in an observation window:
        INS backscattering  Delta >= 0.1 ueV  (24 MHz)                     [INFERENCE / recalled]
        NMR tunnelling spectroscopy (field-cycling / level-crossing) 1e-4 .. 0.4 ueV (~24 kHz .. ~100 MHz) [recalled, UNVERIFIED]
  * fraction of the 16 closest 1UBQ methyl pairs (x 2 coupling models) with an observable AND resolved doublet.
  * classical cost of the identifiable quantity: J is an exact 2-rotor quantity (lane: seconds per pair); 3-rotor
    non-additivity is an exact 3-rotor quantity (lane: 83 s per triangle).
Output: rotor_identifiability.json
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
T2D = os.path.join(ROOT, "research", "experiments", "ROUND3", "new_mechanisms_A", "t2_methyl_rotor")
UEV_MHZ = 241.8


def main():
    pairs = json.load(open(os.path.join(T2D, "results_pairs.json")))
    summ = json.load(open(os.path.join(T2D, "summary_t2.json")))
    tri = json.load(open(os.path.join(T2D, "results_triangle.json")))
    sr = {float(k): v for k, v in summ["single_rotor_splitting_ueV_B0.655"].items()}
    V = np.array(sorted(sr)); D = np.array([sr[v] for v in V])
    slope = {v: float(-np.gradient(np.log(D), V)[i]) for i, v in enumerate(V)}      # -dlnDelta/dV3 per meV
    windows = {"INS_ge_0.1ueV": (0.1, 1e9), "NMR_1e-4_to_0.4ueV": (1e-4, 0.4)}
    out = dict(slope_dlnDelta_dV3_per_meV={str(k): v for k, v in slope.items()}, cases={}, rows=[])
    for key, r in pairs.items():
        if key.startswith("_"):
            continue
        V3 = float(r["V3"])
        Dl = abs(float(r["Delta_exact_s2=0_ueV"]))
        J = max(abs(float(r["J11_ueV"])), abs(float(r["J12_ueV"])))
        out["rows"].append(dict(key=key, V3=V3, Delta_ueV=Dl, Delta_MHz=Dl * UEV_MHZ, J_ueV=J, J_MHz=J * UEV_MHZ,
                                J_over_Delta=J / max(Dl, 1e-300), dmin_HH=r["dmin_HH"]))
    for sV in (0.5, 1.0, 2.0, 5.0):
        for wname, (lo, hi) in windows.items():
            for V3 in (30.0, 60.0, 100.0):
                rows = [x for x in out["rows"] if x["V3"] == V3]
                fw = [2.355 * x["Delta_ueV"] * slope[V3] * sV for x in rows]
                obs = [lo <= x["Delta_ueV"] <= hi for x in rows]
                res = [x["J_ueV"] > w for x, w in zip(rows, fw)]
                both = [a and b for a, b in zip(obs, res)]
                out["cases"][f"sigmaV3={sV}|{wname}|V3={V3:g}"] = dict(
                    n=len(rows), n_observable=int(sum(obs)), n_resolved=int(sum(res)), n_observable_and_resolved=int(sum(both)),
                    examples=[dict(key=x["key"], Delta_MHz=round(x["Delta_MHz"], 4), J_MHz=round(x["J_MHz"], 5),
                                   FWHM_MHz=round(w * UEV_MHZ, 5)) for x, w, b in zip(rows, fw, both) if b][:4])
    # J/Delta needed for resolution at given sigma_V3 (V3-independent up to the slope)
    out["J_over_Delta_needed"] = {f"sigmaV3={sV}|V3={V3:g}": 2.355 * slope[V3] * sV for sV in (0.5, 1, 2, 5)
                                  for V3 in (30.0, 60.0, 100.0)}
    out["J_over_Delta_distribution"] = {f"V3={V3:g}": dict(
        median=float(np.median([x["J_over_Delta"] for x in out["rows"] if x["V3"] == V3])),
        q90=float(np.quantile([x["J_over_Delta"] for x in out["rows"] if x["V3"] == V3], 0.9)),
        max=float(max(x["J_over_Delta"] for x in out["rows"] if x["V3"] == V3))) for V3 in (30.0, 60.0, 100.0)}
    out["classical_cost_identifiable_part"] = dict(pair_exact="seconds per pair (lane run_pairs, M=45, G=144)",
                                                   triangle_exact_s=[v.get("secs") for k, v in tri.items()
                                                                     if not k.startswith("_")])
    tmp = os.path.join(HERE, "rotor_identifiability.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "rotor_identifiability.json"))
    print("slope", {k: round(v, 3) for k, v in slope.items()})
    print("J/Delta distribution", out["J_over_Delta_distribution"])
    print("J/Delta needed", {k: round(v, 3) for k, v in out["J_over_Delta_needed"].items()})
    for k, v in out["cases"].items():
        print(k, {kk: v[kk] for kk in ("n", "n_observable", "n_resolved", "n_observable_and_resolved")}, v["examples"][:2])


if __name__ == "__main__":
    main()
