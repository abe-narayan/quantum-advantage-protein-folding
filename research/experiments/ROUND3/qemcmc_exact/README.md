# ROUND3 lane `qemcmc_exact`: quantum-enhanced MCMC (Layden proposal) on the A80 learned energy, exact gaps

_2026-09-28. Status: **COMPLETE. Verdict: KILLS** (practical L0). A small-n exponent residue is recorded in §6. Label: DEP (native-free). Nothing committed._

## Question and pre-stated criterion

The only published claim of a beyond-quadratic Gibbs-sampling speedup is Layden et al., Nature 619, 282 (2023)
(arXiv:2203.12497). [LITERATURE-SUPPORTED, verified from the arXiv PDF, Fig. 2c and Table S3] On 500 random
fully connected SK instances, n = 3..10, T = 1, the average absolute spectral gap fits <δ> ∝ 2^{-kn} with
k = 0.264(4) for the quantum proposal, 0.94(4) for local single-flip, and 0.948(7) for uniform. That is the source of
the "cubic/quartic" enhancement. The comparators are local and uniform proposals only.
Orfi & Sels (arXiv:2403.03087, 2408.07881; abstracts verified) bound the Markov gap of any unital quantum
proposal by an inverse-participation-ratio quantity and show no speedup on unstructured worst cases.

**This lane asks:** on discretised instances of the A80 learned protein energy, does the Layden proposal beat the
**best classical chain we can build and evaluate exactly** by more than a quadratic, δ_q > δ_c^{1/2} (k_q < k_c / 2)?
And does it survive the K-101 cost floor once the per-step circuit cost is included?

**Pre-stated verdict rule (from the lane brief, fixed before any run).**
- SUPPORTS only if the proposal is super-quadratic over the best classical chain *and* the cost is plausible.
- KILLS if it is at most quadratic, or if the best classical chain matches it.

## Instances (DEP, native-free)

`build_instances.py`. Ladder crops 5O37A_30, 3GAHA_30, 2AB0A_30 (plus replicate crops, below). A80 energy
`qapf.protein.energy.Energy` on internal coordinates (θ, τ).

1. **x\*** is the lowest endpoint of a 64-restart multistart L-BFGS census (prior draws, 200 iterations). No native
   coordinates are read anywhere in this lane.
2. **Alphabet.** State 0 of residue r is x\*'s own (θ_r, τ_r). The alternatives are centres of the most probable
   (θ, τ) bins of r's prior head whose τ lies ≥ 60° from x\*'s τ, and ≥ 45° from each other for the 4-state
   alphabet.
3. **Residue order.** `amb` puts residues with the most probable alternative conformer first. `rnd` is a seeded
   random order.
4. **Encodings.** Binary (1 qubit per residue) or 4-state (2 qubits per residue).
5. **Tables.** Each table covers 2^12 configurations (2^10 for the `_b10` tables). The n-qubit instance is the
   table restricted to the first n bits, with the other alphabet residues pinned at x\*.
   - **FROZEN:** every other coordinate is held at x\*.
   - **RELAXED:** every other coordinate is relaxed by L-BFGS (80 iterations) from x\*, with the alphabet residues
     pinned.
6. **Temperatures.** T ∈ {1, 2, 4} in energy units (nats).

## Chains (all exact: transition matrices built in full, gaps by eigensolver)

`qemcmc.py`, `run_gaps.py`. Metric: the absolute spectral gap δ = 1 − max_{k≥1}|λ_k|, Layden's metric.

