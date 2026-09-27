# Domain D: Quantum protein folding, peptide and biomolecular-conformation literature (critical evidence notes)

_Literature agent D, 2026-09-26. Every paper in §2 was verified in this session. The verification URL or API is given per entry. Where only the metadata was verified and I did not read the content, the entry says "metadata-only" and I make no content claims beyond the abstract. Quotes come from the arXiv abstract or from the full text extracted with `pdftotext` from the arXiv PDF. Locations are given as abstract, § or page._

---

## 1. Scope and search log

**Scope.**
- Quantum algorithms for protein, peptide and lattice-heteropolymer structure: lattice or coarse-grained folding, torsional folding, side-chain packing, lattice sequence design, and conformational sampling with QA.
- Industry hardware "record" claims: IBM/Cleveland Clinic, Kipu/IonQ, QDockBank; Moderna/IBM mRNA as boundary.
- The complexity of lattice folding.
- The strongest classical lattice solvers, used as counterarguments.
- Boundary context: electronic structure of biomolecular active sites, and drug-discovery reviews (orientation only).

**Tools.** WebSearch; WebFetch on arXiv abs pages; the arXiv export API (`export.arxiv.org/api/query`); the Crossref REST API (`api.crossref.org/works/<doi>`); Europe PMC REST (for PubMed abstracts); arXiv PDFs downloaded and converted with `pdftotext` to extract numbers and quotes. Nature, APS, ACS and Springer pages returned 303 or 403, so those DOIs were verified through Crossref, arXiv journal-ref and Europe PMC instead.

**Queries used (WebSearch):**
1. Perdomo-Ortiz 2012 Scientific Reports "Finding low-energy conformations of lattice protein models by quantum annealing"
2. Babbush Perdomo-Ortiz "Construction of energy functions for lattice heteropolymer models" arXiv
3. Fingerhuth Babej Ing "quantum alternating operator ansatz with hard and soft constraints for lattice protein folding"
4. Robert Barkoutsos Woerner Tavernelli "Resource-efficient quantum algorithm for protein folding" npj QI
5. Outeiral "Investigating the potential for a limited quantum speedup on protein lattice problems" NJP
6. Linn "Resource analysis of quantum algorithms for coarse-grained protein folding models"
7. Doga "A perspective on protein structure prediction using quantum computers" JCTC 2024
8. Boulebnane … "Peptide conformational sampling using the QAOA" npj QI 2023
9. Kipu Quantum IonQ "Protein folding with an all-to-all trapped-ion quantum computer"
10. Irbäck Knuthson "Using quantum annealing to design lattice proteins" PRR 2024
11. Micheletti Hauke Faccioli "Polymer physics by quantum computing" PRL 2021
12. Wong Chang "Fast quantum algorithm for protein structure prediction in hydrophobic-hydrophilic model" Grover
13. QDockBank quantum computing protein fragment dataset
14. Pamidimukkala "Protein structure prediction with high degrees of freedom in a gate-based quantum computer"
15. Moderna IBM mRNA secondary structure prediction utility-scale quantum computers

**arXiv API title searches:**
- "Optimized Wang-Landau sampling of lattice polymers"
- "Growth-based optimization algorithm for lattice heteropolymers"
- "Pruned-enriched Rosenbluth method" + Grassberger
- "Construction of model Hamiltonians for adiabatic quantum computation"
- "Sampling rare conformational transitions with a quantum computer"
- "Polymer physics by quantum computing"
- "Protein structure prediction with high degrees of freedom"

**Crossref / Europe PMC lookups:**
- Berger–Leighton, Crescenzi et al., Unger–Moult, Hart–Istrail, Lau–Dill.
- Grassberger PERM, Hsu et al. ×2, Thachuk–Shmygelska–Hoos, Wüst–Landau ×2, Backofen–Will, CPSP-tools.
- Desmet DEE, Xu tree decomposition.
- Barkoutsos CVaR, Szegedy, Somma et al., Montanaro ×2, Rønnow et al., Albash–Lidar, Layden et al.
- AlphaFold, Reiher et al., Goings et al., Lee et al., Blunt et al., Santagati et al.
- Mulligan et al. (bioRxiv), Marchand et al.

**Full-text extraction** (arXiv PDF → text): 2004.01118 (Outeiral NJP, full scaling section), 1204.5485, 1810.13411, 1811.00713, 1908.02163, 2101.10279, 2204.01821, 2205.06084, 2212.13511, 2506.07866, 2604.26861, 2312.00875, 2507.08955, 2507.19383, 2508.00837, 2510.06413, 2508.10660, 2606.21241, 2509.18263, 2005.12792, and the Wong–Chang IEEE TNB preprint.

**Corrections to the task brief** (all verified):
- Babbush et al. is **Advances in Chemical Physics vol. 155 (2014)**, arXiv:1211.3422, not *Sci Rep*.
- Outeiral et al. WIREs is dated 2021 (vol. 11, e1481); arXiv lists 2020.
- The Linn et al. resource analysis exists (PRR 6, 033112, 2024).
- "Agathangelou" is Agathangelou, Manawadu, Tavernelli 2025 (side-chain QAOA).
- The IBM/Cleveland Clinic demonstrations are Doga et al. 2024, Li et al. 2025, Linn et al. 2025 and the QDockBank line.
- The Kipu/IonQ demonstrations are Romero et al. 2025 (12 aa) and Gomez Cadavid et al. 2026 (14–16 aa, 64-qubit system).

---

## 2. Verified papers (per-paper fields)

**Abbreviations.**
- **Rep.:** representation.
- **Max:** largest instance.
- **HW/Sim:** hardware or simulator.
- **Prim.:** the quantum primitive actually used.
- **Baseline:** the classical comparator and its strength.
- **Scaling:** whether a scaling claim is made.
- **FM:** reduces to the S29–S33 failure modes:
  - FM1: diagonal cost with argmin/tail readout.
  - FM2: enumerable space.
  - FM3: weak or absent classical twin.
  - FM4: the cost does not track structural accuracy (the analogue of "condition C").
- **Label:** claim label per LIT_RULES.

### 2A. Quantum lattice / coarse-grained folding (primary)

**D1. Perdomo, Truncik, Tubert-Brohman, Rose, Aspuru-Guzik (2008).** "Construction of model Hamiltonians for adiabatic quantum computation and its application to finding low-energy conformations of lattice protein models." *Phys. Rev. A* 78, 012320.
- DOI 10.1103/PhysRevA.78.012320. arXiv:0801.3625. Verified: arXiv API + Crossref.
- **Content:** the HP model mapped to an adiabatic QC Hamiltonian, with reduction to 2-body terms. Theory only.
- **Label:** none (encoding paper; no speedup claim).
- **FM:** FM1 (diagonal cost); an ancestor of everything that follows.

**D2. Perdomo-Ortiz, Dickson, Drew-Brook, Rose, Aspuru-Guzik (2012).** "Finding low-energy conformations of lattice protein models by quantum annealing." *Sci. Rep.* 2, 571.
- DOI 10.1038/srep00571. arXiv:1204.5485. Verified: arXiv abs + Crossref + full text.
- **Rep.:** 2D lattice, Miyazawa–Jernigan (MJ). Sequence PSVKMA (6 aa), plus a tetrapeptide HP instance.
- **Max:** 6 aa. 5–81 physical qubits on a D-Wave device with 115 working qubits.
- **HW:** D-Wave (superconducting QA). An 8-qubit instance was simulated with Bloch–Redfield.
- **Prim.:** analog QA of a diagonal Ising H, with divide-and-conquer "schemes" that partition the problem classically.
- **Baseline:** exact enumeration only. Quote: "the six-amino acid problem has only 40 possible configurations" (main text). Also: "Although the cases presented here can be solved in a classical computer…" (abstract).
- **Result:** "in the 81 qubit experiment, only 13 out of 10,000 measurements yielded the desired solution" (main text).
- **Scaling:** none. The mapping used is stated to have "exponential scaling with problem size, is not intended for large instances."
- **FM:** FM1, FM2 (40 conformations), FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE (none claimed).

**D3. Babbush, Perdomo-Ortiz, O'Gorman, Macready, Aspuru-Guzik (2014).** "Construction of Energy Functions for Lattice Heteropolymer Models: A Case Study in Constraint Satisfaction Programming and Adiabatic Quantum Optimization." *Adv. Chem. Phys.* 155.
- arXiv:1211.3422. Verified: arXiv abs.
- **Content:** a review and encodings paper. It covers turn, diamond and coordinate encodings as CSP / MaxSAT / PBO, and locality reduction for annealers.
- Notably, it explicitly advocates leveraging "powerful solvers from the computer science community which studies constraint programming" (abstract). The classical CP route (CPSP, D46) is the natural competitor.
- **Label:** none (encoding / theory).
- **FM:** FM1.

**D4. Fingerhuth, Babej, Ing (2018).** "A quantum alternating operator ansatz with hard and soft constraints for lattice protein folding." arXiv:1810.13411 (preprint).
- Verified: arXiv abs + full text.
- **Rep.:** one-hot turn encoding. 6N−17 qubits on a cubic lattice, 4N−10 on a planar lattice.
- **Max:** PSVK (4 aa, planar) in the noiseless Rigetti QVM simulator, p ≤ 2. A hardware run used 4-qubit subproblems on a Rigetti QPU.
- **Prim.:** QAOA with constraint-preserving XY/XZ mixers.
- **Result:** best ground-state probability 0.477 (median 0.263) with XZ-simple at p = 2, vs X-mixer 0.148 (median 0.048).
- **Baseline:** none classical; only other mixers.
- **Scaling:** none.
- **FM:** FM1, FM2, FM3.
- **Label:** SIMULATOR RESULT (small HW run).

**D5. Babej, Ing, Fingerhuth (2018).** "Coarse-grained lattice protein folding on a quantum annealer." arXiv:1811.00713 (preprint).
- Verified: arXiv API + full text.
- **Rep.:** turn-ancilla / turn-circuit / coordinate encodings. Turn-circuit needs 3N−8 qubits but has many-body terms.
- **Max:** Chignolin (10 aa, planar) and the Trp-cage fragment DAYAQWLK (8 aa, cubic) on D-Wave 2000Q.
- **Prim.:** QA of subproblems. For Chignolin, the Hamiltonian was "split … into 1024 subproblems", and "only one out of the 2^10 subproblems actually included the correct solution" (§ results). The **classical enumeration of turn prefixes does the global search**.
- **Baseline:** "the correct lattice fold was obtained with a classical Monte-Carlo" (verification).
- **Scaling:** none (quasilinear circuit-complexity reduction only).
- **FM:** FM1, FM2, FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**D6. Robert, Barkoutsos, Woerner, Tavernelli (2021).** "Resource-efficient quantum algorithm for protein folding." *npj Quantum Inf.* 7, 38.
- DOI 10.1038/s41534-021-00368-4. arXiv:1908.02163. Verified: arXiv abs + full text (Nature page 303-redirected).
- **Rep.:** tetrahedral lattice coarse-grained model with optional side-chain beads. l-NN MJ contacts via penalty-coupled "interaction qubits". Qubits O(N²); Hamiltonian terms O(N⁴); locality ≤ 3 for 1-NN.
- **Max:** Angiotensin (10 aa), 22 qubits, on a *noisy simulator*. APRLRFY (7 aa), 9 qubits, on IBM Q Poughkeepsie (20 q).
- **Prim.:** **CVaR-VQE** (Barkoutsos 2020, D55) + differential-evolution/genetic optimiser. **Diagonal Hamiltonian.**
- **Result:** ground-state probability averaged over the population ">20% and with max P0 peaking up at 33%" (hardware).
- **Baseline:** none classical. The paper's "scaling" is **the number of Pauli terms**, not runtime. Quote: "We define the scaling of the algorithm as the number of terms (or Pauli strings)" (§Scaling).
- **Claims:** entanglement "may lead to quantum advantage" (Discussion); no evidence is offered.
- **FM:** **FM1 exactly.** This is the direct ancestor of the predecessor's CVaR-VQE: CVaR tail = prefix of the energy order (S30 T1). Also FM2 (2^9 hardware space) and FM3.
- **Label:** HARDWARE DEMONSTRATION; SIMULATOR RESULT; NO ADVANTAGE.

