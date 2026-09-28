"""ROUND3 / hardness_what_it_takes, part (3): what quantum speedup exponent and hardware would be needed to beat the best
classical method measured, at L = 100, 200, 300, 500.  Pure derivation (no protein computation); DERIVED from the K-101
break-even algebra generalised to a speedup exponent s, with measured / extrapolated classical costs from cost_fit.json.

Model (T2/T3 notation).  Classical: C_c evaluations per solution, c(L) s each, one core: T_c = C_c c / A.
Quantum: N_q = K n_b C_c^(1/s) coherent walk steps (s = 2, 3, 4), or N_q = K n_b P(L) for an 'exponential' speedup
(P = 1: idealised, P = L: one coherent sweep), each G(L) Toffolis at t_T s: T_q = N_q G t_T; cost rho T_q.
  break-even gate time      t_T^be  = c C_c^(1 - 1/s) / (A rho K n_b G)            (quantum wins iff t_T < t_T^be)
  landscape-independent floor (K-101 generalised): at break-even, B*_s = (A rho K n_b G t_T / c)^(s/(s-1)) and
                             T*_Q,s = K n_b G t_T (A rho K n_b G t_T / c)^(1/(s-1))  (s = 2 reproduces K-101)
Overhead scenarios: MO (most optimistic: K = 10, n_b = 1, A = rho = 1, D2 GENEROUS G) and CE (central: K = 100,
n_b = 2, D2 CENTRAL G); D3 (Cartesian, bond-relaxed, NOT the A80 target) as a sensitivity row only.
G(L): T3 RESOURCE_MODELS.md sec. 4.2 values at L = 100/150/200, extrapolated as a power law in L (fit on those three
points; b_w growth included implicitly).  c(L): measured in this lane (bench_c.json, batched B = 64, single core,
LOADED machine -> larger c -> quantum-favourable), power law fitted on L = 60..200; T2 A-c values as a sensitivity.
Plausibility line: logical Toffoli time t_T >= 1 us (T2's 'most optimistic'; [A56] cites 170 us).  Usefulness line:
T_q <= 30 days per solution at the break-even-or-better gate time.
Output: what_it_takes.json and what_it_takes_table.md
"""
from __future__ import annotations

import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LS = (100, 200, 300, 500)
DAY = 86400.0
PLAUSIBLE_TT = 1e-6
USEFUL_TQ = 30 * DAY

# T3 sec. 4.2 (Toffolis per qubitised walk step)
T3 = {"D2gen": {100: 9.3e7, 150: 2.2e8, 200: 4.2e8}, "D2cen": {100: 3.1e8, 150: 7.5e8, 200: 1.4e9},
      "D3gen": {100: 1.8e7, 150: 3.2e7, 200: 4.8e7}}


def Gfun(design):
    x = np.log(list(T3[design].keys())); y = np.log(list(T3[design].values()))
    b, a = np.polyfit(x, y, 1)
    return (lambda L: float(np.exp(a) * L ** b)), float(b)


