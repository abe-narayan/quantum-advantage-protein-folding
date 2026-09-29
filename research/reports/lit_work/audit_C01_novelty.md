# Novelty audit C01: quantum real-time S_ee(q,w) for XRTS of warm dense matter

Auditor role: novelty / prior-art. Date: 2026-09-28. Status: COMPLETE.
Verdict: **WOUNDED** (scoped category B survives; the gap is material but thin and under active, publicly announced pursuit by the Sandia group; the information-value case over model-free ITCF is unproven).

WebSearch budget was exhausted this session, so every search went through the arXiv API (export.arxiv.org), arXiv abs/html pages, OpenAlex (search and `cites:` filter), Crossref and the OSTI records API. The OSTI search endpoint returned non-JSON, so only individual OSTI records were read. Every paper cited below was verified through an arXiv abs/html page, an OpenAlex record, or Crossref, unless it is marked otherwise.

---

## 1. Classification

**Category B (scoped), with high scoop risk.**
- Quantum methods exist nearby:
  - WDM stopping power: Rubin et al. 2024
  - WDM opacity: Pathak, Kononov, Baczewski 2026
  - WDM conductivity resource estimates: Kononov et al., OSTI 2025
  - a generic electronic DSF quantum algorithm (T=0, core-level EELS): Kunitsa et al. 2025
  - finite-T response-function algorithms: Cruz, Wild, Bañuls, Cirac 2025; Nelson & Baczewski 2026
  - spin DSF on hardware (2603.15608, 2607.07138, 2607.02673)
- None computes the thermal electronic S_ee(q,w) of warm dense matter for XRTS, and none compares against PIMC+AC or model-free ITCF.
- It is not category A: the idea is explicitly flagged as ongoing work. Nelson & Baczewski, arXiv:2605.22920 (May 2026), write: "Ongoing work is aimed at extending the ROQAM at nonzero temperature to applications in high-energy density physics, e.g., calculating linear response functions of warm dense matter". They cite Baczewski et al. PRL 116, 115004 (2016), "X-ray Thomson scattering in warm dense matter without the Chihara decomposition", and the WDM density-response review (Dornheim et al., PoP 30, 2023).

## 2. EXACT PRIOR WORK (quantum S_ee(q,w) for XRTS/WDM)
None found in the sources searched. The closest is the announced intent in arXiv:2605.22920 above, which is not yet a paper.

