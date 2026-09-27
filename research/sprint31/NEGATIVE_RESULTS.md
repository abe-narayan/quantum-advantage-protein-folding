_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s31/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 31: negative, null, killed, falsified and retracted results

All sections share these conventions:
- Paired, n = 126 `tuning126`, fold-clustered on the pinned 5 folds, MDE = 2.8016 × SE, unless stated otherwise.
- Sign convention: `stats_lib.compare` is lower-is-better, so a positive effect means worse.
- "DEP" means deployable / native-free as labelled in the source.
- Items are grouped by component. Section G lists the retractions and withdrawals.

---

## A. Quantum stage / CVaR-VQE (details also in QUANTUM_RESULTS.md)

### A1. The p* substitution, P1 (convex readout) and P2 (selection readout): NULL
- **Measured:**
  - P1 = E − D is −0.0112 Å built chain, SE 0.0207, MDE 0.0580, 0.19×, 62W/64L, median +0.0023, fold CI [−0.0644, +0.0465], 2/5 folds.
  - P2 = C − B is −0.0280 Å, 0.29×, 37W/29L/60T.
  - Per-target |d| for P1: mean 0.1432, p90 0.3706, max 1.1457. 100/126 targets are above 0.0107, which is 10.7× the A2 null.
  - Sources: `s31/LEDGER.md` S31-L20, `s31/REPORT_S31.md` §14.1–14.2, `s31/results/s31_P_substitute.json`.
- **Leakage:** p* is native-free / deployable (`s31/PREREG_S31_P.md` §2).
- **Original interpretation:** "solving the objective exactly reshuffles the answer everywhere and buys nothing". The experiment "does not test whether a better objective would help, and must not be recorded as evidence either way" (REPORT §14.3).
- **Status:** NULL on both primaries. Lane L's "there is no third outcome" is **falsified** (S31-L20 §2).

### A2. The built-chain cost of the shipped quantum stage, S3 = D − A: NULL
- **Measured:**
  - +0.0175 Å, SE 0.0180, MDE 0.0504, 0.35×, fold CI [−0.0173, +0.0446], 55W/71L.
  - Cloud: +0.0178 Å.
  - Exact decomposition: +0.0003 (code path) + 0.0307 (prefix widening 75→128, 0.42× MDE) − 0.0134 (weights). None of the three components is measured.
  - Sources: S31-L20 §4, REPORT §14.1.
- **Leakage:** DEP.
- **Status:** NULL. The +0.2260 Å "parity deficit" the sprint had been carrying was withdrawn (see G).

### A3. Prefix widening 75→128 (F − A2): NOT A RESULT
- **Measured:** +0.0307 Å built chain, SE 0.0260, MDE 0.0728, 0.42×, fold CI [+0.0028, +0.0557], 4/5 folds, median +0.0112 (S31-L20 §8, REPORT §14.1, §20.4).
- **Original interpretation:** "the MDE gate binds and the CI does not rescue it". It is recorded as "the only place in this sprint where turning something OFF has a measured sign", and pricing it on its own, pre-registered, is listed as an S32 candidate.
- **Status:** NOT A RESULT.

### A4. Every deployed-quantum comparison on the CA cloud: NOT A RESULT
- **Measured**, cloud (`s31/THEORY_A.md` §7.1, S31-L13 §5):
  - quantum synthesis − PROD75: +0.0178 (0.37×);
  - vs uniform-128: +0.0125 (0.27×);
  - uniform-128 − PROD75: +0.0053 (0.12×);
  - sel(p_θ) − sel(uniform medoid): −0.0308 (0.34×);
  - quantum synthesis − p* synthesis: −0.0044 (0.09×).
- **Status:** all NOT A RESULT. Lane A had earlier quoted +0.0178 and +0.0125 without MDEs and self-corrected.

### A5. Selection readout vs production
- **Measured** (S31-L20 §4):
  - B − A: +0.2652 cloud (2.15×, MEASURED worse), but +0.1012 built chain (0.93×, NOT MEASURED).
  - C − A: +0.2368 cloud (1.82×), +0.0732 chain (0.61×, NULL).
