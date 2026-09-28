# Classical-adversary verification of lane `r1sim_hybrid_plus`

_2026-09-28. Adversarial verifier (classical)._

**Claim under attack.** No polynomial-cost classical approximation reproduces the exact first-order dipolar echo
F_ab(t) = Tr[W Z_b W Z_b]/2^N of the 1UBQ ¹H cones within σ = 0.01 over 80–320 µs, on both probes (p19, p245), at
N = 16 and N = 18. The lane's verdict is SUPPORTS, narrowly: this is approximation-hardness only, with theory level L1
and practical level L0.

**My verdict: NOT REFUTED in its narrow, empirical form.** I found no credible polynomial classical route. I built a
stronger adversary than any in the lane, and it also fails. Its second order diverges, which supports the lane's
statement that "errors do not shrink with method order".

The claim's universal wording ("No polynomial-cost classical approximation…") still overstates what was tested:
- about 6 families, including the ones I added here;
- 2 instances, at 2 sizes that are both still exactly simulable.

It should be read as "none of the tested families". It is not a hardness result.

Tags: MEASURED (computed here, file cited), DERIVED, INFERENCE, UNPROVEN.

## 1. Re-checks of the lane's own evidence

**CQC self-test re-run (MEASURED, `cqc_selftest_rerun.txt`):**
- One group matches sector-exact N = 10 to 1.46e-3, within the typicality SE of 1.48e-3.
- Forward–backward reversibility error is 5.2e-13.
- One-spin groups have length √3/2, as expected.

This reproduces the lane's validation.

**Scores reproduced (MEASURED, `rescore_lane.py` → `rescore_lane.json`).** Re-scoring the lane's 37 run files (74
estimator rows) directly against the reference gives the lane's best numbers per cell:

| Cell | Best max error |
|---|---|
| p19 N14 | 0.036 |
| p19 N16 | 0.029 |
| p19 N18 | 0.275 |
| p245 N14 | 0.343 |
| p245 N16 | 0.091 |
| p245 N18 | 0.081 |

**The lane's failures are statistically robust (MEASURED).**
- I computed a lower bound on the maximum bias: LB = max over (b, t) of |ΔF| − 2.5·√(SE_method² + SD_ref²).
- All 74 of 74 rows have LB > σ.
- Even the lane's closest result (λ-calibrated, p19 N16, 0.029, SE 0.011) has LB = 0.020.

**The kill rule is passable, so it is not noise-dominated (MEASURED, `noise_floor.py` → `noise_floor.json`).**
- I compared a deterministic sector-exact F on the full N = 12 cluster with the one-vector typicality reference at
  N = 12, over 28 window points.
- rms / 2^(−N/2) = 0.31 (p19) and 0.64 (p245); max / 2^(−N/2) = 0.60 and 1.56.
- [DERIVED] The implied reference floor on the lane's max-norm metric is about 0.004–0.006 at N = 16 and about 0.002–0.003
  at N = 18. It uses up about half of σ at N = 16, but an exact method would still pass.

## 2. New classical adversaries (not in the lane)

All results below are MEASURED with `subcluster.py`, reported in `subcluster_report.json` and `report_output.txt`,
with raw values in `cache.json`.

**Common setup.** Every run is a deterministic, sector-exact simulation of the reference Trotter circuit restricted to
a subcluster. Dropped spins have their gates deleted, and the remaining gates keep their order, so there is no sampling
noise and no mean-field bath. This removes both failure mechanisms the lane identified: chaotic classical trajectories
and mean-field breaking of Z conservation.

**Method (i): per-(a, b) path-aware exact subcluster (`sub_g2k`).**
- The subcluster starts from {a, b}.
- It grows greedily by the total squared coupling Σ_{i∈S} d_ij² to the current set.
- This is the lane's own untested "next test 2".

