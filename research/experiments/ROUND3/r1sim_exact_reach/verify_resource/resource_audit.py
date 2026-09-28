"""Resource audit of the r1sim_exact_reach claim (ROUND3 adversarial verifier, resource lens).

Claim under attack: exact classical simulation cannot reach the converged late-window (240-320 us) first-order dipolar
echo F_ab(t) of the dense 1UBQ 1H network; exact frontier N ~ 26 (workstation/day) ... <= 48 (exascale/month); spins
needed >= 58 (exponential model) to 300-557 (1/N model).

This script (single-threaded, < 2 min, < 1 GB) does NOT rerun the echo; it
  A. re-derives the lane's classical exact cost model and frontier, and re-evaluates the frontier with corrected
     machine memory/bandwidth and a 2-vector memory variant (INFERENCE on machine specs, tagged);
  B. costs the QUANTUM side of exactly the same task (one echo curve: 1 probe, 1 orientation, 8 times 40..320 us,
     4 observed sites b, sigma = 0.01): fault-tolerant Trotter (reference circuit, dt = 2 us) and a qubitization
     alternative; T-count, T-depth, wall-clock at 1 / 10 / 170 us per T layer, logical qubits, NISQ gate counts;
  C. break-even N* of quantum vs classical exact per platform;
  D. robustness of the spins-needed extrapolation (leave-one-out / subset refits of the lane's own ladder data);
  E. pair-count statistics of the actual 1UBQ couplings (dense vs truncated) at the N the claim says are needed;
  F. a short re-benchmark of the lane's production kernel at N = 20 (central sector, complex64) under current load.
Writes resource_audit.json atomically (tmp + replace) after every section.
Run: OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python resource_audit.py
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
sys.path.insert(0, LANE)
sys.path.insert(0, os.path.join(ROOT, "src"))
OUT = os.path.join(HERE, "resource_audit.json")
SIGMA = 0.01
TIMES_STEPS = [20 * k for k in range(1, 9)]          # 40..320 us at dt = 2 us
V_CURVE, V_RECOMP = 4400, 8000                          # lane: forward-reuse vs recompute-forward vector-steps / curve
T_LAYER = {"1us": 1e-6, "10us": 1e-5, "170us": 1.7e-4}
YR, DAY, HR = 3.156e7, 86400.0, 3600.0
OUTD: dict = {}


def save():
    json.dump(OUTD, open(OUT + ".tmp", "w"), indent=1, default=float)
    os.replace(OUT + ".tmp", OUT)


def D_fold(N):
    return (2 ** N + math.comb(N, N // 2)) / 2 if N % 2 == 0 else 2 ** (N - 1)


def fmt(sec):
    if sec == float("inf"):
        return "infeasible"
    for u, s in (("yr", YR), ("d", DAY), ("h", HR), ("min", 60), ("s", 1)):
        if sec >= s:
            return f"{sec / s:.3g} {u}"
    return f"{sec:.2g} s"


# =============================================================================== A. classical exact frontier
def classical_time(N, plat):
    """seconds per echo curve for the lane's exact method on a platform; inf if memory does not fit."""
    pairs = N * (N - 1) / 2
    nvec = plat.get("nvec", 3)
    # vector-steps per curve: the lane charges 4400 (forward reuse) while sizing memory at 3 vectors (inconsistent,
    # generous to classical); corrected platforms charge 8000 for 3 vectors (recompute forward legs) and 8800 for 2
    # vectors (also regenerate psi per b leg; INFERENCE)
    V = plat.get("V", V_RECOMP if nvec == 3 else V_RECOMP + 800 if nvec == 2 else V_CURVE)
    mem = nvec * math.comb(N, N // 2) * plat.get("bytes_per_amp", 8)
    if mem > plat["mem_B"]:
        return float("inf"), mem
    if plat["kind"] == "cpu":
        t = V * pairs * D_fold(N) / 2 * plat["c_pe"] / plat["cores"]
    else:
        t = V * pairs * D_fold(N) * plat.get("bytes_per_amp", 8) / plat["bw_Bps"] * plat.get("comm", 1.0)
    return t, mem


def section_A():
    lane_plats = {  # the lane's own assumptions (reproduced)
        "lane_workstation_1day": dict(kind="cpu", cores=8, c_pe=16e-9, mem_B=12e9, budget=DAY, nvec=3, V=V_CURVE),
        "lane_1gpu_1day": dict(kind="gpu", bw_Bps=2e12, mem_B=80e9, budget=DAY, nvec=3, V=V_CURVE),
        "lane_8gpu_node_1day": dict(kind="gpu", bw_Bps=8 * 2e12, comm=3, mem_B=640e9, budget=DAY, nvec=3, V=V_CURVE),
        "lane_4096gpu_1week": dict(kind="gpu", bw_Bps=4096 * 2e12, comm=3, mem_B=4096 * 64e9, budget=7 * DAY, nvec=3, V=V_CURVE),
        "lane_exascale_37888x64GB_1month": dict(kind="gpu", bw_Bps=37888 * 2e12, comm=3, mem_B=37888 * 64e9,
                                                budget=30 * DAY, nvec=3, V=V_CURVE),
    }
    # corrected / alternative platforms (INFERENCE: public machine specs from memory, not verified this session)
    alt_plats = {
        "workstation_optimised_kernel_1day (c_pe 2 ns, INFERENCE)": dict(kind="cpu", cores=8, c_pe=2e-9, mem_B=12e9,
                                                                         budget=DAY, nvec=3),
        "workstation_optimised_kernel_1week": dict(kind="cpu", cores=8, c_pe=2e-9, mem_B=12e9, budget=7 * DAY, nvec=3),
        "frontier_class_75264GCD_x64GB_1.6TBps_1month (4.8 PB HBM)": dict(kind="gpu", bw_Bps=75264 * 1.6e12, comm=3,
                                                                          mem_B=75264 * 64e9, budget=30 * DAY, nvec=3),
        "frontier_class_2vec_1month": dict(kind="gpu", bw_Bps=75264 * 1.6e12, comm=3, mem_B=75264 * 64e9,
                                           budget=30 * DAY, nvec=2),
        "aurora_class_63744x128GB_3.2TBps_2vec_1month (8.2 PB HBM)": dict(kind="gpu", bw_Bps=63744 * 3.2e12, comm=3,
                                                                          mem_B=63744 * 128e9, budget=30 * DAY, nvec=2),
        "aurora_class_2vec_3months": dict(kind="gpu", bw_Bps=63744 * 3.2e12, comm=3, mem_B=63744 * 128e9,
                                          budget=90 * DAY, nvec=2),
    }
    res = {}
    for name, p in {**lane_plats, **alt_plats}.items():
        ok = []
        for N in range(16, 61, 2):
            t, mem = classical_time(N, p)
            if t <= p["budget"]:
                ok.append(N)
        Nmax = max(ok) if ok else None
        t_next, mem_next = classical_time((Nmax or 14) + 2, p)
        res[name] = dict(N_max=Nmax, time_at_Nmax=fmt(classical_time(Nmax, p)[0]) if Nmax else None,
                         next_N_time=fmt(t_next), next_N_mem_PB=mem_next / 1e15)
    OUTD["A_classical_frontier"] = dict(
        platforms=res,
        literature="Largest universal state-vector simulation: 50 qubits, JUQCS-50 on JUPITER (GH200), arXiv:2511.03359 "
                   "(abstract verified this session; adaptive data encoding, CPU+GPU memory). The lane cites 45 "
                   "(1704.01127) and 48 (1805.04708) as the records; 50 supersedes them. A 50-qubit full vector holds "
                   "2^50 = 1.13e15 amplitudes; one N = 52 half-filling sector holds C(52,26) = 4.96e14.",
        note="Sector restriction means a machine that holds a 50-qubit full state vector holds 2 sector vectors at N = 52.")
    save()


# =============================================================================== B. quantum cost of the same task
def couplings_stats():
    from fastecho import load_instance  # noqa
    from qapf.nmr import spins as SP
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    from fastecho import random_b0
    out = {}
    for probe in (19, 245):
        for N in (20, 26, 34, 50, 58, 82, 150, 300, 550, 629):
            idx = SP.cluster(xyz, probe, N)
            dm = SP.couplings(xyz[idx], random_b0(1000))
            iu = np.triu_indices(N, 1)
            d = np.abs(dm[iu]) / (2 * math.pi)                    # Hz
            lam = float(np.abs(dm[iu]).sum())                      # rad/s, LCU 1-norm (|d|/2 + |d|/4 + |d|/4 per pair)
            out[f"p{probe}_N{N}"] = dict(pairs_dense=int(len(d)), pairs_gt_10Hz=int((d > 10).sum()),
                                         pairs_gt_30Hz=int((d > 30).sum()), pairs_gt_100Hz=int((d > 100).sum()),
                                         max_Hz=float(d.max()), lambda_rad_s=lam,
                                         radius_A=float(np.linalg.norm(xyz[idx[-1]] - xyz[idx[0]])))
    return out


def q_curve(N, M, t_layer, sampling=True, trotter_mult=1.0, eps_tot=1e-3, shots=None):
    """one echo curve (8 times, 4 sites, 1 probe). Circuit per shot: |z> -> U(t) -> Z_a -> U(t)^dag -> measure all Z.
    All 4 sites b are read from the same shot (estimator z_b m_b), so sampling does NOT multiply by n_b.
    M = pair gates per Trotter step; 3 arbitrary-angle Pauli rotations per pair gate (ZZ, XX, YY)."""
    steps_max = 2 * TIMES_STEPS[-1] * trotter_mult
    rot_max = 3 * M * steps_max
    eps_rot = eps_tot / rot_max
    t_rot = 1.15 * math.log2(1 / eps_rot) + 9.2                # repeat-until-success average T per rotation
    steps_curve = 2 * sum(TIMES_STEPS) * trotter_mult           # sum over the 8 circuits
    if sampling:
        reps = shots if shots else 1 / SIGMA ** 2               # var(z_b m_b) = 1 - F^2 <= 1
        n_obs = 1
        logical = N
    else:                                                       # amplitude estimation, purified max-mixed input
        reps = 2 * math.pi / (2 * SIGMA)
        n_obs = 4
        logical = 2 * N + 10
    T_count = reps * n_obs * steps_curve * 3 * M * t_rot
    colours = N - 1 if M >= N * (N - 1) / 2 - 1e-9 else min(N - 1, 2 * M / N + 1)   # edge colouring (Vizing bound)
    T_depth = reps * n_obs * steps_curve * colours * 3 * t_rot
    return dict(T_per_rotation=t_rot, T_count=T_count, T_depth=T_depth, wall_depth_limited_s=T_depth * t_layer,
                logical_qubits=logical, pair_gates_deepest_circuit=M * steps_max,
                cnot_deepest_circuit=3 * M * steps_max, reps=reps)


def q_qubitization(N, lam, M, eps_tot=1e-3):
    """Toffolis per curve for qubitized evolution (LCU over L = 3M Pauli terms, select+prepare ~ 2L Toffolis per
    query; queries ~ lam*t + log(1/eps) per leg). Sampling, 1e4 shots, all b per shot. Order-of-magnitude only."""
    L = 3 * M
    q_per_curve = sum(2 * (lam * n * 2e-6 + math.log(1 / eps_tot)) for n in TIMES_STEPS)
    return dict(queries_per_shot_curve=q_per_curve, toffoli_per_curve=q_per_curve * 2 * L / SIGMA ** 2)


def section_B(cstats):
    rows = []
    for N in (20, 26, 34, 40, 46, 50, 58, 82, 150, 300, 550, 629):
        key = f"p19_N{N}"
        M_dense = N * (N - 1) / 2
        cs = cstats.get(key)
        M_30 = cs["pairs_gt_30Hz"] if cs else None
        r = dict(N=N, pairs_dense=M_dense, pairs_gt_30Hz=M_30)
        for lab, M in (("dense", M_dense), ("cut30Hz", M_30)):
            if M is None:
                continue
            q = q_curve(N, M, 1e-6)
            qa = q_curve(N, M, 1e-6, sampling=False)
            qt = q_curve(N, M, 1e-6, trotter_mult=4.0)
            r[lab] = dict(T_count_sampling=q["T_count"], T_count_AE=qa["T_count"],
                          T_depth_sampling=q["T_depth"], T_depth_AE=qa["T_depth"],
                          wall_sampling={k: fmt(q["T_depth"] * v) for k, v in T_LAYER.items()},
                          wall_AE={k: fmt(qa["T_depth"] * v) for k, v in T_LAYER.items()},
                          wall_sampling_dt0p5us={k: fmt(qt["T_depth"] * v) for k, v in T_LAYER.items()},
                          wall_sampling_s={k: q["T_depth"] * v for k, v in T_LAYER.items()},
                          logical_qubits_sampling=q["logical_qubits"], logical_qubits_AE=qa["logical_qubits"],
                          cnot_deepest_circuit=q["cnot_deepest_circuit"],
                          nisq_log_fidelity_at_1em3_per_cnot=-1e-3 * q["cnot_deepest_circuit"], nisq_fidelity_at_1em3_per_cnot=math.exp(-1e-3 * q["cnot_deepest_circuit"]))
        if cs:
            r["qubitization_dense_toffoli_per_curve"] = q_qubitization(N, cs["lambda_rad_s"], M_dense)["toffoli_per_curve"]
            r["lambda_t_320us"] = cs["lambda_rad_s"] * 320e-6
        rows.append(r)
    OUTD["B_quantum_cost_per_curve"] = dict(
        task="1 probe (p19 couplings), 1 orientation, 8 times 40..320 us, 4 sites read per shot, sigma = 0.01 "
             "(1e4 shots; AE: pi/sigma reps per site, 2N+10 qubits)",
        model="reference first-order Trotter dt = 2 us (x4 steps for dt = 0.5 us physics accuracy, INFERENCE from the "
              "measured 0.013 Trotter error at N = 12); 3 arbitrary rotations per pair gate; 1.15 log2(1/eps)+9.2 T per "
              "rotation; eps_tot = 1e-3 per circuit; depth-limited wall clock = T-depth x T-layer time, one QPU, "
              "unlimited factories (most favourable to quantum); shots are parallel across QPUs (divide by n_QPU)",
        rows=rows)
    save()


# =============================================================================== C. break-even vs classical exact
def section_C():
    plats = {
        "workstation (lane c_pe 16 ns, 8 cores)": dict(kind="cpu", cores=8, c_pe=16e-9, mem_B=12e9, nvec=3),
        "workstation optimised (2 ns)": dict(kind="cpu", cores=8, c_pe=2e-9, mem_B=12e9, nvec=3),
        "1 GPU 80 GB": dict(kind="gpu", bw_Bps=2e12, mem_B=80e9, nvec=3),
        "4096 GPUs": dict(kind="gpu", bw_Bps=4096 * 2e12, comm=3, mem_B=4096 * 64e9, nvec=3),
        "exascale (Frontier-class, 4.8 PB)": dict(kind="gpu", bw_Bps=75264 * 1.6e12, comm=3, mem_B=75264 * 64e9, nvec=2),
    }
    out = {}
    for tl, tsec in T_LAYER.items():
        for pname, p in plats.items():
            Nstar = None
            for N in range(12, 80, 2):
                q = q_curve(N, N * (N - 1) / 2, tsec)["wall_depth_limited_s"]
                c, _ = classical_time(N, p)
                if q < c:
                    Nstar = N
                    break
            q = q_curve(Nstar, Nstar * (Nstar - 1) / 2, tsec)["wall_depth_limited_s"] if Nstar else None
            out[f"{tl} | {pname}"] = dict(N_star=Nstar, quantum_wall_at_Nstar=fmt(q) if q else None,
                                          classical_at_Nstar=fmt(classical_time(Nstar, p)[0]) if Nstar else None)
    OUTD["C_breakeven_vs_exact"] = dict(
        definition="smallest even N at which ONE fault-tolerant QPU (depth-limited, unlimited factories, sampling, "
                   "dense reference circuit) finishes one echo curve faster than the classical exact method; "
                   "classical = inf beyond memory",
        rows=out)
    save()


# =============================================================================== D. robustness of N_needed
def fit_lin(Ns, F, f):
    A = np.vstack([np.ones(len(Ns)), f(np.asarray(Ns, float))]).T
    coef, *_ = np.linalg.lstsq(A, np.asarray(F, float), rcond=None)
    return float(coef[0]), float(coef[1]), float(np.sqrt(np.mean((A @ coef - F) ** 2)))


def fit_exp(Ns, F):
    best = None
    for xi in np.geomspace(0.5, 200, 400):
        Finf, A, rms = fit_lin(Ns, F, lambda n: np.exp(-n / xi))
        if best is None or rms < best[3]:
            best = (Finf, A, float(xi), rms)
    return best


def n_sigma_exp(A, xi):
    return xi * math.log(abs(A) / SIGMA) if abs(A) > SIGMA else 0.0


def section_D():
    rs = json.load(open(os.path.join(LANE, "reach_summary.json")))
    out = {}
    for key, v in rs["convergence"].items():
        Ns = v["Ns"]
        for b, f in v["fits"].items():
            F = f["F"]
            rec = dict(Ns=Ns, F=F)
            # exponential: all points, and leave-one-out
            e = fit_exp(Ns, F)
            rec["exp_all"] = dict(xi=e[2], rms_over_sigma=e[3] / SIGMA, N_sigma=n_sigma_exp(e[1], e[2]), Finf=e[0])
            loo = []
            for i in range(len(Ns)):
                Ns2 = [n for j, n in enumerate(Ns) if j != i]
                F2 = [x for j, x in enumerate(F) if j != i]
                e2 = fit_exp(Ns2, F2)
                loo.append(dict(drop=Ns[i], xi=e2[2], rms_over_sigma=e2[3] / SIGMA, N_sigma=n_sigma_exp(e2[1], e2[2]),
                                Finf=e2[0]))
            rec["exp_leave_one_out"] = loo
            # 1/N variants
            fits_invN = {}
            for lab, sl in (("all", slice(None)), ("last3", slice(-3, None)), ("last2", slice(-2, None)),
                            ("drop12", slice(1, None))):
                Ns2, F2 = Ns[sl], F[sl]
                if len(Ns2) < 2:
                    continue
                Finf, c, rms = fit_lin(Ns2, F2, lambda n: 1.0 / n)
                fits_invN[lab] = dict(Finf=Finf, c=c, N_sigma=abs(c) / SIGMA, rms_over_sigma=rms / SIGMA)
            rec["invN"] = fits_invN
            # 1/N^2 (faster, e.g. boundary-dominated) model on last 3
            if len(Ns) >= 3:
                Finf, c, rms = fit_lin(Ns[-3:], F[-3:], lambda n: 1.0 / n ** 2)
                rec["invN2_last3"] = dict(Finf=Finf, c=c, N_sigma=math.sqrt(abs(c) / SIGMA), rms_over_sigma=rms / SIGMA)
            # acceleration test on the last 3 points: a convergent monotone model needs |d2| < |d1|
            if len(Ns) >= 3:
                d1 = F[-2] - F[-3]
                d2 = F[-1] - F[-2]
                rec["last_steps"] = dict(d_prev=d1, d_last=d2, ratio=(abs(d2) / abs(d1)) if d1 else None,
                                         accelerating=abs(d2) > abs(d1))
            # spread of F_inf across models (model uncertainty of the converged value)
            finfs = [rec["exp_all"]["Finf"]] + [x["Finf"] for x in fits_invN.values()] + [x["Finf"] for x in loo]
            rec["Finf_spread_over_models"] = [min(finfs), max(finfs)]
            out[f"{key}_site{b}"] = rec
    # headline: the lane's '>= 58' (p19 t320 sites 8/9, exponential) under leave-one-out
    head = {}
    for s in ("p19_t320_site8", "p19_t320_site9"):
        r = out[s]
        head[s] = dict(exp_all_N_sigma=r["exp_all"]["N_sigma"], exp_all_rms_over_sigma=r["exp_all"]["rms_over_sigma"],
                       exp_loo_N_sigma=[round(x["N_sigma"], 1) for x in r["exp_leave_one_out"]],
                       exp_loo_rms_over_sigma=[round(x["rms_over_sigma"], 2) for x in r["exp_leave_one_out"]],
                       invN_N_sigma={k: round(x["N_sigma"]) for k, x in r["invN"].items()},
                       invN_Finf={k: round(x["Finf"], 3) for k, x in r["invN"].items()},
                       invN2_last3_N_sigma=r["invN2_last3"]["N_sigma"],
                       last_steps=r["last_steps"], Finf_spread=r["Finf_spread_over_models"])
    OUTD["D_needed_N_robustness"] = dict(headline=head, all=out)
    save()


# =============================================================================== F. kernel re-benchmark (N = 20)
def section_F():
    import fastecho as FE
    from fastecho import SP
    t0 = time.process_time()
    dm, _, _, _ = FE.load_instance("1UBQ", 19, 20)
    pairs = SP.pair_list(dm, 2e-6)
    idx = FE.sector_index(20, 10)
    tb = time.process_time()
    K = FE.SectorKernel(20, idx, pairs, np.complex64)
    tb = time.process_time() - tb
    v = (np.random.default_rng(3).standard_normal(len(idx)) + 1j * np.random.default_rng(4).standard_normal(len(idx))
         ).astype(np.complex64)
    v /= np.linalg.norm(v)
    K.step(v)
    ts = []
    for _ in range(4):
        t = time.perf_counter(); K.step(v); ts.append(time.perf_counter() - t)
    sec = min(ts)
    OUTD["F_kernel_rebench_N20"] = dict(sector_dim=len(idx), pairs=len(pairs), sec_per_step_min=sec,
                                        sec_per_step_all=ts, ns_per_pair_elem=1e9 * sec / (len(pairs) * len(idx) / 2),
                                        build_cpu_s=tb, total_cpu_s=time.process_time() - t0,
                                        norm_err=float(abs(np.linalg.norm(v) - 1)))
    save()


def main():
    t0 = time.process_time()
    section_A()
    cstats = couplings_stats()
    OUTD["E_coupling_stats_1UBQ"] = cstats
    save()
    section_B(cstats)
    section_C()
    section_D()
    if "--no-bench" not in sys.argv:
        section_F()
    OUTD["cpu_s_total"] = time.process_time() - t0
    try:
        import psutil
        OUTD["peak_rss_GB"] = psutil.Process().memory_info().peak_wset / 1e9
    except Exception:
        pass
    save()
    # console summary
    print("A frontier:")
    for k, v in OUTD["A_classical_frontier"]["platforms"].items():
        print(f"  {k}: N_max {v['N_max']} ({v['time_at_Nmax']}); next N: {v['next_N_time']}, mem {v['next_N_mem_PB']:.3g} PB")
    print("B quantum per curve (p19 couplings):")
    for r in OUTD["B_quantum_cost_per_curve"]["rows"]:
        d = r["dense"]
        s = (f"  N={r['N']:3d} dense pairs {r['pairs_dense']:.0f} (>30Hz {r['pairs_gt_30Hz']}) T {d['T_count_sampling']:.2e} "
             f"Tdepth {d['T_depth_sampling']:.2e} wall {d['wall_sampling']} dt0.5 {d['wall_sampling_dt0p5us']['1us']} "
             f"AE {d['wall_AE']['1us']} CNOT/circ {d['cnot_deepest_circuit']:.2e}")
        if "cut30Hz" in r:
            c = r["cut30Hz"]
            s += f" | cut30Hz T {c['T_count_sampling']:.2e} wall {c['wall_sampling']}"
        if "qubitization_dense_toffoli_per_curve" in r:
            s += f" | qubitiz Toff {r['qubitization_dense_toffoli_per_curve']:.2e} (lambda t {r['lambda_t_320us']:.3g})"
        print(s)
    print("C break-even:")
    for k, v in OUTD["C_breakeven_vs_exact"]["rows"].items():
        print(f"  {k}: N* {v['N_star']} (Q {v['quantum_wall_at_Nstar']} vs C {v['classical_at_Nstar']})")
    print("D robustness:")
    for k, v in OUTD["D_needed_N_robustness"]["headline"].items():
        print(" ", k, json.dumps(v, default=float))
    if "F_kernel_rebench_N20" in OUTD:
        print("F", json.dumps(OUTD["F_kernel_rebench_N20"], default=float))
    print("cpu_s", OUTD["cpu_s_total"], "peak_rss_GB", OUTD.get("peak_rss_GB"))


if __name__ == "__main__":
    main()
