_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s32/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 32: lessons the sprint recorded

Everything above the "Importer notes" section is the sprint's own wording or a close paraphrase, attributed to its file.

## 1. Methodology rules the sprint paid for ("Appendix C — methodology this sprint had to learn")

`s32/REPORT_S32.md` Appendix C says "Six rules were added to the contract mid-sprint, each paid for by a defect."

1. **`split_half_transfer` needs production as the baseline.** The function "centres on the grid's **column mean**, not the incumbent". On a grid with one implausible column it read "−0.0254 with a CI excluding zero". Against production it read "+0.0004, CI [−0.0091, +0.0116]". Codified as contract rule 23: "the baseline must be the incumbent, not the grid mean" (`s32/S32_CONTRACT.md`).
2. **"Bit-identity, not value-identity, licenses a cross-job chain comparison."** A one-ULP (7.1e-15 Å) change moves the built chain 0.10–0.15 Å. The irreducible sd on an unpaired chain mean is ±0.003 Å. "nothing else below ~0.03 Å is resolvable." "a *reduction* over 126 float64s is not exact either" (contract rule 20).
   - **2b.** "Does a script write this file?" is not enough: "***a `.py` writes this name AND the quoted number is a numeric leaf inside it.***" Two lane-D artefacts cited numbers that "existed **only in stdout**" (`s32/REPORT_S32.md` App. C 2b; `s32/MULTIPLICITY.md` AUDIT 11).
3. **"An audit that cannot fail is decoration; an audit whose scope shrinks silently is worse."** Examples:
   - A convexity check "initialised its accumulator at the pass threshold".
   - A global string replace "narrowed the path audit from 71 paths to 35".
   - Both now carry positive controls.
4. **Retractions in place versus phrase-matching audits.** "a struck claim is exempt **only if its replacement is stated in the same block**", with a laundering self-test (`s32/LEDGER.md` S32-L12).
5. **"A job name is not a lock, and killing a wrapper does not kill its child."** "Check the pid, not the name". Assert "**both** `len(rows) == 126` **and** `len(set(pdbs)) == 126`".
6. **"Staging is not lane-isolated."** "Write and commit in one call, and **verify the edit is in `HEAD`, not just on disk**" (contract rule 24).

## 2. The recurring defect shape

- "**Every one is the same shape as S31's: a number re-used across a boundary its definition does not cross** — a basis, an object, a moment, a stratum, a direction, a baseline, a job" (`s32/REPORT_S32.md` Appendix A; `s32/S32_CONTRACT.md` rule 4).
- "What is different this sprint is that **most were caught by machine rather than by memory**… each new audit was built from the defect that motivated it" (`s32/REPORT_S32.md` §0.6).
- "S31's finding was that the coordinator's own claims are the ones no lane audits. This is the first S32 instance" (`s32/LEDGER.md` S32-L2). The report adds: "The coordinator wrote the largest share" (Appendix A).

## 3. Scientific lessons the sprint stated

