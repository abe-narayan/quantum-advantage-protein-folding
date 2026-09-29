# Audit C04 (novelty / prior art): kilonova Ln/An expansion opacity from thermal dipole spectral functions

Auditor role: NOVELTY / PRIOR-ART. Date: 2026-09-28. Status: COMPLETE.

**Verdict: WOUNDED.**
- Novelty holds as scoped category **B**.
- The scientific case for a quantum-necessary component is weak on audit questions 1, 2, 3 and 6 (lessons L5, L6 and L7).
- Neither "the exact comparison already exists" nor "the gap is cosmetic" applies, so there is no novelty kill. The physics-side audits should decide whether to kill.

Verification tags:
- [V-arXiv]: abstract read through the arXiv API.
- [V-full]: full text read (arXiv HTML).
- [V-CR]: Crossref record read.
- [V-OA]: OpenAlex record read.
- [MINE]: my own calculation or reasoning. Not from a source.

---

## 1. EXACT PRIOR WORK (quantum computing applied to kilonova / Ln-An opacity)

**None found.** Queries: arXiv API `kilonova AND (quantum computer|computing|algorithm|qubit)` returned 0. The OpenAlex cited-by lists of the two central classical opacity papers (42 + 29 citing works since 2024) contain no quantum-computing paper. The full text of 2607.02811 contains 0 hits for "kilonova", "lanthan", "actinide", "neutron star", "Sobolev" and "line list".

## 2. NEAREST QUANTUM WORK

1. **Pathak, Kononov, Baczewski, arXiv:2607.02811 (2026-07-02)**, "An approach for calculating astrophysical opacities on quantum computers" [V-full].
   - Electron and photon registers in first and second quantization, interaction-picture Hamiltonian simulation, and momentum-resolved photon readout.
   - Logical resources for solar Fe at 2.26e6 K and n_e = 4e22 cm^-3.
   - Uses an average-atom Pauli-Fierz Hamiltonian. It is **non-relativistic**. Quote: "does not include ... electronic relativistic effects leading to spectral line splitting, which **will be the subject of future work**."
   - It leaves "a detailed comparison to resource estimates for other approaches to estimating response functions" to future work, and it has no classical head-to-head.
   - It cites Bobrow et al. (2026, "in preparation") on the cost of thermal-state preparation for warm dense matter.
   - OpenAlex: 0 citing works (W7167595552).
   - **Scoop vector:** the same group has publicly committed to a relativistic extension.
2. **Fomichev et al., arXiv:2405.11015 (2024)** [V-arXiv] and **Fomichev et al., arXiv:2506.15784 (2025)** [V-arXiv]. XAS as a dipole spectral function computed with a time-domain Monte Carlo (Hadamard-test) algorithm, CAS(22e,18o) Mn-O cluster, compressed double-factorized Trotter with eigenvalue-error control. **Algorithmically this is the same primitive C04 proposes** (dipole autocorrelation leading to a broadened spectrum). It starts from the ground state, not a thermal ensemble, and it is non-relativistic.
3. **Response-function algorithms cited by 2607.02811** [V-full, reference list]:
   - Roggero & Carlson, PRC 100, 034610 (2019)
   - Kökcü et al., Nat. Commun. 15, 3881 (2024)
   - Kharazi et al., npj QI 11, 98 (2025)
   - Also related: arXiv:2404.19554, entanglement-assisted phase estimation for dynamical response functions (title only, arXiv listing), and arXiv:2605.22920, Green's functions by a robust quantum Arnoldi method (Sandia authors; title only).
4. **Relativistic atomic structure on quantum hardware or simulators.** All use few-electron light systems and compute energies or hyperfine constants, not spectra or opacity.
   - arXiv:2212.01801, quantum annealer eigensolver, fine-structure splittings of B-like ions (Kumar, ..., Dyall, Das) [V-arXiv]
   - arXiv:2212.02058, Bayesian phase-difference estimation, Dirac-Coulomb-Breit fine structure, 18-qubit active space [V-arXiv]
   - arXiv:2606.20166, QAE hyperfine constants of Li, Be+, Na, Mg+ with at most 12 CSFs, benchmarked against GRASP [V-arXiv]
   - Crossref 10.3390/quantum4020012, VQE precision for atomic many-body effects (title only) [V-CR]
