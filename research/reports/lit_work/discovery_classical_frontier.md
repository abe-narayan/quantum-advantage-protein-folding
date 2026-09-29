# Discovery lens: classical frontier map (classical adversary) (2026-09-28)

Status: COMPLETE (see end). Initially checkpoint 0. WebSearch budget exhausted; using arXiv export API (local urllib, rate-limited 429 after ~11 calls), OpenAlex API, arXiv abs pages.

## Query log
- arXiv API: abs:"beyond-classical" AND abs:annealer AND abs:dynamics
- arXiv API: abs:"belief propagation" AND abs:"tensor network" AND abs:dynamics AND abs:quench
- arXiv API: abs:"neural quantum state" AND abs:dynamics AND abs:"three dimensions" (0 hits)
- arXiv API: abs:Hubbard AND stripe AND AFQMC AND DMRG AND superconductivity (0 hits)
- arXiv API: abs:phaseless AND AFQMC AND bias AND "transition metal" (0 hits)
- arXiv API: abs:"sparse Pauli dynamics" OR abs:"Pauli propagation"
- arXiv API: HEOM low temperature tensor network bath (0 hits)
- arXiv API: ML-MCTDH matrix product state comparison (0 hits)
- arXiv API: "G1-G2" nonequilibrium instability
- arXiv API: inchworm nonequilibrium "steady state"
- arXiv API second batch (11 queries) mostly HTTP 429.

## Early hits (from arXiv API listing, to be verified on abs pages)
- 2504.06283 Comment (King et al. side) on Tindall et al. 2503.05693: TN did not attempt most complex geometry, largest 3D, longest times.
- 2511.19340 Comparative study of large-scale classical numerics for 2D TFIM dynamics (MPS, TTN, BP-TN, t-VMC ...).
- 2504.07344 TN influence-functional BP for 2D dynamics.
- 2409.03097 sparse Pauli dynamics 2D/3D (Begusic, Chan).
- 2306.16372, 2308.05077 classical simulation of IBM utility experiment.
- 2606.10773 NEGF G1-G2 for large correlated systems (instabilities).
- 2407.00771 inchworm multi-orbital steady state.

## Checkpoint 1 (verified items)
Verified via arXiv export API id_list (title/authors/abstract) or OpenAlex DOI record:
- arXiv:2403.00910 King et al. "Beyond-classical computation in quantum simulation" (Science 2025, doi:10.1126/science.ado6285) [VERIFIED]
- arXiv:2503.05693 Tindall, Mello, Fishman, Stoudenmire et al. BP tensor networks 2D/3D disordered dynamics (Science 2026, doi:10.1126/science.adx2728 per OpenAlex) [VERIFIED]
- arXiv:2504.06283 King et al. Comment: Tindall did not attempt most complex geometry, largest 3D, longest times, low-precision ensembles [VERIFIED]
- arXiv:2503.08247 Mauron, Carleo t-VMC Jastrow-Feenberg simulates D-Wave annealing [VERIFIED]
- arXiv:2511.19340 Vovrosh et al. comparative 2D TFIM dynamics MPS/TTN/BP-TN/NQS [VERIFIED]
- arXiv:2409.03097 Begusic, Chan sparse Pauli dynamics 2D/3D [VERIFIED]
- arXiv:2306.16372, 2308.05077 classical simulation of IBM Eagle utility experiment [listing]
- arXiv:2506.10191 Google OTOC(2) "Constructive interference at the edge of quantum ergodic dynamics" [VERIFIED]
- arXiv:2511.02125 Granet et al. Quantinuum Helios pairing correlations Fermi-Hubbard [VERIFIED]
- arXiv:2606.10773 Schroedter, Bonitz, Joost NEGF large correlated systems (G1-G2 instabilities, new quantum-fluctuation formulation) [VERIFIED]
- arXiv:2407.00771 Erpenbeck et al. steady-state multi-orbital inchworm [VERIFIED]
- arXiv:2601.04621 Zhai et al. FeMoco classical to chemical accuracy [VERIFIED]
- arXiv:2603.28648 Legeza et al. Fe4S4 CAS(54,36) DMRG vs IBM/RIKEN Quantum Advantage Tracker [VERIFIED]
- arXiv:2009.08927 Al-Hamdani et al. CCSD(T) vs DMC disagree up to 8 kcal/mol for polarizable supramolecules (Nat Commun 2021, doi:10.1038/s41467-021-24119-3) [VERIFIED]
- doi:10.1038/s41467-025-64104-8 Schafer, Irmler, Gallo, Gruneis Nat Commun 2025: pin down source, modify CC [VERIFIED]
- doi:10.1063/5.0254021 Shi, Della Pia, Al-Hamdani, Michaelides et al. JCP 2025: systematic DMC vs CCSD(T) on S66 [VERIFIED]
- doi:10.1063/5.0246763 Lambie, Kats, Usvyat, Alavi JCP 2025: PPP model; CCSD(T) no sign of overestimation [VERIFIED]
- doi:10.1063/5.0242359 Lao JCP 2024: canonical CCSD(T)/CBS L14/vL11; FN-DMC underbinds pi-pi by >1 kcal/mol [VERIFIED]
- doi:10.1039/d4sc05471g Radon et al. Chem Sci 2024 SSE17: CCSD(T) MAE 1.5 kcal/mol vs experiment-derived [VERIFIED]
- doi:10.1103/physrevlett.131.186401 Masios et al. PRL 2023 (T) IR catastrophe for metals [VERIFIED OpenAlex]
- doi:10.1039/d1sc05691c Malone et al. Chem Sci 2022 SAPT(VQE) [VERIFIED]; doi:10.1039/d2sc05896k Loipersberger et al. Chem Sci 2023 SAPT2 on NISQ [VERIFIED]
- arXiv:2105.12767 Su, Berry, Wiebe, Rubin, Babbush first-quantization FT chemistry [VERIFIED]
- arXiv:2411.12049 HEOM on NISQ computers [listing]; arXiv:2606.16017 cathode Holstein polaron quantum algorithm [listing]
- arXiv:2603.11891 INVEST gaps via O2BMP2 (cheap classical reaching ADC(3)/EOM-CCSD) [VERIFIED]

