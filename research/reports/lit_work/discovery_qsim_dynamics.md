# Discovery lens: quantum simulation of dynamics / transport (2026-09-28)

Status: COMPLETE (2026-09-28). Literature evidence only; no computation run. Resource numbers marked [ESTIMATE] are my order-of-magnitude reasoning, not from the literature.

WebSearch budget exhausted at start of session (200/200). Searches via WebFetch against arXiv export API, OpenAlex, Crossref, arXiv abs pages.

## Query log
(appended below)

## Working hypotheses before search
- Infinite-temperature spin/charge diffusion constants: likely classically accessible (DAOE, Pauli propagation, tDMRG in 1D). Kill candidate.
- Low-T 2D Hubbard/t-J conductivity (sign problem + analytic continuation): candidate.
- Thermal Hall / thermopower via Kubo in frustrated/correlated 2D: candidate.
- Warm-dense-matter dynamic structure factor / conductivity (XRTS at NIF): candidate.
- Mott breakdown NESS: candidate with model-floor risk.

### Queries run so far (2026-09-28)
1. WebSearch "quantum computer transport coefficient diffusion constant Kubo conductivity..." -> budget exhausted (200/200).
2. arXiv API / OpenAlex / arXiv export via WebFetch -> HTTP 429 (shared rate limit).
3. Crossref "quantum computer Kubo conductivity Hubbard real-time" -> noise only.
4. OpenAlex title_and_abstract "quantum computer conductivity Hubbard" (2020+) -> 0.
5. OpenAlex "superdiffusion quantum processor spin transport" -> 1: doi:10.1103/j971-h796 (2026, superdiffusion resilience, Heisenberg chains w/ 2D interactions on quantum processor).
6. OpenAlex "thermal Hall conductivity quantum computer" -> 0 relevant.
7. OpenAlex "thermoelectric Seebeck quantum algorithm" -> 0 relevant.
8. arxiv.org/search abstract "electron-ion" equilibration quantum computer -> 2 hits, both classical (Brown & Singleton 0902.3180, 0707.2370); no quantum-computing paper.
9. arxiv.org/search "warm dense matter quantum computing" -> 2605.07722 (Pennati et al., Post-Moore roadmap: QC "potentially the most disruptive for WDM and ICF microphysics", no specific observable or resource estimate) [VERIFIED abs]; Babati 2606.02890 / 2606.02881 (kinetic-theory conductivity, classical); Liu 2510.10112 (Al conductivities to 1000 eV, mixed stochastic-deterministic DFT + Kubo).
10. arXiv abs 2605.07722 [VERIFIED].
11. arxiv.org/search "quantum algorithm Green-Kubo transport coefficients" -> 2605.30142 (Watanabe et al., KvN classical MD for Green-Kubo, amplitude estimation vs quantum shot sampling) [VERIFIED abs].
12. arXiv abs 2308.12352 (Rubin et al., stopping power, PNAS 121 (2024); ~100x FeMoco Toffolis) [VERIFIED].
13. arxiv.org/search "electron-ion coupling warm dense measurement" -> 1303.1402 (T. G. White et al., inhibited e-i coupling in strongly heated graphite, ~3x longer relaxation) [VERIFIED listing].
14. arxiv.org/search "electron-ion temperature relaxation ab initio" -> 1911.04622 (Simoni & Daligault, QMD e-i equilibration/friction; Kubo-Greenwood inapplicable for friction) [VERIFIED listing]; 1906.01610 Daligault theory [VERIFIED listing].
15. arxiv.org/search "conductivity Hubbard model quantum computer" -> no quantum computation of 2D Hubbard conductivity; 2602.03771 (Pham et al., spin/charge conductivity 2D FH via NLCE) [VERIFIED listing]; 2502.17171 (1D Hubbard Drude/Seebeck); 2106.01381 (Patel, T-linear resistivity invariant).

