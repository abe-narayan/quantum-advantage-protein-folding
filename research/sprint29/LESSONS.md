_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s29/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 29 — lessons the sprint itself recorded

All lessons below are attributed to their source; none is new.

## Scientific / methodological lessons

1. **"The next question is not 'which operator?' It is 'where does new information come from?'"** — `s29/REPORT_S29.md` §13. Every closure in S29 was of a *consumer* of existing information.
2. **A channel is necessary but not sufficient.** "Any new information reaches the endpoint only through the terminal operator, and that operator consumes the set *mean*, so it can spend at most 0.04 of any ranking … A sprint that produces a better channel and feeds it to the shipped average will measure approximately nothing" (REPORT §13; S29-L44 addendum 2).
3. **Aim at the tail, not the average.** "The mean is a tail statistic … it is a request to fix the targets the pipeline fails on" (REPORT §7.1, §13).
4. **Do not tune a single global scalar again.** "Four were measured; two have an ORACLE global optimum of *exactly zero* … 'Tune one number better' is not a strategy that this instrument can reward" (REPORT §13; S29-L47 §5). "The size of a rung's ORACLE gap measures how much PER-TARGET information it needs, not how much accuracy it offers" (`s29_O_FINDINGS.md` U1).
5. **Recompute in-sample corpus diagnostics out-of-fold first.** The distogram memorises training peptides by 8× (+2.075 nats, 4.88× MDE) (S29-L9; REPORT §13 "One cheap prerequisite").
6. **Keep the literature lane and give it "the first word rather than the last."** "Two of the three cheapest and most decisive results came from *not running anything*" (REPORT §13; §4.3).
7. **"A lower objective value is not success unless it produces a lower structural RMSD"** — measured directly by F1: "a better-ordering cost emits the same answer" (REPORT §4.7; S29-L51).
8. **"Spend control effort at the step where a wrong answer would first become quotable."** Lane M's generalisation: the three overreaches "did not differ in care; they differed in whether a cheap control existed at the decisive step" (REPORT §9.2b).
9. **No single meter number is sufficient.** "A single-number gate would have been gamed here; four numbers caught it" (contract addendum 5; S29-L37).
10. **Ladder ρ must name its ladder.** "The shipped cost orders the BULK correctly and anti-orders the near-native half"; charter rungs are "a weaker [test], not a stricter one" (S29-L2; STATE note 6).
11. **Ranking preference and gradient direction are different statements about the same cost** (lane D: "I had them fused") (`s29_D_FINDINGS.md`).
12. **Averaging distortion is a separation-dependent shear, not a contraction** — "the 22% contraction is the left-hand end of that curve, not a property of the operator" (S29-L24; STATE note 16).
13. **"The price falling is not the price being saved"** — a falling projection price can mean the cloud got worse (S29-L57; REPORT §11.3).
14. **"A null prior and a harm prediction are different claims"** — lane P is "not entitled to credit for the sharper later prediction by having written the vaguer earlier one" (S29-L57).
15. **Any number produced by rearranging an identity is an estimate that must be measured before it sets an expectation** (lane M, `s29_M_FINDINGS.md` item 5; S29-L53).
16. **Controls that are the identity by algebra** — spotting it in another's proposal "did not stop me committing it in my own code" (lane M, `s29_M_FINDINGS.md` item 6).
17. **Matched order-statistic nulls are decisive**: lane X "would have put a 0.8 A 'recombination is worth something' claim into the record" without the scrambled-chimera control (`s29_X_FINDINGS.md` §5 item 1).
18. **Small probes find structure that isn't there**: "Both readings found structure in a small sample" (REPORT §14(e); lane X R3 reading).
19. **Derive before measuring when the mechanism is constructive**: lane X "should have DERIVED" that a non-commuting mixer cannot break tail-is-a-prefix (`s29_X_FINDINGS.md` §5 item 2).
20. **Best-of-N at matched budget, never an initialisation mean** (REPORT §6.3, §9.3; project memory `concentration-is-wrong-when-discrimination-binds`).
21. **The Gaussian partial correlation is an upper bound on this instrument, not an estimate** (S29-L33; STATE "RECOGNITION IS NOW CLOSED THREE WAYS").
22. **A negative literature result is a finding**: no QA method below 40–50 residues (S29-L1); "the negative was worth more than the search would have been" (`s29_L_FINDINGS.md` §7).
23. **Physics/interpretation of prior records**: "A twenty-sprint-old number predicted a new arm's endpoint to a hundredth of an Ångström … The project's model of itself is accurate; it is the Ångströms that are not available" (REPORT §4.7).

