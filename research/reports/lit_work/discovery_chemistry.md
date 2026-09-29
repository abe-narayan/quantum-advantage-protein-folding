# Discovery lens: chemistry subproblems inside studied fields (2026-09-28)

Status: COMPLETE (final save). Lens: specific observables or regimes inside studied chemistry fields (ISC rates, quantum yields, KIE, electrochemical barriers, core-level spectra, exchange couplings, NMR/EPR of open-shell metals, reaction-network ranking, excited-state absorption) that have not been tested for quantum advantage.

## Tooling and scope of the search (read before trusting any "not found")
- WebSearch was unavailable because the session budget was used up (200/200). OpenAlex returned HTTP 429.
- All searches ran against the arXiv API (export.arxiv.org, boolean queries on the abstract field, relevance sort, top 20) and Crossref (title/abstract relevance, 2019+). DOIs were checked by Crossref `/works/<doi>` lookup, and arXiv ids by the arXiv API `id_list`.
- A "not found" below therefore means: not found in the top 20 arXiv abstract-field boolean hits, nor in the top 12 Crossref hits, for the queries listed. It does not cover journal-only papers without an arXiv preprint, and it does not cover wording variants I did not query.

## Query log
arXiv API (abs: field boolean) unless marked CR (Crossref):
1. CR "quantum computer intersystem crossing spin-orbit" (2020+): only classical ISC papers.
2. abs:"intersystem crossing" AND (quantum computer|computing|algorithm): 2508.13281 (ODMR defects), 2601.18898 (Zak, Pauli-Breit FT), 2512.15889 (PDT BODIPY ISC).
3. abs:"spin-orbit" AND quantum computer/computing AND molecul*: 1111.3490 (relativistic QC), 2303.09010 (AFQMC+SOC, classical). No study of SOC-driven rates vs classical.
4. abs:"inverted singlet" AND (quantum computer|computing|VQE): none. abs:"inverted singlet-triplet": classical only (2405.03598, 2404.15768, 2603.11891, 2111.08987, 2511.08235).
5. abs:"exchange coupling" AND quantum computer/computing AND (cluster|iron|manganese): nothing on molecules.
6. abs:hyperfine AND quantum computer/computing AND (EPR|radical|g-tensor): 2503.09214 (first HFCs on hardware), 2208.10107.
7. abs:"spin crossover" AND quantum computer/computing: only 2206.03978 (spinmerism).
8. abs:"zero-field splitting" AND quantum computer/computing: spin-defect papers (2601.22091, 2607.14083) and 2303.09010.
9. abs:"kinetic isotope" AND quantum computer/computing/algorithm: none.
10. abs:"spin-vibronic" AND quantum (computer|algorithm|qubit|simulat*): none (2 attempts).
11. abs:"quantum yield" AND "conical intersection" AND quantum computer/simulator: 2202.02364 (trapped-ion engineered CI).
12. (iron-sulfur|Mn4CaO5|oxygen-evolving complex) AND (quantum computer|computing|resource estimate): 2603.22778, 2506.13386, 2404.08565, 2601.06935 (HI-VQE Fe-S), 2601.10813, 2501.07231, 2502.15882, 2609.01264.
13. (X-ray absorption|core-level|RIXS|X-ray emission) AND quantum algorithm/computer: 2405.11015, 2506.15784, 2505.08612, 2602.20270. All are single-site battery XAS/RIXS or logical-QPE demonstrations.
14. (spin-state|porphyrin) AND quantum computer/QPE: nothing on spin-state energetics.
15. (lanthanide|actinide|crystal field) AND quantum computer/QPE AND molecul*: 2601.10813 (U2) only.
16. (electrochemical|electrocatalysis|electrode potential) AND quantum computer/FT: 2609.28369, 2606.16017 (battery). No study of potential-dependent barriers.
17. (reaction network|mechanism) AND quantum computer AND catal*: nothing relevant.
18. (linear response|excited-state absorption|two-photon) AND quantum computer AND molecul*: qLR family (2511.09730, 2404.16586, 2411.03852, 1911.00293, 2301.06260, 2201.02426).
19. (lanthanide|europium|4f) AND (luminescence|Judd-Ofelt|transition intensities) AND (ab initio|quantum chemical|quantum computer): solid-state only, no quantum computing.
20. (actinide|uranium|relativistic) AND (quantum computer|VQE|phase estimation) AND molecul*: 2406.04992, 2211.06907 (relativistic VQE PDMs), 2212.02058 (Bayesian phase difference, fine structure), 2601.10813, 1111.3490.
21. (L-edge|2p3d|L2,3) AND (multinuclear|dimer|cluster|exchange-coupled) AND (RASPT2|DMRG|RAS|multiplet): 2305.08184 (CV-RAS-DMRG L-edge/RIXS), 1803.11248 (DMRG RIXS chains).
22. (spin ladder|exchange coupling|low-lying spin states) AND DMRG AND (iron|manganese|cluster): 2508.13002 (TPSCI vs DMRG J), 2604.06841 (spin-adapted NN backflow).
23. (mixed-valence|double exchange|valence delocalization) AND (DMRG|quantum computer|multireference) AND (iron|Fe-S|manganese): 1908.05802 (DMRG X-ray Raman [2Fe-2S]), 2105.01754 (ASCI/DMRG cubanes).
24. CR "ab initio 4f-4f transition intensities lanthanide complex multiconfigurational dynamic coupling"; CR "quantum computing lanthanide luminescence"; CR "ab initio ligand-to-lanthanide energy transfer rate sensitization europium": no quantum-computing work, sparse ab initio.
25. CR "quantum computing iron-sulfur cluster spin states": 10.26434/chemrxiv.15006382 (SQD spin audit).
26. CR "quantum algorithm exchange coupling constant transition metal complex": none relevant.
27. abs:(exchange coupling|Heisenberg exchange|magnetic coupling) AND (VQE|variational quantum|quantum hardware|processor) AND (binuclear|dinuclear|copper|complex): none on molecular J.
28. (spin crossover|light-induced|metal-centered) AND iron AND (quantum dynamics|MCTDH) AND (MLCT|spin-vibronic|quintet): none on arXiv. CR found classical Fe(II) spin-vibronic papers (10.1002/cphc.202500768, 10.1039/d5cp01208b, 10.1021/acs.inorgchem.1c01838, chemRxiv 10.26434/chemrxiv.15006375).
29. (paramagnetic NMR|pNMR|hyperfine shift|contact shift) AND (quantum computer|DMRG|multireference): none relevant.
30. (single-molecule magnet|magnetic anisotropy) AND (quantum computer|algorithm|phase estimation): nothing on computing SMM anisotropy with QC.
31. (sample-based quantum diagonalization|SQD|quantum-selected) AND (iron|Fe-S|transition metal|spin): 2607.16389, 2603.09346, 2501.07231, and others.
32. CR spin-state energetics SSE17; CR Fe(II) MLCT/MC spin-vibronic MCTDH; CR actinide crystal field / INS.
33. CR "ultrahard magnetism mixed-valence dilanthanide"; CR "radical-bridged dilanthanide exchange ab initio"; CR "relativistic DMRG spin-orbit lanthanide actinide"; CR "U(IV)/U(V) dimer exchange spin-orbit".
34. (L-edge|RIXS|XAS) AND (iron-sulfur|Fe-S|[2Fe-2S]|Mn4CaO5|dinuclear|metal cluster) AND (DMRG|correction vector|quantum computer|ab initio): only 2305.08184.
35. (spin-orbit AND DMRG) AND (dysprosium|lanthanide|actinide|f-element): 2207.02435 (Zhai and Chan, one-step SO-DMRG), 1710.08301 (relativistic DMRG).
36. (vibronic|nonadiabatic) AND (quantum computer|algorithm) AND (transition metal|iron|spin crossover|intersystem): only 2512.15889.

