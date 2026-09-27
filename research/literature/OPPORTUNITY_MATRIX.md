# Quantum Opportunity Matrix (literature-informed)

_Literature phase, 2026-09-26. Map ids (SP-, AA-, QA-, C-, DE-) refer to `research/QUANTUM_OPPORTUNITY_MAP.md`; QX- ids refer to `research/sprint29-33/QUANTUM_RESULTS.md`. Citation keys resolve in `BIBLIOGRAPHY.md`._

The matrix has 18 columns, so it is split into two tables with the same row ids. Statuses, as the charter defines them: **KILLED / WEAK / INTERESTING / PROMISING / HIGH PRIORITY.** Ranking follows evidence, testability and decisiveness. It does not follow excitement.

## Table A: mechanism

| Id | Candidate | Protein bottleneck | Quantum primitive | Classical competitor | Evidence for speedup | Type of speedup | Scaling (literature) | Oracle assumptions | State-prep cost | Measurement cost |
|---|---|---|---|---|---|---|---|---|---|---|
| M1 | Walk / QSA sampling of a learned-energy structure posterior | Exact posterior sampling at ≥60 aa (SP-1, AA-1) | Szegedy walk, QSA, adaptive QSA [A1, A8, A31] | PT/REST2 + HMC, SMC, learned-proposal MCMC, amortised generators [E33, E47, E51, E77, E79, E83] | Proven in steps [A8, A31] | QUERY/ASYMPTOTIC (steps), quadratic in gap | 1/√δ vs 1/δ with a warm path; √N penalty from a cold start [A9] | Coherent ΔE of O(N²) pair terms plus Metropolis rotation; ~10⁶–10⁸ Toffolis/step at 100 aa (I(agent) [A §3.9]) | Cheap uniform start; anneal ℓ/√δ per sample | 1 sample per anneal (no cloning) |
| M2 | Continuous QSVT / quantum Langevin / quantum replica-exchange sampler | Same as M1, continuous coordinates | Witten-Laplacian QSVT, quantum RELD [A44]; provable separation [A45] | As M1 | Provable Ω(α) vs Õ(√α) on hide-and-seek wells [A45] | QUERY-COMPLEXITY, quadratic in e^{βΔ} or C_PI | Õ(√(β d C_PI)), C_PI ~ e^{βΓ} [A44] | Coherent gradient oracle ∇V; never costed | Warm start \|⟨φ\|σ⟩\| = Ω(1) or annealing [A44, A45] | d × log(grid) qubits per sample |
| M3 | Quantum-walk hitting time for rare conformational transitions | Rare-event kinetics | MNRS / Krovi / AGJK walks [A2–A4]; Chowdhury–Somma [A22] | WE, TPS, MSMs, milestoning [E60, E62–E64, E67] | Proven quadratic in hitting time [A3, A4] | QUERY | √HT vs HT | Native-free marking predicate plus coherent chain | Stationary state (= M1 problem) | Detection |
| M4 | Amplitude estimation of ensemble expectations | Posterior means, basin populations (C-3, QA-1) | QAE / quantum mean estimation [B1, B12] | MBAR, QMC, control variates, parallel MC [B60, B68, B46] | Tight quadratic in ε [B16, B29] | QUERY | σ/ε vs σ²/ε² | Coherent observable plus coherent ensemble state | Grover–Rudolph erases the speedup [B37]; needs M1 | O(σ/ε) coherent calls |
| M5 | Quantum partition-function / free-energy estimation | Z, ΔF of conformational models | Wocjan et al. → Montanaro → Harrow–Wei → Arunachalam et al. → Cornelissen–Hamoudi [B24, B26–B28] | AIS/SMC, Wang–Landau, nested sampling [B64–B67]; K*/CFN counting [B75, B76] | Proven (steps) | THEORETICAL, ORACLE-MODEL | Õ(log^{3/4}\|Ω\|/(ε√δ)) vs Õ(log\|Ω\|/(ε²δ)) [B28] | Walk operator at every β | As M1 | AE per stage |
| M6 | Quantum rejection sampling, prior → posterior | Posterior from a learned prior | Ozols–Roetteler–Roland; Low–Yoder–Chuang [A36, A37] | SMC / annealed importance sampling [E74, E75]; learned samplers + reweighting [A78] | Quadratic in 1/P_acc (tight) | QUERY | P^{−1/2} vs P^{−1} | **Coherent prior circuit: the whole decoder run reversibly** | Dominant, prohibitive | 1 per amplification |
| M7 | Quantum-enhanced MCMC proposals (NISQ) | Proposal quality | Layden et al. [A47] | PT, cluster moves, tensor-network proposals [A50] | Empirical n ≤ 10; disputed [A48, A49] | HEURISTIC | fitted 2^{−kn} (n ≤ 10) | Diagonal qubit Hamiltonian (register encoding) | Trivial | 1 shot per proposal |
| M8 | Quantum annealer as Boltzmann sampler | Ensemble sampling | Freeze-out sampling [A61–A63] | PT, QMC [A64] | None | — | — | Native 2-local Ising, embedding | — | Many anneals |
| M9 | Grover / amplitude-amplified decoder restarts | Global search beyond 60 aa (C-2, AA-2) | Amplitude amplification, Dürr–Høyer [C54–C56] | Restart-saturated L-BFGS (QX-30), PT | Optimal quadratic (query) | QUERY | √R restarts | **Reversible continuous decoder** | Uniform | O(1) |
| M10 | Quantum backtracking / B&B for rotamer, contact or branch CSPs | Per-residue discrete choice (C-4, QA-4) | Montanaro backtracking and B&B [C57–C61] | DEE/A*, cost-function networks, tree decomposition, CPSP [C82, C83, C85] | Near-quadratic vs the same tree | QUERY | O(√T n^{3/2} log n) | Coherent predicate and bound | Root | Phase estimation |
| M11 | QAOA / VQE / CVaR / annealing on lattice or register folding | Global minimum of a proxy energy | [C1–C6, D6, D7, D10, D15–D17] | PERM, REMC, Wang–Landau, CPSP [D42–D47]; SA (equal tuning), random prior (QX-25) | None undisputed | HEURISTIC, disputed | none valid | Diagonal k-local, O(N⁴) terms [D6] | Trivial | 1/P(x*) shots, exponential [C19] |
| M12 | Super-quadratic structured primitives (Kikuchi planted inference, DQI, short path) applied to structure inference from noisy restraints | Contact / restraint inference | [C69–C73] | Spectral methods, decoders | Theory vs best known classical | THEORETICAL | nearly quartic [C71, C72] | Sparse matrix access | Guiding state | Phase estimation |
| M13 | Quantum generative models as structure priors or samplers | Ensemble generation | QCBM, QBM, IQP Born machines [F75–F79, F89] | BioEmu, AlphaFlow, diffusion models [E80, E83]; MCMC | Expressivity vs Bayesian networks only [F78] | THEORETICAL (expressivity) | none | Data loading | Training; untrainable if hard [F91] | Many shots |
| M14 | Hamiltonian simulation + QPE for electronic-structure energies | Energy accuracy (AA-3) | Qubitisation, THC [F45, F61] | DMRG/CCSD(T)/AFQMC; ML potentials [F65, F73, F74] | FT estimates; no generic exponential [F64] | Time (gates) | polynomial vs heuristics | Block encoding | Overlap is the crux [F64] | QPE |
| M15 | QSVT / HHL for readout convex programs | Readout (AA-4) | [F46, F50] | NNLS/QP/SOCP in milliseconds (S29–S33) | Dequantised [F52–F55] | — | — | QRAM [F56] | Dominant | Ω(N) to read out x |
| M16 | Beyond-quadratic walks (fully-quantum, nonreversible) | As M1 | [A43, A46] | PT (never compared) | Fits n ≤ 10; conditional | SIMULATOR / THEORETICAL | "6th-degree" (fitted) | Hamiltonian simulation of H_prob | — | — |

