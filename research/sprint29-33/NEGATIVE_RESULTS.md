# S29–S33 consolidated negative results and DO-NOT-REPEAT registry

_Synthesis, 2026-09-26. Tags: **M**, **I(src)**, **I(prog)** and **U**, as in `README.md`. Item-level evidence is in `research/sprintNN/NEGATIVE_RESULTS.md` and `QUANTUM_RESULTS.md`. This file consolidates by class. It does not replace them._

## Part 1. Negative results by class

### 1.1 Quantum stage (all simulation; category-1 tests, all negative)

| Class | Measured headline (M) | Pointer |
|---|---|---|
| Deployed candidate-index CVaR-VQE | ≡ a fixed profile (−0.0082 Å, 0.27×); the circuit is worse than closed-form p* on 126/126; the p* substitution is a null (−0.0112, 0.19×) | QX-01, QX-10 |
| Circuit expressivity | 0.2516 Å (ORACLE objective) is a regulariser artefact of the affine readout; the deployed objective gives 3.4330 Å vs 3.2071 | QX-06 |
| Non-diagonal H on the candidate register | 0/24 gate cells; B1 refuted; `eigh` is the classical counterpart | QX-02, QX-11 |
| Endogenous-order lifts | Halfspace gain 196% order statistic, +0.47 Å as a rule; quadric +0.21 Å WORSE | QX-07 |
| Tail-then-aggregate | Non-prefix optimum exists on 114–124/126 but is +0.245 Å worse; the VQE endpoint is worse | QX-03 |
| Transverse-field configuration space | +0.457 Å WORSE (n = 12); state near \|+⟩^q; BESTOFN ties the VQE | QX-04 |
| Structural registers, 16–90 qubits | Greedy and exact are at least as good as VQE on energy; SA is comparable at 18 qubits and better at 69–90 (E306: 45/45 vs 23/45); the chain equals the SA twin or no-search | QX-17–23, 27 |
| Per-residue registers, 106–171 qubits | Energy win vs untuned SA → tie vs tuned SA → tuned SA better; **random prior sampling beats VQE on the chain** (1.35×) | QX-24, 25, 30 |
| Short-length registers | Condition C fails; random beats VQE (1.02×) at n = 126 | QX-26 |
| Tempered Born machine | Metropolis is closer to exact Gibbs on 9/10 targets | QX-29 |
| Entanglement | No chain effect (2-seed −0.188, 0.26×) | QX-33 |
| Finite-shot CVaR bias | Refuted at 2,048 shots | QX-08 |
| Index encoding | Gray code a no-op; best map below the bar; random permutation is the best deployable | QX-12 |

### 1.2 Information channels at 9–16 aa (non-quantum)

**M.** All null, wrong-signed or harmful:
- 21 native-free displacement fields (best cos 0.1128 vs random 0.1398) (`s29` B4).
- 43 single-structure recognition channels; preference fails on all (`s30` D1).
- Chiral functionals (WRITHE, CHIRAL3, XTWIST) (`s30` D8; `s31` E5; `s32` N-R1).
- Physics scorers, both static and relaxed (AMBER, Legacy); physics as mover (`s32` N-D1–N-D6).
- Consensus as a quality estimate (`s31` B3).
- Native-free sign predictors (`s32` N-D8; `s29` C7).
- Common-mode estimates from the pool (`s31` F1; `s32` N-P12).
- Fitted prior correctors (`s30` E13).
- esmprior_v1 and ESM attention as selectors (`s33` N1–N4).
- Every long-length mechanism transferred to short length (`s33` N5–N8).

**I(src).** "At 9–16 aa no native-free channel carries nonlocal pair information" (`s33` N12). Qualification: saturation is "inductive, not a theorem."

### 1.3 Readout / selection / projection (non-quantum)

**M.** Also null or worse:
- Prefix length m (order statistic; a leave-fold-out m is a coin flip).
- Filter width.
- Sparse readout.
- MEB / dispersion readouts (killed by shuffled controls).
- AVG_SEP / AVG_RG / MED operators.
- Branch selection (no native-free criterion reaches MDE; production argmin ≈ a coin).
- Scalar dilation.
- The bond-length correction.
- Hull projection of a noisy estimate (killed by shrinkage).

Sources: `s29` B3, B10; `s30` C5–C8; `s31` B1–B17, D1–D4; `s32` N-P1–N-P15, N-R1–N-R15, N-Q2.

### 1.4 Length-scaled (S33, non-quantum)

**M.**
- The S32 donor-control mechanism at length was FALSIFIED.
- BLOSUM filter skill does not replicate at length.
- The ESM contact-agreement key has no in-pool skill at 33 aa.
- LFO-XF priors leak via cross-fold homologues (about 10 targets).
- E308's asserted contacts are inert.
- The decoded-ensemble chain effect is NOT MEASURED.
- Elongated targets stay at 11–15 Å under DG even with all native contacts.

Sources: `s33` N14–N30.

## Part 2. DO-NOT-REPEAT registry

**Rule.** The experiments below must not be re-run in this program unless the proposer states, in the pre-registration, which listed "materially different" condition the new formulation meets, and why that condition removes the reduction that killed the original. Changing the ansatz, depth, optimiser, α schedule, shot count, qubit count or entanglement pattern alone is **never** material for these entries: all were varied or shown irrelevant (QX-05, QX-10, QX-33; `s31` Q16).

