# verify_classical: classical-adversary check of the ROUND4 `tx_early` claim

_2026-09-28. Adversarial verifier (classical). Instrument unchanged: 1UBQ p19/p245, sites b ∈ {1, 7, 8, 9}, orientation
0, reference first-order Trotter circuit (dt = 2 µs), b0 = random_b0(1000), γ = 0, flip-folded sector typicality,
complex64, seed 4242. Category 3 (physics simulation) only. Nothing here touches K-105 or K-116._

Tags: **MEASURED** (file in this folder), **DERIVED**, **INFERENCE**, **UNPROVEN**.

## Verdict: REFUTED in its central scientific statement; the procedural KEEP OPEN stands

The lane's 40 µs statement is: "the exact finite-cluster echo F_N is already converged, since it moves ≤ 0.0026 over
N = 18→22 on all 8 series". That statement **fails a cross-family check**, which Round-4 H-2 requires for any
convergence claim. The lane had none.

1. **Why the probe-centred ladder plateaus.** The probe-centred family orders spins by distance from a. It adds the
   dominant dipolar partners of peripheral instrument sites only at ranks 24–48, so the ladder plateaus without ever
   containing b's own strongest coupling [MEASURED, `geometry.json`]. Fraction of b's second moment inside probe
   N = 22:
   - p19 b8: 15.6%. Its methyl partner HG23/ILE3 is rank 24, with d = 127 krad/s and 81.5% of M2_b.
   - p19 b9: 22.6%. HG2/GLU16 is rank 26 (64%).
   - p245 b7: 28.4%. HG3/LYS27 is rank 48 (49%).
2. **Adding those partners moves F at 40 µs by +0.025 (p19 b8, 2.5σ) and +0.065 (p245 b7, 6.5σ)** [MEASURED]. The
   shift is robust on four axes:
   - **Confound removed.** Compare the N = 22 cluster "probe ranks 0–19 + 2 b-partners" with probe ranks 0–21. Adding
     ranks 20–21 moved F by ≤ 0.0015.
   - **Stable in N.** The site-aware family gives 0.9776 / 0.9776 / 0.9775 (p19 b8) and 0.7653 / 0.7653 / 0.7651
     (p245 b7) at N = 18 / 20 / 22.
   - **Independent family agrees.** ROUND3 `pairb` (20 nearest to {a, b}, different spins and different Trotter order)
     gives 0.9720 and 0.7600. With 4 partners instead of 2 the values are 0.9734 and 0.7610.
   - **Not a Trotter artefact.** The shift is the same at dt = 1 µs: +0.0261 vs +0.0248, and +0.0661 vs +0.0662.
   - **Not noise.** Typicality noise is about 0.001–0.002.
3. **Consequences for the claim's sub-statements:**
   - "F within σ/4 of every larger cluster tested" / "exact simulation of 18–22 spins reaches the converged echo within
     σ/4" (claim's practical level): **false for the family the claim used.**
   - "CRITIC-C1's 3–8σ gap at 40 µs is an artefact of the estimator": **not supported.** Against the b-aware values, the
     probe-family finite echo is still 2.5σ and 6.5σ off on 2/8 series. The mechanism is different: b-local missing
     partners, not the floor. So C1's substantive conclusion survives on those series: probe-centred finite clusters
     are not σ-accurate forward models inside T3. The lane's point that the b-independent floor is bookkeeping is not
     contradicted by these data.
   - The back-test (flat-F beats the X-hybrid, 8/8) is arithmetically correct (re-derived exactly). But it is an
     in-family comparison. Against the b-aware reference at 40 µs:
     - flat-F (probe F₂₂): rms 0.025, max 0.065, 6/8 within σ;
     - hybrid (H_∞ + X₂₂): rms 0.051, max 0.080, 0/8 within σ.
     Neither validates convergence.
   - The physical argument ("added spins carry flip-flop strings that commute with Z_b, so F is insensitive") holds
     only for spins far from both a and b. It is **falsified for spins near b** [MEASURED].
4. **80–120 µs: "open" stands, but the finite-size uncertainty is about 10× larger than quoted.**
   - The claim quotes a probe-family drift of ≤ 0.011 per ΔN = 2.
   - The actual probe versus b-aware differences are +0.096 (p19 b8, 80 µs), +0.155 (p19 b8, 120 µs), +0.115 / +0.100
     (p245 b7, 80 / 120 µs), and −0.050 (p245 b9, 120 µs). The last is partly the known rank-19 shell event.
   - The two b-aware families disagree with each other by 0.037–0.072 at 80–120 µs, so no σ-level classical route is
     demonstrated there [MEASURED]. No evidence for quantum necessity either.
5. **What survives.**
   - All of the lane's own numbers (re-derived exactly, `recheck_numbers.json`).
   - The procedural result: the rule did not fire → KEEP OPEN.
   - The observation that X_N is not an independently converging quantity. It is b-independent bookkeeping in-family.
   - Levels L0 / L0.
   - "No quantum resource is needed at 40 µs" plausibly survives, in corrected form: a b-aware exact cluster of ≤ 22
     spins gives F stable to ≤ 0.005 across N = 18→22, 2→4 partners and the pairb family, on every series tested
     [MEASURED stability; convergence beyond N = 22 is INFERENCE, not shown by an F̂_∞]. It costs about 1–8 single-thread
     CPU-min per site and time.

