# T4. Cost of amplitude-amplified mode finding on the learned A80 energy

_Workflow task T4. **Status: v2**, revised on 2026-09-27 after two adversarial reviews. The Review log at the end lists every objection and what was done about it. v1 (same date) is archived unchanged at `research/theory/PROOFS/superseded/T4_amplified_mode_finding_v1.md`. This file has a single writer._

_**Companion script.** `research/theory/PROOFS/T4_amplified_checks.py`:_
- _default run (under a minute, one core): checks C1–C6, which are arithmetic, the census read (C4) and the summary of the C8 runs;_
- _`--energy`: check C7, the small energy checks of §4.6 (about 20 minutes);_
- _`--converge CROP …`: check C8, a converged re-relaxation of the census draws. C8 is pre-registered in `research/experiments/PREREGISTERED/PREREG_T4_C8_convergence.md`; its raw per-restart output is in `research/results/RAW/t4_converge/`._

_Citation keys such as [B1] resolve in `research/literature/BIBLIOGRAPHY.md`. Keys [T4-n] are papers verified in this session that are not yet in the bibliography (§5.2). Every number from the G1 runs or from C7/C8 is **PILOT**: indicative only._

**Tags.** Every claim carries one of these tags.

| Tag | Meaning |
|---|---|
| **DERIVED** | Proved or computed here from the stated assumptions. The proof is in §3; numerical checks are in the script |
| **THEORETICAL [key, locator]** | A result from the verified literature, used as its authors state it |
| **INFERENCE** | Reasoning from evidence that is not a proof. This includes cost constants and readings of pilot data |
| **UNPROVEN** | Open. Stated as a conjecture or a gap |
| **PILOT** | A number from the in-progress G1 runs (`research/results/RAW/g1_*`) or from this note's small checks C7/C8 |
| **A-x** | A labelled assumption (§2.6) |

**Claim levels.** No repository file defines the L0–L6 scale. This note uses the working table of the sibling note `T2_sampling_speedup_statement.md`, so that the two stay consistent:

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

**Question.**
- **Classical baseline.** Draw restarts x₀ from the exact product prior π₀. Relax each with a deterministic local optimiser Φ and keep the lowest endpoint energy.
- **Quantum alternative.** Make the map x₀ ↦ Φ(x₀) coherent and mark the native-free predicate χ_t(x₀) = [E(Φ(x₀)) ≤ t]. Then amplitude-amplify.
- **What both sides pay for** is the energy-level mass p(t) = π₀{x₀ : E(Φ(x₀)) ≤ t}: about 1/p classical runs against about c/√p coherent runs.

What does the quantum side cost end to end, and when could it win?

**Answer in five points.**
1. **Query level.** The saving in runs is quadratic and optimal for black-box amplification. It is a separation only against i.i.d. restarts: nothing here separates quantum from *adaptive* classical search (basin hopping, parallel tempering, SMC). **Theoretical level: L2 relative to the i.i.d.-restart access model. The L3 content (the Toffoli cost of the coherent relaxation) is a provisional INFERENCE estimate.**
2. **Hardware gate at 170 µs.** At the T3 baseline of 170 µs per logical Toffoli, the p-independent hardware gate fails for **every coherent map that evaluates the energy even once per run**:
   - T* ≥ 7.6×10³ yr with nominal gate costs;
   - T* ≥ 31 yr with T3's most generous costs and the slowest measured classical timing (L = 30, S = 1; §4.5a).

   For the converged task map (M-CONVx), whose slot budget covers every observed target restart, T* ≥ 5.0×10⁸ yr at L = 30 and ≥ 4.3×10⁹ yr at L ≥ 60 (nominal).
3. **Hardware gate at 1 µs.** At an optimistic 1 µs, gate H fails for every task-solving map considered. The margin is not large when every quantum-favourable choice is stacked (W_max = 1 yr):
   - at L = 30, T* ≈ 12 yr with the 200-iteration map, or 3.8 yr at the provable floor c = π/4; and 39 yr (13 yr) with the converged task map;
   - at L ≥ 60, where the 200-iteration map misses the deep minima, the stacked converged task map gives T* ≥ 3.0×10² yr (≥ 97 yr at c = π/4).

   So the 1 µs kill at short lengths rests on three named assumptions:
   - the realistic unknown-threshold constant, c ≈ 8 instead of 1.38, which multiplies T* by 34;
   - the convergence budget;
   - the unmeasured speed of an optimised classical kernel.
4. **Instance gate.** It is unmeasured at L ≥ 60. There the energy-level mass within 1 nat of the best endpoint is at the single-hit level p̂ = 1/256 in 88–100% of census crops (Clopper–Pearson 95% interval [1.0×10⁻⁴, 2.2×10⁻²]). So p is censored and the global minimum may be unobserved. At L = 30, where p is mostly resolved, even the interval's lower end exceeds every p* at 170 µs or 1 µs by ≥ 10⁵.
5. **Practical level: L0.** The kill of AA-2 / M9 (`literature/OPPORTUNITY_MATRIX.md`) is confirmed:
   - at 170 µs, independently of the map and of p;
   - at 1 µs, for the maps considered and under the named assumptions.

**Details.**

1. **Query statements** (S1–S3).
   - **Classical i.i.d. restarts** need Θ(1/p) runs. The Ω(1/p) lower bound holds only in the i.i.d.-restart access model. (DERIVED)
   - **Known p.** Amplitude amplification of a coherent restart map A needs π/(2√p) applications of A or A⁻¹ for near-certain success [B1]. Repeated until success it needs an expected ≈ 1.38/√p (THEORETICAL [T4-6 §3], re-derived in check C2). Any strategy needs at least ≈ (π/4)/√p in expectation (DERIVED from [T4-5]). So for known p, c ∈ [0.785, 1.38].
   - **Unknown threshold.** The record process reaches the target set in an expected ≤ 1 + 2c_QS·(p^{−1/2} − 1) applications (THEORETICAL [T4-14, Lemmas 47–48]). This process is Pure Adaptive Search implemented with Grover search [T4-16–T4-19]; with a local optimiser inside A it is quantum basin hopping [T4-20]. For BBHT's unknown-p search, c_QS ≤ 4.5 (THEORETICAL [T4-6, proof of Thm 3]). On measured per-restart energy levels the realised cost is 1.80–1.84·c_QS/√p (check C8).
2. **What a coherent relaxation must pay** (DERIVED unless marked).
   - (a) **Pebbling.** Intermediate iterates must be pebbled. The exact reversible-pebbling trade-off gives, for K = 400 steps, time overheads of 4.4× (12 pebbles), 3.3× (16), 2.4× (24) and 1.9× (32) (§3.5, check C1).
   - (b) **Worst case over branches.** A circuit pays the worst case over branches. With a fixed-slot compilation that worst case is the maximum total number of energy+gradient evaluations, not iterations × line-search trials:
     - 1.25× the classical mean for the census's 200-iteration map at L = 45 (maximum 261 against mean 209);
     - 2.0–3.2× (maximum over mean) for converged relaxations (C8).
   - (c) **No cut-offs.** A reversible gradient step touches all (L−2)(L−3)/2 pairs. Coherent circuits cannot use distance cut-offs, because the pair distances are in superposition.
   - (d) **The relaxation must converge (PILOT, C8).**
     - The census's 200-iteration cap binds for a median of 21% (L = 30) to 83% (L = 100) and 87% (L = 120) of restarts.
     - Converged minima lie 59–531 nats below the census best at L ≥ 60 (531 at 5O37A_120).
     - The restarts that reach the lowest level need 509–871 evaluations at L ≥ 60, at the 89th–100th percentile of their crop. So the slot budget must cover the tail: 440–1,040 evaluations (maximum by L), not the q90 of 257–523.
   - v1's "irreversibility floor" (S4) is kept only as a space remark. Keeping x₀ satisfies it, and it costs no time.
3. **Gate cost** (INFERENCE; labelled constants, §3.7).
   - **Per reversible gradient step:** C_step(L) ≈ 3.0×10⁴·(L−2)(L−3) + 10⁶·L Toffolis. That is 1.6×10⁸ at L = 60, 3.9×10⁸ at L = 100 and 8.1×10⁸ at L = 150.
   - **Cross-check with T3 v1.** T3's costs (`RESOURCE_MODELS.md` v1) give 0.13–2.2× these values (D2 generous to D1), and 0.3–0.5× for D2 central.
   - **Precision.** b = 20 bits is optimistic for coherent L-BFGS. b ≈ 32 is plausible, which multiplies C_step by 1.9–2.0 (INFERENCE, §2.4).
   - **One coherent relaxation** is 5×10² to 10⁴ gradient-step equivalents, including pebbling.
   - **Logical qubits** at L = 60–150 (24 pebbles): 0.9–2.3×10⁵ with a gradient-descent-type state, and 1.0–2.6×10⁶ with an L-BFGS (m = 8) state.
4. **Break-even** (DERIVED from the Babbush form [B46]).
   - **Formulas.** p* = (t_C/(c·S·t_Q))², T* = c²·S·t_Q²/t_C, and p*·T* = t_C/S. Here t_C and t_Q are the classical and quantum times per run of the same map, S is the number of classical cores and c = 1.38.
   - **T\* does not depend on p.** Any quantum win takes at least T* of quantum wall-clock (§3.9).
   - **Window.** A useful win needs (c·t_Q/W_max)² ≤ p < p*. That window spans a factor (W_max/T*)² in p, and closes to a point when T* = W_max.
   - **Floor over maps (new).** A map with K coherent evaluations per run has T* = K·ρ(K)²·T*₁ ≥ T*₁, where T*₁ is the one-evaluation value (§3.9).
   - **Numbers** (c = 1.38, t_C from A-C1; §4.5):

| map | t_Tof | T* (S = 1), L = 30 / 60 / 100 / 150 | p* (S = 1), L = 30 / 60 / 100 / 150 |
|---|---|---|---|
| any map, one coherent energy evaluation (FLOOR-E) | 170 µs | 7.6×10³ / 1.7×10⁴ / 3.7×10⁴ / 7.1×10⁴ yr | 3.0 / 5.3 / 6.9 / 8.0 ×10⁻¹⁶ |
| M-LB2 (200-iteration map, K_eff = 400, 24 pebbles) | 170 µs | 3.1×10⁸ / 7.1×10⁸ / 1.5×10⁹ / 2.9×10⁹ yr | 1.5 / 2.7 / 3.5 / 4.1 ×10⁻¹⁸ |
| M-CONVx (converged task map, slot budget = maximum observed, 24 pebbles) | 170 µs | 5.0×10⁸ / 4.3×10⁹ / 1.1×10¹⁰ / 2.2×10¹⁰ yr | 7.9 / 5.8 / 7.7 / 9.8 ×10⁻¹⁹ |
| M-LB2 | 1 µs | 1.1×10⁴ / 2.5×10⁴ / 5.2×10⁴ / 1.0×10⁵ yr | 4.4 / 7.7 / 10 / 12 ×10⁻¹⁴ |
| M-CONVx | 1 µs | 1.7×10⁴ / 1.5×10⁵ / 4.0×10⁵ / 7.5×10⁵ yr | 2.3 / 1.7 / 2.2 / 2.8 ×10⁻¹⁴ |
| M-LB2 | 1 ns (hypothetical) | 4 / 9 / 19 / 37 days | 4.4 / 7.7 / 10 / 12 ×10⁻⁸ |
| M-CONVx | 1 ns (hypothetical) | 6 / 55 / 146 / 274 days | 2.3 / 1.7 / 2.2 / 2.8 ×10⁻⁸ |

   At S = 10³ classical cores every T* is 10³ times larger and every p* is 10⁶ times smaller. M-CONVx at L = 150 uses the L = 120 budget and mean (1,040 and 370 evaluations), which is a lower bound; C8 did not run at L = 150.
5. **Measured p (PILOT; §4.2).**
   - **Energy-level masses (census).** 16 crops per L, 256 restarts, 200-iteration map. p(1 nat) has median 0.0078 at L = 30. It sits at the single-hit level 1/256 in 44 / 62 / 88 / 100 / 94 / 100% of crops at L = 30 / 45 / 60 / 80 / 100 / 120.
   - **Converged map (C8).** 16 crops (1–4 per L) show the same picture.
   - **Call-count saving at p = 1/256.** 11.6× with known p and a known threshold, which no realisable algorithm has. About 2.0× with the published unknown-threshold constant (record process, c_QS = 4.5). For crops below the single-hit level the saving is not bounded by the data.
   - **What v1 measured.** v1's p_hit (median 0.12 → 0.016 over L = 30 → 100) was the mass of the lowest 2 Å RMSD cluster of *truncated* endpoints. That is not the set the algorithm marks. §4.2c keeps it only as a structural diagnostic, and v1's extrapolated crossing lengths are withdrawn.
6. **Decision criterion** (§3.12), in measured quantities. Both gates are evaluated at the same (L, t_Tof):
   - **Hardware gate, independent of p:** T*(L) = c²·S·t_Q(L)²/t_C(L) ≤ W_max.
   - **Instance gate:** (c·t_Q/W_max)² ≤ p_Q(L) < p*(L, t_Tof) = t_C/(S·T*). In addition, no classical method may reach the target in less time than c·t_Q/√p_Q.
   - **Hardware needed for gate H** (S = 1, M-LB2): t_Tof ≤ 9.7 / 6.4 / 4.4 / 3.2 ns at L = 30 / 60 / 100 / 150 (nominal costs, A-C1). This relaxes to ≤ 150 / 86 / 46 / 28 ns with T3's most generous costs and the measured classical timing. At S = 10³, divide by √10³ ≈ 32.
   - **At the threshold** the window is a single point. p* = 10⁻⁷ is the value at t_Tof = 1 ns only, because p* ∝ t_Tof⁻².
7. **Classical counterarguments** (§3.10–3.11). Each one only widens the gap:
   - classical parallelism enters p* as S⁻², while S_Q independent quantum machines gain only √S_Q [T4-5];
   - better classical proposals raise p, and the quantum call saving shrinks as √p. On a closely related distogram potential, AlphaFold (2020) reports that "a simple gradient descent algorithm" suffices "without complex sampling procedures" [T4-21];
   - adaptive and population methods and learned proposals are not i.i.d. restarts, so the 1/p bound does not bind them. Their coherent versions either cost far more or are Markov chains (the T2 question). This note bounds only restart maps (S11a);
   - on this program's evidence the argmin may be the wrong output for accuracy: restart saturation left ≤ 0.14 Å headroom at 44–60 aa. That figure is PILOT, from 6 dev targets (S33 R10).

### Statement table

| # | Statement (short) | Tag | Theoretical level | Practical level |
|---|---|---|---|---|
| S1 | Classical i.i.d. restarts: expected 1/p runs; ⌈ln(1/δ)/p⌉ for confidence 1−δ; Ω(1/p) in the i.i.d.-restart model only | DERIVED | lower bound in the restart model only | — |
| S2 | AA with coherent A: π/(2√p) applications of A/A⁻¹; expected 1.38/√p with repetition; any strategy ≥ (π/4)/√p | THEORETICAL [B1, T4-6 §3, C55, T4-5] + DERIVED floor | L2 (relative to i.i.d. restarts) | L0 |
| S3 | Unknown threshold (record process): E[N_A] ≤ 1 + 2c_QS(p^{−1/2} − 1) < 2c_QS/√p for c_QS > 1/2; c_QS ≤ 4.5 (BBHT); budget 4C/√p for success ≥ 3/4 | THEORETICAL [T4-14 App. C, T4-6]; evaluation on measured levels DERIVED | L2 (relative to i.i.d. restarts) | L0 |
| S4 | Space remark: a reversible embedding of many-to-one Φ must keep ≥ log₂ max fibre bits; keeping x₀ suffices | THEORETICAL [T4-1] | — | not a cost driver |
| S5 | Exact reversible-pebbling time/space table for K-step relaxation | DERIVED (constructive; BFS-checked for small cases) | L3 ingredient (provisional) | — |
| S6 | A coherent circuit pays the maximum over branches of total evaluations (slot compilation), plus data-dependent sparsity | DERIVED + PILOT | L3 ingredient (provisional) | — |
| S7 | C_step(L) ≈ 3.0×10⁴(L−2)(L−3) + 10⁶L Toffolis per reversible gradient step (b = 20) | INFERENCE (labelled constants) | L3 ingredient (provisional) | — |
| S8 | Logical qubits 0.9–2.3×10⁵ (GD-type) to 1.0–2.6×10⁶ (L-BFGS m = 8) at L = 60–150, 24 pebbles | INFERENCE | — | — |
| S9 | p* = (t_C/(cSt_Q))², T* = c²St_Q²/t_C, p*T* = t_C/S; any win runs ≥ T*; floor T* ≥ T*₁ over maps; L-scaling under A-C1 | DERIVED (form of [B46]) | L3 (provisional: INFERENCE-grade constants) | **L0: KILL at 170 µs (map-independent) and at 1 µs (considered maps, named assumptions)** |
| S10 | Parallelism: classical S enters p* as S⁻²; quantum only √S_Q | DERIVED + THEORETICAL [T4-5] | — | widens the gap |
| S11 | Better proposals: W_Q/W_C = c·S·R·√p; the amplifiable *restart maps* form a subset of the classical procedures | DERIVED (restart maps only) + INFERENCE | — | widens the gap |
| S12 | Decision criterion: gates H and I at matched (L, t_Tof); instance gate censored at L ≥ 60 | DERIVED (conditions) + PILOT | — | decisive |

---

## 1. Statements

### S1. Classical restarts (DERIVED)
Let each restart independently land in the marked set G with probability p.
- The number of restarts to the first hit is geometric with mean 1/p.
- Confidence 1−δ needs N_C(δ) = ⌈ln(1/δ)/(−ln(1−p))⌉ ≤ ⌈ln(1/δ)/p⌉ restarts.
- Wall-clock on S cores is ⌈N_C/S⌉·t_C.
- In the **i.i.d.-restart access model**, where an algorithm sees only independent runs of Φ and their energies, Ω(1/p) runs are necessary.
- **Scope.** This lower bound does *not* apply to adaptive classical methods such as basin hopping, PT or SMC, which are not i.i.d. restarts (S11). Every query-level statement in this note is therefore relative to the i.i.d.-restart model.

