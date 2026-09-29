# Discovery lens: optimization / search with genuine structure (2026-09-28)

Status: COMPLETE (2026-09-28). Candidates, kills and full query log at end of file. WebSearch budget exhausted (200/200). Searches via arXiv export API / arXiv abs pages / OpenAlex / Crossref, fetched with local urllib (python) and WebFetch.

Hard filter (protein lessons): no argmin/sampling over a classical energy with only Grover/QAE/walk speedup; need beyond-quadratic mechanism with a practical instance, or a quantum-native objective where the inner evaluation is itself classically hard and solver error dominates model error.

## Planned threads
1. DQI / OPI / max-LINSAT: follow-ups, classical attacks, any physical/engineering instance.
2. Quantum annealer as native simulator of physical spin glasses (King et al. claims, TN/NQS challenges); distinct material subsections.
3. Hamiltonian-structured optimization: quantum optimal control of molecules; pulse design with quantum-evaluated objectives.
4. Local minima of quantum Hamiltonians under thermal perturbation (Chen-Huang-Preskill-Zhou) as a quantum-native optimization objective.
5. Combinatorial materials problems with correlated energies.
6. Super-quadratic claims: backtracking/B&B, Kikuchi planted inference, QHD, LABS, QAOA dequantization.

## Query log
See "Query log (final)" at end of file.

## Checkpoint 1 (raw findings, all IDs verified via arXiv export API abstracts or arXiv abs pages or OpenAlex records on 2026-09-28)

### DQI / OPI / max-LINSAT (arXiv API query: abs:"decoded quantum interferometry", sorted by date, 40 results)
- Jordan et al. arXiv:2408.08292 [VERIFIED] (Nature 2025): DQI; OPI superpolynomial candidate; sparse max-XORSAT advantage vs SA on some instances.
- Khattar, Shutty, Gidney, Zalcman et al. arXiv:2510.10967 [VERIFIED]: OPI over GF(2^b); instances needing >1e23 classical trials solved with ~5.72e6 Toffoli; "verifiable quantum advantage".
- Gu & Jordan arXiv:2510.06603 [VERIFIED]: Hermitian-code HOPI extends regime.
- Challenges: Anschuetz, Gamarnik, Lu arXiv:2509.14509 [VERIFIED] (OGP obstructs DQI on random sparse instances; AMP beats DQI on some distributions); Parekh arXiv:2509.19966 [VERIFIED title] (no advantage for MaxCut); Gil-Fuster et al. arXiv:2607.28120 [VERIFIED] (MCMC block-Gibbs emulates DQI output quality; OPI in claimed-advantage regime runtime ~1.1^n); Sun & Wootters arXiv:2604.09533 [VERIFIED] (semicircle law not optimal worst case, existential only); Kramer, Schubert, Eisert arXiv:2606.13570 [VERIFIED] (bounded-degree max-LINSAT: advantage confined to constant prefactor); Marwaha et al. arXiv:2509.14443 [VERIFIED title].
- Applications: only Sabater et al. arXiv:2509.08328 [VERIFIED] (automotive option-package pricing ILP -> max-XORSAT, BP decoder, compared to Gurobi) = generic industrial ILP (excluded category). Hamiltonian DQI (Schmidhuber et al. arXiv:2510.07913 [VERIFIED]): Gibbs sampling via decoding; efficient for toric/Haah code at all T but with matching classical algorithm; non-commuting semiclassical spin glass only up to constant beta threshold.
- Scoped finding: in the 33 DQI-titled/abstracted arXiv records through 2026-09-25, no instance family with a physical/measurable observable (a material, a device measurement) was found; OPI is polynomial regression over finite fields (Reed-Solomon dual). => DQI killed for this program's "measurable physical output" requirement, while remaining the strongest verifiable-optimization advantage candidate in the abstract.

