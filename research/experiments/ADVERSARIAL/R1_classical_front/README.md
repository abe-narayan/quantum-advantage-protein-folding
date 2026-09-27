# R1 adversarial lens: classical front (new classical echo adversaries)

_2026-09-27. Lens agent "classical_front". Scope: attack the only surviving lead R1 (NMR echo window) with classical
estimators of the first-order OTOC F_ab(t) that are not yet in the panel._

**Bottom line.** None of the four new estimator families reaches t_c ≥ 160 µs on all three clusters at polynomial
cost. None of them even beats the panel's 80 µs at polynomial cost. **The kill rule did not fire.** (MEASURED)

A light-cone diagnostic found something else. The N=10 exact echo is not converged in cluster size inside the window.
Adding the 11th and 12th nearest protons changes F_ab by more than 0.01 at 40–120 µs, and by up to 0.14 (14σ) within
[80, 320] µs. Every one of the 10 spins shifts F_ab by more than 0.01 at 20–160 µs. The echo in the window is a
collective property of at least 12 spins, so the N=10 cluster is not the physical observable there. (MEASURED)

Verdict: **SUPPORTS**, in the narrow sense that the approximation-hardness of the N=10 echo window survives four more
adversary families. Theoretical level L1: empirical failure of approximations. There is no complexity separation, and
exact simulation at N=10 still costs about 1 CPU-s. Practical level L0.

## Setup (identical to `scripts/nmr_gate.py`)

- **Clusters:** 1UBQ probe 19, 1UBQ probe 245, 1PGA probe 390. N=10 nearest protons, orientation 0 (b0 = random_b0(1000)), γ = 0.
- **Observed spins:** bs = 3 farthest + nearest = local indices [1, 7, 8, 9] in all three clusters.
- **Circuit:** first-order Trotter, dt = 2 µs, 160 steps, fixed pair order, recorded every 20 µs (0–320 µs).
- **Reference:** `qapf.nmr.spins.sector_exact_correlators` with `otoc=True`, about 1.1 CPU-s per cluster at N=10. It is cached in `out/ref_*.json`.
- **Failure time:** t_c = first recorded t where max_b |F_est − F_exact| > 0.01.
- **Kill rule (task card):** t_c ≥ 160 µs on all three clusters with cost polynomial in N.
- **Panel best for the echo (existing RAW, `research/results/RAW/nmr_gate/`):** `pauli_eps0.0001`, which fails at t_c index 4 = 80 µs.

## Estimators tested

| ID | Estimator | Cost model | Script |
|---|---|---|---|
| E1 | **Cluster-correlation expansion (CCE) of the OTOC.** Exact sub-cluster OTOCs on all subsets {a,b} ∪ C, combined by Möbius inversion with an additive link or a multiplicative (log) link, truncated at order k = \|C\| (sub-cluster size k+2). Plus a "nested" baseline: one sub-cluster of the spins most strongly coupled to {a} ∪ bs. | Σ_{j≤k} C(N−2, j) exact sims of ≤ k+2 spins. Polynomial at fixed k. | `cce_otoc.py` |
| E2 | **Operator-spreading stochastic model** (task item b), in microscopic form. The incoherent Pauli-path Markov chain replaces each Pauli rotation by P→P (cos²2λθ) or P→G·P (sin²2λθ), i.e. it drops all cross-terms between paths; its coarse-grained limit is FKPP operator-weight spreading. Parameter-free (λ=1), or (λ, memory block n_c) calibrated on the **N=8 exact echo of the same probe** (no N=10 data used). Also a product-state (mean-field) closure of the same chain. | O(M · gates) trajectories. Polynomial. | `opspread_mc.py` |
| E3 | **Sparse Pauli propagation with unbiased stochastic reinsertion** (task item c; Monte-Carlo Pauli paths, FCIQMC-style stochastic rounding). Echo from independent replica pairs (U-statistic), plus a ratio (norm-corrected) form. String budget M with adaptive ε. | O(M · gates · R). Polynomial at fixed M. | `stoch_pauli.py` |
| E4 | **Tensor network: MPO / operator-TEBD of Z_a(t)** in the Pauli basis. Real MPS with local dim 4, the exact 16×16 Pauli-transfer matrix of each pair gate in the reference order, SWAP routing with tracked positions, Fiedler chain order, bond cap χ, normalised OTOC. Validated against exact at N=6, full χ: max error 4.6e-7. | O((gates+swaps) · χ³) per step. Polynomial at fixed χ. | `mpo_otoc.py` |
| — | Light-cone diagnostic: leave-one-out influence times and add-one/add-two (N=11, 12) cluster convergence. | exact | `influence.py` |

