_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s29/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 29 — negative, null, killed, falsified and retracted results

Format per item: **Measured** (with source), **Original interpretation** (attributed), **Status in source**, **Leakage**. "NOT MEASURED" is the source's own `ST.compare` verdict (|effect| ≤ own MDE). All paths are relative to the source repo.

## 0. The retractions index, and what it actually contains

- **Measured / recorded:** `s29/RETRACTIONS_S29.md` is an append-only table "lane D keeps it"; at the pinned commit its only row is **"(none yet)"**.
- **Original interpretation:** the file says "Every S29 retraction, with the ledger entry it retracts, the entry that retracts it, and the artefact … this file is the index."
- **Status in source:** the index was never populated. The withdrawals are instead recorded in `s29/REPORT_S29.md` §3.2 ("**18 claims were withdrawn during the sprint, 11 of them mine**") and §14(e) (18-row table), and in the ledger entries cited below. Every one of those 18 is itemised in §A below. (Contradiction recorded, not resolved: the index file says "none yet"; the report says 18.)

## A. The 18 claims withdrawn during the sprint (`s29/REPORT_S29.md` §14(e))

A1. **Corollary 2b (lane T's sign law).**
- Measured: registered "beta > 1 on ≥ 2/3 of targets and sign(cos_DIS) = −sign(beta − 1) on ≥ 70%". Measured beta median 0.756 / 0.753 / 0.569 / 0.69 under four definitions, > 1 on 10–13%, sign agreement 48–50% inside coin-toss CI [41, 59] (S29-L26; `s29/results/s29_D_theory_beta.json`, `s26/logs/s29D_theory_beta.log`). Post-mortem at n = 126: sign law fails on unsaturated and saturated pairs alike (agreement 0.448–0.472 vs 0.468–0.492); in linear regime beta 0.947–0.961 (S29-L39; `s29/results/s29_T_beta_unsat.json`). Four-term repair: agreement 74/126 = exactly the coin-toss bar, clears on none of six cells (S29-L40; `s29/results/s29_T_beta_full.json`).
- Original interpretation: lane T: "WITHDRAWN at my own registered bar"; "not merely wrong, it is VACUOUS in its own valid regime"; "the second-order model is not predictive for this cosine at n = 126" (S29-L29, L39, L40; `THEORY.md` §2.3b).
- Status: **withdrawn/retracted**. Theorem 2's central claim, corollaries 2a and 2c stand (`THEORY_SUMMARY.md` §2). ORACLE diagnostic.

A2. **Rule 20's cosine justification ("the cosine is gameable by shrinking").**
- Measured: 9-point shrink grid, 126 targets: cosine −0.0338 → −0.0558 (s = 0.6) → −0.0334, never rises, never crosses zero; native percentile 0.3688 → 0.4910, 9/9 steps; ladder ρ −0.186 → −0.054; pref(circ_best) 0.198 → 0.373 (S29-L37; `s29/results/s29_D_theory_shrink.json`).
- Original interpretation: lane D: "THE COSINE HALF IS REFUTED … THE PERCENTILE HALF IS CONFIRMED"; contract addendum 5 (rule 30): "RULE 20's JUSTIFICATION IS WITHDRAWN; THE RULE STANDS ON A DIFFERENT AND MEASURED FOOTING … Do not quote 'the cosine is gameable by shrinking' anywhere."
- Status: **half refuted, half confirmed**; rule kept. ORACLE. (Note: `THEORY_SUMMARY.md` §2 table still lists "the shrink warning … **stands and is now mechanical**: a positive cosine is purchasable with zero information by shrinking" — contradiction with S29-L37/addendum 5 recorded in LESSONS importer notes.)

A3. **The coordinator's trainability premise (centring the coupling matrix fixes trainability; the reason lane B was spawned).**
- Measured: λ₂/λ₁ 0.138 → 0.465 (A_c) → 0.634 (G), but r_stable only 1.04 → 1.59/1.68; hop-only gradient-variance slopes −2.305 (A_c), −1.900 (G) vs −1.830 for raw A (S29-L11; `s29/results/s29_T_grad_rows.jsonl`); independent reproduction to 2.03e-14; bright line B1 refuted on both clauses — n = 9 variances 3.60e-6 / 5.05e-6, 283× and 201× below the 30× threshold (S29-L36; `s29/results/s29_B_grad.json`).
- Original interpretation: STATE integration note 5: "I WAS WRONG ABOUT WHY LANE B WAS WORTH SPAWNING … 'The spectrum is no longer degenerate' is the wrong justification for a build, and I gave it." Lane B: "The justification that spawned this lane is dead."
- Status: **refuted** (by derivation and measurement). Property measurement, no native.

A4. **The coordinator's provenance claim that lane T's sign formula "was derived before those numbers were read".**
- Measured: `2q-1` first enters `THEORY.md` at commit `53c42bd4`, 2026-09-20 00:38:49, 7.5 minutes after lane O's S29-L21 (00:31:19); `git log --all -S "2q-1"` finds nothing earlier; the |ρ| = 0.37 in that row was inverted from lane O's −0.214/−0.246 (S29-L28, S29-L29).
- Original interpretation: lane D: "the agreement is a POST HOC FIT, not a prediction"; lane T: "I HOLD NO EARLIER ARTEFACT AND THE CLAIM IS WITHDRAWN. Worse than late … lane O's numbers are an INPUT."
- Status: **refuted by commit history**; the bound's derivation unaffected. (S29-L23's text still contains "it was derived before those numbers were read" — left standing per append-only rule.)

