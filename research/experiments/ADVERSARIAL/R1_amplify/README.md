# R1 lens: amplify. What is the strongest honest version of the NMR echo window?

_2026-09-27. Adversarial-amplification pass on the surviving lead R1 (protein ¹H dipolar echo / first-order OTOC window).

The job: find variants that make the classically-hard echo window larger, more robust, more structurally relevant, or harder classically at fixed quantum cost. Then test them against the same adversaries.

Tags: **MEASURED** (computed here, or read from RAW with the file named), **DERIVED** (algebra on measured inputs), **LITERATURE** (abstract verified this session via arXiv), **LIT-UNVERIFIED** (from memory), **INFERENCE**, **UNPROVEN**._

## Verdict: WEAKENS

One tested variant, the second-order OTOC F2, measurably re-opens a window that the strongest pre-registered adversary closes for the standard echo F1. The re-opened window is small.

**What F2 does:**
- Against the sparse-Pauli twin at ε = 3×10⁻⁵ (the bottom of the pre-registered ladder, 256k strings), F1 and transfer S are reproduced within σ over the whole 320 µs window. This was MEASURED by sibling lens `R1_replicate/pauli_eps3e-05_pair.json`: F1 max bias 0.0075.
- **F2 fails at 60 µs** under the same twin (bias 2.05σ at 60 µs, 3.45σ at 80 µs; MEASURED).
- The quantum-only gain from adding late F2 is **g = 1.65× median (max 1.76×)** (DERIVED, `gain_eps3e5.json`).

**Why this does not strengthen the case overall:**
- A still stronger twin, ε = 10⁻⁵, reproduces F2 within 0.44σ to at least 70 µs (MEASURED).
- F2 costs twice the evolution time of F1.
- F2 is more environment-sensitive (MEASURED).
- Every other lever tried is either classically easier or is only a constant-factor or rescaling effect (below).

**The amplification search also weakens the existing evidence.** The headline "every classical adversary fails by 80 µs" depends on adversary strength at N = 10. With ε ≤ 3×10⁻⁵, sparse Pauli dynamics reproduces the F1 echo over the whole window. Such an adversary keeps 153k strings at 80 µs and 256k at its peak. That is comparable to, or larger than, the 184,756 complex numbers the exact charge-conserving block representation needs, so the adversary is no longer a compression. At N = 10, therefore, nothing is hard. Only scaling tests can decide the question (§6).

**Levels:**
- Theoretical: **L1.** Truncated classical approximations fail earlier for F2 by a constant factor. There is no exact-classical separation, and none is testable at N ≤ 12.
- Practical: **L0** (unchanged).

**Nothing tested here creates a capability a classical approach cannot match at the sizes tested.**

## 1. Variants: mechanism, test, result

Canonical job: 1UBQ H/ILE3 (probe 19), N = 10, orientation 0, dense ¹H, dt = 2 µs. The cluster, parameters (3 radial moves + a rigid residue shift), h = 0.05 Å, σ = 0.01, time grid and Trotter circuit are identical to C1 v2. Replication job: 1PGA probe 325. Exact references use total-Z sector (secular) or popcount-parity (DQ) block diagonalisation.

Engines were validated in `selftest.json` (MEASURED):
- exact S and F1 match the C1 RAW to 1×10⁻¹⁶;
- sector and parity engines agree to 7×10⁻¹⁴;
- untruncated Pauli propagation plus the WHT dense reconstruction matches exact values of S, F1, F2, P_δ and MQC to 1×10⁻¹³ (secular and DQ);
- the ε = 10⁻⁴ adversary reproduces the stored C1 RAW OTOC bias bit-for-bit.

