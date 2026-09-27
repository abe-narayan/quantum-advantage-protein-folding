"""Figures for the discovery report (research/results/FIGURES).  Reads RAW/PROCESSED results; every figure is
regenerable:  python scripts/make_figures.py
  F1 g1_census.png      mode census vs L: fraction of distinct modes, p_hit(best mode) (gmean), end discovery rate
  F2 g1_nrpt.png        lambda-path NRPT: communication barrier Lambda vs L (T = 1 and T-scan), round trips
  F3 nmr_example.png    one NMR job: exact S_ab(t), per-time Fisher information, classical-adversary failure times
  F4 nmr_scaling.png    NMR: f_hard (best adversary) and max information gain vs N and gamma
  F5 tpt.png            temperature exchange: C_max/L vs L and dip ratio (cooperativity)
"""
from __future__ import annotations

import glob
import json
import os
from collections import defaultdict

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research", "results", "RAW")
PROC = os.path.join(ROOT, "research", "results", "PROCESSED")
FIG = os.path.join(ROOT, "research", "results", "FIGURES")
os.makedirs(FIG, exist_ok=True)


def f1():
    p = os.path.join(PROC, "g1_summary.json")
    if not os.path.exists(p):
        return
    g = json.load(open(p))
    fig, ax = plt.subplots(1, 3, figsize=(12, 3.4))
    for name, mk in (("census256", "o-"), ("census2k", "s--")):
        by = defaultdict(list)
        for x in g.get(name, []):
            by[x["L"]].append(x)
        if not by:
            continue
        Ls = sorted(by)
        ax[0].plot(Ls, [np.median([x["frac_modes"] for x in by[L]]) for L in Ls], mk, label=name)
        ax[1].semilogy(Ls, [np.exp(np.mean(np.log([x["p_hit"] for x in by[L]]))) for L in Ls], mk, label=name)
        ax[2].plot(Ls, [np.median([x["new_mode_rate_end"] for x in by[L]]) for L in Ls], mk, label=name)
    ax[0].set_ylabel("distinct modes / restarts"); ax[1].set_ylabel("p_hit(best mode), gmean")
    ax[2].set_ylabel("new modes per restart (last quarter)")
    for a in ax:
        a.set_xlabel("crop length L (aa)"); a.legend(fontsize=7)
    fig.suptitle("G1 mode census (multistart L-BFGS from the exact prior, 2 Å clustering)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "g1_census.png"), dpi=130); plt.close(fig)


def f2():
    p = os.path.join(PROC, "g1_summary.json")
    if not os.path.exists(p):
        return
    g = json.load(open(p))
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    for name, mk in (("nrpt_pilot", "o"), ("nrpt_tscan", "s")):
        xs = g.get(name, [])
        if not xs:
            continue
        for T in sorted({x["T"] for x in xs}):
            s = sorted([x for x in xs if x["T"] == T], key=lambda x: x["L"])
            ax[0].plot([x["L"] for x in s], [x["Lambda"] for x in s], mk + "-", label=f"{name} T={T:g}")
            ax[1].plot([x["L"] for x in s], [x["trips"] for x in s], mk + "-", label=f"{name} T={T:g}")
    ax[0].set_ylabel("communication barrier Λ"); ax[1].set_ylabel("round trips (production)")
    for a in ax:
        a.set_xlabel("L (aa)"); a.legend(fontsize=6)
    fig.suptitle("G1 λ-path non-reversible PT (prior → posterior)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "g1_nrpt.png"), dpi=130); plt.close(fig)


def f3():
    files = sorted(glob.glob(os.path.join(RAW, "nmr_gate", "*_N10_o0_g0.json")))
    if not files:
        return
    r = json.load(open(files[0]))
    t = np.array(r["times"]) * 1e6
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.6))
    for b, v in r["S_exact"].items():
        ax[0].plot(t, v, label=f"S_a,{b}")
    if r.get("F_exact"):
        for b, v in r["F_exact"].items():
            ax[0].plot(t, v, "--", lw=0.8, label=f"F_a,{b} (OTOC)")
    for p in r["params"]:
        ax[1].semilogy(t, np.maximum(p["FI_t"], 1e-6), label=f"{p['name']} (S)")
        if "FI_otoc_t" in p:
            ax[2].semilogy(t, np.maximum(p["FI_otoc_t"], 1e-6), label=f"{p['name']} (OTOC)")
    for k, v in r["adversaries"].items():
        tc = v["t_c_index"]
        if tc < len(t):
            ax[1].axvline(t[tc], color="k", alpha=0.25, lw=0.8)
            ax[1].text(t[tc], ax[1].get_ylim()[1] * 0.5, k, rotation=90, fontsize=6)
        tco = v.get("t_c_otoc_index")
        if tco is not None and tco < len(t):
            ax[2].axvline(t[tco], color="k", alpha=0.25, lw=0.8)
            ax[2].text(t[tco], 1, k, rotation=90, fontsize=6)
    ax[0].set_ylabel("correlator"); ax[1].set_ylabel("Fisher information per time point (σ = 0.01)")
    ax[2].set_ylabel("OTOC Fisher information per time point")
    for a in ax:
        a.set_xlabel("t (µs)"); a.legend(fontsize=6)
    fig.suptitle(f"C1 NMR gate: {r['pdb']} probe {r['probe_name']}, N={r['N']}, γ={r['gamma']:g}/s; vertical lines = classical failure times")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "nmr_example.png"), dpi=130); plt.close(fig)


