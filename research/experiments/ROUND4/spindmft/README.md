# ROUND4 lane `spindmft`: spinDMFT adversary for R1-SIM at t ≤ 120 µs

_2026-09-28. Lane folder: `research/experiments/ROUND4/spindmft/`._

**Pre-registration.** `PREREG_spindmft.md`:
- main rules written at 11:33, before any output;
- Addendum A (world ladder, deviation D1) written at 12:17, before those runs;
- Addendum B (exact b-aware test) written at 12:36, before those runs.

**Tags.** MEASURED / DERIVED / THEORETICAL / LITERATURE-SUPPORTED / INFERENCE / UNPROVEN.

**Scope.** This lane addresses only R1-SIM: whether the converged ¹H dipolar echo F_ab(t) at t ≤ 120 µs is beyond σ-level classical reach. The outcome is category 3 (physics simulation) at most. Whatever it is, it has no protein-structure endpoint and does not touch K-105.

## 0. Verdict: **INTERESTING**

1. **The pre-registered kill rule does not fire.**
   - Series within σ = 0.01 of the round-3 hybrid F_∞^hyb = H_∞(CSD) + X₁₈: 0/8, 0/8 and 1/8 at 40, 80 and 120 µs. The median |Δ| is 0.05–0.07 [MEASURED].
   - spinDMFT also fails its own pre-registered validation gate at every t [MEASURED].
2. **The rule cannot fire because its comparator is wrong, not because the echo is classically out of reach.** Three measurements refute the hybrid at 40 µs:
   - **Exact data refute its "flat-X" premise.** The pooled slope dF_N / d(H_N + floor_N) over N = 14–20 is −0.03 ± 0.10; the hybrid needs 1. X rises on 8/8 series [MEASURED].
   - **Exact b-aware clusters sit above it by 0.056–0.096**, i.e. 5.6–9.6σ, on the 3 tested series [MEASURED].
   - Consequently CRITIC C1's "finite clusters are 3.1–8.2σ from F_∞ inside T3" is **not supported at 40 µs**.
3. **At 40 µs, two independent classical families agree within σ on 8/8 series** [MEASURED agreement; that the common value is F_∞ is INFERENCE].
   - **5 probe-local series** (p19 b1, b7; p245 b1, b8, b9). The exact probe-family F₁₈ ≈ F₂₀ is flat in N (|F₂₀ − F₁₈| ≤ 0.002), and the spinDMFT thermodynamic bath correction is ≤ 0.004 on 5/5. It is n_c-stable (10 → 12) to ≤ 0.004, checked for p19 only.
   - **3 b-remote series** (p245 b7, p19 b8, p19 b9). Each butterfly site keeps ≤ 27% of its M2 inside the 18-cluster. spinDMFT predicted, before the exact runs, shifts of +0.064, +0.030 and −0.001 relative to F₁₈. Exact b-aware clusters of 16 spins land within 0.006 of the spinDMFT values on 3/3 (−0.000 / −0.005 / −0.005).
   - So the converged 40 µs echo is **σ-level classically reachable**: exact simulation of ≤ 16–20 spins in seconds to minutes, plus polynomial spinDMFT. This is a KILL-leaning result for R1-SIM at 40 µs, but it comes through a post hoc comparator, not the literal pre-registered rule, so it is reported as INTERESTING.
4. **80 µs: partly open.**
   - The b-remote series agree (2/3 within σ).
   - On the probe-local series, the spinDMFT bath corrections (−0.039 to +0.039) have no second confirming estimator. They move by up to 0.02 between n_c = 10 and 12, and spinDMFT's absolute errors in the closed world reach 0.09.
5. **120 µs: open.** The derived OTOC extension is unreliable there (errors 0.03–0.17 against exact).
6. **No quantum advantage claim of any category is made or supported.** Theoretical level L0, practical level L0. K-105 is untouched (its forward-model-error arm, 5–66σ, is independent of all of this).

## 1. What spinDMFT can and cannot compute here

