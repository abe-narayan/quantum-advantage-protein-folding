# Round 2 discovery lens: static / ground / low-T thermal quantities inside a multi-family classical wall

Date: 2026-09-28. Status: FINAL for this lens.

**Question.** Find problems whose decision-relevant quantity is a static, ground-state or low-T thermal property that:
- lies inside a multi-family classical wall;
- has S*G <~ 1e13, using early-FT QPE (single ancilla / QCELS);
- has a model floor below the solver spread.

**Round-1 inputs consulted first.**
- selection.md
- pool_and_shortlist.md: chemistry kills C32, C33 and C39; C17 in reserve.
- discovery_classical_frontier.md: W4 static TM clusters MOVING; W5 NCI CC/DMC MOVING to consensus; W6 metal surfaces; W12 doped Hubbard MOVING.
- audit_C01_classical.md and audit_C01_resources.md, for the WDM static branch.

All cost numbers are order-of-magnitude estimates unless they carry a citation with a table. Nothing here is an experimental result.

## 0. Bottom line

**One candidate plausibly passes the round-1 filter, and only conditionally.** It is S-M1: the multi-band ground-state phase competition (FCI vs CDW / anomalous Hall crystal) of hBN-aligned rhombohedral multilayer graphene at fractional filling.
- Category B/C. It leans toward physics.
- Main risk: a model floor from the normal-ordering scheme and the moire-potential parameters.

**Everything else tested here is killed** (section 3). The brief asked for 2-4 candidates. I did not lower the bar to supply a second one.

**Scoped structural finding: a trilemma for static targets.** Across the 17 static target families tested here, each filter kills a different family.

1. **Molecular / cluster chemistry** (multi-center spin states, exchange couplings, SMM barriers).
   - Active-space-only QPE is cheap, about 1e9-1e11 Toffoli per circuit. But the decision quantity then depends on dynamic correlation outside the active space. The model floor ends up at or above the solver spread.
   - Full-basis QPE removes that floor but costs 1e13-1e16 and has poor overlap.
   - Classical CC+DMRG ranking closes posted targets within 1-3 years (FeMoco 2601.04621, Fe4S4 2603.28648, SSE17).
2. **Ab initio periodic solids** (LNO-type contested ground states, defects, magnetic anisotropy).
   - Cost is 1e12-1e14 Toffoli per QPE even at a 2x2x2 k-mesh in DZVP (Rubin et al., PRX Quantum 4, 040303, Table VI).
   - Phonon ZPE and dynamic Jahn-Teller floors are the same size as the energy differences.
3. **Downfolded lattice models for real materials** (doped Hubbard, nickelates). The model floor (Hund coupling, downfolding) flips the answer (2602.20288).
4. **Exact-Hamiltonian systems** (electron gas, unitary gas, clean-limit quantum Hall). Either there is no practical decision, or the experimentally relevant question sits in a disorder floor.
5. **Warm dense matter, static branch.** The static observable is exactly where classical families reach furthest (xi-PIMC for static properties, FT-AFQMC, pseudo-fermion). Where they fail (H at eta >= 128), the cost exceeds 1e15.

**The one opening: engineered flat-band 2D materials with dense momentum-space interactions.** Four properties make this regime different:
- the Hamiltonian is specified to about 10-30%;
- the quantities needed are eigenvalues in momentum sectors, which is QPE-native with no sampling-dominated readout;
- exact classical diagonalization is capped by band mixing (2407.13770);
- the per-state-point cost can fall in the 1e11-1e13 range.

## 1. Query log (2026-09-28)

WebSearch was not used (budget exhausted). Every query below went through WebFetch.

