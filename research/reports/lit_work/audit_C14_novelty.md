# Audit C14 (novelty / prior art): finite-T polarized S(q,w) of 3D dipolar-octupolar pi-flux QSI

Date: 2026-09-28. Auditor role: NOVELTY / PRIOR-ART. Status: COMPLETE.

## Query log
- WebSearch: budget exhausted (200/200), so I fell back to the arXiv API, Crossref, Semantic Scholar and OpenAlex via WebFetch.
- arXiv API `abs:"spin ice" AND abs:"quantum computer"`: 2404.04207 and 1810.00446 only. No quantum-computing hits.
- arXiv API `all:"quantum spin ice" AND (quantum processor|quantum simulation|trapped ion|Rydberg|superconducting qubits)`: 2603.28125 (2D annealer, dipolar spin ice monopole transport), 2502.00836 (3D Rydberg QSI RVB), 2305.08571 (2D qubit spin ice), 2301.04657 (QSI in 3D Rydberg arrays, ground-state phase diagram), 2009.04499, 1404.5326.
- arXiv API `(pyrochlore OR spin ice) AND (quantum circuit|quantum computer|...)`: only neutron papers.
- arXiv API `abs:"quantum link model" AND (3+1|pyrochlore|three-dimensional)`: 2601.04345 (cold-atom 3+1D U(1) LGT proposal with TTN benchmark), 2210.14836 (dipolar spinor 2D/3D QLM proposal), 2201.07171 (ED on 3+1D tubes), 2602.22332.
- arXiv API `abs:"dynamical structure factor" AND (quantum computer|processor|hardware|algorithm)`: 2607.07138 (Granet, pumping, trapped-ion, 1D), 2607.02673 (quench spectroscopy, 101-spin XXZ chain), 2603.15608 (Lee, KCuF3, 1D, 50 qubits), 2410.03958 (Bauer, QuEra, TFIM chain), 2304.06146 (dimer), 1910.14213 (Sels), 2508.15935 (EELS resource estimate).
- arXiv API `(neutron scattering|structure factor) AND (fault-tolerant|resource estimate|T gates|qubitization)`: **2607.13301 (Google, Andersen et al.: finite-T linear and nonlinear magnon response of a 2D XY magnet, 97 qubits; MPS inaccurate away from small systems or low T)**, 2607.01568 (ORNL/LANL validation framework: quantum simulation vs INS vs classical), 2606.27734, 1912.06076 (Baez: DSF BQP-hard).
- arXiv API `(dipolar-octupolar|pi-flux QSI|π-flux) AND (dynamics|structure factor|spectrum)`: 2510.14813, 2502.14067, 2406.18650, 2406.01472, 2404.15902, 2401.09551, 2312.11641, 2312.03106, 2311.04269, 2304.05452, 2301.05240, 2201.00828, 2112.00014, 2108.01096.
- arXiv API `(quantum spin ice|pyrochlore) AND (neural quantum|neural-network|tensor network|PEPS|DMRG|VMC)`: 2604.11880, 2405.12745, 2311.11561, 2210.07235, 2203.00032 (pyrochlore tube, ED/DMRG/METTS), 2111.06411 (NN sign structure, 48 sites), 2106.09722 (DMRG ground state, 128 spins), 2101.08787 (NQS, 64 spins), 2010.03563.
- arXiv API `abs:"spin liquid" AND (quantum processor|computer|trapped-ion|superconducting) AND (dynamics|spectroscopy|structure factor)`: all 1D or 2D (Kitaev honeycomb 2501.18554, 2507.08939; kagome 2401.03015; 2604.16164 nonlinear spectroscopy; 2203.15291 RuCl3 on Sycamore).
- arXiv API `ti:"quantum spin ice"`, sorted by date, 60 results. New items: **2609.28643 (defect poisoning of QSI: ~2% vacancies dominate the dynamics, below the levels reported in Ce pyrochlores)**, 2608.11305, 2607.12274 (Ce2Sn2O7 orders at 40 mK), 2601.20766, 2512.14843, 2505.15677, 2502.19482, 2407.07640, 2306.13183 (Ce2Zr2O7 in field, with NLC), 1911.10243 (random QSI, ED N=64).
- arXiv API `abs:"3+1D" gauge theory AND (quantum computer|resource|circuits)`: 2608.16783, 2604.15132, 2507.12589, 2307.05593, 2201.02412, 2105.06019. None mentions spin ice or pyrochlore.
- arXiv API `abs:pyrochlore AND (Trotter|qubits|quantum simulator|digital quantum|Gibbs state)`: only 2301.04657, 2109.08799 (classical TPQ), 1806.04014. No gate-model pyrochlore dynamics.
- arXiv API pyrochlore + (neural network quantum state | transformer | group convolutional): no NQS paper on the pi-flux DO QSI. The only NQS pyrochlore work is Heisenberg (2101.08787, 64 spins). The candidate's "NQS ground states <=108 spins" is [UNVERIFIED].
- Crossref `quantum spin ice quantum computer simulation dynamics` (2020+): nothing on target.
- Crossref `quantum algorithm finite temperature dynamical correlation functions structure factor`: Sun et al. PRX Quantum 2, 010317 (2021) (QITE finite-T dynamical properties); Eklund, Digital Discovery 2026 (10.1039/d5dd00381d); Irmejs, Quantum 2025 (10.22331/q-2025-02-19-1639); Altuntas, QST 2025. All generic.
- Crossref `Ce2Zr2O7 quantum spin ice` (2022+): Smith et al. Annu. Rev. CMP 2025 (10.1146/annurev-conmatphys-041124-015101), Shah et al. PRX 15, 011025 (2025), Zhou et al. Nat Commun 2026 (10.1038/s41467-026-74589-6), Hosoi PRL 129, 097202, Desrochers PRL 132, 066502, Bhardwaj npj QM 2022.
- Crossref bibliographic lookup for Gao 2404.04207: published as Nature Physics 21, 1203-1210 (2025), doi:10.1038/s41567-025-02922-9, under a new title. The follow-up is PRL (2026) doi:10.1103/svt2-m3pp (= 2601.03202).
- I downloaded the arXiv:2404.04207v1 PDF and extracted its text (parameters, resolution, the GMFT discrepancy). See below.
- Semantic Scholar citation lists read in full: arXiv:2401.09551 (7 citers), arXiv:2404.04207 (25 citers), arXiv:2201.00828 (17 citers).
- Abstract and HTML pages read: 2607.13301, 2607.01568 (+html), 2510.14813 (+html), 2601.03202, 2609.28643, 2201.00828, 2603.28125, 2403.00910, 2409.03097, 2409.17142, 2305.08261.
- Rate limits: arXiv API returned 429 twice late in the session. OpenAlex returned 429 on all 4 attempts, so cited-by was done through Semantic Scholar. Semantic Scholar search returned 429, but its citations endpoint worked.

