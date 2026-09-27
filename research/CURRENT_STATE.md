# Current State

_Last updated: 2026-09-26 (predecessor S29–S33 evidence imported)_

| Field | Value |
|---|---|
| Current research question | Where, if anywhere, does a quantum primitive provide a defensible advantage for protein structure computation? (See charter.) |
| Strongest hypothesis | H-001 (PROPOSED, not pre-registered): the predecessor's quantum null is structural. A diagonal Hamiltonian over enumerable registers with an argmin/CVaR-prefix readout reduces to a classical sort. |
| Strongest competing hypothesis | H-002 (PROPOSED): the binding bottleneck at the studied lengths is information, not computation, so no computational primitive moves the endpoint without new information. |
| Current best quantum architecture | None in this repository. Predecessor: no CVaR-VQE design was load-bearing in S29–S33 (`sprint33/QUANTUM_RESULTS.md`). |
| Current strongest classical baseline | None run here. Predecessor references (imported, not reproduced): tuning126 production 3.2105 Å; long40 E308/A31.2 4.739 and A80 4.343 (tied); mid30 A80 3.717 ungated / 3.815 gated. All built chain, DEP, and quantum-free (`sprint33/README.md` H1–H3). |
| Current best result | None. No experiments have been run in this repository. |
| Strongest counterevidence | Against any quantum role in the old formulation: S29–S33 (see `SCIENTIFIC_MEMORY.md`, 2026-09-26 cross-sprint entry). Against H-001 as a *general* claim: none yet, but it has only been shown for the predecessor's formulation class. |
| Running experiments | None |
| Next experiments | PLANNED, and none started: (1) formalise H-001 in `theory/` (formulation-class conditions under which a quantum stage reduces to classical sort or argmin); (2) literature research into `LITERATURE_MAP.md`, focused on computational (sampling, estimation, simulation) sub-problems of structure computation; (3) architecture discovery against the three screening conditions in `SCIENTIFIC_MEMORY.md`. |
| Current Git checkpoint | See `git log`. Last commit: import of the S29–S33 evidence. |

## Imported evidence

- `research/sprint29/` … `research/sprint33/`: four files each (README, NEGATIVE_RESULTS, QUANTUM_RESULTS, LESSONS), imported 2026-09-26.
- **Source:** the predecessor repo at `C:\Users\abena\cvar-vqe-protein-folding-v3` (GitHub `abe-narayan/cvar-vqe-protein-folding-v3`), commit `3d5b2d25`. It was only read. The S29 contract says the work originally ran in the `Protein-Folding-Algorithm` repository, branch `s26`.
- **Not imported:** sprints before S29, `docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` (these have no S29–S33 content), code, and data.
- **Source discrepancies:** logged, unresolved, in each sprint's `LESSONS.md` importer notes.