## 3. NEAREST QUANTUM WORK (verified)
| Work | What it does | Distance from C01 |
|---|---|---|
| Rubin, Berry, Kononov, Malone, Khattar, White, Lee, Neven, Babbush, Baczewski, PNAS 121 e2317772121 (2024), arXiv:2308.12352, OpenAlex W4399208307 | First-quantized plane-wave electron dynamics for stopping power in WDM; resource estimates | Same machinery; different observable (projectile energy loss, not the thermal density correlator); no thermal-state preparation beyond sampled determinants |
| Pathak, Kononov, Baczewski, arXiv:2607.02811 (2026-07-02) | Opacity via a Pauli-Fierz Hamiltonian; momentum-resolved photon-register readout gives "a direct relationship between qubit count and spectral range/resolution"; solar iron at 2.26e6 K; Coulomb exponentiation cost about 2395*eta(eta-1)/2 Toffolis (from the Rubin implementation); thermal ensemble through shots over Slater determinants | Spectral readout of a dense-plasma response at q near 0 (dipole). XRTS needs finite-q density response. The full text has no mention of Thomson, XRTS or structure factor. It cites the in-preparation work [UNVERIFIED, in prep] Bobrow, Chien, Kononov, Nelson, Zhao, Baczewski, Kovalsky (2026), "Assessing the cost of thermal state preparation for quantum simulations of warm dense matter". Funding line: DOE FES "Foundations for quantum simulation of warm dense matter" |
| Nelson & Baczewski, arXiv:2605.22920 (2026-05) "Estimating Green's functions with a robust quantum Arnoldi method" (ROQAM) | Krylov/orthogonal-polynomial GF estimation; nonzero-T GFs via TFD with one Krylov subspace; impurity-model resource estimates | Mechanism for finite-T response; states WDM linear response as ongoing work (scoop) |
| Kononov et al., OSTI doi:10.2172/3363975 (2025-05, conference) "Improving WDM conductivity predictions: ... to estimating quantum resource requirements" | WDM conductivity plus quantum resource estimates | Adjacent observable (current-current at q=0) |
| Kunitsa, Dhawan, Fomichev, Arrazola, Zhang, Stetina, arXiv:2508.15935 (2025) "Quantum Simulation of EELS for Battery Materials" | General quantum algorithm for the electronic DSF (momentum-resolved) via off-diagonal time-domain GF; O K-edge Li2MnO3, 18-orbital active space, 3.25e8 T depth, 100 logical qubits, about 1e4 shots | Same observable class (electronic S(q,w)), but T=0, active-space cluster, core-level. No thermal ensemble, no plane-wave continuum, no PIMC comparator. **Reduces the novelty of "quantum electronic DSF algorithm" to that of an application/regime** |
| Cruz, Wild, Bañuls, Cirac, doi:10.1103/lpz2-j7vg (2025) "Quantum simulation of dynamical response functions of equilibrium states" | Energy-filter route to microcanonical/canonical response functions without preparing the Gibbs state; demonstrated on free-fermion conductivity | Provides the thermal-response primitive C01 needs |
| Babbush et al., Nat. Commun. 14, 4058 (2023), arXiv:2301.01203 | First-quantized exact dynamics vs RT-TDHF/TDDFT: exponentially less space, polynomially fewer operations in basis size; "quantum speedup is most pronounced for finite temperature simulations" | The theoretical basis for C01. The speedup it claims over mean-field is **polynomial in basis size (exponential in space)**, not exponential in accuracy |
| Chen & Chan, arXiv:2508.15765 / doi:10.1103/v2ms-wmz1 (2026) | Robust quantum speedups precisely where classical heuristics succeed | Frames any WDM gain against TDDFT as a polynomial, not exponential, speedup. No WDM content |
| Spin DSF: arXiv:2603.15608 (KCuF3 vs INS, 50 qubits); arXiv:2607.07138 (pumping approach, Quantinuum Reimei); arXiv:2607.02673 (quench spectroscopy, L=101) | Hardware DSF for spin chains | Different physics; they show that "DSF vs experiment" is already an established genre |
| Roggero & Carlson, PRC 100, 034610 (2019), "Dynamic linear response quantum algorithm", OpenAlex W2796184659 (108 citing works; filtered list checked) | Nuclear response functions | Mechanism-level precedent. None of the citing works in the filtered list concerns an electron plasma |
| Pennati et al., arXiv:2605.07722 / doi:10.1145/3774895.3815547 (2026), Post-Moore plasma roadmap | Lists "finite-temperature response" among WDM/ICF quantum targets, generically | Qualitative mention only |
| Vorberger et al., "Roadmap for warm dense matter physics", arXiv:2505.02494, doi:10.1088/1361-6587/ae672c | Mentions quantum computing only as a future TD-DFT benchmark | Qualitative |

## 4. NEAREST CLASSICAL WORK (verified)
- PIMC of the UEG DSF through a stochastically sampled dynamic LFC: Dornheim et al., PRL 121, 255001 (2018), OpenAlex W2899027045. Finite-size study, arXiv:2004.13429: reconstructed S(q,w) "not afflicted with any finite-size effects for as few as N=14 electrons" at WDM conditions.
- PIMC with xi-extrapolation reproduces the NIF Be XRTS: Dornheim et al., arXiv:2402.19113, Nat. Commun. 16, 5103 (2025), doi:10.1038/s41467-025-60278-3. Taylor-xi: arXiv:2509.11317 (Phys. Rev. doi:10.1103/53fr-mnm6).
- Analytic continuation of the UEG DSF:
  - MEM: Chuna et al., arXiv:2503.20433 (doi:10.1103/4d4b-kgtk)
  - MEM plus PyLIT across temperature: Chuna, Böhme, Dornheim, arXiv:2603.27212
  - PyLIT: CPC 319, 109904 (2026), doi:10.1016/j.cpc.2025.109904
- Model-free ITCF:
  - arXiv:2211.00579
  - review: Gawne et al., arXiv:2604.25735 / doi:10.1007/s41614-026-00227-9
  - guidelines: Böhme et al., doi:10.1063/5.0304837 (2026)
  - SIF-free thermometry: Gawne, **Kononov, Baczewski** et al., arXiv:2510.26747. This shows the Sandia quantum group already co-authors XRTS analysis.
