# Strongest classical counterarguments

_Literature phase, 2026-09-26. Citation keys resolve in `BIBLIOGRAPHY.md`. **I(prog)** marks this program's own reasoning or arithmetic._

This file records the case *against* each quantum candidate. It follows the project rule: **no quantum implementation until a classical test has failed to rule the idea out.** The first section gives general counterarguments that apply to every candidate. The second gives the strongest single counterargument per candidate. The third gives the classical-first filter used to assign KILL.

## Part 1. General counterarguments

### CA-1. Quadratic speedups do not pay on early fault-tolerant hardware
- **Babbush et al.** Quadratic speedups alone will not give runtime advantage on modest surface-code machines, and quartic speedups are "significantly more practical" [A57 = B46 = C65 = F66].
  - Their break-even time is T* = t_Q²·S/t_C, where S is classical parallelism.
- **Sanders et al.** Quantum-accelerated simulated annealing needs "roughly a day and a million physical qubits" to optimise spin glasses "that could be solved by classical simulated annealing in about four CPU-minutes." For N=512 SK the crossover is about one year of quantum runtime [A56 = B47 = C64 = F67].
- **Lemieux et al.** Matching a specialised classical MCMC machine (Janus, 10¹² spin updates/s) with a quadratic speedup needs about 1 ns logical gates [A55].
- **Campbell–Khurana–Montanaro.** For constraint satisfaction, a speedup factor of 10³–10⁵ on day-long instances "disappears" once classical decoding costs are included [C63].
- **Calibration outside optimisation.** Derivative pricing via amplitude estimation needs a 10–50 MHz logical T-rate against ~10 kHz projected [B43, B44].
- **Consequence.** Every quadratic candidate (walk sampling, QSA, AE, Grover, backtracking) must clear an explicit break-even bar, not just show a better exponent.

### CA-2. Noise implies classical simulability (NISQ)
- With constant noise and no error correction:
  - noisy random-circuit sampling is classically samplable in polynomial time asymptotically [F10];
  - "efficient error mitigation ⇒ classical simulability on most inputs" [F35].
- Beyond depth ~1/p, noisy QAOA is exponentially unlikely to beat efficient classical algorithms [C25, C26].
- **Consequence.** Any NISQ protein proposal inherits these limits.

### CA-3. Trainable implies (often) classically simulable
- **Trainability barriers.** Barren plateaus [C20, C21]; landscapes "swamped with traps" [C24 = F39]; NP-hard training [C23].
- **The same structures give classical access.** Where barren plateaus are provably absent, dynamics are often confined to classically simulable subspaces [C22 = F37, F40].
- **Generative models.** Anticoncentrating (hard-to-sample) generative models are untrainable on average [F91]. Trainable IQP models admit classical surrogates [F88–F90].
- **Relation to this program.** This is the general form of the S29–S33 result that the circuit was replaceable by a closed form or a random sampler (H-001).

### CA-4. Precision is not the bottleneck in biomolecular estimation
- Biomolecular free-energy errors are dominated by force-field bias ("RMS errors in the 1–2 kcal/mol range") and by barrier-limited sampling. Statistical precision of ≲0.1 kcal/mol is already routine [B71].
- MBAR is statistically optimal [B60 = E69].
- Quasi-Monte Carlo gives near-quadratic rates on smooth integrands [B51, B68].
- **Calibrated crossover (I(prog) arithmetic on the Babbush model [B46]).** For a coarse-grained protein Monte Carlo step:
  - quantum oracle ~10⁵ Toffolis (t_Q ≈ 17 s) vs a classical step of ~1 µs;
  - break-even T* ≈ 9 years on one core, or ~9,000 years against 10³ cores;
  - it would need σ/ε ≳ 10⁴ for estimation;
  - protein decisions need σ/ε ≈ 10–10².

### CA-5. Loading and state preparation erase speedups
- Grover–Rudolph loading gives no quantum Monte Carlo speedup, and this is a theorem [B37].
- Conformational Boltzmann laws lack integrable marginals [B36].
- Learned loaders add bias and uncounted training cost [B40].
- General qsampling is SZK-hard [A11].
- Active QRAM erases most asymptotic advantage [F56]. The caveats of HHL-type algorithms are in [F51].

