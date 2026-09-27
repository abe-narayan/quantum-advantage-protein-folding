# Break-even: when a quantum computer would beat the best classical method, with full accounting

_Discovery sprint, 2026-09-27. This file collects the break-even conditions for every quantum route this program examined. Derivations live in the source notes cited per section; this file states the inequalities, their inputs and the numbers, and adds the landscape-independent corollary and the NMR forward-model break-even (§4). Tags as in the source notes: DERIVED, THEORETICAL [key], INFERENCE, PILOT, UNPROVEN._

**Rule.** A quantum route "breaks even" only when C_quantum < C_classical with everything counted on both sides. Quantum: state preparation, oracle/Hamiltonian access, coherent arithmetic, walk or Trotter steps, phase-estimation and amplification overheads, shots, error correction, wall-clock. Classical: the **best validated classical portfolio** at matched accuracy, not the chain the quantum algorithm quantises. Below, ρ is the cost of one quantum-computer-second in core-seconds (ρ = 1 prices a 10⁷–10⁸-physical-qubit machine as one CPU core, which favours quantum).

---

## 1. Sampling a learned-energy structure posterior (QSA / quantum walk / quantum Langevin): QM-01, 03, 04, 05, 11, 12

Source: `PROOFS/T2_sampling_speedup_statement.md` S6, §3.6, §4.3; `RESOURCE_MODELS.md` (T3).

**Inequality (DERIVED).** Per independent posterior sample, the λ-path QSA wins iff

    τ_*  >  B* := (A · ρ · K · n_b · R)²,   R := G(L) · t_T / c(L)

- τ_*: relaxation time (local steps) of the quantised chain at the bottleneck;
- A := τ_*/B_best ≥ 1, where B_best is the best classical portfolio's cost per sample;
- K: per-stage QSA overhead (≈ 700 at stated constants; 10–10³ in tables);
- n_b: bottleneck-equivalent stages (1–2 for a single first-order crossing; up to ℓ);
- G(L): Toffolis per qubitised walk step. T3 final (with round-to-nearest fixed-point precision, b_w = 22–25 bits): D2 central 2.7×10⁷ – 1.4×10⁹ for L = 30–200 (G/L² ≈ 2.9–3.6×10⁴); D2 generous G/L² ≈ 0.8–1.0×10⁴; D3 Cartesian (a different, bond-relaxed target) 6.8×10⁶ – 6.1×10⁷. T2's tables below use the pre-precision T3 values, which are 1.2–1.9× lower, so they favour quantum;
- t_T: seconds per logical Toffoli;
- c(L): seconds per classical energy+gradient evaluation (≈ 0.6–2 ms, one core).

**Numbers (DERIVED from T3 + PILOT c(L)).** T3's own break-even at its default settings (S = 10³ classical cores, κ_min, c_q = 1, R = 100): B = 3.8–5.7×10¹⁷ (D2 central) and 3.0–4.8×10¹⁶ (D2 generous; T* ≈ 100–6,000 yr). Every break-even run needs ≥ 3.5×10¹² Toffolis, i.e. a CCZ error ≤ 3×10⁻¹⁴, beyond the assumed factory, so physical-qubit and time figures are lower bounds. T2's grid: B* = 1.0×10¹⁰ (Cartesian target, 1 µs Toffolis, K = 10, n_b = 1) to 1.1×10¹¹ (A80 target, most optimistic), ~10¹⁷ at central values, ~10²² with cited constants (170 µs, K = 10³), up to 9×10²⁴ pessimistic.

**Minimum useful runtime (DERIVED, landscape-independent).** At break-even the quantum wall-clock per sample is T*_Q = A·ρ·(K n_b G t_T)²/c. **No landscape, however hard, gives an advantage at a per-sample wall-clock below T*_Q.**

| scenario | L = 45 | L = 100 | L = 150 |
|---|---|---|---|
| T*_Q, Cartesian target, most optimistic (1 µs) | 0.26 yr | 0.53 yr | 0.59 yr |
| T*_Q, A80 target, most optimistic (1 µs) | 1.05 yr | 9.6 yr | 20 yr |
| T*_Q, central (10 µs, K = 100, n_b = 2) | 9×10⁵ yr | 9×10⁶ yr | 1.9×10⁷ yr |
| Toffoli time needed for T*_Q ≤ 1 day, A80 target, most optimistic | 51 ns | 17 ns | 12 ns |

**What classical costs we measured (PILOT/production, `results/PROCESSED/g1_summary.json`).**
- NRPT: 0 round trips within 2–4×10⁵ evaluations (L = 45–150), so classical cost > 10⁵–10⁶ per sample for this configuration. This is a lower bound for one method, not for the best classical method.
- Multistart census: gmean p_hit(best mode) ≈ 0.10 (L = 30) to 0.008 (L = 120) per restart of ~200 evaluations, i.e. ~2×10³–2.5×10⁴ evaluations per hit of the best-found basin.

**Status.** Theoretical level L2 (same-chain); L3 with T3's G(L). Relative-to-best: L0. Practical: **L0**. To reach break-even, the best classical method must need ≥ 10¹⁰–10¹¹ evaluations per sample at L ≤ 150. Even then T*_Q is months to decades per sample. Killed at the practical level (`discovery/KILLED_DIRECTIONS.md`).

