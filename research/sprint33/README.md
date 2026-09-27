_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s33/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 33 (S33): evidence index

## 1. Source pin

| item | value |
|---|---|
| repository | `C:\Users\abena\cvar-vqe-protein-folding-v3` (predecessor repo, read-only) |
| commit | `3d5b2d25b718346401268634da275f4d7e9fcf3f` |
| sprint directory | `s33/` (10,543 tracked files; this import covers the tracked `.md` files listed in §8) |
| sprint's own branch / commits (as the source states them) | branch `s26`; base `cd9671e3`; final-numbers commit `5a737e98`; latest checkpoint `d2c0fc75` (`s33/REPORT_S33.md` header) |
| sprint status (as the source states it) | "FINAL, 2026-09-26"; only E812 (A80 on tuning126, 84/126) still running at close (`s33/REPORT_S33.md` header; `s33/STATE.md`) |
| authoritative sources named by the sprint | `s33/LEDGER.md` "is authoritative"; `s33/LEDGER_CONSOLIDATED.md` "Nothing here supersedes `s33/LEDGER.md`" (`s33/REPORT_S33.md`; `s33/LEDGER_CONSOLIDATED.md`) |

Import scope of this file set (part A of 2): `s33/*.md`, `s33/ARCHITECTURES/*.md`, `s33/RESULTS/**.md`, `s33/VERIFICATION/final/*.md`, plus a search of the top-level `docs/FINDINGS.md` and `docs/CONDENSED_REPORT.md` for Sprint 33 passages (none found; see §8). `s33/LANES/**` and `s33/VERIFICATION/attack_*/**` were imported by a second agent and integrated in "Lane and attack evidence".

## 2. The sprint's own question / contract

- Charter: `s33/BRIEF.md`, "S33 DECISIVE RESEARCH SPRINT — OPUS 5.5 ULTRACODE — MAXIMUM FREEDOM / MAXIMUM EXPERIMENTATION / RMSD-FIRST", 62 sections. The user's closing words: "Many agents many jobs, max experiment and change, bring that rmsd way down." (`s33/BRIEF.md`).
- "SACRED: the system must remain protein folding centred on CVaR-VQE with a meaningful (non-cosmetic) quantum role. Nothing else is sacred" (`s33/BRIEF.md` §2).
- Targets: baseline 3.2105 Å; target < 3.00; ambition < 2.50 (`s33/BRIEF.md` §3).
- Leakage control: every experiment declares DEPLOYABLE or ORACLE; no native structure in deployment (`s33/BRIEF.md` §27).
- Early-kill rules (§49), survival rule "new mechanism AND new information flow AND credible deployment path AND measured improvement" (§50); before declaring done: "does the quantum component change the answer" (§59); 20 final questions (§60) (`s33/BRIEF.md`).
- Endpoint (unchanged from S32): mean built-chain Cα RMSD on `tuning126` (n = 126), production = 3.2105 Å (λ=0.3 re-projection of `s29/results/s29_O_structs/<pdb>.npz["prod"]`). Secondary instrument `long40` (45 targets, 44–60 aa), production-analogue avg75 = 9.7450 Å. "The two are reported separately and never pooled." (`s33/STATE.md`).
- Statistical contract (S32 contract, `s33/harness.py compare`): effect = new − reference (negative better); x = |effect|/MDE, MDE = 2.8016·SE; < 0.7x NOT A RESULT; 0.7–1.0x NOT MEASURED; RESULT needs ≥ 1.0x, fold CI excluding 0 and ≥ 4/5 folds; 1.0–1.3x "type-M zone" (`s33/REPORT_S33.md` conventions).
- Tags: `value (basis · instrument · E-id · DEP|ORC)`; DEP = "no native structure anywhere upstream of scoring"; ORC = ORACLE. Bases: chain (endpoint), cloud (diagnostic), energy (native-free objective, no RMSD) (`s33/REPORT_S33.md` conventions).

## 3. Structure

### 3.1 Instruments (`s33/REPORT_S33.md` conventions)

| instrument | targets | length | reference |
|---|---|---|---|
| `tuning126` (PRIMARY) | 126 | 9–16 aa | production 3.2105 |
| `mid30` (built and frozen in S33 by E600, 2026-09-25T10:21:16Z) | 41 | 25–40 aa | avg75 8.180 |
| `long40` (S32 folds) | 45 | 44–60 aa | avg75 9.745 |

Phase-1 incumbent (E001-ESM, ESM-2 contact-agreement top-5 average): long40 7.231 (gated 7.018), mid30 7.815 (`s33/REPORT_S33.md`).

### 3.2 Phases (`s33/REPORT_S33.md` §4)

| phase | agents / lanes | output |
|---|---|---|
| 1. Map, harness, engine (01:47–03:09, 2026-09-25) | map-pipeline, map-quantum, map-learned, map-long, map-history, QENG, HARNESS, coordinator | `s33/MAP_*.md`, `s33/FALSIFICATION_CATALOGUE.md`, `s33/harness.py`, `s33/qengine.py` (43 tests), E000–E003 |
| 2. Six competing lanes (03:10–~10:25) | S_mosaic (E1xx, A10–A12), F_fragment (E2xx, A20–A21), C_contact (E3xx, A30–A34), P_prior (E4xx, A40–A41), X_short (E5xx, A50–A56), M_mid (E6xx, A60–A62) | 22 architecture IDs; mid30 frozen; esmprior_v1 published 07:10 |
| 3. Lane adversaries (~08:10–13:30) | one per Phase-2 lane | `VERIFICATION/attack_<lane>/ATTACK_REPORT.md` (F report is a draft) |
| 4. Decisive lanes (08:35–14:40; jobs ran overnight) | D_decoder (E8xx, A80–A82), Y_synth (E9xx, A90–A91), T_tempered (E7xx, A70–A72), H_hybrid (E10xx, A100–A101) + adversaries | load-bearing quantum tests; final clean composite |
| Final verification | FINAL_V (E308 reproduction, leakage, census); close-out (report + narrow A80 adversary) | `s33/VERIFICATION/final/`, `attack_D_decoder_final/` |

A weekly usage limit stopped several agents at ~14:40 on 2026-09-25; governed jobs completed overnight and were scored 2026-09-26 (`s33/REPORT_S33.md` §31).

### 3.3 Architectures

