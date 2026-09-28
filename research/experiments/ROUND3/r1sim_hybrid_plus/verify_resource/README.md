# Resource audit of lane `r1sim_hybrid_plus` (R1-SIM narrow residual)

_2026-09-28. Adversarial verifier, role RESOURCE AUDITOR. I did not modify anything outside this folder, and I made no
commits._

## Claim under attack

The lane claims that no polynomial-cost classical approximation reproduces the exact first-order echo OTOC(1) of the
1UBQ ¹H cones:
- within σ = 0.01;
- over 80–320 µs;
- on both probes (p19, p245);
- at N = 16 and 18.

Errors shrink only along the exact-core-size ladder, at a cost approaching exact. The lane rates this L1 theoretical and
L0 practical, category 3 at most, and says it tells us nothing about exceeding exact classical reach.

## Verdict

**NOT REFUTED as a narrow measurement, and it carries zero resource weight.** Break-even for any quantum resource claim
on this observable is **not credible**. Practical level L0 is confirmed. The lane *overstates* the classical exact cost,
which makes L0 stronger, not weaker. Two sub-statements need correcting (§2 and §4).

## 1. Every reported failure is real beyond noise [MEASURED], `power_audit.py` → `power_audit.json`

For each run I computed two numbers:
- the Bonferroni lower confidence bound on the true max |bias| over the 16 (b, t) points, using method SE and
  reference SE sqrt((1−F²)/(2^N+1)), family-wise 95 %;
- the noise floor that a zero-bias method would show.

**What is resolved outside the band.** Every coupled-cluster, hybrid, calibrated and zz run has a lower bound above σ:

| Run | Lower bound |
|---|---|
| kls12 p19 N16 | 0.016 |
| λ-calibrated p19 N16 | 0.019 |
| kl10 p19 N16 | 0.035 |
| kl10 p245 N16 / N18 | 0.058 / 0.063 |
| All others | 0.08–0.79 |

**CCE orders 1 and 2 are not resolved.** Their SE is 0.28–0.33 and their lower bounds are −0.05 and +0.03. "CCE does not
converge" is a *variance* statement, not a demonstrated bias. Certifying CCE at σ would need about 10⁴× more samples.
That is itself a cost failure.

## 2. At N ≤ 16 the kill rule sat on the reference noise floor [MEASURED]

**Validation.** `exact_fast.py` reproduces the reference cone exactly at seed 12345 (N = 14: max diff 0.0).

**Exact runs fail the rule at N = 14.** Three independent exact typicality vectors at N = 14 score 0.0151, 0.0179 and
0.0126 against the reference; pairwise exact-vs-exact gives 0.0128–0.0179. All of them "fail" σ = 0.01.

**N = 16 is marginal.** Monte Carlo floors:
- An exact method with its own vector: median 0.010, 95th percentile 0.015.
- A perfect method at M = ∞: 95th percentile 0.011.

So at N ≤ 16 the rule could not have certified even an exact method. The λ calibration used the N = 14 reference, whose
per-point noise is 0.0075.

**The verdict does not change.** Every method fails beyond noise (see §1), but "the kill rule did not fire" is partly
uninformative. Future lanes should use:
- a reference with n_rand ≥ 4, or σ ≥ 0.015 at N = 16;
- lower confidence bounds rather than raw max errors.

## 3. New data point: the fixed-k = 12 core at N = 18 [MEASURED], `cqc_run.py` → `out_cqc/`

I re-ran the lane's unmodified `cqc_echo.py` for p19 at N = 18 with kls12 (groups [12, 6], M = 48). This is the lane's
best N = 16 method.

- **Error:** E = 0.062, lower bound 0.049, SE 0.007, 11.7 SE above σ.
  - Worst point: b8, +0.062 at 160 µs.
  - Late-time over-decay on b1 and b7: −0.045 at 320 µs.
- **Comparison:** 0.035 at N = 16 and 0.277 for kls10 at N = 18.
- **Cost:** 413 CPU-s (448 s wall).

At fixed k = 12 the error grows with N (0.035 → 0.062), so the core needed for σ grows with N, as the lane inferred. The
zero-compute correction kls12(18) + [exact(16) − kls12(16)] gives 0.040 (lower bound 0.025). Exact(16) as a predictor of
exact(18) gives 0.026 at the 4 lane times.

## 4. Cost accounting corrections [DERIVED from counts; wall-clock calibrated on this loaded host, INDICATIVE]

`resource_ledger.py` → `resource_ledger.json`

**The reference script is about 2.9× wasteful in steps.** `scripts/nmr_cone.py` does 8000 single-vector Trotter
steps: it recomputes the forward evolution for every time and every b. An incremental, window-only exact echo
(`exact_fast.py`, verified identical to the reference) needs 2800 column-steps. My batched kernel ran at 19 ns/update on
this host, against 7–11 ns for `apply_step`. The realised gain was therefore only about 1.1–1.6× per vector (N = 14: 80 s
per vector against 86–132 s). The 2.9× is reached only with the faster per-column kernel.

**The quoted exact cost is inflated.**
- N = 16 (632 s): 10 ns per amplitude-gate update.
- N = 18 (9509 s): 29.6 ns per update, about 3× that, because of governor suspensions and load.
- An efficient exact echo would cost about 0.06 h at N = 16 and about 0.3 h at N = 18 (single thread, 10 ns/update).

**At N = 16 the CQC is more expensive than exact, not "approaching" it.** CQC kls12 at M = 48 does about 25× the
arithmetic of an efficient exact typicality run:
- 5.5e11 dense MACs against 2.2e10 updates;
- it also tracks 3× more amplitudes (48 × 5 × 2^12 against 5 × 2^16).