1. arXiv abs 2302.05531 (Rubin et al., Bloch-orbital FT materials; LNO). PDF text extracted locally with pypdf; Table VI read.
2. arXiv API `all:LiNiO2 AND (QMC | AFQMC | Jahn-Teller)`: 9 hits (2507.00542, 2403.18919, 2310.11856, 2011.06441, 1911.01610, ...).
3. OpenAlex "spin state energetics discrepancy DMRG AFQMC transition metal cluster": HTTP 429.
4. arXiv API `abs:"early fault-tolerant" AND abs:"ground state energy" AND (resource|chemistry)`: 9 hits (2606.06442, 2508.02578, 2508.00533, 2405.03754, 2403.00077, 2310.13757, 2309.16790, 2209.06811, 2204.05955).
5. arXiv API `all:"Ir17+" OR (highly charged AND level crossing AND 4f)`: 2509.06710.
6. arXiv abs 2509.06710 (Os HCI 5s-4f crossing).
7. arXiv API `highly charged AND iridium AND (clock | alpha)`: 0 hits.
8. OpenAlex Ir17+ search: HTTP 429. OpenAlex then returned Retry-After ~78000 s and stayed blocked for the rest of the session.
9. Crossref "Identifying optical transitions Ir17+ highly charged": Berengut 2012 PRL (doi:10.1103/physrevlett.109.070802) and Chen 2024 PR Applied (doi:10.1103/physrevapplied.22.054059).
10. arXiv API `ti:"Accurate prediction of clock transitions"`: 1912.08714 (Cheung et al., PRL 124, 163001 (2020)).
11. arXiv API `AFQMC AND (DMRG|NEVPT2|CASPT2) AND (iron|copper|manganese|cluster) AND spin`: 0 hits.
12. arXiv API `abs:"auxiliary-field quantum Monte Carlo" AND abs:"spin gap"`: 6 hits, none a polynuclear TM disagreement.
13. OpenAlex iron porphyrin: HTTP 429.
14. Crossref "iron porphyrin spin state auxiliary-field QMC coupled cluster": Lee et al., JCTC 2020 (doi:10.1021/acs.jctc.0c00055); Zhang et al., JCP 2026 (doi:10.1063/5.0341498).
15. arXiv API `abs:"advantage tracker"`: 2603.28648 only.
16. arXiv API `hydrogen AND PIMC AND (density response | ITCF)`: 10 hits (2503.14014, 2502.04921, 2405.10627, 2403.08570, 2306.05814, 2304.10807, 2212.08326, 2207.14716, 2203.01797, and quant-ph/0611105, which is not relevant).
17. arXiv abs 2403.08570 (Dornheim et al., static density response of warm dense H).
18. arXiv API `warm dense AND (pseudo-fermion | fictitious identical | sign problem) AND hydrogen`: 4 hits.
19. arXiv API `neutron matter AND pairing gap AND (Monte Carlo | neural | lattice)`: 12 hits, including 2201.01308, 0805.2513 and 0708.2523.
20. arXiv abs 2211.11973 (Ding & Lin, QCELS).
21. arXiv abs 2011.03494 (Lee et al., THC).
22. arXiv API `MoTe2 AND continuum model AND fractional Chern AND parameters`: 2406.20036.
23. arXiv API `single-molecule magnet AND spin-phonon AND ab initio AND Raman`: 2507.17910, 2412.04362, 1704.06699.
24. arXiv API `ti:"Moire fractional Chern insulators"`: 0 hits.
25. arXiv API `fractional Chern AND band mixing AND (MoTe2|pentalayer|rhombohedral)`: 2608.12452, 2504.20140, 2407.13770.
26. arXiv abs 2608.12452 and arXiv abs 2407.13770.
27. arXiv API `(moire|fractional Chern|twisted bilayer) AND (quantum computer|phase estimation|fault-tolerant|quantum algorithm)`: 25 hits. Relevant: 2607.11380 (VQE for FQH manifolds) and 2510.09999 (modified QPE for the LDOS of TBG quasicrystals).
28. arXiv API `(neural network|DMRG|VMC) AND rhombohedral AND (fractional|anomalous Hall crystal)`: 2507.07921.
29. arXiv API `neural AND (moire|MoTe2) AND (fractional|Chern)`: 2503.13585.
30. arXiv API `5/2 AND Landau level mixing AND (anti-Pfaffian|PH-Pfaffian)`: 1603.03754, 1411.1068, 1410.3861, 1303.1541, 1209.6606, 0707.0483.
31. Crossref "Entangled quantum electronic wavefunctions of the Mn4CaO5 cluster": Kurashige, Chan, Yanai, Nat. Chem. 2013 (doi:10.1038/nchem.1677).
32. arXiv abs 2412.04362 (Mondal ... Lunghi, Co-dimer spin-phonon).

