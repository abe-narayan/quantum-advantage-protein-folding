_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s31/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 31: quantum-component results

This file covers every result in `s31/` where a quantum component was tested or characterised: the CVaR-VQE objective, the Hamiltonian, the ansatz, the qubit and index encoding, the quantum readouts, FULL-vs-classical-twin substitutions, and resource figures. Positive, negative and null results are all included. The per-item format follows the import rules.

---

## 0. Resources and configuration, as the source states them

- **Deployed stage:** `core/pipeline.py:806-877`. It takes the top `2^k` candidates by score, builds a diagonal H from standardised score ranks, and minimises a CVaR free energy "over a 9-qubit (deployed: **7**-qubit) RY/CNOT statevector circuit" (`s31/REPORT_S31.md` §4).
  - `cfg.vqe_qubits = 7`, so D = 128 (`s31/PREREG_S31_A.md` §0).
  - The charter's 0.2516 / 3.4330 Å figures come from a 9-qubit, depth-3 harness circuit (`s31/BRIEF.md` §5E).
- **Ansatz:** "`layers × (RY on every wire, CNOT chain + ring)` on a real statevector (`core/quantum.py:818-895`), `n = 7`, `layers = 3`, **21 parameters** against a 127-dimensional simplex" (`s31/THEORY_A.md` §6).
- **Deployed optimiser settings:**
  - `run_cvar_vqe(E, alpha, T, n=7, layers=3, iters=50, seed=0)`, i.e. `Config.vqe_layers=3, vqe_iters=50, vqe_seed=0, vqe_qubits=7` (`s31/PREREG_S31_P.md` §3).
  - Lane L describes "the shipped `run_cvar_vqe` at its deployed settings" as "layers 3, iters 80, restarts 1, exact parameter-shift gradient" (`s31/LIT_L.md` L1.1). This conflicts with iters=50; see LESSONS.md, importer notes.
- **(α, T):** `VQE_LFO = {0:(1.0,0.3), 1:(0.25,0.3), 2:(0.25,0.3), 3:(1.0,0.3), 4:(1.0,0.3)}` (`core/pipeline.py:113`). T = 0.3 on every fold and α = 1 on 3 of 5 folds.
- **Simulator vs hardware:** exact statevector simulation throughout. No hardware run is recorded. **Shots: not recorded in source** (exact probabilities are used).
- **Production state:** `quantum: bool = False` in `PROD = Config()`. "the 3.2105 Å endpoint is produced with the stage **off**" (REPORT §4).
- **Wall time:**
  - p* takes 0.0012 s against 0.0985 s for `run_cvar_vqe` per target, i.e. 82× (S31-L20 §1).
  - layers=12, 400 iters, 8 restarts takes "~60 s" and is still short of p* (LIT_L L1.1).
- **Gradient scaling:** `Var ~ 16/D = 16·2^(−n)`: n=7 → 0.125, n=9 → 0.031, n=12 → 0.0039. The source identifies this with the Cerezo et al. global-cost barren plateau. Caveat as stated: "at n = 7–9 we are **not yet gradient-limited**" (LIT_L L1.4).

---

## Q1. Closed-form global minimiser of the deployed CVaR free energy (Theorem, lanes L and A)

- **Measured:**
  - `F(p) = CVaR_α(E;p) − T·H(p)` is convex. Its minimiser is `p*_i ∝ exp((s* − E_i)_+/(αT))`, pinned by one scalar.
  - Synthetic check (12 cells, n ∈ {7,9}, α ∈ {0.1,0.25,1.0}, T ∈ {0.1,0.05}): strong duality holds to 1e-9…1e-16; mirror descent agrees to ~1e-5; the circuit is strictly worse in 12/12 with F-gap +0.0186 to +0.2368 and TV 0.246–0.962 (`s31/LIT_L.md` L1.1, `s31/LEDGER.md` S31-L4).
  - Real instrument at deployed settings, n = 126: duality gap 3.560e-09; KKT 2.665e-15; mirror descent never below p*; the circuit is strictly worse on 126/126 with F gap mean +0.1937 and TV mean 0.378 (S31-L20 §1, `s31/results/s31_P_substitute.json`).
  - Lane A derived the same law independently by KKT. `F(closed) ≤ F(numeric)` holds at +1.8e-15, and at α = 1 the result agrees with Boltzmann to 1.4e-15 (THEORY_A §1).