- **Do not call a pool "containing the answer" when a pool assembled for a different protein contains it equally well.** "***The ORACLE top rung and the deployed pipeline consume different properties of the pool, and only the second is retrieval-sensitive.***" (`s32/REPORT_S32.md` §2.0)
- **The FAIL18 prefix class.** "*any comparison of the score's prefix against an alternative prefix, scored on the BEST MEMBER, is entirely FAIL18*". This is registered as "a general property of the instrument, not three coincidences". AUDIT 4 flags "any aggregate whose FAIL18 and non-FAIL18 strata have opposite signs" (`s32/REPORT_S32.md` §0.6, App. B; `s32/MULTIPLICITY.md` D3).
- **Median vs mean is "the project's free early warning", and it fired.** Mean +0.187 against median −0.038 (`s32/LEDGER.md` S32-L3 annotation). The ε = 4.0 hull arm had mean/median 1.85 (`s32/THEORY_Q.md`).
- **Charter §29's trap, confirmed at the endpoint.** "A filter can retain a *worse best member* than random and still produce a *better prediction*, because production averages 75 candidates" (`s32/REPORT_S32.md` §2.2).
- **Asymmetry, seen three times.** The score prefix, consensus and the branch criteria "all have **real skill at identifying the worst candidate and none at identifying a better one than the incumbent already picks**" (`s32/STATE.md` NOTE 3). "Native-free observables have real skill at avoiding disasters and none at finding winners" (`s32/REPORT_S32.md` §5.5).
- **Compute-matched controls can remove an apparent effect.** On GEN4-only "nothing is a result in either direction". "The large ARGMAX effects are a property of having ~200 branches to find a bad one among, not of the criteria" (`s32/REPORT_S32.md` §5.5).
- **Test both directions for a criterion with no a priori sign.** "testing one direction is an **unregistered choice that halves the apparent multiplicity**" (`s32/MULTIPLICITY.md` D7).
- **The null must match the claim.** `nullPERM` "cannot test the claim being made". The cross-target null is "the null the claim needs". A NOISE self-test proves "the audit can fail" (`s32/LEDGER.md` S32-L12; `s32/MULTIPLICITY.md` D4).
- **Report the marginal before an accuracy.** "if the bit is 70/30, a 70%-accurate classifier is nothing." "A one-bit feature that is 81/19 cannot carry a 59/41 label" (`s32/MULTIPLICITY.md` D4-M, D4-X).
- **Controls must match the operator's own space** (contract rule 6). The hull-vs-shrinkage control is matched "to the projection's own displacement" (`s32/LEDGER.md` S32-L(Q2)). The magnitude-matched random direction is used for D3-M (`s32/PREREG_S32_D.md`).
- **`cos` is an interpretation, not corroboration.** "***Any sentence quoting the price AND the cos as two pieces of support is double-counting one measurement.***" (`s32/S32_CONTRACT.md` rule 16)
- **Name the G1 hypothesis before building an observable.** D0 "closed more than it opened". "*Physics is closed as a ranker and open as a mover*". "What doors 2–4 escape is the *function class*, not the information" (`s32/PREREG_S32_D.md`).
- **"Noise is not information"** (Corollary D-E1). "Stochasticity is not an escape" (`s32/REPORT_S32.md` §8).
- **"A real, transferable, completely redundant signal is a sharper negative than a null."** (GEN4D, `s32/LEDGER.md` S32-L(R4))
- **Price in the right currency.** "A bit count prices a selection alphabet; this decision is continuous, so the two are never differenced" (`s32/THEORY_Q.md` Q4).
- **A theorem can be stronger than the empirical conclusion.** "gain exactly 1 means no noise suppression" was struck. "Charter §4 names *'a theorem was stronger than the empirical conclusion'* as an S31 failure mode; this was one" (`s32/STATE.md` NOTE 2).
- **Obstructions belong to a register, not to CVaR-VQE.** "The closure moved from 'a circuit cannot be built' to 'a circuit can be built and there is nothing for it to compute'" (`s32/THEORY_Q.md` Q3).
- **Cross-lane synthesis must be re-derived by one person in one script.** The chirality/filter synthesis "did not survive". "Every cross-lane synthesis in S31 failed, four for four" (`s32/LEDGER.md` S32-L7, S32-L(D2)(d)).
- **Solver certificates catch what smoke tests miss.** "The smoke did not catch it; the certificate did, and the certificate existed only because it was written as a returned value rather than as an assertion nobody reads." (`s32/LEDGER.md` S32-L(Q1))
- **Leakage filters need their own null.** The identity filter "rejects 100% of REAL and 100% of SHUFFLED". "The correction was made on a null measurement, with no RMSD computed" (`s32/LEDGER.md` S32-L(L1-L4)).
- **Do not silently back-apply a code fix to an artefact.** "a silent edit would have made artefact and code merely *look* consistent" (`s32/LEDGER.md` S32-L(L1-L4)).
- **Store the charter verbatim and read it back.** "*A charter that exists only in a summary is not a specification.*" (`s32/LEDGER.md` S32-L0)

## 4. What the sprint told S33 not to reopen (`s32/REPORT_S32.md` §10 item 4)

"**Do not re-open**":

- the prefix length `m`;
- scalar dilation in any calibration;
- branch selection by any of the sixteen criteria;
- force fields as rankers or movers;
- the per-target sign as a route;
- ensemble/dynamics scalars (theorem D-E).

Standing S33 priorities (§10):

1. Run the donor-pool control on `long40` first, and retrain the distance prior (`MAXLEN = 26`).
2. "Weight toward the set best" (untested).
3. "Stop looking for native-free in-band skill as posed."

The library admission gate (`REBUILD_TOL`) is flagged but "Not acted on, because changing library admission would change `tuning126`'s pools" (§7.5).

---

## Importer notes (2026-09-26 — not from source)

Factual notes about the import only. No findings are resolved here.

**Coverage**
- All 13 tracked `.md` files in `s32/` were read in full. `s32/report_page.html` was skimmed: it renders `REPORT_S32.md` client-side and adds only a masthead, a legend and a footer.
- 13 result JSONs were opened to confirm headline numbers (listed in README.md). All matched the quoted values to the stated precision.
- `s32/s32_verify.py` and the lane verifiers were not run. No `.py` was executed.
- **`docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` contain no Sprint 32 passages.** A grep for "S32", "sprint 32", "long40", "donor" and "hull floor" found no S32 material. `git log` shows both last changed 2026-09-14, while the S32 documents are dated 2026-09-21.

**Contradictions and inconsistencies found across the source (recorded, not resolved)**
1. **Verifier counts differ.**
   - `REPORT_S32.md` header: "143 recomputed, 0 mismatched, 0 flagged, 18/18 self-tests across eleven audits".
   - REPORT §0.6: "grew from 58 checks to 134 with 18 self-tests".
   - `STATE.md` NOTE 3: "58 → 138 checks".
   - `report_page.html`: masthead "143 / 0", footer "138 recomputed".
   - Interim ledger states: 58 (S32-L6), 64 (S32-L8), 97 (S32-L12).
