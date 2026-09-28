"""Collect this verifier's exact runs (runs/pp_*.json) and set them against the lane's numbers (analysis.json:
probe-family F18/F20, hybrid, spinDMFT F_corr = F18 + bath correction, b-aware spinDMFT predictions) and the lane's
exact b-aware N = 12-16 files.  Pure bookkeeping (< 1 CPU-s).  Writes verify_summary.json."""
import glob
import json
import os
from collections import defaultdict

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
SIG = 0.01
TIMES = {20: 40, 40: 80, 60: 120}
A = json.load(open(os.path.join(LANE, "analysis.json")))
rows = {(r["probe"], r["t_us"], r["site"]): r for r in A["echo_rows"]}
pred = {}
for k, v in A["pairb_nc10"].items():
    if "Wprotein" in k:
        p, b = int(k.split("_")[0][1:]), int(k.split("_")[1][1:])
        for t, d in v.items():
            pred[(p, int(t), b)] = d["F"]

mine = defaultdict(list)      # (family, p, b, N, t_us) -> list of F (one per seed)
cpu = {}
for f in sorted(glob.glob(os.path.join(HERE, "runs", "pp_*.json"))):
    s = json.load(open(f))
    if "F" not in s:
        continue
    for n, F in s["F"].items():
        mine[(s["family"], s["probe"], s["b_world"], s["N"], TIMES[int(n)])].append(F)
    cpu[os.path.basename(f)] = dict(cpu_s=s["cpu_s_total"], peak_rss_GB=s.get("peak_rss_GB"), N=s["N"],
                                    steps=s["steps"], M2_in=s["M2_fraction_b_in_cluster"])
lane_pb = {}
for f in glob.glob(os.path.join(LANE, "out", "exact_pairb_p*_b*_N*.json")):
    d = json.load(open(f))
    for i, t in enumerate(d["times_us"]):
        if round(t) in (40, 80, 120):
            lane_pb[(d["probe"], d["b_world"], d["N"], round(t))] = d["F"][i]

series = [(19, 1), (19, 7), (19, 8), (19, 9), (245, 1), (245, 7), (245, 8), (245, 9)]
b_remote = {(19, 8), (19, 9), (245, 7)}
table = []
for t in (40, 80, 120):
    for (p, b) in series:
        r = rows[(p, t, b)]
        e = dict(probe=p, site=b, t_us=t, lane_b_remote=(p, b) in b_remote, F18_probe=r["F18"], F20_probe=r.get("F20"),
                 F_hybrid=r["Fhyb"], Fcorr_spinDMFT=r["Fcorr_nc10"], spinDMFT_baware_pred=pred.get((p, t, b)))
        for N in (18, 22):
            v = mine.get(("probe", p, b, N, t))
            if v:
                e[f"F{N}_probe_verifier"] = float(np.mean(v))
        for N in (12, 14, 16):
            if (p, b, N, t) in lane_pb:
                e[f"Fb{N}_lane"] = lane_pb[(p, b, N, t)]
        bx = {}
        for N in (16, 18, 20, 22):
            v = mine.get(("pairb", p, b, N, t))
            if v:
                e[f"Fb{N}_verifier"] = float(np.mean(v))
                e[f"Fb{N}_verifier_nseeds"] = len(v)
                bx[N] = float(np.mean(v))
        if bx:
            Nm = max(bx)
            e["Fb_best"] = bx[Nm]; e["Fb_best_N"] = Nm
            steps = sorted(bx)
            if len(steps) >= 2:
                e["Fb_last_step_change"] = bx[steps[-1]] - bx[steps[-2]]
            ref = e["spinDMFT_baware_pred"] if e["spinDMFT_baware_pred"] is not None else e["Fcorr_spinDMFT"]
            e["spinDMFT_ref_used"] = "baware_pred" if e["spinDMFT_baware_pred"] is not None else "Fcorr_probe_family"
            e["Fb_best_minus_spinDMFT"] = bx[Nm] - ref
            e["Fb_best_minus_Fcorr"] = bx[Nm] - e["Fcorr_spinDMFT"]
            e["Fb_best_minus_F18_probe"] = bx[Nm] - e["F18_probe"]
            e["Fb_best_minus_hybrid"] = bx[Nm] - e["F_hybrid"]
            e["agree_within_sigma_with_spinDMFT"] = bool(abs(e["Fb_best_minus_spinDMFT"]) <= SIG)
            e["agree_within_sigma_with_Fcorr_or_pred"] = bool(min(abs(e["Fb_best_minus_Fcorr"]),
                                                                  abs(e["Fb_best_minus_spinDMFT"])) <= SIG)
        table.append(e)
counts = {}
for t in (40, 80, 120):
    tt = [e for e in table if e["t_us"] == t and "Fb_best" in e]
    counts[str(t)] = dict(n_series_with_baware=len(tt),
                          n_within_sigma_spinDMFT_ref=sum(e["agree_within_sigma_with_spinDMFT"] for e in tt),
                          n_within_sigma_either_spinDMFT_estimate=sum(e["agree_within_sigma_with_Fcorr_or_pred"] for e in tt),
                          n_hybrid_more_than_3sigma_below=sum(e["Fb_best_minus_hybrid"] > 3 * SIG for e in tt),
                          min_over_hybrid_sigma=min(e["Fb_best_minus_hybrid"] for e in tt) / SIG,
                          max_over_hybrid_sigma=max(e["Fb_best_minus_hybrid"] for e in tt) / SIG,
                          max_abs_Fb_minus_spinDMFT=max(abs(e["Fb_best_minus_spinDMFT"]) for e in tt),
                          max_abs_last_step_change=max((abs(e.get("Fb_last_step_change", 0)) for e in tt), default=None))
out = dict(sigma=SIG, table=table, counts=counts, runs=cpu, total_cpu_s_runs=sum(v["cpu_s"] for v in cpu.values()))
json.dump(out, open(os.path.join(HERE, "verify_summary.json.tmp"), "w"), indent=1)
os.replace(os.path.join(HERE, "verify_summary.json.tmp"), os.path.join(HERE, "verify_summary.json"))
hdr = "p   b  t  | F18pr  F22pr | Fb16L  Fb16V  Fb18V  Fb20V  Fb22V | dmft(ref) | Fb-dmft  Fb-hyb  Fb-F18"
print(hdr)
for e in table:
    f = lambda k: ("%.4f" % e[k]) if e.get(k) is not None else "  -   "
    ref = e.get("spinDMFT_baware_pred") if e.get("spinDMFT_baware_pred") is not None else e["Fcorr_spinDMFT"]
    print(f"{e['probe']:<3d} {e['site']} {e['t_us']:3d} | {f('F18_probe')} {f('F22_probe_verifier')} | {f('Fb16_lane')} "
          f"{f('Fb16_verifier')} {f('Fb18_verifier')} {f('Fb20_verifier')} {f('Fb22_verifier')} | {ref:.4f} | "
          + (f"{e['Fb_best_minus_spinDMFT']:+.4f} {e['Fb_best_minus_hybrid']:+.4f} {e['Fb_best_minus_F18_probe']:+.4f}"
             if "Fb_best" in e else ""))
print(json.dumps(counts, indent=1))
print("verifier exact-run CPU total (s):", round(out["total_cpu_s_runs"], 1))
