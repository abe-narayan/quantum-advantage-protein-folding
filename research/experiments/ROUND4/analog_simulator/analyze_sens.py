"""Summarise sens_*.json: per channel and level, over instrument sites b and times t in the physical window
(40-120 us): rms and mean of dF = S - F0 across realisations, and for R-channels the normalised dF_norm = S/R - F0.
Tolerance eps*: the level at which max_(b,t) rms|dF| reaches sigma = 0.01, by log-log interpolation between
bracketing levels (power-law extrapolation flagged when outside the scanned range).  Writes sens_summary.json."""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIGMA = 0.01
WINDOW = (40.0, 120.0)


def tol(levels, vals, target=SIGMA):
    lv = np.array(levels, float); v = np.array(vals, float)
    ok = v > 0
    lv, v = lv[ok], v[ok]
    if len(lv) == 0:
        return None, "no-signal"
    for i in range(len(lv) - 1):
        if (v[i] - target) * (v[i + 1] - target) <= 0:
            s = math.log(v[i + 1] / v[i]) / math.log(lv[i + 1] / lv[i])
            return float(lv[i] * (target / v[i]) ** (1 / s)), "interp"
    if len(lv) >= 2:
        s = math.log(v[-1] / v[0]) / math.log(lv[-1] / lv[0])
        ref = 0 if v[0] > target else -1
        return float(lv[ref] * (target / v[ref]) ** (1 / s)), f"extrap(slope={s:.2f})"
    return None, "single"


def summarise(path):
    d = json.load(open(path))
    ts = d["times_us"]
    win = [i for i, t in enumerate(ts) if WINDOW[0] <= t <= WINDOW[1]]
    F0 = {b: np.array(v) for b, v in d["baseline"]["F"].items()}
    groups = {}
    for key, u in d["units"].items():
        ch, lv, rep = key.split("|")
        groups.setdefault(ch, {}).setdefault(float(lv), []).append((rep, u))
    out = dict(pdb=d["pdb"], probe=d["probe"], N=d["N"], times_us=ts, window_idx=win, rmin_A=d["rmin_A"],
               F0={b: v.tolist() for b, v in F0.items()}, H=d["baseline"]["H"], channels={})
    for ch, bylv in groups.items():
        rows = {}
        if ch == "delete_j":
            per_j = {}
            for rep, u in bylv[0.0]:
                dF = np.array([np.array(u["S"][b]) - F0[b] for b in F0])[:, win]
                per_j[rep] = float(np.abs(dF).max())
            mean_abs = float(np.mean([np.mean(np.abs(np.array([np.array(u["S"][b]) - F0[b] for b in F0])[:, win]))
                                      for _, u in bylv[0.0]]))
            out["channels"][ch] = dict(max_abs_dF_per_j=per_j, mean_abs_dF_over_j_b_t=mean_abs,
                                       median_max_abs=float(np.median(list(per_j.values()))))
            continue
        levels = sorted(bylv)
        for lv in levels:
            us = [u for _, u in bylv[lv]]
            dF = np.array([[np.array(u["S"][b]) - F0[b] for b in F0] for u in us])[:, :, win]   # rep, b, t
            rms = np.sqrt((dF ** 2).mean(0))
            mean = dF.mean(0)
            r = dict(nrep=len(us), max_rms=float(rms.max()), max_abs_mean=float(np.abs(mean).max()),
                     mean_rms=float(rms.mean()), rms_bt=rms.tolist(), mean_bt=mean.tolist())
            if us[0].get("R"):
                dN = np.array([[np.array(u["S"][b]) / np.array(u["R"][b]) - F0[b] for b in F0] for u in us])[:, :, win]
                r["max_abs_dF_normalised"] = float(np.abs(dN).max())
                r["R_min"] = float(min(min(u["R"][b][i] for i in win) for u in us for b in F0))
            rows[str(lv)] = r
        e_rms, how = tol(levels, [rows[str(l)]["max_rms"] for l in levels])
        e_bias, how_b = tol(levels, [rows[str(l)]["max_abs_mean"] for l in levels])
        out["channels"][ch] = dict(levels=rows, eps_star_rms=e_rms, eps_star_rms_how=how,
                                   eps_star_bias=e_bias, eps_star_bias_how=how_b)
    return out


def main():
    res = {}
    for p in sorted(glob.glob(os.path.join(HERE, "sens_*_N*.json"))):
        if p.endswith("summary.json"):
            continue
        s = summarise(p)
        res[f"{s['pdb']}_p{s['probe']}_N{s['N']}"] = s
    json.dump(res, open(os.path.join(HERE, "sens_summary.json"), "w"), indent=1)
    for k, s in res.items():
        print("==", k, "rmin %.2f A" % s["rmin_A"])
        for ch, c in s["channels"].items():
            if ch == "delete_j":
                print("  %-14s per-j max|dF| median %.3f, mean|dF| %.3f" % (ch, c["median_max_abs"],
                                                                         c["mean_abs_dF_over_j_b_t"]))
                continue
            lv = "  ".join("%s: rms %.4f bias %.4f%s" % (l, r["max_rms"], r["max_abs_mean"],
                           (" norm %.4f" % r["max_abs_dF_normalised"]) if "max_abs_dF_normalised" in r else "")
                           for l, r in c["levels"].items())
            e = c["eps_star_rms"]
            print("  %-14s eps*=%s (%s) | %s" % (ch, ("%.4f" % e) if e else None, c["eps_star_rms_how"], lv))


if __name__ == "__main__":
    main()
