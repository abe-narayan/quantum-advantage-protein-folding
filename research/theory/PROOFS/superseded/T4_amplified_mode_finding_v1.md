# T4. Cost of amplitude-amplified mode finding on the learned A80 energy

_Workflow task T4, written 2026-09-27. Status: **v1**. This file has a single writer. Companion script: `research/theory/PROOFS/T4_amplified_checks.py`. Checks C1–C6 are arithmetic plus a read of the G1 census JSONs and take under a minute on one core. Check C7 (`--energy`) reruns the small energy-based checks of §4.6 in about 20 minutes. Citation keys such as [B1] resolve in `research/literature/BIBLIOGRAPHY.md`. Keys [T4-n] are papers verified in this session that are not yet in the bibliography (§5.2). Every number from the G1 runs is **PILOT**: in-progress data, indicative only._

**Tags.** Every claim carries one of these tags.

| Tag | Meaning |
|---|---|
| **DERIVED** | Proved or computed here from the stated assumptions. The proof is in §3; numerical checks are in the script |
| **THEORETICAL [key]** | A result from the verified literature, used as its authors state it |
| **INFERENCE** | Reasoning from evidence that is not a proof. This includes cost constants and readings of pilot data |
| **UNPROVEN** | Open. Stated as a conjecture or a gap |
| **PILOT** | A number from the in-progress G1 runs (`research/results/RAW/g1_*`) or from this note's small checks |
| **A-x** | A labelled assumption (§2.6) |

**Claim levels.** No repository file defines the L0–L6 scale. This note uses the working table of the sibling note `T2_sampling_speedup_statement.md` so that the two stay consistent:

| Level | Kind | Meaning |
|---|---|---|
| L0 | — | No supported claim |
| L1 | theoretical | Query-model separation on a constructed instance family |
| L2 | theoretical | Query speedup for the stated problem class, under stated assumptions. Oracle cost excluded |
| L3 | theoretical | L2 plus the gate-level (Toffoli) cost of the oracle for the actual energy, giving a fault-tolerant runtime statement |
| L4 | practical | L3 plus the measured cost of the best classical portfolio, giving a projected resource advantage under stated hardware |
| L5 | practical | L4 plus small-scale compiled or simulated validation, with the crossover inside a practical wall-clock |
| L6 | practical | Hardware demonstration |

Theoretical and practical levels are reported separately throughout.

---

## 0. Summary

**Question.** The classical baseline draws restarts x₀ from the exact product prior π₀. It relaxes each one with a deterministic local optimiser Φ and keeps the best. A restart lands in the dominant (lowest-energy) basin with probability p_hit(L). The quantum alternative makes the map x₀ ↦ Φ(x₀) coherent and marks "E(Φ(x₀)) ≤ t", a native-free predicate. It then amplitude-amplifies: O(1/√p_hit) coherent runs instead of O(1/p_hit) classical runs. What does this cost end to end, and when would it win?

**Answer.** The quadratic query gain is real, optimal in the black-box model, and survives an unknown threshold. But one coherent relaxation costs so much, and its ratio to one classical relaxation is so nearly independent of L, that:
- on T3-baseline hardware a quantum win needs p_hit ≲ 10⁻¹⁸, and the win then takes ≳ 10⁹ years. With the most generous gate costs of the parallel T3 script the figures are ≲ 10⁻¹⁶ and ≳ 5×10⁶ years;
- a win inside one year needs logical Toffolis roughly 4×10³ to 2×10⁶ times faster than that baseline. The low end uses the most generous gate costs of the parallel T3 script (§4.5a); the high end uses this note's nominal costs with S = 10³ cores.

The measured p_hit(L) decides the question only in that second, hypothetical regime. **Theoretical level: L2, with the L3 cost derived here. Practical level: L0.** The kill of AA-2 / M9 (`literature/OPPORTUNITY_MATRIX.md`) is confirmed, now with explicit numbers.

1. **Query statements.**
   - Classical i.i.d. restarts need Θ(1/p) runs. (DERIVED)
   - Amplitude amplification of a coherent restart map A needs π/(2√p) applications of A or A⁻¹ for near-certain success, or an expected 1.38/√p if runs are repeated until success [B1]. Ω(1/√p) is a lower bound [C55, T4-5]. (THEORETICAL + DERIVED constant)
   - With an **unknown threshold**, a Dürr–Høyer-style "record process" over basins reaches the lowest basin with an expected ≤ 1 + 2c_QS·(w₁^{−1/2} − 1) < 2c_QS/√w₁ applications of A. Here w₁ = p_hit and c_QS is the constant of the unknown-p search of [B1]. On the measured basin-mass spectra the realised constant is 1.56–1.78·c_QS. (DERIVED; §3.3, check C3)
2. **The coherent relaxation cannot be cheap.** Four structural facts, all DERIVED:
   - (a) Relaxation is many-to-one. Any unitary embedding needs ancilla ≥ log₂ of the largest basin fibre, so x₀ must be kept (§3.4).
   - (b) Intermediate iterates must be pebbled. The exact reversible-pebbling trade-off gives, for K = 400 steps, time overheads of 5.9× (10 pebbles), 3.3× (16) and 2.4× (24) (§3.5, check C1).
   - (c) A circuit pays the worst case over branches: the maximum number of iterations and of line-search trials, with no early abort and no data-dependent sparsity. Classical L-BFGS averages 174–218 gradient evaluations per restart (PILOT census, L = 30–100). Its coherent worst case under the same line-search budget is about 2,400, 11.5 times more (§3.6). Variable-time amplitude amplification [T4-13] can recover much of this penalty in principle.
   - (d) A reversible gradient step on the A80 energy touches all (L−2)(L−3)/2 pairs. Coherent circuits cannot use cut-offs, because the pair distances are in superposition.
3. **Gate cost** (INFERENCE; labelled constants, §3.7):
   - Toffolis per reversible gradient step: C_step(L) ≈ 3.1×10⁴·(L−2)(L−3) + 10⁶·L. That is 1.6×10⁸ at L = 60, 3.9×10⁸ at L = 100 and 8.2×10⁸ at L = 150. The dominant cost is the O(L²) pair loop: fixed-point distance arithmetic (≈ 70% at b = 20) plus lookups in the pair-specific soft tables (≈ 30%). The tables are compiled into the circuit as classical data (no QRAM).
   - One coherent relaxation needs 10³–10⁴ gradient-step equivalents, i.e. 10¹¹–10¹³ Toffolis at L = 60–150. The parallel T3 script's gate costs give 0.4–2× these (§4.5a).
   - Logical qubits: 1.6×10⁵ (GD-type state, 24 pebbles) to 1.8×10⁶ (L-BFGS state, 24 pebbles) at L = 100.
4. **Break-even** (DERIVED from the Babbush form [B46]).
   - Formulas:
     - p* = (t_C / (c·S·t_Q))²
     - T* = c²·S·t_Q²/t_C

     Here t_C is the time of one classical restart plus relaxation on one core, t_Q the time of one application of A, c ≈ 1.38, and S the number of classical cores.
   - **T\* does not depend on p.** Any quantum win takes at least T* of quantum wall-clock (§3.9).
   - The ratio R = t_Q/t_C is almost independent of L, because both sides scale as L². It is about 4×10⁸ at the 170 µs baseline for the most quantum-favourable map. So p* is roughly constant in L, and T* grows as L².
   - Numbers (map M-LB2: K_eff = 400 gradient evaluations, 24 pebbles; §4.5):

| t_Tof | L | p* (S = 1) | T* (S = 1) | p* (S = 10³) | T* (S = 10³) |
|---|---|---|---|---|---|
| 170 µs (T3 baseline) | 60 / 100 / 150 | 2.7 / 3.5 / 4.1 ×10⁻¹⁸ | 0.7 / 1.5 / 2.9 ×10⁹ yr | ~10⁻²⁴ | ~10¹² yr |
| 1 µs (optimistic future) | 60 / 100 / 150 | 0.8 / 1.0 / 1.2 ×10⁻¹³ | 2.5 / 5.2 / 10 ×10⁴ yr | ~10⁻¹⁹ | ~10⁷–10⁸ yr |
| 1 ns (hypothetical) | 60 / 100 / 150 | 0.8 / 1.0 / 1.2 ×10⁻⁷ | 9 / 19 / 37 days | ~10⁻¹³ | 25 / 52 / 100 yr |

5. **Measured p_hit(L)** (PILOT; G1 mode census, 256 restarts per crop, T = 1):
   - Median p_hit is 0.12 / 0.11 / 0.05 / 0.06 / 0.016 at L = 30 / 45 / 60 / 80 / 100 (16 crops each).
   - In 6–25% of crops the best mode was hit only once (p ≤ 1/256, censored).
   - The per-protein slope over L = 30–100 is d ln p/dL ≈ −0.030 per residue (IQR −0.040 to −0.008).
   - The largest call-count saving amplitude amplification could deliver is 1/(1.38√p): **≈ 2–6× at the median crop (L = 30–100) and ≤ 12× at the censoring floor.** It has to pay a per-call overhead R ≈ 2×10³ (hypothetical 1 ns) to 4×10⁹ (baseline). (DERIVED arithmetic on PILOT data)
