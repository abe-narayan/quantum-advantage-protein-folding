# T1: the generalised H-001 reduction theorem

_Written 2026-09-26; **revised 2026-09-27** after two skeptic reviews (§9 answers the points not accepted in full; §10 logs every objection and its resolution). Roadmap item `research/THEORY_ROADMAP.md` T1; hypotheses H-001 and H-009 (`research/HYPOTHESES.md`); opportunity-matrix row G4 (`research/literature/OPPORTUNITY_MATRIX.md`). No experiment was run for this note. The numerical checks are in `T1_reduction_checks.py` in this directory: about a minute on one core, reading the G1 census files read-only. Citation keys resolve in `research/literature/BIBLIOGRAPHY.md`. Keys [T1-n] are papers verified on arXiv on 2026-09-27 and not yet in the bibliography (§5.1). S29–S33 pointers (`s30 Q2`, `QX-10`, R1–R12) resolve in `research/sprint29/` … `research/sprint33/` and `research/sprint29-33/`._

## Tags used in this note

| Tag | Meaning |
|---|---|
| **DERIVED** | Proved here. Where a numerical falsifier is cheap, `T1_reduction_checks.py` runs it. |
| **THEORETICAL** | A literature result, cited by key. Its content is as recorded in the verified domain notes or re-read on arXiv (stated where so). |
| **INFERENCE** | A reasoned step that is not a proof: it rests on an unproven premise, an empirical number or an extrapolation. |
| **UNPROVEN** | Stated but not established. |
| **EVIDENCE** | A measured number from S29–S33, the current pilot, or this note's checks, with its source. Pilot numbers are marked **PILOT** (indicative only). |

**Claim status.** The main results are **theoretical**: exact statements inside the model of §2, with worst-case, exact-arithmetic proofs. They are a structural negative, recorded under CLAUDE.md claim category 6 (theoretical/provable advantage) in its **negative (no-go)** form, as H-001 is. **Practical** consequences are in §4 and §6, kept apart and conditional on labelled assumptions.

**Claim levels.** No repository-level file defines the L0–L6 scale (G-10). The sibling notes use a working table (`T2_sampling_speedup_statement.md`, also adopted by `T4_amplified_mode_finding.md`). On that table T1 asserts **no advantage (practical L0)**. The one positive statement it records is the literature's quadratic query speedup for OPT on implicit registers with black-box E [C56]: theoretical **L2** (oracle cost excluded), practical L0.

---

## 0. Result in brief

Suppose a quantum stage is trained on an objective that sees the prepared state only through its computational-basis distribution p, or that only adds a penalty on coherence. Then the best the stage can do is output a distribution that a classical optimiser over the probability simplex also reaches (Theorem 1).

Suppose further that later stages use p only through three channels: its argmin, its energy-order tail, or as the solution of a convex program. Then, at the optimum, the pipeline output is a function of the classical problem specification alone (Theorem 2; for the set readout, when p has full support). The ideal stage therefore contributes no *information* beyond the specification. Its only possible contribution is *computational* (speed), and a classical algorithm computes the same output (Theorem 3):
- in time poly(N) for an **explicit** register of N listed valid states (diagonal E), or poly(d_H) for a non-diagonal Hamiltonian on a densely encoded register of Hilbert dimension d_H;
- for an **implicit** register (N = 2^Θ(n)), at the cost of the classical solver of one of four *specification problems*: OPT(E), TOP_m(E), CVX(Ψ) or SAMPLE(π).

**OPT and TOP_m** are classical optimisation problems. For **black-box** E their quantum query speedup is at most quadratic: for OPT by [C55, C56], and for TOP_m because its first element solves OPT (§1.5). That ceiling does **not** apply to structured E. The A80 energy is an explicit, differentiable, non-convex formula, and for such landscapes Quantum Hamiltonian Descent claims a query-model separation on engineered instances, with only empirical classical hardness [T1-1, T1-2] (§6, B5). **CVX** is polynomial-time classically when its support is of polynomial size (explicit registers, candidate simplices; microseconds to milliseconds at S29–S33 sizes). A general convex objective over an implicit register has no reduction here (§1.5). **SAMPLE(π)** means sampling a distribution specified over an implicit register. **T1 stops at that problem.** It is the surviving lead (matrix rows M1/M2). The proven quantum sampling speedups for it are also at most quadratic and query-model [A44, A45], so the FT break-even of [B46] applies to it too. The pilot's relevant hardness signal is the first-order-like bottleneck with 0 round trips, not the barrier Λ (§4 N4).

The S29–S33 reductions are corollaries of the theorem: the prefix theorem, solver equivalence, tail collapse, the closed-form hinged-Gibbs p*, Born-machine/Gibbs equivalence, the hull projection, dimension counting, the register-relaxation bound, and sparse s-of-K monotonicity.

- **H-001** splits (§7). **H-001a** (output equivalence) is **proved**. **H-001b** (the stage "cannot be load-bearing", i.e. cost equivalence) is proved for explicit registers with a tabulated E. It is **false in the query model** for implicit registers with black-box E [C56], open for structured E, and practically unresolved by T1 alone.
- **H-009**, as worded, is **falsified in both clauses** (§7).

---

## 1. Statements

### 1.1 Definitions (the model is in §2)

- **D1 · Register.** The measured computational basis on n qubits: X = {0,1}ⁿ, with Hilbert dimension **d_H := 2ⁿ**. An encoding enc maps the valid structures into X. **X_valid := enc(structures)** and **N := N_valid := |X_valid|**. Strings outside X_valid carry E = +∞ (or a finite penalty). For diagonal E, N means N_valid below. Every statement that needs the full dimension says d_H.
  - **Explicit:** N ≤ poly(input), X_valid listed. Candidate-index registers are explicit (N = 128 production prefix / 512 harness in S29–S31, dense binary encoding, so d_H = N up to padding).
  - **Implicit:** N = 2^Θ(n), X_valid described by n bits. Subset, mosaic, fragment, contact, (θ,τ)-torsion, macro and lattice-turn registers are implicit (9–171 qubits in S32–S33).
- **D2 · Diagonal cost.** A classical E: X → ℝ ∪ {+∞}, evaluable in time t_E per point. E may call a decoder, for example E_basin(b) = the energy after continuous relaxation from b. H_E = Σ_x E(x)|x⟩⟨x|.
- **D3 · Quantum stage.** Any process that outputs a state ρ_out, followed by measurement in the computational basis. It may use any circuit, depth, ancillas, entanglement, noise, mitigation, initialisation or optimiser. Its only classical output is samples from p_out(x) = ⟨x|ρ_out|x⟩ (or S-shot empirical draws from it).
- **D4 · Dephasing-dominated objective.** The stage minimises J over a state family 𝒮, and J(ρ) ≥ Φ(diag ρ) for every state, with equality on diagonal states, for some Φ: Δ_X → ℝ ∪ {+∞}. The named members:

  | Name | Φ or J | Used in |
  |---|---|---|
  | Φ₁ | ⟨E⟩_p | expectation VQE, QAOA |
  | Φ_α | CVaR_α(E;p) := (1/α)·min{⟨E,λ⟩ : 0 ≤ λ ≤ p, Σλ = α}, α ∈ (0,1] (the Rockafellar–Uryasev / LP form) | CVaR-VQE [C6] |
  | Φ_{α,T} | CVaR_α(E;p) − T·H(p) | the deployed S29–S31 free energy |
  | Φ_T | ⟨E⟩_p − T·H(p) = T·KL(p‖π_T) − T·log Z_T, where π_T ∝ e^{−E/T} | the tempered Born machine (S33 A71) |
  | J_q | tr(H_E ρ) − T·S(ρ), the quantum free energy with von Neumann S | dephasing-dominated by Lemma 1 |
  | any of these + c(ρ) | with a coherence penalty c ≥ 0, c(diag) = 0 | — |

- **D5 · Readouts.** The pipeline output is Y = G(R(p_out), ξ). G is any classical map. It may use side information fixed before the quantum stage and independent randomness ξ. "Consumes p only through R" means this factorisation. The classes:
  - **(a) argmin.** R_a(p) = argmin{E(x) : x ∈ supp p}: the best state in the support. With S shots, the best of S draws.
  - **(b) E-order tail.** **λ*(p)** is the greedy fill of the α-tail in a **fixed stable E-order** (ties broken by a fixed rule; `tail_greedy` in the checks). It is a minimiser in the definition of Φ_α, and the unique one unless several states tie at E = VaR_α(p), where the LP optimum is a face and λ*(p) is its tie-rule vertex. Set form **(b-set)**: R_b(p) = supp λ*(p), for example the uniform average over the tail set (the deployed S29 readout). Weighted form **(b-wt)**: R_b′(p) = λ*(p)/α.
  - **(c) convex program.** The pipeline uses p_out as (an approximation to) w* ∈ argmin_{w∈Δ} Ψ(w), for a convex Ψ with classical data, and emits Y = G(r(w*)). Two sub-cases:
    - **(c1)** Ψ = Φ from D4, and p_out is used as weights or sampled;
    - **(c2)** a weight program over a candidate simplex Δ_K, for example Ψ(w) = ‖Σ w_i U_i − t‖² (S32).
- **Specification problems.** Each is defined by classical data only:

  | Problem | Output |
  |---|---|
  | **OPT(E)** | some x ∈ X_min := argmin E |
  | **TOP_m(E)** | the m lowest-E states, under the fixed tie rule |
  | **CVX(Ψ)** | w* to accuracy ε (polynomial when the support is explicit) |
  | **SAMPLE(π)** | draws from a distribution π specified by E over an implicit register (π_T, the hinged Gibbs law p*_{α,T}, or the uniform law on a sublevel set) |

### 1.2 Lemma 1 (dephasing) · DERIVED

For any density matrix ρ with p = diag ρ:

`H(p) − S(ρ) = D(ρ ‖ Δ(ρ)) ≥ 0`

Here Δ is complete dephasing in the computational basis. Equality holds iff ρ is diagonal. Hence J_q(ρ) = Φ_T(p) + T·D(ρ‖Δρ) ≥ Φ_T(p). The same inequality holds for every Schur-concave entropy (Rényi, Tsallis), because diag ρ is majorised by spec ρ (Schur–Horn).

### 1.3 Theorem 1 (objective reduction) · DERIVED

Under D1–D4:
1. {diag ρ : ρ a state} = Δ_X. Hence inf over all states of J = min over Δ_X of Φ. For any family 𝒮 (any ansatz, noise, depth or ancilla count), inf_𝒮 J ≥ min_Δ Φ.
2. If ρ* minimises J over all states, then diag ρ* minimises Φ. Conversely, the diagonal state diag(p*) minimises J whenever p* minimises Φ. So a universal ideal stage emits p_out ∈ argmin_Δ Φ, and a restricted stage has Φ(p_out) ≥ min_Δ Φ. **On its own declared objective, no quantum output beats the classical optimum over the simplex.**
3. The optimal sets are:

   | Objective | argmin over Δ_X |
   |---|---|
   | Φ₁ | {p : p(X_min) = 1} |
   | Φ_α | {p : p(X_min) ≥ α} |
   | Φ_{α,T}, T > 0 | the unique hinged-Gibbs law p*_{α,T} (Corollary 3) |
   | Φ_T | the unique π_T |
   | J_q | the diagonal Gibbs state diag(π_T) |

### 1.4 Theorem 2 (readout reduction: the output is fixed by the specification) · DERIVED

Under D1–D5, with p_out emitted by an ideal stage:
- **(a)** Take J ∈ {Φ₁, Φ_α}. For the exact distribution, every optimal p has R_a(p) ⊆ X_min, and under (b-set) and (b-wt) its tail is supported on X_min (tail collapse). With S shots, R_a ⊆ X_min with probability ≥ 1 − (1 − p(X_min))^S ≥ 1 − (1 − α)^S (for example 7.7% failure at α = 0.05, S = 50). If X_min = {x*}, then Y = G(x*, ξ), the same for every solver that returns x*.
- **(b)** For **any full-support** p_out, optimal or not, the set readout satisfies R_b(p_out) ∈ {P₁, …, P_N}, where P_m is the set of the first m states in the fixed stable E-order. The stage's whole influence on Y is therefore one integer m: **at most log₂ N bits per target**. Without full support, the influence is the pair (supp p_out, m), which can take up to about 2^N values.
- **(b-wt at Φ_{α,T})** On {E < s*}, p*_i ∝ e^{−E_i/(αT)}: a Gibbs law at temperature αT, with total mass P_{p*}(E < s*) ≤ α. The remaining α − P_{p*}(E < s*) of the tail comes from the flat level set {E = s*}, filled under the tie rule. Strict inequality (s* on a kink of the dual) occurs for α in intervals of positive length. Example: E = (0,1,2), α = 0.8, T = 1 gives s* = 1, p* = (0.636, 0.182, 0.182), P(E < s*) = 0.636.
- **(c)** If Ψ has a unique minimiser (for example because an entropy term makes it strictly convex), or r is constant on argmin Ψ, then Y = G(r(w*), ξ).

