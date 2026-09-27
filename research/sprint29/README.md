_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s29/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 29 — "CVaR-VQE protein folding: find the path below 2.5 Å" (evidence index)

## Source pin

- **Repository:** `C:\Users\abena\cvar-vqe-protein-folding-v3`, commit `3d5b2d25b718346401268634da275f4d7e9fcf3f` (read-only).
- **Sprint directory:** `s29/` (199 tracked files: 18 `.md` read by this importer, 9 `PREREG_*.md`, 8 `briefs/*.md`, 9 `lit/*.md`, 1 `REPORT_S29.html`, 27 `.py` scripts, and result JSON/JSONL/TXT under `s29/results/`).
- **The sprint's own original location:** `s29/S29_CONTRACT.md` says the work ran in repository `C:\Users\abena\Protein-Folding-Algorithm`, branch `s26`, under `s29/`; production code frozen at `a15406c`.
- **Dates:** charter received 2026-09-19 (`s29/BRIEF.md`); ledger S29-L0 at 2026-09-19 23:35; first close 2026-09-20 03:56; final close (after lane P's S29-L57) 2026-09-20 09:15 Pacific (`s29/REPORT_S29.md`, `s29/STATE.md`, `s29/STATUS.md`).

## The sprint's question, contract and brief

- **Charter** (`s29/BRIEF.md`, the user's text verbatim): "Reduce the real built-chain mean Cα RMSD as much as scientifically possible, with the CVaR-VQE remaining the central component of the system." Production ≈ 3.21 Å built chain on the 126-target instrument; aspirational target "< 2.5 Å"; "< 3.0 Å would already be meaningful movement". One hard constraint: "CVaR-VQE remains the main scientific object, not a decorative final stage" — "Removing or randomizing the quantum stage measurably degrades the result." Charter §11 requires, for every serious quantum formulation, nine questions and ten controls (classical equivalent, diagonalised equivalent, permuted, random, matched budget, untrained circuit, simpler ansatz, order-statistic, product-state restriction, second seed). Charter §4 lists S28 findings 1–11 that every hypothesis must engage (notably finding 8, recognition failure, and finding 11, ~68% common-mode error).
- **Contract** (`s29/S29_CONTRACT.md`): inherits S28's 12 non-negotiables (never open benchmark60; built chain is the reporting basis; `s24.stats_lib.compare`, fold-clustered CI decides; "below 0.7x MDE is NOT A RESULT"; pre-register falsifiers; ORACLE labelled in the same sentence; "no quantum advantage claim; an exact simulator is never a cause"). Adds rules 13–19 (findings engaged per hypothesis; information test for literature imports; nine questions/ten controls; 12-target probe before any 126-target run; multiplicity; mechanism beside outcome; the lane-D cost-RMSD meter). Five mid-sprint addenda (rules 20–30): the shrink rule (20, later re-justified by addendum 5), marginal-class bound (21), perception-distortion bound (22), averaging bound (23), flat-minimiser clause (24), "contraction is Jensen, not the posterior" (25), "the bound does not license dismissing a measurement" (26), chronology as evidence (27), commit by pathspec (28), ledger heading authoritative over commit message (29), rule 20's justification withdrawn (30).
- **Endpoint:** mean built-chain Cα RMSD over 126 dev targets (9–16 aa). Production anchor quoted as **3.2126 Å** (`s27/results/chain_rows.jsonl :: DIS`) in the contract/data path and **3.2105 Å** when production is re-projected in S29 jobs; point cloud 3.0483 Å. The 0.002 Å gap is attributed in source to the multi-start projection's "branch-flip floor" (S29-L20, S29-L54).

## Structure: lanes, experiments, verification

Eight lanes (charter max 8), per `s29/REPORT_S29.md` §1 and `s29/STATE.md`:

| lane | remit (as stated in source) | ledger entries |
|---|---|---|
| L | literature, permanent | S29-L1, L8, L12, L13, L14, L16, L19, L31, L42 |
| T | theory, permanent (`THEORY.md`, `THEORY_SUMMARY.md`) | S29-L7, L11, L15, L17, L18, L23, L24, L29, L32, L39, L40, L41, L50 |
| D | adversary (permanent), the cost–RMSD meter, test suite | S29-L2–L6, L10, L26, L28, L33–L35, L37, L38, L52, L55 |
| M | data path, convenience choices, harness audit; then F1 and F2 | S29-L9, L51, L53 |
| O | ORACLE ceiling ladder; typicality-axis probe (H1) | S29-L20, L21, L30, L47 |
| X | divergent: configuration-space ("chimera") CVaR-VQE | S29-L56 |
| P | the projection stage's price | S29-L22, L57 |
| B | compatibility Hamiltonian; tail-then-aggregate CVaR | S29-L25, L27, L36, L45, L49, L54 |
| coordinator | STATE, report, audits | S29-L0, L44 (+3 addenda), L46 (+addendum), L48 |

- Ledger: `s29/LEDGER.md`, S29-L0 … S29-L57, **no S29-L43** (numbering note in ledger at line 3860).
- Hypotheses carried in `s29/STATE.md`: **H1** (typicality axis; falsified S29-L20), **H0** (ceiling = absence of per-target information orthogonal to typicality; became leading hypothesis), **H2** (divergent: pool is the wrong state space; lane X; closed negatively S29-L56).
- Pre-registrations: `PREREG_S29_{B,D_band,D_m6,M_F1,M_F2,O,P,T,X}.md` (read by a second importer; summarised with outcome status in the last section of this file).
- Verification (`s29/REPORT_S29.md` header, §4.6; S29-L46 + addendum; S29-L48): `s29/s29_audit_paths.py` — **205 of 217** ledger-cited paths resolve, 12 itemised, 1 genuinely dangling (`s7/debias_tune.json`); `s29/s29_verify_report.py` — **58 of 58** headline numbers recomputed from artefacts, 0 mismatches. Test suite: light run 17 files, 378 passed / 3 skipped / 0 failed (S29-L5); heavy files pipeline 35 passed / 2 skipped, integration+equivalence (VERIFY_SLOW=1) 39 passed, amber 16 passed, amber_frame_invariance 3 passed (S29-L52, S29-L55).
- Harness audit (lane M, `s29/s29_M_harness_audit.md`, S29-L9): nine checks, all PASS; one declared non-bit-exactness of the s12 distogram cache (score order differs on 2/126, top-75 set on 0/126, RMSD 0.00e+00 on 126/126).

## Headline findings as the sprint stated them

### 1. The endpoint did not move
- **Measured:** production 3.2105 Å built chain (median 2.9661, sd 1.7290, SE 0.1540, p90 5.6060, max 8.2406), point cloud 3.0483; projection price +0.1622; 50.8% of targets < 3.0 Å, 34.9% < 2.5 Å (`s29/REPORT_S29.md` §7, §7.1).
- **Interpretation:** "Nothing deployable changed, and that is a result rather than an absence of one." (`REPORT_S29.md` §2). "The mean is a tail statistic" (§7.1).
- **Status:** final. Leakage: production is DEP (deployable).

### 2. The achievable native-free bound (S29-L23, attacked in S29-L35/L52)
- **Measured:** identity `RMSD_new = RMSD_prod · √(1 − ρ²)`; 3.00 Å needs ρ = 0.358, 2.50 Å needs 0.628 vs random-shape reference 0.1398. 21 native-free displacement fields (`s29/results/s29_D_fields.json`, n = 126): best signed mean cosine CHAN_DISTPOT +0.1128 [+0.088, +0.137] fold CI; `beats_random_reference` False on all 21; best ORACLE-stepped gain 0.0195 ± 0.001 Å on the point cloud. Per-target |cos| 0.251–0.325 on every field → with an ORACLE per-target sign, 2.708 Å (EXPAND) point cloud.
- **Interpretation:** "no native-free operator over the present information reaches below about 3.18 A on the built chain" (S29-L23); bound levels ≥ 3.210 / ≥ 3.181 / ≥ 2.98 Å (`THEORY_SUMMARY.md` §1). REPORT §0/§12.0 scopes it: "the bound's measured half stands while its universal half does not" after S29-L50.
- **Status:** "survived attack" (S29-L35); assumption B2 load-bearing; universal form not established (S29-L50). All cosines ORACLE diagnostics.

### 3. The architectural ceiling (S29-L30 → corrected S29-L44 → final S29-L44 addendum 3 / S29-L47)
- **Measured:** best prefix-m average over the top-128 (the CVaR tail's reachable set), ORACLE per-target m: **2.9027 Å** built chain vs production 3.2105, −0.3079, MDE 0.0982, 3.14× MDE, fold CI [−0.3625, −0.2499], 117W/9L, n = 126 (`s29/results/s29_O_headline_contrasts.json`, verified). Best single member of the same 128: 2.1435 (−0.7592 vs prefix average, 4.18× MDE). Top-128 hull 1.8538; K=500 hull 1.1235 ("expressiveness, not ceilings").
- **Interpretation:** "The charter's 2.5 Å is therefore unreachable through this architecture *even with an oracle*" (REPORT §0). "Choosing *m* and choosing *which member* cost the **same 7 bits** and are worth −0.3079 and −1.0670 against production."
- **Status:** ORACLE; originally quoted on the point cloud (2.7605) and corrected (see NEGATIVE_RESULTS / retractions).

### 4. The deployed quantum stage is endpoint-equivalent to a fixed profile (S29-L15, L26, L55)
- **Measured:** deployed CVaR-VQE arm 3.2187 Å built chain vs fixed target-independent prefix m = 75 3.2105: −0.0082 Å, 0.27× MDE, fold CI [−0.0310, +0.0098], NOT MEASURED; structure-level equality 42/126 within the 0.006 Å floor (`s29/results/s29_D_m6_chain_seed0.json`, verified −0.00817, −0.266×).
- **Interpretation:** "THE DEPLOYED QUANTUM STAGE CONTRIBUTES NOTHING MEASURABLE AT THE ENDPOINT THAT A SINGLE TARGET-INDEPENDENT NUMBER DOES NOT" (S29-L55).
- **Status:** confirmed as endpoint statement; F-M6a (structure-level) failed.

### 5. Set-equality fails under a free subset optimisation, and buys nothing (S29-L25, L45, L54)
- **Measured:** exhaustive over C(500,2) = 124,750 pairs, 126 targets: f-optimal pair non-prefix 114/126, m=5 subset non-prefix 124/126, per-state sort finds optimum 12/126. m=5 subset vs production +0.2451 (1.45×, WORSE), of which non-prefix choice +0.0804 (0.73×, NOT MEASURED). VQE endpoint: λ=1 +0.104/+0.116 Å (0.95×/1.03×), F5b REFUTED.
- **Interpretation:** "the escape is real and ubiquitous *under search*, the deployed circuit does not take it, and where it is taken it buys nothing measurable" (REPORT §4.2).
- **Status:** mechanism confirmed (lane D reproduced, S29-L38); endpoint refuted. ORACLE evaluation of native-free selections.

### 6. Recognition "closed three independent ways" (REPORT §9.1)
Perception–distortion theorem (S29-L12, literature), within-band measurement F2 fails on 58/70 (S29-L33), Neyman–Scott incidental parameter (S29-L31, literature).

### 7. What stayed open (REPORT §12, §13)
LEG_torsion and 8 other non-compactness in-band channels (S29-L50); a sparse weighted readout (S29-L47); a genuinely new information channel; the S8 free-energy stage (does not exist on disk or in git — rebuild required, S29-L41/L42).

## Glossary of original terminology (as used in source)

- **DEP / deployable** vs **ORACLE**: ORACLE = any quantity computed from the native; "no native quantity chooses a deployable parameter" (contract rule 4).
- **built chain** / **point cloud**: endpoint (ideal-geometry projected chain) vs diagnostic coordinate average.
- **NOT MEASURED**: `ST.compare` verdict when |effect| ≤ own MDE; "below 0.7x MDE is not a result"; 0.7–1.3× = "Type-M zone".
- **MDE** = 2.8016 × SE, per comparison; **fold CI** = cluster bootstrap over 5 pinned folds.
- **FAIL18 / the 108**: ORACLE partition of the 126 (18 zero-recall targets) (`CONVENIENCE_CHOICES.md` C8).
- **set-equality theorem**: the CVaR tail's support is a prefix of the energy order; identified as Barkoutsos et al. eq (12) (S29-L13).
- **tail-then-aggregate (TTA)**: CVaR over the tail's own coordinate average `R_α(p)` (THEORY §4).
- **M6 / fixed-profile control**: the target-independent rank-weight profile p*(α,T) replacing the whole quantum stage (S29-L15).
- **the bound / B1–B4**: S29-L23 displacement bound and its assumptions; **B2** = ρ_max ≤ 0.14 for any field from present information ("LOAD-BEARING").
- **class M / theorem 2 / corollaries 2a–2c**: marginal-objective class and its informativeness theorem (THEORY §2).
- **incidental parameter**: Neyman–Scott 1948, the per-target sign (S29-L31).
- **the meter**: lane D's cost–RMSD meter (`s29/s29_D_cost_audit.py`), four numbers (ladder ρ, gradient cosine, native percentile, preference), plus shrink signature.
- **shrink twin / RSHRINK / SWAPCTL / CTRL-RAND / FLOOR**: zero-information and floor controls (S29-L51, L53, L57).
- **chimera**: lane X's basis state (segments' torsions from one of 8 retrieved parents).
- **stable rank law**: Var[∂F/∂θ] ≈ r_stable/D² (S29-L11).
- **readout slack**, **lateral motion**, **separation-dependent shear**, **7 bits**, **operator consumes set mean** (`d_out = 1.16·d_set_mean + 0.04·d_set_best`, R² 0.89).
- **rung** (lane O ladder rungs 1–9), **H0/H1/H2**, **F1/F2** (lane M assignments; also lane D/T falsifier labels — context-dependent).

## Source files read by this importer (complete)

`s29/BRIEF.md`, `s29/CONVENIENCE_CHOICES.md`, `s29/DATAPATH.md`, `s29/LEDGER.md` (all 5,823 lines), `s29/REPORT_S29.md`, `s29/RETRACTIONS_S29.md`, `s29/S29_CONTRACT.md`, `s29/STATE.md`, `s29/STATUS.md`, `s29/THEORY.md`, `s29/THEORY_SUMMARY.md`, `s29/s29_B_FINDINGS.md`, `s29/s29_D_FINDINGS.md`, `s29/s29_L_FINDINGS.md`, `s29/s29_M_FINDINGS.md`, `s29/s29_M_harness_audit.md`, `s29/s29_O_FINDINGS.md`, `s29/s29_P_FINDINGS.md`, `s29/s29_X_FINDINGS.md` (18 files). Result artefacts opened to confirm headline values: `s29/results/s29_O_headline_contrasts.json`, `s29_D_fields.json`, `s29_M_F1_summary.json`, `s29_D_m6_chain_seed0.json`, `s29_P_summary.json`, `s29_M_F2_supply.json`, `s29_M_F2_gate.json`, `s29_T_compactness.json`, `s29_X_probe.json`, `s29_X_bestofn.json`, `s29_X_bestofn_fmt.txt`, `s29_B_tta_end_cloud.json`. The 26 excluded files (`s29/PREREG_S29_*.md` ×9, `s29/briefs/*.md` ×8, `s29/lit/*.md` ×9) were read by a second importer and integrated from its digest; `git log` of `s29/PREREG_S29_B.md` and grep of `PREREG_S29_P.md`, `briefs/S29P.md`, `lit/L_3_decision_theory.md` were checked by this importer for the flagged discrepancies. Also searched `docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` for Sprint 29 passages (none found; see LESSONS.md importer notes).

## Pre-registration, brief and literature evidence

_Integrated 2026-09-26 from a second importer's reading of `s29/PREREG_S29_*.md`, `s29/briefs/*.md` and `s29/lit/*.md`. None of the nine preregs records its own final outcome; the "status in source" column is taken from the ledger and FINDINGS files as cited._

### Pre-registrations (9)

| prereg | registered (as stated in file) | what it registered | status in source (outcome entry) |
|---|---|---|---|
| `s29/PREREG_S29_O.md` | 2026-09-19 23:43 | ORACLE ladder rungs 1–7; rung 6 = H1 typicality-axis probe (F6a cosine, F6b LFO step; prior: both fire); 4 endpoint comparisons | Rung 6 **falsified on both clauses** (S29-L20); rung 8 (added) ORACLE global η = 0 (S29-L21); rung 9 (added) LFO prefix +0.0079 (S29-L30); full ladder S29-L47 (`s29_O_FINDINGS.md`) |
| `s29/PREREG_S29_X.md` | 2026-09-19 23:50; addenda 00:10, 00:35, one undated | chimera configuration-space CVaR-VQE; D1 (vs scrambled null after A1), P1 (GO only at ≤ −0.7× MDE; prior WORSE 0.1–0.4 Å), P2–P5; A2 adds lane T's gate ladder (TV > 0.45, SA main comparison); A3 adds BESTOFN | **Closed negatively**: P1 +0.4572 (1.18×, WORSE), GO fires backwards; D1 branch (b) fires (S29-L56; `s29_X_FINDINGS.md`) |
| `s29/PREREG_S29_B.md` | header 00:10; addenda A1 00:09, A2 00:33, A3 01:20 | M1 bright line B1; M2 exact-ground-state gate (prior: does not open); M3 endpoint only if gate opens; A2 adds TTA measurement 5 (F5a mechanism, F5b endpoint, F5c greedy subset); A3 runs the 126 unconditionally | B1 **REFUTED** (A1 / S29-L36); M2 gate **not opened** (S29-L49); M3 **not run**; F5c clause 1 confirmed / clause 2 did not fail (S29-L25, L45); F5b **REFUTED** (S29-L54) |
| `s29/PREREG_S29_P.md` | 00:10; addenda A1–A6 00:12–01:15 | BOND/SPAN/ISO vs PROD and vs CTRL-RAND mean-of-8 (F-P1/F-P2/F-P3); prior null 0.0–0.3× MDE; A4 wider multi-start MS-OBJ; A5 chronology; A6 incidental-parameter reading rule | **Refuted; all falsifiers fail to fire**; BOND 0.03× from CTRL-RAND, +0.7222 vs PROD; MS-OBJ and ORACLE grid deferred, not run (S29-L22, S29-L57; `s29_P_FINDINGS.md`) |
| `s29/PREREG_S29_M_F1.md` | 00:1x; addendum 1 00:2x | LOG vs PROD (primary; result requires < 0, > 1.0× MDE, fold CI excl. 0, ≥ 4/5); SWAPCTL (A1); prior null-to-worse +0.00–0.10 Å; A1 withdraws contraction mechanism | **NOT A RESULT**: +0.0822 (0.55×); LOG − SWAPCTL +0.0202 (0.14×) (S29-L51) |
| `s29/PREREG_S29_D_band.md` | 00:28; addendum 1 00:36 (+ addendum 2 per S29-L33) | within-realism-band ordering; F1 (any scorer in-band > 0), F2 (in-band > across); prior F1 does not fire | **F1 fires (50/70), F2 fails (58/70)** — "not a recognition result" (S29-L33) |
| `s29/PREREG_S29_D_m6.md` | 00:44 | fixed-profile control; F-M6a (≥ 120/126 within floor), F-M6b (deployed vs best profile clears 0.7×), F-M6c (quantum contribution); 2 endpoint comparisons | F-M6a **fails** (43/126 cloud, 42/126 chain); F-M6b **does not fire** (−0.0097 cloud 0.43×; −0.0082 chain 0.27×); F-M6c does not fire (S29-L26, S29-L55) |
| `s29/PREREG_S29_M_F2.md` | 00:5x; addenda 02:2x, 02:3x, 02:4x | native-free shell-profile ratio vs B2 (cos > 0.140 AND beat shrink twin); stopping rule; bits currency | **Class closed on a measured supply gap**; stopping rule fired, no projections (S29-L53) |
| `s29/PREREG_S29_T.md` | undated in text; committed 02:13:31 per REPORT §12.0 / S29-L50 | compactness loading of 32 channels; F1 (objection confirmed; row 3 closes), F2 (row 3 stays open); prior F1 at ~3:1 | **F1 fails, F2 fires** (repaired); row 3 stays open (S29-L50) |

### Briefs (8)
`s29/briefs/S29{B,D,L,M,O,P,T,X}.md` set each lane's question and plan as summarised in the lane table above. Notable brief-level items: S29B's gate constant 2.954 (the S10-5 ORACLE ladder figure from another pool era) was corrected in `PREREG_S29_B.md` to a paired per-target comparator (3.048338 over 126; 3.252928 over 12); S29D required the meter to reproduce S28's −0.40 / −0.034 / 36.9 / 0.071 / 0.206; S29P and PREREG_P quote the projection price as +0.159 Å (see LESSONS importer notes); S29T specified the seven THEORY.md sections, each ending in a checkable prediction; S29X's prior: "ties the pool on the point cloud, worse on the built chain … SA control ties the VQE".

### Literature (`s29/lit/L_1` … `L_8`, `L_INDEX.md`)
Eight topics, verdicts per paper (KEPT/REJECTED/NOTED/RECORDED), mirrored in ledger entries S29-L1, L8, L12, L13, L14, L16, L19, L31 and correction S29-L42. `L_INDEX.md` tallies: T1 15 entries (4 KEPT, 11 REJECTED); T2 9 (4/5); T3 6 (5 KEPT, 2 REJECTED); T4 9 (7 KEPT, 1 NOTED); T5 6 (not tallied); T6 9 (7 KEPT, 1 NOTED); T7 10 (5 KEPT, 1 NOTED, 4 RECORDED, 2 REJECTED); T8 10 (2 KEPT, 1 available-in-principle, 5 RECORDED, 3 REJECTED). Load-bearing imports: Barkoutsos et al. eq (12); Blau & Michaeli 2018 Thm 3; Neyman & Scott 1948; Krogh–Vedelsby / Ueda–Nakano (Brown, Wyatt & Tiňo 2005 eqs 9–10); McDonald et al. 2023; Cerezo et al. 2025 (arXiv:2312.09121). The S8 free-energy "resumable" claim in `L_1` §8.3 and `L_7` §(c) is annotated in place as lane L's error (S29-L42).
