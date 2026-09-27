# Architecture search: formulations, representations and program structure explored

_Discovery sprint, 2026-09-27._

## 1. What was searched

The sprint did not assume VQE, QAOA, sampling or optimisation. Seven lanes generated 90 cards, deduplicated to 28 mechanisms:
- quantum algorithms;
- complexity theory;
- genuinely quantum physics;
- learned priors and representation;
- a classical-adversary scout;
- unconventional formulations;
- prior-art scout.

The mechanisms span five computational roles a quantum computer could play:

| Role | Formulations explored | Representations | Cards |
|---|---|---|---|
| Sampler of a classical posterior | λ-path QSA / Szegedy walks, QRELD (Witten-Laplacian QSVT), quantum rejection sampling, hide-and-seek amplifier, restraint-joint posteriors, fold-switch bimodality | (θ,τ) torsions on a 2^b grid; Cartesian single-residue moves; restraint-assignment × structure | QM-01, 02, 03, 04, 11, 15, 18 |
| Optimiser / searcher | QHD / coherent tunnelling, amplitude-amplified multistart, backtracking / tree size over SSE topologies and DMDGP trees, planted-inference Kikuchi, quantum games for negative design | continuous torsions; combinatorial topology trees; distograms and restraint tensors | QM-02, 10, 16, 17, 28 |
| Estimator | amplitude estimation of posterior functionals, DQC1 / Lee–Yang, committors via QLSA / QSVT | posterior expectations, partition-function ratios, backward-Kolmogorov operators | QM-13, 14 |
| Quantum forward model of physical quantum data | ¹H dipolar spin-diffusion (RFDR), OTOC / echo NMR, ZULF / DEER / radical-pair / optical / scattering forward models, metal-cofactor electronic structure, nuclear quantum effects | spin-½ networks from protein proton coordinates; active-space fermionic Hamiltonians | QM-19, 20, 21, 22, 23 |
| Structural invariants / other | quantum knot invariants, quantum TDA (Mayer homology), coupled-oscillator (Babbush) simulation of elastic networks, quantum sensing (NV quantum memory, multi-pass TEM) | knot diagrams; simplicial complexes; spring networks; sensor states | QM-24, 25, 26 |
| Meta (no-go / costing / dequantisation) | consumption-factoring no-go, fault-tolerant cost certificate, TN / Schmidt dequantisation audit, ground-state (stoquastic parent) formulation, GHV / LWWZ transfer | — | QM-05, 06, 07, 08, 09 |

## 2. Revival templates applied (old mechanism → new mechanism)

The inherited S29–S33 failure class was quantum stages with a diagonal classical cost, consumed via argmin, energy-order prefix or convex functional over small enumerable registers (K-001 … K-013). Each new formulation states why the old control no longer applies:
- **Sampling routes (QM-01 family).**
  - OLD: CVaR-VQE on enumerable registers; solver-equivalence.
  - NEW: provable Chebyshev/QSVT mixing acceleration on a non-enumerable continuous posterior, consumed as samples.
  - Why the old control does not apply: the space is not enumerable, and the twin is a mixing-limited MCMC rather than an exact solver.
  - NEW TEST: G1 + R2-T. **Killed** by the landscape-independent runtime floor (T*_Q), not by the old control.
- **Forward-model routes (QM-19/20/21).**
  - OLD: classical objective.
  - NEW: the quantum computer evaluates a physical quantum observable (non-diagonal, non-commuting dipolar dynamics).
  - Why the old control does not apply: T1's reduction covers diagonal classical costs only.
  - NEW TEST: C1/C2/C3/R1-E/PoP. **This is the only formulation for which a classical approximation has been observed to fail on protein-derived data.**

## 3. Program structure and compute allocation (from the synthesis)

Programs A and C keep their meanings from PREREG_G1_C1_Q4. The allocation covers the next 7 days of the 8-core / 15.6 GB box at ≤ 95%, about 1,150 core-hours. All runs go through the governor; agent-side checks run under it too.

