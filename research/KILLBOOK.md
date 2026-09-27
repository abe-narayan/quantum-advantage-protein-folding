# Killbook

Directions that were killed, with evidence. Each entry has the date, the architecture or hypothesis ID, the kill criterion that fired, the evidence (experiment IDs), what capability did *not* disappear under ablation, and the conditions under which reopening it would be justified.

Reopening a killed direction requires new evidence or a materially different formulation.

## Section A: Inherited kills (predecessor S29–S33, source-verified 2026-09-26)

These kills were made by the predecessor project and verified against its sources during the S29–S33 reconstruction. Evidence records are in `research/sprint29-33/QUANTUM_RESULTS.md` (QX-ids). The full reopening conditions are the DO-NOT-REPEAT registry in `research/sprint29-33/NEGATIVE_RESULTS.md` Part 2 (DNR-ids). Every kill below was established in **simulation** and at **9–60 aa**.

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-001 | CVaR-VQE on the candidate-index register (all variants) | Theorem + measurement | Nothing: a fixed profile m and the closed-form p* reproduce the endpoint | QX-01, 05, 06, 10, 12 | DNR-01 |
| K-002 | Quantum optimisation of diagonal costs consumed via argmin, prefix or convex functional | Theorem (R1, R2, R4) + 34 S33 contrasts | Nothing: SA, greedy, exact or sort give the same chain | QX-17–27, 32 | DNR-02 |
| K-003 | Non-diagonal Hamiltonians on candidate registers | Theorem (dimension counting, stable rank) + gate measurement | Nothing: `eigh` is the classical counterpart; the gate stayed shut | QX-02, 11 | DNR-09 |
| K-004 | CVaR-tail ensembles as readouts | Theorem (tail collapse) + E306 | Nothing: a no-register noise ensemble was better; SA tails were equally concentrated | QX-22 | DNR-04 |
| K-005 | Structural register search at 16–90 qubits (subset, mosaic, fragment, contact) | Measurement + condition C | Nothing: SA/greedy/exact matched; search-vs-no-search gains were delivered equally by SA | QX-18–21, 27 | DNR-03, DNR-08 |
| K-006 | Per-residue (θ,τ)/macro registers at 106–171 qubits as load-bearing search | Measurement (equal-tuning SA, random prior, register-free decoder) | Nothing: random prior sampling beat VQE on the chain (1.35×); the register-free decoder was better | QX-24, 25, 30 | DNR-05, 06, 07 |
| K-007 | Tempered Born machine / Gibbs-readout circuits on small (enumerable) spaces | Measurement (Metropolis twin, exact Gibbs) | Nothing: Metropolis was closer to the exact target on 9/10 | QX-28, 29 | DNR-10 |
| K-008 | Transverse-field configuration-space CVaR-VQE (chimera) | Measurement (BESTOFN, SA) | Nothing: untrained best-of-N tied the VQE | QX-04 | DNR-11 |
| K-009 | Endogenous-order tail lifts (halfspace/quadric) | Measurement with order-statistic nulls | N/A (never built); the apparent gain was 196% null | QX-07 | DNR-13 |
| K-010 | Index/encoding redesign and register widening without a selector | Measurement | N/A | QX-12, 13 | DNR-12 |
| K-011 | Quantum solvers for readout convex programs (p*, QP/hull, SOCP, sparse s-of-K) | Theorem (classical polynomial, milliseconds) | N/A | QX-10, 14–16 | DNR-18 |
| K-012 | Native-free in-band recognition/ranking at 9–16 aa from existing inputs (any computational method) | Theorem + measurement | N/A (information-limited) | `sprint29-33/NEGATIVE_RESULTS.md` §1.2 | DNR-16 (new information source required) |
| K-013 | Global-scalar tuning at 9–16 aa | Measurement | N/A | `sprint29-33/NEGATIVE_RESULTS.md` §1.3 | DNR-15 (never) |

**Scope warning.** These kills close the predecessor's *formulation class* (H-001). They do **not** kill:
- quantum algorithms with known separations (amplitude estimation, quantum walks/QMCMC, QSVT, Hamiltonian simulation);
- problems beyond 60 aa;
- sampling problems where classical mixing is slow.

