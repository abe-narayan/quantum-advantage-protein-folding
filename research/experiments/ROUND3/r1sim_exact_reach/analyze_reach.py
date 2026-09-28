"""R1-SIM exact-reach analysis (no heavy compute).  Reads the lane's runs/, bench_kernels.json and the reference
ladder (research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone/), and writes reach_summary.json:
  1. validation summary (reference mode bit-level, flip mode statistical, complex64 error, Trotter vs exact time)
  2. measured cost per echo curve vs N and the cost/memory model -> exact-reach frontier N_max(budget, memory)
  3. convergence ladder incl. the new N = 20 points; pre-registered Delta statistic; 1/N and exponential fits;
     the N at which the finite-size error would fall below sigma under each model; false-convergence check of the
     pre-registered step criterion under 1/N drift.
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REF = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
SIGMA = 0.01
V_CURVE = 4400          # vector-steps per full echo curve (8 times, 4 sites, forward reuse) = 5 * (160 + 720)
V_REF = 8000            # reference script: 5 * 2 * 720 + 5 * 160


def D_fold(N):
    return (2 ** N + math.comb(N, N // 2)) / 2 if N % 2 == 0 else 2 ** (N - 1)


def load_runs():
    out = {}
    for f in glob.glob(os.path.join(HERE, "runs", "*.json")):
        if f.endswith(".ckpt.json"):
            continue
        out[os.path.basename(f)] = json.load(open(f))
    return out


def ladder(probe):
    return {N: json.load(open(os.path.join(REF, f"1UBQ_p{probe}_N{N}.json"))) for N in (12, 14, 16, 18)
            if os.path.exists(os.path.join(REF, f"1UBQ_p{probe}_N{N}.json"))}


def n20_values(runs):
    """{(probe, t_us): {site: F}} from the N = 20 runs (complete JSON or the p245 union checkpoint)."""
    vals = {}
    for name, r in runs.items():
        if r.get("N") != 20:
            continue
        for ti, t in enumerate(r["times_us"]):
            if t == 0:
                continue
            vals[(r["probe"], round(t))] = {b: r["F"][b][ti] for b in r["F"]}
    ck = os.path.join(HERE, "runs", "1UBQ_p245_N20_flip_trotter_complex64_t80-160_U.json.ckpt.json")
    if os.path.exists(ck):
        s = json.load(open(ck))
        for n in ("80", "160"):
            if all(n in s["F"][b] for b in s["F"]):
                vals[(245, round(int(n) * 2))] = {b: s["F"][b][n] for b in s["F"]}
    return vals


def fit_inv_n(Ns, F):
    A = np.vstack([np.ones(len(Ns)), 1.0 / np.asarray(Ns, float)]).T
    coef, res, *_ = np.linalg.lstsq(A, np.asarray(F, float), rcond=None)
    pred = A @ coef
    return float(coef[0]), float(coef[1]), float(np.sqrt(np.mean((pred - F) ** 2)))


def fit_exp(Ns, F):
    """F = Finf + A exp(-N/xi): scan xi, linear LSQ for (Finf, A)."""
    best = None
    for xi in np.geomspace(0.5, 200, 400):
        A = np.vstack([np.ones(len(Ns)), np.exp(-np.asarray(Ns, float) / xi)]).T
        coef, *_ = np.linalg.lstsq(A, np.asarray(F, float), rcond=None)
        r = float(np.sqrt(np.mean((A @ coef - F) ** 2)))
        if best is None or r < best[3]:
            best = (float(coef[0]), float(coef[1]), float(xi), r)
    return best


def main():
    runs = load_runs()
    out = {}
    # ------------------------------------------------------------------ 1. validation
    val = {}
    for p in (19, 245):
        r = runs.get(f"1UBQ_p{p}_N14_reference_trotter_complex128_t20-40-60-80-100-120-140-160.json")
        L = ladder(p)
        if r and 14 in L:
            val[f"N14_reference_mode_p{p}_max_abs_dF"] = max(abs(x - y) for b in L[14]["F"] for x, y in zip(r["F"][b], L[14]["F"][b]))
    for N in (14, 16):
        r = runs.get(f"1UBQ_p245_N{N}_flip_trotter_complex64_t20-40-60-80-100-120-140-160_U.json")
        L = ladder(245)
        if r and N in L:
            d = np.array([[x - y for x, y in zip(r["F"][b][1:], L[N]["F"][b][1:])] for b in L[N]["F"]])
            val[f"N{N}_flip_c64_vs_reference_p245"] = dict(max_abs=float(np.abs(d).max()), rms=float(np.sqrt((d ** 2).mean())),
                                                            expected_rms=float(math.sqrt(3 * 2.0 ** -N)),
                                                            cpu_s=r["cpu_secs_total"], ref_s=L[N]["secs"])
    a = runs.get("1UBQ_p245_N14_flip_trotter_complex64_t20-40-60-80-100-120-140-160_U.json")
    b_ = runs.get("1UBQ_p245_N14_flip_trotter_complex128_t20-40-60-80-100-120-140-160_U.json")
    if a and b_:
        val["N14_c64_vs_c128_same_draws_max_abs_dF"] = max(abs(x - y) for k in a["F"] for x, y in zip(a["F"][k], b_["F"][k]))
    if os.path.exists(os.path.join(HERE, "validate_flip.json")):
        val["flip_identity_N10"] = json.load(open(os.path.join(HERE, "validate_flip.json")))
    for p in (19, 245):
        T = runs.get(f"1UBQ_p{p}_N12_reference_trotter_complex128_t20-40-60-80-100-120-140-160_U.json")
        C = runs.get(f"1UBQ_p{p}_N12_reference_cheb_complex128_t20-40-60-80-100-120-140-160.json")
        if T and C:
            dd = np.array([[x - y for x, y in zip(T["F"][b], C["F"][b])] for b in T["F"]])
            val[f"N12_trotter_minus_exact_time_p{p}"] = dict(max_abs_dF=float(np.abs(dd).max()),
                                                              max_abs_dF_t_ge_160=float(np.abs(dd[:, 4:]).max()),
                                                              cheb_terms_per_40us_max=max(C["stats"]["cheb_terms"].values()))
    out["validation"] = val
    # ------------------------------------------------------------------ 2. cost and reach
    bench = json.load(open(os.path.join(HERE, "bench_kernels.json")))
    meas = []
    for name, r in runs.items():
        if r.get("N") == 20 and r.get("complete"):
            vs = r["vector_steps_total"] / (r["N"] // 2 + 1)            # per-sector vector steps
            meas.append(dict(run=name, cpu_s=r["cpu_secs_total"], vector_steps_per_sector=vs,
                             s_per_vector_step=r["cpu_secs_total"] / vs,
                             ns_per_pair_elem=1e9 * r["cpu_secs_total"] / vs / (190 * D_fold(20) / 2),
                             peak_rss_GB=r.get("peak_rss_GB")))
    c_pe = dict(low=min(m["ns_per_pair_elem"] for m in meas) * 1e-9 if meas else 7.5e-9,
                high=16e-9)  # high: N=22 central-sector complex64 benchmark under full machine contention
    rows = []
    for N in range(16, 49, 2):
        pairs = N * (N - 1) / 2
        Df = D_fold(N)
        cpu_curve = [V_CURVE * pairs * Df / 2 * c for c in (c_pe["low"], c_pe["high"])]
        mem_sector_min = 3 * math.comb(N, N // 2) * 8          # 3 complex64 vectors of the largest sector (recompute fwd)
        mem_full_fast = 8 * 2 ** N * 8                          # 8 complex64 full-space vectors (forward reuse)
        gates = V_CURVE * pairs
        gpu_bytes_per_gate = Df * 8                             # flip-flop half of the folded vector, read + write
        rows.append(dict(N=N, D_fold=Df, pairs=pairs, gates_per_curve=gates,
                         cpu_core_hours_per_curve=[c / 3600 for c in cpu_curve],
                         mem_GB_sector_3vec=mem_sector_min / 1e9, mem_GB_full_8vec=mem_full_fast / 1e9,
                         gpu_hours_per_curve_at_2TBps=gates * gpu_bytes_per_gate / 2e12 / 3600))
    out["cost_model"] = dict(V_curve=V_CURVE, V_reference=V_REF, c_pe_s=c_pe, measured_N20=meas, rows=rows,
                             notes="cpu: single core numpy on this (contended) machine; gpu: pure bandwidth bound, "
                                   "no gate fusion, no communication; multi-node adds all-to-all for global qubits")
    # frontier
    def nmax(pred):
        ok = [r["N"] for r in rows if pred(r)]
        return max(ok) if ok else None
    out["frontier"] = {
        "workstation_this_machine_8cores_15.6GB_1day": nmax(lambda r: r["cpu_core_hours_per_curve"][1] / 8 <= 24 and r["mem_GB_sector_3vec"] <= 12),
        "workstation_1week": nmax(lambda r: r["cpu_core_hours_per_curve"][1] / 8 <= 168 and r["mem_GB_sector_3vec"] <= 12),
        "one_gpu_80GB_1day": nmax(lambda r: r["gpu_hours_per_curve_at_2TBps"] <= 24 and r["mem_GB_sector_3vec"] <= 80),
        "gpu_node_8x80GB_1day": nmax(lambda r: r["gpu_hours_per_curve_at_2TBps"] / 8 * 3 <= 24 and r["mem_GB_sector_3vec"] <= 640),
        "large_hpc_4096_gpus_64GB_1week": nmax(lambda r: r["gpu_hours_per_curve_at_2TBps"] / 4096 * 3 <= 168 and r["mem_GB_sector_3vec"] <= 4096 * 64),
        "exascale_37888_gpus_64GB_1month": nmax(lambda r: r["gpu_hours_per_curve_at_2TBps"] / 37888 * 3 <= 720 and r["mem_GB_sector_3vec"] <= 37888 * 64),
        "assumptions": "per-curve = 8 echo times x 4 sites x 1 probe x 1 orientation; x3 comm penalty for multi-GPU; "
                       "memory = 3 complex64 vectors of the largest magnetisation sector (sector-restricted, recompute "
                       "forward legs, x~1.6 more steps); no gate fusion (would buy ~3-10x time, ~1-2 spins)"}
    # ------------------------------------------------------------------ 3. convergence
    n20 = n20_values(runs)
    conv = {}
    for p in (19, 245):
        L = ladder(p)
        for t_us, ti in ((160, 4), (320, 8)):
            key = f"p{p}_t{t_us}"
            Ns = sorted(L)
            series = {b: [L[N]["F"][b][ti] for N in Ns] for b in L[18]["F"]}
            Ns_all = list(Ns)
            if (p, t_us) in n20:
                Ns_all = Ns + [20]
                for b in series:
                    series[b].append(n20[(p, t_us)][b])
            steps = []
            for i in range(len(Ns_all) - 1):
                errs = [2.0 ** (-Ns_all[i] / 2), (math.sqrt(2) if Ns_all[i + 1] == 20 else 1.0) * 2.0 ** (-Ns_all[i + 1] / 2)]
                d = max(abs(series[b][i + 1] - series[b][i]) for b in series)
                steps.append(dict(N=Ns_all[i], N_next=Ns_all[i + 1], delta=d, thr=SIGMA + 2 * sum(errs)))
            fits = {}
            for b, F in series.items():
                if len(Ns_all) < 4:
                    continue
                Finf, c, rms1 = fit_inv_n(Ns_all, F)
                Finf_l, c_l, rms_l = fit_inv_n(Ns_all[-3:], F[-3:])
                e = fit_exp(Ns_all, F)
                fits[b] = dict(F=F, invN_all=dict(Finf=Finf, c=c, rms=rms1, N_sigma=abs(c) / SIGMA),
                               invN_last3=dict(Finf=Finf_l, c=c_l, rms=rms_l, N_sigma=abs(c_l) / SIGMA),
                               exp_all=dict(Finf=e[0], A=e[1], xi=e[2], rms=e[3],
                                            N_sigma=(e[2] * math.log(abs(e[1]) / SIGMA) if abs(e[1]) > SIGMA else 0.0)),
                               step_criterion_N_under_invN=math.sqrt(2 * abs(c_l) / (SIGMA + 2 * (2 ** -10 + 2 ** -11))))
            conv[key] = dict(Ns=Ns_all, steps=steps, fits=fits)
    out["convergence"] = conv
    # pre-registered statistic with what exists
    pre = {}
    for p in (19, 245):
        d18 = {t: [s for s in conv[f"p{p}_t{t}"]["steps"] if s["N"] == 18] for t in (160, 320)}
        pre[f"p{p}"] = {f"t{t}": (dict(delta18=v[0]["delta"], thr=v[0]["thr"], above_thr=v[0]["delta"] > v[0]["thr"],
                                         above_3sigma=v[0]["delta"] > 3 * SIGMA) if v else "not measured")
                        for t, v in d18.items()}
    out["preregistered_delta18"] = pre
    json.dump(out, open(os.path.join(HERE, "reach_summary.json.tmp"), "w"), indent=1)
    os.replace(os.path.join(HERE, "reach_summary.json.tmp"), os.path.join(HERE, "reach_summary.json"))
    # console summary
    print(json.dumps(out["validation"], indent=0)[:1500])
    print("frontier", json.dumps(out["frontier"], indent=0))
    for r in rows:
        if r["N"] in (18, 20, 22, 24, 26, 28, 30, 32, 36, 40, 44, 48):
            print(f"N={r['N']:2d} cpu-core-h/curve {r['cpu_core_hours_per_curve'][0]:.3g}-{r['cpu_core_hours_per_curve'][1]:.3g}  "
                  f"mem(sector,3vec) {r['mem_GB_sector_3vec']:.3g} GB  mem(full,8vec) {r['mem_GB_full_8vec']:.3g} GB  "
                  f"GPU-h/curve {r['gpu_hours_per_curve_at_2TBps']:.3g}")
    print("measured N20", meas)
    for k, v in conv.items():
        print(k, "Ns", v["Ns"], "steps", [(s["N"], round(s["delta"], 4)) for s in v["steps"]])
        for b, f in v["fits"].items():
            print(f"   site {b}: F {[round(x, 4) for x in f['F']]}  1/N(all): Finf {f['invN_all']['Finf']:.3f} c {f['invN_all']['c']:.2f} "
                  f"rms {f['invN_all']['rms']:.3f} N_sig {f['invN_all']['N_sigma']:.0f} | 1/N(last3): Finf {f['invN_last3']['Finf']:.3f} "
                  f"c {f['invN_last3']['c']:.2f} N_sig {f['invN_last3']['N_sigma']:.0f} | exp: Finf {f['exp_all']['Finf']:.3f} "
                  f"xi {f['exp_all']['xi']:.1f} rms {f['exp_all']['rms']:.3f} N_sig {f['exp_all']['N_sigma']:.0f} | step-crit N {f['step_criterion_N_under_invN']:.0f}")
    print("pre-registered", json.dumps(pre))


if __name__ == "__main__":
    main()
