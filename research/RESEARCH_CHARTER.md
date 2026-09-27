# Research Charter

_Established 2026-09-26. This file is amended by dated addenda. Earlier text is never silently rewritten._

## Central question

> Where, if anywhere, can quantum computing provide a real, testable, scientifically defensible advantage for protein structure computation?

"Nowhere, in the regimes we tested, for these reasons" is a legitimate and valuable outcome.

## Scope

The program is algorithm-agnostic and architecture-agnostic. Candidate quantum primitives include, and are not limited to:

VQE; QAOA; adaptive VQE / ADAPT-style methods; quantum walks; amplitude amplification; amplitude estimation; quantum sampling; Gibbs-state preparation; quantum Metropolis-style methods; quantum imaginary-time evolution; Hamiltonian simulation; QSP/QSVT; quantum generative models; quantum Boltzmann methods; tensor-network/quantum hybrids; fault-tolerant quantum algorithms; entirely new formulations.

The whole protein-folding architecture may be replaced. The target is a **computational bottleneck** where a quantum primitive genuinely matters.

## Historical context

The predecessor repository, *Protein-Folding-Algorithm*, ran Sprints 1–33 around a CVaR-VQE pipeline. Sprint 33 found that the quantum stage was not load-bearing (details in `SCIENTIFIC_MEMORY.md`). That project supplies validated baselines, negative results, benchmark definitions, leakage controls, infrastructure and lessons. It does not supply an architecture to preserve.

## Claim taxonomy

Every claim must declare one category:

| # | Category | Minimum evidence (initial working definition, to be refined in `theory/quantum_advantage/`) |
|---|----------|------|
| 1 | Quantum usefulness | The quantum component contributes measurably in FULL vs. ABLATION. It need not beat the best classical method. |
| 2 | Empirical quantum advantage | Beats the strongest tuned classical twin on a pre-registered metric, with uncertainty, replication and a clean leakage audit |
| 3 | Computational/resource advantage | Better scaling or cost in an accounted resource (evaluations, time, memory), with simulator cost separated from projected physical cost |
| 4 | Sampling advantage | Samples a target distribution better or more cheaply than the classical samplers, using a defined distributional metric |
| 5 | Hardware advantage | Demonstrated on physical quantum hardware under stated noise and mitigation assumptions |
| 6 | Theoretical/provable advantage | A complexity or query-complexity separation under stated assumptions |

Lower RMSD, more qubits, a larger Hilbert space, a faster simulator, fewer optimizer iterations or a "more interesting" distribution are not advantage by themselves.

## Method

**Classical twin.** Each quantum architecture has a seriously tuned classical counterpart (SA, parallel tempering, MCMC, replica exchange, SMC, beam search, evolutionary search, multistart, branch-and-bound, exact enumeration, tensor networks, problem-specific combinatorics, efficient vectorized/multiprocess implementations).

**Quantum necessity test.** FULL (classical + quantum) vs. ABLATION (the strongest classical replacement for the quantum component). The question is what capability disappears without the quantum component. If nothing important disappears, the architecture is killed or redesigned.

**Leakage.** Native structures are allowed only for final evaluation, labeled ORACLE diagnostics and scientific analysis. They are never allowed in production optimization, hyperparameter or candidate selection, training, oracle construction, or test-driven algorithm selection. DEP and ORACLE stay distinct.

**Resource accounting.** Wall-clock, CPU time, peak RAM, objective and candidate evaluations, qubits, depth, gate count, two-qubit gate count, shots, measurements, state preparation, readout, classical pre/postprocessing, communication, simulator, compilation and error-mitigation overhead, and hardware assumptions. Simulator runtime is never physical runtime.

## Research cycle

READ → FORM HYPOTHESIS → PRE-REGISTER → IMPLEMENT → RUN → COMPARE → ATTACK → REPLICATE → SCALE → THEORIZE → DECIDE → KILL | ESCALATE

## Experiment ledger schema

Every substantial experiment records:

experiment ID · hypothesis · architecture · quantum algorithm · classical algorithm · target set · protein lengths · train/dev/test split · qubits · circuit depth · gate counts · shots · objective evaluations · wall time · CPU · RAM · RMSD · energy · sampling metrics · classical comparator · effect size · uncertainty · statistical test · replication status · leakage status · hardware assumptions · conclusion

(PLANNED: a machine-readable ledger format and location, to be decided when the first experiment is pre-registered.)

## Repository philosophy

This is a laboratory. Preserve negative results, failed hypotheses and raw metadata. Checkpoint with Git often, and commit before destructive redesigns.