| # | Do not repeat | Killed by (type) | Materially different would require |
|---|---|---|---|
| DNR-01 | CVaR-VQE (or any variational circuit) on a **candidate-index register** (any n, any readout) | Theorem: prefix T1, closed-form p*, dimension counting; measurement: M6, p* substitution | Leaving the candidate-index encoding entirely |
| DNR-02 | Any quantum optimiser of a **diagonal** cost whose output is consumed only through **argmin, an energy-order prefix or a convex functional** of the output distribution | Theorem: solver-equivalence (R2), T1 (R1), R4 | A readout that uses the full distribution *and* a measured reason why classical samplers cannot produce that distribution |
| DNR-03 | Quantum search on **enumerable registers** (≤ ~2^24 states at simulator speed) | Measurement: A60, A51, A10, QX-04, E230 | A register that is provably non-enumerable at the target sizes |
| DNR-04 | **CVaR-tail ensembles** as readouts | Theorem (tail collapse, R3) + measurement (E306; the SA tail is equally concentrated) | A non-CVaR objective with a diversity guarantee (for which classical twins also exist) |
| DNR-05 | VQE-vs-SA comparisons at **equal budget but unequal tuning** | Methodology (E406 → E406V/E1001) | Never admissible. Equal tuning effort is mandatory. |
| DNR-06 | Claims of VQE advantage **without a random-prior-sampling twin** (same warm-start prior, same budget) | Measurement: random beat VQE on the chain (E1006/E1007, E518V, M adversary) | Never admissible. This twin is mandatory for any register search. |
| DNR-07 | Structural register search against a **continuous decoder that is already restart-saturated** | Theorem R10 + measurement E800b (saturation at 32–64 restarts) | A measured search gap: decoder − information floor growing with length and not closed by restarts |
| DNR-08 | Registers whose energy fails **condition C on the readout energy** (lower energy after relaxation ⇒ lower RMSD, in band) | Measurement: A30, A51, A20.0, E100, E604, E901, E903; D attack (raw → polished ρ 0.00) | Condition C passing on the readout energy, pre-checked before any build |
| DNR-09 | **Non-diagonal Hamiltonians on candidate registers** (similarity/compatibility couplings, mean-field diag(â) − B) | Theorem: stable-rank law, dimension counting; measurement: lane B gate | A register whose dimension grows exponentially with protein size |
| DNR-10 | **Tempered Born machine / Gibbs-readout circuits on spaces where exact enumeration or Metropolis mixes quickly** | Measurement: A71 (Metropolis 9/10), A70 (Gibbs readout NOT A RESULT on the chain) | A measured MCMC mixing failure on the target distribution (see the opportunity map) |
| DNR-11 | Transverse-field mixers on small configuration spaces as a "non-commuting" escape | Measurement: QX-04 (flattening to \|+⟩^q; BESTOFN ties) | Non-commuting terms that encode problem information, not a generic mixer, with C2 verified |
| DNR-12 | Index / encoding redesign; Gray codes; register widening without a selector | Measurement: QX-12, QX-13 | A deployable selector with in-band skill, which does not exist |
| DNR-13 | Endogenous-order (halfspace / quadric) tail lifts | Measurement + order-statistic nulls: QX-07 | "A rule that produces a direction, not a larger search over directions" (`s30` Q5) |
| DNR-14 | Finite-shot CVaR bias as a mechanism | Measurement: QX-08 | Low shot or low α regime (the closure lapses there) |
| DNR-15 | Tuning **one global scalar** (typicality, PC1 step, prefix m, profile, filter width, scale) at 9–16 aa | Measurement: `s29` B22; `s30` C6; `s31` D2 | Never. A global scalar cannot carry per-target information. |
| DNR-16 | Native-free **in-band ranking / recognition** at 9–16 aa from single-structure geometry, physics scorers, chiral functionals, consensus or sign predictors | Theorem (G1, Neyman–Scott, perception–distortion) + measurement | A new *information source*: not a new scorer on the same inputs |
| DNR-17 | Transferring long-length mechanisms (ESM priors, decoders, loglik selectors) to 9–16 aa | Measurement: all harmful (`s33` N2–N8) | Short-length-specific training data or signal |
| DNR-18 | Classical-solver problems dressed as quantum (SOCP, QP/hull projection, sparse s-of-K, set selection via QUBO) | Theorem: convex / polynomial (QX-14–16; `s30` Q6) | None. These are solved classically. |

## Part 3. What the negatives do **not** show (I(prog))

- No experiment in S29–S33 tested a quantum algorithm with a **known asymptotic separation**: amplitude estimation, quantum walks, QMCMC spectral-gap speedups, Hamiltonian simulation or QSVT.
- No experiment measured **classical sampling hardness**: mixing times or gaps.
- No experiment went **beyond 60 aa**.
- No experiment used hardware or estimated fault-tolerant resources.
- The negatives therefore close the *predecessor's formulation class* (H-001). They do not close quantum computing for protein structure. They do shift the burden of proof: any new proposal must show a computational gap classically *before* building a quantum component.
