# Discovery lens: AMO / light-matter (2026-09-28)

Status: FINAL for this pass. Nothing here is a research result; these are literature-scoped candidates.

## Search infrastructure and scope
- The session WebSearch budget was already used up (200/200). OpenAlex anonymous search returned HTTP 429. The arXiv export API worked for about 30 queries and then returned 429.
- Sources actually used: arXiv export API (boolean queries on the abstract field), arXiv abstract pages via WebFetch, and the Crossref API.
- Scope of every "no paper found" statement below: arXiv abstract-field boolean search plus targeted Crossref lookups, through 2026-09-28. Journal-only work without an arXiv copy (JQSRT, ApJS, J. Phys. B, ADNDT) can be missed. The absence of a hit is not proof that no work exists.

## Query log
arXiv export API, abs: field unless noted. "QC terms" means ("quantum computer" OR "quantum algorithm" OR "quantum computing").
1. "quantum computer" AND vibrational AND anharmonic -> 10 hits (2605.12866, 2009.05066, 2504.10602, 2204.08571, 2503.23983, ...)
2. "quantum algorithm" AND opacity -> 2607.02811 (Pathak, Kononov, Baczewski: astrophysical opacities on a QC, solar iron)
3. "quantum computer" AND "line list" -> nothing relevant
4. quantum AND "dipole autocorrelation" AND "quantum algorithm" -> 0
5. "quantum algorithm" AND rovibrational -> 2510.19062
6. (QC terms | digital quantum simulation) AND (superradiance | collective radiance | subradiance) -> 2201.11597, 2603.12563, 2412.14285
7. "optical lattice clock" AND "dipole-dipole" AND (density or collective shift) -> 0. Relaxed to "optical clock" AND "dipole-dipole" -> 2303.05613
8. superradiance AND many-body AND "atomic arrays" -> 2211.11895, 2305.19829, 2604.11795, 2110.11288
9. "vibronic spectra" AND "boson sampling" -> 1412.8427, 2202.01861, 2502.12882, 2507.19442, 2508.03943
10. vibronic AND "quantum algorithm" AND anharmonic -> 1812.10495, 2510.10495
11. QC terms AND (photoionization | strong-field | attosecond | high-harmonic) -> no quantum-algorithm paper on correlated multi-electron ionization
12. QC terms AND "electron scattering" -> 2507.05514
13. QC terms AND ("double ionization" | "multiphoton ionization" | "tunnel ionization") -> nothing relevant
14. "first quantized" AND quantum AND (ionization | continuum | "absorbing boundary") -> 2105.12767, 2602.20234
15. ti:quantum + (algorithm | computer | computing) AND (photoionization | "photoelectron spectrum/spectra") -> nothing relevant
16. "nonsequential double ionization" AND many-electron AND time-dependent -> 1411.3082
17. QC terms AND ("pressure broadening" | "line shape parameters" | "line mixing") -> 0
18. QC terms AND ultracold AND ("reactive scattering" | sticky | "collision complex") -> 0
19. QC terms AND ("reactive scattering" | "S-matrix") AND chemical -> 2403.03052, 2603.26881
20. "pressure broadening" AND close-coupling -> 1304.4804, 1009.1699, 2606.07039, 2201.04530, 2510.03327
21. Ir17+ -> 1912.08714, 2502.01112, 2309.07507, 1505.01019
22. QC terms AND relativistic AND atoms -> 2212.02058, 2406.04992, 2510.18005
23. kilonova AND opacity AND "atomic data" AND uncertain -> 2408.02731
24. quantum AND computer AND kilonova -> 0
25. lanthanide AND opacity AND (CI | "atomic structure calculations") AND kilonova -> 2209.12759, 1906.08914, 2507.07785, 2302.01780, 2502.13250
26. QC terms AND ("parity violation" | "parity nonconservation" | "EDM enhancement") -> 0. A Cs APV coupled-cluster query returned 0 because it was too narrow; not pursued.
27. tungsten AND ("R-matrix" | "electron-impact excitation") AND plasma -> 1805.02757, 2509.00878, 1506.03939
28. QC terms AND ("charge exchange" | "electron capture") AND ion -> 0
29. "charge exchange" AND "cross sections" AND X-ray AND "highly charged" -> 2105.04438. ti:"charge exchange" AND (XRISM | Hitomi | "solar wind") -> 2308.13647, 1901.07854, ...
30. "iron opacity" AND ("Z machine" | solar) -> 1509.08652, 1606.02731, 2607.21238, 2309.12073, 1704.03528
31. Crossref: RMT R-matrix with time dependence -> 10.1016/j.cpc.2019.107062. TD-CASSCF -> 10.1103/physreva.88.023402. TD-ORMAS -> 10.1103/physreva.91.023417
32. Crossref: triple photoionization of lithium, TDCC -> 10.1103/physreva.57.318 (TDCC for helium). The Li triple-photoionization paper itself was not retrieved: [UNVERIFIED]
33. Crossref: state-selective charge exchange of HCI with water, comet, X-ray (from 2018) -> 10.1093/mnras/stad040, 10.1016/j.adt.2021.101464, 10.3390/psf2026013004, 10.3390/atoms10030090
34. WebFetch of arXiv abstract pages: 2607.02811, 2507.05514, 1805.02757, 2510.19062, 2202.01861

