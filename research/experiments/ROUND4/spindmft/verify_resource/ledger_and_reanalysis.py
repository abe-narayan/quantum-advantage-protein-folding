"""Resource verifier (ROUND4 spindmft): (1) re-derive the lane's compute ledger from its own output files;
(2) re-run the lane's analyze.py logic (unchanged code, output redirected here) and diff it against analysis.json;
(3) recompute the headline MEASURED numbers of the claim from raw inputs.  Reads JSON only (< 5 CPU-s).
Writes only verify_resource/ledger_reanalysis.json."""
import glob
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
OUT = os.path.join(HERE, "ledger_reanalysis.json")
c0 = time.process_time()

# ------------------------------------------------------------------ (1) ledger
rows = []
for f in sorted(glob.glob(os.path.join(LANE, "out", "*.json"))):
    d = json.load(open(f))
    base = os.path.basename(f)
    if base.endswith(".ckpt.json"):
        # only count checkpoints with no finished twin (i.e. stopped runs)
        twin = f[: -len(".ckpt.json")] + ".json"
        if os.path.exists(twin):
            continue
    c = d.get("cpu") if "cpu" in d else d.get("cpu_s")
    rows.append(dict(file=base, cpu_s=float(c) if c is not None else None))
t = json.load(open(os.path.join(LANE, "test_sdmft.json")))
rows.append(dict(file="test_sdmft.json", cpu_s=float(t["cpu_s"])))
logged = sum(r["cpu_s"] for r in rows if r["cpu_s"] is not None)
largest = max(rows, key=lambda r: r["cpu_s"] or 0)
groups = {}
for r in rows:
    k = r["file"].split("_")[0]
    groups[k] = groups.get(k, 0.0) + (r["cpu_s"] or 0.0)
ledger = dict(rows=rows, logged_cpu_s=logged, logged_cpu_min=logged / 60, largest=largest,
              by_kind_cpu_min={k: v / 60 for k, v in groups.items()},
              lane_claim=dict(total_cpu_min=58, logged_cpu_min=48.9, tests_cpu_min=1.4, largest_run_cpu_min=9.3,
                              unlogged_cpu_min=5.5 + 2.0))

# cost of the pieces the claim says reach the 40 us echo (the 'classical method' that must be costed)
def cpu(name):
    return next(r["cpu_s"] for r in rows if r["file"] == name)
kill40 = dict(
    exact_baware_N16_three_series_cpu_s=sum(cpu(f"exact_pairb_p{p}_b{b}_N16.json") for p, b in ((245, 7), (19, 8), (19, 9))),
    exact_baware_ladder_N12_16_three_series_cpu_s=sum(cpu(f"exact_pairb_p{p}_b{b}_N{N}.json") for p, b in ((245, 7), (19, 8), (19, 9))
                                                     for N in (12, 14, 16)),
    spinDMFT_sr_protein_cpu_s=cpu("sr_protein_T120_M384.json"),
    spinDMFT_sr_W18_cpu_s=cpu("sr_1UBQ_p19_N18_T120_M4096.json") + cpu("sr_1UBQ_p245_N18_T120_M4096.json"),
    spinDMFT_emb_protein_and_W18_nc10_probeb_cpu_s=sum(cpu(f"emb_p{p}_W{W}_nc10_probeb_sr_M512_s7.json")
                                                     for p in (19, 245) for W in ("protein", "18")),
    spinDMFT_emb_pairb_cpu_s=sum(cpu(f) for f in ["emb_p19_Wprotein_nc10_pairb8_sr_M512_s7.json",
                                                   "emb_p19_Wprotein_nc10_pairb9_sr_M512_s7.json",
                                                   "emb_p245_Wprotein_nc10_pairb7_sr_M512_s7.json"]),
)
kill40["note"] = ("Probe-family exact F18/F20 are round-3 artefacts (not re-costed by the lane). The lane's own "
                  "classical pipeline for all 8 series at 40 us = exact b-aware + spinDMFT; F18 cost from round 3.")
kill40["lane_pipeline_total_cpu_min_excl_probe_family"] = (sum(v for k, v in kill40.items() if k.endswith("_cpu_s")
                                                               and "ladder" not in k)) / 60
ledger["cost_of_40us_classical_pipeline"] = kill40

