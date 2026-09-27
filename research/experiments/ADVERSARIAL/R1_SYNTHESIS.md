# R1 (NMR echo window): consolidated verdict from the Program Director

Date: 2026-09-27. Inputs: 7 lens reports under `research/experiments/ADVERSARIAL/R1_*`, plus one cross-check of my own on the live C2 data.

**Bottom line.** R1 is **KILLED** as a claim of quantum advantage for protein structure. Two lenses returned specific, credible kills, and they rest on independent assumptions: physics feasibility and value/break-even. Replication and methodology then removed most of the evidence underneath it. The N=10 "classical failure" was the failure of classical *approximations* that stopped one rung short. The model they failed on was a 10-spin cluster that has not converged in size. One question survives, and it is a physics-simulation question rather than a protein-structure one: is the converged dipolar OTOC(1) light cone larger than what exact classical simulation can reach? It is parked as R1-SIM, OPEN, and is not a project lead.

## 0. Director cross-check (new evidence)

I recomputed the echo bias of the C2 runs against the sector-exact reference stored in each file. That includes the `.partial` files of the jobs still running. Script: `research/experiments/ADVERSARIAL/R1_director/c2_echo_check.py`. Output: `c2_echo_check.json`. Timings are wall-clock seconds under governor suspend/resume, so treat them as indicative.

| Case | Echo fails at | Strings used (fraction of 4^N/4) | Pauli wall time | Sector-exact wall time |
|---|---|---|---|---|
| N=8, p19 and p245 | first closed at ε=1e-4 (p19) / 3e-5 (p245) | 0.98 / 0.997 | — | 0.8 s |
| N=10, p19 and p245, ε=1e-4 | 80 µs | 0.53–0.65 | 555–826 s | 2.2–2.4 s |
| N=10, ε=3e-5 | never (window closed) | 0.92–0.98 | 1439–1910 s | 2.2–2.4 s |
| N=12, ε=1e-4 (still running) | 60 µs (p19), 80 µs (p245); max echo bias 0.14–0.22 | 0.075–0.079 | 1976–3497 s | about 31 s |
| N=14, ε=3e-4 (still running) | 60 µs | — | — | 3866–4128 s, under suspension |

- **[MEASURED] At N=8 and N=10, sparse Pauli reproduced the echo only when it held essentially the whole symmetric operator space.** No compression of the echo has been found at any N. That is a precondition for hardness, not evidence of it.
- **[MEASURED, wall-clock] The Pauli adversary is dominated by exact simulation.** At N=12 the failing ε=1e-4 rung is 64–115× slower than sector-exact simulation.
- **[INFERENCE] The ε=3e-5 rung at N=12 will almost certainly hit its budget cap.** The cap is 3600 s per rung and 4M strings, and the ε=1e-4 rung already took 3497 s. A capped result cannot tell us anything about classical hardness.
- **[MEASURED] The N=14 exact S and F references are already in the `.partial` files.** They are usable as a larger-N reference now.

## 1. Lens verdicts