| Quantity | Can spinDMFT compute it? | Accuracy on this network (MEASURED unless marked) |
|---|---|---|
| Probe autocorrelation G_aa(t) | Yes: single-site (sr) or cluster (nl) | **sr fails**: p19 G_aa(80 µs) = 0.21–0.23 vs 0.36 exact; z_eff median 3.15 violates the method's many-partner prerequisite [LITERATURE-SUPPORTED]. **nl** (n_c = 10–12) errs by −0.01 to −0.03 in the closed N = 18 world and does not improve with n_c (no back-flow, A2) |
| Pair correlations G_aj, j inside the cluster | Yes (nl-spinDMFT) | Symmetric G_aj ≈ G_ja to ≤ 0.009 |
| H = Σ_j G_aj² (two-point part of the echo) | Only the in-cluster part H_C, plus the bound H ≤ H_C + (1 − ΣG_C)². Bath-site G_aj are not computed | At 40 µs the bracket matches the CSD H_∞ (p19 0.317–0.341 vs 0.351 ± 0.010; p245 0.339–0.362 vs 0.366 ± 0.011). Too loose to test at 80–120 µs |
| Echo / OTOC F_ab | **No published extension** [LITERATURE-SUPPORTED, abstract level]. Here: a derived quenched-Gaussian-bath extension (A3) | Absolute: 7/8 within σ of exact F₁₈ at 40 µs; fails at 80–120 µs (up to 0.17). **Bath correction to F** (difference between worlds): reproduces the exact N-dependence at 40 µs (23/24) and 80 µs (20/24). Its thermodynamic-limit predictions are confirmed by exact b-aware clusters at 40 µs (3/3, ≤ 0.006) and 80 µs (2/3) |
| Late-time echo (≥ 120 µs), or sites whose local factor is scrambled by the bath | Not reliably | A3 drives F toward −1/3 instead of 0 [DERIVED]. Site 1 errors are 0.06–0.17 at 80–120 µs |


## 2. Literature (arXiv API and abs pages, fetched this session)

| Work | Verified id | What it provides |
|---|---|---|
| spinDMFT: Gräßer, Bleicker, Hering, Yarmohammadi, Uhrig, PRR 3, 043168 (2021) | **arXiv:2107.07821**. The task text's "2105.xxxxx" is wrong | A single-site classical Gaussian mean field at infinite temperature. Two-point autocorrelations |
| CspinDMFT: Gräßer, Rezai, Sushkov, Uhrig, PRR 5, 043191 (2023) | arXiv:2307.14188 | A cluster extension for randomly placed dipolar ensembles (autocorrelations) |
| nl-spinDMFT: Gräßer, Hahn, Uhrig, SSNMR 132, 101936 (2024) | arXiv:2403.10465 | Pair correlations on clusters coupled to the spinDMFT mean fields (FID). Its "Hahn echo" is a **two-point** function with a π pulse, not an OTOC |
| Spin diffusion in static solids: Gräßer, Uhrig, Ernst, Sci. Adv. 12, eaee6228 (2026) | arXiv:2512.15572 | spinDMFT for spectral spin diffusion. Stated prerequisite: "each spin interacts with a large number of other spins" |
| Dipolar–quadrupolar spinDMFT: Gräßer, Uhrig, SciPost Phys. 20, 031 (2026) | arXiv:2507.17720 | Not used here |
| Finite-temperature spinDMFT: Bieniek, Gräßer, Uhrig (2026 preprint) | arXiv:2604.21563 | Not used here |

- **No OTOC or four-point extension of spinDMFT exists in this literature** [LITERATURE-SUPPORTED, abstract level].
  - Search 1: all Gräßer ∧ Uhrig entries (7).
  - Search 2: "mean-field" ∧ "out-of-time-order" ∧ dipolar returned 0 entries.
  - Full texts were not read, so an OTOC treatment inside a paper body is [UNPROVEN either way].
- The echo extension used here is **derived in this lane** (§3, A3).

## 3. Methods: what was implemented (`sdmft.py`)

All three components use the same instance:
- 1UBQ, with the 629 OpenMM protons of `data/instruments/nmr/1UBQ_H.pdb`;
- couplings `qapf.nmr.spins.couplings`, with b0 = `random_b0(1000)`;
- probes p19 and p245, and sites b ∈ {1, 7, 8, 9} (probe-cluster ranks), as in round 3.

**1. sr-spinDMFT** (site-resolved, for disordered positions).
- Every proton i sees a Gaussian classical field V_i with covariances
  - ⟨V^z V^z⟩(τ) = Σ_j d_ij² g_j^z(τ);
  - ⟨V^x V^x⟩ = ⟨V^y V^y⟩ = ¼ Σ_j d_ij² g_j^⊥(τ).
- The field is sampled on a 1 µs grid and iterated to self-consistency.
- For spin ½ in a classical field, the single-site problem is exactly the rotation of a classical unit vector, dS/dt = V × S [DERIVED; checked in T3 below]. So g^z = E[R_zz] and g^⊥ = E[R_xx].
- Converged in 3 iterations to the Monte Carlo floor: mean |Δg| is 0.026 at M = 384 (protein) and 0.006 at M = 4096 (closed worlds) [MEASURED, `out/sr_*.json`].

