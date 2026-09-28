# ROUND3 lane r1sim_hybrid_plus: stronger polynomial adversaries for the R1-SIM echo

_2026-09-28. Lane agent `r1sim_hybrid_plus`. Scope: can any polynomial-cost classical method reproduce the exact protein ¹H
first-order echo F_ab(t) = Tr[W Z_b W Z_b]/2^N (W = Z_a(t)) of the N = 16 and N = 18 typicality cones within σ = 0.01
over 80–320 µs on both probes (1UBQ p19 and p245)? Methods: (a) Starkov–Fine coupled quantum clusters, (b)
classical spins with quantum few-spin corrections, (c) a quantum core with a quantum-cluster bath, (d) a
cluster-correlation expansion with the hybrid as base._

## Bottom line

**The kill rule did not fire.** No polynomial method reproduces the N = 16/18 echo within σ = 0.01 on both probes.
Across 37 coupled-cluster runs, a 27-sub-run CCE and 4 zero-compute adversaries, the best maximum errors in the window
are:
- **p19, N = 16:** 0.029 (per-probe calibrated mean field) and 0.035 (12-spin exact core, at about the cost of the exact
  run).
- **p245, N = 16:** 0.091.
- **N = 18:** 0.28 (p19) and 0.081 (p245).

[MEASURED]

Errors do not shrink with polynomial method order:
- Coupled-cluster size k = 6 → 8 stays flat at 0.21–0.29.
- CCE order 0 → 1 → 2 goes 0.39 → 0.62 → 0.57.

They shrink only along the exponential ladder where the exact cluster approaches the whole system: k = 4…12 at N = 16
gives 0.54 → 0.035, and the k = 12 run costs about as much as exact N = 16. [MEASURED]

**Verdict: SUPPORTS**, in the narrow R1-SIM sense that approximation-hardness of the converging echo survives four more
method families. This lane cannot show that the echo exceeds *exact* classical reach. N = 16/18 are exactly simulable
(10 min–3 h), and that question belongs to T-A (N = 20/22 convergence). [INFERENCE]

## Setup (identical to `scripts/nmr_cone.py`)

**Geometry and circuit:**
- 1UBQ, N nearest protons to the probe, b0 = random_b0(1000).
- Observed sites bs = [1, 7, 8, 9]; a = 0.
- Fused-pair Trotter circuit, dt = 2 µs. Echo times 40, 80, 160, 240, 320 µs.

**Reference:** the exact typicality cone `ADVERSARIAL/R1_theory_hardness/typicality_cone/1UBQ_p{19,245}_N{14,16,18}.json`.
It uses one random vector, so its own error is about 2^(−N/2): 0.008 at N = 14, 0.004 at N = 16, 0.002 at N = 18.

**Metric:** max over b and t ∈ [80, 320] µs of |F_method − F_exact|. The method SE is the sample SE; M = 48 unless noted.

### Framework: `cqc_echo.py`

**Partition.** All N spins are split into groups, and every group is an exact state vector.
- Intra-group couplings are applied as the exact reference pair gates, precomputed as magnetisation-sector block
  unitaries (equal to `apply_step` to 2e-16).
- Inter-group couplings use Starkov–Fine correlation-preserving mean fields: m_j = sqrt(2^n_g + 1)⟨I_j⟩.
  - Source: PRB 101, 024428 (2020), arXiv:1911.00990, Eqs. (9)–(10) and (19)–(20), read from the arXiv PDF.
  - A one-spin group is therefore exactly a classical spin of length sqrt(3)/2, i.e. the hybrid bath (verified).

**Integrator.**
- Each step is a sequential group sweep (dt/2), then the intra-group gates (dt), then the reverse sweep (dt/2).
- The backward map is the exact inverse of the forward map. Measured reversibility error is 2.7e-13 after 80 + 80 steps,
  so no spurious irreversibility is injected.
- With one group the code reproduces sector-exact N = 10 within typicality SE (1.5e-3).

**Echo estimator.**
- Haar state per group; branches Ψ and Z_bΨ; W = backward ∘ Z_a ∘ forward on the product manifold.
- `F_tdh` is the product of all group overlaps (time-dependent-Hartree Loschmidt echo).
- `F_core` uses only the groups that contain a or b (the convention of the old hybrid).

**Back-action knob `ba` for the core group:**
- `sf`: sqrt(D+1), faithful Starkov–Fine.
- `unamp`: factor 1, as in the old `hybrid_echo.py`.
- `none`: a reversible external classical field, the second-cumulant limit.

**Partitions:**
- `near10`: the 10 nearest spins as core.
- `kl<k>` / `kls<k>`: swap-refined partitions that maximise intra-group Σd², i.e. the weakest mean-field cut, with
  {a} ∪ bs pinned; `kls` keeps the core size. They capture 0.88–0.92 of Σd², against 0.67–0.75 for `near10`.

### Other scripts

