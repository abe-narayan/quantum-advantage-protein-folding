"""R1_fi_method / tests FD and GRID (exact model only, cheap).
FD:   Fisher information (transfer S, echo F) with central-difference step h in {0.02, 0.05, 0.1} A, plus a Richardson
      estimate from (0.05, 0.1); reports FI_total per parameter and the hard fraction at the stored best-adversary t_c.
GRID: the same with every Trotter step recorded (rec = 1) vs the production grid (rec = steps/nt); FI per time point is
      normalised by the number of points (so totals are comparable at equal total measurement effort), and the hard
      fraction is reported with the partition at the stored t_c and at the previous grid point (t_c resolution).
Jobs: 1UBQ p19 N=8 dense, 1UBQ p19 N=10 dense (gate t_c^F = 80 us), 1UBQ HN p19 N=10 amide-only (dt = 5 us, t_c^F = 650 us).
"""
from __future__ import annotations

import json
import time

import numpy as np

from fi_common import RAW, dump, exact, geom, setup

SIG = 0.01


def fi_profiles(cfg, h, dt, steps, rec, params_idx=None):
    bs = cfg["bs"]
    P = cfg["params"] if params_idx is None else [cfg["params"][i] for i in params_idx]
    out = {}
    for p in P:
        tt, Sp, Fp = exact(cfg, geom(cfg, p, +h), dt=dt, steps=steps, rec=rec)
        _, Sm, Fm = exact(cfg, geom(cfg, p, -h), dt=dt, steps=steps, rec=rec)
        fS = sum(((Sp[b] - Sm[b]) / (2 * h)) ** 2 for b in bs) / SIG ** 2
        fF = sum(((Fp[b] - Fm[b]) / (2 * h)) ** 2 for b in bs) / SIG ** 2
        dS = np.concatenate([(Sp[b] - Sm[b]) / (2 * h) for b in bs]); dF = np.concatenate([(Fp[b] - Fm[b]) / (2 * h) for b in bs])
        out[p["name"]] = dict(FI_t_S=fS, FI_t_F=fF, dS=dS, dF=dF, t=tt)
    return out


def main():
    jobs = [dict(tag="1UBQ_p19_N8", pdb="1UBQ", probe=19, N=8, hn=False, dt=2e-6, steps=160, nt=16, tcF_us=None),
            dict(tag="1UBQ_p19_N10", pdb="1UBQ", probe=19, N=10, hn=False, dt=2e-6, steps=160, nt=16, tcF_us=80.0,
                 gate="nmr_gate/1UBQ_p19_N10_o0_g0.json"),
            dict(tag="1UBQHN_p19_N10", pdb="1UBQ", probe=19, N=10, hn=True, dt=5e-6, steps=200, nt=20, tcF_us=650.0,
                 gate="nmr_gate_hn/1UBQHN_p19_N10_o0_g0.json")]
    res = {}
    for j in jobs:
        t0 = time.time()
        cfg = setup(j["pdb"], j["probe"], j["N"], 0, hn_only=j["hn"])
        rec = j["steps"] // j["nt"]
        if j.get("gate"):
            g = json.load(open(f"{RAW}/{j['gate']}"))
            assert g["bs"] == cfg["bs"]
        fd = {h: fi_profiles(cfg, h, j["dt"], j["steps"], rec) for h in (0.02, 0.05, 0.1)}
        tt = fd[0.05][cfg["params"][0]["name"]]["t"] * 1e6
        tc = int(np.searchsorted(tt, j["tcF_us"] - 1e-6)) if j["tcF_us"] else None
        rows = {}
        for p in cfg["params"]:
            n = p["name"]
            r_ = {}
            for key in ("S", "F"):
                tot = {h: float(fd[h][n][f"FI_t_{key}"].sum()) for h in fd}
                # Richardson on the derivative: d_R = (4 d(h) - d(2h)) / 3 with h = 0.05
                dR = (4 * fd[0.05][n]["d" + key] - fd[0.1][n]["d" + key]) / 3
                totR = float((dR ** 2).sum() / SIG ** 2)
                fh = {h: (float(fd[h][n][f"FI_t_{key}"][tc:].sum() / max(tot[h], 1e-30)) if tc is not None else None) for h in fd}
                r_[key] = dict(FI_total={str(h): v for h, v in tot.items()}, FI_total_richardson=totR,
                               rel_change_002_vs_005=tot[0.02] / tot[0.05] - 1, rel_change_01_vs_005=tot[0.1] / tot[0.05] - 1,
                               rel_richardson_vs_005=totR / tot[0.05] - 1, frac_hard_at_tc={str(h): v for h, v in fh.items()},
                               max_rel_deriv_err_002_vs_005=float(np.max(np.abs(fd[0.02][n]["d" + key] - fd[0.05][n]["d" + key])) /
                                                                  max(np.max(np.abs(fd[0.05][n]["d" + key])), 1e-30)))
            rows[n] = r_
        # fine grid (rec = 1) at h = 0.05
        fine = fi_profiles(cfg, 0.05, j["dt"], j["steps"], 1)
        tf = fine[cfg["params"][0]["name"]]["t"] * 1e6
        grid = {}
        for p in cfg["params"]:
            n = p["name"]
            gg = {}
            for key in ("S", "F"):
                c_ = fd[0.05][n][f"FI_t_{key}"]; f_ = fine[n][f"FI_t_{key}"]
                gg[key] = dict(FI_per_point_coarse=float(c_.sum() / len(c_)), FI_per_point_fine=float(f_.sum() / len(f_)))
                if j["tcF_us"]:
                    for lab, tcut in (("at_tc", j["tcF_us"]), ("at_prev_point", j["tcF_us"] - (tt[1] - tt[0]))):
                        gg[key][f"frac_hard_coarse_{lab}"] = float(c_[tt >= tcut - 1e-6].sum() / max(c_.sum(), 1e-30))
                        gg[key][f"frac_hard_fine_{lab}"] = float(f_[tf >= tcut - 1e-6].sum() / max(f_.sum(), 1e-30))
            grid[n] = gg
        res[j["tag"]] = dict(params=[p["name"] for p in cfg["params"]], tc_index=tc, times_us=tt.tolist(), fd=rows, grid=grid,
                             secs=time.time() - t0)
        print("==", j["tag"], f"{time.time()-t0:.1f}s")
        for n in rows:
            for key in ("S", "F"):
                z = rows[n][key]; gz = grid[n][key]
                print(f"  {n:22s} {key} FI(h=.02/.05/.1) {z['FI_total']['0.02']:9.1f} {z['FI_total']['0.05']:9.1f} {z['FI_total']['0.1']:9.1f} "
                      f"Richardson {z['FI_total_richardson']:9.1f}  frac_hard@tc {z['frac_hard_at_tc']} | per-pt coarse {gz['FI_per_point_coarse']:.2f} "
                      f"fine {gz['FI_per_point_fine']:.2f} " + " ".join(f"{k}={v:.3f}" for k, v in gz.items() if k.startswith('frac')))
    print("wrote", dump(res, "fd_grid_checks.json"))


if __name__ == "__main__":
    main()
