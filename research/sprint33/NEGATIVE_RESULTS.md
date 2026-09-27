_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s33/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 33 — negative, null, killed, falsified, weakened and retracted results

Every negative / null / killed / falsified / retracted / weakened result found in the imported sources, any component. Quantum-stage negatives are summarised here and detailed in `QUANTUM_RESULTS.md` (item IDs Q-…). Per item: **Measured** / **Original interpretation** / **Status in source** / **Leakage**. Conventions: effect = arm − reference (negative better); x = |effect|/MDE (`s33/REPORT_S33.md`).

---

## 1. Primary endpoint (tuning126, 9–16 aa): nothing beat production 3.2105

### N1. E501 — S33-A50 ESM-2 attention-map prior as the stage-2 selector
- **Measured:** 3.2288 vs 3.2105, +0.018, SE 0.055, MDE 0.155, 0.12x, fold CI [−0.066, +0.100], 4/5 folds, W/L 66/60; same-job sentinel 126/126 (`s33/RESULTS/E501_prior_attn/RESULT_E501_prior_attn.md`). Corrected +0.074 (k = 4) to +0.111 (k ≈ 15) worse than a best-of-k null; Westfall-Young p 0.99; "the arm is +0.207 worse than a best-of-13 null" (`s33/REPORT_S33.md` §17; `s33/VERIFICATION/final/CLAIM_CENSUS.md` §2).
- **Original interpretation:** "a sideways move" (`s33/REPORT_S33.md` §24, FAILED_E501); "a diversity null accounts for it" (§5).
- **Status:** falsified (NOT A RESULT); X adversary SURVIVES (bit-exact reproduction). **Leakage:** DEP (CLEAN, inherited caveat: 4/126 targets verbatim in training peptides; "E501 is +0.018 with or without them").

### N2. E511 — S33-A54 esmprior_v1 as the tuning126 selector
- **Measured:** 3.3743, +0.164, SE 0.075, 0.78x, fold CI [+0.085, +0.237], 5/5 folds worse, W/L 51/75 (`s33/RESULTS/E511_esmprior/RESULT_E511_esmprior.md`).
- **Original interpretation:** "harmful"; "a protein-segment prior ... improves selection at 9–16 aa" FAILED (`s33/REPORT_S33.md` §24).
- **Status:** NOT MEASURED (harmful direction); falsified. **Leakage:** DEP.

### N3. E512 — S33-A55 chiral local prior fused into the selector
- **Measured:** 3.3979, +0.187, 0.83x, fold CI [+0.020, +0.318], 4/5 folds worse (`s33/RESULTS/E512_prior_ttz/RESULT_E512_prior_ttz.md`).
- **Status:** NOT MEASURED, harmful; falsified. **Leakage:** DEP.

### N4. E404 — S33-A40 esmprior_v1 risk top-75 on tuning126
- **Measured:** 3.3724, +0.162, 0.77x, fold CI [+0.084, +0.235], worse on 5/5 folds (`s33/RESULTS/E404_prior_tuning126/risk_m75/RESULT_E404_prior_tuning126_risk_m75.md`). esmprior_v1 MAE 2.26 (vs production 2.34) yet selection ρ 0.515 vs 0.568 (`s33/REPORT_S33.md` §12).
- **Original interpretation:** "Better MAE does not mean better selection at peptide length." (`s33/REPORT_S33.md` §12). Registered expectation (H3) was null-or-worse (`s33/STATE_LIVE.md` P_prior block).
- **Status:** FAILED_E404; reproduced as a negative by the P adversary. **Leakage:** DEP.

### N5. E504a — S33-A52 long40 incumbent transferred to tuning126
- **Measured:** 5.3480, +2.137, SE 0.230, 3.32x, fold CI [+1.72, +2.59], 5/5, W/L 25/101 (`s33/RESULTS/E504a_esm_top5avg/RESULT_E504a_esm_top5avg.md`).
- **Original interpretation:** "The long40 incumbent (−2.51 A there) is catastrophic at 9-16 aa" (`ARCHITECTURE_S33-A52.md`); "the mechanism is length-specific" (`s33/REPORT_S33.md` §5).
- **Status:** RESULT: WORSE; falsified; SURVIVES adversary. E504b (m = 75) NOT RUN. **Leakage:** DEP.

### N6. E105 — S33-A12 refinement decoder transferred to tuning126
- **Measured:** 3.5550 vs 3.2105, +0.344, SE 0.068, 1.82x, fold CI [+0.246, +0.439], 5/5, W/L 36/90 (`s33/RESULTS/E105_refine_tuning126/RESULT_E105_refine_tuning126.md`).
- **Original interpretation:** "the decoder is length-specific (FAILED_E105.md)" (`ARCHITECTURE_S33-A12.md`).
- **Status:** RESULT: WORSE; FALSIFIED. **Leakage:** DEP.

### N7. E606 — S33-A62 loglik selector on tuning126
- **Measured:** 3.4984, +0.288, SE 0.098, 1.05x, fold CI [+0.164, +0.427], 5/5, W/L 49/77 (type-M) (`s33/RESULTS/E606_tuning126_loglik_top5avg/RESULT_E606_tuning126_loglik_top5avg.md`); vs BLOSUM avg75 3.482: +0.016 (tie) (`ARCHITECTURE_S33-A62.md` v A62.2).
- **Status:** RESULT: WORSE ("harmful at 9–16 aa"). **Leakage:** DEP, CLEAN.

### N8. E812 — S33-A80 decoder on tuning126 (interim)
- **Measured:** interim n = 84/126: rf 3.523 vs production 3.227 on the same targets, +0.296 (1.10x, RESULT: WORSE, subset), fold CI [+0.10, +0.54] (`s33/REPORT_S33.md` §5; `s33/LEDGER_CONSOLIDATED.md` E812).
- **Original interpretation:** "harmful at 9–16 aa (interim)"; "cannot affect the endpoint because tuning126 routes to production".
- **Status:** RUNNING at report close (84/126); final value not in the imported files. **Leakage:** DEP.

