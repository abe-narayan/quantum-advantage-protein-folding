_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s32/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 32: negative, null, killed, falsified and retracted results

Every item below uses the same four fields:

- **Measured**: the numbers as the source records them.
- **Original interpretation**: what the sprint concluded, attributed to the file.
- **Status in source**: the verdict label the source uses.
- **Leakage**: whether the arm is ORACLE or deployable, as the source labels it.

Verdict vocabulary follows `s32/S32_CONTRACT.md` rule 1:

- < 0.7× MDE is NOT A RESULT.
- 0.7–1.0× is NOT MEASURED.
- ≥ 1.0× with a fold CI excluding zero and ≥ 4/5 folds is a RESULT.
- `stats_lib.compare` is LOWER IS BETTER, so a positive effect is a regression.

Headline: "Improvements clearing 1.0× MDE on the BUILT CHAIN, deployable: **ZERO.**" (`s32/REPORT_S32.md` §0; `s32/MULTIPLICITY.md` Running totals). The endpoint stayed at 3.2105 Å.

---

## A. Pool, filter and selection (lanes P and V)

### N-P1. Random 128-window gate instead of the score's window, at the endpoint
- **Measured:** built chain, n=126, 8 draws, all arms projected in one process.
  - ALL: +0.1648, 0.92× MDE, 52W/74L, 0 of 8 draws better, draw sd 0.0187.
  - OTHER 108: +0.2614, 1.52× WORSE.
  - FAIL18: −0.4149, 0.70×, 15W/3L.
  - Source: `s32/REPORT_S32.md` §2.2; `s32/MULTIPLICITY.md` P-41…P-43; `s32/results/s32_P_rand.json` (effect 0.16479, effect_over_mde 0.92351, other108 1.52375).
- **Original interpretation:** "The score's value is real and it is MEAN CANDIDATE QUALITY FOR AN AVERAGE. Its failure is WINDOW PLACEMENT on one target in seven. Randomising discards the first to fix the second, and the first is worth more." The registered prediction ("unchanged or worse") held.
- **Status:** NOT MEASURED overall. WORSE on the non-circular 108.
- **Leakage:** deployable, native-free ("needs **no native information at all**").

### N-P2. Random 75 of 500 (score never consulted)
- **Measured:** built chain.
  - R75 − PROD: +0.4086, 1.65× MDE, 5/5 folds, 43W/83L — WORSE. 0 of 8 draws better, draw sd 0.0381.
  - Other 108: +0.5627, 2.23×.
  - FAIL18: −0.5160, 0.94×.
  - Source: `s32/MULTIPLICITY.md` P-44…P-46.
- **Status:** RESULT, in the WORSE direction.
- **Leakage:** deployable.

### N-P3. "The score filter is worse than random at retaining the best candidate": RETRACTED
- **Measured:** CA cloud, ORACLE, 2000 draws.
  - Score top-128 vs random 128: +0.1872, 1.06× MDE, median −0.0380, 72W/54L (read backwards originally).
  - FAIL18 +1.4879 (0W/18L). Other 108 −0.0296 (0.30×, NOT A RESULT).
  - 128→75: +0.0696 (1.02×). FAIL18 +0.3611. Other 108 +0.0210 (0.38×).
  - Dropping the 10 worst targets gives +0.0294. Dropping 20 gives −0.0567.
  - Filter-independent length split: +0.1826 short vs +0.1940 long.
  - Source: `s32/LEDGER.md` S32-L3 (original), S32-L8 (retraction); `s32/MULTIPLICITY.md` D2, D3.
- **Original interpretation (S32-L3, coordinator):** "THE SCORE FILTER IS WORSE THAN RANDOM AT RETAINING THE BEST CANDIDATE".
- **Revised (S32-L8, lane V):** "The score is not a general anti-ordering… on one target in seven it places its window in the wrong part of the pool entirely."
- **Status:** **RETRACTED IN PART** at 09:01. The corrected increment sentence is: 0.595 Å (member/cloud) or 0.598 Å (chain), of which 0.338 is the order statistic and 0.257 is the 18 targets, "NOT MEASURED on the other 108".
- **Leakage:** ORACLE / NOT DEPLOYABLE (diagnostic).

### N-P4. BLOSUM top-75 vs score top-75 on the best member (third FAIL18-circular instance)
- **Measured:** −0.2020 overall (1.14×, RESULT). FAIL18 −1.5871 (18W/0L). Other 108 +0.0288 (0.26×, NOT A RESULT). Median exactly 0.0000. (`s32/MULTIPLICITY.md` V-A10; P-09 gives −0.2021, 1.06× TYPE-M.)
- **Original interpretation:** "any comparison of the score's prefix against an alternative prefix, scored on the BEST MEMBER, is entirely FAIL18". This is registered as "a general property of the instrument" (`s32/REPORT_S32.md` §0.6, Appendix B).
- **Status:** NOT A RESULT off the circular stratum.
- **Leakage:** ORACLE.

