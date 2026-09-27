_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s32/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 32 (S32): "Where the RMSD is lost, and what it would take to get it back"

## Source pin

- Repository: `C:\Users\abena\cvar-vqe-protein-folding-v3` (GitHub `abe-narayan/cvar-vqe-protein-folding-v3`), commit `3d5b2d25b718346401268634da275f4d7e9fcf3f`, read-only.
- Sprint directory: `s32/` (183 tracked files: 13 `.md`, 1 `.html`, 1 page-builder `.py`, 80 analysis/verification `.py`, and 88 result artefacts under `s32/results/`).
- The sprint ran on branch `s26`. The charter was captured "on branch `s26` at commit `373d9176`" (`s32/BRIEF.md` provenance header; `s32/LEDGER.md` S32-L0).
- Report status line: "FINAL — 2026-09-21 11:38. All six lanes closed" (`s32/REPORT_S32.md` header).
- Published page named in source: `https://claude.ai/artifact/BiAF9fiysaHGTHH1CYNQmL` (`s32/REPORT_S32.md` header). It was not opened for this import.

## The sprint's own question (charter)

`s32/BRIEF.md` stores the user's charter "VERBATIM and in full" (2,087 lines, 71 numbered sections). Its key terms:

- North star: "**mean built-chain Cα RMSD on the canonical 126-target development instrument**." The endpoint at the start was "approximately 3.2105 Å". Primary target "< 3.00 Å", ambitious "< 2.50 Å" (BRIEF §2).
- "CVaR-VQE is the central scientific focus and must remain the main quantum research spine, but CVaR-VQE itself is not the goal. The goal is RMSD." (BRIEF preamble)
- It treats S31's finding that "the deployed Hamiltonian's diagonal is effectively the same vector across targets" as a hypothesis to audit, "NOT automatically the final explanation" (BRIEF §3).
- Central quantum question (§14): "**Can a genuine CVaR-VQE be designed whose quantum state and objective actually contain information that can improve RMSD?**"
- Ultimate question (§67): "**Why is the final built-chain RMSD stuck around 3.21 Å, and what intervention can actually move it?**"
- Statistics (§48): "MDE = 2.8016 × SE". Below 0.7× MDE is "not a result". 0.7–1.0× is "not measured".
- Oracle discipline (§46): every native-reading result is labelled "ORACLE / NOT DEPLOYABLE".
- Closing line: "Say if its possible to lower rsmd at the end, maybe test on longer proteins etc."

## Contract (rules every lane worked under)

`s32/S32_CONTRACT.md` carries S31's 32 rules forward and adds S32-specific rules 15–24. The load-bearing ones:

- Rule 0: three objects "never differenced against each other": built chain **3.2105** ("THE ENDPOINT"), CA point cloud 3.0483 ("diagnostic only"), set mean 3.5507.
- Rule 1: `MDE = 2.8016 × SE` per comparison. A RESULT needs ≥ 1.0× MDE, a fold CI excluding zero and ≥ 4/5 folds agreeing. `stats_lib.compare` is "LOWER IS BETTER".
- Rule 2: ORACLE arms are labelled "ORACLE / NOT DEPLOYABLE" on every occurrence.
- Rules 3 and 20: the projection is "deterministic but chaotic". "Bit-identity, not value-identity, licenses a cross-job chain comparison." "Unpaired cross-job chain claims below ~0.03 Å are not resolvable."
- Rule 7: "Cross-lane claims have no owner". In S31, "every single-lane result held and every cross-lane synthesis failed, four for four."
- Rule 12: "FAIL18 is outcome-defined". It is a circular stratum.
- Rule 13: retractions stay in place, annotated, never deleted.
- Rule 16: "The projection cost is a property of the OBJECT being projected, not a constant". Later amended: "It is not sparsity that is cheap — it is ALIGNMENT", and then "AND ALIGNMENT IS NOT A LEVER".
- Rule 17: "The pool is not the bottleneck; say what is, with the ladder in the sentence."
- Rule 21: "The endpoint is not a cached scalar".
- Rule 22: "a penalty is not a selector".
- Rule 23: "`split_half_transfer` nulls the wrong question unless you give it production as the baseline".
- Rule 24: "Staging is not lane-isolated in practice".

