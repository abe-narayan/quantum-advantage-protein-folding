# Discovery lens: ALTERNATIVE DOMAINS (nuclear, plasma / warm dense matter, semiconductor devices, PDE solvers, geophysics)

Date: 2026-09-28. Status: FINAL for this lens.
Author: discovery subagent (alt-domains lens). No computation was run; literature only.

## 0. Search constraints and method

- WebSearch budget was exhausted (200/200) at the start of this lens; all three WebSearch calls were refused.
- WebFetch to the arXiv API and OpenAlex returned HTTP 429 on first try. All subsequent searches ran through python/curl against:
  arXiv export API (boolean abstract-field queries, sorted by submission date), arXiv abs pages (abstract verification),
  OpenAlex (search, cited-by, DOI lookup) and Crossref (keyword search, DOI metadata). Calls were spaced 6-12 s with retry.
- "Not found" statements below are scoped: they refer only to the queries listed in section 5, run through 2026-09-28.
  arXiv abstract-field searches miss papers that use other wording; they are evidence, not proof, of absence.

## 1. Landscape finding that shapes this lens

High-energy-density (HED) / warm-dense-matter (WDM) physics is now an active quantum-algorithm lane, driven by Google Quantum AI
and Sandia (Baczewski, Kononov, Pathak, Nelson):
- stopping power: Rubin et al. arXiv:2308.12352, PNAS 121 (2024) doi:10.1073/pnas.2317772121 [VERIFIED arXiv abs + OpenAlex]
- astrophysical (solar iron) opacity: Pathak, Kononov, Baczewski arXiv:2607.02811 (2026-07) [VERIFIED arXiv abs]
- WDM conductivity incl. electron-electron scattering, quantum resource estimates: Kononov et al., OSTI report doi:10.2172/3363975 (2025) [VERIFIED Crossref metadata; no abstract]
- "Quantum computing and warm dense matter", Baczewski et al., OSTI doi:10.2172/3028616 (2025) [VERIFIED Crossref]; "Prospects for simulating WDM on quantum computers", doi:10.2172/2005714 (2022) [VERIFIED Crossref]
- finite-temperature Green's functions via robust quantum Arnoldi: Nelson & Baczewski arXiv:2605.22920 [VERIFIED]
- community roadmap: Pennati et al. arXiv:2605.07722 (quantum "potentially the most disruptive for WDM and ICF microphysics") [VERIFIED]
- 29 works cite Rubin et al. (OpenAlex cited-by W4399208307, 2026-09-28); none is an electronic dynamic-structure-factor / XRTS quantum algorithm.

Why HED is structurally attractive after the protein failure: the Hamiltonian is the bare Coulomb Hamiltonian of electrons and nuclei
(no force field, no active space, no embedding), which addresses lesson 6 (model floor) better than chemistry or nuclear physics.
The output is a spectrum or a transport coefficient (not an argmin of a classical energy), which addresses lesson 3.
Why it is dangerous: (a) a strong, fast-moving classical program (Dornheim/Vorberger/Bonitz PIMC, imaginary-time correlation-function
(ITCF) metrology, TDDFT) keeps extracting the diagnostic information without real-time dynamics (lesson 5); (b) Sandia is working
in exactly this space, so novelty windows are short; (c) finite-temperature state preparation is an unsolved cost item.

## 2. Candidates

### C1. Real-frequency electronic dynamic structure factor for XRTS diagnostics of partially degenerate, partially ionized warm dense matter
- Domain: HED physics / ICF and XFEL diagnostics.
- INPUT: element(s) (H, D-T, Be, C/CH ablator), mass density (r_s about 1.5-4), electron temperature (theta = T/T_F about 0.25-1),
  scattering wavevector q (forward to backward scattering), optionally ionic configurations from DFT-MD/PIMC snapshots.
- OUTPUT: S_ee(q, omega) on an eV-resolved grid including plasmon position/width, bound-free and free-bound features
  (free-bound: Boehme et al. arXiv:2306.17653), and derived ionization degree / continuum lowering (IPD).
- Practical use: XRTS is the standard density/temperature/ionization diagnostic at NIF, LCLS, European XFEL; the forward model S_ee
  is what converts measured spectra into EOS points used in rad-hydro and ICF capsule design. Users: ICF/HED experimentalists, EOS table builders.
