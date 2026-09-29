# Quantum-advantage candidates outside protein structure: final report

Date: 2026-09-28. Status: LITERATURE AND DESIGN REPORT. No experiment has been run for anything in this report. Unless a citation is given, all numbers are order-of-magnitude estimates by the program's auditors. All novelty statements are scoped to the sources and dates in Section 3.

Working notes (query logs, arithmetic, per-citation verification): `research/reports/lit_work/`. These comprise 12 discovery files, the pool/shortlist synthesis, 18 audit files, the selection file and 2 red-team files.

---

## 1. Executive summary

**The brief** asked for exactly three practical, benchmarkable problems where an original quantum advantage could plausibly be shown and has not already been shown. It accepted a useful, materially distinct subsection of a studied field.

**The result is one finalist, not three.** The program considered 50 distinct problems from 12 discovery lenses. Six were shortlisted and each received three independent audits (novelty, strongest classical adversary, resources/break-even). The selection lead found that only one cleared the bar, and only conditionally. That candidate went to two hostile reviewers. Neither found a fatal objection to the whole candidate, but together they killed two of its sub-claims and required ten revisions. Slots 2 and 3 are left empty on purpose (Sections 11, 12): filling them would mean accepting a quantum-usefulness-only claim (category 1) or an unmeasured decision flip. That is the false-hardness pattern that sank the protein program (lessons L1, L5).

**Finalist C01, after red-team revision:** the correlated thermal electronic dynamic structure factor S_ee(q,ω) of warm dense hydrogen at r_s ≈ 2 and θ = T/T_F = 0.25–0.5, at X-ray Thomson scattering (XRTS) wavevectors. The uniform electron gas (UEG) serves only as an exact validation rung against path-integral Monte Carlo (PIMC).
- **Scoped novelty: category B.** Quantum protocols exist nearby for warm-dense-matter (WDM) stopping power, opacity and conductivity, and for the zero-temperature electronic DSF in an active space. In the sources searched, no quantum computation of the thermal electronic S_ee(q,ω) for XRTS was found, and no comparison against PIMC plus analytic continuation or model-free imaginary-time analysis.
- **Claim target: category 3 (computational/resource advantage), and only in accuracy class.** It would apply only at a named state point where a tuned classical portfolio either cannot run (the exact families hit the fermion sign problem) or disagrees internally beyond experimental error. Any gain over TDDFT in cost is polynomial.
- **Main risks:**
  1. Information value (L5). In equilibrium, the imaginary-time correlation function (ITCF) and S(q,ω) are a Laplace pair, and temperature is already extracted model-free.
  2. Single-family hardness (L7). The wall rests on one group's statement that PIMC is unavailable, with no multi-family disagreement documented.
  3. Correlated thermal-state preparation is unsolved. A Mermin-determinant start gives an estimated 8–16% temperature bias.
  4. Resources. The UEG validation rung is 4e13–9e14 Toffoli per state point, which is 1.5–3 orders above the program's S·G ≤ 1e12 screen. The hydrogen advantage rung is 7e16–1.6e18 Toffoli before the Born-Oppenheimer snapshot multiplier.
  5. No equilibrium consumer experiment at this state point has been found.
  6. High scoop risk. A Sandia group has publicly announced WDM linear response as ongoing work.
- **A structural contradiction the program must resolve.** The rung that can be benchmarked exactly (UEG) has no advantage. The rung that might have one (hydrogen) has no exact cross-check.

**First experiment:** a purely classical, laptop-scale information gate (K-C01a, Section 19). It tests whether an exact real-frequency S_ee narrows the (n_e, Z, collision-frequency) posterior beyond the best classical forward model plus model-free temperature, at a named instrument resolution. It is followed by a multi-family classical gate (K-C01b, about 1e4 core-hours) with a θ = 1 control. No quantum resource work beyond a UEG-rung estimate is justified until both pass.

**Cross-cutting finding** (recommended for `SCIENTIFIC_MEMORY.md`). In all six audited candidates the same pattern appeared: *the classical wall and the decision-relevant information sit in different regimes, and cost is dominated by sampling and state preparation, not Hamiltonian simulation.* It generalises protein lessons L3, L5 and L6 beyond protein structure.

---

## 2. Research methodology

The workflow followed the program's cycle (READ → HYPOTHESIS → … → KILL/ESCALATE). It was restricted to literature, reasoning and order-of-magnitude costing, and no compute was launched.

1. **Discovery.** Twelve lenses independently proposed candidates and logged queries and kills (Section 5).
2. **Pooling.** Duplicates were merged into 50 distinct problems. Each was classified as shortlist (6), reserve (6) or killed (38), with a named filter for every kill (`pool_and_shortlist.md`, Section 1).
3. **Hard filters.** These were applied at every stage:
   - F-claimed: already claimed or established.
   - F-classical: the strongest classical method already closes the gap.
   - F-quad: quadratic or low-polynomial speedup.
   - F-load: preparation, oracle or readout dominates.
   - F-sim: classically simulable in the relevant regime.
   - F-toy: no practical user.
   - F-bench: no benchmark path.
   - L1–L7: the protein lessons (weak baseline; solver equivalence; argmin over a classical landscape; simulator time ≠ physical time; information vs computation; model floor; single-family hardness).
4. **Triple audit.** Each shortlisted candidate received three audits: novelty/prior art, classical adversary, and resources/break-even.
5. **Selection.** Candidates were ranked qualitatively on ten dimensions, with no single score, and marked eligible or not.
6. **Red team.** Each eligible candidate went to two hostile reviewers (classical/technical; prior art/significance). An adjudicator was available for disputed fatal objections.
7. **Integration.** Every red-team required revision is folded into the final formulation (Section 10). Findings are reported with the program's six claim categories.

**Resource screen.** Toffoli count per circuit G times the number of circuits S must satisfy S·G ≲ 1e12 for an early-fault-tolerant (FT) claim. A stated later-FT rate is allowed if it is declared. Runtime conversions use 170 µs per Toffoli for one magic-state factory (Babbush et al., arXiv:2011.04149), or stated aggregate rates of 1e6 and 1e8 Toffoli/s. Simulator runtime is never counted as physical runtime.

---

## 3. Literature-search scope

- **Date limit.** All searches ran through 2026-09-28.
- **Sources actually used:**
  - arXiv export API and arXiv abstract, listing and HTML pages, including full-text scans of key papers
  - Crossref (bibliographic and DOI queries)
  - OpenAlex (search and `cites:` cited-by lists, where not rate-limited)
  - Semantic Scholar (citations, partially)
  - OSTI records (individual records; the OSTI search endpoint failed)
  - local PDF text extraction (pypdf) for tables in Rubin et al. 2024, Babbush et al. 2021, Dornheim 2019 and Gao et al. 2024/25
- **Not available or incomplete:**
  - WebSearch: the session budget of 200/200 was exhausted before or during every audit.
  - OpenAlex and Semantic Scholar returned HTTP 429 repeatedly, and some arXiv API calls also returned 429.
  - Not searched: theses, patents, conference talks, company and group web pages (PsiQuantum, Quantinuum, IBM, Microsoft, Phasecraft, QSimulate, Riverlane, Algorithmiq, BlueQubit, LANL/LLNL group pages), and journal-only work not indexed by these services.
- **Volume.** Several hundred logged queries: about 30–50 per discovery lens, about 12–34 per audit, and about 30 per red-team reviewer. The full logs are in each `lit_work/*.md` file.
- **Consequence.** Every "not found" in this report is a scoped statement, not a proof of absence. Where a statement is load-bearing, Section 14 repeats its exact scope.

---

## 4. Search domains

The lenses covered:
- high-energy-density (HED) and inertial-confinement-fusion (ICF) plasma physics: XRTS, transport, stopping power, opacity, equation of state
- stellar and kilonova atomic data
- nuclear astrophysics: supernova neutrino opacities, neutron matter
- nuclear structure and reactions: shell model, level densities, 0νββ, fission, capture, neutrino-nucleus scattering
- 1D, 2D and 3D quantum magnetism and neutron scattering (INS), including spin ice, Kitaev materials, thermal Hall and THz 2D spectroscopy
- correlated-electron lattice models: Hubbard, nickelates, moiré, DMFT impurity solvers, nonequilibrium impurity transport, Mott photophysics
- magnetic resonance: NMR, EPR, µSR, NV ensembles
- molecular and bioinorganic chemistry: spin ladders, f-element exchange, core-level spectroscopy, photophysics, spin-state energetics
- organic electronics
- AMO physics: strong-field and multiphoton ionization, collective radiance, clocks, charge exchange, line lists and pressure broadening, parity violation
- semiconductor ultrafast optics: exciton Mott transition in 2D TMDs
- defect metrology (positrons)
- optical communications (joint detection)
- continuum PDE solvers (CFD, Vlasov, radiative transfer, NEGF transistors, seismology)
- combinatorial optimization and planted inference (DQI/OPI, QAOA, QHD, MIS, quantum MCMC)
- SciML and inference loops
- claimed-advantage demonstrations and their dequantizations
- fault-tolerant resource estimates across all of the above

Excluded by the brief: protein problems; generic finance, logistics, ML, crypto, "drug discovery" and "materials discovery"; pure mathematics.

---

## 5. Agent/workstream design

| Stage | Agents | Output file(s) | Role |
|---|---|---|---|
| Discovery | 12 lenses: **algorithms, complexity, claims, amo, materials, chemistry, sciml_inference, optimization, classical_frontier, qsim_dynamics, alt_domains, resources** | `discovery_<lens>.md` | Each proposed candidates with INPUT → OUTPUT, quantum mechanism, classical twin and scoped novelty, and logged its own kills with reasons. |
| Synthesis | 1 | `pool_and_shortlist.md` | Merged candidates into 50, applied the filters, and produced 6 shortlisted, 6 reserve and 38 killed. |
| Audits | 3 per shortlisted candidate (18 in total): novelty, classical adversary, resources | `audit_C{01,04,07,14,41,44}_{novelty,classical,resources}.md` | Independent verdicts (survives, wounded or killed) with a scoped novelty statement, the strongest classical attack, and S·G arithmetic. |
| Selection | 1 | `selection.md` | Ranked the 6 on 10 qualitative dimensions, sharpened each formulation, and marked eligibility. |
| Red team | 2 hostile reviewers per eligible candidate (classical/technical; prior art/significance), plus 1 adjudicator | `redteam_C01_{classical,priorart}.md` | Fatal vs fixable objections and required revisions. The adjudicator acts only on contested fatal objections. |
| Writers | this report | `TOP3_QUANTUM_ADVANTAGE_CANDIDATES.md` | Integration. It adds no new evidence. |

What each lens looked for:
- **algorithms:** primitive-to-observable fits.
- **complexity:** hardness and dequantization maps.
- **claims:** published advantage claims and their rebuttals.
- **amo, materials, chemistry:** domain scouting.
- **sciml_inference:** forward models inside inference loops.
- **optimization:** non-landscape optimization mechanisms.
- **classical_frontier:** places where classical methods genuinely disagree.
- **qsim_dynamics:** transport and nonequilibrium dynamics.
- **alt_domains:** fields outside the usual quantum-chemistry lanes.
- **resources:** the fault-tolerant resource-estimate register and break-even.

---

## 6. Initial candidate pool

After merging, the pool held 50 problems: 6 shortlisted, 6 in reserve and 38 killed. The filter abbreviations are defined in Section 2.

