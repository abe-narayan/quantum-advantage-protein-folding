# Quantum primitives: what is actually known

_Literature phase, 2026-09-26. Citation keys such as [A44], [B46], [C64], [D·], [E33] and [F66] resolve in `BIBLIOGRAPHY.md`; the letter is the search domain (A sampling, B estimation, C optimisation, D quantum-folding literature, E protein/classical, F advantage claims). Every key was verified against a primary page during this session. **I(prog)** marks this program's own reasoning or arithmetic. It is never a literature claim. Claim labels follow the charter's list (`LITERATURE_REVIEW.md` §1)._

For each primitive: the operation, the exact known speedup and its type, the assumptions and oracle, the strongest classical competitor, whether the advantage survives, fault-tolerance and resource figures, protein mapping, and verdict. The full 16-question analyses are in the domain notes summarised here. See `LITERATURE_REVIEW.md` §9 for provenance.

---

## 1. Sampling primitives (Markov-chain acceleration)

### 1.1 Szegedy quantum walk / quantised Metropolis
- **Operation.** W(P) is a product of reflections built from √P(x,y). Its phase gap is Θ(√δ), where δ is the spectral gap of a reversible chain P [A1, A28]. Phase estimation on W gives an approximate reflection about |π⟩ [A2].
- **Known speedup.**
  - Hitting and detection: 1/√(δε) vs 1/(δε) [A1, A3, A4]. Labels: QUERY-COMPLEXITY SPEEDUP, ORACLE-MODEL.
  - Mixing from a cold start: **not** generically 1/√δ. The known generic cost is O(√δ⁻¹·√N), where N is the state-space size [A9]. The quadratic mixing gain is proven only for special chains or distributions [A5, A6, A10].
  - General qsampling of a stationary distribution would imply SZK ⊆ BQP [A11].
- **Classical competitors.**
  - Classical lifted and nonreversible chains already achieve up to a square-root mixing gain on some chains [A14, A15].
  - "For every quantum walk there is a (classical) lifted Markov chain with faster mixing time" in the graph-mixing sense [A18]. Mixing speedups "are not necessarily diagnostic of quantum effects" [A16].
  - Quantum walks are at most polynomially faster on general graphs [A12].
- **Oracle.** Coherent evaluation of ΔE for proposed moves, plus the Metropolis rotation. A Boltzmann coin for local Ising models costs O(N log 1/ε) T gates, and the cost is exponential in locality [A55].
- **FT resources.** Walk steps cost 2×10⁴–4.6×10⁶ Toffolis on SK/LABS instances [A56]. Crossover for SK at N=512 is about 1 year of quantum runtime [A56]. Matching a specialised classical MCMC machine at a quadratic speedup needs roughly 1 ns logical gates [A55].
- **Protein mapping.** Direct, for a Metropolis or PT chain over residue or torsion moves on a learned energy (SP-1). The only published protein use is QFold, which has ≤1,024 states and a precomputed energy table [A65; see `QUANTUM_ADVANTAGE_CLAIMS.md`].
- **Verdict. INTERESTING as a theory and resource-estimate target; WEAK as a practical route.**

### 1.2 Quantum simulated annealing (QSA) and adaptive QSA
- **Operation.** Walk-based transport |π_β0⟩ → |π_βL⟩ along an inverse-temperature schedule [A8, A7, A34].
- **Known speedup.** O(1/√δ) vs O(1/δ) steps, where δ is the minimum gap along the schedule [A8]. There is a quadratic gap improvement with adaptive schedules, explicitly framed for **Bayesian inference** [A31]. Labels: THEORETICAL, ASYMPTOTIC (in walk steps).
- **Assumptions.** Consecutive Gibbs states overlap by a constant; the gap is known or bounded; the chain is reversible. Each measured sample needs a fresh anneal (no-cloning; I(prog)).
- **Classical competitors.** PT/REMD, adaptive SMC, and the improved classical cooling schedules that appeared in the *same* paper as the quantum result [A32].
- **FT resources.** "Roughly a day and a million physical qubits to optimize spin glasses that could be solved by classical simulated annealing in about four CPU-minutes" [A56 = C64 = F67].
- **Protein mapping.** Annealing toward the learned-energy posterior. Few samples are needed (the S33 soft readout used tens), which is favourable to QSA's per-sample cost (I(prog)).
- **Verdict. INTERESTING (conditional); WEAK in wall-clock.**

