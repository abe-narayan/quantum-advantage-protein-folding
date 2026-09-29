# Literature search audit: search for an original, testable quantum advantage outside protein folding

Date: 2026-09-28. Role: audit-trail writer. Status: FINAL for this round.

This file records **how** the literature search was done: tools, queries, screening and coverage gaps. It does not add findings. Everything below comes from the 34 working notes in `research/reports/lit_work/`. Where a note carries a claim, the note is named so the claim can be checked at its source. Nothing here is an experimental result.

**Outcome.** The brief asked for exactly three problems. Selection (`lit_work/selection.md`) found only one that clears the bar, and only conditionally: **C01, correlated thermal S_ee(q,w) of partially degenerate warm dense matter at theta 0.25-0.5 for X-ray Thomson scattering (XRTS)**. Slots 2 and 3 were deliberately left empty. The two red-team reviews then narrowed C01 further (section 5.6).

---

## 1. Inputs and structure of the search

| Stage | Files | Agents |
|---|---|---|
| Discovery (12 lenses) | `discovery_{algorithms, complexity, claims, amo, materials, chemistry, sciml_inference, optimization, classical_frontier, qsim_dynamics, alt_domains, resources}.md` | 12 subagents, one per lens |
| Pool and shortlist | `pool_and_shortlist.md` | synthesis |
| Deep audits (6 candidates x 3 roles) | `audit_C{01,04,07,14,41,44}_{novelty,classical,resources}.md` | 18 auditors: novelty / prior art, classical adversary, resource / break-even |
| Selection | `selection.md` | selection lead |
| Red team (finalist only) | `redteam_C01_classical.md`, `redteam_C01_priorart.md` | Hostile Reviewer #1 (classical/technical), #2 (prior art/significance) |

All searches were run on **2026-09-28**. The upstream context also listed claimed applications and earlier kills from this week's prior searches (singlet fission/OPV, Anderson-Newns, PDT, cathode XAS/RIXS, P450, Pd-zeolite, EUV photoemission, stopping power, corrosion; Cu-oxo zeolite, DNP, DEA etch gases, ultrafast demagnetisation, radical-pair compass, spin-qubit decoherence, polaritonic chemistry, rare-earth magnets, crystal-structure prediction). Those were treated as prior exclusions and not searched again from scratch.

---

## 2. Databases and search engines actually used

### 2.1 Sources that returned data

| Source | How accessed | Used by | Notes |
|---|---|---|---|
| arXiv export API (`export.arxiv.org`) | WebFetch, or local python `urllib`/curl when WebFetch was rate-limited | all 12 lenses, all 18 audits, both red teams | Boolean queries on `abs:`, `ti:`, `au:`, `all:` fields, sorted by relevance or submission date. `id_list` lookups were used to verify IDs. This was the main engine. |
| arxiv.org/search HTML interface | WebFetch | algorithms, materials, qsim_dynamics, resources, optimization (HTML search), C07 novelty/resources, C01 resources | Keyword-literal AND semantics. It carried most queries when the export API returned 429. |
| arXiv abstract and HTML full-text pages | WebFetch | all | Used for verification. HTML full texts were grepped for particular terms, e.g. 2607.02811 for kilonova/Thomson/XRTS, and 2605.07722 for Thomson/structure factor/Toffoli. |
| arXiv PDFs with local text extraction | curl plus `pypdf` / `pdftotext` | C01 resources (Rubin 2023/24, Babbush 2021, Dornheim 2019), C04 resources (2011.03494 tables), C07 resources (2312.05344 Table 9; 2011.04149), C14 novelty/resources (2404.04207, 2304.05452, 2210.14109, 1711.10980, 2601.03202) | Used where the HTML was missing (e.g. 2404.04207 HTML returned 404) or tables were needed. |
| Crossref REST API | keyword (`query.bibliographic`), `/works/<doi>` | all lenses except materials (one query) | Relevance was often noisy. It was the main DOI verifier. |
| OpenAlex | search, `title_and_abstract.search`, `cites:` (cited-by), DOI lookup | complexity, claims (partial), sciml, optimization, classical_frontier, qsim_dynamics, alt_domains, resources (partial), C01 novelty, C04 novelty, C07 novelty, C41 novelty/classical/resources, C44 novelty/resources, C01 red team #2 | Frequently returned HTTP 429. Cited-by lists were the main forward-citation tool (section 3.3). |
| Semantic Scholar | DOI records, citations endpoint | C07 classical, C14 novelty, C41 classical/novelty, C01 red team #2 | The search endpoint returned 429. The citations endpoint worked, and C14 novelty used it for cited-by after OpenAlex returned 429 on all 4 attempts. |
| OSTI | individual records (`biblio/...`) | C01 novelty, C01 classical, resources lens (OSTI 3023927) | The OSTI search endpoint returned non-JSON, so only individual records were read, and these had no abstracts. |
| Bing | one attempt | C07 classical | Returned no usable metadata. |

### 2.2 Failures and limits (recorded in the notes)

