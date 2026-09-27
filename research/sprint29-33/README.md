# Predecessor S29–S33: reconstructed scientific state

_Written 2026-09-26 by synthesising the per-sprint imports in `research/sprint29/` … `research/sprint33/`, which were imported from `cvar-vqe-protein-folding-v3@3d5b2d25`. No new experiments were run. This is a synthesis layer: the per-sprint files remain the evidence of record. If this file and a per-sprint file disagree, the per-sprint file wins; record the discrepancy in `OPEN_PROBLEMS.md`._

## How to read this directory

Every statement carries one of three tags:

| Tag | Meaning |
|---|---|
| **M** | **Measured fact.** A number recorded in the source, with a pointer to the per-sprint item (e.g. `s33 Q-C12`, i.e. `research/sprint33/QUANTUM_RESULTS.md` item Q-C12). |
| **I(src)** | **Interpretation made by the predecessor sprint.** Quoted or closely paraphrased, and attributed. |
| **I(prog)** | **Interpretation made by this program** during this synthesis. It is not a finding of the source. |
| **U** | **Untested hypothesis.** Nobody measured it: not the source and not us. |

| File | Contents |
|---|---|
| `QUANTUM_RESULTS.md` | One record per quantum experiment or architecture, with the nine required fields |
| `ARCHITECTURE_EVOLUTION.md` | How the pipeline and its quantum stage changed from S29 to S33, including the non-quantum architectures that became the headline |
| `NEGATIVE_RESULTS.md` | Consolidated negatives, plus the **DO-NOT-REPEAT registry** |
| `OPEN_PROBLEMS.md` | What is unresolved: never run, contradictory, or measured too weakly |
| `../QUANTUM_OPPORTUNITY_MAP.md` | The program-level map derived from all of the above |

## 1. Instruments and the statistical contract (inherited, reusable)

**M.** Three instruments. Built-chain Cα RMSD is the endpoint. Instruments are never pooled (`s33` README §2–3).

| Instrument | Targets | Length | Production / reference | Best at S33 close (DEP, quantum-free) |
|---|---|---|---|---|
| `tuning126` | 126 | 9–16 aa | 3.2105 Å (production A00; quantum stage **off**) | 3.2105 Å, unbeaten in S29–S33 |
| `mid30` | 41 | 25–40 aa | avg75 8.180 Å | A80 3.717 ungated / **3.815 under the pre-registered gate** |
| `long40` | 45 | 44–60 aa | avg75 9.745 Å | A80 4.343 ≈ E308 4.739 (statistical tie; E308 is the more-verified) |