## Verified citations (V = checked in this session through the arXiv API or Crossref)
- [V] arXiv:2601.04621 Zhai, Li, Zhang, Li, Lee et al. 2026. The ground state of a FeMoco model is computed classically to chemical accuracy with high-order CC plus DMRG plus extrapolation. The authors characterise the problem as "ranking many competing, but largely simple, states".
- [V] arXiv:2208.02199 / doi:10.1038/s41467-023-37587-6. Lee et al., Nat Commun 2023. They find no evidence of a generic exponential advantage for ground-state energy estimation.
- [V] arXiv:2601.10813 Poyyapakkam Sundar, Abraham, Peng, Asthana 2026. Benchmark hierarchy: N2, FeS, [2Fe-2S], U2 (ADAPT-GCIM).
- [V] arXiv:2601.06935 Yoo et al. 2026. HI-VQE on N2 and an Fe-S cluster, compared against HCI.
- [V] chemRxiv doi:10.26434/chemrxiv.15006382 Vitale 2026. Spin audit of SQD Fe-S benchmarks: no audited run returned the named singlet at a competitive energy, and the released [2Fe-2S] hardware samples show no energy advantage over a uniform-random control.
- [V] arXiv:2501.07231. "Critical Limitations in Quantum-Selected Configuration Interaction Methods" (title verified).
- [V] doi:10.1038/nchem.2041 Sharma, Sivalingam, Neese, Chan, Nat Chem 2014. DMRG low-energy spectrum of Fe-S clusters.
- [V] doi:10.1038/nchem.1677 Kurashige, Chan, Yanai, Nat Chem 2013. DMRG on Mn4CaO5.
- [V] doi:10.1038/s41557-019-0337-3 Li, Guo, Sun, Chan, Nat Chem 2019. DMRG on the nitrogenase P-cluster.
- [V] arXiv:2105.01754 Mejuto-Zaera et al. 2021. ASCI and DMRG CASSCF on cubanes. Spin-state gaps are below 1 mHa, and the overall spin gap is strongly geometry dependent.
- [V] arXiv:2508.13002 Bachhar and Mayhall 2025. TPSCI vs DMRG J values for dinuclear Cr/Fe/Mn and a Ni4 cubane, active spaces (22e,29o) to (42e,49o). J agrees within 10-30 cm^-1.
- [V] arXiv:2604.06841. Spin-adapted neural-network backflow for strongly correlated electrons (title verified).
- [V] arXiv:2305.08184 Lee, Zhai, Chan 2023. Correction-vector RAS-DMRG for L-edge XAS and 2p3d RIXS of [FeCl4] and [Fe(SCH3)4], stated as a step toward larger metal clusters.
- [V] arXiv:1908.05802 Cho, Rouxel, Mukamel, Chan, Li 2019. DMRG stimulated X-ray Raman of homovalent and mixed-valence [2Fe-2S].
- [V] arXiv:1803.11248 Nocera et al. 2018. DMRG RIXS for 1D chains.
- [V] arXiv:2405.11015 Fomichev et al. 2024. Quantum XAS algorithms for battery materials, CAS(22e,18o) O-Mn cluster.
- [V] arXiv:2506.15784, 2505.08612, 2602.20270. Quantum XAS, logical-QPE XAS and RIXS for battery materials (titles verified).
- [V] arXiv:2503.09214 Jensen et al. 2025. First isotropic HFCs on quantum hardware (OH, NO, OH+).
- [V] arXiv:2511.09730 Fuglsbjerg et al. 2025. qLR NMR spin-spin couplings.
- [V] arXiv:2601.18898 Zak 2026. FT block encoding of the Pauli-Breit Hamiltonian (SOC plus spin-spin). "Explicit spin degrees of freedom do not worsen asymptotic scaling."
- [V] arXiv:2512.15889 Zhou et al. 2025. FT algorithms for PDT BODIPY absorption and ISC rates, active spaces of 11 to 45 spatial orbitals.
- [V] arXiv:2406.04992 Chawla et al. 2024 and arXiv:2211.06907. Relativistic VQE PDMs of heavy molecules.
- [V] arXiv:2212.02058. Bayesian phase difference estimation for fine-structure splitting.
- [V] arXiv:2303.09010 Eskridge, Krakauer, Zhang 2023. AFQMC with SOC for the ZFS of a Co2+ complex.
- [V] arXiv:2207.02435 / doi:10.1063/5.0107805 Zhai and Chan, JCP 2022. One-step SOC DMRG vs two-step, on a Dy octahedral complex and a bridged Dy dimer.
- [V] doi:10.1063/5.0127621 Z. Li, JCP 2023. Time-reversal-adapted relativistic DMRG.
- [V] arXiv:1710.08301. Relativistic DMRG in matrix-product formulation (title verified).
- [V] doi:10.1126/science.abl5470 Gould et al., Science 2022. Mixed-valence Ln2 (Tb, Dy) with a single-electron metal-metal bond, coercive fields above 14 T.
- [V] doi:10.1021/acs.jpca.2c08526 Shang et al., JPCA 2023. Theory of relaxation in mixed-valence dilanthanides (no abstract in Crossref).
- [V] doi:10.1021/jacs.0c10612 Gould et al., JACS 2020. Bipyrimidine radical-bridged Ln2 exchange.
- [V] doi:10.1038/s41557-018-0158-9 Knecht, Jensen, Saue, Nat Chem 2019. The U2 quadruple bond.
- [V] doi:10.1039/d4sc05471g Radon et al., Chem Sci 2024. SSE17 spin-state benchmark derived from experiment. The Crossref abstract is only one line; the numerical MAE values quoted here come from memory and are [UNVERIFIED].
- [V] chemRxiv doi:10.26434/chemrxiv-2023-jnt7m Neugebauer et al. CCSD(T) vs ph-AFQMC on 3dTMV. CCSD(T) is within about 2 kcal/mol inside a symmetry-breaking-defined regime.
- [V] doi:10.1002/cphc.202500768 Gao et al., ChemPhysChem 2026. HEOM spin-vibronic dynamics of [Fe(bmip)2]2+.
- [V] doi:10.1039/d5cp01208b. BSE@GW LVC spin-vibronic protocol for Fe(II), PCCP 2025.
- [V] doi:10.1021/acs.inorgchem.1c01838. Spin-vibronic LS to HS mechanism of an octahedral Fe(II), Inorg Chem 2021.
- [V] arXiv:2605.00745 Bay-Smidt et al. 2026. Nanographene PPP gaps and Trotter error cancellation for gaps.
- [V] arXiv:2603.11891 Tran et al. 2026. O2BMP2 matches ADC(3)/EOM-CCSD on 30 INVEST molecules.
- [V] arXiv:2202.02364. Trapped-ion wave-packet branching through an engineered conical intersection.
- [V] arXiv:2601.22091 Naranjo et al. 2026. QC for spin-defect ESR Hamiltonians.