### Annealer as native simulator (arXiv API query: annealer AND (spin glass|frustrated magnet|spin ice) AND dynamics AND (material|experiment|neutron))
- King et al. arXiv:2403.00910 [VERIFIED] (Science 2025) beyond-classical quench dynamics; challenged by Tindall et al. arXiv:2503.05693 [VERIFIED], Mauron & Carleo arXiv:2503.08247 [cited in sibling notes VERIFIED], King et al. comment arXiv:2504.06283 [VERIFIED], and now Wiersema arXiv:2609.01719 [VERIFIED] (t-VMC reaches QPU two-spin correlation errors for 2D cylinder, 3D dimer, diamond, biclique at 7 and 20 ns). => Category E.
- Material-specific annealer simulations: Ca3Co2O6 out-of-equilibrium magnetization (King et al. arXiv:2101.02769 [VERIFIED]); Shastry-Sutherland Ising (Kairys et al. arXiv:2003.01019 [VERIFIED title]); scaling advantage vs PIMC relaxation (King et al. arXiv:1911.03446 [VERIFIED], PIMC is not a dynamics method -> weak comparator = D); programmable dipolar spin ice coherent monopole transport (Giergiel & Surowka arXiv:2603.28125 [VERIFIED], no classical dynamics comparator stated in abstract = D); long-range competing interactions (Koziol & Schmidt arXiv:2511.08336 [VERIFIED title]).

### Local minima of quantum Hamiltonians under thermal perturbations
- Chen, Huang, Preskill, Zhou arXiv:2309.16596 [VERIFIED] (Nature Physics 2025 doi:10.1038/s41567-025-02781-4 [VERIFIED OpenAlex W4407675334]; STOC 2024 doi:10.1145/3618260.3649675): quantum thermal gradient descent finds local minima efficiently; classically hard (BQP-hard) for a family of 2D Hamiltonians where all local minima are global.
- OpenAlex cited-by (36 works, W4407675334|W4399521417|W4387225835): theory, Gibbs samplers (Efficient quantum thermal simulation, Nature 2025 doi:10.1038/s41586-025-09583-x), dissipative prep; "Dissipative continuation for ground-state preparation at chemical transition states" (2026, doi:10.1103/8s88-x43b); no work applies local-minimum finding to a measured protocol-dependent metastable state of a material.

### Hamiltonian-structured optimization (molecular control)
- Magann et al. "Digital quantum simulation of molecular dynamics and control" PRR 3, 023165 (2021) doi:10.1103/physrevresearch.3.023165 [VERIFIED OpenAlex W3006710752]; follow-up "Digital quantum simulation of controlled molecular dynamics in first quantization" (2024, OSTI doi:10.2172/2540419 [VERIFIED OpenAlex]).
- Castaldo et al. "Quantum optimal control with quantum computers: a hybrid algorithm featuring machine learning optimization" PRA 103, 022613 (2021) doi:10.1103/physreva.103.022613 [VERIFIED OpenAlex].
- de Keijzer et al. arXiv:2202.08908 [VERIFIED via arXiv search listing] pulse-based variational (hardware control, not molecular control).

### Super-quadratic / structured-optimization claims
- Schmidhuber, O'Donnell, Kothari, Babbush arXiv:2406.19378 [VERIFIED] (PRX 15, 021077 (2025)): nearly quartic speedup, planted noisy kXOR via Kikuchi; relevance stated is cryptographic.
- Shaydulin et al. arXiv:2308.02342 [VERIFIED] (Sci. Adv. 2024) QAOA+QMF LABS scaling vs branch-and-bound; classical counter-pressure: Zhang, Shen, Kumar, Pistoia arXiv:2504.00987 [VERIFIED via arXiv listing] (GPU memetic tabu to N=120); Ikeuchi, Matsuda, Tanaka arXiv:2510.24237 [VERIFIED via listing].
- Leng, Hickman, Li, Wu arXiv:2303.01471 [VERIFIED] QHD: empirical advantage on nonconvex QP up to 75 dims on D-Wave.