**2. nl-spinDMFT** (an exact cluster embedded in the spinDMFT fields).
- The cluster C (n_c spins, containing a and b) is solved exactly with typicality vectors.
- It uses the **same fused pair gates in the same order** as the reference Trotter circuit (dt = 2 µs).
- Each cluster spin q is driven by V_q = Σ_{j∉C} c_α d_qj ξ_j:
  - c_z = 2 and c_⊥ = −1;
  - the ξ_j are independent Gaussian processes with covariance g_j/4 taken from step 1;
  - so the fields on different cluster spins are correlated through shared bath spins.
- A symmetric noise–pair–noise split is used in each 2 µs step.
- Outputs: G_ja(t) for j ∈ C, and H_C = Σ_{j∈C} G_aj².
- Cost is polynomial in the world size and exponential only in the fixed n_c.

**3. OTOC extension** (derived here; approximation **A3, quenched Gaussian bath**).
- F_ab = E_ξ Tr[W_ξ Z_b W_ξ Z_b]/2^{n_c}, with W_ξ = U_ξ† Z_a U_ξ and the same bath realisation in both branches.

**Approximations, stated in advance:**
- **A1: Gaussian bath.** Weak for protein ¹H. The effective coordination z_eff = (Σd²)²/Σd⁴ has median **3.15** over all 629 protons, and is 7.1 (p19) and 6.7 (p245) [DERIVED here].
- **A2: bath–bath correlations neglected.** So polarisation lost to the bath never flows back.
- **A3: no back-action.** Operator growth that passes through bath spins back to b is missed, except as a local rotation of b. At full scrambling of b's local factor, A3 gives F → 1 − 2·(2/3) = **−1/3**. The exact scrambled value is 0, since X or Y occupy half of a random Pauli string at b [DERIVED].

**Unit validation** [MEASURED, `test_sdmft.py` → `test_sdmft.json`]:

| Test | Setup | Result |
|---|---|---|
| T1 | No bath (C = the whole closed N = 10 world): embedded typicality estimates vs the deterministic `sector_exact_correlators` on the same Trotter circuit, 20–60 µs | max \|ΔF\| = **0.0010** (≤ 2.3 SE); max \|ΔG_ab\| = 0.005 |
| T2 | G_ja (the estimator used for H) vs G_aj computed directly, with a bath | Agree to 0.012 (2.2 SE, max over 7 time points). In production runs, G_ab direct − G_ba ≤ 0.009 |
| T3 | n_c = 1 quantum spin-½ vs the classical-rotation single-site solver, same fields | Agree to 0.013 (SE 0.008 each) |

## 4. Results

The summary numbers below come from `analysis.json`, produced by `analyze.py`. σ = 0.01 throughout. "Series" means probe × site; there are 8 per time point.

### 4.1 Two-point functions: what spinDMFT gets right and wrong [MEASURED]

**G_aa(t) and H at 40 / 80 / 120 µs**

| Estimator | p19 G_aa | p19 H (nl: in-cluster H_C … upper bound H_C + (1 − ΣG_C)²) | p245 G_aa | p245 H |
|---|---|---|---|---|
| Exact, N = 18 (probe family) | 0.600 / 0.366 / 0.265 | 0.384 / 0.176 / 0.122 | 0.583 / 0.281 / 0.188 | 0.366 / 0.130 / 0.092 |
| Exact, N = 20 | 0.597 / 0.364 / 0.259 | 0.378 / 0.172 / 0.116 | 0.583 / 0.285 / 0.189 | 0.364 / 0.128 / 0.086 |
| CSD, N_c = 80 / 160 (round 3) | 0.56–0.59 / 0.31–0.35 / 0.22–0.25 | H_∞(hybrid) = 0.351 ± 0.010 / 0.143 ± 0.007 / 0.082 ± 0.006 | 0.597 / 0.317 / 0.197 | 0.366 ± 0.011 / 0.128 ± 0.007 / 0.058 ± 0.005 |
| sr-spinDMFT (single site), protein | 0.533 / **0.211** / **0.089** | — | 0.604 / 0.324 / 0.122 | — |
| sr-spinDMFT, closed N = 18 world | 0.522 / **0.225** / **0.101** | — | 0.612 / 0.310 / 0.157 | — |
| nl-spinDMFT n_c = 10, N = 18 world | 0.585 / 0.344 / 0.236 | 0.364…0.372 / 0.149…0.208 / 0.079…0.222 | 0.572 / 0.260 / 0.163 | 0.352…0.361 / … |
| nl-spinDMFT n_c = 12, N = 18 world | 0.583 / 0.340 / 0.233 | 0.362…0.368 / … | not run (budget) | |
| nl-spinDMFT n_c = 10, protein | 0.545 / 0.281 / 0.162 | **0.317…0.341** / 0.100…0.247 / 0.039…0.356 | 0.566 / 0.263 / 0.146 | **0.339…0.362** / … |
| nl-spinDMFT n_c = 12, protein | 0.544 / 0.279 / 0.171 | 0.316…0.336 / … | stopped at 2/10 batches (checkpoint kept, not analysed) | |

