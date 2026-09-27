# R1 adversarial lens: physical feasibility of the NMR echo window

_2026-09-27. Adversarial audit of the only surviving lead, R1 (the protein ¹H dipolar echo/OTOC window). This lens asks one question: **can the echo data that carry the classically-hard Fisher information be produced by a real protein sample?** It does not re-test classical hardness._

Tags: **MEASURED** (computed here; files below), **DERIVED** (short derivation, checked numerically), **LIT** (literature, verified this session on arXiv; the source is named), **LIT-2°** (a reference we saw only in the reference list of a verified paper), **INFERENCE**, **UNPROVEN**.

## Verdict: KILLS at the practical level (conditional on one transferable constant)

**Why the practical level fails.** The echo window that holds the classically-hard information sits at or beyond the many-body time-reversal horizon measured in dipolar solids.

- **Where the window is (MEASURED).** Time is expressed in units of T2 = 1/√M2, the definition of Sánchez et al. 2022. The classical-failure time is t_c* = 3.8–17 T2. The echo-FI midpoint is t_50 = 4.8–25 T2 (median ≈ 10). Both are measured in the isolated-cluster T2, the most generous normalisation. In whole-protein-network units they are 5.6–19.5 T2 and 11–24 T2.
- **Where reversal fails (LIT).** Measured reversal horizons are T3 ≈ 4 T2 for a local polarization echo, which is the protocol a site-resolved protein experiment needs. They are T3 ≈ 6.7 T2 for the best magic-echo-type Loschmidt echo, in adamantane, in the perturbation-independent limit. Past T3 the echo decays exponentially with time constant 1.7 T2.
- **What survives (MEASURED).** Only the RAW per-time-point Fisher information (FI) is re-weighted, so nothing else is assumed.
  - Under the site-resolved polarization-echo envelope, a median of 0.9% of the hard-window echo FI survives (range 5e-12 to 10%).
  - The quantum forward model's information gain over everything a classical inversion can use is ≤ 1.32 in 11 of 11 jobs. That classically usable set is the transfer data plus the early echo.
  - With the best-case adamantane Loschmidt-echo envelope and the most generous normalisation, 2 of 11 jobs reach gain ≥ 2. With the physical whole-network T2, 0 of 11 do (maximum 1.35).
- **Break-even (MEASURED).** A median gain of 2 needs T3/T2 ≈ 7.5 in the most generous accounting (range 5.4–18.8, and one job never reaches it). In the physical accounting it needs ≈ 15 (8–29 in network units, 11–38 if backward time is counted). Measured values are 4–6.7. Sánchez et al. 2022 argue that better hardware cannot raise this ratio.

**The condition.** T3/T2 has been measured in adamantane, ferrocene, cymantrene and cobaltocene, not in a protein. The verdict holds only if proteins are not ≥ 2× more reversible than those model solids (INFERENCE). One experiment decides this; see test C.

**Independent obstacles.** These hold even if reversal were perfect (MEASURED in-model, N = 10):

- **Model error.** The isolated, static, secular, offset-free Hamiltonian that produced the RAW data is wrong by 7–49 σ once methyl rotation is included, and by 5–66 σ once realistic 1 kHz site offsets are included. The first exceedance comes at 40–50 µs.
- **Nuisance parameters.** Unknown offsets plus an imperfect backward leg absorb most of the hard-window structural information. With no priors, 21% (dense) and 2% (amide-only) is retained. With moderate priors (±0.2 ppm, ±2%) it is 46% and 14%.
- **Site resolution.** Static ¹H lines are 43–47 kHz wide (dense) and 10–11 kHz wide (amide-only), so a single proton cannot be picked out by chemical shift. Site selection has to come from site-specific ¹³C/¹⁵N labels, with one labelled sample per (probe, butterfly) pair.

**What is benign (MEASURED).** Static conformational heterogeneity (≤ 0.2 Å, rigid-residue model) keeps 80–99% of the hard-window echo FI. A 2° mosaic spread keeps 87–99%. A full powder average keeps about 56% (N = 10, M = 16 orientations). Physical sample imperfection is therefore not the problem. Irreversibility and model error are.