## Structure: lanes, pre-registrations, verification

Per `s32/STATE.md` (LANES table), `s32/REPORT_S32.md` Appendix B and the PREREG files, the sprint ran six lanes:

| lane | question (as stated in source) | prereg | commit cited |
|---|---|---|---|
| **R** reconstruction | "Is the +0.1622 projection cost recoverable? Is the branch degeneracy an *opportunity*? Does a chiral criterion have in-band skill over branches?" | `s32/PREREG_S32_R.md` | `02754f5a` |
| **Q** CVaR-VQE | "Falsify S31's target-invariance first. Then: how precisely must `a` be known for `w*` to be useful?" | `s32/PREREG_S32_Q.md` | `a8f9d6a7` |
| **P** pool/selection | "Decompose pool quality / diversity / common-mode / ranking / readout / reconstruction independently." | `s32/PREREG_S32_P.md` | `33dfe0d3` |
| **D** physical response | "Does a **chiral** native-free observable have in-band skill where achiral ones provably cannot?" | `s32/PREREG_S32_D.md` | `34973b1b` |
| **V** verification/adversary | "Independently rebuild 3.2105 from artefacts. Own the verifier, multiplicity, and the attack on every promising result." | none (audits; `s32/MULTIPLICITY.md` says "Lane V emits no endpoint comparison by design") | — |
| **L** length generalisation | the charter's "maybe test on longer proteins"; builds `long40` | `s32/PREREG_S32_L.md` | `88f2da39` |

- Ledger: `s32/LEDGER.md`, entries S32-L0 through S32-L12 plus lane-labelled entries L(D1–D3), L(Q1–Q3), L(R1–R4), L(P1), L(L1–L4).
- Causal map (charter §55 "backbone"): `s32/CAUSAL_MAP.md`, marked "v1, hours into the sprint".
- Theory: `s32/THEORY_Q.md` (lane Q derivations Q0–Q4, theorems Q1-T1/T2/T3).
- Multiplicity: `s32/MULTIPLICITY.md`, owned by lane V.
- Verifier: `s32/s32_verify.py` (not run for this import). `REPORT_S32.md` states "143 recomputed, 0 mismatched, 0 flagged, 18/18 self-tests across eleven audits". The final count is quoted inconsistently across files; see LESSONS.md, Importer notes.
- Lane-specific verifiers named in the ledger: `s32/s32_Q_verify.py` ("22 checks, all pass"), `s32/s32_R_verify.py` ("43 checks, 43 pass"), `s32/s32_L_verify.py` ("8 checks, 8 pass").
- Scale (REPORT Appendix B): "Six lanes, 24 ledger entries, ten pre-registrations, 56 result artefacts." Comparisons emitted: lane P 38, lane D 92, lane V "32 on the chain basis plus 8 in-band", lane R 64 in the branch family alone.

### Instruments

- **`tuning126`**: 126 targets, 9–16 aa (mean length 12.96), folds 25/23/25/23/30 (`s32/REPORT_S32.md` §1.1; `s32/THEORY_Q.md`).
- **`long40`**: 45 targets, 44–60 residues (mean 54.71), five frozen folds of nine. It was built by lane L from `prots/`. It has "Zero overlap with `tuning126`; `benchmark60` never opened" (`s32/REPORT_S32.md` §7.1; `s32/LEDGER.md` S32-L(L1-L4)).

## Headline findings as the sprint stated them

### H1. The endpoint did not move

- **Measured:** "Improvements clearing 1.0× MDE on the BUILT CHAIN, deployable: **ZERO.**" 30 arms clear 1.0× MDE on some basis: "about twenty read the native, four are filter-vs-random on the pool mean, six are in-band diagnostics." The endpoint is 3.2105 Å (`s32/REPORT_S32.md` §0; `s32/MULTIPLICITY.md` Running totals).
- **Original interpretation:** "Every arm that clears MDE either reads the native, is measured on a basis that is not the endpoint, or points the wrong way." The charter targets < 3.00 and < 2.50 are "both unmet" (REPORT §0).
- **Status in source:** final.