5. **f-element quantum chemistry.** arXiv:2510.25675 treats Pu oxide/hydride reaction energetics with QCM and QPE on Quantinuum hardware with up to 19 qubits [V-arXiv]. arXiv:2601.10813 uses U2 as a benchmark for ADAPT-GCIM [V-arXiv]. These are molecular ground states, not atomic ion spectra.

## 3. NEAREST CLASSICAL WORK

- **Calibrated FAC line lists.** Flörs et al., arXiv:2507.07785, now Phys. Rev. D (2026), doi:10.1103/jxqw-7ynk [V-arXiv, V-CR]:
  - 28 Ln II/III ions, 146,856 levels and 28.7M E1 transitions.
  - Only 66,591 transitions have calibrated wavelengths.
  - Strong lines with log gf > -1 agree with experiment.
- **FAC fictitious-mean-configuration Bayesian optimisation.** Ferreira da Silva et al., arXiv:2502.13250, PRA 112, 012802 [V-arXiv, V-OA]:
  - Level errors fall from 20-60% to at most 10%.
  - **log gf RMS remains 1.1-1.4 dex versus experiment for Pr and Er.**
- **Systematic HULLAC/GRASP calculations.**
  - Tanaka et al., arXiv:1906.08914 [V-arXiv].
  - Kato et al., arXiv:2501.13286, MNRAS stae2504 [V-arXiv, V-OA]. Improved strategies give opacities **3-10x higher per element** (1.5x for the mixture). The structure is "controlled by transition arrays among several configurations", so an accurate energy-level distribution is the key. The new results agree with ab initio GRASP2K.
- **Gaigalas et al., arXiv:1901.10671** [V-arXiv]. MCDHF/RCI for Nd II-IV, level accuracy 10%, 3% and 11%. The Planck mean moves by at most 1.5x (kilonova timescale changes of 20% or less), but wavelength-dependent features are sensitive.
- **LANL CI suite with line-binned opacities.**
  - Fontes et al., arXiv:1904.08781, MNRAS 493, 4143 (doi:10.1093/mnras/staa485) [V-arXiv, V-CR]. Line-binned opacity is **area-preserving**, i.e. linear in line strength. It "agree[s] well with ... continuous Monte Carlo Sobolev" and with expansion opacity.
  - Actinides: arXiv:2209.12759 [V-arXiv].
- **Three-code Nd comparison.** Fontes et al., arXiv:2604.04362, ApJ (2026), doi:10.3847/1538-4357/ae5bfe [V-arXiv, V-CR]. LANL vs HULLAC vs Autostructure: peak L_bol differs by about 1.5x. The differences are **attributed to neutral Nd I data**, and **calibration to NIST changes the late-time IR structure significantly**.
- **Flörs et al., arXiv:2302.01780, MNRAS stad2053** [V-arXiv, V-CR]. FAC vs HFR for Nd and U II/III. Where experimental levels are few, "a large spread in the opacities" appears between codes.
- **HFR for all of Ca-Lr.** Deprince et al., arXiv:2412.16688, A&A 2025 [V-arXiv, V-OA].
- **Statistical RTA opacities without diagonalization.** Carvajal Gallego, Pain, Godefroid, Palmeri, Quinet, J. Phys. B (2024), doi:10.1088/1361-6455/ad2182 [V-CR abstract].
  - For half-filled-4f ions the Hamiltonian matrices are "so large that their diagonalization is challenging".
  - Statistical resolved-transition-array draws reproduce the exact HFR **expansion** opacity for Sm VIII and Eu VI and are then applied to Dy VIII.
  - **This classical method already avoids line enumeration.**
  - Also by Deprince et al.: EPJD (2024), doi:10.1140/epjd/s10053-024-00897-5 (Er III, "statistical simulations"; title only) [V-CR].
  - Also by Kato et al.: Phys. Lett. A (2025), doi:10.1016/j.physleta.2025.130884 (statistical analysis of level energies and effective line strengths; title only) [V-CR].
