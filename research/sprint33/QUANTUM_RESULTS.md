_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s33/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 33 — quantum-component results

Every result in the imported sources where a quantum component (CVaR-VQE, ansatz, register/qubit encoding, Born-machine sampler, tempered objective) was tested, positive, negative or null. Per item: **Measured** / **Original interpretation** / **Status in source** / **Resources** / **Leakage**.

Conventions (from `s33/REPORT_S33.md`): effect = arm − reference, negative = better; for quantum contrasts "negative means VQE is better" (`s33/VERIFICATION/final/QUANTUM_CONTRASTS.md`). x = |effect|/MDE, MDE = 2.8016·SE. < 0.7x NOT A RESULT; 0.7–1.0x NOT MEASURED; RESULT ≥ 1.0x + fold CI excluding 0 + ≥ 4/5 folds.

Hardware: no quantum-hardware run is recorded in any imported file. All circuits were classically simulated (statevector ≤ 22 qubits; exact MPS "classically simulable by construction") (`s33/ARCHITECTURES/QENGINE.md`; `s33/ARCHITECTURES/ARCHITECTURE_S33-A20.md`; `ARCHITECTURE_S33-A33.md`).

---

## A. Sprint-level verdict

### Q-A1. Census: did CVaR-VQE ever change a built-chain answer?
- **Measured:** 34 chain-level rows, 10 lanes, 3 instruments; "no contrast between a CVaR-VQE arm and its classical twin (SA, exact enumeration, greedy, random, or the same pipeline with the quantum stage removed) reached the contract bar in VQE's favour. None even reached the 0.7x NOT MEASURED zone in VQE's favour." The only chain RESULTs involving a register search are search-vs-no-search (#15 E230 vqe − trivial −0.840, 2.40x; #24 E900 mid30 sa − none −0.393, 1.05x), "and SA delivers them equally well" (`s33/VERIFICATION/final/QUANTUM_CONTRASTS.md` §A, §D). At census time (13:25, 2026-09-25) E810 43/45, E1000 21/45, E406 32/45 were read as RUNNING.
- **Original interpretation:** "**No.**" (QUANTUM_CONTRASTS §D). Report: "CVaR-VQE never improved a built-chain answer (where it changed one, it was for the worse)" (`s33/REPORT_S33.md` §1.4). "In S33, CVaR-VQE had a real *role* in several designs ... In no design was that role *load-bearing*." (§16).
- **Status in source:** census COMPLETED; later full-n results (E810, E811, E1000, E1003, E1006, E1007, E518V) were added in REPORT §8 and did not change the verdict (the E1000 ungated P1 later reached 0.84x in VQE's favour, see Q-H1 — so "None even reached 0.7x in VQE's favour" is a census-time statement).
- **Leakage:** all chain arms DEP.

### Q-A2. Quantum stage in the headline architectures
- **Measured:** production A00: "`core/pipeline.py:179 quantum=False`"; "the canonical endpoint contains no quantum computation at all" (`s33/MAP_PIPELINE.md` §4 D10). E308/A31.2 and A80 contain no quantum stage. A90: VQE→SA +0.026, stage removed +0.110 (long40) (`s33/REPORT_S33.md` §1.4). A101: quantum tails removed 4.352 vs 4.356 (long40), 3.847 vs 3.846 (mid30) (`ARCHITECTURE_S33-A101.md`).
- **Original interpretation:** "The quantum stage is absent or inert in every headline." (`s33/REPORT_S33.md` §1.4). Final length-routed system "contains **no CVaR-VQE stage that changes the answer**" (§17).
- **Status:** SURVIVES (Y adversary: "quantum stage not load-bearing at any length SURVIVES", `s33/LEDGER.md` E990V/E991V).
- **Leakage:** DEP, CLEAN.

---

## B. Engine and resource figures

### Q-B1. E003 engine benchmark (QENG)
- **Measured:** n = 16 dense QUBOs (6 instances, one seed each), evaluations to exact optimum: CVaR-VQE 980–2,664; greedy 19–85; steepest 88–158; SA 402–859; random never. 60-qubit torsion-like chain (20 residues × 6 bins, modulo-encoded) at 20,000 evaluations: SA with group moves −40.74 (exact, chain DP), greedy −40.01, CVaR-VQE (MPS χ = 16, 2 layers, warm start, SPSA over 360 parameters; 50/200/500 shots) −27.4 / −26.5 / −22.3, random −22.9 (`s33/ARCHITECTURES/QENGINE.md` §7.0; `s33/LEDGER.md` E003).
- **Original interpretation:** "On landscapes that local search solves, **the VQE is 10–100x less evaluation-efficient than greedy descent**"; "any S33 quantum claim must beat SA/greedy at equal n_evals, not random" (`QENGINE.md` §7.0; `s33/LEDGER.md` E003). "At equal budget the early CVaR-VQE *is* random sampling" (§7.1).
- **Status:** "AD HOC (not endpoint results)" / "Ad hoc, 6 instances, one seed each; not a ledger result" (`s33/LEDGER.md`; `QENGINE.md`).
- **Resources:** engine `s33/qengine.py`, 43/43 tests pass (22 s). Leakage: synthetic, n/a.

### Q-B2. Simulator costs (as stated)
- MAP_QUANTUM benchmark (Intel Core Ultra 7 256V, 8 cores): exact numpy statevector CVaR + adjoint gradient 0.004 / 0.046 / 4.4 / 20.3 s at 12 / 16 / 20 / 22 qubits; lightning adjoint 1.21 s at 20 qubits; own ExactMPS 1024-shot CVaR + exact score gradient at 120 qubits 0.15 s (χ = 16), 0.29 s (χ = 32), 1.15 s (χ = 64) (`s33/MAP_QUANTUM.md` §0.4, §4). Repo MPS scales O(n log n χ⁶) time / O(nχ⁴) memory, not O(nχ³) as documented; χ = 64 at n = 120 would need ~15 GB (`s33/MAP_QUANTUM.md` §0.5, §7.2).
- QENGINE benchmark (1 BLAS thread): statevector n = 20, 2 layers, exact-grad iteration 0.78 s; MPS SPSA iteration n = 120 linear-CZ 2 layers 53–62 ms; "Multithreaded BLAS (8 threads) never helped" (`QENGINE.md` §6.1).
- Sprint accounting: "The quantum searches were cheap: a 6000-evaluation VQE on 168 qubits took about 12–18 CPU-s"; chain arms and projections dominated compute (`s33/REPORT_S33.md` §23).
- Per-architecture register sizes/shots/budgets are listed in each item below.

---

## C. Registers and their classical twins (by lane)

### Q-C1. S33-A10 subset register (S_mosaic; E100, E101, E102)
- **Measured:** 16 qubits (top-16 members), enumerable (65,535). E100 (cloud, exhaustive): loglik Spearman(E, RMSD) +0.25 (in-band +0.22), argmin 6.527 vs incumbent 7.032; brief's QUBO form wrong sign (−0.16..−0.20). E101 sub_vqe chain 6.613 (vs incumbent −0.618, 0.86x NM per REPORT §5; A10 file records PARTIAL 32/45 −0.565, 0.59x); subset VQE vs SA energies 4/15/4 (23 targets) (`ARCHITECTURE_S33-A10.md`; `s33/REPORT_S33.md` §5).
- **Original interpretation:** "the subset register adds nothing resolvable over the top-m rule; it is a hull readout (NOTES 1.1)" (`ARCHITECTURE_S33-A10.md`).
- **Status:** falsified; QUBO form killed by condition C (FAILED_E100) (`ARCHITECTURES/INDEX.md`).
- **Leakage:** DEP (chain arms); E100/E102 cloud diagnostics ORACLE-scored.

### Q-C2. S33-A11 mosaic register (S_mosaic; E101, E103, E104, E107)
- **Measured:** S = 6 segments × K = 8 members, 18 qubits, exact MPS RY+CZ L = 2 (χ = 4), 256 shots/iter, 60 iters, α 0.5→0.1, budget cap 15,360; controls SA (64 chains), greedy, random(prior), exhaustive 2^18 (`ARCHITECTURE_S33-A11.md`). Energy at equal n_evals (3,269 mean, E103): VQE vs SA 14W/17T/14L (mean dE +0.011), vs greedy 21/1/23, vs random(prior) 27/11/7; CVaR tail 4.5 distinct states. Chain: dmos_vqe − dmos_sa +0.026 (0.07x); **E107** dmos_vqe_ref − dmos_sa_ref −0.012 (0.04x); gated 5.813 vs 5.826 (−0.013, 0.04x) (`ARCHITECTURE_S33-A11.md`; `s33/RESULTS/E107_ablation_sa_ref/RESULT_E107_ablation_sa_ref.md` sa_ref 6.1737; QUANTUM_CONTRASTS rows 4–8). E104 (11/45 targets): SA or greedy lowest energy at 18/32/40 qubits; VQE-L2 beats product ansatz 8W/3L at 40 q and random(prior) 10/1; hits exhaustive optimum 6/11 at 18 q. E101 (32 targets): mos_vqe − mos_sa +0.064; census full 45: +0.195 (0.46x).
- **Original interpretation:** "the CVaR-VQE stage does NOT change the answer (FAILED_E107.md). The best pipeline's gain is solver-agnostic (mosaic start + refinement + gate)." (`s33/STATE_LIVE.md` S_mosaic block). REPORT §16: "the warm-start mode alone (0 VQE iterations) gives the same answer".
- **Status:** quantum stage falsified (FAILED_E107); adversary "The quantum role is REFUTED: the warm-start mode alone gives the same answer"; S adversary cloud: VQE seed spread +0.225 "exceeds every solver gap" (`s33/REPORT_S33.md` §5; QUANTUM_CONTRASTS §C). Equal tuning: NO (budget only).
- **Leakage:** DEP, LFO-XF (headline 5.813).

### Q-C3. S33-A20 SEG-FRAG de novo fragment register (F_fragment; E201, E202, E210)
- **Measured:** 16–18 windows × K = 32 fragments, 5 qubits/window, 80–90 qubits (32^17 ≈ 4e25 states), ExactMPS L = 2 χ = 4, 512 shots, α 0.5→0.1, budget 40,000 distinct evaluations. A20.0 condition C ρ −0.152 (killed); A20.1 ρ 0.839 / in-band 0.461 (pass). E210 INTERRUPTED at 4 dev targets: chain vqe 8.419 vs sa 6.724, saP 7.455, incumbent 4.265, avg75 7.953; VQE lower best-E than SA on 2/4, prior-SA on 1/4; mean best E vqe −69.74 vs sa −93.28, saP −94.90 (`ARCHITECTURE_S33-A20.md`; `s33/RESULTS/E210_partial_analysis/RESULT_E210_partial.md`). Census row 12: vqe − sa +1.695 (0.39x, n = 4).
- **Original interpretation:** "Dominated by the incumbent; superseded by A21"; collapse lemma (NOTES D-F2) cited; 1KNT "stuck at −124.5 while prior-SA reached −140.8" (`ARCHITECTURE_S33-A20.md`; `s33/REPORT_S33.md` §9).
- **Status:** A20.0 killed by condition C (E201); A20.1 superseded; E210 INTERRUPTED (4/45).
- **Leakage:** DEP (corpus excluding target and 9-mer sharers).

### Q-C4. S33-A21 HYBRID-FRAG (F_fragment; E221, E222, E230)
- **Measured:** 80–90 qubits, ExactMPS L = 2, 3 restarts, 128 shots, budget 40,000 distinct evaluations. E222 chain (n = 45): vqe_ref 6.603; saX0_ref 6.426; esm5_ref (no search) 6.428; saP_ref 5.830 (n = 22). vqe_ref − saX0_ref +0.177 (0.24x); − esm5_ref +0.175 (0.33x); − saP_ref −0.279 (0.42x, n = 22). Energy: VQE lower best-E than saP 15/22, saX0 23/45 (`s33/RESULTS/E222_hybrid_analysis/RESULT_E222_hybrid.md`; `ARCHITECTURE_S33-A21.md`). F adversary (V_rand, cloud, 33 targets): trained VQE − untrained sampling after refinement +0.187 (0.27x) "although it is lower in energy on 33/33"; refined 5-member tail beats refined argmin −0.378 (1.13x): "the ENSEMBLE carries weight, not training" (`s33/LEDGER.md` E810 block, E222V addendum; QUANTUM_CONTRASTS §C).
- **Original interpretation:** "A21's CVaR-VQE stage does not change the answer (FAILED_E222.md); the measured gain is the classical refinement readout." (`ARCHITECTURE_S33-A21.md`).
- **Status:** quantum stage falsified; F adversary: "quantum null SURVIVES" (`s33/LEDGER.md` E222V/E223V). Equal tuning: NO.
- **Leakage:** DEP, LFO-XF.

### Q-C5. E230 matched short null at tuning126 (F_fragment)
- **Measured:** full n = 126: vqe 3.592 vs production 3.2105, +0.381 (1.76x, RESULT: WORSE); vqe − sa +0.007 (0.07x); vqe − saP +0.024 (0.20x); vqe − trivial (no search) −0.840 (2.40x, RESULT: BETTER) (`s33/RESULTS/E230_short_null/RESULT_E230_short_null.md`; QUANTUM_CONTRASTS rows 13–15). Lane analysis at n = 114: vqe − sa +0.024 (0.23x), vqe − saP +0.053 (0.48x) (`s33/RESULTS/E230_short_null_analysis/RESULT_E230_short_null.md`).
- **Original interpretation:** "the search matters; SA does it equally" (QUANTUM_CONTRASTS #15); "the matched null holds" (`s33/LEDGER_CONSOLIDATED.md`).
- **Status:** COMPLETED (126, re-scored by the adversary). **Leakage:** DEP.

### Q-C6. S33-A30 contact-subset register (C_contact; E300, E301)
- **Measured:** one qubit per top-M ESM contact (66–90 qubits). E300 (cloud, ORC): true subset 5.992 vs asserting all 5.828 vs random equal-size 5.979. E301 (18 targets, ORC): ρ(E, RMSD) lower half −0.038 (kill rule 0.2); ρ(E, precision) −0.526. 41.8% of top-1.5n candidates already satisfied by the prior-only decode (65.6% of true, 21.6% of false) (`ARCHITECTURE_S33-A30.md`).
- **Original interpretation:** inert-qubit lemma: "the register's live degrees of freedom are mostly ways to ADD errors" (`ARCHITECTURE_S33-A30.md`).
- **Status:** KILLED by condition C (FAILED_E301). **Leakage:** ORC diagnostic.

### Q-C7. S33-A32 near/far mode register (C_contact; E303)
- **Measured:** ORACLE register state 5.733 vs top-n decode 5.828 (cloud); complete native near/far map 4.379 (`ARCHITECTURE_S33-A32.md`).
- **Original interpretation:** "the best possible state of this register is only 0.10 A below the deployable top-n decode"; the remaining error "lives in pairs the prior is CONFIDENTLY wrong about (outside the register)".
- **Status:** NOT BUILT (headroom too small). **Leakage:** ORC.

### Q-C8. S33-A33 CVaR-VQE tail as DG restraint ensemble (C_contact; E306) — CVaR tail collapse
- **Measured:** register top-1.5n pairs (69–90 qubits), ExactMPS RY+CZ 2 layers χ 4, warm start, 128 shots, α 1→0.1 over 50 its, budget B = 6000 distinct bitstrings; tail = 12 lowest-energy distinct states. Chain (n = 45): vqe_tail 5.816, sa_tail 5.751, noise12 (no register) 5.681; vqe_tail − sa_tail **+0.065** (0.72x MDE 0.090, NOT MEASURED, VQE worse); gated vqe 5.370 vs gated noise12 5.264, gated sa 5.317. Cloud: vqe 5.755, sa 5.691, greedy 5.695, rand_tail 5.644, prior12 5.648, noise12 5.580. Solver: SA and greedy reach the best energy on 45/45, CVaR-VQE on 23/45 (mean gap 0.35), random 2/45. Tail Hamming distance 2.4 (vqe) / 2.3 (sa) / 11.5 (random) / 20.6 (prior draws) (`ARCHITECTURE_S33-A33.md`; `s33/RESULTS/E306_cvar_tail_chain/RESULT_E306_cvar_tail_chain.md` 5.8163; `CENSUS_analysis.json` confirms +0.0648, 0.716x). C adversary (cloud): VQE tail − random tail +0.112 (0.80x, W/L 13/32), − trivial prior draws +0.107, − greedy +0.060; "lower tail energy goes with higher RMSD (ρ −0.26)" (QUANTUM_CONTRASTS §C; `s33/REPORT_S33.md` §5).
- **Original interpretation:** "pre-registered null confirmed -- the CVaR-VQE stage does not change the answer; lower-energy tails are less diverse and average slightly worse (E310 law)" (`ARCHITECTURE_S33-A33.md`). Mechanism in report: "CVaR tails collapse onto the argmin and destroy the diversity that ensemble readouts need" (`s33/REPORT_S33.md` §1.6).
- **Status:** falsified; C adversary "SURVIVES, strengthened". Equal tuning: "moot: SA/greedy hit the register optimum on 45/45" (QUANTUM_CONTRASTS row 1).
- **Leakage:** DEP, LFO-XF.

### Q-C9. S33-A34 robust / joint CVaR over a predictor ensemble (C_contact; E307, E312)
- **Measured:** E307 cloud (18 targets): vqe_mean 4.411, vqe_rob 4.420, vqe_joint 4.217, sa_mean 4.478, sa_rob 4.477, sa_opt 4.225; robust tails assert 4–6 contacts (= prior-only decode); vqe_joint − sa_opt −0.008. E312 chain INTERRUPTED 16/45: joint − mean −0.027 (0.04x); subset chain mean 4.482 (`ARCHITECTURE_S33-A34.md`; `s33/RESULTS/E312_d4_chain/RESULT_E312_d4_chain.md`).
- **Original interpretation:** D4 sign lemma: "the stochastic-energy CVaR-VQE is risk-SEEKING in model disagreement"; "robust = 'assert nothing'"; "the 'joint' energy equals a classical optimistic energy" (`ARCHITECTURE_S33-A34.md`; `s33/REPORT_S33.md` §5).
- **Status:** falsified (sign lemma, E307 confirmed); E312 INTERRUPTED. **Leakage:** DEP (subset).

### Q-C10. S33-A41 CVaR-VQE on the per-residue (θ,τ) head8 register (P_prior; E405, E406) and E406V
- **Measured:** register (L−3) × 3 qubits = 123–171 qubits (head8), ExactMPS RY+CZ 2 layers χ 4, 32 shots, α 0.5→0.1, Adam 0.15, budget 6000 distinct structures (`ARCHITECTURE_S33-A41.md`; `s33/LEDGER_CONSOLIDATED.md` E406). E405 condition C (10 targets, ORC): ρ 0.78 / 0.81 / 0.73 (head4/head8/win8). E406 energy (45 targets): VQE 3.057, product ansatz 3.093, lane SA (8 chains, untuned) 3.222, random (untrained warm-start circuit) 3.535, greedy 4.528; VQE < SA on 41/45; decoded cloud VQE 6.195, product 6.918, SA 6.468, random 7.071, greedy 15.273 (`ARCHITECTURE_S33-A41.md`). Raw built chain (n = 45): vqe 6.2220, sa 6.5132, vqe_prod 6.9430, random 7.2814, greedy 15.2663 (`s33/RESULTS/E406_tt_vqe/head8_*/RESULT_*.md`); chain VQE − SA −0.291 (0.33x) (`s33/REPORT_S33.md` §5). E406V: VQE vs tuned SA (9 configs) 3.057 vs 3.064, +0.007, 0.18x, VQE lower 24/45; ICM 3.111; product ansatz 3.093 (23/45 tie) (QUANTUM_CONTRASTS §B). α → 1 ablation: energy 3.69 vs 3.27, 10/10 targets (`s33/LEDGER.md` E403V/E404V/E406V).
- **Original interpretation:** P_prior (at the time): "CVaR-VQE beats SA on energy 41/45 (3.057 vs 3.222), cloud 6.195 vs 6.468 (0.30x); entanglement ablation worse cloud (−0.72)" (`s33/STATE.md` Phase 2). Later: "P_prior's 41/45 VQE win was an SA-tuning artefact" (`s33/SCIENTIFIC_MEMORY.md`). "CVaR α is load-bearing INSIDE the optimiser ... but the readout is solver-agnostic; S4 pool selection (no quantum) beats the A41 VQE decoded cloud (6.041 vs 6.195)" (`s33/LEDGER.md`).
- **Status:** "falsified: the energy win was an SA-tuning artefact"; "the energy claim is REFUTED" (`s33/REPORT_S33.md` §5). Equal tuning in E406: **NO** ("VQE had 11 configs, SA 3 configs × 2 seeds, SA T0 never tuned", QUANTUM_CONTRASTS §B); E406V ~YES.
- **Leakage:** DEP (esmprior_v1, CLEAN).

### Q-C11. E1001 — SA tuned with equal effort (H_hybrid)
- **Measured:** 10 SA configs on 3 long40 dev targets, same 6000-distinct-evaluation budget as the VQE's tuning: tuned SA 3.394 < CVaR-VQE 3.457 < P_prior's SA config 3.670 (`s33/LEDGER.md` E1001).
- **Original interpretation:** "With equal tuning effort, classical SA out-optimises CVaR-VQE on the largest structural register S33 built." (`s33/LEDGER.md`).
- **Status:** COMPLETED (energy level); FAILED_E1001 ("CVaR-VQE is a better optimiser than SA on A41") (`s33/REPORT_S33.md` §24). Equal tuning: **YES**. **Leakage:** native-free energy.

### Q-C12. S33-A100 — A41 CVaR-VQE tail relaxed under the A80 energy (H_hybrid; E1000, E1002, E1003, E1004)
- **Measured:** A41 head8 register, CVaR-VQE bit-identical to E406 config (6000 E_P evaluations, seed 0), 16-state tail, 150 L-BFGS its each under E_D, readout min, gate. Budgets/twins identical after the search (`ARCHITECTURE_S33-A100.md`). Full-n chain (long40 45 / mid30 41):

  | arm | long40 | long40 gated | mid30 | mid30 gated |
  |---|---|---|---|---|
  | vqe_min | 5.519 | 4.865 | 4.297 | 4.156 |
  | sa_t_min (tuned SA) | 6.343 | 5.423 | 4.122 | 4.058 |
  | sa_p_min | 5.947 | 4.838 | 4.174 | 4.007 |
  | random_min (untrained warm-start circuit) | 4.759 | 4.415 | 3.742 | 3.828 |
  | vqe_prod_min | 6.207 | 5.204 | 4.365 | 4.279 |
  | rf_min (register-free A80, matched CPU) | 4.726 | 4.382 | 3.877 | 3.864 |

  Contrasts (from `s33/RESULTS/H_hybrid_long40_scored.json`, `H_hybrid_mid30_scored.json`): P1 vqe_min − sa_t_min long40 **−0.824 (0.84x, NOT MEASURED; median −0.07, W/L 27/18)**; gated −0.558 (0.66x); mid30 +0.176 (0.22x); vqe_min − rf_min +0.793 (0.90x, NM, wrong way); vqe_min − random_min +0.761 (0.85x, NM; mid30 +0.555, 0.81x); vqe − vqe_prod −0.688 (0.60x); sa_p_min − random_min +1.188 (1.16x RESULT WORSE); relaxation vs raw A41 chain −0.703 (1.43x RESULT). Energy: E_P vqe 3.057 vs tuned SA 3.052, VQE lower 24/45 (`ARCHITECTURE_S33-A100.md`).
- **Transmission (H_hybrid):** within-target Spearman(E_P, chain) across 5 equal-budget solvers −0.082 (long40), −0.076 (mid30); Spearman(E_D, chain) +0.40 / +0.30; VQE beats random tail on E_P on 45/45 and 41/41 and loses on the chain by 0.76 / 0.56; trap counts long40 random 0 < VQE 6 < SA_p 10 < product 11 < tuned SA 13; mid30 random 0 < tuned SA 2 < SA_p 3 < VQE 5 < product 6; continuous energy flags 55/56 traps; snapping the register-free structure onto the head8 register moves it 9–25 Å (`s33/REPORT_S33.md` §16).
- **Original interpretation:** "CVaR-VQE is NOT load-bearing" (`s33/STATE_LIVE.md` H_hybrid block); "The register energy does not transmit"; "Mechanism: a topology-trap lottery" (`s33/REPORT_S33.md` §16); "A100 is not load-bearing and is dominated by the register-free decoder and by its own untrained warm start" (`ARCHITECTURE_S33-A100.md`).
- **Status:** load-bearing test FAILED (FAILED_E1000). "No adversary ran (the lane agent died at the usage limit)" per REPORT §5 A100 row; the H_hybrid adversary later ran 4 seeds (Q-C14). Equal tuning: **YES** (P1). "the only EQUAL-TUNING-EFFORT chain test" (`s33/LEDGER.md` E1000 FINAL).
- **Resources:** "a 6000-evaluation VQE on 168 qubits took about 12–18 CPU-s" (`s33/REPORT_S33.md` §23); the harness RESULT files for E1000/E1002/E1003/E1004 report only the job's first chain arm vs avg75 (e.g. E1000 f012 n = 27 mean 6.3822; f34 n = 18 mean 4.2254) (`s33/RESULTS/E1000_*`, `E1002_*`, `E1003_*`, `E1004_*`).
- **Leakage:** DEP, CLEAN.

### Q-C13. E1006 / E1007 — pre-registered seed-1 replication of E1000
- **Measured (`s33/RESULTS/H_hybrid_E1006_long40.json`, `H_hybrid_E1007_mid30.json`):** long40 seed 1 (n = 45, sentinels 15/15): R-P1 vqe_min − sa_t_min −0.066 (0.05x, W/L 20/25); 2-seed −0.445 (0.43x); seed-1 vqe − random +1.309 (1.12x RESULT WORSE); **2-seed vqe − random +1.035 (1.35x RESULT WORSE)**; 2-seed vqe − vqe_prod −0.188 (0.26x); seed1 − seed0 vqe_min +0.507 (0.36x). mid30 seed 1: R-P1 +0.011 (0.01x); seed-1 vqe − random +0.679 (1.02x RESULT WORSE); 2-seed vqe − random +0.617 (0.98x NOT MEASURED); 2-seed entanglement +0.008. "Same-solver chains move > 2 A between seeds on 27% of targets (random: 0%)" (`ARCHITECTURE_S33-A100.md`).
- **Original interpretation:** "the seed-0 −0.824 was a basin lottery"; "the only contrast that ever leaned toward CVaR-VQE is a seed artefact" (`s33/REPORT_S33.md` §1.4; `s33/LEDGER.md` E1006/E1007).
- **Status:** "REPRODUCED(null) / FALSIFIED(VQE advantage)" (`s33/LEDGER.md`). **Leakage:** DEP, CLEAN.

### Q-C14. S33-A101 multi-source relaxed pool (H_hybrid; E1005) and H adversary
- **Measured:** GATE_pool_all long40 4.356 / mid30 3.846; quantum ablation GATE_pool_cl 4.352 / 3.847; register-free GATE_rf_min 4.382 / 3.864; long40 hyb_vqe − hyb_rand −0.001; pool_all − pool_cl +0.002 (Q2 +0.004 gated); GATE_pool_all − GATE_E308 −0.383 (0.67x); − D_decoder GATE_rfp +0.013. Readout source picked (long40): rf 42%, random 24%, sa_p 13%, vqe 9%, sa_t 7%, vqe_prod 4% (`ARCHITECTURE_S33-A101.md`; `s33/RESULTS/H_hybrid_E1005_long40.json`). H adversary (4 seeds): energy tie ΔE_P +0.0012 (51.7% of 180 pairs); relaxed readout "leans VQE on all seeds but NOT MEASURED (4-seed cloud −0.571, 0.81x; 3-seed chain −0.355, 0.42x)"; random-prior tail beats VQE 4-seed +0.872 (1.46x RESULT, p_WY 1e-4); "Parallel tempering tuned with equal effort does not change the picture"; topology-trap mechanism "reproduces but is partly definitional (WEAKENED)" (`s33/LEDGER.md` E1005/E10xxV).
- **Original interpretation:** "The CVaR-VQE is not load-bearing in it" (`ARCHITECTURE_S33-A101.md`).
- **Status:** A101 declared post hoc ("designed after the E1000-E1004 means"), "not claimed"; H adversary "CVaR-VQE NOT load-bearing SURVIVES". **Leakage:** DEP, CLEAN.

### Q-C15. S33-A51 short mosaic register (X_short; E503)
- **Measured:** 9–12 qubits, exhaustive, 12 targets (ORC): in-band Spearman mean −0.038 / median −0.011 (distogram), ESM energy −0.152; argmin mosaic 3.565 vs production cloud 3.264 (`ARCHITECTURE_S33-A51.md`; `s33/LEDGER_CONSOLIDATED.md` E503).
- **Original interpretation:** "Condition A fails (enumerable ...) AND condition C fails ... At 9-16 aa the energy, not the register or solver, is the barrier."
- **Status:** KILLED at the condition-C pre-check; "no VQE compute spent". **Leakage:** ORC diagnostic.

### Q-C16. S33-A53 chiral (θ,τ) TT-register (X_short; E513, E513b, E518V)
- **Measured:** 18–39 qubits, ExactMPS L = 2 χ 4, 512 shots, α 0.1, Adam 0.05, 12k evals (E513b). E513: in-band ρ median 0.270 (pass), tail cloud 3.464 vs production 3.264 (fail); discretisation floor 0.53 Å. E513b (12 targets) best E VQE 33.192 / SA 33.187 / greedy 33.187 / random 36.203 / prior 34.287; tail cloud 3.469 / 3.456 / 3.458 / 3.482 / 3.507 (`ARCHITECTURE_S33-A53.md`). Round-1 adversary chain n = 12 +0.053 ± 0.198. **E518V (round 2, full n = 126, same-job sentinel 126/126):** VQE tail 3.454 (+0.243 vs production, 1.16x RESULT WORSE); SA tail 3.460 (+0.249, 1.19x); VQE − SA −0.006 ± 0.013 (0.17x); VQE − random +0.070 ± 0.025 (1.02x, 5/5, "RANDOM IS BETTER", tail cloud); VQE − prior-sampler ablation +0.040 (0.64x) (`s33/REPORT_S33.md` §5; `s33/LEDGER.md` E516V–E518V).
- **Original interpretation:** "the VQE stage is replaceable by SA/greedy" (`ARCHITECTURE_S33-A53.md`); "'VQE beats random/ablation' REFUTED (energy only). The tail-vs-argmin gain is averaging, shared by SA." (`s33/LEDGER.md`). "Round 1's n = 12 estimate was a favourable draw." (`s33/REPORT_S33.md` §5).
- **Status:** killed by its pre-registered rule; kill CONFIRMED at full n. **Leakage:** DEP.

### Q-C17. S33-A60 exactly enumerated mosaic at mid length (M_mid; E604a, E604b, E609, E604bV)
- **Measured:** 18 qubits (262,144 states), ExactMPS L = 2 χ 4, 256 shots, α 0.5→0.1, budget 2,000 distinct evaluations (0.76% of 2^18). E604a condition C (exact, 10 targets): agree +0.358 FAIL; loglik +0.600 PASS. E604b chain (n = 41, same job): exact argmin 6.341, CVaR-VQE 6.431, SA 6.358; VQE − exact +0.089 (0.33x, W/L/T 10/20/11); VQE − SA +0.072 (0.20x); SA − exact +0.017. P(best-found = exact optimum): VQE 27%, SA 24%, greedy 54%, random 0%; median energy rank VQE 8, SA 3, greedy 0, random 104 (`ARCHITECTURE_S33-A60.md` v A60.3; `s33/RESULTS/E604b_mid30_mosaic_loglik/RESULT_E604b_mid30_mosaic_loglik.md` 6.4305). E609 (energy, 10 targets): 18 q hit rate VQE 37% / SA 27% / greedy 63% / random 3%; 20 q 30/0/30/0%; 24 q gap/sd VQE 1.41 vs greedy 0.51 (QUANTUM_CONTRASTS §B). M adversary (cloud): random at equal budget ties VQE +0.041 (0.08x); register worth exact −0.91 / VQE −0.82 / random −0.78 vs best whole member; CVaR tail − best bitstring −0.081 (0.19x) (`s33/LEDGER.md` E606V/E604bV).
- **Original interpretation:** "at this length the register is enumerable in ~20 s, so the quantum stage is decorative by construction (condition A fails). Honest summary: CVaR-VQE does not change the answer here." (`ARCHITECTURE_S33-A60.md`). "quantum ≡ SA ≡ exact" (`s33/STATE.md`).
- **Status:** superseded; "the quantum stage is decorative"; M adversary "SURVIVES, strengthened". E604bV chain job INTERRUPTED 0/41 ("terminated externally 11:36 with 0 rows, not relaunched (the cloud-basis ablation is complete)") (`s33/RESULTS/E604bV_qablate_mid30/RESULT_E604bV_qablate_mid30.md`; `s33/LEDGER.md`). Equal tuning: moot (exact optimum known).
- **Leakage:** DEP (CLEAN; ESM loglik, no learned prior).

### Q-C18. S33-A70 exact Gibbs posterior-mean readout / H-Q1 (T_tempered; E700, E701)
- **Measured:** 18-qubit R60 mosaic, exact over all 262,144 states. E700 cloud: mid30 argmin 6.327 / gibbs_lfo 5.965 (−0.362, 0.70x) / pm_lfo 6.342; long40 6.371 / 6.105 (0.73x) / 6.015; gibbs_lfo − tail_lfo −0.268 (1.53x) / −0.198 (1.12x) RESULT. E701 chain, full n (adversary re-score): Gibbs − argmin mid30 −0.170 (0.33x), long40 −0.159 (0.47x); Gibbs − perturb-and-MAP −0.219 / +0.138. Projection penalty +0.20 for gibbs_lfo vs +0.01 for argmin (mid30) (`ARCHITECTURE_S33-A70.md`; `s33/REPORT_S33.md` §5). T adversary: "soft Boltzmann weights beat hard CVaR tails on the mid30 chain (−0.248, 1.40x RESULT)"; long40 not established (`s33/LEDGER.md` E7xxV).
- **Original interpretation:** "H-Q1 FALSIFIED on R60 ... the posterior-mean readout's cloud gain is mostly contraction, which the canonical projection removes" (`ARCHITECTURE_S33-A70.md`).
- **Status:** falsified (FAILED_E700_R60); T adversary "H-Q1 falsification SURVIVES at full n". E701 lane chain numbers were "TIME-TRUNCATED subsets" (mid30 28/41, long40 26/45) at the lane cutoff; the adversary re-scored full n. **Leakage:** DEP.

### Q-C19. S33-A71 tempered Born machine vs Metropolis twin (T_tempered; E710)
- **Measured:** exact statevector RY+CZ L = 3 (72 parameters), Adam 120 steps; sampled ExactMPS L = 2 χ 4, 256 shots/step, budget 15,360 distinct evaluations; CVaR control α = 0.1. Lane (2 targets): KL(p_θ‖p_T) 0.21 / 0.43; distance to exact Gibbs mean: sampled circuit 0.949 Å vs Metropolis twin 0.079 Å (2/2); plain CVaR tail perplexity 1.0 (= argmin) (`ARCHITECTURE_S33-A71.md`). 10 targets (report): TBM 2.08 vs Metropolis 0.73 Å; Metropolis closer on 9/10 (1.08x RESULT against the circuit) (`s33/REPORT_S33.md` §5; `s33/LEDGER_CONSOLIDATED.md` E710). T adversary: "the sampled tempered circuit is ~2.9x farther than Metropolis from the exact posterior mean (MCMC closer 9/10) ... plain CVaR-VQE collapses to one state that is the argmin on only 5/10 (L = 2 under-optimised)" (`s33/REPORT_S33.md` §5).
- **Original interpretation:** "the tempered quantum distribution is NOT load-bearing"; "the circuit is dominated by, not equal to, its classical twin"; "the plain CVaR objective returns the argmin exactly (tail perplexity 1.0)" (`ARCHITECTURE_S33-A71.md` v A71.2).
- **Status:** falsified (FAILED_E710). Contradiction recorded: the lane file says CVaR "returns the argmin exactly"; the T adversary says it collapses to one state "that is the argmin on only 5/10". E720 (A72, 32 q) NOT RUN. **Leakage:** ORC diagnostic (cloud, distance to exact Gibbs mean).

### Q-C20. S33-A81 / A81m discrete (θ,τ) registers searched by CVaR-VQE (D_decoder; E800, E810, E811)
- **Measured:** A81 joint-bin: native-bin coverage 18% (k = 2) / 31% (k = 4); ORACLE bits polish to 8.45 / 6.28 Å vs RF 4.35 (capacity failure). A81m macro4: ~106–114 qubits (long40), 44–74 (mid30); ExactMPS RY+CZ L1 χ 2, 128 shots, α 1→0.1, 8192 evaluations; coverage 100%; ORACLE bits polish to 5.11 Å (> RF); condition C lower-half ρ raw 0.65 / basin 0.26 (`ARCHITECTURE_S33-A81.md`; `s33/LEDGER_CONSOLIDATED.md` E810). E810 final (long40 45): rf 4.763, rfp 4.671, vqe 5.127, sa 5.696; GATE_vqe 4.645, GATE_sa 4.792; P1 REG_best(vqe) − rf +0.364 (0.60x, wrong direction); P2 vqe − sa −0.568 (0.48x, "D's SA untuned"); cloud vqe − random +0.192. E811 final (mid30 41): rf 3.717, rfp 3.726, vqe 4.524, sa 4.178; P1 REG_best(sa) − rf +0.461 (0.79x); P2 vqe − sa +0.346; **vqe − rf +0.807 (1.04x, RESULT: WORSE)** (`s33/LEDGER.md` E810/E811 FINAL; `s33/REPORT_S33.md` §8). Energy (census, 43/45): polished best E VQE − SA −56.6 nats (38/43), − greedy −67.5 (33/43), − random −4.5 (27/43, "about random"), +44.1 vs register-free RF (VQE lower on only 9/43) (QUANTUM_CONTRASTS §B). D adversary: "'CVaR-VQE best register solver in energy' REFUTED: ties random prior sampling (−3.9 nats, 27/45, p 0.23); greedy beats it on raw objective 27/45" (`s33/LEDGER.md` E850V–E853V).
- **Original interpretation (interim, later revised):** "CVaR-VQE is the best register solver (beats SA in energy), but the register is not load-bearing: the register-free decoder is better." (`ARCHITECTURE_S33-A81.md`, E810 interim 13/45). Final: "CVaR-VQE NOT load-bearing" (`s33/LEDGER.md` E810 FINAL).
- **Status:** falsified (FAILED_E800_A81; FAILED_E810_Ha); the "best register solver" claim REFUTED by the D adversary; close-out adversary: "SURVIVES as 'not load-bearing'; 'worse' is established only on mid30" (`s33/REPORT_S33.md` §5). Equal tuning: **NO** ("D's SA was worse than random"). **Leakage:** DEP, CLEAN.

### Q-C21. S33-A82 RF-seeded macro register (D_decoder; E813/E814)
- **Measured:** none. Implemented, pre-registered (PREREG_E813.md), queued on mid30 (E814), not run (`ARCHITECTURE_S33-A82.md`; `s33/LEDGER_CONSOLIDATED.md`).
- **Original interpretation:** proposed as the S34 quantum re-test: "Re-open CVaR-VQE only on a register built around the *decoder's* residual uncertainty ... Kill the design if condition C restricted to the neighbourhood of the decoder's answer fails, or if random ≤ VQE." (`s33/REPORT_S33.md` §28).
- **Status:** NOT RUN.

### Q-C22. S33-A90 final composite with an 18-qubit mosaic CVaR-VQE stage (Y_synth; E900, E901, E902, E903)
- **Measured:** 18-qubit mosaic over {DG mean, 3 DG decodes, 4 A62 windows}; RY+CZ HEA (2 entangling layers, 54 parameters), 256 shots, α 0.5→0.1, readout CVaR tail of 2,048 final shots; equal n_evals ~4,555 (long40) / ~5,390 (mid30). long40: A90 4.915, GATE_sa 4.888, GATE_none 4.805; A90 − GATE_sa +0.026 (0.34x); A90 − GATE_none +0.110 (0.34x); vqe − sa ungated +0.023. mid30: A90 4.304, GATE_sa 4.279, GATE_none 4.566; A90 − GATE_sa +0.025 (0.44x); A90 − GATE_none −0.262 (0.95x NOT MEASURED, fold CI [−0.43, −0.08], 4/5); vqe − none (30 no-template) −0.359 (0.97x). Energy long40 best E VQE vs SA W/T/L 21/12/12, vs greedy 4/27/14, vs random 16/22/7; CVaR-tail mean E vs SA-tail 12/1/32. mid30 vs SA 7/9/14, vs greedy 1/11/18, vs random 20/4/6; tail vs SA tail 6/0/24. Condition C: E901 in-band ρ +0.109 FAIL; E903 (A91) +0.018 FAIL (`ARCHITECTURE_S33-A90.md` §5–6). E902 seed 2: 4.861 vs 4.915 (mean abs Δ 0.093); A90 − GATE_none (seed 2) +0.010 (`s33/LEDGER.md` E902). Y adversary: vqe − sa +0.035 / +0.016; vqe − random +0.025 / −0.030; all ≤ 0.52x (`s33/LEDGER.md` E990V/E991V).
- **Original interpretation:** "the CVaR-VQE stage does NOT change the answer ... as condition C (E901 FAIL) and the averaging lemma predicted"; mid30: "the gain belongs to the discrete search, not to the quantum solver" (`ARCHITECTURE_S33-A90.md` §6). "Therefore the CVaR-VQE stage of A90 is expected NOT to change the answer; it is kept because the architecture is the reference that a load-bearing quantum stage (D_decoder E810) must beat" (§5).
- **Status:** superseded; seed reproduction REPRODUCED; Y adversary "Quantum stage not load-bearing at any length SURVIVES". Equal tuning: NO. **Leakage:** DEP, CLEAN.

---

## D. Mechanisms the sprint recorded (derived and measured)

### Q-D1. Solver-equivalence lemma
- **Statement (source):** "For a diagonal H on register x, min over distributions of CVaR_α(p) = min_x E(x) for every α ∈ (0,1] (put all mass on argmin). So a sufficiently expressive CVaR-VQE converges to the ground state, and any pipeline whose readout depends only on argmin E gives the SAME built chain whichever solver finds the argmin. Hence 'the quantum stage changes the answer' can only come from (i) optimisation quality ... or (ii) a readout that uses the whole output distribution (tail ensembles). On enumerable registers (i) is impossible by construction (M_mid: VQE = exhaustive = SA). (ii) was measured harmful when the tail concentrates (E310, E306)" (`s33/SCIENTIFIC_MEMORY.md` IMPORTANT DERIVATIONS).
- **Measured support:** E604b VQE 6.431 ≈ exact 6.341 ≈ SA 6.358 (chain); M adversary random ties VQE (+0.041) (Q-C17).
- **Status:** derivation (coordinator); listed first among the "Key mathematical results" (`s33/REPORT_S33.md` §25.1) and as mechanism 1 in QUANTUM_CONTRASTS §D.

### Q-D2. CVaR tail collapse
- **Statement (source):** "The optimum set is {p : p(argmin) ≥ α}, and the score-function gradient vanishes there, so tail ensembles degenerate to the argmin at convergence." "CVaR_α − T·S has minimiser p* ∝ exp((μ − E)₊ / (αT)): a Gibbs law truncated at μ" (`s33/REPORT_S33.md` §25.2; sources cited there: S_mosaic NOTES §1.5; T_tempered T2).
- **Measured:** E710 tail perplexity ≈ 1.0; S adversary: "the final tail sitting on states *worse* than the circuit's own best-evaluated state on 35/42 targets" (`s33/REPORT_S33.md` §8); E103 CVaR tail 4.5 distinct states of 2048 shots at α = 0.1 (`ARCHITECTURE_S33-A11.md`); tail distinct count 1 on 2UUX (`ARCHITECTURE_S33-A11.md` Theory); E306 tail Hamming 2.4 (VQE) vs 11.5 (random) / 20.6 (prior) (`ARCHITECTURE_S33-A33.md`); E310 (C_contact): averaging all 12 decodes 5.580 beats pick-by-loss 6.018 though ρ(loss, RMSD) +0.245 (`s33/LEDGER_CONSOLIDATED.md` E310).
- **Original interpretation:** "Concentration (CVaR, argmin of a weak energy) and averages of contracted objects hurt." (`s33/REPORT_S33.md` §14); "the Bayes-optimal readout under RMSD loss wants a posterior-like, DIVERSE distribution, which CVaR training destroys as α → 0" (`s33/SCIENTIFIC_MEMORY.md`).
- **Status:** recorded as mechanism 2 (`QUANTUM_CONTRASTS.md` §D; `s33/REPORT_S33.md` §1.6). Source caveat: SA tails were equally concentrated in E306 (Hamming 2.3), so the concentration is a property of optimised tails, not specific to the circuit (`ARCHITECTURE_S33-A33.md`).

### Q-D3. Non-transmission of register energy; no search headroom
- **Measured:** within-target ρ(E_P, chain) −0.08 (Q-C12); C adversary per-target Spearman −0.26 (E306); information floor 4.21 vs RF 4.35 on 6 dev targets; restart saturation at 32–64 starts (`s33/REPORT_S33.md` §1.6, §18; QUANTUM_CONTRASTS §D items 3–4).
- **Derived:** register bounds (D D1, D2, D4): "A random register with basin relaxation equals register-free restarts"; "min_b E_basin(b) ≥ min_x E(x): a register can beat only a heuristic continuous decoder, never an exact one"; "Restart saturation bounds any global solver's gain to ≤ 4.35 − 4.21 = 0.14 Å" (`s33/REPORT_S33.md` §25.12). Basin equivalence (H1): "the ordering is set by topology-trap counts, not by E_P" (§25.14).

### Q-D4. Other quantum-specific lemmas
- **Collapse lemma (F D-F2):** "CVaR score-function training equals a correlated cross-entropy method, and a collapsed bit is absorbing (its gradient is O(√m)). The warm-started circuit therefore beats SA at small budgets and freezes at large ones" (`s33/REPORT_S33.md` §9, §25.7).
- **Free energy = Gibbs / distribution-equivalence (T1–T4):** "a fully trained tempered Born machine (objective <E> − T·S) is an exact Gibbs sampler ... at best it REPRODUCES the Gibbs readout, which classical Metropolis also targets"; with a linear energy perturb-and-MAP samples are exact (`s33/SCIENTIFIC_MEMORY.md`; `s33/REPORT_S33.md` §25.3).
- **D4 sign lemma:** Q-C9.
- **Warm start is exact (S §1.4):** "First-layer RY angles 2·asin√p with later angles 0 give exactly ∏ Bern(p_q)" — so improvements are attributable to optimisation (`s33/REPORT_S33.md` §9, §25.18).
- **ADAPT:** not used; "its gradient criterion is undefined for CVaR (catalogue §4)" (`s33/REPORT_S33.md` §9).

### Q-D5. Entanglement ablations
- **Measured:** E104 VQE-L2 vs product ansatz 8W/3L at 40 q (energy); E406 decoded cloud VQE − product −0.723 (0.76x); E1000 chain VQE − product −0.688 (0.60x); E1006 2-seed −0.188 (0.26x); E1007 2-seed +0.008 (`s33/REPORT_S33.md` §9; `H_hybrid_E1006_long40.json`; `H_hybrid_E1007_mid30.json`).
- **Original interpretation:** "Entanglement changes which basins are reached, not how good they are." "entanglement has no chain effect" (`s33/REPORT_S33.md` §9, §1.4).

### Q-D6. α ablation
- **Measured:** α → 1 on A41: energy 3.69 vs 3.27, 10/10 targets (E406V) (`s33/LEDGER.md`).
- **Original interpretation:** "α is load-bearing *inside* the optimiser ... but the readout is solver-agnostic" (`s33/REPORT_S33.md` §8).

---

## E. Inherited quantum closures re-verified in Phase 1 (MAP_QUANTUM)

### Q-E1. 7-qubit candidate-index register (production's optional stage)
- **Measured:** K1 max |E − ramp| 0.0406840, 125/126 tied (native-free); circuit p_θ per target vs ramp TV mean 0.072, max 0.360; K2 closed-form p* vs circuit KL 0.9302 bits; last end-to-end measurement (S31 arm D) +0.0175 (0.35x, NULL) (`s33/MAP_QUANTUM.md` §0, §1).
- **Original interpretation:** "rows 1–13 are closed/escaped by changing what a basis state means; rows 15–16 are closed only by changing what the energy knows" (§3). Contradiction found: S31 prose "p* and the circuit's output are one fixed weighting curve per α" is "false for the circuit"; "Conclusion unchanged (it is tie noise, not target information)" (§7.1).
- **Status:** kill list "CVaR-VQE on the 7-qubit candidate-index register in any variant" (`s33/MAP_QUANTUM.md` §8); "closed by theorem (kill list); not re-opened" (`s33/REPORT_S33.md` §6).
- **Leakage:** K1/K2 native-free; K4/K5 ORACLE (verify).

### Q-E2. Historical structural registers at 9–16 aa (quoted in Phase 1)
- **Measured (inherited, as quoted):** S9 torsion register 18–32 qubits: VQE vs uniform random +0.0002 [−0.052, +0.052]; vs SA −0.0637 [−0.114, −0.014] (loses to annealing); S12 fragment assembly "the objective — not the solver — is what limits this family" (`s33/MAP_QUANTUM.md` §0.3, §2.2).
- **Status:** inherited; kill list "Short-length (9–16 aa) structural CVaR-VQE with the shipped distogram energy" (`s33/MAP_QUANTUM.md` §8).

---

## Lane and attack evidence

Relayed from importer part B, which read the lane and attack files in full; original paths cited. This agent did not re-read them. Items add to (not replace) Q-A1 … Q-E2 above; differences with REPORT / LEDGER / census are listed in `README.md` §L2.

### Q-L1. C_contact — A33 tail ensemble, A34 D4 (lane and attack)
- **Measured (lane):** A33 E306 VQE run 71 iterations, CVaR −143.6 → −179.7; parameters "3M" (3 per qubit); tail = 12 lowest distinct of 1024 final shots (`s33/LANES/C_contact/LEDGER_ROWS.md`). E307 set sizes: mean 26–27, robust 4–6, joint/optimistic 41–43; vqe_joint − vqe_mean −0.195 (SE 0.150); sa_opt − sa_mean −0.253 (SE 0.162); "a coverage effect, not a CVaR-VQE effect" (`s33/LANES/C_contact/NOTES.md`).
- **Measured (attack C5):** register re-run bit-identical (5WLF / 1KNT; 10-target subset); vqe_tail − vqe_argmin −0.17 ± 0.17 (10-target cloud); "trivial rule beats tail −0.31 ± 0.19"; per-target Spearman(tail energy, RMSD) −0.257 (`s33/VERIFICATION/attack_C_contact/ATTACK_REPORT.md`).
- **Original interpretation:** lane: "QUANTUM CONTRIBUTION: none measurable ... CVaR-VQE had a meaningful ROLE in the design ... but it does not change the answer"; "the natural place for a quantum register would be a decision the prior cannot make (none found here)" (`s33/LANES/C_contact/NOTES.md`). Attack: "The quantum stage does not change the answer. Where it differs, it is worse."
- **Status:** C5 SURVIVES (strengthened). **Leakage:** DEP (LFO caveat); ORACLE-scored cloud diagnostics.

### Q-L2. D_decoder — A81m load-bearing test (lane, attack session 2, close-out)
- **Measured (lane config):** macro4 106–114 qubits; ExactMPS RY+CZ 1 layer (χ 2); warm start = head-prior product state; α 1 → 0.1 over 6 iterations; 128 shots/it, ~64 it, 8192 distinct bitstrings; Adam 0.05; SA 128 chains (`s33/LANES/D_decoder/PREREG_E810.md`, `LEDGER_ROWS.md`). E800b restart saturation: min-E decoy RMSD at 1/2/4/8/16/32/64/128 starts 7.08/6.47/5.68/4.94/4.59/4.40/4.37/4.35 — "The global search of this energy is SOLVED by ~32-64 independent restarts" (`s33/LANES/D_decoder/NOTES.md`). Lane PREDICTION (10:25): "the load-bearing test (a) will FAIL on long40".
- **Measured (attack session 2):** claim 11 (a) FAILS — SURVIVES (strengthened): vqe − rf +0.364 (0.60x, W/L 15/30); sa − rf +0.932; cloud greedy − rf +1.383 RESULT WORSE; mid30 vqe − rf +0.807 (1.04x RESULT WORSE). Claim 12 (b) HOLDS — SURVIVES: vqe − sa −0.568 (0.48x); energy vqe < sa 40/45; second seeds 29/39, p = 0.003; SA deficit "structural at this budget, less than 1 sweep". Claim 13 "CVaR-VQE was the best register solver in energy" — REFUTED: vs random prior sampling at equal budget −3.9 nats (27/45, p 0.23); E852V second seed +1.8 (22/39, p 0.52), pooled +0.5 (19/39, p 1.0) — "CVaR-VQE is indistinguishable from sampling its warm-start prior"; greedy beats VQE on the raw objective 27/45 (6998 vs 7139); raw → polished rank correlation 0.00; mid30 random beats VQE 73%. Claim 14 quantum contribution none — SURVIVES: "Every register arm is worse than no discrete stage on the chain (long40, mid30)" (`s33/VERIFICATION/attack_D_decoder/ATTACK_REPORT.md`).
- **Measured (close-out C3):** long40 P1 +0.364 (0.60x; 0.55x on 37 non-dev targets); mid30 vqe − rf +0.807 (1.04x RESULT WORSE, type-M); cloud vqe − random +0.829 (1.04x RESULT WORSE); budget parity not met (RF used 1.45x / 1.21x evaluations, "worth <= 0.02 A"); E860V energy: VQE lower polished energy than RF on 20% (long40) / 24% (mid30), than SA 89% / 49%, than random 60% / 27% (`s33/VERIFICATION/attack_D_decoder_final/ATTACK_REPORT.md`).
- **Original interpretation (close-out recommended wording):** "H-a fails on both instruments. VQE never beats RF or random prior sampling on the built chain."
- **Status:** as above. **Leakage:** DEP, CLEAN. Simulator: ExactMPS.

### Q-L3. F_fragment — SEG-FRAG / HYBRID-FRAG (lane; attack draft)
- **Measured (lane):** E210 best energy VQE −69.7 vs SA −93.3, saP −94.9, greedy −69.4, prior +41.0 (4 dev targets). D-F2 collapse evidence: small budget VQE beats SA (2FDN smoke VQE −115.7 vs SA +91); large budget freezes (E210 1KNT VQE −124.49 vs greedy −133.4, prior-SA −140.8). E222 no-template vqe_ref − esm5_ref +0.369 (0.63x, CI [+0.05, +0.68], 5/5 positive). E230 config 15–35 qubits, 256 shots, 8000 budget (VQE max_iters cap → 3.6–4.8k distinct evals). "2GQV noted as the one case so far where the quantum stage finds a different, much better basin" (interim, 7 targets) (`s33/LANES/F_fragment/NOTES.md`, `LEDGER_ROWS.md`). "entropy bonus not tested".
- **Original interpretation:** "not decorative ... but it does not change the answer, and a no-search control (esm5_ref) does as well" (`s33/LANES/F_fragment/FAILED_E222.md`).
- **Attack:** draft only; E223V_qablation (45/45, cloud-only quantum arms q_randP, q_argmin, q_triv, q_vqe_rerefine) — per-arm numbers not in the tracked `.md` (`s33/VERIFICATION/attack_F_fragment/RESULTS/E223V_qablation/RESULT_E223V_qablation.md`). The E222V/E223V verdict "quantum null SURVIVES" is recorded only in `s33/LEDGER.md`.
- **Leakage:** DEP (LFO caveat).

### Q-L4. H_hybrid — A100 transmission and attack
- **Measured (lane NOTES):** transmission table long40 E_P / chain / traps: sa_t 3.052 / 6.343 / 13; vqe 3.057 / 5.519 / 6; vqe_prod 3.093 / 6.207 / 11; sa_p 3.222 / 5.947 / 10; random 3.535 / 4.759 / 0; demeaned slope −2.38 / −1.29 Å per unit E_P; E_D flags 98/99 traps pooled; E1006 same-solver seed |Δchain| 1.66–1.86 Å (random 0.13 Å); per-target P1 seed rank correlation 0.10; VQE ~12–17.5 s CPU per 6000 evaluations (`s33/LANES/H_hybrid/NOTES.md`). Caveat in FAILED_E1001: VQE was tuned on head4; a head8 re-tune was not run.
- **Measured (attack, `s33/VERIFICATION/attack_H_hybrid/ATTACK_STATUS.md`):** A1 reproduction 15/15 (E_P equal ≤ 3e-8; clouds bit-identical 37/45). A3 effort: VQE tuned 10 configs × 3 targets on head4 (+10 × 3 win8); sa_t 10 × 3 on head8; distinct evals long40 vqe 5967 / sa_t 5969. A4 seeds: long40 seed-2 chain P1 −0.175 (0.14x); 3-seed chain −0.355 (0.42x); cloud P1 per seed −0.829 / −0.082 / −0.176 / −1.198, 4-seed −0.571 (0.81x NOT MEASURED); traps vqe 6/9/7/6 vs sa_t 13/10/9/15 (per-target Wilcoxon p 0.015); pooled ΔE_P +0.0012 (VQE lower 51.7%); mid30 4-seed P1 +0.130 (0.27x), traps vqe 18 vs sa_t 11 (p 0.18). A5 tuned parallel tempering "not stronger on 45". A6 head8-retuned VQE "no better than E406 cfg". vqe − random 4-seed (cloud) +0.872 (1.46x RESULT WORSE, p_WY 0.0001); mid30 4-seed +0.451 (0.98x). RESULT files flagged "BASIS WARNING ... NOT ideal-geometry built chains" (cloud_as_chain).
- **Lane lessons quoted:** "Route (ii) (distribution readouts) favours the MOST diverse distribution, i.e. the untrained circuit = the prior product sampler, which is classical"; route (i) "fails on BOTH premises" of the solver-equivalence lemma; head8 register "CANNOT represent the continuous decoder's basin" (`s33/LANES/H_hybrid/NOTES.md`).
- **Status:** verdict labels not in tracked attack `.md`. **Leakage:** DEP, CLEAN.

### Q-L5. M_mid — A60 and attack C8
- **Measured (attack C8):** random sampling at equal budget ties CVaR-VQE (+0.041, SE 0.186, 0.08x; random finds the exact optimum 0/41); CVaR tail ensemble not load-bearing (−0.081, 0.19x; "tail collapsed to single state on 20%"); new seed +0.042; register vs best WHOLE member under the same H: exact −0.912 (1.73x), VQE −0.823 (1.49x), random −0.782 (1.46x) — "The register ... is worth about -0.8 to -0.9 A, not the lane's -1.7" (`s33/VERIFICATION/attack_M_mid/ATTACK_REPORT.md`).
- **Lane:** "At every length measured, the coarse-grained register used by the lanes is enumerable (18 qubits) and greedy coordinate descent solves it better than CVaR-VQE; the quantum stage changes no chain answer beyond noise." (`s33/LANES/M_mid/LENGTH_CURVE.md`). E609 partial (4–5 targets/shape): 18 q VQE hit 40% (greedy 47%, SA 13%); 20 q 33% (42%, 0%); 24 q gap/sd VQE 0.87–1.77 vs greedy 0.19–0.51.
- **Status:** C8 "SURVIVES, and strengthened against the lane". **Leakage:** DEP.

### Q-L6. P_prior — A41 and attack C4
- **Measured (lane E406):** VQE lower energy than SA 41/45, random 45/45, vqe_prod 23/45; VQE had 11 tuning configs vs SA 3 configs × 2 seeds (`s33/LANES/P_prior/LEDGER_ROWS.md`). Lane hypothesis for the win8 result: SA "T0 = sd(E of prior samples) is too hot" (`s33/LANES/P_prior/NOTES.md`).
- **Measured (attack C4):** tuned SA (2 chains, T0 = 0.3 sd; 9 configs) 3.064 vs VQE 3.057 (+0.007, 0.18x, VQE lower 24/45; SA wins 21/45); held-out 42 +0.015 (0.39x); ICM 3.111 (VQE wins 31/45); decoded cloud tuned SA 6.452 vs VQE 6.195 (0.25x). Other: α → 1 3.69 vs 3.27 (10/10; below random 8/10); top-5 vs argmin −0.056 (0.79x); cross-solver Spearman(best E, decoded cloud) 0.20; on 12 landed A41 chain rows head8_vqe 5.80 vs S4 4.44 (`s33/VERIFICATION/attack_P_prior/ATTACK_REPORT.md`).
- **Original interpretation (lane):** "on this structural register the trained circuit is a better optimiser than SA at equal budget (the E003 null does not transfer ...)"; RMSD consequence "unresolved vs SA". Attack: "the quantum stage does not change the answer relative to a tuned classical solver".
- **Status:** C4 — instance B "WEAKENED to a tie; the lane's win is an SA-tuning artefact"; instance A "REFUTED" (both in source). **Leakage:** native-free energy; cloud ORACLE-scored.

### Q-L7. S_mosaic — A11 (lane and attack)
- **Measured (lane E104, energy, 11/45):** R18 greedy 3.060 < SA 3.085 < VQE-L0 3.102 ≈ VQE-L2 3.103 < random 3.106; R32 SA 2.981 < greedy 2.994 < VQE-L2 3.058; R40 greedy 2.964 ≈ SA 2.967 < VQE-L2 2.994 < VQE-L0 3.022 < random 3.076; ORACLE cloud R40 VQE-L2 4.24 vs SA 4.67 (n = 11, "not a result") (`s33/LANES/S_mosaic/LEDGER_ROWS.md`).
- **Measured (attack):** trivial rule = VQE's own warm-start mode refined (dtop1_ref) +0.079 (0.22x, W/L 21/21); SA +0.150; greedy +0.202; random +0.295 (0.66x); VQE seed 7 +0.225; tail on states worse than the VQE's own best-evaluated state 35/42 (lane rows 37/45); energy record vs adversary SA 20/9/13 — "The VQE-vs-SA record depends on the SA implementation." (`s33/VERIFICATION/attack_S_mosaic/ATTACK_REPORT.md`).
- **Original interpretation:** lane: "the entangling circuit starts to matter as the register grows ... but SA/greedy reach lower energies at equal budget on every register size tested -- the E003 lesson holds"; "A register where the VQE could matter must be non-enumerable AND hard for local search" (`s33/LANES/S_mosaic/NOTES.md`).
- **Status:** quantum null SURVIVES (strengthened); "CVaR-VQE has a real role (it chooses the mosaic start)" REFUTED. **Leakage:** DEP.

### Q-L8. T_tempered — A70/A71 (lane; attack prereg only)
- **Measured (lane E700 cloud):** ORACLE ρ whole +0.53, lowest-1% +0.15; optimal perplexities 4k–16k of 262k; gibbsT_lfo long40 5.982 (−0.390, 1.10x RESULT, secondary). E701 at cutoff: mid30 gibbs − tail −0.306 (1.27x RESULT); P4 vs memavg −1.730 (2.48x); long40 P4 −1.005 (1.07x); vs A31.2 same 26 +0.373 (0.29x). E710 (n = 2): exact TBM 0.111 / 0.664 Å; sampled TBM 0.424 / 1.475; Metropolis 0.033 / 0.125; CVaR α 0.1 = argmin (tail perplexity 1.0) (`s33/LANES/T_tempered/LEDGER_ROWS.md`, `FAILED_E710.md`). FAILED_E710: "n < 5, conclusion rests on the theorem T1 plus E701".
- **Attack:** no ATTACK_REPORT tracked; RESULT files AT_* compare against avg75, not the attack contrasts (`s33/VERIFICATION/attack_T_tempered/`). Verdict in tracked `.md`: not recorded.
- **Lane lesson:** "Soft beats hard: ... Boltzmann-weighted mean beats the CVaR tail mean at matched support (cloud 1.12-1.53x, mid30 chain 1.27x RESULT) -- the one positive, reusable readout lesson." (`s33/LANES/T_tempered/NOTES.md`).

### Q-L9. X_short — A53 (lane; attack R1 and R2)
- **Measured (attack R2, final):** E518V full 126 chain VQE − SA −0.006 ± 0.013 (0.17x); energy SA lower 9, VQE lower 2, tie 115. C4b at 126: VQE tail − random tail cloud +0.070 ± 0.025 (1.02x, CI [+0.042, +0.111], 5/5, random better); VQE − prior ablation +0.040 ± 0.022 (0.64x); tail cloud random 3.361 < prior 3.391 < VQE 3.431 ≈ SA 3.437; VQE wins only on energy (−2.97, −1.04). C4c kill: SA tail − prod +0.249 ± 0.075 (1.19x, W/L 48/78) RESULT WORSE; VQE tail +0.243 (1.16x); the 12 E513 targets "a favourable draw" (+0.048 vs +0.271 on the other 114). C4d: tail beats argmin −0.048 cloud (1.28x RESULT), −0.025 chain (0.74x); SA tail gives the same −0.042 → "an averaging effect, not a CVaR/quantum effect" (`s33/VERIFICATION/attack_X_short/ATTACK_REPORT.md`).
- **Measured (R1):** C4c REFUTED on endpoint basis (+0.053 ± 0.198, n = 12; projection asymmetry production +0.171 vs tail +0.019); C4d REFUTED as load-bearing (−0.027 ± 0.031) (`ATTACK_REPORT_R1.md`). R2 overturns R1 on C4c.
- **Lane theory:** "at 9-16 aa the quantum stage is either decorative (A fails) or optimises an energy that does not know the answer (C fails)" (Remark 6.2, `s33/LANES/X_short/SHORT_REGIME_THEORY.md`).
- **Quantum answer (R2):** "no ... Swapping it for random sampling or for its own warm-start sampler ... makes it BETTER." **Leakage:** DEP.

### Q-L10. Y_synth — A90 (lane and attack)
- **Measured (attack):** own statevector re-implementation (ansatz agree 1e-16); L6 long40 vqe − sa +0.035 (0.43x), vqe − random +0.025 (0.52x), vqe − none +0.118, vqe − dg +0.197; "A90 is its own worst ablation" (dg 4.730 < none 4.808 < sa 4.891 < rand 4.902 < vqe 4.926). M4 mid30 vqe − none −0.359 / −0.348 / −0.400 / −0.502 (seed s3 1.12x RESULT); rand − none −0.308 (0.93x, 5/5); vqe − rand −0.041 (0.22x) → gain from "register CONTENT + energy-ranked tail readout". Q: own statevector VQE best-E vs SA 12/9/12 (long40), 8/7/15 (mid30); the lane's VQE energy "wins" are mostly sub-1e-4 ties (at 1e-4 tolerance 13/28/4 and 0/23/7) (`s33/VERIFICATION/attack_Y_synth/ATTACK_REPORT.md`).
- **Lane:** quantum-contribution rule "changes the answer only if A90 − GATE_sa AND A90 − GATE_none both RESULT BETTER"; register "mostly inert or harmful" at long40 (retrieval member used 5/45; one catastrophic swap 6ZSY 3.89 → 8.57), "informative" at mid30 (18/30) (`s33/LANES/Y_synth/NOTES.md`, `PREREG_E900.md`).
- **Status:** L6 SURVIVES (strengthened with a random twin); M4 WEAKENED ("not search"); Q SURVIVES. **Leakage:** DEP, CLEAN.

### Q-L11. Cross-lane quantum summary (as compiled from lane/attack files)
All ten lanes that tested a quantum stage report it null or worse on the built chain; adversaries SURVIVE or strengthen the null where a verdict is tracked (C, D, M, S, X, Y); F, H, T have no tracked final verdict label; P's two instances differ in wording (WEAKENED vs REFUTED). The decisive classical controls named across lanes: equal-budget and equal-tuning SA, greedy, random prior sampling / untrained warm-start circuit, exact enumeration, register-free continuous decoder, Metropolis / perturb-and-MAP twins, product ansatz, and no-search controls.
