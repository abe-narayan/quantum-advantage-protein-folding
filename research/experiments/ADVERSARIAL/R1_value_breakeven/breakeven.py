"""R1 value lens, part 4: break-even of a fault-tolerant quantum forward model for protein 1H dipolar echoes against
(a) exact classical light-cone simulation and (b) the measured sparse-Pauli adversary; end-to-end task costs.

Extends research/theory/nmr_resource_model.py (copied logic, not imported, so that file stays untouched):
  * z_eff = min(z, N-1) coupled partners per spin (the original fixed z = 15 over-counts at small N);
  * circuits for time point k have 2k Trotter steps (forward + backward), so a forward evaluation over n_t equally spaced
    times costs n_b * n_T * (n_t + 1) steps per repetition (the original charged every time point the full n_T twice);
  * two T-supply scenarios: depth-limited (unlimited parallel factories, t_T = one T layer; most favourable to quantum)
    and rate-limited (n_fact = 100 factories each emitting one T per t_T);
  * repetitions: amplitude estimation to eps = 3e-3 (2 * pi / (2 eps) ~ 1047) or plain sampling 1/eps^2 (~1.1e5).

Classical exact (dynamical typicality, one random vector, error 2^-N/2 << sigma for N >= 14):
  * steps per evaluation: A|r> once per time point, A B_b|r> per observable -> (1 + n_b) * n_T * (n_t + 3) / 2
    (forward sweeps are shared across time points by storing checkpoints, backward legs are not);
  * each step = M(N) = N z_eff / 2 pair gates, each touching 2^N amplitudes; throughput per core measured here with a
    numpy kernel (MEASURED, this machine, unoptimised) plus INFERENCE scenarios for optimised CPU / GPU simulators;
  * memory wall: 3 state vectors of 16 B * 2^N must fit (INFERENCE budgets: node 1 TB, cluster 64 TB, leadership 4 PB).
Sparse-Pauli adversary (MEASURED at N = 8, 10 in C2/C3): M*_F(N) = 256,643 * kappa^(N-10), kappa = 4 per spin
(x16 per +2 spins, measured) or 2 per spin (optimistic for the adversary); one Heisenberg pass gives every b and t;
cost per string-pair-gate measured from the C2 run (1910 s for 160 steps x 45 pairs with <= 256,643 strings).
Gradients: classical adjoint ~3x a forward pass for all P parameters; quantum central differences (2P+1)x.

Run: OMP_NUM_THREADS=1 python breakeven.py   (~10 s).  Output: breakeven.json.
"""
import json
import math
import os
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
YR, DAY, HR = 3.156e7, 86400.0, 3600.0

NET = {  # instrument settings of the measured jobs (C1 dense; C1-HN amide-only)
    "dense": dict(z=15, dt_us=2.0, t_us=320.0, n_t=16, n_b=4),
    "amide": dict(z=8, dt_us=5.0, t_us=1000.0, n_t=20, n_b=3),
}
EPS = 3e-3


# ----------------------------------------------------------------------------- measured classical kernel
def bench_pair_gates(N=20, n_gates=40, seed=0):
    """Apply secular dipolar pair factors exp(-i th (2ZZ - XX - YY)/4) to a 2^N statevector (numpy, one thread)."""
    rng = np.random.default_rng(seed)
    psi = rng.standard_normal(2 ** N) + 1j * rng.standard_normal(2 ** N)
    psi /= np.linalg.norm(psi)
    pairs = [tuple(sorted(rng.choice(N, 2, replace=False))) for _ in range(n_gates)]
    th = 0.05
    ph_d = np.exp(-1j * th / 2)             # |00>, |11>: eigenvalue +th/2
    # {01,10} block: (th/2) [[-1,-1],[-1,-1]] -> eigen 0 (sym... ) ; exact 2x2 exponential
    Hb = (th / 2) * np.array([[-1.0, -1.0], [-1.0, -1.0]])
    w, V = np.linalg.eigh(Hb)
    Ub = (V * np.exp(-1j * w)) @ V.T
    t0 = time.perf_counter()
    for (i, j) in pairs:
        s = psi.reshape(2 ** i, 2, 2 ** (j - i - 1), 2, 2 ** (N - j - 1))
        a00 = s[:, 0, :, 0, :]; a11 = s[:, 1, :, 1, :]
        a01 = s[:, 0, :, 1, :].copy(); a10 = s[:, 1, :, 0, :].copy()
        a00 *= ph_d; a11 *= ph_d
        s[:, 0, :, 1, :] = Ub[0, 0] * a01 + Ub[0, 1] * a10
        s[:, 1, :, 0, :] = Ub[1, 0] * a01 + Ub[1, 1] * a10
    dt = time.perf_counter() - t0
    assert abs(np.linalg.norm(psi) - 1) < 1e-9
    return (2 ** N) * n_gates / dt      # amplitude-gate updates per second per core


