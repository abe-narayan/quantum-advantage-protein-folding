# ROUND3 lane: hardness_what_it_takes

_2026-09-28. What quantum speedup would the measured classical hardness of the A80 learned energy require, and is that hardness real?_

Tags: MEASURED (this lane, files below), DERIVED (algebra in `what_it_takes.py`), LITERATURE-SUPPORTED, INFERENCE, UNPROVEN.

Native structures appear only as ORACLE labels (fields ending `_ORACLE`, RMSD to native). They were never used in a success criterion, in selection or in seeding. Every arm here is on the DEP path: the DG seeds use only the distogram fields `expected` and `sd`, and `prob` for the draws.

## Verdict: KILLS

1. The measured multistart hardness, p_hit(best mode) ~ exp(−0.041 L) after censoring, is **not** the cost of the best classical method. It is mostly an artefact of three things:
   - random-prior initialisation;
   - an unsaturated, moving census target;
   - under-relaxed 200-iteration endpoints.
2. A native-free distance-geometry (DG) seed plus L-BFGS takes 2 descents, about 410 energy+gradient evaluations and 0.3 s of O(L³) embedding. It reaches the best-known energy on 8/16, 11/16 and 14/16 crops at L = 60, 100 and 150 (MEASURED).
3. The best classical portfolio measured reaches the best-known basin at a median of 420 evaluations at L = 100 and L = 150, and at most 5.8×10⁴ at L = 150 (MEASURED).
4. Against that portfolio, no speedup exponent (s = 2, 3, 4, or exponential) is viable at any L ≤ 500 at logical Toffoli times ≥ 1 µs (DERIVED).
5. A plausible (s, hardware) pair exists at L ≤ 300 only in the hypothetical scenario that extrapolates the no-bypass multistart. That scenario needs s ≥ 4 at L = 300 (break-even at t_T ≈ 2.1 µs; ≈ 12 days per solution at 1 µs) or an exponential speedup with ~10 coherent steps. The DG bypass measured here refutes the scenario.

## Pre-registration (stated before the runs, in the task)

| Field | Content |
|---|---|
| Hypothesis | The G1 hardness (p_hit decay, 0 NRPT round trips) is intrinsic, so a quantum speedup exponent s could pay off at L ≤ 300. |
| Comparator | Random-prior multistart (census), λ-path NRPT, DG seeding. |
| Kill | A polynomial classical bypass reaches the best basins, or no plausible (s, hardware) pair exists at L ≤ 300. |
| Verdict rule | INTERESTING only if a plausible pair exists at L ≤ 300 **and** there is no classical bypass. |

## (1) Classical cost-to-solution C_c(L): `cost_fit.py` → `cost_fit.json`

| Task | Best measured method | C_c (energy+gradient evaluations) | Status |
|---|---|---|---|
| **T-own:** hit the census' own best 2-Å cluster | random multistart | Median 1.5×10³ (L=30), 1.5×10⁴ (L=100), 5.5×10⁴ (L=150; 16/16 crops at the 1/256 floor). Tobit fit (censored): log p = −0.69 − 0.0415 L; exponential beats power law by ΔBIC = 12.9. Extrapolated: 2.7×10⁴ (L=100), 1.7×10⁶ (200), 1.1×10⁸ (300), 4.3×10¹¹ (500). | MEASURED + INFERENCE (extrapolation). **Moving target:** at R = 2048 the "best" changed on 4/8 crops (p fell to 1/2048). The census is unsaturated (new-mode rate ≈ 1), so the best-of-R cluster is hit once by construction. |
| **T-ref:** reach E ≤ E_ref + 20, where E_ref is the lowest energy found on the crop by any method | portfolio: DG-E1 → DG draws → multistart → NRPT | Median 2.4×10³ / 420 / 420 at L = 60 / 100 / 150. Maximum 2.0×10⁶ / 4.8×10⁵ / 5.8×10⁴ (the maxima are crops where only NRPT reached E_ref). Cost does not grow with L (power fit exponent −1.6), because DG's success rises with L. | MEASURED. E_ref is the best *known* energy, not a certified minimum. |
| **T-fold:** land within 3 Å of the best-known polished fold | DG-E1 (370–430 evaluations), or random multistart | Per-restart p_fold(3 Å) = 0.34, 0.09, 0.33, 0.06 (8AXJA_100, 3GAHA_100, 2AB0A_150, 3M3PA_150), so C_ms,fold = 6.4×10²–3.5×10³ | MEASURED on 4 crops (64 restarts each). Fold finding is **not** exponentially hard at L ≤ 150. |
| **T-samp:** one decorrelated T=1 posterior sample | λ-path NRPT | Right-censored: 0 round trips at L ≥ 80 for T = 1–8. 95% lower bounds per trip: 1.1×10⁵ (L=60), 3.0×10⁵ (L=80), 9.1×10⁴ (L=100), 6.5×10⁴ (L=120), 5.7×10⁴ (L=150). | MEASURED lower bounds only. No method gives an upper bound at L ≥ 80. |