**Method (ii): exact-base spin-addition cluster expansion (CCE / NLCE-type), per b.**
- The base is the g2 core C with |C| = k.
- Order 1 adds each remaining spin j, costing (N − k) exact runs of k + 1 spins.
- Order 2 adds every pair, with inclusion–exclusion.
- Both additive and multiplicative (log-additive) links were tested.
- The cost is polynomial in N at fixed k.

Maximum error over b ∈ {1, 7, 8, 9} and t ∈ [80, 320] µs (σ = 0.01):

| Method | p19 N16 | p245 N16 | p19 N18 | p245 N18 |
|---|---|---|---|---|
| sub_g2, k = 10 | 0.216 | 0.191 | 0.295 | 0.229 |
| sub_g2, k = 11 | 0.202 | 0.075 | 0.263 | 0.128 |
| nested exact(k = 12) predictor | 0.141 | 0.126 | 0.149 | 0.132 |
| order 1, multiplicative, base 8 | 0.436 | 0.064 | 0.465 | 0.099 |
| order 1, multiplicative, base 9 | 0.066 | 0.061 | 0.076 | 0.059 |
| **order 1, multiplicative, base 10** | **0.050** | **0.064** | **0.066** | **0.062** |
| order 1, multiplicative, base 11 | 0.077 | – | – | – |
| order 1, additive, base 10 | 0.075 | 0.057 | 0.066 | 0.074 |
| order 2, multiplicative, base 8 | 0.233 | 0.527 | 0.499 | 0.927 |
| order 2, additive, base 8 | 0.893 | 0.388 | 1.030 | 0.582 |
| Lane's best, for comparison | 0.029 / 0.035 | 0.091 | 0.275 | 0.081 |

**Findings:**
- **The best new method is uniform but not good enough (MEASURED).** First-order multiplicative expansion around a
  10-spin exact core reaches 0.050–0.066 on all four cells, with mean bias of ±0.01.
  - It beats every lane method on p245 N16, p19 N18 and p245 N18.
  - Its cost is 7–9 exact runs of at most 11 spins per b, about 2.5 s each on this host. That is far below exact N = 18
    typicality (9509 s).
  - It is still 5–7σ outside the band.
  - Its errors have both signs and depend on b and t (for example p19 N18 b1 +0.066 at 320 µs, p245 N18 b9 −0.058), so no
    single fudge factor removes them.
- **The error does not converge with order or base size (MEASURED).**
  - Second order diverges, to 0.23–1.03. This is the classic cluster-expansion failure in a dense dipolar network.
  - Order-1 error against base size is non-monotone: 0.066 → 0.050 → 0.077 for base 9 → 10 → 11 at p19 N16.
  - This confirms the lane's mechanism claim for a non-chaotic, exact-base expansion too.
- **Exact subclusters without a bath are biased upward (MEASURED).** They sit +0.08 to +0.11 too high on average
  (under-decay: fewer channels and a larger finite-size plateau). k = 12 is still 0.13–0.18.
- **Exact(N−2) with a cheap-method difference correction is not reliable (MEASURED, `delta_correction.py` →
  `delta_correction.json`).**
  - F_ref(N−2)·M_N/M_(N−2) gives 0.022 at p245 N18 but 0.096 at p19 N16 and N18.
  - This adversary costs exponentially, so it bears only on T-A.

## 3. Sparse Pauli dynamics at the start of the window

MEASURED with `spd_probe.py` → `spd_probe.json`, on p19 N = 16.

| Truncation ε | Cost | Strings | Kept norm² | Max error at 80 µs |
|---|---|---|---|---|
| 1e-3 | 5.6 s | 4.8e3 at 80 µs | 0.81 | 0.049 raw; 0.19 when the dropped weight is renormalised |
| 1e-4 | 314 s, budget hit at 68 µs | 2.6e5 | 0.957 at 60 µs | not reached |

**Interpretation.**
- [DERIVED] Z_a(t) commutes with Σ Z. It lives in the charge-0 operator space of dimension C(2N, N), which is 6.0e8 at
  N = 16 and 9.1e9 at N = 18.