### 1.3 Continuous-space quantum samplers (QSVT / Witten-Laplacian / quantum Langevin / quantum replica exchange)
- **Operation.** Encodes √σ with σ ∝ e^{−βV} as the kernel of an operator derived from the Witten Laplacian, extracted by singular-value thresholding [A44]. Alternatives are quantum MALA [A39], stochastic-gradient QSA [A41], and Fokker–Planck solvers [A42].
- **Known speedup.**
  - Õ(√(β d C_PI)) for Langevin. Replica-exchange Langevin costs √(β d/Gap), which is "the first quantum algorithm that accelerates replica exchange Langevin diffusion" [A44]. That paper's "up to quartic" is relative to MALA's Cheeger bound; against the Poincaré scaling it is quadratic [A44].
  - **The first provable continuous-domain separation:** every classical algorithm querying values, gradients or higher derivatives needs Ω(α) queries, while the quantum algorithm needs Õ(√α), with α = e^{βΔ} [A45]. It is quadratic, on hide-and-seek narrow-well instances on the torus.
  - Log-concave targets: Õ(κ^{1/2}d) [A39] and Õ(√κ d) with local structure [A40]. Folding posteriors are not log-concave.
  - Labels: QUERY-COMPLEXITY SPEEDUP, THEORETICAL. [A45] is provable in its query model.
- **Assumptions.** A warm start |⟨φ|σ⟩| = Ω(1) [A44], or annealing to supply one [A45]; smoothness; discretised grids. C_PI grows as exp(βΓ) with barrier height Γ [A44]. The quantum gain is the square root of that exponential; it does not remove it.
- **Oracle.** A coherent gradient or value oracle for V. No paper costs one for a molecular or learned energy (gap G-2).
- **Protein mapping.** **The best formal match to SP-1**: a continuous non-convex energy, with a quantised version of the strongest classical sampler family (replica exchange).
- **Verdict. INTERESTING, the top theory line in the sampling domain. Not HIGH PRIORITY:** the gain is quadratic, measured in queries, assumes a warm start, and has no gate costs.

### 1.4 Beyond-quadratic walk claims
- **Fully-quantum walks.** A "sixth-degree polynomial queries speedup" and a crossover of under a day [A46]. The classical exponents are fitted on **exact n=3…10** SK transition matrices, the baselines are local and uniform Metropolis (no PT), and the gate times are optimistic (20 ns). Labels: SIMULATOR RESULT, HEURISTIC ADVANTAGE. **WEAK.**
- **Nonreversible-chain quantum speedup.** "Up-to-exponential" relative to the chain's own mixing time, under a condition the authors could not provide a general way to check. The motivation mentions MD, but "no concrete MD simulation results" are given [A43]. **WEAK.**
- **Quantum-enhanced MCMC (QeMCMC, NISQ).**
  - Original result: δ ∝ 2^{−kn}, fitted for 3 ≤ n ≤ 10 against local and uniform proposals, with a "roughly cubic/quartic" enhancement [A47].
  - There is no speedup on worst-case unstructured problems [A48]. The gap is bounded by the inverse participation ratio, with no advantage for ergodic quenches [A49].
  - Tensor-network (classical) proposals retain the scaling advantage [A50].
  - Labels: ADVANTAGE DISPUTED. **KILLED for protein structure.** It needs diagonal register encodings, which failed condition C in S29–S33 (DNR-08).

### 1.5 Quantum Metropolis and quantum Gibbs samplers
- These target *quantum* Hamiltonians, where the classical difficulty is the sign problem [A19, A20, A24–A27].
- The original quantum Metropolis proof relies on a "boosted and shift-invariant version of QPE which may not exist" [A23].
- For a **diagonal** (classical) protein energy there is no sign problem. The sampler reduces to classical Metropolis plus at most the walk speedup of §1.1 (I(prog)).
- The brute-force variants cost Õ(√(Nβ/Z)) [A22] or D^α [A21], which is exponential in the number of degrees of freedom.
- **KILLED as a distinct source of advantage for protein energies.**