## Checkpoint 2 (additional verified findings)
- QHD: arXiv listing "quantum hamiltonian descent" (13 results). Chakrabarti et al. arXiv:2503.24332 [VERIFIED via listing]: with exact oracles QHD gives no speedup over classical zeroth-order methods for convex problems; super-quadratic query advantage only under noisy evaluations. Leng et al. arXiv:2504.14841 [VERIFIED abs]: provable (sub)exponential speedups, but on objective functions built by perturbative reductions from the Gilyen-Hastings-Vazirani oracle separation (no practical instance). Leng et al. arXiv:2311.00811 [VERIFIED via listing]: separation on a constructed family with 2^d local minima. Applications: power-to-hydrogen NLP (arXiv:2508.02969), community detection (arXiv:2411.14696) [both VERIFIED via listing] = generic engineering/graph problems on classical landscapes.
- QeMCMC: Layden et al. arXiv:2203.12497 [VERIFIED via listing]; Orfi & Sels arXiv:2403.03087 and arXiv:2408.07881 [VERIFIED via listing] bound/refute generic speedup (none for unital proposals on worst-case unstructured problems; needs fine-tuned quenches); Marshall, Egger et al. arXiv:2602.06171 [VERIFIED via listing] MIS scaling to 117 qubits (classical landscape). => E.
- Rydberg MIS: Ebadi et al. arXiv:2202.09372 [VERIFIED via listing]; Andrist, Schuetz et al. arXiv:2307.09442 [VERIFIED via listing]: classical solvers solve UDG instances with thousands of nodes in minutes. => E.
- Backtracking: Montanaro arXiv:1509.02374 [VERIFIED abs]: O(sqrt(T) n^{3/2} log n), quadratic. Babbush et al. arXiv:2011.04149 [VERIFIED in sibling notes]: quadratic speedups do not survive early-FT overhead.
- Cluster expansion + quantum: only Ichikawa et al. arXiv:2503.09356 [VERIFIED via listing] (QAOA configurational search on a CE of Au-Cu fitted to DFT) = quantum search over a classical landscape (protein lesson 3). No work found where CE training energies come from a quantum computer (arXiv abstract search "cluster expansion" "quantum computer" alloy: 1 hit).
- Annealer hysteresis: Pelofske, Barrows, Sathe, Nisoli arXiv:2506.17418 [VERIFIED via listing] (hysteresis loops on D-Wave, stoquastic Ising).
- Optical joint detection (quantum data, not computation): Rengaswamy, Seshadreesan, Guha, Pfister arXiv:2003.04356 [VERIFIED via listing] BPQM; Delaney et al. arXiv:2102.13052 [VERIFIED via listing] 3-bit code BPQM on trapped ions (optical states emulated in qubits); Piveteau & Renes arXiv:2109.08170 [VERIFIED via listing]; Mandal, Piveteau, Renes, Pfister arXiv:2609.05857 [VERIFIED API] BPQM for random LDPC, vanishing block error; Cui, Postlewaite, Saif, Fan, Guha arXiv:2310.05889 [VERIFIED abs] (Nat. Commun. 16, 3760 (2025)) linear-optics Green Machine demonstrates superadditive BPSK communication without qubits; Guha arXiv:1101.1550 [VERIFIED via listing].
- Classical oscillators: Babbush, Berry, Kothari, Somma, Wiebe arXiv:2303.13012 [VERIFIED abs] (PRX 13, 041041 (2023)): BQP-complete kinetic-energy estimation for 2^n oscillators. Schade, Simon, Wiebe, Keating, Boesch, Fichtner arXiv:2609.20721 [VERIFIED abs] (2026-09-17): dissipative non-Markovian (viscoacoustic/viscoelastic) extension, BQP-complete, quartic speedup for locally coupled 3D systems, Lieb-Robinson-type bound excludes exponential advantage for local topologies; abstract gives no numerical comparison with classical solvers. Luangsirapornchai et al. arXiv:2501.06100 [VERIFIED via listing]: circuits for 1D spring-mass.
- Perspective: Babbush, King, Boixo, Huggins, Khattar, Low et al. "Grand Challenge of Quantum Applications", PRX Quantum (2026) doi:10.1103/6r9l-lynr [VERIFIED Crossref]: finding concrete instances and linking them to use cases are the under-resourced stages.
- Serbyn, Avdoshkin, Diessel, Huse, PRX (2026) doi:10.1103/4zs8-7kf4 [VERIFIED Crossref]: ETH at thermal first-order transitions, coexisting eigenstate branches (physics relevant to C1).
- Watts, Sarkar, Collins, Nguyen, Quezada, Bremner, PRA (2026) doi:10.1103/8s88-x43b [VERIFIED Crossref, no abstract]: dissipative continuation for ground-state prep at chemical transition states.