## Claim levels

| Level | Status after this audit |
|---|---|
| Theoretical (forward-simulation task: exact site-resolved echo of a secular XXZ network) | **Unchanged.** It is still a well-posed simulation task. Hardness of the tested classical approximations was MEASURED at N = 10 and is not proven (L1). This audit does not touch it. |
| Practical (structural information from real protein echo data that only a quantum forward model can use) | **L0 / killed (conditional).** The informative data lie beyond demonstrated reversal horizons. The model omits effects that exceed σ by 5–66×. Obtaining site resolution costs one labelled sample per spin pair. |

## Feasibility table: required vs achievable

"Required" means what the R1 FI numbers assume. "Achievable" means what the verified literature or our computation shows.

| Quantity | Required by R1 | Achievable / measured | Status |
|---|---|---|---|
| Homonuclear coupling scale | Dense N = 10 clusters: max \|d_ij\|/2π = 6.7–10.3 kHz (MEASURED). The formula uses d = 2π·120.1 kHz·P2/r³, so the task's "20–40 kHz" corresponds to the unscaled 120.1/r³ at 1.5–1.8 Å. Amide-only: 1.8–5.0 kHz. | A rigid protonated protein has whole-network √M2/2π = 18–20 kHz (FWHM 43–47 kHz); amide-only has 4.4–4.8 kHz (MEASURED from the PDB geometry). Methyl rotation lengthens T2 from 8.0–8.7 to 9.8–10.8 µs (MEASURED). | OK. Couplings are geometric. Only ratios matter for the reversal test. |
| Position of the hard window | t_c*/T2_cl = 3.8–5.7 (dense), 4.6–16.8 (amide). t_50/T2_cl = 4.8–10.1 (dense), 9.2–25 (amide) (MEASURED, `scales.json`). | — | — |
| Reversal horizon T3/T2 | Break-even for gain ≥ 2 (median): 7.5 (cluster T2, forward time only), 14.8 (network T2), 15.0 (cluster T2, forward + backward) (MEASURED, `reversal_envelope.json`). | **6.7** for the best magic-echo-type Loschmidt echo, adamantane, perturbation-independent, stated as not improvable (LIT: Sánchez, Chattah & Pastawski PRA 105, 052232 (2022)). **≈ 4** for the local polarization echo, which "remains Gaussian as long as the SNR is significant" (LIT, same paper, citing Usaj et al. 1998, Pastawski et al. 2000, Zangara & Pastawski 2017). "T3 ~ T2" (LIT: Sánchez et al. PRL 124, 030601 (2020)). "T3 … closely tied to T2" (LIT: Zangara et al. Phil. Trans. A 374 (2016)). | **FAIL.** The polarization-echo protocol gives gain ≤ 1.32 in 11/11 jobs. The best-case Loschmidt echo gives gain ≥ 2 in 2/11 jobs (generous) and 0/11 (physical). |
| Operator size at reversal failure | The hardness argument needs light cones beyond exact classical reach (≳ 30–40 spins). | XXZ Loschmidt-echo signal "fades away after reaching 10² entangled spins"; for the DQ Hamiltonian, 10⁴ (LIT: Sánchez 2022, adamantane). | Marginal. The window where the operator is large and the data still survive is narrow for XXZ. |
| Hamiltonian model error at t ≥ t_c* | < σ = 0.01 | Methyl/NH₃ rotation: 7–33 σ (1UBQ p19), 24–49 σ (1PGA p390). 1 kHz RMS offsets: 5–9 σ (dense), 65–66 σ (amide). Backward-leg scaling mismatch of 2%: 1–3 σ; 5%: 4.6–18 σ; 15% (the ±k slope difference Sánchez 2022 measured): 23–65 σ (MEASURED, `physics_*.json`). | **FAIL as-is.** Fixable only by adding nuisance parameters (next row). |
| Heteronuclear and offset terms (amide-only) | Pure homonuclear model (local √M2/2π 1.7–4.2 kHz) | Bonded-N local field RMS: ¹⁵N 2.7–5.6 kHz, ¹⁴N 3.2–6.5 kHz. ²H bath: 1.3–2.2 kHz (MEASURED). | **FAIL** without ¹⁵N plus ²H decoupling or engineered sequences on both legs. |
| Identifiability with nuisances (offsets Ω_i, backward mismatch η) | All hard-window FI usable | Retained hard-window structural FI (trace) after profiling: dense 0.21 with no prior, 0.46 with Ω ±0.2 ppm and η ±2%, 0.83 with ±0.05 ppm and ±0.5%. Amide-only: 0.02 / 0.14 / 0.42 (MEASURED). | Costly: a factor of 1.2 to 50 in FI. |
| Site resolution (prepare/read one ¹H; butterfly on one ¹H) | Single-proton Z_a and Z_b | Static ¹H FWHM 43–47 kHz (dense) and 10–11 kHz (amide) (MEASURED), against a total ¹H shift range of ~8–12 kHz at 0.8–1.2 GHz (INFERENCE). The only route is a site-specific ¹³C/¹⁵N label: polarization-echo injection via the bonded ¹H (LIT: Sánchez 2022 describing Zhang, Meier & Ernst PRL 69, 2149 (1992) [LIT-2°]; single-¹³C-label OTOC in Zhang et al. arXiv:2510.19550). | Possible in principle. It needs one labelled sample per (probe, butterfly): 4 per probe in the RAW design. |
| Per-point SNR | σ = 0.01 of the full single-site polarization, i.e. SNR 100 per point | Scans needed = (1/(σ·s1·A))². s1 is the per-scan single-site SNR, taken as 0.1–3 (INFERENCE). At A = 1: 0.23 d/point for s1 = 1, 23 d for s1 = 0.1 (2 s recycle). Recovering the ideal hard-window FI of one probe under the best-case Loschmidt echo (generous): 32–206 d (dense) and 125 to 6.5·10⁶ d (amide) at s1 = 1. Under the polarization echo: 120–1900 d (dense) (MEASURED arithmetic, `snr_budget.json`). | Marginal (Loschmidt echo, s1 ≥ 1) to FAIL (polarization echo). This is per probe; a structure needs many probes. |
| Orientation | A single B0 orientation | Powder: echo keeps 0.59 (easy) and 0.56 (hard); transfer keeps 0.46 and 0.26. 2° mosaic keeps 0.87–0.99 (MEASURED). | OK |
| Static heterogeneity | A single structure | Rigid-residue σ = 0.05 / 0.1 / 0.2 Å keeps 0.99 / 0.94–0.96 / 0.80–0.89 of the hard FI. The ensemble-mean signal differs from the single structure by 3–15 σ, so the forward model must average over the ensemble (MEASURED). | OK, but the forward model must include the ensemble average. |
| Liquid-crystal-aligned protein (alternative sample) | Many-body scrambling regime | Residual ¹H–¹H couplings in weakly aligned proteins are ≲ 10–100 Hz and ¹H T2 is tens of ms, which allows only a few coherent dipolar radians (INFERENCE). Zhang et al. reach 2.5 ms forward plus 2.5 ms backward at d ≈ 2 kHz because their molecules are **finite isolated ~10–15-spin networks** (LIT: 2510.19550). | FAIL for the R1 regime |
| rf heating and hardware | ms of rf | No appreciable heating in adamantane; the multipulse variant "could be used in biological systems without the risk of heating" (LIT: Sánchez 2022). | OK (INFERENCE for hydrated proteins) |

