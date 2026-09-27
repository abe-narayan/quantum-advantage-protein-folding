"""R1_fi_method / test FIT (requested improved statistic): the ACTUAL parameter-estimation error of a least-squares fit of a
truncated classical model to exact (noise-free) data, in Angstrom, vs the Cramer-Rao bound of the exact model.
Cluster: 1UBQ probe 19 (H/ILE3), N = 8, dense, orientation 0, gamma = 0, same parameters / observables / grid as the gate.
Classical models: sparse Pauli eps = 1e-3, 3e-4 (coefficient truncation) and weight-4 Pauli (one model per invocation).
Per parameter k (single-parameter fits, the others held at truth), on the echo F and the transfer S:
  * J_c = classical-model derivative (central differences, h = 0.05 A); J_e = exact derivative
  * one-step Gauss-Newton phi1 = -(J_c' r0)/(J_c' J_c), r0 = m_c(0) - m_e(0), then (echo) one secant step using m_c(phi1);
    phi_hat = the evaluated point with the smallest residual (nonlinear fit, full 0-320 us window)
  * linearised predictions with J_e and J_c for the full window and for the gate's easy window [0, t_c)
  * sd_exact(full) = sigma/||J_e||, sd_exact(easy), sd_classical(full) = sigma/||J_c||,
    RMSE_classical(full) = sqrt(phi_hat^2 + sd_c^2) vs the classical-easy-window RMSE and the exact-model CRB.
Usage: python n8_fit.py eps1e-3 | eps3e-4 | w4
"""
from __future__ import annotations

import sys
import time

import numpy as np

from fi_common import SP, dump, exact, geom, setup

SIG = 0.01
H = 0.05
DT, STEPS, REC = 2e-6, 160, 10