A5. **The coordinator's flatness gate** ("if the flat fraction does not fall materially, the idea is dead").
- Measured: flat_cvar = flat_f = 0.8552 identically at every λ, 12 targets; overlap 0.0000; TTA readout moves along 74 directions vs deployed 0 of 511 (S29-L27; `s29/results/s29_B_tta_flat.json`).
- Original interpretation: lane B registered before measuring that it "could not fall"; STATE note 18: "A GATE I SET THAT WOULD HAVE KILLED A LIVE IDEA BY A CONSTANT."
- Status: **withdrawn** (gate corrected before measurement).

A6. **The architectural-ceiling figure quoted on the wrong basis.**
- Measured: S29-L30 point-cloud ceiling 2.7605 Å (vs 3.0483); built chain 2.9122 (n = 121) then **2.9027** (n = 126) vs 3.2105 (S29-L44 + addendum 3; `s29/results/s29_O_headline_contrasts.json`).
- Original interpretation: coordinator: "I have been quoting the architectural ceiling on the **POINT CLOUD** while the charter's endpoint is the **BUILT CHAIN** … the exact error the S28 steer warned about."
- Status: **corrected**; conclusion stated as "stronger, not weaker". ORACLE.

A7. **The coordinator's "absent instantiation" framing for the shell-profile class.**
- Measured: five native-free profile rules already measured leave-fold-out in S12 (incumbent 3.078, per-shell debias 3.071, affine recal 3.089, ridge 3.309, pool mean 3.383 vs ORACLE 2.402) (STATE note 24; `s12/obj_FINDINGS.md:306-331` as cited).
- Original interpretation: lane M declined the framing; closure became "a MEASURED SUPPLY GAP, which is stronger".
- Status: **withdrawn/corrected**.

A8. **The coordinator's "7 bits" reading** (that 0.757 Å is recoverable by supplying ranking bits to the shipped readout).
- Measured: operator law `d_out = 1.16·d_set_mean + 0.04·d_set_best` (R² 0.89); perfect rank-1 worth ≈ −1.74 Å through argmin vs ≈ −0.03 Å through the m = 75 average (S29-L44 addendum 2; STATE note 26).
- Original interpretation: "the 0.757 A prices a readout SWITCH plus the bits, not a ranking improvement fed to the shipped operator."
- Status: **corrected** (lane M's caveat).

A9. **Lane L's "S8 free-energy stage is committed and resumable as `python -m s8.relax best`".**
- Measured: all seven paths (`s8/relax.py`, `s8/test_relax.py`, `s8/relax_fe.json`, `s8/relax_best.json`, `s8/relax_sweep.json`, `s8/relax_report.txt`, `s8/relax_findings.md`) absent from disk and from all git history; `importlib.util.find_spec('s8.relax')` → None (S29-L41, S29-L42).
- Original interpretation: lane L: "The third clause is mine and it is false"; item becomes "a REBUILD from a prose spec, not a resume … a lane-week".
- Status: **retracted**; annotated in place in `s29/lit/L_1_native_free_qa.md` §8.3 and `s29/lit/L_7_inband_training.md` §(c) (per S29-L42).

A10. **Lane D's ±3 Å B3 bracket.**
- Measured: hardened to ±6 Å; residual grows with step size; |rel| exceeds 10% of effect at median step 1.77 Å; 20/630 cells at the ±6 Å edge excluded (S29-L52; `s29/results/s29_D_fields_b3.json`).
- Original interpretation: "the n = 2 probe … was replaced"; scope restated as a measured curve.
- Status: **superseded by the 126-target run**.

A11. **The coordinator's field count ("39 displacement fields"; STATE said "eighteen").**
- Measured: `s29/results/s29_D_fields.json` contains 21 fields (verified: 21 keys) (S29-L48, S29-L52).
- Original interpretation: "I wrote '39 displacement fields' … the file holds **21** … Caught by recomputing from the artefact."
- Status: **corrected** in §0; but "39" still appears in REPORT §9.2, §11.2 and §14(d) (see LESSONS importer notes).

A12. **The coordinator's compactness expectation** (that lane L's objection would close B2's last exit).
- Measured: F1a Spearman(|ρ_Rg|, |ρ_inband|) = +0.083 vs bar +0.40; F1b 9% of skill removed vs bar 40%; 9 of 31 channels keep partialled in-band skill ≥ 0.15 (S29-L50; `s29/results/s29_T_compactness.json`).
- Original interpretation: STATE note 28: "MY STANDING EXPECTATION WAS WRONG AND **B2's LAST EXIT STAYS OPEN**."
- Status: **refuted** at n = 126. ORACLE diagnostics (in-band skill); loadings native-free.

A13. **The coordinator's "39 passed".**
- Measured: first VERIFY_SLOW run left a log with 39 dots, no pytest summary, no exit code; re-run: exit 0, 140 s, 1.14 GB, 39 passed (REPORT §4.6; S29-L55).
- Original interpretation: "Written from a log … then compounded by asserting the governor had *killed* the run, when `REAP` fires for processes already gone."
- Status: **withdrawn**, then confirmed by re-run.

A14. **Lane M's F2 prior** ("0.16–0.24, genuinely close to the line").
- Measured: fitted RATIO cosine 0.0895; ORACLE displacement cosine 0.483 (not the inferred 0.66) (S29-L53; `s29/results/s29_M_F2_supply.json`).
- Original interpretation: "wrong in the direction that flatters the experiment … the shrink twin is what caught it."
- Status: **refuted prior**.

A15. **Lane B's `tail_is_prefix` column** (0.91–0.99, suggesting the VQE escaped set-equality).
- Measured: value-based gate passes with equality on every tested cell (16 cells, 8 targets); the 37 flagged targets have exact E ties (up to 4-way) (S29-L54).
- Original interpretation: "It is an artefact of my own column … The CVaR tail under tail-then-aggregate is still the energy prefix, by construction."
- Status: **claim not made** (caught before claiming).

A16. **Lane T's compactness prior** (registered 3-to-1 that lane L's objection holds).
- Measured / interpretation: as A12; lane T: "My registered prior was F1 at 3 to 1 and it was WRONG" (S29-L50).
- Status: **refuted**.

