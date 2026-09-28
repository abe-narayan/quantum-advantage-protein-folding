# Resource verifier, ROUND4 lane `spindmft`: full accounting, independent exact re-runs, break-even

_2026-09-28. Adversarial verifier (resource lens). Artefacts only in this folder. Tags: MEASURED / DERIVED / INFERENCE /
UNPROVEN. σ = 0.01 throughout._

## Verdict: NOT REFUTED at 40 µs. Two corrections: 80 µs is fully open, and "≤ 0.006" becomes ≤ 0.010

The claim is a classical-reach result with no quantum advantage (L0/L0). Under a resource audit its core stands, and
my new data make the 40 µs part stronger:

1. **The kill rule does not fire, and the validation gate fails** [MEASURED, reproduced].
   - I re-ran the lane's `analyze.py` unchanged, with only the output path redirected. It gives 0 differences from
     `analysis.json`.
   - Numbers reproduced: 0/8, 0/8, 1/8; median 0.053/0.071/0.050; gate 1/8, 0/8, 2/8; flat-X −0.03 ± 0.10 /
     0.56 ± 0.47 / 0.78 ± 0.66; world ladder 23/24, 20/24, 11/20.
2. **The hybrid comparator is wrong at 40 µs** [MEASURED, strengthened].
   - My independent exact b-aware clusters now cover **all 8 series**, not only the lane's 3. On every series they lie
     above F_∞^hyb, by 2.7–9.5σ; 5/8 series exceed 3σ.
   - The probe-family N = 22 points I ran stay flat: p19 b1 gives 0.6029 against F₂₀ = 0.5999, and p19 b7 gives
     0.8731 against 0.8711. The hybrid needs −0.062 on p19.
3. **At 40 µs, two classical families agree within σ on 8/8 series** [MEASURED, replicated and extended].
   - Exact b-aware clusters at N = 18–22 (the largest available per series) agree with the lane's spinDMFT
     thermodynamic-limit values on 8/8 series.
   - The largest gap is 0.0096 and the largest last-step change in N is 0.0011.
4. **Correction A: "80 µs partly open" should read "80 µs open"** [MEASURED].
   - At N = 18–22 the b-aware family disagrees with spinDMFT by more than σ on 8/8 series, by 0.016–0.044.
   - The lane's b-aware plateau at N = 12–16 was pre-asymptotic. p19 b8 drops by 0.033 between N = 16 and 18, at 80 µs.
   - So the README's "b-remote 2/3 within σ at 80 µs" does not survive.
5. **Correction B: "reproduced to ≤ 0.006" holds only at N = 16** [MEASURED].
   - At N = 18–22, p19 b8 converges to 0.9733 (flat to 2e-4 over N = 18–22). spinDMFT's prediction is 0.9829, so the
     gap is 0.0096: still within σ, but at its edge.
6. **Resources** [MEASURED].
   - Ledger: the lane's output files log 49.7 CPU-min (claimed 48.9 + 1.4). The largest run is 557.6 s = 9.29 min,
     matching the claim.
   - "Peak RSS < 0.3 GB" is **UNVERIFIED**: no RSS was recorded in any lane file. It is plausible, since my exact runs
     at N ≤ 20 peak at 0.215 GB.
   - "Seconds to minutes" is correct:
     - σ-level classical reach at 40 µs for all 8 series costs **2.7 CPU-min** (exact b-aware N = 18 only);
     - it costs **19 CPU-min** with N = 20 plus the full spinDMFT pipeline;
     - both are single-core.
7. **Break-even: none credible at 40 µs** [DERIVED, using the ROUND3 quantum model at its most favourable].
   - A fault-tolerant machine needs 2.8 h (30 Hz cut) to 10 h (dense) per probe on 629 logical qubits, at a 1 µs T
     layer with unlimited factories. That is 17–65× the single-core classical cost for the same 8 series.
   - Even a 20-qubit cluster-only circuit is 1.5× slower.
   - NISQ is excluded: ln F = −23 at N = 20 and −6680 at N = 629.
   - This matches the claim's L0/L0 and its statement that no advantage is claimed.

## 1. What was checked and how

