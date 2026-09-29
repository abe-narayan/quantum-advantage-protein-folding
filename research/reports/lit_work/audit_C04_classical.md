# Audit C04 (classical adversary): kilonova Ln/An expansion opacity from thermal dipole spectral functions

Status: COMPLETE (2026-09-28). Auditor role: classical adversary.
Verdict: **KILLED** in the decision-relevant regime (LTE photospheric expansion opacity at the accuracy that kilonova inference can use). One narrow residual lane is noted in section 6. It is not a quantum-solver lane.

---

## 0. Query log (all searches were run 2026-09-28)

- WebSearch: the session budget was exhausted (200/200). One attempt was refused and no results came back.
- OpenAlex: HTTP 429 on the first call and not retried.
- arXiv export API queries:
  1. `abs:kilonova AND abs:opacity AND abs:lanthanide` sorted by date, 40 max. 32 hits (2017-2026).
  2. `abs:"open 4f" AND abs:"configuration interaction"`. 2 hits, not relevant.
  3. `abs:"configuration interaction" AND abs:"perturbation theory" AND abs:"open shells"`. Returned AMBiT 1805.11265.
  4. `ti:pCI AND abs:"configuration interaction"`. Returned 2410.06680 and 2503.01379.
  5. `au:Bilous AND abs:neural`. Returned 2408.00477, 2209.05867, 2406.08154 and others.
  6. `abs:"neutron star merger" AND abs:"energy levels" AND (Ln/An terms)`. 11 hits: 2608.20881, 2507.07785, 2501.13286, 2412.14597, 2411.16998, 2302.01780, 2206.04232, 2204.06861, 2102.07879, 2002.08075, 1906.08914.
  7. `abs:kilonova AND (NLTE|non-LTE) AND abs:opacit*`. 0 hits.
  8. `abs:kilonova AND abs:"expansion opacities"`. 7 hits: 2602.22886, 2412.16688, 2306.17612, 2207.02311, 2202.09245, 2009.13192, 1904.08781.
  9. `au:Gaigalas AND (lanthanide|kilonova|"neutron star")`. 15 hits.
  10. `abs:"configuration interaction perturbation theory" OR "CIPT method"`. Not useful.
  11. `abs:"coupled cluster" AND (open 4f / open f)`. 1 hit: 2107.11234.
  12. `abs:"CI+MBPT" AND (Ln/An)`. Returned 2008.01675 and 1701.09075.
  13. `au:Berengut AND (open shell|emu|lanthanide|many valence)`. Returned 2606.04868, 1805.11265, 1805.06615 and 1612.00747.
  14. `abs:kilonova AND (laboratory|experimental|FTS) AND spectra`. Returned 2507.07785 and 2606.11748.
  15. `(Nd III|Er III|U II|U III|Pr III|Sm III) AND (levels|spectrum)`. Returned 2408.07830 and 2307.09282 (experimental Nd III).
  16. `(quantum algorithm|quantum computer|fault-tolerant) AND (opacity|opacities|atomic spectra|line list)`. The only relevant hit was 2607.02811.
- Abstract and HTML pages fetched to verify: 2501.13286 (abstract and full HTML), 2507.07785, 2302.01780, 2408.02731, 2607.02811, 1904.08781, 2412.16688, 2502.13250, 2209.12759, 2606.04868, 2202.09245, 2306.17612.
- Local calculation (a trivial one): binomial determinant counts for active spaces (section 2, Q3).

## 1. Verified sources used

