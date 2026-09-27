"""R1 amplify: re-analysis (seconds of CPU; no new dynamics).
 A. Depth-normalised comparison of F1 (2 evolution segments) and F2 (4 segments): hard FI available within a total
    evolution budget T_evo (F1 points need 2t <= T_evo, F2 points 4t <= T_evo).
 B. Truncation-bias mechanism: bias(F1) vs lost norm delta and bias(F2) vs sqrt(delta) (log-log slopes).
 C. Dilution scale law: t_c and t_50 of the C1 RAW echo jobs in units of the probe's local dipolar time 1/omega_loc
    (dense vs amide-only), and the absolute radius R_47 at which a labelled network holds N_ex = 47 spins around a
    buried probe, per labelling scheme, with the physical time stretch lambda^3 relative to dense 1H.
 D. Time-point design: hard FI per unit quantum evolution cost; how much of it the best k time points carry.
Writes analysis.json."""
from __future__ import annotations

import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import amp_lib as L  # noqa: E402

OUT = {}
N_EX = 47


# ------------------------------------------------------------------------------------------------ A
def depth_budget(fn):
    r = json.load(open(os.path.join(HERE, "out", fn)))
    t = np.asarray(r["times_us"])
    res = {}
    seg = dict(F1=2, F2=4, F1_multi=2)
    for T in (80, 120, 160, 200, 240, 320, 480, 640):
        row = {}
        for k, s in seg.items():
            if k not in r["families"]:
                continue
            v = r["families"][k]
            fi_t = np.asarray(v["FI_t"])
            tc = v["best_t_c_index"]
            ok = s * t <= T + 1e-9
            hard = ok & (np.arange(len(t)) >= tc)
            row[k] = dict(FI_all=float(fi_t[ok].sum()), FI_hard=float(fi_t[hard].sum()), n_points=int(ok.sum()),
                          n_hard=int(hard.sum()))
        res[str(T)] = row
    return dict(file=fn, t_c={k: r["families"][k]["best_t_c_index"] for k in seg if k in r["families"]},
                t_c_adv={k: r["families"][k]["best_adversary"] for k in seg if k in r["families"]}, budget=res)


OUT["A_depth_budget"] = [depth_budget(f) for f in ("obs_1UBQ_p19_N10_o0_secular.json",
                                                   "obs_1UBQ_p19_N10_o0_secular_fine.json",
                                                   "obs_1PGA_p325_N10_o0_secular_fine.json")]


# ------------------------------------------------------------------------------------------------ B
def mech(fn):
    r = json.load(open(os.path.join(HERE, "out", fn)))
    rows = {}
    for key, meta in r["adv_meta"].items():
        delta = 1 - np.asarray(meta["norm2"])
        n = len(delta)
        b1 = np.asarray(r["families"]["F1"]["t_c"][key + "_plain"]["max_bias"])[:n]
        b2 = np.asarray(r["families"]["F2"]["t_c"][key + "_plain"]["max_bias"])[:n]
        m = (delta > 1e-7) & (b1 > 1e-7) & (b2 > 1e-7)
        s1 = np.polyfit(np.log(delta[m]), np.log(b1[m]), 1)[0] if m.sum() >= 3 else None
        s2 = np.polyfit(np.log(delta[m]), np.log(b2[m]), 1)[0] if m.sum() >= 3 else None
        rows[key] = dict(delta=delta, bias_F1=b1, bias_F2=b2, slope_logF1_vs_logdelta=s1, slope_logF2_vs_logdelta=s2,
                         ratio_F1_over_delta=(b1[m] / delta[m]).tolist(),
                         ratio_F2_over_sqrtdelta=(b2[m] / np.sqrt(delta[m])).tolist())
    return dict(file=fn, adversaries=rows)


OUT["B_mechanism"] = [mech("obs_1UBQ_p19_N10_o0_secular_fine.json"), mech("obs_1PGA_p325_N10_o0_secular_fine.json"),
                     mech("obs_1UBQ_p19_N10_o0_secular_eps3e-5.json")]