### S2. Amplitude amplification with a coherent restart map
- **Setup.** A|0⟩ = √p|ψ_good⟩ + √(1−p)|ψ_bad⟩, where "good" is decided by a phase oracle S_χ computed from A's output registers.
- **Iteration count** (THEORETICAL [B1]). After m iterations of Q = −A S₀ A⁻¹ S_χ the success probability is sin²((2m+1)θ), with sin²θ = p. m = ⌊π/(4θ)⌋ gives success ≥ 1−p with 2m+1 ≈ π/(2√p) applications of A or A⁻¹.
- **Output law** (THEORETICAL [B1]). On success, the output is distributed as π₀ restricted to G and pushed through Φ, because amplification preserves relative amplitudes inside the good subspace. So an amplified run returns the same kind of object as a lucky classical restart.
- **Expected-cost constant.** Repeating an m-iteration run until a measured success costs an expected (2m+1)/sin²((2m+1)θ) applications. The minimum over m is ≈ **1.3801/√p**, at (2m+1)θ = φ* with tan φ* = 2φ*. This is [T4-6 §3], which gives "(z/(4 sin²(z/2)))√(N/t) ≈ 0.69003√(N/t)" iterations; each iteration applies A and A⁻¹ once, so that is 1.380 applications of A (THEORETICAL [T4-6 §3]; re-derived in check C2). This note uses **c = 1.38** in all break-even formulas. It is the best *known* constant, not a floor.
- **Lower bound on the constant** (DERIVED from THEORETICAL [T4-5]). [T4-5] shows that "for any probability of success" Grover's algorithm is optimal. Equivalently, with k oracle queries no algorithm succeeds with probability above sin²((2k+1)θ), for k up to about π/(4θ). Algorithms with intermediate measurements are covered by the standard deferred-measurement argument. A strategy that stops at its first success within k queries is itself a k-query algorithm. So P(T ≤ k) ≤ sin²((2k+1)θ), and E[T] = Σ_k P(T > k) ≥ Σ_{(2k+1)θ≤π/2} cos²((2k+1)θ) → π/(8θ). In applications of A this gives E[N_A] ≥ (π/4)/√p·(1 + o(1)) (check C2: 0.795 at p = 10⁻⁴, 0.786 at 10⁻⁶). The bound applies to any black-box amplification algorithm, because such an algorithm must also work on the search instance with N = 1/p. **So c ∈ [π/4, 1.38]; using π/4 instead of 1.38 lowers every T\* by 3.1×** (§4.5b).
- **Optimality.** Ω(1/√p) applications are necessary [C55, T4-5] (THEORETICAL).
- **Garbage inside A is harmless.** A may leave its history registers dirty, because A⁻¹ undoes them in the next iteration (DERIVED; §3.2).

### S3. Unknown threshold: the record process (THEORETICAL [T4-14 App. C]; evaluation DERIVED on PILOT data)
**This is known prior art.** v1 presented it as new, and that was wrong.
- The procedure is **Pure Adaptive Search** [T4-16, T4-17]: sample from the improving region, repeat. Its Grover implementation is **Grover Adaptive Search** [T4-18, T4-19], and the Dürr–Høyer minimum finder [C56] is the uniform-prior special case [T4-19]. With a local optimiser inside the oracle it is **quantum basin hopping** [T4-20], which states "effort proportional to the square root of the number of basins".
- The general statements used here are those of van Apeldoorn, Gilyén, Gribling and de Wolf [T4-14], Appendix C.

**Setting.** Let X = E(Φ(x₀)) with x₀ ~ π₀. Its values are the endpoint energy levels x₁ < x₂ < …. The target set is {X ≤ t}, with mass p.
- **Procedure.** Measure one run of A. Then repeat an unknown-p search with marked set {X < current value}.
- **Visit probability** (THEORETICAL [T4-14, Lemma 47]). Level x_k is ever the current value with probability Pr(X = x_k)/Pr(X ≤ x_k).
- **Expected cost** (THEORETICAL [T4-14, Lemma 48 and eq. (30)]). The expected number of uses of A and A⁻¹ before the current value is ≤ t is at most C/√p. Tracking the constant explicitly gives

  E[N_A] ≤ 1 + c_QS·Σ_{levels above t} (w_k/W_k)·W_{k−1}^{−1/2} ≤ 1 + 2c_QS·(p^{−1/2} − 1),

  where c_QS·a^{−1/2} bounds the expected cost of the unknown-p search at success probability a. The further bound < 2c_QS/√p holds iff c_QS > 1/2. **That condition holds, because c_QS ≥ π/4 (S2).**
- **Constants.**
  - c_QS ≤ 4.5 for BBHT's search with λ = 6/5 and t ≪ N (THEORETICAL [T4-6, proof of Thm 3]: at most (9/2)·m₀ ≈ (9/4)·√(N/t) Grover iterations, each using A and A⁻¹; plus one A per round). BBHT note that this is "less than four times" the known-t cost.
  - [T4-14] estimate "something like C ≈ 25" for their whole minimum finder, which corresponds to 2c_QS ≲ 25.
  - This closes v1's gap G7.
- **Stopping** (THEORETICAL [T4-14, Thm 49]). Nothing signals arrival at the target. With a budget M ≥ 4C/√p_min the procedure succeeds with probability ≥ 3/4 (Markov), and O(log(1/δ)) repetitions give 1 − δ. The classical budget is ln(1/δ)/p_min.
- **Measured constant** (DERIVED on PILOT data; check C8). On per-restart endpoint energies of converged relaxations, with target = within 1 nat of the best, the realised E[N_A]·√p/c_QS is 1.80–1.84. That is near the bound 2, which a near-continuum of levels saturates. v1's figure of 1.56–1.78 was computed on RMSD-cluster masses, which are not the marked levels; it is withdrawn.
- **Classical analogue.** "Keep the best of i.i.d. restarts" reaches the target in expected 1/p restarts. Thresholding buys a classical sampler nothing, because sampling the improving region is exactly the step Grover search accelerates [T4-18].

§3.3 keeps a short self-contained re-derivation of Lemma 47 and the integral bound as a check. It is not new.

### S4. Space remark: reversibility of a many-to-one map (THEORETICAL [T4-1]; not a cost driver)
- A reversible circuit that maps |x⟩|0^a⟩ to |Φ(x)⟩|j(x)⟩ needs a ≥ log₂ max_y |Φ⁻¹(y)| ancilla bits. This is the injectivity argument behind Bennett's reversible simulation [T4-1].
- Keeping x₀ satisfies it, and A keeps x₀ anyway. That is D·b ≈ 3,900 qubits at L = 100, about 2% of the gradient-descent-type total (S8).
- It costs no time, and garbage is harmless inside amplitude amplification (S2).
- v1 also stated an H_min(π₀) floor for a "converging relaxation that collapses each basin onto one grid point". That premise does not describe the measured map: the census map is truncated (C8), and the energy has flat directions (a median of 33 of 85 Hessian eigenvalues ≤ 10⁻³, §4.6). The floor is dropped.
- Momentum made exactly reversible by an information buffer [T4-9] still buffers about D·log₂(1/γ) bits per step (§3.4).

### S5. Reversible pebbling of K relaxation steps (DERIVED)
Node k of the pebble game is the iterate x_k. The input x₀ is always available. Placing or removing a pebble on node k costs one reversible step (Toffolis C_step) and needs node k−1 pebbled.

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

- **Space.** s × (state size) + workspace. The state is D·b qubits for gradient descent, or (2m+2)·D·b for L-BFGS with memory m.
- **Per Grover iteration.** Each iteration applies A and A⁻¹, so it costs 2·G(K, s)·C_step Toffolis plus preparation and marking.

### S6. Coherent worst-case cost (DERIVED + PILOT)
A circuit has a fixed gate sequence, so it pays for data-dependent control flow at its maximum. The *right* maximum is the one over total work, not over each loop separately.
- **Slot compilation** (DERIVED; construction in §3.6).
  - Compile the optimiser as N_slots identical energy+gradient slots. A small coherent state machine decides whether each slot is a line-search trial or the first evaluation of a new iterate. It carries the L-BFGS two-loop recursion, O(m·D) multiply-adds, which is negligible next to the O(L²) pair loop.
  - The circuit then pays N_slots ≥ max_x n_eval(x), not (iterations) × (maximum trials).
  - Choosing N_slots at a quantile instead truncates the remaining restarts. Truncation changes the marked set only on those restarts, which is classically measurable.
- **The numbers** (PILOT).
  - 200-iteration census map at L = 45 (64 single restarts, check C7): mean 209, median 222, minimum 109, 10th–90th percentile 149–237, maximum 261. The slot penalty is max/mean = **1.25×**. v1 unrolled 200 iterations × 12 Armijo trials to 2,401 evaluations and called it an 11.5× penalty; that is withdrawn.
  - Converged maps (C8): max/mean = 2.0–3.2× and q90/mean = 1.4–1.8× (§4.2a). The q90 is not enough: the target restarts sit at the 89th–100th percentile of evaluation counts at L ≥ 60.
- **Sparsity.** Distance-based sparsity, such as neighbour lists or the constant far tails of the tables, cannot be exploited. The pair distances are in superposition, so every pair is computed.
- **Variable-time amplitude amplification** [T4-15] generalises AA "to the case when parts of the quantum algorithm that is being amplified stop at different times". v1 cited [T4-13] (variable-time *search* over items), which is the wrong tool.
  - At slot penalties of 1.25–3.2× there is little left for VTAA to recover, and its overheads, not re-derived here, may exceed that. Worse, the expensive branches are exactly the target branches, so VTAA cannot shorten them.
  - The real driver of K_eff is convergence (C8), not the line search.

### S7. Toffolis per reversible gradient step (INFERENCE; constants A-T1–A-T6)

C_step(L) = c_pair·(L−2)(L−3)/2 + c_res·L,

with c_pair ≈ 2·4·(12b² + 2G_tab + 10b) + 12b² ≈ 6.1×10⁴ and c_res ≈ 10⁶ at b = 20 and G_tab = 1,001.

| L | 30 | 45 | 60 | 80 | 100 | 150 |
|---|---|---|---|---|---|---|
| C_step nominal (b = 20) | 5.3×10⁷ | 1.0×10⁸ | 1.6×10⁸ | 2.6×10⁸ | 3.9×10⁸ | 8.1×10⁸ |
| b = 16 / b = 24 | 4.5 / 6.2 ×10⁷ | 0.8 / 1.2 ×10⁸ | 1.3 / 2.0 ×10⁸ | 2.1 / 3.3 ×10⁸ | 3.1 / 4.9 ×10⁸ | 6.3 / 10.3 ×10⁸ |
| aggressive (b = 16, ½b² multiply, QROAM lookups) | 3.6×10⁷ | 6.1×10⁷ | 9.1×10⁷ | 1.4×10⁸ | 1.9×10⁸ | 3.7×10⁸ |
| pair-term share (nominal) | 0.43 | 0.55 | 0.63 | 0.70 | 0.74 | 0.82 |

- **Consistency with T2 and T3.**
  - The T2 placeholder, G_grad = 3gL² with g ∈ [5×10³, 3×10⁴] (T2 A-G), brackets these values.
  - T3 v1 (`RESOURCE_MODELS.md`), with T3's quantised-HMC convention C_step = 3·C_E, gives 3·C_E/C_step(nominal) at L = 30 / 60 / 100 / 150 of:
    - D1: 1.20 / 1.69 / 1.99 / 2.18;
    - D2 central: 0.29 / 0.38 / 0.44 / 0.48;
    - D2 generous: 0.13 / 0.16 / 0.18 / 0.20.

    That is **0.13–2.2×** overall (D2 generous to D1), and 0.3–0.5× for D2 central (check C6; §4.5a).
- **Precision** (INFERENCE; see A-T1). At b = 32, C_step is 1.9–2.0× the b = 20 value at L = 100–150 (C5 arithmetic), so T* is 3.6–3.9× larger.
- **Scaling.** T* ∝ C_step².
  - At 170 µs the M-LB2 verdict of S9 survives a C_step overestimate of up to ~1.8×10⁴ (√T* at L = 30).
  - The FLOOR-E verdict at 170 µs survives an overestimate of up to ~90, or ~5.6 with T3-generous costs and the measured classical timing.
  - At 1 µs the M-LB2 verdict survives an overestimate of up to ~10² with S = 1.

### S8. Qubits (INFERENCE)
Logical qubits = x₀ register D·b + s pebbles × state + gradient workspace (≈ 29·L·b). With b = 20 and s = 24:

| L | GD / heavy-ball state (D·b per pebble) | L-BFGS m = 2 (6D·b) | L-BFGS m = 8 (18D·b) | Heavy-ball + buffer, K = 10⁴, γ = 0.9, no pebbles |
|---|---|---|---|---|
| 60 | 9.2×10⁴ | 3.7×10⁵ | 1.0×10⁶ | 2.2×10⁵ |
| 100 | 1.6×10⁵ | 6.2×10⁵ | 1.75×10⁶ | 3.7×10⁵ |
| 150 | 2.3×10⁵ | 9.4×10⁵ | 2.6×10⁶ | 5.5×10⁵ |

- **Physical data qubits.** At about 2d² ≈ 1.9×10³ physical per logical (d ≈ 31, A-Q), the data qubits alone come to **2×10⁸–5×10⁹** physical.
- **Factories** (qualified in v2).
  - Reaching t_Tof = 1 µs by factory parallelism would need about 170 concurrent CCZ factories (≈ 2.6×10⁷ physical qubits at ~1.5×10⁵ per factory region [A56]). 1 ns would need 1.7×10⁵ factories.
  - Those counts are **necessary, not sufficient**. The Toffolis must also be parallel, which needs about R concurrent pair workspaces (each O(b²)–O(10³) logical qubits; T3 §3.9), and the depth of dependent Toffolis is limited by reaction time.
  - [B46] states that parallel factories reduce t_Q "only by a factor that is between about ten and one-hundred" (quote verified by T3, `RESOURCE_MODELS.md` §5.1). So 1 µs via 170 factories is already **outside** [B46]'s range. Both 1 µs and 1 ns are new-hardware scenarios, not "more factories".

### S9. Break-even (DERIVED)
Assume the classical side can run the same map at cost t_C per run, with the same p. Then:
- Classical time-to-target is W_C = t_C/(S·p).
- Quantum time-to-target is W_Q = c·t_Q/√p.
- **Advantage.** W_Q < W_C ⟺ p < p* := (t_C/(c·S·t_Q))².
- **Break-even runtime.** At p = p* both take T* := c²·S·t_Q²/t_C. This is [B46]'s eq. (5) with d = 2 and the constant c. Equivalently, **p*·T\* = t_C/S**.
  - For every p < p*, W_Q = c·t_Q/√p > T*, so **any quantum win takes at least T\* of quantum wall-clock.**
- **Window.** With a tolerable wall-clock W_max, a useful win needs (c·t_Q/W_max)² ≤ p < p*.
  - The ratio of the two ends is (W_max/T*)². The window is non-empty iff T* < W_max, and it is a single point at T* = W_max.
  - In particular p* depends on t_Tof (p* ∝ t_Tof⁻²). A p* quoted at one t_Tof does not transfer to another.
- **Floor over maps** (new in v2). Let a map make K coherent evaluations per run, each costing ≥ C_eval Toffolis, with pebbling overhead ρ(K) ≥ 1. Let the classical side run the same map at K·t_eval.
  - Then T*(K) = c²·S·(K·ρ·C_eval·t_Tof)²/(K·t_eval) = K·ρ²·T*₁ ≥ T*₁, where T*₁ := c²·S·(C_eval·t_Tof)²/t_eval.
  - Any map that marks by energy makes at least one coherent energy evaluation. So T*₁ with C_eval = C_E (energy only), and t_eval an upper bound on the classical energy-only time, is a **map-independent lower bound on T\***. It is used as FLOOR-E with C_E = C_step/3 and t_E ≤ t_g.
  - Longer maps pay linearly in K, not quadratically, because t_C grows with K as well.
- **L-dependence** (DERIVED **under A-C1**, a classical kernel whose cost is ∝ L², with no cut-offs).
  - Both t_Q (∝ C_step) and t_C (∝ t_g) then scale as L², so R(L) = t_Q/t_C tends to a constant: ≈ 3.6–5.8×10⁸ for M-LB2 at 170 µs over L = 30–150.
  - Hence p*(L) ≈ (c·S·R)^{−2} is nearly constant, and T* ∝ L².
  - **With an O(L) classical kernel** (neighbour lists and flat far tails; §3.6), t_C ∝ L, so R ∝ L, p* ∝ L⁻² and T* ∝ L³. That is quantum-unfavourable.
  - The measured PyTorch timings in §4.1 also scale more steeply than L² on a loaded machine.
  - **Longer chains make the hardware gate harder, not easier.** The instance gate becomes easier only if p(L) falls.

### S10. Parallelism (DERIVED + THEORETICAL)
- **Classical.** Restarts are embarrassingly parallel: S cores give S× in wall-clock, and p* ∝ S⁻².
- **Quantum.** Quantum search "cannot be parallelized better than by assigning different parts of the search space to independent quantum computers" [T4-5]. S_Q machines give only √S_Q.
- **Equal machine counts.** Against S classical cores, S quantum computers have p* = (t_C/(c·t_Q))²/S.
- **In practice.** One fault-tolerant machine here is 2×10⁸–5×10⁹ physical qubits (S8), while S = 10³–10⁵ classical cores is routine. Batching already amortises the energy by up to ≈ 15× per core at B = 64 (L = 45; PILOT timing, §4.1).

### S11. Better classical proposals (DERIVED for restart maps + INFERENCE)
Take any randomised procedure B: a proposal law, a relaxation and a marking rule. It has hit probability p(B) and classical per-run time t_C(B). If it can be made coherent, it also has a per-run time t_Q(B). Then

W_Q(B)/W_C(B) = c·S·R(B)·√p(B), with R(B) = t_Q(B)/t_C(B).

Three consequences:
- **(a) Which restart maps the quantum side can amplify** (DERIVED, restricted in v2).
  - Consider every coherent restart map A = U_Φ·(U_P ⊗ I), where U_Φ is a classical reversible circuit (a basis permutation) and U_P prepares the square-root state Σ_x √π(x)|x⟩ of a classically samplable law π. Measuring A|0⟩ reproduces the classical procedure "draw x ~ π, run Φ". Hence the amplifiable restart maps 𝒬_restart form a subset of the classical procedures 𝒞, and the comparison is min_{B∈𝒬_restart} W_Q(B) against min_{B∈𝒞} W_C(B).
  - **Out of scope.** Other unitaries A are *not* covered, and this note does not bound them. That includes A containing a quantum walk, phase estimation, a QSA-prepared coherent tempered state, or other interference whose output law need not be classically samplable (for example nested QSA or walk preparation followed by AA). Those belong to T2 and T5.