- **Original interpretation:** "the selection readout's cost is a cloud result that does not survive onto the chain."

### A6. Circuit vs closed form: the ansatz does not reach the optimum
- **Measured:**
  - KL(p_θ‖p*) is 0.930 bits mean. Registered A1-e required < 0.10; the source calls it **FALSIFIED ~10×**.
  - TV is 0.378. The circuit is strictly worse in 12/12 synthetic cells (S31-L4) and 126/126 real targets (S31-L20).
  - Iterations 80 → 2000 change the gap from 0.025764 to 0.025944 (`s31/LIT_L.md` L1.1).
- **Interpretation:** "The gap is expressivity, not optimisation". "21 parameters cannot cover a 127-dimensional simplex."

### A7. Popcount explanation of the ansatz residual: REFUTED
- **Measured:** the relabel intervention gave KL 0.967 vs 0.930 and cloud −0.0031 Å at 0.060× MDE. Popcount adds 0.016 of R² beyond the hinge (THEORY_A §7.5).
- **Status:** refuted by lane A's own registered intervention. "I have no replacement explanation and am not fitting one after the fact."

### A8. Non-diagonal Hamiltonian: CLOSED by three obstructions (theorem, no compute)
- **Content:**
  1. CVaR needs a per-shot energy.
  2. The forced operator `diag(â) − B` is mean-field and quartic in ψ.
  3. A candidate-index register's Hilbert dimension equals the candidate count, so any operator on it is "a microsecond `eigh`".
- Sources: REPORT §5.2, THEORY_A §2–3, `s31/LIT_L.md` L1.3.
- **Also:** the brief's proposed attractive sign `−λW` is the wrong sign. The attractive branch "degenerates to 'pick the single best-scoring candidate'", described as "A theorem, not a measurement".

### A9. ADAPT-VQE / qubit-ADAPT: CLOSED (theorem)
- **Content:** its selection rule `|⟨ψ|[H,A]|ψ⟩|` presumes a linear cost. "CVaR is not the expectation of any observable", so the criterion is "*undefined*, not merely unhelpful" (LIT_L L1.5, S31-L9, REPORT §16).

### A10. α is inert on three of five folds
- **Measured:** `VQE_LFO = {0:(1.0,0.3), 1:(0.25,0.3), 2:(0.25,0.3), 3:(1.0,0.3), 4:(1.0,0.3)}`. At α = 1, CVaR_1 = ⟨E,p⟩ and "CVaR is inactive by construction" (REPORT §7, THEORY_A §1.1).

### A11. Stale "+0.113 Å measured role" of the CVaR tail in shipped code: removed
- **Measured**, from S25 re-read in S31-L7:
  - vqe_a0.1 − vqe_a1.0: −0.1126, 0.51× MDE, NULL.
  - VQE_LFO − argmin: −0.1405, 0.68× MDE, NOT MEASURED.
- **Status:** the docstring at `core/pipeline.py` was corrected in place. "no Angstrom effect of that mechanism has been measured."

### A12. `core/quantum.py` docstring "a property of CVaR, not of the optimiser" for ANY α: FALSE by theorem
- **Measured**, at T = 0: entropy 0.258 bits at α = 1 (78 targets) and 3.596 bits at α = 0.25 (48 targets) (THEORY_A §7.6, S31-L13 §8).
- **Status:** corrected in place.

### A13. Deployable 128 → 512 widening: PREDICTION, labelled and not run
- **Predicted:** "a DEPLOYABLE 128 → 512 arm should come out WORSE than production, not merely flat" (S31-L16 §3, REPORT §11).
- **Status:** unverified prediction.

---

## B. Readout / terminal operator

### B1. Lane A's derived readout (primary registered comparison CAL − PROD75): WORSE, MISSED the registered band
- **Measured**, CA cloud:
  - CAL − PROD75: +0.1334, SE 0.0409, 1.17×, 5/5 folds.
  - GAM(LFO): +0.1459 (1.10×).
  - MEB: +0.1436 (1.22×).
  - The registered band was [−0.15, +0.10] (THEORY_A §7.3, S31-L13 §2, `s31/results/s31_A_readout.json`).