### N-P5. Deployable 500→75 filter on the best-member axis
- **Measured:** +0.2286, 1.18×, 63W/63L, WORSE (P-07). Stratified: mean +0.2260, median +0.0046. FAIL18 +1.7713 = 112%. Other 108 −0.0316 at 0.27× (P-35). The mean axis for the same filter is −0.9030, 4.01× BETTER (P-08).
- **Original interpretation:** "Every filter in the pipeline buys the set MEAN at ≥ 4× MDE and buys nothing on the BEST axis… It is throwing away UNREACHABLE quality" (`s32/LEDGER.md` S32-L(P1)).
- **Status:** best-axis loss is NOT A RESULT off FAIL18.
- **Leakage:** ORACLE labels (cloud).

### N-P6. Retrieval (universe→500 BLOSUM) on the best-member axis
- **Measured:** −0.0718 (0.89× in S32-L(P1); P-01 gives −0.0735, 0.89×). FAIL18 contributes 0%. Other 108 −0.0833 at 0.98× (P-36).
- **Original interpretation:** "Retrieval is not the problem." Its best-member contribution is "unmeasured" (`s32/REPORT_S32.md` §2.0, §2.1).
- **Status:** NOT MEASURED.
- **Leakage:** ORACLE.

### N-P7. 128→75 score prefix
- **Measured:** best axis +0.0684, 0.98× (P-05). Mean axis −0.0349, 0.71× (P-06).
- **Status:** NOT MEASURED on both axes.
- **Leakage:** ORACLE.

### N-P8. Prefix length `m` (S31 closure restated and not reopened)
- **Measured:** ORACLE global `m*`=72 gives −0.0044 (0.19×). Leave-fold-out `m` gives +0.0075, 63W/63L, "a literal coin flip". A matched random-subset family reaches 141% of the prefix family's gain (lag-1 autocorrelation 0.917 vs 0.112) (`s32/REPORT_S32.md` §2.1; `s32/CAUSAL_MAP.md` arrow 3).
- **Original interpretation:** "this arrow is an order statistic, not a lever. **Do not re-open the `m` axis.**"
- **Status:** closed (S31 result, restated in S32). Note: `s32/LEDGER.md` S32-L1 quotes the LFO `m` as "+0.0075, 0.22× MDE".
- **Leakage:** ORACLE (m*) / deployable (LFO).

### N-P9. Operator-law prediction (set_mean coefficient ≥ 5× set_best): FAILED
- **Measured:**
  - Built chain, 17 arms: `out = −0.9934 + 0.9219·set_mean + 0.3232·set_best`, ratio 2.85, R² 0.9162 (P-47).
  - Cloud: ratio 2.07 (0.6730 / 0.3256) (P-30).
  - Out-of-sample: R128 predicted +0.144, measured +0.1369 (HIT). R75 predicted +0.524, measured +0.3740 (MISS by 0.150) (P-39, P-40).
- **Original interpretation:** "S18's `1.16 / 0.04` (ratio 29) does not hold under a gate that orders candidates — the set BEST does reach the output, about a third as hard as the set mean." "The law is a local linearisation."
- **Status:** registered prediction FAILED. The report calls it "the one arm this sprint's data argues *for*", and that arm is untested.
- **Leakage:** set statistics use ORACLE labels.

### N-P10. "READOUT is the largest decomposition cell": partly FAILED
- **Measured:** CA cloud, ORACLE. Ranking alone (ORACLE top-75 through the deployed average) −1.0853 (4.26×). Readout (ORACLE convex over the same 75) −1.0508. Both together −1.9316 (`s32/LEDGER.md` S32-L(P1)).
- **Status:** "Readout and ranking are **tied** (−1.05 vs −1.09)" (`s32/REPORT_S32.md` §8, Appendix A).
- **Leakage:** ORACLE / NOT DEPLOYABLE.

### N-P11. Negative in-band ρ of consensus as a collider artefact: FAILED
- **Measured:** ORACLE band. ρ(CONS, a) = −0.2745 ± 0.0366, negative on 78.6%, which fails the registered ≥ 80% bar though the sign is confirmed. The shuffled-U collider control gives +0.1387 ± 0.0214. Removing μ flips ρ to +0.7046 ± 0.0096 (`s32/MULTIPLICITY.md` P-12, P-13, P-15).
- **Original interpretation:** "the collider alone produces the WRONG sign, so the negative needs the real U–V dependence". "The negative sign is caused by μ and by nothing else."
- **Status:** registered collider prediction FAILED. P3-2's 80% bar FAILED.
- **Leakage:** ORACLE.

### N-P12. Native-free estimates of the common-mode direction μ
- **Measured:**
  - Seven native-free directions: best cos(μ̂, μ) = +0.0568 ± 0.0434, below the crossing point cos* = 0.2137.
  - Distogram gradient: −0.0140 ± 0.0095.
  - Mismatched same-length native: −0.0088 ± 0.0235. Mean of same-length natives: −0.0080 ± 0.0419. Shared-referent floor +0.0512 ± 0.0342.
  - Source: `s32/MULTIPLICITY.md` P-17, P-31…P-33; `s32/LEDGER.md` S32-L(P1).
- **Status:** all below the price. P3-6's deployable test did not fire.
- **Leakage:** native-free estimates, ORACLE-scored.