## Additional verified items (checkpoint 2)
- doi:10.1021/acs.jctc.6c00882 Lambie, Lopez Rios, Kats, Alavi JCTC 2026 "Nodal Error behind Discrepancies between CC and DMC": discrepancy dominated by Slater-Jastrow fixed-node error; CC should be regarded as benchmark (acetic acid dimer, water-peptide) [VERIFIED OpenAlex]
- doi:10.1063/5.0348824 Nakano, Shi, Alfe, Zen JCP 2026: AGPn nodes; MAD CCSD(T) vs FN-DMC 0.2-0.4 kcal/mol on 12 NCI systems [VERIFIED]
- doi:10.1021/acs.jpca.6c01097 Lao JPCA 2026 vL27 up to 205 atoms converged local CCSD(T) [VERIFIED]
- doi:10.1021/acs.jctc.5c01910 Jiang, Matthews et al. JCTC 2026 DLPNO-CCSDTQ [VERIFIED]
- doi:10.1021/acs.jpclett.5c02576 Fanta, Jurecka, Dubecky JPCL 2025: single-determinant DMC underbinds pi-pi (benzene dimer) due to weak nondynamic correlation in nodes [VERIFIED]
- doi:10.1021/acs.jctc.4c00751 Dorfner, Brey, Burghardt, Ortmann JCTC 2024: MPS vs ML-MCTDH agree for 2 states x 100 modes, deviate for 26 states x 113 modes (P3HT:PCBM exciton dissociation), traced to entanglement treatment [VERIFIED]
- arXiv:2411.13669 Motlagh et al. vibronic product-formula algorithm, singlet fission case study [VERIFIED]
- arXiv:2312.14914 Ostmeyer, Nematiaram, Troisi, Buividovich HMC mobility in 2D OSC tight-binding: agrees with experiment, justifies transient localisation [VERIFIED]
- doi:10.1063/5.0299359 JCP 2025 numerically exact dissipative e-ph transport rationalizing TL [OpenAlex listing]; doi:10.1103/3mgx-x6t5 PRB 2026 quantum-classical multi-mode OSC transport [OpenAlex listing]
- arXiv:2202.05740 Monacelli, Casula, Nakano, Sorella et al. hydrogen phase diagram DMC+SSCHA (atomic metal at 577+-10 GPa) [VERIFIED]
- arXiv:2308.10095 Dollberg, Schechter LiHoF4 non-standard quantum Ising (off-diagonal dipolar terms; model discrepancies) [VERIFIED]
- arXiv:2504.07344 Park, Gray, Chan TN influence-functional BP 2D dynamics [VERIFIED]
- arXiv:2411.12049 Dan, Geva, Batista HEOM on NISQ [VERIFIED]
- arXiv:2403.20247 Ast et al. theory of ESR-STM: Green's functions + quantum master equation reproduce TiH/MgO quantitatively [VERIFIED]
- arXiv:2303.09944 Reina-Galvez, Wolf, Lorente driven impurity ESR-STM, lowest-order ME [VERIFIED]
- arXiv:2210.09623 Werner, Lotze, Arrigoni AMEA+CI nonequilibrium steady-state impurity solver [VERIFIED]
- doi:10.1103/physrevb.110.195148 quasi-Lindblad pseudomode theory 2024 [OpenAlex listing]
- doi:10.1063/5.0214051 JCP 2024 managing temperature in HEOM / T-TEDOPA for structured environments [OpenAlex listing]

