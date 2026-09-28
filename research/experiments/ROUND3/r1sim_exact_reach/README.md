# ROUND3 lane: r1sim_exact_reach. How far can exact classical simulation take the protein ¹H echo?

_2026-09-28. Lane question (R1-SIM, `PREREG_G1_C1_Q4.md`): does the converged first-order dipolar echo
F_ab(t) = Tr[W Z_b W Z_b]/2^N, W = U(t)† Z_a U(t), of the dense 1UBQ ¹H network need more spins than exact classical
simulation can handle? The setup is fixed: probes 19 and 245, the instrument's sites b ∈ {1, 7, 8, 9}, one field
orientation, and t = 40…320 µs with the reference first-order Trotter circuit at dt = 2 µs._

Tags: **MEASURED** (file in this folder), **DERIVED** (algebra shown here), **LITERATURE** (arXiv abstract verified
this session), **INFERENCE**, **UNPROVEN**.

## Verdict: SUPPORTS, narrowly scoped

**Late window (≳ 240–320 µs).** The converged echo needs more spins than any exact classical method can handle. This is
a category-3 physics-simulation statement only. It does **not** revive R1 (K-105), and it says nothing about approximate
classical methods, which remain untested at N ≥ 22.

1. **N = 20 is measured unconverged on both probes** (MEASURED, new data).
   - p245, 160 µs: Δ₁₈ = |F₂₀ − F₁₈| = **0.038** at site 9 (0.856 → 0.819). That is > 3σ and about 15× the typicality noise.
   - p19, 320 µs: Δ₁₈ = **0.026**, which is *larger* than Δ₁₆ = 0.017. Sites 8 and 9 fall exactly as a 1/N law predicts
     (0.2451 measured vs 0.2442 predicted from N = 18; 0.2476 vs 0.2445).
   - p19, 160 µs: nearly converged. Δ₁₈ = 0.013 is below the pre-registered threshold of 0.0167, and site 1 is flat
     (0.2273 → 0.2274).
2. **Every finite cluster carries an exact O(1/N) term** (DERIVED, §4.3): F_ab = 1/N + F_⊥. At late times the measured
   values track c/N with c ≈ 3–5.5.
3. **Extrapolated need at 320 µs** (INFERENCE):
   - N_σ ≈ **58–82** under the most optimistic model that fits the drifting sites (exponential approach);
   - N_σ ≈ **250–550** under the 1/N model.
   Both exceed the exact-reach frontier (item 4). They are consistent with the earlier light-cone extrapolation of
   331–629 spins at 320 µs (`ADVERSARIAL/R1_theory_hardness/README.md`).
4. **Exact-reach frontier** for one echo curve (8 times × 4 sites) with the fastest exact method built here, under a
   generous-to-classical model (DERIVED from MEASURED kernel costs):

   | platform | N_max |
   |---|---|
   | this 8-core workstation, 1 day | **26** |
   | one 80 GB GPU / one 8-GPU node, 1 day | **32 / 34** |
   | 4096 GPUs, 1 week | **46** |
   | exascale-class machine, 1 month | **48** |

   The largest published state-vector simulations are 45 qubits (0.5 PB) and 48 qubits (LITERATURE).
5. **Early window (≤ 160 µs) is within exact reach for p19** (N ≈ 20–24) **but not demonstrated for p245**, where a
   shell event occurred at N = 19–20.

**Pre-registered statistic** (Δ_N = max_b |F_{N+2} − F_N| against σ + 2(err_N + err_{N+2}); only t = 160 and 320 µs
measured at N = 20):
- **KILL is excluded on both probes**: "converged by N ≤ 20" fails for p245 at 160 µs and for p19 at 320 µs.
- **SUPPORT is met on p245** (0.038 > 3σ at t ≥ 160 µs).
- **SUPPORT is not met on p19** at the measured times (0.026 < 0.03 at 320 µs).
- Formal pre-registered reading: **INCONCLUSIVE, with KILL excluded**.

