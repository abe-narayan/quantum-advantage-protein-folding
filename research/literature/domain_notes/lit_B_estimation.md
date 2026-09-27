# Domain B: quantum estimation, Monte Carlo speedup, partition functions, free energies, and what they cost in practice

_Literature evidence notes for the coordinator. Compiled 2026-09-26 by the Domain-B literature agent. No experiments were run and no repo files were edited._

**Key question.** Is any protein-structure computation plausibly limited by Monte Carlo **variance**? The candidates are an ensemble expectation, a free-energy difference, the partition function of a conformational model, and an uncertainty estimate. If one is, could a quadratic *precision* speedup (O(1/ε) vs O(1/ε²)) still matter after the costs of the oracle, state preparation and error correction?

**Short answer (details in §10).** Probably not, on the evidence available.
- Every protein-relevant ensemble estimate in the literature is limited by one of three things:
  - **mixing / decorrelation time** (τ), not by the variance factor σ²/ε²;
  - **force-field / model bias**;
  - (in this program's own evidence) **information**.
- The quadratic 1/ε gain applies only to the σ²/ε² factor. That factor is small at the precision protein decisions need.
- The published crossover arithmetic (Babbush et al. 2021; Sanders et al. 2020) puts break-even for quadratic speedups at **months to millennia** of fault-tolerant runtime, even for primitives far cheaper than a protein energy evaluation.
- The only asymptotically interesting component for proteins is the quadratic **spectral-gap** (√δ) improvement from quantum walks. That belongs to Domain A / AA-1, and it depends on a classical mixing-time measurement that has never been made (OP-01).

---

## 1. Scope and search log

**Scope.** This section covers:
- amplitude amplification and estimation (AE), and quantum counting;
- QPE-free, low-depth and variational AE;
- quantum mean estimation (bounded variance, heavy tails);
- lower bounds (Heinrich/Novak, Nayak–Wu, Chen–Nannicini);
- quantum partition-function algorithms (WCNA09, Montanaro, Harrow–Wei, AHNTW, Cornelissen–Hamoudi);
- quantum free-energy proposals (Liouvillian / Koopman–von Neumann, QM/MM bookending on hardware);
- the state-preparation bottleneck (Grover–Rudolph, Herbert, qGAN, Carrera Vazquez–Woerner);
- end-to-end fault-tolerant resource estimates (finance QAE, quantum-walk simulated annealing);
- crossover analyses (Babbush, Sanders, Campbell–Khurana–Montanaro, Hoefler–Häner–Troyer, Beverland);
- classical competitors (MBAR/BAR/TI/Jarzynski, AIS, SMC, Wang–Landau, nested sampling, QMC, SVV annealing);
- protein-specific free-energy and partition-function practice (FEP, K*/BBK*, weighted counting, MD sampling limits).

**Search / fetch log** (WebSearch queries and WebFetch/API targets, in order):
1. arXiv abs pages fetched: quant-ph/0005055, quant-ph/9805082, 1904.10246, 1912.05559, 2012.03348, 2109.03687, 1504.06987, quant-ph/0105116, 0811.0596, 2009.11270, 2207.08643, quant-ph/0208112, 2101.02240, 2105.09100, 2012.03819.
2. WebSearch: `Harrow Wei "Adaptive quantum simulated annealing for Bayesian inference and estimating partition functions" arXiv` → 1907.09965. Also surfaced 2404.02414, which was fetched.
3. arXiv abs fetched: 1907.09965, 2404.02414, 2011.04149, 1905.02666, 1806.06893, 2307.14310.
4. Babbush et al. PDF, full text extracted with pdftotext. The crossover formulas and Tables I–II were read in full.
5. arXiv abs fetched: 2007.07391, 1910.01659, 0804.1571, 0905.2199, cs/0612058, quant-ph/9804066, 1807.06456, 2208.07544, 2108.12172, 1908.10846, 2006.16223, 2307.00523, 0801.1426, physics/9803008, cond-mat/0011174.
6. WebSearch:
   - `Del Moral Doucet Jasra 2006 "Sequential Monte Carlo samplers" ... doi`
   - `Skilling 2006 "Nested sampling for general Bayesian computation" ...`
   - `Dick Kuo Sloan "High-dimensional integration: the quasi-Monte Carlo way" ...`
   - `Grossfield ... "Best practices for quantifying uncertainty and sampling quality..."`
   - `Mobley Gilson 2017 "Predicting binding free energies..."`
   - `quantum algorithm free energy estimation molecular binding amplitude estimation arXiv` → 2508.16719, 2506.20825
   - `Neal "Annealed importance sampling" Statistics and Computing 2001 ...`
   - `OSPREY K* algorithm epsilon-approximate partition function ...`
   - `Viricel Simoncini Barbe de Givry Schiex "Guaranteed weighted counting..."`
   - `Simon Santagati ... "Improved precision scaling..."`
   - `quantum amplitude estimation protein conformational ensemble Boltzmann average quadratic speedup` → 2603.12334, 2411.03972
   - `quantum walk Metropolis molecular conformations quantum speedup sampling protein arXiv resource estimate` → 2607.22818, 2506.11576
   - `Wang et al. 2015 JACS "Accurate and reliable prediction..."`
   - `Chodera Mobley Shirts ... 2011 "Alchemical free energy methods for drug discovery..."`
7. Crossref API: 10.1089/cmb.2017.0267 (BBK*), 10.1007/978-3-319-44953-1_46 (Viricel), 10.1103/PhysRevE.103.063302 (Herbert PRE title), 10.1016/0021-9991(76)90078-4 (Bennett), 10.1063/1.1749657 (Kirkwood). Zwanzig 10.1063/1.1740409 returned HTTP 429 and was **not verified**.
8. Europe PMC REST API (PubMed was blocked by a CAPTCHA): PMIDs 25625324, 21349700, 28399632, 30533602, 22034434.
9. arXiv export API: quant-ph/0401053, 1904.00043, 2203.12497, 2006.14510, 2006.14145, 2111.12509, 2310.03011, 1810.05582.
10. Full-text PDF extraction for exact theorem statements:
    - Montanaro 1504.06987 (Table 1, §1.3–1.4, Theorem 11, Cor. 13);
    - Arunachalam et al. 2009.11270 (§1.1–1.2);
    - Cornelissen–Hamoudi 2207.08643 (Theorem 4.1 informal, Tables 1–2);
    - Harrow–Wei 1907.09965 (Theorem 1, Table 1);
    - WCNA09 0811.0596 (Theorem 1);
    - Chakrabarti et al. 2012.03819 (Table 1, conclusion);
    - Herbert 2101.02240;
    - Dalzell et al. 2310.03011 (§8.2 Option pricing, §15 Gibbs sampling);
    - Mobley–Gilson bioRxiv 074625v2.
11. WebFetch arXiv HTML for 2508.16719 (theorem and caveats) and 2603.12334 (method and limitations).

**Tooling caveats.**
- PDF text extraction lost some Unicode symbols (√, ε, δ, τ, ℓ). I reconstructed formulas only where the surrounding text makes them unambiguous. Where I could not, I quote the abstract instead.
- Complexities marked Õ hide polylog factors.

---

## 2. Verified papers

Format: **[ID] Title**, followed by the fields below.

- **Header line:** authors · year · venue · DOI · arXiv · **Verified:** the URL checked.
- **Alg / setting / claim / assumptions / comparator / type / limitations / LABEL(S).**

Label vocabulary: THEORETICAL SPEEDUP | QUERY-COMPLEXITY SPEEDUP | ASYMPTOTIC SPEEDUP | SAMPLING SPEEDUP | HEURISTIC ADVANTAGE | EMPIRICAL ADVANTAGE | HARDWARE DEMONSTRATION | SIMULATOR RESULT | ORACLE-MODEL RESULT | NO ADVANTAGE | ADVANTAGE DISPUTED.

### 2A. Amplitude amplification, estimation and counting

**[B1] Quantum Amplitude Amplification and Estimation**
- Brassard, Høyer, Mosca, Tapp · 2002 · AMS Contemporary Mathematics 305:53–74 · arXiv quant-ph/0005055 · **Verified:** https://arxiv.org/abs/quant-ph/0005055
- **Alg:** amplitude amplification (AA) and amplitude estimation (AE), based on phase estimation of the Grover iterate.
- **Setting:** an algorithm A prepares Σα_x|x⟩; the probability *a* of a "good" output is to be estimated.
- **Claim (abstract):** "Amplitude amplification is a process that allows to find a good x after an expected number of applications of A and its inverse which is proportional to 1/√a, assuming algorithm A makes no measurements."
- AE estimates *a* to additive error ε with O(1/ε) applications of A. Classical repeated sampling needs O(1/ε²).
- **Assumptions:** A is available as a coherent unitary (no mid-circuit measurement), and A⁻¹ is available.
- **Comparator:** classical repeated sampling.
- **Type:** theoretical.
- **Limitation:** the counts are **queries to A**. They ignore the cost of A, the controlled powers of A, and the QFT.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP, ORACLE-MODEL RESULT.

**[B2] Quantum Counting**
- Brassard, Høyer, Tapp · 1998 · ICALP 1998, LNCS 1443:820–831 · arXiv quant-ph/9805082 · **Verified:** https://arxiv.org/abs/quant-ph/9805082
- **Claim:** "we combine ideas from Grover's and Shor's quantum algorithms to perform approximate counting, which can be seen as an amplitude estimation process."
- **LABELS:** QUERY-COMPLEXITY SPEEDUP, ORACLE-MODEL RESULT.

**[B3] Quantum Approximate Counting, Simplified**
- Aaronson, Rall · 2020 · SOSA 2020, 24–32 · arXiv 1908.10846 · **Verified:** https://arxiv.org/abs/1908.10846
- **Claim:** the BHMT count uses "O(1/ε√(N/K)) queries"; a QFT-free algorithm achieves "the same query complexity using Grover iterations only", with a generalisation to QFT-free AE.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B4] Amplitude estimation without phase estimation (MLAE)**
- Suzuki, Uno, Raymond, Tanaka, Onodera, Yamamoto · 2020 · Quantum Inf. Process. 19, 75 · arXiv 1904.10246 · **Verified:** https://arxiv.org/abs/1904.10246
- **Alg:** maximum-likelihood estimation over circuits with different numbers of Grover iterates. No controlled-Q and no QFT.
- **Claim:** "Numerical simulations we conducted demonstrate that our algorithm asymptotically achieves nearly the optimal quantum speedup with a reasonable circuit length."
- **Type:** numerical (simulator).
- **Limitation:** the Grover powers still need depth ∝ 1/ε for Heisenberg scaling.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP, SIMULATOR RESULT.