## Provenance / process lessons

24. **"An artefact path in prose is a CLAIM, not a citation"**; run `git log --all -- <path>` during the reading; the risk concentrates on "the one item that survived a closure" (S29-L41, S29-L42; `s29_L_FINDINGS.md` §6).
25. **"A number in a ledger entry is a claim about a file, and it is worth exactly what recomputing it is worth"** (S29-L48).
26. **Chronology certified from git, not from anyone's word** (contract rule 27; S29-L28).
27. **Commit by pathspec, never by index** in a shared working tree (contract addendum 4; S29-L34).
28. **"A job name is not a lock"**; check `s26/jobs/<name>.json` and the live process list (lane M, `s29_M_FINDINGS.md`); "the invariant is one process per unit of *work*, not per name" (REPORT §3.3).
29. **`os.replace` is atomic and does not make a SHARED temp path safe** (lane X, S29-L56).
30. **"A rule that lives only in prose is not enforced by the thing that schedules the work"** (REPORT §3.3, AMBER concurrency); paired thresholds changed on one side only caused both the governor deadlock and the CPU_START throughput bug.
31. **"The axis that is undefined is the axis nobody wrote a test for"** (lane D, `s29_D_FINDINGS.md`).
32. **An unrun suite and a passing suite look identical in a report that does not say which it had** (REPORT §4.6).
33. **`ca_rmsd` has a Kabsch/SVD floor of 1.274e-07 Å on identical input**; "agrees to 1e-8" claims through it should be read as ~1.3e-7 (S29-L27).
34. **Finite differences on a piecewise-linear cost**: h = 0.01 Å straddles the 0.05 Å risk-grid knots; h = 1e-3 holds to 3e-4 (`s29_D_FINDINGS.md`).

## Pre-registration, brief and literature evidence

_Integrated 2026-09-26 from a second importer's reading of the preregs, briefs and lit notes (lessons as stated in those files)._

35. **Commit hygiene: explicit pathspec, never `git add` first** (`s29/PREREG_S29_B.md` addendum 3; mirrors contract addendum 4).
36. **A null can demonstrate constructively** that "the barrier is the information content of f, not the shape of the optimisation" (`PREREG_S29_B.md` addendum 3; realised in S29-L54).
37. **"Contraction and RMSD do not track across functionals"** (`s29/PREREG_S29_M_F1.md` probe) and **the averaging bound must price any change of m** (infinite pool 3.040 vs 3.0483).
38. **MAE does not price selected RMSD**, recorded as a "fourth independent direction" (`s29/PREREG_S29_M_F2.md` addendum 2) — fifth instance per S29-L53.
39. **"A job name is not a lock"** (`PREREG_S29_M_F2.md` addendum 3).
40. **Bits and Ångströms are never to be multiplied** through a mean-consuming readout (`PREREG_S29_M_F2.md` addendum 3).
41. **A per-target argmin is an incidental parameter and "may NOT" be written up as "headroom"**; a cleared falsifier would count as evidence against the bound (`s29/PREREG_S29_P.md` addenda 5–6).
42. **Best-of-N at matched budget, never a single untrained draw** — a single draw is a "FLATTERED control that must not be quoted" (`s29/PREREG_S29_X.md` addendum 3).
43. **Cite Barkoutsos eq (12)** rather than presenting the set-equality theorem as a discovery (`s29/lit/L_4_quantum.md`).
44. **Use CRPS, not MAE,** to compare posteriors (`s29/lit/L_3_decision_theory.md`).
45. **"The averaging route is closed by arithmetic"** (`s29/lit/L_2_correlated_error.md`).
46. **"Do not build a better in-band ranker"**; measure ρ(R, Rg) before banding, or a compactness-loaded band gives a "SELF-FULFILLING null" (`s29/lit/L_7_inband_training.md`).
47. **The per-target sign is an incidental parameter**; the sign regression is "a MECHANISM measurement only"; "S30's only plausible route to a materially better number is a better distance prior" (`s29/lit/L_8_conditioning.md`).
48. **The near-miss re-import** of the PEP-FOLD retrieval key: a FAIL18 diagnostic in one file and its chain closure in another invites re-proposal (`s29/lit/L_5_peptide_ceiling.md`; S29-L14).
49. **Leave erroneous paragraphs visible and annotate them** (`s29/lit/L_1_native_free_qa.md` correction per S29-L42).