- **WebSearch was not available to any agent.** The session budget (200/200) was already spent when discovery began. Every lens and every audit logs a refused or "budget exhausted" call, and none used a WebSearch result. So there was **no general web search (Google, Google Scholar, Bing) anywhere in this round**, apart from one unusable Bing attempt.
- **arXiv export API.** HTTP 429 came intermittently throughout, and the notes say the limit was shared across concurrently running agents. The AMO lens got about 30 queries before 429, and classical_frontier about 11. There were timeouts (e.g. claims "quantum echoes" OR "OTOC(2)", C41 "first quantization AND dynamics"). A batch of 11 queries in classical_frontier was mostly lost to 429.
- **OpenAlex.** HTTP 429 on first call in most lenses. The materials lens got 429 throughout, C14 novelty on all 4 attempts, and C07 resources on all 5 searches. The qsim_dynamics batch was incomplete at exit.
- **Semantic Scholar.** The search endpoint returned 429 (materials, C04 novelty, C07 resources, C41 classical).
- **Other access failures:**
  - Local urllib to arxiv.org/search returned HTTP 406 (materials).
  - WebFetch to arXiv/OpenAlex/Semantic Scholar returned 503 (complexity).
  - nature.com redirected to a login page (C14).
  - APS abstract pages returned 403 (C41 resources); OpenAlex was used instead.
  - The PDF of 2202.05864 was too large to fetch.
  - The PDF of 2205.13595 was not text-readable, so its r_s/T values stay [UNVERIFIED] (red team #1).
  - 2607.25481 was not read because of a classifier error (C01 classical).
  - One wrong ID was corrected: 2007.14460 should be 2011.03494 (C41 resources).
- **Indexing limits.**
  - arXiv abstract search does not reliably index chemical formulas with subscripts. "KYbSe2", "MoTe2", "Ce2Zr2O7" and "RuCl3" variants returned 0 or few hits (materials, algorithms, C14 classical), so a null result there is weak evidence.
  - arXiv listing search is keyword-literal and misses paraphrases (resources, algorithms).
  - The chemistry lens looked only at the top 20 arXiv and top 12 Crossref hits per query.

---

## 3. Query families

Queries are grouped by family. Representative queries are quoted from the logs; each lens and audit file has its complete log. "QC terms" means ("quantum computer" OR "quantum algorithm" OR "quantum computing"), with variants such as qubits, fault-tolerant, QPE or qubitization.

### 3.1 Discovery lenses (12)

| Lens | Query families | Representative queries (from the logs) |
|---|---|---|
| algorithms | Quantum primitives mapped to observables: DSF/neutron scattering, WDM/XRTS, nuclear response, transport, Gibbs sampling, vibrational QPE, reaction rates | arxiv.org/search "quantum computing dynamic structure factor plasma"; "Dornheim imaginary-time correlation function temperature diagnostics"; "quantum Gibbs sampler resource estimates application"; "stochastic estimation nuclear level density shell model"; Crossref "quantum computer algorithm thermal rate constant flux correlation chemical reaction"; author listing arxiv.org/a/baczewski_a_1 |
| complexity | Dequantization and hardness map; nuclear NMEs; neutrino-40Ar; WDM; ADR refrigerants; fission; analytic continuation; opacity | arXiv API abs:"double beta" AND (QC terms); OpenAlex cited-by W4385380575 (Perez-Obiol 2023, 54 works); (40Ar OR argon) AND (Gamow-Teller OR MARLEY OR forbidden) AND neutrino; au:Dornheim AND (imaginary-time correlation OR sign problem) AND X-ray Thomson; (imaginary time OR Euclidean) AND (analytic continuation OR ill-posed) AND (QC terms); HTML grep of 2605.07722 |
| claims | Audit of 2023-2026 advantage and utility claims and their classical rebuttals | arXiv abs 2403.00910, 2503.05693, 2503.08247, 2506.10191, 2306.14887, 2605.04025, 2606.04771; arXiv API "quantum advantage" AND "Pauli propagation"; "sample-based quantum diagonalization"; Rydberg AND (beyond classical OR classically intractable) AND dynamics; Crossref Laurell Okamoto RuCl3, Scheie KYbSe2, Ce2Zr2O7 QSL |
| amo | Collective radiance, clocks, line lists, pressure broadening, ionization (photo, strong-field, multiple), charge exchange, HCI clocks, APV/EDM, kilonova and iron opacity | [arXiv] QC terms AND (photoionization OR strong-field OR attosecond OR high-harmonic); "nonsequential double ionization" AND many-electron AND time-dependent; lanthanide AND opacity AND (CI OR atomic structure) AND kilonova; "charge exchange" AND "cross sections" AND X-ray AND "highly charged"; [Crossref] RMT R-matrix with time-dependence; triple photoionization lithium TDCC |
| materials | INS S(q,w) on quantum computers, Kitaev/RuCl3, thermal Hall, DMFT solvers, defects, Hubbard pairing, spin ice, moire FCI, RIXS | arXiv abstract search: quantum computer "dynamical structure factor"; "thermal Hall" Kitaev exact diagonalization / tensor network / thermal pure quantum; pi-flux QSI sign problem Monte Carlo; all: Ce2Zr2O7; pyrochlore neural network quantum state; RIXS Hubbard model doped paramagnon numerical |
| chemistry | Specific observables inside studied chemistry fields: ISC, spin-orbit, INVEST, exchange couplings, hyperfine, SCO, ZFS, KIE, spin-vibronic, core-level, lanthanide luminescence, actinides, pNMR, SMMs | arXiv abs:"intersystem crossing" AND (QC terms); abs:"inverted singlet-triplet"; (L-edge OR 2p3d OR L2,3) AND (multinuclear OR dimer OR cluster) AND (RASPT2 OR DMRG OR RAS OR multiplet); (spin-orbit AND DMRG) AND (dysprosium OR lanthanide OR actinide); Crossref SSE17 spin-state energetics benchmark; ~14 Crossref DOI checks, including chemRxiv DOIs |
| sciml_inference | Inverse problems: INS Hamiltonian fitting, analytic continuation, 2DCS, RIXS, NMR inference, MLIP labels, DMFT for ARPES | arXiv API "analytic continuation" AND (QC terms); spectral function AND imaginary time AND real time AND "quantum advantage" (0 hits); "quantum computer" AND Hamiltonian AND (inverse problem OR parameter estimation OR Bayesian inference) AND (spectroscopy OR scattering OR spectra); OpenAlex quantum computing inverse problem neutron scattering Hamiltonian learning |
| optimization | DQI/OPI, annealer-native dynamics, quantum local minima, optimal control, QHD, LABS, MIS, QMCMC, BPQM receivers | arXiv API abs:"decoded quantum interferometry" (40 records, date-sorted); abs:"beyond-classical" AND abs:"quantum annealing"; OpenAlex cited-by of "Local minima in quantum systems" (36 works); arXiv HTML search "quantum hamiltonian descent", "low autocorrelation binary sequences", "belief propagation with quantum messages", "green machine" Hadamard receiver (0 hits) |
| classical_frontier | Where classical methods fail (AFQMC, DMRG, HEOM, ML-MCTDH, NQS, NEGF, CC vs DMC) | arXiv API "G1-G2" nonequilibrium instability; ti:"CCSD(cT)"; "quantum advantage tracker"; ESR-STM theory Kondo; OpenAlex cited-by W3087523511 (Al-Hamdani 2021), W4415148299, W4405451244; OpenAlex DOI lookups including 10.1039/d4sc05471g, 10.1021/acs.jctc.4c00751 |
| qsim_dynamics | Transport coefficients, Kubo, diffusion, Floquet heating, NESS, WDM transport, opacity, HHG in Mott insulators, thermopower | OpenAlex title_and_abstract batch ("quantum algorithm linear response Kubo", "Pauli propagation transport diffusion constant", "polaron mobility quantum computer", ...); arxiv.org/search "electron-ion equilibration quantum computer"; "charged-particle transport coefficient comparison workshop"; "Kelvin formula thermopower"; "impact ionization Mott insulator" |
| alt_domains | Nuclear, plasma/WDM, semiconductor devices, PDE solvers, geophysics | OpenAlex cited-by W4399208307 (Rubin et al. PNAS 2024); Crossref "quantum algorithm Thomson scattering plasma"; arXiv au:Baczewski / au:Kononov AND abs:quantum; abs:'warm dense' AND abs:'sign problem'; abs:positron AND abs:lifetime AND abs:'quantum Monte Carlo'; abs:'computational fluid dynamics' AND abs:'fault-tolerant'; Crossref check of the Zhang-Cohen-Haule Nature 2015 retraction |
| resources | Fault-tolerant resource estimates 2021-2026, break-even, first-quantized dynamics, electron-phonon, e-h plasma | Crossref "fault-tolerant quantum resource estimates simulation Toffoli" (2021+); arxiv.org/search title "Hunting for quantum-classical crossover condensed matter"; abstract "quantum computer warm dense matter" (27 hits); "quantum computer transport coefficients conductivity" (44 hits); "exciton Mott transition monolayer" (24 hits); about 16 Crossref DOI verification batches |

### 3.2 Deep audits (18) and red team (2)

| Candidate | Novelty auditor | Classical adversary | Resource analyst |
|---|---|---|---|
| C01 WDM XRTS S_ee(q,w) | DSF + quantum + (warm dense OR electron gas); HED/Thomson/opacity + QC terms; ITCF + quantum computer; authors Baczewski/Kononov/Bobrow; HTML scans of 2605.07722, 2505.02494, 2607.02811, 2511.14643, 2605.22920, 2508.15765; OpenAlex cited-by of Rubin 2024 (30), Babbush 2023 / Kökcü 2024 (56), Dornheim Nat. Commun. 2025 (47) | all:"dynamic structure factor" AND all:"warm dense" (30); all:"fictitious identical particles" (11); abs:"imaginary-time" AND abs:"warm dense" (18); au:Moldabekov AND abs:hydrogen; Crossref warm dense hydrogen PIMC fermion sign low temperature 2023+; OSTI 3389315, 3662053 | Rubin 2308.12352 (abs, html, PDF); arxiv.org/search "quantum algorithm dynamic structure factor electron gas", "quantum computer Thomson scattering"; pypdf table extraction |
| C04 kilonova opacity | kilonova + QC terms (0); (lanthanide OR actinide OR 4f) + QC terms (78); opacity + QC terms (13; only 2607.02811 relevant); (Lanczos OR kernel polynomial) AND (opacity OR transition array) (14); OpenAlex cites W2940065607 (42) and W4384281337 (29) | abs:kilonova AND abs:opacity AND abs:lanthanide (32); abs:kilonova AND abs:"expansion opacities" (7); au:Gaigalas; au:Berengut; (Nd III OR Er III OR U II ...) AND (levels OR spectrum) | relativistic AND quantum AND (phase estimation OR qubitization OR resource estimates) AND (heavy OR actinide OR lanthanide OR Dirac) (28); abs:kilonova AND abs:opacity AND abs:calibrat* (0) |
| C07 supernova neutrino opacity | abs:quantum AND abs:neutrino AND abs:"dynamic structure factor" (0); "quantum computer" AND pionless (3); au:Roggero AND quantum (40); OpenAlex cited-by of 7 works (108 citing works scanned for W2796184659) | all:"neutron matter" AND "structure factor" AND lattice; supernova AND explosion AND (many-body corrections OR structure factor); au:Horowitz AND virial AND neutrino; Crossref Bartl Bollig Janka Schwenk; Semantic Scholar doi:10.1103/physrevd.94.083009 | abs:"spin response" AND abs:"neutron matter"; au:Bartl AND au:Schwenk; Watson 2312.05344 Table 9 via pdftotext; Crossref "quantum computing neutron matter spin response" |
| C14 pi-flux QSI | abs:"spin ice" AND abs:"quantum computer"; all:"quantum spin ice" AND (quantum processor OR Rydberg OR trapped ion ...); (neutron scattering OR structure factor) AND (fault-tolerant OR resource estimate OR qubitization); ti:"quantum spin ice" (60, date-sorted); Semantic Scholar citers of 2401.09551, 2404.04207, 2201.00828 | abs:"dipolar-octupolar" AND abs:pyrochlore (23); abs:"quantum spin ice" AND (cerium OR pi-flux) (30); (pi-flux OR frustrated transverse) AND "Monte Carlo" AND (ice OR pyrochlore) (1); author queries Smith_E_M, Bhardwaj, Schafer_R, Udagawa | abs:"Gibbs" AND abs:"resource estimates" (1); abs:"thermal state preparation" AND (T-count OR resource); OpenAlex "Ce2Zr2O7 exchange parameters dipolar octupolar" |
| C41 multi-electron ionization | 32-row log: arXiv/OpenAlex title-and-abstract searches for QC terms x (strong-field, attosecond, double ionization, photoelectron spectrum, CAP); OpenAlex cited-by of Su 2021 (32 filtered), Chan 2023 (49), Langkabel & Bande (8), Mangin-Brinet (7), Efimov 2021 (12); arXiv author Sato, Takeshi | Crossref "triple photoionization lithium"; "nonsequential triple ionization strong field" (from 2008); TD-ORMAS / TD-RASCI / MCTDHF convergence; OpenAlex W2173353984 cited-by (44) | Crossref Colgan/Pindzola/Robicheaux; Zielinski-Majety-Scrinzi tSURFF; arXiv abs:"absorbing boundary" AND quantum AND algorithm; OpenAlex DOI abstracts for PRL 93 053201, PRL 81 1813, PRA 93 023406 |
| C44 2D e-h plasma | all:"electron-hole" AND all:"quantum computer"; (Bethe-Salpeter OR excitons OR electron-hole plasma) AND (qubitization OR phase estimation OR first quantized); (SBE OR band-gap renormalization OR optical gain OR TMD) AND QC terms (this found 2606.04295); OpenAlex cited-by W2977125138 (~70) and W2765173966 (118) | all:"exciton Mott" AND all:monolayer; au:Perfetto AND au:Stefanucci; au:Bonitz AND (G1-G2 ...); (GKBA OR G1-G2 OR "Kadanoff-Baym ansatz") AND exciton*; "electron-hole liquid" AND (QMC OR DMC) (0) | abs:"time-dependent" AND abs:"neural" AND abs:"many-electron"; abs:"G1-G2" AND abs:scheme; abs:"Mott" AND abs:exciton AND (WS2 OR WSe2 OR MoS2 OR MoSe2) (30) |

**Red team (C01 only).**
- **Hostile Reviewer #1 (classical/technical)** targeted the classical escape routes:
  - abs:"warm dense" AND abs:"sign problem"
  - au:Dornheim (50 most recent, to 2609.29257)
  - ti:"effective static approximation"
  - abs:"free energy" AND neural AND (electron gas OR dense hydrogen)
  - abs:"exchange-correlation kernel" AND (jellium OR electron gas) AND frequency
  - (thermal state OR Gibbs state OR Gibbs sampl) AND (electron gas OR warm dense OR jellium OR plane wave) AND quantum
  - Crossref deuterium XRTS metallization
- **Hostile Reviewer #2 (prior art/significance)** targeted four things: post-July-2026 preprints, finite-T response-algorithm literature, cited-by of the closest papers, and domain significance. Queries included:
  - au:Baczewski by date
  - au:Babbush / Rubin / Berry / Low / Arrazola plus plasma terms
  - abs:"thermal state preparation" AND (plasma OR warm dense OR electron gas OR jellium OR first quantized), which returned 0
  - ti:(finite temperature OR thermal) AND ti:(correlation functions OR response functions OR structure factor) AND QC terms
  - OpenAlex cites:W4399208307 (27)
  - Semantic Scholar citations of 2508.15935, 2605.22920 and 2301.01203
  - "Thomson scattering" AND (Bayesian OR posterior OR MCMC OR UQ) AND (warm dense OR dense)

### 3.3 Forward-citation (cited-by) sweeps

Where they worked, cited-by lists were the main defence against missing a paper through wording. OpenAlex `cites:` or Semantic Scholar citations were run for:
- Rubin et al. PNAS 2024 (W4399208307; 27-30 citers, run 3 times by different agents)
- Babbush 2023 and Kökcü 2024
- Roggero & Carlson PRC 2019 (W2796184659; 108 citers)
- Dornheim PRL 2018 and Nat. Commun. 2025
- Perez-Obiol 2023 (54)
- Su et al. 2021 (W3165437982)
- Chan et al. 2023 (W4322726929)
- Langkabel & Bande
- Mangin-Brinet (CAP)
- Efimov 2021
- Kharazi EUV (0 citers)
- the Local-minima papers (36)
- Al-Hamdani 2021 and two 2024/2025 CC/DMC works
- Chernikov 2015, Steinhoff 2017, G1-G2 PRL
- kilonova opacity papers W2940065607 and W4384281337
- 2401.09551, 2404.04207, 2201.00828, 2508.15935, 2605.22920, 2301.01203

Some cited-by calls hit 429 and were not retried: Babbush 2023 filtered to ionization (C41), and Chernikov filtered on "Mott" (C44).

---

## 4. Date range

- **Search dates:** all queries were run 2026-09-28.
- **Publication window covered:** most arXiv/OpenAlex queries had no lower date bound, sorted by relevance or newest first. Some carried explicit windows:
  - chemistry lens Crossref: 2019+ and 2020+
  - complexity: 2020+ and 2021+
  - qsim_dynamics OpenAlex batch: 2020+
  - resources lens: 2021-2026
  - claims and classical_frontier: 2023-2026 claims and rebuttals
  - red team #2: Crossref from 2024-06-01, plus a post-July-2026 preprint pass
  - C44 cited-by: 2022+ and 2023+
- **Newest items seen:** arXiv submissions from late September 2026. The highest IDs in the notes are 2609.29257, 2609.28643, 2609.28369, 2609.25164 and 2609.24282. The DQI survey covered records through 2026-09-25.
- **Oldest anchors:** classical anchors reach back to the 1990s (Wehlitz 1998 PRL; PRL 81, 1813), plus nucl-th/0408043 and nucl-th/0605013.
- Preprints posted in the last days before 2026-09-28 may not yet have been indexed by the APIs.

---

## 5. Candidate screening process

### 5.1 Discovery (12 lenses → 65 raw candidates, about 150 killed ideas)
- **Two-part filter.** Each lens began from its own angle and applied two filters to every idea:
  - the seven protein-failure lessons L1-L7: weak baseline, solver equivalence, argmin/search over a classical landscape, simulator runtime, information vs computation, model floor, single-family hardness;
  - the brief's exclusions: no protein, generic finance/logistics/ML/crypto/"drug discovery"/"materials discovery", or pure math.
- **Candidates per lens:** algorithms 5, complexity 6, claims 6, amo 6, materials 6, chemistry 6, sciml_inference 6, optimization 6, classical_frontier 4, qsim_dynamics 5, alt_domains 5, resources 4. That makes 65 raw candidates.
- **Kill lists:** about 150 killed-idea entries in total, each with a stated reason (per-lens lists in the evidence bundle and in each file's "Killed" section).
- **Novelty category:** each candidate got a scoped category (A-F) and a provisional verdict (plausible / weak).

### 5.2 Pool (65 raw candidates + kill lists → 50 distinct problems)
`pool_and_shortlist.md` merged duplicates into 50 distinct problems (C01-C50). For each, it records the source lens items ("merged from") and the filter that decided it:
- F-claimed, F-classical, F-quad, F-load, F-sim, F-toy, F-bench, L1-L7.

Result: 6 shortlist, 6 reserve, 38 killed.

### 5.3 Shortlist (6, at most 2 per domain)
The six shortlisted candidates:
- C01 WDM XRTS S_ee(q,w)
- C41 correlated multi-electron ionization
- C14 3D pi-flux quantum spin ice S(q,w)
- C07 hot neutron-rich matter response for supernova neutrino opacities
- C04 kilonova Ln/An expansion opacity
- C44 dense 2D e-h plasma through the exciton Mott crossover

**Selection rule.** The quantum object had to be a real-time or spectral quantum correlator, or a Born-rule sample. It could not be an argmin of a classical energy (L3), and it could not rest on a Grover or amplitude-estimation speedup.

**Reserve (6):**
- C02 WDM conductivity
- C15 2D frustrated-magnet S(q,w)
- C17 Kitaev thermal Hall
- C19 quantum local minima
- C32 SO-coupled f-element exchange
- C34 multinuclear L-edge XAS/RIXS

**Pre-registered kill tests.** Each shortlisted item got a cheap classical kill test before any quantum resource work was allowed.

### 5.4 Deep audits (6 x 3 = 18 notes)
Each candidate was audited independently in three roles:
- **Novelty / prior art:** exact prior work, nearest quantum work, nearest classical work, what has and has not been tested, and a scoped novelty statement.
- **Classical adversary:** the strongest classical families, where exactly they fail, model floor, decision relevance, and the cheapest decisive kill experiment.
- **Resource / break-even:** Toffoli per circuit G, circuit count S, logical qubits, checked against the program screen S*G <~ 1e12.

Verdicts as recorded in the note headers:

| ID | Novelty | Classical | Resources |
|---|---|---|---|
| C01 | WOUNDED (B, high scoop risk) | WOUNDED | WOUNDED (UEG rung later-FT; practical H/CH resource-killed) |
| C04 | WOUNDED (B) | KILLED | KILLED as formulated |
| C07 | WOUNDED (B) | KILLED | KILLED |
| C14 | WOUNDED (B) | WOUNDED (severe) | KILLED as specified |
| C41 | WOUNDED (B) | KILLED | WOUNDED |
| C44 | WOUNDED (B bordering C; the candidate's claimed A was falsified by arXiv:2606.04295) | KILLED | WOUNDED (spectra resource-killed) |

### 5.5 Selection (`selection.md`)
- **Ranking:** C01 > C14 (redesign lane) > C44 (residual) > C41 (residual) > C07 (residual) > C04.
- **Eligible:** only C01, and only conditionally, behind four gates:
  - K-C01a: L5 information test
  - K-C01b: multi-family classical spread at H, r_s = 2, theta 0.5/0.25
  - thermal-state preparation bound
  - resource gate
  - Scoop risk is flagged high.
- **Slots 2 and 3 left empty.** The selection lead declined to fill them. Doing so would have meant accepting a claim that is category 1 only, or a decision flip that nobody has measured.
- **Cross-cutting finding** recorded by selection:
  - the classical wall and the decision-relevant information sit in different regimes;
  - cost is dominated by sampling and state preparation;
  - the model floor is at or above the solver spread.

### 5.6 Red team (C01 only)
- **Reviewer #1 (classical): "not fatal overall, but two sub-claims are dead".**
  - The UEG rung at theta 0.25-0.5 has no classical wall and is validation only. Sources: ESA LFC 2101.05498/2008.02165; real-frequency diagMC 2205.13595 and 2311.05611; FT-AFQMC 2012.12228; pseudo-fermion 2603.28000.
  - The CH rung falls outside the model and resource envelope.
  - The H wall at r_s = 2, theta 0.5/0.25 (2507.00688) is a validation gap from a single family, not a demonstrated disagreement between families. A variational free-energy thermal state exists there (2507.18540).
  - K-C01a has to be reframed: temperature is model-free from the ITCF, so the test must be on (n_e, Z, nu).
- **Reviewer #2 (prior art): "WOUNDED, not fatal; significance is the main weakness".**
  - No quantum S_ee(q,w)/XRTS paper was found, so category B stands.
  - Every algorithmic component is already published.
  - The XRTS community names non-equilibrium, not equilibrium theta < 0.5, as its frontier (2604.23687).
  - Scoop risk is high (Sandia; Google's Grand Challenge 2511.09124).

`selection.md` records the four gates. The red-team revisions add to those gates; they do not replace them.

---

## 6. Inclusion and exclusion criteria (as applied)

**Inclusion (required for shortlist):**
1. A practical problem with a clear INPUT → OUTPUT and a measurable physical output with real experimental consumers.
2. Strong classical algorithms exist, and a named classical twin can be tuned with comparable effort.
3. The quantum algorithm attacks the actual bottleneck: a real-time or spectral quantum correlator, or a Born-rule sample of a many-body state.
4. A scaling variable and a benchmark ladder, preferably with an exact classical validation rung.
5. Novelty category B or C in the scoped search, or a D/E subsection with a genuinely distinct mechanism.

**Exclusion (any one kills; the codes are those used in `pool_and_shortlist.md`):**
- **F-claimed:** already claimed or established, with no materially distinct subproblem left. Examples: stopping power 2308.12352; opacity 2607.02811; WDM conductivity OSTI 10.2172/3363975.
- **F-classical / L7:** the strongest classical method closes the gap, or hardness rests on a single family.
- **F-quad / L3:** a quadratic or low-polynomial speedup, or an argmin/search over a classical landscape. Judged against Babbush et al. 2021 (arXiv:2011.04149).
- **F-load:** state preparation, oracle, data loading or readout dominates the cost.
- **F-sim:** classically simulable in the relevant regime (high-T, short-time, 1D, small active space, sign-free).
- **F-toy / F-bench:** no practical user, or no fair benchmark path.
- **L5:** the regime is classically computable where the output is informative, and hard only where it carries little information.
- **L6:** model error at or above solver error.
- **Resource screen:** S*G <~ 1e12 Toffoli for early fault tolerance, with later-FT rates stated separately. Simulator runtime never counts as physical runtime (L4).
- **Domain exclusions from the brief:** protein problems, generic finance/logistics/ML/crypto/drug or materials discovery, pure math.

---

## 7. Key papers (verified in the notes)

Verification route as recorded: arXiv abs/html/API, Crossref, OpenAlex, Semantic Scholar or OSTI record. Items the notes mark [UNVERIFIED] are listed in section 9.

**Break-even and framing**
- Babbush et al., "Focus beyond quadratic speedups", PRX Quantum 2, 010103 (2021), arXiv:2011.04149, doi:10.1103/prxquantum.2.010103
- Su, Berry, Wiebe, Rubin, Babbush, PRX Quantum 2, 040332 (2021), arXiv:2105.12767
- Babbush et al., Nat. Commun. 14, 4058 (2023), arXiv:2301.01203
- Chen & Chan, PRL 137, 130601 (2026), arXiv:2508.15765, doi:10.1103/v2ms-wmz1
- Google Quantum AI, "The Grand Challenge of Quantum Applications", PRX Quantum 7, 020101 (2026), arXiv:2511.09124, doi:10.1103/6r9l-lynr

**Dequantized or contested claims (used for kills)**
- High-T Gibbs states: Bakshi-Liu-Moitra-Tang arXiv:2403.16850
- Noisy circuits: Schuster-Yin-Gao-Yao arXiv:2407.12768
- IBM kicked Ising: TN-BP arXiv:2306.14887; sparse Pauli dynamics 2306.16372, 2308.05077; IF-BP 2504.07344
- D-Wave quench dynamics: claim 2403.00910 (Science 388, 199 (2025)); challenges 2503.05693, 2503.08247, 2609.01719
- GBS vibronic spectra: Oh et al. arXiv:2202.01861
- 1D Fermi-Hubbard quench: claim 2605.04025, challenge 2606.04771
- Liquid-state NMR: 2508.06448
- SQD/QSCI: 2608.11569, 2608.05314
- Rydberg MIS: Andrist et al. 2307.09442
- QMCMC: Orfi & Sels 2403.03087
- FeMoco: near-classically solved, 2601.04621
- Fe4S4: 2603.28648
- DQI/OPI: 2510.10967, 2509.14509, 2607.28120, 2606.13570

**C01 (finalist)**
Quantum side:
- Rubin et al., PNAS 121, e2317772121 (2024), arXiv:2308.12352 (OpenAlex W4399208307)
- Pathak, Kononov, Baczewski, arXiv:2607.02811
- Nelson & Baczewski, arXiv:2605.22920 (announces WDM linear response as ongoing work)
- Kononov et al., OSTI doi:10.2172/3363975 (metadata only)
- Baczewski SNL report doi:10.2172/3028616
- Kunitsa et al., arXiv:2508.15935
- Cruz, Wild, Bañuls, Cirac, doi:10.1103/lpz2-j7vg
- Becker, Rouze, Salzmann, arXiv:2604.15263
- Pennati et al. roadmap, arXiv:2605.07722, doi:10.1145/3774895.3815547

Classical side:
- Moldabekov et al., arXiv:2507.00688 (MRE 11, 025401 (2026))
- Dornheim et al., arXiv:2402.19113, Nat. Commun. 16, 5103 (2025), doi:10.1038/s41467-025-60278-3
- Taylor-xi arXiv:2509.11317; xi-extrapolation 2308.06071
- Model-free ITCF 2211.00579; review 2604.25735 (doi:10.1007/s41614-026-00227-9); SIF-free thermometry 2510.26747
- Hentschel et al. 2408.15346
- UEG finite size 2004.13429
- pseudo-fermion 2603.28000 (doi:10.1103/6bdz-8gmq)
- Li, Xie, Dong, Wang 2507.18540
- Morresi et al. 2506.10113
- Tupitsyn & Prokof'ev 2311.05611; LeBlanc et al. 2205.13595
- ESA 2008.02165, 2101.05498
- Dornheim et al. XRTS overview 2604.23687
- Regan et al., PRL 109, 265003 (2012), doi:10.1103/PhysRevLett.109.265003
- Bellenbaum et al. 2503.14014
- Bespalov et al. 2509.10107, doi:10.1103/86cw-8wm5

**Other audited candidates (load-bearing kills)**
- **C07:**
  - Ma et al., PRL 132, 232502 (2024), arXiv:2306.04500, doi:10.1103/PhysRevLett.132.232502
  - Watson et al. arXiv:2312.05344
  - Melson et al. arXiv:1504.07631
  - Bartl et al., PRD 94, 083009 (2016), arXiv:1608.05037
  - Lu et al., PRL 125, 192502, arXiv:1912.05105
- **C14:**
  - Gao et al. arXiv:2404.04207, Nat. Phys. 21, 1203 (2025), doi:10.1038/s41567-025-02922-9
  - Gao et al. arXiv:2601.03202, PRL 136, 256703 (2026), doi:10.1103/svt2-m3pp
  - Poree et al. arXiv:2304.05452
  - vacancies 2609.28643
  - Ce2Sn2O7 ordering 2607.12274
  - Google 2D XY magnon response 2607.13301
- **C41:**
  - Zielinski, Majety, Scrinzi, PRA 93, 023406 (2016)
  - Colgan et al., PRL 93, 053201 (2004)
  - Kharazi EUV arXiv:2602.20234
  - Chan et al. grid methods arXiv:2202.05864
- **C44:**
  - Klymenko et al. arXiv:2606.04295 (falsified scoped category A)
  - Dogadov et al. arXiv:2604.06897
  - 2601.17167
  - Nys et al. arXiv:2403.07447 (Nat. Commun. 15, 9404 (2024))
  - δNEGF 2606.10773
  - Steinhoff et al. doi:10.1038/s41467-017-01298-6
- **C04:**
  - 2607.02811 (the only quantum-opacity paper found)
  - 2501.13286
  - 2606.04868
  - staa485 / stad2053 cited-by sets

---

## 8. Duplicate handling

1. **Cross-lens merge by problem, not by wording.** `pool_and_shortlist.md` gives, for each of the 50 pool entries, the lens items it absorbed:
   - C01 = algorithms:C1 + complexity:C-c + alt_domains:C1. qsim_dynamics explicitly deduplicated its XRTS item and kept only the distinct omega→0 transport regime, which became C02.
   - C14 = claims:C2 + materials:C1 + sciml:C2. sciml:C4 was folded in as the sign-free validation rung.
   - C15 merged four lenses.
   - C24 merged the whole high-T spin/NMR family across 5 lenses.
   - C43, C47 and C48 merged families of polynomial-wall AMO data, PDE/linear-algebra solvers and classical-landscape optimization.
2. **Family-level merges for killed material.** Related kills were grouped into one pool row with one decisive reason, so that the same idea could not be counted twice under different names. Examples:
   - C06: static WDM, dense-H, H-He, Earth-core Fe
   - C22: annealer beyond-classical claims
   - C39: ground-state chemistry energetics
   - C50: dequantized demonstrations
3. **Folding instead of duplicating.** Some items became extensions or validation rungs of a surviving candidate rather than separate entries:
   - C16 (THz 2DCS) became an extension of C14/C15.
   - C18 (real-time vs QMC+AC) became C14's certified 0-flux validation rung.
   - Warm-dense G_ei was folded into C01/C02.
4. **Domain cap.** At most 2 shortlist slots per domain. C14 and C15 share a topic family, so only C14 was shortlisted. C04 and C41 are both AMO/atomic, and were kept because their mechanisms and users differ.
5. **Prior-week exclusions.** Topics already claimed or killed earlier this week were reused as exclusions, not re-searched. Examples: OPV/vibronic, where C37 was killed with reference to the Dorfner et al. MPS-vs-ML-MCTDH result; doped-Mott transport; and Anderson-Newns, which was kept only as a crossover audit (C40).
6. **Repeated citations across agents.** Several agents independently verified the same anchor papers (2308.12352, 2607.02811, 2011.04149, 2105.12767, 2403.16850). They count once in section 7.
7. **Correction recorded, not overwritten.** The claims lens appends a dated correction: arXiv:2504.07344 simulates the IBM kicked-Ising experiment, not the D-Wave one.

---

## 9. Novelty uncertainty: what could have been missed

Every novelty category in this round is **scoped**. The standard form, taken from `audit_C01_novelty.md` section 10, reads: "in sources X searched through 2026-09-28, we found A, B, C but no study of D against E, F". "Not found" is not proof of absence. The known gaps:

1. **No general web search.** WebSearch was exhausted (200/200) before the round began. No Google or Google Scholar was used, and one Bing attempt failed. Group pages, blogs, talk slides, press releases and news items were therefore not searched. Red team #2 names this as a coverage gap (F10).
2. **Journal-only and paywalled literature.** Keyword searches covered arXiv abstracts. Crossref and OpenAlex keyword relevance was noisy and often rate-limited. Papers without an arXiv preprint can be missed, especially in JQSRT, ApJS, J. Phys. B and ADNDT (AMO lens), and chemistry journals. Paywalls blocked reading: nature.com (login) and APS abstract pages (403). In those cases only metadata or OpenAlex-reconstructed abstracts were read.
3. **ChemRxiv.** It was never searched as a repository. ChemRxiv items were reached only through Crossref DOI lookups of specific known DOIs: 10.26434/chemrxiv.15006382, 10.26434/chemrxiv-2023-jnt7m, 10.26434/chemrxiv-2024-nwbqd. Chemistry-side "not found" statements therefore do not cover ChemRxiv-only preprints. This matters most for the chemistry lens and the killed chemistry rows C32-C39.
4. **Patents.** Not searched. C04 novelty and C44 novelty state this explicitly, and C07 novelty judged patents not relevant. Industrial quantum groups (quantum-hardware vendors, quantum-software firms) may file before publishing.
5. **Unpublished and in-preparation work.** Known in-preparation items could not be read:
   - Bobrow, Chien, Kononov, Nelson, Zhao, Baczewski, Kovalsky, "Assessing the cost of thermal state preparation for quantum simulations of warm dense matter". It is cited as in preparation in 2607.02811 and was not on arXiv as of 2026-09-28.
   - The ongoing WDM linear-response work announced in arXiv:2605.22920.

   Other industrial groups were only reachable through generic abstract searches, which returned nothing: PsiQuantum, Quantinuum, IBM, Microsoft, Phasecraft, QSimulate, Riverlane, Algorithmiq, BlueQubit. Internal industrial or national-lab work that has not been posted would be missed entirely. Red team #2 rates scoop risk for C01 as HIGH.
6. **Theses, conference proceedings and reports.** Theses were not found through these APIs (C07). Conference proceedings were reached only via Crossref (C44). OSTI records had no abstracts, and OSTI search failed.
7. **Domain databases not queried.** No log shows INSPIRE-HEP or NASA ADS being queried; C07 novelty recommends INSPIRE-HEP as a follow-up. Both are primary indexes for the nuclear-astrophysics candidates (C07, C08-C13) and the astrophysical opacity candidates (C03, C04).
8. **Non-English literature.** No log records a non-English query or source. Every query was in English. Chinese-, Japanese- and Russian-language journals, and non-English national-lab reports, are covered only as far as Crossref or OpenAlex index them under English metadata.
9. **Indexing and wording limits.**
   - arXiv abstract search does not reliably index subscripted chemical formulas (KYbSe2, MoTe2, Ce2Zr2O7).
   - Keyword-literal AND search misses paraphrases.
   - The chemistry lens looked only at the top 20 and top 12 results per query.
   - Cited-by lists came from OpenAlex and Semantic Scholar, not Web of Science or Scopus. Some cited-by calls failed with 429 and were not retried.
10. **Recency.** Preprints from the final days before 2026-09-28 may not have been indexed yet. Several decisive items were only weeks old: 2609.28643, 2609.18584, 2609.01719. Novelty can therefore change quickly, especially for C01.
11. **Items the notes mark [UNVERIFIED]** (not independently checked):
    - exact r_s/T of 2205.13595
    - Davis 2016 state points
    - Marciniak et al. Nature 2022 (optimization kill)
    - SrCu2(BO3)2 finite-T iPEPS claim (materials kill)
    - "NQS ground states <=108 spins" for QSI (C14)
    - the auditors' own Toffoli/shot estimates, marked [ESTIMATE] or [UNVERIFIED] throughout
    - the ~1.6e3x internal inconsistency in the Rubin 2024 per-a.u. cost, which remains unresolved
    - Kononov et al. OSTI 10.2172/3363975: metadata only, not re-verified in audit_C01_classical

---

## 10. Reproducibility pointers

- Complete per-agent query logs: the "Query log" section of every file in `research/reports/lit_work/`. The C04 classical, C14 novelty, C41 novelty and C44 classical/resources notes put the log near the top; all other notes put it at the end.
- Pool, merge map and filters: `lit_work/pool_and_shortlist.md`.
- Final ranking and gates: `lit_work/selection.md`.
- Red-team revisions to the gates: `lit_work/redteam_C01_classical.md` section 7 and `lit_work/redteam_C01_priorart.md` "Required revisions".
