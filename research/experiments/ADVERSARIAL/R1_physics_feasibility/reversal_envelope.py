"""R1 physics-feasibility audit, part 2: how much of the classically-hard echo Fisher information survives the
MEASURED irreversibility of many-body time reversal in dipolar solids?

Input: the gamma=0 RAW jobs with echo FI (research/results/RAW/nmr_gate, nmr_gate_hn) and scales.json (T2 per job).
Literature envelopes (verified this session from the arXiv full text of Sanchez, Chattah & Pastawski, PRA 105, 052232
(2022), arXiv:2112.00607):
  * ME-type Loschmidt echo (adamantane, 303 K): logistic M(t) = C/(1+exp[(t-T3)/l]), T3 = T2/0.15 = 6.7 T2 in the
    perturbation-independent (best achievable) limit, exponential tail 1/lambda = l = 1.7 T2 (= 0.25 T3).
  * polarization echo (local 13C->1H injection and read-back, the site-resolved protocol a protein experiment needs):
    "the LE decay remains Gaussian as long as the signal-to-noise ratio is significant ... an emergent T3 of about 4 T2".
  T2 := 1/sqrt(M2) with the Van Vleck M2 (their Eq. 2).
Model: the measured echo is A(t) * F(t) with a structure-independent reversal envelope A and fixed per-point noise
sigma, so the per-time-point FI is multiplied by A(t)^2 (echo normalisation by a reference LE rescales signal and noise
alike and does not change this).  Transfer S_ab needs no reversal and is left undamped: transfer data (classically
reproducible, f_hard = 0) are part of what a classical inversion can use, so they belong to the classical side of the
gain.
Time argument: 'generous' = A(t_forward) (reversal failure counted in forward proper time only);
               'literal'  = A(2 t_forward) (forward + backward proper time; a magic-echo backward leg at k_B = 1/2
                            takes 2t of lab time, i.e. 3t in total, so even 'literal' is generous in lab time).
T2 choices: cluster (the isolated-model T2, longest, most generous), network (whole-protein static 1H network),
            network_rotoravg (methyl/NH3 3-site jumps averaged; dense only).
Outputs: reversal_envelope.json.  Pure re-analysis, seconds of CPU.
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def env_logistic(x, c, lam_frac=0.25):
    """x = t/T2; T3 = c T2; tail l = lam_frac*T3; normalised to A(0) = 1."""
    T3 = c
    l = lam_frac * T3
    return (1 + math.exp(-T3 / l)) / (1 + np.exp((x - T3) / l))


def env_gauss(x, c):
    return np.exp(-math.log(2) * (x / c) ** 2)


ENVS = {
    "PE_gauss_T3=4T2": lambda x: env_gauss(x, 4.0),
    "LE_logistic_T3=6.7T2": lambda x: env_logistic(x, 1 / 0.15, 1.7 * 0.15),
    "hypothetical_logistic_T3=20T2": lambda x: env_logistic(x, 20.0),
    "hypothetical_logistic_T3=50T2": lambda x: env_logistic(x, 50.0),
}


def split(fio, fit, tc, A):
    w = A ** 2
    easy = float((w[:tc] * fio[:tc]).sum())
    hard = float((w[tc:] * fio[tc:]).sum())
    tr = float(fit.sum())
    return easy, hard, tr


def required_c(fio, fit, tc, x, target_gain, arg_scale=1.0):
    """smallest T3/T2 (logistic, tail 0.25 T3) for which (tr+easy+hard)/(tr+easy) >= target_gain."""
    def gain(c):
        A = env_logistic(arg_scale * x, c)
        e, h, tr = split(fio, fit, tc, A)
        return (tr + e + h) / max(tr + e, 1e-300)
    if gain(1e4) < target_gain:
        return None
    lo, hi = 0.5, 1e4
    for _ in range(80):
        mid = math.sqrt(lo * hi)
        if gain(mid) >= target_gain:
            hi = mid
        else:
            lo = mid
    return hi


def main():
    sc = {r["file"]: r for r in json.load(open(os.path.join(HERE, "scales.json")))["jobs"]}
    files = sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate", "*_N10_*_g0.json"))) + \
        sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate_hn", "*_g0.json")))
    out = []
    for f in files:
        fn = os.path.basename(f)
        if fn not in sc:
            continue
        d = json.load(open(f))
        s = sc[fn]
        t = np.array(d["times"])
        tc = int(d["best_t_c_otoc_index"])
        fio_p = [np.array(p["FI_otoc_t"]) for p in d["params"]]
        fit_p = [np.array(p["FI_t"]) for p in d["params"]]
        fio = np.sum(fio_p, axis=0)
        fit = np.sum(fit_p, axis=0)
        e0, h0, tr = split(fio, fit, tc, np.ones_like(t))
        rec = dict(file=fn, hn_only=s["hn_only"], probe=s["probe"], t_c_us=float(t[tc] * 1e6),
                   ideal=dict(FI_echo_easy=e0, FI_echo_hard=h0, FI_transfer=tr,
                              gain_vs_classical=(tr + e0 + h0) / (tr + e0),
                              hard_over_transfer=h0 / tr), cases={})
        T2s = {"cluster": s["T2_cluster_us"], "network": s["T2_network_static_us"]}
        if not s["hn_only"]:
            T2s["network_rotoravg"] = s["T2_network_rotoravg_us"]
        for T2name, T2 in T2s.items():
            x = t * 1e6 / T2
            for argname, sc_ in (("generous", 1.0), ("literal", 2.0)):
                for ename, ef in ENVS.items():
                    A = ef(sc_ * x)
                    e, h, _ = split(fio, fit, tc, A)
                    # per-parameter gains
                    gp = []
                    for fo, ft in zip(fio_p, fit_p):
                        ee, hh, trr = split(fo, ft, tc, A)
                        gp.append((trr + ee + hh) / max(trr + ee, 1e-300))
                    rec["cases"][f"{T2name}|{argname}|{ename}"] = dict(
                        A_at_tc=float(A[tc]), A_at_t50=float(ef(sc_ * s["t50_echo_us"] / T2)),
                        hard_retained=h / h0, FI_echo_hard=h, FI_echo_easy=e,
                        hard_over_transfer=h / tr, gain_vs_classical=(tr + e + h) / (tr + e),
                        gain_per_param=[float(g) for g in gp])
                for tg in (1.5, 2.0, 10.0):
                    rc = required_c(fio, fit, tc, x, tg, sc_)
                    rec["cases"].setdefault(f"{T2name}|{argname}|required", {})[f"T3_over_T2_for_gain_{tg}"] = rc
        out.append(rec)
        g = rec["cases"]
        print(fn, "tc=%.0fus" % rec["t_c_us"], "ideal gain %.1f hard/tr %.1f" % (rec["ideal"]["gain_vs_classical"],
                                                                             rec["ideal"]["hard_over_transfer"]))
        for T2name in T2s:
            for argname in ("generous", "literal"):
                row = [f"{T2name[:8]:8s} {argname[:4]}"]
                for ename in ENVS:
                    c = g[f"{T2name}|{argname}|{ename}"]
                    row.append(f"{ename.split('_')[0]}{ename.split('=')[1][:-2]}: ret={c['hard_retained']:.2e} "
                               f"gain={c['gain_vs_classical']:.3f}")
                req = g[f"{T2name}|{argname}|required"]
                row.append("req(g>=2)=%s" % (None if req["T3_over_T2_for_gain_2.0"] is None
                                             else round(req["T3_over_T2_for_gain_2.0"], 1)))
                print("   " + " | ".join(row))
    json.dump(out, open(os.path.join(HERE, "reversal_envelope.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