## Candidates

### C1. Exchange-coupled spin ladders of synthetic 3d polynuclear clusters, including dynamic correlation (J, biquadratic and double-exchange B, spin-projection coefficients)
- Domain: bioinorganic and molecular magnetism (synthetic [2Fe-2S]/[4Fe-4S] model complexes, Mn3/Mn4 oxo cubanes, Ni4 cubanes, mixed-valence Fe2/Mn2).
- Input: X-ray geometry of a polynuclear cluster with 2 to 8 open-shell 3d centres and its oxidation state. Output: the low-energy spin ladder (energies of the lowest state in each S and redox sector), fitted J/B parameters, and spin-projection coefficients. These are compared with INS, magnetic susceptibility chi(T), EPR/ENDOR and Moessbauer data.
- Classical wall: DMRG handles the static (magnetic) active space (Sharma 2014; Kurashige 2013; Li 2019). TPSCI reaches (42e,49o) (2508.13002). Quantitative J, however, needs ligand and double-shell dynamic correlation (DDCI-level). DMRG-NEVPT2 with 4-RDMs, or DMRG on active spaces with 100 or more orbitals, is the frontier. The target spacings are below 1 mHa (2105.01754).
- Quantum mechanism: qubitization QPE of each spin and redox sector, with spin-adapted initial states built from classical DMRG/BS-DFT (the overlap is high because the states are "largely simple"). Gaps are computed directly and benefit from Trotter or QPE gap-error cancellation (2605.00745). This replaces the large-active-space DMRG/NEVPT2 step. Any advantage would be polynomial in active-space size at fixed precision. It is not exponential in general (2208.02199).
- Novelty: C. Fe-S ground-state energies on quantum hardware exist (2601.06935, 2601.10813) and are contested for SQD (Vitale 2026 spin audit; 2501.07231). In queries 5, 22, 26 and 27 I found no study of J/spin-ladder observables compared with DMRG/TPSCI/NQS as a quantum-vs-classical study.
- Main risk: 2601.04621 shows that FeMoco is classically solvable by ranking simple states with CC plus DMRG plus extrapolation, and the same machinery likely extends to spin ladders. The required precision (1-10 cm^-1) multiplies the QPE cost. Model floor: geometry sensitivity (2105.01754), because a J change from structure can exceed solver error.
- Resources: about 1e11 Toffolis per state at a 10 cm^-1 target for about 100-150 orbitals. This is extrapolated from FeMoco THC estimates of about 1e10 at 1.6 mHa, is [UNVERIFIED], and must be recomputed.
- Verdict: plausible.

