# Search for an original, high-likelihood quantum advantage (atomic scale)

_2026-09-28. Deep literature search: four domain agents, one per lens, then one red-team agent against the finalists. Companion to `NEXT_TOPICS.md`, which has the top-10 list of already-studied topics. **This is literature evidence only. No experiments were run.**_

## The question and the short answer

The request was for a topic with **huge use, very high likelihood of quantum advantage, and not yet discovered**.

**Short answer: nothing in the literature meets all three at once.**
- Across about 30 candidates in four lenses, no domain agent rated any candidate above 2/5.
- The red team concluded that no candidate is both likely and undiscovered.

The pattern is consistent:
- **Where a candidate is new**, nobody has done the quantum analysis because the bottleneck is model or parameter error, or the problem has low entanglement. Lessons L2 and L3 fail.
- **Where a solver wall is plausible**, a Google, Xanadu, PsiQuantum or GM-type group has already published the resource estimate or a template for it. L5 fails.

**The original contribution is on the hardness side.** Most published fault-tolerant resource estimates **never benchmark against the strongest classical method**. Mapping exactly where that method fails, or showing it does not fail, is new and checkable. It can also be done on this machine, and it is the same full-versus-ablation discipline this repo already follows.

## Method

- **Filters.** Each candidate was scored against:
  - L1: a genuinely quantum object;
  - L2: hardness that survives the best classical methods, where single-family convergence does not count as convergence;
  - L3: solver error larger than model error;
  - L4: a decision that flips;
  - L5: novelty.
- **Lenses.** The four agents covered:
  - (a) spin dynamics and magnetic resonance;
  - (b) real-time and finite-temperature correlated dynamics;
  - (c) quantum-data-native (sensor or experiment input);
  - (d) under-explored industrial chemistry.
- **Red team.** The red team re-ran the novelty searches against OpenAlex, Crossref and the arXiv API, with at least four queries per candidate. It also ran the strongest classical method it could find against five finalists.
- **Limits.**
  - The web-search budget was exhausted, and Semantic Scholar rate-limited the red team.
  - Novelty therefore rests on arXiv, OpenAlex and Crossref only, and **a negative search is not proof of white space**.
  - Arxiv IDs and DOIs were checked by the agents. Items marked [mem] were recalled, not checked.

## Finalists after the red team

| Rank | Candidate | Use | Novelty (A) | Classical attack (B) | Why |
|---|---|---|---|---|---|
| 1 | **Many-state organic photovoltaic donor–acceptor charge separation at ps times** (Dorfner-type P3HT:PCBM, 100 states × 113 modes) | Solar cells | KILLED as an application: Motlagh et al. arXiv:2411.13669 claimed it (1053 qubits, 2.66×10⁷ Toffolis) | **WOUNDED, the only published crack.** MPS and ML-MCTDH "deviate" (Dorfner, Brey, Burghardt, Ortmann, JCTC 2024, doi:10.1021/acs.jctc.4c00751) | Tree tensor networks converge 5 states × 252 modes for singlet fission (doi:10.1038/s41467-019-12220-7), but the many-state interface at ps times is open. The Motlagh estimate has no classical benchmark |
| 2 | **Ultrafast demagnetisation of Ni/NiO** (driven multiorbital Hubbard–Kanamori model) | Spintronics, all-optical recording | SURVIVES. No paper frames it as a quantum-computing application. The algorithm, nonequilibrium DMFT on a quantum computer, dates from 2016 (doi:10.1103/physrevx.6.031045) | WOUNDED, leaning toward model error. Phonons, magnons and transport are missing from a closed supercell. RT-TDDFT and exact clusters already reproduce the timescales (doi:10.1021/acs.jctc.5b00621, doi:10.1103/PhysRevLett.115.217204). G1–G2 NEGF scales linearly in time (doi:10.1103/physrevb.101.245101) | The framing is new, but a quantum computer might solve the wrong model exactly |
| 3 | **Methane-to-methanol at Cu-oxo sites in zeolites and MOFs** ([Cu₂O]²⁺, [Cu₃O₃]²⁺, Fe α-O) | Methanol from flared gas | WOUNDED. No quantum-computing paper found, but the P450 template (Goings et al. PNAS 2022) and the Pd-zeolite QPE paper (arXiv:2512.19778) already exist | KILLED as a case for quantum necessity. The ranking flip is already produced by classical multireference methods (Wardzala…Gagliardi, JACS 2026, doi:10.1021/jacs.6c05408). AFQMC handles [Cu₂O₂]²⁺ (doi:10.1063/1.5049143). Al siting and speciation (model error) dominate | Only a re-application of an existing template |
| 4 | **Thermal-mixing DNP electron reservoir** (hyperpolarised ¹³C-pyruvate MRI) | Cancer metabolic imaging | SURVIVES. No quantum-computing proposal found | KILLED on decision relevance. The breakdown is already mapped experimentally and explained as Anderson/Zeno localisation (arXiv:2401.08270, 2009.11784). Strong dissipation keeps entanglement low. The operating point is set empirically | Nothing left to predict that would change a decision |
| 5 | **Low-energy electron–molecule resonances and dissociative electron attachment** for low-GWP etch gases and EUV resists | Semiconductor manufacturing | WOUNDED to KILLED. The UKRmol group already calls their VQE paper the "first" in this area and cites plasma use (arXiv:2507.05514). See also arXiv:2603.26881 and 2602.20234 | KILLED. Plasma outputs are controlled by about 10 of 400 rates (doi:10.1088/0963-0252/25/1/015003). Nuclear dynamics and condensed-phase effects dominate | The extra precision a quantum computer would give is irrelevant to the decision |

