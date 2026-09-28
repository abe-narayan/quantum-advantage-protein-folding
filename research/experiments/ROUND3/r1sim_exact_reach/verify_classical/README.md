# verify_classical: classical-adversary check of the `r1sim_exact_reach` claim

_2026-09-28. Adversarial verifier (classical). Claim under attack: exact classical simulation cannot reach the converged
late-window (about 240–320 µs) first-order dipolar echo F_ab(t) of the dense 1UBQ ¹H network at the instrument sites.
The claimed support: N = 20 is unconverged, and extrapolation gives N_σ ≥ 58 (exponential) to 300–557 (1/N). The claim
also says the early window (≤ 160 µs) is within exact reach for p19. Category 3 only; it does not revive R1 (K-105)._

Tags: **MEASURED** (file here), **DERIVED** (algebra here, checked numerically), **INFERENCE**, **UNPROVEN**,
**LITERATURE** (cited from repo code, not re-verified this session).

## Verdict: NOT REFUTED on its literal scope, but its significance is substantially weakened and two statements are corrected

1. **Literal claim (exact reach): survives, and is strengthened.**
   - Even the two-point part of the echo is not converged at N = 20.
   - Classical spin dynamics shows H(t) = Σ_j G_aj(t)² still falls by 0.04 at 320 µs and by 0.05 at 160 µs between
     N = 20 and N_c = 80–160. [MEASURED]
2. **Most of the measured finite-size drift is classically compressible two-point physics, not echo hardness.** The echo
   splits exactly (DERIVED, validated to 1e-14) into F = H + floor + X:
   - H is a pure two-point transfer quantity.
   - floor is the cluster's conserved-charge term. It is exactly computable and vanishes as N → ∞.
   - X is the four-point remainder.

   For **5 of 8 late-window (320 µs) series**, 75–109% of the last N-step drift of F is in H + floor, while X is flat to
   ≤ 0.004 per step. [MEASURED] H itself is obtained on 80–160 spins by classical spin dynamics (CSD) in about 3 CPU-min,
   validated against exact H to ≤ 0.012 (≤ 0.007 at N = 20). [MEASURED]
3. **The N_σ = 58–557 figures are not a measure of classical cost.** They extrapolate the raw F_N, which mixes the
   compressible H + floor drift with the four-point residue. [INFERENCE]
4. **Correction: the early window is NOT shown to be within exact reach for p19.**
   - The "nearly converged" p19 160 µs site 1 (F: 0.2273 → 0.2274 at N = 18 → 20) is a cancellation: H + floor fell by
     0.010 and X rose by 0.010.
   - H(160 µs) is 0.097 at N = 20 and about 0.044–0.05 for N_c ≥ 80.
   - The hybrid estimate of F_∞(p19, 160 µs, site 1) is about 0.14, against F_20 = 0.227. [MEASURED + INFERENCE]
5. **Correction to the "1/N law" (F_N ≈ c/N, F_∞ ≈ 0) used for the 300–557 numbers.** The four-point residue X is far
   from zero on several sites, for example X ≈ 0.13 (p19 site 7) and X ≈ 0.62 (p245 site 9) at 320 µs. So F_∞ is not
   ≈ 0 there. [MEASURED]
6. **What is still open (UNPROVEN).**
   - Whether X is converged beyond N = 20. The H ladder at 40 µs looked flat over N = 14–20 (≤ 0.007) yet shifts by
     about 0.02 at N_c ≥ 24 under CSD, so a comparable false plateau in X cannot be excluded.
   - The shell-event series: p19 sites 8/9 at 320 µs (dX = −0.014/−0.012 at N = 20) and p245 site 8 (dX = −0.043 at
     N = 18). These still carry four-point drift.

**Credible classical route (partial).** The estimator is F_∞ ≈ H_∞(CSD on N_c ≥ 80, plus the exact−CSD offset at N = 20)
+ X_{N≤20}. It gives candidate converged late-window values for the 5 flat series at an estimated ±0.005 (H) plus the
unquantified X-convergence error, possibly 0.01–0.02. That route is not demonstrated for the 3 shell-event series.
Because the claim is explicitly about *exact* simulation and already flags approximate adversaries as open, it is not
refuted. But its "exceeds exact reach ⇒ meaningful simulation target" reading now rests on the four-point residue of 3
of 8 late series plus the unverified convergence of X.

Claim levels: theoretical **L0** (no separation; the hardness is instance-level and largely two-point hydrodynamic);
practical **L0** (no quantum resource advantage shown; a poly-cost classical estimator covers most of the drift).

## 1. Exact decomposition (DERIVED; `decomp_echo.py`, validated by `validate_decomp.py`)

With W = Z_a(t) = Σ_j G_j Z_j + W_rest, where G_j = Tr[W Z_j]/2^N (the two-point transfer a→j) and Tr[Z_j W_rest] = 0:
- [Z_j, Z_b] = 0, so the cross terms vanish, and **F_ab = H + R_ab** with H = Σ_j G_j² (independent of b, two-point
  only) and R_ab = Tr[W_rest Z_b W_rest Z_b]/2^N.