| Program | Scope | Residual / cards | Share | ≈ core-h | Stop rule |
|---|---|---|---|---|---|
| **A** Learned-posterior landscape | G1 production + R2 tests (transmission, preconditioned NRPT, DG replication, planted wells) | R2; QM-01/02/03/04/10/12/15 | 30% | 345 | Close after the R2 tests if K-G1a–d fire (expected). Publish the landscape characterisation as classical science. |
| **B** Resource and break-even certificates | T3 final, compiled t_pair kernel, coherent gradient oracle (G-6), BREAK_EVEN freeze | QM-05; gate for all quadratic cards | 3% | 35 | Stop once BREAK_EVEN §1–4 is frozen and committed. |
| **C** NMR many-body forward model | C1/C2/C3 + embedding and hybrid adversaries + perdeuterated HN network | R1; QM-19/20/21 | 40% | 460 | Close on any R1 kill criterion. Move its budget to E. |
| **D** Sensing and metrology (hardware-realistic) | NV memory, multi-pass TEM | QM-24 | 0% | 0 | Parked; outside the computational mission. Reopen only on a verified multi-pass EM with ≤ 10% per-pass loss. |
| **E** New-information hybrids | Restraint-value curve, collapsed ambiguous-restraint posteriors, fold-switch information test | R3; QM-18, QM-15, QM-14 residue | 20% | 230 | Ends when the restraint-value curve and the ambiguity census are done (one pass). |
| **F** No-go consolidation (paper) | KILLED_DIRECTIONS.md; T1/T5 addenda; no-gos from QM-06/08/09/11/13/16/17/25/26 | All killed cards | 2% | 25 | Stop once each KILLBOOK Section B entry cites committed evidence. |
| **G** Super-quadratic theory residues | Mayer gate, 3-body Fourier-degree audit, explicit-naming lemma | R5; QM-09/17/25 residue | 3% | 35 | Close the Mayer branch if the AUC gain is ≤ 0.01. The paper items end at a memo. |
| **H** Out-of-endpoint chemistry | DMRG [2Fe-2S]/[4Fe-4S] check | R4; QM-23(a) | 2% | 25 | Park after one run whatever the outcome. It is outside the structure endpoint. |

**Priority order if capacity is contended:** C (only measured adversary failure) > A (already running) > E > G > B > F > H.

**Immediate actions.**
1. Commit a checkpoint now. Theory T1–T5, the prereg, the NMR v2 instrument, C2 outputs and the qm26/qm11 adversary folders are all uncommitted.
2. Move every scratchpad artefact cited by a lens into `research/results/RAW/<card>_adversary/` with a README noting "exploratory, not pre-registered".
3. Append the R1 and R2 additions to the deviation log before any new output is inspected.

**State changes to record in CURRENT_STATE / HYPOTHESES.**
- H-006: killed at the practical level (landscape-independent); hardness pending the R2 tests.
- H-007: killed by DG dequantisation, pending converged replication.
- H-008: resolved. Break-even is computable, and it is astronomically far except in the single most optimistic stacked corner (T*_Q ≥ 0.26 yr/sample).
- H-009: remains falsified (T1 §7). QM-06 supplies a rescoped screening checklist instead.
- H-C1: weakened. Transfer is killed (f_hard = 0); the OTOC branch stays open under R1.
- New H-C1-null evidence: bath embedding, and the κ ≤ 0.05 weak-coupling reduction for 5–8 Å pairs.

---

## 4. Architecture actually built in this sprint

- **Program A (classical-first gate for sampling).** The vendored A80 energy on a leakage-screened 16-chain ladder (30–150 aa); NRPT on the λ-path with HMC and pivot moves; temperature exchange; multistart mode census; Laplace-mixture transmission test.
- **Program C (quantum forward model and adversaries).**
  - Exact references: sector-exact deterministic, validated to 1e-15.
  - Adversary panel: weight-w and ε-sparse Pauli propagation, sub-cluster exact, classical spins, and a Gaussian-bath dephasing embedding.
  - Fisher-information split and gain spectrum.
  - Minimal quantum circuit proof-of-principle: a shot-based echo circuit with depolarising noise and echo-normalisation mitigation.
- **Theory stack.** T1 reduction, T2 sampling speedup and break-even, T3 fault-tolerant resources, T4 amplified mode finding, T5 quadratic ceiling, plus the NMR resource model.