| ID | Problem | Domain | Status | Reason (short) |
|---|---|---|---|---|
| C01 | Real-frequency S_ee(q,ω) of degenerate WDM for XRTS | HED / ICF diagnostics | shortlist → **finalist (conditional)** | Found by 3 lenses. Scoped B, little model floor. Sign problem plus ill-posed analytic continuation. |
| C02 | WDM DC/AC and thermal conductivity, Lorenz number, G_ei | HED transport | reserve | Scoped C (Sandia OSTI resource report). DC limit costs 1e13–1e16 Toffoli. Fallback if C01 fails L5. |
| C03 | Solar-interior Fe L-shell opacity | Stellar opacity | killed | F-claimed (arXiv:2607.02811). L6 plasma-environment floor. Classical screening+CI result (2607.21238). |
| C04 | Kilonova Ln/An expansion opacity via thermal dipole spectral function | Atomic data / astrophysics | shortlist → killed | See Section 7. |
| C05 | WDM stopping power | HED | killed | F-claimed (Rubin et al. PNAS 2024). |
| C06 | Static WDM/dense-matter thermodynamics (EOS, H LLT, H-He demixing, Earth-core Fe, lattice κ) | HED / planetary | killed | F-classical. L3 (QPE inside a classical sampler). L6 finite-size and composition floors. Earth-core claim retracted. |
| C07 | Hot neutron-rich matter axial/vector response for supernova opacities | Nuclear astrophysics | shortlist → killed | See Section 7. |
| C08 | ν-nucleus response at DUNE energies | Nuclear / neutrino | killed | L6: pions and relativistic kinematics lie outside lattice EFT. Scoped C. |
| C09 | Low-energy CC ν_e–40Ar exclusive branching | Nuclear / neutrino | killed | No classical wall. The 5% target is below the LEC uncertainty. |
| C10 | 0νββ nuclear matrix elements | Nuclear | killed | L6: the LEC dominates the spread. |
| C11 | Fission fragment fluctuations | Nuclear data | killed | An EDF is not a Hamiltonian (F-bench). |
| C12 | Nuclear level densities; shell-model ground states | Nuclear | killed | F-classical (SMMC, Lanczos). Crowded field. |
| C13 | Few-nucleon capture/resonances; collective ν flavour | Nuclear | killed | L6: keV placement. Few-body is classically exact. |
| C14 | Finite-T polarized S(q,ω) of 3D π-flux quantum spin ice | 3D magnetism / INS | shortlist → killed as specified | See Section 7. A redesign lane is noted in Section 11. |
| C15 | 2D frustrated-magnet S(q,ω) forward model / Hamiltonian discrimination | 2D magnetism | reserve | Scoped C. Strongest classical 2D toolbox. Semiclassics suffice at high T. |
| C16 | THz 2DCS of frustrated magnets | Nonlinear spectroscopy | killed | F-bench (scarce data). Two-time cost. |
| C17 | Thermal Hall κ_xy of extended Kitaev models via Gibbs states | Kitaev QSL | reserve | Scoped A, static mechanism. Unknown mixing time. Phonon-dominated signal. |
| C18 | Real-time quantum vs QMC+analytic continuation resolution benchmark | Spectral inverse problems | killed | F-toy. Folded into C14 as a validation rung. |
| C19 | Protocol-dependent metastable states via quantum thermal gradient descent | Quantum spin glasses | reserve | Most original mechanism in the pool. No physical hard instance. Lab-timescale floor. |
| C20 | Sub-K ADR refrigerant entropy of Yb magnets | Cryogenics | killed | F-sim (T ≳ J). |
| C21 | LiHoF4 3D dipolar Ising dynamics | Quantum magnetism | killed | F-toy. L6. |
| C22 | Annealer beyond-classical dynamics | Analog simulation | killed | E (TN-BP, NQS, t-VMC). |
| C23 | 1D INS S(q,ω) | 1D magnetism | killed | F-sim and F-claimed (hardware demonstrations exist). |
| C24 | High-T spin dynamics and NMR family | Magnetic resonance | killed | L5, as in the protein NMR lane. |
| C25 | Momentum-resolved RIXS of doped 2D Hubbard / nickelates | X-ray spectroscopy | killed | L6. DQMC may match at 30–40 meV. Far-FT. |
| C26 | Pairing symmetry of 2D Hubbard / bilayer nickelates | Superconductivity | killed | L6 (Hund J). Helios demonstration. DMRG+AFQMC. |
| C27 | Correlated-metal transport | Correlated metals | killed | Weak decision relevance. Cold-atom analogs. |
| C28 | Impact ionization in photoexcited 2D Mott insulators | Mott PV | killed (runner-up) | L6 (multi-orbital, e-ph, interfaces). |
| C29 | Multi-orbital f-electron DMFT impurity solvers | Heavy fermions | killed | L6 (U/J/double counting). Crowded C. |
| C30 | Nonequilibrium impurity transport | Nanoelectronics | killed | F-classical (inchworm, AMEA, TN). L7. |
| C31 | Hubbard quench demos and driven-Mott phenomena | Nonequilibrium matter | killed | E/D claims. L6. |
| C32 | SO-coupled exchange spectra of multinuclear f-element magnets | Molecular magnetism | reserve | Scoped B. Polynomial advantage. FeMoco-type floor. |
| C33 | Spin ladders of 3d polynuclear clusters | Bioinorganic | killed | F-classical (CC+DMRG ranking). Polynomial. |
| C34 | Multinuclear L-edge XAS/RIXS/Kβ XES | Core-level spectroscopy | reserve | Scoped C. Lifetime broadening may wash out correlation (L5). |
| C35 | Paramagnetic NMR contact shifts in clusters | Magnetic resonance | killed | L6 (core spin polarization). |
| C36 | TM/Ln photophysics and photochemical control | Photochemistry | killed | L6 (LVC/PES). Experiment is its own oracle. |
| C37 | Organic-semiconductor charge generation and mobility | Organic electronics | killed | Duplicates prior OPV lane. L6. Wall closed. |
| C38 | π-stacked noncovalent reference energies | Quantum chemistry | killed | Classical consensus converging. |
| C39 | Ground-state chemistry energetics (SQD Fe-S, FeMoco, spin states, …) | Chemistry | killed | E, or classically solved (2601.04621, 2603.28648). |
| C40 | Crossover audit of cheap published algorithms | Audit | killed as advantage target | Expected clean negative. |
| C41 | Correlated multi-electron ionization: joint photoelectron momentum sampling | AMO / attosecond | shortlist → killed | See Section 7. |
| C42 | Solar-wind HCI charge exchange | Ion-molecule collisions | killed | L6/L5 (composition dominates). |
| C43 | Atomic/molecular data with polynomial walls | Spectroscopic databases | killed | F-quad. L6. |
| C44 | Dense e-h plasma through the exciton Mott crossover in 2D TMDs | Ultrafast optics | shortlist → killed (residual only) | See Section 7. |
| C45 | Positron annihilation lifetimes at vacancies | Defect metrology | killed | F-classical (nodeless positron, so DMC works). |
| C46 | BPQM joint detection of coded optical signals | Optical comms | killed | Not a computational advantage. |
| C47 | Quantum PDE/linear-algebra solvers | Continuum simulation | killed | F-quad, F-load. |
| C48 | Optimization over classical landscapes | Optimization | killed | L3, F-quad, E. No physical output. |
| C49 | Quantum-in-the-loop inference and ML | SciML | killed | At most quadratic over a classical likelihood. |
| C50 | Dequantized demonstrations and out-of-scope fundamental targets | Demonstrations / HEP | killed | E, contrived hardness, or no observable. |

About 150 further problems were killed at lens level before pooling and were merged into the entries above (for example C22, C24, C43, C47, C48, C50). They are listed with reasons in each `discovery_<lens>.md` file under "killed" and summarised in Section 8.

---

## 7. Major candidates eliminated

These are the five shortlisted candidates that received full triple audits and were not selected. The verdicts are novelty / classical / resources.

| ID | Candidate | Verdicts | Terminal verdict |
|---|---|---|---|
| C14 | Finite-T polarized S(q,ω) of 3D dipolar-octupolar π-flux quantum spin ice (Ce2Zr2O7 / Ce2Sn2O7 / Ce2Hf2O7) | wounded / wounded (severe) / killed | Killed as specified. An unaudited redesign lane remains (Section 11). |
| C44 | Dense e-h plasma dynamics through the exciton Mott crossover in 2D TMDs | wounded (B, not A) / killed / wounded | Killed as a practical target. A category-1 residual remains. |
| C41 | Correlated multi-electron strong-field/photo-ionization: joint momentum sampling | wounded / killed / wounded | Killed. A category-3 reference residual has no consumer. |
| C07 | Real-frequency spin/density response of hot neutron-rich matter for supernova opacities | wounded / killed / killed | Killed. A category-1 residual remains. |
| C04 | Kilonova Ln/An expansion opacity from thermal dipole spectral functions | wounded / killed / killed | Killed. No quantum residual. |

Pool-level kills worth noting because they were popular or were claimed elsewhere:
- WDM stopping power (C05) and solar Fe opacity (C03): already claimed.
- 1D INS (C23): already on hardware and classically exact.
- NMR/high-T spin dynamics (C24): the protein L5 failure again.
- Annealer beyond-classical dynamics (C22): category E.
- SQD/FeMoco-class ground states (C39): category E, or classically solved.
- Optimization over classical landscapes, including DQI/OPI (C48): L3, and no physical output.

---

## 8. Why they were eliminated

### 8.1 Shortlisted candidates

**C14, 3D π-flux quantum spin ice.**
1. **L5: the data need only short times.** The Gao et al. ThALES data (arXiv:2404.04207) have 0.042–0.076 meV FWHM resolution. That corresponds to t_max ≈ 5–13 ħ/J_par, which is the home ground of classical methods, not the 50/J± the candidate assumed. The emergent photon (≈ 0.0028 meV) is below resolution. The authors themselves report that c_QSI and θ "cannot be uniquely determined".
2. **The decision version flips nothing.** Four or more classical approaches already rank π-flux above 0-flux: ED+MD, Lanczos+MC, GMFT, and QMC/ED/GMFT.
3. **Finite size biases the decisive quantity.** At L = 3 the lowest photon mode lies above k_BT, so the quasielastic weight that matters is biased. L ≥ 5 (N ≥ 2000) is needed.
4. **The bottleneck is misidentified.** It is the low-T Gibbs state of a U(1) spin liquid, which has no mixing bound, not 3D entanglement growth.
5. **L6: disorder dominates.** About 2% vacancies dominate the dynamics (arXiv:2609.28643), and the measured crystal has 4% anti-site disorder.
6. **Resources:** 7e13 T with a heuristic preparation, up to 3e16–4e18 T with a Gibbs sampler.

**C44, 2D TMD e-h plasma.**
1. **Novelty is B, not A.** Klymenko et al. (arXiv:2606.04295) already compute semiconductor Bloch equation absorption and gain on a (simulated) quantum computer and name the many-body extension as their route to advantage.
2. **L5/L7: an approximate method already reproduces the experiment.** GW + Fan-Migdal GKBA (arXiv:2604.06897) reproduces the ~100 fs exciton quench and the absence of gain at the same carrier count the candidate proposes. No multi-family disagreement was found.
3. **L6: the model floor is large.** Phonon-driven exciton formation, K–Q valley reordering and r0/ε_env uncertainty move n_M by about 3x.
4. **Representation defect.** A fixed-particle-number first-quantized register cannot hold the coherent pump.
5. **Cost:** spectra need 5e14–1e15 Toffoli per point. Only scalars at η ≤ 64 (3e11–3e12) fit the screen, as a category-1 benchmark.

**C41, multi-electron ionization.**
1. **Every named channel is covered classically.**
   - He is solved in full 3+3-D (Zielinski et al. 2016; Zhu & Scrinzi 2020 vs COLTRIMS).
   - Li triple photoionization was solved by TDCC in 2004, and experiments measure only totals.
   - Ne/Ar near-IR triple ionization is matched by two independent approximate families (3D semiclassics and a reduced-dimension quantum model).
2. **The sampling claim fails (category 4).** Classical-trajectory Monte Carlo is itself a cheap sampler of the joint momentum distribution.
3. **L3: rare channels make it expensive.** Differential marginals cost about 1e16 Toffoli even with amplitude amplification, which is only quadratic.
4. **L6: the model floor exceeds solver error.** Intensity calibration and frozen-core/pseudopotential error are larger.
5. **The mechanism is already published** (Kharazi 2026; Chan 2023).
6. **No consumer.** The exact η ≥ 4 wall is real, but nothing downstream needs it.

**C07, supernova neutrino opacities.**
1. **The decision-relevant quantities are already computed.** Static S_A and S_V are ab initio at lattice N3LO (Ma et al., PRL 132, 232502, 2024).
2. **No sign problem where the candidate put it.** LO pure neutron matter and SU(4)-symmetric LO at Y_p > 0 are sign-free.
3. **The lineshape width is where cost explodes.** A width requires tensor/OPE forces, which cost about 5.9e23 T at L = 10 (Watson et al., arXiv:2312.05344).
4. **L5: low decision leverage.** A 2–5x change in bremsstrahlung moves luminosities by 5% or less (Bartl et al. 2016).
5. **A smeared classical twin exists** (Hansen–Lupo–Tantalo).
6. **L6:** where the sign problem returns, uniform matter is the wrong model (clusters, pasta).

**C04, kilonova opacity.**
1. **Classically exact in the valence space.** Valence-space FCI covers every Ln II/III ion, at most C(32,14) ≈ 4.7e8 determinants.
2. **L6: the code spread is not solver error.** It comes from completeness, calibration and configuration-average energies set by core-valence correlation outside any active space.
3. **The readout mismatches the field's direction.** A thermal readout serves only LTE line-binned opacity, while the field is moving to line-by-line NLTE.
4. **L5: other uncertainties are larger.** NLTE (x2–10), thermalization and nuclear inputs swamp the atomic-data effect.
5. **Cost:** 6e13–5e18 Toffoli per ion per temperature, against an already-published calibrated classical dataset (arXiv:2507.07785).

### 8.2 Pool and lens-level kills, grouped by mechanism

1. **Already claimed or established (F-claimed):**
   - WDM stopping power (arXiv:2308.12352)
   - Fe opacity (arXiv:2607.02811)
   - WDM conductivity (OSTI doi:10.2172/3363975)
   - 1D INS on hardware (arXiv:2603.15608, 2607.07138)
   - pairing on Helios (arXiv:2511.02125)
   - PDT intersystem crossing (arXiv:2512.15889, 2601.18898)
   - nanographene PPP (arXiv:2605.00745)