A17. **The coordinator's "the chimera family is expressive".**
- Measured: chimera ORACLE best +0.6533 Å worse than the pool's own ORACLE best (cloud, n = 12, 0.61× MDE, 5/5 folds, NOT MEASURED) (S29-L56; `s29/results/s29_X_probe.json`).
- Original interpretation: REPORT §14(e): "I had compared its ORACLE against *production*; the informative comparison is against the *pool's own* ORACLE."
- Status: **withdrawn**. ORACLE.

A18. **The coordinator's "the untrained circuit is the best arm"** (from lane X's 5-target probe).
- Measured: at n = 12 UNTRAINED|R3 vs trained R3 arms 0.08–0.55× MDE, NOT MEASURED; R3 separation-to-noise 0.459 vs R1 1.047; R3 captures mean 0.3116 of mass (S29-L56 §10; `s29/s29_X_FINDINGS.md` §4.10).
- Original interpretation: "Both readings found structure in a small sample."
- Status: **refuted**.

## B. Every deployable/candidate intervention that failed (`s29/REPORT_S29.md` §3.1, §7.2)

B1. **H1, the typicality axis (rung 6).**
- Measured: ORACLE mean cos(u, v) −0.0584 (SE 0.0324) vs random signed ref +0.0075 (0.73× MDE, NOT MEASURED) and vs random |cos| 0.1443 (−2.19× MDE, fold CI [−0.2355, −0.1663]); ORACLE best global step t = 0 exactly; leave-fold-out step bit-identical to production on 126/126 (built chain 3.2105 both); BPRIME LFO +0.0037 Å chain (0.29×); FAIL18 cos −0.3171 vs 108 −0.0153, random-18 p = 0.0006; per-target ORACLE step −0.3061 Å, split-half transfer +0.0056 (S29-L20; `s29/results/s29_O_lfo.json`, `s29_O_cloud_rows.jsonl`).
- Original interpretation: "H1 IS FALSIFIED on both registered clauses … H1's premise … is false exactly where it was hoped to be most true."
- Status: **falsified**. LFO arm DEP; everything else ORACLE.

B2. **Rung 8, the PC1 one-parameter family (signed-readout collapse of centred Hamiltonians).**
- Measured: ORACLE best global η exactly 0.0000; per-target η (order statistic) −0.4543; one-sign ceilings −0.2142/−0.2455; sign positive on 52%; LFO η +0.0071 Å worse (0.82× MDE, NOT MEASURED) (S29-L21; `s29/results/s29_O_pc1.json`).
- Original interpretation: "a centered / agreement-matrix Hamiltonian consumed by a signed readout … has an achievable ceiling of 0.000 A."
- Status: **falsified at ceiling**; T's prediction "under 0.15" confirmed at its floor. LFO DEP; rest ORACLE.

B3. **A transferable prefix length m / widening the quantum stage's field of view (rung 9).**
- Measured: ORACLE global m = 72 worth −0.0018 Å; LFO prefix +0.0079 Å (0.30× MDE, NOT MEASURED, 59W/67L); 75 → 128 worth −0.0663 Å ORACLE (point cloud); per-target m transfers −3% (S29-L30; `s29/results/s29_O_p128.json`, `s29_O_mladder.json`).
- Original interpretation: "a BOUND, not an opportunity"; "Widening the prefix … is a lever worth 0.07 A ORACLE, and zero achievable."
- Status: **falsified** (transferable part zero). LFO DEP.

B4. **21 native-free displacement fields vs assumption B2** — none beats 0.1398 (see README headline 2; S29-L35). Status: **falsified as routes** (B2 survived). ORACLE.