36 IDs (A00–A101); per-ID status in `s33/ARCHITECTURES/INDEX.md`. Families (`s33/REPORT_S33.md` §4): (1) structural CVaR-VQE registers (A10, A11, A60, A70/A71 registers, A20, A21, A30, A32–A34, A41, A53, A81/A81m, A82, A100); (2) learned priors and selectors (A40 esmprior_v1, A50, A54, A55, A61, A62); (3) decoders (A12, A31/A31.2, A80); (4) distribution readouts (A33, A70, A71); (5) compositions (A90, A91, A100, A101); (6) short-length nulls/transfers (A51, A52, A54, A55, A56, E105, E230, E504a). `s33/ARCHITECTURES/QENGINE.md` documents the shared engine (infrastructure, not an architecture).

### 3.4 Verification

- Lane adversaries (Phase 3/4), FINAL_V census (`s33/VERIFICATION/final/CLAIM_CENSUS.md`: K = 101 long40 / 23 mid30 / 13 tuning126 candidate arms, 185-row `ARM_CENSUS.csv`) and quantum census (`s33/VERIFICATION/final/QUANTUM_CONTRASTS.md`: 34 chain-level rows).
- Same-job sentinel re-projection of production in every run (bit-identity licensing; "contract rule 20") (`s33/REPORT_S33.md` §2, §22).

## 4. Headline findings as the sprint stated them

Each item: **Measured** / **Original interpretation** / **Status in source**. Leakage labels as the source gives them.

### H1. tuning126 (primary endpoint) did not move
- **Measured:** production A00 3.2105 (chain · tuning126 · E000 · DEP), SE 0.154, bit-identical re-projection 126/126 (`s33/RESULTS/E000_baseline/run_tuning126/RESULT_E000_baseline_run_tuning126.md`; `s33/LEDGER.md` E000). 13 candidate arms; best challenger E501 (A50 attention prior) 3.2288, +0.018, SE 0.055, 0.12x, fold CI [−0.066, +0.100], W/L 66/60; Westfall-Young p 0.99 (`s33/RESULTS/E501_prior_attn/RESULT_E501_prior_attn.md`; `s33/VERIFICATION/final/CLAIM_CENSUS.md` §2).
- **Original interpretation:** "At 9–16 aa no native-free channel carries nonlocal pair information: ESM-2's within-separation ρ is −0.12, against −0.34 at 55 aa"; "Reaching 3.00 would need about 0.16 nats/pair of native-directed prior information" (`s33/REPORT_S33.md` §1.1).
- **Status in source:** charter target (< 3.00) and ambition (< 2.50) "not met on the primary instrument" (`s33/REPORT_S33.md` §1.1). DEP.

### H2. long40: best point estimate A80 4.343, statistically tied with E308 (A31.2) 4.739; E308 is "the most-verified headline"
- **Measured:** A80 GATE_rfp 4.343 (chain · long40 · E810 · DEP) vs avg75 −5.402 (3.99x); vs GATE_E308 −0.396, SE 0.215, 0.66x, fold CI [−0.81, −0.13], 5/5, W/L 23/10, median −0.021; 5AL6 alone 46% of the lead (`s33/REPORT_S33.md` §1.2, §17; `s33/VERIFICATION/final/COORD_FINAL_PAIRS.json` confirms −0.396, 0.66x). E308 GATE 4.739, ungated 5.136, vs avg75 −5.006 (SE 0.469, 3.81x, 5/5, W/L 41/4) (`s33/LEDGER.md` E308; `s33/RESULTS/E308_dg_pprior/RESULT_E308_dg_pprior.md` ungated 5.1357). Independent re-decode 45/45: ungated 5.132 vs 5.136, GATE 4.736 (`s33/VERIFICATION/final/V_E308_verdicts.json` mean_own 5.13203 vs 5.13573).
- **Original interpretation:** "The two clean, quantum-free decoders are statistically indistinguishable, and E308 is the verified one." (`s33/REPORT_S33.md` §17).
- **Status in source:** A80 GATE_rfp: close-out adversary "SURVIVES as a tie" (0.43–0.65x after correction); D adversary REPRODUCED 4.323; GATE_rfp is a secondary arm "added after dev-target ORACLE looks — the pre-registered primary is GATE_rf 4.424". E308: survives every best-of-k correction (≥ 2.47x vs avg75; 1.04x weakest vs gated incumbent); leakage-clean in 3 audits; REPRODUCED 45/45; mechanism "WEAKENED as stated" (asserted ESM contacts inert under esmprior_v1) (`s33/REPORT_S33.md` §5, §17, §19). Both DEP, CLEAN.

### H3. mid30: A80 3.717 ungated / 3.815 gated
- **Measured:** A80 rf 3.717 (chain · mid30 · E811 · DEP) vs avg75 8.180: −4.463 (SE 0.38, 4.24x, fold CI [−5.08, −3.92], 5/5, W/L 40/1); GATE_rf 3.815 vs A90 4.304: −0.489 (1.04x, fold CI [−0.83, −0.23], 5/5, type-M) (`s33/REPORT_S33.md` §17; `s33/LEDGER.md` E811 FINAL).
- **Original interpretation:** "best mid30 point estimate" (`s33/REPORT_S33.md` §17).
- **Status in source:** close-out adversary: WEAKENED as an improvement over A90 (0.73–0.99x after best-of-k); Y adversary rates "A90 is the mid30 best" REFUTED by it; "3.717 picks the policy (ungated) that is better on mid30 ... under the pre-registered gating policy the mid30 number is 3.815" (`s33/REPORT_S33.md` §17). DEP, CLEAN (one training-crop flag; rf 3.788 without 2WQ0).

### H4. The gain came from information plus decoding, not search
- **Measured:** swapping the prior alone (LFO 36-protein distogram → esmprior_v1) took the DG ensemble from 5.681 (E306 noise12) to 5.136 (E308), ungated chain; on 6 dev targets (cloud, ORC) decoder 4.35 vs information floor 4.21; decoder capacity with native pair information 0.62 Å (E800) (`s33/REPORT_S33.md` §1.3, §18).
- **Original interpretation:** "The gains at length came from new information (ESM-2 pair geometry, distilled into a clean length-general prior) decoded directly into coordinates. The next lever is more of that information, not more search." (`s33/REPORT_S33.md` §1).
- **Status in source:** 0.62 Å capacity oracle "WEAKENED as a decoder comparison" by the D adversary (same native near/far map: A80 4.04 vs DG 3.83 on 6 dev targets); information floor / RF / saturation "SURVIVE" (`s33/LEDGER.md` E850V–E853V).