**Methodological warning.** Under a 1/N drift, the pre-registered step criterion would be satisfied at N ≈ 20–28 while
the true finite-size error is still c/N ≈ 0.1–0.2 (10–20σ); see §4.4. The KILL rule should not be used as it stands.

Claim levels: theoretical **L0–L1**; practical **L0–L1** (details at the end of the summary).

---

## 1. What was built (`fastecho.py`, `echo2.py`, `run_echo.py`)

The method is exact typicality: the same estimator as the reference, with no approximation other than the random-vector
average. Five engineering levers apply to the reference circuit (`spins.pair_list` / `apply_step`):

| lever | what | gain |
|---|---|---|
| L1 sector restriction | Every fused pair gate, Z_a and Z_b conserve total Z, so vectors evolve per magnetisation sector with precomputed gather/scatter maps. | memory: largest sector C(N, N/2) instead of 2^N |
| L2 spin-flip folding | P = X^⊗N commutes with every pair gate and anticommutes with Z_a and Z_b, so Tr_k[W Z_b W Z_b] = Tr_{N−k}[…] (and the same for S). Only sectors k ≤ N/2 are evolved, with weight 2 for k < N/2. (DERIVED; verified exactly, §2.) | work × (2^N + C(N,N/2))/2^{N+1} ≈ 0.59 at N = 20 |
| L3 forward reuse | U(t_k)ψ and U(t_k)Z_bψ are propagated once through all echo times; only the backward legs are per time point. | 4400 instead of 8000 vector-steps per curve |
| L4 global-phase factoring | Each pair gate is e^{−ia}·[1 on \|00⟩,\|11⟩; e^{2ia}[[c, is],[is, c]] on \|01⟩,\|10⟩]. The scalar cancels exactly in W and S, so only the flip-flop half is touched. | about 2× fewer element operations |
| L5 complex64 | same random draws in complex64 vs complex128 differ by max \|ΔF\| = 3.6e-5 (MEASURED) | about 1.5–2.4× bandwidth |

Drivers:
- **Per-sector** (`echo2.echo`): checkpoints each sector.
- **Union-of-sectors** (`echo2.echo_union`): one vector on ⊕_{k≤N/2} sector_k with the weights folded into the
  amplitudes. It checkpoints after every backward leg, and resume after an injected kill is bit-exact (MEASURED).
  - At N = 20 under full machine load the union layout was ~2× *slower* than per-sector. Its 470 MB of index maps
    stream from DRAM, so per-sector is the production driver.

**Chebyshev backend** (`echo2.ChebKernel`): exact continuous-time exp(−iHt) on the real sparse sector Hamiltonian, used
for the Trotter-error audit.

Things that did not help (MEASURED, N = 18–20):
- a single gather + 2×2 GEMM + single scatter instead of elementwise updates;
- torch `index_select` / `index_copy_`;
- int32 maps (numpy converts them to intp on every call);
- the full-space strided 5-D-view kernel. It needs no index memory, but it is 2–7× slower per folded dimension under
  contention.

## 2. Validation (MEASURED; `reach_summary.json` → `validation`)

