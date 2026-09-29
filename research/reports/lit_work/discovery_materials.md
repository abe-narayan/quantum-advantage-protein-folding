# Discovery lens: correlated / magnetic / defect / superconducting materials

Date: 2026-09-28. Status: COMPLETE (subagent lit scan, no computation).

Scope: experimentally measured response functions and phases of correlated materials (INS S(q,w), RIXS, thermal transport, nonlinear THz, DMFT spectra, defect multiplets, pairing), filtered by the seven protein-failure lessons.

Tool note: WebSearch budget was exhausted at start of this session. arXiv export API, OpenAlex and Semantic Scholar returned HTTP 429 throughout; local urllib to arxiv.org/search returned 406. All searches below were run through WebFetch on arxiv.org/search (abstract field, newest first), arXiv abs/html pages, and one Crossref query. arXiv's abstract search ANDs all terms and does not index chemical formulas with subscripts reliably (e.g. "KYbSe2" and "MoTe2" returned nothing), so absence of hits is weak evidence. All novelty statements are scoped to these sources through 2026-09-28.

## Query log
1. WebSearch "quantum computer dynamical structure factor inelastic neutron scattering Hamiltonian fitting 2025" -> budget exhausted.
2. arXiv API abs:"quantum computer" AND abs:"neutron scattering" -> HTTP 429.
3. OpenAlex "quantum computer dynamical structure factor inelastic neutron scattering" -> 429 (twice, later also 429).
4. Crossref "quantum computer dynamical structure factor neutron scattering magnet" -> irrelevant hits.
5. arXiv abstract: quantum computer "dynamical structure factor" -> 44 hits (list below).
6. arXiv abstract: quantum computer neutron scattering Hamiltonian -> 16 hits.
7. arXiv abstract: quantum computer Kitaev RuCl3 -> 6 hits, none quantum-computing.
8. arXiv abstract: "thermal Hall" "quantum algorithm" / "quantum computer" -> 6 hits, none a quantum algorithm for kappa_xy.
9. arXiv abstract: "thermal Hall" Kitaev + ED / TN / TPQ -> 2507.16558.
10. arXiv abstract: quantum algorithm transport coefficient Kubo conductivity finite temperature -> 0 hits.
11. arXiv abstract: quantum computer impurity solver dynamical mean-field theory -> 37 hits.
12. arXiv abstract: quantum computer spin defect color center electronic structure embedding -> 0; retry "spin defects quantum computers embedding" -> 9 hits.
13. arXiv abstract: Fermi-Hubbard quantum computer superconducting pairing correlations -> 3 hits.
14. arXiv abstract: fault-tolerant resource estimate dynamical structure factor -> 0 hits.
15. arXiv abstract: quantum processor spin liquid dynamics classical simulation -> 3 hits.
16. arXiv abstract: two-dimensional coherent spectroscopy terahertz quantum magnet nonlinear response -> 5 hits.
17. arXiv abstract: triangular antiferromagnet dynamical structure factor DMRG cylinder neutron -> 0; "KYbSe2 ..." -> 0; all-fields "KYbSe2" -> 0 (formula indexing issue).
18. arXiv abstract: "frontier of classical" / "beyond-classical" quantum simulation magnet Hubbard -> malformed (OR), unusable.
19. arXiv abs pages: 2503.20870, 2403.00910, 1911.03446, 2311.09207.
20. arXiv abstract: quantum Gibbs sampling frustrated magnet finite temperature phase diagram -> 0.
21. arXiv abstract: quantum spin ice quantum computer / quantum simulator pyrochlore -> 20 hits, none quantum-computing.
22. arXiv abstract: pi-flux quantum spin ice dynamical structure factor -> 7 hits.
23. arXiv abstract: pi-flux QSI sign problem Monte Carlo -> 0; frustrated transverse exchange sign problem -> 0; resolved via html of 2401.09551.
24. arXiv all: Ce2Zr2O7 -> 5 hits.
25. arXiv abstract: pyrochlore neural network quantum state -> 2 hits (ground states only).
26. arXiv abstract: moire fractional Chern insulator quantum computer algorithm -> 0; MoTe2 variants -> 0 (formula indexing).
27. arXiv abstract: Kitaev magnet dynamical spin structure factor -> 41 hits.
28. arXiv abs: 2602.10190, 2407.04205.
29. arXiv all: Begusic sparse Pauli -> 3 hits.
30. arXiv abstract: resonant inelastic x-ray scattering quantum algorithm -> 1 hit (2602.20270).
31. arXiv abstract: RIXS Hubbard model doped paramagnon numerical -> 1 hit.
32. arXiv abstract: quantum computer spectral function two-dimensional lattice -> 2 relevant.
33. Semantic Scholar / OpenAlex retries -> 429.

