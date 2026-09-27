_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s30/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 30 — Negative, null, killed, falsified and retracted results

The sprint's own count: 91 hypotheses entertained — **58 killed by measurement, 19 by theorem, 8 by price, 6 still open** (`s30/REPORT_S30.md` §7). *"A hypothesis killed by measurement can be reopened by a better instrument; one killed by theorem cannot … one killed by price is not wrong."* This file indexes every negative the source records, grouped by component. Quantum-component negatives are summarised here and detailed in `QUANTUM_RESULTS.md`.

Conventions (from `s30/S30_CONTRACT.md`): ×MDE = |effect| / (2.8016·SE); < 0.7× "not a result", 0.7–1.0× "NOT MEASURED". Basis stated per item (CA cloud = point cloud intermediate; chain = built-chain endpoint). Leakage: ORACLE (reads native) vs native-free.

---

## A. The endpoint

### A1. No accuracy improvement
- **Measured:** mean built-chain RMSD 3.2105 Å unchanged; < 3.0 and < 2.5 not reached; *"Zero — nothing was deployed"* (`s30/REPORT_S30.md` §0.1). The one confirmed applicable effect (AMBER relax k = 30) is −0.0221 Å, 0.69% of baseline, not deployable (§0.1, §11.2; `s30/results/s30_G_disp2.json`).
- **Original interpretation:** *"There was no gain. The sprint's contribution is the reason why"* (§0.1 row 11).
- **Status:** final.

## B. Quantum stage (details in `QUANTUM_RESULTS.md`)

| item | measured (source) | status |
|---|---|---|
| B1. Circuit on the deployed native-free objective | `circ_opt` 3.4330 Å chain vs PROD 3.2071 (same 9q circuit reaches 0.2516 on ORACLE objective) (`s30/results/s30_D_meter_DIS_chain.json`) | negative; *"worse than the classical average it was meant to improve"* (§5.2) |
| B2. CVaR tail stops being a prefix under some condition | T1: never (`s30/THEORY.md` §2) | killed by theorem |
| B3. S29 §4.5 "lifted CVaR readout reaches non-prefix optimum" / "classical counterpart genuinely goes away" | incompatible with S29 §4.3 by T1 | WITHDRAWN (S30-L9) |
| B4. Endogenous-order lift opens a combinatorial search | 24.3–175.5 bits vs 300.6 (T1b); pair-distance r_stable 1.859 | closed by price (scope: coordinate r_stable 3.404/3.619 does not fire the rule) |
| B5. HALFSPACE − PREFIX −0.9816 Å "BETTER" | 196% accounted by across-target null; transferable rule +0.4724 Å WORSE, 1.88×, 5/5 (S30-L15 §3c) | RETRACTED by lane T |
| B6. Quadric / second-moment escape | +0.2059 (1.81×, 37W/89L, Q) and +0.0860 (2.95×, 5/5, T); disp2 3.3585 vs 3.0483 CA | closed by measurement |
| B7. Finite-shot CVaR bias as mechanism | bias +0.0000…+0.0025; argmin unmoved | REFUTED (opposite direction) |
| B8. Sparse weighted readout (L6) | argmin beats every fully-priced sparse arm B = 3…9 by +0.1622 to +0.7267 CA; chain 2.1683 @11.4+ bits vs 2.1435 @7.0 (`s30/results/s30_Q_sparse.json`) | closed by price; F4 REFUTED |
| B9. Torsion/configuration encodings | 25.9–77.8 bits vs 7 qubits | closed by price |
| B10. Subset cardinality as bit allocation | 0.044 vs 0.132 Å/bit | closed by price (dominated 3.0×) |
| B11. Submodular / DPP / QUBO machinery for set selection | V non-monotone; constant on centroid classes; Frank–Wolfe upper-bounds any circuit | killed by theorem / rejected |
| B12. Non-diagonal Hamiltonian (L9), ADAPT-VQE (L10) | not built | not pursued (precondition / pre-check) |
| B13. `core/pipeline.py:821` "+0.113 Å" CVaR role | withdrawn in S25-L5 (−0.1126, 0.51×; −0.1405, 0.68×) | open defect in shipped code |

