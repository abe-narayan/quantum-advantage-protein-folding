# ROUND4 lane `tx_early`: T-X-early (the converged ¹H echo inside T3)

_2026-09-28. Pre-registered in `PREREGISTERED/PREREG_G1_C1_Q4.md` ("Round 4", T-X-early; CRITIC A-1). Instrument:
1UBQ probes 19 and 245, sites b ∈ {1, 7, 8, 9}, orientation 0, reference first-order Trotter circuit (dt = 2 µs),
probe-centred clusters, b0 = random_b0(1000), γ = 0. Category 3 (physics simulation) only; nothing here touches K-105._

Tags: **MEASURED** (file in this folder), **DERIVED** (algebra here, checked numerically), **INFERENCE**, **UNPROVEN**.

## Verdict: INTERESTING (pre-registered rule: KEEP OPEN, because it could not be completed)

1. **The pre-registered KILL did not fire, and could not be tested completely** [MEASURED].
   - At **40 µs**, 7 of the 8 series pass both conditions: |X₂₂ − X₂₀| ≤ 0.005 and budget ≤ σ. All 8 pass once
     typicality noise is allowed for. The one failure is p245 b7, with ΔX = +0.0059 ± 0.0007.
   - At **80 and 120 µs**, F₂₂ was not computed. The per-agent limit of 90 CPU-min allows about 21 N = 22
     vector-steps per minute, and the full 3-time echo needs about 2 CPU-h for both probes (§4).
   - Under the strict reading fixed before any output (§0), a series passes only if it passes at all three times.
     So the result is 0 series passing, 1 failing and 7 undetermined, and the rule falls to its else-branch: **KEEP
     OPEN**.
   - SUPPORTS is not met: no series drifts by ≥ 0.01 per step (maximum |ΔX| = 0.006).
2. **At 40 µs, which lies inside every T3 estimate, the finite-cluster exact echo is already converged**
   [MEASURED for N ≤ 22; INFERENCE beyond].
   - F_N moves by at most 0.0026 between N = 18 and 22, and by at most 0.0056 between N = 16 and 22, on all 8 series.
   - Over the same range, H + floor on p245 fell by 0.015. Only X moved.
3. **The T-X hybrid estimator F̂_∞ = H_∞ + X_N is biased at early times.** This undercuts CRITIC-C1's "3–8σ gap" at
   40 µs [MEASURED back-test + INFERENCE].
   - The test: predict the exact N = 22 echo from smaller-N data (`backtest.json`).
   - The "F converged" model (F̂ = F_{N_s}) wins on **8/8 series for every N_s ∈ {14, 16, 18}**: rms 0.0015–0.0043.
   - The "X converged" model loses even when given exact H₂₂ and floor₂₂: rms 0.0086–0.0145, mean bias −0.009 to
     −0.014.
   - At 40 µs the full hybrid lies **0.054 (p19) and 0.015 (p245) below F₂₂**. Those gaps equal (H_∞ − H₂₂) − floor₂₂.
   - The pre-registered ΔX statistic reads this bookkeeping as drift. On p245, ΔX = +0.0044 ≈ −Δ(H + floor) = +0.0044,
     with ΔF ≈ 0.
4. **80–120 µs stays open** [MEASURED, N ≤ 20]. Neither model predicts F₂₀ from N = 16 to σ: rms 0.008–0.024, and
   F still moves by up to 0.011 from N = 18 to 20.

Claim levels: theoretical **L0** (no separation; instance-level finite-size physics). Practical **L0**: no quantum
resource is involved, and the classical side reaches the 40 µs echo by exact simulation of ≤ 22 spins.

## 0. Pre-run operationalisation (written 2026-09-28T11:28-07:00, before any N = 20/22 output; unchanged)

The pre-registered rule: KILL "the converged echo inside T3 is beyond σ-level classical reach" if
|X₂₂ − X₂₀| ≤ 0.005 on ≥ 6/8 series AND √(se_H² + offset² + ΔX²) ≤ σ = 0.01 on those series; else KEEP OPEN.

1. **"Series".** 8 series = 2 probes × 4 sites. A series passes only if both conditions hold at all three times (40,
   80, 120 µs). Secondary readings: per-time counts and the pooled 24-cell count.