## Candidates (ranked)

### C1. Protocol-dependent metastable states of disordered non-stoquastic quantum magnets via quantum thermal gradient descent (quantum local minima)
- Input: a quantum spin Hamiltonian with a disorder distribution (e.g. anisotropic-exchange triangular XXZ with bond randomness, YbMgGaO4/YbZnGaO4 family [material refs UNVERIFIED, from memory]), a cooling/field protocol (rate, field-cooled vs zero-field-cooled), and a bath model (local jump operators).
- Output: local observables (magnetization, nearest-neighbour correlators, static structure factor, remanent moment) of the state reached by thermal gradient descent; FC/ZFC splitting; memory/rejuvenation signatures.
- Mechanism: Chen-Huang-Preskill-Zhou thermal gradient descent (Lindbladian cooling with quasi-local jump operators, CKG-type construction). The objective is quantum-native: a local minimum of a quantum Hamiltonian under thermal perturbations. Hardness is BQP-hard in the worst case, which is not a Grover-type speedup. The quantum computer replaces classical open-system many-body simulation (MPO Lindblad, t-VMC/NQS trajectories, cluster mean field), which is the bottleneck for non-stoquastic 2D models.
- Classical SOTA: QMC for stoquastic TFIM-type models (and annealer hysteresis, 2506.17418); MPO/PEPO Lindblad and MPS quantum trajectories; t-VMC with NQS (2609.01719 reaches D-Wave-scale dynamics); classical spin kinetic MC on effective classical models; DMFT/cluster DMFT for coexistence/hysteresis in itinerant cases.
- Novelty: B. Scoped: the arXiv search "local minima" + "thermal gradient descent" returns only 2309.16596; the OpenAlex cited-by set (36 works) contains no material application; the arXiv search "metastable hysteresis quantum computer" returns only annealer hysteresis on stoquastic Ising (2506.17418).
- Main risk: (i) for physical Hamiltonians local minima may be classically easy (near-product metastable states), and the BQP-hard families are contrived; (ii) model floor: real freezing involves lattice, nuclear spins and a bath that idealized jump operators do not capture, and disorder distributions are poorly known; (iii) the local-minimum notion (fixed point of a class of thermal channels) may not map to laboratory timescales (seconds to hours).
- First test: small-n (<=24 spins) exact trajectories comparing thermal-gradient-descent fixed points with classical cluster/MPS methods. Decide whether any physical disorder model yields entangled, protocol-dependent minima that classical methods misassign.
- Rough resources: n = 100-400 spins, ~2n+O(log n) logical qubits, Lindbladian step cost ~ Hamiltonian simulation to time ~beta (my rough estimate is 1e8-1e10 T gates per protocol; UNVERIFIED, not from a paper).
- Verdict: plausible. It is the only candidate in this lens with a complexity-theoretic beyond-quadratic mechanism and a quantum-native objective.

