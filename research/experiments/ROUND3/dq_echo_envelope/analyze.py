"""R1-DQ inside the physical reversal envelope: analysis (pure re-analysis of out/*.json; seconds of CPU).

Inputs
  out/fi_<pdb>_p<probe>.json      exact S, F1 and FD Jacobians, secular (0-320 us) and physical DQ (0-300 us), 10 us grid
  out/adv_<pdb>_p<probe>_dq_eps*.json   sparse-Pauli adversary on the DQ echo (failure times)
  out/kgrowth_*.json              operator size K(t) (mean Pauli weight) at N = 30
  secular adversary failure times (MEASURED earlier, read from the files named in SEC_TC below)

Model: the measured echo is A_H(t) * F1(t) with a structure-independent reversal envelope of the Hamiltonian H that
generates it and fixed per-point noise sigma -> per-time-point FI x A_H(t)^2 (R1_physics_feasibility convention).
t = forward evolution time, which is how the literature T3 is defined (the LE is plotted against the forward time).
Secular transfer S needs no reversal: undamped.  DQ transfer S is produced by the same imperfect DQ pulse sequence:
damped by A_DQ in the 'literal' variant, undamped in 'generous'.

Envelopes
  T2-scaled (literature anchors, T2 = 1/sqrt(M2) Van Vleck):
    XXZ/secular:  PE  Gaussian, T3 = 4 T2 (local polarization echo, Sanchez 2022)
                  LE  logistic, T3 = 6.7 T2, tail 0.25 T3 (Sanchez, Chattah & Pastawski PRA 105, 052232 (2022))
    DQ:           LIT logistic, T3 = 12.5 T2, tail 0.23 T3: adamantane DQ Loschmidt echo t_c = 545 +- 2 us, tail
                  123 +- 2 us (Rufeil-Fiori et al. PRA 79, 032324 (2009), arXiv:0810.1722, full text) divided by the
                  adamantane T2 = 1/23.0 ms^-1 = 43.5 us (Sanchez 2022 Fig. 5 slope at k = 1; INFERENCE that k = 1 is
                  the natural dipolar T2).  Global (all-spin) echo.
                  LOCAL  logistic, T3 = 7.5 T2 (= 12.5 x 4/6.7: the XXZ local/global T3 ratio transferred; INFERENCE)
                  ASXXZ  DQ with the XXZ anchors (PE 4, LE 6.7) on the local-equal clock, and x1.5 on the global clock
    T2 choices: cluster (isolated N = 10 model; longest, most generous), network (whole static 1H network),
                rotoravg (methyl/NH3 rotor-averaged network; physical).
  K(t)-dependent (Dominguez et al. PRA 104, 012402 (2021): Gamma(t) = Gamma_1 K(t)^alpha, alpha = 0.48 weak / 0.96
    strong perturbation): A(t) = exp(-Gamma_1 int_0^t K^alpha).  K(t) = N = 30 mean Pauli weight while the kept norm^2
    >= 0.9, then extrapolated (exponential at the last reliable log-slope = fast; linear = slow).  Gamma_1 calibrated
    per Hamiltonian by (i) the T2 anchors above (A(c T2) = 1/2) or (ii) a K-horizon: A = 1/2 when K reaches K3
    (XXZ 1e2, DQ 1e3 / 1e4; Sanchez 2022: the DQ echo 'only fades away after reaching 1e4 entangled spins ... largely
    exceeds the 1e2 of the dipolar case').  MQC-K vs Pauli-weight-K differ by an O(1) factor (Alvarez & Suter 2011).

Gains ('joint', classically usable data = everything a classical forward model reproduces at the given adversary):
  classical set = sec S (all t) + sec F1 (t < tc_sec) + DQ S (t < tc_dqS) + DQ F1 (t < tc_dq), each x its envelope^2
  quantum   set = classical + sec F1 (t >= tc_sec) + DQ F1 (t >= tc_dq) (x envelope^2)
  g_par = (CRB_cl / CRB_q)^2 per parameter (median reported over all params and over 'physical' params, i.e.
  excluding radial moves of single methyl protons); g_max = largest generalised eigenvalue; g_trace = tr Fq / tr Fcl.
Output: analysis.json, printed summary.
"""
from __future__ import annotations

import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SIG = 0.01
PROBES = [("1UBQ", 19), ("1UBQ", 245), ("1PGA", 390)]