- **Leakage:** p* is native-free / deployable (PREREG_S31_P §2).
- **Original interpretation:** "CHARTER §11 IS CLOSED FOR THE DEPLOYED OBJECTIVE. The shipped CVaR-VQE is a lossy approximate solver for a convex program that has an analytic solution. No interference, spectrum or entanglement is doing anything. Whatever it contributes, it contributes BY FAILING TO OPTIMISE." (STATE NOTE 5).
- **Status:** confirmed and derived twice. Lane A's registered A1-v clause was "REFUTED AS WRITTEN" because the statistic measured the reference solver, not the closed form.

## Q2. Circuit vs optimum: expressivity gap, not optimiser gap

- **Measured:**
  - KL(p_θ‖p*) is 0.930 bits mean (median 1.298, p90 1.303) and TV is 0.378 (`s31/results/s31_A_r1.json`: 0.93023).
  - 80 → 2000 Adam iterations move the synthetic gap from 0.025764 to 0.025944 at α = 0.1 and from 0.233580 to 0.233116 at α = 1.0.
  - Depth and restarts do close it: layers 12 / 400 iters / 8 restarts gives +0.0042 / +0.0176, TV about 0.10 (LIT_L L1.1).
- **Interpretation:** "21 parameters cannot cover a 127-dimensional simplex."
- **Status:** A1-e (KL < 0.10) is FALSIFIED about 10×. The readout half of A1-e (< 0.02 Å) HELD: −0.0044 Å cloud, 0.09× MDE, while per-target |Δ| is 0.102 Å. "The optimisation gap is real and cancels in the mean."

## Q3. Target-independent Hamiltonian (S31-L17; lane P, verified by the coordinator; audited by lane V D6)

- **Measured:**
  - `E = _zrank(pool["sc"][o])` on a sorted slice gives the standardised rank ramp [−1.718572 … +1.718572].
  - On real scores: 125/126 targets carry ties; 1/126 is exactly the ramp; tied positions have mean 9.56 and max 34; max |E − ramp| is 0.0407; the max between-target deviation is 0.0812; distinct structures have mean 118.45 and min 94 (`s31/AUDIT_V.md` D6; `s31/results/s31_V_zrank.json`: 0.04068, 0.08123).
  - H(p*) is 4.9137 bits at α=1 with sd 3.1e-4, and 6.6392 at α=0.25 with sd 4.6e-3 (S31-L20 §5). S31-L17 gives 4.9136 with sd 1.4e-4.
  - ESS(p*) is 22.19/128 at α=1 and 58.32–58.34 at α=0.25.
- **Leakage:** native-free (E depends on the score order only).
- **Original interpretation:** "The quantum stage carries ZERO target-specific information" (S31-L17). The revised form reads "target-independent to within a measured bound … one fixed weighting curve per α" (REPORT §5.1). "The stage answers 'what fixed weight should rank `k` receive?', which is a 128-number global hyperparameter, not a per-target computation."
- **Status:** the algebra was confirmed by lane V. The original verification (three synthetic vectors) "was structurally incapable of testing its own caveat". "Zero" was revised to a measured bound, and the conclusion is unchanged.

## Q4. The p* substitution at the endpoint (lane P; the "decisive experiment")

Built chain, n = 126. All arms were projected in one process from one cache. Arm A reproduces 3.2105 with a worst per-target deviation of 0.0000. CA cloud values are in brackets.

| arm | built chain ± SE | [cloud] |
|---|---|---|
| A quantum OFF (production) | 3.2105 ± 0.1540 | [3.0483] |
| A2 same operator recoded | 3.2108 ± 0.1542 | [3.0483] |
| B selection, VQE p | 3.3117 ± 0.1648 | [3.3135] |
| C selection, p* | 3.2838 ± 0.1586 | [3.2852] |
| D convex, VQE p (SHIPPED quantum arm) | 3.2281 ± 0.1558 | [3.0661] |
| E convex, p* | 3.2169 ± 0.1526 | [3.0605] |
| F convex, uniform p (shipped ablation) | 3.2415 ± 0.1528 | [3.0532] |