2. **Claimed, then challenged or dequantized (category E):**
   - IBM kicked Ising (arXiv:2306.14887, 2306.16372)
   - D-Wave spin-glass quench (arXiv:2403.00910 vs 2503.05693, 2503.08247, 2609.01719)
   - GBS vibronic spectra (arXiv:2202.01861)
   - 1D Fermi-Hubbard quench (arXiv:2606.04771)
   - SQD/QSCI ground states (arXiv:2608.11569, 2608.05314)
   - Rydberg MIS (arXiv:2307.09442)
   - quantum-enhanced MCMC (arXiv:2403.03087)
   - noisy-circuit utility (arXiv:2407.12768)
3. **L3 (argmin or search over a classical landscape) and F-quad:**
   - QAOA/LABS, QHD, backtracking, cluster-expansion ordering, seismic inversion
   - quantum likelihood / Grover-over-grids inference
   - QLSA/Carleman PDE solvers (particle Monte Carlo already gives 1/ε²)
   - CFD, bounded at O(Re^{3D/8}) (arXiv:2512.03758)
   - NEGF transistors
   - pressure broadening (close coupling is N³)
4. **L5 (classically computable where informative):**
   - high-T spin dynamics and NMR (arXiv:2508.06448, 2403.16850, 2409.01706)
   - short-time dynamics (arXiv:2210.11490)
   - optical-clock collective shifts (arXiv:2303.05613)
   - 1/T1 and µSR (hydrodynamic tails)
5. **L6 (model floor larger than solver error):**
   - 0νββ (arXiv:2408.02169)
   - keV nuclear resonances; fission EDFs
   - DMFT double counting
   - Hubbard/nickelate parameters (arXiv:2602.20288)
   - spin-state energetics (SSE17, doi:10.1039/d4sc05471g)
   - TADF rates; electrochemistry
   - ultracold sticky collisions; Earth-core composition
   - H-He finite size (arXiv:2603.28927)
   - collective-neutrino reduced models
6. **F-classical (the classical wall is already closed):**
   - FeMoco and Fe4S4 (arXiv:2601.04621, 2603.28648)
   - noncovalent CC/DMC puzzle
   - organic mobility (arXiv:2312.14914)
   - INVEST gaps (arXiv:2603.11891)
   - SMMC level densities (arXiv:2509.26571)
   - positron DMC
   - HCI clocks (CI+MBPT/KRCI agree)
7. **Not a computational problem, or F-toy:**
   - BPQM receivers, quantum-limited imaging, metrology protocol design
   - lattice-gauge string breaking
   - DQI/OPI (no physical output)
   - quartic planted inference (cryptographic motivation)

---

## 9. Final candidates

| Slot | Candidate | Status | Scoped novelty | Claim category targeted |
|---|---|---|---|---|
| 1 | **C01, correlated thermal S_ee(q,ω) of warm dense hydrogen at r_s ≈ 2, θ = 0.25–0.5 for XRTS, with an exact UEG validation rung** | Conditional finalist: it must pass classical gates K-C01a and K-C01b before any quantum work | B | 3 (accuracy-class computational/resource advantage vs a tuned classical portfolio); fallback 1 |
| 2 | none | Not filled (Section 11) | none | none |
| 3 | none | Not filled (Section 12) | none | none |

The red team rejected no candidate: C01 was the only candidate sent to it, and neither reviewer found a fatal objection to the whole candidate. The red team did kill two C01 sub-claims (Section 18).

---

## 10. Detailed analysis: Finalist 1, C01

The formulation below is the final one. It incorporates all required revisions from both hostile reviewers; Section 18 maps each revision to where it lands.

**1. Topic name.** Correlated real-frequency electronic dynamic structure factor of partially degenerate warm dense hydrogen, for X-ray Thomson scattering diagnostics. The uniform electron gas serves as the exact validation rung.

**2. Precise computational problem.**
- INPUT:
  - Validation rung: the UEG at r_s ∈ {2, 3, 4}, θ ∈ {0.5, 1}.
  - Target rung: hydrogen (bare protons, Born-Oppenheimer ion snapshots from classical MD or DFT-MD) at r_s ≈ 2 (ρ ≈ 0.33 g/cc), θ ∈ {0.5, 0.25} (T ≈ 6.3 and 3.1 eV).
  - XRTS wavevector q, and a stated instrument function (NIF-like 5–20 eV FWHM; XFEL-like 0.1–1 eV).
  - The CH rung is dropped. Carbon K-shell electrons force either a prohibitive plane-wave cutoff or pseudopotentials, and pseudopotentials break the bare-Coulomb premise.
- COMPUTE:
  - The correlated thermal density-density correlator ⟨ρ_q(t) ρ_{−q}(0)⟩_β out to t ≈ 2π/Δω, at resolution Δω of 2–5 eV.
  - It starts from a costed correlated thermal state, not a Mermin determinant.
- OUTPUT:
  - S_ee(q,ω) with error bars (plasmon position, width and damping; intermediate-q lineshape).
  - The induced posterior on (n_e, Z/ionization, collision frequency ν), with temperature taken model-free from ITCF detailed balance.
- SCALING LADDER:
  - η = 32 is restricted to q ≥ 0.64 k_F, because q_min/k_F = 0.64 (32/η)^{1/3}.
  - η ≥ 131 is required to reach q = 0.4 k_F.
  - θ runs from 1 through 0.5 to 0.25.
  - Each state point carries a Born-Oppenheimer snapshot multiplier of 10–100 and an interpolation error from the discrete-q grid.
- VALIDATION:
  - At θ ≥ 0.5 on the UEG, the two-sided Laplace transform of the quantum S must reproduce quasi-exact PIMC F(q,τ).
  - A θ = 1 hydrogen control, where the classical families must agree with PIMC, calibrates the spread metric.

**3. Real-world use.** XRTS is a primary diagnostic of density, temperature and ionization in ICF capsules (NIF), shock-compressed matter (OMEGA) and XFEL-heated samples (LCLS, EuXFEL). Inferred states feed equation-of-state tables and hydrocode design.

**4. Why it matters.**
- In partially degenerate, partially ionized hydrogen at θ ≲ 0.5, XRTS inference relies on forward models (TDDFT kernels, Chihara/average-atom) that have not been validated at those temperatures.
- The one validation, corrected LR-TDDFT vs PIMC for hydrogen, exists at θ = 1 (arXiv:2507.00688).
- If the classical families disagree there by more than experimental error, inferred (n_e, Z) are model-dependent in a regime that ICF compression paths cross.
- If they do not, that is itself a useful negative result for the XRTS community.

**5. Classical state of the art.**
- **PIMC:**
  - Direct fermionic PIMC is feasible down to θ ≈ 0.5 at small N (Dornheim 2019, arXiv:1906.00635).
  - ξ-extrapolation / Taylor-ξ / fictitious-particle methods reach N ≤ 1000 for static properties (arXiv:2311.08098), matched NIF Be XRTS at θ ≈ 2.7 (arXiv:2402.19113), and give free energies "down to half the Fermi temperature" (arXiv:2502.15288). They break down at θ = 0.5 (arXiv:2509.11317, 2308.06071).
- **Analytic continuation of PIMC ITCF:** stochastic dynamic LFC, MaxEnt, PyLIT (arXiv:1810.12776, 2503.20433, 2603.27212). S(q,ω) is free of finite-size effects already at N = 14 (arXiv:2004.13429).
- **UEG in the C01 window:**
  - the effective static approximation (ESA) LFC for 0.7 ≤ r_s ≤ 20, 0 ≤ θ ≤ 4 (arXiv:2101.05498, 2008.02165);
  - real-frequency diagrammatic Monte Carlo at r_s = 1, 2, 4 across T/ε_F from ≪1 to >2 (arXiv:2205.13595, 2311.05611);
  - phaseless finite-T AFQMC at θ ≤ 0.5, r_s ≤ 2 (arXiv:2012.12228);
  - pseudo-fermion PIMC to θ = 0.0625 for energies (arXiv:2603.28000);
  - static UEG at θ = 0.25 (arXiv:2506.10113).
- **Correlated thermal states of warm dense hydrogen:**
  - deep variational free-energy method at N = 14–54, r_s 1.86–2, θ ≈ 0.07–0.43, sign-free and in agreement with RPIMC (arXiv:2507.18540);
  - fixed-node RPIMC.
- **Dynamics and response:**
  - LR-TDDFT and Liouville–Lanczos (arXiv:2502.04921);
  - ITCF-constrained TDDFT (arXiv:2510.01875);
  - f-sum-corrected nonlocal-xc TDDFT (arXiv:2609.18584);
  - RT-TDDFT (arXiv:2511.14643);
  - mixed stochastic TDDFT (arXiv:2410.23599);
  - finite-T GW for WDM (arXiv:2605.11308);
  - wave-packet DSF (arXiv:2407.08875);
  - Chihara/average-atom (xDAVE, arXiv:2604.27237);
  - exact odd-moment and cubic sum rules tying S to static n(k) and kinetic energy (arXiv:2508.17810, 2606.30123).
- **Model-free ITCF analysis** gives T, normalization and Rayleigh weight without a forward model (arXiv:2211.00579, 2604.25735), now even without the source-and-instrument function (arXiv:2510.26747).

**6. Why it is classically difficult.**
- **The fermion sign problem is exponential in N and β.** For the UEG at θ = 0.5 the average sign is 3.6e-3 at N = 8, and about 1e-6 is expected at N = 66 (arXiv:2509.11317).
- **Every exact-PIMC workaround breaks down at θ = 0.5.** Moldabekov et al. state that for hydrogen at r_s = 2, θ = 0.5 and 0.25, "PIMC becomes unavailable due to the notorious fermion sign problem" (arXiv:2507.00688). At those points only an adiabatic-kernel TDDFT family has been applied, and its kernel already deviates from PIMC S_ee(q) at q ≳ 3 q_F at θ = 1.
- **Honest qualification (red team).**
  - This is a validation gap, not a demonstrated classical failure.
  - Sign-free variational thermal states, fixed-node RPIMC, finite-T GW/BSE and sum-rule-constrained models are all available or near-available at the point, and have not been compared.
  - The hardness is single-family (L7) until K-C01b is run.

**7. Proposed quantum mechanism.**
- First-quantized plane-wave electrons with 3η·n_p system qubits and qubitized or product-formula block encodings (Su et al., arXiv:2105.12767; Rubin et al., arXiv:2308.12352).
- **Correlated thermal state.** Microcanonical QPE filtering of sampled determinants (ETH-level ensemble equivalence), or a detailed-balance Gibbs sampler (arXiv:2303.18224, 2311.09207), or energy-filtered response functions without an explicit Gibbs state (Cruz, Wild, Bañuls, Cirac, doi:10.1103/lpz2-j7vg).
- **FULL vs ABLATION.** If a classical variational thermal state (arXiv:2507.18540) seeds the preparation, the design must be pre-registered as FULL vs ABLATION to show the quantum stage is load-bearing.
- **Observable.** A weak density kick exp(−i g Σ_j cos(q·r_j)) (diagonal, cheap), evolution to t, then a QFT and projective position measurement to read ρ_q. The fluctuation-dissipation theorem then gives S(q,ω).
  - A Hadamard test is worse: ρ_q has LCU norm η, so it needs about (η/ε)² shots.
  - The single-electron trick yields only the self part.
- **The observable is not an argmin and not a search over a classical landscape (L3).**

**8. Exact quantum/classical comparison.**
- FULL: the quantum pipeline above.
- ABLATION / classical twin: the named portfolio, each member tuned with comparable effort:
  1. LR-TDDFT with ALDA, PBE, ESA, PIMC-derived static, and f-sum-corrected nonlocal kernels, plus Liouville–Lanczos
  2. RT-TDDFT
  3. finite-T GW / GW+BSE
  4. Chihara / average-atom
  5. ξ / Taylor-ξ PIMC at N = 14–32 with measured sign and extrapolation error, plus analytic continuation
  6. static constraints from RPIMC and variational-NN thermal states, entered through sum rules
  7. where available, ph-FT-AFQMC, qSTLS/dynamic LFC, wave-packet MD and G1-G2 NEGF
- Metrics:
  - S_ee(q,ω) after instrument convolution at named (r_s, θ, q), in units of experimental error (5–10% intensity at stated resolution);
  - the posterior on (n_e, Z, ν).
- Exact cross-check: UEG Laplace-transform agreement with PIMC F(q,τ) at θ ≥ 0.5.
- **"Exact finite-T fermion dynamics" is not the comparator.** Treating it as one would be a straw man (L1/L2).

**9. What constitutes advantage.**
- **Category 3 (accuracy-class computational/resource advantage).** All five must hold:
  1. At a named hydrogen state point (r_s ≈ 2, θ ≤ 0.5) the portfolio's inter-family spread, after instrument convolution, exceeds experimental error.
  2. The exact classical families verifiably fail there (measured sign, extrapolation breakdown).
  3. The quantum S_ee agrees with PIMC at the θ ≥ 0.5 UEG and θ = 1 hydrogen controls within stated error.
  4. The quantum result resolves the disagreement with bounded, stated resources.
  5. The thermal-state preparation error is bounded below the discriminating signal.