Task item (d) (Taylor + Padé) was not run. It needs the continuous-time model, which differs from the Trotter
reference, and the budget went to E1–E4.

## Results: t_c in µs (first 20 µs grid point where max_b error > 0.01)

| Estimator | 1UBQ p19 | 1UBQ p245 | 1PGA p390 | Cost / comment |
|---|---|---|---|---|
| panel best: sparse Pauli ε=1e-4 (existing RAW) | 80 | 80 (C2 RAW) | 80 | ~550–850 s, 1.4–1.7e5 strings |
| context: panel sparse Pauli ε=3e-5 (C2 RAW, `nmr_sparse/`) | none (> 320) | none (> 320) | not run | 1439–1910 s, **2.4–2.6e5 strings ≈ 4^10/4**: the full symmetry-allowed operator space, i.e. exact simulation in disguise (at N=8, 16.3k ≈ 4^8/4 = 16384). Not polynomial. |
| **E1 CCE additive, k=2** (≤4-spin sub-clusters) | 40 | 40 | 60 | 148 sub-sims |
| **E1 CCE add./mult., k=4** (≤6 spins) | 60 | 60 | 60 | 652 sub-sims |
| E1 CCE additive, k=6 (≤8 spins) | 60 | 80 | 100 | 988 sub-sims |
| E1 CCE additive, k=7 (≤9 = N−1 spins) | 80 | 100 | 120 | 1020 sub-sims. **Not polynomial:** order = N−3. |
| E1 CCE multiplicative, k=7 | 80 | 80 | 120 | same |
| E1 nested sub-cluster n=9 (strongest-coupled) | 40 | 40 | 60 | |
| E2 Markov chain, λ=1 | 20 | 20 | 20 | max error 0.60–0.62 |
| E2 Markov chain, (λ, n_c) fitted on N=8 | 20 | 20 | 20 | max error 0.30–0.57 |
| E2 mean-field (FKPP-type) closure, fitted | 20 | 20 | 20 | max error 0.43–0.94 |
| E3 stochastic Pauli, M=1e4, R=3 | 40 | — | — | error at 40 µs: 897 (unbiased) / 1.39 (ratio). 141 CPU-s. |
| E3 stochastic Pauli, M=3e3, R=3 | — | 40 | 40 | error at 40 µs: 104–165 / 1.3–2.7. 40 CPU-s (guard). |
| E4 MPO χ=16 | 40 | — | — | error at 80 µs: 0.35 |
| E4 MPO χ=32 | 40 | 40 | 40 | error at 60 µs: 0.06–0.13, at 80 µs: 0.15–0.26. ~55 CPU-s. |
| E4 MPO χ=64 (max 1024) | 40 | — | — | error at 60/80 µs: 0.10/0.21. Summed discarded weight 1.05. 239 CPU-s. |

At N=8 (`out/cce_N8.json`), CCE of order N−3 (7 of 8 spins) fails at 60–100 µs. The order needed for t ≥ 160 µs is the
full cluster at both N=8 and N=10. (MEASURED)

### Why each estimator fails (mechanisms)

- **E1 (CCE).** The echo does not factorise over sub-clusters. Removing **any single spin** from the 10-spin cluster
  shifts F_ab by more than 0.01 at some t ≤ 160 µs. For the most influential spin that happens at 20–40 µs; for the
  least influential at 100–160 µs (below). So every truncated expansion fails before max_c t_infl(c), which is 100–160 µs.
  Adding more orders does not converge before the full cluster. (MEASURED)
- **E2 (operator spreading).** Dropping path cross-terms turns coherent (ballistic, ∝ (nθ)²) weight transfer into
  gate-level diffusion (∝ nθ²). Coarse-graining the memory time and fitting λ cannot recover the coherent oscillations
  and revivals of F at the 0.01 level. (MEASURED; the mechanism is DERIVED)