2. **ΔX** = |X₂₂ − X₂₀| at that cell.
3. **se_H** = standard error of H_∞ (CSD statistics + exact-H typicality).
4. **offset** = |H_exact − H_CSD| at N = 22, same cluster and time, used at full magnitude.
5. **H_∞** = H_CSD(N_c = 80) + (H_exact,22 − H_CSD,22). CSD uses common random numbers for the two clusters. The
   verifier's estimator (independent N_c ≥ 80 runs + offset) is reported alongside.
6. **Typicality noise.** Reported, not subtracted.
7. **Verdict mapping (lane brief).**
   - KILLS if the rule fires.
   - SUPPORTS if |X₂₂ − X₂₀| ≥ 0.01 on ≥ 2 series at some t ≤ 120 µs on each probe.
   - INTERESTING otherwise.
8. **Precision.** complex64 is accepted only if complex64 and complex128 differ by ≤ 1e-4 at N = 18 (same draws).

Deviation (logged here, after output): compute ran out before F₂₂ at 80/120 µs. No threshold or reading was changed.
The "F converged" analysis (§2.3) and the back-test are **added analyses, not pre-registered**.

## 1. Methods

**Exact typicality driver: `tx_echo.py`, validated.**
- Estimator: the flip-folded sector estimator of `ROUND3/r1sim_exact_reach` (same circuit, clusters and random-draw
  order as `verify_classical/decomp_echo.py`).
- Kernel: `kernels.ClipSectorKernel`. It applies the same gates as `fastecho.SectorKernel`, with clip-mode take/put
  and preallocated temporaries, and is about 1.7× faster at N = 22 (`bench.py`).
- Time-major phases: forward vectors are stored between phases, so 40 µs finishes first.
- Checkpointing: after every leg (atomic JSON + npz). A resumed run is bit-identical.
- Two modes:
  - `echo`: F, S and G per sector, which gives H, floor and X.
  - `honly`: G by two inverse passes.
- **New: a direct X estimator.** R̂ = F̂ − ΣĜ² − Σ_j Ĝ_j Ĉ_bj + Ĝ'M̂Ĝ, with Ĉ_bj = ⟨Z_j x|Z_b W Z_b x⟩ and
  M̂_ij = ⟨x|Z_iZ_j|x⟩ taken from the same vector.
  - This is the single-vector estimate of Tr[W′Z_bW′Z_b]/2^N with W′ = W − ΣĜ_jZ_j. The O(δG) term vanishes because
    Tr[Z_j W_rest] = 0 [DERIVED].
  - X_direct = R̂ − floor.
  - It agrees with the plain X to ≤ 0.0006 at N = 20/22.

**Validation** (`validate.json`, `validate_direct.json`, N = 18 runs) [MEASURED]:

| check | result |
|---|---|
| tx_echo vs decomp_echo (N = 12, same draws, echo and honly, both probes) | F, G, H, floor, X to ≤ 2.2e-16 |
| kill/resume, 15 forced interruptions | bit-identical (0.0) |
| Clip vs reference kernel, one step, N = 12 | 6e-16 (c128), 3e-7 (c64) |
| complex64 vs complex128, N = 18, p19, same draws, 3 times × 4 sites | max \|ΔF\| 2.4e-6, \|ΔX\| 2.2e-6, \|ΔH\| 4e-7 → **complex64 accepted** |
| Direct X vs exact dense traces (N = 12, 24 seeds, both probes) | unbiased within noise (mean −0.0017 ± 0.0021 / +0.0018 ± 0.0021); rms 0.0103–0.0107 vs plain 0.0129–0.0131 (typicality scale 2^−6) |
| Own N = 18 vs reference N = 18 (different vectors) | \|ΔF\| ≤ 0.0032; H 0.3799 vs 0.3836 (typicality level) |
| N = 22: echo-mode H vs honly H (independent estimators, 40 µs) | 0.3613 vs 0.3609 (p245); 0.3808 vs 0.3809 (p19) |
| N = 20 X: own R = 2 vs mixed (reference F₂₀ + VC honly H₂₀) | agree to ≤ 0.0007 on all 8 series |