### Sibling coverage (do not duplicate)
- discovery_materials.md C3 thermal Hall of extended Kitaev models (2507.16558); C4 RIXS.
- discovery_algorithms.md C1 XRTS DSF of warm dense matter (first-quantized dynamics).
- discovery_claims.md C1-C6: 2D frustrated S(q,w), QSI, THz 2DCS, nickelate pairing, RIXS, MAS spin diffusion; kills for 1D FH quench (E), infinite-T diffusion (Pauli propagation), 2D FH quench demos.
- NOVEL_ADVANTAGE_SEARCH.md: doped Mott optical conductivity/Seebeck rated 1/5 (L4; DQMC + cold atoms).
16. arXiv abs 2510.26845 (Alam, Bosse et al., Google Willow 72-qubit 2D FH dynamics 6x6, polarons, VBS, stripes; validated vs exact + TN + operator propagation) [VERIFIED abs].
17. arXiv abs 2510.26300 (Alam, Bosse et al., Quantinuum H2 56-qubit 2D FH spin-charge separation, beyond exact; differs from TN predictions) [VERIFIED abs].
18. arxiv.org/search "impact ionization Mott insulator" -> classical only: 2412.05798 (Cheng, 1D ionic Hubbard, tLanczos), 2408.14822 / 2404.01729 / 2208.14752 (Gazzaneo, Arrigoni: Floquet/neq DMFT Mott photovoltaics), 2012.11257 / 1806.02570 (Wais: QBE vs DMFT), 1708.05011 (Sorantin), 1408.3425 (Werner, Held, Eckstein), 0911.4933 (Manousakis Mott PV proposal) [VERIFIED listing]. No quantum-computing paper.
19. arxiv.org/search "Floquet engineering exchange interaction Mott heating" -> 1801.00401 (Liu, perturbation theory, titanates) only.
20. arxiv.org/search "high harmonic generation Mott insulator" -> 30 classical/experimental hits (1D iTEBD 2010.13255, ladders 2407.01936, Floquet DMFT 1911.04183, Ca2RuO4 expt 2106.15478, Sr2CuO3 2508.00296, TDDMRP 2605.01388); no quantum computer.
21. arxiv.org/search "Kelvin formula thermopower" -> Kokalj & McKenzie 1410.0830 (triangular Hubbard, Kelvin formula semi-quantitative), Mravlje & Georges 1504.03860 (Sr2RuO4 DMFT consistent with Kelvin), Zlatic 1307.4800, Peterson & Shastry 1001.3423 [VERIFIED listing].
22. arxiv.org/search "iron opacity solar discrepancy" -> 2607.21238 (Zhou et al. 2026: plasma screening 14-17% + CI 10-20% -> 25-30% Fe L-shell opacity enhancement; refs Bailey Nature 517, 56 (2015); Nagayama PRL 122, 235001 (2019)) [VERIFIED abs].
23. arxiv.org/search "opacity quantum computer" -> no plasma-opacity quantum computation (A for this subproblem in arXiv abstracts).
24. arxiv.org/search "charged-particle transport coefficient comparison workshop" -> 2007.00744 (Grabowski et al., first workshop 2016: thermal/electrical conduction, e-i coupling, diffusion, viscosity, stopping; "Large variations ... when Coulomb coupling large or computational expense") [VERIFIED abs].
25. arxiv.org/search "second transport coefficient code comparison workshop" -> 2503.13014 (Wetta, average-atom dc conductivity; refs 2nd workshop LLNL July 2023) [VERIFIED listing].
26. arxiv.org/search "electron-electron collisions Kubo-Greenwood conductivity" -> 1401.0805 (Reinholz et al.: e-e collisions reduce conductivity in non-degenerate plasmas, negligible for liquid metals) [VERIFIED listing].
27. arxiv.org/search "bad metallic transport" Brown Bakr -> 1802.09456 (Brown et al., Science 363, 379 (2019), cold-atom 2D FH resistivity, linear-T, exceeds MIR; compared with FTLM/DQMC/DMFT authors) [VERIFIED listing].
28. arXiv abs 2503.20870 (Haghshenas, Chertkov et al., Quantinuum H2 digital magnetism, diffusion constant from relaxation of inhomogeneous state; Nature 2026) [VERIFIED abs].
29. arxiv.org/search "G1-G2 scheme nonequilibrium Green functions dense plasma" -> 2402.05214 (Schroedter, Bonitz group, G1-G2 fluctuations) [VERIFIED listing].
30. arxiv.org/search "moire Hubbard resistivity", "triangular lattice Hubbard model resistivity" -> 2605.13837 (Cao, DMFT Nagaoka supermetal), 2112.03080 (Zang, DMFT moire TMD, T-linear), 2103.09779 (Li et al., continuous Mott transition MoTe2/WSe2, expt), 2006.01707 (Vranic, DMFT+FTLM triangular vs square), 2004.02302 (Reymbaut) [VERIFIED listing]. No quantum-computer transport study.
31. Crossref: Hu, Militzer, Goncharov, Skupsky PRE 89, 043105 (2014) doi:10.1103/physreve.89.043105 [VERIFIED]; Desjarlais et al. PRE 95, 033203 (2017) doi:10.1103/physreve.95.033203 [VERIFIED].
32. arxiv.org/search "uniform electron gas quantum computer" -> 2203.17006 (Childs et al., real-space dynamics, finite T Coulomb), 1706.00023 (Babbush low-depth jellium), 2211.09133 (Low, Trotter UEG) [VERIFIED listing]; 2505.11150 (Chuna, PIMC dynamic properties of electron liquid), 2301.08444 (Dornheim, frequency moments from ITCF). No quantum computation of UEG/WDM transport coefficients.
33. arxiv.org/search "diagrammatic Monte Carlo optical conductivity Hubbard" -> 2509.00281 (Eom et al., DiagMC + analytic continuation, half-filled 2D Hubbard, strange diffusivity) [VERIFIED listing].
34. arxiv.org/search "Vucicevic conductivity Hubbard" -> 2501.19118 (Kovacevic, Ferrero, Vucicevic: numerically exact weak-coupling conductivity in the thermodynamic limit, no analytic continuation), 2208.04047 (hydrodynamics + transport, QMC + FTLM), 1811.08343 (high-T conductivity, vertex corrections), 2006.01707 [VERIFIED listing].
35. arxiv.org/search "photodoped Mott quantum computer" -> 0; "doublon dynamics quantum processor" -> 1 irrelevant (2507.22112).
36. OpenAlex batch (title_and_abstract, 2020+, 20 queries): relevant hits only: doi:10.1103/gz9n-v8ty (2026, "Probing hydrodynamic crossovers with dissipation-assisted operator evolution", finite U(1) density, ballistic to diffusive), PRB 110, 075149 (2024, fermionic DAOE energy diffusion), arXiv:2004.05177 (DAOE original), PRL 127, 170603 (2021, 13C Floquet prethermal >90 s), doi:10.1038/s41586-025-09977-x (prethermalization by random multipolar driving, 78-qubit processor), arXiv:2608.05988 (strange metal, 2D Hubbard, DiagMC + cold atoms), PRB 103, 155123 (2021, spin diffusion and spin conductivity, 2D Hubbard), arXiv:2608.07178 (relaxation landscape of 2D magnet, 256-qubit processor). Zero relevant hits for: "quantum computer conductivity Hubbard", "dynamic structure factor warm dense matter quantum computer", "Pauli propagation transport diffusion constant", "thermal Hall conductivity quantum computer", "thermoelectric Seebeck quantum algorithm", "quantum algorithm linear response Kubo" (only LinReTraCe, classical), "optical conductivity quantum computer", "polaron mobility quantum computer".

