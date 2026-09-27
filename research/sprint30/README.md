_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s30/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 30 — "Find the first real accuracy breakthrough" (evidence index)

## 1. Source pin

| item | value |
|---|---|
| Repository | `C:\Users\abena\cvar-vqe-protein-folding-v3` (read-only) |
| Commit | `3d5b2d25b718346401268634da275f4d7e9fcf3f` |
| Sprint directory | `s30/` (267 tracked files: 28 `.md`, 72 top-level result files in `s30/results/`, 126 `s30/results/s30_R_chains/`, scripts) |
| Branch named in report | `s26` (`s30/REPORT_S30.md` header) |
| Sprint date | 2026-09-20 (ledger timestamps 12:35 to 14:16; `s30/LEDGER.md`) |
| Benchmark | 126 dev targets, 9–16 aa; endpoint = mean built-chain Cα RMSD (`s30/REPORT_S30.md` header) |

## 2. The sprint's own question, contract and brief

**Charter** (`s30/BRIEF.md`, recovered verbatim from the session transcript and written 77 minutes after S30-L0 claimed it had been saved — see the provenance comment at the top of `s30/BRIEF.md` and the annotation in S30-L0):

- Objective: *"Produce a genuinely better protein structure using a CVaR-VQE-centered architecture, while driving the mean built-chain Cα RMSD as low as possible."* Production was ~3.21 Å; targets < 3.0 Å (primary), < 2.5 Å (ambitious) (`s30/BRIEF.md` §2).
- Hard constraint: *"CVaR-VQE remains the spine and main scientific object"*, and *"removing or randomizing the quantum stage measurably degrades the result"* (`s30/BRIEF.md` §5).
- The central question: *"How do we make CVaR-VQE optimize a structurally meaningful problem whose solutions actually correspond to better protein structures?"* (`s30/BRIEF.md` §3).
- Twelve leads L1–L12 carried from S29, explicitly *"a leads register, not a task list"* (`s30/BRIEF.md` §8).
- §7: build the cost/RMSD meter first, with baselines ladder ρ ≈ −0.40, cosine ≈ −0.03, native percentile ≈ 36.9, ORACLE preference ≈ 0.07.
- §18: a quantum breakthrough requires *"the CVaR-VQE to contribute information or optimization behavior that a matched classical control does not reproduce"*, including a product-state/separable restriction.
- A sixth, unranked priority: *"a decisive measurement of what imposes the ceiling"* (`s30/BRIEF.md` §4).

**Contract** (`s30/S30_CONTRACT.md`, 28 rules): built-chain RMSD is the endpoint; below 0.7× MDE is not a result and 0.7–1.0× is not a demonstrated improvement; MDE per comparison (2.8016 × SE); fold-clustered CIs govern; controls in the operator's own space; ORACLE rows labelled in every sentence; pre-register falsifiers; the meter gates compute (rule 22); multiplicity tracked sprint-wide (rule 26); *"The main team may not approve its own positive"* (rule 27); *"Do not call something quantum merely because a quantum circuit produced it"* (rule 28).

**Setup notes** (`s30/STATUS.md`): two corrections to the charter's reading list (S29 report is at `s29/REPORT_S29.md`; S29's ledger is `s29/LEDGER.md`); the meter already existed as `s29/s29_D_cost_audit.py` and was verified/extended; the `s26/jobrun.py` `CPU_START = 85.0` vs `s26/governor.py` `CPU_CEILING = 101.0` defect was open.

## 3. Structure of the sprint

### 3.1 Lanes (`s30/REPORT_S30.md` §2.1; `s30/LEDGER.md` S30-L0)