In every case the ideal stage contributes **no information beyond the specification** (E, α, T, the tie rule and the data of Ψ): the problem determines the output, the solver does not. This is an information statement, not a computational one, since any deterministic algorithm's output is a function of its input. The stage's only possible contribution is computational (speed), and Theorem 3 routes it to OPT, TOP_m, CVX or SAMPLE.

### 1.5 Theorem 3 (classical reproduction cost) · DERIVED unless marked

The ideal output Y is computed classically at these costs:

| Readout / objective | Explicit register (N listed) | Implicit register (N = 2^Θ(n)) |
|---|---|---|
| (a) with Φ₁ or Φ_α | O(N·t_E) | **OPT(E)** |
| (b-set), full-support p | O(N·t_E + N log N) (one sort); all N possible outputs can be enumerated | **TOP_m(E)** for small m: O(m·n) OPT calls (Lemma 3), **conditional on G-3**, and reproducing the tie-rule set exactly needs a lexicographic OPT (otherwise A4: some set of m lowest-E states). For m ∝ αN it is SAMPLE(uniform on a sublevel set), **outside T1** |
| (b-wt) or (c1) with Φ_{α,T} | exact: O(N·t_E + N log N) (sort, then one scan over the gaps and levels, §3.6); or by bisection O(N·t_E + N·log₂(range(E)/(αT·ε))). Invalid strings (E = +∞) enter only as a count | **SAMPLE(p*_{α,T})**, **outside T1** |
| (c1) with Φ_T (Born machine) | O(N·t_E) | **SAMPLE(π_T)**, **outside T1** |
| (c1) with any other convex Φ (e.g. robust or joint CVaR over a predictor ensemble, QX-23) | poly(N, log 1/ε) (convex program over Δ_N, given a polynomial-time value and subgradient oracle for Φ) | **no reduction here**. It includes OPT(E) as the case Φ₁. **Open** (G-15) |
| (c2) convex Ψ on Δ_K | poly(K, d, log 1/ε) (QP; affine case: one linear solve) | same (K is explicit) |
| any Hamiltonian, not only diagonal | eigh, O(d_H³), which **requires d_H = poly(input)** (a dense encoding; Corollary 5) | not covered (B2) |

Two further bounds follow.
- **Lemma 2 (input cost) · DERIVED.** Suppose E on an explicit register is a table computed classically, as in S29–S31, where E = the standardised rank of classical scores. Producing the input to the quantum stage then already costs N·t_E. The reproduction costs N·t_E + C_post, where C_post is the classical post-processing time. So the quantum pipeline cannot be faster than its classical reproduction by more than the dimensionless factor

  `ratio ≤ 1 + C_post / (N·t_E)`.

  - For (a), (b-set), and (b-wt)/(c1) at Φ_{α,T} by the exact method, C_post = O(N log N)·t_cmp, so ratio ≤ 1 + O(t_cmp·log N / t_E). Only for these diagonal readouts, with Õ(N) post-processing, does it follow that there is **no speedup of any size**, not even a quadratic one. Bisection instead gives C_post = O(N·log(range(E)/(αTε)))·t_op.
  - For a non-diagonal H on an explicit register, C_post = O(d_H³)·t_flop, so ratio ≤ 1 + O(d_H²·t_flop / t_E). That gap is polynomial but need not be small.
- **Coherent-oracle bound.** Suppose E is available as a coherent oracle. OPT(E) then takes O(√N) quantum queries [C56] against Θ(N) classical ones for black-box E. Search reduces to minimum finding (E = 0 on marked items, 1 elsewhere), so the Ω(√N) search lower bound [C55] applies: **at most quadratic** (THEORETICAL, with a DERIVED reduction). TOP_m inherits the ceiling. Classically it needs at most N queries. Quantumly it needs Ω(√N), because its first element solves OPT (DERIVED). This bound says nothing about structured E (§6, B5).

### 1.6 Proposition 4 (suboptimality clause)

Let the *actual* output satisfy Φ(p_out) > min_Δ Φ.
1. **DERIVED.** On the declared objective, the classical p* (or X_min) is strictly better. If G(R(p_out)) beats G(R(p*)) downstream, the objective does not certify that gain. It comes from the solver's bias: the ansatz, initialisation, optimiser or noise.
2. **DERIVED, for full-support p_out** (in practice: explicit registers simulated exactly, or sampled with enough shots to cover the support). Under (b-set) that bias is one integer m. The *family* of classical rules choosing m spans every possible output, and in S29 a single target-independent m matched the stage (QX-01). Without full support the bias is the pair (supp p_out, m).
3. **INFERENCE / boundary.** Under (a), (b-wt) and (c), the bias channel is a distribution the objective does not specify. Calling it an advantage needs three things T1 does not supply:
   - a gain under the contract;
   - no classical family that reproduces it at equal tuning (random prior, p* at other (α,T), SA or PT tails);
   - a p_out that is not classically samplable in the operating regime.

   The literature argues against the third on average for noisy or trainable circuits [F35, F37, F91]. Those arguments are average-case, not theorems about a given circuit, and F37 and F91 themselves leave room for advantage (§5). This is where T1 hands over to the literature.

### 1.7 Proposition 5 (approximate extension by concentration) · DERIVED, conditional

For any target π and set B*, TV(π, π|_{B*}) = 1 − π(B*).

If π(B*) ≥ 1 − ε, every readout E_π f with |f| ≤ 1 is reproduced to within 2ε by OPT(E) followed by sampling π restricted to B*. Under that premise SAMPLE(π) reduces to OPT(E) plus a *local* sampling problem.

On a register, B* is a set of register states, for example those whose decode lands in the basin of X_min under a deterministic descent map. For the continuous A80 energy, "basin" is a continuous-space notion, and applying Proposition 5 needs the discretisation named (§4 N4). The premise concerns basin **mass** (free energy), not minimum energy. §4 N3 shows the pilot cannot yet establish it.

### 1.8 Corollaries: the S29–S33 instances

| # | Corollary | Source result | Tag |
|---|---|---|---|
| C1 | **Prefix theorem.** For any V differentiable on Λ_α(p) = {0 ≤ λ ≤ p, Σλ = α}, every KKT point is a prefix of the order induced by ∇V(λ*). For V = ⟨E,λ⟩ the LP optimum is the greedy E-order fill: one sort. **Sufficient condition for one sort:** if V is convex and ∇V at the greedy fill along a fixed order π is non-decreasing along π, that fill is a global minimiser. S30's "iff more than one self-consistent order" criterion is cited, not proved (INFERENCE). | R1; `s30 Q2` (S30 T1). The sorted-sample estimator is eq. (12) of [C6], verified 2026-09-27 (§5) | DERIVED (criterion: INFERENCE) |
| C2 | **Solver equivalence and tail collapse.** min_Δ CVaR_α = min_x E(x) for every α ∈ (0,1]. The optimal set is {p : p(X_min) ≥ α}, and the tail law at any optimum lives on X_min. | Sufficiency ("a state with ground-state probability ρ is a global CVaR_α optimum for any α ≤ ρ") is prior art: [C6] §5, the discussion following Prop. 5.1. The characterisation and tail collapse are R2, R3; `s33 Q-D1, Q-D2` | DERIVED |
| C3 | **Closed-form hinged Gibbs.** Φ_{α,T} is strictly convex. Its minimiser is p*_i ∝ exp((s* − E_i)₊/(αT)), where s* maximises the concave dual g(s) = s − T·log Σ_i exp((s − E_i)₊/(αT)) and satisfies P_{p*}(E < s*) ≤ α ≤ P_{p*}(E ≤ s*), with strict inequality allowed. At α = 1 every s ≥ E_max maximises g, and p* = π_T exactly (Born-machine/Gibbs equivalence). A limit s* → ∞ is needed only if some E = +∞. For α < 1, every state above s*, including invalid encodings with E = +∞, gets the same flat weight, so p*_{α,T} depends on the encoding (A9). | R4, R9; `s31 Q1, Q10`; `s33 Q-D4` | DERIVED |
| C4 | **Hull projection.** For Σw = 1: ‖Σ w_i U_i − t‖² = ⟨w,a⟩ − ½wᵀBw, with a_i = ‖U_i − t‖² and B_ij = ‖U_i − U_j‖². With sign-free weights, the program emits x* = c + Π(t − c) for any c ∈ aff{U_i} (e.g. c = U_0), with gain ∂x*/∂t = Π (1 in the hull, 0 orthogonal). Error: ‖x* − x_nat‖² = ‖Π(t − x_nat)‖² + ‖(I − Π)(x_nat − c)‖². With w ≥ 0, x*(t) is **piecewise affine** in t. On a region where the active support S is constant, {U_i : i ∈ S} is affinely independent and strict complementarity holds, the gain is the projector onto the active face, with \|S\| − 1 unit eigenvalues. | R5, R6; `s32 QR-2, QR-3` | DERIVED |
| C5 | **Dimension counting.** On a register with d_H = poly(input) (dense encoding), the ground or Gibbs state of *any* Hamiltonian costs O(d_H³) (eigh), and a G-gate circuit with a ancillas costs O(G·d_H·2^a) to simulate. No exponential separation is possible. A one-hot or sparse encoding of K candidates on K qubits has d_H = 2^K and is not covered once the Hamiltonian or circuit leaves the valid subspace (B2). | R7; `s31 Q9, Q10` | DERIVED |
| C6 | **Register-relaxation bound.** If E_reg(b) = E(decode(b)), then min_b E_reg ≥ min_y E(y). Under (a), a register stage can beat only a heuristic continuous decoder, never an exact one. | R10; `s33 Q-D3` | DERIVED |
| C7 | **Sparse s-of-K monotonicity.** f*(s) = min{Ψ(w) : \|supp w\| ≤ s} is non-increasing in s and equals min Ψ exactly for s ≥ s*, where **s* := min{\|supp w\| : w ∈ argmin Ψ}** (needed when Ψ is not strictly convex). Cardinality binds iff s < s*. | R11; `s32 QR-4` | DERIVED |

R6 enters C4 only through its identity. Its claim that the sufficient statistic is about 33 real numbers per target is an information statement: T1 neither needs nor proves it.

R8 and R12 are not corollaries. They are **boundary conditions**: R12's (C1) ∧ (C2) is exactly "outside D4" (B2 in §6), and R8's P1 ∧ P2 is "implicit register and a stochastic/specified target" (B1).

### 1.9 Screening checklist (the roadmap's required output)

Answer these in order for any proposed architecture, before any compute.

1. **Q1.** Is every classical output of the quantum stage a function of computational-basis samples, with no quantum downstream and no measurement in another basis? **No:** outside T1 (B4).
2. **Q2.** Is the training objective dephasing-dominated for a classical cost E, i.e. J(ρ) ≥ Φ(diag ρ)? **No** (non-commuting H, or a data-driven loss): outside T1. See B2, or [F86, F90, F91] for data losses.
3. **Q3.** Does downstream use p only through argmin, the E-order tail, or a convex-program solution with an explicit support or a named Φ? **Yes:** Theorems 1–3 apply. The stage is a solver for OPT, TOP_m, CVX or SAMPLE of a classical specification. A general convex Φ on an implicit register: no reduction (G-15).
4. **Q4.** Is the register explicit? Classical reproduction is poly(N) for diagonal E, or poly(d_H) for a non-diagonal H on a dense encoding. **Stop if E is a classically computed table** and the readout is diagonal with Õ(N) post-processing (Lemma 2). If E is a formula evaluated on demand, Grover-type minimum finding still offers √N queries on a poly-size register. Then apply the N2-type FT break-even to that √N gain.
5. **Q5.** Implicit register with readout (a), or (b) with small m? The question left is the speed of OPT(E) or TOP_m(E). Then:
   - **(i)** Is E black-box, or a structured continuous landscape (such as the A80 energy) where QHD-type dynamics apply [T1-1, T1-2]? The quadratic ceiling holds only for black-box E; structured E is open (B5).
   - **(ii)** Apply the FT break-even (§4 N2; T4 for compiled costs).
   - **(iii)** Check transmission (condition C: a lower E must mean a better endpoint; within-target ρ(E_P, chain) = −0.08 in S33 is a failure of C).
   - **(iv)** Check conditioning: if the top modes are near-degenerate below the solver's tolerance, the output is decided by solver bias (Q7).
6. **Q6.** Implicit register with a whole-distribution readout of a specified π? This is SAMPLE(π), outside T1. Go to T2 (mixing, lifting, warm start, break-even). First test the premise of Proposition 5 (concentration), and name the discretisation if the energy is continuous.
7. **Q7.** Does the claim rest on the stage **not** reaching its optimum? Apply Proposition 4(3): a contract-level gain, an equal-tuning classical distribution family, and evidence that the output cannot be simulated classically.

---

## 2. Model and assumptions

