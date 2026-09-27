# Quantum Advantage Claim Audit

_Discovery sprint, 2026-09-26/27. Every major statement in `QUANTUM_ADVANTAGE_DISCOVERY_REPORT.md` is classified. Classes:_
- _**MEASURED**: produced by a run in this repository (RAW path given);_
- _**DERIVED**: proved or computed here from stated assumptions;_
- _**THEORETICAL**: a result from the literature, used as its authors state it;_
- _**LITERATURE-SUPPORTED**: an empirical claim from the literature;_
- _**INFERENCE**: reasoning from evidence, not a proof;_
- _**UNPROVEN**: stated but not established._

_"Exploratory" marks measurements that were not pre-registered or not replicated._

## A. Starting evidence and literature

| # | Statement | Class | Source |
|---|---|---|---|
| A1 | 33 predecessor CVaR-VQE experiments never moved the built-chain endpoint; SA and random prior sampling matched or beat them | MEASURED (predecessor; imported) | `research/sprint29-33/QUANTUM_RESULTS.md` |
| A2 | Single-structure accuracy at ≤ 60 aa is information-limited | INFERENCE (predecessor evidence) | H-002; `sprint29-33/README.md` |
| A3 | Every known quantum speedup for classical-energy protein tasks is at most quadratic, query-model, fault-tolerant | LITERATURE-SUPPORTED | `research/literature/LITERATURE_REVIEW.md` |
| A4 | Quadratic speedups fail early fault-tolerant break-even (QSA "a day and a million physical qubits" vs "four CPU-minutes") | THEORETICAL [A56, B46] | BIBLIOGRAPHY |
| A5 | O'Brien et al. 2022 proposed quantum learning of the protein dipolar Hamiltonian (ubiquitin) and found learnability only as dynamics turn non-ergodic | LITERATURE-SUPPORTED | arXiv:2109.02163 (abstract and HTML read) |
| A6 | Zhang et al. 2025 NMR OTOC geometry demo is "not yet beyond classical" | LITERATURE-SUPPORTED | [F34] |
| A7 | Liquid-state NMR spectra are reproduced by linear-scaling classical cluster methods | LITERATURE-SUPPORTED | Fratus et al. arXiv:2508.06448 (abstract) |

## B. Theory

| # | Statement | Class | Source |
|---|---|---|---|
| B1 | Dephasing-dominated quantum stages consumed via argmin / tail / convex programs are output-equivalent to classical simplex optimisation (H-001a) | DERIVED | T1 Thms 1–2 |
| B2 | Cost equivalence (H-001b) fails in the query model for implicit black-box E (quadratic) | DERIVED + THEORETICAL [C56] | T1 |
| B3 | QSA on the prior→posterior path gives a same-chain quadratic walk-step speedup | THEORETICAL [A7, A8, A31] + DERIVED (stage count) | T2 S1 |
| B4 | A first-order crossing changes Λ by 1 + O(s/ΔV) and needs one intermediate rung | DERIVED | T2 Lemma 2 |
| B5 | δ ≤ (8/p) e^{−ΔF‡} at a two-phase rung | DERIVED | T2 Prop. 3 |
| B6 | No landscape gives advantage at per-sample quantum wall-clock below T*_Q = Aρ(K n_b G t_T)²/c | DERIVED | T2 corollary |
| B7 | G(L) ≈ 2.9–3.6×10⁴·L² Toffolis per faithful walk step (D2 central, 22–25-bit fixed point) | DERIVED (under labelled assumptions A1–A15) | T3 |
| B8 | B* = 10¹⁰–10²⁵ classical evaluations/sample; T*_Q ≥ 0.26 yr (most optimistic) | DERIVED | T2 §4.3, T3 |
| B9 | Amplified multistart is quadratic only vs i.i.d. restarts; hardware gate fails at 170 µs for any energy-evaluating map | DERIVED | T4 |
| B10 | ≤ quadratic separation on information-local families with easy background; ≤ quadratic precision gains; no universal ceiling | DERIVED + THEORETICAL | T5 |
| B11 | Transfer = one Pauli coefficient (truncation-robust); echo = anticommuting weight of the whole operator (truncation-sensitive) | DERIVED | T6 |
| B12 | NMR echo forward model costs 2.5×10¹¹–9.6×10¹² T per evaluation (N = 14–466); ~11 h depth-limited; inversion ~11 yr per machine | DERIVED (product-formula costing; labelled inputs) | `research/theory/nmr_resource_model.py` |
| B13 | Worst-case BQP/DQC1 hardness of spin dynamics / infinite-temperature correlators does not transfer to the protein instance family | INFERENCE | COMPLEXITY.md |

## C. Program A (learned posterior)