### C2. Spin-orbit-coupled exchange spectra of multinuclear f-element complexes (mixed-valence Ln2 with a metal-metal bond, radical-bridged Ln2, U/Np dimers)
- Input: crystal geometry of Ln2 (Gould 2022, doi:10.1126/science.abl5470) or radical-bridged Ln2 (doi:10.1021/jacs.0c10612) or a U dimer. Output: the low-lying SO-coupled exchange-split doublets and anisotropic exchange tensors, the magnetisation-blocking barrier (Ueff), and g-tensors. These are compared with far-IR/INS, magnetometry and EPR.
- Classical: two-step CASSCF-SO/RASSI with POLY_ANISO/Lines fragment models; one-step SO-DMRG (Zhai and Chan 2022, applied to a bridged Dy dimer); time-reversal-adapted R-DMRG (Li 2023); X2C-AFQMC with SOC (2303.09010); 4c KRCI/FSCC for small species (U2, 2601.10813; Knecht 2019).
- Quantum mechanism: QPE on a 2-component (Pauli-Breit or X2C) Hamiltonian, block-encoded with explicit SOC in a double-factorised Majorana form (Zak 2601.18898). The number of spin-free states that a two-step RASSI needs grows combinatorially with 4f/5f count and multiplicity, and a one-step QPE avoids it. The target is the large one-step SO active space (two 4f shells plus the sigma bond plus donor orbitals plus the 5d/6s double shell) with dynamic correlation, where one-step SO-DMRG's complex-arithmetic cost is the wall.
- Novelty: B. There are relativistic QC algorithms and resource analyses (2601.18898, 2406.04992, 2212.02058) and a U2 benchmark (2601.10813). In queries 15, 20, 30, 33 and 35 I found no quantum study of SO-coupled exchange or blocking barriers in multinuclear f-element magnets.
- Main risk: exchange splittings in 4f systems are often small, and CASSCF-SO plus fragment models may already reproduce the experimental Ueff and ladders within the uncertainty of the experiment. Ligand-field dynamic correlation and vibronic (spin-phonon) effects set the model floor for relaxation. Mixed-valence Ln2 with a sigma bond is the regime least likely to be classically easy.
- Verdict: plausible.