- **Expansion vs line-binned for Sm V-X.** Carvajal Gallego et al., MNRAS stad990 (2023) [V-CR]. More than 100M lines with HFR, cross-checked against MCDHF.
- **Correlation-specific work.**
  - Yang & Gao, "Electron correlation effects on radiative opacity of Nd III-IV: a large-scale calculation", Proc. SPIE (ICPQC 2026), doi:10.1117/12.3119572 [V-CR, title, authors and venue only; no abstract available].
  - Reitsma, Sheil, Versolato, Kahl, Berengut, arXiv:2606.04868 [V-arXiv]. This is the **closest analogue of "correlation fixes a dense-spectrum opacity"**, and it was **solved classically**. Saturated n=4 CI plus core-valence correlation in AMBiT (CI+MBPT, arXiv:1805.11265 [V-arXiv]) removes the long-standing blueshift of the Sn12+ EUV emission peak.
- **Machine-learning surrogate for mixed LTE opacities.** Kathirgamaraju, Wollaeger, Fontes, SSRN 6996785 (2026) [V-CR abstract]. H/He demonstration only.
- **Laboratory benchmark.** Er II at the LHD, J. Fusion Energy (2025), doi:10.1007/s10894-025-00531-1 [V-CR abstract].
- **Inference sensitivity.**
  - Brethauer et al., arXiv:2408.02731 [V-arXiv]. Atomic data change X_Ln by about 1 dex and M_ej by 25-40%. Thermalization changes M_ej by 20-50%. Lanthanide mass for GW170817 varies about 6x across datasets.
  - Gillanders, Flörs, Ferreira da Silva, arXiv:2512.24257, MNRAS stag748 [V-arXiv]. With **more complete** calibrated line lists, the fitted X_Ln is **20x lower** than earlier claims. The shift is driven by completeness.
- **NLTE.**
  - Pognan, Jerkstrand, Grumer, arXiv:2202.09245 [V-arXiv]. LTE expansion opacities hold for the first few days. After that, NLTE excitation changes opacity by 2-10x, and NLTE ionization by up to orders of magnitude.
  - Brethauer et al., arXiv:2508.18364 [V-arXiv]. Non-thermal ionization matters even at 2 days or earlier and changes the required mass by up to 3x.

## 4. WHAT HAS BEEN TESTED

- Code-to-code opacity spreads, calibrated vs uncalibrated:
  - Nd: 1901.10671, 2302.01780, 2604.04362
  - all Ln II: 2501.13286
  - all Ln II/III: 2507.07785
  - Ca-Lr: 2412.16688
- Line-binned vs Sobolev vs expansion opacity formalisms (1904.08781, stad990).
- Opacity convergence with number of lines (1904.08781).
- Statistical RTA vs exact diagonalization for expansion opacity (J. Phys. B 2024).
- Sensitivity of kilonova inference to atomic data, thermalization and NLTE (2408.02731, 2202.09245, 2508.18364, 2512.24257).
- Quantum side:
  - A dipole spectral function on a fault-tolerant quantum computer, with resource estimates, for XAS (2405.11015, 2506.15784).
  - An opacity protocol for dense Fe (2607.02811).
  - Tiny relativistic atomic eigenproblems on annealers and simulators (2212.01801, 2212.02058, 2606.20166).

## 5. WHAT HAS NOT BEEN TESTED (the gap)

- D: a quantum thermal dipole spectral function (a relativistic open-4f/5f ion Hamiltonian, Boltzmann-weighted initial states at 3000-10000 K, binned over 0.3-3 um).
- E: calibrated CI/FAC/HFR line lists.
- F: a classical kernel-polynomial / Lanczos (or stochastic-trace) spectral function on a large relativistic CI matrix.
- None of D, E or F has been compared with the others.
- **I found no application of KPM/Lanczos spectral functions to kilonova opacity at all.** arXiv query `(Lanczos|kernel polynomial|Chebyshev|moments) AND (opacity|transition array)` found only UTA/STA moment methods: 2505.21121, 2509.24042, 1608.00871 and 0905.2513 (titles). So the classical twin F is itself untested in this field.
- No study separates, for any Ln ion, opacity error from configuration completeness, from empirical calibration and from correlation/solver error. 2501.13286 and 2604.04362 come closest, but they vary the whole strategy, not the correlation treatment alone.

