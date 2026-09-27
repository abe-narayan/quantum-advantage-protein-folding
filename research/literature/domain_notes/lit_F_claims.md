# Domain F — Recent quantum advantage / utility claims (2019–2026), classical rebuttals, and cross-cutting counterarguments

_Literature evidence notes for the coordinator. Compiled 2026-09-26. No experiments run, no repo files edited. Every entry in §2 was checked in this session against an authoritative page (arXiv abs/API record, publisher/DOI page, Crossref, DBLP or an institutional record); the URL checked is recorded. Anything not checked is in §9 only._

Label vocabulary used (from LIT_RULES): THEORETICAL SPEEDUP | QUERY-COMPLEXITY SPEEDUP | ASYMPTOTIC SPEEDUP | SAMPLING SPEEDUP | HEURISTIC ADVANTAGE | EMPIRICAL ADVANTAGE | HARDWARE DEMONSTRATION | SIMULATOR RESULT | ORACLE-MODEL RESULT | NO ADVANTAGE | ADVANTAGE DISPUTED.

---

## 1. Scope & search log

**Scope.** (a) Hardware "beyond-classical" claims: RCS (Google 2019, 2023/24, Willow 2024), boson sampling (Jiuzhang 2020, Borealis 2022), IBM utility (2023), D-Wave annealing dynamics (2025), Google OTOC "Quantum Echoes" (2025), with the classical rebuttals and counter-rebuttals. (b) Fault-tolerant primitives: Hamiltonian simulation (Lloyd, Taylor series, QSP, qubitization), QSVT and its unification, QITE, HHL. (c) Dequantization. (d) Chemistry resource estimates and the evidence against generic exponential advantage. (e) QML and quantum generative models (QBM, QCBM, IQP Born machines), trainability and classical simulability. (f) Cross-cutting counterarguments: quadratic-speedup overhead, QRAM/data loading, noise ⇒ classical simulability.

**Method.** Batched arXiv API look-ups (`export.arxiv.org/api/query?id_list=…`) for all papers with known arXiv ids (returns title, authors, dates, journal_ref, DOI, abstract), WebSearch for publisher/DOI records of non-arXiv papers, Crossref API for Nature metadata, text extraction of two PDFs (Reiher 2017, Goings 2022) for resource numbers. Four arXiv ids I tried from memory returned unrelated papers (2206.08264, 2309.15163, 2305.04856 and one other). They were **discarded** and the correct records were found by search (Madsen 2022 → DOI only; Hibat-Allah → 2303.15626).

**Queries used (WebSearch):**
- `Google Quantum AI 2025 Nature "quantum echoes" OTOC "constructive interference at the edge of quantum ergodicity"`
- `arxiv "Constructive interference at the edge of quantum ergodic dynamics"`; `arxiv "Quantum computation of molecular geometry via many-body nuclear spin echoes"`
- `classical simulation OTOC Google quantum echoes Willow rebuttal tensor network Pauli path 2025 arXiv`
- `Kim et al 2023 Nature "Evidence for the utility of quantum computing before fault tolerance"`
- `Madsen 2022 Nature "Quantum computational advantage with a programmable photonic processor"`
- `Aaronson "Read the fine print" Nature Physics 11 291 2015`; `Lloyd 1996 "Universal Quantum Simulators" Science`
- `Hibat-Allah "A framework for demonstrating practical quantum advantage…"`; `Chia … "Sampling-based sublinear low-rank matrix arithmetic framework" Journal of the ACM`
- `Schuster Yin Gao Yao "A polynomial-time classical algorithm for noisy quantum circuits" published`
- `Google Willow December 2024 random circuit sampling "10 septillion" years`
- `Unke 2024 Science Advances "Biomolecular dynamics with machine-learned quantum-mechanical force fields…"`
- `Ghazi Vakili quantum circuit Born machine KRAS inhibitors Nature Biotechnology`
- `quantum generative model protein structure prior sampler "Born machine" protein conformations`
- `"Born Ultimatum" conditions for classical surrogation of quantum generative models`
- `2025 arXiv classical computation FeMoco ground state energy Chan "quantum advantage"`
- `"Quantum supremacy using a programmable superconducting processor" "200 seconds" "10,000 years"`

**arXiv API batches (id_list):** 1910.11333, 2111.03011, 2103.03074, 2110.14502, 2304.11119, 2408.13687, 2207.06431, 2306.14887, 2306.16372, 2306.17839, 2306.15970, 2403.00910 | 2503.05693, 2503.08247, 2012.01625, 2109.11525, 2306.03709, 2211.03999, 2407.12768, 2112.01657, 2308.05077, 2308.03082, 2309.15642 | 1412.4687, 1312.1414, 1606.02685, 1610.06546, 1806.01838, 2105.02859, 1901.07653, 0811.3171, 1807.04271, 1910.06151, 1811.00414, 2111.09079, 1912.08854 | 1605.03590, 2011.03494, 2208.02199, 2202.01244, 2011.04149, 1902.02134, 2007.14460, 2301.04114, 2110.08163, 1601.02036, 1801.07686, 1904.02214, 2101.08354 | 2007.14451, 2203.01340, 2205.05786, 2312.09121, 2403.07059, 2011.01938, 1803.11173, 2101.02464, 2210.13200, 2305.02881, 2012.09265, 2208.11060 | 2506.10191, 2510.19550, 2510.19928, 2401.16317 | 2603.18825, 2604.15427, 2508.15759, 2507.11424 | 2408.12739, 2409.01706, 2210.13442, 2503.02934, 2502.15882, 2404.16351 | 1910.09534, 2406.18889, 2112.15083, 2312.15211, 2301.01203, 2205.08306 | 2511.01845, 2512.24801, 2402.08210, 2607.06675 | 2601.04621, 2503.21041, 1809.10307 | 2007.07391, 2307.00523, 2305.10310, 2210.15021.

---

## 2. Verified papers

