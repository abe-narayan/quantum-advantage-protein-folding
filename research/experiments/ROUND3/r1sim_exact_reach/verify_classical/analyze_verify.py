"""Combine: reference F ladders (N = 12..18, governor/reference script), lane N = 20 F points, exact H/floor ladders
(decomp_echo honly runs), CSD H on large clusters (csd_hydro runs) -> verify_summary.json.

Adversary estimator (INFERENCE-level method, all ingredients MEASURED):
    F_inf(t) ~= H_inf(t) + X_Nmax(t),   X_N = F_N - H_N - floor_N,
    H_inf from classical spin dynamics on N_c >> N (validated against exact H_N at N = 12..20),
    valid for series whose X ladder has flattened (last step |dX| <= tol); shell-event series are flagged."""
import glob
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REF = os.path.join(HERE, "..", "..", "..", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
LANE = os.path.join(HERE, "..", "runs")
TIMES = [40, 80, 120, 160, 200, 240, 280, 320]


def load_H(p, N):
    f = glob.glob(os.path.join(HERE, "runs", f"1UBQ_p{p}_N{N}_probe_honly_*.json"))
    if not f:
        return None
    d = json.load(open(f[0]))
    return dict(H=np.array(d["H"]), floor=np.array(d["floor"]), G=np.array(d["G"]), sumG=d["sumG"][0])


def load_F(p, N):
    """dict t_us -> {b: F}"""
    out = {}
    if N <= 18:
        d = json.load(open(os.path.join(REF, f"1UBQ_p{p}_N{N}.json")))
        for i, t in enumerate(d["times_us"]):
            if round(t) in TIMES:
                out[round(t)] = {b: d["F"][b][i] for b in d["F"]}
        return out
    for f in glob.glob(os.path.join(LANE, f"1UBQ_p{p}_N{N}_flip_*.json*")):
        if f.endswith(".npz"):
            continue
        d = json.load(open(f))
        if "times_us" in d and isinstance(next(iter(d["F"].values())), list):
            for i, t in enumerate(d["times_us"]):
                if round(t) in TIMES:
                    out[round(t)] = {b: d["F"][b][i] for b in d["F"]}
        else:                                       # union checkpoint: F[b][step]
            for b, v in d["F"].items():
                for s, val in v.items():
                    t = 2 * int(s)
                    if t in TIMES:
                        out.setdefault(t, {})[b] = val
    return out


def load_csd(p):
    res = {}
    for f in glob.glob(os.path.join(HERE, "runs", f"csd_1UBQ_p{p}_Nc*_M*_h*.json")):
        if f.endswith(".ckpt.json") or "custom" in f:
            continue
        d = json.load(open(f))
        res.setdefault(d["Nc"], []).append(d)
    out = {}
    for Nc, ds in res.items():
        d = max(ds, key=lambda z: z["M_done"])
        idx = [d["times_us"].index(t) for t in TIMES if t in d["times_us"]]
        out[Nc] = dict(H=np.array(d["H_unbiased"])[idx], se=np.array(d["H_se_est"])[idx], M=d["M_done"],
                       cpu=d["cpu_secs"])
    return out


def main():
    summ = dict(times_us=TIMES)
    for p in (19, 245):
        Ns = [N for N in (12, 14, 16, 18, 20) if load_H(p, N) is not None]
        HL = {N: load_H(p, N) for N in Ns}
        FL = {N: load_F(p, N) for N in Ns}
        csd = load_csd(p)
        block = dict(Ns=Ns, H={N: HL[N]["H"].tolist() for N in Ns}, floor={N: HL[N]["floor"].tolist() for N in Ns},
                     csd={Nc: dict(H=v["H"].tolist(), se=v["se"].tolist(), M=v["M"], cpu_s=v["cpu"])
                          for Nc, v in sorted(csd.items())})
        # CSD validation at matching N
        val = {}
        for N in Ns:
            if N in csd:
                val[N] = dict(maxabs_t160_320=float(np.max(np.abs(csd[N]["H"][3:] - HL[N]["H"][3:]))),
                              diff=(csd[N]["H"] - HL[N]["H"]).tolist())
        block["csd_vs_exact_H"] = val
        series = {}
        for ti, t in enumerate(TIMES):
            for b in ("1", "7", "8", "9"):
                Fs, Xs, HFs = [], [], []
                for N in Ns:
                    if t in FL[N] and b in FL[N][t]:
                        F = FL[N][t][b]
                        Fs.append((N, F)); Xs.append((N, F - HL[N]["H"][ti] - HL[N]["floor"][ti]))
                if len(Xs) < 3:
                    continue
                dF = [Fs[i + 1][1] - Fs[i][1] for i in range(len(Fs) - 1)]
                dX = [Xs[i + 1][1] - Xs[i][1] for i in range(len(Xs) - 1)]
                series[f"t{t}_b{b}"] = dict(N=[n for n, _ in Fs], F=[round(f, 4) for _, f in Fs],
                                            X=[round(x, 4) for _, x in Xs], dF=[round(x, 4) for x in dF],
                                            dX=[round(x, 4) for x in dX])
        block["series"] = series
        summ[f"p{p}"] = block
    # hybrid adversary estimate: H_inf = mean CSD H over the largest clusters (N_c >= 80) + quantum offset at N = 20
    lane_fits = json.load(open(os.path.join(HERE, "..", "reach_summary.json")))["convergence"]
    for p in (19, 245):
        B = summ[f"p{p}"]
        csd = {int(k): v for k, v in B["csd"].items()}
        big = [Nc for Nc in csd if Nc >= 80]
        Hbig = np.mean([csd[Nc]["H"] for Nc in big], axis=0)
        sebig = np.sqrt(np.sum([np.array(csd[Nc]["se"]) ** 2 for Nc in big], axis=0)) / len(big)
        Nq = max(N for N in B["csd_vs_exact_H"])
        dq = -np.array(B["csd_vs_exact_H"][Nq]["diff"])            # exact - CSD at N = Nq
        Hinf = Hbig + dq
        B["H_inf"] = dict(csd_clusters=big, H_csd_big=Hbig.tolist(), quantum_offset_N=Nq, offset=dq.tolist(),
                          H_inf=Hinf.tolist(), se=sebig.tolist(),
                          sys_note="CSD-vs-exact offset at N<=20 is 0.002-0.012; N_c 80 vs 160 agree within noise")
        est = {}
        for key, v in B["series"].items():
            t = int(key[1:key.index("_")]); b = key.split("_b")[1]
            ti = TIMES.index(t)
            if len(v["X"]) < 3:
                continue
            X_last = v["X"][-1]; dX_last = abs(v["dX"][-1]); dF_last = abs(v["dF"][-1])
            e = dict(N_last=v["N"][-1], F_last=v["F"][-1], X_last=X_last, dX_last=dX_last, dF_last=dF_last,
                     H_last=float(B["H"][v["N"][-1]][ti]), floor_last=float(B["floor"][v["N"][-1]][ti]),
                     F_inf_hybrid=round(float(Hinf[ti]) + X_last, 4),
                     X_flat=bool(dX_last <= 0.006 and (len(v["dX"]) < 2 or abs(v["dX"][-2]) <= 0.01)))
            lk = f"p{p}_t{t}"
            if lk in lane_fits and b in lane_fits[lk]["fits"]:
                lf = lane_fits[lk]["fits"][b]
                e["lane_Finf"] = {m: round(lf[m]["Finf"], 3) for m in ("invN_all", "invN_last3", "exp_all")}
                e["lane_Nsigma"] = {m: round(lf[m]["N_sigma"], 1) for m in ("invN_all", "invN_last3", "exp_all")}
            est[key] = e
        B["hybrid_estimates"] = est
    json.dump(summ, open(os.path.join(HERE, "verify_summary.json"), "w"), indent=1)
    for p in (19, 245):
        B = summ[f"p{p}"]
        print(f"== probe {p}")
        for k, v in B["series"].items():
            if k.startswith(("t160", "t240", "t320")):
                print(f"  {k:10s} N={v['N']} F={v['F']} dF={v['dF']}\n{'':12s} X={v['X']} dX={v['dX']}")
        print("  CSD vs exact H (t>=160):", {N: round(v["maxabs_t160_320"], 4) for N, v in B["csd_vs_exact_H"].items()})
        for Nc, v in B["csd"].items():
            print(f"  CSD Nc={Nc} M={v['M']} H={np.round(v['H'], 4)} se~{np.round(v['se'][-1], 4)}")
        print("  H_inf", np.round(B["H_inf"]["H_inf"], 4), "offset", np.round(B["H_inf"]["offset"], 4))
        for k, e in B["hybrid_estimates"].items():
            if k.startswith(("t160", "t240", "t320")):
                print(f"  {k:9s} N{e['N_last']} F={e['F_last']:.3f} X={e['X_last']:.3f} dX={e['dX_last']:.3f} dF={e['dF_last']:.3f} "
                      f"flat={e['X_flat']} F_inf_hyb={e['F_inf_hybrid']:.3f} lane={e.get('lane_Finf')} Nsig={e.get('lane_Nsigma')}")


if __name__ == "__main__":
    main()