## Query log (complete)
arXiv export API (local urllib; many HTTP 429):
1. abs:"beyond-classical" AND abs:annealer AND abs:dynamics
2. abs:"belief propagation" AND abs:"tensor network" AND abs:dynamics AND abs:quench
3. abs:"neural quantum state" AND abs:dynamics AND abs:"three dimensions" (0)
4. abs:Hubbard AND stripe AND AFQMC AND DMRG AND superconductivity (0)
5. abs:phaseless AND AFQMC AND bias AND "transition metal" (0)
6. abs:"sparse Pauli dynamics" OR abs:"Pauli propagation"
7. HEOM "low temperature" "tensor network" bath (0)
8. "ML-MCTDH" "matrix product state" comparison (0)
9. "G1-G2" nonequilibrium instability
10. inchworm nonequilibrium "steady state"
11. "classical simulation" "quantum utility" experiment (0); "iron porphyrin" spin DMRG AFQMC (429)
12-22. second batch (iron porphyrin, AFQMC trial error, Hubbard discrepancies, HEOM, ML-MCTDH, NQS 2D quench, 3D advantage, finite-T TN, molecular junction NESS, optical conductivity strange metal, CDMFT sign problem) - mostly 429
23. ti:"CCSD(cT)" (0); DMC AND CCSD(T) AND discrepancy AND large; "spin-state" AND AFQMC (0); quantum computer nonequilibrium impurity steady state; quantum algorithm HEOM
24. "quantum advantage tracker"; quantum noncovalent "phase estimation" (0); CC metal surface CO DMC (0); "inverted singlet-triplet" quantum computer; TM spin-state CC DMRG discrepancy (0)
25. ti:"Understanding discrepancies..." (0); hydrogen phase III QMC metallization; Pt(111) CO coupled cluster; quantum computer Anderson impurity nonequilibrium (0); Holstein-Peierls mobility numerically exact (0); quantum computing DMC CC noncovalent
26. "ESR-STM" theory Kondo (0); ESR STM nonequilibrium strong coupling (0); "ESR-STM" theory; "auxiliary master equation" nonequilibrium Kondo; multi-orbital Anderson tensor steady state (0)
27. id_list verifications (3 calls)
OpenAlex:
- iron porphyrin spin state DMRG AFQMC CC (429); phaseless AFQMC TM (429); doped Hubbard stripe DMRG AFQMC; HEOM low T TN (429); ML-MCTDH MPS discrepancy; NQS real-time 2D; beyond-classical annealer; NESS multi-orbital (429); finite-T S(q,w) 2D TN; real-frequency CDMFT sign problem
- puzzle for reference QM methods; CCSD(T) DMC buckyball; SSE17; phaseless AFQMC spin gap (429); HEOM Matsubara tree TN; digital quantum magnetism frontier; NESS impurity STM (429); Tindall title
- IR catastrophe CC; SAPT on NISQ; hydrogen phase diagram (429); CO Pt(111) (429); quantum impurity transport (429)
- cited-by W3087523511 (Al-Hamdani), W4415148299 (Schafer 2025), W4405451244 (Lao 2024)
- quantum computer NESS impurity Lindblad leads; quantum algorithm molecular junction transport
- ESR-STM Kondo (429); Holstein-Peierls 2D mobility; LiHoF4 annealing; MPS vs ML-MCTDH (429); driven impurity (429)
- DOI lookups: 10.1038/s41467-025-64104-8, 10.1063/5.0254021, 10.1063/5.0246763, 10.1063/5.0242359, 10.1039/d4sc05471g, 10.26434/chemrxiv-2024-nwbqd, 10.1021/acs.jctc.6c00882, 10.1063/5.0348824, 10.1021/acs.jpca.6c01097, 10.1021/acs.jctc.5c01910, 10.1021/acs.jpclett.5c02576, 10.1021/acs.jctc.4c00751
WebSearch: budget exhausted (0 results).


