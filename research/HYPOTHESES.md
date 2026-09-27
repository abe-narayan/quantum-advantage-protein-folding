# Hypotheses

Registry of scientific hypotheses. Each entry gets an ID (`H-###`), a statement, a claim category (see the charter taxonomy), predictions, a kill criterion, linked experiments and a status (OPEN / SUPPORTED / KILLED / SUPERSEDED). Killed hypotheses stay here and are cross-referenced in `KILLBOOK.md`.

## Inherited hypotheses (predecessor S29–S33): status as recorded in source

These were tested in the predecessor project. They are listed so they are not re-tested unknowingly. The status is the source's own label, and details and citations are in `research/sprintNN/`. They have not been re-tested in this repository.

| Source ID | Statement (source terminology) | Status in source | Where |
|---|---|---|---|
| S29 charter constraint | "Removing or randomizing the quantum stage measurably degrades the result." | Not satisfied: the deployed arm is indistinguishable from a fixed profile (S29-L55) | `sprint29/QUANTUM_RESULTS.md` |
| S29 F5b / tail-then-aggregate | The TTA VQE endpoint improves on production | REFUTED (S29-L54) | `sprint29/NEGATIVE_RESULTS.md` |
| S29 PREREG_B, bright line B1 | The compatibility Hamiltonian improves ordering | REFUTED (S29-L11) | `sprint29/NEGATIVE_RESULTS.md` |
| S30 quadric / second-moment escape | A non-diagonal (quadric) objective escapes T1's prefix result | Closed before any Hamiltonian was built (S30-L12, L15) | `sprint30/QUANTUM_RESULTS.md` |
| S31 CVaR objective solved exactly | Solving the deployed CVaR objective exactly (p*) improves the chain | Null (S31-L4, L20); the circuit was worse than p* on 126/126 | `sprint31/QUANTUM_RESULTS.md` |
| S32 charter §14 | A quantum component can matter on this instrument | "NO on this instrument"; the binding reason is chain length (S32-L(Q3)) | `sprint32/QUANTUM_RESULTS.md` |
| S33 H-Q1 | The posterior-mean readout of a tempered Born machine beats argmin and classical ensembles | FALSIFIED (E700, R60); the circuit is dominated by its Metropolis twin (E710) | `sprint33/QUANTUM_RESULTS.md` |
| S33 D_decoder (a)/(b) | CVaR-VQE global search over a learned energy is load-bearing | (a) FAILS, SURVIVES attack; VQE ties random prior sampling | `sprint33/QUANTUM_RESULTS.md` |
| S33 H_hybrid | The A41 energy advantage survives to the built chain | NOT load-bearing (E1000–E1007); the energy win was an SA-tuning artefact | `sprint33/QUANTUM_RESULTS.md` |
| S33 next step (S34-A01) | esmprior_v2 + A80 + template gate, with a pre-registered quantum re-test (A82) | Proposed only, never run | `sprint33/README.md` H8 |

## Hypotheses of this program

None are pre-registered yet. The following are **PROPOSED** working framings drawn from the import. They need sharpening, a kill criterion and pre-registration before any experiment.

### H-001 (PROPOSED): the predecessor's quantum null is structural, not tuning-related
- **Statement:** In the predecessor's formulation, a diagonal cost Hamiltonian over enumerable registers with an argmin or CVaR-prefix readout, no quantum primitive can be load-bearing. The reason is that the stage reduces exactly to a classical sort or argmin. This follows from the set-equality/T1, solver-equivalence and enumerability arguments.
- **Claim category:** 6, theoretical. It is a negative claim about the formulation.
- **Prediction:** Any architecture that keeps these three properties will pass the ablation test with no capability loss, whatever the ansatz, optimiser or qubit count.
- **Kill criterion (draft):** A pre-registered FULL-vs-ABLATION contrast within this formulation class that loses a capability when the quantum component is removed, against an equally tuned classical twin.
- **Status:** PROPOSED. It needs a formal restatement in `theory/`.

### H-002 (PROPOSED, competes with H-001 as the program's explanation): the binding bottleneck is information, not computation
- **Statement:** At the lengths studied, the limit on accuracy is missing native-free information, such as long-range pair distributions or the per-target sign. It is not search, sampling or optimisation difficulty. If so, no computational primitive, quantum or classical, will move the endpoint without new information.
- **Source basis:** S33 REPORT §1.7; S32 Q1-T1/T2; S30 H3; S29 L_8. These are interpretations in the sources.
- **Consequence for this program:** A quantum-advantage search should target a sub-problem whose hardness is computational (sampling, estimation, simulation). It should not target structure-selection accuracy on inputs already limited by information.
- **Status:** PROPOSED.