## Key physics framing for this lens
Protein lesson 5 generalises. Infinite-temperature transport (spin diffusion, NMR, Floquet heating at T=inf) is where DAOE, Pauli propagation and cluster methods converge, and the quantum-hard long-time tails carry little decision value. The candidate window is the intersection of:
(i) a thermal (T << bandwidth) or degenerate initial state;
(ii) an omega -> 0 transport observable that needs t >> tau_collision;
(iii) strong coupling, where diagrammatic series (DiagMC, kinetic theory, NEGF-GW) are uncontrolled;
(iv) a Hamiltonian with a small model floor (bare Coulomb, or a cold-atom or moire Hubbard realisation).
Imaginary-time QMC is weakest exactly at omega -> 0: the Drude width equals the collision rate, the most ill-conditioned part of analytic continuation.

## Candidates (final)

### C1. Low-frequency transport tensor of warm dense hydrogen/DT beyond Kohn-Sham: sigma_DC, thermal conductivity kappa (with e-e scattering), electron-ion coupling G_ei  [novelty B; verdict plausible]
- INPUT: species (H/D/T, later CH), mass density (r_s ~ 1-4), T_e (theta = T/T_F ~ 0.3-2), T_i (two-temperature for G_ei), ion snapshots from DFT-MD (or quantum protons).
- OUTPUT: sigma_DC(rho,T), kappa(rho,T), Lorenz number, G_ei(rho,T_e,T_i) with error bars; tables for ICF radiation-hydrodynamics codes.
- Practical use: ICF capsule design (hot-spot conduction losses, ablator/fuel heat flow), two-temperature relaxation in laser-heated matter, Jupiter-interior hydrogen. The first code-comparison workshop found "large variations ... when either the relevant Coulomb coupling parameter is large or computational expense causes difficulties" (2007.00744). A second workshop ran at LLNL in July 2023 (cited in 2503.13014). Measured e-i coupling in strongly heated graphite gave relaxation ~3x slower than earlier reports (1303.1402).
- Quantum mechanism: first-quantized plane-wave electrons (Su et al. 2105.12767, cited by sibling, not re-verified here) with the non-BO finite-T machinery of Rubin et al. 2308.12352 (PNAS 121, 2024). Thermal electrons via Gibbs sampler, microcanonical QPE energy filter, or TPQ. Three readout routes:
  (a) direct nonequilibrium response: a weak uniform field, or a weak T_e-T_i imbalance, then measure the extensive total current or the ion kinetic-energy change (per-shot variance ~ N_e and signal ~ N_e, so the shot count stays modest);
  (b) Kubo/Green-Kubo correlators <J(t)J(0)>; for G_ei, the clamped-ion electronic force autocorrelation <F_I(t)F_I(0)> (the Simoni-Daligault friction formulation, 1911.04622), evaluated with the correlated rather than the Kohn-Sham propagator;
  (c) kappa from the diffusive pole of the small-q energy-density correlator.
  Methods this replaces: KS-DFT Kubo-Greenwood, which misses e-e scattering (Desjarlais et al. PRE 95, 033203; Reinholz et al. 1401.0805); Ziman/average-atom; kinetic theory with strong-coupling closures (Babati 2606.02890/2606.02881); G1-G2 NEGF (2402.05214); PIMC ITCF + analytic continuation, which is worst at omega -> 0.