## 6. WHY THE GAP IS MATERIAL (and where it is thin)

**Material:**
1. Regime: isolated, low-density, open-4f/5f low-charge ions with a thermal initial ensemble. 2607.02811 covers dense-plasma average-atom Fe, is non-relativistic, and has one effective ion. 2405.11015 covers ground-state core-level XAS in a molecular cluster.
2. The target quantity is a **binned, temperature-dependent** opacity that feeds a radiative-transfer inference. It is not a single spectrum.
3. There is a real, documented unmet need for **uncalibrated ions** (most III ions and the actinides; 2302.01780, 2507.07785).
4. The classical twin F has never been run in this field, so even a negative head-to-head result would be new.

**Thin:**
1. **The quantum primitive is not new.** It is a dipole autocorrelation with a Hadamard test or QPE sampling, i.e. Fomichev XAS with a different Hamiltonian. The novelty is in the application and the comparison, not in the algorithm.
2. **Q2, the formalism.** A spectral-function readout is linear in line strength.
   - This matches the LANL **line-binned** formalism exactly (1904.08781), and LANL reports it agrees with Sobolev MC.
   - It does **not** by itself give the **expansion (Sobolev) opacity** sum of (1 - e^{-tau_l}), which Sedona, TARDIS, Tanaka/Kato and Deprince use. That opacity needs the per-bin line-strength distribution.
   - [MINE] Getting individual S_l, or sum S_l^2, needs spectral resolution below the line spacing (about 1e7 lines over about 3e4 cm^-1 gives sub-cm^-1 spacing, i.e. evolution near the Heisenberg time) or four-point / diagonal-ensemble quantities. Either is far more costly.
   - A workable path is a statistical RTA-style closure (J. Phys. B 2024) fed with quantum-computed array moments. But low-order array moments are what classical UTA/Racah algebra already gives cheaply.
3. **Q1 decomposition** from the evidence above:
   - (a) Completeness dominates the inference shifts: 20x in X_Ln (2512.24257), plus configuration-set choice (2302.01780, 2507.07785).
   - (b) Calibration and energy placement come next: 3-10x per element (2501.13286), IR structure (2604.04362), Planck mean at most 1.5x (1901.10671).
   - (c) Pure correlation/solver error has not been isolated. Where ab initio GRASP was compared, it agreed with the improved semi-empirical opacities (2501.13286).
   - Correlation does control relative configuration energies (4f^n vs 4f^{n-1}5d), and Sn12+ shows that correlation can shift a dense-spectrum peak (2606.04868). **That case was fixed classically** (saturated CI + CI+MBPT).
4. **Q3, the classical twin** [MINE, combinatorics]:
   - The valence space 4f5d6s6p has 32 spinors: Nd II (5e) is 2.0e5 determinants, Nd I (6e) 9.1e5, Gd II (9e) 2.8e7, Er III (12e) 2.3e8. Full CI + Lanczos/KPM with stochastic thermal traces is feasible classically across the whole series.
   - Classical exact methods become infeasible only once the 4d/5s/5p core is explicit: Nd II with 23e in 50 spinors is 1.1e14 determinants, and 120 spinors is 2.7e24.
   - That is **dynamic core-valence correlation**, which CI+MBPT (AMBiT), MRCI and relativistic CC treat perturbatively with small residual error.
   - The quantum-necessary slice is therefore narrow and not yet shown to matter at bin-width precision.
