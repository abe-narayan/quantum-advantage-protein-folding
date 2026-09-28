"""Relevance verifier for ROUND3/r1sim_exact_reach (read-only analysis; no new dynamics).

Two questions:
 (A) Which part of the late-window echo is still drifting with N (the part that puts the converged echo beyond exact reach)?
     Exact identity (DERIVED; also stated by the sibling verify_classical lane, and in R1_theory_hardness §3.4c):
        W = Z_a(t) = sum_j G_j Z_j + W_rest,  G_j = Tr[W Z_j]/2^N  (two-point transfer a->j)
        F_ab = H + R_ab,  H = sum_j G_j^2 (b-independent, two-point only),  R_ab = Tr[W_rest Z_b W_rest Z_b]/2^N.
     We split each ladder step dF_N = F_{N+2}-F_N into dH (two-point, the K-104 class) and dR (the rest), and further
     separate the finite-cluster sector floor (floor(t) = Tr[W_rest (Z_tot/N) W_rest (Z_tot/N)]/2^N, -> 0 as N -> inf).
     Inputs: F ladders from the lane (reach_summary.json; N=12..18 governor reference, N=20 lane);
             H and floor from the sibling verify_classical/runs (honly mode, same circuit, different random vectors).
 (B) Where do the claim's times sit relative to the physical reversal horizon?
     T2 values from ADVERSARIAL/R1_physics_feasibility/scales.json; envelopes from reversal_envelope.py (Sanchez 2022).
Output: relevance_decomp.json (this folder).
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ADV = os.path.join(LANE, "..", "..", "ADVERSARIAL")
SIGMA = 0.01


def load_H():
    out = {}
    for f in glob.glob(os.path.join(LANE, "verify_classical", "runs", "1UBQ_p*_N*_probe_honly_*.json")):
        if f.endswith(".ckpt.json"):
            continue
        d = json.load(open(f))
        if not d.get("complete"):
            continue
        ts = [round(t) for t in d["times_us"]]
        key = (d["probe"], d["N"])
        # prefer the larger-R file if duplicates
        if key in out and out[key]["R"] >= d["R"]:
            continue
        out[key] = dict(R=d["R"], H={t: h for t, h in zip(ts, d["H"])}, floor={t: x for t, x in zip(ts, d["floor"])},
                        file=os.path.basename(f))
    return out


def main():
    rs = json.load(open(os.path.join(LANE, "reach_summary.json")))
    Hd = load_H()
    res = dict(inputs=dict(F="reach_summary.json convergence (lane)", H_floor=sorted(v["file"] for v in Hd.values())),
               decomposition={}, step_shares={}, reversal={})
    for key, conv in rs["convergence"].items():
        probe = int(key.split("_")[0][1:])
        t = int(key.split("_")[1][1:])
        Ns = conv["Ns"]
        rows = {}
        for site, fit in conv["fits"].items():
            F = dict(zip(Ns, fit["F"]))
            r = []
            for N in Ns:
                h = Hd.get((probe, N))
                if h is None or t not in h["H"]:
                    r.append(dict(N=N, F=F[N], H=None, floor=None, R=None, X=None))
                    continue
                H, fl = h["H"][t], h["floor"][t]
                r.append(dict(N=N, F=F[N], H=H, floor=fl, R=F[N] - H, X=F[N] - H - fl, invN=1.0 / N))
            rows[site] = r
        res["decomposition"][key] = rows
        # steps
        steps = []
        for i in range(len(Ns) - 1):
            N0, N1 = Ns[i], Ns[i + 1]
            for site, r in rows.items():
                a, b = r[i], r[i + 1]
                if a["H"] is None or b["H"] is None:
                    continue
                dF = b["F"] - a["F"]
                dH = b["H"] - a["H"]
                dfl = b["floor"] - a["floor"]
                dR = dF - dH
                dX = dF - dH - dfl
                steps.append(dict(site=site, N=N0, N_next=N1, dF=dF, dH=dH, dfloor=dfl, dR=dR, dX=dX,
                                  frac_H=(dH / dF if abs(dF) > 1e-12 else None),
                                  frac_H_plus_floor=((dH + dfl) / dF if abs(dF) > 1e-12 else None)))
        res["step_shares"][key] = steps
        # aggregate over sites for the last two steps with H
        agg = {}
        for s in steps:
            agg.setdefault(f"{s['N']}->{s['N_next']}", []).append(s)
        res["step_shares"][key + "_agg"] = {
            k: dict(mean_abs_dF=float(np.mean([abs(s["dF"]) for s in v])),
                    dH=float(v[0]["dH"]), dfloor=float(v[0]["dfloor"]),
                    mean_abs_dR=float(np.mean([abs(s["dR"]) for s in v])),
                    mean_abs_dX=float(np.mean([abs(s["dX"]) for s in v])),
                    max_abs_dR=float(np.max([abs(s["dR"]) for s in v])),
                    max_abs_dX=float(np.max([abs(s["dX"]) for s in v])),
                    max_abs_dF=float(np.max([abs(s["dF"]) for s in v])))
            for k, v in agg.items()}

    # (B) reversal horizon mapping
    sc = json.load(open(os.path.join(ADV, "R1_physics_feasibility", "scales.json")))
    T2 = {}
    for j in sc["jobs"]:
        if j["pdb"] == "1UBQ" and not j["hn_only"]:
            T2.setdefault("cluster", []).append(j["T2_cluster_us"])
            T2.setdefault("network_static", []).append(j["T2_network_static_us"])
            if "T2_network_rotoravg_us" in j:
                T2.setdefault("network_rotoravg", []).append(j["T2_network_rotoravg_us"])

    def env_logistic(x, c, lam_frac=0.25):
        T3 = c
        l_ = lam_frac * T3
        return (1 + math.exp(-T3 / l_)) / (1 + math.exp((x - T3) / l_))

    def env_gauss(x, c):
        return math.exp(-math.log(2) * (x / c) ** 2)

    rev = {}
    for name, vals in T2.items():
        lo, hi = min(vals), max(vals)
        for t in (40, 80, 160, 240, 320):
            for tag, T2v in (("T2_min", lo), ("T2_max", hi)):
                x = t / T2v
                rev.setdefault(name, {}).setdefault(str(t), {})[tag] = dict(
                    T2_us=T2v, t_over_T2=x,
                    A_LE_logistic_T3_6p7=env_logistic(x, 1 / 0.15, 1.7 * 0.15),
                    A_PE_gauss_T3_4=env_gauss(x, 4.0),
                    A_forward_plus_backward_LE=env_logistic(2 * x, 1 / 0.15, 1.7 * 0.15))
        rev[name]["T3_LE_us_range"] = [6.7 * lo, 6.7 * hi]
        rev[name]["T3_PE_us_range"] = [4.0 * lo, 4.0 * hi]
    res["reversal"] = rev
    # physically observable echo amplitude A(t) * F_N20(t) at the claim's times, most generous envelope
    # (cluster T2, largest value, forward time only) and the network-static envelope; compare with sigma = 0.01
    obs = {}
    for key, conv in rs["convergence"].items():
        t = str(int(key.split("_")[1][1:]))
        Nlast = conv["Ns"][-1]
        for site, fit in conv["fits"].items():
            F = fit["F"][-1]
            for name in ("cluster", "network_rotoravg", "network_static"):
                A = rev[name][t]["T2_max"]["A_LE_logistic_T3_6p7"]
                obs.setdefault(key, {}).setdefault(site, {})[name] = dict(N=Nlast, F=F, A=A, AF=A * F,
                                                                         AF_over_sigma=A * F / SIGMA)
    res["observable_amplitude"] = obs
    json.dump(res, open(os.path.join(HERE, "relevance_decomp.json.tmp"), "w"), indent=1)
    os.replace(os.path.join(HERE, "relevance_decomp.json.tmp"), os.path.join(HERE, "relevance_decomp.json"))

    # console summary
    for key in rs["convergence"]:
        print("==", key)
        for site, r in res["decomposition"][key].items():
            print("  site", site, " ".join(
                f"N{x['N']}:F={x['F']:.3f}" + (f",H={x['H']:.3f},fl={x['floor']:.3f},R={x['R']:.3f},X={x['X']:.3f}"
                                               if x['H'] is not None else "") for x in r))
        for k, v in res["step_shares"][key + "_agg"].items():
            print(f"  step {k}: max|dF|={v['max_abs_dF']:.4f} dH={v['dH']:+.4f} dfloor={v['dfloor']:+.4f} "
                  f"max|dR|={v['max_abs_dR']:.4f} max|dX|={v['max_abs_dX']:.4f}")
    for key, v in obs.items():
        print("A*F/sigma", key, {s: {n: round(x["AF_over_sigma"], 3) for n, x in d.items()} for s, d in v.items()})
    for name, v in rev.items():
        print(name, "T3_LE us", [round(x, 1) for x in v["T3_LE_us_range"]],
              {t: (round(v[t]["T2_min"]["t_over_T2"], 1), round(v[t]["T2_max"]["t_over_T2"], 1),
                   f"{v[t]['T2_max']['A_LE_logistic_T3_6p7']:.1e}") for t in ("40", "80", "160", "240", "320")})


if __name__ == "__main__":
    main()
