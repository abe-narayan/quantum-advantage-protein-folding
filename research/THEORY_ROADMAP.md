# Theory Roadmap

_Created 2026-09-26 at the end of the literature phase. This is the program's plan for theoretical work, and it sets the order in which theory and classical measurement gate any quantum work. Evidence: `research/literature/` and `research/sprint29-33/`. Citation keys resolve in `research/literature/BIBLIOGRAPHY.md`._

## Principle

Every claim of advantage the program could make is quadratic, query-model and fault-tolerant, and it is conditional on classical hardness (`literature/LITERATURE_REVIEW.md` §4, §7). Theory therefore has two jobs:
1. state precisely **what the quantum primitive would buy, in which parameter**;
2. state precisely **what classical measurement would make that parameter large enough to matter**.

No quantum implementation happens until both are written down and the classical measurement has been made.

## T1. H-001 reduction theorem (generalised) — `theory/quantum_advantage/`

- **Statement to prove.** Let a pipeline's quantum stage output a distribution p over a register, where p is shaped by a diagonal cost E. Suppose downstream stages consume p only through (a) argmin E, (b) an E-order prefix or tail, or (c) a convex functional of p over a diagonal-energy objective. Then a classical algorithm reproduces the pipeline output at equal or lower cost.
- **Ingredients.**
  - Predecessor results: prefix theorem T1, solver-equivalence, closed-form p*, hull projection (R1–R12).
  - Literature: Barkoutsos eq. (12) [C6].
- **Generalisation step.** Place the theorem alongside the known general classical-reproducibility results:
  - error-mitigated noisy circuits [F35];
  - barren-plateau-free circuits [F37];
  - trainable generative models [F91];
  - dequantisation [F52–F55].
  Then state the combined scope.
- **Output.** A screening checklist every future architecture must pass before compute is spent.
- **Kill criterion.** A counterexample found in the evidence.
- **Status.** Not started. Needs no compute.

## T2. Quantum sampling speedup for learned-energy posteriors: precise statement (supports H-006/H-007)

- **T2a. Parameter identification.** Write the target π_L ∝ exp(−E_learned/T) over (i) discretised Cα coordinates and (ii) torsions. Identify which known result applies, and in which parameter:
  - Szegedy/QSA: δ of the chosen classical chain [A8, A31];
  - quantum RELD: Gap of replica-exchange Langevin, or C_PI [A44];
  - continuous separation: α = e^{βΔ} [A45].
  Make explicit that the gain is **relative to the classical chain being quantised**. Against a *different*, better classical sampler the comparison must be made separately.
- **T2b. Warm-start and cold-start accounting.** State when a gapped annealing path with Ω(1) overlaps exists, as needed by [A7, A9, A44]. Otherwise quantify the √N (state-space) penalty [A9].
- **T2c. Classical lifting check.** For the chosen chain, decide whether a nonreversible or lifted classical chain already captures the square-root gain [A14, A15, A18]. If it does, the quantum comparison must use the lifted chain.
- **T2d. Per-sample accounting.** A quantum anneal gives one sample per run (no cloning). Derive the quantum-vs-classical cost ratio for M samples, including classical burn-in amortisation (`literature/QUANTUM_PRIMITIVES.md` §1.2).
- **Output.** A single inequality that H-006's classical measurement must satisfy for the quantum primitive to be relevant, in the measured quantities (τ_int, round-trip time, ESS/CPU-s, basin structure).
- **Status.** Not started. Prerequisite for pre-registering H-006.

## T3. Fault-tolerant resource estimate of a learned-energy walk operator (H-008)

1. Specify the energy: shared-coefficient spline potentials over pair distances, fixed-point b-bit coordinates, and a move set (Cartesian single-residue; torsion).
2. Compile the pieces: squared distance, inverse sqrt, spline evaluation, ΔE accumulation over affected pairs, the Metropolis coin e^{−βΔE} → arcsin √, controlled rotation, and uncomputation. Use published arithmetic building blocks [A59] and the Lemieux coin construction [A55].
3. Count Toffolis per step and logical qubits vs L. Include data loading (QROM) if coefficients are pair-specific (G-6).
4. Convert to wall-clock and break-even under Sanders/Babbush assumptions [A56, B46], at several parallelism levels S.

- **Output.** The break-even classical steps per independent sample, B(L), to compare with the H-006 measurement.
- **Kill criterion.** B(L) ≫ any plausible classical cost, e.g. >10¹⁵ steps at the relevant L.
- **Status.** Not started. Paper study, no hardware.

## T4. Landscape theory for learned energies (supports H-007)

- Formalise the persistence criterion of Woodard et al. [E39] and the golf-course and first-order regimes [E33, E40] in terms measurable on a learned energy: basin masses, widths and barrier structure along a tempering path.
- Connect them to the hide-and-seek instance class of [A45].
- **Output.** Measurable diagnostics, and a statement of which regime would make each quantum primitive relevant.
- **Status.** Not started.

## T5. Scope statements for closed directions (cheap, for the record)

Short notes, citing the literature, for directions the matrix marks KILLED:
- amplitude estimation on biomolecular estimates (variance is not binding [B71]; break-even needs σ/ε ≳ 10⁴);
- Grover and backtracking on protein search (structure plus fault-tolerant overhead [C63–C65, C82, C83]);
- quantum generative priors (data-processing inequality; trainable ⇒ surrogate [F91]);
- electronic structure as a structure lever ([F64], DE-7).

The aim is that future sessions cite a stated reason, not an impression.

## Ordering and gates

```
T1 (reduction theorem) ─────────────┐
T2 (precise speedup statement) ─────┼─► pre-register H-006/H-007 ─► G1 classical measurement (mixing vs L, transmission, landscape census)
T4 (landscape diagnostics) ─────────┘                                          │
T3 (FT resource estimate) ─────────────────────────────────────────────────────┤
                                                                               ▼
                                     compare measured classical cost C(L) with break-even B(L)
                                     ├─ C(L) ≪ B(L) or no transmission  → KILL M1/M2; publish scoped negative (cat. 6/3)
                                     └─ C(L) ≳ B(L) and transmission   → category-3 resource claim study;
                                                                          small-scale simulated operator validation (pre-registered)
```

**Budget note.** T1–T5 need no quantum hardware and no simulator beyond small-scale verification of compiled arithmetic. G1 is classical CPU work under the compute policy.