**Reading.**
- **Single-site spinDMFT fails for this network.** For p19 it gives G_aa(80 µs) = 0.21–0.23 against 0.36 exact, including in the closed N = 18 world where exact is known. This is the few-strong-neighbour regime (z_eff median 3.15) that the method's own prerequisite excludes [MEASURED; LITERATURE-SUPPORTED prerequisite].
- **nl-spinDMFT is closer but still not σ-accurate.** In the N = 18 world its error is −0.011 to −0.029, and it does not improve from n_c = 10 to 12 (A2: no polarisation back-flow from the bath) [MEASURED].
- **H_∞ at 40 µs.** The nl-spinDMFT bracket contains or touches the CSD hybrid H_∞ on both probes: p19 0.317–0.341 vs 0.351 ± 0.010; p245 0.339–0.362 vs 0.366 ± 0.011.
  - This is a weak cross-family confirmation of H_∞ at 40 µs [MEASURED].
  - At 80–120 µs the bracket is too wide to test H_∞.
  - spinDMFT cannot compute G_aj for bath spins, so it cannot give H_∞ itself.

### 4.2 Echo in the closed N = 18 world: absolute validation [MEASURED]

| t (µs) | within σ of F₁₈ − floor₁₈ (pre-registered primary), n_c = 10 | within σ of F₁₈ (direct, post hoc D1), n_c = 10 | max \|err\| vs F₁₈ | p19: n_c = 10 → 12 error vs F₁₈ (sites 1 / 7 / 8 / 9) |
|---|---|---|---|---|
| 40 | 1/8 | **7/8** | 0.032 | −0.032→−0.036 / +0.004→+0.003 / −0.004→−0.004 / +0.004→+0.004 |
| 80 | 0/8 | 2/8 | 0.094 | −0.094→−0.099 / +0.009→+0.008 / −0.016→−0.018 / +0.019→+0.014 |
| 120 | 2/8 | 1/8 | 0.167 | −0.102→−0.107 / −0.014→−0.016 / −0.041→−0.043 / +0.025→+0.014 |

**Reading.**
- The **pre-registered validation gate fails at every t**.
- Against the direct target, spinDMFT reproduces the exact echo at 40 µs (7/8 within σ). It fails at 80–120 µs, by up to 0.17 at p245 site 1.
- **The error does not fall from n_c = 10 to 12.** It is set by the Gaussian-bath approximations (A2/A3), not by the cluster size.
- The worst series is always site 1, the probe's strong nearest partner. At 80–120 µs it is 60–67% bath-coupled, where A3's over-scrambling bias (F → −1/3) acts.

### 4.3 Thermodynamic limit and the pre-registered kill rule [MEASURED]

- The protein-world nl-spinDMFT echo is **converged in cluster size** for p19. From n_c = 10 to 12 it changes by ≤ 0.004 at 40 µs, ≤ 0.015 at 80 µs and ≤ 0.017 at 120 µs. The p245 n_c = 12 run was stopped at 2/10 batches to fund test E-B; its checkpoint is kept and it was not analysed.
- **It disagrees with the hybrid F_∞^hyb = H_∞ + X₁₈:**

| t (µs) | series within σ of the hybrid (n_c = 10) | median \|Δ\| | max \|Δ\| | sign of Δ (spinDMFT − hybrid) |
|---|---|---|---|---|
| 40 | **0/8** | 0.053 | 0.090 | + on 8/8 |
| 80 | **0/8** | 0.071 | 0.162 | + on 6/8 |
| 120 | **1/8** | 0.050 | 0.296 | mixed |

The pre-registered literal rule (**KILL if ≥ 7/8 agree within σ**) **does not fire at any t ≤ 120 µs**.

### 4.4 Why it cannot fire at 40 µs: the hybrid's premise is refuted by exact data [MEASURED + DERIVED]

**The hybrid's assumption.** The hybrid sets X_∞ = X₁₈, so F moves 1:1 with H + floor, a slope of s = 1.