### CA-6. Dequantisation
- Low-rank quantum ML and linear-algebra speedups collapse to polynomial under ℓ²-sampling access [F52–F54].
- Constant-precision QSVT is dequantised [F55].

### CA-7. Classical baselines in positive quantum claims are usually weak
- **Annealing.** Advantages over SA dissolve against SQA, cluster algorithms, exact solvers, PT-ICM, population annealing or SBM [C38–C43, C45, C52, C78, C79].
- **Quantum-enhanced MCMC and fully-quantum walks.** Compared against local or uniform Metropolis, not PT [A46, A47].
- **QFold.** Compared against matched Metropolis only [A65].
- **Hybrid LABS work.** The benchmark's own abstract reports classical solvers that "matched or exceeded" the quantum results [C37].
- **Quantum ML.** Classical models outperform quantum classifiers on systematic benchmarks [F81].

### CA-8. "Beyond-classical" claims keep falling
- **Rebutted:**
  - Sycamore 2019 [F1] fell to tensor networks [F4, F5, F7];
  - IBM 2023 utility [F18] was reproduced at laptop scale [F19–F21, F23];
  - Gaussian boson sampling was spoofed or reproduced [F15–F17].
- **Contested:** D-Wave 2025 [F26] vs [F27, F28], with a reply [F29].
- **Standing:** only the 67-qubit random-circuit sampling [F9] and Google's OTOC(2) [F30]. Neither computes anything protein-relevant.

### CA-9. Protein landscapes are funnelled and classical samplers are strong
- **Landscape theory.**
  - Minimal frustration and funnels [E2–E5].
  - Lattice Monte Carlo folding time is **polynomial**: ~N⁴ for designed and ~N⁶ for random sequences at the optimal temperature [E6].
  - Physical folding has a speed limit of ~N/100 µs [E9].
- **Classical sampler scaling.**
  - PT turns energetic barriers from exponential to polynomial in barrier height (Machta) [E33].
  - Replica count grows only as √N [E23, E28].
  - HMC needs O(d^{1/4}) steps [E51 = A75].
  - REST2 removes the solvent dependence [E47].
- **Rare events.** WE, TPS and MSMs remove the exp(ΔG‡/kT) waiting-time factor [E60, E62, E63, E67].
- **Learned samplers.**
  - Learned-proposal and SMC-corrected samplers are exact [E77, E79].
  - BioEmu is approximate: about 4 minutes per 1,000 samples at 100 aa on one GPU, scaling roughly as L² [E83 = A79].

### CA-10. Structure beats unstructured search
- Rotamer packing is NP-hard in the worst case [C81] but solved exactly in practice by cost-function networks [C82] and tree decomposition [C83].
- HP lattice folding is NP-complete [C80, E12] but solved by CPSP [C85], PERM [C84, E53], and Wang–Landau up to 500-mers [E56].
- A speedup relative to Grover, or to the naive search tree, is irrelevant when the classical algorithm exploits structure.

### CA-11. Energy validity precedes speed
- A cost Hamiltonian for small peptides "is not correlated well enough to the actual error to provide meaningful predictions" [A72]. This is independent confirmation of the S29–S33 condition-C result.
- No sampler or optimiser, quantum or classical, fixes an energy whose low states are not better structures.

## Part 2. Strongest counterargument per candidate