5. **Q4, the model floor** [MINE]:
   - Bins of 10-100 A at 1 um are about 100-1000 cm^-1.
   - Ab initio level errors today are about 3-11% of level energies (1901.10671), i.e. 1000+ cm^-1.
   - A 60-120-spinor quantum solve would still omit deeper core, Breit/QED and basis completeness, a floor of perhaps 100s of cm^-1 [UNVERIFIED magnitude].
   - The quantum solve could beat the current ab initio floor only if the classical CI+MBPT effort that removed the Sn12+ blueshift (2606.04868) cannot be repeated for Ln II/III. Nobody has shown that.
6. **Q6, information vs computation (L5):**
   - Beyond a few days, NLTE excitation and ionization (2-10x, up to orders of magnitude; 2202.09245, 2508.18364) and thermalization (20-50% in mass; 2408.02731) are of the same order as, or larger than, the atomic-data effects.
   - LTE opacity leverage is confined to the photospheric first few days.
   - The X_Ln leverage is real (1 dex), but it is dominated by completeness and calibration, which a better solver does not supply.
7. **Q5, resources** [MINE, indicative, UNVERIFIED]:
   - 100 cm^-1 resolution needs T of about 2*pi/(4.6e-4 Ha), i.e. about 1.4e4 a.u.
   - kT at 5000 K is about 3500 cm^-1, so many initial levels are populated and thermal ensemble or typicality preparation is needed.
   - With lambda of about 1e2-1e3 Ha for 60-120 spinors and about 1e3-1e5 samples, I estimate roughly 1e12-1e15 Toffoli per ion per T.
   - Multiplied over about 28 Ln II/III ions plus actinides.
   - Classical line lists for one ion cost CPU-hours to CPU-days. The resources auditor should firm this up.
8. **Q7, scoop risk: MODERATE-HIGH for the generic idea "relativistic quantum opacity".** 2607.02811 promises relativistic line splitting as future work; the group is at Sandia, next to Hansen's opacity codes (their ref. 29). The risk is **low for the specific kilonova thermal-ion + KPM-twin + inference-sensitivity study**: no signal in the quantum or kilonova literature through 2026-09-28.

## 7. WHY IT COULD STILL BE A NEW PAPER

A three-way benchmark would be publishable whatever the sign of the result:
- D: quantum-circuit (simulated) spectral function with fault-tolerant resource estimates.
- F: KPM/Lanczos on the largest feasible relativistic CI, the first use of this in kilonova opacity.
- E: calibrated FAC (2507.07785) / LANL (1904.08781).
- Scaling variables: f-occupation n and the explicit-core size.
- Validation: La II / Ce II / Nd II / Er II against NIST and the LHD Er II data.
- Decision metrics: the line-binned opacity (linear, spectral-function-native), the Planck mean, and a SuperNu/Sedona light-curve sensitivity.

The most likely outcome, and itself a novel result, is a scoped negative: "the valence-space thermal spectral function converges classically (F), and the opacity uncertainty budget is set by completeness, calibration and NLTE, not by the solver." This mirrors the protein-program conclusion. A positive quantum-advantage result would need evidence, not yet in the literature, that non-perturbative core-valence correlation moves binned opacity by more than the NLTE and calibration floors.

## 8. SCOPED NOVELTY STATEMENT

Sources searched through 2026-09-28:
- arXiv API: 11 queries (listed below).
- OpenAlex cited-by for Fontes 2020 (W2940065607, 42 works since 2024) and Flörs 2023 (W4384281337, 29 works since 2024), plus records for 2607.02811 (0 citations) and 2405.11015 (1 citation).
- Crossref: 6 queries/lookups.
- The full text of 2607.02811.

Found:
- (A) quantum dipole spectral-function algorithms for ground-state XAS (2405.11015, 2506.15784) and a non-relativistic quantum opacity protocol for dense-plasma Fe (2607.02811);
- (B) small relativistic atomic eigenproblems on quantum annealers and simulators (2212.01801, 2212.02058, 2606.20166);
- (C) extensive classical kilonova Ln/An opacity work, including calibrated FAC, HULLAC/GRASP, LANL line-binned, HFR and statistical RTA, with code-to-code comparisons.