| Lens | Verdict | One-line reason | Decisive number |
|---|---|---|---|
| replicate | WEAKENS | Independent reimplementation matches RAW to 1e-14. But the next sparse-Pauli rung (ε=3e-5) closes the echo window in 4 of 6 N=10 jobs, and the C2 string metric is saturated. | Median f_hard^OTOC goes from 0.95 to **0.00** over 17 parameters (10 of 17 closed) [MEASURED]. M*/(4^N/2) = 0.46–0.50 [DERIVED] |
| fi_method | WEAKENS (conditional practical kill) | The gate's gain assumes the classical analyst throws away all data after t_c. Fitting the biased model to all the data cuts the deficit 3–5000×. With the literature Loschmidt-echo attenuation and joint use of transfer data, the gain is about 1. | Median joint gain **1.18 (dense) / 1.00 (amide)** at T3 = T2/0.15 [DERIVED; T3 transfer to proteins is INFERENCE] |
| classical_front | SUPPORTS (narrow) | Four new polynomial-cost families fail at 20–60 µs: cluster-correlation expansion, operator-spreading Markov/mean-field, stochastic Pauli, and MPO with χ ≤ 64. But exact N=10 costs 1.1 CPU-s, and the N=10 echo is not converged in cluster size. | Best polynomial method t_c = 60 µs [MEASURED]. \|F12−F10\| up to **0.14** (14σ) inside the window [MEASURED] |
| physics_feasibility | **KILLS** (practical, conditional) | The informative window sits at 4.8–25 T2. Measured reversal horizons in dipolar solids are T3 ≈ 4–6.7 T2. The forward model is also off by 5–66σ (methyl rotation, 1 kHz site offsets, reversal mismatch). | **0 of 11** jobs reach gain ≥ 2 with the physical network T2 (maximum 1.35). Break-even needs T3/T2 ≈ 15 [MEASURED+LIT; transfer to proteins is INFERENCE] |
| value_breakeven | **KILLS** (practical/value) | Against the classical data (transfer plus early echo) and exact classical reach, the saving is a factor of 1–3. The achievable CRBs are below the systematic floors. Fault-tolerant break-even needs N_eff of 30–47 at hours per forward evaluation. | g ≈ **2.7 (dense) / 1.0 (amide)** after exact reach [INFERENCE]. CRB 0.014–0.03 Å vs model-bias floor 0.06–0.6 Å [MEASURED-derived] |
| theory_hardness | WEAKENS | The dense-network σ-cone probably exceeds exact reach, but only by extrapolation. The amide branch is killed up to 350 µs. The N=10 reference is unconverged. There is no hardness result for OTOC(1); the published beyond-classical echo result is for OTOC(2). | N_σ = **16–20 spins at 40 µs** [MEASURED]; ≥ 57 at 80 µs [INFERENCE]. Amide N_σ ≤ 12–16 up to 350 µs [MEASURED] |
| amplify | WEAKENS | No variant strengthens the window (second-order OTOC F2, multi-site butterflies, multiple-quantum coherences, double-quantum Hamiltonian, dilution). Each lever that adds information also adds depth or environment sensitivity. | Late-F2 gain against the ε=3e-5 classical twin is **1.65×** [DERIVED]. ε=1e-5 reproduces F2 to at least 70 µs [MEASURED] |

**How the lenses fit together:**
- **The two kills are independent where it matters.** The fi_method and physics lenses both rely on the same literature anchor (T3 ≈ T2/0.15, Sánchez et al. PRA 105, 052232), so they count as one line of evidence on attenuation. The value kill does not use that anchor. Its conditions are a light-cone calibration (INFERENCE) and in-model bias floors (MEASURED-derived).
- **classical_front and replicate do not conflict.** Every sub-exponential truncation fails. Sparse Pauli holding about 4^N/4 strings, and exact simulation, both succeed. So the failure belongs to the approximations, not to classical computation.
- **theory and value agree in direction but not in size.** Both put the dense-network cone at or beyond exact reach at the informative times. Theory extrapolates ≥ 57 spins at 80 µs; value puts N_eff at t50 in the range 21–110, with a 7–589 bracket. Both are INFERENCE, and neither is measured beyond 40 µs.
- **Recorded figures that need correcting:**

  | Quantity | Recorded | Corrected |
  |---|---|---|
  | Echo/transfer FI ratio | 10–160× | 3.2–183× [MEASURED] |
  | f_hard | 0.55–1.0 | 0.49–1.0 [MEASURED] |
  | Fault-tolerant cost per forward evaluation | 11 h | 4–6 h with z corrected; the conclusion does not change [DERIVED] |

## 2. Consolidated status

**Status: KILLED.** This applies to R1 as a quantum advantage for protein structure computation, in any of claim categories 1–6.

**Which kill criteria fired:**
- **Feasibility:** the informative data lie beyond the physical reversal horizon.
  - Condition for the kill to stand: protein T3/T2 < ~15.
  - Measured in model solids: 4–6.7.
- **Value/break-even:** the gain over classically usable data is ≤ 3, and that precision is below the systematic floors. Separately, fault-tolerant break-even needs N_eff > 30–47 at 4–11 h per forward evaluation.
  - The value kill holds even with perfect reversal.

**Supporting evidence that it is not an artefact:** the N=10 evidence base is itself compromised in four ways.
1. ε=3e-5 closes the window in 4 of 6 jobs.
2. The reference is not converged in cluster size (N=12 vs N=10 differs by up to 0.46).
3. The gain definition inflates the deficit 3–5000×.
4. The parameter set has defects: a duplicated rigid_res16 parameter, a rigid parameter that moves the probe's nearest proton, and methyl protons treated as static coordinates.

**Claim levels:**
- **Theoretical: L1 at most, and only in a narrow sense.**
  - MEASURED: at least 9 polynomial-cost approximation families fail on a fixed, unconverged 10-spin model.
  - L0 as a hardness or separation claim. There is no separation from exact classical simulation and no hardness result for an instance family. The only anchors are worst-case (DQC1-completeness of all-eigenstate OTOCs, universality results), and they do not transfer to protein geometries [LITERATURE-SUPPORTED; transfer UNPROVEN].
