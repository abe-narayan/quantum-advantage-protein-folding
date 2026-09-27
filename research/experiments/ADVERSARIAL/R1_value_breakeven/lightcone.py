"""R1 value lens, part 3: how many protons N_eff does the real protein put inside the echo light cone?

The echo-window claim is only a quantum-advantage claim if N_eff(t) at the informative times exceeds exact classical
reach (~36-45 spins).  The value claim is only realisable if the forward model is CONVERGED in N (model_bias.py shows
that +2/+4 environment spins already bias the fitted distances by 0.1-0.6 A).  This script estimates N_eff(t) with a
first-passage ("fastest coupling path") light cone, calibrated on MEASURED exact echoes:

  1. Heuristic front model (INFERENCE): the echo front reaches proton j at t_j = c * min_path sum_edges 1/|d_edge|
     (Dijkstra on the full secular dipolar coupling graph, d in rad/s, the same B0 orientation as the job).
  2. Calibration (MEASURED): for every C1 / C1-HN job at gamma = 0, the arrival time at each observed proton b is the
     first time 1 - F_ab(t) > sigma = 0.01 (log-log interpolation between recorded times).  Path times are computed
     inside the same isolated 10-spin cluster.  c = median ratio (spread reported).
  3. Cross-check (MEASURED): the embedding runs give the time at which the 2 / 4 added environment protons first move
     any observed signal by > sigma; compare with the model's predicted arrival time at those protons.
  4. N_eff(t) = number of protons (whole single molecule, all H or backbone amide H only) with t_j <= t, for
     t in the dense window (80-320 us) and the amide-only window (250-1000 us).  Intermolecular protons of a real
     solid sample are NOT included, so N_eff is a lower bound in that respect (INFERENCE).
Also reports the plain geometric count of protons within radius R of the probe.
Cost: seconds (600 x 600 couplings).  Output: lightcone.json.
"""
import glob
import json
import math
import os
import sys

import numpy as np
from scipy.sparse.csgraph import dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402


def arrival_measured(tt, F, sig=0.01):
    y = 1 - np.asarray(F)
    k = next((i for i in range(1, len(tt)) if y[i] > sig), None)
    if k is None:
        return None
    if k == 1 or y[k - 1] <= 0:
        # power-law through the origin: y ~ A t^2 at short times (DERIVED: second order in t)
        return tt[k] * math.sqrt(sig / y[k])
    lt = np.interp(math.log(sig), [math.log(max(y[k - 1], 1e-300)), math.log(y[k])], [math.log(tt[k - 1]), math.log(tt[k])])
    return math.exp(lt)


def path_times(dm, src):
    W = np.zeros_like(dm)
    nz = np.abs(dm) > 1e-9
    W[nz] = 1.0 / np.abs(dm[nz])
    return dijkstra(W, directed=False, indices=src)


