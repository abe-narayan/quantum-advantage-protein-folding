# Hypotheses

Registry of scientific hypotheses. Each entry gets an ID (`H-###`), a statement, a claim category (see the charter taxonomy), predictions, a kill criterion, linked experiments and a status (OPEN / SUPPORTED / KILLED / SUPERSEDED). Killed hypotheses stay here and are cross-referenced in `KILLBOOK.md`.

_Revision history:_
- _2026-09-26: file created._
- _2026-09-26: inherited table added; H-001/H-002 proposed._
- _2026-09-26: after the S29–S33 reconstruction, H-001 and H-002 were sharpened and H-003 … H-005 added from `QUANTUM_OPPORTUNITY_MAP.md`._

## Inherited hypotheses (predecessor S29–S33): status as recorded in source

These were tested in the predecessor project and are listed so they are not re-tested unknowingly. The status column uses the source's own label; the evidence is in `research/sprint29-33/QUANTUM_RESULTS.md` (QX-ids). Kills are in `KILLBOOK.md` (K-ids).

| Source ID | Statement (source terminology) | Status in source | Record |
|---|---|---|---|
| S29 charter constraint | "Removing or randomizing the quantum stage measurably degrades the result." | Not satisfied (S29-L55) | QX-01 |
| S29 PREREG_B, B1 | Centring the coupling fixes trainability of the compatibility Hamiltonian | REFUTED (S29-L36) | QX-02 |
| S29 F5b | The TTA VQE endpoint improves on production | REFUTED (S29-L54) | QX-03 |
| S29 lane X | Configuration-space CVaR-VQE with a transverse field contributes | Closed negatively (S29-L56) | QX-04 |
| S30 quadric / halfspace | Endogenous-order lifts escape T1 usefully | Closed by measurement; halfspace headline RETRACTED | QX-07 |
| S31 exact CVaR (p*) | Solving the deployed objective exactly improves the chain | NULL (S31-L20) | QX-10 |
| S32 charter §14 | A quantum component can matter on this instrument | "NO on this instrument" (S32-L(Q3)) | QX-14, QX-15 |
| S33 A41 | CVaR-VQE is a better optimiser than SA on the (θ,τ) register | REFUTED / WEAKENED to a tie under equal tuning | QX-24 |
| S33 H_hybrid | The A41 energy advantage survives to the built chain | NOT load-bearing (FAILED_E1000, E1006/7) | QX-25 |
| S33 D_decoder H-a | Register search beats the register-free decoder on the chain | FAILS on both instruments | QX-30 |
| S33 H-Q1 | Tempered Born machine / posterior-mean readout beats argmin and classical ensembles | FALSIFIED (E700, E710) | QX-28, QX-29 |
| S33 S34-A01 / A82 | RF-seeded register re-test | Pre-registered, NOT RUN | QX-31 |

## Hypotheses of this program

None are pre-registered yet. All five are **PROPOSED**. Each needs a written pre-registration in `experiments/preregistered/` before any compute is spent.

### H-001 (PROPOSED, theory): classical reproducibility of argmin/prefix/convex-consumed quantum stages
- **Statement:** Suppose a pipeline's quantum component prepares a distribution p over a register with a diagonal cost E, and downstream stages consume p only through (a) argmin_x E, (b) an E-order prefix/tail, or (c) a convex functional of p. Then a classical algorithm reproduces the pipeline's output at no loss and at polynomial cost in the register size, or at a cost bounded by that of the classical solver for E. Therefore the quantum component cannot be load-bearing.
- **Claim category:** 6 (a structural negative).
- **Basis:** R1–R4, R9–R11 (`sprint29-33/README.md` §3); QX-01, 03, 10, 14, 22, 27.
- **Prediction:** every inherited architecture falls inside the class, and every inherited null follows from it.
- **Kill criterion:** a counterexample within the class, i.e. a pipeline of that form where the quantum stage changes the output in a way no classical algorithm of comparable cost reproduces.
- **Deliverable:** `theory/quantum_advantage/` derivation plus a screening checklist.
- **Status:** PROPOSED (opportunity-map rank 1).

### H-002 (PROPOSED, competing explanation): information-limited endpoint at ≤ 60 aa
- **Statement:** At 9–60 aa with the available native-free inputs, the built-chain endpoint is limited by missing information: the per-target sign, the common mode, and the long-range pair distributions. It is not limited by search, sampling or estimation. No computational primitive, classical or quantum, moves it without new information.
- **Claim category:** Not an advantage claim. It is the null that any advantage claim must defeat.
- **Basis:** I-1 … I-6 in the opportunity map. Strong at 9–16 aa; moderate at 44–60 aa (I-5 rests on 6 targets).
- **Kill criterion:** a measured computational gap (H-003, H-004 or H-005 surviving) at ≤ 60 aa.
- **Status:** PROPOSED. It is the working prior.

