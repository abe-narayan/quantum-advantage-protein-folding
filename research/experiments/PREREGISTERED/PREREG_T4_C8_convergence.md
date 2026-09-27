# Pre-registration: T4 check C8, converged relaxation of the G1 mode-census draws

_Written 2026-09-27 before the production C8 runs. **Timing disclosure.** Two things ran before this file was written. (1) A reviewer's scratch check (`conv_check.py`, B = 1, n = 16–24 draws on 5O37A_45, 2AB0A_60 and 2AB0A_100) found that the census's 200-iteration L-BFGS cap binds for 42–88% of restarts. (2) The tracked optimiser was validated on the first 64 of the 256 draws of 5O37A_45: its 200-iteration snapshot reproduces `energy.relax` exactly (max |ΔE| = 0), 47% of restarts are capped at 200 iterations, and all converge within 706. The thresholds below are fixed now and are not changed after seeing production output._

**Purpose.** T4 (`research/theory/PROOFS/T4_amplified_mode_finding.md`) takes its hit probabilities, gradient-evaluation counts and mode gaps from the G1 census (`scripts/g1_mode_census.py`). That census stops L-BFGS at 200 iterations. C8 measures what changes when the same optimiser runs to its own stopping rule. This is a classical diagnostic of T4's inputs, not a quantum–classical comparison.

**Instrument.** Ladder crops {2AB0A, 5O37A, 3TE4A, 4LPQA} × L ∈ {30, 45, 60, 80, 100}, plus 5O37A_120. The census's own draws: R = 256, seed 0, `hrex.ExactPrior` at T = 1, chunks of 64. `T4_amplified_checks.lbfgs_tracked` has the same code path as `energy.lbfgs` (m = 8, ≤ 12 Armijo trials, tol = 10⁻⁶ relative decrease) with the cap raised to 5,000 iterations and per-restart counters. DEP only: the native coordinates in the npz are never read.

**Comparator.** The 200-iteration census map on identical draws, i.e. the snapshot after 200 iterations of the same run.

**Metrics.**
- The fraction of restarts still active after 200 iterations (capped@200) and after 5,000 iterations (capped@5000).
- Energy+gradient evaluations per restart to stop: mean, q90 and maximum.
- The median extra energy drop of the capped restarts.
- The energy-level mass p_E(Δ) = P[E(Φ(x₀)) ≤ min E + Δ] for Δ ∈ {0.1, 1, 5, 20} nats, under both maps.
- The 2 Å RMSD-cluster mass of the lowest cluster, under both maps.
- The gap between the best and second cluster.

**Hypotheses.**
- H-C8a: the median capped@200 is ≥ 0.25 at every L ≥ 60.
- H-C8b: the median q90 of evaluations per restart under convergence is > 400 at L ≥ 60.
- H-C8c: p_E(1 nat) is at the 1/R floor (one restart) in ≥ 50% of crops at every L ≥ 60, under both maps.

**Decision rules (fixed now).**
1. If H-C8a holds at any L, every T4 number taken from the census is relabelled "a property of the 200-iteration truncated map", and T4's extrapolated crossing lengths are withdrawn.
2. The coherent-map budget K_eff in T4 becomes max(400, the median over crops of the q90 evaluation count) at each L. Sensitivity rows use the maximum.
3. If H-C8c holds at an L, T4 reports the instance gate at that L as "censored: p ≲ 1/R, poorly constrained", not as a number.
4. No C8 outcome can reverse T4's hardware-gate KILL. That gate does not depend on p, and C8 can only keep or raise K_eff. If C8 instead showed K_eff < 400, T4 would report it and recompute T* downward. The KILL margin at 1 µs would then be re-examined, not assumed.

**Analysis plan.** `python research/theory/PROOFS/T4_amplified_checks.py` prints C8 per crop and per L (`check_c8_summary`). Raw per-restart energies, iteration counts, evaluation counts and cluster assignments are stored in `research/results/RAW/t4_converge/`.

**Budget.** About 1–2 core-hours in one or two single-thread processes. The machine is shared with a governor-managed queue, whose governor suspends its own youngest job when load exceeds 93%.

## Deviation log

- 2026-09-27 (execution). During the runs the machine was at ~100% CPU from other lanes' jobs. To keep under the 95% ceiling, C8 ran as one single-thread process at a time: a throttle (`research/results/RAW/t4_converge/throttle.jsonl`) paused the second process while load exceeded 94%. After the two L = 100 crops of the second batch finished, the runs were stopped so that T4 v2 rests on a fixed set: 16 of 21 crops (all of 2AB0A and 5O37A at L = 30–100, plus 5O37A_120; 3TE4A at 30, 45 and 100; 4LPQA at 30 and 100). The remaining crops (3TE4A_60, 4LPQA_60, 3TE4A_80, 4LPQA_80, 4LPQA_45) are open (T4 G11), and `--converge` can be rerun on them unchanged.
- 2026-09-27 (analysis; **post hoc, decided after seeing C8 data**). Decision rule 2 sets the slot budget at the q90 of evaluations per restart. At L ≥ 60, however, the restarts that reach the lowest energy level (within 1 nat of the best) need evaluation counts at the 89th–100th percentile of their crop, e.g. 835 of a maximum of 835 at 2AB0A_60 and 871 of 1,015 at 2AB0A_100. A q90 slot budget would therefore truncate exactly the target restarts and change p. T4 reports the pre-registered q90 row (M-CONV), flagged as not solving the task at L ≥ 60. It uses the maximum observed count (M-CONVx) as the task-solving converged map. Both rows are shown.
- 2026-09-27 (reporting wording). Rule 3 says "censored: p ≲ 1/R". A single hit in R draws is not an upper bound on p (Clopper–Pearson 95% interval [1.0×10⁻⁴, 2.2×10⁻²] at R = 256). T4 therefore reports such crops as "single-hit, p̂ = 1/R, poorly constrained". The substance of the rule, that no number is reported for the instance gate, is unchanged.
