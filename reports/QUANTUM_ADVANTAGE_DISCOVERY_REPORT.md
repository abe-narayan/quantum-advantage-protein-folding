# Quantum Advantage Discovery Report: protein structure computation

_quantum-advantage-protein-folding, discovery sprint of 2026-09-26 to 2026-09-28 (four rounds: discovery attack, R1 attack, round 3, round 4). Every statement's evidence class is in `reports/QUANTUM_ADVANTAGE_CLAIM_AUDIT.md`. Pre-registrations and deviations are in `research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`. Round syntheses: `research/discovery/`, `research/experiments/ADVERSARIAL/R1_SYNTHESIS.md`, `research/experiments/ROUND3/SYNTHESIS.md`, `research/experiments/ROUND4/SYNTHESIS.md` (each with a completeness critic)._

---

## 1. Executive summary

**No quantum advantage for protein-structure computation survives in any regime this program examined** (claim categories 1–6; practical level L0 everywhere). The statement is scoped and falsifiable, not a theorem.

**Scale of the search.**
- Rounds and workflows:
  - 28 discovery mechanisms, attacked from 3 independent lenses each;
  - a 7-lens attack on the only lead with a measured classical failure (NMR echoes);
  - round 3, with 9 lanes and ~30 new mechanisms;
  - round 4, with 5 lanes, including a pro-quantum red team against the program's own kills.
- Evidence types: exact simulations, pre-registered experiments on a leakage-screened 30–150-residue ladder, and derived fault-tolerant resource models.
- Record: 20 new kills (K-101 to K-120), each with a reopen condition.

**Why it fails: three classes, none leaving room for a quantum advantage** (INFERENCE from MEASURED and DERIVED parts):
1. **Structure-bearing and classically easy.**
   - Learned-energy structure prediction: native-free distance-geometry seeding reaches the best basins in a median of ~420 energy evaluations. Against that baseline, any quantum speedup exponent would need logical gates of ~3 ns or faster.
   - Protein ¹H dipolar echoes inside the physical reversal window: computed classically to σ = 0.01 at 40 µs in minutes of CPU.
2. **Possibly classically hard, but structurally uninformative.** Dense-spin echo dynamics beyond ~80 µs lies beyond the site-resolved reversal horizon. The profiled structural gain there stays below 2 even if the whole echo were quantum-only.
3. **Classically expensive and structure-bearing, but no applicable quantum algorithm.** This is physics-based all-atom folding kinetics and ensembles.
   - No super-quadratic algorithm has its preconditions met by a protein force field (Carleman R ≥ 4.3×10³, where R < 1 is needed).
   - Quadratic routes cost ≥ 2.2 years per estimate even at 10 ns logical Toffolis.
   - This is the only examined regime that a *new* s ≥ 3 algorithm could open. A hypothetical s = 4 would take 2.6 h–10 d at 10 ns.

**Two orthogonal closures.**
- **Quantum memory / quantum data** gives exactly 1× per structural parameter. This is a theorem for selective-polarisation ¹H states.
- **Exact electronic structure** hits the QM/MM model floor before the solver floor (FeMoco E4 isomers stay WEAK, chemistry level only).

**Strongest publishable claims:**
- (a) the resource-normalised negative for learned-energy sampling and optimisation: a landscape-independent runtime floor, T3 costing, and the distance-geometry classical twin;
- (b) protein ¹H OTOC(1) echoes are classically computable to σ where they are observable (40 µs; b-aware cluster families + spinDMFT; provisional pending replication) and not useful where they might be hard.

---

## 2. Research question

Is there a computational task that matters to protein structure science where a quantum mechanism changes the scaling or capability in a genuinely non-classical way, against the best classical approach and with full resource accounting? If not, where and why does it fail?

The sprint did not assume VQE, QAOA, sampling or optimisation. It was free to redesign the formulation, representation, objective and architecture. It followed oracle discipline (no free oracles, state preparation, block encodings or native indicators), required a classical adversary first, kept claim levels L0–L6 with theoretical and practical levels separate, and allowed no forced positive.

---

## 3. Starting evidence

- **Predecessor S29–S33** (9–60 aa, all simulated; imported read-only):
  - 33 CVaR-VQE-style experiments on diagonal registers of 7–171 qubits never moved the built-chain endpoint.
  - Equal-tuning simulated annealing and random prior sampling matched or beat them.
  - Twelve reduction results explain why: prefix theorem, solver equivalence, tail collapse, closed-form p*, and others.
  - Single-structure accuracy at ≤ 60 aa is information-limited.
  - One positive signal: a Boltzmann soft average beat hard tails (1.40× MDE), but as an exact enumerated sum.
  - Sources: `research/sprint29-33/`, `research/SCIENTIFIC_MEMORY.md`.
- **Literature phase** (448 verified papers):
  - Every known quantum speedup touching classical-energy protein tasks is at most quadratic, query-model and fault-tolerant.
  - Quadratic speedups fail fault-tolerant break-even (Sanders 2020; Babbush 2021).
  - The only surviving lead was sampling a learned-energy structure posterior at ≥ 60 aa, conditional on an unmeasured classical mixing bottleneck.
  - Source: `research/literature/LITERATURE_REVIEW.md`.

## 4. Literature landscape (condensed)

