# Open Questions

Questions that are not yet sharp enough to be hypotheses. Promote them to `HYPOTHESES.md` when they become testable. The scientific open problems inherited from the predecessor are catalogued in `research/sprint29-33/OPEN_PROBLEMS.md` (OP-ids).

_Updated 2026-09-26 after the S29–S33 reconstruction._

## Program-level

- **Which bottleneck in protein structure computation is genuinely computational, with a measurable gap, as opposed to information-limited?**
  - Current candidates, none with a measured gap: posterior sampling at length (→ H-003), search beyond 60 aa (→ H-004), variance-limited estimation (→ H-005). See `QUANTUM_OPPORTUNITY_MAP.md` §1.
- **What is the right long-chain instrument?**
  - Needs targets at 60–150 aa with leakage controls at least as strict as esmprior_v1's R3 rule and cross-fold homologue exclusion (`sprint29-33/OPEN_PROBLEMS.md` §D).
  - Open sub-questions: the source dataset, split design, and whether the predecessor's `prots/` corpus suffices.
- **Which classical samplers define "the strongest classical twin" for continuous CA-trace posteriors?**
  - Candidates: PT, replica exchange, SMC, HMC, and random-prior + relaxation (which beat CVaR-VQE).
  - The choice must be made and tuned *before* any quantum comparison.
- **How should mixing be measured so that it maps onto quantum-walk / QMCMC resource models?**
  - Options: spectral-gap estimates vs integrated autocorrelation vs round-trip times.
  - The literature bridge is needed in `LITERATURE_MAP.md`.
- **Does soft (Boltzmann-weighted) readout from a converged ensemble beat argmin/decoder output at long40 and beyond?** (OP-08; a precondition for H-003's value clause.)

## Inherited, still open (details in OP-ids)

- Is the S33 topology-trap asymmetry (VQE fewer traps than tuned SA, p 0.015) real and reproducible, or a seed/definition effect? (OP-05; low priority, because the random prior sampler dominated both.)
- Is the long-length decoder near its information floor on more than 6 targets and on the chain basis? (OP-02; this feeds H-004.)
- Is there any per-residue non-separable discrete decision at ≥ 40 aa whose ORACLE ceiling is not an order statistic? (OP-06)
- Would A82 survive its own pre-registered kill rules? (OP-03; run only if H-004 opens a search gap.)

## Answered by the reconstruction (kept for history)

- ~~Which parts of the Sprint 33 conclusions survive independent reconstruction?~~ All six points of the user's summary are consistent with the source, with two qualifications (`SCIENTIFIC_MEMORY.md`, 2026-09-26). The synthesis is in `research/sprint29-33/`.
