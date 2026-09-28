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