| # | Variant (lever) | Mechanism | Test run | Result | Creates something classical cannot match? |
|---|---|---|---|---|---|
| V1 | **Second-order OTOC** F2 = Tr[(Z_a(t) Z_b)⁴]/2^N (levers i, iv) | Quartic in the Heisenberg operator. Discarded Pauli strings interfere with kept ones, so the truncation bias per unit discarded norm is ~10× larger than for F1. This is the large-loop interference argument of Abanin et al., arXiv:2506.10191 (LITERATURE). | Canonical run over 0–320 µs. Fine 10 µs grid over 0–100 µs with ε = 10⁻⁴ and 10⁻⁵. ε = 3×10⁻⁵ over 0–80 µs. 1PGA p325 replication. | See §2. Fails earlier than F1 at ε = 10⁻⁴ (40 vs 80 µs) and at ε = 3×10⁻⁵ (60 µs vs never). Re-opens a window at ε = 3×10⁻⁵ (g = 1.65). At ε = 10⁻⁵ neither fails within 70 µs. | No. The saving is a constant factor in strings, and the exact cost is the same 2^N. |
| V2 | **Multi-site butterflies** F_T = Tr[O Z_T O Z_T], T ⊆ observed set (11 settings), and **subset coherence-order spectrum** MQC_S (phase-multiplexed echo) (lever i) | Tomography of the X/Y occupation pattern on the observed spins | Canonical and fine runs, plus 1PGA | **Classically easier than F1.** F1_multi first fails at 120 µs (F1: 80 µs), frac_hard 0.23 (F1: 0.77), g_med 2.45 (F1: 4.71). MQC_S is never failed within 200 µs (norm-corrected Pauli), carries ~1% of F1's FI per scalar, and gives g = 1.02. MEASURED. | No |
| V3 | **Pulse-engineered double-quantum Hamiltonian** H_DQ = Σ (√3 d/4)(XX − YY), pair norm matched to secular (levers ii, iv) | Exactly reversible by an RF phase shift, the standard MQC-NMR construction (Baum–Pines; LIT-UNVERIFIED). Every term flips the probe, so the probe's local second moment is 3× the secular one at equal pair norm (DERIVED). | 1UBQ and 1PGA, 0–100 µs; ε = 10⁻⁴ and 10⁻⁵; sub-clusters; embedding (N_env = 12) | See §3. More FI per measurement (×2.2–3.1 at matched local-T2 time). **Not** classically harder in local-T2 units. **More** environment-sensitive. Global MQC_tot carries negligible FI (≤ 172 per scalar). | No |
| V4 | **Isotope dilution / labelling** (amide-only, ILV methyl, sparse site labels) (lever iii) | Dipolar coupling ∝ r⁻³ is scale-free, so a network diluted by λ³ is statistically a rescaled dense network: same qubits, gates and hardness per unit dimensionless time; distances ×λ; time ×λ³ (DERIVED). | Collapse check on the C1 RAW (4 dense + 7 amide jobs). R₄₇ (radius holding 47 labelled spins) for each scheme from 1UBQ/1PGA coordinates. | See §4. The hard regime maps to **11–15 Å (amide), 15–18 Å (ILV), ~25 Å (1 label per 10 residues)** instead of ~6 Å (dense). The coherent evolution needed grows ×7.5–8.6 / 19–28 / 84–90. | No. It moves the hard regime to useful long-range distances, but reversal decay tracks the network's own T₂ (LITERATURE), so the dimensionless reversible window does not grow. |
| V5 | **Time-point design / hybrid** (quantum only in the hard window) (lever iv, cost) | Spend quantum evolution time only where hard FI per µs of evolution is largest | Re-analysis (`analysis.json` D) | The best 5 time points carry 63% (F1) / 81% (F2) of hard FI for 23% / 15% of the hard-window evolution cost, i.e. 2.7× / 5.4× FI per quantum-µs. Skipping the easy window saves little, because early points are short. MEASURED/DERIVED. | No (cost constant only) |
| V6 | Scaled flip-flop (secular H with κ ≠ 1) via RF | — | DERIVED, no run | **Not physically available with global pulses.** Global rotations preserve the traceless rank-2 dipolar tensor. The only Z-conserving averages are scalar multiples of 2ZZ − XX − YY: averaging (−1,−1,2) with its permutations under x↔y symmetry gives (3w−1)(−½,−½,1). κ ≠ 1 needs an isotropic component that global RF cannot create. | — |
| V7 | Heteronuclear (¹⁹F/¹³C) probe | Heteronuclear couplings are secular Ising (ZZ), so Z_a of a hetero probe is conserved and the echo is trivial. Transverse probes decohere through spectral diffusion, where cluster-correlation expansion is the known strong classical method (INFERENCE). | not run | — | not expected |
| V8 | Multiple B₀ orientations | Adds FI to the classical and quantum routes alike. No hardness mechanism. | not run | — | not expected (INFERENCE) |