| Ref | ID / DOI | What it establishes (verified from the abstract or HTML) |
|---|---|---|
| Kato, Tanaka, Gaigalas, Kitoviene, Rynkun, MNRAS 535, 2670 (2024) | arXiv:2501.13286 | Better potential optimization and a larger configuration set lower the level distributions, which raises the opacities by x3-10 per element but only **x1.5 for a Ln mixture**. The new opacities agree with ab initio GRASP2K. Opacity is "controlled by transition arrays among several configurations", so an accurate *energy distribution* is what matters. From the HTML: transitions per ion are Pr II 418K (62.5K strong), Nd II 4.0M (67.9K), Sm II 69.9M (35.7K) and Gd II 158M (32.0K), with strong meaning gf e^{-E/kT} > 1e-5 at 5000 K. The HULLAC/GRASP factor of ~3 at 5000-10000 A traces to the higher 4f10 5d2 configuration energy. Mixture differences are 1.2-1.6. Median level errors of 12-17% (42% for Gd II) were adequate for opacity. |
| Flors et al., MNRAS (2023), doi:10.1093/mnras/stad2053 | arXiv:2302.01780 | FAC and HFR, with calibration, for Nd and U. Opacities agree well where many experimental levels exist. The spread is large only where there are few levels. The U opacity is about 2x the Nd opacity. |
| Flors, da Silva, Marques, Sampaio, Martinez-Pinedo (2025) | arXiv:2507.07785 | Calibrated FAC for La-Yb II-III: 28 ions, 146,856 levels, 28.69M transitions, 66,591 with experimentally calibrated wavelengths. Opacities agree with prior calculations for well-measured ions. |
| da Silva et al. (2025) | arXiv:2502.13250 | Bayesian-optimized FAC brings level errors from 20-60% down to at most 10%. About 90% of wavelengths fall within 10% (Pr and Er ions). Individual transition probabilities still carry about 1.1-1.4 dex RMS error. |
| Fontes et al. (2020) | arXiv:1904.08781 | The line-binned, area-preserving (optically thin sum) opacity agrees with continuous Monte Carlo Sobolev and with expansion-opacity spectra. The paper also studies convergence in the number of lines. |
| Fontes et al., MNRAS, doi:10.1093/mnras/stac2792 | arXiv:2209.12759 | CI actinide opacities for Z = 89-102. Ejecta mass and velocity matter more than the actinide abundance distribution. |
| Deprince et al., A&A 696, A32 (2025) | arXiv:2412.16688 | HFR for every element from Ca to Lr. On average, lanthanides are not the dominant opacity source. |
| Brethauer et al. (2024) | arXiv:2408.02731 | The choice of atomic dataset shifts the inferred lanthanide fraction by about 1 dex (a factor of about 6 in total Ln for GW170817). Thermalization shifts inferred masses by 20-50%. |
| Pognan, Jerkstrand, Grumer, MNRAS, doi:10.1093/mnras/stac1253 | arXiv:2202.09245 | NLTE excitation departures reach factors of 2-10 in expansion opacity a few days after merger. With NLTE ionization included, opacities can change by orders of magnitude. |
| Shingles et al., ApJL 954, L41 (2023) | arXiv:2306.17612 | 3D line-by-line transport with millions of lines. Line-by-line treatment replaces binned opacities to capture fluorescence and to attribute features. Calibrating the Sr/Y/Zr wavelengths changes the spectra substantially. |
| Gaigalas et al. (2024) | arXiv:2405.05463 | GRASP2018 for Ce III: ground-configuration RMS of 2732 cm-1 and excited-configuration RMS of 618 cm-1. |
| Kitoviene et al. (2025) | arXiv:2502.20424 | GRASP2018 for Th III: RMS of 436 cm-1 against experiment. |
| Gaigalas et al. (2019) | arXiv:1901.10671 | Nd II-IV MCDHF/RCI: 3-11% against NIST. |
| Radziute et al. (2020) | arXiv:2002.08075 | Pr II-Gd II GRASP2K: 6-12% on energy levels. |
| Ding et al. (2023, 2024) | arXiv:2307.09282, 2408.07830 | Fourier transform spectroscopy of Nd III: 105 and then 116 new experimental levels at 1e-3 to 0.3 cm-1. The experimental route keeps closing the gap. |
| Reitsma, Sheil, Versolato, Kahl, Berengut (2026) | arXiv:2606.04868 | For Sn12+, a complex open shell, saturating the n=4 CI plus core-valence correlation on CPU HPC resolves a long-standing blueshift in a *binned* EUV emission spectrum. This is a classical precedent for exactly this kind of observable. |
| Cheung, Kozlov, Porsev, Safronova, Tupitsyn, Bondarev (2024) | arXiv:2410.06680 | pCI: MPI-parallel CI+MBPT and CI+all-order with QED, for high-precision atomic structure. |
| Bilous, Cheung, Safronova (2024, 2025) | arXiv:2408.00477, 2503.01379 | Neural-network configuration selection for large-scale atomic CI in pCI. |
| Kahl, Berengut (2019) | arXiv:1805.11265 | AMBiT particle-hole CI+MBPT for open shells with N > 5 valence electrons. |
| Geddes et al. (2018) | arXiv:1805.06615 | Saturated CI for atoms with many valence electrons. |
| Pototschnig et al. (2021) | arXiv:2107.11234 | For YbF, Fock-space CC cannot put 4f13 and 4f14 configurations in one active space. This is a real single-reference/FSCC limitation for open f shells. |
| Pathak, Kononov, Baczewski (2026) | arXiv:2607.02811 | Quantum opacity protocol (interaction picture, photonic register) for dense solar iron. It does not cover lanthanides, low-density bound-bound opacity or kilonovae, and its abstract gives no classical baseline. |