## CLASSICAL WALL MAP (2023 to 2026-09-28)
Legend: MULTI = independent method families disagree or fail (published); SINGLE = limitation shown within one family only; MOVING = wall receded within 2024-2026; DURABLE = no family converges in the regime as of the searched sources.

| # | System class | Scaling variable | Evidence | Status |
|---|---|---|---|---|
| W1 | Unitary quench/anneal dynamics of disordered spin models in 2D/3D and high-connectivity lattices, intermediate/long times | lattice dimension, N, anneal time, precision ensemble | King et al. 2403.00910 (MPS/PEPS stretched-exponential cost); Tindall et al. 2503.05693 (BP-TN reaches 2D/3D; Science 2026); Mauron-Carleo 2503.08247 (t-VMC); King et al. comment 2504.06283 (largest 3D, longest times, low-precision ensembles, most complex geometry not reproduced); Vovrosh et al. 2511.19340 (MPS/TTN/BP-TN/NQS comparative; anneal vs quench regimes) | MULTI, contested; durable only at 3D x long t x fast-correlating ensembles; practical output weak |
| W2 | Heisenberg-picture observable dynamics (Pauli propagation) | time, temperature, dimension, non-Clifford density | Begusic-Chan 2409.03097 (competitive in 2D, 3D where TN struggles); 2306.16372 and 2308.05077 (IBM utility circuits classically simulated); 2510.22311 (truncation error set by operator stabilizer Renyi entropy); 2601.14400 (imaginary-time PP best at high T) | SINGLE-family limits: low T x long t x >=2D |
| W3 | OTOC(2)/echo observables beyond reversal horizon | circuit depth, qubits | Google 2506.10191 | claimed hard; informational value low (protein lesson 5) |
| W4 | Static strongly correlated molecular ground states (FeMoco, Fe4S4, mononuclear TM spin states) | active-space size | FeMoco to chemical accuracy 2601.04621; Fe4S4 CAS(54,36) 2603.28648 (IBM/RIKEN tracker item); SSE17 CCSD(T) MAE 1.5 kcal/mol (doi:10.1039/d4sc05471g) | MOVING fast; not a wall |
| W5 | Noncovalent binding of large polarizable complexes (CC vs DMC) | pi-electron count / HOMO-LUMO gap closure | Al-Hamdani 2021 (up to 8 kcal/mol); Schafer 2025 ((T) overcorrelation, CCSD(cT)); Lao 2024/2026 (canonical/converged local CCSD(T) to 205 atoms); Lambie 2025 PPP (no (T) overbinding); Fanta 2025, Lambie 2026, Nakano 2026 (fixed-node error dominant; MAD 0.2-0.4 kcal/mol with better nodes); DLPNO-CCSDTQ 2026 | MULTI in 2021, MOVING to classical consensus by 2026; residual (T) vs (cT) question only for largest gap-closing systems |
| W6 | Correlated wavefunction energies for metals / metal surfaces | k-mesh, slab size | Masios PRL 2023 (T) IR catastrophe; CCSD(cT) remedy; JACS 2023 consensus for insulating surfaces | SINGLE-family fix exists; model floor (slab, finite size) comparable |
| W7 | Vibronic dynamics with many electronic states x many modes (aggregates, donor/acceptor interfaces) | N_el states, N_vib modes | Dorfner et al. JCTC 2024: MPS vs ML-MCTDH agree at 2x100, deviate at 26x113 (P3HT:PCBM) | MULTI (two gold-standard families disagree); durable in searched sources |
| W8 | Charge mobility in organic semiconductors (Holstein-Peierls, 2D) | lattice size, phonon modes | HMC 2312.14914 agrees with experiment; numerically exact dissipative model JCP 2025; quantum-classical multi-mode PRB 2026 | CLOSED classically |
| W9 | Nonequilibrium multi-orbital impurity steady states (bias, drive) | orbitals, bias, time, drive | Erpenbeck 2407.00771 (dynamical + multi-orbital sign problems, inchworm alleviates); AMEA+CI/MPS 2210.09623; ESR-STM regime reproduced by perturbative master equations (2403.20247, 2303.09944) | SINGLE-family limits; practical weak-coupling regime classically solved |
| W10 | Real-time NEGF for large inhomogeneous correlated systems | basis size, time steps | G1-G2 instabilities limited N_b ~ 1e2; 2606.10773 quantum-fluctuation formulation extends | MOVING |
| W11 | Open-system dynamics with structured baths at low T | 1/T, Matsubara terms, bath modes | JCP 2024 doi:10.1063/5.0214051 (HEOM low-T vs T-TEDOPA high-T limits) | SINGLE-family; complementary families cover |
| W12 | Doped 2D Hubbard | doping, T, cluster size | ground state DMRG+AFQMC consistent (Science 2024 doi:10.1126/science.adh7691); pseudogap by diagMC (Science 2024 doi:10.1126/science.ade9194); pairing dynamics on Helios 2511.02125 | ground state MOVING; low-T dynamics owned by materials lens |

