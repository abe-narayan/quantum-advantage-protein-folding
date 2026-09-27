# Where could a quantum advantage exist for protein structure computation? A critical literature review

_Literature phase of the quantum-advantage-protein-folding program, 2026-09-26. No experiments were run and no quantum algorithm was implemented._

**Companion files** (all in `research/literature/`):

| File | Contents |
|---|---|
| `QUANTUM_PRIMITIVES.md` | Per-primitive analysis |
| `CLASSICAL_COUNTERARGUMENTS.md` | Counterarguments and the classical-first filter |
| `PROTEIN_BOTTLENECKS.md` | What is actually hard |
| `QUANTUM_ADVANTAGE_CLAIMS.md` | Claim register with labels and rebuttals |
| `OPPORTUNITY_MATRIX.md` | The 18-column matrix |
| `OPEN_LITERATURE_GAPS.md` | Gaps |
| `BIBLIOGRAPHY.md` | Every citation key |

The research program's plan is `research/THEORY_ROADMAP.md`.

---

## Abstract

- **Scope.** We reviewed quantum computing primitives for optimisation, sampling, estimation, linear algebra, Hamiltonian simulation and generative modelling, along with their complexity theory, fault-tolerant resource estimates and classical rebuttals. We also reviewed the quantum protein-folding literature (2008–2026) and the classical literature on what makes protein structure computation hard. Each primitive was tied to the S29–S33 evidence of the predecessor project.
- **The quantum-folding literature.** No paper shows a load-bearing quantum component against a strong classical baseline on a realistic protein representation.
- **Optimisation and search primitives** are closed on three grounds:
  - classical saturation;
  - structure exploited by exact classical solvers;
  - the transmission failure of optimised proxy energies.
  In addition, the known quadratic speedups do not survive fault-tolerant overhead at relevant scales.
- **Estimation primitives** attack Monte Carlo variance. Biomolecular computation is limited by bias and mixing, not variance.
- **Generative, linear-algebra and NISQ primitives** are dequantised, classically simulable, or aimed at the wrong target.
- **The one line that survives** is *sampling a specified learned-energy structure posterior at ≥60 residues*. The relevant primitives are Szegedy walks, quantum simulated annealing, and continuous quantum Langevin / replica-exchange samplers. Its properties:
  - it offers at most a **quadratic, query-model, fault-tolerant** speedup;
  - it has one provable continuous-domain separation, on hide-and-seek instances;
  - it is relevant only if the best classical sampler is slow on that posterior.
- **The decisive measurement is missing.** Nobody has measured how the best classical sampler's cost grows with chain length for such a posterior. It is a **classical** measurement.
- **Recommendation.** Take that measurement, together with the first fault-tolerant resource estimate of the matching quantum walk operator, as the next experimental gate. A strong negative is the most likely outcome and would be a publishable, scoped result.

---

## 1. Method

- **Six parallel searches,** each with explicit verification rules:
  - A: quantum sampling and Markov-chain acceleration;
  - B: estimation, Monte Carlo and partition functions;
  - C: optimisation and search;
  - D: the quantum protein-folding literature;
  - E: protein bottlenecks and classical methods;
  - F: advantage claims, rebuttals and cross-cutting topics (chemistry, QSVT, QML).
- **Verification.** Every cited paper was checked this session against arXiv, DOI/publisher, Crossref, DBLP, PubMed or Semantic Scholar. Leads that could not be verified are listed separately and never used as evidence (`BIBLIOGRAPHY.md`). A few entries were verified for existence only and are flagged.
- **Claim labels** (charter list): THEORETICAL SPEEDUP, QUERY-COMPLEXITY SPEEDUP, ASYMPTOTIC SPEEDUP, SAMPLING SPEEDUP, HEURISTIC ADVANTAGE, EMPIRICAL ADVANTAGE, HARDWARE DEMONSTRATION, SIMULATOR RESULT, ORACLE-MODEL RESULT, NO ADVANTAGE, ADVANTAGE DISPUTED.
  - Query complexity is never converted into runtime.
  - Simulator results are never converted into hardware advantage.
  - Weak-baseline wins are never converted into general advantage.