- **Practical: L0, killed.**

**Paper claim ladder:**

| Category | Status |
|---|---|
| A. New formulation | Reached, but partly prior art: O'Brien et al. PRX Quantum 2022; Schuster et al. 2208.02254 (learning-protocol version); Zhang et al. 2510.19550 (small-molecule demonstration). Recorded in NM-1 and the lens READMEs; I did not re-verify them. |
| B. Empirically useful | **Not reached.** The in-model FI gain is erased by attenuation, nuisance parameters and model error, and it concerns short-range distances that classical data already constrain. |
| C. Advantage vs strong classical baseline | **Failed.** Exact simulation takes 1–12 CPU-s at N=10, and ε=3e-5 closes the window. |
| D. Resource-normalised | **Negative result.** Break-even N_eff ≈ 30–47. The smallest plausible task is about 1 month at a 1 µs T-layer (14 years at 170 µs). |
| E. Scaling | **Not reached.** The C2/C3 metric is saturated at N ≤ 10 and dominated by exact simulation at N=12. The physically relevant variable, the σ-cone N_σ(t), is measured only up to 40 µs. |
| F. Theoretical/query | None. |
| G. Fault-tolerant | An estimate exists and it is negative: 5–9e13 T gates and 100–160 logical qubits for the smallest task. |
| H. Hardware | None. Q-PoP is simulator-only; a window survives only at ≤ 1e-3 depolarising noise per qubit per Trotter step. |
| I. End-to-end | None. |

**Residual windows** (none of them is a project lead):
- **R1-SIM (OPEN, parked):** does the converged OTOC(1) light cone of dense protein ¹H networks exceed exact classical reach by 80–320 µs? At best this is a category-3 physics-simulation question.
- **R1-DQ (untested, low prior):** the double-quantum echo.
  - For: it is more reversible [LIT, unverified] and carries 1.8–4× more FI [MEASURED].
  - Against: it is not harder in local-T2 units, and it is about 7× more environment-sensitive (2.1σ vs 0.28σ at 60 µs) [MEASURED].
- **R1-dilute (long-range labels):** coherent time must stretch by λ³ ≈ 8–90×, while the reversal window scales with the network's own T2. Killed by INFERENCE, untested.

## 3. What the evidence supports saying

> In static, oriented protein ¹H dipolar networks (ubiquitin, GB1) modelled as isolated 10-spin clusters, the first-order dipolar echo (OTOC) carries 3–183× more per-parameter Fisher information than two-point polarisation transfer under ideal time reversal. Polynomial-cost classical approximations fail to reproduce it after 40–80 µs: coefficient- or weight-truncated Pauli dynamics at ε ≥ 1e-4, cluster-correlation expansion up to order N−3, operator-spreading Markov and mean-field models, stochastic Pauli paths, and MPOs with χ ≤ 64. Sparse Pauli dynamics that retains essentially the whole symmetry-allowed operator space, and exact sector simulation (seconds per geometry), do reproduce it. The echo's σ-level light cone already covers 16–20 protons at 40 µs, so the 10-spin model is not converged. The information gain disappears once three things are accounted for: literature-anchored reversal horizons (T3 ≈ 4–6.7 T2), joint use of the classically exact transfer data, and profiling of site offsets, methyl motion and reversal mismatch. The gain falls to ≈ 1.0–1.5× (at most 3×), and fault-tolerant forward simulation breaks even with exact classical simulation only at effective cones of 30–47 spins, at hours per evaluation. We therefore find no quantum advantage for protein structure from NMR echo simulation in the regimes examined, and identify irreversibility, forward-model error and the exact-classical light cone as the binding constraints.

**It does NOT support:**
- "Classical computation fails." Only approximations failed.
- Any claim of empirical, resource, sampling, hardware or provable advantage.
- "Echo FI 10–160× transfer FI" as a quantum gain. That is a comparison inside an ideal, noiseless, isolated model.
- Reading C2/C3 string-count growth as exponential classical hardness.
- Any statement about the physical (converged, embedded, dephased, time-reversed) protein echo.
- The amide-only branch. It is classically exact-simulable up to 350 µs.
- Long-range structural information. All parameters are 3.2–8.3 Å from the probe.
- Experimental feasibility: site-resolved preparation and readout, σ = 0.01, labelling, and 32–1900 spectrometer-days per probe.
- "OTOC(1) is classically hard." Google's beyond-classical claim is for OTOC(2), and Mi et al. 2021 report that operator spreading in OTOC(1) is captured by an efficient classical model.