**The test.** Fit exact F_N against exact H_N + floor_N over N = 14, 16, 18, 20. The data are the typicality cones, with N = 20 from the partial reference checkpoint.

| t (µs) | pooled slope s = dF / d(H + floor) | ΔX (N = 14 → 20), 8 series | Δ(H + floor) (14 → 20) |
|---|---|---|---|
| 40 | **−0.03 ± 0.10** (s = 1 excluded at about 10 SE) | **+0.003 to +0.018, positive on 8/8** (sign test p = 0.004) | −0.009 to −0.010 |
| 80 | 0.56 ± 0.47 | −0.078 to +0.082 | −0.019 to −0.024 |
| 120 | 0.78 ± 0.66 | −0.056 to +0.137 | −0.024 to −0.026 |

**Mechanism [DERIVED].**
- F_ab = 1 − 2 w_b, where w_b is the Pauli weight of W = Z_a(t) with X or Y at site b. H and floor are b-independent parts of the norm.
- A flat X therefore requires Δw_b = −(ΔH + Δfloor)/2. That is, half of every unit of norm leaving the single-Z sector or the floor would have to land on X/Y at b, which is the "fully scrambled at b" limit.
- Norm that spreads to spins far from b commutes with Z_b and leaves F unchanged.
- At 40 µs the exact ladder shows exactly this: F_N is flat to ≤ 0.008 (median 0.002) while floor_N falls by 0.010.
- So **the round-3 hybrid F_∞^hyb double-subtracts at 40 µs**, and CRITIC C1's "finite clusters 3.1–8.2σ from F_∞ inside T3" is **not supported at 40 µs**.
- At 80–120 µs the test has no power (SE 0.5–0.7).

### 4.5 World ladder: does spinDMFT reproduce the exact N-dependence? (Addendum A, fixed before the runs) [MEASURED]

**Test.** Compare ΔF_dmft(N) = F^emb(W_N) − F^emb(W₁₈) with ΔF_exact(N) = F_N − F₁₈. Settings: n_c = 10, N = 14, 16, 20, with a self-consistent bath in each closed world.

| t (µs) | pairs within σ | fraction (criterion ≥ 80%) | median \|err\| | median \|ΔF_exact\| (power) | verdict |
|---|---|---|---|---|---|
| 40 | 23/24 | 0.96 | 0.0004 | 0.0005 (low power) | **corroborated** (weakly) |
| 80 | 20/24 | 0.83 | 0.003 | 0.006 | **corroborated** |
| 120 | 11/20 | 0.55 | 0.008 | 0.014 | not corroborated |

**Where it fails at 80 µs.** All four failures come from N = 14/16 shell events: p19 b1 at N = 14 (−0.086), p19 b8 at N = 14/16 (+0.024/+0.018), and p19 b9 at N = 14 (−0.022). All 8 N = 20 pairs are within σ.

### 4.6 The spinDMFT bath correction, b-aware clusters, and the exact b-aware test [MEASURED; extrapolation INFERENCE]

**The spinDMFT bath correction** is ΔW = F^emb(protein) − F^emb(W₁₈) at n_c = 10, probe family. It is n_c-stable for p19 at 40 µs (≤ 0.004).

| t (µs) | p19 sites 1 / 7 / 8 / 9 | p245 sites 1 / 7 / 8 / 9 | series with \|ΔW\| ≤ σ |
|---|---|---|---|
| 40 | +0.004 / +0.003 / **+0.017** / +0.002 | +0.000 / **+0.065** / +0.001 / −0.003 | **6/8** |
| 80 | −0.039 / −0.011 / +0.033 / −0.019 | +0.027 / +0.039 / +0.005 / −0.022 | 1/8 |
| 120 | −0.063 / −0.105 / +0.024 / −0.073 | +0.051 / +0.006 / −0.032 / −0.068 | 1/8 |

**Where the two large 40 µs corrections come from.** Both sit on butterfly sites whose own dipolar partners lie outside the probe-centred cluster:
- p19 b8 is a methyl proton (HG22/ILE3); 15% of its M2 is inside the 18-cluster and 4% inside the n_c = 10 cluster.
- p245 b7 is HA/LYS27; 27% is inside the 18-cluster.

**b-aware clusters** ({a, b} ∪ protons nearest to a or b, n_c = 10) do two things:
- They reproduce exact F₁₈ in the N = 18 world at 40 µs for all three such series: p19 b8 +0.003, p19 b9 +0.004, p245 b7 +0.001.
- They give the same or larger protein corrections: p245 b7 **+0.064 / +0.072 / +0.035**; p19 b8 **+0.027 / +0.073 / +0.068**; p19 b9 −0.005 / −0.031 / −0.051.