| check | result |
|---|---|
| One Trotter step vs `spins.apply_step` (N = 10, up to the factored phase) | 1e-16 (sector and full kernels); inverse round trip 1.5e-16 |
| Reference-ψ mode vs reference JSON, N = 14, all 8 times, both probes | max \|ΔF\| = 1.2e-14 (p19), 4.2e-13 (p245); \|ΔS\| ≤ 2e-14 |
| Flip-folding identity, dense per-sector traces, N = 10, n = 20/80/160 | max \|Tr_k − Tr_{N−k}\| = 1.2e-12 (traces ~ 240) |
| Flip mode (complex64) vs reference, N = 16 p245 (different random vectors) | rms 0.0043, max 0.012 (expected rms 0.0068) |
| Flip mode, N = 20, p19: transfer S vs the **governor's own reference-script N = 20 checkpoint** (independent code, vector and precision) | max \|ΔS\| = 0.0022 at 160 and 320 µs (typicality level) |
| Union vs per-sector driver (same draws, N = 12) | 4.4e-16 |
| Kill and resume (union driver, N = 12, injected failures after legs 700 and 1300) | bit-identical (\|ΔF\| = 0) |
| **Trotter circuit vs exact exp(−iHt)**, same ψ, N = 12 | max \|ΔF\| = 0.013 (p19, site 7, 40 µs), 0.007 (p245); ≤ 0.005 at t ≥ 160 µs. The reference circuit tracks the physical echo to about σ. |

## 3. Measured cost and memory vs N (single core, machine at 92–95% CPU from the governor's 4 jobs)

| N | kernel | measured |
|---|---|---|
| 16 | flip + union, complex64, full curve | **70 s** vs reference 654 s (9.3×) |
| 18 | per-sector, complex64, central sector (48 620) | 25 ms per Trotter step (6.6 ns per pair-element) |
| 20 | per-sector flip, complex64, production | **0.43–0.44 s per vector-step** over all folded sectors (7.3–7.6 ns per pair-element); 355 s for t = 160 µs; 683.5 s for t = 320 µs; peak RSS **0.23 GB** |
| 20 | reference script (`scripts/nmr_cone.py`, governor, same machine) | 3436 s for its 800-vector-step forward pass = **4.3 s per vector-step**. The full curve ≈ 8000 × 4.3 s ≈ **9.5 h** (INFERENCE from its own rate) vs ≈ **32 min** here (4400 × 0.44 s), about **18×** |
| 22 | per-sector, complex64, central sector (705 432) | 1.28 s per step (15.8 ns per pair-element, contention and cache); maps 745 MB (intp) |
| 22 | full-space complex64 / complex128 | 4.25 s / 10.2 s per step |

Cost model (DERIVED; `reach_summary.json` → `cost_model`):
- CPU time per curve = 4400 × N(N−1)/2 × D_fold/2 × c_pe, with D_fold = (2^N + C(N, N/2))/2 and
  c_pe = 7.3–16 ns (MEASURED range).
- GPU time per curve = gates × D_fold × 8 B / (2 TB/s), with no gate fusion, and × 3 for communication on multi-GPU.
  This model is generous to classical.
- Memory = 3 complex64 vectors of the largest sector. That variant recomputes the forward legs; the fast variant needs
  about 8 vectors.

| N | CPU core-hours per curve | memory, sector (3 vectors) | memory, full space (8 vectors) | GPU-hours per curve |
|---|---|---|---|---|
| 20 | 0.52–1.15 | 4 MB | 67 MB | 6e-4 |
| 22 | 2.5–5.5 | 17 MB | 0.27 GB | 3e-3 |
| 24 | 12–26 | 65 MB | 1.1 GB | 0.013 |
| 26 | 56–123 | 0.25 GB | 4.3 GB | 0.06 |
| 28 | 260–570 | 0.96 GB | 17 GB | 0.29 |
| 30 | 1.2e3–2.6e3 | 3.7 GB | 69 GB | 1.3 |
| 32 | 5.4e3–1.2e4 | 14 GB | 275 GB | 5.9 |
| 36 | 1.1e5–2.4e5 | 218 GB | 4.4 TB | 120 |
| 40 | 2.2e6–4.7e6 | 3.3 TB | 70 TB | 2.4e3 |
| 44 | 4e7–9e7 | 50 TB | 1.1 PB | 4.6e4 |
| 48 | 8e8–1.7e9 | 0.77 PB | 18 PB | 8.7e5 |

**Frontier N_max for one echo curve (one probe, one orientation):**

