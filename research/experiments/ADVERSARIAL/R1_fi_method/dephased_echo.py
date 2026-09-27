"""R1_fi_method / test DEPH: the echo branch was only ever evaluated at gamma = 0 (nmr_gate.py sets do_otoc only for
gamma == 0).  Here: echo F_ab(t) and the Loschmidt-normalised ratio R_ab = F_ab / L, L(t) = Tr[O(t)^2]/2^N, for the
dephased Heisenberg operator (same Pauli-diagonal dephasing channel as the C1 transfer runs and the R1-E proxy), with the
same cluster/parameters (1UBQ p19, N = 10, dense, orientation 0).  gamma in {1000, 5000, 20000} 1/s (R1-E's Gaussian-bath
proxy gave gamma_i ~ 2-14e4 1/s).  Classical adversary: sparse Pauli eps = 1e-3, 1e-4 run here (gamma = 1000 eps = 1e-4
and 3e-5 taken from the C2 file research/results/RAW/nmr_sparse/1UBQ_p19_N10_o0_g1000.json, which stores F and the kept norm).
The classical ratio estimator is F_c / N_kept (N_kept = sum of kept c^2 = the truncated model's L).
Noise: F with constant sigma; R with sd = (sigma / L) sqrt(1 + R^2) (both echo and Loschmidt echo measured with sigma).
Reported: FI (F, R) per parameter, classical failure times (gate criterion), f_hard, gain, joint gain with the (classically
exact at gamma > 0, C1) transfer data, echo/transfer FI ratio.
"""
from __future__ import annotations

import json
import math
import os
import time

import numpy as np

from fi_common import RAW, SP, dump, geom, setup

SIG = 0.01
H = 0.05
DT, STEPS, REC = 2e-6, 160, 10


def sector_SFL(dm, dt, n_steps, a, bs, gamma, record_every):
    """copy of the dephased branch of SP.sector_exact_correlators that also returns L(t) = Tr[O^2]/2^N."""
    N = len(dm); D = 1 << N
    times = list(range(0, n_steps + 1, record_every))
    S = {b: np.zeros(len(times)) for b in bs}; F = {b: np.zeros(len(times)) for b in bs}; L = np.zeros(len(times))
    za_full = SP.zsign(N, a); zb_full = {b: SP.zsign(N, b) for b in bs}
    for idx, Uk in SP.sector_step_unitaries(dm, dt):
        za = za_full[idx]
        xr = idx[:, None] ^ idx[None, :]
        pcb = SP._PC16[xr & 0xFFFF] + SP._PC16[(xr >> 16) & 0xFFFF]
        damp = np.exp(-2 * gamma * dt * pcb)
        O = np.diag(za.astype(complex)); Uh = Uk.conj().T
        ti = 0
        for n_ in range(n_steps + 1):
            if n_ % record_every == 0:
                dg = np.real(np.diag(O)); A2 = np.abs(O) ** 2
                L[ti] += float(A2.sum())
                for b in bs:
                    zb = zb_full[b][idx]
                    S[b][ti] += float((dg * zb).sum())
                    F[b][ti] += float((zb[:, None] * A2 * zb[None, :]).sum())
                ti += 1
            if n_ == n_steps:
                break
            O = (Uh @ O @ Uk) * damp
    return np.array(times) * dt, {b: v / D for b, v in S.items()}, {b: v / D for b, v in F.items()}, L / D


