"""ROUND4 / allatom_superquadratic: generalised landscape-independent floor (hardness lane / CRITIC D1 formula) for
physics-based all-atom sampling of benchmark folders, against the enhanced-sampling classical twin.

  X = A rho K n_b G t_T / c ;  B*_s = X^(s/(s-1)) ;  T*_Q,s = K n_b G t_T X^(1/(s-1)) ;  exp: B* = X, T* = K n_b G t_T
  and for a concrete classical cost B_c (MD steps):  T_Q(B_c) = K n_b G t_T B_c^(1/s)  vs  T_c = c B_c / A.

Inputs
  * sizes: MEASURED (work/S1_*.json: amber14 + TIP3P cube, 1.0 nm padding; pairs within 1.0 nm) for 1L2Y / 1PGA / 1UBQ;
    other folders by a power-law fit of those three in residue count (INFERENCE).
  * c (s per MD step): MEASURED one loaded CPU core (work/S2_*.json); GPU implicit = 2 fs / (1 us/day)  [Nguyen et al.
    2014, PMID 25255057, verified: '~1 us/day per GPU'; 2 fs step is INFERENCE]; GPU explicit = CPU-core / 200
    (INFERENCE); Anton-class = 2e-6 s (UNVERIFIED recall, sensitivity only).
  * G (Toffolis per coherent full force evaluation, compute + uncompute): 2 x n_terms x tau
       explicit: n_terms = pairs within cutoff x f_nl  (f_nl = 1 generous: an oracle hands over the neighbour list;
                 4 central: padded coherent cell list) x (1 generous; 1.2 central for PME)
       implicit GBn2 (no cutoff): n_terms = all pairs x passes (2 generous: Born radii + energy; 3 central: + chain rule)
       tau (Toffolis per pair term): 6e3 generous (b = 20, b^2/2 multiplies), 1.6e4 central (b = 23, T3 primitives:
       sqdist 1,760 + inverse sqrt + ~16 multiplies for LJ 12-6, Coulomb/erfc, force components), 3e4 at b = 32.
       Consistent with T3's 7-9e3 Toffolis per learned-energy pair term (theory/RESOURCE_MODELS.md sec. 4).  DERIVED
       from stated assumptions; not compiled.
  * overheads: MO (K = 10, n_b = 1, A = rho = 1) and CE (K = 100, n_b = 2), as in ROUND3 hardness_what_it_takes.
  * classical twin B_c (MD steps per task), LITERATURE-SUPPORTED where marked (PubMed / PMC full text verified this
    session, lit/pubmed_records.json, lit/pmc/), step sizes INFERENCE (2 fs implicit, 2.5 fs explicit).
Output: floor_allatom.json, floor_allatom_table.md   (pure arithmetic, < 1 CPU-s)
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
DAY, YR = 86400.0, 3.156e7


def load(p):
    return json.load(open(os.path.join(WORK, p)))


S1 = {p: load(f"S1_{p}.json") for p in ("1L2Y", "1PGA", "1UBQ")}
S2 = {p: load(f"S2_{p}.json") for p in ("1L2Y", "1PGA", "1UBQ")}
nres = np.array([S1[p]["n_residues"] for p in S1], float)
fit_prot = np.polyfit(np.log(nres), np.log([S1[p]["n_atoms_protein"] for p in S1]), 1)
fit_exp = np.polyfit(np.log(nres), np.log([S1[p]["explicit_n_atoms"] for p in S1]), 1)
fit_cimp = np.polyfit(np.log([S1[p]["n_atoms_protein"] for p in S1]), np.log([S2[p]["implicit_gbn2_s_per_step"] for p in S1]), 1)
fit_cexp = np.polyfit(np.log([S1[p]["explicit_n_atoms"] for p in S1]), np.log([S2[p]["explicit_pme_s_per_step"] for p in S1]), 1)
PAIRS_PER_ATOM = float(np.mean([S1[p]["explicit_pairs_per_atom"] for p in S1]))


def size(p, n):
    if p in S1:
        s = S1[p]
        return dict(n_prot=s["n_atoms_protein"], n_exp=s["explicit_n_atoms"], pairs_imp=s["implicit_all_pairs"],
                    pairs_exp=s["explicit_pairs_within_1nm"], c_cpu_imp=S2[p]["implicit_gbn2_s_per_step"],
                    c_cpu_exp=S2[p]["explicit_pme_s_per_step"], size_source="MEASURED")
    npr = float(np.exp(np.polyval(fit_prot, math.log(n))))
    nex = float(np.exp(np.polyval(fit_exp, math.log(n))))
    return dict(n_prot=npr, n_exp=nex, pairs_imp=npr * (npr - 1) / 2, pairs_exp=nex * PAIRS_PER_ATOM,
                c_cpu_imp=float(np.exp(np.polyval(fit_cimp, math.log(npr)))),
                c_cpu_exp=float(np.exp(np.polyval(fit_cexp, math.log(nex)))), size_source="INFERENCE (fit to 3 measured)")


TAU = {"gen": 6e3, "cen": 1.6e4, "b32": 3e4}


def G_model(sz, solvent, level):
    if solvent == "explicit":
        f_nl, pme = (1.0, 1.0) if level == "gen" else (4.0, 1.2)
        terms = sz["pairs_exp"] * f_nl * pme
    else:
        terms = sz["pairs_imp"] * (2 if level == "gen" else 3)
    return 2.0 * terms * TAU[level]


def c_model(sz, solvent, hw):
    if hw == "cpu1":
        return sz["c_cpu_imp"] if solvent == "implicit" else sz["c_cpu_exp"]
    if hw == "gpu":
        # implicit: 2 fs step at ~1 us/day per GPU [Nguyen 2014] -> 86400 s / 5e8 steps = 1.73e-4 s
        return (86400.0 / (1e-6 / 2e-15)) if solvent == "implicit" else sz["c_cpu_exp"] / 200.0
    if hw == "anton":
        return 2e-6
    raise ValueError(hw)


# Benchmark folders and classical-twin costs.  B in MD steps.  'tag' records evidence status.
FOLDERS = [
    dict(name="Trp-cage", pdb="1L2Y", nres=20, solvent="explicit", tau_f_s=4.1e-6,
         twin=[("plain MD, one folding event (tau_f 4.1 us [Voelz 2010 PMC text] / 2.5 fs)", 4.1e-6 / 2.5e-15, "LIT tau_f; step INFERENCE"),
               ("bias-exchange metadynamics, full folding FES (8 replicas x 40 ns) [Piana & Laio 2007, PMID 17419610]", 8 * 40e-9 / 2e-15, "LIT; step INFERENCE")]),
    dict(name="Trp-cage (GBn2)", pdb="1L2Y", nres=20, solvent="implicit", tau_f_s=4.1e-6,
         twin=[("plain MD, one folding event (implicit)", 4.1e-6 / 2e-15, "INFERENCE: explicit tau_f reused")]),
    dict(name="villin HP35 / Fip35 WW (~10 us folders)", pdb=None, nres=35, solvent="explicit", tau_f_s=1.0e-5,
         twin=[("plain MD, one folding event (villin ~10 us, Fip35 ~13 us [Voelz 2010 PMC text])", 1.0e-5 / 2.5e-15, "LIT; step INFERENCE")]),
    dict(name="NTL9(1-39) (GB, water-like friction)", pdb=None, nres=39, solvent="implicit", tau_f_s=1e-3,
         twin=[("weighted ensemble, rate to ~1 decade (252 us aggregate) [Adhikari 2019 Table 1, PMC6660137]", 252e-6 / 2e-15, "LIT aggregate; step INFERENCE"),
               ("plain MD, one folding event (tau_f 0.2-2 ms; 1 ms)", 1e-3 / 2e-15, "LIT")]),
    dict(name="protein G B1 (GB, low friction)", pdb="1PGA", nres=56, solvent="implicit", tau_f_s=3e-3,
         twin=[("weighted ensemble, rate to ~2 decades (225 us aggregate) [Adhikari 2019 Table 1]", 225e-6 / 2e-15, "LIT aggregate; step INFERENCE"),
               ("plain MD, one folding event (tau_f >= 3 ms)", 3e-3 / 2e-15, "LIT lower end")]),
    dict(name="protein G B1 (explicit)", pdb="1PGA", nres=56, solvent="explicit", tau_f_s=6.5e-5,
         twin=[("distributed MD + MSM, ~65 us folding time for ~500 us aggregate [Ensign & Pande via Adhikari 2019 text]", 500e-6 / 2.5e-15, "LIT (secondary citation); step INFERENCE")]),
    dict(name="ubiquitin (explicit, ms folder)", pdb="1UBQ", nres=76, solvent="explicit", tau_f_s=1e-3,
         twin=[("plain MD, one folding event (ms folder [Piana 2013, PMID 23503848])", 1e-3 / 2.5e-15, "LIT (ms class); step INFERENCE")]),
    dict(name="lambda 6-85 (explicit, MSM)", pdb=None, nres=80, solvent="explicit", tau_f_s=1e-2,
         twin=[("MSM from 3,265 trajectories, 1.3 ms aggregate, 10 ms-timescale model [Bowman 2011, PMC3043158]", 1.3e-3 / 2.5e-15, "LIT; step INFERENCE")]),
]
OVER = {"MO": dict(K=10, nb=1, A=1.0, rho=1.0), "CE": dict(K=100, nb=2, A=1.0, rho=1.0)}
TT = (1e-6, 1e-7, 1e-8)
SS = (2, 3, 4, "exp")
BIOEMU_STEP_EQUIV = None  # filled per folder: 1 GPU-second per independent sample / c_gpu (INFERENCE from 'thousands/hour/GPU')


def floor(G, c, o, tT, s):
    X = o["A"] * o["rho"] * o["K"] * o["nb"] * G * tT / c
    step = o["K"] * o["nb"] * G * tT
    if s == "exp":
        return X, X, step
    return X, X ** (s / (s - 1)), step * X ** (1 / (s - 1))


def main():
    out = dict(fits=dict(prot_atoms_vs_nres=fit_prot.tolist(), explicit_atoms_vs_nres=fit_exp.tolist(),
                         c_cpu_imp_vs_atoms=fit_cimp.tolist(), c_cpu_exp_vs_atoms=fit_cexp.tolist(), pairs_per_atom=PAIRS_PER_ATOM),
               rows=[])
    for f in FOLDERS:
        sz = size(f["pdb"], f["nres"])
        for level in ("gen", "cen"):
            G = G_model(sz, f["solvent"], level)
            for hw in ("gpu", "cpu1", "anton"):
                if hw == "anton" and f["solvent"] == "implicit":
                    continue
                c = c_model(sz, f["solvent"], hw)
                for on, o in OVER.items():
                    if on == "CE" and level == "gen":
                        continue
                    for tT in TT:
                        row = dict(folder=f["name"], solvent=f["solvent"], size_source=sz["size_source"],
                                   n_atoms=sz["n_exp"] if f["solvent"] == "explicit" else sz["n_prot"],
                                   G_level=level, G=G, hw=hw, c=c, over=on, t_T=tT, per_s={}, twin=[])
                        for s in SS:
                            X, B, TQ = floor(G, c, o, tT, s)
                            row["per_s"][str(s)] = dict(X=X, Bstar=B, TstarQ_s=TQ, TstarQ_days=TQ / DAY)
                        for (desc, Bc, tag) in f["twin"]:
                            tw = dict(desc=desc, B_c=Bc, tag=tag, T_c_days=c * Bc / o["A"] / DAY, per_s={})
                            for s in SS:
                                step = o["K"] * o["nb"] * G * tT
                                TQb = step if s == "exp" else step * Bc ** (1 / s)
                                tw["per_s"][str(s)] = dict(T_Q_days=TQb / DAY, quantum_wins=bool(TQb < c * Bc / o["A"]),
                                                           within_month=bool(TQb <= 30 * DAY))
                            row["twin"].append(tw)
                        # amortised AI emulator (BioEmu: 'thousands of statistically independent structures per hour
                        # on a single GPU', PMID 40638710) -> ~1 GPU-s per independent sample; ~1 kcal/mol accuracy
                        if hw == "gpu":
                            row["bioemu_step_equiv_per_sample"] = 1.0 / c
                            row["exp_speedup_T_per_sample_s"] = o["K"] * o["nb"] * G * tT
                        out["rows"].append(row)
    # ---------------- verdict arithmetic (resource arm only; precondition arm is in README / families.json)
    def best(s, tT, hwsel="gpu"):
        rr = [r for r in out["rows"] if r["t_T"] == tT and r["hw"] == hwsel and r["over"] == "MO" and r["G_level"] == "gen"]
        return min(rr, key=lambda r: r["per_s"][s]["TstarQ_s"])
    out["most_favourable"] = {f"s={s}, t_T={tT:g}": dict(folder=best(str(s), tT)["folder"],
                                                        TstarQ_days=best(str(s), tT)["per_s"][str(s)]["TstarQ_days"],
                                                        Bstar=best(str(s), tT)["per_s"][str(s)]["Bstar"])
                              for s in SS for tT in TT}
    tmp = os.path.join(HERE, "floor_allatom.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "floor_allatom.json"))

    # ---------------- markdown
    def fd(d):
        if d < 1 / 24:
            return f"{d * 86400:.2g} s"
        if d < 1:
            return f"{d * 24:.2g} h"
        if d < 365:
            return f"{d:.2g} d"
        return f"{d / 365.25:.2g} yr"
    L = ["| folder | solvent | atoms | G (Toffoli/step) | c (s/step, hw) | t_T | B*_2 / T*_Q,2 | B*_3 / T*_Q,3 | B*_4 / T*_Q,4 | T*_Q,exp |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in out["rows"]:
        if r["over"] != "MO" or r["G_level"] != "gen" or r["hw"] != "gpu":
            continue
        ps = r["per_s"]
        L.append(f"| {r['folder']} | {r['solvent']} | {r['n_atoms']:.3g} | {r['G']:.2g} | {r['c']:.2g} | {r['t_T'] * 1e9:g} ns | "
                 + " | ".join(f"{ps[s]['Bstar']:.1e} / {fd(ps[s]['TstarQ_days'])}" for s in ("2", "3", "4")) + f" | {fd(ps['exp']['TstarQ_days'])} |")
    L2 = ["| folder | twin (classical cost B_c, MD steps) | T_c on 1 GPU | t_T | s=2: T_Q (wins?) | s=3: T_Q (wins?) | s=4: T_Q (wins?) |",
          "|---|---|---|---|---|---|---|"]
    for r in out["rows"]:
        if r["over"] != "MO" or r["G_level"] != "gen" or r["hw"] != "gpu" or r["t_T"] not in (1e-6, 1e-8):
            continue
        for tw in r["twin"]:
            L2.append(f"| {r['folder']} | {tw['desc']} = {tw['B_c']:.1e} | {fd(tw['T_c_days'])} | {r['t_T'] * 1e9:g} ns | "
                      + " | ".join(f"{fd(tw['per_s'][s]['T_Q_days'])} ({'yes' if tw['per_s'][s]['quantum_wins'] else 'no'})" for s in ("2", "3", "4")) + " |")
    L3 = ["| folder | G level | hw | overheads | t_T | T*_Q,2 | T*_Q,3 | T*_Q,4 |", "|---|---|---|---|---|---|---|---|"]
    for r in out["rows"]:
        if r["t_T"] != 1e-8 or (r["G_level"], r["hw"], r["over"]) == ("gen", "gpu", "MO"):
            continue
        ps = r["per_s"]
        L3.append(f"| {r['folder']} | {r['G_level']} | {r['hw']} | {r['over']} | 10 ns | {fd(ps['2']['TstarQ_days'])} | {fd(ps['3']['TstarQ_days'])} | {fd(ps['4']['TstarQ_days'])} |")
    open(os.path.join(HERE, "floor_allatom_table.md"), "w", encoding="utf-8").write(
        "## Floor, MO overheads, generous G, one GPU as classical comparator\n\n" + "\n".join(L) +
        "\n\n## Against the literature classical twin (MO, generous G, 1 GPU)\n\n" + "\n".join(L2) +
        "\n\n## Sensitivity at t_T = 10 ns (central G, CPU-core / Anton comparators, CE overheads)\n\n" + "\n".join(L3) + "\n")
    print("\n".join(L)); print(); print("\n".join(L2))
    print(json.dumps(out["most_favourable"], indent=1))


if __name__ == "__main__":
    main()
