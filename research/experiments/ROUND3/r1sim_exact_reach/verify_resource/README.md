# Resource audit of `r1sim_exact_reach`: can exact classical simulation reach the converged late-window ¹H echo?

_ROUND3 adversarial verifier, resource lens, 2026-09-28._

**Claim under attack.** The lane r1sim_exact_reach says SUPPORTS for a Category-3 physics-simulation statement:
exact classical simulation cannot reach the converged late-window (240–320 µs) first-order dipolar echo F_ab(t) of
the dense 1UBQ ¹H network. Its numbers are:
- exact frontier N ≈ 26 (workstation, 1 day), 32–34 (GPU or GPU node, 1 day), ≤ 48 (exascale, 1 month);
- spins needed: ≥ 58 under the "optimistic" exponential model, 300–557 under the 1/N model.

Tags: MEASURED (file in this folder), DERIVED, LITERATURE (arXiv abstract verified this session), INFERENCE, UNPROVEN.

## Verdict: REFUTED as a resource or break-even claim. The correct status is INCONCLUSIVE; R1-SIM stays OPEN.

Four parts of the lane's work survive this audit:
- the lane's code, its validations and its N = 20 measurement (I replicate it independently, §2);
- the exact 1/N identity;
- the lane's own frontier arithmetic, reproduced exactly (the machine assumptions behind it need a +2-spin correction, §3);
- the statement "N = 20 is unconverged at p19 320 µs and p245 160 µs".

A fifth survives and is strengthened by my new N = 22 point (§0): the late window is **still unconverged at N = 22**.

What does not survive is **"exact classical simulation cannot reach the converged echo"** as an established fact, and
therefore any break-even. The reasons, all detailed below:
1. **The spins needed are still not identified** (§0, §4).
   - Before N = 22, the lane's "≥ 58, optimistic" came from the worst-fitting member of its own model family.
     Better-fitting refits gave 18–23 spins.
   - My measured F₂₂ rules out that fast-convergence reading (predicted 0.239, measured 0.228).
   - With N = 22 included, the model spread is still **26–45 (exponential variants), 57–65 (1/N²), 350–430 (1/N)**, and
     F_∞ ranges over 0.03–0.21, which is 18σ wide.
2. **The frontier is understated by about 2 spins** (§3). A 50-qubit universal simulation already exists
   (arXiv:2511.03359). With the correct exascale memory, the lane's own cost model gives N_max = 50 per month and 52 in
   about 40 days. That frontier falls inside the model spread of the spins needed.
3. **Break-even against exact classical simulation sits at N\* ≈ 48–52 per curve on an exascale machine** (§5). One
   fault-tolerant QPU takes 1 day (1 µs T layer) to 191 days (170 µs) per curve there. A quantum-only regime exists only
   if N_needed > 50–52. That is plausible, since the 1/N and 1/N² fits say so, but it is not shown.
4. **Exact simulation is the wrong comparator for a resource claim** (§6). The quantum estimator is itself a
   σ-accurate estimate, not an exact one. The best classical method at σ = 0.01 (finite-size extrapolation, cluster
   methods, hydrodynamic correction of the conserved part) is untested at N ≥ 22. The lane's own 1/N branch implies
   that F_∞ can be obtained by extrapolation, so exact reach would not be needed.