## Filter applied: lessons from the protein work
Each candidate had to pass these checks:
- (a) The Hamiltonian is known well enough that solver error dominates model error (lesson 6).
- (b) The quantum output is a physical observable that is sampled or estimated directly, not an argmin over a classical landscape (lesson 3).
- (c) An exact classical reference exists at small size and there is a scaling variable (lesson 1).
- (d) The strongest classical methods are named (lesson 7).
- (e) The observable carries decision-relevant information in the regime where it is classically hard (lesson 5).

---------------------------------------------------------------------

## CANDIDATE 1: Correlated multi-electron photoionization and strong-field ionization, sampled photoelectron momentum distributions (initial verdict: PLAUSIBLE; best of this lens)
- Domain: attosecond / strong-field / XUV-XFEL atomic and molecular physics.
- Input: atom or small molecule with eta active electrons (nonrelativistic Coulomb Hamiltonian); laser or XUV/X-ray pulse (intensity, wavelength, duration, polarization; dipole approximation).
- Output: multi-electron photoelectron momentum distributions (joint p1, p2, p3), double- and triple-ionization yields and ratios, and angular correlations. These are the quantities COLTRIMS reaction microscopes and XFEL end-stations measure.
- Practical use: interpretation and design of attosecond and XFEL experiments; multiple-ionization and damage models for XFEL single-particle imaging; benchmarks for the approximate TD methods used across the field. The practical pull is moderate and science-facing more than industrial.
- Quantum mechanism: first-quantized real-space grid simulation of eta electrons, with 3*eta*log2(N) system qubits. The kinetic term is diagonal after a QFT and the pairwise Coulomb terms are evaluated coherently with arithmetic, in the style of Su et al. first-quantized chemistry (2105.12767). The laser coupling is time-dependent (interaction picture or time-dependent product formulas). The continuum is handled with a large box, or with a dilated or ancilla-assisted absorbing boundary. The readout is a measurement of the electron registers in momentum space after a QFT, which directly draws samples from the joint photoelectron momentum distribution. No tomography and no argmin are involved; the physical output is a sample stream.
- Replaced classical computation: full-dimensional 3*eta-D TDSE propagation. The grid classically costs N^(3*eta) memory; the quantum register costs 3*eta*log N qubits. For eta >= 3 this is an exponential memory separation with polynomial gate cost. That is a Hamiltonian-simulation speedup, not a quadratic search speedup.
- Classical SOTA to beat:
  - Exact full-dimensional 2-electron TDSE (TDCC, Pindzola-Robicheaux PRA 57, 318 (1998), doi:10.1103/physreva.57.318; the HELIUM code [UNVERIFIED])
  - RMT (R-matrix with time dependence, CPC 2020, doi:10.1016/j.cpc.2019.107062)
  - TD-CASSCF (doi:10.1103/physreva.88.023402) and TD-ORMAS (doi:10.1103/physreva.91.023417)
  - MCTDHF and TD-RASCI [UNVERIFIED specific refs]
  - tSURFF flux methods [UNVERIFIED]
  - TDDFT (known failure for the non-sequential double-ionization knee [UNVERIFIED])
  - Classical-trajectory Monte Carlo
