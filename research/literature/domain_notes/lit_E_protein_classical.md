# Domain E — What is actually computationally hard in protein structure computation, and the strongest classical methods

_Literature agent E, 2026-09-26. Evidence notes for the coordinator; not the final review. No experiments were run and no repository file was edited._

**Scope note.** This domain is classical. The 16-question block (§3) is applied to the **computational subproblems** that a quantum primitive would have to replace. For each subproblem I identify what is hard, the strongest classical competitor, and how its cost scales. Quantum-side resource numbers (qubits, T-count, oracle cost) belong to other domains. Here they are marked "defer to QMCMC / QAE domain" and **no quantum number is asserted from this domain**.

**Claim labels.** Labels are applied **classical-vs-classical** unless marked otherwise. For example, "THEORETICAL SPEEDUP (classical)" means a proven speedup of one classical sampler over another. This lets the coordinator see where classical methods already remove the "hard" regime that a quantum method would need.

---

## 1. Scope and search log

**Verification method (applies to every entry in §2).**
- Bibliographic metadata was checked programmatically against **Crossref** (`https://api.crossref.org/works/<DOI>`; title, authors, year, venue, volume and pages were returned and matched). This is tagged **[CR]**.
- Abstracts or claims were checked against one or more of the following sources:

| Tag | Source |
|---|---|
| **[OA]** | OpenAlex (`https://api.openalex.org/works/doi:<DOI>`) |
| **[EP]** | Europe PMC REST API |
| **[AX]** | arXiv API (`export.arxiv.org/api/query?id_list=`) |
| **[PDF]** | Full text downloaded from arxiv.org/pdf and text-searched |
| **[PMC]** | Europe PMC full-text XML (PMC8371605 for AF2) |
| **[WS]** | WebSearch hit on the publisher or proceedings page |
| **[GH]** | GitHub README (BioEmu) |

- Where a quote is given, it was read in this session from the tagged source.

**Queries used**:
- **Crossref DOI lookups** (about 110 DOIs, batch script).
- **Crossref bibliographic queries**:
  - "Unger Moult … NP-hard"
  - "Nymeyer How efficient is replica exchange"
  - "Zuckerman Lyman second look canonical sampling replica exchange"
  - "Naganathan Munoz scaling of folding times"
  - "Denschlag Lingenheil Tavan optimal temperature ladders"
  - "Bhatnagar Randall torpid mixing simulated tempering Potts"
  - "Katzgraber Trebst Huse Troyer feedback-optimized parallel tempering"
  - "Adhikari weighted ensemble NTL9"
  - "Roberts Gelman Gilks optimal scaling"
  - "Nadler Hansmann optimal number of replicas"
  - "Charron machine-learned transferable coarse-grained"
  - "Kmiecik coarse-grained protein models"
  - "Does sequence clustering confound AlphaFold2"
- **arXiv API**:
  - By id: 2402.04845, 2306.03117, 2302.01170, 2406.14426, 2502.18462, 2202.04164, 1508.04521, 1005.1444, 0709.3289, 2601.01740, 2410.14898, 2509.04291, 2608.02866.
  - Title searches for Machta ("Strengths and weaknesses of parallel tempering" → 0908.0012), Jarzynski 2006 (cond-mat/0603185) and Clisby 2010.
- **Full-text greps**:
  - Earl & Deem arXiv physics/0508111 ("√N" replica statement)
  - Machta 0908.0012 (double-well and golf-course scaling)
  - Nadler & Hansmann 0709.3289 (N_opt ∝ √V)
  - Jarzynski cond-mat/0603185 (N_c ∼ exp(βW_d))
  - AF2 PMC8371605 (pLDDT calibration, MSA-depth threshold)
- **WebSearch**:
  - "parallel tempering number of replicas scales as square root of system size N Earl Deem"
  - "Sequence clustering confounds AlphaFold2 Nature matters arising"
  - "Lindorff-Larsen 2011 How fast-folding proteins fold 12 proteins…"
  - "Timewarp … NeurIPS 2023 proceedings"
  - "Transferable Boltzmann Generators … NeurIPS 2024"
  - "BioEmu limitations benchmark fold-switching rare states evaluation 2025"
- **GitHub**: microsoft/bioemu README (sampling-time table, monomer-only scope).

**Coverage.** All items in the task brief are covered except those listed in §9 (Unverified leads).

---

## 2. Verified papers (per-paper fields)

Field order: **Title** | Authors | Year | Venue | DOI | arXiv | Verified. Then: *Algorithm / setting*; *Key claim (verbatim where possible, location)*; *Scaling / comparator*; *Theory vs empirical*; *Limitations*; **Label**; *Relevance to the program*.

### 2.1 Energy-landscape theory, Levinthal, folding-time scaling

**E1. Are there pathways for protein folding?** | C. Levinthal | 1968 | J. Chim. Phys. 65:44–45 | 10.1051/jcp/1968650044 | — | [CR]
- *Setting.* Origin of "Levinthal's paradox": unbiased random search over conformations would take astronomically long.
- *Key claim.* Metadata only (no abstract available). The paradox is stated precisely in E2.
- **Label:** THEORETICAL (argument). *Relevance:* This is the worst-case (unstructured-search) picture. It is the only picture under which Grover-type quadratic speedups would map naturally, and E2–E5 show that real proteins are not in it.

**E2. Levinthal's paradox** | R. Zwanzig, A. Szabo, B. Bagchi | 1992 | PNAS 89:20–22 | 10.1073/pnas.89.1.20 | — | [CR][OA]
- *Key claim (abstract):* "a small and physically reasonable energy bias against locally unfavorable configurations, of the order of a few kT, can reduce Levinthal's time to a biologically significant size."
- *Scaling:* The bias converts search time from exponential in N to tractable.
- **Label:** THEORETICAL. *Relevance:* A biased (funnelled) landscape removes the unstructured-search hardness that quantum search exploits.

**E3. Spin glasses and the statistical mechanics of protein folding** | J.D. Bryngelson, P.G. Wolynes | 1987 | PNAS 84:7524–7528 | 10.1073/pnas.84.21.7524 | — | [CR][OA]
- *Key claim (abstract):* "The theory of spin glasses was used to study a simple model of protein folding. The phase diagram of the model was calculated…"
- *Setting:* Random-energy / spin-glass heteropolymer. Defines the competition between folding and glassy trapping (T_f vs T_g; the detailed ratio is not quoted here).
- **Label:** THEORETICAL. *Relevance:* Glassy (rugged) landscapes are where classical MCMC mixes torpidly. Natural sequences are argued to be *minimally frustrated* (E4), i.e. selected away from this regime.

**E4. Theory of protein folding: the energy landscape perspective** | J.N. Onuchic, Z. Luthey-Schulten, P.G. Wolynes | 1997 | Annu. Rev. Phys. Chem. 48:545–600 | 10.1146/annurev.physchem.48.1.545 | — | [CR][OA]
- *Key claim (abstract):* "the most realistic model of a protein is a minimally frustrated heteropolymer with a rugged funnel-like landscape biased toward the native structure."
- **Label:** REVIEW / THEORETICAL. *Relevance:* The funnel is the core physical reason why *natural* folding landscapes are not worst-case for classical samplers.

**E5. How does a protein fold?** | A. Šali, E. Shakhnovich, M. Karplus | 1994 | Nature 369:248–251 | 10.1038/369248a0 | — | [CR][EP]
- *Key claim (abstract):* "The necessary and sufficient condition for folding in this model is that the native state be a pronounced global minimum". Also: "the reduced number of conformations that need to be searched in the semi-compact globule (approximately 10(10) versus approximately 10(16) for the random coil) and the existence of many (approximately 10(3)) transition states."
- *Setting:* 27-mer lattice MC.
- **Label:** SIMULATOR RESULT (classical MC). *Relevance:* Search is reduced by collapse and by multiple transition states. The energy gap is the determinant.

**E6. Chain length scaling of protein folding time** | A.M. Gutin, V.I. Abkevich, E.I. Shakhnovich | 1996 | PRL 77:5433–5436 | 10.1103/PhysRevLett.77.5433 | — | [CR][OA]
- *Key claim (abstract):* "the folding time of chains of length N scales as N^λ at the temperature of fastest folding. For chains with random sequences of monomers λ≈6, and for chains with sequences designed to provide a pronounced minimum of energy to their ground state conformation λ≈4."
- *Scaling:* **Polynomial** in N (lattice MC, local moves) at optimal T. The source adds: "Folding at low temperatures exhibits a simple Arrhenius-like behavior."
- **Label:** SIMULATOR RESULT. *Relevance:* This is the key explicit statement. **Classical local-move MC folding time on lattice heteropolymers is polynomial (N^4–N^6) at the optimal temperature**, not exponential. Below that temperature, Arrhenius (barrier-exponential) behaviour appears.

**E7. Scaling of folding times with protein size** | A.N. Naganathan, V. Muñoz | 2005 (online 2004) | JACS 127:480–481 | 10.1021/ja044449u | — | [CR][OA]
- *Key claim (abstract):* "Using a database of 69 proteins… the folding time scales with the number of residues… it is possible to predict the folding time of a protein with a precision of approximately 1.1 times decades from just its size." Also: "the smallest proteins are expected to have very marginal free energy barriers."
- *Scaling:* The fitted functional form (often reported as ln τ ∝ N^{1/2}) was **not verified** in this session; see §9.
- **Label:** EMPIRICAL (experimental data). *Relevance:* Physical folding times grow with N, spanning 9 orders of magnitude across proteins. This sets the MD cost.

**E8. Contact order, transition state placement and the refolding rates of single domain proteins** | K.W. Plaxco, K.T. Simons, D. Baker | 1998 | J. Mol. Biol. 277:985–994 | 10.1006/jmbi.1998.1645 | — | [CR][EP]
- *Key claim (abstract):* "statistically significant correlations between the average sequence separation between contacting residues in the native state and the rate… No significant relationship is apparent between protein length and folding rates".
- **Label:** EMPIRICAL. *Relevance:* Folding barriers track topology (non-local contacts), not simply N. For two-state proteins, "hardness" is not a clean function of length.

**E9. The protein folding 'speed limit'** | J. Kubelka, J. Hofrichter, W.A. Eaton | 2004 | Curr. Opin. Struct. Biol. 14:76–88 | 10.1016/j.sbi.2004.01.013 | — | [CR][EP]
- *Key claim (abstract):* "Both experimental and theoretical approaches predict a speed limit of approximately N/100 μs for a generic N-residue single-domain protein".
- **Label:** EMPIRICAL / THEORETICAL. *Relevance:* This is a lower bound on the physical folding time. MD must cover ≥ N/100 μs of simulated time, i.e. ~10^9·N/100 fs-steps.

**E10. Brownian motion in a field of force and the diffusion model of chemical reactions** | H.A. Kramers | 1940 | Physica 7:284–304 | 10.1016/S0031-8914(40)90098-2 | — | [CR]
- *Setting:* Barrier-crossing rate theory (rate ∝ exp(−ΔG‡/kT) with friction prefactor). Metadata verified; standard result, not quoted.
- **Label:** THEORETICAL. *Relevance:* This is the origin of the "exponential in barrier height" cost of unbiased dynamics.

### 2.2 Computational complexity of structure search

**E11. Finding the lowest free energy conformation of a protein is an NP-hard problem: proof and implications** | R. Unger, J. Moult | 1993 | Bull. Math. Biol. 55:1183–1198 | 10.1007/BF02460703 | — | [CR][EP]
- *Key claim (abstract):* "we present a proof that finding the lowest free energy conformation belongs to the class of NP-hard problems… we suggest that the natural folding process cannot be considered as a search for the global free energy minimum."
- **Label:** THEORETICAL (worst case). *Relevance:* This is worst-case hardness only. It says nothing about natural instances (see E2–E6).

**E12. Protein folding in the hydrophobic-hydrophilic (HP) model is NP-complete** | B. Berger, T. Leighton | 1998 | J. Comput. Biol. 5:27–40 | 10.1089/cmb.1998.5.27 | — | [CR][OA]
- *Key claim (abstract):* "the protein folding problem under the HP model on the cubic lattice is shown to be NP-complete."
- **Label:** THEORETICAL. *Relevance:* A quantum method gives at most a polynomial (Grover-like) speedup on an NP-complete problem, absent structure. Practical HP instances are solved by E47–E50.