### H2. The canonical endpoint's definition

- **Measured:** 3.210534 is "the λ = 0.3 multi-start projection arm of `s12/instrument.project` applied to `s29/results/s29_O_structs/<pdb>.npz["prod"]`". It reproduces "bit-identical 126/126". The chain production itself emits is 3.214765. The endpoint is 0.0043 Å better than that. A one-ULP (7.1e-15 Å) cloud change moves the chain 0.10–0.15 Å. Five perturbed draws give sd **0.003049**. (`s32/REPORT_S32.md` §1; `s32/LEDGER.md` S32-L4, S32-L6, S32-L12. Confirmed in `s32/results/s32_V_chain_bitexact.json`: 3.210533994943299 / 3.2147651542 / 3.2126252197. Confirmed in `s32/results/s32_V_ulp_distribution.json`: draw_sd 0.0030491.)
- **Original interpretation:** "The operator is bit-reproducible. The input is what is fragile."
- **Status:** confirmed (AUDIT; lane V).

### H3. The readout is a hull projection (Q1-T2)

- **Measured:** gain 0.9999999999 in-hull and 4.0e-09 orthogonal. Window dimension |S|−1 = 5.254 mean. Hull floor `d = 1.8290 ± 0.1178` (CA cloud, ORACLE). Crossover against direct emission at "ε ≈ 2.2". (`s32/THEORY_Q.md` Q1-T2; `s32/results/s32_Q1_sufficiency.json`: gain_in_mean 0.99999999989, support_aff_dim_mean 5.254, hull/kabsch_mean 1.82904.)
- **Original interpretation:** "**A structure estimate good enough to make the readout worth solving is already good enough to emit.**" S31's null for exactly solving the CVaR objective is "**forced**" (REPORT §0.1, §3.1).
- **Status:** theorem plus numerical falsifier that did not fire. An auxiliary claim, "gain exactly 1 means no noise suppression", was **struck** (see NEGATIVE_RESULTS N-Q3).

### H4. `a` and `μ` are one object (Q1-T1, closes S31 §20.3)

- **Measured:** substituting `P_aff{W} t` for `t` moves `w` by 7.0e-12 and the structure by 2.9e-12 Å on 126/126. Lane P recovers `μ` from `{a_k, d_k}` at relative residual 2e-14 on 126/126, against a shuffled-`d` control of 0.373. `rank(d) = 3n − 6` "EXACTLY on 126/126". (`s32/THEORY_Q.md` Q1-T1; `s32/LEDGER.md` S32-L5, S32-L(P1); `s32/MULTIPLICITY.md` P-14, P-37.)
- **Original interpretation:** "**A per-candidate quality estimator with in-band skill IS a structure predictor**, and a common-mode corrector IS a per-candidate quality estimator." The requirement is "exactly ~39 real numbers with no compression available" (REPORT §0.2, §3.2).
- **Status:** "closed, by derivation", established "independently and in opposite directions" by two lanes.

### H5. The 2.10 Å pool headroom "is a FIT, not a RETRIEVAL"

- **Measured (CA cloud, ORACLE / NOT DEPLOYABLE, n=126):**
  - BLOSUM500 1.1167.
  - RAND500 1.1495 (+0.0328, 0.38×, 63W/63L).
  - DONOR500, another target's universe, 1.1626 (+0.0459, 0.49×, 47W/79L), NOT A RESULT.
  - "Retrieval's share of the 2.10 Å is 2.2%".
  - Source: `s32/REPORT_S32.md` §2.0; `s32/MULTIPLICITY.md` V-A9. Confirmed in `s32/results/s32_V_hull_capacity.json`: 1.11672 / 1.14951 / 1.16262, effect_over_mde 0.3786 / 0.4877.
- **Original interpretation:** "At 9–16 residues fragment space is close to saturated, so the ladder's top rung prices a FIT, not a RETRIEVAL." Retrieval "sets the **pool mean**", and that is what production consumes.
- **Status:** stated as "the deepest result of the sprint". The long-length prediction that this control "should FAIL" at 3n ≈ 164 was **not run** (REPORT §7.6).

### H6. In-band skill: the per-target SIGN is missing, and the route is ceilinged