- **Leakage:** DEP (LFO-calibrated).
- **Status:** A3 PRIMARY "MISSED … on the side that says the direction fails".

### B2. MEB beats the shipped argmin, killed by its own shuffled-B control
- **Measured:** MEB − argmin(score) is −0.2621, 2.74×, 81W/45L. But γ=1 − shuffled-B is −0.0250 at 0.54×, NOT A RESULT (S31-L13 §2).
- **Interpretation:** "the mechanism is 'spread the weights over many candidates', not 'spread them along the real geometry'".
- **Status:** "No part of the −0.2621 Å may be attributed to the pairwise structure".

### B3. DIS + consensus as the quality estimate `â` (arm 3): REFUTED
- **Measured**, CA cloud:
  - Arm 3 − PROD75: +0.1347, 1.71×, 5/5, 48W/78L.
  - Consensus adds −0.0016 over DIS (0.02×).
  - In-band ρ: CONS −0.2837, DIS −0.0262 (S31-L19, `s31/results/s31_A_ahat.json`).
- **Status:** "Consensus as a quality estimate is closed by identity". corr(medoid criterion, B·1/D) = 0.9667.

### B4. ρ_global = 0.211 as a crossing target: WITHDRAWN by its author
- **Measured:** consensus reaches ρ_global 0.4278 but lands at 3.1614, where the price curve predicts about 2.80 (S31-L19 §2).
- **Status:** withdrawn as a target, "necessary-not-sufficient". The binding axis is in-band ρ.

### B5. MEB weighting on production's own set (2×2): WORSE
- **Measured**, cloud: WEIGHTS (MEB − uniform) on top-75 is +0.1102, 2.68×, 5/5, 49W/77L. SET (top-128 − top-75) is +0.0049, 0.14×, NOT A RESULT (S31-L19 §4).

### B6. Native-free readout rules via the cross-term identity: the channel is 3.99% of ORACLE
- **Measured**, cloud: soft-score rules are near-null. `soft_T2.00` is −0.0101 at 0.56×. The typicality rule has the **wrong sign**, with cross +0.1844 (S31-L14 §2, §6, corrected in CORRECTION 1).
- **Status:** F-C1a REFUTED.

### B7. Identifiability of ORACLE convex weights from native-free features: REFUTED
- **Measured:** out-of-fold R² is 0.02103 against a 5% bar. Applied, the fitted weights are +0.0309 worse (0.37×, 60W/66L) (S31-L14 §6).
- **Status:** F-C1c REFUTED.

### B8. Constrained-affine readout (norm-bounded middle): no knee, no selection rule
- **Measured:** the ridge path is smooth and monotone (`||w||₁` 1.01 → 28.3, ORACLE 2.7318 → 0.0000) (S31-L14 §5).
- **Status:** "cannot be selected by ceiling and cannot be selected by fit" (REPORT §10.4).

### B9. The affine ceiling is vacuous: F-C1d REFUTED as informative
- **Measured:** ORACLE affine over 128 gives 0.0000. Median ess is 1.13 and median neg_mass is 3.38. Only 1.6% of targets have ess ≥ 5 and neg_mass ≤ 1. rank(aff) is 32.9 ≥ 3n−3 (S31-L14 §4, THEORY_A §3.2).
- **Interpretation:** "0.2516 Å under an ORACLE objective" is "a statement about a REGULARISER, not a class ceiling".

### B10. Terminal-operator arms (lane F), built chain vs production re-projected in the same job (3.2126)

| arm | effect | × MDE | W/L | verdict |
|---|---|---|---|---|
| MED | +0.0688 | 0.81 | 58/68 | NOT MEASURED (CI excludes zero on the bad side) |
| AVG_RG | +0.0475 | 1.11 | 51/75 | MEASURED WORSE |
| AVG_SEP | +0.4609 | 2.34 | 41/85 | MEASURED MUCH WORSE |

- **Sources:** S31-L21 §2, `s31/results/s31_F_analyse.json`, `s31/results/s31_V_avgsep.json`.
- **Leakage:** all native-free, zero free parameters.
- **Status:**
  - "ALL FOUR REGISTERED FALSIFIERS FIRED AGAINST THIS LANE".
  - AVG_SEP was "the sprint's only live deployable candidate and it is dead".
  - AVG_RG was a registered negative control after the 25.8% premise was withdrawn.