## Full candidate register, per lens

| Lens | Candidate | Likelihood (agent) | Fails on |
|---|---|---|---|
| Spin | EPR/ENDOR/Mössbauer observables from metallocluster spin ladders (FeMoco E-states, OEC) | 2 | L2 (FeMoco states are "largely simple", arXiv:2601.04621), L3 (hyperfine model) |
| Spin | DNP electron reservoir | 1–2 | L4, L3 |
| Spin | Molecular spin-qubit decoherence in dense baths | 1 | L2 (modified CCE converges, arXiv:2007.00412) |
| Spin | Radical-pair compass and OLED magnetic field effects | 1 | L2 (47-spin exact calculations and semiclassics suffice, arXiv:2004.11261), L5 |
| Spin | Zero-field and liquid NMR, MRI contrast relaxivity, PHIP/SABRE, spin crossover and single-molecule magnets | killed | L2/L5; L1/L3 |
| Dynamics | Ultrafast demagnetisation | 2 | L3 risk |
| Dynamics | Electron–molecule dissociative attachment for etch gases and EUV | 1.5–2 | L4, L5 |
| Dynamics | Sn 4d Auger / ICD cascades in EUV resists | 1.5 | L3, cost ≥ 10¹⁴ gates |
| Dynamics | Optical conductivity and Seebeck coefficient of doped Mott oxides | 1 | L4; DQMC and cold atoms already there |
| Dynamics | Stopping power, polaritonic chemistry, plasmonic hot carriers, SEI | killed | L5 (arXiv:2308.12352); L2 (mean-field at large N); L1; L3 |
| Quantum data | Dose-optimal multi-pass electron phase imaging for small-protein cryo-EM | 2 | **This is a sensing advantage, not a computational one.** Hardware is not ready (arXiv:1612.04931, 2201.09183) |
| Quantum data | Quantum computational sensing for NV nanoscale-NMR decisions | 2 | Constant-factor gain, niche (arXiv:2507.16918) |
| Quantum data | Heisenberg-limited Hamiltonian learning of spin-cluster structure | 1.5 | T2 cap on the gain, L3 |
| Quantum data | Entangled learning of non-Gaussian noise | 1 | Commuting dephasing removes the separation |
| Quantum data | Quantum processor as analysis engine for quantum-device data | 4 (real) | **Already demonstrated** (arXiv:2112.00778), and useful only for characterising devices |
| Chemistry | Cu-oxo zeolite methane activation | 2 | L2 (classical multireference methods), L5 template |
| Chemistry | NiFe oxyhydroxide OER (green hydrogen) | 1–2 | L3 (potential, pH, protons) |
| Chemistry | Fe/Cr/Co photosensitisers replacing Ir/Ru | 1–2 | L2 (CCSD(T) spin gaps, ML-MCTDH) |
| Chemistry | Am/Eu separation selectivity | 1 | L3 (solvation, extraction thermodynamics) |
| Chemistry | Rare-earth magnets, phosphors, corrosion, high-entropy alloys, flow batteries, ALD, Criegee intermediates | killed | L2/L3; L5 for corrosion (arXiv:2406.18759); L1 for high-entropy alloys |

## Recommended original project

**"Classical wall" maps of published quantum resource estimates** (full versus ablation, applied to other people's claims).

1. **Primary: OPV interface charge separation.**
   - Take Motlagh's anthracene/C₆₀ model (arXiv:2411.13669) and run 2TDVP-MPS with a bond-dimension sweep to 100 fs. This takes hours on 8 cores.
   - Then run the Dorfner 113-mode, 100-state model to 1 ps with a second, independent method family (TTNS or ML-MCTDH).
   - Measure the converged charge-separation yield against bond dimension, time and number of states.
   - Outcome either way:
     - The methods converge. The Motlagh advantage window is dequantized, which is publishable.
     - The methods fail to converge while the quantum cost stays flat. The first *measured* classical wall for a decision-relevant OPV observable, which is publishable, with category 3 evidence (computational/resource advantage) for a quantum route.
2. **Secondary (fast, cheap kill tests).**
   - **Demagnetisation.** Compare G1–G2 GW/T-matrix NEGF with tDMRG/ED on a pulsed two-orbital Hubbard–Kanamori ladder, looking at local-moment decay to 100 fs. Kill the idea if they agree within experimental error, or if the spread from varying U/J over the cRPA window exceeds the spread between solvers.
   - **Cu-oxo.** Compare DMRG-NEVPT2, extrapolated in active space, with AFQMC (or FNO-CCSD(T) if AFQMC is unavailable) on 2–3 motifs. Kill the idea if the ranking agrees within about 10 kJ/mol (2 kcal/mol).
3. **The same template generalises** to the P450 (Goings), Pd-zeolite (arXiv:2512.19778) and EUV photoemission (arXiv:2602.20234) estimates. Each is a published claim with no strongest-classical benchmark.

Each of these needs a pre-registration in `experiments/preregistered/` before any run: hypothesis, comparator, metric, kill criterion. None has been started.

## Things that would change this assessment

- A published proof or measurement that TTNS/MPS bond dimension grows exponentially in time for many-state vibronic interfaces at ps times, at decision-relevant accuracy.
- Multi-pass electron microscopes reaching biological imaging. The cryo-EM idea would become a real *sensing* advantage, which is claim category 5 (hardware), not a computational one.
- An algorithm that is super-quadratic for open or dissipative dynamics with realistic baths. This would reopen DNP and PCET, in the same way K-117 remains open for all-atom sampling.