- **Tags.** **I(prog)** marks the program's own reasoning or arithmetic, and **I(agent)** marks a search agent's order-of-magnitude estimate. Neither is a literature claim.
- **Search size.** 531 verified keys across the six domains, merging to 448 canonical entries (`BIBLIOGRAPHY.md`, integrity notes). A citation-key audit found 0 missing keys among 970 usages; the one wrong key and one weakly supporting key it flagged were corrected.

## 2. What is actually hard computationally? (question A)

Full table: `PROTEIN_BOTTLENECKS.md` §1.

- **Single-structure prediction is information-limited.**
  - AlphaFold2 accuracy is gated by MSA depth, falling below a median depth of about 30 [E89].
  - Alternative conformations are limited by training data: about 280,000 extra models captured 1 of 7 out-of-training fold switchers [E100].
  - The S29–S33 evidence says the same at 9–60 aa (I-1 … I-6).
- **Approximate equilibrium ensembles of monomers are amortised** by learned generators. BioEmu takes about 4 minutes per 1,000 samples at 100 aa and scales roughly as L² [E83].
- **Kinetics and free energies have mature classical tools** that remove the waiting-time exponential: WE, TPS, MSMs and MBAR [E60, E62, E63, E67, E69]. Their residual error comes from force fields and slow-mode sampling [B71].
- **Worst-case NP-hard lattice and rotamer problems** are solved in practice: Wang–Landau to 500-mers, CPSP, cost-function networks and tree decomposition [E56, C82, C83, C85].
- **What remains computation-limited is exact sampling of a *specified* energy at ≥ tens of residues.** Exact learned samplers stop at about hexapeptides [E79]. Classical sampling is provably slow only in specific regimes:
  - golf-course / entropic bottlenecks [E33];
  - persistence, meaning very narrow and very wide peaks of comparable mass [E39];
  - first-order transitions crossed by tempering [E40].
  Energetic barriers with large basins are made polynomial by parallel tempering [E33]. Natural landscapes are argued to be funnelled [E2–E6]. **Learned energies have never been characterised** (G-3).

## 3. Which hard subproblems have known or plausible quantum speedups? (question B)

| Subproblem | Primitive with a known speedup | Size of the speedup |
|---|---|---|
| Posterior / Boltzmann sampling | Szegedy walks, QSA, continuous quantum samplers [A1, A8, A31, A44, A45] | Quadratic in gap, barrier amplitude or Poincaré constant |
| Expectation estimation | Amplitude estimation [B1, B12] | Quadratic in 1/ε (tight) |
| Partition functions | [B26–B28] | Quadratic in ε and in δ |
| Search / minimum finding | Grover, Dürr–Høyer [C54–C56] | Quadratic (optimal) |
| Tree search | Backtracking / B&B [C57–C61] | Near-quadratic relative to the same tree |
| Hitting times | Quantum walk search [A3, A4] | Quadratic |
| Planted inference | Kikuchi [C71, C72] | Nearly quartic, needs planted structure |
| Electronic structure | Qubitisation + QPE [F45, F61] | Exponential over exact diagonalisation; polynomial or unproven against heuristics [F64] |

**No primitive offers a super-quadratic speedup for any protein subproblem** without planted or algebraic structure that no protein subproblem is known to have.

## 4. Asymptotic vs heuristic (question C)

- **Asymptotic** (proven, all query- or step-model):
  - walk hitting times [A1–A4];
  - QSA steps [A8];
  - adaptive QSA for Bayesian inference [A31];
  - continuous samplers [A39, A40, A44];
  - the Ω(α) vs Õ(√α) continuous Gibbs separation [A45];
  - amplitude estimation [B12];
  - partition functions [B26–B28];
  - Grover and backtracking [C54–C61].
  All are quadratic.
- **Heuristic or empirical:**
  - QAOA on LABS, fitted at N ≤ 40 [C28];
  - quantum annealing scaling claims [C42, C44], disputed [C45, C46];
  - quantum-enhanced MCMC, fitted at n ≤ 10 [A47], disputed [A48–A50];
  - fully-quantum walks, fitted at n ≤ 10 [A46];
  - lattice-folding quantum annealing, fitted at 6–9 aa [D7];
  - QFold, fitted on ≤1,024 states [D9].
  **No heuristic claim is validated at scale against the strongest classical baseline.**