- Classical SOTA:
  - KS-DFT-MD + Kubo-Greenwood (Hu et al. PRE 89, 043105 (2014) for D).
  - Mixed stochastic-deterministic DFT/TDDFT (Liu 2510.10112, Al to 1000 eV; White 2112.01638).
  - QMD friction for G_ei (Simoni & Daligault 1911.04622; Daligault 1906.01610).
  - Quantum kinetic theory (Babati 2026).
  - G1-G2 NEGF (Bonitz group).
  - PIMC with sign mitigation (2009.11036, 2412.13596, 2407.01044).
  - Frequency moments / ITCF (2301.08444).
  - Average-atom Ziman (2503.13014).
- Why classically hard: at theta ~ 1 and r_s ~ 1-3 the electrons are partially degenerate and moderately coupled.
  - PIMC has a fermion sign problem and gives only imaginary time.
  - KS-DFT has no e-e collision term and an uncontrolled finite-T xc.
  - Kinetic theory is controlled only at weak coupling.
  - NEGF approximations (GW, T-matrix) are uncontrolled at Gamma ~ 1.
  - The DC limit needs t >> tau_coll.
- Novelty evidence (scoped): these searches (2020 to 2026-09-28) returned no quantum algorithm or resource estimate for WDM conductivity, thermal conductivity or G_ei:
  - arXiv abstract searches: "warm dense matter quantum computing", "electron-ion equilibration quantum computer", "quantum algorithm Green-Kubo transport coefficients", "uniform electron gas quantum computer", "opacity quantum computer";
  - OpenAlex: "dynamic structure factor warm dense matter quantum computer".
  Nearest work: quantum stopping power (2308.12352); the roadmap 2605.07722 (names no observable); sibling candidate discovery_algorithms.md C1 (XRTS DSF at finite k). -> B.