- LR-TDDFT and Liouville-Lanczos: arXiv:2502.04921. ITCF-constrained TDDFT: arXiv:2510.01875. Mixed stochastic and orbital-free TDDFT DSF: White, arXiv:2410.23599. Real-time TDDFT tutorial for HED DSF: Kononov, Nguyen, Baczewski, arXiv:2511.14643 / doi:10.1063/5.0312253. Nonequilibrium (isochorically heated) LR-TDDFT DSF: arXiv:2402.09005.
- Wave-packet DSF for H: arXiv:2407.08875. xDAVE: arXiv:2604.27237 (doi:10.1063/5.0340851). Chihara plus f-sum repair: arXiv:2607.25481. Free-bound transitions: doi:10.1002/ctpp.70149 (Böhme, Fletcher, Baczewski et al. 2026).
- The sign-problem frontier is moving (it attacks the claimed quantum window):
  - pseudo-fermion method reaches theta=0.0625 at 1 <= r_s <= 2 for UEG energies (N=33), arXiv:2603.28000 (doi:10.1103/6bdz-8gmq)
  - hydrodynamic backflow, arXiv:2604.01963
  - learned sign structure, arXiv:2607.15060
  - reweighting estimators for density response, doi:10.1063/5.0340968
  - these results concern energies or static response. None yet delivers the ITCF at theta<0.5 for N>=32 (not established in the sources read).
- Dense-hydrogen benchmark review: Bonitz et al., arXiv:2405.10627. It names the sign problem, approximate xc functionals and chemical-model inconsistencies as method limits, and gives no single quantified multi-family disagreement point in the abstract.

## 5. WHAT HAS BEEN TESTED
- Quantum: stopping power, opacity and conductivity (resource estimates only). Electronic DSF at T=0 in an active space (resource estimates). Finite-T response primitives on toy models (free fermions, impurity models). Spin DSF on hardware vs INS.
- Classical: PIMC ITCF (quasi-exact where the sign is manageable) vs NIF Be XRTS (agreement). PIMC+MEM/PyLIT S(q,w) for the UEG across theta. LR-TDDFT/LL/stochastic TDDFT vs XRTS. Model-free ITCF thermometry, normalization and Rayleigh weight from experimental spectra.

## 6. WHAT HAS NOT BEEN TESTED
- Any quantum algorithm (or resource estimate) for the thermal S_ee(q,w) of WDM (UEG, H, Be, CH) at XRTS q, with thermal-state preparation costed.
- Any comparison of a quantum-computed S(q,w) (or its Laplace transform) against quasi-exact PIMC F(q,tau). The UEG gives a unique exact validation route that the EELS, opacity and stopping-power proposals lack.
- An information test: whether real-frequency S narrows the (rho,T,Z) posterior beyond model-free ITCF analysis. No source found quantifies this, in either direction.
- A quantified map of where the PIMC ITCF (with xi, Taylor-xi, pseudo-fermion or backflow) fails at XRTS-relevant (r_s, theta, q, N>=32).

## 7. WHY THE GAP IS MATERIAL (not cosmetic)
1. Thermal ensemble plus continuum electrons plus finite q is a different algorithmic bottleneck from T=0 active-space EELS: Gibbs/microcanonical preparation for eta = 32-128 plane-wave electrons. Its cost is exactly what Sandia's in-preparation paper addresses, which shows the cost is open and non-trivial.
2. It is the only quantum-dynamics target in HED with an exact classical cross-check (the PIMC ITCF on the UEG). That makes a FULL vs ABLATION-type validation possible. The stopping-power, opacity and EELS proposals lack this.
3. The observable feeds a real diagnostic decision (inferring rho, T and Z from NIF/LCLS/EuXFEL XRTS), where model disagreement is documented: the Chihara-based temperature is inconsistent without free-bound terms (doi:10.1002/ctpp.70149), and Chihara violates the f-sum rule (arXiv:2607.25481).