### N-P13. PC1 / sign route
- **Measured:** cos²(μ, PC1) = 0.2277 vs random 0.0316 (7.21×). The placebo (mismatched native) gives 0.2024, i.e. 87.1% placebo. One perfect bit with a global LFO step is worth +0.1835 Å. The best of nine native-free sign rules gives +0.0032 Å (1.7% of that), at accuracy 0.5952 (P-21…P-24).
- **Original interpretation:** "Two controls killed it." "One bit plus one real, not one bit."
- **Status:** "opened and closed inside the lane".
- **Leakage:** ORACLE bit. The rules are native-free.

### N-P14. Spread maximisation above a score floor (coordinator arm)
- **Measured:** CA cloud screen.
  - SPREAD vs PROD: +0.6447 / +0.1796 / +0.0436 / +0.0076 at floors 25/50/60/75%.
  - SPREAD vs RANDFLOOR: +0.4196 / +0.0864 / −0.0104 / −0.0039.
  - LFO floor: +0.0076, 0.11×. It converges on production.
  - Source: `s32/MULTIPLICITY.md` P-25…P-27.
- **Original interpretation:** "spread does no work at any floor". "Closed by its own control — `SPREAD − RANDFLOOR ≈ 0`" (`s32/REPORT_S32.md` §8).
- **Status:** closed.
- **Leakage:** deployable-shaped (cloud screen only).

### N-P15. Quality-blind dispersion maximisation (S31 figure, re-read through S32-L2)
- **Measured:** +0.1436 Å, 1.22× MDE, WORSE (S31, quoted in `s32/LEDGER.md` S32-L2 and `s32/THEORY_Q.md` Objective A item 14).
- **Original interpretation:** "`a` is load-bearing and it is the only unknown."
- **Status:** closed.

---

## B. Readout and quantum reformulation (lane Q)

Full detail is in QUANTUM_RESULTS.md. Negatives listed for completeness:

- **N-Q1. Sparse s-of-K.** "Closed by monotonicity". `s*` mean 10.06, 61.1% ≤ 10 (`s32/LEDGER.md` S32-L(Q1)). ORACLE.
- **N-Q2. Hull projection of a noisy estimate.** Killed by a norm-matched shrinkage control. It is WORSE at ε ≤ 1.5 (+0.370 / +0.265 / +0.170) and better only at ε = 4.0 (−0.137, 1.59×, median −0.074, "concentration warning") (`s32/LEDGER.md` S32-L(Q2); `s32/THEORY_Q.md`). ORACLE, CA cloud.
- **N-Q3. "Gain exactly 1 means no noise suppression": STRUCK.**
  - Measured: gain 0 on ≈33 dimensions. "~87% of a generic error annihilated". At ε = 4.0, a 3.65/3.66 Å estimate emits at 2.23 Å.
  - Original (coordinator and lane Q): "gain exactly 1 means no noise suppression".
  - Status: "**Backwards**". The headline survives "on the **hull floor** `d = 1.8290`" (`s32/THEORY_Q.md` Q1-T2(c)3; `s32/LEDGER.md` S32-L5; `s32/STATE.md` NOTE 2).
- **N-Q4. Q0 tie channel.** S31's target-invariance is "NOT falsified, and is now sharper". Residual 0.26× (cloud). Selection readout "identically tied 126/126". Block-relocation control 0.38× (`s32/THEORY_Q.md` Q0).
- **N-Q5. Objective A (CVaR over a quality posterior).** Closed by classical equivalence: a Gaussian posterior gives a second-order cone program (`s32/THEORY_Q.md` Q2).
- **N-Q6. Charter §14.** "NO, on this instrument", because of chain length (`s32/LEDGER.md` S32-L(Q3)).
- **N-Q7. FISTA solver defect.** A 4000-iteration FISTA with a drop-only polish passed a 3-target smoke test, then failed its KKT certificate (residual 1.26 at K=128, 10.85 at K=500). "Every sensitivity number from that run was invalid and none was reported." It was replaced by Lawson–Hanson NNLS, certificate 2.0e-12 (`s32/LEDGER.md` S32-L(Q1)).

---

## C. Reconstruction / projection (lane R, audited by lane V)

### N-R1. Chiral Ramachandran branch criterion (the coordinator's hypothesis that opened lane R): FALSIFIED
- **Measured:** in-band ρ across the branch set: `rama_nlp` +0.0153, fold CI [−0.0461, +0.0608], median −0.0740, positive on 54/126. For comparison, `d_to_C` +0.1122, `obj1` +0.0742, `disto_risk` +0.0702, `obj0` +0.0603 (`s32/LEDGER.md` S32-L(R4) R3; `s32/REPORT_S32.md` §5.5).
- **Original interpretation (hypothesis):** "every native-free ranker is a distance-map function and therefore achiral, so a chiral criterion should see what they cannot" (`s32/CAUSAL_MAP.md` thesis; `s32/STATE.md` headline).
- **Revised:** "The ACHIRAL distance-map channels beat the chiral one FOUR TO ONE." P3.2 and P3.3 FALSIFIED, "and so is the reasoning that produced it". Report: "the cleanest negative in the sprint and it is the coordinator's."
- **Status:** FALSIFIED.
- **Leakage:** criteria are native-free. ρ uses ORACLE labels.

