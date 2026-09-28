# ROUND3 lane: dq_echo_envelope (R1-DQ inside the physical reversal envelope)

_2026-09-28. Tests the last untested residue of the killed R1 lead (K-105): the double-quantum (DQ) echo. It is phase-reversible, and the R1_amplify lens measured 1.8–4× more echo FI for it. The question is whether a DQ (or other reversible) echo carries classically-hard structural information **inside its own reversal envelope**, with a joint gain ≥ 2 over the classically usable data._

**Tags:** MEASURED (computed here; file named), DERIVED (algebra, checked), LIT (full text read this session via arXiv), LIT-abs (abstract only), INFERENCE, UNPROVEN.

## Verdict: KILLS R1-DQ at N = 10

1. **The DQ window is not classically hard against the strongest twin.**
   - Against the pre-registered ε = 3×10⁻⁵ sparse-Pauli twin, the DQ echo is reproduced to within σ up to 220 µs (1UBQ p19, censored), 200 µs (1UBQ p245) and 140 µs (1PGA p390). The failures that do occur are marginal (1.07–1.14 σ).
   - The only probe where any metric reached 2 is 1PGA p390. There, ε = 10⁻⁵ reproduces the DQ echo to 250 µs, with a maximum bias of 0.15 σ (MEASURED).
2. **The joint gain over classically usable data stays below 2 inside every literature-anchored envelope.**
   - Median per-parameter g against the ε = 3×10⁻⁵ twin: ≤ 1.16 in all 3 probes × 3 T2 choices. With the physical rotor-averaged T2 it is 1.00 / 1.00 / 1.04 (MEASURED + LIT anchor).
   - Even with *perfect* reversal the median is 1.02 / 1.27 / 1.42 against ε = 3×10⁻⁵ and 1.07 against ε = 10⁻⁵ (p390) (MEASURED).
3. **Result of the pre-registered kill tests** (R1_SYNTHESIS §4 item 4, adapted to this lane):

   | Kill test | Fired? | Detail |
   |---|---|---|
   | "DQ hard FI inside the envelope ≤ secular" | **No** | At a matched ε = 10⁻⁴ adversary, DQ inside its literature envelope carries 13–47× more hard FI than secular inside its own. DQ really is more informative and more reversible. |
   | "Sparse Pauli reproduces the DQ echo to σ over the window" | **Yes** | At ε = 3×10⁻⁵ on 2/3 probes over the whole envelope; at ε = 10⁻⁵ on the third. |
   | Value criterion (joint g ≥ 2) | **Yes** | g < 2 in all cases (item 2). |

## What was computed

All runs were single-threaded, with ≤ 0.6 GB RAM and 28.4 CPU-min in total. Everything checkpoints to `out/`.

| Step | Script | Output | CPU |
|---|---|---|---|
| Exact S, F1 and FD Jacobians for the secular (0–320 µs) and **physical** DQ (0–300 µs) Hamiltonians. Same N = 10 clusters, butterflies, params, h = 0.05 Å, σ = 0.01 and dt = 2 µs Trotter circuit as C1/R1_amplify; 10 µs grid. | `run_fi.py` | `out/fi_<pdb>_p<probe>.json` | 3 × 80 s |
| Sparse-Pauli adversary on the DQ echo: ε = 10⁻⁴, 3×10⁻⁵ (3 probes), 10⁻⁵ (p390). Plain and norm-corrected estimators; failure only if both exceed σ. | `run_adv.py` + `dq_lib.pauli_adversary` | `out/adv_*_dq_eps*.json/.npz` | 1102 s |
| Operator size K(t) (mean Pauli weight of Z_a(t)) in N = 30 protein clusters, both Hamiltonians (1UBQ p19, 1PGA p390). | `run_kgrowth.py` | `out/kgrowth_*_N30.json` | 355 s |
| Envelope re-weighting, hard-window FI, joint gains, break-even T3/T2, K(t)-dependent model | `analyze.py` | `analysis.json` | 3 s |

**Validation (MEASURED).** The same engine run at the R1_amplify norm-matched scaling (s = √3) reproduces the stored `R1_amplify/out/obs_1UBQ_p19_N10_o0_dq_fine.json` S and F1 exactly (max |Δ| = 0.0). T2 values reproduce `R1_physics_feasibility/scales.json` (1UBQ p19: 14.05 / 8.04 / 9.77 µs; 1PGA p390: 15.92 / 8.73 / 10.73 µs).

### Physical DQ scaling (DERIVED + LIT)

