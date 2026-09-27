"""R1 theory_hardness, step E: combine the measured sigma-cone (pauli_cone_*.json), the exact finite-size data
(front/*.json), the density table (density_couplings.json) and the front models (front_model.json) into one table
N_cone(t) at t = 40, 80, 160, 320 us, with the cost of exact classical simulation at that N.

Definitions (stated in README):
  N_sigma(t): smallest cluster size N in the nested ladder such that every later ladder step changes max_{b<12} F_ab(t)
              by <= sigma + L_N + L_N' (L = discarded norm of the sparse-Pauli run, the heuristic certificate).
              'uncertified' if the certificate width itself exceeds sigma (then only an indicative value).
  Extrapolations from N_sigma(40 us) to later times:
     E1 (conservative, MEASURED-trend): power law N ~ t^alpha fitted to the ladder values at 20-40 us (alpha < 1 at
        these radii; physically alpha should grow toward 3 (ballistic) or 1.5 (diffusive), so E1 is a floor).
     E2 (diffusive front): r(t) = r_sigma(40) * sqrt(t/40), N = N(r) from the buried-proton radial count.
     E3 (ballistic front): r(t) = r_sigma(40) * t/40, N = N(r).
     E4 (front model, k=2 laws, threshold P >= 0.02 calibrated to N_sigma(40)): from front_model.json.
Output: cone_summary.json.  Cost: < 5 s.
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIGMA = 0.01


def n_sigma_from_ladder(fn):
    d = json.load(open(fn))
    Ns = sorted(d["runs"], key=int)
    times = d["runs"][Ns[0]]["times_us"]
    out = []
    for ti, t in enumerate(times):
        steps = []
        for a_, b_ in zip(Ns[:-1], Ns[1:]):
            Fa = np.array(d["runs"][a_]["F"][ti]); Fb = np.array(d["runs"][b_]["F"][ti])
            L = d["runs"][a_]["lost"][ti] + d["runs"][b_]["lost"][ti]
            steps.append((int(a_), int(b_), float(np.abs(Fb - Fa).max()), float(L)))
        # lenient: smallest N such that all later steps are within sigma + L (certificate allowance)
        nsig, cert = None, True
        for k in range(len(steps)):
            if all(s[2] <= SIGMA + s[3] for s in steps[k:]):
                nsig = steps[k][0]
                cert = all(s[3] <= SIGMA for s in steps[k:])
                break
        # strict: smallest N such that all later steps change F by <= sigma (no allowance)
        nstrict = None
        for k in range(len(steps)):
            if all(s[2] <= SIGMA for s in steps[k:]):
                nstrict = steps[k][0]
                break
        out.append(dict(t_us=t, N_sigma=nsig, N_sigma_strict=nstrict, certified=cert, steps=steps,
                        r_max_A={n: d["runs"][n]["r_max_A"] for n in Ns}))
    return out


def N_of_r(r, table):
    Rs = np.array(sorted(float(k) for k in table))
    Ns = np.array([table[str(R) if str(R) in table else f"{R:.1f}"]["mean"] for R in Rs])
    # interpolate in log-log (N ~ r^3 asymptotically); extrapolate with rho * 4/3 pi r^3 beyond the table
    if r <= Rs[-1]:
        return float(np.exp(np.interp(math.log(r), np.log(Rs), np.log(np.maximum(Ns, 1e-9)))))
    return float(Ns[-1] * (r / Rs[-1]) ** 3)


def exact_cost(N):
    """classical exact reference cost at N spins (U(1) sectors): memory of one state vector (complex128),
    largest sector dimension, and dense sector-diagonalisation flops ~ 10 * sum_k C(N,k)^3."""
    sv_bytes = 16.0 * 2 ** N
    dmax = math.comb(N, N // 2)
    diag = 10.0 * sum(float(math.comb(N, k)) ** 3 for k in range(N + 1))
    return dict(N=N, statevector_bytes=sv_bytes, largest_sector=dmax, sector_diag_flops=diag)


def main():
    dens = json.load(open(os.path.join(HERE, "density_couplings.json")))
    fm = json.load(open(os.path.join(HERE, "front_model.json")))
    tq = [40.0, 80.0, 160.0, 320.0]
    res = dict(sigma=SIGMA, probes={})
    for probe in (19, 245):
        fn = os.path.join(HERE, f"pauli_cone_1UBQ_p{probe}.json")
        lad = n_sigma_from_ladder(fn)
        # ladder values at 20, 30, 40 us
        pts = [(x["t_us"], x["N_sigma_strict"], x["certified"]) for x in lad if x["t_us"] >= 19 and x["N_sigma_strict"]]
        tt = np.array([p[0] for p in pts]); nn = np.array([p[1] for p in pts], float)
        alpha = float(np.polyfit(np.log(tt), np.log(nn), 1)[0]) if len(pts) >= 2 else float("nan")
        n40 = float(nn[-1]); t40 = float(tt[-1])
        r40 = json.load(open(fn))["runs"][str(int(n40))]["r_max_A"]
        table = dens["1UBQ"]["N_within_R_buried"]
        E1 = {t: n40 * (t / t40) ** alpha for t in tq}
        E2 = {t: max(n40, N_of_r(r40 * math.sqrt(t / t40), table)) for t in tq}
        E3 = {t: max(n40, N_of_r(r40 * t / t40, table)) for t in tq}
        E4 = {}
        for law in ("golden_k2", "coherent_k2"):
            p = fm["laws"][law]["prediction"][f"1UBQ_p{probe}"]
            ts = p["times_us"]; c = p["N_sites_P_ge"]["0.02"]
            E4[law] = {t: float(np.interp(t, ts, c)) for t in tq}
        nH = 629
        rows = []
        for t in tq:
            vals = [E2[t], E3[t]] + [E4[k][t] for k in E4]           # physically motivated front laws
            lo, hi = min(vals), min(max(vals), nH)
            rows.append(dict(t_us=t, E1_floor_powerlaw=E1[t], E2_diffusive=E2[t], E3_ballistic=E3[t],
                             E4_golden_k2=E4["golden_k2"][t], E4_coherent_k2=E4["coherent_k2"][t],
                             range_physical=[lo, hi], floor_E1=E1[t], protein_nH=nH,
                             exact_cost_at_low=exact_cost(int(round(min(lo, 60)))),
                             physical_low_exceeds_30=bool(lo > 30), physical_low_exceeds_40=bool(lo > 40),
                             floor_exceeds_30=bool(E1[t] > 30)))
        res["probes"][str(probe)] = dict(ladder=lad, alpha_20_40us=alpha, N_sigma_40us=n40, r_sigma_40us_A=r40,
                                         table=rows)
        print("probe", probe, "N_sigma ladder (t, lenient, strict, certified):",
              [(round(x['t_us']), x['N_sigma'], x['N_sigma_strict'], x['certified']) for x in lad],
              "alpha %.2f r40 %.2f" % (alpha, r40))
        for r in rows:
            print("   t=%3d  E1(floor) %.0f | E2 %.0f  E3 %.0f  E4g %.0f  E4c %.0f  -> physical range [%.0f, %.0f]  low>30 %s" % (
                r["t_us"], r["E1_floor_powerlaw"], r["E2_diffusive"], r["E3_ballistic"], r["E4_golden_k2"],
                r["E4_coherent_k2"], r["range_physical"][0], r["range_physical"][1], r["physical_low_exceeds_30"]))
    res["exact_cost_reference"] = [exact_cost(N) for N in (12, 14, 16, 20, 24, 30, 36, 40, 44, 48, 50)]
    json.dump(res, open(os.path.join(HERE, "cone_summary.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