### N9. E230 — A20 matched short null
- **Measured:** vqe 3.592, +0.381 (1.76x, RESULT: WORSE, 5/5); VQE − SA +0.007 (`s33/RESULTS/E230_short_null/RESULT_E230_short_null.md`). See Q-C5.
- **Status:** null holds. **Leakage:** DEP.

### N10. E503 / E513 / E518V — short-length registers (A51, A53)
- A51: killed by condition C (band ρ −0.011; ESM energy −0.15), no VQE compute (Q-C15). A53: killed by its pre-registered tail rule (tail cloud 3.464 vs 3.264); full-n VQE tail 3.454 (+0.243, 1.16x RESULT WORSE), VQE − random +0.070 (1.02x, random better) (Q-C16). **Leakage:** ORC diagnostic (A51); DEP (A53 chains).

### N11. Other tuning126 operators
- **Measured:** BLOSUM top-1 4.1055 (+0.895, 2.46x WORSE) (`s33/RESULTS/E601_tuning126_top1/RESULT_E601_tuning126_top1.md`); harness smoke top-1 torsions, no projection 4.1187 (+0.908, 2.45x WORSE) (`s33/RESULTS/E000_harness_smoke/tuning126/*.md`); avg75_random 3.624 (+0.142 vs avg75, 1.27x WORSE) (`s33/RESULTS/E603_length_curve/curve.md`).
- **Status:** COMPLETED (reference/control arms). **Leakage:** DEP.

### N12. tuning126 ORACLE ceilings and the "information-saturated" conclusion
- **Measured:** perfect-bin distogram inside production's readout 2.402 (chain, ORC); nonlocal-only perfect prior 2.278 / local-only 2.696 (cloud, ORC); 3.00 Å needs t ≈ 0.13 (~0.16 nats/pair) (`s33/REPORT_S33.md` §18). NMR sample condition: membrane 2.178 vs aqueous 3.431, η² 0.076 (p 0.041) (§13).
- **Original interpretation:** "the prior alone cannot reach 2.50 in this architecture"; "At 9–16 aa the answer is partly not in the sequence" (§18, §26.8). X_short: "tuning126 (9-16 aa) is information-saturated for every channel available on this box" (`s33/STATE_LIVE.md` X_short block).
- **Status:** X adversary round 2: "tuning126 saturation WEAKENED to 'inductive, not a theorem'" (`s33/LEDGER.md` E516V–E518V). **Leakage:** ORACLE (ceilings).

### N13. Not run / withdrawn at tuning126
- A56 / E505b parent-protein ESM context: NOT RUN (UniProt peptide search timed out after 4 queries) (`ARCHITECTURE_S33-A56.md`). E502 `coh` WITHDRAWN (compute; governor RAM kills); E500 `base` deferred (`ARCHITECTURE_S33-A50.md`).

---

## 2. Length-scaling and long-chain negatives (non-quantum)

### N14. E001 — S32's registered donor-control prediction at length: rule holds, mechanism falsified
- **Measured:** DONOR500 − BLOSUM500 +0.952 (1.21x, fold CI [+0.56, +1.18], 5/5, W/L 19/26); 11 template targets +3.52 (3.05x, 0/11); 34 template-free +0.121 (0.22x, NOT A RESULT); RAND 125/500/2000 hull 5.27 / 4.43 / 3.82 Å (cloud, ORC) (`s33/MAP_LONG.md` §5).
- **Original interpretation:** "By its registered mechanism ('500 points cannot fill 164 dimensions'): **FALSIFIED.**" (`s33/MAP_LONG.md` §5).
- **Status:** COMPLETED; "the S32 donor-control *mechanism* at length" listed among falsified claims (`s33/REPORT_S33.md` §24). **Leakage:** ORACLE (cloud).

### N15. BLOSUM readouts at length
- **Measured:** long40 top1 9.039 (−0.706, 0.37x NOT A RESULT); avg3 8.326 (0.93x NM); avg5 8.480 (0.97x NM); no-template targets: avg75 10.15 is the best BLOSUM readout (top1 11.46, avg3 10.32, avg5 10.26) (`s33/MAP_LONG.md` §7). mid30 avg75 8.180 equals its random-window control 8.123 (−0.057, 0.10x) (`s33/RESULTS/E601_mid30_avg75_random_d0/*.md`); long40 avg75_random +0.317 (0.39x) (`s33/RESULTS/E603_length_curve/curve.md`).
- **Original interpretation:** "KILLED at length on the chain: 'a smaller uniform prefix m fixes the readout' for template-free targets"; "KILLED as a general statement: 'the pool contains the answer' at length" (`s33/MAP_LONG.md` §9); "the BLOSUM filter has no endpoint value at 33 aa" (`s33/REPORT_S33.md` §2).
- **Leakage:** DEP.

### N16. E001-ESM contact-agreement key at mid30
- **Measured:** esm_top5avg 7.815 vs avg75 8.180, −0.365 (0.25x NOT A RESULT); esm_top1 8.133 (−0.047, 0.03x) (`s33/RESULTS/E601_mid30_esm_top5avg/*.md`, `E601_mid30_esm_top1/*.md`); in-pool ρ −0.03 at 33 aa (`s33/REPORT_S33.md` §2).
- **Original interpretation:** "the agreement key has no in-pool skill at 33 aa"; "It is scale-invariant in the contact map, so it rewards compaction on rods, which are 46% of mid30" (§2, §11).
- **Leakage:** DEP.