- **Interpretation:** "the distortion is a SYMPTOM of averaging, not the MECHANISM of its error", which "closes the entire 'repair the average's shape' family".

### B11. Native-free gates G0, G3, G4, G5: all REFUTED in the registered direction
- **Measured**, built chain: G0 (DISP → MED) +0.0591 (0.72×); G3 (MOVE → MED) +0.0600 (0.74×); G4 (MOVE → AVG_SEP) +0.1412 (1.34×); G5 (DISP → AVG_SEP) +0.1457 (1.30×). Reversed directions: +0.0096 and +0.0087, NOT A RESULT.
- **Leakage:** G1/G3τ are ORACLE-ADJACENT (−0.0039, +0.0171, NOT A RESULT).
- **Source:** S31-L21 §3.

### B12. ORACLE per-target operator choice: small, mostly best-of-K
- **Measured:**
  - G2 min(AVG, MED) is −0.0782 (1.57×, 58/0, ORACLE). Split-half transfer is −0.0323 with a CI spanning zero.
  - G6 min(AVG, AVG_SEP) is −0.0615 (ORACLE).
  - The min over all four operators is −0.1471 (2.54×, ORACLE, unregistered). Its argmin is near-uniform across operators (26/46/25/29), median −0.0570, p90 0.0000.
  - Source: S31-L21 §3, §9b.
- **Interpretation:** "no rule for realising it exists."

### B13. The dispersion mechanism for MED: the registered NEGATIVE direction was refuted
- **Measured:** hi-minus-lo DISP contrast is +0.0990 (0.59×). Tertiles are +0.0049 / +0.0604 / +0.1410 (S31-L21 §4).
- **Status:** the registered mechanism falsifier fired. "the medoid's own cost scales faster, so there is no operating point where it turns over."

### B14. The separation-band mechanism: band falsifier FIRED
- **Measured:** long-band |ratio−1| is 0.2918 for MED vs 0.2824 for AVG (+0.0094, 0.55×) (S31-L21 §5).
- **Status:** "The separation-band framing is refuted for this operator pair." A correction followed: averaging "contracts everywhere".

### B15. AVG_SEP registered as "NOT affine": measured affine in practice
- **Measured:** 0.045 Å RMS per coordinate from the best affine combination (S31-L21 §6).
- **Status:** "a registered claim of my own that failed". The source calls it "affine-in-disguise".

### B16. Convex rung under the deployed objective: closed by ceiling (inherited)
- **Measured:** it converges to 3.0522 Å CA cloud, which is the uniform average (S31-L2 annotation, citing S23-L8 and S23-L5).

### B17. C1 weight families W1–W5 and the rescale idea: already closed in the record
- **Source:** `s31/PREREG_S31_C.md` Amendment 1 table.
- **Status:** not re-run, inherited as closed.
- **Examples:** W2 typicality is "measurably HARMFUL" (+0.0364); W4 unconstrained is "CLOSED catastrophically" (+2.930, 4.36×).

---

## C. Candidate index / register

### C1. Index redesign: F-C2a, F-C2b and F-C2c all REFUTED (CA cloud)
- **Measured** (S31-L15, `s31/results/s31_C_index.json`):
  - Best map raises the ORACLE product-state ceiling by −0.0655 (bisect_score, 1.34×) against a −0.10 bar.
  - Best deployable triple is `perm`, j = 2, by_score: −0.0160 vs production.
  - The structure-aware pre-check was +0.130 / +0.127 against a +0.15 bar.
  - The grid is 194% accounted by order statistics; split-half transfer is 23%.
- **Interpretation:** "The best index map for a deployable partial readout is the random permutation." Structure-aware indexing "raises the ORACLE value … and lowers its deployable value (3.2369 -> 3.3721)" by construction.

### C2. Gray coding: proven no-op
- **Measured:** the prefix partition is identical on 126/126. The ceiling difference is −0.0014 at 0.03× (S31-L15).

