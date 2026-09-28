"""Resource auditor: full resource ledger for the R1-SIM echo observable under the lane metric
(F_ab(t) = Tr[W Z_b W Z_b]/2^N, W = U(t)^dag Z_a U(t), fused-pair Trotter circuit dt = 2 us, window t = 80,160,240,320 us,
|bs| = 4, sigma = 0.01, family-wise 95 % over 16 (b,t) points).  Pure arithmetic + measured timings; no simulation.

Classical sides (MEASURED counts; wall-clock calibrated on this loaded host, INDICATIVE):
  exact_nmr_cone   : scripts/nmr_cone.py cost: 5*160 forward (S pass) + sum_{k=20..160 step 20} 5*2k steps, 1 vector
  exact_incremental: verify_resource/exact_fast.py cost: 160 forward + sum_{k in window} k backward, 5 columns
  cqc(k)           : lane cqc_echo.py, M = 48, 5 branches, 840 steps, dense sector blocks sum_m C(k,m)^2 per column-step
Quantum side (DERIVED, fault-tolerant, optimistic): infinite-temperature OTOC via random computational basis states:
  F_b = E_s[(-1)^{s_b} <s|W Z_b W|s>]  -> circuit: |s>, U(t), Z_a (Pauli, free), U(t)^dag, measure all Z; every b from the
  same shot; per-shot variance 1 - F_b^2 <= 1.  Pair gate = exp(-i theta (2ZZ - XX - YY)) = 3 commuting 2-qubit Pauli
  rotations = 3 arbitrary-angle Rz after Clifford basis change.  Rotation synthesis T-count 1.15 log2(1/eps) + 9.2
  (Ross-Selinger, arXiv:1403.2975 [LITERATURE-SUPPORTED, not re-read this session]).  Synthesis error budget
  delta = 0.003 (<< sigma) split over the rotations of the LONGEST circuit.  Shots: per-point SE <= (sigma - delta)/2.96.
  T-depth: one Trotter step = N-1 perfect matchings (round robin) x 3 rotations x T/rot.  Clock: 1 us per T (serial) or
  per T-layer (unlimited factories) -- the optimistic K-101 convention.  Logical qubits N (+ synthesis ancillas).
  NISQ: 2k*N(N-1)/2 native 2-qubit gates, fidelity (1 - 1e-3)^G.
"""
from __future__ import annotations

import json
import math
import os
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
WIN_K = [40, 80, 120, 160]
NB = 4
SIG, DELTA, ZB = 0.01, 0.003, 2.96


def npairs(N):
    return N * (N - 1) // 2


def exact_nmr_cone_updates(N):
    steps = 5 * 160 + sum(5 * 2 * k for k in range(20, 161, 20))
    return steps * npairs(N) * 2 ** N, steps


def exact_incr_updates(N):
    col_steps = (1 + NB) * (160 + sum(WIN_K))
    return col_steps * npairs(N) * 2 ** N, col_steps


def cqc_macs(sizes, M=48, steps=840):
    return steps * M * (1 + NB) * sum(comb(n, m) ** 2 for n in sizes for m in range(n + 1))


def quantum(N):
    rot_step = 3 * npairs(N)
    rot_longest = 2 * max(WIN_K) * rot_step
    eps = DELTA / rot_longest
    t_rot = 1.15 * math.log2(1 / eps) + 9.2
    se = (SIG - DELTA) / ZB
    shots = math.ceil(1 / se ** 2)                                  # per time point (all b from the same shots)
    T_per_shot_all_t = sum(2 * k for k in WIN_K) * rot_step * t_rot
    T_total = shots * T_per_shot_all_t
    tdepth_step = (N - 1) * 3 * t_rot
    layers_total = shots * sum(2 * k for k in WIN_K) * tdepth_step
    G_longest = 2 * max(WIN_K) * npairs(N)
    G_short = 2 * min(WIN_K) * npairs(N)
    # Heisenberg-limited alternative: amplitude estimation per (b, t) point on the purified infinite-temperature state
    # (2N logical qubits); ~pi/(2 SE) coherent applications of (echo circuit + inverse) per point, no shot sharing.
    A = math.pi / (2 * se)
    qae_step_units = NB * sum(A * 2 * (2 * k) for k in WIN_K)
    qae_layers = qae_step_units * tdepth_step
    qae_coherent_layers_longest = A * 2 * (2 * max(WIN_K)) * tdepth_step
    return dict(N=N, logical_qubits=N, qae_logical_qubits=2 * N,
                qae_T_layers_total=qae_layers, qae_parallel_1us_per_layer_hours=qae_layers * 1e-6 / 3600,
                qae_parallel_10us_per_layer_hours=qae_layers * 1e-5 / 3600,
                qae_longest_coherent_T_layers=qae_coherent_layers_longest, rotations_longest_circuit=rot_longest, eps_per_rotation=eps,
                T_per_rotation=round(t_rot, 1), shots_per_time_point=shots, T_count_total=T_total,
                wallclock_serial_T_1us_days=T_total * 1e-6 / 86400, T_layers_total=layers_total,
                wallclock_parallel_1us_per_layer_days=layers_total * 1e-6 / 86400,
                nisq_2q_gates_longest=G_longest, nisq_fidelity_longest_1e3=math.exp(-1e-3 * G_longest),
                nisq_fidelity_shortest_1e3=math.exp(-1e-3 * G_short))