| Item | How | Result |
|---|---|---|
| Lane analysis | `ledger_and_reanalysis.py`: executes the lane's `analyze.py` source unchanged, output redirected to `reanalysis_analysis.json`, deep diff against `analysis.json` | **0 differences** |
| Compute ledger | sums `cpu`/`cpu_s` over `out/*.json` (finished runs, plus the stopped p245 n_c = 12 checkpoint) and `test_sdmft.json` | 49.66 CPU-min: emb 38.0, exact 6.6, sr 4.3, tests 0.7. Largest run `emb_p19_Wprotein_nc12` 557.6 s. The claimed ≈ 7.5 unlogged min (first unoptimised test, lost batches) are not verifiable |
| Kernel and family independence | `pplus_cluster.py`: single-site P₊ sector estimator (ROUND3 `pplus_echo.py`, validated there to 7e-14 against dense unitaries), sector-restricted `fastecho.SectorKernel` complex64, own random vectors; cluster built by the **same** family rule as the lane's `exact_pairb.py` (`C_world` identical, checked) | independent of the lane's full-space `spins.exact_correlators` path |
| Probe-family path validation | N = 18 p19 b1 and b8 against the reference cone F₁₈ | 0.6012/0.3783/0.2774 vs 0.6005/0.3750/0.2787; 0.9528/0.8113/0.6509 vs 0.9527/0.8110/0.6513 (≤ 0.003) |
| Lane E-B values at N = 16 | 4 seeds per series | p245 b7 0.7617/0.4839/0.3474 vs lane 0.7637/0.4892/0.3451; p19 b8 0.9778/0.9061/0.8033 vs 0.9776/0.9054/0.8037; p19 b9 0.9472/0.7291/0.5789 vs 0.9480/0.7307/0.5842. Replicated within typicality noise (the seed spread at N = 16 is ≤ 0.009) |
| Failed attempt (kept as a note) | exact-trace mode at N = 12 was too slow on this loaded machine (1.2 s per matrix step). It was killed by its timeout, wrote no output, and cost ≈ 11 CPU-min | not used |

## 2. Exact b-aware clusters to N = 18–22 against spinDMFT, the probe family and the hybrid [MEASURED; `verify_summary.json`]

Fb_N is my exact b-aware cluster ({a, b} ∪ nearest to either). "dmft" is the lane's spinDMFT value: the b-aware
protein prediction for p245 b7, p19 b8 and p19 b9, and F_corr = F₁₈ + bath correction for the rest. Differences use the
largest N available.

| series | t | F₁₈ probe | F₂₂ probe | Fb₁₆ (lane / mine) | Fb₁₈ | Fb₂₀ | Fb₂₂ | dmft | Fb − dmft | Fb − hybrid | Fb − F₁₈ |
|---|---|---|---|---|---|---|---|---|---|---|---|
| p19 b1 | 40 | 0.6005 | 0.6029 | – | 0.6014 | – | – | 0.6044 | −0.003 | +0.063 | +0.001 |
| p19 b7 | 40 | 0.8712 | 0.8731 | – | 0.8752 | – | – | 0.8738 | +0.001 | +0.066 | +0.004 |
| p19 b8 | 40 | 0.9527 | **0.9527** | 0.9776 / 0.9778 | 0.9735 | 0.9733 | 0.9733 | 0.9829 | **−0.0096** | +0.083 | +0.021 |
| p19 b9 | 40 | 0.9538 | – | 0.9480 / 0.9472 | 0.9464 | 0.9467 | – | 0.9527 | −0.006 | +0.055 | −0.007 |
| p245 b1 | 40 | 0.9790 | – | – | 0.9777 | 0.9781 | – | 0.9794 | −0.001 | +0.030 | −0.001 |
| p245 b7 | 40 | 0.6988 | – | 0.7637 / 0.7617 | 0.7624 | 0.7635 | – | 0.7638 | −0.000 | +0.096 | +0.065 |
| p245 b8 | 40 | 0.9551 | – | – | 0.9535 | 0.9534 | – | 0.9562 | −0.003 | +0.029 | −0.002 |
| p245 b9 | 40 | 0.9746 | – | – | 0.9714 | – | – | 0.9714 | −0.000 | +0.028 | −0.003 |
| p19 b1 | 80 | 0.3750 | – | – | 0.3803 | – | – | 0.3363 | **+0.044** | +0.078 | +0.005 |
| p19 b7 | 80 | 0.5227 | – | – | 0.5400 | – | – | 0.5120 | +0.028 | +0.090 | +0.017 |
| p19 b8 | 80 | 0.8110 | – | 0.9054 / 0.9061 | **0.8731** | 0.8730 | 0.8716 | 0.9070 | **−0.035** | +0.133 | +0.061 |
| p19 b9 | 80 | 0.7608 | – | 0.7307 / 0.7291 | 0.7137 | 0.7144 | – | 0.7489 | −0.035 | +0.026 | −0.046 |
| p245 b1 | 80 | 0.7627 | – | – | 0.7615 | 0.7700 | – | 0.7902 | −0.020 | +0.051 | +0.007 |
| p245 b7 | 80 | 0.4206 | – | 0.4892 / 0.4838 | 0.4781 | 0.4762 | – | 0.4955 | −0.019 | +0.100 | +0.056 |
| p245 b8 | 80 | 0.7737 | – | – | 0.7441 | 0.7409 | – | 0.7791 | −0.038 | +0.011 | −0.033 |
| p245 b9 | 80 | 0.9374 | – | – | 0.8998 | – | – | 0.9158 | −0.016 | +0.007 | −0.038 |