def f4():
    p = os.path.join(PROC, "nmr_gate2_summary.json")
    if not os.path.exists(p):
        return
    s = json.load(open(p))["rows"]
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    by = defaultdict(list)
    for x in s:
        by[x["gamma"]].append(x)
    for gm, xs in sorted(by.items()):
        Ns = sorted({x["N"] for x in xs})
        fh = [np.median([pp["frac_hard_best"] for x in xs if x["N"] == N for pp in x["params"]]) for N in Ns]
        gg = [np.median([max(x["gain_spectrum"]) for x in xs if x["N"] == N and x["gain_spectrum"]] or [np.nan]) for N in Ns]
        ax[0].plot(Ns, fh, "o-", label=f"γ={gm:g}/s")
        ax[1].semilogy(Ns, gg, "o-", label=f"γ={gm:g}/s")
    ax[0].set_ylabel("median f_hard (best classical adversary)"); ax[1].set_ylabel("median max information gain g")
    for a in ax:
        a.set_xlabel("cluster size N"); a.legend(fontsize=7)
    fig.suptitle("C1: structural information beyond the best classical approximation")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "nmr_scaling.png"), dpi=130); plt.close(fig)


def f5():
    p = os.path.join(PROC, "g1_summary.json")
    if not os.path.exists(p):
        return
    xs = json.load(open(p)).get("tpt", [])
    if not xs:
        return
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.4))
    ax[0].plot([x["L"] for x in xs], [x["Cmax_per_res"] for x in xs], "o", alpha=0.7)
    ax[0].set_ylabel("C_max / L"); ax[0].set_xlabel("L")
    d = [(x["L"], x["dip_ratio"]) for x in xs if x["dip_ratio"] is not None]
    if d:
        ax[1].plot(*zip(*d), "o")
    ax[1].set_ylabel("dip ratio at C_max rung (bimodal only)"); ax[1].set_xlabel("L")
    fig.suptitle("Q4 cooperativity: temperature replica exchange at λ = 1")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "tpt.png"), dpi=130); plt.close(fig)


if __name__ == "__main__":
    for f in (f1, f2, f3, f4, f5):
        try:
            f()
        except Exception as e:                      # one missing input must not block the others
            print(f.__name__, "skipped:", e)
    print("figures in", FIG)