**[B5] Iterative Quantum Amplitude Estimation**
- Grinko, Gacon, Zoufal, Woerner · 2021 · npj Quantum Inf. 7, 52 · DOI 10.1038/s41534-021-00379-1 · arXiv 1912.05559 · **Verified:** https://arxiv.org/abs/1912.05559
- **Claim:** "we ... prove that it achieves a quadratic speedup up to a double-logarithmic factor compared to classical Monte Carlo simulation."
- **Type:** theorem plus empirical comparison against other QAE variants, not against classical MC practice.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B6] Low depth algorithms for quantum amplitude estimation**
- Giurgica-Tiron, Kerenidis, Labib, Prakash, Zeng · 2022 · Quantum 6, 745 · arXiv 2012.03348 · **Verified:** https://arxiv.org/abs/2012.03348
- **Claim (abstract):** "For β ∈ (0,1], our algorithms require N = Õ(1/ε^(1+β)) oracle calls and require the oracle to be called sequentially D = O(1/ε^(1−β)) times."
- **Meaning:** an explicit depth–speedup trade-off. With depth capped at D, the quantum advantage in total calls is at most ≈ D. The analysis includes depolarizing noise.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP (interpolating).

**[B7] Variational quantum amplitude estimation (VQAE)**
- Plekhanov, Rosenkranz, Fiorentini, Lubasch · 2022 · Quantum 6, 670 · arXiv 2109.03687 · **Verified:** https://arxiv.org/abs/2109.03687
- **Claim (abstract, verbatim):** "VQAE typically has larger computational requirements than classical MC sampling. To reduce the variational cost, we propose adaptive VQAE and numerically show in 6 to 12 qubit simulations that it can outperform classical MC sampling."
- **Type:** 6–12-qubit simulations.
- **LABELS:** HEURISTIC ADVANTAGE (small-scale, simulator), SIMULATOR RESULT. The authors themselves flag that it is usually worse than classical MC.

**[B8] Faster Amplitude Estimation**
- Nakaji · 2020 · Quantum Inf. Comput. (2020) · arXiv 2003.02417 · **Verified:** https://arxiv.org/abs/2003.02417
- **Claim:** a query upper bound that "almost achieves the Heisenberg scaling" with a small constant.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B9] Amplitude Estimation from Quantum Signal Processing**
- Rall, Fuller · 2023 · Quantum 7, 937 · DOI 10.22331/q-2023-03-02-937 · arXiv 2207.08628 · **Verified:** https://arxiv.org/abs/2207.08628
- **Claim:** QSP-based AE offering "non-destructive estimation without any assumptions on the amplitude ... unbiased amplitude estimation ... a simpler method for trading quantum circuit depth for more repetitions".
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B10] Quantum Amplitude Estimation in the Presence of Noise**
- Brown, Goktas, Tham · 2020 · arXiv 2006.14145 (no journal reference in the arXiv metadata) · **Verified:** arXiv export API, id 2006.14145
- **Claim:** under noise "one must choose a schedule that balances the trade-off between the greater ideal performance achieved by higher-depth circuits, and the correspondingly greater accumulation of noise-induced error."
- **LABELS:** SIMULATOR RESULT. It is a noise analysis that limits the advantage.

**[B11] Amplitude estimation via maximum likelihood on noisy quantum computer**
- Tanaka, Suzuki, Uno, Raymond, Onodera, Yamamoto · 2021 · Quantum Inf. Process. 20, 293 · DOI 10.1007/s11128-021-03215-9 · arXiv 2006.16223 · **Verified:** https://arxiv.org/abs/2006.16223
- **Claim (abstract):** "the proposed maximum likelihood estimator achieves quantum speedup in the number of queries, though the estimation error saturates due to the noise."
- **Type:** IBM superconducting hardware, with a toy oracle.
- **LABELS:** HARDWARE DEMONSTRATION (query scaling only on a toy problem; the error floor is set by noise); NO ADVANTAGE in wall-clock.

### 2B. Quantum mean estimation, Monte Carlo speedup and lower bounds

**[B12] Quantum speedup of Monte Carlo methods**
- Montanaro · 2015 · Proc. R. Soc. A 471, 20150301 · arXiv 1504.06987 · **Verified:** https://arxiv.org/abs/1504.06987, plus PDF full text
- **Claim (abstract):** "The algorithm estimates the expected output value of an arbitrary randomised or quantum subroutine with bounded variance, achieving a near-quadratic speedup over the best possible classical algorithm."
- **Table 1** (from the text):
  - bounded output in [0,1]: Õ(1/ε) uses of A;
  - Var ≤ σ²: Õ(σ/ε) uses;
  - relative variance ≤ B: Õ(√B/ε) uses.
- Classical needs O(σ²/ε²). The paper motivates this with: "to estimate μ up to 4 decimal places we would need to run A over 100 million times".
- **Partition functions (§1.3; Theorem 11; Cor. 13):**
  - Quantum: Õ((log A)·√τ·(√τ + 1/ε)) steps, where A = |Ω| and τ is the relaxation time, *including* classical construction of the cooling schedule.
  - Classical SVV: "quadratically worse dependence on both τ and ε".
  - Example: ferromagnetic Ising above T_c. Quantum "O(n^{3/2}/ε + n²) steps. The corresponding classical algorithm uses O(n²/ε²) steps."
- **Caveat stated by the paper:** a general quadratic quantum-walk mixing speedup is not known, because the dependence on π_min "cannot be kept logarithmic" in general. The paper says proving it "would imply a polynomial-time quantum algorithm for graph isomorphism."
- **Assumptions:** coherent access to A; for Markov chains, a slowly varying sequence of chains (Wocjan–Abeyesinghe) and a known gap bound.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP, THEORETICAL SPEEDUP, ORACLE-MODEL RESULT.

**[B13] Quantum Summation with an Application to Integration**
- Heinrich · 2001 (submitted to J. Complexity) · arXiv quant-ph/0105116 · **Verified:** https://arxiv.org/abs/quant-ph/0105116
- **Claim:** quantum algorithms for the means of p-summable sequences and for L_p integration, "We also prove lower bounds which show that the proposed algorithms are, in many cases, optimal".
- **Role:** this is the origin of the optimal O(1/ε) quantum mean estimator, and of the quantum **lower bound** that caps the speedup at quadratic.
- **LABELS:** THEORETICAL SPEEDUP (query), with a matching lower bound.

**[B14] Quantum Integration in Sobolev Classes**
- Heinrich · 2001 · arXiv quant-ph/0112153 · **Verified:** https://arxiv.org/abs/quant-ph/0112153
- **Claim:** optimal rates for quantum integration of W^r_p([0,1]^d), with lower bounds.
- **LABELS:** THEORETICAL SPEEDUP.

**[B15] Quantum Complexity of Integration**
- Novak · 2001 · J. Complexity 17, 2–16 · arXiv quant-ph/0008124 · **Verified:** https://arxiv.org/abs/quant-ph/0008124
- **Claim (abstract):** "(1) there is an exponential speed-up of quantum algorithms over deterministic (classical) algorithms, if the smoothness is small; (2) there is a (roughly) quadratic speed-up of quantum algorithms over randomized classical methods, if the smoothness is small."
- **Implication:** the relative quantum gain **shrinks as integrand smoothness grows**, which is exactly the regime where classical QMC is strong.
- **LABELS:** THEORETICAL SPEEDUP (worst case over function classes).

**[B16] The quantum query complexity of approximating the median and related statistics**
- Nayak, Wu · 1998 · arXiv quant-ph/9804066 (journal/conference version not verified) · **Verified:** https://arxiv.org/abs/quant-ph/9804066
- **Claim:** "We prove a lower bound of Ω(min{1/ε, n}) queries ... [the degree bound] also immediately yields lower bounds for ... approximating the mean of a sequence of numbers."
- **Role:** the quantum mean-estimation lower bound. **No better than quadratic is possible** in the black-box model.
- **LABELS:** THEORETICAL (lower bound).

**[B17] Quantum Chebyshev's Inequality and Applications**
- Hamoudi, Magniez · 2019 · ICALP 2019, LIPIcs 132 · arXiv 1807.06456 · **Verified:** https://arxiv.org/abs/1807.06456
- **Claim:** quantum mean estimation with relative-variance guarantees, and quadratic speedups for estimating edge and triangle counts.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B18] Quantum Sub-Gaussian Mean Estimator**
- Hamoudi · 2021 · ESA 2021, LIPIcs 204, 50:1–50:17 · arXiv 2108.12172 · **Verified:** https://arxiv.org/abs/2108.12172
- **Claim:** "a nearly-optimal quadratic speedup over the number of classical i.i.d. samples needed to estimate the mean of a heavy-tailed distribution with a sub-Gaussian error rate."
- **Relevance:** exponential-average free-energy estimators (Zwanzig/Jarzynski) have heavy tails. The quantum speedup is still **quadratic** here.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B19] Mean estimation when you have the source code; or, quantum Monte Carlo methods**
- Kothari, O'Donnell · 2022 · arXiv 2208.07544 (venue not verified) · **Verified:** https://arxiv.org/abs/2208.07544
- **Claim:** "runs the code O(n) times and returns an estimate ... |μ̂ − μ| ≤ σ/n ... This dependence on n is optimal for quantum algorithms ... classical algorithms ... can only achieve the quadratically worse |μ̂ − μ| ≤ σ/√n."
- **LABELS:** QUERY-COMPLEXITY SPEEDUP (optimal; tight quadratic).

**[B20] Quantum-accelerated multilevel Monte Carlo methods for SDEs in mathematical finance**
- An, Linden, Liu, Montanaro, Shao, Wang · 2021 · Quantum 5, 481 · arXiv 2012.06283 · **Verified:** https://arxiv.org/abs/2012.06283
- **Claim:** "a quantum algorithm that gives a quadratic speed-up for multilevel Monte Carlo methods in a general setting."
- **Relevance:** the classical variance-reduction baseline (MLMC) can itself be quantized, but the gain is again only quadratic.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

### 2C. Quantum walks, qsampling and partition functions

**[B21] Spectra of Quantized Walks and a √(δε) rule**
- Szegedy · 2004 · arXiv quant-ph/0401053 (FOCS 2004 version not verified here) · **Verified:** arXiv export API, id quant-ph/0401053
- **Claim:** the classical cost O(℘0 + (℘1+℘2)/(δε)) becomes quantum "O(℘0 + (℘1+℘2)/√(δε)) ... We refer to this as the √(δε) rule."
- **Role:** the source of the quadratic spectral-gap improvement used by every quantum partition-function algorithm below.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B22] Quantum Simulations of Classical Annealing Processes**
- Somma, Boixo, Barnum, Knill · 2008 · PRL 101, 130504 · arXiv 0804.1571 · **Verified:** https://arxiv.org/abs/0804.1571
- **Claim:** "It requires order 1/√δ steps to find an optimal solution with bounded error probability, where δ is the minimum spectral gap of the stochastic matrices used in the classical annealing process. This is a quadratic improvement over the order 1/δ steps".
- **LABELS:** ASYMPTOTIC SPEEDUP (walk steps), ORACLE-MODEL RESULT.

**[B23] Speed-up via Quantum Sampling**
- Wocjan, Abeyesinghe · 2008 · PRA 78, 042336 · arXiv 0804.4259 · **Verified:** https://arxiv.org/abs/0804.4259
- **Claim:** a quantum algorithm to prepare "a quantum sample, i.e., a coherent version of the stationary distribution of a reversible Markov chain", given slowly varying chains.
- **LABELS:** ASYMPTOTIC SPEEDUP (conditional on the slowly varying sequence).