- Quantum mechanism: first-quantized plane-wave electrons (block encodings of Su et al. PRX Quantum 2, 040332 (2021)
  doi:10.1103/prxquantum.2.040332 [VERIFIED]) with nuclei either as BO snapshots or quantum particles (as in Rubin et al.).
  Compute C(q,t) = <rho_q(t) rho_-q(0)>_beta by Hadamard-test interferometry or directly sample the spectral measure of rho_-q|psi_beta>
  by phase estimation (Roggero-Carlson style response algorithm); for finite T use (i) microcanonical energy-filtered random states
  (ensemble equivalence at large N), (ii) Krylov/Arnoldi GF estimation at nonzero T (arXiv:2605.22920), or (iii) sampled thermal initial states.
  What it replaces: analytic continuation of PIMC ITCF data (ill-posed) and LR-TDDFT with adiabatic XC kernels (misses dynamic local field
  correction G(q,omega)). The speedup is in the fermionic real-time dynamics: classical exact methods scale exponentially in N
  (sign problem in PIMC; exponential Hilbert space in ED), quantum Hamiltonian simulation is polynomial in N and t. Claimed type:
  computational/resource advantage (category 3), and only if the classical attack fails where information is present.
- Classical SOTA / strongest competitors: ab initio PIMC F(q,tau) with sign-problem mitigation (Dornheim et al., e.g. arXiv:2509.11317,
  arXiv:2508.18935, arXiv:2502.15288, arXiv:2403.01979) + analytic continuation (Chuna, Boehme, Dornheim arXiv:2603.27212; PyLIT);
  model-free ITCF thermometry (Dornheim et al. Nat Commun 13, 7911 (2022) doi:10.1038/s41467-022-35578-7 [VERIFIED]; review arXiv:2604.25735;
  guidelines arXiv:2510.00493); LR-TDDFT/Liouville-Lanczos (Moldabekov et al. arXiv:2502.04921, arXiv:2510.01875); mixed stochastic-deterministic
  and orbital-free TDDFT DSF (doi:10.1088/2516-1075/adad24); Chihara-decomposition models; PIMC-based IPD (Bellenbaum et al. arXiv:2503.14014).
- Why classically hard: real-frequency spectra require real-time fermionic dynamics at finite T; PIMC is exact only in imaginary time
  and its sign problem is exponential in N at theta below about 1 with r_s of a few; analytic continuation cannot resolve line shapes
  that the ITCF does not constrain; TDDFT lacks dynamic correlation and e-e scattering widths.
- Novelty: B. Scoped evidence: arXiv abstract searches "warm dense" AND "quantum computer", "dynamic structure factor" AND "quantum computer",
  "Thomson scattering" AND "quantum computer" (through 2026-09-28) and Crossref/OpenAlex searches found quantum protocols for stopping power,
  opacity and conductivity (all linear-response relatives) but no quantum-algorithm study of the WDM electronic DSF for XRTS, and no
  quantum-vs-classical comparison against PIMC+ITCF.
- Closest prior work: Rubin et al. 2023/2024 (same Hamiltonian machinery, different observable); Pathak et al. 2026 (photon-register spectral readout);
  Kononov et al. 2025 OSTI (conductivity). Note: Baczewski co-authored the free-bound XRTS paper (arXiv:2306.17653), so Sandia is adjacent.
- Main failure risk: (1) information-vs-computation (lesson 5): the ITCF already delivers T, normalization, Rayleigh weight and density model-free;
  the real-frequency spectrum adds information only for features above instrument resolution (source-and-instrument function of about eV;
  meV XFEL setups mainly probe ion-acoustic features, which are slow ionic dynamics). If the quantum spectrum changes no inferred (rho, T, Z)
  beyond the experimental error bar, it is not useful. (2) Gibbs/thermal state preparation cost at theta < 1. (3) Finite-size (N about 32-128 electrons)
  errors in q-resolution. (4) Scoop risk from Sandia/Google.
- Rough resources (extrapolated, not computed here): Rubin et al. report stopping-power costs about 100x FeMoco-class Toffoli counts
  with similar logical qubits; a DSF at a few q-points with O(10^2-10^3) time points is the same order per q-point (times the thermal-state overhead).
  Benchmark scaling variables: N (16 -> 256 electrons), theta (1 -> 0.25) at fixed r_s, q.
- Kill criterion (proposed): if ξ-extrapolated PIMC + analytic continuation, or TDDFT with a PIMC-derived dynamic kernel, reproduces
  exact small-N spectra and changes no XRTS-inferred parameter beyond experimental uncertainty in the target regime, kill.
- Initial verdict: plausible.