## 5. Testability with realistic representations (question D) and oracle realism (question E)

- **Testable with a realistic representation** (off-lattice Cα or torsion chain, learned pair energy):
  - **M1/M2 sampling.** The *classical* half (δ(L), landscape census) is testable now. The *quantum* half is testable only as a resource estimate (G-2). Simulated quantum walks at protein scale are infeasible, and simulating at toy scale repeats QFold's mistake.
  - M4/M5 estimation, which reduces to M1.
- **Oracles that are unrealistic or exponentially expensive:**
  - **QFold's energy table** was precomputed over all configurations, which is exhaustive enumeration [D9].
  - **Quantum rejection sampling** needs a coherent circuit for the learned prior, i.e. the whole decoder run reversibly [A37].
  - **Grover-type search over decodes** needs a reversible continuous optimiser [C64].
  - **Amplitude estimation** needs a qsample, and loading erases the speedup [B37]. General qsampling is SZK-hard [A11].
  - **QSVT/HHL** needs QRAM, whose cost erases the advantage [F56].
  - **Quantum Metropolis** relies on a QPE variant that "may not exist" [A23].
- **Plausible but uncosted:** the coherent Metropolis step for a learned pair-distance energy.
  - It has O(N²) pair terms, fixed-point distances and spline potentials.
  - I(agent) estimate: ~10⁶–10⁸ Toffolis per step at N = 100 [A §3.9].
  - No published estimate exists (G-2).

## 6. Mapping primitives to protein problems

Format: primitive → subproblem → representation → input → quantum operation → output → classical alternative → possible advantage → main obstacle. Status in brackets.

1. **Ensemble sampling:** Szegedy/QSA walk → posterior sampling → Cα/torsion chain → learned pair energy E(x), T → annealed walk to |π⟩ → posterior samples → PT/REST2+HMC, SMC, learned-proposal MCMC, BioEmu → quadratic in δ → per-step overhead ~10⁷–10¹⁰ vs classical; δ(L) unmeasured. [INTERESTING]
2. **Correlated / continuous sampling:** quantum RELD / QSVT sampler [A44, A45] → same → continuous coordinates → ∇V oracle → Witten-Laplacian singular-value filter → samples → replica-exchange Langevin → quadratic in C_PI or e^{βΔ} (provable on hide-and-seek wells) → warm start; costing; do protein landscapes have such wells? [INTERESTING]
3. **Markov-chain acceleration:** fast-forwarding [A35], nonreversible walks [A43] → transient or relaxation dynamics → chain → transition operator → P^t|ψ⟩ → lifted/nonreversible classical chains [A14, A15] → quadratic in t → relaxation is restart-saturated (QX-30). [WEAK]
4. **Rare-event sampling:** walk hitting time [A3, A4, A22] → transitions → MSM-like discretisation → marked set → quadratic search → transition found → WE, TPS, MSM [E60–E67] → quadratic over brute-force MD only → classical methods already remove the exponential; outside the structure endpoint. [WEAK]
5. **Low-probability conformational discovery:** amplitude amplification over a sampler → rare basins → chain → sampler circuit + threshold → amplified rare states → importance sampling, WE, metadynamics → quadratic in 1/p → needs a coherent sampler (M1) plus a native-free marking criterion. [WEAK, a sub-case of M1]
6. **Partition-function estimation:** [B26–B28] → Z of a conformational model → discrete model → walk at each β → Z to ε → AIS/SMC/Wang–Landau, K* bounds → quadratic in ε and δ → only √δ matters; deterministic incumbents. [WEAK]
7. **Free-energy estimation:** AE over qsamples; KvN/Liouvillian [B53, B54] → ΔG → force field / ab initio → coherent dynamics → ΔF → MBAR/FEP+ → quadratic in ε → force-field bias dominates [B71]. [WEAK / out of scope]
8. **Expectation and uncertainty estimation:** AE [B12] → posterior means, confidence → as 1 → qsample + observable → mean to ε → MBAR, bootstrap, parallel MC → quadratic in ε → protein decisions need σ/ε of only 10–10²; break-even needs ≳10⁴. [KILLED (practical)]
9. **Conformational-state search / global discrete search:** Grover, QAOA, annealing → argmin of E → registers / lattice → diagonal H → low-energy bitstrings → PERM, CPSP, Wang–Landau, SA with equal tuning, restart-saturated L-BFGS → quadratic at best → reduction class (H-001), saturation, condition C [D28]. [KILLED]
10. **Long-range contact constraint satisfaction:** backtracking / B&B [C57–C61] → contact CSP → contact graph → coherent predicate → satisfying assignment → distance geometry + restarts, CP → near-quadratic relative to the same tree → classical pruning; restart-saturated DG. [WEAK]
11. **Search over exponentially large conformational spaces:** as 9 and 10 → funnels plus classical structure; no unstructured regime [E2–E6]. [KILLED]
12. **Probabilistic structure generation:** Born machines / QBM [F75–F79] → ensemble generation → learned → training data → samples → BioEmu, AlphaFlow, diffusion models → none on natural data → data-processing inequality; trainable ⇒ surrogate [F91]. [KILLED]
13. **Correlated (non-product) sampling via entanglement:** QCBM/QAOA-MC → correlated proposals → registers → diagonal H → proposals → cluster moves, tensor-network proposals [A50] → empirical at n ≤ 10 → disputed; register encoding fails condition C. [KILLED for protein]