**[B24] Quantum Speed-up for Approximating Partition Functions**
- Wocjan, Chiang, Nagaj, Abeyesinghe · 2009 · PRA 80, 022340 · arXiv 0811.0596 · **Verified:** https://arxiv.org/abs/0811.0596, plus PDF
- **Claim (abstract):** "a quadratic reduction with respect to the spectral gap of the underlying Markov chains and a quadratic reduction with respect to the parameter characterizing the desired accuracy ... Both reductions are intimately related and cannot be achieved separately."
- **Setting:** annealing FPRAS with non-adaptive cooling schedules.
- **LABELS:** ASYMPTOTIC SPEEDUP (walk-step count), ORACLE-MODEL RESULT.

**[B25] Sampling from the thermal quantum Gibbs state and evaluating partition functions with a quantum computer**
- Poulin, Wocjan · 2009 · PRL 103, 220502 · arXiv 0905.2199 · **Verified:** https://arxiv.org/abs/0905.2199
- **Claim:** Gibbs-state preparation with a "universal upper bound D^α on the thermalization time ... α < 1/2". The partition function is evaluated in time "inversely proportional to the targeted accuracy squared".
- **LABELS:** THEORETICAL SPEEDUP (quantum Hamiltonians; exponential in the worst case).

**[B26] Adaptive Quantum Simulated Annealing for Bayesian Inference and Estimating Partition Functions**
- Harrow, Wei · 2020 · SODA 2020 · arXiv 1907.09965 · **Verified:** https://arxiv.org/abs/1907.09965, plus PDF
- **Claim (abstract):** the schedule "roughly matches the length of the best classical adaptive annealing schedules ... Our dependence on the Markov chain gap ... is quadratically better than what classical Markov chains achieve. Our algorithm is the first to combine both of these quadratic improvements."
- **Table 1 (counting):** quantum Õ(log|Ω|/(ε√δ)) vs classical SVV Õ(log|Ω|/(ε²δ)).
- **Ising example (§5):** quantum Õ(|V|^{3/2}/ε) vs classical Õ(|V|²/ε²).
- It also gives Bayesian-inference qsampling in Õ(√(E_{π0}[L])/√δ)-type bounds (symbols partly lost in extraction; see Theorem 1).
- **LABELS:** ASYMPTOTIC SPEEDUP, ORACLE-MODEL RESULT.

**[B27] Simpler (classical) and faster (quantum) algorithms for Gibbs partition functions**
- Arunachalam, Havlicek, Nannicini, Temme, Wocjan · 2022 · Quantum 6, 789 · arXiv 2009.11270 · **Verified:** https://arxiv.org/abs/2009.11270, plus PDF
- **Claims:**
  - Abstract: "a quadratic advantage in the number of required quantum samples compared to the number of random samples drawn by the best classical algorithm, and its computational complexity has quadratically better dependence on the spectral gap".
  - §1.2.4: Ising (Glauber, low β) "our classical algorithm achieves complexity Õ(n²·ε⁻²) ... The quantum algorithm in comparison achieves complexity of Õ(n^{3/2}·ε⁻¹)".
  - Schedule length O(√(ln|Ω| ln n)), matching the SVV conjecture.
  - The assumption of a qsample oracle "is not restrictive, as qsamples can be generated from a classical Markov chain ... [but] total running time ... must also account for the time ... taken to generate these samples."
- **Important classical side-result:** the paper also *improves the classical algorithm*. This illustrates that the classical baseline keeps moving.
- **LABELS:** ASYMPTOTIC SPEEDUP, ORACLE-MODEL RESULT.

**[B28] A Sublinear-Time Quantum Algorithm for Approximating Partition Functions**
- Cornelissen, Hamoudi · 2023 · SODA 2023, 1245–1264 · arXiv 2207.08643 · **Verified:** https://arxiv.org/abs/2207.08643, plus PDF
- **Claim (Theorem 4.1, informal):** "O~(log^{3/4}(|Ω|) log^{3/2}(n)/(ε√δ)) steps of the quantum walk operator", compared with classical Õ(log|Ω|/(ε²δ)) [SVV09; Hub15; Kol18].
- Abstract: "the first speed-up of this type to be obtained over the seminal nearly-linear time algorithm of Štefankovič, Vempala and Vigoda."
- The paper also gives "a nearly unbiased quantum mean estimator that reduces the variance quadratically faster than the classical empirical mean."
- **Applications (Table 2):**
  - Ising/colourings/independent sets: Õ(|V|^{1.25}/ε) vs classical Õ(|V|²/ε²);
  - convex-body volume: Õ(d³ + d^{2.25}/ε).
- **The paper notes** that preparing qsamples at low temperature is "significantly harder" than reflecting through them. This is why every algorithm recycles qsamples non-destructively.
- **LABELS:** ASYMPTOTIC SPEEDUP (walk steps; the log^{1/4}|Ω| gain is super-quadratic in no parameter), ORACLE-MODEL RESULT.

**[B29] A simple lower bound for the complexity of estimating partition functions on a quantum computer**
- Chen, Nannicini · 2024 · arXiv 2404.02414 · **Verified:** https://arxiv.org/abs/2404.02414
- **Claim:** "a Ω(1/ε) lower bound for the number of reflections needed to estimate the partition function with a quantum algorithm."
- **Role:** in the reflection model, the ε-dependence **cannot beat** the quadratic improvement.
- **LABELS:** THEORETICAL (lower bound).

**[B30] Quantum algorithms for Gibbs sampling and hitting-time estimation**
- Chowdhury, Somma · 2017 · QIC 17(1/2), 41–64 · arXiv 1603.02940 · **Verified:** https://arxiv.org/abs/1603.02940
- **Claim:** Gibbs-state preparation "almost linear in √(Nβ/Z)" (N = Hilbert-space dimension). Hitting-time estimation in "1/(εΔ^{3/2})", "quadratically improv[ing] the dependence on 1/ε and 1/Δ".
- **LABELS:** QUERY-COMPLEXITY / ASYMPTOTIC SPEEDUP (worst case exponential in n).

**[B31] Adiabatic Quantum State Generation and Statistical Zero Knowledge**
- Aharonov, Ta-Shma · 2003 · arXiv quant-ph/0301023 (STOC 2003 version not verified) · **Verified:** https://arxiv.org/abs/quant-ph/0301023
- **Role:** frames qsampling (coherent stationary distributions) as "state generation" and links it to SZK and graph isomorphism. Generic efficient qsampling of arbitrary Markov-chain stationary distributions would be surprising (Montanaro [B12] cites this line).
- **LABELS:** THEORETICAL (hardness context).

**[B32] Efficient Quantum Walk Circuits for Metropolis-Hastings Algorithm**
- Lemieux, Heim, Poulin, Svore, Troyer · 2020 · Quantum 4, 287 · arXiv 1910.01659 · **Verified:** https://arxiv.org/abs/1910.01659
- **Claim:** "a direct implementation of this oracle requires costly arithmetic operations"; they reformulate the walk to avoid it. "Our numerical results indicate polynomial quantum speedups in heuristic settings."
- **LABELS:** SIMULATOR RESULT, HEURISTIC ADVANTAGE (walk steps only).

**[B33] Quantum Circuits for the Metropolis-Hastings Algorithm**
- Claudon, Rodenas-Ruiz, Piquemal, Monmarché · 2025/2026 · J. Phys. A 59, 305304 (2026) · arXiv 2506.11576 · **Verified:** https://arxiv.org/abs/2506.11576
- **Claim:** a Szegedy walk following the classical proposal–acceptance logic without extra reversible arithmetic. "we expect the end-to-end quadratic speedup to hold for MH Markov Chain Monte-Carlo simulations."
- **Note:** Piquemal's group works on molecular simulation, so this is the closest walk construction to molecular MCMC.
- **LABELS:** THEORETICAL SPEEDUP (expected, not a resource estimate).

**[B34] Practical advantage beyond the quadratic speedup limit with fully-quantum walks**
- Incudini, Mazzola · 2026 · arXiv 2607.22818 (preprint) · **Verified:** https://arxiv.org/abs/2607.22818
- **Claim (abstract):** "about a cubic polynomial asymptotic advantage over previous quantum-walks, resulting in a total sixth-degree polynomial queries speedup compared to the best classical walk ... the resulting advantage runtime crossover is reduced from approximately 10³ years for conventional quantum walks to less than one day."
- **Setting:** low-temperature Gibbs sampling of dense classical Ising models, with full FT compilation vs CPU/GPU/FPGA baselines.
- **Relevance:** it independently confirms that **conventional (quadratic) quantum walks have ~10³-year crossovers**. The super-quadratic claim is new, unreviewed and model-specific (dense Ising).
- **LABELS:** QUERY-COMPLEXITY SPEEDUP (super-quadratic, heuristic/empirical scaling); ADVANTAGE DISPUTED/UNREPLICATED (preprint).

**[B35] Quantum-enhanced Markov chain Monte Carlo**
- Layden, Mazzola, Mishmash, Motta, Wocjan, Kim, Sheldon · 2023 · Nature 619, 282–287 · DOI 10.1038/s41586-023-06095-4 · arXiv 2203.12497 · **Verified:** arXiv export API
- **Claim:** "this quantum algorithm converges in fewer iterations than common classical MCMC alternatives on relevant problem instances, both in simulations and experiments."
- **Note:** this is a sampling (Domain A) primitive. It is included because it is the only hardware-run quantum MCMC. The iteration count is not wall-clock, and the instances are small Ising models.
- **LABELS:** HARDWARE DEMONSTRATION, SAMPLING SPEEDUP (iterations), SIMULATOR RESULT.

### 2D. State preparation / data loading

**[B36] Creating superpositions that correspond to efficiently integrable probability distributions**
- Grover, Rudolph · 2002 · arXiv quant-ph/0208112 · **Verified:** https://arxiv.org/abs/quant-ph/0208112
- **Claim:** "a simple and efficient process for generating a quantum superposition of states which form a discrete approximation of any efficiently integrable (such as log concave) probability density functions."
- **LABELS:** THEORETICAL (state preparation).

**[B37] No quantum speedup with Grover-Rudolph state preparation for quantum Monte Carlo integration**
- Herbert · 2021 · PRE 103, 063302 · DOI 10.1103/PhysRevE.103.063302 · arXiv 2101.02240 (arXiv title: "The Problem with Grover-Rudolph State Preparation for Quantum Monte-Carlo") · **Verified:** https://arxiv.org/abs/2101.02240 and Crossref
- **Claim (abstract):** "We prove that there is no quantum speed-up when using quantum Monte-Carlo to estimate the mean (and other moments) of analytically-defined log-concave probability distributions prepared as quantum states using the Grover-Rudolph method."
- **Intro:** "the quadratic speed-up arises from comparing classical complexity to quantum query complexity, and if we take into account the additional operations needed to build increasingly precise oracles ... we find that there is no quantum advantage."
- **LABELS:** NO ADVANTAGE (theorem).

