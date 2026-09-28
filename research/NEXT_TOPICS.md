# Next topics: atomic-scale prediction/optimisation problems for a quantum-advantage search

_2026-09-28. A short literature scan (from memory plus the program's bibliography; the session's web-search budget was exhausted). **Every citation below must be verified before it is relied on.**_

## What protein folding taught us

The four sprint rounds narrow where a real advantage can live. A good next topic needs all four of the following:

1. **A genuinely quantum object.** Electrons or nuclei whose behaviour is quantum-mechanical, not a classical energy that has merely been put on a quantum computer. Every classical-objective route died on a quadratic ceiling plus the runtime floor (K-101, K-107).
2. **Strong correlation that beats the best classical solvers.** The benchmark classical methods are DMRG, AFQMC, CCSD(T) and selected CI. The "hardness" must not be an artefact of a weak baseline; that was the distance-geometry lesson.
3. **The solver error must be the bottleneck, not the model error.** It must dominate the errors from environment, solvent, dynamics and basis set. This was the FeMoco lesson.
4. **A decision that matters.** A real product or process choice should flip when the energy is computed more accurately.

## Candidate topics, ranked

| Rank | Topic | Real-world stakes | Why quantum might matter | Main classical threat | Prior |
|---|---|---|---|---|---|
| 1 | **Transition-metal catalysis** (nitrogen fixation, CO₂ reduction, C–H activation, water oxidation) | Fertiliser (Haber–Bosch uses ~1–2% of world energy), fuels, green chemistry | Multi-metal active sites are strongly correlated; spin states and reaction barriers need ≤1 kcal/mol accuracy. This is the most-studied fault-tolerant chemistry target: FeMoco estimates by Reiher et al. 2017 and Lee et al. 2021 (tensor hypercontraction); cytochrome P450 by Goings et al. 2022 | Lee et al. 2023 (Nat. Commun., "Evaluating the evidence for exponential quantum advantage in ground-state quantum chemistry") argue classical heuristics keep up; DMRG and AFQMC are improving fast | **Highest** |
| 2 | **Battery materials**: Li/Na-ion cathodes (Ni/Mn/Co oxides, Li-rich layered oxides), redox, degradation | EVs and grid storage | Transition-metal d-electrons and oxygen redox are strongly correlated, and DFT+U gets voltages and phase stability wrong. Several fault-tolerant resource estimates exist for cathode materials (e.g. Google/BASF-type studies on LiNiO₂, ~2023–24, to verify) | Periodic systems need huge qubit counts; embedding (DMET) plus classical correlated solvers | High |
| 3 | **Photochemistry and excited states**: OLED emitters, photovoltaic dyes, photoswitches, photodegradation | Displays, solar, drug photostability | Conical intersections and multi-reference excited states break TDDFT. Quantum phase estimation / excited-state algorithms give exact multi-reference energies; nonadiabatic quantum dynamics is itself quantum | CASPT2/NEVPT2 and MRCI at moderate active spaces; ML surrogates | Medium–high |
| 4 | **Drug–metal and covalent binding energies** (metallodrugs, metalloenzyme inhibitors, covalent warheads) | Drug discovery | Accurate binding energies at metal centres or bond-forming sites, where force fields and DFT fail | Free-energy perturbation dominates, and the error is mostly sampling and model, not electronic (the same trap as proteins); QM/MM with DLPNO-CCSD(T) | Medium–low |
| 5 | **Nuclear quantum effects**: proton transfer and tunnelling in catalysts and materials | Fuel cells, hydrogen storage, enzymes | Tunnelling and zero-point effects | Path-integral MD is sign-free and classically efficient (K-115) | Low |
| 6 | **Crystal structure prediction / materials discovery** (a direct optimisation analogue of folding) | Pharmaceutical polymorphs, new materials | Search over structures | **Likely a repeat of protein folding.** A classical energy plus search gives a quadratic ceiling, and ML potentials plus random-search baselines are strong | Low (a useful control, not a lead) |
| 7 | **Correlated-materials design** (superconductors, magnets; Hubbard-type models) | Energy transmission, electronics | The canonical quantum-simulation advantage (dynamics, low-temperature phases) | Tensor networks and QMC; more physics than application | Medium, but "too physics" for your brief |

## Recommendation

**Start with #1, transition-metal catalysis**, framed as a *decision* problem rather than an energy problem:

> Does exact correlated electronic structure (fault-tolerant QPE) change which catalyst, spin state or reaction pathway is predicted, compared with the best classical solver, at a cost that beats it?

This carries over the three filters that did the most work in this sprint:
- a classical-reach check against DMRG, AFQMC and CCSD(T) at the same active space;
- a model-floor ladder (active-space size, basis set, embedding and environment);
- a value test (does the ranking flip?).

A cheap first experiment on this machine: take 5–10 published catalyst benchmarks with known spin-state or barrier controversies, measure how far classical correlated methods disagree with each other, and check whether that spread exceeds the model-floor spread. This is the FeMoco-E4 test (K-115 residue) turned into a program.

