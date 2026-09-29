# Discovery lens: resource estimates and break-even (2026-09-28)

Status: COMPLETE for this pass (about 45 tool calls). Lens owner: resource-estimate / break-even subagent.
Scope: fault-tolerant (FT) and early-FT resource estimates, 2021 to 2026-09-28, for physical-application tasks; break-even reasoning; candidates where an original quantum-vs-strongest-classical study is possible.

Tooling caveat (read before trusting any "not found"): WebSearch budget was exhausted before this lens started (200/200). The arXiv export API and OpenAlex returned HTTP 429. Searches therefore used arxiv.org/search listing pages (abstract field, via WebFetch), arXiv abs/html pages, and the Crossref REST API. arXiv listing search is keyword-literal and misses paraphrases, and Crossref keyword ranking is noisy. Every "no quantum paper found" below is scoped to these sources and queries only.

---

## 1. Break-even framework used in this lens

### 1.1 What the frameworks say (verified abstracts)
- Babbush, McClean, Newman, Gidney, Boixo, Neven, "Focus beyond quadratic speedups for error-corrected quantum advantage", PRX Quantum 2, 010103 (2021), arXiv:2011.04149 [VERIFIED]. Quadratic speedups do not give advantage on early surface-code machines, even with an order-of-magnitude faster logical gates. Quartic speedups look far more practical.
- Hoefler, Haener, Troyer, "Disentangling hype from practicality", CACM 66(5) (2023), doi:10.1145/3571725, arXiv:2307.00523 [VERIFIED]. Only small-data problems with super-quadratic speedups are practical. Chemistry and materials are singled out as the promising area.
- Beverland et al., "Assessing requirements to scale to practical quantum advantage", arXiv:2211.07629 [VERIFIED]. Practical advantage needs 1e5 to 1e6+ physical qubits, and gate speed is a first-class parameter.
- Hardware-rate anchors: Lee et al. (THC FeMoco), PRX Quantum 2, 030305 (2021), arXiv:2011.03494 [VERIFIED]: about 4e6 physical qubits and under 4 days at 1 us cycles and 1e-3 error. Gidney, arXiv:2505.15917 [VERIFIED]: RSA-2048 with fewer than 1e6 noisy qubits in under a week at 1 us cycles and 1e-3 error. The implied effective Toffoli rate on a single-factory early-FT surface-code machine is about 1e4 to 1e5 Toffoli/s. [This rate is my inference from these papers; the exact Toffoli totals are UNVERIFIED in this session.]

### 1.2 The operational break-even rule applied to every candidate (my derivation)
Let G be Toffolis per circuit, S the number of circuit repetitions needed for the observable (shots, time points, initial-state samples), r_T the Toffoli rate, and T_wall the tolerable wall time.
- Feasibility: S * G <= r_T * T_wall. With r_T = 1e5/s and T_wall = 1e7 s (about 4 months), S * G <= 1e12. For a dynamical observable at 3-5% precision, S is about 1e3, so an early-FT study needs G <= ~1e9 per circuit. With r_T = 1e6/s (many factories, a later generation) the bound is G <= ~1e10.
- Speedup type:
  - (a) If the strongest classical competitor is itself Monte Carlo with 1/eps^2 cost (PIC, stochastic trace/KPM, path-integral sampling without a sign problem), the quantum gain is at most quadratic in 1/eps. By Babbush 2021 that gain is dead on early FT.
  - (b) If the classical competitor has controlled error at polynomial cost (DMRG in quasi-1D, CCSD(T) for single-reference systems, ML-MCTDH for weakly correlated modes, free-fermion-bath impurity solvers), there is no advantage whatever G is.
  - (c) Only exponential classical cost for the controlled-error answer, together with an uncontrolled-error cheap classical method that demonstrably disagrees with other methods by more than the experimental error, gives a real target. In that case the advantage category is 3 (computational/resource) or 1 (usefulness), never "speed vs the cheap approximate method".
- Model floor (protein lesson 6): the solver error of the best classical method must exceed the model error (Hamiltonian parameters, environment, finite size). This is why zero-model-floor Hamiltonians (bare Coulomb: warm dense matter, electron-hole plasmas, atoms) are preferred in this lens.
- State-preparation caveat: many dynamics estimates quote only time-evolution cost. Finite-T observables also need Gibbs/thermal-ensemble preparation, which is often omitted and can dominate. Candidates whose physical initial state is a product/Slater state (quench, pump-probe, scattering) avoid this.

---

## 2. Resource-estimate register (2021-2026), with a strongest-classical flag