[UNVERIFIED, general background only, not load-bearing] Kilonova ejecta velocities are about 0.1-0.3c; Pian et al. 2017 (arXiv:1710.05858, listing seen in query 1) cites 0.2c. This implies Doppler smoothing of Delta-lambda/lambda of about 0.1. The Brewer (1971) systematics of 4f^n versus 4f^{n-1}5d configuration energies across the series are cited from memory and are unverified.

## 2. Audit question answers

### Q1. Decomposing the code-to-code opacity spread
- **Configuration completeness and potential choice:** This is the dominant term. Kato+ 2024 shows that changing only the configuration set and the potential optimization moves single-element opacities by x3-10. The HULLAC/GRASP factor of ~3 traces to one configuration-average energy (4f10 5d2).
- **Calibration against experimental levels:** Where many experimental levels exist, FAC, HFR, GRASP and HULLAC agree (Flors 2023, 2025). The spread is large only for ions with few experimental levels: U II, many doubly ionized ions and actinides.
- **Correlation within a fixed configuration space (the "solver" term):** This is minor for the binned opacity. Once the configuration-average positions are right, the semi-empirical HULLAC and ab initio GRASP2K opacities agree (Kato 2024). For the mixture the spread is 1.2-1.6.
- **Individual line strengths:** These are poor (1.1-1.4 dex RMS, da Silva 2025). In a bin, however, they sum over about 1e4-1e5 strong lines per ion, and the total per configuration pair is fixed by sum rules and transition-array moments.
- **Conclusion:** The one hard ab initio quantity is the set of **configuration-average energy offsets**, about O(10) numbers per ion. These come from differential core-valence (dynamic) correlation of 4f versus 5d/6s/6p, which spans hundreds to thousands of virtual spinors and is handled by CI+MBPT, CI+all-order or calibration. Exact diagonalization of a 60-120-spinor active space does not target it (L6). **Kill condition met (L6/L7).**

### Q2. Can a spectral-function readout replace line-resolved Sobolev data?
- For LTE binned opacity, yes in practice. Fontes+ 2020 shows the line-binned, optically-thin, area-preserving opacity, which is a binned dipole spectral function, reproduces MC-Sobolev spectra. This point goes *in favour of* the proposal's readout.
- It cuts the other way on two counts:
  - (a) A linear, low-resolution, thermally averaged observable is exactly the kind that moments, transition-array statistics and KPM/stochastic-trace methods converge cheaply.
  - (b) The frontier has moved to line-by-line NLTE transport (Shingles+ 2023, ARTIS; Pognan+ 2022; Collins+ 2026, arXiv:2604.22671, listing only). That needs individual transitions, NLTE populations (so rho is not rho_T) and wavelength-accurate lines for feature identification (Sr II, Ce III, Gd III, Te III). A Tr[rho_T mu delta(H-E-w) mu] readout cannot supply these.
- The proposal's selling point is that cost does not scale with 1e6-1e8 lines. That targets a non-bottleneck: classical codes already enumerate 158M lines for Gd II (Kato 2024), and only about 3e4-7e4 of them are strong.

### Q3. Classical twin and where exact classical diagonalization fails
Raw determinant counts C(n_spinors, n_valence), before M_J and parity blocking (which gives roughly /10-50):

| Ion (valence e-) | 34 spinors | 60 | 82 | 100 | 120 |
|---|---|---|---|---|---|
| Nd II, U II (5) | 2.8e5 | 5.5e6 | 2.7e7 | 7.5e7 | 1.9e8 |
| Gd II (9) | 5.2e7 | 1.5e10 | 2.9e11 | 1.9e12 | 1.1e13 |
| Tb II (10) | 1.3e8 | 7.5e10 | 2.1e12 | 1.7e13 | 1.2e14 |
| Er III (12 particles) | 5.5e8 | 1.4e12 | 8.3e13 | 1.1e15 | 1.1e16 |

