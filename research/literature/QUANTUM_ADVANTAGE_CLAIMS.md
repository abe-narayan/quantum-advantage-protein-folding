# Quantum advantage claims: register and status

_Literature phase, 2026-09-26. Citation keys resolve in `BIBLIOGRAPHY.md`. Labels follow the charter's claim-type list (THEORETICAL SPEEDUP, QUERY-COMPLEXITY SPEEDUP, ASYMPTOTIC SPEEDUP, SAMPLING SPEEDUP, HEURISTIC ADVANTAGE, EMPIRICAL ADVANTAGE, HARDWARE DEMONSTRATION, SIMULATOR RESULT, ORACLE-MODEL RESULT, NO ADVANTAGE, ADVANTAGE DISPUTED)._

Rules applied throughout:
- A query-complexity result is never restated as runtime.
- A simulator result is never restated as hardware advantage.
- A win against a weak baseline is recorded as HEURISTIC ADVANTAGE against that baseline, and nothing more.

## 1. General "beyond-classical" and utility claims (2019–2026)

| Claim | Labels | Status | Rebuttal / support |
|---|---|---|---|
| Sycamore random-circuit sampling (RCS), 53 qubits, "200 s vs 10,000 years" [F1] | HARDWARE DEMONSTRATION, SAMPLING | **Rebutted** | Tensor-network simulation [F4, F5, F7]. Noisy RCS is classically samplable asymptotically [F10]. |
| 67-qubit RCS, phase transitions (2024) [F9] | HARDWARE DEMONSTRATION | **Stands so far** | No protein relevance: the distribution is structureless (`QUANTUM_PRIMITIVES.md` §4.5) |
| Gaussian boson sampling: Jiuzhang (2020), Borealis (2022) | HARDWARE DEMONSTRATION | **Disputed / reproduced** | Loss-exploiting tensor networks; spoofing [F15–F17] |
| IBM "utility before fault tolerance" (2023) [F18] | HARDWARE, EMPIRICAL (expectation values) | **Rebutted** | Belief-propagation tensor networks [F19]; sparse Pauli dynamics [F20, F21]; effective-volume tensor networks [F23] |
| D-Wave "beyond-classical computation in quantum simulation" (Science 2025) [F26] | HARDWARE, EMPIRICAL | **Disputed** | Tindall et al. [F27] (Science 2026) and Mauron & Carleo t-VMC [F28]; D-Wave reply [F29] |
| Google OTOC(2) "quantum echoes" (2025) [F30] | HARDWARE, EMPIRICAL | **Stands so far** | Companion NMR molecular-geometry work is "not yet beyond classical" [F34] |
| Noisy circuits in general | — | **Theory against** | Efficient error mitigation ⇒ classical simulability on most inputs [F35] |

## 2. Optimisation claims

| Claim | Labels | Status | Notes |
|---|---|---|---|
| QAOA approximation-ratio advantage (large-girth graphs, p=11) [C14] | THEORETICAL (D→∞) | Limited | Locality and overlap-gap limits at low depth [C12, C13, C15, C16] |
| LABS scaling advantage: QAOA + quantum minimum finding 1.21^N vs memetic tabu search (MTS) 1.34^N [C28] | SIMULATOR RESULT, HEURISTIC ADVANTAGE | **Weak** | Noiseless at N ≤ 40. QAOA alone is 1.46^N. MTS could receive the same Grover layer. GPU MTS reaches N ≤ 120 [C30] |
| Quantum-seeded MTS (QE-MTS) 1.24^N [C29] | SIMULATOR RESULT | Weak | N = 27–37; crossover extrapolated to N ≳ 47 |
| Quantum annealing scaling over SA [C42, C51] | EMPIRICAL (vs SA) | **Dissolved** | Against SQA, cluster methods, exact solvers [C41, C42, C52] |
| Scaling advantage in approximate optimisation over PT-ICM (quantum annealing correction, 2025) [C44] | HARDWARE, EMPIRICAL | **Disputed** | Simulated bifurcation shows "comparable or superior scaling" [C45]; runtime re-analysis [C46] |
| Hybrid sequential quantum computing (HSQC) benchmark [C37] | HARDWARE | NO ADVANTAGE (own abstract) | Strong classical solvers "matched or exceeded" the quantum results |
| Grover / backtracking / B&B [C54–C62] | QUERY-COMPLEXITY SPEEDUP (proven) | Valid as theory | Fault-tolerant cost kills practicality [C63–C66] |
| Kikuchi planted inference, nearly quartic [C71, C72]; DQI [C73] | THEORETICAL SPEEDUP (vs best known classical) | Valid as theory | Needs planted or algebraic structure; no protein mapping |

