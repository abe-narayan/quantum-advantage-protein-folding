# Quantum-advantage candidates outside protein structure: final report

Date: 2026-09-28. Revised the same day after round 2. Status: LITERATURE AND DESIGN REPORT. No experiment has been run for anything in this report. Unless a citation is given, all numbers are order-of-magnitude estimates by the program's auditors. All novelty statements are scoped to the sources and dates in Section 3.

Working notes (query logs, arithmetic, per-citation verification): `research/reports/lit_work/`.
- **Round 1:** 12 discovery files, the pool/shortlist synthesis, 18 audit files, the selection file (`selection.md`) and 2 red-team files.
- **Round 2:**
  - 2 targeted discovery lenses: `round2_discovery_static_inside_wall.md` and `round2_discovery_short_time_dynamics_inside_wall.md`;
  - the prefilter, `round2_prefilter.md`;
  - 3 audit files, `audit_N01_{novelty,classical,resources}.md`;
  - the selection file, `round2_selection.md`.
- No round-2 red-team or adjudication file exists. No round-2 candidate was eligible for red team (Section 18.4).

---

## 1. Executive summary

**The brief** asked for exactly three practical, benchmarkable problems where an original quantum advantage could plausibly be shown and has not already been shown. It accepted a useful, materially distinct subsection of a studied field.

**After two rounds there is one finalist, not three.**
- **Round 1.**
  - 12 discovery lenses produced 50 distinct problems.
  - Six were shortlisted, and each received three independent audits: novelty, strongest classical adversary, and resources/break-even.
  - The selection lead found that only one cleared the bar, and only conditionally.
  - That candidate (C01) went to two hostile reviewers. Neither found a fatal objection to the whole candidate. Together they killed two of its sub-claims and required ten revisions.
- **Round 2.** The round-1 cross-cutting lesson was applied as an up-front filter with three conditions:
  - the decision-relevant value must lie inside the classical wall;
  - S·G ≲ 1e13 per useful state point;
  - the model floor must sit below the solver spread.

  Round 2 then ran as follows:
  - Two targeted lenses tested 17 static, ground-state and low-temperature target families and 12 short-time dynamics problems.
  - A prefilter re-sharpened the six round-1 reserves and the C14 redesign lane, and dropped all seven.
  - One new candidate, N01 (the multi-band fractional Chern insulator competition in hBN-aligned rhombohedral graphene), received the triple audit.
  - Selection marked N01 not eligible, so no round-2 candidate reached red team. **Round 2 adds no finalist.**
- **Slots 2 and 3 are left empty on purpose** (Sections 11, 12). Filling them would mean accepting one of the following:
  - a claim of quantum usefulness only (category 1);
  - an unmeasured decision flip;
  - a decision that lies inside the model floor.

  That is the false-hardness pattern that sank the protein program (lessons L1, L5, L6).

**Finalist C01, after red-team revision:** the correlated thermal electronic dynamic structure factor S_ee(q,ω) of warm dense hydrogen at r_s ≈ 2 and θ = T/T_F = 0.25–0.5, at X-ray Thomson scattering (XRTS) wavevectors. The uniform electron gas (UEG) serves only as an exact validation rung against path-integral Monte Carlo (PIMC).
- **Scoped novelty: category B.** Quantum protocols exist nearby for warm-dense-matter (WDM) stopping power, opacity and conductivity, and for the zero-temperature electronic DSF in an active space. In the sources searched, no quantum computation of the thermal electronic S_ee(q,ω) for XRTS was found, and no comparison against PIMC plus analytic continuation or model-free imaginary-time analysis.
- **Claim target: category 3 (computational/resource advantage), and only in accuracy class.** It would apply only at a named state point where a tuned classical portfolio either cannot run (the exact families hit the fermion sign problem) or disagrees internally beyond experimental error. Any gain over TDDFT in cost is polynomial.
- **Main risks:**
  1. Information value (L5). In equilibrium, the imaginary-time correlation function (ITCF) and S(q,ω) are a Laplace pair, and temperature is already extracted model-free.
  2. Single-family hardness (L7). The wall rests on one group's statement that PIMC is unavailable, with no multi-family disagreement documented.
  3. Correlated thermal-state preparation is unsolved. A Mermin-determinant start gives an estimated 8–16% temperature bias.
  4. Resources.
     - The UEG validation rung costs 4e13–9e14 Toffoli per state point. That is 1.5–3 orders above the round-1 screen of S·G ≤ 1e12, and about 0.6–2 orders above the round-2 upper edge of 1e13.
     - The hydrogen advantage rung costs 7e16–1.6e18 Toffoli before the Born-Oppenheimer snapshot multiplier.
  5. No equilibrium consumer experiment at this state point has been found.
  6. High scoop risk. A Sandia group has publicly announced WDM linear response as ongoing work.
