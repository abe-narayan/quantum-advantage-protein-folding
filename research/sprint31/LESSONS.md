_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s31/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 31: lessons the sprint recorded

Every lesson below is attributed to the S31 document that states it. Phrases in quotation marks are verbatim.

## A. Rules the sprint says it earned (`s31/REPORT_S31.md` Appendix A.3)

1. "A claim combining two lanes' numbers needs a named owner who holds both, and must carry both caveats in the sentence carrying the number." The stated reason: "a single-lane claim is audited by the lane that owns the data and a cross-lane claim is audited by nobody." The same rule is in STATE NOTE 13 and LEDGER S31-L16 (lane L), where it was "saved to memory".
2. "Every lever comparison carries its information cost in the same sentence as its Ångströms." Also in REPORT §10.1 and STATE NOTE 13(1), which cites S30 §9.4 as the precedent.
3. "A bar imported from another sprint must be checked against the object it graded there." The case was the `0.6931` bar, which "crossed from corrector-space into readout-space with no owner holding both, and reached shipped code in two lanes."
4. "A fold CI excluding zero does not rescue a sub-MDE effect". This happened twice, at 0.44× (B4) and 0.42× (widening). REPORT §15 describes it as "the documented sibling of the underpowered bug (`s24/stats_lib.py:145`)".
5. "A null in the mean is not 'no effect': report the per-target distribution against a matched implementation-noise null." The case was P1: its per-target spread is 10.7× the A2 null.
6. "An optimistically biased upper bound is still a valid upper bound. Order-statistic inflation deflates a *lead*, not a *ceiling*." Also in S31-L12 and LIT_L L3.1.

## B. The adversary's lessons (`s31/AUDIT_V.md`)

- "A number carries its definition, not just its value. Re-read the definition at the source before re-using it across a sprint boundary — and check that the formula you write beside it is the one that produces it." REPORT §0.4 adopts this as "**A number carries its definition, not just its value.**"
- The pattern across all nine defects: "a quantity **transplanted across a boundary its definition does not cross**". The boundaries named are an object, a search size, a basis, a data regime, a moment, Jensen, and provenance.
- "An audit that checks for an absent label cannot catch a wrong label." The verifier passed 97/97 on "is a basis named?" while the headline carried a misnamed basis. The recommended fix, which was implemented: "assert each number against the value on the basis it names" and ship a self-test on the defect that motivated it.
- "A check that cannot fire is indistinguishable from a check that passed." This comes from V-SELF error 3, where the auditor's own regression guard silently skipped a file. The fix: "'could not read' must never render as 'clean'".
- D5: lanes should "stage explicit paths" instead of `git add -A`. Pre-registration evidence depends on commit history saying "which lane registered what and when".
- D9: "the verifier must read the artefact's key list before asserting a path". The source records this as the seventh instance of contract rule 14 ("prose is not evidence of code").
- D10: "A partial-rows reading is not a result, and the sign is exactly what a partial reading gets wrong." AUDIT_V also records that lane F's "no mean until 126/126" discipline "is what contained it".

## C. Statistical and instrument lessons

- **Projection reproducibility (lane D, S31-L6, STATE standing rules):**
  - "Reprojection is reproducible only from bit-identical input clouds. Both sides of any built-chain contrast must be projected in the same job from the same stored clouds."
  - Refined in S31-L22 / REPORT §20.1: "identical clouds give identical chains to the last bit, and the check costs one line". Also: "The projection is deterministic; what lane D measured is sensitivity to *differing* inputs, not nondeterminism."
