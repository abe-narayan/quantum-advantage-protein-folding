# Discovery lens: start from quantum algorithms (2026-09-28)

Status: COMPLETE (subagent pass, ~50 tool calls). Scope: quantum primitives with super-quadratic or evidence-backed exponential speedups for PHYSICAL OBSERVABLES, matched to a practical measured quantity, filtered through the protein-failure lessons (L1-L7 in the task brief). Supersedes the two interim checkpoints written earlier in this file (their content is folded in below).

Search infrastructure note: the WebSearch budget was exhausted (200/200) at the start of this pass. The arXiv export API and OpenAlex returned HTTP 429. Crossref worked but gave low-precision matches. The arxiv.org/search HTML interface (keyword "all" field, AND semantics) worked and carried most queries. It misses papers whose abstracts do not contain all query words, so every "not found" below applies only to the listed queries.

## 0. Algorithm -> observable map (what this lens produced)

| Primitive (2019-2026) | Speedup type | Matching practical observable | App-level quantum-vs-strongest-classical study found? |
|---|---|---|---|
| Hamiltonian simulation + linear response (Roggero & Carlson 1804.01505; GIT 2004.04889; Chebyshev 2110.02108; entangled QPE 2404.19554; robust quantum Arnoldi Green's functions at T>0, 2605.22920) | exponential vs exact classical when there is no sign-free or low-entanglement structure | dynamic structure factors: neutron (INS), X-ray Thomson (XRTS), lepton-nucleus, neutrino opacities | Only 1D INS on hardware (KCuF3, 2603.15608). None for XRTS, hot nuclear matter, 2D Kitaev |
| First-quantized plane-wave dynamics (Su et al. 2105.12767), incl. finite-T non-BO dynamics (Rubin et al. 2308.12352) | exponential vs exact, polynomial in eta and N | stopping power (claimed), XRTS DSF (not claimed), conductivity | Stopping power only (resource estimate, no classical head-to-head) |
| Gibbs samplers (CKG 2311.09207), TPQ (2310.07774), QITE thermal (2306.16580) | exponential only below dequantization thresholds (Bakshi-Liu-Moitra-Tang 2403.16850; Yin-Lucas 2305.18514) | finite-T spectra, thermodynamics of sign-problem systems | None at application level |
| Nuclear EFT simulation costs (Watson et al. 2312.05344) | exponential vs exact; competes with lattice-EFT AFQMC (pinhole trace, 1912.05105) | nuclear thermodynamics, response | Cost estimates only |
| Scattering / reaction wave packets (2603.26881, 2512.16138, 2407.04155, 2609.25164, 2006.01369) | exponential vs exact many-body continuum | reaction cross sections, resonances | Method papers; no advantage study vs NCSMC |
| Vibrational QPE / block encodings (2504.08065, 2307.07478) | polynomial-to-exponential in mode number | anharmonic IR spectra | No; classical VCI/vDMRG/MCTDH are strong |
| DOS / level density (VQE toy 2209.07820; nuclear response toy 2405.02255) | trace estimation (DQC1-like) | nuclear level density | Toy models only; SMMC reaches actinides (2509.26571) |

Cross-cutting pattern: the most defensible quantum gap is REAL-FREQUENCY dynamical response at finite temperature in fermionic systems with a sign problem. There, the strongest classical route gives exact IMAGINARY-TIME correlators (PIMC / AFQMC / GFMC / CC-LIT/GIT) and must then solve an ill-posed inversion. This gives a built-in validation channel: the Laplace transform of the quantum real-frequency output must reproduce the classical imaginary-time data wherever the latter is exact. The advantage claim then concerns only the information that the inversion cannot recover. This differs from the protein failure (L3): the quantity is not an argmin or ranking over a classical landscape, but a quantum dynamical correlator.

## 1. Candidates

### C1. Real-frequency XRTS dynamic structure factor of warm dense matter (ICF diagnostics)  [verdict: plausible-strong; novelty B]
- INPUT: element(s) and composition (H, Be, C, CH), mass density (rs ~ 1-4), electron temperature (theta = T/T_F ~ 0.3-1.5), scattering wavevector k, ion snapshots or quantum ions.
- OUTPUT: electronic S_ee(k, omega) over omega (plasmon, bound-free, free-free), and from it the inference of (rho, Z, T) from a measured XRTS spectrum.
- Practical use: XRTS is the main in-situ diagnostic of compressed matter at NIF/OMEGA/XFELs. The Chihara decomposition used for inference is contested (Baczewski et al. 1512.05795), and PIMC has already revised an inferred Be density (Schwalbe et al. 2504.13611). Users: ICF design and diagnostics groups, planetary-interior EOS groups.
- Quantum mechanism: first-quantized plane-wave electrons (+ ions, quantum or snapshot) (Su et al. 2105.12767; non-BO finite-T machinery in Rubin et al. 2308.12352). Thermal ensemble via a Gibbs sampler, microcanonical energy filtering (QPE-based) or TPQ. S(k, omega) via the density-density correlator <rho_k(t) rho_-k(0)> (Hadamard test / Roggero-Carlson linear response / robust quantum Arnoldi at T>0, 2605.22920). It replaces sign-limited PIMC + ill-posed analytic continuation, and TDDFT with an approximate xc kernel. The Hamiltonian is bare Coulomb, so there is no active-space or fitted-parameter model floor (L6 largely passed). The residual model error comes from pseudopotentials, finite size and BO for the ions.
- Classical SOTA: PIMC with xi-extrapolation (2403.01979); PIMC agreement with Be XRTS (Dornheim et al. 2402.19113); model-free ITCF temperature (2211.00579, 2604.25735); MaxEnt continuation (2501.01869); real-time wave-packet DSF (2407.08875); mixed stochastic-deterministic TDDFT DSF (White 2410.23599; Moldabekov et al. 2510.01875); Chihara codes (xDAVE 2604.27237).
- Why classically hard: the PIMC fermion sign grows exponentially with N/theta and density; recovering real-frequency S(k,omega) from the ITCF is exponentially ill-conditioned; TDDFT depends on an uncontrolled dynamic xc kernel; the bound-free separation is ambiguous.
- Novelty evidence: the arXiv queries "warm dense matter quantum algorithm", "quantum computing dynamic structure factor plasma", "Thomson scattering quantum computer" and "first-quantized quantum simulation finite temperature electron gas" returned no quantum-algorithm XRTS/DSF paper. The nearest work is quantum stopping power (2308.12352, PNAS 121, 2024). -> B.
- Main failure risk: (a) the ITCF already gives a model-free T (2211.00579), so decision-relevant new information must lie in real-frequency features (plasmon width, bound-free edge) that the measurement resolution (a few eV) can resolve (L5 information check). (b) In the hard regime (theta<0.5), thermal-state preparation cost and plane-wave counts (N ~ 1e5-1e6) push Toffoli counts to or beyond the stopping-power level (the abstract gives ~100x FeMoco-class Toffolis). (c) xi-extrapolation keeps extending the PIMC frontier.
- Rough resources: eta ~ 32-128 electrons, N ~ 1e4-1e6 plane waves; ~1e3-3e3 logical qubits; Toffolis per trajectory of the order of the stopping-power estimates (~1e11-1e13) [ESTIMATE, not computed]; ~1e3-1e4 shots per (k, t) grid point. Scaling variable: N_e at fixed (rs, theta), and theta decreasing at fixed N_e.
- Benchmark design: (i) UEG, where PIMC is exact: the Laplace transform of the quantum S(k,omega) must match the ITCF (validation). (ii) Hydrogen, then Be at NIF conditions. (iii) Decisive comparison: infer (rho, Z) from real NIF spectra under FULL (quantum S) vs ABLATION (best of PIMC+MaxEnt, TDDFT, Chihara) and compare posterior widths.

### C2. Real-frequency spin (axial) response of hot, neutron-rich nuclear matter for supernova neutrino opacities  [verdict: plausible; novelty B]
- INPUT: nuclear Hamiltonian (lattice chiral EFT at LO/NLO, or pionless for validation), density n ~ 0.01-1 n0, T ~ 3-30 MeV, proton fraction Y_p ~ 0.05-0.3, momentum transfer q.
- OUTPUT: S_A(q, omega) and S_V(q, omega) (axial/vector dynamic structure factors), and from them neutrino scattering and absorption opacities.
- Practical use: core-collapse supernova models are sensitive to opacity changes of ~10-20%. A modest strangeness-induced opacity reduction turns a failed 3D 20 Msun model into an explosion (Melson et al. 1504.07631, ApJL 808 L42). Production opacities use mean-field/RPA/Landau and virial corrections (Roberts & Reddy 1612.02764).
- Quantum mechanism: lattice nuclear-EFT Hamiltonian simulation (costed by Watson et al. 2312.05344); thermal state via Gibbs sampler / QITE (Turro 2306.16580) or microcanonical filtering; real-time spin-density correlator via linear-response algorithms (1804.01505, 2004.04889). It replaces AFQMC/pinhole-trace Euclidean data + inversion, and CC+GIT, which is limited to T=0.
- Classical SOTA: lattice-EFT pinhole-trace thermodynamics (Lu et al. 1912.05105, PRL 125 192502); CC+GIT spin response of neutron matter (Sobczyk, Jiang, Roggero 2407.20986); virial expansion at low density; AFDMC ground states; NQS for dilute neutron matter (2212.04436, 2407.21207).
- Why classically hard: realistic chiral forces (tensor, spin-orbit, 3N) and a finite proton fraction bring back the sign problem that SU(4)/pionless interactions avoid; the real-frequency spin response again requires inversion; CC works only at T=0.
- Novelty evidence: the queries "neutron matter quantum computer", "neutrino opacity neutron matter response" and "neutrino opacities dense matter dynamic response ab initio" found quantum thermal-state and EFT-cost papers but no quantum-vs-classical study of the hot-matter axial response. -> B.
- Main failure risk: model floor (L6). The chiral-EFT truncation error at n ~ n0 and T ~ 10 MeV may exceed the solver gap. Decision relevance depends on supernova sensitivity studies at the density and temperature where the solver gap is largest. The sign problem may be mild enough at LO for AFQMC to win.
- Rough resources: L^3 = 6^3-10^3 sites, 2-4 species x 2 spins -> ~1e3-8e3 qubits in second quantization (fewer in first quantization). Toffolis per time step follow the 2312.05344 scaling [not extracted]. Scaling variables: L (box) and Y_p.
- Benchmark design: validate on the unitary Fermi gas S(q,omega) (Bragg spectroscopy data; sign-free AFQMC exists), then move to chiral LO/NLO where the classical sign problem worsens. FULL vs ABLATION = quantum S_A vs the best Euclidean+inversion and CC-GIT.

### C3. Semi-exclusive (lepton + nucleon-knockout) neutrino-40Ar response for DUNE  [verdict: plausible; novelty C (inclusive) / B (semi-exclusive)]
- INPUT: 40Ar (12C/16O for validation) chiral-EFT Hamiltonian and currents, (q, omega), final-state channel selector (p/n knockout, residual-nucleus excitation).
- OUTPUT: semi-exclusive cross sections d sigma / (dE_l dOmega_l dT_N) and the final-state composition (proton multiplicity, missing energy) that event generators need.
- Practical use: the DUNE oscillation analysis reconstructs neutrino energy from final states. Generators rely on a factorized spectral function + a semi-classical intranuclear cascade (e.g. Isaacson et al. 2007.15570).
- Quantum mechanism: prepare the ground state (QPE or dissipative), apply the current operator, evolve in real time, then measure the outgoing nucleon flux or channel projectors (Roggero et al. 1911.06368, PRD 101 074038; Weiss, Baroni, Carlson 2404.00202; lattice wave-packet reaction machinery 2603.26881, 2512.16138). It replaces factorization + cascade for final-state interactions. Integral-transform methods (LIT/GIT) cannot access exclusive channels.
- Classical SOTA: CC-LIT inclusive 40Ca (Sobczyk et al. 2103.06786); CC spectral functions (2506.16774); GFMC/AFDMC Euclidean responses (2304.03229, 2405.14916); SF+cascade.
- Why classically hard: exclusive channels need the continuum many-body final states of A=40 with final-state interactions; integral transforms give only inclusive sums.
- Novelty evidence: the queries "neutrino nucleus quantum computing response", "nuclear response function quantum algorithm", "exclusive neutrino nucleus quantum simulation" and "lepton-nucleus scattering quantum computing" found algorithms and small demonstrations, but no advantage study and no semi-exclusive quantum study. -> C/B.
- Main failure risk: chiral-EFT model floor and two-body-current uncertainty (L6); the A=40 continuum box (L ~ 20+ fm) inflates qubit counts; generators tuned to electron-scattering data may already be adequate at DUNE precision (needs a decision-flip test).
- Rough resources: first-quantized A=40 on a 20^3 lattice x spin-isospin -> ~700 logical qubits + ancilla; likely >1e12 Toffolis with 3N forces [ESTIMATE].

### C4. Kitaev-material (alpha-RuCl3 class) Hamiltonian inference from INS + THz/ESR via quantum-computed finite-T, finite-field S(q,omega)  [verdict: plausible; novelty B for 2D inference, C for S(q,omega) in general]
- INPUT: candidate spin-Hamiltonian family (J1, K1, Gamma1, Gamma', J3, ...), field B, temperature T; measured INS S(q,omega) and THz/ESR spectra.
- OUTPUT: a posterior over exchange parameters and a model-discrimination decision (which Hamiltonian family explains the continuum), plus predictions of field-induced phases.
- Practical use: fixing the RuCl3 Hamiltonian settles the spin-liquid interpretation debates (Winter et al. 1702.08466, Nat Commun 8 1152; Maksimov & Chernyshev 2004.10753, PRR 2 033011). Autonomous neutron spectroscopy and NN inverse solvers are now being built (2609.22535, 2304.03949, 2604.23821).
- Quantum mechanism: 2D Trotter/qubitized Hamiltonian simulation of N ~ 50-200 spins; finite T via Gibbs/TPQ; S(q,omega) by Hadamard test or QPE-based spectral estimation; inference in an outer Bayesian loop. It replaces 24-32-site ED, width-limited DMRG cylinders, LSWT/NLSWT, and NN emulators trained on those.
- Classical SOTA: ED/TPQ on small clusters; (i)DMRG dynamics on cylinders (2003.11876); NQS/tensor-network dynamics; sparse Pauli dynamics (Begusic, Gray, Chan 2308.05077, Sci Adv 10 eadk4321); ML emulators.
- Why classically hard: 2D + frustration + finite T + long times for the low-energy continuum; the QMC sign problem; entanglement growth limits DMRG time windows.
- Novelty evidence: a 1D quantum-hardware DSF benchmarked against neutron data exists (Lee et al. 2603.15608, KCuF3, 50 qubits). The queries "RuCl3 quantum simulation dynamical structure factor quantum computer" and "Kitaev material quantum computer spectroscopy" found no quantum computation for Kitaev materials. -> B.
- Main failure risk: L3 (the inference loop multiplies quantum calls by ~1e2-1e3 parameter points unless emulated); L5 (data resolution and phonons may fail to identify the parameters whatever the solver); L6 (spin-only model floor: stacking faults, interlayer coupling, magnon-phonon coupling). The project must show that finite-size classical solvers are the dominant error in the posterior.
- Rough resources: 100-200 qubits, 1e4-1e5 Trotter layers for t ~ 50/J; early-FT regime. Scaling variable: cluster size N.

### C5. Collisional line-shape parameters (pressure broadening, line mixing) for polyatomic-polyatomic pairs in atmospheric remote sensing  [verdict: weak; novelty A]
- INPUT: ab initio PES for (CO2, CH4, O2) + (N2, O2), temperature 200-300 K, line list.
- OUTPUT: broadening and shift coefficients, speed dependence, line-mixing matrices.
- Quantum mechanism: time-dependent wave-packet or S-matrix estimation over many coupled rotational channels via Hamiltonian simulation (a polynomial-degree reduction vs close coupling at O(N_ch^3)).
- Classical SOTA: close coupling / coupled states (2309.08413, 2505.13560); requantized classical MD.
- Novelty evidence: the query "quantum computing pressure broadening line shape" found no quantum paper. -> A.
- Main failure risk: the speedup is polynomial (L3), and PES error likely dominates the required ~0.3% accuracy (L6). Kept only as a category-A reference point.

## 2. Killed ideas (this lens)
- Nuclear level density via quantum DOS/trace estimation: SMMC already reaches the actinides (dimension ~1e32) and agrees with neutron-resonance spacings (DeMartini, Alhassid et al. 2509.26571); stochastic shifted-Krylov methods also exist (Shimizu et al. 1511.06840). Quantum work covers only the toy LMG model (2209.07820, 2405.02255).
- Earth-core iron conductivity (e-e scattering): DFT+DMFT finds the e-e scattering reduction is at most ~20% (Pourovskii et al. 2004.03700), and compositional (O) disorder effects are comparable (Blesio et al. 2304.13962), so the composition model floor dominates the geodynamo decision.
- 12C(alpha,gamma)16O ab initio capture: the S-factor is controlled by near-threshold states that must be positioned to the keV level, and ab initio chiral-EFT errors are far larger (model floor). [reasoning; no specific quantum paper found]
- Low-T deep-tunneling rate constants by exact quantum dynamics: the only quantum rate work found is on classical landscapes (Mazzola 2108.11410); instanton methods (2010.14309) are strong; PES barrier error dominates.
- Nonequilibrium Anderson/Kondo steady-state transport via Lindbladian leads: two queries found no quantum paper, but classical NCA/inchworm/reduced-dynamics methods are strong (2408.09477, 2111.08525), and molecular-junction parameters are model-floor limited.
- Anharmonic vibrational spectra (CH5+, protonated water clusters): quantum block encodings exist (2504.08065, 2307.07478); classical MCTDH/vDMRG are strong; PES floor.
- Standalone finite-T thermodynamics of frustrated magnets via Gibbs samplers: the high-T regime is dequantized (2403.16850, 2305.18514); low-T mixing is unknown; practical value is weak. Folded into C4.
- Dense-hydrogen liquid-liquid transition via QPE energies inside CEIMC: quantum energy calls inside a classical sampler hit the L3 break-even problem, and the fixed-node DMC error is small.
- WDM static EOS via Gibbs sampling: PIMC+xi-extrapolation and DFT-MD are adequate for EOS tables. Only the real-frequency dynamics (C1) is kept.
- Liquid-state NMR / ZULF spectra: L5 (classically computable where informative).

## 3. Query log (2026-09-28)
1. WebSearch "quantum algorithm dynamical structure factor neutron scattering resource estimate fault-tolerant 2025" -> budget exhausted
2. export.arxiv.org API all:"neutrino-nucleus" AND quantum AND computer -> HTTP 429
3. OpenAlex search "neutrino-nucleus scattering quantum computer" -> HTTP 429
4. Crossref "neutrino nucleus scattering quantum computer linear response" -> irrelevant hits
5. arxiv.org/search "neutrino nucleus quantum computing response"
6. arxiv.org/search "nuclear response function quantum algorithm"
7. arxiv.org/search "warm dense matter quantum algorithm"
8. arxiv.org/search "quantum computing dynamic structure factor plasma"
9. arxiv.org/search "Thomson scattering quantum computer"
10. arxiv.org/search "first-quantized quantum simulation finite temperature electron gas" (0 results)
11. arXiv abs 2308.12352
12. arxiv.org/search "Dornheim imaginary-time correlation function temperature diagnostics"
13. arxiv.org/search "fermion sign problem path integral Monte Carlo warm dense hydrogen"
14. arxiv.org/search "inelastic neutron scattering quantum computer dynamical structure factor"
15. arXiv abs 2603.15608
16. arxiv.org/search "RuCl3 quantum simulation dynamical structure factor quantum computer" (0)
17. arxiv.org/search "Kitaev material quantum computer spectroscopy"
18. arxiv.org/search "quantum algorithm nonequilibrium steady state quantum transport mesoscopic leads" (0)
19. arxiv.org/search "quantum computer Anderson impurity nonequilibrium current"
20. arxiv.org/search "Lindblad leads quantum computer transport simulation"
21. arxiv.org/search "vibrational spectra quantum phase estimation anharmonic resource" (0)
22. arxiv.org/search "quantum algorithm vibrational structure fault-tolerant"
23. arxiv.org/search "quantum Gibbs sampler resource estimates application"
24. arxiv.org/search "quantum Gibbs sampling frustrated"
25. arxiv.org/search "quantum computing nuclear reaction cross section scattering phase shift" (0)
26. arxiv.org/search "quantum algorithm nuclear scattering"
27. arXiv abs 2312.05344
28. arxiv.org/search "Sobczyk coupled cluster Lorentz integral transform neutrino" (0); "Sobczyk Bacca coupled cluster response" (0); "ab initio coupled-cluster neutrino response"
29. arXiv abs 1911.06368
30. arxiv.org/search "quantum computing pressure broadening line shape"
31. arxiv.org/search "quantum algorithm thermal rate constant chemical reaction"; "quantum computer reactive scattering tunneling rate"
32. Crossref "quantum computer algorithm thermal rate constant flux correlation chemical reaction"
33. arxiv.org/search "neutron matter quantum computer"
34. arXiv abs 2403.16850; arxiv.org/search "neutrino opacities dense matter dynamic response ab initio" (0); "neutrino opacity neutron matter response"
35. arXiv abs 2407.20986; 1504.07631
36. arxiv.org/search "X-ray Thomson scattering National Ignition Facility beryllium implosion" (0); "X-ray Thomson scattering beryllium NIF" (0); "Thomson scattering warm dense beryllium"
37. arxiv.org/search "nuclear level density quantum computer"; "stochastic estimation nuclear level density shell model"; "shell model Monte Carlo level density heavy nuclei"
38. arxiv.org/search "exclusive neutrino nucleus quantum simulation"; "lepton-nucleus scattering quantum computing"
39. arXiv abs 1702.08466; 2308.05077; 2004.10753; 2105.12767; 2605.22920; 1912.05105
40. arxiv.org/a/baczewski_a_1 (author listing; incomplete, it missed 2308.12352)
41. arxiv.org/search "iron Earth core conductivity electron-electron scattering"
42. arxiv.org/search "Laurell Okamoto alpha-RuCl3 ..." (0); "RuCl3 Hamiltonian parameter sets exact diagonalization" (0); "RuCl3 minimal model"

## 4. Citation list (verification status)
VERIFIED via arXiv abs page: 2308.12352 (Rubin et al., PNAS 121 2024), 2603.15608 (Lee et al. 2026), 2312.05344 (Watson et al.), 1911.06368 (Roggero et al., PRD 101 074038), 2403.16850 (Bakshi et al.), 2407.20986 (Sobczyk et al.), 1504.07631 (Melson et al., ApJL 808 L42), 1702.08466 (Winter et al., Nat Commun 8 1152), 2308.05077 (Begusic et al., Sci Adv 10 eadk4321), 2004.10753 (Maksimov & Chernyshev, PRR 2 033011), 2105.12767 (Su et al., PRX Quantum 2 040332), 2605.22920 (Nelson & Baczewski 2026), 1912.05105 (Lu et al., PRL 125 192502).
VERIFIED via arXiv search listing (title/authors/date from the listing; abstract page not opened): 1804.01505, 2004.04889, 2110.02108, 2404.00202, 2404.19554, 2210.08757, 2304.03229, 2103.06786, 2506.16774, 2405.14916, 2007.15570, 2403.01979, 2407.01044, 2405.10627, 2207.14716, 2211.00579, 2604.25735, 2501.01869, 2407.08875, 2510.01875, 2402.19113, 2504.13611, 2410.23599, 1512.05795, 2604.27237, 2609.22535, 2304.03949, 2604.23821, 2003.11876, 2311.09207, 2310.07774, 2305.18514, 2306.16580, 2212.04436, 2407.21207, 1612.02764, 2603.26881, 2512.16138, 2407.04155, 2609.25164, 2006.01369, 2504.08065, 2307.07478, 2209.07820, 2405.02255, 2509.26571, 1511.06840, 2108.11410, 2010.14309, 2408.09477, 2111.08525, 2004.03700, 2304.13962, 2309.08413, 2505.13560.
UNVERIFIED / reasoning only: the keV-level precision requirement for 12C(alpha,gamma)16O; all Toffoli and qubit numbers marked [ESTIMATE].