### H5. CVaR-VQE never improved a built-chain answer
- **Measured:** 34 chain-level CVaR-VQE-vs-classical-twin contrasts across 10 lanes and 3 instruments; none reached a RESULT in VQE's favour; none reached 0.7x in VQE's favour at census time (`s33/VERIFICATION/final/QUANTUM_CONTRASTS.md` §D). Only equal-tuning chain test E1000: ungated P1 vqe_min − tuned sa_t_min −0.824 (0.84x NOT MEASURED; median −0.07); gated −0.558 (0.66x); mid30 +0.176 (0.22x); seed-1 replication −0.066 (0.05x); 2-seed −0.445 (0.43x) (`s33/RESULTS/H_hybrid_long40_scored.json`; `s33/RESULTS/H_hybrid_E1006_long40.json`). Only chain RESULT involving VQE vs register-free: E811 +0.807 (1.04x, RESULT: WORSE) (`s33/REPORT_S33.md` §8).
- **Original interpretation:** "CVaR-VQE never improved a built-chain answer (where it changed one, it was for the worse)"; "In S33, CVaR-VQE had a real *role* in several designs ... In no design was that role *load-bearing*." (`s33/REPORT_S33.md` §1.4, §16).
- **Status in source:** census verdict "No." (`QUANTUM_CONTRASTS.md` §D); H adversary 4 seeds: "CVaR-VQE NOT load-bearing SURVIVES" (`s33/LEDGER.md` E1005/E10xxV). Full detail in `QUANTUM_RESULTS.md`.

### H6. Energy-level "VQE beats SA" results were SA-tuning artefacts
- **Measured:** E406 VQE 3.057 vs lane SA 3.222 (41/45) → E406V tuned SA 3.064 (+0.007, 0.18x, VQE lower 24/45); E1001 tuned SA 3.394 < VQE 3.457 < P_prior SA 3.670 (3 dev targets) (`s33/LEDGER.md` E1001, E403V/E404V/E406V).
- **Original interpretation:** "LESSON: every VQE-vs-SA claim needs equal tuning effort, not just equal evaluation budget." (`s33/SCIENTIFIC_MEMORY.md`).
- **Status in source:** "the energy claim is REFUTED" (A41 row, `s33/REPORT_S33.md` §5).

### H7. Length changed the problem
- **Measured:** optimal operator flips (averaging wins at 13 aa; narrow selection at 33; decoding at 33–55); sign of (top-1 − avg75) +0.62 / −0.92 / −0.71; ESM-2 P@L/5 0.53 / 0.66 / 0.74 at 13 / 33 / 55 aa; every long-length mechanism transferred to tuning126 is harmful (E105 +0.344, E504a +2.137, E606 +0.288, E511 +0.164, E812 interim +0.296) (`s33/REPORT_S33.md` §11; `s33/RESULTS/E603_length_curve/curve.md`).
- **Original interpretation:** "Did length change the problem? Yes, completely." (`s33/REPORT_S33.md` §11).
- **Status in source:** measured (DEP arms; ORACLE diagnostics labelled).

### H8. Bottleneck and next architecture
- **Original interpretation:** "The bottleneck is information in esmprior_v1's long-range pair distributions (600 training crops, 6 of 82 planned shards). It is not search and not decoding." S34-A01: esmprior_v2 + A80 + template gate, length-routed, "with a pre-registered quantum re-test" (A82) with kill rules (`s33/REPORT_S33.md` §1.7, §27, §28).
- **Status in source:** esmprior_v2 (E407) CANCELLED in S33 for RAM (needed 3.8 GB free) and carried to S34 (`s33/LEDGER.md` E407; `s33/REPORT_S33.md` §12).

## 5. Check of the user's S33 summary against the source

The user's summary was checked, not copied. "Supports" = the source states it; "Qualifies" = the source states it with limits the summary omits; "Contradicts" = the source states otherwise.