**Test E-B: exact b-aware clusters** (Addendum B, fixed before running).
- Clusters: {a, b} ∪ the protons nearest to a or b, with the same Trotter circuit (`qapf.nmr.spins.exact_correlators`).
- Sizes and typicality vectors: N = 12 / 14 / 16 with R = 8 / 4 / 2.
- These clusters hold 83–97% of b's second moment M2.
- Pipeline check: the same code on the probe family at N = 12 reproduces the round-3 cone file within typicality noise (`out/exact_pipeline_check.json`).

[MEASURED]

| series, t (µs) | exact b-aware F at N = 12 / 14 / 16 | spinDMFT prediction (b-aware, protein) | exact probe-family F₁₈ | hybrid | exact₁₆ − spinDMFT | exact₁₆ − hybrid |
|---|---|---|---|---|---|---|
| p245 b7, 40 | 0.767 / 0.761 / **0.764** | **0.764** | 0.699 | 0.668 | **−0.000** | +0.096 |
| p245 b7, 80 | 0.511 / 0.483 / 0.489 | 0.496 | 0.421 | 0.376 | −0.006 | +0.113 |
| p245 b7, 120 | 0.351 / 0.350 / 0.345 | 0.290 | 0.267 | 0.189 | +0.055 | +0.156 |
| p19 b8, 40 | 0.978 / 0.977 / **0.978** | **0.983** | 0.953 | 0.891 | −0.005 | +0.087 |
| p19 b8, 80 | 0.900 / 0.905 / 0.905 | 0.907 | 0.811 | 0.739 | −0.002 | +0.167 |
| p19 b8, 120 | 0.797 / 0.810 / 0.804 | 0.775 | 0.651 | 0.570 | +0.029 | +0.234 |
| p19 b9, 40 | 0.941 / 0.945 / 0.948 | 0.953 | 0.954 | 0.892 | −0.005 | +0.056 |
| p19 b9, 80 | 0.700 / 0.714 / 0.731 | 0.749 | 0.761 | 0.688 | −0.018 | +0.042 |
| p19 b9, 120 | 0.599 / 0.604 / 0.584 | 0.540 | 0.565 | 0.484 | +0.045 | +0.100 |

**Addendum B criterion.** Corroborated at 40 µs (2/2 counting series), at 80 µs (2/2) and at 120 µs (2/3). At 120 µs the exact values overshoot the spinDMFT values by 0.03–0.055 rather than agreeing.

**Reading.**
1. **The probe-centred exact family is not converged at butterfly sites whose own partners lie outside it** [MEASURED].
   - This family was the reference throughout round 3 and the source of X₁₈ in the hybrid.
   - At 40 µs, b-aware exact clusters of 12–16 spins are converged in N to ±0.003.
   - They give F higher than the probe family by **+0.065** (p245 b7) and **+0.025** (p19 b8).
   - Finite-cluster convergence depends on the cluster family, not only on N.
2. **spinDMFT predicted these values before the exact runs, in the thermodynamic limit (Addendum B).**
   - It agrees with the exact b-aware clusters to **≤ 0.006 at 40 µs (3/3)**.
   - At 80 µs it agrees to ≤ 0.006 on 2/3. For p19 b9 the gap is −0.018, and the exact values are still drifting by +0.015 per ΔN = 2.
   - At 120 µs it is 0.03–0.055 low, consistent with the A3 over-scrambling bias.
3. **The hybrid comparator is refuted as an F_∞ estimate** [MEASURED]. At 40 µs it lies 5.6–9.6σ below the exact b-aware values, and 4–17σ below at 80 µs. Together with §4.4, this is why the pre-registered rule cannot fire.

**Bath-corrected estimator F_corr = F₁₈ + ΔW vs the hybrid** [MEASURED arithmetic; F_corr is an INFERENCE estimator]:
- It lies above the hybrid on 8/8 series at 40 µs (+0.028 to +0.096) and 8/8 at 80 µs (+0.023 to +0.105).
- The F₂₀-based version, F₂₀ + [F^emb(protein) − F^emb(W₂₀)], agrees with it to ≤ 0.006 at 40–80 µs.


## 5. Decision against the pre-registration