"SC?" asks whether the paper benchmarked against the strongest classical method for the same observable. Y = yes, P = partial (a classical reference or one method), N = no.

| Task (paper) | Logical qubits | Toffoli / T | Runtime / physical | SC? | Notes |
|---|---|---|---|---|---|
| FeMoco ground-state QPE, THC (Lee et al. 2021, arXiv:2011.03494) | ~2e3 (UNVERIFIED) | ~4e9 Toffoli (UNVERIFIED) | <4 days, ~4e6 physical, 1 us cycle | P | FeMoco now near-classically solved (arXiv:2601.04621, from task context). Classical overtook the target. |
| Cytochrome P450 (Goings et al. PNAS 2022, arXiv:2202.01244) | not in abstract | not in abstract | not in abstract | Y (DMRG+NEVPT2, CCSD(T)) | One of the few estimates paired with a strong classical study. |
| Materials via Bloch orbitals (Rubin et al. PRX Quantum 4, 040303, 2023, doi:10.1103/PRXQuantum.4.040303) | not extracted | reported as far above molecular cases (UNVERIFIED magnitude) | - | P | Periodic materials cost more than molecules. |
| Exact electron dynamics vs mean field (Babbush et al. Nat Commun 2023, doi:10.1038/s41467-023-39024-0) | - | asymptotic | - | theoretical | First-quantized exact dynamics can cost less than classical mean-field (TDHF/TDDFT) scaling. Basis for super-polynomial accuracy-class arguments. |
| Stopping power in WDM (Rubin et al. PNAS 2024, doi:10.1073/pnas.2317772121, arXiv:2308.12352) | "roughly same as FeMoco/P450" | "about 100x more Toffoli" than those, so ~1e11-1e12 by my extrapolation | - | P (TDDFT context) | Claimed application. Fails the early-FT rule (G >> 1e9). |
| Pre-BO photochemistry, end-to-end (Eklund, ..., Berry, Kassal, arXiv:2603.19007, 2026) | 3000-8000 | 1e13-1e16 Toffoli (quantum yield, eps = 0.095) | - | N (MCTDH only mentioned qualitatively) | S*G ~ 1e15-1e18: infeasible even at r_T = 1e6/s. |
| Cathode XAS, Li4Mn2O cluster (Fomichev et al. arXiv:2506.15784, 2025) | 100 | < 4e8 T per circuit | - | P (reconstructs a classical reference) | (22e, 18o) active space is classically tractable (CASCI/DMRG). Cheap because the instance is small. |
| Generalized Anderson-Newns metal-surface dynamics (Lang, Jain, Arrazola, Motlagh arXiv:2601.16264, 2026) | 271 | 7.9e7 Toffoli (1000 Trotter steps) | - | N | Free-fermion metal bath plus few interacting orbitals: an impurity problem. ML-MCTDH-SQR, HEOM and TN impurity solvers are the untested classical adversaries. |
| Nuclear dynamics, first quantization, LO pionless EFT (Spagnoli, Lissoni, Roggero, Quantum 10, 2200 (2026), arXiv:2507.22814) | "few hundred" | "tens of millions of T" for low-energy nuclear scattering | - | N | Cheapest physical estimate found. The regime (few-nucleon LO pionless scattering) is classically exact (Faddeev-Yakubovsky, NCSMC, lattice EFT), and the LO pionless model floor is large. |
| Nuclear EFTs, pionless/pionful (Watson, ..., Childs, Gorshkov, Davoudi, arXiv:2312.05344, rev. 2026) | not in abstract | "several orders of magnitude" below earlier estimates | - | N | Numbers not extracted. |
| LGT with gauge-covariant codes (Spagnoli, Roggero, Wiebe, Quantum 2026, doi:10.22331/q-2026-01-16-1968) | - | - | - | N | Not practical-observable driven. |
| Fermi-Hubbard + cuprate/pnictide models (Kan & Symons, npj QI 2025, doi:10.1038/s41534-025-01091-0, arXiv:2411.02160) | "far lower than chemistry QPE" | realistic superconductor models about 10x Hubbard | - | N (classical difficulty asserted) | Cheapest classically-hard-asserted instances, but a lattice-model observable. The classical frontier (AFQMC, DMRG, fPEPS, NQS) is strong. |
| Generalized Hubbard (Bay-Smidt, Klausen, Suenderhauf, Izsak, PRX Quantum 2025, doi:10.1103/gr4t-b1w5) | - | - | - | N | Same class. |
| 2D condensed-matter crossover (Yoshioka et al., arXiv:2210.14109) | - | - | hours with ~1e5 physical qubits (claimed) | Y (DMRG/TN extrapolated) | The one explicit crossover study. Ground-state energies of 2D spin/Hubbard models. |
| Spin-chain dynamics circuits (Childs et al. PNAS 115, 9456 (2018), arXiv:1711.10980) | ~50-100 | far below chemistry/factoring | - | N | 1D Heisenberg is TN/Pauli-propagation friendly at relevant times. |
| Vibrational/vibronic block encodings (Kamakari & Zak, arXiv:2504.08065, 2025) | not in abstract | reduced via CP/Tucker | - | N | H2O, CH3D: classically exact. |
| Lindbladian Gibbs-state prep (Bobrow et al., Sandia, APS 2025, doi:10.2172/3023927) | not available | not available | - | - | Gibbs-prep costs are beginning to be estimated. Most dynamics estimates omit them. |
| Diarylethene excited states, photonic FT (Kanno et al., ACS Omega 2025, doi:10.1021/acsomega.4c09568) | not extracted | not extracted | - | N | Crossref hit only; not read. |

