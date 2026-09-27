_Imported 2026-09-26 from cvar-vqe-protein-folding-v3@3d5b2d25, s30/. Historical evidence — do not edit findings; append dated notes instead._

# Sprint 30 — Quantum-component results

**Framing from source.** `s30/QUANTUM_W.md` §0: *"No CVaR-VQE was trained in Sprint 30. No new Hamiltonian was built, no ansatz was designed, no trainability, gradient-variance or DLA measurement was taken."* But *"'No VQE' and 'no quantum circuit' are different claims, and only the first is true"* — a 9-qubit statevector circuit did run (Q1 below). The production anchor (3.2105 Å) is computed with the quantum stage off: `core/pipeline.py:179` `quantum: bool = False`, `:241` `PROD = Config()`, and the comment at `:173-178` *"VQE/CVaR do not participate at all"* (`s30/QUANTUM_W.md` §12.0; verified against code by `s30/AUDIT_Z.md` §5).

**How the absence was verified** (`s30/QUANTUM_W.md` §0 table): grep of all 24 `s30/s30_*.py` (16,557 lines) for cvar/vqe/ansatz/qiskit/pennylane/qubit/hamiltonian/statevector/SparsePauli/quantum → 2 hits, both comments; `quantum=True` appears only in `s26/`; zero `cvar`/`theta`/`vqe`/`qubits`/`ansatz` keys in the 30 `s30/results/*.json` scanned; no VQE lane staffed; no ledger entry reports a VQE run.

Leakage labels follow the source: ORACLE = reads the native; native-free = deployable in principle.

---

## Q1. The 9-qubit circuit that did run: same circuit, ORACLE objective vs deployed objective