- **M. Contract.** MDE = 2.8016·SE. Below 0.7× MDE is NOT A RESULT; 0.7–1.0× is NOT MEASURED. A RESULT needs ≥ 1.0× MDE, a fold CI excluding 0 and ≥ 4/5 folds. 1.0–1.3× is the type-M zone. Every result carries a DEP or ORACLE label. Chain pairings must be same-job with bit-identical sentinels. Best-of-k corrections are required (Bonferroni, Westfall–Young, winner's curse, split-half transfer) (`s33` README §2; `s33` LESSONS 20–22).
- **M. Instrument hazards.** The projection is deterministic but chaotic: a 1e-14 Å cloud change moves individual chains by up to 1.78 Å. The per-target implementation-noise floor is 0.0134 Å mean and 0.2285 Å max (`s31` headline 7; `s33` LESSONS 26). About +0.16 Å of the tuning126 endpoint is NMR reference noise (`s33` LESSONS 27).
- **I(prog).** The contract, instruments and adversary protocol are the most reusable assets of the predecessor. This program should adopt them unchanged for any structure-accuracy claim.

## 2. What is established: measured facts

1. **M. The deployed quantum stage never reached production.** Production runs `quantum=False` throughout S29–S33. The 3.2105 Å endpoint contains no quantum computation (`s29` QR §0; `s30` QR framing; `s31` QR §0; `s32` QR resource table; `s33` Q-A2).
2. **M. No CVaR-VQE arm improved a built chain at any length.**
   - S33 ran 34 chain-level VQE-vs-classical-twin contrasts over 10 lanes and 3 instruments; none was a RESULT in VQE's favour (`s33` Q-A1).
   - The only equal-tuning chain contrast that leaned toward VQE (E1000, −0.824 Å at 0.84×) did not replicate: seed 1 gave −0.066 (`s33` Q-C12, Q-C13).
   - Untrained random-prior sampling beat the trained VQE on the chain: long40, 2 seeds, +1.035 Å, 1.35× (`s33` Q-C13).
3. **M. The deployed candidate-index CVaR-VQE reduces to classical objects.**
   - (a) Its CVaR tail is always the prefix of the energy order (4,914/4,914 cells to 1e-13; theorem T1) (`s30` Q2).
   - (b) Its free energy has a closed-form "hinged Gibbs" minimiser p*. The circuit is strictly worse than p* on 126/126 targets, and substituting p* is a null (−0.0112 Å, 0.19×) (`s31` Q1, Q4).
   - (c) Its Hamiltonian is target-independent to 0.0407 max-norm (`s31` Q3; confirmed `s32` QR-1).
   - (d) At the endpoint it is indistinguishable from one fixed, target-independent number m (−0.0082 Å, 0.27×) (`s29` QR §2).
4. **M. Structural registers were solved as well or better by classical methods at equal budget.**
   - Registers covered: subset, mosaic, fragment, contact, (θ,τ) torsion, macro and chimera, at 9–171 qubits with exact MPS/statevector simulation.
   - Classical comparators: SA, greedy, exact enumeration, random prior sampling, the untrained warm-start circuit.
   - On 18-qubit registers, greedy found the exact optimum more often than VQE (54% vs 27%). SA's hit rate was comparable to VQE's (24% vs 27% in E604b; 27% vs 37% in E609), and the chain results were equal.
   - On the 69–90-qubit contact register (E306), SA and greedy reached the register optimum on 45/45 targets vs VQE 23/45 (`s33` Q-C8, Q-C17; `s29` QR §8).
5. **M. Register energies did not transmit to the chain.** Within-target ρ(E_P, chain) was −0.08 over 5 equal-budget solvers. VQE beat the random tail on register energy on 45/45 targets and lost on the chain by 0.76 Å (`s33` Q-C12 transmission).
6. **M. The continuous decode at 44–60 aa is restart-saturated.**
   - Min-energy decoy RMSD vs number of restarts: 7.08 (1), 4.40 (32), 4.37 (64), 4.35 (128). Information floor (the native relaxed under the same energy): 4.21 Å.
   - Measured on 6 dev targets, cloud basis, ORACLE (`s33` Q-D3, Q-L2).
7. **M. The long-length gains are quantum-free.** They came from a learned pair-distance prior (esmprior_v1, distilled from ESM-2 650M) decoded by distance geometry (E308) or a register-free L-BFGS decoder (A80). Swapping the prior alone moved the DG ensemble 5.681 → 5.136 Å (`s33` README H4).
8. **M. At 9–16 aa, every native-free channel tested was null or wrong-signed in band.**
   - Channels: 21 displacement fields, 43 recognition channels, physics scorers (AMBER, Legacy), consensus, chiral functionals, sign predictors.
   - Every long-length mechanism transferred to tuning126 was harmful (`s29` B1–B16; `s30` D1–D20, E1–E17; `s32` N-D1–N-D9; `s33` N1–N8).
9. **M. ORACLE headroom exists on the short instrument but is not deployable.**
   - Ceilings: 2.9027 Å (ORACLE prefix-m over top-128; `s29` QR §3); five ORACLE signs 2.8867 Å (`s30` H2); along-μ correction −0.8102 Å (`s31` headline 4); hull floor 1.8290 Å cloud (`s32` QR-3).
   - Each required per-target information that no native-free source supplied.
10. **M. Distribution readouts: diversity helps, concentration hurts.**
    - Averaging all 12 DG decodes beat picking one by loss (5.580 vs 6.018) (`s33` N26).
    - Soft Boltzmann weights beat hard CVaR tails on the mid30 chain (−0.248 Å, 1.40× RESULT, T adversary) (`s33` Q-C18).
    - The random-prior tail beat the VQE tail (`s33` Q-C13).
    - Metropolis came closer than the tempered Born machine to the exact Gibbs mean on 9/10 targets (`s33` Q-C19).
11. **M. No quantum hardware was used.** Every circuit in S29–S33 was classically simulated: statevector ≤ 22 qubits, exact MPS beyond that, with χ ≤ 16 in practice (`s33` Q-B2).

## 3. Reduction results that shape the quantum question

Stated in the source and supported there by measurement.

| # | Result | Scope | Source |
|---|---|---|---|
| R1 | **Set-equality / prefix theorem (T1).** For a diagonal H, every KKT point of a CVaR tail objective is a prefix of the order induced by ∇V. Deployed case: one classical sort. This is Barkoutsos et al. 2020 eq. (12). | Any tail objective whose gradient order is fixed | `s29` QR §5; `s30` Q2 |
| R2 | **Solver-equivalence lemma.** For a diagonal H, min over distributions of CVaR_α equals min_x E(x). Any argmin-only readout gives the same chain whichever solver finds the argmin. A quantum stage can matter only through (i) better optimisation or (ii) a whole-distribution readout. | Diagonal H, argmin readouts | `s33` Q-D1 |
| R3 | **Tail collapse.** At convergence the CVaR tail sits on the argmin. The CVaR − T·S minimiser is a truncated Gibbs law. | CVaR training | `s33` Q-D2 |
| R4 | **Closed-form p*.** The deployed CVaR free energy is convex with an analytic minimiser, solvable by one bisection in microseconds. | Deployed objective | `s31` Q1, Q10 |
| R5 | **Hull projection (Q1-T2).** The sum-to-one readout has gain exactly 1 inside the affine hull and 0 outside. "A structure estimate good enough to make the readout worth solving is already good enough to emit." | Σw = 1, fixed frame, CA cloud | `s32` QR-3 |
| R6 | **a ≡ μ (Q1-T1).** A per-candidate quality estimate and the common-mode correction are the same ~33–39 real numbers per target, with no compression available. | Readout problem | `s32` QR-2 |
| R7 | **Candidate-index dimension counting.** No Hamiltonian on a candidate-index register can be classically hard: dim = number of candidates, so `eigh` costs about 1 ms. | Candidate registers | `s31` Q9, Q10 |
| R8 | **P1 ∧ P2 (S32).** A quantum role needs a decision space that grows with the target *and* a genuinely stochastic energy. "This project has never had either." | Stated as a derived requirement | `s32` QR-9 |
| R9 | **Distribution-equivalence (T1–T4).** A fully trained tempered Born machine is at best an exact Gibbs sampler, which classical Metropolis also targets. | Free-energy objectives | `s33` Q-D4 |
| R10 | **Register bounds (D1–D4).** A random register with basin relaxation equals register-free restarts. A register beats only a heuristic continuous decoder, never an exact one. Restart saturation bounds any global solver's gain at 4.35 − 4.21 = 0.14 Å. | A80 energy, long40, 6 dev targets | `s33` Q-D3 |
| R11 | **Sparse s-of-K closes by monotonicity.** "The hard instances are exactly the ones whose optimum is worse." | Subset readout | `s32` QR-4 |
| R12 | **Non-classicality needs (C1) non-commuting terms and (C2) a prepared state that is not an eigenvector.** "The project has never satisfied both." | All S29-era encodings | `s29` QR §5 |

**I(prog).** R1–R12 share one structure. Whenever the quantum output is consumed only through an argmin, an energy-order prefix or a convex functional of a diagonal-energy distribution, a classical algorithm reproduces it at equal or lower cost. That is the structural core of H-001. The predecessor never tested a formulation outside that class **with a measured computational gap**. S29 lane X (transverse-field mixer) and lane B (compatibility Hamiltonian) were outside it formally, but reduced in practice ("flattening", "microsecond eigh").

## 4. The predecessor's own reading of the bottleneck

- **I(src), S33 REPORT §1.7:** "The bottleneck is information in esmprior_v1's long-range pair distributions … It is not search and not decoding."
- **I(src), S32 REPORT §9:** lowering the RMSD is possible, "but not by any route this pipeline's architecture makes available"; "the next bottleneck is 3n−6 ≈ 39 real numbers per target, which are the answer."
- **I(src), S31:** "SEARCH IS NOT THE BARRIER; DISCRIMINATION IS" (`s31` NR G2).
- **Qualifications recorded in the source:**
  - tuning126 information saturation was "WEAKENED to 'inductive, not a theorem'" (`s33` N12).
  - The decoder-vs-floor gap of 0.14 Å rests on 6 dev targets on the cloud basis (`s33` Q-D3).
  - Nothing was measured beyond 60 aa.

## 5. Scope limits of the inherited evidence (I(prog))

The negatives are strong **inside** this envelope and silent outside it:

- **Chain length:** 9–60 aa, with no targets beyond 60 aa.
- **Representation:** candidate-index, subset/mosaic/fragment/contact/torsion/macro registers, and continuous CA-trace decoders.
- **Energies:** classical, pairwise and diagonal in every quantum formulation. The only non-diagonal cases were S29 lane B (similarity coupling) and S29 lane X (transverse field).
- **Quantum algorithms:** only CVaR-VQE variants, a tempered Born machine (free energy), exact ground-state eigensolves and exact Gibbs.
  - Not tested: QAOA as such, amplitude amplification or estimation, quantum walks, quantum Metropolis or QMCMC, QSVT, Hamiltonian simulation, and fault-tolerant resource estimates.
- **Execution:** simulation only. No hardware and no noise model.
- **Sampling hardness:** never measured. Nobody measured MCMC mixing times, spectral gaps or tunnelling barriers on any energy.

An absence of evidence outside this envelope is not evidence of opportunity. It is where `../QUANTUM_OPPORTUNITY_MAP.md` looks.