| lane | remit (source wording) | ledger entries |
|---|---|---|
| D | adversary, permanent; owns and extends the cost/RMSD meter | S30-L3, L4, L5, L21, L22, L23, L24 |
| L | literature, permanent | S30-L6, L7, L8, L13, L18 (+ `s30/lit/`) |
| T | theory: bit accounting (L8) and when the CVaR tail stops being a prefix | S30-L9, L14, L15 (+ `s30/THEORY.md`) |
| F | the failure tail (FAIL18) | S30-L2, L16, L17 |
| X | divergent, permanent: should the quantum stage select or generate? | S30-L10, L20 (+ `s30/s30_X_FINDINGS.md`) |
| R | is nativeness recognisable from one structure at all (L11) | S30-L1, L19 |
| Q | L5 + L6 together: subset objectives and sparse readouts | S30-L11, L12 (+ `s30/briefs/Q_to_T_quadric_and_rank.md`) |
| P | the prior (L3 reformulated) | S30-L25, L27 |
| G | "the two questions nobody had measured" | S30-L26 |
| V | report adversary (§1, §3, §4, App. A) | `s30/AUDIT_V.md` |
| W | what CVaR-VQE contributed (charter items 12–19) | `s30/QUANTUM_W.md` |
| Y | synthesis of §7/§8 | `s30/SYNTHESIS_Y.md` |
| Z | second report adversary (§0, §2, §5, §6, §9–§13) | `s30/AUDIT_Z.md` |
| coordinator | integration, report | S30-L0, S30-L28, `s30/STATE.md`, `s30/REPORT_S30.md` |

Ledger entries S30-L0 … S30-L28 (29 headings; AUDIT_Z counted 28 at the time of its audit, before S30-L28 was added). Several entries were renumbered after numbering collisions; the collision notices are in-place annotations (`s30/LEDGER.md`, e.g. lines 1348, 1734, 2219, 2325, 2375, 3102).

### 3.2 Pre-registrations (ten files, eight lanes)

`PREREG_S30_D_gram.md`, `PREREG_S30_F1.md`, `PREREG_S30_F2.md`, `PREREG_S30_F3.md`, `PREREG_S30_G.md`, `PREREG_S30_P.md`, `PREREG_S30_Q_sparse.md`, `PREREG_S30_R.md`, `PREREG_S30_T.md` (with addenda M4/M5/P5 and a declared post-hoc clause P5d), `PREREG_S30_X.md` (with addendum H-X3).

### 3.3 Experiments / architectures

**No new architecture was deployed.** `s30/REPORT_S30.md` §0.1: *"None was deployed. Every candidate was closed — by measurement, by theorem, or by price — before it reached the pipeline."* The production path is unchanged, with the quantum stage **off** (`core/pipeline.py:179` `quantum: bool = False`; `:241` `PROD = Config()`; cited in `s30/QUANTUM_W.md` §12.0 and verified by `s30/AUDIT_Z.md`). What was built is instrumentation: `s30/s30_D_meter.py` (meter with `verify`, both bases, R = 8 draw control, multiplicity counter), `s30/s30_verify.py` (36 headline numbers asserted, 0 mismatches per `s30/REPORT_S30.md` §13.2), and `s30/THEORY.md` (`s30/REPORT_S30.md` §13.2).

### 3.4 Verification

- Two independent report adversaries under contract rule 28: lane V (18 defects; *"two of which inverted a headline"*) and lane Z (23 defects; four severe). The report states all are fixed in place with the original error stated (`s30/REPORT_S30.md` header; `s30/AUDIT_V.md`; `s30/AUDIT_Z.md`). See `LESSONS.md` Importer notes for items that appear not fully fixed.
- `s30/s30_verify.py`: 36/36 matched (`s30/REPORT_S30.md` §10.1; run by lane Z, `s30/AUDIT_Z.md`). Lane V noted the verifier's coverage was concentrated on lane D artefacts (`s30/AUDIT_V.md` D16).
- S30-L28 records seven ledger-vs-ledger contradictions found by lane Y (`s30/LEDGER.md` S30-L28; `s30/SYNTHESIS_Y.md` Appendix Y).

## 4. Headline findings as the sprint stated them

### H1. The endpoint did not move
- **Measured:** final mean built-chain RMSD **3.2105 Å**, unchanged; did not beat 3.21, 3.0 or 2.5 (`s30/REPORT_S30.md` §0.1). Nothing deployed.
- **Interpretation:** *"The target is reachable. Nothing we own can reach it."* (`s30/REPORT_S30.md` §0.2).
- **Status:** final, audited by lanes V and Z.