**#2 (batteries)** is the best second track: large industrial interest, and the same test structure applied to periodic embedding.

## Papers to verify and read first

- Reiher, Wiebe, Svore, Wecker, Troyer, "Elucidating reaction mechanisms on quantum computers", PNAS 2017 (FeMoco).
- Lee et al., "Even more efficient quantum computations of chemistry through tensor hypercontraction", PRX Quantum 2021.
- Goings et al., "Reliably assessing the electronic structure of cytochrome P450 on today's classical computers and tomorrow's quantum computers", PNAS 2022.
- Lee et al., "Evaluating the evidence for exponential quantum advantage in ground-state quantum chemistry", Nat. Commun. 2023. This is the main classical counterargument.
- von Burg et al., "Quantum computing enhanced computational catalysis", PRR 2021 (ruthenium CO₂ catalyst).
- Bauer, Bravyi, Motta, Chan, "Quantum algorithms for quantum chemistry and quantum materials science", Chem. Rev. 2020 (review).
- Recent FeMoco classical results in the program's bibliography (arXiv:2601.04621, preprint), and battery-cathode FT resource estimates 2023–2025 (search "LiNiO2 quantum resource estimate").

---

# Top 10 (2026-09-28, multi-agent literature review): supersedes the ranking above

_Method: three parallel literature agents, one per cluster: (a) catalysis and metalloenzymes; (b) energy and functional materials; (c) quantum dynamics and spectroscopy. Each agent checked arXiv IDs against the arXiv API or abstract pages on 2026-09-28. Items marked [unverified] were recalled, not checked. Each candidate was scored against the four protein-folding lessons above. **Likelihood** is the agents' 1–5 estimate after that filter._

**Honest headline.** No topic scores above 3/5. The literature does not support a "high likelihood" of advantage anywhere yet.

The strongest shift since the first ranking is that **FeMoco, the flagship ground-state target, is being caught up with classically**:
- arXiv:2601.04621: high-order coupled cluster plus DMRG with extrapolation reaches chemical accuracy.
- arXiv:2510.04795: GPU DMRG on CAS(113,76).

The best odds have moved toward **quantum dynamics**, where lesson 1 (a genuinely quantum object) is satisfied by construction and published Toffoli counts are lowest (10⁶–10⁸).