Structural finding of this lens (the cost-hardness anti-correlation). Every estimate found below about 1e9 Toffoli per circuit falls in one of two groups:
1. Instances small or structured enough that a controlled classical method already solves them: XAS at 18 orbitals, LO-pionless few-nucleon scattering, CH3D vibrations, spin chains, and plausibly the Anderson-Newns impurity model.
2. Lattice-model observables whose practical relevance runs through an uncertain model: Hubbard and cuprate models.

The practical, classically unverified tasks cost 1e11 to 1e16 Toffoli per circuit: stopping power, pre-BO photochemistry, and periodic materials. None of the low-cost papers audited classical hardness against the strongest method, with P450 and Yoshioka as partial exceptions. An original study therefore has two possible shapes:
- (i) take a cheap published algorithm and locate the true classical-hardness crossover, a scaling study; or
- (ii) find zero-model-floor observables whose physical initial state is cheap to prepare, so G stays near 1e9 while the controlled-error classical cost is exponential.

---

## 3. Candidates

### C1. Electron-electron-scattering contribution to the DC/AC electrical conductivity and Lorenz number of warm dense light elements (H, Be, CH) at theta = T/T_F ~ 0.5-2
- **Domain:** high-energy-density physics / ICF and planetary-interior transport.
- **Input:** element/composition, mass density (r_s ~ 1-3), T_e, T_i. Classical ion configurations (snapshots from DFT-MD or ML potential) are held fixed or treated in a BO/Ehrenfest split.
- **Output:** sigma(omega), sigma_DC, thermal conductivity kappa and Lorenz number L = kappa/(sigma T), with controlled finite-size error. Measurables: XRTS-inferred and THz/optical conductivities, and conductivity tables used in hydrocodes.
- **Why practical:** conductivity tables drive hot-spot conduction losses and MagLIF electrothermal instabilities. Code-comparison workshops found large inter-method variation at strong coupling (Grabowski et al. HEDP 2020, doi:10.1016/j.hedp.2020.100905 [VERIFIED]; Haines, Phys. Plasmas 2024, doi:10.1063/5.0197128 [VERIFIED title]). Robinson, Kononov, Stanek, Baczewski, Schleife, Hansen (arXiv:2605.11308, 2026 [VERIFIED]) state that "state-of-the-art conductivity calculations based on DFT ... neglect electron-electron scattering lifetimes". Their GW approach gives "a surprisingly large reduction in low-temperature DC conductivity" for Be. The classical frontier is therefore moving, and different approximations disagree.
- **Quantum mechanism:** first-quantized plane-wave electrons (Su et al. PRX Quantum 2021, doi:10.1103/PRXQuantum.2.040332 [VERIFIED]; Babbush et al. Nat Commun 2023), with qubitized/Trotter evolution under the full Coulomb Hamiltonian and fixed classical ions. Current-current correlation via a Hadamard test, or a weak-field linear-response quench measuring induced current (avoids the ancilla-controlled evolution). This replaces KS-DFT Kubo-Greenwood (mean field, no e-e lifetime) and GW self-energies (perturbative) with exact many-electron dynamics. The speedup is exponential against exact classical dynamics, and comparable-cost scaling against mean-field (Babbush 2023). It is an accuracy-class advantage, category 3 or 1.
- **Classical SOTA / red team:** KS-DFT-MD + Kubo-Greenwood; GW-conductivity (Robinson 2026); mean-force kinetic theory with e-e (Babati, Shaffer, Jose, Baalrud arXiv:2606.02881 and 2606.02890, 2026 [VERIFIED listing/abs]); real-time TDDFT; average-atom (Wetta & Pain arXiv:2503.13014 [VERIFIED listing]); PIMC imaginary-time current correlators with analytic continuation (Efremkin, Mossa, Barrat, Holzmann arXiv:2602.16405 [VERIFIED listing], nonperturbative thermal conductivity from PIMC; Dornheim ITCF work). PIMC is the strongest attack but hits the sign problem at theta < ~1.
- **Why classically hard:** real-time, finite-T, many-electron dynamics at theta ~ 1. PIMC loses to the fermion sign problem, and analytic continuation of PIMC data is ill-posed for the DC limit. DFT lacks e-e lifetimes, and GW/kinetic theories are uncontrolled at intermediate coupling. The hardness is an argument, not a demonstration: no study has shown the methods fail to converge to experiment at a specific (rho, T).
- **Novelty:** B. In arXiv abstract search "quantum computer warm dense matter" (27 hits), "quantum algorithm conductivity Kubo linear response" (0) and "quantum computer transport coefficients conductivity" (44 hits), and in Baczewski's arXiv author listing, I found quantum algorithms for WDM stopping power (Rubin 2024, claimed) and exact-dynamics theory (Babbush 2023), and quantum XRTS proposals are covered by another lens. I found no quantum-computing study of WDM electrical/thermal conductivity or the Lorenz number versus KS-KG, GW, kinetic or PIMC methods. The Sandia group that published arXiv:2605.11308 also works on quantum algorithms, so that closest competitor may move soon.
- **Break-even (my estimate):** by analogy with the stopping-power estimate (same logical-qubit class as FeMoco, about 100x Toffoli), G ~ 1e10-1e12 per circuit for eta ~ 100-250 electrons. S >= 1e2-1e3 (ion snapshots x initial-state samples x field strengths). This FAILS the early-FT rule; it needs r_T ~ 1e6-1e7/s. Thermal-ensemble preparation is an added cost. The mitigation is thermal-typicality or KS-determinant sampling, which is ensemble-sampling of pure states; its validity must be checked.
- **Main failure risk:** GW + kinetic theory converge to one another and to experiment (the classical gap closes). Beyond that, the G*S cost pushes any hardware test to later-generation FT, so a near-term study is an emulation plus resource-crossover study only. Finite-size errors (eta <= 250) could swamp the e-e correction.
- **Verdict:** plausible (long horizon). This is the strongest zero-model-floor, super-polynomial candidate in this lens.