At 120 µs only 1/8 series is within σ. Fb − dmft spans −0.042 to +0.087, and the drop from N = 16 to 18 reaches
0.071 on p19 b8 (`verify_summary.json`).

**Counts** (Fb at its largest N vs the spinDMFT value; hybrid excess over 3σ):

| t (µs) | within σ | largest \|Fb − dmft\| | largest last-step \|ΔFb\| | hybrid > 3σ below Fb | range of (Fb − hybrid)/σ |
|---|---|---|---|---|---|
| 40 | **8/8** | 0.0096 | 0.0011 | 5/8 | 2.7 to 9.5 |
| 80 | **0/8** | 0.044 | 0.0085 | 5/8 | 0.7 to 13.3 |
| 120 | 1/8 | 0.087 | 0.0064 | 6/8 | −1.8 to 16.3 |

**What this establishes.**
1. **40 µs** [MEASURED agreement; that the common value equals F_∞ is INFERENCE].
   - A second exact family, independent in kernel, vectors and cluster, agrees with spinDMFT on all 8 series.
   - The 5 "probe-local" series no longer depend only on probe-family flatness. That matters because p245 site 1
     keeps only 44% of its M2 inside the probe cluster (N = 18). The lane classed it as probe-local.
2. **Flatness in N is not convergence** [MEASURED].
   - The probe family at p19 b8 is flat at 0.9527 for N = 18, 20 and 22, while the b-aware family is flat at 0.9733.
     The two plateaus sit 2σ apart.
   - So the lane's argument for the probe-local series ("F₁₈ ≈ F₂₀") was insufficient on its own. The b-aware runs
     above close that gap at 40 µs.
3. **80 µs is open** [MEASURED].
   - The b-aware plateaus at N = 12–16 hid a shell event at N = 18 (−0.033 on p19 b8).
   - At N = 18–22 no series has two classical estimators agreeing within σ.
   - The b-aware and probe families differ by up to 0.061, and spinDMFT differs from both by 0.016–0.044.
4. **Lever arm of the flat-X test** [MEASURED; `ledger_reanalysis.json`].
   - At 40 µs the regressor's change over N = 14 → 20 is almost entirely floor. For p19, dH = +0.0005 and
     dfloor = −0.0104; for p245, +0.0021 and −0.0115.
   - So −0.03 ± 0.10 refutes the hybrid's floor subtraction. It does not test the hybrid's H_∞ − H₂₀ term, which is
     −0.027 on p19.
   - The p19 N = 22 probe points (b1 +0.003, b7 +0.002) and the b-aware agreement are the evidence that F does not
     follow that drop either. This is a partial test: H₂₂ was not computed.

## 3. Resource ledger and break-even (`breakeven_40us.py` → `breakeven_40us.json`)

**Classical side, single core, MEASURED on this loaded machine (CPU 55–70% from other jobs):**

| Method | CPU time | Peak RSS |
|---|---|---|
| Exact b-aware, one series, t = 40/80/120 µs | 5 s (N = 16), 20 s (N = 18), 88 s (N = 20) | 0.05 / 0.08 / 0.22 GB |
| Exact at N = 22 | 275–364 s for one time; 675 s for two times | 0.84 GB |
| spinDMFT (lane) | 67 s for the protein bath; 49 s for the two W₁₈ baths; 319 s for the embedded protein + W₁₈ runs of both probes | not recorded |

σ-level 40 µs values for all 8 series:
- **160 s** with exact b-aware N = 18 only;
- **1141 s ≈ 19 min** with b-aware N = 20 × 8 plus the full spinDMFT pipeline.