## 2. V1 in detail: the second-order OTOC (all MEASURED unless tagged)

**Failure times** (first recorded time with max_b |bias| > σ = 0.01). The fine grid is 10 µs; 1UBQ p19 unless noted.

| adversary | strings at 70–80 µs | F1 fails at | F2 fails at | transfer S |
|---|---|---|---|---|
| sparse Pauli ε = 10⁻⁴ | 55k (80 µs) | 70–80 µs | **30–40 µs** (bias 0.027 at 40 µs) | never (≤ 0.08σ) |
| sparse Pauli ε = 3×10⁻⁵ | 153k (80 µs) | not within 320 µs (R1_replicate) | **60 µs** (0.0205; 0.0345 at 80 µs) | never |
| sparse Pauli ε = 10⁻⁵ | 219k (70 µs) | not within 70 µs (0.0007) | not within 70 µs (0.0044) | never |
| exact sub-cluster n = 9 | — | 40 µs | 30 µs | 60 µs |
| 1PGA p325, ε = 10⁻⁴ | — | > 60 µs (run capped) | 40 µs | never |

**Bias law.** In log–log fits of bias against lost norm δ = 1 − Σc², the slope is ≈ 1.0 for both F1 and F2 across all three ε and both proteins (fitted slopes 0.96–1.36).
- Prefactors: bias(F1) ≈ (1.3–2.9)·δ and bias(F2) ≈ (15–21)·δ (`analysis.json` B).
- F2 therefore needs about 10× smaller δ than F1 at the same σ. At 80 µs that is about 1.5–2× more strings (DERIVED from 55k/153k/~240k strings versus δ = 1.1×10⁻² / 2.2×10⁻³ / ~3×10⁻⁴).
- The δ-law predicted the ε = 3×10⁻⁵ failure *before* the run: 0.016 / 0.033 predicted, 0.0205 / 0.0345 measured.
- My first hypothesis, bias ∝ √δ (the Hölder bound), is **not** what happens. The bound is loose.

**Information** (canonical, 0–320 µs, 20 µs grid, 4 scalars per family):

| | F1 (ε = 10⁻⁴ twin) | F2 (ε = 10⁻⁴ twin) | F1 + F2 (ε = 10⁻⁴) | F2 added vs ε = 3×10⁻⁵ twin |
|---|---|---|---|---|
| FI per scalar | 17,612 | 9,875 | — | — |
| frac_hard | 0.77 | 0.79 | — | 0.66 (INFERENCE: F2 assumed failed after 80 µs) |
| g_par median (max eigen) | 4.71 (29.6) | 14.1 (107) | 9.8 (51.8) | **1.65 (1.76)** |

**Depth normalisation.** F1 at time t costs 2t of evolution (forward, butterfly, backward). F2 costs 4t: the sequence is U† · Z_b · U · Z_a · U† · Z_b · U applied to ρ ∝ Z_a, then Z_a is read out (DERIVED).
- Against the ε = 10⁻⁴ twin on 1UBQ, F1 gives **more** hard FI than F2 at every total-evolution budget: 160 µs: 7,161 vs 5,163; 320 µs: 33,985 vs 18,957; 640 µs: 54,209 vs 27,105.
- 1PGA (window ≤ 100 µs) favours F2 at budgets of 160–200 µs: 8,460 vs 6,517 and 18,993 vs 10,828.
- Against ε = 3×10⁻⁵, F1 has no hard window at any budget, and F2's starts at a 240 µs budget.