### C2. Electron-ion energy-exchange (temperature relaxation) rate in two-temperature warm dense hydrogen/DT and light ablators, beyond Fermi-golden-rule and Ehrenfest
- INPUT: species, density, T_e, T_i (T_e != T_i), ionic structure (snapshots or quantum protons).
- OUTPUT: electron-ion coupling factor G(rho, T_e, T_i) (W m^-3 K^-1) and relaxation time; coupled-mode correction.
- Practical use: G enters rad-hydro codes for ICF implosions (compression and hot-spot formation) and for interpreting XFEL/laser
  isochoric-heating experiments (e.g. enhanced/inhibited coupling observations, arXiv:2110.14704, arXiv:1303.1402).
- Quantum mechanism: non-Born-Oppenheimer first-quantized simulation of electrons + (quantum) protons from a prepared two-temperature state,
  measuring the electron-subsystem energy flux over 10-100 fs (Green-Kubo-like short-time extraction), i.e. the Rubin et al. multi-species
  machinery with a different initial state and observable; alternatively the exact f-sum golden-rule formula needs S_ee(q,omega) and S_ii (C1 primitive)
  plus coupled modes. Replaces: Ehrenfest TDDFT (no detailed balance, mean-field electrons), DFT-MD + DFPT Eliashberg-type estimates,
  linear-response coupled-mode models.
- Classical SOTA: DFT-MD + DFPT (Zhang, Qin, Zhu, Vorberger arXiv:2401.08184 [VERIFIED]); first-principles e-i couplings (Simoni & Daligault
  arXiv:1904.04450 [VERIFIED]; arXiv:2007.06747); quantum mean-force kinetic theory (Rightley & Baalrud arXiv:2001.11438, arXiv:2102.05115);
  unified relaxation theory (Daligault arXiv:1906.01610); wave-packet MD; NEGF G1-G2 (Bonitz group, [UNVERIFIED specific paper]).
  Documented disagreement between coupled-mode theories and simulations: Dharma-wardana arXiv:1705.10221 [VERIFIED].
- Why classically hard: correlated nonadiabatic electron-ion dynamics at partial degeneracy; mean-field dynamics misses e-e scattering and
  detailed balance; exact methods are exponential.
- Novelty: B. Scoped evidence: arXiv "electron-ion" AND ("quantum computer" OR "quantum algorithm") returned no relaxation-rate paper
  (only plasma-kinetics and unrelated hits); "temperature relaxation" AND "quantum computer" returned nothing relevant.
- Closest prior work: Rubin et al. stopping power (projectile energy loss = the same energy-transfer physics for a single fast ion).
- Main failure risk: rad-hydro decision insensitivity (G may matter only in a narrow window); relaxation times (ps) exceed simulable windows,
  forcing short-time extrapolation; T_e != T_i state preparation; weak-coupling regimes where Landau-Spitzer/Brown-Preston-Singleton kinetic theory suffices.
- Initial verdict: weak-to-plausible (depends on a sensitivity study showing G uncertainty flips an ICF design quantity).

### C3. Positron annihilation lifetimes and Doppler momentum densities at vacancies in strongly inhomogeneous semiconductors (halide perovskites, oxides)
- INPUT: supercell with candidate defect (vacancy type/charge), relaxed geometry (with positron-induced relaxation).
- OUTPUT: positron lifetime tau (ps), contact density / enhancement, 2-gamma Doppler momentum distribution; defect identification.
- Practical use: positron annihilation spectroscopy is a standard vacancy metrology for semiconductor wafers, perovskite photovoltaics,
  and irradiated reactor steels; interpretation requires computed lifetimes per candidate defect.
- Quantum mechanism: first-quantized multi-species simulation (eta electrons + 1 positron, distinguishable particle, as in multi-species
  Rubin et al. encodings); QPE/filtered ground-state preparation of the positron-trapped state; estimate the electron-positron coincidence
  density (contact density) and pair-momentum distribution (natural in first quantization via QFT of pair coordinates). Replaces:
  two-component DFT with LDA/GGA/WDA enhancement factors and DMC mixed estimators.
- Classical SOTA: two-component DFT (Barbiellini arXiv:1504.03359; Kuriplach arXiv:1407.4154); QMC lifetimes in solids
  (Simula, Muff, Makkonen, Drummond arXiv:2202.13204 [VERIFIED]); weighted-density approximation.
  Evidence the correlation treatment is the bottleneck: Madaan et al. arXiv:2511.06926 [VERIFIED] (choice of e-p correlation functional
  is "crucial" for cation vacancies in MAPbI3/CsPbX3, stronger than in metals).