## Verified literature (by arXiv abs page, html page, or arXiv listing)

### Quantum computation of S(q,w) / spectroscopy (the occupied territory)
- arXiv:2603.15608 [VERIFIED abs] Lee, Kumaran, Pokharel, Scheie, Sarkis, Tennant, Humble, Schleife, Kandala, Banerjee, "Benchmarking quantum simulation with neutron-scattering experiments" (Mar 2026, v3 Apr 2026). IBM superconducting, up to 50 qubits; KCuF3 (1D Luttinger liquid) vs INS; 1D XXZ+NNN for CsCoX3. 1D, so DMRG-tractable; no advantage claim.
- arXiv:2607.07138 [VERIFIED abs] Granet, Murota, Dreyer, Yamamoto, Pedersen, Suwa, "Dynamical structure factor with a pumping approach on a trapped-ion quantum computer" (Jul 2026). Quantinuum Reimei; 1D Heisenberg 20 sites; copper sulfate.
- arXiv:2410.03958 [VERIFIED listing] Bauer et al., "Simulating Neutron Scattering on an Analog Quantum Processor" (Oct 2024).
- arXiv:2607.02673 [VERIFIED listing] Millar et al., "Quench Spectroscopy of Magnetic Excitations on a Superconducting Quantum Processor" (Jul 2026).
- arXiv:1912.06076 [VERIFIED listing] Baez et al., "Dynamical structure factors of dynamical quantum simulators".
- arXiv:1910.14213 [VERIFIED listing] Sels et al., "Quantum generative model for sampling many-body spectral functions" (QPE-based sampling of S(q,w)).
- arXiv:2508.15935 [VERIFIED listing] Kunitsa et al., "Quantum Simulation of Electron Energy Loss Spectroscopy for Battery Materials" (Aug 2025).
- arXiv:2407.04205 [VERIFIED abs] Umeano, Jamet, Lindoy, Rungger, Kyriienko, "Quantum subspace expansion approach for simulating dynamical response functions of Kitaev spin liquids", Phys. Rev. Materials 9, 034401 (2025). Pure honeycomb Kitaev model, T=0, finite field, small simulated systems.
- arXiv:2203.15291 [VERIFIED abs] Tazhigulov et al. (Chan group + Google), "Simulating challenging correlated molecules and materials on the Sycamore quantum processor" (2022): small alpha-RuCl3 model; details of the observable not in abstract.
- arXiv:2604.16164 [VERIFIED abs] Xiong, Wang, Cai, Yuan, "A unified framework for efficient quantum simulation of nonlinear spectroscopy" (Apr 2026). n-th order response via generalized parameter shift; 12-qubit XXZ on IBM hardware; spin-liquid quasiparticle example.
- arXiv:2401.03015 [VERIFIED listing] Szasz et al., kagome Heisenberg ground-state energy and magnetization curve on Quantinuum H1-1, 8-12 spins.
- arXiv:2602.20270 [VERIFIED listing] Loaiza et al., quantum algorithm for RIXS in battery materials; molecular cluster, 20 orbitals, 2.0e10 Toffoli, 414 logical qubits.

