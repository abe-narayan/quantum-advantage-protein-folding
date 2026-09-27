_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s31/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 31 (S31): evidence index

## Source pin

- **Repository:** `C:\Users\abena\cvar-vqe-protein-folding-v3` (GitHub `abe-narayan/cvar-vqe-protein-folding-v3`), commit `3d5b2d25b718346401268634da275f4d7e9fcf3f`. Read-only.
- **Paths:** `s31/` (146 tracked files: 16 `.md`, 1 `.html`, scripts, `s31/results/*`, `s31/lit_L/*`).
- **Sprint dates and branch:** opened 2026-09-20 (charter saved 23:44). REPORT_S31.md was marked "FINAL — 2026-09-21 01:27". The code ran on branch `s26` (`s31/REPORT_S31.md` header).
- **Published page:** `s31/REPORT_S31.md` names `https://claude.ai/artifact/BJ6WTXG3cjtq5jQ95LqgSS`, which is rebuilt from REPORT_S31.md by `s31/build_report_page.py`. The report says the page "renders this file client-side, so the two cannot drift". I did not treat `s31/report_page.html` as a separate content source (see LESSONS.md, importer notes).

## The sprint's own question, contract and brief

**Charter** (`s31/BRIEF.md`, the user's message saved verbatim, 1,660 lines):
- Improve the canonical 126-target `tuning126` endpoint, "mean built-chain Cα RMSD", from about 3.21 Å. The primary target is < 3.00 Å and the ambition is < 2.50 Å.
- The charter requires CVaR-VQE to be "the main research spine".
- Central question (§6): *"What objective and Hamiltonian should a CVaR-VQE optimize so that quantum optimization actually spends its limited information capacity on endpoint-relevant candidate selection?"*
- It mandates three S30 recommendations: §7A free-energy stage, §7B backbone-torsion channel and §7C sparse weighted readout.
- Other items it names:
  - candidate-index allocation and the 128→512 widening gate (§12);
  - FAIL18 (§13), which lists 18 PDB IDs;
  - a "new physical observable" whose error is incoherent with the pool common mode (§14);
  - the classical-reducibility burden (§11);
  - four open bug fixes (§20): the stale +0.113 Å docstring at `core/pipeline.py:821`, the projection seed, the governor/launcher gate, and the 128→512 gate.
- The charter's premise (§5E), quoted from S30: *"THE CIRCUIT CAN EXPRESS GOOD SOLUTIONS. THE CURRENT OBJECTIVE DOES NOT DIRECT THE OPTIMIZER TOWARD THEM"*. The supporting numbers are 0.2516 Å built chain under an ORACLE objective and 3.4330 Å under the deployed native-free objective.

**Contract** (`s31/S31_CONTRACT.md`) has 32 rules, each annotated with "the incident that paid for it". The following rules come up again later in this index:
- Rule 1: the endpoint is the built chain, 3.2105 Å. The CA cloud is 3.0483 Å and the set mean is 3.5507 Å.
- Rule 2: cloud→chain transfer is 0.92.
- Rule 3: MDE = 2.8016 × SE. Below 0.7× is "not a result" and 0.7–1.0× is "NOT MEASURED".
- Rule 6: ORACLE labels travel inside the sentence that carries the number.
- Rule 7: a control must match the operator's own space.
- Rule 12: a stratum defined by the outcome cannot measure the thing that defines it.
- Rule 19: pre-register the falsifier before the number exists.
- Rule 24: the main team may not approve its own positive.
- Rule 25: a withdrawal is a claim too.
- Rule 27: determine classical reducibility.
- Rule 29: "Incoherence with the pool's common mode" is the test. REPORT_S31 later says rule 29 is "inverted".
- Rule 31: no sub-0.01 Å chain claim until the projection seed is pinned.

**Running state:** `s31/STATE.md` (NOTES 1–15). **Ledger:** `s31/LEDGER.md` (S31-L0 … S31-L23). **Multiplicity register:** `s31/MULTIPLICITY.md`. **Verifier:** `s31/s31_verify.py`. The verifier's final count is "271 matched, 0 mismatched, 0 not-found, 0 flagged" per the REPORT header.

## Structure: lanes

The lanes below are listed in `s31/STATE.md` (LANES table) and `s31/LEDGER.md` S31-L0.

| lane | remit (as recorded) | main outputs |
|---|---|---|
| **A** | quantum/CVaR theory; verify R1; realised capacity; classical reducibility (§11) | `THEORY_A.md`, `PREREG_S31_A.md`, S31-L13, S31-L19 |
| **B** | free energy (§7A) and torsion (§7B), theoretical pre-check first | `PREREG_S31_B.md`, S31-L10 |
| **C** | readout design, sparse native-free support, index allocation, the 128→512 gate | `PREREG_S31_C.md`, S31-L5, S31-L14, S31-L15 |
| **D** | integrity: projection seed, `pipeline.py:821`, governor/launcher, verifier and multiplicity register | `PREREG_S31_D_branch.md`, S31-L6, S31-L7, S31-L8, `MULTIPLICITY.md` |
| **E** | "the incoherence hypothesis" (project out the common mode) | `PREREG_S31_E.md`, S31-L3, S31-L22 |
| **F** | terminal operator (MED / AVG_RG / AVG_SEP); later the per-target prefix length `m` | `PREREG_S31_F.md`, S31-L11, S31-L21, S31-L23 |
| **L** | literature (permanent lane) | `LIT_L.md`, S31-L4, S31-L9, S31-L12, S31-L16 |
| **P** | the `p*` substitution, which lane L called "the decisive experiment" | `PREREG_S31_P.md`, S31-L17, S31-L18, S31-L20 |
| **V** | the adversary (contract rule 24) | `AUDIT_V.md` (defects D0–D10, V-SELF) |

`REPORT_S31.md` §0.4 counts "Nine lanes, 24 ledger entries (S31-L0…L23), ten pre-registrations". STATE.md calls it "Eight lanes, the charter's maximum"; see the importer notes in LESSONS.md.

## Experiment and entry IDs (original terminology)

- **Ledger entries:** S31-L0 … S31-L23.
- **Theorems and claims:**
  - T1 (S30, the prefix theorem);
  - R1 (coordinator's readout-capacity claim, S31-L1);
  - A1 (closed-form minimiser), A2 (non-diagonal H does not make the order endogenous) and A3 (readout identity), all in THEORY_A;
  - G1 (S30 achiral theorem);
  - Lemma B1 and Corollaries B1 / B1′ (lane B).
- **Pre-registered clauses:**
  - lane A: A1-v, A1-e, A1-d, A3-i, A3-frame, A3-sign, A3-meb, A3-oracle;
  - lane B: F1–F3, G1-check, G2–G5, M0–M6;
  - lane C: F-C1a–d, F-C2a–c, F-C3a/b;
  - lane E: E1–E7;
  - lane F: F1 gates G0–G6, F2 tail strata T_POOL / T_BEST / T_CHAIN, F3-a–g;
  - lane P: arms A, A2, B–F; P1 = E−D, P2 = C−B, S3 = D−A;
  - lane D: PROD / B4 / ORACLE_B4;
  - lane V: V1 (matched-K) and V3 (AVG_SEP audit).
- **Arms and objects:**
  - PROD75, TOP128U, QVQE, BOLTZ, QPORACLE, MEB, CAL, GAM (lane A);
  - AVG, MED, AVG_RG, AVG_SEP (lane F);
  - index maps `score`, `gray`, `bisect`, `bisect_score`, `spectral`, `perm` (lane C);
  - `LEG_torsion`, `RAMA`, `HELIX_CONST`, `XTWIST`, `XTWABS` (lane B);
  - `bestm128`, `best1_top128`, `hull_top128`, `best1_pool` (S29 ladder rungs re-read here);
  - `mu`, `mu_hat`, `y`, `coh`.

## Verification machinery (as the sprint describes it)

- `s31/s31_verify.py` recomputes headline numbers from artefacts. It parses the sprint documents for every path they name, asserts MDE == 2.8016 × SE, and carries a cross-basis self-test added after lane V's defect D3. Its count grew during the sprint: 82 → 87 → 97 → 129 → 136 → 230 → 270 → 271 (STATE, AUDIT_V, LEDGER, REPORT).
- A sprint-wide multiplicity register with an adjusted-MDE table: k = 32 → 1.43×, k = 912 → 1.74×. The final running total is "k = 759 comparisons registered" as of 01:26 (`s31/MULTIPLICITY.md`).
- Adversarial audit by lane V (`s31/AUDIT_V.md`), with nine defects (D0–D10; D5 is process). Two are labelled SEVERE and headline-inverting: D0 (the 0.6931 coherence bar) and D10 (the AVG_SEP sign).

## Headline findings as the sprint stated them

All numbers below are copied as recorded. Basis and ORACLE/DEP labels follow the source.

1. **The endpoint did not move.**
   - **Measured:** production is 3.2105 Å built chain. No arm was deployed. "not one arm in the sprint reached its own MDE in the helpful direction" (`s31/REPORT_S31.md` §0, §17, §18).
   - **Interpretation:** both the primary (<3.00) and the ambitious (<2.50) targets are unmet.
2. **The CVaR-VQE Hamiltonian is a target-independent constant.**
   - **Measured:** `E = _zrank(pool["sc"][o])`. Max |E − ramp| is 0.0407 and the max between-target deviation is 0.0812. 125/126 targets have ties, with a mean of 9.56 tied positions. sd(H(p*)) is 1.4e-4 bits (REPORT §0.1, §5.1; S31-L17; AUDIT_V D6). Artefact: `s31/results/s31_V_zrank.json`, which confirms 0.0407 and 0.0812.
   - **Interpretation:** "The stage answers *'what fixed weight should rank `k` receive?'* — a 128-number global hyperparameter, not a per-target computation."
   - **Status:** the original "ZERO target-specific information" (S31-L17) was revised by lane V D6 to "target-independent to within a measured bound". The conclusion is unchanged.
3. **The deployed CVaR free energy is a convex program with a closed-form global minimiser**, the "hinged Gibbs" p*.
   - **Measured:** `run_cvar_vqe` is strictly worse on 126/126 targets at the deployed settings. p* takes 0.0012 s against 0.0985 s. Substituting p* is worth −0.0112 Å built chain at 0.19× MDE, a NULL (P1). The two selection readouts disagree on 66/126 targets (REPORT §0.1, §14.1–14.3; S31-L4, S31-L20; `s31/results/s31_P_substitute.json`: P1 effect −0.011204).
   - **Interpretation:** "Solving the objective exactly reshuffles the answer everywhere and buys nothing."
   - **Status:** confirmed. Lane L's "there is no third outcome" was falsified.
4. **"The bottleneck was stated backwards".** The source calls this the sprint's most consequential result. All values are ORACLE / NOT DEPLOYABLE, built chain.
   - **Measured:** correcting only the along-`mu` half gives −0.8102 Å (3.29× MDE, 5/5 folds, 121W/5L). Correcting only the orthogonal half gives +0.0747 Å (0.87× MDE, 57W/69L). The out-of-fold R² is +0.9403 for y_perp and −0.0051 for y_along. The source says this follows from the identity `mu_hat = mu − y` (REPORT §0.2, §20.1; S31-L22; `s31/results/s31_E2_applied.json`, `s31_E4_predictability.json`, `s31_E5_contrasts.json`).
   - **Interpretation:** "What can be predicted is the component ORTHOGONAL to the common mode, and it is harmful. What would help is the common mode itself, and it is unpredictable." REPORT says S30's slogan "survives verbatim; its mechanism was inverted".
   - **Status, as REPORT qualifies it:** "The controlled half of this result is the negative one". Against the shrink curve, the along arm is NOT MEASURED (0.94× and 0.64× MDE). About 42% of the raw −0.8848 along-vs-perp asymmetry is "generic geometry".
5. **The readout identity.**
   - **Measured:** `‖Σ w_x W_x − t‖² = ⟨w,a⟩ − ½ w'Bw` for any Σw = 1, verified to 1.66e-11. The native-free readout channel is "3.99% of the ORACLE cross term". Every native-free quality estimate has in-band skill that is "zero or the wrong sign": DIS −0.0262, CONS −0.2837 (REPORT §0.3, §3(ii–iii), §10.3, §20.2; S31-L13, S31-L14, S31-L19).
   - **Interpretation:** "the readout question and the ranking question are the same problem." What is missing is "a per-candidate quality estimate with positive IN-BAND skill."
6. **Thirteen directions closed, "most by theorem or by derivation before compute was spent"** (REPORT §0.3, §16). The list:
   - the free-energy stage and the elastic-network / normal-mode family;
   - non-diagonal Hamiltonians;
   - ADAPT-VQE;
   - the torsion channel;
   - charter §14 "by provenance" (92.9% of the benchmark is NMR-determined);
   - index redesign;
   - the per-target prefix length `m`;
   - the constrained-affine readout;
   - consensus as a quality estimate;
   - E1;
   - E2/E3.
7. **Instrument findings.**
   - **Measured:** the projection has "no seed". It is "deterministic and chaotic", with amplification about 1e13. 73/126 targets have their branch chosen at a margin below 1e-6 (S31-L6; `s31/results/s31_D_projection_pin.json`: max shift 0.5113 Å, median margin 3.11e-7). The per-target built-chain floor, measured as the same operator written twice, is 0.0134 mean, 0.0329 p90 and 0.2285 max (S31-L18).
8. **Process meta-finding.**
   - **Measured:** "Every single-lane result held. Every cross-lane synthesis of mine failed". This was four for four before the adversary, then eleven more defects, four of them severe (REPORT §0.4; STATE NOTE 13; S31-L16). Six of the ten pre-registered predictions went against the lane that wrote them, three of them the coordinator's.
9. **Next-sprint recommendation** (REPORT §21): "Find a source of information about the POOL'S COMMON MODE … that does not come from the pool." The parallel requirement is "a per-candidate quality estimate with positive in-band skill"; the report asks that every proposal "State which of the two any proposal addresses."

## Glossary of original terminology

- **built chain / CA point cloud / set mean:** three different endpoint objects (3.2105 / 3.0483 / 3.5507 Å). The contract says: "State the basis in the same sentence as the number."
- **ORACLE / NOT DEPLOYABLE:** uses the native. **native-free / DEPLOYABLE:** no native at inference. "ORACLE-ADJACENT" marks a threshold that touches the native (lane F gates G1, G3τ).
- **MDE** = 2.8016 × SE. "NOT A RESULT" means below 0.7× MDE; "NOT MEASURED" means 0.7–1.0×; "MEASURED" means ≥ 1.0×.
- **T1:** S30 theorem: for diagonal H the CVaR tail is a prefix of the induced order, so the state specifies "one integer".
- **R1:** the coordinator's readout ceiling claim (S31-L1). It was restated three times; the final form is "the SELECTION readout's alphabet is the number of distinct candidates — 6.886 bits mean, 6.555 worst".
- **three readouts:** *selection* (`consensus_medoid`, `core/pipeline.py:795-803`, diagnostic arm), *convex* (`average_weighted`, `:880-895`, SHIPPED) and *affine* (`s27/s28_A_amp.py:105-117`, harness only).
- **hinged Gibbs distribution:** `p*_i ∝ exp((s* − E_i)_+/(αT))`, the closed-form minimiser of `F(p) = CVaR_α(E;p) − T·H(p)`.
- **`mu` / `y` / `mu_hat`:** the pool's common-mode pair error / the prior (distogram) error / `pool75_mean − expected`. The identity is `mu_hat = mu − y` "EXACTLY".
- **along-mu / perp-mu:** the components of the ORACLE correction `y` parallel and orthogonal to `mu`.
- **coh:** within-target corr(error, mu). S30's `coh` grades a corrector's residual. Lane B and lane F's `coh` grades emitted readout error. These are two different objects (0.6931 vs 0.9780 for production).
- **G1:** S30 theorem that any rotation-, translation- and reflection-invariant single-structure observable is a function of the distance map.
- **T_even / T_odd:** reflection-invariant and reflection-anti-invariant halves of a torsion observable.
- **FAIL18:** the 18 targets defined by the filter's own recall (`s12/instrument.py:271-278`). **defn18** is the top-18 by widening gain and equals FAIL18 exactly. **worst18_poolmean / worst18_bestpool / T_POOL / T_BEST / T_CHAIN** are filter-independent or outcome-defined strata. REPORT Appendix B is the key: "five different strata are called 'the worst 18'".
- **bestm128:** per-target ORACLE best prefix length over the top-128. It equals 2.9027 Å built chain and is called "a best-of-K order statistic".
- **A2 null:** the same operator written in two implementations (`average_weighted(uniform, top-75)` vs `coordinate_average`). It is the implementation-noise null.
- **B4:** carry all four λ=0 projection branches to λ=0.3 and take the argmin. It is a "conditioning fix, 1082×, with a null accuracy effect".
- **MEB:** `argmax_Δ ½w'Bw`, the quality-blind, dispersion-maximising readout.
- **"a number carries its definition, not just its value":** the sprint's name for the pattern behind its defects.
- **"operator-consumes-set-mean", "grid-oracles-are-order-statistics", "consensus-is-outlier-avoidance", "in-band-is-the-only-ranking-metric", "control-at-the-decisive-step":** project memory labels cited in the source.

## Source files read (complete list)

Every tracked `.md` from `git ls-files s31` was read in full:

1. `s31/AUDIT_V.md`
2. `s31/BRIEF.md`
3. `s31/LEDGER.md` (3,559 lines)
4. `s31/LIT_L.md`
5. `s31/MULTIPLICITY.md`
6. `s31/PREREG_S31_A.md`
7. `s31/PREREG_S31_B.md`
8. `s31/PREREG_S31_C.md`
9. `s31/PREREG_S31_D_branch.md`
10. `s31/PREREG_S31_E.md`
11. `s31/PREREG_S31_F.md`
12. `s31/PREREG_S31_P.md`
13. `s31/REPORT_S31.md` (1,519 lines)
14. `s31/S31_CONTRACT.md`
15. `s31/STATE.md`
16. `s31/THEORY_A.md`

I opened the following result JSONs only to confirm the headline values cited, by searching their keys: `s31/results/s31_P_substitute.json`, `s31_E2_applied.json`, `s31_E5_applied.json`, `s31_E5_contrasts.json`, `s31_E4_predictability.json`, `s31_E1_direction.json`, `s31_V_avgsep.json`, `s31_V_orderstat.json`, `s31_V_zrank.json`, `s31_D_branch.json`, `s31_D_projection_pin.json`, `s31_C_widen.json`, `s31_C_ladder.json`, `s31_C_index.json`, `s31_A_readout.json`, `s31_A_r1.json`, `s31_A_cap.json`, `s31_A_ahat.json`, `s31_A_setweights.json`, `s31_B1_achirality.json`, `s31_B2_inpool.json`, `s31_F3_chain.json`, `s31_F3_prefix.json`, `s31_F_analyse.json`, `s31_F_coh.json`.

I searched `docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` for Sprint 31 material and found none; see the importer notes in LESSONS.md.