- [INFERENCE] Already at 80 µs, sparse Pauli dynamics needs more than 2^16 strings, and its cost is comparable to the
  whole exact run. By 160 µs or later the operator is scrambled over the cluster. It is not a credible route in this
  window, consistent with the earlier `pauli_cone.py` result (discarded norm above σ by 40 µs for N ≥ 16).

## 4. Families still untested (the claim is only as strong as this list)

**Not attempted in this lane's budget (UNPROVEN either way):**
- MPS/MPO/TDVP;
- neural quantum states;
- spinDMFT and its cluster/non-local variants;
- DAOE;
- a proper cluster-TWA.

**[INFERENCE] Why none is expected to reach σ = 0.01 at 80–320 µs:**
- For N ≤ 18 on an all-to-all 3-D dipolar graph, MPO/MPS bond dimensions would have to approach the exact limits (4^(N/2)
  for an operator).
- spinDMFT targets two-point autocorrelations.
- DAOE damps exactly the high-weight strings that set F_ab.

## 5. Where the claim is weaker than stated

1. **The universal quantifier.** "No polynomial-cost approximation" is inferred from about 6 families on 2 instances at
   N = 16/18. At fixed N, "polynomial" is defined only through each family's order parameter. This is empirical
   L1 evidence, not a separation or hardness result.
2. **The best-achievable frontier was understated.** The lane's best numbers at N = 18 (0.275 / 0.081) were not the real
   polynomial frontier. An exact-base first-order expansion does 0.059–0.066 uniformly. The gap to σ is about 6×, not up
   to 28×.
3. **"Cost approaching exact" depends on the implementation.**
   - The lane's k = 12 CQC cost 442 s. A deterministic sector-exact 12-spin subcluster costs about 17 s here, against
     632 s for exact N = 16 typicality.
   - The conclusion (only near-whole-system exact clusters converge) still stands, because no k ≤ 12 subcluster or
     expansion gets below 0.05.
4. **The target is a finite cluster.** The reference moves by up to 0.057 between N = 16 and N = 18. Matching N = 16/18
   to 0.01 means matching finite-cluster values, not the physical N → ∞ echo.
5. **Nothing here touches R1's kills (K-105) or protein-structure value.** Exact classical simulation reproduces every
   target number in this lane (10 min–3 h), so there is no quantum resource advantage at these sizes. Claim category 3
   at most; practical level L0.

## Ledger

**Compute:**
- Single-threaded (OMP/MKL/OPENBLAS = 1).
- Sector-exact subclusters: 958 CPU-s (649 cached runs, k = 8–12).
- Sparse Pauli dynamics probe: 320 s. CQC self-test: about 30 s. Overheads: about 60 s.
- **Total about 23 CPU-min.** Peak RAM under 0.5 GB.
- No background processes. Nothing outside this folder was modified.

**Other fields:**
- **Leakage:** none. Native structures only define the model Hamiltonian, as in the reference.
- **Quantum resources:** none.

## Files

| File | Contents |
|---|---|
| `subcluster.py` | Methods (i) and (ii); stages `sub`, `add1`, `add2`, `report`; resumable cache |
| `cache.json` | Every subcluster F(t) with its cost (atomic writes) |
| `subcluster_report.json` | Per-(method, probe, N) errors, per-b errors, bias and F(t) |
| `report_output.txt` | Printed report |
| `noise_floor.py`, `noise_floor.json` | Reference typicality noise floor |
| `rescore_lane.py`, `rescore_lane.json` | Noise-aware re-score of the lane's runs |
| `delta_correction.py`, `delta_correction.json` | Exact(N−2) plus cheap-method difference adversary |
| `spd_probe.py`, `spd_probe.json` | Sparse Pauli dynamics at 40–80 µs, N = 16 |
| `cqc_selftest_rerun.txt` | Lane self-test re-run |