None of those was ever tested.

## Section B: Kills made by this program

_Entries added 2026-09-27 (discovery sprint). Evidence paths are relative to `research/`. Reopen conditions are the revival templates in the cited files._

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-101 | Quantum sampling of the learned-energy structure posterior (walk / QSA / QRELD / quantum replica-exchange Langevin; QM-01, 03, 04, 05, 12) | Derivation (landscape-independent floor T*_Q = Aρ(K n_b G t_T)²/c ≥ 0.26 yr/sample at 1 µs Toffolis; B* ≥ 10¹⁰–10²⁵) + resource model (T3) | Nothing: classical NRPT/HMC/multistart remain cheaper at every L ≤ 150 under every stated assumption | `theory/PROOFS/T2_*`, `theory/RESOURCE_MODELS.md`, `theory/BREAK_EVEN.md` §1, `discovery/attack_records.json` | logical Toffolis ≤ ~50 ns **and** a measured, precondition-resistant, readout-visible barrier ≥ 23 nats with ≥ 1 MDE transmission |
| K-102 | Amplitude-amplified multistart / quantum rejection sampling / hide-and-seek amplification on learned energies (QM-02, 11) | Derivation (T4; p* ≤ 10⁻¹¹ vs measured p_hit ~10⁻²) + white-box dequantisation (distance geometry; e^{−KL} sublevel bound, KL = 113–960 nats; exploratory) | Nothing | `theory/PROOFS/T4_*`, `discovery/CLASSICAL_COUNTERARGUMENTS.md` QM-02/11 | a planted distributed well missed by all classical arms with p < 10⁻⁶ **and** real tables containing such structure |
| K-103 | All other discovery mechanisms (QM-06…10, 13…18, 22…28): no-go routes, QHD, ground-state parents, TN audits, QLSA committors, fold-switch samplers, backtracking, Kikuchi, restraint posteriors, other spectroscopies, metal-cofactor QPE (structure endpoint), sensing, knots/TDA, oscillator simulation, cryo-EM solvers, negative design | Mixed: theorem / measurement / resource / information (per mechanism) | Nothing load-bearing for protein structure | `discovery/KILLED_DIRECTIONS.md`, `discovery/CANDIDATE_MECHANISMS.md` | per-mechanism reopen conditions in KILLED_DIRECTIONS |
| K-104 | Quantum forward model of protein ¹H **two-point transfer** (spin diffusion / NOE-like build-up) | Measurement: sparse Pauli dynamics (ε = 1e-4) reproduces transfer exactly at N = 10 (f_hard = 0; 1UBQ, 1PGA, dense and amide-only, γ = 0 / 1000 / 5000 s⁻¹). Weak-coupling reduction for 5–8 Å pairs (κ ≤ 0.05) | Nothing | `results/RAW/nmr_gate*`, `discovery/attack_records.json` QM-19 | a transfer observable the best classical forward model fails on at physically relevant times |
| K-105 | Quantum forward model of protein ¹H **dipolar echoes (OTOC(1))** as an advantage for structure (R1; QM-20/21 residue) | Pre-registered C3 survival clause failed (reversal horizon: informative window at 4.8–25 T2 vs T3 ≈ 4–6.7 T2) + value/cost (exact classical simulation beats a fault-tolerant forward model below N_eff ≈ 30–47 at 4–6 h per evaluation; gain under realistic priors median 1.1–1.5) + ε-ladder completion (ε = 3e-5 closes the N = 10 window) | At N ≤ 14: nothing. Exact simulation (seconds) supplies everything. Open physics residue: R1-SIM | `experiments/ADVERSARIAL/R1_SYNTHESIS.md`, `R1_CRITIC.md`, `R1_*` lens folders, PREREG deviation log | all four revival conditions in `R1_SYNTHESIS.md` §5 at once: converged σ-cone > 47 spins at information-bearing times; reversal horizon beyond them in a real protein; a structural degree of freedom classical data leave undetermined with profiled gain ≥ 10; a forward model accurate to σ |