# ------------------------------------------------------------------ (2) re-run analyze.py logic, output redirected
src = open(os.path.join(LANE, "analyze.py")).read()
assert src.count('os.path.join(HERE, "analysis.json")') == 1
src = src.replace('os.path.join(HERE, "analysis.json")', "__REANALYSIS_OUT__")
g = {"__file__": os.path.join(LANE, "analyze.py"), "__name__": "reanalysis", "__REANALYSIS_OUT__": os.path.join(HERE, "reanalysis_analysis.json")}
import io
import contextlib
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    exec(compile(src, "analyze_redirected", "exec"), g)
    g["main"]()
new = json.load(open(os.path.join(HERE, "reanalysis_analysis.json")))
old = json.load(open(os.path.join(LANE, "analysis.json")))


def diff(a, b, path="", out=None, tol=1e-12):
    if out is None:
        out = []
    if isinstance(a, dict) and isinstance(b, dict):
        for k in set(a) | set(b):
            if k not in a or k not in b:
                out.append((path + "/" + str(k), "missing"))
            else:
                diff(a[k], b[k], path + "/" + str(k), out, tol)
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            out.append((path, "len"))
        for i, (x, y) in enumerate(zip(a, b)):
            diff(x, y, f"{path}[{i}]", out, tol)
    elif isinstance(a, float) or isinstance(b, float):
        if a is None or b is None or (not (isinstance(a, float) and math.isnan(a) and math.isnan(b)) and abs(a - b) > tol):
            out.append((path, a, b))
    elif a != b:
        out.append((path, a, b))
    return out


d = diff(old, new)
reanalysis = dict(n_differences=len(d), first_differences=d[:20], stdout_head=buf.getvalue()[:3000])

# ------------------------------------------------------------------ (3) headline numbers from raw inputs
dec = new["decisions"]
head = {tt: dict(n_within_sigma_vs_hybrid=dec[tt]["n_agree_within_sigma"], median=dec[tt]["median_abs_diff"],
                 max=dec[tt]["max_abs_diff"], val_primary=dec[tt]["val_n_within_sigma_vs_F18_minus_floor"],
                 val_direct=dec[tt]["val_n_within_sigma_vs_F18"]) for tt in dec}
fx = new["flat_X_test"]
head["flatX"] = {tt: (fx[tt]["pooled_slope"], fx[tt]["pooled_slope_se"]) for tt in fx}
# flat-X: how much of d(H+floor) over N=14..20 is H and how much is floor (the test's lever arm)
lever = {}
for tt in ("40", "80", "120"):
    per = []
    for p in (19, 245):
        L = new["exact_ladders"][f"p{p}_t{tt}_b1"]
        L = {r["N"]: r for r in L}
        if 14 in L and 20 in L:
            per.append(dict(probe=p, dH=L[20]["H"] - L[14]["H"], dfloor=L[20]["floor"] - L[14]["floor"],
                            H20=L[20]["H"]))
    lever[tt] = per
head["flatX_lever_arm_H_vs_floor"] = lever
# E-B sigma arithmetic (exact16 - hybrid) / sigma and against the hybrid's own H budget
eb = new["EB_exact_baware"]
hyb_rows = {(int(r["probe"][1:]), r["t_us"], r["site"]): r for r in
            json.load(open(os.path.join(LANE, "..", "..", "ROUND3", "critic", "critic_checks.json")))["C1_early_window"]["rows"]}
ebrows = []
for tt in eb:
    for r in eb[tt]["rows"]:
        hb = hyb_rows[(r["probe"], int(tt), r["site"])]
        budget = hb.get("hybrid_H_error_budget")
        ex = r["exact_baware"][str(r["N_used"])]
        ebrows.append(dict(t=int(tt), probe=r["probe"], site=r["site"], exact16=ex, hyb=r["Fhyb"],
                           diff=ex - r["Fhyb"], diff_over_sigma=(ex - r["Fhyb"]) / 0.01,
                           hybrid_H_error_budget=budget,
                           diff_over_combined_se=(ex - r["Fhyb"]) / math.sqrt((budget or 0) ** 2 + 0.0028 ** 2)
                           if budget else None,
                           exact_minus_spinDMFT=r["exact_minus_spinDMFT"]))
head["EB"] = ebrows

json.dump(dict(ledger=ledger, reanalysis=reanalysis, headline=head, cpu_s=time.process_time() - c0),
          open(OUT + ".tmp", "w"), indent=1, default=str)
os.replace(OUT + ".tmp", OUT)
print(json.dumps(dict(logged_cpu_min=round(logged / 60, 2), largest=largest, by_kind=ledger["by_kind_cpu_min"],
                      kill40=kill40, n_diff=len(d)), indent=1, default=str))
print(json.dumps(head, indent=1, default=str)[:6000])
