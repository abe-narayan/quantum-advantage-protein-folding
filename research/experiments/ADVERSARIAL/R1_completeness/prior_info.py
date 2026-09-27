"""R1_completeness: reconcile the value lens (CRB 0.014-0.03 A, other coordinates KNOWN) with the fi_method nuisance result
(marginal sd 1.2-1.5 A, other coordinates FREE, flat prior).  Real structure work sits in between: every coordinate is unknown
but constrained by a prior (X-ray / AlphaFold / NOE level).  Uses the stored exact Jacobians of R1_fi_method/nuisance.py
(1UBQ p19, N=10, o0, gamma=0; 27 coordinates of the 9 non-probe protons + coupling scale s).  Bayesian (Gaussian, linearised):
posterior precision P = J'J/sigma^2 + prior.  Reports per-proton radial posterior sd and the expected information gain (bits)
of the hard echo window (t >= t_c = 80 us) over transfer(all) + echo(easy), with and without reversal attenuation A(t).
"""
import json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
z = np.load(os.path.join(HERE, "..", "R1_fi_method", "nuisance_jacobians.npz"))
JxS, JxF, sS, sF, X0, bs, times = z["JxS"], z["JxF"], z["sS"], z["sF"], z["X0"], z["bs"], z["times"]
SIG = 0.01; nb = len(bs); nt = len(times); tcF = 4
tus = np.tile(times * 1e6, nb)
easy = tus < tcF * 20 - 1e-9
N = X0.shape[0]
rad = []
for i in range(1, N):
    u = X0[i] - X0[0]; r = np.linalg.norm(u); v = np.zeros(3 * (N - 1)); v[3 * (i - 1):3 * i] = u / r; rad.append((i, r, v))
out = {"note": __doc__, "cases": []}
for att_name, T3 in (("none", None), ("T3=130us", 130.0), ("T3=85us", 85.0)):
    A = np.ones_like(tus) if T3 is None else np.exp(-tus / T3)
    JF = JxF * A[:, None]; sFa = sF * A
    for sp in (0.2, 0.5, 1.0):
        for s_prior in (0.05,):
            Pprior = np.diag(np.r_[np.full(27, 1 / sp ** 2), 1 / s_prior ** 2])
            def post(rowsS, rowsF):
                JS_ = np.column_stack([JxS, sS])[rowsS] if rowsS is not None else np.zeros((0, 28))
                JF_ = np.column_stack([JF, sFa])[rowsF] if rowsF is not None else np.zeros((0, 28))
                Jall = np.vstack([JS_, JF_])
                P = Jall.T @ Jall / SIG ** 2 + Pprior
                C = np.linalg.inv(P)
                eig = 0.5 * np.linalg.slogdet(np.eye(28) + (Jall.T @ Jall / SIG ** 2) @ np.linalg.inv(Pprior))[1] / np.log(2)
                sds = [float(np.sqrt(np.r_[v, 0] @ C @ np.r_[v, 0])) for (_, _, v) in rad]
                return C, eig, sds
            allS = np.ones(len(tus), bool)
            _, e_S, sd_S = post(allS, None)
            _, e_easy, sd_easy = post(allS, easy)
            _, e_all, sd_all = post(allS, allS)
            gains = [ (a / b) ** 2 for a, b in zip(sd_easy, sd_all)]
            case = dict(attenuation=att_name, prior_sd_A=sp, s_prior=s_prior,
                        EIG_bits_S=e_S, EIG_bits_S_Feasy=e_easy, EIG_bits_all=e_all, hard_window_bits=e_all - e_easy,
                        radial_sd_S=sd_S, radial_sd_S_Feasy=sd_easy, radial_sd_all=sd_all, var_gain_hard=gains,
                        r_A=[r for (_, r, _) in rad])
            out["cases"].append(case)
            print(f"{att_name:9s} prior {sp:.1f} A | EIG bits S {e_S:6.1f}  S+Feasy {e_easy:6.1f}  all {e_all:6.1f}  (hard +{e_all - e_easy:5.1f}) | "
                  f"radial sd (A) easy->all median {np.median(sd_easy):.3f}->{np.median(sd_all):.3f}  var-gain median {np.median(gains):.2f} max {max(gains):.2f}")
json.dump(out, open(os.path.join(HERE, "out", "prior_info.json"), "w"), indent=1)