The wall-clock parity (442 s against 632 s) comes only from dense BLAS being about 12× faster per operation than numpy
strided pair gates. The per-sample SD of the Haar product ensemble (about 0.05 for kls12) forces M ≈ 200 (N = 18, `power_audit.json`) to certify σ even with zero bias.
Exact typicality self-averages as 2^(−N/2).

**At N = 18 the CQC is cheaper, but not accurate enough.** kls12 costs about 0.2–0.4× an efficient exact run but is
6σ off. To reach σ it would need k ≥ 14 (dense-block cost ×15, about 6600 s) or a larger M together with removing the
bias. Either way the cost is ≥ exact. The lane's resource inference holds at N ≤ 18.

**Wording correction.** "Errors do not shrink with polynomial method order" is inaccurate as stated. CQC error falls
monotonically with cluster size k: 0.54 → 0.24 → 0.24 → 0.062 → 0.035. k is the polynomial-in-N order parameter (cost
∝ M·k²·2^k·T + N²). The accurate statement is: *at fixed k ≤ 12 the error does not reach σ, and at fixed k it grows
with N.*

## 5. Break-even for any category-3 (resource) reading: NOT CREDIBLE [DERIVED + INFERENCE]

**Target.** The lane observable, certified: 4 sites × 4 times, σ = 0.01, family-wise 95 %.

**Quantum side, fault-tolerant, optimistic.** Assumptions:
- Pair gate = 3 commuting Pauli rotations.
- Ross–Selinger T-count 1.15·log2(1/ε) + 9.2 (arXiv:1403.2975; LITERATURE-SUPPORTED, not re-read).
- Synthesis budget 0.003.
- Infinite-temperature protocol: random basis state |s⟩, then U, then Z_a, then U†, then measure all qubits in Z.

Two variants:
- **Sampling.** 1.8e5 shots per time point; 2.0e12–3.9e12 T at N = 16–22. That is 23–45 days serial at 1 µs/T, or
  2.8–4.1 days with unlimited factories.
- **Heisenberg-limited amplitude estimation.** 2N logical qubits and coherent depth about 1e9 T-layers, which needs
  logical error below about 1e-11. It takes 2.0 / 2.6 / 2.9 / 3.2 / 3.5 h at N = 16 / 20 / 22 / 24 / 26 with 1 µs per
  T-layer, and 10× that at 10 µs.
- **NISQ.** Circuit fidelity at 320 µs with a 1e-3 two-qubit error is 2e-17 at N = 16 and 8e-33 at N = 22. Impossible.

**Classical exact** (single thread, 10 ns/update; 8 threads assumed 6× faster):

| N | Single thread | Memory |
|---|---|---|
| 16 | 0.06 h | |
| 18 | 0.31 h | |
| 20 | 1.6 h | |
| 22 | 7.5 h | 0.7 GB |
| 24 | 36 h | 2.7 GB |
| 26 | 170 h | |

**Crossover.** The most optimistic quantum variant (amplitude estimation, 1 µs per layer) first beats exact at:
- N ≈ 21–22 against one laptop thread;
- N ≈ 24–26 against 8 threads;
- N ≈ 26–28 at a realistic 10 µs per layer;
- later against GPU or HPC state vectors (N ≈ 30–40; INFERENCE, not measured).

**Convergence.** The reference is converging in N (MEASURED):
- p19: max |F_{N+2} − F_N| = 0.186, 0.139, 0.037.
- p245: 0.120, 0.132, 0.057.

A geometric extrapolation (INFERENCE, 3 points) predicts dF(20→22) ≈ 0.003 (p19) and 0.011 (p245), and dF(22→24) ≈
0.0045 for p245. So the converged echo is expected at N ≈ 22–24. That is at or below the most optimistic crossover, and
it lies inside exact classical reach on this laptop. A quantum resource advantage would require convergence to fail
at N = 20/22 (T-A) *and* persist past N ≈ 28–40.

## 6. Recommendations

- Tag the lane's cost numbers as implementation-bound. Replace "cost approaching exact" with the counts in §4.
- **T-A speed.** The running N = 20 `nmr_cone.py` job has done only k = 0 after 3436 s (about 21 ns/update). That
  projects to about 9.5 h at N = 20 and about 45 h at N = 22. An incremental, window-only exact echo cuts steps by 2.9×
  when it uses the `apply_step` kernel.
  I recommend it for the next T-A rung; I did not touch the running jobs.
- Report lower confidence bounds, and use a multi-vector reference at N ≤ 16.

## Compute ledger (this audit)

All runs were single-threaded (OMP/MKL/OPENBLAS = 1) with peak RAM under 0.3 GB, and all were checkpointed per time point.

| Run | Time |
|---|---|
| exact_fast N = 12 validation | 6 s |
| exact_fast N = 14, 4 vectors | 322 s wall |
| CQC kls12 p19 N = 18 | 413 CPU-s |
| Analysis | about 30 s |
| **Total** | **about 13 CPU-min** |

No quantum resources were used. There is no leakage issue: native coordinates only define the model Hamiltonian.

## Files

- `power_audit.py`, `power_audit.json`: noise floors and lower confidence bounds for all 37 lane runs and the CCE.
- `exact_fast.py`, `out_exact/`: validated efficient exact echo, and the exact-vs-reference floor at N = 14.
- `cqc_run.py`, `out_cqc/1UBQ_p19_N18_kls12_none_M48_s7.json`: the new kls12 point at N = 18.
- `score_new.py`, `score_new.json`: scoring of the new runs.
- `resource_ledger.py`, `resource_ledger.json`: classical, CQC, fault-tolerant, amplitude-estimation and NISQ costs,
  plus the convergence extrapolation.
