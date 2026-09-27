# S29–S33 open problems

_Synthesis, 2026-09-26. Tags: **M**, **I(src)**, **I(prog)** and **U**, as in `README.md`. "Open" means the source left it unresolved: never run, contradictory, or measured too weakly to decide. Items are ordered by relevance to this program's quantum question._

## A. Scientifically open, relevant to the quantum question

| ID | Open problem | What is known (M) | What is not known (U) | Pointer |
|---|---|---|---|---|
| OP-01 | **Classical sampling hardness of learned-energy posteriors** | Diversity and soft Boltzmann readouts help (mid30 chain −0.248, 1.40× RESULT; averaging beats selection). Metropolis matches exact Gibbs at 18 qubits (9/10). | Mixing times, spectral gaps and barrier heights of MCMC or parallel tempering on the esmprior/A80 energy at any length. Whether they grow with chain length. **Never measured.** | QX-28, QX-29; `s33` N26 |
| OP-02 | **Search gap beyond 60 aa** | At 44–60 aa: restart saturation at 32–64 restarts; decoder 4.35 vs information floor 4.21 (6 dev targets, cloud, ORACLE). | Whether decoder − floor grows with length. Whether restarts stop saturating at 100–300 aa. | QX-30; `s33` Q-D3 |
| OP-03 | **A82**: register around the decoder's residual uncertainty | Implemented and pre-registered, with kill rules | Every outcome. **Not run.** | QX-31 |
| OP-04 | **A72 / E720**: tempered Born machine at 32 qubits; E700-R90 | Only the 18-qubit version ran | Every outcome. **Not run** (machine load). | `s33` LN8 |
| OP-05 | **Topology-trap asymmetry** | VQE had fewer traps than tuned SA on long40 (6/9/7/6 vs 13/10/9/15; Wilcoxon p 0.015). Random prior: 0 traps. The 4-seed cloud P1 is −0.571 (0.81×, NOT MEASURED). | Is the lower trap rate a reproducible property of the circuit's distribution? The adversary rated the mechanism "partly definitional". Even if real, random prior sampling dominated it. | QX-25 |
| OP-06 | **Per-residue non-separable branch selection at length** | At 9–16 aa it is enumerable ("blocked ONLY by chain length"). Native-free branch criteria have no in-band skill. The ORACLE best branch is 96% order statistic. | The formulation and its discrimination signal at ≥ 40 aa. The branch diagnostic ("do branches differ at a sparse set of residues or globally?") was **never answered**. | QX-15; `s32` N-R3–N-R5 |
| OP-07 | **Precision-limited estimation** | No source identifies a decision limited by estimator variance. The finite-shot CVaR bias is negligible at 2,048 shots. | Whether any pipeline quantity (basin free-energy differences, ensemble weights) is variance-limited, not bias-limited. **Never audited.** | QX-08 |
| OP-08 | **Soft-vs-hard readouts at long40** | mid30 RESULT (1.40×, T adversary). long40 "not established". | long40 and beyond | QX-28 |
| OP-09 | **Deployable register widening 128 → 512** | ORACLE −1.18 Å on the filter-independent worst-18 stratum. The source predicts the deployable arm is WORSE. | The deployable arm. **Not run.** | QX-13 |
| OP-10 | **Barren-plateau / trainability scaling** beyond 9 qubits | Var ~ 16·2^-n (synthetic); "not yet gradient-limited at n = 7–9" | Measured scaling on structural registers of 18–171 qubits (MPS). **Not measured.** | QX-05 |
| OP-11 | **DLA obstruction when 3 \| n** | Measured at n = 3, 6, 9 | The mechanism, labelled a CONJECTURE | `s29` QR §6 |

## B. Scientifically open, not quantum (context for where information comes from)