- Why classically hard: electron-positron cusp and strong local screening cloud in highly inhomogeneous density; DMC contact-density
  estimators are mixed/extrapolated and expensive for defect supercells.
- Novelty: A (scoped): arXiv abstract searches positron AND ("quantum computer" OR "quantum computing") returned only HEP/lattice-gauge
  items; no quantum-algorithm paper on positron states in solids or defects found.
- Main failure risk: DMC is likely adequate (the positron is nodeless, so fixed-node error comes only from electron nodes); experimental
  lifetime resolution (a few ps) may be larger than the classical solver error; Madaan et al. also show polymorphism/structure dominates
  (model floor from structure, not correlation). Pseudopotential/core-annihilation errors.
- Initial verdict: weak (keep as an A-category probe: first task is a classical DMC-vs-functional error budget vs experimental resolution).

### C4. Semi-exclusive neutrino-40Ar response (nucleon knockout final states) for DUNE cross-section modeling
- INPUT: nucleus (40Ar), nuclear lattice EFT Hamiltonian (pionless or one-pion exchange), weak current operator, momentum transfer q.
- OUTPUT: inclusive response R(q, omega) and semi-exclusive one-nucleon knockout distributions (missing energy/momentum) in the quasielastic region.
- Practical use: cross-section systematics are expected to dominate DUNE oscillation analyses (Roggero et al. arXiv:1911.06368 [VERIFIED]);
  event generators need exclusive final states.
- Quantum mechanism: lattice-EFT real-time evolution after applying the current operator; spectral sampling via phase estimation or Chebyshev
  spectral reconstruction (Sobczyk & Roggero arXiv:2110.02108 [VERIFIED]); final-state measurement gives exclusive channels.
  Costs for pionless/OPE lattice EFT: Watson, Bringewatt, Shaw, Childs, Gorshkov, Davoudi arXiv:2312.05344 [VERIFIED].
- Classical SOTA: LIT coupled cluster for 40Ca longitudinal and transverse responses (Sobczyk et al. arXiv:2103.06786, arXiv:2310.03109 [VERIFIED listing]),
  16O responses (Acharya et al. arXiv:2410.05962), GFMC for A <= 12 (Lovato et al., [UNVERIFIED id]), ab initio spectral functions (Cavallin et al. arXiv:2608.23057),
  SuSAv2, AFDMC.
- Why classically hard: 40-body continuum real-time dynamics; LIT-CC gives inclusive only; GFMC limited to light nuclei.
- Novelty: C (quantum methods and resource estimates exist; no quantum-vs-classical advantage study vs LIT-CC found in searched sources).
- Main failure risk: model floor (lesson 6) is severe: DUNE energies (0.5-5 GeV) are dominated by resonance/pion production and relativistic
  kinematics that nonrelativistic lattice EFT does not describe; LO pionless errors exceed solver errors.
- Initial verdict: weak.

### C5. Adversarial head-to-head: weakly nonlinear kinetic-plasma Carleman quantum algorithm vs dynamical low-rank and reduced classical solvers
- INPUT: 3D electrostatic electron-ion plasma model (adiabatic electrons, kinetic ions, Debye screening, Krook relaxation), Fourier cutoff N_F,
  Hermite cutoff N_H, horizon T, precision epsilon.
- OUTPUT: spacetime-averaged ion kinetic energy (the observable in Berntson et al.), and more usefully, transport/heating rates.
- Practical use: moderate; a controlled benchmark for kinetic plasma (ion-acoustic turbulence) rather than an engineering deliverable.
- Quantum mechanism: Lyapunov-transformed Carleman embedding + hierarchical dense block-encoding + history-state readout
  (Berntson, Jennings, Lostaglio, Parker arXiv:2607.14308 [VERIFIED]); claimed superquadratic time and exponential memory savings relative to a
  Fourier-Hermite spectral solver.
- Classical SOTA to test against: dynamical low-rank / projector-splitting Vlasov solvers (Einkemmer & Lubich SISC 2018 doi:10.1137/18m116383x [VERIFIED];
  quasi-conservative DLR doi:10.1137/18m1218686 [VERIFIED]); tensor-train Vlasov; delta-f PIC with noise control; quasilinear theory in the
  weakly nonlinear regime; Monte Carlo estimation of the same averaged observable.