| Id | Assumption | Status |
|---|---|---|
| A1 | Computational-basis readout only (D3). Downstream is classical. | Modelling choice; B4 relaxes it. |
| A2 | The objective is dephasing-dominated for a **classical** cost E (D4). | Holds for Φ₁, Φ_α, Φ_{α,T}, Φ_T (equality) and J_q (Lemma 1). Fails for non-commuting H (B2). |
| A3 | E is classically computable at t_E per point. Both sides have the **same access**: the classical algorithm evaluates E; the quantum stage builds H_E (or a coherent E oracle) from the same classical description, and that construction is charged to it. There are **no free oracles, state preparation or block encodings**. | Oracle discipline; B3 relaxes it. |
| A4 | "Reproduce" means: output the ideal pipeline's Y, in distribution over ξ and shots. If R is not constant on argmin Φ (a degenerate X_min under (a); weights among ties), output *one of* the outputs the ideal pipeline can produce. | Definition. |
| A5 | The costs are worst-case, in exact arithmetic, per target. ε is the tolerance for convex solves and bisection. | Standard. |
| A6 | "Ideal stage" means p_out ∈ argmin_𝒮 J. Non-ideal outputs are handled only by Proposition 4. | Scope. |
| A7 | Finite shots enter only through the optimisation-quality channel, except for the explicit S-shot statement in Theorem 2(a). S30 measured CVaR shot bias below one shot-noise SD (`s30` lane L); it is not proved in general. | INFERENCE; G-7. |
| A8 | Explicit versus implicit is a property of the **state count relative to the input size**, not of the qubit count. For diagonal E the count is N_valid. For non-diagonal H or circuit simulation (C5) it is d_H, which must itself be poly(input). A 9-qubit candidate register is explicit. A 40-qubit contact register is implicit. | Definition. |
| A9 | Invalid strings carry E = +∞ (or a penalty). This is harmless for Φ₁, Φ_α, Φ_T and J_q, whose optima put no mass there. It is **not** harmless for Φ_{α,T} with α < 1: p*_{α,T} gives every invalid string the flat weight of a valid state above s* (check C3: E = (0, 1, 3, ∞, ∞, ∞), α = 0.5, T = 0.5 puts mass 0.30 on the invalid strings). On an implicit register with many invalid strings, most of the 1 − α mass can sit on invalid structures. | Stated; affects SAMPLE(p*_{α,T}). |

**Standard facts used without a bibliography key** (mathematics, not literature claims): Klein's inequality (D ≥ 0, with equality iff the states are equal); the Schur–Horn majorisation theorem; LP duality; Sion's minimax theorem (compact convex × convex, convex–concave, lower/upper semicontinuous); polynomial-time interior-point methods for QP/SOCP; Weierstrass (a lower semicontinuous function on a compact set attains its minimum); the Clopper–Pearson interval.

---

## 3. Proofs

### 3.1 Lemma 1 (dephasing)
The complete dephasing Δ(ρ) = Σ_x |x⟩⟨x|ρ|x⟩⟨x| = diag(p). log Δ(ρ) is diagonal, so tr(ρ log Δρ) = Σ_x p_x log p_x = −H(p). Then

`D(ρ‖Δρ) = tr ρ log ρ − tr ρ log Δρ = −S(ρ) + H(p)`

This is ≥ 0 by Klein's inequality, with equality iff ρ = Δρ. Since tr(H_E ρ) = ⟨E⟩_p for diagonal H_E, J_q(ρ) = Φ_T(p) + T·D(ρ‖Δρ). For a general Schur-concave entropy f: diag ρ ≺ spec ρ (Schur–Horn) gives f(diag ρ) ≥ f(spec ρ). ∎

**Check C4 · EVIDENCE (this note):** over 5,000 random mixed states at d = 16, min [J_q(ρ) − Φ_T(diag ρ)] = 0.120 > 0.

### 3.2 Theorem 1
1. For any p ∈ Δ_X, the diagonal state ρ_p = Σ p_x|x⟩⟨x| (or the pure state Σ √p_x |x⟩) has diagonal p, so ρ ↦ diag ρ maps onto Δ_X. For every ρ, J(ρ) ≥ Φ(diag ρ) ≥ inf_Δ Φ, and J(ρ_p) = Φ(p), so the infima coincide.

   **Minima exist** because each named Φ is lower semicontinuous on the compact set Δ_X, including when E takes the value +∞ (D1). By (★) in §3.3, CVaR_α is a supremum of affine functions of p: terms with E_i = +∞ drop out, and the supremum is +∞ exactly when p({E < ∞}) < α. ⟨E,p⟩ is lsc for E bounded below, and −T·H is continuous. With finite E all named Φ are continuous. Restricting to 𝒮 can only raise the infimum.
2. Immediate from 1.
3. Φ₁ and Φ_α: Corollary 2. Φ_{α,T}: Corollary 3. Φ_T: Φ_T(p) = T·KL(p‖π_T) − T·log Z_T is minimised uniquely at π_T. J_q: by Lemma 1 its minimum equals min Φ_T, attained only at the diagonal state diag(π_T). ∎

### 3.3 Corollary 1 (prefix theorem)
Take V differentiable on the polytope Λ_α(p). The constraints are linear, so every local minimiser is a KKT point.

At a KKT point there is a multiplier s with g := ∇V(λ*) satisfying:
- λ*_i = 0 ⇒ g_i ≥ s;
- λ*_i = p_i ⇒ g_i ≤ s;
- 0 < λ*_i < p_i ⇒ g_i = s.

So λ* is full on {g < s}, empty on {g > s} and partial only on {g = s}. That is a prefix of the order induced by g.

For linear V = ⟨E,λ⟩, g = E does not depend on λ*, so the LP optimum is the greedy fill in E-order (the fractional knapsack). The LP dual is max_s [sα − Σ_i p_i (s − E_i)₊], which gives

`CVaR_α(E;p) = max_s [ s − (1/α) Σ_i p_i (s − E_i)₊ ]` (★)

**Sufficient condition for one sort (DERIVED).** Let V be convex, π a fixed order, λ^π the greedy fill of Λ_α(p) along π, and suppose ∇V(λ^π) is non-decreasing along π. Take s = ∇V(λ^π) at the partially filled element, or any value between the last full and the first empty element's gradients if no element is partial. Then full elements have g ≤ s and empty ones g ≥ s, so λ^π is a KKT point. For convex V it is a global minimiser, and one sort along π reproduces it. For V = ⟨E,λ⟩ the order is the E-order, known before solving. ∎

**Not proved here (INFERENCE, cited).** S30's criterion (`s30 Q2`) says the tail stops being reproducible by one sort iff λ ↦ ∇V(λ) has more than one self-consistent order. Neither direction is proved here. Even a unique self-consistent order is defined through ∇V(λ*), which is unknown until λ* is solved.

**Check C1 · EVIDENCE (this note):**
- Over 240 random cells (N ∈ {8, 64, 512}, α ∈ {0.05, 0.18, 0.5, 1}), max |λ_LP − λ_greedy| = 1.2×10⁻¹⁵, and objectives agree to 4.0×10⁻¹⁵, also under heavy ties.
- For 30 random convex-quadratic V, the KKT prefix violation is at most 5.6×10⁻¹⁵.

The source measured 4,914/4,914 cells to 1.1×10⁻¹³ (`s30 Q2`).

### 3.4 Corollary 2 and Theorem 2(a) (solver equivalence, tail collapse)
λ*/α is a probability law on X, so CVaR_α(p) = ⟨E, λ*/α⟩ ≥ E_min, with equality iff supp λ* ⊆ X_min. By C1, λ* fills X_min first, so supp λ* ⊆ X_min iff p(X_min) ≥ α. Hence:
- min_Δ Φ_α = E_min;
- argmin = {p : p(X_min) ≥ α};
- at any optimum the tail law lives on X_min, and supp p meets X_min, so R_a(p) ⊆ X_min for the exact distribution.

With X_min = {x*}, every readout in (a) and (b) equals G(x*), whatever solver produced p. Φ₁ is the case α = 1.

**Finite shots.** S independent draws from an optimal p all miss X_min with probability (1 − p(X_min))^S ≤ (1 − α)^S. So the S-shot argmin lies in X_min with at least the complementary probability. ∎

**Check C2 · EVIDENCE (this note):**
- A joint LP over (p, λ) gives min_Δ Φ_α − E_min = 0 exactly, over 9 cells.
- Over 2,000 random (p, α), the rule "CVaR = E_min ⇔ p(X_min) ≥ α" had 0 mismatches.
- With p(X_min) = α exactly, Monte Carlo miss rates (2×10⁵ trials) were 0.0773, 0.0290 and 0.0617, against (1 − α)^S = 0.0769, 0.0281 and 0.0625 at (α, S) = (0.05, 50), (0.2, 16) and (0.5, 4).

The source's chain-level agreement: E604b VQE 6.431 ≈ exact 6.341 ≈ SA 6.358 Å (`s33 Q-D1`).

### 3.5 Theorem 2(b) (the one-integer bound)
By C1 and D5(b), λ*(p) is the greedy fill in the fixed stable E-order up to v = VaR_α(p). If p has full support, supp λ* is the first m elements of that order, where m = #{E < v} + the number of tied elements at E = v that the stable fill reaches with positive mass (possibly several). So supp λ* = P_m with m ∈ {1, …, N}. The set readout therefore takes at most N values, and the stage can transmit at most log₂ N bits to Y.

If the support is arbitrary, supp λ* is the E-order prefix *within* supp p, indexed by (supp p, m), which can take up to about 2^N values. With S shots, the empirical tail is the prefix of the *observed* support, which puts it in the Proposition 4 regime. ∎

### 3.6 Corollary 3 (closed-form hinged Gibbs) and Theorem 2(b-wt)
Using (★), write

`Φ_{α,T}(p) = max_s L(p,s)`, where `L(p,s) = s − (1/α) Σ p_i (s−E_i)₊ + T Σ p_i log p_i`

- **Convexity.** L is convex in p: it is linear plus the negentropy, which is strictly convex. L is concave in s, because (s − E_i)₊ is convex in s. So Φ_{α,T} is a pointwise maximum of convex functions plus a strictly convex term: strictly convex, with a unique minimiser.
- **Minimax.** Δ_X is compact, so Sion's theorem gives min_p max_s L = max_s min_p L.
- **Inner minimisation.** Over the simplex, min_p L(p,s) is attained at p_i(s) ∝ exp((s − E_i)₊/(αT)) with value g(s) = s − T·log Σ exp((s − E_i)₊/(αT)). A state with E_i = +∞ has (s − E_i)₊ = 0 and weight e⁰ = 1, the same as any valid state above s.
- **Dual.** g is concave. Its one-sided derivatives are g′(s−) = 1 − (1/α)·P_{p(s)}(E < s) and g′(s+) = 1 − (1/α)·P_{p(s)}(E ≤ s). The maximiser s* satisfies P_{p*}(E < s*) ≤ α ≤ P_{p*}(E ≤ s*). p(s) is continuous in s, since at s = E_i the weight is e⁰ from both sides.
- **Tail law.** On {E < s*}, p*_i ∝ exp(−E_i/(αT)): a Gibbs law at temperature αT, with total mass P_{p*}(E < s*) ≤ α. The remaining α − P_{p*}(E < s*) of the tail comes from the flat level set {E = s*}. Above s*, p* is flat. Equality P_{p*}(E < s*) = α holds when s* falls in an open gap between levels. When s* sits on a level (a kink of g), the inequality can be strict, and this happens for α in intervals of positive length.
- **α = 1.** For s ≥ E_max, p(s) = π_T and g(s) = −T·log Z_T. For s < E_max, g′(s+) = 1 − P_{p(s)}(E ≤ s) > 0. So argmax g = [E_max, ∞) and p* = π_T exactly, with no limit needed. A limit s* → ∞ is needed only if some E = +∞, and it again gives π_T.
- **Bisection.** The map s ↦ P_{p(s)}(E < s) is non-decreasing: weights below s grow like e^{s/(αT)} while weights above stay 1, and the set {E < s} grows with s. So bisection finds s*. Since |∂ log p_i(s)/∂s| ≤ 1/(αT), TV accuracy ε needs s to accuracy about αT·ε, i.e. ⌈log₂(range(E)/(αT·ε))⌉ steps of O(N) each.
- **Exact O(N log N) method.** Sort E. In an open gap (e_j, e_{j+1}) between consecutive levels, with k = #{E ≤ e_j}, P_{p(s)}(E < s) is continuous and strictly increasing, and P = α has the closed-form solution

  `s = αT·ln( α(N − k) / ((1 − α)·Σ_{i ≤ k} e^{−E_i/(αT)}) )`

  (N counts all states, invalid ones included). If that s lies inside the gap, it is s*. Otherwise test each level e for the kink condition P_{p(e)}(E < e) ≤ α ≤ P_{p(e)}(E ≤ e). With prefix log-sum-exps this is one O(N) scan after the sort, and needs no ε.
- **Uniqueness.** L(·, s*) is strictly convex, so p* = p(s*). ∎