## What was computed (all single-threaded; about 11 CPU-minutes in total)

1. **`scales.py` → `scales.json`.** Coupling scales, Van Vleck M2, T2 of the isolated cluster, of the whole protein network (static and methyl/NH₃-rotor-averaged) and of the powder, and heteronuclear local-field second moments for all 11 γ = 0 RAW jobs that have echo FI.
   - DERIVED and checked to machine precision against dense matrices at N = 6: M2_global = (9/4)⟨Σ_j d_ij²⟩, M2_loc(I_y^a) = (5/4)Σ_j d_aj², M2_loc(I_z^a) = (1/2)Σ_j d_aj².
2. **`reversal_envelope.py` → `reversal_envelope.json`.** Re-weights the RAW per-time-point echo FI by A(t)².
   - Literature envelopes: polarization-echo Gaussian with T3 = 4 T2; Loschmidt-echo logistic with T3 = 6.7 T2 and tail 1.7 T2 (Sánchez 2022, Eq. 15); hypothetical envelopes at 20 T2 and 50 T2.
   - Three T2 normalisations (cluster, network, rotor-averaged network) × two time arguments (forward only, "generous"; forward + backward, "literal").
   - Reports the hard-window retention, the gain against all classically usable data (transfer FI plus easy echo FI), and the T3/T2 that gain ≥ 1.5, 2 and 10 require.
   - Echo normalisation by a reference Loschmidt echo scales signal and noise together, so it does not undo the A² factor (DERIVED).