- Novelty: D (advantage claimed only against a dense spectral solver). The distinct contribution would be the strongest-classical comparison.
- Main failure risk: in the certified weakly nonlinear regime the distribution function is likely low-rank and quasilinear theory accurate,
  so the classical comparator may be polylog in N_H; output is a single averaged scalar with limited engineering use.
- Initial verdict: weak as an application, plausible as a red-team paper.

## 3. Killed ideas (with reasons)

- Solar/Z-machine iron opacity: already claimed (Pathak, Kononov, Baczewski arXiv:2607.02811, 2026-07). Not original; revisit only as a
  classical red-team of that protocol.
- WDM electrical/thermal conductivity with e-e scattering: already claimed with quantum resource estimates (Kononov et al., OSTI doi:10.2172/3363975, 2025).
- Stopping power: claimed (Rubin et al. 2024).
- Dense hydrogen / H-He demixing for giant planets: the bottleneck is statistical sampling and finite size, not per-configuration electronic accuracy.
  Wang, Hamel, Cheng arXiv:2603.28927 [VERIFIED] find demixing temperatures about 2000 K lower than earlier small-cell ab initio work, a shift
  larger than the functional, MLP and nuclear-quantum-effect errors. A quantum energy oracle per snapshot does not address this (lesson 1/3).
- Earth-core iron conductivity (e-e scattering): the strong-correlation claim (Zhang, Cohen, Haule, Nature 2015 doi:10.1038/nature14090) was
  retracted (doi:10.1038/nature17648 [VERIFIED]); DFT+DMFT finds a small e-e contribution (Pourovskii et al. NJP 2017, corrigendum doi:10.1088/1367-2630/aae6e1 [VERIFIED]);
  high T and compressed wide bands make local/perturbative methods accurate. No quantum-hard regime.