**Check C3 · EVIDENCE (this note):**
- **Closed form vs generic solvers.** Over 18 cells (N ∈ {16, 64}, α ∈ {0.1, 0.25, 1}, T ∈ {0.05, 0.1, 0.5}), the closed form was compared with the best of two independent primal solvers (SLSQP on the joint (p, λ) program, and composite entropic mirror descent).
  - Strong-duality gap ≤ 3.3×10⁻¹⁴, including α = 1, where s* = E_max.
  - F_numeric − F* ∈ [+1.3×10⁻¹⁵, +4.4×10⁻¹²]: no solver went below the closed form.
  - TV(p_numeric, p*) ≤ 1.6×10⁻⁷. The exact method and bisection agree to TV 3.3×10⁻¹⁵.
- **Kink cells.** On E = (0,1,2), α = 0.8, T = 1, both methods give s* = 1 and p* = (0.6357, 0.1821, 0.1821), with P(E < s*) = 0.636 < 0.8 < P(E ≤ s*) = 0.818 and F* = −0.702991, matching Nelder–Mead to 4×10⁻¹⁶.
- **Integer-level cells.** On 60 cells (N = 8, E ∈ {0,…,3}, random α and T), 20 had strict inequality. The sandwich P(E < s*) ≤ α ≤ P(E ≤ s*) held to 5×10⁻¹⁶, and the closed form was never above the numerical optimum (F* − F_num ≤ 4.4×10⁻¹⁶).
- **The rest.** The α = 1 plateau of g is flat to 4×10⁻¹⁵ for s ≥ E_max. The invalid-string example is in A9. On 6 random 6-spin Ising costs, the best product (mean-field) distribution lies 0.062–0.136 above p*, as Theorem 1.1 predicts.

The previous version's check reported "tail mass below s* equals α". That held only because none of its cells landed on a kink, and it did not test the sentence it was cited for.

The source's instrument measurements (`s31 Q1`): duality gap 3.56×10⁻⁹; circuit strictly worse on 126/126; substituting p* is a null at the endpoint (−0.0112 Å, 0.19×; `QX-10`).

### 3.7 Theorem 2(c) and Corollary 4 (hull projection)
**(c).** A unique minimiser w* means every exact solver returns the same w*, so Y = G(r(w*)) is fixed.

**C4 identity.** For Σw = 1:
- Σ w_i‖U_i − t‖² = ‖x(w) − t‖² + Σ w_i‖U_i − x(w)‖², where x(w) = Σ w_i U_i (bias–variance decomposition).
- Σ w_i‖U_i − x‖² = ½ Σ_ij w_i w_j ‖U_i − U_j‖².

Together these give ‖x(w) − t‖² = ⟨w,a⟩ − ½wᵀBw. The program is a convex QP, because it is the squared norm of an affine map.

**Affine weights.** With the sign of w unconstrained, the minimiser of ‖x − t‖² over x ∈ aff{U_i} is the orthogonal projection x* = c + Π(t − c), for any c ∈ aff{U_i} (take c = U_0). Here Π projects onto span{U_i − U_0}, and ∂x*/∂t = Π.

**Error decomposition.** Write x* − x_nat = Π(t − x_nat) − (I − Π)(x_nat − c). The two terms are orthogonal, which gives the stated decomposition.

**Simplex weights.** With w ≥ 0, the KKT conditions fix an active support S, and x*(t) is piecewise affine in t. On a region where S is locally constant (strict complementarity) and {U_i : i ∈ S} is affinely independent, x* is the affine projection onto aff{U_i : i ∈ S}, so the gain has |S| − 1 unit eigenvalues.

**Consequence · DERIVED.** Emitting t directly has error² = ‖Π(t − x_nat)‖² + ‖(I − Π)(t − x_nat)‖². The (affine-weight) readout beats direct emission iff ‖(I − Π)(t − x_nat)‖ > ‖(I − Π)(x_nat − c)‖, i.e. iff the estimate's out-of-hull error exceeds the hull floor. Its output is a fixed affine function of t (piecewise affine with w ≥ 0), so it adds no information beyond t and the candidates. This is S32's sentence: "a structure estimate good enough to make the readout worth solving is already good enough to emit". ∎

**Corollary 7 (proof).** f* is non-increasing because the feasible sets are nested. For s ≥ s*, some minimiser of Ψ is feasible, so f*(s) = min Ψ. For s < s*, the feasible set Δ ∩ {|supp w| ≤ s} is a finite union of compact faces, so f*(s) is attained. None of those faces contains a minimiser of Ψ, by the definition of s*, so f*(s) > min Ψ. ∎

**Check C5 · EVIDENCE (this note):**
- The identity holds to 8.4×10⁻¹⁶ relative, and x* = P_aff(t) to 5.1×10⁻¹⁵.
- Gain eigenvalues are {1 (×6), 0 (×24)} at K = 7, d = 30, and the error decomposition holds to 2.1×10⁻¹⁴.
- **Simplex case.** The constrained solver itself (Lawson–Hanson NNLS with a stiff equality penalty) was differentiated by central differences. The previous version differentiated the affine solve restricted to S, which assumed the claim it tested.
  - All 20 cases had a locally constant, affinely independent active set with minimum support weight > 10⁻⁶.
  - The number of unit gain eigenvalues equalled |S| − 1 in 20/20 (|S| ∈ {2, …, 5}).
  - The Jacobian matched the face projector to 1.6×10⁻⁷.

The source's numbers (`s32 QR-3`): in-hull gain 0.9999999999, orthogonal gain 4.0×10⁻⁹, mean |S| − 1 = 5.25, hull floor 1.829 Å.

### 3.8 Theorem 3 and the lemmas
- **Explicit costs.** Evaluate E on all N items, then take one min, one sort, one scan (or bisection), one QP or one eigh. Each count follows from §3.3–3.7. The eigh row needs d_H = poly(input) (A8). Circuit simulation with a ancillas costs O(G·d_H·2^a). Theorem 1 works at the objective level and does not depend on this.
- **Lemma 3 (TOP_m from OPT) · DERIVED for E whose restrictions stay in the solver's class; UNPROVEN in general (G-3).** Keep a priority queue of subcubes, each labelled by its minimum. Pop the subcube C with the lowest minimum, emit its minimiser x, and split C \ {x} into at most n disjoint subcubes: C_j agrees with x on the first j − 1 free bits and flips bit j. That needs at most n OPT calls per emitted state, so O(m·n) OPT calls in total.
  - The step "E restricted to a subcube is in the solver's class" is true for QUBO/Ising-type E, since fixing bits gives fields. It is not guaranteed for arbitrary E.
  - The output is a set of m lowest-E states. It equals the tie-rule set P_m only if each OPT call returns the tie-rule-least minimiser (a lexicographic OPT). Otherwise the output is reproduced in the sense of A4.
- **Lemma 2 (input cost).** Any stage whose H_E is built from a classically computed N-entry table pays N·t_E to produce the table. The reproduction pays N·t_E + C_post. The ratio is ≤ 1 + C_post/(N·t_E), with C_post as listed in §1.5.
- **Coherent-oracle bound.** OPT(E) with E ∈ {0,1} is unstructured search. So minimum finding inherits Ω(√N) [C55], and Dürr–Høyer attains O(√N) [C56]. The classical black-box cost is Θ(N). TOP_m: classically ≤ N queries (evaluate and sort); quantumly Ω(√N), since its first element answers OPT. ∎

### 3.9 Proposition 4 and Proposition 5
**Proposition 4.**
- (1) Restates Φ(p_out) > Φ(p*).
- (2) Follows from Theorem 2(b), under its full-support hypothesis.
- (3) Is a boundary statement, not a theorem.

**Proposition 5.** π|_B = π·1_B/π(B), so ½‖π − π|_B‖₁ = ½[(1 − π(B)) + (1 − π(B))] = 1 − π(B). For |f| ≤ 1, |E_π f − E_ν f| ≤ 2·TV(π, ν). ∎

---

## 4. Numbers

Every assumption below is labelled. Theoretical statements live in §1–3; everything here is **practical and conditional**. Census numbers are from the read of 2026-09-27 by `T1_reduction_checks.py` (check C7). There were 85 files: 16 chains at each of L = 30, 45, 60, 80 and 100, plus 5 so far at L = 120. The census is still running, with L = 120 and 150 queued.

### N1. The deployed S29–S31 stage (explicit register)
- **EVIDENCE.** Register size D = 512 in the harness, with a production prefix of 128.
  - The stage was simulated as an exact statevector with no shots, using real-amplitude RY + CNOT circuits (`s29` QR §0). The observed support is therefore the full support of p_out, and generic parameters leave no amplitude exactly zero.
  - The measured tail equalled the classical top-m prefix to 1.1×10⁻¹³ on 4,914 cells (`s29` QR §1, citing S28-L21). The full-support hypothesis of Theorem 2(b) held in practice.
- **DERIVED (Theorem 2(b), full support).** The set readout carries at most log₂ 128 = 7.0 bits per target in production and log₂ 512 = 9.0 bits in the harness.
- **EVIDENCE.**
  - The realised m had mean 74.1 and SD 6.7, with correlation +0.026 against chain length.
  - A fixed, target-independent m was indistinguishable from VQE (−0.0082 Å, 0.27×; `s29` QR §2; `QX-01`).
- **EVIDENCE (timing).** p* costs 1.2 ms per target (`QX-10`). Measured with numpy on this machine at about 55% CPU load (check C8, 2026-09-27): eigh 3.5 ms at D = 128 and 64 ms at D = 512; eigvalsh 0.8 ms and 37 ms. The previous "eigh ≈ 1 ms at D = 512" (from `s31 Q10`) is withdrawn: it matches eigvalsh at D = 128, not eigh at 512. Classical reproduction stays sub-second.
- **DERIVED.** E is a classical score table and the readout is diagonal with O(N log N) post-processing, so Lemma 2 applies: no speedup of any size was ever possible for this stage.

### N2. Argmin readouts at L ≤ 100: a parametric sensitivity sketch for matrix row M9 (case (a) → OPT(E) → amplitude-amplified restarts)

**Scope.** N2 concerns M9 only: Grover or amplitude amplification over multistart L-BFGS restarts. It does not cover argmin readouts in general; structured quantum optimisers are B5. The compiled-cost treatment of M9 is T4 (`T4_amplified_mode_finding.md`, v1). Using T3's gate costs, T4 finds the hardware gate failing by ≥ 7×10⁸ at 170 μs with nominal gate costs, whatever q is. N2 is a parametric sketch and defers to T4 for the verdict.

The model is [B46] eq. (12) with a quadratic speedup. The classical cost is T_C = t_C·(1/q)/S and the quantum cost T_Q = t_Q·(1/√q)/R, where q is the probability that one restart reaches the target. Quantum wins iff

`1/q > (t_Q·S / (t_C·R))²`, with break-even runtime `T* = t_Q²·S / (t_C·R²)`

| Id | Assumption | Status |
|---|---|---|
| A-N1 | One classical restart is 200 L-BFGS iterations (185–216 energy+gradient evaluations per restart, line search included). t_C(L) is the median census wall time per restart: 0.123, 0.250, 0.346, 0.970 and 1.341 s at L = 30, 45, 60, 80 and 100, i.e. 0.73, 1.25, 1.72, 4.63 and 6.21 ms per evaluation. Measured one process per job on a loaded 8-core machine. Load inflates t_C, which lowers the threshold, so it favours the quantum side. | EVIDENCE, **PILOT** |
| A-N2 | A reversible coherent decode costs G_eval Toffolis per energy+gradient. **Base:** 10³ at L = 45 (990 pair terms), scaled by pair count: 439, 1,000, 1,788, 3,192 and 5,000 at L = 30…100. Multipliers ×10² and ×10³ are also tabulated. The base is deliberately unrealistic, at about one Toffoli per pair term. The T3 draft primitives (`research/theory/T3_resource_model.py`, CENTRAL, unreviewed) put one pair term at 5.7×10³–2.7×10⁴ Toffolis, i.e. ≈ 5.6×10⁶ per energy at L = 45 before the gradient. On those figures the ×10³ row is the realistic order or below it. | **UNPROVEN**; T3/T4 |
| A-N3 | **Babbush 2021 baseline**, re-read on 2026-09-27: t_G ≈ 170 μs per Toffoli [B46 eq. (6)], t_Q = t_G·G [eq. (7)], sequential. Faster distillation enters as t_G = 170 μs/R, R ∈ {1, 10, 100} [eq. (12), Table II]. The paper puts parallel factories at "a factor that is between about ten and one-hundred". Free: reversible L-BFGS history, uncomputation, QRAM, amplitude-amplification constants. | THEORETICAL inputs. The free items are quantum-generous; the sequential Toffoli count is not, which is why R is tabulated |
| A-N4 | The quantum side needs ≈ 1/√q coherent decodes (amplitude amplification / Dürr–Høyer [B1, C56]). The classical side needs ≈ 1/q restarts (up to ln 1/δ). | THEORETICAL |
| A-N5 | Classical parallelism S ∈ {1, 8, 10³}. S = 10³ is the reference adversary of [B46] Table II. | Choice |