### C2. Coherent joint detection (BPQM) of LDPC-coded photon-starved optical signals versus the best classical receivers
- Input: optical coherent-state BPSK codewords (block length n = 32-1024) after a pure-loss channel at mean photon number per pulse 0.01-1; code (LDPC/polar).
- Output: decoded message. Figures of merit: block error rate and bits per photon at fixed rate. Scaling variable: n.
- Mechanism: belief propagation with quantum messages (coherent processing of the received quantum states, then measurement). It is optimal on tree codes and gives vanishing block error on random LDPC codes (2609.05857). The classical ablation is any symbol-by-symbol measurement (Dolinar/Kennedy/homodyne) followed by the best classical soft decoder, which is limited by the Shannon capacity of the induced classical channel. The gap is information-theoretic (claim category: sampling/information plus hardware advantage), not a runtime speedup.
- Classical SOTA: Dolinar receiver + soft BP; linear-optics structured receivers (Green Machine, Hadamard codes), which already demonstrate superadditivity without qubits (Cui et al. 2310.05889).
- Novelty: C. Quantum methods exist and a 3-bit trapped-ion demo with emulated optical input has been run (2102.13052), but there is no benchmark of qubit BPQM at LDPC lengths against Green-Machine-class linear-optical receivers at matched loss.
- Main risk: optical-to-qubit transduction loss and mode mismatch erase the Holevo-Shannon gap; linear-optics receivers capture most of the practical gain; the gain exists only in the photon-starved regime; this is a "quantum data" advantage (the same class as learning from quantum experiments, already demonstrated), so novelty lies only in the LDPC/length subsection.
- Verdict: weak to plausible. The comparator is clean and the output measurable, but the advantage type is informational and dominated by hardware.

### C3. Wavefield energy estimation in 3D viscoacoustic/viscoelastic media (seismic/acoustic) via coupled-oscillator Hamiltonian simulation
- Input: discretized 3D heterogeneous medium (density, moduli, attenuation Q with memory variables), source, time t; N grid oscillators.
- Output: kinetic+potential energy in a spatial subregion at time t (e.g. coda energy envelopes, energy partition in a target volume) to additive error eps.
- Mechanism: the Babbush et al. (2303.13012) oscillator-to-Schrodinger mapping. Schade et al. (2609.20721) extend it to dissipative non-Markovian media, prove BQP-completeness, and give a quartic speedup for locally coupled 3D systems (Lieb-Robinson bounds rule out exponential). The speedup is beyond quadratic but polynomial.
- Classical SOTA: GPU spectral-element / finite-difference solvers (SPECFEM3D, Salvus [names UNVERIFIED, from memory]); radiative-transfer / diffusion approximations for coda energy.
- Novelty: C. The method and asymptotic analysis exist; the abstract has no numerical classical comparison or break-even.
- Main risk: readout is limited to a few regional energies at 1/eps cost, while seismograms require waveforms; classical radiative-transfer approximations already model coda energy; model floor: sub-wavelength Earth heterogeneity is unknown, so an exact simulation of an assumed medium may not beat the modeling error; break-even needs N >~ 1e15 grid points (my rough estimate compares ~1e12 Toffoli for eps ~ 1e-3 with 1e17 classical flop; UNVERIFIED).
- Verdict: weak.

### C4. Quantum-evaluated optimal control of polyatomic photochemistry (vibronic, many-mode)
- Input: vibronic Hamiltonian (2-4 electronic states, 20-100 modes), control-pulse parameterization, target product channel.
- Output: optimized pulse and predicted yield / selectivity (measurable in pump-probe or product-yield experiments).
- Mechanism: Hamiltonian simulation evaluates the control objective and its gradients (Magann et al. PRR 2021; Castaldo et al. PRA 2021). The objective is quantum-native (many-mode coherent dynamics), not an argmin of a classical energy.
- Classical SOTA: ML-MCTDH / MPS-TDVP propagation with Krotov/GRAPE; closed-loop experimental learning control (the experiment evaluates the objective directly).
- Novelty: C.
- Main risk: closed-loop experiments already act as the oracle, so there is no computational need; the PES/vibronic-coupling model floor dominates optimal-pulse predictions; gradient estimation needs O(P) evaluations x shots, which puts break-even far beyond early FT (my rough estimate is 1e14 Toffoli per optimization; UNVERIFIED).
- Verdict: weak.

