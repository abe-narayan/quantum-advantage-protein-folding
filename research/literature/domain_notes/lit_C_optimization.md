# Domain C — Quantum optimization and search, with critiques

_Literature evidence notes for the coordinator. Written 2026-09-26. The scope is QAOA and QAOA+, VQE, CVaR and ADAPT, quantum annealing, Grover-type search and minimum finding, quantum backtracking and branch-and-bound, super-quadratic structured primitives, and the classical baselines used against all of these._

**Key question.** For protein-relevant discrete search, is there a quantum optimization mechanism whose scaling advantage survives both strong classical baselines and realistic fault-tolerant overhead? "Protein-relevant discrete search" here means:
- conformational search over exponentially large discrete spaces;
- contact-constraint satisfaction;
- rotamer or branch selection.

**Short answer (details in §10).** No mechanism in the literature meets both conditions for any protein-relevant problem.
- **Asymptotically provable separations** (Grover, minimum finding, backtracking, branch-and-bound) are at most about quadratic. Published fault-tolerant resource analyses conclude that quadratic speedups do not pay off on early fault-tolerant machines.
- **Heuristic scaling claims** (QAOA on LABS, annealing with QAC, counterdiabatic hybrids) rest on small-N noiseless simulation or on engineered spin-glass instances. Each has been matched, disputed, or not yet tested against the strongest classical solvers.
- **The only super-quadratic optimization-flavoured speedups** need algebraic or planted structure that has no known protein mapping. These are short-path and "jump to the end", Kikuchi or planted-inference, and DQI.

Label conventions follow LIT_RULES. "Verified" means I fetched or searched that authoritative page in this session.

---

## 1. Scope and search log

**Method.** Candidate arXiv ids were fetched in batches through the arXiv export API (`export.arxiv.org/api/query?id_list=...`). Each returns the title, authors, abstract, journal_ref and DOI. Individual `arxiv.org/abs/...` pages were fetched where a full verbatim abstract was needed. Non-arXiv papers were verified through publisher, PubMed, Semantic Scholar or DBLP pages found by WebSearch.

**Queries and fetches used:**
- arXiv API batches:
  - `1411.4028, 1709.03489, 1812.11173, 2005.10258, 1304.3061, 1907.04769, 1905.07047, 1910.08980`
  - `2106.05900, 2004.09002, 2005.08747, 2110.14206, 2101.05513, 2411.04979, 1803.11173, 2405.00781, 2312.09121`
  - `2308.02342, 1401.2910, 1512.02206, 1705.07452, 2207.13800, 2401.07184, quant-ph/9701001, quant-ph/9607014, quant-ph/9605043`
  - `1509.02374, 1906.10375, 1810.05582, 2007.07391, 2011.04149, 2406.19378, 2211.12489, 2312.02279` (id 1807.05571 was a wrong guess and returned an unrelated paper; corrected below)
  - `2009.05532, 2205.05786, 2101.07267, 2206.03579, 1812.07589, 2004.04197, 2202.09372, 2307.09442, 2208.06909`
  - `1401.1546, 1604.01746, 1711.01368, 1412.2104, 1501.05630, cond-mat/9512035, 2403.00910, 2210.04291, 2212.01513`
  - `2004.01118, 1908.02163, 1204.5485, 1811.00713, 2205.06084, 2312.00875, 2311.04186, 2408.08292`
  - `2307.00523, 2210.03210, 1711.05295, 1802.10124, 1907.12724, 2504.03832, 1812.01041, 0712.1008, 2503.05693`
  - `2507.19383, 2606.02104, 2402.09069, 2503.08247, 2511.04553`
  - `2505.22514, 2508.08869, 2405.09169, 2509.11535, 2505.08663`
  - `2310.03011, 2204.03455, 1704.06774, 2108.06049, 2204.10306`
  - `2506.07866, 2604.26861, 2508.10660`
  - `2504.00987, 2607.09688`
- Full-abstract fetches (`arxiv.org/abs/`): 2007.07391, 2011.04149, 1810.05582, 2406.19378, 1906.10375, 2401.07184, 1705.07452, 1910.08980, 1905.07047, 2507.19383, 2004.01118, 2510.06337, 2603.13607, 2511.04553, 2506.17391, 2504.00987.
- PMC full text of Shaydulin et al. (PMC11135426), for the TTS exponents.
- WebSearch queries:
  - "Ambainis Balodis … exponential-time dynamic programming"
  - "Montanaro Quantum-walk speedup of backtracking Theory of Computing"
  - "LABS … classical solver scaling rebuttal QAOA"
  - "Shaydulin LABS QAOA scaling advantage critique 1.21^N"
  - "quantum-enhanced memetic tabu search LABS"
  - "Munoz-Bauza Lidar … critique OR comment OR classical rebuttal"
  - "Toward quantum scaling advantage in approximate optimization simulated bifurcation"
  - "Evidence of scaling advantage on an NP-complete problem with enhanced quantum solvers"
  - "Boulebnane Montanaro PRX Quantum"
  - "Zhu Tang Barron adaptive QAOA PRR"
  - "Perdomo-Ortiz Sci Rep 2012"
  - "side-chain packing rotamer optimization quantum annealing OR QAOA"
  - "protein folding trapped-ion counterdiabatic"
  - "Pierce Winfree Protein design NP-hard"
  - "Berger Leighton HP NP-complete"
  - "Traoré … cost function network"
  - "Jinbo Xu tree decomposition side-chain"
  - "Hsu Mehra Nadler Grassberger PERM"
  - "Backofen Will CPSP"
  - "Hoefler Häner Troyer CACM"
- Semantic Scholar API: DOI 10.1186/1471-2105-9-230 (CPSP-tools).
- Failed or blocked (not relied on): Springer, APS and Nature landing pages (redirects or 403) and the Crossref API (429). The same records were verified through arXiv or search listings instead.

---

## 2. Verified papers (per-paper fields)

Abbreviations: **Alg** algorithm; **Set** problem setting; **Claim** claimed speedup or result, verbatim where quoted; **Res** resource assumptions; **Comp** classical comparator; **T/E** theoretical or empirical; **Lim** limitations; **Lab** claim labels.

### 2A. Variational algorithms: QAOA, QAOA+, VQE, CVaR, ADAPT

**[C1] A Quantum Approximate Optimization Algorithm**
- Farhi, Goldstone, Gutmann; 2014; arXiv preprint; arXiv:1411.4028.
- Verified: export.arxiv.org API (id 1411.4028).
- **Alg:** p-layer alternating cost and mixer unitaries.
- **Set:** MaxCut on 3-regular graphs.
- **Claim (abstract):** "For p = 1, on 3-regular graphs the quantum algorithm always finds a cut that is at least 0.6924 times the size of the optimal cut."
- **Res:** gate model, no fault tolerance assumed.
- **Comp:** none in the abstract. Goemans–Williamson gives 0.878 in general, so p=1 is below the best classical guarantee.
- **T/E:** theoretical.
- **Lim:** approximation ratio only; no runtime speedup claim.
- **Lab:** THEORETICAL (approximation guarantee); NO ADVANTAGE claimed.

**[C2] From the QAOA to a Quantum Alternating Operator Ansatz**
- Hadfield, Wang, O'Gorman, et al.; 2019; *Algorithms* 12(2):34; DOI 10.3390/a12020034; arXiv:1709.03489.
- Verified: arXiv API.
- **Alg:** QAOA+ with problem-specific mixers that preserve the feasible subspace.
- **Set:** constrained combinatorial problems.
- **Claim:** "This ansatz supports the representation of a larger, and potentially more useful, set of states than the original formulation."
- **Res:** gate model.
- **Comp:** none.
- **T/E:** framework.
- **Lim:** no performance or speedup claim. It is relevant to protein models because constraints such as self-avoidance and one-hot rotamer choice can be enforced in the mixer rather than by penalties.
- **Lab:** none (framework); NO ADVANTAGE claimed.

**[C3] An adaptive variational algorithm for exact molecular simulations on a quantum computer (ADAPT-VQE)**
- Grimsley, Economou, Barnes, Mayhall; 2019; *Nat. Commun.* 10, 3007; DOI 10.1038/s41467-019-10988-2; arXiv:1812.11173.
- Verified: arXiv API.
- **Alg:** operator-pool greedy ansatz growth.
- **Set:** molecular electronic structure, not combinatorial optimization.
- **Claim:** "Our algorithm performs much better than a unitary coupled cluster approach, in terms of both circuit depth and chemical accuracy."
- **Comp:** UCCSD, a quantum baseline rather than a classical one.
- **T/E:** simulation.
- **Lim:** the comparison is quantum versus quantum; not a speedup over classical methods.
- **Lab:** SIMULATOR RESULT; NO ADVANTAGE (versus classical) claimed.

**[C4] Adaptive QAOA for solving combinatorial problems on a quantum computer (ADAPT-QAOA)**
- Zhu, Tang, Barron, Calderon-Vargas, Mayhall, Barnes, Economou; 2022; *Phys. Rev. Research* 4, 033029; DOI 10.1103/PhysRevResearch.4.033029; arXiv:2005.10258.
- Verified: arXiv API plus search (OSTI/PRR listing).
- **Claim:** "It converges much faster than the standard QAOA, while simultaneously reducing the required number of CNOT gates and optimization parameters."
- **Comp:** standard QAOA only.
- **T/E:** simulation.
- **Lim:** no classical baseline.
- **Lab:** SIMULATOR RESULT; NO ADVANTAGE (versus classical) claimed.

**[C5] A variational eigenvalue solver on a photonic quantum processor (VQE)**
- Peruzzo, McClean, Shadbolt, et al.; 2014; *Nat. Commun.* 5, 4213; DOI 10.1038/ncomms5213; arXiv:1304.3061.
- Verified: arXiv API.
- **Claim:** "…by drastically reducing the coherence time requirements, enhances the potential of the quantum resources available today…"
- **Set:** He–H+ ground state.
- **Comp:** none.
- **Lab:** HARDWARE DEMONSTRATION (feasibility); NO ADVANTAGE claimed.

**[C6] Improving Variational Quantum Optimization using CVaR**
- Barkoutsos, Nannicini, Robert, Tavernelli, Woerner; 2020; *Quantum* 4, 256; DOI 10.22331/q-2020-04-20-256; arXiv:1907.04769.
- Verified: arXiv API.
- **Alg:** replaces the expectation objective with CVaR_α of sampled diagonal energies.
- **Claim:** "This leads to faster convergence to better solutions for all combinatorial optimization problems tested in our study."
- **Comp:** expectation-value VQE and QAOA; no strong classical solver.
- **T/E:** simulation plus small hardware runs.
- **Lim:** improvement is relative to variational baselines only. This is the objective used in S29–S33.
- **Lab:** SIMULATOR RESULT; NO ADVANTAGE (versus classical).

**[C7] QAOA: Performance, Mechanism, and Implementation on Near-Term Devices**
- Zhou, Wang, Choi, Pichler, Lukin; 2020; *PRX* 10, 021067; DOI 10.1103/PhysRevX.10.021067; arXiv:1812.01041.
- Verified: arXiv API.
- **Claim:** "QAOA can learn via optimization to utilize non-adiabatic mechanisms to circumvent challenges…"
- **Set:** MaxCut, small n, heuristic parameter strategies.
- **Lab:** SIMULATOR RESULT; HEURISTIC; no classical advantage shown.

### 2B. Critiques and classical matches for QAOA (locality, symmetry, OGP)

**[C8] Classical and Quantum Bounded Depth Approximation Algorithms**
- Hastings; 2019; arXiv preprint (no journal_ref shown); arXiv:1905.07047.
- Verified: arxiv.org/abs/1905.07047.
- **Claim (abstract):**
  - "a single step of the classical algorithm will outperform the single-step QAOA on all triangle-free MAX-CUT instances"
  - "for any fixed number of steps, its [QAOA's] performance on MAX-3-LIN-2 on bounded degree graphs cannot achieve the same scaling as can be done by a class of 'global' classical algorithms"
  - "local classical algorithms are likely to be at least as promising as the QAOA for approximate optimization."
- **T/E:** theoretical.
- **Lab:** NO ADVANTAGE; ADVANTAGE DISPUTED (for bounded-depth QAOA).