### N-R2. P3.1 (projection's own objective is blind in band): FALSIFIED
- **Measured:** `obj1` +0.0742 and `obj0` +0.0603, both fold CIs excluding zero (`s32/LEDGER.md` S32-L(R4)).
- **Status:** FALSIFIED (the objective is not blind).

### N-R3. P3.4 (a native-free branch selector beats production by ≥ 1 MDE): FALSIFIED
- **Measured:** best of 29 deployable arms `SEL_d_to_C_GEN4+MEM75` −0.0100, 0.61× MDE, "before charging the search" (`s32/LEDGER.md` S32-L(R4); `s32/MULTIPLICITY.md` R-7).
- **Status:** FALSIFIED.
- **Leakage:** deployable.

### N-R4. Sixteen criteria × two directions branch search (lane V)
- **Measured:** 64 comparisons, built chain, paired in-job. Every ARGMIN is < 0.7× or worse. Examples: `d_to_C` −0.0091 at 0.57×; `disto_risk` +0.0571 at 1.13× WORSE; `disto_mae` +0.0549 at 1.03× WORSE. Every ARGMAX is WORSE at 1.88–2.76×. On GEN4-only, "nothing is a result in either direction, largest 0.46×". `vbond_mean`/`vbond_sd` are degenerate ("204 of 204" or "203 of 203" branches tied) (`s32/REPORT_S32.md` §5.5; `s32/MULTIPLICITY.md` Lane V section).
- **Out-of-sample search value against production:** quoted variously as +0.0004 CI [−0.0091, +0.0116], +0.0026 CI [−0.0067, +0.0141], and +0.0028 CI [−0.0054, +0.0128]. All CIs straddle zero. See LESSONS.md, Importer notes.
- **Original interpretation:** "Native-free observables have real skill at avoiding disasters and none at finding winners." Report §0: "the third time in the sprint that exact asymmetry appears — after the score prefix and after consensus."
- **Status:** no improvement. ARGMAX RESULTs are in the worse direction.
- **Leakage:** deployable arms.

### N-R5. ORACLE best-branch ceiling is mostly an order statistic
- **Measured:** built chain, ORACLE / NOT DEPLOYABLE.
  - ALL (K=158): 3.0941, −0.1165, 3.43×.
  - Best-of-K pricing: ALL oracle −0.1210, split-half −0.0046 (4%). RAND0 control transfers 3%.
  - The K=8 row replicates S31-D: 3.1168, −0.0938, 2.92×, 114W/0L.
  - Source: `s32/LEDGER.md` S32-L(R4); `s32/results/s32_R_analysis.json` (ALL mean 3.09406, effect −0.11648, effect_over_mde −3.43276).
- **Original interpretation:** "96% of the ORACLE branch ceiling does not survive a split half."
- **Status:** NOT A SIGNAL.
- **Leakage:** ORACLE.

### N-R6. GEN4D named-start choice: transferable but redundant
- **Measured:** the GEN4D family transfers 60%. Leave-fold-out gives +0.0081, 0.28× MDE, 2/5 folds (`s32/MULTIPLICITY.md` R-16).
- **Original interpretation:** "A real, transferable, completely redundant signal is a sharper negative than a null." Production's argmin already reaches the α-helix start.
- **Status:** NOT MEASURED.
- **Leakage:** deployable.

### N-R7. Production's multi-start argmin vs a random branch
- **Measured:**
  - Lane R: random branch over 5 draws 3.2106 (draw sd 0.0028) vs PROD 3.2105; branch-set mean 3.2151 (+0.0045, 0.28×).
  - Lane V: 300 draws, "+0.0049 ± 0.0079". The artefact `s32/results/s32_V_R_adversary.json` records vs_prod 0.00405, draw_sd 0.00758.
  - Source: `s32/LEDGER.md` S32-L(R4); `s32/MULTIPLICITY.md` Lane V.
- **Original interpretation:** "Production's multi-start argmin is worth **0.0001 Å** over a coin" (lane R). Also "worth 0.005 Å over a coin" (lane V). Both sentences appear in `s32/REPORT_S32.md` §5.5.
- **Status:** null.
- **Leakage:** deployable.

### N-R8. Scalar dilation of the cloud (registered P1.3): FALSIFIED
- **Measured:** CLOUD basis, n=126. Dilate to the ideal virtual bond: +1.0425, 2.79× MDE, 5/5, WORSE. Rg-matched dilation: +0.0622, 1.47×, WORSE. ORACLE best dilation on a grid: −0.158. Contraction is 22.15% at |i−j|=1 and 5.40% in Rg (`s32/LEDGER.md` S32-L(R3); `s32/results/s32_R_dilation_cloud.json` effect 1.04245, 2.78951×).
- **Original interpretation:** "the contraction is **separation-dependent**… One scalar matched to one moment is wrong at the others." It also reconciles "the '3.5% contraction' in project memory and `core/project.py`'s '2.96 against 3.80'".
- **Status:** FALSIFIED by its own falsifier. Provenance was re-cleared at `63608f9d` (`s32/REPORT_S32.md` §5.3).
- **Leakage:** deployable (ORACLE grid labelled).