The 8-pulse DQ average Hamiltonian is H_DQ = −Σ d_ij (IxIx − IyIy), with the same d_ij as the secular H = Σ d_ij (2IzIz − IxIx − IyIy). This is Eq. (2) of Domínguez et al. PRA 104, 012402 (2021) and Eq. (3) of Álvarez & Suter PRA 84, 012320 (2011) (LIT).

Consequences:
- **Pauli coefficient:** d/4, which is 1/√3 of the norm-matched s = √3 form used by R1_amplify. R1_amplify's DQ time t_m therefore equals physical time √3·t_m.
- **Local second moment of Z_a:** equal for the two Hamiltonians, (1/2)Σ_j d_aj² (DERIVED).
- **Global second moment:** the DQ M2 on I_z is (4/9) × the secular FID M2 (T2^DQ,global = 1.5 T2) (DERIVED).

Physical-time comparisons in this lane need no extra clock factor.

## Results

### 1. DQ vs secular information and adversary failure (MEASURED)

| Probe | DQ/secular total echo FI | DQ t₅₀ | DQ fails at ε = 10⁻⁴ | ε = 3×10⁻⁵ | ε = 10⁻⁵ | Secular fails (ε = 10⁻⁴ / 3×10⁻⁵) |
|---|---|---|---|---|---|---|
| 1UBQ p19 | 1.40 | 90 µs (9.2 T2_rot) | 80 µs (8.2 T2_rot) | none to 220 µs (bias 0.96σ) | — | 80 µs / never to 320 µs |
| 1UBQ p245 | 1.41 | 90 µs (9.2 T2_rot) | 100 µs (10.2) | 210 µs (21.5; 1.14σ) | — | 80 µs / never |
| 1PGA p390 | 2.24 | 150 µs (14.0) | 90 µs (8.4) | 150 µs (14.0; 1.07σ) | none to 250 µs (0.15σ) | 80 µs / never |

- **In physical time, DQ fails no earlier than secular** under the same twin: 80–100 µs vs 80 µs at ε = 10⁻⁴.
- **The adversary is not a compression.** The ε = 10⁻⁵ twin that closes p390 holds 260k strings, which is half of the 4¹⁰/2 = 524k parity-even operator space and the same size as the exact parity-block operator.
- **So "hardness" at N = 10 is only a proxy.** Exact simulation takes about 7 s per geometry. This is the same pattern as for the secular echo in R1.

### 2. Reversal envelopes (literature anchors; T2 = 1/√M2)

| Envelope | Anchor | Status |
|---|---|---|
| Secular/XXZ local polarization echo | Gaussian, T3 = 4 T2 | LIT, Sánchez, Chattah & Pastawski PRA 105, 052232 (2022), arXiv:2112.00607 |
| Secular/XXZ Loschmidt echo | logistic, T3 = 6.7 T2, tail 0.25 T3 | LIT, same paper |
| **DQ Loschmidt echo, adamantane** | Fermi decay, t_c = 545 ± 2 µs, tail 123 ± 2 µs | LIT, Rufeil-Fiori, Sánchez, Oliva, Pastawski & Levstein PRA 79, 032324 (2009), arXiv:0810.1722 |
| DQ tail/T3 cross-check | "λ⁻¹ ≈ 0.23 T3" for a Floquet DQ Hamiltonian in the same crystal | LIT, Sánchez 2022. Consistent with 123/545 = 0.23 |
| **DQ T3 in T2 units** | T3^DQ ≈ **12.5 T2**, using adamantane T2 = 1/(23.0 ms⁻¹) = 43.5 µs | Slope of 1/T2^k vs k in Sánchez 2022 Fig. 5, read at k = 1. **INFERENCE:** k = 1 is the natural dipolar T2. Other adamantane T2 readings (13 kHz FWHM in Domínguez 2021 → 29 µs; 7.9 kHz "average dipolar" in Álvarez & Suter 2011) would give **12.5–19**. The verdict does not depend on this (see break-even below). |
| DQ "local" variant | 7.5 T2 (= 12.5 × 4/6.7, the XXZ local/global ratio transferred) | INFERENCE |

**DQ vs XXZ.** The DQ echo is about 1.9× more reversible than XXZ in T2 units (12.5 vs 6.7). This is consistent with "the signal only fades away after reaching 10⁴ entangled spins … largely exceeds the 10² of the dipolar case" (LIT, Sánchez 2022).