**[C9] Obstacles to Variational Quantum Optimization from Symmetry Protection**
- Bravyi, Kliesch, Koenig, Tang; 2020; *PRL* 125, 260505; DOI 10.1103/PhysRevLett.125.260505; arXiv:1910.08980.
- Verified: arxiv.org/abs/1910.08980.
- **Claim (abstract):**
  - "the Goemans-Williamson algorithm outperforms the Quantum Approximate Optimization Algorithm (QAOA) for certain instances of MaxCut, at any constant level."
  - "the locality and symmetry of QAOA severely limits its performance."
- They propose a non-local recursive QAOA (RQAOA).
- **Lab:** NO ADVANTAGE (constant-depth QAOA); THEORETICAL.

**[C10] Classical algorithms and quantum limitations for maximum cut on high-girth graphs**
- Barak, Marwaha; 2022; ITCS 2022, art. 14; DOI 10.4230/LIPIcs.ITCS.2022.14; arXiv:2106.05900.
- Verified: arXiv API.
- **Claim:** "every one-local algorithm achieves … a maximum cut of at most 1/2 + C/√D". The paper also gives classical algorithms that beat low-depth QAOA on high-girth graphs.
- **Lab:** NO ADVANTAGE; THEORETICAL.

**[C11] Local classical MAX-CUT algorithm outperforms p=2 QAOA on high-girth regular graphs**
- Marwaha; 2021; *Quantum* 5, 437; DOI 10.22331/q-2021-04-20-437; arXiv:2101.05513.
- Verified: arXiv API.
- **Claim:** "there exists a 2-local randomized classical algorithm … that has a larger expected cut fraction than QAOA_2".
- **Lab:** NO ADVANTAGE.

**[C12] The QAOA Needs to See the Whole Graph: A Typical Case**
- Farhi, Gamarnik, Gutmann; 2020; arXiv:2004.09002 (no journal_ref shown).
- Verified: arXiv API.
- **Claim:** "if p is less than a d-dependent constant times log n, the QAOA cannot do better than finding an independent set of size .854 times the optimal". The argument uses the overlap gap property (OGP).
- **Lab:** NO ADVANTAGE (locality limit); THEORETICAL.

**[C13] The QAOA Needs to See the Whole Graph: Worst Case Examples**
- Farhi, Gamarnik, Gutmann; 2020; arXiv:2005.08747.
- Verified: arXiv API.
- **Claim:** "the QAOA with (d−1)^{2p} < n^A for any A<1, can only achieve an approximation ratio of 1/2 for Max-Cut" (on bipartite random d-regular graphs).
- **Lab:** NO ADVANTAGE; THEORETICAL.

**[C14] QAOA at High Depth for MaxCut on Large-Girth Regular Graphs and the SK Model**
- Basso, Farhi, Marwaha, Villalonga, Zhou; 2022; TQC 2022, 7:1–7:21; DOI 10.4230/LIPIcs.TQC.2022.7; arXiv:2110.14206.
- Verified: arXiv API.
- **Claim:** "at optimal parameters and as D goes to infinity … the p=11 QAOA beats all classical algorithms". This holds on large-girth D-regular graphs, relative to the classical algorithms known at the time and under assumptions stated in the paper.
- **Lab:** THEORETICAL; HEURISTIC ADVANTAGE (approximation ratio in a limit). Contrast with [C15] and [C23].

**[C15] Performance and limitations of the QAOA at constant levels on large sparse hypergraphs and spin glass models**
- Basso, Gamarnik, Mei, Zhou; 2022; FOCS 2022, pp. 335–343; DOI 10.1109/FOCS54457.2022.00039; arXiv:2204.10306.
- Verified: arXiv API.
- **Claim:** "the average-case value produced by the QAOA at constant levels is bounded away from optimality for pure q-spin models when q≥4" (via OGP).
- **Lab:** NO ADVANTAGE (constant depth); THEORETICAL.

**[C16] Limitations of Local Quantum Algorithms on Random Max-k-XOR and Beyond**
- Chou, Love, Sandhu, Shi; 2021; arXiv:2108.06049 (venue not recorded).
- Verified: arXiv API.
- **Claim:** "any generic local algorithm … cannot arbitrarily-well approximate boolean CSPs if the problem satisfies … the coupled overlap-gap property".
- **Lab:** NO ADVANTAGE; THEORETICAL.

**[C17] Quantum speedups in solving near-symmetric optimization problems by low-depth QAOA**
- Montanaro, Zhou; 2024; arXiv:2411.04979.
- Verified: arXiv API.
- **Claim:** "the 1-step QAOA can achieve a success probability of Ω(1/√n) … proving a separation of O(1) quantum queries and Ω(n/log n) classical queries".
- **Res:** oracle or query model on specially constructed near-symmetric cost functions.
- **Lab:** QUERY-COMPLEXITY SPEEDUP; ORACLE-MODEL RESULT.
- **Lim:** contrived symmetric problems; must not be converted to a runtime claim on natural instances.

**[C18] QAOA for Max-Cut requires hundreds of qubits for quantum speed-up**
- Guerreschi, Matsuura; 2019; *Sci. Rep.* 9, 6903; DOI 10.1038/s41598-019-43176-9; arXiv:1812.07589.
- Verified: arXiv API.
- **Claim:** "quantum speedup will not be attainable, at least for a representative combinatorial problem, until several hundreds of qubits are available".
- **Lab:** NO ADVANTAGE (at small n); resource extrapolation.

**[C19] Sampling Frequency Thresholds for Quantum Advantage of QAOA**
- Lykov, Wurtz, Poole, et al.; 2023; *npj QI* 9, 73; DOI 10.1038/s41534-023-00718-4; arXiv:2206.03579.
- Verified: arXiv API.
- **Claim:** "the number of required samples grows exponentially with N, hindering the scalability of QAOA with p≤11". The paper compares against Gurobi and MQLib-type classical solvers for MaxCut on 3-regular graphs.
- **Lab:** NO ADVANTAGE (low depth); ADVANTAGE DISPUTED.

### 2C. Trainability, noise and dequantization of variational methods

**[C20] Barren plateaus in quantum neural network training landscapes**
- McClean, Boixo, Smelyanskiy, Babbush, Neven; 2018; *Nat. Commun.* 9, 4812; DOI 10.1038/s41467-018-07090-4; arXiv:1803.11173.
- Verified: arXiv API.
- **Claim:** "the probability that the gradient along any reasonable direction is non-zero … is exponentially small as a function of the number of qubits" (for random parameterized circuits).
- **Lab:** NO ADVANTAGE (trainability obstacle); THEORETICAL.

**[C21] Barren Plateaus in Variational Quantum Computing (review)**
- Larocca, Thanasilp, Wang, et al.; 2025; *Nat. Rev. Phys.* 7, 174–189; DOI 10.1038/s42254-025-00813-9; arXiv:2405.00781.
- Verified: arXiv API.
- **Claim:** "all the moving pieces of an algorithm … can lead to BPs when ill-suited".
- **REVIEW (orientation only).**

**[C22] Does provable absence of barren plateaus imply classical simulability?**
- Cerezo, Larocca, García-Martín, et al.; 2025; *Nat. Commun.* 16, 7907; DOI 10.1038/s41467-025-63099-6; arXiv:2312.09121.
- Verified: arXiv API.
- **Claim:** "many commonly used models whose loss landscapes avoid barren plateaus can also admit classical simulation".
- Stated as evidence and argument, not a theorem for all models.
- **Lab:** NO ADVANTAGE (a trainability-versus-simulability dilemma); THEORETICAL.

**[C23] Training variational quantum algorithms is NP-hard**
- Bittel, Kliesch; 2021; *PRL* 127, 120502; DOI 10.1103/PhysRevLett.127.120502; arXiv:2101.07267.
- Verified: arXiv API.
- **Claim:** "gradient and higher order descent algorithms will generally converge to far from optimal solutions".
- **Lab:** NO ADVANTAGE; THEORETICAL.

**[C24] Beyond Barren Plateaus: Quantum Variational Algorithms Are Swamped With Traps**
- Anschuetz, Kiani; 2022; *Nat. Commun.* 13, 7760; DOI 10.1038/s41467-022-35364-5; arXiv:2205.05786.
- Verified: arXiv API.
- **Claim:** "only a superpolynomially small fraction of local minima within any constant energy from the global minimum".
- **Lab:** NO ADVANTAGE; THEORETICAL.

**[C25] Limitations of optimization algorithms on noisy quantum devices**
- Stilck França, García-Patrón; 2021; *Nat. Phys.*; DOI 10.1038/s41567-021-01356-3; arXiv:2009.05532.
- Verified: arXiv API.
- **Claim:** "substantial quantum advantages are unlikely for classical optimization unless the current noise rates are decreased by orders of magnitude".
- **Lab:** NO ADVANTAGE (NISQ); THEORETICAL.

**[C26] Limitations of variational quantum algorithms: a quantum optimal transport approach**
- De Palma, Marvian, Rouzé, Stilck França; 2023; *PRX Quantum* 4, 010309; DOI 10.1103/PRXQuantum.4.010309; arXiv:2204.03455.
- Verified: arXiv API.
- **Claim:** "at depths L=O(p⁻¹) it is exponentially unlikely that the outcome of a noisy quantum circuit outperforms efficient classical algorithms".
- **Lab:** NO ADVANTAGE (noisy); THEORETICAL.

**[C27] Quantum Approximate Optimization of Non-Planar Graph Problems on a Planar Superconducting Processor**
- Harrigan, Sung, Neeley, et al.; 2021; *Nat. Phys.* 17, 332–336; DOI 10.1038/s41567-020-01105-y; arXiv:2004.04197.
- Verified: arXiv API.
- **Claim:** "performance decreases with problem size but still provides an advantage over random guessing".
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

### 2D. Recent QAOA-type scaling-advantage claims and responses

**[C28] Evidence of Scaling Advantage for QAOA on a Classically Intractable Problem (LABS)**
- Shaydulin, Li, Chakrabarti, et al. (33 authors); 2024; *Sci. Adv.* 10(22), eadm6761; DOI 10.1126/sciadv.adm6761; arXiv:2308.02342.
- Verified: arXiv API; full text at pmc.ncbi.nlm.nih.gov/articles/PMC11135426.
- **Alg:** fixed-parameter QAOA, p=12; optionally combined with quantum minimum finding (QMF, a Grover-type step).
- **Set:** LABS; noiseless simulation up to N=40. Hardware runs on Quantinuum H-series up to N=18, p=1, with error detection.
- **Claim (abstract):** "runtime of QAOA with fixed parameters scales better than branch-and-bound solvers".
- **Full-text TTS exponents:**

  | Method | Scaling |
  |---|---|
  | QAOA p=12 | 1.46^N |
  | QAOA + QMF | 1.21^N |
  | Memetic Tabu Search (best classical heuristic) | 1.34^N |
  | Branch-and-bound (time to solution) | 1.62^N |
  | Branch-and-bound (time to certificate) | 1.73^N |

- **Res:** the 1.21^N figure requires amplitude amplification, and so requires fault tolerance. The authors note that larger instances "would likely require error correction".
- **Comp:** exact branch-and-bound and MTS.
- **T/E:** simulator.
- **Lim:**
  - QAOA alone (1.46^N) scales **worse** than MTS (1.34^N).
  - The claimed win over MTS appears only after adding a quadratic Grover-type layer.
  - The authors themselves note that MTS might also be quadratically accelerated, in the style of quantum simulated annealing, which would erase the comparison.
  - N ≤ 40.
- **Lab:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (versus exact B&B); ADVANTAGE DISPUTED (versus the best heuristic, see [C29]–[C31]).

**[C29] Scaling advantage with quantum-enhanced memetic tabu search for LABS**
- Gomez Cadavid, Chandarana, Romero, et al.; 2025 preprint (later published in *Quantum Mach. Intell.*, DOI 10.1007/s42484-026-00433-1 per the Springer listing; landing page not fetched); arXiv:2511.04553.
- Verified: arxiv.org/abs/2511.04553.
- **Claim:** "suppresses the empirical time-to-solution scaling to O(1.24^N) for sequence length N∈[27,37] … surpasses the best-known classical heuristic O(1.34^N)"; projected "crossover point at N ≳ 47".
- **Res:** DCQO seeds for classical MTS; circuits simulated.
- **Lim:** N ≤ 37 simulated; the crossover is extrapolated.
- **Lab:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (claimed); not independently confirmed.