### C3. Bit information about candidate quality: negligible
- **Measured:** the best bit carries 0.0658 bits (bisect). The deployed map carries 0.0343 and perm 0.005 (S31-L15).
- **Interpretation:** "two orders of magnitude short in size."

---

## D. Prefix length `m` / `bestm128` (lane F F3, lane V)

### D1. `bestm128 = 2.9027` is an order statistic, and the prefix axis is worse than an arbitrary 7-bit index
- **Measured**, CA cloud: the matched random-subset family gains −0.4279 against the prefix's −0.2879, i.e. **149%**, draw sd 0.0273 over 4 draws. The registered bar was ≥ 80% and it fired. Lag-1 autocorrelation is 0.917 vs 0.126.
- **Measured**, built chain (S31-L23): random draw 0 − PREFIX is −0.1368 (1.13×, 90W/36L) and draw 1 is −0.1146 (0.93×, NOT MEASURED on its own), i.e. 141%.
- **Sources:** S31-L11, S31-L23, `s31/results/s31_F3_prefix.json`, `s31_F3_chain.json`.
- **Leakage:** ORACLE / NOT DEPLOYABLE.
- **Status:** confirmed on both bases. The superseded hash-seeded values (−0.4191, sd 0.0065, 146%) are kept per rule 13.

### D2. Transferable / deployable `m`: NULL, "a coin flip"
- **Measured:**
  - Built chain: M_LFO +0.0075 (0.22×, 2/5 folds, 63W/63L); M_GLOBAL −0.0044 (0.19×).
  - Cloud: split-half transfer −0.0039, 1.2%.
  - Best native-free fold-held-out m-rule: n_distinct −0.0221 (0.51×).
  - Sources: S31-L11 §4, S31-L23.
- **Status:** "no part of it is deployable" fired. This agrees with S29-L30's earlier FALSIFIED verdict.

### D3. "0.308 Å lead available to a better selector": WITHDRAWN (the coordinator's)
- **Status:** "the lead was measured at 0.6% of face value two sprints ago" (S31-L12, LIT_L L3.1). The *ceiling* reading stands: "an optimistically biased upper bound is still a valid upper bound".

### D4. "0.076 Å of error cancellation at zero weight bits" (2-of-128): at matched K it is a 0.077 Å PENALTY
- **Measured**, CA cloud, ORACLE: 128 random pairs vs 128 singletons gives +0.0771 worse (1.11×, fold CI [+0.040, +0.111], 5/5, 44W/82L). The exhaustive K=8128 gives −0.2388. Decomposition: level −0.2378, dispersion loss +0.3149 (`s31/AUDIT_V.md` V1/D1, `s31/results/s31_V_orderstat.json`).
- **Status:** the registered bar fired and the sign reversed.

---

## E. Physical-model channels (lane B)

### E1. Free-energy stage (§7A): CLOSED by derivation, no compute
- **Measured:** Lemma B1 was verified. 1340 torsion phases sit at 0.000e+00 from {0, π}, with no CMAP (S31-L10 §1).
- **Status:** closed by Corollary B1 (G1). The elastic-network / normal-mode family is closed by Corollary B1′.
- **Left open "on price, not theory":** multi-structure barriers F‡.

### E2. F1 falsifier fired, then was inverted by a matched control
- **Measured:** reflection residual 3.673e-06 against a 1e-6 bar. The rotation control gives 5.377e-06 (0.68×) (`s31/results/s31_B1_achirality.json`).
- **Status:** "a mis-set threshold — not a falsification".

### E3. Backbone-torsion channel for in-pool selection (§7B): CLOSED
- **Measured:**
  - G2 fired: LEG_torsion in-band is +0.0444 at 0.65×. For comparison DIS is 0.83×.
  - G3 did not fire: best partial ρ is +0.0401 (0.61×).
  - G5 fired: constant α-helix vs LEG_torsion is −0.1722 at 3.17× (500 band) and −0.0901 at 1.81× in band, 5/5.
  - Sources: S31-L10 §3, `s31/results/s31_B2_inpool.json`.
- **Interpretation:** "The chiral escape from G1 is real … and it only works on a problem the pipeline does not have." The Ramachandran channel's in-pool skill is "a constant-prior effect".