### N17. S33-A61 contact-mass fold-class gate at long40
- **Measured:** long40 7.465 vs esm_top5avg 7.231, +0.234 (0.28x, NOT A RESULT) (`ARCHITECTURE_S33-A61.md`).
- **Original interpretation:** "long40's M is not bimodal ... Neutral-to-harmful"; "at long40 the gate should be OFF".
- **Status:** superseded by A62 (mid30 result stands, 5.957). **Leakage:** DEP.

### N18. S33-A62 loglik selector: long40 null vs incumbent; robustness weakened
- **Measured:** long40 6.895 vs incumbent 7.231, −0.335 (0.55x, NOT A RESULT); vs gated incumbent −0.122 (0.17x) (`ARCHITECTURE_S33-A62.md` v A62.2). M adversary: defaults "sit on a sharp optimum (rank 4/75 of a loglik grid; neighbours +0.22..+1.20)"; mid30 sensitive to ESM calibration in the c < 0.01 tail (`s33/LEDGER.md` E606V/E604bV).
- **Original interpretation:** "zero free parameters / prospective": **WEAKENED**; "implicit gate": WEAKENED (`s33/LEDGER.md`).
- **Status:** mid30 validity SURVIVES (corrected −1.43, 1.40x); superseded at mid30 by A90 and A80 (`s33/REPORT_S33.md` §5). **Leakage:** DEP, CLEAN.

### N19. S33-A40 S4 selector vs incumbent weakened by multiplicity
- **Measured:** S4 6.232 vs incumbent −0.999 (1.00x, 4/5); after multiplicity 0.84–0.87x (NOT MEASURED); −strict10 0.88x (`s33/LEDGER.md` E403V; `CLAIM_CENSUS.md` §3). Pre-registered primary P2 6.702 (`s33/RESULTS/E403_prior_long40/riskesm_m5/*.md`).
- **Status:** "the claim vs the incumbent is WEAKENED"; superseded as a selector; "The prior itself underpins A31.2, A80, A90 and A100" (`s33/REPORT_S33.md` §5). **Leakage:** DEP, CLEAN.