## 3. Sampling and estimation claims

| Claim | Labels | Status | Notes |
|---|---|---|---|
| Szegedy √(δε) rule [A1]; quantum walk search on any graph [A3, A4] | QUERY-COMPLEXITY, ORACLE-MODEL | Proven | For hitting and detection, not generic mixing |
| Generic quadratic mixing speedup | THEORETICAL | **Not proven in general** | Only special chains or distributions [A5, A6, A10]. Generic cost is O(√δ⁻¹√N) [A9]. General qsampling is SZK-hard [A11] |
| Quantum simulated annealing (QSA) 1/√δ [A8]; adaptive QSA for Bayesian inference [A31] | THEORETICAL, ASYMPTOTIC (steps) | Proven (steps) | Wall-clock: "a day and a million physical qubits" vs "four CPU-minutes" [A56] |
| Quantum Metropolis sampling [A19] | THEORETICAL | **Proof questioned** | The boosted shift-invariant QPE "may not exist" [A23]. Reduces to classical Metropolis for diagonal energies |
| Continuous non-log-concave quantum sampling, "up to quartic", quantum replica-exchange Langevin (RELD) [A44] | THEORETICAL, QUERY-COMPLEXITY | Valid (query) | Quadratic against the Poincaré-constant scaling; warm-start assumption |
| Provable continuous Gibbs separation Ω(α) vs Õ(√α) [A45] | QUERY-COMPLEXITY SPEEDUP, ORACLE-MODEL | **Proven, quadratic** | Hide-and-seek narrow-well instances on the torus |
| Nonreversible chains: "up-to-exponential" [A43] | THEORETICAL | Conditional | Relative to the chain's own mixing time; condition hard to check; no MD results |
| Fully-quantum walks: "sixth-degree", crossover under a day [A46] | SIMULATOR RESULT, HEURISTIC | **Weak** | Fits at n ≤ 10 against local/uniform Metropolis, no PT; 20 ns gates |
| Quantum-enhanced MCMC, cubic/quartic gap enhancement [A47] | HARDWARE (n ≤ 10), SIMULATOR, HEURISTIC | **ADVANTAGE DISPUTED** | No worst-case speedup [A48]; bounded by inverse participation ratio [A49]; quantum-inspired classical proposals keep the gain [A50] |
| Quantum annealers as Boltzmann samplers [A61–A63] | HARDWARE | NO ADVANTAGE | Uncontrolled temperature; spurious couplings |
| Amplitude estimation / quantum Monte Carlo [B1, B12] | QUERY-COMPLEXITY SPEEDUP (tight) | Proven | Grover–Rudolph loading erases it [B37]. Finance calibration needs 10–50 MHz logical T-rate [B43, B44] |
| Quantum partition-function algorithms [B26–B28] | THEORETICAL, ORACLE-MODEL | Proven (steps) | The only practical lever is √δ |
| NISQ / variational amplitude estimation [B6, B7, B11] | SIMULATOR / HARDWARE | NO ADVANTAGE | Gain capped by depth; noise saturation |

## 4. Protein and peptide claims (the quantum-folding literature)

Failure-mode columns:
- **FM1:** diagonal cost with argmin or tail readout.
- **FM2:** enumerable instance.
- **FM3:** weak classical twin.
- **FM4:** cost does not track accuracy.