- **Measured:** in-band diagnostic basis. AMBER mean in-band ρ is +0.0000, while mean|ρ| is 1.88× a within-band permutation null (2.36× MDE, 5/5). Split-half sign transfer under a cross-target null is AMBER +0.1163, DIS +0.1901, LEG_total +0.2180, LEG_torsion +0.1492, RG +0.3228, and NOISE +0.0056 (0.15×) as the self-test. 2.0 Å needs in-band ρ ≈ 0.638. (`s32/REPORT_S32.md` §4; `s32/MULTIPLICITY.md` D-14…D-17, D-67…D-72.)
- **Original interpretation:** "`Var(ρ) > 0` with `E[ρ] = 0`". "Even a free, perfect per-target sign leaves the best in-band scorer 2–3× short." "The sign is CLOSED AS A ROUTE and kept as a FINDING." Positive in-band skill exists on the native-free band, "it is typicality — and the terminal operator is already its argmin."
- **Status:** ORACLE / NOT DEPLOYABLE ceiling. The native-free prediction of the sign failed (see NEGATIVE_RESULTS).

### H7. The quantum question

- **Original interpretation:** Charter §14 is answered "**no, on this instrument, and the binding reason is chain length.**" `2^n_res ≤ 65536` on 126/126. Two properties are needed together: "P1 — a decision space that GROWS WITH THE TARGET" and "P2 — a genuinely STOCHASTIC energy". The source says "this project has never had either". (`s32/REPORT_S32.md` §0.5, §6; `s32/THEORY_Q.md`; `s32/LEDGER.md` S32-L(Q3).) Details are in QUANTUM_RESULTS.md.

### H8. Longer proteins (`long40`)

- **Measured (built chain, pre-AMBER):** readout share of recoverable loss is "77.9% at L ≈ 13 and 82.0% at L ≈ 55". All three registered predictions P1–P3 "HOLD". Filter skill does **not** replicate at length: −0.3171 at 0.39× (`s32/REPORT_S32.md` §7.2; `s32/LEDGER.md` S32-L(L1-L4); ladder numbers confirmed in `s32/results/L2_ladder_verdict.json`).
- **Original interpretation:** "This sprint's conclusions are not a peptide-length artefact". The shape is preserved "in the ORACLE rungs and the readout rung, not universally".
- **Status:** registered predictions held. L-H1 was falsified (see NEGATIVE_RESULTS).

### H9. "Is it possible to lower the RMSD?"

- **Original interpretation (REPORT §9):** "**Yes — but not by any route this pipeline's architecture makes available**". "On `tuning126`, with this architecture, at this chain length: no." "The primary target of < 3.00 Å is 0.21 Å away and it is not 0.21 Å of engineering."
- **Next bottleneck (REPORT §10):** "`3n − 6` ≈ 39 real numbers per target, which are the answer."
- **S33 priorities:**
  1. "Go longer" (run the donor-pool control on `long40` first; retrain the distance prior capped at `MAXLEN = 26`).
  2. "Weight toward the set best" (operator law ratio 2.85, untested).
  3. "Stop looking for native-free in-band skill as posed".
  4. The "Do not re-open" list.

## Glossary of original terminology (as used in source)