def main():
    bench = json.load(open(os.path.join(HERE, "bench_c.json")))
    fitc = next(r for r in bench if r.get("fit") == "c_batched64_s")
    c_meas = lambda L: fitc["prefactor"] * L ** fitc["exponent"]                     # noqa: E731
    c_Ac = lambda L: 1.80e-3 * (L / 150.0) ** 1.48                                   # noqa: E731  T2 A-c (idle-corrected)
    cf = json.load(open(os.path.join(HERE, "cost_fit.json")))
    own = {int(k): v for k, v in cf["T_own"]["extrapolated_C"].items()}
    ref = cf["T_ref"]["per_L"]
    # classical cost scenarios C_c(L) (evaluations per solution)
    med150 = ref["150"]["median_C_portfolio"]; max150 = ref["150"]["max_C_portfolio"]
    scen = {
        "BEST-median": dict(desc="best classical portfolio measured (DG-E1 first, DG draws, multistart, NRPT), median crop; "
                                 "measured 420 evals at L = 100 and 150; extrapolated x (L/150) (linear growth assumed)",
                            C=lambda L: med150 * max(L / 150.0, 1.0)),
        "BEST-worst": dict(desc="best classical portfolio, worst measured crop at L = 150 (5.8e4 evals), extrapolated x (L/150)^2",
                           C=lambda L: max150 * max(L / 150.0, 1.0) ** 2),
        "FOLD-ms": dict(desc="random-prior multistart to the best-known fold (3 A), worst measured crop 3.5e3 evals at L = 150, "
                             "extrapolated with the census exponential rate exp(0.041 (L-150))",
                        C=lambda L: 3.5e3 * math.exp(0.0415 * (L - 150))),
        "HYP-own": dict(desc="HYPOTHETICAL no-bypass: random multistart to its own best 2-A cluster, censored-Tobit "
                             "exponential fit (rate 0.041/residue) extrapolated; a moving target, NOT the best classical method",
                        C=lambda L: own[L]),
    }
    Gs = {k: Gfun(k) for k in T3}
    over = {"MO": dict(K=10, nb=1, A=1.0, rho=1.0, G="D2gen"), "CE": dict(K=100, nb=2, A=1.0, rho=1.0, G="D2cen"),
            "MO-D3": dict(K=10, nb=1, A=1.0, rho=1.0, G="D3gen")}
    speed = {"s=2": 2.0, "s=3": 3.0, "s=4": 4.0, "exp(P=1)": math.inf, "exp(P=L)": "L"}
    out = dict(G_exponents={k: v[1] for k, v in Gs.items()}, G_values={k: {L: Gs[k][0](L) for L in LS} for k in T3},
               c_values_meas={L: c_meas(L) for L in LS}, c_values_Ac={L: c_Ac(L) for L in LS},
               scenarios={k: dict(desc=v["desc"], C={L: v["C"](L) for L in LS}) for k, v in scen.items()},
               floors={}, table=[])
    # ---- landscape-independent floor generalised to s (no classical data needed)
    for on, o in over.items():
        for L in LS:
            G = Gs[o["G"]][0](L)
            for tT in (1e-6, 1e-7, 1e-8):
                X = o["A"] * o["rho"] * o["K"] * o["nb"] * G * tT / c_meas(L)
                for sn, s in (("s=2", 2.0), ("s=3", 3.0), ("s=4", 4.0)):
                    B = X ** (s / (s - 1)); TQ = o["K"] * o["nb"] * G * tT * X ** (1 / (s - 1))
                    out["floors"].setdefault(on, []).append(dict(L=L, t_T=tT, s=sn, Bstar=B, TstarQ_s=TQ, TstarQ_days=TQ / DAY))
                out["floors"][on].append(dict(L=L, t_T=tT, s="exp(P=1)", Bstar=X, TstarQ_s=o["K"] * o["nb"] * G * tT,
                                              TstarQ_days=o["K"] * o["nb"] * G * tT / DAY))
    # ---- requirement table per (scenario, overheads, L, s)
    for sc, sv in scen.items():
        for on, o in over.items():
            for L in LS:
                G = Gs[o["G"]][0](L); c = c_meas(L); C = sv["C"](L)
                Tc = C * c / o["A"]
                row = dict(scenario=sc, overheads=on, L=L, C_c=C, c=c, T_c_s=Tc, G=G, per_s={})
                min_s = None
                for sn, s in speed.items():
                    if s == "L":
                        Nq = o["K"] * o["nb"] * L
                    elif s == math.inf:
                        Nq = o["K"] * o["nb"] * 1.0
                    else:
                        Nq = o["K"] * o["nb"] * C ** (1.0 / s)
                    tbe = Tc / (o["rho"] * Nq * G)                    # break-even Toffoli time
                    tuse = USEFUL_TQ / (Nq * G)                         # Toffoli time for T_q <= 30 days
                    treq = min(tbe, tuse)
                    TQ1us = Nq * G * 1e-6
                    ok = treq >= PLAUSIBLE_TT
                    row["per_s"][sn] = dict(N_q=Nq, t_T_breakeven=tbe, t_T_30days=tuse, t_T_required=treq,
                                            T_q_at_1us_days=TQ1us / DAY, plausible=bool(ok))
                    if ok and min_s is None:
                        min_s = sn
                row["min_s_plausible"] = min_s
                out["table"].append(row)
    tmp = os.path.join(HERE, "what_it_takes.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "what_it_takes.json"))

    # ---- markdown table
    def f(x):
        if x is None:
            return "-"
        if x >= 1:
            return f"{x:.2g} s" if x < 1e3 else f"{x:.1e} s"
        for unit, sc_ in (("ms", 1e-3), ("us", 1e-6), ("ns", 1e-9), ("ps", 1e-12)):
            if x >= sc_:
                return f"{x / sc_:.2g} {unit}"
        return f"{x:.1e} s"
    lines = ["| classical cost scenario | overheads | L | C_c (evals) | T_c | s=2 | s=3 | s=4 | exp(P=1) | exp(P=L) | min s at t_T >= 1 us and T_q <= 30 d |",
             "|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in out["table"]:
        if r["overheads"] == "MO-D3":
            continue
        cells = [f(r["per_s"][k]["t_T_required"]) for k in speed]
        Tc = r["T_c_s"]
        Tcs = f"{Tc:.2g} s" if Tc < 3600 else (f"{Tc / 3600:.2g} h" if Tc < DAY else f"{Tc / DAY:.2g} d")
        lines.append(f"| {r['scenario']} | {r['overheads']} | {r['L']} | {r['C_c']:.2g} | {Tcs} | " + " | ".join(cells) +
                     f" | {r['min_s_plausible'] or 'none'} |")
    lines.append("")
    lines.append("Cells: required logical Toffoli time t_T = min(break-even, 30-day usefulness) for the given speedup; "
                 "'plausible' means >= 1 us.")
    fl = ["| overheads | L | t_T | B*_2 | T*_Q (s=2) | B*_3 | T*_Q (s=3) | B*_4 | T*_Q (s=4) | T*_Q exp(P=1) |", "|---|---|---|---|---|---|---|---|---|---|"]
    for on in ("MO", "CE"):
        for L in LS:
            for tT in (1e-6, 1e-8):
                rr = {x["s"]: x for x in out["floors"][on] if x["L"] == L and x["t_T"] == tT}
                d = lambda s: rr[s]["TstarQ_days"]                                # noqa: E731
                fmt = lambda v: (f"{v * 24:.2g} h" if v < 1 else (f"{v:.2g} d" if v < 365 else f"{v / 365:.2g} yr"))  # noqa: E731
                fl.append(f"| {on} | {L} | {f(tT)} | {rr['s=2']['Bstar']:.1e} | {fmt(d('s=2'))} | {rr['s=3']['Bstar']:.1e} | "
                          f"{fmt(d('s=3'))} | {rr['s=4']['Bstar']:.1e} | {fmt(d('s=4'))} | {fmt(d('exp(P=1)'))} |")
    open(os.path.join(HERE, "what_it_takes_table.md"), "w").write(
        "## Required speedup exponent and hardware per L\n\n" + "\n".join(lines) +
        "\n\n## Landscape-independent floor generalised to exponent s (break-even classical cost B*_s and per-solution quantum wall-clock T*_Q,s)\n\n"
        + "\n".join(fl) + "\n")
    print("\n".join(lines)); print(); print("\n".join(fl))
    print("G exponents", out["G_exponents"]); print("c(L) meas", out["c_values_meas"]); print("c(L) A-c", out["c_values_Ac"])


if __name__ == "__main__":
    main()
