"""Relevance/novelty verifier for ROUND4 lane `spindmft` (adversarial, relevance lens).

Checks (all single-threaded, cheap, resumable: one atomic JSON checkpoint updated after every exact run):
  C1  Load-bearing test for the "spinDMFT predicted the b-remote shifts" claim: ISOLATED (no bath) exact b-aware
      clusters {a, b} U nearest-to-(a or b), N = 8, 10, 12 (N = 14 dropped: it duplicates the lane's exact_pairb_N14), deterministic sector-exact, same Trotter circuit.  If the
      isolated 10-spin b-aware cluster already gives the spinDMFT n_c = 10 protein-world value, the Gaussian bath (the
      only spinDMFT-specific ingredient) is not what carried the prediction.
  C2  Isolated probe-family clusters N = 10, 12 (sector-exact) for all 8 series, to show how small a cluster suffices
      at 40 us on the probe-local series.
  C3  Out-of-sample check of the flat-X refutation at N = 22 (p245, 40 us) from the sibling lane tx_early's files
      (read-only; not used by the spindmft lane).
  C4  Physical visibility of the residue the lane calls "open" (80, 120 us): A(t) * spread of classical F estimates,
      with the Sanchez-2022 reversal envelopes and the repo's T2 normalisations (same functions as the round-3
      relevance verifier), vs sigma = 0.01; and the same spread vs the physics lens's forward-model error.
Outputs: relevance_checks.json (+ .ckpt.json during the run).  Reads only; writes only into this folder.
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.abspath(os.path.join(HERE, ".."))
EXP = os.path.abspath(os.path.join(LANE, "..", ".."))            # research/experiments
sys.path.insert(0, LANE)
import sdmft as S  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

SIG = 0.01
TIMES = (40, 80, 120)
CK = os.path.join(HERE, "relevance_checks.ckpt.json")
OUT = os.path.join(HERE, "relevance_checks.json")


def atomic(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def load(p):
    with open(p) as f:
        return json.load(f)


def sector_F(D, a, bl):
    t0 = time.process_time()
    tt, Sd, Fd = SP.sector_exact_correlators(D, S.DT, 60, a, [bl], record_every=20, otoc=True)
    return dict(times_us=[round(float(x) * 1e6, 3) for x in tt], F=[float(x) for x in Fd[bl]],
                S=[float(x) for x in Sd[bl]], cpu_s=time.process_time() - t0)


def main():
    ck = load(CK) if os.path.exists(CK) else {}
    names, xyz_all, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    b0 = S.random_b0(1000)

    # ---------------- C1: isolated exact b-aware clusters (no bath)
    for p, b in ((245, 7), (19, 8), (19, 9)):
        order = SP.cluster(xyz_all, p, len(xyz_all))
        X = xyz_all[order]
        dmin = np.minimum(np.linalg.norm(X - X[0], axis=1), np.linalg.norm(X - X[b], axis=1))
        rest = [int(i) for i in np.argsort(dmin, kind="stable") if i not in (0, b)]
        for N in (8, 10, 12):          # N >= 12 duplicates the lane's own isolated exact b-aware runs
            key = f"C1_iso_pairb_p{p}_b{b}_N{N}"
            if key in ck:
                continue
            C = sorted([0, b] + rest[: N - 2])
            D = SP.couplings(X[C], b0)
            r = sector_F(D, C.index(0), C.index(b))
            r["C_world"] = C
            ck[key] = r
            atomic(ck, CK)
            print(key, [round(x, 4) for x in r["F"]], "cpu", round(r["cpu_s"], 1), flush=True)

    # ---------------- C2: isolated probe-family clusters (the round-3 reference family), N = 10, 12
    for p in (19, 245):
        for N in (10, 12):
            key = f"C2_iso_probe_p{p}_N{N}"
            if key in ck:
                continue
            w = S.load_world("1UBQ", p, N)
            res = {}
            for b in w["bs"]:
                res[str(b)] = sector_F(w["D"], 0, b)
            ck[key] = res
            atomic(ck, CK)
            print(key, {b: [round(x, 4) for x in v["F"]] for b, v in res.items()}, flush=True)

    # ---------------- gather lane numbers
    an = load(os.path.join(LANE, "analysis.json"))
    out = dict(C1={}, C2={}, C3={}, C4={}, notes={})

    def emb(tag):
        d = load(os.path.join(LANE, "out", tag + ".json"))
        return {int(round(t)): (f[0], s[0]) for t, f, s in zip([40, 80, 120], d["F"], d["F_se"])}

    for p, b in ((245, 7), (19, 8), (19, 9)):
        sd_prot = emb(f"emb_p{p}_Wprotein_nc10_pairb{b}_sr_M512_s7")
        sd_w18 = emb(f"emb_p{p}_W18_nc10_pairb{b}_sr_M512_s7")
        ex = {N: load(os.path.join(LANE, "out", f"exact_pairb_p{p}_b{b}_N{N}.json")) for N in (12, 14, 16)}
        rows = {}
        for i, t in enumerate(TIMES):
            iso = {N: ck[f"C1_iso_pairb_p{p}_b{b}_N{N}"]["F"][i + 1] for N in (8, 10, 12)}
            exN = {N: ex[N]["F"][i + 1] for N in (12, 14, 16)}
            rows[t] = dict(
                iso_exact_pairb=iso, exact_pairb_typ=exN, spinDMFT_pairb_protein=sd_prot[t][0],
                spinDMFT_pairb_protein_se=sd_prot[t][1], spinDMFT_pairb_W18=sd_w18[t][0],
                bath_contribution_spinDMFT_minus_iso10=sd_prot[t][0] - iso[10],
                iso10_minus_exact16=iso[10] - exN[16],
                iso12_sector_minus_typ12=iso[12] - exN[12],
                spinDMFT_minus_exact16=sd_prot[t][0] - exN[16])
        out["C1"][f"p{p}_b{b}"] = rows

    # probe-local series: how small a cluster suffices at 40 us
    tab = {(r["probe"], r["t_us"], r["site"]): r for r in an.get("table", [])} if isinstance(an.get("table"), list) else {}
    for p in (19, 245):
        for b in ("1", "7", "8", "9"):
            rows = {}
            for i, t in enumerate(TIMES):
                rows[t] = {f"iso_probe_N{N}": ck[f"C2_iso_probe_p{p}_N{N}"][b]["F"][i + 1] for N in (10, 12)}
            out["C2"][f"p{p}_b{b}"] = rows
    out["notes"]["C2_table_source"] = "compare with F18/F20 in ../analysis_stdout.txt"

    # ---------------- C3: tx_early N = 22 (p245, 40 us), read-only
    tx = os.path.join(EXP, "ROUND4", "tx_early", "runs")
    try:
        e22 = load(os.path.join(tx, "1UBQ_p245_N22_echo_R1_complex64_s4242_t20-40-60.json"))
        e20 = load(os.path.join(tx, "1UBQ_p245_N20_echo_R2_complex64_s4242_t20-40-60.json"))
        c3 = {}
        for b in ("1", "7", "8", "9"):
            c3[b] = dict(F20=e20["F"][b][0], F22=e22["F"][b][0], dF=e22["F"][b][0] - e20["F"][b][0],
                         dX=e22["X"][b][0] - e20["X"][b][0])
        c3["dH"] = e22["H"][0] - e20["H"][0]
        c3["dfloor"] = e22["floor"][0] - e20["floor"][0]
        c3["d_H_plus_floor"] = c3["dH"] + c3["dfloor"]
        c3["p245_b7_F22_minus_exact_pairb16"] = e22["F"]["7"][0] - out["C1"]["p245_b7"][40]["exact_pairb_typ"][16]
        c3["typicality_err_N22_R1"] = 2 ** -11
        c3["source"] = "ROUND4/tx_early/runs (partial files: only t = 40 us complete for echo mode)"
        out["C3"] = c3
    except FileNotFoundError as exc:  # sibling lane files may move
        out["C3"] = dict(error=str(exc))

    # ---------------- C4: physical visibility of the open residue
    sc = load(os.path.join(EXP, "ADVERSARIAL", "R1_physics_feasibility", "scales.json"))
    T2 = {}
    for j in sc["jobs"]:
        if j["pdb"] == "1UBQ" and not j["hn_only"]:
            T2.setdefault("cluster_isolated(non-physical,generous)", []).append(j["T2_cluster_us"])
            T2.setdefault("network_static", []).append(j["T2_network_static_us"])
            if "T2_network_rotoravg_us" in j:
                T2.setdefault("network_rotoravg", []).append(j["T2_network_rotoravg_us"])

    def env_LE(x):                      # Sanchez 2022 Loschmidt echo, T3 = 6.7 T2, tail 1.7 T2 (as round-3 verifier)
        T3 = 1 / 0.15
        l_ = 1.7 * 0.15 * T3
        return (1 + math.exp(-T3 / l_)) / (1 + math.exp((x - T3) / l_))

    def env_PE(x):                      # local polarisation echo, Gaussian, T3 = 4 T2
        return math.exp(-math.log(2) * (x / 4.0) ** 2)

    # classical F_inf candidates per series (hybrid excluded: refuted by the lane and by C3)
    stdout = open(os.path.join(LANE, "analysis_stdout.txt")).read().splitlines()
    hdr = [ln for ln in stdout if ln.strip().startswith("probe")]
    rows = []
    started = False
    for ln in stdout:
        if ln.strip().startswith("probe"):
            started = True
            continue
        if started and ln.strip():
            parts = ln.split()
            if len(parts) >= 12 and parts[0].isdigit():
                rows.append(parts)
    cols = ["probe", "t_us", "site", "F18", "F18_minus_floor", "Fhyb", "emb18_nc10", "embP_nc10", "embP_nc12",
            "Fcorr_nc10", "F20", "Fcorr20_nc"]

    def num(x):
        return None if x == "--" else float(x)

    spread = {}
    for r in rows:
        d = dict(zip(cols, r))
        p, t, b = int(d["probe"]), int(d["t_us"]), int(d["site"])
        cands = {k: num(d[k]) for k in ("F18", "F20", "Fcorr_nc10", "Fcorr20_nc")}
        key = f"p{p}_b{b}"
        if key in out["C1"]:
            cands["exact_pairb16"] = out["C1"][key][t]["exact_pairb_typ"][16]
            cands["spinDMFT_pairb_protein"] = out["C1"][key][t]["spinDMFT_pairb_protein"]
            cands["exact_pairb14"] = out["C1"][key][t]["exact_pairb_typ"][14]
            # probe-family numbers are known family-biased at b-remote sites: spread over b-aware estimators only
            use = ["exact_pairb16", "spinDMFT_pairb_protein", "exact_pairb14"]
        else:
            use = [k for k in ("F20", "F18", "Fcorr_nc10", "Fcorr20_nc") if cands[k] is not None]
        vals = [cands[k] for k in use]
        spread.setdefault(t, {})[key] = dict(candidates=cands, used=use, spread=max(vals) - min(vals),
                                             F_mid=0.5 * (max(vals) + min(vals)), Fhyb=num(d["Fhyb"]))
    vis = {}
    for name, v in T2.items():
        lo, hi = min(v), max(v)
        vis[name] = {"T2_us": [lo, hi], "T3_LE_us": [6.7 * lo, 6.7 * hi], "T3_PE_us": [4 * lo, 4 * hi]}
        for t in TIMES:
            x_lo, x_hi = t / hi, t / lo                               # generous end uses the largest T2
            A_LE = env_LE(x_lo)
            A_PE = env_PE(x_lo)
            sp = [s["spread"] for s in spread[t].values()]
            fm = [s["F_mid"] for s in spread[t].values()]
            vis[name][str(t)] = dict(
                t_over_T2=[x_lo, x_hi], A_LE_generous=A_LE, A_PE_generous=A_PE,
                max_spread=max(sp), median_spread=float(np.median(sp)),
                max_visible_spread_LE_over_sigma=A_LE * max(sp) / SIG,
                max_visible_spread_PE_over_sigma=A_PE * max(sp) / SIG,
                median_visible_signal_LE_over_sigma=A_LE * float(np.median(fm)) / SIG,
                median_visible_signal_PE_over_sigma=A_PE * float(np.median(fm)) / SIG)
    phys = load(os.path.join(EXP, "ADVERSARIAL", "R1_physics_feasibility", "physics_1UBQ_p19_N10_o0_g0.json"))
    out["C4"] = dict(
        spread_by_time={str(t): v for t, v in spread.items()}, visibility=vis,
        forward_model_error_1UBQ_p19_N10=dict(
            rotor_max_over_sigma_easy_t_lt_80=phys["rotor"]["max_dF_over_sigma_easy"],
            rotor_max_over_sigma_hard_t_ge_80=phys["rotor"]["max_dF_over_sigma_hard"],
            offsets_1kHz_easy=phys["nuisance"]["offsets_model_error"]["max_over_sigma_easy"],
            offsets_1kHz_hard=phys["nuisance"]["offsets_model_error"]["max_over_sigma_hard"],
            first_exceedance_us=phys["rotor"]["first_time_dF_exceeds_sigma_us"],
            reversal_mismatch_15pct_hard=phys["nuisance"]["eta_scan"]["0.15"]["max_dev_over_sigma_hard"]))
    out["cpu_s_exact_runs"] = sum(v["cpu_s"] for k, v in ck.items() if k.startswith("C1_")) + \
        sum(vv["cpu_s"] for k, v in ck.items() if k.startswith("C2_") for vv in v.values())
    out["raw"] = ck
    atomic(out, OUT)

    # ---------------- print summary
    print("\nC1 (b-remote; F at 40/80/120 us)")
    for k, rows_ in out["C1"].items():
        for t, r in rows_.items():
            print(f" {k} t={t}: iso N8/10/12 = " + " / ".join(f"{r['iso_exact_pairb'][N]:.4f}" for N in (8, 10, 12))
                  + f" | exact typ N12/14/16 = " + " / ".join(f"{r['exact_pairb_typ'][N]:.4f}" for N in (12, 14, 16))
                  + f" | spinDMFT = {r['spinDMFT_pairb_protein']:.4f}; bath part = {r['bath_contribution_spinDMFT_minus_iso10']:+.4f};"
                  f" iso10-ex16 = {r['iso10_minus_exact16']:+.4f}; iso12(sector)-typ12 = {r['iso12_sector_minus_typ12']:+.4f}")
    print("\nC2 (probe family, isolated)")
    for k, rows_ in out["C2"].items():
        print(" ", k, {t: {n: round(v, 4) for n, v in r.items()} for t, r in rows_.items()})
    print("\nC3", json.dumps(out["C3"], indent=None)[:900])
    print("\nC4 visibility")
    for name, v in vis.items():
        print(" ", name, "T2", [round(x, 2) for x in v["T2_us"]], "T3_LE", [round(x) for x in v["T3_LE_us"]],
              "T3_PE", [round(x) for x in v["T3_PE_us"]])
        for t in TIMES:
            q = v[str(t)]
            print(f"   t={t}: t/T2 {q['t_over_T2'][0]:.1f}-{q['t_over_T2'][1]:.1f}  A_LE {q['A_LE_generous']:.3g}  A_PE {q['A_PE_generous']:.3g}"
                  f"  max spread {q['max_spread']:.3f} (median {q['median_spread']:.3f})  visible spread LE {q['max_visible_spread_LE_over_sigma']:.2f} sig,"
                  f" PE {q['max_visible_spread_PE_over_sigma']:.2f} sig; median visible signal LE {q['median_visible_signal_LE_over_sigma']:.1f} sig, PE {q['median_visible_signal_PE_over_sigma']:.1f} sig")
    for t in TIMES:
        print(" spread", t, {k: round(v["spread"], 4) for k, v in spread[t].items()})
    print(" forward-model error", out["C4"]["forward_model_error_1UBQ_p19_N10"])
    print("cpu exact runs", round(out["cpu_s_exact_runs"], 1))


if __name__ == "__main__":
    main()