| # | Statement | Class | Source |
|---|---|---|---|
| C1 | NRPT λ-path communication barrier Λ ≈ 13.6 (L=45) … 29.3 (L=150), 0 round trips in every pilot | MEASURED (PILOT, 1 seed, HMC-only) | `RAW/g1_pilot/` |
| C2 | The 0-round-trip deficit is significant at L=45 (P(0) ≈ 5×10⁻⁵ under ELE), marginal at L=60, uninformative at L ≥ 100 | DERIVED from MEASURED | T2 §4.1 |
| C3 | Mode census: distinct-mode fraction 0.32 → 0.98 and gmean p_hit 0.10 → 0.008 from L=30 to 120; unsaturated at L ≥ 100 | MEASURED (256 restarts, 200-iteration minima) | `RAW/g1_modes/`, `PROCESSED/g1_summary.json` |
| C4 | ρ(E, RMSD) over modes ≈ 0.31 at L=120; the best-RMSD mode ranks ~11th by energy | MEASURED (7 crops) | same |
| C5 | The A80 energy is piecewise smooth (0.05 Å table interpolation): L-BFGS endpoints keep gradient norms 2–130; Hessians have ~40% non-positive eigenvalues | MEASURED | R2-T deviation log |
| C6 | Distance-geometry seeding reaches the deepest known basin in 61/64 runs at 1–5% of restart/PT cost | MEASURED (exploratory lens run; not replicated) | `research/discovery/attack_records.json` QM-02 |
| C7 | Transmission of posterior averaging (R2-T) | ⟦R2T-CLASS⟧ | `RAW/g1_transmission/`, `PROCESSED/transmission_summary.json` |
| C8 | λ-path T-scan / temperature exchange / 2048 census | ⟦G1PROD-CLASS⟧ | `RAW/g1_tscan`, `RAW/tpt`, `RAW/g1_modes2k` |

## D. Program C (NMR forward model)

| # | Statement | Class | Source |
|---|---|---|---|
| D1 | Sector-exact solver agrees with the dense Heisenberg matrix to 1e-15 (with/without dephasing); shot-based circuit agrees within 1–2 SE | MEASURED | validation runs (session); `RAW/nmr_pop/` |
| D2 | Transfer S_ab: sparse Pauli dynamics (ε=10⁻⁴) reproduces exact to < σ over the full window at N=10: f_hard(best) = 0 (1UBQ, 1PGA; γ = 0, 10³, 5×10³; dilute HN networks) | MEASURED | `RAW/nmr_gate/`, `RAW/nmr_gate_hn/` |
| D3 | The pre-registered weight-4 statistic gives f_hard ≈ 0.99, a weak adversary | MEASURED | same |
| D4 | Echo (OTOC) F_ab: every sub-exponential classical truncation tested fails by 20–80 µs (dense) / 200–650 µs (amide-only) at N=10. The families: weight-w and ε ≥ 1e-4 Pauli, CCE to order N−3, operator-spreading/FKPP, stochastic Pauli, MPO χ ≤ 64, classical spins/DTWA. ε = 3e-5 sparse Pauli (≈ full operator space) and exact simulation (seconds) reproduce it. Echo FI is 3.2–183× transfer FI in the ideal isolated model; f_hard 0.49–1.0 vs the ε ≥ 1e-4 panel, median 0.00 vs ε = 3e-5 | MEASURED (2 proteins, several probes; adversarial replication) | `RAW/nmr_gate*`, `RAW/nmr_sparse`, `experiments/ADVERSARIAL/R1_*` |
| D5 | Scaling of the needed classical resource M*(N) (C2/C3) | ⟦C2C3-CLASS⟧ | `RAW/nmr_sparse/`, `PROCESSED/c2_summary.json` |
| D6 | Bath embedding (R1-E) | ⟦R1E-CLASS⟧ | `RAW/nmr_embed/` |
| D7 | Noiseless shot-based quantum echo circuit tracks the exact echo beyond the classical failure time at N=10 | MEASURED | `RAW/nmr_pop/` |
| D8 | Hardware-noise attack on the echo circuit | ⟦POP-CLASS⟧ | `RAW/nmr_pop/` |
| D9 | The protein's echo information would be measurable at σ = 0.01 per point with time-reversed dipolar sequences | UNPROVEN (supported only by the small-molecule precedent [F34]) | — |
| D10 | A coarse-grained operator-front (FKPP-type) classical model cannot reproduce the echoes | UNPROVEN (untested adversary) | T6 §4 |

## E. Decisions

| # | Statement | Class |
|---|---|---|
| E1 | 28/28 candidate mechanisms are killed as quantum-advantage claims for protein structure computation | INFERENCE, from DERIVED kills (theorems, break-even) and exploratory MEASURED lens checks |
| E2 | No claim above practical L0 is supported | INFERENCE |
| E3 | Final claim level | ⟦E3⟧ |
