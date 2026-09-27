# Current State

_Last updated: 2026-09-26 (S29–S33 reconstruction and Quantum Opportunity Map v1)_

| Field | Value |
|---|---|
| Current research question | Where, if anywhere, does a quantum primitive provide a defensible advantage for protein structure computation? (See charter.) |
| Phase | **Reconstruction complete; opportunity map v1 exists.** No experiments run in this repository. Next phase: classical kill tests and theory (the gate rule applies). |
| Strongest hypothesis | H-002 (PROPOSED, working prior): at ≤ 60 aa the endpoint is information-limited; no computational primitive moves it without new information. |
| Strongest competing hypothesis | H-003 (PROPOSED): classical sampling of learned-energy structure posteriors becomes hard with length **and** better samples improve the chain. This would open AA-1 (quantum-walk/QMCMC gap speedup). |
| Structural hypothesis under formalisation | H-001 (PROPOSED): argmin/prefix/convex-consumed quantum stages over diagonal costs are classically reproducible. It explains all 33 inherited quantum nulls. |
| Current best quantum architecture | **None.** No inherited quantum architecture was load-bearing (QX-01 … QX-33). Candidates exist only on the opportunity map, all conditional on classical kill tests. |
| Current strongest classical baseline | Inherited, **not yet reproduced here**: tuning126 production 3.2105 Å; long40 E308 4.739 / A80 4.343 (tie); mid30 A80 3.717 ungated / 3.815 gated. All built chain, DEP, and quantum-free. The strongest classical *twins* for quantum comparisons: equal-tuning SA, random prior sampling, register-free decoder, Metropolis/PT. |
| Current best result | None in this repository. |
| Strongest counterevidence | Against any quantum role in the predecessor's formulation class: 33 records, 12 reduction results, 13 inherited kills (`KILLBOOK.md` K-001 … K-013). Against H-002 at length: only that I-5 rests on 6 targets on the cloud basis, and nothing was measured beyond 60 aa. |
| Running experiments | None |
| Next experiments | PLANNED, **none started**, and each needs pre-registration first. Ranked (from `QUANTUM_OPPORTUNITY_MAP.md` §8): (1) H-001 derivation in `theory/`; (2) sampling-hardness characterisation vs length on a new leakage-controlled long-chain instrument (H-003); (3) search-gap scaling beyond 60 aa (H-004); (4) variance audit of ensemble decisions (H-005); (5) A82 only if (3) opens a gap. Parallel prerequisite: `LITERATURE_MAP.md` for QMCMC / quantum-walk mixing speedups, amplitude estimation, and quantum backtracking resource models. |
| Current Git checkpoint | See `git log`. Last commit: S29–S33 reconstruction and opportunity map. |

## Where things are

- **Evidence of record (per sprint):** `research/sprint29/` … `research/sprint33/`, imported read-only from `cvar-vqe-protein-folding-v3@3d5b2d25`.
- **Synthesis:** `research/sprint29-33/`: README (state, R1–R12), QUANTUM_RESULTS (QX-01 … QX-33), ARCHITECTURE_EVOLUTION, NEGATIVE_RESULTS (+ DNR registry), OPEN_PROBLEMS (OP / EI ids).
- **Map:** `research/QUANTUM_OPPORTUNITY_MAP.md`.
- **Gate rule:** no quantum build until a classical kill test has failed to kill the item.

## Open logistics

- A long-chain (60–150 aa) instrument does not exist yet. Designing it, with its leakage rules and splits, is a prerequisite for H-003 and H-004.
- The inherited classical baselines have not been reproduced in this repository. Reproduction is needed before any comparison is claimed against them.