- How it differs from the sibling DSF candidate: it targets the omega -> 0, long-time regime and hydrocode-input observables rather than diagnostics, and this is where the ITCF constraints are weakest.
- Main failure risks:
  - (a) Cost. The DC limit needs ~1e2-1e3 hbar/E_F of evolution. A stopping-power-class trajectory costs ~1e11-1e13 Toffoli (2308.12352 gives ~100x FeMoco-class). With 1e2-1e3 repetitions per state point that is 1e13-1e16 Toffoli per point [ESTIMATE], or days to years per point at 1e6-1e7 Toffoli/s. Only a decision version (a handful of (rho,T) points where classical methods disagree by >30%) is plausible.
  - (b) Thermal-state preparation cost at theta < 0.5.
  - (c) Finite size: N_e = 32-128 may not converge sigma_DC.
  - (d) The workshop spread may come from cheap models (Lee-More, Spitzer) rather than first-principles methods. If KS-DFT + e-e correction, QMD, kinetic theory and G1-G2 agree within ~10-20%, there is no solver wall.
  - (e) Hydrocode sensitivity (yield vs kappa multiplier) was not verified in this session.
- Kill test (cheap, classical): compile the 2016 and 2023 workshop data for H/D at theta in [0.3,2] and r_s in [1,3]. If the first-principles methods agree within the decision tolerance there, kill.
- Scaling variables: N_e at fixed (r_s, theta); theta decreasing; r_s increasing (coupling).

### C2. Strong-coupling 2D Hubbard DC resistivity and optical conductivity at low T (U = 6-10 t, T = 0.05-0.25 t, doping 5-20%)  [novelty C (subsection of a D-adjacent area); verdict weak-plausible]
- INPUT: t, t', U, doping p, T, lattice L x L (8x8 to 16x16).
- OUTPUT: rho_DC(T,p), the low-frequency Drude width of sigma(omega), charge diffusivity D_c and compressibility (Nernst-Einstein), optionally the Hall coefficient.
- Practical use: correlated-metal transport (cuprate strange metal, bad metals). A cold-atom benchmark exists: Brown et al. 1802.09456, Science 363, 379 (2019), linear-T resistivity exceeding MIR in the 2D FH model. Practical decision relevance is weak; NOVEL_ADVANTAGE_SEARCH rated doped-Mott transport 1/5.
- Quantum mechanism: Jordan-Wigner or compact-encoded fermions (hardware precedent: 2510.26845 Willow 6x6; 2510.26300 H2 56 q; 2409.06789).
  - Thermal ensemble via METTS-style product-state sampling plus imaginary-time evolution or a Gibbs sampler, or via energy-filtered microcanonical states.
  - Trotter/QSP evolution to t ~ 20-50/t, then the current-current correlator or the direct response to a tilt.
  - The cold-atom experiment itself serves as the analog quantum comparator.
  - It replaces DQMC + MaxEnt (sign problem, ill-posed continuation) and DiagMC (series divergence at strong coupling).