### C5. Annealer-native coherent dynamics of programmable quantum spin ice (monopole transport) as a material-anchored subsection of the King et al. claim
- Input: dipolar square/pyrochlore-projected spin-ice couplings, transverse field Gamma, quench/anneal schedule.
- Output: monopole mean-squared-displacement exponent, Dirac-string statistics, defect density vs anneal time.
- Mechanism: native transverse-field Ising Schrodinger dynamics on the annealer (quantum-native).
- Classical SOTA: t-VMC (2609.01719), BP tensor networks (2503.05693), NQS (2503.08247), classical stochastic monopole dynamics.
- Novelty: D. Giergiel & Surowka (2603.28125) claim monopole transport beyond classical stochastic relaxation; no TN/NQS comparator appears in the abstract.
- Main risk: the parent claim is already challenged (E); coherent ns-scale annealer dynamics do not correspond to the timescale of any real spin-ice material (model floor: real spin-ice dynamics are thermally activated, ms to s); classical variational methods are closing the gap.
- Verdict: weak.

### C6. Correlated configurational ordering (dopant / vacancy / charge order) with quantum-computed cluster-expansion training energies
- Input: supercell configurations of a strongly correlated oxide; Hamiltonian per configuration (active space or downfolded Hubbard).
- Output: ordering ground state / order-disorder temperature via cluster expansion + classical MC.
- Mechanism: QPE energies for ~1e2 training configurations (quantum-native evaluation). The search stays classical (MC on the CE), which avoids the protein failure mode.
- Classical SOTA: DFT+U / hybrid-DFT CE, AFQMC/DMC per configuration, DMFT.
- Novelty: B (only QAOA on a classical CE was found, 2503.09356).
- Main risk: ordering energies of meV/site require solver + model error below 1 meV; vibrational/entropic and lattice-relaxation terms dominate model error; ~1e2 QPE runs each costing 1e9-1e11 Toffoli.
- Verdict: weak.

## Killed ideas
- DQI / OPI / max-LINSAT: the strongest verifiable optimization candidate (Khattar et al. 2510.10967: ~5.7e6 Toffoli for instances that need >1e23 classical trials), but OPI is finite-field polynomial regression with no physical or measurable output. Random sparse instances are obstructed by OGP (2509.14509); MCMC emulates DQI quality (2607.28120); on bounded-degree instances the advantage is limited to a constant prefactor (2606.13570); the only application found is an automotive ILP (2509.08328, an excluded class).
- Hamiltonian DQI Gibbs sampling: in the efficient regimes (toric/Haah codes) the same paper gives a matching classical algorithm (2510.07913); the non-commuting case reaches only constant beta, and no physical material instance exists.
- Quartic planted inference (Kikuchi, 2406.19378): beyond quadratic, but planted noisy kXOR has only cryptographic motivation; no physical measurement sits at the detection threshold.
- QHD (2303.01471 etc.): exponential / sub-exponential separations only on constructed objectives (2311.00811, 2504.14841); no speedup with exact oracles for convex problems (2503.24332); the applications are classical landscapes.
- QAOA on LABS (2308.02342): claimed scaling vs branch-and-bound (D); classical memetic tabu at GPU scale (2504.00987) and PUBO solvers (2510.24237) compete; the gain is a polynomial exponent on a classical landscape with no physical measurement.
- Rydberg MIS (2202.09372): challenged; classical solvers handle the UDG instances (2307.09442), so E.
- Quantum-enhanced MCMC (2203.12497): generic speedup bounded (2403.03087, 2408.07881), so E; classical Boltzmann landscapes fall under protein lesson 3.
- Quantum backtracking / branch-and-bound: quadratic (1509.02374); does not survive FT overhead (2011.04149).
- QAOA/annealing configurational search on classical cluster expansions (2503.09356): argmin of a classical energy.
- Generic annealer "beyond-classical" spin-glass quench dynamics (2403.00910): E (2503.05693, 2503.08247, 2609.01719).
- Annealer hysteresis / Ca3Co2O6 magnetization (2506.17418, 2101.02769): stoquastic Ising, where QMC and classical kinetic MC are competitive; the material dynamics are thermally activated.
- Scaling advantage vs PIMC relaxation (1911.03446): PIMC is not a dynamics comparator (weak baseline, D).
- NMR/DNP pulse design with many-spin objectives: spin dynamics are classically tractable where informative (project lesson 5; DNP was killed earlier).
- Floquet/pump-pulse optimization of photoinduced phases: no quantum-computing paper found (arXiv "optimal control" photoinduced "quantum algorithm": 0 hits), but the experiment is its own oracle and the heating/phonon model floor dominates.
- Variational metrology protocol design: already demonstrated on-device with programmable quantum sensors [UNVERIFIED citation: Marciniak et al., Nature 2022]; the device evaluates its own objective.