**`cce_hybrid.py`: (b)/(d), CCE with the hybrid as base.**
- F^(0) = hybrid with core {a} ∪ bs and a classical bath (ba = none).
- Order 1 promotes each bath spin to the quantum core; this is a "quantum two-spin"-type correction per bath spin.
- Order 2 adds screened pair corrections among the top-6 bath spins (27 sub-runs, max core 7).
- Additive and multiplicative links.
- Common random numbers come from a product-state initial ensemble in global spin order. It is unbiased for exact
  evolution; product-init vs sector-exact agree within 1 SE at N = 10.
- The Navez–Starkov–Fine equations themselves (arXiv:1812.02155, abstract read; EPJ ST) were not implemented. The
  abstract reports singular long-time behaviour even for a chain. The CCE promotion is this lane's well-defined
  stand-in [INFERENCE].

**`compare.py`:** scoring, plus zero-compute adversaries built from existing data.

## Results

Maximum error over b and t in [80, 320] µs; σ = 0.01. All MEASURED unless tagged.

**Hybrid family: exact 10-spin core (`near10`) plus classical spins**

| Method | p19 N16 | p245 N16 | p19 N18 | p245 N18 | Cost (wall s, 1 thread, loaded host) |
|---|---|---|---|---|---|
| Old hybrid (`unamp`), from `R1SIM_hybrid` | 0.147 | 0.198 | 0.184 | 0.224 | ~2300 (old code) |
| Faithful Starkov–Fine (`sf`) | **0.553** (F → 0.00 by 160 µs) | — | — | — | 71 |
| No back-action (`none`) | 0.108 | — | — | — | 68 |

**(a) Pure CQC.** All groups ≤ k, coupling-refined. Entries are sf / unamp / none; N = 18 was run with `none` only.

| k | p19 N16 | p245 N16 | N18 (p19, p245) |
|---|---|---|---|
| 4 | 0.550 / 0.529 / 0.538 | 0.832 / 0.751 / 0.571 | — |
| 6 | 0.540 / 0.299 / 0.239 | 0.840 / 0.422 / 0.282 | — |
| 8 | 0.552 / 0.211 / 0.237 | 0.808 / 0.266 / 0.292 | 0.275, 0.310 |

**(c) Quantum core plus quantum-cluster bath**

| Method | p19 N14 | p19 N16 | p245 N14 | p245 N16 | p19 N18 | p245 N18 |
|---|---|---|---|---|---|---|
| Core 10 + bath cluster 4–8 (`kl10`/`kls10`, `none`) | 0.036 | **0.062** | 0.343 | **0.091** | 0.277–0.312 | **0.081** |
| Same with `unamp` back-action | — | 0.079 | — | 0.100 | — | — |
| Same, Ising-only mean field | — | 0.247 (bias +0.115) | — | — | — | — |
| Same, λ calibrated on the same probe's exact N = 14 (λ = 0.86 / 1.54) | — | **0.029** (SE 0.011) | — | 0.135 | — | — |
| Core 12 + bath 4 (`kls12`) | — | **0.035** (SE 0.005), 442 s | — | — | — | — |

**(b)/(d) CCE with hybrid base (p19, N = 16)**

| Link | Order 0 | Order 1 | Order 2 |
|---|---|---|---|
| Additive | 0.392 | 0.615 (SE 0.33) | 0.571 (SE 0.28) |
| Multiplicative | — | 1.162 | 0.308 |

**Zero-compute adversaries built from existing data**

| Method | p19 N16 | p245 N16 | p19 N18 | p245 N18 |
|---|---|---|---|---|
| Hybrid + [exact(N−2) − hybrid(N−2)] | 0.077 | 0.043 | 0.053 | 0.065 |
| Core-size extrapolation, Nc 10, 12 → Ntot | 0.067 | 0.309 | — | — |
| Exact(N−2) as predictor | 0.139 | 0.132 | 0.037 | 0.057 |
| Linear-in-N extrapolation | 0.281 | 0.159 | 0.133 | 0.152 |

Reference cost: exact N = 16 typicality took 632 s wall (governed). N = 18 took 9509 s wall (governed, with suspensions).
Full per-(b, t) values are in `summary.json` (also `compare_output.txt`). Raw runs are in `out/*.json` (37 files) and
`out_cce/` (the CCE checkpoint keeps every per-sample value).

## Mechanisms (why the families fail)

1. **Correlation-preserving amplification collapses the echo.**
   - [MEASURED] Starkov–Fine back-action amplification sqrt(D+1) drives F to 0.000 ± 0.004 for t ≥ 160 µs in every
     partition (errors 0.54–0.86).
   - [INFERENCE] The factor is designed for 2-point functions (FIDs). For an OTOC it turns the local Z_a flip, of size
     O(2^(−n/2)), into an O(1) kick of a chaotic mean-field bath, and the kick is never undone on the way back.