- The proposal's own validation ions (La II, Ce II), its flagships (Nd II, U II) and the whole light half of each series are **exactly solvable classically across the full proposed 60-120-spinor space** (at most about 2e8 determinants). Lanczos/KPM with stochastic thermal traces is routine at that size.
- Exact classical FCI fails only for mid-series ions with 9-12 valence electrons at 60 or more spinors (1e10-1e16), roughly n_f = 6-12 at 60+ spinors. Even there:
  - The minimal valence space (4f5d6s6p7s, about 34 spinors, 5e7-5e8 determinants) is exact classically.
  - Saturated/emu CI (1805.06615), CI+MBPT/all-order (AMBiT, pCI), NN-selected CI (2408.00477) and particle-hole formalisms for late lanthanides are available.
  - Nobody has shown that a *variational* treatment of spinors 35-120, as opposed to perturbative, changes the binned opacity. The Sn12+ precedent (2606.04868) shows classical saturated CI plus core-valence correlation already fixes systematic shifts in binned spectra of complex open shells.
- There is a genuine weakness: FSCC/single-reference CC handles near-degenerate 4f^n / 4f^{n-1}5d manifolds poorly (2107.11234). This is single-family, though. CI-based families do not share it.

### Q4. Model floor
- Current ab initio level errors: Th III 436 cm-1 and Ce III 618-2732 cm-1 (GRASP2018); 3-12% for Nd II-IV and Pr II-Gd II; 10% or better after Bayesian FAC optimization.
- Tolerances:
  - kT = 2100-7000 cm-1 for T = 3000-10000 K. A 1000 cm-1 error changes a Boltzmann factor by about x1.3-1.6.
  - Doppler smoothing is Delta-lambda/lambda of about 0.1 [UNVERIFIED], so line-position errors of about 10% are largely washed out in binned opacity.
  - Kato 2024 found 12-17% median errors adequate.
- Residual error is dominated by core-valence correlation outside any 60-120-spinor active space, plus Breit/QED and the effective-Hamiltonian truncation. None of these improve with an exact active-space solver. Solver error does not dominate model error: **L6 kill**.

### Q5. Resources
This is an order-of-magnitude estimate of my own and has not been checked against literature.
- Bins at 1% resolution are about 100 cm-1, or about 4.6e-4 Eh, so T is about 2e3 Eh^-1.
- With lambda of about 10-100 Eh for a 100-spinor relativistic atomic Hamiltonian, there are about 2e4-2e5 qubitization steps. At about 1e3-1e4 Toffoli per step, that is about 1e7-1e9 Toffoli per shot.
- Thermal-state preparation, or thermal typicality sampling, plus percent-level precision per bin over about 100 bins needs about 1e4-1e6 shots.
- Total: about 1e11-1e15 Toffoli per ion per T. Multiply by about 30 elements, 2-3 charge states and about 10 temperatures.
- The classical calibrated FAC run covering all 28 Ln II-III ions is a published, completed dataset (2507.07785). The quantum side would need fault-tolerant hardware to reproduce a quantity whose error budget is not solver-limited.

### Q6. Do inference systematics swamp opacity improvements (L5)?
Yes.
- NLTE excitation changes expansion opacity by x2-10 after a few days, and NLTE ionization by up to orders of magnitude (Pognan 2022). The quantum observable is defined with rho_T, the LTE assumption itself.
- Atomic-dataset choice gave about 1 dex in the inferred X_lan (Brethauer 2024), but the newer converged mixtures differ by only x1.2-1.6 (Kato 2024).
- Thermalization contributes 20-50% on masses. Ejecta mass and velocity dominate over the actinide pattern (Fontes 2022). Deprince 2025 finds lanthanides are not even the dominant opacity on average.
- The marginal decision value of a more exact correlated solver for LTE Ln opacity is below these systematics.