| platform | N_max |
|---|---|
| this workstation (8 cores, 15.6 GB), 1 day | **26** |
| this workstation, 1 week | 28 |
| one 80 GB GPU, 1 day | 32 |
| one 8×80 GB node, 1 day | 34 |
| 4096 GPUs, 1 week | 46 |
| 37 888 GPUs × 64 GB, 1 month | **48** |

- Gate fusion or a dedicated (uncontended) machine would add about 1–2 spins.
- The frontier grows by roughly 2 spins per 4.5× more compute.
- Every time point, site, probe and orientation multiplies the cost.

LITERATURE anchors, verified by arXiv abstract: Häner & Steiger, "0.5 Petabyte Simulation of a 45-Qubit Quantum Circuit",
arXiv:1704.01127 (Cori II, 8192 nodes); De Raedt et al., "Massively parallel quantum computer simulator, eleven years
later", arXiv:1805.04708 ("up to 48 qubits"). Our circuits are much deeper (4400 × N²/2 two-qubit gates per curve,
2.8M at N = 36), so the practical frontier sits at or below these records.

## 4. Convergence with the new N = 20 points (`reach_summary.json` → `convergence`)

### 4.1 Ladders (N = 12, 14, 16, 18 from the reference; N = 20 new here; MEASURED)

| probe, t | site | F at N = 12 / 14 / 16 / 18 / **20** | Δ₁₆ | **Δ₁₈** |
|---|---|---|---|---|
| p19, 160 µs | 1 | 0.310 / 0.287 / 0.239 / 0.227 / **0.227** | 0.011 | 0.000 |
| | 7 | 0.511 / 0.436 / 0.417 / 0.403 / **0.397** | 0.014 | 0.006 |
| | 8 | 0.595 / 0.635 / 0.550 / 0.524 / **0.511** | 0.026 | **0.013** |
| | 9 | 0.496 / 0.544 / 0.446 / 0.443 / **0.439** | 0.003 | 0.004 |
| p19, 320 µs | 1 | 0.266 / 0.228 / 0.176 / 0.167 / **0.156** | 0.008 | 0.011 |
| | 7 | 0.369 / 0.286 / 0.268 / 0.251 / **0.239** | 0.017 | 0.012 |
| | 8 | 0.405 / 0.409 / 0.287 / 0.271 / **0.245** | 0.015 | **0.026** |
| | 9 | 0.412 / 0.408 / 0.286 / 0.272 / **0.248** | 0.014 | 0.024 |
| p245, 160 µs | 1 | 0.476 / 0.362 / 0.359 / 0.365 / **0.362** | 0.006 | 0.002 |
| | 7 | 0.358 / 0.263 / 0.228 / 0.223 / **0.220** | 0.005 | 0.003 |
| | 8 | 0.461 / 0.427 / 0.533 / 0.496 / **0.469** | 0.037 | 0.028 |
| | 9 | 0.873 / 0.870 / 0.861 / 0.856 / **0.819** | 0.005 | **0.038** |
| p245, 320 µs | all sites | N = 20 not computed (budget) | Δ₁₆ = 0.054 | — |

Typicality error: 2^{−N/2} for the reference ladder and √2·2^{−10} = 0.0014 at N = 20 (flip mode).

### 4.2 Pre-registered statistic (Δ₁₈ vs threshold 0.0167 and 3σ = 0.03)

| | 160 µs | 320 µs |
|---|---|---|
| p19 | 0.013: converged at this time | 0.026: **not converged**, < 3σ |
| p245 | 0.038: **not converged, > 3σ** | not measured |

- KILL ("converged by N ≤ 20 at all t") fails on both probes.
- SUPPORT holds for p245 only.
- Pre-registered overall: **INCONCLUSIVE, with KILL excluded**.

### 4.3 Why the late-time echo drifts like 1/N (DERIVED + INFERENCE)