## Verified citations (each checked this session via arXiv abs page/API, Crossref or Semantic Scholar)

Quantum side (nearest):
- Lee et al., arXiv:2603.15608 (2026): 50-qubit superconducting processor; KCuF3 and XXZ chain S(q,w) compared with INS. 1D.
- Granet et al., arXiv:2607.07138 (2026): pumping approach on a trapped-ion computer (Quantinuum); 20-site 1D Heisenberg and copper sulfate, compared with neutron data.
- Millar et al., arXiv:2607.02673 (2026): quench spectroscopy on a 101-spin XXZ chain; classical simulation was feasible in the tested regime.
- Bauer et al., arXiv:2410.03958 (2024): analog QuEra simulation of neutron scattering from a TFIM chain.
- **Andersen et al. (Google, ~330 authors), arXiv:2607.13301 (2026): finite-T linear and nonlinear magnon response of a 2D XY spin-1/2 magnet, 97 qubits. MPS predictions are "inaccurate away from" small systems or low T.** This is the closest beyond-MPS finite-T spectral study. It is 2D, unfrustrated and sign-free, with no material or INS target.
- Buchs et al., arXiv:2607.01568 (2026): validation framework comparing quantum simulation, INS and classical simulation. Generic; no pyrochlore.
- Baez et al., arXiv:1912.06076: dynamical structure factors of dynamical quantum simulators (BQP-hardness).
- Sun et al., PRX Quantum 2, 010317 (2021): QITE for finite-T static and dynamical properties of spin systems.
- Shah et al., arXiv:2301.04657 / PRX 15, 011025 (2025): QSI in 3D Rydberg arrays, ground-state phase diagram (proposal).
- Wang et al., arXiv:2502.00836: doped RVB and robustness of spin-ice phases in 3D Rydberg arrays (ground state and thermodynamics).
- Giergiel & Surowka, arXiv:2603.28125 (2026): quantum annealer realization of 2D square dipolar spin ice with >400 vertices; super-diffusive monopole transport.
- King et al., arXiv:2403.00910, Science 388, 199 (2025): beyond-classical claim for quench dynamics of 2D, 3D and infinite-dimensional spin glasses on an annealer.
- Cochran et al., arXiv:2409.17142, Nature 642, 315 (2025): (2+1)D Z2 LGT charge and string dynamics on a superconducting processor.
- Orlando et al., arXiv:2601.04345 (2026): cold-atom 3+1D U(1) LGT simulator proposal.
- Fontana et al., arXiv:2210.14836: spinor dipolar atoms for 2D/3D quantum link models.
- Joshi et al., arXiv:2507.12589: qudit circuits for 2+1D QLM quench dynamics.