## (2) DG seeding replication: `dg_replicate.py`, `analyze_dg.py`, `polish_check.py`, `ms_polish.py`

- **Implementation (independent of the exploratory scratchpad code).** For each crop:
  - D = `expected` (distogram mean);
  - DG-E0 = classical MDS only;
  - DG-E1 = classical MDS, then weighted SMACOF with W = 1/(sd² + 0.25);
  - DG-D = 10 per-pair distogram draws → SMACOF.
  - Both chiralities are tried → internal coordinates → the same 200-iteration batched L-BFGS as the census.
  - 48 crops: 16 chains × L = 60/100/150. About 14 CPU-min in total.
- **Energy-level result (MEASURED, δ = 20 nats).**

  | L | DG-E1 reaches E_ref | median E_DG-E1 − best other method | median E_DG-E1 − census-256 best | DG-E1 cost | census-256 cost |
  |---|---|---|---|---|---|
  | 60 | 8/16 | +36 | +24 | 412 evaluations | 5.2×10⁴ |
  | 100 | 11/16 | −145 | −161 | 406 | 5.5×10⁴ |
  | 150 | 14/16 (15/16 with draws) | −1012 | −1048 | 418 | 5.5×10⁴ |

- **Plain classical MDS (DG-E0, the literal task recipe) is not a bypass.** It reached E_ref on 0/48 crops. The weighted-SMACOF step, which uses the distogram sd, is load-bearing (MEASURED).
- **Adversarial check 1: relaxation.** 200-iteration endpoints are under-relaxed.
  - +800 iterations lower DG-E1 minima by a median of 9 / 27 / 86 nats (L = 60 / 100 / 150), with a maximum of 187.
  - The same polish lowers the best of 64 fresh random restarts by 600–1,550 nats at L = 150 (MEASURED).
- **Symmetric polish (`ms_polish_results.json`, `ms_polish_fold.json`; 8 crops).** Both sides get +800 iterations, and the DG side costs 30–40× less.
  - DG-E1 is still lower on 5/8 crops: −541, −411, −306, −436 (L=150) and −387 (L=100).
  - In 4 of those 5 it lies in the **same fold** as the best random restart (1.4–1.9 Å CA-RMSD, native-free).
  - It loses on 3GAHA_150 (+1214, a different and better fold found by multistart), 3GAHA_100 (+507) and 5O37A_150 (+47, a different fold).
  - So after symmetric polishing, DG's advantage at L = 150 shrinks from the 380–1,430 nats seen against the unpolished census to 300–540 nats. Most of the ~10³-nat census gap is under-relaxation. The remainder is genuine sub-basin depth within the same fold.
- **Basin identity vs NRPT (native-free).**
  - 5O37A_100: polished DG and polished NRPT fall in the same basin (1.1–1.2 Å), with DG 20752 vs NRPT 20755. DG reaches for ~640 evaluations what NRPT reached for ~5×10⁵–10⁶.
  - 4LPQA_60: same basin (1.8 Å), but NRPT is 79 nats deeper.
  - 3GAHA_60 and 5O37A_150: different basins, and NRPT's is deeper.
- **Transmission (ORACLE).**
  - At L = 150 the DG-E1 minimum has lower RMSD than the census best on 12/16 crops, but the median gain is only 0.19 Å. Mean RMSD is 6.24 vs 6.19 Å, because 3GAHA_150 loses 3 Å.
  - Where DG and multistart share a fold, the 300–540-nat energy gain buys 0.1–0.5 Å.
  - DG success does not correlate with native-free distogram confidence: Spearman 0.16, p = 0.27, n = 48.