### E4. Lane B's 4:1 prior that LEG_torsion is predominantly odd: FAILED
- **Measured:** the odd variance share is 0.3001, so the channel is 70% even (S31-L10 §3).

### E5. M6 chiral non-separable cell (XTWIST): empty at 9–16 residues
- **Measured:** XTWIST_4 is −0.0104 (−0.23×) and XTWIST_8 is −0.0853 (−1.02×, backwards). The achiral twin XTWABS beats it (+0.1124, +0.1486) (S31-L10 §3).

### E6. The 32-cost meter sweep's top rows measure triage, not nativeness
- **Measured:** pref(circ_best vs PROD) is 0.5079 / 0.4206 / 0.4048 for the top three rows, "at or below a coin flip" (S31-L10 §2).
- **Status:** the arithmetic reproduces and the construction is exonerated; the reading is corrected.
- Lane B's own suspicion that the result was a RAND_SIGNED artefact was refuted by the GAUSS_MATCHED control.

### E7. Node-level candidate-graph observables: CLOSED (C2 fired)
- **Measured:** every node statistic's in-band skill is absorbed by consensus, e.g. geo_cent +0.2099 → +0.0377 partialled (S31-L10 §5).
- **Left open:** pair-level quantities (C1 did not fire).

### E8. "No ranker can pass the coherence bar": WITHDRAWN and reworded
- See G, item D0. The replacement reads: "coherence does not vary along the ranking axis at all".

---

## F. Common-mode / prior-correction channel (lane E)

### F1. E1, native-free common-mode direction `mu_hat = pool75_mean − expected`: DEAD
- **Measured:**
  - cos is +0.0495 against a 0.30 kill bar.
  - Excess over the permutation control is +0.0282 at 0.51×.
  - Only 1% of targets reach the USABLE bar.
  - `mu_hat = mu − y` exactly (1.8e-15). r = sd(y)/sd(mu) = 1.5997.
  - Sources: S31-L3, `s31/results/s31_E1_direction.json`.
- **Status:** "Circular, killed by one line of algebra" (REPORT A.1). This was the coordinator's opening hypothesis.

### F2. E2 / E3 projected and constrained correctors: FALSIFIED as registered
- **Measured**, built chain: E2_PROJ_MUHAT +0.0414 (0.46×) and E3_CONSTR_MUHAT +0.0323 (0.44×). With the true `mu`: +0.0741 / +0.0644 (S31-L22).
- **Leakage:** LFO-supervised, native-free at inference.
- **Status:** "closed at its ORACLE ceiling".

### F3. Orthogonal-only correction with ORACLE magnitude and direction: HARMFUL
- **Measured:** +0.0747 Å (0.87×, 57W/69L). It is +0.6169 worse than its norm-matched shrink (3.25×, 9W/117L) and +0.3797 worse than the energy-matched direction (2.53×, 12W/114L) (S31-L22, `s31/results/s31_E5_contrasts.json`).
- **Leakage:** ORACLE / NOT DEPLOYABLE.
- **Status:** the source calls this "The controlled half" of the along/perp result. Charter §14 and contract rule 29 are "INVERTED".

### F4. The projection is not the mechanism
- **Measured:** E2 vs norm-matched shrink is +0.0216 (0.26×). Projecting against the true `mu` vs not projecting is +0.0192 (0.18×) / +0.0095 (0.08×) (S31-L22 controls 4–5).

### F5. Along-mu arm vs its own magnitude control: NOT MEASURED
- **Measured:** vs SHRINK_Y_075 −0.0614 (0.94×, 81W/45L); vs SHRINK_Y_090 −0.0405 (0.64×, 65W/61L) (S31-L22, `s31/results/s31_E5_contrasts.json`).
- **Interpretation:** "'Correcting along `mu` is the whole prize' is, at matched magnitude, the same statement as 'most of a perfect correction is the whole prize.'"

### F6. ALONG vs FULL (perfect prior): a tie
- **Measured:** −0.0345, 0.51×, 3/5 folds (S31-L22).

---

## G. Instrument, provenance and process negatives