# ------------------------------------------------------------------------------------------------ C
def c1_dimensionless():
    rows = []
    for d, hn in (("nmr_gate", 0), ("nmr_gate_hn", 1)):
        for f in sorted(glob.glob(os.path.join(L.ROOT, "research", "results", "RAW", d, "*.json"))):
            r = json.load(open(f))
            if r.get("version") != 2 or r["gamma"] != 0 or r["N"] != 10 or not r.get("F_exact"):
                continue
            pdb = r["pdb"]
            probe_full = int(os.path.basename(f).split("_p")[1].split("_")[0])
            g = L.job_geometry(pdb, probe_full, r["N"], r["orient"], hn_only=bool(hn))
            dm = L.SP.couplings(g["X0"], g["b0"])
            w_loc = math.sqrt(0.5 * (dm[0] ** 2).sum())                    # probe M2_loc(Z) = (1/2) sum d_aj^2
            w_cl = math.sqrt((dm[np.triu_indices(len(dm), 1)] ** 2).mean()) # rms pair coupling in the cluster
            tt = np.asarray(r["times"])
            tco = r.get("best_t_c_otoc_index")
            fo = np.sum([np.asarray(p["FI_otoc_t"]) for p in r["params"]], axis=0)
            c = np.cumsum(fo) / fo.sum()
            t50 = float(tt[np.searchsorted(c, 0.5)])
            rows.append(dict(file=os.path.basename(f), network="amide" if hn else "dense",
                             omega_loc_krad_s=w_loc / 1e3, omega_rms_krad_s=w_cl / 1e3,
                             t_c_echo_us=(float(tt[tco]) * 1e6 if tco is not None and tco < len(tt) else None),
                             t50_echo_us=t50 * 1e6,
                             t_c_x_omega=(float(tt[tco]) * w_loc if tco is not None and tco < len(tt) else None),
                             t50_x_omega=t50 * w_loc,
                             t_c_x_omega_rms=(float(tt[tco]) * w_cl if tco is not None and tco < len(tt) else None)))
    summ = {}
    for net in ("dense", "amide"):
        xs = [x for x in rows if x["network"] == net]
        summ[net] = {k: (float(np.median([x[k] for x in xs if x[k] is not None])),
                         float(np.min([x[k] for x in xs if x[k] is not None])),
                         float(np.max([x[k] for x in xs if x[k] is not None])))
                     for k in ("t_c_echo_us", "t50_echo_us", "t_c_x_omega", "t50_x_omega", "t_c_x_omega_rms",
                               "omega_loc_krad_s")}
    return dict(rows=rows, median_min_max=summ)


def read_atoms(pdb):
    out = []
    with open(os.path.join(L.ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb")) as f:
        for line in f:
            if line.startswith("ENDMDL"):
                break
            if line.startswith(("ATOM", "HETATM")):
                out.append((line[12:16].strip(), line[17:20].strip(), int(line[22:26]),
                            np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])])))
    return out


def label_schemes(pdb):
    at = read_atoms(pdb)
    H = [(n, rn, ri, x) for (n, rn, ri, x) in at if (n[0] == "H" or (n[0].isdigit() and n[1] == "H"))]
    allx = np.array([x for (_, _, _, x) in at])
    nres = len({ri for (_, _, ri, _) in at})
    mass = 110.0 * nres                                                 # Da (INFERENCE: 110 Da / residue)
    V = mass * 0.73 / 0.6022                                            # A^3 (partial specific volume 0.73 cm^3/g)
    schemes = {}
    schemes["dense_1H"] = np.array([x for (_, _, _, x) in H])
    schemes["amide_HN"] = np.array([x for (n, _, _, x) in H if n == "H"])
    # ILV methyl pseudo-spins: centroid of the 3 methyl protons (Ile HD1*, Leu HD1*/HD2*, Val HG1*/HG2*)
    groups = {}
    for (n, rn, ri, x) in H:
        key = None
        if rn == "ILE" and n.startswith("HD1"):
            key = (ri, "D1")
        elif rn == "LEU" and n[:3] in ("HD1", "HD2"):
            key = (ri, n[:3])
        elif rn == "VAL" and n[:3] in ("HG1", "HG2"):
            key = (ri, n[:3])
        if key:
            groups.setdefault(key, []).append(x)
    schemes["ILV_methyl"] = np.array([np.mean(v, axis=0) for v in groups.values() if len(v) == 3])
    # sparse: one amide H per ~10 residues (synthetic site-specific label set)
    schemes["sparse_1per10res"] = np.array([x for (n, _, ri, x) in H if n == "H" and ri % 10 == 0])
    hull_c = allx.mean(0)
    out = {}
    for name, X in schemes.items():
        n = len(X)
        rho = n / V
        a = rho ** (-1 / 3)
        # R_47 from the density law: (4 pi / 3) rho R^3 = 47
        R47 = (N_EX / (4 * math.pi / 3 * rho)) ** (1 / 3)
        # direct count: median over the 30% most central spins of the radius holding N_EX spins (if available)
        dc = np.linalg.norm(X - hull_c, axis=1)
        cen = X[np.argsort(dc)[:max(1, int(0.3 * n))]]
        if n > N_EX:
            rk = [np.sort(np.linalg.norm(X - c, axis=1))[N_EX] for c in cen]
            R47_count = float(np.median(rk))
        else:
            R47_count = None
        out[name] = dict(n_spins=n, rho_per_A3=rho, spacing_a_A=a, R47_density_law_A=R47,
                         R47_counted_central_A=R47_count, whole_network_beyond_exact=bool(n > N_EX))
    dense_rho = out["dense_1H"]["rho_per_A3"]
    for name in out:
        lam = (dense_rho / out[name]["rho_per_A3"]) ** (1 / 3)
        out[name]["lambda_vs_dense"] = lam
        out[name]["time_stretch_lambda3"] = lam ** 3
        out[name]["residues_needed_for_whole_network_gt_47"] = int(math.ceil(N_EX / (out[name]["n_spins"] / nres)))
    return dict(pdb=pdb, n_res=nres, V_A3=V, schemes=out)