### H-003 (PROPOSED): classical sampling of learned-energy structure posteriors becomes hard with length, and better samples improve the chain
- **Statement:** For the posterior over CA-trace structures under a learned pair-distance energy (esmprior-class), the best tuned classical samplers (PT, replica exchange, SMC, HMC) have mixing or round-trip times that grow steeply (super-polynomially or with a large exponent) in chain length from 30 to 150 aa. At the same time, higher-fidelity samples improve the built chain through a soft (Boltzmann-weighted) readout.
- **Claim category:** Classical precondition for categories 3, 4 and 6 (AA-1: quantum walk / QMCMC gap speedup).
- **Basis:** mid30 soft-over-hard 1.40× RESULT; diversity beats selection (M). Hardness never measured (U).
- **Kill criterion (draft):** (a) mixing within the compute budget with polynomial scaling of modest degree at all tested lengths, or (b) the soft readout from a better-converged ensemble not improving the chain by ≥ 1.0× MDE.
- **Status:** PROPOSED (opportunity-map rank 2). **Classical-only first step.**
- **2026-09-26 literature update:** SUPERSEDED by H-006 (sharpened: best classical *portfolio*, explicit break-even, sampled not enumerated soft readout) and H-007 (landscape mechanism). Kept for history.

### H-004 (PROPOSED): a search gap opens beyond 60 aa
- **Statement:** The gap between the continuous decoder's result and the information floor (the native relaxed under the same energy) grows with chain length, and multi-restart classical search stops closing it beyond about 60 aa.
- **Claim category:** Classical precondition for category 3 / 6 (AA-2, QA-4).
- **Basis:** At 44–60 aa, 32–64 restarts saturate and the gap is ≤ 0.14 Å on 6 dev targets (M). Nothing beyond 60 aa (U).
- **Kill criterion (draft):** the gap does not grow with length, or stays within noise, on ≥ 20 targets per length band.
- **Status:** PROPOSED (rank 3).
- **2026-09-26 literature update:** the *quantum payoff* of a search gap (amplitude-amplified restarts, Grover, backtracking) is KILLED by fault-tolerant overhead and restart saturation [C63–C65] (`literature/OPPORTUNITY_MATRIX.md` M9). H-004 is retained only as a classical measurement of information value, measured opportunistically alongside H-006.

### H-005 (PROPOSED): some pipeline decision is estimator-variance-limited
- **Statement:** At least one decision in the best classical pipeline (e.g. ensemble weights, basin free-energy differences) changes with Monte Carlo sample count at feasible budgets. That makes quadratic-precision estimation (amplitude estimation) relevant.
- **Claim category:** Classical precondition for category 3 / 6 (QA-1).
- **Basis:** None positive. All inherited limits are bias- or information-limited (I(prog)).
- **Kill criterion (draft):** decisions are stable at feasible sample counts.
- **Status:** PROPOSED (rank 4, low prior).
- **2026-09-26 literature update:** RETIRED as a standalone hypothesis. Biomolecular estimates are bias-/mixing-limited [B71]; amplitude-estimation break-even needs σ/ε ≳ 10⁴ vs protein decisions at 10–10² (`literature/CLASSICAL_COUNTERARGUMENTS.md` CA-4). Kept only as a zero-cost side measurement in H-006 runs.

## Hypotheses from the literature phase (2026-09-26)

Full statements, falsifiers, minimal and scaling experiments, resources, confounds and differences from S29–S33 are in `literature/LITERATURE_REVIEW.md` §10. None is pre-registered yet.

### H-006 (PROPOSED; supersedes H-003): learned-energy posterior sampling is classically hard at length **and** samples transmit
- **Statement:** for π_L ∝ exp(−E_learned/T) over Cα traces, L ∈ [30,150], the best equal-effort classical portfolio (PT/REST2+HMC, SMC, learned-proposal MCMC, amortised independence proposal) needs cost growing super-polynomially in L — or ≳10¹² steps per independent sample — to reach a fixed soft-readout quality; and the *sampled* soft readout beats argmin/decoder on the built chain by ≥1.0× MDE.
- **Category:** classical precondition for 3/4/6 (M1, M2).
- **Falsifier (draft):** low-degree polynomial cost with ≤10⁹ steps/sample at L=150, OR no transmission at long40 scale.
- **Status:** PROPOSED — **the next experimental gate (G1)**, after T1/T2 in `THEORY_ROADMAP.md`.