| Rule | Outcome |
|---|---|
| Literal parent rule: KILL if ≥ 7/8 series agree within σ with F_∞^hyb | **Does not fire** at 40 / 80 / 120 µs (0/8, 0/8, 1/8) |
| Validation gate: primary target F₁₈ − floor₁₈, ≥ 6/8 within σ | **Fails** at every t (1/8, 0/8, 2/8). Against the direct target F₁₈ (post hoc, deviation D1): 7/8, 2/8, 1/8 |
| Addendum A: world ladder, ≥ 80% of pairs within σ | Corroborated at 40 µs (96%, low power) and 80 µs (83%). Not at 120 µs (55%) |
| Addendum B: exact b-aware test | Corroborated at 40 µs (2/2, \|Δ\| ≤ 0.006 on 3/3), at 80 µs (2/2) and nominally at 120 µs (2/3, but with an overshoot of 0.03–0.055) |

**Verdict mapping.**
- **KILLS** is excluded: the literal rule did not fire and the gate failed.
- **INTERESTING** is chosen. The pre-registered INTERESTING clause is: "literal rule does not fire but the discrepancy is explained by a validated failure of one estimator; the question moves but is not settled". That fits:
  - the discrepancy is explained by a *measured* failure of the comparator (§4.4, §4.6);
  - the 40 µs window moves to "classically reachable at σ" (INFERENCE);
  - 80–120 µs stays open.
- **Transparency note on SUPPORTS.** Its three formal conditions are also met:
  - spinDMFT is not validated at σ;
  - its closed-world error does not fall from n_c = 10 to 12 (p19);
  - it disagrees with the hybrid by > 3σ on ≥ 4/8.

  But SUPPORTS was written to mean "classical estimators disagree, so σ-level reach is not demonstrated". Here the disagreement is traced to a demonstrated defect in one estimator, and at 40 µs two other classical families agree. Reporting SUPPORTS would misstate the evidence. Verifiers should check this choice.

## 6. Consequences for the open R1-SIM questions (INFERENCE unless tagged)

1. **Retire F_∞^hyb = H_∞ + X_N as an F_∞ comparator**, at least at t ≤ 80 µs.
   - It double-subtracts norm redistribution that commutes with Z_b [DERIVED §4.4; MEASURED 40 µs].
   - It inherits the cluster-family error of X_N at b-remote sites [MEASURED §4.6].
   - CRITIC C1's 3.1–8.2σ table rests on it and should be withdrawn for 40 µs.
2. **The pre-registered T-X-early criterion "|X₂₂ − X₂₀| ≤ 0.005" is ill-posed.**
   - X_N drifts upward as floor_N falls even when F_N is converged: 8/8 series at 40 µs, with ΔX = +0.003 to +0.018 over N = 14 → 20 while F is flat.
   - A convergence criterion must be stated on F, with a b-aware cluster family and an explicit thermodynamic correction, e.g. spinDMFT's.
3. **Cluster family matters more than cluster size at t ≤ 80 µs.**
   - Exact {a, b}-centred clusters of 12–16 spins are converged to ±0.003 (40 µs) and ±0.006 (80 µs; p19 b9 still +0.015 per step).
   - The probe-centred family at N = 20 is still off by 0.025–0.065 at the b-remote sites [MEASURED].
   - This lowers the classical cost of the physically observable window, not raises it.
4. **R1-SIM residue after this lane.**
   - 40 µs: σ-level classical reach is supported by two agreeing classical families (KILL-leaning; needs a verifier and replication on 1PGA p390 / 1UBQ p487 and on other orientations).
   - 80 µs: open for the 6 series without a second estimator, at the 0.01–0.04 level.
   - 120 µs: open.
   - The physically relevant window is t ≤ T3 ≈ 30–70 µs (≤ 123 µs under the most generous convention), so the part with the strongest physical claim (≈ 40 µs) is the part now most classically settled.
5. **Nothing here revives K-105.** Even a perfectly converged echo carries the 5–66σ forward-model error (methyl rotation, offsets, reversal mismatch) and joint value ≤ 1.2–3.

## 7. Levels and claim category

- **Theoretical level: L0.** No separation is claimed or implied. The classical methods are polynomial (sr-spinDMFT O(N² T M) per iteration; embedded cluster O(C(2n_c, n_c) · T² · M) at fixed n_c, polynomial in the bath size) or exact on ≤ 20 spins.
- **Practical level: L0.** No quantum resource was costed. The classical comparator now includes exact b-aware clusters plus spinDMFT corrections, which is strictly stronger than the round-3 hybrid.
- **Claim category:** none of 1–6 for any quantum component. This lane is a classical-adversary result on a physics-simulation question.

## 8. Resource ledger