def main():
    # calibrations (MEASURED on this host; see README for sources)
    cal = {}
    ref_secs = {("p19", 14): 86, ("p245", 14): 132, ("p19", 16): 632, ("p245", 16): 654, ("p19", 18): 9509,
                ("p245", 18): 9451}
    for (p, N), s in ref_secs.items():
        u, _ = exact_nmr_cone_updates(N)
        cal[f"nmr_cone_{p}_N{N}_ns_per_update"] = round(1e9 * s / u, 2)
    fe = os.path.join(HERE, "out_exact", "1UBQ_p19_N14_seeds12345-1-2-3.json")
    if os.path.exists(fe):
        d = json.load(open(fe))
        u, _ = exact_incr_updates(14)
        u *= len(d["seeds"])
        cal["exact_fast_p19_N14_R4_ns_per_update"] = round(1e9 * d["wall_total_this_call"] / u, 2)
        cal["exact_fast_p19_N14_R4_wall_s"] = round(d["wall_total_this_call"], 1)
    cqc_secs = {"kls12_[12,4]_N16": (441.7, [12, 4]), "kl10_[10,6]_N16": (69.7, [10, 6]),
                "kls10_[10,8]_N18": (85.5, [10, 8]), "kl8_[8,8]_N16": (18.0, [8, 8])}
    for k, (s, sizes) in cqc_secs.items():
        cal[f"cqc_{k}_ns_per_MAC"] = round(1e9 * s / cqc_macs(sizes), 3)
    ns_upd = 10.0                       # representative exact ns/update on this loaded host (N14-16 nmr_cone range)
    rows = []
    for N in (16, 18, 20, 22, 24, 26, 28, 30, 36, 40, 44, 50):
        u_cone, _ = exact_nmr_cone_updates(N)
        u_inc, _ = exact_incr_updates(N)
        mem_gb = (2 * (1 + NB)) * 2 ** N * 16 / 1e9            # forward columns + one backward copy
        cq = cqc_macs([12, N - 12]) if N - 12 <= 12 else cqc_macs([12] * (N // 12) + ([N % 12] if N % 12 else []))
        rows.append(dict(N=N, exact_nmr_cone_updates=u_cone, exact_incr_updates=u_inc,
                         exact_incr_1thread_hours_at_10ns=u_inc * ns_upd * 1e-9 / 3600,
                         exact_incr_state_memory_GB=mem_gb,
                         cqc_k12_partition_MACs=cq, cqc_k12_over_exact_incr_ratio=cq / u_inc,
                         quantum=quantum(N)))
    # convergence of the reference in N (MEASURED from typicality_cone JSONs; geometric extrapolation = INFERENCE)
    dF = {"p19": [0.1857, 0.1394, 0.0372], "p245": [0.1199, 0.1316, 0.0567]}   # max|F_{N+2}-F_N|, N = 12,14,16
    conv = {}
    for p, v in dF.items():
        r = v[-1] / v[-2]
        conv[p] = dict(dF_12_14_16_18=v, last_ratio=round(r, 3),
                       extrap_dF_18_20=round(v[-1] * r, 4), extrap_dF_20_22=round(v[-1] * r * r, 4),
                       extrap_dF_22_24=round(v[-1] * r ** 3, 4))
    out = dict(calibration=cal, rows=rows, reference_convergence=conv, conventions=__doc__)
    json.dump(out, open(os.path.join(HERE, "resource_ledger.json") + ".tmp", "w"), indent=1)
    os.replace(os.path.join(HERE, "resource_ledger.json") + ".tmp", os.path.join(HERE, "resource_ledger.json"))
    print(json.dumps(cal, indent=0))
    print(json.dumps(conv))
    print(f"{'N':>3} {'exact_inc_upd':>13} {'1thr_h':>9} {'memGB':>9} {'cqc12/exact':>11} | {'Tcount':>9} "
          f"{'serial_d':>9} {'par_d':>8} {'shots/t':>8} {'NISQ F(320us)':>13}")
    print("QAE variant (Heisenberg-limited, 2N logical qubits), hours at 1 us / 10 us per T-layer vs classical exact "
          "(1 thread at 10 ns/update; 8 threads assumed 6x):")
    for r in rows:
        q = r["quantum"]
        c1 = r["exact_incr_1thread_hours_at_10ns"]
        print(f"  N={r['N']:>2}  QAE {q['qae_parallel_1us_per_layer_hours']:9.3g} h / {q['qae_parallel_10us_per_layer_hours']:9.3g} h"
              f"   classical 1thr {c1:9.3g} h  8thr {c1 / 6:9.3g} h   coherent layers {q['qae_longest_coherent_T_layers']:.2g}")
    for r in rows:
        q = r["quantum"]
        print(f"{r['N']:>3} {r['exact_incr_updates']:13.3g} {r['exact_incr_1thread_hours_at_10ns']:9.3g} "
              f"{r['exact_incr_state_memory_GB']:9.3g} {r['cqc_k12_over_exact_incr_ratio']:11.3g} | "
              f"{q['T_count_total']:9.3g} {q['wallclock_serial_T_1us_days']:9.3g} "
              f"{q['wallclock_parallel_1us_per_layer_days']:8.3g} {q['shots_per_time_point']:8d} "
              f"{q['nisq_fidelity_longest_1e3']:13.3g}")


if __name__ == "__main__":
    main()