### C3. L-edge XAS / 2p3d RIXS / K-beta XES of exchange-coupled multinuclear clusters (Fe-S, Mn-oxo) in operando redox states
- Input: cluster geometry, redox state and edge. Output: the L2,3 XAS and 2p3d RIXS maps (and K-beta XES), including exchange-split and valence-delocalisation features, for comparison with synchrotron/XFEL spectra.
- Classical: correction-vector RAS-DMRG (2305.08184, mononuclear, stated goal larger clusters); DMRG X-ray Raman of [2Fe-2S] (1908.05802); RASPT2/RASSI; charge-transfer multiplet fits (CTM4XAS/Quanty, parametrised); DMRG RIXS for chains (1803.11248).
- Quantum mechanism: time-domain Hadamard-test / QPE dipole-autocorrelation spectra of the core-excited Hamiltonian (Fomichev 2405.11015; logical QPE XAS 2505.08612; RIXS 2602.20270). Core-hole lifetime broadening (about 0.2-0.5 eV) caps the total evolution time, so circuits are shallower than for ground-state energy estimation. Each additional open-shell metal multiplies the multiplet count. This replaces the correction-vector DMRG sweep for each frequency.
- Novelty: C/D subsection. Quantum XAS/RIXS exists only for single-site battery oxides. In queries 13, 21 and 34 I found no study of multinuclear exchange-coupled clusters compared with CV-RAS-DMRG.
- Main risk (lesson 5, information vs computation): the lifetime broadening that makes the problem easy for a quantum computer may also wash out the features that need exact correlation, so parametrised multiplet fits could match the experiment. The benchmark must show a spectral feature that changes a structural or redox assignment.
- Verdict: plausible.