### G1. The "unpinned multi-start projection seed" (three sprints, charter §19/§20B): FALSE
- **Measured:** "There is no RNG anywhere on the projection path". Reprojection is bit-identical (S31-L6).
- **Status:** superseded by the conditioning diagnosis.

### G2. B4 branch-carry for accuracy: NOT A RESULT (H0 held as registered)
- **Measured:** B4 − PROD is −0.0055, SE 0.0044, 0.44×, 34W/21L/71T, median 0.0000, fold CI [−0.0071, −0.0031] (excludes zero), iid CI spans zero. ORACLE_B4 is −0.0938 (2.92×, 114W/0L, ORACLE) (S31-L8, `s31/results/s31_D_branch.json`).
- **Status:** "Do not adopt B4 for accuracy" (STATE NOTE 9). The source reads this as "SEARCH IS NOT THE BARRIER; DISCRIMINATION IS."

### G3. The deposited-ensemble reference does not explain the tail: NULL
- **Measured:** tail-minus-rest ensemble spread is −0.1374, SE 0.2421, 0.20×. corr(RMSD, spread) is +0.1118 with CI [−0.0762, +0.2921] (S31-L9, `s31/LIT_L.md` L2.1).
- **Leakage:** ORACLE diagnostic of the benchmark.

### G4. Charter §14 new-observable question: CLOSED "by provenance" / "by data availability"
- **Measured:** 117/126 (92.9%) of targets are NMR-determined. Measured VCD/ROA spectra for these targets: zero (S31-L9).

### G5. "You need a measurement of the molecule, not a computation": WITHDRAWN
- **Status:** "True premise, vacuous conclusion". I(N; sequence) = H(N). The source adds: "If it implied a ceiling, AlphaFold would be impossible" (S31-L12, STATE NOTE 12).

### G6. FAIL18 widening effect of −1.9004 Å: RETIRED as a near-tautology
- **Measured:** defn18 ∩ FAIL18 = 18/18, with an identical effect. The re-priced filter-independent value is −1.1811 cloud / −1.1762 chain (ORACLE, p = 0.0001) (S31-L5, `s31/results/s31_C_widen.json`).
- **Status:** "−1.9004 Å is never quotable again". A level control removes about two thirds of FAIL18's excess.

### G7. "The tail is disproportionately a FILTER failure": RETRACTED in part by lane F's own control
- **Measured:** filter-minus-readout excess, tail minus rest: T_POOL +0.1925 (0.16×), T_BEST +0.4298 (0.38×), T_CHAIN +0.8781 (0.84×), FAIL18 +1.6165 (1.24×) (S31-L21 §8(b)).
- **Status:** "Which of filter and readout is hurt more on the tail is NOT MEASURED." The effect rises with how circular the stratum is.

---

## Retractions and withdrawals (REPORT_S31 Appendix A; AUDIT_V)

**Coordinator's (REPORT A.1)**, each with how it died:
1. R1's quantifier "the entire quantum stage carries at most k bits". The coordinator's own falsifier fired in shipped code (`average_weighted`, 1.1144 Å from the nearest pool member).
2. R1 point 4, "all 2^k vertices reachable". Duplicates make the capacity 6.886 bits, not 7.
3. "Two readouts" (S31-L2). There are three.
4. The +0.2260 Å deficit broadcast to four lanes. It belonged to the affine harness readout. The shipped stage costs +0.0178 cloud / +0.0175 chain, both NULL.
5. "Averaging contracts the backbone 25.8%". This had been withdrawn two sprints earlier (`s15/coord_FINDINGS.md:914-921`); the correct figure is 3.5%.
6. Opening hypothesis E1, which was circular.
7. "You need a measurement of the molecule, not a computation", which was vacuous.
8. "The set-matched ladder inverts S30-L11". This withdrawal was itself wrong; S30's conclusion survives on its own `argmin_ref` curve (1.7108 at 9 bits).
9. "0.076 Å of pure error cancellation at zero weight bits". The support is ORACLE-greedy at 12.99 bits, and at matched K it is a 0.077 Å penalty.
10. The headline's basis, "2.1435 Å (CA cloud) … ~0.90 Å". 2.1435 is the built chain value; the headroom is 1.067 Å on the chain.
11. "If coh(AVG_SEP) < 0.6931 it is the first native-free operator to pass". The bar comes from a different object (see D0).
12. The lever comparison "convex readout is 0.290 Å better". That is 7 bits against 128 free reals.
13. "bestm128 may deflate". This was inverted: the ceiling reading was licensed and the "0.308 Å lead" was not.
14. "The widening null as 0.35×". The widening is F − A2 at 0.42×.
15. "The basis was doing the work" (§14.6). Overstated: both bases give nulls.
16. The coordinator's 2:1 reasoning on E2/E3. Right in direction, wrong in mechanism: the orthogonal complement is 94% predictable and harmful, not noise.