### H2. Five ORACLE signs clear the primary target (ORACLE, not deployable)
- **Measured:** `ORACLEsign_LFOmag` built chain **3.2126 → 2.8867, Δ −0.3259 Å, 2.05× MDE, 5/5 folds, 92W/34L** (cloud Δ −0.3567); `ORACLE_SEPPROF5` built chain 2.6791, Δ −0.5335, 2.29× MDE (`s30/results/s30_P_chain.json`, confirmed by importer; S30-L27 annotation). Baseline for this arm is 3.2126, not 3.2105 (projection seed not pinned; `s30/REPORT_S30.md` §1.1). Leakage: **ORACLE**.
- **Interpretation:** *"The prize is five bits per target"*; 68% of the profile prize in `|i−j| ≥ 7` (S30-L25 §4). AUDIT_Z D9: the five signs are one per separation bin (`SEP_EDGES = [(2,2),(3,3),(4,4),(5,6),(7,99)]`), not five long-range signs, and the ~4× tail concentration belongs to `ORACLE_SEPPROF5` (the five-sign arm is 3.25× / 1.82×).
- **Status:** measured, ORACLE; the report now carries the corrected wording (§12.3).

### H3. Correcting the prior from {sequence, library} is closed; the "coherence" gate
- **Measured:** out-of-fold R² of the whole native-free feature space against the ORACLE displacement **0.0083** (excess over matched-dimension control +0.0095, 0.75× MDE, NOT MEASURED) against a registered 1.96% bar (S30-L25; `s30/PREREG_S30_P.md`). Fitted correctors applied (CA point cloud vs 3.0483): N1 +0.1461 (0.91×), N2 +0.1513 (0.95×), N3 +0.0554 (0.68×, fold CI [−0.006, +0.119]) — all NOT MEASURED; ORACLE-constructed i.i.d. arms −0.1260 (1.23×, TYPE-M flag) and −0.2466 (1.77×) (`s30/results/s30_P_lr.json`, confirmed by importer). `coh` (within-target): uncorrected 0.6931; N1 0.7857, N2 0.7827, N3 0.9172; i.i.d. 0.5868, 0.5365 (same file).
- **Interpretation:** *"What can be predicted is coherent and therefore harmful; what would help is incoherent and therefore unpredictable."* Proposed gate: *"ADMIT iff coh < 0.6931"* (`s30/REPORT_S30.md` §0.3, §12.2).
- **Status:** the gate is **ORACLE** (both arguments need `d_nat`, `s30_P_lr.py:58,78,202`), a development-time test only — the report first called it "native-free" and was corrected after `s30/AUDIT_Z.md` D1.

### H4. The tail is selection-limited, not pool-limited
- **Measured:** ORACLE best pool member on FAIL18 **2.2842 Å** CA cloud (2.2845 chain), 13/18 under 3.00, worst 3.5436 (`s30/results/s30_F_stagegap.json` F1a, confirmed). On the worst 18 by production RMSD: 2.5298, 11/18, worst 3.9523 (recomputed by lane V, `s30/AUDIT_V.md` D3). ORACLE.
- **Interpretation:** *"the material to fix the tail is already inside the candidate sets"* (`s30/REPORT_S30.md` §4.1).
- **Status:** survived; FAIL18 label corrected after AUDIT_V D3.

### H5. Recognition from single-structure geometry: ordering survives, preference fails on all 43 channels
- **Measured:** F-R1 does not fire; DIS ordering +0.347, anchor contrast +0.134, p_max 0.000; best `pref_near` RAMA 0.640 (bar 0.65); D1 locality ΔR² local −0.0894 [−0.1217, −0.0522] vs global +0.5997 [+0.5850, +0.6166] (`s30/results/s30_R_verdict.json`, confirmed; S30-L19).
- **Interpretation:** *"A sum of per-residue terms cannot see a lever arm"*; null for per-residue channels is *"a theorem on this instrument"* (S30-L19). With G1 (lane G), every achiral single-structure channel is a distance-map reading (S30-L26).
- **Status:** survived; lane R's registered prior (4:1 does not fire) held.