- **Conclusion (MEASURED at L ≤ 150).**
  - The exponential p_hit decay is a property of random-prior initialisation plus 200-iteration relaxation, not an intrinsic cost of reaching the best basins.
  - A polynomial classical method (O(L³) embedding + O(10²) O(L²) evaluations) reaches or beats every other method's best energy on most crops at L ≥ 100. Its success rate *rises* with L.
  - The residual: DG misses the best basin on 2/16 crops at L=150 and 5/16 at L=100. A 64–256-restart multistart (1.4–5.5×10⁴ evaluations) covers them, so the portfolio stays ≤ 5.8×10⁴ at L = 150.
  - The exploratory claim "DG reaches the deepest known basin in 61/64 runs" was a mis-transcription. The source says the expected-distance pair gave the lowest *DG* basin in 61/64 runs. The corrected, replicated statement is the table above.

## (3) What it would take: `what_it_takes.py` → `what_it_takes.json`, `what_it_takes_table.md`

- **Model (DERIVED; generalises K-101).**
  - Quantum steps N_q = K n_b C_c^{1/s}, each costing G(L) Toffolis at t_T.
  - Break-even Toffoli time: t_T^be = c C_c^{1−1/s}/(AρK n_b G).
  - At break-even the landscape-independent floor becomes B*_s = X^{s/(s−1)} and T*_Q,s = K n_b G t_T · X^{1/(s−1)}, with X = AρK n_b G t_T / c. s = 2 reproduces K-101. Exponential speedup: N_q = K n_b (P = 1) or K n_b L.
- **Inputs.**
  - G(L) from T3 §4.2: D2 generous 9.3×10⁷ / 4.2×10⁸ / 1.0×10⁹ / 3.1×10⁹ and D2 central 3.1×10⁸ / 1.4×10⁹ / 3.4×10⁹ / 1.0×10¹⁰ at L = 100/200/300/500. Values beyond L = 200 are a power-law extrapolation (INFERENCE).
  - c(L) measured single-core, batched: 0.63 / 1.6 / 4.6 / 8.4 ms at L = 60/100/150/200 (fit ∝ L^2.19). The machine was loaded, so these values are larger than on an idle core, which is quantum-favourable. T2's A-c values are 1.8–6× smaller.
  - Overhead scenarios: MO (K=10, n_b=1, A=ρ=1, D2 generous) and CE (K=100, n_b=2, D2 central).
- **Required-hardware table (MO overheads).** Each cell is the logical Toffoli time needed both to break even and to finish in ≤ 30 days per solution. "Plausible" means t_T ≥ 1 µs. The CE and D3 rows are in `what_it_takes_table.md` and `what_it_takes.json`.

  | classical cost scenario | L | C_c | T_c | s=2 | s=3 | s=4 | exp (10 steps) | min plausible s |
  |---|---|---|---|---|---|---|---|---|
  | BEST (portfolio, median; MEASURED at 100/150) | 100 | 4.2e2 | 0.8 s | 40 ps | 0.11 ns | 0.18 ns | 0.82 ns | none |
  | | 200 | 5.6e2 | 4.6 s | 47 ps | 0.13 ns | 0.23 ns | 1.1 ns | none |
  | | 300 | 8.4e2 | 17 s | 58 ps | 0.18 ns | 0.31 ns | 1.7 ns | none |
  | | 500 | 1.4e3 | 86 s | 75 ps | 0.25 ns | 0.46 ns | 2.8 ns | none |
  | BEST (portfolio, worst crop, ×(L/150)²) | 100 | 5.8e4 | 100 s | 0.47 ns | 2.9 ns | 7.3 ns | 110 ns | none |
  | | 300 | 2.3e5 | 1.3 h | 0.96 ns | 7.5 ns | 21 ns | 460 ns | none |
  | | 500 | 6.4e5 | 11 h | 1.6 ns | 15 ns | 45 ns | 1.3 µs | exp only |
  | HYPOTHETICAL no-bypass (T-own extrapolated) | 100 | 2.7e4 | 49 s | 0.32 ns | 1.8 ns | 4.1 ns | 53 ns | none |
  | | 200 | 1.7e6 | 3.9 h | 2.6 ns | 28 ns | 93 ns | 3.4 µs | exp only |
  | | 300 | 1.1e8 | 25 d | 21 ns | 450 ns | **2.1 µs** | 210 µs | **s = 4** |
  | | 500 | 4.3e11 | 800 yr | 0.13 ns (30-day cap) | 11 ns | 110 ns | 85 µs | exp only |