| ID | Open problem | Status (M / U) | Pointer |
|---|---|---|---|
| OP-12 | **esmprior_v2** (more training crops): "the top classical lever" | **U.** Cancelled for RAM in S33 | `s33` N31 |
| OP-13 | **E812 final value** (A80 on tuning126) | Interim +0.296 Å WORSE at 84/126. Final value not in the imported files. | `s33` N8 |
| OP-14 | **Elongated, non-globular targets** (5AL6, 5QU8, 6Z2T, 8CMP) | Stay at 11–15 Å under DG even with all native contacts. A80/rfp rescued 5AL6. | `s33` N28 |
| OP-15 | **tuning126 information saturation** | "Inductive, not a theorem." NMR membrane class partly sequence-predictable (AUC 0.71). | `s33` N12, LN9 |
| OP-16 | **Along-μ correction vs its own shrink control** | NOT MEASURED (0.94× / 0.64×) | `s31` F5 |
| OP-17 | **Operator law: "weight toward the set best"** | Ratio 2.85 (S32); "the one arm this sprint's data argues *for*", untested | `s32` N-P9 |
| OP-18 | **Pair-level candidate-graph quantities** | Node-level quantities closed. Pair-level left open (C1 did not fire). | `s31` E7 |
| OP-19 | **Multi-structure barriers F‡** | Open "on price, not theory". D4-P not run. | `s31` E1; `s32` N-D7 |
| OP-20 | **S8 free-energy stage** | Absent from disk and git; would need to be rebuilt from a prose spec | `s29` A9 |
| OP-21 | **AMBER relax (E2)** | Real but small (−0.0221 Å); restraint constant tuned on dev RMSD (native-informed) | `s30` H8 |
| OP-22 | **Bridge instrument 17–26 aa** | Proposed for S34, not built | `s33` LESSONS §5 |

## C. Evidence-integrity problems (logged, not resolved; details in per-sprint LESSONS importer notes)

| ID | Issue | Pointer |
|---|---|---|
| EI-01 | Several numbers circulate with more than one value: production 3.2105 / 3.2126 / 3.2071 (basis and meter differ); projection price +0.159 / 0.164 / 0.1664 / 0.1622; S30 CHARTER ρ −0.0921 vs −0.1964 | `s29`, `s30` LESSONS |
| EI-02 | S33 attack files for F, H and T have no final verdict labels. The P_prior instances disagree (WEAKENED vs REFUTED). | `s33` LESSONS importer 9–11 |
| EI-03 | S33 quantum census: 34 rows in `.md` vs 33 in JSON. Census-time vs final statements differ (E1000 later reached 0.84× in VQE's favour). | `s33` LESSONS importer 5–6 |
| EI-04 | S33 REPORT calls the mid30 E1007 +0.679 a "2-seed RESULT"; the 2-seed value is +0.617 (0.98×, NOT MEASURED) | `s33` LESSONS importer 4 |
| EI-05 | S29 retractions index says "(none yet)", while the report lists 18 withdrawn claims | `s29` NR §0 |
| EI-06 | Verifier and defect counts differ within S31 and S32 reports; S32 cites "ten" pre-registrations but five are tracked | `s31`, `s32` LESSONS |
| EI-07 | The predecessor's leakage safety was "by convention, not by construction" (`rr` / `nat_ca` stored beside deployable arrays) | `s33` LESSONS 25 |
| EI-08 | No quantum resource figures (qubits, depth, shots, wall time) recorded for the S29–S32 deployed stage beyond configuration constants | `s32` QR resource table |

**I(prog).** None of EI-01 … EI-08 changes a quantum verdict in this synthesis. Every quantum null holds on the most conservative reading of each disputed number. The integrity issues matter for any future *reproduction* of the predecessor's classical baselines.

## D. Measurement gaps this program must fill before any quantum claim (I(prog))

1. **Classical hardness data** (OP-01, OP-02, OP-07): no sampling-, search- or estimation-hardness measurement exists at any length.
2. **Length beyond 60 aa**: no instrument exists. Building one needs the predecessor's leakage rules: esmprior_v1's R3 rule (gapless-30 identity ≥ 0.4 to any target is excluded) and cross-fold homologue checks (`s33` LESSONS 23).
3. **Resource accounting for quantum primitives with known separations**: no fault-tolerant or query-count estimate exists for any subproblem.
4. **Hardware**: none, and nothing in the evidence yet justifies it.