- Classical SOTA:
  - Numerically exact weak-coupling conductivity without continuation (2501.19118).
  - DQMC + continuation (Huang et al. Science 2019 [UNVERIFIED ref; disputed by 2104.08733]).
  - FTLM on 4x4-20 sites; high-T multi-method studies (1811.08343, 2208.04047).
  - NLCE at strong coupling (2602.03771); DiagMC + continuation (2509.00281).
  - DMFT/DCA; METTS on cylinders.
- Why classically hard: at U >= 6t and T <= 0.2t:
  - the DQMC average sign collapses at 5-20% doping;
  - DiagMC series diverge;
  - FTLM is finite-size dominated below T ~ 0.3t;
  - NLCE converges only at T >~ 0.3-0.5t;
  - real-time TN on 2D thermal states saturates.
- Novelty evidence (scoped):
  - The arXiv abstract search "conductivity Hubbard model quantum computer" and the OpenAlex search "quantum computer conductivity Hubbard" returned no digital quantum computation of 2D Hubbard conductivity.
  - An analog cold-atom measurement exists (Brown 2019), but without a quantum-vs-classical advantage framing.
  - The digital 2D FH dynamics demonstrations (2510.26845, 2510.26300) measured polarons and spin-charge separation, not transport coefficients.
  - -> C.
- Main failure risks:
  - L4 decision relevance.
  - Model floor for real cuprates (three-band physics, phonons, disorder).
  - Thermal-state preparation at T ~ 0.1t.
  - Finite size in the DC limit at L <= 12.
  - Cold-atom experiments may reach the regime first; that would be an analog advantage, not a digital one.
- Resources [ESTIMATE]: 128-512 logical qubits, ~1e3-1e4 Toffoli per Trotter step, 1e2-1e3 steps and 1e3-1e5 samples, giving 1e9-1e12 Toffoli per (T,p) point.

### C3. Triangular-lattice (moire TMD) Hubbard: resistivity scaling across the continuous bandwidth-tuned Mott transition  [novelty B; verdict weak]
- INPUT: triangular Hubbard model (plus nearest-neighbour V and gate-screened Coulomb) with moire continuum-model parameters; U/W sweep; T = 0.02-0.3 W.
- OUTPUT: rho(T, U/W) near the transition, scaling-collapse exponents, and whether the transition is continuous in the clean model.
- Practical use: interpreting the MoTe2/WSe2 continuous Mott transition (Li et al. 2103.09779) and Pomeranchuk physics (2203.01010). It tests whether clean-model physics or disorder explains the experiment. This is a scientific use, not an industrial one.
- Quantum mechanism: as in C2, on a triangular lattice (frustrated hopping, no sign-free QMC); thermal states plus Kubo or direct response.
- Classical SOTA:
  - DMFT, which gives a first-order transition (Zang 2112.03080; Reymbaut 2004.02302).
  - DMFT+FTLM transport (Vranic 2006.01707).
  - DMRG ground states on cylinders.
  - NLCE at high T; CDMFT.
- Why classically hard:
  - Frustration gives a strong sign problem at all T.
  - Low-T quantum-critical transport near a continuous MIT needs long times on an entangled finite-T state.
  - Single-site DMFT gives the wrong order of the transition.
- Novelty evidence (scoped): the arXiv abstract searches "moire Hubbard resistivity" and "triangular lattice Hubbard model resistivity" returned only DMFT, FTLM and experimental papers, with no quantum-computer study. -> B.
- Main failure risks:
  - Model floor: twist-angle disorder, long-range Coulomb and device inhomogeneity may set the measured scaling.
  - Low practical value.
  - Quantum-critical scaling needs large L.

