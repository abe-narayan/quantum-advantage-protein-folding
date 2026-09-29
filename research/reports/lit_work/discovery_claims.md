# Discovery lens: audit of 2023-2026 quantum advantage / utility claims on physical simulation

Date: 2026-09-28. Status: COMPLETE (final save; candidates and kills at the end of this file). WebSearch budget exhausted; searches via arXiv API / OpenAlex / Crossref / arXiv abs pages.

Correction (2026-09-28, later in session): arXiv:2504.07344 (Park, Gray, Chan, PRB 112, 174310 (2025)) simulates the IBM heavy-hex kicked-Ising experiment with influence-functional BP, NOT the D-Wave experiment as first logged below.

## Query log
- WebSearch "D-Wave beyond-classical quantum simulation spin glass Science 2025 tensor network rebuttal" -> budget exhausted (no results)
- WebFetch arXiv abs 2403.00910 (D-Wave King et al., Science 388,199 (2025)) [VERIFIED]
- WebFetch arXiv abs 2503.05693 (Tindall, Mello, Fishman, Stoudenmire, Sels: 2D/3D TN-BP of D-Wave dynamics) [VERIFIED]
- WebFetch arXiv abs 2503.08247 (Mauron & Carleo: t-VMC Jastrow up to 128 spins, errors <7%) [VERIFIED]
- WebFetch arXiv abs 2506.10191 (Google OTOC(2) "Constructive interference at the edge of quantum ergodic dynamics") [VERIFIED]
- WebFetch arXiv abs 2510.19550 (Google NMR OTOC toluene / dimethylbiphenyl in liquid crystal) [VERIFIED]
- arXiv API: abs:OTOC AND abs:classical AND abs:simulation (sorted by date) -> found 2604.15427 (Bermejo, Villalonga, Ware, Vidal, Szasz: TN-BP cannot simulate Quantum Echoes), 2607.15493 (Chiew: operator shadows, exponential learning separations for dynamical correlators)
- arXiv abs 2306.14887 (Tindall et al. PRX Quantum 5,010308 (2024), IBM Eagle TN-BP) [VERIFIED]; 2306.16372 (Begusic & Chan, sparse Pauli dynamics) [VERIFIED]; 2308.05077 (Begusic & Chan converged) [VERIFIED via listing]
- arXiv abs 2503.20870 (Quantinuum H2 digital magnetism, Nature 2026) [VERIFIED]
- arXiv API: Fermi-Hubbard AND pairing AND trapped-ion -> 2511.02125 (Granet et al., Helios pairing correlations) [VERIFIED]
- arXiv API: "quantum advantage" AND "Pauli propagation" -> 2511.21651, 2606.20441, 2603.27532
- arXiv API: "quantum advantage" AND "observable estimation" -> 2607.16116 (Sun et al., FT quantum-classical crossover, mixed-field Ising) [VERIFIED abs]
- arXiv API: "sample-based quantum diagonalization" -> critiques 2608.11569, 2608.05314, 2605.02494, 2603.13160, 2608.16436; classical alt 2606.26760
- arXiv API: "dynamical structure factor" AND "quantum computer" -> 2603.15608 (IBM/ORNL KCuF3 50-qubit vs INS, 1D) [VERIFIED], 2607.07138 (Quantinuum Reimei pumping DSF, 1D Heisenberg 20 sites + copper sulfate) [VERIFIED]
- arXiv API: "belief propagation" AND quantum AND experiment -> 2504.07344 (Park et al., TN influence-functional BP on D-Wave 2D) , 2308.05077
- arXiv abs 2405.17385 (Google analog-digital XY thermalization, 69 qubits, beyond-classical claim) [VERIFIED]
- arXiv API: "classical simulation" AND (Quantinuum OR H2) AND Ising -> no rebuttal of 2503.20870 found in this query
- arXiv API: Fermi-Hubbard AND dynamics AND beyond AND classical -> 2605.04025 (IBM 1D FH L=60 "~3000x vs TDVP chi=4096"), 2606.04771 (Rausch: GPU TN chi~62000, advantage reduced to ~36x), 2510.26845 (Phasecraft/Google Willow 6x6 2D FH, "beyond exact state-vector") [VERIFIED abs], 2510.26300 (Quantinuum 56-qubit 2D FH, beyond exact), 2511.02809 (D'Anna: Majorana-string propagation, 2D FH quenches)
- arXiv API: "neutron scattering" AND quantum computer/computing/algorithm -> 1809.07974 (Chiesa et al., Nat Phys 2019, 4D INS on hardware), 1804.01505 (Roggero & Carlson linear response), 2309.15165 (Wall: quantum TN spectral functions for molecular nanomagnets), 2603.15608, 2607.07138
- arXiv API: DSF AND finite temperature AND (triangular|kagome|Kitaev) -> only old classical (1711.05375 NLCE kagome)
- Crossref: Laurell & Okamoto npj Quantum Mater. 2020 doi:10.1038/s41535-019-0203-y [VERIFIED]
- arXiv API: DSF AND (TN|DMRG|NQS) AND two-dimensional -> 2303.08184 (Mendes-Santos NQS spectral functions 24x24 TFIM, T=0), 2307.08083 (PEPS generating function, T=0)
- arXiv abs 2607.15493 (Chiew, Angrisani, Holmes: operator shadows, OTOC learning lower bounds) [VERIFIED]
- arXiv API: (solid-state NMR|dipolar) AND quantum computer AND (spin diffusion|multiple-quantum|FID) -> 0 results
- arXiv API: NMR AND "quantum computer" AND spectra -> all liquid-state: 2609.17102 (21-spin on Quantinuum), 2512.14513 (34 spins), 2404.17548, 2508.06448 (Fratus: classical cluster solver linear scaling challenges quantum NMR advantage), 2609.20406 (shot noise), 1910.14221 (Sels QABC)
- arXiv API: Rydberg AND (beyond classical|classically intractable|quantum advantage) AND dynamics -> 2603.20372 (Pasqal: one-to-one 256-qubit simulation of TmMgGaO4, magnetization vs single-crystal data; quench "beyond classical reach") [VERIFIED abs]
- arXiv API: RIXS AND quantum computing -> HTTP 429
- arXiv abs 2210.14109 (Yoshioka et al., npj QI 2024: 2D Heisenberg/Hubbard ground-state crossover, hours, few 1e5 physical qubits) [VERIFIED]
- arXiv abs 2303.08376 (Xu, Chung, Qin, Schollwoeck, White, Zhang, Science 384 adh7691 (2024): t' Hubbard stripes + SC, DMRG+AFQMC) [VERIFIED]
- arXiv API "Hamiltonian learning" AND (neutron|structure factor|spectroscopy) -> HTTP 429
- OpenAlex RIXS quantum computer -> HTTP 429; Crossref RIXS quantum computer -> no quantum-computing lattice RIXS paper among top 15 hits

## Interim audit table (claims -> status)
| Claim | Observable | Category | Rebuttal / status | Open residue |
|---|---|---|---|---|
| IBM kicked-Ising utility, Kim et al. Nature 618, 500 (2023) [UNVERIFIED ref; rebuttals VERIFIED] | single-site/weight-k Pauli expectations after Floquet kicked-Ising on heavy-hex, 127 q | E | Tindall et al. 2306.14887 (TN-BP, PRX Quantum 2024), Begusic & Chan 2306.16372 / 2308.05077 (sparse Pauli dynamics) | nothing practical; heavy-hex low connectivity + Clifford-near angles |
| D-Wave quench dynamics, King et al. Science 388,199 (2025), 2403.00910 | Coherent-anneal correlation functions / KZ in 2D,3D, inf-D spin glasses | E (contested) | Tindall et al. 2503.05693 (2D/3D TN-BP), Mauron & Carleo 2503.08247 (t-VMC, 128 spins, <7%), Park et al. 2504.07344 (TN influence-functional BP) | 3D and dense (inf-D) graphs at long anneal times less clearly covered; no practical observable |
| Google Quantum Echoes OTOC(2), 2506.10191 (Nature 2025) | OTOC(2) of random-ish circuits, 103 q | claimed, standing (not E as of 2026-09) | Defended by Google-affiliated 2604.15427 (TN-BP infeasible) | Practical use (Hamiltonian learning) not shown at hard scale; NMR follow-up 2510.19550 was classically simulable scale |
| Google NMR OTOC, 2510.19550 | H-H distances/dihedral from LC-NMR echoes (toluene, DMBP) | C/D (no advantage at this size) | classically simulable size | liquid-crystal oriented molecules, lesson 5 info floor |
| Google analog-digital XY, 2405.17385 (Nature 2025) | KT/KZ thermalization, 69 q | D/claimed | no rebuttal found in queries run | none practical |
| Quantinuum digital magnetism H2, 2503.20870 (Nature 2026) | 2D Ising thermalization, diffusion constants | claimed, no rebuttal found in queries run | - | diffusion constants at infinite/high T are Pauli-propagation friendly (DAOE-type) - likely attackable |
| Quantinuum Helios pairing, 2511.02125 | pairing correlations, square/checkerboard/bilayer (nickelate) Hubbard | C (demo, no advantage claim) | - | bilayer nickelate model |
| IBM 1D FH, 2605.04025 | quench, L=60, t=6 | E | Rausch 2606.04771: chi~62000, 3000x -> ~36x | 1D is classically favourable |
| Phasecraft/Google 2D FH 6x6, 2510.26845; Quantinuum 2D FH 56 q, 2510.26300 | polarons, stripes, thermalisation | D (beyond exact statevector only; compared vs TN and operator propagation) | Majorana-string propagation 2511.02809 | 2D doped dynamics at longer times |
| Pasqal TmMgGaO4 one-to-one, 2603.20372 | magnetization vs crystal data; quench dynamics | equilibrium part classically easy (stoquastic TFIM -> QMC); quench claim D | - | INS-type S(q,w) not done |
| IBM/ORNL KCuF3 vs INS, 2603.15608; Quantinuum Reimei DSF, 2607.07138 | S(q,w) 1D | C (1D is DMRG-easy; usefulness not advantage) | - | 2D/3D frustrated, finite T, non-stoquastic |
| IBM SQD chemistry (Fe-S etc.) | ground-state energies | D/E | 2608.11569, 2608.05314, 2605.02494, 2603.13160 | none |
| FT crossover mixed-field Ising, 2607.16116 | dynamics observables 1D/2D | theoretical resource (cat 3/6) | - | 2D crossover at modest sizes -> any practical 2D dynamics observable inherits |
- arXiv abs 2504.07344 -> Park, Gray, Chan (IF-BP), kicked Ising heavy-hex (IBM), PRB 112,174310 (2025) [VERIFIED]
- Crossref: Samarakoon et al. Nat Commun 2020 doi:10.1038/s41467-020-14660-y (ML-assisted INS fitting, Dy2Ti2O7) [VERIFIED]; Sunny.jl not found in Crossref (cite as [UNVERIFIED])
- Crossref: Scheie et al. Nat Phys 20 (2024) doi:10.1038/s41567-023-02259-1 (KYbSe2 proximate QSL, INS) [VERIFIED]
- arXiv abs 2606.04771 (Rausch, Singh, Jahromi, Kshetrimayum, Orus) [VERIFIED]; 2605.04025 (Hartnett ... Biercuk, Baum; Q-CTRL on IBM; 120 qubits; 1D FH) [VERIFIED]
- arXiv API "quantum spin ice" AND (quantum computer|simulator|annealer|qubits) -> 2603.28125 (Giergiel and Surowka, 2D programmable dipolar spin ice on an annealer, 400+ vertices) [VERIFIED abs], 2305.08571 (qubit spin ice), 2404.04207 (Gao et al., Ce2Zr2O7 emergent photons, INS); no 3D pyrochlore QSI dynamics on quantum hardware
- Crossref: Smith, Lhotel, Petit, Annu Rev CMP 16 (2025) doi:10.1146/annurev-conmatphys-041124-015101 [VERIFIED]; Hosoi, Zhang, Patri, Kim, PRL 129, 097202 (2022) doi:10.1103/physrevlett.129.097202 [VERIFIED]; Potts, Moessner, Benton, PRL 133, 226701 (2024) doi:10.1103/physrevlett.133.226701 (2DCS of DO QSI) [VERIFIED]; Bhardwaj et al., npj QM 2022 doi:10.1038/s41535-022-00458-2 [VERIFIED]
- arXiv API La3Ni2O7 AND pairing AND (DMRG|QMC|quantum computer) -> 0 hits; all:nickelate AND bilayer AND DMRG -> 2605.25654, 2605.10101, 2602.20288 (RPA+DMRG: strong Hund -> s-wave, weak -> d-wave), 2602.04945, 2509.02673, 2502.13960, 2411.07292, 2408.02847, 2405.00092, 2309.15843, 2309.15095
- arXiv API "spin diffusion" AND "magic-angle spinning" AND (simulation|first principles) -> 1 irrelevant hit (2112.00438); Crossref MAS spin diffusion first principles -> Jia, Zhang, Chen JPCA 2008 doi:10.1021/jp077067u (phenomenological D vs MAS rate) [VERIFIED]
- arXiv API dipolar AND ensemble AND (TWA|cluster) AND (NV|P1|diamond) -> 2307.14188 (Graesser et al.: random dipolar ensembles in diamond; improved cluster mean-field recovers experiment) [VERIFIED listing]
- arXiv API RIXS AND quantum AND (qubits|quantum computer|quantum algorithm) -> only 2602.20270 (Loaiza, cluster RIXS for cathodes, QPE); no lattice momentum-resolved RIXS quantum study
- Crossref: Jia et al. Nat Commun 5, 3314 (2014) doi:10.1038/ncomms4314 (ED RIXS, doped AFM) [VERIFIED]
- arXiv API Kitaev AND quantum computer AND (dynamics|structure factor|correlation) -> no extended Kitaev-Heisenberg-Gamma S(q,w) study on quantum hardware
- arXiv API (DSF|linear response|spectral function|dynamical correlation) AND fault-tolerant AND resource -> no FT resource estimate for 2D frustrated S(q,w) (hits: 2603.02715, 2506.01204, 2408.14543)
- arXiv API (2DCS|nonlinear spectroscopy|nonlinear response) AND quantum (computer|algorithm|simulation) AND (spin|magnet) -> 2604.16164 (Xiong: unified framework for nonlinear spectroscopy, IBM 12-qubit 1D XXZ, no classical comparison), 2407.01313 (Mootz: adaptive variational chi3, statevector, small chains)
- Crossref doi:10.1038/s41586-023-06096-3 -> Kim et al., "Evidence for the utility of quantum computing before fault tolerance", Nature 618, 500-505 (2023) [VERIFIED]

## Claim audit, additional rows (final)
Row "D-Wave" in the interim table: Park et al. 2504.07344 concerns IBM, see correction at top. IBM Kim et al. now [VERIFIED].

| Claim | Observable | Category | Status | Nearby practical subproblem that inherits hardness |
|---|---|---|---|---|
| Q-CTRL on IBM 1D FH (2605.04025) | spin-charge separation, L=60, t=6 | E | 3000x -> ~36x (2606.04771) | none: 1D favours MPS |
| Pasqal TmMgGaO4 (2603.20372) | M(H), quench | static part classically easy (stoquastic TFIM, QMC); quench D | - | INS S(q,w) of non-stoquastic 2D magnets (C1) |
| IBM/ORNL KCuF3 (2603.15608), Quantinuum DSF (2607.07138) | 1D S(q,w) vs INS | C (usefulness, 1D) | - | 2D/3D, finite T (C1, C2) |
| IBM nonlinear spectroscopy (2604.16164) | chi(3), 12-qubit 1D XXZ | C | no classical comparison | THz 2DCS of 2D/3D frustrated magnets (C3) |
| Quantinuum Helios pairing incl. bilayer nickelate model (2511.02125) | pair correlations | C | - | bilayer nickelate pairing symmetry in 2D limit (C4) |
| Loaiza RIXS cathodes (2602.20270) | cluster RIXS via QPE | resource estimate without strongest-classical benchmark | - | lattice momentum-resolved RIXS (C5) |
| Google NMR OTOC (2510.19550) + liquid-state NMR hardware (2404.17548, 2512.14513, 2609.17102) | spectra, echoes | D/E for liquid state (Fratus 2508.06448) | - | solid-state MAS dipolar many-body (C6) |

## Rough break-even for C1 (order of magnitude; my estimate, not from literature)
- Model: N = 12x12 = 144 spin-1/2 on a triangular lattice, 3N = 432 bonds, anisotropic exchange ~5 rotations per bond per 2nd-order Trotter step -> ~2e3 rotations per step.
- Resolution dw ~ 0.05 J -> t_max ~ 60/J; dt ~ 0.1/J -> mean ~300 steps per circuit -> 6e5 rotations x ~40 T per rotation -> ~2.4e7 T gates per circuit.
- Circuits: 300 time points x ~1e4 shots (eps ~ 1e-2, all r measured in parallel with a linear-response protocol) -> 3e6 circuits -> ~7e13 T gates per full S(q,w) at ONE parameter point and ONE temperature.
- At 1 us per logical T: ~7e7 s (~2 years) on one logical processor. Amplitude estimation / Heisenberg-limited spectroscopy and QSP evolution might cut this by 1e2-1e3, parallel QPUs by a further factor. Classical YC6 DMRG S(q,w) at T=0: days to weeks on a cluster.
- Conclusion: full-spectrum fitting is not a break-even target. The defensible target is a DECISION version (discriminate 2-5 candidate Hamiltonians at a few (q,w) points where cylinder DMRG / METTS / NQS disagree), which cuts circuits by ~1e2-1e3. Shot overhead is this problem's analogue of the lesson-3 per-sample floor.

## Candidates (final)
1. C1. 2D non-stoquastic frustrated magnets: finite-T S(q,w) forward model and Hamiltonian discrimination from INS. Category C. Verdict: plausible.
2. C2. 3D pi-flux dipolar-octupolar quantum spin ice (Ce2Zr2O7 / Ce2Sn2O7 / Ce2Hf2O7): S(q,w) spinon continuum and photon signatures. Category B. Verdict: plausible (sharpest classical wall, weakest practicality).
3. C3. THz 2D coherent spectroscopy (third-order nonlinear response) of 2D/3D frustrated magnets. Category C. Verdict: plausible/weak.
4. C4. Bilayer two-orbital nickelate (La3Ni2O7) pairing symmetry in the 2D limit. Category C. Verdict: weak (model floor: 2602.20288 finds s <-> d flips with Hund coupling).
5. C5. Lattice momentum-resolved RIXS of doped 2D three-band Hubbard (cuprate paramagnons). Category B. Verdict: weak.
6. C6. Solid-state 1H MAS many-body dipolar dynamics: first-principles spin-diffusion coefficients for domain sizing in pharmaceutical amorphous solid dispersions. Category B (arguably A for MAS). Verdict: weak.

### Candidate details
- C1 INPUT: lattice + candidate H(theta) (XXZ + J_pmpm, J_zpm for Yb delafossites such as KYbSe2; or J-K-Gamma-Gamma-prime for alpha-RuCl3), g-tensor, T in [0.05, 1] J, instrument resolution, measured INS data. OUTPUT: S(q,w) with error bars on a q-path; likelihood ratio between candidate H; decision gapless continuum vs magnon at K/M. CLASSICAL: ED/FTLM 24-36 sites (Laurell and Okamoto 2020), tDMRG/tDVP on YC6-YC8 cylinders (T=0), METTS/purification (finite T, width <= 6), PEPS excitation / generating function (2307.08083), NQS dynamics (2303.08184), QMC+MaxEnt (sign-free only), NLCE (1711.05375), LSWT/NLSWT, SU(N) classical dynamics (Sunny [UNVERIFIED]), Schwinger bosons, ML-surrogate fitting (Samarakoon 2020). QUANTUM: product-state/METTS-like sampling + Trotter/QSP evolution + linear-response measurement of all-r correlators (Roggero and Carlson 1804.01505; pumping 2607.07138), Fourier transform to w. KILL TESTS: (a) at experimental resolution and T, spread among YC6/YC8 DMRG, NQS and LSWT is below the INS error bars -> kill; (b) parameter-posterior width from existing fits exceeds solver spread -> kill (model floor); (c) decision-version circuits x T-count > ~1e12 -> not break-even.
- C2: as C1 but 3D pyrochlore, N = 16 L^3 (L=2: 128, L=3: 432); pi-flux regime (QMC sign problem [standard knowledge, UNVERIFIED in this session]); TN weak in 3D. Classical: ED 16-32 sites (Hosoi 2022), gauge MFT, semiclassical spin dynamics, NLCE thermodynamics (Bhardwaj 2022). Risks: emergent-photon bandwidth ~ J_pm^3/J_zz^2 needs t >> 1e2/J_zz (deep circuits); sample disorder (Ce2Zr2O7+x); practical use is fundamental materials physics.
- C3 INPUT: H, pulse polarisations, T. OUTPUT: chi(3)(t1,t2) 2D spectra (rephasing / non-rephasing), lifetimes vs inhomogeneous broadening. Nested commutators of time-evolved magnetisation (OTOC-adjacent operator growth). Classical: ED, 1D tDMRG, large-S spin dynamics, free-fermion Kitaev, Potts-Moessner-Benton 2024 approximations for DO QSI. Risks: sparse experimental data; informativeness.
- C4 INPUT: bilayer two-orbital Hubbard-Kanamori (DFT hoppings, U, J_H, t_perp), doping, L x L x 2. OUTPUT: pairing symmetry, pair-correlation decay. Classical: DMRG ladders/cylinders, RPA/FLEX, AFQMC, DQMC (sign), DCA/CDMFT, iPEPS. Quantum: QPE/adiabatic from DMRG/AFQMC trial state, then pair correlators; resources cf. 2210.14109. Risks: lesson 6 (Hund-coupling sensitivity), QPE overlap.
- C5 INPUT: three-band Hubbard, core-hole potential U_c, lifetime Gamma, doping, q, polarisation. OUTPUT: RIXS I(q,w). Classical: ED small clusters (Jia 2014), DQMC susceptibility + MaxEnt, DCA, 1D DMRG. Quantum: time-domain Kramers-Heisenberg with core-hole Hamiltonian (short intermediate propagation ~ hbar/Gamma), long final-state evolution for resolution. Risks: model floor, decision relevance.
- C6 INPUT: 1H coordinates (crystal / MD amorphous), MAS rate, B0, pulse sequence. OUTPUT: spin-diffusion coefficient D, build-up curves, residual linewidths. Classical: LCL / restricted Liouville space (Dumez-Butler-Emsley [UNVERIFIED]), Floquet ED 12-16 spins, cluster/spinDMFT, Pauli propagation, phenomenological D (Jia-Zhang-Chen 2008). Quantum: time-dependent (MAS-modulated) Hamiltonian simulation of 50-200 dipolar spins; OTOC-style echoes. Risks: lesson 5 (D is calibrated empirically, 30-50% tolerance), classical convergence.

## Killed ideas
- IBM kicked-Ising utility observables as a target: E (2306.14887, 2306.16372, 2308.05077, 2504.07344).
- D-Wave spin-glass quench as a practical target: E / contested (2503.05693, 2503.08247); no practical observable; stoquastic equilibrium goes to QMC.
- Random-circuit OTOC(2) itself: a demonstration, not a practical problem; claim still standing (2604.15427).
- Oriented liquid-crystal molecular geometry via OTOC (2510.19550): already claimed; molecules below ~30 spins are exactly simulable; spectral-resolution floor (lesson 5).
- Liquid-state NMR spectra on quantum hardware: D/E (Fratus 2508.06448, linear-scaling cluster solver).
- SQD/QSCI chemistry ground states: D/E (2608.11569, 2608.05314, 2605.02494, 2603.13160).
- 1D Fermi-Hubbard quench: E (2606.04771).
- 2D FH quench demos (2510.26845, 2510.26300) recast as photo-doped Mott switching: model floor, NEGF, cold-atom microscopes; overlaps the killed doped-Mott-oxide transport topic.
- Infinite/high-T diffusion constants (Quantinuum 2503.20870 lineage): Pauli-propagation/DAOE-friendly regime; no practical decision.
- Dense dipolar electron-spin ensembles for sensor design: cluster mean-field recovers experiment (2307.14188); model floor (charge dynamics, strain).
- Magnetocaloric sub-K ADR materials: operating T >~ J where HTSE/QMC/NLCE converge; stoquastic cases go to QMC.
- NMR 1/T1 and muSR relaxation in quantum magnets: hydrodynamic long-time tails lie beyond any coherent-simulation horizon on both sides.
- Lattice-gauge string breaking / hadronisation (Rydberg/QuEra/Google): 1+1D is MPS-easy, 3+1D QCD far off; no practical near-term decision.
- Google analog-digital XY KT thermalisation (2405.17385): D; no practical observable.
- 2D mixed-field Ising FT crossover (2607.16116) as an application: it is a theory/resource result (claim categories 3/6), usable only as the enabling estimate for C1-C3.