**[C30] New Improvements in Solving Large LABS Instances Using Massively Parallelizable Memetic Tabu Search**
- Zhang, Shen, Kumar, et al.; 2025; arXiv:2504.00987.
- Verified: arxiv.org/abs/2504.00987.
- **Claim:** GPU MTS reaches "sizes up to 120", with "up to 26 fold speedup compared to the analogous 16-core CPU implementation", and finds "new LABS merit factor values for sixteen different problem sizes between 92 and 120".
- **Lab:** classical baseline (strengthens the classical frontier). The quantum claims above are extrapolated from N ≤ 40.

**[C31] A competitive NISQ and qubit-efficient solver for the LABS problem (Pauli correlation encoding)**
- Sciorilli, Camilo, Maciel, et al.; 2025/2026; arXiv:2506.17391.
- Verified: arxiv.org/abs/2506.17391.
- **Claim:** "We observe improved scaling in the total time to reach the exact solution, outperforming the best-performing classical heuristic while using only a fraction of the quantum resources".
- **Lab:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (claimed); not independently confirmed.

**[C32] Solving Boolean Satisfiability Problems With QAOA**
- Boulebnane, Montanaro; 2024; *PRX Quantum* 5, 030348; DOI 10.1103/PRXQuantum.5.030348; arXiv:2208.06909.
- Verified: arXiv API plus search listing of the PRX Quantum DOI.
- **Claim:** "for around 14 ansatz layers, QAOA matches the scaling performance of the highest-performance classical solver tested" (random k-SAT at threshold; analytic in the large-n limit plus numerics). With amplitude amplification added, the QAOA becomes competitive or better, which requires fault tolerance.
- **Lab:** THEORETICAL + SIMULATOR RESULT; HEURISTIC ADVANTAGE (at best parity without amplification).

**[C33] Towards a Linear-Ramp QAOA protocol: Evidence of a scaling advantage in solving some combinatorial optimization problems**
- Montanez-Barrera, Michielsen; 2025; *npj QI* 11, 131; DOI 10.1038/s41534-025-01082-1; arXiv:2405.09169.
- Verified: arXiv API.
- **Claim:** "success probability scales as P(x*) ≈ 2^(−η(p) N_q + C), where η(p) decreases with increasing p". Simulations reach N_q=42 and p=400; hardware runs reach 109 qubits.
- **Comp:** SA, Tabu, branch-and-bound.
- **Lab:** SIMULATOR RESULT + HARDWARE DEMONSTRATION; HEURISTIC ADVANTAGE (claimed, small N).

**[C34] Evidence of scaling advantage on an NP-Complete problem with enhanced quantum solvers**
- Lu, Wei, Li, et al.; 2026; *Nat. Comput. Sci.*; DOI 10.1038/s43588-026-01007-8; arXiv:2508.08869.
- Verified: arXiv API plus search listing.
- **Claim:** space reduction (RSRA) plus QAOA or QAA on one-in-three SAT; "problem instances with up to 65 variables"; "superconducting quantum processor with 13 qubits"; enhanced solvers "outperform state-of-the-art classical solvers".
- **Lim:** small N; the classical space reduction does much of the work.
- **Lab:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (claimed).

**[C35] Combinatorial optimization enhanced by shallow quantum circuits with 104 superconducting qubits**
- Zhu, Zou, Jin, et al.; 2025/2026; *Natl. Sci. Rev.*; DOI 10.1093/nsr/nwag124; arXiv:2509.11535.
- Verified: arXiv API.
- **Claim:** "outputs favorable solutions against even a highly-optimized classical simulated annealing (SA) algorithm".
- **Lab:** HARDWARE DEMONSTRATION; weak baseline (SA only), so it cannot be read as a general advantage.

**[C36] Runtime Quantum Advantage with Digital Quantum Optimization (BF-DCQO)**
- Chandarana, Gomez Cadavid, Romero, et al.; 2025; arXiv:2505.08663.
- Verified: arXiv API.
- **Claim:** "outperform simulated annealing (SA) and CPLEX".
- **Lab:** HARDWARE DEMONSTRATION; ADVANTAGE DISPUTED. [C45] reports "no runtime advantage observed under comprehensive benchmarking".

**[C37] The Quest for Quantum Advantage in Combinatorial Optimization: End-to-end Benchmarking of Quantum Solvers vs. Multi-core Classical Solvers**
- Chandarana, Gomez Cadavid, Solano, et al.; 2026; arXiv:2603.13607.
- Verified: arxiv.org/abs/2603.13607.
- **Claim:** HSQC on one QPU "can achieve performance competitive with strong classical solvers running on 128 vCPUs or 8 NVIDIA A100 GPUs". The abstract's own summary also reports that enhanced parallel tempering and the GPU ABS3 solver "matched or exceeded quantum results".
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE against the strongest baselines (by its own account).

### 2E. Quantum annealing: claims and rebuttals

**[C38] Defining and detecting quantum speedup**
- Rønnow, Wang, Job, et al.; 2014; *Science* 345, 420; DOI 10.1126/science.1252319; arXiv:1401.2910.
- Verified: arXiv API.
- **Claim:** "find no evidence of quantum speedup when the entire data set is considered". The paper defines "limited" versus "potential" speedup.
- **Lab:** NO ADVANTAGE; methodological.

**[C39] Glassy Chimeras could be blind to quantum speedup**
- Katzgraber, Hamze, Andrist; 2014; *PRX* 4, 021008; DOI 10.1103/PhysRevX.4.021008; arXiv:1401.1546.
- Verified: arXiv API.
- **Claim:** "benchmarking optimization methods using spin glasses on the Chimera graph might not be the best benchmark problems" (no finite-temperature spin-glass transition, so the instances are classically easy).
- **Lab:** methodological critique; NO ADVANTAGE.

**[C40] What is the Computational Value of Finite Range Tunneling?**
- Denchev, Boixo, Isakov, et al.; 2016; *PRX* 6, 031015; DOI 10.1103/PhysRevX.6.031015; arXiv:1512.02206.
- Verified: arXiv API.
- **Claim:** D-Wave 2X "~10^8 times faster than SA" on weak-strong cluster instances.
- **Comp:** SA and QMC. The paper itself notes that other classical algorithms, such as cluster-finding methods, do better.
- **Lab:** HARDWARE DEMONSTRATION; ADVANTAGE DISPUTED (constant factor versus SA; see [C41]).

**[C41] Strengths and weaknesses of weak-strong cluster problems: A detailed overview of state-of-the-art classical heuristics versus quantum approaches**
- Mandrà, Zhu, Wang, Perdomo-Ortiz, Katzgraber; 2016; *PRA* 94, 022337; DOI 10.1103/PhysRevA.94.022337; arXiv:1604.01746.
- Verified: arXiv API.
- **Claim:** "quantum speedup is limited to sequential approaches". Classical algorithms that exploit the cluster structure (for example HFS and cluster moves) match or beat the quantum annealer.
- **Lab:** ADVANTAGE DISPUTED.

**[C42] Demonstration of a scaling advantage for a quantum annealer over simulated annealing**
- Albash, Lidar; 2018; *PRX* 8, 031016; DOI 10.1103/PhysRevX.8.031016; arXiv:1705.07452.
- Verified: arxiv.org/abs/1705.07452.
- **Claim:** "the D-Wave device exhibits certifiably better scaling than simulated annealing, with 95% confidence … However, we do not find evidence for a quantum speedup: simulated quantum annealing exhibits the best scaling by a significant margin."
- **Lab:** HARDWARE DEMONSTRATION; limited scaling advantage over SA only; NO ADVANTAGE versus the best classical method (SQA).

**[C43] A deceptive step towards quantum speedup detection**
- Mandrà, Katzgraber; 2018; *Quantum Sci. Technol.* 3, 04LT01; DOI 10.1088/2058-9565/aac8b2; arXiv:1711.01368.
- Verified: arXiv API.
- **Claim:** D-Wave 2000Q on deceptive cluster-loop instances: "While there is a sizable constant speedup over all known classical heuristics, a noticeable improvement in the scaling remains elusive."
- **Lab:** HARDWARE DEMONSTRATION; constant factor only; NO scaling advantage.

**[C44] Scaling Advantage in Approximate Optimization with Quantum Annealing**
- Munoz-Bauza, Lidar; 2025; *PRL* 134, 160601; DOI 10.1103/PhysRevLett.134.160601; arXiv:2401.07184.
- Verified: arxiv.org/abs/2401.07184.
- **Claim:** "with QAC, quantum annealing exhibits a scaling advantage over PT-ICM at sampling low energy states with an optimality gap of at least 1.0%".
- **Res:** QAC gives "over 1,300 error-suppressed logical qubits on a degree-5 interaction graph"; 2D spin glasses with high-precision couplings; time-to-epsilon metric.
- **Comp:** PT-ICM (strong).
- **Lab:** HARDWARE DEMONSTRATION; EMPIRICAL ADVANTAGE (claimed; approximate optimization only); ADVANTAGE DISPUTED ([C45], [C46]).

**[C45] Toward quantum scaling advantage in approximate optimization**
- Pawłowski, Tarasiuk, Tuziemski, et al.; 2026; *Phys. Rev. Applied* 26, 014024; DOI 10.1103/qcws-8kgm; arXiv:2505.22514.
- Verified: arXiv API plus search listing (the APS page returned 403).
- **Claim:** SBM gives "comparable or superior scaling", "closing the reported quantum–classical gap". "the small instances studied previously are insufficient to infer asymptotic behavior". "current quantum annealers are unlikely to exhibit a clear scaling advantage over SBM-like solvers".
- **Lab:** ADVANTAGE DISPUTED (direct rebuttal of [C44]).