### C4. Carrier-multiplication (impact-ionization) quantum yield in photoexcited 2D Mott insulators, beyond DMFT  [novelty A/B; verdict weak-plausible]
- INPUT: 2D single- or two-orbital Hubbard model with U, t, t', and optionally an ionic potential or Hund J; pump photon energy hbar*omega, fluence, and an initial Mott (AF) state at low T. Scaling variables: L and omega/U.
- OUTPUT: doublon-holon pairs per absorbed photon vs time (quantum yield), the impact-ionization onset hbar*omega/Delta_Mott, and the fast and slow thermalisation times.
- Practical use: Mott-insulator photovoltaics that could exceed single-junction limits through carrier multiplication (Manousakis 0911.4933; LaVO3 photovoltaic studies [UNVERIFIED]). An active classical program exists:
  - Gazzaneo & Arrigoni 2208.14752, 2404.01729, 2408.14822;
  - Werner, Held & Eckstein 1408.3425;
  - Wais QBE 1806.02570, 2012.11257;
  - 1D ionic Hubbard 2412.05798.
- Quantum mechanism: Hamiltonian simulation of the pumped 2D Hubbard model (Peierls-phase drive), starting from an adiabatically prepared AF Mott state and counting doublons (a diagonal observable, so readout is cheap). It is a pure-state quench and needs no Gibbs state, which puts it closer to current hardware demonstrations (2510.26845, 6x6 FH on Willow). It replaces:
  - nonequilibrium DMFT, whose local self-energy misses the 2D spin-polaron and magnon-emission channels that compete with impact ionization;
  - NEGF (GW, T-matrix);
  - QBE;
  - 1D and ladder tDMRG/tLanczos.
- Classical SOTA: nonequilibrium and Floquet DMFT with phonon baths, the quantum Boltzmann equation, 1D time-dependent Lanczos/tDMRG, short-time 2D TN or operator propagation, NEGF.
- Why classically hard:
  - The model is 2D and strongly correlated, and high-energy photoexcitation drives fast entanglement growth.
  - The relevant timescales (tens to hundreds of 1/t) exceed 2D TN reach.
  - DMFT's locality removes the AF-background energy-dissipation channel whose rate competes with impact ionization.
- Novelty evidence (scoped):
  - arXiv "impact ionization Mott insulator" returned 10 classical or experimental papers (2009-2024), none quantum.
  - "photodoped Mott quantum computer" returned 0 results; "doublon dynamics quantum processor" returned 1 irrelevant result.
  - -> A for the impact-ionization yield; B because 2D FH quench demonstrations exist.
- Main failure risks:
  - Model floor: multi-orbital t2g bands in LaVO3-type materials, e-ph relaxation at ~100 fs competing with impact ionization, interfaces and contacts.
  - Nonlocal corrections might be small, in which case DMFT suffices.
  - Device efficiency is dominated by extraction and recombination, not the intrinsic yield.
- Resources [ESTIMATE]: 8x8-12x12 sites (128-288 qubits), t_max ~ 50-100/t, ~1e2-1e3 shots per time point. Short times fit NISQ with error mitigation; long times need FT.

### C5. Dense-plasma L-shell opacity of mid-Z ions (Fe at the solar convection-zone base) with dynamical free-electron screening  [novelty A; verdict weak]
- INPUT: Fe (Cr, Ni) at T_e ~ 150-200 eV and n_e ~ 1e22-1e23 cm^-3; the ion plus surrounding free electrons in a box.
- OUTPUT: frequency-dependent photoabsorption cross-section and Rosseland-mean opacity in the L-shell band.
- Practical use: solar interior models (the solar abundance problem) and ICF radiation transport. The Z-facility Fe opacity discrepancy: Bailey et al. Nature 517, 56 (2015) and Nagayama et al. PRL 122, 235001 (2019), both cited via 2607.21238. 2607.21238 proposes plasma screening (14-17%) plus CI (10-20%), giving a 25-30% enhancement.
- Quantum mechanism: first-quantized dynamics of bound and free electrons around the ion (dipole autocorrelation). It captures dynamical (not static Debye) screening and bound-free correlation together. It replaces R-matrix with static screening, detailed and super-configuration accounting codes, and average-atom Kubo-Greenwood.
- Classical SOTA: R-matrix (Iron Project, astro-ph/0207223 listing); screened MCDF/CI (2607.21238); super-transition-array codes (1809.10189); DFT-MD Kubo-Greenwood.
- Novelty evidence (scoped): the arXiv abstract search "opacity quantum computer" found no plasma-opacity quantum computation. -> A.
- Main failure risks:
  - L2: the plasma is weakly coupled at these conditions, so static screening plus large CI may suffice.
  - L5/L6: the discrepancy may be experimental systematics.
  - The keV core scale is costly in plane-wave first quantization, so pseudopotentials are needed.

