# Domain A: Quantum sampling and Markov-chain acceleration (literature evidence notes)

_Literature agent, Domain A. Compiled 2026-09-26. These are evidence notes for the coordinator; they are not the final review. No experiments were run and no repository file was edited._

**Tags.** **L** = a claim stated in a verified paper (quoted, or closely paraphrased with its location). **I(agent)** = my own reasoning or back-of-envelope estimate. An I(agent) item is never a literature claim. Every I(agent) number is order-of-magnitude only and must be re-derived before anyone cites it.

**Summary.**
- The provable quantum gain for sampling a classical Boltzmann/posterior distribution is **quadratic in the spectral gap (or in the barrier amplitude, or in the Poincaré constant)**. That holds for:
  - Szegedy walks;
  - quantum simulated annealing (QSA);
  - quantum walks over parallel tempering / replica exchange;
  - continuous-space QSVT samplers.
- Claims of more than a quadratic gain fall into three groups:
  - "cubic/quartic" (Layden) and "sixth-degree" (Incudini–Mazzola): empirical, from fits at n ≤ 10 spins;
  - "quartic" (Leng et al.): measured against a weaker classical *bound*;
  - "up-to-exponential" (Claudon et al.): relative to a chain's own mixing time, under a condition that must be checked case by case.
- Fault-tolerant resource estimates (Sanders et al. 2020; Lemieux et al. 2020; Babbush et al. 2021) conclude that a quadratic speedup of Metropolis/SA is **not** practical on modest surface-code machines.
  - Sanders et al.: about 1 year of quantum runtime is needed to cross over on 512-spin SK, even under quantum-favourable assumptions.
- The only protein application of a quantum-walk Metropolis sampler (QFold, 2022) has three problems:
  - it precomputes the energy of *every* configuration, which is exhaustive classical enumeration;
  - it tests 64–1,024-state peptides;
  - it extrapolates a fitted exponent to claim a 10^87–10^373 speedup for a 250-residue protein. I judge that extrapolation unsupported.
- **No paper measures, bounds or estimates the mixing time of a learned-energy protein structure posterior. No paper gives a resource estimate for a Metropolis walk operator on such an energy.** Both are open gaps.

---

## (1) Scope and search log

**Scope.** Quantum walks and mixing (Szegedy, MNRS, Richter, Wocjan–Abeyesinghe):
- QSA;
- quantum Metropolis and quantum Gibbs samplers;
- fast-forwarding;
- quantum rejection sampling;
- QSVT and continuous-space samplers;
- quantum-enhanced MCMC (QeMCMC) and its critiques;
- quantum annealers used as Boltzmann samplers;
- lower bounds and no-go results;
- fault-tolerant resource estimates;
- protein, molecular and polymer applications.

Classical counterarguments were also covered: lifting and nonreversible chains, parallel tempering (PT) mixing theory, HMC scaling, replica-exchange MD (REMD), and learned one-shot samplers.

**Queries and fetches** (WebSearch, plus WebFetch of arxiv.org abstract/HTML/PDF pages; PDFs parsed locally with pypdf for Lemieux, Sanders and Layden):
- `Szegedy "Quantum speed-up of Markov chain based algorithms" FOCS 2004 doi`
- arXiv abstract pages fetched directly: quant-ph/0401053, quant-ph/0608026, quant-ph/0609204, quant-ph/0606202, 0804.4259, 0804.1571, 0911.3635, 1011.1468, 0905.2199, 1603.02940, 2303.18224, 2311.09207, 2210.01670, 2405.20322, 2406.16023, 2107.07365, 1804.02321, 1103.2774, 1806.01838, 2203.12497 (+PDF), 2403.03087, 2408.07881, 2305.08789, 2411.17821, 2405.04247, 2502.08060, 2606.23350, 2607.22818 (+HTML), 1910.01659 (+PDF), 2007.07391 (PDF), 2011.04149, 2101.10279 (HTML, two targeted passes), 2207.06462, quant-ph/0301023 (+HTML v2), quant-ph/0012090, 2001.06305, 1712.01609, 1705.08253, 1712.02318, 1502.05511, 1503.01334, 1504.06987, 0811.0596, 1907.09965, 2009.11270, 2210.06539, 2310.11445, 2210.08104, 2505.05301 (+HTML), 2608.24527 (+HTML), 2609.20253, 2501.05868 (+HTML), 1903.07493, 1002.2419, 0903.3465, 1110.2494, 1005.3034, 1402.7359, 1805.12445, 1805.03662, 2012.08827, 1510.07611, 1503.04216, 1510.08057, 2201.11781, 2311.15891, 2205.06084, 1204.5485, 2004.01118, 2606.21241, 2308.07964, 0906.2341, 1001.4460, 1812.01729
- `Ozgul Li Mahdavi Wang "Stochastic quantum sampling for non-logconcave distributions..."`
- `"Gibbs sampling of continuous potentials on a quantum computer" Motamedi Ronagh`
- `quantum-enhanced Markov chain Monte Carlo Layden follow-up spectral gap scaling critique 2024 2025`
- `"From quantum-enhanced to quantum-inspired Monte Carlo"`
- `Ferguson Wallden "Quantum-enhanced Markov chain Monte Carlo for systems larger than a quantum computer"`
- `quantum walk Metropolis protein folding torsion angles 2023 2024 2025 follow-up QFold`
- `quantum-enhanced Markov chain Monte Carlo protein OR peptide OR polymer conformations sampling`
- `Ghamari Hauke Covino Faccioli ... Scientific Reports doi`
- `Woodard Schmidler Huber "Conditions for rapid mixing..."` and `"...torpid mixing..."`
- `Aharonov Ta-Shma qsampling "statistical zero knowledge"...`
- `Chen Lovász Pak "Lifting Markov chains to speed up mixing"`
- `Diaconis Holmes Neal "Analysis of a nonreversible Markov chain sampler"`
- `Lewis et al. "Scalable emulation of protein equilibrium ensembles..." BioEmu`
- `Lindorff-Larsen ... "How fast-folding proteins fold"`
- `Beskos ... "Optimal tuning of the hybrid Monte Carlo algorithm" Bernoulli`
- `Sugita Okamoto "Replica-exchange molecular dynamics method for protein folding"`
- `Perdomo-Ortiz ... Scientific Reports 2 571`
- `Noé Olsson Köhler Wu "Boltzmann generators" Science 2019`

---

## (2) Verified papers

Fields per paper: citation · Verified URL · key quote · algorithm / setting · claimed speedup · resources · classical comparator · type · limitations · labels.

### A. Quantum-walk foundations

**P1. Szegedy, "Quantum speed-up of Markov chain based algorithms."**
- **Citation:** M. Szegedy, FOCS 2004, pp. 32–41. DOI 10.1109/FOCS.2004.53. arXiv companion: "Spectra of Quantized Walks and a √(δε) rule", quant-ph/0401053.
- **Verified:** https://arxiv.org/abs/quant-ph/0401053 ; https://dl.acm.org/doi/10.1109/FOCS.2004.53 (ACM listing seen via search).
- **Quote** (arXiv abstract): the classical algorithm costs "O(℘0 + (℘1+℘2)/δε) … for the 'quantized' version … only O(℘0 + (℘1+℘2)/√(δε)). We refer to this as the √δε rule."
- **Algorithm / setting:** quantized bipartite walk for a symmetric (reversible) Markov chain; detects whether marked elements exist.
- **Claimed speedup:** quadratic in 1/(δε).
- **Resources:** black-box model (℘0: uniform sample; ℘1: transition sample; ℘2: marking test).
- **Classical comparator:** the random-walk algorithm.
- **Type:** theory.
- **Limitations:** detection, not sampling; symmetric chains.
- **Labels:** QUERY-COMPLEXITY SPEEDUP, ORACLE-MODEL RESULT, THEORETICAL SPEEDUP.

**P2. Magniez, Nayak, Roland, Santha, "Search via quantum walk."**
- **Citation:** SIAM J. Comput. 40(1):142–164 (2011). DOI 10.1137/090745854. arXiv quant-ph/0608026.
- **Verified:** https://arxiv.org/abs/quant-ph/0608026
- **Quote** (abstract): "apply quantum phase estimation to the quantum walk in order to implement an approximate reflection operator … used in an amplitude amplification scheme."
- **Setting:** finding a marked element; Szegedy walk + phase estimation + amplitude amplification.
- **Claimed speedup:** quadratic in 1/√δ and 1/√ε terms (MNRS cost framework).
- **Labels:** QUERY-COMPLEXITY SPEEDUP, ORACLE-MODEL RESULT.
- **Limitations:** search, not sampling. It needs a marking oracle. For proteins that oracle must be native-free, which the opportunity map (QA-3) requires.

**P3. Krovi, Magniez, Ozols, Roland, "Quantum walks can find a marked element on any graph."**
- **Citation:** Algorithmica 74(2):851–907 (2016). DOI 10.1007/s00453-015-9979-8. arXiv 1002.2419.
- **Verified:** https://arxiv.org/abs/1002.2419
- **Quote:** "the number of steps of the quantum walk is quadratically smaller than the classical hitting time HT(P,M) of any reversible random walk P."
- **Scope:** single marked vertex.
- **Labels:** QUERY-COMPLEXITY SPEEDUP.

**P4. Ambainis, Gilyén, Jeffery, Kokainis, "Quadratic speedup for finding marked vertices by quantum walks."**
- **Citation:** arXiv 1903.07493 (STOC 2020).
- **Verified:** https://arxiv.org/abs/1903.07493
- **Quote:** "a new quantum algorithm for finding a marked vertex in any graph, with any set of marked vertices, that is (up to a log factor) quadratically faster than the corresponding classical random walk."
- **Labels:** QUERY-COMPLEXITY SPEEDUP.
- **Limitation:** hitting and search only, not equilibrium sampling.

**P5. Richter, "Quantum speedup of classical mixing processes."**
- **Citation:** PRA 76, 042306 (2007). DOI 10.1103/PhysRevA.76.042306. arXiv quant-ph/0609204.
- **Verified:** https://arxiv.org/abs/quant-ph/0609204
- **Quote:**
  - "mixing time of P, is O(δ⁻¹ log 1/π*) … A natural question is whether a speedup … to O(√δ⁻¹ log 1/π*) … is possible using quantum walks. We provide evidence for this possibility …";
  - it is proven only for the "periodic lattice Z_n^d".
- **Labels:** THEORETICAL SPEEDUP (special graphs).
- **Limitation:** the general quadratic mixing speedup is *not* proven.

**P6. Richter, "Almost uniform sampling via quantum walks."**
- **Citation:** New J. Phys. 9, 72 (2007). DOI 10.1088/1367-2630/9/3/072. arXiv quant-ph/0606202.
- **Verified:** https://arxiv.org/abs/quant-ph/0606202
- **Quote:** "formulate two plausible conjectures which together would imply that it runs in time O(δ^{-1/2} log N log ε^{-1}) … We prove each conjecture for a subclass of Cayley graphs."
- **Labels:** THEORETICAL SPEEDUP (conjectural in general).
- **Limitation:** uniform target distribution only.

**P7. Wocjan & Abeyesinghe, "Speed-up via quantum sampling."**
- **Citation:** PRA 78, 042336 (2008). arXiv 0804.4259.
- **Verified:** https://arxiv.org/abs/0804.4259
- **Quote:** "prepare a quantum sample, i.e., a coherent version of the stationary distribution of a reversible Markov chain … significantly better running time than that of a previous algorithm based on adiabatic state generation."
- **Setting:** needs a *sequence* of slowly varying chains whose stationary states overlap (an annealing path).
- **Claimed speedup:** quadratic in the gap along the path.
- **Labels:** THEORETICAL SPEEDUP, SAMPLING SPEEDUP (qsample).

**P8. Somma, Boixo, Barnum, Knill, "Quantum simulations of classical annealing processes."**
- **Citation:** PRL 101, 130504 (2008). DOI 10.1103/PhysRevLett.101.130504. arXiv 0804.1571.
- **Verified:** https://arxiv.org/abs/0804.1571
- **Quote:** "It requires order 1/√δ steps to find an optimal solution with bounded error probability, where δ is the minimum spectral gap of the stochastic matrices used in the classical annealing process. This is a quadratic improvement over the order 1/δ steps."
- **Algorithm:** Szegedy walk + Zeno effect via randomised evolution.
- **Labels:** THEORETICAL SPEEDUP, ASYMPTOTIC SPEEDUP (in walk steps), ORACLE-MODEL RESULT (the walk is assumed implementable).
- **Limitation:** counts steps, not gates. There is also an extra dependence on the length of the annealing schedule.

**P9. Orsucci, Briegel, Dunjko, "Faster quantum mixing for slowly evolving sequences of Markov chains."**
- **Citation:** Quantum 2, 105 (2018). DOI 10.22331/q-2018-11-09-105. arXiv 1503.01334.
- **Verified:** https://arxiv.org/abs/1503.01334
- **Quote:**
  - "except in special cases, quantum algorithms achieve a run-time of O(√δ⁻¹ √N), which introduces a costly dependence on the Markov chain size N, not present in the classical case";
  - for slowly evolving sequences, "O(√δ⁻¹ ⁴√N)"; "under certain assumptions, our algorithms are optimal."