### Quantum-vs-classical frontier studies (for context)
- arXiv:2503.20870 [VERIFIED abs] Haghshenas et al., "Digital quantum magnetism on a trapped-ion quantum computer", Nature 653, 56-62 (2026). Quantinuum H2, TFIM on square and triangular lattices, thermalization/hydrodynamics; claims results "severely challenge classical simulation methods".
- arXiv:2403.00910 [VERIFIED abs] King et al., "Beyond-classical computation in quantum simulation", Science 388, 199-204 (2025). Annealer quench dynamics of spin glasses; claim vs TN and NQS (subsequently challenged by TN/NQS groups; challenge papers not re-verified here [UNVERIFIED]).
- arXiv:1911.03446 [VERIFIED abs] King et al., "Scaling advantage in quantum simulation of geometrically frustrated magnets", Nat. Commun. (doi:10.1038/s41467-021-20901-5). Million-fold speedup in relaxation vs PIMC with cluster updates, stoquastic Hamiltonian. Category D-type claim (single classical dynamics proxy).
- arXiv:2511.02125 [VERIFIED abs] Granet et al. (Quantinuum), "Superconducting pairing correlations on a trapped-ion quantum computer" (Nov 2025, v2 Feb 2026). Helios; field-driven nonequilibrium pairing at half filling, d-wave checkerboard 1/6 doping, bilayer s-wave (nickelate-motivated).