### N-R9. Repair arms on the chain
- **Measured:** built chain.
  - SCALE_NF: +0.7219, 2.24×, WORSE, 5/5.
  - SCALE_NF_MED: +0.7228.
  - SCALE_GRID per-target ORACLE: −0.1352 (3.84×), "122% accounted by the across-target null". Its leave-fold-out factor is +0.0044 at 0.14×.
  - MEDOID_EXTRA: −0.0064, 0.35×. Its fold CI excludes zero and 4/5 folds agree, but "the MDE gate binds: NOT MEASURED".
  - Source: `s32/LEDGER.md` S32-L(R4) R4; `s32/MULTIPLICITY.md` R-17, R-18.
- **Status:** WORSE / NOT MEASURED. The scale grid's split half (−0.0497) is "centred on the GRID MEAN and must NOT be quoted vs production".
- **Leakage:** deployable, except SCALE_GRID per-target (ORACLE).

### N-R10. Sparsity and alignment are not levers
- **Measured:** built chain, same s=10, same job.
  - ORACLE members: price +0.0002, cos +0.380.
  - RANDSPARSE (3 draws): +0.1988, cos +0.019, 0.22×.
  - SCORESPARSE (top-10): +0.1371, 1.46× on the WRONG side of its orthogonal null.
  - PROD: +0.1622 vs null +0.1504, 0.24×.
  - Source: `s32/LEDGER.md` S32-L(R1); `s32/results/s32_R_sparse_control.json`.
- **Original interpretation:** "The cheap price was ORACLE-induced." "Every object the native did not touch sits at or above its own orthogonal null." "Neither sparsity nor alignment is an available intervention."
- **Status:** closed.
- **Leakage:** ORACLE (sparse) / deployable (score, random).

### N-R11. Coordinator mechanism "sparse combinations barely leave the manifold": FALSE
- **Measured:** sparse `d` 0.844 vs production 0.705 (n=16 interim). At n=126: sparse 0.7023, production 0.8150 (`s32/LEDGER.md` S32-L9, S32-L(R1)).
- **Status:** corrected in place (contract rule 16). The Appendix A entry reads "Sparse sits **farther** off-manifold (0.8503 vs 0.8150)". See the Importer notes in LESSONS.md.

### N-R12. "λ = 0.3 costs +0.0107 at the endpoint": RETRACTED
- **Measured:** same cloud, same job: +0.0055, SE 0.0057, 0.35×, 57W/69L (`s32/LEDGER.md` S32-L(R4); `s32/MULTIPLICITY.md` R-2).
- **Status:** "A cross-job difference, not an effect". NOT MEASURED.

### N-R13. Lane R's explanation "λ=0.3 branches must all already be Ramachandran-plausible": REFUTED by its own data
- **Measured:** positive-φ spread 0.632. 31.2% of branches sit above the 17.5% unconstrained rate. 126/126 targets carry such a branch, against a real-library rate of 5.40% (`s32/results/s32_R_rama_headroom.json` as cited in `s32/LEDGER.md` S32-L(R4)).
- **Original revised interpretation:** "Ramachandran plausibility and native proximity are ORTHOGONAL among the branches this projection admits". This is S9-2 re-derived.
- **Status:** refuted.

### N-R14. Other reconstruction-lane corrections
- `n_distinct` was "A greedy-seed count, not connected components". Union-find changed 39 of 126 targets (`s32/LEDGER.md` S32-L(R4)).
- "3.210533994943299 to sixteen digits" was asserted by `s32_R_verify.py` and FAILED. Summation order gives `...300`. "The bit-identity claim is PER-TARGET" (`s32/LEDGER.md` S32-L(R1)).
- The PREREG_R assertion that the S29 cloud is bit-identical to the cache `avg_ca` is "FALSE": 0 of 126 are identical, max |Δ| 5.7e-14 (`s32/PREREG_S32_R.md`, annotated in place).
- `s32_R_gen4d_start.json` "had a committed script that **had never actually run**, dying on a `KeyError`" (`s32/REPORT_S32.md` Appendix A).

### N-R15. Projection as earliest irreversible loss: NO
- **Measured:** spearman(d, mean pairwise member RMSD) +0.9646; permutation null max +0.466. Price +0.1622 = 5.05% of the endpoint (`s32/LEDGER.md` S32-L(R2)).
- **Original interpretation:** "The reconstruction stage faithfully transmits an upstream defect; it does not create one."
- **Status:** exploratory (R-13). The relation is "monotone, not a proportionality" (cv 0.467).

---

## D. Physics and dynamics (lane D)

### N-D1. Static in-band ranking by AMBER, Legacy, DIS and RG
- **Measured:** in-band Spearman, top-75, n=126.

  | scorer | ρ | × MDE |
  |---|---|---|
  | AMBER | +0.0000 | 0.00 |
  | DIS | +0.0652 | 0.83 |
  | LEG_total | +0.0376 | 0.42 |
  | LEG_torsion | +0.0444 | 0.65 |
  | RG | +0.0501 | 0.44 |

  AMBER over the whole pool is −0.0266, the wrong sign (`s32/MULTIPLICITY.md` D-1…D-7; `s32/LEDGER.md` S32-L(D1)).