## 7. Which primitives survive strong classical algorithms? (question F)

The classical-first filter (`CLASSICAL_COUNTERARGUMENTS.md` Part 3) kills a candidate if any of these holds:
- **K1** reduction (H-001 class);
- **K2** classical saturation;
- **K3** information limit;
- **K4** wrong cost factor;
- **K5** quadratic speedup below fault-tolerant break-even.

**Only the sampling line (M1/M2) survives, conditionally.**
- It passes K1: the posterior is consumed whole, as a distribution.
- It passes K3: sampling a *given* energy is not information-limited.
- It passes K4: the target is mixing, not variance.
- It is **unresolved on K5**: the break-even is unknown.
- It is **unresolved on S1**: classical cost growth with length has never been measured.
- It **partially passes S2**: sample value is shown at mid30, but only for an enumerated space.

## 8. What could matter for a publishable result? (question G)

- **A publishable positive would need all of:**
  1. a measured steep growth in the best classical sampler's cost with chain length on a learned-energy posterior, in a torpid regime (golf course, persistence or first-order);
  2. demonstrated transmission of better samples to structure accuracy;
  3. a fault-tolerant resource estimate showing break-even is reachable at a plausible size.
- **Even then,** the available claim is **category 3 / 6** (resource estimate and theory), not an empirical or hardware advantage (categories 2 and 5).
- **A publishable negative is the more likely outcome.** It is valuable: the literature has no mixing-time measurement for learned protein posteriors (G-1), no resource estimate for a protein-energy walk operator (G-2), and no landscape census of learned energies (G-3).

## 9. Connection to S29–S33

| Mechanism | Tested in S29–S33? | What was tested | Why it failed | What would make a new experiment different |
|---|---|---|---|---|
| Variational optimisation (VQE, CVaR, QAOA-like), annealing-like | **Yes, 33 experiments** (QX-01 … QX-33) | Candidate-index and structural registers, 7–171 qubits, diagonal energies | R1–R12 reductions; equal-tuning SA and random prior sampling match or beat it; energies do not transmit | Nothing. The literature predicts the null [C20–C24, D14, D28] and the family is KILLED |
| Non-diagonal / non-commuting terms | Yes (QX-02, QX-04, QX-11) | Similarity couplings; transverse-field mixer | Dimension counting; flattening to \|+⟩^q | Non-commuting terms that encode problem information on a register growing with protein size. No literature proposal exists |
| Tempered Born machine / Gibbs readout | Yes (QX-28, QX-29) | 18-qubit enumerable mosaic | Metropolis was closer to exact Gibbs (9/10); the space is enumerable | **Different primitive** (walk/QSA/continuous sampler with a proven gap speedup), **non-enumerable space** (≥60 aa, continuous), classical portfolio twin |
| Quantum walks, QSA, QMCMC, continuous quantum samplers | **No** | — | — | New: this is M1/M2 |
| Amplitude estimation / partition functions | **No** | — | — | New, but the literature kills it in practice (M4); only √δ matters (M5 ⊂ M1) |
| Grover / backtracking / B&B | **No** (S32 derived QX-14/QX-15 closures) | — | — | New, but WEAK/KILLED by saturation and fault-tolerant overhead |
| Electronic structure | No (DE-7 by evidence) | — | Energy accuracy is not the bottleneck | Out of scope |