### N20. LFO-XF leakage caveat on Phase-2 composites (A31/A31.1, A11/A12, A21)
- **Measured:** 13 cross-fold long40 pairs with NW identity > 0.40 (max 0.474, 5M4V/6Q61); 10/33 no-template targets have such a homologue's native in training (their gain −2.11 vs −1.00 on the rest). Strict-10 exclusion: 5.421 → 1.20x; 5.264 → 1.23x; S_mosaic 5.813 → 1.00x (0.89x with +S4, NOT MEASURED); F 6.037 → 0.78x (`s33/LEDGER.md` E222V/E223V; `CLAIM_CENSUS.md` §3; `s33/REPORT_S33.md` §21).
- **Original interpretation:** "every arm built on it (5.264, 5.421, 5.813, 6.037) is contaminated on ~10 targets. The clean-prior E308 (4.739) is the headline" (`s33/SCIENTIFIC_MEMORY.md`). "The clean-prior re-runs remove the caveat for the *methods*" (REPORT §21).
- **Status:** S_mosaic 5.813 WEAKENED (dropping best 3 targets 0.98x; clean-prior re-run E111V 5.617, 1.68x); F 6.037 WEAKENED (winner's-curse 1.04x; dominated by the A31 gate +0.615); A31 5.421 / 5.264 SURVIVE (corrected 1.26x) (`s33/REPORT_S33.md` §5). **Leakage:** LFO-XF (as labelled).

### N21. S33-A90 final composite superseded; weaker than its own component
- **Measured:** long40 4.915 vs E308 +0.176 (0.46x); vs GATE_noise12 (P1, pre-registered) −0.349 (0.54x NOT A RESULT; best-of-82 null share 1.51); vs gated incumbent −2.103 (1.68x) → best_of_k_accounted 0.87x (NOT MEASURED after correction) (`ARCHITECTURE_S33-A90.md` §6; `CLAIM_CENSUS.md` §2). Y adversary: "dominated by its own A31.2 component (dg 4.730 < none 4.808 < sa 4.891 < random 4.902 < vqe 4.926 — every post-DG stage moves the wrong way, n.s.)"; GATE_none − E308 (refinement) +0.066 (0.31x) (`s33/REPORT_S33.md` §5). mid30 A90 4.304: "'A90 is the mid30 best' REFUTED" by A80 GATE_rf (A90 − GATE_rf +0.489, 1.04x) (`s33/LEDGER.md` E990V/E991V). Side observation: REFINE raises the DG mean's RMSD 6.05 → 6.22 on 18 targets at cloud level (`ARCHITECTURE_S33-A90.md` §7).
- **Status:** superseded; REPRODUCED (E902 4.861); "vs incumbent after best-of-126 < 1 MDE (WEAKENED)". **Leakage:** DEP, CLEAN.

### N22. S33-A80 claims weakened or tied
- **Measured:** long40 GATE_rfp − GATE_E308 −0.396 (0.66x, NOT A RESULT); corrected 0.43–0.65x; "a best-of-k null accounts for 105–240% of the lead"; 5AL6 alone 46%; dropping the top-10 targets reverses the sign (+0.075); GATE_rfp is "a secondary arm added after dev-target ORACLE looks — the pre-registered primary is GATE_rf 4.424"; GATE_rf − GATE_E308 −0.315 (0.53x). mid30 GATE_rf − A90 −0.489 (1.04x) → Bonferroni 0.73–0.87x, Westfall-Young 0.83–0.99x, winner's curse 0.81–0.83x; 0.98x without 4HTM (`s33/REPORT_S33.md` §5, §17, §19).
- **Original interpretation:** long40 "SURVIVES as a tie"; mid30 improvement over A90 "WEAKENED (NOT MEASURED after correction)" (REPORT §19).
- **Status:** as stated. **Leakage:** DEP, CLEAN.

### N23. A80 decoder-capacity oracle weakened as a decoder comparison
- **Measured:** A80 with native one-hot bins 0.62 Å (6 dev targets, cloud, ORC); with the same native near/far map DG got: A80 4.04 vs DG 3.83 on the 6 dev targets (`s33/REPORT_S33.md` §1.3; `s33/LEDGER.md` E850V–E853V).
- **Original interpretation:** "the 0.62 Å oracle carries more information, so it shows the energy form is expressive, not that A80 decodes better than DG from equal information" (REPORT §1.3).
- **Status:** "ORACLE capacity 0.62 WEAKENED as a decoder comparison"; information floor / RF / saturation SURVIVE. **Leakage:** ORACLE.

### N24. E308 mechanism weakened; E308 vs strongest same-prior selector weakened
- **Measured:** leave-fold-out picks M = 0 asserted contacts in 5/5 folds (cloud M0 5.035 vs M1.0 5.072); E308 vs P_prior S4 with the same gate (6.121): −1.382 (1.13x, 4/5; Bonferroni-4 0.95x); 3/12 gated targets take their rank-0 window from another long40 target or its cluster — re-routed GATE 4.831 (`s33/REPORT_S33.md` §17; `s33/LEDGER.md` E308V).
- **Original interpretation:** "with esmprior_v1 the asserted top-n ESM contacts are INERT ... The gain is the learned prior + distance-geometry embedding + ensemble" (REPORT §17).
- **Status:** "MECHANISM WEAKENED"; vs S4 "WEAKENED"; vs A62 −2.156 (1.93x) SURVIVES; the E308 headline itself REPRODUCED and survives every best-of-k correction. **Leakage:** DEP, CLEAN.

### N25. Decoded-ensemble mean on the chain
- **Measured:** 12-decode mean vs single decode: cloud 5.072 vs 5.516 (1.06x, RESULT, E308 screen); on the chain −0.167 (0.75x, NOT MEASURED, C adversary) "and it compacts the chain" (`s33/REPORT_S33.md` §14).
- **Status:** chain effect NOT MEASURED; C adversary: "the ensemble claim WEAKENED" (`s33/LEDGER_CONSOLIDATED.md` E380V). **Leakage:** DEP.

### N26. E310 — selecting a DG decode by its loss
- **Measured:** averaging all 12 (5.580) beats selecting the lowest-loss decode (6.018) although ρ(loss, RMSD) +0.245 (cloud) (`s33/REPORT_S33.md` §14; `s33/LEDGER_CONSOLIDATED.md` E310).
- **Original interpretation:** "diversity beats selection" (`LEDGER_CONSOLIDATED.md`).
- **Leakage:** DEP (cloud diagnostic).

### N27. Refinement / relaxation destroys templates; gate needed
- **Measured:** A12 refinement: template stratum WORSE (+0.70) (`ARCHITECTURE_S33-A12.md`); E222: "Refinement degrades template targets (+0.67 A vs unrefined incumbent)" (`ARCHITECTURE_S33-A21.md`); relaxing a template under any energy: 1YK4 0.74 → 3.06 (`s33/REPORT_S33.md` §11).
- **Original interpretation:** "Energies with a 2–3 Å information error degrade them, so the template gate is a physical necessity" (REPORT §26.5).
- **Leakage:** DEP.

### N28. Elongated, non-globular targets remain unsolved
- **Measured:** 5AL6, 5QU8, 6Z2T, 8CMP stay at 11–15 Å under DG "even with all native contacts" (`s33/REPORT_S33.md` §13; `ARCHITECTURE_S33-A31.md`). A80/rfp rescued 5AL6 (1.73 vs E308 9.91) (REPORT §13).
- **Status:** limitation recorded. **Leakage:** DEP (ORACLE for the "all native contacts" diagnostic).

### N29. S33-A31 mirror rule failures
- **Measured:** "Mirror rule fails on ~5 beta-rich/irregular targets (ORACLE mirror is 0.34 A better on average)" (`ARCHITECTURE_S33-A31.md`).

### N30. Condition-C failures on non-VQE energies/registers used by composites
- E604 `agree` mosaic energy: +0.358, 5/10 FAIL (FAILED_E604); E607 A60.2 loglik-ranked members: 5/10 (4 exact ties where the ground state IS a whole member) FAIL; E901 A90 register +0.109 FAIL ("averaging lemma"); E903 A91 +0.018 FAIL ("information floor") (`ARCHITECTURE_S33-A60.md`; `ARCHITECTURE_S33-A90.md` §5). **Leakage:** ORACLE diagnostics.

### N31. esmprior_v2 (E407) not run
- **Measured:** none — "never started (RAM gate: 3.8 GB free never available)"; cancelled 12:20 (`s33/LEDGER_CONSOLIDATED.md` E407).
- **Status:** CANCELLED (to S34). "the top classical lever".

---

## 3. Quantum-stage negatives (summary; details in `QUANTUM_RESULTS.md`)

| ID | item | measured headline | status in source |
|---|---|---|---|
| Q-A1 | census | 34 chain rows, none a RESULT (none ≥ 0.7x) in VQE's favour at census time | "No." |
| Q-B1 | E003 engine | VQE 980–2,664 evals to optimum vs greedy 19–85; 60 q VQE ≈ random | ad hoc |
| Q-C1 | A10 subset | hull readout; QUBO wrong sign | falsified / killed (C) |
| Q-C2 | A11 mosaic, E107 | VQE→SA −0.012 (0.04x); = warm-start mode | quantum stage falsified (FAILED_E107) |
| Q-C3 | A20, E210 | vqe 8.42 vs sa 6.72 (n = 4) | A20.0 killed (C); A20.1 superseded; INTERRUPTED |
| Q-C4 | A21, E222 | vqe_ref − saX0_ref +0.177; − no search +0.175 | FAILED_E222 |
| Q-C5 | E230 | vqe − sa +0.007 | null holds |
| Q-C6 | A30 | lower-half ρ −0.038 | killed (C) |
| Q-C7 | A32 | ORACLE headroom 0.10 Å | not built |
| Q-C8 | A33, E306 | vqe_tail − sa_tail +0.065 (0.72x, VQE worse); − noise12 +0.135 | falsified |
| Q-C9 | A34, E307/E312 | robust = prior-only; joint = optimistic; chain −0.027 (16/45) | falsified; E312 INTERRUPTED |
| Q-C10 | A41, E406/E406V | 41/45 energy win vs untuned SA → tie vs tuned SA | "REFUTED" |
| Q-C11 | E1001 | tuned SA 3.394 < VQE 3.457 | FAILED_E1001 |
| Q-C12 | A100, E1000/E1003 | P1 −0.824 (0.84x NM) / gated −0.558 / mid30 +0.176; random better | FAILED_E1000 |
| Q-C13 | E1006/E1007 | seed 1 −0.066; 2-seed vqe − random +1.035 (1.35x WORSE) | FALSIFIED (VQE advantage) |
| Q-C14 | A101, E1005 | quantum tails removed: 4.352 vs 4.356 | post hoc, not claimed |
| Q-C15/16 | A51, A53 | condition C fail; full-n random beats VQE (1.02x) | killed; kill CONFIRMED |
| Q-C17 | A60, E604b | VQE 6.431 vs exact 6.341 vs SA 6.358; random ties | "decorative" |
| Q-C18 | A70, E701 | Gibbs − argmin −0.170 / −0.159 (0.33x / 0.47x) | H-Q1 falsified |
| Q-C19 | A71, E710 | Metropolis closer to exact Gibbs mean on 9/10 | FAILED_E710 |
| Q-C20 | A81/A81m, E810/E811 | register − register-free +0.364 / +0.807 (1.04x WORSE, mid30) | FAILED_E800_A81, FAILED_E810_Ha |
| Q-C22 | A90 | VQE→SA +0.026 / +0.025; stage removed +0.110 (long40) | quantum stage inert |

---

## 4. Retractions, revisions and superseded statements (within S33 and of the inherited record)

### R1. Inherited-record corrections found in Phase 1 (FALSIFICATION_CATALOGUE §2)
- C1: S8-10 "second law" (selected = 0.915·ref + 0.346) "Withdrawn in S8-13" — identity map in band (1.009·ref + 0.011); selection costs +0.049. C2: "Distance prior hard-capped at n ≤ 26" — `MAXLEN`/`SEP_BINS` belong to PairNet; the deployed per-pair MLP is evaluable at any length. C3: medoid frame choice "Measured three times" (CM). C4: probability-weighted tail average already tried (CM). C5: hull floor 1.8290 vs this audit's 1.9912 cloud (unreconciled 0.16 Å, definition/solver). C6: S12 "learned set decoder closes the decoder class" — it is a hull readout; coordinate-output decoders are PT. C7: "torsion encodings are arithmetically infeasible" — torsion registers were built (CM, not closed by arithmetic). C8: S8-10 DDPM trained on one fold, never reported (PT/NT) (`s33/FALSIFICATION_CATALOGUE.md` §2).
- MAP_LEARNED: S32's "the distogram score cannot be evaluated at 40-60 residues" is "false for the production MLP"; measured 8.933 vs 9.745 on long40 (`s33/MAP_LEARNED.md` §9). MAP_PIPELINE §7.7 agrees.
- MAP_QUANTUM §7: S31 "p* and the circuit's output are one fixed weighting curve per α" false for the circuit (TV 0.072 mean); repo MPS "O(n χ^3)" docstring false in χ; S32 "condition A fails by chain length alone" scoped to per-residue binary decisions; S30 "torsion encodings arithmetically infeasible" holds only for 7–9-qubit statevector registers; S32 "P1 alone gives QAOA, not CVaR-VQE" is "a definitional stance, not a theorem".
- MAP_PIPELINE: S32 lane L's reason for dropping the distogram at 44–60 aa "cites the wrong model" (§7.7).
- Leakage: ORACLE/diagnostic as stated in each file.

### R2. A41 "VQE better optimiser" (P_prior) → refuted
- Initial: "A41 (θ,τ) register CVaR-VQE beats SA on energy 41/45 (3.057 vs 3.222)" (`s33/STATE.md` Phase 2). Revised: "P_prior's 41/45 VQE win was an SA-tuning artefact" (`s33/SCIENTIFIC_MEMORY.md`); "the energy claim is REFUTED" (`s33/REPORT_S33.md` §5). See Q-C10/Q-C11.

### R3. D_decoder "CVaR-VQE is the best register solver" → refuted
- Initial (E810 interim): "CVaR-VQE is the best register solver (beats SA in energy)" (`ARCHITECTURE_S33-A81.md`). Revised: "'CVaR-VQE best register solver in energy' REFUTED: ties random prior sampling" (`s33/LEDGER.md` E850V–E853V); D's SA "scored worse than random sampling" (`s33/REPORT_S33.md` §1.5).

### R4. E1000 P1 lean toward VQE → not replicated
- Seed 0 −0.824 (0.84x NM); seed 1 −0.066 (0.05x); "the seed-0 −0.824 was a basin lottery" (`s33/REPORT_S33.md` §1.4). See Q-C13.

### R5. Phase-2 statement "CVaR-VQE ... beats random(prior)" → later results show random beats VQE on the chain
- Phase 2 (SCIENTIFIC_MEMORY): "QUANTUM, measured in every lane at equal energy-evaluation budget: CVaR-VQE ≈ SA ... loses to greedy on easy 18-qubit registers; beats random(prior)". Later: random-prior tail beats VQE on the chain (E1006 2-seed +1.035, 1.35x RESULT; H adversary 4-seed +0.872, 1.46x RESULT; E518V +0.070, 1.02x RESULT; M adversary random ties VQE) (`s33/REPORT_S33.md` §1.4, §5). The source does not explicitly retract the Phase-2 sentence; both are recorded.

### R6. Interim E810 figures in STATE → obsolete
- "The E810 interim figures in STATE (GATE_rf 3.503 on 13 targets; rf − E308 −0.13) are obsolete. At 43/45: GATE_rf 4.563, GATE_rf − GATE_E308 −0.321 (0.52x, NOT A RESULT)." The 12:10 interim "came from an easy subset" (`s33/VERIFICATION/final/CLAIM_CENSUS.md` §2, §4). Final 45/45: GATE_rf 4.424, GATE_rfp 4.343 (`s33/LEDGER.md` E810 FINAL).

### R7. mid30 best (STATE) → corrected twice
- "STATE.md still lists mid30 = 5.948. This is outdated." Census: mid30 best is A90 4.304, family minimum its SA twin GATE_sa 4.279 ("the mid30 best is a classical-search result") (`CLAIM_CENSUS.md` §2, §4). Later superseded by A80 E811 3.717 / 3.815 (`s33/REPORT_S33.md` §17).

### R8. Earlier "long40 deployable best" statements superseded
- MAP_LONG: gate 8.069 "the new long40 DEPLOYABLE best", then 7.018 (`s33/MAP_LONG.md` §0, §7b); map-learned 8.505 "the best long40 DEPLOYABLE-SHAPED number I know of" (`s33/MAP_LEARNED.md` §0.8); C_contact GATE_noise12 5.264; S_mosaic 5.813; F 6.037 — all superseded by E308 4.739 and A80 4.343 (`s33/REPORT_S33.md` §5).

### R9. X_short A53 round-1 estimate
- "Round 1's n = 12 estimate was a favourable draw" (`s33/REPORT_S33.md` §5); round-1 A53 chain +0.053 ± 0.198; "the A53 kill basis was biased" (`s33/LEDGER_CONSOLIDATED.md` E501V row) → full n kill CONFIRMED.

### R10. Topology-trap mechanism weakened
- H adversary: "Topology-trap mechanism reproduces but is partly definitional (WEAKENED)" (`s33/LEDGER.md` E1005/E10xxV).

---

## 5. Interrupted, abandoned, not run (recorded as such by the source)

`s33/REPORT_S33.md` §31 "Not pending, recorded as abandoned": E104 (summary not regenerated beyond n = 11); E106 (46 rows, not analysed); E312 (16/45); E302 (7-arm, superseded, stopped at 3–6 targets); E504b, E502, E505b, E720, E700-R90, E813/E814, A72 (not run); M adversary vM_chain_all2 (16/41); C adversary E381V (1/45). Also: E604bV chain job 0/41 (terminated externally 11:36, not relaunched) and E606V 0/41 (`s33/RESULTS/E604bV_qablate_mid30/*.md`, `E606V_attack_mid30/*.md`); E210 INTERRUPTED 4/45; E812 RUNNING 84/126 at close; F adversary final ATTACK_REPORT never written (usage limit) (`s33/REPORT_S33.md` §31).

## Lane and attack evidence

Relayed from importer part B (lane and attack files read in full by that agent; not re-read here). Only negatives not already recorded above, or recorded above only through REPORT/LEDGER, are added. Quantum negatives from lanes are in `QUANTUM_RESULTS.md` Q-L1…Q-L11. Differences with REPORT/LEDGER/census: `README.md` §L2.

### LN1. C_contact
- **E309 near-miss (weak prior):** separation-only prior: all top-n 8.220 vs ORACLE true subset 8.841 — "removing every false positive LOSES 0.62 A even with a weak prior"; "closes D3 as a subset register" (`s33/LANES/C_contact/NOTES.md`). ORACLE diagnostic.
- **mirror_LFO:** LFO combined mirror rule 5.884 vs catrace 5.828 (ORACLE mirror 5.490) — NULL, keep catrace (`s33/LANES/C_contact/LEDGER_ROWS.md`). DEP rule, ORACLE-scored.
- **E302:** 7-arm run stopped after 3 targets (throttled); superseded by E302b.
- **Attack (`s33/VERIFICATION/attack_C_contact/ATTACK_REPORT.md`):** C1b "noise12 best arm" WEAKENED (GATE_noise12 − GATE_dg_topL −0.157, 0.72x; "93% of the gap is the best-of-7 null"); C4b ungated noise12 vs incumbent WEAKENED (below 1.0x under every leakage exclusion: 0.99x / 0.96x / 0.97x; drop best 6 targets 0.83x); C6 leakage WEAKENED — "sensitivity set incomplete" (lane missed 1JO8, 3I35, 9EYC, 5TAB, 5WLF), "but the result SURVIVES a clean prior"; C7 contact mechanism WEAKENED (dg_topL − dg_none −0.181, 0.36x; 30% random contacts +1.37 ± 0.58 cloud); C8 ensemble WEAKENED (diversity, NOT MEASURED on chain, compacts chain Rg/native 0.912). Not completed: E381V INTERRUPTED 1/45, E382V NOT RUN, E383V stopped. Contradiction in source: strict-10 figure −1.820 (1.23x) in the table vs −1.832 (1.24x, 4/5) in the body text.

### LN2. D_decoder
- **E800d:** reference-state energy β 0.5 / 1: ρ 0.570 → 0.571 / 0.563; min-E RMSD 4.351 → 4.352 / 4.451 — "NULL" (`s33/LANES/D_decoder/NOTES.md`). ORACLE.
- **Attack session 2 (`s33/VERIFICATION/attack_D_decoder/ATTACK_REPORT.md`):** claim 1 "GATE_rfp 4.185 best long40 DEPLOYABLE" WEAKENED (full-45 4.343; vs E308 −0.396, 0.66x; Bonferroni k = 115 0.42x; WY p 0.49; vs A90 −0.572, 0.85x); claim 2 GATE_rfp − GATE_dg_topL WEAKENED (−1.079, 1.18x → Bonferroni 0.76x); claim 5 rf − E308 WEAKENED (−0.372, 0.63x); claim 7 "rfp better readout" WEAKENED (GATE_rfp − GATE_rf −0.081, 0.41x; 5EXH alone −0.071; "arm added after dev-target ORACLE looks"); claim 8 "decoder bottleneck removed" WEAKENED (equal-information oracle A80 4.04 vs DG 3.83 on 6 dev targets, W/L 2/4; 0.62 needs native 1-Å bins, rerun 0.81, CA-only 0.88). E812: "The decoder does not transfer to 9-16 aa" (84/126, +0.296, 1.10x RESULT WORSE).
- **Close-out (`s33/VERIFICATION/attack_D_decoder_final/ATTACK_REPORT.md`):** C1 mid30 WEAKENED (Bonferroni 0.87x / 0.81x / 0.73x; WY MDE 0.99 / 0.91 / 0.83x; winner's curse 0.81–0.83x; WY p 0.0045 > 0.0025; drop 4HTM 0.98x); ungated-vs-gated choice at mid30 "Not pre-registered" — "The central forking path of C1". Re-decode: 1AJJ not bit-reproducible across processes ("likely cause is MKL kernel dispatch ... The cause was not verified"); per-target chaos up to 0.95 Å (3V1A); "Means should be quoted to 2 decimals".

### LN3. F_fragment
- **E200 greedy composition:** greedy per-window-best 13.3 / 9.5 / 7.7 Å (K16/32/64) vs ORACLE-SA 4.04 / 3.54 / 3.42; top-1 assembly 17.6 (`s33/LANES/F_fragment/LEDGER_ROWS.md`). ORACLE.
- **E201 detail:** in-band +0.223 but overall −0.152 (kill < 0.15); min-E RMSD 13.73; extended chains Rg ~20 vs ~10 — energy "LANDSCAPE failure (penalty for any compaction)" (`s33/LANES/F_fragment/FAILED_E201.md`).
- **E210 interpretation:** pure de novo "loses ~4 A per target" (`s33/LANES/F_fragment/NOTES.md`). A20.3 declared "NOT run" (deviation).
- **Attack (draft only, `s33/VERIFICATION/attack_F_fragment/ATTACK_REPORT.md`):** F headline 6.037 dominated by C_contact GATE_dg_topL 5.421: F − C +0.615 (0.72x, CI [+0.33, +0.99], 5/5, W/L 12/21); no-template gains correlate 0.79 ("the same information route"); refinement "CHAOTIC" (1e-14 rad → 0.17–1.3 Å member moves on 2GQV; up to 2.7 Å at 400 steps); decode-only control +0.004 ("all of the gain is the refinement"). No final verdict label in tracked `.md`.

### LN4. H_hybrid
- **Interim superseded:** LEDGER 13:25 n = 20: P1 −0.714 (0.59x); GATE_vqe_min 2.824 — superseded by full n (`s33/LANES/H_hybrid/LEDGER_ROWS.md`).
- **Cross-job reproducibility:** 34/45 bit-identical (esmprior ~1e-8 worker noise) (`s33/LANES/H_hybrid/NOTES.md`).
- **Attack A7:** head8 register and min readout chosen by pre-registered RMSD rules on 10 long40 targets (not leave-fold-out); mid30 fold-out vs in-sample Otsu differ on 2 targets (`s33/VERIFICATION/attack_H_hybrid/ATTACK_STATUS.md`). No verdict labels tracked.

### LN5. M_mid
- **E601:** "the long40 incumbent (ESM agreement) does not transfer to 33 aa"; P3 fails (`s33/LANES/M_mid/LEDGER_ROWS.md`).
- **E607a detail:** median Spearman +0.456; argmin beats whole 5/10 (4 exact ties); "member quality dominates register design at this length" (`s33/LANES/M_mid/FAILED_E607.md`).
- **E608:** post-hoc template-gated A62 (mid30 5.584, long40 6.693) "Not claimed".
- **Attack (`s33/VERIFICATION/attack_M_mid/ATTACK_REPORT.md`):** C2 "zero-parameter, prospective" WEAKENED (eps 1e-2 +1.03, 1.14x RESULT WORSE; additive noise sd 0.05 +1.41, 1.30x RESULT WORSE; T 1.25 +0.886); C6 "A62 = implicit A61 gate" WEAKENED (rods +0.493 vs BLOSUM top1; globules tie agreement −0.442, 0.78x); C1 magnitude WEAKENED by fragility. Minor: PREREG_E600 "written ~10:30Z before any RMSD" is 2 min after the first baseline row (10:27:58Z). Deposition-era weak flag (ids ≥ 7xxx −0.86, 0.35x vs −2.52; p ~0.08) "not evidence of memorisation". Default rank "4/75" in text vs "3/75" in table (0-indexed).

### LN6. P_prior
- **E402-t:** tuning126 cloud top-75 risk 3.211 vs production 3.048 — "slightly better distance MAE but a WORSE selector" (`s33/LANES/P_prior/LEDGER_ROWS.md`).
- **Attack (`s33/VERIFICATION/attack_P_prior/ATTACK_REPORT.md`):** C1c S4 vs E001 WEAKENED (Bonferroni 0.87x / 0.84x; type-M 1.12x; fold 1 +0.07; vs gated incumbent −0.79, 0.75x); C2 P2 vs E001 WEAKENED (0.95x / 0.90x); C5 "prior adds information beyond raw ESM" WEAKENED (vs A62 cloud 6.041 vs 6.411, 0.39x; chain 6.232 vs 6.895, 0.70x; "the prior is a re-processing of ESM-2's attention maps"). Chain re-runs NOT COMPLETED (IDLE priority, deliberate). Seed retrain / homologue-clean retrain NOT COMPLETED. Infrastructure: ~3 h lost to ESM lock race, bf16 switch, launch starvation, NpzFile memory bug (`s33/LANES/P_prior/NOTES.md`).

### LN7. S_mosaic
- **E100 QUBO detail:** Spearman −0.160 to −0.195 at 4 (λ, μ); in-band −0.056 to −0.115; argmin collapses to a single member 7.596 — "The sign is WRONG at every setting" (`s33/LANES/S_mosaic/FAILED_E100.md`).
- **E101 partial:** contact-only refinement ref_c 6.221 (0.55x) "too weak" (`s33/LANES/S_mosaic/LEDGER_ROWS.md`).
- **E103 template stratum:** refinement hurts (3.29 → 4.00).
- **Attack (`s33/VERIFICATION/attack_S_mosaic/ATTACK_REPORT.md`):** headline WEAKENED ("seed-dependent (~0.2 A)", "carried by 3 targets", ~1.04–1.07x vs gated incumbent, fold 1 +0.13, "its quantum stage is inert"); decoder controls: geometry-only refinement +0.182 (2.14x WORSE); donor distogram +1.85 (2.93x RESULT WORSE) → "target-specific". Leakage: 5 non-gated structural relatives (4ZC3 ↔ 4L5E etc.); 4ZC3 is the lane's largest win. E108V_ablate and E105V not run.

### LN8. T_tempered
- **E701 at cutoff:** P1 mid30 −0.090 (0.14x); long40 −0.177 (0.36x); P2 −0.235 / +0.130 — NOT A RESULT; lane chain numbers "TIME-TRUNCATED subsets" (mid30 28/41, long40 26/45); earlier interim included pm_lfo − argmin −0.511 (1.15x, RESULT, TYPE-M) on long40 n = 15 (`s33/LANES/T_tempered/LEDGER_ROWS.md`).
- **Mechanism (FAILED_E700_R60):** "SHRINKAGE, NOT BETTER GEOMETRY" — Rg-rescaled Gibbs keeps 70% (mid30) / 20% (long40) of the cloud gain; projection penalty argmin +0.01 vs Gibbs +0.20.
- **E720 / R90:** 0 rows, NOT RUN (machine load).
- **Attack:** no ATTACK_REPORT; AT_g64o_long40 14/23 INTERRUPTED (`s33/VERIFICATION/attack_T_tempered/RESULTS/`). Verdict not recorded in tracked `.md`.

### LN9. X_short
- **E503b:** ESM-contact agreement energy on the short register: in-band ρ −0.220 mean / −0.152 median (WRONG SIGN) — "passes at L~55, fails (wrong sign) at 9-16 aa. Length changes condition C" (`s33/LANES/X_short/FAILED_E503.md`).
- **E510:** "KL, native-bin log-likelihood and gam_eff are not selection currencies" (sepnull prior better calibrated yet selects worse, set mean 4.058 vs 3.551) (`s33/LANES/X_short/NOTES.md`).
- **Attack (`s33/VERIFICATION/attack_X_short/ATTACK_REPORT.md`):** C5 information saturation WEAKENED ("inductive not theorem"; Shapley 75/25; NMR membrane class sequence-predictable, AUC 0.71); R1 documentation defect: E513b labelled pre-registered but amendment file and script share mtime 05:13:59, results 05:15; E517V (E501 seed-1 retrain) NOT RUN. RESULT-file note: E518V_a53_full headed INTERRUPTED 63/126 (+0.2593, 0.81x) and E518V_a53_full_h2 63/63 (+0.2394, 0.87x) — each half NOT MEASURED alone; ATTACK_REPORT says both halves COMPLETED and the combined 126 is RESULT WORSE (recorded as in source).

### LN10. Y_synth
- **E901 / E903c detail:** E901 x = 0 minimum on 4/18; median E(0) − E_min 0.0017; E903c energy range compressed 12x (1.401 → 0.118) vs RMSD range 1.8x — "once a structure has been relaxed into the prior, the prior cannot tell which relaxed structure is closer to the native" (`s33/LANES/Y_synth/FAILED_E901.md`, `FAILED_E903.md`).
- **Lane reading:** long40 ordering "DG 4.739 < +REFINE 4.805 < +REFINE after an SA mosaic 4.888 < +REFINE after a CVaR-VQE mosaic 4.915 (all steps n.s.)"; "the clean architecture is EQUIVALENT to the leaky best, not better" (`s33/LANES/Y_synth/NOTES.md`).
- **Attack (`s33/VERIFICATION/attack_Y_synth/ATTACK_REPORT.md`):** L3 vs incumbent / gated / A62 WEAKENED (best-of-126 residuals 0.95x / 0.79x / 0.84x); L5 "best clean arm 4.739" WEAKENED (superseded by A80 4.343: A90 − it +0.572, 0.85x); M2 A90 − A62 WEAKENED (0.76x k = 44; 0.87x k = 20); M3 "A90 is the new best mid30 deployable" REFUTED (A90 − GATE_rf +0.489, 1.04x, W/L 10/20); M4 WEAKENED ("not search"). Leakage: mid30 rule gap (P_prior mid30 exclusion lacks identity rule R3; 7OAF / 2WQ0 0.67) "with zero effect"; REFINE weights "mildly in-sample on 2 long40 folds". RESULT-file note: E991V_mid30_nogate files headed INTERRUPTED (6/8, 5/7, 0/3) while ATTACK_REPORT says the relaunch "completed 11/11".