**Local work.**
- Read the round-1 notes listed at the top.
- Computed Hilbert-space dimensions, QPE cost brackets and 3P2 coherence lengths with python one-liners (not saved).
- A heredoc write of this file failed once in Bash. The file was then written with the Write tool.

## 2. Cost conventions used (early-FT QPE)

**QCELS.** Ding & Lin, arXiv:2211.11973, PRX Quantum 4, 020331 (2023) [VERIFIED abs].
- Maximal evolution time is delta/eps, and delta -> 0 as the initial overlap -> 1.
- Total cost is Heisenberg-limited, O~(1/eps). For small overlap it is combined with Fourier filtering.
- Per circuit: G ~ delta * pi * (lambda/eps) * C_W, where C_W is the qubitization walk cost.
- Repetitions: S ~ 1e2-1e3 per eigenvalue for overlap^2 ~ 0.1-0.5 [ESTIMATE].

**Other early-FT QPE assessments.** Seen at listing level only, not read in full:
- Kiss et al., arXiv:2405.03754.
- Nelson & Baczewski, arXiv:2403.00077: ~300x computational-volume reduction vs textbook QPE for minimal-basis H2.
- Dong, Lin, Tong, arXiv:2204.05955.
- Wang et al., arXiv:2209.06811.

**Anchor: FeMoco with THC.** Lee et al., PRX Quantum 2, 030305 (arXiv:2011.03494) [VERIFIED abs]: "about four million physical qubits", "under four days" at 1 us cycles. The ~1e10 Toffoli figure is recalled and was not verified from the text.

**Anchor: LNO.** Rubin et al. 2023, Table VI [VERIFIED from PDF text]. DF Toffoli per QPE:

| Structure | Smaller k-mesh | Toffoli | Larger k-mesh | Toffoli |
|---|---|---|---|---|
| R-3m | 2x2x2 | 4.97e12 | 3x3x3 | 7.28e13 |
| C2/m | 2x2x1 | 1.18e12 | 4x4x2 | 9.82e13 |
| P2/c | 1x1x1 | 9.72e11 | 2x2x2 | 1.40e14 |

- Sparse and SF representations cost 1e13-2e16.
- The paper's own verdict: "exorbitantly expensive even at small k-mesh; estimated to run in O(10^2)-O(10^3) days using the DF LCU".

## 3. Kills (explicit)

### K-S1. Multi-center spin-state / protonation energetics deciding a catalytic mechanism
Targets: OEC, nitrogenase, hydrogenase, CODH, P450, Cu2O2.

**Classical frontier.**
- FeMoco: chemical accuracy by CC + DMRG + extrapolation, as a ranking of "largely simple" states (2601.04621, round-1 [V]).
- Fe4S4 CAS(54,36): DMRG at state-of-the-art level, against the IBM/RIKEN Quantum Advantage Tracker entry (2603.28648 [V]).
- Mononuclear spin gaps: CCSD(T) MAE ~1.5 kcal/mol (SSE17, doi:10.1039/d4sc05471g, round-1 [V]).
- AFQMC spin gaps exist for FeP (Lee et al., JCTC 2020, doi:10.1021/acs.jctc.0c00055 [V title]).
- **Scoped negative:** no published case was found in which DMRG-NEVPT2 and AFQMC disagree by >3 kcal/mol for a polynuclear cluster at a converged model (queries 3 and 11-14; OpenAlex was blocked).

**The trilemma applied.**
- The decision quantity is a relative energy of protonation or oxidation isomers, 1-5 kcal/mol.
- That quantity includes dynamic correlation outside any active space, the QM/MM environment and the geometry. Together these give a model floor of ~2-5 kcal/mol.
- Active-space QPE (1e9-1e11 Toffoli per circuit) leaves that floor in place.
- NEVPT2 on top of QPE needs 3- and 4-RDMs, which makes the cost sampling-dominated (L4).
- Full-basis QPE (~1000 orbitals) costs ~5e11 Toffoli per circuit [ESTIMATE: extrapolated from THC scaling]. With 5-10 states and overlap^2 of 0.01-0.1, S*G is 1e14-1e16.