Keys [F#] are used throughout. "Verified:" gives the page checked. Unless stated otherwise, quotes are from the abstract.

### 2A. Random-circuit sampling (RCS) claims and rebuttals

**[F1] Quantum supremacy using a programmable superconducting processor.** Arute, Arya, Babbush et al. (Google; 81 authors on the SI). Nature 574, 505–510 (2019). DOI 10.1038/s41586-019-1666-5. arXiv 1910.11333 (the arXiv record is the *Supplementary Information*). Verified: export.arxiv.org API record for 1910.11333; nature.com/articles/s41586-019-1666-5 (search snippet); PubMed 31645734 listing.
- Claim: "Sycamore processor takes about 200 seconds to sample one instance of a quantum circuit a million times—our benchmarks currently indicate that the equivalent task for a state-of-the-art classical supercomputer would take approximately 10,000 years."
- Algorithm: RCS on 53 qubits, 20 cycles, verified by linear XEB. Problem setting: sample from the output distribution of a random circuit. Comparator: Schrödinger–Feynman simulation on Summit (as estimated by the authors). Hardware, noisy (XEB fidelity about 0.2%). Limitations: the task has no application, and the classical estimate was quickly undercut ([F2]–[F6]).
- **Labels:** HARDWARE DEMONSTRATION; SAMPLING SPEEDUP (claimed); **ADVANTAGE DISPUTED** (the 2019 instance was later classically reproduced).

**[F2] Leveraging Secondary Storage to Simulate Deep 54-qubit Sycamore Circuits.** Pednault, Gunnels, Nannicini et al. (IBM), arXiv 1910.09534 (2019), no journal_ref. Verified: arXiv API.
- Claim: "Such circuits can be simulated with high fidelity to arbitrary depth in a matter of days" (a Summit disk-storage proposal; not executed at full scale).
- **Labels:** THEORETICAL (resource estimate); ADVANTAGE DISPUTED.

**[F3] Simulating the Sycamore quantum supremacy circuits.** Feng Pan, Pan Zhang, arXiv 2103.03074 (2021). The arXiv record has no journal_ref. (I believe it appeared in PRL in 2022 under a different title; that is not verified, see §9.) Verified: arXiv API.
- Claim: a big-batch tensor-network method "massively more efficient in computing a large number of correlated bitstring amplitudes". **Labels:** SIMULATOR RESULT (classical); ADVANTAGE DISPUTED.

**[F4] Solving the sampling problem of the Sycamore quantum circuits.** Pan, Chen, Zhang. PRL 129, 090502 (2022). DOI 10.1103/PhysRevLett.129.090502. arXiv 2111.03011. Verified: arXiv API (journal_ref and DOI present).
- Claim: "For the Sycamore quantum supremacy circuit with 53 qubits and 20 cycles, we have generated one million uncorrelated bitstrings … the approximate state ψ̂ has fidelity F≈0.0037. The whole computation has cost about 15 hours on a computational cluster with 512 GPUs … on a modern supercomputer with ExaFLOPS performance … a few dozens of seconds, which is faster than Google's quantum hardware."
- Comparator: this *is* the classical comparator. It is empirical, with a fidelity matched to the experiment's XEB. **Labels:** ADVANTAGE DISPUTED (for the 2019 claim).

**[F5] Closing the "Quantum Supremacy" Gap: Achieving Real-Time Simulation of a Random Quantum Circuit Using a New Sunway Supercomputer.** Yong (A.) Liu, Xin Liu et al. (17 authors). SC'21 (Gordon Bell). DOI 10.1145/3458817.3487399. arXiv 2110.14502. Verified: arXiv API.
- Claim: a tensor simulator with "near-optimal slicing scheme, and path-optimization strategy" that closes the Sycamore gap. **Labels:** ADVANTAGE DISPUTED.

**[F6] Classical Sampling of Random Quantum Circuits with Bounded Fidelity.** Kalachev, Panteleev, Zhou et al., arXiv 2112.15083 (2021). Verified: arXiv API. Contracts dominant paths partially, with a "rigorously bounded" fidelity. **Labels:** ADVANTAGE DISPUTED.

**[F7] Leapfrogging Sycamore: Harnessing 1432 GPUs for 7× Faster Quantum Random Circuit Sampling.** Xian-He Zhao, Han-Sen Zhong, Feng Pan et al. (13 authors), arXiv 2406.18889 (2024). Verified: arXiv API.
- Claim (abstract): "the first unambiguous experimental evidence to refute Sycamore's claim of quantum advantage". **Labels:** ADVANTAGE DISPUTED (2019 instance).

**[F8] Limitations of Linear Cross-Entropy as a Measure for Quantum Advantage.** Xun Gao, Kalinowski, Chou et al. (6). PRX Quantum 5, 010334 (2024). DOI 10.1103/PRXQuantum.5.010334. arXiv 2112.01657. Verified: arXiv API.
- An efficient classical algorithm achieves high XEB "without full circuit simulation", so XEB is spoofable in some regimes. **Labels:** ADVANTAGE DISPUTED (benchmark validity).

**[F9] Phase transition(s) in random circuit sampling.** Morvan, Villalonga, Mi et al. (178). Nature 634, 328–333 (2024). DOI 10.1038/s41586-024-07998-6. arXiv 2304.11119. Verified: arXiv API.
- Claim: "two phase transitions observable with XEB … by presenting an RCS experiment with 67 qubits at 32 cycles, we demonstrate that the computational cost of our experiment is beyond the capabilities of existing classical supercomputers, even when accounting for the inevitable presence of noise."
- The noise-strength phase transition defines where the output becomes spoofable, and the experiment is placed in the "stable computationally complex phase". **Labels:** HARDWARE DEMONSTRATION; SAMPLING SPEEDUP (claimed, **currently unrefuted** as far as I found for the 67q/32-cycle instance, though see [F10]'s asymptotic caveat).

**[F10] A polynomial-time classical algorithm for noisy random circuit sampling.** Aharonov, Gao, Landau, Liu, Vazirani. STOC 2023. DOI 10.1145/3564246.3585234. arXiv 2211.03999. Verified: arXiv API.
- Claim: a "polynomial time classical algorithm for sampling from the output distribution of a noisy random quantum circuit in the regime of anti-concentration … strong evidence that, in the presence of a constant rate of noise per gate, random circuit sampling (RCS) cannot be the basis of a scalable experimental violation of the extended Church-Turing thesis. Our algorithm is not practical in its current form, and does not address finite-size RCS based quantum supremacy experiments."
- **Labels:** THEORETICAL (classical); NO ADVANTAGE (asymptotic, noisy, uncorrected RCS).

**[F11] Quantum error correction below the surface code threshold.** Google Quantum AI (Acharya et al., 254 authors). Nature 638, 920–926 (2025). DOI 10.1038/s41586-024-08449-y. arXiv 2408.13687. Verified: arXiv API.
- Claim: "logical error rate … suppressed by a factor of Λ = 2.14 ± 0.02 when increasing the code distance by two, culminating in a 101-qubit distance-7 code with 0.143% ± 0.003% error per cycle … beyond break-even … by a factor of 2.4 ± 0.3 … limited by rare correlated error events occurring approximately once every hour."
- A single logical *memory*. There is no logical computation and no advantage claim in the paper. The "5 minutes vs 10^25 years" Willow RCS figure was a press/blog claim (Google blog, 9 Dec 2024, checked via search). It uses the [F9] methodology and is **not** a result of this paper. **Labels:** HARDWARE DEMONSTRATION (QEC milestone; no computational advantage).

**[F12] Suppressing quantum errors by scaling a surface code logical qubit.** Google Quantum AI (Acharya et al.). Nature 614 (2023). DOI 10.1038/s41586-022-05434-1. arXiv 2207.06431. Verified: arXiv API. Predecessor of [F11] (distance-5 slightly beats distance-3). **Label:** HARDWARE DEMONSTRATION (QEC).

### 2B. Boson sampling claims and spoofing

**[F13] Quantum computational advantage using photons (Jiuzhang).** Zhong, Wang, Deng et al. (24). Science 370, 1460 (2020). DOI 10.1126/science.abe8770. arXiv 2012.01625. Verified: arXiv API.
- Claim: GBS "sampling rate … 10^14 faster than using the state-of-the-art simulation strategy and supercomputers." **Labels:** HARDWARE DEMONSTRATION; SAMPLING SPEEDUP (claimed); ADVANTAGE DISPUTED ([F15], [F16]).

**[F14] Quantum computational advantage with a programmable photonic processor (Borealis).** Madsen, Laudenbach et al. Nature 606, 75 (2022). DOI 10.1038/s41586-022-04725-x. Verified: nature.com article page and ADS 2022Natur.606...75M (via search). arXiv id not verified.
- Claim: ">9,000 years for the best available algorithms and supercomputers to produce a single sample … using exact methods, whereas Borealis requires only 36 μs." **Labels:** HARDWARE DEMONSTRATION; ADVANTAGE DISPUTED ([F16]).

**[F15] Efficient approximation of experimental Gaussian boson sampling.** Villalonga, Niu, Li et al. (7), arXiv 2109.11525 (2021). Verified: arXiv API. Polynomial (low-order marginal) approximations match the experiments on the benchmarks used. **Label:** ADVANTAGE DISPUTED.

**[F16] Classical algorithm for simulating experimental Gaussian boson sampling.** Oh, Liu, Alexeev, Fefferman, Jiang. Nature Physics 20, 1461–1468 (2024). DOI 10.1038/s41567-024-02535-8. arXiv 2306.03709. Verified: arXiv API.
- The abstract reports that, because the experiments "inevitably suffer from loss and other noise", the authors' classical (tensor-network) algorithm outperforms large-scale GBS experiments on the quantum-advantage benchmarks. **Label:** ADVANTAGE DISPUTED.

**[F17] Spoofing cross entropy measure in boson sampling.** Oh, Jiang, Fefferman. PRL 131, 010401 (2023). DOI 10.1103/PhysRevLett.131.010401. arXiv 2210.15021. Verified: arXiv API.
- Claim: "a heuristic classical algorithm that attains a better XE than the current BS experiments in a verifiable regime." **Label:** ADVANTAGE DISPUTED (benchmark).

### 2C. IBM "utility" (2023) and rebuttals

**[F18] Evidence for the utility of quantum computing before fault tolerance.** Y. Kim, Eddins, Anand et al. (IBM). Nature 618, 500–505 (2023). DOI 10.1038/s41586-023-06096-3. No arXiv. Verified: Crossref API api.crossref.org/works/10.1038/s41586-023-06096-3; DBLP record (search).
- Claim: accurate expectation values on a noisy 127-qubit processor "at a scale beyond brute-force classical computation … in regimes of strong entanglement, the quantum computer provides correct results for which leading classical approximations such as pure-state-based 1D (MPS) and 2D (isoTNS) tensor network methods break down."
- Algorithm: Trotterised 2D transverse-field (kicked) Ising on heavy-hex, with zero-noise extrapolation (ZNE). Comparator: MPS and isoTNS only. **Labels:** HARDWARE DEMONSTRATION; **ADVANTAGE DISPUTED** (reproduced classically within weeks: [F19]–[F24]).

**[F19] Efficient tensor network simulation of IBM's Eagle kicked Ising experiment.** Tindall, Fishman, Stoudenmire, Sels. PRX Quantum 5, 010308 (2024). DOI 10.1103/PRXQuantum.5.010308. arXiv 2306.14887. Verified: arXiv API.
- Claim: "an accurate and efficient classical simulation of a kicked Ising quantum system on the heavy-hexagon lattice." Method: belief-propagation-gauged tensor network matched to the heavy-hex geometry. **Label:** ADVANTAGE DISPUTED.

**[F20] Fast classical simulation of evidence for the utility of quantum computing before fault tolerance.** Begušić, Chan, arXiv 2306.16372 (2023). Verified: arXiv API.
- Claim: "sparse Pauli dynamics can efficiently simulate … on a single core of a laptop … orders of magnitude faster than the reported walltime." **Label:** ADVANTAGE DISPUTED.

**[F21] Fast and converged classical simulations of evidence for the utility of quantum computing before fault tolerance.** Begušić, **Gray**, Chan. Sci. Adv. 10, eadk4321 (2024). DOI 10.1126/sciadv.adk4321. arXiv 2308.05077. Verified: arXiv API.
- Note: the task brief says "Begušić & Chan 2024 Science Advances". The published Sci. Adv. version has three authors, including J. Gray. The two-author paper is [F20] (arXiv only, as checked). Claim: classical simulations "match or exceed experimental accuracy orders of magnitude faster". **Label:** ADVANTAGE DISPUTED.

**[F22] Classical benchmarking of zero noise extrapolation beyond the exactly-verifiable regime.** Anand, Temme, Kandala, Zaletel, arXiv 2306.17839 (2023). Verified: arXiv API. Classical benchmarking of the ZNE results beyond the exactly verifiable regime, with IBM co-authors. Only the first two abstract sentences were read in this session, so the specific classical method is not stated here. **Label:** SIMULATOR RESULT (classical benchmarking).

**[F23] Effective quantum volume, fidelity and computational cost of noisy quantum processing experiments.** Kechedzhi, Isakov, Mandrà et al. (Google; 7). Future Gener. Comput. Syst. 153, 431–441 (2024). DOI 10.1016/j.future.2023.12.002. arXiv 2306.15970. Verified: arXiv API.
- Claim: an "effective circuit volume" framework explaining the tradeoff between SNR and classical cost. It "allows us to reproduce the results of Ref. [7] [IBM] in less than one second per data point using one GPU." **Label:** ADVANTAGE DISPUTED.

**[F24] Simulation of IBM's kicked Ising experiment with Projected Entangled Pair Operator.** Liao, Wang, Zhou et al., arXiv 2308.03082 (2023). Verified: arXiv API. **[F25] Efficient tensor network simulation of IBM's largest quantum processors.** Patra, Jahromi, Singh, Orús. Phys. Rev. Research 6, 013326 (2024). DOI 10.1103/PhysRevResearch.6.013326. arXiv 2309.15642. Verified: arXiv API. It simulates "Eagle (127 qubits), Osprey (433 qubits) and Condor (1121 qubits)". **Label (both):** ADVANTAGE DISPUTED.

### 2D. D-Wave "beyond-classical" quantum simulation (2025) and rebuttals

**[F26] Beyond-classical computation in quantum simulation.** King, Nocera, Rams et al. (50). Science 388, 199–204 (2025). DOI 10.1126/science.ado6285. arXiv 2403.00910. Verified: arXiv API.
- Claim: "superconducting quantum annealing processors can rapidly generate samples in close agreement with solutions of the Schrödinger equation. We demonstrate area-law scaling of entanglement in the model quench dynamics of two-, three-, and infinite-dimensional spin glasses, supporting the observed stretched-exponential scaling of effort for matrix-product-state approaches. We show that several leading approximate methods based on tensor networks and neural networks cannot achieve the same accuracy as the quantum annealer within a reasonable time frame."
- Algorithm: analog quench (annealing) dynamics; the observables are correlations after a finite-time quench. **Labels:** HARDWARE DEMONSTRATION; ADVANTAGE DISPUTED ([F27], [F28]; counter-response [F29]).

**[F27] Dynamics of disordered quantum systems with two- and three-dimensional tensor networks.** Tindall, Mello, Fishman, Stoudenmire, Sels. **Science 392, 868–872 (2026)**. DOI 10.1126/science.adx2728. arXiv 2503.05693. Verified: arXiv API (journal_ref and DOI present).
- Claim: using "lattice-specific tensor networks, using belief propagation … state-of-the-art accuracies can be achieved with modest computational resources … scalable in both two and three dimensions." **Label:** ADVANTAGE DISPUTED.

**[F28] Challenging the Quantum Advantage Frontier with Large-Scale Classical Simulations of Annealing Dynamics.** Mauron, Carleo, arXiv 2503.08247 (2025). No journal_ref on arXiv as checked. Verified: arXiv API.
- Claim: "time-dependent variational Monte Carlo (t-VMC) with a physically motivated Jastrow-Feenberg wave function can efficiently simulate the quantum annealing of spin glasses … only polynomially scaling computational resources … For systems up to 128 spins on a three-dimensional diamond lattice, we maintain correlation errors below 7%, which match or exceed the precision of existing quantum hardware." **Label:** ADVANTAGE DISPUTED (for sizes up to 128 spins; the D-Wave claim involved larger systems).

**[F29] Evaluating classical simulations with a quantum processor.** Nocera, Raymond, Bernoudy et al. (D-Wave; 5), arXiv 2508.15759 (2025). Verified: arXiv API.
- Counter-rebuttal. It uses the annealer as ground truth for evaluating tensor-network methods: "Our observations run contrary to previous scaling predictions, demonstrating the need for caution when extrapolating the accuracy of classical simulations." **Label:** HARDWARE DEMONSTRATION; the dispute is **unresolved**.

### 2E. Google OTOC / "Quantum Echoes" (2025)

**[F30] Observation of constructive interference at the edge of quantum ergodicity.** Google Quantum AI and collaborators (Abanin, Acharya, Aghababaie-Beni et al.; 185 authors on arXiv). Nature 646, 825–830 (2025). DOI 10.1038/s41586-025-09526-6. arXiv 2506.10191 (arXiv title: "Constructive interference at the edge of quantum ergodic dynamics"). Verified: arXiv API; Google Research blog research.google/blog/a-verifiable-quantum-advantage/; search listing (PubMed 41125780, Caltech Authors).
- Claim (arXiv): "OTOC(2) is dominated by constructive interference between Pauli strings that form large loops … endows OTOC(2) with a high degree of classical simulation complexity, culminating in a set of large-scale OTOC(2) measurements exceeding the simulation capacity of known classical algorithms."
- Blog: about 13,000× faster than Frontier, comparing nine classical algorithms. It used 65 qubits for the advantage instance, and QMC was argued to fail because of sign structure. Secondary coverage cites about 2.1 h on the device versus about 3.2 years on Frontier; I did not check that against the paper.
- **Labels:** HARDWARE DEMONSTRATION; EMPIRICAL ADVANTAGE (claimed; an *expectation value*, not sampling). As of the literature found, **not refuted** ([F31], [F32]).

**[F31] Tensor Networks with Belief Propagation Cannot Feasibly Simulate Google's Quantum Echoes Experiment.** Bermejo, Villalonga, Ware et al. (5), arXiv 2604.15427 (2026). Verified: arXiv API.
- Claim: "the OTOC circuits generate enough entanglement that they are largely incompressible, implying that other approaches in which OTOCs are computed by evolving a tensor network state in the Schrödinger picture will also fail." (Villalonga is a Google author, so this is not an independent test.) **Label:** supports [F30].

**[F32] Quantum Advantage: a Tensor Network Perspective.** Kshetrimayum, Jahromi, Singh, Orús, arXiv 2603.18825 (2026). **REVIEW (orientation only).** Verified: arXiv API.
- It reviews the IBM, D-Wave and Google claims from a tensor-network viewpoint. Per the search snippet, Willow's SNR "currently remains unchallenged by published classical simulations". See also [F33].

**[F33] Simulating and Sampling from Quantum Circuits with 2D Tensor Networks.** Rudolph, Tindall, arXiv 2507.11424 (2025). Verified: arXiv API. "We observe a rapid buildup of complex loop correlations on the Google Willow geometry … loop correlations build up extremely slowly on heavy-hex processors … underscore[s] the role the geometry of the quantum processor plays in classical simulability." This explains *why* the IBM claim fell and the Google claims stand.

**[F34] Quantum computation of molecular geometry via many-body nuclear spin echoes.** C. Zhang, Cortiñas, Karamlou et al. (89), arXiv 2510.19550 (2025). Verified: arXiv API; Google blog.
- OTOCs measured by NMR on toluene and 3',5'-dimethylbiphenyl in a liquid crystal are interpreted by simulating them on Willow. They estimate an H–H distance and a dihedral angle "with similar accuracy and precision to independent spectroscopic measurements". The Google blog states this demonstration "is not yet beyond classical".
- **Labels:** HARDWARE DEMONSTRATION; **NO ADVANTAGE (self-declared)**. It is the only advantage-programme experiment that touches *molecular geometry*.

### 2F. Noisy-circuit and trainable-circuit classical simulability

**[F35] A polynomial-time classical algorithm for noisy quantum circuits.** Schuster, Yin, Gao, Yao. Phys. Rev. X 15, 041018 (2025) (DOI 10.1103/xct1-7kf2, from the APS page in search). arXiv 2407.12768. Verified: arXiv API; journals.aps.org/prx/abstract/10.1103/xct1-7kf2 (search listing).
- Claim: "computes the expectation value of any observable for any circuit, with a small average error over input states drawn from an ensemble … sampling … in quasi-polynomial time, so long as the distribution anti-concentrates … for constant noise rates, any quantum circuit for which error mitigation is efficient on most input states, is also classically simulable on most input states."
- **Label:** THEORETICAL (classical); NO ADVANTAGE (noisy, uncorrected, average-case).

**[F36] Classically estimating observables of noiseless quantum circuits.** Angrisani, Schmidhuber, Rudolph et al. (6). PRL 135, 170602 (2025). DOI 10.1103/lh6x-7rc3. arXiv 2409.01706. Verified: arXiv API.
- Claim: "Estimating observables of quantum circuits exhibiting chaotic and locally scrambling behavior is classically tractable" (Pauli propagation, average-case). **Label:** NO ADVANTAGE (average-case, for that circuit class).

**[F37] Does provable absence of barren plateaus imply classical simulability?** Cerezo, Larocca, García-Martín et al. (12). Nat. Commun. 16, 7907 (2025). DOI 10.1038/s41467-025-63099-6. arXiv 2312.09121. **Perspective.** Verified: arXiv API.
- Claim: "many commonly used models whose loss landscapes avoid barren plateaus can also admit classical simulation, provided that one can collect some classical data from quantum devices during an initial data acquisition phase … current approaches for solving them end up encoding the problem into some small, classically simulable, subspaces." The abstract itself lists the caveats (average-case arguments, smart initialisations, models outside the assumptions). **Label:** NO ADVANTAGE (argued, case-by-case).

**[F38] Barren plateaus in quantum neural network training landscapes.** McClean, Boixo, Smelyanskiy, Babbush, Neven. Nat. Commun. 9, 4812 (2018). DOI 10.1038/s41467-018-07090-4. arXiv 1803.11173. Verified: arXiv API. For random PQCs, the probability that the gradient is non-zero to fixed precision is exponentially small in the number of qubits. **Label:** THEORETICAL (negative).

**[F39] Beyond Barren Plateaus: Quantum Variational Algorithms Are Swamped With Traps.** Anschuetz, Kiani. Nat. Commun. 13, 7760 (2022). DOI 10.1038/s41467-022-35364-5. arXiv 2205.05786. Verified: arXiv API. Shallow, non-BP models have a "superpolynomially small fraction of good local minima". **Label:** THEORETICAL (negative).

**[F40] Quantum Convolutional Neural Networks are Effectively Classically Simulable.** Bermejo, Braccia, Rudolph et al. (6). PRX Quantum 7, 020304 (2026). DOI 10.1103/8qt9-72ts. arXiv 2408.12739. Verified: arXiv API. **Label:** NO ADVANTAGE.

### 2G. Hamiltonian simulation, QSP, QSVT, QITE

**[F41] Universal Quantum Simulators.** S. Lloyd. Science 273, 1073–1078 (1996). DOI 10.1126/science.273.5278.1073. Verified: science.org DOI page and ADS/PubMed 8688088 (search). Shows that Feynman's conjecture holds for local Hamiltonians (Trotterised evolution with polynomial gate count). **Label:** THEORETICAL SPEEDUP (exponential over exact classical state-vector simulation of generic local quantum dynamics).

**[F42] Exponential improvement in precision for simulating sparse Hamiltonians.** Berry, Childs, Cleve, Kothari, Somma. STOC 2014. DOI 10.1145/2591796.2591854. arXiv 1312.1414. Verified: arXiv API. **[F43] Simulating Hamiltonian dynamics with a truncated Taylor series.** Same five authors. PRL 114, 090502 (2015). DOI 10.1103/PhysRevLett.114.090502. arXiv 1412.4687. Verified: arXiv API. Claim: the "cost of our method depends only logarithmically on the inverse of desired precision." **Labels:** QUERY-COMPLEXITY SPEEDUP / THEORETICAL.

**[F44] Optimal Hamiltonian Simulation by Quantum Signal Processing.** Low, Chuang. PRL 118, 010501 (2017). DOI 10.1103/PhysRevLett.118.010501. arXiv 1606.02685. Verified: arXiv API. The query complexity "matches lower bounds in all parameters" (sparse-oracle model). **Label:** QUERY-COMPLEXITY SPEEDUP (optimal); ORACLE-MODEL RESULT.

**[F45] Hamiltonian Simulation by Qubitization.** Low, Chuang. Quantum 3, 163 (2019). DOI 10.22331/q-2019-07-12-163. arXiv 1610.06546. Verified: arXiv API. Query complexity "O(t+log(1/ε))" (with t measured in units of the block-encoding normalisation), "optimal in asymptotic and non-asymptotic regime". **Label:** QUERY-COMPLEXITY SPEEDUP; ORACLE-MODEL (block-encoding) RESULT.

**[F46] Quantum singular value transformation and beyond: exponential improvements for quantum matrix arithmetics.** Gilyén, Su, Low, Wiebe. STOC 2019, 193–204. DOI 10.1145/3313276.3316366. arXiv 1806.01838. Verified: arXiv API. Polynomial transformations of the singular values of block-encoded matrices, in a unified framework. **Labels:** QUERY-COMPLEXITY; ORACLE-MODEL RESULT (the "exponential improvements" are relative to prior quantum methods and require block-encoding access).

**[F47] A Grand Unification of Quantum Algorithms.** Martyn, Rossi, Tan, Chuang. PRX Quantum 2, 040203 (2021). DOI 10.1103/PRXQuantum.2.040203. arXiv 2105.02859. **REVIEW/tutorial.** Verified: arXiv API.

**[F48] A Theory of Trotter Error.** Childs, Su, Tran, Wiebe, Zhu. PRX 11, 011020 (2021). DOI 10.1103/PhysRevX.11.011020. arXiv 1912.08854. Verified: arXiv API. Tighter commutator-scaling Trotter bounds, making product formulas competitive in practice. **Label:** THEORETICAL.

**[F49] Determining eigenstates and thermal states on a quantum computer using quantum imaginary time evolution (QITE).** Motta, Sun, Tan et al. (8). Nature Physics 16, 205–210 (2020). DOI 10.1038/s41567-019-0704-4. arXiv 1901.07653. Verified: arXiv API.
- Claim: QITE and related algorithms require "exponentially less space and time per iteration" than classical counterparts. The key assumption is a finite correlation length: the unitary domain, and hence the tomography and linear-solve cost, grows exponentially with correlation length. The "exponentially less" is per iteration, not end-to-end. **Labels:** THEORETICAL; SIMULATOR RESULT plus small hardware tests.

### 2H. Linear systems, dequantization, data loading

**[F50] Quantum algorithm for solving linear systems of equations (HHL).** Harrow, Hassidim, Lloyd. PRL 103, 150502 (2009). DOI 10.1103/PhysRevLett.103.150502. arXiv 0811.3171. Verified: arXiv API. "runs in poly(log N, κ) time, an exponential improvement". It outputs a *quantum state* |x⟩, not x, and needs sparse-oracle access and efficient preparation of |b⟩. **Labels:** ORACLE-MODEL RESULT; THEORETICAL SPEEDUP (conditional).

**[F51] Read the fine print.** S. Aaronson. Nature Physics 11, 291–293 (2015). DOI 10.1038/nphys3272. Verified: nature.com/articles/nphys3272 (search listing). This is the standard list of caveats for HHL-type QML: input loading, sparsity/conditioning, output readout, and the need to compare against the best classical algorithm. **COMMENTARY.**

**[F52] A quantum-inspired classical algorithm for recommendation systems.** E. Tang. STOC 2019. DOI 10.1145/3313276.3316310. arXiv 1807.04271. Verified: arXiv API. Given ℓ²-norm sampling access (the classical analogue of QRAM state preparation), the classical algorithm is "only polynomially slower than the quantum algorithm". **Label:** NO ADVANTAGE (exponential → polynomial) for low-rank recommendation.

**[F53] Quantum principal component analysis only achieves an exponential speedup because of its state preparation assumptions.** E. Tang. PRL 127, 060503 (2021). DOI 10.1103/PhysRevLett.127.060503. arXiv 1811.00414. Verified: arXiv API. **Label:** NO ADVANTAGE (exponential) under matched access models.

**[F54] Sampling-based sublinear low-rank matrix arithmetic framework for dequantizing quantum machine learning.** Chia, Gilyén, Li, Lin, Tang, Wang. STOC 2020 (DOI 10.1145/3357713.3384314) and J. ACM 69(5) (2022) (DOI 10.1145/3549524). arXiv 1910.06151. Verified: arXiv API; dl.acm.org/doi/10.1145/3549524 (search).
- Classical singular-value transformation of low-rank matrices "in time independent of input dimension" under sampling access. It dequantizes QSVT-based QML *for low-rank inputs*. The polynomial degrees are large, so polynomial quantum gaps may remain. **Label:** NO ADVANTAGE (exponential), low-rank regime.

**[F55] Dequantizing the Quantum Singular Value Transformation: Hardness and Applications to Quantum Chemistry and the Quantum PCP Conjecture.** Gharibian, Le Gall. SIAM J. Comput. 52(4), 1009–1038 (2023). DOI 10.1137/22M1513721. arXiv 2111.09079. Verified: arXiv API. It dequantizes constant-precision QSVT for sparse matrices with low-degree polynomials, and proves BQP-hardness at higher precision. This sets the dividing line: **precision** is where quantum advantage lives. **Label:** THEORETICAL (both directions).

**[F56] QRAM: A Survey and Critique.** Jaques, Rattew. Quantum 9, 1922 (2025). DOI 10.22331/q-2025-12-02-1922. arXiv 2305.10310. Verified: arXiv API.
- Claim: "In the active model … one could repurpose the control hardware … to run an extremely parallel classical algorithm to achieve the same results just as fast. We … prove that most asymptotic quantum advantage disappears with active QRAM systems … cheap, asymptotically scalable passive QRAM is unlikely with existing proposals." **Label:** NO ADVANTAGE (for data-loading-dominated quantum linear algebra).

**[F57] Disentangling Hype from Practicality: On Realistically Achieving Quantum Advantage.** Hoefler, Häner, Troyer. Commun. ACM (May 2023). arXiv 2307.00523. Verified: arXiv API (journal_ref "CACM May 2023").
- Claim: "small data problems and quantum algorithms with super-quadratic speedups are essential to make quantum computers useful in practice." **PERSPECTIVE.**

### 2I. Chemistry / electronic structure: resources and the evidence debate

**[F58] Elucidating Reaction Mechanisms on Quantum Computers.** Reiher, Wiebe, Svore, Wecker, Troyer. PNAS 114, 7555–7560 (2017). DOI 10.1073/pnas.1619152114. arXiv 1605.03590. Verified: arXiv API and the PDF text (Table I).
- FeMoco model with 54 electrons in 54 orbitals (CAS(54,54), about 108 spin-orbital qubits), Trotter + QPE. Table I, structure 1 at 0.1 mHa: serial 1.1×10^15 T gates, 130 days, 111 logical qubits. Nesting: 3.5×10^15 T, 15 days, 135 logical qubits. PAR: 3.1×10^16 T, 110 h, 1982 logical qubits.
- **Labels:** THEORETICAL (fault-tolerant resource estimate). The active space was later criticised as unrepresentative ([F63]).

**[F59] Qubitization of Arbitrary Basis Quantum Chemistry Leveraging Sparsity and Low Rank Factorization.** Berry, Gidney, Motta, McClean, Babbush. Quantum 3, 208 (2019). DOI 10.22331/q-2019-12-02-208. arXiv 1902.02134. Verified: arXiv API. Reports "700 times less surface code spacetime volume than prior quantum algorithms" for FeMoco. **Label:** THEORETICAL (resource estimate).

**[F60] Quantum computing enhanced computational catalysis.** von Burg, Low, Häner et al. (7). Phys. Rev. Research 3, 033055 (2021). DOI 10.1103/PhysRevResearch.3.033055. arXiv 2007.14460. Verified: arXiv API. Double factorisation for a Ru catalyst. **Label:** THEORETICAL (resource estimate).

**[F61] Even more efficient quantum computations of chemistry through tensor hypercontraction.** J. Lee, Berry, Gidney et al. (7). PRX Quantum 2, 030305 (2021). DOI 10.1103/PRXQuantum.2.030305. arXiv 2011.03494. Verified: arXiv API.
- Claim: "quantum circuits with only Õ(N) Toffoli complexity that block encode the spectra of quantum chemistry Hamiltonians … With O(λ/ε) repetitions … FeMoCo can be simulated using about four million physical qubits and under four days of runtime, assuming 1 μs cycle times and physical gate error rates no worse than 0.1%." **Label:** THEORETICAL (resource estimate); fault tolerance required.

**[F62] Reliably assessing the electronic structure of cytochrome P450 on today's classical computers and tomorrow's quantum computers.** Goings, White, Lee et al. (9). PNAS 119 (2022). DOI 10.1073/pnas.2203533119. arXiv 2202.01244. Verified: arXiv API and PDF text.
- Abstract: CYP models "at scales large enough to balance dynamic and multiconfigurational electron correlation has the potential to be a quantum advantage problem". PDF text: the largest Cpd I active space "can be assessed with approximately 4.6 million physical qubits in 73 hours of run time" at 0.1% physical error. The THC table shows about 1426 logical qubits and Toffoli counts of about 4–6×10^9 per phase-estimation run.
- The classical comparator is converged DMRG+NEVPT2 / CCSD(T), a *well-defined* frontier. **Label:** THEORETICAL (resource estimate); advantage "potential", not shown.

**[F63] The electronic complexity of the ground-state of the FeMo cofactor of nitrogenase as relevant to quantum simulations.** Z. Li, J. Li, Dattani, Umrigar, Chan. J. Chem. Phys. (2019). DOI 10.1063/1.5063376. arXiv 1809.10307. Verified: arXiv API. The Reiher active space "is not representative of the electronic structure of the FeMo cofactor ground-state". **Label:** ADVANTAGE DISPUTED (benchmark validity).

**[F64] Is there evidence for exponential quantum advantage in quantum chemistry? (published as "Evaluating the evidence for exponential quantum advantage in ground-state quantum chemistry").** S. Lee, J. Lee, Zhai et al. (16). Nat. Commun. 14, 1952 (2023). DOI 10.1038/s41467-023-37587-6. arXiv 2208.02199. Verified: arXiv API (the arXiv title is the question form; journal_ref and DOI present).
- Claim: "We conclude that evidence for such an exponential advantage across chemical space has yet to be found. While quantum computers may still prove useful for quantum chemistry, it may be prudent to assume exponential speedups are not generically available for this problem."
- The core arguments (from the paper): state preparation needs an initial state with non-negligible overlap, and overlap can decay exponentially with system size, so QPE's exponential advantage depends on it. Classical heuristics (DMRG, CC, QMC) show no generic exponential cost growth on the studied systems. **Label:** NO ADVANTAGE (exponential, generic); polynomial advantage left open.

**[F65] Classical computational simulation of the FeMo-cofactor model to chemical accuracy and its implications.** Zhai, C. Li, X. Zhang, Z. Li, S. Lee, Chan, arXiv 2601.04621 (2026, preprint). Verified: arXiv abs page.
- Claim: "We use classical computational methods to estimate the ground-state energy to chemical accuracy in a model of the FeMo-cofactor of nitrogenase which is widely studied as a target of quantum computing." Methods: CC + DMRG with extrapolation, plus unrestricted/split-localised orbitals (per a secondary summary). **Label:** ADVANTAGE DISPUTED (for the canonical FeMoco benchmark), pending peer review.

**[F66] Focus beyond quadratic speedups for error-corrected quantum advantage.** Babbush, McClean, Newman, Gidney, Boixo, Neven. PRX Quantum 2, 010103 (2021). DOI 10.1103/PRXQuantum.2.010103. arXiv 2011.04149. Verified: arXiv API.
- Claim: "quadratic speedups will not enable quantum advantage on early generations of such fault-tolerant devices unless there is a significant improvement in how we would realize quantum error-correction … quartic speedups look significantly more practical." **Label:** THEORETICAL (cost model; NO ADVANTAGE for quadratic on early fault-tolerant hardware).

**[F67] Compilation of Fault-Tolerant Quantum Heuristics for Combinatorial Optimization.** Sanders, Berry, Costa et al. (8). PRX Quantum 1, 020312 (2020). DOI 10.1103/PRXQuantum.1.020312. arXiv 2007.07391. Verified: arXiv API.
- Claim: "quantum accelerated simulated annealing would require roughly a day and a million physical qubits to optimize spin glasses that could be solved by classical simulated annealing in about four CPU-minutes." This paper bears directly on Szegedy-walk and QSA proposals for Boltzmann sampling. **Label:** THEORETICAL (resource estimate; NO ADVANTAGE on modest surface-code hardware).

**[F68] Quantum simulation of exact electron dynamics can be more efficient than classical mean-field methods.** Babbush, Huggins, Berry et al. (9). Nat. Commun. 14, 4058 (2023). DOI 10.1038/s41467-023-39024-0. arXiv 2301.01203. Verified: arXiv API. First-quantised algorithms give "exact time evolution with exponentially less space and polynomially fewer operations in basis set size" than classical mean-field. **Label:** ASYMPTOTIC SPEEDUP (polynomial in basis size; fault tolerance required).

**[F69] Fast quantum simulation of electronic structure by spectrum amplification.** Low, R. King, Berry et al. (9). PRX 15, 041016 (2025). DOI 10.1103/pb2g-j9cw. arXiv 2502.15882. Verified: arXiv API. Improved ground-state-energy cost scaling. **Label:** THEORETICAL (resource/asymptotic).

**[F70] Drug design on quantum computers.** Santagati, Aspuru-Guzik, Babbush et al. (15). Nature Physics (2024). DOI 10.1038/s41567-024-02411-5. arXiv 2301.04114. **PERSPECTIVE.** Verified: arXiv API.

**[F71] Quantum Computational Quantification of Protein-Ligand Interactions.** Kirsopp, Di Paola, Manrique et al. (10). Int. J. Quantum Chem. (2022). DOI 10.1002/qua.26975. arXiv 2110.08163. Verified: arXiv API.
- "First application of real quantum computers to the calculation of protein-ligand binding energies" (tiny active spaces). **Labels:** HARDWARE DEMONSTRATION; NO ADVANTAGE (the active spaces are classically trivial).

**[F72] Exponential quantum speedups for near-term molecular electronic structure methods.** Leimkuhler, Whaley, arXiv 2503.21041 (2025). Verified: arXiv API. It proves classical-simulation hardness "under the generalized P≠NP conjecture" for certain ansatz families (BQP-completeness). This is a hardness-of-*simulating-the-ansatz* result, not evidence that the ansatz solves chemistry better. **Label:** THEORETICAL.

**[F73] Biomolecular dynamics with machine-learned quantum-mechanical force fields trained on diverse chemical fragments (GEMS).** Unke, Stöhr, Ganscha et al. Sci. Adv. 10, eadn4397 (2024). DOI 10.1126/sciadv.adn4397. arXiv 2205.08306. Verified: arXiv API; science.org DOI page (search; erratum 10.1126/sciadv.adt0518 corrects an RMSD axis scaling without changing conclusions).
- arXiv: "nanosecond-scale MD simulations of >25k atoms at essentially ab initio quality". This is the classical route to QM-accuracy energies for *proteins*. **Label:** classical comparator.

**[F74] MACE-OFF: Transferable Short Range Machine Learning Force Fields for Organic Molecules.** Kovács, Moore, Browning et al. (11), arXiv 2312.15211 (2023). Verified: arXiv API. **Label:** classical comparator.

### 2J. QML and quantum generative models

**[F75] Quantum Boltzmann Machine.** Amin, Andriyash, Rolfe, Kulchytskyy, Melko. PRX 8, 021050 (2018). DOI 10.1103/PhysRevX.8.021050. arXiv 1601.02036. Verified: arXiv API. Transverse-field Boltzmann machine trained with bounds on the log-likelihood, using sampling from a quantum annealer or QMC. **Labels:** SIMULATOR RESULT (small); no advantage claim against strong classical baselines.

**[F76] A generative modeling approach for benchmarking and training shallow quantum circuits.** Benedetti, Garcia-Pintos, Perdomo, Leyton-Ortega, Nam, Perdomo-Ortiz. npj Quantum Inf. 5, 45 (2019). DOI 10.1038/s41534-019-0157-8. arXiv 1801.07686. Verified: arXiv API. QCBM with a qBAS benchmark "starting at four qubits". **Labels:** HARDWARE DEMONSTRATION (tiny); NO ADVANTAGE claim.

**[F77] The Born Supremacy: Quantum Advantage and Training of an Ising Born Machine.** Coyle, Mills, Danos, Kashefi. npj Quantum Inf. 6, 60 (2020). DOI 10.1038/s41534-020-00288-9. arXiv 1904.02214. Verified: arXiv API. The IBM model "cannot … be simulated efficiently by a classical device" under suitable error notions. This is sampling hardness of the model class, **not** an advantage in learning a given data distribution. **Label:** SAMPLING SPEEDUP (model-class hardness; complexity-conjecture based).

**[F78] Enhancing Generative Models via Quantum Correlations.** Gao, Anschuetz, Wang, Cirac, Lukin. PRX 12, 021037 (2022). DOI 10.1103/PhysRevX.12.021037. arXiv 2101.08354. Verified: arXiv API.
- Claim: "an unconditional proof of separation in expressive power between a class of widely-used generative models, known as Bayesian networks, and its minimal quantum extension … associated with quantum nonlocality and quantum contextuality." The comparator is Bayesian networks (of matched structure), not unrestricted deep generative models. **Label:** THEORETICAL (expressivity separation, restricted model classes).

**[F79] On the Quantum versus Classical Learnability of Discrete Distributions.** Sweke, Seifert, Hangleiter, Eisert. Quantum 5, 417 (2021). DOI 10.22331/q-2021-03-23-417. arXiv 2007.14451. Verified: arXiv API.
- Claim: "a class of discrete probability distributions which, under the decisional Diffie-Hellman assumption, is provably not efficiently PAC learnable by a classical generative modelling algorithm, but for which we construct an efficient quantum learner." The distributions are cryptographic constructs. **Label:** THEORETICAL SPEEDUP (conditional, contrived instance class).

**[F80] Is quantum advantage the right goal for quantum machine learning?** Schuld, Killoran. PRX Quantum 3, 030101 (2022). DOI 10.1103/PRXQuantum.3.030101. arXiv 2203.01340. **PERSPECTIVE.** Verified: arXiv API.

**[F81] Better than classical? The subtle art of benchmarking quantum machine learning models.** Bowles, Ahmed, Schuld, arXiv 2403.07059 (2024). No journal_ref as checked. Verified: arXiv API.
- Claim: "overall, out-of-the-box classical machine learning models outperform the quantum classifiers." (I recall that the paper also reports that removing entanglement often does not hurt performance. That was not re-read in this session, so it is not cited as evidence.) **Labels:** SIMULATOR RESULT; NO ADVANTAGE.

**[F82] Power of data in quantum machine learning.** H.-Y. Huang, Broughton, Mohseni et al. (7). Nat. Commun. 12, 2631 (2021). DOI 10.1038/s41467-021-22539-9. arXiv 2011.01938. Verified: arXiv API. Classical ML trained on data can predict some classically-hard-to-compute quantum functions. **Label:** NO ADVANTAGE (for data-driven prediction in many settings).

**[F83] Information-theoretic bounds on quantum advantage in machine learning.** Huang, Kueng, Preskill. PRL 126, 190505 (2021). DOI 10.1103/PhysRevLett.126.190505. arXiv 2101.02464. Verified: arXiv API. Average-case prediction error: classical and quantum learners have comparable sample complexity. An exponential advantage is possible for worst-case (all-input) prediction. **Label:** THEORETICAL.

**[F84] Classically Approximating Variational Quantum Machine Learning with Random Fourier Features.** Landman, Thabet, Dalyac, Mhiri, Kashefi, arXiv 2210.13200 (2022). Verified: arXiv API. A "classical sampling method may closely approximate a VQC with Hamiltonian encoding". **Label:** NO ADVANTAGE (dequantization of VQCs).

**[F85] Exponential concentration in quantum kernel methods.** Thanasilp, Wang, Cerezo, Holmes. npj Quantum Inf. (2024), DOI 10.1038/s41534-024-00902-0 (as returned by the arXiv API). arXiv 2208.11060. Verified: arXiv API. **Label:** THEORETICAL (negative).

**[F86] Trainability barriers and opportunities in quantum generative modeling.** Rudolph, Lerch, Thanasilp et al. (8). arXiv 2305.02881 (2023). The arXiv API returned the *same* DOI as [F85], which is probably a metadata error, so the DOI is not relied on. Verified: arXiv API (title/authors/abstract).
- Claim: explicit losses (e.g. KL) create "a new flavour of barren plateaus"; implicit losses (MMD) have different tradeoffs. **Label:** THEORETICAL (negative/mixed).

**[F87] A Framework for Demonstrating Practical Quantum Advantage: Racing Quantum against Classical Generative Models.** Hibat-Allah, Mauri, Carrasquilla, Perdomo-Ortiz. Commun. Phys. (2024) (nature.com/articles/s42005-024-01552-6). arXiv 2303.15626. Verified: arxiv.org/abs/2303.15626 and the Commun. Phys. page (search).
- On a 20-variable task, QCBMs are "more efficient in the data-limited regime" than Transformer/RNN/VAE/WGAN baselines. **Labels:** SIMULATOR RESULT; HEURISTIC ADVANTAGE (small n, 20 qubits, which is classically simulable, so this is not a computational advantage).

**[F88] Protocols for classically training quantum generative models on probability distributions.** Kasture, Kyriienko, Elfving. PRA 108, 042406 (2023). DOI 10.1103/PhysRevA.108.042406. arXiv 2210.13442. Verified: arXiv API.

**[F89] Train on classical, deploy on quantum: scaling generative quantum machine learning to a thousand qubits.** Recio-Armengol, Ahmed, Bowles, arXiv 2503.02934 (2025). Verified: arXiv API.
- Claim: IQP-based generative models "can be trained efficiently on classical hardware. Although training is classically efficient, sampling from these circuits is widely believed to be classically hard … perform surprisingly well compared to simple energy-based classical generative models." **Labels:** SIMULATOR RESULT (classical training); SAMPLING SPEEDUP (conjectured for deployment); comparator is *simple* energy-based models only.

**[F90] The Born Ultimatum: Conditions for Classical Surrogation of Quantum Generative Models with Correlators.** Herrero-Gonzalez, Coyle, McDowall et al. (7), arXiv 2511.01845 (2025). Verified: arXiv API.
- Claim: "we identify QCBMs as a quantum Fourier model independently of the loss function. This allows us to apply known dequantization conditions … We analyze the limitations of [train-classical, deploy-quantum] methods arising from deployment discrepancies." **Label:** THEORETICAL (dequantization conditions).

**[F91] Limits of quantum generative models with classical sampling hardness.** Herbst, Brandić, Pérez-Salinas, arXiv 2512.24801 (2025). Verified: arXiv API.
- Claim: "models that anticoncentrate are not trainable on average, including those exhibiting quantum advantage. In contrast, models outputting data from sparse distributions can be trained … this opens the path for classical algorithms for surrogate sampling … quantum advantage can still be found in generative models, although its source must be distinct from anticoncentration." **Label:** THEORETICAL (negative for the "hard-to-sample ⇒ useful generator" argument).

**[F92] Spectral Born machines: classically trainable quantum generative models for discrete data.** A. Huang, Maxwell, Belis et al. (7), arXiv 2607.06675 (2026). Verified: arXiv API.
- It trains a "190-qubit model with over 1 million parameters to successfully learn a distribution of 93 nucleotide-long ribosomal RNA". The models are classically trained, with classical hardness of sampling claimed "in general". **Label:** SIMULATOR RESULT (classical training); no classical-baseline advantage stated in the abstract. This is the closest biosequence application found.

**[F93] Quantum-computing-enhanced algorithm unveils potential KRAS inhibitors.** Ghazi Vakili, Gorgulla, Nigam et al. (21). Nature Biotechnology 43, 1954–1959 (2025). DOI 10.1038/s41587-024-02526-3. arXiv 2402.08210 (title "Quantum Computing-Enhanced Algorithm Unveils Novel Inhibitors for KRAS"). Verified: arXiv API; nature.com article listing and PubMed 39843581 (search).
- A QCBM prior "trained on a 16-qubit IBM quantum computer" seeds a classical LSTM. 15 molecules were synthesised and 2 engaged KRAS. It claims that "efficacy of distribution learning correlates with the number of qubits utilized."
- A 16-qubit QCBM is exactly classically simulable (2^16 amplitudes), so any benefit is an inductive-bias / prior effect, not a quantum computational advantage. **Labels:** HARDWARE DEMONSTRATION; HEURISTIC ADVANTAGE claimed against a classical LSTM baseline; **NO computational advantage possible at this size.**

**[F94] Variational Quantum Algorithms.** Cerezo, Arrasmith, Babbush et al. (11). Nat. Rev. Phys. 3, 625–644 (2021). DOI 10.1038/s42254-021-00348-9. arXiv 2012.09265. **REVIEW (orientation only).** Verified: arXiv API.

### 2K. Orientation reviews (not used as primary evidence)

**[F95] Mind the gaps: The fraught road to quantum advantage.** Eisert, Preskill, arXiv 2510.19928 (2025). **REVIEW.** Verified: arXiv API. It names four transitions (error mitigation → correction; rudimentary → scalable fault tolerance; heuristics → mature algorithms; exploratory → credible simulation advantage).

**[F96] Assessing the Benefits and Risks of Quantum Computers.** Scholten, Williams, Moody et al. (8), arXiv 2401.16317 (2024). **REVIEW/policy**, low weight. Verified: arXiv API.

**Count: 96 entries verified** (about 88 primary; [F32], [F47], [F70], [F80], [F94], [F95] and [F96] are reviews or perspectives, and [F51] and [F57] are commentaries).

---

## 3. Primitive analyses (16 questions each)

Primitives in this domain:
- **P1** Sampling from classically-hard distributions (RCS/GBS) as a "sampler" primitive
- **P2** NISQ expectation-value estimation of many-body dynamics (utility / OTOC / annealing dynamics)
- **P3** Fault-tolerant Hamiltonian simulation + QPE for electronic structure (the chemistry lever)
- **P4** QSVT / quantum linear algebra (HHL-type) and its dequantization
- **P5** QITE / NISQ imaginary-time and thermal-state preparation
- **P6** Quantum generative models (QBM, QCBM, IQP/spectral Born machines) as structure priors or samplers
- **P7** Variational / parametrised QML more broadly (trainability ↔ simulability)
- **P8** Cross-cutting: the fault-tolerant cost of quadratic speedups (applies to AA-1/AA-2 in the Opportunity Map)

### P1 — Hard-distribution sampling (RCS / GBS)
1. **What the QC does:** it samples bitstrings from |⟨x|U|0⟩|² for a random U (RCS) or a photon-count pattern (GBS).
2. **What it replaces:** exact or approximate classical sampling of the same distribution.
3. **Why it is hard classically:** #P-hardness of output probabilities plus anticoncentration ([F77] style arguments), and tensor-network cost exponential in treewidth.
4. **Exact speedup:** none proven. The claims are runtime ratios at fixed instances: 200 s vs 10,000 yr ([F1], later refuted by [F4], [F5], [F7]); 67q/32-cycle "beyond supercomputers" ([F9]).
5. **Type:** sample / time.
6. **Assumptions:** complexity conjectures, plus fidelity high enough to sit above the noise phase transition ([F9]).
7. **Oracle:** none.
8. **Oracle cost:** n/a.
9. **State preparation:** trivial (|0⟩).
10. **Readout:** one shot per sample; verification by XEB needs classical simulation (exponential), and XEB can be spoofed ([F8], [F17]).
11. **Postprocessing:** XEB estimation.
12. **Strongest classical:** tensor-network contraction with slicing and big-batch methods ([F4], [F5], [F7]); asymptotically, poly-time for noisy anticoncentrated RCS ([F10], [F35]); for GBS, loss-exploiting tensor networks ([F16]).
13. **Survives?** 2019 Sycamore: no. 2020 Jiuzhang and 2022 Borealis: disputed or reproduced ([F15], [F16]). The 67-qubit 2023/24 RCS: stands so far. Asymptotically with constant noise and no QEC: no ([F10]).
14. **Fault tolerance:** not for demonstrations, but any *scalable* advantage needs error correction ([F10]).
15. **Resources:** 53–105 physical qubits, 20–32 cycles.
16. **Protein mapping:** **none.** The distributions are random and carry no information about any protein. "Hard to sample" is a property of the device's distribution, not of the posterior we need (Map SP-1).

### P2 — NISQ many-body expectation values (IBM utility, D-Wave quench, Google OTOC)
1. **What the QC does:** it estimates ⟨O(t)⟩ after Trotterised or analog dynamics, or OTOCs with time reversal.
2. **What it replaces:** classical simulation of quantum dynamics (tensor networks, Pauli propagation, t-VMC, QMC).
3. **Why it is hard classically:** entanglement growth (area/volume law), loop correlations on 2D lattices ([F33]), and the sign structure of OTOC(2) ([F30]).
4. **Exact speedup:** none proven. The claims are instance runtime ratios: OTOC about 13,000× vs Frontier ([F30]); the D-Wave claim is "cannot achieve same accuracy within reasonable time" ([F26]).
5. **Type:** time at fixed accuracy/SNR.
6. **Assumptions:** error mitigation (ZNE) for IBM, and a noise model that stays within the SNR window. For constant noise, efficient mitigation ⇒ classical simulability on most inputs ([F35]).
7. **Oracle:** none (native Hamiltonian).
8. **Oracle cost:** n/a.
9. **State preparation:** product states.
10. **Readout:** O(1/ε²) shots per observable, with SNR decaying exponentially with circuit volume ([F23]). This is the binding constraint.
11. **Postprocessing:** ZNE/PEC; the extrapolation can be biased ([F22]).
12. **Strongest classical:** BP-gauged tensor networks ([F19], [F27]); sparse Pauli dynamics ([F20], [F21]); t-VMC ([F28]); PEPO ([F24]); effective-volume tensor-network contraction ([F23]).
13. **Survives?**
    - IBM 2023: **no** (laptop-scale reproduction, [F20], [F21], [F23]).
    - D-Wave 2025: **disputed.** [F27] (Science 2026) and [F28] reproduce much of it; D-Wave's counter-argument is [F29]; unresolved at the largest sizes.
    - Google OTOC 2025: **stands so far** ([F31], [F32]; no published refutation found).
14. **Fault tolerance:** no for the demonstrations; yes for scalable versions ([F35]).
15. **Resources:** 65–127 superconducting qubits; thousands of annealer qubits (D-Wave).
16. **Protein mapping:** weak.
    - Proteins at structure-prediction level are *not* quantum many-body spin dynamics. The Cα-trace energy in S29–S33 is classical.
    - The only geometry-adjacent use is [F34]: NMR OTOCs of small molecules, which is self-declared not beyond classical.
    - Possible niche: interpreting many-body nuclear-spin data (dipolar-coupled ¹H networks) for structural constraints.
    - Standard protein NMR structure determination uses NOE/relaxation-matrix treatments that are classically cheap. **U** (not verified): no literature found showing protein NOE analysis is limited by classical spin-dynamics cost.

### P3 — Fault-tolerant Hamiltonian simulation + QPE (electronic structure)
1. **What the QC does:** it block-encodes the molecular H (qubitisation with THC or double factorisation, [F45], [F59]–[F61]), runs QPE and samples eigenenergies. Or it runs time evolution ([F41]–[F44], [F48]).
2. **What it replaces:** FCI / DMRG / CCSD(T) / AFQMC for strongly correlated active spaces.
3. **Why it is hard classically:** exact diagonalisation is exponential. Approximate methods can fail for strong multireference character (metal clusters).
4. **Exact speedup:** qubitization needs O(λt + log(1/ε)) queries ([F45]). Energy estimation to ε costs O(λ/ε) block-encoding calls, each Õ(N) Toffolis with THC ([F61]). The comparator speedup is exponential over *exact* diagonalisation. Against the best heuristics, **no generic exponential advantage has been evidenced** ([F64]).
5. **Type:** time (gate count), given an initial state of good overlap.
6. **Assumptions:** fault tolerance; an initial state with non-negligible overlap with the ground state (the central caveat of [F64]); a fixed active space and basis.
7. **Oracle:** a block encoding of H (PREPARE/SELECT).
8. **Oracle cost:** Õ(N) Toffoli per call with THC ([F61]).
9. **State preparation:** the crux ([F64]). Overlap can vanish exponentially with system size, so preparation may itself need classical heuristics.
10. **Readout:** QPE gives one energy sample per run. Properties need additional estimation rounds.
11. **Postprocessing:** light.
12. **Strongest classical:** DMRG + NEVPT2 / CCSD(T) / AFQMC. The canonical FeMoco model was classically solved to chemical accuracy in 2026 ([F65], preprint). For proteins, ML potentials give QM-quality energies at scale ([F73], [F74]).
13. **Survives?** Polynomial or constant-factor advantage is plausible for select strongly correlated clusters ([F62]: CYP "has the potential to be a quantum advantage problem"). Generic exponential advantage: not evidenced ([F64]). The flagship FeMoco target is eroding ([F63], [F65]).
14. **Fault tolerance:** **yes.**
15. **Resources:**
    - FeMoco: ~10^15 T gates, 111–2024 logical qubits, 110 h to 130 days ([F58]).
    - FeMoco with THC: ~4 million physical qubits, under 4 days ([F61]).
    - CYP Cpd I: ~4.6 million physical qubits, 73 h, ~1426 logical qubits ([F62]).
16. **Protein mapping:** *metal-site chemistry* such as enzyme mechanism, spin-state energetics or cofactor electronic structure. **Not** backbone structure accuracy.
    - For a structure-accuracy endpoint, the energy function would need to be the bottleneck. S29–S33 measured that it is not: AMBER in-band ρ = 0.000, and physics as a mover is indistinguishable from a random direction (Map AA-3, DE-7).
    - Where QM accuracy does matter for proteins, it is overwhelmingly weakly correlated chemistry, reachable by DFT or ML potentials ([F73], [F74]).

### P4 — QSVT / quantum linear algebra (HHL) and dequantization
1. **What the QC does:** it applies a polynomial f(A) to a block-encoded A, e.g. A⁻¹|b⟩ ([F46], [F50]).
2. **What it replaces:** dense or sparse linear algebra such as solves, PCA and regression.
3. **Why it is hard classically:** poly(N) cost versus the claimed polylog(N).
4. **Exact speedup:** HHL is poly(log N, κ) ([F50]) against poly(N) classically. With ℓ²-sampling access, classical methods are poly(k, κ, 1/ε) and independent of dimension ([F52]–[F54]), so the exponential gap collapses to polynomial for low rank.
5. **Type:** query/time under the access model.
6. **Assumptions:** QRAM or efficient state preparation, sparsity or low rank, bounded κ, and an output that is a state ([F51]).
7. **Oracle:** block encoding or QRAM.
8. **Oracle cost:** active QRAM erases most asymptotic advantage ([F56]).
9. **State preparation:** it dominates ([F51], [F53]).
10. **Readout:** extracting x classically costs Ω(N) samples; only sampled properties are cheap.
11. **Postprocessing:** n/a.
12. **Strongest classical:** quantum-inspired sampling algorithms ([F52], [F54]); constant-precision QSVT dequantized ([F55]).
13. **Survives?** Only for high-precision, sparse, full-rank, well-conditioned problems with implicitly defined inputs ([F55]). Not for data-loaded problems.
14. **Fault tolerance:** yes.
15. **Resources:** problem-dependent; none relevant here.
16. **Protein mapping:** readout QPs and hull projections (Map AA-4, S-6). These are D ≤ 500 and solve in milliseconds classically. **Dead.**

### P5 — QITE (NISQ imaginary time / thermal states)
1. **What the QC does:** it approximates e^{−βH}|ψ⟩ by local unitaries fitted each step from measurements ([F49]).
2. **What it replaces:** classical imaginary-time projection or thermal-state preparation.
3. **Why it is hard classically:** exponential state space for quantum H.
4. **Exact speedup:** "exponentially less space and time per iteration" ([F49]), assuming a finite correlation length. The unitary domain grows with correlation length, and the cost is exponential in the domain size.
5. **Type:** memory and time per step.
6. **Assumptions:** bounded correlation length, and tomography of local reduced density matrices.
7. **Oracle:** none.
8. **Oracle cost:** n/a.
9. **State preparation:** simple.
10. **Readout:** many local measurements per step; shot noise enters the linear solve.
11. **Postprocessing:** a classical linear system per step.
12. **Strongest classical:** for classical (diagonal) energies such as the protein Cα-trace energy, e^{−βH} is just Boltzmann weighting. Sampling it is classical MCMC, and there is nothing "quantum" to evolve.
13. **Survives?** For a diagonal Hamiltonian, QITE reduces to classical reweighting (compare S33 R9, R12).
14. **Fault tolerance:** no (NISQ), but noise is limiting.
15. **Resources:** small demonstrations only.
16. **Protein mapping:** only through a quantum H. The inherited energies are diagonal, so QITE on them is classically reproducible (H-001). **Dead** for this program.

### P6 — Quantum generative models as structure priors / samplers
1. **What the QC does:** it prepares |ψ(θ)⟩ and samples x ~ |⟨x|ψ(θ)⟩|² (QCBM/IQP/spectral Born machine), or samples a transverse-field Gibbs state (QBM) ([F75]–[F79], [F89], [F92]).
2. **What it replaces:** classical generative models (diffusion, flows, autoregressive, EBMs + MCMC) and MCMC on a known energy.
3. **Why it is hard classically:** it is hard only for *sampling from the model's own distribution* (IQP/RCS-type hardness, [F77], [F89]). Expressivity separations exist only against restricted classical classes ([F78]: Bayesian networks) or cryptographic distributions ([F79]).
4. **Exact speedup:** none for any natural data distribution.
   - Proven: an unconditional *expressivity* separation vs Bayesian networks ([F78]); DDH-conditional *learnability* separation on contrived distributions ([F79]).
   - Empirical: data-limited-regime wins on 20-variable tasks ([F87]), which is classically simulable.
5. **Type:** expressivity / sample complexity. Not runtime on real data.
6. **Assumptions:** trainability, which conflicts with hardness. Anticoncentrating (hard-to-sample) models are *not trainable on average* ([F91]). Explicit losses create barren plateaus ([F86]). Classical training of IQP models is possible, but the trained model then has a classical surrogate in many regimes ([F88]–[F90]).
7. **Oracle:** none. For the Boltzmann-sampling use, it needs the classical energy E(x) loaded as a Hamiltonian (diagonal).
8. **Oracle cost:** coherent evaluation of a learned pair-distance energy over a continuous-coordinate discretisation is O(L²) arithmetic per evaluation, in reversible fault-tolerant arithmetic (not quantified in this domain's literature).
9. **State preparation:** training cost, ([F86], [F91]).
10. **Readout:** one sample per shot. MMD/KL estimation from samples needs many shots, and output probabilities are unavailable for hard models (so no likelihoods).
11. **Postprocessing:** decoding bitstrings to coordinates.
12. **Strongest classical:**
    - Modern deep generative models (not the weak baselines used in [F87], [F89]).
    - MCMC / PT / SMC for a known energy.
    - Classical surrogates of the QCBM itself ([F90]).
    - In S29–S33: Metropolis came closer than the tempered Born machine to the exact Gibbs mean on 9/10 targets (Q-C19), and random prior sampling beat trained circuits.
13. **Survives?** **No evidence it survives** against strong classical baselines on any natural dataset ([F81]: classical models "outperform the quantum classifiers"). The 16-qubit KRAS result ([F93]) is classically simulable by construction.
14. **Fault tolerance:** it depends. Classical-training / quantum-deployment schemes are NISQ-ish. For Boltzmann sampling with a guarantee you need quantum-walk MCMC, which is a different primitive (fault tolerant, P8).
15. **Resources:** 16 qubits ([F93]); 20 ([F87]); simulated up to 1000 ([F89]) and 190 ([F92]).
16. **Protein mapping:** "a prior over structures" or "a sampler of the learned-energy posterior".
    - **Key structural mismatch:** the program's target distribution (Map SP-1) is a *specified* classical Gibbs/posterior law π(x) ∝ exp(−E(x)/T), with E a classical learned energy. A Born machine's hardness is the hardness of sampling *its own* |ψ|². It confers no advantage in sampling a *given* π unless (a) the circuit provably prepares π faster than classical mixing does, which is quantum-walk/QMCMC territory, not generative modelling, or (b) π itself were quantum-hard, which a classical energy with a fast classical evaluator does not suggest.
    - As a *learned prior from data* (PDB), the data-processing inequality applies (Map DE-6). The inductive bias of a small QCBM is classically simulable and has no demonstrated edge over protein-scale classical models (ESM-type priors were the predecessor's top lever).

### P7 — Variational QML / PQC trainability ↔ simulability
1. **What the QC does:** it evaluates a loss via ⟨O⟩ on U(θ)|x⟩ and trains θ.
2. **What it replaces:** classical ML models.
3. **Why it is hard classically:** only when the circuit is hard to simulate.
4. **Exact speedup:** none known for natural tasks.
5. **Type:** —
6. **Assumptions:** the absence of barren plateaus ([F38]) and traps ([F39]).
7. **Oracle:** data encoding.
8. **Oracle cost:** data loading ([F51], [F56]).
9. **State preparation:** encoding circuits.
10. **Readout:** O(1/ε²) shots per gradient component, and exponentially small gradients in BP regimes.
11. **Postprocessing:** a classical optimiser.
12. **Strongest classical:**
    - Classical surrogates when BPs are absent ([F37]).
    - Pauli propagation for scrambling circuits ([F36]); QCNN simulation ([F40]); random Fourier features ([F84]).
    - Classical ML with data ([F82], [F83]).
13. **Survives?** Generally no. The trainability ⇒ simulability tension is the central negative result ([F37], [F40], [F91]).
14. **Fault tolerance:** no, but noise ⇒ classical simulability ([F35]).
15. **Resources:** —
16. **Protein mapping:** VQE/CVaR/QAOA over protein registers. This was already tested in S29–S33, 33+ contrasts, **null**, and the literature predicts that outcome (P7 = DE-1/DE-9).

### P8 — Cross-cutting: the fault-tolerant cost of quadratic speedups
1. **What the QC does:** it runs quantum walks, amplitude amplification or QSA to get quadratic speedups in 1/δ, restarts or queries.
2. **What it replaces:** MCMC, SA, restarts, search.
3. **Why it is hard classically:** slow mixing and many restarts.
4. **Exact speedup:** quadratic, in queries or steps.
5. **Type:** query/steps.
6. **Assumptions:** coherent energy oracles on a surface code.
7. **Oracle:** a reversible energy evaluation.
8. **Oracle cost:** it dominates. It is why [F67] finds a day and a million physical qubits for what classical SA does in 4 CPU-minutes.
9. **State preparation:** coherent encoding (sampling-to-state) of the initial distribution.
10. **Readout:** —
11. **Postprocessing:** —
12. **Strongest classical:** optimised SA/PT on CPUs and GPUs.
13. **Survives?** Not on early fault-tolerant hardware ([F66], [F67]). Quartic speedups are "significantly more practical" ([F66]). Super-quadratic speedups and small data are required ([F57]).
14. **Fault tolerance:** yes.
15. **Resources:** ~10^6 physical qubits for small instances ([F67]).
16. **Protein mapping:** this constrains the Map's **AA-1** (QMCMC/quantum walks for mixing) and **AA-2**. A quadratic gap speedup pays off only if the *measured* classical mixing time is very long (well beyond hours of CPU time at the relevant lengths) and the coherent energy oracle is cheap.

---

## 4. Strongest classical counterarguments (with citations)

1. **Tensor networks and Pauli propagation keep catching up with "beyond-classical" claims, usually within weeks to months.**
   - Sycamore 2019 → [F4], [F5], [F7].
   - IBM 2023 → [F19]–[F21], [F23]–[F25].
   - D-Wave 2025 → [F27], [F28] (disputed by [F29]).
   - GBS → [F15]–[F17].
   - Only the 67-qubit RCS ([F9]) and the OTOC(2) echoes ([F30]) stand today. Neither computes anything with a scientific application. [F34], the one structural application, is self-declared "not yet beyond classical".
2. **Noise ⇒ classical simulability.** For constant noise and no error correction:
   - noisy RCS is classically samplable in poly time asymptotically ([F10]);
   - expectation values are classically computable on average ([F35]);
   - "efficient error mitigation ⇒ classical simulability on most inputs" ([F35]).
   Any NISQ protein proposal inherits this.
3. **Trainable ⇒ (often) simulable.**
   - The structures that avoid barren plateaus confine dynamics to small classically simulable subspaces ([F37], [F40], [F36]).
   - Shallow models are "swamped with traps" ([F39]).
   - Hard-to-sample (anticoncentrating) generative models are untrainable on average ([F91]).
   - Classically trainable IQP models ([F89]) meet surrogate and deployment-discrepancy limits ([F90]).
4. **Dequantization.**
   - Exponential QML speedups relying on QRAM-style access collapse to polynomial for low-rank data ([F52]–[F54]).
   - Constant-precision QSVT is dequantized ([F55]).
   - Active QRAM erases most asymptotic advantage ([F56]).
   - The caveats checklist is [F51].
5. **Chemistry.**
   - No evidence of generic exponential advantage for ground-state energies ([F64]); the state-preparation overlap is the crux.
   - The flagship FeMoco benchmark was criticised as unrepresentative ([F63]) and is now classically solved to chemical accuracy in a model (preprint [F65]).
   - Resource estimates remain ~4–5 million physical qubits and days ([F61], [F62]).
   - For proteins, ML potentials reach ab-initio quality at more than 25k atoms ([F73], [F74]).
6. **Quadratic speedups do not pay on early fault-tolerant hardware** ([F66], [F67]; QSA: 1 day and 10^6 qubits vs 4 CPU-min).
7. **Benchmarking hygiene.** Classical out-of-the-box models beat quantum classifiers ([F81]). Wins against weak baselines ([F87], [F89], [F93]) are not general advantage (LIT_RULES).

---

## 5. Scaling statements (explicit, from the literature only)

| Primitive | Scaling statement | Source |
|---|---|---|
| Hamiltonian simulation (qubitization) | O(t + log(1/ε)) queries (t in units of the block-encoding normalisation), optimal | [F45] |
| Taylor-series simulation | cost logarithmic in 1/ε | [F43] |
| Chemistry QPE (THC) | Õ(N) Toffoli per block encoding × O(λ/ε) repetitions; N = orbitals, λ = 1-norm | [F61] |
| Exact electron dynamics (first quantised) | exponentially less space and polynomially fewer operations in basis-set size than mean field | [F68] |
| HHL | poly(log N, κ), with state-in/state-out caveats | [F50], [F51] |
| Quantum-inspired classical | time independent of dimension, poly in rank, κ and 1/ε (ℓ²-sampling access) | [F54] |
| Noisy RCS (classical) | poly time for constant noise and anticoncentration | [F10] |
| Noisy circuits (classical) | poly time expectation values (average input); quasi-poly sampling | [F35] |
| Barren plateaus | gradient concentration exponential in qubit number | [F38] |
| Traps | superpolynomially small fraction of good local minima | [F39] |
| Quadratic FT speedups | not advantageous on early FT; quartic "significantly more practical" | [F66] |
| QSA vs SA (spin glasses) | about 1 day at 10^6 physical qubits vs about 4 CPU-min | [F67] |
| MPS vs D-Wave quench | stretched-exponential effort for MPS (claimed); t-VMC polynomial up to 128 spins | [F26], [F28] |

**No paper in this domain gives any scaling in protein residues, degrees of freedom, temperature or mixing time for a protein-structure task.** The closest are [F92], an RNA sequence distribution at 93 nt with no residue scaling, and [F93], small molecules. Mixing-time scaling for protein-posterior sampling is outside this domain's literature (Map C-1/OP-01 remains unmeasured).

---

## 6. NISQ vs fault-tolerant routes

- **NISQ route:**
  - Evidence: every NISQ advantage claim with a computational task of any application value (IBM utility, D-Wave dynamics) has been classically reproduced or is contested.
  - Theory predicts this for constant noise ([F10], [F35]).
  - For QML, the trainability/simulability dichotomy ([F37], [F91]) removes the remaining NISQ angle for generative priors.
  - The surviving NISQ claims (RCS, OTOC(2)) are for tasks with no protein mapping.
  - **Verdict: no credible NISQ route for protein structure.**
- **Fault-tolerant route:**
  - Real, rigorous primitives exist: qubitization/QSVT and QPE, quantum walks.
  - The only domain with a mature cost story is electronic structure, at ~10^6 physical qubits and days per energy ([F61], [F62]).
  - Speedups there are not generically exponential ([F64]).
  - Quadratic-speedup primitives (the only type relevant to sampling/search in the Map) need super-quadratic or very long classical runtimes to pay off ([F66], [F67]).
  - **Verdict: FT is the only possible route, conditional on measured classical hardness. It is years away at the needed scale.**

---

## 7. Protein mapping and S29–S33 connection

- **P6 generative priors and samplers.**
  - Already tested in S29–S33: the tempered Born machine and the MPS Born machine were classically simulable. Metropolis beat the Born machine on the Gibbs mean on 9/10 targets (Q-C19), and random prior sampling beat trained circuits (Q-C13).
  - The literature fully explains this:
    - (i) a Born machine trained to a free-energy objective is at best a Gibbs sampler that MCMC also targets (S33 R9 is consistent with the general "trainable ⇒ surrogate" results [F37], [F90], [F91]);
    - (ii) at simulable sizes (χ ≤ 16 MPS, ≤ 22 qubits) there is by construction no computational advantage (as in [F93] at 16 qubits);
    - (iii) the positive signal (soft Boltzmann readout, 1.40× MDE) concerns sampling a **specified classical posterior**, which RCS/IQP-style hardness does not address (§3 P6.16).
  - **What would be different:** only a primitive that *provably accelerates convergence to a given π*, i.e. quantum walks/QMCMC (other domain), *and* a measured classical mixing time large enough to beat the [F66]/[F67] overhead. That is the Map's AA-1 with an explicit extra bar from P8.
- **P3 electronic structure as a structure-accuracy lever.**
  - Not tested directly. S29–S33 showed that physics energy accuracy is not the bottleneck (AMBER in-band ρ 0.000; DE-7).
  - The literature adds that proteins' structure-relevant energetics are weakly correlated and reachable by classical ML potentials ([F73], [F74]). Quantum advantage in chemistry is, at best, polynomial and localised to strongly correlated metal centres ([F62], [F64]); even the flagship FeMoco model is now classically solved ([F65]).
  - Mapping: it would matter only for metalloprotein active-site *chemistry*, not Cα-trace RMSD.
- **P4 QSVT/HHL.** Map AA-4 is confirmed dead: tiny classical problems, and dequantization covers low-rank cases.
- **P7 variational.** Identical to DE-1 and DE-9. The literature (traps, BPs, simulability, [F81] benchmarking) predicted the S29–S33 null.
- **P2 NISQ dynamics.** No mapping to the learned-energy pipeline. The [F34] NMR-geometry work is a structurally adjacent curiosity: small molecules, not beyond classical.
- **H-001 relevance.** Several literature results are general forms of H-001:
  - [F35]: efficient mitigation ⇒ classical simulation;
  - [F37]: BP-free ⇒ classical surrogate;
  - [F90], [F91]: trainable generative ⇒ surrogate sampling;
  - [F52]–[F55]: dequantization of access-model speedups.
  Together they support upgrading H-001 from a project-specific observation to an instance of a known pattern. The theory write-up (Map rank 1) should cite these.

---

## 8. Literature gaps (novelty ≠ advantage)

1. There is **no** published quantum generative model for protein *structures* (coordinates or torsions) that I could find. The nearest are small-molecule QCBM priors ([F93]) and an RNA *sequence* distribution ([F92]). Filling this gap would be novel but **not** evidence of advantage: at trainable sizes, the preceding sections predict classical surrogates.
2. No paper compares a quantum sampler against **strong** classical samplers (PT/SMC/HMC or modern diffusion) on a *specified* biomolecular Boltzmann law with measured mixing times. This is the actual open question for Map SP-1/AA-1. It is classical-first.
3. No resource estimate exists for a coherent **learned pair-distance energy oracle** (O(L²) terms, continuous coordinates) as needed by quantum walks. Without it, AA-1 cannot be costed against [F67]-style overheads.
4. No evidence that any *protein-structure* decision is limited by electronic-structure accuracy in a strongly correlated regime. The chemistry-advantage literature targets energies and mechanisms, not folds.
5. The OTOC/NMR route ([F34]) is new. No study shows that protein NMR structure determination is limited by classical spin-dynamics simulation cost.

---

## 9. Unverified leads (not cited as evidence)

- Pan & Zhang, "Simulation of quantum circuits using the big-batch tensor network method", believed to be PRL 128, 030501 (2022). This may be the published form of [F3]. Not verified.
- The arXiv id for Madsen et al. 2022 (Borealis). The DOI was verified; the arXiv id was not.
- Journal publication of Bowles, Ahmed, Schuld ([F81]) and of Mauron & Carleo ([F28]): none on arXiv as checked; there may be later versions.
- The correct DOI of Rudolph et al. "Trainability barriers…" ([F86]); the arXiv API returned the DOI of a different paper.
- Classical responses to [F30] (OTOC echoes) beyond [F31]/[F32]. None found, but the search was not exhaustive after April 2026.
- Precise Willow RCS figures (5 min vs 10^25 years): press/blog only; no peer-reviewed paper located in this session.
- Montanaro, "Quantum speedup of Monte Carlo methods" and Szegedy/quantum-walk MCMC papers: out of this domain's scope (see the MCMC domain). Not verified here.

---

## 10. Bottom-line verdicts per primitive

- **P1 — RCS/GBS hard-distribution sampling: KILLED (for protein work).**
  - One claim survives today (67-qubit RCS, [F9]). Every other instance was classically reproduced ([F4]–[F7], [F15]–[F17]).
  - Asymptotically, constant-noise RCS is classically samplable ([F10]).
  - Even if it survives, the distributions are structureless and hardness is a property of the device, not of any protein posterior.
- **P2 — NISQ many-body expectation values (utility / annealing / OTOC): KILLED for structure prediction; WEAK as a curiosity via NMR.**
  - IBM utility fell to laptop-scale Pauli and tensor-network methods ([F20], [F21], [F23]). D-Wave's claim is contested in Science ([F27]) and by t-VMC ([F28]). Google's OTOC(2) stands ([F30], [F31]) but has no protein mapping.
  - [F34] ties OTOCs to molecular geometry, but only for small molecules and explicitly not beyond classical.
  - Constant noise implies classical simulability of mitigated circuits ([F35]).
- **P3 — FT Hamiltonian simulation + QPE (electronic structure): KILLED as a structure-accuracy lever; INTERESTING only for metalloprotein active-site chemistry.**
  - The algorithms are rigorous and resource-costed (~4–5 M physical qubits and days: [F61], [F62]).
  - Generic exponential advantage is not evidenced ([F64]), and the FeMoco flagship is now classically solved in a model ([F65]).
  - S29–S33 showed that energy accuracy is not the endpoint bottleneck, and protein-relevant QM is largely weakly correlated and ML-potential accessible ([F73], [F74]).
  - It remains a legitimate long-horizon tool for strongly correlated cofactors (CYP, [F62]), a different scientific question from backbone RMSD.
- **P4 — QSVT/HHL quantum linear algebra: KILLED.**
  - Map problem sizes are tiny and solve in milliseconds classically.
  - Dequantization ([F52]–[F55]) and QRAM costs ([F56]) remove access-model exponential gaps.
  - The caveats of [F51] all apply.
  - QSVT survives only as the *language* in which any FT protocol (e.g. quantum walks) would be written.
- **P5 — QITE: KILLED.**
  - For the program's diagonal classical energies, imaginary-time evolution is classical Boltzmann reweighting (H-001, S33 R9/R12).
  - For quantum H, the finite-correlation-length and tomography costs ([F49]) keep it a small-system NISQ heuristic.
- **P6 — Quantum generative models (QCBM/QBM/IQP/spectral Born machines) as structure priors or samplers: KILLED as a prior; WEAK as a sampler.**
  - As a prior learned from data, the data-processing inequality applies, and simulable sizes give no computational edge ([F93] at 16 qubits).
  - Classical benchmarks win ([F81]). Hard-to-sample models are untrainable on average ([F91]), and trainable ones admit surrogates ([F88]–[F90]).
  - As a sampler of a specified classical posterior (the only S29–S33 signal), Born-rule hardness is irrelevant. The right primitive is quantum-walk MCMC, not generative modelling.
  - S29–S33 already observed the predicted failure (Q-C13, Q-C19, R9).
  - Only [F92]-type scalable, classically trained models remain as open *engineering* novelty, and novelty is not advantage.
- **P7 — Variational QML / PQC trainability: KILLED.**
  - The literature's trainability ⇒ simulability results ([F37], [F39], [F40], [F36]) and benchmark results ([F81]) match the 33-contrast null of S29–S33.
  - Do not revisit (DNR-01, 02, 09).
- **P8 — The quadratic-speedup overhead constraint: HIGH PRIORITY as a constraint, not as an opportunity.**
  - This is the most decision-relevant finding for the program's top-ranked quantum candidate (Map AA-1, QMCMC/quantum walks).
  - [F66] and [F67] show that quadratic speedups do not pay on early FT hardware (QSA: one day and 10^6 qubits vs 4 CPU-minutes).
  - The C-1 kill test should therefore include an explicit break-even criterion. The measured classical mixing cost at the relevant lengths must exceed the FT overhead of a coherent learned-energy oracle, which is a resource estimate the literature does not yet contain (§8.3). Otherwise AA-1 should be downgraded even if classical mixing is slow.
