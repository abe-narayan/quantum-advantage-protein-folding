# R1 adversarial: independent replication of the NMR echo window

_2026-09-27. Lens: **replicate**. Target: `research/results/RAW/nmr_gate/1UBQ_p19_N10_o0_g0.json`. The target is 1UBQ, probe H/ILE3 (H index 19), N = 10, orientation 0 (b0 = random_b0(1000)), γ = 0, dt = 2 µs, 160 steps, a record every 10 steps._

Tags: **MEASURED** means computed here from the listed scripts. **DERIVED** means arithmetic on measured numbers. **INFERENCE** means reasoning, not tested.

## Verdict: WEAKENS

- **The stored numbers are right.** They replicate to machine precision with a code base written independently of `src/qapf/nmr/spins.py`.
- **The N = 10 "echo window" is a property of where the adversary panel stopped (ε ≥ 1e-4). It is not a failure of classical computation, nor even of sparse Pauli dynamics.**
  - One more ladder rung (ε = 3e-5, the C2 ladder's own last rung) reproduces the echo within σ over the full window for this job.
  - The same holds for 3 of 4 further jobs tested. The median f_hard^OTOC over the 17 parameters tested falls from 0.95 to 0.00.
- Claim wording in D4, T6 and CURRENT_STATE ("every classical adversary / approximation tested fails") is contradicted by the repo's own C2 data.

## 1. What was built (independent of the original correlator code)

`repl_lib.py`. Only `read_h_coords` and `cluster` are imported, for geometry. `couplings()` is re-derived and agrees with the original to a relative 1e-16.

- **Dense engine.**
  - Each pair propagator is `scipy.linalg.expm(-i dt (d/4)(2ZZ-XX-YY))` on 4×4, embedded into 2^N by bit manipulation (qubit q = bit q).
  - U_step = g_M … g_1 with the pairs in lexicographic order, and Z_a(t) = W†Z_aW with W = U_step^n.
  - S = Tr[Z_a(t)Z_b]/2^N and F = Tr[(Z_a(t)Z_b)²]/2^N.
  - The embedding was checked against a full Kronecker-product expm to 1.4e-17.
- **PTM engine (sparse Pauli dynamics).**
  - Each pair gate acts as its exact 16×16 Pauli transfer matrix on a coefficient array over all 4^N strings (dense storage, 8 MB at N = 10).
  - Pairs are applied to the operator in reverse order within each step.
  - Truncation zeroes |c| ≤ ε after every pair gate (or, as a variant, after every step).
  - S = c(Z_b), and F = Σ c_P² s_P, with s_P = −1 iff P has X or Y on b.
- **Engine cross-checks (MEASURED).**
  - With no truncation, PTM matches dense to 1.8e-15 at N = 6 and to 2.7e-14 at N = 10 (60 steps).
  - Unitarity error is 2e-15.

## 2. Replication of the stored file (MEASURED; `exact_trotter.json`, `pauli_eps0.0001_pair.json`)

| quantity | max abs deviation, mine vs stored |
|---|---|
| S_exact (4 observed spins × 17 times) | 8.1e-15 |
| F_exact | 4.2e-14 |
| FI_t (each of 3 radial params) | ≤ 6.5e-11 (≤ 4e-12 relative to peak) |
| FI_otoc_t | ≤ 1.9e-9 (≤ 1.6e-11 relative to peak) |
| dS/dφ, dF/dφ | ≤ 7.4e-13 |
| FI_total / FI_otoc_total | 476.515 / 7992.123 (HA/GLU16), 62.570 / 9144.002 (HG22/ILE3), 65.210 / 656.491 (HG3/GLN2); agree to ≥ 11 digits |
| sparse ε = 1e-4: n_strings at all 17 records | identical (max diff 0; 1 → 165,537) |
| sparse ε = 1e-4: kept norm², bias(S), bias(F) | 9e-14, 1e-14, 9e-14 |
| t_c (transfer) / t_c (echo) at ε = 1e-4 | 17 / 4 (stored 17 / 4) |
| frac_hard echo at t_c = 4 | 0.922 / 0.973 / 0.851 (stored identical) |

**Robustness checks (MEASURED).**
- Finite-difference step h = 0.02 vs 0.05 Å changes FI_total by ≤ 0.5% and FI_otoc_total by ≤ 2%.
- Trotter circuit vs continuous-time exp(−iHt) (`exact_continuous.json`):
  - max |ΔS| = 0.003 and max |ΔF| = 0.013 (1.3 σ at one early point, spin HG3/GLN2, 40–60 µs);
  - FI totals change by ≤ 4%;
  - the late-window (index ≥ 4) echo-FI fraction is unchanged (0.919 vs 0.922).
- Conclusion: the stored instrument is numerically sound.

## 3. Findings that matter

**F1. The stored rigid parameter is a duplicate (MEASURED, provenance).**
- The file was written by `nmr_gate.py` at git 92bb4eb. That version picked the farthest proton of a different residue, which gave rigid_res16. Only one proton of residue 16 is in the cluster, so the parameter is identical to radial_HA/GLU16 (dS and dF equal to 1e-13).
- The same duplicate is in `1UBQ_p19_N10_o1_g0.json`.
- `analyze_nmr2.py::unique_params` removes it, so the processed statistics are not double-counted. Anything that counts the raw `params` lists (e.g. "4 parameters", CLAIM_AUDIT tallies) overstates the parameter count.
- The later fix (≥ 2 cluster protons) is **not recorded in the PREREG deviation log**; only the v1 geminal fix is.
- The current rule gives rigid_res2. That parameter moves HA/GLN2, the probe's *nearest* proton (2.16 Å), so its FI (9,583 transfer / 52,655 echo) is dominated by short-range coupling, not "long-range geometry". Its echo f_hard is 0.71 at t_c = 4.

**F2. The N = 10 echo window closes at the next ε rung (MEASURED).**
- With my PTM engine at ε = 3e-5 (per-pair truncation), the echo stays within σ at all 17 times for this job: max bias 0.0075. So t_c = none, f_hard = 0 and gain = 1 for every parameter.
- It uses ≤ 256,425 strings, which match the stored C2 run string for string (max diff 0, F to 5e-14).
- The repo's own C2 file shows the same for probe 245 at N = 10 (240,390 strings).
- Norm-correction does not help: it fails earlier (index 3 at 1e-4, index 7 at 3e-5).

**F3. Other N = 10 jobs (MEASURED; `other_*_eps3e-05.json`, run against each job's stored exact F and stored FI).**

| job | stored t_c echo (panel ε ≥ 1e-4) | t_c echo at ε = 3e-5 | f_hard, stored panel → ε = 3e-5 |
|---|---|---|---|
| 1UBQ p19 o0 (target) | 4 | none (17/17) | 0.85–0.97 → **0** |
| 1PGA p390 | 4 | none (17/17) | 0.90–0.98 → **0** |
| 1PGAHN p260 | 4 | none (21/21) | 0.95–1.00 → **0** |
| 1PGA p325 | 4 | 5 (bias 0.022) | 0.55–0.87 → 0.38–0.67 |
| 1UBQHN p548 | 5 | 7 (bias 0.013) | 0.98–0.99 → 0.81–0.98 |

- Median f_hard^OTOC over these 17 parameters: 0.95 → **0.00**. Ten of the 17 close completely.
- That is below the C3 kill threshold (median < 0.3 at N = 10). The subset is **not representative**, though: I chose the jobs, and 6 jobs (15 parameters) are untested. So C3-kill-1 is *indicated, not established*.

**F4. The C2 string metric is saturated at N ≤ 10 (DERIVED from stored C2 RAW + my ε = 0 run).**
- The exact operator Z_a(t) populates exactly 4^N/2 strings (all strings with an even number of X/Y factors, fixed by parity symmetry): 524,288 at N = 10.
- The strings needed to keep the echo within σ (ε = 3e-5) are 0.498 × 4^N/2 (N = 8) and 0.490 × 4^N/2 (N = 10) for probe 19, and 0.499 and 0.459 for probe 245.
- So "16k → 257k" is exactly the growth of the operator space itself (×16 per 2 spins). Sparse Pauli dynamics has **no compression left** for the echo.
- INFERENCE:
  - The pre-registered C2/C3 test (ΔBIC exp vs power law; M*(60) vs 1e9) will favour "exponential" trivially in this regime. It says nothing about the cheapest exact classical method, whose cost scales as 2^N (statevector / typicality) or C(N, N/2)³ (sector-exact), not 4^N.
  - Measured here: dense exact N = 10, all 17 times, S and F for 4 spins, takes **12.5 CPU-s** per geometry.
  - Treating C2 survival as evidence of classical hardness would be a category error.

**F5. f_hard depends on the adversary's implementation details (MEASURED).**
- At the same ε = 1e-4, truncating after each Trotter step instead of each pair gate moves the echo t_c from 4 to 5 (80 → 100 µs).
- That changes f_hard from 0.92 / 0.97 / 0.85 / 0.71 to 0.75 / 0.93 / 0.84 / 0.61.
- With 20 µs records, one bin moves f_hard by up to 0.17. The statistic should be reported as a range over reasonable adversary variants.

**F6. The summary ranges in T6 and CLAIM_AUDIT D4 are slightly off (MEASURED over the stored RAW).**
- Per-parameter echo/transfer FI ratios span 3.2–183× (1PGA p325: 3.2–8.2; 1PGAHN p390: 183), not "10–160×". R1_value_breakeven flagged this too.
- f_hard^OTOC (stored panel) spans 0.49–1.00 (1UBQHN p19: 0.49, 0.50), not "0.55–1.0".

## 4. Consequences for the claims

- **D4 and CURRENT_STATE** say "every classical adversary (…sparse ε…) fails by 80 µs" and "past the failure time of every classical approximation tested".
  - This is false for the dense 1UBQ p19 / p245 and 1PGA p390 clusters, and for 1PGAHN p260, at ε = 3e-5 (MEASURED).
  - It should read: "fails for ε ≥ 1e-4, w ≤ 5, n_c ≤ N − 2; at ε = 3e-5 (≈ half the parity-allowed Pauli space) the echo is reproduced for 4 of 6 tested N = 10 jobs".
- At N = 10 the relevant statement is not "classical failure". It is "no compression". The echo operator fills about half of the symmetry-allowed Pauli space by 60–100 µs. That is consistent with T6's "the echo is global" argument, and it is a precondition for hardness, not evidence of it (INFERENCE).
- Nothing here bears on N ≥ 12. The decisive question stays open: does N_cone at the informative times exceed exact classical reach (≈ 40–50 spins), with the information surviving embedding? C2 must be reanalysed against the exact-method cost (F4).

## 5. Reproduce

All runs are single-threaded: `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python <script>` from this folder.

| step | command | CPU |
|---|---|---|
| self-tests + timing | `python selftest.py` | 25 s |
| exact dynamics + FI (h = 0.05, 0.02) + stored comparison | `python run_exact.py --mode trotter` | 217 s |
| continuous-time comparison | `python run_exact.py --mode continuous --hlist 0.05` | 110 s |
| sparse Pauli, ε = 1e-4 (replicates the stored adversary) | `python run_pauli.py --eps 1e-4 --trunc pair` | 158 s |
| sparse Pauli, ε = 3e-5 | `python run_pauli.py --eps 3e-5 --trunc pair` | 165 s |
| engine cross-check at N = 10 | `python run_pauli.py --eps 0 --trunc pair --max-steps 60` | 35 s |
| truncation-granularity variant | `python run_pauli.py --eps 1e-4 --trunc step --max-steps 60` | 40 s |
| other jobs at ε = 3e-5 | `python run_other_jobs.py 1PGA_p325_N10_o0_g0 1PGA_p390_N10_o0_g0` then `... 1PGAHN_p260_N10_o0_g0 1UBQHN_p548_N10_o0_g0` | 174 + 181 + 240 + 253 s |
| collect | `python summarize.py` → `summary.json` | < 1 s |

Total ≈ 26.4 CPU-min (single-threaded, peak RSS < 0.3 GB). The last extension run started while the system CPU was at about 95% (shared machine, governor running).

### Recommended governed jobs (not run: budget)

1. Complete F3. Each command is ~8 CPU-min:
   - `python research/experiments/ADVERSARIAL/R1_replicate/run_other_jobs.py 1UBQ_p19_N10_o1_g0 1PGAHN_p325_N10_o0_g0`
   - `... 1PGAHN_p390_N10_o0_g0 1UBQHN_p19_N10_o0_g0`
   - `... 1UBQHN_p359_N10_o0_g0 1UBQHN_p487_N10_o0_g0`

   Then run `--eps=1e-5` on every job that still fails at 3e-5 (1PGA_p325, 1UBQHN_p548, plus any new ones).

   **Kill:** C3-kill-1 fires if the median f_hard^OTOC over all N = 10 γ = 0 unique parameters at the best of {ε ≤ 3e-5} is < 0.3.
2. Reanalyse C2/C3 with the saturation ratio M*/(4^N/2) and the measured CPU cost of sector-exact vs N (N = 8–16).
   **Kill** the "classical cost explodes" reading if the saturation ratio ≥ 0.3 at every N while exact cost stays below the C2 budget. In that case the Pauli metric is uninformative, and the relevant hardness scale is N_cone vs the ≈ 40–50-spin exact frontier.