### 1.6 Quantum rejection sampling (prior → posterior)
- **Speedup.** Quadratic in 1/P_acc [A36, A37]. Labels: QUERY-COMPLEXITY, ORACLE-MODEL.
- **Obstacle.** It needs a **coherent** circuit that prepares the prior. For a learned structural prior this means running the whole decoder (neural network plus iterative L-BFGS / distance geometry) reversibly in superposition (I(prog)).
- **Classical competitor.** SMC and importance sampling with MCMC rejuvenation are not plain rejection sampling [E74, E75]; learned samplers with reweighting also compete [A78].
- **WEAK.**

### 1.7 Quantum annealers as Boltzmann samplers
- The effective temperature is instance-dependent [A62]. Annealers are "noisy Gibbs samplers" with "spurious interactions absent from the hardware specification" [A63]. They sample at a quasistatic freeze-out [A61].
- Classical QMC reproduces the tunnelling scaling [A64].
- **KILLED.**

---

## 2. Estimation primitives

### 2.1 Amplitude estimation / quantum mean estimation
- **Speedup.** Õ(σ/ε) vs Θ(σ²/ε²) queries. This is tight: quantum Ω(1/ε), classical Ω(σ²/ε²) black-box [B1, B12, B16, B19, B29]. The "near-quadratic speedup over the best possible classical algorithm" holds for bounded-variance subroutines [B12 = A30]. Labels: QUERY-COMPLEXITY SPEEDUP.
- **Classical competitors.**
  - Quasi-Monte Carlo reaches a near-quadratic rate on smooth, low-effective-dimension integrands [B51, B68].
  - MLMC [B20].
  - MBAR is the minimum-variance equilibrium estimator [B60].
  - Monte Carlo averaging is embarrassingly parallel [B46].
- **State preparation.** Grover–Rudolph loading erases the speedup, and this is a theorem [B37]. Conformational Boltzmann laws lack the integrable marginals that loading needs [B36]. The only principled route is quantum-walk qsampling (§1), so AE on proteins inherits the walk problem (I(prog)).
- **FT calibration.**
  - Derivative pricing, a far simpler oracle, needs 8k logical qubits and T-depth 5.4×10⁷. It is advantageous only at a 10–50 MHz logical T-rate, against ~10 kHz projected [B43, B44].
  - The QSP variant needs 4.7k logical qubits and 10⁹ T gates at 45 MHz [B45].
- **Protein relevance.** Biomolecular estimates are limited by force-field bias (RMS 1–2 kcal/mol) and by barrier-limited sampling. Statistical precision of ≤0.1 kcal/mol is already routine [B71]. The quadratic gain acts on the wrong factor.
- **Verdict. KILLED in practice; WEAK in theory.** See `CLASSICAL_COUNTERARGUMENTS.md` CA-4 for the calibrated crossover.

### 2.2 Quantum partition-function estimation
- **Speedup.** Classical Õ(log|Ω|/(ε²δ)) vs quantum Õ(log|Ω|/(ε√δ)) [B26, B27], then Õ(log^{3/4}|Ω|/(ε√δ)) [B28 = Cornelissen–Hamoudi]. The lower bound is Ω(1/ε) reflections [B29]. Labels: THEORETICAL, ORACLE-MODEL.
- **Classical competitors.**
  - AIS, SMC, Wang–Landau, nested sampling [B64–B67].
  - For rotamer spaces, deterministic bounded enumeration (K*/BBK*, CFN counting [B75, B76]). These are not MCMC, so the δ-premise of the quantum algorithms does not describe them.
- **Verdict. WEAK (conditional).** Its only payoff is the √δ factor, which makes it a sub-case of mixing acceleration (§1). It is gated by the unmeasured δ(L).

### 2.3 Quantum free-energy algorithms (Liouvillian / Koopman–von Neumann dynamics)
- These target *electronic-structure accuracy* of forces in alchemical free energies, compared only with prior quantum algorithms, with no concrete resource counts [B53, B54]. Hardware "quantum-centric" versions claim no speedup [B55, B56].
- **WEAK, out of structure scope.**

### 2.4 NISQ / low-depth / variational amplitude estimation
- With depth D the gain is ≤ about D-fold [B6]. Hardware error "saturates due to the noise" [B11]. Variational QAE "typically [has] larger computational requirements than classical MC" [B7].
- **KILLED.**

