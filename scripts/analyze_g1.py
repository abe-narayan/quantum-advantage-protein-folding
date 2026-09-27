"""Analyse G1 (Program A) results: mode census (256 and 2048 restarts), lambda-path NRPT (pilot + T-scan) and
temperature replica exchange (cooperativity).  Writes research/results/PROCESSED/g1_summary.json and prints tables.

Quantities:
  census: n_modes/restarts (search saturation), p_hit(best mode), first-hit restart, discovery-curve slope at the end
          (new modes per restart over the last quarter: ~1 => unsaturated), Spearman(E, RMSD) over modes (transmission),
          rank of the best-RMSD mode in energy order.
  nrpt:   Lambda, rungs, round trips, deepest penetration of a prior-origin replica, posterior spread vs error.
  tpt:    C_max per residue vs L (first-order signature: grows with L), T at C_max, histogram bimodality at the peak
          rung (dip ratio), Lee-Kosterlitz barrier estimate ln(Ppeak/Pvalley) where bimodal, round trips.
"""
from __future__ import annotations
import glob, json, os
from collections import defaultdict
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research", "results", "RAW")


def census(sub):
    rows = []
    for f in glob.glob(os.path.join(RAW, sub, "*.json")):
        r = json.load(open(f))
        cur = r["discovery_curve"]["1000000000.0"]
        R = len(cur); q = max(1, R // 4)
        slope = (cur[-1] - cur[-q - 1]) / q
        rows.append(dict(crop=r["crop"], L=r["L"], R=r["restarts"], n_modes=r["n_modes"], frac_modes=r["n_modes"] / r["restarts"],
                         p_hit=r["p_hit_best_mode"], first_hit=r["first_hit_best_mode"], new_mode_rate_end=slope,
                         rho_E_rmsd=r.get("spearman_E_rmsd_modes"), rank_best_rmsd=r.get("rank_of_best_rmsd_mode_by_E"),
                         best_mode_rmsd=r["best_mode_rmsd_native"], min_mode_rmsd=r.get("min_mode_rmsd"), secs=r["secs"],
                         grad_evals=r["grad_evals"]))
    return rows


def tpt_rows():
    rows = []
    for f in glob.glob(os.path.join(RAW, "tpt", "*.json")):
        r = json.load(open(f))
        z = np.load(f.replace(".json", ".npz"))
        E = z["E"]; Ts = z["Ts"]; burn = len(E) // 5; E = E[burn:]
        C = E.var(0) / Ts ** 2
        k = int(np.argmax(C))
        h, edges = np.histogram(E[:, k], bins=30)
        hs = np.convolve(h, np.ones(3) / 3, "same")
        # bimodality: two local maxima separated by a dip; dip ratio = min between peaks / smaller peak
        pk = [i for i in range(1, len(hs) - 1) if hs[i] >= hs[i - 1] and hs[i] >= hs[i + 1] and hs[i] > 0.1 * hs.max()]
        dip = None
        if len(pk) >= 2:
            a, b = pk[0], pk[-1]
            dip = float(hs[a:b + 1].min() / min(hs[a], hs[b]))
        rows.append(dict(crop=r["crop"], L=r["L"], scans=r["scans"], trips=r["trips"], Cmax_per_res=float(C.max() / r["L"]),
                         T_Cmax=float(Ts[k]), n_peaks=len(pk), dip_ratio=dip,
                         LK_barrier=(float(-np.log(max(dip, 1e-6))) if dip is not None else 0.0), secs=r["secs"]))
    return rows


def nrpt_rows(sub):
    rows = []
    for f in glob.glob(os.path.join(RAW, sub, "*.json")):
        r = json.load(open(f))
        e = r.get("eval", {})
        rows.append(dict(crop=r["crop"], L=r["L"], T=r["T"], rungs=r["rungs"], Lambda=r["Lambda"], trips=r["round_trips"],
                         scans=r["scans"], deepest=r.get("deepest_rung_label0"), first_top=r.get("first_top_scan_label0"),
                         post_rmsd=e.get("post_expected_rmsd"), spread=e.get("pairwise_rmsd_mean"),
                         lowestE_pol=e.get("lowestE_polished_rmsd"), grad=r["grad_evals_total"], secs=r["secs"]))
    return rows


def main():
    out = dict(census256=census("g1_modes"), census2k=census("g1_modes2k"), tpt=tpt_rows(),
               nrpt_pilot=nrpt_rows("g1_pilot"), nrpt_tscan=nrpt_rows("g1_tscan"))
    os.makedirs(os.path.join(ROOT, "research", "results", "PROCESSED"), exist_ok=True)
    json.dump(out, open(os.path.join(ROOT, "research", "results", "PROCESSED", "g1_summary.json"), "w"), indent=0)
    for name in ("census256", "census2k"):
        by = defaultdict(list)
        for x in out[name]:
            by[x["L"]].append(x)
        if not by:
            continue
        print(f"\n{name}:  L  n  frac_modes  p_hit(gmean)  new_mode_rate_end  rho(E,RMSD)  best-RMSD-mode rank  bestE-mode RMSD  min-mode RMSD")
        for L in sorted(by):
            a = by[L]
            ph = np.array([x["p_hit"] for x in a])
            rho = [x["rho_E_rmsd"] for x in a if x["rho_E_rmsd"] is not None]
            rk = [x["rank_best_rmsd"] for x in a if x["rank_best_rmsd"] is not None]
            mm = [x["min_mode_rmsd"] for x in a if x["min_mode_rmsd"] is not None]
            print(f"   {L:4d} {len(a):2d} {np.median([x['frac_modes'] for x in a]):9.2f} {np.exp(np.mean(np.log(ph))):12.4f} "
                  f"{np.median([x['new_mode_rate_end'] for x in a]):16.2f} {np.median(rho) if rho else float('nan'):11.2f} "
                  f"{np.median(rk) if rk else float('nan'):16.0f} {np.median([x['best_mode_rmsd'] for x in a]):15.2f} "
                  f"{np.median(mm) if mm else float('nan'):12.2f}")
    if out["tpt"]:
        print("\ntpt: crop L scans trips Cmax/res T_Cmax peaks dip LK")
        for x in sorted(out["tpt"], key=lambda x: (x["L"], x["crop"])):
            print(f"   {x['crop']:12s} {x['L']:4d} {x['scans']:6d} {x['trips']:4d} {x['Cmax_per_res']:7.3f} {x['T_Cmax']:6.2f} {x['n_peaks']:2d} "
                  f"{('%.3f' % x['dip_ratio']) if x['dip_ratio'] is not None else '  -  '} {x['LK_barrier']:.2f}")
    for name in ("nrpt_pilot", "nrpt_tscan"):
        if out[name]:
            print(f"\n{name}: crop L T rungs Lambda trips scans deepest post_rmsd spread lowestE_pol")
            for x in sorted(out[name], key=lambda x: (x["crop"], x["T"])):
                print(f"   {x['crop']:12s} {x['L']:4d} {x['T']:4.1f} {x['rungs']:3d} {x['Lambda']:6.1f} {x['trips']:4d} {x['scans']:6d} "
                      f"{str(x['deepest']):>4s} {x['post_rmsd'] or float('nan'):6.2f} {x['spread'] or float('nan'):6.2f} {x['lowestE_pol'] or float('nan'):6.2f}")


if __name__ == "__main__":
    main()
