_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s32/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 32: results touching the quantum component (CVaR-VQE and its reformulations)

Lane Q ("QUANTUM / CVaR-VQE REFORMULATION") owned this question under prereg `s32/PREREG_S32_Q.md` @ `a8f9d6a7`. Its derivations are in `s32/THEORY_Q.md`, and its ledger entries are S32-L5 and S32-L(Q1)–L(Q3) in `s32/LEDGER.md`.

Scope:

- No new quantum circuit was run in S32, so there is no FULL-vs-ablation or classical-twin circuit comparison this sprint.
- Lane Q's registered scope said: "Optimiser, depth, iteration or ansatz tuning (charter §36) — no objective in this lane has endpoint evidence yet, so none of it is in scope" (`s32/PREREG_S32_Q.md`).
- Q0 used "the exact hinged-Gibbs minimiser, since S31 proved the circuit is strictly worse 126/126 and the circuit adds only optimisation noise" (`s32/PREREG_S32_Q.md` Q0-H3).

## Resource and implementation facts, as the source states them

| item | as recorded | source |
|---|---|---|
| register / field of view | the top-128 score prefix, "**128 = 2⁷, the VQE register width**", which `s29_O_ladder.py` calls "the quantum field of view" | `s32/REPORT_S32.md` §2.1; `s32/CAUSAL_MAP.md` arrow 2 |
| is the quantum stage on the deployable path? | "**the 128 window does not exist on the deployable path** (`want = max(m, 128 if quantum else 0)`, and production is `quantum=False`)". The deployable filter is 500→75 | `s32/LEDGER.md` S32-L(P1); `s32/PREREG_S32_P.md` §0 |
| deployed Hamiltonian | `E = _zrank(pool["sc"][o])` (`core/pipeline.py:863`), diagonal, candidate-index | `s32/PREREG_S32_Q.md` Q0 |
| optimisation argument list | `(E, α, T, n, layers, iters, seed)`. `(α,T)` "takes exactly two values over the whole instrument, selected by fold". Deployed `α = 1, T = 0.3` | `s32/THEORY_Q.md` Q0-H2; `s32/PREREG_S32_Q.md` Q0-H3 |
| qubits (numeric), circuit depth, layers, shots, hardware vs simulator, evaluation budget | not recorded in source for S32 | — |
| wall time | not recorded in source for any quantum arm. The QP solver is described as "milliseconds, with a KKT certificate" | `s32/THEORY_Q.md` Q1-T3 |
| convex readout solver | Lawson–Hanson NNLS on the sum-to-one-augmented system, KKT certificate 2.0e-12. It replaced a 4000-iteration FISTA with drop-only polish, which failed its certificate (1.26 at K=128, 10.85 at K=500) | `s32/LEDGER.md` S32-L(Q1) |
| "tail collapse" | term not used in S32 sources | — |

---

## QR-1. Q0: audit of S31's target-invariance claim for the deployed CVaR-VQE Hamiltonian
- **Measured:** real 126 pools plus two synthetic self-tests.
  - Self-tests: a deliberately tied vector gives max deviation 0.1221; a deliberately unsorted vector gives 3.3830; a sorted distinct vector gives 0.0.
  - `sc[o]` is non-decreasing on 126/126. 125/126 targets have ≥ 1 tie in the top-128. `E` is exactly the ramp on 1/126.
  - max |E − ramp| = 0.0406840 (S31 quoted 0.0407). Block model error 0.0e+00 on 126/126.
  - Price at the deployed (α,T), CA cloud: `Q0_TIE − Q0_RAMP` +0.0000, 0.26×, 70/55/1. Selection readout "identically tied on every target" (0/0/126). `Q0_PERM` (blocks relocated, 8 draws) +0.0004, 0.38×.
  - TV(p*_tie, p*_ramp) 3.3e-03 mean. Selected medoid identical on 126/126.
  - Source: `s32/THEORY_Q.md` Q0; `s32/results/s32_Q0_invariance.json` (cmp_cloud effect_over_mde 0.25546; cmp_perm 0.38062; cmp_sel nan).