- **(b) Better proposals shrink the gain** (DERIVED). For any B the call saving is at most 1/(c·√p(B)). A classical improvement that raises p by g at cost factor h leaves the classical side better off by g/h, and it cuts the quantum side's maximal relative gain by √g.
- **(c) The strong classical methods do not fit into 𝒬_restart cheaply** (INFERENCE). Five families:
  - **Population methods** (SMC [B65 = E74], PERM [D41 = E53], growth algorithms [C84 = E54], fragment regrowth [E55]) need N-particle coherent populations with reversible resampling.
  - **Adaptive search** (basin hopping [T4-11], Monte Carlo minimisation [T4-10], PT [C77 = E20, E33]) is a Markov chain, not i.i.d. restarts. Its quantum analogue is walk or QSA acceleration, the T2 question [A8, A31, A44].
  - **Fragment assembly** [T4-12] is a Monte Carlo chain over fragment insertions, so the same applies.
  - **Better starts for plain gradient descent on distogram potentials.** AlphaFold (2020) built a potential of mean force from predicted inter-residue distances (the same class as the A80 pair term). It reports that "the resulting potential can be optimized by a simple gradient descent algorithm to generate structures without complex sampling procedures" [T4-21, abstract]. That suggests p is not small for this class once the starts are sensible. Distance-geometry/MDS initialisation from the distogram means, and noisy-restart gradient descent, are cheap classical proposals that plausibly push p toward O(1). The restart details in [T4-21]'s body were not re-read (G4).
  - **Learned proposals** (Boltzmann generators [A78 = E76], sequential BGs [E79], AlphaFlow [E80], BioEmu [A79 = E83]) run 10⁸–10¹⁰-MAC networks per sample, which is 10¹⁰–10¹³ Toffolis if made coherent. They can also drive p toward O(1), which leaves nothing to amplify.

### S12. Decision criterion in measured quantities (DERIVED conditions; PILOT inputs)
Define the measured quantities:
- **p_Q(L):** the energy-level mass π₀{x₀ : E(Φ_Q(x₀)) ≤ t} of the coherently implementable map Φ_Q (b-bit fixed point, fixed slot budget) from the product prior. It is measurable **classically**, by running the same deterministic map.
- **p_C(L) and t_C^best(L):** the hit probability and per-run cost of the best classical portfolio. TTT_C(L) = t_C^best/(S·p_C).
- **t_Q(L):** from the gate model (Toffolis × t_Tof).

Amplitude-amplified mode finding is relevant at length L and Toffoli time t_Tof **iff both gates hold at that same (L, t_Tof)**:

**(H) hardware gate, independent of p:** T*(L, t_Tof) = c²·S·t_Q²/t_C^map ≤ W_max;

**(I) instance gate:** (c·t_Q/W_max)² ≤ p_Q(L) < p*(L, t_Tof) = t_C^map/(S·T*), and c·t_Q/√p_Q ≤ TTT_C(L).

- **Gate H at 170 µs.** It fails for every map at every L ≥ 30 (FLOOR-E, §4.5a):
  - T* ≥ 7.6×10³ yr (nominal costs, A-C1);
  - T* ≥ 31 yr (T3-generous costs, measured classical timing, S = 1), or ≥ 10 yr at c = π/4.

  For the converged task map (M-CONVx), T* ≥ 5.0×10⁸ yr (nominal) and ≥ 2.1×10⁶ yr (T3-generous, measured timing). **KILL, practical L0, whatever p turns out to be.**
- **Gate H at 1 µs.** It fails for every task-solving map considered:
  - M-LB2: T* ≥ 1.1×10⁴ yr at L = 30 and ≥ 2.5×10⁴ yr at L ≥ 60 (nominal); ≥ 44 yr (T3-generous, measured timing).
  - M-CONVx: T* ≥ 1.7×10⁴ yr (nominal); ≥ 72 yr at L = 30 and ≥ 8.0×10² yr at L ≥ 60 (T3-generous, measured timing).
  - Stacking every quantum-favourable choice (40 pebbles, T3-generous costs, measured classical timing, S = 1) gives 12 yr at L = 30 with the 200-iteration slot map (3.8 yr at c = π/4). With the converged task map it gives 39 yr (13 yr) at L = 30 and ≥ 3.0×10² yr (97 yr) at L ≥ 60 (§4.5b).
  - The one-evaluation floor itself *passes* at 1 µs with the nominal or T3-D2 costs (0.001–2.5 yr). So the 1 µs kill rests on K_eff (convergence), on c (unknown threshold: ×34) and on classical kernel speed, not on a large margin. **KILL for the considered maps under those named assumptions.**
- **Hypothetical hardware.** Gate H passes only for t_Tof ≤ 3.2–9.7 ns (M-LB2, S = 1, nominal, A-C1). The limit is ≤ 28–150 ns with T3-generous costs and measured timing, and √10³ ≈ 32× tighter at S = 10³ (§4.7).
  - At the passing threshold the p-window is a single point.
  - At t_Tof = 1 ns the window is p ∈ [4.7×10⁻¹¹, 7.7×10⁻⁸] at L = 60 up to [1.2×10⁻⁹, 1.2×10⁻⁷] at L = 150 (M-LB2, S = 1).
- **Instance gate: censored.** At L ≥ 60 the energy-level mass near the best endpoint is at the single-hit level in 88–100% of census crops. p is not measured there, and the global minimum may be unobserved.
- **At L = 30** the census resolves p(1 nat) in 56% of crops (median 0.78%) and p(20 nats) in all of them (median 24%). Even the single-hit 95% lower limit (1.0×10⁻⁴) exceeds every 170 µs or 1 µs p* by ≥ 10⁵, and the 1 ns p* (M-LB2) by ≈ 2×10³.
- **Withdrawn.** v1 extrapolated p_hit(L) and put the instance-gate crossing at L ≈ 500 (median) or ≈ 390 (T3-generous). Those numbers used the wrong predicate (RMSD clusters of truncated endpoints) and mixed (L, t_Tof) points. They are withdrawn; the Review log records the matched-L correction.

---

## 2. Model and assumptions

### 2.1 Energy, coordinates, prior
- **Coordinates.** Internal coordinates x = (θ₁…θ_{L−2}, τ₁…τ_{L−3}), with D = 2L − 5. Structures are rebuilt with ideal 3.8 Å Cα bonds (`src/qapf/protein/energy.py`, `build_ca`).
- **Energy (A-E).** E(x) = E_prior(x) + E_pair(x), the vendored A80 energy at T = 1.
  - E_prior = w_tt·Σ_i −log P̃_i(θ_i, τ_i) + w_w·wall(θ). It is a product over residues.
  - E_pair = Σ_{j−i≥3} [−log p̃^CA_ij(d_ij) − log p̃^CB_ij(d^cb_ij)] + w_s·Σ relu(r₀ − d_ij)².
  - The soft tables p̃_ij are **pair-specific**. Each is a 1,001-point grid on 0–50 Å, derived from esmprior_v1 pair-distance bin probabilities (28 bins) by Gaussian soft-binning (σ = 0.5 Å).
  - Pairs: P(L) = (L−2)(L−3)/2, i.e. 903, 1,653, 4,753 and 10,878 at L = 45, 60, 100 and 150.
  - Energies are positive NLLs of order 10³–10⁴ nats (e.g. about 7×10³ at L = 60 and 2×10⁴ at L = 100).
- **Prior (A-P).** π₀ ∝ exp(−E_prior/T), the λ = 0 end of the G1 path. It is exactly sampleable residue by residue on a 0.5° × 1° grid (360 × 360 = 129,600 cells per residue), with uniform jitter inside cells (`hrex.ExactPrior`).

### 2.2 Relaxation maps and the marked set
- **Classical optimiser.** Batched L-BFGS in `energy.lbfgs`: m = 8, Armijo backtracking with ≤ 12 trials, float64. It stops when an iteration's decrease falls below 10⁻⁶·max(1, |E|), about 0.002–0.02 nats here (|E| ≈ 1.5×10³–2×10⁴), or when no Armijo step is found.
  - **The census map Φ₂₀₀** caps it at 200 iterations. It is **truncated**: C8 shows the cap binds for a median of 21–87% of restarts over L = 30–120 (§4.2a). Every census number is therefore a property of the 200-iteration map.
  - **The converged map Φ_conv** runs the same code until its own stopping rule fires, capped at 5,000 iterations; no C8 restart reached that cap.
- **Coherent candidate maps (A-Φ).**

| Map | Description | Gradient-step equivalents per run (K_eff), before pebbling |
|---|---|---|
| **FLOOR-E** | Any map that marks by energy: at least one coherent energy evaluation (C_E = C_step/3) | 1/3 (lower bound; no pebbling) |
| **M-SLOT2** | Φ₂₀₀, slot-compiled at the maximum observed evaluations (261 at L = 45) | ≈ 270 |
| **M-LB2** | Φ₂₀₀ with a fixed schedule of 200 iterations × 2 line-search trials | 400 (v1 nominal) |
| **M-CONV** | Φ_conv, slot-compiled at max(400, the median over crops of the q90 of evaluations per restart), the pre-registered rule. **Does not solve the task at L ≥ 60**: it truncates target restarts (89th–100th percentile) | 400 / 400 / 453 / 424 / 468 / 523 at L = 30 / 45 / 60 / 80 / 100 / 120 (C8) |
| **M-CONVx** | Φ_conv, slot-compiled at the maximum evaluations observed at that L, which covers every observed target restart. **The converged task map** | 440 / 755 / 835 / 816 / 1,023 / 1,040 at L = 30 / 45 / 60 / 80 / 100 / 120 (C8); L = 150 uses 1,040 (lower bound) |
| **M-LB12** | Φ₂₀₀ with classical settings (12 trials) unrolled | 2,400 |
| **M-HB** | Heavy-ball momentum made exactly reversible with an information buffer [T4-9] | K ≈ 10⁴ steps, no pebbling |
| **M-GD** | Fixed-step gradient descent | K ≳ 10⁴ (≥ ~50× L-BFGS evaluations; §4.6), at the edge of stability |

  - **Energy-only line-search trials** (sensitivity for fixed-schedule maps). Pricing rejected trials at C_E ≈ C_step/3 and only the accepted point at C_step gives K_eff ≈ 330 for M-LB2 and ≈ 1,000 for M-LB12. That lowers T* by ≤ 1.44× and ≤ 5.8× respectively. Slot compilation makes this moot, because a slot must contain the (controlled) gradient circuit anyway.
- **Marked set (A-B, revised).** χ_t(x₀) = [E(Φ(x₀)) ≤ t]. It is native-free: it uses the learned energy only, and t is a classical number chosen by the algorithm from its own earlier measurements.
  - **p(Δ) := π₀{x₀ : E(Φ(x₀)) ≤ E_min + Δ}** is the mass the algorithm pays for. It is measured as the fraction of restarts within Δ nats of the best endpoint.
  - Here E_min is the lowest endpoint found. That is not necessarily the global minimum: at L = 45, PT reached lower energy than multistart (T5 §4.3).
- **Structural clusters (diagnostic only).** The census also clusters endpoints at 2 Å Cα-RMSD. v1 used the mass of the lowest cluster as "p_hit". That is a different set from the marked set. For example, at 2AB0A_100 the lowest cluster holds 8 of 256 restarts, but only 1 restart lies within 20 nats of the best energy. Cluster masses appear only in §4.2c.

### 2.3 Classical cost model
- **A-C1 (nominal).** One energy+gradient on one core takes t_g(L) = 1.8 ms·(L/150)², scaled from the orchestrator-reported 1.8 ms at L = 150 (PILOT) as L² (the pair terms dominate). This is the *fastest* classical figure available, so it is conservative for a kill.
  - **Measured** (PILOT; loaded machines; PyTorch, batch 64, per structure):
    - T4 session: 0.35 / 0.59 / 1.63 / 5.93 ms at L = 45 / 60 / 100 / 150;
    - T3 `--timing` (`RESOURCE_MODELS.md` C2): 0.29 / 0.97 / 1.40 / 2.94 / 5.44 ms at L = 30 / 45 / 60 / 100 / 150.

    Both are 2–6× slower than A-C1. The T3 timing is the single "measured" source used in every sensitivity row of this note, so T3 and T4 now share one t_C source. An idle-machine measurement is open (G11).
  - **An optimised C or GPU kernel with neighbour lists** would plausibly be 10–100× faster than PyTorch (INFERENCE, unmeasured). Since T* ∝ 1/t_C, that raises T* 10–100×. It is used only as a sensitivity, never as a margin.
- **A-C2.** One classical restart costs t_C = K_C·t_g.
  - Φ₂₀₀: K_C = 209. This is the PILOT mean at L = 45; the census mean is 174–217 over L = 30–120.
  - Φ_conv: K_C = the C8 mean, 175 / 243 / 270 / 298 / 347 / 370 at L = 30 / 45 / 60 / 80 / 100 / 120.
  - Prior sampling cost is negligible.
- **A-C3.** S ∈ {1, 10³} independent cores.

### 2.4 Quantum cost model
This note's own gate model (§3.7) is cross-checked against T3 v1: `research/theory/RESOURCE_MODELS.md`, status v1, read 2026-09-27.
- **Frozen snapshot of T3.** T3's script `T3_resource_model.py` was being revised by the T3 lane while this v2 was written (its current revision does not run). T4 therefore re-implements T3 v1's documented C_E formula (S1, §3.2–3.3: C_E = 2·C_build + 2·n_p·τ, with τ_D1 = 26,889 and τ_D2 = 5,712 central) as a frozen snapshot, `C_E_T3v1` in the companion script. It reproduces T3 v1's per-term costs.
- **Rescaling.** If T3's revision changes G(L), rescale with p* ∝ G⁻² and T* ∝ G².
- **A-t.** Logical Toffoli time t_Tof:
  - **170 µs**: the T3 baseline. Surface code with d ≈ 31, 1 µs cycles, one CCZ factory [A56, B46].
  - **1 µs**: optimistic future, as in T2/T5. It is already beyond [B46]'s 10–100× factory-parallelism range (S8).
  - **1 ns**: hypothetical, the order Lemieux et al. say is needed to match a special-purpose classical MCMC machine at a quadratic speedup [A55]. Used only to show what hardware would have to do.
- **A-Q.** Clifford gates are free. Qubits are counted separately (S8). Physical per logical ≈ 2d² with d ≈ 31. Surface-code decoding cost is ignored [C63], which favours the quantum side.
- **A-c.** c = 1.38, the best known constant with known p (S2). The provable floor is π/4 (×0.32 in T*). With an unknown threshold the realistic factor is ≈ 1.8·c_QS ≈ 8.1 with BBHT's c_QS = 4.5 (×34 in T*; S3). All tables use 1.38 unless marked.
- **A-W.** W_max = 1 year where a single number is needed.
- **A-map.** p_Q = p_C for the coherent map, unless stated otherwise. This is a convenience, not a bound: §4.6 shows that p changes between maps in both directions, so p_Q must be measured for the actual coherent map (G2).
- **A-T1 (precision; revised).** b = 20-bit fixed point, sensitivity 16–32. b = 20 is **optimistic** for coherent L-BFGS (INFERENCE):
  - |E| ~ 10⁴ nats against a stopping tolerance of ~0.01–0.02 nats already needs ~20 bits of energy dynamic range, before guard bits (T3 uses a 32-bit accumulator);
  - the curvature pairs sᵀy and 1/ρ lose about log₂κ ≈ 17 bits at the effective condition number κ ~ 10⁵ (§4.6).

  b ≈ 32 is plausible. It multiplies C_step by 1.9–2.0 and T* by 3.6–3.9, which strengthens every verdict here.

### 2.5 Oracle discipline (what is and is not assumed)
- **No free oracles.** All components below are explicit circuits, counted in S7:
  - **Prior preparation.** ⊗_i Σ_c √π_i(c)|c⟩ ⊗ (Hadamard jitter), prepared per residue from a 129,600-entry classical table.
    - Cost ≈ one table-size unary iteration per residue, ~1.3×10⁵ Toffolis. [A60]'s unary-iteration cost, "T-count of 4L − 4", has been verified by T3 (`RESOURCE_MODELS.md` §5.1).
    - The total, ≤ 2×10⁷ at L = 150, is below 10⁻⁴ of one relaxation.
    - v1 quoted "~6×10³ by the dirty-qubit trade-off [T4-7]". [T4-7] states only an asymptotic T-count, O(N/λ + λ·log(N/ε)·log(log N/ε)), without constants, so that figure is dropped. It does not affect any verdict.
    - This preparation is legitimate *only because* π₀ is a product of low-dimensional factors. Loading a correlated conformational law this way would fall under the Grover–Rudolph no-go [B36, B37].
  - **Energy tables.** The per-pair and per-residue tables are classical data compiled into the circuit. The circuit loops over pairs, so pair indices are classical and only the distances are quantum. No QRAM is used. Computing the tables from the sequence (esmprior_v1 forward pass) is the same classical preprocessing the classical side pays.
  - **Marking.** Computed from the output registers. With the energy kept as an output of A, marking is a b-bit comparator.
- **No native structure anywhere.** RMSD appears only in the classical census clustering and in C8's clustering, relative to relaxed endpoints, never to the native (DEP path). C8 never reads the native coordinates stored in the crop files.
- **No simulation was run.** All quantum numbers are resource-model arithmetic. Simulator ≠ hardware, and query count ≠ runtime.

### 2.6 Assumption table