**Classical spin dynamics: `csd_crn.py`, `csd_stats.py`.**
- Model: the ROUND3 `csd_hydro.py` model (RK4, h = 1 µs), up to 120 µs.
- 48k trajectories per probe, N_c = 80, with the nested N = 22 cluster driven by the same initial spins (CRN).
- Control variate C_j = S_a^z(0)S_j^z(0), with known mean δ_aj, and a batch jackknife for SEs.
- The control variate cuts the SE by about 1.3×. CRN helps little at 40 µs, because 22- and 80-spin trajectories
  decorrelate [MEASURED].
- The pilot `csdcrn_..._s515` (8k, no control-variate moments) is superseded and kept.

## 2. Results

### 2.1 Exact H, floor (N = 22, all times) and CSD H_∞ [MEASURED; H_∞ INFERENCE-level method]

| probe | t (µs) | H₂₂ exact | floor₂₂ | H₂₂ CSD | offset | D = H₈₀ − H₂₂ (CSD, CRN) | H_∞ | se_H | √(se_H² + offset²) |
|---|---|---|---|---|---|---|---|---|---|
| p19 | 40 | 0.3809 | 0.0250 | 0.3759 | +0.0049 | −0.0290 ± 0.0036 | 0.3519 | 0.0036 | 0.0061 |
| p19 | 80 | 0.1693 | 0.0340 | 0.1694 | −0.0001 | −0.0305 ± 0.0036 | 0.1388 | 0.0037 | 0.0037 |
| p19 | 120 | 0.1092 | 0.0365 | 0.1064 | +0.0029 | −0.0286 ± 0.0027 | 0.0806 | 0.0028 | 0.0040 |
| p245 | 40 | 0.3609 | 0.0267 | 0.3669 | −0.0059 | +0.0119 ± 0.0041 | 0.3729 | 0.0041 | 0.0072 |
| p245 | 80 | 0.1251 | 0.0364 | 0.1335 | −0.0084 | −0.0025 ± 0.0029 | 0.1226 | 0.0029 | 0.0089 |
| p245 | 120 | 0.0839 | 0.0380 | 0.0897 | −0.0058 | −0.0250 ± 0.0025 | 0.0589 | 0.0026 | 0.0064 |

- The verifier-style estimator (independent N_c ≥ 80 runs + offset) agrees to ≤ 0.0006.
- The budget without ΔX is below σ in all 6 (probe, t) cells, so the rule turns on ΔX.
- p245 at 80 µs allows |ΔX| ≤ 0.0046 only.

### 2.2 The pre-registered test at 40 µs [MEASURED]

| series | F₁₆ / F₁₈ / F₂₀ / F₂₂ | X₂₀ (R = 2) | X₂₂ | ΔX (plain / direct) | budget | pass |
|---|---|---|---|---|---|---|
| p19 b1 | 0.5993 / 0.6005 / 0.6006 / 0.6031 | 0.1943 | 0.1973 | +0.0030 / +0.0030 | 0.0068 | yes |
| p19 b7 | 0.8717 / 0.8712 / 0.8711 / 0.8731 | 0.4648 | 0.4674 | +0.0025 / +0.0021 | 0.0066 | yes |
| p19 b8 | 0.9470 / 0.9527 / 0.9528 / 0.9526 | 0.5465 | 0.5468 | +0.0003 / +0.0002 | 0.0061 | yes |
| p19 b9 | 0.9534 / 0.9538 / 0.9525 / 0.9529 | 0.5462 | 0.5471 | +0.0009 / +0.0007 | 0.0062 | yes |
| p245 b1 | 0.9790 / 0.9790 / 0.9791 / 0.9790 | 0.5867 | 0.5910 | +0.0042 / +0.0045 | 0.0084 | yes |
| p245 b7 | 0.6962 / 0.6988 / 0.6990 / 0.7005 | 0.3067 | 0.3126 | +0.0059 / +0.0060 | 0.0093 | **no** (ΔX) |
| p245 b8 | 0.9551 / 0.9551 / 0.9551 / 0.9550 | 0.5627 | 0.5671 | +0.0044 / +0.0045 | 0.0084 | yes |
| p245 b9 | 0.9750 / 0.9746 / 0.9726 / 0.9726 | 0.5802 | 0.5847 | +0.0044 / +0.0044 | 0.0085 | yes |

