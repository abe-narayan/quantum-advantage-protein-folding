# Novelty memos

_Discovery sprint, 2026-09-27. Each memo gives: the claim whose novelty is at stake, the search performed (scope, dates, tools), the nearest prior art found, what is and is not new, and the verdict. Wording rule: "the literature search found no evidence of X under scope Y". It never says "X has never been done". The literature-phase bibliography is `research/literature/BIBLIOGRAPHY.md`; keys like [F34] refer to it._

**Search budget disclosure.** The session's WebSearch budget (200 calls) was exhausted before this memo was written. Searches below used the arXiv API (export.arxiv.org, via WebFetch) and the literature-phase records. They are narrower than a full web search, and each memo states that limit.

---

## NM-1 · Program C (QM-19/20/21): protein ¹H dipolar spin dynamics as a quantum forward model for structure, with a hardness–identifiability gate

**Claim at stake.** Structural (geometric) information in protein ¹H many-body spin dynamics lies in the part of the dynamics that the best classical approximation cannot reproduce. A quantum simulator of the forward model would therefore extract structure that a classical inversion cannot.

**Search.**
- arXiv API, 2026-09-27: title/abstract searches for NMR ∧ quantum ∧ (structure ∨ classically ∨ simulate); "Pauli propagation" ∧ spin; NMR ∧ "quantum advantage"; protein ∧ (spin diffusion ∨ dipolar) ∧ "quantum computer"; titles "classical spin simulations", "Digital quantum simulation of NMR", "spinDMFT".
- The literature-phase F-domain notes (`research/literature/domain_notes/lit_F_claims.md`), which cover OTOC/echoes and the NMR geometry demo.
- No general web search (budget exhausted).

**Nearest prior art (verified on arXiv).**

| Work | What it does | Relation |
|---|---|---|
| O'Brien, Ioffe, Su, Fushman, Neven, Babbush, Smelyanskiy, *PRX Quantum* 3, 030345 (2022), arXiv:2109.02163 | Quantum algorithm to learn the anisotropic dipolar Hamiltonian from time-resolved spin–spin correlators. Case study: **ubiquitin (1D3Z) in a membrane/oriented setting**, spin clusters of 8 and 60 of the ~600 protons. **Finds that learnability (Hessian rank) appears only as the dynamics become non-ergodic**, i.e. when dipolar couplings are suppressed. Gives NISQ and fault-tolerant cost scalings. | **Anticipates the core idea of QM-19/21**: same protein, same Hamiltonian, same "hard dynamics vs learnability" question. Its answer (ergodic → degenerate) is the hardness–identifiability trade-off in qualitative form. It does not test any classical approximation method. |
| C. Zhang, Cortiñas, Karamlou et al. (Google Quantum AI), arXiv:2510.19550 (2025) [F34] | OTOCs measured by NMR on small molecules in a liquid crystal, interpreted by simulation on the Willow processor; an H–H distance and a dihedral are recovered. Self-declared "not yet beyond classical". | Hardware demonstration of the pipeline QM-20 proposes, for small molecules. |
| Google Quantum AI, OTOC(2) "quantum echoes", Nature (2025) [F30]; Bermejo et al. arXiv:2604.15427 [F31] | Beyond-classical OTOC(2) on 2D random circuits; tensor-network/BP simulation argued infeasible. | Hardness evidence for echoes on random circuits, not dipolar protein networks. |
| Seetharam, …, Demler, Sels, *Sci. Adv.* 9 (2023), arXiv:2109.13298 | NMR spectra (ZULF) simulated on trapped ions; structure-extraction motivation. | Same application family (small molecules). |
| Fratus, Enenkel, Zanker, Reiner, Marthaler, Schmitteckert, arXiv:2508.06448 (v3 2026) | Classical cluster approximation (linear in spin number) reproduces liquid-state NMR spectra "throughout, and even somewhat beyond" typical regimes. | **Classical rebuttal for liquid-state NMR.** It does not cover strongly coupled static/oriented dipolar networks. |
| Walch et al., arXiv:2609.20406 (2026) | Shot-noise cost of quantum computation of NMR spectra. | Resource side. |
| Elsayed & Fine, *PRB* 91, 094424 (2015), arXiv:1409.8564; Navez, Starkov & Fine arXiv:1812.02155 | Classical-spin simulations reproduce NMR free-induction decays of quantum spin lattices quantitatively in many regimes; a two-spin quantum correction extends them. | **Classical adversary** for bulk dipolar dynamics. Implemented here as `classical_spin_correlators`. The two-spin-corrected version is **not** implemented (open adversary). |
| Begušić & Chan arXiv:2306.16372; Begušić, Gray & Chan *Sci. Adv.* 10 (2024) [F20, F21] | Sparse Pauli dynamics reproduced IBM's 127-qubit "utility" dynamics. | **Classical adversary**; implemented here as coefficient-threshold Pauli propagation. |