Not found:
- (D) any quantum thermal dipole spectral-function computation of open-4f/5f low-ionization opacity;
- any comparison of D against (E) calibrated CI line lists or (F) classical KPM/Lanczos spectral functions on large relativistic CI;
- any use of F in kilonova opacity;
- any decomposition of the kilonova opacity spread that isolates correlation/solver error.

**Category B.** This is not proof of absence. WebSearch, Semantic Scholar and Google Scholar were unavailable, and theses and patents were not searched.

## 9. CITATION LIST (verification status)

| ID | Paper | Status |
|---|---|---|
| arXiv:2607.02811 | Pathak, Kononov, Baczewski (2026), quantum opacities | V-full |
| arXiv:2405.11015 | Fomichev et al. (2024), XAS on a QC | V-arXiv |
| arXiv:2506.15784 | Fomichev et al. (2025), fast XAS simulations | V-arXiv |
| arXiv:2212.01801 | Kumar et al., QAE relativistic excitation energies | V-arXiv |
| arXiv:2212.02058 | Sugisaki et al., BPDE fine structure | V-arXiv |
| arXiv:2606.20166 | Paul, Deb, Jönsson, Ekman, Das, QAE hyperfine constants | V-arXiv |
| arXiv:2510.25675 | Sorathia et al., actinide chemistry on trapped ions | V-arXiv |
| arXiv:2601.10813 | Poyyapakkam Sundar et al., chemically decisive benchmarks | V-arXiv |
| arXiv:2507.07785 / doi:10.1103/jxqw-7ynk | Flörs et al., calibrated Ln data | V-arXiv, V-CR |
| arXiv:2502.13250 | Ferreira da Silva et al., Bayesian optimization FAC | V-arXiv |
| arXiv:2501.13286 | Kato et al., Systematic opacity II | V-arXiv |
| arXiv:1906.08914 | Tanaka et al., Systematic opacity | V-arXiv |
| arXiv:1901.10671 | Gaigalas et al., Nd II-IV | V-arXiv |
| arXiv:1904.08781 / doi:10.1093/mnras/staa485 | Fontes et al., line-binned | V-arXiv, V-CR, V-OA |
| arXiv:2209.12759 | Fontes et al., actinide opacities | V-arXiv |
| arXiv:2604.04362 / doi:10.3847/1538-4357/ae5bfe | Fontes et al., three Nd data sets | V-arXiv, V-CR |
| arXiv:2302.01780 / doi:10.1093/mnras/stad2053 | Flörs et al., Nd and U | V-arXiv, V-CR |
| arXiv:2412.16688 | Deprince et al., HFR Ca-Lr | V-arXiv |
| doi:10.1088/1361-6455/ad2182 | Carvajal Gallego et al., statistical RTA | V-CR (abstract) |
| doi:10.1093/mnras/stad990 | Carvajal Gallego et al., Sm expansion/line-binned | V-CR (abstract) |
| doi:10.1140/epjd/s10053-024-00897-5 | Deprince et al., Er III statistical | V-CR (title) |
| doi:10.1016/j.physleta.2025.130884 | Kato et al., statistical line strengths | V-CR (title) |
| doi:10.1117/12.3119572 | Yang & Gao, correlation effects in Nd III-IV opacity | V-CR (title only) |
| doi:10.2139/ssrn.6996785 | Kathirgamaraju et al., ML opacity surrogate | V-CR (abstract) |
| doi:10.1007/s10894-025-00531-1 | Priti et al., Er II at the LHD | V-CR (abstract) |
| arXiv:2606.04868 | Reitsma et al., Sn12+ blueshift resolved | V-arXiv |
| arXiv:1805.11265 | Kahl & Berengut, AMBiT | V-arXiv |
| arXiv:2408.02731 | Brethauer et al., systematic uncertainties | V-arXiv |
| arXiv:2512.24257 | Gillanders et al., improved Ln constraints | V-arXiv |
| arXiv:2202.09245 | Pognan et al., NLTE expansion opacities | V-arXiv |
| arXiv:2508.18364 | Brethauer et al., non-thermal ionization | V-arXiv |
| Roggero & Carlson PRC 2019; Kökcü Nat. Commun. 2024; Kharazi npj QI 2025 | response-function algorithms | seen in the 2607.02811 reference list only |
| arXiv:2505.21121, 2509.24042, 1608.00871, 0905.2513 | STA/UTA moment methods | titles only (arXiv listing) |