| Field | Value |
|---|---|
| ID | ROUND4-spindmft (tests T1–T3, sr-spinDMFT ×9 worlds, nl-spinDMFT ×19 runs, exact b-aware ×9 runs, pipeline check) |
| Hypothesis | PREREG_spindmft.md (+ Addenda A, B) |
| Algorithms | sr-spinDMFT (self-consistent Gaussian fields, classical-rotation single site); nl-spinDMFT (typicality-exact cluster, n_c = 1, 6, 10, 12, sector-blocked BLAS pair layer, complex64); derived quenched-bath OTOC (A3); exact typicality (`qapf.nmr.spins.exact_correlators`) on b-aware clusters N = 12–16 |
| Targets | 1UBQ ¹H (629 protons), probes p19 and p245, sites 1/7/8/9, b0 = random_b0(1000), t = 40/80/120 µs, dt = 2 µs Trotter circuit |
| Compute | ≈ **58 CPU-min** single-thread (OMP/MKL/OPENBLAS = 1). Logged 48.9 min in `out/*.json` + tests 1.4 + first unoptimised test ≈ 5.5 + partial batches lost at two stops ≈ 2. Largest single run 9.3 CPU-min. Peak RSS < 0.3 GB |
| Checkpointing | sr: per iteration (`*.ckpt.npz`); embedded: per batch (`*.ckpt.json`, atomic tmp + replace); exact b-aware: per (series, N) output. To re-prioritise I stopped my own queued n_c = 12 loops twice. The p19 N18 n_c = 12 process ran to completion; the p245 protein n_c = 12 run was stopped at 2/10 batches, and its checkpoint is kept for resumption |
| Process note | The tool auto-backgrounded some long commands. Each python run was bounded by `timeout` and a wall budget. I waited for each and never ran two of my compute processes at once. I stopped only processes I had launched and touched no other process |
| Quantum resources | None. Simulator time is not physical quantum time |
| Statistics | Typicality/noise SEs per series in `out/emb_*.json` (F_se 0.0001–0.007). Pooled-slope SE from residuals. Sign test for ΔX (8/8, p = 0.004) |
| Leakage | None. The native geometry defines the physical instance only; there is no optimisation or selection on test data |
| Replication | Two probes; the world ladder over 4 closed worlds; two cluster families; independent exact b-aware clusters. Single protein and single orientation (**not replicated** on 1PGA or 1UBQ p487) |
| Conclusion | §0 |

## 9. Files

| File | Content |
|---|---|
| `PREREG_spindmft.md` | Pre-registration, Addenda A and B (timestamped) |
| `sdmft.py` | sr-spinDMFT, cluster field factors, embedded cluster (two-point + quenched OTOC), summaries |
| `test_sdmft.py` → `test_sdmft.json` | Unit validation T1–T3 |
| `run_sr.py` → `out/sr_*.json`, `out/sr_*.ckpt.npz` | Self-consistent baths (protein; closed N = 14/16/18/20 worlds) |
| `run_emb.py` → `out/emb_*.json`, `out/emb_*.ckpt.json` | Embedded-cluster runs (tag = probe, world, n_c, family, bath, M, seed) |
| `run_ladder.sh`, `out/ladder_log.txt` | World-ladder and b-aware spinDMFT batch |
| `exact_pairb.py` → `out/exact_pairb_*.json`, `out/exact_pipeline_check.json` | Exact b-aware clusters (test E-B) and the pipeline check |
| `analyze.py` → `analysis.json`, `analysis_stdout.txt` | All tables, the flat-X test, the world ladder, E-B, decisions |

## 10. Next tests (ranked; each ≤ 30 CPU-min, single-thread, checkpointed; pre-register first)

1. **Exact b-aware clusters for all 8 series** at N = 16–20 (fastecho flip mode), t = 40–120 µs. For probe-local sites use {a, b} ∪ nearest-to-either. Kill R1-SIM at t if F converges (|ΔF| ≤ σ/2 over two N steps) **and** agrees with the spinDMFT-corrected value within σ on ≥ 7/8. This would decide 80 µs.
2. **Replication**: repeat §4.4–§4.6 on 1PGA p390 and 1UBQ p487 (cones exist to N = 16–18) and on 2 further b0 orientations.
3. **spinDMFT upgrades for 80–120 µs**:
   - a CspinDMFT pair-cluster bath (bath autocorrelations from embedded pairs);
   - bath–bath correlations to restore back-flow (A2);
   - a two-centre {a, b} embedding;
   - a beyond-quenched OTOC treatment (bath spins promoted to a second quantum shell) to remove the A3 over-scrambling bias.
4. **Record corrections** in the state files for the orchestrator: CRITIC C1 withdrawn at 40 µs; the T-X-early criterion replaced by an F-based, b-aware-family criterion; the hybrid F_∞ retired as a comparator.