**DERIVED.** Z_a = Z_tot/N + (Z_a − Z_tot/N), and U conserves Z_tot. Therefore W = Z_tot/N + W_⊥ with
Tr[Z_tot W_⊥] = 0. Because [Z_tot, Z_b] = 0, the cross terms vanish exactly. The result, for every finite cluster and
for the Trotter circuit as well as exact time:

  **F_ab(t) = 1/N + Tr[W_⊥ Z_b W_⊥ Z_b]/2^N**

- The exact 1/N piece is the cluster's equilibrated conserved charge. At N = 20 it is 0.05 = 5σ.
- In an infinite protein, this piece is instead set by how far spin diffusion has spread by time t.
- A scrambled W_⊥, random within each sector, adds about E_k[m_k²] ≈ 1/N more (INFERENCE).

**Consequence.** Once the operator front and the diffusing charge fill the cluster, F_N(t) sits on a finite-size
plateau that scales ∝ 1/N. It converges only when N ≫ N_cone(t).

**Observed (MEASURED).** At 320 µs the late values are 0.16–0.25 ≈ (3–5)/N at N = 20, and sites 8 and 9 of p19 follow
the F ∝ 1/N prediction to within 0.001–0.003.

### 4.4 Extrapolated N needed for |F_N − F_∞| < σ (INFERENCE; 4–5 points per series, with shell events)

| series | 1/N fit: c, N_σ = c/σ | exponential fit: ξ, N_σ |
|---|---|---|
| p19, 160 µs, sites 1 / 7 (plateauing) | c ≈ 0.9–1.6 (last 3 points) → 94–162 | ξ ≈ 2–4.6 → **17–23** |
| p19, 160 µs, site 8 | c ≈ 3.1 → 312 | degenerate (no curvature) |
| **p19, 320 µs, sites 8 / 9** | c ≈ 3.0–5.6 → **300–557** | ξ ≈ 12–18 → **58–82** |
| p19, 320 µs, sites 1 / 7 | c ≈ 1.5–3.7 → 154–374 | ξ ≈ 2–4 → 17–23 |
| p245, 160 µs, site 9 | c ≈ 1.4–3.3 → 136–328 | degenerate |
| p245, 320 µs (N ≤ 18) | c ≈ 1.8–5.3 → 180–531 | 16 for sites 1/7; degenerate for sites 8/9 |

**Robust reading.**
- For each late-window series, the site that is still drifting needs N ≳ 58 even under the most optimistic model that
  fits it. The 1/N model gives hundreds.
- Both exceed the 48-spin exascale ceiling.
- Only the early, near-probe sites (p19 site 1 and similar) look convergeable within reach (N ≈ 17–24).

**False convergence of the pre-registered rule (DERIVED).** If F_N = F_∞ + c/N, then Δ_N ≈ 2c/N². This falls below the
threshold 0.0167 at N ≈ √(2c/0.0167) ≈ 15–28 (column "step-crit N" in the summary), while the true error c/N is still
0.1–0.2. A ladder that ends at N = 22–26 could therefore "KILL" R1-SIM spuriously.

**Recommendation.** Replace the step rule with extrapolation-based or cross-cluster-family criteria.

## 5. Attacks on this verdict (what could overturn it)

1. **Cluster family (UNPROVEN either way).**
   - The nested clusters are centred on probe a. Three of the four b sites lie at the N = 10 boundary (≈ 3.9 Å from a).
   - Their own first coordination shells extend to ≈ 7 Å from a, which corresponds to N ≈ 50–120 in this family
     (R1_theory_hardness §2.1 density table).
   - The p245 site-9 jump at N = 19–20 is such a shell event. A b-aware family (nearest to {a} ∪ b) may converge the
     early window faster.
   - It cannot remove the 1/N conserved-charge floor at late times (§4.3).