**E13. On the complexity of protein folding** | P. Crescenzi, D. Goldman, C. Papadimitriou et al. | 1998 | J. Comput. Biol. 5:423–465 | 10.1089/cmb.1998.5.423 | — | [CR][OA]
- *Key claim (abstract):* "the protein folding problem in the two-dimensional H-P model is NP-complete."
- **Label:** THEORETICAL.

**E14. On the computational complexity of Ising spin glass models** | F. Barahona | 1982 | J. Phys. A 15:3241–3253 | 10.1088/0305-4470/15/10/028 | — | [CR]
- *Setting:* NP-hardness of spin-glass ground states (metadata verified).
- **Label:** THEORETICAL. *Relevance:* Hardness of glassy energy minimisation. It applies to learned pairwise energies only if those are genuinely frustrated.

### 2.3 Brute-force MD on special hardware

**E15. Atomic-level characterization of the structural dynamics of proteins** | D.E. Shaw, P. Maragakis, K. Lindorff-Larsen et al. | 2010 | Science 330:341–346 | 10.1126/science.1187409 | — | [CR][OA]
- *Key claim (abstract):* "Equilibrium simulations of a WW protein domain captured multiple folding and unfolding events…". Also: "A 1-millisecond simulation of the folded protein BPTI reveals a small number of structurally distinct conformational states whose reversible interconversion is slower than local relaxations within those states by a factor of more than 1000."
- **Label:** EMPIRICAL (classical special-purpose hardware). *Relevance:* This shows the timescale separation (>10^3) that makes equilibrium sampling hard even *within* the folded state.

**E16. How fast-folding proteins fold** | K. Lindorff-Larsen, S. Piana, R.O. Dror et al. | 2011 | Science 334:517–520 | 10.1126/science.1208351 | — | [CR][OA][WS]
- *Key claim (abstract):* "atomic-level molecular dynamics simulations, over periods ranging between 100 μs and 1 ms, that reveal a set of common principles underlying the folding of 12 structurally diverse proteins… spontaneously and repeatedly fold to their experimentally determined native structures." Also: "In most cases, folding follows a single dominant route".
- *Limitations:* Only small fast-folders (size range not re-checked verbatim; §9). Force-field dependent.
- **Label:** EMPIRICAL (classical). *Relevance:* For fast-folding domains, unbiased all-atom classical MD already samples folding/unfolding equilibria. A "single dominant route" means low path multiplicity; the landscape is not glassy.

**E17. Protein folding kinetics and thermodynamics from atomistic simulation** | S. Piana, K. Lindorff-Larsen, D.E. Shaw | 2012 | PNAS 109:17845–17850 | 10.1073/pnas.1201811109 | — | [CR][OA]
- *Key claim (abstract):* "simulations of spontaneous folding and unfolding can provide direct access to thermodynamic and kinetic quantities such as folding rates, free energies, folding enthalpies, heat capacities, Φ-values".
- **Label:** EMPIRICAL. *Relevance:* The residual error is force-field accuracy, not sampling, for villin-size systems.

**E18. Anton 3** (Crossref title; a longer subtitle is commonly cited but not verified) | D.E. Shaw, P.J. Adams, A. Azaria et al. | 2021 | SC'21 Proceedings, 1–11 | 10.1145/3458817.3487397 | — | [CR][OA]
- *Key claim (abstract):* "a 512-node Anton 3 simulates a million atoms at over 100 microseconds per day." Also: "over 100-fold faster than any other currently available supercomputer".
- **Label:** HARDWARE DEMONSTRATION (classical special-purpose). *Relevance:* Defines the classical brute-force frontier: ~10^2 μs/day at 10^6 atoms, so ms-scale events take ~10 days.

### 2.4 Enhanced sampling: tempering, biasing

**E19. Replica Monte Carlo simulation of spin-glasses** | R.H. Swendsen, J.-S. Wang | 1986 | PRL 57:2607–2609 | 10.1103/PhysRevLett.57.2607 | — | [CR][OA]
- *Key claim (abstract):* "greatly reduces the long correlation times characteristic of standard methods, allowing the investigation of lower temperatures".
- **Label:** EMPIRICAL ADVANTAGE (classical, over single-temperature MC).

**E20. Exchange Monte Carlo method and application to spin glass simulations** | K. Hukushima, K. Nemoto | 1996 | JPSJ 65:1604–1608 | 10.1143/JPSJ.65.1604 | — | [CR][OA]
- *Key claim (abstract):* "The ergodicity time in this method is found much smaller than that of the multi-canonical method… the system relaxes very rapidly through the exchange process even in the low temperature phase."
- **Label:** EMPIRICAL ADVANTAGE (classical). *Relevance:* This is the standard parallel tempering (PT) algorithm. It is the classical twin the program must beat.

**E21. Parallel tempering algorithm for conformational studies of biological molecules** | U.H.E. Hansmann | 1997 | Chem. Phys. Lett. 281:140–150 | 10.1016/S0009-2614(97)01198-6 | — | [CR]
- *Setting:* First PT application to peptides (metadata verified). **Label:** EMPIRICAL.