**Threshold 1/q* (DERIVED arithmetic, check C6).** Pair-scaled G_eval unless stated, with the median t_C(L).

| Setting (G_eval multiplier, S, R) | L = 30 | 45 | 60 | 80 | 100 |
|---|---|---|---|---|---|
| ×1, S = 1, R = 1 (baseline) | 1.5×10⁴ | 1.9×10⁴ | 3.1×10⁴ | 1.3×10⁴ | 1.6×10⁴ |
| ×1, S = 8, R = 1 | 9.4×10⁵ | 1.2×10⁶ | 2.0×10⁶ | 8.0×10⁵ | 1.0×10⁶ |
| ×1, S = 1, R = 100 | 1.5 | 1.9 | 3.1 | 1.3 | 1.6 |
| ×1, S = 10³, R = 100 | 1.5×10⁶ | 1.9×10⁶ | 3.1×10⁶ | 1.3×10⁶ | 1.6×10⁶ |
| ×10², S = 1, R = 100 | 1.5×10⁴ | 1.9×10⁴ | 3.1×10⁴ | 1.3×10⁴ | 1.6×10⁴ |
| ×10³, S = 1, R = 100 | 1.5×10⁶ | 1.9×10⁶ | 3.1×10⁶ | 1.3×10⁶ | 1.6×10⁶ |
| ×10³, S = 1, R = 1 | 1.5×10¹⁰ | 1.9×10¹⁰ | 3.1×10¹⁰ | 1.3×10¹⁰ | 1.6×10¹⁰ |
| G_eval = 10³ fixed, S = 1, R = 1 | 7.6×10⁴ | 1.9×10⁴ | 9.6×10³ | 1.2×10³ | 6.4×10² |

Break-even runtimes T* at L = 45: 1.3 h at the baseline; 147 yr at ×10³ with R = 1; 5.4 days at ×10³ with R = 100.

**EVIDENCE, PILOT.** The G1 mode census (`research/results/RAW/g1_modes/`): R = 256 restarts drawn from the exact prior, 200 L-BFGS iterations, greedy 2 Å Cα-RMSD clustering in energy order, T = 1. A "mode" is a 2 Å cluster, and its reported energy is its lowest member's. "Cluster q̂" is the fraction of restarts in the lowest cluster. "Energy-level q̂_E" is the fraction within 1 nat of the lowest energy found (`frac_within_dE`).

| L | chains | median cluster q̂ (min–max) | best cluster hit once | median modes / 256 | median Good–Turing unseen mass (bounds) | chains with unseen ≥ 0.5 | energy level: chains with q̂_E = 1/256 | median top-2 gap (nats) | min non-positive Hessian eigenvalues |
|---|---|---|---|---|---|---|---|---|---|
| 30 | 16 | 0.117 (0.0039–0.945) | 1/16 | 82 | 0.17–0.19 | 4 | 7/16 | 2.2 | 6 |
| 45 | 16 | 0.109 (0.0039–0.613) | 1/16 | 109 | 0.31–0.32 | 6 | 10/16 | 6.8 | 15 |
| 60 | 16 | 0.049 (0.0039–0.398) | 4/16 | 150 | 0.47–0.49 | 8 | 14/16 | 20 | 36 |
| 80 | 16 | 0.059 (0.0039–0.246) | 3/16 | 181 | 0.64–0.65 | 14 | 16/16 | 52 | 57 |
| 100 | 16 | 0.016 (0.0039–0.137) | 4/16 | 244 | 0.93 | 16 | 15/16 | 41 | 77 |
| 120 (partial) | 5 | 0.016 (0.0039–0.020) | 2/5 | 252 | 0.98 | 5 | 5/5 | 107 | 112 |

**How to read the unseen-mass column.** The census JSONs store the sizes of only the 50 lowest-energy modes, while n_modes reaches 256. The previous version counted singletons among those 50, which caps the estimate at 50/256 = 0.195 and gave 0.078, 0.115, 0.129 and 0.146. The bounds above use n_modes: the unstored modes hold the remaining restarts, each mode at least one. For example, 3GAHA_60 has n_modes = 256, so its unseen mass is 1.0, not 0.195. Per-chain values are in the check output. The 95% Clopper–Pearson upper bound on 1/q is 1.0×10⁴ for a chain whose best cluster was hit once, and 1.06×10³ for two hits.

**INFERENCE (scoped; supersedes the previous "cannot carry a practical quantum advantage at L ≤ 60").**
- **Median chain, lowest-found cluster, L ≤ 45.**
  - At the baseline (R = S = 1) the threshold is 10^3.24 and 10^3.31 above median 1/q̂ ≈ 9. It is 10^3.18, 10^2.87 and 10^2.40 at L = 60, 80 and 100, so the gap is **≈ 2.4–3.3 orders** at pair-scaled base G_eval. With S = 8 it is about 5 orders.
  - At base G_eval the conclusion needs R ≤ 10. At R = 100 (Toffolis as cheap as Cliffords) the threshold falls to 1/q* ≈ 2, below every median.
  - With G_eval ≥ 10² × base (≈ 10⁵ Toffolis at L = 45), the gap is ≥ 2.4 orders even at R = 100.
  - So the median statement rests on G_eval ≫ 10³. The T3 draft primitives support that, but T3 has not finalised them.
- **Resolution-limited chains** (best cluster hit once in 1, 1, 4, 3 and 4 of 16 chains).
  - Their 95% upper bound, 1/q ≤ 1.0×10⁴, is within 1.3–3× of the baseline threshold. It also exceeds the fixed-G_eval threshold at L ≥ 60 (9.6×10³, 1.2×10³, 6.4×10²). At base G_eval these chains are **not excluded**.
  - They are excluded, by ≥ 2 orders, once G_eval·S/R ≳ 10 × base: G_eval ≳ 10⁴ at L = 45 with S = R = 1, or ≳ 10⁶ with R = 100.
  - That exclusion is **conditional on the lowest-found cluster being the global one**.
- **The global minimum is not bounded by these data.** At L ≥ 60 the census is unsaturated: median unseen mass ≥ 0.47, and ≥ 0.5 in 8, 14 and 16 of 16 chains at L = 60, 80 and 100. A never-hit lower basin is then plausible, and for it the data give no upper bound on 1/q.
- **Energy level.** OPT(E) proper asks for the minimum energy, not the 2 Å cluster.
  - Within 1 nat of the best energy found, q̂_E sits at the resolution limit 1/256 in 7, 10, 14, 16 and 15 of 16 chains at L = 30…100. That gives 1/q ≥ 256 as a point estimate and ≤ 1.0×10⁴ at 95%, again conditional on best-found = global.
  - The cluster rate overstates the energy-level rate because one 2 Å cluster spans tens of nats of unconverged energies. In 5O37A_45 the lowest cluster holds 46 restarts, but only 1 of 256 lies within 20 nats of its minimum.