## C. The failure tail (FAIL18) — lane F, D, X, G

### C1. Tail is pool-limited (F1a) — REFUTED
- **Measured:** ORACLE best-of-pool FAIL18 2.2842 Å CA (2.2845 chain), 13/18 < 3.00, worst 3.5436 (`s30/results/s30_F_stagegap.json`); worst-18-by-production 2.5298, 11/18, worst 3.9523 (`s30/AUDIT_V.md` D3). ORACLE.
- **Interpretation:** *"The tail is NOT pool-limited"* (S30-L2 §2).
- **Status:** hypothesis killed by measurement (report §7.1 #1); F1a stands after S30-L23.

### C2. F1c FAIL18 filter row (+1.7674 Å, 3.87× MDE, 0W/18L) — WITHDRAWN as an effect estimate
- **Measured:** lane D reproduced −1.7622 (opposite sign convention); by `keep` stratum: keep=0 (= FAIL18) −1.7622, keep=1 −0.0363, keep 2–3 −0.8654, keep 4–8 −0.0039, keep ≥ 9 +0.0380; Spearman(keep, effect) over 108 = −0.046; predicate forces |effect| ≥ 0.869 Å (49%); outside the 18 the filter is +0.0245 Å; all-126 effect 100% the 18 (S30-L23). Filter-independent tails: +0.6708 (p 0.0148), +0.6320 (p 0.0300) (S30-L2 §6).
- **Interpretation:** *"S30-L2's headline is conditioned on its own numerator"*; *"a matched control in the right space does not rescue a stratum defined by the outcome"* (S30-L23).
- **Status:** withdrawn (report §7.1 #15; App. A.5). The +0.63/+0.67 filter effects survive.

### C3. F1b "fires on all three clauses" — NOT ESTABLISHED, not formally withdrawn
- **Measured:** share_filt ratio 2.21; G_filt FAIL18 2.3932 vs random-18 null [0.2690, 0.9880], p = 0; 18/18 above difficulty band, mean z +4.99 (S30-L2 §4) — all on the forced quantity.
- **Interpretation:** S30-L2 §4 still reads *"F1b FIRES on all three registered clauses"*.
- **Status:** contradiction recorded by lane Y and coordinator; report lists as *"NOT ESTABLISHED, and not withdrawn either"* (§7.4 #1; S30-L28 #1).

### C4. BLOSUM retrieval harms the tail — NOT MEASURED (not exonerated)
- **Measured:** BLOSUM-500 vs random-500 ORACLE best: FAIL18 −0.0034 (0.01× MDE, MDE 0.2902, power 0.05, type-M 71); all −0.0722 (0.87×); other-108 −0.0837 (0.99×) (S30-L2 §3; `s30/AUDIT_V.md` D6).
- **Interpretation:** S30-L2 wrote *"Retrieval is exonerated at every stratum"*; revised after AUDIT_V D6 to *"absence of evidence, not evidence of absence"* and flagged as this sprint's control-space mismatch (report §4.1, §6.1).
- **Status:** NOT MEASURED; the original "exonerated" claim was corrected.

### C5. Wider filter is a free lunch (F2a) — REFUTED
- **Measured:** benefit-retained vs harm-shed cross smoothly ~55%/55% near k ≈ 275; no k fires (e.g. k=128 95.0%/20.6%; k=300 60.3%/59.6%) (S30-L16 §2; CA cloud, ORACLE).
- **Status:** refuted by lane F's own measurement (App. A.5).

### C6. Deployable filter width (F2b) — closed by ceiling
- **Measured:** emitted cloud mean vs k: k=75 3.0483 (production) is the minimum; k=500 +0.3790 (1.59×, 5/5) (S30-L16 §3; AUDIT_V: k75_m75 = 3.04834 minimum of all 41 cells, `s30_F_width_cloud.json`).
- **Interpretation:** *"The ORACLE global argmin over k is k = 75 — the shipped value"*; fifth instance of the single-global-scalar pattern.
- **Status:** closed without spending the chain. Lane F had pre-registered it expected F2b to fail.

### C7. Filter width behaves like averaging width (F2c) — REFUTED
- **Measured:** filter width moves emitted cloud 0.3790 Å vs averaging width 0.0256–0.0927 (4–15×) (S30-L16 §1).
- **Status:** refuted (a methodological positive: S29's flat m-sweep does not transfer to filter width).

### C8. Widening rescues hard targets — does not replicate (circular)
- **Measured:** FAIL18 −0.6193 at k = 400 (null p = 0) but worst18_bestpool −0.0081 and worst18_poolmean **+0.7313** (reversed); one mechanism ρ = +0.81 with filter set-mean benefit (S30-L16 §4).
- **Status:** killed by its own filter-independent control (report §7.1 #4).

### C9. Regression to the mean explains widening's tail gain — REFUTED
- **Measured:** predicted +0.069 vs observed −0.619, residual −0.688 (S30-L16 §4).

### C10. Lane L's scale-separable term is the filter-collapse mechanism (F3c) — does not fire (provisional)
- **Measured:** partial Spearman(ρ_pool, |scale error| | shape) −0.067, p 0.46; shape −0.641, p 6.5e−16; |scale error| 3.23× on FAIL18 vs shape 1.93×; shape 83.1% of tail error (91.2% all, 94.2% other-108) (S30-L17 §3; AUDIT_V D7, AUDIT_Z D22).
- **Status:** refuted as mechanism, **provisional** — *"statistic guessed by lane F; lane L was unreachable"*.

### C11. "Confidently wrong" (F3d) — REFUTED
- **Measured:** error×confidence −0.729 vs error alone −0.799; gain −0.069 vs +0.10 bar (S30-L17 §4).

### C12. Pool Rg dispersion predicts filter failure — NOT MEASURED
- **Measured:** F4 pool Rg sd −0.128, fold CI [−0.316, +0.036] (S30-L17).

### C13. FAIL18 tail is conformational ambiguity in NMR references (H-X2) — PRICED AND DEAD
- **Measured:** floor RMSD(medoid, model 1) mean 0.6136 Å (median 0.3784, 21.4% > 1 Å); tail minus rest: floor −0.1776 (−5.0% of excess), spread −0.4872 (−13.6%) (`s30/results/s30_X_ensemble.json`, confirmed). 111/126 multi-model.
- **Interpretation:** *"the hard 18 have tighter deposited ensembles"*.
- **Status:** dead with sign reversed; lane X had predicted it would die. **Caveat:** the "FAIL18" in this analysis is actually worst-18-by-endpoint (`s30_X_ensemble.py:96-97`) (S30-L28 #3).

### C14. Radial field direction "anti-aligned on hard targets" — WITHDRAWN (0.67× MDE)
- **Measured:** cos(direction to native, radial) all −0.0675 (0.74× MDE), FAIL18 −0.2524 (SE 0.1337, 0.67× MDE; one fold −0.6491 carries it) (`s30/AUDIT_V.md` D5).
- **Status:** the anti-alignment half is withdrawn; "orthogonal in general" retained as a null (report §4.3).

### C15. ORACLE FAIL18 gate prize "too small to measure" generalisation
- **Measured:** ORACLE gate (widen to k = 400 where filter hurt set mean, 16/126 targets) −0.1193 Å cloud, 1.29× MDE vs lane C's −0.0474 chain, 0.62× (S30-L16 §5). ORACLE router.
- **Interpretation:** the "even a perfect detector is too small to measure" half of lane C's closure *"must not be quoted as a general property"*; router family stays closed on its first ground.
- **Status:** router not built; closure wording narrowed.

## D. Recognition / scorers — lanes R, G, D

### D1. F-R1: nativeness recognisable from single-structure geometry — does NOT fire
- **Measured:** 43 channels; ordering clause fires on 2/43 (DIS +0.347, anchor contrast +0.134, p_max 0.000; DIS_MEAN +0.335/+0.101); preference fires on none (best `pref_near` RAMA 0.640, pool control 0.790); DIS prefers production to a 0.55 Å structure on 94.2% (`s30/results/s30_R_verdict.json`; S30-L19). Floor 0.347 Å.
- **Status:** null; registered prior (4:1) held. ORACLE labels, native-free channels (A3: no `nat_ca` attribute; test `tests/test_s30_R.py::test_t4`).

### D2. Leave-fold-out 40-channel combination recognises nativeness — NO
- **Measured:** prefers 0.55 Å structure on 93.0%, random pool member on 100%, 3 Å rung on 100%; margin −0.070 [−0.110, −0.028], 1.04× MDE, 4/5 folds, n = 114; label-shuffled margin +0.114 (S30-L19).
- **Interpretation:** *"It learned 'is this production?', not 'is this near-native'"*.

### D3. LEG_torsion (S29 §12.0's last outside-class-M hope) — closed negatively
- **Measured:** anchor contrast +0.024 [+0.010, +0.038] (quarter of +0.10 bar); pref 0.503 vs pool control 0.698; native at 0.503 percentile of its own ladder (S30-L19).
- **Status:** killed; coordinator's wording "at chance" withdrawn (CI excludes zero) (App. A.1).

### D4. Per-residue/local channels — killed by theorem-on-instrument
- **Measured:** held-out ΔR² local −0.0894 [−0.1217, −0.0522] vs global +0.5997 (84 vs 80 features; local block ORACLE-advantaged) (`s30_R_verdict.json` D1, confirmed).
- **Interpretation:** *"A sum of per-residue terms cannot see a lever arm."*

### D5. Size-invariant twins decorrelate from Rg — NO
- **Measured:** RG_LAW rel. sd 0.5009 → 3.2e−16; but CONS −0.374 → −0.807, DMAP_CONS −0.050 → −0.729, POOLGO +0.611 → −0.678; DISTPOT_SI does improve over DISTPOT (+0.193 vs +0.136) (S30-L19).
- **Interpretation:** *"a correctness fix, not a decorrelation"*.

### D6. Lane R 0.500/0.500/0.500 cell — null-input artefact (withdrawn)
- **Measured:** channel filter required `d_near` on every row; 3 targets lack a sub-1 Å rung → empty channel set (S30-L19 disclosure).

### D7. S28-L48 "20 of 31 scorers prefer production to a 0.25 Å ORACLE structure" as evidence nativeness is invisible — WITHDRAWN (cross-kind)
- **Measured:** no new data; rungs differ in construction (projected average vs circuit output vs LS fit vs perturbations) (S30-L1).
- **Interpretation:** survives only as *"no native-free scorer prefers a near-native structure of a DIFFERENT CONSTRUCTION to the production average"*; perception–distortion predicts the cross-kind half.

### D8. Chiral functionals carry nativeness signal (F-G2) — does NOT fire
- **Measured:** WRITHE anchor contrast +0.0405 [−0.0255, +0.1015], 0.41×, 3/5 vs max-over-3 null mean 0.0408, p_max 0.430; CHIRAL3 −0.0363; CHIRAL3_LONG −0.0394 (corrected in place from −0.0391); WRITHE − |WRITHE| +0.0170, 0.29× (`s30/results/s30_G_chiral.json`, confirmed; S30-L26).
- **Status:** null; *"G1's survivor family … measured and empty"*, length-scoped (9–16mers).

### D9. Lane G's registered mechanism (chiral coordinate degenerate at peptide length) — REFUTED
- **Measured:** occupancy WRITHE 0.685, CHIRAL3 0.953, CHIRAL3_LONG 0.965 vs DIS 0.345 (pool) / 0.231 (ladder) (S30-L26).
- **Interpretation:** refutation made the negative stronger (*"the easy explanation is gone"*).

### D10. WRITHE preference contrast +0.1641 (2.17×, 5/5, p = 0.000) — SELF-KILLED (cross-kind)
- **Measured:** kind-matched rebuilt-native percentile WRITHE 0.6061 [0.5609, 0.6522], |WRITHE| 0.6732 — worse than 0.5 chance; DIS 0.2876 (S30-L26; `s30_G_chiral.json`).
- **Status:** withdrawn by lane G before being quoted. Count of cross-kind instances: STATE Note 15 and SYNTHESIS_Y say "third"; report §A.7 / §7.1 #46 corrected to "Second" (AUDIT_V D13, AUDIT_Z D21).

### D11. Any achiral single-structure channel / charter's candidate list as "new channels" — killed by theorem (G1, G1a, G1b)
- **Measured/derived:** classical MDS; contact topology, Rg profile, inertia, SASA etc. are reflection-invariant ⇒ functions of D; three references only (distogram, pool, universal physics) (S30-L26).

### D12. Deflating the radial/scale direction creates rank — NO
- **Measured:** radial share of Gram trace 0.5798; cos(PC1, radial) 0.947; stable rank 1.705 → 2.642 with radial removed; residual 42% no large eigenvalue (S30-L22).
- **Interpretation:** *"the size-matched field IS the deflated field"* (lane L conceding its constructive proposal, S30-L18 §8).

### D13. S29 "median target worse than chance" — WITHDRAWN
- **Measured:** 7 − log₂r right-skewed: null mean 1.4050, median 0.9888, win rate 62.5%; all five statistics p = 0.16–0.75; KS D 0.0685 p 0.571; χ² 8.35 p 0.303; "82 of 126" vs null 78.8 (S30-L4).
- **Status:** "at chance" survives and is strengthened; "worse than chance" withdrawn (coordinator reported it to the user twice).

### D14. S29 "no field's mean |cos| clears 0.140" — WRONG (label and null)
- **Measured:** mean |cos| 0.2505–0.3249, clears 0.1398 on 21/21; vs correct signed null (+0.0014 ± 0.0144) 11/21 fold CIs exclude zero, best +7.7σ (CHAN_DISTPOT +0.1128) (S30-L5).
- **Interpretation:** B2's number survives (fields worth 0.0195 Å because √(1−ρ²) squares them); its argument withdrawn.

### D15. The 21 fields combine past ρ = 0.358 — NO
- **Measured:** ORACLE global ρ 0.1693 (0.69 bits vs 3.22; 0.046 Å chain); LFO equal weights 0.0948; LFO 21-param 0.0124; best honest arm vs best single −0.0267, −0.36×; Gram stable rank 2.057 aggregate / 1.681 per-target (n = 119) (S30-L21; `s30/results/s30_D_gram.json`, confirmed).
- **Status:** closed; lane D's own falsifier not met.

### D16. ORACLE per-target combination ρ 0.9491 as a ceiling — NO
- **Measured:** matched random 21-dim subspace 0.8095; excess +0.1396, 6.83×, 5/5 (S30-L21).
- **Interpretation:** *"Without that control this would have gone into the record as a 0.97 Å result."*

### D17. S29 built-chain preference contrast +0.0635 (0.92×) — WITHDRAWN
- **Measured:** 8 draws: +0.0357, 0.56×, fold CI [−0.011, +0.082], 3/5; S29's seed-0 draw was the maximum of eight; CA version confirmed +0.1716, 1.84×, 5/5 (S30-L24).

### D18. Meter could gate new costs on the chain basis — it could not (fixed)
- **Measured:** 0/126 ladder-cache files carried chain projections; CHARTER ρ sign differed by basis (+0.2603 CA vs −0.0921 chain as stated in S30-L3) (S30-L3 §3).
- **Status:** fixed; see LESSONS importer notes for the −0.0921 vs −0.1964 discrepancy.

### D19. "Run `selftest` to confirm baselines" — unsatisfiable instruction
- **Measured:** selftest is an 8-residue synthetic check (0.4 s) (S30-L3 §2a). Replaced by `verify`.

### D20. Shipped cost as a structural objective
- **Measured:** meter gate BLOCK on both bases; S28 ladder ρ −0.4023 chain [−0.477, −0.322], 5/5; cosine −0.0339 (z −2.45) CA; native percentile 0.3676 (`s30/results/s30_D_meter_DIS_chain.json`, confirmed). 32-cost sweep: DIS ranks 12th of 32 on contrast (0.56×), second-worst ladder ρ; no cost ranks the native inside its pool better than 0.37 (`s30/REPORT_S30.md` §10.6).
- **Interpretation:** *"coarse ordering is common and cheap; in-band selection is absent everywhere."*

## E. Prior correction / common mode — lanes L, P

### E1. Common mode estimable from pool — killed by theorem (S30-L7)
- **Derived:** under `w_k = t + μ + d_k`, likelihood depends on (t, μ) only via t + μ; m_eff = 224.18/160.36 = 1.398. Relative to model class M, pool-only.

### E2. E1 escape (prior on bias form) — closed three ways (S30-L13)
### E3. E3 escape, obvious form (different candidate source) — refuted by S24 provenance cosine 0.9432 vs 0.9330 within-source control (S30-L7)
### E4. PCA / factor models / ICA, EIV, Reiersøl, multichannel blind deconvolution, instrument calibration, bagging/consensus QA — rejected by theorem/assumption (S30-L7, S30-L18 §6; `s30/lit/L30_2_common_mode.md`, `L30_4_shared_bias.md`)

### E5. EDM projection / triangle repair — prohibited (re-import caught)
- **Measured (S19, cited):** incoherent magnitude-matched field worse on realisability (defect 0.340, 10.85% violations) yet 1.24 Å better; ρ(EDM defect, RMSD) +0.511 vs residual RMS +0.891 (S30-L18 §1).

### E6. Decorrelation as the lever — killed by price
- **Derived:** orthogonal channel must carry ρ 0.3398 vs 0.3580 alone (5.1% discount); must be 3.01× better than anything owned; 10.1 orthogonal channels needed (S30-L18 §4). Scope: pool-space operators, not the prior.

### E7. P1: native-free features price the ORACLE displacement out of fold — NULL (P1 held)
- **Measured:** best arm R² 0.0083; excess +0.0095, 0.75× MDE; C-PERM −0.0388; applying fitted displacement 3.0519 vs 3.0483 CA (S30-L25).
- **Status:** registered null held; not a falsifier firing.

### E8. Global 5-number profile / pool-estimated profile — zero or wrong sign
- **Measured:** LFO_GLOBALPROF5 +0.0036 (0.11×); NF_POOLPROF5 +0.0395 (0.48×, wrong sign); per-target dispersion ~9× mean (S30-L25 §3). CA cloud.

### E9. Implied-endpoint conversion from ρ is a fair summary — NO
- **Measured:** ρ → 3.0338 implied vs 3.0519 applied (S30-L25 §1).

### E10. Per-residue corrections beat 5-number profile; single offset/stretch corrects the prior — NO / NOT MEASURED
- **Measured:** ORACLE_PERRES −0.5714 vs SEPPROF5 −0.5740; OFFSET1 −0.1443 (0.87×), STRETCH1 −0.1501 (0.85×) (S30-L25 §3). ORACLE.

### E11. Coordinator's 3:1 prediction that long-range R² ≈ 0 — FALSIFIED (raw +0.1959)
- **Measured:** N0 −0.0205; N1 calibration +0.1406; N2 posterior −0.0184; N3 pool +0.0758 (S30-L27 §2).

### E12. Long-range R² is a route — NO
- **Interpretation:** +0.1406 is calibration (already closed); bar was registered for aggregate displacement R², not pair-space R² (*"a category difference, not a clearance"*).

### E13. Fitted prior corrector helps once accurate enough — NO
- **Measured:** N3 (R² 0.2355) applied +0.0554 CA, 0.68×, NOT MEASURED; N1 +0.1461 (0.91×), N2 +0.1513 (0.95×); vs ORACLE i.i.d. −0.2466 (1.77×) at R² 0.2349 (`s30/results/s30_P_lr.json`, confirmed).
- **Interpretation:** *"a 0.30 Å swing at matched accuracy"*. AUDIT_Z D3: the report originally called +0.0554 "the best *measured*" and "strictly harmful"; corrected to "does not help, not that it measurably hurts".

### E14. Native-free sign channels supply the five signs — NO
- **Measured:** baseline 0.556/0.571/0.579/0.643/0.627; best POOLDIS75 0.667, +0.040, 0.25×; every channel emits worse (+0.0401 to +0.1492 CA) (S30-L27 §1; `s30_P_sign.json`).

### E15. Lane L's "AMBER-relax benefit concentrates on divergent pools" downgrade — the WITHDRAWAL was itself withdrawn
- See `LESSONS.md`; measured confirmation in S30-L26 (97.2% in high half; −0.0406, 3.56×).

### E16. E2 divergence effect as a tail intervention — NO (on size)
- **Measured:** targeting divergent half −0.0215 vs whole −0.0221; FAIL18 −0.0113 vs 108 −0.0239 (0.22×); worst18_poolmean −0.0386 vs −0.0193 (0.31×) (`s30_G_disp2.json`; AUDIT_V D1).
- **Status:** E2 out of mechanism column *"on SIZE, not on reach"* (report §A.7); both tail legs NOT MEASURED and point opposite ways.

### E17. Lane G's 2:1-against concentration — wrong (and its reasoning)
- **Measured:** ρ(d, DISP_rmsd) −0.316, p₂ 0.000; mediation ρ(DISP, contraction) +0.947 (S30-L26).

## F. Generation / readout — lane X, Q

### F1. "Measure the ceiling first, always" gate — ANTI-PREDICTOR
- **Measured:** sign correct 1/10 vs source law 5/6; |residual| 0.333 vs 0.0153 Å (22×) (S30-L10 §1). ORACLE ceilings.
### F2. H-X3 better typical member — NO (H-X3 stands)
- **Measured:** all d_set_mean positive; best T3_pool +0.0409 (0.57×); counting falsifier 24.80% vs 25% (tied, decided nothing); split-half transfer of d_B +0.1597 [+0.0676, +0.2687] (S30-L20).
### F3. "Nobody built a typical-good generator" — false; T0_helix S 0.5676, endpoint 3.7892 CA (worst in record)
### F4. corr(S, B) = −0.4744 — artefact of T0_helix; +0.0851 without it (withdrawn by lane X; AUDIT_V D9 on presentation)
### F5. "Generation closed on five instruments" — only one carried an oracle arm; T2_restype beats whole pool best on 45/126 targets yet endpoint +0.0157 (S30-L10 §4)
### F6. "68% common-mode, 50.7× i.i.d." as a cap on generation — not independent evidence (`‖ē‖² = n·RMSD²` exactly) (S30-L10 §6)
### F7. Native-free support rule for sparse readout (F3) — confirmed and worthless: +0.364 over random at s = 2, every arm above production (3.198 vs 3.048 CA) (S30-L11)
### F8. The "two qubits" synthesis — withdrawn one minute after posting (STATE 13:07/13:08); register half open (see QUANTUM_RESULTS Q14)

## G. Theory lane's own misses (lane T)
- **P2b** retrieval Å gain +0.10–0.30 registered; measured 0.0715 (0.79×) — REFUTED 2–4× (S30-L14 §2).
- **P4c** searched classes beat prefix by < 0.6 Å; measured 0.982 — missed by 64% (falsifier 1.0 not crossed) (S30-L15 §1).
- **"12 bits ≈ six coefficients"** — unregistered aside, withdrawn; corrected to 3.78 (S30-L15 §3).
- **Halfspace headline** — retracted (B5).
- **P5c** — not scored; mechanism wrong (lane D's ridge degenerated to 0.0124) (`s30/THEORY.md` §10).
- **P5d** — post-hoc, declared not a pre-registration; would have been falsified (0.607 vs [0.15, 0.40]).

## H. Report-level retractions (adversary audits)
`s30/AUDIT_V.md` (18 defects) and `s30/AUDIT_Z.md` (23 defects) — each defect removed a multiplier, stratum label, basis, count or over-claim; *"None removes a result"* (both audits). The most consequential: D2(V) 5.2× multiplier `d`-dependent; D1(V) E2 tail argument on wrong stratum; D1(Z) coh gate called native-free but ORACLE; D2(Z) −0.0406 is a contrast not the relax gain (−0.0221); D3(Z) +0.0554 is 0.68× NOT MEASURED; D4(Z) ORACLE label missing on −0.126/−0.247 in two graphics. Report App. A lists 26 withdrawn claims (10 the coordinator's).