6. **Decision criterion.** Stated in measured quantities, in two gates (§3.12):
   - **Hardware gate, independent of p:** T*(L) = c²·S·t_Q(L)²/t_C(L) ≤ W_max.
   - **Instance gate:** the best classical time-to-target TTT_C(L) = t_C^best/(S·p_C) must exceed c·t_Q(L)/√p_Q(L), and c·t_Q/√p_Q ≤ W_max.
   - The hardware gate fails at every L ≥ 30. At 170 µs it fails by ≥ 7×10⁸ with nominal gate costs and ≥ 5×10⁶ with T3's most generous costs. At 1 µs (S = 1) it fails by ≥ 10⁴ and ≥ 1.8×10² respectively; at S = 10³, by 10³ times more. **No p_hit(L) measurement can reverse that.**
   - The gate passes only if t_Tof ≲ 3–6 ns (S = 1; ≲ 16–39 ns with T3's most generous costs) or ≲ 0.1–0.2 ns (S = 10³; ≲ 0.5–1.2 ns).
   - Even then, the instance gate needs p_Q ≲ 10⁻⁷ at S = 1 (≲ 3×10⁻⁶ with T3's most generous costs). The pilot median reaches those values only near L ≈ 500 and ≈ 390 respectively (≈ 380 and ≈ 300 on the steep quartile). Only the censored hard tail at L = 60–100 could enter earlier, and it is unmeasured.
7. **Classical counterarguments** (§3.10–3.11). Each one only widens the gap:
   - classical parallelism enters p* as S⁻², while S_Q independent quantum machines gain only √S_Q [T4-5];
   - better classical proposals raise p, and the quantum call saving shrinks as √p;
   - adaptive and population methods (PT, basin hopping, SMC, PERM, fragment assembly) and learned proposals are not i.i.d. restarts, so the 1/p lower bound does not bind them, and their coherent versions are either far costlier or are Markov chains (a T2 question, not amplitude amplification);
   - on this program's evidence the argmin is the wrong output for accuracy: restart saturation leaves ≤ 0.14 Å headroom at 44–60 aa (S33 R10).

### Statement table

| # | Statement (short) | Tag | Theoretical level | Practical level |
|---|---|---|---|---|
| S1 | Classical i.i.d. restarts: expected 1/p runs; ⌈ln(1/δ)/p⌉ for confidence 1−δ; Ω(1/p) in the i.i.d.-restart model | DERIVED | lower bound in the restart model only | — |
| S2 | AA with coherent A: π/(2√p) applications of A/A⁻¹ (success ≥ 1−p); expected 1.38/√p with repetition; Ω(1/√p) optimal | THEORETICAL [B1, C54, C55, T4-5] + DERIVED constant | L2 | L0 |
| S3 | Unknown threshold: record process reaches the best basin in E[N_A] ≤ 1 + 2c_QS(w₁^{−1/2} − 1); realised constant 1.56–1.78 on measured spectra | DERIVED (extends [C56]) | L2 | L0 |
| S4 | Irreversibility floor: ancilla ≥ log₂ max_y \|Φ⁻¹(y)\| ≥ H_min(π₀) + log₂ w_j bits for a converging relaxation | DERIVED | structural (space) | fixes the space floor |
| S5 | Exact reversible-pebbling time/space table for K-step relaxation | DERIVED (constructive; BFS-checked for small cases) | L3 ingredient | — |
| S6 | A coherent circuit pays max-branch cost (iterations, line search, pair sparsity); penalty ≈ 11.5× for classical L-BFGS settings at L = 45 | DERIVED + PILOT | L3 ingredient | — |
| S7 | C_step(L) ≈ 3.1×10⁴(L−2)(L−3) + 10⁶L Toffolis per reversible gradient step (b = 20) | INFERENCE (labelled constants) | L3 ingredient | — |
| S8 | Logical qubits 0.9–2.6×10⁵ (GD-type) to 1.0–2.6×10⁶ (L-BFGS m = 8) at L = 60–150, 24 pebbles | INFERENCE | — | — |
| S9 | p* = (t_C/(cSt_Q))², T* = c²St_Q²/t_C; any quantum win runs ≥ T*; R and p* are ≈ L-independent, T* ∝ L² | DERIVED (form of [B46]) | L3 | **L0: KILL at T3 baseline and at 1 µs** |
| S10 | Parallelism: classical S enters p* as S⁻²; quantum only √S_Q | DERIVED + THEORETICAL [T4-5] | — | widens the gap |
| S11 | Better proposals: W_Q/W_C = c·S·R·√p for any coherently runnable procedure; the quantum-runnable set is a subset of the classical set | DERIVED + INFERENCE | — | widens the gap |
| S12 | Decision criterion: hardware gate T* ≤ W_max (p-independent), then instance gate on p_Q(L), p_C(L) | DERIVED (conditions) + INFERENCE (extrapolation) | — | decisive |

---

## 1. Statements

### S1. Classical restarts (DERIVED)
Let each restart independently land in the marked set G with probability p.
- The number of restarts to the first hit is geometric with mean 1/p.
- Confidence 1−δ needs N_C(δ) = ⌈ln(1/δ)/(−ln(1−p))⌉ ≤ ⌈ln(1/δ)/p⌉ restarts.
- Wall-clock on S cores is ⌈N_C/S⌉·t_C.
- In the **i.i.d.-restart access model**, where an algorithm sees only independent runs of Φ and their energies, Ω(1/p) runs are necessary.
- **Scope.** This lower bound does *not* apply to adaptive classical methods, such as basin hopping, PT or SMC. They are not i.i.d. restarts (S11).

### S2. Amplitude amplification with a coherent restart map
- **Setup.** Suppose A|0⟩ = √p|ψ_good⟩ + √(1−p)|ψ_bad⟩, where "good" is decided by a phase oracle S_χ computed from A's output registers.
- **Iteration count.** After m iterations of Q = −A S₀ A⁻¹ S_χ the success probability is sin²((2m+1)θ), with sin²θ = p [B1]. m = ⌊π/(4θ)⌋ gives success ≥ 1−p with 2m+1 ≈ π/(2√p) applications of A or A⁻¹ (THEORETICAL [B1]).
- **Output law.** On success, the output is distributed as π₀ restricted to G and pushed through Φ, because amplification preserves relative amplitudes inside the good subspace [B1]. So an amplified run returns the same kind of object as a lucky classical restart (THEORETICAL [B1]).
- **Expected-cost constant.** Repeating an m-iteration run until a measured success gives expected (2m+1)/sin²((2m+1)θ) applications. The minimum over m is ≈ **1.3801/√p**, attained at (2m+1)θ = φ* with tan φ* = 2φ* (φ* = 1.1656) (DERIVED; check C2). This note uses **c = 1.38** in all break-even formulas, which is quantum-favourable.
- **Optimality.** Any algorithm that uses A only as a black box needs Ω(1/√p) applications [C55]. Grover's constant is optimal for any success probability [T4-5] (THEORETICAL).
- **Garbage inside A is harmless.** A may leave its history registers dirty, because A⁻¹ undoes them in the next iteration (DERIVED; §3.2).

### S3. Unknown threshold: Dürr–Høyer on basin masses (DERIVED)
Order the basins by energy e₁ < e₂ < …, with prior masses w_j and W_j = Σ_{i≤j} w_i.
- **Procedure.**
  1. Measure one run of A. Its outcome basin is j₀ ~ w.
  2. Repeat: run the unknown-p search QSearch of [B1] (its QSearch theorem) with marked set {E(Φ(x₀)) < e_current}.
- **Lemma.** Basin j is ever the current threshold with probability exactly w_j/W_j.
- **Theorem.** The expected number of applications of A before the current basin is basin 1 satisfies

  E[N_A] ≤ 1 + c_QS · Σ_{j≥2} (w_j/W_j)·W_{j−1}^{−1/2} ≤ 1 + 2c_QS·(w₁^{−1/2} − 1) < 2c_QS/√w₁,

  where c_QS·a^{−1/2} bounds the expected cost of QSearch at success probability a [B1, T4-6].
- **Stopping.** Nothing signals arrival at basin 1. Both sides therefore stop on a budget set by a prior lower bound p_min. The quantum budget is 4c_QS/√p_min per round, which fails with probability ≤ 1/2 by Markov; r rounds fail with probability ≤ 2^{−r}. The classical budget is ln(1/δ)/p_min.
- **Measured constant.** On the measured basin spectra (PILOT census) the realised E[N_A]·√w₁/c_QS is 1.56–1.78 (median by length; maximum 1.83), against the bound 2 (check C3).
- This is the continuous, prior-weighted analogue of [C56]. [C56] finds the minimum of N items in O(c√N) with probability ≥ 1 − 2^{−c}, by its abstract.

### S4. Irreversibility floor (DERIVED)
Let Φ: Ω → Ω be deterministic on the b-bit grid Ω, with |Ω| = 2^{Db}.
- **Claim.** Any reversible (basis-permuting) circuit that maps |x⟩|0^a⟩ to |Φ(x)⟩|j(x)⟩ needs a ≥ log₂ max_y |Φ⁻¹(y)|.
- **For a converging relaxation.** Suppose Φ collapses basin B_j onto one grid point. Then a ≥ log₂|B_j| ≥ H_min(π₀) + log₂ w_j, where H_min(π₀) = −log₂ max_x π₀(x).
- **Consequence 1.** No "in-place" coherent optimiser exists. The information a relaxation discards must be parked in ancilla. The natural parking is to keep x₀ itself (n = Db qubits), which A does anyway. The floor is ≥ H_min(π₀) + log₂ w_j and at most n, so keeping x₀ costs at most a small constant factor more than the floor. The consequence that matters is the qualitative one: the discarded information cannot be erased in place.
- **Consequence 2.** A momentum method made exactly reversible by an information buffer [T4-9] must buffer at least this much. Its buffer grows by D·log₂(1/γ) bits per step.

### S5. Reversible pebbling of K relaxation steps (DERIVED)
Node k of the pebble game is the iterate x_k. The input x₀ is always available. Placing or removing a pebble on node k costs one reversible step, Toffolis C_step, and needs node k−1 pebbled.

Inside A the final configuration may keep garbage pebbles. The minimum number of step applications G(K, s) with ≤ s pebbles then obeys

G(K, s) = min( K [if K ≤ s], min_{1≤m<K} F(m, s) + G(K−m, s−1) ),
F(K, s) = min_{1≤m<K} F(m, s) + F(K−m, s−1) + F(m, s−1),  F(1, s) = G(1, s) = 1.

Here F is the clean variant, which ends with only node K pebbled.
- **Reach.** With s pebbles, F reaches K = 2^{s−1} and G reaches K = 2^s − 1.
- **Verification.** The recursions agree with exhaustive search for K ≤ 8 and s ≤ 4 (check C1).
- **Overheads.** Time overhead ρ = G(K, s)/K for the number of pebbles s:

| K | s = ⌈log₂(K+1)⌉ | s = 12 | s = 16 | s = 20 | s = 24 | s = 32 | s = 40 |
|---|---|---|---|---|---|---|---|
| 256 | 5.44 (s = 9) | 3.34 | 2.88 | 2.28 | 1.91 | 1.88 | 1.84 |
| 400 | 8.39 (s = 9) | 4.38 | 3.28 | 2.90 | 2.44 | 1.92 | 1.90 |
| 1,024 | 9.62 (s = 11) | 7.32 | 4.82 | 3.57 | 3.39 | 2.94 | 2.36 |
| 2,400 | 14.36 (s = 12) | 14.36 | 6.64 | 5.44 | 3.80 | 3.55 | 3.30 |
| 4,096 | 16.54 (s = 13) | — | 9.38 | 6.50 | 5.47 | 3.73 | 3.59 |

- **Space.** s × (state size) + workspace. The state is D·b qubits for GD, or (2m+2)·D·b for L-BFGS with memory m.
- **Per Grover iteration.** Each iteration applies A and A⁻¹, so it costs 2·G(K, s)·C_step Toffolis plus the cost of preparation and marking.

### S6. Coherent worst-case penalty (DERIVED + PILOT)
A circuit has a fixed gate sequence, so it pays for every data-dependent branch. Two cases, then the numbers:
- **Loops.** Loop exits (the convergence test) and line-search acceptances are unrolled to their maxima.
- **Sparsity.** Distance-based sparsity, such as neighbour lists or constant far tails of the tables, cannot be exploited. The pair distances are in superposition, so every pair is computed.
- **Classical L-BFGS numbers (PILOT).**
  - At L = 45, 64 single restarts use a mean of 209 gradient evaluations, median 222, maximum 261 (check C7).
  - Across the census the mean is 174–218 per restart for L = 30–100.
  - The coherent worst case at the classical settings (200 iterations × up to 12 Armijo trials) is 2,401 evaluations. That is **≈ 11.5× the classical mean**.
  - Truncating the line search reduces the penalty but changes Φ, and so changes p. Whether a 2-trial coherent L-BFGS (map M-LB2, K_eff ≈ 400) keeps p is UNPROVEN.
- **Mitigation.** Variable-time amplitude amplification [T4-13] replaces t_max by √(Σ t_i²)-type costs, up to polylog factors. It could in principle recover most of this penalty; M-LB2 roughly represents that case (INFERENCE).

### S7. Toffolis per reversible gradient step (INFERENCE; constants A-T1–A-T6)

C_step(L) = c_pair·(L−2)(L−3)/2 + c_res·L,

with c_pair ≈ 2·4·(12b² + 2G_tab + 12b) + 12b² ≈ 6.1×10⁴ and c_res ≈ 10⁶ at b = 20 and G_tab = 1,001.

| L | 30 | 45 | 60 | 80 | 100 | 150 |
|---|---|---|---|---|---|---|
| C_step nominal (b = 20) | 5.3×10⁷ | 1.0×10⁸ | 1.6×10⁸ | 2.6×10⁸ | 3.9×10⁸ | 8.2×10⁸ |
| b = 16 / b = 24 | 4.5 / 6.3 ×10⁷ | 0.8 / 1.2 ×10⁸ | 1.3 / 2.0 ×10⁸ | 2.1 / 3.3 ×10⁸ | 3.1 / 4.9 ×10⁸ | 6.3 / 10.4 ×10⁸ |
| aggressive (b = 16, ½b² multiply, QROAM lookups) | 3.6×10⁷ | 6.1×10⁷ | 9.1×10⁷ | 1.4×10⁸ | 1.9×10⁸ | 3.7×10⁸ |
| pair-term share (nominal) | 0.44 | 0.55 | 0.63 | 0.70 | 0.74 | 0.82 |

- **Consistency with T2 and T3.** The T2 placeholder, G_grad = 3gL² with g ∈ [5×10³, 3×10⁴] (T2 A-G), brackets these values. The parallel T3 script gives 3·C_E between 0.4× (spline design D2) and 2× (literal-table design D1) of C_step (§4.5a).
- **Scaling.** T* ∝ C_step². At 170 µs the verdict of S9 survives a C_step overestimate of up to ~2×10⁴. At 1 µs it survives an overestimate of up to ~10² with S = 1, or ~3×10³ with S = 10³.

### S8. Qubits (INFERENCE)
Logical qubits = x₀ register D·b + s pebbles × state + gradient workspace (≈ 29·L·b). With b = 20 and s = 24:

| L | GD / heavy-ball state (D·b per pebble) | L-BFGS m = 2 (6D·b) | L-BFGS m = 8 (18D·b) | Heavy-ball + buffer, K = 10⁴, γ = 0.9, no pebbles |
|---|---|---|---|---|
| 60 | 9.2×10⁴ | 3.7×10⁵ | 1.0×10⁶ | 2.2×10⁵ |
| 100 | 1.6×10⁵ | 6.2×10⁵ | 1.8×10⁶ | 3.7×10⁵ |
| 150 | 2.3×10⁵ | 9.4×10⁵ | 2.6×10⁶ | 5.5×10⁵ |

- **Physical data qubits.** At about 2d² ≈ 1.9×10³ physical per logical (d ≈ 31, A-Q), the data qubits alone come to 2×10⁸–5×10⁹ physical.
- **Factories.** Reaching t_Tof = 1 µs by factory parallelism needs about 170 factories, ≈ 2.6×10⁷ physical qubits. Reaching 1 ns this way needs 1.7×10⁵ factories, ≈ 2.6×10¹⁰ physical qubits. **So "1 ns" is a new-paradigm scenario, not "more factories".** This counts ~1.5×10⁵ physical qubits per factory region [A56, as recorded in `lit_A_sampling.md`].

### S9. Break-even (DERIVED)
Assume the classical side can run the same map at cost t_C per run, with the same p. Then:
- Classical time-to-target is W_C = t_C/(S·p).
- Quantum time-to-target is W_Q = c·t_Q/√p.
- **Advantage.** W_Q < W_C ⟺ p < p* := (t_C/(c·S·t_Q))².
- **Break-even runtime.** At p = p* both take T* := c²·S·t_Q²/t_C. This is [B46]'s eq. (5) with d = 2 and the constant c. For every p < p*, W_Q = c·t_Q/√p > T*, so **any quantum win takes at least T* of quantum wall-clock.**
- **Window.** With a tolerable wall-clock W_max, a useful win needs (c·t_Q/W_max)² ≤ p < p*. The window is non-empty iff T* < W_max.
- **L-dependence.**
  - Both t_Q (∝ C_step) and t_C (∝ t_grad) scale as L² for large L. So R(L) = t_Q/t_C → const: ≈ 3.6–4.4×10⁸ for M-LB2 at 170 µs over L = 60–150.
  - Hence p*(L) ≈ (c·S·R)^{−2} is nearly constant, and T* ∝ L².
  - **Longer chains make the hardware gate harder, not easier.** The instance gate becomes easier only if p(L) falls.

### S10. Parallelism (DERIVED + THEORETICAL)
- **Classical.** Restarts are embarrassingly parallel: S cores give S× in wall-clock, and p* ∝ S⁻².
- **Quantum.** Quantum search cannot be parallelised better than by splitting the search space over independent machines [T4-5]. S_Q machines give only √S_Q.
- **Equal machine counts.** Against S classical cores, S quantum computers have p* = (t_C/(c·t_Q))²/S.
- **In practice.** One fault-tolerant machine here is 10⁸–10⁹ physical qubits (S8), while S = 10³–10⁵ classical cores is routine. Batching already amortises the energy up to ≈ 15× per core at B = 64 (L = 45; PILOT timing, §4.1).

### S11. Better classical proposals (DERIVED + INFERENCE)
Take any randomised procedure B: a proposal law plus relaxation plus a marking rule. It has hit probability p(B), classical per-run time t_C(B) and, if it can be made coherent, per-run time t_Q(B). Then

W_Q(B)/W_C(B) = c·S·R(B)·√p(B), with R(B) = t_Q(B)/t_C(B).

Three consequences:
- **(a) Which procedures the quantum side can amplify (DERIVED).** Every coherent A is a classical reversible circuit fed by a superposition of random bits. Fed classical random bits, the same circuit produces the same output law. So the procedures amplitude amplification can amplify form a subset 𝒬 of the classical procedures 𝒞. The comparison is min_{B∈𝒬} W_Q(B) against min_{B∈𝒞} W_C(B).
- **(b) Better proposals shrink the gain (DERIVED).** For any B the call saving is at most 1/(c·√p(B)). A classical improvement that raises p by g at cost factor h leaves the classical side better off by g/h. It cuts the quantum side's maximal relative gain by √g.
- **(c) The strong classical methods do not fit into 𝒬 cheaply (INFERENCE).** Four families:
  - **Population methods** (SMC [B65 = E74], PERM [D41 = E53], growth algorithms [C84 = E54], fragment regrowth [E55]) need N-particle coherent populations with reversible resampling.
  - **Adaptive search** (basin hopping [T4-11], Monte Carlo minimisation [T4-10], PT [C77 = E20, E33]) is a Markov chain, not i.i.d. restarts. Its quantum analogue is walk or QSA acceleration, the T2 question [A8, A31, A44].
  - **Fragment assembly** [T4-12] is a Monte Carlo chain over fragment insertions, so the same applies.
  - **Learned proposals** (Boltzmann generators [A78 = E76], sequential BGs [E79], AlphaFlow [E80], BioEmu [A79 = E83]) run 10⁸–10¹⁰-MAC networks per sample, which is 10¹⁰–10¹³ Toffolis if made coherent. They can also drive p toward O(1), which leaves nothing to amplify.

### S12. Decision criterion in measured quantities (DERIVED conditions; INFERENCE extrapolation)
Define the measured quantities:
- **p_Q(L):** the hit probability of the coherently implementable map (b-bit fixed point, fixed K, fixed line-search budget) from the product prior. It is measurable **classically**, by running the same deterministic map.
- **p_C(L) and t_C^best(L):** the hit probability and per-run cost of the best classical portfolio. TTT_C(L) = t_C^best/(S·p_C).
- **t_Q(L):** from T3 (Toffolis × t_Tof).

Amplitude-amplified mode finding is relevant at length L **iff both gates hold**:

**(H) hardware gate, independent of p:** T*(L) = c²·S·t_Q(L)²/t_C^map(L) ≤ W_max;

**(I) instance gate:** c·t_Q(L)/√p_Q(L) ≤ min(W_max, TTT_C(L)).

- **Gate H at T3-baseline and 1 µs hardware.** It fails at every L ≥ 30 (§4.5, §4.5a). With nominal gate costs it fails by ≥ 7×10⁸ at 170 µs, and by ≥ 10⁴ at 1 µs with S = 1 (≥ 10⁷ at S = 10³); T* ≈ 1.1×10⁴ yr at L = 30 and grows as L². With the T3 script's most generous gate costs the margins are ≥ 5×10⁶ (170 µs) and ≥ 1.8×10² (1 µs, S = 1). The practical question is then closed whatever p_hit(L) turns out to be (**KILL**, practical L0).
- **Hypothetical hardware.** Gate H passes only for t_Tof ≲ 3–6 ns (S = 1) or ≲ 0.1–0.2 ns (S = 10³). With T3's most generous gate costs the limits are ≲ 16–39 ns and ≲ 0.5–1.2 ns, and p* rises about 30-fold. Gate I then needs p_Q ≲ 10⁻⁷ (S = 1) with p_Q ≥ (c·t_Q/W_max)² ≈ 5×10⁻¹¹–10⁻⁹, and no classical method may reach the basin more cheaply.
- **Pilot extrapolation.** The median slope (−0.030 per residue over L = 30–100) puts median crops at p ≈ 10⁻⁷ only near L ≈ 500, and at T3-generous p* ≈ 3×10⁻⁶ near L ≈ 390. Only the censored tail at L = 60–100 (19–25% of crops) might enter earlier, and it has not been measured (INFERENCE).

---

## 2. Model and assumptions

### 2.1 Energy, coordinates, prior
- **Coordinates.** Internal coordinates x = (θ₁…θ_{L−2}, τ₁…τ_{L−3}), with D = 2L − 5. Structures are rebuilt with ideal 3.8 Å Cα bonds (`src/qapf/protein/energy.py`, `build_ca`).
- **Energy (A-E).** E(x) = E_prior(x) + E_pair(x), the vendored A80 energy at T = 1.
  - E_prior = w_tt·Σ_i −log P̃_i(θ_i, τ_i) + w_w·wall(θ). It is a product over residues.
  - E_pair = Σ_{j−i≥3} [−log p̃^CA_ij(d_ij) − log p̃^CB_ij(d^cb_ij)] + w_s·Σ relu(r₀ − d_ij)².
  - The soft tables p̃_ij are **pair-specific**. Each is a 1,001-point grid on 0–50 Å, derived from esmprior_v1 pair-distance bin probabilities (28 bins) by Gaussian soft-binning (σ = 0.5 Å).
  - Pairs: P(L) = (L−2)(L−3)/2 (903, 1,653, 4,753 and 10,878 at L = 45, 60, 100 and 150).
- **Prior (A-P).** π₀ ∝ exp(−E_prior/T), the λ = 0 end of the G1 path. It is exactly sampleable residue by residue on a 0.5° × 1° grid (360 × 360 = 129,600 cells per residue), with uniform jitter inside cells (`hrex.ExactPrior`).

### 2.2 Relaxation maps and basins
- **Classical map Φ_C.** Batched L-BFGS (m = 8, ≤ 200 iterations, Armijo backtracking with ≤ 12 trials, relative-decrease stopping), `energy.lbfgs`. Float64.
- **Coherent candidate maps (A-Φ).**

| Map | Description | Gradient-step equivalents per run |
|---|---|---|
| **M-LB2** | L-BFGS, 200 iterations, 2 line-search trials per iteration, b-bit | K_eff = 400; the VTAA-like, quantum-favourable nominal |
| **M-LB12** | Classical settings (12 trials) unrolled | K_eff = 2,400 |
| **M-HB** | Heavy-ball momentum made exactly reversible with an information buffer [T4-9] | K ≈ 10⁴ steps, no pebbling |
| **M-GD** | Fixed-step gradient descent | K ≫ 10⁴ (§4.6) |

- **Basins (A-B).** Clusters of relaxed endpoints at 2 Å Cα-RMSD, as in the census (`scripts/g1_mode_census.py`). Basin j has energy e_j (idealised as one value per basin) and prior mass w_j = π₀(Φ⁻¹(basin j)). **p_hit := w₁**, the mass of the lowest-energy basin found.
  - PILOT caveat: the census's best mode is the best among 256 restarts, not necessarily the global minimum. At L = 45, PT reached lower energy than multistart (T5 §4.3).
- **Marking predicate.** χ_t(x₀) = [E(Φ(x₀)) ≤ t]. It is native-free: it uses the learned energy only, and t is a classical number chosen by the algorithm from its own earlier measurements.

### 2.3 Classical cost model
- **A-C1.** One energy+gradient on one core takes t_g(L) = 1.8 ms·(L/150)², scaled from the orchestrator-reported 1.8 ms at L = 150 (PILOT) as L² (the pair terms dominate).
  - A measurement in this session on a machine at ~84% load gave 0.35 / 0.59 / 1.63 / 5.93 ms per structure at L = 45 / 60 / 100 / 150 in batches of 64, and 5–10 ms unbatched (torch overhead).
  - An optimised C or GPU kernel with neighbour lists would plausibly be 10–100× faster (INFERENCE). That lowers p* by 10²–10⁴.
- **A-C2.** One classical restart costs t_C = K_C·t_g, with K_C = 209. The PILOT mean is 209 at L = 45; the census mean is 174–218 over L = 30–100. Prior sampling cost is negligible.
- **A-C3.** S ∈ {1, 10³} independent cores.

### 2.4 Quantum cost model ("T3 resource model")
The T3 note had not been written when this note was drafted. This note uses the same scenario set as the sibling notes T2 (A-t) and T5 ([AS3]), plus a hypothetical extreme. T3's script appeared during this work: its Toffoli time (170 µs, one CCZ factory, d = 31) matches A-t, and its gate costs are used as a cross-check in §4.5a. If T3's final note gives a different Toffoli count G(L), rescale: p* ∝ G⁻² and T* ∝ G².

- **A-t.** Logical Toffoli time t_Tof:
  - **170 µs**: the T3 baseline. Surface code with d ≈ 31, 1 µs cycles, one CCZ factory [A56, B46].
  - **1 µs**: optimistic future, as in T2/T5.
  - **1 ns**: hypothetical, of the order Lemieux et al. say is needed to match a special-purpose classical MCMC machine at a quadratic speedup [A55]. It is used only to show what hardware would have to do.
- **A-Q.** Clifford gates are free. Qubits are counted separately (S8). Physical per logical ≈ 2d² with d ≈ 31. Surface-code decoding cost is ignored [C63], which favours the quantum side.
- **A-c.** c = 1.38 (S2), quantum-favourable. The unknown-threshold record process multiplies this by ≈ 1.6·c_QS/1.38 (S3).
- **A-W.** W_max = 1 year where a single number is needed.
- **A-map.** p_Q = p_C for the coherent map, unless stated otherwise. This is a convenience, not a bound: §4.6 shows that p changes between maps in both directions, so p_Q must be measured for the actual coherent map (G2).

### 2.5 Oracle discipline (what is and is not assumed)
- **No free oracles.** All components below are explicit circuits, counted in S7:
  - **Prior preparation.** ⊗_i Σ_c √π_i(c)|c⟩ ⊗ (Hadamard jitter), prepared per residue from a 129,600-entry classical table. Cost ≈ one table-size lookup per residue: ~1.3×10⁵ Toffolis by unary iteration ([A60], cost claim unverified), or ~6×10³ by the dirty-qubit trade-off [T4-7] (λ ≈ 40). The total ≤ 2×10⁷ at L = 150 is below 10⁻⁴ of one relaxation.
    - This is legitimate *only because* π₀ is a product of low-dimensional factors. Loading a correlated conformational law this way would fall under the Grover–Rudolph no-go [B36, B37].
  - **Energy tables.** The per-pair and per-residue tables are classical data compiled into the circuit. The circuit loops over pairs, so pair indices are classical and only the distances are quantum. No QRAM is used. Computing the tables from the sequence (esmprior_v1 forward pass) is the same classical preprocessing the classical side pays.
  - **Marking.** Computed from the output registers. With the energy kept as an output of A, marking is a b-bit comparator.
- **No native structure anywhere.** RMSD appears only in the classical census clustering, relative to relaxed endpoints, never to the native (DEP path).
- **No simulation was run.** All quantum numbers are resource-model arithmetic. Simulator ≠ hardware, and query count ≠ runtime.

### 2.6 Assumption table

| Label | Assumption | Used in | Direction if wrong |
|---|---|---|---|
| A-E | Energy exactly as vendored (T = 1, DEFAULT_W) | all | — |
| A-P | Prior grid 0.5° × 1° with jitter; b-bit discretisation does not change basin masses materially | S2, S3 | UNPROVEN; measurable classically |
| A-Φ | Coherent maps M-LB2 / M-LB12 / M-HB / M-GD as defined | S6, S9 | M-LB2 is favourable to quantum |
| A-B | One energy per basin; clusters at 2 Å | S3 | Intra-basin energy spread adds extra record levels (hurts quantum) |
| A-C1 | t_g = 1.8 ms·(L/150)² per core | S9 | A faster classical kernel hurts quantum quadratically |
| A-C2 | K_C = 209 gradient evaluations per restart | S9 | PILOT |
| A-T1 | b = 20-bit fixed point (sensitivity 16–24) | S7 | ±25% in C_step |
| A-T2 | b×b multiply ≈ b² Toffolis (schoolbook; [A59] has optimised variants, constants not re-verified) | S7 | aggressive variant ½b² |
| A-T3 | sqrt, reciprocal, division ≈ 2b² each | S7 | INFERENCE |
| A-T4 | Lookup of 2 adjacent entries from a G_tab = 1,001-entry classical table at a quantum index ≈ 2·G_tab Toffolis (unary; [A60], cost unverified); aggressive ≈ 4√(2b·G_tab) [T4-7] | S7 | aggressive variant |
| A-T5 | ×2 to uncompute per-pair intermediates; ×2 for the force-uncompute pass per step | S7 | standard compute–use–uncompute |
| A-T6 | Per-residue terms c_res ≈ 4·(100b² + 2.1×10⁵) ≈ 10⁶ (sin/cos, frames, virtual Cβ, Jᵀ·force back-propagation, θ/τ head) | S7 | subleading at L ≥ 60 |
| A-t | t_Tof ∈ {170 µs, 1 µs, 1 ns} | S9 | scenarios, not predictions |
| A-Q | 2d² physical per logical, d ≈ 31; decoding ignored | S8 | favours quantum |
| A-c | c = 1.38 | S9 | favours quantum |
| A-map | p_Q = p_C | S9 | UNPROVEN; §4.6 shows the maps differ |

---

## 3. Proofs and derivations

### 3.1 S1 (classical restarts)
- **Upper bound.** Restarts are i.i.d. Bernoulli(p) trials of the event "lands in G". The number to the first success is geometric with mean 1/p. P(no success in N) = (1−p)^N ≤ e^{−pN}, which gives N_C(δ).
- **Lower bound.** In the i.i.d.-restart access model every run is an independent Bernoulli(p) draw, whatever the algorithm does with the outcomes. So P(some success in N runs) ≤ N·p, and constant success probability needs N ≥ Ω(1/p). ∎
- This says nothing about algorithms that correlate their runs (§3.11).

### 3.2 S2 (amplitude amplification with garbage)
- **The map A.** Let U_P prepare |π₀⟩ = Σ_x √π₀(x)|x⟩ on the x₀ register. Let U_Φ be a reversible circuit with U_Φ|x⟩|0⟩ = |x⟩|Φ(x)⟩|E(Φ(x))⟩|g(x)⟩, where g(x) is whatever pebbling garbage remains. Set A = U_Φ·(U_P ⊗ I). Then A|0⟩ = Σ_x √π₀(x)|x⟩|Φ(x)⟩|E(Φ(x))⟩|g(x)⟩.
- **Good subspace.** Take the span of basis states whose energy register is ≤ t. It has squared amplitude Σ_{x∈G} π₀(x) = p.
- **Iterate.** Q = −A S₀ A⁻¹ S_χ, where S₀ reflects about |0⟩ on *all* registers, garbage included. Q acts as a rotation by 2θ in span{|ψ_good⟩, |ψ_bad⟩} [B1]. The garbage needs no separate uncomputation, because A⁻¹ inside each Q undoes it.
- **Output.** Measuring the x₀ register after success yields x ∈ G with probability π₀(x)/p, because |ψ_good⟩ is the normalised projection of A|0⟩.
- **Constant.** Take m iterations, write φ = (2m+1)θ, and use θ ≈ √p for small p. The expected cost to first success is (2m+1)/sin²φ ≈ (φ/sin²φ)/√p. The function φ/sin²φ has derivative [sin²φ − 2φ sin φ cos φ]/sin⁴φ, which is zero at tan φ = 2φ, i.e. φ* = 1.16556, where φ*/sin²φ* = 1.38010 (check C2).
- **Lower bound.** Ω(1/√p) applications are needed [C55, T4-5]. ∎

### 3.3 S3 (record process and unknown threshold)
**Setting.** Basins 1…n in energy order, masses w_j > 0 (Σ w_j = 1), W_j = Σ_{i≤j} w_i. The procedure moves a threshold basin J through a strictly decreasing sequence:
- J₀ ~ w;
- each QSearch call succeeds eventually (unless J = 1) and returns a basin distributed as w restricted to {1, …, J−1}, by the output law of §3.2 with G = {E < e_J}.

**Lemma (visit probability).** P(J ever equals j) = w_j/W_j.

*Proof.* Consider the first index in the sequence that lies in {1, …, j}. It exists, because the sequence ends at 1.
- If J₀ ∈ {1, …, j}, that first index is J₀, and conditioned on this event it is distributed as w restricted to {1, …, j}.
- Otherwise the entry happens at some step whose sampling set {1, …, J_prev − 1} contains {1, …, j}. Conditioned on landing in {1, …, j}, it is again distributed as w restricted to {1, …, j}.

So the first entry point has law w_i/W_j on {1, …, j}. Basin j is ever visited iff the first entry point is j, because afterwards the sequence stays below j. ∎

(Monte Carlo check with 2×10⁵ runs on a random 12-basin spectrum: maximum absolute error 0.0018, check C3.)

**Theorem (expected cost).** While J = j ≥ 2, the marked mass is W_{j−1}. By the QSearch theorem of [B1], QSearch uses expected ≤ c_QS·W_{j−1}^{−1/2} applications of A and A⁻¹; the explicit constant is in the analysis of [T4-6]. By linearity and the tower rule,

E[N_A until J = 1] ≤ 1 + c_QS·Σ_{j≥2} (w_j/W_j)·W_{j−1}^{−1/2}.

For each j ≥ 2, write a = W_{j−1} and b = W_j, with a < b. Then

(b−a)/(b·√a) ÷ ∫_a^b u^{−3/2} du = (b−a)/(b√a) ÷ [2(b−a)/(√a√b(√a+√b))] = (√a + √b)√b/(2b) = (1 + √(a/b))/2 ≤ 1.

So each term is at most the integral of u^{−3/2} over [W_{j−1}, W_j]. Summing gives ≤ ∫_{w₁}^{1} u^{−3/2} du = 2(w₁^{−1/2} − 1). ∎

Remarks:
- The classical analogue, "keep the best of i.i.d. restarts", reaches basin 1 in expected 1/w₁ restarts. Thresholding buys a classical algorithm nothing.
- A mass-weighted continuum of basins, where w₁ → 0 with density, saturates the bound 2c_QS/√w₁. The measured spectra sit at 78–89% of it.
- Intra-basin energy spread breaks A-B. It adds record levels inside basins and only raises E[N_A].

### 3.4 S4 (irreversibility floor)
- **Injectivity.** A reversible circuit on basis states is a permutation. If it maps (x, 0) to (Φ(x), j(x)), then x ↦ (Φ(x), j(x)) is injective. So on each fibre Φ⁻¹(y) the values j(x) are distinct, and 2^a ≥ max_y |Φ⁻¹(y)|.
- **Converging relaxation.** Suppose Φ maps every grid point of basin B_j to one point m_j. Then |Φ⁻¹(m_j)| = |B_j|.
- **Link to the prior.** π₀(B_j) = w_j and π₀(x) ≤ 2^{−H_min(π₀)}, so |B_j| ≥ w_j·2^{H_min(π₀)}. ∎
- **Fit of the natural construction.** The garbage j(x) = x uses n = Db qubits, and log₂|B_j| ≤ n. So keeping x₀ overshoots the floor by at most n − log₂|B_j| ≤ n − H_min(π₀) − log₂ w_j qubits. That is a constant factor of the register size, not an asymptotic loss (INFERENCE: H_min(π₀) grows linearly in L, as a product of per-residue terms).
- **Momentum with a buffer.** Exact reversal of v ← γv − η∇E, x ← x + v in fixed point loses ≈ log₂(1/γ) bits per coordinate per step, which must be buffered [T4-9]. Over K steps that is K·D·log₂(1/γ) bits. For convergence to resolution 2^{−b} the total must reach the floor, which is consistent with K·log₂(1/γ) ≳ b (INFERENCE).

### 3.5 S5 (pebbling recursions)
**Game.**
- Nodes 1…K form a line; node 0 is x₀ and always available.
- A move toggles the pebble on node k, and is allowed iff k = 1 or node k−1 is pebbled. Each move is one reversible step (compute x_k from x_{k−1} into a fresh register, or uncompute it), at cost C_step.
- At most s pebbles may be on the board at once.

**Recursions.**
- *F (clean).* To reach {K} with ≤ s pebbles:
  1. reach {m} with ≤ s pebbles (F(m, s));
  2. holding m, reach {m, K} with the remaining ≤ s−1 pebbles (F(K−m, s−1));
  3. remove m while holding K, by running a clean pebbling of m backwards with ≤ s−1 pebbles (F(m, s−1)).
- *G (garbage allowed).* Do steps 1–2 only: G(K−m, s−1) with garbage permitted. Alternatively, if K ≤ s, pebble straight through with K moves.
- **Reach.** Induction gives F reach 2^{s−1} and G reach 2^s − 1.
- **Optimality.** The recursions are constructive, so they are upper bounds on the optimum. They equal the breadth-first optimum for all K ≤ 8 and s ≤ 4 (check C1). General optimality is UNPROVEN here. [T4-4] states a recursion for the time-optimal solution; it was not re-read.
- **Literature.** Bennett introduced reversible simulation [T4-1] and its time/space trade-off [T4-2]; Levine and Sherman analysed the trade-off [T4-3]. Only the game's definition is used from them.

### 3.6 S6 (worst-case penalty)
A circuit has one gate sequence for all inputs. A circuit obtained by compiling a classical algorithm with data-dependent control flow must therefore be sized for that algorithm's longest execution. A loop of at most k_max iterations is unrolled k_max times; iterations after the exit are applied controlled on "not yet converged", and their gates are still present. For such compilations, Toffolis ≥ (reversible-arithmetic factor) × max_x ops(x), while the classical cost is E_x ops(x). ∎

This is a statement about compiling the given optimiser. It is not a circuit lower bound for Φ: a different algorithm computing the same Φ could be cheaper.

- **The L-BFGS numbers.**
  - Classical mean: ≈ 209 evaluations (single-restart range 109–261; census mean 174–218). That is at most 200 iterations with on average ≈ 1 Armijo trial each.
  - Coherent worst case: 200 × 12 + 1 = 2,401.
- **Sparsity.** The classical code could skip pairs with d > r_cut, where the tables are flat. The coherent code cannot, because d is in superposition.
- **Mitigation.** VTAA [T4-13] costs O(√(Σ_i t_i²)) instead of t_max·√n when evaluation times differ across items. Applied to prior-weighted restarts with variable run lengths, the extension would give ≈ √(E_π[t²]/p). That is INFERENCE; [T4-13] treats uniform items.

### 3.7 S7 (Toffoli count per reversible gradient step)
One step x_k → x_{k+1} = x_k − η·g(x_k) (or one L-BFGS trial evaluation) consists of seven stages:
1. **Kinematics** (per residue): sin/cos of θ and τ; composition of the L−1 local frames (a 3×3 product and a translation, 27 multiplications each); virtual Cβ with three normalisations. About 60b² per residue in the forward pass.
2. **Pair loop** (per pair, per channel CA/CB): Δ = X_i − X_j (3b); d² (3b²); d = √d² (2b²); grid index d/h (½b²); lookup of T_ij[g] and T_ij[g+1] (2·G_tab); interpolation (b²); slope (½b²); division by d (2b²); force vector (3b²); accumulation into 6 force registers and the energy (7b). That totals **12b² + 2G_tab + 12b ≈ 7.0×10³** at b = 20.
3. **Uncompute** the per-pair intermediates: ×2.
4. **Sterics** on Cα pairs: relu² and its derivative, ≈ 3b², ×4.
5. **Back-propagation** from forces to (θ, τ) gradients: suffix sums of forces and of r×F along the chain, then one dot or cross product per coordinate. About 40b² per residue. Plus the θ/τ head: 58 erf-type evaluations and 225 products, or a QROAM on the 0.5° × 1° grid, ≈ 2×10⁵.
6. **Update** x_{k+1} = x_k − ηg into a fresh register: D multiply-adds by a constant, negligible.
7. **Uncompute** g, the forces and the kinematics, i.e. a second pair pass: ×2.

This gives c_pair = 2 channels × 2 (uncompute intermediates) × 2 (uncompute forces) × 7.0×10³ + 12b² ≈ 6.1×10⁴ per pair per step, and c_res ≈ 10⁶ per residue per step. **(INFERENCE; constants A-T1–A-T6.)**

Remarks:
- **Why not a quantum gradient algorithm.** Jordan-type and later quantum gradient algorithms [T4-8] save queries relative to finite differences. Here the classical-exact gradient comes from reverse-mode arithmetic at a small constant multiple of one energy evaluation (the cheap-gradient principle, a standard result not re-verified here). The phase-estimation gradient would also be stochastic per step, which would branch the trajectories. It buys nothing (INFERENCE).
- **Why not incremental updates.** Every torsion step moves the whole chain downstream, so all O(L²) distances change each step. Incremental ΔE (O(L) pairs) is unavailable for gradient steps, unlike single-residue Metropolis moves with a classical move index (compare T2 open gap 7).

### 3.8 S8 (qubits)
Arithmetic in §1 S8 and check notes:
- workspace ≈ (3 Cα + 3 Cβ + 9 frames + 6 forces + 6 suffix sums)·L·b + D·b + O(b²) ≈ 29·L·b;
- one pebble = one optimiser state;
- the heavy-ball buffer = K·D·log₂(1/γ) bits with K = 10⁴ and γ = 0.9, plus x, v and x₀.

### 3.9 S9 (break-even)
1. Take the classical side to run the *same* map, which it can (S11a). Then W_C = t_C/(S·p) and W_Q = c·t_Q/√p, and W_Q < W_C ⟺ √p < t_C/(c·S·t_Q) ⟺ p < p*.
2. At p = p*, W_Q = c·t_Q/√p* = c²·S·t_Q²/t_C = T*. W_Q is decreasing in p, so for p < p*, W_Q > T*.
3. Usefulness also needs W_Q ≤ W_max ⟺ p ≥ (c·t_Q/W_max)². That interval meets (0, p*) iff c·t_Q/W_max < t_C/(c·S·t_Q) ⟺ T* < W_max. ∎
4. **L-independence of R.** t_Q = K_eff·ρ·C_step(L)·t_Tof and t_C = K_C·t_g(L). With C_step ≈ c_pair·L²/2 and t_g ∝ L², R → K_eff·ρ·c_pair·t_Tof/(2·K_C·t_g(L)/L²), a constant. Numerically R is 4.4, 3.9 and 3.6 ×10⁸ at L = 60, 100 and 150 (M-LB2, 170 µs). The small drift comes from the O(L) terms. ∎

### 3.10 S10 (parallelism)
- **Classical.** W_C(S) = t_C/(S·p) exactly: independent restarts, no communication.
- **Quantum.** By [T4-5], S_Q quantum machines cannot beat dividing the search space. Splitting the prior into S_Q parts of equal mass gives each part conditional hit probability ≈ S_Q·p on average, so W_Q(S_Q) ≈ c·t_Q/√(S_Q·p).
- **Equal counts.** Setting S_Q = S gives p* = (t_C/(c·t_Q))²/S. ∎

### 3.11 S11 (better proposals)
- **The ratio.** From the two time-to-target expressions, W_Q(B)/W_C(B) = [c·t_Q(B)/√p(B)]·[S·p(B)/t_C(B)] = c·S·R(B)·√p(B).
- **𝒬 ⊆ 𝒞.** A coherent A is a reversible classical circuit applied to a superposition over random-bit strings, with U_P implementable as a classical sampler on random bits. Measuring immediately gives exactly the classical run on random bits. ∎
- **Population methods.** A coherent N-particle SMC needs N× the per-particle coherent cost, plus reversible resampling (prefix sums over N weights and a coherent search per offspring, or a sorting network; a polylog overhead per particle per generation). Its success probability is that of the whole population run.
- **Adaptive methods.** Basin hopping and PT make each run depend on the previous one. They are Markov chains, and their quantum acceleration is the walk or QSA question [A8, A31, A44], treated in T2.
- **Structured search trees.** Quantum backtracking and branch-and-bound speed up tree search only relative to *the same classical tree* [C57, C60, C61]. Fragment assembly is not a tree search with a bounding function. So no near-quadratic gain beyond S2 is known for it (INFERENCE).

### 3.12 S12 (criterion)
Gates H and I are §3.9 with p_Q and p_C separated. Gate I compares c·t_Q/√p_Q with the best classical TTT_C, which may use a *different* procedure than the coherent map.

The necessary condition T* ≤ W_max uses t_C^map, the classical cost of running the coherent map itself. The classical side can always do that (§3.11). ∎

---

## 4. Numbers

### 4.1 Classical timings (PILOT)
- **Orchestrator-reported.** 1.8 ms per energy+gradient at L = 150, one core (A-C1).
- **This session** (machine at 83–84% CPU from other G1 jobs, one thread, `T4` scratch timing):

| L | pairs | per structure, B = 1 | per structure, B = 64 |
|---|---|---|---|
| 45 | 903 | 5.4 ms | 0.35 ms |
| 60 | 1,653 | 6.9 ms | 0.59 ms |
| 100 | 4,753 | 6.2 ms | 1.63 ms |
| 150 | 10,878 | 10.2 ms | 5.93 ms |

- **Evaluations per restart.** L-BFGS gradient evaluations per restart: mean 174 / 193 / 203 / 213 / 217 at L = 30 / 45 / 60 / 80 / 100 (census; the largest per-crop mean at each L is 202–221). Single restarts at L = 45 (check C7): mean 209, median 222, 10th–90th percentile 149–237, maximum 261.

### 4.2 Mode census, p_hit(L) (PILOT)
Source: `research/results/RAW/g1_modes/*.json`, written by `scripts/g1_mode_census.py` (another workstream). R = 256 restarts per crop, T = 1, seed 0, clustering at 2 Å. Snapshot taken 2026-09-27 00:31, with 16 crops at every L; the census queue continues to L = 120–150.

| L | crops | median p_hit | lower quartile | min | censored (p ≤ 1/256) | median #modes / 256 | max call saving 1/(1.38√p) at median |
|---|---|---|---|---|---|---|---|
| 30 | 16 | 0.117 | 0.072 | 0.0039 | 6% | 82 | 2.1× |
| 45 | 16 | 0.109 | 0.026 | 0.0039 | 6% | 109 | 2.2× |
| 60 | 16 | 0.049 | 0.013 | 0.0039 | 25% | 150 | 3.3× |
| 80 | 16 | 0.059 | 0.019 | 0.0039 | 19% | 181 | 3.0× |
| 100 | 16 | 0.016 | 0.0068 | 0.0039 | 25% | 244 | 5.7× |

- **Slope.** Per-protein least-squares slope of ln p_hit over L = 30–100 (16 proteins): median **−0.030 per residue**, IQR [−0.040, −0.008]. The pooled slope is −0.024. An earlier snapshot without L = 100 gave −0.019, so the estimate is still moving.
  - Censoring at 1/R biases these toward zero, and the true tail is steeper. The number of distinct modes rises toward R, so R = 256 under-resolves L ≥ 60.
- **Largest achievable call saving at the censoring floor** p = 1/256: 1/(1.38·(1/16)) = **11.6×**.

### 4.3 Dürr–Høyer on the measured basin spectra (DERIVED on PILOT)

| L | median E[N_A]/c_QS (quantum) | median 1/w₁ (classical) | E[N_A]·√w₁/c_QS, median (max) |
|---|---|---|---|
| 30 | 4.6 | 8.5 | 1.56 (1.77) |
| 45 | 4.7 | 9.2 | 1.57 (1.83) |
| 60 | 7.8 | 20.8 | 1.65 (1.80) |
| 80 | 7.0 | 17.1 | 1.66 (1.82) |
| 100 | 14.4 | 68.3 | 1.78 (1.82) |

Masses beyond the 50 listed modes are bounded by the integral (script `dh_cost`). **Reading:** at the measured spectra the query saving is at most 2–5× in calls (the classical/quantum ratio at c_QS = 1), before any per-call overhead.

### 4.4 Gate cost of one coherent relaxation (INFERENCE)
Toffolis per application of A = K_eff·ρ·C_step(L), with prior preparation and marking negligible (§2.5):

| Map | K_eff × ρ (gradient-step equivalents) | L = 60 | L = 100 | L = 150 |
|---|---|---|---|---|
| M-LB2 (s = 24) | 400 × 2.44 = 976 | 1.6×10¹¹ | 3.8×10¹¹ | 8.0×10¹¹ |
| M-LB12 (s = 24) | 2,400 × 3.80 = 9,120 | 1.5×10¹² | 3.6×10¹² | 7.4×10¹² |
| M-HB (no pebbling, buffer) | ≈ 10⁴ | 1.6×10¹² | 3.9×10¹² | 8.2×10¹² |

Wall-clock per application of A, t_Q (M-LB2):
- 170 µs: 309 d / 750 d / 4.3 yr at L = 60 / 100 / 150;
- 1 µs: 1.8 / 4.4 / 9.2 d;
- 1 ns: 157 / 381 / 795 s.

For comparison t_C = 0.060 / 0.167 / 0.376 s.

### 4.5 Break-even (DERIVED arithmetic; c = 1.38, W_max = 1 yr; check C6)

| Map | L | t_Tof | R = t_Q/t_C | p*, S = 1 | T*, S = 1 | p*, S = 10³ | T*, S = 10³ |
|---|---|---|---|---|---|---|---|
| M-LB2 | 60 | 170 µs | 4.4×10⁸ | 2.7×10⁻¹⁸ | 7.2×10⁸ yr | 2.7×10⁻²⁴ | 7.2×10¹¹ yr |
| M-LB2 | 100 | 170 µs | 3.9×10⁸ | 3.5×10⁻¹⁸ | 1.5×10⁹ yr | 3.5×10⁻²⁴ | 1.5×10¹² yr |
| M-LB2 | 150 | 170 µs | 3.6×10⁸ | 4.1×10⁻¹⁸ | 2.9×10⁹ yr | 4.1×10⁻²⁴ | 2.9×10¹² yr |
| M-LB2 | 60 | 1 µs | 2.6×10⁶ | 7.7×10⁻¹⁴ | 2.5×10⁴ yr | 7.7×10⁻²⁰ | 2.5×10⁷ yr |
| M-LB2 | 100 | 1 µs | 2.3×10⁶ | 1.0×10⁻¹³ | 5.2×10⁴ yr | 1.0×10⁻¹⁹ | 5.2×10⁷ yr |
| M-LB2 | 150 | 1 µs | 2.1×10⁶ | 1.2×10⁻¹³ | 1.0×10⁵ yr | 1.2×10⁻¹⁹ | 1.0×10⁸ yr |
| M-LB2 | 60 | 1 ns | 2.6×10³ | 7.7×10⁻⁸ | 9 d | 7.7×10⁻¹⁴ | 25 yr |
| M-LB2 | 100 | 1 ns | 2.3×10³ | 1.0×10⁻⁷ | 19 d | 1.0×10⁻¹³ | 52 yr |
| M-LB2 | 150 | 1 ns | 2.1×10³ | 1.2×10⁻⁷ | 37 d | 1.2×10⁻¹³ | 100 yr |
| M-LB12 | 100 | 170 µs | 3.6×10⁹ | 4.0×10⁻²⁰ | 1.3×10¹¹ yr | 4.0×10⁻²⁶ | 1.3×10¹⁴ yr |
| M-LB12 | 100 | 1 µs | 2.1×10⁷ | 1.2×10⁻¹⁵ | 4.6×10⁶ yr | 1.2×10⁻²¹ | 4.6×10⁹ yr |
| M-LB12 | 100 | 1 ns | 2.1×10⁴ | 1.2×10⁻⁹ | 4.6 yr | 1.2×10⁻¹⁵ | 4.6×10³ yr |
| M-HB | 100 | 1 ns | 2.3×10⁴ | 9.6×10⁻¹⁰ | 5.5 yr | 9.6×10⁻¹⁶ | 5.5×10³ yr |

The full grid (3 maps × 3 lengths × 3 Toffoli times × 2 values of S) is printed by check C6.

**Sensitivity (DERIVED).** p* ∝ (t_C/t_Q)² and T* ∝ t_Q²/t_C.
- The aggressive gate constants (§1 S7) divide t_Q by ≈ 2 at L = 100.
- The unknown-threshold record process multiplies c by ≈ 1.2·c_QS (c_QS ≥ 1; not extracted, G7).
- An optimised classical kernel divides t_C by 10–100.

None of these changes the verdict at 170 µs or 1 µs.

### 4.5a Cross-check with the parallel T3 script (DERIVED arithmetic on T3's cost functions; provisional)
During this work the T3 lane published a script, `research/theory/T3_resource_model.py` (read 2026-09-27; its note `RESOURCE_MODELS.md` did not yet exist). It costs one full coherent energy evaluation, C_E, with build/unbuild and temporaries uncomputed, for three designs:
- **D1:** literal 1,001-point tables with a square root;
- **D2:** per-pair cubic splines in d², QROAM lookups;
- **D2 generous:** D2 with T3's most optimistic parameters.

Its quantised-HMC variant prices a gradient at 3·C_E. Taking C_step = 3·C_E, with the same M-LB2 map (976 gradient-step equivalents), c = 1.38, t_C as A-C1 and S = 1:

| Gate-cost source | C_step at L = 30 / 60 / 100 / 150 | T* at 170 µs | T* at 1 µs | p* at 1 µs |
|---|---|---|---|---|
| This note, nominal (§3.7) | 5.3×10⁷ / 1.6×10⁸ / 3.9×10⁸ / 8.2×10⁸ | 3.1×10⁸ / 7.2×10⁸ / 1.5×10⁹ / 2.9×10⁹ yr | 1.1×10⁴ / 2.5×10⁴ / 5.2×10⁴ / 1.0×10⁵ yr | ≈ 4×10⁻¹⁴–1×10⁻¹³ |
| T3 D1 central, 3·C_E | 6.3×10⁷ / 2.7×10⁸ / 7.8×10⁸ / 1.8×10⁹ | 4.4×10⁸ / 2.0×10⁹ / 6.0×10⁹ / 1.4×10¹⁰ yr | 1.5×10⁴ / 7.1×10⁴ / 2.1×10⁵ / 4.8×10⁵ yr | ≈ 3×10⁻¹⁴ |
| T3 D2 central, 3·C_E | 1.5×10⁷ / 6.2×10⁷ / 1.7×10⁸ / 3.9×10⁸ | 2.6×10⁷ / 1.1×10⁸ / 2.9×10⁸ / 6.6×10⁸ yr | 9.1×10² / 3.6×10³ / 1.0×10⁴ / 2.3×10⁴ yr | ≈ 5×10⁻¹³ |
| T3 D2 generous, 3·C_E | 6.8×10⁶ / 2.6×10⁷ / 7.1×10⁷ / 1.6×10⁸ | 5.1×10⁶ / 1.9×10⁷ / 5.0×10⁷ / 1.1×10⁸ yr | 1.8×10² / 6.5×10² / 1.7×10³ / 3.8×10³ yr | ≈ 3×10⁻¹² |

**Reading (INFERENCE).**
- This note's nominal C_step lies between T3's D2 and D1 designs, within factors of about 2.5 and 2 respectively.
- T3's D2 design replaces the 1,001-point tables and the square root by cubics in d². That change, not arithmetic precision, is the main lever.
- Even with T3's most generous costs, gate H fails at every L ≥ 30: T* ≥ 5×10⁶ yr at 170 µs and ≥ 180 yr at 1 µs (S = 1; ×10³ at S = 10³).
- The hypothetical-hardware thresholds relax to t_Tof ≲ 16–39 ns (S = 1) and ≲ 0.5–1.2 ns (S = 10³) at L = 60–150, and the 1 ns p* rises to about 3×10⁻⁶.
- If T3's final note changes these functions, rescale with T* ∝ C_step² and p* ∝ C_step⁻².

### 4.6 Coherent-friendly optimisers vs L-BFGS on 5O37A_45 (PILOT; check C7)
Setup: 16 seed-0 prior draws, the same x₀ as the census, compared with L-BFGS from the same x₀. "Same basin" means within 2 Å Cα-RMSD of that start's L-BFGS endpoint.

| Map | K = 500 | K = 2,000 | K = 10,000 | Energy increases |
|---|---|---|---|---|
| GD, η = 3×10⁻⁴ / 10⁻³ / 3×10⁻³ (64 starts) | diverging: 0 same basin, E − E_LBFGS ≈ +2.5×10³ to +7×10³ | same | same | ~45–50% of steps |
| GD, η = 10⁻⁵ | 0.00 same; ΔE median +392 | 0.25; +184 | **0.44; +29** | 0.2% |
| GD, η = 2×10⁻⁵ | 0.06; +282 | 0.25; +106 | **0.44; −2.3** (50% below L-BFGS) | 21% (edge of stability) |
| Clipped GD, η = 10⁻³, clip 0.02 rad | 0.00; +715 | 0.00; +713 | 0.00; +713 (limit cycle) | 50% |

**Hessian spectrum** of the energy in internal coordinates (16 L-BFGS endpoints):
- at the endpoints: λ_max median 281, maximum 8.7×10⁴; smallest eigenvalue above 10⁻³ median 0.50; a median of 33 of 85 eigenvalues ≤ 10⁻³ (flat directions);
- at 4 prior draws: |λ|_max = 6.1×10³–9.7×10⁴, from steric clashes.
- So a globally stable fixed step is η ≲ 2×10⁻⁵, and the effective condition number is ~10⁵.

**Reading (INFERENCE).**
- Fixed-step descent, the textbook "reversible-friendly" map, needs ≫ 10⁴ steps: at least ≈ 50× the gradient evaluations of L-BFGS.
- It lands in *different* basins from L-BFGS: 44% agreement after 10⁴ steps at either stable step size. At η = 2×10⁻⁵ it ends lower than L-BFGS in 50% of runs; at η = 10⁻⁵, 19% (still descending).
- **p is a property of the pair (landscape, map), not of the landscape.** A-map (p_Q = p_C) is an assumption, and a coherent design must be validated by classically measuring p_Q for the exact b-bit map.
- An L-BFGS-type coherent map (M-LB2/M-LB12) is therefore the realistic choice, with its line-search worst case (S6).

### 4.7 Required hardware and the extrapolated window (DERIVED + INFERENCE)
**Hardware needed for the gate.** Gate H (T* ≤ 1 yr) for M-LB2 needs:

| L | S = 1: t_Q ≤ | t_Tof ≤ | Toffoli/s | S = 10³: t_Q ≤ | t_Tof ≤ | Toffoli/s |
|---|---|---|---|---|---|---|
| 60 | 999 s | 6.4 ns | 1.6×10⁸ | 32 s | 0.20 ns | 5.0×10⁹ |
| 100 | 1,660 s | 4.4 ns | 2.3×10⁸ | 53 s | 0.14 ns | 7.2×10⁹ |
| 150 | 2,500 s | 3.1 ns | 3.2×10⁸ | 79 s | 0.10 ns | 1.0×10¹⁰ |

That is 2.7×10⁴–1.7×10⁶ times the T3-baseline Toffoli rate of 5.9×10³ /s. With T3's most generous gate costs (§4.5a) the requirement relaxes about 5–6-fold, to ≲ 16–39 ns (S = 1) or ≲ 0.5–1.2 ns (S = 10³), i.e. 4×10³–3×10⁵ times the baseline rate.

**Window.** Under the 1 ns hypothetical (M-LB2, S = 1, W_max = 1 yr), p_Q ∈ [4.7×10⁻¹¹, 7.7×10⁻⁸] at L = 60, [2.8×10⁻¹⁰, 1.0×10⁻⁷] at L = 100 and [1.2×10⁻⁹, 1.2×10⁻⁷] at L = 150. At S = 10³ the window is empty (T* > 25 yr).

**Extrapolation (INFERENCE, PILOT slope).** Take ln p_hit(L) ≈ ln 0.117 − α·(L − 30), with α = 0.030 (median) or α = 0.040 (steep quartile). This fits the L = 100 median (predicted 0.014, observed 0.016). Then:
- p ≈ 10⁻⁷ at L ≈ 500 (median) or ≈ 380 (steep quartile);
- p ≈ 3×10⁻⁶ (the 1 ns p* with T3-generous costs) at L ≈ 390 or ≈ 300;
- the T3-baseline p* ≈ 3×10⁻¹⁸ at L ≈ 1,300 or ≈ 1,000, where T* ≈ 10¹¹ yr (T* ∝ L²).

Within L ≤ 150 the extrapolated median crop has p ≳ 3×10⁻³, so the call saving is ≤ 13× on any hardware.

---

## 5. Literature

### 5.1 Bibliography keys used (verified in the literature phase; `BIBLIOGRAPHY.md`)

| Key | Paper | Used for | Label |
|---|---|---|---|
| B1 | Brassard, Høyer, Mosca, Tapp 2002 | AA iteration, output law, QSearch with unknown a | THEORETICAL |
| B2 | Brassard, Høyer, Tapp 1998 | quantum counting (estimating p at O(1/√p)) | THEORETICAL |
| C54 | Grover 1996 | search | THEORETICAL |
| C55 | Bennett, Bernstein, Brassard, Vazirani 1997 | Ω(√N) lower bound | THEORETICAL |
| C56 | Dürr, Høyer 1996 | minimum finding, O(c√N) with probability ≥ 1 − 2^{−c} (abstract re-read this session) | THEORETICAL |
| C57, C60, C61 | Montanaro 2018/2020; Chakrabarti et al. 2022 | backtracking / B&B speedups relative to the same tree | THEORETICAL |
| C63 | Campbell, Khurana, Montanaro 2019 | decoding cost erases Grover-type advantage | resource estimate |
| A56 = C64 | Sanders et al. 2020 | 170 µs/Toffoli, factory footprint, "a day and a million physical qubits … four CPU-minutes" | NO ADVANTAGE (resource) |
| B46 = C65 | Babbush et al. 2021 | T* = t_Q²·S/t_C (d = 2), eq. (5) | NO ADVANTAGE (quadratic) |
| A55 | Lemieux et al. 2020 | ~1 ns logical gates to match a special-purpose MCMC machine | resource |
| A59 | Häner, Roetteler, Svore 2018 | reversible arithmetic building blocks (constants not re-verified) | — |
| A60 | Babbush et al. 2018 | unary-iteration lookups (**existence only; the linear-cost claim is unverified**) | — |
| F59 | Berry et al. 2019 | QROAM-type lookups (existence verified; cost statement not re-read) | — |
| B36, B37 | Grover–Rudolph 2002; Herbert 2021 | loading correlated laws erases speedups; why the product prior matters | THEORETICAL |
| A8, A31, A44 | QSA / adaptive QSA / quantum RELD | the Markov-chain alternative (T2) | THEORETICAL |
| B65 = E74 | Del Moral, Doucet, Jasra 2006 | SMC | classical |
| D41 = E53, C84 = E54, E55 | Grassberger PERM 1997; Hsu et al. 2003; Zhang, Kou, Liu FRESS 2007 | population / growth / regrowth | classical |
| C77 = E20, E33 | Hukushima–Nemoto 1996; Machta 2009 | PT | classical |
| A78 = E76, E79, E80, A79 = E83 | Boltzmann generators; sequential BG; AlphaFlow; BioEmu | learned proposals | classical ML |

### 5.2 References verified in this session (not yet in BIBLIOGRAPHY; add on integration)

| Key | Reference | Verification (2026-09-27) |
|---|---|---|
| T4-1 | C. H. Bennett, "Logical reversibility of computation," IBM J. Res. Dev. 17(6):525–532 (1973). DOI 10.1147/rd.176.0525 | Crossref metadata |
| T4-2 | C. H. Bennett, "Time/space trade-offs for reversible computation," SIAM J. Comput. 18(4):766–776 (1989). DOI 10.1137/0218053 | Crossref metadata. Only the pebble-game setting is used; the trade-off here is computed independently (C1) |
| T4-3 | R. Y. Levine, A. T. Sherman, "A note on Bennett's time-space tradeoff for reversible computation," SIAM J. Comput. 19(4):673–677 (1990). DOI 10.1137/0219046 | Crossref metadata |
| T4-4 | E. Knill, "An analysis of Bennett's pebble game," arXiv math/9508218 (1995) | arXiv abstract ("a recursion for the time optimal solution … given a space bound") |
| T4-5 | C. Zalka, "Grover's quantum searching algorithm is optimal," PRA 60:2746–2751 (1999). arXiv quant-ph/9711070 (= T5's X15) | arXiv abstract: optimal for any success probability; "cannot be parallelized better than by assigning different parts of the search space to independent quantum computers" |
| T4-6 | M. Boyer, G. Brassard, P. Høyer, A. Tapp, "Tight bounds on quantum searching," Fortschr. Phys. 46:493–506 (1998). arXiv quant-ph/9605034 (= T5's X16) | arXiv abstract + journal ref. Explicit unknown-t constant not extracted (§7 G7) |
| T4-7 | G. H. Low, V. Kliuchnikov, L. Schaeffer, "Trading T gates for dirty qubits in state preparation and unitary synthesis," Quantum 8, 1375 (2024). arXiv 1812.00954 | arXiv abstract: T-count O(N/λ + λ·log(N/ε)·log(log N/ε)) |
| T4-8 | A. Gilyén, S. Arunachalam, N. Wiebe, "Optimizing quantum optimization algorithms via faster quantum gradient computation," SODA 2019, 1425–1444. arXiv 1711.00465 | arXiv abstract (quadratic improvement over Jordan's algorithm; smoothness assumptions) |
| T4-9 | D. Maclaurin, D. Duvenaud, R. P. Adams, "Gradient-based hyperparameter optimization through reversible learning," arXiv 1502.03492 (2015) | arXiv abstract ("exactly reversing the dynamics of stochastic gradient descent with momentum"). The information-buffer detail is from the body and was **not re-read**; venue not verified |
| T4-10 | Z. Li, H. A. Scheraga, "Monte Carlo-minimization approach to the multiple-minima problem in protein folding," PNAS 84:6611–6615 (1987). DOI 10.1073/pnas.84.19.6611 | Crossref metadata |
| T4-11 | D. J. Wales, J. P. K. Doye, "Global optimization by basin-hopping and the lowest energy structures of Lennard-Jones clusters containing up to 110 atoms," J. Phys. Chem. A 101:5111–5116 (1997). DOI 10.1021/jp970984n | Crossref metadata |
| T4-12 | K. T. Simons, C. Kooperberg, E. Huang, D. Baker, "Assembly of protein tertiary structures from fragments with similar local sequences using simulated annealing and Bayesian scoring functions," J. Mol. Biol. 268:209–225 (1997). DOI 10.1006/jmbi.1997.0959 | Crossref metadata |
| T4-13 | A. Ambainis, "Quantum search with variable times," arXiv quant-ph/0609168 (2006) | arXiv abstract: O(√(t₁² + … + t_n²)), optimal; unknown t_i with polylog overhead |

### 5.3 Not verified, not used as evidence
- The explicit constant 22.5√N often quoted for [C56]. The abstract gives only O(c√N) with probability ≥ 1 − 2^{−c}, so no constant from [C56] is used.
- The cheap-gradient principle of reverse-mode differentiation (Baur–Strassen / Griewank). It is used only as a standard remark (INFERENCE).
- The QROM linear-cost statement of [A60] and the QROAM cost of [F59]. They enter only through A-T4, which is bracketed by the verified scaling of [T4-7].
- Jordan's original gradient algorithm (2005). It is known here only through [T4-8]'s abstract.

---

## 6. Scope and what is NOT claimed

- **Not claimed:** that finding the argmin of the learned energy is useful for accuracy.
  - S33 found restart saturation at 44–60 aa, with ≤ 0.14 Å headroom above the information floor (R10, `sprint29-33/README.md`).
  - The surviving program lead is posterior *sampling* (T2), not mode finding.
  - This note answers the computational question only: cost-to-argmin under the stated model.
- **Not claimed:** exact Toffoli counts. §3.7 is a labelled order-of-magnitude model. T* ∝ (K_eff·ρ·C_step)², so:
  - the 170 µs conclusion holds unless the coherent relaxation is overestimated by more than ~2×10⁴;
  - the 1 µs conclusion holds unless it is overestimated by more than ~10² (S = 1) or ~3×10³ (S = 10³).
- **Not claimed:** any lower bound against *structured* quantum algorithms, such as walks, QSA, or quantum algorithms using the energy's white-box form. S2 and S3 are black-box statements about amplifying a given restart map. Super-quadratic routes are T5's subject.
- **Not claimed:** that p_hit(L) scaling is measured. The census is PILOT, R = 256 censors the tail, and the best mode may not be the global minimum. The slope (−0.030 per residue; −0.019 before the L = 100 crops arrived) is indicative.
- **Not claimed:** that A-map (p_Q = p_C) holds. §4.6 shows it can fail in both directions.
- **Not claimed:** hardware predictions. 170 µs / 1 µs / 1 ns are scenarios. No quantum simulation or hardware run was performed, and the simulator ≠ hardware and query ≠ runtime rules are respected.
- **Not claimed:** a classical lower bound for adaptive classical search. The Ω(1/p) of S1 holds only in the i.i.d.-restart model.
- **Leakage:** no native structure was read by any check (DEP only). The census clustering is endpoint-to-endpoint.

---

## 7. Open gaps

| # | Gap | Why it matters | Next step |
|---|---|---|---|
| G1 | T3's Toffoli count G(L) for the actual A80 gradient, including the pair-specific soft-table lookups and verification of the lookup cost ([A60], [F59], [T4-7]) | Replaces A-T1–A-T6; rescales p* ∝ G⁻² and T* ∝ G² | T3 |
| G2 | p_Q for the exact b-bit coherent maps (M-LB2 with a 2-trial line search, M-HB with a buffer) vs p_C of float64 L-BFGS | A-map is UNPROVEN; §4.6 shows the map changes p | Classical emulation of the b-bit maps on the census crops (cheap) |
| G3 | The censored tail of p_hit(L) at L = 60–150 (19–25% of crops at the 1/256 floor) and whether the census best mode is the global minimum | Only the tail could ever enter an instance window (S12) | More restarts on the censored crops; compare with PT/NRPT minima (T5 §4.3 found PT lower at L = 45) |
| G4 | Best classical portfolio TTT_C(L) (basin hopping, PT, SMC, learned proposals) against naive i.i.d. restarts | Gate I uses the best classical method, not the naive one | Part of G1's classical-twin portfolio |
| G5 | VTAA [T4-13] extended to prior-weighted items with variable relaxation lengths; its constants | Could recover most of the ≈ 11.5× worst-case penalty (S6); already assumed in M-LB2 | Theory, short |
| G6 | Surface-code decoding and classical co-processing cost [C63] | Ignored (favours quantum) | T3 |
| G7 | Explicit c_QS for the unknown-p search [T4-6, B1] | Sets the unknown-threshold constant (≈ 1.6·c_QS) | Read the full text of [T4-6] |
| G8 | Transmission: does the dominant mode matter for accuracy beyond 60 aa (H-004)? | If not, the task itself is irrelevant, whatever its cost | G1 transmission arm |
| G9 | Integration: add [T4-1]–[T4-13] to `BIBLIOGRAPHY.md`; record this note in KILLBOOK / OPPORTUNITY_MATRIX M9 as "KILLED, now quantified" | Housekeeping | Integrator |
| G10 | The L0–L6 scale is taken from T2's working table; the program should define it centrally | Consistency | Integrator |

**What would reopen AA-2 (INFERENCE).** Three things together:
1. logical Toffoli throughput ≳ 10⁷–10¹⁰ per second, which is ≥ 4×10³ times the T3 baseline even with T3's most generous gate costs;
2. a protein class where p_Q(L) ≲ 10⁻⁷ at L ≤ 150 for the coherent map;
3. evidence that no adaptive or learned classical method reaches the basin at TTT_C below c·t_Q/√p_Q.

None of the three is in view. If (2) held while (3) failed, the classical method is the answer.

---

## Appendix: check output (`python research/theory/PROOFS/T4_amplified_checks.py [--energy]`, 2026-09-27, one core)

Default checks, census snapshot 00:31 ({30: 16, 45: 16, 60: 16, 80: 16, 100: 16}); excerpt:
```
C1 DP vs brute force (n<=8, s<=4): OK
C1 max K reachable with s pebbles: clean F: [1, 2, 4, 8, 16, 32]  garbage-allowed G: [1, 3, 7, 15, 31, 63]
C1 K=  400: time overhead G(K,s)/K  s=9:8.39  s=12:4.38  s=16:3.28  s=20:2.90  s=24:2.44  s=32:1.92  s=40:1.90
C1 K= 2400: time overhead G(K,s)/K  s=12:14.36  s=16:6.64  s=20:5.44  s=24:3.80  s=32:3.55  s=40:3.30
C2 known p, repeated fixed-m runs: expected A-applications * sqrt(p) -> min phi/sin^2 phi = 1.3801 at phi = 1.1656 (tan phi = 2 phi); single long run: pi/2 = 1.5708
C3 record-process lemma P(visit j)=w_j/W_j, Monte Carlo n=200000: max abs error 0.0018
C3 L= 30: median E[N_A]/c_QS   4.6  median classical 1/w1   8.5  E[N_A]*sqrt(w1)/c_QS median 1.56 max 1.77 (bound 2)
C3 L= 60: median E[N_A]/c_QS   7.8  median classical 1/w1  20.8  E[N_A]*sqrt(w1)/c_QS median 1.65 max 1.80 (bound 2)
C3 L=100: median E[N_A]/c_QS  14.4  median classical 1/w1  68.3  E[N_A]*sqrt(w1)/c_QS median 1.78 max 1.82 (bound 2)
C4 L= 60 crops=16 R=256: p_hit median 0.049 q25 0.0127 min 0.0039 censored(<=1/R) 0.25 | modes median 150 | grad evals/restart mean 203 max 211
C4 L=100 crops=16 R=256: p_hit median 0.016 q25 0.0068 min 0.0039 censored(<=1/R) 0.25 | modes median 244 | grad evals/restart mean 217 max 220
C4 slope d ln p_hit / dL: pooled (all L) -0.0244; per-protein over L=[30, 45, 60, 80, 100] (16 proteins) median -0.0295 IQR [-0.0395, -0.0078]
C5 L=100: C_step nominal 3.91e+08 | b=16 3.09e+08 | b=24 4.90e+08 | aggressive 1.94e+08 Toffolis; pair share 0.74
C6 M-LB2 (K_eff=400, s=24) L=100 t_Tof=170us: t_C=0.167s t_Q=6.48e+07s R=3.9e+08 | S=1: p*=3.5e-18 T*=1.5e+09yr | S=1000: p*=3.5e-24 T*=1.5e+12yr
C6 M-LB2 (K_eff=400, s=24) L=100 t_Tof=1ns  : t_C=0.167s t_Q=3.81e+02s R=2.3e+03 | S=1: p*=1.0e-07 T*=5.2e-02yr | S=1000: p*=1.0e-13 T*=5.2e+01yr
C6 T*<=1yr at L=100 S=1: t_Q <= 1.66e+03s -> t_Tof <= 4.37e-09s (2.29e+08 Toffoli/s) for M-LB2
C6 window (1 ns, S=1, W=1yr, M-LB2) L=100: p in [2.8e-10, 1.0e-07]; max speedup at p=0.05: 3.2x in calls
```
Energy checks (`--energy`, run 00:12–00:30 on a machine at ~84% load):
```
C7 L-BFGS evals/restart (B=1): mean 209 median 222 max 261
C7 Hessian at L-BFGS endpoints: lambda_max median 281, max 8.65e+04; smallest eigenvalue > 1e-3 median 0.495
C7 GD eta=2e-5, K=1e4: same basin as L-BFGS 0.44; median E - E_LBFGS -2.3
C7 clipped GD eta=1e-3 clip=0.02, K=1e4: same basin as L-BFGS 0.00; median E - E_LBFGS 713.3
```
The GD rows with η = 10⁻⁵ and η ≥ 3×10⁻⁴, the K = 500/2,000 checkpoints and the prior-draw curvature in §4.6 come from equivalent scratch runs in this session. Those runs used the same code, crop and seeds; they are not saved in the repository. Later census snapshots will change the C3/C4 rows.