# secular echo failure times (us) of the sparse-Pauli adversary on the SAME clusters/butterflies (MEASURED earlier):
#   eps 1e-4: first failure at 80 us on the 20 us grid (RAW nmr_gate 1UBQ_p19 / 1PGA_p390 best_t_c_otoc_index = 4;
#             RAW nmr_sparse 1UBQ_p245 eps-ladder) -> 80 us (conservative for the secular hard window: true value in (60,80])
#   eps 3e-5: never within 320 us (R1_replicate/pauli_eps3e-05_pair.json [p19], RAW nmr_sparse/1UBQ_p245 [p245],
#             R1_replicate/other_1PGA_p390_N10_o0_g0_eps3e-05.json [p390])
SEC_TC = {"1e-4": 80.0, "3e-5": None, "1e-5": None}
METHYL = {"radial_HG22/ILE3", "radial_HG21/THR53"}          # single methyl-proton radial moves (non-physical, R1 flaw 2)


def env_gauss(x, c):
    return np.exp(-math.log(2) * (x / c) ** 2)


def env_logistic(x, c, lam_frac):
    l = lam_frac * c
    return (1 + math.exp(-c / l)) / (1 + np.exp((x - c) / l))


def fisher(J, w):
    """J (np, nt, nb), w (nt,) -> sum_t w_t J_t J_t^T / sigma^2."""
    Jw = J * np.sqrt(w)[None, :, None]
    Jf = Jw.reshape(len(J), -1)
    return Jf @ Jf.T / SIG ** 2


def crb(F):
    Fr = F + 1e-12 * max(np.trace(F), 1e-30) * np.eye(len(F))
    return np.sqrt(np.clip(np.diag(np.linalg.inv(Fr)), 0, None))


def gen_max(Fq, Fc):
    A = Fc + 1e-9 * max(np.trace(Fq), 1e-30) * np.eye(len(Fc))
    Li = np.linalg.inv(np.linalg.cholesky(A))
    return float(np.linalg.eigvalsh(Li @ Fq @ Li.T).max())


def load_tc(pdb, probe, eps):
    f = os.path.join(OUT, f"adv_{pdb}_p{probe}_dq_eps{eps}.json")
    st = json.load(open(f))
    recs = st["records"]
    fails = [r["t_us"] for r in recs if r["fail_F1"]]
    failS = [r["t_us"] for r in recs if r["fail_S"]]
    return dict(tc_us=(fails[0] if fails else None), censored=(not fails), last_verified_us=recs[-1]["t_us"],
                tcS_us=(failS[0] if failS else None), cpu_s=st["cpu_s"], done=st["done_reason"],
                max_bias_F1=max(min(r["bias_F1_plain"], r["bias_F1_normcorr"]) for r in recs),
                strings_at_end=recs[-1]["n_strings"], mean_weight_end=recs[-1]["mean_weight"])


def tc_index(t, tc_us, censored_last=None):
    """first index with t >= tc; tc None -> never (len); censored -> hard begins after the last verified time."""
    if tc_us is None:
        if censored_last is None:
            return len(t)
        return int(np.searchsorted(t, censored_last + 1e-6))
    return int(np.searchsorted(t, tc_us - 1e-6))


# ------------------------------------------------------------------------------------------ K(t) model
def load_K(pdb, probe, ham):
    f = os.path.join(OUT, f"kgrowth_{pdb}_p{probe}_{ham}_N30.json")
    if not os.path.exists(f):
        return None
    d = json.load(open(f))
    t = np.array([r["t_us"] for r in d["records"]]); K = np.array([r["mean_weight"] for r in d["records"]])
    n2 = np.array([r["kept_norm2"] for r in d["records"]])
    ok = n2 >= 0.9
    return dict(t=t[ok], K=K[ok], t_all=t, K_all=K, n2=n2)


def K_of_t(kd, tq, mode):
    t, K = kd["t"], kd["K"]
    out = np.interp(tq, t, K)
    tl = t[-1]
    after = tq > tl
    if after.any():
        if mode == "exp":
            s = (math.log(K[-1]) - math.log(K[-3])) / (t[-1] - t[-3])
            out[after] = K[-1] * np.exp(s * (tq[after] - tl))
        else:
            s = (K[-1] - K[-3]) / (t[-1] - t[-3])
            out[after] = K[-1] + s * (tq[after] - tl)
    return out