2. **Defect count differs.** REPORT §0.6 says "Eleven defects". REPORT Appendix A and `STATE.md` NOTE 3 say "Sixteen defects".
3. **Branch selection figures differ across sentences in REPORT §5.5.** The section contains two adjacent blockquotes:
   - "worth **0.0001 Å** over a coin… **96%**" (lane R, 5 random draws, 3.2106);
   - "worth 0.005 A over picking a branch with a coin… **95%**" (lane V, 300 draws). `MULTIPLICITY.md` gives "+0.0049 ± 0.0079". The artefact `s32_V_R_adversary.json` records vs_prod 0.00405, draw_sd 0.00758.
   - The ORACLE best-branch ceiling appears as −0.1165 (3.43×, lane R), "−0.11" and "5%" (MULTIPLICITY lane V), −0.1072 (2.93×, "3%"; MULTIPLICITY running totals) and −0.1178 ("3.3%"; REPORT App. B).
4. **Out-of-sample criterion-search value is quoted three ways:**
   - +0.0004 CI [−0.0091, +0.0116] (contract rule 23; App. C; MULTIPLICITY D6);
   - +0.0026 CI [−0.0067, +0.0141] (REPORT §5.5, App. B);
   - +0.0028 CI [−0.0054, +0.0128] (MULTIPLICITY after doubling to 64).
   - REPORT §9.2 says "search-adj +0.0028".
   - The best single arm is quoted as 0.57× (REPORT), 0.51× (MULTIPLICITY) and 0.61× (lane R's 29-arm P3.4).
5. **`rama_nlp` argmin is quoted three ways:** −0.0037 at 0.20× (REPORT §5.5 table); "0.0031 at 0.16×" (REPORT §8 table and §9.2). The lane V artefact records effect_over_mde 0.196 for `ALL|rama_nlp|min`.
6. **Sparse vs production off-manifold distance.** REPORT Appendix A says "0.8503 vs 0.8150". Ledger S32-L(R1) at n=126 gives sparse s=10 `d` 0.7023 vs production 0.8150, and bestm 0.8505. The n=16 interim (S32-L9) gave 0.844 vs 0.705. At n=126 the sparse object is not farther off-manifold than production. The Appendix A figure appears to be the `bestm` row.
7. **The operator law ratio is basis-dependent:** 2.85 on the built chain (P-47) and 2.07 on the cloud (P-30). REPORT quotes 2.85.
8. **Per-target sign ceiling values change between versions.** S32-L12 (non-dedup, lane V) gives best Hamiltonian 0.2263 and Rg 0.3316/0.3323. The superseding dedup v2 gives LEG_total 0.2180 and RG 0.3228. REPORT and STATE use the v2 values. The superseded `s32_D1_signtransfer.json` is retained and annotated.
9. **LFO prefix-m verdict.** `LEDGER.md` S32-L1 quotes "+0.0075, 0.22× MDE". Other files give only "+0.0075, 63W/63L".
10. **REPORT §9.3 still cites "−2.58 Å on the long one"** as evidence for averaging, although REPORT §7.2 calls the same −2.58 vs −1.16 comparison "arithmetically right and misleading twice".
11. **`common-mode` alignment by-product:** D3-M interim (n=72) gives cos(e_prod, e_pool75) = +0.9519. The final (n=126) value is +0.9443.
12. **"ten pre-registrations"** (REPORT App. B). Only five `PREREG_S32_*.md` files are tracked. Other registrations appear to be inline in ledger/MULTIPLICITY entries, but the source does not enumerate ten.
13. **`MULTIPLICITY.md` "Emitted comparisons" table** still shows the "*(none yet)*" placeholder. Actual rows are in the per-lane sections.
14. **`STATE.md` NOTE 3 "Outstanding"** lists "five lane D artefacts with no producing script… and lane L's close-out". Both are later recorded as resolved: AUDIT 11 re-emission in MULTIPLICITY, and S32-L(L1-L4) in the LEDGER. `STATE.md` was not updated after that.
15. **`report_page.html` legend** labels "Below 0.7× MDE" as "Falsified / worse". The contract calls this band "NOT A RESULT".
16. **REPORT section order:** §2.3 precedes §2.2, and §5.5 precedes §5.4. Content is intact.
17. **Contract rule 3's per-target floor** (max 0.2285) was exceeded by the lane P reproduction (max 0.5174 on 2LNG; P-48). The contract text was not amended in the file read.

**Gaps**
- Qubit count as a number, circuit depth, shots, hardware or simulator, and quantum wall time are not recorded for S32. No circuit was run (see QUANTUM_RESULTS.md).
- The source contains no answer to lane Q's per-residue vs global branch-difference diagnostic handed to lane R.
- The `long40` donor-pool control and any quantum arm at length were not run.
- The source uses "deployable" / "native-free" rather than "DEP". The mapping is recorded in the README glossary.