- **Generalised floor (MO, t_T = 1 µs; landscape-independent).**

  | | L=100 | L=300 | L=500 |
  |---|---|---|---|
  | s = 2: B* / T*_Q | 2.6×10¹¹ / 15 yr | 2.5×10¹¹ / 160 yr | — / 480 yr |
  | s = 3: B* / T*_Q | 3.6×10⁸ / 7.6 d | — / 82 d | — |
  | s = 4: B* / T*_Q | 4.1×10⁷ / 21 h | — / 9.2 d | — / 28 d |

  The CE overheads are 3–4 orders worse (s=2 at L=100: 6.7×10⁴ yr). B*_s is almost independent of L, because G and c both scale ≈ L^2.2.
- **Reading (DERIVED + INFERENCE).**
  - Against the best classical method actually measured, even an exponential speedup with 10 coherent walk steps loses at every L ≤ 500 unless t_T ≤ 0.8–2.8 ns. The per-step oracle cost alone (G ≈ 10⁸–10⁹ Toffolis) exceeds the whole classical solution.
  - A plausible pair at L ≤ 300 appears only in the hypothetical no-bypass extrapolation, at s = 4. No quantum algorithm with a super-quadratic speedup is known for this white-box pair-additive energy (ADVANTAGE_CONDITIONS A3/A4; T5).
  - With the non-faithful D3 target (sensitivity only), s = 3 at L = 300 also becomes plausible in that same hypothetical scenario.
  - T=1 posterior sampling remains classically unresolved (lower bounds only). Its break-even needs C_samp ≥ 4×10⁷ (s = 4) to 2.6×10¹¹ (s = 2) evaluations per sample at L = 100. The measured lower bounds sit 2.6–6.5 orders below that, and the ORACLE value of resolving sub-basins within a fold is 0.1–0.5 Å.

## Claim levels

- **Theoretical.** The generalised floor T*_Q,s is L2 (DERIVED, conditional on T3's G(L) and the walk-overhead model). No separation of any exponent is proven or known for this energy family: L0 for s ≥ 3.
- **Practical: L0.** The best classical method (DG portfolio) costs 4×10²–6×10⁴ evaluations at L ≤ 150.
  - Against the median crop, every quantum route needs ≤ 3 ns logical Toffolis at any exponent, up to L = 500.
  - Against the worst crop, extrapolated ×(L/150)², any finite s ≤ 4 needs ≤ 45 ns up to L = 500.
  - Only an idealised 10-step exponential algorithm, on the worst crop at L = 500, crosses 1 µs (1.3 µs). No such algorithm is known.

## Resource accounting (this lane)

- Single-threaded runs:
  - DG replication: 48 crops, ≈ 14 CPU-min, peak RAM < 1 GB;
  - analysis with NRPT polish recomputation: 2 × 1.5 min;
  - polish check: 1.7 min;
  - symmetric multistart: 6 + 4 crops, 64 restarts each: ≈ 12 min;
  - c(L) benchmark: 2 × 1 min.
- Total ≈ 33 CPU-min, all on the loaded machine.
- No quantum resources were simulated. All quantum figures are DERIVED from T3's G(L); simulator runtime is not involved.

## Files

- **Scripts:** `dg_replicate.py`, `analyze_dg.py`, `polish_check.py`, `ms_polish.py`, `bench_c.py`, `cost_fit.py`, `what_it_takes.py`.
- **Results:**
  - `dg_results_A.json`
  - `dg_summary.json`
  - `polish_results.json`
  - `ms_polish_results.json`
  - `ms_polish_fold.json`
  - `bench_c.json`
  - `cost_fit.json`
  - `what_it_takes.json`
  - `what_it_takes_table.md`
  - `endpoints/*.npz` (DG endpoints)
  - `endpoints_ms/*.npz` (multistart endpoints for the fold test)

## What would reopen this (all needed)

1. A protein-structure task where the best classical portfolio, including DG / mode-finding bypasses and symmetric polishing, needs ≥ 4×10⁷ evaluations per solution at L ≤ 300 (for s = 4; ≥ 3.6×10⁸ for s = 3).
2. A quantum algorithm with s ≥ 4 for that task, with a named escape route (A4).
3. Evidence that solving the task transmits ≥ 1 MDE of structural accuracy (A8). Sub-basin depth within a fold does not: 0.1–0.5 Å.