3. **`physics_perturbations.py` → `physics_<job>.json`.** Exact in-model tests on the RAW cluster geometry: rotor averaging, nuisance Fisher/Schur complement, disorder and mosaic, powder.
   - The explicit echo engine reproduces RAW F_ab to 2e-16. The reconstructed parameters reproduce RAW dF exactly.
   - Jobs: 1UBQ p19 (dense) for all tests, 1UBQHN p548 (the best amide-only job) for nuisance and disorder, 1PGA p390 for rotor.
4. **`snr_budget.py` → `snr_budget.json`.** Scan-count arithmetic under stated assumptions.
5. **`summarize.py` → `summary.json`.** The decisive numbers in one place.

Reproduce (single-threaded, ≈ 11 CPU-min):
```
cd research/experiments/ADVERSARIAL/R1_physics_feasibility
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python scales.py && python reversal_envelope.py
python physics_perturbations.py --job 1UBQ_p19_N10_o0_g0.json --tests rotor,nuis,disorder,powder --M 8   # ~5 min (powder was run with --M 16)
python physics_perturbations.py --job 1UBQHN_p548_N10_o0_g0.json --tests nuis,disorder --M 8            # ~5 min
python physics_perturbations.py --job 1PGA_p390_N10_o0_g0.json --tests rotor
python snr_budget.py && python summarize.py
```

## Mechanism (why the two windows coincide)

- **INFERENCE, supported by MEASURED and LIT.** Classical approximations fail when the Heisenberg operator Z_a(t) has spread its weight over many high-weight strings (T6, §3). Time reversal fails when a scrambled operator amplifies small uncontrolled terms Σ. Sánchez 2022 calls this the perturbation-independent regime: the decay rate is set by the local second moment, not by the size of Σ.
- Both are consequences of the same operator growth, and both are measured in units of T2. The constants put reversal failure (4–6.7 T2) before or at classical-approximation failure (3.8–17 T2) and before the FI midpoint (4.8–25 T2).
- Rescaling the couplings (dilution, deuteration, Floquet scaling k) moves both windows together, because T3 ∝ T2^k (LIT). It cannot open a gap.
- The late-echo sensitivity that produces 10–160× more FI than transfer is the same sensitivity that makes the echo irreversible and confounded by nuisance parameters (MEASURED: Schur-complement losses are largest in the hard window).

## Flaws found in the R1 evidence (outside this lens's own code)