- Why it is classically hard: an exact grid is exponential in eta. Every scalable classical method truncates correlation, either through a restricted active space or through a single-electron outer region (RMT's outer region carries one ionized electron). For three or more simultaneously continuum electrons, such as triple photoionization of Li or non-sequential multiple ionization of Ne and Ar, no exact full-dimensional classical reference exists.
- Model floor: good. The Coulomb Hamiltonian and the dipole approximation are essentially exact for these experiments, so solver error dominates. Relativistic effects are negligible for light atoms.
- Novelty: category B.
  - Nearby first-quantized dynamics work: 2105.12767 (chemistry), 2602.20234 (EUV electron cascades), 2308.12352 (stopping power, Rubin et al. PNAS 2024; taken from the task context, not rechecked).
  - Nearby scattering work: 2403.03052 (reactive scattering S-matrix on a QC), 2603.26881 (wave-packet reactions).
  - Queries 11, 13, 14, 15 and 16 found no quantum-algorithm study of correlated multi-electron photo- or strong-field ionization, and no quantum-vs-classical comparison against RMT, TD-CASSCF or TDCC.
- Benchmark ladder, with eta as the scaling variable:
  - He (eta=2), where classical is exact: a validation rung.
  - Li triple photoionization (eta=3): classical TDCC with angular truncation exists [UNVERIFIED].
  - Be and Ne multiple ionization (eta=4-6): only approximate classical methods exist.
  - The second scaling variable is box size L, which grows with wavelength (ponderomotive excursion).
  - The FULL-vs-ABLATION test replaces the quantum propagator with the best-converged TD-ORMAS or RMT and asks which observables change beyond the experimental error.
- Rough resources (my estimate, UNVERIFIED): XUV single-photon triple ionization needs a box of about 200 a.u. per dimension at 0.2 a.u. spacing, i.e. about 10 qubits per dimension. That gives about 90 system qubits for eta=3, and about 200-400 logical qubits with ancillas. The Hamiltonian norm is about 1e3 a.u. (grid kinetic energy) over t ~ 200-1000 a.u. With first-quantized block encodings this is roughly 1e9-1e10 Toffoli per shot. Strong-field IR needs boxes about 10x larger and times about 10x longer.
- Main failure risks:
  1. Shot cost. Rare channels (triple ionization is about 1e-3 to 1e-5 of events) need 1e4-1e6 shots or amplitude amplification, which gives only a quadratic gain. The total may reach 1e14-1e16 Toffoli.
  2. Converged TD-ORMAS or RMT may already match experiment within its error bars (the information-vs-computation risk).
  3. Absorbing boundaries are non-unitary, and grid Coulomb cusps need fine grids.
- Initial verdict: plausible.

## CANDIDATE 2: Kilonova lanthanide and actinide expansion opacities from a thermal dipole spectral function (initial verdict: PLAUSIBLE-WEAK)
- Domain: atomic data for multi-messenger astronomy (r-process nucleosynthesis).
- Input: singly and doubly ionized lanthanides and actinides with open 4f or 5f shells (e.g. Nd II, Er III, U II); ejecta temperature 3000-10000 K; wavelength grid 0.3-3 um at a resolution of about 10-100 Angstrom.
- Output: frequency-binned bound-bound (expansion or Sobolev) opacity kappa(lambda, T). This is Tr[rho_T mu delta(H - E - omega) mu], a thermal spectral function. It is not a line list.
- Practical use: radiative-transfer modelling of kilonova light curves and spectra (GW170817 / AT2017gfo, and future LIGO-Virgo-KAGRA events). According to 2408.02731, differences in atomic data change inferred lanthanide mass by about 1 dex in lanthanide-rich ejecta and by about 6x for GW170817, and change ejecta mass by 25-40%. That bears directly on the question of whether mergers dominate r-process production.
- Quantum mechanism:
  - A second-quantized relativistic (Dirac-Coulomb or X2C) active-space Hamiltonian, e.g. 4f, 5d, 6s, 6p plus correlating shells, about 60-120 spinors.
  - The thermal state is prepared by canonical typicality or a Gibbs-state method, followed by dipole-dipole correlation C(t) = <mu(t) mu(0)>_T via Hamiltonian simulation and a Hadamard test, or by QPE-based spectral sampling.
  - Alternatively, the photon-register momentum readout of Pathak et al. (2607.02811), which ties qubit count to spectral range and resolution.
  - The quantum cost scales with spectral resolution and correlation space, not with the number of lines (about 1e6-1e8 per ion). This replaces classical CI diagonalization plus line enumeration.
- Classical SOTA to beat:
  - FAC with calibration (2507.07785)
  - HULLAC and LANL CI codes (2209.12759; Fontes et al.)
  - GRASP MCDHF / RCI
  - HFR (Cowan) with experimental level fits
  - AMBiT-style CI+MBPT [UNVERIFIED for lanthanide opacities]
  - Kernel-polynomial or Lanczos spectral functions on CI matrices. This is the fair classical twin, because it also avoids enumerating lines.
- Why it is classically hard: open 4f^n shells with n = 3-11 plus 5d/6s/6p give very large numbers of CSFs. Classical codes truncate configuration sets and correlation. 2507.07785 needs experimental calibration and has calibrated wavelengths for only about 66,591 transitions across all Ln II/III. Ions with few experimental levels (most doubly ionized ions, actinides) remain uncalibrated.
- Model floor: fairly good. Ejecta are low-density, so the isolated-ion Hamiltonian is valid. Breit and QED terms are small relative to the 10-20% level errors that matter for binned opacity. However, NLTE effects and the expansion-opacity formalism add model uncertainty, and thermalization efficiency moves mass estimates by 20-50% (2408.02731).
- Novelty: category B. The nearest work is 2607.02811, a quantum opacity protocol for dense-plasma solar iron. Query 24 (quantum AND computer AND kilonova) returned 0 hits, and query 23 returned no quantum work. The kilonova regime is materially distinct: neutral to doubly ionized open-f-shell ions at low density with LTE/NLTE ejecta, versus hot dense Fe L-shell plasma.
- Benchmark: scale by active-space size, or by f-occupation n across the lanthanide series. Validate on La II / Ce II, where experimental levels exist. Test on Er III and U II against calibrated FAC and large CI with KPM.
- Main failure risks:
  1. Binned opacities may be insensitive to correlation beyond what calibrated CI already captures. The spread in 2408.02731 may come from differences in configuration completeness, not from correlation exactness. That would be the lesson-5 risk.
  2. Line identification needs accuracy of 0.1% or better, which is below the ab initio model floor.
  3. Thermal-state preparation cost.
  4. A per-ion cost at FeMoco scale is multiplied by about 30 ions and several charge states.
- Initial verdict: plausible-weak.

## CANDIDATE 3: Solar-interior iron opacity (initial verdict: WEAK)
- Input: Fe at T of about 180-190 eV and n_e of about 1e22-1e23 cm^-3, with the plasma environment.
- Output: monochromatic opacity and the Rosseland mean.
- Practical use: the solar abundance / helioseismology problem, and pulsating-star models.
- Quantum mechanism: 2607.02811 simulates the electron and photon subsystems in first and second quantization, uses interaction-picture Hamiltonian simulation, and reads out momentum-resolved photons.
- Classical SOTA to beat: OP, OPAL, SCO-RCG, ATOMIC/LANL, and R-matrix with core excitations (1606.02731).
- Novelty: category C. The quantum method exists with logical resource estimates (2607.02811), but I found no quantum-vs-classical advantage study.
- Main failure risk: model floor. 2607.21238 attributes a 25-30% L-shell opacity enhancement to plasma screening plus CI effects, so the plasma-environment model is itself uncertain. The Z-machine measurements (Bailey et al. 2015) are also disputed. An exact solve of an uncertain plasma model repeats the FeMoco-type lesson.
- Initial verdict: weak. It is kept as a comparison anchor for candidate 2.

## CANDIDATE 4: High-temperature absorption cross sections of 6 or more atom molecules for exoplanet retrievals, from a thermal dipole autocorrelation (initial verdict: WEAK)
- Input: ab initio PES and dipole moment surface (DMS) of, for example, C2H4, C2H6 or CH3OH-class molecules; T = 1000-2500 K.
- Output: sigma(nu, T) at the R of about 100-3000 used by JWST. It is not a line list.
- Quantum mechanism: DVR / Walsh-Hadamard-QROM rovibrational block encoding (2510.19062), used for thermal C(t) instead of individual QPE eigenvalues.
- Classical SOTA to beat: TROVE and DVR3D variational line lists (ExoMol) [UNVERIFIED specific refs], MCTDH / ML-MCTDH, vibrational DMRG, VCI with pruning, and quantum-corrected classical MD spectra.
- Novelty: 2510.19062 compares only against classical variational methods ("30,000 years"), with no MCTDH or vDMRG baseline, which places it in category D. The thermal cross-section formulation is a distinct subsection; queries 3-5 found no quantum paper on it.
- Main failure risks:
  1. At high T and low R, approximate classical methods (hot-band extrapolation, super-lines, quantum-corrected MD) may suffice.
  2. High-resolution cross-correlation needs line positions to about 0.01 cm^-1, which is below the PES accuracy floor, so an exact solver does not help there.
- Initial verdict: weak.

## CANDIDATE 5: State-selective multi-electron charge exchange of solar-wind highly charged ions with molecular targets (initial verdict: PLAUSIBLE-WEAK)
- Input: projectile (O8+, O7+, C6+, Ne9+, ...) at 0.1-10 keV/u; target (H2O, CO2, CO, or H2 for validation).
- Output: n- and l-resolved single and multiple capture cross sections, followed by cascade to X-ray line ratios (e.g. O VII forbidden-to-resonance ratios, O VIII Lyman series).
- Practical use: modelling solar-wind charge exchange X-ray emission from comets, planetary exospheres and the heliosphere. This emission is a foreground for XRISM, SMILE and LEXI-class soft X-ray observations and is also used as a diagnostic.
- Quantum mechanism: time-dependent many-electron simulation in the semiclassical impact-parameter picture (classical straight-line nuclei). The electrons are second-quantized on a two-centre basis extended to Rydberg n of about 4-7, or treated first-quantized on a grid. Capture channels are read out by projection with QPE onto projectile-centred states. The scaling variable is the number of active target electrons.
- Classical SOTA to beat: MOCC, AOCC, CTMC (see 10.3390/atoms10030090), multichannel Landau-Zener, TDDFT / independent-electron models, and ADNDT tabulations (10.1016/j.adt.2021.101464). Nearly all comet modelling uses H or H2 targets or scaled data (10.1093/mnras/stad040).
- Why it is classically hard: multiple capture from 8-10-electron molecular targets into high-n projectile states, with autoionization, needs correlated many-electron time-dependent treatment. Classical methods either truncate to one or two active electrons or treat the electrons classically (CTMC, which gets l-distributions wrong at low velocity [UNVERIFIED]).
- Model floor: fair. The straight-line impact-parameter approximation holds at keV/u; the molecular target geometry and orientation averaging add work.
- Novelty: category A. Query 28 (quantum AND charge exchange / electron capture) returned 0 hits.
- Main failure risks:
  1. Astrophysical line-ratio uncertainty may be dominated by solar-wind composition and charge-state distribution (2308.13647), not by cross sections.
  2. Independent-electron models may already be adequate for observed ratios.
  3. The basis size for high-n capture makes gate counts large.
- Initial verdict: plausible-weak.

## CANDIDATE 6: Electron-impact excitation and ionization of open-shell tungsten (W I to about W5+) for fusion erosion diagnostics (initial verdict: WEAK)
- Input: electron energy 1-100 eV and the W target (5d^4 6s^2, and related).
- Output: excitation and ionization cross sections, and hence S/XB coefficients for the W I 400.9 nm line and alternative diagnostic lines.
- Practical use: gross W erosion measurements in ITER-class divertors.
- Quantum mechanism: R-matrix inner-region (N+1)-electron eigenproblem on a QC, using VQE/QPE for the R-matrix boundary amplitudes (the method of 2507.05514), extended to a heavy relativistic open-shell target.
- Classical SOTA to beat: Dirac R-matrix (DARC; 1805.02757), B-spline R-matrix, and relativistic distorted-wave FAC (2509.00878).
- Novelty: category B. The quantum R-matrix method exists only for e- + H2 (2507.05514, which states it is the first formulation of the R-matrix inner-region problem on a QC). Queries 12 and 27 found no quantum work on W.
- Main failure risks:
  1. The classical wall is polynomial (close-coupling expansion size), not clearly exponential.
  2. Collisional-radiative and plasma-model uncertainty may dominate.
  3. VQE-based inner-region solvers bring back the optimizer failure modes seen in the protein work.
- Initial verdict: weak.

---------------------------------------------------------------------

## KILLED IDEAS (with reasons)
1. **Optical-lattice clock dipolar / cooperative Lamb shifts.** 2303.05613 (JILA, 87Sr, 3D lattice) reports "high accuracy of the modeled response" and shows ensemble-averaged shifts can be suppressed below the systematic budget. The clock is itself the analog simulator and measures its own shift, and semiclassical methods (DTWA, 2305.19829; cumulants, 2211.11895) suffice at mHz scale. There is no decision-relevant classical wall.
2. **Many-body super- and subradiance in 2D/3D arrays (general dynamics).** This is category C: quantum circuits already exist (2201.11597, 2603.12563) and site-resolved analog experiments exist (2604.11795). Classical DTWA, cumulant and MPS methods cover most regimes, and no practical user needs a digital QC prediction here.
3. **GBS vibronic spectra.** Category E: Oh et al., Nat. Phys. 20, 225 (2024), arXiv:2202.01861, give a quantum-inspired classical algorithm, and 2502.12882 gives classical linear-optics expectation values. Anharmonic and non-Condon variants (1812.10495, 2510.10495) meet ML-MCTDH, and prior-week searches already covered LVC vibronic cases.
4. **Pressure broadening, line mixing and collision-induced absorption for HITRAN-type data.** Category A (query 17 returned 0 hits), but the classical wall is polynomial (close-coupling channels N^3). CC calculations are routine (2510.03327, 2606.07039), and CS and requantized-MD approximations work. A quantum linear-systems speedup would be at most polynomial, and the gain is lost to fault-tolerance overhead (lesson 3).
5. **Ultracold molecule "sticky" collisions and reactions.** Category A/B (reactive-scattering QC papers exist: 2403.03052, 2603.26881). Ultracold observables depend on PES details below 0.1%, so the model floor dominates (lesson 6). Universal loss rates are already classically predicted.
6. **Highly charged ion clock transitions (Ir17+ class).** Classical CI+MBPT (1912.08714) and KRCI/FSCC (2502.01112) now agree and explain the earlier puzzle of missing E1 lines. The remaining error is QED and Breit terms (model floor), not correlation.
7. **Atomic parity violation / EDM enhancement factors.** No QC paper was found (query 26), but the theory target (about 0.1-0.5%) sits at the QED radiative-correction model floor, and the practical user base is narrow. Not searched in depth.
8. **Photodissociation cross sections for atmospheric chemistry.** For small molecules, MCTDH on MRCI PES is classically feasible. For large VOCs the bottleneck is sampling of nonadiabatic trajectories and PES model error, and quantum speedup applies only per electronic-structure point. Prior-week claimed work (PDT photodynamics) covers the nearby space.
9. **Franck-Condon branching ratios for laser-cooling polyatomics.** The vibrational problem is small enough for classical exact treatment, and the error comes from the ab initio PES (model floor).
10. **Waveguide/cavity QED many-photon transport through emitter chains.** MPS and cascaded-system methods work in 1D, and mean field works at large N (see the prior-week polaritonic kill). No practical decision depends on it.

## Verified citation list
Verified means an arXiv API record or abstract page, or a Crossref record, was retrieved in this session.
- arXiv:2607.02811 Pathak, Kononov, Baczewski, quantum opacities (solar Fe). [VERIFIED abs page]
- arXiv:2607.21238 Plasma screening + CI -> L-shell Fe opacity enhancement. [VERIFIED API]
- arXiv:2510.19062 Szczepanik, Nagy, Zak, DVR Walsh-Hadamard QROM rovibrational QPE. [VERIFIED abs page]
- arXiv:2202.01861 Oh, Lim, Wong, Fefferman, Jiang, Nat. Phys. 20, 225 (2024). [VERIFIED abs page]
- arXiv:2502.12882 classical expectation values in linear optics. [VERIFIED API]
- arXiv:1812.10495 Sawaya & Huh, vibronic quantum algorithm. [VERIFIED API]
- arXiv:2510.10495 uracil cation oscillator-qubit GQSP. [VERIFIED API]
- arXiv:2303.05613 mHz cooperative Lamb shifts in a Sr clock. [VERIFIED API]
- arXiv:2305.19829 DTWA collective radiance. [VERIFIED API]
- arXiv:2211.11895 cumulant superradiance. [VERIFIED API]
- arXiv:2604.11795 many-body super/subradiance experiment. [VERIFIED API]
- arXiv:2201.11597, arXiv:2603.12563 QC collective emission. [VERIFIED API]
- arXiv:2507.05514 Picozzi, Tennyson, Graves, Gorfinkiel, R-matrix VQE. [VERIFIED abs page]
- arXiv:1805.02757 Smyth et al., Dirac R-matrix W I. [VERIFIED abs page]
- arXiv:2509.00878 W I FAC distorted-wave. [VERIFIED API]
- arXiv:2403.03052, arXiv:2603.26881 reactive scattering on a QC. [VERIFIED API]
- arXiv:1912.08714, arXiv:2502.01112 Ir17+. [VERIFIED API]
- arXiv:2212.02058 BPDE fine structure; arXiv:2406.04992 relativistic VQE EDM. [VERIFIED API]
- arXiv:2408.02731 kilonova systematic uncertainties. [VERIFIED API]
- arXiv:2507.07785 calibrated lanthanide FAC data. [VERIFIED API]
- arXiv:2209.12759, arXiv:1906.08914, arXiv:2302.01780 kilonova opacity atomic data. [VERIFIED API]
- arXiv:2105.12767 first-quantized FT chemistry; arXiv:2602.20234 EUV. [VERIFIED API]
- arXiv:2510.03327 CO2-H2/He close coupling; arXiv:2606.07039 H2CO-He. [VERIFIED API]
- arXiv:2105.04438 n-resolved CX Ne8,9+; arXiv:2308.13647 SWCX compound cross sections. [VERIFIED API]
- doi:10.1016/j.cpc.2019.107062 RMT (CPC 2020). [VERIFIED Crossref]
- doi:10.1103/physreva.88.023402 TD-CASSCF (PRA 2013). [VERIFIED Crossref]
- doi:10.1103/physreva.91.023417 TD-ORMAS (PRA 2015). [VERIFIED Crossref]
- doi:10.1103/physreva.57.318 TDCC helium (Pindzola & Robicheaux 1998). [VERIFIED Crossref]
- doi:10.1093/mnras/stad040 CX HCI + H for comet C/1999 S4. [VERIFIED Crossref]
- doi:10.1016/j.adt.2021.101464 Ne-ion + H CX cross sections. [VERIFIED Crossref]
- doi:10.3390/atoms10030090 nl-selective CTMC CX. [VERIFIED Crossref]
- arXiv:2308.12352 Rubin et al. stopping power (PNAS 2024). [taken from task context; not re-verified here]
- Bailey et al. Nature 2015 Z iron opacity. [UNVERIFIED; referenced via 1509.08652]
- HELIUM code, MCTDHF, TD-RASCI, tSURFF, TROVE/DVR3D, AMBiT specifics. [UNVERIFIED]