## 10. QUERY LOG

- WebSearch: budget exhausted (200/200); no queries possible.
- Semantic Scholar: HTTP 429.
- OpenAlex keyword search: rate-limited, so I used DOI lookups and `cites:` filters.
- arXiv API (after an initial 429):
  1. `all:kilonova AND (all:"quantum computer" OR all:"quantum computing" OR all:"quantum algorithm" OR all:qubit)` returned 0.
  2. `(lanthanide|actinide|"rare earth"|"open f-shell"|4f) AND ("quantum computer"|"quantum computing"|"quantum algorithm"|QPE|"variational quantum")` returned 78, mostly hardware. Relevant: 2510.25675, 2601.10813.
  3. `(opacity|opacities|photoabsorption|"oscillator strengths") AND ("quantum computer(s)"|"quantum algorithm"|"fault-tolerant"|QPE)` returned 13. Relevant: 2607.02811 only.
  4. `(kilonova|kilonovae|macronova) AND (opacity|"atomic data"|"line list") AND (lanthanide|actinide|"atomic structure"|CI)` returned 62, all classical.
  5. `(atom|atomic|ions) AND relativistic AND (quantum computer|computing|algorithm|VQE|QPE|annealer)` returned 22. Relevant: 2212.01801, 2212.02058, 2606.20166, 2406.04992.
  6. `CI|CI+MBPT|CIPT AND open 4f ... lanthanide` returned 3 (AMBiT, hfs Dy/Ho/Cf/Es, polarizabilities).
  7. `CI|emu CI|PT AND (many valence electrons|dense spectra) AND atoms` returned 34. Relevant: 2606.04868.
  8. `(absorption spectrum|dipole autocorrelation|linear response|spectroscopy) AND (fault-tolerant|QPE|Hadamard test) AND (thermal|excited|molecules|atoms)` returned 17, none on atomic opacity.
  9. `au:Baczewski|Kononov|Pathak AND quantum` returned 60. No kilonova or relativistic-opacity follow-up yet.
  10. `(Lanczos|kernel polynomial|Chebyshev|moments) AND (opacity|transition array) AND (atomic|ions|plasma)` returned 14. Only UTA/STA; no KPM for kilonova.
  11. `(kilonova) AND (NLTE|non-LTE) AND (opacity|ionization|photospheric)` returned 11. Relevant: 2202.09245, 2508.18364.
  12. `(quantum computer|algorithm) AND (atomic spectra|atomic structure|line strengths|oscillator strength|transition probabilities|highly charged ions)` returned 66, none relevant.
- OpenAlex:
  - DOI lookups: 2607.02811 (W7167595552, 0 citations), 1904.08781 arXiv record, 2507.07785, 2604.04362, staa485 (W2940065607, 125 citations), stad2053 (W4384281337, 33 citations), 2405.11015 (W4398191577, 1 citation).
  - `cites:W2940065607` since 2024: 42 works, no quantum-computing paper.
  - `cites:W4384281337` since 2024: 29 works, no quantum-computing paper.
- Crossref:
  - "quantum computing kilonova opacity lanthanide" (no QC hits; found the Yang & Gao SPIE record)
  - "quantum algorithm atomic opacity spectral function Hamiltonian simulation" (no relevant hits)
  - "variational quantum eigensolver relativistic atoms heavy elements" (found Quantum Reports 2022)
  - DOI lookups: staa485, stad2053, 12.3119572, ad2182, epjd 2024, physleta 2025, ssrn 6996785, LHD Er, stad990, jxqw-7ynk, ae5bfe.
- Full text of arXiv HTML 2607.02811, grepped for kilonova, lanthan, actinide, Sobolev, expansion, relativistic, future work, thermal and the reference list.