**Embedding (+2 protons, base geometry).** The misfit between the core-10 and embedded-12 signals, in units of σ at 60/80/100 µs:
- F1: 0.28 / 0.64 / 1.0
- **F2: 0.32 / 1.31 / 2.61**
- S: 0.15 / 0.29 / 0.28

F2's extra sensitivity comes with a larger dependence on unmodelled protons (MEASURED, `embed_check.json`).

## 3. V3 in detail: the double-quantum Hamiltonian (MEASURED)

**Echo FI in 0–100 µs.** At equal pair norm:
- 1UBQ: DQ 103,867 vs secular 57,947 (×1.8);
- 1PGA: 73,717 vs 18,582 (×4.0).

At matched local-T₂ time (a DQ time t corresponds to a secular time √3·t, DERIVED from M₂,loc(DQ) = 3·M₂,loc(sec)), the FI per measurement is ×2.2 (1UBQ) and ×3.1 (1PGA). This is the right clock if reversal decay tracks the Hamiltonian's own local second moment. Sánchez et al. show the Loschmidt-echo decay becomes perturbation-independent with T₃ ~ T₂, "a rate only related to the local second moment of the Hamiltonian" (PRL 124, 030601 (2020), arXiv:1902.06628; LITERATURE).

**Hardness:**
- ε = 10⁻⁴ fails the DQ echo at 60 µs, which is ≈ 104 µs in secular-equivalent time. That is later than secular (70–80 µs).
- ε = 10⁻⁵ reproduces it to ≥ 60 µs.
- The exact sub-cluster (n = 9) fails at 20 µs vs 40 µs on 1UBQ, but at 40 µs vs 30 µs on 1PGA. **The faster-cone effect does not replicate.**
- g_med in the 0–100 µs window: DQ 1.69 / 2.16 vs secular 2.13 / 1.86.

**Environment.** The embedding misfit of the DQ F1 is 2.1σ at 60 µs, against 0.28σ for secular.

**Net:** DQ gives more information per shot at the price of more model dependence. It does not add classical hardness.

## 4. V4 in detail: the dilution scale law and structural relevance

**Scale invariance (DERIVED, exact).** H(λX) = λ⁻³ H(X) for dipolar couplings. Hence:
- O_{λX}(t) = O_X(t/λ³);
- per-parameter FI in Å⁻² scales as λ⁻², so the CRB scales as λ;
- qubit count, Trotter depth per dimensionless time, and classical cost are unchanged.

A network of density ρ is statistically a dense network rescaled by λ = (ρ_dense/ρ)^{1/3}.

**Consistency checks (DERIVED, INFERENCE):**
- The value lens reports amide CRB 0.026 Å against dense 0.014 Å. The scale law predicts ×λ ≈ 2.05.
- The dense exact-reach time (103–141 µs, value lens) × λ³ = 8.6 gives 0.9–1.2 ms for amide networks. This matches the value lens's "amide cone within exact reach for 1 ms in 6 of 7 jobs".

**Collapse check (MEASURED, coarse 20–60 µs grids).**
- In units of the cluster's rms coupling, the first echo failure is at t_c·ω_rms = 1.04 (0.85–1.27) for dense and 1.34 (1.02–3.7) for amide.
- In units of the probe-local coupling it is 2.5 vs 4.6.
- This is an approximate collapse, with a wide amide spread.

**Where the hard regime lives** (R₄₇ = radius holding N_ex = 47 labelled spins; `analysis.json` C; density law, with the direct count where the protein has enough spins):

| labelling | spins in 1UBQ / 1PGA | spacing a (Å) | R₄₇ (Å) | time stretch λ³ vs dense | residues needed for > 47 labels |
|---|---|---|---|---|---|
| dense ¹H | 629 / 419 | 2.5–2.6 | 5.7–6.1 | 1 | 6–7 |
| amide HN (perdeuterated) | 73 / 56 | 5.1–5.2 | 11.4–11.6 (count 14.7–15.5) | 7.5–8.6 | 47–49 |
| ILV methyl pseudo-spins | 33 / 15 | 6.8–7.9 | 15–18 | 19–28 | 109–176 |
| 1 label per 10 residues | 7 / 5 | 11.3–11.4 | 25 | 84–90 | ~510–530 |