B5. **The compatibility Hamiltonian on the candidate register (lane B measurement 2).**
- Measured: 0 of 24 (M, J) cells clear 0.7× MDE vs own DIS top-75 on either readout; signed readout R4 0.3–4.7 Å worse, sign_correct 0.40–0.75 (median 0.50); p-readout emitted cloud moves 0.22–1.45 Å from production while RMSD moves < 0.1 Å; J-grid split-half transfer +0.1571 (worse) (S29-L49; `s29/results/s29_B_gs.json`).
- Original interpretation: "THE GATE IS CLOSED … measurement 3 … is NOT run"; the route "is shut for a **structural** reason … about the ENCODING … not about off-diagonal Hamiltonians."
- Status: **gate not opened; endpoint not run**. ORACLE diagnostic, n = 12.

B6. **S29-L11 prediction 3 as lane B operationalised it** ("p-readout emits the pool mean within a 0.05 Å floor on ≥ 80%").
- Measured: 0.00–0.17 of targets (S29-L49).
- Status: **falsified as operationalised**; "SPIRIT is confirmed and its letter is not" (lateral motion).

B7. **Tail-then-aggregate: the non-prefix choice (free subset search).**
- Measured: f-optimal m=5 − production +0.2451 (1.45×, WORSE, fold CI [+0.171, +0.326]); m=5 prefix − production +0.1647 (1.36×, WORSE); non-prefix choice +0.0804 (0.73×, NOT MEASURED, fold CI [+0.0280, +0.1354]); pair-level +0.0934 (0.69×, NOT MEASURED) (S29-L45; `s29/results/s29_B_tta_subset_rows.s*of4.jsonl`; reproduced S29-L48).
- Original interpretation: "escaping the prefix is mildly harmful at best and is not measured to be harmful at all at this n."
- Status: aggregate **WORSE**; hypothesis-specific part **NOT MEASURED**. ORACLE evaluation of native-free selection.

B8. **Tail-then-aggregate VQE endpoint (F5b).**
- Measured (built chain, 126, 9 arms): λ=1 +0.1042/+0.1157 (0.95×/1.03×; s1 WORSE); λ=3 +0.1055/+0.1028 (0.80×/0.81×); λ=1 s1 vs own λ=0 +0.1123 (1.08×, WORSE); deployed tail-set readout flat, max |effect| 0.046; Jaccard with DIS top-75 0.933 → 0.518, m 74 → 39; λ grid split-half transfer +0.047/+0.053 (S29-L54; `s29/results/s29_B_tta_chain_rows.s*of4.jsonl`, `s29_B_tta_end_cloud.json`).
- Original interpretation: "F5b IS REFUTED. The registered prior held on both clauses … The mechanism is alive and irrelevant."
- Status: **refuted as registered**. Deployable-style arms (native-free), evaluated ORACLE.

B9. **The signed amplitude readout** — R4 0.3–4.7 Å worse, median sign_correct 0.50 (S29-L49). Status: **WORSE**.

B10. **The projection-stage bond-length correction (lane P).**
- Measured (built chain, 126): BOND − CTRL-RAND(mean of 8) −0.0087 (0.03× MDE, NOT MEASURED, fold CI [−0.1776, +0.1027]); BOND − PROD +0.7222 (2.24×, WORSE); CTRL-RAND − PROD +0.7308 (3.58×); SPAN +0.1220 (1.65×, WORSE); ISO +0.0737 (1.25×, WORSE, Type-M zone); CTRL-GLOBAL +0.6578 (3.52×); CTRL-INV +0.1671 (0.95×, NOT MEASURED); fit residual 0.8135 → 0.6191 Å; emitted Rg BOND 8.1353 (1.272× native) (S29-L57; `s29/results/s29_P_summary.json`, verified means).
- Original interpretation: "**The mechanism is confirmed and the hypothesis is refuted** … the +0.164 A is the cost of the geometry constraint, not a recoverable loss."
- Status: **REFUTED; all of F-P1/F-P2/F-P3 fail to fire**. DEP (native-free arms).

B11. **Separation-profile (population-profile) correction of the cloud.**
- Measured (point cloud, diagnostic): native-free +0.5782 (2.83×, WORSE, 5/5); ORACLE-fitted +0.5824 (2.56×, WORSE); r ≡ 1 control 0.00e+00 (S29-L22; `s29/results/s29_P_sepprofile_cloud.json`).
- Original interpretation: "closes the POPULATION-PROFILE class of distance-space corrections."
- Status: **refuted** (point cloud only; chain not measured).

B12. **Within-realism-band ordering (lane D's band design, recognition's last open version).**
- Measured: F1 fires on 50/70 cells (DIS in-band +0.5075 R1, +0.5397 R2); **F2 fails on 58/70** (DIS +0.568 global → +0.508/+0.540/+0.361 in-band, paired fold CIs below zero); SS_MATCH −0.009 → +0.060, worth ~1e-3 Å; Gaussian partial correlation overstates (DIS/R1 predicted +0.596, measured +0.508) (S29-L33; `s29/results/s29_D_band_ca.json`).
- Original interpretation: "Conditioning on realism **removes** ordering skill rather than revealing any … this is not a recognition result"; design "SILENT BY CONSTRUCTION about the per-target sign."
- Status: **falsified (F2)**. ORACLE.