- **Category 1 (quantum usefulness)** if the result changes an XRTS inference (n_e, Z, ν) at a real experiment, even without a cost comparison.
- **Things that do not count:**
  - matching PIMC where PIMC works;
  - beating ALDA alone;
  - UEG results at θ 0.25–0.5, which ESA and diagMC already cover;
  - simulator runs;
  - a faster wall-clock than one classical code.

**10. Smallest meaningful benchmark.**
- **Validation benchmark.** UEG, η = 32, r_s = 2, θ = 0.5, q ≥ 0.64 k_F, 5 eV resolution, 5% precision. Pass criterion: the Laplace transform of the quantum S matches PIMC F(q,τ).
  - Audited cost for η = 32 at 5 eV and 5% with Heisenberg-limited estimation (θ = 0.25 row): 4e13–9e14 Toffoli per state point.
  - A θ = 0.5 point at the same resolution and precision is expected to be of the same order. It was not separately costed.
- **Smallest advantage-relevant benchmark.** Hydrogen at r_s = 2, θ = 0.5, η ≈ 128–131, one q in the collective regime, 2 eV resolution.

**11. Scaling variable.**
- Primary: electron number η at fixed (r_s, θ), from 32 to ≥ 131 (q-access), with η = 256 as a finite-size check.
- Secondary:
  - degeneracy θ from 1 to 0.25, the regime where the sign problem grows;
  - instrument resolution Δω;
  - precision ε.
- Cost scales roughly as S·G ∝ η^{1–2} / (Δω² ε²) (resource audit). Halving Δω or ε each costs about 4x.

**12. Required quantum resources.** From the resource audit; the arithmetic is in `audit_C01_resources.md`.

| Case | G (Toffoli/shot) | S·G, standard shots | S·G, Heisenberg-limited | Logical qubits |
|---|---|---|---|---|
| UEG η=32, θ=0.25, 5 eV, 5% | 5e9–1.2e11 | 1.6e15–3.7e16 | **4e13–9e14** | ~500–800 |
| UEG η=32, θ=0.5, 2 eV, 2% | 1e10–2e11 | 8e16–2e18 | 9e14–2e16 | ~500–800 |
| H η=128, θ=0.5, 2 eV | 1.6e12–3.6e13 | 3e18–8e19 | 7e16–1.6e18 | ~2700–3000 |
| H η=256, θ=0.5, 2 eV | 1.2e13–2.7e14 | 1e19–3e20 | 4e17–8e18 | larger |

- **Physical qubits:** about 1e6–1e7 surface-code qubits (order of magnitude, not sourced).
- **Multipliers not included in the table:**
  - 10–100 state points per posterior;
  - 10–100 Born-Oppenheimer snapshots for hydrogen;
  - the cost of correlated thermal preparation beyond the optimistic microcanonical filter (40–70% of G in the audited protocol).
- **Unresolved inconsistency.** Rubin et al. 2024's own per-a.u. cost differs by about 1.6e3x between λ·C_BE, their Fig. 8a and their Table IV. The table brackets it. It must be resolved, and the real-space quantum FMM Coulomb costing (arXiv:2510.07380) evaluated as an alternative.

**13. Expected classical resources.**
- PIMC above θ ≈ 0.5: about 1e3–1e5 CPU-hours per state point (auditor estimate).
- K-C01a: laptop, days.
- K-C01b, the full portfolio at two hydrogen state points plus the θ = 1 control: about 1e4 core-hours.
- LR-TDDFT per state point was not costed by the audits. It is expected to be many orders of magnitude below the quantum cost.

**14. Break-even estimate.**
- Against exact classical fermion dynamics: exponential separation in the sign-problem regime.
- Against the tuned approximate portfolio: **no cost break-even at any η**. Classical costs are CPU-hours to node-days; quantum costs are 1e13–1e18 Toffoli. The only possible advantage is in accuracy class, where the portfolio is unreliable.
- Wall-clock (my arithmetic from the table; simulator time excluded):
  - UEG validation, 4e13–9e14 Toffoli: about 5 days to about 3.4 months at 1e8 Toffoli/s; about 1.3–29 years at 1e6/s; about 200+ years with a single factory at 170 µs/Toffoli.
  - Hydrogen advantage rung, 7e16–1.6e18: about 22–500 years at 1e8/s, before the snapshot and state-point multipliers.
- Against the program screen: the UEG rung is 1.5–3 orders above S·G ≤ 1e12 and needs a declared later-FT rate. The hydrogen rung is 5–6 orders above and is resource-killed at any rate the program can currently justify.

**15. Existing quantum literature.**
- First-quantized WDM dynamics for stopping power (Rubin et al., arXiv:2308.12352).
- Exact dynamics vs mean field, with the speedup "most pronounced for finite temperature" (Babbush et al., arXiv:2301.01203).
- A zero-temperature active-space electronic DSF/EELS algorithm (Kunitsa et al., arXiv:2508.15935).
- Dynamic linear response of many-fermion systems (Roggero & Carlson, arXiv:1804.01505; Roggero GIT, arXiv:2004.04889; Baroni et al., arXiv:2111.02982; Spagnoli, Lissoni, Roggero, arXiv:2507.22814).
- Finite-T response functions without Gibbs-state preparation (doi:10.1103/lpz2-j7vg).
- Finite-T Green's functions (ROQAM), which state WDM linear response as ongoing work (Nelson & Baczewski, arXiv:2605.22920).
- Quantum opacity with spectral readout (Pathak, Kononov, Baczewski, arXiv:2607.02811).
- WDM conductivity resource estimates (OSTI doi:10.2172/3363975; metadata only).
- A Coulomb continuous-variable Gibbs sampler with a mixing-time guarantee, for Boltzmann particles only (Becker, Rouzé, Salzmann, arXiv:2604.15263).
- The Google "Grand Challenge" (arXiv:2511.09124), which lists stopping power, not XRTS.
- Spin-model DSF on hardware (arXiv:2603.15608, 2607.07138, 2607.02673).

**16. Exact novelty gap.** Three things are missing:
- a quantum algorithm or resource estimate for the thermal electronic S_ee(q,ω) of the UEG, H or CH at XRTS wavevectors with costed thermal preparation;
- any comparison of such a result, or of its Laplace transform, against PIMC F(q,τ) or against LR/RT-TDDFT;
- a quantified map of where the classical families fail or disagree at θ ≤ 0.5.

**17. Closest prior work.**
- Rubin et al. 2024: the same machinery with a different observable.
- Pathak, Kononov, Baczewski 2026: a spectral readout of a dense-plasma response at q ≈ 0.
- Kunitsa et al. 2025: the same observable class at T = 0 in an active space.
- Nelson & Baczewski 2026: announced intent.
- Moldabekov et al. 2026 (arXiv:2507.00688): the classical wall statement.

**18. Why it is genuinely different.**
- **A different bottleneck.** It requires a correlated thermal ensemble of continuum plane-wave electrons at finite q. That is a different bottleneck from T = 0 active-space EELS (no thermal state, no continuum), from stopping power (a projectile energy-loss observable from a mean-field determinant ensemble) and from dipole opacity (q ≈ 0).
- **An exact cross-check.** It is the only HED quantum-dynamics target found with an exact classical check (UEG PIMC F(q,τ)).
- **The contribution is not a new algorithm.** The red team was explicit: it is the observable and regime, the exact validation protocol, and the classical-wall map.

**19. Main failure reason (most likely).** The following are expected together.
1. **L5.** K-C01a shows that an exact real-frequency S does not narrow (n_e, Z, ν) beyond the best classical forward model plus model-free T at available resolution. Noise-free inference is already factor-3 to factor-22 degenerate (arXiv:2408.15346), and only a low-dimensional set of spectral features is stably recoverable (arXiv:2609.07208).
2. **L7.** K-C01b shows that classical families agree within experimental error at hydrogen r_s = 2, θ = 0.5/0.25.
3. **Structural contradiction.** The benchmarkable rung has no advantage and the advantage rung has no exact check.

**20. Strongest classical counterargument.**
- The UEG window is already covered by ESA and real-frequency diagMC.
- The correlated thermal state of warm dense hydrogen at θ 0.07–0.43 is already reached sign-free by variational neural methods.
- The observable's limits are fixed by static sum rules: the plasmon at small q by the f-sum and third moment, and the Compton regime at large q by n(k).
- At θ = 0.25 (T ≈ 3 eV), lineshape differences of order T sit below NIF resolution.
- Temperature is extracted model-free.
- So an exact S_ee would at most refine a low-dimensional, instrument-limited feature set that improved classical kernels are about to cover. The Dornheim/Moldabekov/Vorberger group is visibly moving TDDFT kernels, pseudo-fermion PIMC and variational states toward θ < 1.

**21. Kill experiment.** Pre-register both kills in `experiments/preregistered/`.
- **K-C01a (information gate).** Kill if an exact real-frequency S narrows the (n_e, Z, ν) posterior by less than 2x beyond the best classical forward model plus model-free T at named NIF-like and XFEL-like resolutions, with the degeneracy of arXiv:2408.15346 as the null.
- **K-C01b (multi-family gate).** Kill if the inter-family spread at hydrogen r_s = 2, θ = 0.5/0.25, convolved with the instrument function, is below experimental error. The θ = 1 control must reproduce PIMC for the result to count.
- **Consumer gate.** If no equilibrium XRTS experiment at r_s ≈ 2, θ 0.25–0.5 exists or is planned, record "no consumer".
- On a kill, enter it in `research/KILLBOOK.md` and `architectures/killed/`.

**22. Establishing experiment.** Sequence:
1. K-C01a passes.
2. K-C01b finds a named state point with spread beyond error, where ξ/Taylor-ξ verifiably fail.
3. A bounded-cost correlated thermal preparation is demonstrated at small η: exact classical emulation at η ≤ 8–14 comparing the microcanonical/filtered ensemble against canonical PIMC, with a measured window error.
4. A corrected resource estimate is produced that resolves the Rubin inconsistency and costs the FMM alternative.
5. On FT hardware at a declared rate: run the UEG θ = 0.5 validation (Laplace match to PIMC) and the hydrogen θ = 1 control, then the hydrogen θ = 0.5 point, compared against the portfolio and against a named experiment.

Items 1–4 are classical and publishable. Item 5 is far-FT.

**23. NISQ plausibility.** None. Depth is at least 1e9 Toffoli-equivalent even at η = 32, and thermal preparation needs coherent phase estimation or a Lindbladian sampler.

**24. FT need.** Full fault tolerance at a later-FT rate (≥ 1e6–1e8 Toffoli/s aggregate) is needed even for the validation rung. It needs about 500–3000 logical and about 1e6–1e7 physical qubits.

**25. Publication contribution.**
- Independent of any quantum outcome:
  1. the information-gain analysis (real-frequency S vs ITCF for XRTS inference);
  2. the first multi-family classical comparison of S_ee(q,ω) for warm dense hydrogen at θ ≤ 0.5 with a θ = 1 control;
  3. a sign and extrapolation-error map for ξ/Taylor-ξ at N = 14–32.
- Conditional:
  4. the first end-to-end resource estimate for thermal S_ee(q,ω) at XRTS geometries with costed thermal preparation and a UEG–PIMC validation protocol.
- The scoop risk argues for writing up items 1–3 as they complete.

**26. Usefulness beyond quantum computing.** Items 1–3 of 25 are directly useful to XRTS analysis and to TDDFT kernel development, whatever happens on the quantum side. They also address the WDM roadmap's validation needs (arXiv:2505.02494, 2604.23687).

**Paper thesis.**

> We would test whether the correlated real-frequency electronic dynamic structure factor S_ee(q,ω) of warm dense hydrogen at r_s ≈ 2 and θ = 0.25–0.5 can be formulated as a first-quantized plane-wave linear-response (density-kick) simulation started from a costed correlated thermal state and validated against quasi-exact PIMC F(q,τ) on the uniform electron gas at θ ≥ 0.5.
>
> Unlike previous approaches, which either need analytic continuation of PIMC data that the fermion sign problem makes unavailable below θ ≈ 0.5, or use TDDFT exchange-correlation kernels validated only at θ ≥ 1, the quantum method evolves the bare Coulomb Hamiltonian in real time with no xc kernel and no analytic continuation.
>
> Against tuned classical baselines (LR-TDDFT with ALDA/PBE/ESA/PIMC-derived/f-sum-corrected kernels and Liouville–Lanczos, RT-TDDFT, finite-T GW/BSE, Chihara/average-atom, ξ/Taylor-ξ PIMC, and RPIMC/variational-NN sum-rule constraints), the quantum method could exhibit an accuracy-class computational/resource advantage (category 3), meaning a controlled-error lineshape at a state point where those families disagree beyond experimental error. This would hold under resource scaling polynomial in electron number, resolution and precision (S·G ∝ η^{1–2}/(Δω² ε²)), compared with exponential sign-problem scaling for exact classical methods, and it is conditional on a bounded-cost correlated thermal-state preparation.