---

## 3. Optimisation and search primitives

### 3.1 Grover / amplitude amplification / minimum finding
- Θ(√N) queries is optimal [C54–C56]. Relative to an oracle, NP search cannot be done in o(2^{n/2}) quantum time [C55].
- Quadratic speedups "will not enable quantum advantage on early generations" of fault-tolerant hardware [C65 = A57 = B46 = F66].
- Protein subproblems are structured, so exhaustive search is never the baseline.
- Amplitude-amplified decoder restarts would save at most about √64 = 8× at the measured saturation point. Each call would need a reversible continuous optimiser (I(prog), [C64]).
- **KILLED as a protein lever.**

### 3.2 Quantum backtracking / branch-and-bound
- Costs: O(√T n^{3/2} log n) [C57]; early-stopping variants [C58, C59]; near-quadratic B&B [C60, C61]; DP-type O*(1.817^n) vs O*(2^n) [C62].
- The speedup is **relative to the same classical tree**. Exact classical rotamer and lattice solvers (cost-function networks [C82], tree decomposition [C83], CPSP [C85]) shrink that tree.
- The CSP-specific fault-tolerant estimate finds the 10³–10⁵ advantage "disappears" once decoder costs are included [C63].
- **WEAK (conditional, low prior).**

### 3.3 QAOA / QAOA+ (shallow, NISQ)
- Locality and overlap-gap limits [C12, C13, C15, C16]. Symmetry protection [C9]. Local classical algorithms match it [C8, C10, C11]. A noise barrier [C25, C26]. The required sample count grows exponentially for p ≤ 11 [C19].
- **KILLED.**

### 3.4 High-depth QAOA + quantum minimum finding (LABS)
- Time-to-solution: 1.21^N with minimum finding vs memetic tabu search 1.34^N. QAOA alone gives 1.46^N. Noiseless simulation at N ≤ 40 [C28].
- The gain comes from a Grover layer that the classical heuristic could also receive, giving about 1.16^N (I(agent-C) arithmetic).
- **WEAK. No protein mapping.**

### 3.5 VQE / CVaR-VQE / ADAPT on classical costs
- Compared only against quantum baselines [C3, C4, C6]. Barren plateaus [C20, C21]. NP-hard training [C23]. Landscapes swamped with traps [C24]. Where barren plateaus are provably absent, the model is often classically simulable [C22 = F37].
- **KILLED.** This is the family S29–S33 already tested (33 experiments, null).

### 3.6 Quantum annealing (including QAC and counterdiabatic variants)
- Twelve years of claims show the same pattern: an advantage over SA dissolves against SQA, cluster methods, exact solvers or SBM [C38–C43, C52].
- The strongest current claim is scaling in approximate optimisation over PT-ICM at a gap ≥1% [C44]. It is directly contested by simulated bifurcation [C45] and a runtime re-analysis [C46].
- **KILLED for protein search.**

### 3.7 Super-quadratic structured primitives
- Short-path / super-Grover: 2^{(0.5−c)n} with small c [C69, C70].
- Kikuchi planted inference: nearly quartic [C71, C72].
- DQI: superpolynomial for OPI [C73].
- All need planted or algebraic structure. The planted regime ("information present but classically hard to extract") is the **opposite** of the program's measured information-limited regime (I(prog)).
- **INTERESTING as theory; WEAK for the program.**

---

## 4. Linear-algebra, Hamiltonian and generative primitives

### 4.1 Hamiltonian simulation + phase estimation (electronic structure)
- **Algorithms.** Qubitisation costs O(λt + log(1/ε)) queries [F45]. QSP/QSVT [F46–F48]. Tensor-hypercontraction (THC) block encodings [F61].
- **Resources.**
  - FeMoco: ~10¹⁵ T gates [F58], or ~4 M physical qubits and under 4 days with THC [F61].
  - Cytochrome P450 compound I: ~4.6 M physical qubits and 73 h [F62].