- **Contrasts** (S31-L20; REPORT §14.1; `s31/results/s31_P_substitute.json`):
  - P1 = E − D: −0.0112 (0.19×), NULL.
  - P2 = C − B: −0.0280 (0.29×), NULL.
  - S3 = D − A: +0.0175 (0.35×), NULL.
  - F − A2 widening: +0.0307 (0.42×), NOT A RESULT.
  - B − A: cloud +0.2652 (2.15×, MEASURED worse); chain +0.1012 (0.93×, NOT MEASURED).
- **Per-target spread vs the A2 implementation-noise null:**
  - P1 |d| mean 0.1432, p90 0.3706, max 1.1457; 100/126 above 0.0107.
  - A2 − A: mean 0.0134, p90 0.0329, max 0.2285.
  - P2 changes the selected medoid on 66/126 targets (54/78 at α = 1, 12/48 at α = 0.25).
- **Leakage:** all arms native-free except the RMSD scoring.
- **Interpretation:** "Solving the objective exactly reshuffles the answer everywhere and buys nothing." The scope caveat: "Both substituted arms are target-independent rank curves… This experiment does not test whether a better objective would help, and must not be recorded as evidence either way." It is also "not reachable" as a test of S20's law (S31-L20 §7).
- **Status:** NULL. Lane L's dichotomy ("no third outcome") is falsified. Lane P's prediction that "E lies between D and F" is falsified because its premise reverses at the deployed T: at α=1, H* = 4.9137 vs circuit 5.6738, so "the circuit is MORE entropic than the optimum".

## Q5. The readout-capacity claim R1 and realised capacity

- **Measured:**
  - The selection readout `argmin(P·p/Σp)` has reachable vertices of 118.45 mean and 94 min, equal to the byte-distinct count on every target.
  - Capacity is 6.886 bits mean and 6.555 worst (`s31/results/s31_A_cap.json`: 6.88616).
  - The shipped convex readout emits structures 1.1144 Å mean (min 0.0730) from the nearest pool member.
  - ORACLE bits delivered: p_θ medoid 1.805, p* medoid 1.876, score argmin 1.693, uniform medoid 1.659.
  - The stage moves the selection on 77.8% of targets and delivers 0.112 bits over the argmin, which is 1.6% of the alphabet (THEORY_A §7.2; S31-L13 §4).
- **Leakage:** ORACLE / NOT DEPLOYABLE for "bits delivered".
- **Interpretation:** the final form of R1 is "the SELECTION readout's alphabet is the number of distinct candidates — 6.886 bits mean, 6.555 worst — and it is a scored diagnostic arm (`rmsd_vqe_sel`, `:1173`, registered `:1609`), not the answer path."
- **Status:** R1's quantifier was falsified by lane C in shipped code (`average_weighted`). Point 4 (all 2^k reachable) was falsified by lane A. The theorem "has been true at every restatement and about something smaller each time" (S31-L1 annotation 2). Two capacity values circulated, 6.888 and 6.886; lane V D8 resolves this in favour of 6.886 as the mean of logs.

## Q6. Three readouts, and "expressivity without an aligned objective is harmful"

- **Measured:**
  - The affine harness readout (`s27/s28_A_amp.py`, signed amplitudes) gives 0.2516 Å under an ORACLE objective and 3.4330 Å under the deployed objective, against the uniform average's 3.2071 (S31-L2).
  - The affine hull's ORACLE ceiling is exactly 0.0000 on all 126 targets: rank(aff{W_x}) is 32.9 ≥ 3n−3, median ess 1.13, neg_mass 3.38 (THEORY_A §3.2; S31-L14 §4).
- **Interpretation:** "'0.2516 Å under an ORACLE objective' is a statement about a REGULARISER, not a class ceiling — and the simplex constraint is precisely the regulariser the uniform average enjoys for free" (REPORT §10.5). The charter's premise "the circuit can express good solutions" "rests on numbers from the **affine harness** readout, while a deployable quantum stage would use the **convex** one" (REPORT §4).
- **Status:** "Two readouts" (S31-L2) was retracted to "three". The +0.2260 Å parity deficit was retracted because it was the affine readout's cost.

## Q7. Ansatz inductive bias

- **Measured:**
  - Schmidt ranks across the six cuts are 2, 4, 8, 8, 4, 2: "an MPS Born machine of bond dimension exactly `2^layers = 8`".
  - R² of log p on the hinge shape: random θ 0.0071; best of 400 draws 0.0538; optimised p_θ 0.467; popcount alone 0.122; hinge + popcount 0.483.
  - Entropy at random θ is 4.889 bits (THEORY_A §7.5).
