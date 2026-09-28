"""Multi-seed ladder at 40 us: does F track GENUINE H drift, or only fail to track the floor?  (file reads only)
Inputs: noise.json (4 honly + 3 echo seeds, R = 1, at N = 14..20), lane runs (N = 20 R = 2, N = 22), ROUND3 VC honly
(single estimates), reference cone F (full-space single vector).  Output: tracking.json."""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
RUNS = os.path.join(LANE, "runs")
EXP = os.path.abspath(os.path.join(LANE, "..", ".."))
TC = os.path.join(EXP, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
VC = os.path.join(EXP, "ROUND3", "r1sim_exact_reach", "verify_classical", "runs")
SITES = ["1", "7", "8", "9"]


def J(p):
    with open(p) as f:
        return json.load(f)


NZ = J(os.path.join(HERE, "noise.json"))
out = {}
for p in (19, 245):
    nz = NZ["per_probe"][f"p{p}"]
    e22 = J(os.path.join(RUNS, f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    h22 = J(os.path.join(RUNS, f"1UBQ_p{p}_N22_honly_R1_complex64_s4242_t20-40-60.json"))
    e20 = J(os.path.join(RUNS, f"1UBQ_p{p}_N20_echo_R2_complex64_s4242_t20-40-60.json"))
    ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json")) for N in (14, 16, 18)}
    H, seH, VCH, F, seF = {}, {}, {}, {}, {}
    for N in (14, 16, 18, 20):
        vch = J(glob.glob(os.path.join(VC, f"1UBQ_p{p}_N{N}_probe_honly_*.json"))[0])["H"][0]
        VCH[N] = vch
        hs = list(nz[f"N{N}"]["H"])
        # R = 1 Sigma_j G_j^2 is biased up by Sigma_j var(G_j) = N s^2.  Empirical s from the seed spread:
        # sd(H) ~ 2 s sqrt(H)  ->  bias ~ N sd(H)^2 / (4 H)   (<= 2e-4 here; the naive 2N/2^N over-corrects)
        bias = N * np.std(hs, ddof=1) ** 2 / (4 * np.mean(hs))
        H[N] = float(np.mean(hs) - bias)
        seH[N] = float(np.std(hs, ddof=1) / math.sqrt(len(hs)))
    H[22] = float(0.5 * (h22["H"][0] + e22["H"][0]))
    seH[22] = 0.0009                     # R = 1 at N = 22: sd scaled from N = 20 (0.0005-0.0009) x 2^-1; conservative
    for b in SITES:
        F[b] = {}
        for N in (16, 18):
            fs = nz[f"N{N}"]["F"][b]
            F[b][N] = float(np.mean(fs))
        F[b][14] = ref[14]["F"][b][1]
        F[b][20] = e20["F"][b][0]
        F[b][22] = e22["F"][b][0]
    fl = {N: nz[f"N{N}"]["floor_mean"] for N in (14, 16, 18, 20)}
    fl[22] = h22["floor"][0]
    rows = {}
    for (Na, Nb) in ((16, 22), (18, 22), (14, 22)):
        dH = H[Nb] - H[Na]
        sedH = math.hypot(seH[Na], seH[Nb])
        dfl = fl[Nb] - fl[Na]
        dF = {b: F[b][Nb] - F[b][Na] for b in SITES}
        rows[f"{Na}->{Nb}"] = dict(dH=dH, se_dH=sedH, dH_significance=abs(dH) / sedH, dfloor=dfl,
                                   dF=dF, dF_over_dH={b: (dF[b] / dH if abs(dH) > 2 * sedH else None) for b in SITES},
                                   hybrid_predicted_dF=dH + dfl)
    out[f"p{p}"] = dict(H_multiseed=H, se_H=seH, H_VC_single=VCH, VC_minus_multiseed={N: VCH[N] - H[N] for N in VCH},
                        floor=fl, F_multiseed=F, steps=rows)

# far-spin drift estimates at 40 us from CSD (lane CRN D) and the non-CRN VC ladder incl. Nc = 160
csd = {}
for p in (19, 245):
    lad = {}
    for f in glob.glob(os.path.join(VC, f"csd_1UBQ_p{p}_Nc*_M*_h1.0.json")):
        d = J(f)
        lad[d["Nc"]] = (d["H_unbiased"][1], d["H_se_est"][1])
    csd[f"p{p}"] = {str(k): v for k, v in sorted(lad.items())}
out["csd_VC_ladder_40us"] = csd
S = J(os.path.join(LANE, "tx_early_summary.json"))
out["lane_D_80_22"] = {f"p{p}": (S["per_probe"][f"p{p}"]["D_80_22_crn"][0], S["per_probe"][f"p{p}"]["se_D"][0]) for p in (19, 245)}
tmp = os.path.join(HERE, "tracking.json.tmp")
with open(tmp, "w") as f:
    json.dump(out, f, indent=1)
os.replace(tmp, os.path.join(HERE, "tracking.json"))
for p in (19, 245):
    o = out[f"p{p}"]
    print(f"p{p}: H multiseed {{{', '.join(f'{N}: {o['H_multiseed'][N]:.4f}+-{o['se_H'][N]:.4f}' for N in o['H_multiseed'])}}}")
    print(f"      VC single - multiseed {{{', '.join(f'{N}: {v:+.4f}' for N, v in o['VC_minus_multiseed'].items())}}}")
    for k, r in o["steps"].items():
        print(f"   {k}: dH {r['dH']:+.4f}+-{r['se_dH']:.4f} ({r['dH_significance']:.1f} se) dfloor {r['dfloor']:+.4f} "
              f"hybrid-pred dF {r['hybrid_predicted_dF']:+.4f} | dF {[round(v, 4) for v in r['dF'].values()]}")
print("CSD VC ladder 40us:", {p: {k: (round(v[0], 4), round(v[1], 4)) for k, v in d.items()} for p, d in csd.items()})
print("lane D_80_22:", out["lane_D_80_22"])

# ---- explicit F_inf (H-2): weighted 1/N fit over N = 16..22 using multi-seed F (sector-folded estimator) ----
fin = {}
for p in (19, 245):
    o = out[f"p{p}"]
    nz = NZ["per_probe"][f"p{p}"]
    Ns = np.array([16, 18, 20, 22], float)
    for b in SITES:
        Fv = np.array([o["F_multiseed"][b][int(N)] for N in Ns])
        sd16 = max(nz["N16"]["sd_F_R1"][b], 5e-4) / math.sqrt(3)
        sd18 = max(nz["N18"]["sd_F_R1"][b], 3e-4) / math.sqrt(3)
        sd = np.array([sd16, sd18, 7e-4, 5e-4])
        A = np.vstack([np.ones(4), 1 / Ns]).T
        W = np.diag(1 / sd ** 2)
        cov = np.linalg.inv(A.T @ W @ A)
        c = cov @ A.T @ W @ Fv
        r = (A @ c - Fv) / sd
        fin[f"p{p}_b{b}"] = dict(Finf=float(c[0]), se=float(math.sqrt(cov[0, 0])), Finf_minus_F22=float(c[0] - Fv[-1]),
                                 chi2_dof2=float(r @ r), F16_22=Fv.tolist())
out["Finf_invN_multiseed"] = fin
with open(tmp, "w") as f:
    json.dump(out, f, indent=1)
os.replace(tmp, os.path.join(HERE, "tracking.json"))
print("F_inf (1/N, weighted, N = 16..22, multi-seed F):")
for k, v in fin.items():
    print(f"   {k}: F16-22 {[round(x, 4) for x in v['F16_22']]} Finf {v['Finf']:.4f}+-{v['se']:.4f} "
          f"Finf-F22 {v['Finf_minus_F22']:+.4f} chi2/2dof {v['chi2_dof2']:.1f}")