- **Optimisation and search** (Grover, Dürr–Høyer, QAOA, annealing, backtracking): quadratic at best on black boxes. Classically saturated or exactly solvable on protein structure. Transmission of proxy energies fails.
- **Sampling** (Szegedy/QSA walks, quantum Langevin/QRELD [A44], continuous hide-and-seek separation [A45]): quadratic, needs a warm start and a gap lower bound; the only live line after the literature phase.
- **Estimation** (amplitude estimation): quadratic in precision; biomolecular estimation is limited by bias and mixing, not variance.
- **Hamiltonian simulation of physical quantum systems:** the one family whose target is not a classical objective.
  - The nearest prior art is O'Brien et al., PRX Quantum 2022: dipolar-Hamiltonian learning on ubiquitin spin clusters, learnability tied to loss of ergodicity.
  - Zhang et al. 2025 [F34]: NMR OTOCs of small molecules interpreted on Willow, "not yet beyond classical".
  - Google's OTOC(2) beyond-classical evidence [F30] concerns random circuits.
  - Classical rebuttals: Fratus et al. 2025 (cluster methods for liquid NMR); Elsayed–Fine 2015 (classical spins); Begušić–Chan (sparse Pauli dynamics); Schuster et al. 2025 (noisy circuits are classically easy).
- **Quantum chemistry of metal cofactors** (FeMoco-class QPE): the strongest literature-supported quantum use near proteins. It is outside the structure endpoint.

## 5. Computational bottleneck map

| Bottleneck class | Status for protein structure | Quantum relevance |
|---|---|---|
| Single-structure prediction ≤ 60 aa | information-limited (S29–S33; H-002) | none: more computation does not help |
| Conformational search / decoding | classically saturated (32–64 restarts at 44–60 aa); census unsaturated at L ≥ 100 (MEASURED) | quadratic (Grover/AA) only vs i.i.d. restarts; killed (T4) |
| Posterior sampling of a learned energy | classically hard signals at L ≥ 45 (0 NRPT round trips; unsaturated census) | quadratic same-chain (T2); practical floor T*_Q ≥ 0.26–20 yr/sample (killed) |
| Rare events, committors, free energies | classical splitting/stratification polynomial | quadratic; killed (QM-12/13/15) |
| Inverse problems with physical quantum data (NMR spin dynamics) | classical forward models exact for 2-point transfer; echoes (OTOC) beyond classical approximations at N ≥ 10 (MEASURED) | **the only formulation with a measured classical-approximation failure** |
| Electronic structure of active sites | classical DMRG/CC at chemical accuracy for FeMoco-class ranking (per lens) | polynomial; outside the endpoint |

## 6. Candidate quantum mechanisms

28 unique mechanisms (from 90 lane cards) across five roles: sampler, optimiser, estimator, quantum forward model, structural invariants. Plus meta items (no-gos, costing, dequantisation). Full catalogue: `research/discovery/CANDIDATE_MECHANISMS.md`. Architecture map: `research/discovery/ARCHITECTURE_SEARCH.md`.

## 7. Classical counterarguments

Four structural reasons recur (`research/discovery/CLASSICAL_COUNTERARGUMENTS.md`):
1. **Quadratic ceiling plus a landscape-independent runtime floor** (T2, T5).
2. **White-box pair-additive energies leak their own structure.** Distance-geometry seeding, the e^{−KL} sublevel bound and assignment collapse dequantise the constructions that separations need.
3. **Fold information lives in weak couplings**, which are classically perturbative. The hard sectors carry local or degenerate information.
4. **The endpoint is information-limited**, and new information comes from experiments that already have classical interpreters.

## 8. Architectures explored

- Program A: learned-posterior sampling (λ-path NRPT, temperature exchange, mode census, transmission).
- Program B: synthetic exact-mechanism lab.
- Program C: quantum forward models for NMR, with an adversary panel, Fisher-information split, dephasing and bath embedding, a dilute amide-proton network, a shot-based quantum circuit with hardware noise, and a resource model.
- Theory T1–T6.

See `ARCHITECTURE_SEARCH.md`.

## 9. Experiments performed

Ledger: `research/experiments/README.md`. All heavy jobs ran under the CPU/RAM governor.

| ID | What | Scale |
|---|---|---|
| G1-P / M1 / M1b / M2 / Q4-M3 | NRPT pilot; 256- and 2048-restart mode census; λ-path T-scan; temperature exchange | 16 leakage-screened chains × L = 30–150 |
| R2-T | Laplace-free posterior-mixture transmission test | 16 chains × L = 60, 100 |
| C1 | NMR hardness–identifiability gate (v2) | 1UBQ 6 probes × 2 orientations × γ ∈ {0, 10³, 5×10³} s⁻¹, N = 10 (+12, 14); 1PGA replication |
| C1-HN | dilute amide-proton (perdeuterated) networks | 1PGA, 1UBQ; N = 10, 12; 1 ms window |
| C2/C3 | classical cost scaling (sparse Pauli strings) for transfer and echoes | N = 8–20 |
| R1-E | bath embedding (exact N_env = 12/14; Gaussian-bath dephasing) | 2 probes |
| Q-PoP | shot-based quantum echo circuit, depolarising noise, echo-normalisation mitigation | N = 10, 12 |
| B-SYN | exact mechanism lab | 5 landscape families, n = 6–16 |
| Theory checks | T1–T6 companion scripts | — |
| Round 3 | 9 lanes: QeMCMC exact gaps, DG classical twin, structured-speedup preconditions, exact echo reach, polynomial echo adversaries, DQ echo, 3 new-mechanism lenses; 6 verifiers + critic | `research/experiments/ROUND3/` |
| Round 4 | T-X-early, spinDMFT, all-atom regime, pro-quantum red team, analog simulators; 6 verifiers + critic | `research/experiments/ROUND4/` |