### C2. Photoexcited dense electron-hole plasma in 2D semiconductors (TMD monolayers/bilayers): time-resolved optical/THz response through the exciton Mott crossover, from a product initial state
- **Domain:** ultrafast semiconductor optics; optoelectronic devices at high excitation (gain, bandgap renormalization, photodetector saturation).
- **Input:** effective masses, the dielectric environment via a Rytova-Keldysh screened interaction (r0, eps_substrate), and the pump-created e/h distribution (density n ~ 1e11-1e13 cm^-2, excess energy).
- **Output:** time-resolved absorption / optical gain spectrum and THz conductivity over 0-500 fs. Also the time-dependent exciton fraction and the Mott density n_M(t, T_eff). Directly comparable to pump-probe data (Chernikov et al. Nat Photon 2015, doi:10.1038/nphoton.2015.104 [VERIFIED]; Mohapatra et al. arXiv:2601.17167 and Dogadov et al. arXiv:2604.06897, 2026 [VERIFIED listing]).
- **Quantum mechanism:** first-quantized two-component (electrons and holes, similar masses) 2D plane-wave simulation of the bare screened-Coulomb Hamiltonian. The initial state is the product of e and h Slater determinants given by the pump, so Gibbs preparation is not needed. Evolution uses qubitization or Trotter, and the readout is dipole/current correlation or measured momentum occupations. This replaces NEGF with approximate self-energies (GW, T-matrix, G1-G2 scheme), which are uncontrolled at the Mott crossover where bound and unbound pairs coexist at comparable energy scales. The advantage is exponential against exact dynamics and an accuracy class against NEGF.
- **Classical SOTA / red team:** semiconductor Bloch equations with screened HF and correlation; excitonic Heisenberg equations (Mittenzwey et al. arXiv:2512.03198 [VERIFIED listing]); NEGF in the G1-G2 scheme with GW/T-matrix (Schluenzen, Joost, Bonitz PRL 2020, doi:10.1103/PhysRevLett.124.076601 [VERIFIED]); GW-BSE statics (Steinhoff et al. Nat Commun 2017, doi:10.1038/s41467-017-01298-6 [VERIFIED]); DMC/PIMC for equilibrium e-h liquid energetics; exact diagonalization on small clusters. TN methods for 2D continuum Coulomb systems are weak.
- **Why classically hard:** a two-component degenerate Coulomb system with mass ratio ~1 at T ~ E_binding. PIMC has a severe sign problem and no real time, and NEGF approximations are not controlled at the crossover.
- **Novelty:** A (scoped). arXiv abstract search "electron-hole plasma quantum computer simulation" gave 2 hits, neither a quantum-computing paper. "exciton Mott transition monolayer" gave 24 hits, all classical theory or experiment. Crossref queries found no quantum-algorithm paper.
- **Break-even (my estimate, UNVERIFIED order of magnitude):** eta = 32 e + 32 h on a 32x32 grid gives about 640 system qubits and about 1e3 logical qubits with ancillas. G ~ 1e8-1e10 per circuit for about 200 fs, with S ~ 1e3. This sits at or just above the early-FT feasibility boundary, the best cost profile of the zero-floor candidates here.
- **Main failure risk:** model floor. Dielectric screening by the substrate, phonon coupling and disorder shift n_M by amounts that may exceed the solver disagreement (the listing summaries note strong substrate dependence). Also, eta = 64 may be too small for a 2D Mott crossover without large finite-size effects.
- **Verdict:** plausible-weak. A good benchmarkable scaling variable is eta and density at fixed r0, with G1-G2 NEGF as the tuned classical twin.