Lens conclusion: static ground-state walls recede within 1-3 years once a well-defined target is posted (FeMoco, Fe4S4, the CC/DMC NCI dispute, SSE17). Walls that remain with published multi-family disagreement are real-time dynamics: W1 (>=2D unitary dynamics at long times) and W7 (many-state vibronic dynamics). Of these only W7 has a direct practical output with an existing experimental observable (transient absorption, charge generation yield). Nothing in this map passes all protein-lesson filters without a named main risk.

## CANDIDATES

### C1. Charge generation at donor/acceptor interfaces in the MPS vs ML-MCTDH divergence regime (verdict: PLAUSIBLE)
- Input: LVC or quadratic vibronic-coupling Hamiltonian for a D/A cluster (P3HT:PCBM, polymer:non-fullerene acceptor): N_el = 20-100 diabatic states (local excitons, CT, charge-separated), N_vib = 100-300 modes; parameters from TDDFT/ADC(2) diabatization; initial Franck-Condon exciton.
- Output: diabatic populations P_XT(t), P_CT(t), P_CS(t) to about 1 ps; charge-separation yield and time constants (compare transient absorption).
- Scaling variable: number of acceptor molecules in the cluster (N_el at fixed modes per molecule); secondary: modes per state.
- Strongest classical: ML-MCTDH, MPS with 1TDVP/2TDVP and adaptive bond dimension, tree tensor network states, vMCG, HEOM with effective modes; surface hopping / Ehrenfest as approximate baselines.
- Wall evidence: Dorfner, Brey, Burghardt, Ortmann JCTC 2024 (doi:10.1021/acs.jctc.4c00751).
- Quantum mechanism: real-space product-formula simulation of the vibronic Hamiltonian (Motlagh et al. arXiv:2411.13669): modes on position-grid registers, electronic states in a binary register; populations by projective measurement (shots ~ 1/eps^2, amplitude estimation ~ 1/eps). Replaces entanglement-limited variational propagation. Resource: poly(N_el, N_vib, t) vs classical cost set by electron-vibration entanglement.
- Novelty: C. In arXiv/OpenAlex sources searched through 2026-09-28: algorithm and cost model (2411.13669, singlet fission) and classical disagreement (Dorfner 2024) found; no quantum-vs-classical study at the disagreement point and no quantum study of D/A charge generation found. Overlaps the prior-week singlet-fission/OPV lane.
- Main risk: divergence is a convergence artifact that larger bond dimension or better tree topology resolves; LVC model floor exceeds solver disagreement; few-state populations are low-information observables.
- Pre-registration hook: run the classical adversary ladder first (MPS bond dimension to saturation, TTNS topologies, ML-MCTDH SPF convergence) and confirm the 26x113 disagreement survives before any quantum resource work.