**[B38] Quantum Monte Carlo Integration: The Full Advantage in Minimal Circuit Depth**
- Herbert · 2022 · Quantum 6, 823 · arXiv 2105.09100 · **Verified:** https://arxiv.org/abs/2105.09100
- **Claim:** "retains the full quadratic quantum advantage, without requiring any arithmetic or quantum phase estimation to be performed on the quantum computer" (Fourier-series decomposition plus AE).
- **Limitation:** it still requires an efficient state-preparation circuit for the distribution. It is a remedy for the *integrand* side, not the *distribution* side.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP.

**[B39] Efficient State Preparation for Quantum Amplitude Estimation**
- Carrera Vazquez, Woerner · 2021 · Phys. Rev. Applied 15, 034027 · DOI 10.1103/PhysRevApplied.15.034027 · arXiv 2005.07711 · **Verified:** https://arxiv.org/abs/2005.07711
- **Claim (abstract):** "If state preparation is too expensive, it can diminish the quantum advantage. Preparing arbitrary quantum states has exponential complexity with respect to the number of qubits".
- **LABELS:** HARDWARE DEMONSTRATION (numerical-integration toy), SIMULATOR RESULT.

**[B40] Quantum Generative Adversarial Networks for Learning and Loading Random Distributions**
- Zoufal, Lucchi, Woerner · 2019 · npj Quantum Inf. 5, 103 · DOI 10.1038/s41534-019-0223-2 · arXiv 1904.00043 · **Verified:** arXiv export API
- **Claim:** exact loading is "O(2^n) gates", which "can easily predominate the complexity"; a qGAN loads approximately with poly(n) gates.
- **Limitation:** the approximation error of the loaded distribution caps the achievable ε. The training cost is not counted.
- **LABELS:** HEURISTIC, SIMULATOR RESULT, HARDWARE DEMONSTRATION (small).

### 2E. End-to-end resource estimates and crossover analyses (calibration)

**[B41] Quantum Risk Analysis**
- Woerner, Egger · 2019 · npj Quantum Inf. 5, 15 · DOI 10.1038/s41534-019-0130-6 · arXiv 1806.06893 · **Verified:** https://arxiv.org/abs/1806.06893
- **Claim:** "The shortest possible circuit depth ... leads to a convergence rate of O(M^−2/3) ... If we allow the circuit depth to grow faster ... the convergence rate quickly approaches the optimum of O(M^−1)."
- **LABELS:** QUERY-COMPLEXITY SPEEDUP; SIMULATOR/HARDWARE (toy).

**[B42] Option Pricing using Quantum Computers**
- Stamatopoulos, Egger, Sun, Zoufal, Iten, Shen, Woerner · 2020 · Quantum 4, 291 · arXiv 1905.02666 · **Verified:** https://arxiv.org/abs/1905.02666
- **Claim:** AE "provides a quadratic speedup compared to classical Monte Carlo". Circuits were run on IBM Q Tokyo with error mitigation.
- **LABELS:** HARDWARE DEMONSTRATION (toy), QUERY-COMPLEXITY SPEEDUP.

**[B43] A Threshold for Quantum Advantage in Derivative Pricing**
- Chakrabarti, Krishnakumar, Mazzola, Stamatopoulos, Woerner, Zeng · 2021 · Quantum 5, 463 · arXiv 2012.03819 · **Verified:** https://arxiv.org/abs/2012.03819, plus PDF
- **Claims:**
  - Abstract: "the benchmark use cases we examine require 8k logical qubits and a T-depth of 54 million. We estimate that quantum advantage would require executing this program at the order of a second."
  - Conclusion: "the quantum processor would need to execute T-gates at a rate of 10MHz ... Although current estimates target logical clock rates around 10kHz ... (i.e. orders of magnitudes slower than our requirement)".
  - "the quadratic speedup available in amplitude estimation-based algorithms could be lost in the constant factor overheads of error correction."
  - Table 1 caption: "We find that Grover-Rudolph methods are not applicable in practice".
  - A Riemann-sum loading variant needs T-depth ≈1.5×10⁸.
- **Clock-rate discrepancy:** later papers ([B44], and Dalzell [B51]) quote the Chakrabarti requirement as **~50 MHz**. The conclusion text I extracted says 10 MHz for T-gates. Both are **3–4 orders of magnitude** above the ~10 kHz projected logical rate.
- **LABELS:** NO ADVANTAGE on foreseeable hardware (resource estimate).

**[B44] Towards Quantum Advantage in Financial Market Risk using Quantum Gradient Algorithms**
- Stamatopoulos, Mazzola, Woerner, Zeng · 2022 · Quantum 6, 770 · DOI 10.22331/q-2022-07-20-770 · arXiv 2111.12509 · **Verified:** arXiv export API
- **Claim:** it "lowers the estimated logical clock rate required for financial quantum advantage from Chakrabarti et al. ... by a factor of ~7, from 50MHz to 7MHz".
- **LABELS:** resource estimate; QUERY-COMPLEXITY SPEEDUP.

**[B45] Derivative Pricing using Quantum Signal Processing**
- Stamatopoulos, Zeng · 2024 · Quantum 8, 1322 · arXiv 2307.14310 · **Verified:** https://arxiv.org/abs/2307.14310
- **Claim:** "quantum advantage will require 4.7k logical qubits, and quantum devices that can execute 10^9 T-gates at a rate of 45MHz."
- **LABELS:** resource estimate (NO ADVANTAGE on foreseeable hardware).

**[B46] Focus beyond quadratic speedups for error-corrected quantum advantage**
- Babbush, McClean, Newman, Gidney, Boixo, Neven · 2021 · PRX Quantum 2, 010103 · DOI 10.1103/PRXQuantum.2.010103 · arXiv 2011.04149 · **Verified:** https://arxiv.org/abs/2011.04149, plus full-text PDF
- **Crossover model (extracted):**
  - T_Q = M·t_Q and T_C = M^d·t_C (eq. 1).
  - Advantage requires M > (t_Q/t_C)^{1/(d−1)}.
  - Break-even time T* = t_Q·(t_Q/t_C)^{1/(d−1)} (eq. 3).
  - With classical parallel speedup S: M > (t_Q S/t_C)^{1/(d−1)} and T* = t_Q·(t_Q S/t_C)^{1/(d−1)} (eq. 5).
  - For d=2: **T* = t_Q²·S/t_C.**
- **Surface-code assumptions:**
  - Toffoli time t_G = 30 × 5.5 × 1 μs ≈ **170 μs** (eq. 6), from distance d≈30, physical error ~10⁻³, and one CCZ factory.
  - Lower-bound primitive: G = 100 Toffolis, so t_Q ≈ 17 ms (eq. 8).
  - Classical equivalent t_C ≈ 33 ns (eq. 10), under the "generous" equivalence of 1 Toffoli ≈ 1 classical clock cycle at 330 ps.
- **Table I, quadratic d=2:**

  | Case | S | M* | T* |
  |---|---|---|---|
  | Lower bound | 1 | 5.2×10⁵ | **2.4 hours** |
  | Lower bound | 10³ | 5.2×10⁸ | **100 days** |
  | Lower bound | 10⁶ | 5.2×10¹¹ | **280 years** |
  | QSA on SK model, N=512 (t_Q = 440 ms from 2.6×10³ Toffolis per update; t_C = 7 ns) | 1 | 6.3×10⁷ | **320 days** |
  | same | 10³ | — | **880 years** |
  | same | 10⁶ | — | **880 millennia** |

- **Table I, quartic d=4, SA example:** S=10⁶ gives **4.9 hours**.
- **Table II** (quadratic, S=10³, faster distillation R): the SA example needs 8.8 years (R=10), 32 days (R=10²), 7.7 hours (R=10³).
- **Key sentences:**
  - "quadratic speedups will not enable quantum advantage on early generations of such fault-tolerant devices unless there is a significant improvement in how we would realize quantum error-correction"
  - "The comparison to parallel classical resources is particularly damning for quantum computing and unfortunately, many quadratic quantum speedups (especially those leveraging amplitude amplification) apply to problems that are highly parallelizeable."
- **LABELS:** NO ADVANTAGE (for quadratic speedups on early FT hardware; a quantitative argument, not a theorem).

**[B47] Compilation of Fault-Tolerant Quantum Heuristics for Combinatorial Optimization**
- Sanders, Berry, Costa, Tessler, Wiebe, Gidney, Neven, Babbush · 2020 · PRX Quantum 1, 020312 · arXiv 2007.07391 · **Verified:** https://arxiv.org/abs/2007.07391
- **Claim (abstract):** "under quantum-favorable assumptions ... quantum accelerated simulated annealing would require roughly a day and a million physical qubits to optimize spin glasses that could be solved by classical simulated annealing in about four CPU-minutes."
- **LABELS:** NO ADVANTAGE (resource estimate).

**[B48] Applying quantum algorithms to constraint satisfaction problems**
- Campbell, Khurana, Montanaro · 2019 · Quantum 3, 167 · DOI 10.22331/q-2019-07-18-167 · arXiv 1810.05582 · **Verified:** arXiv export API
- **Claim:** potentially large Grover/backtracking speedups for SAT and colouring. However, "the quantum advantage disappears if one includes the cost of the classical processing power required to perform decoding of the surface code using current techniques."
- **LABELS:** ADVANTAGE DISPUTED (by its own caveat); resource estimate.

**[B49] Disentangling Hype from Practicality: On Realistically Achieving Quantum Advantage**
- Hoefler, Häner, Troyer · 2023 · Commun. ACM (May 2023) · arXiv 2307.00523 · **Verified:** https://arxiv.org/abs/2307.00523
- **Claim:** "small data problems and quantum algorithms with super-quadratic speedups are essential to make quantum computers useful in practice."
- **LABELS:** NO ADVANTAGE (for quadratic, big-data problems; perspective).

**[B50] Assessing requirements to scale to practical quantum advantage**
- Beverland, Murali, Troyer, Svore, Hoefler, et al. · 2022 · arXiv 2211.07629 · **Verified:** https://arxiv.org/abs/2211.07629
- **Claim:** "hundreds of thousands to millions of physical qubits are needed to achieve practical quantum advantage" for the three applications assessed.
- **LABELS:** resource-estimation framework (context).

**[B51] Quantum algorithms: A survey of applications and end-to-end complexities** (REVIEW, used for orientation)
- Dalzell, McArdle, Berta, et al. · 2023/2025 · Cambridge University Press, DOI 10.1017/9781009639651 · arXiv 2310.03011 · **Verified:** arXiv export API, plus PDF §8.2 and §15
- **§8.2 quotes:**
  - The survey says it is worth noting that "quasi-Monte Carlo methods ... can achieve a nearly quadratic speedup compared to traditional classical Monte Carlo methods, but gain an exponential dependence on the number of underlying assets".
  - "the Grover-Rudolph approach to state preparation is incompatible with a quantum speedup in the context of Monte Carlo estimation".
  - Chakrabarti et al. need a "logical clock rate of about 50 MHz ... orders of magnitude faster than what is foreseeably possible".
- **§15:** Gibbs-sampling mixing times "can be exponentially large (or worse) in the system size".

**[B52] Quantum Computing for Finance: State of the Art and Future Prospects** (REVIEW, orientation)
- Egger et al. · 2020 · IEEE TQE 1, 3101724 · DOI 10.1109/TQE.2020.3030314 · arXiv 2006.14510 · **Verified:** arXiv export API