## Table B: feasibility, relevance, status

| Id | Fault tolerance needed | NISQ feasibility | Protein relevance | Tested in S29–S33? | Strongest classical counterargument | Experiment difficulty | Potential significance | **Status** |
|---|---|---|---|---|---|---|---|---|
| M1 | Yes (~10⁴ logical qubits at 100 aa; I(agent)) | None | High: the only computation-limited structure row (`PROTEIN_BOTTLENECKS.md` §1); matches the 1.40× soft-readout signal | **No.** Adjacent: an 18-qubit Born machine lost to Metropolis (QX-29); enumerable (QX-28) | Quadratic gain vs a ~10⁷–10¹⁰ per-step overhead ratio; crossover needs ≳10¹²–10¹⁵ classical steps per sample; funnels plus PT make barriers polynomial [A56, E33, E2–E6] | Classical gate: moderate (CPU). Quantum: resource estimate only | High if slow mixing is found; a negative is also publishable | **INTERESTING (conditional)** |
| M2 | Yes | None | Highest formal match to SP-1 | No | Separation only on hide-and-seek wells; funnels argue against such wells; query-only | Theory plus classical landscape census | High (theory) | **INTERESTING, top theory line** |
| M3 | Yes | None | Low: kinetics lie outside the structure endpoint | No | WE/TPS/MSM already remove the waiting-time exponential | — | Low | **WEAK** |
| M4 | Yes | Killed [B6, B7, B11] | Low | No | Bias- and mixing-limited, not variance-limited; break-even needs σ/ε ≳ 10⁴ [B71, B46] | Cheap classical audit | Low | **KILLED (practical)** |
| M5 | Yes | None | Medium (reduces to the √δ of M1) | No | Deterministic incumbents for rotamer Z; only the √δ factor matters | — | Low beyond M1 | **WEAK** |
| M6 | Yes | None | Medium in form | No | A coherent learned decoder is prohibitive; SMC is not plain rejection | — | Low | **WEAK** |
| M7 | No | Yes, but no gain at scale | Low: needs a diagonal register, which fails condition C | Adjacent (registers, DNR-08) | Disputed; dequantised by tensor-network proposals [A48–A50] | — | Low | **KILLED (protein)** |
| M8 | No | Yes | Low | Adjacent | Uncontrolled temperature; noisy Gibbs [A62, A63] | — | None | **KILLED** |
| M9 | Yes | None | Low: search is saturated | Adjacent (QX-30 saturation) | At most ~8× fewer decoder calls; each needs a reversible decoder; quadratic fails the FT test [C64, C65] | — | None | **KILLED** |
| M10 | Yes | None | Low: discrimination-limited (C-4) | Adjacent (S32 QX-15) | Exact classical solvers shrink the tree; CSP advantage "disappears" [C63, C82, C83] | Classical tree-size measurement | Low | **WEAK** |
| M11 | No (NISQ) | "Yes", but null | None: proxy energies fail condition C [D28] | **Yes: 33 experiments, null** | Every literature instance is enumerable with a weak baseline [D §4]; random sampling matches QAOA [D14] | — | None | **KILLED** |
| M12 | Yes | None | Low: planted regime vs the measured information-limited regime | No | Requires information present but hidden; the program's endpoint lacks the information | Theory note | Low | **WEAK** |
| M13 | Varies | Small only | Low | **Yes** (QX-28, QX-29, Born machine) | Data-processing inequality; trainable ⇒ surrogate [F37, F88–F91]; Born hardness is irrelevant to a specified π | — | None | **KILLED** |
| M14 | Yes (~4–5 M physical qubits, days) | None | Out of structure scope (metal-site chemistry only) | No (DE-7: energy is not the bottleneck) | No generic exponential advantage [F64]; FeMoco solved classically [F65]; ML potentials [F73, F74] | — | Chemistry, not structure | **WEAK / out of scope** |
| M15 | Yes | None | None | Adjacent (S31/S32 closed-form solutions) | Millisecond classical; dequantised | — | None | **KILLED** |
| M16 | Yes | None | As M1 | No | Fits n ≤ 10 against local Metropolis; no PT baseline | — | Watch only | **WEAK** |