Classical side (nearest):
- Desrochers & Kim, arXiv:2401.09551 (2024): SCEBR finite-T dynamics for 0-flux and pi-flux QSI.
- Desrochers & Kim, arXiv:2301.05240, PRL 132, 066502 (2024): GMFT spectroscopic signatures (three-peak pi-flux spinon continuum).
- Hosoi et al., arXiv:2201.00828, PRL 129, 097202 (2022): ED + MD S(q,w) in all four DO-QSI regimes; the pi-flux octupolar regime matches Ce2Zr2O7 best. I did not extract the ED cluster size; the candidate's "32 sites" is not re-verified.
- Bhardwaj et al., arXiv:2108.01096, npj QM (2022) doi:10.1038/s41535-022-00458-2: FTLM + MC + spin dynamics; pi-flux U(1) QSL for Ce2Zr2O7.
- **Zhou, Zhou, Desrochers, Kim, Meng, arXiv:2510.14813, Nat Commun (2026) doi:10.1038/s41467-026-74589-6: multi-directed-loop QMC + SAC S(q,w) at L=3 and L=4 (108 and 256 spins, 4L^3 convention), down to T ~ 12 J±^3/Jz^2, in the 0-flux regime only. The paper states "QMC encounters a sign problem" in the pi-flux J±<0 regime "where most QSI candidate materials reside". The pi-flux regime is treated with ED on a 16-site cubic cluster plus GMFT. Best fit for Ce2Zr2O7: J± ~ -0.3 (Jz = 1).**
- Zhou et al., arXiv:2502.14067 and 2406.18650: GMFT + MC phase diagrams in field.
- Zhao & Chen, arXiv:2404.15902: interprets the low-energy INS of Ce2Sn2O7 and Ce2Zr2O7 as an electric-monopole continuum. This is a competing interpretation.
- Herz, Schafer, Gonzalez, Luitz, arXiv:2607.24679 (2026-07): sign-optimized QMC via local basis rotation, benchmarked on 1D chains and the 2D maple-leaf lattice. Not yet applied to the pyrochlore; it threatens the sign-problem leg of the argument.
- Begusic & Chan, arXiv:2409.03097, PRX Quantum 6, 020302 (2025): sparse Pauli dynamics in 2D and 3D (3D TFIM quenches, where tensor networks struggle).
- Tindall et al., arXiv:2503.05693 (2025): BP tensor networks for 2D/3D disordered dynamics (the D-Wave rebuttal).
- Mauron & Carleo, arXiv:2503.08247 (2025): t-VMC, D-Wave rebuttal, up to 128 spins.
- Wiersema, arXiv:2609.01719 (2026): t-VMC simulation of the D-Wave advantage experiment.
- Feng et al., arXiv:2203.00032: XXZ model on a pyrochlore tube with ED/DMRG/METTS (finite-T TN on a quasi-1D pyrochlore geometry).