**Envelopes inside the protein** (rotor-averaged network T2 of 9.8–10.7 µs):
- T3^DQ ≈ 122–134 µs, against T3^XXZ ≈ 65–72 µs.
- The DQ hard window at ε = 3×10⁻⁵ begins at 1.1–1.9 T3^DQ, where A² ≈ 0.14 (p390), 1.7×10⁻³ (p245) and 4×10⁻⁴ (p19; censored start).

### 3. Hard-window FI inside the envelope and joint gains (MEASURED model arithmetic)

These use the secular LE 6.7 T2 envelope and the DQ LIT 12.5 T2 envelope, with DQ transfer undamped (generous to quantum). Each cell gives the median per-parameter g / g_max / fraction of ideal DQ hard FI retained. Full grid: `analysis.json` → `jobs.*.decisive`, `cases`.

| Probe | Twin | Ideal reversal | Cluster T2 (most generous) | Rotor-avg T2 (physical) | Network T2 | K-model, near-perfect reversal (K3 = 10⁴) |
|---|---|---|---|---|---|---|
| 1UBQ p19 | 10⁻⁴ | 4.18 / 12.8 / 1 | 2.62 / 4.94 / 0.63 | 1.92 / 3.41 / 0.36 | 1.52 / 2.52 / 0.21 | 3.58 / 7.28 / 0.98 |
| 1UBQ p19 | **3×10⁻⁵** | 1.02 / 1.17 / 1 | 1.00 / 1.01 / 0.02 | 1.00 / 1.00 / 0.00 | 1.00 / 1.00 / 0.00 | 1.03 / 1.28 / 0.93 |
| 1UBQ p245 | 10⁻⁴ | 7.69 / 15.1 / 1 | 1.27 / 1.74 / 0.22 | 1.18 / 1.56 / 0.17 | 1.07 / 1.25 / 0.07 | — |
| 1UBQ p245 | **3×10⁻⁵** | 1.27 / 1.53 / 1 | 1.00 / 1.00 / 0.00 | 1.00 / 1.00 / 0.00 | 1.00 / 1.00 / 0.00 | — |
| 1PGA p390 | 10⁻⁴ | 5.00 / 14.1 / 1 | 2.93 / 6.38 / 0.48 | 1.94 / 3.20 / 0.20 | 1.51 / 2.10 / 0.10 | 4.09 / 12.9 / 0.98 |
| 1PGA p390 | 3×10⁻⁵ | 1.42 / 2.33 / 1 | 1.16 / 1.57 / 0.29 | 1.04 / 1.11 / 0.04 | 1.01 / 1.02 / 0.01 | 1.60 / 2.85 / 0.97 |
| 1PGA p390 | **10⁻⁵** | 1.07 / 1.28 / 1 | 1.00 / 1.01 / 0.03 | 1.00 / 1.00 / 0.00 | 1.00 / 1.00 / 0.00 | 1.09 / 1.38 / 0.95 |

**DQ vs secular hard FI inside each Hamiltonian's own envelope** (matched ε = 10⁻⁴, rotor T2):

| Probe | DQ (LIT anchor) | Secular | DQ with XXZ anchors instead of its literature anchor |
|---|---|---|---|
| p19 | 48,154 | 1,014 | 2,777 |
| p245 | 6,635 | 507 | 95 |
| p390 | 29,764 | 1,047 | 1,157 |

- With its literature anchor, the DQ gets 13–47× more hard FI than secular. With XXZ anchors the comparison is mixed.
- DQ is the better *echo*. It is not a quantum advantage, because the twin that matters (ε ≤ 3×10⁻⁵) closes it.

**Break-even DQ T3/T2** (logistic, tail 0.23) for a joint median g ≥ 2:

| Twin | Required T3/T2 | Where it stands |
|---|---|---|
| ε = 10⁻⁴ | 8.3–24.7 | The literature value (12.5–19) is inside this range, so the verdict would be "SUPPORTS against the weak twin" in the generous T2 accountings. |
| ε = 3×10⁻⁵ | **None on any probe, even at T3/T2 = 1000** | — |
| ε = 3×10⁻⁵, g_max ≥ 2 (best single direction only) | ≥ 16.6 (cluster T2) / 23–57 (physical T2); p245 and p390 only | — |
| ε = 10⁻⁵ | None | — |

### 4. K(t)-dependent decoherence model (Γ = Γ₁ K^α)