**D7. Outeiral, Morris, Shi, Strahm, Benjamin, Deane (2021).** "Investigating the potential for a limited quantum speedup on protein lattice problems." *New J. Phys.* 23, 103030.
- DOI 10.1088/1367-2630/ac29ff. arXiv:2004.01118. Verified: arXiv abs + Crossref + full text.

**Setup (§2).**
- 29,503 random MJ sequences with a unique global minimum (15,173 in 2D, 14,330 in 3D). Lengths: 2D 6–9 aa (4 lengths), 3D 6–8 aa (3 lengths).
- Turn encoding (Babbush), "10 (6 aa peptide in 2D) to 21 qubits (8 aa peptide in 3D), meaning Hilbert spaces of size 1,024 to 2,097,152."
- The dataset was **generated by brute-force enumeration** ("The states of these instances were enumerated by a brute force algorithm").
- **Prim.:** idealised closed-system QA. Exact Schrödinger integration: "idealised quantum annealer at zero temperature, in the absence of noise, and with perfect control over couplings". Minimum gaps by Krylov–Schur. TTS optimised by Bayesian optimisation over anneal time. Stoquastic and non-stoquastic catalysts. Tailored schedules.

**Scaling results (the crucial part).**
- **Gap (§3):** "the median gap remains approximately constant, while the worst case gap grows exponentially [smaller]" (Fig. 2 caption). "the worst cases decrease by five orders of magnitude between 6 and 9 amino acids" (§7).
  - A polynomial model was statistically selected for the gap, but the authors write: "This data does not allow us to conclude that the gap vanishes polynomially" and "we hypothesise that the protein lattice problem presents exponentially vanishing spectral gaps that will hinder a general polynomial-time solution by quantum annealing for large sizes" (§3).
- **Optimised QA TTS (§4):** "either the exponential model is selected over the polynomial, or there is not a significant difference … in 2D the polynomial model x^α (with α ≈ 0.65) and the exponential model e^{αx} (with α ≈ 0.15) cannot be separated. In 3D, an exponential model e^{αx} with α ≈ 0.45 is selected with high significance."
  - The Discussion (§7) instead states "approximately equal to e^{0.15L} for 2D examples and approximately e^{0.75L} for 3D examples". **This is an internal inconsistency (0.45 vs 0.75 for 3D). Neither number should be quoted without flagging it.**
  - Also: "Problems with gaps smaller than 10^-2 a.u. (and down to 10^-8 a.u.) do not take significantly longer than problems with a median gap".
  - Tailored schedules gave "10-100x speedups" (§7).
- **Classical comparator (§2.4, §6):** "an off-the-shelf classical simulated annealing subroutine, the gsl siman.h module of the GNU Scientific Library", on turn sequences, "analyse the results in term of Monte Carlo moves instead of times". Four SA parameters were Bayesian-optimised.
  - Finding: "the model fits to a square exponential e^{αx²} with a high level of significance".
  - The authors caveat: "The square exponential fit … could be an artifact of parameter optimisation".
- **Headline claim:** "we find some evidence of a potential limited quantum speedup for protein lattice folding problems of modest size" (§1). Also: "quantum annealing requires exponentially growing runtimes … it precludes an exponential speedup, since enumerating all possible conformations of a lattice model has the same asymptotic complexity" (§6).

**Critical assessment.**
1. The fits are over **3–4 consecutive lengths (6–9 aa)**. At these lengths the entire space (≤2.1 M states) is enumerated in well under a second. The paper itself enumerated all 29,503 instances by brute force.
2. The classical twin is **generic GSL SA with naive turn moves**. It is not a pull-move REMC (D43), PERM/nPERMis (D41–42), Wang–Landau (D44–45) or exact CP (D46–47). Those classical methods solve HP benchmarks of 48–136 residues.
3. The units differ: QA anneal time in a.u. (idealised) vs SA Monte Carlo moves. There is no common wall-clock basis.
4. The QA is error-free, closed-system and zero-temperature. By the authors' own framing this is "achievable in future devices … in the presence of error correction … or with fault-tolerant universal quantum computers employing Hamiltonian simulation" (§1).
5. The "worse-than-exponential" SA fit is almost certainly a small-size artefact: SA cannot be worse than brute force asymptotically.

- **FM:** FM2 (fully enumerable), FM3 (weak twin), FM1 (diagonal H, ground-state readout).
- **Label:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (claimed vs weak baseline, small N). **Not** an ASYMPTOTIC SPEEDUP.

**D8. Outeiral, Strahm, Shi, Morris, Benjamin, Deane (2021).** "The prospects of quantum computing in computational molecular biology." *WIREs Comput. Mol. Sci.* 11, e1481.
- DOI 10.1002/wcms.1481. arXiv:2005.12792. Verified: arXiv abs + Crossref + full text. **Review (orientation).**
- Quote: "it is currently believed that quantum computers cannot offer an exponential speedup to NP-complete and harder problems, although they can offer scaling advantages that have been known in the literature as 'limited quantum speedup'."
- It also notes that its own NJP result "may require adiabatic machines using error correction or quantum simulation in fault-tolerant universal machines" (§ protein structure prediction).
- It warns that the prospects "are susceptible to 'hype'" (abstract).
- **Label:** review; NO ADVANTAGE demonstrated.

**D9. Casares, Campos, Martin-Delgado (2022).** "QFold: quantum walks and deep learning to solve protein folding." *Quantum Sci. Technol.* 7, 025013.
- DOI 10.1088/2058-9565/ac4f2f. arXiv:2101.10279. Verified: arXiv abs + Crossref + full text.
- **Rep.:** backbone torsion angles (φ, ψ) discretised to 2^b values per angle. Initialisation from a Minifold (AlphaFold-like) distogram/torsion predictor.
- **Prim.:** Szegedy-walk **quantum Metropolis** under heuristic annealing schedules (after Lemieux et al.). Figure of merit: minimum TTS.
- **Max (simulated):** "Dipeptides with 3 to 5 rotation bits. Tripeptides with 2 rotation bits." Tetrapeptides with 2 bits only "for a few steps".
- **Hardware:** a minimal quantum-Metropolis step on IBMQ Casablanca (QV 32). The circuit had 176 gates after transpilation; the authors say it "does not make much sense to directly compare the values of the TTS figure of merit".
- **Baseline:** "classical Metropolis" with the same moves. There is no replica exchange or parallel tempering.
- **Claim:** "find a polynomial quantum advantage" (abstract). The fitted exponents between quantum and classical min-TTS are "e_m = 0.89 and e_r = 0.53 for minifold and random". The authors favour 0.89 as "more accurately represent[ing] the true asymptotic exponent".
- **Extrapolation:** they extrapolate to "a speedup factor of between ≈10^87 and 10^373". This is an extrapolation from spaces of at most ~2^10 states and **must not be cited as evidence**.
- The simulator implementation "has to iterate over all possible values of the angles and proposed movements". The energy table is therefore precomputed over an enumerable space (FM2).
- **FM:**
  - FM2.
  - FM3: plain Metropolis, not PT or SMC.
  - Not FM1: this is a sampling primitive, and the readout is the TTS to the minimum, i.e. an argmin.
- **Label:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (claimed, tiny N); ADVANTAGE DISPUTED (my assessment: an exponent of 0.89 over 2–3 sizes is statistically indistinguishable from 1).

