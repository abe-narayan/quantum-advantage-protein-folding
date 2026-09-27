# T5: The quadratic ceiling for black-box protein-posterior sampling and estimation

_Theory note, 2026-09-26; revised 2026-09-27 after two skeptic reviews (see "Response to review" and "Review log" at the end). Workflow task T5; this file has a single writer. It covers no-go results for quantum speedups in sampling, search and estimation when an energy is accessed only through classical oracles, and the structural conditions a super-quadratic speedup would need._

_Citation keys such as [A45] resolve in `research/literature/BIBLIOGRAPHY.md`. Keys [X1]–[X25] were verified for this note on 2026-09-26/27 (arXiv API abstracts, Crossref metadata, or full text; see §5.2) and are **not yet** in the bibliography. Keys [T2-n] are verified in the sibling note `research/theory/PROOFS/T2_sampling_speedup_statement.md` §5.2. Pilot numbers come from `research/results/RAW/g1_pilot/*.json` and `*.npz`, `research/results/RAW/g1_modes_test/5O37A_45_R64_s0.json`, and the mode census `research/results/RAW/g1_modes/*_R256_s0.json` (a snapshot of 2026-09-27; files were still being written). They are labelled **PILOT** and are indicative only._

**Tags used on every claim.**
- **DERIVED**: proved in this note. A "proof sketch" is marked as one.
- **THEORETICAL**: proved in the cited literature.
- **INFERENCE**: argued here, not proved.
- **UNPROVEN**: open or conjectural.
- **REPORTED**: stated by the orchestrator's task text; not reproducible from any stored RAW file.

**Levels.** Each statement gives its *theoretical level* (what is proved, in which model) separately from its *practical level* (what it implies for wall-clock time on hardware). No repository file defines the program's L0–L6 scale. T2 and T4 use a working table (T4 header). Levels here are written out in words for the integrator to map (G9).

---

## 0. Summary

1. **On information-local (hide-and-seek) families whose background is classically easy, the quantum–classical separation is at most quadratic.**
   - *Lemma 1 (DERIVED).* Suppose a hidden region R_s carries posterior mass ≥ δ, and every answer of a pointwise oracle outside R_s is unchanged (M8). Then any quantum sampler needs T_Q ≥ (δ−ε−p_max)/(2√p_max) queries, and any classical sampler needs T_C ≥ (δ−ε)/p_max − 1. Here p_max is the largest prior probability that a given point lies in R_s.
   - Lemma 1 gives two *lower* bounds. A *ceiling* on the speedup also needs a classical upper bound O(1/p_max). That holds for uniform partitions with a fixed, known background, such as [A45]'s flat background. It fails when the background is itself classically hard (§3.1 Remark).
   - *Theorem A (DERIVED + THEORETICAL).* On the lattice sub-family F_M of Olivucci et al.'s hard family [A45] (M hiding places), the optimal costs are **T_Q = Θ(√M) and T_C = Θ(M)**. They are attained by Grover search over cell centres and by cell-by-cell search. The separation is exactly quadratic for every M, d and ramp ratio ϱ.
   - In terms of the barrier amplitude α: at constant patch mass, M = Θ(α(1−2ϱ)^d). In [A45]'s Theorem II.4 regime (ϱ = Θ(1/d)) this gives M = Θ(α), so the optimal quantum cost is Θ(√α). Amplified rejection sampling (S4) also attains it.
   - [A45]'s own general-purpose algorithm costs Õ(α^{1/2+s/d}·poly(d)) on the family. Their proven separation is Ω̃(α^{1/2−s/d}/poly(d)) for d > 2s [A45, Thm. II.4]. It is within α^{s/d}·poly(d) of optimal, which is poly(d)·e^{O(s)} only when log α = O(d).
   - An "exponential in d" ratio is still a quadratic polynomial relation between the two costs.
2. **Precision gains are capped at quadratic: Θ(1/ε) vs Θ(1/ε²).** This is derived here by a hybrid argument in the state-preparation model. The bound is within 2–3% of an explicit strategy for ε ≤ 0.01, and within 1.95% asymptotically (§4.4). The literature covers the sequence-oracle model [B16, B13] and the reflection model [B29]. (DERIVED + THEORETICAL)
3. **There is no universal quadratic ceiling for classical energies behind an oracle.**
   - *Proposition C1 (DERIVED, proof sketch).* It constructs a family of smooth energies on the torus (a "Simon trail"). Quantum Gibbs sampling costs **O(log α)** expected value queries, while every classical algorithm, even one given all derivatives, needs **Ω(√α)**.
   - Total Boolean functions admit super-quadratic separations: quartic for D vs Q [X2, X3], and R ≥ Q^{3−o(1)} for R vs Q [X9, X10]. R = O(Q³) is only conjectured.
   - Promise problems admit exponential separations [X5–X10] whose oracles are classical functions.
   - Simulating 2^n coupled classical oscillators with oracle-specified couplings gives an exponential query separation, and the problem is BQP-complete [X23].
   - A correct ceiling is therefore stated **per instance family, or as a worst case over a class**. It never follows from "the forward model is classical". (DERIVED + THEORETICAL)
4. **Routes to a super-quadratic speedup (non-exhaustive list):**
   - (i) leakage of the hard region's location that a quantum algorithm can read but a classical one cannot (algebraic hidden structure);
   - (ii) a quantum forward model;
   - (iii) planted structure between the information-theoretic and computational thresholds. The known speedups there are up to nearly quartic relative to the best *known* classical algorithm (Kikuchi) [C71, C72], and no ceiling is proved;
   - (iv) quantum data;
   - (v) white-box structure that a specialised quantum algorithm exploits: DQI [C73], short-path and jump-to-the-end [C69, C70], or BQP-complete linear/Hamiltonian dynamics of exponentially many classical degrees of freedom [X23];
   - or a change of cost measure (expected cost under a skewed prior).

   No protein-structure task examined has any of these in usable form (INFERENCE). **Whether the surviving lead's bottleneck is information-local is untested (G6).** Pair-distance energies encode the predicted structure in every pair term, which leaks the basin location globally. S1–S3 therefore do not apply without a new argument. If the hardness is intrinsic, it may be frustration or glassiness, a regime no proved ceiling covers (§3.7(e)).
5. **Numbers (PILOT; details in §4).**
   - At L = 45, β·(max E − min E) ≥ 396 nats over the full energy. T2 §4.1 bounds the pair-term range by ≥ 3.2×10³ nats. Every α-parameterised bound is **vacuous** here, which is automatic for any extensive energy. The substantive point is that α is the wrong hardness parameter for practical samplers.
   - For the five pilot runs, non-reversible PT theory for finite schedules predicts **27.5, 21.1, 4.5, 3.3 and 1.7** round trips [X20, Thm. 1 / Cor. 1]. The fine-mesh limit 1/(2+2Λ) gives only upper bounds. **Zero** were observed.
     - The deficit is significant at L = 45 and 60. It is not diagnostic at L ≥ 100, where the schedules were under-provisioned (swap rejection up to 0.89).
     - All runs are non-stationary. Open hypotheses: within-rung metastability (ELE violation), burn-in or under-exploration, and at L ≥ 100 swap communication as well. (INFERENCE, PILOT)
   - The first-order-like bottleneck at λ ≈ 0.4–0.5, and the finding that replicas from the prior "never penetrate", are **REPORTED**. The stored RAW files hold no replica-index traces. The stored data (smooth rung means, no variance peak) are consistent with, but do not demonstrate, such a bottleneck.
   - Babbush-form break-even at L = 45 (t_C = 0.59 ms): a quadratic speedup breaks even only if the best classical sampler needs **≳ 2.9×10⁶ evaluations per independent sample (1 µs Toffolis, one core)**, rising to 8×10²⁰ under surface-code assumptions [B46]. With one core per PT rung (S = 30) the optimistic figure is 2.6×10⁹. These are lower bounds on the break-even cost. T2's fuller model gives ≥ 2×10¹² (§4.5).
   - At L = 45 the pilot's whole production budget, 3.9×10⁵ evaluations, produced no round trip. That is an indication for **this NRPT configuration** (INFERENCE), not a bound on the best classical sampler. It lies below every threshold. The gap between the two is unmeasured.

### Statement table

| # | Statement (short) | Tag | Theoretical level | Practical level |
|---|---|---|---|---|
| S1 | Lemma 1: information-local hiding forces T_Q ≥ Ω(1/√p_max), T_C ≥ Ω(1/p_max) | DERIVED | unconditional query lower bound, any pointwise oracle satisfying M8, finite precision | none (lower bound on queries only) |
| S2 | Theorem A: on [A45]'s lattice sub-family F_M the optimal costs are T_Q = Θ(√M), T_C = Θ(M); equal to Θ(√α) vs Θ(α) when ϱ = O(1/d); [A45]'s algorithm is within α^{s/d}·poly(d) of optimal | DERIVED + THEORETICAL | unconditional, oracle model, worst case over the family | none; α-bounds vacuous for learned energies (§4.1) |
| S3 | Corollary A1: the same for ΔE oracles, walk operators, qsample preparation, mode finding, and estimation of basin observables | DERIVED | as S2 | none |
| S4 | Corollary A2: with an offset c of min E known, classical O(e^c α) vs quantum O(e^{c/2}√α) by rejection sampling, plain or amplified | DERIVED (upper bounds standard) + THEORETICAL | query model | none |
| S5 | Theorem B: estimation precision Θ(1/ε) quantum vs Θ(1/ε²) classical | DERIVED + THEORETICAL | unconditional, three oracle models; query ratio ≈ 27 at ε = 0.01 (§4.4) | none (a ≤ 100× query gain cannot offset per-call FT overhead under §4.5 assumptions) |
| S6 | Proposition C1: smooth energies with quantum O(log α) expected vs classical Ω(√α) Gibbs sampling | DERIVED (proof sketch) | unconditional, black-box, contrived family | none (no protein relevance claimed) |
| S7 | Total functions: D, R = O(Q⁴); quartic D-vs-Q and R ≥ Q^{3−o(1)} separations exist; R = O(Q³) conjectured | THEORETICAL | unconditional query | — |
| S8 | Promise problems: exponential separations with classical-function oracles | THEORETICAL | unconditional query (relativised) | — |
| S9 | Symmetric problems are polynomial; Aaronson–Ambainis conjecture open; random-oracle search and prior-weighted expected cost can be exponential | THEORETICAL / UNPROVEN | query | — |
| S10 | White-box energies: only conditional ceilings are possible (e.g., QSETH) | THEORETICAL + INFERENCE | conditional | — |
| S11 | Routes (R1)–(R5) to super-quadratic speedups (non-exhaustive); protein tasks lack them in usable form | INFERENCE | not a theorem | decisive for program strategy if G1 confirms |

---

## 1. Statements

**S1 (Lemma 1: hiding lemma; DERIVED).** Take the model of §2. Let {E_s}_{s∈S} be an energy family with prior D on S, a reference energy E_0 (not necessarily in the family) and regions R_s ⊆ X such that:
- (i) *information-locality:* every oracle answer (values and derivatives of every order the oracle returns, after b-bit rounding) of E_s equals that of E_0 at every x ∉ R_s (M8);
- (ii) *mass:* π_s(R_s) ≥ δ.

Let p_max := max_x Pr_{s∼D}[x ∈ R_s]. Consider any algorithm that, for every s, outputs a sample whose law is within total variation (TV) ε of π_s. Then:
- a **quantum** algorithm makes T_Q ≥ (δ − ε − p_max) / (2√p_max) queries;
- a **classical** randomised algorithm makes T_C ≥ (δ − ε)/p_max − 1 queries.

*Scope.* The lemma covers **pointwise** oracles, i.e. values and derivatives at the queried point, which satisfy M8. It does not cover oracles that return integrals, Fourier data, or intermediate partition functions.