1. **Duplicated parameter.** In every 1UBQ p19 N = 10 RAW job (o0 and o1, γ = 0 / 1000 / 5000), `rigid_res16` moves one proton. It is identical to `radial_HA/GLU16`: same FI to the last digit (MEASURED). These jobs predate the "≥ 2 protons" rule in the prereg v2 fix. Summed FI double-counts that direction, and the 4×4 Fisher matrix is singular.
2. **Methyl protons as structural parameters.** Methyl protons are held static and used as parameters: `radial_HG22/ILE3` (1UBQ p19) and `radial_HG21/THR53` (1PGA p390). Above ~100 K methyls rotate fast (INFERENCE), so a "radial displacement of one methyl proton" is not a physical structural coordinate. Rotor averaging alone changes the echo by 7–49 σ (MEASURED).
3. **Omitted strongest partners.** The N = 10 clusters include 1–2 protons of a methyl but not the other methyl protons, which sit 1.8 Å away with ~20 kHz unscaled couplings (MEASURED, cluster composition). R1-E embedding tested only +2 nearest environment spins.
4. **The cluster model cannot represent irreversibility.** The isolated-cluster model has no unbounded bath and no Σ, so it cannot predict its own reversal failure. "Noiseless circuit tracks exact beyond t_c*" (Q-PoP) is therefore silent on whether the data exist (INFERENCE).
5. **Mismatched gain metric.** The C1 gain compares echo-total with echo-easy. It ignores that transfer data (classically exact, no reversal needed) are also available to the classical side. Here gain is re-defined against transfer plus easy echo. The ideal median gain is then 8.4 (range 1.8–24) (MEASURED).
6. **Conflict with the prior-art protein estimate.** Zhang et al.'s SI estimate for proteins (LIT: 2510.19550, SI §M) assumes cluster decoherence τ_d ≈ 1 s and t_exp ≈ 0.5–2 ms at 10–12 Å. Our computed protonated-protein T2 of 8–11 µs and the literature T3 ≈ 4–6.7 T2 give T3 ≈ 30–70 µs, 7–60× shorter than their t_exp (INFERENCE). They attribute their own Loschmidt-echo decay to fixable higher-order Magnus terms and rf inhomogeneity. Sánchez 2022 argues the XXZ decay is intrinsic and not fixable. Their systems are finite ~10–15-spin molecules with a DQ Hamiltonian. A protein solid is an unbounded XXZ network.

## Counter-evidence and residual windows

- **Scaling counter-evidence (LIT).** Domínguez, Rodríguez, Kaiser, Suter & Álvarez, PRA 104, 012402 (2021) (arXiv:2005.12361), measured on a controlled Hamiltonian (abstract-level): the fidelity decay rate grows as K^α with the number K of correlated qubits, and α drops below 1 under weak perturbation ("no inherent limit to the number of qubits that can be controlled"). This concerns how the rate scales with cluster size. It is compatible with a finite T3/T2 but weakens "intrinsic" as a universal claim. Sánchez 2022 itself warns against "excessive universality" of the decay laws.
- **Residual R1-DQ (UNPROVEN).** The DQ (double-quantum) engineered Hamiltonian (TARDIS in 2510.19550) is reported to be more reversible: its Loschmidt echo survives to ~10⁴ spins against ~10² for XXZ (LIT: Sánchez 2022). The DQ echo is a different forward model. Its classical-adversary failure time and FI split have not been computed.
- **Protein-specific T3/T2 (UNPROVEN).** No protein measurement exists in what we could verify. Only a measured T3/T2 ≥ ~15 for a site-resolved echo in a protein solid would reopen R1 at the practical level.

## Recommended tests (with kill criteria)

- **A. Replicate the physics tests on all 11 jobs** (governed; ≈ 8–10 CPU-min per job; each run ≤ 1.5 GB):
  `OMP_NUM_THREADS=1 python research/experiments/ADVERSARIAL/R1_physics_feasibility/physics_perturbations.py --job <JOB>.json --tests rotor,nuis,disorder,powder --M 12`
  - Kill: if the median hard-window FI retained after profiling with moderate priors (Ω ±0.2 ppm, η ±2%) is < 0.5, every R1 FI and gain number must be restated after profiling.
- **B. In-model Loschmidt echo with explicit Σ** (new code; governed; N = 12 dense 4096-dim, ≤ 10 CPU-min per setting). Simulate an actual magic-echo / MPSDI block with finite pulses, ω1 = 80 kHz and rf inhomogeneity σ = 6.4% (the Zhang et al. value). Measure the polarization-echo half-time T3 in units of T2_cluster.
  - If T3/T2 ≤ 7, the model itself confirms that the hard window is irreversible.
  - If T3/T2 ≫ 15, record that the finite cluster cannot represent intrinsic irreversibility (a model-inadequacy flag), and rely on test C.
- **C. Decisive experiment** (outside compute). Measure a local polarization echo (single ¹³Cα or ¹⁵N label → bonded ¹H → back) in a microcrystalline protein (GB1 or ubiquitin) at 100–280 K. Record T3/T2 with T2 = 1/√M2 from the ¹H FID.
  - Kill: T3/T2 < 10 means R1 stays dead at the practical level.
  - Reopen only if T3/T2 ≥ 15.