- **floor** = Tr[W_rest (Z_tot/N) W_rest (Z_tot/N)]/2^N = Σ_k m_k² τ_k(W_rest²), with m_k = (N − 2k)/N. It is
  computed exactly per sector from G and exact Z_iZ_j sector traces, and floor ≈ (1 − H)/N → 0.
- **X = F − H − floor → F_∞ − H_∞** as N → ∞.

**Validation (MEASURED, `validate_decomp.json`).** N = 10, p19, compared against an independent dense computation with
the reference `apply_step`:

| check | max error |
|---|---|
| identity F = H + R | 7.9e-16 |
| F | 1.1e-14 |
| G, echo mode | 4.4e-15 |
| G, two-inverse-pass mode | 4.4e-15 |
| H | 7.3e-15 |
| floor | 2.0e-16 |
| R | 3.3e-15 |

**H ladders** (MEASURED, `runs/1UBQ_p*_N*_probe_honly_*.json`).
- Two inverse passes: G_j(n) = ⟨S^{−n} Z_a x|Z_j|S^{−n} x⟩, i.e. 320 vector-steps instead of 4400 for an echo.
- N = 12–16 use R = 2 vectors (unbiased H); N = 18 and 20 use R = 1 (bias ≤ N/2^N).
- N = 12 typicality noise is about 0.01 (the deterministic H_12(320 µs) is 0.1488 vs the estimate 0.138); N ≥ 16 is
  ≤ 0.002.
- G_ab reproduces the reference transfer S to ≤ 0.006 at N ≥ 16.

**Trotter offset on H** (MEASURED, `trotter_H.json`, partial): at p19, N = 12, Trotter vs exact exp(−iHt) differs by
max 0.0010 in H and 0.0031 in G. The script was stopped by its own 800 s timeout before N = 14, because its per-time
outer products were too slow.

## 2. Where the drift lives (MEASURED, `verify_summary.json` → `series`)