### C2. Exact reference for gap-closing pi-stacked noncovalent complexes (residual (T) vs (cT) regime) (verdict: WEAK)
- Input: geometries of large pi complexes (coronene/circumcoronene dimers, C60 in buckycatcher, acene dimers) + Gaussian basis; tier-0 scalable proxy: PPP pi-model of 2D nanographene dimers, N_pi = 50-300 sites.
- Output: interaction energy to +-0.2 kcal/mol.
- Scaling variable: pi-electron count / HOMO-LUMO gap.
- Strongest classical: canonical and local CCSD(T)/CBS, CCSD(cT), CCSDT(Q), DLPNO-CCSDTQ (2026), FN-DMC with AGPn/backflow/multi-determinant nodes, AFQMC, DMRG for PPP.
- Wall evidence: W5 (MULTI 2021, MOVING by 2026).
- Quantum mechanism: qubitized QPE with double-factorized/THC block encodings on PNO/FNO active spaces; tier-0 QPE on PPP Hamiltonian vs DMRG/CCSDTQ.
- Novelty: B. Quantum NCI methods exist (SAPT(VQE) Malone Chem Sci 2022; SAPT2 on NISQ Loipersberger Chem Sci 2023); no quantum study of the large-pi CC/DMC discrepancy regime found.
- Main risk: classical consensus forming; decision outputs dominated by solvation/entropy model floor; ab initio resources very large.

### C3. Driven, strongly coupled multi-orbital impurity transport (verdict: WEAK)
- Input: multi-orbital Anderson impurity (3-5 orbitals, U, J_H, SOC), two leads, bias V, field B, drive f.
- Output: I(V,B,f), dI/dV, ESR signal in the strong-coupling (Kondo) regime.
- Scaling variable: correlated orbitals x lead modes; bias; drive amplitude.
- Strongest classical: perturbative QME + Green's functions (2403.20247, 2303.09944), AMEA with MPS/CI (2210.09623), steady-state multi-orbital inchworm (2407.00771), TN influence functional, fermionic HEOM, NRG (equilibrium).
- Wall evidence: SINGLE-family sign-problem statements only.
- Quantum mechanism: Lindbladian (AMEA auxiliary open system) or pseudomode dilation on qubits; or closed-system Trotter with O(10^2) discretized lead modes; current as expectation value.
- Novelty: B (quantum HEOM exists 2411.12049; no driven multi-orbital steady-state transport study found; weakly scoped).
- Main risk: experimentally used weak-coupling ESR-STM regime is classically quantitative; DFT-derived impurity parameters dominate error.

### C4. 3D dipolar quantum Ising dynamics of LiHo_xY_{1-x}F_4 (verdict: WEAK, practicality low)
- Input: electronuclear effective Hamiltonian (Ho doublet + hyperfine I=7/2 + long-range dipolar + exchange), dilution x, transverse field, anneal/quench protocol.
- Output: magnetization relaxation, ac susceptibility chi(omega), residual defect density after field anneals.
- Scaling variable: N in 3D, anneal time, x.
- Strongest classical: BP-TN in 3D (2503.05693), t-VMC (2503.08247), sparse Pauli dynamics 3D (2409.03097), mean-field+RPA, cluster expansions.
- Quantum mechanism: digital Trotter/qubitization of long-range dipolar electronuclear Hamiltonian (local dim 16 -> 4 qubits/ion) or annealer-native emulation.
- Novelty: A/B for this material on digital QC; generic spin-glass anneal dynamics is category E.
- Main risk: model floor (2308.10095 shows effective-model discrepancies); low practical value; O(N^2) long-range gate cost.

## KILLED IDEAS (this lens)
- Mononuclear TM spin-state energetics: SSE17 CCSD(T) MAE 1.5 kcal/mol vs experiment-derived references with comparable back-correction uncertainty.
- FeMoco / Fe4S4 static ground states: classical to chemical accuracy (2601.04621; 2603.28648).
- Organic-semiconductor mobility (Holstein-Peierls 2D): wall closed (2312.14914; JCP 2025; PRB 2026).
- D-Wave-type spin-glass anneal dynamics as a target: category E, no practical output.
- INVEST singlet-triplet gaps: cheap classical O2BMP2 reaches ADC(3)/EOM-CCSD (2603.11891).
- Large inhomogeneous NEGF dynamics: wall moved (2606.10773); stopping power already claimed (2308.12352).
- Low-T structured-bath HEOM: single-family limitation, covered by T-TEDOPA/pseudomodes/TEMPO.
- Dense solid hydrogen metallization: single-family evidence only (2202.05740); nuclear sampling x QPE cost = protein break-even trap.
- CO on transition-metal surfaces: classical (cT) fix (PRL 2023); slab/finite-size model floor; not fully assessed (rate limits).
- OTOC beyond reversal horizon (2506.10191): protein lesson 5.
- Doped 2D Hubbard ground state: DMRG+AFQMC consistent (Science 2024); dynamics owned by materials lens.

Status: COMPLETE (2026-09-28).