- **D. R1-DQ.** Re-run the C1/C3 statistics (sparse-Pauli ε = 1e-4 adversary, echo FI split) with H_DQ = Σ d_ij (I⁺I⁺ + I⁻I⁻) + h.c. on the same clusters.
  - Kill: sparse Pauli reproduces the DQ echo to σ over the window, or the DQ t_50/T2 exceeds the DQ T3/T2 reported in the literature.
- **E. Repair the C1 parameterisation.**
  - Remove the duplicated rigid parameter.
  - Replace methyl-proton radial parameters with rotor-axis (carbon) displacements under rotor-averaged couplings.
  - Include offsets as profiled nuisances.
  - Recompute f_hard and the gain.
  - Kill: gain (against transfer plus easy echo) < 2 in the median job, even before reversal envelopes are applied.

## Literature verified this session (arXiv abstract or full text)

- **Sánchez, Chattah & Pastawski**, *PRA* 105, 052232 (2022), arXiv:2112.00607. **Full text read.**
  - Setup: adamantane polycrystal, 300 MHz, 303 K; T2 = 1/√M2 (Eq. 2).
  - T3 ≈ T2/0.15 ≈ 6.7 T2; logistic decay with 1/λ ≈ 1.7 T2.
  - The ±k slopes were 23.0 and 26.5 ms⁻¹ (a 15% mismatch).
  - For the polarization echo, "emergent T3 of about 4 T2", Gaussian.
  - Loschmidt-echo signal fades at 10² spins for XXZ and at 10⁴ for DQ.
- **Sánchez, Chattah, Wei, Buljubasich, Cappellaro & Pastawski**, *PRL* 124, 030601 (2020), arXiv:1902.06628 (abstract): "T3 ~ T2", perturbation-independent.
- **Levstein, Usaj & Pastawski**, *J. Chem. Phys.* 108, 2718 (1998), arXiv:cond-mat/9708172 (abstract): polarization echoes in polycrystalline cymantrene and ferrocene; the non-inverted Hamiltonian explains the decay for a single ring.
- **Zangara, Bendersky, Levstein & Pastawski**, *Phil. Trans. R. Soc. A* 374, 20150163 (2016), arXiv:1508.07284 (abstract): T3 is "closely tied to T2".
- **Domínguez et al.**, *PRA* 104, 012402 (2021), arXiv:2005.12361 (abstract). **Domínguez & Álvarez**, *PRA* 104, 062406 (2021), arXiv:2107.03870 (abstract).
- **Morgan, Oganesyan & Boutis**, *PRB* 86, 214410 (2012), arXiv:1205.7039 (abstract): magic-echo degradation.
- **Zhang, Cortiñas, Karamlou et al.**, arXiv:2510.19550. **Full text read.**
  - Samples: [4-¹³C]-toluene in EBBA and ¹³C-DMBP in 5CB; 500 MHz; 295 K and 289 K.
  - TARDIS DQ-engineered reversal; rf inhomogeneity FWHM ~15%; d ≈ 2 kHz; 2.5 ms forward plus 2.5 ms backward.
  - SI protein estimate assumes τ_d ≈ 1 s.
- **O'Brien et al.**, *PRX Quantum* 3, 030345 (2022), arXiv:2109.02163 (abstract): ubiquitin "confined in a membrane"; learnability appears only as the dipolar interaction is suppressed.
- **LIT-2°** (seen only in the Sánchez 2022 reference list, not fetched): Rhim, Pines & Waugh, PRB 3, 684 (1971); Zhang, Meier & Ernst, PRL 69, 2149 (1992); Álvarez, Suter & Kaiser, Science 349, 846 (2015); Usaj, Pastawski & Levstein, Mol. Phys. 95, 1229 (1998).
- **Not verified here (INFERENCE-level typical values):** ¹H chemical-shift ranges and amide ¹H CSA, residual-dipolar-coupling magnitudes in weakly aligned proteins, ¹H T1/T2 of protein samples, per-scan single-site SNR.