### 2F. Quantum free-energy and polymer/protein thermodynamics proposals

**[B53] Improved precision scaling for simulating coupled quantum-classical dynamics**
- Simon, Santagati, Degroote, Moll, Streif, Wiebe · 2024 · PRX Quantum 5, 010343 · arXiv 2307.13033 · **Verified:** https://arxiv.org/abs/2307.13033
- **Claim:** a "super-polynomial improvement in the precision scaling" for Born–Oppenheimer MD via the Koopman–von Neumann/Liouville formulation, "at the price of increased space complexity". It is able to estimate "thermodynamic properties from the prepared probability density".
- **LABELS:** THEORETICAL SPEEDUP (precision of the dynamics simulation, not of the sampling), ORACLE-MODEL RESULT.

**[B54] Fullqubit alchemist: Quantum algorithm for alchemical free energy calculations**
- Huang, Boyd, Anselmetti, ..., Wiebe, Bromley, Koczor · 2025/2026 · npj Quantum Inf. (2026), DOI 10.1038/s41534-026-01275-2 · arXiv 2508.16719 · **Verified:** https://arxiv.org/abs/2508.16719, plus HTML
- **Claim (abstract):** "super-polynomial runtime scaling improvements in the precision of our Liouvillian simulation approach and quadratic improvements in the scaling with the number of particles relative to prior quantum algorithms."
- **Theorem 3 (per HTML):** Õ(N·Ñ·N_tot⁵·t_eq/(δγε)·log(1/ξ)) Toffolis. AE is used on a Hadamard-test estimator, giving O(α_Δ/ε) queries.
- **Assumptions:**
  - a ground-state-preparation oracle with overlap ≥ δ at every nuclear configuration;
  - a polynomially bounded electronic gap γ;
  - equilibration time t_eq given.
- **No concrete molecular resource counts.** The authors note that the logarithmic dependence on the number of λ windows "does not indicate an exponential speedup when compared to classical methods". The comparator is prior *quantum* algorithms, not classical TI/FEP.
- **LABELS:** THEORETICAL SPEEDUP (vs prior quantum), ORACLE-MODEL RESULT. There is **no demonstrated advantage over classical FEP**.

**[B55] Quantum-Centric Alchemical Free Energy Calculations**
- Bazayeva, Li, Kaliakin, Liang, Shajan, Das, Merz · 2025 · arXiv 2506.20825 · **Verified:** https://arxiv.org/abs/2506.20825
- **Method:** MBAR bookending from MM to QM, where the QM (CI) part is done by FCI or by SQD on quantum hardware. Tested on the hydration free energy of ammonia, methane and water.
- **LABELS:** HARDWARE DEMONSTRATION (hybrid; the quantum part is electronic structure, not sampling); NO ADVANTAGE claimed.

**[B56] Protein-Ligand Free Energy Perturbation on Quantum Hardware**
- Li, Bazayeva, Pellegrini, ..., Merz · 2026 · arXiv 2604.09857 · **Verified:** https://arxiv.org/abs/2604.09857
- **Method:** QM/MM bookending with LUCJ + SQD/extSQD on quantum processors.
- **Speed:** the paper reports that "execution time between the HCI-based FEP method and the LUCJ-SQD/extSQD-based FEP method is also comparable" (per fetched summary).
- **LABELS:** HARDWARE DEMONSTRATION; NO ADVANTAGE claimed. The Monte Carlo / sampling part remains fully classical.

**[B57] Quantum algorithms for compact polymer thermodynamics**
- Rattacaso, Jaschke, Trovato, Siloi, Montangero · 2026 · arXiv 2603.12334 · **Verified:** https://arxiv.org/abs/2603.12334, plus HTML
- **Claim (abstract):** "we enable a quadratic speedup in the estimation of thermodynamic properties of maximally compact polymers and heteropolymers by quantum computation", motivated by "modeling protein and RNA folding".
- **Per HTML:**
  - ground-state-preparation cost is **not quantified** ("a comprehensive understanding of the complexity of ground-state preparation will be essential");
  - the classical MPS construction works on 6×n strips (χ ≤ 384) but degrades on square lattices (3.5% counting error at 10×10);
  - direct classical sampling from the MPS is not discussed.
- **Critical note (I(prog)):** where their MPS converges, it already yields Z and expectations by **classical tensor contraction**. The quadratic claim is relative to plain MC, not to the classical tensor-network route the paper itself uses.
- **LABELS:** QUERY-COMPLEXITY SPEEDUP (vs naive MC); ADVANTAGE DISPUTED (a stronger classical baseline exists in the paper itself).

**[B58] Toward end-to-end quantum simulation for protein dynamics**
- Liu, Li, Wang, Liu · 2024/2025 · arXiv 2411.03972 · **Verified:** https://arxiv.org/abs/2411.03972
- **Method:** quantum algorithms for normal-mode (Gaussian-network / all-atom NMA) dynamics, plus observable read-out (energy, density of states, correlations).
- **Classical validation:** only "classical numerical experiments ... serve to validate our claims regarding potential quantum speedups."
- **Limitation (I(prog)):** these are harmonic models, whose observables are classically computable by diagonalisation of an N×N matrix.
- **LABELS:** THEORETICAL SPEEDUP (claimed), ORACLE-MODEL RESULT; relevance to structure prediction is low.

### 2G. Classical competitors and protein-practice evidence

**[B59] Adaptive Simulated Annealing: A Near-optimal Connection between Sampling and Counting**
- Štefankovič, Vempala, Vigoda · 2006 preprint (J. ACM 56(3) 2009 per the citation in [B27]; the JACM page itself was not fetched) · arXiv cs/0612058 · **Verified:** https://arxiv.org/abs/cs/0612058
- **Claim:** "a cooling schedule of length ℓ=O*(√ln A) ... an overall savings of O*(n) in the running time".
- **Role:** the classical benchmark every quantum partition-function algorithm quantizes.
- **LABELS:** classical baseline.

**[B60] Statistically optimal analysis of samples from multiple equilibrium states (MBAR)**
- Shirts, Chodera · 2008 · J. Chem. Phys. 129, 124105 · DOI 10.1063/1.2978177 · arXiv 0801.1426 · **Verified:** https://arxiv.org/abs/0801.1426
- **Claim:** "In the large sample limit, MBAR is unbiased and has the lowest variance of any known estimator for making use of equilibrium data collected from multiple states."

**[B61] Efficient estimation of free energy differences from Monte Carlo data (BAR)**
- Bennett · 1976 · J. Comput. Phys. 22, 245–268 · DOI 10.1016/0021-9991(76)90078-4 · **Verified:** Crossref API

**[B62] Statistical Mechanics of Fluid Mixtures (thermodynamic integration)**
- Kirkwood · 1935 · J. Chem. Phys. 3, 300–313 · DOI 10.1063/1.1749657 · **Verified:** Crossref API

**[B63] A nonequilibrium equality for free energy differences**
- Jarzynski · 1997 · PRL 78, 2690 · DOI 10.1103/PhysRevLett.78.2690 · arXiv cond-mat/9610209 · **Verified:** https://arxiv.org/abs/cond-mat/9610209

**[B64] Annealed Importance Sampling**
- Neal · 2001 · Statistics and Computing 11, 125–139 · DOI 10.1023/A:1008923215028 · arXiv physics/9803008 · **Verified:** https://arxiv.org/abs/physics/9803008 and Springer link (search)
- **Claim:** AIS "is most attractive when isolated modes are present, or when estimates of normalizing constants are required ... its independent sampling allows one to bypass some of the problems of assessing convergence and autocorrelation".

**[B65] Sequential Monte Carlo samplers**
- Del Moral, Doucet, Jasra · 2006 · JRSS B 68(3), 411–436 · DOI 10.1111/j.1467-9868.2006.00553.x · **Verified:** WebSearch (Wiley/OUP publisher pages listed)

**[B66] An efficient, multiple range random walk algorithm to calculate the density of states (Wang–Landau)**
- Wang, Landau · 2001 · PRL 86, 2050 · DOI 10.1103/PhysRevLett.86.2050 · arXiv cond-mat/0011174 · **Verified:** https://arxiv.org/abs/cond-mat/0011174
- **Claim:** "permits us to directly access the free energy and entropy, is independent of temperature ... useful for the study of complex systems with a rough energy landscape."

**[B67] Nested sampling for general Bayesian computation**
- Skilling · 2006 · Bayesian Analysis 1(4), 833–859 · DOI 10.1214/06-BA127 · **Verified:** WebSearch (projecteuclid.org page listed)

**[B68] High-dimensional integration: the quasi-Monte Carlo way**
- Dick, Kuo, Sloan · 2013 · Acta Numerica 22, 133–288 · DOI 10.1017/S0962492913000044 · **Verified:** WebSearch (Cambridge Core page listed)
- **Role:** QMC reaches ~O(N^{-1+δ}) error for integrands in suitably weighted spaces. That is the same rate as QAE, for smooth / low-effective-dimension problems.

**[B69] Best Practices for Quantification of Uncertainty and Sampling Quality in Molecular Simulations**
- Grossfield, Patrone, Roe, Schultz, Siderius, Zuckerman · 2018 · LiveCoMS 1, 5067 · DOI 10.33011/livecoms.1.1.5067 · PMID 30533602 · **Verified:** Europe PMC API

**[B70] Equilibrium Sampling in Biomolecular Simulation**
- Zuckerman · 2010 preprint (submitted to Annu. Rev. Biophys.) · arXiv 1009.2958 · **Verified:** https://arxiv.org/abs/1009.2958
- **Claim:** "Equilibrium sampling of biomolecules remains an unmet challenge after more than 30 years of atomistic simulation ... progress resulting from novel hardware use appears to be more clear-cut than from algorithms alone".

**[B71] Predicting Binding Free Energies: Frontiers and Benchmarks**
- Mobley, Gilson · 2017 · Annu. Rev. Biophys. 46, 531–558 · DOI 10.1146/annurev-biophys-070816-033654 · PMID 28399632 · **Verified:** Europe PMC API; quotes from the bioRxiv preprint 10.1101/074625v2 PDF
- **Preprint quotes:**
  - "free energy calculations appear to be capable of achieving RMS errors in the 1-2 kcal/mol range with current force fields";
  - "calculations with a 2 kcal/mol RMS error will suffice [for a three-fold reduction in compounds synthesized]";
  - "The problem of finite sampling is most acute for systems where low-energy (hence highly occupied) conformational states are separated by high effective barriers";
  - "Sampling problems are also common, with slow sidechain rearrangements and ligand binding mode rearrangements ... posing timescale problems";
  - reference benchmarks use "high precision free energies (e.g., uncertainty ≲0.1 kcal/mol)".

**[B72] Alchemical free energy methods for drug discovery: progress and challenges**
- Chodera, Mobley, Shirts, Dixon, Branson, Pande · 2011 · Curr. Opin. Struct. Biol. 21, 150–160 · DOI 10.1016/j.sbi.2011.01.011 · PMID 21349700 · **Verified:** Europe PMC API
- **Claim:** the methods "still fall short of providing robust tools for pharmaceutical engineering."