2. **Approximate classical adversaries are the real competitor, not exact reach.**
   - Finite-size extrapolation in 1/N from N = 16–26 (feasible here in about 1 day) could give F_∞ with a controlled
     error bar.
   - If that error bar is < σ, R1-SIM is answered classically without exact reach, and the practical significance of
     this SUPPORT disappears.
   - Also untested at N ≥ 22: spinDMFT and cluster DMFT, and the hybrid core+bath adversary (which failed at 4–20σ for
     N ≤ 18).
3. **Only 2 time points, 2 probes and 1 orientation at N = 20.**
   - p245 at 320 µs and p19 at 200–280 µs are missing.
   - The 1PGA p390 and 1UBQ p487 ladders (N ≤ 16, governor) are not analysed here.
4. **Trotter vs physics.**
   - The reference circuit differs from exact exp(−iHt) by ≤ 0.013 at N = 12.
   - It is not rechecked at N = 20.
5. **The quantum side is not costed here.**
   - The prior synthesis estimates fault-tolerant break-even at N_eff ≈ 30–47 and 4–6 h per evaluation.
   - A converged 60–500-spin echo at σ = 0.01 needs roughly 1e4 shots × 320 Trotter layers × N²/2 gates.
   - That is fault-tolerant territory; practical level L0.

## 6. Resource ledger

| field | value |
|---|---|
| ID | ROUND3/r1sim_exact_reach |
| Hypothesis | the converged late-window echo exceeds exact classical reach (R1-SIM) |
| Algorithms | sector-restricted, flip-folded, forward-reusing statevector typicality (Trotter); Chebyshev exact-time audit |
| Targets | 1UBQ probes 19 and 245, instrument sites {1, 7, 8, 9}, orientation seed 1000, dt = 2 µs |
| Compute | about 42 single-threaded CPU-minutes; largest invocation 9.4 min (565 s); every run ≤ 1 GB RAM; peak RSS in production 0.23 GB |
| Quantum resources | none (classical lane); simulator time is not physical quantum time |
| Leakage | none. Native geometry only defines the physical instance (the forward model), as in the reference; no fitting or selection on outcomes |
| Hardware assumptions | frontier model: 2 TB/s per GPU, × 3 communication penalty, no fusion (generous to classical) |
| Statistics | typicality error ≤ 0.0014 at N = 20; Δ₁₈ = 0.038 is about 15× the combined noise; fits are descriptive (4–5 points) |
| Replication | N = 20 transfer cross-checked against the independent governor reference run (≤ 0.0022) |

## 7. Files

- `fastecho.py`: kernels (`SectorKernel`, `FullKernel`), instance loader, reference draw. Its `echo_sector` is
  superseded by `echo2.echo`.
- `echo2.py`: production drivers `echo` (per-sector, checkpoint per sector) and `echo_union` (checkpoint per backward
  leg, stop and resume), plus the Chebyshev backend.
- `run_echo.py`: CLI; writes `runs/*.json`.
- `bench_kernels.py` → `bench_kernels.json`: correctness check and per-step timings, N = 12–22.
- `validate_flip.py` → `validate_flip.json`: exact flip-folding identity at N = 10.
- `analyze_reach.py` → `reach_summary.json`: validation, cost model, frontier, convergence fits, pre-registered Δ₁₈.
- `runs/`:
  - N = 12 Trotter vs Chebyshev audit;
  - N = 14 reference-mode validations;
  - N = 14/16 flip validations;
  - **N = 20: `1UBQ_p19_N20_flip_trotter_complex64_t80.json` (160 µs) and `..._t160.json` (320 µs)**;
  - **p245 N = 20 at 160 µs, kept in the checkpoint `1UBQ_p245_N20_flip_trotter_complex64_t80-160_U.json.ckpt.json`
    (+ `.npz` with the forward vectors at step 80)**. Rerunning
    `python run_echo.py --probe 245 --N 20 --mode flip --dtype complex64 --times 80 160` resumes it to 320 µs
    (about 1200 union vector-steps, 20–30 CPU-min).

All runs use `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`.