**Literature basis (LIT, Domínguez et al. PRA 104, 012402 (2021), full text):**
- DQ Loschmidt-echo fidelity decays at Γ ∝ K^α, with K the number of correlated spins.
- α∞ = 0.96 ± 0.02 under strong H_dd perturbation. α₀ = 0.48 ± 0.03 in the weak-perturbation limit. Critical p_c = 0.026.
- Sample: adamantane, about 5000 spins.
- K grows exponentially at first, then as a power law. Álvarez & Suter 2011 report t^4.3 from about 0.6 to 1.2 ms, with K going from 10³ to 10⁴ (LIT; figure digits partly unreadable).
- Krojanski & Suter PRL 93, 090501 (2004) is **not on arXiv and was not verified**.

**Protein K(t) (MEASURED, N = 30 truncated Pauli; kept norm² ≥ 0.9 until 50–60 µs for secular and 80–100 µs for DQ; exponential extrapolation beyond that is INFERENCE):**

| Hamiltonian | 40 µs | 80 µs | 120 µs | 160 µs |
|---|---|---|---|---|
| DQ, 1UBQ p19 | 2.8 | 5.2 | 8.0 | 12.3 |
| Secular, 1UBQ p19 | 2.9 | 6.9 | 17 | 42 |
| DQ, 1PGA p390 | 2.0 | 4.0 | 5.7 | 8.0 |
| Secular, 1PGA p390 | 2.1 | 4.5 | 9.5 | 20 |

**How the model behaves:**
- At equal physical time K_DQ ≈ K_sec while both are reliable, consistent with equal local second moments.
- So a Γ₁ common to both Hamiltonians would give DQ the **same** envelope as XXZ. Only a Hamiltonian-specific (smaller) Γ₁, as the adamantane data imply, makes DQ more reversible.

**Results:**
- **Calibrated to the T2 anchors** (A(12.5 T2) = ½ for DQ): same conclusion as §3. Against ε = 3×10⁻⁵ on p390, g_med = 1.08–1.11 and g_max = 1.24–1.37. On p19, g_med ≤ 1.00 (`analysis.json` → `kmodel`).
- **Calibrated to a K-horizon** (A = ½ when K reaches 10³ or 10⁴): DQ half-times come out at 570–1200 µs, i.e. essentially no envelope over the window.
  - Even so, against ε = 3×10⁻⁵: g_med = 1.03 (p19) and 1.56–1.63 (p390), with g_max up to 2.9 on p390.
  - Against ε = 10⁻⁵: g_med = 1.09 and g_max = 1.38 (p390).
- The K-horizon calibration is an upper bound (INFERENCE). It is inconsistent with the adamantane DQ Loschmidt echo, which decays at 545 µs ≈ 12.5 T2 while MQC-K already exceeds 10². The Pauli-weight K is much smaller than the MQC-K the literature quotes.

**Mechanism (INFERENCE from MEASURED + LIT).**
- DQ is more reversible than XXZ (≈ 12.5 vs 6.7 T2). It also concentrates more structural FI earlier: 41–77% of DQ echo FI accrues before T3^DQ.
- But its sparse-Pauli failure time moves out with it: the ε = 3×10⁻⁵ failure is at 14 to ≥ 22.5 T2_rot. The information that is inside the envelope is information a classical twin with about half the operator space reproduces.
- The lever that improves reversibility (the DQ phase-reversal structure) does not create a gap between "reversible" and "classically reproducible". It is the same operator-growth coupling found for XXZ (R1_physics_feasibility §Mechanism), shifted by a factor of about 2.

## Claim levels

| Level | Status |
|---|---|
| **Theoretical: L0–L1** | No hardness result for the DQ OTOC(1). At N = 10 the "hard window" is a truncation artefact: ε = 10⁻⁵ (≈ the exact operator space) closes it, and exact simulation takes seconds. Whether the converged DQ σ-cone exceeds exact reach inside T3^DQ (122–134 µs) is untested (R1-SIM-DQ, not a lead). The mean Pauli weight at T3^DQ is only about 6–8 (N = 30, partly extrapolated), but the σ-cone is typically several times the mean weight (secular: 16–20 spins at 40 µs vs mean weight 2.9). UNPROVEN either way. |
| **Practical: L0 (killed)** | Joint gain < 2 against the strongest twin, inside every envelope, and even with ideal reversal. It has not been tested against the nuisance parameters (site offsets, methyl rotation), which R1_physics_feasibility showed cost a further 1.2–50× in FI for the secular echo and which R1_amplify showed are larger for DQ (embedding misfit 2.1σ vs 0.28σ). |
| **Claim category** | None of categories 1–6 is supported. |

## Caveats and flaws found

