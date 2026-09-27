"""Program C resource model: fault-tolerant cost of ONE quantum forward-model evaluation for protein 1H dipolar
NMR (transfer S_ab(t) or first-order OTOC F_ab(t)), and of an inversion that consumes it.  All inputs labelled;
prints a table for research/theory/RESOURCE_MODELS.md §8.  No hardware claim; product-formula (Trotter) costing.

Circuit per shot (infinite-temperature trace by random computational-basis inputs |z>):
  transfer:  |z> -> U(t) -> measure Z_a            (estimator z_b * outcome)       one evolution
  OTOC(1):   |z> -> U(t) -> Z_a -> U(t)^dag -> measure Z_b  (estimator z_b * outcome)  two evolutions
U(t) = n_T first-order Trotter steps (as in the classical instrument); each secular dipolar pair factor
exp(-i dt d_ij (2ZZ - XX - YY)/4) = three commuting Pauli rotations -> 3 arbitrary-angle rotations.
Rotation synthesis (Ross-Selinger): T-count ~ 3 log2(1/eps_rot) (i.e. ~1.15 log2 + 9 for the average case; we use 3x
for worst-case, conservative for quantum is 1x); eps_rot = eps_total / n_rot.
Shots: sampling needs ~ 1/eps^2 per (time, observable); amplitude estimation (coherent average over z via a
purified maximally mixed input, 2N qubits) needs ~ pi/(2 eps) controlled repetitions (x2 for the reflection).
"""
import math

T_PER_S = {"1us": 1e-6, "10us": 1e-5, "170us": 1.7e-4}      # seconds per logical T/Toffoli (A56 / optimistic)


def cost(N, z=15, t_us=300.0, dt_us=2.0, n_t=16, n_b=4, eps=3e-3, P=4, otoc=True, ae=True, rs_mult=1.15, eps_tot=1e-3):
    M = N * z / 2                          # coupled pairs within the cutoff
    n_T = t_us / dt_us
    evol = 2 if otoc else 1
    n_rot = 3 * M * n_T * evol
    eps_rot = eps_tot / n_rot
    t_per_rot = rs_mult * math.log2(1 / eps_rot) + 9.2
    T_circ = n_rot * t_per_rot
    reps = (math.pi / (2 * eps)) * 2 if ae else 1 / eps ** 2
    T_eval = T_circ * reps * n_t * n_b      # one forward evaluation: all times, all observables, one geometry
    T_grad = T_eval * (2 * P + 1)           # finite-difference gradient over P parameters
    # T-depth with unlimited parallel factories: pairs edge-coloured into ~ (z + 1) layers per step
    Tdepth_circ = n_T * evol * (z + 1) * 3 * t_per_rot
    return dict(N=N, pairs=M, steps=n_T, rotations=n_rot, T_per_circuit=T_circ, reps=reps, T_eval=T_eval, T_grad=T_grad,
                Tdepth_eval=Tdepth_circ * reps * n_t * n_b, Tdepth_grad=Tdepth_circ * reps * n_t * n_b * (2 * P + 1))


def fmt_t(sec):
    for unit, s in (("yr", 3.15e7), ("d", 86400), ("h", 3600), ("s", 1)):
        if sec >= s:
            return f"{sec / s:.3g} {unit}"
    return f"{sec:.2g} s"


if __name__ == "__main__":
    print("| N | observable | pairs | T per circuit | reps (AE) | T per forward eval | time/eval @1us | @10us | @170us | inversion (1e3 grad evals) @1us |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for N in (14, 30, 60, 120, 466):
        for otoc in (False, True):
            c = cost(N, otoc=otoc)
            row = [str(N), "OTOC(1)" if otoc else "transfer", f"{c['pairs']:.0f}", f"{c['T_per_circuit']:.2e}",
                   f"{c['reps']:.0f}", f"{c['T_eval']:.2e}"]
            row += [fmt_t(c["T_eval"] * T_PER_S[k]) for k in ("1us", "10us", "170us")]
            row += [fmt_t(1e3 * c["T_grad"] * T_PER_S["1us"])]
            print("| " + " | ".join(row) + " |")
    print("\nDepth-limited (unlimited parallel T factories, one machine), OTOC(1), T-layer time 1 us / 10 us:")
    for N in (14, 60, 466):
        c = cost(N, otoc=True)
        print(f"  N={N}: T-depth per forward eval {c['Tdepth_eval']:.2e} -> {fmt_t(c['Tdepth_eval'] * 1e-6)} / {fmt_t(c['Tdepth_eval'] * 1e-5)};"
              f" inversion (1e3 gradient evals, P=4): {fmt_t(1e3 * c['Tdepth_grad'] * 1e-6)} / {fmt_t(1e3 * c['Tdepth_grad'] * 1e-5)}")
    # NISQ view: two-qubit gate count per circuit (each pair factor = one 2q gate, ~3 CNOT)
    print("\nNISQ two-qubit (fused pair) gates per OTOC circuit:")
    for N in (14, 30, 60, 120):
        c = cost(N, otoc=True)
        print(f"  N={N}: {c['rotations'] / 3:.2e} pair gates (~{c['rotations']:.2e} CNOT); fidelity at 1e-3/2q-gate ~ exp(-{c['rotations'] / 3 * 1e-3:.0f})")