- **Original interpretation:** "S31 §5.1 is NOT falsified, and is now sharper." "The deployed Hamiltonian is a **global 128-number hyperparameter plus one integer per target**." "The residual channel is the existence of duplicates, not which candidates duplicate: one integer per target."
- **Status:** confirmed S31. The registered falsifier (≥ 1.0× MDE) did not fire.
- **Leakage:** the Hamiltonian is native-free. The pricing arm is evaluated with ORACLE RMSD on the cloud.

## QR-2. Q1-T1: the CVaR readout's quality vector `a` and the common mode `μ` are one object
- **Measured:**
  - Identity `‖U'w − t‖² = ⟨w,a⟩ − ½w'Bw` verified to 1.1e-11 relative (126 × 80 draws, simplex and signed-affine).
  - `a` affine in `t` to 5.8e-13.
  - Substituting `P_aff{W} t`: max |Δw| 7.0e-12, max Δx 2.9e-12 Å, KKT 2.0e-12.
  - `rank(aff{W})` 32.88 mean (21–42) vs d = 38.88. ‖t − P_aff t‖ = 1.5e-14.
  - Source: `s32/THEORY_Q.md` Q1-T1; `s32/results/s32_Q1_sufficiency.json` (rank_aff_mean 32.881, d_mean 38.881, hull_gap 1.48e-14).
- **Original interpretation:** "the sufficient statistic for the entire sum-to-one readout problem is ≈ 33 real numbers, not 128." "There is one missing channel this project has been describing in two vocabularies." "*This is a closure, not a lead.*" This resolves S31 §20.3.
- **Status:** theorem with a numerical falsifier that "did not fire". Independently re-derived by lane P from the other direction (μ recovered at 2e-14, `s32/MULTIPLICITY.md` P-14). Contract rule 7 is recorded as "satisfied without coordination".
- **Leakage:** `a` and `t` are ORACLE. The bijection itself is native-free.

## QR-3. Q1-T2: the readout (CVaR objective's weight program) is a hull projection with gain exactly 1 / 0
- **Measured:**
  - Finite differences, n = 126 × 4. Gain along an in-hull direction 0.9999999999 (max dev 1.17e-08). Orthogonal gain 4.01e-09 mean.
  - Support |S| 6.254 mean, window |S|−1 = 5.254. 3 of 126 targets are degenerate with |S| = 1.
  - Step size set by an h-sweep in which the residual "scales as 1/h = roundoff".
  - Hull floor d = 1.8290 ± 0.1178 (CA cloud, Kabsch). The fixed-frame value in the artefact is 1.8549. Crossover against direct emission ε ≈ 2.2.
  - Source: `s32/THEORY_Q.md` Q1-T2; `s32/MULTIPLICITY.md` Q-5; `s32/results/s32_Q1_sufficiency.json`.
- **Original interpretation:** "A structure estimate good enough to make the readout worth solving is already good enough to emit." S31's measurement that solving the CVaR objective exactly "reshuffles the answer on 66 of 126 targets and buys nothing" (−0.0112 Å, 0.19× MDE) "is forced" (`s32/REPORT_S32.md` §3.1).
- **Scope limits the source states:**
  - Σw = 1 is assumed.
  - There is no binding cardinality constraint.
  - The output lies in the affine hull.
  - The frame is fixed.
  - "'Gain exactly 1' is a statement about the CA POINT CLOUD and must not be carried to the built chain" (`s32/THEORY_Q.md` "Scope").
- **Status:** theorem holds. The auxiliary claim "gain exactly 1 means no noise suppression" was **STRUCK** (gain 0 on ≈33 dimensions is "TOTAL suppression"). The closure now rests "on the LOWER bound".
- **Leakage:** ORACLE / NOT DEPLOYABLE for every Ångström figure.

## QR-4. Q1-T3: sparse s-of-K subset basis (the last CVaR-VQE formulation standing)
- **Measured:**
  - Support of the unconstrained convex optimum over K=500: s* mean 10.06, median 10, min 3, p90 13, max 23.
  - 61.1% of targets have s* ≤ 10; 98.4% have s* ≤ 20.
  - Emitted value 1.1535 ± 0.0669 (CA cloud), deliberately "NOT differenced" against the 1.1139 built-chain figure.
  - Source: `s32/LEDGER.md` S32-L(Q1); `s32/results/s32_Q1_sufficiency.json` (k500_support_mean 10.056, frac ≤ 10 0.611, k500_kabsch_mean 1.1535).