B13. **F1, the selection functional (log score) — the direct cost-vs-RMSD test.**
- Measured (built chain, 126): LOG − PROD +0.0822 (0.55×, NOT MEASURED, power 0.34); LOG − SWAPCTL +0.0202 (0.14×, fold CI [−0.1020, +0.1622], 57W/69L, power 0.07, Type-M 6.07); SWAPCTL − PROD +0.0621 (0.78×); L2RISK +0.0440 (0.59×); LOGW +0.0596 (0.47×); LOG − LOGW +0.0227 (0.39×); LOGPERM +0.7295 (2.29×, WORSE, 5/5); error-direction cosine vs production 0.924 mean (random ref 0.177) (S29-L51; `s29/results/s29_M_F1_summary.json`, verified).
- Original interpretation: "**NOT A RESULT** … The log score's entire endpoint effect is indistinguishable from exchanging 20.6 of 75 members at random"; REPORT §4.7: "cost and RMSD will not be made to correlate through this architecture no matter how good the cost gets."
- Status: **NOT MEASURED / pre-registered falsifier fires**; C9 closed. DEP arms.

B14. **Contraction as the lever (third independent confirmation).**
- Measured: LOG cloud +0.0593 Å less contracted (1.34× MDE) and endpoint worse; L2RISK more contracted and also worse (S29-L51); shipped cost's descent expands (bond ×1.0438, Rg ×1.0248, 18/126 contract) (S29-L10); EXPAND field signed cos −0.021, frac>0 0.468 (S29-L35).
- Original interpretation: "Two functionals move contraction in opposite directions and both move the endpoint the same way"; contract rule 25 "CONTRACTION IS JENSEN, NOT THE POSTERIOR."
- Status: **refuted as a lever**; lane M's F1 prereg withdrew the contraction mechanism before running (M18).

B15. **F2, the shell-profile supply gap (the "last structurally live exit on the deployable side").**
- Measured: RATIO cosine 0.0895 vs 0.140 (−0.50×, NOT MEASURED); RATIO − RSHRINK −0.0319 (fold CI [−0.0628, −0.0057]); POOL (pure typicality) 0.122; ORACLE_PROF 0.483; LFO corr(r̂, r_true) +0.313 vs incumbent +0.366; no projections spent (S29-L53; `s29/results/s29_M_F2_supply.json` verified 0.3129/0.3660).
- Original interpretation: "**THE CLASS CLOSES ON A MEASURED SUPPLY GAP** … a fifth instance of `MAE does not price selected RMSD`."
- Status: **closed**; B2 in general explicitly NOT closed (M19).

B16. **The deployed score locating the best member of its own top-128.**
- Measured: 1.4415 bits vs random 1.4050 (+0.0366, 0.10× MDE, 2/5 folds); median paired difference −0.575 bits; below random on 82/126; median rank 72/128 (S29-L53).
- Original interpretation: "at chance for locating the best member of its own top-128, and on the typical target slightly worse than chance."
- Status: **null**. ORACLE diagnostic.

B17. **M6: the deployed quantum stage vs a fixed profile** — point cloud −0.0097 (0.43×), built chain −0.0082 (0.27×), both NOT MEASURED; m-ladder slope −0.00047 Å/unit m; sweep best cell (m = 70) split-half transfer −5% ("NOT A SIGNAL") (S29-L26, L55). Status: **null (quantum stage contributes nothing measurable)**. See QUANTUM_RESULTS.

B18. **Lane T's M6 structure-level clause** ("equals the fixed profile within the floor on ≥ 120/126").
- Measured: 43/126 (cloud), 42/126 (chain), worst 0.58/0.69 Å (S29-L26, L55).
- Status: **false at structure level**, true as endpoint statement; restated by lane T (S29-L29).

B19. **Lane X: chimera configuration-space CVaR-VQE (H2).**
- Measured (n = 12): P1 VQE_g1_s0|R2 − production (chain) +0.4572 (1.18×, WORSE, fold CI [+0.1454, +0.6161], 3W/9L) — GO rule fires backwards; D1p chimera ORACLE − pool ORACLE +0.6533 (0.61×, NOT MEASURED, 5/5); D1 vs scrambled null −0.1086 (NOT MEASURED) vs vs-parents −0.8065 ("87% … order statistic"); all 13 controls NOT MEASURED; corr(H_diag, RMSD) +0.0199; exact argmin 3.9125 vs space mean 3.8771 (S29-L56; `s29/results/s29_X_probe.json`, P1 verified +0.4572/1.18).
- Original interpretation: "The divergent direction is CLOSED, negatively, with a mechanism … no operator can recover 0.65 A that the space does not contain."
- Status: **closed negatively** (scoped to F = 8 parents × contiguous 3-mers × q ≤ 15, 12 targets). Selection native-free; ORACLE rows labelled.

B20. **Lane X's D1 prior** (recombination worth 0.3–0.8 Å ORACLE over the top-8's best member) — "right about the arithmetic and wrong about the science" (S29-L56). Status: **refuted by matched null**.