1. **Methyl-proton radial parameters are non-physical** (R1 flaw 2): radial_HG22/ILE3 on p19 and radial_HG21/THR53 on p390. `g_med_phys` excludes them, and the conclusion is unchanged (for example p19 ideal ε = 10⁻⁴: 2.90 vs 4.18).
2. **Secular ε = 10⁻⁴ failure time.** It is taken at 80 µs from the earlier 20 µs grid, while the true value lies in (60, 80] µs. This slightly under-counts the secular hard FI, which is generous to DQ in the DQ-vs-secular comparison.
3. **p19 at ε = 3×10⁻⁵ was censored at 220 µs** (CPU budget), with max bias 0.96σ. Its hard window is treated as starting at 230 µs, which is generous. At most 4% of the DQ FI lies after 220 µs, and A² there is ≤ 0.04 (cluster T2) and ≤ 4×10⁻⁴ (rotor-averaged T2).
4. **The literature DQ envelope is a global, all-spin echo in a plastic crystal.** A site-resolved (local) DQ echo in a protein has not been measured. The "LOCAL7.5" variant, which assumes a local/global ratio of 0.6 as for XXZ, makes every DQ number worse.
5. **Isolated N = 10 clusters, static geometry, no site offsets** (same model as R1). As in R1, this is generous to the quantum side.

## Reproduce (single-threaded)

```
cd research/experiments/ROUND3/dq_echo_envelope
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python run_fi.py --pdb 1UBQ --probe 19;  python run_fi.py --pdb 1UBQ --probe 245;  python run_fi.py --pdb 1PGA --probe 390   # ~80 s each
for p in "1UBQ 19" "1UBQ 245" "1PGA 390"; do set -- $p; python run_adv.py --pdb $1 --probe $2 --eps 1e-4 --budget 300; done   # ~9 s each
for p in "1UBQ 19" "1UBQ 245" "1PGA 390"; do set -- $p; python run_adv.py --pdb $1 --probe $2 --eps 3e-5 --budget 300; done   # 112-316 s
python run_adv.py --pdb 1PGA --probe 390 --eps 1e-5 --budget 520 --tmax 250                                                    # 529 s
python run_kgrowth.py --pdb 1UBQ --probe 19 --ham dq --N 30 --eps 3e-4 --budget 120      # also --ham sec; 1PGA 390 with --norm-stop 0.8 --budget 90
python analyze.py                                                                        # 3 s -> analysis.json
```

Every adversary run checkpoints after each 10 µs record (JSON plus an NPZ of the operator) and resumes if restarted.

## Next tests (none can revive R1-DQ at N = 10)

1. **R1-SIM-DQ.** Measure the converged σ-cone of the DQ echo inside T3^DQ (≤ 130 µs) at N = 12–18 with the parity engine or typicality.
   - Kill: |F_N − F_{N+2}| < σ for t ≤ T3^DQ at some N ≤ 16. Exact classical simulation of the reversible DQ window then suffices.
2. **Protein DQ Loschmidt echo, measured.** A global DQ Loschmidt echo in microcrystalline GB1 or ubiquitin, recording T3^DQ/T2.
   - Only T3^DQ/T2 ≥ 50 together with a failing converged twin could matter. Even then the ε = 3×10⁻⁵ median gain stayed below 2 at T3/T2 = 1000.
3. **DQ with nuisance profiling.** Profile site offsets, rotor averaging and DQ-sequence scaling error (R1_physics_feasibility tests A/E) before any gain is quoted.

## Literature verified this session

- **Domínguez, Rodríguez, Kaiser, Suter & Álvarez**, PRA 104, 012402 (2021), arXiv:2005.12361 (full text).
- **Álvarez & Suter**, PRA 84, 012320 (2011), arXiv:1103.4546 (full text; figure digits partly unreadable).
- **Rufeil-Fiori et al.**, PRA 79, 032324 (2009), arXiv:0810.1722 (full text; DQ Loschmidt-echo Fermi fit).
- **Sánchez, Chattah & Pastawski**, PRA 105, 052232 (2022), arXiv:2112.00607 (full text; T3 = T2/0.15, the DQ tail 0.23 T3, the 10⁴ vs 10² spins statement, 1/T2 slope of 23.0 ms⁻¹).
- **Cho, Cappellaro, Cory & Ramanathan**, PRB 74, 224434 (2006), arXiv:cond-mat/0608620 (abstract only).
- **Not verified:** Krojanski & Suter PRL 93, 090501 (2004) (not on arXiv); Baum, Munowitz, Garroway & Pines JCP 83, 2015 (1985).