### Strong classical competitors
- arXiv:2303.08184 [VERIFIED listing] Mendes-Santos et al., NQS spectral functions of 2D quantum Ising up to 24x24.
- arXiv:2505.14571, 2505.23699 [VERIFIED listing] Burkard et al., high-temperature expansion of dynamic correlations for frustrated spins.
- arXiv:2409.03097 [VERIFIED listing] Begusic et al., "Real-time operator evolution in two and three dimensions via sparse Pauli dynamics". Also 2306.16372, 2308.05077 (classical simulation of IBM utility experiment).
- arXiv:2307.08083 [VERIFIED listing] Tu et al., PEPS generating function for DSF.
- arXiv:1802.02854 [VERIFIED listing] Yamaji et al., exact finite-T spectra (FTK-omega) for frustrated spins (Kitaev-Heisenberg).
- arXiv:2503.11596 [VERIFIED listing] Potten et al., Keldysh pseudo-fermion FRG for quantum magnetism dynamics.
- arXiv:2003.11876 [VERIFIED listing] Gohlke et al., iDMRG + LSWT for K-Gamma-Gamma' model in field.
- arXiv:2602.10190 [VERIFIED abs] Kim, Mourigal, "Semiclassical Routes to the alpha-RuCl3 Scattering Continuum via Model Meta-Analysis" (Feb 2026). 38 published exchange parameter sets; stochastic Landau-Lifshitz with quantum corrections + 24-site ED; concludes high-T continuum is correlated paramagnetism below theta_CW, quantum fractionalization not required. IMPORTANT for lesson 5.
- arXiv:2202.10715 [VERIFIED abs] Samarakoon et al., PRR 4, L022061 (2022): alpha-RuCl3 parameters from INS via ML; forward model = semiclassical LL dynamics + MC; ED only as a check.
- arXiv:2609.22535 [VERIFIED abs] Luo, Williams, Wu, Dahlbom, Batista, Zhang, "Approaching the Inverse Neutron Scattering Problem with Neural Networks" (Sep 2026): forward model LSWT only (fully polarized honeycomb).
- arXiv:2507.16558 [VERIFIED abs+html] Okubo, Nasu, Misawa, Motome, "Thermal Hall transport in Kitaev spin liquids" (2025). kappa_xy from static energy polarization P_E, J_E = i[H,P_E], kappa_xy = (2/L') d<J_E_parallel>_T/dT; XTRG MPO, D=500, 72-spin (6x6) honeycomb, K-Gamma-Gamma'-h. Quote: "The bond dimension D=500 is not sufficient to yield reliable results at low temperatures for h<~0.04"; quantization window T >> v/L' not reachable at this size.
- arXiv:2401.09551 [VERIFIED abs+html] Desrochers, Kim, PRB 109, 144410 (2024), SCEBR for finite-T dynamics of 0-flux and pi-flux QSI. Quote: "the sign problem in QMC for J+-<0 makes any theoretical predictions for pi-QSI, apart from its existence close to the Ising point, extremely challenging." ED benchmark at 32 sites; "The only available method is arguably the large-N approximation of gauge mean-field theory."
- arXiv:2201.00828 [VERIFIED listing] Hosoi et al., Ce2Zr2O7 neutron signatures via ED + MD.
- arXiv:2301.05240, 2406.18650, 2502.14067 [VERIFIED listing] Desrochers / Zhou et al., GMFT for DO QSI spectra and field response.
- arXiv:2101.08787 [VERIFIED listing] Astrakhantsev et al., pyrochlore Heisenberg: ED up to 4x4^3? and NQS up to 4x3^3 = 108 spins, ground state only (no dynamics).
- DMFT solvers: arXiv:2312.13668 (FTPS-METTS finite-T impurity solver, Sr2RuO4), 2410.16791 (NORG ab initio DMFT incl. La3Ni2O7), 2607.13993 (iNORG), 2607.00702 (tensor cross interpolation weak-coupling solver), 2603.15741 (NN embedding solvers) [all VERIFIED listing].
- arXiv:1808.01682 [VERIFIED listing] Peng et al., Bi2201 paramagnons; DQMC of three-band Hubbard S(Q,w) across doping.

### Experiments / materials anchors
- arXiv:2404.04207 [VERIFIED listing] Gao et al., "Emergent photons and fractionalized excitations in a quantum spin liquid" (polarized INS, Ce2Zr2O7 as DO pi-flux QSI).
- arXiv:1901.10092, 2209.04590 [VERIFIED listing] Gao et al., Ce2Zr2O7 continuum and field effects. arXiv:2209.03235 [VERIFIED listing] Lovesey comment disputing the U(1)pi analysis.
- arXiv:2203.00282, 2112.12254 [VERIFIED listing] Na2Co2TeO6 / Na3Co2SbO6 INS.

### Quantum algorithms / other quantum work in the lens
- arXiv:2311.09207 [VERIFIED abs] Chen, Kastoryano, Gilyen, "An efficient and exact noncommutative quantum Gibbs sampler".
- Quantum DMFT: arXiv:1910.04735 (Rungger et al., hardware DMFT), 2404.09527 (Selisko et al., 14 qubits, Ca2CuO2Cl2), 2601.10594 (Karabin et al., SIAM VQE), 2508.00118 (Ayral lecture notes), 2601.19896 (Rangi et al., real-time DMFT for near-term QC) [VERIFIED listing]. Bauer, Wecker, Millis, Hastings, Troyer PRX 2016 [UNVERIFIED in this session].
- Defects: arXiv:2112.04435 (Huang, Govoni, Galli et al., spin defects on quantum computers, VQE on QDET Hamiltonians), 2105.04736 (Vorwerk et al. review), 2607.14025 (WEST code, QDET) [VERIFIED listing].

## Candidates

### C1. Low-temperature S(q,w,T) of 3D dipolar-octupolar pi-flux quantum spin ice (Ce2Zr2O7, Ce2Sn2O7, Ce2Hf2O7)
- INPUT: DO pyrochlore XYZ Hamiltonian (Jx, Jy, Jz, Jxz, g-tensor, field h) on N = 16 L^3 sites (L = 2, 3 -> 128, 432 spins), temperature T ~ 0.1-1 J+-, INS kinematic grid (|Q| up to ~2.5 A^-1, dE ~ 0.01 meV).
- OUTPUT: polarized-neutron S(q,w,T) (spin-flip / non-spin-flip channels), spinon continuum lineshape and the low-energy spectral weight near q -> 0 (photon contribution); likelihood of each published parameter set given INS data.
- Why classically hard: 3D kills DMRG/TN; QMC has a sign problem for J+- < 0 (pi-flux) [verified quote, 2401.09551]; ED is 32 sites; NQS on pyrochlore exists only for ground states (108 spins, 2101.08787); available dynamics methods are GMFT, SCEBR, parton, MD (classical spins) - all uncontrolled.
- Quantum mechanism: digital Hamiltonian simulation (Trotter or qubitization) of a local 3D spin-1/2 model; prepare low-T state (Gibbs sampler of 2311.09207 or ground state via QPE from a GMFT/NQS trial state), measure C_ab(q,t) with Hadamard test / ancilla-free linear response, Fourier transform; or QPE-based spectral sampling (1910.14213). The speedup is on real-time dynamics of a 3D frustrated sign-problem Hamiltonian, which has no known polynomial classical algorithm; not a search over a classical landscape.
- Novelty: B. In arXiv abstract searches through 2026-09-28, quantum S(q,w) computations found are 1D (KCuF3, CsCoX3, CuSO4, Heisenberg chains) or pure Kitaev QSE (2407.04205); a search "quantum spin ice quantum computer / quantum simulator pyrochlore" returned 20 hits with none using quantum hardware or quantum algorithms.
- Main failure risk: (i) information vs computation: GMFT/SCEBR + 32-site ED may already fit polarized INS within experimental resolution, so exact dynamics does not change the model ranking; (ii) the emergent photon bandwidth scales as J+-^3/Jz^2, requiring evolution times far beyond 1/J (costly for the quantum side too); (iii) model floor: disorder/oxygen non-stoichiometry and multipolar form factors (Lovesey comment 2209.03235); (iv) low-T state preparation in a U(1) QSL (Gibbs mixing time).
- Rough resources: 128-432 logical qubits; per (q,t) circuit ~ (terms ~6N) x (J t_max / dt) ~ 1e3 x 1e3 ~ 1e6 two-qubit rotations (Trotter, t_max ~ 100/J); plus state prep; ~1e4 shots per point. Early fault-tolerant; not NISQ.
- Verdict: plausible (best in lens).

### C2. Intermediate-field S(q,w) model discrimination for Kitaev-Gamma honeycomb magnets (alpha-RuCl3, Na2Co2TeO6)
- INPUT: J-K-Gamma-Gamma'-J3 (+ interlayer) Hamiltonian candidates (38 published sets per 2602.10190), in-plane field h near and above h_c (~7-8 T for alpha-RuCl3), T << J; INS S(q,w) data.
- OUTPUT: S(q,w;h) with quantum fluctuations on 100-200 site clusters; posterior ranking of parameter sets; predicted field-dependent magnon breakdown continuum.
- Classical SOTA: 24-site ED (standard forward check), stochastic LL + quantum corrections (2602.10190), LSWT/NLSWT, iDMRG/tMPS on narrow cylinders (2003.11876), Keldysh pf-FRG (2503.11596), FTK-omega (1802.02854), Majorana MFT+RPA (2503.10330). Failure: in the field-induced disordered/near-critical regime LSWT breaks down; ED is 24 sites; cylinders width-limited; entanglement growth limits t_max.
- Quantum mechanism: adiabatic preparation from the high-field polarized product state (a natural initial state) down to h > h_c, then real-time correlators; parameter inference loop stays classical and the quantum device is the forward model only.
- Novelty: B. Quantum work exists for the pure Kitaev model (2407.04205, simulated) and 1D INS materials; no quantum computation of extended K-Gamma field-dependent S(q,w) or quantum-vs-classical study against cylinder DMRG / ED found.
- Main risk: Kim & Mourigal 2026 find semiclassics sufficient for the high-T continuum; high-field polarized phase is LSWT-exact enough; model floor from interlayer coupling, stacking faults, and 3D effects; DMRG cylinders may converge to INS resolution in the gapped high-field phase (gap -> finite correlation length -> TN easy). Hardness concentrates at h ~ h_c, where adiabatic prep also slows.
- Verdict: plausible (need decision-flip pre-test: does exact S(q,w) at h ~ h_c change the ranking of the 38 sets vs ED24+LL?).

### C3. Low-temperature thermal Hall conductivity kappa_xy(T,h) of extended Kitaev models via static energy polarization
- INPUT: K-Gamma-Gamma'-h honeycomb Hamiltonian, strip geometry L x L', T range down to ~0.005-0.01 |K|, fields h <~ 0.04.
- OUTPUT: kappa_xy(T,h)/T and whether a half-quantized plateau survives with Gamma, Gamma'; comparison to (contested) alpha-RuCl3 measurements.
- Classical SOTA: XTRG MPO D=500 on 72 spins (2507.16558) - explicitly unreliable at low T for h <~ 0.04 and too small for T >> v/L'; TPQ ED ~24-32 sites; sign-free QMC only for the pure Kitaev model (Majorana representation); LSWT magnon thermal Hall for ordered phases.
- Quantum mechanism: quantum Gibbs state preparation (2311.09207 or METTS-type sampling on hardware) of a 2D non-stoquastic Hamiltonian on L' large enough for the quantization window, then measurement of <J_E_parallel>_T, a sum of local 3-site operators (cheap observables, no long-time dynamics). The advantage would be in thermal-state preparation for a sign-problem 2D Hamiltonian at low T.
- Novelty: A/B. In arXiv abstract searches ("thermal Hall" + quantum algorithm / quantum computer; quantum algorithm + Kubo/transport coefficient), no quantum algorithm or quantum hardware computation of thermal Hall conductivity of spin models was found.
- Main risk: Gibbs-sampler mixing time at low T in a topological / gapless phase may be large; temperature derivative of a small edge current amplifies shot noise (O(1/eps^2) with small eps); model floor: phonon thermal Hall dominates measured signals in alpha-RuCl3 (2501.11272, 2303.03067 [VERIFIED listing]) so the computed magnetic kappa_xy may not be decision-relevant for data; iPEPS/NQS at finite T not yet tried at scale (strong classical attack available).
- Verdict: plausible (novel framing; high risk).

### C4. Momentum-resolved RIXS / S(q,w) of doped 2D three-band Hubbard models (cuprate paramagnons, bilayer nickelate La3Ni2O7)
- INPUT: three-band (Emery) or bilayer two-orbital Hubbard parameters, doping p, core-hole potential, incident energy/polarization; clusters of 16-64 Cu/Ni.
- OUTPUT: Kramers-Heisenberg RIXS intensity I(q,w) along high-symmetry cuts; paramagnon dispersion and damping vs doping.
- Classical SOTA: ED of small clusters (~8-12 Cu), DQMC + MaxEnt at elevated T (1808.01682), DMRG for ladders, DMFT/cluster DMFT; NORG DMFT for La3Ni2O7 (2410.16791). Failure: real-frequency, doped 2D, low T.
- Quantum mechanism: fermionic Hamiltonian simulation + core-hole intermediate-state propagation (resolvent via QSVT or time-domain Kramers-Heisenberg), as in the molecular RIXS algorithm of 2602.20270 but on a lattice.
- Novelty: B. Quantum RIXS algorithm found only for molecular clusters (2602.20270, cathode O2-Mn); no lattice RIXS quantum algorithm or advantage study found.
- Main risk: model floor (three-band parameters, core-hole approximation, phonons); fermionic 2D resources are large (Jordan-Wigner / compact encodings); DQMC and cluster DMFT paramagnon results may already match data within RIXS resolution (~30-40 meV), so decision value unclear; overlaps previous-week RIXS searches.
- Verdict: weak-plausible.

### C5. Nonlinear THz (2D coherent) spectroscopy of 2D non-integrable Kitaev/QSL candidates
- INPUT: extended Kitaev Hamiltonian, THz pulse polarizations, delays t1, t2.
- OUTPUT: chi^(3)(t1,t2) and rephasing/non-rephasing 2D spectra; spinon/Majorana echo signatures.
- Classical SOTA: exact Majorana solutions for pure Kitaev; ED (2301.11243); four-spinon / projection methods for 1D CoNb2O6 (2512.16829, 2512.20209); tMPS in 1D.
- Quantum mechanism: multi-time response functions via generalized parameter shift or ancilla interferometry (2604.16164).
- Novelty: C (quantum framework exists 2604.16164 on 12-qubit XXZ; no quantum-vs-classical study for 2D Kitaev 2DCS).
- Main risk: experimental 2DCS data for 2D QSL candidates is scarce (existing data are 1D CoNb2O6 or ordered FePS3, 2605.20067), so benchmark against measurement is weak; high-order responses need many circuits.
- Verdict: weak.

### C6. Real-frequency multi-orbital f-electron impurity spectra for heavy-fermion DFT+DMFT
- INPUT: 7 f-orbitals with SOC + crystal field + full Coulomb, discretized bath (~10-30 bath orbitals/orbital), T.
- OUTPUT: real-frequency impurity Green's function, Kondo resonance, quasiparticle weights; ARPES-comparable spectra.
- Classical SOTA: CTQMC-hyb (sign problem with off-diagonal hybridization/SOC at low T; needs analytic continuation), FTPS/METTS (2312.13668), NORG/iNORG (2410.16791, 2607.13993), tensor cross interpolation (2607.00702), NN surrogates (2603.15741).
- Quantum mechanism: impurity Green's function via Hamiltonian simulation / Krylov or QPE-sampling on ~100-400 spin-orbitals.
- Novelty: C (quantum DMFT demonstrated repeatedly: 1910.04735, 2404.09527, 2601.10594, 2601.19896; no advantage study vs FTPS/NORG for 7-orbital SOC f-shells).
- Main risk: lesson 6 - U, J, double counting, bath discretization and DMFT self-consistency dominate error; noisy Green's functions destabilize self-consistency.
- Verdict: weak.

## Killed ideas
- 1D INS S(q,w) (KCuF3, CsCoX3, copper sulfate, Heisenberg chains): DMRG/Bethe ansatz exact to INS resolution; already done on 50-qubit IBM (2603.15608) and Quantinuum Reimei (2607.07138). Category C/D with no possible advantage.
- Paramagnetic / high-T INS continua, NMR 1/T1 and ESR linewidths of frustrated magnets: high-T expansions (2505.14571), sparse Pauli dynamics in 2D/3D (2409.03097), semiclassical LL (2602.10190) suffice; same failure as the protein NMR OTOC lane (lesson 5).
- Defect multiplets (NV-, SiV, hBN, T-centre): QDET effective Hamiltonians are small enough for classical FCI; embedding/double-counting error dominates (lesson 6); quantum computation already done (2112.04435).
- Superconducting pairing symmetry in Hubbard / nickelate bilayer: demonstrated on Helios (2511.02125); DMRG/AFQMC/iPEPS strong; single-band model floor.
- Stoquastic frustrated TFIM finite-T phases and relaxation: sign-free QMC; NQS DSF up to 24x24 (2303.08184); annealer claim is vs PIMC dynamics only (1911.03446, category D) and quench-dynamics claim is contested (2403.00910, category E).
- Shastry-Sutherland SrCu2(BO3)2 thermodynamics / plateaus: iPEPS and finite-T tensor networks treat it (not re-verified here [UNVERIFIED]); no solver-limited decision identified.
- Moire FCI (twisted MoTe2) phase diagrams: continuum-model parameter and band-mixing uncertainty dominates (model floor); ED/DMRG/NQS active; arXiv formula indexing blocked verification here -> deferred, not a candidate.
- Superconducting-qubit flux noise / TLS surface-spin baths: effectively high-T spin baths where cluster expansions converge (same as prior molecular spin-qubit decoherence kill).
- Magnon lifetimes in 3D ordered magnets: nonlinear spin-wave 1/S expansion controlled; no hardness.
- Hamiltonian inference loop itself (fitting parameters): an argmin over a classical objective; quantum search would be at most quadratic (lesson 3). Only the forward S(q,w) evaluation can carry advantage (built into C1/C2).

## Pre-registration hooks (for whichever candidate escalates)
- Decision-flip test before any quantum work: compute, classically, the ranking of published parameter sets under (a) best cheap forward model (LSWT/LL/GMFT) and (b) best exact-on-small-cluster model (ED 24-32, cylinder DMRG). If rankings agree and match data within resolution, the lane dies (information vs computation).
- Classical adversary ladder not stopped early: ED -> DMRG/tMPS cylinders -> NQS dynamics -> pf-FRG -> sparse Pauli -> high-T expansion.
- Model-floor bound: vary Hamiltonian parameters within published uncertainty; solver error must exceed the parameter-induced spread.