**p19, 320 µs** (F from the reference, N ≤ 18, and the lane's N = 20):

| site | F, N = 16 / 18 / 20 | X, N = 16 / 18 / 20 | last dF | last dX |
|---|---|---|---|---|
| 1 | 0.176 / 0.167 / 0.156 | 0.042 / 0.044 / **0.045** | −0.011 | +0.001 |
| 7 | 0.268 / 0.251 / 0.239 | 0.134 / 0.128 / **0.128** | −0.012 | 0.000 |
| 8 | 0.287 / 0.271 / 0.245 | 0.153 / 0.148 / 0.134 | −0.026 | −0.014 (shell) |
| 9 | 0.286 / 0.272 / 0.248 | 0.152 / 0.149 / 0.136 | −0.024 | −0.012 (the 2.03 Å neighbour of b9, rank 19, enters at N = 20) |

**p245, 320 µs** (N ≤ 18):

| site | F, N = 14 / 16 / 18 | X, N = 14 / 16 / 18 | last dF | last dX |
|---|---|---|---|---|
| 1 | 0.223 / 0.206 / 0.194 | 0.083 / 0.082 / 0.081 | −0.013 | −0.001 |
| 7 | 0.194 / 0.167 / 0.154 | 0.053 / 0.044 / 0.042 | −0.013 | −0.002 |
| 9 | 0.770 / 0.745 / 0.730 | 0.629 / 0.621 / 0.617 | −0.015 | −0.004 |
| 8 | 0.332 / 0.333 / 0.279 | 0.191 / 0.209 / 0.167 | −0.054 | −0.043 (shell) |

**p19, 160 µs, site 1** (the claim's "converged" early point):
- dF(18→20) = +0.0001, but dX = +0.0103 and d(H + floor) = −0.0103.
- The apparent convergence is a cancellation, not convergence.

**Cluster geometry** (MEASURED): in the probe-centred family, p19 site 8 (a methyl proton) gets its methyl partners at
ranks 16 and 23. Site 9 gets a 2.03 Å neighbour at rank 19. p245 site 9 gets a 3.06 Å neighbour at rank 19.

## 3. Two-point part beyond exact reach: classical spin dynamics (`csd_hydro.py`)

The CSD model follows `spins.classical_spin_correlators` (Elsayed–Fine-type; LITERATURE as cited in the repo code, not
re-verified).
- |S| = √3/2, RK4 with h = 1 µs; h = 0.5 µs gives identical results to 4 decimals; norm drift ≤ 0.0035.
- G is estimated with an a↔j-symmetrised estimator, and H is estimated unbiased from two independent halves.

**Validation against exact H on the same clusters** (MEASURED, 40–320 µs):

| probe | N = 18 | N = 20 |
|---|---|---|
| p19 | max \|Δ\| 0.012 (CSD low) | 0.0067 |
| p245 | 0.012 (0.0045 at t ≥ 160 µs) | 0.012 (0.0047 at t ≥ 160 µs) |

**CSD H ladder** (MEASURED):

| probe, N_c | 40 µs | 160 µs | 240 µs | 320 µs | CPU s |
|---|---|---|---|---|---|
| p19, 20 | 0.378 | 0.097 | 0.072 | 0.066 | 25 |
| p19, 22 | 0.362 | 0.081 | 0.064 | 0.061 | 48 |
| p19, 24 | 0.357 | 0.070 | 0.053 | 0.047 | 27 |
| p19, 40 | 0.362 | 0.053 | 0.038 | 0.032 | 53 |
| p19, 80 | 0.338 | 0.049 | 0.027 | 0.020 | 167 |
| p19, 160 (M = 4000) | 0.363 | 0.054 | 0.027 | 0.025 | 183 |
| p245, 20 | 0.376 | 0.079 | 0.063 | 0.058 | 27 |
| p245, 80 | 0.378 | 0.041 | 0.028 | 0.017 | 159 |

- **H_∞ estimate** (mean of N_c ≥ 80 plus the exact−CSD offset at N = 20) at 320 µs: **0.026 (p19) and 0.017 (p245)**.
  The typical SE is 0.004–0.008.
- **The bath effect is collective, not a single shell** (MEASURED). Adding only ranks 21 and 23 to the N = 16 core
  leaves H(320 µs) at 0.084, and 16 + {20, 21, 22, 23} gives 0.063 vs 0.066 for the standard N = 20. The cross-boundary
  coupling Σd² from ranks 20–40 onto the N = 20 cluster is 5.7e10 s⁻², larger than a's whole inner shell.

## 4. Hybrid adversary estimates (INFERENCE; `verify_summary.json` → `hybrid_estimates`)

F_∞ ≈ H_∞ + X_{N_last}. For comparison, the lane's F_∞ fits are given as (1/N on all points / 1/N on the last 3 /
exponential):

| series | X flat? | hybrid F_∞ | lane F_∞ fits |
|---|---|---|---|
| p19, 320 µs, site 1 | yes | 0.071 | −0.025 / 0.080 / 0.133 |
| p19, 320 µs, site 7 | yes | 0.154 | 0.041 / 0.122 / 0.241 |
| p245, 320 µs, site 1 | yes | 0.098 | −0.033 / 0.090 / 0.193 |
| p245, 320 µs, site 7 | yes | 0.059 | −0.158 / 0.014 / 0.153 |
| p245, 320 µs, site 9 | yes | 0.634 | 0.632 / 0.588 / −0.962 |
| p19, 320 µs, sites 8/9; p245, 320 µs, site 8 | **no (shell)** | 0.160 / 0.163 / 0.184 | not a σ-level estimate |

The lane's own fits scatter by 0.1–0.3 across models. The decomposition supplies the mechanism that selects among them.

## 5. Falsifiable prediction for the pending exact N = 22 runs (`predictions_N22.json`)

The governor's N = 22 runs use the same family and circuit. Prediction, made before they finish:
F_22 = H_22(CSD_22 + offset) + floor_22 + X_20.

| series | decomposition | 1/N law (F_20 · 20/22) |
|---|---|---|
| p19, 320 µs, site 1 | 0.148 | 0.142 |
| p19, 320 µs, site 7 | 0.230 | 0.217 |
| p19, 320 µs, site 8 | 0.236 | 0.223 |
| p19, 320 µs, site 9 | 0.239 | 0.225 |

- The decomposition's uncertainty is about ±0.005, plus |dX| on non-flat series. The N = 22 typicality noise is about
  0.0005.
- A result near the 1/N column on the flat series (sites 1 and 7) would falsify the "X is flat" hypothesis.
- CSD predicts that the larger H step comes at N = 22 → 24 (0.061 → 0.047 at 320 µs).

## 6. Attacks this verification did not close

- **X beyond N = 20 is unverified.** This matters most.
- A b-aware or {a} ∪ b-centred cluster family was not run (the `pairb` / `custom` options exist in `decomp_echo.py`).
- An embedded X (exact core plus a CSD bath) was not tried; the sibling lane `r1sim_hybrid_plus` found such hybrids fail
  at finite N.
- The CSD offset is assumed transferable from N = 20 to N_c ≥ 80.
- Single field orientation; 1UBQ only.
- The Trotter offset on H was measured at N = 12 only.

## 7. Resource ledger

| field | value |
|---|---|
| Compute | about 36 single-thread CPU-min in total (about 13 of them in the timed-out `trotter_H.py`); every run ≤ 0.3 GB RSS; OMP/MKL/OPENBLAS = 1 |
| Process note | the tool auto-moved `trotter_H.py` to the background after 600 s. It was bounded by `timeout 800`, and I waited for it to exit before running anything else |
| Quantum resources | none. Simulator time is not physical quantum time |
| Leakage | none. The native geometry defines the physical instance only |
| Files | `decomp_echo.py`, `validate_decomp.py` → `validate_decomp.json`, `csd_hydro.py`, `trotter_H.py` → `trotter_H.json` (partial), `analyze_verify.py` → `verify_summary.json`, `predict_N22.py` → `predictions_N22.json`, `runs/` (exact H ladders, CSD runs) |
