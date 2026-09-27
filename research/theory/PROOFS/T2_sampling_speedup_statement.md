# T2. Quantum sampling speedup on the prior → posterior path: precise statement, first-order bottlenecks, break-even

_Theory lane T2 of `research/THEORY_ROADMAP.md` (T2a–T2d). v1 written 2026-09-26. Status: **v2**, revised 2026-09-27 after two skeptic reviews (R1: 21 objections, R2: 16). §8 gives the responses where an objection was only partly accepted, and §9 is the full review log. The derivation is complete for the stated model. All numbers from the G1 runs are **PILOT** numbers and only indicative. Companion script: `research/theory/PROOFS/T2_sampling_checks.py` (checks C1–C6, about 2.5 min on one core because C4 simulates the replica-exchange index process; `--fast` gives about 30 s). Its output is reproduced in §4. Break-even numbers use T3's Toffoli counts G(L) (`research/theory/RESOURCE_MODELS.md`). Citation keys such as [A31] resolve in `research/literature/BIBLIOGRAPHY.md`. Keys [T2-n] are papers verified in these sessions that are not yet in the bibliography (§5.2)._

**Tags.** Every claim carries one tag.

| Tag | Meaning |
|---|---|
| **DERIVED** | Proved or computed here from the stated assumptions (proof in §3, or a check in the script) |
| **THEORETICAL [key]** | A result from the verified literature, used as its authors state it |
| **INFERENCE** | Reasoning from evidence that is not a proof, including readings of pilot data |
| **UNPROVEN** | Open. Stated as a conjecture, hypothesis or gap |
| **NO-GO** | A lower bound or impossibility statement. It is not an advantage level |
| **PILOT** | A number from the in-progress G1 runs (`research/results/RAW/g1_*`). Indicative only |
| **A-x** | A labelled assumption (§2.4) |

**Claim levels.** The repository does not yet define L0–L6, so this note uses the working definitions below. Theoretical and practical levels are kept separate. **L1–L3 are same-chain levels.** They measure a quantum algorithm against the classical chain or procedure it quantises, *not* against the best classical method. Comparison with the best classical method starts at L4. Every verdict in this note therefore gives two levels: same-chain and relative-to-best.

| Level | Kind | Meaning | Measured against | Charter category |
|---|---|---|---|---|
| L0 | — | No supported claim | — | — |
| L1 | theoretical | Query-model separation on a constructed instance family. It applies to that family only; for any other task it is L0 | all classical algorithms, on that family | 6 |
| L2 | theoretical | Walk-step or query speedup for the stated problem class, conditional on stated gap, overlap and warm-start assumptions. Oracle cost excluded | **the quantised classical chain or procedure (same-chain)** | 6 |
| L3 | theoretical | L2 plus the gate-level (Toffoli) cost of the oracle for the actual energy, giving an asymptotic fault-tolerant runtime statement | the quantised chain (same-chain) | 6 / 3 |
| L4 | practical | L3 plus the measured or proved cost of the **best classical portfolio** at the relevant L, giving a projected resource advantage under stated hardware | **best classical method** | 3 |
| L5 | practical | L4 plus small-scale compiled or simulated validation of the operator, with crossover inside a practical wall-clock | best classical method | 3 |
| L6 | practical | Hardware demonstration | best classical method | 2 / 5 |

---

## 0. Summary

1. **What QSA gives (item i).** Along the path π_λ ∝ π_0·e^{−λV}, with V = E_pair/T and an exactly preparable product prior π_0:
   - Walk-based QSA prepares a qsample |π_1⟩ with `N_walk = O( Σ_i ½(δ_{λ_i}^{-1/2} + δ_{λ_{i+1}}^{-1/2}) · K ) = K · n_b · δ_*^{-1/2}` walk steps. δ_λ is the absolute spectral gap of the quantised classical chain, δ_* is the smallest gap on the schedule, and K = O((1/p)log(1/p)·log²(ℓ/ε)) is the per-stage overhead.
   - n_b ∈ [1, ℓ] is the number of *bottleneck-equivalent* stages. It equals ℓ when all gaps are equal, which recovers the uniform bound `O(ℓ δ_min^{-1/2} …)`. It is ≈ 1 when one rung carries the bottleneck (DERIVED, §3.2; toy check C3 gives n_b = 1.01–1.22).
   - The stages must satisfy the overlap condition ⟨π_{λ_i}|π_{λ_{i+1}}⟩² ≥ p. Here the overlap is the Bhattacharyya coefficient, which has an exact closed form on this path.
   - The number of stages is ℓ ≈ 𝓛/√8. 𝓛 is the thermodynamic length. Under Gaussian fluctuations ℓ ≈ 0.63·Λ, where Λ is the Syed et al. communication barrier.
   - QSA needs a **certified lower bound on δ** to set its phase-estimation precision (A-δ). Nothing in the verified literature supplies one in the hard regime, and under-resolving δ fails silently (S1a).
   - M independent samples cost M·N_walk (no-cloning). A posterior mean to ±ε costs O((σ/ε)·N_walk).
   - **THEORETICAL [A7, A8, A31]; stage count and n_b DERIVED. Same-chain level L2 (theoretical). With T3's G(L) it is a same-chain L3 statement. Relative-to-best level: L0. Practical: L0.**
2. **Continuous samplers (item i).**
   - Quantum Langevin costs Õ(√(β d C_PI)) gradient-oracle queries and quantum replica-exchange Langevin costs √(β d/Gap), each given a warm start [A44]. On the λ-path, that warm start is exactly the same Bhattacharyya overlap condition.
   - The first provable continuous-domain separation is Ω(α) classical vs Õ(√α) quantum, with α = e^{βΔ}, on hide-and-seek instances [A45]. It is the only one in the verified bibliography.
   - For the **full** learned energy, βΔ ≥ E_{π_0}[E_pair] − E_min ≥ 3.1×10³ nats at L=45 and 5.4×10⁴ at L=150 (PILOT, C4). This is consistent with T5's weaker bound (≥ 396 nats), since both are lower bounds. So α gives no usable runtime.
   - **[A44]: same-chain L2. [A45]: L1 for its own instance family, L0 for the A80 task.**