**Fallback branch** (same direction, not a separate slot): non-equilibrium, XFEL-isochorically heated two-temperature XRTS (arXiv:2402.09005). PIMC and ITCF do not apply there by construction, which makes a multi-family wall (RT-TDDFT vs G1-G2 NEGF) more plausible. The heated initial state is an L6 model-floor risk that must be quantified first. Pre-register this branch only if K-C01a fails because of equilibrium Laplace equivalence rather than information limits.

---

## 11. Detailed analysis: Finalist 2, not filled

No second candidate cleared the bar. The closest was the **C14 redesign lane**, which selection ranked second and marked not eligible.

**The lane.** Long-time (t·J_par ≈ 128–600), finite-T (T ≈ 0.25 J_par) local, powder-averaged S(ω) of the π-flux dipolar-octupolar XYZ model at L ≥ 3, convolved with µeV backscattering resolution. It would decide between incompatible published parameter sets for Ce2Sn2O7 (Porée et al., arXiv:2304.05452): J± = −5.2 vs −17 µeV, and ring exchange 0.73 vs 12.4 µeV. It includes a vacancy arm.

**Why it is not a finalist:**
- The redesign has never been audited as a problem.
- Ce2Sn2O7 orders at about 40 mK (arXiv:2607.12274), which questions the QSI model itself.
- Powder local S(ω) discriminates weakly, and samples depend on the growth route.
- The vacancy floor persists (arXiv:2609.28643).
- Estimated cost is about 6e15 T.
- Practical significance is limited to one neutron-scattering community.

**What would promote it.** A pre-registered classical decision-flip test: do ED32, GMFT and SCEBR rank the two Ce2Sn2O7 parameter sets differently after IN16B resolution convolution, with a vacancy arm? The redesign would also need its own triple audit, preferably merged with reserve C17 (Gibbs-only targets: thermal Hall, sign of thermal expansion, arXiv:2608.11305). For that pair, Gibbs preparation is at least the correct bottleneck.

---

## 12. Detailed analysis: Finalist 3, not filled

No third candidate cleared the bar. The residuals that survived audit are all category 1 (quantum usefulness) or have no downstream consumer:

| Residual | Cost | Why not a finalist |
|---|---|---|
| C44: exact 2D two-component Rytova–Keldysh e-h dynamics at η 64–128, one scalar (n(k,t) or g_eh(r,t)), as ground truth for GKBA self-energies | 3e11–3e12 Toffoli (best in set) | Category 1 only. GW+Fan-Migdal NEGF already reproduces the experiment. The experimental disagreement (Chernikov 2015 gain vs Dogadov 2026 no gain vs Mohapatra 2026 discontinuous) is between experiments, not solvers. Phonon/valley floor. Coherent-pump representation defect. |
| C41: full-3D η = 3–4 near-IR strong-field triple/double ratio | 1e12–1e13 Toffoli | Real exact wall at η ≥ 4 but no consumer. Two approximate families already match data. Intensity-calibration floor. |
| C07: ab initio real-frequency spin-relaxation width of warm neutron-rich matter with tensor forces | 1e14–1e19 per state point, plus uncosted thermal preparation | Low decision leverage (≤ 5% on luminosities). A smeared classical twin exists. |

**What would promote C44.** Both of the following must be shown: a TMD observable where the classical self-energy families disagree by more than the phonon/parameter floor, and a phonon-inclusive formulation that stays within S·G ≤ 1e12.

**Where to look next.** The selection lead recommends drawing slots 2–3 from a new audit round (C14-redesign + C17, then other reserves: C02, C15, C19, C32, C34). The round should apply an up-front filter: the decision-relevant observable must sit inside the classical wall, and S·G must be ≲ 1e13 before shortlisting.

---

## 13. Side-by-side comparison (qualitative; no single score)

"Surviving form" means the sharpened formulation after audit. Only C01 is eligible.

| Dimension | C01 WDM S_ee(q,ω) (finalist) | C14 π-flux QSI (µeV redesign) | C44 2D e-h plasma (residual) | C41 multi-electron ionization (residual) | C07 hot n-rich response (residual) | C04 kilonova opacity |
|---|---|---|---|---|---|---|
| Novelty evidence (scoped) | B; solid for the exact problem but thin (Sandia intent announced) | B; only 1D/2D quantum S(q,ω), 3D Rydberg ground-state proposals | B bordering C (arXiv:2606.04295) | B; mechanism already published | B; T = 0 quantum response and nuclear EFT costs exist | B; quantum dipole spectral-function primitive exists |
| Classical difficulty | Exact PIMC variants fail at θ ≤ 0.5; approximate families unvalidated and uncompared there | Plausible multi-family wall at long times, unmeasured | Exact dynamics out of reach, approximations suffice | Exact wall at η ≥ 4 IR | Sign-free lattice covers the static part | Valence FCI classically exact |
| Quantum mechanism strength | Exponential vs exact finite-T fermions; polynomial vs TDDFT; thermal preparation unsolved | Cheap local dynamics; Gibbs plausible at T ≈ 0.25 J | Exponential vs exact; mixed initial state; coherent pump not native | Exponential memory; rare channels quadratic only | Exponential only where cost explodes | Matched primitive aimed at a non-bottleneck |
| Practical importance | High (ICF/HED diagnostics), conditional on a consumer | Low–moderate | Moderate (methods); low (decision) | Low | Low for this piece | Moderate field, low leverage |
| Benchmarkability | Excellent (exact UEG Laplace check) | Fair (0-flux QMC+SAC; powder data) | Fair (small-N ED/NQS) | Good (He exact) | Fair (unitary gas, virial) | Good (NIST levels) |
| Scaling potential | η 32 → ≥131; θ 1 → 0.25 | L, t_max, T | η, density | η 2 → 6, wavelength | L³, Y_p | f-occupation, core size |
| Resource feasibility | UEG 4e13–9e14 (later-FT); H 7e16–1.6e18 | ~6e15 T | 3e11–3e12 scalar; spectra 1e14–1e15 | 1e12–1e13 scalar; marginals ~1e16 | 1e14–1e19 per point | 6e13–5e18 per ion per T |
| Classical-adversary risk | Moderate–high (pseudo-fermion, Taylor-ξ, variational NN, sum rules advancing) | High | Very high | Very high | Very high | Very high |
| Literature saturation | Classical dense; quantum side empty but about to be occupied | Classical dense; quantum empty | Classical saturated; quantum just opened | Classical saturated for η ≤ 3 | Classical static side saturated | Classical saturated |
| Publication potential | High in any outcome (information analysis, classical wall map, resource estimate) | Moderate (classical decision-flip test) | Moderate | Low–moderate | Low | Low–moderate (likely negative) |

---

## 14. Novelty audits

### 14.1 C01 (finalist)

- **EXACT PRIOR WORK.** None found. The closest item is the announced intent in Nelson & Baczewski (arXiv:2605.22920): "Ongoing work is aimed at extending the ROQAM at nonzero temperature to … calculating linear response functions of warm dense matter". It is not a paper.
- **NEAREST QUANTUM WORK.**
  - Rubin et al. arXiv:2308.12352 (stopping power)
  - Pathak, Kononov, Baczewski arXiv:2607.02811 (opacity, spectral readout, no Thomson/XRTS/structure factor in the full text)
  - Kunitsa et al. arXiv:2508.15935 (T = 0 active-space EELS DSF, 100 logical qubits, 3.25e8 T)
  - Cruz, Wild, Bañuls, Cirac doi:10.1103/lpz2-j7vg (finite-T response)
  - Babbush et al. arXiv:2301.01203
  - Roggero & Carlson arXiv:1804.01505
  - Becker, Rouzé, Salzmann arXiv:2604.15263
  - spin DSF on hardware (arXiv:2603.15608, 2607.07138, 2607.02673)
- **NEAREST CLASSICAL WORK.**
  - Dornheim et al. arXiv:2402.19113 (PIMC matches NIF Be XRTS)
  - arXiv:2509.11317 (Taylor-ξ)
  - arXiv:2507.00688 (H at θ 0.5/0.25, TDDFT only)
  - arXiv:2604.25735 and 2211.00579 (model-free ITCF)
  - arXiv:2603.27212 (UEG S(q,ω) via MaxEnt/PyLIT)
  - arXiv:2502.04921 (Liouville–Lanczos)
  - arXiv:2507.18540 (variational thermal H)
  - arXiv:2205.13595 and 2311.05611 (real-frequency diagMC)
- **TESTED.**
  - Quantum: stopping power, opacity and conductivity resource estimates; T = 0 electronic DSF (active space); finite-T response primitives on toy models; spin DSF vs INS.
  - Classical: PIMC ITCF vs NIF Be XRTS; PIMC+AC S(q,ω) for the UEG; LR-TDDFT vs PIMC for H at θ = 1; model-free ITCF thermometry.
- **NOT TESTED.**
  - Any quantum algorithm or resource estimate for thermal S_ee(q,ω) of WDM at XRTS q with costed thermal preparation.
  - Any quantum vs PIMC F(q,τ) comparison.
  - The information gain of real-frequency S over ITCF.
  - A multi-family classical comparison at θ ≤ 0.5 for H.
- **WHY MATERIAL.** It combines a thermal ensemble, continuum electrons and finite q, a different bottleneck from T = 0 EELS, stopping power or dipole opacity. It has the only exact classical cross-check among HED quantum-dynamics targets. Its output feeds an XRTS inference with documented model disagreements (free-bound terms, doi:10.1002/ctpp.70149; f-sum violations of Chihara models, arXiv:2607.25481).
- **WHY NEW PAPER.** It would be the first end-to-end costing with a UEG–PIMC validation protocol, plus the classical information and wall-map results. It is an application/regime/benchmark contribution, not a new algorithm.
- **Scoped negative statement.** In the arXiv API and abs/html pages (including full texts of 2607.02811, 2605.22920, 2605.07722, 2505.02494, 2511.14643, 2508.15765), OpenAlex search and cited-by lists (Rubin 2024, Babbush 2023, Roggero & Carlson 2019, Dornheim PRL 2018 and Nat Commun 2025), Semantic Scholar cited-by lists (2508.15935, 2605.22920, 2301.01203), Crossref and OSTI records, searched through 2026-09-28, we found:
  - quantum protocols for WDM stopping power, opacity and conductivity;
  - a T = 0 active-space electronic DSF algorithm;
  - finite-T quantum response and Green's-function methods, one of which announces WDM linear-response work;
  - spin-chain DSF hardware demonstrations.

  We found no study of a quantum-computed thermal electronic S_ee(q,ω) of warm dense matter at XRTS wavevectors (D) compared against PIMC plus analytic continuation (E) or model-free ITCF plus LR/RT-TDDFT (F). Coverage gaps: no WebSearch, no company or group pages, OpenAlex 429 on some cited-by lookups.

### 14.2 Non-finalists (condensed, from the audit files)

| ID | Exact prior work | Nearest quantum work | Nearest classical work | Not tested (material gap) | Scoped negative statement (sources as in the audit file, through 2026-09-28) |
|---|---|---|---|---|---|
| C14 | None found | 1D quantum S(q,ω) vs INS (2603.15608, 2607.07138); Google 2D finite-T magnon response (2607.13301); 3D QSI Rydberg ground states (2301.04657, 2502.00836) | GMFT (2301.05240), SCEBR (2401.09551), ED+MD (2201.00828), Lanczos+MC (2108.01096), QMC+SAC 0-flux (2510.14813) | Beyond-GMFT treatment of the Q = (1,1,0) polarization anomaly; a common-size multi-solver comparison | No quantum finite-T polarized S(q,ω) study of 3D DO π-flux QSI vs GMFT/SCEBR/ED or 3D sparse-Pauli/BP-TN/t-VMC was found |
| C44 | Klymenko et al. arXiv:2606.04295 (SBE absorption/gain on a QC, HF level) | First-quantized dynamics (2105.12767, 2301.01203, 2603.19007) | GW+Fan-Migdal GKBA (2604.06897); real-time GW (2109.15209); G1-G2 | Exact correlated 2D e-h dynamics vs GW/T-matrix/G1-G2 at the crossover | No correlated quantum simulation of 2D e-h plasma across the exciton Mott crossover vs NEGF/SBE was found |
| C41 | None found | Kharazi 2602.20234 (photoemission); Chan et al. 2202.05864 (grid ionization, ≤ 36 qubits); CAP on QC (2205.10543) | tSURFF He (1511.06655); TDCC Li (PRL 93, 053201); ECBB (doi:10.1088/1361-6455/ae2e65); Thiede (1804.05773) | η ≥ 3 joint-momentum quantum sampling vs RMT/TD-CASSCF/RASCI/MCTDHF/TDCC | No such study was found |
| C07 | None found | Roggero–Carlson response (1804.01505); GIT (2004.04889); Watson nuclear EFT costs (2312.05344) | Ma et al. static S_A, S_V at N3LO (2306.04500); CC-GIT T = 0 (2407.20986); virial (1611.05140) | Finite-T real-frequency spin/spin-isospin response of hot asymmetric matter with tensor forces | No quantum computation or quantum-vs-classical study of finite-T S_A/S_V of hot asymmetric matter was found |
| C04 | None found (arXiv query "kilonova AND quantum computer" returned 0) | Pathak et al. 2607.02811 (dense Fe, non-relativistic); quantum XAS dipole spectral functions (2405.11015, 2506.15784) | Calibrated FAC (2507.07785); LANL binned opacity (1904.08781); Kato et al. (2501.13286) | Quantum thermal spectral-function opacity vs calibrated CI or KPM on large relativistic CI | No such study was found |