**Verdict: killed.** Either L6 or cost, depending on the branch, and the classical wall is receding.

### K-S2. Exchange couplings that decide an EPR assignment
Targets: Mn4CaO5 S-states, Fe/Mn dimers and tetramers.
- The DMRG precedent exists: Kurashige, Chan, Yanai, Nat. Chem. 2013, doi:10.1038/nchem.1677 [V].
- J depends on ligand-to-metal charge-transfer (dynamic) correlation. Active-space DMRG-CASSCF underestimates superexchange, and DDCI-type treatment is needed [known; not re-verified here].
- Required precision is ~1-10 cm^-1 (5e-6 to 5e-5 Ha).
  - For 100-200 orbitals, lambda/eps is 1e8-1e9, giving 1e12-1e14 Toffoli per circuit.
  - 10-20 spin states are needed.
- Geometry sensitivity is a floor comparable to the method spread (2105.01754, round-1 C33).

**Verdict: killed**, as round-1 C33 was.

### K-S3. Magnetic anisotropy barriers of polynuclear SMMs
- **L5.** The decision quantity (blocking temperature, relaxation time) is set by Raman / spin-phonon processes and QTM, not by Ueff.
- A classical first-principles spin-phonon workflow already matches experiment for an exchange-coupled Co(II) dimer, and predicts that Raman relaxation is suppressed at nuclearity 4 (Mondal, Netz, Hunger, Suhr, Sarkar, van Slageren, Koehn, Lunghi, arXiv:2412.04362 [V abs]).
- Single-ion Ln barriers are handled by CASSCF-SO (round-1 notes: AFQMC-SOC 2303.09010; CASSCF-SO/NEVPT2).
- Strong-exchange f-element dimers remain in round-1 C32 (reserve, polynomial advantage).

**Verdict: killed.**

### K-S4. Doped 2D Hubbard and cuprate/nickelate downfolded models
Question type: stripe vs uniform d-wave, pairing symmetry.
- The pure-model ground state is converging: DMRG and AFQMC agree (Xu et al., Science 384, adh7691 (2024), arXiv:2303.08376, round-1 [V]).
- For bilayer La3Ni2O7, the s <-> d assignment flips with the Hund coupling (2602.20288, round-1 [V]). That is a model floor.
- Tying the question to a material decision needs ab initio multi-orbital supercells, at LNO-scale cost (section 2).

**Verdict: killed** (L6 + cost).

### K-S5. LiNiO2 (LNO) contested ground state (Jahn-Teller vs bond disproportionation)
- **Cost.** Rubin et al. give 1e12-1e14 Toffoli per QPE with 1-2 k-points per direction in GTH-DZVP (Table VI). Their own discussion says the thermodynamic and CBS limits need >= 3x3x3 k-points and QZ basis sets.
- **Model floor.** The JT energy distance is comparable to the zero-point vibrational energies. The dynamic-JT interpretation comes from the paper's ref. [39] (quoted text).
- **L5.** XAS and RIXS evidence already favours bond disproportionation (2011.06441, 2403.18919).
- **Novelty.** Already a published quantum target (category C/D).

**Verdict: killed.**

### K-S6. HCI clock-line prediction at the 5s-4f crossing (Ir17+, Os16+)
- Classical large-scale CI with core excitations is the moving frontier. Cheung et al. (PRL 124, 163001 (2020), arXiv:1912.08714 [V]) give "accurate predictions" and explain the missing E1 lines.
- Rehbehn et al. 2025 (arXiv:2509.06710 [V]): the predicted interconfiguration transitions "were too weak to be detected". The limit is line strength, not the energy prediction.
- A narrow-line laser search needs ~1-10 cm^-1. That is at or below the QED model-operator floor (tens of cm^-1 [ESTIMATE]).

**Verdict: killed** (L6 + L5).