**S2 (Theorem A: the optimal separation on [A45]'s lattice sub-family; DERIVED + THEORETICAL).** Let F_M be the sub-family of [A45]'s hide-and-seek family in which the hidden patch sits at one of M lattice positions (disjoint cells), with patch mass δ as in [A45, Prop. III.3].

*Lower bounds.* Take any quantum algorithm with coherent access to a pointwise oracle satisfying M8 (values, gradients, all higher derivatives, b-bit) that samples π_s to TV error ε < δ − 1/M. Then

  T_Q ≥ ((δ − ε − 1/M)/2) · √M ≥ c_{δ,ε} · √(T_C^{LB}),

where T_C^{LB} = M(δ − ε) − 1 is the classical lower bound [A45, Thm. III.1] (reproduced by Lemma 1).

*Upper bounds on F_M (DERIVED, standard).*
- **Quantum.** The patch core contains its cell centre, where E = min E; at every other cell centre E = max E. Run Grover search over the M cell centres, with 2 value queries per iterate (compute and uncompute the marking). Then sample offline from the member of the (known) family that has now been identified. This costs ≤ 2⌊π√M/4⌋ + 1 ≈ (π/2)√M value queries for near-certain success, or ≈ (π/3)√M for TV ⅛ at δ = ½ (§4.6).
- **Classical.** Query the cell centres one by one: ≤ M value queries.

*Hence* the optimal costs on F_M are **T_Q = Θ(√M) and T_C = Θ(M)**. The optimal separation is exactly quadratic for every M, d and ramp ratio ϱ.

*Conversion to α.* [A45, Prop. III.3] gives δ = (1+S)/(M+S) with S = (α−1)(1−2ϱ)^d, so at constant δ, M = Θ(α(1−2ϱ)^d).
- If ϱ = O(1/d), then M = Θ(α). The optimal quantum cost is Θ(√α), which amplified rejection sampling also attains (S4; min E is known on the family). [A45]'s Theorem II.4 is in this regime (INFERENCE from their stated formulas; constants not checked):
  - eq. (12) gives 1/ρ = Θ(d^{1+s}α^{1/d}log^s α);
  - Prop. III.3 gives ρ ∝ ν/(d^s log^s α) with ν ≤ ℓ/4;
  - ℓ = 2πM^{−1/d};
  - together these give ν = Θ(ℓ/d), i.e. ϱ = ν/ℓ = Θ(1/d).
- If ϱ is constant, M = α·e^{−Θ(d)}. The α-form bounds (Ω(√M) against O(√α) for rejection sampling) then differ by e^{Θ(d)}. The bounds stated in M, or in T_C^{LB}, remain tight.

*[A45]'s own algorithm (THEORETICAL).* By [A45, Thm. IV.3], N_q = Õ(√α · d^{1/2}(d+ξ)^s ρ^{−s} · polylog) gradient queries. On the hard family 1/ρ ≳ α^{1/d}, because the ramp satisfies ν ≤ ℓ/4 and ℓ = Θ(α^{−1/d}). So N_q = Õ(α^{1/2+s/d}·poly(d)·polylog α). Their stated separation is N_cl/N_q = Ω̃(α^{1/2−s/d}/poly(d)), for s > 1, d > 2s and log α = Ω(d) [A45, Thm. II.4, eq. (14)].
- The algorithm is general-purpose: it serves the whole class and does not know the lattice.
- On F_M it is within a factor α^{s/d}·poly(d)·polylog of optimal. That factor is poly(d)·e^{O(s)} when log α = O(d). The algorithm is not tight when log α = ω(d).
- Over the whole class, the worst-case optimal quantum cost lies between Ω(√α) (via F_M, when ϱ = O(1/d)) and [A45]'s Õ(α^{1/2+s/d}·poly(d)).

**S3 (Corollary A1: other oracles and tasks; DERIVED).** S2's lower bound still holds, with the constant divided by k, when each call of the algorithm's primitive can be simulated by at most k calls to the energy oracle:
- ΔE oracles: k = 4 under M3's XOR convention (compute E(x) and E(x′), write the difference, uncompute both). k = 2 under an additive-output convention, which also satisfies M8;
- a Metropolis/Szegedy walk operator W built from local energy evaluations: k = c_W;
- Boltzmann-coin rotations: k = 2.

It also holds for:
- (a) preparing the coherent sample |√π_s⟩, since measuring it samples;
- (b) finding the dominant basin (outputting a point of R_s with probability ≥ 2/3): T_Q = Ω(√M);
- (c) estimating E_{π_s}[g] to additive error < (2δ−1)/2 (this needs δ > ½) for an observable g that separates two halves of the patch lattice: T_Q ≥ (1/12)·√(M/2).

**S4 (Corollary A2: what the separation is; DERIVED, upper bounds standard).** Suppose a lower bound E_lb ≤ min E is known with β(max E − E_lb) ≤ ln α + c for some c ≥ 0. Then, on any grid discretisation:
- classical rejection sampling from the uniform law uses O(e^c·α) expected value queries;
- amplitude-amplified rejection sampling (BBHT exponential search [X16]; cf. quantum rejection sampling [A36]) uses O(e^{c/2}·√α) expected value queries.

On [A45]'s family min E is known (c = 0). So when ϱ = O(1/d), the optimal classical Θ(α) and quantum Θ(√α) are both attained by rejection sampling, plain or amplified. The provable separation is a Grover speedup of rejection sampling, and S2 shows nothing better is possible on that family.

**S5 (Theorem B: precision ceiling; DERIVED + THEORETICAL).**
- (B1, DERIVED) *State-preparation model.* The algorithm may use U, U† and controlled-U, where U|0⟩ = √(1−p)|0⟩|φ_0⟩ + √p|1⟩|φ_1⟩. Any quantum algorithm that distinguishes p = ½ + ε from p = ½ − ε with success ≥ 2/3 uses at least (1/3)/|θ(½+ε) − θ(½−ε)| ≈ 1/(6ε) calls, where θ(p) = arcsin √p. In particular this holds for any estimator of p with error ε′ < ε. Classically, n i.i.d. samples need n = Ω(1/ε²).
- (B2, THEORETICAL) *Sequence model:* Ω(min{1/ε, n}) queries for the mean of n numbers [B16]; the matching algorithms are optimal [B13, B19]. *Reflection model:* Ω(1/ε) reflections for partition-function estimation [B29]. The classical rate is Θ(σ²/ε²) [B12].
- (B3, THEORETICAL) For smooth integrands the quantum gain shrinks as smoothness grows, because classical rules already beat 1/ε² [B15].
- **Consequence.** Every quantum speedup in estimation *precision* is at most quadratic, in every standard black-box model.

**S6 (Proposition C1: no universal ceiling for smooth classical energies; DERIVED, proof sketch).** For every n ≥ 2 there is a family {E_{f,s}} of C^∞ energies on 𝕋^n with the following properties:
- the energies are built from compactly supported Gevrey bumps of the kind [A45] uses;
- the barrier amplitude is α ∈ [e^{βΔ}, e^{0.1}·e^{βΔ}] = Θ(2^n);
- β·max|E| = O(n);
- the needle slot A_s (the support of ψ_{A_s}) carries posterior mass ≥ ½.

On this family:
- a quantum algorithm samples π_{f,s} with **O(n) = O(log α) value queries in expectation**, at oracle precision b = n + O(log(Δ/η)) bits.
  - It is Las Vegas: Simon's algorithm with verification and repetition, then rejection with ≤ e^{0.1} expected proposals.
  - Its output law is exact up to oracle-rounding error O(β·2^{−b}·(Δ+η)) in TV.
  - Markov's inequality turns the expected bound into a worst-case, bounded-error O(n) bound, so the separation is unchanged.
- every classical algorithm, even one querying all derivatives, needs **Ω(2^{n/2}) = Ω(√α)** queries to sample at TV error ≤ ¼.

The family violates information-locality: the needle's location is encoded in tiny, Simon-structured energy variations that span the whole domain.

**S7 (Total functions; THEORETICAL).**
- If the oracle's truth table is arbitrary (no promise), every Boolean function of it satisfies D(f) = O(Q(f)⁴) [X2], improving O(Q⁶) [X1]. Hence R(f) = O(Q(f)⁴).
- **Best known separations.**
  - D vs Q: quartic [X3], so O(Q⁴) is tight for D.
  - R vs Q: power 2.5 [X4], improved to 8/3 by Tal (as reported in [X10]; not read here), and then to R(f) ≥ Q(f)^{3−o(1)} [X9, Cor. 1.5; X10, Thm. 1.5].
  - R = O(Q³) is conjectured by Aaronson, Ben-David, Kothari, Rao and Tal [X2] (as stated in [X9, X10]).
- **Quadratic is therefore not the ceiling even for total functions.** The proven ceiling is quartic and is attained for D vs Q. For R vs Q the truth lies between cubic, attained up to o(1) in the exponent, and quartic. The ceiling is exactly quadratic for OR-type questions such as "is there x with E(x) < E₀?" [C55, X15].

**S8 (Promise problems; THEORETICAL).** Exponential query separations exist where the oracle is a classical function:
- Simon's problem [X5];
- period finding [X6];
- glued-trees traversal [X7];
- Forrelation, 1 query vs Ω̃(√N) [X8];
- k-Forrelation, O(1) vs Ω̃(N^{1−ε}), which is optimal [X9, X10];
- the dynamics of 2^n coupled classical oscillators with oracle-given couplings: poly(n) quantum vs 2^{Ω(n)} classical queries; BQP-complete when the oracles are circuits [X23].

In instantiations such as modular exponentiation [X6] the oracle is an efficient classical circuit. **"The forward model is a classical circuit" does not imply "at most a polynomial speedup."**

**S9 (Symmetry, random oracles, cost measure; THEORETICAL / UNPROVEN).**
- For problems invariant under permuting inputs and outputs, Q ≥ R^{1/7} up to polylog [X11], and R = O(Q³) for a more general symmetric class [X12]. (THEORETICAL)
- The Aaronson–Ambainis conjecture implies that every T-query quantum algorithm can be simulated on most inputs by a poly(T)-query classical algorithm [X11]. It is **UNPROVEN**.
- Relative to a random oracle, NP *search* problems with exponential quantum speedups exist [X13]. The structure there lives in the task (a code-based relation), not in the oracle. (THEORETICAL)
- For unstructured search with a *prior* over the marked location, the *expected* quantum query count can be exponentially smaller than the classical one for some priors, e.g., certain power laws [X14]. (THEORETICAL)
- **The ceiling depends on the cost measure.** S1–S3 bound worst-case, bounded-error cost.

**S10 (White-box energies; THEORETICAL + INFERENCE).**
- Query lower bounds are statements about *families*. A single fixed energy given as source code has trivial query complexity (the answer can be hard-coded).
- Under standard assumptions, white-box classical functions admit exponential speedups (factoring [X6]).
- White-box ceilings can only be *conditional*. The QSETH framework converts quantum query lower bounds into conditional quantum time lower bounds [X22]. (THEORETICAL)
- An unconditional white-box quadratic ceiling for learned-energy sampling would need lower bounds against quantum circuits, far beyond current techniques. (INFERENCE)

**S11 (Routes to super-quadratic speedups; INFERENCE; the list is not exhaustive).** A super-quadratic quantum speedup for a sampling, search or estimation task over an energy is known to arise from at least one of:
- (R1) the family is *not* information-local, and its leakage about the hard region can be read by quantum but not by classical algorithms (algebraic hidden structure: hidden subgroup, period, Fourier correlation, codes);
- (R2) a quantum forward model, i.e., an oracle that is itself a quantum process with no efficient classical simulation;
- (R3) planted structure between the information-theoretic and computational thresholds, of kXOR/tensor type. The known speedups are up to nearly quartic relative to the best known classical algorithm (Kikuchi) [C71, C72]; no upper limit on planted-inference speedups is known;
- (R4) quantum input data [X18];
- (R5) white-box structure exploited by a specialised algorithm:
  - DQI on algebraic (Reed–Solomon-decodable) problems [C73];
  - short-path / jump-to-the-end on Ising-type costs, 2^{(0.5−c)n} with small c, which is super-Grover but still exponential [C69, C70];
  - BQP-complete linear or Hamiltonian dynamics of exponentially many classical degrees of freedom [X23];
- or a change of cost measure (expected cost under a skewed prior, S9).

The protein tasks examined in §3.8 lack (R1)–(R5) in usable form. Hardness that comes from frustration or glassiness with no hiding (§3.7(e)) is covered by none of S1–S3 and by no route above. For that regime neither a ceiling nor a speedup is established.

---

## 2. Model and assumptions

- **M1. Configuration space.** X is either 𝕋^d (the [A45] setting) or a finite set.
  - Internal-coordinate protein models are close to the torus: torsions τ ∈ 𝕋^L. Bond angles θ ∈ [0, π] are not periodic.
  - Quantum registers hold grid points of a discretisation G_h ⊂ X with b_x bits per coordinate. Lower bounds are proved on G_h, so any grid algorithm is covered.
- **M2. Targets.** π_s(x) ∝ exp(−βE_s(x)). α(E) := exp(β(max E − min E)), as in [A45] (Definition II.3).
- **M3. Quantum oracles.** O_E^{(k)} : |x⟩|y⟩ ↦ |x⟩|y ⊕ ⌊D^{≤k}E(x)⌉_b⟩. The output is all partial derivatives of order ≤ k, with deterministic rounding to b bits.
  - k = 0 is the value oracle; k = 1 adds the gradient oracle of [A45].
  - The algorithm may use controlled and inverse oracles, arbitrary ancillas and free non-query unitaries. This is generous to quantum, which is the right direction for lower bounds.
  - Derived primitives count as k calls:
    - ΔE(x, x′): k = 4 under the XOR convention above (compute E(x) and E(x′), write the difference, uncompute both). k = 2 under an additive convention |y⟩ ↦ |y + E(x) mod 2^b⟩, where O_E and O_E^{−1} accumulate E(x) − E(x′) directly;
    - Boltzmann-coin rotation (compute E, rotate, uncompute): k = 2;
    - a walk step W_P of a local Metropolis or Szegedy chain: k = c_W, with c_W = O(1) for the constructions in [A55, B33] (INFERENCE).
- **M4. Classical algorithms.** Adaptive, randomised, with the **same** oracles including derivatives of all orders. This matches [A45]'s classical model and is generous to classical, which is the right direction for the classical lower bound.
- **M5. Tasks.**
  - SAMPLE(ε): output x with law Q, TV(Q, π_s) ≤ ε.
  - QSAMPLE(ε): prepare a state within ε of |√π_s⟩.
  - FIND: output a point of R_s with probability ≥ 2/3.
  - ESTIMATE(ε): output E_{π_s}[g] ± ε with probability ≥ 2/3.
- **M6. Cost.** The number of oracle calls, worst case over the family, at bounded error. **Query complexity is not runtime.** Lower bounds on queries lower-bound runtime, because each call costs at least one step. Upper bounds on queries say nothing about runtime (see §4.5).
- **M7. Estimation oracle models.**
  - (i) State-preparation unitary U, with U, U† and controlled-U [B12, B19].
  - (ii) Value oracle on a sequence [B16].
  - (iii) Reflection/walk operators [B29].
- **M8. Information-locality** (the hypothesis of S1). O_{E_s}(x) = O_{E_0}(x) for all x ∉ R_s, *after rounding*.
  - Compactly supported (Gevrey, s > 1) bumps satisfy this exactly.
  - [A45] notes that analytic potentials (s ≤ 1) cannot hide a well from an infinite-precision oracle that returns all derivatives.
  - Deterministic b-bit rounding does **not** hide an analytic well automatically. Any nonzero perturbation flips ⌊·⌉_b wherever the unperturbed answer lies within the perturbation of a rounding threshold. For analytic tails, Cauchy estimates make high derivatives larger than the value.
  - *Sufficient condition (DERIVED).* M8 holds if (a) every returned derivative of E_s − E_0 of order ≤ k is below half an ulp outside R_s, and (b) every returned value and derivative of E_0 lies at least half an ulp from every rounding boundary. Condition (b) is automatic for a flat E_0 with an exactly representable value.
  - *General fallback (DERIVED).* Enlarge the hiding region to R′_s := R_s ∪ {x ∉ R_s : O_{E_s}(x) ≠ O_{E_0}(x)} and apply Lemma 1 with p′_max computed over R′_s. The proof uses M8 only on the complement, so it goes through unchanged. For analytic wells R′_s may spread over the domain and make p′_max large. An approximate-locality version with randomised rounding is not done here.
  - Hiding is therefore a property of the *oracle precision* as well as of smoothness.

---

## 3. Proofs and derivations

### 3.1 Proof of Lemma 1 (S1)

*Quantum part.* This is the BBBV hybrid argument [C55] adapted to sampling outputs; no novelty is claimed. Purify the algorithm, so it is unitaries V_0, O, V_1, …, O, V_T followed by a measurement. Let |φ_t⟩ be the state just before the t-th query in the run with O_{E_0}. Let m_t(x) := ‖(|x⟩⟨x| ⊗ I)|φ_t⟩‖², so Σ_x m_t(x) = 1. Let |ψ_s⟩ and |ψ_0⟩ be the final states with oracles O_{E_s} and O_{E_0}.

1. By M8, O_{E_s} and O_{E_0} agree on span{|x⟩ : x ∉ R_s} ⊗ (everything else). So ‖(O_{E_s} − O_{E_0})|φ_t⟩‖ ≤ 2‖Π_{R_s}|φ_t⟩‖ = 2√(m_t(R_s)).
2. By the telescoping (hybrid) argument, ‖ψ_s − ψ_0‖ ≤ Σ_t 2√(m_t(R_s)). Cauchy–Schwarz then gives ‖ψ_s − ψ_0‖ ≤ 2√(T·Σ_t m_t(R_s)).
3. Average over s ∼ D, using Jensen for √:

   E_s‖ψ_s − ψ_0‖ ≤ 2√(T·E_s Σ_t m_t(R_s)).

   Here E_s Σ_t m_t(R_s) = Σ_t Σ_x m_t(x)·Pr_s[x ∈ R_s] ≤ T·p_max. Hence E_s‖ψ_s − ψ_0‖ ≤ 2T√p_max.
4. Let Q_s and Q_0 be the output laws. For pure states, TV(Q_s, Q_0) ≤ trace distance = √(1−|⟨ψ_s|ψ_0⟩|²) ≤ ‖ψ_s − ψ_0‖. The last inequality holds because 1 − c² ≤ 2(1−c) ≤ ‖ψ_s−ψ_0‖² for c = |⟨ψ_s|ψ_0⟩|.
5. Correctness gives Q_s(R_s) ≥ π_s(R_s) − ε ≥ δ − ε. Also Q_s(R_s) ≤ Q_0(R_s) + ‖ψ_s − ψ_0‖, and E_s Q_0(R_s) = Σ_x Q_0(x) Pr_s[x∈R_s] ≤ p_max. Averaging:

   δ − ε ≤ p_max + 2T√p_max, so T ≥ (δ − ε − p_max)/(2√p_max). ∎

*Classical part.* Fix a deterministic decision tree; a randomised algorithm is a mixture of trees and the bound is uniform. Run the tree on E_0: it queries x_1,…,x_T and outputs x̂_0. On E_s its transcript is identical unless some x_i ∈ R_s, which happens with probability ≤ T·p_max over s. So δ − ε ≤ E_s Q_s(R_s) ≤ p_max + T·p_max, which gives T ≥ (δ−ε)/p_max − 1. ∎

**Remark: lower bounds versus a ceiling (DERIVED).** Up to constants, T_Q ≥ √(T_C^{LB}) on every information-local family. This relates two *lower* bounds. A statement about the *speedup* also needs a classical *upper* bound of order 1/p_max.
- **The upper bound holds** when D is uniform over a partition into M cells and the background E_0 and patch profiles are fixed and known. The classical algorithm queries cell by cell, then samples offline, or it uses rejection sampling (S4).
- **It fails when the background is classically hard.** Example: superimpose information-local wells, M hiding places, on a Simon-trail background (§3.5) whose Simon function f is a second hidden parameter.
  - For each fixed f the s-sub-family is information-local, so T_Q = Ω(√M).
  - Classical algorithms must also pay Ω(2^{n/2}) to learn f, while quantum ones pay O(n).
  - The separation is super-quadratic when M ≪ 2^n.
- **Non-uniform priors.** The speedup in *expected* cost can exceed quadratic [X14].
- S1 bounds worst-case, bounded-error cost only, and only for pointwise oracles satisfying M8.

### 3.2 Proof of Theorem A (S2)

**Facts taken from [A45].** Read via arXiv HTML fetch on 2026-09-26 and re-read on 2026-09-27 (Definition III.2, Proposition III.3, Theorem III.1, Theorem II.4, Theorem IV.3):
- the hard family places a flat background on 𝕋^d;
- a smooth patch of side ℓ carries mass δ = (1+S)/(M+S), with S = (α−1)(1−2ϱ)^d, ϱ = ν/ℓ, ramp width 0 < ν ≤ ℓ/4, and M = (2π/ℓ)^d possible positions;
- the patch is built from mollified (Gevrey, compactly supported) step functions, with Gevrey radius ρ_E = 𝔯_t·ν/(2d^s(log α)^s) (Prop. III.3);
- the classical lower bound comes from "M(δ−ε)−1 patches must be searched". Thm. II.4, eq. (13): N_cl ≥ (1−2ε₀)(α−1)/16;
- Thm. II.4, eqs. (12) and (14): 1/ρ_{α,d} = Θ(d^{1+s}α^{1/d}log^s α), and N_cl/N_q = Ω̃(α^{1/2−s/d}/(d^{1/2+(2+s)s}·log^{s+1}(1/ε))), for s > 1, d > 2s, log α = Ω(d);
- Thm. IV.3: N_q = Õ(√α · d^{1/2}(d+ξ)^s ρ^{−s} · polylog).

**The proof.**
1. **Sub-family.** Restrict to the M lattice positions, with patch s occupying cell s of a partition of 𝕋^d into M congruent cells. A worst-case lower bound on a sub-family is a lower bound on the family.
2. **Hypotheses of Lemma 1.** Take R_s = interior of cell s. E_s equals the flat E_0 outside R_s, including all derivatives, because the bump's support lies inside the cell. With a flat, exactly representable E_0 this also holds after rounding (M8). Also π_s(R_s) ≥ δ, and p_max = 1/M for s uniform.
3. **Apply Lemma 1:** T_Q ≥ (δ − ε − 1/M)√M/2. For δ = ½ and ε = ⅛: T_Q ≥ 0.19√M − o(1).
4. **Relation to the classical bound.** T_C^{LB} = M(δ−ε) − 1, so M = (T_C^{LB}+1)/(δ−ε). Hence T_Q ≥ ((δ−ε−1/M)/(2√(δ−ε)))·√(T_C^{LB}+1).
5. **Matching upper bounds on F_M.** The patch core, where E = min E, contains the cell centre, and E = max E at every other cell centre. So f(c) := [E(centre_c) = min E] is a search oracle costing 1 value query, or 2 when coherent (compute, uncompute).
   - Grover search over the M centres finds s with ≈ (π/4)√M iterates, i.e. ≈ (π/2)√M value queries, plus 1 classical check.
   - The algorithm knows the family, so once s is known it samples π_s offline with no further queries.
   - Classically, querying centres one by one costs ≤ M.
   - So T_Q = Θ(√M) and T_C = Θ(M) on F_M, for every d and ϱ.
6. **Conversion to α and comparison with [A45]'s algorithm.** This is as stated in S2. The ρ^{−s} factor of Thm. IV.3 cannot be constant on the family: ν ≤ ℓ/4 and ℓ = 2πM^{−1/d} = Θ(α^{−1/d}) force 1/ρ ≳ α^{1/d}, in agreement with eq. (12). ∎

**Alternative proof by direct reduction from search (DERIVED).** Let f(c) = [c = s] be an unstructured-search oracle over M cells. Energy-oracle answers at x ∈ cell c are a fixed function of (x, f(c)): if f(c) = 1, add the patch profile at its known relative position. So one energy query costs 2 queries to f (compute, then uncompute).

A sampler with TV error ε lands in cell s with probability ≥ δ − ε. Checking the cell costs 1 more query. Repeating r = O(1/(δ−ε)) times finds s with probability ≥ 2/3. This gives a search algorithm using r(2T_Q + 1) queries to f. Search needs Ω(√M) queries [C55]; the exact constant π/4·√M for near-certain success is [X15], building on [X16]. So T_Q = Ω((δ−ε)√M) again.

**Relevance of "exponential in d" (DERIVED).** [A45] says the advantage "becomes exponential in the dimension, e^{Ω(d)}, at low temperature". Their proven ratio is α^{1/2−s/d} with log α = Ω(d). The optimal ratio on F_M is Θ(√M). Classical and quantum costs remain related polynomially: T_Q = Θ(T_C^{1/2}) optimally. An exponential gap in a *parameter* is not a super-quadratic *speedup*.

### 3.3 Corollaries A1 and A2 (S3, S4)

- **Other primitives (DERIVED).** If each primitive call can be simulated with k energy-oracle calls, a T-call algorithm gives a kT-query algorithm, so the primitive count is ≥ T_Q^{LB}/k. This covers:
  - ΔE: k = 4 with the XOR oracle, k = 2 with the additive oracle, which also satisfies M8;
  - Boltzmann coins: k = 2;
  - local Metropolis/Szegedy walk operators (M3).

  Quantum walk *steps* on hide-and-seek families therefore cannot beat Ω(√M)/c_W.
- **QSAMPLE ⇒ SAMPLE** by measurement, so the bound transfers.
- **FIND** is the search problem itself.
- **ESTIMATE of a basin observable (DERIVED).**
  - Split the M cells into halves H_L and H_R, and take g = 1[x ∈ ∪_{c∈H_L} cell c].
  - Then E_{π_s}[g] ≥ δ if s ∈ H_L and ≤ 1−δ if s ∈ H_R. With δ > ½, an estimate within (2δ−1)/2 decides the half with success ≥ 2/3.
  - Run the hybrid argument of §3.1 separately for s uniform in H_L and in H_R, where p_max = 2/M. The two output-bit probabilities must differ by ≥ ⅓ on average, and each differs from the E_0 value by ≤ 2T√(2/M) on average.
  - So ⅓ ≤ 4T√(2/M), which gives T ≥ (1/12)√(M/2).
- **Mixing-time phrasing (INFERENCE).**
  - If the best local chain on F_M has spectral gap δ_gap = Θ̃(1/M), then T_Q = Ω̃(1/√δ_gap) on F_M. The quadratic gap improvement of Szegedy walks [A1] and quantum simulated annealing [A8] would then be optimal *on this family*. I have not computed δ_gap(M) for [A45]'s construction (gap G3).
  - A lower bound of Ω(1/√δ_gap) for *every* chain is **false**: a chain can mix slowly on a distribution that is easy to sample directly.
  - Related literature: quantum walks are at most polynomially faster at mixing [A12]; gap amplification is at most quadratic in the frustration-free black-box setting [A33]; there is no generic speedup for worst-case unstructured QeMCMC [A48].
- **S4 upper bounds (DERIVED, standard).** Weight w(x) = exp(−β(E(x) − E_lb)) ≤ 1. The acceptance probability under the uniform law on G_h is p_acc = mean_x w(x) ≥ exp(−β(max E − E_lb)) ≥ e^{−c}/α.
  - Classical rejection sampling: expected 1/p_acc ≤ e^c·α value queries.
  - Quantum: prepare the uniform superposition over G_h, rotate an ancilla by arcsin √w(x) (2 value queries), and amplify the accept branch with BBHT exponential search, since p_acc is unknown [X16]. This costs an expected O(1/√p_acc) = O(e^{c/2}√α) value queries.
  - Measuring gives a sample from the grid Gibbs law, exact up to oracle rounding. The discretisation error is controlled by the Lipschitz constant of βE and the grid spacing. The number of grid points enters only the qubit count, not the query count.
  - On [A45]'s family min E is known, so c = 0.

### 3.4 Proof of Theorem B1 (S5)

Let R(θ) be the real rotation with R(θ)|0⟩ = cos θ|0⟩ + sin θ|1⟩, so p = sin²θ. Put θ_± = arcsin √(½ ± ε). Any estimator with error ε′ < ε distinguishes p_+ from p_−. (With error exactly ε the two intervals touch, so the strict inequality is needed.) Replace every use of R(θ_+) by R(θ_−), including U†, controlled-U and ancilla-tensored versions, which have the same operator-norm difference.

‖R(θ_+) − R(θ_−)‖ = |e^{i(θ_+−θ_−)} − 1| = 2|sin((θ_+−θ_−)/2)| ≤ |θ_+ − θ_−|. By the hybrid argument, the final states differ in norm by ≤ T|θ_+ − θ_−|. Success ≥ 2/3 needs trace distance ≥ ⅓, so T ≥ (1/3)/|θ_+ − θ_−|. Since dθ/dp = 1/(2√(p(1−p))) = 1 at p = ½, |θ_+ − θ_−| = 2ε + O(ε³), which gives T ≥ 1/(6ε)·(1 − O(ε²)).

Classically, n i.i.d. Bernoulli samples distinguish p_± only if n·KL(p_+‖p_−) = Ω(1). KL = 2ε·ln((½+ε)/(½−ε)) = 8ε² + O(ε⁴), so n = Ω(1/ε²).

The numerical check in §4.4 puts the quantum bound within 2–3% of an explicit Grover-iterate strategy for ε ≤ 0.01. Asymptotically the explicit strategy needs asin(1/3)/(2ε) ≈ 0.1699/ε calls against the 1/(6ε) bound, a ratio of 3·asin(1/3) ≈ 1.0195. ∎

**Joint cost (UNPROVEN).** For posterior expectations the literature's upper bounds combine the two resources: Õ(√τ/ε) quantum vs Õ(τ/ε²) classical [B12, B26, B28]. The lower bounds proved here and in [B29] are *separate*: Ω(1/ε), and Ω(√M) on hide-and-seek families (§3.3). A joint lower bound Ω(√M/ε) is not proved here (gap G2).

### 3.5 Proof sketch of Proposition C1 (S6): the "Simon trail"

**Construction.**
1. *Geometry.* Take X = 𝕋^n = [0, 2π)^n, split into M = 2^n cubic cells C_c of side π, indexed by c ∈ {0,1}^n. In each cell choose two disjoint closed sub-cubes:
   - a *label slot* B_c = Π_i [πc_i, πc_i + πκ], with centre b_c;
   - a *needle slot* A_c = Π_i [πc_i + 2πκ, π(c_i+1) − πκ].

   With κ = 1/(3n) the needle slot fills a fraction (1 − 1/n)^n ≥ ¼ of the cell.
2. *Bumps.* ψ_A is a Gevrey-s bump (s > 1), equal to 1 on the inner part (core) of A_c (relative ramp ϱ = 1/(4n)) and supported in the interior of A_c. ψ_B is a Gevrey bump supported in the interior of B_c with ψ_B(b_c) = 1.
3. *Hidden data.* Let f: {0,1}^n → {0,1}^n satisfy Simon's promise: f(c) = f(c′) ⇔ c′ ∈ {c, c ⊕ s}, with s ≠ 0 [X5]. Let v(y) ∈ [0, 1) be the n-bit string y read as a binary fraction.
4. *Energy.*

   E_{f,s}(x) = Δ·(1 − ψ_{A_s}(x)) + η·Σ_c v(f(c))·ψ_{B_c}(x), with βη ≤ 0.1.

   So min E = 0 in the needle core and Δ ≤ max E < Δ + η, giving e^{βΔ} ≤ α ≤ e^{β(Δ+η)} ≤ e^{0.1}·e^{βΔ}.
5. *Needle mass.*
   - Let q := 2^{−n}(1−3κ)^n(1−2ϱ)^n be the volume fraction of the needle core, and choose e^{βΔ} = 1/q = Θ(2^n).
   - Outside A_s, E ≥ Δ. The weight there is ≤ (1 − vol(A_s))·e^{−βΔ} < q, while the core alone has weight q.
   - So the **needle slot A_s** (core plus ramp) carries mass > q/(q + q) = ½. The core alone can carry less than ½, because the background weight is ≈ (1 − vol(A_s))·q and the ramp adds more (≈ 0.48 at n = 2 for a typical ramp profile; the crude bounds guarantee only ≈ 0.36). Only the slot mass is used below.
   - α = Θ(2^n) = Θ(M).
   - To get core mass ≥ ½ instead, take e^{βΔ} = 2(1−2ϱ)^{−n}/q, which keeps α = Θ(2^n).

**Quantum upper bound: O(n) = O(log α) expected value queries.**
- At x = b_c only the label bump of cell c is nonzero, so E(b_c) = Δ + η·v(f(c)) exactly.
- A reversible circuit computes E(b_c) (1 query), extracts f(c) = 2^n (E−Δ)/η, XORs it into a register, and uncomputes (1 query). This needs oracle precision b ≥ n + log₂(Δ/η) + O(1).
- Simon's algorithm recovers s with O(n) expected f-queries [X5]. It uses O(n) expected repetitions to collect n−1 independent equations y·s = 0 over GF(2). Each candidate s is verified by checking f(0) = f(s) (2 more f-queries), with repetition on failure. The algorithm is Las Vegas.
- With s known, E′(x) := Δ(1 − ψ_{A_s}(x)) is known in closed form. Draw x from q′ ∝ e^{−βE′} (no queries; the normalising constant is computable offline to any precision). Accept with probability e^{−β(E−E′)(x)} ∈ (e^{−0.1}, 1], which costs 1 query.
- Accepted samples have law ∝ e^{−βE} up to the b-bit rounding of E used in the acceptance step. The TV error is O(β·2^{−b}·(Δ+η)). The expected number of proposals is ≤ e^{0.1}.
- Stopping at 3× the expected query count gives, by Markov's inequality, a worst-case O(n)-query algorithm with failure probability ≤ ⅓. The separation below is unchanged.

**Classical lower bound, Ω(2^{n/2}) = Ω(√α) (proof sketch after Simon [X5]).**
1. *Information per query.* The answer to any query in cell c (value and every derivative) is a function of (x, c, f(c), 1[c = s]). The needle and label bumps of cell c live inside C_c, and every bump vanishes with all its derivatives near the cell boundary.
2. *Transcript.* Take s uniform in {0,1}^n∖{0} and f uniform subject to the promise. Suppose the first t queried cells c_1,…,c_t show no collision (f(c_i) = f(c_j), i ≠ j) and no hit (c_i = s). Then s is uniform on {0,1}^n∖({0} ∪ {c_i} ∪ {c_i ⊕ c_j}), a set of size ≥ 2^n − 1 − t − t²/2. The next query creates a collision or a hit with probability ≤ (t+1)/(2^n − 1 − t − t²/2).
3. *Summing over T queries,* Pr[collision or hit] ≤ (T² + O(T))/(2^n − O(T²)).
4. *Output.* Without a collision or hit, the output lands in C_s with probability ≤ 1/(2^n − O(T²)). But correct sampling needs Pr[output ∈ A_s] ≥ ½ − ε ≥ ¼. Hence T = Ω(2^{n/2}). ∎ (sketch)

**Caveats.**
- The family is **contrived**. It encodes the address of the needle in exponentially small, algebraically structured energy variations. Nothing like it is claimed for any physical or learned energy.
- It lies in a Gevrey class with ramps of width Θ(1/n), the same scaling [A45]'s Theorem II.4 regime has (§3.2). I did **not** check membership in [A45]'s exact class with its constants (ρ, ξ); see gap G4.
- It does not contradict S2. The worst case over the class is still set by information-local sub-families. C1 shows that **per-family** separations inside the same smoothness class can be exponential.

### 3.6 What S7–S10 say, precisely

Quotations are from arXiv abstracts fetched 2026-09-26, or from full-text PDFs fetched 2026-09-27 where marked.
- **Total functions** [X1, X2, X3, X4, X9, X10]:
  - "the exponential quantum speed-up obtained for partial functions … cannot be obtained for any total function: … O(T^6)" [X1];
  - "D(f) = O(Q(f)^4) … This matches the known separation (up to log factors) due to Ambainis, Balodis, Belovs, Lee, Santha, and Smotrovs" [X2];
  - "total function with a super-quadratic gap between its quantum and deterministic query complexities" [X3];
  - "power 2.5 separation between bounded-error randomized and quantum query complexity for a total Boolean function, refuting the widely believed conjecture that the best such separation could only be quadratic (from Grover's algorithm)" [X4];
  - (full text) "Corollary 1.5. There exists an explicit total boolean function f for which R(f) ≥ Q(f)^{3−o(1)}. The recent work of Aaronson, Ben-David, Kothari, Rao and Tal [ABK+20] conjectures that for any total boolean function f, it always holds that R(f) = O(Q(f)^3)" [X9];
  - (full text) "This was improved by Tal [31] to R_{1/3}(f) ≥ Q_{1/3}(f)^{8/3−o(1)}. We give a polynomially stronger separation: Theorem 1.5. There is a function f : {−1, 1}^n → {0, 1} with R_{1/3}(f) ≥ Q_{1/3}(f)^{3−o(1)}" [X10].
- **Partial functions** [X7–X10, X23]:
  - glued trees: "an oracular … problem that can be solved exponentially faster on a quantum computer than on a classical computer" [X7];
  - Forrelation: "1 quantum query, yet … any randomized algorithm needs ~sqrt(N)/log(N) queries … this 1 versus ~sqrt(N) separation is optimal" [X8];
  - k-Forrelation: "an O_ε(1) vs Ω(N^{1−ε}) separation between bounded-error quantum and randomized query complexities" [X9], and "best possible" [X10];
  - coupled oscillators: for 2^n coupled classical oscillators, "any classical algorithm solving this same problem is inefficient and must make 2^{Ω(n)} queries to the oracle", and "when the oracles are instantiated by efficient quantum circuits, the problem is BQP-complete" [X23].
- **Symmetric problems and structure** [X11–X13]:
  - "for any problem that is invariant under permuting inputs and outputs … the quantum query complexity is at least the 7th root of the classical randomized query complexity". The conjecture that "every bounded low-degree polynomial has a 'highly influential' variable" implies "every T-query quantum algorithm can be simulated on most inputs by a poly(T)-query classical algorithm" [X11];
  - "R(f) = O(Q³(f)) for a more general class of symmetric functions" [X12];
  - "relative to a random oracle: There are NP search problems solvable by quantum polynomial-time machines but not classical probabilistic polynomial-time machines … Our results do not appear to contradict the Aaronson-Ambainis conjecture" [X13].
- **Cost measure** [X14]: "For some distributions on the input, such as certain power law distributions, the algorithm can achieve exponential speed-ups over the best possible classical algorithm". This concerns expected queries for search with advice.
- **White-box conditional ceilings** [X22]: "translate quantum query lower bounds on black-box problems to conditional quantum time lower bounds for many problems in BQP".

**Consequence for the program (INFERENCE).** A rigorous negative result cannot read "classical energy ⇒ ≤ quadratic". The defensible form has three parts:
- (1) a **worst-case / information-local** black-box ceiling on families with a classically easy background (S1–S5, proved);
- (2) an **explicit, non-exhaustive list of escape routes** (S11), each checked against the protein task;
- (3) **optionally, a conditional white-box ceiling** (QSETH-type) for energies expressive enough to encode hard search. That third part is not done here (gap G5).

### 3.7 Why super-quadratic needs a route out of Lemma 1

Lemma 1 lists what an algorithm must break to beat Ω(1/√p_max) against Ω(1/p_max) at bounded error in the worst case:
- (a) **Information-locality.** Queries outside R_s must carry information about s.
  - (a1) *Classically readable leakage* (funnels, gradients, correlations that local search or regression exploits) helps classical and quantum alike. It shrinks the hard residual, but does not by itself create a super-quadratic gap.
  - (a2) *Leakage readable only by quantum algorithms* (Simon/Forrelation/HSP structure; Proposition C1) can create exponential gaps.
  - "Classically readable" is not formalised here, so the a1/a2 dichotomy is an INFERENCE (gap G1).
- (b) **The oracle model.** If the oracle is a quantum process (R2) or the input is quantum data (R4), the hybrid argument against a *classical* oracle no longer bounds the task. The same applies to non-pointwise oracles (integrals, Fourier data).
- (c) **The cost measure.** Expected cost under a skewed prior [X14].
- (d) **White-box structure** exploited by specialised algorithms (R3, R5):
  - planted-inference spectral structure [C71, C72];
  - algebraic codes (DQI [C73]);
  - short-path / jump-to-the-end on Ising-type costs, super-Grover by a small exponent margin [C69, C70];
  - linear or Hamiltonian dynamics of exponentially many coupled classical degrees of freedom [X23].
- (e) **A classically hard background.** Lemma 1 lower-bounds the quantum cost, but when the background is classically hard the classical cost can exceed 1/p_max by a super-quadratic margin (§3.1 Remark).
- **Outside all of these: frustration or glassiness without hiding (INFERENCE / UNPROVEN).** A pair-distance NLL energy encodes the predicted distance distribution in every pair term. The location of the model's preferred structure therefore leaks through queries almost everywhere.
  - Over a family indexed by sequence, the model's own prediction makes the effective p_max = O(1), and Lemma 1 gives nothing.
  - If sampling is nonetheless hard, the hardness would come from frustration among pair terms, chain-geometry constraints, and entropic or glassy multi-basin structure.
  - No proved ceiling covers this regime. For white-box frustrated energies (spin glasses) the best known quantum algorithms are quadratic or slightly super-Grover [C69, C70]. No lower bound is known beyond the conditional ones of S10.

### 3.8 Does any protein-structure task have (R1)–(R5)? (INFERENCE throughout)

| Task | Forward model | (R1) quantum-only algebraic leakage | (R2) quantum forward model | (R3) planted stat–comp gap | (R4) quantum data | (R5) exploitable white-box structure | Verdict |
|---|---|---|---|---|---|---|---|
| Single-structure prediction (sequence → structure) | learned classical networks | none known | no | endpoint information-limited at ≤ 60 aa (H-002; S29–S33) | no | none known | **No** |
| **Learned-energy posterior sampling (surviving lead)** | classical (esmprior pair-distance NLL + (θ,τ) head + sterics) | Symmetries are known, not hidden: internal coordinates remove SE(3), and torsion periodicity is explicit. Pair terms are smooth in distances; no hidden-period structure is known. Leakage is classical and global: every pair term encodes its predicted distance distribution (§3.7). L-BFGS was run for a fixed 200 iterations; convergence was not verified (§4.3) | no (Born–Oppenheimer nuclei; nuclear quantum effects are outside this model) | not a planted-inference task | no | None known. Polynomially many (≈ 2L) degrees of freedom with stochastic, dissipative dynamics. The exponential dimension is in the distribution, not in a conservative linear state vector of the kind [X23] needs; a harmonic (normal-mode) model of the chain is classically poly(L) | **No known route.** Whether the bottleneck is information-local is untested (G6); global leakage suggests it is not, so S1–S3 do not apply without a new argument. The pilot is consistent with, but does not demonstrate, a first-order-like bottleneck (§4.2). Frustration or glassy hardness (§3.7) is covered by no proved ceiling |
| Free energies / ensemble averages | classical | — | no | — | no | none known | **No.** Estimator precision is capped at quadratic by S5. Mixing is capped at quadratic by S1–S3 only on information-local families; slow conformational sampling is exactly the τ that walks square-root, and [B71] names it as a binding cost alongside force-field bias ("most acute for systems where low-energy … states are separated by high effective barriers"). The practical cost is set by §4.5 |
| Global-minimum / decoding (mode finding) | classical | — | no | — | no | Short-path / jump-to-the-end apply to Ising-type costs [C69, C70]; no protein mapping known, and the exponent margin c is small | **No.** Black-box search is Θ(√) [C55, C56]. **Not restart-saturated.** At L = 45 (R64), 23/32 clusters are singletons (Good–Turing unseen mass ≈ 0.36), only 1–5 of 64 restarts reach within 20 nats of the best, and PT found lower energy. In the R256 census the best-found cluster was hit once in 16 of 87 files (§4.3) |
| Design / rotamer packing | classical, discrete | none; classical exact and bounded solvers exploit problem structure [B75, B76] | no | no | no | Pairwise discrete costs are Ising-like, so [C69, C70] apply in principle (super-Grover by a small margin; INFERENCE) | **No** |
| Structure inference from noisy restraints (contacts, coevolution, NMR, cryo-EM) | classical likelihood | none known | no | **Planted in spirit.** The known quartic speedups need kXOR/tensor structure in the stat–comp gap [C71, C72]. Pairwise restraints are a k = 2 (matrix) problem. For those, spectral methods are the natural classical algorithm, and no Kikuchi-level advantage is known to me (INFERENCE, not verified). The measured regime is information-limited | no | none known | **Weak candidate** (known speedups up to nearly quartic; no ceiling proved; theory note needed, gap G8) |
| Electronic structure of active sites | **quantum** | — | **yes** | — | no | — | Chemistry, not conformational structure. No generic exponential advantage [F64]. Embedding it in conformational sampling multiplies costs by the number of energy calls. **Out of scope for structure** |
| NMR-based determination with quantum sensors | physical quantum spins | — | — | — | **possible in principle** [X18] | — | Current data are classical records. A quantum-memory transduction experiment would be a different program. **No for present data** |

### 3.9 Published claims of super-quadratic sampling speedups, placed against S1–S11 (INFERENCE; sources: `lit_A_sampling.md` P43, P44, P46, P47)

| Claim | Cost measure | Classical comparator | Why it does not contradict S1–S3 | Evidence level |
|---|---|---|---|---|
| [A46] Incudini–Mazzola: "a total sixth-degree polynomial queries speedup compared to the best classical walk"; crossover "less than one day" | walk/query count from spectral gaps | local and uniform-proposal Metropolis; PT not compared | White-box SK instances at β = 4, not an information-local family, so S1–S3 say nothing about them (S10). Exponents are fitted from exact matrices at n = 3–10 and extrapolated to n ≈ 50–90. The comparator is one class of chain, not the best classical algorithm. The one-day figure assumes 20 ns gates | SIMULATOR (exact small-n) + FT estimate; empirical |
| [A47] Layden et al.: "roughly cubic/quartic enhancement" | spectral gap δ ∝ 2^{−kn} | local (single-flip) and uniform proposals | Same as above: white-box instances, n ≤ 10, weak comparator; disputed by [A48] | SIMULATOR + HARDWARE (n ≤ 10); empirical |
| [A44] Leng et al.: "up to a quartic quantum speedup over best-known classical Langevin-based methods" | gradient-oracle queries | MALA's Cheeger-based *upper* bound Õ(d·C_CG²) | Measured against a weaker classical upper bound, not a classical lower bound. Against the Poincaré-constant scaling the gain is quadratic, and C_PI still grows as e^{βΓ} | THEORETICAL (upper bounds only) |
| [A43] Claudon et al.: "up-to-exponential quantum speedup" for nonreversible chains | Szegedy-walk uses O(√(τ_rev·τ(ε))·log 1/ε) | the nonreversible chain's own mixing time | Relative to one chain, not the best classical sampler; its condition (reversibility on π-average) must be checked case by case. On information-local families S1 still bounds every algorithm | THEORETICAL (toy examples) |

None of these compares against the best classical algorithm on a family where S1 applies. Their super-quadratic exponents are either relative to a comparator or empirical fits at n ≤ 10. They are evidence about specific white-box instances and chains, not counterexamples to a worst-case ceiling.

---

## 4. Numbers

Assumptions are labelled [AS#] and pilot inputs PILOT. The Python checks are in the Appendix; they read the RAW files directly.

### 4.1 α for the learned energy (DERIVED from PILOT data)

- L = 45 (crop 5O37A_45, T = 1, energies in nats).
- The 32 L-BFGS endpoint clusters from 64 restarts span E = 3820.0 … 4183.7 (`g1_modes_test`).
- PT's polished lowest energy is 3787.2 (`g1_pilot/5O37A_45_T1_s0.json`).
- So β(max E − min E) ≥ 4183.7 − 3787.2 = 396.5 for the **full** energy, i.e. **α ≥ e^{396} ≈ 10^{172}** and √α ≥ 10^{86}. The true range is larger, because max E is taken over all of X, including steric clashes.
- T2 §4.1 bounds the **pair-term** range: max V − min V ≥ E_{π₀}[V] − E_{π₁}[V] ≈ 3.2×10³ nats at L = 45, 2.1×10⁴ at L = 100 and 5.4×10⁴ at L = 150. That is the α relevant to rejection sampling from the exact prior. The two bounds concern different ranges and both are valid lower bounds.

**Consequence.**
- [A45]'s α-parameterised bounds and the Θ(α) classical rejection-sampling bound are **vacuous** for this energy.
- That is automatic: for any extensive energy βΔ grows at least in proportion to L, and faster here because the pair term has O(L²) terms. So "α is huge" carries little information.
- The substantive point is that **α is the wrong hardness parameter.** Practical samplers are governed by barriers and free-energy differences along their path (ΔF‡, Λ, and the relaxation time at the bottleneck), not by the energy range.
- The classical sampler used here is not governed by α at all. NRPT used 5.6×10⁵ gradient evaluations in 331 s at L = 45, including tuning (PILOT). The α-parameterised separation is a worst-case statement over a class, and neither side's practical algorithm operates in that regime.

### 4.2 The tempering path: NRPT prediction vs observation (DERIVED from PILOT + [X20]; readings are INFERENCE)

For a finite schedule with swap rejections r_i, under stationarity and "efficient local exploration" (ELE, assumption A2 of [X20]), the round-trip rate of non-reversible PT is τ_N = 1/(2 + 2Σ_i r_i/(1−r_i)) per scan [X20, Thm. 1 / Cor. 1]. As the schedule is refined this tends to 1/(2 + 2Λ) [X20, Thm. 3], which is an upper bound on τ_N at a finite schedule. Λ = Σ r_i is the integrated rejection. The sibling note T2 (§S4, §4.1) uses the same finite-N formula.

| Crop | L | Rungs N | Λ final (Λ used to size schedule) | Σ r/(1−r) | Scans | Predicted round trips (finite N) | Fine-mesh limit (upper bound) | Observed | Poisson P(0) | Swap rejection mean / max |
|---|---|---|---|---|---|---|---|---|---|---|
| 5O37A_45 | 45 | 30 | 13.6 (11.2) | 26.3 | 1500 | **27.5** | 51 | 0 | 1×10⁻¹² | 0.47 / 0.59 |
| 3GAHA_60 | 60 | 32 | 14.4 (11.9) | 27.5 | 1200 | **21.1** | 39 | 0 | 7×10⁻¹⁰ | 0.46 / 0.58 |
| 5O37A_100 | 100 | 39 | 24.9 (14.5) | 87.2 | 800 | **4.5** | 15.5 | 0 | 0.011 | 0.65 / 0.88 |
| 4LPQA_120 | 120 | 37 | 25.2 (13.9) | 90.9 | 600 | **3.3** | 11.4 | 0 | 0.038 | 0.70 / 0.83 |
| 5O37A_150 | 150 | 39 | 29.3 (14.7) | 150.2 | 500 | **1.7** | 8.3 | 0 | 0.19 | 0.77 / 0.89 |

The Poisson P(0) ignores the minimum trip time of ≥ 2(N−1) scans (58–76 here), the initial transient, and the persistent-walk dynamics. The true P(0) under the model is larger, especially at L ≥ 100.

**Stationarity diagnostics (PILOT; from `*.npz`).**
- Mean of E_top over successive fifths of the run (nats):
  - L = 45: 3839 → 3833;
  - L = 60: 8259, 8244, 8236, 8241, 8247 (no monotone trend);
  - L = 100: 21196 → 21030;
  - L = 120: 33566 → 33405;
  - L = 150: 53207 → 52598.
- Rungs whose second-half mean E_pair is below the first-half mean: 27/30, 29/32, 35/39, 34/37, 35/39.
- T2 §4.1(d) reports the drift at λ ≥ 0.3 as 1–26 nats (L = 45) rising to 326–732 nats (L = 150).
- **None of the runs is stationary.** Non-stationarity grows with L. [X20]'s rate formula assumes stationarity.

**What the stored data show about the λ-path (PILOT).**
- About one third of Λ sits at λ ∈ [0, 0.05]: 4.4 of 13.6 at L = 45, 4.7 of 14.4 at L = 60, 11.3 of 29.3 at L = 150. Only about 10% sits in [0.35, 0.6] (1.4–3.1).
  - By T2's Lemma 2, a first-order crossing adds exactly 1 to Λ, so this distribution can neither show nor exclude one.
- Rung means of E_pair fall smoothly with λ. Their standard deviations decrease monotonically through λ ≈ 0.4–0.5 (full-trace SD 22.0 → 21.5 → 20.1 at λ = 0.38, 0.43, 0.49 for L = 45). There is no jump and no variance peak of the kind an equilibrium two-phase crossing produces.
- **REPORTED, not reproducible from RAW:**
  - that the bottleneck sits at λ ≈ 0.4–0.5;
  - that "replicas from the prior never penetrate".

  The pilot JSONs, npz files and joblogs store no replica-index or penetration traces.

**Reading (INFERENCE, PILOT).**
- **L = 45 and 60.** Zero observed against 27.5 and 21.1 predicted is a significant deficit. Swap rejection is moderate there (≤ 0.59), so swap communication is not the limiting factor at these lengths. Two hypotheses remain open:
  - (H1) ELE violation from within-rung metastability. This could be a first-order-like crossing seen out of equilibrium, or glassy multi-basin trapping [E39].
  - (H2) Burn-in or under-exploration: the runs are non-stationary. T2's check D3 separates the two by scanning exploration steps per scan. If the deficit vanishes as exploration grows, the bottleneck is cheap classically.
- **L ≥ 100: not diagnostic.**
  - Only 1.7–4.5 round trips were expected.
  - The schedules were sized from pilot values Λ ≈ 14–15, while the final Λ was 25–29. With N = 37–39 rungs, swap rejection reached 0.83–0.89, so swap communication is itself a bottleneck there (H3).
  - These runs are the most strongly non-stationary.
- The pilot is **consistent with, but does not demonstrate,** a first-order-like bottleneck.
- Classical results that bear on this: first-order transitions defeat temperature tempering for any schedule, while entropy-dampening paths can be polynomial [E40]; narrow-vs-wide peaks cause torpid PT mixing [E39].
- The quantum-annealing analogue of a first-order transition "reduce[s] to the Grover problem in a particular limit" with an exponentially closing gap [X19]. S1–S3 apply to that regime only *if* the bottleneck is information-local, which global leakage (§3.7) makes doubtful.
- **The classical adversary comes first.** The linear λ-path (prior → posterior) "performs poorly in the setting where the reference and target are nearly mutually singular" [X21]. The options in G7 must be tried before this bottleneck is treated as intrinsic.
- **Budget (PILOT; production scans only).**
  - L = 45 used 393,000 production gradient evaluations. That is 8.7 per rung per scan, or 1.3×10⁴ per rung over the run. The totals of 5.6×10⁵ also include pilot and tuning runs.
  - Per rung: 1.05×10⁴ at L = 60 and 7.0×10³ at L = 100.
  - The whole production budget that produced no round trip was 3.9×10⁵ (L = 45), 3.4×10⁵ (L = 60) and 2.7×10⁵ (L = 100).
  - A 95% Poisson bound (rate ≤ 3/n) gives ≳ 1.3×10⁵ local steps per round trip at L = 45 (T2 §4.1(b)).
  - These are **heuristic indications for this NRPT configuration** (INFERENCE). They are not lower bounds on the best classical sampler. "Within-rung relaxation exceeds the per-rung budget" is an inference from zero round trips, not a bound.

### 4.3 Mode finding by multistart (DERIVED from PILOT)

**R64 test file** (5O37A_45; 64 restarts; a fixed 200 L-BFGS iterations, convergence not verified; greedy 2 Å CA-RMSD clustering):
- 32 clusters, 23 of them singletons. The Good–Turing unseen-mass estimate is 23/64 ≈ 0.36. The last new cluster appeared at restart index 53.
- The lowest-energy cluster holds 14/64 restarts (p = 0.219).
- Only **1–5 of 64 restarts end within 20 nats of E_best**. The first is at index 59. The discovery curve records clusters, not restarts, which is why only a range can be given.
- PT found lower energy (3815.0 raw, 3787.2 polished) than any restart (3820.0).
- The "modes" are **L-BFGS endpoints, not certified minima.** Their Hessians have 26 eigenvalues ≤ 10⁻⁶ at the best representative (L = 45, D = 85). These are flat directions or negative curvature.

**R256 census** (2026-09-27 snapshot: 87 crop × length files, 256 restarts each, same protocol):

| L | Files | Median clusters | Median p(best-found cluster) | Median p(E ≤ E_best + 20 nats) | Eigenvalues ≤ 10⁻⁶ at representatives (D = 2L−5) |
|---|---|---|---|---|---|
| 30 | 16 | 82 | 0.117 | 0.24 | 6–25 (D = 55) |
| 45 | 16 | 109 | 0.109 | 0.041 | 15–39 (85) |
| 60 | 16 | 150 | 0.049 | 0.012 | 36–61 (115) |
| 80 | 16 | 181 | 0.059 | 0.0078 | 57–89 (155) |
| 100 | 16 | 244 | 0.016 | 0.0039 (= 1/256 floor) | 77–118 (195) |
| 120 | 7 | 252 | 0.008 | 0.0039 (floor) | 112–142 (235) |

The best-found cluster was hit exactly once in 16 of 87 files, e.g. 3GAHA_60/80, 3TE4A_60, 7B4RA_60, 9IXCA_60, 4LPQA_80/100, 3S0QA_80/100 and 5QHWA_45. The census is **not restart-saturated**, and the energy-predicate hit rate falls quickly with L.

**Grover over restarts (DERIVED; query counts only).**
- Accounting: an amplified attempt with k iterates costs 2k+1 calls of the reversible restart map (A, A†, plus the initial call). It is repeated until success, with k chosen to minimise the expected number of calls and p assumed known.
- **Structural predicate** (membership in the best CA-RMSD cluster, p = 14/64): k = 1 gives 3 calls with success 0.988, so 3.04 expected calls against 4.57 classical restarts, a gain of **≈ 1.5×**. At matched confidence 0.988 the comparison is 3 calls against 18 restarts, **≈ 6×**.
  - A coherent marking oracle **cannot** evaluate this predicate without already knowing the best structure. Only an energy predicate "E(Φ(x₀)) ≤ t" is implementable, as T4 uses.
- **Energy predicate** (within 20 nats of E_best):
  - At L = 45 (R64), p ≈ 1/64–5/64. Expected quantum calls are 11.0–5.1 (k = 4 and k = 2) against 64–12.8 classical, a gain of **≈ 5.8–2.5×**.
  - Using the R256 medians: ≈ 3.5× (L = 45), 6.7× (L = 60), and ≥ 11.6× at L ≥ 100 if p ≤ 1/256 there.
- The gain grows as Θ(1/√p) but stays quadratic.
  - With an unknown threshold, a Dürr–Høyer-style record process adds a constant: T4 measures 1.56–1.78·c_QS on the census spectra.
  - All of this comes before the reversibility overheads. Each call is a reversible 200-iteration L-BFGS. T4 costs these at a coherent worst case of ≈ 2,400 gradient-evaluation equivalents against a classical average of 174–218, or 10¹¹–10¹³ Toffolis at L = 60–150. It finds that break-even needs p ≲ 10⁻¹⁶–10⁻¹⁸.

### 4.4 Precision (DERIVED, numerical check of S5)

Success ≥ 2/3 for distinguishing p = ½ ± ε. Quantum: k Grover iterates plus one measurement, costing 2k + 1 calls. Classical: majority test on n samples, with n the exact minimum.

| ε | Hybrid lower bound (calls) | Explicit quantum strategy (calls) | Classical samples | Ratio (classical / quantum) |
|---|---|---|---|---|
| 0.1 | 1.66 | 3 | 5 | 1.7 |
| 0.03 | 5.55 | 7 | 51 | 7.3 |
| 0.01 | 16.67 | 17 | 465 | 27.4 |
| 0.003 | 55.56 | 57 | 5,153 | 90.4 |

- The lower bound of §3.4 is within 2–3% of the explicit strategy for ε ≤ 0.01 (26% at ε = 0.03). Asymptotically the ratio is 3·asin(1/3) ≈ 1.0195, so Theorem B1 is essentially tight.
- These are **query** ratios. Each quantum call is a coherent preparation U of the posterior state, itself ≥ √τ walk steps of 10⁶–10⁸ Toffolis each. Each classical call is one i.i.d. sample. Under the §4.5 assumptions a query gain of ≤ 100× cannot offset that per-call overhead, so S5 has no practical level here.

### 4.5 Fault-tolerant break-even for a speedup of degree d (Babbush model [B46]; DERIVED arithmetic on labelled assumptions)

**Model** [B46, eqs. 1–5]: M quantum calls at t_Q each; M^d classical evaluations at t_C each, with parallel speedup S. Break-even is at M* = (t_Q·S/t_C)^{1/(d−1)} and T* = t_Q·M*.

**Assumptions** (one length throughout, L = 45, where the pilot is diagnostic).
- [AS1] t_C = 0.59 ms per energy+gradient evaluation at L = 45, one core. This is the pilot wall-clock including sampler overhead (T2 §4.1). The orchestrator's microbenchmark is 1.8 ms at L = 150. For d = 2 the thresholds scale as t_C^{−2}, so using the L = 150 figure at L = 45 would understate them by ≈ 9×.
- [AS2] 10⁶–10⁸ Toffolis per coherent energy/gradient call or walk step. This is an I(agent) range from `lit_A_sampling.md` §3.9. T2 uses 1.0×10⁷–6.1×10⁷ at L = 45, and T4's C_step(45) ≈ 1.0×10⁸, so the 10⁶ rows are optimistic.
- [AS3] 170 µs per Toffoli (surface code, one factory [B46]), or 1 µs (optimistic future).
- [AS4] S ∈ {1, 30, 10³}. S = 30 is one core per PT rung, the parallelism PT has natively.
- [AS5] One quantum call replaces one classical evaluation-equivalent, and the degree-d speedup applies to the **total** cost. This is generous to quantum. Walk and QSA speedups square-root only the gap: the stage count ℓ ≈ 0.63Λ, the K reflections per stage, log(1/π_min), overlap and phase-estimation overheads are not square-rooted. The effective degree is therefore below d.
- [AS6] d = 2 is the ceiling proved here for information-local families. d = 4 is hypothetical, for contrast.

**Break-even thresholds.** Each cell gives the classical evaluations per independent sample at break-even (M\*^d), then the quantum wall-clock at break-even (T\*). Every entry is a **lower bound on the classical cost needed for break-even**, by [AS5].

| t_Q (per call) | d | S = 1 | S = 30 | S = 10³ |
|---|---|---|---|---|
| 1 s (10⁶ Toff @ 1 µs, optimistic) | 2 | 2.9×10⁶; 28 min | 2.6×10⁹; 14 h | 2.9×10¹²; 20 d |
| 1 s | 4 | 2.0×10⁴; 12 s | 1.9×10⁶; 37 s | 2.0×10⁸; 2 min |
| 170 s (10⁶ Toff @ 170 µs) | 2 | 8.3×10¹⁰; 1.6 yr | 7.5×10¹³; 47 yr | 8.3×10¹⁶; 1.6×10³ yr |
| 170 s | 4 | 1.9×10⁷; 3.1 h | 1.8×10⁹; 9.7 h | 1.9×10¹¹; 1.3 d |
| 1.7×10⁴ s (10⁸ Toff @ 170 µs) | 2 | 8.3×10¹⁴; 1.6×10⁴ yr | 7.5×10¹⁷; 4.7×10⁵ yr | 8.3×10²⁰; 1.6×10⁷ yr |
| 1.7×10⁴ s | 4 | 8.8×10⁹; 60 d | 8.2×10¹¹; 187 d | 8.8×10¹³; 1.7 yr |
| 1 s, GPU-batched classical (t_C = 5.9 µs; **hypothetical** 100× throughput, not measured) | 2 | 2.9×10¹⁰; 2.0 d | 2.6×10¹³; 59 d | 2.9×10¹⁶; 5.4 yr |

**Reconciliation with T2 §4.3.**
- T2 computes B* = (K·ℓ·R)² with R = G·t_T/c. This table is the special case K = ℓ = ρ = 1.
- T2's most favourable L = 45 scenario uses G = 10⁷ (1 µs), K = 10 and ℓ = 8.6. That multiplies the optimistic S = 1 entry by (Kℓ)²·10² ≈ 7.4×10⁵, giving **B\* ≈ 2.1×10¹² local steps per sample and T\* ≈ 40 years**.
- The two notes agree once the non-square-rooted factors are included. T2's figure is the one to use for decisions.

**Reading.**
- Under [B46]'s surface-code assumptions a quadratic speedup needs the best classical sampler to spend **≥ 8×10¹⁰ evaluations per independent sample** (10⁶ Toffolis, one core), and up to 8×10²⁰. Break-even wall-clock ranges from 1.6 years to 10⁷ years.
- Under the optimistic row the lower bound is 2.9×10⁶ (S = 1) or 2.6×10⁹ with PT's native parallelism (S = 30). With T2's stage and reflection factors it rises to ≥ 2×10¹² (≈ 40 years per sample).
- The practical verdict on a quadratic speedup therefore needs hardware far beyond [AS3]. That is the T2 and T4 conclusion, and S1–S5 do not settle it, because they are query statements.
- Faster classical evaluation (e.g. GPU batching) raises every d = 2 threshold as t_C^{−2}.
- A quartic speedup would cut the thresholds by many orders of magnitude, which is why S11 matters.
- **Pilot comparison (INFERENCE).**
  - At L = 45 this NRPT configuration used 3.9×10⁵ production evaluations with no round trip; the Poisson-95% indication is ≳ 1.3×10⁵ per round trip.
  - Both lie below every threshold above, including the optimistic S = 1 figure of 2.9×10⁶.
  - They bound this configuration only, not the best classical sampler that break-even requires. G1 must bound the latter at L = 60–150.

### 4.6 Lemma 1 constants vs Grover, in energy queries (DERIVED)

δ = ½, ε = ⅛. Each Grover iterate costs 2 energy queries (compute and uncompute the marking at a cell centre), plus 1 classical check.

| M | T_Q lower bound (Lemma 1) | Grover energy queries to find the cell (≈ π/2·√M, success ≈ 1) | Grover energy queries for SAMPLE at TV ⅛ (success ≥ ¾, ≈ π/3·√M) | T_C lower bound |
|---|---|---|---|---|
| 2¹⁰ | 6.0 | 51 | 35 | 383 |
| 2²⁰ | 192 | 1,609 | 1,073 | 3.9×10⁵ |
| 2⁴⁰ | 2.0×10⁵ | 1.6×10⁶ | 1.1×10⁶ | 4.1×10¹¹ |

- Lower and upper bounds agree to a constant factor of **≈ 8.4** for search to near-certainty. The factor is **≈ 5.6** for the SAMPLE task, which only needs success ≥ ¾: output an exact sample of π_s if the cell is found, otherwise a uniform sample, giving TV ≤ (1−q)·½.
- Sampling after the cell is found needs no further queries, because the family's patch profile is known in closed form.

---

## 5. Literature

### 5.1 Bibliography keys used (verified in the literature phase; see `BIBLIOGRAPHY.md`)

| Group | Keys |
|---|---|
| Sampling separations and samplers | [A45] Olivucci et al. 2026 (arXiv 2608.24527; re-read via HTML on 2026-09-26/27: Def. II.3, Thm. II.4 eqs. (12)–(14), Def. III.2, Prop. III.3, Thm. III.1, Thm. IV.3); [A44] Leng et al.; [A36] Ozols–Roetteler–Roland; [A1] Szegedy; [A8] QSA; [A12] AAKV; [A33] Somma–Boixo; [A48] Orfi–Sels; [A43] Claudon et al.; [A46] Incudini–Mazzola; [A47] Layden et al.; [A55] Lemieux et al.; [A11]/[B31] Aharonov–Ta-Shma |
| Search | [C54] Grover; [C55] BBBV; [C56] Dürr–Høyer |
| Structured / super-quadratic | [C69] Hastings, short path; [C70] Dalzell et al., jump to the end; [C71] Schmidhuber et al., quartic planted inference; [C72] Hastings, tensor PCA; [C73] DQI |
| Estimation | [B12] Montanaro; [B13] Heinrich; [B15] Novak; [B16] Nayak–Wu; [B19] Kothari–O'Donnell; [B26] Harrow–Wei; [B28] Cornelissen–Hamoudi; [B29] Chen–Nannicini; [B33] Claudon et al. circuits; [B71] Mobley–Gilson |
| Fault-tolerant cost | [A56]/[C64] Sanders et al.; [B46]/[A57] Babbush et al. |
| Classical tempering and samplers | [E33] Machta (golf course); [E39]/[A74] Woodard et al. (persistence); [E40] Bhatnagar–Randall; [B66] Wang–Landau; [A78]/[E76] Noé et al., Boltzmann generators |
| Chemistry / discrete design | [F64] Lee et al.; [B75], [B76] |
| Sibling-note keys (T2 §5.2) | [T2-3] Surjanovic et al., variational reference; [T2-12] Paulin–Jasra–Thiery, interpolation to independence; [T2-13] Mathews–Schmidler, SMC on multimodal targets |

### 5.2 New references verified for this note (not yet in BIBLIOGRAPHY; add on integration)

| Key | Reference | Verification |
|---|---|---|
| X1 | Beals, Buhrman, Cleve, Mosca, de Wolf, "Quantum lower bounds by polynomials," J. ACM 48(4):778–797 (2001). DOI 10.1145/502090.502097. arXiv quant-ph/9802049 | arXiv API abstract + Crossref (2026-09-26) |
| X2 | Aaronson, Ben-David, Kothari, Rao, Tal, "Degree vs. approximate degree and quantum implications of Huang's sensitivity theorem," arXiv 2010.12629 | arXiv API abstract; venue (STOC 2021) not verified |
| X3 | Ambainis, Balodis, Belovs, Lee, Santha, Smotrovs, "Separations in query complexity based on pointer functions," arXiv 1506.04719 | arXiv API abstract; J. ACM venue only as cited in X2 |
| X4 | Aaronson, Ben-David, Kothari, "Separations in query complexity using cheat sheets," STOC 2016, 863–876. DOI 10.1145/2897518.2897644. arXiv 1511.01937 | arXiv API abstract + journal_ref |
| X5 | D. R. Simon, "On the power of quantum computation," SIAM J. Comput. 26(5):1474–1483 (1997). DOI 10.1137/S0097539796298637 | **Crossref metadata only.** The classical lower-bound argument in §3.5 is the standard one, reconstructed here and not re-read from the paper |
| X6 | P. W. Shor, "Polynomial-time algorithms for prime factorization and discrete logarithms on a quantum computer," SIAM J. Comput. 26(5):1484 (1997). DOI 10.1137/S0097539795293172. arXiv quant-ph/9508027 | arXiv API abstract + DOI |
| X7 | Childs, Cleve, Deotto, Farhi, Gutmann, Spielman, "Exponential algorithmic speedup by quantum walk," STOC 2003, 59–68. DOI 10.1145/780542.780552. arXiv quant-ph/0209131 | arXiv API abstract |
| X8 | Aaronson, Ambainis, "Forrelation: a problem that optimally separates quantum from classical computing," arXiv 1411.5729 | arXiv API abstract; venue (STOC 2015 / SICOMP 2018) only as cited in X9 |
| X9 | Bansal, Sinha, "k-Forrelation optimally separates quantum and classical query complexity," arXiv 2008.07003 | arXiv API abstract (2026-09-26) + **full-text PDF** (2026-09-27): Cor. 1.5, R(f) ≥ Q(f)^{3−o(1)} for a total function; cites the R = O(Q³) conjecture |
| X10 | Sherstov, Storozhenko, Wu, "An optimal separation of randomized and quantum query complexity," arXiv 2008.10223 | arXiv API abstract (2026-09-26) + **full-text PDF** (2026-09-27): Thm. 1.5, R_{1/3} ≥ Q_{1/3}^{3−o(1)}; reports Tal's 8/3 |
| X11 | Aaronson, Ambainis, "The need for structure in quantum speedups," Theory of Computing 10:133–166 (2014). DOI 10.4086/toc.2014.v010a006. arXiv 0911.0996 | arXiv API abstract + Crossref |
| X12 | A. Chailloux, "A note on the quantum query complexity of permutation symmetric functions," arXiv 1810.01790 | arXiv API abstract; venue not verified |
| X13 | Yamakawa, Zhandry, "Verifiable quantum advantage without structure," J. ACM 71(3):20 (2024). DOI 10.1145/3658665. arXiv 2204.02063 | arXiv API abstract + journal_ref |
| X14 | A. Montanaro, "Quantum search with advice," Proc. TQC 2010, 77–93. arXiv 0908.3066 | arXiv API abstract + journal_ref |
| X15 | C. Zalka, "Grover's quantum searching algorithm is optimal," PRA 60:2746–2751 (1999). DOI 10.1103/PhysRevA.60.2746. arXiv quant-ph/9711070 | arXiv API abstract + Crossref |
| X16 | Boyer, Brassard, Høyer, Tapp, "Tight bounds on quantum searching," Fortschr. Phys. 46:493–506 (1998). arXiv quant-ph/9605034 | arXiv API abstract + journal_ref |
| X17 | A. Ambainis, "Quantum lower bounds by quantum arguments," arXiv quant-ph/0002066 | arXiv API abstract; venue not verified. Cited only as the adversary-method alternative to §3.1 |
| X18 | H.-Y. Huang, Broughton, Cotler, Chen, Li, Mohseni, et al., "Quantum advantage in learning from experiments," Science (2022). DOI 10.1126/science.abn7293. arXiv 2112.00778 | arXiv API abstract + DOI |
| X19 | Jörg, Krzakala, Kurchan, Maggs, Pujos, "Energy gaps in quantum first-order mean-field-like transitions: the problems that quantum annealing cannot solve," EPL 89:40004 (2010). DOI 10.1209/0295-5075/89/40004. arXiv 0912.4865 | arXiv API abstract + journal_ref |
| X20 | Syed, Bouchard-Côté, Deligiannidis, Doucet, "Non-reversible parallel tempering: a scalable highly parallel MCMC scheme," JRSS-B (2022). DOI 10.1111/rssb.12464. arXiv 1905.02939 (= [T2-1]) | arXiv API + **full-text PDF** (Thm. 1 / Cor. 1: finite-N rate 1/(2+2E(P_N)); Thm. 3: τ̄ = 1/(2+2Λ); assumption A2 = ELE) |
| X21 | Syed, Romaniello, Campbell, Bouchard-Côté, "Parallel tempering on optimized paths," arXiv 2102.07720 (= [T2-2]) | arXiv API abstract; venue not verified |
| X22 | Buhrman, Patro, Speelman, "The quantum strong exponential-time hypothesis," arXiv 1911.05686 | arXiv API abstract; venue not verified |
| X23 | Babbush, Berry, Kothari, Somma, Wiebe, "Exponential quantum speedup in simulating coupled classical oscillators," Phys. Rev. X 13, 041041 (2023). DOI 10.1103/PhysRevX.13.041041. arXiv 2303.13012 | arXiv abstract page (2026-09-27): 2^n oscillators, 2^{Ω(n)} classical queries, BQP-complete |
| X24 | Berg, Neuhaus, "Multicanonical ensemble: a new approach to simulate first-order phase transitions," PRL 68, 9–12 (1992). DOI 10.1103/PhysRevLett.68.9 (= [T2-8]) | Crossref metadata (2026-09-27) |
| X25 | J. Machta, "Population annealing with weighted averages: a Monte Carlo method for rough free-energy landscapes," PRE 82, 026704 (2010). DOI 10.1103/PhysRevE.82.026704 (= [T2-11]) | Crossref metadata (2026-09-27) |

**Unverified / not cited as evidence.**
- (i) Tal's 8/3 R-vs-Q separation is cited only as reported in [X10]; the paper was not read.
- (ii) The exact statement of QSETH (which variant, which exponent) was not read beyond the abstract of [X22].
- (iii) The claim that rank-one spiked matrix problems with pairwise restraints have no statistical–computational gap for standard priors is my recollection. It is used only as INFERENCE in §3.8 and is not verified.
- (iv) That [A45]'s Theorem II.4 regime has ϱ = Θ(1/d) is inferred from eq. (12) and Prop. III.3. The constants were not checked.

---

## 6. Scope and what is NOT claimed

- **Not claimed:** that learned-energy posterior sampling admits no super-quadratic quantum speedup. S1–S5 are black-box statements about instance families. The real energy is white-box, and only conditional white-box ceilings are possible (S10).
- **Not claimed:** that the pilot energy contains hide-and-seek (information-local) wells, or that it has a first-order-like bottleneck.
  - The pilot is consistent with, but does not demonstrate, such a bottleneck (§4.2).
  - Its location at λ ≈ 0.4–0.5 is REPORTED and cannot be checked from RAW.
  - Pair-distance energies leak basin location globally, so information-locality is doubtful (§3.7, G6).
- **Not claimed:** that [A45]'s separation is relevant to proteins. α ≥ 10^172 at L = 45 makes it vacuous there (§4.1).
- **Not claimed:** that [A45]'s own algorithm is optimal on its hard family. It is within α^{s/d}·poly(d) of optimal (S2).
- **Not claimed:** a gap-parameterised lower bound (Ω(1/√δ_gap)) for all chains. That is false in general. On [A45]'s family it depends on an uncomputed δ_gap(M) (gap G3).
- **Not claimed:** a joint lower bound Ω(√M/ε) for estimation (gap G2).
- **Not claimed:** that Proposition C1's family lies in [A45]'s Gevrey class *with their constants* (gap G4), or that anything like it occurs physically.
- **Not claimed:** a lower bound on the cost of the **best** classical sampler. The pilot numbers bound one NRPT configuration (§4.2, §4.5).
- **Not claimed:** any statement about **runtime**. Every lower bound here is a query bound, and every upper bound is a query bound (§4.5 converts to wall-clock only under labelled assumptions). No simulator result is used. No hardware claim is made.
- **Not claimed:** ceilings for **expected cost under skewed priors**; [X14] shows these can be exponential. Also not claimed: ceilings for quantum-data or quantum-forward-model settings, for non-pointwise oracles, for families with a classically hard background, or for frustration or glassy hardness without hiding.
- **Scope of the "ceiling":** worst-case, bounded-error, black-box query complexity with pointwise oracles, on information-local (hide-and-seek) families with a classically easy background, or on classes containing them. It covers sampling, qsampling, finding, and estimating a mean or basin observable.

---

## 7. Open gaps

- **G1 (theory).** Formalise "classically readable leakage", so that the (a1)/(a2) dichotomy of §3.7 becomes a theorem. One candidate definition: the classical query complexity of locating R_s using only queries outside R_s, compared with its quantum counterpart.
- **G2 (theory).** A joint lower bound Ω(√M/ε), or Ω(1/(ε√δ_gap)), for estimation on hide-and-seek families. This would show that the Õ(√τ/ε) upper bounds [B12, B26, B28] are jointly optimal.
- **G3 (theory, small).** Compute the spectral gap of the best local chain on [A45]'s family as a function of M. If it is Θ̃(1/M), the Szegedy/QSA quadratic gap improvement is optimal there.
- **G4 (theory, small).** Check Proposition C1's family against [A45]'s exact s-Gevrey class and constants (ρ, ξ). Tighten the Simon-style classical bound into a full proof. Check the ϱ = Θ(1/d) inference for [A45]'s Theorem II.4 (§5.2 (iv)).
- **G5 (theory).** A conditional (QSETH-type [X22]) white-box ceiling. Show that a pairwise learned-energy family is expressive enough to embed CNF-SAT or orthogonal-vectors instances, so that exact minimisation (and low-temperature sampling) inherits a conditional ~2^{n/2} quantum lower bound.
- **G6 (measurement, G1 gate).** Is there a bottleneck, where is it, and is it information-local?
  - Store replica-index traces and per-rung time series, so that the REPORTED λ ≈ 0.4–0.5 bottleneck and the "never penetrate" finding can be checked from RAW.
  - Run to stationarity (split-half and E_top drift within noise) before interpreting round-trip counts.
  - Diagnostics: does the dominant λ = 1 basin leave any gradient or committor signature at λ < λ*? Measure hitting probabilities of that basin from λ < λ* chains, and the dependence of basin mass on L.
  - Quantify leakage: how well does the model's own predicted structure, or a short local search from it, locate the dominant basin? If it does so with O(1) probability, the effective p_max is O(1) and Lemma 1 is moot.
  - Estimate log(Z_1/Z_0) and KL(π_1‖π_0) by thermodynamic integration from PT output. Rejection from the prior costs e^{D_∞(π_1‖π_0)} classically and e^{D_∞/2} quantumly. This is unmeasured.
- **G7 (classical adversary, G1 gate).** Before treating the bottleneck as intrinsic, test the options that remove first-order or singular-path bottlenecks classically:
  - optimised or spline paths [X21];
  - entropy-dampening paths [E40];
  - multicanonical sampling [X24] and Wang–Landau [B66];
  - SMC with resampling and population annealing [X25], and interpolation to independence [T2-12];
  - learned-proposal samplers such as Boltzmann generators with reweighting [A78];
  - a reference distribution centred on the model's own predicted structure, or a variational reference [T2-3], instead of the product prior;
  - T2's check D3 (does the round-trip deficit vanish as exploration steps per scan grow?).

  If any of these removes the bottleneck, the quantum question at this L is moot.
- **G8 (theory).** Map structure-from-restraints inference onto the planted kXOR/tensor framework of [C71, C72]. Decide whether k ≥ 3 structure appears, which is needed for the quartic speedup. Decide whether the program's regime sits between the information-theoretic and computational thresholds or below the information threshold (the S29–S33 finding at ≤ 60 aa).
- **G9 (integration).** Add [X1]–[X25] to `BIBLIOGRAPHY.md`; [X20], [X21], [X24] and [X25] duplicate T2's [T2-1], [T2-2], [T2-8] and [T2-11]. Map the levels in the §0 table onto the program's L0–L6 scale, using the working table in T4.
- **G10 (theory).** Frustration or glassy hardness without hiding (§3.7). Is there any lower bound, even conditional, for sampling white-box frustrated pairwise energies at T = 1 that goes beyond S10? Is anything better than quadratic (short-path-type [C69, C70]) plausible for such energies?

---

## Appendix: Python checks (run 2026-09-27 from the repository root; needs numpy; reads the RAW files; under 5 s)

```python
import json, glob, math, statistics as st
from math import asin, sqrt, sin, lgamma, log, exp, pi, ceil, floor
import numpy as np
RAW = "research/results/RAW"

# §4.2: NRPT finite-N prediction [X20 Thm 1 / Cor 1]: scans / (2 + 2*sum r/(1-r)); fine-mesh limit scans/(2+2*Lambda)
for f in sorted(glob.glob(f"{RAW}/g1_pilot/*_T1_s0.json")):
    d = json.load(open(f)); rej = d["rej"]; lams = d["lams"]; E = sum(r / (1 - r) for r in rej)
    z = np.load(f.replace(".json", ".npz")); P = z["pair_trace"]; Et = z["E_top"]; n = len(Et)
    lo = sum(r for r, l1 in zip(rej, lams[1:]) if l1 <= 0.05 + 1e-12)
    mid = sum(r for r, l0, l1 in zip(rej, lams[:-1], lams[1:]) if l0 >= 0.35 and l1 <= 0.6 + 1e-9)
    pred = d["scans"] / (2 + 2 * E)
    print(d["crop"], "N", d["rungs"], "Lam", round(d["Lambda"], 1), "Lam_pilot", round(d["Lambda_pilot"], 1),
          "sum r/(1-r)", round(E, 1), "pred", round(pred, 1), "fine-mesh", round(d["scans"] / (2 + 2 * d["Lambda"]), 1),
          "P0", f"{exp(-pred):.1e}", "rej mean/max", round(st.mean(rej), 2), round(max(rej), 2),
          "Lam[0,.05]", round(lo, 1), "Lam[.35,.6]", round(mid, 1),
          "prod evals", d["grad_evals_production"], "per rung", round(d["grad_evals_production"] / d["rungs"]),
          "per rung/scan", round(d["grad_evals_production"] / d["rungs"] / d["scans"], 2),
          "ms/eval(all)", round(1e3 * d["secs"] / d["grad_evals_total"], 2),
          "E_top quintiles", [round(float(q.mean())) for q in np.array_split(Et, 5)],
          "rungs 2nd-half<1st", int((P[n // 2:].mean(0) < P[:n // 2].mean(0)).sum()), "/", P.shape[1])
# -> pred 27.5 (L45), 21.1 (L60), 4.5 (L100), 3.3 (L120), 1.7 (L150); fine-mesh 51.2, 39.0, 15.5, 11.4, 8.3
# -> per rung 13100 / 10500 / 7036; per rung per scan 8.73; ms/eval 0.59 (L45) ... 3.51 (L150); 2nd-half lower 27/30 ... 35/39

# §4.3: amplitude amplification over restarts: expected calls min_k (2k+1)/sin^2((2k+1)theta) vs classical 1/p
def q_exp(p):
    th = asin(sqrt(p)); return min(((2 * k + 1) / sin((2 * k + 1) * th) ** 2, k) for k in range(400))
for p in [14 / 64, 5 / 64, 1 / 64]:
    e, k = q_exp(p); print(f"p={p:.4f} classical {1/p:.2f} quantum k={k} ({2*k+1} calls) E={e:.2f} gain {1/p/e:.2f}")
# -> gains 1.51 (k=1), 2.50 (k=2), 5.81 (k=4)
p = 14 / 64; s = sin(3 * asin(sqrt(p))) ** 2; n = ceil(log(1 - s) / log(1 - p))
print("matched confidence", round(s, 3), "classical", n, "quantum 3 -> gain", round(n / 3, 1))   # 0.988, 18, 6.0
t = json.load(open(f"{RAW}/g1_modes_test/5O37A_45_R64_s0.json"))
print("R64: modes", t["n_modes"], "singletons", sum(1 for x in t["mode_sizes"] if x == 1),
      "first idx within 20 nats", t["discovery_curve"]["20.0"].index(1),
      "last new mode idx", t["discovery_curve"]["1000000000.0"].index(32))              # 32, 23, 59, 53
rows = [json.load(open(f)) for f in sorted(glob.glob(f"{RAW}/g1_modes/*_R256_s0.json"))]
for L in sorted({r["L"] for r in rows}):
    R = [r for r in rows if r["L"] == L]
    pb = [r["p_hit_best_mode"] for r in R]; fw = [r["frac_within_dE"]["20.0"] for r in R]
    nn = [l["n_nonpos"] for r in R for l in r["laplace"]]
    print("L", L, "crops", len(R), "modes med", st.median(r["n_modes"] for r in R), "p_best med", round(st.median(pb), 4),
          "gain", round((1 / st.median(pb)) / q_exp(st.median(pb))[0], 1),
          "p(E<=Ebest+20) med", round(st.median(fw), 4), "gain", round((1 / st.median(fw)) / q_exp(st.median(fw))[0], 1),
          "n_nonpos", min(nn), max(nn), "D", 2 * L - 5)
print("best mode hit once:", sum(1 for r in rows if r["mode_sizes"][0] == 1), "of", len(rows))  # 16 of 87 (snapshot)

# §4.4: precision, p = 1/2 +- eps, success >= 2/3
def maj(n, p): return sum(exp(lgamma(n + 1) - lgamma(k + 1) - lgamma(n - k + 1) + k * log(p) + (n - k) * log(1 - p)) for k in range(n // 2 + 1, n + 1))
for eps in [0.1, 0.03, 0.01, 0.003]:
    tp, tm = asin(sqrt(.5 + eps)), asin(sqrt(.5 - eps))
    k = next(k for k in range(10 ** 5) if 0.5 + abs(sin((2 * k + 1) * tp) ** 2 - sin((2 * k + 1) * tm) ** 2) / 2 >= 2 / 3)
    n = 1
    while maj(n, 0.5 + eps) < 2 / 3: n += 2
    lb = (1 / 3) / abs(tp - tm); print(eps, "lb", round(lb, 2), "quantum", 2 * k + 1, "classical", n, "ratio", round(n / (2 * k + 1), 1))
# -> 1.66/3/5, 5.55/7/51, 16.67/17/465, 55.56/57/5153 (ratio 90.4)
print("asymptotic explicit/lb = 3*asin(1/3) =", round(3 * asin(1 / 3), 4))                     # 1.0195

# §4.5: Babbush form at L = 45, tC = 0.59 ms (pilot wall-clock incl. sampler overhead); thresholds M*^d, T* = tQ*M*
tC = 5.9e-4
for tQ in [1.0, 170.0, 1.7e4]:
    for d in [2, 4]:
        print(tQ, d, [(f"{(tQ*S/tC)**(d/(d-1)):.1e}", f"{tQ*(tQ*S/tC)**(1/(d-1))/86400:.3g} d") for S in [1, 30, 1e3]])
print("GPU-batched (tC/100), tQ=1 s, d=2:", [f"{(1.0*S/(tC/100))**2:.1e}" for S in [1, 30, 1e3]])
print("T2 reconciliation: (K*ell)^2 * (G ratio)^2 =", f"{(10*8.6)**2 * 10**2:.1e}", "x", f"{(1/tC)**2:.1e}", "=", f"{(10*8.6)**2*100*(1/tC)**2:.1e}")
# -> 7.4e+05 x 2.9e+06 = 2.1e+12

# §4.6: Lemma 1 vs Grover in energy queries (2 per iterate + 1 check), delta = 1/2, eps = 1/8
for M in [2 ** 10, 2 ** 20, 2 ** 40]:
    th = asin(1 / sqrt(M)); kc = floor(pi / (4 * th)); kp = next(k for k in range(10 ** 7) if sin((2 * k + 1) * th) ** 2 >= 0.75)
    lb = (0.5 - 0.125 - 1 / M) * sqrt(M) / 2
    print(M, "LB", round(lb, 1), "certainty", 2 * kc + 1, "TV1/8", 2 * kp + 1, "gaps", round((2 * kc + 1) / lb, 1), round((2 * kp + 1) / lb, 1), "TC LB", f"{0.375*M-1:.2g}")
# -> gaps 8.5/5.8 (M=2^10), 8.4/5.6 (2^20, 2^40)

# §4.1
print("full-energy range >=", round(4183.7 - 3787.2, 1), "nats -> alpha >= 10^%d" % int(396.5 / log(10)))   # 396.5, 10^172
```

---

## Response to review

Every objection from both skeptics was checked against the RAW files, the sibling notes T2 and T4, and the cited papers. All were found valid in substance and fixed (see the Review log). The points below were adopted **only in part**, or with corrected numbers, and say why.

- **R1: the Λ distribution as evidence against a first-order crossing (Skeptic 2, obj. 1(a)).** The numbers are confirmed: ≈ 1/3 of Λ lies at λ ≤ 0.05 and ≈ 10% in [0.35, 0.6]. The *inference* is not adopted. T2's Lemma 2 shows that a first-order crossing adds exactly 1 to Λ for any latent jump, so the distribution of Λ along λ cannot detect or exclude one. The evidence that does bear on the question is the smooth rung means with no variance peak, and it is confounded by non-stationarity. The requested fix was adopted in full: the bottleneck is tagged REPORTED, and the summary says "consistent with, but does not demonstrate".
- **R2: "cite the stronger T2 bound" (Skeptic 2, obj. 14).** T2's 3.2×10³ nats bounds the range of the pair term V, max V − min V, via E_{π₀}[V] − E_{π₁}[V]. This note's 396 nats bounds the range of the full energy. Neither implies the other, so both are cited with the distinction stated (§4.1), rather than one replacing the other. The extensivity sentence and "α is the wrong hardness parameter" were adopted.
- **R3: Grover-over-restarts gain under the energy predicate (Skeptic 1, obj. 4).** The skeptic's range was ≈ 2.5–4.9×, computed with near-certain success per attempt (13 calls at p = 1/64). Minimising expected calls gives k = 4 at p = 1/64: 9 calls, success 0.82, 11.0 expected calls, gain 5.8×. The reported range is therefore ≈ 2.5–5.8×. The 2k+1 accounting and the energy-predicate point were adopted in full.
- **R4: "≈ 6× at fixed 0.99 confidence" (Skeptic 2, obj. 9(d)).** This holds at matched confidence 0.988: one k = 1 attempt (3 calls) against 18 restarts. At exactly 0.99, one attempt falls just short, so two are needed (6 calls) against 19 restarts, which is 3.2×. §4.3 reports the matched-confidence figure with its confidence level.
- **R5: Hessian eigenvalue counts and "saddles" (Skeptic 2, obj. 9(c)).** `g1_mode_census.py` counts eigenvalues ≤ 10⁻⁶. The count includes flat directions (the script's own note: "tail bins, termini") as well as negative curvature, so "saddles" is not established. The counts in the R256 snapshot are 15–39 at L = 45 and 77–118 at L = 100, not 24–36 and ≈ 100. The substantive point, that these are not certified minima, was adopted.
- **R6: "> 3.9×10⁵ already exceeds the optimistic d = 2, S = 1 threshold of 3.1×10⁵" (Skeptic 1, obj. 3(b)).** That comparison pairs the L = 45 budget with the L = 150 t_C. At the L = 45 t_C (obj. 3(c), adopted) the threshold is 2.9×10⁶, and the pilot budget lies below it. No crossing is reported. The unit fix and the "this NRPT configuration only" label were adopted.
- **R7: "quantum cost Θ(√α) in the value-oracle model" (Skeptic 1, obj. 1 fix).** This holds only when ϱ = O(1/d), as Skeptic 2's obj. 13 notes. For constant ϱ, M = α·e^{−Θ(d)}. The adopted statement is: T_Q = Θ(√M) on F_M for every ϱ (via Grover over cell centres), and Θ(√α) when ϱ = O(1/d), which covers [A45]'s Theorem II.4 regime.
- **R8: "sampling adds O(1) more" (Skeptic 1, obj. 11).** Once the cell is found, sampling needs zero further queries, because the family's profile is known in closed form. Conversely, SAMPLE at TV ⅛ needs only success ≥ ¾, which lowers the constant from ≈ 8.4 to ≈ 5.6. §4.6 reports both.
- **R9: "the numbers do not match T2's break-even table" (Skeptic 2, obj. 11).** The two tables use different models, and this note's is the K = ℓ = ρ = 1 special case of T2's. They were reconciled explicitly (a factor ≈ 7.4×10⁵ at L = 45) rather than forced to match. T2's figure is named as the decision-relevant one.

---

## Review log

Skeptic 1 = first review (verdict FIXABLE, 13 objections). Skeptic 2 = second review (verdict FIXABLE, 15 objections).

| # | Location (as cited) | Objection (short) | Resolution |
|---|---|---|---|
| 1.1 | §0 item 1; S2; §3.2 step 5; table S2 | [A45]'s algorithm is not Õ(√α) on the family (ρ^{−s} ≳ α^{s/d}); tightness claim wrong | **Accepted.** Verified [A45] Thm. II.4 eqs. (12)–(14). Tightness now comes from Grover over cell centres, Θ(√M), and from amplified rejection sampling, Θ(√α) when ϱ = O(1/d). [A45]'s algorithm is restated as Õ(α^{1/2+s/d}·poly(d)), within α^{s/d}·poly(d) of optimal. Fixed in §0.1, S2, §3.2 (facts, steps 5–6, "exponential in d"), table S2, §6 (see R7) |
| 1.2 | §4.2 table; §0.5 | Fine-mesh round-trip predictions misapplied; finite-N gives 27.5/21.1/4.5 | **Accepted.** Recomputed from `rej`; the table now has finite-N predictions, fine-mesh upper bounds and Poisson P(0). The ELE-violation reading is restricted to L = 45/60, and L ≥ 100 is marked non-diagnostic with an under-provisioned schedule. §0.5 updated |
| 1.3 | §4.2 last bullet; §0.5; §4.5 | Per-rung budget used total (incl. tuning) evals; unit mismatch; t_C from wrong L; bounds only this sampler | **Accepted** (see R6 on the crossing). The figures are now production-only: 8.7 per rung per scan, 1.3×10⁴ per rung, and totals 3.9/3.4/2.7×10⁵. The comparison with thresholds is per independent sample, §4.5 is recomputed at L = 45 with t_C = 0.59 ms, and the result is labelled "this NRPT configuration (INFERENCE)". The PT parallelism column S = 30 was added |
| 1.4 | §4.3 | Grover calls miscounted (2k+1); structural predicate not implementable; recompute p | **Accepted** with corrected range (see R3). The 2k+1 accounting gives 1.5× under the structural predicate. The energy predicate is required, with p = 1–5/64 at L = 45 and a gain of ≈ 2.5–5.8×. R256 medians and the unknown-threshold constant from T4 were added |
| 1.5 | §3.8 rows | "Restart-saturated" contradicted; 200 iterations is a fixed budget | **Accepted.** Rows rewritten with 23/32 singletons, Good–Turing 0.36, 1–5/64 within 20 nats, PT lower, and the R256 statistics. "Fixed 200 iterations; convergence not verified" |
| 1.6 | §2 M8 | Analytic-well hiding false under deterministic rounding | **Accepted.** Replaced with a sufficient condition (derivatives below half an ulp, and E_0 answers at least half an ulp from boundaries) plus the enlarged-region fallback R′_s |
| 1.7 | S3; M3 | ΔE costs 4 calls under the XOR oracle | **Accepted.** k = 4 (XOR) and k = 2 (additive convention, which also satisfies M8), in S3, M3 and §3.3 |
| 1.8 | §3.5 steps 4–5 | Core mass < ½; α range | **Accepted.** The mass statement is now for the needle slot A_s, α ∈ [e^{βΔ}, e^{0.1}e^{βΔ}], and the alternative choice of e^{βΔ} for core mass ≥ ½ is noted. S6 updated |
| 1.9 | S6; §3.5 quantum bound | O(n) only in expectation; exact only up to rounding | **Accepted.** Las Vegas, expected O(n), with verification of s; TV error O(β·2^{−b}(Δ+η)); Markov gives worst-case bounded error |
| 1.10 | S4; §3.3 | Hypothesis forces E_lb = min E | **Accepted.** Restated with offset c: O(e^c α) classical, O(e^{c/2}√α) quantum |
| 1.11 | §4.6 | Lower bound in energy queries vs Grover iterations; FIND vs SAMPLE | **Accepted** (see R8). Recounted in energy queries: gap ≈ 8.4 to certainty, ≈ 5.6 for SAMPLE at TV ⅛ |
| 1.12 | §0.4(iii); S11 (R3) | "At most quartic" not proved | **Accepted.** Now reads "known speedups up to nearly quartic relative to the best known classical algorithm; no ceiling proved" (verified [C71] abstract) |
| 1.13 | §3.2 alt. proof; S5/B1; §4.4 | r = O(1/(δ−ε)); strict ε′ < ε; exact classical n at ε = 0.003 | **Accepted.** All three fixed; §4.4 now has 5,153 and 90.4, plus the closed-form ratio 3·asin(1/3) ≈ 1.0195 |
| 2.1 | §0.4; §6; §3.8; §4.2 | "Grover-like, information-local" unsupported; bottleneck not reproducible from RAW; pair-distance energies leak globally; add frustration/glassiness | **Accepted** (see R1 on the Λ-distribution inference). §0.4's last sentence was replaced. The bottleneck and "never penetrate" are tagged REPORTED (no traces in RAW, checked). §6 now says "consistent with, but does not demonstrate". Global leakage and frustration/glassiness were added to §3.7 and §3.8, plus G6 (leakage test, trace storage) and G10 |
| 2.2 | §4.2; §0.5 | Finite-N predictions; all five runs; non-stationarity; recast ELE as one hypothesis | **Accepted.** All five runs are in the table. Stationarity diagnostics (E_top quintiles, split-half rung means) were added. H1/H2/H3 are stated as competing hypotheses and tagged INFERENCE, PILOT |
| 2.3 | §4.2; §0.5; §4.5 | Budget should be production-only (1.3×10⁴); heuristic, not a bound | **Accepted** (merged with 1.3) |
| 2.4 | S7; table; §3.6; §5.2 (i) | R-vs-Q cubic separation exists [X9, X10]; R = O(Q³) conjectured | **Accepted.** Verified from full-text PDFs (Bansal–Sinha Cor. 1.5; Sherstov–Storozhenko–Wu Thm. 1.5, with Tal's 8/3). S7, §0.3, §3.6 quotes and the table updated; old caveat (i) removed and replaced by a note that Tal is cited only via [X10] |
| 2.5 | §0.4(iii); S11; §3.8 | Quartic is not a ceiling | **Accepted** (merged with 1.12); §3.8 restraint row updated |
| 2.6 | §0.1; table S1 | Lemma 1 is a lower bound, not a ceiling (hard background); "any oracle type" too broad | **Accepted.** §0.1 is restated for classically easy backgrounds. The §3.1 Remark gives the hard-background counterexample (wells on a Simon-trail background). S1 now says "any pointwise oracle satisfying M8", with the non-pointwise exclusion stated |
| 2.7 | S11; §0.4; §3.7; §3.8 | Escape-route list incomplete (DQI, short path/jump-to-end, coupled oscillators [X23]) | **Accepted.** Verified [X23] (PRX 13, 041041). (R5) was added to §0.4, S8, S11, §3.7(d), with an (R5) column in §3.8 evaluated per task. The global-minimum row now cites [C69, C70]. The list is marked non-exhaustive |
| 2.8 | §5.1 vs body | [A43], [A44], [A46], [A47] cited but not reconciled | **Accepted.** New §3.9 places each claim against S1–S11 (cost measure, comparator, evidence level), from `lit_A_sampling.md` P43, P44, P46, P47 |
| 2.9 | §3.8; §4.3 | Not restart-saturated (R256); Hessians; cost accounting | **Accepted** with corrected counts and wording (see R4, R5); merged with 1.4 and 1.5 |
| 2.10 | table S5; §4.4 | Practical column mixes query count and runtime; unsourced ε range | **Accepted.** S5's practical level is now "none"; the ratio moved to the theoretical column; the "protein-relevant ε" sentence was removed; §4.4 explains the per-call overhead |
| 2.11 | §4.5 | d = 2 on total cost optimistic; mixed L; reconcile with T2; GPU row | **Accepted** (see R9). The table is labelled as lower bounds on the break-even cost, L = 45 is used throughout, a GPU row (hypothetical) was added, and the reconciliation with T2 §4.3 is explicit |
| 2.12 | M8 | Analytic-well hiding false; enlarge R_s | **Accepted** (merged with 1.6; the enlarged-region fallback is the skeptic's fix) |
| 2.13 | S2; §3.2 | ϱ regime unstated; constant ϱ gives e^{Θ(d)} gap in α-form | **Accepted** (see R7). The ϱ regime is stated, ϱ = Θ(1/d) is inferred for [A45] Thm. II.4 (flagged in §5.2 (iv) and G4), and tightness is stated in M for all ϱ |
| 2.14 | §4.1; §0.5 | Cite T2's stronger bound; extensivity; α is the wrong parameter | **Accepted in part** (see R2). Both bounds are cited with the distinction stated; extensivity and "wrong hardness parameter" were added |
| 2.15 | G7; §3.8 free-energy row | Missing classical adversaries (multicanonical, population annealing, Boltzmann generators, prediction-centred reference); [B71] wording | **Accepted.** G7 extended with [X24], [B66], [X25], [T2-12], [A78], [T2-3] and T2's D3. The free-energy row is rephrased to separate estimator variance (S5), mixing (S1–S3, information-local only) and practical cost (§4.5), with [B71]'s wording quoted from `lit_B_estimation.md` |