def env_K(tq, kd, alpha, mode, anchor):
    """A(t) = exp(-G1 int K^alpha); anchor = ('t', t_half_us) or ('K', K3)."""
    tf = np.linspace(0, max(tq.max(), 1.0) * 4, 4001)
    Kf = K_of_t(kd, tf, mode)
    I = np.concatenate([[0], np.cumsum(0.5 * (Kf[1:] ** alpha + Kf[:-1] ** alpha) * np.diff(tf))])
    if anchor[0] == "t":
        th = anchor[1]
    else:
        idx = np.nonzero(Kf >= anchor[1])[0]
        if not len(idx):
            # extend: K never reaches K3 inside the grid -> use last point (generous)
            th = tf[-1]
        else:
            th = tf[idx[0]]
    Ih = np.interp(th, tf, I)
    G1 = math.log(2) / max(Ih, 1e-300)
    return np.exp(-G1 * np.interp(tq, tf, I)), dict(t_half_us=float(th))


# ------------------------------------------------------------------------------------------ gains
def gains(fi, A_sec, A_dq, tcs, tcd, dqS_damped=True, params_mask=None):
    Js_S = np.array(fi["sec"]["J_S"]); Js_F = np.array(fi["sec"]["J_F1"])
    Jd_S = np.array(fi["dq"]["J_S"]); Jd_F = np.array(fi["dq"]["J_F1"])
    ts = np.array(fi["sec"]["times_us"]); td = np.array(fi["dq"]["times_us"])
    ws, wd = A_sec ** 2, A_dq ** 2
    one_s = np.ones_like(ts); one_d = np.ones_like(td)
    m_s_easy = (np.arange(len(ts)) < tcs).astype(float); m_d_easy = (np.arange(len(td)) < tcd).astype(float)
    FsS = fisher(Js_S, one_s)
    FdS = fisher(Jd_S, wd if dqS_damped else one_d)
    Fs_e = fisher(Js_F, ws * m_s_easy); Fs_h = fisher(Js_F, ws * (1 - m_s_easy))
    Fd_e = fisher(Jd_F, wd * m_d_easy); Fd_h = fisher(Jd_F, wd * (1 - m_d_easy))
    Fcl = FsS + FdS + Fs_e + Fd_e
    Fq = Fcl + Fs_h + Fd_h
    # DQ-only accounting (no secular data on either side)
    Fcl_dq = FdS + Fd_e; Fq_dq = Fcl_dq + Fd_h
    cq, cc = crb(Fq), crb(Fcl)
    gp = (cc / np.maximum(cq, 1e-300)) ** 2
    names = [p["name"] for p in fi["params"]]
    phys = [i for i, n in enumerate(names) if n not in METHYL]
    gp_dq = (crb(Fcl_dq) / np.maximum(crb(Fq_dq), 1e-300)) ** 2
    return dict(g_par=gp.tolist(), g_med=float(np.median(gp)), g_med_phys=float(np.median(gp[phys])),
                g_max=gen_max(Fq, Fcl), g_trace=float(np.trace(Fq) / np.trace(Fcl)),
                g_med_dqonly=float(np.median(gp_dq)), g_max_dqonly=gen_max(Fq_dq, Fcl_dq),
                FI_dq_hard_tr=float(np.trace(Fd_h)), FI_sec_hard_tr=float(np.trace(Fs_h)),
                FI_dq_easy_tr=float(np.trace(Fd_e)), FI_sec_easy_tr=float(np.trace(Fs_e)),
                FI_secS_tr=float(np.trace(FsS)), FI_dqS_tr=float(np.trace(FdS)),
                CRB_q_A=cq.tolist(), CRB_cl_A=cc.tolist())