| Label | Assumption | Used in | Direction if wrong |
|---|---|---|---|
| A-E | Energy exactly as vendored (T = 1, DEFAULT_W) | all | — |
| A-P | Prior grid 0.5° × 1° with jitter; b-bit discretisation does not change level masses materially | S2, S3 | UNPROVEN; measurable classically |
| A-Φ | Coherent maps as in §2.2; slot compilation with a negligible state machine | S6, S9 | FLOOR-E is map-independent; M-SLOT2 and M-LB2 are the most favourable maps considered, but task-solving only at L ≲ 45; M-CONVx is the converged task map |
| A-B | Marked set = energy level set within Δ of the best endpoint found | S3, S12 | E_min may not be the global minimum (censoring; T5 §4.3) |
| A-C1 | t_g = 1.8 ms·(L/150)² per core (fastest available) | S9 | measured PyTorch is 2–6× slower (lowers T* 2–6×); an optimised kernel is faster (raises T*) |
| A-C2 | K_C = 209 (Φ₂₀₀) or the C8 mean (Φ_conv) | S9 | PILOT |
| A-T1 | b = 20-bit fixed point (sensitivity 16–32) | S7 | optimistic; b = 32 gives ×1.9–2.0 in C_step |
| A-T2 | b×b multiply ≈ b² Toffolis (the [A56] convention; T3 notes [A59]'s circuit is ≈ 2.25b²) | S7 | aggressive variant ½b² |
| A-T3 | sqrt, reciprocal, division ≈ 2b² each | S7 | INFERENCE |
| A-T4 | Lookup of 2 adjacent entries from a G_tab = 1,001-entry classical table at a quantum index ≈ 2·G_tab Toffolis (unary iteration; [A60], verified by T3); aggressive ≈ 4√(2b·G_tab) (select-swap scaling [T4-7]) | S7 | aggressive variant |
| A-T5 | ×2 to uncompute per-pair intermediates; ×2 for the force-uncompute pass per step | S7 | standard compute–use–uncompute |
| A-T6 | Per-residue terms c_res ≈ 4·(100b² + 2.1×10⁵) ≈ 10⁶ (sin/cos, frames, virtual Cβ, Jᵀ·force back-propagation, θ/τ head) | S7 | subleading at L ≥ 60 |
| A-t | t_Tof ∈ {170 µs, 1 µs, 1 ns} | S9 | scenarios, not predictions |
| A-Q | 2d² physical per logical, d ≈ 31; decoding ignored | S8 | favours quantum |
| A-c | c = 1.38 (known p) | S9 | floor π/4 (×0.32 in T*); unknown threshold ≈ 8.1 (×34) |
| A-map | p_Q = p_C | S9 | UNPROVEN; §4.6 shows the maps differ |

---

## 3. Proofs and derivations

### 3.1 S1 (classical restarts)
- **Upper bound.** Restarts are i.i.d. Bernoulli(p) trials of the event "lands in G". The number to the first success is geometric with mean 1/p. P(no success in N) = (1−p)^N ≤ e^{−pN}, which gives N_C(δ).
- **Lower bound.** In the i.i.d.-restart access model every run is an independent Bernoulli(p) draw, whatever the algorithm does with the outcomes. So P(some success in N runs) ≤ N·p, and constant success probability needs N ≥ Ω(1/p). ∎
- This says nothing about algorithms that correlate their runs (§3.11).

### 3.2 S2 (amplitude amplification with garbage; the constant and its floor)
- **The map A.** Let U_P prepare |π₀⟩ = Σ_x √π₀(x)|x⟩ on the x₀ register. Let U_Φ be a reversible circuit with U_Φ|x⟩|0⟩ = |x⟩|Φ(x)⟩|E(Φ(x))⟩|g(x)⟩, where g(x) is whatever pebbling garbage remains. Set A = U_Φ·(U_P ⊗ I). Then A|0⟩ = Σ_x √π₀(x)|x⟩|Φ(x)⟩|E(Φ(x))⟩|g(x)⟩.
- **Good subspace.** Take the span of basis states whose energy register is ≤ t. It has squared amplitude Σ_{x∈G} π₀(x) = p.
- **Iterate.** Q = −A S₀ A⁻¹ S_χ, where S₀ reflects about |0⟩ on *all* registers, garbage included. Q acts as a rotation by 2θ in span{|ψ_good⟩, |ψ_bad⟩} [B1]. The garbage needs no separate uncomputation, because A⁻¹ inside each Q undoes it.
- **Output.** Measuring the x₀ register after success yields x ∈ G with probability π₀(x)/p, because |ψ_good⟩ is the normalised projection of A|0⟩.
- **Constant** (re-derivation of [T4-6 §3]). Take m iterations, write φ = (2m+1)θ, and use θ ≈ √p for small p.
  - The expected cost to first success is (2m+1)/sin²φ ≈ (φ/sin²φ)/√p.
  - The function φ/sin²φ has derivative [sin²φ − 2φ sin φ cos φ]/sin⁴φ, which is zero at tan φ = 2φ, i.e. φ* = 1.16556. There φ*/sin²φ* = 1.38010 (check C2).
  - [T4-6]'s z = 2φ* = 2.33112 and "0.69003" iterations are the same optimum.
- **Floor.** See S2. The sum Σ_{k: (2k+1)θ ≤ π/2} cos²((2k+1)θ) is a Riemann sum for (1/(2θ))∫₀^{π/2} cos²u du = π/(8θ). ∎
- **Lower bound.** Ω(1/√p) applications are needed [C55, T4-5]. ∎

### 3.3 S3 (record process): self-contained re-derivation of [T4-14, Lemmas 47–48]
**Setting.** Levels 1…n in energy order, masses w_j > 0 (Σ w_j = 1), W_j = Σ_{i≤j} w_i. The target is level 1, which may be a set of levels merged into one of mass p = w₁. The procedure moves a current level J through a strictly decreasing sequence:
- J₀ ~ w;
- each search call succeeds eventually (unless J = 1) and returns a level distributed as w restricted to {1, …, J−1}. This is the output law of §3.2 with G = {E < e_J}.

**Lemma (visit probability; = [T4-14, Lemma 47]).** P(J ever equals j) = w_j/W_j.

*Proof.* Consider the first index in the sequence that lies in {1, …, j}. It exists, because the sequence ends at 1.
- If J₀ ∈ {1, …, j}, that first index is J₀, and conditioned on this event it is distributed as w restricted to {1, …, j}.
- Otherwise the entry happens at some step whose sampling set {1, …, J_prev − 1} contains {1, …, j}. Conditioned on landing in {1, …, j}, it is again distributed as w restricted to {1, …, j}.

So the first entry point has law w_i/W_j on {1, …, j}. Level j is ever visited iff the first entry point is j, because afterwards the sequence stays below j. ∎

(Monte Carlo check with 2×10⁵ runs on a random 12-level spectrum: maximum absolute error 0.0018, check C3.)

**Cost (= [T4-14, Lemma 48], constant tracked).** While J = j ≥ 2, the marked mass is W_{j−1}, and the search uses an expected ≤ c_QS·W_{j−1}^{−1/2} applications. By linearity and the tower rule,

E[N_A until J = 1] ≤ 1 + c_QS·Σ_{j≥2} (w_j/W_j)·W_{j−1}^{−1/2}.

For each j ≥ 2, write a = W_{j−1} and b = W_j, with a < b. Then

(b−a)/(b·√a) ÷ ∫_a^b u^{−3/2} du = (√a + √b)√b/(2b) = (1 + √(a/b))/2 ≤ 1.

So each term is at most the integral of u^{−3/2} over [W_{j−1}, W_j]. Summing gives ≤ ∫_{w₁}^{1} u^{−3/2} du = 2(w₁^{−1/2} − 1), the same integral comparison as [T4-14] eq. (30). Then 1 + 2c_QS(w₁^{−1/2} − 1) < 2c_QS/√w₁ ⟺ c_QS > 1/2, which holds since c_QS ≥ π/4 (S2). ∎

Remarks:
- A mass-weighted continuum of levels saturates the bound. Per-restart endpoint energies are such a continuum, and the realised factor is 1.80–1.84 (C8).
- Intra-basin energy spread only adds levels, and so raises E[N_A]. Truncated relaxations make that spread large (§2.2).

### 3.4 S4 (space remark)
- **Injectivity** [T4-1]. A reversible circuit on basis states is a permutation. If it maps (x, 0) to (Φ(x), j(x)), then x ↦ (Φ(x), j(x)) is injective. So on each fibre Φ⁻¹(y) the values j(x) are distinct, and 2^a ≥ max_y |Φ⁻¹(y)|. Keeping j(x) = x satisfies this with a = D·b. ∎
- **Momentum with a buffer.** Exact reversal of v ← γv − η∇E, x ← x + v in fixed point loses ≈ log₂(1/γ) bits per coordinate per step, which must be buffered [T4-9]. Over K steps that is K·D·log₂(1/γ) bits (INFERENCE; the buffer construction is from [T4-9]'s body, not re-read).

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

### 3.6 S6 (slot compilation)
**Worst-case principle.** A circuit has one gate sequence for all inputs. Compiling an algorithm with data-dependent control flow therefore sizes the circuit for its longest execution. The *measure* of length is up to the compiler.

**Slot construction** (DERIVED). The L-BFGS of `energy.lbfgs` is a sequence of energy+gradient evaluations separated by cheap bookkeeping. Each evaluation is either an Armijo trial at x + t·d or, after acceptance, the start of a new iteration, which needs the two-loop recursion and a new direction d.
- Compile N_slots identical slots. Each slot does four things:
  1. controlled on a "new iteration" flag, update the (s, y, ρ) memory and run the two-loop recursion to get d. This is about 4m·D fixed-point multiplies, i.e. ≈ 2.5×10⁶ Toffolis at L = 100 (m = 8, b = 20), ≈ 0.7% of C_step ≈ 3.9×10⁸;
  2. form the trial point x + t·d;
  3. run one energy+gradient evaluation (C_step);
  4. run the Armijo test and the stopping test, and set the flags and the step t (multiply by 0.3 on rejection).
- A converged branch idles in its remaining slots, controlled on a "done" flag. Its gates are still present.
- The cost is N_slots·C_step·(1 + O(10⁻²)), plus pebbling over N_slots states. The state is (x, E, g, t, d, memory), i.e. the L-BFGS state of S8.
- This is a statement about compiling this optimiser. It is not a circuit lower bound for Φ.

**Numbers.**
- Φ₂₀₀ at L = 45: mean 209, maximum 261, so 1.25× (C7 and the preserved scratch run; §4.6 provenance).
- Φ_conv: see §4.2a.

**Sparsity.** The classical code could skip pairs with d > r_cut, where the tables are flat. The coherent code cannot, because d is in superposition. An O(L) classical kernel is exactly what S9's L³ scaling refers to.

### 3.7 S7 (Toffoli count per reversible gradient step)
One step x_k → x_{k+1} = x_k − η·g(x_k), or one L-BFGS slot, consists of seven stages:
1. **Kinematics** (per residue): sin/cos of θ and τ; composition of the L−1 local frames (a 3×3 product and a translation, 27 multiplications each); virtual Cβ with three normalisations. About 60b² per residue in the forward pass.
2. **Pair loop** (per pair, per channel CA/CB):
   - Δ = X_i − X_j (3b); d² (3b²); d = √d² (2b²); grid index d/h (½b²);
   - lookup of T_ij[g] and T_ij[g+1] (2·G_tab); interpolation (b²); slope (½b²); division by d (2b²);
   - force vector (3b²); accumulation into 6 force registers and the energy (7b).

   That totals **12b² + 2G_tab + 10b ≈ 7.0×10³** at b = 20. v1's formula said 12b; the itemised terms sum to 10b, a ≈ 0.5% difference in c_pair.
3. **Uncompute** the per-pair intermediates: ×2.
4. **Sterics** on Cα pairs: relu² and its derivative, ≈ 3b², ×4.
5. **Back-propagation** from forces to (θ, τ) gradients: suffix sums of forces and of r×F along the chain, then one dot or cross product per coordinate. About 40b² per residue. Plus the θ/τ head: 58 erf-type evaluations and 225 products, or a QROAM on the 0.5° × 1° grid, ≈ 2×10⁵.
6. **Update** x_{k+1} = x_k − ηg into a fresh register: D multiply-adds by a constant, negligible.
7. **Uncompute** g, the forces and the kinematics, i.e. a second pair pass: ×2.

This gives c_pair = 2 channels × 2 (uncompute intermediates) × 2 (uncompute forces) × 7.0×10³ + 12b² ≈ 6.1×10⁴ per pair per step, and c_res ≈ 10⁶ per residue per step. **(INFERENCE; constants A-T1–A-T6.)**

Remarks:
- **Why not a quantum gradient algorithm** (INFERENCE).
  - Jordan-type and later quantum gradient algorithms [T4-8] save queries relative to finite differences, which need D+1 evaluations.
  - Here the classical-exact gradient comes from reverse-mode arithmetic at a small constant multiple of one energy evaluation (the cheap-gradient principle, a standard result not re-verified here). The classical baseline uses exactly that (PyTorch autograd).
  - The phase-estimation gradient would also be stochastic per step, which would branch the trajectories.
  - **Bulger's quantum basin hopping** [T4-20] claims "an extra acceleration proportional to the domain dimension" from Jordan's method. A factor proportional to D is the saving over gradient *estimation* from function values (D+1 evaluations), as in Jordan's comparison; this reading is from the abstract, the body was not read. Against reverse-mode gradients, which cost O(1) energy evaluations, the factor disappears.
- **Why not incremental updates.** Every torsion step moves the whole chain downstream, so all O(L²) distances change each step. Incremental ΔE (O(L) pairs) is unavailable for gradient steps, unlike single-residue Metropolis moves with a classical move index (compare T2 open gap 7, and T3 §3.1).

### 3.8 S8 (qubits)
Arithmetic in §1 S8, with these components:
- workspace ≈ (3 Cα + 3 Cβ + 9 frames + 6 forces + 6 suffix sums)·L·b + D·b + O(b²) ≈ 29·L·b;
- one pebble = one optimiser state;
- the heavy-ball buffer = K·D·log₂(1/γ) bits, with K = 10⁴ and γ = 0.9, plus x, v and x₀.

Check: GD-type totals D·b + 24·D·b + 29·L·b = 9.2×10⁴, 1.56×10⁵ and 2.35×10⁵ at L = 60, 100 and 150. The L-BFGS m = 8 total at L = 100 is 1,746,700.

### 3.9 S9 (break-even and the floor)
1. Take the classical side to run the *same* map, which it can for restart maps (S11a). Then W_C = t_C/(S·p) and W_Q = c·t_Q/√p, and W_Q < W_C ⟺ √p < t_C/(c·S·t_Q) ⟺ p < p*.
2. At p = p*, W_Q = c·t_Q/√p* = c²·S·t_Q²/t_C = T*, and p*·T* = t_C/S. W_Q is decreasing in p, so for p < p*, W_Q > T*.
3. Usefulness also needs W_Q ≤ W_max ⟺ p ≥ (c·t_Q/W_max)². The ratio p*/(c·t_Q/W_max)² = (t_C·W_max/(c²·S·t_Q²))² = (W_max/T*)². So the interval is non-empty iff T* < W_max. ∎
4. **Floor.** With t_Q = K·ρ(K)·C_eval·t_Tof and t_C = K·t_eval: T* = c²·S·K²·ρ²·C_eval²·t_Tof²/(K·t_eval) = K·ρ²·T*₁ ≥ T*₁, since K ≥ 1 and ρ ≥ 1. Any map that marks by energy evaluates E coherently at least once. Replacing t_eval by an upper bound (t_g ≥ t_E) only lowers T*₁. ∎
5. **L-dependence of R under A-C1.** t_Q = K_eff·ρ·C_step(L)·t_Tof and t_C = K_C·t_g(L). With C_step ≈ c_pair·L²/2 and t_g ∝ L², R tends to K_eff·ρ·c_pair·t_Tof/(2·K_C·t_g(L)/L²), a constant. Numerically R is 5.8, 4.4, 3.9 and 3.6 ×10⁸ at L = 30, 60, 100 and 150 (M-LB2, 170 µs). The drift comes from the O(L) terms. With t_g ∝ L instead, R ∝ L. ∎

### 3.10 S10 (parallelism)
- **Classical.** W_C(S) = t_C/(S·p) exactly: independent restarts, no communication.
- **Quantum.** By [T4-5], S_Q quantum machines cannot beat dividing the search space. Splitting the prior into S_Q parts of equal mass gives each part conditional hit probability ≈ S_Q·p on average, so W_Q(S_Q) ≈ c·t_Q/√(S_Q·p).
- **Equal counts.** Setting S_Q = S gives p* = (t_C/(c·t_Q))²/S. ∎

### 3.11 S11 (better proposals; restart maps only)
- **The ratio.** From the two time-to-target expressions, W_Q(B)/W_C(B) = [c·t_Q(B)/√p(B)]·[S·p(B)/t_C(B)] = c·S·R(B)·√p(B).
- **𝒬_restart ⊆ 𝒞.**
  - Let A = U_Φ·(U_P ⊗ I). U_Φ is a basis permutation computed by a classical reversible circuit. U_P prepares Σ_x √π(x)|x⟩ for a law π that has a classical sampler.
  - Then measuring A|0⟩ in the computational basis gives (x, Φ(x), …) with x ~ π, the law of the classical procedure. ∎
  - For a general A, measuring A|0⟩ yields a law that may have no efficient classical sampler. The inclusion is not claimed for such A (S11a).
- **Population methods.** A coherent N-particle SMC needs N× the per-particle coherent cost, plus reversible resampling: prefix sums over N weights and a coherent search per offspring, or a sorting network, i.e. a polylog overhead per particle per generation. Its success probability is that of the whole population run.
- **Adaptive methods.** Basin hopping and PT make each run depend on the previous one. They are Markov chains, and their quantum acceleration is the walk or QSA question [A8, A31, A44], treated in T2.
- **Structured search trees.** Quantum backtracking and branch-and-bound speed up tree search only relative to *the same classical tree* [C57, C60, C61]. Fragment assembly is not a tree search with a bounding function. So no near-quadratic gain beyond S2 is known for it (INFERENCE).

### 3.12 S12 (criterion)
Gates H and I are §3.9 with p_Q and p_C separated, evaluated at one (L, t_Tof). Gate I compares c·t_Q/√p_Q with the best classical TTT_C, which may use a *different* procedure from the coherent map. The necessary condition T* ≤ W_max uses t_C^map, the classical cost of running the coherent map itself. The classical side can always do that for restart maps (§3.11). ∎

---

## 4. Numbers

### 4.1 Classical timings (PILOT)
- **A-C1 (nominal).** 1.8 ms per energy+gradient at L = 150, one core, orchestrator-reported. Scaled as L² that is 0.072 / 0.16 / 0.29 / 0.80 / 1.8 ms at L = 30 / 45 / 60 / 100 / 150.
- **T4 session** (machine at 83–84% CPU from other G1 jobs, one thread):

| L | pairs | per structure, B = 1 | per structure, B = 64 | T3 `--timing`, B = 64 |
|---|---|---|---|---|
| 30 | 378 | — | — | 0.29 ms |
| 45 | 903 | 5.4 ms | 0.35 ms | 0.97 ms |
| 60 | 1,653 | 6.9 ms | 0.59 ms | 1.40 ms |
| 100 | 4,753 | 6.2 ms | 1.63 ms | 2.94 ms |
| 150 | 10,878 | 10.2 ms | 5.93 ms | 5.44 ms |

- **Evaluations per restart.**
  - Φ₂₀₀ (census): mean 174 / 193 / 203 / 213 / 217 / 217 at L = 30 / 45 / 60 / 80 / 100 / 120. The largest per-crop mean at each L is 202–221.
  - Single Φ₂₀₀ restarts at L = 45 (C7): mean 209, median 222, minimum 109, 10th–90th percentile 149–237, maximum 261.
  - Φ_conv: §4.2a.

### 4.2 Mode census (PILOT)
Source: `research/results/RAW/g1_modes/*.json`, written by `scripts/g1_mode_census.py` (another workstream). R = 256 restarts per crop, T = 1, seed 0, map Φ₂₀₀ (200-iteration cap). Snapshot of 2026-09-27: 16 crops at L = 30–100 and 7 at L = 120.

**4.2a Convergence of the census map (C8; PILOT; pre-registered).** The census's own draws (same crops, seed, R = 256 and chunks of 64) were re-relaxed with the same L-BFGS, run to its own stopping rule (cap 5,000 iterations).
- Check: the 200-iteration snapshot reproduces the census's E_best and lowest-cluster mass exactly on every crop.
- Pre-registered hypotheses: **H-C8a holds** (median capped share 41–87% at every L ≥ 60); **H-C8b holds** (median q90 424–523 > 400 at L ≥ 60); **H-C8c holds** (p(1 nat) at the single-hit level in every converged crop at L ≥ 60).
- Crops: 2AB0A_100, 2AB0A_30, 2AB0A_45, 2AB0A_60, 2AB0A_80, 3TE4A_100, 3TE4A_30, 3TE4A_45, 4LPQA_100, 4LPQA_30, 5O37A_100, 5O37A_120, 5O37A_30, 5O37A_45, 5O37A_60, 5O37A_80 (16 crops). The other 5 pre-registered crops are open (G11).

| L | crops | share capped at 200 iterations | capped at 5,000 | evaluations per restart: mean / q90 / max | target restarts (1 nat): evaluations, percentile | median extra drop of capped restarts (nats) | E_min(Φ₂₀₀) − E_min(Φ_conv) (nats) | p(1 nat), Φ_conv | RMSD-cluster mass, median, Φ₂₀₀ → Φ_conv |
|---|---|---|---|---|---|---|---|---|---|
| 30 | 4 | 6–37% | 0% | 145–204 / 212–297 / 373–440 | 226–305, 66–99th pct | 0.1–0.9 | 0.0–0.1 | 0.0039–0.0273 | 0.14 → 0.14 |
| 45 | 3 | 38–52% | 0% | 217–279 / 368–506 / 520–755 | 187–493, 36–89th pct | 5–30 | 0.0–10.7 | 0.0039–0.0078 | 0.18 → 0.18 |
| 60 | 2 | 41–42% | 0% | 266–274 / 448–458 / 761–835 | 594–835, 96–100th pct | 37–45 | 59–61 | 0.0039 | 0.21 → 0.26 |
| 80 | 2 | 62–71% | 0% | 289–307 / 423–424 / 721–816 | 509–532, 96th pct | 96–126 | 128–151 | 0.0039 | 0.14 → 0.27 |
| 100 | 4 | 80–88% | 0% | 315–401 / 428–622 / 770–1023 | 569–871, 89–100th pct | 172–294 | 195–375 | 0.0039 | 0.02 → 0.06 |
| 120 | 1 | 87% | 0% | 370 / 523 / 1040 | 854, 99th pct | 501 | 531 | 0.0039 | 0.00 → 0.04 |

Reading (PILOT):
- The cap binds for a large share of restarts from L = 45 on.
- Converged endpoints of capped restarts fall by a median of 0.1–0.9 nats at L = 30, 5–30 at L = 45 and 37–501 at L ≥ 60 (per crop).
- At L ≥ 60 converged minima are 59–531 nats below the census best. The best-to-second-cluster gaps change by up to two orders of magnitude (e.g. 5O37A_60: 13 → 121 nats; 5O37A_100: 0.8 → 402 nats).
- The target restarts (within 1 nat of the converged best) need 509–871 evaluations at L ≥ 60, at the 89th–100th percentile of their crop. A slot budget must cover them (§2.2, M-CONVx); the pre-registered q90 budget does not (deviation logged).
- **v1's mode gaps, p_hit spectra, K_C = 209 and the slope were all properties of Φ₂₀₀.** Pre-registered rule 1 applies: they are relabelled here, and the extrapolated crossings are withdrawn.

**4.2b Energy-level masses, the marked set** (census, Φ₂₀₀; the census stores the fraction of restarts within Δ of E_best).

| L | crops | p(1 nat): median / single-hit share | p(5 nats): median / single-hit share | p(20 nats): median / single-hit share |
|---|---|---|---|---|
| 30 | 16 | 0.0078 / 44% | 0.020 / 12% | 0.24 / 0% |
| 45 | 16 | 0.0039 / 62% | 0.0078 / 31% | 0.041 / 6% |
| 60 | 16 | 0.0039 / 88% | 0.0039 / 56% | 0.012 / 0% |
| 80 | 16 | 0.0039 / 100% | 0.0039 / 88% | 0.0078 / 38% |
| 100 | 16 | 0.0039 / 94% | 0.0039 / 81% | 0.0039 / 69% |
| 120 | 7 | 0.0039 / 100% | 0.0039 / 100% | 0.0039 / 86% |

- **Single hit.** "Single-hit" means p̂ = 1/256. The Clopper–Pearson 95% interval for one hit in 256 is [1.0×10⁻⁴, 2.2×10⁻²], so a single hit is not an upper bound on p. For such crops the true lowest level may also be unobserved.
- **The converged map** (C8) gives p(1 nat) medians of 0.0078 / 0.0039 / 0.0039 / 0.0039 / 0.0039 / 0.0039 at L = 30 / 45 / 60 / 80 / 100 / 120, i.e. the single-hit level from L = 45 on.
- **So p is censored at L ≥ 60 for any threshold within ~5 nats of the best,** and no slope in L can be estimated from these data.

**4.2c Structural clusters (diagnostic only; not the marked set; Φ₂₀₀).** The 2 Å RMSD-cluster mass of the lowest-energy cluster (v1's "p_hit"):

| L | crops | median | lower quartile | min | single-hit share | median #clusters / 256 |
|---|---|---|---|---|---|---|
| 30 | 16 | 0.117 | 0.072 | 0.0039 | 6% | 82 |
| 45 | 16 | 0.109 | 0.026 | 0.0039 | 6% | 109 |
| 60 | 16 | 0.049 | 0.013 | 0.0039 | 25% | 150 |
| 80 | 16 | 0.059 | 0.019 | 0.0039 | 19% | 181 |
| 100 | 16 | 0.016 | 0.0068 | 0.0039 | 25% | 244 |
| 120 | 7 | 0.008 | 0.0039 | 0.0039 | 43% | 252 |

- **Slope.** The per-protein slope of ln(cluster mass) over L = 30–100 is −0.030 per residue (IQR −0.040 to −0.008). The pooled slope is −0.026. This is a property of Φ₂₀₀'s structural clusters only.
- **Converged map.** C8 changes these masses moderately: e.g. 5O37A_60 0.13 → 0.19, 2AB0A_80 0.16 → 0.32.
- **Call saving.** For single-hit crops the saving at p̂ = 1/256 is 1/(1.38·(1/16)) ≈ 11.6× with known p. It is not bounded by the data.

### 4.3 Record process on the measured levels (DERIVED on PILOT)
**Primary: energy levels of Φ_conv (C8), target within 1 nat of the best endpoint, median crop.**

| L | p(1 nat) | classical 1/p | quantum, known p and threshold (1.38/√p) | quantum, record process with BBHT c_QS = 4.5 | realised E[N_A]·√p/c_QS |
|---|---|---|---|---|---|
| 30 | 0.0078 | 128 | 16 | 103 | 1.80–1.84 |
| 45 | 0.0039 | 256 | 22 | 129 | 1.80–1.84 |
| 60 | 0.0039 | 256 | 22 | 129 | 1.80 |
| 80 | 0.0039 | 256 | 22 | 129 | 1.80 |
| 100 | 0.0039 | 256 | 22 | 129 | 1.80 |
| 120 | 0.0039 | 256 | 22 | 129 | 1.80 |

**Reading.**
- At the measured p the idealised saving (known p and threshold) is 8–12× in calls.
- With a published unknown-threshold constant it is ≈ 1.2–2×, before any per-call overhead.
- For crops below the single-hit level the saving is unbounded by the data, but so is p*: gate H does not depend on p.

**Secondary (v1 table, RMSD-cluster spectra of Φ₂₀₀, kept for the record).**

| L | median E[N_A]/c_QS | median 1/w₁ (classical) | quantum at c_QS = 1.38 (known-p constant) | quantum at c_QS = 4.5 (BBHT) | E[N_A]·√w₁/c_QS, median (max) |
|---|---|---|---|---|---|
| 30 | 4.6 | 8.5 | 6.3 | 20.7 | 1.56 (1.77) |
| 45 | 4.7 | 9.2 | 6.5 | 21.2 | 1.57 (1.83) |
| 60 | 7.8 | 20.8 | 10.8 | 35.1 | 1.65 (1.80) |
| 80 | 7.0 | 17.1 | 9.7 | 31.5 | 1.66 (1.82) |
| 100 | 14.4 | 68.3 | 19.9 | 64.8 | 1.78 (1.82) |
| 120 | 20.7 | 128 | 28.6 | 93.2 | 1.80 (1.83) |

With BBHT's constant the quantum side needs 2.3–2.4× *more* calls at L = 30–45 and 1.7–1.8× more at L = 60–80, is at parity at L = 100 and has 1.4× fewer at L = 120. v1 read these at c_QS = 1 as "a saving of 2–5×". That needed a known p, a known threshold and a constant below the best known (1.38); it is withdrawn.

### 4.4 Gate cost of one coherent relaxation (INFERENCE)
Toffolis per application of A = K_eff·ρ·C_step(L), with prior preparation and marking negligible (§2.5):

| Map | K_eff × ρ (gradient-step equivalents) | L = 60 | L = 100 | L = 150 |
|---|---|---|---|---|
| FLOOR-E | 1/3 | 5.4×10⁷ | 1.3×10⁸ | 2.7×10⁸ |
| M-SLOT2 (s = 24) | 270 × 1.91 = 516 | 8.3×10¹⁰ | 2.0×10¹¹ | 4.2×10¹¹ |
| M-LB2 (s = 24) | 400 × 2.44 = 976 | 1.6×10¹¹ | 3.8×10¹¹ | 7.9×10¹¹ |
| M-CONV (q90 rule, s = 24; not task-solving at L ≥ 60) | 453 × 2.62 = 1,188 (L = 60); 468 × 2.67 = 1,249 (L = 100); 523 × 2.81 = 1,468 (L = 150, L = 120 budget) | 1.9×10¹¹ | 4.9×10¹¹ | 1.2×10¹² |
| **M-CONVx** (converged task map, s = 24) | 835 × 3.25 = 2,716 (L = 60); 1,023 × 3.39 = 3,468 (L = 100); 1,040 × 3.40 = 3,536 (L = 150, L = 120 budget) | 4.4×10¹¹ | 1.3×10¹² | 2.9×10¹² |
| M-LB12 (s = 24) | 2,400 × 3.80 = 9,128 | 1.5×10¹² | 3.6×10¹² | 7.4×10¹² |
| M-HB (no pebbling, buffer) | ≈ 10⁴ | 1.6×10¹² | 3.9×10¹² | 8.1×10¹² |

Wall-clock per application of A, t_Q (M-LB2):
- 170 µs: 308 d / 748 d / 4.3 yr at L = 60 / 100 / 150;
- 1 µs: 1.8 / 4.4 / 9.2 d;
- 1 ns: 157 / 380 / 792 s.

For comparison, t_C = 0.060 / 0.167 / 0.376 s (Φ₂₀₀, A-C1).

### 4.5 Break-even (DERIVED arithmetic; c = 1.38, t_g from A-C1, W_max = 1 yr; check C6)

| Map | L | t_Tof | R = t_Q/t_C | p*, S = 1 | T*, S = 1 | p*, S = 10³ | T*, S = 10³ |
|---|---|---|---|---|---|---|---|
| M-LB2 | 30 | 170 µs | 5.8×10⁸ | 1.5×10⁻¹⁸ | 3.1×10⁸ yr | 1.5×10⁻²⁴ | 3.1×10¹¹ yr |
| M-LB2 | 60 | 170 µs | 4.4×10⁸ | 2.7×10⁻¹⁸ | 7.1×10⁸ yr | 2.7×10⁻²⁴ | 7.1×10¹¹ yr |
| M-LB2 | 100 | 170 µs | 3.9×10⁸ | 3.5×10⁻¹⁸ | 1.5×10⁹ yr | 3.5×10⁻²⁴ | 1.5×10¹² yr |
| M-LB2 | 150 | 170 µs | 3.6×10⁸ | 4.1×10⁻¹⁸ | 2.9×10⁹ yr | 4.1×10⁻²⁴ | 2.9×10¹² yr |
| M-LB2 | 30 | 1 µs | 3.4×10⁶ | 4.4×10⁻¹⁴ | 1.1×10⁴ yr | 4.4×10⁻²⁰ | 1.1×10⁷ yr |
| M-LB2 | 60 | 1 µs | 2.6×10⁶ | 7.7×10⁻¹⁴ | 2.5×10⁴ yr | 7.7×10⁻²⁰ | 2.5×10⁷ yr |
| M-LB2 | 100 | 1 µs | 2.3×10⁶ | 1.0×10⁻¹³ | 5.2×10⁴ yr | 1.0×10⁻¹⁹ | 5.2×10⁷ yr |
| M-LB2 | 150 | 1 µs | 2.1×10⁶ | 1.2×10⁻¹³ | 1.0×10⁵ yr | 1.2×10⁻¹⁹ | 1.0×10⁸ yr |
| M-LB2 | 60 | 1 ns | 2.6×10³ | 7.7×10⁻⁸ | 9 d | 7.7×10⁻¹⁴ | 25 yr |
| M-LB2 | 100 | 1 ns | 2.3×10³ | 1.0×10⁻⁷ | 19 d | 1.0×10⁻¹³ | 52 yr |
| M-LB2 | 150 | 1 ns | 2.1×10³ | 1.2×10⁻⁷ | 37 d | 1.2×10⁻¹³ | 100 yr |
| M-CONV (q90) | 100 | 170 µs | 3.0×10⁸ | 5.9×10⁻¹⁸ | 1.5×10⁹ yr | 5.9×10⁻²⁴ | 1.5×10¹² yr |
| **M-CONVx** | 30 | 170 µs | 8.1×10⁸ | 7.9×10⁻¹⁹ | 5.0×10⁸ yr | 7.9×10⁻²⁵ | 5.0×10¹¹ yr |
| **M-CONVx** | 60 | 170 µs | 9.5×10⁸ | 5.8×10⁻¹⁹ | 4.3×10⁹ yr | 5.8×10⁻²⁵ | 4.3×10¹² yr |
| **M-CONVx** | 100 | 170 µs | 8.3×10⁸ | 7.7×10⁻¹⁹ | 1.1×10¹⁰ yr | 7.7×10⁻²⁵ | 1.1×10¹³ yr |
| **M-CONVx** | 60 | 1 µs | 5.6×10⁶ | 1.7×10⁻¹⁴ | 1.5×10⁵ yr | 1.7×10⁻²⁰ | 1.5×10⁸ yr |
| **M-CONVx** | 100 | 1 µs | 4.9×10⁶ | 2.2×10⁻¹⁴ | 4.0×10⁵ yr | 2.2×10⁻²⁰ | 4.0×10⁸ yr |
| **M-CONVx** | 60 | 1 ns | 5.6×10³ | 1.7×10⁻⁸ | 55 d | 1.7×10⁻¹⁴ | 150 yr |
| **M-CONVx** | 100 | 1 ns | 4.9×10³ | 2.2×10⁻⁸ | 146 d | 2.2×10⁻¹⁴ | 400 yr |
| M-LB12 | 100 | 170 µs | 3.6×10⁹ | 4.0×10⁻²⁰ | 1.3×10¹¹ yr | 4.0×10⁻²⁶ | 1.3×10¹⁴ yr |
| M-LB12 | 100 | 1 µs | 2.1×10⁷ | 1.2×10⁻¹⁵ | 4.6×10⁶ yr | 1.2×10⁻²¹ | 4.6×10⁹ yr |
| M-HB | 100 | 1 ns | 2.3×10⁴ | 9.7×10⁻¹⁰ | 5.5 yr | 9.7×10⁻¹⁶ | 5.5×10³ yr |

The full grid (all maps × L = 30/60/100/150 × three Toffoli times × two values of S) is printed by check C6.

### 4.5a Cross-check with T3 v1 gate costs (DERIVED arithmetic on the frozen T3 v1 formulas)
T3 v1 costs one full coherent energy, C_E, with build/unbuild and temporaries uncomputed, for three designs:
- **D1:** literal 1,001-point tables with a square root;
- **D2 central:** per-pair cubic splines in d², QROAM lookups;
- **D2 generous:** D2 with T3's most optimistic parameters.

Its quantised-HMC variant prices a gradient at 3·C_E, and T4 takes C_step = 3·C_E. Below, T* is in years for S = 1 and c = 1.38, at L = 30 / 60 / 100 / 150. "A-C1" and "meas" are the two classical t_g sources of §2.3.

| Gate-cost source | C_step | map | T*, 170 µs, A-C1 | T*, 170 µs, meas | T*, 1 µs, A-C1 | T*, 1 µs, meas |
|---|---|---|---|---|---|---|
| This note, nominal | 5.3×10⁷ / 1.6×10⁸ / 3.9×10⁸ / 8.1×10⁸ | FLOOR-E | 7.6×10³ / 1.7×10⁴ / 3.7×10⁴ / 7.1×10⁴ | 1.9×10³ / 3.6×10³ / 1.0×10⁴ / 2.3×10⁴ | 0.26 / 0.60 / 1.3 / 2.5 | 0.07 / 0.12 / 0.35 / 0.81 |
| | | M-LB2 | 3.1×10⁸ / 7.1×10⁸ / 1.5×10⁹ / 2.9×10⁹ | 7.7×10⁷ / 1.5×10⁸ / 4.1×10⁸ / 9.6×10⁸ | 1.1×10⁴ / 2.5×10⁴ / 5.2×10⁴ / 1.0×10⁵ | 2.7×10³ / 5.1×10³ / 1.4×10⁴ / 3.3×10⁴ |
| T3 D1 central | 6.3×10⁷ / 2.7×10⁸ / 7.8×10⁸ / 1.8×10⁹ | M-LB2 | 4.4×10⁸ / 2.0×10⁹ / 6.0×10⁹ / 1.4×10¹⁰ | 1.1×10⁸ / 4.2×10⁸ / 1.6×10⁹ / 4.6×10⁹ | 1.5×10⁴ / 7.1×10⁴ / 2.1×10⁵ / 4.8×10⁵ | 3.8×10³ / 1.5×10⁴ / 5.6×10⁴ / 1.6×10⁵ |
| T3 D2 central | 1.5×10⁷ / 6.2×10⁷ / 1.7×10⁸ / 3.9×10⁸ | M-LB2 | 2.6×10⁷ / 1.1×10⁸ / 2.9×10⁸ / 6.6×10⁸ | 6.5×10⁶ / 2.2×10⁷ / 7.9×10⁷ / 2.2×10⁸ | 9.1×10² / 3.6×10³ / 1.0×10⁴ / 2.3×10⁴ | 2.2×10² / 7.5×10² / 2.7×10³ / 7.5×10³ |
| T3 D2 generous | 6.8×10⁶ / 2.6×10⁷ / 7.1×10⁷ / 1.6×10⁸ | FLOOR-E | 1.3×10² / 4.6×10² / 1.2×10³ / 2.7×10³ | **31** / 95 / 3.3×10² / 8.9×10² | 0.004 / 0.016 / 0.042 / 0.094 | 0.001 / 0.003 / 0.012 / 0.031 |
| | | M-LB2 | 5.1×10⁶ / 1.9×10⁷ / 5.0×10⁷ / 1.1×10⁸ | 1.3×10⁶ / 3.9×10⁶ / 1.4×10⁷ / 3.7×10⁷ | 1.8×10² / 6.5×10² / 1.7×10³ / 3.8×10³ | **44** / 1.3×10² / 4.7×10² / 1.3×10³ |
| | | M-CONVx | 8.3×10⁶ / 1.1×10⁸ / 3.8×10⁸ / 8.2×10⁸ | 2.1×10⁶ / 2.3×10⁷ / 1.0×10⁸ / 2.7×10⁸ | 2.9×10² / 3.9×10³ / 1.3×10⁴ / 2.8×10⁴ | **72** / 8.0×10² / 3.6×10³ / 9.4×10³ |

**Reading (INFERENCE).**
- This note's nominal C_step lies between T3's D2 and D1 designs: within factors of about 2.5 (D2 central) and 2 (D1) at L ≥ 60, and 3.4 and 1.2 at L = 30.
- T3's D2 design replaces the 1,001-point tables and the square root by cubics in d². That change, not arithmetic precision, is the main lever.
- **At 170 µs**, even the one-evaluation floor fails gate H with T3's most generous costs and the slower measured classical timing: ≥ 31 yr at L = 30.
- **At 1 µs**, the floor passes with the nominal and T3-D2 costs, so the 1 µs verdict depends on the map (M-LB2 ≥ 44 yr; M-CONVx ≥ 72 yr, both with T3-generous costs and measured timing).
- If T3's revision changes these functions, rescale with T* ∝ C_step² and p* ∝ C_step⁻².

### 4.5b Worst case for the verdict, and the constant (DERIVED arithmetic; check C6)
**Stack every quantum-favourable choice the note allows:**
- the cheapest map considered, Φ₂₀₀ slot-compiled at K_eff = 270 (M-SLOT2), which solves the task only at L ≲ 45; the converged task map M-CONVx is shown alongside;
- 40 pebbles (ρ = 1.85);
- T3 D2-generous gate costs;
- the slower measured classical timing;
- S = 1.

| L | M-SLOT2: T* at 1 µs, c = 1.38 | M-SLOT2: c = π/4 (floor) | M-SLOT2: T* at 170 µs, c = 1.38 | M-SLOT2: p* at 1 µs | converged task map (M-CONVx, s = 40): T* at 1 µs, c = 1.38 / π/4 | M-CONVx: p* at 1 µs |
|---|---|---|---|---|---|---|
| 30 | 11.6 yr | 3.8 yr | 3.4×10⁵ yr | 1.7×10⁻¹⁰ | 39 / 13 yr | 4.1×10⁻¹¹ |
| 60 | 35 yr | 11 yr | 1.0×10⁶ yr | 2.6×10⁻¹⁰ | 3.0×10² / 97 yr | 4.0×10⁻¹¹ |
| 100 | 124 yr | 40 yr | 3.6×10⁶ yr | 1.6×10⁻¹⁰ | 1.7×10³ / 5.6×10² yr | 1.9×10⁻¹¹ |

At L ≥ 60 the 200-iteration map (M-SLOT2) does not solve the task: converged minima are 59–531 nats lower (§4.2a; up to 11 nats at L = 45). Its rows there are the most favourable bound, not a realistic design. At L = 30 truncation costs < 1 nat, so both rows apply.

**Assumptions that carry the 1 µs kill in this row.**
- The constant: c ≈ 1.8·c_QS ≈ 8.1 for a realisable unknown-threshold search (×34 in T*), instead of 1.38.
- The convergence budget: the converged task map M-CONVx instead of M-SLOT2 multiplies T* by 5.8 (L = 30), 22 (L = 60) and 27 (L = 100), with the same costs.
- The classical kernel: an optimised kernel 10–100× faster than PyTorch (unmeasured) multiplies T* by 10–100.
- The instance gate: at L = 30 the census median p(1 nat) is 7.8×10⁻³, and even the single-hit 95% lower limit (1.0×10⁻⁴) is ≥ 4×10⁵ times p* ≈ 2×10⁻¹⁰.

Without any of these the margin at L = 30 is about 12× (3.8× at c = π/4).

**Sensitivity of T\* to the constant.** T* ∝ c²:

| c | T* multiplier |
|---|---|
| π/4 (provable floor) | 0.32 |
| 1.38 (known p; nominal) | 1 |
| ≈ 8.1 (record process, BBHT c_QS = 4.5, realised factor 1.8) | 34 |
| ≈ 22 ([T4-14]'s rough C ≈ 25 for the whole minimum finder, × the realised 0.9 of the bound) | ≈ 260 |

### 4.6 Coherent-friendly optimisers vs L-BFGS on 5O37A_45 (PILOT; check C7 and preserved scratch runs)
**Setup.** The same seed-0 prior draws as the census. Each optimiser is compared with Φ₂₀₀ from the same x₀. "Same basin" means within 2 Å Cα-RMSD of that start's Φ₂₀₀ endpoint. **Caveat:** 47% of Φ₂₀₀ runs at this crop are still descending at iteration 200 (C8), so the L-BFGS reference is itself truncated.

**Provenance.**
- Diverging GD: `t4_gd_check.py`, 64 starts, checkpoints K = 200 / 1,000 / 5,000.
- Stable and clipped GD: `t4_gd_check3.py`, 16 starts, K = 500 / 2,000 / 10,000.
- Hessians: `t4_gd_check2.py`, 16 starts.
- Scripts, logs and the 64-start JSON are preserved in `research/results/RAW/t4_checks/`. Check C7 reruns the Hessian and two GD rows.

| Map | starts | checkpoints | same basin; median E − E_LBFGS | Energy increases |
|---|---|---|---|---|
| GD, η = 3×10⁻⁴ / 10⁻³ / 3×10⁻³ (diverging) | 64 | K = 200 / 1,000 / 5,000 | 0 at every checkpoint; +2.5×10³ / +4.0×10³ / +6.5×10³ at K = 5,000 | 44 / 48 / 44% of steps |
| GD, η = 10⁻⁵ | 16 | K = 500 / 2,000 / 10,000 | 0.00; +392 → 0.25; +184 → **0.44; +29** | 0.2% |
| GD, η = 2×10⁻⁵ | 16 | K = 500 / 2,000 / 10,000 | 0.06; +282 → 0.25; +106 → **0.44; −2.3** (50% below L-BFGS) | 21% (edge of stability) |
| Clipped GD, η = 10⁻³, clip 0.02 rad | 16 | K = 500 / 2,000 / 10,000 | 0.00; +715 → 0.00; +713 → 0.00; +713 (limit cycle) | 50% |

**Hessian spectrum** of the energy in internal coordinates (16 Φ₂₀₀ endpoints):
- at the endpoints: λ_max median 281, maximum 8.7×10⁴; smallest eigenvalue above 10⁻³ median 0.50; a median of 33 of 85 eigenvalues ≤ 10⁻³ (flat directions);
- at 4 prior draws: |λ|_max = 6.1×10³–9.7×10⁴, from steric clashes;
- so a globally stable fixed step is η ≲ 2×10⁻⁵, and the effective condition number is ~10⁵.

**Reading (INFERENCE).**
- Fixed-step descent, the textbook "reversible-friendly" map, needs **K ≳ 10⁴** steps: at least ≈ 50× the 209 evaluations of Φ₂₀₀. Even then it runs at the edge of stability.
- It lands in *different* basins from L-BFGS: 44% agreement after 10⁴ steps at either stable step size. At η = 2×10⁻⁵ it ends lower than truncated L-BFGS in 50% of runs; at η = 10⁻⁵, 19% (still descending).
- **p is a property of the pair (landscape, map), not of the landscape.** A-map (p_Q = p_C) is an assumption, and a coherent design must be validated by classically measuring p_Q for the exact b-bit map.
- An L-BFGS-type coherent map (slot-compiled) is therefore the realistic choice.

### 4.7 Required hardware and the p-window (DERIVED)
**Hardware needed for gate H** (T* ≤ 1 yr), in t_Tof at L = 30 / 60 / 100 / 150:

| Map, cost source, t_g | S = 1 | S = 10³ |
|---|---|---|
| M-LB2, nominal, A-C1 | 9.7 / 6.4 / 4.4 / 3.2 ns | 0.31 / 0.20 / 0.14 / 0.10 ns |
| M-LB2, nominal, measured | 19 / 14 / 8.4 / 5.5 ns | 0.61 / 0.44 / 0.27 / 0.17 ns |
| M-LB2, T3 D2 generous, A-C1 | 75 / 39 / 24 / 16 ns | 2.4 / 1.2 / 0.76 / 0.51 ns |
| M-LB2, T3 D2 generous, measured | 150 / 86 / 46 / 28 ns | 4.8 / 2.7 / 1.5 / 0.89 ns |
| **M-CONVx**, nominal, A-C1 | 7.6 / 2.6 / 1.6 / 1.2 ns | 0.24 / 0.082 / 0.050 / 0.037 ns |
| **M-CONVx**, T3 D2 generous, measured | 118 / 35 / 17 / 10 ns | 3.7 / 1.1 / 0.53 / 0.33 ns |

- **In Toffoli rates**, these are 6.7×10⁶ to 2.7×10¹⁰ logical Toffolis per second. That is 1.1×10³ to 4.6×10⁶ times the T3-baseline rate of 5.9×10³ /s.
- **Relative to A-C1**, the measured classical timing relaxes the limits by √(t_meas/t_A-C1) = 1.7–2.2× at L = 30–150.

**Window at t_Tof = 1 ns** (S = 1, W_max = 1 yr), with width factor (W_max/T*)²:

| map | L = 60 | L = 100 | L = 150 |
|---|---|---|---|
| M-LB2 | [4.7×10⁻¹¹, 7.7×10⁻⁸], 1.7×10³ | [2.8×10⁻¹⁰, 1.0×10⁻⁷], 3.7×10² | [1.2×10⁻⁹, 1.2×10⁻⁷], 99 |
| **M-CONVx** | [3.6×10⁻¹⁰, 1.7×10⁻⁸], 46 | [3.5×10⁻⁹, 2.2×10⁻⁸], 6.4 | [1.6×10⁻⁸, 2.8×10⁻⁸], 1.8 |

At S = 10³ the window is empty: T* > 11 yr. For the converged task map the 1 ns window is already nearly closed at L ≥ 100 (width 1.8–6.4).

**No extrapolation.** v1 extrapolated p_hit(L) with the RMSD-cluster slope and read off crossing lengths. That is withdrawn:
- the slope belongs to the wrong set (§2.2);
- the energy-level p is censored at L ≥ 60 (§4.2b);
- the crossings were read at a p* quoted for 1 ns while the gate-H limits were quoted at other t_Tof.

The only statements the data support are these. At L = 30, p(1 nat) is resolved in 56% of crops (median 7.8×10⁻³), and even the single-hit 95% lower limit (1.0×10⁻⁴) exceeds the 1 ns p* (4.4×10⁻⁸, M-LB2) by ≈ 2×10³ and every 170 µs or 1 µs p* by ≥ 10⁵. At L ≥ 60, p is not measured.

---

## 5. Literature

### 5.1 Bibliography keys used (verified in the literature phase; `BIBLIOGRAPHY.md`)

| Key | Paper | Used for | Label |
|---|---|---|---|
| B1 | Brassard, Høyer, Mosca, Tapp 2002 | AA iteration, output law, QSearch with unknown a | THEORETICAL |
| B2 | Brassard, Høyer, Tapp 1998 | quantum counting (estimating p at O(1/√p)) | THEORETICAL |
| C54 | Grover 1996 | search | THEORETICAL |
| C55 | Bennett, Bernstein, Brassard, Vazirani 1997 | Ω(√N) lower bound | THEORETICAL |
| C56 | Dürr, Høyer 1996 | minimum finding, O(c√N) with probability ≥ 1 − 2^{−c} (abstract); the uniform-prior case of GAS [T4-19] | THEORETICAL |
| C57, C60, C61 | Montanaro 2018/2020; Chakrabarti et al. 2022 | backtracking / B&B speedups relative to the same tree | THEORETICAL |
| C63 | Campbell, Khurana, Montanaro 2019 | decoding cost erases Grover-type advantage | resource estimate |
| A56 = C64 | Sanders et al. 2020 | 170 µs/Toffoli, factory footprint, "a day and a million physical qubits … four CPU-minutes" | NO ADVANTAGE (resource) |
| B46 = C65 | Babbush et al. 2021 | T* = t_Q²·S/t_C (d = 2), eq. (5); factories cut t_Q "only by a factor that is between about ten and one-hundred" (verified by T3) | NO ADVANTAGE (quadratic) |
| A55 | Lemieux et al. 2020 | ~1 ns logical gates to match a special-purpose MCMC machine | resource |
| A59 | Häner, Roetteler, Svore 2018 | reversible arithmetic building blocks (constants checked by T3) | — |
| A60 | Babbush et al. 2018 | unary-iteration lookups, "T-count of 4L − 4" (**verified by T3**, `RESOURCE_MODELS.md` §5.1) | — |
| F59 | Berry et al. 2019 | QROAM lookups (App. C costs checked by T3) | — |
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
| T4-5 | C. Zalka, "Grover's quantum searching algorithm is optimal," PRA 60:2746–2751 (1999). arXiv quant-ph/9711070 (= T5's X15) | arXiv abstract (re-read 2026-09-27): "for any probability of success Grovers quantum searching algorithm is optimal"; near-certain success needs π/4·√N queries; "cannot be parallelized better than by assigning different parts of the search space to independent quantum computers". The extension to intermediate measurements is by deferred measurement (standard, not from [T4-5]) |
| T4-6 | M. Boyer, G. Brassard, P. Høyer, A. Tapp, "Tight bounds on quantum searching," Fortschr. Phys. 46:493–506 (1998). arXiv quant-ph/9605034 (= T5's X16) | **PDF text checked (v2):** §3 "(z/(4 sin²(z/2)))√(N/t) ≈ 0.69003√(N/t)" expected iterations with restarts; Thm 3 proof: λ = 6/5, "upper-bounded by (9/2)m₀", "≈ (9/4)√(N/t) when t ≪ N", "less than four times" the known-t cost |
| T4-7 | G. H. Low, V. Kliuchnikov, L. Schaeffer, "Trading T gates for dirty qubits in state preparation and unitary synthesis," Quantum 8, 1375 (2024). arXiv 1812.00954 | arXiv abstract: T-count O(N/λ + λ·log(N/ε)·log(log N/ε)); no constants, so used for scaling only |
| T4-8 | A. Gilyén, S. Arunachalam, N. Wiebe, "Optimizing quantum optimization algorithms via faster quantum gradient computation," SODA 2019, 1425–1444. arXiv 1711.00465 | arXiv abstract (quadratic improvement over Jordan's algorithm; smoothness assumptions) |
| T4-9 | D. Maclaurin, D. Duvenaud, R. P. Adams, "Gradient-based hyperparameter optimization through reversible learning," arXiv 1502.03492 (2015) | arXiv abstract ("exactly reversing the dynamics of stochastic gradient descent with momentum"). The information-buffer detail is from the body and was **not re-read**; venue not verified |
| T4-10 | Z. Li, H. A. Scheraga, "Monte Carlo-minimization approach to the multiple-minima problem in protein folding," PNAS 84:6611–6615 (1987). DOI 10.1073/pnas.84.19.6611 | Crossref metadata |
| T4-11 | D. J. Wales, J. P. K. Doye, "Global optimization by basin-hopping and the lowest energy structures of Lennard-Jones clusters containing up to 110 atoms," J. Phys. Chem. A 101:5111–5116 (1997). DOI 10.1021/jp970984n | Crossref metadata |
| T4-12 | K. T. Simons, C. Kooperberg, E. Huang, D. Baker, "Assembly of protein tertiary structures from fragments with similar local sequences using simulated annealing and Bayesian scoring functions," J. Mol. Biol. 268:209–225 (1997). DOI 10.1006/jmbi.1997.0959 | Crossref metadata |
| T4-13 | A. Ambainis, "Quantum search with variable times," arXiv quant-ph/0609168 (2006) | arXiv abstract: O(√(t₁² + … + t_n²)) for search over items with different query times. **Not the tool for S6** (v2); see T4-15 |
| T4-14 | J. van Apeldoorn, A. Gilyén, S. Gribling, R. de Wolf, "Quantum SDP-Solvers: Better upper and lower bounds," Quantum 4, 230 (2020). arXiv 1705.01843 | **PDF text checked:** App. C, Meta-Algorithm 2 and Algorithm 3 (generalized minimum-finding); Lemma 47 (Pr(x_k ∈ S(X)) = Pr(X = x_k)/Pr(X ≤ x_k)); Lemma 48 (expected uses of U, U⁻¹ ≤ C/√Pr(X ≤ x_k), eq. (30) integral bound); "something like C ≈ 25"; Thm 49 (M ≥ 4C/√Pr(X ≤ x), success ≥ 3/4) |
| T4-15 | A. Ambainis, "Variable time amplitude amplification and a faster quantum algorithm for solving systems of linear equations," arXiv 1010.4458 | arXiv abstract: "a generalization of amplitude amplification to the case when parts of the quantum algorithm that is being amplified stop at different times". Body (cost and polylog overheads) not re-read; venue not verified |
| T4-16 | Z. B. Zabinsky, R. L. Smith, "Pure adaptive search in global optimization," Math. Program. 53:323–338 (1992). DOI 10.1007/BF01585710 | Crossref metadata |
| T4-17 | Z. B. Zabinsky, G. R. Wood, M. A. Steel, W. P. Baritompa, "Pure adaptive search for finite global optimization," Math. Program. 69:443–448 (1995). DOI 10.1007/BF01585570 | Crossref metadata |
| T4-18 | D. Bulger, W. P. Baritompa, G. R. Wood, "Implementing pure adaptive search with Grover's quantum algorithm," J. Optim. Theory Appl. 116:517–529 (2003). DOI 10.1023/A:1023061218864 | Crossref metadata |
| T4-19 | W. P. Baritompa, D. W. Bulger, G. R. Wood, "Grover's quantum algorithm applied to global optimization," SIAM J. Optim. 15:1170–1184 (2005). DOI 10.1137/040605072 | Crossref metadata + abstract ("a framework called Grover adaptive search … A method of Dürr and Hoyer and one introduced by the authors fit into this framework") |
| T4-20 | D. Bulger, "Quantum basin hopping with gradient-based local optimisation," arXiv quant-ph/0507193 (2005) | arXiv abstract ("effort proportional to the square root of the number of basins"; "Jordan's quantum gradient estimation method … extra acceleration proportional to the domain dimension") |
| T4-21 | A. W. Senior et al., "Improved protein structure prediction using potentials from deep learning," Nature 577:706–710 (2020). DOI 10.1038/s41586-019-1923-7 | Crossref metadata + Europe PMC abstract ("the resulting potential can be optimized by a simple gradient descent algorithm to generate structures without complex sampling procedures"). The body (restart and noise details) was not read |

### 5.3 Not verified, not used as evidence
- The explicit constant 22.5√N often quoted for [C56]. No constant from [C56] is used.
- The cheap-gradient principle of reverse-mode differentiation (Baur–Strassen / Griewank). Used only as a standard remark (INFERENCE).
- The QROAM select-swap constant of [T4-7] (asymptotic only).
- Jordan's original gradient algorithm (2005). Known here only through [T4-8] and [T4-20]'s abstracts.
- The body of [T4-15] (VTAA cost), of [T4-9] (buffer construction) and of [T4-21] (restart procedure).

---

## 6. Scope and what is NOT claimed

- **Not claimed:** that finding the argmin of the learned energy is useful for accuracy.
  - S33 found restart saturation at 44–60 aa, with ≤ 0.14 Å headroom above the information floor (R10, `sprint29-33/README.md`). That figure is **PILOT: 6 dev targets**, and nothing was measured beyond 60 aa.
  - The surviving program lead is posterior *sampling* (T2), not mode finding.
  - This note answers the computational question only: cost to reach the lowest energy level under the stated model.
- **Not claimed:** exact Toffoli counts. §3.7 is a labelled order-of-magnitude model. T* ∝ (K_eff·ρ·C_step)². The level is therefore L3 *provisional*. The 170 µs conclusion holds unless the one-evaluation cost is overestimated by more than ~90× (nominal) or ~5.6× (T3-generous costs with measured timing). The 1 µs conclusion holds unless the coherent relaxation is overestimated by more than ~10² (M-LB2, S = 1, nominal).
- **Not claimed:** any lower bound against *structured* quantum algorithms. That includes A built from walks, QSA, phase estimation or other interference, and quantum algorithms using the energy's white-box form. S2, S3 and S11(a) are statements about amplifying a *restart map*. Super-quadratic routes are T5's subject.
- **Not claimed:** a query separation for the actual problem. The quadratic saving is relative to i.i.d. restarts. No lower bound against adaptive classical search is claimed.
- **Not claimed:** that p(L) is measured at L ≥ 60. The census is PILOT, R = 256 censors the tail, the best endpoint may not be the global minimum, and the census map is truncated.
- **Not claimed:** that A-map (p_Q = p_C) holds. §4.6 shows it can fail in both directions.
- **Not claimed:** hardware predictions. 170 µs / 1 µs / 1 ns are scenarios. No quantum simulation or hardware run was performed. Simulator ≠ hardware and query ≠ runtime.
- **Leakage:** no native structure was read by any check (DEP only). The census and C8 clusterings are endpoint-to-endpoint.

---

## 7. Open gaps

| # | Gap | Why it matters | Next step |
|---|---|---|---|
| G1 | T3's revised Toffoli count G(L) for the actual A80 gradient (T3's script is under revision; T4 uses frozen T3 v1 formulas) | Rescales p* ∝ G⁻² and T* ∝ G²; does not touch the 170 µs floor verdict unless C_E falls ≥ 5.6× below T3-generous | T3; re-run C6 on integration |
| G2 | p_Q for the exact b-bit coherent maps (slot-compiled L-BFGS at b ∈ {20, 24, 32}; M-HB with a buffer) vs p_C of float64 L-BFGS | A-map is UNPROVEN; §4.6 shows the map changes p; b = 20 may be numerically unstable for L-BFGS curvature pairs | Classical emulation of the b-bit maps on the C8 crops (cheap) |
| G3 | The energy-level mass p(Δ) at L ≥ 60, and whether the census best is the global minimum | Censored at 1/R in 88–100% of crops; only p decides gate I | ≫ 256 converged restarts on a few crops (e.g. the planned 2,048-restart census, run to convergence); compare with PT/NRPT minima (T5 §4.3) |
| G4 | Best classical portfolio TTT_C(L): basin hopping, PT, SMC, learned proposals, **distogram/MDS-initialised L-BFGS and AlphaFold-style gradient descent with noisy restarts [T4-21]** | Gate I uses the best classical method, not naive restarts | Part of G1's classical-twin portfolio |
| G5 | Constants and polylogs of VTAA [T4-15] at K ~ 10³ | Could recover at most the slot penalty (1.25–3.2×, §4.2a), and not on the target branches, which are the long ones | Theory, short (read [T4-15] body) |
| G6 | Surface-code decoding and classical co-processing cost [C63] | Ignored (favours quantum) | T3 |
| G7 | **CLOSED (v2).** Explicit c_QS: ≤ 4.5 from [T4-6, Thm 3 proof]; ≥ π/4 (S2); [T4-14] "C ≈ 25" for the full minimum finder | — | — |
| G8 | Transmission: does the lowest-energy level matter for accuracy beyond 60 aa (H-004)? | If not, the task itself is irrelevant, whatever its cost | G1 transmission arm |
| G9 | Integration: add [T4-1]–[T4-21] to `BIBLIOGRAPHY.md`; record this note in KILLBOOK / OPPORTUNITY_MATRIX M9 as "KILLED (170 µs map-independent; 1 µs under named assumptions)"; note that S3 is prior art ([T4-14], PAS/GAS) | Housekeeping | Integrator |
| G10 | The L0–L6 scale is taken from T2's working table; the program should define it centrally | Consistency | Integrator |
| G11 | C8 was completed on 16 of the 21 pre-registered crops; 3TE4A_60, 4LPQA_60, 3TE4A_80, 4LPQA_80 and 4LPQA_45 are open (deviation logged in the pre-registration); one classical t_C source measured on an idle machine for T3 and T4 | Completes the convergence picture; removes the 2–6× spread between A-C1 and the loaded-machine timings | Rerun `--converge` on the remaining crops; idle-machine timing |

**What would reopen AA-2** (INFERENCE). All of the following together:
1. Logical Toffoli throughput ≳ 10⁷–3×10¹⁰ per second, i.e. t_Tof ≲ 0.037–150 ns depending on the map, L, S and the gate costs (§4.7). That is ≥ 10³ times the T3 baseline even in the most favourable combination.
2. A protein class and length where the *measured* energy-level mass satisfies (c·t_Q/W_max)² ≤ p_Q < p*(L, t_Tof) at the same (L, t_Tof), for a coherent map that actually converges.
3. A realisable unknown-threshold constant well below BBHT's, or a reason why the threshold is known in advance.
4. Evidence that no adaptive, initialised or learned classical method reaches the target at TTT_C below c·t_Q/√p_Q.

None of the four is in view. If (2) held while (4) failed, the classical method is the answer.

---

## Response to review

No objection was rejected outright. Four were accepted with a qualification.

- **R2-1 (truncated map).** Accepted and acted on (C8). Two qualifications:
  - The reviewer expected converged budgets to strengthen the kill *everywhere*. At 170 µs the kill does not depend on K_eff at all, because of the one-evaluation floor (S9). Convergence matters only for the 1 µs verdict, where it does strengthen it.
  - Converging does not by itself raise the cost much: the q90 of converged evaluation counts (≈ 420–470 at L = 60–100) is close to v1's 400. The kill is strengthened because the *target* restarts need tail budgets (up to 1,040 evaluations), not because typical restarts do.
- **R2-2 (predicate) and R1-4 (censoring).** Accepted. The wording "the census only bounds p at ≤ 1/256" (R2-2) is not used. As R1-4 notes, a single hit does not bound p from above; the note gives p̂ = 1/R with its Clopper–Pearson interval.
- **R2-6 / R1-12 ("rerun §4.5a against T3's final functions").** Accepted against T3's final **v1** note. T3's script is being revised concurrently and does not currently run. T4 therefore freezes T3 v1's documented formulas instead of importing a moving target, and G1 records the re-run needed on integration.
- **R2-10 ("use one t_C source measured on an idle machine").** One source (T3's `--timing`) is now used for every measured-timing row in T3 and T4. No idle machine was available during this revision (the machine ran at ~100% CPU from other lanes' jobs), so the idle-machine measurement is open (G11). A-C1 remains the nominal source because it is the fastest classical figure, which is conservative for a kill.

---

## Review log

Two skeptics reviewed v1 (both verdicts: FIXABLE). R1-n and R2-n number their objections in the order given. All numbers in the resolutions come from the companion script (checks C2–C8) unless stated.

| # | Location (v1) | Objection (short) | Severity | Resolution in v2 |
|---|---|---|---|---|
| R1-1 | §0 6, S12, §7 | Gates H and I checked at different (L, t_Tof); p ≤ 10⁻⁷ applies only at 1 ns | medium | **Fixed.** Gates stated at matched (L, t_Tof); p*(L, t_Tof) = t_C/(S·T*) ∝ t_Tof⁻²; window width (W_max/T*)², a point at the threshold (S9, S12, §4.7). The extrapolated crossings are withdrawn. For the record, the reviewer's matched-L recomputation of the withdrawn v1 statement (nominal costs: gate H needs t_Tof ≤ 1.06 ns at L = 500 and ≤ 1.37 ns at L = 380; T3-generous ≤ 6.3 ns at L = 390 and ≤ 8.2 ns at L = 300; at 1 ns and L = 500 the window is [1.19, 1.48]×10⁻⁷ with the extrapolated median just below it) was checked with the v1 model (1.06 ns at L = 500, 1.37 ns at L = 380 and the 1 ns window at L = 500 reproduced) and is correct |
| R1-2 | §0 6, S12 | "≥ 7×10⁸ at every L ≥ 30" is the L = 60 value; L = 30 gives 3.1×10⁸ | low | **Fixed.** All margins restated per L (§0, S12, §4.5, §4.5a) |
| R1-3 | §0 first bullet | "p ≲ 10⁻¹⁸, ≳ 10⁹ yr" does not match computed values | low | **Fixed.** Replaced by the per-L table in §0 item 4 (p* = 1.5–4.1×10⁻¹⁸, T* = 3.1×10⁸–2.9×10⁹ yr for M-LB2) and the floor values |
| R1-4 | §0 5, §4.2 | "p ≤ 1/256 (censored)" and "≤ 12× at the floor" are statistically wrong | low | **Fixed.** Single-hit crops: p̂ = 1/256, CP 95% [1.0×10⁻⁴, 2.2×10⁻²], global level possibly unobserved; saving 11.6× *at* p = 1/256 and unbounded by the data (§4.2b–c) |
| R1-5 | S11(a), §3.11 | "Every coherent A is a classical reversible circuit" is false | medium | **Fixed.** Restricted to restart maps A = U_Φ(U_P ⊗ I); other A (walks, QPE, nested QSA+AA) explicitly out of scope → T2/T5 (S11a, §3.11, §6) |
| R1-6 | §0 3, S7, §4.5a | "0.4–2×" inaccurate | low | **Fixed.** 0.13–2.2× (D2 generous to D1), 0.3–0.5× D2 central; the §4.5a factor statement is qualified to L ≥ 60, with the L = 30 values given (S7, §4.5a) |
| R1-7 | §0 5 | R ~ 4×10⁹ mixes maps | low | **Fixed.** R stated per map in §4.5 (M-LB2 3.6–5.8×10⁸ at 170 µs); the mixed sentence is removed |
| R1-8 | S8, S10 | qubit arithmetic slips | low | **Fixed.** 0.9–2.3×10⁵; 1.75×10⁶; "2×10⁸–5×10⁹ physical" (S8, S10, §3.8) |
| R1-9 | S3, §4.3, §4.5 | Strict inequality needs c_QS > 1/2; c_QS ≥ 1 unjustified | low | **Fixed.** Condition stated; c_QS ≥ π/4 derived from [T4-5] (S2, §3.2), so it holds. "c_QS ≥ 1" and the c_QS = 1 "upper bound" reading are withdrawn; c_QS ≤ 4.5 from BBHT closes G7 |
| R1-10 | S9, §3.9 | L-scaling is conditional on A-C1 | low | **Fixed.** Tagged "DERIVED under A-C1"; O(L) kernel gives R ∝ L, p* ∝ L⁻², T* ∝ L³ (S9, §3.9) |
| R1-11 | A-C1 vs §4.1 | A-C1 is 2–3× faster than measured; thresholds should show both | low | **Fixed.** Every gate-H threshold and margin is given for both t_g sources (§4.5a, §4.7); relaxation factor 1.4–2.4× stated |
| R1-12 | claim levels | "L3 derived" overstated | low | **Fixed.** "L2 relative to the i.i.d.-restart model; L3 provisional (INFERENCE-grade constants)" (§0, statement table, §6) |
| R1-13 | M-GD, §4.6 | "K ≫ 10⁴" contradicts data | low | **Fixed.** "K ≳ 10⁴ (≥ ~50× L-BFGS evaluations), at the edge of stability" (§2.2, §4.6) |
| R1-14 | §3.7 | per-pair linear tally 10b vs 12b | low | **Fixed.** Formula and script use 10b (c_pair 6.11 → 6.08×10⁴; no rounded number changes except C_step(150) 8.2 → 8.1×10⁸) |
| R1-15 | §0 2(a), S4 | S4 does not prove x₀ must be kept; the H_min factor is not derived | low | **Fixed** (with R2-9): S4 reduced to a space remark; the H_min floor is dropped (S4, §3.4) |
| R1-16 | S8 factories | factory count is necessary, not sufficient | low | **Fixed.** Qualified, plus [B46]'s 10–100× range (S8) |
| R1-17 | §2.5 | "~6×10³ by dirty-qubit trade-off" not derivable | low | **Fixed.** Dropped; unary 1.3×10⁵ kept ([A60] now verified by T3) (§2.5) |
| R1-18 | §2.2, S6, §4.4 | Armijo trials could be energy-only | low | **Fixed.** Sensitivity stated (≤ 1.44× for M-LB2, ≤ 5.8× for M-LB12); moot under slot compilation (§2.2) |
| R1-19 | §4.6, §3.6 | 16 vs 64 starts; minimum/percentiles not in C7 output | low | **Fixed.** Start counts per row; diverging-GD checkpoints corrected to K = 200/1,000/5,000 (v1's table said 500/2,000/10,000); C7 now prints minimum and percentiles; scratch scripts, logs and JSON preserved in `research/results/RAW/t4_checks/` (§4.6) |
| R2-1 | all pilot numbers | 200-iteration cap binds; basins, p_hit, K_C, gaps are cap artefacts | high | **Fixed.** Pre-registered check C8 (16 of 21 crops) quantifies the cap (§4.2a); every census number relabelled as a property of Φ₂₀₀; crossings withdrawn. Converged maps added: M-CONV (pre-registered q90 budget) and M-CONVx (maximum budget), which is the task map because the target restarts sit at the 95th–100th percentile of evaluation counts (post-hoc choice, logged in the pre-registration). K_C for Φ_conv is the C8 mean. Against M-LB2 the converged task map raises T* 6–7× at L = 60–100, and against M-SLOT2 22–27× |
| R2-2 | §2.2, S3, §4.2–4.3 | marked set (energy) ≠ measured p_hit (RMSD cluster) | high | **Fixed.** p redefined as the energy-level mass (§0, §2.2); census energy-level masses (§4.2b) and C8 per-restart levels (§4.3) are primary; RMSD clusters are diagnostic only (§4.2c); censoring at L ≥ 60 stated |
| R2-3 | S3, §3.3, §5 | S3 is prior art (vAGGdW App. C; PAS; GAS; quantum basin hopping) | high | **Fixed.** Retagged THEORETICAL [T4-14, Lemmas 47–48, Thm 49]; [T4-16]–[T4-20] added and verified; §3.3 kept only as a re-derivation; Bulger's Jordan-gradient claim answered (§3.7) |
| R2-4 | S2, G7, §4.3, §0 5 | 1.38 is BBHT's; c_QS ≈ 4.5 closes G7; realisable column | medium | **Fixed.** 1.38 tagged THEORETICAL [T4-6 §3] (PDF text checked); G7 closed; realisable columns in §4.3; the c sensitivity row (×34) in §4.5b; §0 item 5 restated |
| R2-5 | S11(a) | same as R1-5 | medium | **Fixed** (see R1-5) |
| R2-6 | §0, S2, S9 | L2 "real" overstated; L3 overstated; §2.4/§4.5a stale wording | medium | **Fixed.** L2 relative to i.i.d. restarts; L3 provisional; §2.4/§4.5a rewritten against T3 v1 with a frozen snapshot (see Response to review) |
| R2-7 | S6, §3.6 | 11.5× is a naive unroll; slot compilation gives ~1.25×; VTAA reference wrong | medium | **Fixed.** Slot compilation (S6, §3.6); 11.5× withdrawn; VTAA cited as [T4-15] (arXiv 1010.4458); G5 reworded |
| R2-8 | S4 | S4 is not a time cost; premise fails for the measured map | low | **Fixed.** Removed from the cost list; space remark citing [T4-1] |
| R2-9 | §0, S12 | margins inconsistent; ns thresholds cover L = 60–150 only | low | **Fixed.** Per-L margins and thresholds including L = 30 (§0, S12, §4.7) |
| R2-10 | §6, S7, A-C1, S8 | quantum-favourable choices never stacked; t_C sources differ; factories beyond [B46] | low | **Fixed.** Worst-case row (§4.5b: 12 yr / 3.8 yr at L = 30, 1 µs); the assumptions carrying the 1 µs kill are named; one measured t_C source; factories qualified (S8). Idle-machine timing open (G11) |
| R2-11 | S9, S12 | gate H must be the minimum over task-solving maps | low | **Fixed.** Floor over maps T* ≥ T*₁ (S9, §3.9): makes the 170 µs kill map-independent; at 1 µs the converged budgets from C8 are used and the dependence on K_eff is stated |
| R2-12 | S11(c), G4 | Senior et al. 2020 missing; MDS/distogram initialisation | low | **Fixed.** [T4-21] cited (abstract verified); added to S11(c) and G4; body details marked unread |
| R2-13 | A-T1, G2 | 20-bit precision optimistic for coherent L-BFGS | low | **Fixed.** Precision estimate in A-T1; b ∈ {20, 24, 32} in G2; b = 32 gives ×1.9–2.0 in C_step |
| R2-14 | §0 7, §6 | 0.14 Å headroom rests on 6 dev targets | low | **Fixed.** Marked PILOT (6 dev targets; nothing beyond 60 aa) in §0 and §6 |

---

## Appendix: check output (`python research/theory/PROOFS/T4_amplified_checks.py`, 2026-09-27, one core)

Default checks, census snapshot {30: 16, 45: 16, 60: 16, 80: 16, 100: 16, 120: 7}; excerpt:
```
C1 DP vs brute force (n<=8, s<=4): OK
C1 max K reachable with s pebbles: clean F: [1, 2, 4, 8, 16, 32]  garbage-allowed G: [1, 3, 7, 15, 31, 63]
C1 K=  256: time overhead G(K,s)/K  s=9:5.44  s=12:3.34  s=16:2.88  s=20:2.28  s=24:1.91  s=32:1.88  s=40:1.84
C1 K=  400: time overhead G(K,s)/K  s=9:8.39  s=12:4.38  s=16:3.28  s=20:2.90  s=24:2.44  s=32:1.92  s=40:1.90
C1 K= 1024: time overhead G(K,s)/K  s=11:9.62  s=12:7.32  s=16:4.82  s=20:3.57  s=24:3.39  s=32:2.94  s=40:2.36
C1 K= 2400: time overhead G(K,s)/K  s=12:14.36  s=16:6.64  s=20:5.44  s=24:3.80  s=32:3.55  s=40:3.30
C1 K= 4096: time overhead G(K,s)/K  s=13:16.54  s=16:9.38  s=20:6.50  s=24:5.47  s=32:3.73  s=40:3.59
C2 known p, repeated fixed-m runs: expected A-applications * sqrt(p) -> min phi/sin^2 phi = 1.3801 at phi = 1.1656 (tan phi = 2 phi); single long run: pi/2 = 1.5708  [= BBHT sec. 3: 2 x 0.69003 iterations]
C2 lower bound, any strategy, p=0.01: E[N_A]*sqrt(p) >= 0.884 (limit pi/4 = 0.785)
C2 lower bound, any strategy, p=0.0001: E[N_A]*sqrt(p) >= 0.795 (limit pi/4 = 0.785)
C2 lower bound, any strategy, p=1e-06: E[N_A]*sqrt(p) >= 0.786 (limit pi/4 = 0.785)
C2 unknown p (BBHT Thm 3 proof, lambda=6/5): <= (9/2) m0 Grover iterations, m0 = 1/sin(2 theta) ~ 1/(2 sqrt p) -> c_QS <= 2 x 9/4 = 4.5 A-applications per 1/sqrt(p) (+ one A per round), t << N
census snapshot: {30: 16, 45: 16, 60: 16, 80: 16, 100: 16, 120: 7}
C3 record-process lemma P(visit j)=w_j/W_j, Monte Carlo n=200000: max abs error 0.0018
C3 L= 30: median E[N_A]/c_QS   4.6  median classical 1/w1   8.5  E[N_A]*sqrt(w1)/c_QS median 1.56 max 1.77 (bound 2)
C3 L= 60: median E[N_A]/c_QS   7.8  median classical 1/w1  20.8  E[N_A]*sqrt(w1)/c_QS median 1.65 max 1.80 (bound 2)
C4 L= 30 crops=16 R=256: p_hit median 0.117 q25 0.0723 min 0.0039 censored(<=1/R) 0.06 | modes median 82 | grad evals/restart mean 174 max 202
C4 L= 30 energy-level p(dE) [200-it map]: dE=1: median 0.0078 q25 0.0039 single-hit 0.44 | dE=5: median 0.0195 q25 0.0137 single-hit 0.12 | dE=20: median 0.2441 q25 0.1885 single-hit 0.00
C4 L= 60 crops=16 R=256: p_hit median 0.049 q25 0.0127 min 0.0039 censored(<=1/R) 0.25 | modes median 150 | grad evals/restart mean 203 max 211
C4 L= 60 energy-level p(dE) [200-it map]: dE=1: median 0.0039 q25 0.0039 single-hit 0.88 | dE=5: median 0.0039 q25 0.0039 single-hit 0.56 | dE=20: median 0.0117 q25 0.0078 single-hit 0.00
C4 single hit in R=256: p-hat = 0.0039, Clopper-Pearson 95% [9.9e-05, 2.2e-02]
C4 slope d ln p_hit / dL: pooled (all L) -0.0263; per-protein over L=[30, 45, 60, 80, 100] (16 proteins) median -0.0295 IQR [-0.0395, -0.0078] (censoring at 1/R biases toward 0)
C5 L=100: C_step nominal 3.89e+08 | b=16 3.08e+08 | b=24 4.88e+08 | aggressive 1.93e+08 Toffolis; pair share 0.74
C6 c=1.3801 (known p; floor pi/4, unknown threshold ~1.8x4.5); t_C = K_C x t_g(A-C1); A-application Toffolis = (gradient-equivalents incl. pebbling) x C_step(L)
C6 C8 converged budgets per L (median q90 / max / mean evals per restart): {30: (257, 440, 175), 45: (370, 755, 243), 60: (453, 835, 270), 80: (424, 816, 298), 100: (468, 1023, 347), 120: (523, 1040, 370)}
C6 M-LB2   L=100 K_eff*rho=    976 t_Tof=170us: t_C=0.167s t_Q=6.46e+07s R=3.9e+08 | S=1: p*=3.5e-18 T*=1.5e+09yr | S=1000: p*=3.5e-24 T*=1.5e+12yr
C6 M-LB2   L=100 K_eff*rho=    976 t_Tof=1ns  : t_C=0.167s t_Q=3.80e+02s R=2.3e+03 | S=1: p*=1.0e-07 T*=5.2e-02yr | S=1000: p*=1.0e-13 T*=5.2e+01yr
C6 M-CONVx L=100 K_eff*rho=   3468 t_Tof=170us: t_C=0.278s t_Q=2.29e+08s R=8.3e+08 | S=1: p*=7.7e-19 T*=1.1e+10yr | S=1000: p*=7.7e-25 T*=1.1e+13yr
C6 M-CONVx L=100 K_eff*rho=   3468 t_Tof=1us  : t_C=0.278s t_Q=1.35e+06s R=4.9e+06 | S=1: p*=2.2e-14 T*=4.0e+05yr | S=1000: p*=2.2e-20 T*=4.0e+08yr
C6 FLOOR-E L= 30 K_eff*rho= 0.3333 t_Tof=170us: t_C=7.2e-05s t_Q=3.00e+03s R=4.2e+07 | S=1: p*=3.0e-16 T*=7.6e+03yr | S=1000: p*=3.0e-22 T*=7.6e+06yr
C6 T*[yr] S=1 L=30/60/100/150 M-LB2   nominal t_g=A-C1: 170us: 3.1e+08 / 7.1e+08 / 1.5e+09 / 2.9e+09 | 1us: 1.1e+04 / 2.5e+04 / 5.2e+04 / 1.0e+05
C6 T*[yr] S=1 L=30/60/100/150 M-LB2   nominal t_g=meas: 170us: 7.7e+07 / 1.5e+08 / 4.1e+08 / 9.6e+08 | 1us: 2.7e+03 / 5.1e+03 / 1.4e+04 / 3.3e+04
C6 T*[yr] S=1 L=30/60/100/150 M-LB2   T3-D2g  t_g=A-C1: 170us: 5.1e+06 / 1.9e+07 / 5.0e+07 / 1.1e+08 | 1us: 1.8e+02 / 6.5e+02 / 1.7e+03 / 3.8e+03
C6 T*[yr] S=1 L=30/60/100/150 M-LB2   T3-D2g  t_g=meas: 170us: 1.3e+06 / 3.9e+06 / 1.4e+07 / 3.7e+07 | 1us: 4.4e+01 / 1.3e+02 / 4.7e+02 / 1.3e+03
C6 T*[yr] S=1 L=30/60/100/150 M-CONVx nominal t_g=A-C1: 170us: 5.0e+08 / 4.3e+09 / 1.1e+10 / 2.2e+10 | 1us: 1.7e+04 / 1.5e+05 / 4.0e+05 / 7.5e+05
C6 T*[yr] S=1 L=30/60/100/150 M-CONVx nominal t_g=meas: 170us: 1.2e+08 / 8.8e+08 / 3.1e+09 / 7.1e+09 | 1us: 4.3e+03 / 3.0e+04 / 1.1e+05 / 2.5e+05
C6 T*[yr] S=1 L=30/60/100/150 M-CONVx T3-D2g  t_g=A-C1: 170us: 8.3e+06 / 1.1e+08 / 3.8e+08 / 8.2e+08 | 1us: 2.9e+02 / 3.9e+03 / 1.3e+04 / 2.8e+04
C6 T*[yr] S=1 L=30/60/100/150 M-CONVx T3-D2g  t_g=meas: 170us: 2.1e+06 / 2.3e+07 / 1.0e+08 / 2.7e+08 | 1us: 7.2e+01 / 8.0e+02 / 3.6e+03 / 9.4e+03
C6 T*[yr] S=1 L=30/60/100/150 FLOOR-E nominal t_g=A-C1: 170us: 7.6e+03 / 1.7e+04 / 3.7e+04 / 7.1e+04 | 1us: 2.6e-01 / 6.0e-01 / 1.3e+00 / 2.5e+00
C6 T*[yr] S=1 L=30/60/100/150 FLOOR-E nominal t_g=meas: 170us: 1.9e+03 / 3.6e+03 / 1.0e+04 / 2.3e+04 | 1us: 6.5e-02 / 1.2e-01 / 3.5e-01 / 8.1e-01
C6 T*[yr] S=1 L=30/60/100/150 FLOOR-E T3-D2g  t_g=A-C1: 170us: 1.3e+02 / 4.6e+02 / 1.2e+03 / 2.7e+03 | 1us: 4.3e-03 / 1.6e-02 / 4.2e-02 / 9.4e-02
C6 T*[yr] S=1 L=30/60/100/150 FLOOR-E T3-D2g  t_g=meas: 170us: 3.1e+01 / 9.5e+01 / 3.3e+02 / 8.9e+02 | 1us: 1.1e-03 / 3.3e-03 / 1.2e-02 / 3.1e-02
C6 3*C_E(T3-D1)/C_step(nominal) at L=30/60/100/150: 1.20 / 1.69 / 1.99 / 2.18
C6 3*C_E(T3-D2c)/C_step(nominal) at L=30/60/100/150: 0.29 / 0.38 / 0.44 / 0.48
C6 3*C_E(T3-D2g)/C_step(nominal) at L=30/60/100/150: 0.13 / 0.16 / 0.18 / 0.20
C6 gate H (T*<=1yr) M-LB2   nominal t_g=A-C1 S=1: t_Tof <= 9.66ns / 6.37ns / 4.38ns / 3.15ns at L=30/60/100/150
C6 gate H (T*<=1yr) M-LB2   nominal t_g=A-C1 S=1000: t_Tof <= 0.305ns / 0.202ns / 0.139ns / 0.0997ns at L=30/60/100/150
C6 gate H (T*<=1yr) M-CONVx T3-D2g  t_g=meas S=1: t_Tof <= 118ns / 35.2ns / 16.7ns / 10.3ns at L=30/60/100/150
C6 gate H (T*<=1yr) M-CONVx T3-D2g  t_g=meas S=1000: t_Tof <= 3.74ns / 1.11ns / 0.527ns / 0.326ns at L=30/60/100/150
C6 window 1ns S=1 W=1yr M-LB2   L=100: p in [2.8e-10, 1.0e-07]; width factor (W/T*)^2 = 3.7e+02
C6 window 1ns S=1 W=1yr M-CONVx L=100: p in [3.5e-09, 2.2e-08]; width factor (W/T*)^2 = 6.4e+00
C6 window 1ns S=1 W=1yr M-CONVx L=150: p in [1.6e-08, 2.8e-08]; width factor (W/T*)^2 = 1.8e+00
C6 worst case L=30 (T3-D2g, t_g measured, s=40 rho=1.85, K_eff=270, c=1.38), 1us: T* = 11.6 yr, p* = 1.7e-10; 170us: 3.36e+05 yr
C6 worst case L=30 (T3-D2g, t_g measured, s=40 rho=1.85, K_eff=270, c=pi/4), 1us: T* = 3.8 yr, p* = 5.1e-10; 170us: 1.09e+05 yr
C6 worst case, converged task map L=30 (M-CONVx K_eff=440, s=40 rho=1.91, T3-D2g, t_g measured, c=1.38), 1us: T* = 39.2 yr, p* = 4.1e-11
C6 worst case, converged task map L=30 (M-CONVx K_eff=440, s=40 rho=1.91, T3-D2g, t_g measured, c=pi/4), 1us: T* = 12.7 yr, p* = 1.3e-10
C6 convergence factor L=30: T*(M-CONVx)/T*(M-SLOT2) = 5.8
C6 worst case L=60 (T3-D2g, t_g measured, s=40 rho=1.85, K_eff=270, c=1.38), 1us: T* = 35.2 yr, p* = 2.6e-10; 170us: 1.02e+06 yr
C6 worst case L=60 (T3-D2g, t_g measured, s=40 rho=1.85, K_eff=270, c=pi/4), 1us: T* = 11.4 yr, p* = 8.1e-10; 170us: 3.30e+05 yr
C6 worst case, converged task map L=60 (M-CONVx K_eff=835, s=40 rho=1.99, T3-D2g, t_g measured, c=1.38), 1us: T* = 300.7 yr, p* = 4.0e-11
C6 worst case, converged task map L=60 (M-CONVx K_eff=835, s=40 rho=1.99, T3-D2g, t_g measured, c=pi/4), 1us: T* = 97.4 yr, p* = 1.2e-10
C6 convergence factor L=60: T*(M-CONVx)/T*(M-SLOT2) = 21.5
C6 worst case L=100 (T3-D2g, t_g measured, s=40 rho=1.85, K_eff=270, c=1.38), 1us: T* = 124.4 yr, p* = 1.6e-10; 170us: 3.59e+06 yr
C6 worst case L=100 (T3-D2g, t_g measured, s=40 rho=1.85, K_eff=270, c=pi/4), 1us: T* = 40.3 yr, p* = 4.8e-10; 170us: 1.16e+06 yr
C6 worst case, converged task map L=100 (M-CONVx K_eff=1023, s=40 rho=2.36, T3-D2g, t_g measured, c=1.38), 1us: T* = 1741.6 yr, p* = 1.9e-11
C6 worst case, converged task map L=100 (M-CONVx K_eff=1023, s=40 rho=2.36, T3-D2g, t_g measured, c=pi/4), 1us: T* = 564.0 yr, p* = 5.7e-11
C6 convergence factor L=100: T*(M-CONVx)/T*(M-SLOT2) = 27.2
C6 c = pi/4 (floor): T* x 0.32 relative to c = 1.38
C6 c = 1.38 (known p): T* x 1.00 relative to c = 1.38
C6 c = 8.1 (record, BBHT): T* x 34.45 relative to c = 1.38
C8 L= 30 calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = 128; quantum known p and threshold 16 (c=1.38); record process with BBHT c_QS=4.5: 103; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) 1.80
C8 L= 30 (4 crops): capped@200 median 0.21 | capped@max median 0.00 | evals/restart mean-of-means 175, q90 median 257, max 440 | pE1 conv median 0.0078, pE20 conv median 0.2871 | p_rmsd conv median 0.1426 (200: 0.1406)
C8 L= 45 calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = 256; quantum known p and threshold 22 (c=1.38); record process with BBHT c_QS=4.5: 129; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) 1.80
C8 L= 45 (3 crops): capped@200 median 0.43 | capped@max median 0.00 | evals/restart mean-of-means 243, q90 median 370, max 755 | pE1 conv median 0.0039, pE20 conv median 0.0430 | p_rmsd conv median 0.1797 (200: 0.1797)
C8 L= 60 calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = 256; quantum known p and threshold 22 (c=1.38); record process with BBHT c_QS=4.5: 129; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) 1.80
C8 L= 60 (2 crops): capped@200 median 0.41 | capped@max median 0.00 | evals/restart mean-of-means 270, q90 median 453, max 835 | pE1 conv median 0.0039, pE20 conv median 0.0117 | p_rmsd conv median 0.2617 (200: 0.2070)
C8 L= 80 calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = 256; quantum known p and threshold 22 (c=1.38); record process with BBHT c_QS=4.5: 129; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) 1.80
C8 L= 80 (2 crops): capped@200 median 0.67 | capped@max median 0.00 | evals/restart mean-of-means 298, q90 median 424, max 816 | pE1 conv median 0.0039, pE20 conv median 0.0039 | p_rmsd conv median 0.2656 (200: 0.1445)
C8 L=100 calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = 256; quantum known p and threshold 22 (c=1.38); record process with BBHT c_QS=4.5: 129; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) 1.80
C8 L=100 (4 crops): capped@200 median 0.83 | capped@max median 0.00 | evals/restart mean-of-means 347, q90 median 468, max 1023 | pE1 conv median 0.0039, pE20 conv median 0.0039 | p_rmsd conv median 0.0645 (200: 0.0195)
C8 L=120 calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = 256; quantum known p and threshold 22 (c=1.38); record process with BBHT c_QS=4.5: 129; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) 1.80
C8 L=120 (1 crops): capped@200 median 0.87 | capped@max median 0.00 | evals/restart mean-of-means 370, q90 median 523, max 1040 | pE1 conv median 0.0039, pE20 conv median 0.0078 | p_rmsd conv median 0.0352 (200: 0.0039)
```
Energy checks (`--energy`, run 00:12–00:30 on a machine at ~84% load, v1 session; the C7 printout now also gives min and percentiles, taken here from the preserved 64-start scratch JSON):
```
C7 L-BFGS evals/restart (B=1): mean 209 median 222 min 109 q10 149 q90 237 max 261
C7 Hessian at L-BFGS endpoints: lambda_max median 281, max 8.65e+04; smallest eigenvalue > 1e-3 median 0.495
C7 GD eta=2e-5, K=1e4: same basin as L-BFGS 0.44; median E - E_LBFGS -2.3
C7 clipped GD eta=1e-3 clip=0.02, K=1e4: same basin as L-BFGS 0.00; median E - E_LBFGS 713.3
```
Later census snapshots and further C8 crops will change the C4/C8 rows.