- **Both rates are properties of the decoder budget and the clustering, not of the landscape.** 200 iterations leave every recorded Hessian with ≥ 6, 15, 36, 57 and 77 non-positive eigenvalues at L = 30…100. Converged decodes and a larger R (G1) are needed before either rate is read as a landscape property (G-13).
- **Beyond 80 aa.**
  - L = 100 is now measured: median cluster 1/q̂ = 64. T4 fits ln p_hit with a median slope of −0.030 per residue.
  - The census t_C grows about as L^1.98 from L = 30 to 100, so the pair-scaled baseline threshold stays within 1.3–3.1×10⁴.
  - That growth is confounded by load. Per-evaluation cost grows as ≈ L^1.24 over L = 30–60 and jumps at L ≥ 80. The brief's single-core figure is ≈ 1.8 ms at L = 150, against 4.6–6.2 ms loaded at L = 80–100.
  - Suppose unloaded cost grows as L^b, with b ≈ 0.6 (the brief's 1.8 ms at L = 150 against 0.73 ms at L = 30) to 1.25 (census, L = 30–60), and G_eval ∝ L². Then 1/q* ∝ L^{2(2−b)} ≈ L^{1.5–2.8}, which moves the threshold away from the quantum side.
  - Either way the threshold does not fall with L, and the census timings are the quantum-favourable choice. The previous sentence ("t_C and G_eval both grow roughly as L²") is withdrawn as stated.
- **Downgraded conclusion.** For the lowest-found cluster in the median chain at L ≤ 45, M9 cannot reach break-even under A-N1–A-N5, provided G_eval ≳ 10⁵ Toffolis per energy+gradient at L = 45 (or R ≤ 10). At L ≥ 60 the census is unsaturated and the question is **undetermined by these data**. T4's compiled costs decide it independently of q. This is a statement about M9, not about case (a) in general.
- **Superseded brief numbers.** The brief's "~32 distinct minima from 64 restarts at L = 45, best mode hit by ~22%" comes from the R64 test file. The census gives, for the same crop, 104 clusters in 256 restarts and a best-cluster rate of 18%, with its best energy (±1 nat) hit once. Across 16 crops at L = 45 the median is q̂ = 0.11 with 109 clusters. See §9, R-1.

### N3. Can whole-distribution readouts at T = 1 be approximated by argmin (the premise of Proposition 5)?

**EVIDENCE, PILOT.**
- The previous version used `g1_modes_test/5O37A_45_R64_s0.json`, which is superseded by the census file for the same crop (§9, R-1). In `g1_modes/5O37A_45_R256_s0.json` the two lowest cluster minima differ by ΔE = 79.7 nats.
- **Across the census**, the top-2 gap is < 1 nat in 7 of 85 cells, < 2.2 nats in 17 and < 5 nats in 24. The median is 17.6 nats and the IQR 3.4–64. Per-L medians are 2.2, 6.8, 20, 52 and 41 nats at L = 30…100. Examples: 3M3PA_60 0.02, 9IXCA_45 0.23, 3TE4A_30 0.41 nats. "Gaps of tens of nats between modes" is typical at L ≥ 60, not at L ≤ 45.
- **The stored Laplace numbers cannot decide the question.** `scripts/g1_mode_census.py::hessian_logdet` clips eigenvalues at 10⁻⁶, and every recorded Hessian has non-positive eigenvalues. Each one contributes ln(floor) to log det H. The Laplace log-mass ratio (mode 1 over mode 0, T = 1) is therefore:
  - −35.80 − 4·ln(floor) in the R64 file: +19.5 at a floor of 10⁻⁶, +1.0 at 10⁻⁴, −8.2 at 10⁻³;
  - −76.86 − 3·ln(floor) in the census file.

  The sign is set by an arbitrary floor. The previous version's reading, that the higher-energy mode "nevertheless" wins, was an artifact of that floor and is withdrawn.

**INFERENCE.**
- ΔE alone does not establish π(B*) ≈ 1. At T = 1 a reversal needs the higher mode to carry ΔE nats more log-volume: 44.7 nats (0.53 nats per dimension over D = 2L − 5 = 85) for the R64 pair, and 79.7 nats (0.94 per dimension) for the census pair. Nothing in the pilot data measures that volume.
- Near-degenerate cells (about 20% within 2.2 nats) need no reversal at all: their two modes carry comparable mass unless the volumes differ sharply.
- The premise of Proposition 5 must be measured as **basin free energies** (G3), not minimum energies. Until it is, whole-distribution readouts of π at T = 1 must be treated as SAMPLE(π), which is outside T1.
- **Argmin conditioning.** For readout (a), T1's statement is unaffected: the ideal output is still OPT's. But gaps below the decoder's convergence tolerance mean that *which* structure OPT returns is decided below the energy's resolution, and any non-exact solver's output is decided by its bias. That is Proposition 4 (G-1), where T1 has no theorem. For this energy that regime is practically relevant, especially at L ≤ 45.

### N4. The pilot sampling numbers
The brief (**PILOT**) reports a communication barrier Λ ≈ 7 (L = 30), ≈ 14 (L = 45–60) and ≈ 25 (L = 100–120), a first-order-like bottleneck at λ ≈ 0.4–0.5, and 0 round trips in 1,200–1,500 scans.

**T1 is silent on these numbers.** They concern SAMPLE(π_λ) along a tempering path, the excluded case, and they are input to T2. Two cautions (INFERENCE):
- Λ growing roughly linearly in L would, on its own, suggest polynomial cost for non-reversible PT. The hardness signal is the bottleneck with 0 round trips, where a Λ computed from local swap rates may misstate the barrier.
- The proven quantum speedups for SAMPLE are at most quadratic and query-model [A44, A45], so the [B46] break-even applies here too.

**One direct T1 implication.** T1's model (D1) is a finite register, while the A80 energy lives on continuous internal coordinates. Take a discretised register, for example a (θ,τ)-torsion register with b bits per angle (T3 uses b = 10). A quantum stage trained on Φ_T for that register would, if trained perfectly, sample π_T **of the discretised energy** (Corollary 3 at α = 1). Its distance from the continuous posterior is a separate approximation that T2 must control: bin volume, the within-cell variation of E, and any Jacobian between coordinate systems. The stage's value is therefore bounded by the answer to T2, not by anything variational.

### N5. Classical-reproduction cost at the deployed scale
- **EVIDENCE.** At N ≤ 512: sort in microseconds, p* in 1.2 ms (`QX-10`), eigh 3.5–64 ms and eigvalsh 0.8–37 ms (check C8, loaded machine).
- **THEORETICAL.** The FT reference point: quantum-accelerated SA needs "roughly a day and a million physical qubits" for spin glasses "that could be solved by classical simulated annealing in about four CPU-minutes" [A56 = C64].

---

## 5. Literature: where T1 sits among the general classical-reproducibility results

T1 is elementary mathematics: LP duality, minimax, majorisation. Its value is the **scope statement and the routing**, not novelty (INFERENCE).

Barkoutsos et al. [C6] (re-read on arXiv, 2026-09-27) already contain two pieces of it:
- **Eq. (11)** defines CVaR_α(X) = E[X | X ≤ F_X⁻¹(α)], the lower-tail conditional expectation.
- **Eq. (12)** is its sorted-sample estimator: the mean of the ⌈αK⌉ lowest of K sorted samples. As printed, the sum runs from k = 0 to ⌈αK⌉ while the samples are indexed from 1. The estimator has **no fractional boundary weight**, so at finite K it differs from D4's LP form and from the (b-wt) tail by the share of the boundary sample. It coincides with (11) when no atom straddles the VaR.
- **§5**, in the discussion following Prop. 5.1, states that if a trial state "has overlap ρ with the ground state, then it is a global optimum of (13) for any α ≤ ρ". Here overlap means ground-state probability. That is the sufficiency half of C2.

| Result | Object reduced | Hypotheses | Conclusion | Relation to T1 | Tag |
|---|---|---|---|---|---|
| Schuster, Yin, Gao, Yao [F35], PRX 15, 041018 (2025), arXiv 2407.12768 | Noisy circuits, **any** observable | Constant noise rate; average over an input ensemble; anticoncentration for sampling | Poly-time expectation values (small average error); quasi-poly sampling; "any quantum circuit for which error mitigation is efficient on most input states, is also classically simulable on most input states" | **Complementary, not an instance.** F35 works at circuit level and needs noise, average-case over inputs. T1 works at objective level and holds for noiseless, arbitrarily deep circuits, worst case. A NISQ diagonal-objective stage is closed twice. Neither covers FT sampling of a specified π. T1's stages have one fixed input (\|0⟩), so F35's ensemble average does not transfer automatically (G-8). | THEORETICAL |
| Cerezo et al. [F37], Nat. Commun. 16, 7907 (2025), arXiv 2312.09121 (a perspective) | Barren-plateau-free variational models | Provable BP absence; a data-acquisition phase | Such models often "encode the problem into some small, classically simulable, subspaces". The abstract (re-read 2026-09-27) lists its caveats: "the limitations of average case arguments, the role of smart initializations, models that fall outside our assumptions, **the potential for provably superpolynomial advantages**" | **Same mechanism, different lever.** In T1 a trained stage's information is compressed into a classical object: X_min, one integer m, one scalar s*, or w*. T1 needs no BP-freeness and holds for BP-afflicted circuits too (S29: the CVaR landscape is flat on 85.5% of simplex directions, `s29` QR §1). F37 is argued case by case; T1 is a theorem in its narrower class. | THEORETICAL |
| Herbst, Brandić, Pérez-Salinas [F91], arXiv 2512.24801; Rudolph et al. [F86], arXiv 2305.02881; Herrero-Gonzalez et al. [F90], arXiv 2511.01845 | Quantum generative models (Born machines) | [F91] is average-case over model classes; [F86] concerns explicit vs implicit losses; [F90] treats a QCBM as a quantum Fourier model | [F91]: anticoncentrating models are not trainable on average, while sparse-output models can be trained, and its abstract (re-read 2026-09-27) ends: "quantum advantage can still be found in generative models, although its source must be distinct from anticoncentration". [F86]: explicit losses such as KL give "a new flavour of barren plateaus". [F90]: dequantisation conditions for QCBMs | **T1's optima are sparse or specified.** CVaR optima concentrate on X_min, which is F91's trainable, surrogate-able regime. The free energy Φ_T is an explicit KL loss to π_T, so F86 predicts training obstacles and T1 identifies the target. F91 and F90 concern *learning from data*; T1 concerns *optimising a known energy*. Proposition 4(3) is where they meet. | THEORETICAL |
| Tang [F52] (STOC 2019, arXiv 1807.04271); Tang [F53] (PRL 127, 060503, arXiv 1811.00414); Chia et al. [F54] (arXiv 1910.06151); Gharibian–Le Gall [F55] (SIAM J. Comput. 52(4), arXiv 2111.09079) | QML and linear-algebra speedups | ℓ²-sampling-and-query access (the classical analogue of QRAM state preparation); low rank; constant-precision QSVT | Exponential gaps collapse to polynomial [F52–F54]. Constant-precision QSVT is dequantised, and higher precision is BQP-hard [F55] | **The same access-model logic.** In dequantisation, the apparent advantage lived in the state-preparation assumption. In T1, it would have to live in the readout, and argmin, prefix and convex readouts extract only a classically computable object. Matrix row M15 (QSVT/HHL for readout convex programs) is closed jointly by T1(c) (explicit, poly) and [F52–F55]. T1 needs no low-rank assumption; dequantisation needs no diagonal objective. | THEORETICAL |
| Barkoutsos et al. [C6], Quantum 4, 256 (2020), arXiv 1907.04769 | CVaR-VQE | Diagonal costs | CVaR objective (eqs. (11)–(13)); compared only against expectation-VQE | C1's structure is visible in their eq. (12), a sorted-sample prefix. C2's sufficiency half is their §5 remark. The KKT prefix theorem for general V and the characterisation are S30/S33's. | THEORETICAL (re-read) |
| BBBV [C55] (SIAM J. Comput. 26(5), 1997, arXiv quant-ph/9701001); Dürr–Høyer [C56] (arXiv quant-ph/9607014) | Unstructured search and minimum finding | Black-box oracle | Θ(√N) quantum queries | Bounds the speedup left in case (a) for black-box E at quadratic, and for TOP_m via its first element. | THEORETICAL |
| Leng, Hickman, Li, Wu [T1-1], "Quantum Hamiltonian Descent", arXiv 2303.01471 (2023); Leng, Zheng, Wu [T1-2], "A quantum-classical performance separation in nonconvex optimization", arXiv 2311.00811 (2023) | Continuous non-convex optimisation with an explicit objective | [T1-1]: Hamiltonian evolution from the path integral of gradient flow; empirical D-Wave runs on non-convex QPs up to 75 dimensions. [T1-2]: a constructed d-dimensional family with 2^d local minima | [T1-2]: QHD solves every instance of the family with Õ(d³) quantum queries to the function value and Õ(d⁴) further gates; "a comprehensive empirical study suggests" that state-of-the-art classical solvers, including Gurobi, "would require a super-polynomial time" | **Outside T1's ceiling.** It is the structured-OPT route (B5) for exactly the A80 type of objective: explicit, continuous, differentiable, non-convex. The separation is query-model, on engineered instances, with **empirical** classical hardness only, and no FT cost is given. Screening item Q5(i). | THEORETICAL (abstracts verified 2026-09-27) |
| Sanders et al. [A56 = C64], PRX Quantum 1, 020312 (2020), arXiv 2007.07391; Babbush et al. [B46 = C65], PRX Quantum 2, 010103 (2021), arXiv 2011.04149 | Quadratic speedups on early FT hardware | Surface-code cost models | "A day and a million physical qubits" vs "four CPU-minutes". The d = 2 break-even is M > t_Q·S/t_C [B46 eq. (5)], or M > t_Q·S/(t_C·R) with faster distillation [eq. (12)], where M² is the classical step count | Used in §4 N2. It decides the case-(a) routing in practice, together with T4. | THEORETICAL (B46 re-read 2026-09-27) |

**Combined scope (INFERENCE).** The literature forms and T1 share one pattern: *a quantum stage that can be trained or mitigated, or whose objective sees only its diagonal, produces an object a classical algorithm with the same access can compute.* What survives all of them is a quantum stage that:
1. runs fault-tolerantly, not NISQ (F35);
2. has no trained output law, or one whose advantage does not come from anticoncentration. Trained and variational laws are **argued against on average (F37, F91), not excluded**: F91's closing sentence and F37's caveats keep the door open;
3. reads out a whole distribution of a *specified* target over an implicit space (T1), or solves a *structured* OPT outside the black-box ceiling (B5);
4. is compared at matched access (F52–F55) and against the FT break-even (B46).

The program's prioritised instance is SAMPLE(π) by a coherent walk or Langevin-type operator (matrix rows M1/M2; T2's subject). It is not the only one (§7).

### 5.1 Papers cited here that are not yet in the bibliography
- **[T1-1]** J. Leng, E. Hickman, J. Li, X. Wu, "Quantum Hamiltonian Descent," arXiv:2303.01471 (submitted 2 Mar 2023). Title, authors and abstract verified on arXiv, 2026-09-27.
- **[T1-2]** J. Leng, Y. Zheng, X. Wu, "A quantum-classical performance separation in nonconvex optimization," arXiv:2311.00811 (submitted 1 Nov 2023; no journal reference listed on arXiv). Title, authors and abstract verified on arXiv, 2026-09-27.

These should enter `BIBLIOGRAPHY.md` under the literature phase's key scheme (§9, R-3).

---

## 6. Scope: what is NOT claimed

**Boundary (outside T1):**