**D10. Irbäck, Knuthson, Mohanty, Peterson (2022).** "Folding lattice proteins with quantum annealing." *Phys. Rev. Research* 4, 043013.
- DOI 10.1103/PhysRevResearch.4.043013. arXiv:2205.06084. Verified: arXiv abs + Crossref + full text.
- **Rep.:** 2D HP. Distributed (site-occupancy) QUBO encoding with N·L²/2 spins, quadratic with no ancillas.
- **Max:** hybrid solver, N = 64 (lowest known E = −42) and N = 48 (E = −23). **Pure QPU: N = 14 only.** Quote: "The performance of pure QA is less impressive with a drastic decrease in success rate as the system size is increased."
- **HW:** D-Wave Advantage, via **D-Wave's hybrid quantum-classical solver**. That solver is proprietary; the QPU's contribution to the result is not isolated.
- **Baseline:** classical SA, both QUBO SA and explicit-chain SA. The exact results for N ≤ 30 are known from exhaustive enumeration. Claim: "100% hit rate, thereby also outperforming classical simulated annealing" (abstract).
- The N = 48 and N = 64 benchmark energies were **found originally by classical methods** (the paper's refs [22, 23]).
- **FM:** FM1, FM3 (SA only; the classical solvers that established the reference energies are not run head-to-head).
- **Label:** HARDWARE DEMONSTRATION (hybrid); NO ADVANTAGE vs strong classical.

**D11. Irbäck, Knuthson, Mohanty, Peterson (2024).** "Using quantum annealing to design lattice proteins." *Phys. Rev. Research* 6, 013162.
- DOI 10.1103/PhysRevResearch.6.013162. arXiv:2402.09069. Verified: arXiv API.
- **Content:** HP sequence design, 30–64 aa, with the hybrid solver at a 100% success rate.
- "using only the QPU … confines us to sizes ≤20, due to exponentially decreasing success rates". Control-error simulations "semi-quantitatively reproduce the modest pure QPU results".
- **FM:** FM1, FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**D12. Irbäck, Knuthson, Mohanty (2025).** "Folding lattice proteins confined on minimal grids using a quantum-inspired encoding." *Phys. Rev. E* 112, 045302.
- DOI 10.1103/8n7p-7lh2. arXiv:2510.01890. Verified: arXiv API + Crossref.
- **Content:** N = 48 on a minimal grid. The problem "can be swiftly and consistently solved … using either classical simulated annealing or hybrid quantum-classical annealing".
- The **classical SA suffices**; the "quantum-inspired" encoding is the useful ingredient.
- **Label:** NO ADVANTAGE (internal dequantisation).

**D13. Gellersen, Irbäck, Knuthson, Prestel (2026).** "Penalty-free quantum optimization applied to lattice protein folding." arXiv:2606.02104 (preprint).
- Verified: arXiv API.
- **Content:** QAOA with an MIS mixer on a conflict graph. Simulated N = 4, 6. A local-search scheme reaches N = 14 "using local subgraphs with at most 26 qubits".
- **FM:** FM1, FM2 (each subproblem ≤ 2^26), FM3.
- **Label:** SIMULATOR RESULT.

**D14. Boulebnane, Lucas, Meyder, Adaszewski, Montanaro (2023).** "Peptide conformational sampling using the Quantum Approximate Optimization Algorithm." *npj Quantum Inf.* 9, 70.
- DOI 10.1038/s41534-023-00733-5. arXiv:2204.01821. Verified: arXiv abs + Crossref + full text.
- **Rep.:** (i) self-avoiding walks on Z², up to 28 qubits; (ii) an alanine peptide with heavy backbone atoms on a tetrahedral lattice and a Lennard-Jones potential, 20 qubits.
- **Prim.:** QAOA (statevector).
- **Result (abstract):** "deep quantum circuits are required to achieve accurate results, and the performance of QAOA can be matched by random sampling up to a small overhead. Overall, these results cast serious doubt on the ability of QAOA to address the protein folding problem in the near term, even in an extremely simplified setting."
- The SAW task is "trivially solvable using a classical algorithm".
- **Baseline:** uniform random sampling, which is weak, yet QAOA does not beat it meaningfully.
- **FM:** FM1, FM2. This is the literature's cleanest reproduction of the S33 finding that random prior sampling ≥ VQE (Q-C13).
- **Label:** SIMULATOR RESULT; NO ADVANTAGE.

**D15. Chandarana, Hegade, Montalban, Solano, Chen (2023).** "Digitized-Counterdiabatic Quantum Algorithm for Protein Folding." *Phys. Rev. Applied* 20, 014024.
- DOI 10.1103/PhysRevApplied.20.014024. arXiv:2212.13511. Verified: arXiv abs + Crossref + full text.
- **Rep.:** tetrahedral lattice (the Robert model).
- **Max:** 9 aa, 17 qubits.
- **HW:** Quantinuum trapped ions, Google and IBM superconducting devices.
- **Prim.:** a variational ansatz "inspired" by CD terms (O(N²) parameters, where N is the number of qubits); the success probability is the metric.
- **Baseline:** **QAOA and a hardware-efficient ansatz only.** No classical solver.
- Instances fail as size grows: "The observed trend of decreasing successful instances with inc[reasing size]".
- **FM:** FM1, FM2, FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**D16. Romero, Gomez Cadavid, Nikačević, Solano, Hegade, Lopez-Ruiz, Girotto, Yamada, Barkoutsos, Kaushik, Roetteler (2025).** "Protein folding with an all-to-all trapped-ion quantum computer." arXiv:2506.07866 (preprint; Kipu Quantum + IonQ).
- Verified: arXiv API + full text.
- **Rep.:** tetrahedral lattice with MJ 1-NN contacts (Robert model), dense turn encoding (2 qubits per turn), HUBO.
- **Max:** "up to 12 amino acids mapped onto 33 qubits" (instances with 22, 27 and 33 qubits).
- **HW:** IonQ Forte / Forte Enterprise.
- **Prim.:** BF-DCQO, a non-variational counterdiabatic evolution with bias fields updated iteratively from low-energy samples, plus classical **post-processing**.
- **Claim:** "representing the largest quantum hardware implementations of protein folding problems reported to date" (abstract).
- **Baseline:** "to obtain their exact ground states we use a brute force method" (§III). No classical heuristic twin is run on the protein instances.
- **FM:** FM1 (diagonal HUBO + best-sample readout), FM2 (2^33 is enumerable), FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE shown.

**D17. Gomez Cadavid, Nikačević, Chandarana, Romero, Solano, Hegade, Lopez-Ruiz, Girotto, Linn, Doga, Epifanovsky, Barkoutsos, Kaushik, Roetteler (2026).** "Protein folding on a 64 qubit trapped-ion hardware via counterdiabatic quantum optimization." arXiv:2604.26861 (preprint).
- Verified: arXiv API + full text.
- **Rep.:** tetrahedral lattice, 6 sequences of 14–16 aa, 46–61 qubits, up to 5-body terms.
- **HW:** a 64-qubit Barium development system.
- **Prim.:** BF-DCQO samples. A "consensus-based post-processing pipeline" transfers "quantum-learned contact information" onto feasible backbones.
- **Baseline:** the **random-seeded** pipeline (uniform random samples). The result: "the warm-started consensus pipeline reaches the classical reference energy in 4 out of 6 sequences. In the randomly-started case, it reaches the reference energy in 1 out of 6". At 61 qubits, "none of the two sequences reached the reference energy".
- The authors concede that "most raw samples still violate backbone constraints". They also concede that the seeds' advantage "diminishes as geometries are corrected and the contacts are re-optimized, hence overwritten".
- The "classical reference energy" is produced classically.
- **FM:** FM1, FM3 (random-seed twin only), and a strong **post-processing confound**.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE vs a real classical solver.

**D18. Linn, Brundin, García-Álvarez, Johansson (2024).** "Resource analysis of quantum algorithms for coarse-grained protein folding models." *Phys. Rev. Research* 6, 033112.
- DOI 10.1103/PhysRevResearch.6.033112. arXiv:2311.04186. Verified: arXiv API.
- **Content:** counts qubits, interactions and 2-qubit gates for lattice folding and fixed-backbone side-chain models under several encodings.
- Quote: "the number of qubits required falls within current technological capabilities. However, the limiting factor is the high number of interactions in the Hamiltonian, resulting in a quantum gate count unavailable today" (abstract).
- There is no runtime comparison with classical methods.
- **Label:** resource estimate; NO ADVANTAGE claimed.

**D19. Linn, Li, Holden, Saki, DiFilippo, Radivoyevitch, Blankenberg, García-Álvarez, Johansson (2025).** "Efficient Quantum Protein Structure Prediction with Problem-Agnostic Ansatzes." arXiv:2509.18263 (preprint; Chalmers + Cleveland Clinic).
- Verified: arXiv API + full text.
- **Rep.:** tetrahedral, BCC and FCC lattices with up to 2-NN interactions; the energy is evaluated **classically on samples**.
- **Max:** 26 aa, >40 qubits. Simulator and ibm_kingston.
- **Prim.:** a hardware-efficient ansatz trained on a classical cost of samples (sample-based VQE).
- **Baseline:** random sampling.
- Quote: "the exact ground state was not observed in any of the larger protein instances".
- **FM:** FM1 (classical cost of measured bitstrings: the circuit is a trainable sampler of a diagonal cost), FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**D20. Linn, Knuthson, Irbäck, Mohanty, García-Álvarez, Johansson (2026).** "Designing lattice proteins with variational quantum algorithms." *Phys. Rev. Applied* (2026).
- DOI 10.1103/kpf7-fx7t. arXiv:2508.02369. Verified: arXiv API + Crossref.
- **Content:** QAOA variants reach success ≥ 0.95 noiseless, but performance "drops drastically under noise". A hardware-efficient ansatz on hardware gives ≥ 0.2 success.
- **Label:** SIMULATOR RESULT / HARDWARE DEMONSTRATION; NO ADVANTAGE.

**D21. Doga, Raubenolt, Cumbo, Joshi, DiFilippo, Qin, Blankenberg, Shehab (2024).** "A Perspective on Protein Structure Prediction Using Quantum Computers." *J. Chem. Theory Comput.* 20, 3359–3378.
- DOI 10.1021/acs.jctc.4c00067. arXiv:2312.00875. Verified: arXiv API + full text. IBM + Cleveland Clinic.
- **Rep.:** the Robert tetrahedral model applied to the **7-aa Zika NS3 helicase P-loop (LHPGAGK)**, on IBM Cleveland (Eagle).
- **Result:** quantum best-RMSD model 1.781 Å. "The Hamiltonian term corresponding to the second best result was obtained as the optimal solution by both Gurobi and a brute force search, yielding an RMSD of 1.879 Å". AlphaFold2: 3.53 Å.
- **Critical point:** the structure with the best RMSD from hardware is **not the optimum of the encoded Hamiltonian**; brute force and Gurobi found the true optimum, which is worse in RMSD. So the RMSD "win" comes from noise and sample selection, not from optimisation. This is FM4 in miniature.
- The AF2 comparison is on a 7-residue loop excised from its protein context, which is not a fair test of AF2.
- The resource estimation is admittedly "simplified" ("rigorous resource estimation … is beyond the scope").
- **FM:** FM1, FM2 (brute force feasible), FM3, FM4.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE (the claimed accuracy advantage is spurious).

**D22. Li, Doga, Raubenolt, Mostame, … Shehab, Blankenberg (2025).** "Quantum Algorithm for Protein Structure Prediction Using the Face-Centered Cubic Lattice." arXiv:2507.08955 (preprint).
- Verified: arXiv API.
- **Content:** FCC lattice, PolyFit and VQE-with-constraints. Ground states for the **6-aa KLVFFA** were recovered on ibm_cleveland and ibm_kingston. The comparison is hardware vs hardware (Heron ≈ 2–3× better).
- **FM:** FM1, FM2, FM3.
- **Label:** HARDWARE DEMONSTRATION.

**D23. Pamidimukkala, Bopardikar, Dakshinamoorthy, Kannan, Dasgupta, Senapati (2024).** "Protein Structure Prediction with High Degrees of Freedom in a Gate-Based Quantum Computer." *J. Chem. Theory Comput.* 20, 10223–10234.
- DOI 10.1021/acs.jctc.4c00848. Verified: Crossref + Europe PMC abstract.
- **Content:** a turn-based HP encoding "utilizing up to 114 qubits (IBM hardware)". It "captures … the hydrophobic collapse".
- The per-length ground-truth and baseline details were not read (see §9).
- **FM:** FM1 (HP diagonal); FM3 is likely.
- **Label:** HARDWARE DEMONSTRATION.

**D24. Kannan, Pamidimukkala, Dakshinamoorthy, Bopardikar, Dasgupta, Senapati (2025).** "Capturing Protein Free Energy Landscape using Efficient Quantum Encoding." arXiv:2510.15316 (preprint).
- Verified: arXiv API.
- **Content:** FCC MJ Hamiltonian, VQE on IBM 133-qubit hardware, "compared against classical simulated annealing and molecular dynamics".
- **Label:** HARDWARE DEMONSTRATION (metadata and abstract only).

**D25. Zhang, Yang, Lu, Jiang, Cheng, Fang, Guan (2025).** "QDockBank: A Dataset for Ligand Docking on Protein Fragments Predicted on Utility-Level Quantum Computers." arXiv:2508.00837; SC '25, DOI 10.1145/3712285.3759799.
- Verified: arXiv API + full text.
- **Content:** 55 pocket fragments of **5–14 residues**, VQE on IBM, ">60 hours of quantum processor runtime", "total computational cost exceeding one million USD".
- **Claim:** "over 90% of entries surpassing AlphaFold2 and more than 80% surpassing AlphaFold3 in accuracy".
- **Critique:**
  - The comparison is between a lattice VQE on isolated fragments and AF2/AF3 run on the same short fragments out of context. AF is known to be weak on isolated short peptides.
  - I found **no same-Hamiltonian classical solve (exact / SA) reported** in the extracted text. So the lattice model plus selection, not the QPU, may explain every "win" (cf. D21).
- **FM:** FM1, FM2 (≤14 aa lattice), FM3, FM4 unexamined.
- **Label:** HARDWARE DEMONSTRATION; ADVANTAGE DISPUTED (my assessment).

**D26. Zhang, Yang, Chen, Lu, Saeidi, Volchenboum, Zhao, Chen, Jiang, Guan (2025).** "A Hybrid Quantum-AI Framework for Protein Structure Prediction on NISQ Devices." arXiv:2510.06413 (preprint).
- Verified: arXiv API + text.
- **Content:** VQE on a 127-qubit IBM device produces candidates. These are re-scored with NSP3 secondary-structure and dihedral statistical potentials ("energy fusion"). Mean RMSD 4.9 Å on 75 fragments, "improvements over AlphaFold3, ColabFold, and quantum-only".
- The neural potential does the discriminative work. No classical-candidate-generator twin is reported.
- **FM:** FM1, FM3.
- **Label:** HARDWARE DEMONSTRATION; NO ADVANTAGE isolatable.

**D27. Chen, Zhang, Chen, Xu, Guan, Ding (2026).** "QFoldAgent: An Autonomous Quantum Optimization Multi-Agent System for Protein Structure Prediction." arXiv:2607.22549 (preprint).
- Verified: arXiv API.
- **Content:** 5-residue tetrahedral folding; VQE under Qiskit Aer noise; LLM agents tune penalties. Median RMSD falls 3.64 → 3.20 Å on QDockBank fragments.
- A 5-residue lattice space is trivially enumerable.
- **FM:** FM1, FM2, FM3.
- **Label:** SIMULATOR RESULT.

**D28. Roget, Damour, Cadet, Wang (2026).** "Assessing Cost Hamiltonian Reliability in Quantum Protein Structure Prediction." arXiv:2606.21241 (preprint).
- Verified: arXiv API + full text. **Critical-assessment paper.**
- Quote (§5): "On average, the error of the structure with minimal cost is larger than the error of a structure taken at random. Thus, for short peptides, the minimum-cost conformation has, on average, a larger RMSD than a randomly selected feasible conformation."
- Also: "On average, this correlation [cost vs RMSD] is negative for small peptides." The correlation rises for ≥75-aa proteins when higher-order interaction shells are added (Monte-Carlo estimated).
- This is the **literature analogue of the predecessor's "condition C fails" (I-6)**. The exact optimum of the standard quantum-folding cost Hamiltonian is *anti-informative* at the peptide lengths used in every hardware demonstration.
- **Label:** NO ADVANTAGE (structural negative).

**D29. Scheiber, Heller, Giebel (2026).** "Exploring quantum annealing for coarse-grained protein folding." *Sci. Rep.* 16, 12035.
- DOI 10.1038/s41598-026-46916-w. arXiv:2508.10660. Verified: arXiv API + Crossref + text.
- **Content:** compares several encodings under SA and QA.
- Quote: "current quantum annealing hardware is not yet suited for tackling problems beyond a proof-of-concept size, primarily due to challenges in the embedding. Nonetheless, we observe a possible scaling advantage over our in-house simulated annealing implementation, which, however, is only noticeable when comparing performance on the embedded problems."
- In other words, the apparent advantage disappears when SA runs on the logical (unembedded) problem. Coupler resolution must grow for turn encodings.
- **Label:** ADVANTAGE DISPUTED (self-refuting); HARDWARE DEMONSTRATION.

**D30. Wong, Chang (2021).** "Quantum Speedup for Protein Structure Prediction." *IEEE Trans. NanoBioscience* (PMID 33690123).
- DOI 10.1109/TNB.2021.3065051. Verified: Europe PMC abstract + preprint full text.
- **Rep.:** 3D HP on a body-centred cubic lattice.
- **Prim.:** **Grover search** over all 2^{3(n−1)} conformations. The oracle coherently computes coordinates and energies.
- **Claim:** "quadratic speedup over its classical counterparts". Space O(n² log n) in the published abstract; the preprint abstract says O(n³). The time formula is an exponential O(2^{Θ(n)}) whose exponent did not render in either source.
- **Max:** simulated on the IBM simulator with 21 and 25 qubits. Quote: "two amino acids are the maximal size that can be simulated in three dimensions, while three is the maximal size for two dimensions".
- **Baseline:** implicitly brute-force enumeration.
- **FM:** FM2, FM3 (the comparator is exhaustive search, not CP/branch-and-bound).
- **Label:** QUERY-COMPLEXITY SPEEDUP (vs brute force); SIMULATOR RESULT.

**D31. Wong, Chang (2022).** "Fast quantum algorithm for protein structure prediction in hydrophobic-hydrophilic model." *J. Parallel Distrib. Comput.* 164, 178–190.
- DOI 10.1016/j.jpdc.2022.03.011. Verified: Crossref. Metadata-only (the publisher page returned 403); the search-engine summary says 2D square lattice, Grover, quadratic.
- **Label:** QUERY-COMPLEXITY SPEEDUP (claimed).

### 2B. Side-chain packing, design, conformer search (adjacent)

**D32. Agathangelou, Manawadu, Tavernelli (2025).** "Quantum Algorithm for Protein Side-Chain Optimisation: Comparing Quantum to Classical Methods." arXiv:2507.19383 (preprint).
- Verified: arXiv API + full text.
- **Content:** rotamer QUBO on a fixed backbone. QAOA with an XY mixer via statevector (≤28 qubits) or **MPS simulation (5–6 residues, up to 54 qubits)**.
- **Baseline:** SA. The cost is "defined as the number of calls to the CPU or QPU, respectively, required to find the ground state".
- **Result:** fitted SA cost ∝ e^{AM} with A ≈ 0.109. QAOA A ≈ 0.029 (SV) and ≈ 0.080 (MPS, 6 residues), from M ≥ 15–18 qubits. The extracted text is partly garbled around the error bars.
- **Critique:**
  1. A "call" is not comparable across CPU and QPU (a QAOA call is a full circuit with shots, and the parameters are optimised classically).
  2. The QAOA itself was run by classical MPS simulation at 54 qubits.
  3. The strongest classical rotamer solvers (DEE, D49; tree decomposition, D50; Rosetta packer) are not compared.
- **FM:** FM1, FM3.
- **Label:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (claimed, weak twin).

**D33. Mulligan, Melo, Merritt, Slocum, et al. (2019).** "Designing Peptides on a Quantum Computer." bioRxiv, DOI 10.1101/752485 (QPacker).
- Verified: Crossref. **Metadata-only.**
- Secondhand (Outeiral WIREs, D8): D-Wave 2000Q rotamer sampling "finding a scaling that seemed almost constant in comparison with classical simulated annealing".
- Not independently checked; do not cite as evidence.

**D34. Marchand, Noori, Roberts, Rosenberg, et al. (2019).** "A Variable Neighbourhood Descent Heuristic for Conformational Search Using a Quantum Annealer." *Sci. Rep.* 9, 13708.
- DOI 10.1038/s41598-019-47298-y. Verified: Crossref. Metadata-only.

**D35. Panizza, Hauke, Micheletti, Faccioli (2024).** "Protein Design by Integrating Machine Learning with Quantum Annealing and Quantum-inspired Optimization." arXiv:2407.07177 (preprint).
- Verified: arXiv API.
- Quote: "Strikingly, our quantum-inspired reformulation outperforms conventional sequence optimization even when adopted on classical machines."
- The encoding helps, not the quantum hardware. **Label:** NO ADVANTAGE (dequantised).

**D36. Meuser, Patsilinakos, Faccioli (2025).** "De Novo Design of Protein-Binding Peptides by Quantum Computing." *J. Chem. Theory Comput.* 21(19), 9993–10005.
- DOI 10.1021/acs.jctc.5c00768. arXiv:2503.05458. Verified: arXiv API.
- **Content:** D-Wave used to generate diverse binder candidates.
- **Label:** HARDWARE DEMONSTRATION (no classical-twin claim in the abstract).

### 2C. Quantum annealers and quantum states as *samplers* of polymer / conformational ensembles

**D37. Micheletti, Hauke, Faccioli (2021).** "Polymer Physics by Quantum Computing." *Phys. Rev. Lett.* 127, 080501.
- DOI 10.1103/PhysRevLett.127.080501. arXiv:2104.10102. Verified: arXiv API.
- **Content:** binary-tensor encoding; D-Wave samples lattice polymer mixtures across densities.
- **Label:** HARDWARE DEMONSTRATION (sampling). No classical speedup shown in the abstract.

**D38. Slongo, Hauke, Faccioli, Micheletti (2023).** "Quantum-inspired encoding enhances stochastic sampling of soft matter systems." *Sci. Adv.* 9, eadi0204.
- DOI 10.1126/sciadv.adi0204. Verified: Crossref (title).
- The title itself states the key point: the **encoding** improves *classical* stochastic sampling. This is a dequantisation of D37's benefit.
- **Label:** NO ADVANTAGE (classical counter-result).

**D39. Ghamari, Hauke, Covino, Faccioli (2022).** "Sampling rare conformational transitions with a quantum computer." *Sci. Rep.* 12, 16336.
- DOI 10.1038/s41598-022-20032-x. arXiv:2201.11781. Verified: arXiv API + Crossref.
- **Content:** ML-derived low-resolution path representation; D-Wave samples the transition-path ensemble; "the quantum computing step generates uncorrelated trajectories".
- No mixing-time comparison with classical path samplers is claimed.
- **Label:** HARDWARE DEMONSTRATION (sampling).

**D40. Rattacaso, Jaschke, Trovato, Siloi, Montangero (2026).** "Quantum algorithms for compact polymer thermodynamics." arXiv:2603.12334 (preprint).
- Verified: arXiv API.
- **Claim:** "a quadratic speedup in the estimation of thermodynamic properties of maximally compact polymers and heteropolymers". The Hamiltonian-cycle ensemble is encoded as a quantum sample (ground state of a local parent Hamiltonian), then processed by amplitude amplification/estimation.
- The **same paper** finds "an entanglement area law" and, "for fixed-width rectangular lattices, … a time-efficient and compact encoding of the full ensemble … via tensor contractions, without resorting to sampling". That is an efficient classical route for the tractable geometry.
- **Label:** THEORETICAL SPEEDUP (quadratic, estimation) + a classical tensor-network counterpart in the same work.
- This is **the most relevant sampling primitive for SP-1/AA-1**, but it covers compact lattice polymers, not learned off-lattice energies.

### 2D. Classical complexity and strong classical solvers (the counterarguments)

**D41. Grassberger (1997).** "Pruned-enriched Rosenbluth method: Simulations of θ polymers of chain length up to 1 000 000." *Phys. Rev. E* 56, 3682–3693.
- DOI 10.1103/PhysRevE.56.3682. Verified: Crossref.

**D42. Hsu, Mehra, Nadler, Grassberger (2003).**
- (a) "Growth algorithms for lattice heteropolymers at low temperatures." *J. Chem. Phys.* 118, 444. DOI 10.1063/1.1522710; arXiv cond-mat/0208042. Verified: arXiv abs + Crossref.
- (b) "Growth-based optimization algorithm for lattice heteropolymers." *Phys. Rev. E* 68, 021113. DOI 10.1103/PhysRevE.68.021113; arXiv cond-mat/0209366. Verified: arXiv API + Crossref.
- Quote (b): the improved PERM "outperform[s] not only the previous version of PERM, but also all other fully blind general purpose stochastic algorithms … In many cases it found new lowest energy states".
- Quote (a): it is "a fully blind general purpose algorithm giving correct Boltzmann-Gibbs weights". It supplies **thermodynamics**, not just minima.

**D43. Thachuk, Shmygelska, Hoos (2007).** "A replica exchange Monte Carlo algorithm for protein folding in the HP model." *BMC Bioinformatics* 8, 342.
- DOI 10.1186/1471-2105-8-342. Verified: Crossref + Europe PMC.
- Quote: "REMC utilizing the pull move neighbourhood significantly outperforms current state-of-the-art methods … on 2D and 3D lattices … it scales well with sequence length".

**D44. Wüst, Landau (2009).** "Versatile Approach to Access the Low Temperature Thermodynamics of Lattice Polymers and Proteins." *Phys. Rev. Lett.* 102, 178101.
- DOI 10.1103/PhysRevLett.102.178101. Verified: Crossref.

**D45. Wüst, Landau (2012).** "Optimized Wang-Landau sampling of lattice polymers: Ground state search and folding thermodynamics of HP model proteins." *J. Chem. Phys.* 137, 064903.
- DOI 10.1063/1.4742969. arXiv:1207.3974. Verified: arXiv API + Crossref.
- Quote: "all currently known putative ground states for the most difficult benchmark HP sequences could be found … we could also determine the entire energy density of states … for sequence lengths up to 500 residues."

**D46. Backofen, Will (2006).** "A Constraint-Based Approach to Fast and Exact Structure Prediction in Three-Dimensional Protein Models." *Constraints* 11, 5–30.
- DOI 10.1007/s10601-006-6848-8. Verified: Crossref. Metadata-only.

**D47. Mann, Will, Backofen (2008).** "CPSP-tools – Exact and complete algorithms for high-throughput 3D lattice protein studies." *BMC Bioinformatics* 9, 230.
- DOI 10.1186/1471-2105-9-230. Verified: Crossref + Europe PMC.
- Quote: "programs to solve exactly and completely … the prediction of (all) globally optimal and/or suboptimal structures … fast, non-heuristic techniques … cubic and face centered cubic (FCC) lattices."

**D48. Complexity results.**
- **Unger, Moult (1993).** "Finding the lowest free energy conformation of a protein is an NP-hard problem: proof and implications." *Bull. Math. Biol.* 55, 1183. DOI 10.1007/BF02460703. Verified: Europe PMC.
- **Berger, Leighton (1998).** "Protein folding in the hydrophobic-hydrophilic (HP) model is NP-complete." *J. Comput. Biol.* 5, 27–40. DOI 10.1089/cmb.1998.5.27. Verified: Crossref + Europe PMC.
  - Quote: "the protein folding problem under the HP model on the cubic lattice is shown to be NP-complete."
- **Crescenzi, Goldman, Papadimitriou, Piccolboni, Yannakakis (1998).** "On the complexity of protein folding." *J. Comput. Biol.* 5, 423–465. DOI 10.1089/cmb.1998.5.423. Verified: Crossref + Europe PMC.
  - Quote: "the protein folding problem in the two-dimensional H-P model is NP-complete."
- **Hart, Istrail (1996).** "Fast Protein Folding in the Hydrophobic–Hydrophilic Model within Three-Eighths of Optimal." *J. Comput. Biol.* 3, 53–96. DOI 10.1089/cmb.1996.3.53. Verified: Crossref. Metadata-only. A polynomial-time constant-factor approximation, from the title.
- **Lau, Dill (1989).** "A lattice statistical mechanics model of the conformational and sequence spaces of proteins." *Macromolecules* 22, 3986–3997. DOI 10.1021/ma00200a030. Verified: Crossref. The HP model origin.

**D49. Desmet, De Maeyer, Hazes, Lasters (1992).** "The dead-end elimination theorem and its use in protein side-chain positioning." *Nature* 356, 539–542.
- DOI 10.1038/356539a0. Verified: Crossref.

**D50. Xu (2005).** "Rapid Protein Side-Chain Packing via Tree Decomposition." RECOMB, *LNCS*, 423–439.
- DOI 10.1007/11415770_32. Verified: Crossref. Metadata-only.

**D51. Jumper et al. (2021).** "Highly accurate protein structure prediction with AlphaFold." *Nature* 596, 583–589.
- DOI 10.1038/s41586-021-03819-2. Verified: Crossref. This is the realistic-representation classical frontier.

**D52. Fang, He, Gong, Liang (2025).** "A Novel P-bit-based Probabilistic Computing Approach for Solving the 3-D Protein Folding Problem." arXiv:2502.20050.
- Verified: arXiv API.
- **Content:** a *classical* probabilistic Ising machine finds the 3D HP ground state for 36 aa. Classical Ising hardware already exceeds every pure-QPU folding size.

### 2E. Primitive / methodology references (for §3)

**D53. Szegedy (2004).** "Quantum Speed-Up of Markov Chain Based Algorithms." FOCS 2004, 32–41.
- DOI 10.1109/FOCS.2004.53. Verified: Crossref.

**D54. Somma, Boixo, Barnum, Knill (2008).** "Quantum Simulations of Classical Annealing Processes." *Phys. Rev. Lett.* 101, 130504.
- DOI 10.1103/PhysRevLett.101.130504. Verified: Crossref.

**D55. Barkoutsos, Nannicini, Robert, Tavernelli, Woerner (2020).** "Improving Variational Quantum Optimization using CVaR." *Quantum* 4, 256.
- DOI 10.22331/q-2020-04-20-256. Verified: Crossref. The CVaR objective used by Robert et al. and the predecessor.

**D56. Montanaro (2015).** "Quantum speedup of Monte Carlo methods." *Proc. R. Soc. A* 471, 20150301.
- DOI 10.1098/rspa.2015.0301. Verified: Crossref.

**D57. Montanaro (2015/2018).** "Quantum walk speedup of backtracking algorithms." arXiv:1509.02374; *Theory of Computing* 14 (2018), DOI 10.4086/toc.2018.v014a015. Verified: arXiv API + Crossref.
- Quote: "a bounded-error quantum algorithm which completes the same task using O(sqrt(T) n^(3/2) log n) tests".

**D58. Rønnow, Wang, Job, Boixo, et al. (2014).** "Defining and detecting quantum speedup." *Science* 345, 420–424.
- DOI 10.1126/science.1252319. Verified: Crossref. The "limited quantum speedup" definition used by Outeiral.

**D59. Albash, Lidar (2018).** "Demonstration of a Scaling Advantage for a Quantum Annealer over Simulated Annealing." *Phys. Rev. X* 8, 031016.
- DOI 10.1103/PhysRevX.8.031016. Verified: Crossref. Its SA-only comparator class is the one Outeiral cites.

**D60. Layden, Mazzola, Mishmash, Motta, et al. (2023).** "Quantum-enhanced Markov chain Monte Carlo." *Nature* 619, 282–287.
- DOI 10.1038/s41586-023-06095-4. Verified: Crossref. A sampling primitive (quantum proposal moves); not yet applied to proteins in anything I found.

### 2F. Reviews and boundary context (orientation only)

**D61. Cordier, Sawaya, Guerreschi, McWeeney (2022).** "Biology and medicine in the landscape of quantum advantages." *J. R. Soc. Interface* 19, 20220541.
- DOI 10.1098/rsif.2022.0541. arXiv:2112.00760. Verified: arXiv API. Review.

**D62. Blunt, Camps, Crawford, Izsák, et al. (2022).** "Perspective on the Current State-of-the-Art of Quantum Computing for Drug Discovery Applications." *J. Chem. Theory Comput.* 18, 7001–7023.
- DOI 10.1021/acs.jctc.2c00574. Verified: Crossref. Review.

**D63. Santagati, Aspuru-Guzik, Babbush, Degroote, et al. (2024).** "Drug design on quantum computers." *Nat. Phys.* 20, 549–557.
- DOI 10.1038/s41567-024-02411-5. Verified: Crossref. Review.

**D64. Reiher, Wiebe, Svore, Wecker, Troyer (2017).** "Elucidating reaction mechanisms on quantum computers." *PNAS* 114, 7555–7560.
- DOI 10.1073/pnas.1619152114. Verified: Crossref. Boundary: FeMoco electronic structure.

**D65. Goings, White, Lee, Tautermann, et al. (2022).** "Reliably assessing the electronic structure of cytochrome P450 on today's classical computers and tomorrow's quantum computers." *PNAS* 119, e2203533119.
- DOI 10.1073/pnas.2203533119. Verified: Crossref. Boundary.

**D66. Lee, Lee, Zhai, Tong, et al. (2023).** "Evaluating the evidence for exponential quantum advantage in ground-state quantum chemistry." *Nat. Commun.* 14, 1952.
- DOI 10.1038/s41467-023-37587-6. Verified: Crossref. Boundary counterargument.

**D67. Alevras, Metkar, Yamamoto, … Galda (2024).** "mRNA secondary structure prediction using utility-scale quantum computers." arXiv:2405.20328 (IEEE QCE 2024). Verified: arXiv API. Boundary (RNA).
- **Content:** CVaR-VQE, ≤60 nt, 10–80 qubits; results "match the results of the classical solver CPLEX".
- FM1 + FM3 (the quantum run reproduces the classical optimum).

**D68. Kumar, Alevras, Metkar, … Galda (2025).** "Towards secondary structure prediction of longer mRNA sequences using a quantum-centric optimization scheme." arXiv:2505.05782. Verified: arXiv API. Boundary.
- **Content:** CVaR + local search and IQP sampling, up to 156 qubits.

**D69. Liu, Li, Wang, Liu (2024).** "Toward end-to-end quantum simulation for protein dynamics." arXiv:2411.03972. Verified: arXiv API.
- **Content:** Hamiltonian simulation of normal-mode (GNM) protein models with read-in and read-out. A dynamics or normal-mode, not structure-prediction, primitive. It is classically linear-algebraic at moderate sizes.

**Count: 69 numbered entries (≈77 distinct verified works, since D42, D48 and a few others group several).** Metadata-only entries (no content claims used as evidence): D31, D33, D34, D46, D50, and Hart–Istrail in D48.

---

## 3. Primitive analyses (16 questions each)

### P-A. Quantum annealing / adiabatic / (bias-field) digitized-counterdiabatic evolution on lattice-folding Ising/HUBO Hamiltonians
Papers: D2, D5, D7, D10–D12, D15–D17, D29.

1. **Operation:** prepares low-energy states of a diagonal classical H_protein (HP or MJ contacts plus self-avoidance penalties), by slow (QA), counterdiabatically compressed (DCQO) or iteratively biased (BF-DCQO) evolution from a transverse-field start. It outputs bitstring samples.
2. **Replaces:** heuristic global minimisation of a lattice energy (SA, MC, chain growth, CP).
3. **Why hard classically:** it is NP-complete in the worst case: 2D HP (D48 Crescenzi), 3D cubic HP (D48 Berger–Leighton), and NP-hard generally (Unger–Moult). But **the instances used (≤16 aa hardware, ≤64 aa hybrid) are practically easy** for PERM, REMC, Wang–Landau and CPSP (D41–D47).
4. **Exact speedup:** **none proven.** Outeiral (D7) fits idealised-QA TTS ≈ e^{0.15L} (2D) and e^{0.45L} or e^{0.75L} (3D; the paper is internally inconsistent) over L = 6–9. The SA fit is e^{αL²}. The authors themselves hypothesise exponentially closing gaps at larger L. In general only a limited (constant-rate) speedup is conceivable (D8, D58).
5. **Resource type:** time-to-solution. Units are mismatched in D7 (anneal a.u. vs SA moves).
6. **Assumptions:** D7 assumes zero temperature, no noise, perfect control and closed-system dynamics. Real hardware adds analog control error: D11 reproduces the poor QPU success via control-error simulation. Minor embedding is also needed (D29).
7. **Oracle:** none. H is programmed directly, but k-local terms need locality reduction (ancillas) and embedding.
8. **Oracle/H construction cost:**
   - O(N⁴) Pauli terms and O(N²) qubits (D6).
   - N·L²/2 spins for the grid encoding (D10).
   - Coupler resolution Jmax/Jmin grows for turn encodings (D29).
   - D29: embedding overhead makes the apparent scaling advantage vanish on the logical problem.
9. **State prep:** trivial (|+⟩^n).
10. **Readout:** repeated sampling. TTS = t·ln(0.01)/ln(1−p). p = 13/10⁴ at 81 qubits (D2). Pure-QPU success decays exponentially: ≤14 aa folding (D10), ≤20 design (D11).
11. **Classical post-processing:** often dominant.
    - Classical subproblem partition (D2, D5: 1024 subproblems, only one containing the answer).
    - Proprietary hybrid solver (D10–D11).
    - Feasibility repair plus greedy descent that "overwrite[s]" the quantum signal (D17).
    - Brute-force ground truth (D16).
12. **Strongest classical:**
    - Exact: CPSP constraint programming (D46–D47) for 3D cubic/FCC HP.
    - Heuristic: nPERMis (D42), pull-move REMC (D43), optimized Wang–Landau (D45).
    - Also classical Ising machines (D52: 36-aa 3D HP).
13. **Does the advantage survive?** It was **never tested against any of these.** Comparators were gsl SA (D7), in-house SA (D29, where the advantage exists only on the embedded problem), QUBO SA (D10), or random seeds (D17).
14. **Fault tolerance:** the only positive scaling evidence (D7) is for error-free closed-system QA. D8 concedes that this "may require adiabatic machines using error correction or quantum simulation in fault-tolerant universal machines".
15. **Requirements:**
    - Qubits are "within current capabilities", but the gate count is "unavailable today" (D18).
    - D17: 61 qubits and ~1,000 entangling gates at 16 aa, and it fails there.
    - No logical-qubit or T-count estimate exists anywhere in this literature.
16. **Protein mapping:** only to coarse lattice models. On those models the exact optimum is **structurally anti-informative for short peptides** (D28), and its best hardware "wins" are noise-selected non-optima (D21).

### P-B. Variational optimisation (VQE, CVaR-VQE, QAOA, constraint mixers, HEA, sample-based VQE) of lattice-folding costs
Papers: D4, D6, D13–D15, D19–D22, D25–D27, D32; boundary D67–D68.

1. **Operation:** a parameterised circuit is trained to concentrate probability on low-energy bitstrings of a **diagonal** cost; the best sample or CVaR tail is read out.
2. **Replaces:** heuristic minimisation.
3. **Hardness:** as P-A.
4. **Speedup:** none claimed rigorously. D6 claims "may lead to quantum advantage through the use of entanglement" with no evidence. D32 fits exponents with "CPU calls vs QPU calls".
5. **Resource type:** —.
6. **Assumptions:** trainability. Barren plateaus are acknowledged (D16, D32). Noise degrades QAOA "drastically" (D20).
7. **Oracle:** none (diagonal H) or a classical cost evaluated on samples (D19).
8. **H cost:** O(N⁴) terms (D6). Many-body terms (D16/D17 up to 5-body).
9. **State prep:** trivial.
10. **Readout:** sampling. The **argmin or CVaR tail = prefix of the energy order**. This is R1/R2 of the predecessor, and here it is literally the same objective (D55 → D6 → predecessor).
11. **Postprocessing:** classical optimiser loop, penalty tuning (D27 uses LLM agents), energy fusion with neural potentials (D26).
12. **Strongest classical:** as P-A. For the tiny instances used, exhaustive enumeration (D16, D21 used brute force).
13. **Survives?** **No.**
    - D14: "the performance of QAOA can be matched by random sampling up to a small overhead".
    - D19: the ground state is never observed at larger sizes.
    - D21: the best-RMSD sample is not the optimum.
    - D67: the quantum run matches CPLEX (reproduces rather than beats it).
14. **Fault tolerance:** N/A (NISQ by design). No scaling path is argued.
15. **Requirements:** 9–114 qubits on hardware (D6, D23). The simulated QAOA at 54 qubits was itself run by classical MPS (D32).
16. **Mapping:** lattice or coarse-grained folding, rotamer packing and design. This is the exact class the predecessor exhausted (DE-1, DE-2, DE-8).

### P-C. Grover / amplitude amplification over conformations (and quantum backtracking)
Papers: D30, D31; D57 for the backtracking variant.

1. **Operation:** amplitude amplification over all 2^{3(n−1)} BCC conformations (D30), with a reversible coherent coordinate and energy oracle and a threshold comparison ("Grover's optimization").
2. **Replaces:** exhaustive enumeration.
3. **Hardness:** the space is exponential. But exhaustive enumeration is **not** the classical frontier: CP (D47), PERM (D42) and REMC (D43) prune massively.
4. **Speedup:** quadratic in the number of conformations, i.e. √(2^{3(n−1)}) oracle calls vs 2^{3(n−1)} (D30 abstract: "quadratic speedup over its classical counterparts").
5. **Resource type:** query complexity (oracle calls). It is **not** runtime versus the best classical algorithm.
6. **Assumptions:** fault-tolerant execution of a long coherent oracle. Circuits of 1,624–3,328 gates were needed already at 2 aa (3D).
7. **Oracle:** yes: coherent self-avoidance plus contact-energy evaluation plus a comparator.
8. **Oracle cost:** poly(n) reversible arithmetic per call. Space O(n³) (preprint) or O(n² log n) (published abstract). There is no T-count.
9. **State prep:** uniform superposition over turn strings (cheap). Infeasible walks are included.
10. **Readout:** a single measurement per run; repeat for thresholds (Dürr–Høyer style).
11. **Postprocessing:** trivial.
12. **Strongest classical:** exact CP branch-and-bound (CPSP) and approximation (Hart–Istrail 3/8, D48). The fair quantum analogue is **Montanaro backtracking** (D57): O(√T·n^{3/2} log n) tests, where T is the size of the classical *search tree*.
13. **Survives?** Against brute force, yes (trivially). Against CPSP or PERM, **unknown and implausible**:
    - No one has measured the classical CP tree size T(N) for lattice proteins.
    - No one has built a quantum-backtracking resource estimate.
    - Pruned trees are far smaller than 2^{3(n−1)}.
14. **Fault tolerance:** yes, required.
15. **Requirements:** 21–25 qubits for 2 aa (3D) (D30). No logical-qubit estimate.
16. **Mapping:** exact lattice optimisation. This is a 2^n_res-type discrete choice, analogous to C-4/QA-4 in the Opportunity Map, which is inherited as discrimination-limited.

### P-D. Quantum walks / quantum Metropolis / quantum Gibbs sampling / QA-as-sampler for conformational ensembles
Papers: D9 (QFold), D37, D39, D40; theory D53, D54, D56, D60; counter D38, D42, D45.

1. **Operation:** Szegedy-walk quantization of a Metropolis chain (D9, D53). This either speeds up annealing to low-energy states (D54) or prepares "quantum samples" (coherent encodings of a Boltzmann or ensemble distribution) for amplitude estimation of thermodynamic averages (D40, D56). QA used as a heuristic ensemble sampler (D37, D39) is a different, unproven primitive.
2. **Replaces:** classical MCMC, simulated annealing, and ensemble estimation of free energies or populations (PT, Wang–Landau, PERM with Boltzmann weights).
3. **Hardness:** the classical mixing or tunnelling time can scale as 1/δ with a spectral gap δ that closes exponentially at low T on rugged landscapes. **Whether this happens for realistic or learned protein energies at biologically relevant T has not been measured in this literature.**
4. **Speedup:**
   - Quadratic in the spectral gap, O(1/√δ) vs O(1/δ), for Szegedy-type or QSA annealing (D53, D54). Stated here from the known literature; the domain papers cite it.
   - Quadratic in precision, O(1/ε) vs O(1/ε²), for mean estimation (D56).
   - D40 claims "a quadratic speedup in the estimation of thermodynamic properties".
   - QFold's *empirical* exponents are 0.89 and 0.53 (quantum min-TTS vs classical min-TTS). The 10^87–10^373 speedups are an unjustified extrapolation.
5. **Resource type:** time or query in δ (mixing); sample complexity in ε (estimation).
6. **Assumptions:**
   - A reversible, detailed-balance chain.
   - A coherent implementation of the transition operator (energy differences computed in superposition).
   - For the quadratic mixing speedup one needs either a slowly varying annealing path (D54) or a warm start.
   - Out-of-equilibrium heuristic schedules (QFold) carry no guarantee.
7. **Oracle:** the Szegedy walk operator W(P) requires coherent evaluation of the energy change for each proposal. For learned energies, that means **coherent evaluation of a neural-network or pair-distance energy**.
8. **Oracle cost:** reversible arithmetic for torsion→coordinate transforms and pairwise energies, O(N²) pair terms per move for a pair potential. QFold avoided this by precomputing a table over *all* discretised angle values, which is exponential and non-scalable. There is **no T-count or logical-qubit estimate for any protein-energy walk operator** in the literature found.
9. **State prep:** the start state (for example a Minifold-initialised torsion distribution in D9). In D40, the ground state of a parent Hamiltonian is prepared by adiabatic methods.
10. **Readout:** samples, or amplitude estimation of an observable. The latter is the only readout that exploits the coherent sample non-classically.
11. **Postprocessing:** reweighting and averaging.
12. **Strongest classical:**
    - Parallel tempering / replica exchange (D43).
    - PERM with correct Boltzmann weights (D42).
    - Wang–Landau with pull, bond-rebridging and pivot moves (D45: full density of states, up to 500 residues).
    - Tensor-network contraction for narrow lattices (D40).
    - Quantum-inspired encodings run classically (D38).
13. **Survives?**
    - **Not demonstrated.** QFold compares with plain Metropolis on ≤ tripeptides.
    - D40 has a classical tensor-network route in the same paper for the tractable geometry.
    - D38 shows the encoding benefit transfers to classical samplers.
    - A quadratic-in-gap speedup survives only if the *best* classical sampler (PT or WL with smart moves) still has a small gap. That is exactly the unmeasured quantity (Map C-1, OP-01).
14. **Fault tolerance:** yes, for any rigorous version (a coherent walk operator plus phase estimation or amplitude estimation). QFold's hardware run (176 gates, one step) is a demonstration only.
15. **Requirements:** no literature estimate. QFold's ideal simulation was limited by RAM at dipeptides with ≤5 bits per angle.
16. **Mapping:** the **most natural mapping in this whole domain** to the predecessor's one positive signal: Boltzmann-weighted averaging beating argmin (S33 Q-C18). It maps to SP-1/AA-1 in the Opportunity Map. It is still conditional on classical slow mixing, which no paper has shown for protein-like energies.

### P-E. QA/QAOA for side-chain packing and lattice sequence design (adjacent)
Papers: D11, D20, D32–D36; classical D49, D50.

1. **Operation:** minimise a pairwise rotamer or sequence QUBO on a fixed backbone or structure.
2. **Replaces:** DEE, A*, tree decomposition, Rosetta Monte Carlo packer; sequence optimisation.
3. **Hardness:** NP-hard in general, but protein interaction graphs have small treewidth (D50), and DEE prunes most rotamers (D49).
4. **Speedup:** none proven. D32 fits e^{0.029M} to e^{0.080M} vs SA e^{0.109M}, at ≤6 residues and ≤54 qubits (MPS simulated), in "calls".
5. **Resource type:** —.
6. **Assumptions:** that a CPU call and a QPU call have comparable cost (untenable).
7. **Oracle:** none.
8. **H cost:** O((N·n_rot)²) couplings.
9. **State prep:** trivial.
10. **Readout:** argmin (FM1).
11. **Postprocessing:** classical.
12. **Strongest classical:** DEE (D49), tree decomposition (D50), and ILP. Also classical runs of quantum-inspired encodings (D35: "outperforms conventional sequence optimization even when adopted on classical machines").
13. **Survives?** No evidence.
14. **Fault tolerance:** —.
15. **Requirements:** D18 counts gates for fixed-backbone side-chain models; the gate count is prohibitive today.
16. **Mapping:** side-chain packing is a real protein subproblem, but it is classically well solved and not the S29–S33 bottleneck (per-residue discrete choices were discrimination-limited, C-4).

### P-F (boundary). Phase estimation for electronic structure of biomolecular active sites
Papers: D64–D66.
- It operates on a different problem (energies of strongly correlated clusters such as FeMoco and P450), not backbone structure.
- D66 argues that the evidence for *exponential* advantage in generic ground-state chemistry is not established.
- There is no mapping to structure accuracy at 9–60 aa (Map AA-3, DE-7).
- It is recorded so that it is not rediscovered.

---

## 4. Strongest classical counterarguments

1. **Every quantum-folding instance ever run is classically trivial.**
   - Hardware maxima: 6 aa with 40 conformations (D2); 10 aa after classical splitting (D5); 7 aa at 9 qubits (D6); 9 aa at 17 qubits (D15); 12 aa at 33 qubits (D16); 14–16 aa at 46–61 qubits (D17, reference energy classical); pure-QPU HP N = 14 (D10) and design N ≤ 20 (D11).
   - All of these are within exhaustive enumeration or instant CP. Several papers generated ground truth *by brute force* (D7, D16, D21).
2. **Classical lattice solvers reached far beyond these sizes decades ago, and give thermodynamics as well.**
   - PERM variants "outperform … all other fully blind general purpose stochastic algorithms" and give Boltzmann weights (D42).
   - REMC with pull moves "significantly outperforms" prior methods on 2D and 3D and "scales well with sequence length" (D43).
   - Optimized Wang–Landau finds "all currently known putative ground states for the most difficult benchmark HP sequences" and whole densities of states up to 500 residues (D45).
   - CPSP solves 3D cubic and FCC HP "exactly and completely" (D47).
   - Classical p-bit Ising machines fold 36-aa 3D HP (D52).
   - **Not one quantum paper benchmarks against PERM, REMC, WL or CPSP.**
3. **Quantum-inspired encodings dequantise.** The encodings developed for annealers help classical SA or MC just as much, or more (D12, D35, D38). Scheiber et al. find that the QA scaling advantage exists only against SA on the *embedded* problem (D29).
4. **The lattice cost is the wrong objective.** For short peptides the global minimum of the standard contact-energy cost Hamiltonian has, on average, **worse RMSD than a random feasible conformation** (D28). D21's hardware "win over AlphaFold2" is a non-optimal noisy sample that beat the true optimum (1.781 vs 1.879 Å). Optimising this cost better, whether quantum or classical, does not improve structure.
5. **The realistic-representation frontier is classical deep learning (D51).** Every "beats AF2/AF3" claim (D21, D25, D26) is on 5–14-residue fragments excised from context. That is AF's known weak regime, and no same-Hamiltonian classical twin is reported.
6. **Worst-case complexity does not give a quantum opening.** Lattice folding is NP-complete (D48). For NP-complete problems the generic expectation is at most a Grover-type quadratic (query) or "limited" speedup (D8), and it must be measured against pruned classical search (D57's T, not 2^n).

---

## 5. Scaling statements (explicit, with ranges; nothing inferred from small numerics)

| Source | Statement (verbatim or near-verbatim) | Variable / range | Status |
|---|---|---|---|
| D48 Berger–Leighton | "the protein folding problem under the HP model on the cubic lattice is shown to be NP-complete" | N, worst case | Theorem |
| D48 Crescenzi et al. | "the protein folding problem in the two-dimensional H-P model is NP-complete" | N, worst case | Theorem |
| D48 Unger–Moult | lowest-energy conformation of a lattice model "belongs to the class of NP-hard problems" | N | Theorem |
| D48 Hart–Istrail | poly-time folding "within three-eighths of optimal" (title) | N | Theorem (metadata) |
| D7 Outeiral (gap) | worst-case gap decreases "by five orders of magnitude between 6 and 9 amino acids"; authors "hypothesise … exponentially vanishing spectral gaps" | L = 6–9 (2D), 6–8 (3D) | Empirical, 3–4 sizes |
| D7 Outeiral (QA TTS) | 2D: poly x^0.65 vs e^{0.15x} "cannot be separated"; 3D: e^{0.45x} selected (§4) but "e^{0.75L}" (§7) | same | Empirical; **internally inconsistent** |
| D7 Outeiral (SA) | "fits to a square exponential e^{αx²}" but "could be an artifact of parameter optimisation" | same | Empirical, weak twin |
| D9 QFold | quantum-vs-classical min-TTS exponent 0.89 (Minifold init) / 0.53 (random); classical TTS vs size exponent 0.88; extrapolated "10^87 and 10^373" speedup | dipeptides (3–5 bits), tripeptides (2 bits) | Empirical; extrapolation invalid |
| D6 Robert | "number of qubits scales quadratically", Hamiltonian terms "O(N⁴)" | N monomers | Resource count, not runtime |
| D4 Fingerhuth | "6N − 17 ∈ O(N)" qubits (cubic); "4N − 10" (planar) | N | Resource count |
| D5 Babej | turn-circuit "3N − 8 ∈ O(N)" qubits (many-body) | N | Resource count |
| D10 Irbäck | N·L²/2 spins; L ≈ N gives cubic, a compact grid gives ~N² | N | Resource count |
| D11 Irbäck | pure-QPU success "exponentially decreasing", ≤20 | N ≤ 20 | Empirical (hardware) |
| D18 Linn | qubits feasible; gate count "unavailable today" | N | Resource analysis |
| D29 Scheiber | coupler resolution grows for turn encodings; QA scaling advantage "only noticeable … on the embedded problems" | small N | Empirical, self-refuting |
| D30 Wong–Chang | "quadratic speedup"; space O(n³) / O(n² log n); time ≈ √(2^{3(n−1)}) oracle calls | n aa | Query complexity vs brute force |
| D57 Montanaro | O(√T n^{3/2} log n) tests for backtracking tree of size T | T, n | Theorem (query) |
| D53/D54 | quadratic speedup in spectral gap for quantized Markov chains / annealing | δ | Theorem |
| D56 Montanaro | quadratic speedup in precision for Monte Carlo estimation | ε | Theorem |
| D40 Rattacaso | "quadratic speedup in the estimation of thermodynamic properties"; entanglement area law; efficient TN encoding for fixed-width lattices | lattice size | Theory + classical counterpart |
| D32 Agathangelou | SA ∝ e^{0.109M}; QAOA ∝ e^{0.029M} (SV) / e^{0.080M} (MPS, 6 res) in "calls" | M = 15–54 qubits | Empirical; incommensurate units |
| D45 Wüst–Landau | DOS and ground states "for sequence lengths up to 500 residues" (classical) | N ≤ 500 | Empirical classical capability |

**No paper gives any scaling in temperature, mixing time or precision for a realistic (off-lattice or learned) protein energy.**

---

## 6. NISQ route vs fault-tolerant route

- **NISQ (QA, VQE/QAOA, DCQO, BF-DCQO).** This is the entire hardware literature (D2–D6, D10–D11, D15–D17, D19–D26).
  - Pure-QPU capability tops out at roughly 12–16 aa with brute-forceable or classically referenced answers.
  - Success collapses with size: D10 N = 14, D11 N ≤ 20, D17 fails at 61 qubits.
  - Useful results rely on classical hybrid solvers or post-processing.
  - Every result falls into FM1–FM3, and the objective fails FM4 (D28).
  - **Verdict: no route.** It matches predecessor DE-1/DE-8.
- **Fault-tolerant.** There are three candidates:
  - (i) Idealised coherent QA with a possible "limited" constant-rate speedup (D7). The evidence rests on 3–4 sizes against weak SA.
  - (ii) Grover or backtracking over conformations (D30, D57). This is quadratic in the pruned tree at best and has no resource estimate.
  - (iii) **Quantum walks / QMCMC / amplitude estimation for Boltzmann sampling and thermodynamic estimation** (D9, D40, D53, D54, D56). This is the only route with (a) a proven separation (quadratic in gap or precision) and (b) a plausible link to the predecessor's positive soft-readout signal.
  - **No paper provides T-counts or logical qubits for a protein-energy walk operator.** That is a clear gap (§8).

---

## 7. Protein mapping and S29–S33 connection

**The lineage is direct.** Barkoutsos et al. CVaR (D55) → Robert et al. tetrahedral CVaR-VQE (D6) → Chandarana (D15), Doga (D21), Kipu/IonQ (D16, D17), QDockBank (D25). The predecessor's deployed CVaR-VQE is the same family. S30's T1 ("CVaR tail = prefix of energy order") and S33's R2 (solver equivalence under argmin) apply **verbatim** to this literature.

**Failure-mode audit** (FM1 diagonal + argmin/tail; FM2 enumerable; FM3 weak twin; FM4 cost does not track accuracy):

| Paper | Rep. | Max residues / qubits | HW/Sim | Primitive | Classical baseline (strength) | Scaling claim? | FM1 | FM2 | FM3 | FM4 |
|---|---|---|---|---|---|---|---|---|---|---|
| D2 Perdomo-Ortiz 2012 | 2D MJ lattice | 6 aa / 81 q | HW D-Wave | QA | enumeration (40 confs) | no | ✔ | ✔ | ✔ | n/a |
| D4 Fingerhuth 2018 | cubic/planar turn | 4 aa / sim | Sim (+tiny HW) | QAOA | none | no | ✔ | ✔ | ✔ | n/a |
| D5 Babej 2018 | 2D/3D turn | 10 aa (split) | HW D-Wave 2000Q | QA on subproblems | classical MC check | no | ✔ | ✔ | ✔ | n/a |
| D6 Robert 2021 | tetrahedral CG | 10 aa/22 q sim; 7 aa/9 q HW | both | CVaR-VQE | none | Pauli-term count only | ✔ | ✔ | ✔ | n/a |
| D7 Outeiral 2021 | 2D/3D MJ | 9 aa / 21 q | ideal sim | closed-system QA | gsl SA (weak) | **yes (limited, empirical)** | ✔ | ✔ | ✔ | n/a |
| D9 QFold 2022 | torsions (discrete) | tripeptide, 2 bits | sim + 1-step HW | quantum Metropolis walk | plain Metropolis (weak) | **yes (poly exponent)** | argmin TTS | ✔ | ✔ | n/a |
| D10 Irbäck 2022 | 2D HP grid QUBO | 64 hybrid / 14 pure | HW D-Wave Adv. | QA + hybrid | SA (weak); refs set by classical | no | ✔ | ✔ (N ≤ 30 exact known) | ✔ | n/a |
| D14 Boulebnane 2023 | tetra. lattice + LJ | alanine / 20 q; SAW 28 q | Sim | QAOA | random sampling | no (negative) | ✔ | ✔ | twin ties QAOA | n/a |
| D15 Chandarana 2023 | tetrahedral | 9 aa / 17 q | HW ×3 | CD-inspired VQA | none (QAOA, HEA) | no | ✔ | ✔ | ✔ | n/a |
| D16 Romero 2025 | tetrahedral HUBO | 12 aa / 33 q | HW IonQ | BF-DCQO + post-proc | brute force (truth) | no | ✔ | ✔ | ✔ | n/a |
| D17 Gomez Cadavid 2026 | tetrahedral HUBO | 16 aa / 61 q | HW 64-q Ba | BF-DCQO + consensus | random seeds (weak) | no | ✔ | near | ✔ | n/a |
| D19 Linn 2025 | tet/BCC/FCC | 26 aa / >40 q | Sim + ibm_kingston | HEA sampler | random sampling | no | ✔ | – | ✔ | n/a |
| D21 Doga 2024 | tetrahedral | 7 aa | HW ibm_cleveland | CVaR/VQE | brute force + Gurobi; AF2 | resource sketch | ✔ | ✔ | ✔ | **✔ (best RMSD ≠ optimum)** |
| D22 Li 2025 | FCC | 6 aa | HW IBM | PolyFit, VQE-C | none | no | ✔ | ✔ | ✔ | ? |
| D23 Pamidimukkala 2024 | HP turn | ≤114 q | HW IBM | VQE | (not read) | no | ✔ | ? | ? | ? |
| D25 QDockBank 2025 | lattice fragments | 14 aa | HW IBM | VQE | AF2/AF3 on fragments | no | ✔ | ✔ | ✔ (no same-H twin) | unexamined |
| D29 Scheiber 2026 | several | small | HW + SA | QA | in-house SA | yes → only on embedded | ✔ | ✔ | ✔ | n/a |
| D30 Wong–Chang 2021 | 3D HP BCC | 2 aa / 25 q | Sim | Grover | brute force | yes (quadratic query) | – | ✔ | ✔ | n/a |
| D32 Agathangelou 2025 | rotamer QUBO | 6 res / 54 q | MPS sim | QAOA | SA (calls) | yes (exponent fits) | ✔ | ✔ | ✔ | n/a |

**What would be different from S29–S33?**
1. Only the P-D sampling line (quantum walks, QMCMC, amplitude estimation of Boltzmann expectations) escapes FM1. It changes *what is consumed* from an argmin to a distribution or expectation, and it has a theoretical separation.
2. That is the program's AA-1 / SP-1. The literature neither kills nor supports it, because:
   - (a) no paper measures classical mixing on protein-like energies with a strong sampler (PT, WL, PERM);
   - (b) QFold's evidence is ≤ tripeptides against plain Metropolis;
   - (c) the one theoretical polymer result (D40) contains its own classical tensor-network counterpart.
3. The Opportunity Map's rank-2 classical kill test (τ_int, round-trip times and ESS/CPU-s vs length on the learned-energy posterior) is **exactly the missing experiment in this literature**. It is novel with respect to Domain D.

---

## 8. Literature gaps (novelty ≠ advantage)

1. **No head-to-head against strong classical lattice solvers** (PERM/nPERMis, pull-move REMC, Wang–Landau, CPSP) in any quantum-folding paper, 2012–2026. Filling this gap would most likely produce a *negative* paper. That is still valuable, but it is not an advantage route.
2. **No cost-Hamiltonian validity check** (condition C) before the quantum step, except D28 (2026, negative). Every hardware "accuracy" claim (D21, D25, D26) lacks the same-Hamiltonian classical optimum as control.
3. **No measurement of classical mixing or tunnelling times vs length** for lattice or learned protein energies at biologically relevant temperatures with best-in-class samplers. This is required before any quantum-walk or QMCMC claim. (The predecessor also never measured it: OP-01.)
4. **No fault-tolerant resource estimate** (logical qubits, T-count, walk-operator cost) for quantum Metropolis or quantum walks on any protein energy, lattice or off-lattice, learned or physical. D18 counts NISQ gates only; D21's estimate is self-described as simplified.
5. **No quantum-backtracking analysis** (D57) against a measured CPSP search-tree size T(N).
6. **No learned-energy formulation.** Deep-learning inputs appear only as initialisation (D9) or as post-hoc re-scoring (D26). No paper samples a learned posterior with a quantum primitive, which is the setting where the predecessor saw its only positive (soft-readout) signal.
7. **Reporting hygiene:** internal inconsistency (D7: 3D rate 0.45 vs 0.75); extrapolation over 80+ orders of magnitude (D9); incommensurate cost units (D7, D32).

---

## 9. Unverified leads (not cited as evidence)

- **BF-DCQO "runtime quantum advantage … for specific HUBO problems"** (ref. [61] in D16). Not identified or verified in this session. It is outside folding in any case.
- **Pamidimukkala 2024 (D23) details:** the search-engine summary says up to 22 aa with dense encoding on 127-qubit devices. I did not read the paper, so the classical baseline and ground-truth method are unknown.
- **Mulligan et al. 2019 QPacker (D33):** the "almost constant scaling vs SA" claim is known only secondhand via D8.
- **CPSP per-length runtimes and maximum sequence lengths** (D46/D47): not extracted; only the "exact and complete" abstract claim is used.
- **Perdomo-Ortiz 2012 device identity:** D4's text calls it "D-Wave One"; not checked in D2 itself.
- **Chinese hardware folding demonstrations** (for example on domestic superconducting processors) and **Fox et al., RNA folding with quantum computers**: suspected to exist; not searched or verified.
- **Campos, Casares, Martin-Delgado, "Quantum Metropolis Solver"** (a follow-up to QFold): not verified.
- **Kannan et al.'s earlier "hydrophobic collapse" quantum-encoding paper** (referenced by D24): not verified.

---

## 10. Bottom-line verdicts per primitive

**P-A. Quantum annealing / adiabatic / (BF-)DCQO for lattice folding: KILLED** (as a protein-structure route).
- Fourteen years of hardware work (D2 → D17) scale from 6 aa to 16 aa. Every instance is brute-forceable or classically referenced. Pure-QPU success decays exponentially (D10, D11).
- The only scaling evidence for a "limited speedup" (D7) rests on:
  - 3–4 peptide lengths (6–9 aa) in a fully enumerable space;
  - error-free closed-system simulation;
  - off-the-shelf GSL SA as the twin;
  - an internally inconsistent 3D rate;
  - an SA fit that its authors call possibly an artefact.
- D29 shows a QA scaling edge that exists only against SA on the embedded problem.
- The encoded objective is anti-correlated with RMSD at peptide length (D28).
- Nothing survives contact with PERM, REMC, WL or CPSP, which were never used as baselines.

**P-B. Variational (VQE / CVaR-VQE / QAOA / HEA / sample-based VQE) lattice folding: KILLED.**
- It is literally the predecessor's objective class (D55 → D6). H-001, R1 and R2 apply without modification.
- The best independent study (D14) finds QAOA "matched by random sampling up to a small overhead", which reproduces S33's random-prior ≥ VQE.
- Hardware "accuracy wins" (D21, D25) come from sample selection on anti-informative lattice costs, not from optimisation. In D21 the quantum best-RMSD structure is *not* the Hamiltonian optimum found by brute force and Gurobi.

**P-C. Grover / amplitude amplification over conformations: KILLED;** the quantum-backtracking variant is **WEAK.**
- D30/D31 prove only a quadratic *query* speedup over brute-force enumeration. That is not the classical frontier, which is pruned CP search (CPSP) and PERM.
- They were simulated at 2–3 residues. There is no T-count.
- The principled version (D57, √T over the classical search tree) has never been analysed for lattice proteins. Even if it were, it targets exact discrete optimisation, which the inherited evidence marks as discrimination-limited (Map C-4) and cost-limited (D28).

**P-D. Quantum walks / quantum Metropolis / amplitude estimation for Boltzmann sampling and ensemble estimation: INTERESTING** (conditional; not PROMISING).
- This is the only primitive here with:
  - (i) a proven separation: quadratic in spectral gap (D53, D54) or in precision (D56, D40);
  - (ii) a readout (distribution or expectation) outside the argmin class that killed the predecessor;
  - (iii) a plausible link to the predecessor's one positive signal (Boltzmann averaging beat argmin, S33 Q-C18).
- The literature's evidence for it is poor:
  - QFold (D9) covers ≤ tripeptides against plain Metropolis, with an extrapolation of 10^87 or more.
  - D40's quadratic estimation speedup comes with a classical tensor-network route for the tractable geometry.
  - Quantum-inspired encodings improve classical samplers (D38).
  - No fault-tolerant resource estimate exists for a protein-energy walk operator.
- It upgrades to PROMISING only if the program's classical kill test shows two things:
  - best-in-class classical samplers (PT, WL, PERM-type, SMC) exhibit steeply growing mixing times with length on the learned-energy posterior;
  - better samples transmit to built-chain accuracy.

**P-E. QA/QAOA for side-chain packing and lattice sequence design: WEAK.**
- The problems are real protein subproblems, but classical DEE, tree decomposition and ILP solvers are strong.
- The quantum-inspired encodings help classical solvers equally (D35).
- The only scaling claim (D32) compares CPU calls with QPU calls on ≤6 residues using MPS-simulated QAOA.
- It does not address a measured bottleneck of this program.

**P-F (boundary). Phase estimation for electronic structure of active sites: out of scope / WEAK for structure.**
- It may matter for chemistry (D64, D65), but generic exponential advantage is contested (D66). It has no demonstrated link to backbone-structure accuracy (Map AA-3, DE-7).

**Meta-assessment.** Does any paper show a load-bearing quantum component against a strong classical baseline on a realistic protein representation? **No.** Not one paper in 2008–2026 satisfies even two of the three conditions together:
1. **A realistic representation.** Only QFold uses torsions, and only up to tripeptides.
2. **A strong classical baseline.** No paper benchmarks PERM, REMC, WL, CPSP or DEE. The best twins are GSL SA, in-house SA, plain Metropolis or random sampling.
3. **A load-bearing quantum component.** Hybrid solvers, classical splitting and post-processing, or random-matched QAOA cover all of the hardware results. D17 explicitly admits that its post-processing "overwrit[es]" the quantum seeds' advantage.

The most rigorous independent studies (D14, D28, D29, and D7 read critically) point negative. The literature's single defensible open direction is the sampling or estimation line (P-D). There, the decisive classical measurement, mixing time vs length with best-in-class samplers, has never been made.