- **Mean floor vs per-target floor (lane P, S31-L18):** "The 0.0107 A figure … has been quoted throughout this sprint as though it bounded per-target chain statements, and it does not." The per-target floor is about 0.03 Å at p90 with a 0.23 Å tail. "Any per-target chain statement below ~0.03 A is indistinguishable from re-running the same computation in a different implementation."
- **Cloud→chain is locally chaotic (lane D, S31-L6):** "the measured 0.92 cloud→chain transfer is an average over a map that is locally chaotic on a substantial minority of targets". Lane F added a licence for the `m` axis only (S31-L23): "the cloud→chain price is flat across prefixes… That is a licence for the `m` axis specifically and nowhere else".
- **Matched thresholds (lane B, S31-L10):** "A registered threshold set at an absolute value, on a quantity only a matched control can read, is a mis-set threshold, not a falsification."
- **Pre-registration (REPORT §15; contract rule 19):** "A pre-registration that only ever confirms is decoration." Six of ten registered predictions went against their authors.
- **Controls that can hurt their own lane (REPORT §13):** the shuffled-`B` and rotation controls "changed a lane's own conclusion rather than confirming it… Both were run by the lane that stood to lose from them."
- **Strata defined by the outcome (lane F, S31-L21 §8(b)):** "The effect size rises monotonically with how circular the stratum is… That gradient *is* the signature of the stratum's definition doing the work".
- **Order statistics (lane F, S31-L11; lane V V1):** "A quantity that keeps growing with K and has not begun to flatten at K = 128 is a best-of-K, not a ceiling." V1 adds that it is the same law with the operator reversed: decorrelating a family grows its minimum and contracting one shrinks it.
- **Search size must be matched (lane V D1):** comparing a minimum over 8,128 supports with one over 128 is "a 64× oracle-search mismatch".
- **Constructing operators (lane F, S31-L21 §7b):** "The rule for any future arm that CONSTRUCTS rather than SELECTS: carry the geometry secondaries from its first row, and check `achieved` — does the operator do the thing it is named for — before reading its endpoint."
- **Synthetic checks (lane V D6):** a synthetic check fed tie-free random floats "was structurally incapable of testing its own caveat". REPORT §5.1 says "My check was structurally incapable of testing its own caveat."
- **Moments (lane V D7):** "`d_obs² = d_true² + r²` is an identity **in squares**" and must be applied with second moments. Deltas are protected because "both arms share the same reference on the same target", which gives "attenuation, not cancellation".

## D. Scientific and methodological lessons

- **Classical reducibility (THEORY_A §5; charter §11):** "Classically reducible is not the same as useless." A1's closed form "is a strict improvement over the shipped solver", but no such construction "should ever be described as quantum."
- **Information sources vs ceilings (lane L, S31-L12, STATE NOTE 12):** "'Not a source' does not mean 'not a constraint.'" Enumerating sources is closed, but "the bound is vacuous and cannot limit accuracy… The open moves are a better estimator or a better library. A measurement of the molecule is *one* escape, not the only one."
- **Quality estimates (lane A, S31-L19):** "The binding axis is in-band ρ, not global ρ". Global ρ is "necessary-not-sufficient".
- **Readout identity (lane A, S31-L13):** "The readout question and the ranking question are the same problem". Also: "Sparsity is an *output* of the correct objective, not a design choice".
- **Averaging distortion (lane F, S31-L21):** "the distortion is a SYMPTOM of averaging, not the MECHANISM of its error". The source also records a correction: comparing the average with the native instead of with its members produced an artefactual "crossing" near s = 8.
- **Where the prize is (REPORT §20.1, §21):** "A future common-mode channel does not have to be accurate — it has to point the right way." Three quarters of a perfect correction buys 97% of its benefit. REPORT §21 qualifies the ask: "'supply the common mode' is not a clever projection… it is a request for most of a perfect prior".
- **Search vs discrimination (lane D, S31-L8):** "SEARCH IS NOT THE BARRIER; DISCRIMINATION IS."
- **Cheap nulls (lane L, S31-L9):** "Stopping at 'the reference is uncertain by 1.08 Å' would have been quotable, alarming and wrong… the cheap null sits exactly where the wrong answer would first have become quotable."

## E. Engineering lessons (lane D, S31-L7)

- "Recording a defect in a table is not fixing it". The withdrawn +0.113 Å claim had sat in shipped code for four or more sprints.
- Paired thresholds should be imported rather than duplicated. `jobrun.py` v3 derives its launch gate from `governor.py`, "the first fix that makes the next one impossible rather than merely unlikely."
- "Stop launching detached". Detached jobs are invisible to the governor.
- The verifier should parse documents for every path they name "rather than using a hand-kept list — because a hand-kept list is exactly what fails."

## F. Recommendations the sprint carried forward (REPORT §21)

- The next question: "Find a source of information about the POOL'S COMMON MODE … that does not come from the pool." It runs in parallel with the requirement for "a per-candidate quality estimate with positive in-band skill". The report asks every proposal to "State which of the two any proposal addresses." Whether the two are one requirement or two "is stated as open rather than resolved by assertion" (§20.3).
- Do not spend on "Any further readout, index, ansatz, optimiser, α-schedule or register-width work". Do not spend on "A deployable 128 → 512 widening", or on "Chiral single-structure functionals at 9–16 residues". The last is worth retesting at 40+ residues because "The theorem is length-free and only the emptiness is length-dependent".
- B4 should be adopted only "deliberately at a sprint boundary as a *conditioning change*, never as an improvement". It moves canonical 3.2105 to 3.2050.
- "S32 should price the widening on its own, pre-registered" (STATE NOTE 14).
- The ORACLE 0.0938 Å over the eight projection branches is "a real S32 lead", with the "honest prior … that nothing native-free will order them better than the objective" (STATE NOTE 9).

---

## Importer notes (2026-09-26 — not from source)