Experiment and model floor:
- **Gao et al., arXiv:2404.04207, published as Nature Physics 21, 1203 (2025), doi:10.1038/s41567-025-02922-9.** Polarized INS on ThALES (ILL) at T = 50 mK, fitted with GMFT for the spinons (fixed pi-flux background) plus Gaussian QED for the photons.
  - Fitted couplings: J_x = 0.076 meV, J± = (J_y+J_z)/4 = 0.021 meV, theta = 0.12 pi, hbar c/a0 = 0.65 k_B T_exp.
  - Resolution FWHM is 0.076, 0.062 and 0.042 meV at (0,0,1), (3/4,3/4,0) and (1,1,0). The theory was broadened by 0.035-0.04 meV.
  - Peaks appear at E ~ 0, 0.05 and 0.12 meV.
  - **Stated discrepancy (text extracted from the arXiv v1 PDF): "the model predicts a finite M_z - M_y at Q = (1,1,0) in the inelastic spinon contribution, which is not seen in the experiment. This could potentially be attributed to effects beyond GMFT, such as thermally excited fluxes or spinons-photon interactions."**
- Gao et al., arXiv:2601.03202, PRL (2026) doi:10.1103/svt2-m3pp: [111]-field same-temperature subtraction; 0.15 T suppresses the photon weight. GMFT and ED support pi-flux.
- **Sanders, Naik, Hallen, Schafer, arXiv:2609.28643 (2026-09-23): at dilution "as low as two percent, well below those reported in cerium-based pyrochlores", vacancy-induced processes "dominate over the conventional quantum-spin-ice dynamics". Methods: large-scale QMC + ED.**
- Smith et al., arXiv:2607.12274 (2026): Ce2Sn2O7 undergoes a first-order transition to long-range order at ~0.04 K, so its ground state is not QSI.
- Yuan et al., arXiv:2601.20766 (2026): Ce2Sn2O7 diffuse scattering resembles classical dipolar spin ice, which implies further-neighbour couplings the NN XYZ model lacks.
- Poree et al., arXiv:2305.08261, PRB 112, L180404 (2025): exchange hierarchy of Ce2Hf2O7.
- Poree et al., arXiv:2304.05452: backscattering INS on Ce2Sn2O7 showing fractional matter.
- Smith et al., Annu. Rev. CMP (2025) doi:10.1146/annurev-conmatphys-041124-015101: review, verified by Crossref search listing. Abstract not retrieved (429).
- Smith et al., PRX 2022, "Case for a U(1)pi QSL in Ce2Zr2O7": [UNVERIFIED]; the Crossref lookup failed.

## Classification: B (scoped)

## EXACT PRIOR WORK
None found. No quantum algorithm (gate-model or analog) has been used to compute finite-T, polarization-resolved S(q,w) of the 3D DO XYZ pyrochlore model and compare it with tuned classical methods or with polarized INS data.