2. **Mean-field transverse coupling breaks Z conservation between clusters.**
   - [MEASURED] Full mean-field window-mean bias is negative (over-decay) in 17 of 25 `none`/`unamp` runs, 15 of 18
     at N = 16; at N = 18 the sign is mixed and site-dependent (see 4). Ising-only (zz) mean field: +0.115 (under-decay).
   - [INFERENCE] Exact dynamics conserve Σ_i Z_i, and the slow late-echo plateau is tied to it. A classical transverse
     field replaces conserving flip-flops with non-conserving rotations, while zz-only forbids operator transfer across
     the cut altogether.
3. **No transferable one-parameter fix.**
   - [MEASURED] The λ that zeroes the N = 14 bias is 0.86 (p19) and 1.54 (p245). For p245 the N = 14 calibration points
     the wrong way at N = 16: λ = 1 already over-decays there, and λ = 1.54 gives 0.135.
   - [INFERENCE] Not checked at N = 18: bias is monotone in λ in all three measured pairs, and the p19 N = 18 error is a
     +0.28 under-decay at b = 8, so λ = 0.86 would enlarge it.
4. **Errors are site-dependent and change sign.** [MEASURED]
   - They concentrate on sites whose strong partners are cut by the partition: p19 N18 b8 +0.28 while b1 and b7 are
     −0.07 to −0.09; p245 N14 b1 and b8 +0.2 to +0.34.
   - Accuracy therefore depends on the instance's cut structure, and it is not monotone in N: p19 errors are 0.036 →
     0.062 → 0.28 at N = 14 → 16 → 18.
5. **CCE on a chaotic classical base does not converge.**
   - [MEASURED] Promoting one bath spin changes the classical trajectories, giving increments |d_j| of 0.05–0.41 with
     SE ≈ 0.3 even under common random numbers. The series does not converge (order 2 is worse than order 0).
6. **The only convergent ladder is exact simulation in disguise.**
   - [MEASURED] Core size k (p19, N = 16): 0.54, 0.24, 0.24, 0.062, 0.035 for k = 4, 6, 8, 10, 12.
   - [MEASURED, wall-clock on a loaded host, indicative only] The k = 12 run takes 442 s, the same order as exact
     N = 16 (632 s).
   - [INFERENCE] Reaching σ needs an exact cluster holding ≥ 75% of the system.

## Claim levels

- **Theoretical: L1 (narrow).** Empirical failure of 4 more approximation families (plus 4 zero-compute adversaries) on
  2 instances at N = 16–18, a converging reference. It is not a hardness result.
- **Practical: L0.**
  - Exact simulation still reaches N = 16–18.
  - R1 stays killed as a protein-structure advantage (K-105). This lane does not touch the reversal-horizon or value kills.
- **Claim category:** at most 3 (a physics-simulation resource question). No category-1…6 advantage for protein
  structure is supported.

**Does NOT support:**
- "OTOC(1) of protein networks is classically hard."
- Any statement about N ≥ 20.
- Any advantage for structure determination.

## Caveats

- **SE and sample size.** M = 48 gives SE 0.005–0.022. The two closest methods (0.029 and 0.035 for p19 N16) are about
  3σ outside the band; neither was repeated at larger M.
- **Reference convergence.** The reference itself is unconverged in N: |F18 − F16| is up to 0.057. The physical target
  is N → ∞.
- **Families not tried:**
  - cluster truncated Wigner;
  - dissipation-assisted operator evolution;
  - neural quantum states;
  - a Navez–Starkov–Fine two-spin closure built from the actual EPJ ST equations (the full text was not read).
- **Wall-clock timing.** Costs are wall-clock on a host at 95–99% CPU. Simulator runtime is not physical quantum
  runtime.

## Resource ledger

- **Compute:** single-threaded throughout (OMP/MKL/OPENBLAS = 1), peak RAM < 0.3 GB.
- **Time:** 37 CQC runs took 1786 s wall; the CCE took 185 CPU-s; self-tests, validation and timing about 150 s. Total
  ≈ 35 min, within the 45 CPU-min budget.
- **Quantum resources:** none. No leakage issue: native structures only define the model Hamiltonian, as in the
  reference.

## Next tests

1. **Pin the two closest methods.** Run the calibrated-λ core-10 and core-12 methods at M ≥ 192 at N = 16/18 on both
   probes, to fix their errors to ±0.003 (about 20 CPU-min).
2. **Path-aware core selection.** Choose the core from exact N = 12 influence scores for each b rather than from Σd².
   This tests whether the site-dependent cut errors (mechanism 4) drop below σ at N = 18 with a 10-spin core.
3. **Families not yet tested.** Cluster-TWA and DAOE-type operator truncation at N = 18.
4. **R1-SIM itself is decided only by exact-convergence T-A (N = 20/22).** The approximation route cannot settle it.
   KILL R1-SIM if |F_N − F_(N+2)| < σ on both probes at some N ≤ 22.
