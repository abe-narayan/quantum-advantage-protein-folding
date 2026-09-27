"""R1 theory_hardness, step C: operator-front (first-passage / SI 'operator epidemic') model of the light cone of Z_a(t),
calibrated on the EXACT per-site support p_j(t) of 12-spin clusters (front/*.json from exact_front.py), checked against
an early-time anchor, and then run on the FULL protein proton network (629 H for 1UBQ, 419 H for 1PGA; same field
direction b0 as the instrument) and on the amide-only (perdeuterated) network.

Model (INFERENCE; a coarse-grained operator-spreading picture):
  spin j joins the support at T_j = min_i (T_i + E_ij), T_a = 0, independent edge times E_ij with
  P(E_ij <= t) = 1 - exp(-(Gamma_ij t)^k)   (k = 1: stochastic SI epidemic; k = 2: quadratic onset, the short-time
  perturbative law p ~ (d t)^2).   Rate laws:
     'golden'   Gamma_ij = kappa * d_ij^2 / wbar       (wbar = 2 pi * 10 kHz, fixed)
     'coherent' Gamma_ij = kappa * |d_ij|
  Target p_j(t) ~= PSAT * P(T_j <= t), PSAT = 0.75 (random-operator saturation of Pr(P_j != I)).
  kappa fitted on the three dense N = 12 clusters (sites j != a, t <= 100 us, same finite cluster in the model).

Validation:
  (V1) RMSE of p_j(t) on N = 12 (fit window, and t > 100 us) and on N = 10 (out of sample).
  (V2) EARLY-TIME ANCHOR: the model's expected operator size in the FULL protein at 20/40 us must not exceed the exact
       N = 12 size plus 3x the exact N = 10 -> 12 increment (the exact size is nearly N-converged there).
  (V3) cross-network transfer: kappa from dense clusters predicts the amide-only N = 12 cluster (different time scale).
Outputs: front_model.json.   Cost: single-threaded, ~1-2 min.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.sparse.csgraph import dijkstra

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

WBAR = 2 * math.pi * 1.0e4
PSAT = 0.75
LAWS = [("golden", 1), ("coherent", 1), ("golden", 2), ("coherent", 2)]


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def rates(dm, law, kappa):
    G = kappa * dm ** 2 / WBAR if law == "golden" else kappa * np.abs(dm)
    np.fill_diagonal(G, 0.0)
    return G


def fpp_times(G, src, n_samp, rng, k):
    """first-passage times (seconds) from src; edge time E_ij = Exp(1)^(1/k) / Gamma_ij."""
    n = len(G)
    out = np.empty((n_samp, n))
    with np.errstate(divide="ignore"):
        inv = np.where(G > 0, 1.0 / G, np.inf)
    for s in range(n_samp):
        E = rng.exponential(1.0, size=(n, n)) ** (1.0 / k)
        W = E * inv
        W[~np.isfinite(W)] = 0.0                    # csgraph: 0 = no edge
        out[s] = dijkstra(W, directed=True, indices=src)
    return out


def load_front(tag):
    return json.load(open(os.path.join(HERE, "front", tag + ".json")))


def coords(pdb, hn_only=False):
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    if hn_only:
        keep = [i for i, n in enumerate(names) if n.startswith("H/")]
        return [names[i] for i in keep], xyz[keep], keep
    return names, xyz, list(range(len(names)))


def cluster_dm(fr):
    _, xyz, _ = coords(fr["pdb"], fr.get("hn_only", 0))
    return SP.couplings(xyz[fr["cluster"]], np.array(fr["b0"]))


def model_P(T_us, t_us):
    return (T_us[:, None, :] <= t_us[None, :, None]).mean(0)          # (nt, n)


def main():
    dense = ["1UBQ_p19", "1UBQ_p245", "1PGA_p325"]
    res = dict(model="first-passage operator front on the dipolar network", psat=PSAT, wbar_rad_s=WBAR, laws={})
    n_fit = 300
    for law, k in LAWS:
        key = f"{law}_k{k}"
        data = []
        for tag in dense:
            fr = load_front(f"{tag}_N12_o0")
            T1 = fpp_times(rates(cluster_dm(fr), law, 1.0), 0, n_fit, np.random.default_rng(1), k)
            data.append((T1, np.array(fr["times_us"]), np.array(fr["support_p"])))

        def f(lk):
            kap = math.exp(lk)
            s = 0.0
            for (T1, t, p) in data:
                m = t <= 100.0
                P = model_P(T1 / kap * 1e6, t[m])[:, 1:]
                s += float(((PSAT * P - p[m][:, 1:]) ** 2).sum())
            return s
        opt = minimize_scalar(f, bounds=(math.log(1e-4), math.log(1e6)), method="bounded")
        kappa = math.exp(opt.x)
        # ---- V1 validation on the finite clusters
        val = {}
        for tag in dense + ["1UBQHN_p19"]:
            for N in (10, 12):
                fr = load_front(f"{tag}_N{N}_o0")
                T = fpp_times(rates(cluster_dm(fr), law, kappa), 0, n_fit, np.random.default_rng(2), k) * 1e6
                t = np.array(fr["times_us"]); p = np.array(fr["support_p"])
                P = PSAT * model_P(T, t)[:, 1:]
                e = P - p[:, 1:]
                tsplit = 100.0 if "HN" not in tag else 500.0
                val[f"{tag}_N{N}"] = dict(rmse_early=float(np.sqrt((e[t <= tsplit] ** 2).mean())),
                                          rmse_late=float(np.sqrt((e[t > tsplit] ** 2).mean())),
                                          tsplit_us=tsplit, times_us=[round(x, 1) for x in t.tolist()],
                                          size_exact=[round(x, 3) for x in fr["size"]],
                                          size_model=[round(1 + x, 3) for x in P.sum(1).tolist()])
        # ---- full-network predictions
        pred = {}
        tq = np.array([20, 30, 40, 60, 80, 120, 160, 240, 320, 480, 640, 1000.0])
        for pdb, probes, hn in (("1UBQ", (19, 245), 0), ("1PGA", (325, 390), 0), ("1UBQ", (19,), 1)):
            names, xyz, keep = coords(pdb, hn)
            dmf = SP.couplings(xyz, random_b0(1000))
            for pr in probes:
                src = keep.index(pr) if hn else pr
                T = fpp_times(rates(dmf, law, kappa), src, 120, np.random.default_rng(7), k) * 1e6
                inf = T[:, None, :] <= tq[None, :, None]
                size = inf.sum(2)
                P = inf.mean(0)
                r = np.linalg.norm(xyz - xyz[src], axis=1)
                pred[f"{pdb}{'HN' if hn else ''}_p{pr}"] = dict(
                    n_sites=int(len(xyz)), times_us=tq.tolist(),
                    N_cone_mean=size.mean(0).tolist(),
                    N_cone_p10=np.percentile(size, 10, axis=0).tolist(),
                    N_cone_p90=np.percentile(size, 90, axis=0).tolist(),
                    N_sites_P_ge_0p5=(P >= 0.5).sum(1).tolist(),
                    N_sites_P_ge={str(th): (P >= th).sum(1).tolist() for th in (0.2, 0.1, 0.05, 0.02, 0.01)},
                    radius_P_ge_0p5_A=[float(np.max(r[P[i] >= 0.5])) for i in range(len(tq))],
                    expected_operator_size=(PSAT * P.sum(1) + (1 - PSAT)).tolist())
        # ---- V2 early-time anchor (dense)
        anchor = {}
        for tag in ("1UBQ_p19", "1UBQ_p245", "1PGA_p325"):
            f12, f10 = load_front(f"{tag}_N12_o0"), load_front(f"{tag}_N10_o0")
            t12 = np.array(f12["times_us"])
            pk = f"{tag}"
            if pk not in pred:
                continue
            for tt in (20.0, 40.0):
                i = int(np.argmin(abs(t12 - tt)))
                exact12 = f12["size"][i]; inc = f12["size"][i] - f10["size"][i]
                model = float(np.interp(tt, tq, pred[pk]["expected_operator_size"]))
                anchor[f"{tag}_{int(tt)}us"] = dict(exact_N12=exact12, incr_N10_to_N12=inc,
                                                     ceiling=exact12 + 3 * max(inc, 0.05), model_full=model,
                                                     passes=bool(model <= exact12 + 3 * max(inc, 0.05)))
        res["laws"][key] = dict(law=law, k=k, kappa=kappa, fit_sse=float(opt.fun), validation=val,
                                anchor=anchor, anchor_pass=all(v["passes"] for v in anchor.values()),
                                prediction=pred)
        print(key, "kappa=%.4g sse=%.3f anchor_pass=%s" % (kappa, opt.fun, res["laws"][key]["anchor_pass"]))
        for kk, v in val.items():
            print("   V1", kk, "rmse_early %.3f late %.3f" % (v["rmse_early"], v["rmse_late"]))
        for kk, v in anchor.items():
            print("   V2", kk, "exact12 %.2f ceiling %.2f model %.2f" % (v["exact_N12"], v["ceiling"], v["model_full"]))
        for kk, v in pred.items():
            print("   pred", kk, "N_cone_mean", [round(x, 1) for x in v["N_cone_mean"]])
            print("        size", [round(x, 1) for x in v["expected_operator_size"]], "r50", [round(x, 1) for x in v["radius_P_ge_0p5_A"]])
    json.dump(res, open(os.path.join(HERE, "front_model.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
