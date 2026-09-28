# Classical adversarial verification of ROUND4 lane `spindmft`

_2026-09-28. Verifier: classical adversary. Folder: `research/experiments/ROUND4/spindmft/verify_classical/`._

**Tags.** MEASURED (a file in this folder) / DERIVED / INFERENCE / UNPROVEN. σ = 0.01 throughout.

**Claim under test (lane verdict INTERESTING).**
- The pre-registered spinDMFT kill rule does not fire (0/8, 0/8, 1/8), and spinDMFT fails its own validation gate.
- The cause is a wrong comparator (the hybrid F_∞ = H_∞ + X₁₈), not classical out-of-reach:
  - flat-X is refuted, with slope −0.03 ± 0.10;
  - the exact b-aware clusters sit 5.6–9.6σ above the hybrid.
- At 40 µs two classical families agree within σ on 8/8 series.
- 80 µs is "partly open"; 120 µs is open.

**Default rule for this verifier.** The claim counts as refuted if a credible classical route exists for the part it calls open.

## Verdict: NOT REFUTED. The 40 µs core is strengthened; the 80 µs part is more open than claimed.

1. **Reproduced exactly.** Re-running the lane's `analyze.py` on its own files gives byte-identical stdout and JSON (`reanalysis_stdout.txt`, `reanalysis.json`) [MEASURED].
   - This covers every MEASURED number in the claim: the literal rule (0/8, 0/8, 1/8), the validation gate, the world ladder, E-B and the flat-X slope.
2. **Flat-X refutation holds at 40 µs** [MEASURED + DERIVED].
   - Independent recomputation: pooled slope −0.034, bootstrap-over-series SE 0.11 (95% CI −0.24 to +0.20).
   - Direct test: mean dF(N 14→20) = +0.0007 against the hybrid's predicted −0.0097, a difference of +0.0103 ± 0.0017 (z = 6.2).
   - The mechanism checks out algebraically [DERIVED here]. floor = (1/N²) Σ_{j,k} Tr[W_rest Z_j W_rest Z_k]/2^N ≈ (1 − H)/N comes from sites outside the support of W. That is a kinematic site-average, not a contribution to F_ab at early times.
   - No power at 80 or 120 µs (z = 0.34, 0.19).
   - Replication on 1UBQ p487 and 1PGA p390 has low power because H + floor moves by only +0.004 and +0.001 over N = 14→18. On p487 F does not track H + floor (difference −0.0045 ± 0.0008); p390 is uninformative (`flatx_replication.json`).
3. **Independent exact b-aware family** (`fe_pairb.py`; fastecho SectorKernel, different Trotter pair order, different RNG) [MEASURED].
   - At N = 16 it reproduces the lane's `exact_pairb` to ≤ 0.003 on p19 b8/b9. On p245 b7 the gaps are −0.006 / −0.010 / +0.002 at 40 / 80 / 120 µs, within typicality noise.
4. **Extending the b-aware family to N = 18 and 20 exposes a false plateau at 80–120 µs** [MEASURED].

| series | F at 40 µs, N = 16 / 18 / 20 | F at 80 µs | F at 120 µs | lane spinDMFT prediction (40/80/120) |
|---|---|---|---|---|
| p19 b8 | 0.978 / 0.972 / 0.972 | 0.906 / **0.870** / 0.869 | 0.801 / **0.729** / 0.729 | 0.983 / 0.907 / 0.775 |
| p19 b9 | 0.946 / 0.944 / 0.944 | 0.728 / 0.705 / 0.708 | 0.581 / 0.527 / 0.527 | 0.953 / 0.749 / 0.540 |
| p245 b7 | 0.758 / 0.759 / 0.760 | 0.479 / 0.466 / 0.466 | 0.347 / 0.313 / 0.305 | 0.764 / 0.496 / 0.290 |

   - **40 µs:** the family is flat to ≤ 0.006. Exact N = 20 against the lane's spinDMFT prediction gives −0.011 / −0.009 / −0.004, so 2/3 are within σ. The lane reported ≤ 0.006 on 3/3 at N = 16.
   - **80 µs:** the lane's statements "b-aware clusters converged to ±0.006" and "b-remote series agree 2/3" are **refuted**. N = 16 → 18 drops by up to 0.036, and N = 20 against spinDMFT is −0.038 / −0.041 / −0.030 (0/3 within σ).
   - The spinDMFT embedding in the closed b-aware N = 20 world is itself +0.041 off for p19 b8 at 80 µs. So the lane's 80 µs "agreement" at N = 16 was two errors cancelling [INFERENCE].
5. **Bath-model swap (sr-spinDMFT → classical spin dynamics, CSD)** for the lane's probe-family correction ΔW [MEASURED].
   - CSD reproduces the exact G_aa in the closed N = 18 world for p19: 0.601 / 0.373 / 0.264 against 0.600 / 0.366 / 0.265. sr-spinDMFT gives 0.522 / 0.225 / 0.101.
   - ΔW barely moves: max |ΔW_csd − ΔW_sr| = 0.005 (40 µs), 0.013 (80 µs), 0.020 (120 µs).
6. **Second, independent thermodynamic estimator E2** [MEASURED arithmetic; that E1 ≈ E2 ≈ F_∞ is INFERENCE].
   - E2 = exact b-aware F_N (N = 18 for probe-local series, N = 20 for b-remote), plus a CSD-bath correction computed with the b-aware embedded cluster (`emb_bworld.py`).
   - It is compared with the lane's E1 = probe-family F₁₈ + sr-spinDMFT ΔW.
   - E2 differs from E1 in its exact kernel, cluster family, bath model and embedded cluster. It shares only the quenched-bath (A3) OTOC structure and the Trotter circuit.

