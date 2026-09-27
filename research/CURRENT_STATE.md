# Current State

_Last updated: 2026-09-27 (discovery sprint in progress)_

| Field | Value |
|---|---|
| Current research question | Is there a real place where quantum computation does something important for protein structure that the best classical approach cannot do as efficiently? If not, where and why does it fail? |
| Phase | **Discovery sprint (in progress).** Infrastructure committed (4036d44). Theory T1–T5 written and skeptic-revised (research/theory). Discovery workflow: 28 candidate mechanisms generated, deduplicated and attacked from three lenses; synthesis pending. Experiments G1 (learned-posterior sampling), Q4 (cooperativity) and C1 (NMR hardness–identifiability) are pre-registered (`experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`) and running under the governor. |
| Strongest hypothesis | **H-C1 (Program C):** protein ¹H dipolar spin dynamics carry structural Fisher information past the failure time of the best classical approximation, so a quantum forward model saves repetitions or identifies parameters a classical inversion cannot. Prior art: O'Brien et al., PRX Quantum 2022 (`discovery/NOVELTY_MEMOS.md` NM-1). |
| Strongest competing hypothesis | H-C1-null: in the classically hard (ergodic) window the information is degenerate or destroyed by dephasing (O'Brien's ergodicity finding). Structure is then identified from early-time data that classical models reproduce. |
| Status of the sampling route (H-006, QM-01…13) | **Killed at the practical level** by every attack lens so far: quadratic ceiling (T5) and break-even ≥ 1e12–1e22 classical evaluations per sample (T2/T3) against measured costs of 1e5–1e6. Pilots show real classical difficulty (unsaturated mode census at L ≥ 100; first-order-like λ-path bottleneck; zero NRPT round trips). Transmission is weak (ρ(E,RMSD over modes) = 0.31 at L=120). Production G1 runs are still confirming the kill criteria. |
| Current best quantum architecture | None load-bearing. Candidate: quantum forward simulation of the protein ¹H dipolar network (Trotterised secular dipolar Hamiltonian, 2-point transfer and OTOC echoes), pending C1. |
| Current strongest classical baseline | Structure: inherited (not reproduced). Sampling: NRPT + HMC + pivot moves; multistart L-BFGS census. NMR: panel of weight-w Pauli propagation, sparse Pauli dynamics (ε), sub-cluster exact, classical-spin dynamics. |
| Current best result | Instruments: sector-exact deterministic NMR reference (1e-15 agreement with the dense matrix, 200× faster). NMR smoke evidence (N=8): OTOC observables carry 10–40× the Fisher information of 2-point transfer, and classical models fail on them earlier (not yet a result). |
| Running experiments | Governor (`research/results/RAW/master/`): NMR v2 grid (N=10 × 6 probes × 2 orientations × γ∈{0,1000,5000}; N=12; N=14 γ=0), mode census L=120/150, 2048-restart census, λ-path T-scan, temperature exchange, synthetic lab. |
| Compute note | Workflow agents' own checks ran outside the governor and pushed CPU above 95% for stretches. Governed jobs were throttled to compensate. Suspending agent processes was refused by the permission classifier and is not done. |
| Current Git checkpoint | 4036d44 (infrastructure). Later work uncommitted: theory T1–T5, prereg, NMR v2 instrument, discovery memos. |

## Where things are

- **Discovery:** `research/discovery/` (NOVELTY_MEMOS so far; the other files follow the workflow synthesis).
- **Theory:** `research/theory/PROOFS/` (T1 reduction, T2 sampling speedup + break-even, T4 amplified mode finding), `NO_GO_RESULTS/T5_quadratic_ceiling.md`, `RESOURCE_MODELS.md` (T3 Toffoli costs).
- **Pre-registration:** `research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md` (with deviation log).
- **Code:** `src/qapf/protein` (vendored A80/esmprior_v1, ladder instrument), `src/qapf/sampling` (NRPT, T-exchange), `src/qapf/nmr/spins.py` (exact, sector-exact, Pauli, classical-spin), `src/qapf/synthetic`, `scripts/`.
- **Literature, map and inherited evidence:** as before (`research/literature/`, `QUANTUM_OPPORTUNITY_MAP.md`, `sprint29…33/`).