### C3. Classical-hardness crossover for published low-cost quantum dynamics/spectroscopy algorithms: generalized Anderson-Newns (7.9e7 Toffoli) and cathode/cluster L-edge XAS (4e8 T)
- **Domain:** interfacial nonadiabatic dynamics (molecule-metal charge transfer, vibrational relaxation) and core-level spectroscopy of transition-metal clusters.
- **Input:** Anderson-Newns: 100 metal orbitals, 8 molecular orbitals and 20 nuclear DOF with parameters from DFT (Lang et al. 2026). XAS: an active space of N_orb orbitals for multinuclear Mn/Fe/Co oxide clusters, scaled from 18 to about 80 orbitals.
- **Output:** a crossover curve showing, per scaling variable (N_orb, number of bath orbitals, simulated time), the Toffoli cost of the quantum algorithm against the cost of the strongest classical method at equal controlled error. The physical outputs are vibrational relaxation probabilities or electron-transfer rates, and L-edge spectra.
- **Quantum mechanism:** Trotterized fermion-boson evolution (Anderson-Newns) and QPE-sampled spectral functions with compressed double factorization (XAS). These are the published algorithms; the original contribution is the adversarial classical side.
- **Classical SOTA / red team:** ML-MCTDH in second quantization (Wang-Thoss type) for a free-fermion bath with vibrations; HEOM for Anderson-Holstein; TN impurity solvers with bath discretization; electronic friction and IESH as cheap baselines. For XAS: DMRG correction-vector / TD-DMRG spectra, RAS-CI/RASPT2, SHCI, and multiplet ligand-field theory.
- **Why classically hard (unverified):** neither quantum paper benchmarked against these methods (see the section 2 table). The Anderson-Newns bath is non-interacting, which strongly suggests classical tractability. XAS at 18 orbitals is exactly tractable.
- **Novelty:** C. Quantum algorithms and resource estimates exist; in the sources searched, no quantum-vs-strongest-classical crossover study exists for these tasks. Overlaps: the claims lens covers these as claimed applications, and the chemistry lens (C3) covers multinuclear-cluster XAS physics. This candidate is the break-even audit itself.
- **Break-even:** both algorithms pass the early-FT rule (G ~ 1e8, S ~ 1e3, so S*G ~ 1e11). The open question is whether classical cost stays polynomial at the sizes where the physics becomes relevant.
- **Main failure risk:** the likely outcome is a clean negative, with classical methods matching at all practical sizes (an impurity bath is classically compressible). That is publishable as a hardness audit but is not an advantage demonstration. The model floor (DFT-derived coupling parameters) also limits decision value.
- **Verdict:** plausible as an original study (likely negative, category 3 test), weak as an advantage route.