## 10. Negative results

**N1. Sampling or optimising the learned structure energy: no advantage at any accounting (K-101, K-102).** DERIVED + MEASURED
- The landscape-independent floor is T*_Q ≥ 0.26 yr per sample at 1 µs Toffolis, ≥ 1–20 yr on the A80 target, and 10⁵–10⁷ yr at central constants (T2 + T3).
- Measured classical costs: NRPT 0 round trips within 2–4×10⁵ evaluations (a lower bound for one method); multistart ~2×10³–2.5×10⁴ evaluations per hit of the best-found basin.
- Break-even needs ≥ 10¹⁰–10¹¹ evaluations per sample.
- Amplified multistart: p* ≤ 10⁻¹¹ vs measured p_hit ~ 10⁻² (T4).

**N2. 25 further mechanisms killed by theorem, measurement, resource or information arguments** (K-103, `research/discovery/KILLED_DIRECTIONS.md`). Among them:
- QHD (Gaussian homotopy dequantises the known separation family);
- ground-state parents (BCGL fixed-node dominance);
- QLSA committors (barrier exponential conserved);
- Kikuchi on pairwise protein data (arity collapse);
- restraint posteriors (assignment collapse);
- knots (≤ 8 crossings);
- oscillator simulation (Ω(N) loading);
- metal cofactors (outside the structure endpoint);
- sensing (not computation).

**N3. NMR two-point transfer as a quantum forward model: killed (K-104).** MEASURED
- Sparse Pauli dynamics at ε = 1e-4 reproduces transfer exactly at N = 10 on 1UBQ and 1PGA, for dense and amide-only networks at γ = 0 / 10³ / 5×10³ s⁻¹ (f_hard = 0).
- The pre-registered weight-4 adversary (f_hard ≈ 0.99) was too weak; the adversary panel caught it.

**N4. NMR dipolar echo (OTOC(1)) as a quantum forward model for structure (R1): killed (K-105).**
- ε = 3e-5 sparse Pauli (≈ full operator space) and exact simulation (seconds) reproduce the N = 10 echo. Median f_hard over 17 parameters falls from 0.95 to 0.00 once the ε ladder is completed (MEASURED).
- The N = 10 reference is unconverged in cluster size (MEASURED).
- The pre-registered C3 feasibility survival clause failed: the informative window lies at 4.8–25 T2 versus measured reversal horizons T3 ≈ 4–6.7 T2. Transfer of those horizons to proteins is INFERENCE.
- Realistic value: gain ≈ 1.1–1.5 under priors and attenuation (MEASURED on stored Jacobians).
- Break-even vs exact classical simulation needs N_eff ≈ 30–47 at 4–6 h per quantum evaluation (DERIVED).

**N5. Quantum hardware noise (Q-PoP).** MEASURED, simulator only
- Unmitigated echo circuits fail immediately (20 µs) at every noise level ≥ 1e-3 per qubit per Trotter step.
- With echo-normalisation mitigation, a window beyond the (then) classical-approximation failure time exists only at ≤ 1e-3 (≈ 1e-4 per two-qubit gate) and closes at 3e-3.

**N6. Transmission (R2-T).** Classical result, pre-registered (R2-T v2 weightings; 16 chains per length; T* chosen native-free as the smallest temperature with ESS ≥ 3). MEASURED:
- **L = 60.** Energy-weighted soft readout beats the argmin by a median of +0.54 Å (mean +0.67), 1.01 MDE, improving 88% of crops. Hit-weighted: +0.33 Å, 0.61 MDE.
- **L = 100.** The median gain is ≈ 0.00 Å (mean +0.09), 0.00 MDE.
- **Pre-registered kill** (median gain < 1.0 MDE at both lengths): **does not fire**, by a hair at L = 60. The transmission clause of H-006 therefore holds weakly at 60 aa and fails at 100 aa.
- This is classical information about the value of posterior averaging. It cannot rescue the quantum route (K-101 is landscape- and transmission-independent).

**N8. Round 3 (K-106 to K-116; `research/experiments/ROUND3/SYNTHESIS.md`).**
- Quantum-enhanced MCMC: at most quadratic; gap ratio ≤ 12.7 vs ≥ 784 needed.
- Any-exponent speedups on the learned energy: the DG portfolio makes it classically easy.
- Structured super-quadratic families: preconditions absent (e.g. the DQI dual distance is 3).
- Double-quantum echo; GBS contact sampling; methyl-rotor tunnelling; quantum SDP; six derivation-level mechanisms.
- Quantum-memory learning: the gain is exactly 1 per parameter (theorem).
- Active-site FT-QPE for structure: model-floor cap.
- R1-SIM as a resource claim against exact F_N.