## NEAREST QUANTUM WORK
- 1D material S(q,w) on hardware: 2603.15608, 2607.07138, 2607.02673, 2410.03958.
- Finite-T 2D XY magnon response beyond MPS: 2607.13301 (Google, July 2026).
- 3D QSI appears only as Rydberg ground-state proposals (2301.04657, 2502.00836) and as 3+1D U(1) LGT analog proposals (2601.04345, 2210.14836).
- 2D spin-ice annealer dynamics: 2603.28125.
- A 3D spin-glass quench beyond-classical claim (2403.00910) that was then attacked by BP-TN (2503.05693) and t-VMC (2503.08247, 2609.01719).

## NEAREST CLASSICAL WORK
- GMFT (2301.05240; used for the Nat. Phys. 2025 fit)
- SCEBR at finite T (2401.09551)
- ED + MD (2201.00828)
- FTLM + MC + spin dynamics (2108.01096)
- QMC + SAC at 108-256 spins, 0-flux only (2510.14813), with ED-16 for pi-flux in the same paper
- Sparse Pauli dynamics in 3D (2409.03097)
- BP-TN in 3D (2503.05693)
- Sign-optimized QMC (2607.24679; not yet applied to the pyrochlore)

## WHAT HAS BEEN TESTED
- Ranking 0-flux vs pi-flux, and dipolar vs octupolar, against Ce2Zr2O7 INS has been done by ED+MD (Hosoi 2022), FTLM+MC (Bhardwaj 2022), GMFT (Gao 2025 Nat Phys; Gao 2026 PRL, with ED) and QFI via QMC/ED/GMFT (Zhou 2026). All of them favour pi-flux (octupolar-dominant) for Ce2Zr2O7. The competing interpretation is the electric-monopole continuum of Zhao & Chen (2404.15902).
- A quantum-vs-classical finite-T spectral response has been run only for the 2D XY model (Google 2607.13301). That model is unfrustrated and sign-free.

## WHAT HAS NOT BEEN TESTED
- A controlled beyond-mean-field finite-T calculation (T ~ 0.2 J±, pi-flux, L >= 2-3) of the polarization anisotropy M_z - M_y at Q=(1,1,0). The question is whether thermal visons/fluxes or spinon-photon coupling remove the inelastic anisotropy that GMFT predicts, which is the discrepancy flagged in Gao 2025. I found no quantum study and no quantitative classical study beyond ED-16 and GMFT.
- Any quantum resource estimate or hardware run for real-time correlators of the 3D pyrochlore XYZ model.
- A head-to-head of GMFT, SCEBR, ED, sparse Pauli, BP-TN and t-VMC for pi-flux finite-T S(q,w) at a common system size. Only single-family convergence exists.
- Disorder-averaged (vacancy) S(q,w) in the pi-flux regime at INS resolution. 2609.28643 uses QMC and ED, but I did not extract which flux regime or which dynamics it covers.

## WHY THE GAP IS MATERIAL (and where it is cosmetic)
- **Cosmetic:** the headline decision "0-flux vs pi-flux" has already been decided the same way by at least four independent classical families. A quantum computation that re-ranks it would not change a decision, so it fails audit question 1 as posed.
- **Material:**
  - (i) 2510.14813 states explicitly that the pi-flux sign problem blocks QMC, so no unbiased large-cluster finite-T method exists in the regime the materials occupy.
  - (ii) GMFT's documented failure on the Q=(1,1,0) polarization is a concrete observable on which mean-field and exact answers can differ.
  - (iii) 3D + frustrated + finite T differs in mechanism from the 2D XY Google result.

## WHY IT COULD BE A NEW PAPER
A working title would be "Beyond-mean-field polarized dynamics of pi-flux quantum spin ice: classical frontier and quantum resource estimate". The paper would:
- (a) run ED-16/32, NLCE, sparse Pauli, BP-TN, t-VMC and GMFT on the same finite-T polarized observable at Q=(1,1,0);
- (b) report where these methods disagree;
- (c) give fault-tolerant T-counts for Trotter or qubitization plus thermal-state preparation on the 432-spin L=3 cluster.