def main():
    lab = sys.argv[1]
    wmax, eps = (4, 1e-9) if lab == "w4" else (None, float(lab[3:]))
    cfg = setup("1UBQ", 19, 8, 0)
    bs = cfg["bs"]
    nruns = [0]

    def cls(X):
        nruns[0] += 1
        dm = SP.couplings(X, cfg["b0"])
        _, S, F, _, _ = SP.pauli_correlators(dm, DT, STEPS, 0, bs, wmax=wmax, eps=eps, record_every=REC)
        return np.concatenate([S[b] for b in bs]), np.concatenate([F[b] for b in bs])

    def ex(X):
        _, S, F = exact(cfg, X, dt=DT, steps=STEPS, rec=REC)
        return np.concatenate([S[b] for b in bs]), np.concatenate([F[b] for b in bs])

    t0 = time.time()
    Se0, Fe0 = ex(cfg["X0"])
    Sc0, Fc0 = cls(cfg["X0"])
    nt = STEPS // REC + 1
    out = dict(model=lab, cluster="1UBQ_p19_N8_o0_g0", sigma=SIG, h=H, params={})
    for key, me0, mc0 in (("S", Se0, Sc0), ("F", Fe0, Fc0)):
        bias = (mc0 - me0).reshape(len(bs), nt)
        bad = np.nonzero(np.max(np.abs(bias), 0) > SIG)[0]
        out[f"tc_gate_{key}"] = int(bad[0]) if len(bad) else nt
        out[f"max_abs_bias_{key}"] = float(np.max(np.abs(bias)))
    for p in cfg["params"]:
        Sep, Fep = ex(geom(cfg, p, +H)); Sem, Fem = ex(geom(cfg, p, -H))
        Scp, Fcp = cls(geom(cfg, p, +H)); Scm, Fcm = cls(geom(cfg, p, -H))
        rowp = {}
        for key, Je, Jc, me0, mc0 in (("S", (Sep - Sem) / (2 * H), (Scp - Scm) / (2 * H), Se0, Sc0),
                                       ("F", (Fep - Fem) / (2 * H), (Fcp - Fcm) / (2 * H), Fe0, Fc0)):
            r0 = mc0 - me0
            tc = out[f"tc_gate_{key}"]
            easy = np.tile(np.arange(nt) < tc, len(bs))

            def lin(J, m):
                n2 = float(J[m] @ J[m])
                return (float(-(J[m] @ r0[m]) / n2), float(SIG / np.sqrt(n2))) if n2 > 0 else (float("nan"), float("inf"))
            phiJe, sdE = lin(Je, np.ones_like(easy)); phiJc, sdC = lin(Jc, np.ones_like(easy))
            phiJe_easy, sdE_easy = lin(Je, easy) if tc > 0 else (0.0, float("inf"))
            phiJc_easy, sdC_easy = lin(Jc, easy) if tc > 0 else (0.0, float("inf"))
            z = dict(tc_gate=tc, sd_exact_full=sdE, sd_exact_easy=sdE_easy, sd_classical_full=sdC, sd_classical_easy=sdC_easy,
                     phi_lin_Je_full=phiJe, phi_lin_Jc_full=phiJc, phi_lin_Je_easy=phiJe_easy, phi_lin_Jc_easy=phiJc_easy,
                     rel_deriv_err_full=float(np.linalg.norm(Jc - Je) / max(np.linalg.norm(Je), 1e-30)),
                     cos_Jc_Je=float(Jc @ Je / max(np.linalg.norm(Jc) * np.linalg.norm(Je), 1e-30)))
            if key == "F":                     # nonlinear fit on the full window (GN + secant)
                pts = [(0.0, float(r0 @ r0))]
                d1 = phiJc
                S1, F1 = cls(geom(cfg, p, d1)); r1 = F1 - Fe0
                pts.append((d1, float(r1 @ r1)))
                Js = (F1 - Fc0) / d1 if abs(d1) > 1e-9 else Jc
                d2 = d1 - float(Js @ r1) / max(float(Js @ Js), 1e-30)
                S2, F2 = cls(geom(cfg, p, d2)); r2 = F2 - Fe0
                pts.append((d2, float(r2 @ r2)))
                best = min(pts, key=lambda q: q[1])
                z.update(fit_points=pts, phi_hat_fit=best[0], chi2_min=best[1] / SIG ** 2, n_data=len(r0))
                ph = best[0]
            else:
                ph = phiJc
            z["phi_hat"] = ph
            z["bias_over_sd_exact_full"] = abs(ph) / sdE
            z["rmse_classical_full"] = float(np.hypot(ph, sdC))
            z["rmse_classical_easy"] = float(np.hypot(phiJc_easy, sdC_easy))
            z["rmse_classical_best"] = min(z["rmse_classical_full"], z["rmse_classical_easy"])
            z["gain_rmse"] = (z["rmse_classical_best"] / sdE) ** 2      # repetitions factor vs exact model (exact CRB)
            z["gain_gate"] = (sdE_easy / sdE) ** 2
            rowp[key] = z
        out["params"][p["name"]] = rowp
        for key in ("S", "F"):
            z = rowp[key]
            print(f"{lab:7s} {p['name']:18s} {key} tc_gate {z['tc_gate']:2d} phi_hat {z['phi_hat']:+.4f} A (linJe {z['phi_lin_Je_full']:+.4f}, "
                  f"linJc {z['phi_lin_Jc_full']:+.4f}) sd_exact {z['sd_exact_full']:.4f} |bias|/sd {z['bias_over_sd_exact_full']:6.1f} "
                  f"RMSE_c full {z['rmse_classical_full']:.4f} easy {z['rmse_classical_easy']:.4f}  gain_rmse {z['gain_rmse']:.2f} "
                  f"gain_gate {z['gain_gate']:.2f} relJerr {z['rel_deriv_err_full']:.2f}", flush=True)
    out["secs"] = time.time() - t0
    out["classical_runs"] = nruns[0]
    print("secs", round(out["secs"], 1), "classical runs", nruns[0])
    dump(out, f"n8_fit_{lab}.json")


if __name__ == "__main__":
    main()