**The S33 soft-readout signal.** A Boltzmann-weighted average beat hard tails on the mid30 chain, at 1.40× MDE (QX-28).
- **It is not evidence of quantum advantage.** It was computed by an exact sum over an enumerated 262,144-state space, so there was no sampling cost and no variance [B §7].
- **It is a scientifically meaningful target distribution** (`PROTEIN_BOTTLENECKS.md` §5). A posterior consumed through its *average* lies outside H-001's reduction class.
- **The open question** is whether such averages still help when *sampled* at ≥60 aa, and whether sampling them is classically hard.

## 10. Hypotheses emerging from the literature (question 15)

Four hypotheses, recorded in `research/HYPOTHESES.md` as H-006 … H-009. H-003 and H-005 are refined or retired there.

### LH-1 (H-006). Learned-energy posterior sampling is classically hard at length, *and* samples transmit
- **Hypothesis.** For the posterior π_L(x) ∝ exp(−E_learned(x)/T) over Cα traces of chains with L ∈ [30, 150], the best classical portfolio's cost to reach a fixed soft-readout quality grows super-polynomially in L, or reaches ≳10¹² steps per independent sample within that range. The portfolio is PT/REST2 + HMC, SMC, learned-proposal MCMC, and an amortised independence proposal. At the same time, the sampled soft readout improves the built chain by ≥1.0× MDE over argmin/decoder output.
- **Why it might work.**
  - The only S29–S33 positive signal is posterior averaging.
  - Learned energies are uncharacterised and could be frustrated (G-3).
  - Rigorous torpid regimes exist [E33, E39, E40].
  - A quantum primitive with a proven quadratic gap speedup matches this exact task [A8, A31, A44, A45].
- **Classical baseline.** The portfolio above, each member tuned with equal effort [E §7D].
- **Falsified by** either of:
  - (a) mixing-cost growth fits a polynomial of low degree, with absolute cost ≤10⁹ steps per effective sample at L = 150 (well below break-even, G-2); or
  - (b) the sampled soft readout fails to beat argmin/decoder at ≥1.0× MDE on long40-scale targets.
