"""R1_fi_method / test EB: replace the gate's "bias > sigma" partition by the parameter-estimation error of a fit of the
truncated classical model to exact data.

Inputs: the C2 sparse-Pauli eps ladders (research/results/RAW/nmr_sparse/<tag>.json, which store the exact and truncated
S_ab(t), F_ab(t) for the SAME cluster/B0/time grid as the C1 gate) + exact Jacobians computed here (sector-exact,
central differences, h = 0.05 A, identical parameter construction to scripts/nmr_gate.py).
For every eps and observable (transfer S, echo F plain, echo F norm-corrected) and every window [0, T]:
  gate:  t_c = first index with max_b |bias| > sigma
  EB:    D(T) (joint Mahalanobis bias, all unique parameters), max_k |dphi_k|/sd_k (single-parameter), dphi in Angstrom
  NUIS:  same with nuisance regressors fitted jointly (no oracle): (a) per-b norm-correction direction
         (1 - N_kept) F_c / N_kept (F only); (b) per-b quadratic polynomial in t (all observables)
Derived: t_ok(D<=0.5), t_ok(D<=1) (largest T with the criterion holding at every T' <= T), and C2-style M* under each
criterion (peak strings of the largest eps accurate up to t_50 and up to the full window).
Also the MSE-optimal single-parameter classical information max_T 1/(dphi_k(T)^2 + sd_k(T)^2) vs the gate's FI_easy.
Usage: python estimator_bias.py [tags...]   (default: the four N=8/10 gamma=0 jobs; N=12 partials if --n12)
"""
from __future__ import annotations

import glob
import json
import math
import os
import sys
import time

import numpy as np

from fi_common import RAW, dump, exact, geom, lin_bias, setup, unique_cols

SIG = 0.01
H = 0.05


def jac(cfg, rec, steps=160):
    """exact S, F and Jacobians (n_obs x p) for the gate parameters."""
    bs = cfg["bs"]
    _, S0, F0 = exact(cfg, cfg["X0"], rec=rec, steps=steps)
    JS, JF = [], []
    for p in cfg["params"]:
        _, Sp, Fp = exact(cfg, geom(cfg, p, +H), rec=rec, steps=steps)
        _, Sm, Fm = exact(cfg, geom(cfg, p, -H), rec=rec, steps=steps)
        JS.append(np.concatenate([(Sp[b] - Sm[b]) / (2 * H) for b in bs]))
        JF.append(np.concatenate([(Fp[b] - Fm[b]) / (2 * H) for b in bs]))
    return S0, F0, np.array(JS).T, np.array(JF).T


def poly_G(nb, nt, T, deg=2):
    """per-b polynomial nuisance regressors restricted to the window [0, T)."""
    cols = []
    t = np.arange(nt) / max(nt - 1, 1)
    for bi in range(nb):
        for d in range(deg + 1):
            v = np.zeros(nb * nt)
            v[bi * nt:(bi + 1) * nt] = t ** d
            cols.append(v)
    return np.array(cols).T