### C4. Accuracy-class break-even for 2D Fermi-Hubbard-type early-FT dynamics with cuprate/pnictide parameters (included for completeness; overlaps the materials lens)
- **Input:** a three-band / t-t'-U model with ab initio parameters on an L x L lattice, and a quench or weak-probe protocol.
- **Output:** the dynamic spin/charge response or optical conductivity at intermediate T.
- **Quantum mechanism:** Trotter/qubitization with the Kan & Symons compilation (npj QI 2025) and the Bay-Smidt et al. (PRX Quantum 2025) block encodings. These are the lowest-cost "classically difficult" estimates in the register.
- **Classical SOTA:** DQMC plus MaxEnt, FTLM, METTS/DMRG on cylinders, NLCE, NQS, AFQMC, fPEPS, Pauli propagation, and belief-propagation TN (for dynamics).
- **Novelty:** D/E for Hubbard dynamics generally. A subsection with ab initio multi-band parameters and a specific response observable is C. The overlap with the materials lens (C4 RIXS/S(q,w)) is large, so this is not proposed as a separate lead.
- **Verdict:** weak. The practical link to cuprates runs through a model with an uncertain floor, and the classical frontier is the strongest of any candidate.

---

## 4. Killed ideas (with break-even reasons)
1. **Pre-BO end-to-end photochemistry quantum yields (arXiv:2603.19007):** 3000-8000 logical qubits and 1e13-1e16 Toffoli per circuit, with S ~ 1e2 for eps ~ 0.1. That is decades even at r_T = 1e6/s. Classical surface hopping / ML-MCTDH on ab initio surfaces is the relevant competitor, and the authors did not benchmark against it. Killed on break-even.
2. **Linear/nonlinear Vlasov, linear Boltzmann, radiation transport via QLSA/Carleman:** the strongest classical competitor for scalar outputs is particle Monte Carlo (PIC) with 1/eps^2 cost. Quantum amplitude estimation gives at most a quadratic gain in 1/eps (Babbush 2021 kill), plus readout limits and nonlinearity (Hoefler 2023 small-data rule). The complexity lens has a matching kill (roadmap arXiv:2605.07722).
3. **Low-energy few-nucleon scattering (arXiv:2507.22814, tens of millions of T):** the cheapest estimate found, but the regime is classically exact (Faddeev-Yakubovsky, NCSMC, lattice EFT), and LO pionless EFT has a model floor far above solver error. Extending to A = 11-16 radiative capture (12C(alpha,gamma), p+11B) needs keV-level resonance placement that chiral EFT cannot provide (consistent with the algorithms-lens kill).
4. **Small-active-space XAS (arXiv:2506.15784 at 18 orbitals):** cheap (4e8 T) only because it is classically exact. Kept only as a crossover study (C3).
5. **Organic-semiconductor carrier mobility (Holstein-Peierls, 2D) via quantum dynamics:** a first-principles HMC/QMC study (Ostmeyer, Nematiaram, Troisi, Buividovich, Phys. Rev. Applied 22, L031004 (2024), arXiv:2312.14914 [VERIFIED]) reports mobilities "in good agreement with experiment" that "justify" transient-localization theory. The classical methods agree with each other and with experiment, so the hardness is not verified. Model floor (transfer integrals ±10-20%, mobility ∝ J^2) is comparable to any residual solver gap.
6. **TADF reverse-intersystem-crossing rates (spin-vibronic):** k_RISC ∝ exp(-dE_ST/kT) with dE_ST errors of about 0.1 eV from excited-state electronic structure gives factors of ~50. Model floor dominates (lesson 6).
7. **eEDM effective fields / molecular enhancement factors (ThO, HfF+, RaF):** relativistic CC already reaches a few percent, and bounds are interpreted at order-of-magnitude level. Decision-insensitive (lesson 5).
8. **Polyatomic tunneling rate constants and CH5+/protonated-cluster vibrational spectra on grids:** already killed by the algorithms lens (PES floor). This lens adds that coherent PES-oracle cost (NN/PIP arithmetic, protein lesson 3's G(L)) multiplies every Trotter step. ML-MCTDH keeps controlled error at polynomial cost for most 12-21D reactions of interest, so class (b) applies.
9. **Real-time LGT / QCD observables:** costs are orders above chemistry, and the observables are not practical-decision outputs.
10. **Collective neutrino flavor many-body dynamics:** the Hamiltonian is a drastic reduction (single-angle, few momentum modes). An exact solution of that model is lesson 6 (wrong-model) territory.
11. **Anharmonic lattice thermal conductivity with nuclear quantum effects:** classical PIMC nonperturbative kappa (arXiv:2602.16405) plus SSCHA/TDEP-BTE covers the cases of practical interest (room T). The MLIP floor is ~10-30% of kappa.
12. **Warm-dense electron-ion temperature relaxation (G(T_e)):** a sibling of C1, but it needs coupled quantum electrons and ions (pre-BO class, G >= 1e12). Folded into C1 as a later extension.

---

## 5. Query log (chronological)
1. WebSearch "fault-tolerant resource estimate Toffoli count quantum dynamics 2025 arXiv logical qubits" -> budget exhausted (200/200)
2. arXiv API abs:"resource estimates" AND abs:Toffoli AND abs:dynamics -> HTTP 429 x3
3. OpenAlex "fault-tolerant resource estimates Toffoli quantum simulation dynamics" (2021+) -> one partial page, then 429
4. Crossref "fault-tolerant quantum resource estimates simulation Toffoli" (2021+) -> Kan & Symons 2025; Bay-Smidt 2025; Bobrow 2025; Kanno 2025
5. Crossref: "quantum algorithm chemical reaction rate constant flux correlation first quantization resource"; "quantum computing vibrational spectra anharmonic resource estimates fault-tolerant"; "quantum simulation nuclear effective field theory resource estimates"; "quantum algorithm plasma kinetic Vlasov resource estimate"; "quantum simulation grid-based nuclear dynamics molecules first quantization potential energy surface oracle"
6. arXiv API abs:"reaction rate" AND "quantum computer" AND "first quantization" -> 429
7. arxiv.org/search (all) "quantum computer thermal rate constant flux correlation" -> 0
8. arxiv.org/search (abstract) "quantum algorithm reaction rate constant" -> 5 hits (Mazzola 2108.11410 only quantum)
9. arxiv.org/search (abstract) "first quantization" quantum dynamics molecules grid quantum computer -> 2603.19007
10. arXiv abs + html 2603.19007
11. Crossref DOI batch verification (10 DOIs)
12. arxiv.org/search (title) "Hunting for quantum-classical crossover condensed matter" -> 2210.14109
13. arxiv.org/search (title) "Resource-optimized fault-tolerant simulation of the Fermi-Hubbard model" -> 2411.02160
14. arXiv abs 2011.04149; 2307.00523; 2308.12352
15. arxiv.org/search (abstract) "quantum computer warm dense matter" -> 27 hits
16. arXiv abs 2606.02881
17. arxiv.org/search (abstract) "quantum algorithm conductivity Kubo linear response" -> 0
18. arxiv.org/search (abstract) "quantum computer transport coefficients conductivity" -> 44 hits (none quantum-computing WDM/OSC transport)
19. Crossref "charged-particle transport coefficient code comparison workshop review"; "density functional transport nondegenerate limit role of electron-electron scattering"; "electron-hole plasma exciton Mott transition transition metal dichalcogenide ultrafast"
20. arXiv abs 2504.08065; 2312.05344; 2506.15784
21. arxiv.org/search (abstract) "quantum computer Holstein polaron electron-phonon simulation" -> 5 hits
22. arxiv.org/search (abstract) "quantum algorithm charge transport organic semiconductor mobility" -> 1 hit (2312.14914)
23. arxiv.org/search (abstract) "electron-phonon fault-tolerant quantum simulation resource" -> 2606.16017
24. arxiv.org/search (abstract) "quantum simulation electron-phonon bosons qubits phonon truncation" -> 0
25. arXiv abs 2312.14914
26. arxiv.org/search (abstract) "electron-hole plasma quantum computer simulation" -> 2 hits (neither quantum computing)
27. OSTI 3023927 (Bobrow et al.; no abstract available)
28. arxiv.org/search (all) "Spagnoli Roggero nuclear dynamics first quantization" -> 2507.22814
29. arxiv.org/search (abstract) "transport coefficient comparison workshop" -> 2503.13014, 2007.00744
30. arXiv author listing baczewski_a_1 -> 2605.11308, 2602.22540, 2507.20387, 2301.01203
31. arXiv abs 2605.11308; 2602.22540
32. arXiv abs 2011.03494; 2202.01244; 2211.07629; 2505.15917
33. Crossref DOI verification (Schluenzen PRL 2020; Steinhoff 2017; Grabowski HEDP 2020; Chernikov 2015)
34. arxiv.org/search (abstract) "exciton Mott transition monolayer" -> 24 hits (all classical)
35. arXiv abs 1711.10980; 2601.16264

## 6. Citation list (verification status)
- Babbush et al., PRX Quantum 2, 010103 (2021), doi:10.1103/PRXQuantum.2.010103, arXiv:2011.04149 [VERIFIED]
- Hoefler, Haener, Troyer, CACM (2023), doi:10.1145/3571725, arXiv:2307.00523 [VERIFIED]
- Beverland et al., arXiv:2211.07629 [VERIFIED]
- Lee et al., PRX Quantum 2, 030305 (2021), arXiv:2011.03494 [VERIFIED]
- Gidney, arXiv:2505.15917 [VERIFIED]
- Goings et al., arXiv:2202.01244 (PNAS 2022) [VERIFIED arXiv]
- Rubin, Berry, Malone, White et al., PRX Quantum 4, 040303 (2023) [VERIFIED]
- Babbush, Huggins, Berry et al., Nat Commun (2023), doi:10.1038/s41467-023-39024-0, arXiv:2301.01203 [VERIFIED]
- Rubin, Berry, Kononov, Malone et al., PNAS 121 (2024), doi:10.1073/pnas.2317772121, arXiv:2308.12352 [VERIFIED]
- Su, Berry, Wiebe, Rubin, Babbush, PRX Quantum 2, 040332 (2021), doi:10.1103/PRXQuantum.2.040332 [VERIFIED via OpenAlex record]
- Eklund, Tikku, Sinnott, Huggins, Low, Berry, Kassal, arXiv:2603.19007 (2026) [VERIFIED]
- Fomichev et al., arXiv:2506.15784 (2025) [VERIFIED]
- Lang, Jain, Arrazola, Motlagh, arXiv:2601.16264 (2026) [VERIFIED]
- Spagnoli, Lissoni, Roggero, Quantum 10, 2200 (2026), doi:10.22331/q-2026-09-02-2200, arXiv:2507.22814 [VERIFIED]
- Watson et al., arXiv:2312.05344 [VERIFIED]
- Spagnoli, Roggero, Wiebe, Quantum (2026), doi:10.22331/q-2026-01-16-1968 [VERIFIED Crossref]
- Kan & Symons, npj QI (2025), doi:10.1038/s41534-025-01091-0, arXiv:2411.02160 [VERIFIED]
- Bay-Smidt, Klausen, Suenderhauf, Izsak, PRX Quantum (2025), doi:10.1103/gr4t-b1w5 [VERIFIED Crossref]
- Yoshioka, Okubo, Suzuki, Koizumi, Mizukami, arXiv:2210.14109 [VERIFIED listing]
- Childs, Maslov, Nam, Ross, Su, PNAS 115, 9456 (2018), arXiv:1711.10980 [VERIFIED]
- Kamakari & Zak, arXiv:2504.08065 [VERIFIED]
- Bobrow et al., OSTI doi:10.2172/3023927 (2025) [VERIFIED metadata only]
- Kanno et al., ACS Omega (2025), doi:10.1021/acsomega.4c09568 [VERIFIED Crossref metadata only]
- Robinson, Kononov, Stanek, Baczewski, Schleife, Hansen, arXiv:2605.11308 (2026) [VERIFIED]
- Babati, Shaffer, Jose, Baalrud, arXiv:2606.02881 and arXiv:2606.02890 (2026) [VERIFIED abs / listing]
- Wetta & Pain, arXiv:2503.13014 [VERIFIED listing]
- Grabowski et al., HEDP 37, 100905 (2020), doi:10.1016/j.hedp.2020.100905, arXiv:2007.00744 [VERIFIED]
- Haines, Phys. Plasmas (2024), doi:10.1063/5.0197128 [VERIFIED Crossref metadata]
- Desjarlais, Scullard, Benedict et al., PRE 95, 033203 (2017), doi:10.1103/PhysRevE.95.033203 [VERIFIED]
- Efremkin, Mossa, Barrat, Holzmann, arXiv:2602.16405 [VERIFIED listing]
- Proctor, Blume-Kohout, Baczewski, arXiv:2602.22540 (2026) [VERIFIED]
- Chernikov et al., Nat Photon (2015), doi:10.1038/nphoton.2015.104 [VERIFIED]
- Steinhoff et al., Nat Commun 8, 1166 (2017), doi:10.1038/s41467-017-01298-6 [VERIFIED]
- Schluenzen, Joost, Bonitz, PRL 124, 076601 (2020), doi:10.1103/PhysRevLett.124.076601 [VERIFIED]
- Mittenzwey et al. arXiv:2512.03198; Mohapatra et al. arXiv:2601.17167; Dogadov et al. arXiv:2604.06897 [VERIFIED listing only]
- Ostmeyer, Nematiaram, Troisi, Buividovich, Phys. Rev. Applied 22, L031004 (2024), arXiv:2312.14914 [VERIFIED]
- Mazzola, arXiv:2108.11410 [VERIFIED listing]
- Dorfner, Brey, Burghardt, Ortmann, JCTC (2024), doi:10.1021/acs.jctc.4c00751 [VERIFIED]
- FeMoco near-classical solution arXiv:2601.04621 [from task context; not re-verified in this lens]
- Numbers marked "my estimate" or "UNVERIFIED" are order-of-magnitude reasoning, not literature values.