**N9. Round 4 (K-117 to K-120; `research/experiments/ROUND4/SYNTHESIS.md`).**
- All-atom force-field sampling: no applicable super-quadratic algorithm; T*_Q,2 ≥ 2.2 yr at 10 ns.
- Analog dipolar simulators: 42–100σ outside the budget.
- R1-SIM-early: the 40 µs echo is classically computable to σ (provisional).
- The hybrid comparator was retired.
- The red team found no false kill, but re-based K-105 (reversal horizon), K-109 (value vs measured reach) and K-111 (resolvability).

**N7. G1 production (pre-registered confirmations).** MEASURED (governed production; pre-registered in PREREG G1/Q4):
- **λ-path NRPT T-scan** (5 crops, T ∈ {1, 2, 4, 8}, HMC + pivots, 1500 s):
  - Round trips appear only at L = 45–60 (1–2 at T ≤ 2; 16–17 at T = 8), which also validates the counter.
  - At L = 80–120 there are **0 round trips at every T**. Λ falls with T (L = 100: 24.8 → 15.4) but stays high.
  - K-G1c (hardness only at T = 1) does not fire at L ≥ 80.
- **Mode census** (256 restarts, 16 chains, L = 30–150):
  - Geometric-mean p_hit(best mode) falls 0.10 → 0.0039 and reaches the 1/256 censoring floor at L = 150.
  - exp(−0.028 L) fits better than a power law (ΔBIC = 10.6; tail censored). Round 3 showed this is **not** a hardness measure: it is confounded by fixed-depth (200-iteration) relaxation, and native-free distance-geometry seeding reaches the census-best basin on 14/16 crops at L = 150 in ~420 evaluations.
  - The 2048-restart census (8 crops) is unsaturated at L = 150 (p_hit ≈ 1/2048).
  - ρ(E, RMSD) over modes is 0.03–0.34.
- **Pre-registered G1 survival requires all criteria**, and it **fails**:
  - super-polynomial p_hit: met descriptively, with a censoring caveat;
  - no bypass: contradicted by native-free distance-geometry seeding, which reaches the census-best basin on 14/16 crops at L = 150 (round 3, replicated);
  - transmission: weak at L = 60, absent at L = 100;
  - extrapolated classical cost > B* at some L ≤ 500: **fails**. p_hit ≈ 2×10⁻⁷ at L = 500 gives ~10⁹ evaluations, below B* ≥ 10¹⁰–10¹¹.
- **The quantum sampling route is killed** by both the pre-registered G1 rule and the landscape-independent floor (K-101).
- **Temperature exchange (Q4)**, 24 crops L = 30–120: 0 round trips everywhere.
  - The heat-capacity maxima sit at the lowest rung (T = 1), a non-equilibrium artefact.
  - Histogram "barriers" are 0.02–4.5, far below 2 ln R ≈ 32–46.
  - **K-Q4c fires: QM-04 killed at this instrument.**

## 11. Positive results

There is no positive quantum-advantage result. The following are measured facts that stand:

**P1. Instruments (MEASURED).**
- A deterministic sector-exact solver for protein ¹H dipolar dynamics, validated to 1e-15 against the dense Heisenberg matrix with and without dephasing, and independently reimplemented to 1e-14.
- A shot-based quantum echo circuit that reproduces the exact echo within 1–2 SE.

**P2. Echoes resist compression (MEASURED).** At N ≤ 16, no sub-exponential classical representation of the protein ¹H echo was found. Families tried:
- weight-w and ε ≥ 1e-4 Pauli;
- CCE to order N−3;
- operator-spreading / FKPP;
- stochastic Pauli;
- MPO with χ ≤ 64;
- classical spins / DTWA;
- a hybrid exact-core + classical-spin bath (errors 4–20 σ against the N = 16 reference).

Only representations holding essentially the full operator space succeed, and exact simulation is cheap there. Transfer, by contrast, is compressible. The mechanism is explained in T6: transfer is one Pauli coefficient, while the echo is the whole-operator anticommuting weight.

**P3. Classical landscape science (MEASURED; classical, not quantum).** The first characterisation of a language-model-derived distogram posterior along a 30–150 aa ladder:
- the mode census is unsaturated at L ≥ 100;
- the λ-path shows a communication barrier Λ ≈ 14–29 with 0 round trips;
- ρ(E, RMSD) over modes ≈ 0.31 at L = 120;
- the A80 energy is piecewise smooth (0.05 Å table), which invalidates Laplace basin masses.

**P4. R1-SIM (physics-simulation residue).** R1-SIM (the physics residue: can the protein ¹H echo be computed classically?) was settled in rounds 3–4, in three parts.
- **At 40 µs: classically computable to σ = 0.01 (K-119, provisional).**
  - Two exact cluster families containing the butterfly site's partners (≤ 22 spins; 5 implementations, 3 code paths) agree to ≤ 0.0055 on 8/8 series.
  - Thermodynamic estimators (spinDMFT-embedded, classical-spin-embedded) agree to ≤ 0.011.
  - Cost: minutes of CPU.
- **At 80–120 µs: open**, as a cluster-family problem (spin-off register).
- **The round-3 hybrid comparator and all X-based criteria were retired (K-120).**
- The earlier "N_σ = 16–20 spins" and "finite-cluster floor 3–8σ" claims were step-statistic artefacts and were withdrawn.