- **E3 (stochastic Pauli paths).** The estimator stays unbiased, but independent rounding destroys the destructive
  interference between Pauli paths. The replica population's L1 norm and the pair-product variance then grow
  exponentially, a sign problem: error 10²–10³ by 40 µs and about 1e7 by 80 µs at M=1e4 (MEASURED). Without a cap,
  stochastic reinsertion keeps about ‖O‖₁/ε strings. The first uncapped attempt (ε=1e-3, R=4) had not produced the
  20 µs record after about 10 CPU-min and was stopped (MEASURED). The needed walker number is at the annihilation
  plateau, about the occupied operator space, roughly 4^N/4 here (INFERENCE, consistent with C3's 257k strings at N=10).
- **E4 (MPO).** The 10-proton cluster is effectively all-to-all in 3D. The operator entanglement of Z_a(t) grows
  toward volume law: the summed discarded weight exceeds 1 by 320 µs even at χ=64 (1/16 of the maximum 4^5), and the
  χ=16→32→64 gain is marginal (error at 60 µs 0.27→0.13→0.10). (MEASURED; "volume law" is INFERENCE from the discarded
  weight, not a measured entanglement spectrum)

## Light-cone diagnostic (`influence.py`, `out/influence_N10.json`)

| Cluster | leave-one-out t_infl over the 9 spins (µs): min / max | t_embed N=10→11 | t_embed N=10→12 | max \|F_12 − F_10\| in [80, 320] µs |
|---|---|---|---|---|
| 1UBQ p19 | 20 / 160 | 120 | 120 | 0.041 |
| 1UBQ p245 | 20 / 120 | 60 | 40 | 0.125 (N=11: 0.142) |
| 1PGA p390 | 40 / 100 | 100 | 80 | 0.114 |

(MEASURED.) Consequences:

1. **No sub-cluster or cluster expansion within the N=10 cluster can work.** Every spin matters at the 0.01 level by
   100–160 µs. (MEASURED)
2. **The N=10 exact echo is not the physical signal in most of the window.** The next one or two protons change it by
   up to 14σ from 40–120 µs onward. The 80 µs classical-failure time at N=10 falls exactly where the echo's dependency
   set outgrows the cluster. (MEASURED)
   - What this means for R1: the hardness evidence at N=10 is evidence about a truncated model. The relevant object is
     the echo of the converged light cone, which here is already ≥ 12 spins at 40–120 µs. (INFERENCE)
   - This cuts both ways. A light cone that grows past exact classical reach is what an advantage needs. But the
     decisive comparator for the physical echo is then **exact light-cone simulation** (statevector/typicality at
     n = 16–30 spins, which is classically routine). The approximations tested here are not that comparator. (INFERENCE)
3. **The R1-E embedding result and this one differ.** R1-E reported that echo late-window FI persists when environment
   spins are added (ratio 1.11–1.16). Here the signal itself moves by ≫ σ. Both can hold: FI measures sensitivity, while
   t_embed measures the value of the model. The persistence of FI at N ≥ 14 remains untested by this lens. (INFERENCE)

## Claim levels

- **Theoretical L1:** four more polynomial-cost classical approximation families fail on the N=10 echo window, and none
  beats the panel's 80 µs (MEASURED, 3 clusters, 1 orientation, γ = 0). This is not a complexity statement, since the
  exact classical cost at N=10 is about 1 CPU-s (MEASURED).
- **Practical L0:** unchanged. See `research/theory/BREAK_EVEN.md` §4 (FT cost ≈ 11 h per forward evaluation).
- **No claim** is made about the physical, embedded echo beyond N=12.

## Deviations and flaws in this lens's own work

- **E3, first attempt.** The uncapped run (ε=1e-3, R=4) reached the 10 CPU-minute per-run limit and was stopped by the
  agent. It produced no output. It is replaced by the capped runs with a CPU guard, and its cost is counted below.
- **Unequal E3 budgets.** E3 used M=1e4 on p19 but M=3e3 on the other two clusters, because of the budget. The failure
  mode (variance blow-up by 40 µs) is the same at both budgets.
- **Partial E4 coverage.** χ=16 and χ=64 were run on p19 only. χ=32 covers all three clusters.
- **Grid resolution.** t_c is quantised to the 20 µs record grid. The 0.01 threshold equals σ per point.
  Bias-vs-FI-loss (whether an estimator with 0.02–0.05 bias still keeps the late-window FI) was not evaluated.
- **E2 fit.** For p19 the λ grid hit its edge (λ = 2). This does not matter given errors of 0.3–0.9.
- **E4 geometry.** The MPO uses a 1D chain with SWAP routing, which is structurally disadvantaged on an all-to-all 3D
  cluster. A tree tensor network or better routing might gain a little. The discarded-weight evidence suggests it
  would not close a gap of this size (INFERENCE).
- **References cited from memory.** CCE: W. Yang & R.-B. Liu, PRB 78, 085315 (2008). Stochastic rounding and its sign
  problem, FCIQMC: G. H. Booth, A. J. W. Thom & A. Alavi, J. Chem. Phys. 131, 054106 (2009). Neither was re-verified
  this session (UNVERIFIED citations). All methods are implemented and tested here directly.

## CPU accounting (single-threaded; OMP/MKL/OPENBLAS_NUM_THREADS=1)

| Item | CPU-s (approx.) |
|---|---|
| References N=6/8/10 | 5 |
| E1 CCE N=8 (×2) and N=10 | 28 |
| E2 including calibration and debugging | 140 |
| E4 MPO: N=6 validation, χ16, χ32 ×3, χ64 | 425 |
| E3: stopped uncapped attempt, then capped runs | 600 + 141 + 80 |
| Light-cone diagnostic (N=11, 12 ×3 + leave-one-out) and timing probe | 242 |
| **Total** | **≈ 1660 s ≈ 27.7 CPU-min** (limit 30) |

Peak RAM per run was well under 1.5 GB: N ≤ 12 sector blocks ≤ 924², MPO χ ≤ 64, ≤ 1e4 strings × 3 replicas.

## Reproduce

All from this folder. Prefix each command with `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1`.

```
python cce_otoc.py 8 ; python cce_otoc.py 10            # E1 (~25 s)
python opspread_mc.py 40000                              # E2 (~60 s)
python mpo_otoc.py 64 1UBQ 19 6                          # E4 validation vs exact (N=6)
python mpo_otoc.py 32                                    # E4 chi=32, 3 clusters (~3 min); chi 16/64: python mpo_otoc.py 16|64 1UBQ 19
python stoch_pauli.py 0 3 1e4 150 1UBQ 19                # E3 (M=1e4, R=3, 150 s guard)
python stoch_pauli.py 0 3 3e3 40 1UBQ 245 ; python stoch_pauli.py 0 3 3e3 40 1PGA 390
python influence.py 2                                    # light-cone diagnostic (~4 min)
python summarize.py                                      # -> out/summary.json
```

## Recommended next tests (governed jobs; not run here)

1. **Cluster-size convergence of the echo window (decisive for R1's physical meaning).**
   `python influence.py 4` extends the add-k test to N=13 and 14 (N=14 is about 1 CPU-h per cluster; run it under
   the governor). Then compute the late-window echo FI at N=12 and 14 with `scripts/nmr_gate.py --N 12/14 --otoc 1`.
   **Kill R1's N=10 evidence** if t_conv(N=12→14) < 160 µs on ≥ 2 of 3 clusters **and** the late-window echo FI at
   N=14 falls below 0.5× its N=10 value.
2. **Light-cone reach vs exact classical reach (decisive for any advantage).** For t ∈ {80, 160, 240, 320} µs, find
   the minimal n(t) such that the nearest-n cluster reproduces the N_max echo (N_max = 20 via typicality,
   `SP.exact_correlators(..., otoc=True)`) to 0.01. **Kill R1 at the practical level** if n(320 µs) ≤ 30, because
   exact or typicality statevector simulation of ≤ 30 spins is classically routine.
3. **Stochastic Pauli at the annihilation plateau.** Run `python stoch_pauli.py 0 3 3e5 3600 1UBQ 19` under the
   governor. If the variance collapses only once M reaches the occupied operator space (≈ 2.5e5 strings at N=10),
   record E3 as exponential-cost. **Kill the echo window** only if M ≤ 1e5 gives t_c ≥ 160 µs on all three clusters.
4. **Optional TN completeness.** MPO at χ = 128 and 256 (≈ 30 min and 4 h per cluster) or a tree tensor network.
   **Kill** if t_c ≥ 160 µs at χ ≤ 256 on all three clusters (a fixed-χ polynomial method).

## Files

- Scripts: `common.py`, `cce_otoc.py`, `opspread_mc.py`, `mpo_otoc.py`, `stoch_pauli.py`, `influence.py`, `summarize.py`
- Outputs (`out/`): `ref_*.json` (exact references), `cce_N8.json`, `cce_N10.json`, `opspread_N10.json`, `mpo_*.json`,
  `stoch_*.json`, `influence_N10.json`, `summary.json`