5. **The quantum side needs the same N** (§5). The 1/N term belongs to the finite model, not to the simulator. On the
   1/N branch the quantum machine needs about 350–629 logical qubits (629 is all of 1UBQ's ¹H) and 1e14–4.5e14 T per
   curve, at 1–2 weeks (1 µs T layer) to 4–7.6 years (170 µs) per curve. NISQ is excluded: ln(fidelity) is between −180 and −190 000.

Claim levels: theoretical **L0–L1** (no separation; instance-level exponential cost of one exact method). Practical
**L0** (no credible break-even against the best classical method; the quantum side is fault-tolerant only).

## 0. New exact point: N = 22, p19, site 8, 320 µs (MEASURED; `runs/pplus_1UBQ_p19_N22_site8_seed2026.json`, `n22_summary.json`)

**F₂₂ = 0.2282 ± 0.001** (typicality ≈ 2·2⁻¹¹). Run details:
- single-site P₊ estimator on the lane's reference circuit;
- complex64, flip-folded, all 12 folded sectors;
- 2029 CPU-s in 4 checkpointed chunks, peak RSS 0.84 GB.

| model (fitted on the lane ladder N = 12–20) | predicted F₂₂ | measured − predicted |
|---|---|---|
| lane exponential, all 5 points (source of "N_σ = 82") | 0.202 | **+0.026** (excluded) |
| c/N through the origin | 0.223 | +0.005 |
| 1/N with offset, last 3 | 0.233 | −0.005 |
| 1/N² with offset, last 3 | 0.236 | −0.007 |
| exponential without N = 14 (best fit before N = 22; "N_σ ≈ 23") | 0.239 | **−0.011** (excluded, about 8× noise) |

- **Still unconverged.** |F₂₂ − F₂₀| = 0.0169 (vs lane F₂₀) / 0.0182 (vs this audit's F₂₀), above the single-site
  pre-registered threshold σ + 2(err₂₀ + err₂₂) = 0.0147. F·N = 4.59, 4.88, 4.90, 5.02 at N = 16–22, so the drift is
  close to c/N.
- **Refits with N = 22** (`n22_summary.json` → `refits_with_N22`):

  | model | N_σ | F_∞ | rms |
  |---|---|---|---|
  | exponential, drop N = 14 | 26 | 0.21 | 0.47σ; ξ grew from 4.0 to 4.8, the classic receding-convergence sign |
  | exponential, all 6 points | 45 | — | 2.4σ |
  | 1/N², N = 18–22 | 65 | 0.14 | 0.07σ |
  | 1/N², N = 16–22 | 57 | — | — |
  | 1/N, N = 18–22 | 428 | 0.03 | 0.12σ |
  | 1/N, N = 16–22 | 352 | — | — |

- **What it settles.** N = 22 removes the "converged by 22–26" alternative this audit raised, and moves the evidence
  toward the lane's direction. It does not identify N_needed: 26–430 remains open.
- **The sector-resolved echo drifts most at intermediate magnetisation.** Relative to N = 20 at the same offset from
  half filling, f_k falls by 0.009 at the centre and by up to 0.070 at offsets of 5–7. So the drift is not a
  central-sector artefact.
- **Bottom line.** It sits on the classical side of the ledger: it is a MEASURED datum. The resource conclusions
  below still hold.

## 1. What I checked and re-ran

| item | how | result |
|---|---|---|
| Lane cost model and frontier | `resource_audit.py` §A, lane assumptions | reproduced exactly: 26 / 28 / 32 / 34 / 46 / 48 (MEASURED arithmetic) |
| Production kernel speed, N = 20, central sector, complex64, now | `resource_audit.py` §F | 0.105 s per step = **6.0 ns per pair-element** (lane: 7.3–7.6) (MEASURED) |
| Echo estimator | new `pplus_echo.py`: single site, one vector per sector (below) | exact to **7e-14 / 4e-13** vs dense sector unitaries at N = 10 (MEASURED) |
| Lane's N = 20 values (p19, site 8) | `pplus_echo.py`, independent code and random vectors, 202 CPU-s | **0.5083 / 0.2464** vs lane 0.5108 / 0.2451 at 160 / 320 µs; Δ = 0.0025 / 0.0013, within typicality noise ≈ 0.002 (MEASURED) |
| Robustness of the spins-needed estimate | refits of the lane's ladder (leave-one-out, subsets, 1/N²) | §4 |
| Decisive discriminator | `pplus_echo.py` N = 22, p19 site 8, 320 µs, 2029 CPU-s | §0: F₂₂ = 0.2282; both exponential readings excluded |
| Quantum cost of the same task | `resource_audit.py` §B | §5 |
| Break-even against exact classical | `resource_audit.py` §C | §5 |

**New exact estimator (DERIVED; validated).** Let X = W Z_b W and let P₊ project on Z_b = +1. Then:
- Tr_k[Z_b X] = 2 Tr_k[P₊X] − Tr_k[Z_b], because Tr_k[X] = Tr_k[Z_b].
- The global flip gives Tr_{N−k}[P₊X] = Tr_k[P₊X] − Tr_k[Z_b].
- Therefore F = {Σ_{k<N/2} (4T_k − 2Tr_k[Z_b]) + 2T_{N/2}}/2^N, with T_k = Tr_k[P₊X] ≈ d_k₊⟨Wψ|Z_b|Wψ⟩ for ψ random
  in P₊ ∩ sector k.

This is exactly the quantum protocol (random basis input, U, Z_a, U†, measure Z_b), run classically. It costs one
vector per site per sector, against the lane's five vectors shared by 4 sites. That is at most a 2.5× saving for a
single site: a minor classical gain, worth about 1 spin.

## 2. Validation ledger (MEASURED; `runs/`)

- `pplus_1UBQ_p19_N10_site8_exact.json`, `pplus_1UBQ_p245_N10_site9_exact.json`: exact-trace mode vs dense per-sector
  Trotter unitaries (the lane's validate_flip method) at t = 160 and 320 µs. Max deviation 7.1e-14 and 4.1e-13.
- `runs/buggy_exact_trace_superseded/`: my first exact-trace run. The backward leg was applied in forward gate order,
  a bug in the validation branch only, which gave deviations of 0.002–0.004. It is kept as a record and superseded.
  The random-vector production branch uses `SectorKernel.step(inverse=True)` and was never affected.
- `pplus_1UBQ_p19_N20_site8_seed2026.json`: N = 20, complex64, 202 CPU-s, peak RSS < 0.25 GB. Replicates the lane
  (table above).

## 3. Classical exact frontier: reproduced, then corrected (`resource_audit.json` → `A_classical_frontier`)

| platform (one echo curve) | lane N_max | audited N_max | basis |
|---|---|---|---|
| this workstation, 1 day | 26 | 26 (lane kernel); **28** with an optimised 2 ns/pair-element kernel | DERIVED; 2 ns is INFERENCE (the lane kernel is numpy gather/scatter at about 75 B per element) |
| this workstation, 1 week | 28 | 28–30 | same |
| one 80 GB GPU / 8-GPU node, 1 day | 32 / 34 | 32 / 34 | lane model reproduced |
| 4096 GPUs, 1 week | 46 | 46 | lane model reproduced |
| exascale, 1 month | **48** | **50** (Frontier-class, 4.8 PB HBM, 14–16 d per curve); **52** in about 40 d (Aurora-class, 8.2 PB, 2 vectors) | machine specs are INFERENCE, not verified this session |

Findings (DERIVED unless tagged):
1. **The lane's exascale memory is half the real figure.** It models 37,888 GPUs × 64 GB = 2.4 PB. A Frontier-class
   machine has about 37.6k MI250X × 128 GB ≈ 4.8 PB HBM (INFERENCE). With 3 sector vectors at N = 50 needing 3.0 PB,
   N = 50 fits, and its time is 14 d per curve even when the forward legs are recomputed.
2. **The literature anchor is out of date.** De Raedt et al., "Universal Quantum Computer Simulation of 50 Qubits on
   Europe's First Exascale Supercomputer…" (JUQCS-50, JUPITER), arXiv:2511.03359 (LITERATURE, abstract verified). It
   holds 2^50 = 1.13e15 amplitudes. One N = 52 half-filling sector has C(52,26) = 4.96e14 amplitudes. So a machine at
   the 50-qubit record holds **two N = 52 sector vectors**, which is the minimum the echo needs.
3. **The lane's model is internally inconsistent, in a direction generous to classical.** It charges 4400 vector-steps
   (forward reuse, about 8 live vectors) but sizes memory at 3 vectors, which would force recomputation (8000 steps,
   ×1.8). Its workstation N = 26 also ignores the precomputed sector maps: 3.0 GB at N = 24 and 13.5 GB at N = 26 in
   intp. This is harmless for the claim, since it overstates classical reach, but the per-day figures carry about ±1
   spin.
4. **Net: the exact frontier is 50–52, not 48.** Each further 2 spins costs about 4.5× the compute.

## 4. The spins needed are not identified (DERIVED from the lane's MEASURED ladder; `resource_audit.json` → `D_needed_N_robustness`)

The lane's "N_σ ≥ 58 (optimistic exponential)" comes from p19 at 320 µs, sites 9 and 8 (58 and 82). Refitting the
same ladder (N = 12–20, 5 points) gives:

| p19, 320 µs | lane exponential (all 5) | exponential, drop N = 14 | exponential, drop N = 12 | 1/N², last 3 | 1/N (all / last 3 / last 2) |
|---|---|---|---|---|---|
| site 8: N_σ | 82 (**rms 2.5σ**) | **23** (rms 0.43σ), F_∞ = 0.225 | 18 (rms 0.69σ) | **54** (rms 0.41σ) | 547 / 328 / 471 |
| site 9: N_σ | 58 (**rms 2.4σ**) | **22** (rms 0.42σ), F_∞ = 0.234 | 18 (rms 0.65σ) | **51** (rms 0.38σ) | 557 / 301 / 433 |

- **The lane's exponential is the worst-fitting variant of its own family.** It misses N = 14 by +4σ and N = 16 by
  −3σ. The N = 14 point sits +0.075 above every smooth trend on both sites, a shell event. Dropping it gives a fit
  7× better, with convergence at N ≈ 22–23.
- **Neither end is a bound.** The last step accelerates (|Δ18→20| = 0.026 against |Δ16→18| = 0.015, a ratio of 1.7),
  which weighs against fast convergence. The spread of F_∞ across models is −5 to +0.25 on these two sites.
- **What the data support.** The only MEASURED statement is "not converged at N = 20". N_needed lies anywhere in
  **~22–740**. The lane's "≥ 58" is a model-dependent point, not a lower bound. It has no claim to being
  "optimistic": 1/N² gives 51–54, which is inside the corrected exascale frontier.
- **The physics argument is suggestive but unquantified** (INFERENCE). The exact finite-cluster 1/N term (lane §4.3)
  argues for slow convergence. But the transfer S_ab(320 µs) at N = 16–20 is still spatially non-uniform (0.024–0.10 vs
  1/N = 0.05; MEASURED in the lane and reference files). So the cluster has not equilibrated and the diffusion volume
  that sets the true bias is unmeasured.
- **The decisive discriminator, now run** (§0). p19 site 8 at 320 µs, N = 22, predicted at:
  - 0.202 (lane exponential);
  - 0.223 (c/N through the origin);
  - 0.233–0.236 (1/N and 1/N² with offset);
  - 0.239 (exponential without N = 14).

  **Measured: 0.2282.** Both exponential readings are excluded. The spread that remains is 26 (receding exponential)
  to 430 (1/N), with F_∞ between 0.03 and 0.21.

## 5. Quantum side of the same task (DERIVED; hardware times are INFERENCE) (`resource_audit.json` → `B_quantum_cost_per_curve`, `C_breakeven_vs_exact`)

**Task.** One echo curve: 1 probe, 1 orientation, 8 times from 40 to 320 µs, 4 sites, σ = 0.01.

**Circuit.** A random computational-basis input, with state preparation by X gates. There is no oracle or block
encoding to hide. The sequence is U(t), then Z_a, then U(t)†, then measure all qubits.
- All 4 sites are read from the same shot through the estimator z_b·m_b. That gives 1e4 shots per time, with
  var ≤ 1 − F².
- U is the reference first-order Trotter circuit at dt = 2 µs.
- Each pair gate needs 3 arbitrary rotations, at 1.15 log₂(1/ε) + 9.2 T each (ε_tot = 1e-3 per circuit).
- Depth-limited wall clock assumes one QPU with unlimited factories: N−1 matchings per step, and about N/2 T in
  parallel. This is the case most favourable to quantum.
- Amplitude estimation (AE) instead needs π/σ repetitions per site on 2N+10 logical qubits.

| N | pair gates per step (dense / \|d\|>30 Hz) | T per curve | wall per curve at T layer 1 / 10 / 170 µs | AE at 1 µs | CNOT per deepest circuit (ln F_NISQ at 1e-3) |
|---|---|---|---|---|---|
| 20 | 190 / 183 | 3.4e11 | 9.3 h / 3.9 d / 66 d | 1.2 h | 1.8e5 (−182) |
| 26 | 325 / 310 | 5.9e11 | 12.5 h / 5.2 d / 89 d | 1.6 h | 3.1e5 (−312) |
| 50 | 1225 / 1110 | 2.3e12 | 1.1 d / 10.7 d / 183 d | 3.2 h | 1.2e6 (−1176) |
| **58** | 1653 / 1461 | 3.2e12 | **1.3 d / 12.6 d / 215 d** | 3.8 h | 1.6e6 (−1587) |
| 82 | 3321 / 2701 | 6.5e12 | 1.8 d / 18 d / 313 d | 5.6 h | 3.2e6 |
| 300 | 44 850 / 21 334 | 9.7e13 | 7.5 d / 75 d / 3.5 yr | 22 h | 4.3e7 |
| 550 | 150 975 / 48 518 | 3.4e14 | 14 d / 142 d / 6.6 yr | 1.8 d | 1.5e8 |
| 629 (all of 1UBQ's ¹H) | 197 506 / 55 666 | 4.5e14 | 16 d / 164 d / 7.6 yr | 2.1 d | 1.9e8 |

Multipliers and hidden burdens:
- **Trotter accuracy.** Matching the physical exp(−iHt) to σ/3 with first-order Trotter needs dt ≈ 0.5 µs. That
  multiplies every wall-clock figure by about 4. At N = 58, 1 µs, that is 5.3 d; the ratio is INFERENCE from the
  lane's measured 0.013 at N = 12.
- **Factory count.** At N = 58 the machine consumes about 29 T per layer. At a 1 µs layer, with 15-to-1 factories
  emitting one state per few tens of µs, that means hundreds to about 1500 factories: of order 1e6–1e7 physical qubits.
  At 10 µs it is of order 1e5–1e6 (INFERENCE).
- **Code distance.** Per-shot logical volume is about N × 2.5e6 T layers, which needs d ≈ 19–21 at p/p_th = 0.1
  (INFERENCE).
- **Coupling cutoff.** Truncating at 30 Hz (truncation error unaudited) cuts the pair count by 3.6× at N = 629, but
  barely helps at N ≤ 58.

**Break-even N\* against the exact classical method** (per curve; one QPU, depth-limited):

| T layer | workstation (lane kernel) | 1 GPU | 4096 GPUs | exascale (Frontier-class) |
|---|---|---|---|---|
| 1 µs | 26 | 34 | 44 | **48** (Q 1.0 d vs C 3.6 d) |
| 10 µs | 30 | 36 | 46 | **50** (Q 10.7 d vs C 15.6 d) |
| 170 µs | 32 (memory wall) | 36 (wall) | 48 (wall) | **52** (Q 191 d; C infeasible) |

Consequences (DERIVED):
- A quantum-only exact regime exists only for N_needed > 50–52.
- If N_needed ≈ 26 (the receding exponential, now disfavoured by N = 22), the question is inside **workstation** exact
  reach, and the quantum machine is slower (12 h per curve at 1 µs against 1.2 d on 8 lane-kernel cores).
- If N_needed ≈ 45–65 (exponential over all points, or 1/N²), it straddles the exascale edge. The quantum machine then
  needs 1–13 days per curve at a 1–10 µs T layer, or 5–53 days with dt = 0.5 µs.
- The 1/N branch, N ≈ 350–430, needs 350–430 logical qubits, weeks to years per curve, and about 1e14 T.
- The **K-101 floor does not apply.** This is not a quadratic sampling speedup; exact classical cost is exponential and
  the quantum cost is polynomial. The obstruction here is fault-tolerant scale and the unknown N, not K-101.

## 6. Comparator and value (INFERENCE; not a new kill)

1. **Exact simulation is not the best classical method for a σ-level target.** The quantum output carries shot noise
   (1e4 shots for σ = 0.01) and Trotter or logical error. The fair classical twin is any method that reaches σ = 0.01.
   Candidates, all untested at N ≥ 22:
   - finite-size extrapolation from N = 16–26 (feasible here in about a day);
   - b-aware cluster families;
   - spinDMFT or cluster DMFT;
   - a hybrid correction that replaces the finite-cluster conserved part Σ_j S_aj² with the classically compressible
     large-N transfer (K-104).
2. **The claim's own 1/N branch undercuts itself.** If F_N = F_∞ + c/N holds well enough to predict N_σ = 300–557, the
   same law yields F_∞ by extrapolation, so exact reach is unnecessary. If it does not hold, the 300–557 figures are
   unfounded.
3. **Value.** K-105 stands. The physical object (the protein's own echo) is measured on the spectrometer. A simulation
   of it has structural value only through forward-model inversion, which K-105 killed on reversal horizon, value and
   cost. Category 3 is at L0–L1.

## 7. Recommended next tests (for the lane or the governor; not run here beyond the block at the top)

1. **N = 24 (and 26) at p19 site 8, 320 µs; N = 22 at site 9 and at p245.** N = 22, p19 site 8 is done (0.2282).
   - Cost with `pplus_echo.py`: about 3–5 h (N = 24; the central-sector maps are about 3 GB, so run it under the
     governor) and about 15–25 h (N = 26) on one contended core.
   - Predictions for N = 24: 1/N (N = 18–22) gives 0.211; 1/N² gives 0.214; the receding exponential gives 0.223.
   - A 3-point N = 22–26 ladder with noise 0.0005 pins c and F_∞ to about ±0.01 **under a given law**. That is exactly
     the classical extrapolation adversary: if the 1/N law holds to N = 26, it answers R1-SIM classically.
2. **Re-state the lane's frontier** as 50 (exascale, month) / 52 (about 40 d). Cite arXiv:2511.03359.
3. **Before any quantum claim, run the σ-level classical adversary portfolio** (§6.1) at N = 22–26.
4. **Give the quantum side a Trotter-order study** (2nd order vs dt) and a factory-count model, if R1-SIM is ever
   escalated.

## 8. Ledger

| field | value |
|---|---|
| ID | ROUND3/r1sim_exact_reach/verify_resource |
| Hypothesis attacked | exact classical cannot reach the converged late-window echo (Category 3) |
| Algorithms | cost models (classical exact, fault-tolerant Trotter, qubitization order of magnitude); single-site P₊ typicality echo (new, exact up to typicality) |
| Targets | 1UBQ p19 (site 8) and p245 (site 9) at N = 10 validation; p19 site 8 at N = 20 and N = 22; orientation seed 1000; dt = 2 µs |
| Compute | about 38 single-threaded CPU-min in total: N = 22 at 2029 s (4 chunks of 768 / 734 / 311 / 215 s, each under 15 min); N = 20 at 202 s; N = 10 validations about 15 s; audit script 3.5 s. Peak RSS 0.84 GB. No detached processes; two chunks ran as session-managed background tasks and I waited for both; nothing modified outside this folder; no git commit |
| Quantum resources | none executed; all quantum figures are T-count/T-depth models (INFERENCE on hardware); simulator time is not quantum time |
| Leakage | none. Native geometry defines the physical instance (forward model) only |
| Statistics | typicality error ≈ 2·2^(−N/2) for the P₊ estimator (0.002 at N = 20, 0.001 at N = 22); fits are descriptive (4–5 points) |
| Replication | lane N = 20 values replicated with independent code and vectors (Δ ≤ 0.0025) |

## Files

- `resource_audit.py` → `resource_audit.json`, `resource_audit_stdout.txt`: sections A (frontier), B (quantum cost),
  C (break-even), D (fit robustness), E (1UBQ coupling statistics), F (kernel re-benchmark).
- `pplus_echo.py`: single-site exact-typicality echo (validation modes `--exact_trace --validate_dense`), with a
  checkpoint per sector.
- `analyze_n22.py` → `n22_summary.json`: the N = 22 point against the model predictions, refits including N = 22,
  and sector-resolved drift.
- `runs/`: N = 10 exact validations, N = 20 replication, the N = 22 point (p19, site 8, 320 µs), and the superseded buggy
  validation run.