**Inference.** Dilution is the only lever found that aligns classical hardness with *long-range, topology-level* distances: 11–15 Å for amide networks covers sheet pairing and helix packing; 15–25 Å for methyl or sparse labels covers core packing and domain arrangement.

It does not shrink the dimensionless coherent time needed. In units of T₂ the hard onset stays at the same ~8–16 T₂ (dense value: physics-feasibility lens, `scales.json`). This is well beyond the perturbation-independent reversal window of ~4–7 T₂ (LITERATURE for T₃ ~ T₂ scaling; the numerical 4–6.7 T₂ is quoted from the physics lens). Perturbations that do not scale with dilution (heteronuclear couplings, residual protons, motions) shrink the dimensionless window further (INFERENCE).

**Structural relevance and reversibility therefore pull in opposite directions under dilution.**

## 5. The strongest version found, and what it still lacks

**Strongest honest variant** (INFERENCE, assembled from measured pieces):
- a local-probe echo protocol measuring F1 **and** F2;
- in a perdeuterated or sparsely labelled network of a protein large enough that the labelled cone exceeds ~47 spins (≥ 50 residues for amides);
- time points chosen by hard FI per µs of evolution;
- optionally DQ-driven for ×2–3 FI per shot.

**What it lacks:**
1. At N ≤ 10 the F2 window is closed by ε = 10⁻⁵ (to ≥ 70 µs). No exact-classical separation is testable below the cone sizes where the value lens puts break-even (N_eff ≈ 30–47).
2. Its quantum-only value against the strongest measured twin is **1.65×** in repetitions. This is not the 10–160× echo/transfer FI ratio of the headline, which compares against the wrong baseline.
3. Every lever that raised information (F2, DQ) also raised environment sensitivity per unit time. Rigid N = 10 models are then biased (value lens §2), and the forward model must carry a larger, *known* environment.
4. The dilution route needs coherent, reversible evolution for ~10 T₂ at ms scale, beyond the published reversal windows.

## 6. Recommended decisive tests (not run: over this agent's 30 CPU-min cap). Submit through the governor, single-threaded.

1. **F2 against the ε ladder over the full window, N = 10** (kills or keeps V1 at N = 10).
   `OMP_NUM_THREADS=1 python research/experiments/ADVERSARIAL/R1_amplify/obs_amplify.py --pdb 1UBQ --probe 19 --eps-list 1e-5 --pauli-max-steps 160 --budget 3600 --subs "" --suffix _eps1e-5_full`
   Repeat for `--pdb 1PGA --probe 325` and `--probe 390`. About 20–40 CPU-min each, < 1 GB.
   **Kill:** ε = 10⁻⁵ reproduces F2 within σ over 0–320 µs on ≥ 2 of 3 probes. The N = 10 F2 window is then closed, like F1.
2. **F2 string-count scaling (C2/C3-style) at N = 8, 10, 12.** Extend `pauli_run` to N = 12 (dense 4096² complex matrices, ~270 MB each; F2 by matrix products).
   **Kill:** the ratio M*_F2/M*_F1 of strings needed for σ-accuracy to t₅₀ stays ≤ 3 and does not grow with N. F2 is then a constant-factor effect only, and V1 is killed as a hardness amplifier.
3. **F2 embedding with derivatives (R1-E protocol, N_env = 12)**, full parameter set. Cost ≈ 164 GFlop per recorded time point per geometry, i.e. 60–90 CPU-min: governor only.
   **Kill:** late-window F2 FI ratio (embedded / isolated) < 0.5, or top-eigendirection |cos| < 0.5.
4. **Exact-cone test in evolution-time units:** sub-cluster adversary n_c = N − 2 at N = 12 and 14 for F1 (cost 2t) and F2 (cost 4t).
   **Kill:** F2's cone requirement per µs of total evolution is not larger than F1's.