### C4. Paramagnetic NMR contact shifts and hyperfine tensors in exchange-coupled mixed-valence clusters (ligand nuclei)
- Input: geometry of a cluster and its spin state. Output: ligand 1H/13C/19F/31P contact shifts and their temperature dependence (a Boltzmann average over the spin ladder), and ligand hyperfine tensors, for comparison with pNMR and ENDOR.
- Classical: BS-DFT with spin projection; DMRG spin densities; CASSCF/NEVPT2 pNMR (Vaara/Autschbach-style [UNVERIFIED specific refs]).
- Quantum: QPE-prepared eigenstates across the ladder, with the spin 1-RDM read out by amplitude estimation (Heisenberg-limited). Nearby: the first HFCs on hardware (2503.09214).
- Novelty: C.
- Main risk: metal-nucleus hyperfine is dominated by core spin polarisation outside any feasible active space, which is a model floor, so only ligand nuclei are credible. The temperature average needs many excited states.
- Verdict: weak.

### C5. Fe(II) photosensitiser MLCT-to-MC branching and lifetime (spin-vibronic dynamics across singlet, triplet and quintet manifolds)
- Input: an Fe(II) polypyridyl/NHC complex and its excitation. Output: the 3MLCT lifetime, the 3MC/5MC population yields, and K-beta XES and transient absorption traces.
- Classical: LVC/QVC with ML-MCTDH, HEOM (doi:10.1002/cphc.202500768), BSE@GW-LVC (doi:10.1039/d5cp01208b), surface hopping (SHARC); CASPT2/NEVPT2 spin-state energetics (an IPEA-shift-sensitive error of several kcal/mol).
- Quantum: Hamiltonian simulation of multi-state, multi-mode spin-vibronic models (qudit/boson registers), with QPE-grade MC/MLCT energetics as input.
- Novelty: B. Nearby: PDT ISC rates (2512.15889) and singlet fission (Motlagh). Queries 10, 28 and 36 found no quantum study of Fe(II) SCO dynamics.
- Main risk: the error budget is dominated by the LVC parameterisation and by the MC-state energies (electronic structure, not dynamics). ML-MCTDH covers about 10-20 states x 50 modes. This is the same structure as the killed OPV/singlet-fission cases.
- Verdict: weak.