**[B73] Accurate and reliable prediction of relative ligand binding potency ... (FEP+)**
- Wang, Wu, Deng, et al. · 2015 · JACS 137, 2695–2703 · DOI 10.1021/ja512751q · PMID 25625324 · **Verified:** Europe PMC API
- **Claim (abstract):** the accuracy "needed to guide lead optimization (∼5× in binding affinity)"; "unprecedented level of accuracy across ... 200 ligands".

**[B74] How fast-folding proteins fold**
- Lindorff-Larsen, Piana, Dror, Shaw · 2011 · Science 334 · DOI 10.1126/science.1208351 · PMID 22034434 · **Verified:** Europe PMC API
- **Claim:** "atomic-level molecular dynamics simulations, over periods ranging between 100 μs and 1 ms ... 12 structurally diverse proteins ... spontaneously and repeatedly fold".
- **Role:** equilibrium ensemble estimates for proteins are **time-scale (mixing) limited**. They needed special-purpose hardware, not more i.i.d. samples.

**[B75] BBK* (Branch and Bound over K*)**
- Ojewole, Jou, Fowler, Donald · 2018 · J. Comput. Biol. 25(7), 726–739 · DOI 10.1089/cmb.2017.0267 · **Verified:** Crossref API
- **Role:** provable ε-approximation of **protein conformational partition functions** over rotamer ensembles. It uses deterministic enumeration plus bounds, not MCMC.
- **Note:** the K* ε-approximation description comes from WebSearch snippets of the OSPREY/BBK* literature; the abstract text was not available via Crossref.

**[B76] Guaranteed Weighted Counting for Affinity Computation: Beyond Determinism and Structure**
- Viricel, Simoncini, Barbe, Schiex · 2016 · CP 2016, LNCS, 733–750 · DOI 10.1007/978-3-319-44953-1_46 · **Verified:** Crossref API
- **Role:** protein-design partition functions (binding affinity) treated as guaranteed weighted model counting on cost-function networks. This is a strong exact/bounded classical competitor for discrete conformational Z.

**Count: 76 verified entries** (2 flagged as reviews for orientation: B51, B52).

---

## 3. Primitive analyses (16 questions each)

### P1. Amplitude estimation / quantum mean estimation for ensemble expectations (QA-1)

1. **Operation.** Given a unitary A that prepares Σ_x √p(x)|x⟩|f(x)⟩ (a *qsample* of the ensemble, with the observable encoded in an ancilla amplitude), estimate E_p[f] to ±ε using O(σ/ε) calls to A and A⁻¹ [B1, B12, B19].
2. **Classical computation replaced.** Monte Carlo averaging of f over M ≈ σ²/ε² independent samples. For MCMC this becomes M ≈ 2τ_int·σ²/ε² correlated steps.
3. **Why hard classically.** Only when σ²/ε² is huge (very high precision) *and* each sample is expensive. Otherwise it is cheap and embarrassingly parallel [B46].
4. **Exact speedup.** Õ(σ/ε) vs Θ(σ²/ε²) queries. It is tight in both directions: quantum Ω(1/ε) [B16, B13, B29] and classical Ω(σ²/ε²) black-box [B12].
5. **Kind.** Query/sample complexity. It is **not** runtime.
6. **Assumptions.** A is a coherent unitary without measurement. Its variance or relative variance bound is known. There is no decoherence over O(σ/ε) sequential Grover iterations (depth ∝ 1/ε).
7. **Oracle needed.** (i) a state-preparation unitary for the ensemble p(x) (the qsample); (ii) coherent reversible evaluation of f(x) and its encoding into an amplitude (arithmetic plus controlled rotation).
8. **Oracle construction cost.**
   - For a protein ensemble, (ii) means coherent fixed-point evaluation of structural observables (distances, RMSDs, contact indicators) and possibly energies. That is 10³–10⁶ Toffolis per call, based on finance payoff circuits of T-depth 3–9×10³ ([B43] App.) and SK updates of 2.6×10³ Toffolis at N=512 [B46].
   - Herbert [B38] and Stamatopoulos–Zeng [B45] reduce the arithmetic but do not remove it.
9. **State-prep cost.** This is **dominant and usually disqualifying**.
   - A Boltzmann/posterior ensemble over conformations has no closed-form integrable marginals, so Grover–Rudolph does not apply. Even where it applies, it destroys the speedup [B37].
   - qGAN loading [B40] adds approximation bias.
   - The only principled route is quantum-walk qsampling [B23, B24, B26–B28]. Its cost is Õ(√τ)-type walk steps per reflection *given* a slowly varying annealing sequence. Qsampling a generic stationary distribution efficiently is not known and is linked to SZK-type hardness [B31, B12].
10. **Readout cost.** Phase estimation or QPE-free schedules [B4–B9]. O(log 1/δ_fail) repetitions. Negligible relative to the oracle.
11. **Classical postprocessing.** MLE / interval bookkeeping. Trivial.
12. **Strongest classical algorithm.** Depends on the problem:
    - smooth, low-effective-dimension integrands: QMC, with O(N^{-1+δ}) error [B68, B51];
    - multi-level structure: MLMC [B20];
    - equilibrium ensembles: MBAR [B60] with control variates / reweighting, run on massively parallel hardware.
13. **Does the advantage survive?**
    - Against QMC on smooth problems: largely no (the same rate) [B51, B15].
    - Against massively parallel MC: only after crossover times of days to centuries on the Babbush model [B46]; see §5.
14. **Fault tolerance needed?** Yes. Heisenberg-limited AE requires depth ∝ 1/ε over an expensive oracle. NISQ variants saturate at the noise floor [B11, B10, B6].
15. **Resource numbers from the literature (calibration).**
    - Derivative pricing (a far simpler oracle than a protein ensemble): 8k logical qubits, T-depth 5.4×10⁷, advantage only if run in ~1 s. That requires a T-rate of 10–50 MHz vs ~10 kHz projected [B43, B44].
    - QSP version: 4.7k logical qubits, 10⁹ T at 45 MHz [B45].
    - No protein-ensemble AE resource estimate exists in the literature (§8).
16. **Protein mapping.** Candidates:
    - (a) posterior-mean structures and basin populations under a learned energy (C-3, SP-1);
    - (b) ΔG between basins or alchemical states;
    - (c) uncertainty/confidence estimates.
    
    In all three, precision needs are coarse. Examples: ~0.1 kcal/mol is already the "high precision" reference in [B71], against a 1–2 kcal/mol force-field error; in this program the chain MDE is ~0.1–0.25 Å. The **mixing** time τ dominates cost, not σ²/ε² [B71, B74, B70]. **The mapping is formally natural but aims at the wrong factor.**

### P2. Quantum partition-function estimation (annealing + quantum walks + mean estimation)

1. **Operation.** Estimate Z(β) of a classical Gibbs distribution to relative error ε. It uses a cooling schedule β₀ < … < β_ℓ, qsamples prepared or reflected via Szegedy walks of Markov chains with gap δ, and quantum mean estimation of the telescoping ratios [B24, B12, B26–B28].
2. **Classical computation replaced.** The SVV/TPA-style annealed product (paired-product) estimator using MCMC samples [B59, B27]. Related methods: AIS [B64], SMC [B65], thermodynamic integration [B62], Wang–Landau [B66], nested sampling [B67].
3. **Why hard classically.** Z is #P-hard to compute exactly in general ([B28] intro). The approximation cost scales as log|Ω|/(ε²δ). It is bottlenecked by the spectral gap δ at low temperature and by ε.
4. **Exact speedup (walk steps).**
   - Classical Õ(log|Ω|/(ε²δ)) [SVV, per B28 Table 1].
   - Quantum Õ(log|Ω|/(ε√δ)) [B26, B27] → Õ(log^{3/4}|Ω|·polylog(n)/(ε√δ)) [B28].
   - Montanaro Õ((log|Ω|)√τ(√τ + 1/ε)) including the schedule [B12].
   - Ising/colourings: Õ(n²/ε²) classical → Õ(n^{3/2}/ε) [B27, B26] → Õ(n^{1.25}/ε) [B28].
   - Lower bound: Ω(1/ε) reflections [B29].
5. **Kind.** Walk-step/query complexity (an ORACLE-MODEL result), with explicit dependence on δ, ε and log|Ω|.
6. **Assumptions.**
   - reversible ergodic chains with known gap lower bound δ at every β;
   - Hamiltonian range in {0,…,n} (integer, nonnegative) [B27];
   - direct sampling at β₀;
   - coherent implementation of the chain's transition (Szegedy walk);
   - non-destructive AE for recycling qsamples [B26, B28].
7. **Oracle.** The quantum walk operator W(P_β), which needs coherent computation of the proposal and acceptance probability, i.e. of energy differences [B32, B33].
8. **Oracle construction cost.** Per walk step: coherent ΔE plus the Metropolis acceptance.
   - SK N=512: 2.6×10³ Toffolis per step, i.e. t_Q = 440 ms at 170 μs per Toffoli [B46, B47].
   - For an off-lattice protein energy (pair distances with square roots and smooth tabulated potentials), I(prog) estimates **≥10⁴–10⁶ Toffolis per step**: roughly 10²–10³ pair terms per local move × 10²–10³ Toffolis per fixed-point distance/potential evaluation. This is an estimate, not a literature number.
9. **State-prep cost.** An initial qsample at β₀ (uniform, cheap) plus annealed transport: Õ(√τ) walk steps per stage [B23, B12]. The known-gap requirement is essential.
10. **Readout.** AE on each ratio. O(ℓ) stages.
11. **Classical postprocessing.** Product of ratios. Schedule construction (classical in Montanaro; quantum binary search in [B26, B27]).
12. **Strongest classical algorithm.**
    - General: SVV/TPA/paired-product at Õ(log|Ω|/(ε²δ)) [B27, B59].
    - In molecular practice: MBAR over replica-exchange / expanded-ensemble samples [B60], AIS/SMC [B64, B65], Wang–Landau [B66].
    - For discrete rotamer spaces: exact/bounded weighted counting (K*/BBK* [B75]; CFN counting [B76]). These are deterministic and bound-driven, so the quantum algorithms' premise (MCMC with gap δ) does not describe them.
13. **Does the advantage survive?** Only in walk-step count and only if δ is small. In wall-clock the per-step overhead ratio t_Q/t_C ~ 10⁵–10⁸ (see §5) must be overcome by (1/ε)·(1/√δ)·log^{1/4}|Ω|. For protein-relevant ε (10⁻¹–10⁻²) this requires δ ≲ 10⁻⁶–10⁻¹⁰ *and* runtimes of years (§5). No measurement of δ exists for the program's posteriors (OP-01).
14. **Fault tolerance?** Yes. Walk depths ∝ √τ/ε.
15. **Resource numbers.**
    - The closest compiled analogue is quantum-walk simulated annealing on SK spin glasses [B47, B46]: about a day and ~10⁶ physical qubits to match ~4 CPU-minutes of classical SA; break-even of 320 days (1 core) to 880 years (10³ cores).
    - A 2026 preprint reports "~10³ years for conventional quantum walks" on dense Ising [B34].