**Quantum side** [DERIVED]. This re-uses the ROUND3 `resource_audit.py` model for **one** echo time. The circuit is:
- random basis input → U(t) → Z_a → U(t)† → measure;
- reference first-order Trotter at dt = 2 µs;
- 1e4 shots with 4 sites read per shot;
- 3 rotations per pair gate at 1.15 log₂(1/ε) + 9.2 T each, ε_tot = 1e-3;
- depth-limited timing on one QPU with unlimited factories. This is the case most favourable to quantum.

| N (qubits) | pair gates per step | T per probe | wall per probe at a 1 / 10 µs T layer | NISQ ln F (1e-3 per CNOT) |
|---|---|---|---|---|
| 20 (cluster only) | 190 | 8.5e9 | 14 min / 2.4 h | −23 |
| 629, 30 Hz cut (truncation error unaudited) | 55 666 | 3.1e12 | 2.8 h / 28 h | −6 680 |
| 629, dense | 197 506 | 1.2e13 | 10 h / 4.3 d | −23 701 |
| 629, 30 Hz cut, dt = 0.5 µs (Trotter accuracy) | 55 666 | 1.3e13 | 11.6 h / 4.9 d | −26 720 |

**Ratios for 2 probes (quantum wall at a 1 µs T layer ÷ classical single-core CPU) at 40 µs:**
- 629 qubits, 30 Hz cut: 17.5× against the 19-min pipeline and 124× against exact-only N = 18;
- 629 qubits, dense: 65×;
- 20-qubit cluster circuit: 1.5×.

With 8 classical cores these ratios grow by another factor of about 8. **There is no credible break-even at 40 µs**
[DERIVED; hardware times are INFERENCE]. At 80–120 µs no σ-level classical estimate exists (§2), so a break-even is
undefined there. The quantum cost is 2× and 3× the 40 µs figures. This is not a claim of any quantum advantage
category; it only records that the window remains open.

## 4. Claim levels

- **Theoretical: L0.** No separation is claimed or implied. Every method used is classical, either polynomial or exact
  on ≤ 22 spins.
- **Practical: L0.** The only window with σ-level classical reach (40 µs) costs minutes on one core. A fault-tolerant
  QPU is slower even under its most favourable assumptions.
- **Claim category:** none of 1–6.
- K-105 is untouched.

## 5. Consequences (INFERENCE unless tagged)

1. **Keep the lane's 40 µs conclusion. Record it with the stronger evidence:** b-aware exact on 8/8 series at
   N = 18–22, all within σ of spinDMFT.
2. **Change "80 µs partly open" to "80 µs open."** Mark the lane's E-B "80 µs 2/3 within σ" as superseded at
   N ≥ 18 [MEASURED].
3. **A convergence criterion must be cross-family.** "|ΔF| ≤ σ/2 over two N steps" within one family is not enough. The
   probe family passes it at p19 b8 (N = 18–22) yet sits 0.021 from the b-aware plateau [MEASURED]. The lane's next
   test 1 should require agreement of at least two cluster families plus spinDMFT.
4. **Replicate on other targets** (1PGA p390, 1UBQ p487, other orientations) before any state-file KILL at 40 µs, as the
   lane itself says.

## 6. Ledger (this verifier)

| Field | Value |
|---|---|
| Compute | **≈ 52 CPU-min** single-thread (OMP/MKL/OPENBLAS = 1): exact runs 40.1 min (`runs/`), failed exact-trace attempt ≈ 11 min, analysis < 0.5 min. Largest run 675 s (N = 22, per-sector checkpoints, resumed across 4 invocations). Peak RSS 0.84 GB |
| Checkpointing | `pplus_cluster.py` writes JSON after every sector (atomic tmp + replace) and resumes. One Windows `PermissionError` on replace (p19 b9 N16 seed 4244) was resumed cleanly |
| Process note | One N = 22 command was auto-backgrounded by the tool. I waited for it to finish and ran no other compute process at the same time. No other process was touched |
| Side effect outside this folder | Importing the ROUND3 module `pplus_echo.py` (read-only reuse) made Python write its bytecode cache `ROUND3/r1sim_exact_reach/verify_resource/__pycache__/pplus_echo.cpython-313.pyc` (13:00). It is git-ignored and regenerable, and no source or data file outside this folder was modified. The `typicality_cone` changes in `git status` come from other jobs |
| Leakage | None. The native geometry defines the physical instance only |
| Files | `pplus_cluster.py`, `runs/pp_*.json` (35 runs), `summarize_exact.py` → `verify_summary.json`, `ledger_and_reanalysis.py` → `ledger_reanalysis.json` and `reanalysis_analysis.json`, `breakeven_40us.py` → `breakeven_40us.json` |