## 8. WHY THE GAP IS THIN / THE WOUNDS
- **W1, scoop.** The Sandia team (Baczewski, Kononov, Nelson, Bobrow, Chien, Kovalsky, Zhao) has (a) a funded DOE FES project, "Foundations for quantum simulation of WDM"; (b) finite-T quantum GF machinery (ROQAM) whose paper names WDM linear response as ongoing work; (c) thermal-preparation costing in preparation; (d) an RT-TDDFT DSF tutorial and XRTS co-authorships. The expected time to their paper is short, perhaps months. [Inference, not verified.]
- **W2, information value (L5).** In equilibrium, F(q,tau) and S(q,w) are related by a bijective two-sided Laplace transform. Where PIMC works, the model-free program already compares theory and experiment in the tau domain without any real-frequency theory (2402.19113, 2604.25735). A quantum real-frequency S therefore adds decision value only (i) where the PIMC ITCF fails (low theta, higher Z, N>=32), (ii) out of equilibrium (XFEL isochoric heating; see 2402.09005 and 2510.26747 on non-equilibrium detection), where ITCF and PIMC do not apply by construction, or (iii) where finite spectral windows and noise make the tau route lose information. None of these is quantified. If (i) shrinks under pseudo-fermion or Taylor-xi, the equilibrium case collapses toward L5 "gain < 2".
- **W3, advantage type.** Against TDDFT the quantum gain is polynomial in basis size (Babbush 2023; Chen & Chan 2026). An exponential advantage requires that both PIMC and TDDFT fail, which means low theta, where N>=32 and a small instrument width (long t) drive G up.
- **W4, cost** (auditor order-of-magnitude estimate, [UNVERIFIED, not from sources]).
  - Verified input: the Coulomb exponentiation costs about 2395*eta(eta-1)/2 Toffolis per step (Rubin implementation, as quoted in 2607.02811). That is about 1.2e6 at eta=32 and 1.9e7 at eta=128.
  - Assumptions: 1e3-1e4 steps to reach t of about hbar/(1 eV), plus thermal preparation.
  - Result: G is about 1e9-1e11 per correlator sample, and S (time points x shots) is about 1e6-1e8. So S*G is about 1e15-1e19, which is likely above the 1e12 screen. The Sandia opacity estimates are "comparable to" stopping power, which is consistent with this.
- **W5, finite N.** On the classical side, N=14 suffices for S(q,w) through the dynamic LFC (2004.13429). For a direct real-time quantum correlator at finite N, the spectrum is discrete. Plasmon damping and Landau-damping shapes at small q need broadening or twist averaging. Not addressed in any source.

## 9. WHY IT COULD STILL BE A NEW PAPER
A paper would be publishable if it pre-empts or differentiates from Sandia. Two options:
- (a) The first end-to-end resource estimate for the thermal S_ee(q,w) at XRTS geometries, with thermal preparation costed, plus a UEG validation protocol against the PIMC F(q,tau).
- (b) A sharper subsection: **non-equilibrium (two-temperature, XFEL-isochorically heated) XRTS spectra**. There, PIMC and the ITCF are inapplicable by construction, and the competitors are RT/LR-TDDFT with adiabatic kernels and NEGF (G1-G2). This makes the multi-family wall more plausible. It carries an L6 model-floor risk: specifying the non-equilibrium initial state.
- (c) Alternatively, a negative or information-theoretic paper: quantify whether real-frequency S adds posterior information beyond the model-free ITCF. The program can publish this regardless of the quantum outcome.

## 10. SCOPED NOVELTY STATEMENT
"In the arXiv API (abstract searches), arXiv abs/html full texts of 2607.02811, 2605.22920, 2605.07722, 2505.02494, 2511.14643 and 2508.15765, OpenAlex search and cited-by lists of Rubin et al. PNAS 2024 (W4399208307, 30 citers), Babbush et al. Nat. Commun. 2023 (W4383695264), Kökcü et al. Nat. Commun. 2024 (W4396721271), Roggero & Carlson PRC 2019 (W2796184659), Dornheim et al. PRL 2018 (W2899027045) and Dornheim et al. Nat. Commun. 2025 (W4410958110, 47 citers), Crossref, and OSTI records, searched through 2026-09-28, we found quantum protocols for WDM stopping power (2308.12352), opacity (2607.02811) and conductivity (OSTI 10.2172/3363975), a T=0 active-space electronic DSF algorithm for EELS (2508.15935), finite-temperature quantum response and Green's-function methods (doi:10.1103/lpz2-j7vg; 2605.22920, which announces ongoing WDM linear-response work), and spin-chain DSF hardware demonstrations (2603.15608, 2607.07138, 2607.02673). We found no study of the quantum-computed thermal electronic S_ee(q,w) of warm dense matter at XRTS wavevectors (D) compared against PIMC plus analytic continuation (E) or model-free ITCF analysis plus LR/RT-TDDFT (F)."