## 2. Amplitude-amplified multistart / mode finding (QM-02, QM-11): T4

Source: `PROOFS/T4_amplified_mode_finding.md`.

**Inequality (DERIVED).** A coherent restart map A wins over i.i.d. classical restarts iff p_hit < p* := [(π/2)·ρ·O_rev·R_grad]⁻² (T2 I-5), with O_rev the reversibility overhead (pebbling 1.9–4.4×, worst-case-branch 1.25–3.2×) and R_grad the per-evaluation Toffoli-to-classical time ratio.

**Numbers.** p* = 6.7×10⁻¹⁹ – 1.0×10⁻¹¹ (L = 45) and 1.7×10⁻¹⁹ – 2.8×10⁻¹² (L = 100). Measured p_hit ≈ 10⁻² – 10⁻¹, so p_hit exceeds p* by ≥ 10⁹. With the hardware gate at 170 µs, T* ≥ 7.6×10³ yr for any map that evaluates the energy once per run. This compares only against i.i.d. restarts; adaptive classical search (basin hopping, PT, SMC) is not separated at all.

**Status.** L2 against i.i.d. restarts only; practical **L0**.

## 3. Precision estimation of posterior functionals (QM-14): T5 Theorem B

Quantum Θ(1/ε) vs classical Θ(1/ε²). At ε = 0.01 the query ratio is ≈ 27–100×. Each coherent query costs ≥ 10⁷ Toffolis (one energy), so the constant factor cannot be recovered (T5 §4.5). **L0 practical.**

## 4. Quantum forward model for protein ¹H NMR spin dynamics (QM-19/20/21)

Source: this sprint, `experiments/PREREGISTERED/PREREG_G1_C1_Q4.md` (C1), `discovery/NOVELTY_MEMOS.md` NM-1, results in `results/PROCESSED/nmr_gate2_summary.json`. **The numbers below are a model; they are finalised in §4.3 once C1 reports.**

**Task.** Infer geometry parameters θ (inter-proton distances, residue placements) from time-resolved NMR data s(t) (2-point transfer S_ab(t), or OTOC/echo F_ab(t)) of an oriented or static protein sample. The inference evaluates a forward model s(t; θ) and its derivatives at many candidate θ.

**Classical cost.** Exact: 2^N (sector-exact: C(N, N/2)³ per eigendecomposition; N = 14 ≈ 10–15 min on one core). Approximate: Pauli propagation (cost ~ number of strings, growing with operator weight), sparse Pauli dynamics, cluster methods, classical spins. **Classical cost is not the obstacle while an approximate method is accurate.** The relevant quantity is the **information gain** g = FI_total / FI_easy(t_c*): the factor by which a classical inversion that must discard t ≥ t_c* needs more experimental repetitions (or, if F_easy is singular, cannot identify some parameter combination at all).

**Quantum cost per forward evaluation (DERIVED, first-order Trotter as in the instrument).**
- Two-qubit dipolar pair gates per step ≈ N·z/2 (z = coupled neighbours within the cutoff; z ≈ 15–30 for ¹H at 5–6 Å).
- Steps n_T = t_max/dt ≈ 160 (320 µs at dt = 2 µs; smaller dt for strong couplings).
- One circuit: n_T·N·z/2 gates. N = 60 (O'Brien's ubiquitin cluster), z ≈ 15: ≈ 7×10⁴ pair gates; N = 466 (ubiquitin core): ≈ 6×10⁵.
- Shots: each circuit returns ±1 for one correlator, so a correlator to ±ε needs ~1/ε² shots (sampling) or ~1/ε (amplitude estimation, fault-tolerant).
- NISQ: 7×10⁴ two-qubit gates at 10⁻³ error gives fidelity ≈ e⁻⁷⁰. Infeasible without error correction.
- Fault-tolerant: each pair gate = 3 commuting rotations ≈ 3×(~30–50) T gates. N = 60 gives ≈ 10⁷ T per circuit, ~10 s at 1 µs/T. With amplitude estimation to ε = 3×10⁻³, ~300 circuits per (correlator, time), so ~1 h per (correlator, time, geometry). A gradient over P parameters × n_t times × n_b observables costs ~(2P+1)·n_t·n_b hours.

**Break-even condition (INFERENCE, stated for testing).** The quantum forward model pays only if both hold:
1. **Hardness.** The best classical approximation is biased (> σ) at times carrying a substantial share of the structural information (f_hard large), with the needed classical resource growing super-polynomially in N or t.
2. **Value.** The gain g is large enough that its price, g× more NMR acquisition time or non-identifiability, exceeds the quantum run time above. Classical inference can always buy precision with more repetitions of the easy-window experiment, so g is a sample-complexity factor. It is not an exponential separation unless F_easy is singular for a structurally relevant combination.

**Status before C1 results.** Theoretical: no separation proved for dipolar dynamics on protein geometries. Evidence of classical hardness for related echo dynamics: Google OTOC(2) [F30, F31] (random circuits, not dipolar protein networks). Practical: L0.