- **Original interpretation:** "AMBER ranks, sign-ambiguously." DIS and LEG_torsion "reproduce S31 §9's own two figures exactly".
- **Status:** NOT A RESULT / NOT MEASURED.
- **Leakage:** native-free scorers. ORACLE labels are used for evaluation only.

### N-D2. Chiral Cα pseudo-torsion in band; registered "< 15% in-band variance share": FAILED
- **Measured:** chiral in-band +0.0607, 0.58×. Whole-pool +0.3302, 2.85×. In-band share of chiral variance 23.6% (`s32/MULTIPLICITY.md` D-10…D-12).
- **Status:** registered prediction FAILED ("recorded as a fired falsifier").

### N-D3. Sign sharing between Hamiltonians
- **Measured:** AMBER vs LEG_total sign agreement 36.5% (z −3.0). AMBER oriented by LEG_total's sign: −0.0508, 0.92×, "the wrong way". Oriented by DIS: −0.0108, 0.19× (`s32/MULTIPLICITY.md` D-18…D-29).
- **Original interpretation:** a native-free vote fails because Legacy tracks compactness and AMBER anti-tracks it.
- **Status:** NOT MEASURED / NOT A RESULT.

### N-D4. H-D2 (basins are not operative at 9–16 residues: contraction or frozen): FALSIFIED
- **Measured:** 10 native-free-chosen targets, 24 candidates each, free AMBER relaxation, 97.5% converged. Spread ratio 0.972 (horn ≤ 0.70). Median move 0.5006 Å (horn ≤ 0.30) (`s32/MULTIPLICITY.md` D-40, D-41).
- **Original interpretation:** "The scope excuse this lane was entitled to use is not available".
- **Status:** FALSIFIED (the lane's own hypothesis).

### N-D5. Minimised AMBER in band
- **Measured:** n=10, DIAGNOSTIC. Relaxed in-band ρ −0.0089 vs single point +0.0006. Energies 3.18e9 → −558 kcal/mol for 0.50 Å of Cα motion. Band mean −0.0083. Best member +0.0382 (worse). Rank preservation 0.9208 (`s32/MULTIPLICITY.md` D-42…D-45).
- **Original interpretation:** "AMBER's entire dynamic range on this pool is spent on a rotamer-placement artefact that carries no candidate information".
- **Status:** minimisation "does not rescue AMBER".

### N-D6. D3-M physics as mover (the lane's primary registered arm): FAILED, and the endpoint regresses
- **Measured:** built chain, n=126, same process; PROD rebuilds to 3.2126.

  | rung | cos(Δd, −e_prod) | × MDE | endpoint Δ | × MDE | W/L |
  |---|---|---|---|---|---|
  | k=100 | +0.0057 | 0.09 | +0.0204 | 0.84 | 23/103 |
  | k=10 | +0.0412 | 0.63 | +0.0336 | 1.26 | 40/86 |
  | k=1 | +0.0555 | 0.69 | +0.0726 | 1.96 | 33/93 |
  | k=0 | +0.0651 | 0.73 | +0.0985 | 2.21 | 35/91 |

  All endpoint rungs are 5/5 folds. Surplus over a magnitude-matched random direction: 0.12–0.71×. All 12 scale-ladder arms are positive (worse), best +0.0039. Relaxed chains dilate 1.2–1.7% (`s32/LEDGER.md` S32-L(D3); `s32/MULTIPLICITY.md` D-76…D-91).
- **Original interpretation:** "The physical relaxation displacement is, to the resolution of this instrument, indistinguishable from a random direction of the same length." "Every use of a force field on this pipeline is now closed." The dilation mechanism is "a named candidate mechanism, not a demonstrated one" (no dilation-only control was run).
- **Status:** registered prediction FAILED. Endpoint RESULT in the WORSE direction.
- **Leakage:** cos is ORACLE. The endpoint arm is deployable.

### N-D7. D4-P (pairwise barrier F‡) NOT RUN
- **Status:** not run. The registered gate on D3-M showing a positive cos was not met. Corollary D-E4 leaves it "not closed" (`s32/LEDGER.md` S32-L(D3)).

### N-D8. Native-free supply of the per-target sign: NO
- **Measured:**
  - D4-S, leave-fold-out ridge on 20 native-free features. Oriented ρ: AMBER −0.0355, DIS +0.0674, LEG_total +0.0373, LEG_torsion +0.0444. Excess over shuffled: 0.10–0.59×.
  - D4-M, accuracy vs marginal: AMBER 0.381 vs 0.508 ("worse than constant"); DIS 0.548 vs 0.548; LEG_total 0.595 vs 0.587 ("one target in 126"); LEG_torsion 0.556 vs 0.556.
  - D4-X, `sign(rg_pred − rg_pool)`: positive on 81.0% of targets; corr +0.199; all arms < 0.7×.
  - Source: `s32/MULTIPLICITY.md` D-46…D-53, D-64…D-66.
- **Original interpretation:** "No scorer's sign is predictable above its own marginal." "A one-bit feature that is 81/19 cannot carry a 59/41 label."
- **Status:** closed. REPORT §10 lists "the per-target sign as a route" under "Do not re-open".
- **Leakage:** deployable features.

### N-D9. Zero-information (constant +1) sign arms
- **Measured:** CLOUD: +0.027 to +0.092 worse than PROD (D-55, D-57, D-59). Chain: const +1 is +0.0896, 0.90×, 49W/77L (D-74).
- **Original interpretation:** "selecting the best 25 by an unsigned scorer costs +0.027 to +0.092 Å".
- **Status:** worse / NOT MEASURED.

### N-D10. The chirality/filter cross-lane synthesis: CIRCULAR
- **Measured:** variance retained under the score-75 filter (random-75 retains 0.96–0.98): DIS 0.037, RG 0.111, achiral twin 0.196, chiral 0.271, lane V's `RR_ORACLE` 0.272. Chiral minus twin: +0.0755 (2.35×) (`s32/MULTIPLICITY.md` D-30; `s32/LEDGER.md` S32-L(D2)(d)).
- **Original interpretation (coordinator proposal, S32-L7):** the filter removing 79% of chiral variance and the score halving the spread "may be the same event seen from two sides".
- **Revised:** "Lane D's 0.271 and lane V's 0.272 are the same number to three decimals: one fact, not two." "The synthesis is circular and must not be written down."
- **Status:** "CIRCULAR — controlled and refuted before it was written down" (`s32/REPORT_S32.md` §8).

### N-D11. The 500→128 chiral arm: NOT RUN "by derivation"
- **Measured:** the achiral twin reaches the same global magnitude with the opposite sign (−0.3359 vs +0.3302). Chiral with DIS partialled out: +0.1302 (`s32/MULTIPLICITY.md` D-31…D-35).
- **Original interpretation:** "the G1 escape is not what is doing the work here, for the third time in this project (WRITHE S30-L26, XTWIST S31 §9, this)".
- **Status:** not run.

### N-D12. Classes closed by theorem before compute
- **Theorem D-E** closes MD, ensembles, basin populations, metastability, rates, autocorrelation, dynamic modes (charter §23) and §24's ensemble reweighting and temperature response "as scalar rankers".
- **Theorem D-F** closes "every physics/prior consistency scalar".
- **§0.2c:** "AMBER has no resolution advantage" (the all-atom structure is Ψ(seq, φ, ψ)).
- "AMBER is not a chiral scorer… This project has no chiral scorer at all."
- Source: `s32/PREREG_S32_D.md` Part 0; `s32/REPORT_S32.md` §8.
- **Status:** closed by derivation.

---

## E. Length generalisation (lane L)

### N-L1. L-H1 (the representation is the obstacle at 40–60 residues): FALSIFIED
- **Measured:** deployed projector on the native, λ=0, ORACLE. PROJ_NAT_SHORT 0.0429 (n=126). PROJ_NAT_LONG 0.7002 (n=60, L 41–60, p90 0.956, max 1.129). The registered falsifier was "< 1.0 Å at L = 45" (`s32/LEDGER.md` S32-L(L1-L4); `s32/MULTIPLICITY.md` L-1).
- **Original interpretation:** "the representation is not the obstacle at 40-60 residues". The native-torsion rebuild (`0.0299 · L^1.239`) "overstates the distance to the emittable set by 3.9× at L ≈ 52 and 8.1× on the canonical 126". The library admission gates `REBUILD_TOL` "do not follow". This was "Not acted on".
- **Status:** FALSIFIED by its own registered falsifier.
- **Leakage:** ORACLE.

### N-L2. The sequence channel strengthens with length: NOT SUPPORTED
- **Measured:** in-band Spearman inside K=500: −0.0464 at L≈13, +0.0261 at L≈55 (the wrong sign). Contrast 0.83×, NOT MEASURED (`s32/MULTIPLICITY.md` L-3d).
- **Status:** hypothesis NOT SUPPORTED. `structure-and-sequence-are-decoupled` "survives at length".

### N-L3. Registered admission filter (`identity(norm="shorter") ≥ 0.4`): discarded
- **Measured:** it rejected 140 of 170 monomers and left zero targets. It rejects 100% of real and 100% of shuffled sequences at every threshold ≤ 0.9. The verbatim-substring statistic separates them (real 0.330, shuffled 0.000) (`s32/MULTIPLICITY.md` L-3).
- **Status:** "It was measuring chance, not leakage". It was replaced before any RMSD existed.

### N-L4. Filter skill does not replicate at length
- **Measured:** built chain, `avg75 − avg75_random`: −0.1421 (1.27×, RESULT) at L≈13 vs −0.3171 (0.39×, NOT A RESULT) at L≈55 (`s32/REPORT_S32.md` §7.2; `s32/results/L2_ladder_verdict.json`).
- **Original interpretation:** "BLOSUM's endpoint filter value does not replicate at length."
- **Status:** NOT A RESULT at length.

### N-L5. Prefix size m at length (a lead, not a result)
- **Measured:** CA cloud, one global out-of-fold m vs m=75. L≈55: −1.0127, MDE 1.4156, 0.72×, W/L 21/24, NOT MEASURED. L≈13: +0.0201, 0.47×, NOT A RESULT (`s32/MULTIPLICITY.md` L-3e).
- **Status:** "A LEAD, not a result… on the CLOUD." It is not a proposal for the canonical pipeline.

### N-L6. Common-mode fraction versus length
- **Measured:** f = 0.4683 vs 0.5303. Difference 0.70×, NOT MEASURED (`s32/MULTIPLICITY.md` L-3b).
- **Original interpretation:** "The common mode is NOT length-scoped."
- **Status:** NOT MEASURED.

### N-L7. Donor-pool hull-capacity control at long length: NOT RUN
- **Status:** "It ships as a prediction, not a measurement". The script is `s32/s32_L_hull_capacity.py` (`s32/REPORT_S32.md` §7.6).

### N-L8. "Averaging buys more in absolute terms at length (−2.58 Å against −1.16 Å)": withdrawn as misleading
- **Original interpretation (revised):** "arithmetically right and misleading twice". Relative gain is smaller (1.35 → 1.27), and "at length `m = 75` is past the optimum" (`s32/REPORT_S32.md` §7.2).
- **Note:** `s32/REPORT_S32.md` §9.3 still cites "−2.58 Å on the long one" as evidence that averaging works.

### N-L9. Contract rule 16's constants do not survive at length
- **Measured:** a real member projects for +0.0385 at L≈55 against "−0.0007 to −0.0030" at peptide length ("13–55× larger") (`s32/REPORT_S32.md` §7.2).
- **Status:** the ordering survives. The constants do not.

### N-L10. `avg75_random` seed defect
- The seed used `abs(hash(pdb))`, which is randomised per process, so the arm is "unbiased but not replayable". This was declared before any ladder number was quoted. It was fixed to `zlib.crc32` after the run and not back-applied (`s32/MULTIPLICITY.md` Lane L self-declared defect).

---

## F. Coordinator and verification retractions not already listed (REPORT Appendix A)

| claim | whose | how it died (source wording) | source |
|---|---|---|---|
| "the retrieval filter costs +0.4357" | coordinator | "**Mislabelled.** 500→128 is the **distogram score prefix**… Retrieval is the earlier arrow" | `s32/REPORT_S32.md` App. A; `s32/MULTIPLICITY.md` D2 |
| ladder line "+0.4350 → 2.1435" | coordinator | "**Basis error** — +0.4350 is the **member** basis, the chain increment is **+0.4357**" (caught by AUDIT 9) | App. A |
| convexity check for S32-L2 | coordinator | "**VACUOUS** — accumulator initialised at the pass threshold… could not fail on any input" | `s32/LEDGER.md` S32-L2 |
| "the final rung runs at λ = 0, the prior is inactive" | coordinator | "**False.** …the canonical arm is **λ = 0.3**" (struck in `s32/STATE.md`; `s32/PREREG_S32_R.md`) | App. A |
| "typicality is a RESULT in the wrong direction" | coordinator, from lane V | "**Inverted.** `typicality` is a **distance**… Most typical: −0.0054, 0.29×, a null" (MULTIPLICITY D7) | App. A |
| `split_half_transfer` on a 16-criterion grid | lanes V and R | "**Baseline artefact**". −0.0254 CI [−0.0356, −0.0153] becomes +0.0004/+0.0026 against production | App. A; contract rule 23; MULTIPLICITY D6 |
| S32-L1 "Everything downstream of retrieval destroys 2.10 Å that is already present" | coordinator | superseded by the hull-capacity control (README H5): "the correction is the deepest result of the sprint" | `s32/LEDGER.md` S32-L1; `s32/REPORT_S32.md` §2.0 |
| `cos` as independent corroboration of the price | lane R | "`cos` is a **bijection** with the price given `(e, d)`… double-counting one measurement". It is a real cosine to ±0.004 | contract rule 16; `s32/MULTIPLICITY.md` V-A7 |
| contract rule 3 per-target max floor 0.2285 | contract | lane P reproduces at max 0.5174 on 2LNG, "ABOVE the contract's 0.2285 max floor" | `s32/MULTIPLICITY.md` P-48 |
| D1-T artefact `s32_D1_signtransfer.json` | lane D | no provenance, no producing script (third instance). "SUPERSEDED and must not be quoted". Replaced by `s32_D1_signtransfer_v2.json` | `s32/MULTIPLICITY.md` D5, D1-T re-emitted |
| AUDIT 11 provenance class | several | "seven artefacts with no provenance block and no producing script". Lane R found two more of its own. Lane D re-emitted five, with 3,985 leaves reproducing at 0.000e+00. Two (D0X, D4X) "did not contain the cited number" | App. A, App. C 2b; `s32/MULTIPLICITY.md` AUDIT 11 |
| `nullPERM` as the null for sign transfer | lane D | "could not test the claim": ≈0 even for pure noise. The correct null is cross-target `nullXTGT` | `s32/LEDGER.md` S32-L12 |
| "four unrelated Hamiltonians all respond to it" | lane D / coordinator | "they all load on compactness, and plain `Rg`… beats every Hamiltonian measured". "a confirmation on a new instrument, not a discovery" | `s32/LEDGER.md` S32-L12; `s32/MULTIPLICITY.md` D4 |
| CAUSAL_MAP thesis "Arrow 5… the one place the missing quantity may be computable" (chirality) | coordinator | falsified by N-R1 | `s32/CAUSAL_MAP.md`; `s32/REPORT_S32.md` §5.5 |