- **A structural contradiction the program must resolve.** The rung that can be benchmarked exactly (UEG) has no advantage. The rung that might have one (hydrogen) has no exact cross-check.
- **Round 2 did not change C01's formulation, gates or claim.** It added four notes (Section 10, "Round-2 notes"):
  1. a cost floor of roughly 1e15 for any static-observable variant;
  2. a recommended cap on evolution time;
  3. a statement that the short-time lens found no other regime where cheap short-time circuits and a many-body light cone coexist (consistent with C01's framing, not evidence of advantage);
  4. C02 (WDM conductivity) parked as a conditional branch of C01.

**Closest round-2 miss: N01** (Section 11; not a finalist).
- **Why it was the best round-2 match.** It matches the quantum primitive to the output better than anything else in either round:
  - eigenvalue-only QPE;
  - no Gibbs state;
  - no linear-response shot noise;
  - cheap trial states (pilot overlap² 0.87–0.90);
  - one (N_k = 27, n_b = 3) rung at S·G ≈ 2e12 Toffoli.
- **Why it failed.** It fails three of the round-2 conditions.
  1. **The decision is not inside the wall.**
     - Classical occupation-truncated multi-band ED at 21 sites already answers the primary yes/no "yes" (arXiv:2608.12452).
     - The ν = 2/3 competition seen in experiments is at finite temperature and appears entropy-driven (arXiv:2607.08710, 2408.10203, 2609.16483). T = 0 eigenvalues do not settle it.
  2. **The wall rests on one method family and has not been run.**
     - Only full torus ED is documented to fail.
     - Occupation-truncated ED reaches N_k = 24–27.
     - Multi-band neural quantum states and multi-band iDMRG have not been run on this Hamiltonian.
  3. **The model floor is at or above the solver spread.**
     - The moiré-capacitor term V_val is estimated at 9–12 meV, against an FCI window edge near 10 meV.
     - The resulting gap uncertainty is about the size of the gap.
- **Cost is marginal.** A decision-grade convergence ladder costs about 3e13 (bracket 1e13–3e14), at or just over the screen.
- **Status: parked, not killed.** It has a cheap classical reopen chain (Section 21).

**First experiment:** a purely classical, laptop-scale information gate (K-C01a, Section 19).
- It tests whether an exact real-frequency S_ee narrows the posterior on (n_e, Z, collision frequency) beyond the best classical forward model plus model-free temperature, at a named instrument resolution.
- It is followed by a multi-family classical gate (K-C01b, about 1e4 core-hours) with a θ = 1 control.
- No quantum resource work beyond a UEG-rung estimate is justified until both gates pass.
- Separately, if spare classical capacity exists: N01's gate K1, truncated multi-band ED at N_k = 21 and 24 over the V_val prior. It is workstation-scale and decisive either way. It must be pre-registered.

**Cross-cutting findings** (recommended for `SCIENTIFIC_MEMORY.md`):
1. **Round 1.** In all six audited candidates, *the classical wall and the decision-relevant information sit in different regimes, and cost is dominated by sampling and state preparation, not Hamiltonian simulation.* This generalises protein lessons L3, L5 and L6 beyond protein structure.
2. **Round 2, short-time lens.** The short evolution time that makes circuits cheap is also what makes the problem classically tractable or uninformative. Three mechanisms cause this: light-cone embedding, moment truncation to ground-state expectation values, and perturbative limits at high energy transfer. The scope is lifetime-limited and ultrafast probes of molecules and 3d/4f solids.
3. **Round 2, N01.** N01 removed lesson (ii), but lessons (i) and (iii) came back in a sharper form. In a static phase-competition problem, classical hardness and sensitivity to the Hamiltonian's parameters peak together at the phase boundary.
   - The round-2 selection lead proposes a round-3 filter: a *floor-to-spread ratio* below 1 at the proposed state point, estimated classically at small size before audit. The ratio is (∂decision/∂parameters × prior width) ÷ classical solver spread.
   - The same lead forecasts that another round over the same static, low-temperature and real-frequency space is unlikely to fill slots 2–3 at this bar. This is a forecast from two rounds, not a proof.

---

## 2. Research methodology

The workflow followed the program's cycle (READ → HYPOTHESIS → … → KILL/ESCALATE). It was restricted to literature, reasoning and order-of-magnitude costing. No pre-registered experiment or production compute was launched. The only local computation was in round 2: the N01 resource auditor built a continuum-model λ calculation and a small multi-band ED pilot in the session scratchpad, with sector dimensions up to about 6e4 (Section 3).

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

**Round 2** targeted the empty slots 2–3. It used the same audit and selection machinery, with an up-front filter built from the round-1 cross-cutting lesson.
- **Up-front filter.** Every candidate had to pass three conditions before audit:
  - **F1, decision inside the wall.** The observable that carries the decision must lie where the multi-family classical wall is, not beside it.
  - **F2, cost.** S·G ≲ 1e13 Toffoli per useful state point.
  - **F3, floor.** The model floor must sit below the classical solver spread.
- **Workflow.**
  8. **Targeted discovery.** Two lenses built to put the decision inside the wall:
     - **Static lens:** static, ground-state or low-T thermal quantities inside a multi-family wall, costed with early-FT QPE (single-ancilla QCELS). It covered 17 target families.
     - **Short-time lens:** lifetime-limited or ultrafast correlated dynamics, where cheap circuits meet a few-expectation-value readout. It covered 12 problems. It used a dimensionless screen K = E_corr · t_max / ħ with t_max ≈ ħ/Γ_eff.
  9. **Prefilter.** The six round-1 reserves (C02, C15, C17, C19, C32, C34), the C14 redesign lane and the round-2 lens output were each re-sharpened into their most defensible form, then checked against F1–F3 using numbers already in the audit record. An input was dropped only if its sharpened form still failed on existing evidence. Result: one candidate to audit (N01) and seven dropped.
  10. **Triple audit** of N01 (novelty, classical adversary, resources), with a prescribed gate order (G3 cost first, then G0 ablation, G1 floor, G2 wall, G4 decision, G5 overlap).
  11. **Selection.** Qualitative ranking against the quality bar and eligibility marking.
  12. **Red team.** This stage runs only for eligible candidates. None was eligible, so it did not run.
- **Protein lessons.** L1–L7 remained binding throughout.

**Resource screen.**
- **Screen values.**
  - Round 1: the Toffoli count per circuit G times the number of circuits S must satisfy S·G ≲ 1e12 for an early-fault-tolerant (FT) claim.
  - Round 2: the upper edge was set at S·G ≲ 1e13 per useful state point. This report quotes both where it matters.
  - A later-FT rate is allowed if it is declared.
- **Runtime conversions.** 170 µs per Toffoli for one magic-state factory (Babbush et al., arXiv:2011.04149), or stated aggregate rates of 1e6 and 1e8 Toffoli/s.
- **Simulator runtime** is never counted as physical runtime.

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
- **Round 2: sources and gaps.**
  - Sources: the arXiv export API, arXiv listing search, arXiv abs/HTML pages and Crossref, all through 2026-09-28. WebSearch was not used.
  - OpenAlex and Semantic Scholar returned HTTP 429 for the whole of round 2 (Retry-After of about 75,000–78,000 s), so no cited-by check was possible. The arXiv API also returned 429 or timeouts for part of the short-time lens.
  - Coverage is therefore narrower than in round 1. For N01, cited-by was replaced by term, author and key-phrase searches.
- **Round 2: query counts.**
  - Short-time lens: 33 queries.
  - Static lens: 32 queries.
  - N01 novelty audit: 26 queries.
  - N01 classical audit: 17 queries.
  - N01 resource audit: about 10 queries.
  - The prefilter and the selection ran no new searches.
- **Round 2: local computation.** The N01 resource auditor built a continuum model and a small multi-band ED pilot in the session scratchpad: `n01_model.py`, `n01_ed.py`, `n01_cost.py` and `lam_scan.txt`.
  - These are not repo files.
  - Their numbers are quoted here as the auditor's derived estimates.
  - They are not research results and are not in `results/raw/`.
- **Round 2: full-text extraction.** Several details attributed to arXiv:2608.12452, 2504.20140, 2509.09275, 2512.01863 and 2608.00167 came from HTML full text read through a summarizing fetcher. They are flagged for PDF confirmation (Section 24.10).
- **Consequence.** Every "not found" in this report is a scoped statement, not a proof of absence. Where a statement is load-bearing, Section 14 repeats its exact scope. Every "first" describing a possible paper means "no earlier instance was found in the scoped search". It is not a priority claim.

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

Round 2 added two targeted sweeps.
- **Static / ground / low-T quantities (static lens):**
  - multi-center spin-state and protonation energetics
  - exchange couplings for EPR assignment
  - polynuclear single-molecule-magnet barriers
  - doped Hubbard and nickelate models
  - the LiNiO2 contested ground state
  - highly-charged-ion clock lines (Ir17+, Os16+)
  - moiré TMD (tMoTe2) and rhombohedral-graphene fractional Chern phases
  - ν = 5/2 GaAs topological order
  - neutron-star 1S0 and 3P2 pairing gaps
  - static warm dense matter
  - permanent-magnet anisotropy
  - quantum-spin-ice thermodynamics
  - cold-atom thermometry
  - electron-gas phase diagrams
  - superallowed-β isospin breaking and Cs atomic parity violation
  - exoplanet line lists
  - noncovalent binding and chemisorption
- **Short-time dynamics (short-time lens):**
  - multinuclear L-edge XAS, RIXS and Kβ XES
  - attosecond charge migration
  - early-time pump-probe in correlated oxides
  - XPS shake-up satellites
  - resonant Auger and the core-hole clock
  - EUV photoresist absorption and photoemission
  - stopping power
  - core-excited vibronic bands
  - XFEL damage in metalloproteins
  - WDM XANES
  - 163Ho electron-capture spectra
  - photonuclear giant-dipole widths

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
| Round-2 discovery | 2 targeted lenses: **static inside the wall**, **short-time dynamics inside the wall** | `round2_discovery_static_inside_wall.md`, `round2_discovery_short_time_dynamics_inside_wall.md` | Applied F1–F3 from the start. Static: 1 conditional survivor (S-M1 = N01), 17 kills. Short-time: 0 survivors, 12 kills. |
| Round-2 prefilter | 1 | `round2_prefilter.md` | Sharpened 6 reserves, the C14 redesign lane and S-M1. Sent N01 to audit and dropped 7, each with a named filter failure and a reopen condition. |
| Round-2 audits | 3 (novelty, classical adversary, resources) | `audit_N01_{novelty,classical,resources}.md` | Gate-ordered audits. The resource auditor computed λ from a real continuum model and ran a small ED pilot. |
| Round-2 selection | 1 | `round2_selection.md` | Ranked N01 (1 of 1) and marked it not eligible. Slots 2–3 stay empty. |
| Round-2 red team | none run | none | No eligible candidate. |
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

### 6.1 Round-1 pool

After merging, the pool held 50 problems: 6 shortlisted, 6 in reserve and 38 killed. The filter abbreviations are defined in Section 2.

In the Status column, "→ dropped (R2 prefilter)" marks a round-1 reserve that round 2 re-sharpened and then dropped (Section 6.2). The round-1 reason is kept as written.

| ID | Problem | Domain | Status | Reason (short) |
|---|---|---|---|---|
| C01 | Real-frequency S_ee(q,ω) of degenerate WDM for XRTS | HED / ICF diagnostics | shortlist → **finalist (conditional)** | Found by 3 lenses. Scoped B, little model floor. Sign problem plus ill-posed analytic continuation. |
| C02 | WDM DC/AC and thermal conductivity, Lorenz number, G_ei | HED transport | reserve → dropped (R2 prefilter; parked as C01 branch) | Scoped C (Sandia OSTI resource report). DC limit costs 1e13–1e16 Toffoli. Fallback if C01 fails L5. |
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
| C14 | Finite-T polarized S(q,ω) of 3D π-flux quantum spin ice | 3D magnetism / INS | shortlist → killed as specified; redesign lane → dropped (R2 prefilter) | See Section 7. A redesign lane is noted in Section 11. |
| C15 | 2D frustrated-magnet S(q,ω) forward model / Hamiltonian discrimination | 2D magnetism | reserve → dropped (R2 prefilter) | Scoped C. Strongest classical 2D toolbox. Semiclassics suffice at high T. |
| C16 | THz 2DCS of frustrated magnets | Nonlinear spectroscopy | killed | F-bench (scarce data). Two-time cost. |
| C17 | Thermal Hall κ_xy of extended Kitaev models via Gibbs states | Kitaev QSL | reserve → dropped (R2 prefilter) | Scoped A, static mechanism. Unknown mixing time. Phonon-dominated signal. |
| C18 | Real-time quantum vs QMC+analytic continuation resolution benchmark | Spectral inverse problems | killed | F-toy. Folded into C14 as a validation rung. |
| C19 | Protocol-dependent metastable states via quantum thermal gradient descent | Quantum spin glasses | reserve → dropped (R2 prefilter) | Most original mechanism in the pool. No physical hard instance. Lab-timescale floor. |
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
| C32 | SO-coupled exchange spectra of multinuclear f-element magnets | Molecular magnetism | reserve → dropped (R2 prefilter) | Scoped B. Polynomial advantage. FeMoco-type floor. |
| C33 | Spin ladders of 3d polynuclear clusters | Bioinorganic | killed | F-classical (CC+DMRG ranking). Polynomial. |
| C34 | Multinuclear L-edge XAS/RIXS/Kβ XES | Core-level spectroscopy | reserve → dropped (R2 short-time lens K1; R2 prefilter) | Scoped C. Lifetime broadening may wash out correlation (L5). |
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

### 6.2 Round-2 pool

Round 2 considered three groups:
- 17 static target families (static lens);
- 12 short-time problems (short-time lens);
- 7 re-sharpened round-1 inputs (prefilter).

One candidate, N01, reached audit. The filter labels F1–F3 are defined in Section 2.

**Audited.**

| ID | Problem | Domain | Status | Reason (short) |
|---|---|---|---|---|
| N01 (= S-M1) | Multi-band FCI vs CDW vs anomalous-Hall-crystal competition in hBN-aligned rhombohedral multilayer graphene at fractional filling, with explicit remote bands | Moiré / flat-band 2D materials | audited → **not eligible (parked)** | Section 8.3. Decision not inside the wall; single-family, unrun wall; floor ≥ spread; decision-grade cost ≈ 3e13 |

**Dropped at the round-2 prefilter** (sharpened form shown; `round2_prefilter.md` §4).

| ID | Sharpened form | Filter failed |
|---|---|---|
| C02 | e-e contribution to σ_DC, κ and the Lorenz number of warm dense Be/H at r_s 1–3 | The e-e correction is large only at low θ, where thermal preparation is unsolved (F1/F2). The DC limit costs 1e13–1e16 T per point (F2). Finite-size floor (L6). It shares C01's Hamiltonian, gates and competitor, and its novelty is C. Parked as a C01 branch. |
| C14R | IN16B µeV local S(ω) of π-flux QSI in Ce2Sn2O7 at βJ ≈ 4, as a two-hypothesis decision | F2: ≥ 1e14 in the best sharpened form, 6e15 T as audited. F3: LRO at about 40 mK, further-neighbour couplings, growth dependence, 2% vacancies, powder average. |
| C15 | h > h_c adiabatic-preparation S(q,ω) ranking of about 38 α-RuCl3 parameter sets | F1: cheap preparation happens where DMRG and NLSWT converge; hardness is at h ≈ h_c. F3: the degeneracy comes from data and model, not the solver. L3 inference loop. Novelty C. |
| C17 | Magnetic κ_xy/T plateau of K-Γ-Γ'-h at T ≪ flux gap | L5/F3: the measured signal is phonon-dominated. F2: a Gibbs sample per shot plus derivative shot noise, ≥ 1e14–1e15 T. |
| C19 | FC/ZFC splitting as a thermal-gradient-descent fixed point of a disordered triangular magnet | F1: no physical hard instance. F3/F-bench: an idealized channel vs a laboratory protocol, with bath and disorder floors. |
| C32 | One-step SO exchange ladder of σ-bonded mixed-valence Ln2 | F3: the chemistry trilemma. L5: blocking is set by spin-phonon relaxation. Polynomial advantage. No multi-family disagreement found (L7). |
| C34 | Multinuclear L-edge XAS/RIXS | L5: K_intersite < 1. F-classical at the sizes where cost passes (short-time lens K1). |

**Killed by the static lens** (`round2_discovery_static_inside_wall.md` §3).

| ID | Target | Failure |
|---|---|---|
| K-S1 | Multi-center spin-state / protonation energetics (OEC, nitrogenase, P450, …) | Trilemma: active-space QPE leaves a 2–5 kcal/mol floor; full-basis QPE costs 1e14–1e16. The classical wall is receding. |
| K-S2 | Exchange couplings for EPR assignment | Charge-transfer correlation outside the active space. cm⁻¹ precision costs 1e12–1e14 per circuit. Geometry floor. |
| K-S3 | Polynuclear SMM barriers | L5: blocking is set by Raman / spin-phonon / QTM processes, and a classical workflow already matches a Co dimer. |
| K-S4 | Doped 2D Hubbard, nickelate downfolded models | DMRG and AFQMC converge on the pure model. The Hund-coupling floor flips the pairing assignment. |
| K-S5 | LiNiO2 contested ground state | 1e12–1e14 T per QPE at 1–2 k-points. ZPE/JT floor. XAS/RIXS already favour disproportionation. Already a quantum target. |
| K-S6 | HCI clock lines (Ir17+, Os16+) | The limit is line strength, not the energy prediction. The QED floor sits at the required precision. |
| K-S7 | tMoTe2 FQAH phase diagrams | Parameter floor. A band-mixing NQS already exists. Folded into N01. |
| K-S8 | ν = 5/2 GaAs topological order | The clean-limit spread is real, but the experiment is decided in the disorder floor. |
| K-S9 | Neutron-star pairing gaps | 1S0: QMC families agree. 3P2: the coherence length needs 3e6–3e9 neutrons. |
| K-S10 | Static WDM (S(q), χ(q), LFC) at θ 0.25–0.5 | UEG: no wall. H at r_s = 2: a wall, but it costs ~1e15–1e18. Recorded as an input to C01. |
| K-S11 | Permanent-magnet anisotropy | Brillouin-zone sampling puts cost far beyond 1e13. Chemical-order and temperature floors. |
| K-S12 | QSI low-T thermodynamics | Gibbs mixing is unbounded where the answer differs. Vacancy floor. LRO at 40 mK. |
| K-S13 | Cold-atom Hubbard thermometry | Model-free thermometry exists. The device is its own simulator. |
| K-S14 | Uniform / 2D electron-gas phase diagram | No practical decision (F-toy). |
| K-S15 | Superallowed-β δ_C; Cs APV | Amplitude estimation puts cost at 1e14–1e16. The EFT, QED and neutron-skin floors are comparable. |
| K-S16 | Exoplanet TM-diatomic line lists | 0.1 cm⁻¹ is below any ab initio floor, and the empirical MARVEL route exists. |
| K-S17 | Noncovalent binding; chemisorption | Moving to classical consensus. Not reopened. |

**Killed by the short-time lens** (`round2_discovery_short_time_dynamics_inside_wall.md` §2; zero survivors).

| ID | Target | Failure |
|---|---|---|
| K1 | Multinuclear L-edge / RIXS / Kβ (= C34) | L5: K_intersite < 1. F-classical where cost passes (20-orbital RIXS, 2.0e10 T). |
| K2 | Attosecond charge migration | TDDMRG is converged at CAS(40o,35e) over 2 fs. The initial-state and nuclear-decoherence floors dominate. The observed frequency is insensitive to correlation. |
| K3 | Early-time pump-probe of correlated oxides | Short-time classical algorithms (cluster expansion, Majorana propagation). L6. |
| K4 | XPS shake-up satellites | TD-dCC reproduces exact satellites. The U/Δ/double-counting floor. |
| K5 | Resonant Auger / core-hole clock | Complex-variable CC. A compressible one-particle bath. |
| K6 | EUV photoresist absorption / photoemission | Absorbance is measured directly (L5). Photoemission costs ~1e18. |
| K7 | Stopping power | Already claimed (F). |
| K8 | Core-excited vibronic bands | ML-MCTDH and cumulants are efficient at short times. |
| K9 | XFEL damage of metalloproteins | Incoherent rates dominate (L5). Pulse-parameter floor. |
| K10 | WDM XANES / Kα satellites | A static problem; DFT-MD is the working twin. |
| K11 | 163Ho EC spectrum shake-up | Core-valence correlation floor (the C04 pattern). |
| K12 | Photonuclear GDR widths | EFT floor; QRPA / CC-LIT. |

The short-time lens recorded two residuals, R1 (multinuclear core spectra with an above-Γ intersite feature) and R2 (charge migration with ≥ 80–100 correlated orbitals). Both are marked `eligible = false`, and no instance of either was found.

---

## 7. Major candidates eliminated

The table lists every candidate that received a full triple audit and was not selected: five round-1 shortlisted candidates, and the single round-2 audited candidate, N01. The verdicts are given as novelty / classical / resources.

| ID | Candidate | Verdicts | Terminal verdict |
|---|---|---|---|
| C14 | Finite-T polarized S(q,ω) of 3D dipolar-octupolar π-flux quantum spin ice (Ce2Zr2O7 / Ce2Sn2O7 / Ce2Hf2O7) | wounded / wounded (severe) / killed | Killed as specified. An unaudited redesign lane remains (Section 11). |
| C44 | Dense e-h plasma dynamics through the exciton Mott crossover in 2D TMDs | wounded (B, not A) / killed / wounded | Killed as a practical target. A category-1 residual remains. |
| C41 | Correlated multi-electron strong-field/photo-ionization: joint momentum sampling | wounded / killed / wounded | Killed. A category-3 reference residual has no consumer. |
| C07 | Real-frequency spin/density response of hot neutron-rich matter for supernova opacities | wounded / killed / killed | Killed. A category-1 residual remains. |
| C04 | Kilonova Ln/An expansion opacity from thermal dipole spectral functions | wounded / killed / killed | Killed. No quantum residual. |
| N01 (round 2) | Multi-band FCI vs CDW vs AHC competition in hBN-aligned rhombohedral graphene, re-scoped to the N_k / n_b convergence of the moiré-capacitor ν = 2/3 FCI | wounded (B) / wounded, leaning kill / wounded (single rung passes G3) | Not eligible. Parked with a classical reopen chain (Section 21). A category-3-vs-ED resource-study residual remains. |

Round-2 inputs dropped at the prefilter, with no audit (Section 6.2):
- the reserves C02, C15, C17, C19, C32 and C34;
- the C14 redesign lane (C14R).

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

### 8.3 Round 2: N01 (audited, not eligible)

**What N01 was.** QPE/QCELS eigenvalues of the explicit multi-band (n_b = 3–5), momentum-space continuum Hamiltonian of hBN-aligned rhombohedral N-layer graphene at N_k = 27–36. The question was whether a gapped fractional Chern insulator (FCI) at ν = 2/3 (and 3/5, 2/5) survives remote-band mixing, and how it competes with CDW and anomalous Hall crystal (AHC) states.

1. **The primary yes/no is already answered classically (novelty W1; classical #1).**
   - Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman (arXiv:2608.12452, Aug 2026) introduce a "moiré capacitor" term: the remote valence charge imprinted on the conduction bands.
   - With it, 3-band occupation-truncated ED confirms a ν = 2/3 FCI "stabilized by inter-band fluctuations".
   - Scope of that result: 21 sites; caps n2, n3 ≤ 6; dimension up to ~1e9; gap ~0.1–0.3 meV.
   - The authors state they are "unable to access larger systems".
   - What remains open is narrower than N01's primary question:
     - convergence in N_k and in untruncated n_b;
     - ν = 3/5 and 2/5 under the same model;
     - same-model FCI vs AHC/EQAH vs skyrmion-FCI energetics (arXiv:2608.14535).
   - Answering these confirms or refutes a published classical claim. It does not enable a new design decision.
2. **The experimentally decisive competition is at finite temperature (lesson i).**
   - Observations:
     - FCI → generalized AHC below ~150 mK as a bulk transition (arXiv:2607.08710, abstract only);
     - extended QAH at ~40 mK, with FQAH recovered at higher T or current (arXiv:2408.10203);
     - FCI only at finite B in another pentalayer device (arXiv:2408.10133).
   - A proposed mechanism: entropy-driven FQAH (Kim & Kivelson, arXiv:2609.16483).
   - Deciding the observed phase needs free energies, which brings back the Gibbs-state cost that N01 was built to avoid.
   - The implied T = 0 energy scale is ~0.013 meV (k_B × 150 mK) [ESTIMATE]. That is below both the gap and the floor.
3. **The model floor is at or above the solver spread (lesson iii).**
   - V_val is 9 meV (direct) to 12 meV (formula), against an FCI window of ~4–10 meV.
   - The gap slope of ~0.1 meV/meV turns this into a gap uncertainty of ≥ 0.15–0.3 meV, which is about the size of the gap.
   - Other floor terms:
     - hBN orientation 0° vs 180° ("markedly different" moiré strength; arXiv:2507.20647);
     - lattice relaxation ("crucial"; arXiv:2605.16218);
     - the qualitative CN-vs-AVE valence-reference spread (arXiv:2407.13770).
   - Adding explicit conduction bands removes none of these floor terms.
4. **The wall is single-family and unrun (L7).**
   - Only full torus ED is documented to fail. Its wall lies between (18,3) at 1.9e10 and (21,3) at 1.8e12.
   - The families not yet run on this Hamiltonian:
     - occupation-truncated ED, at 1.6e9–9.6e9 for N_k = 24 and 1.2e10–7.7e10 for N_k = 27;
     - multi-band Neural Transformer Backflow (NTB) NQS, demonstrated at 2.25e12 in tMoTe2 (arXiv:2509.09275);
     - multi-component iDMRG, demonstrated for Landau-level mixing (arXiv:1410.3861).
   - The quantum comparator is therefore truncated ED at 1e10–1e11, not full ED at 1.7e16.
5. **Decision value is confined to unbuilt stacks (novelty W3).**
   - Built devices are their own oracle. Alignment and twist windows are now measured directly (arXiv:2510.15309, 2505.01767, 2507.20647, 2608.24684).
   - Unbuilt stacks are where the parameter floor is widest.
6. **Cost is marginal for a decision.**
   - One (27,3) rung is 2.1e12 and passes.
   - The decision-grade ladder is ~3e13 (1e13–3e14), 1–3× over the screen.
   - The phase map, 3e14–1.5e15, fails.
   - If the FCI correlation length requires N_k ~ 100, the cost is ~6e13 per rung and fails.
7. **What N01 got right.**
   - It fixed round-1 lesson (ii): the output is eigenvalue-only, there is no Gibbs state, and there is no linear-response shot noise.
   - The pilot overlap² is 0.87–0.90, decaying by only ~0.02 per electron.
   - The resource audit refuted the prefilter's pessimistic λ bound (7e5–1.3e6 meV). With real form factors, λ is 2.0e4–3.2e4 meV, or ~8.6e3 meV effective with spectrum amplification.

### 8.4 Round 2: prefilter drops, grouped by mechanism

The details are in Section 6.2 and `round2_prefilter.md`.
1. **Wrong bottleneck, cost already known.** C14R (~6e15 T audited), C17 (≥ 1e14–1e15) and C02 (1e13–1e16). All three are dominated by correlated thermal or Gibbs preparation and shot count (round-1 lesson ii). Sharpening does not remove it.
2. **Wall and information in different places.** C15 (cheap preparation only where classical methods converge) and C34 (K_intersite < 1).
3. **Floor or benchmark missing.** C32 (chemistry trilemma plus L5) and C19 (no physical instance with established hardness, and no observable that maps to a laboratory protocol).

The prefilter's sharper form of the round-1 lesson: in every dropped reserve, *preparing the state that carries the decision* costs more than the quantum primitive that motivated the proposal.

### 8.5 Round 2: lens-level kills, grouped by mechanism

1. **Static trilemma** (static lens §0). Across 17 static target families, each filter kills a different family.
   - **Molecular chemistry.** Active-space QPE is cheap, but the floor is at or above the spread. Full-basis QPE costs 1e13–1e16.
   - **Ab initio periodic solids.** 1e12–1e14 per QPE at small k-meshes; ZPE/JT floors.
   - **Downfolded lattice models.** The Hund and downfolding floor flips the answer.
   - **Exact-Hamiltonian systems.** No practical decision, or a disorder floor.
   - **Static WDM.** Classical methods reach furthest exactly here.
2. **Short-time structural negative** (short-time lens §1). Three mechanisms make "short" classical:
   - light-cone locality, which makes embedding sufficient;
   - moment truncation, which reduces the problem to ground-state expectation values;
   - high energy transfer, which reaches perturbative and factorized limits.

   A survivor needs K ≳ 3–10, a light cone containing many strongly correlated degrees of freedom, and a low floor. In molecules and 3d/4f solids the first two conflict. The only regime found where all three hold is intermediate-q continuum Coulomb matter, which folds back into C01 and C07.

---

## 9. Final candidates

| Slot | Candidate | Status | Scoped novelty | Claim category targeted |
|---|---|---|---|---|
| 1 | **C01, correlated thermal S_ee(q,ω) of warm dense hydrogen at r_s ≈ 2, θ = 0.25–0.5 for XRTS, with an exact UEG validation rung** | Conditional finalist: it must pass classical gates K-C01a and K-C01b before any quantum work | B | 3 (accuracy-class computational/resource advantage vs a tuned classical portfolio); fallback 1 |
| 2 | none | Not filled after round 2 (Section 11). Closest miss: N01, not eligible | none | none |
| 3 | none | Not filled after round 2 (Section 12) | none | none |

**Red team.**
- **Round 1.** The red team rejected no candidate. C01 was the only candidate sent to it, and neither reviewer found a fatal objection to the whole candidate. The red team did kill two C01 sub-claims (Section 18).
- **Round 2.** No candidate was sent to red team, because selection found none eligible. Round 2 therefore has no red-team survivors to add. It also has no red-team rejections (Section 18.4).

**The total is one finalist, which is fewer than the three the brief asked for.** The search covered two rounds and 21 audits. It considered about 80 problem entries: 50 in round 1, and in round 2 17 static families, 12 short-time problems and N01, with some overlap between rounds. It produced no second candidate that meets all three conditions at once:
- the decision-relevant observable lies inside a multi-family classical wall;
- S·G ≲ 1e13 per useful state point;
- the model floor is below the solver spread.

Two structural reasons recur:
1. **Wall and information in different regimes.** Where the classical wall is real, either the decision does not need that regime, or a cheap approximate family already matches the measured observable.
2. **Cost or floor.** Where the quantum primitive is well matched (eigenvalue-only N01, cheap short-time circuits), one of two things happens. Either the classical wall is unrun or already open, or the Hamiltonian is specified too loosely for the exact answer to decide anything.

Slots 2 and 3 are not padded.

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

**Round-2 notes on C01.** Round 2 did not audit or red-team C01 again. Its formulation, gates, claim category and novelty category are unchanged. Four round-2 findings bear on it.
1. **Static-branch cost floor** (static lens K-S10).
   - The static sibling of C01 (static S(q), χ(q), local-field correction, ITCF) was killed as a separate candidate.
   - For the UEG, the static regime at θ = 0.25–0.5 is covered by ξ-PIMC, FT-AFQMC and pseudo-fermion PIMC.
   - For hydrogen at r_s = 2, the static observable at 1% costs roughly 1e15–1e18 [ESTIMATE].
   - Consequence for gate K-C01a: if the ITCF already carries the decision information, any quantum computation must target hydrogen at θ < 0.5, and it cannot cost less than ~1e15. That makes the resource position worse, not better.
2. **Evolution-time cap** (short-time lens §4). The lens recommends the following for the density-kick circuits:
   - cap t_max at ħ/Γ_eff, where Γ_eff combines plasmon damping and instrument broadening;
   - report K = ω_p · t_max for each (q, θ).

   This is a recommendation, not an audited revision. It bounds G per shot and makes the information-vs-computation question (L5) explicit per state point.
3. **Regime confirmation, not independent evidence** (short-time lens §1, §4). Intermediate-q continuum Coulomb matter is the only regime the short-time lens found where short-time cost and a many-body light cone coexist. This is consistent with C01's framing. It is not evidence of advantage.
4. **C02 parked as a conditional C01 branch** (prefilter §2.1).
   - The e-e contribution to σ_DC, κ and the Lorenz number of warm dense Be/H escapes C01's ITCF risk at ω → 0. It shares C01's Hamiltonian, its thermal-preparation gate and its Sandia competitor.
   - Reopen condition: C01 passes gates 2–3, *and* a named (ρ, T) point shows a spread among Kohn-Sham Kubo-Greenwood (KS-KG), GW and kinetic theory above hydrocode tolerance.

---

## 11. Detailed analysis: Finalist 2, not filled

No second candidate cleared the bar in either round. This section records the closest miss from each round. Neither is a finalist, so neither gets the full 26-item treatment. Their key items are given so that a reopening can start from them.

### 11.1 Round-2 closest miss: N01 (audited; not eligible; parked)

**Topic.** Multi-band FCI vs CDW vs AHC ground-state competition in hBN-aligned rhombohedral multilayer graphene at fractional filling, with explicit remote bands.

**Re-scoped problem** (the most defensible form after audit; `round2_selection.md` §2.1).
- **INPUT.**
  - The R5G/hBN model of arXiv:2608.12452: SWMcC hoppings; hBN moiré V1 and phase; the moiré-capacitor valence Hartree term V_val; dual-gate screened Coulomb interaction.
  - V_val is swept over the fixed points {6, 8, 9, 10, 12} meV, with V1 ± 20%. These are sweep points, not fits.
- **COMPUTE.** The low-lying eigenvalues in each many-body momentum sector:
  - N_k = 27 with n_b = 3, 4, 5, untruncated;
  - N_k = 36 with n_b = 3, 5;
  - 3 flux-insertion points;
  - ν = 2/3, 3/5 and 2/5.
- **OUTPUT.**
  - (a) For each V_val point: whether the torus-degenerate FCI gap is converged, and its sign.
  - (b) E_FCI − E_AHC/EQAH, using HF or crystal trial states on commensurate tori.
  - (c) Whether the capacitor-plus-band-mixing FCI and the skyrmion FCI (arXiv:2608.14535) are the same ground state.
- **VALIDATION.** Exact multi-band ED at N_k ≤ 18–21, and truncated ED at 21.

**Quantum mechanism.**
- Qubitized QPE with one of three block encodings of the momentum-conserving density-density Hamiltonian:
  - double factorization (DF);
  - a first-quantized band-basis LCU, which is the resource auditor's derivation and not a published algorithm;
  - DF with spectrum amplification (arXiv:2502.15882).
- Early-FT QCELS or multi-modal QCELS (arXiv:2211.11973, 2303.05714) for each momentum sector.
- Trial states: 1-band ED vectors, HF determinants and crystal states.
- The output is eigenvalue-only. There is no Gibbs state and no linear-response shot noise.

**FULL vs ABLATION.**
- FULL: QPE/QCELS in the untruncated space.
- ABLATION: the best of the following.
  - Occupation-truncated ED at N_k = 24–27. This is the strongest arm.
  - NTB-type multi-band NQS.
  - Multi-band iDMRG.
  - Schrieffer-Wolff three-body-renormalized single-band ED.
    - The one-body-only single-band arm, with the capacitor term, gives a CDW at 21 sites. That is the novelty auditor's reading of the HTML full text, flagged for PDF confirmation. So this arm probably fails.
    - The classical auditor expects the perturbative arm to fail as well, because the bare bands are gapless.

**Scoped novelty: B for this problem; C for the FQH family.**
- In the round-2 arXiv API and Crossref queries through 2026-09-28, no fault-tolerant resource estimate, QPE/QCELS study or advantage study was found for any interacting moiré, FCI, FQH or Landau-level Hamiltonian.
- The quantum work found is:
  - NISQ state preparation and VQE/VQD for single-Landau-level FQH (e.g. arXiv:2607.11380, 2608.05140);
  - a non-interacting DOS computed by modified QPE (arXiv:2510.09999).

**Claim category.**
- 3 (computational/resource), against exact ED only, and narrowly: at N_k ≥ 21 with n_b = 3.
- 1 (quantum usefulness / certification), against truncated ED, NQS and iDMRG, unless those fail or disagree at a named point.

**Resources.**
- λ, from the auditor's continuum model with real form factors: DF 3.2e4 meV; first-quantized band basis 2.0e4 meV; DF with spectrum amplification ~8.6e3 meV.
- C_W ~ 2e4 Toffoli per walk step, from uncompiled formulas (about 2× uncertain).
- About 500–5000 logical qubits and 1e6–3e6 physical qubits.
- S·G:
  - 2.1e12 per (27,3) rung;
  - ~3e13 per decision-grade ladder;
  - 3e14–1.5e15 for the full map.

**Why it is not a finalist.** The details are in Section 8.3.
- The decision is not inside the wall: the yes/no is answered at 21 sites, and the observed competition is finite-T.
- The wall is single-family and unrun.
- The floor is at or above the spread.
- Cost is marginal for a decision.

The selection lead judged these failures structural. Even the best outcome of the pending classical tests leaves a parameter-dependent answer.

**Main risk if reopened.**
- Classical closure by truncated ED or NTB NQS at N_k ≥ 27.
- Classical scoop risk is high: the Bernevig/Regnault multi-band ED series and the Fu/Luo NQS groups.
- Quantum scoop risk comes from the group behind arXiv:2302.05531 and 2502.15882, which already has the Bloch-orbital DF/THC machinery and spectrum amplification.

**Reopen chain.** K1 → K2 → G2 → G4 (Section 21). All steps are classical and cheap, and each must be pre-registered.

### 11.2 Round-1 closest miss: the C14 redesign lane (dropped at the round-2 prefilter)

**The lane.**
- The observable: long-time (t·J_par ≈ 128–600), finite-T (T ≈ 0.25 J_par), local, powder-averaged S(ω) of the π-flux dipolar-octupolar XYZ model at L ≥ 3, convolved with µeV backscattering resolution.
- The decision: between the incompatible published parameter sets for Ce2Sn2O7 (Porée et al., arXiv:2304.05452): J± = −5.2 vs −17 µeV, and ring exchange 0.73 vs 12.4 µeV.
- It includes a vacancy arm.

**Why it is not a finalist.**
- **Round 1:**
  - the redesign had never been audited as a problem;
  - Ce2Sn2O7 orders at about 40 mK (arXiv:2607.12274), which questions the QSI model itself;
  - powder local S(ω) discriminates weakly, and samples depend on the growth route;
  - the vacancy floor persists (arXiv:2609.28643);
  - the estimated cost is about 6e15 T;
  - practical significance is limited to one neutron-scattering community.
- **Round-2 prefilter:**
  - Sharpening cannot remove the per-shot Gibbs preparation (~1e10 T per sample).
  - QPE-type spectral sampling still needs ~1e3–1e4 samples.
  - The best sharpened form is therefore ≥ 1e14 for two hypotheses, at least 10× over the round-2 screen.
  - The merged C14/C17 Gibbs-only thermodynamics lane (arXiv:2608.11305) was killed separately by the static lens (K-S12).

**What would reopen it.** Both of the following:
- A pre-registered classical decision-flip test finds a solver-driven flip. The test asks whether ED32, GMFT and SCEBR rank the two parameter sets differently after IN16B resolution convolution, with a vacancy arm. It remains worthwhile as a classical project.
- A Gibbs preparation below about 1e9 T per sample is demonstrated.

---

## 12. Detailed analysis: Finalist 3, not filled

No third candidate cleared the bar in either round. Every residual that survived audit falls into one of three groups:
- category 1 (quantum usefulness) only;
- a resource study with no advantage claim;
- no downstream consumer.

| Residual | Cost | Why not a finalist |
|---|---|---|
| C44: exact 2D two-component Rytova–Keldysh e-h dynamics at η 64–128, one scalar (n(k,t) or g_eh(r,t)), as ground truth for GKBA self-energies | 3e11–3e12 Toffoli (best in set) | Category 1 only. GW+Fan-Migdal NEGF already reproduces the experiment. The experimental disagreement (Chernikov 2015 gain vs Dogadov 2026 no gain vs Mohapatra 2026 discontinuous) is between experiments, not solvers. Phonon/valley floor. Coherent-pump representation defect. |
| C41: full-3D η = 3–4 near-IR strong-field triple/double ratio | 1e12–1e13 Toffoli | Real exact wall at η ≥ 4 but no consumer. Two approximate families already match data. Intensity-calibration floor. |
| C07: ab initio real-frequency spin-relaxation width of warm neutron-rich matter with tensor forces | 1e14–1e19 per state point, plus uncosted thermal preparation | Low decision leverage (≤ 5% on luminosities). A smeared classical twin exists. |
| N01 (round 2): first FT resource estimate for the explicit multi-band moiré continuum Hamiltonian, with validation against ED at ≤ 21 sites | 2.1e12 per (27,3) rung | Category 3 only against exact ED. Category 1 against truncated ED, NQS and iDMRG. The decision is outside the wall and inside the floor (Section 8.3). |
| Short-time R1 (round 2): multinuclear core spectrum with an above-Γ intersite feature | not costed | No instance found. Intersite scales sit below Γ_eff. |
| Short-time R2 (round 2): charge migration with ≥ 80–100 correlated orbitals | not costed | No published TDDMRG blow-up found. The initial-state and nuclear-decoherence floors remain. |

**What would promote C44.** Both of the following must be shown:
- a TMD observable where the classical self-energy families disagree by more than the phonon/parameter floor;
- a phonon-inclusive formulation that stays within S·G ≤ 1e12.

**Where to look next.**
- **What round 1 recommended.** A new audit round over the C14 redesign plus C17, then the reserves C02, C15, C19, C32 and C34, with an up-front filter. Round 2 did exactly this:
  - the prefilter dropped all seven inputs on existing evidence;
  - the two targeted lenses produced one audited candidate, N01, which was not eligible.
- **What the round-2 selection lead recommends:**
  - Report the scoped negative for slots 2–3. Do not promote N01 or any round-1 residual (C14R, C44, C41).
  - If a round 3 is run, require a floor-to-spread ratio below 1 before audit (Section 1). That is in addition to:
    - an eigenvalue-type or few-expectation-value output;
    - a certified classical trial state whose overlap does not decay exponentially;
    - an explicit L2 ablation that folds the extra degrees of freedom in perturbatively.

    The last three requirements come from the prefilter (§5).
  - The lead expects a round 3 over the same static, low-T and real-frequency space not to fill the slots at this bar. That is a forecast, not a result.

---

## 13. Side-by-side comparison (qualitative; no single score)

"Surviving form" means the sharpened formulation after audit. Only C01 is eligible.

### 13.1 Round-1 audited candidates

The C14 column describes the µeV redesign, which the round-2 prefilter later dropped (Section 11.2).

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

### 13.2 Finalist vs the round-2 audited candidate

This table adds the round-2 filter dimensions (decision inside the wall; floor vs spread). The C01 entries are taken from the round-1 audits and red team, not re-audited. The N01 entries use its re-scoped form.

| Dimension | C01 WDM S_ee(q,ω), θ 0.25–0.5 (finalist, conditional) | N01 multi-band moiré FCI convergence (not eligible) |
|---|---|---|
| Novelty evidence (scoped) | B, but thin (Sandia has announced WDM linear-response work) | B for this problem; C for the FQH family. No FT/QPE costing of any interacting moiré / FCI / FQH / LL Hamiltonian found |
| Classical difficulty | Named wall: every exact PIMC variant fails at θ ≤ 0.5; the approximate families are unvalidated there | Unrun wall: full ED fails beyond N_k ≈ 18–21; truncated ED reaches 24–27; NQS and iDMRG untried |
| Decision inside the wall? | Unresolved (gates K-C01a, K-C01b) | No: the yes/no is answered at 21 sites; the window is in the floor; the observed competition is finite-T |
| Quantum mechanism strength | Exponential against exact finite-T fermions, polynomial against TDDFT; thermal preparation unsolved | The strongest match in either round (eigenvalue-only, overlap² ~0.7, no Gibbs state); exponential only against exact ED |
| Model floor vs solver spread | Low Hamiltonian floor (bare Coulomb); thermal-preparation bias is the floor-like term | Floor ≥ spread (V_val, orientation, relaxation, CN/AVE) |
| Practical importance | High (ICF/HED diagnostics), conditional on a consumer | Low–moderate (FQAH device research; unbuilt stacks only) |
| Benchmarkability | Excellent (exact UEG Laplace check) | Good (exact ED ≤ 18–21; truncated ED 24–27) |
| Resource feasibility | UEG rung 4e13–9e14 (later-FT); H rung 7e16–1.6e18 | Rung 2.1e12 (passes); ladder ~3e13 (1–3× over); map 3e14–1.5e15 (fails) |
| Classical-adversary risk | Moderate–high | High (truncated ED, NTB NQS and iDMRG are each an engineering step away) |
| Publication potential | High in any outcome | Moderate: the first FT resource estimate for a moiré FCI Hamiltonian, plus the K1/K2 classical convergence results; not an advantage paper |

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

### 14.3 N01 (round 2; not eligible)

Verdict: **wounded; class B on the quantum side** (C for the FQH family as a whole). It is not killed on novelty, but its primary output has had to be re-scoped.

- **EXACT PRIOR WORK.**
  - Quantum side: none found.
  - Science question: largely answered.
    - Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman (arXiv:2608.12452) confirm a ν = 2/3 multi-band FCI at 21 sites, with occupation truncation.
    - Yu et al. (arXiv:2407.13770, PRB 112, 075110) and Li, Bernevig, Regnault (arXiv:2504.20140, PRB 112, 075130) show FCI collapse or non-convergence without the capacitor term.
- **NEAREST QUANTUM WORK.**
  - NISQ single-Landau-level FQH state preparation, VQE/VQD and dynamics: 2005.02399, 2303.04806, 2304.13748, 2303.04822, 2503.13294, 2512.09982, 2606.16548, 2606.23451, 2607.11380, 2608.05140.
  - Non-interacting TBG DOS by modified QPE: 2510.09999.
  - The Bloch-orbital FT costing line for ordinary solids: 2302.05531, 2604.12142, 2606.27734.
  - None of these is multi-band, moiré and interacting with an FT cost.
- **NEAREST CLASSICAL WORK.**
  - Multi-band ED for R5G/hBN: 2407.13770, 2504.20140, 2608.12452.
  - Multi-band ED for tMoTe2: 2608.23675, 2407.02560, 2604.16847.
  - Multi-band and continuum NQS: 2509.09275 (NTB), 2503.13585, 2512.01863, 2608.00167.
  - iDMRG with higher bands on a tMoTe2 lattice model: 2505.06354.
  - Competing multiband mechanism, the skyrmion FCI: 2608.14535.
  - Moiréless fractional AHC energetics: 2607.08822.
  - The FQH Landau-level-mixing perturbative line: doi:10.1103/physrevb.87.245425 and doi:10.1103/physrevlett.113.086401.
- **TESTED.**
  - Multi-band ED for R5G/hBN at ≤ 21 sites.
  - The one-body-only single-band arm with the capacitor term gives a CDW at 21 sites (HTML reading; PDF confirmation pending).
  - Multi-band NQS and iDMRG in tMoTe2.
  - HF, TDHF and single-band ED for R4G–R7G.
  - FQH state preparation on NISQ hardware.
- **NOT TESTED.**
  - Any FT resource estimate for the moiré continuum or FCI Hamiltonian.
  - Unbiased methods at N_k ≥ 24–27 with untruncated n_b = 3 and the capacitor term.
  - ν = 3/5 and 2/5 with band mixing and the capacitor term.
  - NTB-type NQS or multi-band iDMRG on R5G/hBN.
  - Schrieffer-Wolff three-body-renormalized single-band ED for R-graphene/hBN.
  - FCI vs AHC/EQAH energetics in the multi-band capacitor model.
  - Propagation of the parameter prior.
- **WHY MATERIAL, AND WHERE IT IS WEAK.**
  - The one controlled calculation that produces the observed FCI attributes it to inter-band fluctuations and cannot go beyond 21 sites. Two multiband mechanisms and moiréless AHCs compete as of Jul–Aug 2026.
  - W1: the yes/no is answered.
  - W2: experiments place the T → 0 state near ν = 2/3 outside a simple FCI.
  - W3: alignment and twist windows are measured directly.
  - W4: the classical scoop risk is high.
- **WHY IT COULD BE A NEW PAPER.** It would be the first FT resource estimate (λ, Toffoli, logical qubits, S·G) for the explicit multi-band moiré continuum Hamiltonian. The paper would include:
  - QCELS for quasi-degenerate torus multiplets and flux insertion;
  - validation against ED at ≤ 21 sites;
  - a crossover analysis against NQS and iDMRG.

  It would be a resource study (category 3 vs ED), not an advantage claim.
- **Scoped negative statement.**
  - What was searched: arXiv API queries (novelty audit queries 1–9, 11, 13–22), Crossref queries (23–24), the classical auditor's query Q13 and the resource auditor's arXiv API and Crossref queries, all through 2026-09-28.
  - What was found: no fault-tolerant resource estimate, QPE/QCELS study or quantum-advantage study for any interacting moiré, FCI, FQH or Landau-level Hamiltonian, including the multi-band rhombohedral graphene/hBN continuum model.
  - Blind spot: OpenAlex and Semantic Scholar cited-by lookups were unavailable (HTTP 429). Citing works of 2407.13770, 2503.13585 and 2608.12452 were checked only through arXiv term and author searches.

### 14.4 Round-2 prefilter drops and lens kills (novelty only)

- The prefilter used the novelty classes already recorded in round 1: C02 = C, C15 = C, C17 = A (scoped), C19 = B, C32 = B, C34 = C. None was dropped on novelty. Each was dropped on F1–F3.
- The short-time lens classes:
  - C for K1 (quantum XAS/RIXS exists, with no multinuclear advantage study), K2 (arXiv:2205.10543) and K4 (arXiv:2511.17985);
  - C/D for K5 (quantum Auger via GQE, arXiv:2603.12859);
  - C/F for K6 (arXiv:2602.20234);
  - F for K7 (arXiv:2308.12352).
- The static lens class for K-S5 (LNO) is C/D, because LNO is already a published quantum target (arXiv:2302.05531).

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

In every round-1 non-finalist, at least one tuned classical family already answers the decision-relevant question.

### 15.3 N01 (round 2): classical families and status

| Family | Demonstrated on RnG/hBN or a sister system | Size | Where it stops / notes | Role in the ablation |
|---|---|---|---|---|
| 1-band ED (HF band) | R5G/hBN | N_k up to ~27–30 | Disagrees with multi-band ED on the window location and the gap size | Weak ablation |
| Full multi-band ED | R5G/hBN, 3 conduction bands | N_k ≤ 18 (1.9e10) | Wall between (18,3) and (21,3) at 1.8e12 | Exact validation |
| Occupation-truncated multi-band ED | R5G/hBN | N_k = 21, ~1e9; the truncation is claimed converged by n2 = 6 | Reachable at N_k = 24 (1.6e9–9.6e9) and 27 (1.2e10–7.7e10); fails near N_k ≈ 30–36 | **Strongest ablation** |
| Iterated (natural-orbital) ED | R5G/hBN | N_k = 18 | "No major effect" on overlaps in 2504.20140 | Ablation arm (d) |
| HF / TDHF, all-band | R5G/hBN | Large | Mean field fails the observed twist dependence (2510.15309) | Trial states |
| HF + GW + RPA | R5G/hBN, MATBG | All-band | Claims agreement at integer fillings (2509.19764) | Context |
| Multi-band NTB NQS | tMoTe2 | 5×5 with N_b = 2 (2.25e12); 3×3 with N_b = 5 | 3e-3 meV against ED; momentum-resolved | Untried here; a direct transfer |
| Continuum NN-VMC | Model FCI; RnG with no moiré | 8–9 e in 24–27 cells; N = 25 | Topological degeneracy extracted in a model system; only crystals found in the minimal RnG model | Untried with hBN moiré |
| iDMRG | LLL + periodic potential (2507.07921); Landau-level mixing at 5/2 (1410.3861); tMoTe2 lattice with higher bands (2505.06354) | Cylinders | No multi-band RnG/hBN run found | Untried here; the natural tool if N_k ≥ 50 is needed |
| AFQMC | none at fractional moiré Chern filling | — | Only sign-free DQMC at quarter filling (2210.11486) | — |

**Verdict.**
- The untruncated T = 0 multi-band spectrum at N_k ≥ 27 is not yet computed classically. That is an *unrun* wall, not a demonstrated one.
- The hardness rests on one method family, full torus ED (L7).
- The decision value lies outside that wall (Section 8.3).

**Citation correction.** Wang & Zaletel (arXiv:2507.07921) is DMRG on a lowest-Landau-level-plus-periodic-potential toy model. It is not iDMRG on the RnG/hBN continuum model, as the round-2 prefilter had described it.

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
- **Round 2: switching primitives.** Round 2 deliberately moved away from the round-1 primitive.
  - **Static lens: eigenvalue-only QPE.** The static lens chose eigenvalue-only early-FT QPE (QCELS).
    - Its one survivor, N01, removed all three round-1 mechanism failures:
      - no thermal state;
      - no readout noise beyond eigenvalue repetitions;
      - a native second-quantized, momentum-conserving representation.
    - Its cost is set by the eigenvalue count (26–40 per Hamiltonian) × (λ/ε) × C_W × the convergence ladder (×10–15). Preparation and sampling do not set it.
    - The multi-modal QCELS repetition factor κ is 3–100. Plain QCELS needs overlap p0 > 0.71, which is marginal at N_e ≥ 18.
    - Where band mixing changes the phase, trial states from every competing phase are needed. The audit charges ×1.5 for this. If no trial family reaches overlap² ≥ 0.1, the bound fails.
  - **Short-time lens: cheap real-time circuits.** It tested whether cheap, short real-time circuits with a few-expectation-value readout could carry a decision. Cost was never the problem: published costs are 2.0e10 T for 20-orbital RIXS (arXiv:2602.20270) and ~1e12 for EUV absorption (arXiv:2602.20234). The information and the classical tractability were the problem (Section 8.5).
- **Round-2 mechanism lesson.**
  - Matching the primitive to the output is necessary but not sufficient.
  - N01 is the best-matched mechanism the program has audited. It still fails, because the eigenvalues it computes cheaply either confirm a result that is already classically accessible or sit in a region where the Hamiltonian's parameter uncertainty decides the answer.
  - For N01 the exponential separation holds only against exact ED. Against truncated ED, NQS and iDMRG no complexity-theoretic break-even exists, only possible certification (category 1).

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

### 17.1 Round 2

Screen: S·G ≲ 1e13 per useful state point. The N01 numbers come from the resource auditor's derived model (`audit_N01_resources.md` §§1–4). The other rows are prefilter or lens estimates quoted from the audit record.

| ID | G per circuit (Toffoli) | S·G per useful state point | Logical qubits | Screen (≲ 1e13) | Break-even vs strongest classical |
|---|---|---|---|---|---|
| N01 (18,3), ED-accessible | 1.7e9 | 5.6e11 | ~500–1500 | Passes | None: ED at (18,3) is faster |
| **N01 (27,3)** | 5.4e9 (1Q 7.1e9; DF 1.1e10) | **2.1e12** (κ = 3: 6.4e11; κ = 100: 2.1e13) | ~500–1500 (1Q); ~1.5e3–5e3 (DF) | Passes | Against exact ED only (category 3, narrow). None against truncated ED, NQS or iDMRG |
| N01 (27,5) / (36,3) / (36,5) / (48,3) | 1.3e10 / 1.2e10 / 3.0e10 / 2.8e10 | 4.9e12 / 5.4e12 / 1.3e13 / 1.4e13 | ≤ ~5e3 | Pass to marginal | As above |
| N01 decision-grade ladder: (27,3), (27,4), (27,5), (36,3), (36,5) | — | ~2.9e13 (bracket 1e13–3e14) | — | 1–3× over | — |
| N01 full phase map (10–50 parameter points) | — | 3e14–1.5e15 | — | Fails | — |
| N01 at N_k ~ 100 | — | ~6e13 per rung | — | Fails | — |
| C14R, best sharpened form | C_evol 2.7e7–1.3e8; Gibbs sample ~1e10 | ≥ 1e14 (two hypotheses); ~6e15 as audited | ~0.5–1e3 | Fails | Unknown |
| C17 | Gibbs sample per shot | ≥ 1e14–1e15 [ESTIMATE] | — | Fails | — |
| C02 | 1e10–1e12 | 1e13–1e16 | — | Central value fails | — |
| K-S10 (static WDM, H at η = 128) | — | ~1e15–1e18 [ESTIMATE] | — | Fails | — |
| Short-time K1 (20-orbital RIXS) | 2.0e10 (arXiv:2602.20270) | ~1e13–1e14 with 1e3–1e4 shots | 414 | Marginal | None: the space is classically exact |

**N01 details.**
- **λ (meV) at (27,3).**
  - DF: 3.2e4.
  - First-quantized band basis: 2.0e4. This is the auditor's derived construction.
  - DF with spectrum amplification: ~8.6e3 effective. The E_SOS input (~1.1e3 meV) is derived, not computed.
  - The prefilter's bound of 7e5–1.3e6 meV is refuted: form factors cut Σ_Q V_Q/A from 557 to 130 meV.
- **λ scaling.**
  - λ_DF grows as M², i.e. as n_b² at fixed N_k.
  - λ_1Q is almost flat in n_b (+7% from 3 to 5 bands) and grows as η².
  - λ is robust to about ±40% across the parameter prior. ε_r dominates.
- **Walk cost.** C_W ≈ 2e4 Toffoli per step, from QROAM and Givens formulas. It is not compiled and is about 2× uncertain.
- **Physical qubits.** About 1e6–3e6.
- **Precision and overlap.**
  - Target ε = 0.1 meV (bracket 0.05–0.2), set by the pilot ED scales.
  - Pilot overlap² is 0.87–0.90, extrapolating to 0.67–0.75 at N_e = 18.
  - NISQ is implausible: depth is 1e9–1e10 Toffoli at relative precision ~5e-6.
- **Wall-clock** (physical, not simulator).
  - One factory: ~10 days per (27,3) circuit and ~11 years per Hamiltonian.
  - At 1e6 Toffoli/s: ~1.5 h per circuit, ~23 days per Hamiltonian and ~1 year per decision-grade ladder.
  - Sectors and flux points parallelize across QPUs. Machine-years do not shrink.
- **Break-even against exact ED.** ED wins at (18,3). The quantum route is the only exact route at N_k ≥ 21 with n_b = 3. Against the polynomial families there is no break-even.

**What round 2 changed about the cost picture.** N01 is the first audited candidate in either round where no Gibbs state is prepared and there is no linear-response shot noise, and where a single state point fits the screen. Its cost is set by the eigenvalue count and the convergence ladder. So the round-1 finding that sampling and preparation dominate is not universal. It held for every round-1 candidate and for the dropped round-2 reserves, but not for eigenvalue-native static targets. There, cost is no longer the binding constraint; the floor and the decision value are.

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

### 18.4 Round 2: no red team run

- **Nothing was sent.** Round-2 selection marked its only audited candidate, N01, `eligible = false`. No round-2 candidate went to hostile review. There are no round-2 red-team files and no `adjudication_*` files in `lit_work/`.
- **Tally.** Round 2 adds 0 red-team survivors and 0 red-team rejections.
- **Adversarial coverage without a red team.** N01 was still attacked adversarially inside the audit stage:
  - The classical adversary built the strongest ablation (truncated ED) and found the finite-T decision issue and the floor.
  - The novelty auditor found that the primary output had already been answered.
  - The resource auditor refuted the prefilter's cost warning, in N01's favour. This shows the audits were not one-sided.
- **What this is not.** These audit findings are not a substitute for a red team on a finalist. They are recorded here only because they are the round's adversarial evidence.
- **C01.** It was not re-red-teamed in round 2. Its round-1 red-team record (Sections 18.1–18.3) stands, and the round-2 notes in Section 10 add no new objection or revision.

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

**Slots 2–3.** No first experiment is recommended as a finalist experiment, because no finalist exists. The cheapest decisive route to reopening a slot is N01's K1. It is optional, to be run only if there is spare classical capacity after K-C01a, and it must be pre-registered in `experiments/preregistered/` first.
- **Hypothesis.** Truncation and finite-size effects shift the ν = 2/3 FCI window edge, or the gap sign, by more than the parameter prior does. That is, Δ_trunc > Δ_param.
- **Setup.**
  - Rebuild the R5G/hBN model of arXiv:2608.12452: 3 conduction bands, valence Hartree V_val, and the 2D gate-screened interaction.
  - Run truncated ED with the (14, 2 / 17, 5; n2 ≤ 6, n3 ≤ 1) truncations at N_k = 21 and 24. Sector dimensions are 2e8–1e10.
  - Sweep V_val over {6, 8, 9, 10, 11, 12} meV and V1 over ± 20%.
  - Check truncation convergence at N_k = 21 with n2 ≤ 7–8.
- **Kill rule.** If Δ_trunc < Δ_param, kill N01 on lesson (iii) and record it in `research/KILLBOOK.md`. Otherwise proceed to K2 (Section 21).
- **Compute.** Workstation to small cluster. It must stay within the compute policy (≤ 95% CPU/RAM; ≤ 3 workers per the host-memory note) and use checkpointed jobs.
- **Expected outcome.** The classical auditor expects K1 to kill. The result is publishable as classical science either way.

The Ce2Sn2O7 decision-flip test (Section 11.2) remains worthwhile as a classical project. On its own it cannot reopen a slot, because the per-shot Gibbs cost keeps C14R ≥ 1e14.

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

**For reference, the same categories applied to N01** (not a finalist):
- **Category 3.** Applies only against exact multi-band ED, and only at N_k ≥ 21 with n_b = 3. Converged torus eigenvalues where full ED cannot run would count as a computational/resource result. They would not count as an advantage over the strongest classical portfolio.
- **Category 1.** Applies against truncated ED, NQS and iDMRG, as certification, unless one of those demonstrably fails or disagrees at a named (N_k, n_b, V_val) point. If that happens, the claim could rise to category 3 against that family at that point.
- **Categories 2, 4, 5 and 6.** Not applicable. The output is not a sample, no hardware claim is made, and no proven separation exists for this instance.
- **Does not count:** a larger Hilbert space than ED; reproducing 2608.12452 at 21 sites; a phase assignment that flips inside the parameter prior.

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
- C14 / C14R: the Ce2Sn2O7 decision-flip test finds a solver-driven flip, *and* a Gibbs preparation below about 1e9 T per sample is demonstrated. The second condition was added by the round-2 prefilter.
- C44: a classical solver disagreement beyond the phonon/parameter floor, and a phonon-inclusive S·G ≤ 1e12.
- C41: an η ≥ 3 joint observable that is measured and where the approximate families disagree beyond error.
- C07: a lineshape-specific supernova sensitivity above 5%.
- C04: evidence that non-perturbative core-valence correlation moves binned opacity beyond the NLTE and calibration uncertainty.

**N01 (round 2; parked).** The chain is K1 → K2 → G2 → G4, in that order, each conditional on the previous step. Each is classical and must be pre-registered.
1. **K1.** Truncated ED at N_k = 21 and 24 over the V_val / V1 prior (Section 19). Kill if Δ_trunc < Δ_param.
2. **K2.** Truncated ED at N_k = 27 (1.2e10–7.7e10), together with remote-band weight and overlap² vs N_k at N_k = 12–24 (G5).
   - Kill if the gap sign at 27 matches 21 and 24, because the primary yes/no is then closed classically.
   - Continue only if the truncation stops converging, or the sign flips.
3. **G2.** NTB-type NQS and/or multi-band iDMRG on R5G/hBN must disagree with each other, or with truncated ED, at a named (N_k, V_val) point. Kill if they agree.
4. **G4.** The disagreement must change a stated prediction for an unbuilt stack, or discriminate the capacitor mechanism from the skyrmion mechanism, *and* the prediction must be invariant across the parameter prior.

Independent kill routes:
- **Finite-T decisive quantity.** If the finite-T, entropy-driven FCI/AHC competition is accepted as the experimentally decisive quantity, the eigenvalue-only form of N01 is killed now, on lesson (i).
- **Classical publication.** A classical NQS or DMRG result at N_k ≥ 27 that agrees with 2608.12452 closes G2 classically.

Recorded kill reason if triggered: "model floor ≥ solver spread; decision (finite-T, entropy-driven) outside the T = 0 eigenvalue wall".

**Round-2 prefilter drops.** Reopen conditions (`round2_prefilter.md` §4):
- C02: C01 passes gates 2–3, and a named (ρ, T) point shows a KS-KG/GW/kinetic spread above hydrocode tolerance.
- C15: a published multi-family (DMRG/NQS/TPQ) disagreement on a resolved S(q,ω) feature that flips the parameter ranking.
- C17: a material with a demonstrably magnetic κ_xy, plus a proven fast-mixing Gibbs sampler at the needed T.
- C19: an n ≤ 24 exact study finds entangled, protocol-dependent minima that classical twins misassign, for a physical disorder model.
- C32: a published CASSCF-SO / SO-DMRG / AFQMC-SOC disagreement above experimental error on a measured ladder.
- C34 and the short-time lens: a published multi-family failure on an above-Γ multinuclear core-spectral feature that flips a redox or structural assignment; or a TDDMRG/TD-ACI/Majorana-propagation convergence failure within the nuclear-decoherence window for a molecule with measured charge migration and a controlled initial state.

---

## 22. Publication contribution

**C01, in decreasing certainty of publication:**
1. A classical information-theoretic analysis: real-frequency S vs ITCF for XRTS inference, including instrument function and degeneracy. This is publishable either way.
2. The first multi-family classical comparison of S_ee(q,ω) for warm dense hydrogen at θ ≤ 0.5, with a θ = 1 control and measured sign/extrapolation error. It maps the wall or shows that no wall exists.
3. The first end-to-end fault-tolerant resource estimate for thermal S_ee(q,ω) at XRTS geometries, with costed thermal preparation and a UEG–PIMC Laplace validation protocol.
4. Only if all gates pass: an accuracy-class category-3 demonstration at a named state point. This would be far-FT.

**N01 (round 2; not a finalist), in decreasing certainty:**
1. The K1/K2 classical convergence results for the moiré-capacitor ν = 2/3 FCI: truncation vs parameter-prior sensitivity at N_k = 21–27. Publishable either way.
2. The first FT resource estimate for an interacting moiré/FCI continuum Hamiltonian. It would cover:
   - real form factors;
   - λ for DF, first-quantized band-basis and spectrum-amplified encodings;
   - QCELS for quasi-degenerate torus multiplets and flux insertion;
   - validation against ED at ≤ 21 sites.

   This is a category-3-vs-ED resource study, not an advantage paper. Scoop risk is high on both the classical and the quantum side.

**Program-level (negative) contribution.**
- **Round 1.** An audited map showing that, for real-frequency response of correlated continuum or thermal systems judged against real experimental consumers, the exponential separation is real but sits where decision value is low. Sampling and state preparation, not Hamiltonian simulation, set the cost. This extends the protein-program lessons (L3, L5, L6) to HED, nuclear, magnetic, AMO, atomic-data and semiconductor-optics settings.
- **Round 2 adds three scoped negatives:**
  1. **Short-time dynamics.** For molecules and 3d/4f solids, cheap short-time circuits coincide with classical tractability or washed-out correlation (three mechanisms).
  2. **Static targets.** A trilemma across chemistry, periodic solids, downfolded models, exact-Hamiltonian systems and static WDM.
  3. **Engineered flat-band 2D materials.** The one static opening found, it fixes the cost problem but not the floor. Hardness and parameter sensitivity peak together at phase boundaries.
- **Proposed pre-audit filter.** Together these motivate a floor-to-spread-ratio filter before any future audit.

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
   - **Round-2 answer: no, on existing evidence.** All seven were dropped at the round-2 prefilter, each with a named filter failure and a reopen condition (Sections 6.2, 21).
10. Is there any physical, non-contrived Hamiltonian whose local minima are hard classically? (C19; arXiv:2309.16596 gives BQP-hardness only in general.)
    - The round-2 prefilter recommends a small classical-only theory note for `research/OPEN_QUESTIONS.md`, not an advantage audit. The note would ask whether physically motivated disorder models yield entangled, protocol-dependent minima at n ≤ 24.
11. **N01, the finite-T question.** Is the experimentally decisive ν = 2/3 quantity in hBN-aligned rhombohedral graphene a free-energy difference, given FCI → AHC below ~150 mK and EQAH at ~40 mK? If so, can any eigenvalue-only formulation carry the decision?
12. **N01, K1.** Does truncation plus finite size shift the ν = 2/3 FCI window edge more than the V_val / V1 prior does? (Section 19.)
13. **N01, correlation length.** What N_k does the multi-band FCI correlation length require? The 1-band ED at N_k = 27–48 gives a free first estimate. If N_k ≥ 50–100 is needed, torus QPE fails the screen and cylinder iDMRG is the natural tool.
14. **N01, mechanism.** Are the moiré-capacitor FCI (arXiv:2608.12452) and the skyrmion FCI (arXiv:2608.14535) the same ground state? Does a Schrieffer-Wolff three-body-renormalized single-band ED reproduce either?
15. **PDF confirmation for N01.** Items to confirm from the arXiv:2608.12452 PDF:
    - the n2 = n3 = 0 CDW result;
    - the truncation labels;
    - the V_val window;
    - the gap values.

    The 2512.01863 energy comparison is also unconfirmed; it was flagged as an unreliable extraction.
16. **Floor-to-spread ratio.** Can a floor-to-spread ratio, (∂decision/∂parameters × prior width) ÷ classical solver spread, be estimated cheaply and classically at small size for any proposed static target? Does any known engineered or exact Hamiltonian give a ratio below 1 at a state point with a practical decision?
17. **Is a round 3 worth running at this bar?** The round-2 selection lead's forecast is negative for the same static, low-T and real-frequency space. A round 3 would need a materially different search space, or a demonstrated classical-side change such as a verified multi-family disagreement at a named point.
18. **Round-2 search gaps.** Before any submission, rerun the following once rate limits clear:
    - OpenAlex and Semantic Scholar cited-by for 2407.13770, 2503.13585, 2608.12452, 2605.22920 and 2508.15935;
    - WebSearch;
    - company and group pages.

---

## 24. Bibliography

These citations were verified during this workflow, in round 1 or round 2, through an arXiv abstract, HTML or PDF page, the arXiv API, Crossref, OpenAlex or an OSTI record, as recorded in the `lit_work` notes. [L] marks items verified only from an arXiv API listing or title, not from a full abstract page. Sections 24.1–24.7 are from round 1, and Sections 24.8–24.9 from round 2. Section 24.10 lists unverified or incompletely verified items from both rounds; they are kept out of the main bibliography.

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
- Quantum Gibbs/thermal-state preparation, arXiv:2303.18224. The paper is verified; its author list is not (see 24.10).
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
- Bhardwaj et al., npj Quantum Mater. (2022), doi:10.1038/s41535-022-00458-2. The metadata is verified; the parameter values are not (see 24.10).

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

### 24.8 Round 2: moiré / fractional Chern (N01)

These were verified in the round-2 N01 audits or the static lens, through arXiv abs, HTML or API pages or Crossref. [L] means listing or title only. [HTML] means specific numbers were taken from HTML full text through a summarizing fetcher and still need PDF confirmation (Section 24.10).

**Classical theory, rhombohedral graphene**
- Yu, Herzog-Arbeitman, Kwan, Regnault, Bernevig, "Moire Fractional Chern Insulators IV: Fluctuation-Driven Collapse of FCIs in Multi-Band Exact Diagonalization Calculations on Rhombohedral Graphene", PRB 112, 075110 (2025), arXiv:2407.13770.
- Li, Bernevig, Regnault, "Multi-Band Exact Diagonalization and an Iteration Approach to Hunt For Fractional Chern Insulators in Rhombohedral Multilayer Graphene", PRB 112, 075130 (2025), arXiv:2504.20140 [HTML for N_k and iteration details].
- Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, "The 'Moire Capacitor Effect' and Stabilization of Fractional Chern Insulators in Rhombohedral Graphene Superlattices", arXiv:2608.12452 (2026) [HTML for sizes, truncations, V_val window, gaps and the n2 = n3 = 0 result].
- May-Mann, Tan, Ledwith, Shi, Devakul, "Skyrmion Fractional Chern Insulator: An Intrinsically Multiband Route to Fractionalization in Rhombohedral Graphene", arXiv:2608.14535 (2026).
- Desrochers & Vishwanath, "Energetics of fractional anomalous Hall crystals in rhombohedral graphene", arXiv:2607.08822 (2026).
- Kim & Kivelson, "Entropy-driven transitions between extended integer and fractional quantum Hall regimes", arXiv:2609.16483 (2026).
- Abouelkomsan, Gaggioli, Guerci, Fu, "Rhombohedral Graphene: A Tale of Many Crystals", arXiv:2608.00167 (2026) [HTML].
- Wang & Zaletel, "Chiral superconductivity near a fractional Chern insulator", arXiv:2507.07921 (2025). This is DMRG on an LLL plus periodic-potential model.
- Nashabeh & Ochoa, arXiv:2605.16218 (lattice relaxation).
- Lu, Yang, Guo, Liu, PRB 114, L111108 (2026), arXiv:2509.19764 (HF+GW+RPA).
- Soejima et al., arXiv:2403.05522 (AHC II).
- [L] Dong, Patri, Senthil, arXiv:2311.03445, 2403.07873; Zhou, Yang, Zhang, arXiv:2311.04217; Dong et al., arXiv:2311.05568; Kwan et al., arXiv:2312.11617; Huang, Li, Das Sarma, arXiv:2407.08661, 2408.05139; Kim, Timmel, Wen, arXiv:2507.18582.

**Classical theory, tMoTe2, FQH and methods**
- Li, Yu, Xu, Bernevig, Regnault, arXiv:2608.23675 (2026).
- Morales-Duran, Shi, Voinea, Potasz, Cano, arXiv:2604.16847 (2026).
- Zhang & Luo, "Neural Transformer Backflow for Solving Momentum-Resolved Ground States of Strongly Correlated Materials", arXiv:2509.09275 (2025) [HTML for sizes and errors].
- Luo, Zaklama, Fu, "Solving fractional electron states in twisted MoTe2 with deep neural network", arXiv:2503.13585 (2025).
- Abouelkomsan, Geier, Fu, "Topological Order in Neural Wavefunctions", PRB 113, 205119 (2026), arXiv:2512.01863 [HTML; one energy comparison flagged unreliable].
- He, Simon, Parameswaran, "Fractional Chern Insulators and Competing States in a Twisted MoTe2 Lattice Model", arXiv:2505.06354 (2025).
- Zaletel, Mong, Pollmann, Rezayi, PRB 91, 045115 (2015), arXiv:1410.3861.
- Läuchli, Sudan, Moessner, PRB 100, 155142 (2019) (ED record).
- Crossref, titles verified: "Landau level mixing and the fractional quantum Hall effect", doi:10.1103/physrevb.87.245425 (2013); "Effects of Landau Level Mixing on the Fractional Quantum Hall Effect in Monolayer Graphene", doi:10.1103/physrevlett.113.086401 (2014).
- [L] Kwan et al., arXiv:2407.02560; Zhang, Jiang, Luo, arXiv:2608.14208; Zhang et al., arXiv:2406.20036; arXiv:2210.11486 (DQMC).
- [L] Pakrouski et al., arXiv:1411.1068; Papić, Haldane, Rezayi, arXiv:1209.6606; Zucker & Feldman, arXiv:1603.03754 (ν = 5/2, static lens K-S8).

**Experiment**
- Lu et al., arXiv:2309.17436 (zero-field FQAH in R5G/hBN).
- Lu et al., "Extended Quantum Anomalous Hall States in Graphene/hBN Moire Superlattices", arXiv:2408.10203.
- Waters et al., "Interplay of electronic crystals with integer and fractional Chern insulators in moire pentalayer graphene", PRX 15, 011045 (2025), arXiv:2408.10133.
- Aronson et al., PRX 15, 031026 (2025), arXiv:2408.11220.
- Xie et al., arXiv:2405.16944.
- Huo et al., "Does Moire Matter? ...", arXiv:2510.15309.
- Li et al., "Stacking-orientation and twist-angle control ...", arXiv:2505.01767.
- Uzan et al., "hBN alignment orientation controls moire strength in rhombohedral graphene", arXiv:2507.20647.
- Pan et al., arXiv:2608.24684.
- H. Li et al., "Competing Chern states revealed by quasiparticle charging in moire rhombohedral graphene", arXiv:2607.08710. Abstract only; the HTML returned 404.
- Hadjri et al., arXiv:2609.09422.
- [L] Choi et al., arXiv:2408.12584; Wang et al., arXiv:2608.12478; Butler et al., arXiv:2606.06450; arXiv:2510.09548, 2504.06251, 2605.05199 (titles only).

**Quantum**
- Rubin, Berry, Malone, White, Khattar, DePrince, Sicolo, Kühn, Kaicher, Lee, Babbush, "Fault-tolerant quantum simulation of materials using Bloch orbitals", PRX Quantum 4, 040303 (2023), arXiv:2302.05531. Table VI was read from the PDF; the Table III text was garbled, so only ranges are quoted.
- Low, King, Berry, Han, DePrince, White, Babbush, Somma, Rubin, "Fast quantum simulation of electronic structure by spectrum amplification", PRX 15, 041016 (2025) per the arXiv page, arXiv:2502.15882.
- Ding & Lin, QCELS, PRX Quantum 4, 020331 (2023), arXiv:2211.11973, doi:10.1103/prxquantum.4.020331.
- Ding & Lin, multi-modal multi-level QCELS, Quantum 7, 1136 (2023), arXiv:2303.05714.
- Expósito, Aseginolaza, Guerrero-Avilés, Jornet-Somoza, Guinea, Borge, arXiv:2607.11380 (VQE/VQD for FQH manifolds).
- [L] Bai et al., arXiv:2510.09999; Bhardwaj, Muñoz, Jones et al., arXiv:2604.12142 and 2606.27734; Xu et al., arXiv:2608.05140; Wu et al., arXiv:2606.16548; Liu et al., arXiv:2606.23451; Shen et al., arXiv:2503.13294; Kirmani et al., arXiv:2512.09982 and 2303.04806; Rahmani et al., arXiv:2005.02399; Chu et al., arXiv:2304.13748; Kobayashi et al., arXiv:2303.04822; Voinea et al., arXiv:2309.04527; review arXiv:2606.02721.
- [L] Early-FT QPE assessments: Kiss et al., arXiv:2405.03754; Nelson & Baczewski, arXiv:2403.00077; Dong, Lin, Tong, arXiv:2204.05955; Wang et al., arXiv:2209.06811.

### 24.9 Round 2: static and short-time lenses; prefilter

**Static lens**
- Cheung, Safronova, Porsev, Kozlov, Tupitsyn, Bondarev, PRL 124, 163001 (2020), arXiv:1912.08714.
- Rehbehn et al., arXiv:2509.06710.
- Berengut et al., PRL 109, 070802 (2012), doi:10.1103/physrevlett.109.070802.
- Kurashige, Chan, Yanai, Nat. Chem. 2013, doi:10.1038/nchem.1677.
- Lee et al., JCTC 2020, doi:10.1021/acs.jctc.0c00055 (title verified).
- Mondal, Netz, Hunger, Suhr, Sarkar, van Slageren, Köhn, Lunghi, arXiv:2412.04362.
- Dornheim et al., arXiv:2403.08570 (static density response of warm dense H).
- [L] Green et al., arXiv:2011.06441; Jacquet et al., arXiv:2403.18919; Saritas et al., arXiv:1911.01610; Gandolfi, Palkanoglou, Carlson, Gezerlis, Schmidt, arXiv:2201.01308; Gandolfi et al., arXiv:0805.2513; Abe & Seki, arXiv:0708.2523.

**Short-time lens**
- Wild & Alhambra, arXiv:2210.11490, PRX Quantum (2023).
- Zhao, Marvian, Tong, arXiv:2608.19448.
- D'Anna, Nys, Carrasquilla, arXiv:2511.02809.
- Wahyutama & Larsson, arXiv:2409.05959, JCTC 2024.
- Loaiza et al., arXiv:2602.20270 (quantum RIXS resources).
- Nishi et al., arXiv:2505.08612.
- Abraham, Senapati, Pathak, Peng, JCP 164, 104113 (2026), arXiv:2511.17985.
- Lee, Zhai, Chan, arXiv:2305.08184.
- arXiv:1908.05802 (DMRG X-ray Raman of [2Fe-2S]; authors not extracted).
- Dubey & Neufeld, arXiv:2609.23615.
- arXiv:1909.07810 (TD-ACI; JCP doi:10.1063/1.5126945 per the arXiv page).
- Krause & Oliver, J. Phys. Chem. Ref. Data 8, 329 (1979), doi:10.1063/1.555595.
- Calegari et al., Science 346, 336 (2014), doi:10.1126/science.1254061.
- Nat. Phys. 18, 1150 (2022), doi:10.1038/s41567-022-01727-4. The DOI is verified; the first author is not (Section 24.10).
- [L] Miller et al., arXiv:2503.18939; Ghiasi et al., PRB 100, 075146 (2019), arXiv:1812.06432; Higashi et al., PRX 11, 041009 (2021), arXiv:2105.01248; Winder et al., PRB 102, 085155 (2020), arXiv:2004.01428; arXiv:1902.08489; arXiv:2603.12859; arXiv:2110.08925; arXiv:2501.03362.

**Prefilter** (verification recorded in round-1 lens notes; cited again in round 2)
- Kim & Mourigal, "Semiclassical Routes to the alpha-RuCl3 Scattering Continuum via Model Meta-Analysis", arXiv:2602.10190.
- Okubo, Nasu, Misawa, Motome, "Thermal Hall transport in Kitaev spin liquids", arXiv:2507.16558.
- Chen, Huang, Preskill, Zhou, arXiv:2309.16596; Nat. Phys. (2025), doi:10.1038/s41567-025-02781-4.
- Gould et al., Science 2022, doi:10.1126/science.abl5470.
- Babati, Shaffer, Jose, Baalrud, arXiv:2606.02881 and 2606.02890.
- [L] Phonon thermal Hall in α-RuCl3: arXiv:2303.03067, 2501.11272.

### 24.10 Unverified or incompletely verified (not load-bearing unless stated)

**Round 2 additions.**
- **[PDF CONFIRMATION PENDING]** arXiv:2608.12452. The following were read from HTML through a summarizing fetcher:
  - 21 sites; caps n2, n3 ≤ 6; truncation labels 14,2 / 14,5 / 17,5;
  - a V_val window of ~4–10 meV and V_val estimates of 9 and 12 meV;
  - a gap of ~0.1–0.3 meV;
  - the n2 = n3 = 0 CDW result.

  These numbers carry N01's floor and ablation arguments.
- **[UNRELIABLE EXTRACTION]** The arXiv:2512.01863 NN vs single-band ED energies (−39.245 vs −39.346).
- **[SECOND-HAND]** Nature 626, 759 (2024) for Lu et al. arXiv:2309.17436, as cited in 2608.12452.
- **[DERIVED, NOT PUBLISHED]** These come from the N01 resource auditor's session-scratchpad scripts (`n01_model.py`, `n01_ed.py`, `n01_cost.py`), which are not repo files:
  - the first-quantized band-basis block encoding and its λ;
  - the E_SOS estimate used for spectrum amplification;
  - C_W, from uncompiled formulas;
  - the pilot ED overlaps and energy scales.
- **[ESTIMATE]**
  - The ~0.013 meV finite-T energy scale for N01.
  - The static-WDM 1e15–1e18 cost.
  - The C17 ≥ 1e14–1e15 cost.
  - All round-2 physical-qubit counts.
- **[UNVERIFIED / recalled, round-2 lenses]**
  - Specific Heisenberg J and double-exchange B values for Fe-S and Mn-oxo clusters.
  - Vinko et al., Nat. Commun. 2014 (IPD by DFT).
  - The ECHo/163Ho spectral-shape literature and the XFEL-damage literature (short-time kills K9–K11 are argument-level).
  - The FeMoco THC Toffoli count (~1e10).
  - The Cs APV method spread, QED and neutron-skin floors.
  - The magnetocrystalline-anisotropy k-point requirement.
  - FDT thermometry references.
  - The tMoTe2 continuum-parameter discrepancy literature beyond arXiv:2406.20036.
  - KYbSe2 delafossite DMRG and semiclassics fits (C15).
  - CASSCF-SO / fragment reproduction of Gould-type observables (C32).
  - YbMgGaO4 disorder specifics (C19).
  - The first author of doi:10.1038/s41567-022-01727-4.
  - arXiv:2512.01873 (KAN FCI predictors; mentioned by the classical auditor, verification not recorded).

**Round 1.**
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