## 4. Decisive remaining experiments, ranked

Budgets: single-threaded; RAM ≤ 1.5 GB unless noted; run under the governor.

**0. [RUNNING] C2/C3 at N=12 and 14** (1UBQ p19 and p245, γ=0; p19 N=14 γ=1000 partial).
- Status: this can no longer decide R1. At N=12 the adversary is dominated 64–115× by exact simulation (see §0).
- Action:
  1. Let N=12 finish its ε=3e-5 rung for the record.
  2. Stop the N=14 Pauli rungs by adding them to `cancel.txt`. Their only useful output, the exact N=14 S and F, is already in the `.partial` files, and stopping them frees about 5 GB and ends the suspend/resume thrashing.
  3. Do not launch N ≥ 16 C2 jobs.
  4. Add a PREREG deviation entry that redefines the C2/C3 scaling variable as N_σ(t), with saturation ratio and exact-cost columns.
- Kill for the "classical cost explodes" reading: saturation ratio ≥ 0.3 or exact cost below the Pauli cost at every measured N. This already holds at N = 8–12.

**1. T-A σ-cone convergence of the echo at the instrument's b sites.** This decides R1-SIM.
- Command: `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone.py --probe {19,245} --N {16,18,20,22}`
- Cost: N=20 takes about 2–4 h; N=22 about 8–15 h and < 1 GB.
- KILL R1-SIM (exact light-cone simulation suffices): |F_N − F_{N+2}| < σ for all t ≤ 320 µs at some N ≤ 22, on both probes.
- SUPPORT: F moves by > 3σ between N=20 and N=22 at t ≥ 160 µs.

**2. T-E: FI split and gain against the converged reference.**
- Use the N=14 exact data from the C2 `.partial` files now, then the T-A reference.
- Joint accounting: transfer plus early echo plus exact-reach classical data.
- Cost: under 30 CPU-min at N=14, since the references exist.
- KILL: late-window echo FI < 25% of its N=10 value, or joint g < 2.

**3. Simulated reversal feasibility (physics test B, new code).**
- Simulate a magic-echo/MPSDI backward block with finite pulses and 6.4% rf inhomogeneity on the N=12 clusters, and measure T3/T2.
- Cost: ≤ 10 CPU-min per setting.
- Pair it with a literature extraction of a protein Loschmidt or multiple-quantum echo T3 (needs WebFetch budget).
- KILL confirmed: T3/T2 ≤ 7.
- Reopen: only a measured protein T3/T2 ≥ 15. If the simulated T3/T2 is much greater than 15, flag that the finite model cannot represent irreversibility.

**4. R1-DQ inside the reversal envelope.**
- Pure reanalysis of `R1_amplify/out/obs_*_{dq,secular}_fine.json`, weighted by A(t)² from `R1_physics_feasibility/reversal_envelope.py`, with each Hamiltonian's own T2. Takes seconds.
- Then a sparse-Pauli ε=1e-4 adversary on the DQ echo (≤ 10 CPU-min).
- KILL R1-DQ: DQ hard-window FI inside the envelope ≤ secular FI on both proteins, or sparse Pauli reproduces the DQ echo to σ over the window.

**5. RT-3: classically non-identifiable directions.**
- Uses `R1_value_breakeven/fi_value.py`, variant `g_exact_reach`. Takes seconds.
- ESCALATE only if some generalised eigendirection has g ≥ 1e3 and maps onto a degree of freedom that AlphaFold or NOE leave undetermined (pLDDT < 70). Otherwise KILL.

**6. Formal C3-kill-1: complete the N=10 adversary panel.**
- Command: `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/experiments/ADVERSARIAL/R1_replicate/run_other_jobs.py <job> <job>` for the 6 untested jobs, about 8 CPU-min per pair. Then `--eps=1e-5` on the survivors (at least 1PGA p325 and 1UBQHN p548).
- KILL (pre-registered): median f_hard^OTOC < 0.3 under the best adversary. This is already indicated at 0.00 over 17 parameters.

**7. T-B: Pauli-phase-randomised OTOC(1) adversary at exact N=12.**
- New code, minutes per run.
- KILL R1-SIM: |F − F_rand| < σ over the window.
- Low prior: classical_front's incoherent path model failed with errors of 0.3–0.9.

