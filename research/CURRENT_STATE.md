# Current State

_Last updated: 2026-09-26 (literature phase complete)_

| Field | Value |
|---|---|
| Current research question | Where, if anywhere, does a quantum primitive provide a defensible advantage for protein structure computation? (See charter.) |
| Phase | **Literature phase complete.** Reconstruction → opportunity map v1 → literature review → opportunity map v2. No experiments run in this repository. Next: theory (T1, T2) and pre-registration of the classical gate G1. |
| Strongest hypothesis | H-002 (working prior): at ≤ 60 aa the endpoint is information-limited. The literature reinforces it: single-structure prediction is information-limited [E89, E100]. |
| Strongest competing hypothesis | **H-006:** sampling a learned-energy structure posterior becomes classically hard at 60–150 aa **and** sampled soft readouts transmit to accuracy. This is the only route by which a quantum primitive (walk/QSA/continuous sampler, quadratic, fault-tolerant) could matter. |
| Theory under development | H-009 (generalised H-001 reduction theorem); H-008 (fault-tolerant break-even B(L)); H-007 (landscape persistence). See `THEORY_ROADMAP.md` T1–T5. |
| Current best quantum architecture | **None.** Literature and inherited evidence contain no load-bearing quantum component for protein structure. Candidates M1/M2 are INTERESTING-conditional on G1–G3 (`literature/OPPORTUNITY_MATRIX.md`). |
| Current strongest classical baseline | Structure accuracy (inherited, not reproduced here): tuning126 3.2105 Å; long40 E308 4.739 / A80 4.343; mid30 A80 3.717 / 3.815. **Sampling twin portfolio** for any quantum sampling claim: PT/REST2 + HMC, SMC/PERM-type, learned-proposal MCMC, amortised generator as an independence proposal, each with equal tuning effort. |
| Current best result | None in this repository. |
| Strongest counterevidence | Against quantum advantage generally: quadratic speedups fail fault-tolerant break-even [A56, B46]; funnelled landscapes and PT [E2–E6, E33]; the quantum-folding literature has no load-bearing result [D §10]; 33 inherited nulls. Against H-002 at length: only I-5 (6 targets); nothing is known beyond 60 aa. |
| Running experiments | None |
| Next experiments | **Gate G1** (HIGH PRIORITY, classical): the mixing-cost scaling of the best classical portfolio on a learned-energy Cα posterior vs L, with sampled soft-readout transmission and a landscape census (H-006/H-007). **In parallel, G2** (HIGH PRIORITY, paper): the fault-tolerant resource estimate of a coherent learned-energy walk operator → B(L) (H-008). **Prerequisites:** T1/T2 theory notes; pre-registration in `experiments/preregistered/`; a long-chain (60–150 aa) leakage-controlled instrument; access to an esmprior-class learned energy. |
| Current Git checkpoint | See `git log`. Last commit: literature phase. |

## Where things are

- **Literature:** `research/literature/`: LITERATURE_REVIEW (entry point), QUANTUM_PRIMITIVES, CLASSICAL_COUNTERARGUMENTS, PROTEIN_BOTTLENECKS, QUANTUM_ADVANTAGE_CLAIMS, OPPORTUNITY_MATRIX, OPEN_LITERATURE_GAPS, BIBLIOGRAPHY.
- **Plan:** `research/THEORY_ROADMAP.md`.
- **Map:** `research/QUANTUM_OPPORTUNITY_MAP.md` (v1 plus the v2 literature update, which governs).
- **Inherited evidence:** `research/sprint29/` … `research/sprint33/` (evidence of record) and `research/sprint29-33/` (synthesis).
- **Gate rule:** no quantum build until a classical kill test has failed to kill the item **and** the break-even B(L) is stated.

## Open logistics

- **Long-chain instrument (60–150 aa).** It does not exist yet. It needs leakage rules at least as strict as esmprior_v1's R3 rule plus cross-fold homologue checks.
- **Learned energy.** The esmprior_v1 model and ESM-2 features live in the predecessor repo (read-only). Either reuse them under an explicit provenance record or retrain. RAM was the binding constraint in S33 (ESM-2 650M features).
- **Classical baselines.** The inherited baselines have not been reproduced in this repository.