- **Minimal experiment.** On mid30 and long40 (existing, leakage-controlled), with the esmprior-class energy:
  - run PT+HMC and SMC to convergence;
  - measure τ_int, round trips, ESS/CPU-s, and multi-start basin-population agreement (E39's warning: diagnostics miss torpid mixing);
  - measure the sampled soft-readout chain RMSD vs the decoder.
- **Scaling experiment.** Build a leakage-controlled 60–150 aa instrument. Measure cost vs L on ≥5 length bands × ≥20 targets per band.
- **Expected resources.** Classical CPU only. An O(L²) energy costs ~10⁴ pair terms at L=150. Tens of replicas × 10⁶–10⁸ steps per target is feasible on 8 cores within the compute policy. ESM-2 feature generation is the RAM bottleneck (the S33 lesson: RAM, not CPU).
- **Most dangerous confound.** Mistaking *under-tuned* classical sampling for intrinsic hardness, the E406 → E1001 lesson. Also a learned energy whose ruggedness is a training artefact that a better-trained prior would remove, i.e. hardness that is not intrinsic to the protein problem.
- **Why different from S29–S33.**
  - A continuous, non-enumerable space instead of registers.
  - The distribution is consumed as a posterior average, not argmin/prefix/convex.
  - Lengths beyond 60 aa.
  - A classical-first measurement instead of a quantum build.

### LH-2 (H-007). Learned-energy landscapes contain persistence / hide-and-seek structure
- **Hypothesis.** At the posterior temperature, learned pair-distance energies have narrow deep modes of mass comparable to broad modes. This is Woodard persistence [E39], and the instance class where the continuous separation [A45] holds. The effect grows with L.
- **Why it might work.** ESM-derived pair potentials can be confidently wrong in places (S33 "near-miss" lemma: false positives median 10.2 Å). That could create narrow, spurious deep wells.
- **Classical baseline / measurement.** A mode census by large multi-start minimisation plus Laplace/Hessian basin-volume estimates and basin masses from converged PT. Test the persistence criterion directly.
- **Falsified by.** Mode mass concentrated in wide basins (a funnel), or narrow modes carrying negligible mass at every L.
- **Minimal experiment.** Mid30 and long40 targets, reusing the G1 runs.
- **Scaling.** As LH-1.
- **Resources.** Marginal on top of LH-1.
- **Confound.** Discretisation or projection artefacts creating spurious narrow modes.
- **Why different.** Never measured, in S29–S33 or in the literature.

### LH-3 (H-008). A coherent learned-energy walk operator has a computable break-even that is not astronomically far
- **Hypothesis.** A fault-tolerant compilation of one Metropolis/Szegedy (or quantum RELD) step for an O(L²) learned pair-distance energy (shared spline potentials, fixed-point coordinates) costs ≤10⁶ Toffolis at L=100. That makes break-even ≤10¹² classical steps per sample under Babbush/Sanders assumptions [A56, B46].
- **Why it might work.** Shared-coefficient potentials avoid per-pair tables. Cartesian single-residue moves touch only O(L) pairs.
- **Classical baseline.** The measured classical cost from LH-1.
- **Falsified by.** A compiled cost ≫10⁶ Toffolis/step, or a break-even beyond ~10¹⁵ steps.
- **Minimal "experiment".** A paper compilation: count Toffolis for distance, sqrt, spline, exp, arcsin and controlled rotation; logical qubits; T-factory assumptions. No quantum hardware.
- **Scaling.** Toffolis per step vs L, and vs move type (Cartesian vs torsion).
- **Resources.** Theory time only.
- **Confound.** Optimistic arithmetic costs; ignoring data-loading (QROM) for learned tables.
- **Why different.** No published estimate exists for any molecular or learned energy (G-2).

### LH-4 (H-001 generalised, theory)
- **Hypothesis.** The S29–S33 reductions (argmin/prefix/convex consumption of diagonal-energy distributions) are special cases of general classical-reproducibility results:
  - error-mitigated noisy circuits [F35];
  - barren-plateau-free circuits [F37];
  - trainable generative models [F91];
  - dequantisation [F52–F55].
  A single screening theorem therefore covers every M-row marked KILLED.
- **Falsified by.** A KILLED row that the theorem does not cover but the evidence does.
- **Deliverable.** `theory/quantum_advantage/` derivation plus a checklist.
- **Why different.** It turns 33 empirical nulls into a stated scope.

**Retired / not advanced.**
- **H-005** (variance-limited decisions): the literature says precision is not binding [B71] and break-even needs σ/ε ≳ 10⁴. It is kept only as a free side measurement of LH-1, not as a hypothesis worth its own experiment.
- **H-004** (search gap beyond 60 aa): retained, but its quantum payoff is KILLED (M9). Only its classical information value remains.

## 11. The next experimental gate

**The literature justifies exactly one gate: LH-1's minimal experiment (G1), run together with LH-3's paper resource estimate (G2).** LH-2 (G3) is measured from the same runs.

- **Why this one.**
  - All five domains that examined sampling identified it independently as the decisive missing measurement.
  - It is classical.
  - It is cheap relative to its information value.
  - It decides every surviving quantum candidate (M1, M2, M5) at once.
- **What the gate decides.**
  - **Pass:** steep classical cost growth, transmission ≥1.0× MDE, and break-even within reach. The program moves to a category-3 resource-claim study and a pre-registered simulated-walk validation of the operator at small scale.
  - **Fail:** the program records a scoped negative for quantum sampling of learned protein posteriors, kills M1/M2, and publishes the negative (category 6).
- **Nothing quantum is built before this gate** (CLAUDE.md gate rule).