### K-S7. Moire TMD (tMoTe2) FQAH phase diagrams
- The continuum parameters have to be fixed experimentally (Zhang ... Yao, arXiv:2406.20036 [V]). The parameter floor is large.
- A neural-network family that includes band mixing already exists (Luo, Zaklama, Fu, arXiv:2503.13585 [V]).

**Verdict: killed as a separate slot.** Folded into S-M1 as a secondary target only.

### K-S8. nu = 5/2 GaAs topological order (Pf / anti-Pf / PH-Pf)
- The clean-limit multi-family disagreement is real:
  - ED gives Pf for kappa < kappa_c(w) (1411.1068).
  - iDMRG gives anti-Pf (1410.3861).
  - Subband-mixing ED gives anti-Pf (1209.6606).
- But the thermal-Hall result that decides the experiment is attributed to disorder or edge equilibration (1603.03754: PH-Pf "when disorder and LL mixing are strong"). The decision therefore sits in the disorder floor.
- All the candidate orders are Ising-type non-Abelian, so the decision value for topological QC is low.

**Verdict: killed** (L6).

### K-S9. Neutron-star pairing gaps
**1S0 channel: killed (classical).** QMC families agree on a "modest suppression" relative to BCS:
- Gandolfi et al., arXiv:2201.01308 [V];
- AFDMC, 0805.2513;
- lattice DQMC ~30% below BCS, 0708.2523.

**3P2-3F2 channel (Cas A cooling): killed (information not reachable).**
- The multi-family spread is large, but the coherence length xi = hbar v_F / (pi Delta) is the problem. At kF = 2 fm^-1, xi ~ 260 fm for Delta = 0.1 MeV and ~2600 fm for Delta = 0.01 MeV.
- A box of side xi holds 3e6-3e9 neutrons, so the information is not reachable at any feasible size.
- The EFT floor also grows at kF ~ 2 fm^-1.

### K-S10. Warm dense matter, static branch (theta 0.25-0.5)
Observables: static S(q), static chi(q), local field correction, ITCF. This was meant as the cheaper static sibling of C01. It fails the round-1 lesson (i): the wall and the affordable regime do not overlap.

**UEG: no wall.** The static regime at theta = 0.25 is covered from several sides (all from the round-1 audit_C01 notes):
- bracketed by ground-state QMC and theta >= 0.5 PIMC;
- xi-PIMC for static properties at N <= 1000 (2311.08098);
- FT-AFQMC for theta <= 0.5, r_s <= 2 (2012.12228);
- pseudo-fermion PIMC energies down to theta = 0.0625 at N = 33.

**Hydrogen at r_s = 2, theta = 0.25: a wall, but too expensive.**
- PIMC is unavailable there (2507.00688, round-1).
- Cost is scaled from the round-1 C01 table. Static S(q) at 1% with coherent amplitude estimation costs:
  - UEG, eta = 32: ~1e12-5e13 [ESTIMATE: G per shot 4e9-1.6e11, from t_prep 60-100 a.u. times g of 7e7-1.6e9, times ~3e2 coherent repetitions];
  - H, eta = 128: roughly 1e3-1e4x more, i.e. ~1e15-1e18.

**Verdict: killed as a separate candidate.** It is recorded as an input to C01 gate 1: if the ITCF carries the decision information, a quantum computation has to target H at theta < 0.5 and cannot cost less than ~1e15.

### K-S11. Magnetocrystalline anisotropy of permanent magnets
Targets: L10 FeNi, Fe16N2, (Fe,Co)2B.
- K1 is ~0.1-1 meV/atom. DFT-level MAE needs ~1e4-1e5 k-points to converge [known practice, not re-verified].
- A QPE supercell with equivalent Brillouin-zone sampling is far beyond 1e13.

**Verdict: killed** (cost, plus chemical-order and temperature floors).

### K-S12. Low-T thermodynamics of 3D frustrated quantum spin ice
Observables: heat capacity, entropy, thermal expansion, used to discriminate parameter sets. This is round-1 C14/C17 territory.
- Gibbs mixing is unbounded for a U(1) QSL.
- The vacancy floor is ~2%.
- Ce2Sn2O7 orders at ~40 mK.
- At temperatures where Gibbs samplers provably mix fast, high-T Gibbs states tend to be classically easy (round-1 C20).