## Enabling studies (classical or theoretical; these decide M1, M2 and M5)

These are **not** quantum candidates. They are the classical-first tests the matrix depends on. Every agent in the literature search independently named G1 as the decisive missing measurement [A §8, B §8, D §8, E §8, F §8].

| Id | Study | Decides | Difficulty | Status |
|---|---|---|---|---|
| G1 | **Classical mixing-time scaling of a learned-energy structure posterior vs chain length**, measured with the best classical portfolio, plus sampled soft-readout transmission | M1, M2, M5 (S1/S2 of the filter) | Moderate: needs a ≥60–150 aa instrument and a learned energy | **HIGH PRIORITY** |
| G2 | **Fault-tolerant resource estimate for a coherent learned pair-distance energy walk operator** (Toffoli/T-count, logical qubits) → explicit break-even classical steps per sample | M1, M2 (filter K5) | Paper study; no quantum hardware | **HIGH PRIORITY** (novel, decisive either way) |
| G3 | **Landscape census of learned energies**: mode count, basin widths and masses; tests for persistence or hide-and-seek structure | M2 (whether [A45]-type instances occur); explains G1 | Moderate | **PROMISING** |
| G4 | **H-001 reduction theorem**, generalised with the literature's general forms [F35, F37, F52–F55, F91] | Screens all future candidates | Theory | **PROMISING** |

**Summary.** No quantum candidate is PROMISING or HIGH PRIORITY on current evidence. Two are INTERESTING (M1, M2), and both are conditional on G1–G3. Everything else is WEAK or KILLED.