- NEGF quantum transport in sub-5 nm transistors: the classical cost is polynomial (recursive Green's function, SCBA electron-phonon at mean-field level);
  a quantum linear-solver speedup is polynomial at best, condition-number sensitive near band edges and exposed to dequantization;
  no strong-correlation object. Arxiv search for quantum-algorithm NEGF transistor work returned nothing (scoped). Killed on mechanism.
- CFD / Navier-Stokes quantum solvers: Jennings et al. arXiv:2512.03758 [VERIFIED] bound the end-to-end advantage by O(Re^{3D/8}) with numerics
  suggesting less; with fault-tolerant overheads (Babbush et al. PRX Quantum 2, 010103 (2021) doi:10.1103/prxquantum.2.010103 [VERIFIED]) a
  low-degree polynomial speedup does not survive. Readout of fields is the other killer.
- Radiative transfer: Igarashi et al. arXiv:2312.01664 [VERIFIED] claim exponential speedup but acknowledge measurement and state-encoding costs;
  classical Monte Carlo transport already scales as 1/epsilon^2 and parallelizes trivially; amplitude estimation gives at most quadratic in epsilon.
- Vlasov/linear plasma wave simulation on NISQ (e.g. doi:10.1103/lxr6-t7vb, 2026): classically trivial linear dynamics; demonstration only.
- Neutrinoless double-beta-decay nuclear matrix elements: model floor (EFT contact term, currents, g_A quenching) dominates solver spread;
  quantum work is a 1+1D pathfinding simulation (Chernyshev et al. arXiv:2506.05757 [VERIFIED]).
- Nuclear level densities / gamma strength for Hauser-Feshbach (n,gamma) evaluations: SMMC already computes heavy-nucleus level densities
  (Alhassid et al., Nuclear Data Sheets 2014 doi:10.1016/j.nds.2014.04.045 [VERIFIED]); remaining uncertainty is the shell-model interaction
  and phenomenology (model floor). No quantum paper found (arXiv "level density" AND "quantum computer").
- Resonance-region neutron cross sections (e.g. 16O(n,alpha) for reactor criticality): need keV accuracy of resonance positions; ab initio
  interactions give MeV-scale errors; R-matrix evaluation is data-driven. Model floor.
- Fission fragment yields: TDDFT/TDGCM phenomenology; model floor dominates; no clean quantum object [reasoning only; no literature search run].
- Quantum-limited imaging: a sensing/metrology advantage, not a computational one; out of scope.
- Seismic/geophysical inversion via annealing/QAOA: classical landscape optimization (lesson 3).
- Few-electron Si/SiGe quantum-dot spectra for spin-qubit design: N small enough for FCI/QMC; disorder/parameter uncertainty dominates [reasoning only].

## 4. Cross-candidate note

C1 and C2 share a primitive (finite-T density-density and energy-flux correlation functions in first quantization) and a failure mode
(finite-T state preparation). If one of them is pursued, the first experiment is classical: quantify, for H at r_s = 2-4, theta = 0.25-1,
how much XRTS-inferable information (T, rho, Z) is in S(q, omega) but not in F(q, tau), using exact small-N ED spectra vs PIMC+AC.
That test decides lesson 5 before any quantum resource estimate.

## 5. Query log (2026-09-28)

WebSearch (all refused, budget exhausted):
1. quantum algorithm dynamic structure factor warm dense matter X-ray Thomson scattering quantum computer
2. quantum computation of stopping power inertial fusion Rubin Berry Kononov
3. Dornheim path integral Monte Carlo fermion sign problem warm dense hydrogen dynamic structure factor 2025

WebFetch (HTTP 429): arXiv API "warm dense" AND quantum; OpenAlex "dynamic structure factor quantum computer algorithm".

OpenAlex: "stopping power quantum computer fusion"; cited-by W4399208307; (429) "warm dense matter quantum computer", "dynamic structure factor quantum algorithm",
"nuclear level density quantum computer"; DOI lookups 10.1103/v2ms-wmz1, 10.1103/physreve.111.l053202, 10.1103/6r9l-lynr, 10.1088/1367-2630/aae6e1.

Crossref: "quantum computer dynamic structure factor warm dense matter"; "quantum algorithm Thomson scattering plasma"; "quantum computing warm dense matter electronic structure";
"quantum algorithm nuclear level density"; "quantum computing neutrino nucleus scattering response function"; DOI metadata 10.2172/3363975, 10.2172/3028616,
10.2172/2005714, 10.1103/v2ms-wmz1, 10.1145/3774895.3815547; verification searches for Dornheim Nat Commun 2022, Zhang-Cohen-Haule Nature 2015 (+retraction),
SMMC level densities, Sobczyk LIT-CC 40Ca, Su et al. first quantization, Babbush quadratic speedups, Einkemmer-Lubich DLR, Watson et al. nuclear EFT.

arXiv API (abstract field):
- "warm dense" AND quantum AND "fault-tolerant"
- "warm dense" AND "quantum computer"
- "dynamic structure factor" AND "quantum computer"
- "level density" AND "quantum computer"
- "neutrino-nucleus" AND "quantum computer"
- au:Baczewski AND quantum; au:Kononov AND quantum
- "warm dense" AND "sign problem"
- "Thomson scattering" AND "imaginary-time"
- "nonequilibrium" AND "inertial confinement" AND quantum
- "electron-ion" AND ("quantum computer" OR "quantum algorithm")
- "temperature relaxation" AND "quantum computer"
- positron AND ("quantum computer" OR "quantum computing")
- "dense hydrogen" AND ("quantum computer" OR "quantum algorithm")  [0 hits]
- "double beta" AND "quantum comput*"
- Green AND "quantum transport" AND "quantum algorithm"  [0 hits]
- "electron-ion" AND "warm dense" AND (relaxation OR "energy exchange" OR coupling)
- hydrogen AND helium AND demixing AND "Monte Carlo" [0]; hydrogen AND helium AND (immiscibility OR demixing)
- "computational fluid dynamics" AND "fault-tolerant"
- "radiative transfer" AND "quantum algorithm"
- positron AND lifetime AND "quantum Monte Carlo"
- "nuclear effective field theor*" AND "quantum algorithm*" [0]; au:Davoudi AND nuclear AND quantum AND simulat* [0]
- "coupled-cluster" AND "40Ar"
- "level densit*" AND "shell model Monte Carlo" [0]
- "electron-positron" AND correlation AND vacancy
- Green AND transistor AND quantum AND algorithm AND qubit [0]
- "electron gas" AND "quantum computer" AND (finite-temperature OR thermal OR dynamic)
- au:Sobczyk AND response
- "linear response" AND "quantum algorithm" AND nuclei

arXiv abs pages read: 2607.02811, 2605.22920, 2308.12352, 2604.25735, 2603.27212, 2607.14308, 2506.05757, 2605.07722, 1911.06368,
2512.03758, 2312.01664, 2202.13204, 2401.08184, 2306.17653, 2510.00493, 2603.28927, 2310.13412, 2511.06926, 2312.05344, 2503.14014, 1705.10221.