16. **Protein mapping.** Z of a discrete conformational model:
    - lattice/HP or compact polymers [B57];
    - rotamer ensembles for design / binding (K*) [B75, B76];
    - a discretised posterior over CA traces (SP-4).
    
    For K*, classical bounded enumeration is the incumbent and gives provable ε. For posteriors, whether δ is small is **unknown**.

### P3. Quantum free-energy algorithms via Liouvillian / KvN dynamics (Simon et al.; Fullqubit alchemist)

1. **Operation.** Coherently simulate Born–Oppenheimer classical-nuclear dynamics (KvN), with electronic forces computed by phase kickback from ground-state electronic simulation. Equilibrate to an NVT density |ρ_Λ⟩. Estimate ΔF with a Hadamard test plus AE [B53, B54].
2. **Classical computation replaced.** Alchemical FEP/TI with ab initio (or QM/MM) forces, where each MD step needs an electronic-structure calculation.
3. **Why hard classically.** The *electronic structure* (correlated QM forces), not the Monte Carlo variance.
4. **Speedup.**
   - Super-polynomial in the *precision of the dynamics simulation*, and quadratic in particle number, both relative to **prior quantum** algorithms [B54].
   - AE yields O(1/ε) in the estimator.
   - No comparison to classical FEP runtime.
5. **Kind.** Gate complexity (Toffolis) under oracles.
6. **Assumptions.**
   - a ground-state overlap oracle ≥ δ for all nuclear configurations;
   - a polynomial electronic gap γ;
   - equilibration time t_eq given;
   - high phase-space overlap between the end states [B54].
7. **Oracle.** Ground-state preparation U_I plus the block-encoded electronic Hamiltonian.
8. **Oracle cost.** Õ(N·Ñ·N_tot⁵·t_eq/(δγε)) Toffolis in total [B54]. For a protein-ligand system, N_tot⁵ with N_tot ~ 10⁴ particles is ~10²⁰ (I(prog) arithmetic): prohibitive.
9. **State prep.** The initial nuclear density plus the electronic ground state (assumed).
10. **Readout.** Hadamard test plus AE.
11. **Classical postprocessing.** Minimal.
12. **Strongest classical.** FEP+/MBAR with MM force fields [B73, B60] (RMS 1–2 kcal/mol [B71]); QM/MM bookending [B55, B56]; ML potentials.
13. **Does the advantage survive?** Not demonstrated. The classical comparator is not analysed.
14. **FT?** Yes, deep FT.
15. **Resources.** No concrete counts in [B54].
16. **Protein mapping.** Binding free energies, not structure prediction. It addresses *force-field accuracy* (bias), which is the real bottleneck per [B71]. Its speed claims are not about MC variance. **Outside the S29–S33 structure-accuracy scope** (cf. AA-3).

### P4. NISQ / low-depth / variational AE

1. **Operation.** AE with bounded-depth Grover powers and classical MLE/Bayesian post-processing [B4–B8], or variationally compressed Grover powers [B7].
2. **Replaces.** Classical MC averaging.
3. **Hard classically?** Same as P1.
4. **Speedup.** N = Õ(1/ε^{1+β}) with depth D = O(1/ε^{1−β}) [B6]. The speedup factor is ≈ D. VQAE is "typically ... larger computational requirements than classical MC" [B7].
5. **Kind.** Query.
6. **Assumptions.** The noise model is known (depolarizing) [B11, B10].
7–9. **Oracle, cost, state prep.** As P1. A protein-observable oracle (10⁴–10⁶ Toffolis, i.e. ~10⁵–10⁷ two-qubit gates after decomposition) exceeds NISQ depth budgets *for a single application of A*, before any Grover power.
10–11. **Readout, postprocessing.** Many shots; MLE.
12. **Strongest classical.** MC/QMC on a laptop.
13. **Survives?** No. Hardware error "saturates due to the noise" [B11].
14. **FT?** The FT-free promise fails for nontrivial oracles.
15. **Resources.** Hardware demonstrations use 1–few-qubit toy oracles [B11, B42].
16. **Protein mapping.** None viable.

### P5. State preparation / loading (Grover–Rudolph, qGAN, arithmetic-free encodings)

1. **Operation.** Build A with A|0⟩ = Σ√p(x)|x⟩.
2. **Replaces.** Classical sampling from p.
3. **Hard classically?** For Boltzmann ensembles, classical sampling *is* the hard part (mixing). Loading does not remove that difficulty; it relocates it.
4. **Speedup.** None with Grover–Rudolph for QMC [B37]. For general states: O(2ⁿ) exact [B40, B39].
5–9. Loading requires integrable marginals (log-concave, analytic) [B36]. A conformational Boltzmann distribution has none. qGAN loading introduces training cost and bias [B40].
10–11. N/A.
12. **Strongest classical.** Direct sampling / MCMC.
13. **Survives?** No for Grover–Rudolph (theorem). Unclear, but not favourable, for learned loaders.
14. **FT?** Yes, for exact arithmetic loaders.
15. **Resources.** Chakrabarti et al.: Grover–Rudolph "not applicable in practice"; Riemann-sum loading needs T-depth 1.5×10⁸ [B43].
16. **Protein mapping.** Only via quantum-walk qsampling (P2). That makes P1 for proteins **equivalent to P2's walk problem**, and P2 is gated by δ.

---

## 4. Strongest classical counterarguments

1. **Quadratic speedups do not survive FT overheads at relevant scales** [B46, B47, B43, B45, B49, B51].
   - The Babbush break-even T* = t_Q²·S/t_C (d = 2) is 2.4 h even for a 100-Toffoli primitive on 1 core. It becomes 100 days on 10³ cores and 280 years on 10⁶ cores.
   - For a compiled QSA step (2.6×10³ Toffolis): 320 days (1 core) → 880 years (10³ cores).
   - Finance QAE needs a 10–50 MHz logical T-rate against ~10 kHz projected [B43, B44, B51].
   - Because T* ∝ t_Q², heavier protein oracles make it **quadratically worse**.
2. **Monte Carlo averaging is embarrassingly parallel.** The S factor in Babbush eq. (5) is realistically 10³–10⁶ for ensemble averaging. Replica exchange, many independent chains, GPUs and Anton-class hardware all apply [B46, B70, B74].
3. **The variance term is not the bottleneck in biomolecular estimation.**
   - Errors are dominated by force-field bias ("RMS errors in the 1-2 kcal/mol range with current force fields") and by barrier-limited sampling ("most acute for systems where low-energy ... states are separated by high effective barriers") [B71].
   - Statistical precision of ≲0.1 kcal/mol is already routine for converged systems [B71].
   - QAE reduces only the σ²/ε² factor. It does nothing for bias and nothing for τ.
4. **Classical variance reduction already captures much of a "quadratic" gain in structured cases.**
   - QMC gives a near-quadratic improvement for smooth, low-effective-dimension integrands [B68, B51].
   - MBAR is minimum-variance among equilibrium estimators [B60].
   - AIS/SMC/nested sampling/Wang–Landau handle normalising constants with multimodality [B64–B67].
   - MLMC is also quantizable, but again only quadratically [B20].
5. **Lower bounds cap quantum gains at quadratic in ε** [B16, B13, B29, B19]. Any protein claim based on AE is at best quadratic in precision.
6. **State preparation erases the speedup** in the analytic-distribution case (theorem [B37]). For Boltzmann ensembles, qsampling reduces to a quantum walk whose efficiency is unknown in general [B12, B31], and whose gain over classical is ≤ quadratic in δ.
7. **Classical baselines keep improving.**
   - AHNTW's own classical improvement to SVV [B27].
   - Deterministic or bounded counting for protein-design partition functions [B75, B76].
   - Tensor-network contraction in the compact-polymer case, where the classical route is already in the quantum paper [B57].

---

## 5. Scaling statements (explicit, from the literature) and a calibrated crossover for protein-like primitives

**Literature asymptotics (no inference from small numerics):**
- **Mean estimation:** classical Θ(σ²/ε²) vs quantum Θ̃(σ/ε) [B12, B19, B16].
- **Partition function, walk steps:**
  - classical Õ(log|Ω|/(ε²δ)) [SVV via B28];
  - quantum Õ(log|Ω|/(ε√δ)) [B26, B27] and Õ(log^{3/4}|Ω|/(ε√δ)) [B28];
  - lower bound Ω(1/ε) reflections [B29].
- **In system size n** (bounded-degree Ising, rapid mixing): classical Õ(n²/ε²); quantum Õ(n^{3/2}/ε) [B12, B26, B27] and Õ(n^{1.25}/ε) [B28].
- **For a protein discretised with k states per residue over L residues:** log|Ω| = L·ln k. The asymptotic step-count ratio is then (classical/quantum) ≈ (1/ε)·(1/√δ)·(L ln k)^{1/4}. The δ(L) of the program's learned-energy posteriors is **unmeasured**.
- **Integration smoothness:** the quantum advantage over randomized classical integration is ~quadratic only "if the smoothness is small" [B15]. It shrinks for smooth integrands [B14, B15].