**E22. Replica-exchange molecular dynamics method for protein folding** | Y. Sugita, Y. Okamoto | 1999 | Chem. Phys. Lett. 314:141–151 | 10.1016/S0009-2614(99)01123-9 | — | [CR]
- *Setting:* REMD with momentum rescaling p′ = √(T_new/T_old)·p (quoted from E23's description). **Label:** EMPIRICAL.

**E23. Parallel tempering: theory, applications, and new perspectives** | D.J. Earl, M.W. Deem | 2005 | PCCP 7:3910 | 10.1039/b509983h | arXiv physics/0508111 | [CR][OA][PDF] — **REVIEW (orientation)**
- *Key claim (full text):* "Since the width of the energy histograms increases as √N, but the average energy increases as N, the number of replicas increases as √N, where N is the system size." Also: "how to swap only part of the system, so as to overcome the growth as √N of the number replicas required". And: "the round-trip time is likely to better characterize the overall efficiency of parallel tempering than is the average acceptance probability."
- **Label:** THEORETICAL (scaling argument). *Relevance:* This is the canonical source for **N_rep ∝ √N**.

**E24. On the acceptance probability of replica-exchange Monte Carlo trials** | D.A. Kofke | 2002 | J. Chem. Phys. 117:6911–6914 | 10.1063/1.1507776 | — | [CR][OA]
- *Key claim (abstract):* "an exact expression for the trial-move acceptance probability in terms of the overlap of these distributions is derived… an asymptotic form for this result, good for large system sizes, is reported… treatment of the energy distributions as Gaussians is an inappropriate way to analyze the acceptance probability."
- **Label:** THEORETICAL.

**E25. Selection of temperature intervals for parallel-tempering simulations** | A. Kone, D.A. Kofke | 2005 | J. Chem. Phys. 122 | 10.1063/1.1917749 | — | [CR][OA]
- *Key claim (abstract):* "temperatures in replica-exchange simulations should be spaced such that about 20% of the phase-swap attempts are accepted… independent of the heat capacity".
- **Label:** THEORETICAL (heuristic).

**E26. Optimal allocation of replicas in parallel tempering simulations** | N. Rathore, M. Chopra, J.J. de Pablo | 2005 | J. Chem. Phys. 122 | 10.1063/1.1831273 | — | [CR][OA]
- *Key claim (abstract):* "A scheme is proposed for the optimal allocation of temperatures… Accuracy… and their dependence on the trial-exchange acceptance rate is reported."
- *Systems:* Coarse-grained protein, atomistic polypeptide, LJ fluid. **Label:** EMPIRICAL.

**E27. Generalized ensemble and tempering simulations: a unified view** | W. Nadler, U.H.E. Hansmann | 2007 | PRE 75:026109 | 10.1103/PhysRevE.75.026109 | — | [CR][OA]
- *Key claim (abstract):* "optimizing the flow is equivalent to minimizing the first passage time for crossing the space… we point out the limitations of these representations under conditions of broken ergodicity."
- **Label:** THEORETICAL.

**E28. Dynamics and optimal number of replicas in parallel tempering simulations** | W. Nadler, U.H.E. Hansmann | 2007 | PRE 76:065701(R) | 10.1103/PhysRevE.76.065701 | arXiv 0709.3289 | [CR][OA][AX][PDF]
- *Key claim (full text):* "suggests that N_opt scales with system size V as N_opt ∝ √V."
- **Label:** THEORETICAL. *Relevance:* Second, independent source for **√(system size)** replicas.

**E29. Efficiency reduction and pseudo-convergence in replica exchange sampling of peptide folding–unfolding equilibria** | R. Denschlag, M. Lingenheil, P. Tavan | 2008 | Chem. Phys. Lett. 458:244–248 | 10.1016/j.cplett.2008.04.114 | — | [CR]
- *Setting:* Metadata only (no abstract retrieved). The title claims pseudo-convergence of REMD for peptide folding. **Used only as a pointer; content unverified.**

**E30. Optimal temperature ladders in replica exchange simulations** | R. Denschlag, M. Lingenheil, P. Tavan | 2009 | Chem. Phys. Lett. 473:193–195 | 10.1016/j.cplett.2009.03.053 | — | [CR]
- Metadata only; content not verified (§9).

**E31. Feedback-optimized parallel tempering Monte Carlo** | H.G. Katzgraber, S. Trebst, D.A. Huse, M. Troyer | 2006 | J. Stat. Mech. P03018 | 10.1088/1742-5468/2006/03/P03018 | — | [CR][OA]
- *Key claim (abstract):* "minimize the round-trip times between the lowest and highest temperatures… the density of temperatures in the optimized temperature set increases at the 'bottlenecks' of the simulation, such as phase transitions."
- **Label:** EMPIRICAL / THEORETICAL (classical).

**E32. Optimized parallel tempering simulations of proteins** | S. Trebst, M. Troyer, U.H.E. Hansmann | 2006 | J. Chem. Phys. 124 | 10.1063/1.2186639 | — | [CR][OA]
- *Key claim (abstract):* "an optimal set of temperatures/replicas which are found to concentrate at the bottlenecks… villin headpiece subdomain HP-36 where we find a lowest-energy configuration with a root-mean-square deviation of less than 4 Å".
- **Label:** EMPIRICAL (classical).

**E33. Strengths and weaknesses of parallel tempering** | J. Machta | 2009 | PRE 80:056706 | 10.1103/PhysRevE.80.056706 | arXiv 0908.0012 | [CR][OA][AX][PDF]
- *Key claims.*
  - Abstract: "For the double-well system, parallel tempering with a number of replicas that scales as the square root of the barrier height yields exponential speedup of the equilibration time. On the other hand, replica exchange yields only marginal speedup for the golf course system."
  - Full text: "replica exchange can reduce the barrier crossing time from exponential to a polynomial in the barrier height". Diffusive-regime optimum "R_opt ∼ (β0−βc)√K", "τ_D ∼ (R_opt−1)² ∼ K(β0−βc)²". Ballistic regime "τ_B ∼ R_opt ∼ (β0−βc)√K".
  - Golf course, full text: "for the golf course landscape, replica exchange achieves a modest speed-up in the equilibration time due to brute force parallelism"; "Nearly degenerate wells equilibrate much more slowly than strongly asymmetric wells."
  - Discussion: "parallel tempering with polynomially many replicas reaches equilibrium in a time that is polynomial in the barrier height and thus achieves exponential speed-up. On the other hand, replica exchange yields little improvement for systems where the relevant macrostates states have small basins of attraction."
- **Label:** THEORETICAL SPEEDUP (classical PT vs local MC, double well); NO ADVANTAGE (classical PT on golf course).
- *Relevance:* **The single most important scaling paper for this program.**
  - PT removes the *energetic*-barrier exponential. It does **not** remove the *entropic* (small-basin, golf-course) exponential.
  - The golf course is the Levinthal landscape and is exactly where an unstructured quantum search (quadratic) would apply.
  - Funnelled natural proteins (E2–E5) are not golf courses.

**E34. How efficient is replica exchange molecular dynamics? An analytic approach** | H. Nymeyer | 2008 | JCTC 4:626–636 | 10.1021/ct7003337 | — | [CR][OA]
- *Key claim (abstract):*
  - "as long as there is a positive activation energy for folding, REMD is more efficient than MD"
  - "Choosing the maximum temperature too high can result in REMD becoming significantly less efficient than conventional MD"
  - "the number of replicas in REMD… has a minimal effect on the asymptotic efficiency".
- **Label:** THEORETICAL (classical; REMD vs MD). *Relevance:* REMD's gain is bounded by the Arrhenius behaviour of folding. Proteins with anti-Arrhenius folding gain little.

**E35. A second look at canonical sampling of biomolecules using replica exchange simulation** | D.M. Zuckerman, E. Lyman | 2006 | JCTC 2:1200–1202 | 10.1021/ct0600464 | — | [CR][OA]
- *Key claim (abstract):* "we are not optimistic for the efficiency of replica exchange for canonical sampling of biomolecules."
- **Label:** ADVANTAGE DISPUTED (classical REMD vs MD).

**E36. Error and efficiency of replica exchange molecular dynamics simulations** | E. Rosta, G. Hummer | 2009 | J. Chem. Phys. 131 | 10.1063/1.3249608 | — | [CR][OA]
- *Key claim (abstract):* "the relative efficiency of REMD and molecular dynamics (MD) simulations is given by the ratio of the number of transitions between the two states averaged over all replicas at the different temperatures, and the number of transitions at the single temperature of the MD run."
- **Label:** THEORETICAL (classical).

**E37. Ensuring mixing efficiency of replica-exchange molecular dynamics simulations** | M.J. Abraham, J.E. Gready | 2008 | JCTC 4:1119–1128 | 10.1021/ct800016r | — | [CR]
- Metadata only. **Label:** pointer.

**E38. Conditions for rapid mixing of parallel and simulated tempering on multimodal distributions** | D.B. Woodard, S.C. Schmidler, M. Huber | 2009 | Ann. Appl. Probab. 19 | 10.1214/08-AAP555 | — | [CR][OA]
- *Key claim (abstract):* "We provide lower bounds on the spectral gaps of parallel and simulated tempering… rapid mixing… for several normal mixture models, and for the mean-field Ising model."
- **Label:** THEORETICAL (rigorous, classical).

**E39. Sufficient conditions for torpid mixing of parallel and simulated tempering** | D.B. Woodard, S.C. Schmidler, M. Huber | 2009 | Electron. J. Probab. 14 | 10.1214/EJP.v14-638 | — | [CR][OA]
- *Key claim (abstract):*
  - "We identify a persistence property of the target distribution, and show that it can lead unexpectedly to slow mixing that commonly used convergence diagnostics will fail to detect."
  - "anytime a multimodal distribution includes both very narrow and very wide peaks of comparable probability mass, parallel and simulated tempering are shown to mix slowly."
- **Label:** THEORETICAL (rigorous: PT torpid on a class). *Relevance:* **This is a candidate hard class for classical PT.** A narrow native basin with comparable mass to a broad misfolded/unfolded ensemble is structurally similar. This is the precise place where a measured classical gap could exist.

**E40. Simulated tempering and swapping on mean-field models** | N. Bhatnagar, D. Randall | 2016 | J. Stat. Phys. 164:495–530 | 10.1007/s10955-016-1526-8 | arXiv 1508.04521 | [CR][AX]
- *Key claim (abstract):*
  - "for the mean-field 3-state ferromagnetic Potts model, tempering converges slowly regardless of the temperature schedule chosen."
  - "the mixing time of simulated tempering is an exponential factor longer than the mixing time at the fixed temperature."
  - "tempering with entropy dampening distributions converges in polynomial time".
- **Label:** THEORETICAL (rigorous). *Relevance:* First-order (discontinuous) transitions defeat temperature tempering. Cooperative two-state folding is first-order-like in finite proteins, so tempering *across T_m* can be exponentially slow in principle (I(prog); no protein-specific proof found, §8). Classical remedies (entropy dampening, Hamiltonian tempering) exist.

**E41. Escaping free-energy minima (metadynamics)** | A. Laio, M. Parrinello | 2002 | PNAS 99:12562–12566 | 10.1073/pnas.202427399 | — | [CR][OA]
- *Key claim (abstract):* "a history-dependent potential term that, in time, fills the minima in the FES… in the space defined by a few collective coordinates."
- **Label:** EMPIRICAL (classical). *Limitation:* Needs good low-dimensional collective variables (CVs); cost grows with CV dimension.

**E42. Well-tempered metadynamics** | A. Barducci, G. Bussi, M. Parrinello | 2008 | PRL 100:020603 | 10.1103/PhysRevLett.100.020603 | — | [CR]. **Label:** EMPIRICAL (convergent variant).

**E43. Metadynamics: a method to simulate rare events and reconstruct the free energy…** | A. Laio, F.L. Gervasio | 2008 | Rep. Prog. Phys. 71:126601 | 10.1088/0034-4885/71/12/126601 | — | [CR][OA] — **REVIEW**. The practical issues it lists include "(i) the choice of the appropriate set of collective variables".

**E44. Enhancing important fluctuations: rare events and metadynamics from a conceptual viewpoint** | O. Valsson, P. Tiwary, M. Parrinello | 2016 | Annu. Rev. Phys. Chem. 67:159–184 | 10.1146/annurev-physchem-040215-112229 | — | [CR][OA] — **REVIEW**.

**E45. Rethinking metadynamics: from bias potentials to probability distributions (OPES)** | M. Invernizzi, M. Parrinello | 2020 | J. Phys. Chem. Lett. 11:2731–2736 | 10.1021/acs.jpclett.0c00497 | — | [CR][OA]
- *Key claim (abstract):* "a drastic improvement in convergence speed, especially when dealing with suboptimal and/or multidimensional sets of collective variables." **Label:** EMPIRICAL (classical).

**E46. Nonphysical sampling distributions in Monte Carlo free-energy estimation: umbrella sampling** | G.M. Torrie, J.P. Valleau | 1977 | J. Comput. Phys. 23:187–199 | 10.1016/0021-9991(77)90121-8 | — | [CR]. **Label:** foundational (classical).

**E47. Replica exchange with solute scaling (REST2)** | L. Wang, R.A. Friesner, B.J. Berne | 2011 | J. Phys. Chem. B 115:9431–9438 | 10.1021/jp204407d | — | [CR][OA]
- *Key claim (abstract):* "bypasses the poor scaling with system size of the standard Temperature Replica Exchange Method (TREM)… the acceptance probability for the exchange of replica configurations does not depend on the number of explicit water molecules in the system."
- **Label:** EMPIRICAL ADVANTAGE (classical over TREM). *Relevance:* This removes the √N_solvent replica cost. The remaining cost is √(solute DOF).

**E48. Accelerated molecular dynamics** | D. Hamelberg, J. Mongan, J.A. McCammon | 2004 | J. Chem. Phys. 120:11919–11929 | 10.1063/1.1755656 | — | [CR][OA]
- *Key claim (abstract):* "a bias potential… to simulate the transition of high energy barriers without any advance knowledge of the location of either the potential energy wells or saddle points… converges to the correct canonical distribution."
- **Label:** EMPIRICAL (classical). *Limitation:* Reweighting variance grows with the boost (exponential-average problem, cf. E60).

**E49. Resolution exchange simulation with incremental coarsening** | E. Lyman, D.M. Zuckerman | 2006 | JCTC 2:656–666 | 10.1021/ct050337x | — | [CR]
- Metadata only. Coarse/fine replica exchange is a classical multiscale sampler. **Label:** pointer.

### 2.5 Generic MCMC dimension scaling

**E50. Weak convergence and optimal scaling of random walk Metropolis algorithms** | G.O. Roberts, A. Gelman, W.R. Gilks | 1997 | Ann. Appl. Probab. 7 | 10.1214/aoap/1034625254 | — | [CR][OA]
- *Key claim (abstract):* "When the proposal variance is appropriately scaled according to n… The asymptotically optimal acceptance rate is 0.234". Proved for "symmetric product form" targets.
- *Scaling:* Proposal variance ∝ 1/n implies O(n) steps per effective sample (product targets).
- **Label:** THEORETICAL (rigorous, idealised target).

**E51. Optimal tuning of the hybrid Monte Carlo algorithm** | A. Beskos, N. Pillai, G. Roberts et al. | 2013 | Bernoulli 19 | 10.3150/12-BEJ414 | — | [CR][OA]
- *Key claim (abstract):* "the leapfrog step size h should be scaled as h = l × d^{−1/4}. Therefore, in high dimensions, HMC requires O(d^{1/4}) steps to traverse the state space… optimal acceptance probability… 0.651".
- **Label:** THEORETICAL (i.i.d. product targets). *Relevance:* This is the within-basin dimension cost of the best local sampler: d^{1/4}. It is benign. The hardness lies in inter-basin barriers, not dimension.

### 2.6 Chain-growth and lattice-polymer samplers

**E52. Monte Carlo calculation of the average extension of molecular chains** | M.N. Rosenbluth, A.W. Rosenbluth | 1955 | J. Chem. Phys. 23:356–359 | 10.1063/1.1741967 | — | [CR]. Foundational sequential importance sampling for chains.

**E53. Pruned-enriched Rosenbluth method (PERM): simulations of θ polymers of chain length up to 1 000 000** | P. Grassberger | 1997 | PRE 56:3682–3693 | 10.1103/PhysRevE.56.3682 | — | [CR][OA]
- *Key claim (abstract):* "combines the Rosenbluth-Rosenbluth method with recursive enrichment… allows high statistics simulations of chains of length up to N=10^6… can be applied also to off-lattice models".
- **Label:** EMPIRICAL (classical). *Relevance:* This is the SMC-for-chains baseline. It is extremely strong at the θ-point, and weaker at low T (see E54).

**E54. Growth algorithms for lattice heteropolymers at low temperatures** | H.-P. Hsu, V. Mehra, W. Nadler, P. Grassberger | 2003 | J. Chem. Phys. 118:444–451 | 10.1063/1.1522710 | — | [CR][OA]
- *Key claim (abstract):* "outperform… all other stochastic algorithms which have been employed on this problem, except for the core directed chain growth method… a fully blind general purpose algorithm giving correct Boltzmann–Gibbs weights".
- **Label:** EMPIRICAL (classical).

**E55. Fragment regrowth via energy-guided sequential sampling (FRESS)** | J. Zhang, S.C. Kou, J.S. Liu | 2007 | J. Chem. Phys. 126 | 10.1063/1.2736681 | — | [CR][OA]
- *Key claim (abstract):* "found new lower energies for all the three-dimensional HP models with sequence length longer than 80 residues."
- **Label:** EMPIRICAL (classical).

**E56. Optimized Wang-Landau sampling of lattice polymers: HP model proteins** | T. Wüst, D.P. Landau | 2012 | J. Chem. Phys. 137 | 10.1063/1.4742969 | — | [CR][OA]
- *Key claim (abstract):* "all currently known putative ground states for the most difficult benchmark HP sequences could be found… entire energy density of states… for sequence lengths up to 500 residues."
- **Label:** EMPIRICAL (classical). *Relevance:* Classical methods reach ground states and full density of states at up to 500-mer lattice proteins despite NP-completeness (E12). **Lattice HP is not a viable quantum-advantage target.**

**E57. The pivot algorithm: a highly efficient Monte Carlo method for the self-avoiding walk** | N. Madras, A.D. Sokal | 1988 | J. Stat. Phys. 50:109–186 | 10.1007/BF01022990 | — | [CR]. Metadata verified. The acceptance-fraction exponents are not re-verified (§9).

**E58. Efficient implementation of the pivot algorithm for self-avoiding walks** | N. Clisby | 2010 | J. Stat. Phys. 140:349–392 | 10.1007/s10955-010-9994-8 | arXiv 1005.1444 | [CR][AX]
- *Key claim (abstract):* "the mean time per attempted pivot for N-step self-avoiding walks is O(1) for the square and simple cubic lattices… consistent with o(log N)… and O(log N)… Our method can be adapted to other models of polymers with short-range interactions, on the lattice or in the continuum".
- **Label:** EMPIRICAL / heuristic argument (classical). *Relevance:* For athermal or good-solvent chains, classical sampling is essentially free per move.

### 2.7 Rare events, kinetics and Markov state models

**E59. Transition path sampling and the calculation of rate constants** | C. Dellago, P.G. Bolhuis, F.S. Csajka et al. | 1998 | J. Chem. Phys. 108:1964–1977 | 10.1063/1.475562 | — | [CR][OA]
- *Key claim (abstract):* "the method relies neither on prior knowledge nor on explicit specification of transition states."

**E60. Transition path sampling: throwing ropes over rough mountain passes, in the dark** | P.G. Bolhuis, D. Chandler, C. Dellago, P.L. Geissler | 2002 | Annu. Rev. Phys. Chem. 53:291–318 | 10.1146/annurev.physchem.53.082301.113146 | — | [CR][OA] — **REVIEW**
- *Key claim (abstract):* "allow computational studies of rare events without requiring prior knowledge of mechanisms, reaction coordinates, and transition states."
- *Relevance:* TPS cost scales with transition-path *duration*, not the waiting time, which removes the exp(ΔG‡/kT) factor for the path ensemble. Rates still need a flux calculation.

**E61. Weighted-ensemble Brownian dynamics simulations for protein association reactions** | G.A. Huber, S. Kim | 1996 | Biophys. J. 70:97–110 | 10.1016/S0006-3495(96)79552-8 | — | [CR][OA]
- *Key claim (abstract):* "yields reaction rate constants in agreement with those obtained by direct Brownian simulation, but at a fraction of the CPU time (10^−4 to 10^−3, depending on the model)."
- **Label:** EMPIRICAL ADVANTAGE (classical over brute force).

**E62. Weighted ensemble simulation: review of methodology, applications, and software** | D.M. Zuckerman, L.T. Chong | 2017 | Annu. Rev. Biophys. 46:43–57 | 10.1146/annurev-biophys-070816-033834 | — | [CR][OA] — **REVIEW**
- *Key claim (abstract):* "The WE strategy can achieve superlinear scaling-the unbiased estimation of key observables such as rate constants and equilibrium state populations to greater precision than would be possible with ordinary parallel simulation."

**E63. Computational estimation of microsecond to second atomistic folding times** | U. Adhikari, B. Mostofian, J. Copperman et al. | 2019 | JACS 141:6519–6526 | 10.1021/jacs.8b10735 | — | [CR][OA]
- *Key claim (abstract):* "folding times τ ranging from ∼10 μs to ∼100 ms using the weighted ensemble (WE) strategy… no biasing forces are used… for Protein G, this characterization required significantly less overall computing than would be required to observe a single folding event with conventional MD". Also: "the variance among atomistic WE folding runs is significant".
- **Label:** EMPIRICAL ADVANTAGE (classical). *Relevance:* Classical unbiased rare-event methods reach 100 ms kinetics for small proteins (implicit solvent). The remaining bottleneck is **variance** of the estimate, a potential amplitude-estimation-type target (see §3 P3). The variance is dominated by rare trajectories, not by i.i.d. Monte Carlo error, though.

**E64. Computing time scales from reaction coordinates by milestoning** | A.K. Faradjian, R. Elber | 2004 | J. Chem. Phys. 120:10880–10889 | 10.1063/1.1738640 | — | [CR][OA]. Classical rare-event kinetics via milestone hopping.

**E65. Markov models of molecular kinetics: generation and validation** | J.-H. Prinz, H. Wu, M. Sarich et al. | 2011 | J. Chem. Phys. 134 | 10.1063/1.3565032 | — | [CR][OA]
- *Key claim (abstract):* "the potential to mitigate the sampling problem by extracting long-time kinetic information from short trajectories… an upper bound for the approximation error… this error can be made arbitrarily small with surprisingly little effort."
- **Label:** THEORETICAL + EMPIRICAL (classical).

**E66. Markov state models: from an art to a science** | B.E. Husic, V.S. Pande | 2018 | JACS 140:2386–2396 | 10.1021/jacs.7b12191 | — | [CR][OA] — **REVIEW (orientation)**. Covers the variational principle (2013) and applications to folding, binding and association.

**E67. Complete protein–protein association kinetics in atomic detail (barnase–barstar)** | N. Plattner, S. Doerr, G. De Fabritiis, F. Noé | 2017 | Nat. Chem. 9:1005–1011 | 10.1038/nchem.2785 | — | [CR][EP]
- *Key claim (abstract):* "combining adaptive high-throughput MD simulations and hidden Markov modelling… energetics and kinetics on timescales from microseconds to hours."
- **Label:** EMPIRICAL (classical). *Relevance:* Kinetics on hour timescales are reachable classically, via short-trajectory MSMs.

### 2.8 Free energies

**E68. High-temperature equation of state by a perturbation method (FEP)** | R.W. Zwanzig | 1954 | J. Chem. Phys. 22:1420–1426 | 10.1063/1.1740409 | — | [CR]. Foundational exponential-average estimator.

**E69. Statistically optimal analysis of samples from multiple equilibrium states (MBAR)** | M.R. Shirts, J.D. Chodera | 2008 | J. Chem. Phys. 129 | 10.1063/1.2978177 | — | [CR][OA]
- *Key claim (abstract):* "In the large sample limit, MBAR is unbiased and has the lowest variance of any known estimator for making use of equilibrium data collected from multiple states."
- **Label:** THEORETICAL (classical optimal estimator). *Relevance:* The classical estimator is statistically optimal given samples. Any quantum gain must come from sample *generation* (mixing) or from a Heisenberg-limit (1/ε) estimator, not from post-processing.

**E70. Accuracy of free-energy perturbation calculations in molecular simulation. I. Modeling** | N. Lu, D.A. Kofke | 2001 | J. Chem. Phys. 114:7303–7311 | 10.1063/1.1359181 | — | [CR][OA]
- *Key claim (abstract):* "conduct the FEP calculation in one direction, namely that in which the entropy of the target is less than the entropy of the reference… prescriptions for the selection of an appropriate multistage FEP scheme based on how the important phase-space regions… overlap". **Label:** THEORETICAL.

**E71. Nonequilibrium equality for free energy differences** | C. Jarzynski | 1997 | PRL 78:2690–2693 | 10.1103/PhysRevLett.78.2690 | — | [CR]. Foundational.

**E72. Rare events and the convergence of exponentially averaged work values** | C. Jarzynski | 2006 | PRE 73:046105 | 10.1103/PhysRevE.73.046105 | arXiv cond-mat/0603185 | [CR][OA][AX][PDF]
- *Key claim (full text, Eq. 34a–b):* "N_c^F = P^{−1} ∼ exp(βW_d^R)… the number of realizations required for convergence grows exponentially in the average dissipated work… and therefore exponentially with system size (assuming dissipated work is an extensive property)". Also (abstract): "Analogous results apply to the equilibrium perturbation method".
- **Label:** THEORETICAL. *Relevance:* This is the **explicit exponential-in-system-size cost** of single-step exponential-average estimators. Classical practice avoids it with multistage (λ-window) schemes, whose cost becomes polynomial (number of windows ∝ overlap, ~√N by the same argument as PT). This is I(prog) by analogy with E23/E28; not separately verified.

**E73. Accurate and reliable prediction of relative ligand binding potency… (FEP+)** | L. Wang, Y. Wu, Y. Deng et al. | 2015 | JACS 137:2695–2703 | 10.1021/ja512751q | — | [CR][OA]
- *Key claim (abstract):* "an unprecedented level of accuracy across a broad range of target classes and ligands, with retrospective results encompassing 200 ligands". Also that achieving ~5× potency accuracy "has proven to be challenging".
- **Label:** EMPIRICAL (classical, industrial). *Relevance:* Alchemical FEP is production-grade classically. Its error floor is dominated by force field and sampling of slow protein modes.

**E74. Sequential Monte Carlo samplers** | P. Del Moral, A. Doucet, A. Jasra | 2006 | JRSS-B 68:411–436 | 10.1111/j.1467-9868.2006.00553.x | — | [CR]. Foundational SMC (metadata verified).

**E75. Annealed importance sampling** | R.M. Neal | 2001 | Stat. Comput. 11:125–139 | 10.1023/A:1008923215028 | — | [CR]. Foundational AIS (metadata verified).

### 2.9 Learned generative ensemble models and ML coarse-graining

**E76. Boltzmann generators** | F. Noé, S. Olsson, J. Köhler et al. | 2019 | Science 365 | 10.1126/science.aaw1147 | — | [CR][OA]
- *Key claim (abstract):* "generate unbiased one-shot equilibrium samples of representative condensed-matter systems and proteins… can avoid rare events during sampling without prior knowledge of reaction coordinates."
- *Limitations:* Per-system training. Importance weights lose effective sample size (ESS) as dimension grows (see E78/E79 scope).
- **Label:** EMPIRICAL (classical ML).

**E77. Timewarp: transferable acceleration of MD by learning time-coarsened dynamics** | L. Klein, A.Y.K. Foong, T.E. Fjelde et al. | 2023 | NeurIPS 2023 | — | arXiv 2302.01170 | [AX][WS: proceedings.neurips.cc/paper_files/paper/2023/hash/a598c367…]
- *Key claim (abstract):* "uses a normalising flow as a proposal distribution in a Markov chain Monte Carlo method targeting the Boltzmann distribution… generalises to unseen small peptides (2-4 amino acids)… providing wall-clock acceleration of sampling compared to standard MD."
- **Label:** EMPIRICAL (classical ML). *Relevance:* This is an exact MH-corrected learned proposal. It is the **classical twin of any "quantum proposal inside MCMC" scheme**. Current scope is 2–4 residues.

**E78. Transferable Boltzmann generators** | L. Klein, F. Noé | 2024 | NeurIPS 2024 | — | arXiv 2406.14426 | [AX][WS: proceedings.neurips.cc/…/5035a409…]
- *Key claim (abstract):* "approximate sampling from the target distribution of unseen systems, as well as efficient reweighting to the target Boltzmann distribution… evaluated on dipeptides".
- **Label:** EMPIRICAL (classical ML). *Scope:* dipeptides.

**E79. Scalable equilibrium sampling with sequential Boltzmann generators** | C.B. Tan, A.J. Bose, C. Lin et al. | 2025 | ICML 2025 | — | arXiv 2502.18462 | [AX]
- *Key claim (abstract):* "inference-time scaling of flow samples using a continuous-time variant of sequential Monte Carlo… demonstrating the first equilibrium sampling in Cartesian coordinates of tri-, tetra- and hexa-peptides that were thus far intractable for prior Boltzmann generators."
- **Label:** EMPIRICAL (classical ML). *Relevance:* **Exact (reweightable) learned samplers currently stop at ~hexapeptides in all-atom Cartesian coordinates.** This is a genuine frontier. It is not evidence of intractability.

**E80. AlphaFold meets flow matching for generating protein ensembles (AlphaFlow/ESMFlow)** | B. Jing, B. Berger, T. Jaakkola | 2024 | ICML 2024 | — | arXiv 2402.04845 | [AX]
- *Key claim (abstract):* "superior combination of precision and diversity compared to AlphaFold with MSA subsampling… faster wall-clock convergence to certain equilibrium properties than replicate MD trajectories".
- **Label:** EMPIRICAL (classical ML). *Limitation:* No Boltzmann weights. It is trained on MD (ATLAS-type) ensembles, which are short-timescale.

**E81. Str2Str: a score-based framework for zero-shot protein conformation sampling** | J. Lu, B. Zhong, Z. Zhang et al. | 2024 | ICLR 2024 | — | arXiv 2306.03117 | [AX]
- *Key claim (abstract):* "has no reliance on simulation data during both training and inference… can be orders of magnitude faster compared to long MD simulations." **Label:** EMPIRICAL.

**E82. Direct generation of protein conformational ensembles via machine learning (idpGAN)** | G. Janson, G. Valdes-Garcia, L. Heo, M. Feig | 2023 | Nat. Commun. 14 | 10.1038/s41467-023-36443-x | — | [CR][OA]
- *Key claim (abstract):* "directly generate physically realistic conformational ensembles of proteins without the need for any sampling and at negligible computational cost… can predict sequence-dependent coarse-grained ensembles for sequences that are not present in the training set". **Label:** EMPIRICAL.

**E83. Scalable emulation of protein equilibrium ensembles with generative deep learning (BioEmu)** | S. Lewis, T. Hempel, J. Jiménez-Luna et al. | 2025 | Science 389 | 10.1126/science.adv9817 | — | [CR][OA][EP][GH]
- *Key claim (abstract):*
  - "generating thousands of statistically independent structures per hour on a single graphics processing unit (GPU)"
  - "integrates more than 200 milliseconds of molecular dynamics (MD) simulations, static structures, and experimental protein stabilities"
  - "predicts relative free energies with 1 kilocalorie per mole accuracy compared with millisecond-scale MD and experimental data"
  - "amortizes the cost of MD".
- *Cost scaling (GitHub README, A100, 1000 samples):* 100 aa → 4 min; 300 aa → 40 min; 600 aa → 150 min, i.e. roughly L^2. README: "This code only supports sampling structures of monomers."
- *Limitations:*
  - Monomers only.
  - The approximate equilibrium distribution has no exact Boltzmann weights. It relies on an MSA/AF2-style input.
  - Rare-state accuracy is bounded by training data.
- **Label:** EMPIRICAL ADVANTAGE (classical ML over MD, wall-clock). *Relevance:* **For monomer ensembles at 300 K, BioEmu removes most of the sampling cost that a quantum sampler would target.**

**E84. Predicting equilibrium distributions for molecular systems with deep learning (DiG)** | S. Zheng, J. He, C. Liu et al. | 2024 | Nat. Mach. Intell. 6:558–567 | 10.1038/s42256-024-00837-3 | — | [CR][OA]
- *Key claim (abstract):* "efficient generation of diverse conformations and provides estimations of state densities, orders of magnitude faster than conventional methods." **Label:** EMPIRICAL.

**E85. Machine learning coarse-grained potentials of protein thermodynamics** | M. Majewski, A. Pérez, P. Thölke et al. | 2023 | Nat. Commun. 14 | 10.1038/s41467-023-41343-1 | — | [CR][OA]
- *Key claim (abstract):* "approximately 9 ms for twelve different proteins… The coarse-grained models are capable of accelerating the dynamics by more than three orders of magnitude while preserving the thermodynamics". **Label:** EMPIRICAL.

**E86. Navigating protein landscapes with a machine-learned transferable coarse-grained model** | N.E. Charron, K. Bonneau, A.S. Pasos-Trejo et al. | 2025 | Nat. Chem. 17:1284–1292 | 10.1038/s41557-025-01874-0 | — | [CR][OA]
- *Key claim (abstract):* "extrapolative molecular dynamics on new sequences… predicts metastable states of folded, unfolded and intermediate structures… relative folding free energies of protein mutants, while being several orders of magnitude faster than an all-atom model." **Label:** EMPIRICAL.

**E87. Accurate model of liquid–liquid phase behavior of IDPs from optimization of single-chain properties (CALVADOS)** | G. Tesei, T.K. Schulze, R. Crehuet, K. Lindorff-Larsen | 2021 | PNAS 118 | 10.1073/pnas.2111696118 | — | [CR]. **Label:** EMPIRICAL (CG model).

**E88. Conformational ensembles of the human intrinsically disordered proteome** | G. Tesei, A.I. Trolle, N. Jonsson et al. | 2024 | Nature 626:897–904 | 10.1038/s41586-023-07004-5 | — | [CR][EP]
- *Key claim (abstract):* "we developed an efficient molecular model to generate conformational ensembles of IDRs… we use this model to simulate nearly all of the IDRs in the human proteome. Examining conformational ensembles of 28,058 IDRs".
- **Label:** EMPIRICAL (classical CG). *Relevance:* **IDP ensembles at CG resolution are classically cheap at proteome scale.** They are not a quantum target.

### 2.10 Single-structure prediction and its limitations

**E89. Highly accurate protein structure prediction with AlphaFold (AF2)** | J. Jumper, R. Evans, A. Pritzel et al. | 2021 | Nature 596:583–589 | 10.1038/s41586-021-03819-2 | — | [CR][PMC]
- *Key claims (full text).*
  - Accuracy: "median backbone accuracy of 0.96 Å r.m.s.d.95… whereas the next best performing method had a median backbone accuracy of 2.8 Å".
  - Calibration: "pLDDT reliably predicts the Cα local-distance difference test (lDDT-Cα) accuracy". Fig. 2c: "lDDT-Cα = 0.997 × pLDDT − 1.17 (Pearson's r = 0.76). n = 10,795 protein chains".
  - MSA depth: "the accuracy decreases substantially when the median alignment depth is less than around 30 sequences… improvements in MSA depth over around 100 sequences lead to small gains."
  - Complexes: "much weaker for proteins that have few intra-chain or homotypic contacts compared to the number of heterotypic contacts".
- **Label:** EMPIRICAL (classical ML). *Relevance:* Accuracy is gated by **evolutionary information** (MSA depth), which is the signature of an information-limited problem.

**E90. Highly accurate protein structure prediction for the human proteome** | K. Tunyasuvunakool, J. Adler, Z. Wu et al. | 2021 | Nature 596:590–596 | 10.1038/s41586-021-03828-1 | — | [CR][OA]
- *Key claim (abstract):* "covers 58% of residues with a confident prediction, of which a subset (36% of all residues) have very high confidence… identifying… regions that are likely to be disordered." **Label:** EMPIRICAL.

**E91. RoseTTAFold: accurate prediction of protein structures and interactions using a three-track neural network** | M. Baek, F. DiMaio, I. Anishchenko et al. | 2021 | Science 373:871–876 | 10.1126/science.abj8754 | — | [CR][OA]. "accuracies approaching those of DeepMind in CASP14". **Label:** EMPIRICAL.

**E92. Evolutionary-scale prediction of atomic-level protein structure with a language model (ESMFold)** | Z. Lin, H. Akin, R. Rao et al. | 2023 | Science 379:1123–1130 | 10.1126/science.ade2574 | — | [CR][OA]
- *Key claim (abstract):* "an order-of-magnitude acceleration of high-resolution structure prediction… predicting structures for >617 million metagenomic protein sequences, including >225 million that are predicted with high confidence".
- **Label:** EMPIRICAL. *Relevance:* Single-structure inference is cheap (proteome/metagenome scale) and not compute-limited.

**E93. Accurate structure prediction of biomolecular interactions with AlphaFold 3** | J. Abramson, J. Adler, J. Dunger et al. | 2024 | Nature 630:493–500 | 10.1038/s41586-024-07487-w | — | [CR][OA]
- *Key claim (abstract):* "diffusion-based architecture… capable of predicting the joint structure of complexes including proteins, nucleic acids, small molecules, ions and modified residues". **Label:** EMPIRICAL.

**E94. AlphaFold2 fails to predict protein fold switching** | D. Chakravarty, L.L. Porter | 2022 | Protein Sci. 31 | 10.1002/pro.4353 | — | [CR][OA]
- *Key claim (abstract):*
  - "tested AlphaFold2's performance on 98-fold-switching proteins… 94% of AlphaFold2 predictions captured one experimentally determined conformation but not the other."
  - "AlphaFold2's estimated confidences were moderate-to-high for 74% of fold-switching residues".
- **Label:** NO ADVANTAGE (a limitation of the classical ML method). *Relevance:* pLDDT is **miscalibrated for alternative states**.

**E95. Extant fold-switching proteins are widespread** | L.L. Porter, L.L. Looger | 2018 | PNAS 115:5968–5973 | 10.1073/pnas.1800168115 | — | [CR][OA]
- *Key claim (abstract):* "we used it to estimate that 0.5-4% of PDB proteins switch folds." **Label:** EMPIRICAL.

**E96. Sampling alternative conformational states of transporters and receptors with AlphaFold2** | D. del Alamo, D. Sala, H.S. Mchaourab et al. | 2022 | eLife 11 | 10.7554/eLife.75751 | — | [CR][OA]
- *Key claim (abstract):* "reducing the depth of the input multiple sequence alignments by stochastic subsampling led to the generation of accurate models in multiple conformations… (average template modeling score of 0.94)". **Label:** EMPIRICAL.

**E97. Predicting multiple conformations via sequence clustering and AlphaFold2 (AF-Cluster)** | H.K. Wayment-Steele, A. Ojoawo, R. Otten et al. | 2024 (online 2023) | Nature 625:832–839 | 10.1038/s41586-023-06832-9 | — | [CR][OA]
- *Key claim (abstract):* "clustering a multiple-sequence alignment by sequence similarity enables AlphaFold2 to sample alternative states of known metamorphic proteins with high confidence". Mutations predicted to flip KaiB were "experimentally verified". **Label:** EMPIRICAL (**ADVANTAGE DISPUTED**, see E98–E99).

**E98. Sequence clustering confounds AlphaFold2 (Matters Arising)** | J.W. Schafer, M. Lee, D. Chakravarty, J.F. Thole, E.A. Chen, L.L. Porter | 2025 | Nature 638:E8–E12 | 10.1038/s41586-024-08267-2 | bioRxiv 10.1101/2024.01.05.574434 | [CR][EP(PubMed record)][OA(bioRxiv abstract)]
- *Key claim (bioRxiv abstract):*
  - "random sequence sampling outperforms sequence clustering, challenging the claim that AF-cluster works by 'deconvolving conflicting sets of couplings.'"
  - "AF-cluster mistakes some single-folding KaiB homologs for fold switchers"
  - "predicts many correct structures with low confidence and some experimentally unobserved conformations with confidences similar to experimentally observed ones."
- **Label:** ADVANTAGE DISPUTED.

**E99. Does sequence clustering confound AlphaFold2? (reply)** | H.K. Wayment-Steele, S. Ovchinnikov, L. Colwell et al. | 2025 | J. Mol. Biol. 437:169376 | 10.1016/j.jmb.2025.169376 | bioRxiv 10.1101/2024.07.29.605333 | [CR][OA]
- *Key claim (abstract):* "Porter et al.'s primary critique, that AF-Cluster does not use local evolutionary couplings in its MSA clusters, is incorrect… local evolutionary couplings do indeed play an important role in AF-Cluster predictions". **Label:** ADVANTAGE DISPUTED (live dispute).

**E100. AlphaFold predictions of fold-switched conformations are driven by structure memorization** | D. Chakravarty, J.W. Schafer, E.A. Chen et al. | 2024 | Nat. Commun. 15 | 10.1038/s41467-024-51801-z | — | [CR][OA]
- *Key claim (abstract):*
  - "AF is a weak predictor of fold switching and… some of its successes result from memorization of training-set structures rather than learned protein energetics."
  - "Combining >280,000 models… a 35% success rate… AF2's confidence metrics selected against models consistent with experimentally determined fold-switching structures and failed to discriminate between low and high energy conformations."
  - "AF captured only one out of seven experimentally confirmed fold switchers outside of its training sets".
- **Label:** NO ADVANTAGE (a limitation). *Relevance:* ~280k models of extra sampling did **not** fix it. More samples from the same learned distribution do not create missing information. This is the same lesson as the predecessor's I-1…I-6.

**E101. High-throughput prediction of protein conformational distributions with subsampled AlphaFold2** | G. Monteiro da Silva, J.Y. Cui, D.C. Dalgarno et al. | 2024 | Nat. Commun. 15 | 10.1038/s41467-024-46715-9 | — | [CR][OA]
- *Key claim (abstract):* "predicted changes in their relative state populations with more than 80% accuracy… worked best when used to qualitatively predict the effects of mutations". **Label:** EMPIRICAL.

**E102. AlphaFold and implications for intrinsically disordered proteins** | K.M. Ruff, R.V. Pappu | 2021 | J. Mol. Biol. 433:167208 | 10.1016/j.jmb.2021.167208 | — | [CR][OA] — **PERSPECTIVE**
- *Key claim (abstract):* "many predictions feature regions of very low confidence, and these regions largely overlap with intrinsically disordered regions (IDRs)… a cautionary note regarding the misinterpretations".

**E103. Systematic identification of conditionally folded intrinsically disordered regions by AlphaFold2** | T.R. Alderson, I. Pritišanac, Đ. Kolarić et al. | 2023 | PNAS 120 | 10.1073/pnas.2304302120 | — | [CR][OA]
- *Key claim (abstract):* "AlphaFold2 assigns confident structures to nearly 15% of human IDRs… AlphaFold2 predictions do not reveal functionally relevant structural plasticity within IDRs and cannot offer realistic ensemble representations".

**E104. AlphaFold predictions are valuable hypotheses and accelerate but do not replace experimental structure determination** | T.C. Terwilliger, D. Liebschner, T.I. Croll et al. | 2024 | Nat. Methods 21:110–116 | 10.1038/s41592-023-02087-4 | — | [CR][OA]
- *Key claim (abstract):* "even very high-confidence predictions differed from experimental maps on a global scale through distortion and domain orientation". **Label:** EMPIRICAL (a calibration limit).

**E105. Proteins with alternative folds reveal blind spots in AlphaFold-based protein structure prediction** | D. Chakravarty, M. Lee, L.L. Porter | 2024 | arXiv 2410.14898 | [AX] — **REVIEW**. "degeneracies in pairwise representations can lead to high-confidence predictions inconsistent with experiment."

**E106. Fold-switching proteins push the boundaries of conformational ensemble prediction** | M. Lee, L.L. Porter | 2026 | arXiv 2601.01740 | [AX] — **REVIEW (preprint)**. "DL models often predict conformational ensembles by association with training-set structures, limiting generalizability."

**E107. Expanding protein structure prediction into conformational state space** | D. Chakravarty, J.J. Miller, D. Teng et al. | 2026 | arXiv 2608.02866 | [AX] — **PERSPECTIVE (preprint)**. "largely solving the problem of identifying a dominant conformation from sequence… structure prediction should be reformulated as a state-space inference problem".

### 2.11 Coarse-grained physical models (candidate "realistic representations")

**E108. AWSEM-MD: protein structure prediction using coarse-grained physical potentials and bioinformatically based local structure biasing** | A. Davtyan, N.P. Schafer, W. Zheng et al. | 2012 | J. Phys. Chem. B 116:8494–8503 | 10.1021/jp212541y | — | [CR][OA]. A 3-bead-per-residue CG force field with memory (fragment) terms. **Label:** EMPIRICAL.

**E109. Topological and energetic factors… transition state ensemble… (Cα Gō model)** | C. Clementi, H. Nymeyer, J.N. Onuchic | 2000 | J. Mol. Biol. 298:937–953 | 10.1006/jmbi.2000.3693 | — | [CR]. Metadata verified. The canonical structure-based Cα model.

**E110. Coarse-grained protein models and their applications** | S. Kmiecik, D. Gront, M. Kolinski et al. | 2016 | Chem. Rev. 116:7898–7936 | 10.1021/acs.chemrev.6b00163 | — | [CR][OA] — **REVIEW**.

### 2.12 Orientation reviews

**E111. Enhanced sampling methods for molecular dynamics simulations (living review)** | J. Hénin, T. Lelièvre, M.R. Shirts et al. | 2022 | LiveCoMS (arXiv 2202.04164) | [AX] — **REVIEW**.

**E112. Enhanced sampling in the age of machine learning: algorithms and applications** | K. Zhu, E. Trizio, J. Zhang et al. | 2025 | arXiv 2509.04291 | [AX] — **REVIEW (preprint)**.

**Count:**
- 112 entries have bibliographic verification.
- About 85 of them also had the abstract or full-text claim verified in-session.
- Entries marked "metadata only" (E1, E10, E14, E21, E22, E29, E30, E37, E42, E46, E49, E52, E57, E68, E71, E74, E75, E87, E109) are **not used as evidence for any specific quantitative claim**.

---

## 3. Primitive analyses (16 questions)

The "primitives" here are the **computational subproblems** of protein-structure computation that a quantum method would have to take over. Each is analysed as: what is hard, what the best classical method is, and what would have to be true for a quantum method to matter. Q14–Q15 (FT / resources) are deferred to the quantum-algorithm domains and are not asserted here.

### P1. Equilibrium (Boltzmann) sampling of conformational ensembles
_Quantum candidates: quantum MCMC / Szegedy walks, quantum simulated annealing, Gibbs-state preparation._

1. **Quantum operation:** Prepare a coherent encoding of the Boltzmann (or posterior) distribution over conformations, or accelerate mixing of a reversible Markov chain.
2. **Replaces:** MD or MCMC (Metropolis, HMC, PT, REST2, SMC/PERM, learned-proposal MCMC) used to draw equilibrium conformations.
3. **Why classically hard.** Four distinct sources, only two of which are exponential:
   - (a) **Energetic barriers**: exp(ΔG‡/kT) waiting times (E10, E15). PT converts this to **polynomial** in barrier height when basins are large (E33).
   - (b) **Entropic / golf-course bottlenecks**: small, hidden basins. PT gives only brute-force-parallel speedup (E33).
   - (c) **Persistence / narrow-vs-wide peaks of comparable mass**: tempering is provably torpid (E39).
   - (d) **First-order (discontinuous) transitions crossed by the tempering parameter**: exponentially slow regardless of schedule (E40, mean-field Potts). Classical fixes exist (entropy dampening, Hamiltonian tempering).
   - Dimension alone is benign: HMC O(d^{1/4}) (E51), RWM O(d) (E50) on product targets.
4. **Exact speedup:** Literature separations are quadratic in the spectral gap (1/√δ vs 1/δ) for quantum walks. That is **not** a separation against PT in general. Defer the exact statements to the QMCMC domain.
5. **Type:** Time / query (walk-operator applications).
6. **Assumptions:** A reversible chain with known gap. Efficient coherent implementation of the chain's transition operator and the energy function. Warm starts or annealing schedules.
7. **Oracle:** A coherent energy evaluation E(x) for the conformational energy (force field or learned pair-distance energy), plus coherent proposal moves.
8. **Oracle construction cost:** A reversible arithmetic circuit for E(x) over O(N²) pair terms at fixed-point precision. For a learned energy (e.g. esmprior-type pair-distance potentials) this is O(N²) neural or spline evaluations per call. Defer the numbers.
9. **State-prep cost:** Encoding continuous coordinates at b bits each needs ~3N·b qubits for Cartesian, or ~2N·b for torsions, plus ancillas.
10. **Readout:** Each measurement yields one sample. Estimating observables still costs O(1/ε²) samples unless combined with amplitude estimation (P2).
11. **Classical postprocessing:** Structural averaging and MBAR-style reweighting (E69), which is cheap.
12. **Strongest classical algorithm** (by regime):
   - Continuous chains with energetic barriers: **PT/REST2 + HMC** (E20, E47, E51).
   - Chains with local interactions: **SMC/PERM** (E53–E54) and **Wang–Landau with pull/pivot moves** (E56, E58).
   - Small peptides with exact correction: **learned-proposal MCMC / SMC-corrected flows** (E77, E79).
   - Monomer ensembles where approximate is acceptable: **amortised generators (BioEmu, AlphaFlow)** (E80, E83).
   - Kinetics-derived equilibria: **MSMs from many short trajectories** (E65, E67).
13. **Does advantage survive?**
   - Not in regimes (a), large-basin energetic barriers: PT is already polynomial (E33).
   - Possibly in (b)–(d), but classical remedies exist for (d) and no protein-specific instance family is proven to be in (b) or (c).
   - For natural proteins at physiological T, landscape theory (E2–E6) and Anton evidence (E16) argue the landscape is funnelled, i.e. not in (b).
   - **Survives only if a specific protein-relevant target (e.g. a learned-energy posterior at ≥ 60–150 aa) is measured to be in regime (b)/(c)/(d).**
14. **Fault tolerance:** Yes for any coherent-walk method at relevant sizes. Defer.
15. **Resources:** Defer to the QMCMC domain. No number asserted here.
16. **Protein mapping:** Direct. This is the predecessor's C-1 / SP-1 (posterior over CA traces under the learned energy). It is the only primitive where the predecessor has *value* evidence (1.40× MDE soft readout) but no *cost* evidence.

### P2. Free-energy and ensemble-expectation estimation
_Quantum candidate: amplitude estimation (QAE) on top of a coherent sampler; quantum-accelerated FEP._

1. **Operation:** Estimate ⟨f⟩ or ΔF to precision ε with O(1/ε) coherent sampler calls.
2. **Replaces:** FEP/TI/MBAR (E68–E70), Jarzynski/nonequilibrium estimators (E71–E72), and population estimates from MSM/WE (E63, E65).
3. **Classical hardness:**
   - (i) Sample *generation* (= P1).
   - (ii) **Overlap**: a single-step exponential average needs N_c ∼ exp(βW_d) realizations, "exponentially with system size" (E72). Classically this is fixed by λ-staging and MBAR (optimal, E69).
   - (iii) Statistical variance O(1/ε²), which is where QAE's quadratic gain would act.
4. **Speedup:** Quadratic in 1/ε (sample complexity) *given* a coherent state-preparation unitary. This does not address (ii) and does not help (i) unless P1 is solved coherently.
5. **Type:** Sample/query complexity.
6. **Assumptions:** A coherent sampler (not classical samples). The observable is encodable as a bounded function.
7. **Oracle:** The P1 sampler unitary plus a coherent observable circuit.
8. **Oracle cost:** Includes all P1 costs.
9. **State prep:** = P1.
10. **Readout:** Phase-estimation-based QAE, or low-depth variants. Defer.
11. **Postprocessing:** Negligible.
12. **Strongest classical:** Multistage alchemical FEP with MBAR (E69, E73). WE for rates (E63). BioEmu gives relative free energies at ~1 kcal/mol for monomers (E83).
13. **Survives?** Only if some decision is **variance-limited** at feasible sample counts. The literature shows error floors dominated by force-field accuracy and slow-mode sampling (E17, E73), not by 1/√n statistical error. This is the predecessor's C-3 / QA-1, "conditional, low prior", and nothing here raises it.
14. **FT:** Yes. **15.** Defer.
16. **Mapping:** Basin populations and ΔG between alternative conformations (fold switchers, E94–E101). But the dominant error there is the *model* (information-limited; E100), not the estimator.

### P3. Rare-event kinetics / hitting times
_Quantum candidates: quantum-walk hitting-time speedups; quantum simulation of dynamics._

1. **Operation:** Find or estimate transitions between metastable states faster than the classical hitting time.
2. **Replaces:** Brute-force MD (E15, E18), TPS (E59–E60), WE (E61–E63), milestoning (E64), MSMs (E65–E67).
3. **Classical hardness:** Waiting time ∝ exp(ΔG‡/kT) (E10). Folding times of 10 μs to seconds (E7, E9, E63). BPTI state interconversion is >10^3 slower than local relaxation (E15).
4. **Speedup:** Quadratic in hitting time for marked-state search via quantum walks (defer). No known exponential speedup for classical stochastic dynamics.
5. **Type:** Query/time.
6. **Assumptions:** A Markovian discretisation (MSM-like). Marked states defined without native leakage.
7. **Oracle:** Coherent transition operator and marking predicate.
8. **Oracle cost:** Requires the coherent force field / energy (P1-8).
9. **State prep:** Stationary-distribution state (P1).
10. **Readout:** Detection of the marked state.
11. **Postprocessing:** Rate extraction (cheap).
12. **Strongest classical:** WE (unbiased, "superlinear scaling", E62; 100 ms folding times, E63), TPS (cost ∝ path length, not waiting time, E60), MSMs (hours-scale kinetics from short trajectories, E67).
13. **Survives?** The classical methods already **remove the exp(ΔG‡/kT) waiting-time factor** for the process of interest. They replace it with costs polynomial in path length and number of states. Their residual problem is **variance** (E63) and **choice of progress coordinate**, not exponential waiting. A quadratic hitting-time gain over brute-force MD is not a gain over WE/TPS/MSM.
14. **FT:** Yes. **15.** Defer.
16. **Mapping:** Folding/unfolding and conformational change kinetics. This is **outside** the predecessor's endpoint (static built-chain RMSD). Not a structure-accuracy lever.

### P4. Global-minimum / single-structure search
_Quantum candidates: Grover / amplitude amplification, QAOA, quantum annealing, VQE._

1. **Operation:** Find argmin E(x) over conformations, with quadratic or heuristic speedup over classical search.
2. **Replaces:** AF2/ESMFold inference (E89, E92), multi-restart minimisation, PERM/FRESS/Wang–Landau on lattice (E53–E56).
3. **Why hard classically:** Worst-case NP-hard (E11–E13). In practice:
   - Lattice HP ground states are found up to 500-mers (E56). FRESS finds new minima for L > 80 (E55).
   - Natural-protein single-structure prediction is limited by **information** (MSA depth < 30 → accuracy drop, E89; memorization, E100), not search.
4. **Speedup:** Quadratic for unstructured search. None proven for structured instances.
5. **Type:** Query.
6. **Assumptions:** Unstructured landscape (golf-course-like). The energy's argmin must equal the correct structure (condition C). E100 and the predecessor's R2 show the latter fails for learned or AF2 confidence functions.
7–11. Same as the predecessor DE-1…DE-3.
12. **Strongest classical:** AF2/AF3/ESMFold for natural proteins. PERM/FRESS/WL for lattice. Restart-saturated L-BFGS (predecessor QX-30).
13. **Survives?** **No** on current evidence. Natural landscapes are funnelled (E2–E5), and the unstructured-search regime is excluded by physics. The predecessor measured argmin readouts as classically reproducible (R1–R2), and restart saturation at 44–60 aa.
14–15. N/A.
16. **Mapping:** Predecessor S-1…S-7, DE-1…DE-3: already tested and failed.

### P5. Ensemble generation from sequence (distributional prediction)
_Quantum candidates: quantum generative models (Born machines) as ensemble generators._

1. **Operation:** Sample conformations from a learned sequence-conditioned distribution.
2. **Replaces:** BioEmu, AlphaFlow, Str2Str, idpGAN, DiG, subsampled AF2 (E80–E84, E96–E101).
3. **Why hard:** Generation is **not** computationally hard (thousands of samples/hour/GPU, E83). The hardness is information and training data: rare states and alternative folds absent from training (E94, E100, E106).
4. **Speedup:** None known that applies. A quantum model cannot create information absent from its inputs (the predecessor's DE-6, data-processing inequality).
5–11. N/A.
12. **Strongest classical:** BioEmu (monomers; 1000 × 100-aa samples in 4 min on an A100, E83), AlphaFlow (E80), CALVADOS for IDRs (E88).
13. **Survives?** **No.**
16. **Mapping:** The predecessor's DE-6 (tempered Born machine ≤ Metropolis).

### P6. Energy-function accuracy (electronic structure)
_Brief; belongs to another domain._

A quantum computer could improve the *energy* (QM for metal sites or strong correlation). In this domain's literature the dominant residual errors are force-field accuracy for folding thermodynamics (E17, E73) and training data for ML ensembles (E83, E100). Nothing in Domain E shows that electronic-structure accuracy for correlated sites is the bottleneck for *structure* computation. This matches the predecessor's AA-3 and DE-7. **Label: out of scope here.**

---

## 4. Strongest classical counterarguments

1. **Funnels remove the exponential.** Natural proteins are minimally frustrated (E4). A few kT of bias collapses the Levinthal time (E2). Lattice MC folding time is **polynomial** (N^4 designed, N^6 random) at the optimal temperature (E6). Physical folding obeys a ~N/100 μs speed limit (E9). The "unstructured search" regime that quantum search accelerates is excluded by the physics of foldable sequences.
2. **Parallel tempering already delivers an exponential classical speedup** on energetic double-well landscapes: polynomial equilibration in barrier height with R ∝ √(barrier) replicas (E33). A quantum walk's quadratic gain over *local* MCMC is therefore not a gain over PT in that regime.
3. **Dimension is benign.**
   - HMC costs O(d^{1/4}) (E51).
   - Replicas grow as √N (E23, E28).
   - REST2 removes the solvent contribution (E47).
   - Pivot moves cost O(1)–O(log N) per attempt (E58).
   - PERM handles 10^6-mers at θ (E53).
   - Wang–Landau finds HP ground states and the full density of states up to 500-mers (E56).
4. **Rare-event classical methods remove waiting-time exponentials.** WE: unbiased, superlinear, 10 μs–100 ms folding times (E62–E63). TPS: no transition-state knowledge needed (E60). MSMs: kinetics to hours (E67). The remaining costs are variance and CV design, and they are polynomial.
5. **Free-energy estimators are statistically optimal** (MBAR, E69). The exponential-in-size cost of single-step exponential averaging (E72) is avoided by staging. Industrial FEP works (E73). Errors are force-field dominated.
6. **Amortised learned samplers make generation nearly free.**
   - BioEmu: thousands of independent samples per GPU-hour, ~1 kcal/mol ΔG, ~L² cost (E83).
   - AlphaFlow beats replicate MD on wall-clock for some observables (E80).
   - CALVADOS simulated 28,058 IDRs (E88).
   - ML-CG models are ≥10³× faster than all-atom (E85–E86).
7. **Single-structure prediction is information-limited, not compute-limited.** AF2 accuracy is gated by MSA depth (~30 sequences, E89). ESMFold predicts 617M structures (E92). The failure on fold switchers persists after ~280,000 extra samples (E100): more compute on the same distribution did not help.
8. **Exact learned samplers are the natural classical twin of any "quantum proposal".** Learned proposals with MH (Timewarp, E77) or SMC correction (SBG, E79) give exact Boltzmann sampling with learned global moves. A quantum sampler must beat these, not vanilla Metropolis.

**Counter-counterarguments (where classical hardness is real):**
- (i) Rigorous **torpid-mixing** results for PT/ST exist:
  - persistence (narrow vs wide peaks of comparable mass, E39)
  - first-order transitions (E40)
  - golf courses (E33).
- (ii) Exact reweightable learned samplers stop at about **hexapeptides** (E79).
- (iii) BioEmu/AlphaFlow are **approximate**, with no exact Boltzmann weights. Their rare-state fidelity is bounded by training data.
- (iv) All-atom brute-force MD remains ~100 μs/day at 10^6 atoms even on Anton 3 (E18).

None of (i)–(iv) has been shown for a *protein-structure-accuracy* endpoint.

---

## 5. Scaling statements (explicit, with source and location)

| # | Quantity | Statement | Source (location) | Type |
|---|---|---|---|---|
| S1 | PT replicas vs system size | "the number of replicas increases as √N" | Earl & Deem 2005 (E23), §on temperature choice, full text | Scaling argument |
| S2 | PT replicas vs system size | "N_opt ∝ √V" | Nadler & Hansmann 2007 (E28), full text | Analytic |
| S3 | PT replicas vs solvent | TREM acceptance depends on the number of waters; REST2 "does not depend on the number of explicit water molecules" | Wang, Friesner, Berne 2011 (E47), abstract | Empirical/analytic |
| S4 | PT on double well, vs barrier | R_opt ∼ (β0−βc)√K. Diffusive τ_D ∼ K(β0−βc)² (∝ barrier). Ballistic τ_B ∼ √barrier. "exponential to a polynomial in the barrier height" | Machta 2009 (E33), Eqs. 11–12, 20 and text | Analytic |
| S5 | PT on golf course | Only "modest speed-up… due to brute force parallelism" (factor ~R). Local Metropolis equilibration "exponential in N" | Machta 2009 (E33), §IV | Analytic |
| S6 | PT/ST torpid mixing | "anytime a multimodal distribution includes both very narrow and very wide peaks of comparable probability mass, parallel and simulated tempering are shown to mix slowly" | Woodard et al. 2009 EJP (E39), abstract | Rigorous |
| S7 | ST on first-order transitions | mean-field 3-state Potts: "converges slowly regardless of the temperature schedule"; "exponential factor longer than the mixing time at the fixed temperature" | Bhatnagar & Randall 2016 (E40), abstract | Rigorous |
| S8 | PT rapid mixing | Spectral-gap lower bounds; rapid mixing for normal mixtures and the mean-field Ising model | Woodard et al. 2009 AAP (E38), abstract | Rigorous |
| S9 | REMD vs MD efficiency | Efficiency ratio = ratio of averaged transition counts | Rosta & Hummer 2009 (E36), abstract | Analytic |
| S10 | REMD replicas | "number of replicas… has a minimal effect on the asymptotic efficiency" | Nymeyer 2008 (E34), abstract | Analytic |
| S11 | RWM vs dimension | Proposal variance scaled with n; optimal acceptance 0.234 (product targets) → O(n) steps | Roberts, Gelman, Gilks 1997 (E50), abstract | Rigorous (idealised) |
| S12 | HMC vs dimension | "h = l × d^{−1/4}… O(d^{1/4}) steps"; acceptance 0.651 | Beskos et al. 2013 (E51), abstract | Rigorous (i.i.d.) |
| S13 | Lattice folding time vs N | N^λ at T of fastest folding; λ≈6 random, ≈4 designed; Arrhenius at low T | Gutin, Abkevich, Shakhnovich 1996 (E6), abstract | Simulation |
| S14 | Physical folding time vs N | Speed limit ≈ N/100 μs | Kubelka, Hofrichter, Eaton 2004 (E9), abstract | Exp./theory |
| S15 | Physical folding time vs N | Folding time correlates with size, precision ~1.1 decades (functional form unverified) | Naganathan & Muñoz 2005 (E7), abstract | Empirical |
| S16 | Folding rate vs topology | Rate correlates with contact order; "No significant relationship… between protein length and folding rates" | Plaxco, Simons, Baker 1998 (E8), abstract | Empirical |
| S17 | Exponential-average FE estimators | N_c ∼ exp(βW_d), "exponentially with system size" | Jarzynski 2006 (E72), Eq. 34 and text | Analytic |
| S18 | Pivot moves (SAW) | O(1) (2D) to O(log N) (3D) time per attempted pivot | Clisby 2010 (E58), abstract | Heuristic + numerics |
| S19 | PERM chain length | Chains up to N = 10^6 at θ (finite volume) | Grassberger 1997 (E53), abstract | Numerics |
| S20 | Lattice HP ground states | Up to 500 residues (Wang–Landau); new minima for L > 80 (FRESS) | E56, E55 abstracts | Numerics |
| S21 | Brute-force MD throughput | >100 μs/day at 10^6 atoms (512-node Anton 3) | Shaw et al. 2021 (E18), abstract | Hardware |
| S22 | Weighted ensemble | Folding times 10 μs–100 ms estimated; "superlinear scaling" | E63, E62 abstracts | Empirical |
| S23 | BioEmu cost vs length | 1000 samples: 4 / 40 / 150 min at L = 100 / 300 / 600 (A100) → ~L² | microsoft/bioemu README (E83) | Empirical |
| S24 | AF2 accuracy vs information | Drops below ~30 median MSA depth; small gains beyond ~100 | Jumper et al. 2021 (E89), "MSA depth" section | Empirical |
| S25 | Exact learned Boltzmann samplers | Reach tri/tetra/hexapeptides (SBG), dipeptides (TBG), 2–4-residue peptides (Timewarp) | E79, E78, E77 abstracts | Empirical frontier |

**Not found (explicit gaps):**
- A rigorous mixing-time bound for PT/HMC on any **off-lattice protein or Cα-chain model** as a function of the number of residues.
- A proof that cooperative (two-state) protein folding places tempering in the torpid first-order regime of S7.
- Any scaling law for sampling **learned (ML) protein energies** such as pair-distance posteriors.

---

## 6. NISQ vs fault-tolerant route (from the classical side)

- **NISQ.** The classical baselines above make NISQ sampling claims implausible for protein ensembles:
  - Any NISQ sampler at ≤ ~100 qubits represents ≤ ~100 bits of conformation (e.g. ~15–30 residues at 2–3 bits per torsion pair).
  - At that size, PT/HMC, exact enumeration (lattice) or learned-proposal MCMC already equilibrate (E6, E33, E56, E77).
  - The predecessor measured exactly this at 18 qubits: Metropolis was near-exact (SP-4).
  - A NISQ "sampling advantage" would additionally need to beat approximate amortised generators (BioEmu) on wall-clock, which run in minutes (S23).
  - **Verdict: no NISQ route in this domain.**
- **Fault-tolerant.** The only coherent route with a known separation is quantum-walk / QMCMC acceleration of a slow-mixing reversible chain (P1). It becomes relevant only if:
  - (a) a protein-relevant target is shown to lie in a torpid regime for the *best* classical sampler (PT/REST2 + learned proposals + SMC), not merely for local Metropolis; and
  - (b) the coherent energy oracle (O(N²) pair terms, or a neural energy) is affordable.
- The literature in this domain supplies (a)'s *templates* (E33, E39, E40) but no protein instance. Resource numbers are deferred.

---

## 7. Protein mapping, the four key questions, and the S29–S33 connection

### (A) Computation-limited vs information-limited subproblems

| Subproblem | Limited by | Evidence |
|---|---|---|
| Single dominant structure from sequence (natural, MSA-rich) | **Information** (MSA depth / training data); inference is cheap | E89 (MSA ≥ ~30), E92 (617M structures), E107 ("largely solving") |
| Alternative conformations / fold switching | **Information** (memorization; extra sampling does not help) | E94, E100 (~280k models, 1/7 out-of-training), E98–E99 (dispute) |
| IDP ensembles (CG level) | Neither is severe: classically cheap at proteome scale; limited by force-field accuracy | E88, E102–E103 |
| Equilibrium ensembles of folded monomers at 300 K | Largely **amortised** by ML (approximate); residual fidelity is training-data limited | E83, E80, E85–E86 |
| **Exact** Boltzmann sampling under a given energy, at ≥ tens of residues, all-atom or learned | **Computation** (mixing across metastable basins); exact learned samplers stop at ~6 residues | E15, E79, E33, E39 |
| Kinetics of slow transitions (ms–s), large systems | **Computation**, but classically addressed by WE/TPS/MSM; residual problem is variance and CVs | E63, E67, E60 |
| Absolute/relative free energies (binding, stability) | Mostly **force-field accuracy**, then slow-mode sampling; estimators are optimal | E69, E73, E17 |
| Lattice/HP ground states | **Computation** in worst case (NP-complete), but practically solved to 500-mers | E12, E56 |

### (B) Explicit scaling of the best classical samplers
See §5.
- **System size:** Replicas grow as √N, with round trips ∝ N_rep² in the diffusive regime (I(prog) from E33 Eq. 12 + E28). HMC steps grow as d^{1/4}.
- **Barrier height:** PT gives polynomial ∝ barrier (diffusive) or √barrier (ballistic) for large-basin landscapes. Entropic golf courses and first-order transitions stay exponential for tempering.
- **Temperature:** REMD gains only if folding has positive activation enthalpy, and T_max matters strongly (E34). Arrhenius behaviour appears below the fastest-folding temperature (E6).
- **Lattice folding time:** N^4–N^6.

### (C) Where learned generative models already make a quantum sampler moot
- Approximate 300 K monomer ensembles (BioEmu, AlphaFlow).
- CG IDP ensembles (CALVADOS/idpGAN).
- Relative stabilities at ~1 kcal/mol (BioEmu).
- Qualitative population shifts (subsampled AF2).
- Learned-proposal exact MCMC (Timewarp/SBG) is the classical twin of "quantum proposals".

A quantum sampler is **not** moot where:
- **exact** Boltzmann weights are required for a *specified* energy at ≥ tens of residues; or
- the target is a non-physical learned posterior (like the predecessor's esmprior energy) for which no amortised generator exists.

The second is exactly the predecessor's SP-1. But a classical amortised model or tempered SMC could also be trained or run for that posterior, so the classical twin set must include them.

### (D) A "realistic protein representation" for a quantum sampling test, and its strongest classical sampler

**Minimum requirements (I(prog) from this literature):**
1. **Off-lattice chain.** Cα trace or backbone torsions, at a resolution where the endpoint (built-chain RMSD or ensemble observables) is meaningful. Lattice HP is disqualified: classically solved to 500-mers (E56), and the predecessor's DE-8.
2. **Scalable instance family.** Lengths from 30 to ≥ 150 residues, so the scaling of the classical mixing time can be *measured*, not inferred.
3. **An energy whose samples matter.** Better samples must improve the endpoint (condition C; the predecessor's 1.40× soft-readout signal at mid30 is the only such evidence).
4. **A demonstrated classical hard regime** for the *best* sampler: persistence (E39), first-order-like tempering bottleneck (E40) or golf-course entropic bottleneck (E33). Slow local Metropolis alone is not enough.
5. **A native-free, coherently implementable energy oracle.** O(N²) pair terms.

**Strongest classical sampler to beat for such a representation:**
- **PT or REST-style Hamiltonian tempering + HMC** (E20, E47, E51), with feedback-optimised ladders (E31–E32).
- **SMC / annealed importance sampling / PERM-style growth with resampling** (E53, E54, E74, E75).
- **Learned-proposal MCMC or SMC-corrected flows** (E77, E79).
- **Entropy-dampened or Hamiltonian tempering** where temperature tempering is torpid (E40).
- **An amortised approximate generator** (BioEmu-like) used as an independence proposal with MH or importance correction.

This is a **portfolio**. Any quantum claim must beat the best member at equal wall-clock or equal energy-oracle calls.

### Relation to S29–S33
- **Already tested and failed:** P4 (argmin / structure search: VQE, CVaR, registers) and P5 (Born machine as ensemble generator). The failures are explained by this literature:
  - Funnelled or saturated search (E2–E6; predecessor QX-30).
  - Classical samplers at ≤ 22 qubits are near-exact (SP-4).
  - Information limits (E89, E100 mirror I-1…I-6).
- **Untested:** P1 on the learned-energy posterior at ≥ 60 aa (C-1 / SP-1 / AA-1). The literature supplies:
  - the measurement protocol: round-trip times (E23, E31), ESS, spectral-gap proxies, and persistence diagnostics (E39: "commonly used convergence diagnostics will fail to detect" torpid mixing, so diagnostics must include multi-start and basin-population cross-checks);
  - the classical twin portfolio above.
- **What would be different from S29–S33:** The quantum role would be sampling (not argmin), consumed through a whole-distribution readout (Boltzmann weighting). That is outside the H-001 reduction class *only if* the classical sampler is shown to be slow. The E39 warning means the kill test must use cross-validated basin populations, not just τ_int.

---

## 8. Literature gaps (novelty ≠ advantage)

1. **No mixing-time theory for off-lattice protein chains.** No rigorous or even systematic empirical scaling of PT/HMC/SMC mixing with residue count for Cα or torsion models was found (S-gap). Filling this is novel. It is a *classical* result, and a positive finding (slow mixing) is necessary but not sufficient for quantum advantage.
2. **Tempering across cooperative folding transitions.** Rigorous torpidity is proven for mean-field Potts (E40) and for persistence (E39). Whether two-state protein folding at the scale of 100–300 residues puts temperature tempering into that regime, after using REST2 / Hamiltonian tempering / entropy dampening, is unaddressed in what I found.
3. **Sampling learned (ML) energies.** No literature characterises the landscape ruggedness of learned pair-distance or language-model-derived energies (the predecessor's esmprior class). These could be *more* frustrated than physical funnels. This is unknown and untested.
4. **Exact learned samplers beyond hexapeptides** (E79). This is a classical-ML frontier. Progress there shrinks any quantum window.
5. **Calibration of ensemble generators on rare states** (E94, E100, E106). This is an information/training problem. A quantum sampler cannot fill it.
6. **Novelty ≠ advantage.** "First quantum sampling of protein X" results will be classically trivial at the sizes a quantum device can encode (§6). Only a result against the §7(D) classical portfolio on an instance family with measured classical slow mixing is meaningful.

---

## 9. Unverified leads (not cited as evidence)

- **Naganathan & Muñoz 2005 functional form.** I believe it fits ln(τ_f) ∝ N^{1/2}. Only the abstract (size correlation, 1.1 decades) was verified.
- **Madras & Sokal 1988 pivot acceptance fraction.** Acceptance ~N^{−p}, with p ≈ 0.19 (2D) / 0.11 (3D). Not verified.
- **Lindorff-Larsen et al. 2011 size range.** Largest protein ~80 residues (λ-repressor); aggregate simulated time ~8 ms. Not verified verbatim.
- **Denschlag, Lingenheil & Tavan 2008/2009 (E29, E30).** Content on REMD pseudo-convergence and optimal ladders not read.
- **Bryngelson & Wolynes (1987/1989).** Quantitative T_f/T_g criterion and glass-transition statements not quoted.
- **Earl & Deem's ref. 4.** The primary derivation of the √N replica scaling was not traced.
- **PT on 3D spin glasses.** Exponential-in-N equilibration times (Janus collaboration / Katzgraber et al.) not searched.
- **Sly (2010) / Galanis et al.** Hardness of approximate sampling for spin systems (worst-case #P / NP-hardness of sampling) not searched.
- **Hart & Istrail (1996).** Approximation algorithms for HP folding not searched.
- **MDGen (Jing et al. 2024, arXiv 2409.17808).** Generative MD trajectories; not verified.
- **ATLAS / mdCATH MD datasets.** Not verified.
- **BioEmu independent benchmarks** (including a claimed 55–90% domain-motion success rate from a search-engine summary). Not verified against the paper.
- **Rathore et al. 2005.** The specific acceptance-rate optimum (~20%) as a result *of this paper* is not verified; the 20% rule is verified from Kone & Kofke (E25).
- **Neuhaus & Hager / Janke.** Explicit results on first-order-transition barriers ∝ N^{(d−1)/d} for multicanonical sampling, as they would apply to proteins. Not searched.

---

## 10. Bottom-line verdicts per primitive

**P1 — Equilibrium (Boltzmann/posterior) sampling of conformational ensembles: INTERESTING (conditional; the only live candidate).**
- **For:** It is the only protein subproblem that is genuinely computation-limited *when exact samples of a specified energy are required at ≥ tens of residues*. Exact learned samplers stop at ~6 residues (E79). Rigorous torpid-mixing results for tempering exist (E39, E40). The golf-course regime defeats PT (E33).
- **Against:** Natural protein landscapes are funnelled (E2–E6, E16), and PT turns energetic barriers into polynomial cost (E33). A protein-relevant instance in a torpid regime has never been exhibited. The classical twin must be a portfolio (PT/REST2 + HMC + SMC + learned-proposal MCMC + amortised generators), not Metropolis.
- **Upgrade path:** Measure mixing-time growth vs length on the predecessor's learned-energy posterior (C-1) using the diagnostics in §7. It would go to PROMISING only if slow mixing persists against the full portfolio *and* samples transmit to the endpoint.

**P2 — Free-energy / expectation estimation (amplitude estimation): WEAK.**
- MBAR is statistically optimal (E69). The exponential cost of single-step estimators (E72) is removed classically by staging.
- Practical errors are dominated by force-field accuracy and slow-mode sampling (E17, E73). The 1/ε² variance that QAE attacks is not the bottleneck.
- Any gain presupposes P1 solved coherently. No variance-limited protein decision is documented.

**P3 — Rare-event kinetics / hitting times: WEAK.**
- WE, TPS and MSMs already remove the exp(ΔG‡/kT) waiting-time factor (E60, E62–E63, E67). A quadratic hitting-time gain over brute-force MD is not a gain over these.
- Kinetics are also outside the program's structure-accuracy endpoint.

**P4 — Global-minimum / single-structure search (Grover, QAOA, annealing, VQE): KILLED.**
- The problem is information-limited (E89, E100). Landscapes are funnelled, excluding the unstructured-search regime (E2–E6).
- Classical methods solve even NP-complete lattice versions to 500-mers (E56).
- The predecessor measured exactly this failure (R1–R2, DE-1…DE-3).

**P5 — Quantum generative models as ensemble generators: KILLED.**
- Generation is cheap classically: BioEmu at ~L² minutes per 1000 samples (E83); CALVADOS proteome-scale IDRs (E88).
- The residual failures (rare/alternative states) are training-information limits that no sampler fixes (E100).
- The predecessor's DE-6.

**P6 — Electronic-structure energies for structure accuracy: WEAK (out of scope).**
- Domain-E literature identifies force-field and training-data limits, not correlated-electron accuracy, as the bottleneck for structure/ensemble computation.