## 11. Answers to the audit questions (novelty-auditor scope)
1. **L5 information test.** No source quantifies it. The model-free ITCF literature argues that in equilibrium the tau domain carries the diagnostic information (T, normalization, Rayleigh weight, density). This is the main existential threat. Run this test first.
2. **Sign < 1e-4 location.** Not quantified in the sources read. The frontier is moving: xi-extrapolation reaches NIF Be; pseudo-fermion reaches theta=0.0625 for energies (N=33). ITCF-level reach at theta<0.5, N>=32 is not established.
3. **Named multi-family disagreement point.** None found with TDDFT vs PIMC+AC vs stochastic TDDFT beyond experimental error. The documented disagreements are Chihara vs ab initio (free-bound terms, f-sum rule), and PIMC resolved them where it applied.
4. **G and S.** Only the per-step Coulomb cost is verified. The auditor estimate S*G ~ 1e15-1e19 is [UNVERIFIED] and likely fails the 1e12 screen.
5. **Finite N.** Classically N=14 suffices through the dynamic LFC (2004.13429). For a direct quantum real-time correlator, the small-q damping shapes need care. Open.
6. **Scoop risk.** HIGH. There is explicit public intent (2605.22920), a funded program, thermal-preparation costing in preparation, and XRTS co-authorships.

## 12. Query log (2026-09-28)
- WebSearch: 2 attempts, both refused (session budget of 200/200 exhausted).
- arXiv API:
  - `all:"dynamic structure factor" AND all:quantum AND (all:"warm dense" OR all:"electron gas")`
  - `abs:"warm dense" AND (abs:"quantum computer" OR ... "fault-tolerant")`: returned 2605.07722, 2308.12352
  - HED/Thomson/dense plasma/opacity + quantum computing: 429 at first; the retry returned 2607.02811, 2605.07722, 2308.12352
  - `ti:"time-dependent density functional theory" AND ti:"high-energy density"`: 2511.14643
  - jellium/UEG/homogeneous electron gas + quantum computing: 10 hits, no finite-T response
  - DSF + quantum computer/algorithm: 2607.07138, 2607.02673, 2603.15608, 2508.15935, 2410.03958, 1910.14213
  - inelastic x-ray scattering/Compton + quantum algorithm: 2602.20270 (RIXS), others irrelevant
  - thermal/Gibbs/finite-T + first quantization/plane wave + quantum algorithm: 2308.12352, 2301.01203, 2111.12471
  - ITCF + quantum computer: 2112.02764 (hybrid ITCF algorithm, generic), 2607.10765
  - DSF + WDM/electron liquid/Thomson, 2024-06 onward: 20 classical papers (listed in section 4)
  - sign problem + WDM/electron gas, 2023 onward: 17 papers (pseudo-fermion, backflow, learned sign, Taylor-xi, reweighting)
  - finite-size DSF UEG: 2004.13429
  - nonequilibrium/ultrafast + XRTS/DSF + WDM: 2402.09005, 2411.06830
  - authors Baczewski/Kononov/Bobrow: 2605.22920, 2605.11308, 2607.02811, 2511.14643, 2510.26747, 2602.22540
  - `ti:"robust quantum speedups"`: 2508.15765
  - plasmon/density response + electron gas + quantum computer: none relevant
- arXiv html full-text scans:
  - 2605.07722: WDM, "finite-temperature response", Gibbs
  - 2505.02494: quantum computing mentions only
  - 2607.02811: no Thomson/XRTS/DSF; references extracted
  - 2511.14643: no quantum-computing XRTS
  - 2602.22540: no WDM
  - 2605.22920: WDM linear response flagged as ongoing work
  - 2508.15765: no WDM
- OpenAlex:
  - search "quantum algorithm dynamic structure factor warm dense matter"; "quantum computer X-ray Thomson scattering" (noise)
  - title.search "roadmap warm dense matter"; "quantum computing"+"plasma" (17 hits)
  - cites: Rubin 2024 (W4399208307|W4386184940, 30), Babbush 2023|Kökcü 2024 (56), Roggero 2019 (filtered), Dornheim PRL 2018 and PoP 2023 (filtered for quantum computing: 0), Dornheim Nat. Commun. 2025 (47, 0 quantum-computing)
- Crossref: 10.2172/3363975; query "quantum computing warm dense matter" (found OSTI 3028616, 2005714, 2005523)
- OSTI: records 3028616, 2005714, 3363975 read (no abstracts); search API failed.