def main():
    cfg = setup("1UBQ", 19, 10, 0)
    bs = cfg["bs"]; nb = len(bs)
    res = dict(cluster="1UBQ_p19_N10_o0", sigma=SIG, h=H, gammas={})
    # validation of the local copy against the library at gamma = 1000
    dm0 = SP.couplings(cfg["X0"], cfg["b0"])
    _, S_l, F_l = SP.sector_exact_correlators(dm0, DT, STEPS, 0, bs, gamma=1000.0, record_every=REC, otoc=True)
    tt, S_c, F_c, L_c = sector_SFL(dm0, DT, STEPS, 0, bs, 1000.0, REC)
    res["validation_max_abs_diff"] = float(max(max(np.max(np.abs(S_l[b] - S_c[b])), np.max(np.abs(F_l[b] - F_c[b]))) for b in bs))
    print("validation", res["validation_max_abs_diff"])
    c2 = json.load(open(os.path.join(RAW, "nmr_sparse", "1UBQ_p19_N10_o0_g1000.json")))
    assert c2["bs"] == bs
    for gamma in (1000.0, 5000.0, 20000.0):
        t0 = time.time()
        dm = SP.couplings(cfg["X0"], cfg["b0"])
        tt, S0, F0, L0 = sector_SFL(dm, DT, STEPS, 0, bs, gamma, REC)
        R0 = {b: F0[b] / L0 for b in bs}
        nt = len(tt)
        par = {}
        for p in cfg["params"]:
            _, Sp, Fp, Lp = sector_SFL(SP.couplings(geom(cfg, p, +H), cfg["b0"]), DT, STEPS, 0, bs, gamma, REC)
            _, Sm, Fm, Lm = sector_SFL(SP.couplings(geom(cfg, p, -H), cfg["b0"]), DT, STEPS, 0, bs, gamma, REC)
            fS = sum(((Sp[b] - Sm[b]) / (2 * H)) ** 2 for b in bs) / SIG ** 2
            fF = sum(((Fp[b] - Fm[b]) / (2 * H)) ** 2 for b in bs) / SIG ** 2
            fR = sum((((Fp[b] / Lp) - (Fm[b] / Lm)) / (2 * H) / ((1 / L0) * np.sqrt(1 + R0[b] ** 2))) ** 2 for b in bs) / SIG ** 2
            par[p["name"]] = dict(FI_t_S=fS.tolist(), FI_t_F=fF.tolist(), FI_t_R=fR.tolist(),
                                  FI_S=float(fS.sum()), FI_F=float(fF.sum()), FI_R=float(fR.sum()))
        # adversaries
        adv = {}
        runs = []
        if gamma == 1000.0:
            for x in c2["runs"]:
                if x["eps"] in (1e-3, 1e-4, 3e-5):
                    runs.append((f"eps{x['eps']:g}(C2)", {b: np.asarray(x["F"][str(b)]) for b in bs},
                                 np.asarray(x["kept_norm2"]), {b: np.asarray(x["S"][str(b)]) for b in bs}))
        else:
            for eps in (1e-3, 1e-4):
                ts = time.time()
                _, Sw, Fw, _, n2 = SP.pauli_correlators(dm, DT, STEPS, 0, bs, eps=eps, gamma=gamma, record_every=REC)
                runs.append((f"eps{eps:g}", Fw, np.asarray(n2), Sw))
                print(f"   gamma {gamma:g} eps {eps:g} sparse {time.time()-ts:.1f}s", flush=True)
        for lab, Fw, n2, Sw in runs:
            n2 = np.maximum(n2, 1e-300)
            bF = np.max([np.abs(Fw[b] - F0[b]) for b in bs], 0)
            bR = np.max([np.abs(Fw[b] / n2 - R0[b]) / ((1 / L0) * np.sqrt(1 + R0[b] ** 2)) for b in bs], 0)   # in units of the ratio noise / sigma
            bS = np.max([np.abs(Sw[b] - S0[b]) for b in bs], 0)
            tcF = int(np.argmax(bF > SIG)) if (bF > SIG).any() else nt
            tcR = int(np.argmax(bR > SIG)) if (bR > SIG).any() else nt
            tcS = int(np.argmax(bS > SIG)) if (bS > SIG).any() else nt
            adv[lab] = dict(tcF=tcF, tcR=tcR, tcS=tcS, max_bias_F=float(bF.max()), max_bias_R_scaled=float(bR.max()),
                            max_bias_S=float(bS.max()))
        bestF = max(adv, key=lambda k: adv[k]["tcF"]); bestR = max(adv, key=lambda k: adv[k]["tcR"])
        tcF, tcR = adv[bestF]["tcF"], adv[bestR]["tcR"]
        summ = {}
        for n, z in par.items():
            fS, fF, fR = (np.asarray(z[k]) for k in ("FI_t_S", "FI_t_F", "FI_t_R"))
            summ[n] = dict(FI_S=z["FI_S"], FI_F=z["FI_F"], FI_R=z["FI_R"],
                           frac_hard_F=float(fF[tcF:].sum() / max(fF.sum(), 1e-300)), frac_hard_R=float(fR[tcR:].sum() / max(fR.sum(), 1e-300)),
                           gain_joint_F=float((fS.sum() + fF.sum()) / max(fS.sum() + fF[:tcF].sum(), 1e-300)),
                           gain_joint_R=float((fS.sum() + fR.sum()) / max(fS.sum() + fR[:tcR].sum(), 1e-300)))
        res["gammas"][str(int(gamma))] = dict(adversaries=adv, best_F=bestF, best_R=bestR, tcF=tcF, tcR=tcR, params=par, summary=summ,
                                             L=L0.tolist(), secs=time.time() - t0)
        print(f"gamma {gamma:g}: ({time.time()-t0:.0f}s) L(320us)={L0[-1]:.3f}  adversaries " +
              "; ".join(f"{k}: tcF {v['tcF']} tcR {v['tcR']} tcS {v['tcS']} maxbF {v['max_bias_F']:.4f}" for k, v in adv.items()))
        for n, s in summ.items():
            print(f"   {n:20s} FI_S {s['FI_S']:8.1f} FI_F {s['FI_F']:8.1f} FI_R {s['FI_R']:8.1f} f_hard F {s['frac_hard_F']:.3f} R {s['frac_hard_R']:.3f} "
                  f"joint gain F {s['gain_joint_F']:.2f} R {s['gain_joint_R']:.2f}", flush=True)
    print("wrote", dump(res, "dephased_echo.json"))


if __name__ == "__main__":
    main()