**Queue hygiene.**
- **C1/HN NMR jobs (52 queued):** r_nmrA2 ×29, r_nmrB ×10, r_hn ×9, r_nmrR ×4. They use the ε ≥ 1e-4 panel and the N=10 reference, both now known to bias f_hard upward. Cancel them, or re-spool them with `--epslist 3e-5,1e-5` and an N+2 reference. They cannot change the verdict.
- **Q-PoP N=12 (r_pop):** low value, because the practical kill does not depend on circuit noise.
- Recommendation only; I have not touched `cancel.txt` or `control.json`.

## 5. Revival template

**OLD MECHANISM**
- Quantum forward simulation of protein ¹H dipolar first-order echoes (OTOC(1)).
- Structural parameters are extracted from a late time window where classical approximations fail to reproduce the echo.

**OLD FAILURE**
1. The failure was of truncated approximations, not of classical computation. Exact simulation takes 1–31 s at N = 10–12, and ε=3e-5 closes the N=10 window.
2. The reference model was unconverged in cluster size.
3. The informative window sits at 4.8–25 T2, beyond the measured reversal horizons T3 ≈ 4–6.7 T2.
4. The gain over classically usable data is 1–3×, on short-range distances whose achievable precision is below the systematic floors (0.06–0.6 Å).
5. Fault-tolerant break-even needs N_eff of 30–47 at hours per evaluation.

**NEW MECHANISM** (all four required)
- **(i) Scale:** a converged σ-cone N_σ(t_info) > 47–51 spins at the information-bearing times, measured and not extrapolated.
- **(ii) Reversibility:** t_info < T3 in a real protein sample, either with natural reversal (T3/T2 ≥ 15 measured) or with an engineered Hamiltonian (for example double-quantum or a Floquet sequence) whose own reversal horizon exceeds its own scrambling time.
- **(iii) Value:** the information must resolve a structural degree of freedom that the classical stack leaves undetermined (AlphaFold, NOE, PRE, DEER, cross-linking MS), with a profiled gain g ≥ 10 after offsets, methyl dynamics and an ensemble forward model.
- **(iv) Accuracy:** a forward model accurate to σ, meaning offsets, the complete methyl groups and motional averaging are all included.

**WHY THE OLD CONTROL NO LONGER APPLIES** (must be stated with evidence, one line per failure)
- (1–2) T-A shows N_σ > 22 with a > 3σ step between N=20 and N=22 at t ≥ 160 µs, so exact simulation of the cone is out of reach.
- (3) A measured protein T3/T2 ≥ 15, or a DQ envelope reanalysis showing DQ hard-window FI inside the envelope is greater than secular, removes the reversal-envelope kill.
- (4) RT-3 finds a direction with g ≥ 1e3 that AlphaFold or NOE leave undetermined.
- (5) A resource model with the corrected z shows a single-probe inversion in under 1 week at a stated, plausible T-layer time, beating exact classical simulation at the measured N_σ.

**NEW TEST** (pre-register in `experiments/preregistered/` before running)
- Tests: T-A, then T-E, the simulated reversal (test 3), R1-DQ (test 4) and RT-3 (test 5), with the kill criteria in §4.
- Classical twin: exact or typicality simulation of the measured cone, plus the best tensor-network or sparse-Pauli method at matched budget.
- ORACLE discipline: native structures are used only for the CRB and bias evaluation.
- Escalate only if all four conditions (i)–(iv) are met at once. A single one failing re-kills the mechanism.

**Record corrections required before anything is published** (no compute needed):
- **Claim wording.** Rewrite "every classical adversary/approximation fails" in CURRENT_STATE, T6 §4 and CLAIM_AUDIT D4 to: "every sub-exponential truncation tested fails; ε=3e-5 sparse Pauli (≈ full symmetric operator space) and exact simulation reproduce the echo at N=10; the N=10 reference is unconverged".
- **Ranges.** Correct the echo/transfer FI ratio to 3.2–183× and f_hard to 0.49–1.0.
- **PREREG deviation log.** Add the rigid-shift rule change (≥ 2 protons), the ε-ladder completion, and the redefinition of the C2/C3 scaling variable.
- **Provenance flags on RAW.**
  - Mark the duplicate rigid_res16 parameter in `1UBQ_p19_N10_o{0,1}_g*.json`.
  - Mark methyl-proton radial parameters as non-physical.
  - Mark rigid_res2 as short-range, since it moves the probe's nearest proton.
- **KILLBOOK.** Add a K-R1 entry built from this template. Move R1-SIM and R1-DQ to OPEN_QUESTIONS.

My own compute for this verdict was under 1 CPU-minute, single-threaded. My files are in `C:\Users\abena\quantum-advantage-protein-folding\research\experiments\ADVERSARIAL\R1_director\`:
- c2_echo_check.py
- c2_echo_check.json