**What this program adds (if results support it).**
1. A **best-classical adversary panel** on the protein ¹H network: weight-truncated Pauli, sparse Pauli dynamics, sub-cluster exact (CCE-like), and classical-spin dynamics. The panel defines a classical-failure time t_c*. O'Brien et al. did not test classical approximations.
2. A **quantitative split of the Fisher information**, per parameter and as a full matrix, into the classically reproducible window (t < t_c*) and the hard window. The gain spectrum g = max_v v'F_total v / v'F_easy v measures how many repetitions a quantum forward model saves.
3. **Dephasing sweeps** (γ = 0, 1000, 5000 s⁻¹) and **cluster-size scaling** (N = 10, 12, 14) under a pre-registered kill rule (`research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`, C1).

**What is NOT new.**
- The application (quantum simulation of NMR to learn protein/molecular geometry) [O'Brien 2022; F34; Seetharam 2023].
- The qualitative trade-off that ergodic, classically hard dynamics are poorly learnable [O'Brien 2022].
- The adversaries themselves [Elsayed–Fine; Begušić–Chan; cluster methods, Fratus 2025].

**Verdict.** Under the scope above, the literature search found no evidence of a study that measures, for protein ¹H dipolar networks, how much structural Fisher information lies beyond the failure time of the best classical approximation. It also found none that tests the O'Brien trade-off against an explicit classical-adversary panel. The contribution is at most an **incremental, quantitative extension of O'Brien et al. (2022)**, not a new mechanism. Any claim must cite O'Brien 2022 as the origin of the idea.

_Outcome of the experiment: see §C1 of the discovery report. This memo is not updated with results._


---

## Open memos NM-2 … NM-15 (from the discovery-workflow synthesis; each needs a full sweep before any novelty claim)

All novelty statements so far are scoped to the arXiv API, Crossref/Europe PMC and the 448-paper bibliography, because web search was exhausted. Each memo below needs a full sweep before any claim.

| Memo | Question | What to check | Program |
|---|---|---|---|
| **NM-2** | Is the landscape and mixing characterisation of an LM-derived distogram posterior (G1), including DG dequantisation of "hide-and-seek" basins and the e^−KL sublevel bound, new? | trRosetta/AF1 DG pipelines; Wales-group statistical-potential landscapes; Varin–Reid–Firth / Ribatet composite-likelihood calibration. Audit and add the new NISQ preprints QSAD 2607.06971 and Patil 2608.05491. Verify the classical reference class in Leng et al. PNAS 2026. | A |
| **NM-3** | Does a published FT Toffoli costing exist for coherent walk, QHD, QRS or gradient oracles on continuous pair-distance protein energies, with an L-independent per-pair R? | Sanders 2020; Incudini–Mazzola 2607.22818; Escrig 2602.11285; Carrasco-Arango 2604.15179; Liu 2607.16996 (QHD synthesis); Miyamoto 2303.05640; Ozgul 2310.11445. | B |
| **NM-4** (extends NM-1) | Have site-resolved OTOCs of dense dipolar networks been benchmarked against spinDMFT, hybrid-core and bath-embedded adversaries? Has the shot-noise consumption cost of quantum NMR likelihoods been stated? | Zhang 2510.19550 follow-ups; nl-/cluster spinDMFT (2403.10465, 2307.14188); Starkov–Fine; Domínguez–Álvarez 2005.12361; Sánchez–Pastawski 1902.06628; Gjonbalaj 2603.04486; 2606.31827; Walch 2609.20406; Ramoa 2507.06941; Sels 1910.14221. | C |
| **NM-5** | Is the consumption-factoring screening lemma for quantum stages on learned energies folklore? Does the LWWZ lower bound survive derivative queries? | GHV authorship (STOC'21); LMRS composition; Garg et al. 2010.01801; Zhang–Li 2212.03906; Abbas 2305.13362. | F |
| **NM-6** | Are stoquastisation dominance (λ₂(H) ≤ λ₂(H₊)) and the sign-blind cut bound for parents of \|√π⟩ already stated? | Henley 2004; Castelnovo et al. 2005; Verstraete et al. 2006; BCGL 2207.07044 (add to bibliography); fixed-node literature (ten Haaf 1995). | F |
| **NM-7** | Is the Gaussian-basin Schmidt obstruction (log χ ≥ I; Mehler spectrum) new as a control for tensor-network dequantisation of continuous posteriors? | Rattacaso 2603.12334; Kodama 2608.21700 (add); Nüske TT 2016; Dolgov 1810.01212; Cui–Dolgov 2007.06968. | F |
| **NM-8** | Planted inference on protein data: is the heterogeneous-MRA K ~ √L ↔ Wein r ~ n^{3/2} correspondence known? Is there any k≥3 coevolution Kikuchi analysis? | Boumal 1710.02590; Wein 2211.05274; Schmidhuber–Hastings 2607.29672; Hastings 2602.10366 fragility note; Lavor 2112.01303 (add); Schmidt–Hamacher 3-body DCA (unverified). | G |
| **NM-9** | Are QRS/QSA on LM-derived posteriors, with measured D_½/D_KL divergences, new? | Ozols 1103.2774; Harrow–Wei 1907.09965; Layden 2510.08462; Rattacaso 2603.12334; Chatterjee–Diaconis 1511.01437. | A/F |
| **NM-10** | Kharazi 2601.15523: do its claims survive AMS/WE/MSM comparators? Verify the summariser-derived quotes against the PDF. | Also Mazzola 2108.11410; Pravatto 2107.13025; Miyamoto–Tada 2410.02276; Cérou–Guyader AMS (unverified). | F |
| **NM-11** | Quantum samplers for integrative/restraint posteriors: absence check, and bibliography gap. | Habeck–Nilges–Rieping PRL 2005; IMP/ISD/ARIA/CYANA/ARTINA; Viswanath 2017; Harrow–Wei 2020; Lin 2312.01402. | E |
| **NM-12** | Protein ZULF resource claims: does the T₂ = 1 s assumption hold, and what is the tertiary-information content? | Full text of Elenewski 2406.09340 (resource numbers unread); Seetharam 2109.13298; Fratus 2508.06448. | F |
| **NM-13** | QHD on protein/learned energies, and whether the rotation-covariant Gaussian-homotopy dequantisation of 2311.00811 is published. | Papers citing 2311.00811 (not enumerated); Chakrabarti 2503.24332; Abe–Nagai 2603.28624; Wu–Li–Zheng 2605.12066 (listing only). | F |
| **NM-14** | Quantum TDA/knots on proteins, and whether high-order Mayer features have predictive value. | Nghiem 2609.28058 (posted 2026-09-23); Laakkonen 2503.05625; Berry 2209.13581; Schmidhuber–Lloyd 2209.14286. | G |
| **NM-15** | Babbush-type oscillator simulation for protein ENMs. | Liu 2411.03972 Thm S1.10 quotes (summariser-derived; verify); Schade 2609.20721; Luangsirapornchai 2501.06100; Kolotouros 2601.05161 runtime (unchecked). | F |

**Unverified citations to resolve across memos:** Liu 1996 (independence-sampler gap); Saxe 1979; the Chen–Lovász–Pak lifting bound (partly checked); Varin–Reid–Firth 2011; Henderson 1995; Andreas et al. 2016 details; Suter–Ernst 1985; the Baur–Strassen constant; the GAW Õ(√d/ε) bound; the Lee–Mittal–Reichardt–Špalek–Szegedy composition theorem; Jarret–Jordan–Lackey 2016; Rieder–Lebowitz–Lieb J. Math. Phys. reference; Gyurik et al. 2026 guided persistence; QROAM cost constants.

**Bibliography additions flagged by the lenses:** QSAD 2607.06971, Patil 2608.05491, Miyamoto 2303.05640, Lavor 2112.01303, Brehm–Weggemans 2412.13274, BCGL 2207.07044, LWWZ 2504.14841, Hamoudi 2602.23183, Escrig 2602.11285, Carrasco-Arango 2604.15179, Kodama 2608.21700, Nghiem 2609.28058, Schade 2609.20721, Ribatet 0911.5357, Stoehr–Friel 1502.01997, Syed NRPT 1905.02939, Eberle–Lörler 2402.05041/2412.16710, Kharazi 2601.15523, plus the IMP/ISD/ARIA/CYANA/ARTINA set.