- **Measured:** `s30/s30_D_meter.py build-cache --chain` → `M.build_rungs` (`s29/s29_D_cost_audit.py:250`) constructs `Q.StatevectorCircuit(A.N_QUBITS, A.LAYERS)` = **9 qubits, depth 3**, and runs `oracle_circuit_ceiling(..., starts=1)`: **Adam, 300 iterations, lr 0.05, exact parameter-shift Jacobian**, minimising point-cloud RMSD **to the native** (`s27/s28_A_amp.py:54,60,422-449`), asserted to `dev_s0 < 1e-6` against S28's stored value (`s30/QUANTUM_W.md` §12.1; `s30/AUDIT_Z.md` §5, which traced the code path and found `"dev_circ_s0": 0.0`). Artefact `s30/results/s30_D_ladder_structs/` (126 `.npz`) — **not git-tracked at the pinned commit** (see LESSONS importer notes). Means over n = 126 (`s30/results/s30_D_meter_DIS_chain.json` / `_ca.json :: mean_rmsd`, confirmed by importer):

  | rung | what it is | built chain | CA cloud | leakage |
  |---|---|---|---|---|
  | NATIVE | rebuilt native (projection floor) | 0.0837 | 0.0000 | ORACLE |
  | circ_best | 9q circuit, ORACLE objective, best of 5 starts (loaded from S28) | **0.2516** | 0.2884 | ORACLE |
  | circ_s0 | 9q circuit, ORACLE objective, 1 start, **regenerated in S30** | 0.3175 | 0.3854 | ORACLE |
  | sub0 | least squares in a random subspace | 0.4992 | 0.6199 | ORACLE |
  | PROD | deployed uniform average of DIS top-75 (meter's re-projection) | 3.2071 | 3.0483 | native-free |
  | circ_opt | **same circuit trained on the deployed native-free objective** (`CIRC_OPT_KEY = "circ_l1_i80"`, lam = 1, 80 iters, loaded from `s27/results/s28_A_structs/`) | **3.4330** | 3.3850 | native-free |

  Resource figures: 9 qubits, 3 layers, P = nL = 27 parameters (`s30/QUANTUM_W.md` §19), statevector simulator (exact), 300 Adam iterations; shots not applicable (exact statevector); wall time not recorded in source for this regeneration beyond "47 s/target, four shards, ~25 min" for the chain-projection cache build (S30-L3 §3).
- **Original interpretation:** *"The same circuit reaches 0.2516 Å when its objective is the native and 3.4330 Å when its objective is the shipped score — worse than the classical average it was meant to improve. The circuit is not the problem. The objective is, and it has been all along."* (`s30/REPORT_S30.md` §5.2). `circ_opt` is *"the most damaging single number about the quantum stage in the whole record"* (`s30/QUANTUM_W.md` §0). circ_opt vs PROD: *"0.2259 Å worse"* (built chain, n = 126; `s30/QUANTUM_W.md` §12.1). Classical control that decides it: *"the deployed uniform average (PROD)"* beats the circuit (`s30/QUANTUM_W.md` §16.1).
- **Status in source:** confirmed; §5 audited *"clean"* by lane Z (`s30/AUDIT_Z.md`). The circ_opt-vs-PROD difference is stated as a mean difference; no MDE/fold CI for that specific contrast is given in the source. Note: the circ_opt rung is loaded from S28 artefacts; only circ_s0 was regenerated in S30 (`s30/AUDIT_Z.md` §5).

## Q2. Theorem T1 — the CVaR tail is always a prefix (solver-equivalence of the deployed stage)

- **Measured / derived:** T1 (`s30/THEORY.md` §2; S30-L9): for any `V` differentiable on the tail polytope `Λ(p) = {0 ≤ λ ≤ p, 1'λ = α}` — the exact feasible set of `core/quantum.py:290 cvar_from_probs` — every KKT point is a prefix of the order induced by `∇V(λ*)`. Deployed case `V = ⟨E, λ⟩` ⇒ `∇V = E` constant ⇒ *"one classical sort reproduces it"*; `cvar_from_probs`'s cumulative scan is the greedy fractional-knapsack solution. Prior empirical corroboration cited: 0 violations on 2,592 cells (`s25/results/q_verify.json`); S28 `gate_set_equality` 4,914/4,914 cells to 1.1e−13 Å (`s30/QUANTUM_W.md` §16.1).
- **Original interpretation:** the charter's question *"under what conditions does the tail stop being a prefix?"* has the answer **never**; the load-bearing question is *"the tail stops being reproducible by one classical sort iff the ordering map λ ↦ ∇V(λ) has more than one fixed point"* (`s30/THEORY.md` §2.2). Under the deployed formulation *"the whole quantum stage reduces, for the structure, to choosing m"* — the state determines **exactly one integer** (`s30/QUANTUM_W.md` §15.2). CVaR's residual role: *"α supplies τ … It is not doing selection."* (`s30/THEORY.md` §3.3).
- **Status in source:** killed-by-theorem (report §7.2 #1). Also withdraws S29 §4.5's claim *"the lifted CVaR readout reaches it"* and *"the first formulation whose classical counterpart genuinely goes away"* (`s30/THEORY.md` §2.3 table: **WITHDRAWN**); S29 §4's other claims (V non-additive, non-monotone; free-subset optimum non-prefix) **stand**.

## Q3. T1b — endogenous-order (halfspace) Hamiltonian class: reachable, capped, closed before building

- **Measured:** tails reachable under an endogenous linear order are halfspace cuts, VC dim d+1; Sauer–Shelah caps against 300.6 bits of free 75-subset choice: **24.3 bits** (d_eff = 2), 50.4 (k90 = 6), ≈80 (coordinate k90 = 11), 126.7 (k99 = 21), 175.5 (nominal 33) (`s30/THEORY.md` §3.1). Rank-collapse pre-check on 126 real pools (`s30_T_bits.py`, `s30_T_spec.py`): pair-distance stable rank **1.859** (median 1.865, min 1.247, max 2.721), PC1 55.4%, k90 5.61; coordinate stable rank **3.404** (k90 11.52). Lane Q independently, 12 pools, deployed path: 1.862 pair-distance / **3.619** coordinate, k90 5.6 / 11.25 (`s30/results/s30_Q_rankcheck.json`, confirmed). Pre-check cost *"76 seconds over data already on disk"* (S30-L9 §3).
- **Original interpretation:** lane T's registered rule (stable rank < 2.0 ⇒ closed at encoding level) fired; *"It should not be built"* (S30-L9). The trichotomy's row 2 (endogenous, convex f) is *"classically polynomial (Frank–Wolfe), so it is not a quantum opening"* (`s30/THEORY.md` §3.2). This is *"the first time in the project's history the cheap pre-check fired before the spend rather than after"* (`s30/QUANTUM_W.md` §0).
- **Status in source:** closed by price (report §7.2b #6), **with a scope correction**: the rule fires for a pair-distance lift and does **not** fire for a coordinate-space one (coordinate r_stable 3.4–3.6 > 2.0); *"the VERDICT is unchanged but it now rests on the direct measurements"* (M4, M6) (`s30/THEORY.md` §3.1; `s30/briefs/Q_to_T_quadric_and_rank.md` §4; S30-L15 §3d).

## Q4. The halfspace class's apparent 0.98 Å gain — retracted (order statistic)

- **Measured (M4, lane T, K = 5,000 per class, 6-dim PC subspace, m = 75, CA cloud, ORACLE):** PREFIX 3.0507; HALFSPACE best-of-5,000 2.0691; QUADRIC 2.1551; FREE (best-of-5,000 random 75-subsets) 2.9259. HALFSPACE − PREFIX −0.9816 (4.08×, 5/5, 122W/4L); HALFSPACE − FREE −0.8568 (4.93×) (S30-L15 §1). **M6 common direction bank:** HALFSPACE observed −1.7881 vs across-target null −3.5038 (**196% accounted**), split-half transfer −0.3319 (19%), k_eff 118; QUADRIC 188%, transfer 20%. Transferable rule 3.5231 vs PREFIX 3.0507: **+0.4724 Å WORSE, 1.88× MDE, 5/5 folds, 39W/87L** (S30-L15 §3c; `s30/results/s30_T_transfer.json :: bok`, share_accounted 1.9595 confirmed).
- **Original interpretation:** *"The halfspace class is reachable, not exploitable, and as a rule it is negative."* The FREE null *"asks whether a structured class beats an unstructured one at equal budget, not whether the winning direction is the same direction twice"* (`s30/THEORY.md` §4.3).
- **Status in source:** **RETRACTED** by lane T (its own headline), on a null lane Q requested (S30-L15 §3c; report App. A.2). Reachability statement (a 6-parameter order reaches 2.07 Å) survives.

## Q5. Second-moment / quadric escape — closed before a Hamiltonian was built

- **Measured:** Lane Q (`s30/results/s30_Q_quadric.json`, 128 directions/class/target, all m, 126 targets, CA cloud): QUADRIC − LINEAR at ORACLE m **−0.0105, SE 0.0230, 0.16× MDE, 65W/57L — NOT MEASURED**; at shipped m = 75 **+0.2059, SE 0.0405, 1.81× MDE, 37W/89L — WORSE** (confirmed). Lane T M4 (K = 5,000): QUADRIC − HALFSPACE **+0.0860, 2.95× MDE, 5/5 folds, 21W/105L** (P4a HELD) (S30-L15). Order statistic (lane Q): LINEAR 225% / QUADRIC 203% accounted by across-target null; split-half +0.0323 (−3%) / −0.0204 (2%) (S30-L12, confirmed `share_accounted` 2.2500). Structured form `disp2(x) = ‖W_x − mean(W)‖²`: **3.3585 at m = 75** vs production 3.0483; every native-free rule direction worse (S30-L12). Best prefix for a linear direction median m = 402 (class does not degenerate to argmin).
- **Original interpretation:** *"A seventeen-fold expansion of the reachable-tail class is worth 0.16x MDE … and is significantly harmful at the set size the pipeline actually emits"* (S30-L12). Heading: *"MEASURED BEFORE A HAMILTONIAN WAS BUILT, AS INSTRUCTED"*. Hard cap stated in advance: `tr(Σ_λ)` is invariant to a common shift, so a dispersion term *"cannot see the 68% common-mode error at all"* (`s30/THEORY.md` §4.1). *"To reopen it, someone must exhibit a rule that produces a direction, not a larger search over directions."*
- **Status in source:** closed by measurement (report §7.1 #24–26); *"Two samplers, two lanes, same sign."*

## Q6. Subset-selection / set-function CVaR: classical counterpart and complexity (literature)

- **Measured / derived (lane L, `s30/lit/L30_3_set_selection_cvar.md`, S30-L8):** `V(S) = f(mean_S W)` factors through the centroid. Maurey bound R/√m with RMS dispersion √63.82 = 7.99: 0.22 Å at m = 75, 0.86 at m = 5, 1.36 at m = 2. **Frank–Wolfe on the simplex** is *"the correct classical counterpart … and strictly upper-bounds what a circuit could find"*. Maehara (Oper Res Lett 43:526, 2015): CVaR of a stochastic submodular set function is not submodular; no poly-time multiplicative approximation unless P = NP. Wilder (AAAI 2018) / Ohsaka & Yoshida (2017): portfolio (distribution over sets) relaxation restores 1−1/e.
- **Original interpretation:** *"The set-selection problem here is computationally easy and informationally expensive … no solver supplies information."* On the quantum link: *"A quantum state over candidate-index bitstrings is a portfolio over sets … That resonance is suggestive and I want to be honest that it is only that"* — their CVaR is over exogenous randomness, ours over a distribution the optimiser controls; *"The theorems do not transfer as stated."* Submodularity guarantees void because V is not monotone; DPPs/facility location void (V constant on centroid-equivalence classes); QUBO/Ising *"AVAILABLE BUT POINTLESS"*.
- **Status in source:** closed by theorem/price (report §7.2 #3–4, §7.2b #8). Lane L's own caveats (`s30/lit/L30_3_set_selection_cvar.md` §6): Maurey bound is for weighted multisets, not uniform subsets; R should be a max, so the table is optimistic by perhaps 2–3×. AUDIT_Z D11 flags that the report's §9.1 row initially dropped both caveats.

## Q7. Finite-shot CVaR estimator bias — hypothesis refuted

- **Measured (lane L, `s30/lit/s30_L_cvar_bias.py`, synthetic Gaussian spectrum at the deployed cell: n = 9 → 512 states, α = 0.18, shots 2,048 from `core/quantum.py:179`, tail k = 369):** A bias vs concentration +0.0000 … +0.0025 (sd 0.017–0.036); B matched true CVaR, support 2–32: +0.0001 … +0.0019, no trend; C argmin unmoved (β 2.5 exact vs 2.5 finite-shot, penalty +0.0000); D Barkoutsos flat minimiser set, support 92 → 1: bias −0.0006 → +0.0162, smaller than one shot-noise sd (0.027) (`s30/lit/L30_3_set_selection_cvar.md` §4; S30-L8).
- **Original interpretation:** *"REFUTED, by my own check, in the direction opposite to my guess"* — lower-tail CVaR is pessimistically biased; *"Finite-shot CVaR estimator bias is not a mechanism for anything at this project's shot count. Do not spend on it."* Scope: at the `foldvqe` sort path (384 shots, 69 tail shots) bias ~5× larger; *"If any lane proposes a low-alpha or low-shot arm, this closure lapses and must be re-run."*
- **Status in source:** killed by measurement (report §7.1 #36). Lane L's caveat: run on a synthetic spectrum, not a real cell's energies.

## Q8. Bit accounting / encoding: what the quantum register can represent

- **Measured (lane T, S30-L14, `s30/THEORY.md` §5–7; ORACLE, CA cloud):** register as codebook index — 7 index bits move the ORACLE ladder 4.1080 → 1.8978 Å ⇒ ρ = 0.8869 ⇒ 36.63 displacement bits (5.23×) at d = 32.88. Bits delivered: retrieval +0.69 (search-equivalent; SE 0.18), tail readout +0.036 [MDE 0.385]; *"Under one delivered bit per target, against 7,019 bits of choice consumed."* Value-of-a-bit law marginal at R = 7: 0.1317 Å/bit (P1b HELD). Candidate identity 0.132 vs subset cardinality 0.044 Å/bit (3.0×). Torsion encodings: `2n·log₂k` = 25.9 (k=2), 41.1 (k=3), 51.8 (k=4), 77.8 (k=8) bits against **7** deployed qubits (`core/pipeline.py:181`) or 9 in the harness.
- **Original interpretation:** *"the readout's 7 bits are worth five times their face value, and the system cannot supply one"*; *"Binary candidate indexing is optimal among the measured classes, by 3×"*; *"The encoding is not the hidden bottleneck."* Lane X corollary: *"The property a quantum encoding is chosen FOR is the property this condition penalises"* — width at ρ ≈ 0 buys ceiling and costs mean; *"Generation is closed jointly with the readout"* (S30-L10 §3; `s30/QUANTUM_W.md` §15.4).
- **Status in source:** the qualitative codebook claim retained; the **5.2× multiplier is `d`-dependent** — at d = 6 it is 6.69 bits, **0.95×** (`s30/AUDIT_V.md` D2; report §4.2 now states the formula). The torsion "48 bits" figure as worded ("4 basins per residue at n = 12") was a factor-2 wording error (AUDIT_V D11; report §4.2 corrected).

## Q9. Six coefficients — the subspace where the answer lives (ORACLE)

- **Measured (lane T M5, `s30_T_combo.py`, n = 126, ORACLE):** `‖Π_k e‖²/‖e‖²` = 0.1997 (k=1), 0.3514 (2), 0.6072 (6, ρ_ceiling **0.7792** ⇒ 1.91 Å), 0.9261 (21), vs isotropic null k/d; *"8× more concentrated"* than isotropy. Within-top-6 bit price: 0.855 bits for 3.00 Å, 3.782 for 2.50 Å; best native-free field supplies 0.076 (S30-L15 §2–3).
- **Original interpretation:** *"The entire 0.98 Å gap is the problem of locating six per-target coefficients"*; *"It is not the encoding, not the objective's functional form, not the Hamiltonian's off-diagonal structure, not the ansatz, not the optimiser, not the pool, and not the search … It is under four bits of direction per target that nothing native-free supplies."* (`s30/THEORY.md` §8.4).
- **Status in source:** stands as reachability, not value; P5d (the related prediction) was written post hoc and is declared *"NOT A PREREGISTRATION"* (`s30/PREREG_S30_T.md` addendum 2). The earlier "12 bits ≈ six coefficients" aside was withdrawn (S30-L15 §3).

## Q10. The diagonal rank-ladder Hamiltonian (unchanged, deployed off)

- **Measured / cited:** would-be Hamiltonian if `quantum=True`: `H = diag(zrank(top-2^n distogram scores))` (`core/pipeline.py:838`), objective `F = CVaR_α(E; p_θ) − T·H(p_θ)`, leave-fold-out (α, T) `VQE_LFO = {0:(1.0,0.3), 1:(0.25,0.3), 2:(0.25,0.3), 3:(1.0,0.3), 4:(1.0,0.3)}`, 7 qubits, 3 RY/CNOT layers, 50 Adam iterations, exact statevector (`s30/QUANTUM_W.md` §13). Same ladder on every target to **1.18% of range** (`s25/results/q_gibbs.json`, cited in `s30/QUANTUM_W.md` §14.1; AUDIT_Z lists this as not recomputable from `s30/results/`).
- **Original interpretation:** *"S30 established that the diagonal rank-ladder is not the thing that is wrong"*; a new Hamiltonian would matter *"only if it changed the order the tail is a prefix of"*, and both candidate ways were measured reachable-but-not-transferable (`s30/QUANTUM_W.md` §14).
- **Status in source:** item 13 "Hamiltonian used": **NONE**; item 14: *"No new Hamiltonian to be different"* (`s30/REPORT_S30.md` §5.3).

## Q11. Non-diagonal Hamiltonians (lead L9), ADAPT-VQE (L10)

- **L9 — Measured:** no build. Closed upstream by the rank pre-check (Q3) and the second-moment measurement (Q5) (`s30/REPORT_S30.md` §8 L9). **Interpretation:** the lead's question *"does the off-diagonal structure encode information that materially changes the optimization problem?"* is *"answered no, and answered before a Hamiltonian existed."* **Status:** NOT PURSUED as a build; scope qualifier (pair-distance vs coordinate stable rank) travels with it.
- **L10 — Measured:** nothing run. **Interpretation:** *"NOT PURSUED. Its precondition never arrived"* — no correlated structural Hamiltonian survived; S26's product-circuit finding at α = 1 still governs (`s30/REPORT_S30.md` §8 L10). **Status:** not pursued.

## Q12. Trainability, gradient variance, DLA (charter items 17–19)

- **Measured this sprint:** **none** — *"NOT APPLICABLE, not measured this sprint"* (`s30/REPORT_S30.md` §5.3). The only S30 input is the measured `r_stable` (1.859 pair-distance / 3.404 coordinate on 126 real pools), the governing quantity of S29's law `Var[∂F/∂θ] ≈ r_stable(A)/D²` (`s30/QUANTUM_W.md` §18).
- **Cited prior positions (not S30 measurements; recorded as the source states them):** deployed diagonal problem at α = 1 is the *"trivial regime"* (S26); S28 `J = 3` ground state not representable (overlap 0.80–0.88) and *"the gap is OPTIMISATION by basin selection, not expressivity"*; spread-spectrum kNN graph *"and the emitted structure does not move"*; DLA obstruction when `3 | n` (CONJECTURE), algebra maximal at n = 7, L = 3 (so(128)) but **not** at n = 9, L = 3 (su(256), 65,535); *"The algebra is not the obstruction; the parameter count is"* (27 params, generic overlap ~P/D = 0.05); cut-rank: prefixes are rank-1/2 objects, random 75-subsets saturate at 16 (`s30/QUANTUM_W.md` §17–19, citing `s29/THEORY.md`, `s26/`, `s27/`).
- **Status in source:** not applicable this sprint; carried as S26–S29 positions. Recorded unused design lever: `s22/qcand_lib.py :: Encoding` free basis-index relabelling — *"S30 did not test it"* (`s30/QUANTUM_W.md` §19).

## Q13. Classical control vs quantum stage (charter item 16)

- **Measured:** see Q1, Q2, Q5, Q6 and sparse readout (S30-L11: argmin over top-2^B beats the best fully-priced sparse arm at every budget B = 3…9 by +0.1622 to +0.7267 Å, CA cloud; built chain 2-of-top-75 with free weights **2.1683 Å at 11.4+ bits** vs top-128 argmin **2.1435 Å at 7.0 bits**; `s30/results/s30_Q_sparse.json :: F4_chain_headline`, confirmed, F4 **REFUTED**).
- **Original interpretation:** *"The honest form is 'is there any positive for a classical control to reproduce?' and the answer is NO. Every decisive classical control runs against the quantum stage: one sort reproduces the tail exactly; Frank–Wolfe is the correct counterpart and is polynomial; argmin dominates the sparse readout at every budget; PROD beats circ_opt"* (`s30/REPORT_S30.md` §5.3 item 16). *"The one control that would matter cannot be run, because its subject does not exist"* (`s30/QUANTUM_W.md` §16.2). No product-state/separable restriction was run (nothing to restrict).
- **Status in source:** no quantum positive; the charter's §18 quantum-breakthrough criterion not met.

## Q14. Register widening 128 → 512 on the tail ("two qubits") — open, ORACLE, circularity undischarged

- **Measured (lane Q incidental, not pre-registered; ORACLE argmin, CA cloud):** best-of-top-N: N = 128 → FAIL18 4.1846 / other-108 1.8060; N = 500 → 2.2842 / 1.6153; widening 128 → 512 worth **−1.9004 on FAIL18 vs −0.1907 on the 108**, difference −1.7097, SE 0.2207, **2.77× MDE** (S30-L11). Lane F: ORACLE set mean worsens with width on the 108 (3.116 → 4.201) and improves on FAIL18 (6.159 → 5.755).
- **Original interpretation:** coordinator's synthesis *"A selecting readout over a wider register, aimed at the tail. Two qubits take 128 → 512"* (`s30/STATE.md` SYNTHESIS 13:07), corrected one minute later: filter width closed by ceiling; widening-rescues-tail circular; and for lane Q's number *"FAIL18 is defined by production … a bad filter is exactly what pushes good candidates down the ranking"*, so the filter-independent-tail check is *"the gate on that whole direction"* (`s30/STATE.md` CORRECTION 13:08).
- **Status in source:** **OPEN** (report §7.4 #3; S30-L28): *"No ledger entry runs it."* The synthesis itself is withdrawn (report App. A.1; §7.1 #57); *"The register half is not closed."*

## Q15. Shipped-code defect about the CVaR stage's measured role

- **Measured:** `core/pipeline.py:821` docstring asserts *"the CVaR tail is worth +0.113 Å by preventing the collapse, and that is the component's measured role."* S25-L5 withdrew it (`s25/LEDGER.md:232-244`: measured −0.1126 Å at 0.51× MDE); replacement headline −0.1405 Å at 0.68× MDE (`s25/LEDGER.md:280`) — itself below the 0.7× floor (`s30/QUANTUM_W.md` §0; citation corrected by `s30/AUDIT_Z.md` D13).
- **Original interpretation:** *"the sixth instance of prose asserting a state that does not hold, and the first located in shipped code"* (`s30/REPORT_S30.md` §5.4).
- **Status in source:** open defect, not fixed (`core/` read-only) (`s30/REPORT_S30.md` §11.3).

---

## Quantum summary table (as stated in `s30/REPORT_S30.md` §5.3)

| # | charter item | S30 answer |
|---|---|---|
| 12 | CVaR-VQE contribution | *"Nothing as an endpoint contribution"*; α supplies τ |
| 13 | Hamiltonian used | NONE |
| 14 | Different from diagonal rank-ladder? | no new Hamiltonian; diagonality *"is not the defect"* |
| 15 | What the state represents | under deployed formulation, one integer `m` |
| 16 | Classical control reproduces? | no positive to reproduce; controls run against the stage |
| 17 | Trainability | not applicable, not measured |
| 18 | Gradient variance | not measured; `r_stable` input measured |
| 19 | DLA / ansatz | not applicable, not measured |