| # | Topic | Real-world use | Quantum route | Best published cost | Main classical threat | Likelihood |
|---|---|---|---|---|---|---|
| 1 | **Vibronic exciton and charge transport** in organic PV, singlet fission and light-harvesting antennas | Solar-cell design rules | Block-encoded vibronic Hamiltonian time evolution | 154 logical qubits, 2.76×10⁶ Toffolis for 100 fs of exciton transport; 1053 qubits, 2.7×10⁷ Toffolis for a charge-transfer model (Motlagh et al., arXiv:2411.13669). Tensor factorisations: arXiv:2504.08065. Reaction-centre workflow on Quantinuum hardware: arXiv:2607.05786 | TD-DMRG, ML-MCTDH, tree-tensor-network HEOM | 3 |
| 2 | **Non-adiabatic dynamics at metal surfaces** (N₂ on Ru/Fe for ammonia, CO on Cu, hot carriers) | Heterogeneous catalysis, ammonia | Trotterised Anderson–Newns electron–nuclear dynamics | 271 qubits, 7.9×10⁷ Toffolis (100 metal orbitals, 20 modes, 1000 steps; Lang et al., arXiv:2601.16264) | Electronic friction, IESH, ML-MCTDH. Model parameters come from DFT | 3 |
| 3 | **Cytochrome P450 Compound I, C–H activation** | Drug metabolism, drug–drug interactions | Qubitised QPE (THC / BLISS-THC) | Crossover at ~40–50 orbitals (Goings et al., arXiv:2202.01244; qubit/day figures [unverified]). ~100× cut from active-volume compilation (arXiv:2501.06165). ~10⁵ physical qubits, days to weeks, on an early-FT architecture (arXiv:2603.22778) | DMRG-NEVPT2 (small models), AFQMC | 3 |
| 4 | **Multinuclear Mn/Cu clusters**: the Mn₄CaO₅ oxygen-evolving complex, Cu/Fe methane monooxygenase | Artificial photosynthesis, methane to methanol | QPE for low-lying spin ladders | No dedicated estimate. Minimal models probably fall in the 20–50-orbital regime of arXiv:2603.22778 [inference] | DMRG on minimal models; broken-symmetry DFT known to be unreliable | 3 |
| 5 | **Photodynamics through conical intersections** (PDT photosensitisers, DNA photodamage, photoswitches) | Cancer photodynamic therapy, photostability | Grid or vibronic simulation; analog trapped-ion vibronic simulation | PDT photosensitisers: 180–350 logical qubits, Toffoli depth 10⁷–10⁹ (arXiv:2512.15889). Pyrazine: arXiv:2506.08609. Geometric phase at a conical intersection seen on trapped ions (arXiv:2211.07319) | ML-MCTDH (pyrazine with 24 modes is routine), surface hopping. Potential-surface error often dominates | 3 |
| 6 | **Cathode oxygen redox and core spectroscopy (XAS/RIXS)** in LiNiO₂ and Li-rich Mn oxides | EV batteries: voltage fade, O₂ loss | Time-evolution spectroscopy / QPE on embedded clusters | XAS, CAS(22,18): ~100 logical qubits, <4×10⁸ T gates (arXiv:2506.15784). RIXS, 20 orbitals: 414 qubits, 2.0×10¹⁰ Toffolis (arXiv:2602.20270). Periodic LNO: arXiv:2302.05531 (very large) | 18 orbitals is exactly solvable. Advantage needs ~40–80 orbitals. Embedding error may dominate | 3 |
| 7 | **Fe–N–C single- and dual-atom fuel-cell catalysts** (spin states, O₂ binding) | Pt-free fuel cells | QPE (double factorisation / THC) on an embedded FeN₄ site | None specific; nearest is arXiv:2603.22778. Spectrum amplification gives 4–195× (arXiv:2502.15882) | DMRG-NEVPT2 and AFQMC do well on single Fe. Dual Fe–Fe and Fe–Co sites are more promising | 2–3 |
| 8 | **Non-perturbative proton-coupled electron transfer rates** (multi-site, anharmonic) | Enzymes, redox catalysts, batteries | Analog trapped-ion open-system simulation; digital spin-boson | Trapped-ion donor–acceptor transfer with an engineered bath (arXiv:2405.10368). Roadmap: arXiv:2305.03156. No FT estimate | HEOM, RPMD/instanton, tensor-network influence functionals. Single-transfer rates are solved | 2 |
| 9 | **FeMoco reaction intermediates** (E₂–E₄, N₂ binding) | Low-energy ammonia catalysts | QPE with THC / spectrum amplification | ~4 M physical qubits, <4 days (arXiv:2011.03494). ~89 k qubits, <1 month on a denser code (arXiv:2605.30455) | Now close to classically solved for the standard model (arXiv:2601.04621). Neural backflow: arXiv:2604.06841 | 2 |
| 10 | **Homogeneous CO₂ and N₂ reduction catalysts** (Ru, Mo complexes) | CO₂ to methanol, ammonia | Double-factorised QPE | Ru catalyst: arXiv:2007.14460. N₂ cycle: ~1.39×10⁵ QPU-h against ~4×10⁵ CPU-h of DMRG, utility ~$200k (Bellonzi et al., arXiv:2406.06335) | The authors' own numbers put quantum cost on the same order as DMRG | 2 |

**Considered and not ranked**, with the lesson each one fails:
- Solid-state quantum emitters (NV, SiV, hBN): the active spaces are small, so embedding double-counting dominates (lesson 3).
- Polaron dynamics in LiMn₂O₄ (arXiv:2606.16017): the model is phenomenological, and tensor networks are strong in quasi-1D.
- f-element separations: relativity and solvation model error dominate.
- Anharmonic vibrational / 2D-IR spectra, and attosecond dynamics: VCI, TD-DMRG and TDDFT are adequate.
- Liquid or zero-field NMR: this matches kills K-117–K-120.
- Drug binding free energies: sampling dominates, the same trap as proteins.

## What to do first

The recommendation is **#1 plus #2** (quantum dynamics), with **#3 or #4** (static strong correlation) as a second lane. Every topic starts with the same classical-first test, the one that decided the protein program:

> **Find the classical wall.** For a realistic model, locate where the best classical method's cost becomes exponential. For dynamics that is TD-DMRG / ML-MCTDH bond dimension against mode count and propagation time. For statics it is DMRG / AFQMC / CCSD(T) disagreement against active-space size. Then check two further things: at that point, does solver error exceed model error, and does the answer change a decision?

Concrete first projects, all laptop-scale:
- **#1.** Reproduce the Motlagh singlet-fission model with TD-DMRG. Publish the curve of bond dimension (at 10⁻² population accuracy) against time and mode count. A "classical wall" curve is a publishable result whichever way it comes out.
- **#2.** Run the Anderson–Newns model classically: exact dynamics for small baths, MPS for large ones. Find the coupling and bath size where the bond dimension blows up, and check whether friction theory fails there.
- **#3.** A Compound I series at 20–60 orbitals. Find the smallest model where DMRG-NEVPT2 and CCSD(T) disagree by more than 2 kcal/mol on the spin gap or barrier.
- **#4.** A minimal 4-Mn model of the S₂ state. Check whether the ordering of the g = 2 and g = 4.1 spin isomers is converged in DMRG bond dimension.

Each of these is the direct analogue of the attack that killed the NMR echo at observable times (K-119). If the wall is never reached at useful sizes, record the kill. If it is reached, cost the quantum circuit for that exact regime.