## Importer notes (2026-09-26 — not from source)

- **Retractions index empty.** `s29/RETRACTIONS_S29.md` contains only "(none yet)", while `s29/REPORT_S29.md` §3.2/§14(e) records 18 withdrawn claims; all 18 are itemised in NEGATIVE_RESULTS.md §A from the report and ledger.
- **"39 fields" persists in the final report.** Corrected to 21 in REPORT §0 and S29-L48, but REPORT §9.2 ("used as the bar for all 39 displacement fields"), §11.2 ("39 fields, none beats the random reference") and §14(d) ("Any of 39 native-free displacement fields") still say 39. The artefact `s29/results/s29_D_fields.json` has 21 fields (checked).
- **Path-audit counts differ by section.** REPORT header/§4.6: 205 of 217 resolve; REPORT §8.6: "all 160 artefact paths"; S29-L46 heading "ALL 160 RESOLVE" is superseded by its own addendum (205/217, 1 genuinely dangling `s7/debias_tune.json`, cited in S29-L51).
- **Production anchor values.** 3.2126 Å (S27 stored rows; contract, DATAPATH, lane P, lane M F1) vs 3.2105 Å (re-projected in S29 jobs; report). Source attributes the difference to the projection branch-flip floor.
- **Report line count.** STATE/STATUS say REPORT_S29.md was 1,581 lines at first close; the pinned file has 1,620 lines (lane P's §9.2c integration added after first close).
- **STATE comparison count stale.** `s29/STATE.md` "Comparison count (multiplicity)" still reads "0 endpoint comparisons run", although later entries record endpoint comparisons (e.g. S29-L51: 7; S29-L57: 5).
- **THEORY_SUMMARY vs addendum 5.** `s29/THEORY_SUMMARY.md` §2 table still states the shrink warning "stands … a positive cosine is purchasable with zero information by shrinking", which S29-L37 and contract addendum 5 refuted on this instrument. Similarly S29-L23's text still says the sign formula "was derived before those numbers were read" (refuted by S29-L28; left standing per append-only discipline).
- **Best-of-N figures.** REPORT §6.3's triple (+0.0095 / +0.0279 / −0.0536) could not be located verbatim in `s29/results/s29_X_bestofn_fmt.txt`, whose per-readout chain values differ (e.g. R1 +0.0063 / +0.0210 / −0.0293); the −0.0088 (0.07×) R2 figure does match. Not resolved.
- **lane X test count.** `s29_X_FINDINGS.md` says `tests/test_s29_X.py` has 16 tests (§1) and 19 (§4 artefacts); STATUS says 12, then 14.
- **"Thirteen controls" in REPORT §6.4** lists 12 items inline; `s29_X_FINDINGS.md` table lists 13 rows (two BESTOFN rows).
- **Lane P "no closing entry"** at first close (STATE/STATUS/REPORT) was later filled by S29-L57 (09:13); both states are recorded in source.
- **docs/FINDINGS.md and docs/CONDENSED_REPORT.md** contain no Sprint 29 passages (grep for "S29"/"Sprint 29" returned nothing; CONDENSED_REPORT covers Sprints 5–13). `docs/FINDINGS.md` section B (≈ lines 6105–6310) is the S8 free-energy prose that S29-L41 found has no code or artefacts behind it.
- **Values checked against artefacts:** 2.9027/3.2105/−0.3079/3.14× (`s29_O_headline_contrasts.json`); 21 fields, best CHAN_DISTPOT 0.11280, random ref 0.13983 (`s29_D_fields.json`); F1 means and contrasts (`s29_M_F1_summary.json`); M6 chain −0.00817/−0.266× (`s29_D_m6_chain_seed0.json`); lane P arm means and max-over-K 3.517, p 0.0 (`s29_P_summary.json`); F2 supply correlations 0.3129/0.3660 and gate PROD/ORACLE values (`s29_M_F2_supply.json`, `s29_M_F2_gate.json`); compactness in-band medians 0.0747 vs 0.4115 (`s29_T_compactness.json`); X P1 +0.4572/1.18× (`s29_X_probe.json`). All matched the source prose.
- **(a) Projection price, +0.159 vs +0.164 Å.** `s29/PREREG_S29_P.md` (lines 13, 73, 204), `s29/briefs/S29P.md` and STATE "Wave-2 candidate probes" P1 say +0.159 Å (3.0483 → 3.2126); `s29/lit/L_3_decision_theory.md` (lines 108, 224), S29-L12, S29-L22 and `s29_P_FINDINGS.md` P6 say +0.1643/+0.164 Å (3.2126 − 3.0483 = 0.1643); `s29/DATAPATH.md` stage 11 says +0.1664 (citing `ARCHITECTURE.md`); REPORT §7 says +0.1622 on the re-projected 3.2105. Not reconciled in source.
- **(b) PREREG_S29_B addendum-1 timestamp.** The file header says "Registered 2026-09-20 00:10 Pacific"; Addendum 1 is headed "2026-09-20 00:09 Pacific" and says S29-L11 "pre-dates my commit on the clock, so I claim independence of **reasoning**, not of clock". Git (read-only `git log`): base prereg commit `1c345f07` at 00:07:37, addendum 1 `9d745692` at 00:09:09, addendum 2 `d3ccf6b6` at 00:32:10, addendum 3 `c89e3106` at 01:28:23 (the file text says A3 01:20). So the stated 00:10 header is later than both commits; the commit order (base before A1) is consistent. Recorded, not resolved.
- **(c) S8 free-energy stage missing.** Confirmed in my sources: S29-L41 (lane T) and S29-L42 (lane L) report all seven `s8/relax*` paths absent from disk and from all git history; only prose in `docs/FINDINGS.md` section B (≈ lines 6105–6310) survives. Also referenced by `PREREG_S29_T.md` and REPORT §12.4 ("a lane-week rebuild from a prose spec").
- **No prereg records its own outcome.** Status for each was assigned from LEDGER/FINDINGS (README "Pre-registrations" table).
- **lit/L_INDEX quirks (reported by the second importer, not independently checked):** T3 lists 6 entries but tallies 5 KEPT + 2 REJECTED; a stray duplicate "Topic 5 … (pending)" header; ANDIS cited as Bioinformatics 35:1499 in L_INDEX vs "Bioinformatics 2019" in L_6.
- **Original repo location.** The contract names `C:\Users\abena\Protein-Folding-Algorithm` (branch `s26`); this import is from the `cvar-vqe-protein-folding-v3` copy at the pinned commit.