### C6. Lanthanide 4f-4f transition intensities and ligand-to-Ln sensitisation rates
- Input: an Eu(III)/Tb(III) antenna complex. Output: 4f-4f oscillator strengths (hypersensitive transitions), ab initio Judd-Ofelt Omega_lambda, and the ligand-T1 to Ln energy-transfer rate / luminescence quantum yield.
- Classical: CASSCF/RASSI-SO intensities; semi-empirical Malta/LUMPAC; dynamic-coupling models.
- Quantum: SO-QPE eigenstates plus a transition-dipole estimate. Parity-forbidden intensities come from tiny admixtures of opposite-parity configurations (4f^(n-1)5d, LMCT) and from ligand polarisation, which calls for large correlated SO active spaces.
- Novelty: A. Query 19 and the Crossref queries in 24 found no QC paper and sparse ab initio work.
- Main risk: the model floor is large (vibronic intensity borrowing, geometry fluctuations, solvent), the complexes are large, and the observables are measured in solution.
- Verdict: weak.

## Killed ideas
- INVEST / inverted singlet-triplet gap emitters: weakly correlated organics. ADC(2), EOM-CCSD, SCS-CC2 and O2BMP2 reach ADC(3)/EOM-CCSD accuracy on 30 molecules (2603.11891). Vibronic and solvent effects dominate the residual error. No classical wall.
- Tunnelling KIEs: no QC paper found (query 9), but instanton and RPMD handle the nuclear quantum dynamics cheaply. The error sits in PES accuracy (CCSD(T)), and nuclear dynamics is low-dimensional, so the problem is not solver-limited in any quantum-attackable way.
- Electrochemical potential-dependent correlated barriers: the model floor (double layer, explicit solvation, grand-canonical charge, potential control) exceeds any multireference solver gain, which is lesson 6.
- Photochemical quantum yields at conical intersections (organic photoswitches): classical MCTDH, surface hopping and XMS-CASPT2 are adequate for small chromophores. Yields depend on PES topography, which is a model floor. Analog trapped-ion demos exist only on engineered toy models (2202.02364).
- Reaction-network ranking under multireference error: an argmin readout (lesson 3), with every node a standard ground-state problem. The Cu-oxo case was already killed because classical multireference flips the ranking.
- Excited-state absorption of organic chromophores: EOM-CC and ADC are adequate. Transition-metal ESA folds into C5.
- Mononuclear spin-state energetics (Fe/Co SCO gaps): SSE17 (doi:10.1039/d4sc05471g) and CCSD(T) vs ph-AFQMC (chemRxiv 2023-jnt7m) show CCSD(T)/AFQMC at about 1-3 kcal/mol against experiment-derived references. The exact MAE is [UNVERIFIED].
- NMR J-couplings via qLR: small molecules, where CCSD matches (2511.09730). No wall.
- Fe-S ground-state energies via SQD/QSCI: category E. The spin audit (Vitale 2026) and 2501.07231 dispute the claims, and FeMoco is near-classically solved (2601.04621).
- Nanographene PPP gaps: already proposed with resource estimates (2605.00745). PPP/Hubbard on bipartite lattices is tractable with DMRG and QMC.
- ISC rates in BODIPY/PDT photosensitisers: already claimed (2512.15889, 2601.18898).
- Atmospheric photolysis quantum yields: small molecules are handled exactly by MCTDH, and larger ones are limited by the PES.
- Mononuclear SMM ZFS and anisotropy: CASSCF-SO/NEVPT2 and AFQMC-SOC (2303.09010). Rare-earth magnets were already killed as classically tractable.
- Heavy-molecule eEDM effective fields / PDMs: relativistic CC is accurate for these single-reference systems, and relativistic VQE demonstrations already exist (2406.04992).

## Overall assessment
Within this lens, the only regimes where the solver error plausibly exceeds the model error and a scaling variable exists are:
- multinuclear open-shell clusters (C1), where the scaling variable is the number of metals and the active space;
- f-element multinuclear systems with non-perturbative SOC (C2), where the scaling variable is the f-shell count and the SO active space;
- multinuclear core-level spectra (C3), where the scaling variable is the number of metals.

All three face the same threat: classical CC/DMRG on "largely simple states" (2601.04621). C3 additionally carries lesson 5, broadening hiding the information. None is category A/B with a demonstrated classical wall. The best subsection is C2 (category B), because one-step SO-DMRG is the published classical frontier and the quantum block encoding of SOC carries no asymptotic penalty (2601.18898).