| Id | Not covered | Why | Where it goes |
|---|---|---|---|
| **B1** | **Whole-distribution readouts of a fixed target over an implicit register**: SAMPLE(π) for π_T, p*_{α,T}, a learned-energy posterior, or the uniform law on a sublevel set | Theorem 3 reduces such stages *to* SAMPLE(π). It says nothing about SAMPLE(π)'s cost. This is the prioritised lead. | T2, G1, G3; matrix M1, M2, M5 |
| **B2** | **Non-diagonal forward models**: objectives with non-commuting terms whose optimum is not diagonal (R12's C1 ∧ C2); transverse-field QBMs; quantum Gibbs states; amplitude-encoded costs ⟨ψ\|A\|ψ⟩ with non-diagonal A; one-hot or sparse encodings whose circuits leave the valid subspace | D4 fails | Dense explicit registers are still closed by C5 (eigh). Implicit ones are open. |
| **B3** | **Quantum data / quantum-computed costs**: E not classically computable (electronic-structure energies; sensor data) | A3 fails | Matrix M14: out of structure scope, **not refuted** |
| **B4** | **Non-computational-basis or quantum downstream**: ρ_out fed coherently into a later routine (e.g. as a qsample for amplitude estimation), or other observables measured | A1 fails | Matrix M4, M5 |
| **B5** | **The solver-speed question itself** | T1 routes (a) and (b) to OPT and TOP_m. It proves a quadratic ceiling only for black-box E. Not addressed: structured discrete problems (planted inference, DQI; matrix M12 [C69–C73]; backtracking on structured trees, M10), and structured continuous non-convex optimisation, where QHD [T1-1] and a query-model separation with empirical classical hardness [T1-2] exist. The A80 energy is of that continuous kind. | Matrix M9, M10, M12; screening Q5(i); G-12 |
| **B6** | **Benefits from sub-optimality** (Proposition 4(3)) | Not a theorem. Closed only empirically in S29–S33 and by average-case literature. Near-degenerate modes (§4 N3) make this regime practically relevant for the A80 energy. | Screening Q7; G-1 |
| **B7** | **Finite-shot effects** beyond Theorem 2(a)'s S-shot bound | Treated as optimisation quality (A7). The S30 bias measurement is evidence, not proof. | G-7 |
| **B8** | **Continuous targets** | T1's register is finite. Continuous posteriors enter only through a named discretisation (§4 N4). | T2 |

**Other non-claims:**
- T1 makes **no accuracy (RMSD) claim**. It is an output-equivalence and cost statement.
- T1 does **not** say classical reproduction is fast on implicit registers. It says the reproduction costs exactly as much as the specification problem.
- T1 does **not** say quantum stages outside the class can have an advantage.
- The practical numbers in §4 are **not** theorems. They depend on A-N1–A-N5 and on PILOT data.

---

## 7. Consequences for the program's hypotheses and matrix

### H-001: split (recommendation to the registry; `research/HYPOTHESES.md` is not edited by this note)

The pre-registered statement ends "Therefore the quantum component cannot be load-bearing". Its kill criterion is "a pipeline of that form where the quantum stage changes the output in a way no classical algorithm of comparable cost reproduces". T1 settles the two halves differently.

- **H-001a (output equivalence): PROVED** as Theorems 1–2, in the model of §2 (the set readout needs full support). An ideal stage's output is a function of the classical specification, as is every exact classical solver's.
- **H-001b ("not load-bearing", i.e. cost equivalence):**
  - **PROVED** for explicit registers with a classically tabulated E and a diagonal readout with Õ(N) post-processing: Lemma 2, ratio ≤ 1 + O(t_cmp·log N/t_E). It is polynomial, but not necessarily small, for the other explicit cases (Theorem 3, C5).
  - **FALSE in the query model** for implicit registers with black-box E. Dürr–Høyer [C56] outputs the same x* with O(√N) queries, and every classical algorithm needs Θ(N). That is exactly the pre-registered kill criterion's form, with cost read as queries. Theoretical level L2, oracle cost excluded; practical L0.
  - **OPEN** for structured E (B5; [T1-1, T1-2]).
  - **PRACTICALLY UNRESOLVED as a T1 matter.** The practical kill of the case-(a) route M9 rests on T4's compiled costs and N2's sensitivity table. It depends on G_eval (T3), and the corrected census does not bound q for the global minimum at L ≥ 60. T1 alone does not deliver it.
- **Kill criterion.** Keep the pre-registered one. The previous version of this note replaced it with "no counterexample in the inherited evidence". That criterion cannot fail, because the inherited architectures were all designed inside the class, so it is withdrawn.
- **Scope correction to the wording.** "At polynomial cost in the register size" holds for explicit registers. For implicit registers, read "at the cost of the classical solver of the specification problem". For (b-wt), (c1) and large-m (b-set) that problem is SAMPLE(π), outside H-001. A general convex Φ on an implicit register has no reduction (G-15).
- **Prediction "every inherited architecture falls inside the class, and every inherited null follows from it."** Not every architecture falls inside: QX-02, 04, 06 and 11 are outside D4 or A1. Every **explicit-register** null follows from T1 or C5. On implicit registers T1 says only that an ideal stage equals the OPT/TOP_m solution. The nulls there are **empirical** (equal-tuned SA, random prior, condition C), except where C2 (tail collapse) or C6 (register relaxation) supplies the mechanism. The audit:

| QX | Register (A8) | T1 case | Checklist exit | Non-load-bearing status explained by |
|---|---|---|---|---|
| 01 | explicit, N = 128 / 512 | Φ_{α,T}; (b-set) | Q4 | **T1**: Thm 2(b) (full support: exact statevector), C3, Lemma 2 |
| 02 | explicit, d_H = 512 | non-diagonal (B2) | Q2 | **C5** (eigh; the gate used the exact ground state) |
| 03 | explicit, 512 | CVaR tail re-scored by a structural observable | Q4 | **T1**: Thm 2(b). For full-support p the tail is one of N prefixes, which the observable only re-scores |
| 04 | 8^S ≤ 32,768 configurations: enumerable, but implicit in S; transverse field | non-diagonal (B2) | Q2 | **C5** at the tested size; formally B2, so **empirical** (SA, BESTOFN) |
| 05 | explicit | trainability characterisation | — | N/A |
| 06 | explicit, 512; signed-amplitude readout | outside A1 | Q1 | **C5** (amplitudes simulable at d_H = 512); the objective-level null is empirical |
| 07 | explicit | endogenous-order lifts, never built | — | N/A (closed by measurement; the one-sort criterion is C1's INFERENCE part) |
| 08 | explicit | finite shots | Q7 / A7 | **empirical** (G-7) |
| 09 | explicit | (b-set) and sparse readouts | Q4 | **T1** bound (≤ log₂ N bits) plus measured bit accounting |
| 10 | explicit, 128 | Φ_{α,T} | Q4 | **T1**: C3 |
| 11 | explicit | non-diagonal (derivation) | Q2 | **C5** |
| 12 | explicit | encoding change | Q4, Q7 | **T1**: the ideal output of a diagonal objective does not depend on the encoding (A9 aside). The encoding acts only on 𝒮, which is Prop. 4, empirical |
| 13 | explicit | register content (ORACLE) | — | N/A (content, not solver) |
| 14 | implicit, 2^500, not built | diagonal with convex inner weights | Q3 | **T1**: C7 |
| 15 | A: explicit SOCP; B per target: explicit argmax; B per residue: implicit | (c2), (a) | Q4; Q5 for per-residue B | **T1** for A and per-target B. Per-residue B routes to OPT(E) and was not built. The discrimination null is empirical |
| 16 | explicit candidates | (c2) hull | Q4 | **T1**: C4 |
| 17 | 16 qubits enumerable; 60-qubit chain implicit | (a) | Q5 | **empirical** (T1 only routes to OPT(E)) |
| 18 | 16 qubits, enumerable | (a)/(b) | Q5(iii) | **empirical** (condition C) |
| 19 | 18 → 40 qubits, implicit | (a)/(b) | Q5 | **empirical** (SA, greedy) |
| 20 | 80–90 qubits, implicit | (a)/(b) | Q5 | **empirical** (SA, prior-SA) |
| 21 | 66–90 qubits, implicit | not built / condition C | Q5(iii) | **empirical** |
| 22 | 69–90 qubits, implicit | (b-set), 12-state tail | Q5 | mechanism by **T1**: C2 tail collapse, solver-agnostic. The SA comparison is empirical |
| 23 | 69–90 qubits, implicit | robust / joint CVaR over a predictor ensemble: a convex Φ outside the named list | Q3 | **empirical**. No T1 reduction, except that joint CVaR at α ≤ 1/K (K predictors, one drawn uniformly per shot) reduces to OPT of the optimistic energy min_k E_k(x), matching the measured "joint = classical optimistic energy" (G-15) |
| 24 | 123–171 qubits, implicit | (a)/(b) | Q5 | **empirical** (equal-tuned SA) |
| 25 | ≤ 171 qubits, implicit; tail relaxed by the decoder | (b-set) → relaxation | Q5 | **C6** in part (a register beats only a heuristic decoder) + **empirical** (random prior, register-free decoder) |
| 26 | 9–12 qubits enumerable / 18–39 qubits | (b) | Q5(iii) | **empirical** (condition C; random prior) |
| 27 | 18 qubits, enumerated | (a) | Q5 (enumerable) | **T1**: Thm 2(a) plus enumeration (≈ 20 s) |
| 28 | 18 qubits, enumerated | the exact SAMPLE(π_T) target; no circuit | Q6 | N/A (exact classical target) |
| 29 | 18 qubits, enumerated | Φ_T (Born machine) | Q6, Q7 | **T1**: the ideal output is π_T (C3 at α = 1), enumerable here. The circuit losing to Metropolis is Prop. 4, empirical |
| 30 | 44–114 qubits, implicit | (a)/(b) | Q5 | **C6** in part + **empirical** (register-free decoder, random prior) |
| 31 | implicit | not run | Q5 | N/A (C6 predicts the ceiling) |
| 32 | 18 qubits | (b) | Q5(iii) | **empirical** (condition C; SA twin) |
| 33 | various | entanglement and α ablations | Q7 | Prop. 4 / **empirical** |

Recommended registry status: **H-001a SUPPORTED/PROVED (scoped)**. **H-001b**: KILLED in the query model for implicit black-box E; PROVED for explicit tabulated E; OPEN for structured E; practical status deferred to T4/T3.

### H-009: FALSIFIED as worded, both clauses
- **Clause (i),** "the S29–S33 reductions are instances of [F35], [F37], [F91], [F52–F55]", is refuted by §5. They are complementary (objective-level, noiseless, worst-case vs circuit-level, noisy or average-case), not instances.
- **Clause (ii),** "one screening theorem covers all rows marked KILLED", is refuted by the table:

  | Row | Covered by T1? | What closes it |
  |---|---|---|
  | M11 (VQE/QAOA/CVaR) | Fully | T1 |
  | M15 (QSVT for readout convex programs) | Fully | T1 + [F52–F55] |
  | M9 (Grover restarts) | Only as routing to OPT(E) | The FT arithmetic (N2; T4), not the reduction |
  | M13 (quantum generative priors) | Only for energy-trained models (Φ_T → π_T) | Data-trained models are closed by [F37, F90, F91] and the data-processing inequality |
  | M4 (amplitude estimation) | No (B1/B4) | Resource break-even [B46, C64]. Biomolecular estimates are bias- or mixing-limited, not variance-limited [B71] |
  | M7 (QeMCMC) | No: a proposal inside a sampler of a fixed π (B1) | Disputes and quantum-inspired reproductions [A48–A50]; condition C |
  | M8 (annealer as Boltzmann sampler) | No (B1/B2) | Uncontrolled effective temperature [A61–A63] |

  **Correct screening set:** T1 (reduction) + the FT break-even (B46; T3, T4) + T2 (sampling) + the structured-OPT screen (Q5(i)).

### Matrix and roadmap
T1 supplies the checklist of §1.9 and discharges row G4. Its routing statement (INFERENCE), corrected:
- **Every KILLED row and every inherited route** either reduces under T1 (explicit registers; implicit ones via OPT/TOP_m), routes to SAMPLE(π) (B1), or was closed by arguments outside T1 (M4's break-even, M7/M8's disputes, data-trained M13).
- **Routes outside T1 remain open:**
  - non-diagonal forward models on implicit registers (B2);
  - quantum-computed energies (B3; M14, out of structure scope, not refuted);
  - coherent downstream estimation that consumes a SAMPLE state (B4; M4, M5);
  - structured OPT (B5: M10, M12 and QHD-type continuous optimisation);
  - rare-event hitting times (M3).
- **G1/G3/T2 is the program's prioritised path, not the only live one.** It is prioritised because B1 is the one route with a measured computation-limited signal: the soft-over-hard readout, 1.40× RESULT (QX-28).

---

## 8. Open gaps

| Id | Gap | Tag |
|---|---|---|
| G-1 | Proposition 4(3), advantage from *failing* to optimise, has no worst-case theorem. A circuit designed on purpose could emit a hard-to-sample distribution whose deviations happen to be useful. Only average-case literature [F35, F37, F91] and the S29–S33 nulls close it. The near-degenerate census cells (§4 N3) make it practically relevant for the A80 energy. | UNPROVEN |
| G-2 | ~~[C6] "eq. (12)" attribution.~~ **Closed 2026-09-27:** eq. (12) is the sorted-sample estimator. It has no fractional boundary weight, so at finite K it differs from the LP tail. C2's sufficiency half is [C6] §5 (§5 above). | Closed |
| G-3 | Lemma 3 (TOP_m by O(m·n) OPT calls) assumes E restricted to subcubes stays in the optimiser's class. That holds for QUBO/Ising-type E but is not proved for learned or decoder-based E. Exact reproduction of the tie-rule set also needs a lexicographic OPT. The implicit (b-set) cell of Theorem 3 is conditional on this gap. | UNPROVEN in general |
| G-4 | B1 is the prioritised remaining question. T1 gives no bound on SAMPLE(π) for the A80 learned energy. | Handed to T2 |
| G-5 | The premise of Proposition 5 (basin-mass concentration at T = 1) is untested. The stored Laplace numbers are invalid (clip-floor dependent, §4 N3). Converged minima and basin free energies (G3) would decide whether SAMPLE(π) approximately reduces to OPT plus local sampling. | UNPROVEN |
| G-6 | N2 depends on G_eval (A-N2), which T3 has not finalised, and on pilot q̂ (unconverged modes, resolution 1/R, an unsaturated census at L ≥ 60). T4 carries the compiled verdict. | UNPROVEN / PILOT |
| G-7 | Finite-shot CVaR estimation is treated as optimisation quality (A7), beyond Theorem 2(a)'s S-shot bound. There is no general proof that shot noise cannot move a set or weighted readout usefully. | INFERENCE |
| G-8 | [F35]'s simulability is average-case over an input ensemble. A deployed stage with one fixed input is not covered automatically. | Open (literature transfer) |
| G-9 | Non-diagonal forward models on implicit registers (B2), including one-hot encodings that leave the valid subspace, have no reduction here. S29 lanes B and X reduced only empirically. | Open |
| G-10 | No repository-level file defines the claim-level scale (L0–L6). This note uses the working table of the sibling notes (T2, T4) for its one positive statement and otherwise asserts no advantage. Keep open until the scale is defined centrally. | Housekeeping |
| G-11 | The census is still being written (85 files at the 2026-09-27 read; L = 120 and 150 queued). Regenerate the N2 tables with `T1_reduction_checks.py`. `scripts/g1_mode_census.py` stores only the 50 lowest modes' sizes, so the unseen mass is bounded, not computed. Storing f₁ (or every mode size) in future runs would make it exact. The bounds are tight (≤ 0.03 wide in the medians). | Housekeeping |
| G-12 | Structured OPT for the A80 energy (B5): is it a landscape where QHD-type dynamics [T1-1, T1-2] give more than quadratic, and at what FT cost? T1 has no theorem here. Add [T1-1, T1-2] to the bibliography. | Open (screening Q5(i)) |
| G-13 | Hit rates at the energy level vs the 2 Å cluster level differ sharply, because a cluster spans tens of nats of unconverged energies. Both depend on the decoder budget. T4 idealises one energy per basin with the marker "E(Φ(x₀)) ≤ t", so its p_hit should be checked against the energy-level rate. That does not affect T4's hardware-gate kill, which holds for any p_hit. Converged decodes and a larger R are needed (G1). | PILOT; flag to T4/G1 |
| G-14 | The distance between π_T of a discretised register and the continuous posterior (bin volume, within-cell variation, Jacobians) is uncontrolled here (§4 N4). | Handed to T2 |
| G-15 | General convex Φ on an implicit register (the (c1) row of Theorem 3; QX-23's robust and joint CVaR) has no specification-problem reduction. | Open |

---

## 9. Response to review

Most objections were accepted as stated (§10). These were accepted only in part, with the reason.

- **R-1. The R64 test file vs the R256 census file (skeptic B, objection B5).** *Accepted:* the test-file numbers are superseded, and N2 and N3 are recomputed from the census. *Not accepted:* the inferred cause, "a change in the energy or initialisation between runs". The evidence points elsewhere:
  - **No energy change.** `src/qapf/protein/energy.py` (23:15), `src/qapf/sampling/hrex.py` (23:30) and `data/instruments/ladder/5O37A_45.npz` (23:16) all predate both files (test 23:33, census 23:40, 2026-09-26). The uncommitted change in `src/qapf/governor.py` only alters job-scheduling thresholds.
  - **What did change.** `scripts/g1_mode_census.py` was saved at 23:34, between the two runs. It dropped the Laplace masses (`laplace_mass` exists only in the test file) and added `p_hit_best_mode` and `frac_within_dE`.
  - **The seeds are not nested.** `ExactPrior.sample(n, rng)` draws each residue's uniforms as vectors of length n, so the 64- and 256-restart streams share almost no initial states.
  - **The "missing 22% mode" follows from the clustering.** Modes are greedy 2 Å clusters built in energy order, reporting their lowest member's energy. The test run's best cluster (14/64 = 22%, 2.81 Å from the native) and the census's best cluster (46/256 = 18%, 2.67 Å) are consistent with being the same structural region. So are the second clusters (8/64 vs 16/256; 3.60 vs 3.49 Å). In the census, one restart reached 3790.69 inside that region. Only 1 of 256 restarts lies within 20 nats of that energy, so no separate mode near 3819.97 should be expected.

  The remedy the skeptic asked for is adopted. The diagnosis is replaced by this one, which is INFERENCE: without stored coordinates, the identity of the two regions is not proved.
- **R-2. Store every mode size in the census JSON (B3).** *Accepted* as the diagnosis: the column is corrected, per-chain values are in the check output, and the bug is recorded (G-11). *Not done here:* changing `scripts/g1_mode_census.py`. That script belongs to the running G1 census (L = 120 and 150 are queued), and changing its output mid-run would make the files inconsistent. The bounds computed from n_modes are tight enough for every use in this note.
- **R-3. Add QHD and arXiv 2311.00811 to the bibliography (B7).** *Accepted* in the note: both abstracts were verified on arXiv, and they are cited as [T1-1] and [T1-2] in B5, Q5, §5 and G-12. *Deferred:* the `BIBLIOGRAPHY.md` entry, because key assignment and verification columns follow the literature phase's scheme. T4 uses the same convention for its [T4-n] keys.
- **R-4. "Beyond 80 aa" (skeptic A, objection A7).** *Accepted:* the old sentence rested on a premise contradicted by the unloaded timing, and it is withdrawn. *Amended:* the replacement adds that the census's own loaded timings grow about as L² over L = 30–100, which keeps the pair-scaled threshold roughly flat. Both readings are now stated. Neither lets the threshold fall with L.
- **R-5. "Near-degenerate optima place real pipelines in Proposition 4(3)" (B11).** *Accepted:* the gap distribution is reported, the "tens of nats" figure is qualified, and conditioning is added to Q5. *Amended:* T1's reproduction statement for an **exact** OPT is unaffected by near-degeneracy. What changes is that the specified output is ill-conditioned, and that any non-exact solver is in the Proposition 4 regime.
- **R-6. "Rerun with converged decodes and a larger R before inferring anything" (B4 (iv)).** *Accepted* as a requirement and recorded as G-13. This note runs no experiments, so the rerun is handed to G1. N2's conclusion is downgraded in the meantime.
- **R-7. Split H-001 (B1).** *Accepted* in full in §7. `research/HYPOTHESES.md` is the registry's file and is not edited by this note, so §7 gives the recommended status for the registry owner.
- **R-8. "Report the gap as ≈ 3 orders (2.9–3.3)" (A5).** *Accepted* with the census as it now stands. L = 100 is complete and its gap is 10^2.40, so N2 reports 2.4–3.3 orders.

---

## 10. Review log

Skeptic A's objections are A1–A19 and skeptic B's are B1–B20, in the order received. "Accepted" means the fix was made as proposed or equivalently. §9 gives the reasons wherever the resolution differs.

| # | Location | Objection (short) | Resolution | Where now |
|---|---|---|---|---|
| A1 | §3.6 α = 1; C3; `pstar` | "s* → ∞" false for finite E: argmax g = [E_max, ∞) | Accepted. Corrected statement; the code returns s* = E_max; plateau checked (4×10⁻¹⁵) | §1.8 C3, §3.6, C3 check |
| A2 | §3.6 tail law; Thm 2(b-wt); C3 check | Mass below s* is ≤ α, not = α; kinks have positive measure | Accepted. Reworded; kink example and 60 integer-level cells (20 strict) added; sandwich checked | §1.4, §3.6, C3 check |
| A3 | Lemma 2 | Unit mismatch; post-processing differs by readout; eigh case polynomial | Accepted. ratio ≤ 1 + C_post/(N·t_E); "no speedup of any size" limited to diagonal Õ(N) readouts | §1.5, §3.8 |
| A4 | D1, A8, C5, eigh row | N used as both 2ⁿ and the candidate count | Accepted. d_H and N_valid defined; C5 and eigh need d_H = poly(input) | §1.1, §2 A8, §1.8 C5, §1.5 |
| A5 | N2 median | "At least 3 orders" false at L = 60, 80; single-L t_C | Accepted. Per-L t_C, pair-scaled G_eval; gap 2.4–3.3 orders; rows in C6 | §4 N2; §9 R-8 |
| A6 | N2 resolution-limited; caveats | A point estimate treated as a bound; unseen mass not neutral | Accepted. Clopper–Pearson bound 1.0×10⁴; "not excluded" at base G_eval; conditional robustness; sentence deleted | §4 N2 |
| A7 | N2 beyond 80 aa | "Threshold moves little" contradicted by timings | Accepted with amendment | §4 N2; §9 R-4 |
| A8 | N3 Laplace | +19.5 nats is a clip-floor artifact | Accepted. Floor sensitivity shown for both files; "nevertheless" reading withdrawn; volume needed quantified (0.53 nats/dim) | §4 N3; C7 check |
| A9 | §3.3 "iff" | Unproved iff inside a ∎ proof | Accepted. Sufficient direction proved; criterion tagged INFERENCE and cited | §1.8 C1, §3.3 |
| A10 | D5(b), Thm 2(b), §3.5, Lemma 3 | λ* not unique under ties | Accepted. λ* is the stable greedy fill; m counts tied elements; Lemma 3 needs a lexicographic OPT or A4 | §1.1 D5, §3.5, §3.8 |
| A11 | Prop. 4(2) | Drops full support; "a constant rule reproduces the range" | Accepted. Qualifier added; "the family of rules" | §1.6 |
| A12 | Thm 2(a), S shots | Holds for the exact distribution only | Accepted. S-shot bound added and checked by Monte Carlo | §1.4, §3.4, C2 check |
| A13 | Thm 3 Φ_{α,T} row | αT missing; an exact method exists | Accepted. Both given; exact method implemented and checked | §1.5, §3.6, C3 check |
| A14 | C4, C7, C5 check | Missing hypotheses; c undefined; piecewise affine; the check assumed its claim | Accepted. Hypotheses added, c defined; the constrained solver is now differentiated; s* = min support over argmin, with proof | §1.8 C4/C7, §3.7, C5 check |
| A15 | §3.2 existence | Continuity fails when E = +∞ | Accepted. Lower semicontinuity argument | §3.2 |
| A16 | N1, N5, `s31 Q10` eigh ≈ 1 ms | Implausible at D = 512 | Accepted. Re-measured (check C8): eigh 64 ms, eigvalsh 37 ms at D = 512 | §4 N1, N5 |
| A17 | N2 census table; G-11 | Table stale | Accepted. Regenerated from 85 files; the census is still running | §4 N2, G-11 |
| A18 | §0, §1.5 | [C55, C56] cover OPT only; Lemma 3 tag missing in Thm 3 | Accepted. TOP_m lower-bound argument added; implicit (b-set) cell marked conditional on G-3 | §0, §1.5, §3.8 |
| A19 | N4 | T1's register is finite; the A80 energy is continuous | Accepted. Discretisation named; distance to the continuous posterior handed to T2 | §1.7, §4 N4, B8, G-14 |
| B1 | §7 H-001 status | Output equivalence ≠ cost equivalence; Dürr–Høyer is a query-model counterexample; kill criterion swapped | Accepted. H-001a/b split; pre-registered kill criterion restored | §0, §7; §9 R-7 |
| B2 | §7 routing statement | "Only live path" contradicts B2–B5, M3 | Accepted. Restated as "prioritised path"; open routes listed | §7, §5 |
| B3 | N2 unseen-mass column; census script | Singletons counted among the top 50 only | Accepted. Bounds from n_modes; per-chain values in the output; script change deferred | §4 N2, G-11; §9 R-2 |
| B4 | N2 inference | Survivorship; CP bound; median vs hardest; unconverged modes; M9 only | Accepted. Conclusion downgraded and scoped to M9; energy-level rate added; rerun handed to G1 | §4 N2, G-13; §9 R-6 |
| B5 | N3, A-N1 source file | Test file inconsistent with census; suspected energy/initialisation change | Remedy accepted; cause replaced (clustering, non-nested seeds, script edit; energy unchanged) | §4 N2, N3; §9 R-1 |
| B6 | A-N3 | "Quantum-generous" mislabel; R and S = 10³ missing | Accepted. Relabelled "Babbush 2021 baseline" after re-reading [B46]; R ∈ {1, 10, 100} and S = 10³ tabulated | §4 N2 |
| B7 | §0, Q5, B5 | Missing QHD line; the quadratic ceiling does not apply to structured E | Accepted. [T1-1, T1-2] verified and cited; Q5(i); G-12; bibliography entry deferred | §0, §1.9, §5, §6 B5; §9 R-3 |
| B8 | §0 CVX; Thm 3 (c1) | A convex program over an implicit simplex is not polynomial in general | Accepted. CVX polynomial only for explicit support; new (c1) row; QX-15 (explicit) and QX-23 (implicit) checked | §0, §1.5, G-15, §7 table |
| B9 | §7 QX coverage | Only 8 of 33 audited; implicit nulls are empirical | Accepted. Full QX-01…33 audit with checklist exits; claim restricted | §7 |
| B10 | Thm 2(b), N1, Prop. 4(2) | Full-support qualifier dropped | Accepted. Qualifier added; S29 exact-statevector evidence cited | §1.4, §1.6, §4 N1 |
| B11 | §4, §6, A4 | Near-degenerate optima are common | Accepted with amendment. Gap distribution; conditioning in Q5 | §4 N3, §1.9, B6; §9 R-5 |
| B12 | Thm 2 closing, §0 | "Zero bits" conflates information and computation | Accepted. Rephrased | §0, §1.4 |
| B13 | §5 combined scope | F37/F91 read selectively | Accepted. Both abstracts re-read and quoted; "argued against on average, not excluded" | §1.6, §5 |
| B14 | §7 H-009 M4 row | B71 misattributed | Accepted. [B46, C64] for break-even; [B71] for bias/mixing | §7 |
| B15 | G-2, §5 [C6], C2 | Closable now | Accepted. [C6] re-read; eqs. (11)–(12) and the §5 remark recorded; G-2 closed; C2 sufficiency attributed to [C6] | §1.8, §5, G-2 |
| B16 | C3 α = 1; D1 | Limit needed only with E = +∞; flat weight on invalid encodings | Accepted. Corrected; A9 added and checked | §1.8 C3, §2 A9, §3.6 |
| B17 | C5 | Ancillas ignored | Accepted. O(G·d_H·2^a) | §1.8 C5, §3.8 |
| B18 | Q4 | Explicit ≠ small; formula E keeps √N | Accepted. Q4 rephrased | §1.9 |
| B19 | §0 Λ | Λ implies a hardness it does not show | Accepted. Removed from §0; bottleneck caveat and the quadratic-FT caveat for SAMPLE added | §0, §4 N4 |
| B20 | H-009; category label | Clause (i) also refuted; category 6 used for a no-go | Accepted. Both clauses refuted; "category 6 (negative/no-go)"; G-10 kept open | header, §7, G-10 |