---

## 15. Classical baseline audits

### 15.1 C01: required portfolio and status

| Family | Demonstrated reach | Where it stops | Role in K-C01b |
|---|---|---|---|
| Direct fermionic PIMC | UEG θ ≥ 0.75; Be small N | UEG θ = 0.5: sign 3.6e-3 at N = 8, ~1e-6 at N = 66 | Measure the sign at N = 14–32 |
| ξ / Taylor-ξ / fictitious particles | NIF Be (θ ≈ 2.7); UEG N ≤ 1000 static | "breaks down for Θ = 0.5" | Measure the extrapolation error |
| Pseudo-fermion, backflow, learned sign | UEG energies to θ = 0.0625 (N = 33) | Energies only so far | Watch: could close the ITCF gap |
| PIMC+AC (MaxEnt, PyLIT, dynamic LFC) | UEG S(q,ω), N = 14 finite-size-free | Inherits the sign wall | UEG validation reference |
| ESA LFC | UEG 0 ≤ θ ≤ 4, 0.7 ≤ r_s ≤ 20 | UEG only | Kills the UEG-as-advantage claim |
| Real-frequency diagMC | UEG r_s 1–4, all T | HF-BSE ladder class | Kills the UEG-as-advantage claim |
| ph-FT-AFQMC | UEG θ ≤ 0.5, r_s ≤ 2 (energies) | No dynamics shown | Optional member |
| Variational NN free energy | Warm dense H, θ ≈ 0.07–0.43, N ≤ 54 | Thermodynamics only | Static sum-rule inputs; possible classical seed |
| LR-TDDFT / Liouville–Lanczos / f-sum-corrected | H θ = 1: "striking agreement" with PIMC | Unvalidated below θ = 1; ALDA/PBE deviate at q ≳ 3 q_F | Core members, multiple kernels |
| RT-TDDFT, mixed stochastic TDDFT | Al, Be, CH DSF | Kernel dependence | Members |
| Finite-T GW(/BSE) | WDM conductivity | S(q,ω) not yet done | Member if implementable |
| Chihara / average-atom | Be ambient/compressed | Model-form error | Member (expected outlier) |
| Model-free ITCF | T, normalization, Rayleigh weight without a model | Not a forward model for n_e, Z, ν | Supplies T in K-C01a |

The UEG at θ 0.25–0.5 is classically covered. The wall for hydrogen is a validation gap until K-C01b is run.

### 15.2 Other candidates

- **C14.** GMFT, SCEBR, ED32 and QMC agree on the spinon-continuum position. Linked-cluster expansion fits energy-integrated scattering down to 0.05 K (Smith et al. PRX 15, 021033, arXiv:2407.07640). BP-TN and t-VMC have not been tried at t·J_par ≤ 13, which is exactly their strong regime.
- **C44.** GW+Fan-Migdal GKBA reproduces experiment. The GKBA failures that are documented occur only in lattice models, with KBE/DSL cross-checks available.
- **C41.** tSURFF (He), TDCC (Li), ECBB, the reduced-dimension model and CTMC all match their respective data.
- **C07.** Lattice N3LO static S_A, S_V; virial; Hansen–Lupo–Tantalo smeared spectra.
- **C04.** Calibrated and Bayesian-optimized FAC; CI+MBPT; pCI and NN-selected CI; KPM on valence FCI.

In every non-finalist, at least one tuned classical family already answers the decision-relevant question.

---

## 16. Quantum mechanism analysis

- **The shared primitive and why it is unsettled.** All six shortlisted candidates share one primitive: a real-time or spectral quantum correlator, or a Born-rule sample of a many-body continuum or thermal state. None is an argmin over a classical landscape (L3), and none rests on Grover or amplitude estimation. That was a deliberate filter, and it held. It did not save the candidates, because the audits found three further failure points in the same primitive.
  1. **Thermal-state preparation** (C01, C07, C14). There is no bounded-cost correlated Gibbs preparation for 3D degenerate Coulomb fermions, a U(1) spin liquid below the spinon gap, or pionful nuclear matter. The one rigorous Coulomb Gibbs mixing result covers only distinguishable particles in a trap (arXiv:2604.15263). Mermin/HF determinant starts bias the correlation physics being measured.
  2. **Readout noise.** A linear-response signal on a many-particle background (C01), rare channels (C41), or per-bin line statistics (C04) push S to 1e5–1e8. Amplitude estimation recovers only a quadratic factor and needs coherent (purified) preparation.
  3. **Representation.** A fixed-particle-number first-quantized register cannot represent a coherent pump (C44). Absorbing boundaries destroy the ionized flux one wants to sample (C41). Plane-wave cutoffs for core electrons break the bare-Coulomb premise (C01 CH rung).
- **C01 in particular.**
  - Exponential separation holds only against exact finite-T fermion methods in the sign regime.
  - Against TDDFT the separation is polynomial in basis size (Babbush et al. 2023; Chen & Chan, PRL 137, 130601, 2026).
  - The density-kick plus position-snapshot readout avoids the (η/ε)² Hadamard-test penalty and gives all reciprocal-lattice q per shot. It still needs Heisenberg-limited estimation to approach the screen.

---

## 17. Resource / break-even analysis

| ID | G per circuit (Toffoli) | S·G per useful state point | Logical qubits | Screen (S·G ≤ 1e12) | Break-even vs strongest classical |
|---|---|---|---|---|---|
| C01 UEG rung | 5e9–1.2e11 | 4e13–9e14 (Heisenberg-limited) | ~500–800 | 1.5–3 orders over; later-FT | None in cost; validation only |
| C01 H rung (η = 128) | 1.6e12–3.6e13 | 7e16–1.6e18 (plus snapshot and state-point multipliers) | ~2700–3000 | 5–6 orders over | Accuracy class only, if K-C01b passes |
| C14 as specified | ~3e6 T per correlator circuit; preparation dominates | 7e13 (heuristic preparation) to 3e16–4e18 (Gibbs sampler) | ~0.5–1e3 | Over | None for the decision |
| C14 redesign | not separately costed | ~6e15 T | ~0.5–1e3 | Over | Unknown |
| C44 | 3e8–4e10 (η 32–128) | Scalars 3e11–3e12; spectra 5e14–1e15; n_M(t) 1e17–5e18 | ~1e3–2.3e3 | Scalars pass; spectra fail | Exact break-even at η ≈ 6 (physically empty); none vs NEGF |
| C41 | 6e8–2e10 | Ratio 3e12–1.2e14; marginals 4e14–1.6e16 | 400–1000 | Over | Beats exact only at η ≥ 4 IR; never approximate methods |
| C07 | ~1e10 per trajectory | 1.8e14–4e15 (up to 2e19 with Gibbs sampler) | 1.5e3–6e3 | Over | None at L = 6–10 |
| C04 | 1e9–1e11 per QPE | 6e13–5e18 per ion per T | ~2e3 (FeMoco-class) | Over | Needs > 1e13–1e14 determinants per block |

Runtime conversions use 170 µs/Toffoli for a single factory (arXiv:2011.04149) or 1e6–1e8 Toffoli/s aggregate. Simulator time is never counted. In every row, measurement and state preparation dominate over Hamiltonian simulation. The quadratic-speedup trap (lesson L3) was avoided by design, but the cost ended up in sampling instead.

---

## 18. Red-team analysis

### 18.1 C01: Hostile Reviewer 1 (classical/technical)

Verdict: **not fatal overall, but two sub-claims are dead.**

**Fatal to sub-claims:**
1. **UEG as an advantage target.** ESA covers 0 ≤ θ ≤ 4, real-frequency diagMC covers r_s 1–4 at all T, and FT-AFQMC and pseudo-fermion PIMC cover the energies. The UEG becomes validation only.
2. **The CH rung.** K-shell cutoff or pseudopotentials, plus the resource kill. It is dropped.

**Fixable objections, and where each is incorporated:**

| Objection | Incorporated in |
|---|---|
| Structural contradiction (exact rung without advantage; advantage rung without check) | 10.19 |
| Hydrogen wall is a validation gap, not a failure | 10.6 |
| Classical correlated thermal states exist (arXiv:2507.18540, RPIMC) | 10.5, 10.7 |
| Untried classical routes (Liouville–Lanczos, f-sum-corrected TDDFT, RT-TDDFT, finite-T GW/BSE, sum rules) | 10.8 portfolio |
| Sum-rule-constrained limits; θ = 0.25 lineshape below NIF resolution | 10.20 |
| K-C01a mis-framed on T | 10.21, Section 19 |
| Continuation and feature-count cap (arXiv:2609.07208) | 10.19 |
| No consumer found (Davis 2016 consistent with DFT-MD; XFEL H data non-equilibrium) | consumer gate, 10.21 |
| Straw-man comparator | 10.8 |
| q-window vs η; BO multiplier | 10.2, 10.12 |
| Thermal preparation unsolved; FULL vs ABLATION if seeded | 10.7, 10.22 |
| Resource basis (Rubin inconsistency, quantum FMM) | 10.12 |
| Scoop | 10.25 |

### 18.2 C01: Hostile Reviewer 2 (prior art / significance)

Verdict: **wounded, no fatal objection.** Significance is the main weakness.

**Findings:**
- Algorithmic novelty is thin: every component is published (Rubin, Babbush, Kunitsa, the Roggero series, Nelson & Baczewski, Becker et al.).
- Scoop risk is high:
  - the Sandia DOE FES program;
  - Bobrow et al. thermal-preparation costing, in preparation and not on arXiv as of 2026-09-28;
  - Kononov and Baczewski co-author XRTS analysis with the Dornheim group;
  - Google's Grand Challenge lists stopping power at 1e15 Toffoli, so an XRTS variant would be a small step.
- Practical value outside quantum computing is not shown:
  - The XRTS overview names non-equilibrium as "the most difficult frontier" (arXiv:2604.23687).
  - The measured D data in this regime (Regan et al., PRL 109, 265003, 2012: T_e = 8 ± 5 eV) are limited by experiment.
  - Where real-frequency theory did change a conclusion (EuXFEL Al, arXiv:2509.10107), classical TDDFT settled it.
  - PIMC shows decreasing DSF sensitivity to ionization at large angles (arXiv:2503.14014).
- The wall is single-group.
- Degenerate-fermion Gibbs preparation remains open.

**Required revisions, incorporated:**
- K-C01a first on real XRTS configurations (OMEGA shocked D; OMEGA planar-shock D at 0.7–0.8 g/cc; LCLS/FLASH/EuXFEL H jets): Section 19.
- Claim repositioning (category 3 vs exact dynamics as the anchor; practical claim "accuracy beyond adiabatic kernels at bounded cost"; UEG validation only): 10.9 and thesis.
- Cite and differentiate the prior art: 10.15, 10.17, 10.18.
- Multi-family stress test: 10.8.
- Thermal preparation as an explicit open item: 10.7, Section 23.
- Priority management: 10.25.
- Non-equilibrium XFEL fallback: 10, fallback branch.
- Close search-coverage gaps before submission: Section 23.

### 18.3 Adjudication and rejections

- **Adjudication.** No adjudication was recorded (adjudication = null). Neither reviewer declared C01 fatally flawed as a whole, so no contested fatal objection needed resolution. The required revisions of both reviewers were merged directly. Where they overlapped, the stricter version was taken. For example, Reviewer 1's reframing of K-C01a onto (n_e, Z, ν), because T is model-free, supersedes the original (n_e, T) framing.
- **Candidates rejected by the red team: none.** C01 was the only candidate sent to red team. The other five were rejected earlier, at audit and selection (Sections 7, 8), which is why no red-team rejections appear.

---

## 19. Recommended first experiment