| # | user's point | verdict | what the source says (citations) |
|---|---|---|---|
| 1 | "strongest improvements came from better structural information and decoding" | **Supports, with qualifications** | REPORT §1.3 "The gain came from information plus decoding, not search"; SCIENTIFIC_MEMORY "DECODING, NOT SELECTING, is the long-chain lever"; prior swap 5.681 → 5.136 (E306 → E308). Qualifications in source: (a) the improvements exist only at 33 and 55 aa; tuning126 "did not move" (REPORT §1.1); (b) the native-free template gate is a separate large contributor ("the most robust composite component", REPORT §14; BLOSUM rank-0 1.55 Å on template targets, `s33/MAP_LONG.md` §7); (c) E308's asserted ESM contacts are "INERT" under esmprior_v1 — "The gain is the learned prior + distance-geometry embedding + ensemble" (REPORT §17). The source frames the information as a learned *pair-distance prior* (esmprior_v1 over ESM-2 650M), i.e. "information", not "structural information" in general. |
| 2 | "CVaR-VQE not load-bearing in final built-chain" | **Supports** | QUANTUM_CONTRASTS §D "Did CVaR-VQE ever change a built-chain answer? **No.**"; REPORT §16 "In no design was that role *load-bearing*"; A90 − GATE_sa +0.026 / +0.025, A90 − GATE_none +0.110 (long40) (`ARCHITECTURE_S33-A90.md` §6); A101 with quantum tails removed 4.352 vs 4.356 (`ARCHITECTURE_S33-A101.md`). Qualification: at mid30 the *discrete search* in A90 nearly mattered (A90 − GATE_none −0.262, 0.95x NOT MEASURED; SA − none −0.393, 1.05x RESULT) "but SA does it at least as well as CVaR-VQE ... the gain belongs to the discrete search, not to the quantum solver" (`ARCHITECTURE_S33-A90.md` §6; QUANTUM_CONTRASTS #22–24). |
| 3 | "tuned classical search matched/beat quantum" | **Supports "matched"; qualifies "beat"** | Energy: tuned SA 3.394 < VQE 3.457 (E1001, 3 dev targets) — beat; E406V tuned SA 3.064 vs VQE 3.057 (+0.007, 0.18x) — tie (LEDGER E1001, E406V). Chain: in the only equal-tuning chain test the point estimate leaned *toward VQE* (E1000 −0.824, 0.84x NOT MEASURED; 4-seed adversary "leans toward VQE on every seed but never resolves") and did not replicate (E1006 −0.066) (REPORT §1.4). So on the chain tuned SA *matched* (no resolvable difference) rather than beat VQE. Greedy beat VQE on raw objectives (E003; S_mosaic E103 21/1/23; E604b hit rate greedy 54% vs VQE 27%). The source adds a stronger point the summary omits: **untrained random-prior sampling beat the trained VQE on the chain** (E1006 2-seed +1.035, 1.35x RESULT; H adversary 4-seed +0.872, 1.46x RESULT, WY p 0.0001; X E518V +0.070, 1.02x RESULT, tail cloud) (REPORT §1.4). |
| 4 | "apparent quantum wins disappeared under stronger controls" | **Supports** | A41 energy win 41/45 (E406) → tie vs tuned SA (E406V) and SA better (E1001); E1000 P1 −0.824 → seed replication −0.066 ("basin lottery", LEDGER E1006/E1007); D_decoder "VQE below SA on 36/40" was "against an SA that scored worse than random sampling" → D adversary: VQE "ties random prior sampling in energy" (REPORT §1.5, §1.4); X_short A53 round-1 n = 12 "was a favourable draw" → full n VQE ≈ SA, random better (REPORT §5); E406 raw chain VQE 6.222 < random 7.281 (`s33/RESULTS/E406_tt_vqe/*`) → after continuous relaxation random 4.759 < VQE 5.519 (`ARCHITECTURE_S33-A100.md`); entanglement win at 40 q energy (E104 8W/3L) → no chain effect (2-seed −0.188, 0.26x). |
| 5 | "CVaR tail collapse and solver-equivalence were failure mechanisms" | **Supports, with qualifications** | Both named in REPORT §1.6 and QUANTUM_CONTRASTS §D ("Solver-equivalence lemma"; "CVaR tails concentrate and destroy the diversity that ensemble readouts need (E306, E310)"). Qualifications: the source lists four mechanisms, not two — also "Register energies do not transmit to the chain: within-target ρ(E_P, chain) is −0.08" and "The continuous search is already solved by 32–64 restarts, leaving no search headroom" (REPORT §1.6); the H-lane "topology-trap" mechanism was rated "partly definitional (WEAKENED)" by its adversary (LEDGER E1005/E10xxV). Tail concentration is not quantum-specific: E306 SA tail Hamming 2.3 vs VQE 2.4 (`ARCHITECTURE_S33-A33.md`). Solver-equivalence is a derivation (SCIENTIFIC_MEMORY "SOLVER-EQUIVALENCE LEMMA"); on enumerable registers "VQE = exhaustive = SA" (M_mid E604b). |
| 6 | "strongest architecture did not require the quantum stage" | **Supports** | E308/A31.2 and A80 "contain no quantum stage" (REPORT §1.4); strongest classical baseline at 55 aa is "E308 A31.2 4.739, with no quantum stage" (REPORT §12); final length-routed system "contains **no CVaR-VQE stage that changes the answer**" (REPORT §17); tuning126 production has `quantum=False` (MAP_PIPELINE §4 D10). Note the source does not claim this satisfies the charter's "SACRED" quantum-centred requirement; it proposes a pre-registered quantum re-test (A82) for S34 (REPORT §28). |

No point of the user's summary is contradicted by the sources in this import. Points 3 and 5 omit source qualifications recorded above.

## 6. Glossary (original terminology, as defined in source)

| term | definition in source |
|---|---|
| DEP / DEPLOYABLE | "no native structure anywhere upstream of scoring" (`s33/REPORT_S33.md` conventions) |
| ORC / ORACLE | reads `rr`, `nat_ca` or anything native-derived; never deployable (`s33/FALSIFICATION_CATALOGUE.md` §1) |
| CLEAN | only learned prior is esmprior_v1, leakage-audited (`s33/REPORT_S33.md` §5, §21) |
| LFO-XF | uses the map-learned leave-long40-fold-out ESM distogram; out-of-fold, but 13 cross-fold long40 pairs > 0.40 NW identity, so 10 targets have a homologue's native in training (`s33/REPORT_S33.md` §21) |
| chain / cloud / energy | built chain after canonical λ = 0.3 projection (endpoint) / unprojected CA cloud (diagnostic) / native-free objective value (`s33/REPORT_S33.md`) |
| NOT A RESULT / NOT MEASURED / RESULT / type-M zone | < 0.7x / 0.7–1.0x / ≥ 1.0x with fold CI excluding 0 and ≥ 4/5 folds / 1.0–1.3x (`s33/REPORT_S33.md`) |
| sentinel / licensed pairing | same-job re-projection of production; a cross-job chain pairing is "licensed only when that job's sentinels re-project production bit-identically (contract rule 20)" (`s33/REPORT_S33.md` §2) |
| production analogue | A00 on tuning126; BLOSUM avg75 on mid30/long40 (`s33/REPORT_S33.md`) |
| Phase-1 incumbent | E001-ESM contact-agreement top-5 average (`s33/REPORT_S33.md`) |
| template gate / GATE_x | fold-out Otsu threshold on log(simres) routing template targets to the BLOSUM rank-0 window (`s33/MAP_LONG.md` §7; `s33/REPORT_S33.md` §14) |
| esmprior_v1 (S33-A40) | 2D dilated ResNet on ESM-2 650M features → 28-bin CA/CB distance distributions + per-residue (θ,τ) head; 600 leakage-safe prots/ crops (`s33/ARCHITECTURES/ARCHITECTURE_S33-A40.md`) |
| rf / rfp | A80 register-free decoder / rf plus 32 lowest-energy BLOSUM pool windows relaxed (`s33/REPORT_S33.md` §17) |
| condition A / C | A: register not enumerable; C: lower energy ⇒ lower RMSD (checked as within-target ρ(E, RMSD), often "in band") (`s33/MAP_QUANTUM.md` §3 #10) |
| load-bearing | not given one formal definition in the imported files. Operational forms: H_hybrid's pre-registered rule "needs RESULT: BETTER" for P1 vqe_min − sa_t_min on the long40 built chain (`s33/STATE_LIVE.md`, H_hybrid block); D_decoder's "Load-bearing test: (a) discrete global search (best solver) vs register-free continuous decoder on the built chain; (b) CVaR-VQE vs SA at equal energy-evaluation budget" (`s33/STATE_LIVE.md`, D_decoder block). Contrasted with a "real *role*" in REPORT §16 |
| solver-equivalence lemma | "For a diagonal H on register x, min over distributions of CVaR_α(p) = min_x E(x) for every α ∈ (0,1] ... any pipeline whose readout depends only on argmin E gives the SAME built chain whichever solver finds the argmin." (`s33/SCIENTIFIC_MEMORY.md`) |
| tail collapse | "At convergence the CVaR tail sits on the argmin, so a 'tail ensemble' degenerates to a single state." (`s33/REPORT_S33.md` §8); formal statement §25.2 |
| collapse lemma | CVaR score-function training = correlated cross-entropy method; "a collapsed bit is absorbing (its gradient is O(√m))" (`s33/REPORT_S33.md` §9, §25.7) |
| inert-qubit lemma / near-miss lemma | contact qubits already satisfied cannot move a converged decode / ESM false positives median 10.2 Å, 57% within ±2 residues of a true contact (`s33/REPORT_S33.md` §25.4–5) |
| D4 sign lemma | per-shot predictor draw makes lower-tail CVaR "risk-SEEKING" (`s33/REPORT_S33.md` §25.6) |
| averaging lemma / contraction bias | averages contract pair distances; a distance-likelihood energy ranks an ensemble mean below its members exactly when RMSD ranks it above (`s33/REPORT_S33.md` §25.9) |
| lever-arm law | RMSD ~ s·ρ·√(n/2) for independent per-residue angle errors (`s33/REPORT_S33.md` §25.8) |
| information floor | native relaxed under the esmprior energy: 4.21 Å (cloud, 6 targets) (`s33/REPORT_S33.md` §18) |
| H-Q1 | hypothesis that a free-energy (tempered Born machine) objective gives a posterior-like distribution whose readout beats argmin and classical ensembles (`s33/SCIENTIFIC_MEMORY.md`) |
| perturb-and-MAP / Metropolis twin | classical ensemble twins of Gibbs / tempered Born machine readouts (`s33/REPORT_S33.md` §25.3; `ARCHITECTURE_S33-A71.md`) |
| equal tuning (vs equal budget) | twin given the same native-free tuning effort, not only the same evaluation budget ("the E1001 lesson") (`QUANTUM_CONTRASTS.md`) |
| topology-trap lottery | concentrated tails commit to one basin; trap counts order solvers as their chain means (`s33/REPORT_S33.md` §16) |
| best-of-k corrections | Bonferroni, `best_of_k_accounted`, winner's-curse, split-half transfer, Westfall-Young (`CLAIM_CENSUS.md` §2) |
| mosaic / subset / fragment / contact / (θ,τ) / macro register | structural CVaR-VQE state spaces (`s33/REPORT_S33.md` §6) |

## 7. Pointers to the other three files

- `NEGATIVE_RESULTS.md` — every negative / null / killed / falsified / retracted / weakened result in the imported sources.
- `QUANTUM_RESULTS.md` — every quantum-component test, classical-twin contrast, solver-equivalence, tail collapse, resource figure.
- `LESSONS.md` — lessons the sprint recorded; importer notes (gaps, contradictions).

## Lane and attack evidence

Provenance of this section: the 176 tracked `.md` files under `s33/LANES/**` (107) and `s33/VERIFICATION/attack_*/**` (69) were read in full by importer part B; their content is relayed here with the original `s33/` paths. This agent did not re-read those files; where they overlap with the files read directly (REPORT, LEDGER, census, architecture files), the two are compared in §L2.

### L1. Lanes: question, lane verdict, adversary verdict

| lane (E-block, A-range) | lane question (source) | lane's own verdict | adversary verdict (tracked .md) | files |
|---|---|---|---|---|
| C_contact (E3xx, A30–A34) | do ESM contacts + a length-appropriate distogram embedded as DG restraints beat window selection; does the A33 CVaR-VQE tail decode lower than SA / trivial rule / no register ("NULL expected") | best DEPLOYABLE GATE_noise12 5.264; pre-registered primary GATE_dg_topL 5.421; "QUANTUM CONTRIBUTION: none measurable" | C1 GATE_noise12 SURVIVES (re-impl 5.271; corrected 1.26x); C1b noise12-as-best WEAKENED; C3 SURVIVES; C4b ungated noise12 vs inc WEAKENED; C5 quantum null SURVIVES (strengthened); C6 leakage WEAKENED "but the result SURVIVES a clean prior"; C7 contact mechanism WEAKENED (dg_topL − dg_none −0.181, 0.36x); C8 ensemble WEAKENED | `s33/LANES/C_contact/{STATUS,NOTES,LEDGER_ROWS,FAILED_E301,PREREG_E30x}.md`; `s33/VERIFICATION/attack_C_contact/ATTACK_REPORT.md` |
| D_decoder (E8xx, A80–A82) | "Make CVaR-VQE load-bearing by giving it the GLOBAL nonconvex search of a strong learned folding energy ... and remove the decoder bottleneck"; load-bearing iff H-a (register < register-free RF on chain) and H-b (VQE matches SA) | E800 "THE DECODER BOTTLENECK IS GONE"; E810 interim n = 40: "(a) FAILS"; "(b) HOLDS"; "CVaR-VQE is NOT load-bearing in the S33-A81m design" (FAILED_E810_Ha, "provisional") | session 2: full-45 re-score GATE_rfp 4.343 (lane interim 4.185) WEAKENED; (a) FAILS SURVIVES (strengthened); (b) HOLDS SURVIVES; "best register solver in energy" REFUTED; decoder-bottleneck claim WEAKENED; close-out: mid30 C1 WEAKENED, long40 tie SURVIVES, C3 SURVIVES | `s33/LANES/D_decoder/{STATUS,NOTES,FAILED_E800_A81,FAILED_E810_Ha,PREREG_E800,PREREG_E810,PREREG_E813}.md`; `s33/VERIFICATION/attack_D_decoder/ATTACK_REPORT.md`; `s33/VERIFICATION/attack_D_decoder_final/ATTACK_REPORT.md` |
| F_fragment (E2xx, A20–A21) | SEG-FRAG / HYBRID-FRAG register searched by MPS Born-machine CVaR-VQE; FAILED_E222 hypothesis: refined VQE assemblies beat equal-budget SA and the no-search refinement | lane best 6.037 (classical LFO gate, "CONTAINS NO QUANTUM STAGE"); "Hypothesis 'the quantum stage adds RMSD' FALSIFIED at this power" | **no final verdict in tracked .md** — `ATTACK_REPORT.md` is a "DRAFT, in progress (10:35)"; draft findings: F headline dominated by C_contact GATE_dg_topL (+0.615, 0.72x); cross-fold homologue concentration; decode-only control +0.004 | `s33/LANES/F_fragment/{STATUS,NOTES,FAILED_E201,FAILED_E222,PREREG_E2xx}.md`; `s33/VERIFICATION/attack_F_fragment/{ATTACK_REPORT,COORDINATOR_NOTE}.md` |
| H_hybrid (E10xx, A100–A101) | does the A41 41/45 energy advantage survive to the built chain once the A80 decoder is attached | "CVaR-VQE is NOT load-bearing" (FAILED_E1000, FAILED_E1001) | **verdict labels not in tracked .md** ("Verdicts ... are in the adversary's structured report to the coordinator", `ATTACK_STATUS.md`); recorded numbers all consistent with the lane verdict | `s33/LANES/H_hybrid/{STATUS,NOTES,FAILED_E1000,FAILED_E1001,PREREG_E1000,PREREG_E1005}.md`; `s33/VERIFICATION/attack_H_hybrid/ATTACK_STATUS.md` |
| M_mid (E6xx, A60–A62) | build and freeze a 24–40 aa instrument and place the length curve | A62 5.948 mid30 best (at the time); "Does the optimal architecture change with length? YES"; A60 quantum "decorative at 33 aa" | C1 SURVIVES (magnitude WEAKENED); C2 zero-parameter WEAKENED; C6 implicit gate WEAKENED; C8 quantum null "SURVIVES, and strengthened against the lane" | `s33/LANES/M_mid/{STATUS,NOTES,LENGTH_CURVE,FAILED_E604,FAILED_E607,PREREG_E60x}.md`; `s33/VERIFICATION/attack_M_mid/ATTACK_REPORT.md` |
| P_prior (E4xx, A40–A41) | H1–H3 (esmprior_v1 as selector); PREREG_E406 "does the quantum component change the answer" | S4 6.232 lane best; "on this structural register the trained circuit is a better optimiser than SA at equal budget" | S4 REPRODUCED; vs E001 WEAKENED; C4 (A41 better optimiser) **instance B "WEAKENED to a tie", instance A "REFUTED"**; C5 WEAKENED; leakage audit SURVIVES | `s33/LANES/P_prior/{STATUS,NOTES,FAILED_E404,PREREG_E403,PREREG_E406}.md`; `s33/VERIFICATION/attack_P_prior/ATTACK_REPORT.md` |
| S_mosaic (E1xx, A10–A12) | subset / mosaic registers over the long40 pool; PREREG_E101 H2 quantum role | best 5.813 (gate_dmos_vqe_ref); E107 FALSIFIED quantum role | headline WEAKENED; gate_ref_d SURVIVES; quantum null SURVIVES (strengthened); "CVaR-VQE has a real role" REFUTED; LFO caveat as threat REFUTED (clean prior 5.617) | `s33/LANES/S_mosaic/{STATUS,NOTES,FAILED_E100,FAILED_E105,FAILED_E107}.md`; `s33/VERIFICATION/attack_S_mosaic/ATTACK_REPORT.md` |
| T_tempered (E7xx, A70–A72) | H-Q1: posterior-mean readout of a tempered Born machine beats argmin and the classical noise ensemble; does a circuit beat its Metropolis twin | H-Q1 FALSIFIED on R60 (FAILED_E700_R60); tempered circuit dominated by Metropolis (FAILED_E710) | **no ATTACK_REPORT or verdict file tracked** — only `PREREG_ATTACK.md` and 5 RESULT files | `s33/LANES/T_tempered/{STATUS,NOTES,FAILED_E700_R60,FAILED_E710,PREREG_E700,PREREG_E710}.md`; `s33/VERIFICATION/attack_T_tempered/PREREG_ATTACK.md` |
| X_short (E5xx, A50–A56) | "is the 9-16 aa regime information-saturated?" | "The 9-16 aa regime IS information-saturated with respect to every channel available on this box" | R2 (final): C1–C3 SURVIVE; C4a quantum ties SA SURVIVES; C4b "VQE beats random" REFUTED; C4c A53 kill SURVIVES (R1's REFUTED overturned); C4d tail readout WEAKENED; C5 saturation WEAKENED | `s33/LANES/X_short/{STATUS,NOTES,SHORT_REGIME_THEORY,FAILED_E5xx}.md`; `s33/VERIFICATION/attack_X_short/{ATTACK_REPORT,ATTACK_REPORT_R1}.md` |
| Y_synth (E9xx, A90–A91) | the clean composition reaches the leaky best (5.264), beats A62 on mid30, routes tuning126 to production | long40 4.915 "EQUIVALENT to the leaky best, not better"; mid30 4.304 "new best"; "the search is load-bearing at 33 aa, the QUANTUM solver is not" | L1/L2/L4 SURVIVE; L3 WEAKENED; L5 WEAKENED; M2 WEAKENED; M3 "A90 is the new best mid30" REFUTED; M4 WEAKENED ("not search"); quantum Q SURVIVES | `s33/LANES/Y_synth/{STATUS,NOTES,FAILED_E901,FAILED_E903,PREREG_E900}.md`; `s33/VERIFICATION/attack_Y_synth/ATTACK_REPORT.md` |

### L2. Reconciliation with REPORT_S33, FALSIFICATION_CATALOGUE and VERIFICATION/final

Where lane/attack files and the files read directly differ, both are recorded; nothing is resolved here.

| topic | lane / attack files say | REPORT / LEDGER / census say | note |
|---|---|---|---|
| A41 energy claim (P attack C4) | instance B: "WEAKENED to a tie; the lane's win is an SA-tuning artefact"; instance A: "REFUTED" (`s33/VERIFICATION/attack_P_prior/ATTACK_REPORT.md`) | REPORT §5: "the energy claim is REFUTED"; LEDGER E406V: "WEAKENED/artefact" | wording differs across the two P adversary instances and across REPORT/LEDGER |
| D_decoder full-45 numbers | lane files have interim only (n = 40); attack session 2: "the lane's full-45 scorer (D_score) never ran"; adversary re-scored GATE_rfp 4.343 (`s33/VERIFICATION/attack_D_decoder/ATTACK_REPORT.md`) | coordinator `s33/LEDGER.md` "E810 FINAL (... 45/45; ... s33/LOGS/D_score_E810.log)" gives the same 4.343 / 4.424 / 5.127 / 5.696; `COORD_FINAL_PAIRS.json` mean 4.3429 | the digest flagged full-45 numbers as attack-only; the coordinator ledger and final JSON also carry them |
| D (b) "VQE matches/beats SA" | attack: "(b) HOLDS — SURVIVES" (energy vqe < sa 40/45; 2nd seeds 29/39, p = 0.003; SA deficit "structural at this budget") | REPORT §1.5: D's "VQE below SA on 36/40 targets" was "against an SA that scored worse than random sampling"; census: equal tuning "NO" | both record that VQE ≈ random prior sampling in energy |
| A80 long40 lead corrections | D attack: Bonferroni k = 115 0.42x, WY p 0.49; close-out: 0.43–0.65x, WY p 0.11 / 0.45 | REPORT §19: 0.43–0.65x | different adversaries, different families (k = 115 vs 8 / 101) |
| E308 vs C_contact composite | C attack: "E308 ... needs its own independent chain reproduction before it replaces 5.264 in STATE" | FINAL_V later REPRODUCED E308 45/45 (`V_E308_verdicts.json`) | timing |
| H adversary verdicts | no verdict labels in tracked `attack_H_hybrid/*.md` | `s33/LEDGER.md` E1005/E10xxV: "CVaR-VQE NOT load-bearing SURVIVES"; "topology-trap mechanism ... (WEAKENED)"; REPORT §5 A100 row: "no adversary ran" | three different statements in the source |
| T adversary verdicts | no ATTACK_REPORT tracked | `s33/LEDGER.md` E7xxV and REPORT §5 quote "H-Q1 FALSIFIED — SURVIVES at full n", "~2.9x", "MCMC closer 9/10" | verdict text exists only in coordinator files |
| F adversary verdicts | ATTACK_REPORT is a draft | `s33/LEDGER.md` E222V/E223V: 6.037 WEAKENED, clean-prior refinement gain SURVIVES, quantum null SURVIVES; REPORT §31 P9 "the owner instance's final ATTACK_REPORT.md was never written" | coordinator ledger carries the original instance's verdicts |
| A53 kill | X R1: kill REFUTED on endpoint basis (n = 12); R2: SURVIVES at n = 126 (`attack_X_short/ATTACK_REPORT_R1.md`, `ATTACK_REPORT.md`) | REPORT §5: "Round 1's n = 12 estimate was a favourable draw" | R2 overturns R1 in the source |
| E518V completeness | `attack_X_short/RESULTS/E518V_a53_full` header "INTERRUPTED" 63/126 + `_h2` 63/63; ATTACK_REPORT says both halves COMPLETED | REPORT §5 gives the full-126 numbers | recorded as in source |
| mid30 A90 − A62 | Y attack M2: residual 0.76x (k = 44) / 0.87x (k = 20) — WEAKENED | CLAIM_CENSUS §2 item 4: "−1.644 (1.52x RESULT)"; census corrects A90 vs avg75 / Phase-1 operator only | different contrasts corrected |
| mid30 A90 discrete search | Y attack M4: equal-budget random sampling ties VQE (vqe − rand −0.041); gain from register content + energy-ranked tail — "not search" | `ARCHITECTURE_S33-A90.md` §6: "the gain belongs to the discrete search, not to the quantum solver"; QUANTUM_CONTRASTS #24 SA − none RESULT | attack re-attributes the lane's reading |
| A60 register value | M attack C8: register worth −0.8 to −0.9 Å vs best whole member, "not the lane's −1.7" | `ARCHITECTURE_S33-A60.md`: −1.8 Å over its own trivial rule (member 0) | different reference (best whole member vs member 0) |
| E1007 "2-seed" | H lane: 2-seed vqe − random +0.617 (0.98x); seed-1 +0.679 (1.02x RESULT) | REPORT §1.4 cites +0.679 1.02x RESULT as part of a "2-seed RESULT" | see `LESSONS.md` importer note 4 |
| A71 CVaR collapse | T lane: CVaR α 0.1 = argmin (tail perplexity 1.0), 2 targets | REPORT §5 (T adversary): argmin "on only 5/10 (L = 2 under-optimised)" | no tracked T attack file to check |
| CVaR tail readout | X R2 C4d: tail beats argmin −0.048 cloud (1.28x RESULT) but SA tail gives the same → "an averaging effect, not a CVaR/quantum effect" (WEAKENED) | REPORT §24: "'the CVaR tail readout is load-bearing' (X, M, S, C adversaries)" falsified | consistent in direction; the X label is WEAKENED, not REFUTED |
| FALSIFICATION_CATALOGUE | Phase-1 catalogue predicted "Nothing ... carries a credible expectation of ≥ 0.2 Å on the tuning126 built chain" and ranked length directions (R1 ESM at length, R2 length-appropriate prior) first | lane outcomes: tuning126 unbeaten (X); R1/R2 realised as esmprior_v1 + decoders (C, D, P) | consistent; no lane contradicts the catalogue's kill list |

### L3. Effect on the user-summary check (§5)

The lane/attack evidence leaves the §5 verdicts unchanged, with these additions from source:
- Point 2 (not load-bearing): every lane's quantum verdict is null or negative (cross-lane table in L1); Y attack adds "A90 is its own worst ablation" (dg 4.730 < none 4.808 < sa 4.891 < rand 4.902 < vqe 4.926) (`s33/VERIFICATION/attack_Y_synth/ATTACK_REPORT.md`).
- Point 3 (tuned classical matched/beat): H attack A5 — equal-effort tuned parallel tempering "not stronger on 45" (E_P 3.082 / 3.060 vs VQE 3.055 / 3.052); A4 — VQE had fewer topology traps than tuned SA on long40 (vqe 6/9/7/6 vs sa_t 13/10/9/15, per-target Wilcoxon p 0.015) while the 4-seed cloud P1 −0.571 stayed NOT MEASURED (`s33/VERIFICATION/attack_H_hybrid/ATTACK_STATUS.md`). D attack: VQE beat D's (untuned) SA in energy 40/45 but "is indistinguishable from sampling its warm-start prior" (`attack_D_decoder/ATTACK_REPORT.md`). So "matched" is supported; "beat" holds on energy only against tuned SA (E1001).
- Point 4 (wins disappeared): F lane recorded 2GQV as "the one case so far where the quantum stage finds a different, much better basin" (interim, 7 targets) — not carried into any final contrast (`s33/LANES/F_fragment/NOTES.md`); P lane's "better optimiser than SA" (`s33/LANES/P_prior/STATUS.md`) → P attack C4 tie/refuted; X R1 "VQE beats random and no-VQE ablation" (−0.039 tail cloud) → R2 REFUTED at 126.
- Point 5 (mechanisms): lane sources state the same two mechanisms — S_mosaic NOTES 1.5 "CVaR tail collapse is a theorem, not a bug"; X SHORT_REGIME_THEORY Theorem 6.1 (enumerable registers → CVaR tail = classical sort); T T1/T2; H "route (i) fails on BOTH premises of the solver-equivalence lemma" — plus D's attack lesson that condition C must be checked "on the readout energy" (raw → polished rank correlation 0.00).

## 8. Source files read (complete list)

Read in full unless noted. All paths relative to the source repo at the pinned commit.

Top level (`s33/`): `BRIEF.md`, `STATE.md`, `STATE_LIVE.md`, `SCIENTIFIC_MEMORY.md`, `REPORT_S33.md`, `LEDGER.md`, `LEDGER_CONSOLIDATED.md`, `FALSIFICATION_CATALOGUE.md`, `MAP_PIPELINE.md`, `MAP_QUANTUM.md`, `MAP_LEARNED.md`, `MAP_LONG.md`.

`s33/ARCHITECTURES/`: `INDEX.md`, `QENGINE.md`, `ARCHITECTURE_S33-A10.md`, `-A11.md`, `-A12.md`, `-A20.md`, `-A21.md`, `-A30.md`, `-A31.md`, `-A31.2.md`, `-A32.md`, `-A33.md`, `-A34.md`, `-A40.md`, `-A41.md`, `-A50.md`, `-A51.md`, `-A52.md`, `-A53.md`, `-A54.md`, `-A55.md`, `-A56.md`, `-A60.md`, `-A61.md`, `-A62.md`, `-A70.md`, `-A71.md`, `-A80.md`, `-A81.md`, `-A82.md`, `-A90.md`, `-A100.md`, `-A101.md` (33 files).

`s33/RESULTS/**.md` (95 files): `E000_baseline/run_long40`, `E000_baseline/run_tuning126`, `E000_harness_smoke/long40`, `E000_harness_smoke/tuning126`, `E1000_a100_long40_f012`, `E1000_a100_long40_f34`, `E1002_twins_long40_f012`, `E1002_twins_long40_f34`, `E1003_a100_mid30_f012`, `E1003_a100_mid30_f34`, `E1004_twins_mid30_f012`, `E1004_twins_mid30_f34`, `E1006_seed1_long40_f012`, `E1006_seed1_long40_f34`, `E1007_seed1_mid30_f012`, `E1007_seed1_mid30_f34`, `E101_mosaic_chain`, `E103_mosaic_disto_chain`, `E105_refine_tuning126`, `E107_ablation_sa_ref`, `E210_partial_analysis/RESULT_E210_partial.md`, `E222_hybrid_analysis/RESULT_E222_hybrid.md`, `E222_hybrid_p0a`, `E222_hybrid_p0b`, `E222_hybrid_p1`, `E230_short_null`, `E230_short_null_analysis`, `E302b_dg_restraint`, `E306_cvar_tail_chain`, `E308_dg_pprior`, `E311_noise_seedrep`, `E312_d4_chain`, `E403_prior_long40/{esm_m5,nll_lfo,risk_m5,riskesm_m5}`, `E404_prior_tuning126/risk_m75`, `E406_tt_vqe/{head8_greedy,head8_random,head8_sa,head8_vqe,head8_vqe_prod}`, `E501_prior_attn`, `E504a_esm_top5avg`, `E511_esmprior`, `E512_prior_ttz`, `E600_mid30/run_baseline_avg75`, `E601_mid30_{avg75_random_d0,esm_top1,esm_top5avg,native_proj,pool_best,sparse_s10,top1,top75_best}`, `E601_tuning126_top1`, `E603_length_curve/curve.md`, `E604bV_qablate_mid30`, `E604b_mid30_mosaic_loglik`, `E606V_attack_mid30`, `E606_{long40,mid30,tuning126}_loglik_top5avg`, `E701_R60_mid30_p{0,1}of2`, `E701b_R60_long40_p{0..5}of6`, `E710_R60_mid30_p{0,1}of2`, `E810_ld_long40_{f012,f34}`, `E811_ld_mid30_{f012,f34}`, `E900_a90_long40` (+ `_p1`..`_p5`), `E900f_a90_mid30` (+ `_p1`..`_p5`), `E902_a90_seed2_long40` (+ `_p1`..`_p5`). The per-part harness files `E900f_a90_mid30_p2`..`p5` and `E902_a90_seed2_long40` (+ parts) were read line by line after stripping the repeated `config:` JSON line (identical within a job).

`s33/VERIFICATION/final/`: `CLAIM_CENSUS.md`, `QUANTUM_CONTRASTS.md`.

JSON opened to confirm headline numbers (not `.md`; read only for confirmation): `s33/VERIFICATION/final/V_E308_verdicts.json`, `CENSUS_analysis.json` (keys and first chain contrast), `COORD_FINAL_PAIRS.json`; `s33/RESULTS/H_hybrid_long40_scored.json`, `H_hybrid_mid30_scored.json`, `H_hybrid_E1005_long40.json`, `H_hybrid_E1006_long40.json`, `H_hybrid_E1007_mid30.json`.

Top-level docs: `docs/FINDINGS.md` (9,105 lines) and `docs/CONDENSED_REPORT.md` (232 lines) were searched for "S33", "Sprint 33", "esmprior", "long40", "mid30" and 2026-09-25/26 dates: **no Sprint 33 passages** (both last committed 2026-09-14, before the sprint). Not otherwise read.

Total `.md` files read by this agent: 12 top-level + 33 architecture + 95 results + 2 final verification = 142.

Integrated from importer part B (read in full by that agent; not re-read here): 176 tracked `.md` files — 107 under `s33/LANES/{C_contact,D_decoder,F_fragment,H_hybrid,M_mid,P_prior,S_mosaic,T_tempered,X_short,Y_synth}/` (STATUS, NOTES, LEDGER_ROWS, MULTIPLICITY, PREREG_*, FAILED_*, COORD*, LENGTH_CURVE, SHORT_REGIME_THEORY, TABLE_E900_*) and 69 under `s33/VERIFICATION/attack_{C_contact,D_decoder,D_decoder_final,F_fragment,H_hybrid,M_mid,P_prior,S_mosaic,T_tempered,X_short,Y_synth}/` (ATTACK_REPORT*, ATTACK_STATUS, PREREG_*, MULTIPLICITY_ATTACK, COORDINATION*, RESULTS/**.md). Grand total across both importers: 318 `.md` files.