Nothing here is a quantum advantage, and it never revives K-105.

## 12. Theoretical results

- **T1 (reduction theorem).**
  - A quantum stage whose objective is dephasing-dominated and whose output is consumed via argmin / energy-order tail / convex program is output-equivalent to a classical optimiser over the simplex. This is **PROVED** (H-001a).
  - Cost equivalence is proved for explicit tabulated E. It is false in the query model for implicit black-box E (quadratic), and open for structured E.
- **T2 (sampling).**
  - QSA along the prior→posterior path gives same-chain quadratic gains, L2 (L3 with T3).
  - The Syed communication barrier is blind to first-order crossings.
  - The gap bound δ ≤ (8/p)e^{−ΔF‡}.
  - Break-even τ_* > B* = (A ρ K n_b R)².
  - **Minimum-runtime corollary: no landscape gives an advantage at a per-sample quantum wall-clock below T*_Q = Aρ(K n_b G t_T)²/c.**
- **T3 (fault-tolerant resources).** A faithful coherent walk step for the A80 energy costs G(L) ≈ 2.9–3.6×10⁴·L² Toffolis, with arithmetic dominating. Fixed-point precision needs 22–25 bits.
- **T4 (amplified mode finding).** Quadratic only against i.i.d. restarts. The hardware gate fails at 170 µs for any map evaluating the energy once, and at 1 µs under stated assumptions.
- **T5 (ceiling).**
  - At most quadratic on information-local families with an easy background.
  - Precision gains at most quadratic.
  - No universal ceiling (Simon-trail counterexample).
  - Escape routes enumerated.
- **T6 (mechanism).** Coefficient-truncated classical dynamics reproduces NMR transfer (one coefficient; operator hydrodynamics) but not echoes, which read the anticommuting weight of the whole operator, including its high-weight tail.
- **No-go notes from the attack:** BCGL fixed-node dominance (QM-08), barrier-exponential conservation in QLSA committors (QM-13), arity collapse of Kikuchi on pairwise protein data (QM-17), and assignment collapse of restraint posteriors (QM-18).

## 13. Scaling results

- **Learned energy (MEASURED).**
  - Random-multistart p_hit(best mode) falls 0.10 → 0.004 over L = 30 → 150, and NRPT makes 0 round trips at L ≥ 80.
  - This is **not** classical hardness. It reflects a weak baseline plus fixed-depth relaxation: distance-geometry seeding reaches or beats the census-best basin on 14/16 crops at L = 150 in ~420 evaluations (replicated by two lanes).
  - Generalised floor (DERIVED): T*_Q,s = K n_b G t_T · X^{1/(s−1)}. Against the DG portfolio, every exponent needs t_T ≲ 3 ns at L = 100–500.
- **Quantum-enhanced MCMC on discretised learned-energy instances (MEASURED, n = 6–10).**
  - The exponent ratio k_q/k_c is sub-quadratic to quadratic.
  - The quantum/classical gap ratio is ≤ 12.7, against 784–2.3×10⁵ needed to break even.
- **NMR echoes.**
  - Sparse Pauli dynamics saturates the operator space (M* ≈ 4^N/4). The Pauli-string count is not a hardness metric at N ≤ 12, and exact simulation dominates it (MEASURED).
  - The echo light cone: converged in cluster families that contain b's partners at 40 µs (≤ 22 spins). At 80–120 µs no classical family pair agrees within σ yet, a cluster-family problem (MEASURED).
- **All-atom physics.**
  - B*₂ ≥ 4×10¹¹ MD steps exceeds every enhanced-sampling twin cost (weighted ensemble NTL9 ~1.3×10¹¹ steps).
  - A hypothetical s ≥ 3 would break even (DERIVED + LITERATURE-SUPPORTED).

## 14. Resource estimates

- **Sampling family** (BREAK_EVEN §1, T2/T3): B* = 10¹⁰ (every optimistic assumption stacked) to 10²² (cited constants). T*_Q ≥ 0.26 yr (Cartesian target, 1 µs Toffolis), 1–20 yr (A80 target), 10⁵–10⁷ yr (central). One-day samples need Toffoli times of 12–100 ns (optimistic) or sub-ns (central).
- **Amplified multistart:** p* ≤ 10⁻¹¹ vs measured p_hit ≈ 10⁻².
- **NMR forward model** (`research/theory/nmr_resource_model.py`):
  - One fault-tolerant echo evaluation (16 times × 4 observables, amplitude estimation to 3×10⁻³) costs 2.5×10¹¹ T (N = 14) to 9.6×10¹² T (N = 466). That is 3 d – 111 d serial at 1 µs/T, or ~11 h depth-limited with unlimited factories.
  - An inversion with 10³ gradient evaluations takes ~11 years per machine at 1 µs T-layers.
  - NISQ needs 3×10⁴–3×10⁵ two-qubit gates, so fidelity is e^{−32} to e^{−270} at 10⁻³ error.

## 15. Hardware analysis