**C01: K-C01a, information gate.** Pre-register in `experiments/preregistered/` before running.
- **Hypothesis H1.** An exact real-frequency S_ee(q,ω) narrows the posterior on (n_e, Z, ν) by at least 2x beyond (best classical forward model + model-free T from ITCF detailed balance) at a named instrument resolution.
- **Null H0.** Narrowing is below 2x. Noise-free degeneracy of the kind reported in arXiv:2408.15346 (factor 3 in ν_DC; factor 22 in two-angle σ_DC) is taken as the reference null behaviour.
- **Configurations.**
  - UEG at r_s ∈ {2, 3, 4}, θ ∈ {0.25, 0.5, 1}.
  - Then real XRTS geometries: OMEGA shocked D (Regan 2012), OMEGA planar-shock D, and LCLS/FLASH/EuXFEL H jets.
  - Instrument functions: NIF-like 5–20 eV FWHM and XFEL-like 0.1–1 eV.
  - Noise: 5–10%.
- **Forward models.**
  - RPA, ESA static LFC, and a dynamic-LFC envelope bounded by PIMC+MaxEnt/PyLIT spectra at θ ≥ 0.5 (the proxy for "exact").
  - Best-available classical TDDFT-type models for the hydrogen geometries.
- **Metric.** Posterior width ratio and posterior shift (in σ) for (n_e, Z, ν), full-S vs (classical forward model + ITCF-T). Use MCMC or Fisher analysis.
- **Kill criterion.** Width ratio < 2 and forward-model-spread shift < 0.5σ at every XRTS-relevant q and both resolution classes.
- **Compute.** Laptop, days. It fits the program's compute policy (≤ 95% CPU/RAM; ≤ 3 workers per the host-memory note).
- **Second experiment, conditional on a pass: K-C01b.** About 1e4 core-hours. The portfolio in 10.8 at hydrogen r_s = 2, θ = 0.5/0.25, with a θ = 1 control. Escalate only if the inter-family spread after convolution exceeds experimental error where ξ methods verifiably fail.

**Slots 2–3.** No first experiment is recommended, because no finalist exists. The pre-test in Section 11 (the Ce2Sn2O7 decision flip) is the cheapest route to reopening a second slot.

---

## 20. What constitutes a genuine quantum advantage

The program's six claim categories, applied to C01:

| Category | Applicable to C01? | What would be required |
|---|---|---|
| 1. Quantum usefulness | Yes (fallback) | A quantum-computed S_ee changes an XRTS inference of (n_e, Z, ν) at a real experiment, validated at the UEG/θ = 1 controls. No cost claim. |
| 2. Empirical quantum advantage | Not in scope before far-FT hardware | Hardware execution beating the tuned portfolio at matched accuracy. Simulator results never count. |
| 3. Computational/resource advantage | **Primary target** | At a named state point, every classical family either verifiably cannot run (sign, extrapolation breakdown) or disagrees beyond experimental error. The quantum result has controlled error, passes the PIMC validation, and has bounded, stated resources including thermal preparation. Comparison against "exact finite-T dynamics" alone does not qualify. |
| 4. Sampling advantage | No | The output is an expectation-value spectrum, not a sample from a hard distribution. Position snapshots are an internal readout device. |
| 5. Hardware advantage | No | No hardware-specific claim. |
| 6. Theoretical/provable advantage | No | No proven separation for this physical instance. Efficient correlated fermionic thermal-state preparation is not established. |

None of the following counts on its own: agreement with PIMC where PIMC works; beating a single TDDFT kernel; beating mean field; a larger Hilbert space; simulator speed; fewer iterations.

---

## 21. What would falsify each

**C01.** Any one of the following ends or demotes the direction:
1. K-C01a: posterior narrowing below 2x (L5). Kill, unless the non-equilibrium branch is pre-registered for a Laplace-equivalence reason.
2. K-C01b: inter-family spread below experimental error at hydrogen r_s = 2, θ 0.5/0.25, with the θ = 1 control passing (L7). Kill.
3. Classical closure. Pseudo-fermion, Taylor-ξ, backflow or learned-sign PIMC delivers the ITCF at θ ≤ 0.5 for N ≥ 32, or variational-NN or RPIMC plus sum rules pins S_ee within error. The wall has moved: kill.
4. Thermal preparation. No bounded-cost correlated preparation exists at small η, or the bias exceeds the discriminating signal (L6). Kill the category-3 claim; category 1 at most.
5. Resources. A corrected estimate (Rubin inconsistency resolved, FMM costed) puts the UEG rung at 1e16 or more. Record it as resource-killed.
6. No consumer: no equilibrium XRTS experiment at this state point exists or is planned. Record "no consumer" and demote to a methods benchmark.
7. Scoop. A Sandia or Google preprint of thermal S_ee(q,ω). This does not falsify the science, but it reduces novelty to replication or extension, and the classical information and wall-map papers remain.

**Non-finalists.** They are already falsified as specified (Section 8). For each, the reopen conditions are:
- C14: the Ce2Sn2O7 decision-flip test passes.
- C44: a classical solver disagreement beyond the phonon/parameter floor, and a phonon-inclusive S·G ≤ 1e12.
- C41: an η ≥ 3 joint observable that is measured and where the approximate families disagree beyond error.
- C07: a lineshape-specific supernova sensitivity above 5%.
- C04: evidence that non-perturbative core-valence correlation moves binned opacity beyond the NLTE and calibration uncertainty.

---

## 22. Publication contribution

**C01, in decreasing certainty of publication:**
1. A classical information-theoretic analysis: real-frequency S vs ITCF for XRTS inference, including instrument function and degeneracy. This is publishable either way.
2. The first multi-family classical comparison of S_ee(q,ω) for warm dense hydrogen at θ ≤ 0.5, with a θ = 1 control and measured sign/extrapolation error. It maps the wall or shows that no wall exists.
3. The first end-to-end fault-tolerant resource estimate for thermal S_ee(q,ω) at XRTS geometries, with costed thermal preparation and a UEG–PIMC Laplace validation protocol.
4. Only if all gates pass: an accuracy-class category-3 demonstration at a named state point. This would be far-FT.

**Program-level (negative) contribution.** An audited map showing that, for real-frequency response of correlated continuum or thermal systems judged against real experimental consumers, the exponential separation is real but sits where decision value is low. Sampling and state preparation, not Hamiltonian simulation, set the cost. This extends the protein-program lessons (L3, L5, L6) to HED, nuclear, magnetic, AMO, atomic-data and semiconductor-optics settings.

---

## 23. Open questions

1. Does an exact real-frequency S_ee carry at least 2x posterior information over classical forward model plus ITCF-T at any available XRTS resolution? (K-C01a.)
2. At hydrogen r_s = 2, θ 0.5/0.25, do LR-TDDFT kernels, RT-TDDFT, finite-T GW/BSE, Chihara and sum-rule-constrained models disagree beyond experimental error? (K-C01b.)
3. Is there an equilibrium XRTS experiment, existing or planned, at r_s ≈ 2, θ 0.25–0.5 with 2–5 eV resolution and stated error?
4. Can a correlated thermal state of first-quantized degenerate Coulomb electrons be prepared with bounded cost? This covers microcanonical/ETH window error at small η, fermionic extensions of arXiv:2604.15263, and the forthcoming Bobrow et al. costing.
5. What does Rubin et al. 2024's per-a.u. cost actually equal, given the ~1.6e3x internal inconsistency? Does real-space quantum FMM (arXiv:2510.07380) change the Coulomb cost basis?
6. How quickly will pseudo-fermion, Taylor-ξ and variational-NN methods reach the ITCF at θ ≤ 0.5, N ≥ 32?
7. For the non-equilibrium XFEL branch, can the heated initial state be specified with an error below the solver disagreement (L6)?
8. Search-coverage gaps must be closed before any submission: WebSearch; company and group pages; OpenAlex cited-by for 2605.22920 and 2508.15935; theses and patents.
9. For slots 2–3, can any reserve candidate (C02, C15, C17, C19, C32, C34) or the C14 redesign pass the up-front filter: decision value inside the classical wall, and S·G ≲ 1e13?
10. Is there any physical, non-contrived Hamiltonian whose local minima are hard classically? (C19; arXiv:2309.16596 gives BQP-hardness only in general.)

---

## 24. Bibliography

These citations were verified during this workflow through an arXiv abstract, HTML or PDF page, the arXiv API, Crossref, OpenAlex or an OSTI record, as recorded in the `lit_work` audit notes. [L] marks items verified only from an arXiv API listing or title, not from a full abstract page.

### 24.1 Quantum algorithms and resources
- Babbush, McClean, Newman, Gidney, Boixo, Neven, "Focus beyond quadratic speedups for error-corrected quantum advantage", PRX Quantum 2, 010103 (2021), arXiv:2011.04149.
- Babbush et al., "Quantum simulation of exact electron dynamics can be more efficient than classical mean-field methods", Nat. Commun. 14, 4058 (2023), arXiv:2301.01203.
- Babbush et al., "The Grand Challenge of Quantum Applications", PRX Quantum 7, 020101 (2026), doi:10.1103/6r9l-lynr, arXiv:2511.09124.
- Becker, Rouzé, Salzmann, arXiv:2604.15263 (2026), Coulomb continuous-variable Gibbs sampling.
- Chen & Chan, PRL 137, 130601 (2026), doi:10.1103/v2ms-wmz1, arXiv:2508.15765.
- Chen, Kastoryano, Gilyén, arXiv:2311.09207 (quantum Gibbs sampling).
- Cruz, Wild, Bañuls, Cirac, "Quantum simulation of dynamical response functions of equilibrium states", doi:10.1103/lpz2-j7vg (2025).
- Flew & Kassal, arXiv:2510.02784.
- Gidney & Fowler, arXiv:1812.01238.
- Kunitsa, Dhawan, Fomichev, Arrazola, Zhang, Stetina, "Quantum Simulation of EELS for Battery Materials", arXiv:2508.15935.
- Lee et al., FeMoco resource estimate, PRX Quantum 2, 030305, arXiv:2011.03494.
- Low et al., arXiv:2211.09133 (Trotter complexity, UEG).
- Nelson & Baczewski, "Estimating Green's functions with a robust quantum Arnoldi method", arXiv:2605.22920.
- Pathak, Kononov, Baczewski, "An approach for calculating astrophysical opacities on quantum computers", arXiv:2607.02811.
- Pennati et al., post-Moore plasma roadmap, arXiv:2605.07722, doi:10.1145/3774895.3815547.
- Rall, PRA 102, 022408 (2020), arXiv:2004.06832.
- Roggero & Carlson, "Linear response on a quantum computer", PRC 100, 034610 (2019), arXiv:1804.01505.
- Roggero, Gaussian integral transform, arXiv:2004.04889 [L]. Baroni et al., arXiv:2111.02982 [L].
- Rubin, Berry, Kononov, Malone, Khattar, White, Lee, Neven, Babbush, Baczewski, "Quantum computation of stopping power for inertial fusion target design", PNAS 121, e2317772121 (2024), arXiv:2308.12352.
- Spagnoli, Lissoni, Roggero, arXiv:2507.22814; Quantum (2026), doi:10.22331/q-2026-09-02-2200.
- Su, Berry, Wiebe, Rubin, Babbush, "Fault-tolerant quantum simulations of chemistry in first quantization", PRX Quantum 2, 040332 (2021), arXiv:2105.12767.
- Quantum Gibbs/thermal-state preparation, arXiv:2303.18224. The paper is verified; its author list is not (see 24.8).
- Quantum real-space FMM, arXiv:2510.07380.
- Kosugi et al., arXiv:2605.29681 [L]; Eklund & Ananth, arXiv:2405.19599 [L]; Lee et al., arXiv:2206.05571 [L]; Ding, Li, Lin, arXiv:2404.05998 [L].
- Watson et al., nuclear EFT simulation costs, arXiv:2312.05344.
- Eklund et al., arXiv:2603.19007 (first-quantized pre-BO dynamics).
- Kharazi et al., arXiv:2602.20234; Chan et al., Sci. Adv. 2023, arXiv:2202.05864; Langkabel & Bande, arXiv:2205.10543; Mangin-Brinet et al., Quantum (2024), doi:10.22331/q-2024-04-08-1311; Wang & Krstic, arXiv:2112.06365.
- Klymenko, Goldozian, Hoang, Cole, Usman, arXiv:2606.04295.
- Fomichev et al., arXiv:2405.11015, arXiv:2506.15784.
- Baczewski, "Quantum computing and warm dense matter", SNL report, doi:10.2172/3028616.