- **built chain / CA point cloud / set mean**: three distinct objects (3.2105 / 3.0483 / 3.5507) that are "never differenced" (`s32/S32_CONTRACT.md` rule 0).
- **ORACLE / NOT DEPLOYABLE**: an arm that reads native coordinates anywhere (contract rule 2).
- **DEP / deployable / native-free**: an arm that uses no native information. Source uses "deployable" and "native-free" rather than "DEP".
- **MDE**: 2.8016 × SE, per comparison. Verdicts are "RESULT", "NOT MEASURED" (0.7–1.0×) and "NOT A RESULT" (< 0.7×).
- **`tuning126`**: the canonical 126-target development instrument, 9–16 aa. **`benchmark60`**: the sealed benchmark, never opened. **`long40`**: the S32 44–60 residue instrument (45 targets).
- **FAIL18**: "targets where no pool member within 1.5 Å of the pool best survives into the production top-75" (`s12/instrument.py::selfcheck`, quoted in `s32/LEDGER.md` S32-L8). It is outcome-defined and "circular".
- **K=500 pool / top-128 / top-75**: BLOSUM62 retrieval to 500, then the distogram score prefix to 128 ("the quantum field of view", 128 = 2⁷, "the VQE register width"), then to 75. The production readout is the uniform coordinate average of the top-75.
- **`a`**: per-candidate quality `a_x = ‖W_x − t‖²` (ORACLE). **`B`**: pairwise squared-distance matrix (native-free). **`μ`**: pool common mode `c − t` or `X̄ − t`. **`t`**: native.
- **hull floor `d`**: dist(native, hull) = 1.8290 (CA cloud, ORACLE).
- **in-band**: within a target's shipped top-75 band. "In-band skill" means Spearman ρ against true RMSD inside the band.
- **typicality / consensus**: small `|d_k|`, i.e. closeness to the pool. The source says "the terminal operator is already its argmin".
- **DIS**: the shipped distogram Bayes-risk score. **LEG_total / LEG_torsion**: Legacy Hamiltonian terms. **AMBER**: ff14SB/GBn2. **RG**: radius of gyration.
- **G1**: S30 theorem that a single-structure scalar is a function of the distance map iff it is reflection-invariant ("achiral"). **D-E / D-F / D-G**: lane D's extensions (`s32/PREREG_S32_D.md`).
- **order statistic / best-of-K / split-half transfer**: the pricing of per-target minima (contract rule 9).
- **GEN4 / GEN4D / MEM75 / RAND0 / PROD8**: lane R branch start families (`s32/LEDGER.md` S32-L(R4)).
- **price / orthogonal null / `cos`**: price = chain − cloud. Orthogonal null = `sqrt(e²+d²) − e`. `cos = (e²+d²−chain²)/(2ed)` (contract rule 16).
- **Q0 / Q1-T1 / Q1-T2 / Q1-T3 / Q4**: lane Q audit and theorems (`s32/THEORY_Q.md`).
- **conditions A–E, P1/P2**: lane Q's criteria for CVaR-VQE doing "real work".
- **operator law**: `out = −0.9934 + 0.9219·set_mean + 0.3232·set_best` (built chain, ratio 2.85).
- **"a number re-used across a boundary its definition does not cross"**: the sprint's name for its recurring defect class.

## Complete list of source files read

Read completely (all tracked `.md` in `s32/` per `git ls-files s32`):

1. `s32/BRIEF.md`
2. `s32/CAUSAL_MAP.md`
3. `s32/LEDGER.md`
4. `s32/MULTIPLICITY.md`
5. `s32/PREREG_S32_D.md`
6. `s32/PREREG_S32_L.md`
7. `s32/PREREG_S32_P.md`
8. `s32/PREREG_S32_Q.md`
9. `s32/PREREG_S32_R.md`
10. `s32/REPORT_S32.md`
11. `s32/S32_CONTRACT.md`
12. `s32/STATE.md`
13. `s32/THEORY_Q.md`

Skimmed: `s32/report_page.html`. Its only non-template content is a masthead summary, a verdict legend and a footer. It renders `REPORT_S32.md` client-side and adds no findings; its count discrepancies are noted in LESSONS.md.

Opened to confirm headline numbers (numeric leaves only):

- `s32/results/s32_V_hull_capacity.json`
- `s32/results/s32_D5_signchain_LEG_total.json`
- `s32/results/s32_V_chain_bitexact.json`
- `s32/results/s32_V_ulp_distribution.json`
- `s32/results/s32_Q1_sufficiency.json`
- `s32/results/s32_P_rand.json`
- `s32/results/L2_ladder_verdict.json`
- `s32/results/s32_P_rankchain.json`
- `s32/results/s32_R_dilation_cloud.json`
- `s32/results/s32_R_sparse_control.json`
- `s32/results/s32_R_analysis.json`
- `s32/results/s32_V_R_adversary.json`
- `s32/results/s32_Q0_invariance.json`

Checked for Sprint 32 passages: `docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` in the source repo. Neither contains any S32 material; see LESSONS.md, Importer notes.