**Calibrated crossover (I(prog) arithmetic on the literature's cost model, Babbush et al. [B46] eqs. 3, 5–6).**

Let G be the number of Toffolis per quantum primitive call (one walk step or one oracle application). Babbush's quantum-generous equivalence is t_Q = G·170 μs and t_C = G·0.33 ns, which gives T* = 88 s·G·S.

| Primitive (G) | Example | T* (1 core) | T* (S = 10³ cores) |
|---|---|---|---|
| 10² | Babbush lower bound | 2.4 h | 100 days |
| 10³ | ≈ an SK spin update | 1 day | 2.8 years |
| 10⁴ | coarse CA-trace local move with a learned pair potential, ~10² pair terms | 10 days | 28 years |
| 10⁵ | same with fixed-point sqrt/tabulated potentials | 100 days | 280 years |
| 10⁶ | all-atom-like local energy update | 2.8 years | 2,800 years |

With realistic arithmetic overhead the picture is worse. One Toffoli ≠ one CPU cycle; the SK example has t_Q/t_C = 6.3×10⁷ [B46]. For example, a coarse-grained step at t_C ≈ 1 μs vs G = 10⁵ Toffolis (t_Q = 17 s) gives:
- T* = t_Q²/t_C ≈ 2.9×10⁸ s ≈ **9 years on 1 core, ~9,000 years on 10³ cores**;
- the break-even requires the classical computation to need M*² ≈ (1.7×10⁷)² ≈ 3×10¹⁴ primitive calls.

Faster distillation (Babbush's R) divides T* by R²:
- R = 10² ("essentially as cheap as Clifford gates") gives ~8 h (1 core) / ~0.9 yr (10³ cores);
- Babbush judges even this "challenging".

**What precision would this require for a protein ensemble estimate?** The quantum run must perform M* ≈ t_Q·S/t_C primitive calls, and the problem must need M*² classical calls. For AE on an MCMC qsample, the quantum call count is ~√τ·σ/ε.

Take the 1-core, G = 10⁵, realistic case (M* ≈ 1.7×10⁷):
- with τ = 10⁶ steps, it requires σ/ε ≳ 1.7×10⁴;
- that means estimating an ensemble average to ~6×10⁻⁵ of its standard deviation.

Protein decisions need σ/ε ~ 10–10², for example:
- ΔG to ~0.1–0.5 kcal/mol when fluctuations are a few kcal/mol [B71];
- basin populations to a few percent;
- structural averages to ~0.1 Å against a MDE of 0.1–0.25 Å.

At σ/ε ~ 10–10², the quadratic 1/ε factor contributes at most 10–10². **Conclusion (I(prog)):** a quadratic *precision* speedup cannot reach break-even for any protein-structure estimate at the precisions that matter. Only the √δ (mixing) factor could, and only if δ is extraordinarily small. That is a Domain-A/AA-1 question gated by OP-01.

---

## 6. NISQ route vs fault-tolerant route

- **NISQ.** QPE-free AE (MLAE, IQAE, FAE, power-law/QoPrime, VQAE [B4–B8]) reduces depth. With depth D the gain is ≤ ~D-fold [B6], and hardware error "saturates due to the noise" [B11].
  - VQAE "typically has larger computational requirements than classical MC" [B7].
  - A single coherent evaluation of any protein observable or energy exceeds NISQ depth budgets.
  - Hybrid "quantum-centric" free-energy work [B55, B56] uses the QPU only for small active-space electronic structure (SQD). It claims no speedup, and runtime parity with classical HCI at best.
  - **Verdict: NISQ route KILLED for estimation.**
- **Fault-tolerant.** The quadratic AE / quantum-walk algorithms are well defined [B12, B24–B28]. The end-to-end costs from every published compilation are unfavourable for quadratic speedups:
  - finance QAE: 10–50 MHz logical rate needed [B43–B45];
  - QSA: 320 days to 880 millennia break-even [B46, B47];
  - conventional walks: "~10³ years" [B34].
  
  The only FT scenario that escapes is a **super-quadratic** gain, for example a combined 1/ε × 1/√δ gain with extremely small δ, or claimed fully-quantum walks [B34, unreplicated]. **Verdict: FT route WEAK, conditional on a measured tiny δ(L).**

---

## 7. Protein mapping and the connection to the S29–S33 evidence

**Where Monte Carlo estimation appears in protein-structure computation:**

| Estimate | What limits it in the literature | Would quadratic precision matter? |
|---|---|---|
| (a) Ensemble expectations under a structural posterior or force field (mean structure, basin populations, contact probabilities) | Mixing / barriers [B71, B74, B70]; model bias [B71] | No: σ²/ε² is modest |
| (b) Free-energy differences (folding ΔG, binding ΔG, alchemical) | Force-field bias of 1–2 kcal/mol RMS, and barrier-limited sampling; statistical precision ≲0.1 kcal/mol is already attainable [B71, B73, B72] | No |
| (c) Partition functions of discrete conformational models (rotamer design, K*/BBK* ε-approx [B75]; CFN weighted counting [B76]; lattice/compact polymers [B57]) | Deterministic bounded enumeration; tensor networks | Conceivably a gap-limited MCMC case exists, but the incumbents are not MCMC and the quantum algorithms' δ-premise is unverified |
| (d) Uncertainty quantification (bootstrap / block averaging [B69]) | Cheap and parallel | No |

**Connection to S29–S33 (from the program files read):**
- **Not tested.** AE, quantum counting and quantum partition-function algorithms were never run in S29–S33. All 33 CVaR-VQE experiments used diagonal costs with argmin, energy-ordered-tail or convex readouts. H-001 says these are classically reproducible, and they involve **no Monte Carlo variance at all**.
- **The one suggestive signal is not a variance signal.** The Boltzmann-weighted structural average (mid30, 1.40× MDE, `s33` Q-C18) is a weighting over an **explicit, enumerated candidate pool**. Its expectation is computed exactly by a classical weighted sum, so there is no sampling error for QAE to reduce.
- **Where sampling was measured, classical was near-exact.** At 18 qubits Metropolis came closer to the exact Gibbs mean than the Born machine on 9/10 targets (`s33` Q-C19). At that size exact enumeration is available anyway.
- **Consequence for the Opportunity Map.** QA-1 ("Conditional, low prior") should be downgraded unless the C-3 variance audit finds a decision that flips with sample count *at a precision where σ²/ε² ≫ τ_int*. Any residual quantum interest in ensemble estimation belongs to AA-1 (walk-based mixing, √δ). Here the amplitude-estimation layer adds at most a factor σ/ε ~ 10–10².
- **What would have to be different for P1/P2 to become load-bearing.** Three things together:
  - (i) an endpoint-relevant expectation whose required precision ε is tiny relative to σ;
  - (ii) no classical estimator (MBAR/QMC/control variates) closing it;
  - (iii) a measured δ(L) small enough that (1/ε)(1/√δ)(log|Ω|)^{1/4} exceeds the per-step overhead ratio t_Q/t_C ≈ 10⁵–10⁸ **and** a parallel factor S.
  
  None of these is supported by the evidence.

---

## 8. Literature gaps (novelty ≠ advantage)

1. **No end-to-end resource estimate exists for QAE or quantum partition-function estimation on any protein conformational model.** This covers Toffoli counts for coherent protein-energy walk steps and for structural-observable oracles. The finance and SK compilations are the only calibration points. Writing one would be novel, but the expected answer is negative (§5).
2. **No measured spectral gaps or mixing times δ(L)** for learned-energy structural posteriors, or for discretised CA-trace spaces, as a function of length. Every quantum partition-function speedup is stated in δ. This is the program's OP-01 / C-1, and it is the decisive input.
3. **No quantum-vs-classical comparison uses realistic classical estimators** (MBAR, QMC, control variates, SMC/AIS with adaptive schedules) for biomolecular free energies. Quantum free-energy papers compare against prior quantum algorithms [B54] or naive MC [B57].
4. **Qsampling of continuous, multimodal molecular densities.** No efficient-loading result exists beyond log-concave or learned approximations [B36, B37, B40]. The error-propagation analysis of approximate qsamples into AE bias for such densities is missing.
5. **Protein partition functions via bounded enumeration (K*) vs quantum counting.** No paper compares Grover-type counting / AE with A*-based ε-approximation on rotamer spaces. Classical bounds exploit structure (DEE pruning), which black-box quantum counting ignores.
6. **Compact-polymer quantum thermodynamics [B57]** leaves the ground-state-preparation cost unquantified, and does not compare against its own classical MPS contraction or perfect sampling.

Novelty of any of the above would not by itself indicate advantage.

---

## 9. Unverified leads (not cited as evidence)

- Zwanzig 1954, free-energy perturbation (J. Chem. Phys.): the Crossref lookup returned HTTP 429.
- Sly & Sun 2012, hardness of approximate counting in two-spin models beyond uniqueness: not fetched.
- Huber 2015 (paired-product estimator / TPA) and Kolmogorov 2018: cited inside [B27]; not independently fetched.
- Temme et al. 2011, "Quantum Metropolis sampling" (Nature): cited in [B51]; not fetched.
- Richter 2007, "Quantum speedup of classical mixing processes" (PRA): cited in [B12]; not fetched.
- Lilien et al. 2005 (K* original) and Georgiev, Lilien & Donald 2008 (minDEE / partition functions): not fetched.
- Kothari–O'Donnell venue (SODA 2023?), Nayak–Wu venue (STOC 1999?), Heinrich J. Complexity 2002 publication details: venues not verified.
- The Štefankovič–Vempala–Vigoda JACM version: only the citation within [B27] was seen.
- Giles 2008, multilevel Monte Carlo (Oper. Res.): not fetched.
- Sugita & Okamoto 1999, replica exchange MD: not fetched (likely Domain A).
- Chakrabarti, Childs, Hung, Li, Wang, Wu 2019, quantum convex-body volume estimation: cited in [B28]; not fetched.

---

## 10. Bottom-line verdicts per primitive

**P1. Amplitude estimation / quantum mean estimation for protein ensemble expectations: KILLED (practical), WEAK (theoretical).**
- The speedup is a tight quadratic in precision [B12, B16, B19]. It reduces only the σ²/ε² factor, which is not the binding cost in any protein-structure or biomolecular free-energy setting found. The literature points to mixing/barriers and force-field bias [B71, B74, B70].
- The state-preparation step needed for a Boltzmann ensemble either destroys the speedup (Grover–Rudolph, theorem [B37]) or turns into a quantum-walk qsampling problem (P2).
- Calibrated on the published FT cost model [B46], break-even needs σ/ε ~ 10⁴ or more with months-to-millennia runtimes. Protein decisions need σ/ε ~ 10–10².
- In the program's own evidence, the only ensemble signal is an exact weighted sum over an enumerated pool, with no variance to reduce.
- Recommend closing QA-1 unless the C-3 variance audit unexpectedly finds a high-precision, variance-dominated decision.

**P2. Quantum partition-function / annealing algorithms (WCNA09 → Montanaro → Harrow–Wei → AHNTW → Cornelissen–Hamoudi): WEAK (conditional).**
- The theory is solid: rigorous quadratic gains in both ε and δ, plus a log^{1/4}|Ω| gain [B24, B26–B28].
- Compiled analogues show quadratic-walk crossovers of 10²–10⁶ days [B46, B47, B34].
- For protein partition functions, the incumbents are often not MCMC (bounded enumeration [B75], weighted counting [B76], tensor networks [B57]).
- The only route to relevance is the √δ factor with a measured, extremely small δ(L) on an endpoint-relevant posterior. That makes it a sub-case of AA-1 and gated by OP-01. If OP-01 finds δ(L) collapsing exponentially with length, this could be upgraded to INTERESTING as a category-3 resource-estimate study, still not an empirical advantage.

**P3. Quantum free-energy algorithms (Liouvillian/KvN; QM/MM bookending on hardware): WEAK, and out of structure scope.**
- These target electronic-structure accuracy (force-field bias) in binding free energies, not Monte Carlo variance, and not structure prediction.
- FT versions have no concrete resource counts and are compared only to prior quantum algorithms [B53, B54].
- Hardware versions claim no speedup [B55, B56].
- Relevant to AA-3, not to this program's endpoint.

**P4. NISQ / low-depth / variational AE: KILLED.**
- The gain is capped by the affordable depth [B6], and error saturates on hardware [B11].
- VQAE is "typically" more expensive than classical MC [B7].
- A single protein-observable oracle exceeds NISQ depth.

**P5. Data loading / state preparation as an enabling route (Grover–Rudolph, qGAN, arithmetic-free encodings): KILLED as a route to a protein-ensemble speedup.**
- There is a no-speedup theorem for Grover–Rudolph [B37].
- Conformational Boltzmann distributions lack integrable marginals.
- Learned loaders add bias and uncounted training cost [B40].
- Arithmetic-free AE [B38, B45] helps the integrand side only.

**Overall answer to the key question.** No protein-structure computation identified in the literature, or in S29–S33, is plausibly limited by Monte Carlo *variance* in the sense that a quadratic precision speedup could matter after oracle, state-preparation and error-correction overheads. The quantitative crossover (§5) confirms this with margins of several orders of magnitude.

The residual open question is **mixing** (spectral gap), not variance. That is a quantum-walk / Domain-A question which must first be settled classically (OP-01).