B21. **Lane X gate 1 (TV > 0.45) as evidence of structure.**
- Measured: TV 0.5765/0.5631/0.5563 but entropy 95.7% of max, ⟨ΣX_q⟩ 88.2% of q ("close to |+⟩^q … an EIGENVECTOR of H_mix") (S29-L56).
- Status: gate **passed for a disqualifying reason** ("My own gate was passed for a reason that fails the condition the gate exists to protect", `s29_X_FINDINGS.md`).

B22. **The typicality/PC1/prefix/profile "tune one global scalar" family** — REPORT §13: "tuning any single global scalar … should not be attempted again"; four scalars with ORACLE global value 0.0–0.6% of per-target gain and LFO on the wrong side of zero (S29-L47 §5). Status: **closed**.

## C. Routes closed without an endpoint run (REPORT §14(a)–(c))

C1. **Better-conditioned coupling matrix / off-diagonal term gradient-visibility** — stable-rank law; any Gram of structural deviations capped at r_stable ≤ 3N_res − 6 ≤ 42 (S29-L11, L36). **Closed by derivation.**
C2. **Non-commuting free-energy cell in the candidate-index encoding** — zero-diagonal coupling's thermal state is a classical reweighting by squared-similarity degree at second order (S29-L15 Q2). **Derived closed.**
C3. **Posterior calibration** — a width error does not move the median map; only separation-band weights change (THEORY §1.4); separation-band re-weighting then withdrawn as a build (S29-L24): LFO per-shell weighted L1 3.058 vs 3.048 (+0.010 Å, from `s12/obj_FINDINGS.md` §4). **"CALIBRATION IS CLOSED, NOT REDIRECTED."**
C4. **Lane T's own §1.4 build recommendation** (separation-band re-weighting as the live form of calibration) — **withdrawn by lane T** (S29-L24; `THEORY.md` §1.4 annotation, §9.2). Band re-weighting shown to be a *different* operator from lane P's rescale by a 4-target probe (`local_only` moves |i−j|=1 ratio 0.885 → 0.802, 46% top-75 overlap; `s29/results/s29_P_bandsel.json`), but closed on the S12 measurement.
C5. **A scorer that prefers near-native structures** — perception–distortion theorem (Blau & Michaeli 2018 Thm 3) (S29-L12); contract rule 22 "forbidden in advance". **Closed by theorem.**
C6. **Better/more averaging** — Krogh–Vedelsby + Ueda–Nakano: infinite pool of the same kind 3.040 Å vs 3.0483, ≤ ~0.008 Å (arithmetic on `s23/results/errdecomp.json`) (S29-L8). **Closed.**
C7. **Supplying the per-target sign from other targets** — Neyman–Scott incidental parameter (S29-L31). **Closed by theory.** Lane L priced a sign classifier: q = 0.70 → 0.035 Å, q = 1.0 → 0.228 Å (ceiling 2.985 Å).
C8. **Importing a published QA method** — none trained/evaluated below 40–50 residues; four signal classes absent/ours/dead here (S29-L1). **Closed.**
C9. **Training an in-band ranker** — S14 0.986 within / 0.600 across vs 0.638 needed; S12 flat learning curve (S29-L19). **Closed by existing record.**
C10. **Correlated-error-breaking literature methods** — each needs trainable members, a known control mean, truth samples, or a known bias ratio; "this instrument has none" (S29-L8). **Rejected.**
C11. **Retrieval by predicted local conformation (PEP-FOLD key)** — lane L's near re-import, closed twice in record (S13 0.517 vs 0.562 baseline on FAIL18; 22-key screen, pool-best 1.711 → 2.161) (S29-L14). **Near-miss recorded.**
C12. **The published peptide "ceiling" (1.96–2.6 Å) as a benchmark** — not like-for-like (S29-L14). **Rejected.**

## D. Smaller withdrawals, defects and wrong priors (recorded in source, not in the 18-row table)

