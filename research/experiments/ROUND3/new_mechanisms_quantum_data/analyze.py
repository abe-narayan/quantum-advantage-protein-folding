"""Analyse out/*.json from qd_fisher.py -> summary.json (+ printed tables).

Per copy of rho (per molecule-experiment), per structural parameter (diagonal FI, 1/A^2):
  QFI            = optimal single-copy measurement = optimal collective (quantum-memory) measurement, one parameter
  Bell (memory)  = two-copy Bell sampling per copy (FI per pair / 2)
  local shadows  = random local Pauli bases;  Zbasis = all-spin computational basis;  mag = site-resolved <Z_k>
  echo           = single-copy time-reversal echo, best butterfly Z_b
  Clifford       = random global 2-design measurement = QFI/(d+1)
"""
import glob
import json
import math
import os

import numpy as np
from scipy.optimize import minimize

HERE = os.path.dirname(os.path.abspath(__file__))
P_THERMAL = 4.8e-5          # 1H, 14.1 T (600 MHz), 298 K: tanh(hbar gamma B / 2kT)  (DERIVED from constants)


def thermal_p(B, T):
    hbar, kB, gH = 1.054571817e-34, 1.380649e-23, 2.6752218744e8
    return math.tanh(hbar * gH * B / (2 * kB * T))


def best_split(Fs, GQ):
    """min over allocation f in simplex of tr((sum f_i F_i)^-1) / tr(GQ^-1)."""
    k = len(Fs)
    trQ = np.trace(np.linalg.inv(GQ))

    def obj(z):
        f = np.exp(z - z.max())
        f /= f.sum()
        M = sum(fi * Fi for fi, Fi in zip(f, Fs))
        try:
            v = np.trace(np.linalg.inv(M))
        except np.linalg.LinAlgError:
            return 1e30
        return v if np.isfinite(v) and v > 0 else 1e30

    best = None
    rng = np.random.default_rng(0)
    for s in range(12):
        z0 = np.zeros(k) if s == 0 else rng.normal(size=k)
        r = minimize(obj, z0, method="Nelder-Mead", options=dict(maxiter=4000, xatol=1e-6, fatol=1e-10))
        if best is None or r.fun < best.fun:
            best = r
    f = np.exp(best.x - best.x.max())
    f /= f.sum()
    return float(best.fun / trQ), f.tolist()