def analyse_job(path):
    r = json.load(open(path))
    N, probe, pdb = r["N"], r["probe"], r["pdb"]
    rec, steps = r["rec"], r["steps"]
    cfg = setup(pdb, probe, N, r["orient"])
    assert cfg["bs"] == r["bs"], (cfg["bs"], r["bs"])
    t0 = time.time()
    S0, F0, JS, JF = jac(cfg, rec, steps)
    secs_jac = time.time() - t0
    bs = cfg["bs"]; nb = len(bs)
    ex = r["exact"]
    for b in bs:  # the stored exact reference must equal the one recomputed here
        assert np.max(np.abs(np.asarray(ex["S"][str(b)]) - S0[b])) < 1e-9
        assert np.max(np.abs(np.asarray(ex["F"][str(b)]) - F0[b])) < 1e-9
    nt = len(ex["times"])
    names = [p["name"] for p in cfg["params"]]
    keepS = unique_cols(JS, names); keepF = unique_cols(JF, names)
    out = dict(tag=os.path.basename(path), N=N, probe=probe, pdb=pdb, nt=nt, times_us=(np.asarray(ex["times"]) * 1e6).tolist(),
               params=names, bs=bs, sigma=SIG, h=H, secs_jac=secs_jac, runs=[])
    # exact information per window
    for key, J, keep in (("S", JS, keepS), ("F", JF, keepF)):
        Jk = J[:, keep]
        fi_t = (Jk.reshape(nb, nt, -1) ** 2).sum(0) / SIG ** 2        # (nt, p)
        out[f"FI_t_{key}"] = fi_t.tolist()
        c = np.cumsum(fi_t, 0) / np.maximum(fi_t.sum(0), 1e-30)
        out[f"t50_{key}"] = int(np.median([int(np.searchsorted(c[:, k], 0.5)) for k in range(c.shape[1])]))
        out[f"params_{key}"] = [names[k] for k in keep]
    for x in r["runs"]:
        if len(x["times"]) < nt:
            continue
        row = dict(eps=x["eps"], peak=x.get("peak_strings"), secs=x.get("secs"))
        nk = np.maximum(np.asarray(x["kept_norm2"], float), 1e-12)
        series = {"S": ({b: np.asarray(x["S"][str(b)]) for b in bs}, S0, JS, keepS),
                  "F": ({b: np.asarray(x["F"][str(b)]) for b in bs}, F0, JF, keepF),
                  "Fnc": ({b: np.asarray(x["F"][str(b)]) / nk for b in bs}, F0, JF, keepF)}
        for key, (mc, m0, J, keep) in series.items():
            bias_bt = np.array([mc[b] - m0[b] for b in bs])                  # (nb, nt)
            gate_bad = np.nonzero(np.max(np.abs(bias_bt), 0) > SIG)[0]
            tc_gate = int(gate_bad[0]) if len(gate_bad) else nt
            bvec = bias_bt.reshape(-1)
            Jk = J[:, keep]
            D, smax, dphi_T, sd_T, Dnc, Dpoly, info_poly = [], [], [], [], [], [], []
            for T in range(2, nt + 1):
                m = np.tile(np.arange(nt) < T, nb)
                lb = lin_bias(Jk[m], bvec[m], SIG)
                D.append(lb["D"])
                smax.append(max(abs(s["dphi"]) / s["crb_sd"] for s in lb["single"]))
                dphi_T.append([s["dphi"] for s in lb["single"]]); sd_T.append([s["crb_sd"] for s in lb["single"]])
                if key == "F":        # nuisance (a): per-b norm-correction direction with free coefficient
                    G = np.zeros((nb * nt, nb))
                    for bi, b in enumerate(bs):
                        G[bi * nt:(bi + 1) * nt, bi] = (1 - nk) * mc[b] / nk
                    Dnc.append(lin_bias(Jk[m], bvec[m], SIG, G=G[m])["D"])
                Gp = poly_G(nb, nt, T)[m]
                lbp = lin_bias(Jk[m], bvec[m], SIG, G=Gp)
                Dpoly.append(lbp["D"])
                Fp = np.asarray(lbp["F"]); Ff = np.asarray(lb["F"])
                info_poly.append(float(np.trace(Fp) / max(np.trace(Ff), 1e-30)))
            D = np.array(D); smax = np.array(smax)

            def t_ok(arr, thr):                 # largest window end index T (exclusive) with arr <= thr for all T' <= T
                bad = np.nonzero(np.asarray(arr) > thr)[0]
                return int(bad[0]) + 1 if len(bad) else nt   # arr[i] is for T = i + 2 -> first bad T = i+2 -> ok up to T-1
            res = dict(tc_gate=tc_gate, max_abs_bias=float(np.max(np.abs(bias_bt))), D=D.tolist(), single_max=smax.tolist(),
                       tok_D05=t_ok(D, 0.5), tok_D1=t_ok(D, 1.0), tok_single1=t_ok(smax, 1.0),
                       dphi_full=dphi_T[-1], crb_sd_full=sd_T[-1], D_full=float(D[-1]),
                       Dpoly=Dpoly, tok_Dpoly05=t_ok(Dpoly, 0.5), info_frac_poly_full=info_poly[-1])
            if Dnc:
                res.update(Dnc=Dnc, tok_Dnc05=t_ok(Dnc, 0.5))
            # MSE-optimal single-parameter classical information (oracle choice of T) vs gate FI_easy
            dT = np.array(dphi_T); sT = np.array(sd_T)
            mse = dT ** 2 + sT ** 2
            fi_cstar = (1 / mse).max(0)
            fi_t = (Jk.reshape(nb, nt, -1) ** 2).sum(0) / SIG ** 2
            fi_tot = fi_t.sum(0); fi_easy = fi_t[:tc_gate].sum(0)
            res.update(FI_total=fi_tot.tolist(), FI_easy_gate=fi_easy.tolist(), FI_cstar_mse=fi_cstar.tolist(),
                       gain_gate=(fi_tot / np.maximum(fi_easy, 1e-30)).tolist(), gain_mse=(fi_tot / fi_cstar).tolist(),
                       frac_hard_gate=(1 - fi_easy / np.maximum(fi_tot, 1e-30)).tolist())
            row[key] = res
        out["runs"].append(row)
    # C2-style M* under each criterion
    for key in ("S", "F", "Fnc"):
        t50 = out["t50_" + ("S" if key == "S" else "F")]
        ms = {}
        for crit in ("tc_gate", "tok_D05", "tok_D1", "tok_Dpoly05") + (("tok_Dnc05",) if key != "S" else ()):
            for horizon, hn in ((t50 + 1, "t50"), (nt, "full")):
                acc = [row for row in out["runs"] if key in row and row[key].get(crit, -1) >= horizon]
                best = max(acc, key=lambda z: z["eps"]) if acc else None
                ms[f"{crit}@{hn}"] = dict(eps=best["eps"] if best else None, Mstar=best["peak"] if best else None)
        out["Mstar_" + key] = ms
    return out


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    tags = args or ["1UBQ_p19_N8_o0_g0", "1UBQ_p245_N8_o0_g0", "1UBQ_p19_N10_o0_g0", "1UBQ_p245_N10_o0_g0"]
    res = {}
    for tg in tags:
        f = os.path.join(RAW, "nmr_sparse", tg + ".json")
        if not os.path.exists(f):
            f = f + ".partial"
        t0 = time.time()
        o = analyse_job(f)
        res[tg] = o
        print(f"== {tg}  (jacobian {o['secs_jac']:.1f}s, total {time.time()-t0:.1f}s)  t50_S={o['t50_S']} t50_F={o['t50_F']}")
        for row in o["runs"]:
            for key in ("S", "F", "Fnc"):
                z = row.get(key)
                if not z:
                    continue
                print(f"  eps {row['eps']:<7g} {key:3s} peak {row['peak']:>7} maxbias {z['max_abs_bias']:.4f} tc_gate {z['tc_gate']:2d} "
                      f"tokD0.5 {z['tok_D05']:2d} tokD1 {z['tok_D1']:2d} tokPoly {z['tok_Dpoly05']:2d} "
                      + (f"tokNC {z['tok_Dnc05']:2d} " if 'tok_Dnc05' in z else "")
                      + f"D_full {z['D_full']:.2f} dphi_full(A) {np.round(z['dphi_full'],4).tolist()} sd {np.round(z['crb_sd_full'],4).tolist()} "
                      f"gain_gate {np.round(z['gain_gate'],1).tolist()} gain_mse {np.round(z['gain_mse'],2).tolist()}")
        for key in ("S", "F", "Fnc"):
            print("  M*", key, o["Mstar_" + key])
    name = "estimator_bias_" + ("_".join(sorted({t.split('_N')[1].split('_')[0] for t in tags}))) + ".json"
    print("wrote", dump(res, "estimator_bias_N" + name.split("estimator_bias_")[1]))


if __name__ == "__main__":
    main()