**Lanes' (REPORT A.2):**
- Lane A: the primary missed; the MEB positive was demolished by shuffled-B; ρ = 0.211 as a target was withdrawn; the popcount explanation was refuted; +0.0178 / +0.0125 had been quoted without MDEs.
- Lane B: the 4:1 odd prior failed; the RAND_SIGNED-artefact suspicion was refuted; the claim that LEG_steric's contrast is chirality-dominated was self-corrected.
- Lane C: a C3 wrong-tail sign error, caught before release; the ORACLE convex ceiling violated its feasibility bound on 4/126 targets (119W/4L → 119W/0L); the claim "must never again be quoted as the architectural ceiling" was withdrawn as too strong. REPORT A.2 attributes this last item to lane C. LEDGER S31-L11 §5b shows it as lane F's sentence, withdrawn by lane F; see LESSONS.md, importer notes.
- Lane D: two defects caught by its own verifier.
- Lane E: "It must carry orthogonal INFORMATION" was half withdrawn.
- Lane F: a `hash()`-seeded random family was repaired to crc32 (146% → 149%); a missed grep for `medoid75` was declared in its prereg.
- Lane L: "Consistent with the unpinned projection seed" was withdrawn; its 12 verification cells ran at T = 0.1/0.05 rather than the deployed 0.3, and its entropy-direction claim reverses at the deployed T.
- Lane P: the disagreement prediction of 20–45 was actually 66; "Arm E lies between D and F" was falsified; lane L's "there is no third outcome" was falsified.

**Lane V defects** (`s31/AUDIT_V.md`):
- **D0 (SEVERE):** the 0.6931 coherence bar grades a corrector's residual, not a readout. It was live in `s31_B2_inpool.py` and `s31_F_coh.py`, and was struck from both plus the verifier. It is now enforced by a regression guard.
- **D1 (SEVERE):** matched-K penalty; see D4 above.
- **D2 (SEVERE):** "inverts S30-L11" was a wrong withdrawal.
- **D3 (MODERATE):** misnamed basis in the headline.
- **D4 (LOW):** STATE quoted superseded hash-seeded draws.
- **D5 (LOW, process):** `git add -A` swept other lanes' files into commits.
- **D6 (MODERATE):** S31-L17's evidence could not test its own tie caveat, and "zero" overstates a measurable quantity.
- **D7 (LOW):** the ~0.70 Å reference term is not uniform and attenuates rather than cancels. Using the wrong moment understated it about 2× (+0.1645 Å, not ~0.08).
- **D8 (LOW):** 6.886 vs 6.888 bits (Jensen).
- **D9 (MODERATE):** the verifier had a check against a key that never existed (`coh_contrast`).
- **D10 (SEVERE):** AVG_SEP was +0.4609 WORSE, not "0.4–0.6 Å better". This was a partial-rows reading with the sign inverted.
- **V-SELF:** three errors of the auditor's own, including a regression guard that silently skipped a file.

**Registered predictions scored against their authors** (REPORT §15): six of ten went against the lane that wrote them, three of those the coordinator's:
- the orthogonal complement is noise (right for the wrong reason);
- long-range R² ≈ 0 (falsified, +0.1959);
- a substantial fraction of bestm128 survives (falsified);
- LEG_torsion is predominantly odd (failed);
- the derived readout beats production (missed at +0.1334);
- a disagreement count of 20–45 (wrong, 66);
- arm E lies between D and F (falsified);
- a deployable prefix-m rule transfers (falsified three ways).