Part (a) is publishable as a classical result even if (c) shows no advantage.

## HARD RED FLAGS FOR THE ADVANTAGE CLAIM (from the literature found)
1. **The resolution caps the time horizon.**
   - Gao 2025 resolution FWHM is 0.04-0.076 meV, i.e. 2-3.6 J± (J± = 0.021 meV). The decision-relevant t_max is therefore ~ hbar/FWHM, of order 1/J± to a few/J±, not 50/J±.
   - The photon bandwidth (hbar c/a0 = 0.65 k_B T, ~0.003 meV) is ~15x below the resolution. Photon dynamics therefore enter only as integrated quasi-elastic weight, which is a static or imaginary-time quantity.
   - Short-time finite-T dynamics is where ED, NLCE, sparse Pauli and cluster methods are strongest. This repeats protein lesson 5.
2. **Model floor.** 2609.28643 finds that ~2% vacancies (below reported Ce-pyrochlore levels) dominate the QSI dynamics. Ce2Sn2O7 orders at 40 mK (2607.12274) and needs further-neighbour couplings (2601.20766). The clean NN XYZ model may be the wrong model at the energy scale the quantum solver would resolve (protein lesson 6).
3. **Temperature.** T = 50 mK ~ 0.2 J± is above the photon scale. The physical state is a thermal state above the photon bandwidth, and warmer states favour sparse Pauli and cluster expansions.
4. **Sign-optimized QMC** (2607.24679, July 2026) is a live threat to the sign-problem leg and has not been tested on the pyrochlore.

## Scoped statement
In the sources searched through 2026-09-28, I found quantum S(q,w) computations for 1D materials, a finite-T 2D XY magnon-response study beyond MPS, 3D QSI only in Rydberg ground-state proposals, 3+1D U(1) LGT only in analog proposals, and classical pi-flux dynamics by GMFT/SCEBR/ED/MD/FTLM (all detailed below). I found no study of:
- (D) a quantum algorithm for finite-T polarized S(q,w) of 3D DO pi-flux QSI, compared with (E) GMFT/SCEBR/ED or (F) 3D sparse Pauli/BP-TN/t-VMC;
- a quantitative beyond-GMFT account of the Q=(1,1,0) polarization discrepancy reported in Gao et al., Nat. Phys. 21, 1203 (2025).

Sources searched: arXiv (the API searches listed above), Crossref, the Semantic Scholar citation graphs of 2401.09551, 2404.04207 and 2201.00828, and arXiv abstract/HTML pages. OpenAlex was unavailable (HTTP 429).

Work found, by group:
- 1D quantum S(q,w): 2603.15608, 2607.07138, 2607.02673, 2410.03958.
- Finite-T 2D XY beyond MPS: 2607.13301.
- 3D QSI Rydberg proposals: 2301.04657, 2502.00836.
- 3+1D U(1) LGT analog proposal: 2601.04345.
- Classical pi-flux dynamics: 2301.05240, 2401.09551, 2201.00828, 2108.01096, 2510.14813.

## Verdict: WOUNDED
- Novelty category B holds for the exact quantum-vs-classical comparison.
- The flux-sector decision version is cosmetic: it is already settled classically, so no decision flips.
- A narrower target is material: the Q=(1,1,0) polarization anisotropy at T ~ 0.2 J± beyond GMFT, with vacancy disorder.
- Against that target, the data's resolution caps the needed t_max at a few/J±, and the vacancy model floor (2609.28643) is severe.

Recommendations:
- Re-scope the decision variable to the Q=(1,1,0) anisotropy.
- Drop Ce2Sn2O7.
- Add vacancy disorder to the model.
- Pre-test with ED-32, sparse Pauli and NLCE before any quantum resource work.

Kill criterion: kill if those three classical families agree on the Q=(1,1,0) anisotropy within the INS error bars.