## Killed ideas (this lens)
- **Infinite/high-T spin and charge diffusion constants, 1D or 2D** (the Quantinuum 2503.20870 lineage, 2608.07178): DAOE (2004.05177, PRB 110 075149, doi:10.1103/gz9n-v8ty) and Pauli propagation converge in this regime, and no practical decision depends on it (lesson 5).
- **1D anomalous/superdiffusive (KPZ) transport, Drude weights, 1D Hubbard Seebeck** (2502.17171, doi:10.1103/j971-h796): tDMRG and GHD handle 1D, it is already demonstrated on hardware, and it has no application.
- **KvN-encoded classical-MD Green-Kubo coefficients** (2605.30142): this is classical dynamics on a classical force field. The claimed speedup is amplitude estimation vs quantum shot sampling, at most quadratic vs classical MD sampling (lesson 3).
- **Doped-Mott / correlated-oxide thermopower**: the Kelvin (entropic) formula captures it semi-quantitatively from equilibrium thermodynamics (1410.0830, 1504.03860, 1307.4800, 1001.3423), so static QMC/DMFT suffice. Heavy-fermion thermoelectrics are DMFT-friendly in 3D.
- **Floquet engineering of the exchange J in Mott insulators, and heating times**: perturbation theory plus the Fermi golden rule cover it (1801.00401). The heating time grows exponentially in omega and exceeds both the classical and the quantum horizon (lesson 5).
- **Floquet prethermal lifetimes in NMR / 13C hyperpolarisation** (PRL 127, 170603): infinite-T dipolar dynamics, the Pauli-propagation regime.
- **HHG spectra of Mott insulators**:
  - Phenomenological dephasing (a few fs) sets both a model floor and a short coherent horizon.
  - 1D (iTEBD 2010.13255) and DMFT (1911.04183, 2203.01029) interpretations already exist.
  - No decision depends on 2D nonlocal corrections.
- **Mott resistive switching / current-driven NESS** (Ca2RuO4, VO2): Joule heating and lattice effects dominate (1309.0909), so the model floor fails.
- **Nonequilibrium Anderson/Kondo junction steady-state transport**: strong impurity solvers exist (inchworm, TN influence functional, 2403.16700); killed by the sibling lens too.
- **Polaron / organic-semiconductor mobility**: overlaps the prior OPV and Ortmann MPS work (lesson 6).
- **Li-ion, proton and hydrogen-in-metal diffusion**: these are nuclear dynamics on a classical potential, where RPMD/PIMD are adequate, and they carry the coherent-oracle cost (lesson 3).
- **Magnon/phonon thermal conductivity of quantum magnets**: phonons dominate the measured signal, LSWT/Boltzmann works at low T, and high-T series work at high T. Thermal Hall is covered by sibling materials C3.
- **QCD shear viscosity (2104.02024) and QGP transport (2601.14399)**: not applied.
- **Electron hydrodynamics** (PdCoO2, graphene): Boltzmann-tractable.

## Cross-cutting benchmark/test plan
- FULL (quantum correlator or response) vs ABLATION (the best of the named classical portfolio at matched wall-clock).
- Validation anchors:
  - the UEG, where PIMC is exact (C1);
  - high-T 2D Hubbard, where FTLM, NLCE and DiagMC agree (C2);
  - 1D limits, where tDMRG is exact (C2-C4).
- Pre-register the decision tolerance (e.g. 20% for sigma, kappa and G_ei) before any run.