- **NISQ.** Echo circuits for N = 14–120 spins need 3×10⁴–3×10⁵ two-qubit gates; fidelity is e^{−32} to e^{−270} at 10⁻³ error. The simulated noise attack (N5) shows mitigation only helps at ≤ 1e-4 per two-qubit gate, and only at N = 10, where exact classical simulation is trivial.
- **Fault-tolerant.**
  - The sampling family needs 10⁴–10⁵ logical and 10⁷–10⁸ physical qubits, with per-sample wall-clock ≥ months (T3, T2).
  - The NMR forward model needs 10¹¹–10¹³ T gates per evaluation, 4–11 h per evaluation even with unlimited factories at 1 µs T-layers, and ~10 yr for an inversion.
  - Every break-even run needs CCZ error ≤ 3×10⁻¹⁴ (T3), beyond assumed factories.
- **No hardware experiment was run.** All quantum results are simulator results. Simulator runtime is never reported as quantum runtime.

## 16. Adversarial results

- **Discovery attack.** 25 mechanisms × 3 independent lenses: classical adversary, oracle/resource auditor, relevance/novelty. All 25 killed; 3 more dead on arrival (`research/discovery/CLASSICAL_COUNTERARGUMENTS.md`, `attack_records.json`).
- **R1 attack.** Seven lenses:
  - independent reimplementation;
  - FI methodology;
  - new classical echo adversaries;
  - physical feasibility;
  - value/break-even;
  - hardness theory;
  - amplification.

  A director synthesis and a completeness critic followed (`research/experiments/ADVERSARIAL/R1_*`).
  - The replication confirmed the numbers to machine precision, then showed the ε-ladder artefact.
  - The critic added classical-spin/DTWA and δ-extrapolation adversaries (both fail on the echo) and prior-regularised information (gain 1.1–2.3 at best).
- **Replication.** The echo result was replicated on a second protein (1PGA) and in amide-only networks. The C1 exact numbers were reproduced by an independent simulator (dense and Pauli-transfer-matrix engines).
- **Controls that killed apparent wins:**
  - the weight-4 statistic → ε-ladder completion;
  - Laplace weights → invalid for piecewise-smooth A80;
  - the per-point partition gain → estimator-level fits (overstatement 3–5000×).

## 17. Novelty analysis

- **NM-1 (Program C).** The idea of quantum-simulating protein ¹H dipolar dynamics to learn structure, and the qualitative hardness–learnability tension, are **anticipated by O'Brien et al. (PRX Quantum 3, 030345, 2022)**. Hardware precedent for small molecules: Zhang et al. 2025 [F34].
- Under the stated search scope (arXiv API, the 448-paper bibliography; general web search was exhausted), the search found no evidence of a study that:
  - (a) benchmarks site-resolved protein ¹H echoes (OTOC) against a best-classical adversary panel;
  - (b) splits the structural Fisher information by classical failure time;
  - (c) shows that transfer is classically reproducible while echoes are not.

  These are incremental, quantitative contributions, not a new mechanism.
- **Sampling-family results** are instantiations of known quadratic-speedup obstructions (Sanders/Babbush) for a learned protein energy. New elements, within the search scope: the landscape-independent T*_Q statement, the first landscape characterisation of an LM-derived distogram posterior, and the white-box dequantisation arguments (NM-2, NM-9).
- Open memos NM-2 … NM-15: `research/discovery/NOVELTY_MEMOS.md`.

## 18. Remaining uncertainties

- **R1-SIM:** whether the converged dense-network echo exceeds exact classical reach (answered at 40 µs (classically computable, K-119, provisional pending replication R-1); open at 80–120 µs as idealised-model physics only).
- **Protein Loschmidt-echo T3/T2:** no measurement is known. The feasibility kill uses model-solid values (INFERENCE). Fine et al. 2014 and Krojanski–Suter 2004/06 suggest the size-dependence of irreversibility is not settled.
- **Learned-energy hardness:** whether the λ-path's classical difficulty is a barrier or ill-conditioning (0 round trips, uninformative at L ≥ 100). It does not affect the quantum verdict (K-101 is landscape-independent).
- **Generality:** only one learned energy (A80/esmprior_v1), two small proteins for NMR, one orientation mostly. No membrane or large protein.
- **Literature scope:** general web search was exhausted. All "no evidence" statements are scoped to the arXiv API, Crossref and the 448-paper bibliography. Several lens citations are abstract-level only (flagged in the records).

## 19. Best candidate

The best candidate that was examined is **quantum forward simulation of dipolar echoes (OTOC(1)) in protein ¹H networks** (Program C, R1).
- It is the only formulation for which classical *approximations* were measured to fail on protein-derived data, and the only one whose target is genuinely quantum (non-diagonal, non-commuting dynamics).
- As a protein-structure advantage it is **killed** (K-105). What remains is a physics-simulation question (R1-SIM, P4), not a structure lead.

## 20. Strongest classical explanation

1. **The endpoint is information-limited, not computation-limited** (S29–S33 and this sprint).
2. **Every classical-objective route is at most quadratically accelerable.** At break-even the quantum wall-clock is months to millennia per sample, whatever the landscape (T2 corollary).
3. **White-box pair-additive energies leak their own structure.** Distance-geometry seeding and the e^{−KL} sublevel bound dequantise the constructions that separations need.
4. **Fold information sits in weak couplings.** Those are classically perturbative. The genuinely quantum sector (echoes) either lies beyond the physical reversal horizon, or within cones that exact classical simulation covers, or it adds only a factor ~1–3 in information over classically usable data.