| t (µs) | E1 vs E2 within σ | max \|E2 − E1\| | exact families (b-aware vs probe) differing by > σ | E2 − hybrid |
|---|---|---|---|---|
| 40 | **8/8** | **0.0045** | 2/8 (the b-remote p19 b8, p245 b7; E2 absorbs both) | +0.026 to +0.094 (8/8 > 2.6σ) |
| 80 | **3/8** | 0.036 (p19 b1); others 0.014–0.022 | 5/8 | +0.006 to +0.124 |
| 120 | 2/8 | 0.063 | 8/8 | −0.020 to +0.170 |

   - n_c-stability of the b-aware correction for p19 b1: n_c 10 → 12 gives ΔW_b = +0.004 → +0.003 / −0.007 → −0.007 / −0.026 → −0.038 [MEASURED].
   - At 80 µs, E1's p19 b1 correction (−0.039 sr, −0.029 CSD) comes from a probe-family embedding whose closed-world absolute error is −0.094 (sr) or −0.098 (CSD). The b-aware embedding's error is only +0.009 to +0.014, and it gives −0.007. The 80 µs corrections are therefore **cluster-choice-dependent**, at the 0.02–0.04 level [MEASURED].

## What this means for the claim

- **The 40 µs claim survives a stronger, largely independent test.**
  - Two thermodynamic estimators agree on 8/8 series to ≤ 0.0045 at 40 µs.
  - Both lie 2.6–9.4σ above the round-3 hybrid.
  - σ-level classical reach of the converged 40 µs echo is **corroborated (INFERENCE)**. It holds for these 2 probes and 1 orientation; replication on p487 and p390 is weak.
- **Corrections to the lane's text.**
  - (a) "80 µs partly open" should read **open**. Its "b-remote agreement 2/3" and "b-aware converged ±0.006 at 80 µs" are N ≤ 16 false plateaus. This is the round-3 step-rule flaw (H-2) again, inside the lane's own E-B test.
  - (b) "reproduced to ≤ 0.006" at 40 µs becomes ≤ 0.011 at N = 20 in absolute terms, with 2/3 within σ. The bath-corrected agreement is ≤ 0.0045.
  - (c) "exact b-aware 5.6–9.6σ above the hybrid" is **not a third independent refutation**. For p19 b9 the family shift is about 0, so its gap is the same floor + H subtraction as flat-X. Only p245 b7 and p19 b8 carry a genuine family effect.
  - (d) CRITIC C1 at 40 µs: the probe-family F₁₈ is within 0.006 of E1/E2 on 6/8 series. On the other 2 it is 1.7–6.5σ **below** F_∞. That is a cluster-family error in the opposite direction to C1's, and b-aware exact clusters remove it.
- **No credible classical route was found for 80–120 µs.** At 80 µs the exact families disagree on 5/8 series and the two thermodynamic estimators on 5/8. The default-refute condition is not met.
- **The INTERESTING-vs-SUPPORTS choice.** The formal SUPPORTS conditions are met, as the lane says. INTERESTING is the accurate label: the disagreement comes from a demonstrated defect in the comparator, and at 40 µs two estimators agree.
- **Levels and category.**
  - Theoretical level L0: no separation; every method used is polynomial or exact on ≤ 20 spins.
  - Practical level L0: no quantum resource costed.
  - No claim category 1–6. K-105 is untouched.

## Files

| file | content |
|---|---|
| `reanalyze_copy.py` → `reanalysis.json`, `reanalysis_stdout.txt` | The lane's analysis, re-run with output redirected here (identical) |
| `fe_pairb.py` → `out/fe_pairb_*.json` (+ per-sector `.ckpt.json`) | Independent exact b-aware echoes, N = 16 (R = 2), 18 and 20 (R = 1, complex64), 8 series; F, H, floor, X |
| `csd_bath.py` → `out/csd_*.json/.npz` (+ `.ckpt.npz`) | CSD bath autocorrelations: protein (M = 1024 × 7 start times) and closed N = 18 worlds |
| `emb_csd.py` → `out/embcsd_*.json` | The lane's embedded cluster (`sdmft.run_embedded`, imported read-only) with the CSD bath, probe family |
| `emb_bworld.py` → `out/embb_*.json`, `out/csdWb_*.npz` | b-aware embedded cluster in the closed b-aware world and in the protein: correction ΔW_b (n_c = 10; n_c = 12 for p19 b1) |
| `replicate_flatx.py` → `flatx_replication.json`, `out/honly_*.json` | Flat-X replication on 1UBQ p487 and 1PGA p390 (reads the finished reference cones) |
| `verify_analysis.py` → `verify_summary.json`, `verify_stdout.txt` | All tables above |

## Ledger

- **Compute.** About 47 CPU-min, single-threaded (OMP/MKL/OPENBLAS = 1): 44.4 min logged in `out/*.json`, plus about 2.5 min for analyses and replication.
  - Largest run: 225 CPU-s (b-aware N = 20).
  - Peak RSS not logged; all runs are ≤ 20 spins, complex64, flip-folded, INFERENCE < 0.5 GB.
- **Checkpoints.** Per sector (exact), per batch (embedded), per sample batch (CSD); all atomic. None deleted.
- **Leakage.** None. Native geometry defines the physical instance only.
- **Replication.** 2 probes and 1 orientation (b0 = random_b0(1000)). Flat-X was replicated weakly on 2 more probes.
- **Housekeeping.** Importing the lane's `analyze.py` created a bytecode file `ROUND4/spindmft/__pycache__/analyze.cpython-313.pyc`. I removed that one file to restore the lane folder. Nothing else outside this folder was written.
