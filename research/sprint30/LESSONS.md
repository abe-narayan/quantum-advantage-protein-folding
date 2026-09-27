_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s30/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 30 — Lessons the sprint itself recorded

Every lesson below is attributed to the source file that states it. Wording in "double quotes" is verbatim.

## 1. Checklist entries the sprint declared (`s30/REPORT_S30.md` App. A.6, and STATE)

1. *"A matched control in the right space does not rescue a stratum defined by the outcome."* — from S30-L23 (FAIL18 is defined by the filter's own recall; `s30/LEDGER.md` S30-L23; `s30/STATE.md` Note 9).
2. *"When a statistic is a nonlinear transform, its mean, median and win-rate have three different nulls — never read one against another's baseline."* — from S30-L4 (`7 − log₂r` right-skewed: null mean 1.4050, median 0.9888, win rate 62.5%).
3. *"'The winning direction is the same direction twice' is a failure mode distinct from the order-statistic one, and needs a common direction bank to detect."* — from lane T's retraction (S30-L15 §3c).
4. The fourth checklist entry: *"An implied-endpoint conversion from ρ is an upper bound attained only by a perfectly calibrated correction. Always also APPLY the correction and measure the endpoint."* (`s30/STATE.md` Note 14; S30-L25 §1: implied 3.0338 vs applied 3.0519 vs production 3.0483).

## 2. Statistical discipline lessons

- *"A control that is itself a random draw needs its own draw distribution reported, and the number of draws must scale inversely with the effect size."* S29's single seed-0 draw was the maximum of its own eight (S30-L24; `s30/STATE.md` Note 13). *"A single-draw control is least trustworthy exactly where the effects are smallest — which is where this project's remaining effects live."*
- *"A statistics library encodes a direction as well as a test"*: `s24.stats_lib.compare` is lower-is-better; fed a higher-is-better rate its verdict reads `WORSE` for the good direction (`s30/REPORT_S30.md` §6.3). Lane P hit the same trap *"in a lane that had just read the entry about it"* (S30-L25; `s30/AUDIT_Z.md` D12).
- Three (later four/five) *"statistic/null mismatches"* are *"the same defect wearing three costumes"* (`s30/REPORT_S30.md` §6.3).
- Two different nulls for a cosine: per-draw |cos| 0.1398 vs 126-target-mean null sd 0.0144; *"A lane reading its new cost's +0.09 cosine against 0.140 would discard a field that is 6 σ from the signed null"* (S30-L5; meter extension E5).
- *"The surviving positives are the ones at 2–10× MDE with 5/5 folds, not the ones at 1.2×"*; max-over-channels nulls *"is the standard the next sprint should inherit for any swept family"* (`s30/REPORT_S30.md` §6.2).
- *"A sprint-wide multiplicity register, written to as comparisons are emitted, is a build item for S31 — not a discipline problem to exhort about"* (`s30/REPORT_S30.md` §6.2).
- *"A pre-check that can only remove your own excuse is worth running before the contrast, not after"* — lane G's chirality occupancy pre-check (`s30/REPORT_S30.md` §6.4).
- *"Two lanes agreeing did not make a prior"* — lanes L and G each revised on an object that was not the one under test (`s30/REPORT_S30.md` §A.7; S30-L26).
- A withdrawal is a claim too: *"A withdrawal is a claim too, and it can be wrong in the same ways"* (`s30/REPORT_S30.md` §A.7).
- `or 0` on a possibly-absent key *"manufactures data"*; *"Sixteen identical values across sixteen different costs"* was the signature (`s30/REPORT_S30.md` §10.6.1); same signature caught lane R's 0.500/0.500/0.500 null-input artefact (S30-L19).
- Stable rank *"must never appear without its feature space in the same sentence"* (pair-distance 1.859 vs coordinate 3.404/3.619) (`s30/THEORY.md` §3.1; `s30/briefs/Q_to_T_quadric_and_rank.md` §4).
- `W/L` cannot diagnose an order statistic; *"only split-half transfer can"* (`s30/THEORY.md` §4.3).
- The 1.16 set-mean coefficient does not map cloud to chain; *"Use 0.92, measured here on two independent arms"* for prior corrections (S30-L27 annotation; `s30/STATE.md` Note 16).
- The FAIL18/108 split: *"fold 0 contains no FAIL18 target"*, so every FAIL18 CI draws from four clusters (S30-L3 E2).
- Endpoint reproducibility: the cloud→chain projection seed is not pinned; *"any future claim below ~0.01 Å on the built chain is inside the noise of the instrument that measures it"* (`s30/REPORT_S30.md` §1.1).

## 3. Provenance and process lessons

- *"Writing 'saved as X' is not saving as X, and the moment of greatest risk is immediately after articulating the lesson"* — `s30/BRIEF.md` was claimed saved at 12:35 and written at 13:52 (S30-L0 annotation). *"The fix is mechanical, not exhortative"*: `s30/s30_verify.py` should assert every path the ledger claims to have written.
- *"Check the job, not just the file"* — lane Y read `s30_P_chain_rows.jsonl` while the job was still writing it (S30-L28 #7; `s30/REPORT_S30.md` §7.4 #2).
- *"A verdict string is a claim about a computation and is worth exactly what reading the computation is worth"* (`s30/STATE.md` Note 5; S30-L5 found S29's printed verdict tested a different statistic than it named).
- Read the memory note's body, not its index line (S30-L7; S30-L10 §6; `s30/lit/L_INDEX.md`).
- Existence/precedent checks: three lane-L proposals *"that survived the information test died on an existence-or-precedent check"* (CAGEO already built; EDM projection prohibited by S19) (S30-L18 §1).
- Permanent roles: the adversary role *"was not rotated"*; *"a sprint that relied on distribution happening spontaneously got lucky"* (`s30/REPORT_S30.md` §2.3).
- *"A pre-registration that only ever confirms is decoration. Four of ten fired against the lane that wrote them"* (`s30/REPORT_S30.md` §2.2).
- Lane T: *"Both misses ran toward my own hypothesis"* — the `unstated-operators-align-with-your-hypothesis` pattern (`s30/THEORY.md` §10).
- The report is less careful than its ledger when summaries drop qualifiers the lane attached (`s30/AUDIT_V.md` verdict; `s30/AUDIT_Z.md` D11).
- Operational: the `jobrun.py` CPU_START = 85 vs governor CPU_CEILING = 101 gate *"bit exactly as predicted"* — shards launched detached (S30-L19 operational disclosure; `s30/REPORT_S30.md` §11.3).

## 4. Scientific lessons (as the sprint stated them)

- *"Fixing ten targets is worth more than improving all 126 by 0.20 Å"* — the mean is a tail statistic (S30-L0).
- *"An objective cannot be pointed at a target nothing can see"* (`s30/REPORT_S30.md` §5.1); same circuit 0.2516 Å (ORACLE objective) vs 3.4330 Å (deployed objective).
- *"The set-selection problem here is computationally easy and informationally expensive … no solver supplies information"* (`s30/lit/L30_3_set_selection_cvar.md` §2).
- *"Relax the set, do not search it harder"* (design lesson from Maehara/Wilder, not a transferred theorem) (S30-L8).
- *"Monotonicity, not submodularity, is what we fail first"* (S30-L8).
- *"Decorrelation is not the lever. Skill is."* (S30-L18 §4) — scoped to pool-space operators, *"the flat lever must not be quoted at the steep one"*.
- The five-instance realism law: *"Every realism-enforcement operator this project or the literature has measured improves realism and costs, or fails to help, accuracy"* — with row 5 (AMBER relax) the exception, explained by the ~2/n bonded fraction (S30-L18 §2; S30-L13).
- A published number that disagrees with a measured one *"is a constraint on the mechanism, not a reason to doubt either"* (`s30/REPORT_S30.md` §9.2).
- *"For an averaging terminal, spread is the raw material, not a defect"* (S30-L20).
- *"Wide space + averaging readout consumes the wrong statistic. Wide space + argmin needs ρ, which is closed. Narrow, uniformly-good space + averaging readout needs no ρ at all"* (S30-L10 §3).
- Admission condition for generative spaces: *"ADMIT G against P iff Δ(bias B) + 0.298·Δ(set best) < 0"* (S30-L20 §4).
- *"The combination ceiling is ρ₀/√s₁ — set by the Gram's RANK, with the field count cancelling exactly"*; *"The Gram is a one-line test to run before anyone builds a twenty-second field"* (`s30/THEORY.md` §9; `s30/STATE.md` Note 7).
- *"The subspace is free. The sign is the whole problem"*, refined to: *"What can be predicted is coherent and therefore harmful; what would help is incoherent and therefore unpredictable"* (S30-L25, S30-L27).
- Theorems must carry quantifiers: common mode non-identifiable *"from the pool, under model class M"*, not *"invisible to any method"* (S30-L7).

## 5. What the sprint said to do next (`s30/REPORT_S30.md` §11–§12)

- The one scientific question: *"Does an observable exist whose error is incoherent with the pool's common mode?"* — with the admission test `coh < 0.6931` (ORACLE, development-time) and price (ORACLE i.i.d. arms −0.126 Å at R² 0.16, −0.247 Å at R² 0.24, CA cloud, not deployable). Named gap: mutual information is *not* shown to be zero.
- *"If the next sprint has one place to spend bits, it is the readout"* (index bit 0.376 Å/bit vs prior-sign bit 0.0713/0.0652; flagged unregistered, currencies not exchangeable).
- Retest chiral functionals at 40+ residues (the emptiness is length-scoped, the theorem is not).
- E2's restraint constant needs a native-free selection rule before it is deployable.
- Discharge the filter-independent-tail check on the 128 → 512 register widening (S30-L28).
- What NOT to spend on (§12.5), closure kind named: theorem (T1 subset objectives through averaging readout; common-mode correction from pool; achiral single-structure channels G1), price (sparse weighted readouts; torsion encodings), measurement (field combination; quadric escape; generative spaces; single-structure recognition; filter width).
- Open defects: `core/pipeline.py:821` withdrawn +0.113 Å claim; unpinned projection seed; launch gate vs governor; no multiplicity register (§11.3).

---

## Importer notes (2026-09-26 — not from source)

Factual notes about the import only. No new scientific conclusions.

**Coverage**
- Read in full: all 28 tracked `.md` files in `s30/` (listed in `README.md` §6). Scripts (`.py`) were not read. 14 result JSONs were opened to confirm cited headline values; all values checked matched the source text (`s30_P_chain.json`, `s30_P_lr.json`, `s30_D_meter_DIS_{chain,ca}.json`, `s30_R_verdict.json`, `s30_G_disp2.json`, `s30_G_chiral.json`, `s30_F_stagegap.json`, `s30_Q_sparse.json`, `s30_Q_quadric.json`, `s30_Q_rankcheck.json`, `s30_T_transfer.json`, `s30_X_ensemble.json`, `s30_D_gram.json`).
- `docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` contain **no Sprint 30 passages** (searched for S30 / Sprint 30 / sprint-30 terms). `docs/CONDENSED_REPORT.md` is titled *"condensed record, Sprints 5-13"*; `docs/FINDINGS.md` was last committed 2026-09-14, before the S30 date (2026-09-20).
- `s30/results/s30_D_ladder_structs/` (the 126 `.npz` holding the 9-qubit circuit rungs, cited in `s30/QUANTUM_W.md` §12.1) is **not git-tracked** at the pinned commit; the aggregate means are available in the tracked `s30_D_meter_DIS_*.json`. S30-L3 states the s30 cache directories are gitignored.
- `s30/results/s30_T_bits.json` does not store the value-of-a-bit fit parameters (per `s30/AUDIT_V.md` "NOT RECOMPUTABLE"); lane V's refit differed in the third digit (a 1.3176 / γ 3.1917 / R² 0.998573 vs reported 1.3312 / 3.1636 / 0.998341).

**Contradictions within the source, recorded not resolved**
1. `s30/REPORT_S30.md` §6.1 still reads *"every lane did; three lanes' falsifiers then failed"* while §2.2 says four of ten fired; `s30/AUDIT_Z.md` D18 flagged this (and that lane L registered nothing). Not changed in the final report.
2. `s30/REPORT_S30.md` §6.3 still calls the `compare` sign trap *"latent"*; `s30/AUDIT_Z.md` D12 and `s30/STATE.md` Note 16 say it fired in lane P. Not changed.
3. Verifier count: `s30/REPORT_S30.md` §7.1 #17 and §7.3 still say 22/22 (22 matched); §10.1 and §13.2 say 36/36 (`s30/AUDIT_Z.md` D16).
4. `s30/REPORT_S30.md` §8 L2 still states the direction to the native is *"anti-aligned on FAIL18 (−0.2524)"*, although §4.3 withdraws the anti-alignment half (0.67× MDE; `s30/AUDIT_V.md` D5).
5. `s30/REPORT_S30.md` §8 L7 and §7.1 #41 still say E2 *"does not reach"* the tail / *"the wrong direction"*, while §A.7 says E2 stays out *"on SIZE, not on reach"* and that the FAIL18 difference is 0.22× MDE (`s30/AUDIT_V.md` D1).
6. `s30/REPORT_S30.md` §8 L7 still says the skill collapse is measured *"on all three tail definitions"*; §4.1 was softened after `s30/AUDIT_V.md` D4 (0.1066 vs 0.3798 / 0.3438; only FAIL18 has a CI).
7. `s30/REPORT_S30.md` §8 L4 still says *"48 bits for 4 basins/residue at n = 12"*; `s30/AUDIT_V.md` D11 says this wording computes to 24; ledger figure is 51.8 at k = 4, n = 12.96.
8. CHARTER ladder ρ on the built chain: S30-L3 and `s30/STATE.md` Note 10 give **−0.0921**; the tracked artefact `s30_D_meter_DIS_chain.json` and `s30/REPORT_S30.md` §10.2 give **−0.1964** (verified by importer). No source entry reconciles them.
9. Production built-chain value: five values circulate (3.2105, 3.2126, 3.2071, 3.2148, 3.2041) plus 3.2052 in `s16/results/repair_A.json` (`s30/AUDIT_V.md` D10); the report attributes the spread to the unpinned projection seed (§1.1).
10. Cross-kind confound count: `s30/STATE.md` Note 15(d) and `s30/SYNTHESIS_Y.md` §7.1 #46 say *"third"*; `s30/REPORT_S30.md` §A.7 and §7.1 #46 say *"Second"*.
11. `s30/SYNTHESIS_Y.md` §7.4 #2 and Appendix Y.1 #7 say lane P's chain run was unfinished (112/126, JSON missing); S30-L28 #7 and report §7.4 #2 say the run completed (126/126) and lane Y had read the file mid-write. The tracked `s30_P_chain.json` exists.
12. Retrieval: S30-L2 and `s30/STATE.md` Note 3 say *"Retrieval is exonerated at every stratum"*; the final report calls it NOT MEASURED, not exonerated (§4.1).
13. Stable ranks for the field Gram: 1.681 (S30-L21, n = 119) vs 1.705 (S30-L22, n = 126) vs 2.057 aggregate (S30-L28 #5).
14. Lane X's "FAIL18" in S30-L10 §5 is actually worst-18-by-endpoint (S30-L28 #3).
15. Minor numeric differences in derived bit figures: `s30/STATE.md` Note 4 says *"~31 effective bits … a 269-bit collapse"* and *"0.29 bits per torsion"*; `s30/THEORY.md` gives 24.3 bits (d_eff = 2), *"a 250-to-275-bit collapse"* and *"0.27 bits per torsion"*.
16. `s30/QUANTUM_W.md` §16 states report §0, §11–§13 are *"still [PENDING]"* — a snapshot at the time of writing; the final report has those sections.
17. `s30/LEDGER.md` line 1348: a numbering-collision notice (renumbering "S30-L3" → S30-L16) sits at the end of the S30-L11 body, immediately before the S30-L16 heading; its placement is ambiguous. S30-L18 §8 refers to lane D's radial entry as *"S30-L7 (D)"*, which is now S30-L22 after renumbering.

**Terminology**
- The source does not use "DEP"; the deployable/non-native label is "native-free" (and "DEPLOYABLE"/"NOT DEPLOYABLE" in capitals). The terms "tail collapse" and "solver-equivalence" do not appear in S30 source; the nearest source concepts are T1 (*"one classical sort reproduces it"*) and S28's `gate_set_equality`, recorded in `QUANTUM_RESULTS.md` Q2.