## 21. Final claim level

| Line | Theoretical | Practical | Claim ladder (A–I) |
|---|---|---|---|
| Learned-posterior sampling / optimisation | L2 same-chain (quadratic, walk steps), L3 with T3 costs; L0 vs best classical | L0 | D (resource-normalised) **negative** |
| NMR transfer forward model | L0 | L0 | killed |
| NMR echo forward model (R1) | L1 at most, in a narrow sense (measured failure of ≥ 9 compression families on a fixed unconverged model) | L0 | A (formulation; prior art O'Brien 2022) only |
| R1-SIM | L0 (no separation; 40 µs classically computable, 80–120 µs open physics) | L0 | none (C failed at 40 µs; analog simulators killed, K-118) |

**Overall: no quantum advantage for protein structure computation is supported at any level above practical L0.** The strongest supported statements are rigorous negatives (categories 3 and 6, in negative form).

## 22. Publication strategy

1. **Main paper (negative, category 3/6).** "Where quantum computing cannot accelerate learned-energy protein structure computation."
   - T1 reduction; T2 landscape-independent runtime floor; T3 fault-tolerant cost of a learned pair-energy walk step; T4/T5 ceilings.
   - The 28-mechanism adversarial map.
   - Measured landscape of an LM-derived distogram posterior.
   - Venue: a quantum-algorithms or computational-biology journal. Novelty: NM-2, NM-3, NM-9.
2. **Short paper (NMR).** "Dipolar echoes in protein proton networks resist classical compression but not exact simulation or physical reality."
   - The transfer-vs-echo mechanism (T6).
   - The ε-ladder lesson.
   - The reversal-horizon and value analysis.
   - R1-SIM outcome.
   - Must cite O'Brien et al. 2022 and Zhang et al. 2025 as the origin.
3. **Methods note.** Sector-exact infinite-temperature correlators and adversary panels for spin forward models.

## 23. Next experiment

- **The single most decisive next experiment** is a *measured* protein Loschmidt/polarisation-echo T3/T2, taken in an oriented or microcrystalline sample.
  - T3/T2 ≥ 15 would reopen the physical side of R1.
  - T3/T2 ≤ 7 closes it for good.
- **Computationally**, extend R1-SIM to N = 22–26 (sector-reduced Krylov typicality) and against an improved hybrid (quantum core + quantum-corrected bath).
- **For Program A** (classical science): diagnose barrier vs ill-conditioning (preconditioned NRPT, 4 seeds, T_cal) and publish the landscape characterisation.

## 24. Final sprint decision (the 17 questions)

1. **Most promising mechanisms.**
   - Quantum forward simulation of protein ¹H dipolar echoes (OTOC(1)) was the only formulation with a measured classical-approximation failure.
   - Hypothetically, an s ≥ 3 algorithm for all-atom Langevin dynamics. No such algorithm exists yet.
2. **Killed.** All examined mechanisms:
   - 28 discovery mechanisms;
   - ~30 round-3 variants;
   - 4 round-4 directions;
   - K-101 to K-120.
3. **Survived strong classical controls.** None as an advantage. Surviving *observations*:
   - the echo resists every sub-exponential classical compression tried (≥ 10 families);
   - the model-internal hybrid failure (L1, excluded from tallies).
4. **Different from S29–S33.** The genuinely new directions are:
   - quantum forward models of physical quantum data (non-diagonal, outside the T1 reduction);
   - the any-exponent floor;
   - the quantum-data theorem;
   - the all-atom no-algorithm regime.

   Sampling routes are new relative to S29–S33 but die by K-101/K-107.
5. **Novel relative to the literature** (scope: arXiv API + the 448-paper bibliography):
   - the landscape-independent T*_Q floor and its any-exponent generalisation;
   - T3 costing of a learned pair-energy walk step;
   - the cross-family σ-level classical computation of protein ¹H OTOC(1) at observable times;
   - the transfer-compressible / echo-incompressible mechanism (T6).

   The NMR idea itself is O'Brien et al. 2022.
6. **Where the quantum algorithm enters.**
   - Sampling routes: a coherent walk or Langevin step replacing the MCMC kernel.
   - NMR routes: the forward model s(t; θ) inside geometry inference.
7. **What classical computation it replaces.**
   - HMC/NRPT/multistart (sampling), which the DG portfolio beats outright.
   - Exact or approximate spin-dynamics simulation (NMR).
8. **Why the same effect cannot simply be reproduced classically.**
   - It can, wherever it is structurally informative: the DG portfolio, and b-aware exact clusters at 40 µs.
   - Where classical reproduction is unresolved (the echo at ≥ 80 µs), the signal is beyond the site-resolved reversal horizon and structurally uninformative (g < 2).
9. **Strongest evidence of advantage.**
   - The echo is incompressible by every sub-exponential classical method tried.
   - Its idealised-model Fisher information is 3–183× that of transfer.
   - Neither survives exact classical simulation at observable times plus physical reversal limits.
10. **Strongest evidence against advantage.** Where structure information exists the classical route is cheap and exact; where hardness might exist there is no usable signal or no algorithm. In detail:
    - K-101/K-107 floors vs the measured ~420-evaluation DG portfolio;
    - K-119 (40 µs echo classically computable);
    - site-resolved reversal horizons (g < 2);
    - K-117 (no applicable all-atom algorithm).
11. **Does the effect scale?**
    - Learned-energy "hardness" does not: it is a baseline artefact.
    - The echo cone converges by ~22 spins at 40 µs and is unresolved at 80–120 µs.
    - All-atom cost scales classically hard, but no quantum algorithm has s > 2.
12. **Complete resource requirements.**
    - Sampling: G(L) ≈ 3×10⁴·L² Toffolis per walk step; 10⁴–10⁵ logical, 10⁷–10⁸ physical qubits; T*_Q ≥ 0.26 yr per sample at 1 µs.
    - NMR echo forward model: 10¹¹–10¹³ T per evaluation (hours, depth-limited).
    - All-atom: T*_Q,2 ≥ 2.2 yr at 10 ns.
    - FeMoco E4: ≥ 10.8 QPU-days per question.
13. **Break-even regime.**
    - Quadratic routes: t_T ≲ 12–100 ns (A80, most optimistic) or sub-ns for one-day samples.
    - Any exponent against the DG portfolio: t_T ≲ 3 ns.
    - All-atom: s ≥ 3 at 10 ns (T*_Q,4 = 2.6 h–10 d).
    - NMR vs exact simulation: N_eff ≈ 30–47. At observable times the needed N is ≤ 22.
14. **Nature of any advantage.**
    - Empirical: none.
    - Theoretical: only same-chain quadratic (L2/L3) and query-model statements.
    - Sampling: none.
    - Computational: none.
    - Hardware: none.
    - Fault-tolerant: negative estimates.
    - End-to-end: none.
15. **Unproven.**
    - Whether an s ≥ 3 algorithm for chaotic force-field Langevin dynamics exists.
    - Protein site-resolved T3/T2.
    - The echo at 80–120 µs.
    - Generality beyond one learned energy, two proteins and one field orientation.
    - FeMoco E4 model floor.
16. **Strongest publishable claim.** The resource-normalised negative (landscape-independent floor + T3 costing + DG classical twin + 28-mechanism map). Plus the NMR statement: protein ¹H OTOC(1) echoes are classically computable to σ at observable times (cross-family + spinDMFT) and structurally uninformative beyond the reversal horizon.
17. **Most decisive next experiment.**
    - Experimental: a measured site-resolved polarisation-echo T3/T2 in microcrystalline GB1 or ubiquitin.
    - Theoretical: an s ≥ 3 quantum algorithm (or no-go) for chaotic multi-basin Langevin dynamics with a compiled force oracle.
    - Computational confirmation: R-1 (replicate K-119 on 1PGA p390, 1UBQ p487 and more orientations; ~2 CPU-h).

## 25. Reproducibility commands

```bash
pip install -e .[dev]                       # repo root; Python 3.13, CPU only
python -m qapf.governor /dev/null --log research/results/RAW/master/governor.jsonl --max-workers 5 \
    --spool research/results/RAW/master/spool.jsonl --forever --stop-file research/results/RAW/master/STOP
# G1 (learned posterior; needs data/instruments/ladder/*.npz from src/qapf/protein/targets.py and the vendored model)
python scripts/g1_mode_census.py --crop 5O37A_100 --restarts 256
python scripts/g1_sample_crop.py --crop 5O37A_45 --T 1 --scans 100000 --time-budget 1500 --pivot 4
python scripts/tpt_crop.py --crop 5O37A_60 --rungs 24 --tmax 40 --budget 750
python scripts/g1_transmission.py --crop 5O37A_60 --restarts 64
python scripts/analyze_g1.py; python scripts/analyze_transmission.py
# Program C (NMR)
python scripts/nmr_gate.py --pdb 1UBQ --probe 19 --N 10 --gamma 0 --exact sector          # C1 (v2)
python scripts/nmr_gate.py --pdb 1PGA --probe 325 --N 10 --hn-only 1 --dt 5e-6 --steps 200 --out research/results/RAW/nmr_gate_hn
python scripts/nmr_sparse_scaling.py --probe 19 --N 12 --gamma 0                          # C2/C3
python scripts/nmr_embed.py --probe 245 --Ncore 10 --envs 12,14                           # R1-E
python scripts/nmr_circuit_pop.py --probe 19 --N 10                                      # quantum proof-of-principle
python scripts/analyze_nmr2.py research/results/RAW/nmr_gate; python scripts/analyze_c2.py
python research/theory/nmr_resource_model.py
python scripts/synthetic_lab.py --family golf --nmax 16
python scripts/make_figures.py
# theory checks
python research/theory/PROOFS/T1_reduction_checks.py; python research/theory/PROOFS/T2_sampling_checks.py
python research/theory/PROOFS/T4_amplified_checks.py; python research/theory/T3_resource_model.py
```

## 26. Git checkpoint

Checkpoints of this sprint (newest first; `git log` is authoritative): the final commit that adds this report, then ae92f98 (adversarial kill of R1), b3fccd8 (pause), 50e0c9e, 0d60410 (discovery synthesis), 92bb4eb (theory + prereg), 4036d44 (infrastructure). Earlier history is preserved: 9ed5531, 86ff140, and the S29–S33 import (33dbaef, 7440b9a).
