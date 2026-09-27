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

_None yet._