- **Noise.** The typicality noise on ΔX is about 0.0007. The per-vector spread of X₂₀ is 0.0000–0.0010.
  - Allowing 2σ of noise, all 8 series pass.
  - On point estimates, 7/8 pass.
- **p245 common mode.** ΔX = +0.0044 on p245 equals −Δ(H + floor)₂₀→₂₂ = +0.0044 exactly, while ΔF ∈ [−0.0001, +0.0015].
- **p19.** H + floor is flat there (Δ = −0.0005), and so is X.
- **Rule outcome.** Strict: 0 pass / 1 fail / 7 undetermined → KEEP OPEN (§0.1). Per time: 7/8 at 40 µs; 80/120 µs
  not measured.

### 2.3 F converges while X absorbs the decomposition's bookkeeping [MEASURED back-test; added analysis]

`backtest.py` → `backtest.json`. It predicts the exact echo at the largest N from a smaller N_s using two models:
- "X converged": H_{N_t} + floor_{N_t} + X_{N_s}. This is the ideal hybrid, since it is given the exact target H.
- "F converged": F_{N_s}.

| target | N_s | hybrid rms / max / mean | flat-F rms / max / mean | flat better |
|---|---|---|---|---|
| N = 22, 40 µs | 18 | 0.0086 / 0.0107 / −0.0085 | **0.0015 / 0.0026 / −0.0004** | 8/8 |
| N = 22, 40 µs | 16 | 0.0133 / 0.0209 / −0.0122 | **0.0030 / 0.0056 / −0.0015** | 8/8 |
| N = 22, 40 µs | 14 | 0.0145 / 0.0214 / −0.0137 | **0.0043 / 0.0079 / −0.0015** | 8/8 |
| N = 20, 80 µs | 16 | 0.0120 / 0.0228 / −0.0079 | 0.0080 / 0.0120 / +0.0039 | 4/8 |
| N = 20, 120 µs (p19 only) | 16 | 0.0156 / 0.0282 / +0.0041 | 0.0242 / 0.0430 / +0.0189 | 2/4 |

**Reading.**
- At 40 µs the finite-cluster echo is converged to about σ/4 from N ≈ 18.
- X is not an independently converging quantity. It rises by approximately the amount that H + floor falls when
  spins are added, and F barely moves.
- F_N does not carry the floor as an additive finite-size bias. On p245 the floor fell from 0.0404 to 0.0267 between
  N = 14 and 22 (H + floor by 0.015), while F moved by ≤ 0.0025 on b1/b8/b9 and by +0.007 on b7.
- So the premise of CRITIC-C1, that a floor ≈ (1 − H)/N ≥ 3σ biases finite-cluster echoes, is **falsified at 40 µs
  for N ≤ 22**.
- CRITIC-C1's F₁₈ − F_∞(hybrid) = +0.031…+0.082 is, at 40 µs, the hybrid's own bias.
  - This lane's full hybrid gives F̂_∞ − F₂₂ = **−0.054 (p19) and −0.015 (p245)**, equal to (H_∞ − H₂₂) − floor₂₂.
  - [MEASURED numbers; the attribution is INFERENCE.]

**Why F is insensitive** [INFERENCE]. When far spins are added, weight of W = Z_a(t) moves from Z_a into flip-flop
strings on those spins. That lowers H. But those strings still commute with Z_b, so F_ab does not change.

**The unproven step** [UNPROVEN]. It is not shown that F stays flat when spins 23–80 enter. For p19, CSD says H drops
by 0.029 there. The support for flatness comes from the p245 N = 16→22 range and from the argument above.

### 2.4 80 and 120 µs (not measured at N = 22)

From the N ≤ 20 data [MEASURED], the largest |F₂₀ − F₁₈| is:
- p19: 0.011 at 80 µs (b9) and 0.0058 at 120 µs;
- p245: 0.0099 at 80 µs (b9).

Mixed-source X₂₀ − X₁₈ ranges from −0.0046 to +0.0105.