### H-007 (PROPOSED): learned-energy landscapes exhibit persistence / hide-and-seek structure
- **Statement:** at the posterior temperature, narrow deep modes carry mass comparable to broad modes (Woodard persistence [E39]; the instance class of the provable separation [A45]), increasingly with L.
- **Category:** classical mechanism for H-006; determines relevance of M2.
- **Falsifier:** funnel-like mass concentration in wide basins, or negligible narrow-mode mass at all L.
- **Status:** PROPOSED — measured from G1 runs (G3).

### H-008 (PROPOSED): the fault-tolerant break-even of a coherent learned-energy walk operator is computable and not astronomically far
- **Statement:** one Metropolis/Szegedy (or quantum RELD) step for an O(L²) shared-spline pair energy compiles to ≤10⁶ Toffolis at L=100, giving break-even B(L) ≤10¹² classical steps/sample under Sanders/Babbush assumptions [A56, B46].
- **Category:** 3 (resource estimate).
- **Falsifier:** ≫10⁶ Toffolis/step or B(L) >10¹⁵.
- **Status:** PROPOSED — paper study (G2), parallel to G1.

### H-009 (PROPOSED; generalises H-001): a single classical-reproducibility theorem covers every KILLED direction
- **Statement:** the S29–S33 reductions are instances of known general results — error-mitigated noisy circuits [F35], barren-plateau-free circuits [F37], trainable generative models [F91], dequantisation [F52–F55] — and one screening theorem covers all matrix rows marked KILLED.
- **Category:** 6.
- **Falsifier:** a KILLED row the theorem does not cover.
- **Status:** PROPOSED — `THEORY_ROADMAP.md` T1.

## Discovery-sprint status updates (2026-09-27)

Earlier entries are kept as written; status changes are recorded here. Sources: `research/theory/` (T1–T5, BREAK_EVEN), `research/discovery/` (the 28-mechanism attack), `experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`.

- **H-001.** Split into H-001a (output equivalence: **PROVED**, T1 Theorems 1–2) and H-001b (cost equivalence). H-001b is proved for explicit tabulated E, **false** in the query model for implicit black-box E (Dürr–Høyer; quadratic), and open for structured E.
- **H-006.** **KILLED at the practical level, independent of the landscape.** For any route that quadratically speeds up a classical sampler, the per-sample quantum wall-clock at break-even is T*_Q ≥ 0.26 yr (the most optimistic Cartesian target) and ≥ 1–20 yr (A80 target) at 1 µs Toffolis (T2 corollary; BREAK_EVEN §1). The hardness clause is still open: 0 round trips in NRPT pilots is significant at L=45 and marginal at L=60; unsaturated mode census at L ≥ 100. The transmission clause is under test (R2-T); pilot posterior E[RMSD] ties the lowest-E structure.
- **H-007.** **KILLED (exploratory, pending replication).** The white-box pair tables let distance-geometry seeding reach the deepest known basin (QM-02 lens: 61/64 runs at 1–5% of restart/PT cost). Prior sublevel mass ≤ e^{−KL} with KL = 113–960 nats.
- **H-008.** **RESOLVED (negative).** Break-even is computable (T3): G(L) ≈ 3×10⁴·L² Toffolis per faithful walk step, far above the ≤ 10⁶ hypothesised. B* ≥ 10¹⁰ (most optimistic) to 10²² (cited constants).
- **H-009.** **FALSIFIED as worded** (T1 §7). QM-06 gives a rescoped screening checklist instead.
- **H-C1 (new; Program C): protein ¹H dipolar dynamics carry structural information past the best classical approximation's failure time.**
  - Transfer (2-point) branch: **KILLED at N = 10.** Sparse Pauli dynamics at ε = 1e-4 reproduces transfer exactly (f_hard = 0) on 1UBQ and 1PGA, at γ = 0, 1000 and 5000 s⁻¹.
  - OTOC/echo branch: **OPEN.** At N = 10 every classical adversary fails by 80 µs, and 55–100% of the OTOC Fisher information lies later (1UBQ ×2 orientations, 1PGA ×2 probes; exploratory under C3). The decisive tests are C2/C3 scaling and R1-E embedding.
  - Prior art: O'Brien et al. 2022 (NM-1).
- **H-C1-null (competing): the late-window information is a finite-size artefact of isolated clusters, or is destroyed by bath dephasing.** Under test (R1-E). The bath second moment gives γ_i ≈ 3–9×10⁴ s⁻¹, ≥ 10× the C1 dephasing grid.