5. **DQ within the reversal envelope:** reweight the DQ and secular FI by the physics lens envelope A(t) (T₂ of each Hamiltonian's own M₂).
   **Kill:** DQ hard FI inside the envelope ≤ secular.
6. **Dilution scale-law check at the cone scale:** amide-only whole-domain networks (1UBQ-HN, 73 spins) with sparse Pauli dynamics or light-cone models. Test the predicted hard onset of 0.9–1.2 ms (λ³ × dense).
   **Kill:** onset < 0.5 ms (a dilution benefit beyond the scale law, which would be a surprise) or > 3 ms (worse than scale-free).

## 7. Reproduce (single-threaded; total used by this agent ≈ 26 CPU-min; each run ≤ 5.5 min)

```
cd research/experiments/ADVERSARIAL/R1_amplify
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python selftest.py                                                                             # 47 s   -> selftest.json
python obs_amplify.py --pdb 1UBQ --probe 19 --pauli-max-steps 100 --budget 300                 # 5.5 min -> out/obs_1UBQ_p19_N10_o0_secular.json
python obs_amplify.py --pdb 1UBQ --probe 19 --steps 50 --nt 10 --eps-list 1e-4,1e-5 --pauli-max-steps 50 --budget 200 --suffix _fine            # 4.8 min
python obs_amplify.py --pdb 1UBQ --probe 19 --ham dq --steps 50 --nt 10 --eps-list 1e-4,1e-5 --pauli-max-steps 50 --budget 90 --suffix _fine --f2 0   # 3.3 min
python obs_amplify.py --pdb 1PGA --probe 325 --ham secular --steps 50 --nt 10 --eps-list 1e-4 --pauli-max-steps 30 --budget 30 --suffix _fine       # 40 s
python obs_amplify.py --pdb 1PGA --probe 325 --ham dq --steps 50 --nt 10 --eps-list 1e-4 --pauli-max-steps 30 --budget 30 --suffix _fine --f2 0    # 46 s
python obs_amplify.py --pdb 1UBQ --probe 19 --steps 40 --nt 4 --eps-list 3e-5 --pauli-max-steps 40 --budget 150 --subs "" --suffix _eps3e-5     # 1.8 min
python embed_check.py        # 3.4 min -> embed_check.json
python analysis.py           # < 1 s   -> analysis.json (A depth budget, B bias law, C scale law, D design)
python gain_eps3e5.py        # < 1 s   -> gain_eps3e5.json
```

**Notes:**
- One DQ run crashed on a shape bug (sub-cluster MQC length) and was re-run after the fix. The crashed run cost ~3.3 CPU-min and produced no output.
- Peak RAM was not measured. The largest objects are N = 12 parity blocks (2048² complex, 64 MB), so the estimate is < 0.5 GB (INFERENCE).
- **Inputs (read-only):** `data/instruments/nmr/*_H.pdb`, `research/results/RAW/nmr_gate*/` and `src/qapf/nmr/spins.py`. Sibling results are quoted, not modified: `R1_replicate/pauli_eps3e-05_pair.json`, `R1_value_breakeven/README.md` and `R1_physics_feasibility/scales.json`.
- Nothing outside this folder was written.

**Literature checked this session (arXiv abstracts):**
- Abanin et al., "Constructive interference at the edge of quantum ergodic dynamics", arXiv:2506.10191. OTOC^(2) is dominated by constructive interference of large Pauli-string loops.
- Sánchez, Chattah, Wei, Buljubasich, Cappellaro & Pastawski, PRL 124, 030601 (2020), arXiv:1902.06628. Perturbation-independent Loschmidt-echo decay, T₃ ~ T₂.
- Zhang et al., arXiv:2510.19550. OTOC NMR of toluene and 3',5'-dimethylbiphenyl in a liquid crystal; geometry via MD-augmented models on Willow.

**Not verified:** Krojanski & Suter (MQC cluster-size decoherence scaling), which is not on arXiv, and Baum–Pines DQ sequences (LIT-UNVERIFIED).