def main():
    res = dict(jobs={}, notes={})
    for pdb, probe in PROBES:
        fi = json.load(open(os.path.join(OUT, f"fi_{pdb}_p{probe}.json")))
        ts = np.array(fi["sec"]["times_us"]); td = np.array(fi["dq"]["times_us"])
        T2 = fi["T2"]
        adv = {e: load_tc(pdb, probe, e) for e in ("0.0001", "3e-05", "1e-05")
               if os.path.exists(os.path.join(OUT, f"adv_{pdb}_p{probe}_dq_eps{e}.json"))}
        job = dict(params=[p["name"] for p in fi["params"]], T2=T2, adv_dq=adv, cases={}, required={}, kmodel={})
        # adversary failure indices
        TC = {}
        for lab, e in (("1e-4", "0.0001"), ("3e-5", "3e-05"), ("1e-5", "1e-05")):
            if e not in adv:
                continue
            a = adv[e]
            tcd = tc_index(td, a["tc_us"], a["last_verified_us"] if a["censored"] else None)
            tcs = tc_index(ts, SEC_TC[lab])
            TC[lab] = (tcs, tcd)
        job["tc_index"] = {k: dict(sec=int(v[0]), dq=int(v[1]), sec_us=(float(ts[v[0]]) if v[0] < len(ts) else None),
                                   dq_us=(float(td[v[1]]) if v[1] < len(td) else None)) for k, v in TC.items()}
        # ideal (no envelope)
        for lab in TC:
            job["cases"][f"ideal|{lab}"] = gains(fi, np.ones_like(ts), np.ones_like(td), *TC[lab])
        # T2-scaled envelopes
        for T2n in ("cluster", "network", "rotoravg"):
            T2v = T2[f"T2_{T2n}_us"]
            xs, xd = ts / T2v, td / T2v
            SEC_ENVS = {"PE4": env_gauss(xs, 4.0), "LE6.7": env_logistic(xs, 6.7, 0.25)}
            DQ_ENVS = {"LIT12.5": env_logistic(xd, 12.5, 0.23), "LOCAL7.5": env_logistic(xd, 7.5, 0.23),
                       "ASXXZ_LE6.7": env_logistic(xd, 6.7, 0.25), "ASXXZ_LE6.7x1.5": env_logistic(xd, 6.7 * 1.5, 0.25),
                       "ASXXZ_PE4": env_gauss(xd, 4.0)}
            for sname, As in SEC_ENVS.items():
                for dname, Ad in DQ_ENVS.items():
                    for lab in TC:
                        for dqS in (True, False):
                            key = f"{T2n}|sec:{sname}|dq:{dname}|{lab}|dqS_{'damped' if dqS else 'free'}"
                            job["cases"][key] = gains(fi, As, Ad, *TC[lab], dqS_damped=dqS)
            # required DQ T3/T2 (logistic, tail 0.23) for joint g_med >= 2 and g_max >= 2 (sec envelope LE6.7, generous)
            for lab in TC:
                for metric in ("g_med", "g_max"):
                    def g(c):
                        return gains(fi, SEC_ENVS["LE6.7"], env_logistic(xd, c, 0.23), *TC[lab], dqS_damped=False)[metric]
                    if g(1e3) < 2:
                        rc = None
                    else:
                        lo, hi = 1.0, 1e3
                        for _ in range(50):
                            mid = math.sqrt(lo * hi)
                            if g(mid) >= 2:
                                hi = mid
                            else:
                                lo = mid
                        rc = hi
                    job["required"][f"{T2n}|{lab}|{metric}>=2"] = rc
        # K(t)-dependent model (probes with K growth data)
        kd = {h: load_K(pdb, probe, h) for h in ("sec", "dq")}
        if kd["sec"] is not None and kd["dq"] is not None:
            T2v = T2["T2_rotoravg_us"]
            job["kmodel"]["K_reliable_until_us"] = {h: float(kd[h]["t"][-1]) for h in kd}
            job["kmodel"]["K_at"] = {h: {str(int(tt)): float(K_of_t(kd[h], np.array([tt]), "exp")[0])
                                         for tt in (40, 80, 120, 160, 200)} for h in kd}
            for alpha in (0.48, 0.96):
                for mode in ("exp", "lin"):
                    anchors_sec = {"T2:LE6.7": ("t", 6.7 * T2v), "T2:PE4": ("t", 4.0 * T2v), "K3=1e2": ("K", 1e2)}
                    anchors_dq = {"T2:LIT12.5": ("t", 12.5 * T2v), "T2:LOCAL7.5": ("t", 7.5 * T2v),
                                  "K3=1e3": ("K", 1e3), "K3=1e4": ("K", 1e4)}
                    for sa, sanc in anchors_sec.items():
                        As, ms = env_K(ts, kd["sec"], alpha, mode, sanc)
                        for da, danc in anchors_dq.items():
                            Ad, md = env_K(td, kd["dq"], alpha, mode, danc)
                            for lab in TC:
                                key = f"a{alpha}|{mode}|sec:{sa}|dq:{da}|{lab}"
                                gg = gains(fi, As, Ad, *TC[lab], dqS_damped=False)
                                gg.update(sec_t_half_us=ms["t_half_us"], dq_t_half_us=md["t_half_us"],
                                          A_dq_at_tc=(float(Ad[TC[lab][1]]) if TC[lab][1] < len(td) else None))
                                job["kmodel"][key] = gg
        # decisive table: strongest available adversary, main envelopes (secular LE 6.7 x T2, DQS free = generous)
        strongest = [l for l in ("1e-5", "3e-5", "1e-4") if l in TC][0]
        dec = {}
        for lab in TC:
            row = {"ideal": job["cases"][f"ideal|{lab}"]}
            for T2n in ("cluster", "rotoravg", "network"):
                row[f"LIT12.5@{T2n}"] = job["cases"][f"{T2n}|sec:LE6.7|dq:LIT12.5|{lab}|dqS_free"]
            kk = f"a0.48|exp|sec:T2:LE6.7|dq:K3=1e4|{lab}"
            if kk in job["kmodel"]:
                row["Kmodel_K3=1e4"] = job["kmodel"][kk]
            dec[lab] = {k: dict(g_med=v["g_med"], g_med_phys=v["g_med_phys"], g_max=v["g_max"], g_trace=v["g_trace"],
                                FI_dq_hard=v["FI_dq_hard_tr"], FI_sec_hard=v["FI_sec_hard_tr"],
                                frac_dq_hard_retained=v["FI_dq_hard_tr"] / max(job["cases"][f"ideal|{lab}"]["FI_dq_hard_tr"], 1e-300))
                        for k, v in row.items()}
        job["decisive"] = dict(strongest_adversary=strongest, table=dec)
        res["jobs"][f"{pdb}_p{probe}"] = job
    tmp = os.path.join(HERE, "analysis.json.tmp")
    json.dump(res, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "analysis.json"))

    # ---------------------------------------------------------------- printed summary
    for jn, job in res["jobs"].items():
        print("=" * 100)
        print(jn, "params", job["params"])
        print(" T2 (us): cluster %.1f network %.1f rotoravg %.1f" % (job["T2"]["T2_cluster_us"], job["T2"]["T2_network_us"],
                                                                  job["T2"]["T2_rotoravg_us"]))
        for e, a in job["adv_dq"].items():
            print(f"  DQ adversary eps={e}: first fail {a['tc_us']} us (censored={a['censored']}, verified to "
                  f"{a['last_verified_us']:.0f} us, max bias {a['max_bias_F1']:.4f}), cpu {a['cpu_s']:.0f}s")
        print("  tc idx", job["tc_index"])
        for lab in [l for l in ("1e-4", "3e-5", "1e-5") if f"ideal|{l}" in job["cases"]]:
            c = job["cases"][f"ideal|{lab}"]
            print(f"  IDEAL {lab}: g_med {c['g_med']:.2f} g_med_phys {c['g_med_phys']:.2f} g_max {c['g_max']:.2f} "
                  f"g_tr {c['g_trace']:.2f} | DQ-only g_med {c['g_med_dqonly']:.2f} | FI dq hard {c['FI_dq_hard_tr']:.0f} "
                  f"sec hard {c['FI_sec_hard_tr']:.0f}")
        for T2n in ("cluster", "network", "rotoravg"):
            for lab in [l for l in ("1e-4", "3e-5", "1e-5") if f"ideal|{l}" in job["cases"]]:
                row = []
                for dname in ("LIT12.5", "LOCAL7.5", "ASXXZ_LE6.7", "ASXXZ_LE6.7x1.5"):
                    c = job["cases"][f"{T2n}|sec:LE6.7|dq:{dname}|{lab}|dqS_free"]
                    row.append(f"{dname}: dqH {c['FI_dq_hard_tr']:.0f} secH {c['FI_sec_hard_tr']:.0f} "
                               f"g {c['g_med']:.2f}/{c['g_max']:.2f}")
                print(f"  {T2n:8s} {lab}: " + " | ".join(row))
            print(f"  {T2n:8s} required DQ T3/T2:", {k.split('|', 1)[1]: (None if v is None else round(v, 1))
                                                    for k, v in job["required"].items() if k.startswith(T2n)})
        if job["kmodel"]:
            print("  K model: reliable until", job["kmodel"]["K_reliable_until_us"], "K_at(exp)", job["kmodel"]["K_at"])
            for key, c in job["kmodel"].items():
                if not key.startswith("a"):
                    continue
                if "sec:T2:LE6.7" not in key or "|exp|" not in key or "a0.48" not in key:
                    continue
                print(f"   {key}: tq_half sec {c['sec_t_half_us']:.0f} dq {c['dq_t_half_us']:.0f} A_dq(tc) "
                      f"{c['A_dq_at_tc']} dqH {c['FI_dq_hard_tr']:.0f} g_med {c['g_med']:.2f} g_max {c['g_max']:.2f}")


    print("=" * 100)
    print("DECISIVE (joint gain over classically usable data; secular LE 6.7 T2 envelope; DQ S undamped):")
    for jn, job in res["jobs"].items():
        for lab, row in job["decisive"]["table"].items():
            print(f"  {jn:10s} eps {lab}: " + " | ".join(
                f"{k}: g_med {v['g_med']:.2f} g_max {v['g_max']:.2f} ret {v['frac_dq_hard_retained']:.3f}"
                for k, v in row.items()))


if __name__ == "__main__":
    main()
