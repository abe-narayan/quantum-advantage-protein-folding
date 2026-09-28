"""Falsifiable predictions for the pending exact N = 22 cone runs (governor, scripts/nmr_cone.py; same probe family,
same circuit), made BEFORE those runs finish (2026-09-28).  Ingredients (all MEASURED here):
  H_22  = CSD H at N_c = 22 + (exact - CSD) offset measured at N = 20
  floor_22 = kappa (1 - H_22) / 22,  kappa = floor_20 * 20 / (1 - H_20)   (kappa measured at N = 20)
  X_22  = X_20 (the 'remainder is flat' hypothesis; shell-event series flagged)
  F_22  = H_22 + floor_22 + X_22.
Also recorded: the naive 1/N-law prediction F_22 = F_20 * 20/22 used by the lane."""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "verify_summary.json")))
T = S["times_us"]
out = dict(note=__doc__, predictions={})
for p in (19, 245):
    B = S[f"p{p}"]
    csd22 = json.load(open(os.path.join(HERE, "runs", f"csd_1UBQ_p{p}_Nc22_M16000_h1.0.json")))
    idx = [csd22["times_us"].index(t) for t in T]
    H22c = np.array(csd22["H_unbiased"])[idx]
    off = np.array(B["H_inf"]["offset"])
    H20 = np.array(B["H"]["20"]); fl20 = np.array(B["floor"]["20"])
    kappa = fl20 * 20 / (1 - H20)
    H22 = H22c + off
    fl22 = kappa * (1 - H22) / 22
    pr = dict(H22_pred=np.round(H22, 4).tolist(), floor22_pred=np.round(fl22, 4).tolist(), series={})
    for key, e in B["hybrid_estimates"].items():
        if e["N_last"] != 20:
            continue
        t = int(key[1:key.index("_")]); ti = T.index(t)
        F22 = H22[ti] + fl22[ti] + e["X_last"]
        pr["series"][key] = dict(F20=e["F_last"], F22_pred_decomp=round(float(F22), 4),
                                 F22_pred_1overN=round(e["F_last"] * 20 / 22, 4), X_flat_at_20=e["X_flat"],
                                 unc_note="+-0.005 (H: CSD SE + offset) +-|dX_last| if X not flat")
    out["predictions"][f"p{p}"] = pr
json.dump(out, open(os.path.join(HERE, "predictions_N22.json"), "w"), indent=1)
for p, v in out["predictions"].items():
    print(p, "H22", v["H22_pred"], "\n   floor22", v["floor22_pred"])
    for k, s in v["series"].items():
        print("  ", k, s)