- **No evidence of generic exponential advantage** for ground-state chemistry; the state-preparation overlap is the crux [F64]. The FeMoco model was classically solved to chemical accuracy in a 2026 preprint [F65].
- **Protein relevance.** It addresses metal-site chemistry, not backbone structure. S29–S33 measured that energy accuracy is not the structure bottleneck (DE-7). ML potentials reach ab-initio quality for proteins [F73, F74].
- **KILLED as a structure-accuracy lever; INTERESTING only for metalloprotein active-site chemistry (out of scope).**

### 4.2 QSVT / HHL linear algebra
- The caveats of [F51] apply. Dequantisation holds for low rank [F52–F54] and for constant precision [F55]. Active QRAM erases most of the asymptotic advantage [F56]. The program's convex programs have D ≤ 500 and solve in milliseconds.
- **KILLED.** QSVT survives only as the language of other algorithms (§1.3).

### 4.3 QITE / imaginary-time evolution
- For diagonal energies, imaginary-time evolution is classical Boltzmann reweighting [F49].
- **KILLED.**

### 4.4 Quantum generative models (QCBM, QBM, IQP, spectral Born machines)
- **What is proven.** An expressivity separation against Bayesian networks only [F78], and a DDH-conditional learnability separation on contrived distributions [F79].
- **Barriers.**
  - Hard-to-sample (anticoncentrating) models are untrainable on average [F91].
  - Trainable IQP models admit classical surrogates [F88–F90].
  - Classical models outperform quantum ones in systematic benchmarks [F81].
- **The key mismatch for this program.** Born-rule hardness is the hardness of sampling the model's *own* |ψ|². It gives no advantage for sampling a *specified* classical posterior π ∝ e^{−E/T}. That task belongs to §1, not to generative modelling.
- **KILLED as a prior; WEAK as a sampler.**

### 4.5 NISQ dynamics / utility / OTOC
- IBM's 2023 utility claim was reproduced classically [F19–F21, F23]. D-Wave's 2025 claim is contested [F27, F28] with a reply [F29]. Google's 2025 OTOC(2) result stands so far [F30] but has no protein mapping. The molecular-geometry NMR companion is self-declared "not yet beyond classical" [F34].
- With constant noise, efficient error mitigation implies classical simulability on most inputs [F35].
- **KILLED for structure.**

---

## 5. Summary

| Primitive | Speedup type | Size | Verdict |
|---|---|---|---|
| Szegedy / QSA walk sampling | query, in the gap | quadratic (warm path); √N penalty otherwise | INTERESTING (theory) / WEAK (practical) |
| Continuous QSVT / quantum RELD samplers | query, provable on hide-and-seek instances | quadratic in e^{βΔ} or C_PI | **INTERESTING, the top theory line** |
| Beyond-quadratic walks, nonreversible speedup | empirical at n ≤ 10 / conditional | claimed 6th-degree / exponential | WEAK |
| QeMCMC (NISQ) | empirical, disputed | — | KILLED (protein) |
| Quantum Metropolis / Gibbs on classical energies | reduces to walks | — | KILLED (distinct) |
| Rejection sampling | query | quadratic in 1/P_acc | WEAK |
| Amplitude estimation | query, tight | quadratic in 1/ε | KILLED (practical) |
| Partition-function algorithms | query | quadratic in ε and δ | WEAK (reduces to √δ) |
| Grover / minimum finding | query, optimal | quadratic | KILLED |
| Backtracking / B&B | query vs the same tree | near-quadratic | WEAK |
| QAOA shallow / VQE / CVaR / ADAPT | none | — | KILLED |
| High-depth QAOA+QMF | simulated fit, N ≤ 40 | 1.21^N vs 1.34^N | WEAK |
| Annealing | disputed empirical | — | KILLED (protein) |
| Super-quadratic planted / structured | theory | up to quartic | INTERESTING theory / WEAK here |
| Hamiltonian simulation + QPE | FT time | polynomial vs heuristics | KILLED (structure) / INTERESTING (metal chemistry) |
| QSVT/HHL, QITE, generative, NISQ dynamics | dequantised / reduces / surrogate | — | KILLED |

**I(prog).** Every surviving primitive offers **at most a quadratic** speedup in a gap, barrier amplitude or precision parameter, in the query model, on fault-tolerant hardware. The one family that is both formally matched to a protein task and provably separated (§1.3) is a *sampling* primitive. It is relevant only if the classical sampler for that task is shown to be slow.