3. **First-order bottleneck (item ii).**
   - At a two-phase crossing, the continuum barrier Λ grows by 1 + O(s/ΔV) and the thermodynamic length by at most π + O(s/ΔV), whatever the latent jump ΔV (s is the within-phase SD). Λ and any schedule adapted to it are therefore insensitive to the crossing.
   - The exact two-point overlap shows the crossing needs exactly one intermediate rung, so at most 2 QSA stages (**DERIVED**, Lemma 2).
   - Every admissible schedule has a rung at which both phases carry mass ≥ ≈ p/4. There the chain gap satisfies δ ≤ (8/p)·e^{−ΔF‡(λ_c)}, where ΔF‡ is the interface free-energy barrier (**DERIVED** from the upper half of Cheeger's inequality and an exponential-family bound, Prop. 3).
   - **Halving is rigorous in δ, not in ΔF‡.** For the same chain, QSA costs Θ̃(δ_*^{-1/2}) and classical annealing Θ̃(δ_*^{-1}) (**DERIVED**, given A-δ). Converting to e^{ΔF‡/2} vs e^{ΔF‡} requires the Arrhenius-type assumption A-Arr, δ_* = C^{-1}e^{−a·ΔF‡} (**INFERENCE**; toy check C3 fits a ≈ 1.10, ln C ≈ 5.4). The lower half of Cheeger's inequality gives only δ ≥ Φ²/2 ~ e^{−2ΔF‡}.
   - Classical λ-tempering is torpid (**THEORETICAL [E40, E39]**; transfer to this path is INFERENCE). SMC from the prior needs ~1/q_F lineages, and a seed-coherent reversible version needs ~1/√q_F (INFERENCE).
   - Adiabatic evolution with the chain's own Hamiltonian adds nothing beyond S1. Physical quantum annealing does not target π_1.
   - In the black-box needle model, halving is optimal (**NO-GO**, [C55] via a DERIVED blocking reduction, §3.7).
4. **What the pilot's zero round trips mean (items ii, v).**
   - v1's prediction of 27.5 (L=45) and 21.1 (L=60) round trips was the *stationary* rate. Each label's round-trip time, 2N(1+E(P_N)), is longer than every pilot run, and production starts from identity labels. The correct ELE prediction therefore comes from simulating the index process from that start (C4): **9.8 ± 2.6 (L=45), 4.8 ± 1.9 (L=60), ≈ 0 at L ≥ 100**.
   - **0** were observed. Under exact ELE and stationarity, P(0) ≈ 5×10⁻⁵ (L=45) and 3.7×10⁻³ (L=60). The deficit is significant at L=45 (one crop, one seed), marginal at L=60, and the L ≥ 100 runs carry no information (PILOT; C4).
   - Both assumptions behind the prediction are visibly violated. The rungs are non-stationary (A1). The pilot also ran n_expl = 1 HMC trajectory per rung per scan and no pivot moves, far below the range Syed et al. tested (A2).
   - That the deficit reflects small stationary fixed-λ gaps (the quantity QSA square-roots) is therefore a **HYPOTHESIS (UNPROVEN)** for D3/D4.
5. **Classical bypasses (item iii).**
   - A first-order transition is a property of the *path*, not of π_1. Classical routes around it include:
     - other paths: temperature, spline or variational reference [T2-2, T2-3], interpolation to independence [T2-12], entropy dampening [E40];
     - multicanonical sampling [T2-8];
     - **nested sampling** [B67, T2-14, T2-15], which compresses in prior mass rather than in λ;
     - mode finding + local sampling + reweighting.
   - When such a bypass costs poly(L), a QSA on the λ-path is **exponentially worse** than the classical bypass (**DERIVED** from S3 + S5).
   - Provable quantum speedups square-root at most the cost of a *quantisable* classical procedure. That includes reversible chains and classical randomised procedures run reversibly over a seed register, **SMC/population annealing included**: resampling copies classical registers, which fan-out does coherently, so no-cloning does not apply.
   - What is not known is a quantum speedup of SMC's internal sequential mixing, or a garbage-free qsample from it (INFERENCE).
   - Beyond-quadratic claims exist only as heuristic small-n fits for diagonal Ising costs [A47, A52, A54]. They are disputed [A48] and killed for this program (OPPORTUNITY_MATRIX M7).
6. **Break-even (item iv).** Per posterior sample, a λ-path QSA beats the best classical portfolio iff
   `ρ · K · n_b · G(L) · t_T · √τ_*(L)  <  c(L) · B_best(L)`.
   - τ_*(L) is the relaxation time of the quantised chain at the bottleneck, in local steps. B_best(L) is the per-sample cost of the best classical method, in the same unit. G is Toffolis per walk step (from T3). t_T is seconds per Toffoli. c is seconds per classical energy+gradient. ρ is the *cost* of one quantum-computer-second in core-seconds.
   - With B_best = τ_*/A, the condition becomes `τ_* > B* := (A·ρ·K·n_b·R)²`, where R = G t_T/c.
   - Inputs (C6): T3's G(L), c(L) overhead-corrected, ρ = 1, and **A = 1 (no classical bypass and κ_chain = 1; both quantum-favourable)**. The break-even classical cost is then:
     - **B\* ≈ 1.0×10¹⁰ (L=150) to 2.7×10¹⁰ (L=45)** in the single most optimistic scenario. That scenario is T3-D3, a Cartesian model that samples a different, bond-relaxed target, with t_T = 1 µs, K = 10 and n_b = 1.
     - **1.1–4.0×10¹¹** for the most optimistic scenario on the A80 target itself (T3-D2 generous);
     - ~10¹⁷ at A-FO central values (T3-D2 central, t_T = 10 µs, K = 100, n_b = 2);
     - up to ~10²⁵ at pessimistic values (C6, §4.3). B\* ∝ n_b², so the choice between the two stage-count estimators matters in the glassy columns.
   - **Corollary (DERIVED): minimum useful runtime.** An advantage on this route needs a quantum wall-clock per sample of at least **T\*_Q = A·ρ·(K n_b G t_T)²/c ≥ (K n_b G t_T)²/c**, *whatever the classical cost*.
     - At t_T = 1 µs, K = 10, n_b = 1 this is 0.26–0.59 yr (T3-D3 target) and 1.05–20 yr (A80 target).
     - At A-FO central values it is ≥ 9×10⁵ yr.
     - Bringing T\*_Q down to one day needs t_T ≤ 12–51 ns (A80 target, most optimistic) or 0.12–0.55 ns (A-FO central). That is 3.5 to 6 orders of magnitude faster than the 170 µs of [A56].
   - The machine in question has 6×10³–5×10⁴ logical and 1.3×10⁷–10⁸ physical qubits (T3). ρ = 1 prices it as one core.
   - The pilot only lower-bounds classical cost, at ≈ 2×10⁴ local steps per round trip at L=45–60 (transit-aware, 95%, model-dependent). At L ≥ 100 the runs carry no information; the ELE-ideal cost per round trip there is 6×10⁴–10⁵. "One round trip per independent sample" is an INFERENCE.
   - Amplitude-amplified multistart needs p_hit < p\* = 7×10⁻¹⁹ to 1×10⁻¹¹. The resolved pilot targets have p_hit ≥ 0.008. Floor-censored targets are unresolved (PILOT).
7. **Decision (item v).** Relevance is decided by eight classical measurements, D1–D8 (§1 S7):
   - the nature of the bottleneck (first-order vs glassy);
   - ΔF‡(L), with a pre-registered extrapolation model;
   - the ELE gap, with n_expl and N scanned;
   - τ_*(L) from stationary starts;
   - B_best(L), with cross-validated basin populations, including nested sampling;
   - p_hit(L) and the basin-mass vs hit-rate relation;
   - c(L), benchmarked on an idle node;
   - temperature sensitivity.

   **Current verdict (INFERENCE, pilot-level):**
   - **Same-chain walk-step speedup: L2 in theory (L3 with T3's G(L)), L0 in practice.**
   - **Advantage over the best classical sampler: L0 at every level, theoretical and practical.** It is provably negative wherever a polynomial classical bypass exists (S5).
   - Break-even needs B_best(L) ≥ B\*: at least ~10¹⁰ (any target) or ~10¹¹ (A80 target) under the most optimistic assumptions.
   - **The pilot only shows B_PT ≳ 2×10⁴–10⁵ local steps per round trip, and neither establishes nor excludes B_best ≥ B\*.** D4 and D5 decide.
   - The robust negative part does not depend on the classical cost. Any advantage comes at a per-sample runtime of at least T\*_Q: months in the single most optimistic scenario, years or more for the A80 target, unless t_T reaches the ns range.

---

## 1. Statements

**Notation.**
- L is the number of residues. x = (θ_1..θ_{L−2}, τ_1..τ_{L−3}) are the internal coordinates, so d = 2L−5.
- V(x) := E_pair(x)/T and U_0(x) := E_prior(x)/T.
- π_λ(x) ∝ e^{−U_0(x) − λV(x)} for λ ∈ [0,1]; π_0 is the learned product prior and π_1 is the posterior. A(λ) := log Z_λ.
- |π⟩ := Σ_x √π(x)|x⟩ on a grid Ω (A-grid). BC(λ,λ′) := ⟨π_λ|π_λ′⟩ = Σ_x √(π_λ π_λ′) is the Bhattacharyya coefficient.
- P_λ is a reversible π_λ-invariant chain. μ_2(P_λ) is its second-largest eigenvalue. δ_λ is its **absolute** spectral gap, 1 − max(μ_2, |μ_min|) (equal to 1 − μ_2 for a lazy chain; A-rev). τ_λ := 1/δ_λ.
- Var_λ is the variance of V under π_λ. 𝓛 := ∫_0^1 √Var_λ dλ is the thermodynamic length [T2-9].
- λ_loc(λ) := ½E|V_1−V_2| with V_1, V_2 i.i.d. under π_λ, and Λ := ∫_0^1 λ_loc dλ is the communication barrier [T2-1].
- δ_* := min_i δ_{λ_i} over the schedule rungs. n_b := ½Σ_{i=0}^{ℓ−1}[(δ_*/δ_{λ_i})^{1/2} + (δ_*/δ_{λ_{i+1}})^{1/2}] ∈ [1, ℓ] (§3.2).
- K is the QSA overhead per stage (A-K). n_loc (§3.4) is the number of local moves spent near λ_c. H := V − min V ≥ 0 is Harrow–Wei's shifted potential (their "L").
- **T3-D1/D2/D3** are T3's walk-step *designs* (RESOURCE_MODELS.md). **D1–D8** (S7) are this note's *measurements*.

### S1. Walk-based QSA along the λ-path (item i)

Let 0 = λ_0 < … < λ_ℓ = 1 with BC(λ_i, λ_{i+1})² ≥ p for all i, let |π_0⟩ be preparable, and let a lower bound on every δ_{λ_i} be known (A-δ). Then:

**(a) Qsample.** |π_1⟩ can be prepared to 2-norm error ε with

`N_walk = O( ℓ · δ_min^{-1/2} · (1/p) log(1/p) · log²(ℓ/ε) )`

walk steps, where δ_min = min_i δ_{λ_i}.
- **THEORETICAL [A7]**, as restated in [A31] Thm 5, verified in the v1 session from the arXiv PDF of 1907.09965.
- The stage-resolved form is `N_walk = O( K · Σ_i ½(δ_{λ_i}^{-1/2} + δ_{λ_{i+1}}^{-1/2}) ) = O(K · n_b · δ_*^{-1/2})`, with K := (1/p)log(1/p)·log²(ℓ/ε). It is **DERIVED** from the same construction (§3.2).
  - Stage i uses O((1/p)log(1/p)) approximate reflections about |π_{λ_i}⟩ and |π_{λ_{i+1}}⟩, each by phase estimation on W(P_{λ_i}) or W(P_{λ_{i+1}}) at phase precision ~√δ [A2].
  - n_b = ℓ for uniform gaps. n_b ≈ 1 when a single rung carries the bottleneck.
- **Hidden input (A-δ).** The phase-estimation precision is set from a *known* lower bound on δ ([A7]; [A31] Thm 5 and Thm 10 take it as input).
  - If δ is overestimated, the approximate reflection treats slow eigenvectors as stationary. The output is then biased toward the metastable branch, with no internal signal.
  - This is the same silent-hysteresis failure that S3(c) attributes to classical annealing.
  - Classical runs give only *upper* bounds on δ (lower bounds on τ from non-observation). No procedure in the verified literature certifies the needed lower bound here. **UNPROVEN** that one exists.
- Somma et al. give the same 1/√δ dependence for the annealing-to-optimum task [A8, C74].
- Harrow–Wei [A31] Thm 10 constructs the schedule adaptively for exactly this Bayesian form π_β ∝ π_0 e^{−βH}. Their total is `Õ(√(E_{π_0}[H]) / √δ)`, with schedule length ℓ = O(√E_{π_0}[H] · log E_{π_0}[H]) (Thm 4, p = e^{−2}).

**(b) Overlap and stage count on this path.** **DERIVED** (Lemma 1, §3.1).
- The identity `BC(λ,λ′) = exp( A((λ+λ′)/2) − ½A(λ) − ½A(λ′) )` is exact (check C2: max error 3×10⁻¹⁶).
- To second order, −ln BC = (Δλ)² Var_{λ̄}/8.
- For BC² ≥ p, i.e. BC ≥ e^{−κ} with κ = ½ln(1/p), the stage count is `ℓ ≈ 𝓛/√(8κ)`. That is 𝓛/√8 at Harrow–Wei's p = e^{−2}.
- Cauchy–Schwarz gives 𝓛 ≤ √(E_{π_0}[V] − E_{π_1}[V]). Under Gaussian V-fluctuations, 𝓛 = √π·Λ, so ℓ ≈ 0.63·Λ.
- **PILOT, two estimators** (C4; both from non-stationary replicas, so both are indicative):

  | L | 45 | 60 | 100 | 120 | 150 |
  |---|---|---|---|---|---|
  | ℓ ≈ 0.63·Λ (Gaussian conversion) | 8.5 | 9.0 | 15.6 | 15.8 | 18.3 |
  | ℓ = 𝓛/√8, 𝓛 from per-rung SD of V | 8.7 | 9.9 | 23.4 | 21.3 | 62.2 |

  - The two agree at L ≤ 60 and differ by 3.4× at L=150.
  - The Cauchy–Schwarz values √(E₀V−E₁V)/√8 = 20 / 21 / 51 / 61 / 82 are a *pilot estimate of the bound*. They are biased low because the λ=1 mean is still drifting down, so they are not valid upper bounds.
- **B\* ∝ n_b² ≤ ℓ².** The stage count matters only where many rungs are slow (the glassy case, S6). There the estimator choice moves B\* by up to 11× (ℓ) or 30× (n_b at λ ≥ 0.3) at L=150.
- **The schedule length is never the bottleneck. The gaps are.**

**(c) M samples and estimation.**
- M independent samples from π_1 cost M·N_walk. A qsample is consumed by measurement and cannot be copied. Harrow–Wei state this obstruction explicitly for reusing intermediate states along annealing schedules [A31 §5]. **THEORETICAL [A31]** plus **DERIVED** (no-cloning).
- A posterior expectation of a bounded-variance scalar observable to ±ε costs O((σ/ε)·N_walk) walk steps, against O((σ/ε)²·B_sample) classically. **THEORETICAL [A30]** (quadratic in 1/ε, query model).
- Classical counterparts:
  - **Annealing with the same chains**, where each stage must mix from the previous stage's output, costs O(Σ_i τ_{λ_i}·[½ln(1+χ²(π_{λ_{i−1}}‖π_{λ_i})) + ln(1/ε_i)]) local steps per sample.
    - This is **DERIVED** from the spectral bound ‖μP^t/π − 1‖_{2,π} ≤ (1−δ)^t‖μ/π − 1‖_{2,π}, which needs the absolute gap.
    - The warm-start factor is set by χ², not by BC. On this path it is exact: `1+χ²(π_{λ}‖π_{λ′}) = exp(A(2λ−λ′) + A(λ′) − 2A(λ))` (C2 verifies this to 2×10⁻¹⁶).
    - 1+χ² ≈ BC^{-8} for small steps. It is far larger across a jump: C3 finds 1+χ² ≈ 10³⁵ across the forced stage at n = 100, where BC² ≥ e^{−2} holds.
  - **AIS and SMC** do not require each stage to mix. Their cost is governed by the variance of the importance weights [E75] and, for SMC with resampling, by local-mixing conditions [T2-12, T2-13], not by Σ_i δ_{λ_i}^{-1}. **THEORETICAL.**
  - **Non-reversible PT** under ELE and stationarity costs (2+2E(P_N)) scans per round trip, with E(P_N) = Σ_k r_k/(1−r_k) → Λ as N → ∞. **THEORETICAL [T2-1]** (Thm 1, Cor. 1, Thm 3, verified from the arXiv PDF). Syed et al. report round trips per unit cost correlating with ESS per unit cost [T2-1].
- **The gain in (a)–(c) is relative to the chain P_λ that is quantised** [A31; `literature/QUANTUM_PRIMITIVES.md` §1.1]. It is a same-chain statement (L2), not a relative-to-best one.

**(d) Cold start and the cost of |π_0⟩.**
- Without the path, the generic quantum mixing cost is O(√δ⁻¹·√|Ω|) [A9]. General qsampling would imply SZK ⊆ BQP [A11].
- Here |π_0⟩ = ⊗_i |π_0^{(i)}⟩ is a product of per-residue (θ_i, τ_i) states. Generic amplitude loading at b bits per angle would cost O(L·2^{2b}) gates, i.e. up to L·2⁴⁰ at b = 20, which is prohibitive.
- The prior, however, is a table at its native resolution: `ExactPrior` uses a 0.5° × 1° grid, i.e. 360 × 360 = 1.3×10⁵ cells per residue. **DERIVED** cost:
  - Load each residue's table by QROM-based amplitude loading. The cost is linear in the number of entries, per T3's reading of [A60]; T2 has not re-verified it. That is ~1.3×10⁵–10⁶ Toffolis per residue (the upper end allowing ~10 Toffolis per entry for amplitude precision), and ≈ 5×10⁶–5×10⁷ (L=45) to 2×10⁷–2×10⁸ (L=150) in total.
  - Put the finer walk-grid bits in uniform superposition (Hadamards). This is the coherent analogue of ExactPrior's uniform jitter.
  - This is comparable to one to a few walk steps (G ≈ 5×10⁶–5×10⁸, T3), so it is negligible against N_walk.
- π_0 is the λ=0 law **exact up to grid discretisation** (`src/qapf/sampling/hrex.py` `ExactPrior`: piecewise-constant cells with uniform jitter). The TV error is O(h/σ) per coordinate and the bias of smooth expectations O((h/σ)²), with h/σ ≈ 0.12 (θ) and 0.17 (τ) against the soft-bin widths. The same caveat applies to the classical sampler.
- Direct amplitude amplification from |π_0⟩ to |π_1⟩ would instead cost ~1/BC(0,1) reflections. With BC(0,1) = e^{A(½)−(A(0)+A(1))/2}, this is exponentially small in L for this energy (INFERENCE from 𝓛 ≫ 1).

*Claim level: same-chain L2 (theoretical); L3 with T3's G(L). Relative-to-best: L0. Practical: L0.*

### S2. Continuous-space samplers (item i)

- **THEORETICAL [A44]** (Leng et al., PNAS 2026). Gibbs sampling of σ ∝ e^{−βV} via the Witten-Laplacian kernel and singular-value thresholding costs:
  - Õ(√(β d C_PI)) gradient-oracle queries for Langevin;
  - √(β d / Gap(ℒ†))·polylog(d,1/ε) for replica-exchange Langevin (RELD);
  - both given a warm start |⟨φ|σ⟩| = Ω(1).
- The "up to quartic" speedup in [A44] is measured against MALA's Cheeger-based bound. Against Poincaré scaling it is quadratic (`literature/QUANTUM_PRIMITIVES.md` §1.3). Either way it is same-chain: it is relative to the classical Langevin/RELD dynamics being quantised.
- **DERIVED (composition) + INFERENCE (warm-start transfer).** On the λ-path, the warm start at stage i+1 is supplied by the qsample at stage i, with overlap BC(λ_i, λ_{i+1}) ≥ √p.
  - The cost per qsample of π_1 is then Σ_i √(β d/Gap_i)·polylog, where Gap_i = 1/C_PI(π_{λ_i}), or the RELD gap if a replica-exchange generator is quantised. This has the same structure as S1 with δ_i ↔ Gap_i/(βd).
  - The query is a **gradient** oracle, so the per-query cost is G_grad ≈ 3G (A-Ggrad).
  - (θ, τ) is not a torus: θ is walled and τ is periodic. The smoothness and domain conditions of [A44, A45] therefore hold only approximately (A-dom).
- **THEORETICAL [A45]** (Olivucci et al., arXiv 2608.24527; abstract re-verified in v1).
  - On 𝕋^d with s-Gevrey potentials and α = e^{βΔ}, Δ = max E − min E of the whole sampled potential: every classical algorithm querying values or derivatives needs Ω(α) queries, while a QSVT + temperature-annealing algorithm needs Õ(√α).
  - The abstract calls this the *first* provable continuous-domain sampling separation. It is the only one in the verified bibliography. It is quadratic.
- **DERIVED (bound) + PILOT (numbers). α for the full energy.**
  - The head probabilities are ≤ 1 and the wall is ≥ 0, so E_prior ≥ −10⁻⁶ per residue. Hence max E ≥ E_pair(x) for any prior draw x, and min E ≤ E_polished (the polished lowest energy).
  - So βΔ ≥ E_{π_0}[E_pair] − E_polished = **3.1×10³ nats (L=45), 3.4×10³ (L=60), 2.0×10⁴ (L=100), 2.9×10⁴ (L=120), 5.4×10⁴ (L=150)** (C4).
  - T5 (`NO_GO_RESULTS/T5_quadratic_ceiling.md` §4.1) gives the weaker lower bound β(max E − min E) ≥ 396 nats from the spread of local minima. Both are valid, and they do not conflict.
  - Õ(√α) is therefore astronomically loose as a runtime. What [A45] contributes is that quadratic is achievable and optimal on its hard class. It says nothing about instances whose classical cost is ≪ α.

*Claim level: [A45] L1 for its own instance family and L0 for the A80 task; [A44] same-chain L2. Relative-to-best: L0. Practical: L0.*

### S3. A first-order-like transition along λ (item ii)

**Model (A-FO).** There is a λ_c ∈ (0,1) and two disjoint regions (phases) U (unfolded, prior-like) and F (folded), separated by an interface region I. In a window W ∋ λ_c, π_λ ≈ w_F(λ)·π_λ^F + (1−w_F(λ))·π_λ^U, with:
- w_F(λ) = σ((λ−λ_c)ΔV), where ΔV = E_U[V] − E_F[V] > 0 is the latent jump, σ is the logistic function, and ΔV ≫ 1;
- within-phase standard deviations s_U, s_F ≪ ΔV;
- for local chains, the probability flux between U and F passes through I, with e^{−ΔF‡(λ)} := π_λ(I)/min(π_λ(U), π_λ(F)). ΔF‡ is the interface free-energy barrier seen from the minority phase.

**(a) Λ and 𝓛 are insensitive to the jump.** **DERIVED**, Lemma 2, check C1.
- The crossing adds 1 + O(s/ΔV) to Λ and at most π + O(s/ΔV) to 𝓛, for every ΔV.
- The exact two-point overlap shows it needs exactly one intermediate rung, with w_F ∈ [p, 1−p], so at most 2 QSA stages at p = e^{−2} (C1; C3 confirms 2 stages).
- Under ELE it adds ≈ 2 scans to an NRPT round trip.
- **What is blind is the continuum Λ and any schedule adapted to it.** On a fixed λ-grid with spacing Δλ ≫ 1/ΔV, a populated jump *is* visible: the straddling pair's swap acceptance is ≈ e^{−ΔλΔV} (§3.3). On a grid finer than 1/ΔV it appears only as an O(1) bump in the rejection profile.

**(b) The gap closes.** **DERIVED**, Prop. 3.
- The Cheeger upper bound δ ≤ 2Φ for reversible chains (a standard inequality, not re-verified in these sessions) gives δ_λ ≤ 2e^{−ΔF‡(λ)} for local P_λ.
- Every admissible schedule has a rung λ_s at which both phases carry mass ≳ p/4. Under an exponential-family monotonicity condition (A-mono, §3.4), δ_{λ_s} ≤ (8/p)·e^{−ΔF‡(λ_c)}.
- The matching *lower* bound on δ, which a cost *upper* bound needs, is not derived. Cheeger's lower half gives only δ ≥ Φ²/2 ~ e^{−2ΔF‡}. Arrhenius-type scaling δ_* = C^{-1}e^{−aΔF‡} is assumption **A-Arr (INFERENCE)**, supported by the toy check C3.

Toy check C3 uses a cooperative mean-field chain whose λ=0 law is a product, so it has the same structure as this program's prior. It gives:

| n | ΔF‡ (nats) | δ_min | Λ | 𝓛 | stages | BC(λ_c ± 0.08) | n_b (greedy schedule) | w_F at the forced rung |
|---|---|---|---|---|---|---|---|---|
| 25 | 3.7 | 8.5×10⁻⁵ | 1.06 | 3.27 | 2 | 0.49 | 1.22 | 0.864 |
| 50 | 8.2 | 5.3×10⁻⁷ | 1.04 | 3.32 | 2 | 0.11 | 1.07 | 0.864 |
| 75 | 12.6 | 4.3×10⁻⁹ | 1.05 | 3.37 | 2 | 0.025 | 1.02 | 0.858 |
| 100 | 17.1 | 3.9×10⁻¹¹ | 1.05 | 3.41 | 2 | 0.005 | 1.01 | 0.857 |

The fit is −ln δ_min = 1.095·ΔF‡ + 5.4 (A-Arr: a ≈ 1.10, ln C ≈ 5.4, in single-flip-attempt units). The forced rung sits at w_F ≈ 1−p, as the two-point calculation predicts, and carries essentially all of the bottleneck.

**(c) Classical costs.**
- **Annealing along λ without a bypass:** ≳ e^{ΔF‡} local steps per sample under A-Arr. Otherwise the output follows the metastable branch (hysteresis) and is silently biased. **INFERENCE** from (b).
- **Simulated or parallel tempering:** torpid. **THEORETICAL [E40]** (arXiv abstract re-verified in v1): for the mean-field 3-state Potts model, "tempering converges slowly regardless of the temperature schedule chosen", and the mixing time is "an exponential factor longer than the mixing time at the fixed temperature". **THEORETICAL [E39]**: when narrow and wide peaks carry comparable mass, PT/ST mix torpidly, and "commonly used convergence diagnostics will fail to detect" it. That these results transfer to the learned λ-path is **INFERENCE**.
- **SMC / population annealing with R particles from the exact prior:** exact as R→∞.
  - Finite R needs R ≳ 1/q_F. Here q_F ≈ max(π_0(F), n_loc·e^{−ΔF‡}) is the probability that one lineage enters F, and n_loc is the number of local moves spent near λ_c (**INFERENCE**, §3.4). Resampling then amplifies the lineages that entered F.
  - This classical rare-event cost is 1/q_F. A seed-coherent, reversible lineage with a checkable "entered F" predicate can instead be amplitude-amplified with ~1/√q_F lineage runs times a reversibility overhead [B1] (**INFERENCE**; S5.2).

**(d) Quantum walk / QSA / continuous samplers.** **DERIVED** from S1 + (b) + Prop. 3 item 2.
- The crossing **cannot be skipped**, because **Prop. 3 item 2** forces a rung λ_s with min(π(U), π(F)) ≳ p/4, which the separating set I then bottlenecks.
  - The exponentially small overlap of the two pure phases (C3: 0.49 → 0.005 as n goes 25 → 100; two-phase model 2e^{−hΔV/2}, §3.4) shows why a direct jump is forbidden. The separating-set argument is what forces the rung.
- This algorithm spends Θ(δ_{λ_s}^{-1/2}) walk steps per reflection at that rung. Hence N_walk ≥ Ω(δ_{λ_s}^{-1/2}) ≥ √(p/8)·e^{ΔF‡(λ_c)/2} for QSA as constructed. This is a statement about the algorithm, not a lower bound over all quantum algorithms.
- **Halving (DERIVED in δ):** Θ̃(δ_*^{-1/2}) quantum vs Θ̃(δ_*^{-1}) classical annealing with the same chain. **In the exponent (A-Arr):** ~e^{aΔF‡/2} vs ~e^{aΔF‡}. The exponent is halved at best, not removed.
- The same holds for [A44] with Gap ↔ e^{−βΓ} (QUANTUM_PRIMITIVES §1.3: "C_PI will grow exponentially with β·Γ").

**(e) Lower bound in the black-box model.** **NO-GO** (a lower bound, not an advantage level). **DERIVED** blocking reduction (§3.7) plus **THEORETICAL [C55, A45]**.
- Suppose F is hidden: V is uninformative outside F, π_1(F) ≥ ½ and π_0(F) = q. Then a sampler for π_1 within TV ¼ finds a point of F with probability ≥ ¼, so it solves search with a qN-marked oracle.
- Grouping items into ⌊1/q⌋ blocks with one marked block reduces single-marked search over ⌊1/q⌋ blocks to it. The problem therefore needs Ω(q^{−1/2}) quantum queries [C55] and Ω(q^{−1}) classical queries.
- Halving is therefore optimal for needle-type instances. For structured learned energies, whether quantum can beat halving, or whether classical can avoid the exponential altogether, is **UNPROVEN** in either direction.

**(f) Adiabatic routes.**
- (i) **Markov-chain Hamiltonian.** H_λ := I − D_λ, with D_λ = Π^{1/2} P_λ Π^{−1/2}, is stoquastic and has ground state |π_λ⟩. Its spectral gap is exactly 1 − μ_2(P_λ), which equals δ_λ for a lazy chain (**DERIVED**, §3.5).
  - Adiabatic evolution costs poly/δ_* or worse [A11]. Eigenpath traversal costs O(path length/gap) [A34].
  - With spectral-gap amplification, which is available for frustration-free H and optimal there [A33], the cost drops to ~δ_*^{-1/2}, the same as QSA. **THEORETICAL [A33, A34] + DERIVED.**
- (ii) **Physical transverse-field annealing.** **THEORETICAL.**
  - Gaps close exponentially at first-order quantum transitions. The models reduce to Grover in a limit [T2-4], and are reviewed in [T2-5].
  - Anderson-localisation-type exponentially small gaps appear near the end of the anneal for the standard transverse-field algorithm [T2-6]. This result is **contested in general**: Choi shows the argument holds only for a specific AQO Hamiltonian, and gives different AQO algorithms for the same problems that evade it [T2-16].
  - Laumann et al. argue that thermodynamic order alone is not predictive, but that MBL-like phases give typically exponentially small gaps [T2-7].
- The physical annealer targets a ground state, not π_1 at T=1. Its output temperature is uncontrolled [A61–A63], and classical QMC reproduces its tunnelling scaling [A64]. **Not a route to π_1 (KILLED for this purpose; INFERENCE consistent with `QUANTUM_PRIMITIVES.md` §1.7).** This conclusion does not depend on [T2-6].

*Claim level: (d) same-chain L2 conditional on A-FO and A-δ (halving in the exponent also needs A-Arr); (e) NO-GO. Relative-to-best: L0. Practical: L0.*

### S4. What the pilot's round-trip count does and does not measure (items ii, v)

**DERIVED** (from [T2-1] Thm 1 / Cor. 1, a simulation of the DEO index process in C4, and S3a) + **INFERENCE** (PILOT).
- **Stationary rate.** Under stationarity (A1 in [T2-1]) and ELE (A2), the non-reversible PT round-trip rate is 1/(2+2E(P_N)) per scan, summed over replicas [T2-1 Cor. 1]. Each label's expected round-trip time is 2N(1+E(P_N)) scans, for N rungs [T2-1 Thm 1].
- **Initial transit.** In the pilot, 2N(1+E) = 1,640 (L=45), 1,820 (L=60), 6,900 (L=100), 6,800 (L=120) and 11,800 (L=150) scans. Each is longer than its run (1,500 / 1,200 / 800 / 600 / 500 scans).
  - Production starts from identity labels (`hrex.py` `run_nrpt`: `track = arange(N)`, `last_end = −1`) and counts a trip only after bottom → top → bottom.
  - The transit correction is therefore O(1) per label and **O(N) in aggregate**. v1's "O(1)" was wrong.
- **Transit-aware prediction.** C4 simulates the index process under exact ELE, with each run's measured r_k, the production initial state and the production counting rule (20,000 replicates). It predicts:
  - **9.8 ± 2.6 round trips (L=45) and 4.8 ± 1.9 (L=60)**, and ≈ 0 at L = 100, 120, 150;
  - against the stationary 27.5, 21.1, 4.5, 3.3 and 1.7 that v1 reported.
  - A long run of the same simulation reproduces the stationary rate (0.01831 vs 1/(2+2E) = 0.01834 per scan at L=45; validation run, not in the script).
- **Zero were observed** in all five runs.
  - Under exact ELE and stationarity, P(0) ≈ 5×10⁻⁵ at L=45. C4 found 1 of 20,000 replicates; a second seed found 0 of 20,000. A Poisson law with the simulated mean gives e^{−9.8} ≈ 6×10⁻⁵, and the simulated count is under-dispersed.
  - P(0) = 3.7×10⁻³ at L=60.
  - At L ≥ 100, zero trips is exactly what ELE predicts.
  - v1's Poisson values (10⁻¹² and 10⁻⁹) were wrong. **The deficit is significant at L=45 (one crop, one seed), marginal at L=60, and uninformative at L ≥ 100.**
- **Attribution.** Both assumptions behind the prediction are visibly violated in the pilot:
  - **A1 (stationarity):** the rungs at λ ≥ 0.3 drift down by 1–26 nats (L=45) up to 326–732 nats (L=150) between the two halves of each run (§4.1d).
  - **A2 (ELE):** production ran one HMC trajectory (8 leapfrog steps) per rung per scan, with no pivot moves (§2.2). That is n_expl = 1 against d = 85 variables at L=45, up to 295 at L=150.
    - [T2-1 §7.2] tested n_expl ∈ {0, d/2, d, 2d, …, 32d}, and reports that "increasing n_expl reduces the difference between the theoretical and observed round trip rate" (text re-read from the arXiv PDF in this revision).
    - The pilot sits below the smallest non-zero value tested.
  - The deficit therefore cannot yet be attributed to small stationary fixed-λ gaps δ_λ. **That it reflects them is a HYPOTHESIS (UNPROVEN).** D3 (scan n_expl and N) and D4 (τ_* from stationary starts) separate the three causes: A1 violation, A2 violation, and small δ_λ.
- **Reliability of Λ.** [T2-1 §7.2] shows empirically that λ is "reliably estimated even when ELE is severely violated, provided n_expl > 0".
  - The estimator measures swap rejection under the rung marginals the replicas actually have. Under the non-stationarity of §4.1(d), the pilot's Λ and E(P_N) are themselves suspect (INFERENCE). Its rejection profile says nothing about a jump, because F is never populated (§3.3, consequence iv).
- **Scale.** Λ(L) itself is small and grows roughly linearly (≈7 → 29 over L = 30 → 150, PILOT).
  - If ELE and stationarity held, classical NRPT would cost only ~(2+2E)·s(L) ≈ 1.4×10⁴ (L=45) to 1.0×10⁵ (L=150) local steps per round trip (C4), which is polynomial. In that regime no quantum walk is relevant (S6).
- **Hence, conditional on the hypothesis above, the quantity that decides relevance is τ_*(L) = 1/δ at the bottleneck, not Λ(L).**
- **Bottleneck type.** The pilot does not yet show which kind of bottleneck it is (INFERENCE, §4.1):
  - The rung-mean E_pair is smooth in λ, with no variance peak near λ ≈ 0.4–0.5.
  - The rungs at λ ≥ 0.3 are still drifting (§4.1d).
  - The observations fit a first-order crossing seen out of equilibrium, but they fit glassy multi-basin trapping (persistence, [E39]) equally well. S7 D1 separates the two.
- **Provenance note (PILOT).** The C4 rows describe HMC-only production runs, so any G1 run with pivot moves needs its own C4 row. This matters because the program summary describes the pilot as "HMC + pivot moves".

### S5. Relative-to-best: classical bypasses and what survives (item iii)

**DERIVED** (logic) + **INFERENCE** (quantisability):
1. **A first-order transition belongs to the path, not the target.** π_1 is fixed. The bottleneck of S3 exists only for the family π_λ ∝ π_0 e^{−λV} with local kernels. Classical methods that change the path, the moves or the compression variable can avoid it:
   - **temperature paths;**
   - **optimised spline paths** ("this path performs poorly in the setting where the reference and target are nearly mutually singular", [T2-2]);
   - **variational references** tuned to the posterior [T2-3];
   - **interpolation to independence**, which gives polynomial-cost SMC on a Potts target where PT is exponential **THEORETICAL [T2-12]**;
   - **entropy-dampening tempering**, polynomial where temperature tempering is torpid **THEORETICAL [E40]**;
   - **multicanonical / Wang–Landau** flattening along V. For 2D 10-state Potts, tunnelling time grows ~L^{2.65} instead of exponentially **THEORETICAL [T2-8]**. Barriers orthogonal to the flattened coordinate remain exponential **THEORETICAL [T2-10]**;
   - **nested sampling** [B67] and its constrained-HMC and replica-exchange variants.
     - It uses exactly this setting: an exactly sampleable prior π_0 and a likelihood threshold on E_pair. It compresses in prior mass rather than in λ, so it is not hampered by first-order transitions *along λ*.
     - On the q-state Potts model with a first-order transition (q > 4), "one run stops after O(N) moves", and results were "compared with those obtained with multi-canonical sampling" [T2-14]. On Lennard-Jones clusters the "efficiency gain over parallel tempering in calculating the heat capacity is more than an order of magnitude" [T2-15]. **THEORETICAL/EMPIRICAL (classical)**; abstracts verified in this revision.
     - Its constrained-sampling step can still be glassy. It removes the λ-path bottleneck, not trapping inside the constrained region;
   - **SMC with only local-mixing requirements**, which is an FPRAS on some multimodal targets where MCMC is exponentially slow **THEORETICAL [T2-13]**;
   - **mode finding (multistart L-BFGS) + within-basin sampling + basin free-energy reweighting.**
2. **Quantum algorithms quantise classical algorithms.** Every known *provable* quantum speedup in S1–S2 is at most a square root of the cost of a *quantisable* classical procedure:
   - a reversible chain: QSA [A7, A31], quantum RELD [A44]. The square root is in the gap, same chain.
   - a classical randomised procedure run reversibly over a seed register, with a Bennett-type reversibility overhead O_rev. This covers Montanaro mean estimation [A30] (quadratic in the number of runs, i.e. in 1/ε), amplitude amplification [B1] of a checkable outcome (multistart hitting a basin; an SMC lineage entering F), and quantum rejection sampling [A36].
   - **SMC / population annealing with resampling is such a procedure.**
     - Resampling copies classical particle registers, i.e. computational-basis values. A coherent circuit does that with CNOT fan-out, so no-cloning does not apply. No-cloning forbids copying an unknown quantum state such as the qsample |π⟩, not resampling.
     - The [A31 §5] passage concerns reusing intermediate *quantum* states across temperatures. v1 misapplied it to resampling.
     - SMC is therefore quantisable in the Montanaro / amplitude-amplification sense: A_q ≈ O_rev for a rare-event SMC bypass (below).
     - **What is not known** (INFERENCE; UNPROVEN that no such algorithm exists): (i) a quantum speedup of SMC's internal sequential mixing beyond QSA-type δ^{-1/2} on the same moves; (ii) a coherent SMC that outputs a *garbage-free* qsample. The coherent population stays entangled with its resampling history, so the output is not |π_1⟩.
   - QSA on a *bypass* path is available in principle. It costs √(bypass mixing cost) and competes against a polynomial classical cost.
   - **Beyond-quadratic claims** exist only as heuristic small-n fits for diagonal Ising costs:
     - quantum-enhanced MCMC [A47], with the gap fitted as 2^{−kn} at 3 ≤ n ≤ 10, "roughly cubic/quartic" against local/uniform proposals (`lit_A_sampling.md` §3.7), and its variants [A52, A54];
     - these are disputed: no speedup in the worst unstructured case [A48];
     - they are killed for this program because they need a diagonal register encoding (`OPPORTUNITY_MATRIX.md` M7).
     - "At most a square root" therefore refers to provable guarantees.
3. **Consequence.**
   - Let B_q be the best classical cost among quantisable algorithms, B_best the best classical cost overall, and A_q := B_q/B_best ≥ 1. The best known quantum cost is ~K·n_b·√B_q walk-step equivalents.
   - A speedup over the best classical method therefore requires √(A_q B_best)·(K n_b R ρ) < B_best, i.e. **B_best > A_q (ρ K n_b R)²** (S6).
   - For a rare-event SMC bypass, A_q ≈ O_rev (≥ 1, small constant). Its quantum version amplitude-amplifies the rare event, turning 1/q_F into 1/√q_F. That is the same halving as QSA, now on a bypass-capable procedure.
   - At a first-order λ-bottleneck with a polynomial classical bypass, the λ-path QSA costs ~δ_*^{-1/2} (e^{aΔF‡/2} under A-Arr) against poly(L) classically. It is **exponentially slower**.
   - The lifting check T2c:
     - Non-reversible PT already realises the classical "lifting" gain on the index process: round-trip rate 1/(2+2Λ) vs 1/(2N+2Λ) for reversible PT [T2-1 Cor. 1, Thm 3]. Transport is ballistic instead of diffusive, as in [A14, A15, A18].
     - A walk quantising reversible PT's index dynamics therefore gains nothing over NRPT on that component.
     - The only quantum lever left is the fixed-λ gap (**DERIVED** from [T2-1] Cor. 1).

### S6. Break-even inequality (item iv)

**DERIVED** (§3.6).
- A classical "local step" is one energy+gradient evaluation, costing c(L) seconds on one core (A-c). A quantum walk step costs G(L) Toffolis at t_T seconds each (G from T3, A-G).
- ρ is the **cost** of one quantum-computer-second in core-seconds: a cost ratio, not a time ratio (A-ρ). R(L) := G(L)·t_T/c(L).
- A := τ_*/B_best ≥ 1. **A = 1 means both "no classical bypass" and κ_chain = 1** (the quantised grid-Metropolis chain relaxes as fast as classical HMC). Both are quantum-favourable.

For M posterior samples:

```
(QSA, λ-path)            M·ρ·K·n_b·R·√τ_*   <   B_burn + M·B_best                                        (I-1)
(per sample)             τ_*  >  B* := ( A·ρ·K·n_b·R )²,     A := τ_*/B_best ≥ 1                           (I-2)
(log form)               ln τ_*  >  2·ln( A·ρ·K·n_b·R );   under A-Arr:  ΔF‡ > [2 ln(AρK n_b R) − ln C]/a   (I-3)
(posterior mean ±ε)      (σ/ε)·ρ·K·n_b·R·√τ_*  <  (σ/ε)²·B_best   ⇔   τ_* > B*/(σ/ε)²                    (I-4)
(ampl.-ampl. multistart) p_hit  <  p* := [ (π/2)·ρ·O_rev·R_grad ]^{-2},   R_grad := G_grad·t_T/c             (I-5)
```

- τ_*(L) is the relaxation time, in local steps, of the chain that the quantum algorithm quantises, at the bottleneck λ. It includes κ_chain = τ_Metropolis/τ_HMC ≥ 1 (A-chain).
- B_best(L) is the per-independent-sample cost of the best validated classical method, in local steps.
- n_b ∈ [1, ℓ] (S1a, §3.2):
  - n_b ≈ 1–2 under A-FO (C3: 1.01–1.22);
  - n_b ≈ the number of stages at λ ≥ 0.3 in the glassy case: 2.9–6.7 (Λ-based) or 2.6–37 (SD-based) for L = 45–150;
  - n_b = ℓ as the uniform upper bound.
- K ≈ (1/p)log(1/p)·log²(ℓ/ε) ≈ 700 at the stated p, ℓ, ε. The tables use K ∈ {10, 100, 10³}, where K ∈ {10, 100} **assumes improved constants** (A-K, gap 6).
- **(I-1) and burn-in.**
  - For a *stationary* NRPT with exact prior refresh, the first sample arrives after about half a round trip, so B_burn ≈ B_per/2 and amortisation changes (I-1) by at most ~1.5×.
  - **This does not describe the pilot.** The pilot's λ ≥ 0.3 rungs are still drifting by up to 732 nats (L=150) after tuning, so at the observed budgets burn-in (non-stationary relaxation) dominates classical cost. It cannot yet be separated from stationary relaxation.
  - Long transients are weak evidence for a small *stationary* gap (the quantity QSA square-roots). For a reversible chain, ‖P^t(x_0,·) − π‖_TV ≤ ½π(x_0)^{−1/2}e^{−t/τ_rel}. So a transient of length t_burn implies only τ_rel ≥ t_burn/[½ln(1/π(x_0)) + ln(1/(2ε))].
  - Here ln(1/π_λ(x_0)) can be 10³–10⁴ nats for a prior-drawn start (E₀V − E₁V ≈ 3×10³–5×10⁴). D4 therefore measures τ_* from stationary starts.
  - Where burn-in genuinely dominates a method's cost, amortisation favours quantum [QUANTUM_PRIMITIVES §1.2] (**DERIVED**).
- **(I-4).**
  - The per-sample threshold falls by (σ/ε)², i.e. 10–100× for σ/ε ≈ 3–10 (the S33-style soft readout; INFERENCE).
  - But the wall-clock of the whole estimation task at break-even is **exactly invariant**. Classical: (σ/ε)²·c·B_best with B_best = τ*/A and τ* = B*/(σ/ε)², i.e. c·(AρK n_b R)²/A = A·ρ²·(K n_b G t_T)²/c. Quantum: (σ/ε)·K n_b G t_T·√τ* = A·ρ·(K n_b G t_T)²/c.
  - So the minimum-runtime corollary holds for any precision (**DERIVED**).
- **(I-5).** An amplitude-amplification iteration applies the decoder A and A† once each, so ~(π/2)·p_hit^{-1/2} decoder runs are needed (v1 had π/4).
  - The target basin is unknown, so the marking oracle must itself find the minimum. Dürr–Høyer minimum finding [C56] costs O(√N), with a constant ≈ 22.5 in the body of [C56] (quoted as a sensitivity, not re-verified; the verified abstract states O(c√N) for success 1 − 2^{−c}). This lowers p\* by a further ≈ 200×.
  - Both corrections favour classical, so the conclusion is conservative.

**Numbers (§4.3, C6).** Assumptions: A-G (T3's G(L): T3-D2 generous/central for the A80 target, T3-D3 generous for the Cartesian target), A-t (t_T ∈ {170 µs [A56], 10 µs, 1 µs}), A-K (K ∈ {10, 100, 10³}), n_b as above, A-c (overhead-corrected c(L)), ρ = 1, A = 1. Then:
- **B\* = (K n_b R)²** ranges over:
  - **1.0×10¹⁰ – 2.7×10¹⁰** in the single most optimistic scenario (T3-D3 target, 1 µs, K = 10, n_b = 1; L = 150 … 45);
  - **1.1×10¹¹ – 4.0×10¹¹** in the most optimistic scenario for the A80 target;
  - ~10¹⁷ at A-FO central values (T3-D2 central, 10 µs, K = 100, n_b = 2);
  - ~10²² with the cited constants (K = 10³, 170 µs);
  - up to 9×10²⁴ at pessimistic values (n_b = ℓ_SD, L=150).
- **ln B\* = 23–58.** Under A-Arr with the toy's (a, ln C), the equivalent barrier is ΔF‡\* = (ln B\* − ln C)/a ≈ 16–48 nats. This is a sensitivity only: C3's C is in single-flip units, not HMC local steps.
- **T\*_Q = 0.26 yr (T3-D3 target, L=45) and 1.05–20 yr (A80 target, most optimistic)** up to ~5×10¹⁴ yr (pessimistic).
- For (I-5), **p\* = 6.7×10⁻¹⁹ – 1.0×10⁻¹¹ (L=45) and 1.7×10⁻¹⁹ – 2.8×10⁻¹² (L=100)**.

**Corollary (minimum useful runtime; DERIVED).** Separate cost from wall-clock.
- At break-even, the classical wall-clock per sample is T\*_C = c·B\* = A·ρ²·(K n_b G t_T)²/c. The quantum wall-clock is **T\*_Q = A·ρ·(K n_b G t_T)²/c ≥ (K n_b G t_T)²/c** for ρ ≥ 1 and A ≥ 1. The two are equal only at ρ = 1.
- For τ_* > B\* the quantum wall-clock K n_b G t_T √τ_* exceeds T\*_Q. For τ_* < B\* classical wins.
- **An advantage is therefore never available at a per-sample quantum wall-clock below T\*_Q, whatever the classical cost.**
- Bringing T\*_Q within a budget T_budget requires **t_T ≤ √(T_budget·c/(Aρ))/(K n_b G)**, so ρ enters as ρ^{−1/2}:
  - for T_budget = 1 day: 51 / 17 / 12 ns (L = 45 / 100 / 150; A80 target, most optimistic), 103 / 72 / 68 ns (T3-D3 target), 0.55 / 0.18 / 0.12 ns (A-FO central);
  - for T_budget = 1 year: 980 / 320 / 230 ns (A80, most optimistic), 2.0 / 1.4 / 1.3 µs (T3-D3), 11 / 3.4 / 2.3 ns (A-FO central) (C6).
- This is the per-step form of the quadratic-speedup obstruction in [A55, A56, A57].

*Claim level: any statement derived from (I-1)–(I-5) is same-chain L3 (G(L) from T3). A relative-to-best statement needs a measured B_best(L) and would then be L4. Current relative-to-best level: L0. Current practical level: L0.*

### S7. Which classical measurements decide relevance (item v)

In priority order. Each item has a decision rule. **INFERENCE** (design), grounded in S3–S6.

| # | Measurement | Protocol (classical, G1-style) | Decides |
|---|---|---|---|
| D1 | **Kind of bottleneck: first-order or glassy** | Fixed-λ runs on a fine λ grid near 0.3–0.6, with ≥4 seeds each started from exact prior draws **and** from decoded low-E modes. Record the E_pair histogram (bimodality), Var_λ(E_pair) (peak), hysteresis between up- and down-anneals, and the crossing point λ_c from BAR/MBAR between branches. Once both branches are populated, a coarse fixed grid (Δλ ≫ 1/ΔV) shows a populated jump as r_k → 1 at the straddling pair (§3.3) | First-order → S3 applies (halving in δ, bypass search). Glassy or persistence → the relevant model is the multi-basin/needle model (S3e), and p_hit and basin masses decide |
| D2 | **ΔF‡(L)** at the bottleneck, with a **pre-registered extrapolation** | Umbrella or multicanonical sampling along E_pair and a fold-order parameter (e.g., contact overlap with the dominant basin), or tunnelling-time scaling at λ_c, for L = 30, 45, 60, 80, 100, 120, 150. Pre-registered model: ΔF‡(L) = a₀ + a₁L^γ with γ ∈ {2/3 (interface), 1 (bulk)}, chosen by AIC, with a crop-bootstrap interval. τ_*(L) = C·e^{a·ΔF‡(L)}, with (C, a) fitted only where τ_* is directly measurable (≤ 10⁸ local steps: small L, or λ near the spinodal). τ_* beyond ~10⁹ is reported only as this extrapolation with its interval | (I-3): relevance requires ln τ_* ≳ ln B\* (23–58 nats; ΔF‡ ≳ 16–48 under A-Arr) **and** A ≈ 1 |
| D3 | **ELE gap** | Transit-aware predicted vs observed round trips: simulate the index process from the actual start (C4), or discard a burn-in of ≥ one E[T] = 2N(1+E) scans before counting. Scan n_expl ∈ {1, d/2, d, 4d} and N as in [T2-1 §7.2], with and without pivot moves. Per-rung τ_int of V | If the deficit vanishes as n_expl or N grows, the "bottleneck" is under-exploration (A2) or non-stationarity (A1). It is then cheap classically, and no quantum relevance follows |
| D4 | **τ_*(L)**, the fixed-λ relaxation time of a *quantisable* chain (Metropolis/MALA on the grid) and of HMC | Multi-start τ_int of V and of basin labels at λ ≈ λ_c, **from stationary starts** (decoded low-E modes; long-equilibrated states), not only from prior draws (S6 burn-in bullet). Report the lower bound from non-observation when transitions are absent. Note: this gives only lower bounds on τ_* (upper bounds on δ), never the certified lower bound on δ that QSA needs (A-δ) | Enters (I-1)/(I-2). Also gives κ_chain |
| D5 | **B_best(L)** over the bypass portfolio | Equal-effort runs of (a) PT on a temperature path, (b) variational-reference / mode-informed-reference PT [T2-3], (c) population annealing / SMC with R scanned [T2-11, T2-12], (d) multicanonical in E_pair [T2-8], (e) multistart + local HMC + basin free energies by TI/BAR (**not** Laplace), (f) learned independence proposals [A78, A79], (g) **nested sampling** with constrained HMC / replica exchange [B67, T2-14, T2-15] | **Decisive.** Cross-validated basin populations must agree across methods (E39 warns that single-method diagnostics fail). A := τ_*/B_best. For (c) and (g), record the rare-event factor, since its quantum version is the amplitude-amplified one (S5.2) |
| D6 | **p_hit(L) and the basin-mass vs hit-rate relation** | Mode census (R ≥ 256; raise R where p_hit sits at the 1/R floor, i.e. 1–4 targets per L now). Basin posterior masses by TI/BAR from a basin-centred Gaussian reference | (I-5). The classically hard regime is a high-mass basin with a tiny hit rate (a needle, S3e). Funnelled landscapes have high-mass ⇒ high-hit |
| D7 | **c(L)** and parallel efficiency | Energy+gradient micro-benchmark, single-structure and batched, on an **idle** node (a loaded-machine attempt in this revision was unusable, §2.4 A-c), plus GPU throughput | Sets R(L) (B\* ∝ c⁻²) and the ρ-equivalent parallel slack |
| D8 | **Temperature sensitivity** | Repeat D1–D5 at the calibrated T (the T-scan in `g1_tscan` is in progress) | The bottleneck belongs to (E, T). If it disappears at the calibrated T, the question is moot |

**Kill rule (INFERENCE, proposed for pre-registration).** KILL the λ-path quantum sampling route (candidates M1/M2 of `literature/OPPORTUNITY_MATRIX.md`) for L ≤ 150 if either condition holds. Both thresholds are numeric.
- **(a)** D3 shows the round-trip deficit disappears at every measured L ∈ {45, …, 150}, at a classical cost per round trip ≤ **10⁹ local steps**. "Disappears" means the observed rate is ≥ ½ of the transit-aware ELE prediction, after raising n_expl and/or N.
- **(b)** D5 finds a classical method with cross-validated B_best(L) ≤ **10⁹ local steps per validated sample** at L = 150, and at every smaller L measured.

Margins. B\*_min(L) over t_T ≥ 1 µs, K ≥ 10, n_b ≥ 1, ρ = 1, A = 1 (C6):
- 1.0–2.7×10¹⁰ for the T3-D3 target, so 10⁹ is ≥ 1 order below;
- 1.1–4.0×10¹¹ for the A80 target, so 10⁹ is ≥ 2 orders below.

v1's threshold of 10¹⁰ would have sat *at* the most optimistic T3-D3 break-even, so it is lowered.

Otherwise, pass to T3 with the measured τ_*(L), A(L) and ΔF‡(L) (with the D2 extrapolation interval).

---

## 2. Model and assumptions

### 2.1 Target and path

- Energy: the A80 learned energy (`src/qapf/protein/energy.py`, vendored from S33; provenance in `src/qapf/protein/PROVENANCE.md`).
  - E = w_ca Σ_{|i−j|≥3} −log p̃^CA_ij(d_ij) + w_cb Σ −log p̃^CB_ij + w_tt Σ_i −log P̃_i(θ_i, τ_i) + w_s Σ relu(r0−d_ij)² + w_w·wall(θ).
  - The pair tables p̃_ij are **pair-specific**: 28 distance bins convolved with a Gaussian, tabulated on a 0.05 Å grid to 50 Å.
- Split (`src/qapf/sampling/hrex.py`): E_prior = w_tt·(θ,τ)-head + w_w·wall, which is a product over residues. E_pair = CA + CB pair NLL + sterics, which has O(L²) terms.
  - E_prior ≥ −10⁻⁶ per residue: the soft-binned head probability is ≤ 1 and the wall is ≥ 0. S2 uses this.
- π_λ ∝ exp(−(E_prior + λE_pair)/T), λ ∈ [0,1], T = 1 in the pilot.
- π_0 is sampled **exactly up to grid discretisation**. `ExactPrior` takes, per residue, the joint (θ_i, τ_i) soft-binned head times the θ wall, on a 0.5° × 1° grid (360 × 360 cells), with uniform jitter inside a cell.

### 2.2 Classical instrument (PILOT)

- Non-reversible PT with DEO swaps and the adaptive schedule of Syed et al. [T2-1]. The schedule is tuned first, then production starts from identity labels.
- **Local moves in the analysed pilot files: HMC only.** Each scan runs one trajectory of n_leap = 8 leapfrog steps per rung (per-rung step size and diagonal mass), plus an exact prior refresh on the λ=0 rung.
  - The files carry no `pivot` field. The current driver `scripts/g1_sample_crop.py` writes one, with default `--pivot 4`.
  - The production cost per scan is 262 = 29·9 + 1 energy evaluations at L=45 (30 rungs). That is HMC only; with 4 pivot moves it would be 29·14 + 1 = 407.
  - So n_expl = 1 per rung per scan.
- Recorded: Λ, per-rung rejection r_k, round trips, gradient evaluations, and the E_pair trace per rung (`research/results/RAW/g1_pilot/*.json|npz`).
- Mode census: 256 restarts of 200-iteration L-BFGS, clustered at 2 Å (`research/results/RAW/g1_modes/*.json`).

### 2.3 Quantum model and oracle discipline

**(O1)** No free oracles. The walk operator W(P_λ) for a reversible, finite-state P_λ is built from:
- a coherent circuit for E(x) or ΔE. A torsion move changes all j(L−j) pair distances that straddle the pivot, i.e. Θ(L²) terms, both classically and coherently. With the proposal index in superposition, a step evaluates all O(L²) pair terms (T3 §3.1);
- coherent forward kinematics (internal → Cartesian: L sequential rotations with sin/cos);
- QROM/QROAM lookups of the pair-specific data (T3: spline coefficients);
- the Metropolis coin arcsin√min(1, e^{−ΔU}) [A55, A56];
- uncomputation.

Continuous samplers need a coherent **gradient** oracle [A44, A45].

**(O2)** No free state preparation. |π_0⟩ is built by per-residue QROM amplitude loading at the prior's native table resolution (S1d). It is not assumed.

**(O3)** Costs are counted in walk steps or oracle queries (theory) and in Toffolis (practice). **Query counts are never converted to runtime without G(L) and t_T.** No simulator is involved. All quantum numbers are paper estimates under A-G and A-t.

### 2.4 Labelled assumptions

| Label | Assumption | Where used | Status |
|---|---|---|---|
| A-grid | The quantum walk acts on a grid Ω of b bits per angle, so Ω has 2^{b(2L−5)} points. T3 uses b = 10; the prior table has ≈ 8.5 bits per angle (360 cells). Discretisation error is below the target TV error | S1, S2 | Standard; b not optimised |
| A-rev | The quantised chain is reversible. δ_λ is its **absolute** spectral gap, 1 − max(μ_2, \|μ_min\|), or the chain is made lazy (P → (I+P)/2, which at most halves δ). Only then is Szegedy's walk phase gap Θ(√δ) [A1, A28]. Eigenvalues of P near −1 give walk phases near 0 | S1, S3f | Required; Metropolis on Ω is not automatically lazy |
| **A-δ** | A **certified lower bound** on δ_λ at the bottleneck is available to set QSA's phase-estimation precision ([A7]; [A31] Thm 5, Thm 10) | S1, S3d, S6 | **UNPROVEN.** No classical or quantum procedure in the verified literature supplies one in the hard regime. Classical runs give only upper bounds on δ. If it fails, both sides fail silently (biased toward the metastable branch) |
| A-chain | The quantisable chain (grid Metropolis / MALA) relaxes κ_chain ≥ 1 times slower than classical HMC. Heuristically κ ~ d^{3/4} from RWM O(d) [E50] vs HMC O(d^{1/4}) [A75], both for i.i.d. targets. **Lever-arm caveat:** in compact states a single-torsion move displaces Θ(L) atoms by up to Θ(L·Δθ), so torsion-move Metropolis acceptance falls with the lever arm, and κ_chain may be much larger than d^{3/4} | S6 A(L) | INFERENCE; to be measured (D4) |
| A-FO | Two-phase crossing model of S3 (logistic w_F, interface barrier ΔF‡) | S3, I-3 | **Hypothesis about the pilot bottleneck**; D1 tests it |
| **A-Arr** | Arrhenius-type gap scaling at the bottleneck: δ_* = C^{-1}·e^{−a·ΔF‡}. Needed to convert halving in δ into halving in ΔF‡ | S3, I-3, §4.3 ΔF‡\* column | **INFERENCE.** C3 gives a ≈ 1.10, ln C ≈ 5.4 (toy, single-flip units). Cheeger alone gives only e^{−2ΔF‡} ≲ δ ≲ e^{−ΔF‡} |
| A-mono | For λ between the forced rung λ_s and λ_c, the conditional mean of V in the interface lies between the phase means: E_{λ,F}[V] ≤ E_{λ,I}[V] ≤ E_{λ,U}[V] | Prop. 3 item 2 | Natural for an interface; not checked on the protein |
| A-G | **Superseded by T3.** G(L) = T3's qubitised walk step (RESOURCE_MODELS.md §0, §4.2): T3-D2 (torsion moves, spline pair terms; ≈ 2.3×10⁴·L² central, ≈ 4.7–5.0×10³·L² generous); T3-D3 (Cartesian single-residue moves, G ≈ 5×10⁶–3.4×10⁷ over L = 45–150, roughly ∝ L; it samples a **different, bond-relaxed target** with unknown per-step mixing κ_D3). v1's itemised count (1.5L² pairs × (10³ + 10³–5×10³ + 10³) × (2–4)) actually gave g ≈ 9×10³–4.2×10⁴, not the stated 5×10³–3×10⁴; that inconsistency is now moot. **[A56] calibration** (per T3's reading of the PDF): 6.7×10²–4.8×10³ Toffolis per qubitised step for SK N = 64–1024 (Table VIII) and 2.0×10⁴–4.6×10⁶ for LABS N = 64–1024 (Table IX). v1 quoted the LABS range as if it covered both | S6, §4.3 | DERIVED in T3 under T3's A1–A15 |
| A-Ggrad | A gradient-oracle query costs G_grad = 3G | S2, (I-5) | Order-of-magnitude placeholder |
| A-t | Seconds per Toffoli t_T ∈ {170 µs (single factory, Sanders et al. [A56]), 10 µs, 1 µs (hypothetical future or ~170 factories)} | §4.3 | Scenario, not a prediction |
| A-K | QSA overhead per stage K = (1/p)ln(1/p)·ln²(ℓ/ε). At p = e^{−2}, ℓ = 10, ε = 10⁻² this is ≈ 14.8 × 47.7 ≈ 700. **K ∈ {10, 100} assumes improved constants** (gap 6). The tables include K = 10³ | S6, §4.3 | Constants of [A7, A31] not tracked |
| A-ρ | ρ = the cost of one QC-second in core-seconds (a cost ratio). ρ = 1 in the tables | S6 | Strongly favours quantum. Realistic ρ ≫ 1 raises B\* by ρ² and T\*_Q by ρ. ρ = 1 prices a 10⁷–10⁸-physical-qubit machine as one core |
| **A-c** | c(L) = pilot wall-clock per local step divided by 1.95, the sampler-overhead factor measured at L=150 (3.51 ms pilot vs 1.8 ms micro-benchmark). This gives 0.30 / 0.40 / 0.75 / 1.23 / 1.80 ms at L = 45 / 60 / 100 / 120 / 150. T3's placeholder 0.2 ms·(L/45)² is within 0.66–1.3× of these values | S6, §4.3 | Approximation. The overhead fraction may be larger at small L (smaller true c raises B\* ∝ c⁻²). A micro-benchmark attempted in this revision on a machine running three G1 jobs was unusable (single-structure calls 9–14 ms at every L, dominated by PyTorch per-call overhead; batched 0.9–6.8 ms/structure under load). D7 must run on an idle node. Using the uncorrected wall-clock instead lowers B\* by 3.8× (quantum-favourable) |
| A-dom | [A44, A45] assume smooth potentials on a torus or a confining domain. Here θ is walled and τ periodic | S2 | Approximate applicability |

---

## 3. Proofs and derivations

### 3.1 Lemma 1: overlap, stage count, and the Λ ↔ 𝓛 relation (DERIVED)

π_λ(x) = q(x)e^{−λV(x)}/Z_λ, with q := π_0 and Z_λ := Σ_x q(x)e^{−λV(x)} (so Z_0 = 1), is an exponential family in λ with log-partition function A(λ) := log Z_λ. Then:

1. **Exact identity.** BC(λ,λ′) = Σ_x √(q e^{−λV}q e^{−λ′V})/√(Z_λ Z_λ′) = Z_{(λ+λ′)/2}/√(Z_λ Z_λ′). Therefore −ln BC = ½A(λ) + ½A(λ′) − A((λ+λ′)/2) ≥ 0, by convexity of A. Check C2 confirms it to 3×10⁻¹⁶.
   - **χ² companion.** 1+χ²(π_λ‖π_λ′) = Σ π_λ²/π_λ′ = Z_{2λ−λ′}Z_λ′/Z_λ² = exp(A(2λ−λ′) + A(λ′) − 2A(λ)) (C2: 2×10⁻¹⁶).
   - To second order, ln(1+χ²) ≈ (Δλ)²A″ = 8·(−ln BC), so 1+χ² ≈ BC^{-8}.
   - Across a jump it is far larger. At λ = 0 it involves A(−λ′), a tilt toward high V (steric clashes), which can be very large.
2. **Second order.** A″ = Var_λ(V). A Taylor expansion about λ̄ = (λ+λ′)/2 gives −ln BC = (Δλ)²·Var_{λ̄}/8 + O(Δλ⁴ A⁗). Check C2 agrees for small Δλ (0.01227 vs 0.01226). The expansion fails across a jump, which is why §3.3 treats the jump exactly.
3. **Stage count.** Require −ln BC ≤ κ, i.e. BC² ≥ p = e^{−2κ}. The admissible local step is Δλ ≤ √(8κ/Var_λ). A greedy schedule then has ℓ = ∫ dλ/Δλ(λ) + O(1) = 𝓛/√(8κ) + O(1), with 𝓛 = ∫_0^1 √Var_λ dλ. Harrow–Wei use κ = 1, so ℓ ≈ 𝓛/√8.
4. **Cauchy–Schwarz.** 𝓛 = ∫_0^1 √Var_λ dλ ≤ (∫_0^1 Var_λ dλ)^{1/2}. Since A′(λ) = −E_λ[V] and A″ = Var_λ, ∫_0^1 Var_λ dλ = A′(1) − A′(0) = E_0[V] − E_1[V].
   - So 𝓛 ≤ √(E_0V − E_1V) and ℓ ≲ √(E_0V − E_1V)/√8.
   - This matches the √(E_{π_0}[H]) schedule of [A31] Thm 4 up to the shift and log factors.
   - The pilot values of this bound use a λ=1 mean that is still drifting down, so they are biased low (§1 S1b).
5. **Relation to Λ.** For Gaussian V under π_λ with standard deviation s: ½E|V_1−V_2| = ½·(2s/√π) = s/√π (C2: 2.0884 vs 2.0875). Hence Λ = 𝓛/√π and ℓ ≈ √π Λ/√8 = 0.627 Λ.
   - For non-Gaussian V this is an approximation. The direct estimator is ℓ = 𝓛/√8 with 𝓛 from the per-rung SD of V.
   - The pilot reports both as a range (S1b: 8.5–8.7 at L=45, 18.3–62.2 at L=150). Both are contaminated by non-stationarity.
   - The stage count enters the cost only through n_b ≤ ℓ, and **B\* ∝ n_b²** (§3.2, S6). ∎

### 3.2 QSA cost, stage-resolved form, and n_b (THEORETICAL + DERIVED)

- **Theorem ([A7], restated in [A31] Thm 5).** Suppose chains M_0..M_ℓ have slow-varying stationary states (|⟨π_i|π_{i+1}⟩|² ≥ p), gaps ≥ δ, and |π_0⟩ is preparable. Then a state ε-close to |π_ℓ⟩ is produced with O(ℓ δ^{-1/2} log²(ℓ/ε)(1/p)log(1/p)) walk steps. δ is an *input* (A-δ). The text was read from the arXiv PDF of 1907.09965 in the v1 session.
- **Stage-resolved form.**
  - In [A7]'s construction, stage i rotates |π_i⟩ toward |π_{i+1}⟩ using O((1/p)log(1/p)) reflections, about equally many about each of the two states.
  - The MNRS approximate reflection about |π_j⟩ [A2] runs phase estimation on W(P_j) to phase precision Θ(√δ_j), repeated O(log(1/ε′)) times. It costs O(δ_j^{-1/2}·log(1/ε′)) walk steps, with ε′ ≈ ε/(ℓ·(1/p)log(1/p)) so that errors add to ε. That accounts for **one** logarithm, log(ℓ/(pε)).
  - The second logarithm in log²(ℓ/ε) is taken from [A7]'s statement as restated in [A31] Thm 5. Its origin is not re-derived here. All constants and logarithms are absorbed into the scenario parameter K, so this affects no conclusion.
  - Summing gives `N_walk = O( K · Σ_{i=0}^{ℓ−1} ½(δ_i^{-1/2} + δ_{i+1}^{-1/2}) ) = O( K · n_b · δ_*^{-1/2} )`, with n_b := ½Σ_i[(δ_*/δ_i)^{1/2} + (δ_*/δ_{i+1})^{1/2}] and δ_* := min_i δ_i.
  - The ½ makes uniform gaps give n_b = ℓ, recovering the uniform bound.
  - A single bottleneck rung s with all other δ_i ≫ δ_* gives n_b = 1. It enters stage s−1 and stage s, each with about half of the reflections.
  - So n_b ∈ [1, ℓ]. **DERIVED (constants not tracked).**
- **n_b under A-FO.** The forced rung (Prop. 3 item 2) carries δ_*. Its neighbours sit at the smooth-overlap spacing Δλ ≈ √8/s, where s is the within-phase SD, extensive as ~√n. Across that spacing the minority-phase barrier falls by ≈ (E_I − E_F)·Δλ ~ ΔV/s ~ √n ≫ 1.
  - So (δ_*/δ_{neighbour})^{1/2} is exponentially small, and n_b → 1. C3's greedy schedule gives n_b = 1.22, 1.07, 1.02, 1.01 at n = 25–100.
  - At finite size, or with a non-greedy schedule that places extra rungs near λ_c, n_b ≈ 2. The tables therefore use n_b ∈ {1, 2} for A-FO.
  - In the glassy case many rungs are slow, and n_b ≈ the number of such rungs (proxy: stages at λ ≥ 0.3). v1's K·ℓ·δ_*^{-1/2} overstated N_walk by ℓ/n_b and B\* by (ℓ/n_b)².
- **Adaptive schedule.** [A31] Thm 10 builds the schedule adaptively by binary search on λ with nondestructive amplitude estimation of the overlap. The total cost is Õ(√E_{π_0}[H]/√δ), and they note that their schedule "roughly matches the length of the best classical adaptive annealing schedules". **The schedule length is not a quantum advantage.** Only the δ-dependence is.
- **M samples.** Each run ends in |π_1⟩, and measuring it yields one sample. No-cloning prevents reusing intermediate quantum states; [A31 §5] states this explicitly for schedules. Cost: M·N_walk. **DERIVED.**
- **Estimation.** Montanaro's mean estimator [A30] uses the preparation unitary and its inverse O(σ/ε·polylog) times, which gives (I-4). **THEORETICAL.**

### 3.3 Lemma 2: a first-order crossing adds 1 + O(s/ΔV) to Λ and at most π + O(s/ΔV) to 𝓛 (DERIVED)

Under A-FO, near λ_c the law of V is a two-component mixture with weight w = σ(x), x = (λ−λ_c)ΔV, component means separated by ΔV, and within-phase SDs s_U, s_F ≤ s ≪ ΔV.

- **Jump part.** First neglect the within-phase fluctuations.
  - Var_λ(V) = w(1−w)ΔV², and ½E|V_1−V_2| = ½·2w(1−w)ΔV.
  - With dλ = dx/ΔV:
    - Λ_jump = ∫ w(1−w)ΔV dλ = ∫_{−∞}^{∞} σ(x)(1−σ(x)) dx = [σ]_{−∞}^{∞} = **1**;
    - 𝓛_jump = ∫ √(w(1−w))ΔV dλ = ∫ dx/(2cosh(x/2)) = **π**.
  - Both are independent of ΔV. C1 gives 1.000000 and 3.141593. The values 0.987 and 2.81 at ΔV = 5 come from truncating λ to [−1, 1].
- **With fluctuations.**
  - Var_λ = w(1−w)ΔV² + w s_F² + (1−w)s_U². √ is subadditive, so √Var_λ ≤ √(w(1−w))ΔV + √(w s_F² + (1−w)s_U²). The jump therefore adds **at most π** to 𝓛, plus O(s/ΔV) from the smooth part varying across a window of width ~1/ΔV.
  - For Λ, cross-phase pairs contribute w(1−w)E|ΔV + ξ| with ξ of SD O(s), which is w(1−w)ΔV up to corrections that vanish as s/ΔV → 0. Same-phase pairs contribute the smooth part. So Λ_jump = **1 + O(s/ΔV)**.

**Consequences.**
- **(i) Exact stage count across the jump.** In the two-point limit (π(I) → 0, within-phase overlap 1), BC(w, w′) = √(ww′) + √((1−w)(1−w′)).
  - From w_F = 0 the next rung can reach at most w′ ≤ 1−p (BC² = 1−w′ ≥ p). From w_F = 1−p, BC² to w_F = 1 is 1−p ≥ p for p ≤ ½.
  - So **exactly one intermediate rung**, with w_F ∈ [p, 1−p], is needed, and the jump costs **at most 2 stages** at p = e^{−2} (C1). A direct 0 → 1 step has BC = 0.
  - C3 confirms this: 2 stages, with the forced rung at w_F ≈ 0.86 ≈ 1−p.
  - v1 converted 𝓛_jump to stages with the second-order formula of Lemma 1(3), which fails across a jump.
- **(ii)** Under ELE, NRPT would cross the jump with ≈ 2 extra scans per round trip ([T2-1] Cor. 1; 2·Λ_jump).
- **(iii)** Therefore the cost of a first-order crossing is in the fixed-λ dynamics, i.e. in the gaps.
- **(iv) What swap statistics can and cannot see.**
  - The *continuum* Λ, and a schedule adapted to it, is insensitive to the jump (adds 1).
  - On a fixed grid with spacing Δλ ≫ 1/ΔV across a *populated* jump, the straddling pair has log r = Δλ(V_{k+1} − V_k) ≈ −ΔλΔV (the acceptance rule in `hrex.py`). Its acceptance is ≈ e^{−ΔλΔV}, so r_k → 1 there and **the jump is visible**.
  - On a grid finer than 1/ΔV it shows only as an O(1) bump, of total height 1 in Λ.
  - The pilot's flat profile near λ ≈ 0.4–0.5 is uninformative for a different reason: F is never populated (non-stationary marginals, §4.1d), so no jump is present in the data. ∎

### 3.4 Proposition 3: gaps at the crossing; classical and quantum costs (DERIVED from standard bounds + INFERENCE for transfer)

1. **Gap upper bound.** For a reversible chain, δ ≤ 2Φ, where Φ = min_{S: π(S) ≤ ½} Q(S,S^c)/π(S) is the conductance (the Cheeger inequality, upper half; standard, not re-verified in these sessions).
   - Take S to be the minority phase (U or F), and a local kernel whose single steps cannot jump from U to F without passing through the interface region I. By reversibility, Q(S, S^c) ≤ π(I).
   - With e^{−ΔF‡(λ)} := π_λ(I)/min(π_λ(U), π_λ(F)), this gives δ_λ ≤ 2e^{−ΔF‡(λ)}.
   - This is an upper bound only. Cheeger's lower half gives δ ≥ Φ²/2, i.e. only ≳ e^{−2ΔF‡}. The Arrhenius/Eyring–Kramers estimate δ ≈ C^{-1}e^{−aΔF‡} with a ≈ 1 is assumption A-Arr (INFERENCE).
   - Toy check C3: −ln δ_min = 1.095·ΔF‡ + 5.4 over n = 25–100, where ΔF‡ ≈ 0.17n. The prefactor e^{−5.4} reflects the lazy single-flip step rate.
2. **The crossing cannot be skipped: a forced rung.**
   - **Separating-set argument.** Let η := (√p − √π_max(I))²/4 ≈ p/4, where π_max(I) := max_i π_{λ_i}(I) ≪ p. Suppose no rung has both π(F) ≥ η and π(U) ≥ η.
     - Let i be the last rung with π_i(F) < η. It exists because π_0(F) < η. Then π_{i+1}(F) ≥ η, so π_{i+1}(U) < η.
     - Cauchy–Schwarz within each region gives BC(λ_i, λ_{i+1}) ≤ √(π_i(U)π_{i+1}(U)) + √(π_i(F)π_{i+1}(F)) + √(π_i(I)π_{i+1}(I)) < 2√η + √π_max(I) = √p. That contradicts BC² ≥ p.
     - So **some rung λ_s has min(π(U), π(F)) ≥ η ≈ p/4** (≥ p in the two-point limit, §3.3).
   - **The gap there, in terms of λ_c.** Write Z_λ(S) := Σ_{x∈S} q e^{−λV}, r_U(λ) := Z_λ(I)/Z_λ(U) and r_F(λ) := Z_λ(I)/Z_λ(F).
     - By the exponential family, d ln r_U/dλ = E_{λ,U}[V] − E_{λ,I}[V] and d ln r_F/dλ = E_{λ,F}[V] − E_{λ,I}[V].
     - Under A-mono, r_U increases and r_F decreases in λ. π_λ(I) ≤ min(r_U, r_F)(λ).
     - At λ_c, Z(U) = Z(F), so r_U(λ_c) = r_F(λ_c) = e^{−ΔF‡(λ_c)}. Hence π_{λ_s}(I) ≤ e^{−ΔF‡(λ_c)} for λ_s on either side of λ_c.
     - With item 1: **δ_{λ_s} ≤ 2π_{λ_s}(I)/min(π_{λ_s}(U), π_{λ_s}(F)) ≤ (2/η)·e^{−ΔF‡(λ_c)} ≈ (8/p)·e^{−ΔF‡(λ_c)}.**
   - **Why a direct jump is forbidden (illustration).** With half-width h, the two-phase model gives BC(λ_c − h, λ_c + h) ≈ 2e^{−hΔV/2} (within-phase overlap ≈ 1).
     - With ΔV ≈ nJ ≈ 1.54n and h = 0.08, this is 0.43, 0.09, 0.02, 0.004 for n = 25–100, against C3's 0.49, 0.11, 0.025, 0.005.
     - The separating set, not this overlap, is what forces the rung.
   - Every admissible schedule therefore places a rung where the gap is at most (8/p)e^{−ΔF‡(λ_c)}. **DERIVED** (given A-mono).
3. **Quantum (QSA as constructed).**
   - By §3.2, this algorithm's reflections at λ_s cost Θ(δ_{λ_s}^{-1/2}) ≥ √(p/8)·e^{ΔF‡(λ_c)/2} walk steps each. This lower-bounds this algorithm's cost, not every quantum algorithm's.
   - The upper bound K·n_b·δ_*^{-1/2} becomes ~e^{aΔF‡/2} only under A-Arr.
   - C3 gives n_b·δ_*^{-1/2} ≈ 1.6×10⁵ (n_b = 1.01) vs 1/δ_min = 2.6×10¹⁰ at n=100. **Halving in δ: DERIVED. Halving in ΔF‡: under A-Arr.**
4. **Classical annealing / SMC along λ.** A lineage started in U at λ < λ_c remains in U past λ_c for ≳ e^{ΔF‡} local steps (under A-Arr), which gives hysteresis. Unbiased output needs either that many steps per lineage near λ_c, or a population with R ≳ 1/q_F lineages, so that at least one enters F before its weight dominates.
   - The probability of entering F is q_F ≈ max(π_0(F), n_loc·e^{−ΔF‡}). This combines exact prior draws landing in F with nucleation during the n_loc local steps spent near λ_c.
   - The **classical cost of the rare event is 1/q_F**. Amplitude amplification of a lineage that lands in F costs ~1/√q_F coherent lineage runs times O_rev. This needs the lineage simulation run reversibly over a seed register and a checkable "entered F" predicate (e.g. an order-parameter threshold) [B1]. Resampling itself is not an obstacle (S5.2).
   - **INFERENCE.** Not proved for SMC with adaptive resampling. [T2-12, T2-13] show SMC can be polynomial on other paths or under local-mixing conditions.
5. **Tempering.** Bhatnagar–Randall prove schedule-independent slow mixing for tempering on the mean-field 3-state Potts model (first-order in temperature) [E40]. Woodard et al. prove torpid PT/ST under persistence [E39]. Transfer to this λ-path is **INFERENCE**. The mechanism is the same: a joint (configuration, λ) bottleneck of mass ~e^{−ΔF‡}. ∎

### 3.5 Adiabatic routes (DERIVED + THEORETICAL)

- **Markov-chain Hamiltonian.** Let D_λ := Π_λ^{1/2} P_λ Π_λ^{−1/2}, where Π_λ = diag(π_λ).
  - D_λ is symmetric (by reversibility) and has the same spectrum as P_λ.
  - H_λ := I − D_λ then has ground state |π_λ⟩ with energy 0, and first excited energy 1 − μ_2(P_λ). That equals δ_λ for a lazy chain (A-rev).
  - For Metropolis with local moves, H_λ = Σ_moves h_m, where each h_m is PSD and annihilates |π_λ⟩ by detailed balance per move pair. H_λ is therefore stoquastic and frustration-free. **DERIVED.**
- Consequences:
  - An adiabatic or eigenpath traversal of H_λ costs O(path length/min gap) [A34] ≈ δ_*^{-1} at a first-order crossing.
  - Quadratic spectral-gap amplification is possible for frustration-free H and optimal in the black-box model [A33]. It gives √δ, i.e. ≈ δ_*^{-1/2}, which is QSA again.
  - **The adiabatic route offers nothing beyond S1** (**THEORETICAL [A33, A34] + DERIVED**).
- **Physical transverse-field annealing.** It encodes the problem as a diagonal Hamiltonian and interpolates from a driver.
  - At first-order quantum phase transitions, the gap closes exponentially with system size [T2-4]; the exactly solvable ferromagnetic models "reduce to the Grover problem in a particular limit". See also the review [T2-5].
  - Near the end of the algorithm, Anderson-localisation-type exponentially small gaps appear for large random instances with the standard transverse-field driver [T2-6]. This is contested in general: "all these negative results are only for a specific AQO algorithm" [T2-16].
  - Laumann et al. argue that "the thermodynamic order of the phase transitions is not predictive of the scaling of the gap", but that in MBL phases "the gaps are going to be typically exponentially small" [T2-7].
  - These results concern *ground-state* preparation. As a sampler of π_1 at T=1, an annealer returns a freeze-out distribution at an uncontrolled, instance-dependent temperature [A61–A63]. **Not a route to π_1.** **THEORETICAL + INFERENCE.**

### 3.6 Derivation of the break-even inequality (DERIVED)

- **Quantum per sample.** Wall-clock t_Q = N_walk·G·t_T, and cost C_Q = ρ·t_Q in core-second equivalents. The bottleneck stages dominate (§3.2), so N_walk ≈ K·n_b·δ_*^{-1/2} with δ_* = 1/τ_*. Hence C_Q = ρ K n_b G t_T √τ_*.
- **Classical cost for M samples.** C_C = c·(B_burn + M·B_best). (I-1) is M·C_Q < C_C. Divide by c and write R = G t_T/c.
- **(I-2).** Put B_best = τ_*/A with M large and B_burn ≲ B_best. Then ρK n_b R√τ_* < τ_*/A ⇔ τ_* > (AρK n_b R)² =: B\*.
- **(I-3)** is the logarithm of (I-2): ln τ_* > 2 ln(AρK n_b R). Under A-Arr (τ_* = C e^{aΔF‡}) it becomes ΔF‡ > [2 ln(AρK n_b R) − ln C]/a. v1 dropped ln C and set a = 1. With C3's values the break-even barrier drops by ≈ 5 nats and is rescaled by 1/1.1.
- **(I-4)** replaces one sample by a (σ/ε)-shot estimate on each side ([A30] quantum, CLT classical). At break-even both *task* wall-clocks are independent of σ/ε (S6).
- **Wall-clock at break-even.**
  - Classical: T\*_C = c·B\* = Aρ²(K n_b G t_T)²/c.
  - Quantum: T\*_Q = K n_b G t_T·√B\* = Aρ(K n_b G t_T)²/c.
  - For a quantum-runtime budget, T\*_Q ≤ T_budget ⇔ t_T ≤ √(T_budget·c/(Aρ))/(K n_b G).
- **(I-5), amplitude-amplified multistart.**
  - Classically, the expected cost to hit a given basin is n_dec·c/p_hit.
  - Quantumly, amplitude amplification [B1] needs about (π/4)p_hit^{-1/2} Grover iterations, each applying the reversible decoder and its inverse once, so ≈ (π/2)p_hit^{-1/2} decoder runs. There is a constant-factor overhead when p_hit is unknown.
  - Each run costs n_dec·G_grad·t_T·O_rev, where O_rev is the reversibility overhead from Bennett-type pebbling or the storage of L-BFGS history. n_dec cancels, which gives (I-5).
  - When the target basin is unknown, the marking step is itself minimum finding [C56], a further constant ≈ 22.5/(π/2) in decoder runs (sensitivity; §1 S6).
  - Reweighting (basin free energies) is charged equally to both sides in this comparison. That is favourable to quantum, since its reweighting would also need coherent free-energy estimation.

**Where the quadratic exponent comes from.** Every route above has cost ∝ (classical cost)^{1/2} × (per-step penalty R). The break-even classical cost therefore scales as R², which is the fault-tolerant break-even logic of [A56, A57/B46]. **DERIVED.**

### 3.7 Blocking reduction for S3(e) (DERIVED)

BBBV [C55] proves Ω(√M) quantum queries for unstructured search with **one** marked item among M. S3(e) needs the k-marked version, with k = qN. The reduction:
- Take M := ⌊1/q⌋ and group N items into M blocks of k = N/M items. The hard family marks all items of one hidden block.
- A query to item x of the k-marked item oracle is answered by one query to block(x) of the single-marked block oracle.
- A T-query algorithm that finds a marked item therefore gives a T-query algorithm for single-marked search over M blocks. So T = Ω(√M) = Ω(q^{−1/2}) quantum [C55], and Ω(M) = Ω(q^{−1}) classical.
- With uniform π_0 on items, π_0(F) = k/N ≈ q. Setting V = −β·1_F with e^β ≥ (1−q)/q gives π_1(F) ≥ ½. The potential's range is then βΔ ≈ ln(1/q), consistent with [A45]'s α = e^{βΔ} ~ 1/q. ∎

---

## 4. Numbers (every assumption labelled; PILOT data indicative only)

Source: output of `python research/theory/PROOFS/T2_sampling_checks.py`, rerun 2026-09-27 for this revision while G1 jobs were still writing files. The mode census in particular is a moving snapshot.

### 4.1 Pilot NRPT runs (C4; PILOT)

| crop | L | rungs N | Λ | E(P_N) | scans | RT stationary (v1) | **RT predicted, transit-aware ELE (C4 sim)** | P(0) under exact ELE | observed RT | local steps / scan | ELE-ideal cost / RT | 95% bound / RT |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 5O37A_45 | 45 | 30 | 13.6 | 26.3 | 1500 | 27.5 | **9.8 ± 2.6** | ≈ 5×10⁻⁵ | 0 | 262 | 1.4×10⁴ | 2.4×10⁴ |
| 3GAHA_60 | 60 | 32 | 14.4 | 27.5 | 1200 | 21.1 | **4.8 ± 1.9** | 3.7×10⁻³ | 0 | 280 | 1.6×10⁴ | 2.0×10⁴ |
| 5O37A_100 | 100 | 39 | 24.9 | 87.2 | 800 | 4.5 | **0.00** | ≈ 1 | 0 | 343 | 6.0×10⁴ | — |
| 4LPQA_120 | 120 | 37 | 25.2 | 90.9 | 600 | 3.3 | **0.00** | 1 | 0 | 325 | 6.0×10⁴ | — |
| 5O37A_150 | 150 | 39 | 29.3 | 150.2 | 500 | 1.7 | **0.00** | 1 | 0 | 343 | 1.0×10⁵ | — |

Stage counts, glassy n_b and energy ranges (C4; second halves of each run):

| L | ℓ = 0.63Λ | ℓ = 𝓛_SD/√8 | CS pilot estimate √(E₀V−E₁V)/√8 (biased low) | n_b(λ ≥ 0.3), Λ-based / SD-based | E₀V − E₁V (nats) | βΔ lower bound, full E (nats) | c (ms/local step, A-c) |
|---|---|---|---|---|---|---|---|
| 45 | 8.5 | 8.7 | 20.0 | 2.9 / 2.6 | 3.2×10³ | 3.1×10³ | 0.30 |
| 60 | 9.0 | 9.9 | 21.3 | 3.3 / 3.7 | 3.6×10³ | 3.4×10³ | 0.40 |
| 100 | 15.6 | 23.4 | 50.6 | 5.4 / 9.3 | 2.1×10⁴ | 2.0×10⁴ | 0.75 |
| 120 | 15.8 | 21.3 | 60.9 | 5.2 / 7.6 | 3.0×10⁴ | 2.9×10⁴ | 1.23 |
| 150 | 18.3 | 62.2 | 82.1 | 6.7 / 36.8 | 5.4×10⁴ | 5.4×10⁴ | 1.80 |

Readings (INFERENCE):
- **(a) Significance.** The ELE deficit is significant at L = 45 (P(0) ≈ 5×10⁻⁵; one crop, one seed) and marginal at L = 60 (3.7×10⁻³). At L ≥ 100 an ideal ELE sampler would also show 0 trips in these run lengths, so the runs carry no information. The deficit is attributed jointly to A1 and A2 violation (S4). That it reflects small stationary gaps is a hypothesis.
- **(b) Classical per-sample cost is only lower-bounded, per round trip.**
  - At L = 45 and 60, zero trips is consistent at 95% only with a cost per round trip ≥ 2.4×10⁴ and 2.0×10⁴ local steps. This is within the model family "ELE index process with all rejection odds scaled by a factor f" (f₉₅ ≈ 1.7 and 1.3), so it is model-dependent.
  - v1's transit-free Poisson bound (1.3×10⁵ and 1.1×10⁵) was ≈ 5.5× too strong.
  - At L ≥ 100 the runs give no bound. The ELE-ideal cost per round trip on these schedules is (2+2E)·s = 6.0×10⁴, 6.0×10⁴ and 1.0×10⁵ local steps (INFERENCE that ELE is the best case for the index process).
  - **"One round trip per independent sample" is an INFERENCE.** [T2-1] reports that round-trip rate correlates with ESS but does not prove the relation, and the λ=1 rung could decorrelate through local moves without any round trip.
  - Against B\* (§4.3), break-even needs B_best to exceed these lower bounds by ≥ 5 orders of magnitude (T3-D3 target) or ≥ 6.5 orders (A80 target) in the most optimistic scenarios. **The pilot neither establishes nor excludes that.**
- **(c) No variance peak.** The rung-mean E_pair decreases smoothly with λ, and its SD decreases monotonically (e.g., L=45: SD 14 → 12 over λ = 0.43 → 0.49). There is no variance peak of the kind a populated two-phase crossing at equilibrium produces (SD ≈ ΔV/2 at λ_c). This is uninformative while F is unpopulated (§3.3 iv).
- **(d) Drift.** The rungs at λ ≥ 0.3 drift down between the first and second halves of each run. The mean E_pair falls by 1–26 nats (L=45), 8–28 (L=60), 72–204 (L=100), 83–167 (L=120) and 326–732 (L=150). The runs are not stationary, increasingly so with L, and both ℓ estimators and the CS estimate inherit this.
- Taken together, (c) and (d) mean the pilot does not yet separate "first-order, seen out of equilibrium" from "glassy/persistent trapping". That is D1.
- **Per-local-step cost.**
  - Pilot wall-clock, including sampler overhead: 0.59, 0.78, 1.46, 2.39 and 3.51 ms at L = 45, 60, 100, 120 and 150. The micro-benchmark gives 1.8 ms at L=150.
  - v1 mixed the two measurements. C6 now applies one overhead correction (÷1.95) at every L (A-c). A smaller c raises B\* ∝ c⁻², so using the uncorrected wall-clock would have favoured quantum by 3.8×.
- **Energy scale.** For the full energy, βΔ ≥ E₀[E_pair] − E_polished = 3.1×10³ (L=45) to 5.4×10⁴ nats (L=150), from the bound in S2. α = e^{βΔ} in [A45] is therefore astronomically large.

### 4.2 Mode census snapshot (C5; PILOT, still being written; rerun 2026-09-27)

| L | targets | at the 1/256 floor | p_hit(best found) median | min | max | geo-mean | modes median | local steps / restart |
|---|---|---|---|---|---|---|---|---|
| 30 | 16 | 1 | 0.117 | 0.0039 (floor) | 0.945 | 0.101 | 82 | 174 |
| 45 | 16 | 1 | 0.109 | 0.0039 (floor) | 0.613 | 0.070 | 109 | 193 |
| 60 | 16 | 4 | 0.049 | 0.0039 (floor) | 0.398 | 0.047 | 150 | 203 |
| 80 | 16 | 3 | 0.059 | 0.0039 (floor) | 0.246 | 0.041 | 181 | 213 |
| 100 | 16 | 4 | 0.016 | 0.0039 (floor) | 0.137 | 0.016 | 244 | 217 |
| 120 | 7 | 3 | 0.008 | 0.0039 (floor) | 0.020 | 0.008 | 252 | 217 |

Readings (INFERENCE):
- p_hit is the hit rate of the **best-found** mode. It is censored at 1/256, and the true global mode may be missed, so it is an upper bound on the hit rate of the true best basin.
- The median declines slowly over L = 30 → 80 (0.12 → 0.06), then drops to 0.016 (L=100, 16 targets) and 0.008 (L=120, 7 targets).
- At L ≥ 100, 244–252 distinct modes come from 256 restarts. The census is **near saturation**: almost every restart finds a new mode. p_hit there is only partly resolved (4 of 16 and 3 of 7 targets sit at the floor).
- This is consistent with a sharp rise in landscape multiplicity at L ≈ 100. (v1 read this from 3 targets. A reviewer's rerun had 8, this rerun has 16, and the census is still being written.) D6 must repeat it with more restarts.
- The Laplace "masses" in the census files are unreliable: the L=45 test file shows 26–34 non-positive Hessian eigenvalues at the reported minima. D6 therefore specifies TI/BAR basin free energies.
- **Against (I-5).** Targets resolved above the floor have p_hit ≥ 2/256 ≈ 0.008. That is **≥ 9 orders of magnitude above p\*** (§4.3; p\* ≤ 1.0×10⁻¹¹ at L=45 and ≤ 2.8×10⁻¹² at L=100), and up to 18 orders.
  - **Floor-censored targets are unresolved.** p_hit < 0.0039 is not bounded below, so for those targets the gap to p\* is not established.
  - The pilot cost to hit the best-found mode is ~10³–5×10⁴ local steps.

### 4.3 Break-even thresholds (C6; assumptions A-G (T3), A-t, A-K, A-ρ, A-c, n_b; A = 1)

`B* = (K n_b R)²` local steps per sample, with R = G t_T/c. ln B\* is reported directly. ΔF‡\* = (ln B\* − ln C)/a uses the C3 toy values (a = 1.095, ln C = 5.4) under A-Arr and is a sensitivity only. T\*_Q = ρ(K n_b G t_T)²/c is the minimum quantum wall-clock per sample at break-even; at ρ = 1 it equals the classical wall-clock. Qubits are T3 central values, one factory, d = 31.

| L | scenario | G (Toffolis/step) | t_T | K | n_b | B\* | ln B\* | ΔF‡\* (A-Arr) | T\*_Q | logical / physical qubits |
|---|---|---|---|---|---|---|---|---|---|---|
| 45 | most optimistic, T3-D3 target | 5.0×10⁶ (D3 gen) | 1 µs | 10 | 1 | 2.7×10¹⁰ | 24.0 | 17.0 | 0.26 yr | 6.0×10³ / 1.3×10⁷ |
| 45 | most optimistic, A80 target | 1.0×10⁷ (D2 gen) | 1 µs | 10 | 1 | 1.1×10¹¹ | 25.4 | 18.3 | 1.05 yr | 1.5×10⁴ / 3.1×10⁷ |
| 45 | A-FO central | 4.6×10⁷ (D2 cen) | 10 µs | 100 | 2 | 9.4×10¹⁶ | 39.1 | 30.8 | 9.0×10⁵ yr | 1.5×10⁴ / 3.1×10⁷ |
| 45 | cited constants | 4.6×10⁷ | 170 µs | 10³ | 2 | 2.7×10²¹ | 49.3 | 40.1 | 2.6×10¹⁰ yr | 1.5×10⁴ / 3.1×10⁷ |
| 100 | most optimistic, T3-D3 target | 1.1×10⁷ | 1 µs | 10 | 1 | 2.2×10¹⁰ | 23.8 | 16.8 | 0.53 yr | 9.6×10³ / 2.0×10⁷ |
| 100 | most optimistic, A80 target | 4.8×10⁷ | 1 µs | 10 | 1 | 4.0×10¹¹ | 26.7 | 19.5 | 9.6 yr | 3.3×10⁴ / 6.7×10⁷ |
| 100 | A-FO central | 2.3×10⁸ | 10 µs | 100 | 2 | 3.7×10¹⁷ | 40.5 | 32.0 | 8.9×10⁶ yr | 3.3×10⁴ / 6.7×10⁷ |
| 100 | glassy (n_b = stages at λ ≥ 0.3, Λ-based) | 2.3×10⁸ | 10 µs | 100 | 5.4 | 2.8×10¹⁸ | 42.5 | 33.8 | 6.5×10⁷ yr | 3.3×10⁴ / 6.7×10⁷ |
| 150 | most optimistic, T3-D3 target | 1.8×10⁷ | 1 µs | 10 | 1 | 1.0×10¹⁰ | 23.1 | 16.1 | 0.59 yr | 1.3×10⁴ / 2.6×10⁷ |
| 150 | most optimistic, A80 target | 1.1×10⁸ | 1 µs | 10 | 1 | 3.5×10¹¹ | 26.6 | 19.3 | 20 yr | 4.9×10⁴ / 1.0×10⁸ |
| 150 | A-FO central | 5.1×10⁸ | 10 µs | 100 | 2 | 3.3×10¹⁷ | 40.3 | 31.9 | 1.9×10⁷ yr | 4.9×10⁴ / 1.0×10⁸ |
| 150 | glassy (Λ-based / SD-based n_b) | 5.1×10⁸ | 10 µs | 100 | 6.7 / 36.8 | 3.7×10¹⁸ / 1.1×10²⁰ | 42.7 / 46.1 | 34.1 / 37.2 | 2.1×10⁸ yr / 6.3×10⁹ yr | 4.9×10⁴ / 1.0×10⁸ |
| 150 | pessimistic (n_b = ℓ_SD) | 5.1×10⁸ | 170 µs | 10³ | 62.2 | 9.1×10²⁴ | 57.5 | 47.6 | 5.2×10¹⁴ yr | 4.9×10⁴ / 1.0×10⁸ |

The full grid is in the script output: L ∈ {45, 60, 100, 120, 150} × {T3-D3 gen, T3-D2 gen, T3-D2 cen} × six n_b cases × six (t_T, K) pairs.

**Range:**
- B\* = 1.0×10¹⁰ (T3-D3, most optimistic) or 1.1×10¹¹ (A80, most optimistic) up to 9×10²⁴;
- ln B\* = 23–58;
- T\*_Q = 0.26 yr to 5×10¹⁴ yr.

Changes from v1 (2×10¹² – 1.4×10²²) come from n_b replacing ℓ (down to 1/ℓ² in B\*), T3's G(L), the K = 10³ row, and c(L).

| (I-5) amplitude-amplified multistart | p\* range over T3-D2 gen/cen, t_T 1–170 µs, O_rev ∈ {2, 10}, (π/2) |
|---|---|
| L = 45 | 6.7×10⁻¹⁹ – 1.0×10⁻¹¹ |
| L = 100 | 1.7×10⁻¹⁹ – 2.8×10⁻¹² |

Dürr–Høyer minimum finding for an unknown target basin lowers p\* by a further ≈ 200× (sensitivity).

**Minimum useful runtime (DERIVED; S6 corollary).**

| t_T needed so that T\*_Q ≤ budget (ρ = 1) | L=45 | L=100 | L=150 |
|---|---|---|---|
| budget 1 day, A80 target, most optimistic (D2 gen, K=10, n_b=1) | 51 ns | 17 ns | 12 ns |
| budget 1 day, T3-D3 target, most optimistic | 103 ns | 72 ns | 68 ns |
| budget 1 day, A-FO central (D2 cen, K=100, n_b=2) | 0.55 ns | 0.18 ns | 0.12 ns |
| budget 1 year, A80 target, most optimistic | 980 ns | 320 ns | 230 ns |
| budget 1 year, T3-D3 target, most optimistic | 2.0 µs | 1.4 µs | 1.3 µs |
| budget 1 year, A-FO central | 11 ns | 3.4 ns | 2.3 ns |

**Interpretation (INFERENCE).**
- **What the numbers do not show.** The pilot gives only lower bounds on classical cost, so it cannot show that quantum falls short of break-even. v1's "7 or more orders of magnitude short" is withdrawn. Break-even needs B_best ≥ B\* ≥ ~10¹⁰ (any target) or ~10¹¹ (A80 target) in the most optimistic scenarios. The pilot neither establishes nor excludes this; D4/D5 decide.
- **What the numbers do show (robust).** Whatever the classical cost, an advantage appears only at a per-sample quantum wall-clock ≥ T\*_Q:
  - ≥ 3–7 months in the single most optimistic scenario, which samples the Cartesian T3-D3 target (1 µs Toffolis, K = 10, n_b = 1);
  - ≥ 1–20 years for the A80 target under the same assumptions;
  - ≥ 10⁵–10⁷ years at A-FO central values.
- Past break-even the quantum side wins but gets slower still: its wall-clock grows as √τ_*.
- There is therefore **no parameter regime** in which this route gives a sample in under a day and beats classical, unless t_T falls to ≤ 12–100 ns (most optimistic) or the sub-ns range (central). That is 3.5–6 orders of magnitude below 170 µs.
- ρ = 1 prices a machine with 10⁷–10⁸ physical qubits as one CPU core.
- This is the Sanders/Babbush conclusion [A56, A57] (and Lemieux et al.'s ~1 ns requirement against Janus [A55]) instantiated for this energy.

### 4.4 Toy first-order model (C3; DERIVED numerics, not protein data)

- Model: V(m) = −nJ(m/n)^{12}, prior = Binomial(n, ½) (a product state), J chosen so that λ_c ≈ 0.45. The table is in S3b.
- Λ ≈ 1.05 and 𝓛 ≈ 3.3–3.4 for every n. Two QSA stages satisfy the overlap condition, with the forced rung at w_F ≈ 0.86 ≈ 1−p.
- δ_min falls from 8×10⁻⁵ to 4×10⁻¹¹ as ΔF‡ grows from 3.7 to 17 nats. The greedy schedule's n_b is 1.22 → 1.01.
- QSA-type cost n_b·δ_*^{-1/2} ≈ 1.3×10² → 1.6×10⁵; classical 1/δ_min = 1×10⁴ → 3×10¹⁰.
- The warm-start factor across the forced stage is 1+χ² ≈ 2.7×10⁷ → 1.2×10³⁵, even though BC² ≥ e^{−2}. Classical annealing pays ½ln(1+χ²) ≈ 9–40 as a multiplier of τ in the spectral bound.

---

## 5. Literature

### 5.1 Keys from `research/literature/BIBLIOGRAPHY.md` used here

| Key | Paper (short) | Used for | Label |
|---|---|---|---|
| A1 | Szegedy 2004 | walk phase gap Θ(√δ) (absolute gap) | THEORETICAL |
| A2 | Magniez–Nayak–Roland–Santha 2011 | approximate reflection by phase estimation | THEORETICAL |
| A7 | Wocjan–Abeyesinghe 2008 | QSA qsample along slow-varying chains | THEORETICAL |
| A8 | Somma, Boixo, Barnum, Knill, "Quantum simulations of classical annealing processes," PRL 101, 130504 (2008); arXiv 0804.1571 | 1/√δ annealing | THEORETICAL |
| C74 | Somma, Boixo, Barnum, "Quantum Simulated Annealing," arXiv 0712.1008 (preprint; no Knill, no journal ref; author list re-checked via arXiv API in this revision) | 1/√δ annealing (separate record) | THEORETICAL |
| A9 | Orsucci–Briegel–Dunjko 2018 | cold-start √N penalty | THEORETICAL |
| A11 | Aharonov–Ta-Shma 2003 | general qsampling ⇒ SZK ⊆ BQP; adiabatic state generation | THEORETICAL |
| A14, A15, A16, A18 | Chen–Lovász–Pak; Diaconis–Holmes–Neal; Apers et al.; Dervovic | classical lifting | THEORETICAL |
| A28 | Wocjan–Temme 2023 | Szegedy phase gap for maps | THEORETICAL |
| A30 | Montanaro 2015 | quantum mean estimation (also of classical randomised procedures run reversibly) | THEORETICAL |
| A31 | Harrow–Wei SODA 2020 | adaptive QSA for Bayesian inference; Thm 4, 5, 10; no-cloning remark on intermediate states (PDF read in v1) | THEORETICAL |
| A33 | Somma–Boixo 2013 | spectral-gap amplification (quadratic, optimal for frustration-free) | THEORETICAL |
| A34 | Boixo–Knill–Somma 2010 | eigenpath traversal O(L/G) | THEORETICAL |
| A36 | Ozols–Roetteler–Roland 2012 | quantum rejection sampling | THEORETICAL |
| A44 | Leng et al., PNAS 2026 | quantum Langevin and RELD costs; warm start | THEORETICAL (same-chain) |
| A45 | Olivucci et al. 2026 (preprint) | Ω(α) vs Õ(√α) continuous separation, "first" provable (abstract re-verified in v1) | THEORETICAL (L1 for its family; L0 for A80) |
| A47 | Layden et al., Nature 619, 282 (2023) | quantum-enhanced MCMC; heuristic fitted gap scaling, n ≤ 10 | HEURISTIC / DISPUTED |
| A48 | Orfi–Sels 2024 (preprint) | bound on quantum-enhanced MCMC speedup; none in the worst case | NO ADVANTAGE (worst case) |
| A52, A54 | Ferguson–Wallden 2025; Cao et al. 2026 (preprint) | quantum-enhanced MCMC variants | SIMULATOR / HEURISTIC |
| A55 | Lemieux et al. 2020 | Metropolis coin circuits | resource |
| A56 = C64 | Sanders et al. 2020 | 170 µs/Toffoli single factory; SK and LABS step costs (Tables VIII–IX); "a day and a million physical qubits … four CPU-minutes" | resource / NO ADVANTAGE |
| A57 = B46 | Babbush et al. 2021 | quadratic speedups fail early FT break-even | NO ADVANTAGE |
| A59, A60 | Häner et al.; Babbush et al. 2018 (QROM; linear cost read by T3, not re-verified by T2) | arithmetic / lookup cost basis | resource |
| A61–A64 | Amin; Benedetti et al.; Vuffray et al.; Isakov et al. | annealers as uncontrolled samplers; QMC tunnelling | THEORETICAL / HW |
| A75, E50 | Beskos et al.; Roberts–Gelman–Gilks | HMC d^{1/4} vs RWM d scaling (A-chain) | THEORETICAL |
| A78, A79 | Boltzmann generators; BioEmu | learned independence proposals (D5f) | EMPIRICAL (classical) |
| B1 | Brassard–Høyer–Mosca–Tapp 2002 | amplitude amplification | THEORETICAL |
| B66 | Wang–Landau 2001 | flat-histogram sampling | classical |
| B67 | Skilling 2006, "Nested sampling for general Bayesian computation," Bayesian Analysis 1(4) | nested sampling (S5.1, D5g) | classical |
| C55 | Bennett–Bernstein–Brassard–Vazirani 1997 | Ω(√N) search lower bound (needle reduction, §3.7) | THEORETICAL / NO-GO |
| C56 | Dürr–Høyer 1996 (preprint) | quantum minimum finding O(c√N) (abstract verified in this revision; constant 22.5 from the body not verified) | THEORETICAL |
| C78 | Wang–Machta–Katzgraber 2015 (PRE 92, 013303) | PA vs SA vs PT for ground states | classical |
| E33 | Machta 2009 | PT: polynomial for energetic, not entropic barriers | THEORETICAL |
| E38, E39 | Woodard–Schmidler–Huber 2009 | rapid / torpid tempering; persistence | THEORETICAL |
| E40 | Bhatnagar–Randall 2016 (abstract re-verified in v1) | tempering slow at first-order transitions regardless of schedule; entropy dampening | THEORETICAL |
| E74, E75 | Del Moral–Doucet–Jasra 2006; Neal 2001 | SMC samplers; AIS (weight-variance cost) | classical (metadata-verified) |

### 5.2 Verified in these sessions, not yet in BIBLIOGRAPHY.md (recommend adding)

[T2-1]–[T2-13] were verified via the arXiv export API (`export.arxiv.org/api/query?id_list=…`) on 2026-09-26. [T2-1] and [A31] were also read in full from their arXiv PDFs in v1. [T2-1] §7.2 was re-read from the PDF in this revision. [T2-14]–[T2-16] were verified via the arXiv API on 2026-09-27, with abstracts quoted in the text.

| Key | Citation | arXiv / DOI | Used for |
|---|---|---|---|
| T2-1 | Syed, Bouchard-Côté, Deligiannidis, Doucet, "Non-Reversible Parallel Tempering: a Scalable Highly Parallel MCMC Scheme," JRSS-B (2022) | arXiv 1905.02939; DOI 10.1111/rssb.12464 | Thm 1 (E[T] = 2(N+1)+2(N+1)E(P_N)), Cor. 1 (τ_DEO = 1/(2+2E)), Thm 2 (λ_loc = ½E\|V₁−V₂\|), Thm 3 (τ → 1/(2+2Λ)), ELE assumption (A2), §7.2 robustness (n_expl ∈ {0, d/2, …, 32d}) |
| T2-2 | Syed, Romaniello, Campbell, Bouchard-Côté, "Parallel Tempering on Optimized Paths" | arXiv 2102.07720 (venue not verified here) | linear path poor when reference and target nearly singular; spline paths |
| T2-3 | Surjanovic, Syed, Bouchard-Côté, Campbell, "Parallel Tempering With a Variational Reference" | arXiv 2206.00080 (venue not verified here) | variational reference to avoid prior–posterior singularity |
| T2-4 | Jörg, Krzakala, Kurchan, Maggs, Pujos, "Energy gaps in quantum first-order mean-field-like transitions: The problems that quantum annealing cannot solve," EPL 89, 40004 (2010) | arXiv 0912.4865; DOI 10.1209/0295-5075/89/40004 | exponential gap closure at first-order QPTs; Grover limit |
| T2-5 | Bapst, Foini, Krzakala, Semerjian, Zamponi, "The Quantum Adiabatic Algorithm applied to random optimization problems: the quantum spin glass perspective," Phys. Rep. 523, 127 (2013) | arXiv 1210.0811; DOI 10.1016/j.physrep.2012.10.002 | review (orientation) |
| T2-6 | Altshuler, Krovi, Roland, "Anderson localization makes adiabatic quantum optimization fail," PNAS 107, 12446 (2010) (arXiv title: "…casts clouds over…") | arXiv 0912.0746; DOI 10.1073/pnas.1002116107 | exponentially small gaps near the end of the anneal, **for the standard transverse-field driver; contested in general [T2-16]** |
| T2-7 | Laumann, Moessner, Scardicchio, Sondhi, "Quantum annealing: the fastest route to quantum computation?," EPJ ST 224, 75 (2015) | arXiv 1411.5710; DOI 10.1140/epjst/e2015-02344-2 | order of transition not predictive; MBL ⇒ exponentially small gaps |
| T2-8 | Berg, Neuhaus, "Multicanonical Ensemble: A New Approach to Simulate First-order Phase Transitions," PRL 68, 9 (1992) | arXiv hep-lat/9202004; DOI 10.1103/PhysRevLett.68.9 | tunnelling time ~L^{2.65} (2D 10-state Potts) |
| T2-9 | Crooks, "Measuring thermodynamic length," PRL 99, 100602 (2007) | arXiv 0706.0559; DOI 10.1103/PhysRevLett.99.100602 | thermodynamic length as metric (𝓛) |
| T2-10 | Neuhaus, Hager, "2D Crystal Shapes, Droplet Condensation and Exponential Slowing Down in Simulations of First-Order Phase Transitions," J. Stat. Phys. 113, 47 (2003) | arXiv cond-mat/0201324 | multicanonical still exponential (barriers ∝ L^{d−1}) via droplet shape transitions |
| T2-11 | Machta, "Population Annealing with Weighted Averages: A Monte Carlo Method for Rough Free Energy Landscapes," PRE 82, 026704 (2010) | arXiv 1006.0252; DOI 10.1103/PhysRevE.82.026704 | population annealing (Hukushima–Iba) |
| T2-11b | Machta, Ellis, "Monte Carlo Methods for Rough Free Energy Landscapes: Population Annealing and Parallel Tempering," J. Stat. Phys. 144, 541 (2011) | arXiv 1104.1138; DOI 10.1007/s10955-011-0249-0 | PA converges ∝ 1/work, PT exponentially |
| T2-11c | Barash, Weigel, Shchur, Janke, "Exploring first-order phase transitions with population annealing," EPJ ST 226, 595 (2017) | arXiv 1704.01888; DOI 10.1140/epjst/e2016-60389-4 | PA at first-order transitions (preliminary observations only) |
| T2-12 | Paulin, Jasra, Thiery, "Error Bounds for Sequential Monte Carlo Samplers for Multimodal Distributions" | arXiv 1509.08775 (journal not verified here) | "interpolation to independence": polynomial SMC on Potts where PT is exponential |
| T2-13 | Mathews, Schmidler, "Finite Sample Complexity of Sequential Monte Carlo Estimators on Multimodal Target Distributions" | arXiv 2208.06672 (journal not verified here) | SMC FPRAS on multimodal problems with only local mixing |
| **T2-14** | Pfeifenberger, Rumetshofer, von der Linden, "Nested sampling, statistical physics and the Potts model" | arXiv 1603.02516 (no journal ref in the arXiv record) | nested sampling on Potts q > 4 (first-order): "one run stops after O(N) moves"; compared with multicanonical sampling |
| **T2-15** | Pártay, Bartók, Csányi, "Efficient sampling of atomic configurational spaces" | arXiv 0906.3544 (journal not verified here) | nested sampling on LJ clusters: "efficiency gain over parallel tempering in calculating the heat capacity is more than an order of magnitude" |
| **T2-16** | Choi, "Different Adiabatic Quantum Optimization Algorithms for the NP-Complete Exact Cover and 3SAT Problems," Quantum Inf. Comput. 11(7&8), 638–648 (2011) | arXiv 1010.1221 | "all these negative results are only for a specific AQO algorithm" (qualifies [T2-6]) |

**Unverified, not cited as evidence:**
- the Cheeger inequality δ ≤ 2Φ and δ ≥ Φ²/2 (standard textbook results; no specific source verified in these sessions);
- the Dürr–Høyer constant 22.5 (paper body; used only as a sensitivity);
- a quantum HMC walk ("Quantum Dynamical Hamiltonian Monte Carlo", arXiv 2403.01775, an unverified lead in the bibliography);
- quantum multivariate mean estimation (not searched);
- the Neuhaus–Hager/Janke protein application (bibliography lead #44);
- a quantum nested-sampling algorithm (not searched).

---

## 6. Scope and what is NOT claimed

- **Not claimed:** any quantum advantage over the best classical method, at any level. The relative-to-best level is L0. The same-chain statements (L2, and L3 with T3's G(L)) are about *known* algorithms relative to the chain they quantise, plus *black-box* lower bounds (NO-GO). No claim is made that a structured learned energy is quantum-hard or classically hard.
- **Not claimed:** that the pilot bottleneck is first-order. S3 is conditional on A-FO, and D1 tests it. The pilot fits glassy/persistent trapping equally well.
- **Not claimed:** that the pilot's zero round trips measure small stationary gaps. They are equally explained by non-stationarity and n_expl = 1 (S4). That is a hypothesis.
- **Not claimed:** that break-even is out of reach by a known margin. The pilot only lower-bounds classical cost (§4.3 interpretation). Only the minimum-runtime corollary is independent of the classical cost.
- **Not claimed:** exact Toffoli counts beyond T3's model. G(L) is T3's DERIVED estimate under T3's assumptions. T3-D3 samples a different target.
- **Not claimed:** that SMC with resampling cannot be quantum-accelerated. It *is* quantisable in the Montanaro / amplitude-amplification sense (S5.2). What is not in the verified literature is a speedup of its internal sequential mixing, or a garbage-free qsample output.
- **Not claimed:** that the posterior at T=1 is the right scientific object. Hardness is a property of (E, T) and of the path. Transmission of sampled structures to accuracy is gated separately (H-006, G1).
- **Query complexity is not runtime.** Walk-step statements (S1, S2) are L2. Runtime needs G(L), t_T and ρ (S6).
- **No simulator results** are used or implied. C3 is a classical toy computation of spectral gaps, and C4's index-process simulation is a classical Monte Carlo of swap events. Neither is a quantum simulation.
- **The lower bound S3e (NO-GO) holds only for needle/hidden-basin instances.** Funnelled energies are outside it, and there classical methods may be polynomial.

## 7. Open gaps

1. **G1-D1 (bottleneck type).** First-order vs glassy is undetermined (UNPROVEN). It needs the hysteresis and bimodality protocol.
2. **ΔF‡(L) scaling and its extrapolation (UNPROVEN).** No measurement yet. It decides (I-3) through the pre-registered model of D2. τ_* ≳ 10¹⁰ local steps cannot be measured directly.
3. **Transfer of tempering torpidity** (E39, E40) to the learned λ-path (INFERENCE only). A rigorous statement would need a conductance bound on the joint (x, λ) chain for a two-basin model with product reference.
4. **Within-lineage mixing in quantised bypasses.** SMC/PA and nested sampling are quantisable in the Montanaro / amplitude-amplification sense (S5.2). Open (UNPROVEN): a quantum speedup of their internal sequential mixing beyond QSA-type δ^{-1/2}, a garbage-free coherent output, and the cost of coherent basin free-energy estimation for the mode-finding bypass.
5. **Quantum HMC and κ_chain.** The HMC kernel is not a Szegedy-ready chain. A-chain's κ_chain may cost the quantum side a factor ~d^{3/4} ≈ 50 at L=100, and more under lever-arm rejection (INFERENCE; D4 measures it).
6. **The per-stage constant K** in [A7, A31] is untracked. The stated formula gives K ≈ 700. A tighter analysis (fixed-point amplitude amplification, better phase estimation) could reduce it toward 10–100, which the tables assume in two of three K columns. This changes B\* by at most ≈ 5×10³.
7. **Move-set locality (with T3).** A single torsion (pivot) move changes all j(L−j) straddling pair distances, i.e. Θ(L²) for mid-chain moves, **both classically and coherently**. O(L) work per step requires local moves: crankshaft moves, or Cartesian single-residue moves (T3-D3, ≈ 4L pair terms, with the move index coherent via QROAM over (residue, segment)). Those moves change the target (bond relaxation) and the per-step mixing κ. v1's "a move register could lower G by ~L" does not hold for the current move set.
8. **Continuous-domain conditions** of [A44, A45] (torus, smoothness) versus walled θ and learned tables. Applicability is only approximate (A-dom).
9. **Bibliography integration.** [T2-1] … [T2-16] should be added to `research/literature/BIBLIOGRAPHY.md` by its maintainer. This note does not edit that file.
10. **A-δ (certified gap lower bound).** QSA needs one. No procedure in the verified literature supplies it in the hard regime, and failure is silent on both the classical and the quantum side (UNPROVEN).
11. **Data gaps.** (a) C4 rows for G1 runs with pivot moves (the analysed pilot files are HMC-only). (b) c(L) on an idle node (D7). (c) Completion of the L ≥ 100 census with more restarts (D6). (d) More seeds and crops for the ELE-deficit significance at L = 45–60.

---

## 8. Response to review

No objection was rejected outright. Every objection is resolved in the text (§9). The points below were accepted only in part, or resolved differently from the fix the reviewer proposed. Each gives the reason.

1. **R1-1 (P(0) at L=45 "below 5×10⁻⁵ (0 of 20,000)").** Zero events in 20,000 replicates supports only P(0) < 1.5×10⁻⁴ at 95% (rule of three), not < 5×10⁻⁵. The script's run found 1 of 20,000, and a second seed 0 of 20,000. The note reports P(0) ≈ 5×10⁻⁵, consistent with the Poisson value e^{−9.8} ≈ 6×10⁻⁵ and the under-dispersion of the simulated count. The substance of the objection (transit, 9.8 and 4.8 predicted trips, uninformative at L ≥ 100) is accepted in full.
2. **R1-2 (transit-aware bound "roughly 4–5×10⁴ and 2–3×10⁴").** The note's own bisection within the stated model family gives 2.4×10⁴ (L=45) and 2.0×10⁴ (L=60) local steps per round trip. Any such bound depends on the model, since zero trips gives no model-free rate bound. The note reports its own values with the model named. The ELE-floor values at L ≥ 100 (6.0×10⁴, 6.0×10⁴, 1.0×10⁵) match the reviewer's.
3. **R1-3 vs R2-4 (n_b ∈ [2, ℓ] with n_b = 2 most optimistic, vs ℓ_eff = 1–2).** The two proposals differ only by a normalisation factor of 2. This note defines n_b with the ½ of §3.2, so that uniform gaps give n_b = ℓ (matching [A7]'s uniform bound with the same K) and a single-rung bottleneck gives n_b = 1. C3 measures n_b = 1.01–1.22 for the greedy schedule, which supports the lower end. Both n_b = 1 (most optimistic) and n_b = 2 (A-FO central) are tabulated.
4. **R1-6 (Cauchy–Schwarz values "not a valid upper bound").** Accepted. They are now labelled "pilot estimate of the bound (biased low)".
5. **R1-14 (use micro-benchmark c(L) at every L).** A micro-benchmark was attempted in this revision but was unusable: the machine was running three G1 jobs, and single-structure calls cost 9–14 ms at every L (PyTorch per-call overhead). The reviewer's alternative, one overhead correction throughout, was applied instead (A-c). A clean D7 remains open (§7 gap 11b).
6. **R2-2 ("set A_q ≈ 1 for the rare-event SMC bypass").** Accepted up to the reversibility overhead: A_q ≈ O_rev ≥ 1, a small constant. The quantised SMC gains a square root on the rare-event factor, not on its internal mixing, and it does not output a garbage-free qsample.
7. **R2-3 (the §7.2 range "n_expl ≥ d_var/2").** Verified from the PDF in this revision: the tested values are n_expl ∈ {0, d/2, d, 2d, …, 32d}. The pilot's n_expl = 1 is below the smallest non-zero value tested. One addition: the analysed pilot files contain **no pivot moves** (§2.2), although the program summary describes the pilot as "HMC + pivot moves". This strengthens the reviewer's point.
8. **R1-7 ("Syed et al.'s §7.2 robustness result assumes correct stationary rung marginals").** §7.2 does not state this assumption explicitly. The logical point stands, however: the swap-rejection estimator targets the rung marginals the replicas actually have. The note states it as a caveat of that kind, not as an assumption of [T2-1].
9. **R2-10 (ii) ("unexplained inconsistency" with T5's ≥ 396 nats).** This is not an inconsistency. Both are lower bounds on range(E): T5 uses the spread of local minima, and T2 now uses a prior draw against the polished minimum for the *full* energy (3.1×10³ nats at L=45). The larger valid bound is the better one, and both make α vacuous. The reviewer's underlying point, that v1 bounded range(V) rather than range(E), is accepted and fixed.
10. **R2-15 ("~2.6×10⁵ cells per residue").** ExactPrior's grid is 360 (θ, 0.5°) × 360 (τ, 1°) = 1.3×10⁵ cells per residue. The cost statement uses 1.3×10⁵.
11. **R2-4 (T3's t_C placeholder 0.2 ms vs T2's 0.59 ms at L=45).** Reconciled. 0.59 ms is pilot wall-clock including sampler overhead. The overhead-corrected value is 0.30 ms, and T3's placeholder lies within 0.66–1.3× of T2's corrected values at L = 45–150.
12. **R1-16 (Dürr–Høyer constant 22.5).** Included only as a sensitivity. The verified abstract of [C56] gives O(c√N) without the constant, and the body was not read in this revision.

---

## 9. Review log

R1 = first skeptic (21 objections, verdict FIXABLE); R2 = second skeptic (16 objections, verdict FIXABLE). "Accepted" means the fix was made as proposed or equivalently. "Partly" means see §8.

| ID | Location (v1) | Objection (short) | Resolution |
|---|---|---|---|
| R1-1 | §0.4; S4; §4.1; C4 | Round-trip prediction ignored the initial transit (O(N), not O(1)); true ELE prediction ≈ 9.8/4.8/0/0/0; Poisson P(0) wrong | **Accepted (partly on the P(0) figure, §8.1).** C4 now simulates the DEO index process from the production start with the production counting rule (20,000 replicates): 9.8 ± 2.6, 4.8 ± 1.9, ≈ 0 at L ≥ 100. P(0) ≈ 5×10⁻⁵ and 3.7×10⁻³. §0.4, S4, §4.1 and the C4 notes rewritten |
| R1-2 | §4.1(b); §0.6; §0.7(a) | B_PT bound was transit-free; no information at L ≥ 100; "one RT per sample" not a bound | **Accepted (own model values, §8.2).** Transit-aware 95% bound 2.4×10⁴ / 2.0×10⁴ (model named). ELE floor 6.0×10⁴ / 6.0×10⁴ / 1.0×10⁵ at L ≥ 100. "One RT per sample" labelled INFERENCE. Order-of-magnitude comparisons recomputed (≥ 5–6.5 orders to the most optimistic B\*) |
| R1-3 | §3.6; S6; §4.3; C6; §0.6 | N_walk ≈ K·ℓ·δ_*^{-1/2} overstated cost; the bottleneck enters ~2 stages | **Accepted (normalisation, §8.3).** n_b defined (§3.2), measured in C3 (1.01–1.22), n_b ∈ {1, 2, glassy, ℓ} tabulated. C6 heading fixed. Kill rule re-examined (see R2-4) |
| R1-4 | §0.7 | "7 or more orders short of break-even" drew a conclusion from a lower bound | **Accepted.** Replaced by "break-even needs B_best ≥ B\*; the pilot neither establishes nor excludes this; D4/D5 decide" (§0.7, §4.3) |
| R1-5 | §0.3; S3(d); Prop. 3.3; §3.6 (I-3) | Only δ ≤ 2e^{−ΔF‡} derived; halving rigorous in δ, not in ΔF‡; ln C dropped | **Accepted.** Halving stated in δ (DERIVED). A-Arr added (INFERENCE; a ≈ 1.10, ln C ≈ 5.4 from C3). (I-3) written as ln τ_* > 2 ln(AρK n_b R), with ΔF‡\* = (ln B\* − ln C)/a as a sensitivity. ln B\* reported directly |
| R1-6 | S1(b); Lemma 1(5) | Robust estimator not used; ℓ estimators differ 3.4× at L=150; B\* ∝ ℓ²; CS "bound" invalid | **Accepted.** Both estimators reported as a range (S1b, §4.1). B\* ∝ n_b² ≤ ℓ² stated. CS values relabelled "pilot estimate of the bound (biased low)" |
| R1-7 | S3(a); §3.3(iv); S4 | "Swap statistics cannot detect a first-order bottleneck" overstated | **Accepted (caveat wording, §8.8).** Restated in S3(a) and §3.3(iv): continuum Λ is blind; a coarse fixed grid shows r_k → 1; a fine grid shows an O(1) bump; the pilot profile is uninformative because F is unpopulated; pilot Λ and E(P_N) suspect under non-stationarity |
| R1-8 | §3.3 Lemma 2; consequence (i) | "Exactly" neglects fluctuations; consequence (i) used the second-order formula across the jump | **Accepted.** 1 + O(s/ΔV) and ≤ π + O(s/ΔV) with a subadditivity argument. Consequence (i) replaced by the exact two-point calculation (one intermediate rung, ≤ 2 stages; C1, C3) |
| R1-9 | §3.4 item 2; S3(d) | w undefined; step to e^{−ΔF‡(λ_c)} not shown; "so" non-sequitur | **Accepted.** h defined, BC ≈ 2e^{−hΔV/2} (checked against C3). Separating-set argument written out, plus the exponential-family bound π_{λ_s}(I) ≤ e^{−ΔF‡(λ_c)} under A-mono. S3(d) now cites Prop. 3 item 2 |
| R1-10 | §2.4 A-G | Itemised count gives g ≈ 9×10³–4.2×10⁴, not 5×10³–3×10⁴ | **Accepted.** A-G superseded by T3's G(L). The v1 inconsistency is recorded in the A-G row |
| R1-11 | §7 gap 7 | Pivot moves are Θ(L²) even classically; "lower G by ~L" wrong for the current move set | **Accepted.** Gap 7 rewritten; O2/O1 note that torsion moves are Θ(L²). O(L) only for crankshaft/Cartesian moves (T3-D3) |
| R1-12 | S6 corollary; §0.6 | ρ is a cost, not a time; T\* formulas and t_T exponent wrong for ρ ≠ 1 | **Accepted.** T\*_C = Aρ²(Kn_bGt_T)²/c and T\*_Q = Aρ(Kn_bGt_T)²/c separated. t_T ≤ √(T_budget·c/(Aρ))/(K n_b G) |
| R1-13 | S6 (I-4) bullet | B\* falls by (σ/ε)² (1–2 orders), so v1's "too little to change" was wrong; task wall-clock invariant | **Accepted.** S6 (I-4) bullet rewritten, with the exact invariance of the task wall-clock |
| R1-14 | §4.1; C6 c_meas | c(L) measured two ways; "conservative for quantum" ambiguous | **Accepted (method, §8.5).** Uniform overhead correction (A-c). Loaded-machine benchmark reported as unusable. "Smaller c raises B\* ∝ c⁻²" wording used |
| R1-15 | A-K; §4.3; §3.2 | Stated K formula gives ≈ 750; K = 10 is below (1/p)log(1/p); log² origin unexplained | **Accepted.** A-K states K ≈ 700 and marks K ∈ {10, 100} as assuming improved constants. K = 10³ added to C6/§4.3. §3.2 accounts for one log and states that the second is inherited from [A7]/[A31] |
| R1-16 | S6/§3.6 (I-5); §4.2 | π/2 not π/4; unknown target needs minimum finding; floor-censored targets unresolved | **Accepted (constant as a sensitivity, §8.12).** π/2 used. Dürr–Høyer [C56] ≈ 200× factor added as a sensitivity. Floor-censored targets reported as unresolved (§4.2) |
| R1-17 | S2 INFERENCE | Bound used range(V), not range(U_0+V) | **Accepted.** New rigorous full-energy bound βΔ ≥ E₀[E_pair] − E_polished (E_prior ≥ 0), computed in C4 |
| R1-18 | S1(c); A-rev | Warm start needs χ², not BC; Szegedy Θ(√δ) needs the absolute gap or laziness | **Accepted.** Exact χ² identity added (Lemma 1.1, C2), with the annealing cost using ½ln(1+χ²). C3 shows χ² huge across the jump. A-rev requires the absolute gap or a lazy chain |
| R1-19 | Notation; S3(c); §3.1(4); §3.5; S3(e) | Symbol clashes (K, L, λ_2); BBBV k-marked reduction missing | **Accepted.** n_loc, H, μ_2 introduced. T3 designs prefixed "T3-". Blocking reduction added (§3.7) |
| R1-20 | §4.2; §0.6; script | Census moved on (L=100 now 8 targets); script crashes under cp1252 | **Accepted.** Census rerun (now 16 targets at L=100 and 7 at L=120), with snapshot caveat and floor counts. Script reconfigures stdout to UTF-8 and prints ASCII only |
| R1-21 | S5 item 2 | Resampling is not forbidden by no-cloning | **Accepted** (merged with R2-2) |
| R2-1 | §0.7; S1 claim line; L2 definition | "Advantage at L2" read as relative-to-best | **Accepted.** L1–L3 redefined as same-chain; L4+ relative-to-best. Every verdict gives both levels: same-chain L2 (L3 with T3), relative-to-best L0 everywhere, provably negative where a polynomial bypass exists. S1–S3 claim lines updated |
| R2-2 | S5.2; §3.4(4); §6; gap 4 | SMC is quantisable (seed-coherent Montanaro / amplitude amplification); no-cloning mechanism wrong; [A31 §5] misapplied | **Accepted (A_q ≈ O_rev, §8.6).** S5.2 rewritten. §3.4(4), S3(c), §6 and gap 4 reframed (within-lineage mixing; garbage-free output) |
| R2-3 | S4; §4.1(a); §0.4; C4 note | Significance overstated; transit; n_expl ≈ 1 ≪ d; stationarity violated; "lies in the fixed-λ gaps" too strong | **Accepted, and verified (§8.7).** Transit-aware simulation (R1-1). "Significant at L=45 (one crop, one seed), marginal at L=60". Deficit attributed jointly to A1 and A2. Fixed-λ-gap reading demoted to HYPOTHESIS. [T2-1 §7.2] range verified from the PDF. HMC-only pilot documented |
| R2-4 | S7 kill rule (b); §4.3; §3.6; C6 | Most optimistic B\* not most optimistic (ℓ vs ℓ_eff; T3's D3 G(L)); kill threshold margin wrong; t_C reconciliation | **Accepted (§8.3, §8.11).** n_b (R1-3). T3's G(L) for T3-D2 gen/cen and T3-D3 gen used via the T3 script, with D3 caveats. Most optimistic B\* now 1.0×10¹⁰ (T3-D3, L=150). Kill threshold lowered to 10⁹ (≥ 1 order below any-target B\*_min, ≥ 2 below A80). t_C reconciled (A-c) |
| R2-5 | §0.7; §4.1(b) | Lower bound used as an estimate ("7 orders short") | **Accepted** (with R1-4). The verdict is split into the robust T\*_Q corollary and the undetermined B_best vs B\* question |
| R2-6 | S1(a)/§3.2; S3(c); S7 D4; kill rule (a) | QSA needs a certified lower bound on δ; silent failure on both sides; extrapolation not pre-registered; "polynomial cost" not operational | **Accepted.** A-δ added (S1a, §2.4, gap 10). D2 carries a pre-registered extrapolation model. D4 notes that it yields only lower bounds on τ_*. Kill rule (a) now numeric (≤ 10⁹ local steps per round trip, ≥ ½ transit-aware ELE rate) |
| R2-7 | §0.5; S5.1 | Nested sampling missing | **Accepted.** Added to S5.1, D5(g) and §0.5, with [B67] and newly verified [T2-14] (arXiv 1603.02516) and [T2-15] (arXiv 0906.3544). Abstracts checked via the arXiv API; the quoted phrases are verbatim |
| R2-8 | §0.5; S5.2 | Quantum-enhanced MCMC [A47] counterclaim ignored | **Accepted.** Sentence added (S5.2, §0.5): heuristic small-n fits for diagonal Ising costs [A47, A52, A54], disputed [A48], killed M7. "At most √" restricted to provable guarantees |
| R2-9 | §2.4 A-G; gap 7 | A-G superseded by T3; gap 7 wrong both ways; [A56] range misattributed; qubits ignored | **Accepted.** A-G points to T3's G(L). Gap 7 corrected (R1-11). [A56] SK vs LABS ranges separated (per T3). Logical/physical-qubit column added to §4.3, with a ρ = 1 caveat |
| R2-10 | S2; §0.2 | "only" → "first"; βΔ bounded range(V) not range(E); T5 inconsistency; level mixing | **Accepted (T5 point clarified, §8.9).** "First (and the only one in the verified bibliography)". Full-energy bound (R1-17). [A45] labelled "L1 for its family, L0 for A80". S3(e) tagged NO-GO |
| R2-11 | §5.1 row A8/C74 | Citation conflation | **Accepted.** Rows split. The author lists were checked against the arXiv API in this revision: 0804.1571 has Somma, Boixo, Barnum, Knill (PRL); 0712.1008 has Somma, Boixo, Barnum (preprint) |
| R2-12 | S3(f)(ii); §3.5; [T2-6] | Altshuler–Krovi–Roland contested (Choi 2011) | **Accepted.** [T2-6] qualified. [T2-16] Choi (arXiv 1010.1221, QIC 11, 638) added after verifying its abstract. The "not a route to π_1" conclusion is noted as independent of it |
| R2-13 | S6 burn-in bullet | 1.5× amortisation claim contradicted by the pilot; transients are weak evidence for a small stationary gap | **Accepted.** Restricted to stationary NRPT. The τ_rel ≥ t_burn/[½ln(1/π(x_0)) + ln(1/(2ε))] caveat added. D4 measures from stationary starts |
| R2-14 | §0.6; S6; A-chain | "A = 1" also assumes κ_chain = 1 | **Accepted.** "A = 1 (no classical bypass and κ_chain = 1; both quantum-favourable)" everywhere. Lever-arm caveat added to A-chain |
| R2-15 | S1(d); O2; §2.1 | Generic amplitude loading at b = 8–20 is prohibitive; ExactPrior not exact | **Accepted (cell count corrected, §8.10).** |π_0⟩ costed at the native table (1.3×10⁵ cells per residue, QROM loading ≈ one walk step in total). "Exact up to grid discretisation" with the error orders stated |
| R2-16 | S1(c) | Annealing conflated with AIS/SMC | **Accepted.** The Σ τ_i bound (with χ²) is kept for annealing only. AIS/SMC costs are attributed to weight variance and local mixing [E75, T2-12, T2-13] |