### 24.2 Warm dense matter and XRTS (classical)
- Dornheim, PRE 100, 023307 (2019), arXiv:1906.00635 (sign problem).
- Dornheim, Groth, Vorberger, Bonitz, PRL 121, 255001 (2018), doi:10.1103/physrevlett.121.255001.
- Groth et al., PRL 119, 135001 (2017), doi:10.1103/PhysRevLett.119.135001.
- Dornheim et al., arXiv:2402.19113; Nat. Commun. 16, 5103 (2025), doi:10.1038/s41467-025-60278-3.
- Dornheim et al., Taylor-ξ, arXiv:2509.11317, doi:10.1103/53fr-mnm6.
- arXiv:2308.06071; arXiv:2311.08098; arXiv:2502.15288 [L]; arXiv:2607.06955; arXiv:2004.13429; arXiv:1810.12776; arXiv:2008.02165; arXiv:2101.05498 [L]; arXiv:2203.12288 [L].
- Chuna et al., arXiv:2503.20433, doi:10.1103/4d4b-kgtk; Chuna, Böhme, Dornheim, arXiv:2603.27212; PyLIT, CPC 319, 109904 (2026), doi:10.1016/j.cpc.2025.109904.
- Lee, Morales, Malone, arXiv:2012.12228 (ph-FT-AFQMC).
- LeBlanc, Chen, Haule, Prokof'ev, Tupitsyn, PRL 129, 246401 (2022), arXiv:2205.13595; Tupitsyn & Prokof'ev, arXiv:2311.05611.
- Xiong, Morresi, Xiong, arXiv:2603.28000, doi:10.1103/6bdz-8gmq; arXiv:2604.01963; arXiv:2607.15060; doi:10.1063/5.0340968.
- Morresi, Garberoglio, Xiong, Xiong, arXiv:2506.10113.
- Li, Xie, Dong, Wang, arXiv:2507.18540; dense-hydrogen neural free energy, PRL 131, 126501 (2023), arXiv:2209.06095.
- Moldabekov et al., arXiv:2507.00688, MRE 11, 025401 (2026).
- Moldabekov et al., arXiv:2502.04921, doi:10.1063/5.0263947; arXiv:2510.01875, npj Comput. Mater. 12, 168 (2026); arXiv:2609.18584.
- Kononov, Nguyen, Baczewski, arXiv:2511.14643, doi:10.1063/5.0312253; Kononov, Phys. Plasmas 2024, doi:10.1063/5.0198008.
- White, arXiv:2410.23599, doi:10.1088/2516-1075/adad24.
- Robinson, Kononov, Stanek, Baczewski, Schleife, Hansen, arXiv:2605.11308.
- arXiv:2508.17810; arXiv:2606.30123; arXiv:2609.07208; arXiv:2606.19205.
- Dornheim, Vorberger, Moldabekov, Böhme, arXiv:2211.00579; Nat. Commun. 13, 7911 (2022), doi:10.1038/s41467-022-35578-7; Sci. Rep. (2024), doi:10.1038/s41598-024-64182-6.
- Gawne et al., arXiv:2604.25735, doi:10.1007/s41614-026-00227-9; Gawne, Kononov, Baczewski et al., arXiv:2510.26747; Böhme et al., doi:10.1063/5.0304837.
- Gawne et al., PRB 109, L241112 (2024), arXiv:2403.02776.
- Hentschel, Kononov, Baczewski, Hansen, arXiv:2408.15346.
- arXiv:2504.04317 (DCI plasma jets); arXiv:2402.09005 (non-equilibrium XRTS).
- Dornheim, Bellenbaum, Gawne, Vorberger, Gericke, arXiv:2604.23687 (XRTS overview).
- Bespalov et al., arXiv:2509.10107, doi:10.1103/86cw-8wm5.
- Bellenbaum et al., arXiv:2503.14014.
- Regan et al., PRL 109, 265003 (2012), doi:10.1103/PhysRevLett.109.265003.
- Davis et al., Nat. Commun. 2016, doi:10.1038/ncomms11189.
- Fletcher et al., Front. Phys. 2022, doi:10.3389/fphy.2022.838524.
- Böhme, Fletcher, Baczewski et al., doi:10.1002/ctpp.70149; arXiv:2607.25481 [L]; xDAVE, arXiv:2604.27237, doi:10.1063/5.0340851.
- Bonitz et al., arXiv:2405.10627; Vorberger et al., WDM roadmap, arXiv:2505.02494, doi:10.1088/1361-6587/ae672c.
- arXiv:2302.06216; arXiv:2402.05214; Filinov, Levashov, Larkin, doi:10.1080/00268976.2024.2440477.
- OSTI doi:10.2172/3389315; doi:10.2172/3662053.

### 24.3 Quantum magnetism (C14)
- Gao et al., arXiv:2404.04207, Nat. Phys. 21, 1203 (2025), doi:10.1038/s41567-025-02922-9; Gao et al., PRL (2026), doi:10.1103/svt2-m3pp.
- Desrochers & Kim, arXiv:2401.09551; Hosoi et al., PRL 129, 097202, arXiv:2201.00828; arXiv:2108.01096; arXiv:2301.05240 (PRL 132, 066502); arXiv:2510.14813.
- Sanders et al., arXiv:2609.28643; arXiv:2607.12274; arXiv:2601.20766; arXiv:2601.03202 (PRL 136, 256703); arXiv:2501.08327; arXiv:2412.14773; arXiv:2608.11305; arXiv:2607.24679.
- Smith et al., PRX 15, 021033 (2025), arXiv:2407.07640; Porée et al., Nat. Phys. 21, 83, arXiv:2304.05452.
- Lee et al., arXiv:2603.15608; arXiv:2607.07138; arXiv:2607.02673; Google, arXiv:2607.13301; arXiv:2301.04657 (PRX 15, 011025); arXiv:2502.00836; arXiv:2603.28125.
- King et al., arXiv:2403.00910 (Science 2025); Tindall et al., arXiv:2503.05693; Mauron & Carleo, arXiv:2503.08247; arXiv:2609.01719; arXiv:2409.03097.
- Childs et al., arXiv:1711.10980; Yoshioka et al., arXiv:2210.14109.
- Bhardwaj et al., npj Quantum Mater. (2022), doi:10.1038/s41535-022-00458-2. The metadata is verified; the parameter values are not (see 24.8).

### 24.4 Semiconductor optics (C44)
- Dogadov et al., arXiv:2604.06897; Perfetto/Stefanucci et al., PRL 128, 016801, arXiv:2109.15209; arXiv:2512.14392; arXiv:2407.17077; arXiv:2607.18183; arXiv:2607.28417; arXiv:2305.07458.
- Schlünzen, Joost, Bonitz, PRL 124, 076601 (2020); arXiv:1909.11489; arXiv:2002.12717; arXiv:2312.15030; arXiv:2202.10061; arXiv:2606.10773; Schroedter et al., arXiv:2609.08932; Tuovinen, PRB 102, 115157 (2020).
- Mittenzwey et al., arXiv:2512.03198; Steinhoff et al., Nat. Commun. 8, 1166 (2017), doi:10.1038/s41467-017-01298-6; Chernikov et al., Nat. Photon. 9, 466 (2015), doi:10.1038/nphoton.2015.104; Mohapatra et al., arXiv:2601.17167; Erben et al., PRB 98, 035434 (2018).
- Nys, Pescia, Sinibaldi, Carleo, Nat. Commun. 15, 9404 (2024), arXiv:2403.07447.

### 24.5 AMO (C41)
- Zielinski, Majety, Scrinzi, PRA 93, 023406 (2016), arXiv:1511.06655; Zhu & Scrinzi, PRA 101, 063407 (2020), arXiv:1912.09250; Henrichs et al., PRA 98, 043405 (2018), arXiv:1808.03516; HeTDSE, Chin. Phys. B (2021), doi:10.1088/1674-1056/abe1a4.
- Colgan, Pindzola, Robicheaux, PRL 93, 053201 (2004); PRL 110, 063001 (2013), arXiv:1301.2350; Wehlitz et al., PRL 81, 1813 (1998), doi:10.1103/physrevlett.81.1813; Juranić et al., PRA 78, 033401 (2008).
- Plummer & Noble, J. Phys. Conf. Ser. 1412, 132053 (2020); Praill, Katsoulis, Emmanouilidou, J. Phys. B (2025), doi:10.1088/1361-6455/ae2e65; Thiede et al., PRA 98, 031401 (2018), arXiv:1804.05773; Efimov et al., PRA (2025), doi:10.1103/43wt-x129, arXiv:2410.16797.
- Young et al., Nature (2010), doi:10.1038/nature09177; Hikosaka et al., PRR (2026), doi:10.1103/x7zf-dx8m; arXiv:2311.15859; arXiv:2303.01029.

### 24.6 Nuclear astrophysics (C07)
- Ma et al., PRL 132, 232502 (2024), arXiv:2306.04500; Alexandru, Bedaque, Berkowitz, Warrington, PRL 126, 132701 (2021), arXiv:2008.02824; Niu & Lu, PRL (2025), doi:10.1103/pn99-6dxt; Lu et al., arXiv:1812.10928.
- Sobczyk, Jiang, Roggero, PRL 134, 192701 (2025), arXiv:2407.20986; Turro et al., arXiv:2306.16580.
- Horowitz et al., arXiv:1611.05140; Bedaque et al., arXiv:1801.07077; Guo et al., arXiv:2401.10737; Shin et al., PRC 109, 015804 (2024), arXiv:2306.05280; Roberts & Reddy, PRC 95, 045807, arXiv:1612.02764.
- Bartl, Bollig, Janka, Schwenk, PRD 94, 083009 (2016), arXiv:1608.05037; Burrows et al., arXiv:1611.05859; Melson et al., arXiv:1504.07631; Just et al., arXiv:1805.03953; O'Connor et al., arXiv:1712.08253.
- Hansen, Lupo, Tantalo, arXiv:1903.06476; Hoinka et al., PRL 109, 050403 (2012).

### 24.7 Atomic data (C04) and general context
- Flörs et al., arXiv:2507.07785; arXiv:2302.01780, doi:10.1093/mnras/stad2053; Kato et al., MNRAS 535, 2670, arXiv:2501.13286; Fontes et al., arXiv:1904.08781; arXiv:2502.13250; arXiv:2604.04362; Gillanders et al., arXiv:2512.24257.
- Pognan et al., arXiv:2202.09245, doi:10.1093/mnras/stac1253; arXiv:2408.02731; arXiv:2209.12759, doi:10.1093/mnras/stac2792; arXiv:2412.16688 (A&A 696, A32); arXiv:2508.18364; Shingles et al., ApJL 954, L41, arXiv:2306.17612.
- AMBiT, arXiv:1805.11265; pCI, arXiv:2410.06680; arXiv:2408.00477; Kozlov et al., PRA 105, 052805, arXiv:2202.02026; arXiv:2606.04868.
- FeMoco near-classical solution, arXiv:2601.04621; Fe4S4, arXiv:2603.28648.
- Dorfner, Brey, Burghardt, Ortmann, JCTC 2024, doi:10.1021/acs.jctc.4c00751.

### 24.8 Unverified or incompletely verified (not load-bearing unless stated)
- **[UNVERIFIED, in preparation]** Bobrow, Chien, Kononov, Nelson, Zhao, Baczewski, Kovalsky (2026), "Assessing the cost of thermal state preparation for quantum simulations of warm dense matter". Cited in arXiv:2607.02811, and not on arXiv as of 2026-09-28 in the searched queries.
- **[METADATA ONLY]** Kononov et al., OSTI doi:10.2172/3363975 (WDM conductivity resource estimates). No abstract was read.
- **[UNVERIFIED author list]** arXiv:2303.18224 (attributed from memory to Chen, Kastoryano, Brandão, Gilyén).
- **[UNVERIFIED]** Baczewski et al., PRL 116, 115004 (2016). Cited here via its citation in arXiv:2605.22920; not fetched.
- **[UNVERIFIED detail]** Exact r_s and T of arXiv:2205.13595 (the PDF was not text-readable); the state points of Davis et al. 2016.
- **[LISTING/TITLE ONLY]** Svensson et al., arXiv:2407.08875.
- **[UNVERIFIED value]** UEG correlation energy of about −0.045 Ha per electron at r_s = 2, which underlies the 8–16% Mermin-bias estimate.
- **[UNVERIFIED]**
  - Smith et al., PRX 12, 021015 (2022) parameter set
  - Bhardwaj et al. 2022 parameter values
  - Huang et al., PRL 120, 167202 (2018), cited from a reference list only
  - Ce2Zr2O7+x oxidation main-article metadata
- **[UNVERIFIED]**
  - Marciniak et al., Nature 2022 (optimization lens)
  - Berry et al. 2018 antisymmetrization cost
  - Li single-photoionization cross-section magnitude
  - Ar/Ne triple/single ratios
  - COLTRIMS triple-coincidence counts
  - intensity-calibration uncertainty for specific datasets
- **[UNVERIFIED]**
  - TMD parameters (r0 ≈ 3.8 nm; m_e ≈ 0.3, m_h ≈ 0.4)
  - Chernikov 2015 gain-threshold density
  - Siday et al. 2022 Mott-density value
  - NQS system sizes in arXiv:2403.07447
- **[UNVERIFIED]** Kilonova Doppler smoothing (Δλ/λ ≈ 0.1); Brewer configuration-energy systematics.
- **[UNVERIFIED author list]** Ehring et al., PRL 131, 061401 (2023). The title was verified.
- **[NO IDENTIFIER IN SOURCES]** Goings et al., PNAS 2022 (P450), from the brief's list of prior searches.
- **[ESTIMATES, NOT LITERATURE]** All Toffoli, qubit, shot and runtime figures not attributed to a specific table in a cited paper. They come from the auditors' arithmetic in `lit_work/audit_*_resources.md`.