def main():
    H = {}
    for pdb in ("1UBQ", "1PGA"):
        names, xyz, res = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
        H[pdb] = (names, xyz, res)
    ratios, calib_rows = [], []
    jobs = []
    for f in sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate", "*.json")) +
                    glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate_hn", "*.json"))):
        d = json.load(open(f))
        if d["gamma"] != 0 or d.get("F_exact") is None:
            continue
        hn = "_hn" in f
        names, xyz, res = H[d["pdb"]]
        if hn:
            keep = [i for i, n in enumerate(names) if n.startswith("H/")]
            names = [names[i] for i in keep]; xyz = xyz[keep]
        probe = [i for i, n in enumerate(names) if n == d["probe_name"]][0]
        idx = SP.cluster(xyz, probe, d["N"])
        assert [names[i] for i in idx] == d["cluster_names"], "cluster mismatch"
        b0 = np.asarray(d["b0"])
        dm_c = SP.couplings(xyz[idx], b0)
        tp = path_times(dm_c, 0)
        tt = np.asarray(d["times"])
        for b in d["bs"]:
            ta = arrival_measured(tt, d["F_exact"][str(b)])
            if ta is not None and tp[b] > 0:
                ratios.append(ta / tp[b])
                calib_rows.append(dict(job=os.path.basename(f), b=b, t_meas_us=ta * 1e6, path=tp[b], ratio=ta / tp[b]))
        jobs.append(dict(f=f, d=d, hn=hn, probe=probe, xyz=xyz, names=names, b0=b0, idx=idx))
    ratios = np.asarray(ratios)
    c_med = float(np.median(ratios))
    c_lo, c_hi = [float(x) for x in np.percentile(ratios, [10, 90])]
    print(f"calibration: t_meas / path_time: median {c_med:.3f}, 10-90% [{c_lo:.3f}, {c_hi:.3f}], n = {len(ratios)}")

    # ---- cross-check against embedding (time the added protons first move a signal by > sigma)
    xchk = []
    for f in sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_embed", "*.json"))):
        d = json.load(open(f))
        names, xyz, res = H[d["pdb"]]
        rb = np.random.default_rng(1000 + d["orient"]).standard_normal(3)   # identical to scripts/nmr_embed.random_b0
        b0 = rb / np.linalg.norm(rb)
        iso = d["envs"]["iso"]; tt = np.asarray(iso["times"])
        for env, n_env in (("exact_N12", 12), ("exact_N14", 14)):
            e = d["envs"].get(env)
            if e is None:
                continue
            for key in ("S", "F"):
                if e.get(key) is None:
                    continue
                dev = np.max([np.abs(np.asarray(e[key][str(b)]) - np.asarray(iso[key][str(b)])) for b in d["bs"]], axis=0)
                k = next((i for i in range(len(tt)) if dev[i] > 0.01), None)
                idx = SP.cluster(xyz, d["probe"], n_env)
                dm = SP.couplings(xyz[idx], b0)
                tp = path_times(dm, [0] + list(d["bs"])).min(axis=0)     # multi-source: probe and observed b's
                pmin = float(tp[10:n_env].min())
                pred = c_med * pmin
                row = dict(file=os.path.basename(f), env=env, obs=key,
                           t_first_dev_gt_sigma_us=float(tt[k] * 1e6) if k is not None else None,
                           predicted_arrival_added_us=float(pred * 1e6), path_added=pmin)
                if k is not None:
                    # influence calibration; the recorded grid is 20 us, so bracket [t_{k-1}, t_k]
                    row["c_infl"] = float(tt[k] / pmin)
                    row["c_infl_lo"] = float(tt[k - 1] / pmin)
                xchk.append(row)
    for x in xchk:
        print("cross-check", x)
    ci = np.asarray([x["c_infl"] for x in xchk if "c_infl" in x])
    cil = np.asarray([x["c_infl_lo"] for x in xchk if "c_infl" in x])
    ci_med, ci_min, ci_max = float(np.median(np.sqrt(ci * np.maximum(cil, 1e-30)))), float(cil.min()), float(ci.max())
    print(f"influence calibration (added protons move a signal by > sigma): c_infl geometric-mid median {ci_med:.3f}, "
          f"bracket [{ci_min:.3f}, {ci_max:.3f}] (arrival-at-b calibration was {c_med:.3f})")

    # ---- N_eff(t) in the whole molecule
    out_jobs = []
    for J in jobs:
        d = J["d"]
        dm = SP.couplings(J["xyz"], J["b0"])
        tp = path_times(dm, [J["probe"]] + [int(J["idx"][b]) for b in d["bs"]]).min(axis=0)
        dist = np.linalg.norm(J["xyz"] - J["xyz"][J["probe"]], axis=1)
        grid = (80, 160, 320) if not J["hn"] else (250, 500, 1000)
        rec = dict(job=os.path.basename(J["f"]), network="amide-only" if J["hn"] else "dense", n_protons_molecule=len(dist),
                   t_c_echo_us=d["times"][d["best_t_c_otoc_index"]] * 1e6 if d.get("best_t_c_otoc_index") is not None and d["best_t_c_otoc_index"] < len(d["times"]) else None)
        for t in grid:
            for lab, c in (("arrival_med", c_med), ("infl_med", ci_med), ("infl_fast", ci_min), ("infl_slow", ci_max)):
                rec[f"Neff_{t}us_{lab}"] = int(np.sum(c * tp <= t * 1e-6))
        for R in (4, 6, 8, 10, 12):
            rec[f"N_within_{R}A"] = int(np.sum(dist <= R))
        # where does the echo FI accrue?  t50 / t90 of the summed per-time echo FI; N_eff there
        tt_ = np.asarray(d["times"])
        fi = np.sum([np.asarray(p["FI_otoc_t"]) for p in d["params"] if "FI_otoc_t" in p], axis=0)
        cf = np.cumsum(fi) / fi.sum()
        for q in (0.5, 0.9):
            tq = float(np.interp(q, cf, tt_))
            rec[f"t{int(q * 100)}_echoFI_us"] = tq * 1e6
            for lab, c in (("infl_med", ci_med), ("infl_fast", ci_min), ("infl_slow", ci_max)):
                rec[f"Neff_at_t{int(q * 100)}_{lab}"] = int(np.sum(c * tp <= tq))
        # exact-classical reach: first time the light cone exceeds N_wall spins (memory wall of a leadership machine;
        # 47 = 3 state vectors of 2^N complex128 in 4 PB; 51 with sector reduction + single precision)
        tmax = float(tt_[-1])
        for Nw in (47, 51):
            for lab, c in (("infl_med", ci_med), ("infl_fast", ci_min), ("infl_slow", ci_max)):
                ts = np.sort(c * tp)
                rec[f"t_ex_N{Nw}_{lab}_us"] = float(ts[Nw] * 1e6) if len(ts) > Nw and ts[Nw] <= tmax else None
        out_jobs.append(rec)
        print(rec)
    json.dump(dict(calibration=dict(c_median=c_med, c_p10=c_lo, c_p90=c_hi, n=len(ratios), rows=calib_rows),
                   influence_calibration=dict(c_mid_median=ci_med, c_fast=ci_min, c_slow=ci_max,
                                              note="first time an added environment proton moves any observed S or F by > sigma, "
                                                   "divided by its multi-source path time; 20-us recording grid bracketed"),
                   embedding_crosscheck=xchk, jobs=out_jobs), open(os.path.join(HERE, "lightcone.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