D1. Lane P's mean-of-per-pair-ratios statistic (1.37 at |i−j| = 13) — "withdrawn and was never used" (S29-L22; `s29_P_FINDINGS.md` P9).
D2. Lane P's registered prior "null, 0.0 to 0.3x MDE" — magnitude wrong (BOND 2.24× worse); "not entitled to credit for the second by having written the first" (S29-L57).
D3. Lane P's "a quarter of the cells" arithmetic — primary set is 58% (1890/3276) (`s29_P_FINDINGS.md` P11).
D4. The coordinator's REPORT §11.3 reading "improving the cloud is worth more than it looks" — converse trap flagged by lane P: "the price falling is not the price being saved" (S29-L57; REPORT §9.2c, §11.3; STATE final section).
D5. Lane M's first permutation control — the identity for a sum aggregator, reproduced LOG to every digit on the probe; repaired (S29-L51; `s29_M_FINDINGS.md` item 6).
D6. The coordinator's proposed F1 matched control (monotone re-ranking) — identity by algebra through a top-m readout; declined by lane M (S29-L51; STATE note 12).
D7. Lane L's first-draft sign-classifier price table — "about 4x" too large, corrected in the same entry (S29-L31; `s29_L_FINDINGS.md` L13).
D8. Lane D meter defects — all-NaN cosine axis crashed the renderer after a 126-target CAGEO run; partially defined cosine (lane X cost, 12/126) printed as a measurement; both fixed with regression tests (S29-L10).
D9. Lane D's pre-run expectation that the shipped cost's descent contracts — it expands (S29-L10; `s29_D_FINDINGS.md`).
D10. Lane B's tie rule took `tie[0]` in array order despite its comment — conservative for B's claim, fixed in `7b2e83e1`, max tie set 4 at n = 126 (S29-L38, S29-L45).
D11. Lane B's registered expectation that the R_α readout would "put the arm in a hole" — +0.0271 (0.43×, NOT MEASURED), no contraction (S29-L27).
D12. Lane T's "closing about a third" phrasing — the F figure is 11.1% of the free-energy gap; 30% in m (S29-L32).
D13. Lane T's three-target saturation estimate (3.8–53.8%) — understated; 69% of pairs saturated at |2F−1| ≥ 0.5 (S29-L39).
D14. Lane T's §1.4 over-weighting figure 2.7× — amended to ~1.6× (S29-L29, L39).
D15. `s26/REPORT.md` V.9 "the algebra at the deployed cell is maximal" — false at n = 9, L = 3 (65535 = dim su(256), half of so(512)) (S29-L18; scope correction).
D16. S29-L7's "beta > 1 is expected" reasoning — superseded by A1.
D17. Lane O's near-declaration of a convex-solver defect — was a convention difference (`cf` vs `oa`) (`s29_O_FINDINGS.md`).
D18. `s29/results/s29_O_ladder_table.json` 01:46 version (top-128 chain arm at n = 43, 3.0324 Å) — "STALE", superseded by the n = 126 regeneration (S29-L44, S29-L47).
D19. Lane X shared temp path race (two processes wrote `s29_X_probe_1A13.json.tmp`) — no corruption; fixed in `d6d59487` (S29-L56).
D20. The coordinator's 2.9122 Å (n = 121) — superseded by 2.9027 (n = 126) (S29-L44 addendum 3).
D21. S29-L46 first version "ALL 160 RESOLVE / genuinely dangling 0" — superseded by addendum: 205/217, one genuinely dangling (`s7/debias_tune.json`), two of the unresolved were the audit's own scratchpad-named citations.

## E. Operational failures (REPORT §3.3)

- Governor deadlock (CPU_RESUME left at 80 while bands raised) starved five jobs up to ~40 min; fixed governor v2.6 (STATE note 19).
- Shared git index across eight lanes: files swept into other lanes' commits at least three times (S29-L10 as "S29-L8", S29-L28 as "S29-L27", S29-L33 in `e2e49109`) (S29-L34; contract addendum 4).
- `s26/jobrun.py` does not deduplicate by `--name` (lane M: 4 copies, 220 duplicate rows; lane O: 509 duplicate chain cells; lane X: duplicate 57-min job).
- 36 result artefacts untracked until S29-L46.
- Contract rule 8 (one AMBER process) vs governor `MAX_AMBER = 2`: two AMBER-tagged pytest jobs ran concurrently (S29-L52).
- `jobrun.py` CPU_START = 85 vs governor CPU_CEILING = 101 — throughput bug, unresolved at close; lane P's fix denied by the permission system (STATE final section).
- Lane P's over-broad process filter terminated its own running shard (`s29_P_FINDINGS.md` P11).

## Pre-registration, brief and literature evidence

_Integrated 2026-09-26 from a second importer's reading of the preregs, briefs and lit notes; outcomes from the ledger as cited._

### F. Pre-registered falsifiers that fired against their authors' hypotheses, or priors that failed