# ----------------------------------------------------------------------------- quantum cost
def q_cost(N, net, t_T, reps_mode="AE", n_fact=None, eps_tot=1e-3):
    p = NET[net]
    z = min(p["z"], N - 1)
    M = N * z / 2
    n_T = p["t_us"] / p["dt_us"]
    steps_rep = p["n_b"] * n_T * (p["n_t"] + 1)        # sum over (b, k) of 2k steps (k = n_T * j / n_t)
    n_rot_circ_max = 3 * M * 2 * n_T
    eps_rot = eps_tot / n_rot_circ_max
    t_rot = 1.15 * math.log2(1 / eps_rot) + 9.2         # Ross-Selinger average-case T per rotation
    reps = (math.pi / (2 * EPS)) * 2 if reps_mode == "AE" else 1 / EPS ** 2
    T_count = reps * steps_rep * 3 * M * t_rot
    T_depth = reps * steps_rep * (z + 1) * 3 * t_rot  # edge-colouring: ~z+1 layers of disjoint pair gates per step
    t_depth = T_depth * t_T
    t_rate = T_count * t_T / n_fact if n_fact else None
    wall = max(t_depth, t_rate) if n_fact else t_depth
    return dict(N=N, M=M, T_count=T_count, T_depth=T_depth, wall_s=wall, logical_qubits=2 * N + 10, reps=reps)


# ----------------------------------------------------------------------------- classical costs
def c_exact(N, net, thr_core, cores, mem_bytes):
    p = NET[net]
    z = min(p["z"], N - 1)
    M = N * z / 2
    n_T = p["t_us"] / p["dt_us"]
    steps = (1 + p["n_b"]) * n_T * (p["n_t"] + 3) / 2
    work = steps * M * 2.0 ** N
    fits = 3 * 16 * 2.0 ** N <= mem_bytes
    return dict(N=N, work_amp_gates=work, wall_s=work / (thr_core * cores), fits=fits)


def c_pauli(N, net, c_s, kappa, cores=1):
    p = NET[net]
    z = min(p["z"], N - 1)
    M = N * z / 2
    n_T = p["t_us"] / p["dt_us"]
    Mstar = 256643 * kappa ** (N - 10)
    return dict(N=N, strings=Mstar, wall_s=0.6 * Mstar * M * n_T * c_s / cores, mem_bytes=Mstar * (N / 4 + 16))


def crossing(fq, fc, Ns):
    """smallest N at which quantum wall-clock < classical wall-clock (or classical infeasible)."""
    for N in Ns:
        q, c = fq(N), fc(N)
        if (not c.get("fits", True)) or q["wall_s"] < c["wall_s"]:
            return N, q, c
    return None, None, None


def fmt(s):
    if s is None:
        return "-"
    for u, v in (("yr", YR), ("d", DAY), ("h", HR), ("min", 60.0), ("s", 1.0)):
        if s >= v:
            return f"{s / v:.3g} {u}"
    return f"{s:.2g} s"