**Verdict: killed.**

### K-S13. Doped-Hubbard quantum-gas thermometry (cold-atom calibration)
- **L5.** Model-free fluctuation-dissipation thermometry exists [known; not re-verified in this session].
- The analog device is itself the simulator.

**Verdict: killed.**

### K-S14. Uniform / 2D electron gas phase diagram (Stoner transition, Wigner crystal)
- The Hamiltonian is exact, but there is no practical decision.
- The TMD Wigner-crystal experiments carry dielectric and disorder floors.

**Verdict: killed** (F-toy).

### K-S15. Isospin-breaking delta_C in superallowed beta decay (V_ud), and Cs atomic parity violation
Both are static and decision-relevant (CKM unitarity, electroweak tests).
- **delta_C.** It needs overlaps at ~1e-3 relative precision, which means amplitude estimation at ~1e3-1e4 x G, with G ~ 1e10-1e12. So S*G ~ 1e14-1e16. The EFT floor on a small isospin-breaking quantity is comparable [ESTIMATE].
- **Cs APV.**
  - Relativistic CC families disagree at ~0.5% [recalled, UNVERIFIED].
  - The QED correction uncertainty is ~0.1% and the neutron-skin uncertainty ~0.1-0.2% [recalled, UNVERIFIED].
  - The transition matrix element needs amplitude estimation, so S*G >= 1e15.

**Verdict: killed** (cost, borderline L6).

### K-S16. Exoplanet line lists for TM diatomics (TiO, VO, FeH)
- Cross-correlation detection needs line positions to ~0.1 cm^-1. That is far below any ab initio model floor (relativistic, Born-Oppenheimer, QED).
- The practical route is empirical MARVEL energy levels.

**Verdict: killed** (L6).

### K-S17. Noncovalent binding of large polarizable complexes; metal-surface chemisorption
- Both are covered by round-1 W5/W6 and are moving to classical consensus: CCSD(cT), and better DMC nodes giving MAD 0.2-0.4 kcal/mol (doi:10.1063/5.0348824, round-1 [V]).

**Verdict: not reopened.**

## 4. Surviving candidate (conditional)

### S-M1. Multi-band ground-state phase competition in hBN-aligned rhombohedral multilayer graphene at fractional filling
The competition is FCI vs CDW vs anomalous Hall crystal (AHC).

**Problem.**
- **Input:**
  - rhombohedral N-layer graphene continuum model (N = 4-7; SWMcC hoppings);
  - hBN moire potential and alignment angle;
  - displacement field D;
  - dual-gate screened Coulomb interaction (eps_r, d_gate);
  - filling nu in {1/3, 2/3, 3/5, 2/5};
  - normal-ordering reference: CN vs AVE, or explicit remote bands.
- **Compute:** low-lying eigenvalues in every many-body momentum sector of a spin- and valley-polarized momentum-space Hamiltonian with n_b = 3-5 bands, on N_k = 27-48 moire cells.
- **Output:**
  - torus ground-state degeneracy and its momentum quantum numbers;
  - the many-body gap;
  - spectral flow under flux insertion (energies only);
  - FCI vs CDW vs AHC energy differences;
  - a phase map in (D, nu, eps_r, N, alignment), compared with transport data (Lu et al., arXiv:2309.17436: FQAH in pentalayer graphene/hBN).
- **Scaling:** N_k at fixed n_b, and n_b at fixed N_k.
- **Validation rung:** exact agreement with multi-band ED at N_k <= 18, n_b = 2-3.

**Why it sits inside the wall.**
- Yu, Herzog-Arbeitman, Kwan, Regnault, Bernevig (arXiv:2407.13770, PRB 112, 075110 (2025) [V]) found the following:
  - FCIs from single-band ED "become gapless" once band mixing is included.
  - At nu = 2/3 the FCIs "fail to converge".
  - Their conclusion: "current models do not support FCIs with correlation length small enough to be converged in accessible, unbiased ED calculations, or do not support FCIs at all".
  - This conflicts with experiment and with HF, which gives a gapped state.
- Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman (arXiv:2608.12452 [V], Aug 2026) propose the "moire capacitor effect": remote valence charge imprinted on the conduction bands. They confirm it with multi-band ED and present it as the first consistent theory for aligned samples.
- The physics needed is therefore remote-band mixing at sizes beyond ED. Momentum-sector dimensions computed here, against an ED limit of ~1e10-1e11:

  | N_k | n_b | Dimension |
  |---|---|---|
  | 27 | 2 | 3.6e12 |
  | 27 | 3 (N_e = 18) | 1.7e16 |
  | 36 | 3 | 1.8e22 |

- Classical families already disagree with each other (HF vs 1-band ED vs multi-band ED):
  - single-band ED;
  - multi-band ED with occupancy truncation or iteration (Li et al., arXiv:2504.20140 [V]);
  - HF;
  - iDMRG, single-band so far (Wang & Zaletel, arXiv:2507.07921 [V]);
  - NQS with band mixing, for tMoTe2 (Luo, Zaklama, Fu, arXiv:2503.13585 [V]).
- NQS and DMRG are variational and uncertified.
- The decision variables are exactly what the wall blocks: which stack, alignment and D-window host FCIs, and whether FCIs at nu = 3/5 or 2/5 survive band mixing.

**Quantum mechanism.**
- Qubitized QPE with a DF- or THC-factorized, momentum-conserving two-body Hamiltonian. It is chemistry-like, with M = N_k * n_b = 81-180 spinless orbitals.
- QCELS for the low-lying eigenvalue in each momentum sector; the sector is fixed by the initial-state momentum.
- Initial states: 1-band ED or iDMRG states embedded in the multi-band space, or NQS samples.
- Every output is an eigenvalue. There is no linear-response shot noise and no Gibbs state, so lessons L3 and L4 are avoided by construction.

**Rough S*G per state point** [ESTIMATE; lambda has not yet been computed from a real factorization].
- Assumptions: lambda 2e3-3e4 meV; eps 0.05 meV; C_W 1e3-1e4 Toffoli; delta 0.1-1.
- G per circuit: 1e7-2e10.
- 36-72 eigenvalues (sectors x states), with S = 1e2-1e3 each.
- **Result: S*G ~ 5e10-1e15 per state point, central value 1e12-1e13.**
- A full phase map multiplies this by 10-50 parameter points.
- Logical qubits: ~200-1000.

**Model floor vs solver spread (the main risk, L6).**
- In 2407.13770, CN vs AVE changes the outcome at nu = 1/3.
- Argument for passing: the scheme dependence is partly a truncation artifact that shrinks as remote bands are added. Adding bands is exactly what the quantum solver buys, and 2608.12452 puts the missing physics in the remote-band charge.
- The remaining floor must be propagated through the calculation:
  - moire-potential parameters (~30%);
  - eps_r (anisotropic hBN);
  - SWMcC gamma values (~10%);
  - lattice relaxation.

**Other risks.**
- FCI correlation lengths may need N_k >= 50-100, which multiplies cost by 10-100.
- NQS may close the wall classically, in the same pattern as FeMoco and Fe4S4.
- Experiments explore D and nu in situ, so decision value lies only in predictions for stacks not yet fabricated.
- The problem leans toward physics. The practical user is device research on FQAH and non-Abelian platforms.

**Novelty: category B/C** (scoped to query 27, through 2026-09-28).
- The only quantum work found on moire systems:
  - single-particle LDOS via a modified QPE (Bai et al., arXiv:2510.09999);
  - VQE/VQD for FQH manifolds on sphere and torus (Exposito et al., arXiv:2607.11380).
- No fault-tolerant resource study or advantage study of the multi-band moire FCI competition was found.

**Claim category.**
- 3 (computational/resource advantage) against exact multi-band ED, where the Hilbert-space gap is exponential.
- 1 (usefulness / certification) against NQS and iDMRG, unless those are shown to fail at a named state point.