F1. **`s29/PREREG_S29_B.md` bright line B1** ("SUPPORTED iff both A_c and G have slope shallower than −1.0 per qubit and n = 9 variance ≥ 1.017e-3"). Addendum 1: "My B1 is therefore already answered NO"; slopes −2.305 / −1.900; to be reported REFUTED. Measured confirmation S29-L36. **Refuted.**
F2. **`PREREG_S29_B.md` M2 gate** (GO iff d ≤ −0.7× MDE, positive split-half transfer, PERM/SPEC < half, PR > 1.5; A1 condition 5: an ORACLE-sign-only win is not a GO). Prior "the gate does NOT open". Outcome S29-L49: 0/24 cells. **Gate closed; M3 not run.**
F3. **`PREREG_S29_B.md` A2 F5b** (TTA endpoint). Prior: "the mechanism works and the endpoint does not move, or moves the wrong way". Outcome S29-L54: **refuted as registered.**
F4. **`PREREG_S29_O.md` rung 6 / H1** (F6a, F6b; prior both fire). Outcome S29-L20: both fire, "harder than registered". **Falsified.**
F5. **`PREREG_S29_P.md` F-P1/F-P2/F-P3** (beat PROD ≥ 1.0× MDE, fold CI excl. 0, 5/5, AND beat CTRL-RAND mean ≥ 1.0×). Prior null 0.0–0.3× MDE; mechanism prediction "the projection price FALLS under BOND … If it falls and RMSD does not, 'the +0.159 A is not a recoverable loss but the price of the geometry constraint'". Outcome S29-L57: none fires; the price fell (+0.1643 → −0.1512) and RMSD worsened; prior wrong in magnitude (BOND +2.24×). A4's MS-OBJ prediction ("lowers obj0 but not RMSD") was **deferred, not run**.
F6. **`PREREG_S29_M_F1.md` primary** (LOG better by > 1.0× MDE). Rule-10 declaration: "asked twice before, both NEGATIVE" (distogram docstring log-likelihood +0.02 to −0.42 vs Bayes-risk +0.16 to +0.82; S7 pure-NLL +0.093 [−0.055, +0.241]; S25 L12 q = 2 +0.0176 at 0.96×). Probe (n = 12, "not evidence for the instrument"): PROD 3.3816 / LOG 3.6161 / L2RISK 3.5632 chain. Addendum 1 withdrew the contraction mechanism. Outcome S29-L51: **NOT A RESULT.**
F7. **`PREREG_S29_M_F2.md` stage 2** (cos > 0.140 AND beat shrink twin > 1.0× MDE). Rule-10: two prior closures (S12 deployable shell profile 3.163; S12 §6 eleven LFO arms "Nothing wins"). Addendum 1 pre-run position "genuinely close to the line" (0.24 / 0.16). Addendum 2 records rule 20's cosine justification withdrawn. Outcome S29-L53: **stopping rule fired; class closed.**
F8. **`PREREG_S29_D_band.md` F2** (in-band > across). Prior: F1 does not fire; "F2 may well pass while F1 fails, and that combination is not a result." Outcome S29-L33: the reverse — F1 fires, **F2 fails on 58/70**.
F9. **`PREREG_S29_D_m6.md` F-M6a** (structure-level ≥ 120/126). Prior: fails on set equality but passes on structure. Outcome S29-L26/L55: **fails on structure too** (43/126, 42/126); F-M6b does not fire as prior expected.
F10. **`PREREG_S29_T.md` F1** (compactness objection confirmed; prior ~3:1). Outcome S29-L50: **F1 fails, F2 fires** — prior refuted.
F11. **`PREREG_S29_X.md`** D1 prior (recombination worth 0.3–0.8 Å) and P1 GO rule — outcome S29-L56: D1 branch (b) fires against the scrambled null; P1 fires backwards (+1.18× WORSE). A3's refutation rule for "the untrained circuit is the best non-oracle arm" (|UNTRAINED R3 − trained R3| < 0.7× MDE or BESTOFN reproduces) — "checked at n = 8 … both point that way"; confirmed at n = 12 (NEGATIVE_RESULTS A18).

### G. Brief-level corrections
- `s29/briefs/S29B.md` gate constant 2.954 — corrected in `PREREG_S29_B.md` to a paired per-target comparator ("2.954 is the S10-5 ORACLE ladder from another pool era").

### H. Literature imports rejected (lane L; `s29/lit/`, one line per family)
- **`L_1_native_free_qa.md`:** VoroMQA, ProQ2/3, ProQ4, DeepAccNet, QMEANDisCo, GraphQA, EnQA, MD-MAE — REJECTED; consensus QA (DAVIS-EMAconsensus, Pcons, PWCom) rejected at family level ("assumes independent member errors; our pool is 68% common-mode", CONS_POOL@chain pref 0.056); quasi-single-model QA rejected as unavailable (flagged); supervised QA on project features already run (S28-L48: 0.960 vs RAND_SIGNED 0.952). Correction: "committed and resumable (`python -m s8.relax best`)" is "MY ERROR and is FALSE".
- **`L_2_correlated_error.md`:** negative correlation learning, control variates, multifidelity MC, Richardson two-source extrapolation (H1 "REJECTED as stated"), boosting/residual correction, recycling — each lacks an input this instrument has.
- **`L_3_decision_theory.md`:** post-hoc temperature calibration (Guo 2017; argmax/median-invariant) and changing the training scoring rule (log score already strictly proper) — REJECTED.
- **`L_4_quantum.md`:** "Topic 4 yields no RMSD lever"; Cerezo 2021 NOTED only (2-design assumption not met); "The project has never satisfied both" (C1)+(C2).
- **`L_5_peptide_ceiling.md`:** "There is NO published ceiling"; PEP-FOLD structural-alphabet retrieval key nearly re-imported — closed twice in record; torsion head, structure-trained predictors, sOPEP, MD, chemical-shift restraints: NO or CLOSED.
- **`L_6_matched_realism.md`:** a null from the current library "would NOT close the in-band question" (scorers fitted for the between-band task).
- **`L_7_inband_training.md`:** Jing/Dong SVMrank decoy LTR and ProQ4 pairwise — REJECTED (gains measured between bands, RMSD 0–12 Å); LambdaRank weighting NOTED only; "Do not build a better in-band ranker."
- **`L_8_conditioning.md`:** MSA depth, recycling ("OPTIMISATION, not information"), templates, confidence heads — REJECTED as conditioning sources here; phase retrieval, PCA sign gauge, one-bit compressed sensing — negative transfers; the PC1-sign regression priced as a mechanism measurement only (q = 0.70 → 0.035 Å; ceiling 2.985 Å).