def main():
    thr_meas = float(np.median([bench_pair_gates(20, 40, s) for s in range(3)]))
    # sparse-Pauli per string-pair-gate cost from the measured C2 run (N=10, eps=3e-5, 1910 s, 160 steps, 45 pairs)
    c_s = 1910.0 / (160 * 45 * 0.6 * 256643)
    print(f"MEASURED numpy statevector throughput: {thr_meas:.3g} amplitude-gate updates / s / core; "
          f"sparse-Pauli (C2 run): {c_s:.3g} s per string-pair-gate")

    CLASSICAL = {   # (throughput per core-equivalent, core-equivalents, memory) -- INFERENCE scenarios except 'numpy-1core'
        "numpy-1core (MEASURED kernel)": (thr_meas, 1, 16e9),
        "opt-node (64 cores, 1 TB)": (1e9, 64, 1e12),
        "cluster (1e4 cores, 64 TB)": (1e9, 1e4, 64e12),
        "leadership (1e6 core-eq, 4 PB)": (1e9, 1e6, 4e15),
    }
    TT = {"1us": 1e-6, "10us": 1e-5, "170us": 1.7e-4}
    Ns = list(range(10, 700))
    out = dict(measured=dict(numpy_amp_gate_per_s=thr_meas, pauli_s_per_string_gate=c_s), breakeven={}, tasks=[])

    print("\n=== (a) break-even vs EXACT classical light-cone simulation: smallest N_eff where quantum wall-clock wins"
          " (or classical memory wall) ===")
    for net in NET:
        for tl, tT in TT.items():
            for qmode in ("AE-depth", "AE-100fact", "sampling-depth"):
                rm = "AE" if qmode.startswith("AE") else "samp"
                nf = 100 if "fact" in qmode else None
                for cl, (thr, cores, mem) in CLASSICAL.items():
                    N, q, c = crossing(lambda n: q_cost(n, net, tT, rm, nf), lambda n: c_exact(n, net, thr, cores, mem), Ns)
                    key = f"{net}|tT={tl}|{qmode}|{cl}"
                    out["breakeven"][key] = dict(N_star=N, q_wall=q["wall_s"] if q else None,
                                                 c_wall=c["wall_s"] if c else None, c_fits=c["fits"] if c else None)
                    if qmode == "AE-depth" or cl.startswith("leadership"):
                        why = "memory wall" if (c and not c["fits"]) else "time"
                        print(f"  {net:5s} tT={tl:5s} {qmode:14s} vs {cl:32s}: N* = {N}  ({why}; quantum {fmt(q['wall_s']) if q else '-'} per eval)")

    print("\n=== (b) break-even vs the MEASURED sparse-Pauli adversary (1 core) and dominance check ===")
    for net in NET:
        for kappa in (4.0, 2.0):
            for tl, tT in TT.items():
                N, q, c = crossing(lambda n: q_cost(n, net, tT, "AE", None), lambda n: c_pauli(n, net, c_s, kappa), Ns)
                out["breakeven"][f"{net}|tT={tl}|AE-depth|pauli-kappa{kappa}"] = dict(N_star=N)
                print(f"  {net:5s} kappa={kappa} tT={tl}: N* = {N}")
            # dominance: is exact statevector (numpy, 1 core) cheaper than Pauli at the same N?
            dom = [n for n in range(10, 40) if c_exact(n, net, thr_meas, 1, 1e30)["wall_s"] < c_pauli(n, net, c_s, kappa)["wall_s"]]
            print(f"    exact(numpy,1 core) cheaper than Pauli(kappa={kappa}) for N in {dom[:1]}..{dom[-1:]} ({len(dom)} of 30 values)")
            out["breakeven"][f"{net}|dominance_exact_over_pauli_kappa{kappa}"] = dom

    # ------------------------------------------------------------------ end-to-end tasks
    print("\n=== (3) end-to-end tasks (Gauss-Newton, 20 iterations, finite-difference Jacobian on the quantum side;"
          " adjoint on the classical side) ===")
    TASKS = [
        ("T1 GB1 amide-only, 1 probe, P=4", "amide", 30, 4, "N_eff(t50) median 20-31 (bracket 13-56)"),
        ("T2 ubiquitin amide-only, 1 probe, P=4", "amide", 45, 4, "N_eff(t90) median 35-50 (bracket 16-73)"),
        ("T3 ubiquitin amide-only, full cone, P=4", "amide", 73, 4, "all 73 amide H (fast-calibration bracket)"),
        ("T4 ubiquitin dense, 1 probe, P=4", "dense", 100, 4, "N_eff(t50) median 21-110"),
        ("T5 ubiquitin dense, 1 probe, P=4, full molecule", "dense", 629, 4, "N_eff(t90) up to 629"),
        ("T6 ubiquitin dense, 76 probes, P=3*76", "dense", 250, 228, "whole-backbone refinement, 76 probe data sets"),
    ]
    for name, net, N, P, note in TASKS:
        n_iter = 20
        n_probe = 76 if "76 probes" in name else 1
        evals_q = n_iter * (2 * P + 1) * n_probe
        evals_c = n_iter * 3 * n_probe
        row = dict(task=name, network=net, N_eff=N, P=P, note=note, quantum_evals=evals_q)
        for tl, tT in TT.items():
            q = q_cost(N, net, tT, "AE", None)
            row[f"quantum_total_{tl}_depth"] = evals_q * q["wall_s"]
            row[f"quantum_total_{tl}_100fact"] = evals_q * q_cost(N, net, tT, "AE", 100)["wall_s"]
        row["T_count_per_eval"] = q_cost(N, net, 1e-6)["T_count"]
        row["logical_qubits"] = q_cost(N, net, 1e-6)["logical_qubits"]
        ce = c_exact(N, net, 1e9, 1e6, 4e15)
        row["classical_exact_leadership_total"] = evals_c * ce["wall_s"] if ce["fits"] else None
        ce1 = c_exact(N, net, 1e9, 64, 1e12)
        row["classical_exact_node_total"] = evals_c * ce1["wall_s"] if ce1["fits"] else None
        out["tasks"].append(row)
        print(f"  {name:48s} N_eff={N:4d} evals_Q={evals_q:6d}  T/eval={row['T_count_per_eval']:.2e}  "
              f"Q total @1us depth {fmt(row['quantum_total_1us_depth'])} | @1us 100 fact {fmt(row['quantum_total_1us_100fact'])}"
              f" | @170us depth {fmt(row['quantum_total_170us_depth'])} || classical exact: node {fmt(row['classical_exact_node_total'])},"
              f" leadership {fmt(row['classical_exact_leadership_total'])}")

    # ------------------------------------------------------------------ value break-even (spectrometer time)
    # The only thing the hard window buys (F_classical nonsingular, fi_value.py) is g-fold fewer repetitions of the data.
    # Break-even acquisition time per probe data set: T_acq * (g - 1) * price_spec >= n_eval * T_eval * price_QC.
    print("\n=== value break-even: acquisition time per probe data set needed before the saved (g-1) x T_acq pays for the"
          " quantum inversion (price ratio QC-hour / spectrometer-hour = r) ===")
    fv = json.load(open(os.path.join(HERE, "fi_value.json")))
    vb = {}
    for net, gkey, Nn, P in (("dense", "dense", 100, 4), ("amide", "amide-only", 45, 4)):
        g_med = fv["aggregate"][gkey]["g_param"]["median"]
        g_max = fv["aggregate"][gkey]["max_gain_eig"]["max"]
        q = q_cost(Nn, net, 1e-6, "AE", None)
        tq = 20 * (2 * P + 1) * q["wall_s"]
        for r in (1, 10, 100):
            for lab, g in (("g_median", g_med), ("g_best_direction", g_max)):
                need = tq * r / (g - 1)
                vb[f"{net}|N={Nn}|r={r}|{lab}"] = need
                print(f"  {net:5s} N_eff={Nn} r={r:3d} {lab:16s} (g={g:5.1f}): T_acq >= {fmt(need)}  (quantum inversion {fmt(tq)} @1us depth-limited)")
    out["value_breakeven_Tacq_s"] = vb
    json.dump(out, open(os.path.join(HERE, "breakeven.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