Prediction for p245 at 80 µs [INFERENCE]: the pending cells will show ΔX ≈ −Δ(H + floor) ≈ +0.006 plus ΔF. That is
probably a failure of the pre-registered rule, driven by the same bookkeeping as in §2.3 and not by four-point
hardness. The budget there allows only 0.0046.

## 3. What this means

- **For the open question in `ROUND3/CRITIC.md` §1 C1**, "is the converged echo inside T3 beyond σ-level classical
  reach?":
  - **At 40 µs, no** [MEASURED to N = 22; INFERENCE beyond]. Exact simulation of 18–22 spins gives F within about
    σ/4 of every larger cluster tested, and the hybrid is the worse estimator.
  - **At 80–120 µs, open.** F still moves by up to 0.011 per ΔN = 2 at N = 18→20, and both finite-size models miss
    by about 1–2σ from N = 16.
- **The Round-4 X-flatness criterion is mis-specified at early times.** X_N tracks −Δ(H + floor) even when the
  observable has converged, so the rule can KEEP OPEN a question whose answer is already classical.
  - Recommended replacement: explicit F_N ladders with a cross-family check (b-aware or pairb clusters, or spinDMFT),
    applied to F itself.
- **Nothing here touches K-105 or K-116**, and nothing is evidence for any quantum-advantage category. The only
  quantum-relevant statement is negative for the early window: a quantum simulator is not needed for the 40 µs echo
  at σ.

## 4. Resource ledger

| field | value |
|---|---|
| CPU (single-thread, OMP/MKL/OPENBLAS = 1) | about 80 CPU-min in total. N = 22 honly: 7.8 + 8.3 min. N = 22 echo at 40 µs: 16.8 + 17.1 min. N = 20 echo R = 2 at 40 µs: 4.5 + 4.3 min. N = 18 c64/c128: 4.0 min. CSD: 4.2 + 4.3 + 1.0 (pilot) min. Validations: about 6 min. Benchmarks: about 1.5 min |
| Kernel cost at N = 22 | 4.1 s per folded vector-step (central sector 705,432: 1.3–1.4 s per step), under 55–90% machine load |
| Peak RAM | ≤ 1.53 GB (N = 22 central sector: 745 MB index maps) |
| Longest run | 1024 CPU-s (N = 22 p245 echo), checkpointed. Every invocation stayed under 10 min wall except one: it reached 599 s wall inside a long leg, was moved to the background by the tool at the 600 s mark, and exited cleanly at its next checkpoint moments later |
| Cost of the missing cells | about 48 CPU-min per probe for N = 22 at 80 + 120 µs (700 vector-steps), plus about 13 CPU-min per probe for N = 20 (R = 2): about 2 CPU-h |
| Disk | `runs/` is about 0.57 GB. N = 22 and N = 20 forward and partial vectors are kept so the 80/120 µs phases can resume. Nothing was deleted |
| Quantum resources | none. Simulator time is not physical quantum time |
| Leakage | none. The native geometry defines the physical instance only; no fitting or selection on the outcome |

**Resume the pending cells** (each call ≤ 330 s wall; repeat until `steps_done` = [20, 40, 60]):
```
OMP_NUM_THREADS=1 python tx_echo.py --probe 245 --N 22 --mode echo --dtype complex64 --max-phase 60 --wall-s 330
OMP_NUM_THREADS=1 python tx_echo.py --probe 245 --N 20 --mode echo --R 2 --dtype complex64 --max-phase 60 --wall-s 330
(same for --probe 19), then: python analyze.py
```
`analyze.py` currently reads only the 40 µs cells at N = 20/22. It needs a small extension to score 80/120 µs once
those phases exist.

## 5. Files

- **Code:** `tx_echo.py` (driver), `kernels.py`, `bench.py`, `validate.py`, `validate_direct.py`, `csd_crn.py`,
  `csd_stats.py`, `analyze.py`, `backtest.py`.
- **Results:** `tx_early_summary.json` (all cells, rule evaluation, H_∞, budgets, F̂_∞), `backtest.json`,
  `validate.json`, `validate_direct.json`.
- **Runs:** `runs/*.json`, with checkpoints in `runs/*.ckpt.json` and `*.npz`.
