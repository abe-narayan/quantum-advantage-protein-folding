"""S6 (short-path / jump-to-the-end / generalised short path / super-quadratic key guessing): exponent comparison.

Every family here is still EXPONENTIAL; it is super-quadratic only relative to a specific classical baseline
(brute force / Grover, stationary-distribution search, or enumerate-by-likelihood).  It gives an advantage on the
protein task only if its per-residue exponent is below the per-residue exponent of the BEST MEASURED classical method.

Classical (MEASURED, G1 census, research/results/PROCESSED/g1_summary.json): per-restart p_hit(best-found mode);
cost per hit = (grad evals per restart) / p_hit ; fit ln(cost) = a + alpha_c * L.
Quantum exponents (per residue, nats), with the discrete encodings most favourable to quantum:
  * jump-to-end / short path (Dalzell et al. 2212.01513, Hastings 1802.10124): (1/2 - c) * ln K per residue for K
    states/residue; required c for parity with alpha_c is reported for K = 2 and K = 216 (9 x 24 head cells).
  * key guessing with a non-uniform prior (Montanaro; Glaser-May-Nowakowski 2509.06549): classical H_{1/2}(D),
    quantum H_{2/3}(D)/2, D = product of per-residue (theta,tau) head distributions (216 cells), Renyi in nats.
  * generalised short path over stationary-distribution search (Chakrabarti et al. 2410.23270): classical baseline
    1/pi(x_opt cell) under the restart prior; quantum at best ~ pi^{-1/2}; x_opt cell = cell of the DEP level-1
    relaxed minimum (S4).
"""
from __future__ import annotations

import json
import os

import numpy as np

from common import EN, HERE, ROOT, CHAINS, atomic_json, load_crop, make_energy, x_from_ca

OUT = os.path.join(HERE, "s6_exponents.json")
COORDS = os.path.join(HERE, "s4_coords.npz")


def renyi(p, a):
    p = p[p > 0]
    if abs(a - 1) < 1e-12:
        return float(-(p * np.log(p)).sum())
    return float(np.log((p ** a).sum()) / (1 - a))


def main():
    g1 = json.load(open(os.path.join(ROOT, "research", "results", "PROCESSED", "g1_summary.json"), encoding="utf-8"))
    rows = []
    for r in g1["census256"]:
        if r.get("p_hit") and r.get("grad_evals"):
            rows.append((r["L"], r["p_hit"], r["grad_evals"] / r["R"]))
    rows = np.array(rows, float)
    Ls = np.unique(rows[:, 0])
    gm = np.array([np.exp(np.mean(np.log(rows[rows[:, 0] == L, 1]))) for L in Ls])
    ev = np.array([np.mean(rows[rows[:, 0] == L, 2]) for L in Ls])
    cost = ev / gm
    A = np.stack([np.ones_like(Ls), Ls], 1)
    coef = np.linalg.lstsq(A, np.log(cost), rcond=None)[0]
    coef_p = np.linalg.lstsq(A, np.log(gm), rcond=None)[0]
    out = dict(classical=dict(L=Ls.tolist(), gmean_p_hit=gm.tolist(), grad_evals_per_restart=ev.tolist(),
                              cost_per_hit_grad_evals=cost.tolist(), fit_ln_cost=dict(a=float(coef[0]), alpha_c=float(coef[1])),
                              fit_ln_phit_slope=float(coef_p[1]),
                              note="p_hit censored at 1/256 at L=150 (gmean includes censored crops); alpha_c is for the best-FOUND mode"))
    alpha_c = float(coef[1])
    out["jump_to_end"] = {f"K={K}": dict(quantum_exponent_per_res_c0=0.5 * np.log(K),
                                          c_required_for_parity=float(0.5 - alpha_c / np.log(K)))
                          for K in (2, 4, 24, 216)}
    coords = np.load(COORDS)
    crops = []
    for L in (30, 60, 100, 150):
        for ch in CHAINS:
            crop = f"{ch}_{L}"
            z, L_ = load_crop(crop)
            en = make_energy(z, L_)
            PT = en.PT.numpy()                         # (L-3, 9, 24) head bin probabilities
            H = {a: 0.0 for a in (0.5, 2 / 3, 1.0, 2.0)}
            for r in range(L_ - 3):
                p = PT[r].ravel().astype(float); p = p / p.sum()
                for a in H:
                    H[a] += renyi(p, a)
            xs = x_from_ca(coords[crop])
            th = np.degrees(xs[:L_ - 2]); ta = np.degrees(xs[L_ - 2:])
            lnpi = 0.0
            for r in range(L_ - 3):
                p = PT[r].astype(float); p = p / p.sum()
                it = int(np.clip(np.searchsorted(EN.TH_LO[1:], th[r], side="right"), 0, 8))
                ia = int(np.argmin(np.abs(((ta[r] - EN.TA_C) + 180) % 360 - 180)))
                lnpi += np.log(max(p[it, ia], 1e-12))
            n = L_ - 3
            crops.append(dict(crop=crop, L=L_, H_half_per_res=H[0.5] / n, H_twothirds_per_res=H[2 / 3] / n,
                              H_shannon_per_res=H[1.0] / n, H_2_per_res=H[2.0] / n,
                              guess_classical_exp_per_res=H[0.5] / n, guess_quantum_exp_per_res=H[2 / 3] / (2 * n),
                              superquad_factor=2 * H[0.5] / H[2 / 3],
                              neg_ln_prior_cell_xstar_per_res=-lnpi / n,
                              stat_search_quantum_exp_per_res_best=-lnpi / (2 * n)))
    out["crops"] = crops
    agg = {k: [float(np.median([c[k] for c in crops])), float(np.min([c[k] for c in crops])),
               float(np.max([c[k] for c in crops]))]
           for k in ("guess_classical_exp_per_res", "guess_quantum_exp_per_res", "superquad_factor",
                     "neg_ln_prior_cell_xstar_per_res", "stat_search_quantum_exp_per_res_best")}
    out["summary_median_min_max"] = agg
    out["ratio_quantum_exp_to_alpha_c"] = dict(
        guessing=agg["guess_quantum_exp_per_res"][1] / alpha_c,
        stationary_search=agg["stat_search_quantum_exp_per_res_best"][1] / alpha_c,
        jump_to_end_K2_c0=0.5 * np.log(2) / alpha_c)
    atomic_json(OUT, out)
    print(json.dumps({k: out[k] for k in ("summary_median_min_max", "ratio_quantum_exp_to_alpha_c", "jump_to_end")}, indent=1, default=float))
    print("classical", json.dumps(out["classical"], default=float)[:900])


if __name__ == "__main__":
    main()