- **Labels:** THEORETICAL SPEEDUP. Also functions as a NO-GO caveat: there is **no generic quadratic mixing speedup from a cold start**.
- **Critical for proteins:** N is the state-space size, which is exponential in the number of residues. The generic quantum mixing cost therefore carries a √N (or N^{1/4}) factor, unless one has a warm-start annealing path whose consecutive distributions overlap well.

**P10. Dunjko & Briegel, "Quantum mixing of Markov chains for special distributions."**
- **Citation:** arXiv 1502.05511 (New J. Phys. 2015; the journal reference is not confirmed on the page).
- **Verified:** https://arxiv.org/abs/1502.05511
- **Quote:**
  - "It has been conjectured that quantum analogs of classical mixing processes may offer a generic quadratic speed-up … However, a true quadratic speed up has thus far only been demonstrated for special classes of Markov chains";
  - they obtain one "when it is beforehand known that the distribution is monotonically decreasing relative to a known order."
- **Labels:** THEORETICAL SPEEDUP (special distributions).

**P11. Aharonov & Ta-Shma, "Adiabatic quantum state generation and statistical zero knowledge."**
- **Citation:** STOC 2003, DOI 10.1145/780542.780546 (DOI as given in Lemieux et al.'s reference list, which was read in this session). arXiv quant-ph/0301023.
- **Verified:** https://arxiv.org/abs/quant-ph/0301023 ; https://arxiv.org/html/quant-ph/0301023v2
- **Quote:** "Any L∈SZK … can be reduced to a family of instances of CQS" (Theorem 1). So "a general solution for quantum sampling would imply SZK⊆BQP" (paraphrase of the paper's remark, via fetch).
- **Labels:** NO ADVANTAGE (general qsampling is believed hard); THEORETICAL.
- **Implication:** preparing the coherent stationary state |π⟩ = Σ√π(x)|x⟩ of an arbitrary efficiently samplable distribution is not expected to be efficient. Quantum sampling speedups must exploit structure: a gapped annealing path or a known Markov chain.

**P12. Aharonov, Ambainis, Kempe, Vazirani, "Quantum walks on graphs."**
- **Citation:** STOC 2001, pp. 50–59. arXiv quant-ph/0012090.
- **Verified:** https://arxiv.org/abs/quant-ph/0012090
- **Quote:** "we give a lower bound on the possible speed up by quantum walks for general graphs, showing that quantum walks can be at most polynomially faster than their classical counterparts."
- **Labels:** NO-GO (bounded speedup, mixing sense).

**P13. Chakraborty, Luh, Roland, "How fast do quantum walks mix?"**
- **Citation:** PRL 124, 050501 (2020). DOI 10.1103/PhysRevLett.124.050501. arXiv 2001.06305.
- **Verified:** https://arxiv.org/abs/2001.06305
- **Quote:** "for dense random networks … the quantum mixing time is O(n^(3/2 + o(1)))."
- **Labels:** THEORETICAL.
- **Relevance:** quantum mixing times of continuous-time quantum walks are poorly characterised outside special graphs.

### B. Classical "lifting" and nonreversible counterparts: limits on what counts as a quantum mixing advantage

**P14. Chen, Lovász, Pak, "Lifting Markov chains to speed up mixing."**
- **Citation:** STOC 1999, pp. 275–281. DOI 10.1145/301250.301315.
- **Verified:** https://dl.acm.org/doi/10.1145/301250.301315 (ACM listing via search).
- **Claim** (from the listing summary; paraphrase): lifting can reduce the mixing time "often to about its square root"; this is best possible; a time-reversible lift gains at most a factor log(1/π₀).
- **Labels:** classical counterargument. A **classical** nonreversible lift already achieves a quadratic mixing speedup on some chains.

**P15. Diaconis, Holmes, Neal, "Analysis of a nonreversible Markov chain sampler."**
- **Citation:** Ann. Appl. Probab. 10(3):726–752 (2000). DOI 10.1214/aoap/1019487508.
- **Verified:** https://projecteuclid.org/journals/annals-of-applied-probability/volume-10/issue-3/Analysis-of-a-nonreversible-Markov-chain-sampler/10.1214/aoap/1019487508.full (via search).
- **Claim:** the nonreversible chain mixes faster than the corresponding Metropolis chain, for certain targets.
- **Labels:** classical counterargument.

**P16. Apers, Sarlette, Ticozzi, "Simulation of quantum walks and fast mixing with classical processes."**
- **Citation:** PRA 98, 032115 (2018). DOI 10.1103/PhysRevA.98.032115. arXiv 1712.01609.
- **Verified:** https://arxiv.org/abs/1712.01609
- **Quote:** "lifted Markov chains … can simulate quantum walks … speedups in mixing and transport phenomena are not necessarily diagnostic of quantum effects."
- **Labels:** NO ADVANTAGE (in the mixing-by-local-evolution sense).

**P17. Apers, Ticozzi, Sarlette, "Lifting Markov chains to mix faster: limits and opportunities."**
- **Citation:** arXiv 1705.08253.
- **Verified:** https://arxiv.org/abs/1705.08253
- **Quote:** "The achievable convergence speed for a lifted chain goes from diameter-time to no acceleration over a standard Markov chain, with conductance bounds limiting the effectiveness of the intermediate cases."
- **Labels:** classical bounds.

**P18. Dervovic, "For every quantum walk there is a (classical) lifted Markov chain with faster mixing time."**
- **Citation:** arXiv 1712.02318.
- **Verified:** https://arxiv.org/abs/1712.02318
- **Quote:** "for every quantum walk there is a lifted Markov chain with a faster mixing time that is polynomial-time computable, as the quantum mixing time is trivially lower bounded by the graph diameter."
- **Labels:** NO ADVANTAGE (graph-mixing sense).
- **Caveat (I(agent)):**
  - The lifted chain lives on n²·D(G) vertices. For exponentially large state spaces (protein conformations) it is not constructible.
  - So this bounds the *physics* of mixing, not the *algorithmic* speedup for implicit exponentially large chains.
  - It nevertheless shows that "diameter-limited mixing" is not intrinsically quantum.

### C. Quantum Metropolis and quantum Gibbs samplers

**P19. Temme, Osborne, Vollbrecht, Poulin, Verstraete, "Quantum Metropolis sampling."**
- **Citation:** Nature 471, 87 (2011). DOI 10.1038/nature09770. arXiv 0911.3635.
- **Verified:** https://arxiv.org/abs/0911.3635
- **Quote:** "we demonstrate how to implement a quantum version of the Metropolis algorithm … sample directly from the eigenstates of the Hamiltonian and thus evades the sign problem."
- **Setting:** *quantum* Hamiltonians.
- **Labels:** THEORETICAL.
- **Limitation (L, from P23 Jiang–Irani):** the analysis "relies upon the use of a boosted and shift-invariant version of QPE which may not exist [CKBG23]."
- **I(agent):** for a classical (diagonal) protein energy the eigenbasis is the computational basis, and the algorithm reduces to classical Metropolis. It offers **no speedup by itself**.

**P20. Yung & Aspuru-Guzik, "A quantum–quantum Metropolis algorithm."**
- **Citation:** PNAS 109, 754–759 (2012). DOI 10.1073/pnas.1111758109. arXiv 1011.1468.
- **Verified:** https://arxiv.org/abs/1011.1468
- **Quote:** "Due to Szegedy's method, the Markov chains of classical Hamiltonians can achieve a quadratic quantum speedup in the eigenvalue gap … [our algorithm] exhibits a quadratic quantum speedup in the eigenvalue gap of the corresponding Metropolis Markov chain for any quantum Hamiltonian."
- **Labels:** THEORETICAL SPEEDUP (quadratic in the gap).

**P21. Poulin & Wocjan, "Sampling from the thermal quantum Gibbs state and evaluating partition functions with a quantum computer."**
- **Citation:** PRL 103, 220502 (2009). DOI 10.1103/PhysRevLett.103.220502. arXiv 0905.2199.
- **Verified:** https://arxiv.org/abs/0905.2199
- **Quote:** "a universal upper bound D^alpha on the thermalization time … where D is the system's Hilbert space dimension and alpha < 1/2."
- **Labels:** THEORETICAL.
- **Scaling:** exponential in the number of degrees of freedom (D^α).

**P22. Chowdhury & Somma, "Quantum algorithms for Gibbs sampling and hitting-time estimation."**
- **Citation:** QIC 17(1/2):41–64 (2017). arXiv 1603.02940.
- **Verified:** https://arxiv.org/abs/1603.02940
- **Quote:**
  - "runs in time almost linear in √(Nβ/Z) … N is the Hilbert space dimension";
  - hitting time estimation in "1/(εΔ^(3/2))", which "quadratically improves the dependence on 1/ε and 1/Δ."
- **Labels:** THEORETICAL SPEEDUP.
- **Scaling:** √(N/Z) is exponential in the number of degrees of freedom for a protein conformation space. This is Grover-style brute force.

**P23. Jiang & Irani, "Quantum Metropolis sampling via weak measurement."**
- **Citation:** arXiv 2406.16023 (2024).
- **Verified:** https://arxiv.org/abs/2406.16023
- **Quote:** "[TOV+11] … relies upon the use of a boosted and shift-invariant version of QPE which may not exist [CKBG23]. … Currently, these [Davies-generator based samplers] are the only provably correct Gibbs samplers for quantum Hamiltonians."
- **Labels:** ADVANTAGE DISPUTED (it disputes the correctness of the original quantum Metropolis proof, not a speedup claim).

**P24. Chen, Kastoryano, Brandão, Gilyén, "Quantum thermal state preparation."**
- **Citation:** arXiv 2303.18224 (2023).
- **Verified:** https://arxiv.org/abs/2303.18224
- **Quote:** "Our algorithms' costs have a provable dependence on temperature, accuracy, and the mixing time (or spectral gap) of the relevant Lindbladian … also benefits from a quantum walk speedup."
- **Labels:** THEORETICAL.
- **I(agent):** for a diagonal (classical) energy the Lindbladian dynamics reduces to a classical Markov generator. The only speedup over classical MCMC is the walk (square-root-in-gap) speedup for the purified state.

**P25. Chen, Kastoryano, Gilyén, "An efficient and exact noncommutative quantum Gibbs sampler."**
- **Citation:** arXiv 2311.09207 (2023; revised 2025).
- **Verified:** https://arxiv.org/abs/2311.09207
- **Quote:** "invokes Hamiltonian simulation for a time proportional to the mixing time and the inverse temperature β … a continuous-time quantum analog of the Metropolis-Hastings algorithm."
- **Labels:** THEORETICAL.
- **Relevance:** made for *noncommutative* H. It is not an advantage source for classical energies.

**P26. Rall, Wang, Wocjan, "Thermal state preparation via rounding promises."**
- **Citation:** Quantum 7, 1132 (2023). DOI 10.22331/q-2023-10-10-1132. arXiv 2210.01670.
- **Verified:** https://arxiv.org/abs/2210.01670
- **Quote:** implementing the Davies generator "demands the ability to estimate the energy of the system unambiguously … only possible if the system satisfies an unphysical 'rounding promise'", which they solve by randomisation.
- **Labels:** THEORETICAL.

**P27. Gilyén, Chen, Doriguello, Kastoryano, "Quantum generalizations of Glauber and Metropolis dynamics."**
- **Citation:** arXiv 2405.20322 (2024; revised 2026).
- **Verified:** https://arxiv.org/abs/2405.20322
- **Quote:** "we prove that the spectral gap of our new highly coherent Gibbs sampler is constant at high temperatures, thereby it mixes fast."
- **Labels:** THEORETICAL.
- **I(agent):** "highly coherent" samplers could in principle have different gaps from their classical analogues. There is **no result** showing a better gap than the best classical chain for a classical energy at low temperature.

**P28. Wocjan & Temme, "Szegedy walk unitaries for quantum maps."**
- **Citation:** Commun. Math. Phys. (2023). DOI 10.1007/s00220-023-04797-4. arXiv 2107.07365.
- **Verified:** https://arxiv.org/abs/2107.07365
- **Quote:** the walk unitary's "eigenphase gap is quadratically larger than the spectral gap of the Lindbladian."
- **Labels:** THEORETICAL SPEEDUP (quadratic).

### D. Annealing, partition functions and expectation estimation

**P29. Wocjan, Chiang, Nagaj, Abeyesinghe, "Quantum algorithm for approximating partition functions."**
- **Citation:** PRA 80, 022340 (2009). DOI 10.1103/PhysRevA.80.022340. arXiv 0811.0596.
- **Verified:** https://arxiv.org/abs/0811.0596
- **Quote:** "a quadratic reduction with respect to the spectral gap … and a quadratic reduction with respect to the parameter characterizing the desired accuracy."
- **Labels:** THEORETICAL SPEEDUP, ASYMPTOTIC SPEEDUP.

**P30. Montanaro, "Quantum speedup of Monte Carlo methods."**
- **Citation:** Proc. R. Soc. A 471, 20150301 (2015). DOI 10.1098/rspa.2015.0301. arXiv 1504.06987.
- **Verified:** https://arxiv.org/abs/1504.06987
- **Quote:** "estimates the expected output value of an arbitrary randomised or quantum subroutine with bounded variance, achieving a near-quadratic speedup over the best possible classical algorithm."
- **Labels:** QUERY-COMPLEXITY SPEEDUP (in samples/ε). The gain is in *estimation precision*, not in mixing.

**P31. Harrow & Wei, "Adaptive quantum simulated annealing for Bayesian inference and estimating partition functions."**
- **Citation:** SODA 2020. arXiv 1907.09965.
- **Verified:** https://arxiv.org/abs/1907.09965
- **Quote:** "Our dependence on the Markov chain gap … is quadratically better than what classical Markov chains achieve … it also improves on classical algorithms by producing 'qsamples' instead of classical samples."
- **Labels:** THEORETICAL SPEEDUP. It explicitly targets **Bayesian inference**, the closest formal match to "sampling a structure posterior".

**P32. Arunachalam, Havlicek, Nannicini, Temme, Wocjan, "Simpler (classical) and faster (quantum) algorithms for Gibbs partition functions."**
- **Citation:** Quantum 6, 789 (2022). DOI 10.22331/q-2022-09-01-789. arXiv 2009.11270.
- **Verified:** https://arxiv.org/abs/2009.11270
- **Quote:** "a quadratic advantage in the number of required quantum samples … and its computational complexity has quadratically better dependence on the spectral gap."
- **Labels:** THEORETICAL SPEEDUP.
- **Note:** the same paper also *improves the classical algorithm*.

**P33. Somma & Boixo, "Spectral gap amplification."**
- **Citation:** SIAM J. Comput. 42, 593–610 (2013). DOI 10.1137/120871997. arXiv 1110.2494.
- **Verified:** https://arxiv.org/abs/1110.2494
- **Quote:** "a quadratic spectral gap amplification is possible when H satisfies a frustration-free property … the quadratic amplification is optimal for frustration-free Hamiltonians and … no spectral gap amplification is possible, in general, if the frustration-free property is removed."
- **Labels:** THEORETICAL SPEEDUP plus a **NO-GO** (quadratic is optimal in the black-box model).

**P34. Boixo, Knill, Somma, "Fast quantum algorithms for traversing paths of eigenstates."**
- **Citation:** arXiv 1005.3034 (2010).
- **Verified:** https://arxiv.org/abs/1005.3034
- **Quote:** "complexity O(L/G log(L/e)), where L is the angular length of the path … path length and the gap are the primary parameters."
- **Labels:** THEORETICAL.
- **Relevance:** the cost of QSA-style paths scales with path length × inverse phase gap.

### E. Fast-forwarding, rejection sampling, QSVT

**P35. Apers & Sarlette, "Quantum fast-forwarding: Markov chains and graph property testing."**
- **Citation:** QIC 19 (2019). arXiv 1804.02321.
- **Verified:** https://arxiv.org/abs/1804.02321
- **Quote:** "uses quantum walks as a means to quadratically fast-forward a reversible Markov chain … quantum walks can accelerate the transient dynamics of Markov chains."
- **Labels:** THEORETICAL SPEEDUP.
- **Limitation:** it returns P^t|ψ⟩ normalised, with a success probability that depends on ‖P^t ψ‖. For sampling it reduces to the same gap-based costs.

**P36. Ozols, Roetteler, Roland, "Quantum rejection sampling."**
- **Citation:** ITCS 2012, pp. 290–308. DOI 10.1145/2090236.2090261. arXiv 1103.2774.
- **Verified:** https://arxiv.org/abs/1103.2774
- **Quote:** "a tight characterization of the query complexity of this quantum state generation problem … it can be used to speed up the main step in the quantum Metropolis sampling algorithm by Temme et al."
- **Labels:** QUERY-COMPLEXITY SPEEDUP (roughly quadratic in the inverse acceptance ratio), ORACLE-MODEL RESULT.

**P37. Low, Yoder, Chuang, "Quantum inference on Bayesian networks."**
- **Citation:** PRA 89, 062315 (2014). DOI 10.1103/PhysRevA.89.062315. arXiv 1402.7359.
- **Verified:** https://arxiv.org/abs/1402.7359
- **Quote:** classical "O(nmP(e)^−1)" vs quantum "O(n2^mP(e)^−1/2) time per sample … notable as it is unrelativized."
- **Labels:** ASYMPTOTIC SPEEDUP (quadratic in 1/P(evidence)).
- **I(agent):** this is the template for "quantum rejection sampling of a posterior from a prior". It requires the prior as a *coherent* state-preparation circuit.

**P38. Gilyén, Su, Low, Wiebe, "Quantum singular value transformation and beyond."**
- **Citation:** STOC 2019, pp. 193–204. DOI 10.1145/3313276.3316366. arXiv 1806.01838.
- **Verified:** https://arxiv.org/abs/1806.01838
- **Role:** the framework underlying QSVT samplers (P44–P46). No sampling claim of its own.

### F. Continuous-space samplers (the closest formal match to a continuous protein energy)

**P39. Childs, Li, Liu, Wang, Zhang, "Quantum algorithms for sampling log-concave distributions and estimating normalizing constants."**
- **Citation:** NeurIPS 2022. arXiv 2210.06539.
- **Verified:** https://arxiv.org/abs/2210.06539
- **Quote:** "quantum Metropolis-adjusted Langevin algorithms with query complexity Õ(κ^{1/2}d) … achieving polynomial speedups in κ,d,ε over the best known classical algorithms."
- **Labels:** QUERY-COMPLEXITY SPEEDUP.
- **Limitation:** log-concave only. A folding posterior is not log-concave.

**P40. Liu, Wang, Ji, "Quantum speedups for log-concave sampling from local structure."**
- **Citation:** arXiv 2609.20253 (2026).
- **Verified:** https://arxiv.org/abs/2609.20253
- **Quote:** "f(x)=Σψ_a(x_{S_a}) … quantum algorithm … using Õ(√κ d) local queries … improves the prior best classical result Õ(κd)."
- **Labels:** QUERY-COMPLEXITY SPEEDUP.
- **I(agent):** the energy is a sum of local clauses, which matches the pairwise structure of a learned energy. Still log-concave only.

**P41. Ozgul, Li, Mahdavi, Wang, "Stochastic quantum sampling for non-logconcave distributions and estimating partition functions."**
- **Citation:** ICML 2024, PMLR 235:38953–38982. arXiv 2310.11445.
- **Verified:** https://arxiv.org/abs/2310.11445
- **Claim:** QSA on slowly varying Langevin chains with stochastic-gradient oracles; "polynomial speedups in terms of both dimension and precision dependencies when compared to the best-known classical algorithms."
- **Labels:** QUERY-COMPLEXITY SPEEDUP.

**P42. Motamedi & Ronagh, "Gibbs sampling of continuous potentials on a quantum computer."**
- **Citation:** ICML 2024, PMLR 235:36322–36371. arXiv 2210.08104 (the v2 title was "…Periodic Potentials…").
- **Verified:** https://arxiv.org/abs/2210.08104
- **Quote:** "Despite suffering from an exponentially long mixing time, this algorithm allows for exponentially improved precision in sampling, and polynomial quantum speedups in mean estimation."
- **Labels:** THEORETICAL.
- **Relevance:** periodic domain (torus), so it is relevant to **torsion-angle** parameterisations.

**P43. Claudon, Piquemal, Monmarché, "Quantum speedup for nonreversible Markov chains."**
- **Citation:** Nat. Commun. 16, 10732 (2025). DOI 10.1038/s41467-025-65761-5. arXiv 2501.05868.
- **Verified:** https://arxiv.org/abs/2501.05868 (+HTML).
- **Quote:** "Such an up-to-exponential quantum speedup goes beyond the predicted quadratic quantum acceleration for reversible chains." Proposition 1: "O(√(τ_rev·τ(ε))·log(1/ε)) uses of the Szegedy quantum walk operators."
- **Caveats** (from the paper, via fetch):
  - "there is no hope to accelerate processes that mix in the time required to cross their underlying graph";
  - "we could not provide a general easy way to check the reversibility on π-average condition";
  - the motivation mentions protein folding and MD, but "no concrete MD simulation results are presented."
- **Labels:** THEORETICAL SPEEDUP, ORACLE-MODEL RESULT (amplitude-encoded transitions).
- **I(agent):** the "exponential" is measured against the nonreversible chain's own mixing time, in toy examples. It is not measured against the best classical sampler.

**P44. Leng, Ding, Chen, Lin, "Operator-level quantum acceleration of non-logconcave sampling."**
- **Citation:** PNAS 123(8), e2512789123 (2026). DOI 10.1073/pnas.2512789123. arXiv 2505.05301.
- **Verified:** https://arxiv.org/abs/2505.05301 (+HTML).
- **Quote:**
  - "yields up to a quartic quantum speedup over best-known classical Langevin-based methods in the non-logconcave setting";
  - "the first quantum algorithm that accelerates replica exchange Langevin diffusion";
  - RELD cost "√(β·d/Gap(ℒ†))·polylog(d,1/ε)"; Langevin cost Õ(√(β d C_PI)).
- **Caveats (via fetch):**
  - "C_PI will grow exponentially with β·Γ, where Γ denotes the barrier height" (the quantum gain is a square root of that exponential, not its removal);
  - the warm-start condition "|⟨ϕ|σ⟩| = Ω(1)";
  - "quartic" is measured against MALA's Cheeger-based bound Õ(d·C_CG²). Against the Poincaré-constant scaling it is quadratic.
- **Labels:** THEORETICAL SPEEDUP, QUERY-COMPLEXITY SPEEDUP (gradient-oracle queries).
- **Relevance:** this is the **most relevant theory paper for SP-1**: a continuous non-convex energy, with a quantum version of *replica exchange* (the strongest classical baseline family) sped up by √gap.

**P45. Olivucci, Sobchuk, Hoque, … Ronagh, "Provable quantum–classical separation for continuous Gibbs sampling."**
- **Citation:** arXiv 2608.24527 (2026).
- **Verified:** https://arxiv.org/abs/2608.24527 (+HTML).
- **Quote:** "every classical algorithm—querying the value, gradient, or any higher-order derivatives of the log-density—requires Ω(α) queries … while a quantum algorithm … samples with Õ(√α) queries," where α = e^{βΔ}.
- **Scope (via fetch):**
  - torus 𝕋^d, s-Gevrey smooth potentials;
  - it is a hide-and-seek construction;
  - the "e^{Ω(d)}" ratio arises only when log α = Ω(d).
- **Labels:** QUERY-COMPLEXITY SPEEDUP (provable, quadratic in α), ORACLE-MODEL RESULT.
- **I(agent):**
  - This is the first *provable* sampling separation on a continuous domain.
  - It is quadratic.
  - The hard instances hide a narrow deep well. Whether learned protein energies have such "needle" wells at the posterior temperature is exactly the question a classical measurement must answer.

**P46. Incudini & Mazzola, "Practical advantage beyond the quadratic speedup limit with fully-quantum walks."**
- **Citation:** arXiv 2607.22818 (2026).
- **Verified:** https://arxiv.org/abs/2607.22818 (+HTML).
- **Quote:**
  - "a total sixth-degree polynomial queries speedup compared to the best classical walk";
  - "runtime crossover is reduced from approximately 10³ years for conventional quantum walks to less than one day."
- **Details (via fetch):**
  - SK model, β = 4;
  - classical exponents from **exact transition matrices at n = 3…10**, fitted as 2^{νn} and extrapolated to n ≈ 50–90;
  - the classical baselines are local and uniform-proposal Metropolis on CPU/GPU/FPGA;
  - parallel tempering was **not** compared;
  - the "<1 day" figure uses optimistic 20 ns gate times.
- **Labels:** SIMULATOR RESULT, HEURISTIC ADVANTAGE (vs weak baselines), plus a FT resource estimate.
- **Assessment:** not a general advantage. The super-quadratic exponent is empirical and comes from n ≤ 10.

### G. Quantum-enhanced MCMC (NISQ route) and critiques

**P47. Layden, Mazzola, Mishmash, Motta, Wocjan, Kim, Sheldon, "Quantum-enhanced Markov chain Monte Carlo."**
- **Citation:** Nature 619, 282–287 (2023). DOI 10.1038/s41586-023-06095-4. arXiv 2203.12497.
- **Verified:** https://arxiv.org/abs/2203.12497 ; PDF parsed.
- **Quote** (main text):
  - "we explicitly computed all the transition probabilities … and then δ … for 3≤ n≤ 10";
  - "⟨δ⟩∝ 2^−kn … ratios suggest a roughly cubic/quartic enhancement at low temperatures";
  - "we observed a quantum speedup experimentally on up to n = 10 qubits";
  - "Characterizing our algorithm at larger scales will require different methods."
- **Comparator:** local (single-flip) and uniform proposals only.
- **Labels:** SIMULATOR RESULT, HARDWARE DEMONSTRATION (n ≤ 10), HEURISTIC ADVANTAGE, and ADVANTAGE DISPUTED (see P48, P49, P50).

**P48. Orfi & Sels, "Bounding speedup of quantum-enhanced Markov chain Monte Carlo."**
- **Citation:** arXiv 2403.03087 (2024).
- **Verified:** https://arxiv.org/abs/2403.03087
- **Quote:** "there is no speedup over classical sampling on a worst-case unstructured sampling problem. We present an upper bound to the Markov gap that rules out a speedup for any unital quantum proposal."
- **Labels:** NO ADVANTAGE (worst case), ADVANTAGE DISPUTED.

**P49. Orfi & Sels, "Quantum enhanced Markov chains require fine-tuned quenches."**
- **Citation:** arXiv 2408.07881 (2024).
- **Verified:** https://arxiv.org/abs/2408.07881
- **Quote:** "in the long-time limit, the gap of the Markov chain is bounded by the inverse participation ratio of the classical states in the eigenstate basis, showing there is no advantage when quenching to an ergodic system."
- **Labels:** ADVANTAGE DISPUTED.

**P50. Christmann, Ivashkov, Chiurco, Mazzola, "From quantum-enhanced to quantum-inspired Monte Carlo."**
- **Citation:** PRA 111, 042615 (2025). DOI 10.1103/PhysRevA.111.042615. arXiv 2411.17821.
- **Verified:** https://arxiv.org/abs/2411.17821
- **Claim:** classical tensor-network simulators used as the proposal "can maintain a scaling advantage over standard classical samplers."
- **Labels:** ADVANTAGE DISPUTED. The benefit is partly reproducible classically ("quantum-inspired").

**P51. Nakano, Hakoshima, Mitarai, Fujii, "Markov-chain Monte Carlo method enhanced by a quantum alternating operator ansatz" (QAOA-MC).**
- **Citation:** PRR 6, 033105 (2024). DOI 10.1103/PhysRevResearch.6.033105. arXiv 2305.08789.
- **Verified:** https://arxiv.org/abs/2305.08789
- **Claim:** uses acceptance rate as a trainable proxy for the gap and reports quadratic speedup in convergence (per the abstract summary).
- **Labels:** SIMULATOR RESULT, HEURISTIC ADVANTAGE.

**P52. Ferguson & Wallden, "Quantum-enhanced Markov chain Monte Carlo for systems larger than your quantum computer."**
- **Citation:** PRR 7, 013231 (2025). DOI 10.1103/PhysRevResearch.7.013231. arXiv 2405.04247.
- **Verified:** https://arxiv.org/abs/2405.04247
- **Quote:** "only 6 simulated qubits suffice to gain advantage compared to standard classical approaches when investigating the magnetization of a 36 spin system."
- **Labels:** SIMULATOR RESULT, HEURISTIC ADVANTAGE (vs "standard" classical samplers).

**P53. Arai & Kadowaki, "Quantum annealing enhanced Markov-chain Monte Carlo."**
- **Citation:** arXiv 2502.08060. Published in Sci. Rep. (2025) per the search listing https://www.nature.com/articles/s41598-025-07293-y; the volume/article number was not checked.
- **Verified:** https://arxiv.org/abs/2502.08060
- **Quote:** "Our results reveal larger spectral gaps, faster convergence of energy observables."
- **Labels:** SIMULATOR/HEURISTIC ADVANTAGE (SK, vs classical MCMC).

**P54. Cao, Cui, Wang, Tang, "Irreversibility enhances quantum-enhanced Markov-chain Monte Carlo."**
- **Citation:** arXiv 2606.23350 (2026).
- **Verified:** https://arxiv.org/abs/2606.23350
- **Claim:** nonreversible QeMCMC improves on spin-glass benchmarks.
- **Labels:** SIMULATOR RESULT, HEURISTIC ADVANTAGE.

### H. Fault-tolerant resource estimates and practicality

**P55. Lemieux, Heim, Poulin, Svore, Troyer, "Efficient quantum walk circuits for Metropolis-Hastings algorithm."**
- **Citation:** Quantum 4, 287 (2020). DOI 10.22331/q-2020-06-29-287. arXiv 1910.01659.
- **Verified:** https://arxiv.org/abs/1910.01659 ; PDF parsed.
- **Quotes:**
  - "a direct implementation of this oracle requires costly arithmetic operations and thus reformulate the quantum walk";
  - Table 1: the Boltzmann coin B costs "O(N·2^d log 1/ε)" T-count for a (k,d)-local Ising model;
  - "the entire Boltzmann coin requires O(N log 1/ε) T gates";
  - "The complexity of the Boltzmann coin does scale exponentially with the sparsity parameters of the model however, namely as O(max_j 2^{|N_j|})."
- **Numerics:**
  - "super-quadratic speed-up (≈x^0.42) for the Ising chain" (n = 3–12);
  - "sub-quadratic speed-up (≈x^0.75) for random sparse Ising graphs" (n = 4–14).
- **Practicality:**
  - against Janus (10^12 spin updates/s, 10^18 steps/month), a quadratic speedup needs one walk step "in a few milliseconds";
  - this implies logical gate times from "0.5 picoseconds (sub-quadratic)" to "1 nanosecond (quadratic)" to "0.5 microseconds (super-quadratic)";
  - conclusion: "if a quantum computer is to offer a practical speed-up … a better understanding of the class of problems for which heuristic super-quadratic speed-ups can be achieved is required."
- **Labels:** SIMULATOR RESULT (heuristic), FT resource analysis, and effectively NO PRACTICAL ADVANTAGE at a quadratic speedup.

**P56. Sanders, Berry, Costa, Tessler, Wiebe, Gidney, Neven, Babbush, "Compilation of fault-tolerant quantum heuristics for combinatorial optimization."**
- **Citation:** PRX Quantum 1, 020312 (2020). DOI 10.1103/PRXQuantum.1.020312. arXiv 2007.07391.
- **Verified:** https://arxiv.org/abs/2007.07391 ; PDF parsed.
- **Quotes:**
  - "quantum accelerated simulated annealing would require roughly a day and a million physical qubits to optimize spin glasses that could be solved by classical simulated annealing in about four CPU-minutes";
  - "For the N = 512 spin SK model … M≈ 7×10^7 as the minimum number of steps … the quantum computer would need to run for … about one year";
  - "the Szegedy walk approach is strictly less efficient than the qubitized variant."
- **Assumptions:** 170 µs per Toffoli with a single CCZ factory, ~150,000 physical qubits per factory region, d = 31.
- **Other numbers:**
  - the LHPST QSA walk step for LABS N = 512 costs 1.2×10^6 Toffolis per step (Table IX);
  - classical SA runs ~7 ns per update.
- **Labels:** NO ADVANTAGE (for quadratic speedups on modest surface-code machines); FT RESOURCE ESTIMATE.

**P57. Babbush, McClean, Newman, Gidney, Boixo, Neven, "Focus beyond quadratic speedups for error-corrected quantum advantage."**
- **Citation:** PRX Quantum 2, 010103 (2021). DOI 10.1103/PRXQuantum.2.010103. arXiv 2011.04149.
- **Verified:** https://arxiv.org/abs/2011.04149
- **Claim:** quadratic speedups alone are insufficient on modest fault-tolerant devices; quartic speedups are far more plausible (abstract plus summary).
- **Labels:** NO ADVANTAGE (quadratic regime).

**P58. Chiang, Nagaj, Wocjan, "Efficient circuits for quantum walks."**
- **Citation:** QIC 10(5&6):420–434 (2010). arXiv 0903.3465.
- **Verified:** https://arxiv.org/abs/0903.3465
- **Quote:** "our method scales linearly in the sparsity parameter and poly-logarithmically with the inverse of the desired precision."
- **Labels:** resource/circuit construction.

**P59. Häner, Roetteler, Svore, "Optimizing quantum circuits for arithmetic."**
- **Citation:** arXiv 1805.12445 (2018).
- **Verified:** https://arxiv.org/abs/1805.12445
- **Content:** circuits for "Gaussians, hyperbolic tangent, sine/cosine, inverse square root, arcsine, and exponentials" as piecewise polynomials.
- **Relevance:** the building blocks for a coherent learned-energy oracle.

**P60. Babbush, Gidney, Berry, Wiebe, McClean, Paler, Fowler, Neven, "Encoding electronic spectra in quantum circuits with linear T complexity."**
- **Citation:** PRX 8, 041015 (2018). DOI 10.1103/PhysRevX.8.041015. arXiv 1805.03662.
- **Verified:** https://arxiv.org/abs/1805.03662 (existence and metadata).
- **Note:** I use this only as the reference for the data-lookup ("QROM") construction. The claim that its cost is linear in the number of table entries is **my recollection of the body. It is not verified in this session.**

### I. Quantum annealers as Boltzmann samplers

**P61. Amin, "Searching for quantum speedup in quasistatic quantum annealers."**
- **Citation:** PRA 92, 052323 (2015). DOI 10.1103/PhysRevA.92.052323. arXiv 1503.04216.
- **Verified:** https://arxiv.org/abs/1503.04216
- **Quote:** "returning a final population that is close to a Boltzmann distribution of the Hamiltonian at a single (freeze-out) point during the annealing."
- **Labels:** THEORETICAL. The effective temperature is not controlled.

**P62. Benedetti, Realpe-Gómez, Biswas, Perdomo-Ortiz, "Estimation of effective temperatures in quantum annealers for sampling applications."**
- **Citation:** PRA 94, 022308 (2016). DOI 10.1103/PhysRevA.94.022308. arXiv 1510.07611.
- **Verified:** https://arxiv.org/abs/1510.07611
- **Quote:** "it will do so with an instance-dependent effective temperature, different from its physical temperature."
- **Labels:** HARDWARE DEMONSTRATION. The comparison is with 100-step contrastive divergence, which is **comparable, not better**.

**P63. Vuffray, Coffrin, Kharkov, Lokhov, "Programmable quantum annealers as noisy Gibbs samplers."**
- **Citation:** PRX Quantum 3, 020317 (2022). DOI 10.1103/PRXQuantum.3.020317. arXiv 2012.08827.
- **Verified:** https://arxiv.org/abs/2012.08827
- **Quote:** "quantum annealers behave as samplers that generate independent configurations from low-temperature noisy Gibbs distributions" with "spurious interactions absent from the hardware specification."
- **Labels:** HARDWARE DEMONSTRATION. This is a limitation: the device samples a *different* distribution from the one programmed.

**P64. Isakov, Mazzola, Smelyanskiy, Jiang, Boixo, Neven, Troyer, "Understanding quantum tunneling through quantum Monte Carlo simulations."**
- **Citation:** PRL 117, 180402 (2016). DOI 10.1103/PhysRevLett.117.180402. arXiv 1510.08057.
- **Verified:** https://arxiv.org/abs/1510.08057
- **Quote:** "the QMC tunneling rate displays the same scaling with system size, as the rate of incoherent tunneling … with open … boundary conditions … we obtain a quadratic speedup for QMC."
- **Labels:** classical counterargument. A classical algorithm matches the tunnelling scaling.

### J. Protein, peptide and biomolecular applications

**P65. Casares, Campos, Martin-Delgado, "QFold: quantum walks and deep learning to solve protein folding."**
- **Citation:** Quantum Sci. Technol. 7, 025013 (2022). DOI 10.1088/2058-9565/ac4f2f. arXiv 2101.10279.
- **Verified:** https://arxiv.org/abs/2101.10279 ; https://arxiv.org/html/2101.10279 (two targeted passes).
- **Labels:** SIMULATOR RESULT, HEURISTIC ADVANTAGE (on 64–1,024-state instances), HARDWARE DEMONSTRATION (4 qubits, trivial). The extrapolated advantage is unsupported (I(agent)).
- The in-depth analysis is in §3.8.

**P66. Campos, Casares, Martin-Delgado, "Quantum Metropolis Solver: a quantum walks approach to optimization problems."**
- **Citation:** Quantum Mach. Intell. 5 (2023). DOI 10.1007/s42484-023-00119-y. arXiv 2207.06462.
- **Verified:** https://arxiv.org/abs/2207.06462
- **Claim:** "potential quantum advantage" on N-Queens (simulation).
- **Labels:** SIMULATOR RESULT.

**P67. Ghamari, Hauke, Covino, Faccioli, "Sampling rare conformational transitions with a quantum computer."**
- **Citation:** Sci. Rep. 12, 16336 (2022). DOI 10.1038/s41598-022-20032-x. arXiv 2201.11781.
- **Verified:** https://arxiv.org/abs/2201.11781 ; https://www.nature.com/articles/s41598-022-20032-x (via search); PubMed 36175529 (via search).
- **Quote:** "the quantum computing step generates uncorrelated trajectories."
- **Setting:** D-Wave samples a *low-resolution* path ensemble built from ML-generated configurations.
- **Labels:** HARDWARE DEMONSTRATION. No speedup claim against the best classical method.

**P68. Ghamari, Covino, Faccioli, "Sampling a rare protein transition with a hybrid classical-quantum computing algorithm."**
- **Citation:** arXiv 2311.15891. Related DOI 10.1021/acs.jctc.3c01174 (J. Chem. Theory Comput.), as listed on the arXiv page.
- **Verified:** https://arxiv.org/abs/2311.15891
- **Quote:** "Our results match those of a special purpose supercomputer designed to perform MD simulations."
- **Labels:** HARDWARE DEMONSTRATION. This is agreement, not advantage.

**P69. Irbäck, Knuthson, Mohanty, Peterson, "Folding lattice proteins with quantum annealing."**
- **Citation:** PRR 4, 043013 (2022). DOI 10.1103/PhysRevResearch.4.043013. arXiv 2205.06084.
- **Verified:** https://arxiv.org/abs/2205.06084
- **Quote:** "evaluated against existing exact results for HP chains with up to N=30 beads with 100% hit rate … obtained by the commonly used hybrid quantum-classical approach. For pure quantum annealing, our method successfully folds an N=14 HP chain."
- **Labels:** HARDWARE DEMONSTRATION (optimisation, not sampling). The hybrid solver confounds the attribution.

**P70. Perdomo-Ortiz, Dickson, Drew-Brook, Rose, Aspuru-Guzik, "Finding low-energy conformations of lattice protein models by quantum annealing."**
- **Citation:** Sci. Rep. 2, 571 (2012). DOI 10.1038/srep00571. arXiv 1204.5485.
- **Verified:** https://arxiv.org/abs/1204.5485 ; https://www.nature.com/articles/srep00571 (via search).
- **Quote:** "Although the cases presented here can be solved in a classical computer …"
- **Labels:** HARDWARE DEMONSTRATION, NO ADVANTAGE.

**P71. Outeiral, Morris, Shi, Strahm, Benjamin, Deane, "Investigating the potential for a limited quantum speedup on protein lattice problems."**
- **Citation:** New J. Phys. (2021). DOI 10.1088/1367-2630/ac29ff. arXiv 2004.01118.
- **Verified:** https://arxiv.org/abs/2004.01118
- **Quote:** "even naive quantum annealing, when applied to protein lattice folding, has the potential to outperform classical approaches."
- **Labels:** SIMULATOR RESULT, HEURISTIC ADVANTAGE (small peptides; optimisation).

**P72. Roget, Damour, Cadet, Wang, "Assessing cost Hamiltonian reliability in quantum protein structure prediction."**
- **Citation:** arXiv 2606.21241 (2026).
- **Verified:** https://arxiv.org/abs/2606.21241
- **Quote:** "for small peptides and on average, the energy landscape of the considered cost Hamiltonian is not correlated well enough to the actual error to provide meaningful predictions."
- **Labels:** NO ADVANTAGE (energy-validity negative).
- **Relevance:** independent support for the S29–S33 "condition C" lesson.

### K. Classical baselines and counterarguments

**P73. Woodard, Schmidler, Huber, "Conditions for rapid mixing of parallel and simulated tempering on multimodal distributions."**
- **Citation:** Ann. Appl. Probab. 19(2):617–640 (2009). DOI 10.1214/08-AAP555. arXiv 0906.2341.
- **Verified:** https://arxiv.org/abs/0906.2341
- **Quote:** "We provide lower bounds on the spectral gaps of parallel and simulated tempering. These bounds imply a single set of sufficient conditions for rapid mixing."
- **Role:** classical theory.

**P74. Woodard, Schmidler, Huber, "Sufficient conditions for torpid mixing of parallel and simulated tempering."**
- **Citation:** Electron. J. Probab. 14:780–804 (2009). DOI 10.1214/EJP.v14-638.
- **Verified:** https://projecteuclid.org/journals/electronic-journal-of-probability/volume-14/issue-none/Sufficient-Conditions-for-Torpid-Mixing-of-Parallel-and-Simulated-Tempering/10.1214/EJP.v14-638.full (via search).
- **Claim:** torpid mixing arises from "persistence" (tall, narrow peaks).
- **Role:** classical theory. It specifies *which* landscapes defeat PT.

**P75. Beskos, Pillai, Roberts, Sanz-Serna, Stuart, "Optimal tuning of the hybrid Monte Carlo algorithm."**
- **Citation:** Bernoulli 19(5A):1501–1534 (2013). DOI 10.3150/12-BEJ414. arXiv 1001.4460.
- **Verified:** https://arxiv.org/abs/1001.4460
- **Quote:** "HMC requires O(d^(1/4)) steps to traverse the state space" (i.i.d. setting).
- **Role:** classical baseline scaling for smooth continuous posteriors.

**P76. Sugita & Okamoto, "Replica-exchange molecular dynamics method for protein folding."**
- **Citation:** Chem. Phys. Lett. 314, 141–151 (1999). DOI 10.1016/S0009-2614(99)01123-9.
- **Verified:** ADS / Semantic Scholar listings via search (https://ui.adsabs.harvard.edu/abs/1999CPL...314..141S/abstract).
- **Role:** the standard classical enhanced sampler for peptides.

**P77. Lindorff-Larsen, Piana, Dror, Shaw, "How fast-folding proteins fold."**
- **Citation:** Science 334, 517–520 (2011). DOI 10.1126/science.1208351.
- **Verified:** https://www.science.org/doi/abs/10.1126/science.1208351 (via search); PubMed 22034434.
- **Content:** 12 fast-folding proteins (10–80 aa) fold reversibly in 100 µs–1 ms of MD with one physics energy.
- **Role:** classical feasibility.

**P78. Noé, Olsson, Köhler, Wu, "Boltzmann generators."**
- **Citation:** Science 365, eaaw1147 (2019). DOI 10.1126/science.aaw1147. arXiv 1812.01729.
- **Verified:** https://arxiv.org/abs/1812.01729 ; https://www.science.org/doi/10.1126/science.aaw1147 (via search).
- **Quote:** "generate unbiased one-shot equilibrium samples of representative condensed matter systems and proteins."
- **Role:** classical counterargument. A learned sampler plus reweighting avoids mixing altogether.

**P79. Lewis, Hempel, Jiménez-Luna, … Clementi, Noé, "Scalable emulation of protein equilibrium ensembles with generative deep learning" (BioEmu).**
- **Citation:** Science (2025). DOI 10.1126/science.adv9817.
- **Verified:** https://www.science.org/doi/10.1126/science.adv9817 (via search); PubMed 40638710.
- **Claim** (search summary): "thousands of statistically independent samples … per hour on a single graphical processing unit."
- **Role:** classical counterargument.

**P80. Mazzola, "Quantum computing for chemistry and physics applications from a Monte Carlo perspective" (REVIEW, orientation only).**
- **Citation:** J. Chem. Phys. 160, 010901 (2024). DOI 10.1063/5.0173591. arXiv 2308.07964.
- **Verified:** https://arxiv.org/abs/2308.07964

**Count:** 80 entries. 79 are verified with metadata. P60 is verified for existence only; its cost claim is not used as evidence.

---

## (3) Primitive analyses (the 16 questions)

Q1–Q16 are answered for each primitive. Each I(agent) number is an order-of-magnitude estimate, not a literature value.

### 3.1 Szegedy walk / quantised Metropolis walk (mixing, hitting, qsample via warm path)

1. **What the QC does.** It applies W(P), a product of two reflections built from √P(x,y), whose phase gap is Θ(√δ) (L: P1, P28). Phase estimation on W reflects about |π⟩ (MNRS, P2).
2. **What it replaces.** Running a reversible chain P for ~1/δ steps.
3. **Why that is hard classically.** When the gap δ is small (bottlenecks, barriers, low temperature), the mixing time is ~δ⁻¹ log(1/π*) (L: P5).
4. **Exact speedup.**
   - Detection and hitting: 1/√(δε) vs 1/(δε) (P1, P3, P4).
   - Mixing from a cold start: generically **not** 1/√δ. It is O(√δ⁻¹·√N) except in special cases (L: P9).
   - Along a slowly varying path with overlaps: Õ(ℓ/√δ) vs Õ(ℓ/δ) (P7, P8).
5. **Complexity measure.** Walk-step (query) count.
6. **Assumptions.**
   - A reversible chain.
   - A warm start or a gapped annealing path.
   - Coherent access to the transition amplitudes.
   - Output is a qsample, and **each measured sample needs a fresh preparation** (I(agent): no-cloning).
7. **Oracle needed.** |x⟩|0⟩ → Σ_y √P(x,y)|x⟩|y⟩. For Metropolis this requires coherent evaluation of E(y)−E(x) for all proposed moves, and a rotation by arcsin√min(1,e^{−βΔE}).
8. **Oracle construction cost.**
   - L (P55): O(N log 1/ε) T gates per Boltzmann coin for bounded-locality Ising models, "exponential[ly] with the sparsity parameters", O(2^{|N_j|}).
   - The direct arithmetic oracle is "costly" (P55). Sanders et al. (P56) give ~10^6 Toffolis per QSA step at N = 512 on a dense cost.
   - For a learned protein energy, see §3.9.
9. **State-prep cost.** You need |π_0⟩ at infinite temperature (cheap: uniform) plus the path. Otherwise amplitude amplification pays a 1/√(overlap) factor, which can be exponential (P9, P11).
10. **Readout cost.** One computational-basis sample per preparation. For expectation values, add amplitude estimation (P30): O(1/ε) repetitions.
11. **Classical post-processing.** Negligible. Energies can be recomputed classically.
12. **Strongest classical algorithm.**
    - Tuned PT / REMD (P73, P76), HMC (P75), nonreversible or lifted chains (P14, P15), SMC.
    - Learned one-shot samplers plus reweighting (P78, P79).
    - Hardware-specialised MCMC (FPGA/GPU; Janus in P55).
13. **Does the advantage survive?**
    - **In query count, against the same chain: yes (quadratic).**
    - Against PT: only if you quantise the PT chain as well (possible, P44). The advantage is then √(PT gap), still quadratic.
    - Against lifted or nonreversible classical chains: those can already achieve up to a square-root gain on some chains (P14), so the margin may vanish.
    - In wall-clock: **not on modest FT hardware for any studied problem** (P55, P56, P57).
14. **Fault tolerance needed?** Yes. Deep coherent arithmetic and phase estimation.
15. **Qubits / depth / T-count (literature).**
    - Sanders (SK/LABS): N = 64–1,024 needs 132–1,116 logical qubits, 2×10^4–4.6×10^6 Toffolis per QSA step, and ~10^5–10^6 physical qubits. That gives ~4×10^3–3×10^4 QSA steps per hour.
    - Crossover for SK N = 512: ~1 year (P56).
    - Lemieux: 3D lattice n = 80³ needs a logical depth of ~200,000 per step at ε ≈ 10^−16 synthesis (P55).
16. **Natural protein mapping.** Sampling a discretised posterior over torsions or CA coordinates under a learned pair energy (SP-1). The chain would be a Metropolis/PT chain over moves of residues or torsions. **Nothing in the literature does this beyond QFold (≤ 1,024 states).**

### 3.2 Quantum simulated annealing / adaptive QSA (Somma et al.; Wocjan–Abeyesinghe; Harrow–Wei; Arunachalam et al.)

1. **What the QC does.** It walks |π_{β_0}⟩ → |π_{β_L}⟩ along an inverse-temperature schedule using Szegedy walks, the Zeno effect, or eigenpath traversal (P8, P34).
2. **What it replaces.** Classical SA or annealed MCMC; FPRAS partition-function schemes (P29, P32).
3. **Why that is hard classically.** Small gaps at low temperature. The schedule length is needed for overlap.
4. **Exact speedup.** 1/√δ vs 1/δ in walk steps (P8). Adaptive schedules with quadratic gap improvement (P31). Plus a quadratic gain in the accuracy of partition-function or expectation estimates (P29, P32).
5. **Complexity measure.** Query / walk steps.
6. **Assumptions.**
   - Consecutive Gibbs states overlap by a constant.
   - The minimum gap along the path is known or bounded.
   - Reversible chains.
7. **Oracle needed.** The same walk oracle as §3.1, at every β.
8. **Oracle construction cost.** The same as §3.1, per step, times the schedule length ℓ.
9. **State-prep cost.** Uniform |π_0⟩ is cheap. The cost is ℓ × (1/√δ_min) walk steps per qsample.
10. **Readout cost.** One sample per full anneal.
    - I(agent): classical MCMC gives one effectively independent sample per ~τ_int after burn-in.
    - QSA must **re-anneal per sample**. For M samples the quantum cost is ~M·ℓ/√δ vs classical ~ℓ/δ + M·τ_int.
    - The quantum advantage therefore requires ℓ·M/√δ < ℓ/δ + M/δ, which roughly means M·√δ·ℓ small. It is **largest when few samples are needed and burn-in dominates.**
11. **Classical post-processing.** Negligible.
12. **Strongest classical algorithm.** PT/REMD, SMC with adaptive temperatures, the improved SVV cooling schedule (P32: that paper also improved the classical side).
13. **Does the advantage survive?**
    - Asymptotically, in queries, yes.
    - In wall-clock, no for SK/LABS (P56: one day of QC ≈ four CPU-minutes).
14. **Fault tolerance needed?** Yes.
15. **Resources.** See 3.1 (Sanders Table IX: "LHPST walk quantum simulated annealing").
16. **Protein mapping.** Annealing along β toward the learned-energy posterior. Harrow–Wei explicitly frames Bayesian inference (P31).
    - I(agent): the S33 soft-Boltzmann readout needs only tens of samples, which is favourable to QSA's per-sample re-anneal cost.

### 3.3 Quantum Metropolis / quantum Gibbs samplers (Temme et al.; Yung–Aspuru-Guzik; CKBG; CKG; Rall–Wang–Wocjan; Gilyén et al.; Jiang–Irani; Poulin–Wocjan; Chowdhury–Somma)

1. **What the QC does.** Prepares Gibbs states of (possibly noncommuting) Hamiltonians, by Lindbladian simulation or by QPE-based Metropolis.
2. **What it replaces.** Classical QMC (sign problem) for quantum H. For a **classical** H it replaces classical MCMC.
3. **Why that is hard classically.** For quantum H: the sign problem. For a classical protein energy there is **no sign problem**, so this reason does not apply.
4. **Exact speedup.**
   - For quantum H: exponential potential (sign problem), unproven in general.
   - For classical H: at most the quadratic walk speedup (P20, P24, P28).
   - Brute-force variants: Õ(√(Nβ/Z)) (P22) and D^α (P21), which are exponential in the number of degrees of freedom.
5. **Complexity measure.** Hamiltonian-simulation time, proportional to the mixing time × β (P25).
6. **Assumptions.**
   - Rapid mixing of the Lindbladian.
   - Energy-estimation issues: the "rounding promise" (P26); boosted, shift-invariant QPE (P23).
7. **Oracle needed.** Block-encoding / Hamiltonian simulation of H.
8. **Oracle construction cost.** For a classical pairwise energy, simulating e^{−iHt} for diagonal H is a phase oracle: the same coherent arithmetic as §3.1.
9. **State-prep cost.** Maximally mixed or TFD state; cheap.
10. **Readout cost.** A computational-basis measurement.
11. **Classical post-processing.** Negligible.
12. **Strongest classical algorithm.** Classical MCMC. For a diagonal H the Gibbs state *is* the classical distribution.
13. **Does the advantage survive?** For classical protein energies: **no, beyond §3.1's quadratic walk speedup.** The brute-force variants are dominated by any MCMC that mixes polynomially.
14. **Fault tolerance needed?** Yes.
15. **Resources.** No classical-energy resource estimates exist.
16. **Protein mapping.** None beyond §3.1. It would matter only for *quantum* Hamiltonians (e.g., electronic structure of a metal site), which is outside SP-1 and noted in the map as AA-3.

### 3.4 Quantum rejection sampling / amplitude-amplified posterior sampling (Ozols–Roetteler–Roland; Low–Yoder–Chuang)

1. **What the QC does.** Converts a qsample of a proposal q (e.g., a prior) into a qsample of the target p ∝ q·L (the posterior) by amplitude amplification.
2. **What it replaces.** Classical rejection or importance sampling from a prior toward a posterior.
3. **Why that is hard classically.** The acceptance probability P_acc (or the ESS fraction) is exponentially small when prior and posterior differ.
4. **Exact speedup.** Quadratic in 1/P_acc: P(e)^{−1/2} vs P(e)^{−1} (P37). The query complexity is tight (P36).
5. **Complexity measure.** Query / time per sample.
6. **Assumptions.** A **coherent** preparation circuit for the proposal (a "q-sample"). It is efficient for Bayesian networks with small in-degree (P37).
7. **Oracle needed.** The proposal-state preparation U_q, and a likelihood/ratio rotation oracle.
8. **Oracle construction cost.**
   - I(agent): if the proposal is a learned generative model (esmprior pair distributions decoded by DG/L-BFGS, BioEmu, a Boltzmann generator), U_q must run the **entire decoder or neural network reversibly in superposition**.
   - That is orders of magnitude more costly than a classical forward pass, and the decoders are iterative optimisers (L-BFGS), which are hard to make reversible.
9. **State-prep cost.** This is the dominant cost (see Q8).
10. **Readout cost.** One sample per amplification.
11. **Classical post-processing.** Reweighting if the result is approximate.
12. **Strongest classical algorithm.** Importance sampling / SMC from the learned prior with MCMC rejuvenation; learned samplers with reweighting (P78, P79).
13. **Does the advantage survive?** Only when P_acc is tiny **and** the classical alternative is plain rejection. SMC/MCMC are not rejection sampling.
14. **Fault tolerance needed?** Yes.
15. **Resources.** None published for continuous molecular models.
16. **Protein mapping.** "Prior → posterior" matches the S33 structure (a learned prior, plus soft reweighting). The coherent prior circuit is the barrier.

### 3.5 Quantum fast-forwarding (Apers–Sarlette)

1–5. It prepares P^t|ψ⟩/‖·‖ in ~√t walk steps (P35). That is a quadratic gain in the *transient* number of steps.
6–9. It needs a reversible chain and the same walk oracle as §3.1. The success probability depends on ‖P^t ψ‖.
10–13.
- For equilibrium sampling it gives nothing beyond §3.1.
- For transient questions (e.g., "where does the chain go in t steps from a decoded structure"), it is quadratic in t.
- Classical lifted chains (P14, P16, P18) cover part of this ground.

14–15. Fault tolerant. No resource estimates.
16. Weak mapping. It could fast-forward local relaxation from a decode. S33 shows local relaxation is restart-saturated (R10), so there is no evident need.

### 3.6 Continuous-space quantum samplers: QSVT / Witten-Laplacian / quantum Langevin / quantum RELD (Childs et al.; Liu–Wang–Ji; Ozgul et al.; Motamedi–Ronagh; Leng et al.; Olivucci et al.)

1. **What the QC does.**
   - Encodes √σ, with σ ∝ e^{−βV}, as the kernel of an operator derived from the Witten Laplacian, and extracts it by singular-value thresholding (P44).
   - Or runs quantum MALA / QSA on Langevin chains (P39, P41).
   - Or solves Fokker–Planck by linear-ODE solvers (P42).
2. **What it replaces.** Langevin, MALA, replica-exchange Langevin.
3. **Why that is hard classically.** Non-log-concave V. The Poincaré constant grows as exp(βΓ) with barrier height Γ (L: P44).
4. **Exact speedup.**
   - Õ(√(β d C_PI)) vs classical Langevin/MALA bounds. "Up to quartic" only against MALA's Cheeger-constant bound (P44).
   - Quantum RELD gives √(1/Gap) (P44).
   - Provable query separation: Ω(α) classical vs Õ(√α) quantum, α = e^{βΔ} (P45).
   - Log-concave: Õ(√κ d) (P40) vs Õ(κ d) classical.
5. **Complexity measure.** Gradient- or evaluation-oracle **query** complexity.
6. **Assumptions.**
   - Warm start, |⟨ϕ|σ⟩| = Ω(1) (P44), or annealing to remove it (P45).
   - Smoothness (Gevrey, P45).
   - Periodic or confining domains.
   - Spatial discretisation with polylog grids.
7. **Oracle needed.** A coherent gradient oracle |x⟩|0⟩ → |x⟩|∇V(x)⟩ (P45), and/or V(x).
8. **Oracle construction cost.** Not given in any of these papers. I(agent): for a learned pair-distance energy over N residues (d = 3N coordinates), ∇V needs O(N²) pair terms, each with sqrt, spline derivative and table lookup (see §3.9).
9. **State-prep cost.** Warm start (P44) or O(β²Δ²) annealing steps (P45).
10. **Readout cost.** Measure the grid registers (d × log N_grid qubits).
11. **Classical post-processing.** Map the grid to coordinates.
12. **Strongest classical algorithm.** PT/REMD, HMC with tempering, SMC, learned generative samplers. P45's lower bound covers every classical query algorithm **on its hard instance class** ("hide-and-seek" narrow wells). It says nothing about typical learned energies.
13. **Does the advantage survive?**
    - In queries, on constructed hard instances: **yes, quadratically, provably** (P45).
    - On a real protein energy: unknown.
    - In wall-clock: no estimates exist.
14. **Fault tolerance needed?** Yes.
15. **Resources.** None published. I(agent): d = 300 coordinates (N = 100 residues) × ~10–20 qubits per coordinate = 3,000–6,000 system qubits, plus arithmetic ancillae.
16. **Protein mapping.** **The best formal match to SP-1**: a continuous non-convex energy with a quantised replica exchange. It is still quadratic.

### 3.7 Quantum-enhanced MCMC (Layden) and variants: the NISQ route

1. **What the QC does.** Prepares |s⟩, evolves under H = (1−γ)H_prob + γH_mix for time t, and measures s′ as the proposal. A classical Metropolis–Hastings accept/reject follows (P47).
2. **What it replaces.** The classical proposal distribution (local or uniform).
3. **Why that is hard classically.** Simulating the quench is believed hard at large n, but P50 shows tensor-network simulation retains a scaling advantage.
4. **Exact speedup.** None proven.
   - Empirical: δ ∝ 2^{−kn}, fitted at 3 ≤ n ≤ 10, giving a "roughly cubic/quartic" enhancement vs local/uniform proposals (P47).
   - Upper bounds: no speedup in the worst unstructured case (P48); the gap is bounded by the IPR, with no advantage for ergodic quenches (P49).
5. **Complexity measure.** Markov-chain gap (iterations).
6. **Assumptions.**
   - A binary (Ising) encoding with H_prob diagonal, implementable as low-order Pauli-Z terms.
   - A symmetric proposal, Q(s′|s) = Q(s|s′), for simple acceptance.
7. **Oracle needed.** Hamiltonian simulation of H_prob.
8. **Oracle construction cost.** I(agent): a learned pairwise distance energy over discretised coordinates expands into **high-order, dense** Z-polynomials. Each pair term is a function of two multi-bit coordinates, so the Trotter circuits are deep.
9. **State-prep cost.** Trivial (a basis state).
10. **Readout cost.** One shot per proposal.
11. **Classical post-processing.** Compute E(s′) classically and accept or reject. This is exact, so the method is robust to noise.
12. **Strongest classical algorithm.** PT, cluster moves, population annealing, and TN-simulated proposals (P50). Layden compared only local and uniform proposals.
13. **Does the advantage survive?** Undetermined at scale. Disputed (P48, P49, P50).
14. **Fault tolerance needed?** No for NISQ runs. Noise is tolerated by construction, but noise reduces the gain.
15. **Resources.** The main text says a speedup was "observed … experimentally on up to n = 10 qubits" (P47). A coarse-grained variant uses √n qubits (P52).
16. **Protein mapping.** Only via a discrete encoding with a diagonal H_prob. S29–S33 showed such register energies fail "condition C": register energy does not transmit to chain RMSD (README R8, fact 5; also P72). **Weak mapping.**

### 3.8 QFold (quantum-walk Metropolis for protein torsions): in-depth analysis

**What was done** (all L, from the arXiv HTML; section numbers as given by the fetch):

- **Representation.** Backbone φ, ψ torsions (ω fixed at π), each discretised to b bits: "1 bit means that angles can take values in {0,π} … 2 bits … π/2" (§IV).
- **Instances.** "Dipeptides with 3 to 5 rotation bits … Tripeptides with 2 rotation bits … Tetrapeptides with a single rotation bit" (§IV); 24 instances in total (10 + 10 + 4) (§V.2).
  - I(agent): the state spaces are 2^{2b} for dipeptides (b = 3–5, i.e. 64–1,024 states), 2^{8} = 256 for tripeptides (b = 2, 4 angles) and 2^{6} = 64 for tetrapeptides (b = 1, 6 angles).
- **Energy.** "we have classically precomputed all the energies and encoded a true oracle" (§IV), at MP2/6-31G via Psi4.
  - Every configuration's energy is computed **before** the quantum walk.
  - I(agent): that is exhaustive enumeration. The ground state is then known by a classical argmin over the table. The walk's "speedup" is measured on a problem already solved classically as a side effect of building the oracle.
- **Walk.** A coin-based Szegedy-type walk W̃ = R V† B† F B V, with system, move and coin registers (§II.3). L annealed steps are applied coherently.
- **Figure of merit.** "TTS(t) := t · log(1−δ)/log(1−p(t))," where p(t) is "the probability of hitting the right state." At fixed β = 1000 this is effectively **ground-state optimisation**, not posterior sampling.
- **Classical comparator.** Classical Metropolis with the same moves and schedules. There is **no PT, no exhaustive search, and no HMC/MD baseline**.
- **Results.**
  - Fitted exponent (quantum min TTS ∝ classical min TTS^e): "0.89 ± 0.06" (Minifold initialisation) and "0.53 ± 0.08" (random initialisation) at β = 1000.
  - Annealing schedules with Minifold: 0.85–0.88 (±0.09–0.18).
  - I(agent): e = 0.5 would be the theoretical quadratic speedup. The Minifold-initialised runs, the paper's headline pipeline, show only e ≈ 0.85–0.89, i.e. a ~10–15% exponent gain, on ≤ 1,024-state instances.
- **Extrapolation.** "an average 250 amino acids protein … b=6 bits … the classical min_t TTS would be ≈(2^b)^(2×250×r) … speedup factor of between ≈10^87 and 10^373"; after error correction, "≈10^22" (§V.2).
  - I(agent): this assumes classical Metropolis TTS scales as (state-space size)^r. That is exponential in chain length, fitted on instances with ≤ 6 torsions. It then extrapolates over ~80 orders of magnitude in state-space size.
  - Real protein sampling does not use single-chain Metropolis on a 2^{3000}-state torsion lattice. Nothing supports the extrapolation.
- **Hardware.** IBMQ Casablanca, 4 qubits, 2 walk steps, "176 … depth" after transpilation. "In 7 of the 8 cases we are able to measure such increase [in probability]" of the target state (§VI).
  - This demonstrates a β-dependent bias. It says nothing about speed.
  - The authors say TTS on hardware "would not be interesting" because of noise (§III).
- **Authors' own limitations.**
  - "the range of the precision is limited by the resources of the classical simulation";
  - "We do not expect such quantum advantage to be profitable with early fault-tolerant quantum computers due to error correction overhead" (§VII);
  - "One should substitute the energy evaluation oracle with the quantized (reversible) version" (§I).

**16 questions (condensed).**
- **(1–3)** The same as §3.1, applied to torsion Metropolis optimisation.
- **(4)** Empirical exponent 0.53–0.89 on ≤ 1,024 states. There is no asymptotic statement.
- **(5)** TTS in walk steps.
- **(6)** A precomputed energy table.
- **(7–8)** The oracle is a lookup over all (2^b)^{#angles} configurations. Its classical construction cost is exponential, and it is **not** a coherent energy circuit.
- **(9)** Uniform or Minifold-biased initial state.
- **(10)** Probability of the ground state.
- **(11)** None.
- **(12)** Exhaustive enumeration (already performed), PT, and the AlphaFold-class predictors the paper itself uses as initialisers.
- **(13)** No.
- **(14)** Yes. The authors concede this.
- **(15)** 4 qubits on hardware. No FT estimate for a coherent energy.
- **(16)** Direct mapping, but only as an *optimisation* on toy sizes.

**Labels:** SIMULATOR RESULT; HEURISTIC ADVANTAGE vs matched Metropolis on 64–1,024-state instances; HARDWARE DEMONSTRATION (trivial); the extrapolated advantage is **unsupported** (I(agent)). I found no independent replication or rebuttal paper, so I do not label it ADVANTAGE DISPUTED on literature grounds.

**Relevance to this program.** QFold is the closest precedent, and it shows the failure modes to avoid:
1. an oracle built by enumeration;
2. optimisation TTS presented as sampling;
3. matched-Metropolis baselines only;
4. exponent extrapolation from ≤ 6 torsions.

These are the same structural lessons S29–S33 recorded as DNR-02 and DNR-07.

### 3.9 Cost of a Metropolis walk operator for a learned pair-distance protein energy (I(agent) estimate; no literature estimate exists)

**Target.** E(x) = Σ_{i<j} f_ij(‖r_i − r_j‖): pair-specific learned distance potentials (esmprior-like), over N CA positions or torsions.

**Components per walk step (Szegedy or Lemieux-style).**
- **Coordinates.** 3N fixed-point registers of b ≈ 16–20 bits.
- **Torsion moves.** A torsion move rigidly rotates all downstream residues. The coherent rotation arithmetic (sin/cos, 3×3 products) costs O(N) per move, and ΔE touches O(N²) pairs in the worst case.
- **Cartesian single-residue moves.** Only O(N) pairs change.
- **Per pair term.**
  - Squared distance: ~3 multiplications, ~3b² ≈ 10³ Toffolis.
  - sqrt / inverse-sqrt and a spline in r: piecewise polynomial (P59), ~10³–10⁴ Toffolis.
  - Pair-specific coefficient lookup, if tables are per pair (N² × K entries): data loading linear in table size, per the QROM construction (P60, cost claim unverified). This could dominate unless coefficients are shared across pairs.
- **Boltzmann coin.** Compute e^{−βΔE} → arcsin √·, then a controlled rotation: ~10³–10⁴ Toffolis (P55, P56 give comparable bit budgets).
- **Uncomputation and reflections.** ×2–4.
- **Total.** Roughly 10^6–10^8 Toffolis per step for N = 100 (Cartesian moves at the low end, torsion moves at the high end). Compare Sanders' 1.2×10^6 Toffolis per QSA step for dense N = 512 binary problems (P56). The protein energy is continuous and multi-bit per variable, so it is plausibly more expensive.

**Wall-clock (Sanders' assumption of 170 µs per Toffoli, single factory).**
- Quantum step: ~3 min to ~5 h per walk step.
- Classical step: a Metropolis ΔE for one residue move at N = 100 costs ~10²–10⁴ pair evaluations, or ~1–10 µs on a CPU core.
- Per-step cost ratio R ≈ 10^7–10^10. With 100–1,000 parallel factories, R ≈ 10^5–10^8.

**Crossover condition for a quadratic speedup.**
- The quantum needs Q ≈ R walk steps, i.e. the classical chain needs 1/δ ≈ R² ≈ 10^10–10^20 steps, before quantum wall-clock beats a *single* classical chain.
- Quantum runtime at crossover is Q × t_q, which is years or more at the low end of R under current FT assumptions. This matches Sanders' ~1 year for SK-512 (P56).
- PT/REMD also parallelises across replicas and cores; P56 notes that restricting to one core already favours the quantum.

**Qubits.** N = 100 needs ~6,000 coordinate qubits, plus ~10^3–10^4 arithmetic ancillae, plus move and coin registers. That is ~10^4 logical qubits and ~10^7 physical qubits at d ≈ 25–31.

**Conclusion (I(agent)).** A quadratic speedup on this energy becomes relevant only if a classical measurement shows **best-tuned PT/REMD needing ≳10^12–10^15 single-chain steps per independent sample** at the target length and temperature, **and** that this cannot be cut by parallel replicas, better moves, or learned proposals. Even then the quantum runtime is impractically long unless the per-step cost falls by orders of magnitude, or a super-quadratic regime (P46, P45's exp(d) regime) exists and is verified at scale.

---

## (4) Strongest classical counterarguments

1. **Quadratic is too small for fault-tolerant hardware** (P56, P55, P57).
   - One day on a million-qubit surface code equals four CPU-minutes of SA (SK N = 512).
   - Crossover needs ~7×10^7 QSA steps, about one year.
   - Matching Janus at a quadratic speedup needs ~1 ns logical gates.
   - Babbush et al. say to "focus beyond quadratic".
2. **Generic quantum mixing is not quadratic from a cold start.** It carries √N (P9). General qsampling is SZK-hard (P11). Quadratic mixing is known only for special chains or distributions (P5, P6, P10). A gapped warm-start annealing path must exist and be known.
3. **Classical lifting and nonreversibility already give up to square-root mixing gains** (P14, P15). A polynomial-time classical lifted chain mixes faster than any quantum walk's average distribution on the same graph (P18). Mixing speedups "are not necessarily diagnostic of quantum effects" (P16).
4. **The best classical samplers are not the baselines used in positive quantum claims.**
   - Layden (P47) and Incudini–Mazzola (P46) compare against local/uniform Metropolis, not PT.
   - QFold (P65) compares against matched Metropolis.
   - PT/REMD's mixing is characterised by persistence conditions (P73, P74). HMC scales as d^{1/4} per traversal (P75).
5. **Learned one-shot samplers bypass mixing.** Boltzmann generators (P78) and BioEmu (P79, thousands of independent samples per GPU-hour) turn sampling into density evaluation plus reweighting. A quantum MCMC speedup must beat *those* on the program's posterior, not Metropolis.
6. **QeMCMC gains are bounded or dequantisable** (P48, P49, P50). There is no speedup in the unstructured worst case, the gap is bounded by the IPR for ergodic quenches, and TN classical proposals keep the scaling advantage.
7. **Annealer "Boltzmann sampling" is uncontrolled.** The effective temperature is instance-dependent (P62), the device samples a noisy Gibbs state with spurious couplings (P63), and freeze-out is quasistatic (P61). Classical QMC reproduces the tunnelling scaling (P64).
8. **For a classical energy, quantum Gibbs samplers add nothing beyond the walk speedup** (§3.3). The brute-force variants (P21, P22) are exponential in the degrees of freedom.
9. **Energy validity precedes sampling** (P72, and S29–S33 condition C). A better sampler for an energy uncorrelated with accuracy is worthless.

---

## (5) Scaling statements (explicit asymptotics only; no inference from small numerics)

| Source | Statement | Parameter |
|---|---|---|
| P1 Szegedy | O(℘0 + (℘1+℘2)/√(δε)) vs O(℘0 + (℘1+℘2)/(δε)) | gap δ, marked fraction ε |
| P5 Richter | classical t_mix = O(δ⁻¹ log 1/π*); quantum O(√δ⁻¹ log 1/π*) proven on Z_n^d only | gap |
| P6 Richter | conjectured O(δ^{-1/2} log N log ε⁻¹) for constant-degree graphs; proven for some Cayley graphs | gap, N states |
| P9 Orsucci et al. | generic quantum mixing O(√δ⁻¹ √N); slowly evolving sequences O(√δ⁻¹ N^{1/4}) | **N = state-space size** |
| P8 Somma et al. | QSA O(1/√δ) vs SA O(1/δ) steps | minimum gap along schedule |
| P29, P32 | quadratic in gap and in accuracy ε for partition functions | δ, ε |
| P30 Montanaro | mean estimation ~O(σ/ε) vs O(σ²/ε²) | precision |
| P22 Chowdhury–Somma | Gibbs state in Õ(√(Nβ/Z)); hitting time 1/(εΔ^{3/2}) | Hilbert dimension N |
| P21 Poulin–Wocjan | thermalisation ≤ D^α, α < 1/2 | Hilbert dimension D |
| P25 CKG | Hamiltonian-simulation time ∝ t_mix · β (polylog factors) | mixing time, β |
| P33 Somma–Boixo | quadratic gap amplification optimal (frustration-free); none in general | gap |
| P39 Childs et al. | quantum MALA Õ(κ^{1/2} d) queries | condition number, dimension |
| P40 Liu–Wang–Ji | Õ(√κ d) local queries vs classical Õ(κ d) | κ, d |
| P44 Leng et al. | Langevin Õ(√(β d C_PI)); RELD √(β d / Gap); C_PI ~ exp(βΓ) | Poincaré constant, barrier Γ |
| P45 Olivucci et al. | classical Ω(α) vs quantum Õ(√α); α = e^{βΔ}; ratio e^{Ω(d)} when log α = Ω(d) | barrier amplitude, temperature |
| P43 Claudon et al. | O(√(τ_rev τ(ε)) log 1/ε) walk uses | reversibilisation vs mixing time |
| P55 Lemieux et al. | Boltzmann coin O(N log 1/ε) T gates; ∝ 2^{\|N_j\|} in locality | spins N, locality |
| P56 Sanders et al. | SK N = 64–1,024: ~4×10^3–3×10^4 QSA steps/hour; crossover ~1 yr at N = 512 | Toffoli rate |
| P14 Chen–Lovász–Pak | lifting reduces mixing time to ~its square root, best possible; reversible lifts ≤ log(1/π₀) gain | mixing time |
| P18 Dervovic | lifted chain on n²D(G) vertices mixes in D(G) steps | diameter |
| P12 AAKV | quantum walks at most polynomially faster (general graphs) | — |
| P75 Beskos et al. | HMC O(d^{1/4}) steps (i.i.d. targets) | dimension |
| P47 Layden (empirical, n ≤ 10) | ⟨δ⟩ ∝ 2^{−kn}; k-ratio ~ cubic/quartic | **empirical only** |
| P46 Incudini–Mazzola (empirical, n ≤ 10 exact) | sixth-degree query speedup | **empirical only** |
| P65 QFold (empirical, ≤ 1,024 states) | exponent 0.53–0.89 | **empirical only** |

**Protein-specific explicit asymptotics in residues, torsions or temperature for a learned energy:** none found in the literature.

---

## (6) NISQ route vs fault-tolerant route

**NISQ.**
- QeMCMC (P47, P51–P54) and annealer samplers (P61–P63, P67–P71).
- Advantages are empirical, at ≤ ~36 spins (P52) or n ≤ 10 (P47), against local/uniform proposals. They are bounded or disputed (P48–P50).
- The protein mappings demonstrated are lattice/HP optimisation (P69–P71) and low-resolution path networks (P67, P68). None samples a continuous learned-energy posterior.
- The NISQ route also requires a diagonal qubit Hamiltonian that encodes the energy, which reintroduces the register encodings that failed condition C in S29–S33.
- **Verdict:** no credible NISQ route for SP-1.

**Fault-tolerant.**
- Szegedy/QSA/quantised PT (P8, P31, P44), continuous QSVT samplers (P44, P45).
- Provable quadratic query speedups.
- Resource estimates for *simpler* energies (Ising, SK, LABS) already show crossover times of ~1 year or more at a quadratic speedup (P55, P56).
- The only beyond-quadratic claims with FT estimates (P46) rest on n ≤ 10 extrapolation, for SK.
- **Verdict:** the only scientifically defensible route, and at present a **category 3/6 (resource-estimate / theory) claim at best**. Its relevance depends on a classical measurement of δ(L).

---

## (7) Protein mapping and connection to S29–S33

**Mapping.**
- SP-1 (posterior over decoded CA traces under an esmprior-like energy) maps onto a quantised PT/RELD walk (P44), or QSA along β (P31).
- The output would be qsamples of the same distribution a classical sampler targets. By H-001/R9 logic, a quantum sampler **cannot change the distribution or add information**. It can only reduce cost.
- A quantum claim here is therefore purely about computational cost (category 3/6). It needs a demonstrated classical cost gap.

**What S29–S33 did and did not test.**
- **Not tested:** quantum walks, QSA, QMCMC, rejection sampling, fault-tolerant estimates (S29–S33 README §5).
- **Tested adjacent:**
  - A tempered Born machine is at best an exact Gibbs sampler, "which classical Metropolis also targets" (R9).
  - Metropolis came closer to the exact Gibbs mean than the Born machine on 9/10 targets (fact 10, Q-C19).
  - At 18 qubits Metropolis was near-exact. **That is direct evidence that mixing was not hard on the registers tested.**
- **Why earlier approaches failed:** diagonal register energies consumed via argmin, prefix or convex readouts (H-001); register energy did not transmit to the chain (fact 5).

**What would be different now.**
1. **Continuous coordinates**, not registers.
2. **The target is the posterior itself**, whose soft average carried the only positive signal (1.40× MDE, mid30).
3. **Lengths ≥ 60–150 aa**, where mixing may become hard.

**Preconditions from this literature for a quantum sampling claim to be relevant (to pre-register in the C-1 kill test).**
- (a) **Measured classical spectral gap or τ_int.** Use best-tuned PT/REMD, HMC and SMC, *and* a learned-proposal / Boltzmann-generator-style baseline, on the learned-energy posterior at T = 1.
  - It must grow **super-polynomially** in chain length, or reach ≳10^12 single-chain steps per effective sample at feasible lengths (§3.9 crossover).
- (b) **Landscape.** The slow mixing must come from **narrow, deep, isolated modes** (Woodard persistence, P74; Olivucci-type hidden wells, P45).
  - Broad entropic bottlenecks are handled classically by tempering and lifting.
- (c) **Warm-start path.** A β-annealing path with constant overlap between consecutive Gibbs states must exist (P7, P9, P44, P45). Otherwise the cold-start √N penalty applies.
- (d) **Sample value.** Better samples must improve the built chain beyond MDE (the map's SP-1 condition ii).
- (e) **Speedup size.** Expect **quadratic in the gap (√δ)**. Treat any super-quadratic claim as unverified unless it is proven or shown at n ≫ 10.
- (f) **Oracle cost.** The per-step Toffoli count for the learned-energy walk operator (§3.9) must be estimated explicitly, including coherent coordinate arithmetic and pair-table loading.

---

## (8) Literature gaps (novelty ≠ advantage)

1. **No measurement of mixing times or spectral gaps for learned-energy protein posteriors** (pair-distance or ESM-derived) as a function of length. This is the decisive missing datum, and it is classical.
2. **No fault-tolerant resource estimate for a Metropolis/Szegedy/QSVT walk on a continuous molecular or protein energy**, whether a force field or a learned potential. Existing estimates are for Ising, SK and LABS only (P55, P56, P46).
3. **No quantum-vs-PT/REMD comparison** on any biomolecular sampling task. Positive quantum results compare against local/uniform Metropolis.
4. **No analysis of coherent oracles for pair-specific learned tables**, or for neural-network potentials (data loading, reversible evaluation).
5. **No test of whether the continuous-space provable separations (P45) have instances resembling protein landscapes.** Hide-and-seek narrow wells vs funnelled landscapes is open.
6. **QFold has no follow-up** with a coherent energy oracle, a sampling (not TTS) metric, or a PT baseline.
7. **Super-quadratic claims (P46, P47) lack large-n validation.** An independent classical-simulation or bound study for structured continuous targets is missing.

Filling gaps 2, 4 and 5 would be *novel*. Novelty is not advantage: a first resource estimate is likely to show a *negative* crossover, which is itself publishable (category 6).

---

## (9) Unverified leads (not cited as evidence)

- Crosson & Harrow, simulated quantum annealing vs SA separations (FOCS 2016). I believe it exists; not fetched.
- The Temme et al. Nature paper's actual quantitative resource statements; only the abstract was fetched.
- The QROM data-loading cost statement in Babbush et al. 2018 (P60), linear in entries. The paper's existence is verified; the cost claim was not verified in this session.
- The journal reference for Dunjko & Briegel (P10), believed to be New J. Phys. 2015; not confirmed on the fetched page.
- Arai & Kadowaki (P53): Sci. Rep. volume/article number not verified.
- "Quantum Dynamical Hamiltonian Monte Carlo" (arXiv 2403.01775): seen in search results only; not fetched.
- "Convergence monitoring of quantum Gibbs samplers" (arXiv 2608.02038): seen in search results only; not fetched.
- "Exploring Quantum Annealing for Coarse-Grained Protein Folding" (arXiv 2508.10660): seen in search results only; not fetched.
- "Quantum-enhanced MCMC for combinatorial optimization" (arXiv 2602.06171) and "Methods for non-variational heuristic quantum optimisation" (arXiv 2602.01353): seen in search results only; not fetched.

---

## (10) Bottom-line verdicts per primitive

| Primitive | Verdict |
|---|---|
| Szegedy walk / quantised Metropolis (FT) for the SP-1 posterior | **INTERESTING** as a theory/resource target; **WEAK** as a practical-advantage route |
| QSA / adaptive QSA (Bayesian-inference framing) | **INTERESTING** (conditional) |
| Continuous QSVT / quantum Langevin / quantum RELD samplers | **INTERESTING** (the highest-priority *theory* line inside Domain A; not HIGH PRIORITY) |
| Beyond-quadratic fully-quantum walks (Incudini–Mazzola) | **WEAK** |
| Nonreversible-chain quantum acceleration (Claudon et al.) | **WEAK** |
| Quantum Metropolis / quantum Gibbs samplers (Temme, CKBG/CKG, Davies, Poulin–Wocjan, Chowdhury–Somma) applied to classical protein energies | **KILLED** as a distinct source of advantage |
| Quantum rejection sampling (prior → posterior) | **WEAK** |
| Quantum fast-forwarding | **WEAK** |
| Amplitude estimation of posterior expectations | **WEAK** (conditional) |
| QeMCMC (Layden) and variants (NISQ) | **KILLED** for protein structure; **WEAK** in general |
| Quantum annealers as Boltzmann samplers | **KILLED** |
| QFold as evidence of a protein quantum-sampling advantage | **KILLED** |

**Szegedy walk / quantised Metropolis (FT) for the SP-1 posterior: INTERESTING as a theory/resource target; WEAK as a practical-advantage route.**
- The speedup is provably quadratic in the gap, but only with a warm-start or annealing path; from a cold start there is a √N penalty (P9).
- Resource estimates on simpler energies give ~1-year crossovers (P56) and require ~ns logical gates (P55).
- A learned pair-distance energy is plausibly *more* expensive per step (§3.9).
- It is worth a classical kill test (δ(L) under best PT/REMD and learned samplers) plus a paper resource estimate, because that combination is novel and decisive either way. It should not be built.

**QSA / adaptive QSA (Bayesian-inference framing): INTERESTING (conditional).**
- It is the formally cleanest match to "sample a posterior along a temperature path" (P31).
- It needs few samples, which suits S33's soft readout.
- It inherits the same quadratic ceiling and oracle costs as the walk.

**Continuous QSVT / quantum Langevin / quantum RELD samplers: INTERESTING. This is the highest-priority theory line inside Domain A, but not HIGH PRIORITY.**
- It is the best formal match to SP-1: a continuous non-convex energy with a quantised replica exchange (P44).
- It includes the first *provable* continuous-domain separation (P45).
- The gain is quadratic in barrier amplitude or Poincaré constant.
- It is query-model only, with warm-start assumptions and no gate-level costs.
- The hard instances are needle-like wells whose relevance to protein landscapes is unknown. That relevance is testable classically: look for narrow, deep isolated modes at T = 1.

**Beyond-quadratic fully-quantum walks (Incudini–Mazzola): WEAK.**
- It is the only published "sub-day crossover" FT estimate, which is significant if true.
- The sixth-degree scaling is fitted on n ≤ 10 exact SK matrices, against local/uniform Metropolis, not PT.
- The proposal relies on Hamiltonian simulation of H_prob, which is unexplored for continuous learned energies.
- It should be watched, not built on.

**Nonreversible-chain quantum acceleration (Claudon et al.): WEAK.**
- "Up-to-exponential" is relative to a chain's own mixing time under a hard-to-check condition, shown in toy examples.
- Classical nonreversible and lifted chains already capture part of the gain (P14, P15).

**Quantum Metropolis / quantum Gibbs samplers applied to classical protein energies: KILLED as a distinct source of advantage.**
- Covers Temme et al., CKBG/CKG, Davies-generator samplers, Poulin–Wocjan and Chowdhury–Somma.
- For a diagonal energy they reduce to classical Metropolis plus at most the walk speedup.
- The brute-force variants scale as √(D/Z) or D^α, exponential in the number of degrees of freedom.
- They remain relevant only for genuinely quantum Hamiltonians, which are out of SP-1 scope.

**Quantum rejection sampling (prior → posterior): WEAK.**
- There is a quadratic gain in 1/P_acc (P36, P37).
- It requires a *coherent* circuit for the learned prior/decoder (an iterative L-BFGS/DG decoder or a neural network run reversibly), which is prohibitive.
- Classical SMC/importance sampling are not plain rejection sampling.

**Quantum fast-forwarding: WEAK.** It gives a quadratic gain on transients. Nothing in S29–S33 indicates that transient relaxation is a bottleneck: decodes are restart-saturated (R10).

**Amplitude estimation of posterior expectations: WEAK (conditional).** It is the O(1/ε) vs O(1/ε²) gain (P30). It stays WEAK until the C-3 variance audit shows a variance-limited decision. The map already rates QA-1 low-prior.

**QeMCMC (Layden) and variants (NISQ): KILLED for protein structure; WEAK in general.**
- The gains are empirical at n ≤ 10, against local/uniform proposals.
- They are bounded or disputed (P48, P49) and partly dequantised (P50).
- The protein mapping needs diagonal register encodings, which failed condition C in S29–S33.

**Quantum annealers as Boltzmann samplers: KILLED.**
- The effective temperature is uncontrolled and the devices sample noisy Gibbs states (P61–P63).
- Protein uses are optimisation or low-resolution path demonstrations without an advantage over classical methods (P67–P71).
- Classical QMC matches tunnelling scaling (P64).

**QFold as evidence of a protein quantum-sampling advantage: KILLED.**
- The oracle is built by exhaustive classical enumeration.
- The instances have 64–1,024 states.
- It measures optimisation TTS, not sampling quality.
- The baseline is matched Metropolis only.
- The headline exponent is ~0.85–0.89, and the 10^87–10^373 extrapolation is unsupported.
- It is useful only as a catalogue of pitfalls.

**Overall.**
- For the program's leading candidate (AA-1/SP-1), the literature supports **at most a quadratic, fault-tolerant, query-model speedup, conditional on a measured classical mixing bottleneck that nobody has measured**.
- Every published practical estimate at a quadratic speedup is negative.
- The correct next step is classical (C-1 kill test with PT/REMD, HMC, SMC and a learned-sampler baseline), followed by a paper resource estimate (§3.9 made rigorous).
- A strong negative is the most likely outcome and would be publishable.