- **Interpretation:** "a ceiling at about half the right shape, not a bias toward anything structural." Lane L adds: "Even the escape hatch is classical" (MPS Born machine, Han et al. PRX 8:031012).
- **Status:** lane A's popcount-basis explanation was REFUTED by its registered relabel (KL 0.967 vs 0.930; −0.0031 Å at 0.060× MDE).

## Q8. Entropy collapse and α

- **Measured:**
  - At T = 0 with 8 seeds per target: entropy 0.258 bits at α = 1 (78 targets) and 3.596 bits at α = 0.25 (48). The seed sd of cloud RMSD is 0.1634 / 0.1599 Å.
  - A1-d: T=0 seed sd is 0.162 (> 0.15, HELD). At deployed T the seed sd is 0.096, against a registered < 0.05, REFUTED 1.9× (THEORY_A §7.6, §8).
  - Lane L synthetic (n=7, T=0.1): the objective asks for 2.310 → 4.685 bits across α and the circuit gives 0.671 → 4.548. Lane L reads this as "~60% … real and ~40% is the ansatz amplifying it", with the caveat "synthetic ladder … Indicative, not measured on the instrument" (LIT_L L1.1).
- **Interpretation:** the shipped docstring's "for ANY alpha … a property of CVaR, not of the optimiser" is "false by theorem". At α < 1 "the entropy belongs to the optimiser". The docstring was corrected in place.
- **Related, inherited from S25 via S31-L7:** the CVaR tail's "+0.113 Å measured role" was withdrawn. The paired values are −0.1126 (0.51×) and −0.1405 (0.68×). "no Angstrom effect of that mechanism has been measured."
- **Literature transfer:** Kolotouros & Wallden's Ascending-CVaR: "alpha is a homotopy parameter in the literature and a shape parameter here". Ranked below the p* substitution (LIT_L L1.2).

## Q9. Non-diagonal Hamiltonians: no quantum mechanism available (theorems A2, A3 and lane L)

- **Content:**
  - (N1) computational-basis energies reduce to the diagonal case.
  - (N2) spectral CVaR gives a "generalised prefix theorem". The relative-phase fibres are "exactly the ones the objective is blind to and the readout consumes".
  - (N3) the VMC local energy is "not a measurement of an observable".
  - A3 forces `H[w] = diag(â) − B`, which is mean-field, quartic in ψ, with "no per-shot eigenvalue".
  - Dimension counting: "No Hamiltonian on a candidate-index register can be classically hard". The assignment encoding would need 128 qubits and is "already beaten by Frank–Wolfe"; the cited clustering literature shows no advantage at 175 points on D-Wave (THEORY_A §2–3, §5; LIT_L L1.3).
- **Status:** CLOSED by derivation, no compute.

## Q10. Classical-reducibility burden (charter §11), discharged by lane A

- **Content:** the classical algorithm and cost for each construction (THEORY_A §5):
  - deployed CVaR − T·H optimum: one bisection, O(D log 1/ε), microseconds;
  - T = 0 case and any diagonal H: a sort, O(D log D);
  - non-diagonal H on a candidate register: `eigh`, O(D³), about 1 ms at D = 512;
  - mean-field `diag(â) − B`: Frank–Wolfe/FISTA, O(D²) per iteration;
  - readout ORACLE ceiling: QP or lstsq, O(D³).
- **Interpretation:** "Nothing in this lane is a quantum mechanism… the reason is the encoding, not the Hamiltonian." Also: "Classically reducible is not the same as useless."

## Q11. The derived non-diagonal/mean-field objective as a readout (A3 arms; classical twins of the "forced Hamiltonian")

- **Measured**, CA cloud (THEORY_A §7.3; S31-L13; `s31/results/s31_A_readout.json`):
  - CAL − PROD75: +0.1334 (1.17×, WORSE; primary MISSED).
  - GAM: +0.1459 (1.10×).
  - MEB: +0.1436 (1.22×).
  - MEB − argmin: −0.2621 (2.74×). This was killed by shuffled-B at −0.0250 (0.54×).
  - A3-sign: LFO γ > 0 on 5/5 folds, HELD.
  - A3-frame: `Pt` breaks the identity at 2.39% median, HELD.
  - QPORACLE: 1.8290 Å cloud (ORACLE), against a registered < 1.2; A3-oracle REFUTED by 0.63 Å.