| Candidate (map id) | Strongest classical counterargument | Key refs |
|---|---|---|
| Walk / QSA posterior sampling (AA-1, SP-1) | Quadratic gain vs ~10⁷–10¹⁰ per-step overhead. Crossover needs ≳10¹²–10¹⁵ classical steps per independent sample (I(prog) [A §3.9]), against PT/HMC/SMC/learned-proposal samplers that scale polynomially on funnelled landscapes. The cold-start √N penalty applies without a gapped warm path. | CA-1, CA-9; [A9, A56, E33] |
| Continuous QSVT / quantum RELD sampler | The separation is proven only on hide-and-seek narrow-well instances. Whether learned protein energies have such wells is unknown, and funnel theory suggests they do not. The gain is quadratic, query-only, and assumes a warm start. | [A44, A45, E2–E6] |
| Amplitude estimation of ensemble averages (QA-1) | Estimation is bias- and mixing-limited, not variance-limited. MBAR is optimal. Break-even needs σ/ε ≳ 10⁴. | CA-4, CA-5; [B37, B71] |
| Quantum partition functions | These are only the √δ factor. Protein partition-function incumbents (K*, CFN counting) are deterministic, not MCMC. | [B75, B76] |
| Rare-event hitting-time speedup | WE/TPS/MSM already remove the waiting-time exponential. Kinetics are outside the structure endpoint. | [E60, E62, E63, E67] |
| Grover / minimum finding / amplitude-amplified restarts (AA-2) | Restart saturation at 32–64 restarts (S33) gives at most ~8× fewer calls, each needing a reversible decoder. Quadratic speedups do not pay under fault tolerance. | CA-1, CA-10; [C64, C65] |
| Backtracking / B&B for rotamer, contact or branch problems (QA-4, C-4) | Exact classical solvers shrink the tree through structure. The CSP advantage "disappears" with decoder costs. C-4 is discrimination-limited at short length. | [C63, C82, C83, C85] |
| QAOA / VQE / CVaR / annealing on lattice or register energies | Locality, trainability and noise limits. The weak-baseline pattern. The S29–S33 null (33 experiments). Proxy energies fail condition C. | CA-2, CA-3, CA-7, CA-11 |
| Quantum generative models as priors or samplers | Data-processing inequality. Trainable implies surrogate. Born-rule hardness is irrelevant to sampling a specified π. | CA-3; [F81, F88–F91] |
| Electronic structure for structure accuracy (AA-3) | Energy accuracy is not the structure bottleneck (S29–S33). No generic exponential advantage [F64]. ML potentials reach ab-initio quality for proteins [F73, F74]. | [F61–F65] |
| QSVT/HHL readouts (AA-4) | Millisecond classical problems. Dequantisation. QRAM cost. | CA-5, CA-6 |
| Beyond-quadratic walk claims | Exponents fitted at n ≤ 10 against local Metropolis, with no PT baseline. | [A46, A47] |

## Part 3. The classical-first filter

A candidate is marked **KILL** if any of K1–K5 holds and nothing in the literature or S29–S33 evidence overrides it. It is marked **SURVIVES FILTER (conditional)** only if every condition in S1–S4 can be tested classically before any quantum work.

- **K1. Reduction.** The quantum output is consumed through an argmin, an energy-order prefix or a convex functional of a diagonal-energy distribution. This is the H-001 class (S29–S33 R1–R12; [C22, F37, F91] as general forms).
- **K2. Classical saturation.** The subproblem is already solved exactly, or saturated, at the relevant sizes: enumeration, dynamic programming, restart saturation, exact solvers [C82, C83, C85, E56].
- **K3. Information limit.** The endpoint is shown to be information-limited (S29–S33 I-1 … I-6; AF2's MSA dependence [E89]; fold-switch memorisation [E100]).
- **K4. Wrong factor.** The speedup acts on a cost factor that is not binding: variance where bias or mixing dominates (CA-4); search where discrimination dominates.
- **K5. Overhead.** The speedup is quadratic or smaller, and no plausible classical cost at the relevant size exceeds the fault-tolerant break-even (CA-1).

**Conditions for survival (all must be classically testable):**
- **S1.** The subproblem's cost for the *best* classical portfolio has been measured, or can be measured, to grow steeply with size.
- **S2.** Better solutions to the subproblem improve the endpoint (condition C / transmission).
- **S3.** A quantum primitive with a known separation applies, and its oracle is native-free and coherently implementable.
- **S4.** A break-even criterion is stated in advance.

**Result of the filter** (details in `OPPORTUNITY_MATRIX.md`):
- **One candidate survives, conditionally:** walk / QSA / continuous-sampler acceleration of learned-energy posterior sampling at ≥60 aa. It passes K1 (whole-distribution soft readout), K3 (sampling is not information-limited if the energy is taken as given) and K4 (mixing, not variance). It is **unresolved** on S1 (never measured), S2 (partially: 1.40× MDE at mid30) and K5 (break-even unknown).
- **All other candidates are KILLED or WEAK.**