These are factual notes about the import only. They are not scientific conclusions.

1. **`docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` contain no Sprint 31 passages.** A grep for `S31`, `Sprint 31` and `sprint31` returned nothing relevant. `git log` shows both files last changed 2026-09-14, before S31 opened on 2026-09-20. Nothing was imported from them.
2. **`s31/report_page.html`** is a template, 24,469 bytes. `s31/build_report_page.py` injects REPORT_S31.md into its `<!--REPORT_MD-->` placeholder for client-side rendering. I skimmed its static text. The only content beyond REPORT_S31.md is a summary banner and a verdict legend:
   - The banner reads "Arms deployed 0 — Thirteen were measured end to end" and "Directions closed 13 routes".
   - The legend phrases "Below 0.7× MDE" as "Falsified / worse". The contract phrases it as "not a result".
   - I did not otherwise use it as a source.
3. **Contradiction: ORACLE convex readout ceiling (CA cloud).**
   - Lane A reports 1.8290 Å (`s31/THEORY_A.md` §7.3, §10.5; S31-L13; S31-L19; `s31/results/s31_A_readout.json` confirms 1.82904).
   - Lane C reports 1.8008 Å, corrected to 1.7977 Å (S31-L14 CORRECTION 1; `s31/results/s31_C_ladder.json` confirms 1.79771).
   - REPORT §20.2 quotes "Lane A's closing statement" using 1.7977. Lane A's own text says 1.829.
   - The two are different constructions: lane A uses a medoid-of-128 frame QP, and lane C uses best-of-hull/FISTA/vertex with an asserted vertex bound. The source does not reconcile them explicitly.
4. **Contradiction: sd of H(p\*) at α = 1.**
   - S31-L17 and REPORT §0.1 / the §5.1 box say sd 1.4e-4, with H = 4.9136.
   - S31-L20 §5 and the REPORT §5.1 prose say sd 3.1e-4, with H = 4.9137.
   - Both appear in REPORT_S31.md.
5. **Contradiction: deployed `iters`.** PREREG_S31_P §3 and PREREG_S31_A §1 give iters = 50 (`Config.vqe_iters=50`). LIT_L L1.1 describes the "deployed settings" as iters 80. Lane L's verification cells also ran at T = 0.1/0.05, not the deployed T = 0.3; the source itself later records this (S31-L17, S31-L20).
6. **Lane count.** STATE.md says "Eight lanes, the charter's maximum". REPORT §0.4 says "Nine lanes". Nine lane letters appear: A, B, C, D, E, F, L, P, V.
7. **Verifier counts differ inside REPORT_S31.md.** The header says 271 matched, §15 says "129 numbers" and §17 says "136 checks". These appear to be progress snapshots that were not updated. STATE and LEDGER record 82 / 87 / 97 / 129 / 230 / 270 / 271 at different times.
8. **Multiplicity register numbering.** Lane E's late rows are numbered 7, 8, 9, which collide with earlier rows 7–9 (lanes D and B) and were not renumbered. The final total, "k = 759 … DERIVED BY SUMMING ALL 24 ROWS", is recorded as stated. I did not re-sum it.
9. **Attribution mismatch.** REPORT Appendix A.2 lists the withdrawal of "*must never again be quoted as the architectural ceiling*" under lane C. In the ledger the sentence is lane F's, withdrawn by lane F (S31-L11 §5b(ii)).
10. **The "energy along mu" share has several values**, each defined differently in the source:
    - 54.70% per-target mean and 71.10% pooled (S31-L3; S31-L22);
    - "84% of y's energy (rms 3.12 of 3.70)" (S31-L22 appended section; REPORT §20.1);
    - "mu captures 71%" of y's norm (S31-L22 control 6).
    None is reconciled here.
11. **λ=0 branch margin.** STATE NOTE 4 says "median lam=0 branch margin ~4e-8". PREREG_S31_D_branch says "~7e-7" over the targets scored so far. S31-L6 / REPORT §1.2 give the final 3.1e-7 over 126, which `s31/results/s31_D_projection_pin.json` confirms (3.108e-7).
12. **"Circuit strictly worse" counts.** REPORT §7 gives "36/36 targets" and §0.1 / §14.3 give "126/126". This looks like an interim count left in §7.
13. **Verification scope of this import.** I checked headline values by searching keys in the result JSONs listed in README.md, and all cited values were found. I did not open `.py` files beyond `s31/build_report_page.py`. I did not re-derive × MDE ratios; they are copied as recorded.
14. **Leakage labels.** Leakage status follows the source's ORACLE / NOT DEPLOYABLE, native-free and ORACLE-ADJACENT labels. Where the source leaves a number unlabelled, the item's section context is the only guide; no item was relabelled.