- **Leakage:** DEP except QPORACLE (ORACLE).
- **Status:** closed as a deployable readout.

## Q12. Price of the quality estimate `â` through the exact objective (ORACLE sweep)

- **Measured**, cloud: ρ(â, a) 0.118 → 3.170; 0.330 → 2.893; 0.604 → 2.614; 0.853 → 2.332; 0.974 → 2.027; 1.000 → 1.829. The shipped DIS gives ρ = 0.1176. Crossing production needs ρ = 0.211 (THEORY_A §7.4).
- **Status:** the ρ = 0.211 "crossing price" was later withdrawn as a target by its author ("necessary-not-sufficient"). Consensus reaches ρ_global 0.4278 but in-band ρ −0.2837 (S31-L19).

## Q13. Candidate-index encoding and qubit information (lane C, S31-L15)

- **Measured**, CA cloud:
  - Product-state ORACLE ceiling: score map 2.0646; bisect_score 1.9991, which is −0.0655 at 1.34× against a −0.10 bar, F-C2a REFUTED.
  - Gray coding: −0.0014 at 0.03×; the prefix partition is identical on 126/126.
  - Best deployable partial readout: perm, j=2, −0.0160; F-C2b REFUTED.
  - Structure-aware maps raise the ORACLE cell value from 2.4216 to 2.2712 and lower the deployable value from 3.2369 to 3.3721.
  - Bit MI with "ORACLE-best decile": deployed best bit 0.0343, best map 0.0658, perm 0.005.
- **Additional row, ORACLE / NOT DEPLOYABLE:** "Seven qubits read out as a product-state weighted average beat the same seven qubits read out as a selection, by 0.081 A on the deployed index map and 0.147 A on the best one." The product restriction costs 0.26 Å against the unrestricted convex optimum.
- **Interpretation:** "The best available map doubles a quantity that is 0.03 bits." Index redesign is closed.

## Q14. Register widening 128 → 512 (lane C, S31-L5)

- **Measured**, ORACLE / NOT DEPLOYABLE:
  - best1(500) − best1(128) on filter-independent worst18_poolmean: −1.1811 cloud / −1.1762 chain, p = 0.0001 against a random-18 null.
  - FAIL18 = defn18: −1.9004, retired as a near-tautology.
  - Level-control residual: FAIL18 −0.577 vs clean tail −0.196.
  - Rank diagnostic: FAIL18 best member below rank 128 at frequency 1.000 against a 0.744 uninformative null.
  - Source: `s31/results/s31_C_widen.json`.
- **Interpretation:** "It does not say two more qubits are worth 1.18 A… Widening only pays if a selector exists". A cross-lane prediction, labelled and not run, says a deployable arm "should come out WORSE than production". The gradient-variance cost is 4× from 128 to 512.
- **Status:** the gate "REVIVE, at 62% of the published size" as an ORACLE ceiling. The deployable version was not run.

## Q15. The `coh` admission theorem and the quantum readout family

- **Measured**, ORACLE: for any Σa = 1 readout, the common mode passes with coefficient exactly one. Uniform mean in pair space gives coh = 1.0000. The shipped DIS argmin gives 0.8288 and a random member 0.8244 (S31-L10 §4).
- **Interpretation:** "coherence does not vary along the ranking axis at all". This covers the quantum stage's convex and selection readouts, which are Σw = 1 combinations.
- **Status:** the comparison against S30's 0.6931 bar was WITHDRAWN (lane V D0). The theorem stands.

## Q16. Summary statement of record (REPORT §20.4, "What is NOT the bottleneck")

REPORT §20.4 lists the following as not the bottleneck:
- "The circuit's expressivity (`p*` is free and closed-form, and substituting it is worth −0.0112 Å at 0.19× MDE)";
- "the optimiser (80 → 2000 iterations move the gap by nothing)";
- "the CVaR α (inactive by construction on three of five folds)";
- "the ansatz depth";
- "the register width";
- "the index encoding";
- "the readout class".

REPORT §21's recommendation includes: "What NOT to spend the next sprint on — Any further readout, index, ansatz, optimiser, α-schedule or register-width work."