## 1. What was run

| check | script | result |
|---|---|---|
| Independent re-derivation of all headline numbers from the raw runs (no lane analysis code imported) | `recheck_numbers.py` → `recheck_numbers.json` | **all reproduced.** Minor: max\|F_N − F₂₂\| over N = 18–22 on p19 b1 is 0.0032 if the reference F₂₀ is used (0.0026 with the lane's own F₂₀) |
| Where the strong partners of a, b sit in the probe ordering; M2_b coverage | `geometry.py` → `geometry.json` | see verdict 1 |
| Wrapper validation: `run_custom.py` (which reuses `tx_echo.run` unchanged; patches only the cluster loader and the output directory) with spec `probe:18`, site 8, vs the lane's N = 18 run | `validate_wrapper.json` | **bit-identical** (ΔF = ΔH = Δfloor = 0.0) |
| Site-aware family `bpart:n0:m`: probe ranks 0..n0−1 + the m strongest-\|d_bc\| missing partners of b | `run_custom.py` | N = 18 (16:2) and N = 20 (18:2) at 40/80/120 µs, all 8 series; N = 20 (16:4) at 40 µs, all 8; N = 22 (20:2) at 40 µs for p19 b8 and p245 b7 |
| Independent family `pairb:20` (ROUND3 decomp_echo definition) | `run_custom.py` | p19 b8, p245 b7 at 40/80/120 µs |
| Trotter check dt = 1 µs (probe:20 and bpart:18:2) | `run_custom.py --dt-us 1` | the partner shift is unchanged to ≤ 0.0013 |
| Cross-family comparison | `compare_families.py` → `verify_summary.json` | tables below |

## 2. Results [MEASURED, `verify_summary.json`]

Δ = site-aware best (largest N) − probe-family best (F₂₂ at 40 µs; F₂₀ at 80 µs; F₂₀ for p19 / F₁₈ for p245 at 120 µs).
σ = 0.01.

**40 µs (inside every T3 estimate)**

| series | M2_b in probe₂₂ | probe F₂₂ | SA2 N = 18 / 20 / 22 | SA4₂₀ | pairb₂₀ | Δ |
|---|---|---|---|---|---|---|
| p19 b1 | 0.95 | 0.6031 | 0.6002 / 0.6011 / – | 0.6008 | – | −0.0020 |
| p19 b7 | 0.82 | 0.8731 | 0.8742 / 0.8730 / – | 0.8729 | – | −0.0002 |
| **p19 b8** | **0.16** | 0.9526 | 0.9777 / 0.9776 / 0.9775 | 0.9734 | 0.9720 | **+0.0249 (2.5σ)** |
| p19 b9 | 0.23 | 0.9529 | 0.9439 / 0.9441 / – | 0.9488 | – | −0.0088 |
| p245 b1 | 0.64 | 0.9790 | 0.9778 / 0.9776 / – | 0.9767 | – | −0.0014 |
| **p245 b7** | **0.28** | 0.7005 | 0.7653 / 0.7653 / 0.7651 | 0.7610 | 0.7600 | **+0.0646 (6.5σ)** |
| p245 b8 | 0.67 | 0.9550 | 0.9570 / 0.9568 / – | 0.9557 | – | +0.0017 |
| p245 b9 | 0.90 | 0.9726 | 0.9723 / 0.9723 / – | 0.9721 | – | −0.0004 |

**80 and 120 µs (inside only the generous T3)**

| series | 80 µs: probe₂₀ / SA2₂₀ / pairb₂₀ | Δ₈₀ | 120 µs: probe / SA2₂₀ / pairb₂₀ | Δ₁₂₀ | SA2 step 18→20 (80 / 120) |
|---|---|---|---|---|---|
| p19 b1 | 0.3753 / 0.3739 / – | −0.001 | 0.2788 / 0.2822 / – | +0.003 | −0.001 / −0.005 |
| p19 b7 | 0.5220 / 0.5277 / – | +0.006 | 0.4865 / 0.4675 / – | −0.019 | −0.007 / −0.010 |
| p19 b8 | 0.8105 / 0.9061 / 0.8693 | **+0.096** | 0.6456 / 0.8010 / 0.7290 | **+0.155** | −0.001 / −0.001 |
| p19 b9 | 0.7500 / 0.7459 / – | −0.004 | 0.5600 / 0.5423 / – | −0.018 | −0.001 / +0.000 |
| p245 b1 | 0.7644 / 0.7671 / – | +0.003 | 0.4936 (N18) / 0.5000 / – | +0.006 | +0.004 / +0.013 |
| p245 b7 | 0.4200 / 0.5348 / 0.4644 | **+0.115** | 0.2674 (N18) / 0.3676 / 0.3050 | **+0.100** | +0.000 / +0.003 |
| p245 b8 | 0.7790 / 0.7897 / – | +0.011 | 0.6116 (N18) / 0.6188 / – | +0.007 | −0.004 / −0.018 |
| p245 b9 | 0.9275 / 0.9173 / – | −0.010 | 0.8957 (N18) / 0.8455 / – | −0.050 | −0.002 / −0.009 |

**Counts of |Δ| > σ:** 40 µs 2/8, 80 µs 4/8, 120 µs 5/8. The site-aware steps are < σ at 80 µs on 8/8. But pairb
and SA2 disagree by 0.037–0.072 at 80–120 µs on the two tested series, so the site-aware step-stability there is not
cross-family confirmed.

**Trotter (40 µs, N = 20, Δ = SA2 − probe):** p19 b8 +0.0248 (dt 2 µs) vs +0.0261 (dt 1 µs); p245 b7 +0.0662 vs
+0.0661.

**Independent concordance** (read-only, not my run). The sibling verifier `../verify_relevance/crossfamily.json` found
the same p19 b8 shift at 40 µs by two routes:
- swapping ranks {18, 19} for {24, 26}: +0.0249;
- adding rank 24 alone to probe N = 20: +0.0248.

Both used common random numbers. Its p19 b9 value (−0.0075) matches this verifier's −0.0088.

## 3. Interpretation

- **Mechanism** [INFERENCE]. F_ab = 1 − 2 w_b^⊥(t), where w_b^⊥ is the weight of Z_a(t) on strings with X/Y at b. A
  strong partner c of b does two things:
  - it converts transverse weight arriving at b into b–c flip-flop strings (such as Z_b X_c) that commute with Z_b;
  - it detunes, through the large Z_bZ_c splitting, the weaker flip-flop routes that feed b.

  Both raise F, which matches the + sign on p19 b8 (d_bc = 127 krad/s) and p245 b7 (46 krad/s). The lane's
  "far-spin" argument is correct only for spins far from both a and b.
- **Structural cause** [DERIVED from the instrument definition]. `instrument_bs` selects sites 7, 8 and 9 as the three
  farthest members of the N = 10 core. A probe-centred ladder therefore covers their neighbourhoods last. Every
  Round-3/Round-4 statistic built on that ladder (step rules, X-flatness, the T-X hybrid, the back-test) inherits this
  blind spot for peripheral sites.
- **Pre-registered rule.** It is unaffected: it did not fire, so KEEP OPEN. But it was also defined on the probe
  family, so even a "pass" would not have established convergence on p19 b8 or p245 b7.

## 4. Recommendations

1. Replace probe-centred ladders with **b-aware union ladders**, i.e. {a-shell} ∪ {b-shell}, grown jointly, plus
   `pairb` as the cross-family check. Report F̂_∞ from those. At 40 µs this appears to be a classical route at about
   σ/2.
2. For 80–120 µs, the families disagree by 4–7σ at N = 20. Grow b-aware union clusters to N = 22–24, or run the
   spinDMFT adversary (CRITIC A-2), before any "open/closed" statement.
3. Correct the lane's wording. "F_N already converged at 40 µs on all 8 series" should read: "probe-family plateau;
   b-aware families shift 2/8 series by 2.5σ and 6.5σ". "CRITIC-C1's gap is an estimator artefact" should read: "the
   floor part is bookkeeping, but probe clusters remain > 2σ off on sites with out-of-cluster partners".
4. SCIENTIFIC_MEMORY candidate: "a flat ladder in one cluster family is not convergence. Check that the observable
   sites' own dominant couplings are inside the cluster."

## 5. Resource ledger

| field | value |
|---|---|
| CPU | 3548 single-thread CPU-s ≈ 59 CPU-min across all dynamics runs (`cpu_s` summed over `runs/*.json`). Analysis scripts < 10 s. Largest runs: 431 s and 470 s (N = 22, 40 µs, one site); every run ≤ 8 CPU-min |
| Threads | OMP / MKL / OPENBLAS = 1. Foreground only; every invocation had a `--wall-s` stop; `tx_echo.run` checkpoints after every leg (atomic), so all runs are resumable |
| Peak RAM | 1.52 GB (N = 22); N = 20 runs 0.37 GB |
| Quantum resources | none. Simulator time is not physical quantum time |
| Leakage | none. The native geometry defines the physical instance only. Partner selection uses \|d_bc\| from that same geometry (instrument definition), with no fitting to outcomes |
| Files touched | only `ROUND4/tx_early/verify_classical/`. The lane's `runs/` and checkpoints were read, never written. No commit |

## 6. Files

- `recheck_numbers.py` → `recheck_numbers.json`
- `geometry.py` → `geometry.json`
- `run_custom.py`: driver (monkeypatched `tx_echo.run`; specs `probe:N`, `bpart:n0:m`, `custom:n0:r,…`, `pairb:N`;
  `--dt-us`)
- `validate_wrapper.json`
- `compare_families.py` → `verify_summary.json` (all cells, Δ, counts, claim-model errors, M2_b coverage)
- `runs/`: result JSONs, checkpoints and npz forward vectors. The N = 20/22 site-aware runs can be resumed or extended
  by re-running the same command.