**[C46] Recent quantum runtime (dis)advantages** (published as "Limits of quantum run-time advantage")
- Tuziemski, Pawłowski, Tarasiuk, et al.; 2026; *Phys. Rev. Applied* 25, 044084; arXiv:2510.06337.
- Verified: arxiv.org/abs/2510.06337.
- **Claim:** "conventional quantum runtime analyses excluding substantial system-level overheads can lead to biased performance assessments". The paper re-evaluates [C44] and BF-DCQO [C36]. Conclusion: "Runtime-based quantum advantage has not yet been demonstrated" (summary of the paper's conclusion).
- **Lab:** ADVANTAGE DISPUTED.

**[C47] Quantum critical dynamics in a 5000-qubit programmable spin glass**
- King, Raymond, Lanting, et al.; 2023; *Nature*; DOI 10.1038/s41586-023-05867-2; arXiv:2207.13800.
- Verified: arXiv API.
- **Claim:** "extract critical exponents that clearly distinguish quantum annealing from the slower stochastic dynamics of analogous Monte Carlo algorithms".
- **Lab:** HARDWARE DEMONSTRATION of coherent dynamics. This is **not** an optimization speedup: it compares dynamics, not time-to-solution against the best solvers.

**[C48] Beyond-classical computation in quantum simulation**
- King, Nocera, Rams, et al.; 2025; *Science* 388, 199–204; DOI 10.1126/science.ado6285; arXiv:2403.00910.
- Verified: arXiv API.
- **Claim:** "quantum annealers can answer questions of practical importance that may remain out of reach for classical computation."
- **Set:** quench dynamics simulation, not optimization.
- **Lab:** HARDWARE DEMONSTRATION (simulation task); ADVANTAGE DISPUTED ([C49], [C50]). Recorded to prevent misuse as optimization evidence.

**[C49] Dynamics of disordered quantum systems with two- and three-dimensional tensor networks**
- Tindall, Mello, Fishman, et al.; 2026; *Science* 392, 868–872; DOI 10.1126/science.adx2728; arXiv:2503.05693.
- Verified: arXiv API.
- **Claim:** "state-of-the-art accuracies can be achieved with modest computational resources".
- **Lab:** ADVANTAGE DISPUTED (versus [C48]).

**[C50] Challenging the Quantum Advantage Frontier with Large-Scale Classical Simulations of Annealing Dynamics**
- Mauron, Carleo; 2025; arXiv:2503.08247.
- Verified: arXiv API.
- **Claim:** "classical variational techniques remain competitive at larger system sizes than previously anticipated".
- **Lab:** ADVANTAGE DISPUTED.

**[C51] Quantum Optimization of Maximum Independent Set using Rydberg Atom Arrays**
- Ebadi, Keesling, Cain, et al.; 2022; *Science* 376, 1209; DOI 10.1126/science.abo6587; arXiv:2202.09372.
- Verified: arXiv API.
- **Claim:** "superlinear quantum speedup in finding exact solutions in the deep circuit regime" relative to SA, on hardest graphs defined by an SA-specific hardness parameter.
- **Lab:** HARDWARE DEMONSTRATION; limited speedup versus SA; ADVANTAGE DISPUTED ([C52]).

**[C52] Hardness of the Maximum Independent Set Problem on Unit-Disk Graphs and Prospects for Quantum Speedups**
- Andrist, Schuetz, Minssen, et al.; 2023; *PRR* 5, 043277; DOI 10.1103/PhysRevResearch.5.043277; arXiv:2307.09442.
- Verified: arXiv API.
- **Claim:** "quasi-planar instances with Union-Jack-like connectivity can be solved to optimality for up to thousands of nodes within minutes" (classical exact solvers).
- **Lab:** ADVANTAGE DISPUTED.

**[C53] On the Emerging Potential of Quantum Annealing Hardware for Combinatorial Optimization**
- Tasseff, Albash, Morrell, et al.; 2022; arXiv:2210.04291.
- Verified: arXiv API.
- **Claim:** "classes of contrived problems exist where this quantum annealer can provide run time benefits".
- **Lab:** HARDWARE DEMONSTRATION; HEURISTIC ADVANTAGE on contrived instances only.

### 2F. Grover-type search, lower bounds, minimum finding

**[C54] A fast quantum mechanical algorithm for database search**
- Grover; 1996; STOC '96; arXiv:quant-ph/9605043.
- Verified: arXiv API.
- **Claim:** "the desired phone number can be obtained in only O(sqrt(N)) steps".
- **Lab:** QUERY-COMPLEXITY SPEEDUP (quadratic); ORACLE-MODEL RESULT.

**[C55] Strengths and Weaknesses of Quantum Computing (BBBV)**
- Bennett, Bernstein, Brassard, Vazirani; 1997; *SIAM J. Comput.* 26(5):1510–1523; DOI 10.1137/S0097539796300933; arXiv:quant-ph/9701001.
- Verified: arXiv API.
- **Claim:** relative to an oracle, "class NP cannot be solved on a quantum Turing machine in time o(2^{n/2})". This is the Ω(√N) lower bound for unstructured search.
- **Lab:** THEORETICAL (lower bound); ORACLE-MODEL RESULT.

**[C56] A Quantum Algorithm for Finding the Minimum**
- Dürr, Høyer; 1996; arXiv:quant-ph/9607014 (journal_ref not listed).
- Verified: arXiv API.
- **Claim:** finds the minimum index "in time O(c sqrt N)".
- **Lab:** QUERY-COMPLEXITY SPEEDUP (quadratic); ORACLE-MODEL RESULT.

### 2G. Quantum backtracking, branch-and-bound, dynamic programming

**[C57] Quantum-walk speedup of backtracking algorithms**
- Montanaro; 2018; *Theory of Computing* 14(15), 1–24; arXiv:1509.02374.
- Verified: arXiv API; theoryofcomputing.org/articles/v014a015 (search listing).
- **Claim:** "quantum algorithm which completes the same task using O(sqrt(T) n^(3/2) log n) tests" versus T classical tests. Also "for certain distributions on the inputs, the algorithm can lead to an exponential reduction in expected runtime".
- **Res:** the predicate and the branching heuristic must be implemented as reversible, coherent circuits.
- **Lab:** QUERY-COMPLEXITY SPEEDUP (near-quadratic in tree size T); THEORETICAL.

**[C58] Quantum algorithm for tree size estimation, with applications to backtracking and 2-player games**
- Ambainis, Kokainis; 2017; STOC 2017; DOI 10.1145/3055399.3055444; arXiv:1704.06774.
- Verified: arXiv API.
- **Claim:** "transform a classical backtracking search algorithm … into an Õ(√T n^{3/2}) time quantum algorithm" (for the explored subtree, when the classical algorithm stops early).
- **Lab:** THEORETICAL SPEEDUP (near-quadratic).

**[C59] Improved quantum backtracking algorithms using effective resistance estimates**
- Jarret, Wan; 2018; *PRA* 97, 022337; DOI 10.1103/PhysRevA.97.022337; arXiv:1711.05295.
- Verified: arXiv API.
- **Claim:** "achieves the conjectured bound of Õ(√T R_max) for finding a single marked vertex".
- **Lab:** THEORETICAL SPEEDUP.

**[C60] Quantum speedup of branch-and-bound algorithms**
- Montanaro; 2020; *PRR* 2, 013056; DOI 10.1103/PhysRevResearch.2.013056; arXiv:1906.10375.
- Verified: arxiv.org/abs/1906.10375.
- **Claim:** "accelerate classical branch-and-bound algorithms near-quadratically in a very general setting". Also "can find exact ground states for most instances of the Sherrington-Kirkpatrick model in time O(2^{0.226n}), which is substantially more efficient than Grover's algorithm."
- **Res:** coherent bounding-function and branching oracles; fault tolerance.
- **Comp:** the same classical B&B (the speedup is relative to that algorithm's tree).
- **Lab:** THEORETICAL SPEEDUP; ASYMPTOTIC SPEEDUP (near-quadratic, relative to classical B&B).

**[C61] Universal Quantum Speedup for Branch-and-Bound, Branch-and-Cut, and Tree-Search Algorithms**
- Chakrabarti, Minssen, Yalovetzky, et al.; 2022; arXiv:2210.03210.
- Verified: arXiv API.
- **Claim:** "near-quadratic speedup over classical Branch-and-Bound algorithms for every input", with complexity Õ(√Q d).
- **Lab:** THEORETICAL SPEEDUP (near-quadratic).

**[C62] Quantum Speedups for Exponential-Time Dynamic Programming Algorithms**
- Ambainis, Balodis, Iraids, Kokainis, Prūsis, Vihrovs; 2019; SODA 2019; arXiv:1807.05209.
- Verified: arxiv.org/abs/1807.05209 (search listing plus University of Latvia record).
- **Claim (from the listing):** "path in the hypercube" problem solved "in time O*(1.817^n)" by combining Grover search with partial DP tables. The classical DP baseline is O*(2^n), for example for TSP.
- **Lab:** THEORETICAL SPEEDUP (polynomial, sub-quadratic: 1.817^n versus 2^n); QRAM-type assumptions apply (see the paper).

### 2H. Fault-tolerant resource estimates and "quadratic is not enough"

**[C63] Applying quantum algorithms to constraint satisfaction problems**
- Campbell, Khurana, Montanaro; 2019; *Quantum* 3, 167; DOI 10.22331/q-2019-07-18-167; arXiv:1810.05582.
- Verified: arxiv.org/abs/1810.05582.
- **Claim:**
  - "In the most optimistic parameter regime we consider, this could be a factor of over 10^5 relative to a classical desktop computer; in the least optimistic regime, the speedup is reduced to a factor of over 10^3."
  - "the number of physical qubits used is extremely large"
  - "the quantum advantage disappears if one includes the cost of the classical processing power required to perform decoding of the surface code using current techniques."
- **Set:** random k-SAT and graph colouring; Grover and backtracking.
- **Lab:** resource estimate; THEORETICAL SPEEDUP; ADVANTAGE DISPUTED (by its own decoding caveat).

**[C64] Compilation of Fault-Tolerant Quantum Heuristics for Combinatorial Optimization**
- Sanders, Berry, Costa, et al.; 2020; *PRX Quantum* 1, 020312; DOI 10.1103/PRXQuantum.1.020312; arXiv:2007.07391.
- Verified: arxiv.org/abs/2007.07391.
- **Claim (abstract):**
  - "Our results discourage the notion that any quantum optimization heuristic realizing only a quadratic speedup will achieve an advantage over classical algorithms on modest superconducting qubit surface code processors without significant improvements in the implementation of the surface code."
  - "quantum accelerated simulated annealing would require roughly a day and a million physical qubits to optimize spin glasses that could be solved by classical simulated annealing in about four CPU-minutes."
- **Res:** surface code; compiled Szegedy and qubitized walks, adiabatic methods, QAOA and population transfer.
- **Lab:** resource estimate; NO ADVANTAGE (for quadratic heuristics).

**[C65] Focus beyond quadratic speedups for error-corrected quantum advantage**
- Babbush, McClean, Newman, Gidney, Boixo, Neven; 2021; *PRX Quantum* 2, 010103; DOI 10.1103/PRXQuantum.2.010103; arXiv:2011.04149.
- Verified: arxiv.org/abs/2011.04149.
- **Claim:** "quadratic speedups will not enable quantum advantage on early generations of such fault-tolerant devices unless there is a significant improvement in how we would realize quantum error-correction … quartic speedups look significantly more practical."
- **Lab:** NO ADVANTAGE (for quadratic speedups on early fault-tolerant hardware).

**[C66] Disentangling Hype from Practicality: On Realistically Achieving Quantum Advantage**
- Hoefler, Häner, Troyer; 2023; *CACM* 66(5):82–87; DOI 10.1145/3571725; arXiv:2307.00523.
- Verified: arXiv API plus DBLP/ACM listing.
- **Claim:** "small data problems and quantum algorithms with super-quadratic speedups are essential".
- **Lab:** perspective; NO ADVANTAGE (for quadratic, big-data problems).

**[C67] End-to-end resource analysis for quantum interior point methods and portfolio optimization**
- Dalzell, Clader, Salton, et al.; 2023; *PRX Quantum* 4, 040325; DOI 10.1103/PRXQuantum.4.040325; arXiv:2211.12489.
- Verified: arXiv API.
- **Claim:** "fundamental improvements to the QIPM are required for it to lead to practical quantum advantage". Large constant prefactors and tomography cost are the reasons.
- **Lab:** resource estimate; NO ADVANTAGE.

**[C68] Quantum algorithms: A survey of applications and end-to-end complexities**
- Dalzell, McArdle, Berta, et al.; Cambridge University Press 2025; DOI 10.1017/9781009639651; arXiv:2310.03011.
- Verified: arXiv API.
- **REVIEW (orientation).** Its combinatorial-optimization chapters are the standard end-to-end reference.

### 2I. Super-quadratic or structured primitives

**[C69] A Short Path Quantum Algorithm for Exact Optimization**
- Hastings; 2018; *Quantum*; arXiv:1802.10124.
- Verified: arXiv API.
- **Claim:** "provably outperforms Grover's algorithm assuming a mild condition on the number of low energy states".
- **Lab:** THEORETICAL SPEEDUP (super-Grover by an exponentially small margin in the exponent).

**[C70] Mind the gap: Achieving a super-Grover quantum speedup by jumping to the end**
- Dalzell, Pancotti, Campbell, Brandão; 2023; STOC 2023; DOI 10.1145/3564246.3585203; arXiv:2212.01513.
- Verified: arXiv API.
- **Claim:** "finds the optimal solution in time O*(2^{(0.5−c)n}), a 2^{cn} advantage over Grover's algorithm". The constant c is small; the setting is Ising-type spin-glass optimization.
- **Lab:** THEORETICAL SPEEDUP (super-Grover). Still exponential time, and c is tiny.

**[C71] Quartic quantum speedups for planted inference**
- Schmidhuber, O'Donnell, Kothari, Babbush; 2025; *PRX* 15, 021077; DOI 10.1103/PhysRevX.15.021077; arXiv:2406.19378.
- Verified: arxiv.org/abs/2406.19378.
- **Claim:** "a quantum algorithm for the Planted Noisy kXOR problem … that achieves a nearly quartic (4th power) speedup over the best known classical algorithm while also only using logarithmically many qubits". The speedup relies on planted problems instantiating "the Guided Sparse Hamiltonian problem".
- **Lab:** THEORETICAL SPEEDUP; ASYMPTOTIC SPEEDUP (relative to the best known classical algorithm, the Kikuchi spectral method).

**[C72] Classical and Quantum Algorithms for Tensor Principal Component Analysis**
- Hastings; 2020; *Quantum* 4, 237; DOI 10.22331/q-2020-02-27-237; arXiv:1907.12724.
- Verified: arXiv API.
- **Claim:** "The quantum algorithm achieves a quartic speedup while using exponentially smaller space than the fastest classical spectral algorithm".
- **Lab:** THEORETICAL SPEEDUP.

**[C73] Optimization by Decoded Quantum Interferometry (DQI)**
- Jordan, Shutty, Wootters, et al.; 2025; *Nature* 646:831–836; DOI 10.1038/s41586-025-09527-5; arXiv:2408.08292.
- Verified: arXiv API.
- **Claim:** "DQI achieves a superpolynomial speedup over known classical algorithms" for optimal polynomial intersection (OPI).
- **Set:** structured algebraic problems (Reed–Solomon-decodable).
- **Lab:** THEORETICAL SPEEDUP (relative to known classical algorithms); no protein-type structure.

**[C74] Quantum Simulated Annealing**
- Somma, Boixo, Barnum, Knill; 2008; arXiv:0712.1008.
- Verified: arXiv API.
- **Claim:** complexity "scales with the inverse of the square root of the minimum spectral gap" versus classical "inverse of the gap".
- **Lab:** THEORETICAL SPEEDUP (quadratic in the gap). Detailed in Domain D; see [C64] for the fault-tolerant cost.

### 2J. Reviews and benchmarking frameworks

**[C75] Challenges and Opportunities in Quantum Optimization**
- Abbas, Ambainis, Augustino, et al.; 2024; *Nat. Rev. Phys.*; DOI 10.1038/s42254-024-00770-9; arXiv:2312.02279.
- Verified: arXiv API.
- **REVIEW (orientation).** It covers problem classes and benchmarking metrics and makes no single speedup claim.

**[C76] Quantum Optimization Benchmarking Library — The Intractable Decathlon**
- Koch, Bernal Neira, Chen, et al.; 2026; *Nat. Comput. Sci.* 6, 653–671; DOI 10.1038/s43588-026-00991-1; arXiv:2504.03832.
- Verified: arXiv API.
- Provides a framework for "systematic, fair, and comparable benchmarks".
- **REVIEW/benchmark infrastructure.**

### 2K. Classical state of the art for rugged landscapes

**[C77] Exchange Monte Carlo Method and Application to Spin Glass Simulations (parallel tempering)**
- Hukushima, Nemoto; 1996; *J. Phys. Soc. Jpn.* 65, 1604; DOI 10.1143/JPSJ.65.1604; arXiv:cond-mat/9512035.
- Verified: arXiv API.
- **Claim:** "The ergodicity time in this method is found much smaller than that of the multi-canonical method."
- **Lab:** classical baseline.

**[C78] Comparing Monte Carlo methods for finding ground states of Ising spin glasses: population annealing, simulated annealing, and parallel tempering**
- Wang, Machta, Katzgraber; 2015; *PRE* 92, 013303; DOI 10.1103/PhysRevE.92.013303; arXiv:1412.2104.
- Verified: arXiv API.
- **Claim:** "population annealing Monte Carlo is significantly more efficient than simulated annealing but comparable to parallel tempering."
- **Lab:** classical baseline. SA is a weak comparator.

**[C79] Efficient Cluster Algorithm for Spin Glasses in Any Space Dimension (Houdayer/ICM generalization)**
- Zhu, Ochoa, Katzgraber; 2015; *PRL* 115, 077201; DOI 10.1103/PhysRevLett.115.077201; arXiv:1501.05630.
- Verified: arXiv API.
- **Claim:** "speeds up thermalization by at least one order of magnitude".
- **Lab:** classical baseline. PT-ICM is the comparator in [C44].

### 2L. Protein-specific: complexity, classical exact solvers, quantum optimization attempts

**[C80] Protein folding in the hydrophobic-hydrophilic (HP) model is NP-complete**
- Berger, Leighton; 1998; *J. Comput. Biol.* 5(1):27–40; DOI 10.1089/cmb.1998.5.27.
- Verified: journals.sagepub.com listing plus ACM DL (search).
- **Claim:** the 3D cubic-lattice HP folding problem is NP-complete.
- **Lab:** THEORETICAL (worst-case hardness). This does not imply that typical instances are hard.

**[C81] Protein Design is NP-hard**
- Pierce, Winfree; 2002; *Protein Eng.* 15(10):779–782; DOI 10.1093/protein/15.10.779.
- Verified: academic.oup.com / PubMed 12468711 (search).
- **Claim:** fixed-backbone, pairwise-energy design (which includes rotamer choice) is NP-hard.
- **Lab:** THEORETICAL (worst case).

**[C82] A new framework for computational protein design through cost function network optimization**
- Traoré, Allouche, André, et al.; 2013; *Bioinformatics* 29(17):2129–2136; DOI 10.1093/bioinformatics/btt374.
- Verified: dx.doi.org / OUP (search).
- **Claim:** exact weighted-CSP (toulbar2) solving of CPD. It addresses the NP-hard combinatorial core and reports large practical speedups over DEE/A*-type exact methods (from the abstract's framing; exact factors not recorded here).
- **Lab:** classical baseline (exact).

**[C83] Rapid Protein Side-Chain Packing via Tree Decomposition**
- Xu; 2005; RECOMB 2005, LNCS 3500; DOI 10.1007/11415770_32.
- Verified: link.springer.com chapter listing (search).
- **Claim:** "can obtain the globally optimal solution of the side-chain packing problem very efficiently", exploiting the small treewidth of residue interaction graphs.
- **Lab:** classical baseline (exact, structure-exploiting).

**[C84] Growth Algorithms for Lattice Heteropolymers at Low Temperatures (PERM variants)**
- Hsu, Mehra, Nadler, Grassberger; 2003; *J. Chem. Phys.* 118, 444–451; arXiv:cond-mat/0208042.
- Verified: arxiv.org/abs/cond-mat/0208042 listing (search).
- **Claim:** outperforms "all other stochastic algorithms which have been employed on this problem, except for … CG of Beutler & Dill"; "found new lowest energy states missed in previous papers".
- **Lab:** classical baseline (lattice proteins, including HP 64-mers and longer).

**[C85] CPSP-tools — Exact and complete algorithms for high-throughput 3D lattice protein studies**
- Mann, Will, Backofen; 2008; *BMC Bioinformatics* 9, 230; DOI 10.1186/1471-2105-9-230.
- Verified: api.semanticscholar.org (DOI lookup).
- **Claim:** exact, provably optimal structure prediction for 3D HP models (cubic and FCC) using constraint programming.
- **Lab:** classical baseline (exact).

**[C86] Finding low-energy conformations of lattice protein models by quantum annealing**
- Perdomo-Ortiz, Dickson, Drew-Brook, Rose, Aspuru-Guzik; 2012; *Sci. Rep.* 2, 571; DOI 10.1038/srep00571; arXiv:1204.5485.
- Verified: arXiv API plus nature.com listing (search).
- **Claim:** "first implementation of lattice protein folding on a quantum device under the Miyazawa-Jernigan model" (up to 81 qubits; 6-residue-class instances).
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**[C87] Coarse-grained lattice protein folding on a quantum annealer**
- Babej, Ing, Fingerhuth; 2018; arXiv:1811.00713.
- Verified: arXiv API.
- **Claim:** encoding complexity reduced "from quadratic to quasilinear"; Chignolin (10 residues) on D-Wave 2000Q.
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**[C88] Resource-Efficient Quantum Algorithm for Protein Folding**
- Robert, Barkoutsos, Woerner, Tavernelli; 2021; *npj QI* 7, 38; DOI 10.1038/s41534-021-00368-4; arXiv:1908.02163.
- Verified: arXiv API.
- **Claim:** Hamiltonian with "O(N⁴) scaling" in the number of terms; a 10-residue peptide on 22 qubits (CVaR-VQE).
- **Lab:** SIMULATOR RESULT + HARDWARE DEMONSTRATION; NO ADVANTAGE. This is the direct ancestor of the S29–S33 approach.

**[C89] Investigating the potential for a limited quantum speedup on protein lattice problems**
- Outeiral, Morris, Shi, et al.; 2021; *New J. Phys.*; DOI 10.1088/1367-2630/ac29ff; arXiv:2004.01118.
- Verified: arxiv.org/abs/2004.01118.
- **Claim:** "even naive quantum annealing, when applied to protein lattice folding, has the potential to outperform classical approaches". The work is a numerical study of simulated QA on "a large number of small peptide folding problems".
- **Lim:** closed-system simulation of small instances; the scaling is inferred from tiny sizes; the comparator is SA-type, not PERM or CPSP.
- **Lab:** SIMULATOR RESULT; HEURISTIC (potential, limited speedup); not an advantage over the classical state of the art.

**[C90] Folding lattice proteins with quantum annealing**
- Irbäck, Knuthson, Mohanty, Peterson; 2022; *PRR* 4, 043013; DOI 10.1103/PhysRevResearch.4.043013; arXiv:2205.06084.
- Verified: arXiv API.
- **Claim:** hybrid D-Wave "100% hit rate" on HP chains up to N=30; recovered "lowest known energies for N=48 and N=64 HP chains".
- **Lim:** hybrid solver (classical plus QPU; attribution unclear); it matches known classical optima rather than beating them.
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE.

**[C91] Using quantum annealing to design lattice proteins**
- Irbäck, Knuthson, Mohanty, Peterson; 2024; *PRR* 6, 013162; arXiv:2402.09069.
- Verified: arXiv API.
- **Claim:** the hybrid solver handles 30–64-mers. The pure QPU approach "confines us to sizes ≤20, due to exponentially decreasing success rates".
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE. The QPU-only success probability decays exponentially.

**[C92] Resource analysis of quantum algorithms for coarse-grained protein folding models**
- Linn, Brundin, García-Álvarez, Johansson, Rehn; 2024; *PRR* 6, 033112; DOI 10.1103/PhysRevResearch.6.033112; arXiv:2311.04186.
- Verified: arXiv API.
- **Claim:** "limiting factor is the high number of interactions in the Hamiltonian, resulting in quantum gate count unavailable today".
- **Lab:** resource estimate; NO ADVANTAGE (near term).

**[C93] A perspective on protein structure prediction using quantum computers**
- Doga, Raubenolt, Cumbo, et al.; 2024; *JCTC* 20, 3359–3378; DOI 10.1021/acs.jctc.4c00067; arXiv:2312.00875.
- Verified: arXiv API.
- **REVIEW/perspective (orientation).** Proposes criteria for problems "amenable for quantum advantage".

**[C94] Quantum Algorithm for Protein Side-Chain Optimisation: Comparing Quantum to Classical Methods**
- Agathangelou, Manawadu, Tavernelli, et al.; 2025; arXiv:2507.19383.
- Verified: arxiv.org/abs/2507.19383.
- **Claim:** rotamer QUBO to Ising, with QAOA; "Our quantum method demonstrates a reduction in computational cost compared to classical simulated annealing techniques".
- **Lim:** the comparator is SA, not DEE/A*, CFN [C82] or tree decomposition [C83]. It shows no scaling against exact rotamer solvers.
- **Lab:** SIMULATOR RESULT; weak baseline. It must not be read as advantage.

**[C95] Penalty-free quantum optimization applied to lattice protein folding**
- Gellersen, Irbäck, Knuthson, et al.; 2026; arXiv:2606.02104.
- Verified: arXiv API.
- **Claim:** a restricted-search-space QAOA variant; simulations at N=4 and 6; "lengths up to N=14 using local subgraphs with at most 26 qubits".
- **Lab:** SIMULATOR RESULT; NO ADVANTAGE claimed.

**[C96] Protein folding with an all-to-all trapped-ion quantum computer**
- Romero, Gomez Cadavid, Nikačević, et al.; 2025; arXiv:2506.07866.
- Verified: arXiv API.
- **Claim:** tetrahedral lattice "for up to 12 amino acids", 36 qubits on IonQ; "consistently achieves optimal solutions".
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE. Instances are tiny and classically trivial.

**[C97] Protein folding on a 64 qubit trapped-ion hardware via counterdiabatic quantum optimization**
- Gomez Cadavid, Nikačević, Chandarana, et al.; 2026; arXiv:2604.26861.
- Verified: arXiv API.
- **Claim:** 14–16-residue peptides mapped to 46–61 qubits with up to 5-body terms; BF-DCQO "reaches the classical reference energy in multiple instances"; "improves over the corresponding random-seeded pipeline".
- **Lab:** HARDWARE DEMONSTRATION; NO ADVANTAGE. It does not always reach the classical optimum, and the comparator is a random-seeded pipeline.

**[C98] Exploring Quantum Annealing for Coarse-Grained Protein Folding**
- Scheiber, Heller, Giebel, et al.; 2026; *Sci. Rep.*; DOI 10.1038/s41598-026-46916-w; arXiv:2508.10660.
- Verified: arXiv API.
- **Claim:** "current quantum annealing hardware is not yet suited for tackling problems beyond proof-of-concept", while reporting a "scaling advantage over our in-house simulated annealing implementation".
- **Lab:** HARDWARE DEMONSTRATION; weak baseline; NO ADVANTAGE (by its own summary).

**Total verified: 98 entries.** Of these, 5 are reviews or perspectives used for orientation only: [C21], [C68], [C75], [C76], [C93].

---

## 3. Primitive analyses (16 questions each)

### P1. QAOA and QAOA+ (constant or low depth, NISQ)

1. **Operation.** Prepares |γ,β⟩ = Π e^{−iβ_k B} e^{−iγ_k C}|+⟩ and samples bitstrings. Classical outer-loop parameter training, or fixed transferred parameters.
2. **Replaces.** A randomized heuristic for min C(x) or approximate optimization, such as SA, tabu or local search.
3. **Why hard classically.** Only when the landscape is glassy (OGP, exponentially many local minima). For many instances it is not hard, and S29–S33 found it not hard at the relevant sizes.
4. **Exact speedup.** No provable speedup on natural problems.
   - Oracle separation on contrived near-symmetric problems: O(1) versus Ω(n/log n) queries [C17].
   - The p=11 approximation-ratio advantage on large-girth graphs holds only in the D→∞ limit [C14].
   - Constant or low depth is provably limited: OGP [C12], [C13], [C15], [C16]; symmetry [C9]; local classical algorithms match [C8], [C10], [C11].
5. **Metric.** Approximation ratio or success probability per shot. Query separation only in [C17].
6. **Assumptions.** Noiseless gates for any positive result. Noise kills advantage at depth L = O(1/p) [C25], [C26].
7. **Oracle.** A phase oracle for C(x). For protein energies this is a k-body diagonal Hamiltonian. For lattice folding, [C88] needs O(N⁴) terms.
8. **Oracle cost.** Per layer, gates ∝ number of Hamiltonian terms (O(N⁴) for [C88]; up to 5-body terms for [C97]). [C92] finds that the gate count is "unavailable today".
9. **State preparation.** Trivial (|+⟩^n), or a feasible-subspace state for QAOA+ [C2].
10. **Readout.** Computational-basis shots. The cost is 1/P(x*) shots. P(x*) decays exponentially in N for fixed p ([C19], [C33]).
11. **Classical post-processing.** Evaluate C(x) per shot and take the argmin. This is the S29–S33 readout, and a classical sampler with equal budget reproduces it (H-001).
12. **Strongest classical.** Problem-dependent:
    - Goemans–Williamson (MaxCut);
    - PT, PT-ICM, population annealing [C77]–[C79];
    - MTS (LABS) [C30];
    - Gurobi and B&B;
    - for protein problems: PERM [C84], CPSP [C85], DEE/A*, CFN [C82], tree decomposition [C83].
13. **Survives?** No, at constant or low depth. At high depth the only evidence is small-N simulation (below).
14. **Fault tolerance?** Needed for any depth where QAOA might help, and needed for QAOA+QMF.
15. **Resources.**
    - Guerreschi–Matsuura: "several hundreds of qubits" for MaxCut speedup [C18].
    - Lykov: exponential sample count for p ≤ 11 [C19].
    - Sanders: QAOA compiled among other heuristics; no quadratic heuristic pays off on modest surface codes [C64].
16. **Protein mapping.**
    - Lattice folding: HP/MJ on a cubic or tetrahedral lattice [C86]–[C91], [C95]–[C97].
    - Rotamer QUBO [C94].
    - Contact or fragment registers (S29–S33).
    - The mapping is natural in form, but the instances are tiny (≤ 16 residues on hardware), and exact classical solvers are strong.

### P2. VQE, CVaR-VQE and ADAPT applied to classical (diagonal) cost functions

1. **Operation.** Parameterized ansatz U(θ). Minimizes ⟨C⟩ or CVaR_α(C) of sampled diagonal energies. ADAPT grows U greedily.
2. **Replaces.** Stochastic search over bitstrings.
3. **Why hard classically.** Same as P1.
4. **Exact speedup.** None. For a diagonal C, the optimum of any such objective is a distribution concentrated on argmin C. The circuit is a parameterized classical sampler with trainability pathologies:
   - barren plateaus [C20]–[C22];
   - NP-hard training [C23];
   - trap-swamped landscapes [C24].
5. **Metric.** Not applicable.
6. **Assumptions.** Trainable, non-simulable ansatz. Per [C22], provable trainability often coincides with classical simulability.
7. **Oracle.** The diagonal cost evaluated on samples. No quantum oracle is needed.
8. **Oracle cost.** Classical evaluation per shot.
9. **State preparation.** An ansatz of depth d.
10. **Readout.** Shots × iterations × parameters. This is the dominant cost.
11. **Post-processing.** CVaR tail or argmin. In S29–S33 it is the prefix of the energy order (theorem T1) and has a closed-form p* (H-001, DNR-01).
12. **Strongest classical.** Any sampler over x with the same objective, including a closed-form Gibbs or hinge minimizer. Also SA, greedy, exact enumeration (≤ 2^24) and DP for chain-structured costs.
13. **Survives?** No. ADAPT-VQE [C3] and ADAPT-QAOA [C4] are compared only against other quantum ansätze. CVaR [C6] is compared only against expectation-value VQE.
14. **Fault tolerance.** Not the issue.
15. **Resources.** Not applicable. Robert et al. [C88] use 22 qubits for 10 residues.
16. **Protein mapping.** The same encodings as P1. **Directly tested in S29–S33 (33 or 34 experiments; null).**

### P3. Quantum annealing (analog; including QAC and counterdiabatic or digitized variants)

1. **Operation.** Interpolates H(s) = A(s)H_driver + B(s)H_problem and reads out low-energy states. Variants are:
   - QAC: embedded repetition code with penalty [C44];
   - DCQO / BF-DCQO: digitized counterdiabatic evolution with bias feedback [C36], [C97].
2. **Replaces.** SA, PT or PT-ICM, SQA, SBM.
3. **Why hard classically.** Spin-glass ground states and low-energy sampling on frustrated instances. Many benchmark classes turned out to be classically easy ([C39], [C41], [C52]).
4. **Exact speedup.** No provable speedup. Empirical claims:
   - over SA only [C42], [C51];
   - constant factor over all classical heuristics, no scaling gain [C43];
   - scaling over PT-ICM for approximate optimization at a ≥ 1% gap [C44], disputed by SBM showing "comparable or superior scaling" [C45] and by runtime accounting [C46].
5. **Metric.** TTS or time-to-epsilon, with optimal annealing time required for a valid scaling claim ([C38], [C42]).
6. **Assumptions.** Analog control precision, native connectivity, and an embedding overhead that grows with the problem.
7. **Oracle.** Native two-local Ising only. Higher-order protein terms need gadgets or ancillas, which cost qubits ([C86], [C87], [C92]).
8. **Oracle cost.** Embedding: chains of physical qubits per logical variable. QAC multiplies qubits further.
9. **State preparation.** Ground state of the driver.
10. **Readout.** Many anneals × 1/P_success. For QPU-only lattice design, success decays exponentially ("sizes ≤20" [C91]).
11. **Post-processing.** Energy evaluation, and often classical polishing. Hybrid solvers obscure attribution [C90], [C91].
12. **Strongest classical.**
    - Spin glasses: PT-ICM [C79], population annealing [C78], SBM [C45], tensor networks for dynamics [C49], [C50].
    - Lattice proteins: PERM [C84], CPSP exact [C85].
13. **Survives?** Not robustly. No undisputed scaling advantage exists in exact optimization. The approximate-optimization claim [C44] is contested [C45], [C46]. Nothing exists for protein problems.
14. **Fault tolerance.** Analog annealers have no full fault tolerance, and QAC gives only partial error suppression.
15. **Resources.**
    - Munoz-Bauza & Lidar: "over 1,300 error-suppressed logical qubits" [C44].
    - Protein demonstrations: ≤ 81 qubits [C86].
    - Hybrid solvers reach up to 64-mers [C90], [C91], but attribution to the QPU is unclear.
16. **Protein mapping.** Lattice folding (HP/MJ) [C86], [C89]–[C91], [C98]; lattice design [C91]; rotamer QUBO (in principle). Only coarse lattice models map natively, and these proxy energies fail condition C in the S29–S33 program (DE-8).

### P4. Grover search, amplitude amplification, Dürr–Høyer minimum finding

1. **Operation.** Amplitude amplification of a marked set in an N-element space, or iterated threshold search for the minimum.
2. **Replaces.** Exhaustive search or random restarts.
3. **Why hard classically.** Only unstructured spaces are hard in this sense. Structured problems admit much better classical algorithms (DP, B&B, local search).
4. **Exact speedup.** Θ(√N) versus Θ(N) queries, and this is optimal: BBBV Ω(√N) [C54]–[C56]. For NP-type search, o(2^{n/2}) quantum time is impossible relative to an oracle [C55].
5. **Metric.** Query complexity. It translates to runtime only if each coherent oracle call has a cost comparable to a classical evaluation, which it does not under fault tolerance.
6. **Assumptions.** A coherent oracle, a known or estimated number of marked items, and no exploitable structure beyond what the oracle hides.
7. **Oracle.** A reversible circuit computing E(x) and comparing it to a threshold. For protein search this means the energy, and potentially the whole decoder (L-BFGS, DG), must run reversibly.
8. **Oracle cost.** High. Arithmetic energy evaluation costs thousands to millions of T gates, per the compilation patterns in [C64]. A reversible continuous optimizer inside the oracle is far larger still.
9. **State preparation.** Uniform superposition, or a heuristic distribution (amplitude amplification of a sampler).
10. **Readout.** O(1) measurements plus verification.
11. **Post-processing.** Verify E(x).
12. **Strongest classical.** Exploit structure: DP (S-7), B&B, CFN, tree decomposition, local search. Exhaustive search is never the baseline for protein subproblems.
13. **Survives?** Asymptotically in the query model, yes. In wall-clock time it fails against the fault-tolerant overhead: "quadratic speedups will not enable quantum advantage on early generations" [C65]; the SA analogue needs "a day and a million physical qubits" versus "four CPU-minutes" [C64]; see also [C66].
14. **Fault tolerance.** Required.
15. **Resources.** Campbell–Khurana–Montanaro give speedup factors of 10^3–10^5 for day-long k-SAT instances, which "disappears" once decoder classical cost is included [C63].
16. **Protein mapping.** Amplitude-amplified restarts of a decoder (AA-2), and search over fragment or rotamer spaces. S29–S33 shows that 32–64 restarts saturate at 44–60 aa, so the best case is roughly √64 = 8 coherent decoder runs instead of 64 classical ones. That is a ≤ 8× reduction in decoder evaluations, against a per-evaluation fault-tolerant slowdown of many orders of magnitude.

### P5. Quantum backtracking and branch-and-bound (quantum-walk tree search)

1. **Operation.** A quantum walk on the classical search tree (Belovs-style electrical-network walk), plus tree-size estimation. The B&B variant interleaves bound estimation.
2. **Replaces.** Classical backtracking (for CSPs) or B&B (for exact optimization) with the same branching and bounding rules.
3. **Why hard classically.** The tree size T grows exponentially on hard instances.
4. **Exact speedup.**
   - O(√T n^{3/2} log n) versus T [C57].
   - Õ(√T n^{3/2}) when the classical algorithm stops early [C58].
   - Õ(√(T R_max)) [C59].
   - B&B near-quadratic: SK ground states in O(2^{0.226n}) [C60].
   - "Universal" near-quadratic Õ(√Q d) [C61].
   - DP-type problems: O*(1.817^n) versus O*(2^n) [C62].
   - Exponential gain only for special input distributions [C57].
5. **Metric.** Queries to the predicate and heuristic oracles. Time follows only under a coherent-oracle cost model.
6. **Assumptions.** Reversible, coherent implementations of the branching heuristic and bounding function. The speedup is relative to the same classical tree; a better classical pruning rule changes T for both.
7. **Oracle.** Predicate P(partial assignment) and heuristic h. For rotamer or contact CSPs these are pairwise-energy bounds or constraint checks.
8. **Oracle cost.** Moderate for simple CSP predicates (k-SAT in [C63]). High for LP-relaxation bounds (B&C, [C61]) or DEE-type bounds.
9. **State preparation.** Root of the tree.
10. **Readout.** Repeated walk phase estimation; logarithmic overheads.
11. **Post-processing.** Reconstruct and verify the solution.
12. **Strongest classical.**
    - Rotamers: DEE/A*, CFN (toulbar2) [C82], tree decomposition exploiting small treewidth [C83].
    - Lattice folding: CPSP exact [C85].
    - SAT: modern CDCL solvers, whose learned clauses do not fit the static-tree model.
13. **Survives?** On paper, versus the same tree, yes. In practice it survives only if the classical tree is astronomically large but still within a fault-tolerant runtime budget, and if no classical algorithm shrinks the tree. [C63] shows that even this favourable case evaporates once decoding costs are included.
14. **Fault tolerance.** Required.
15. **Resources.** [C63]: extremely large physical-qubit counts for 10^3–10^5 factors on day-long instances, erased by decoder cost. No protein-specific estimate exists (gap).
16. **Protein mapping.**
    - Rotamer or branch selection (C-4) as a weighted CSP.
    - Contact-constraint satisfaction as a CSP.
    - Discrete fragment assembly as a tree search.
    - The mapping is natural. But classical exact solvers already handle protein-size rotamer problems through structure (small treewidth), and C-4 is discrimination-limited (96% order-statistic dominated at short length).

### P6. Quantum-accelerated Markov-chain heuristics used as optimizers (QSA, Szegedy/qubitized walks, amplitude-amplified SA or PT restarts)

1. **Operation.** Quantizes the Markov chain and moves along the annealing path with a √(1/δ) cost [C74]. Alternatively amplifies the success probability of a classical heuristic run.
2. **Replaces.** SA, PT, MTS.
3. **Why hard classically.** A small spectral gap δ, or a small success probability p per run.
4. **Exact speedup.** Quadratic in 1/δ or 1/p.
5. **Metric.** Walk steps.
6. **Assumptions.** A coherent Metropolis walk operator.
7. **Oracle.** A reversible energy difference plus acceptance-probability arithmetic.
8. **Oracle cost.** The dominant cost; compiled in detail in [C64].
9. **State preparation.** Coherent encoding of the initial distribution.
10. **Readout.** Standard.
11. **Post-processing.** Standard.
12. **Strongest classical.** PT-ICM, population annealing, SBM, MTS.
13. **Survives?** No for modest fault-tolerant hardware: "roughly a day and a million physical qubits … solved by classical simulated annealing in about four CPU-minutes" [C64]. The LABS paper [C28] itself notes that MTS could be accelerated this way. That would put the quantum-accelerated classical heuristic at roughly 1.34^{N/2} ≈ 1.16^N (my arithmetic, not a published figure), which would beat QAOA+QMF's 1.21^N, so QAOA would not be the relevant quantum algorithm.
14. **Fault tolerance.** Required.
15. **Resources.** [C64] as above.
16. **Protein mapping.** Search or sampling on discrete or discretized conformations. The sampling version (C-1, SP-1, AA-1) belongs to Domain D and is the program's rank-2 item. The optimization version is dominated by restart saturation (C-2).

### P7. Super-quadratic structured primitives (short path, jump to the end, Kikuchi/planted inference, tensor PCA, DQI)

1. **Operation.**
   - Short path and jump-to-end: a Hamiltonian path with a gap guarantee at the endpoints [C69], [C70].
   - Kikuchi/planted: phase estimation or a guided sparse Hamiltonian on a Kikuchi matrix [C71], [C72].
   - DQI: a quantum Fourier transform plus classical decoding of an algebraic code [C73].
2. **Replaces.** Exhaustive or Grover search [C69], [C70]; classical spectral algorithms for planted inference [C71], [C72]; classical algorithms for OPI [C73].
3. **Why hard classically.** Exponential search; spectral methods need large Kikuchi levels (memory and time n^ℓ); algebraic decoding hardness.
4. **Exact speedup.**
   - 2^{(0.5−c)n} with small c [C70].
   - Super-Grover under a condition on low-energy counts [C69].
   - Nearly quartic, versus the best known classical algorithm [C71], [C72].
   - Superpolynomial versus known classical algorithms, for OPI [C73].
5. **Metric.** Time, relative to the best known classical algorithm (not proven lower bounds, except in the oracle setting).
6. **Assumptions.** Planted structure with a signal strength between the information-theoretic and computational thresholds [C71], [C72]; algebraic structure [C73]; Ising-type spin-glass cost [C70].
7. **Oracle.** A sparse Hamiltonian or matrix access to the problem data.
8. **Oracle cost.** Moderate, since the problems have explicit sparse structure.
9. **State preparation.** A guiding state, which the planted problem provides [C71].
10. **Readout.** Phase estimation.
11. **Post-processing.** Classical decoding or rounding.
12. **Strongest classical.** The Kikuchi spectral method, or the best known decoders.
13. **Survives?** Theoretically yes, relative to known classical algorithms. There are no end-to-end protein-relevant instances.
14. **Fault tolerance.** Required.
15. **Resources.** [C71] uses "logarithmically many qubits", which is attractive, but no protein-type resource estimate exists.
16. **Protein mapping.** Not natural. Contact-map or structure inference from noisy restraints is a planted-inference problem in spirit. But the known quartic speedups need the kXOR/tensor structure and the regime between the information-theoretic and computational thresholds (information present, but classically hard to extract). S29–S33 showed the inherited endpoint is **information-limited** (I-1 … I-5), which is below the information threshold, where no algorithm (classical or quantum) can succeed.

### P8. Quantum-seeded classical hybrids (QE-MTS, BF-DCQO/HSQC, QAOA warm starts)

1. **Operation.** Short quantum evolutions produce seeds or bias fields for a classical metaheuristic.
2. **Replaces.** Random seeds for MTS or tabu.
3. **Why hard classically.** Same as P1.
4. **Exact speedup.** Empirical only: 1.24^N versus 1.34^N for N ∈ [27, 37], simulated [C29].
5. **Metric.** TTS.
6. **Assumptions.** Extrapolation from N ≤ 37. A crossover is projected at N ≳ 47 [C29].
7. **Oracle.** Diagonal cost.
8. **Oracle cost.** Diagonal-cost circuit per layer, as in P1.
9. **State preparation.** Trivial.
10. **Readout.** Samples.
11. **Post-processing.** A full classical metaheuristic (which dominates the compute).
12. **Strongest classical.** GPU MTS reaches N ≤ 120 and finds new records [C30]; enhanced PT and GPU ABS3 [C37].
13. **Survives?** Not demonstrated end-to-end. The hardware-runtime versions are disputed [C46]. The HSQC benchmark's own abstract reports that the strongest classical solvers "matched or exceeded" the quantum results [C37].
14. **Fault tolerance.** Claimed to be NISQ.
15. **Resources.** 36–64 trapped-ion qubits for 12–16-residue lattice folding [C96], [C97].
16. **Protein mapping.** Lattice folding [C96], [C97]. These are 12–16 residues, far below the 44–60 aa scale at which the program's classical continuous decode already saturates.

---

## 4. Strongest classical counterarguments (with citations)

1. **Locality and OGP barrier for shallow QAOA.**
   - Constant or log-depth QAOA "needs to see the whole graph" [C12], [C13].
   - It is bounded away from optimum on q≥4 spin glasses [C15], and on OGP CSPs for any local algorithm [C16].
   - Symmetry protection makes it lose to Goemans–Williamson at any constant level [C9].
   - One-local and two-local classical algorithms match or beat low-p QAOA [C8], [C10], [C11].
2. **Noise barrier.** Noisy circuits beyond depth ~1/p are exponentially unlikely to beat efficient classical algorithms [C25], [C26].
3. **Trainability versus simulability dilemma.**
   - Barren plateaus [C20], [C21] and trap-swamped landscapes [C24].
   - NP-hard training [C23].
   - Where barren plateaus are provably absent, classical simulation is often possible [C22].
4. **Quadratic speedups do not pay under fault tolerance.** [C63]–[C66]. The single most important counterargument for Grover, minimum finding, backtracking, B&B and QSA:
   - "a day and a million physical qubits" versus "four CPU-minutes" [C64];
   - quadratic speedups "will not enable quantum advantage on early generations" [C65];
   - CSP advantage "disappears" once decoding is included [C63].
5. **Weak-baseline pattern in annealing and hybrid claims.** Claims made against SA ([C35], [C40], [C42], [C51], [C94], [C98]) collapse, or are disputed, against:
   - SQA [C42];
   - cluster algorithms [C41];
   - exact solvers [C52];
   - PT-ICM or population annealing [C78], [C79];
   - SBM [C45];
   - GPU metaheuristics [C30], [C37].
   The best current claim [C44] is directly contested by [C45] and [C46].
6. **Small-N extrapolation.**
   - LABS evidence: N ≤ 40 [C28]; N ≤ 37 [C29].
   - Protein-lattice evidence: ≤ 16 residues on hardware; 30–64 with hybrids.
   - "the small instances studied previously are insufficient to infer asymptotic behavior" [C45].
7. **Structure beats unstructured search for protein subproblems.**
   - Rotamer packing is NP-hard in the worst case [C81] but solved exactly in practice by CFN [C82] and tree decomposition [C83].
   - HP lattice folding is NP-complete [C80] but solved exactly by CPSP [C85] and near-optimally by PERM [C84].
   - A quantum speedup relative to Grover or backtracking on the naive tree is irrelevant when the classical algorithm uses a far smaller effective tree.
8. **Readout reduction (program-specific).** An argmin, prefix or convex consumption of a diagonal-energy distribution is classically reproducible (H-001; S29–S33 theorem T1 and closed-form p*). No result in this domain escapes this when the cost is diagonal and the output is an argmin.

---

## 5. Scaling statements (explicit asymptotics only; no inference from small numerics)

| Primitive | Statement | Source | Type |
|---|---|---|---|
| Unstructured search | Θ(√N) queries; Ω(2^{n/2}) for NP relative to an oracle | [C54], [C55] | query, tight |
| Minimum finding | O(√N) | [C56] | query |
| Backtracking | O(√T n^{3/2} log n) versus T | [C57] | query |
| Backtracking (early stop) | Õ(√T n^{3/2}) | [C58] | time (model) |
| Backtracking | Õ(√(T R_max)) | [C59] | query |
| Branch-and-bound | near-quadratic; SK ground state O(2^{0.226n}) | [C60] | time (model) |
| B&B / B&C | Õ(√Q d) | [C61] | time (model) |
| Exponential-time DP | O*(1.817^n) versus O*(2^n) | [C62] | time (QRAM model) |
| Super-Grover | O*(2^{(0.5−c)n}) | [C70] | time |
| Planted kXOR / tensor PCA | nearly quartic versus the best known classical | [C71], [C72] | time |
| QSA | ~1/√δ versus 1/δ | [C74] | walk steps |
| QAOA locality | p < c(d)·log n gives MIS ≤ 0.854·opt | [C12] | approximation |
| QAOA locality | (d−1)^{2p} < n^A gives ratio 1/2 on bipartite MaxCut | [C13] | approximation |
| QAOA constant p on q≥4 spin glasses | bounded away from optimum | [C15] | approximation |
| QAOA empirical (LABS, N ≤ 40) | TTS 1.46^N (p=12); 1.21^N with QMF; MTS 1.34^N; B&B 1.62^N | [C28] | empirical fit, simulator |
| QE-MTS (N 27–37) | TTS 1.24^N | [C29] | empirical fit, simulator |
| LR-QAOA | P(x*) ≈ 2^{−η(p)N+C} | [C33] | empirical fit |
| QAOA (p ≤ 11, MaxCut) | required samples grow exponentially in N | [C19] | empirical |
| QPU-only QA (lattice design) | success rate decays exponentially; limited to ≤ 20 | [C91] | empirical |
| Protein lattice Hamiltonian | O(N⁴) terms in residues N | [C88] | encoding size |

- **In residues.** No paper gives a quantum-versus-classical runtime scaling in residue number for a protein-relevant task. The only residue-indexed statements are encoding sizes ([C87] quasilinear, [C88] O(N⁴)) and exponentially decaying QPU success rates [C91].
- **Mixing time, temperature, precision.** Nothing in Domain C, apart from [C74] (gap) and [C44] (optimality gap ε ≥ 1%).

---

## 6. NISQ route versus fault-tolerant route

**NISQ route: QAOA, VQE/CVaR/ADAPT, annealing, DCQO hybrids.**
- **Theory:** [C9], [C12]–[C16], [C20]–[C26] bound what shallow or noisy circuits can do.
- **Empirics:** no undisputed scaling advantage over the strongest classical solvers on any problem ([C38]–[C46], [C52]). The best contemporary claim [C44] (approximate optimization, engineered 2D spin glasses) is contested [C45], [C46].
- **Protein demonstrations:** ≤ 16 residues on hardware [C96], [C97]; 64-mers only through hybrid solvers where the QPU contribution is not isolated [C90], [C91].
- **Verdict:** closed for protein search.

**Fault-tolerant route: Grover, minimum finding, backtracking, B&B, QSA, high-depth QAOA+QMF.**
- These are provable (query-model) speedups, but quadratic.
- End-to-end resource estimates [C63], [C64], [C67] and perspectives [C65], [C66] conclude that quadratic speedups do not produce runtime advantage on early fault-tolerant machines.
- QAOA+QMF (1.21^N) [C28] is itself a fault-tolerant algorithm whose edge over MTS depends on a Grover layer that MTS could also receive.
- **Super-quadratic fault-tolerant options** ([C69]–[C73]) exist only for structured or planted problems without protein mappings.
- **Verdict:** open in principle, but no protein-relevant instance is known where fault-tolerant optimization could beat the classical exact or heuristic state of the art within a practical runtime.

---

## 7. Protein mapping and connection to S29–S33

| Protein subproblem | Natural quantum primitive | Classical state of the art | Evidence | Assessment |
|---|---|---|---|---|
| Lattice or discrete conformational search (HP/MJ, fragment registers) | QA, QAOA, DCQO (P1, P3, P8); Grover (P4) | PERM [C84]; CPSP exact [C85]; SA/PT | Hardware ≤ 16 aa [C96], [C97]; hybrid ≤ 64 [C90], [C91]; simulated-QA scaling from tiny sizes [C89] | No advantage. Proxy energies fail condition C (DE-8) |
| Contact-constraint satisfaction | Backtracking (P5); Grover (P4) | DG plus restarts; CSP solvers; CPSP-type constraint programming | None found (gap) | Quadratic at best; no resource estimate |
| Rotamer or branch selection | QAOA [C94]; QA; backtracking/B&B (P5) | DEE/A*, CFN [C82], tree decomposition [C83] (exact) | [C94] beats only SA | Structure-exploiting classical methods remove the search bottleneck; C-4 is discrimination-limited |
| Continuous decode beyond 60 aa (discretized) | Amplitude-amplified restarts (P4/P6) | L-BFGS × 32–64 restarts (saturated) | S29–S33 QX-30 | At most √R fewer decoder calls, each needing a reversible decoder; dwarfed by fault-tolerant overhead |

**Why S29–S33 failed, as the literature predicts.**
1. **CVaR-VQE on diagonal costs is a classical sampler in disguise.** Barkoutsos [C6] and ADAPT [C3], [C4] compare only against quantum baselines. [C20]–[C24] predict training pathologies. The S31 closed-form p* is the program-specific instance of this. **Already tested; null.**
2. **Equal-tuned SA matching or beating VQE is the historical norm.** It is the same pattern as [C38]–[C43]. Stronger classical baselines (PT-ICM, population annealing, PERM, exact enumeration or DP) would widen the gap, not close it.
3. **Register energies did not transmit to chain accuracy** (ρ = −0.08). No optimization primitive, quantum or classical, can fix a cost whose argmin is not the target. Every speedup in this domain accelerates finding argmin C. None changes C.
4. **Restart saturation at 44–60 aa** (7.08 → 4.40 → 4.37 → 4.35 Å at 1/32/64/128 restarts; floor 4.21 Å). The search component is already solved classically. A quadratic reduction in restarts (64 → ~8 coherent runs) saves nothing measurable, and [C64] and [C65] show the fault-tolerant slowdown per coherent step is many orders of magnitude.

**What would be different (the conditions under which Domain C could matter).** All three would have to hold together:
- (i) a native-free discrete cost whose argmin transmits to accuracy (condition C);
- (ii) a measured classical search gap that grows with length, in the C-2 kill test at 80–150 aa, with PT, PERM and CFN-class baselines rather than SA;
- (iii) a primitive with a super-quadratic separation on that cost, or a quadratic one on instances whose classical runtime is days or more.

None of the three is established. (iii) has no known candidate for protein costs.

---

## 8. Literature gaps (novelty is not advantage)

1. **No fault-tolerant resource estimate for protein discrete search.** Nobody has published T-counts or logical-qubit counts for quantum backtracking or B&B on rotamer or contact CSPs, compared with toulbar2/CFN or tree-decomposition runtimes. [C63] (k-SAT, colouring) and [C64] (spin glasses) are the closest templates. Filling this gap would be novel, but on the evidence of [C63]–[C65] it would almost certainly be a negative (category-3/6) result.
2. **No residue-indexed quantum-versus-classical scaling study** against strong baselines (PERM, CPSP, PT). The existing studies ([C89], [C91], [C98]) use SA or tiny N.
3. **No study checks whether quantum-found low-energy states improve downstream structure accuracy**, rather than proxy lattice energy. This is exactly the transmission failure measured in S29–S33.
4. **No analysis of the treewidth or effective search-tree size T** of protein rotamer or contact problems in the regime where exact classical methods fail. Without it, the √T advantage cannot be sized.
5. **Planted-inference speedups have not been mapped to structure inference from noisy contacts or restraints** ([C71] invites this). Novel, but likely inapplicable because the endpoint is information-limited.
6. **LABS-type claims lack an independent check by a group with the strongest classical solvers.** The only verified responses are classical improvements [C30] and follow-on quantum-hybrid claims [C29], [C31]. I found no published direct rebuttal of [C28] (see §9).

---

## 9. Unverified leads (not cited as evidence)

- A direct peer-reviewed rebuttal of Shaydulin et al. [C28]. None found. The claim is qualified by the authors' own caveats and by [C30]. A 2026 preprint by Pšeničnik, Bošković et al. (arXiv:2607.09688, "Prioritizing Search Space Regions in the LABS Problem") exists (the arXiv API returned the title and authors), but I did not verify its content or conclusions.
- Bošković et al., the memetic tabu search reference for the 1.34^N scaling. It is known only as cited inside [C28] and [C29]; not verified here.
- Harrow/Wei and Hastings follow-ups on quantum speedups of MCMC for optimization. Not searched (Domain D).
- Specific DEE/A* (Desmet 1992; OSPREY) and Rosetta packer references. Not verified this session.
- King et al. 2022 *Nature Physics* (coherent QA in Ising chains), and the Hen et al. planted-solution benchmarking papers. Not verified.
- The *Quantum Mach. Intell.* publication details of [C29] (Springer page redirect; the DOI is taken from the search listing only).

---

## 10. Bottom-line verdicts per primitive

**P1 — QAOA/QAOA+ at constant or low depth (NISQ): KILLED.** Provable locality, OGP and symmetry limits [C9], [C12]–[C16]. Local classical algorithms match it [C8], [C10], [C11]. Noise limits [C25], [C26]. Exponential sample requirements at p ≤ 11 [C19]. Hardware performance "decreases with problem size" [C27]. For protein search the argmin readout is classically reproducible (H-001), and the S29–S33 structural registers were solved by SA or greedy (45/45). No mechanism remains.

**P1′ — High-depth QAOA combined with quantum minimum finding (fault tolerant), LABS-type: WEAK.** The only quantitative "scaling advantage" (1.21^N versus MTS 1.34^N [C28]) is a noiseless simulation at N ≤ 40. It depends on a Grover-type step that the classical competitor could also receive, and QAOA alone scales worse (1.46^N). It is also a fault-tolerant algorithm, so the arguments of [C64] and [C65] apply. It is problem-specific (LABS) with no protein mapping. It is worth tracking, not building on.

**P2 — VQE, CVaR-VQE and ADAPT on classical diagonal costs: KILLED.** No classical-baseline advantage has ever been claimed ([C3], [C4], [C6] compare only against quantum baselines). Training pathologies [C20]–[C24]. The trainable-means-simulable tension [C22]. The program's own 33–34 null contrasts and closed-form reductions.

**P3 — Quantum annealing (including QAC and counterdiabatic variants): KILLED for protein search; WEAK as a general optimization claim.** Twelve years of claims show the same pattern: advantage over SA [C42], [C51], or a constant factor [C43], that dissolves against SQA, cluster methods, exact solvers or SBM ([C41], [C42], [C45], [C52]). The strongest current claim [C44] (approximate, ε ≥ 1%, engineered 2D spin glasses) is directly contested [C45], [C46]. Protein demonstrations are tiny or hybrid ([C86]–[C91], [C96]–[C98]). Their lattice energies are proxies that fail condition C, and classical PERM or CPSP solve them.

**P4 — Grover, amplitude amplification, Dürr–Høyer minimum finding: KILLED as a protein lever.** The quadratic query speedup is optimal [C55] but does not survive fault-tolerant overhead [C63]–[C66]. Protein subproblems are structured, so exhaustive search is never the relevant baseline. Amplitude-amplified decoder restarts gain at most about 8× in calls at the measured saturation point (64 restarts), and each call would require a reversible continuous optimizer.

**P5 — Quantum backtracking and branch-and-bound: WEAK (conditional, low prior).** This is the most rigorous near-quadratic speedup in the domain ([C57]–[C61]). It maps naturally onto rotamer, branch and contact CSPs. But:
- it is relative to the same classical tree, while structure-exploiting exact solvers (CFN, tree decomposition, CPSP) shrink that tree;
- quadratic speedups fail the fault-tolerant cost test, including the CSP-specific estimate whose advantage "disappears" with decoder costs [C63];
- C-4 is discrimination-limited at the lengths tested.

It becomes relevant only if the C-4 ORACLE-ceiling test at length shows value, and the classical exact solvers are then shown to hit exponential walls at protein-relevant sizes.

**P6 — Quantum-accelerated Markov-chain heuristics used as optimizers: KILLED for optimization.** "A day and a million physical qubits" versus "four CPU-minutes" [C64]. Search at 44–60 aa is restart-saturated. The *sampling* version of this primitive (AA-1) is **not** judged here. It belongs to Domain D and remains the program's most defensible candidate, conditional on the C-1 mixing-time kill test.

**P7 — Super-quadratic structured primitives (short path, jump-to-end, Kikuchi quartic, DQI): INTERESTING as theory; WEAK for this program.** These are the only optimization-type speedups that clear the quartic bar suggested by [C65] (the quartic ones in [C71], [C72]). The super-Grover ones [C69], [C70] improve the exponent only slightly. All require planted or algebraic structure that no known protein subproblem has. The planted-inference regime (information present but classically hard to extract) is the opposite of the program's measured information-limited regime. A theory note mapping "structure inference from noisy restraints" onto the planted-inference framework would be novel, but I expect it to be negative.

**P8 — Quantum-seeded classical hybrids (QE-MTS, BF-DCQO, HSQC): WEAK.** The evidence is simulated (N ≤ 37, crossover extrapolated to N ≳ 47 [C29]) or hardware runs against disputed or weak baselines [C36], [C46]. The HSQC benchmark's own abstract reports strong classical solvers matching or exceeding the quantum results [C37]. The protein instances are 12–16 residues [C96], [C97].

**Answer to the key question: no.** No quantum optimization or search mechanism has a demonstrated or credibly estimated scaling advantage for protein-relevant discrete search that survives both strong classical baselines and realistic fault-tolerant overhead.
- The provable speedups are about quadratic, and published end-to-end analyses say quadratic is insufficient on early fault-tolerant machines.
- The empirical claims are small-N, simulated or disputed, and none concerns a protein-relevant cost against exact protein solvers.
- The program's own evidence adds two independent reasons: the search is already classically saturated, and optimized energies do not transmit to accuracy.

Domain C therefore contributes no load-bearing quantum candidate. Its useful output is negative-result scaffolding for the H-001 reduction theorem, and a pointer to Domain D (sampling), where the one open lever sits.