| class | chain | notes |
|---|---|---|
| (a) | local single-flip Metropolis | sparse; grounded-LU pseudo-inverse + Lanczos; values < 1e-12 flagged as censored |
| (b) | uniform proposal | |
| (c) plain | best of local, uniform, mix(p ∈ {0.05, 0.2, 0.5}) = p·uniform + (1−p)·local, and pflip(q ∈ {0.05, 0.1, 0.2, 0.3}) | pflip flips every bit independently with probability q. It is exactly the γ = 1 (pure-mixer) quench, so it is the classical twin of the quantum proposal. |
| (c) idealised | mean-field independence proposal mixed with local; simulated tempering with **exact** weights (K ∈ {3, 5, 8}, T_max/T ∈ {8, 64}) | ST is counted at joint gap / K, which is conservative for classical |
| (d) | Layden proposal Q(s'\|s) = \|⟨s'\|e^{−iHt}\|s⟩\|², H = (1−γ)·α·H_E + γ·Σ X_i, α = ‖ΣX‖_F / ‖H_E − mean‖_F | exact U: no Trotter error, no noise. Two H_E choices: `raw` (E − E_min) and `clip` (min(E − E_min, 40)). Both are legitimate because MH corrects for them. Two protocols: **tuned**, the best single (γ, t) per instance and T on the grid γ ∈ {0.2, 0.35, 0.5, 0.65, 0.8} × t ∈ {2, 4, 7, 12, 20}, which is oracle-tuned and favourable to quantum; and **Layden**, Q averaged over the grid points with γ ∈ [0.25, 0.6] and t ∈ [2, 20] |

Validation (`validate.py` → `validate.json`):
- the sparse and dense gaps agree to a relative error of 8e-8;
- Q row sums equal 1 to 2e-15, and Q is exactly symmetric;
- **the Layden SK result is reproduced**: k_q = 0.270, k_uniform = 0.941, k_local = 1.11 (n = 4..8, 24 instances per n),
  against the published 0.264, 0.948 and 0.94.

## Results

Instance families (the n-qubit instance nests inside the larger table):

| family | tables | n | notes |
|---|---|---|---|
| `relaxed_alph2` | 5O37A, 3GAHA, 2AB0A (amb, 12-bit) | 6..10 | main family; n = 10 costs ~133 s per instance under load |
| `relaxed_alph2_b10` | 3 × rnd (5O37A, 3GAHA, 2AB0A) + 3 × amb (3BHLA, 3M3PA, 7B4RA), 10-bit | 6..9 | replicate family |
| `frozen_alph2` | amb + rnd × 3 crops | 6..9 (amb n = 10 for 2 crops) | golf-course landscapes (§5) |
| `frozen_alph4` | amb + rnd × 3 crops, 2 qubits/residue | 6, 8 | too few n for a fit |
| `SK` control | Layden's ensemble, 8 instances per n | 4..9 | tests Layden's own claim against our classical adversary |

All fits use the same coarse (γ, t) grid at every n. The fine grid, run at n ≤ 8, beats the coarse-grid tuned optimum
by a median factor of 1.16 (max 2.4, 72 comparisons), so the coarse grid under-tunes the quantum chain by at most ~2×.

### 1. Absolute gaps: the quantum chain is below the quadratic line everywhere [MEASURED]

- **δ_q(tuned) > δ_c^{1/2}** (δ_c = best classical, including idealised ST and mean-field): **0% of protein-instance
  records**, at every T and every n. The largest values of δ_q / δ_c^{1/2} are:
  - `relaxed_alph2`: 0.68
  - `relaxed_alph2_b10`: 0.51
  - `frozen_alph2`: 0.74
  - `frozen_alph4`: 0.85
  - SK: 1 record of 48 (1.09, T = 1)
- **Gap ratio δ_q / δ_c at the largest n (median):**
  - `relaxed_alph2` (n = 10): 4.9 / 3.9 / 2.5 at T = 1 / 2 / 4
  - `relaxed_alph2_b10` (n = 9): 2.0 / 1.8 / 1.6
  - `frozen_alph2`: 3.5–4.1
  - SK (n = 9): 9.5 / 3.5 / 1.5

  The largest protein-instance ratio is 12.7 (`frozen_alph4`, n = 8).
- **The best classical chain is never local Metropolis.** It is a random-subset flip (pflip, q = 0.2–0.3: the γ = 1
  classical twin of the quench) or a uniform/local mixture. Its gap decays with k_c = 0.39–0.98, while local gaps are
  1e-6 to 1e-23 (censored below 1e-12 in the frozen family). Layden's comparators are therefore the wrong baseline for these landscapes.
  - Simulated tempering with exact weights is competitive per joint step. At joint gap / K it is never the maximum.

### 2. Scaling exponents, <δ> ∝ 2^{-kn} (geometric mean, bootstrap 90% CI over instances) [MEASURED; n ≤ 10 only]

| family | T | k_local | k_best classical | k_q tuned | k_q Layden | k_q/k_c tuned | k_q/k_c Layden |
|---|---|---|---|---|---|---|---|
| relaxed_alph2 (n 6–10) | 1 | 2.20 | 0.558 [0.42, 0.70] | 0.314 [0.21, 0.42] | 0.319 | **0.56** | 0.57 |
| | 2 | 1.37 | 0.452 | 0.296 | 0.316 | **0.65** | 0.70 |
| | 4 | 0.66 | 0.385 | 0.290 | 0.352 | **0.75** | 0.91 |
| relaxed_alph2_b10 (n 6–9) | 1 | 1.62 | 0.755 [0.56, 0.95] | 0.247 [0.17, 0.32] | 0.418 | **0.33** | 0.55 |
| | 2 | 0.97 | 0.717 | 0.257 | 0.401 | **0.36** | 0.56 |
| | 4 | 0.67 | 0.650 | 0.275 | 0.366 | **0.42** | 0.56 |
| frozen_alph2 (n 6–9) | 1 | censored | 0.979 [0.53, 1.45] | 0.387 | 0.458 | 0.40 | 0.47 |
| | 2 | censored | 0.545 | 0.393 | 0.461 | 0.72 | 0.85 |
| | 4 | censored | 0.512 | 0.386 | 0.460 | 0.75 | 0.90 |
| SK control (n 4–9) | 1 | 1.38 | 0.838 [0.70, 0.99] | 0.347 | 0.324 | 0.41 | 0.39 |
| | 2 | 0.80 | 0.667 | 0.382 | 0.297 | 0.57 | 0.45 |
| | 4 | 0.52 | 0.500 | 0.322 | 0.219 | 0.64 | 0.44 |

Super-quadratic means k_q/k_c < 0.5. Per-instance slope ratios for the tuned chain:
- `relaxed_alph2`: 0.28–0.86 (median 0.52–0.74);
- `relaxed_alph2_b10`: 0.11–0.93 (median 0.25–0.36);
- under the untuned Layden protocol, `relaxed_alph2_b10` has median 0.46–0.57.

**Reading.**
- [MEASURED] In the family that reaches n = 10, the exponent ratio is 0.56–0.75, which is sub-quadratic.
- [MEASURED] A nominally super-quadratic ratio (0.33–0.42) appears only in the replicate family, only at n ≤ 9, and
  only with per-instance oracle-tuned (γ, t). Under Layden's own untuned protocol it is ≈ 0.55, i.e. quadratic.
- [MEASURED] In that family the quantum gap starts *below* the classical gap at n = 6–7 (0.096 vs 0.133) and falls
  slowly. The small k_q is partly a low, saturating prefactor, not a large gap.
- [MEASURED] On Layden's own SK ensemble, replacing local/uniform with the tuned classical chain moves k_q/k_c
  from their 0.28 (verified: 0.264/0.94) to 0.39–0.41 at T = 1 and 0.44–0.64 at T = 2–4. The "cubic/quartic" enhancement
  becomes ~2.5× in the exponent at T = 1 and ≤ 2.3× at T ≥ 2 against a tuned classical proposal (n ≤ 9, 8 instances per n).

### 3. The gap is a worst-case metric; warm starts erase most of the difference [MEASURED, `diag_warm.json`]

For the 12 largest-n relaxed instances at T = 1 and 2 (24 cases):
- x\* (state 0; the multistart minimum used to build the instance, DEP) carries π(x\*) ≥ 0.9 in 13 of 24 cases.
- The best classical chain started at x\* is already within TV 0.01 in 7 of 24 cases. Its largest warm-start mixing
  time is **197 steps**.
- In 17 of 24 cases the slowest classical mode puts > 90% of its L²(π) weight on states with E − E_min > 10T. Those
  states have negligible Boltzmann mass, so the gap mostly measures escape from irrelevant high-energy states.
- Where warm-start mixing is non-trivial (17 cases), the quantum chain is faster by **1.3–6.1×** from x\* and 0.9–4.6×
  from a uniform start.

### 4. Cost: the K-101 floor for a power-law speedup [DERIVED + MEASURED inputs]

**Per-step costs.**
- Quantum step (per Trotter step): 2 coherent A80 energy evaluations (compute and uncompute) at G = 3×10⁴·L² = 2.7×10⁷ Toffolis
  (T3 central, L = 30), 1 µs per Toffoli (K-101's most optimistic rate).
- Classical step: one E-only evaluation, **c = 2.3 ms** [MEASURED here, one core, under load].
- Break-even needs δ_q/δ_c ≥ R = 2·r·G·t_T / c:
  - **R = 2.3×10⁵ at r = 10 Trotter steps**. Layden's hardware Δt = 0.8 puts the tuned t* ≈ 7–12 at r ≈ 9–15.
  - **R = 784** in an optimistic sensitivity case: a 30×-cheaper discrete-instance oracle (G = 10³·L²) and r = 1.
- The measured δ_q/δ_c is ≤ 5.2 (relaxed) and ≤ 12.7 overall. **That is short of break-even by 4.3–4.6 orders of magnitude
  (central) or 1.8–2.2 orders (optimistic).**

**For a power law δ_q = δ_c^α.** The break-even wall-clock per relaxation time is T*_Q = C_q^{1/(1−α)}·c^{−α/(1−α)}, which
generalises K-101: α = 1/2 gives C_q²/c. The table extrapolates the fitted exponents beyond n ≤ 10 [INFERENCE, highly uncertain]:

| family, T = 1 | n* central (r = 10) | T*_Q central | n* optimistic (r = 1) | T*_Q optimistic |
|---|---|---|---|---|
| relaxed_alph2 | 74 | 1.5×10⁵ days | 40 | 0.33 days |
| relaxed_alph2_b10 (tuned, the only super-quadratic fit) | 42 | 34 days | 26 | 10 min |
| frozen_alph2 | 38 | 490 days | 24 | 56 min |
| SK | 39 | 176 days | 23 | 15 min |

At T = 2 and 4 every n* is larger (46–181) and every T*_Q is longer.

Even the most favourable line needs all of the following at once:
1. the n ≤ 9 oracle-tuned exponent to hold over 17 more qubits;
2. a 30× cheaper coherent oracle than T3;
3. 1-µs logical Toffolis and a single Trotter step.

Its n* ≈ 26 is also about the whole 27-residue crop (binary alphabet). For RELAXED instances the coherent oracle must also run a
reversible L-BFGS relaxation (~80 iterations; the pebbling overhead is 1.9–4.4× by T4), which multiplies G by ~10² per step. The classical step grows by the same ~10²; only the reversibility overhead stays against quantum.

### 5. Mechanism notes [MEASURED]

- **Orfi–Sels localisation is visible directly.** With raw Frobenius normalisation, one outlier state 234 nats above
  E_min stays put under the Layden-averaged quench (Q_ii = 0.975). That fixes a T-independent gap of 0.0253
  (5O37A, n = 8). Clipping H_E at 40 nats removes it: the proposal Hamiltonian is a free design choice because MH corrects it.
- **FROZEN tables are golf courses.** x\* is the table minimum, and the first excited state lies 8–96 nats higher
  (n = 12). At T ≤ 4 sampling is trivial from x\*. Local gaps (1e-11 to below 1e-23) are set by clash-trapped
  states of negligible mass.

## 6. Verdict

**KILLS** under the pre-stated rule, at the practical level. The exponent question is left partly open at n ≤ 10.
- **The best classical chain matches the quantum chain to within a factor ≤ 5.2 in gap (relaxed; ≤ 12.7 overall) at every measured size.**
  - δ_q never exceeds δ_c^{1/2} on any protein instance.
  - Warm-start mixing from the classically found x\* takes ≤ 197 steps, and the quantum chain gains 1.3–6.1× there.
  - Break-even needs a gap ratio of 7.8×10²–2.3×10⁵ per step.
- **Theoretical level L1 [MEASURED small-n numerics].** The exponent ratio is sub-quadratic (0.56–0.75) in the family
  measured to n = 10. It is nominally super-quadratic (0.33–0.42) only in the n ≤ 9 replicate family with oracle-tuned (γ, t),
  and ≈ quadratic (0.55) there under Layden's protocol.
- **Practical level L0.**
- **Residue (not a lead).** Whether the oracle-tuned Layden exponent stays below k_c/2 on relaxed protein
  instances at n ≥ 12 is open. That test needs n = 12–16 exact gaps (N = 4096–65536), beyond this lane's budget, or a matrix-free
  Krylov gap. Even a positive answer leaves T*_Q ≥ 10 min–34 days per relaxation time on a 30-residue toy under optimistic
  hardware. It does not touch the continuous-torsion K-101 kill.

## Resource ledger (MEASURED)

- CPU: ~40 CPU-min in total, all single-threaded (OMP/MKL/OPENBLAS = 1).
  - instance builds ~8 min (4096 pinned relaxations ≈ 96–146 s per 12-bit table)
  - gap runs ~24 min: main 850 s; coarse reruns, replicates and SK 423 s
  - validation 14 s; warm-start diagnostic ~1.5 min
- Peak RAM < 0.6 GB (dense 1024² float64 matrices).
- Simulator: exact dense linear algebra (numpy eigh/eigvalsh; scipy splu/eigsh). There is no quantum hardware and no
  Trotter or noise model. **Simulator time is not quantum runtime.** The quantum cost in §4 is a resource model, not a measurement.
- Leakage: DEP only. No native coordinates were read. (γ, t) tuning and chain selection use the instance's own energies.
  Classical and quantum were tuned on the same per-instance basis.

## Files

- `build_instances.py`: instance tables → `instances/*.npz`, including `<crop>_xstar.npz`
- `qemcmc.py`: generators, sparse/dense gaps, proposals
- `validate.py` → `validate.json`
- `run_gaps.py` → `results/<table>[_cg]_n<n>.json` (per instance; atomic). `_cg` = coarse-grid rerun at n ≤ 8.
- `analyze.py` → `summary.json` (tables, fits, bootstrap CIs, per-instance slopes, cost model, break-even extrapolation)
- `diag_warm.py` → `diag_warm.json`

## Next tests (only if the residue is reopened)

1. Exact gaps at n = 11–14 on RELAXED tables via matrix-free Krylov on the quench, with (γ, t) tuned by the same rule on both
   sides. Pre-register k_q < k_c/2 with a bootstrap CI excluding 0.5.
2. Stronger classical proposals at equal energy-evaluation budgets: multiple-try Metropolis with pflip candidates,
   adaptive pflip rates, population annealing.
3. Warm-start mixing (TV from x\* and from the prior product) as the primary metric instead of the worst-case gap.
4. Orfi–Sels IPR bound on the protein instances, to test whether the tuned quench is near the bound.