### H6. The quantum stage (see `QUANTUM_RESULTS.md`)
- **Measured:** no CVaR-VQE was trained; a 9-qubit depth-3 statevector circuit ran on all 126 targets on an ORACLE objective (rung regeneration). Same circuit: `circ_best` 0.2516 Å chain (ORACLE objective) vs `circ_opt` 3.4330 Å (deployed native-free objective) vs PROD 3.2071 (`s30/results/s30_D_meter_DIS_chain.json`, confirmed).
- **Interpretation:** *"The circuit is not the problem. The objective is"* (`s30/REPORT_S30.md` §5.2); T1: *"the tail is always a prefix"*; *"α supplies τ; it is not doing selection."*
- **Status:** audited by lanes W and Z; §5 found clean by Z.

### H7. The pool is a codebook, not a channel; value-of-a-bit law
- **Measured:** ORACLE ladder D(R) 4.1080 → 1.8978 (R = 7) → 1.7108 (R = 8.97), CA cloud; fit a = 1.3312, c = 2.7859, γ = 3.1636, R² 0.998341 (S30-L14; the fit parameters are not stored in `s30_T_bits.json`, lane V's refit gave a 1.3176 / γ 3.1917 / R² 0.998573). Candidate identity 0.132 Å/bit vs subset cardinality 0.044.
- **Interpretation:** *"The encoding is not the hidden bottleneck"* (S30-L14). The "36.6 bits / 5.2×" multiplier depends on `d`; at d = 6 it is 6.69 bits, 0.95× (AUDIT_V D2; report §4.2 now states the formula).
- **Status:** qualitative claim retained; multiplier corrected downward.

### H8. E2 (AMBER relax at k = 30) is real, divergence-graded, small, not deployable
- **Measured:** whole-sample gain **−0.0221 Å** (0.69% of 3.2105); high-minus-low dispersion contrast within length tertiles −0.0406, 3.56× MDE, 5/5; 97.2% of gain in high-dispersion half (`s30/results/s30_G_disp2.json`, confirmed).
- **Interpretation:** E2 *"stays out of the mechanism column on SIZE, not on reach"*; restraint constant has *"no native-free selection rule"* (`s30/REPORT_S30.md` §A.7, §11.2).
- **Status:** open (report §7.4 #4); leakage: the restraint constant was *"picked on dev-set RMSD"* — i.e. native-informed tuning, not deployable.

## 5. Glossary of original terminology

| term | meaning as used in source |
|---|---|
| **ORACLE** | any quantity/arm that reads the native; labelled in every sentence (`s30/S30_CONTRACT.md` rule 9). Opposite: *native-free* / *deployable*. The source does not use the label "DEP". |
| **built chain / CA point cloud** | endpoint basis (ideal-geometry chain after multi-start projection) vs intermediate coordinate average; production 3.2105 chain / 3.0483 cloud |
| **FAIL18** | pinned 18 targets on which the score's top-75 retained zero pool members within 1.5 Å of the pool optimum (`s12/instrument.py:271-278`, per S30-L23) — *not* the 18 worst by RMSD (overlap 13/18) |
| **worst18_poolmean / worst18_bestpool (tail A / tail B)** | the two "filter-independent tails" |
| **MDE** | 2.8016 × SE per comparison; < 0.7× "not a result", 0.7–1.0× "NOT MEASURED" |
| **the meter** | `s30/s30_D_meter.py`; PASS/BLOCK gate; shipped cost DIS BLOCKs on both bases |
| **DIS / DIS_SURR** | shipped L1 Bayes-risk distogram score / its interpolation surrogate |
| **T1, T1b** | lane T's prefix theorem and halfspace (VC dim d+1) reachability cap (`s30/THEORY.md` §2–3) |
| **trichotomy** | exogenous order → one sort; endogenous convex → Frank–Wolfe; endogenous non-convex → combinatorial (`s30/THEORY.md` §3.2) |
| **codebook, not a channel** | the 500 deposited backbones carry the structure and the index names one (S30-L14) |
| **value-of-a-bit law** | `D(R) = a + c·2^(−R/γ)`, `−dD/dR = 0.2191·(D − 1.331)` |
| **m_eff** | effective independent pool size 1.398 (S30-L7) |
| **E1/E2/E3** | the three escapes from common-mode non-identifiability: prior on bias form / constraint on the native / second observation (S30-L7) |
| **G1 (chirality dichotomy), G1a, G1b** | lane G theorem: a rigid-invariant single-structure channel is a function of D iff reflection-invariant; corollaries (S30-L26) |
| **coh** | within-target corr(corrector residual, pool common-mode pair error) — ORACLE (S30-L27) |
| **set_mean² ≈ B² + S²** | lane X decomposition: B = endpoint (bias), S = spread (S30-L20) |
| **source law / admission condition** | `d_out = 0.803·d_set_mean + 0.298·d_set_best` (frozen S20 coefficients); amended to `Δ(bias B) + 0.298·Δ(set best) < 0` (S30-L10, L20) |
| **best_of_k_within / common direction bank / split-half transfer** | order-statistic pricing tools (S30-L12, S30-L15 §3c) |
| **"reachable, not exploitable"** | lane T's phrase for the halfspace class after M6 |
| **killed by measurement / theorem / price** | the report's three-way death taxonomy (58 / 19 / 8 of 91, 6 open; `s30/REPORT_S30.md` §7) |
| **cross-kind confound** | comparing structures that differ in construction as well as nativeness (S30-L1) |
| **"a matched control in the right space does not rescue a stratum defined by the outcome"** | S30-L23 checklist entry |
| **load-bearing** | used in source for numbers/claims a conclusion rests on |

## 6. Source files read (complete)

All 28 tracked `.md` files under `s30/` were read in full:

`s30/AUDIT_V.md`, `s30/AUDIT_Z.md`, `s30/BRIEF.md`, `s30/LEDGER.md` (3,921 lines, S30-L0…L28), `s30/PREREG_S30_D_gram.md`, `s30/PREREG_S30_F1.md`, `s30/PREREG_S30_F2.md`, `s30/PREREG_S30_F3.md`, `s30/PREREG_S30_G.md`, `s30/PREREG_S30_P.md`, `s30/PREREG_S30_Q_sparse.md`, `s30/PREREG_S30_R.md`, `s30/PREREG_S30_T.md`, `s30/PREREG_S30_X.md`, `s30/QUANTUM_W.md`, `s30/REPORT_S30.md` (1,451 lines), `s30/S30_CONTRACT.md`, `s30/STATE.md`, `s30/STATUS.md`, `s30/SYNTHESIS_Y.md`, `s30/THEORY.md`, `s30/s30_X_FINDINGS.md`, `s30/briefs/Q_to_T_quadric_and_rank.md`, `s30/lit/L30_1_reference_state.md`, `s30/lit/L30_2_common_mode.md`, `s30/lit/L30_3_set_selection_cvar.md`, `s30/lit/L30_4_shared_bias.md`, `s30/lit/L_INDEX.md`.

Result JSONs opened to confirm cited headline values: `s30/results/s30_P_chain.json`, `s30_P_lr.json`, `s30_D_meter_DIS_chain.json`, `s30_D_meter_DIS_ca.json`, `s30_R_verdict.json`, `s30_G_disp2.json`, `s30_G_chiral.json`, `s30_F_stagegap.json`, `s30_Q_sparse.json`, `s30_Q_quadric.json`, `s30_Q_rankcheck.json`, `s30_T_transfer.json`, `s30_X_ensemble.json`, `s30_D_gram.json`.

`docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` were searched for Sprint 30 passages; **none exist** (see `LESSONS.md` Importer notes).

See also: `NEGATIVE_RESULTS.md`, `QUANTUM_RESULTS.md`, `LESSONS.md` in this directory.