def main():
    rows = []
    summ = dict(p_thermal_14T_298K=thermal_p(14.1, 298), p_thermal_28T_298K=thermal_p(28.2, 298),
                p_thermal_14T_100K=thermal_p(14.1, 100), p_thermal_9p4T_100K=thermal_p(9.4, 100), jobs={})
    for fj in sorted(glob.glob(os.path.join(HERE, "out", "*.json"))):
        if fj.endswith("partial.json") or fj.endswith(".done.json"):
            continue
        R = json.load(open(fj))
        n, d = R["N"], 2 ** R["N"]
        pn = [p["name"] for p in R["params"]]
        job = dict(N=n, params=pn, max_abs_d_kHz=R["max_abs_d_kHz"], times={})
        for key in sorted(R["per_time"], key=float):
            T = R["per_time"][key]
            GQ = np.array(T["G_Q"])
            qfi = np.diag(GQ)
            gl = np.diag(np.array(T["G_loc"]))
            gz = np.diag(np.array(T["G_Z"]))
            gm = np.diag(np.array(T["G_mag"]))
            gb = {lam: np.diag(np.array(v)) for lam, v in T["G_bell"].items()}
            echo_d = np.array([T["echo"][b]["dF"] for b in T["echo"]]) ** 2      # (n-1, k) leading-order / p^2
            echo_F = np.array([T["echo"][b]["F"] for b in T["echo"]])
            ech = echo_d.max(axis=0)
            le1 = np.diag(np.array(T["loc_exact"]["1"]))
            zb1 = np.diag(np.array(T["zbasis_exact"]["1"]))
            be = T.get("bell_exact", {})
            bell1 = np.diag(np.array(be["1"]["F"], dtype=float)) / 2 if "1" in be else np.full(len(pn), np.nan)
            bell01 = np.diag(np.array(be["0.1"]["F"], dtype=float)) / 2 if "0.1" in be else np.full(len(pn), np.nan)
            # echo exact at p = 1: p^2 dF^2 / (1 - p^2 F^2), best b
            ech1 = (echo_d / np.maximum(1e-300, 1 - echo_F[:, None] ** 2)).max(axis=0)
            wg = np.array(T["wdist_g"])
            wtot = wg.sum(axis=1)
            mean_w = (wg * np.arange(n + 1)).sum(axis=1) / np.maximum(wtot, 1e-300)
            frac_w_le2 = wg[:, :3].sum(axis=1) / np.maximum(wtot, 1e-300)
            frac_w_ge5 = wg[:, 5:].sum(axis=1) / np.maximum(wtot, 1e-300)
            wc = np.array(T["wdist_c"])
            ent = dict(
                QFI_over_p2=qfi.tolist(),
                # ---- ratios to QFI (per copy); Bell leading order is p^2 * G_bell/(2 G_Q)
                bell_over_QFI_lead_coeff=(gb["1"] / 2 / np.maximum(qfi, 1e-300)).tolist(),   # multiply by p^2
                bell_over_QFI_exact_p1=(bell1 / np.maximum(qfi, 1e-300)).tolist(),
                bell_over_QFI_exact_p0p1=(bell01 / np.maximum(qfi * 0.01, 1e-300)).tolist(),
                local_over_QFI_lead=(gl / np.maximum(qfi, 1e-300)).tolist(),
                local_over_QFI_exact_p1=(le1 / np.maximum(qfi, 1e-300)).tolist(),
                zbasis_over_QFI_lead=(gz / np.maximum(qfi, 1e-300)).tolist(),
                zbasis_over_QFI_exact_p1=(zb1 / np.maximum(qfi, 1e-300)).tolist(),
                mag_over_QFI=(gm / np.maximum(qfi, 1e-300)).tolist(),
                echo_best_over_QFI_lead=(ech / np.maximum(qfi, 1e-300)).tolist(),
                echo_best_over_QFI_exact_p1=(ech1 / np.maximum(qfi, 1e-300)).tolist(),
                clifford_over_QFI=1.0 / (d + 1),
                # ---- memory vs restricted single copy
                bell_over_local_exact_p1=(bell1 / np.maximum(le1, 1e-300)).tolist(),
                bell_over_local_thermal=(P_THERMAL ** 2 * gb["1"] / 2 / np.maximum(gl, 1e-300)).tolist(),
                pstar_bell_eq_local_lead=np.sqrt(2 * gl / np.maximum(gb["1"], 1e-300)).tolist(),
                pstar_bell_eq_clifford_lead=np.sqrt(2 * qfi / (d + 1) / np.maximum(gb["1"], 1e-300)).tolist(),
                bell_transduction_over_local_lead_p1={lam: (gb[lam] / 2 / np.maximum(gl, 1e-300)).tolist()
                                                     for lam in gb},
                bell_over_echo_lead_coeff=(gb["1"] / 2 / np.maximum(ech, 1e-300)).tolist(),   # multiply by p^2
                # ---- where the information lives
                mean_weight_info=mean_w.tolist(), frac_info_w_le2=frac_w_le2.tolist(),
                frac_info_w_ge5=frac_w_ge5.tolist(), m90=T["m90"], support=T["support"],
                mean_weight_operator=float((wc * np.arange(n + 1)).sum() / wc.sum()),
                # ---- copies for sigma = 0.1 A on each parameter (single parameter, others known)
                copies_sigma0p1_QFI_thermal=(1 / (0.01 * P_THERMAL ** 2 * np.maximum(qfi, 1e-300))).tolist(),
                copies_sigma0p1_bell_thermal=(1 / (0.01 * P_THERMAL ** 4 * np.maximum(gb["1"] / 2, 1e-300))).tolist(),
                copies_sigma0p1_QFI_p1=(1 / (0.01 * np.maximum(qfi, 1e-300))).tolist(),
                copies_sigma0p1_bell_p1_exact=(1 / (0.01 * np.maximum(bell1, 1e-300))).tolist(),
            )
            # ---- multi-parameter: split-SLD single copy vs SLD bound; Holevo incompatibility
            if float(key) >= 20 and np.linalg.cond(GQ) < 1e10:
                Fs = [np.array(x) for x in T["Fsplit_unit"]]
                ratio, f = best_split(Fs, GQ)
                Dt = np.array(T["Dtilde"])
                Rinc = float(np.max(np.abs(np.linalg.eigvals(np.linalg.solve(GQ, Dt)))))
                ent.update(multi_split_over_SLD=ratio, multi_split_alloc=f, holevo_R_p1=Rinc,
                           multi_k=len(pn),
                           multi_memory_gain_upper_bound=ratio,
                           multi_memory_gain_lower_bound=1.0 / (1.0 + Rinc),
                           sld_basis_max_abs_X=T["sld_basis_max_abs_X"],
                           cond_GQ=float(np.linalg.cond(GQ)))
            # transduction before an ideal coherent (SLD) measurement: per-qubit depolarising shrink lambda,
            # leading-order QFI retained = sum_w lambda^{2w} I(w) / sum_w I(w)
            ent["transduction_QFI_retained"] = {f"{lam:g}": ((wg * lam ** (2.0 * np.arange(n + 1))).sum(axis=1)
                                                            / np.maximum(wtot, 1e-300)).tolist()
                                               for lam in (0.99, 0.95, 0.9, 0.8, 0.5)}
            ent["_echo_leading"] = ech.tolist()
            job["times"][key] = ent
        # echo(t) (2 queries of the dynamics, total evolution 2t) vs state QFI at 2t
        for key, ent in job["times"].items():
            k2 = f"{2 * float(key):g}"
            if k2 in job["times"]:
                q2 = np.array(job["times"][k2]["QFI_over_p2"])
                ent["echo_t_over_QFI_2t"] = (np.array(ent["_echo_leading"]) / np.maximum(q2, 1e-300)).tolist()
        summ["jobs"][R["tag"]] = job
    # ---- aggregate headline numbers
    agg = {}

    def collect(field, tmin=0.0, reduce=np.max):
        vals = []
        for j in summ["jobs"].values():
            for k, e in j["times"].items():
                if float(k) >= tmin and field in e:
                    v = e[field]
                    vals += list(np.ravel(v))
        vals = np.array([x for x in vals if x is not None and np.isfinite(x)])
        return vals

    for field in ("bell_over_QFI_exact_p1", "bell_over_QFI_lead_coeff", "local_over_QFI_exact_p1",
                  "local_over_QFI_lead", "zbasis_over_QFI_lead", "mag_over_QFI", "echo_best_over_QFI_lead",
                  "bell_over_local_exact_p1", "bell_over_local_thermal", "pstar_bell_eq_local_lead",
                  "pstar_bell_eq_clifford_lead", "mean_weight_info", "frac_info_w_le2", "frac_info_w_ge5",
                  "multi_split_over_SLD", "holevo_R_p1", "bell_over_echo_lead_coeff",
                  "copies_sigma0p1_QFI_thermal", "copies_sigma0p1_bell_thermal", "copies_sigma0p1_QFI_p1",
                  "copies_sigma0p1_bell_p1_exact"):
        v = collect(field, tmin=10.0)
        if len(v):
            agg[field] = dict(min=float(v.min()), median=float(np.median(v)), max=float(v.max()), n=int(len(v)))
    for field in ("echo_t_over_QFI_2t",):
        v = collect(field, tmin=10.0)
        if len(v):
            agg[field] = dict(min=float(v.min()), median=float(np.median(v)), max=float(v.max()), n=int(len(v)))
    agg_late = {}
    for field in ("bell_over_QFI_exact_p1", "local_over_QFI_exact_p1", "mag_over_QFI", "echo_best_over_QFI_lead",
                  "echo_t_over_QFI_2t", "bell_over_local_exact_p1", "frac_info_w_ge5", "mean_weight_info"):
        v = collect(field, tmin=80.0)
        if len(v):
            agg_late[field] = dict(min=float(v.min()), median=float(np.median(v)), max=float(v.max()), n=int(len(v)))
    summ["aggregate_t_ge_80us"] = agg_late
    tr = {}
    for lam in ("0.99", "0.95", "0.9", "0.8", "0.5"):
        for tmin, lab in ((10.0, "t>=10"), (80.0, "t>=80")):
            vals = []
            for j in summ["jobs"].values():
                for k, e in j["times"].items():
                    if float(k) >= tmin:
                        vals += e["transduction_QFI_retained"][lam]
            vals = np.array(vals)
            tr[f"lambda={lam},{lab}"] = dict(min=float(vals.min()), median=float(np.median(vals)),
                                             max=float(vals.max()))
    summ["transduction_QFI_retained"] = tr
    # N-scaling: same probe, N = 10 vs N = 12
    scal = {}
    for probe in ("1UBQ_p19", "1UBQ_p245"):
        a10, a12 = summ["jobs"].get(f"{probe}_N10_o0"), summ["jobs"].get(f"{probe}_N12_o0")
        if not (a10 and a12):
            continue
        for key in a12["times"]:
            if key not in a10["times"]:
                continue
            e10, e12 = a10["times"][key], a12["times"][key]
            scal[f"{probe}_t{key}"] = {
                f: dict(N10=float(np.median(e10[f])), N12=float(np.median(e12[f])))
                for f in ("local_over_QFI_exact_p1", "bell_over_QFI_exact_p1", "mag_over_QFI",
                          "echo_best_over_QFI_lead", "mean_weight_info", "frac_info_w_ge5")}
    summ["N_scaling_medians_over_params"] = scal
    summ["aggregate_t_ge_10us"] = agg
    # ---- HKP / Chen-Gong-Ye "predict all Pauli expectations" task: with vs without memory, eps = eta * p
    hkp = []
    for nn in (10, 12, 14, 20, 30, 40, 50):
        for p, lab in ((thermal_p(14.1, 298), "thermal 14.1T/298K"), (thermal_p(28.2, 298), "thermal 28.2T/298K"),
                       (thermal_p(9.4, 100), "thermal 9.4T/100K"), (0.1, "p=0.1"), (1.0, "p=1")):
            eta = 0.1
            eps = eta * p
            n_single = 2 ** nn / eps ** 2                 # Theta~(2^n/eps^2)  [Chen-Gong-Ye 2404.19105, k=0]
            n_mem = nn / eps ** 4                         # O(n/eps^4) Bell sampling [same; HKP 2101.02464]
            hkp.append(dict(n=nn, p=p, label=lab, eta=eta, copies_single=n_single, copies_memory=n_mem,
                            memory_gain=n_single / n_mem))
    summ["hkp_all_pauli_task"] = hkp
    # crossover n* where memory helps: 2^n eps^2 > n
    cross = {}
    for p, lab in ((thermal_p(14.1, 298), "thermal 14.1T/298K"), (thermal_p(9.4, 100), "thermal 9.4T/100K"),
                   (0.01, "p=0.01"), (0.1, "p=0.1"), (1.0, "p=1")):
        for eta in (0.1, 0.01):
            eps = eta * p
            nn = 1
            while 2 ** nn * eps ** 2 <= nn:
                nn += 1
            cross[f"{lab}, eta={eta}"] = nn
    summ["hkp_crossover_n_star"] = cross
    json.dump(summ, open(os.path.join(HERE, "summary.json"), "w"), indent=1)
    # ---- print compact tables
    for tag, j in summ["jobs"].items():
        print(f"\n== {tag}  N={j['N']}  params={j['params']}")
        for k, e in j["times"].items():
            line = (f" t={float(k):5.0f}us QFI/p2={np.round(e['QFI_over_p2'], 3)} "
                    f"Bell/QFI(p=1)={np.round(e['bell_over_QFI_exact_p1'], 3)} "
                    f"loc/QFI(p=1)={np.round(e['local_over_QFI_exact_p1'], 3)} "
                    f"Bell/loc(p=1)={np.round(e['bell_over_local_exact_p1'], 2)} "
                    f"echo/QFI={np.round(e['echo_best_over_QFI_lead'], 3)} "
                    f"<w>={np.round(e['mean_weight_info'], 1)}")
            if "multi_split_over_SLD" in e:
                line += f" split/SLD={e['multi_split_over_SLD']:.2f} R={e['holevo_R_p1']:.3f}"
            print(line)
    def fmt(dd):
        return {k: {kk: (round(vv, 5) if isinstance(vv, float) else vv) for kk, vv in v.items()} for k, v in dd.items()}
    print("\nAGG t>=10", json.dumps(fmt(agg), indent=0))
    print("\nAGG t>=80", json.dumps(fmt(agg_late), indent=0))
    print("\ntransduction", json.dumps(fmt(tr), indent=0))
    print("\nN-scaling", json.dumps(scal, indent=0))
    print("cross", cross)


if __name__ == "__main__":
    main()