| Claim | Rep. / max size | Labels | Baseline | FM | Status |
|---|---|---|---|---|---|
| Lattice folding by quantum annealing [D2 = A70] | 2D MJ lattice, 6 aa / 81 qubits | HARDWARE | Enumeration (40 conformations) | 1, 2, 3 | NO ADVANTAGE ("can be solved in a classical computer") |
| Lattice QAOA with constraints [D4]; turn circuits [D5] | 4–10 aa | SIMULATOR / HARDWARE | None / Monte Carlo check | 1, 2, 3 | No advantage claimed |
| Resource-efficient CVaR-VQE folding [D6] | Tetrahedral, 10 aa / 22 qubits (simulated) | SIMULATOR, HARDWARE (7 aa) | None | 1, 2, 3 | **Same objective as the predecessor.** H-001, R1 and R2 apply verbatim |
| "Limited quantum speedup" on lattice proteins [D7 = A71] | 2D/3D, 6–9 aa | SIMULATOR (ideal closed-system QA), HEURISTIC | Off-the-shelf GSL SA | 1, 2, 3 | **Weak**: 3–4 sizes; internally inconsistent 3D rate (0.45 vs 0.75); SA fit possibly an artefact |
| QFold: quantum walks and deep learning [D9 = A65] | Torsions, ≤ tripeptides (64–1,024 states) | SIMULATOR, HEURISTIC; trivial HARDWARE (4 qubits) | Matched Metropolis | argmin TTS, 2, 3 | **Evidence of advantage KILLED**: energy table precomputed by enumeration; exponent 0.85–0.89 with Minifold initialisation; 10^87–10^373 extrapolation unsupported |
| Folding lattice proteins with quantum annealing [D10 = A69] | 2D HP, 64 aa hybrid / 14 aa pure QPU | HARDWARE | SA; exact references | 1, 2, 3 | Hybrid confounds attribution; pure-QPU success decays exponentially |
| Peptide conformational sampling with QAOA [D14] | Tetrahedral + LJ, ≤28 qubits | SIMULATOR | Random sampling | 1, 2 | **NO ADVANTAGE**: "matched by random sampling up to a small overhead" (mirrors S33 QX-25) |
| Counterdiabatic and bias-field digitised counterdiabatic folding [D15–D17] | Tetrahedral, up to 16 aa / 61 qubits | HARDWARE | None / brute force / random seeds | 1, 2, 3 | Post-processing "overwrite[s]" the quantum signal (D17) |
| Quantum folding "beats AlphaFold2" on fragments (IBM/Cleveland 2024) [D21] | 7 aa | HARDWARE | Brute force, Gurobi, AF2 | 1, 2, 3, **4** | The best-RMSD sample is **not** the Hamiltonian optimum (1.781 vs 1.879 Å) |
| Grover over BCC conformations [D30] | 2 aa / 25 qubits | SIMULATOR, QUERY-COMPLEXITY | Brute force | 2, 3 | Query speedup over brute force only; the classical frontier is pruned search |
| Cost-Hamiltonian reliability [D28 = A72] | Small peptides | NO ADVANTAGE (validity) | — | **4** | The lattice optimum has worse RMSD than a random feasible fold |
| Rare conformational transitions on D-Wave [A67, A68] | Low-resolution path ensembles | HARDWARE | Anton MD (agreement) | — | Agreement, not advantage |
| Rotamer QAOA scaling [D32] | 6 residues / 54 qubits (MPS-simulated) | SIMULATOR, HEURISTIC | SA ("calls") | 1, 2, 3 | Incommensurate units |

**Meta-verdict** [D §10]. No paper from 2008–2026 shows a load-bearing quantum component against a strong classical baseline on a realistic protein representation. No paper satisfies even two of the three conditions together:
1. a realistic representation;
2. a strong baseline (PERM, REMC, Wang–Landau, CPSP, DEE);
3. a load-bearing quantum part.

## 5. Chemistry and electronic structure

| Claim | Labels | Status |
|---|---|---|
| FeMoco resources: ~10¹⁵ T gates [F58]; ~4 M physical qubits, under 4 days with tensor hypercontraction (THC) [F61] | Fault-tolerant resource estimate | Valid estimates. The flagship target is eroding: the model was solved classically to chemical accuracy in a 2026 preprint [F65]; criticised as unrepresentative [F63] |
| Cytochrome P450 compound I: ~4.6 M qubits, 73 h [F62] | FT resource estimate | "Has the potential to be a quantum advantage problem" |
| Exponential advantage for generic ground-state chemistry | — | **Not evidenced** [F64] |
| Quantum free-energy algorithms [B53, B54] | THEORETICAL (vs prior quantum) | No classical comparison; no concrete resource counts |

## 6. What survives, and in what form

**I(prog).** After these rebuttals, the claims that survive and connect to protein-structure computation are all **fault-tolerant, query-model, quadratic** sampling speedups:
- Szegedy walks and quantum simulated annealing, including the Bayesian-inference framing [A8, A31];
- the continuous-domain separation [A45];
- quantum replica-exchange Langevin [A44].

None has been demonstrated or costed on a protein energy.

**The only empirical protein "advantage"** (QFold [D9]) does not survive scrutiny as evidence.

**The only protein result in this literature that bears on validity** is negative [D28], and it matches the program's own S29–S33 condition-C finding.