## Query log (final, 2026-09-28)
WebSearch: budget exhausted (200/200) at the first call ("decoded quantum interferometry classical algorithm challenge max-XORSAT 2025").
arXiv export API (local urllib; later HTTP 429):
1. abs:"decoded quantum interferometry" (40, by date)
2. id_list: 2510.07913, 2604.09533, 2510.10967, 2509.08328, 2509.14509, 2607.28120, 2605.00312, 2606.13570, 2510.06603
3. (abs:"quantum annealer" OR abs:"quantum annealing") AND (spin glass|frustrated magnet|spin ice) AND (dynamics|simulation) AND (material|experiment|neutron)
4. abs:"beyond-classical" AND abs:"quantum annealing"
5. id_list: 2609.01719, 2101.02769, 2603.28125, 1911.03446, 2504.06283, 2403.00910
6. id_list: 2309.16596
7. abs:"local minima" AND quantum AND (thermal perturbations|Lindbladian|cooling) AND Hamiltonian -> 429
8. abs:"optimal control" AND (quantum computer|algorithm|simulation) AND (molecular|chemical reaction|photochemistry) -> 429
OpenAlex:
9. search "Local minima in quantum systems Chen Huang Preskill"; title.search "local minima in quantum systems"
10. cited-by W4407675334|W4399521417|W4387225835 (36 works)
11. search "quantum computer algorithm quantum optimal control molecular dynamics laser pulse"
12. title.search: "digital quantum simulation of molecular dynamics and control"; "quantum optimal control with quantum computers"; "quantum algorithm optimal control molecules"; "quantum computing laser control chemical reactions" (429)
Crossref: 13. DOIs 10.1103/8s88-x43b, 10.1103/4zs8-7kf4, 10.1103/6r9l-lynr
arXiv HTML search (WebFetch):
14. "optimal control" "quantum computer" molecular
15. control "digital quantum simulation" molecular
16. "low autocorrelation binary sequences"
17. "quantum hamiltonian descent"
18. "classical oscillators" quantum algorithm
19. "local minima" "thermal gradient descent"
20. metastable hysteresis "quantum computer"
21. "quantum-enhanced Markov chain Monte Carlo"
22. "maximum independent set" Rydberg classical speedup
23. "cluster expansion" "quantum computer" alloy
24. "optimal control" photoinduced "quantum algorithm" (0 hits)
25. "belief propagation with quantum messages"
26. superadditivity joint detection receiver experiment coherent state (1 hit)
27. "green machine" Hadamard receiver (0 hits)
28. superadditive capacity receiver
arXiv abs pages (WebFetch): 2406.19378, 2308.02342, 2303.01471, 2504.14841, 2303.13012, 1509.02374, 2310.05889, 2609.20721