**Gates.** All are cheap and classical; run them in this order.
- **G1 (L6).** At N_k <= 18 and n_b = 2-4, measure how the CN-vs-AVE spread and the parameter-uncertainty spread change as n_b grows. Kill if the floor spread does not shrink below the method spread.
- **G2 (wall).** Run multi-band iDMRG and NQS on the same Hamiltonian at N_k = 27. Kill if they agree with each other and with experiment across the target windows.
- **G3 (cost).** Compute the actual DF/THC lambda and C_W for N_k = 27, n_b = 3. Kill if S*G per state point exceeds 1e13.
- **G4 (decision).** Name at least one unmeasured prediction (e.g. a hexalayer, or a specific alignment angle) where the families disagree.

## 5. Citations

Verified in this session unless marked otherwise.

**Quantum resource and algorithm papers**
- Rubin, Berry, Malone, White, Khattar, DePrince, Sicolo, Kuehn, Kaicher, Lee, Babbush, "Fault-tolerant quantum simulation of materials using Bloch orbitals", PRX Quantum 4, 040303 (2023), arXiv:2302.05531 [V; Table VI read from the PDF].
- Ding & Lin, arXiv:2211.11973, PRX Quantum 4, 020331 (2023) [V abs].
- Lee, Berry, Gidney, Huggins, McClean, Wiebe, Babbush, arXiv:2011.03494, PRX Quantum 2, 030305 (2021) [V abs].
- Legeza, Menczer, Werner et al., arXiv:2603.28648 [V abs listing].

**LNO**
- Green et al., arXiv:2011.06441 [V listing].
- Jacquet et al., arXiv:2403.18919 [V listing].
- Saritas et al., arXiv:1911.01610 (DMC on LiNiO2) [V listing].

**Highly charged ions**
- Cheung, Safronova, Porsev, Kozlov, Tupitsyn, Bondarev, arXiv:1912.08714, PRL 124, 163001 (2020) [V].
- Rehbehn et al., arXiv:2509.06710 [V].
- Berengut et al., PRL 109, 070802 (2012), doi:10.1103/physrevlett.109.070802 [V Crossref].

**Chemistry and molecular magnetism**
- Lee et al., JCTC 2020, doi:10.1021/acs.jctc.0c00055 [V Crossref title].
- Kurashige, Chan, Yanai, Nat. Chem. 2013, doi:10.1038/nchem.1677 [V Crossref].
- Mondal et al. (Lunghi), arXiv:2412.04362 [V].

**Warm dense matter and neutron matter**
- Dornheim et al., arXiv:2403.08570 [V abs].
- Gandolfi, Palkanoglou, Carlson, Gezerlis, Schmidt, arXiv:2201.01308 [V listing].
- Gandolfi et al., arXiv:0805.2513 [V listing].
- Abe & Seki, arXiv:0708.2523 [V listing].

**Moire and flat-band systems**
- Yu, Herzog-Arbeitman, Kwan, Regnault, Bernevig, arXiv:2407.13770, PRB 112, 075110 (2025) [V].
- Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, arXiv:2608.12452 [V].
- Li et al., arXiv:2504.20140 [V listing].
- Wang & Zaletel, arXiv:2507.07921 [V listing].
- Luo, Zaklama, Fu, arXiv:2503.13585 [V listing].
- Zhang et al., arXiv:2406.20036 [V listing].
- Lu et al., arXiv:2309.17436 [V listing].
- Bai et al., arXiv:2510.09999 [V listing].
- Exposito et al., arXiv:2607.11380 [V listing].

**nu = 5/2 quantum Hall** (all [V listing])
- Pakrouski et al., arXiv:1411.1068.
- Zaletel et al., arXiv:1410.3861.
- Papic, Haldane, Rezayi, arXiv:1209.6606.
- Zucker & Feldman, arXiv:1603.03754.

**Reused from round 1** (verified there): 2601.04621, doi:10.1039/d4sc05471g, 2303.08376, 2602.20288, 2507.00688, 2311.08098, 2012.12228, 2105.01754, doi:10.1063/5.0348824.

**[UNVERIFIED / recalled]**
- FeMoco THC Toffoli count (~1e10).
- Cs APV method spread, and the QED and neutron-skin floors.
- The MAE k-point requirement.
- FDT thermometry references.
- tMoTe2 continuum-parameter discrepancy literature beyond 2406.20036.