- **Original interpretation:**
  - It "escapes all three of S31's obstructions":
    - the subset basis is diagonal;
    - `⟨E⟩` is linear in p because the weights are solved classically inside `E(x)`;
    - the dimension is `2^K` not `K`.
  - "**All three of S31 §5.2's obstructions are properties of the CANDIDATE-INDEX REGISTER, not of CVaR-VQE.**"
  - It is then closed "by monotonicity": `f*(s)` is constant for s ≥ s* and strictly worse for s < s*. "**The hard instances are exactly the ones whose optimum is worse. A quantum solver could only ever be needed to compute an answer a convex program already beats.**"
- **Status:** closed by derivation. The source says the closure "does not depend on where `s*` falls".
- **Leakage:** `E(x)` needs `a`, which is ORACLE. Condition B fails.

## QR-5. Objective A: CVaR over a posterior on candidate quality
- **Measured:** derivation only (the charter's 15-item table).
- **Original interpretation:** "Gaussian π ⇒ ⟨w,â⟩ − ½w'Bw + φ(α)√(w'Σw) = a second-order cone program: convex, unique optimum, milliseconds. CLOSED." The closure is described as stronger than "a circuit is unnecessary", because the program "inherits its input's error at gain exactly 1" (`s32/THEORY_Q.md` Q2).
- **Status:** closed by classical equivalence (charter §16 item 13).

## QR-6. Objective B: reconstruction branch selection as a CVaR decision
- **Measured:** formulation only in lane Q.
  - Branch census from lane R: 126/126 targets have ≥ 2 distinct branches, median 149 of 158. The λ=0.3 objective gap is below 1e-3 on 102/126. Spread > 0.3 Å on 86 targets (`s32/LEDGER.md` S32-L(R4)).
  - Production's argmin is about a coin (QR-9, NEGATIVE_RESULTS N-R7).
  - No native-free selector reaches MDE (NEGATIVE_RESULTS N-R3, N-R4).
- **Original interpretation:** per-target with a handful of values, "CVaR adds nothing over argmax for a fixed, known energy vector". It "earns a circuit iff the branch variable is PER-RESIDUE and the energy is non-separable across residues", giving `2^{n_res}`. At n_res 9–16 that is enumerable (`s32/THEORY_Q.md` Q2 Objective B).
- **Status:** "argmax in quantum notation" (per target). "blocked ONLY by chain length" (per residue). The diagnostic lane Q handed to lane R ("do they differ at a sparse set of residues or globally?") has no reported answer in the S32 sources.

## QR-7. Q3: non-diagonal Hamiltonians / S31's obstructions re-examined
- **Original interpretation:**
  - Obstruction 1 (per-shot energy) and obstruction 3 (dimension counting) are "properties of the candidate-index register, not of CVaR-VQE". Both are escaped by changing what a basis state means (subset or per-residue basis).
  - Obstruction 2 (quartic in ψ) is escaped "by solving the continuous part classically inside a diagonal `E(x)`".
  - The family is "**reopened** on that mechanism — and then closed again, one level down, by Q1-T1… and Q1-T3".
  - "The closure moved from 'a circuit cannot be built' to 'a circuit can be built and there is nothing for it to compute'" (`s32/THEORY_Q.md` Q3).
- **Status:** reopened, then closed by derivation. No experiment.

## QR-8. Q4: the five-bit result re-priced in real numbers
- **Measured:** ORACLE / NOT DEPLOYABLE, CA cloud, n=126. Emitted RMSD vs r retained principal directions of the pool's own spread:

  | r | emitted RMSD |
  |---|---|
  | 0 | 3.0532 |
  | 1 | 2.5804 |
  | 3 | 2.2638 |
  | 6 | 2.0312 |
  | 10 | 1.9110 |
  | ~33 | 1.8290 |

  Source: `s32/THEORY_Q.md` Q4; `s32/MULTIPLICITY.md` Q-7.
- **Original interpretation:** "Six real numbers buy 83% of what all thirty-three buy." "A bit count prices a selection alphabet; this decision is continuous, so the two are never differenced." On amplitude encoding: "representational capacity was never the binding constraint: the numbers required are the native's coordinates in the pool's basis, and no encoding manufactures them."
- **Status:** registered pricing curve. ORACLE ceiling. The falsifier (curve flat until r ≈ 33) did not fire.
- **Leakage:** coefficients are ORACLE. The direction ordering is native-free "and it is the part that is worth nothing on its own".

## QR-9. Charter §14 answered: conditions A–E and properties P1/P2
- **Measured:** n_res 9–16, mean 12.96, so `2^n_res ≤ 65536` on 126/126 targets (`s32/THEORY_Q.md`; `s32/LEDGER.md` S32-L(Q3)).
- **Decision table as recorded:**

  | decision | A | B | C | D | E | verdict |
  |---|---|---|---|---|---|---|
  | candidate index (deployed) | no | no | – | no | no | "dead 4 ways" |
  | subset / sparse s-of-K | YES | no | yes | no | no | constraint slack, objective ORACLE |
  | recon branch, per target | no | yes | open | no | no | "argmax in quantum notation" |
  | recon branch, per residue | no* | yes | open | no* | no | "blocked ONLY by chain length" |
  | fragment assembly | YES | yes | yes | YES | no | "does not exist at this length" |

- **Original interpretation:**
  - "**P1 — the decision space must GROW WITH THE TARGET**… **P2 — the energy must be GENUINELY STOCHASTIC**… **P1 and P2 must hold TOGETHER**… This project has never had either."
  - P1 alone "is QAOA and not CVaR-VQE". P2 alone is "a one-dimensional classical rule".
  - Charter §34 (CVaR of free energy) is "the one place this could be met, and it is met by the **sampling**, not by the physics vocabulary."
  - The lane "does NOT say" the quantum stage should be deleted; "that is the coordinator's call".
- **Status:** "The answer on `tuning126` is no, by derivation rather than by exhaustion." The report frames the long-protein test as "a DERIVED REQUIREMENT" (`s32/REPORT_S32.md` §6, §7). A quantum test at length was not run in S32.

## QR-10. Hull projection of a noisy external structure estimate (candidate readout for a future channel)
- **Measured:** ORACLE / NOT DEPLOYABLE, CA cloud, n=126, 8 draws per level.

  | ε | PROJ − SHRINK | × MDE | verdict |
  |---|---|---|---|
  | 0.5 | +0.370 | 4.71 | WORSE |
  | 1.0 | +0.265 | 3.17 | WORSE |
  | 1.5 | +0.170 | 1.96 | WORSE |
  | 2.0 | +0.077 | 0.89 | NOT MEASURED |
  | 2.5 | −0.001 | 0.01 | NOT MEASURED |
  | 3.0 | −0.066 | 0.77 | NOT MEASURED |
  | 4.0 | −0.137 | 1.59 | better, 86W/40L; median −0.074 |

  SPAN ≈ DIRECT at every level (`s32/LEDGER.md` S32-L(Q2); `s32/THEORY_Q.md` "The near-miss").
- **Original interpretation:** "The hull is a shrinkage." The isotropic error model is "an upper bound obtained under an error direction no real estimator has". Realising it needs "a native-free external structure estimate… the same missing channel".
- **Status:** "The control fired and killed the arm."

## QR-11. What CVaR-VQE contributed to the endpoint in S32
- **Measured:** no CVaR-VQE arm reached the built chain. Production is `quantum=False` (resource table above).
- **Original interpretation (REPORT §0.5):** "**The last formulation standing, sparse `s`-of-`K`, escapes all three of S31's obstructions and then falls to monotonicity: *the hard instances are exactly the ones whose optimum is worse.***"
- **Next-sprint direction (REPORT §10 item 1):** "Go longer… the quantum question fails on `2^n_res ≤ 65536`… At 54.7 residues `3n ≈ 164`, both change." The `long40` instrument exists (45 targets). The source does not record a quantum arm on it.
- **Status:** answered "NO on this instrument". Endpoint contribution: none measured.
- **Leakage:** n/a.