### Q7. Scoop risk
Scoop risk is low to moderate. In arXiv searches through 2026-09-28, the only quantum-algorithm opacity paper is 2607.02811 (Sandia group: Pathak, Kononov, Baczewski). It targets dense solar-iron opacity via the interaction picture and has no classical baseline in its abstract. That group has the machinery to extend it to bound-bound low-density opacity. No quantum kilonova or quantum lanthanide-opacity paper was found. The novelty classification (scoped category B) survives, but novelty does not rescue the candidate.

## 3. Lesson-filter scorecard
- **L1, false hardness:** Hardness is asserted from the line count (1e6-1e8), which is not the bottleneck. Classical codes already enumerate 1.6e8 lines per ion.
- **L2, solver equivalence:** At the binned-opacity level, calibrated semi-empirical codes and ab initio GRASP agree (1.2-1.6 for the mixture). The solver is not load-bearing.
- **L3, classical landscape / quadratic:** Not directly applicable. The observable is a linear thermal response, which is classically cheap to moment-expand.
- **L5, information vs computation:** The informative quantities (feature identification, NLTE populations) need line-resolved, NLTE, experimentally calibrated data that the proposed readout does not provide.
- **L6, model floor:** Fails. The dominant error sits in configuration-average energies set by dynamic core-valence correlation outside the active space, and in NLTE.
- **L7, strongest classical attack:** Calibration against FTS experiment (Ding+), Bayesian-optimized FAC, CI+MBPT/pCI/AMBiT, saturated CI (the Sn12+ precedent) and KPM on the minimal valence space.

## 4. Cheapest decisive classical kill experiment (laptop-scale, CPU-hours)
1. **Data:** Use the public calibrated FAC line lists (2507.07785) for Nd II, Gd II (mid-series, worst case) and U II (actinide, few experimental levels, from 2302.01780 data).
2. **Perturbation study (solver-error proxy):**
   - (a) Shift each configuration-average energy by +/-delta, with delta from 250 to 3000 cm-1.
   - (b) Apply log-normal scatter of 1 dex to individual gf values while preserving each configuration-pair total strength (sum rule).
   - (c) Apply random level jitter of +/-epsilon within configurations.
   - Recompute the Sobolev expansion opacity and the line-binned opacity at t = 1-7 d, rho of about 1e-13 to 1e-15 g cm^-3 and T = 3000-10000 K. Then recompute Planck/Rosseland means and a one-zone or 2D light curve, from which to infer X_lan.
3. **Comparator:** The NLTE-induced opacity change (x2-10 after a few days; Pognan 2022) and the thermalization uncertainty.
4. **Kill criterion:**
   - If (b) and (c) change the binned opacity by less than 20%, correlation within a fixed configuration space is irrelevant. Averaging over 3e4-7e4 strong lines makes this very likely.
   - If the delta* that shifts inferred X_lan by x2 exceeds the current classical level error (about 500-1500 cm-1), exact solvers add no decision value.
5. **Optional second arm:** For Gd II, compare the binned opacity from minimal-valence (34-spinor) exact CI + CI+MBPT effective Hamiltonian + KPM against a 60-spinor NN-selected CI (pCI + Bilous NN). If the difference is below 20%, the larger (quantum-only) active space is not load-bearing.

## 5. Verdict: KILLED
A classical method convincingly handles the decision-relevant regime:
- LTE binned expansion opacities for Ln/An II-III at the accuracy that kilonova inference can use.
- The residual spread comes from configuration completeness, configuration-average energies (dynamic correlation outside any feasible quantum active space, fixed by calibration or experiment) and NLTE. It does not come from active-space solver error.
- The proposed quantum observable is also the LTE thermal quantity that NLTE work shows to be inadequate after a few days.
- The light-ion validation and flagship targets (La, Ce, Nd, U) are exactly classically diagonalizable across the entire proposed active space.

## 6. Residual lane (not a quantum lane as posed)
The only open scientific gap is *ab initio* configuration-average energies for mid-series doubly-ionized lanthanides and for actinide ions lacking experimental levels. There the spread between codes is large (Flors 2023). It is a dynamic-correlation / effective-Hamiltonian problem, and a better classical answer is CI+all-order/pCI with NN selection, or new FTS measurements. A quantum formulation would have to be recast as a strongly correlated effective-Hamiltonian problem in which exact treatment of the 4f^n / 4f^{n-1}5d near-degeneracy beyond classical CI is shown to change the configuration offsets by more than about 1000 cm-1. No evidence of that was found.