OUT["C_scale_law"] = dict(c1_dimensionless=c1_dimensionless(),
                          label_schemes=[label_schemes("1UBQ"), label_schemes("1PGA")])


# ------------------------------------------------------------------------------------------------ D
def design(fn, fam="F1", seg=2):
    r = json.load(open(os.path.join(HERE, "out", fn)))
    t = np.asarray(r["times_us"])
    v = r["families"][fam]
    fi = np.asarray(v["FI_t"])
    tc = v["best_t_c_index"]
    idx = np.arange(len(t))
    hard = idx >= tc
    cost = seg * t                                                     # evolution time per repetition (us)
    eff = np.where(hard & (cost > 0), fi / np.maximum(cost, 1e-9), 0)
    order = np.argsort(-eff)
    tot_h = fi[hard].sum()
    cum = []
    for k in (1, 2, 3, 5, 8):
        sel = order[:k]
        sel = sel[hard[sel]]
        cum.append(dict(k=k, frac_hard_FI=float(fi[sel].sum() / max(tot_h, 1e-30)),
                        frac_cost=float(cost[sel].sum() / max(cost[hard].sum(), 1e-30)),
                        times_us=t[sel].tolist()))
    return dict(file=fn, family=fam, t_c_index=tc, hard_FI=float(tot_h), best_points=cum)


OUT["D_design"] = [design("obs_1UBQ_p19_N10_o0_secular.json", "F1", 2),
                   design("obs_1UBQ_p19_N10_o0_secular.json", "F2", 4)]

json.dump(L.jsonable(OUT), open(os.path.join(HERE, "analysis.json"), "w"), indent=1)

# ---------------------------------------------------------------- console summary
for d in OUT["A_depth_budget"]:
    print("A", d["file"], d["t_c"], {T: {k: (round(v["FI_hard"]), v["n_hard"]) for k, v in row.items()}
                                      for T, row in d["budget"].items()})
for d in OUT["B_mechanism"]:
    for k, v in d["adversaries"].items():
        print("B", d["file"], k, "slope F1", None if v["slope_logF1_vs_logdelta"] is None else round(v["slope_logF1_vs_logdelta"], 2),
              "slope F2", None if v["slope_logF2_vs_logdelta"] is None else round(v["slope_logF2_vs_logdelta"], 2),
              "F1/delta", [round(x, 2) for x in v["ratio_F1_over_delta"]][-4:],
              "F2/sqrt", [round(x, 2) for x in v["ratio_F2_over_sqrtdelta"]][-4:])
print("C", json.dumps(OUT["C_scale_law"]["c1_dimensionless"]["median_min_max"]))
for s in OUT["C_scale_law"]["label_schemes"]:
    print("C", s["pdb"], s["n_res"], {k: (v["n_spins"], round(v["spacing_a_A"], 2), round(v["R47_density_law_A"], 1),
                                          None if v["R47_counted_central_A"] is None else round(v["R47_counted_central_A"], 1),
                                          round(v["time_stretch_lambda3"], 1), v["residues_needed_for_whole_network_gt_47"])
                                      for k, v in s["schemes"].items()})
for d in OUT["D_design"]:
    print("D", d["family"], d["t_c_index"], [(c["k"], round(c["frac_hard_FI"], 2), round(c["frac_cost"], 2)) for c in d["best_points"]])
