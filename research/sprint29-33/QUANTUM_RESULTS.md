# S29–S33 quantum experiments: consolidated records

_Synthesis, 2026-09-26. Tags as in `README.md`: **M** measured (with pointer), **I(src)** the sprint's interpretation, **I(prog)** this program's reading, **U** untested. Pointers such as `s33 Q-C12` mean `research/sprint33/QUANTUM_RESULTS.md` item Q-C12, and `NR` means that sprint's NEGATIVE_RESULTS file._

**Global facts for every record below:**
- Simulation only. Statevector up to 22 qubits, exact MPS above that (χ 2–16). No hardware, no noise model (`s33` Q-B2).
- "Simulator time" is recorded where the source gives it. It is **not** physical quantum runtime.
- **Claim category tested:** every S29–S33 quantum experiment tested **category 1 (quantum usefulness)**. Some also tested **category 3 (resource: evaluations to optimum)**, in simulation only. No experiment tested categories 2, 4, 5 or 6 as defined in `research/RESEARCH_CHARTER.md`.
- **"Load-bearing"** means: FULL beats the same pipeline with the strongest classical replacement for the quantum part, as a RESULT on the built chain. That is this program's operational definition. The source used the same idea, e.g. H_hybrid "needs RESULT: BETTER" (`s33` README glossary).

Field order in each record: **Problem · Representation · Quantum algorithm · Classical comparator · Resources · Result · Load-bearing? · Falsified/weakened by · Unresolved**.

---

## A. The deployed candidate-index stage (S29–S32)

### QX-01 · Deployed CVaR-VQE on the candidate-index register vs a fixed profile (S29 M6)
- **Problem:** Choose weights over the top-2^n score-ranked candidates so that their coordinate average is closer to the native.
- **Representation:** Basis state = candidate index. n = 7 deployed (9 in the harness). H = diag(zrank(score)).
- **Quantum algorithm:** CVaR_α − T·H(p) free energy. RY + CNOT-ring ansatz, 3 layers (21–27 parameters). Adam with exact parameter-shift gradients, 50–80 iterations. Exact statevector, no shots.
- **Classical comparator:** A fixed target-independent prefix profile m (M6); a uniform top-75 average (production).
- **Resources (M):** 0.30–0.35 GB peak RSS per job. 2P = 54 statevectors per gradient (`s29` QR §0).
- **Result (M):**
  - Built chain: deployed 3.2187 vs fixed m=75 3.2105, −0.0082 Å, 0.27×, NOT MEASURED.
  - Structure-level equality only 42/126 (`s29` QR §2).
- **Load-bearing?** **No.** I(src): "costs or buys nothing measurable."
- **Falsified/weakened by:** The M6 control. Theorem T1, the prefix result (`s30` Q2). The closed-form p* (`s31` Q1).
- **Unresolved:** Nothing material. This register is on the kill list in every variant (`s33` Q-E1).

### QX-02 · Compatibility (non-diagonal) Hamiltonian on the candidate register (S29 lane B)
- **Problem:** Add off-diagonal structure (centred similarity A_c or signed agreement G) so the state encodes candidate compatibility.
- **Representation:** Candidate index, n = 9. H = diag(E) − J·M.
- **Quantum algorithm:** CVaR_0.18 − 0.5·H − J⟨ψ|M|ψ⟩, 27-parameter RY + CNOT. The gate test used the **exact** ground state.
- **Classical comparator:** The exact eigensolver (`eigh`), which is the classical counterpart. PERM and SPEC controls. Production top-75.
- **Resources (M):** 9.6 s/target, 0.35 GB. Gradient variance ~ r_stable/D², with r_stable ≈ 1.0–1.7 (`s29` QR §4a–b).
- **Result (M):**
  - 0 of 24 (M, J) cells cleared 0.7× MDE vs production on either readout.
  - The signed readout was 0.3–4.7 Å worse (`s29` QR §4c).
  - Bright line B1 (the trainability premise) was refuted: slopes −2.305 and −1.900 vs −1.830 for raw A (`s29` NR F1).
- **Load-bearing?** **No.** The endpoint arm (M3) was never run because the gate stayed shut.
- **Falsified/weakened by:** The exact-ground-state gate. The stable-rank law: a Gram of structural deviations has r_stable ≤ 3N−6 ≤ 42. The sign-mixing lemma.
- **Unresolved:** **I(src):** the closure is "about the ENCODING … not about off-diagonal Hamiltonians." **U:** off-diagonal structure on a register whose dimension grows with the target was not tested here.

### QX-03 · Tail-then-aggregate (TTA): CVaR over a structural observable (S29 lane B / T)
- **Problem:** Escape the prefix theorem by applying CVaR to the tail's aggregated structure instead of per-state energies.
- **Representation:** Candidate index, n = 9. Objective f(R_α(p)).
- **Quantum algorithm:** CVaR-VQE with the lifted objective. Same ansatz as QX-01.
- **Classical comparator:** Free subset search (greedy plus exhaustive over pairs and m=5 subsets); production; M6; an untrained best-of-16 control.
- **Resources (M):** 6 s/target, 0.33 GB (`s29` QR §7d).
- **Result (M):**
  - Free subset search does break set-equality: non-prefix optimum on 114/126 (pairs) and 124/126 (m=5).
  - But the m=5 optimum is +0.2451 Å WORSE than production (1.45×).
  - The VQE endpoint at λ=1 is +0.104 / +0.116 Å (0.95× / 1.03× WORSE).
  - The VQE tail was still the energy prefix (`s29` QR §7c–d).
- **Load-bearing?** **No.** F5b REFUTED.
- **Falsified/weakened by:** The endpoint arm. T1 (`s30` Q2) withdrew S29's claim that the lifted readout "reaches" the non-prefix optimum.
- **Unresolved:** None for this objective. **I(src):** "the mechanism is alive and irrelevant."

### QX-04 · Configuration-space ("chimera") CVaR-VQE with a transverse-field mixer (S29 lane X)
- **Problem:** Is the candidate pool the wrong state space? Search recombinations of fragment segments instead.
- **Representation:** S ≤ 5 segments × 8 parents; q = 3S ∈ {9, 12, 15} qubits; exhaustively enumerable (512–32,768 configurations). H = pair log-score + Ramachandran prior (diagonal) − Γ·ΣX.
- **Quantum algorithm:** CVaR_0.15 − T·S − Γ⟨ΣX⟩, exact statevector, Adam 80 iterations, 2 seeds. This is the only S29 formulation meeting C1 (non-commuting) and nominally C2.
- **Classical comparator:**
  - SA at matched evaluations.
  - Exact ground state, Gibbs at matched entropy, exact top-m.
  - Untrained circuit, best-of-N untrained draws (BESTOFN).
  - Product state, permuted posterior.
- **Resources (M):** q=18 cost 32.5 min/arm, so capped at q ≤ 15. Probe job 11,117 s wall, 0.31 GB (`s29` QR §8).
- **Result (M), n = 12:**
  - VQE vs production +0.4572 Å, 1.18× WORSE.
  - VQE vs SA −0.0186 (0.09×).
  - BESTOFN vs VQE −0.0088 (0.07×).
  - The state was 95.7% of maximum entropy, i.e. near |+⟩^q, an eigenvector of the mixer.
  - The chimera ORACLE ceiling was +0.6533 Å worse than the pool's own ORACLE best.
- **Load-bearing?** **No.** I(src): "Nothing the quantum stage does survives to the chain"; the mixer's endpoint channel is "m".
- **Falsified/weakened by:** The BESTOFN control; the SA control; the pool's own ORACLE ceiling. The space does not contain the answer.
- **Unresolved:** Scoped to 12 targets, 8 parents and contiguous 3-mers. **U:** a chimera space that contains better structures than the pool.

### QX-05 · Trainability / DLA / gradient-variance characterisation (S29 lane T; S31)
- **Problem:** Is the ansatz or trainability the obstruction?
- **Representation / algorithm:** The deployed ansatz. Exact Pauli-closure DLA; gradient variance over θ draws.
- **Result (M):**
  - The DLA is not the obstruction (n = 9, L = 3 gives su(256), 65,535-dimensional). I(src): "the parameter count is."
  - KL(p_θ‖p*) is 0.930 bits.
  - 80 → 2000 iterations leave the gap unchanged. Depth 12 with 8 restarts closes it, taking about 60 s (`s29` QR §6; `s31` Q2).
- **Load-bearing?** N/A (characterisation).
- **Unresolved:** **I(src):** "at n = 7–9 we are not yet gradient-limited" (`s31` QR §0). Barren-plateau scaling at larger n was never measured.

### QX-06 · Same 9-qubit circuit: ORACLE objective vs deployed objective (S30)
- **Problem:** Is the circuit's expressivity the limit?
- **Representation:** Candidate index, n = 9, depth 3, affine (signed-amplitude) harness readout.
- **Quantum algorithm:** Adam 300 iterations (ORACLE objective: RMSD to the native) vs the deployed native-free objective.
- **Classical comparator:** Production uniform average (PROD 3.2071 in that meter).
- **Result (M):**
  - circ_best 0.2516 Å (ORACLE objective) vs circ_opt 3.4330 Å (deployed objective), which is worse than PROD (`s30` Q1).
  - S31 later showed the 0.2516 is a property of the affine readout's regulariser: the affine ORACLE ceiling is exactly 0.0000 on 126/126 (`s31` Q6).
- **Load-bearing?** **No.**
- **I(src):** "The circuit is not the problem. The objective is."
- **Unresolved:** None for this register.

### QX-07 · Endogenous-order lifts: halfspace and quadric (second-moment) classes (S30)
- **Problem:** Change the order the CVaR tail is a prefix of by making the order depend on the state.
- **Representation:** Candidate index. Tails as halfspace or quadric cuts in a PC subspace.
- **Quantum algorithm:** None built. Closed by measurement before any Hamiltonian existed.
- **Classical comparator:** Best-of-K random directions; across-target null; a FREE class (random subsets).
- **Result (M):**
  - The halfspace best-of-5,000 gain of −0.98 Å was 196% accounted by the across-target null. As a transferable rule it was +0.4724 Å WORSE (1.88×): RETRACTED.
  - Quadric vs linear: +0.2059 Å (1.81× WORSE) at shipped m.
  - Pair-distance stable rank is 1.859 (`s30` Q3–Q5).
- **Load-bearing?** N/A (never built).
- **Falsified/weakened by:** Order-statistic nulls; the stable-rank pre-check.
- **Unresolved:** Scope correction: the coordinate-space stable rank is 3.4–3.6, so the rank rule does not fire there, although the verdict rests on the direct measurements.

### QX-08 · Finite-shot CVaR estimator bias (S30 lane L)
- **Result (M):** Bias +0.0000…+0.0025, below one shot-noise sd. The argmin is unmoved (synthetic spectrum, 2,048 shots) (`s30` Q7).
- **Load-bearing?** N/A.
- **Status:** REFUTED as a mechanism.
- **Unresolved:** **I(src):** the closure lapses at low shots or low α (e.g. 384 shots / 69 tail shots gives about 5× the bias).

### QX-09 · Sparse weighted readout and bit accounting of the register (S30 lane Q / T)
- **Result (M):**
  - The argmin over top-2^B beats every fully priced sparse arm at B = 3…9 by 0.16–0.73 Å (CA cloud).
  - Candidate identity is worth 0.132 Å/bit vs subset cardinality 0.044 Å/bit.
  - Delivered bits are below 1 per target vs 7,019 consumed (`s30` Q8, Q13).
- **Load-bearing?** N/A.
- **I(src):** "The encoding is not the hidden bottleneck."

### QX-10 · Exact p* substitution for the circuit (S31 lane P, "the decisive experiment")
- **Problem:** Does solving the deployed objective exactly (instead of via the circuit) change the endpoint?
- **Representation:** Candidate index, n = 7, deployed (α, T).
- **Quantum algorithm:** The deployed run_cvar_vqe (50 iterations) vs the closed-form hinged-Gibbs p*.
- **Classical comparator:** p* by one bisection, O(D log 1/ε).
- **Resources (M):** p* 0.0012 s vs circuit 0.0985 s per target, 82× (`s31` QR §0).
- **Result (M):**
  - The circuit is strictly worse in free energy on 126/126 (mean gap +0.1937).
  - P1 (p* − circuit, convex readout) −0.0112 Å, 0.19×, NULL.
  - P2 (selection readout) −0.0280, 0.29×, NULL.
  - The shipped stage vs production is +0.0175, 0.35×, NULL (`s31` Q1, Q4).
- **Load-bearing?** **No.** I(src): "Whatever it contributes, it contributes BY FAILING TO OPTIMISE."
- **Unresolved:** **I(src):** this "does not test whether a better objective would help."

### QX-11 · Non-diagonal Hamiltonians and ADAPT-VQE on the candidate register (S31, theorem)
- **Result:** Derivation only, no compute. The source gives three obstructions:
  1. CVaR needs a per-shot energy.
  2. The forced operator diag(â) − B is mean-field and quartic in ψ.
  3. The register dimension equals the candidate count, so the problem is a ~1 ms `eigh`.
  - ADAPT's gradient criterion is undefined for CVaR (`s31` Q9, NR A8–A9).
- **Load-bearing?** N/A.
- **Falsified/weakened by:** S32 re-examination: obstructions 1 and 3 are "properties of the candidate-index register, not of CVaR-VQE" (`s32` QR-7).
- **Unresolved:** See QX-14.

### QX-12 · Index encoding redesign: Gray code, structure-aware maps (S31 lane C)
- **Result (M):**
  - Gray coding is a proven no-op (identical partition on 126/126).
  - The best map raises the ORACLE ceiling by 0.0655 Å against a registered 0.10 bar.
  - The best deployable map is a random permutation (−0.0160).
  - Bit mutual information with quality is ≤ 0.066 bits (`s31` Q13).
- **Load-bearing?** N/A.
- **Status:** CLOSED.

### QX-13 · Register widening 128 → 512 ("two more qubits") (S30 / S31)
- **Result (M, ORACLE):**
  - Widening is worth −1.1811 Å (cloud) on the filter-independent worst-18 stratum, p = 0.0001.
  - The FAIL18 figure of −1.9004 was retired as near-tautological (`s31` Q14; `s30` Q14).
- **Load-bearing?** Not tested. The **deployable** arm was never run.
- **Unresolved:** **U:** does a deployable widened selector beat production? The source's labelled prediction is that it "should come out WORSE" (`s31` NR A13). **I(src):** "Widening only pays if a selector exists."

### QX-14 · Sparse s-of-K subset basis: the "last CVaR-VQE formulation standing" (S32 lane Q)
- **Problem:** A subset basis escapes all three S31 obstructions: it is diagonal, ⟨E⟩ is linear because the weights are solved classically inside E(x), and the dimension is 2^K.
- **Result (M):** The unconstrained convex optimum over K = 500 has support s* with mean 10.06 and max 23; 98.4% of targets have s* ≤ 20 (`s32` QR-4).
- **Load-bearing?** N/A (not built).
- **Falsified/weakened by:** The monotonicity closure. f*(s) is constant for s ≥ s* and worse below it, so "a quantum solver could only ever be needed to compute an answer a convex program already beats."
- **Unresolved:** E(x) needs `a`, which is ORACLE (condition B fails). **I(prog):** the closure is an argument that holds for any solver. It is the cleanest example of R2 generalised.

### QX-15 · Objective A (CVaR over a quality posterior) and Objective B (branch selection) (S32)
- **Result:**
  - Objective A reduces to a second-order cone program: convex, milliseconds.
  - Objective B per target is "argmax in quantum notation".
  - Objective B per residue, with a non-separable energy, is `2^{n_res}` and "blocked ONLY by chain length" (enumerable at 9–16 aa) (`s32` QR-5, QR-6).
- **Load-bearing?** N/A (derivation only).
- **Unresolved:**
  - **U:** per-residue branch selection with a non-separable energy at ≥ 40 aa (non-enumerable).
  - **But M:** no native-free branch selector reached MDE even over 158 branches, and the ORACLE best-branch ceiling is 96% order statistic (`s32` NR N-R3–N-R5). The discrimination signal is missing before any search question arises.

### QX-16 · Hull projection of a noisy external estimate (S32 QR-10)
- **Result (M):** Killed by a norm-matched shrinkage control. WORSE for ε ≤ 1.5 Å; better only at ε = 4.0 Å (ORACLE, cloud).
- **Load-bearing?** N/A. This was a readout candidate for a future information channel.

---

## B. Structural registers and distribution readouts (S33)

S33 simulator facts (M, `s33` Q-B2):
- A 6000-evaluation VQE on 168 qubits (MPS) took about 12–18 CPU-s.
- Statevector with adjoint gradient took 20.3 s per iteration at 22 qubits.
- Multithreaded BLAS never helped.

### QX-17 · E003 engine benchmark (QENG)
- **Problem:** Evaluation efficiency of CVaR-VQE on QUBOs.
- **Representation / algorithm:** 16-qubit dense QUBOs (6 instances); 60-qubit torsion chain; MPS χ 16, SPSA.
- **Classical comparator:** Greedy, steepest descent, SA, random.
- **Result (M):**
  - Evaluations to the exact optimum: VQE 980–2,664 vs greedy 19–85 vs SA 402–859.
  - At 60 qubits: SA with group moves reached −40.74 (exact, via chain DP) vs VQE −27.4 to −22.3, which was roughly the random level (−22.9) (`s33` Q-B1).
- **Load-bearing?** N/A.
- **I(src):** "VQE is 10–100× less evaluation-efficient than greedy"; "At equal budget the early CVaR-VQE *is* random sampling."
- **Status:** AD HOC. 6 instances, one seed each.
- **Category tested:** 3, in simulation. Negative.

### QX-18 · A10 subset register (S_mosaic, E100–E102)
- **Representation:** 16 qubits, enumerable.
- **Result (M):**
  - The brief's QUBO form has the wrong sign (condition C fails).
  - Chain sub_vqe 6.613 vs incumbent −0.618 (0.86×, NOT MEASURED).
  - VQE vs SA energy: 4/15/4.
- **Load-bearing?** **No.** I(src): "a hull readout".
- **Status:** Killed by condition C.

### QX-19 · A11 mosaic register (S_mosaic, E101/E103/E104/E107)
- **Representation:** 6 segments × 8 members, 18 qubits. E104 extended to 32 and 40 qubits.
- **Quantum algorithm:** MPS RY + CZ, L = 2, χ = 4, 256 shots/iteration, 60 iterations, budget 15,360.
- **Classical comparator:** SA (64 chains), greedy, random(prior), exhaustive 2^18.
- **Result (M):**
  - Energy at equal evaluations vs SA: 14W / 17T / 14L.
  - E107 chain: VQE_ref − SA_ref −0.012 (0.04×).
  - The warm-start mode alone (0 VQE iterations) gives the same answer.
  - At 40 qubits (11 targets) greedy/SA reach the lowest energy. VQE-L2 beats the product ansatz 8W/3L on energy, with no chain effect.
- **Load-bearing?** **No** (FAILED_E107). The adversary: "CVaR-VQE has a real role" REFUTED.
- **Unresolved:** **I(src), lane NOTES:** "A register where the VQE could matter must be non-enumerable AND hard for local search." No such register was found.

### QX-20 · A20/A21 fragment registers and the E230 short null (F_fragment)
- **Representation:** 16–18 windows × 32 fragments, 80–90 qubits (~4e25 states). E230 uses 15–35 qubits at 9–16 aa.
- **Quantum algorithm:** MPS L = 2, χ = 4, 128–512 shots, budget 40,000 distinct evaluations.
- **Classical comparator:** SA, prior-SA, a no-search control (esm5_ref), a trivial rule.
- **Result (M):**
  - E210 (n = 4, interrupted): VQE 8.419 vs SA 6.724 on the chain, with VQE higher in energy.
  - E222 (n = 45): vqe_ref − saX0_ref +0.177 (0.24×); vqe_ref − no search +0.175.
  - E230 (n = 126): VQE − SA +0.007; search vs no search −0.840 (2.40× RESULT). **SA delivers that equally.**
  - The F adversary: the trained VQE is lower in energy on 33/33 but not better than untrained sampling after refinement (+0.187).
- **Load-bearing?** **No** (FAILED_E222; the quantum null SURVIVES).
- **Falsified/weakened by:**
  - SA and prior-SA controls.
  - The collapse lemma: CVaR training is a correlated cross-entropy method, and collapse is absorbing, so VQE beats SA at small budgets and freezes at large ones (`s33` Q-D4).
- **Unresolved:** The F attack report was never finalised (draft only). The interim note that on 2GQV the VQE "finds a different, much better basin" (7 targets) was never carried into a final contrast.

### QX-21 · A30/A32 contact-subset and near/far registers (C_contact)
- **Representation:** One qubit per ESM contact (66–90 qubits).
- **Result (M):**
  - Condition C lower-half ρ is −0.038 against a 0.2 kill bar, so A30 was KILLED.
  - The A32 ORACLE register state is only 0.10 Å below the deployable decode, so it was NOT BUILT.
  - 41.8% of candidate contacts are already satisfied by the prior-only decode ("inert-qubit lemma") (`s33` Q-C6, Q-C7).
- **Load-bearing?** **No** / not built.
- **I(src):** "the natural place for a quantum register would be a decision the prior cannot make (none found here)."

### QX-22 · A33 CVaR-VQE tail as a DG restraint ensemble (E306): the tail-collapse exhibit
- **Representation:** Top-1.5n contact pairs, 69–90 qubits. MPS, 128 shots, budget 6,000. Tail = 12 lowest distinct states.
- **Classical comparator:** SA tail, greedy, random tail, prior draws, noise12 (no register).
- **Result (M):**
  - Chain VQE tail 5.816 vs SA tail 5.751 (+0.065, 0.72×, VQE worse) vs no-register noise12 5.681.
  - SA and greedy reach the register optimum on 45/45; VQE on 23/45.
  - Tail Hamming distance: VQE 2.4, SA 2.3, random 11.5.
  - Lower tail energy goes with higher RMSD (ρ −0.26) (`s33` Q-C8).
- **Load-bearing?** **No.** The pre-registered null was confirmed and SURVIVES, strengthened.
- **Mechanism:** Tail concentration destroys the diversity the ensemble readout needs. **This is not quantum-specific: SA tails concentrate equally.**

### QX-23 · A34 robust / joint CVaR over a predictor ensemble (E307, E312)
- **Result (M):**
  - The robust tail equals the prior-only decode.
  - The joint energy equals a classical optimistic energy (vqe_joint − sa_opt −0.008).
  - E312 chain −0.027 (0.04×, 16/45, interrupted).
- **I(src), D4 sign lemma:** a per-shot predictor draw makes lower-tail CVaR "risk-SEEKING."
- **Load-bearing?** **No.**

### QX-24 · A41 CVaR-VQE on the per-residue (θ,τ) head8 register (P_prior E405/E406; H_hybrid E1001; E406V)
- **Problem:** Optimise per-residue discrete backbone geometry under the learned prior energy E_P.
- **Representation:** (L−3) × 3 qubits = **123–171 qubits** (the largest S33 register). Condition C passed (ρ 0.73–0.81, ORACLE).
- **Quantum algorithm:** MPS RY + CZ, 2 layers, χ 4, 32 shots, α 0.5 → 0.1, Adam, budget 6,000 distinct structures. VQE had 11 tuning configurations.
- **Classical comparator:**
  - E406: lane SA (3 configurations × 2 seeds, untuned T0), greedy, random, product ansatz.
  - E406V: SA tuned over 9 configurations.
  - E1001: SA tuned over 10 configurations, the same effort as the VQE.
- **Result (M):**
  - E406: VQE 3.057 vs untuned SA 3.222 (41/45 better).
  - E406V: VQE vs tuned SA 3.057 vs 3.064 (+0.007, 0.18×, a tie).
  - E1001: tuned SA 3.394 < VQE 3.457 (3 dev targets).
  - Raw chain VQE − SA −0.291 (0.33×).
- **Load-bearing?** **No.** "The energy claim is REFUTED" (REPORT); "WEAKENED to a tie" (one adversary instance).
- **Falsified/weakened by:** **Equal tuning effort.** This is the source's key methodological lesson (`s33` LESSONS 1).
- **Category note (I(prog)):** this was the nearest the predecessor came to a category-3 claim (better energy at equal budget on a 123–171-qubit register). It dissolved under equal tuning.

### QX-25 · A100 hybrid: A41 tail relaxed under the A80 energy (H_hybrid E1000–E1007) and A101 pool
- **Problem:** Does the A41 register search improve the built chain once the tail is relaxed by the continuous decoder?
- **Representation:** head8 register (≤ 171 qubits). 16-state tail, 150 L-BFGS steps each.
- **Quantum algorithm:** The E406 CVaR-VQE (6,000 E_P evaluations).
- **Classical comparator:** Tuned SA (equal tuning), SA_p, **random_min (untrained warm-start circuit)**, product ansatz, **register-free A80 at matched CPU**, tuned parallel tempering (adversary).
- **Resources (M):** About 12–18 CPU-s per 6,000-evaluation VQE on 168 qubits. Distinct evaluations: VQE 5,967 vs tuned SA 5,969.
- **Result (M):**
  - Seed 0 long40 P1 (vqe − tuned SA) −0.824 (0.84×, NOT MEASURED; median −0.07).
  - Seed 1: −0.066 (0.05×). 2-seed: −0.445 (0.43×).
  - **2-seed vqe − random +1.035 (1.35× RESULT, VQE WORSE).**
  - vqe − register-free +0.793 (0.90×, wrong way).
  - A101: removing the quantum tails changes 4.356 → 4.352.
  - Transmission: ρ(E_P, chain) −0.08. Same-solver chains move > 2 Å between seeds on 27% of targets (random: 0%) (`s33` Q-C12–C14).
- **Load-bearing?** **No.** FAILED_E1000; the null SURVIVES a 4-seed adversary. Tuned parallel tempering "does not change the picture."
- **I(src):** "a topology-trap lottery". The adversary rated this mechanism "partly definitional (WEAKENED)."
- **Unresolved:**
  - Trap counts: VQE 6/9/7/6 vs tuned SA 13/10/9/15 (Wilcoxon p 0.015).
  - The 4-seed cloud P1 is −0.571 (0.81×, NOT MEASURED).
  - **U:** whether fewer topology traps is a real, reproducible property of the circuit's distribution or a seed effect. The random prior sampler had 0 traps, so broad sampling dominated anyway.

### QX-26 · A51 / A53 short-length registers (X_short E503, E513, E518V)
- **Representation:** A51 mosaic, 9–12 qubits, exhaustive. A53 chiral (θ,τ), 18–39 qubits, MPS, 512 shots, 12k evaluations.
- **Result (M):**
  - A51: condition C fails (in-band ρ −0.011), so it was killed with no VQE compute.
  - A53 full n = 126: VQE tail +0.243 vs production (1.16× WORSE); VQE − SA −0.006; **VQE − random +0.070 (1.02× RESULT, random better).**
- **Load-bearing?** **No.** The kill was CONFIRMED at full n. Round 1 (n = 12) was "a favourable draw."
- **I(src):** "at 9–16 aa the quantum stage is either decorative (A fails) or optimises an energy that does not know the answer (C fails)."

### QX-27 · A60 exactly enumerated mid-length mosaic (M_mid E604, E609)
- **Representation:** 18 qubits (262,144 states), enumerable in about 20 s. Budget 2,000 evaluations (0.76% of the space).
- **Result (M):**
  - Chain: exact 6.341 ≈ SA 6.358 ≈ VQE 6.431.
  - P(found exact optimum): greedy 54%, VQE 27%, SA 24%.
  - Adversary: random at equal budget ties VQE (+0.041, 0.08×).
- **Load-bearing?** **No.** "Decorative by construction" (condition A fails).

### QX-28 · A70 exact Gibbs posterior-mean readout (H-Q1; T_tempered E700/E701)
- **Problem:** Does a posterior-mean readout of a tempered distribution beat the argmin?
- **Representation:** R60 18-qubit mosaic, exact over 262,144 states.
- **Quantum algorithm:** None. This is the exact target a quantum sampler would approximate.
- **Classical comparator:** Argmin, perturb-and-MAP, CVaR tail.
- **Result (M):**
  - Chain Gibbs − argmin: −0.170 (0.33×, mid30) and −0.159 (0.47×, long40).
  - The cloud gain is mostly contraction, which projection removes (+0.20 penalty vs +0.01).
  - **But soft Boltzmann beats hard CVaR tails on the mid30 chain: −0.248, 1.40× RESULT (T adversary).**
- **Load-bearing?** N/A (H-Q1 falsified on R60).
- **Unresolved (U):** whether posterior readouts over non-enumerable, length-scaling spaces help on the chain.

### QX-29 · A71 tempered Born machine vs Metropolis twin (T_tempered E710)
- **Problem:** Can a circuit sample the tempered distribution better than MCMC?
- **Representation:** R60 18-qubit mosaic.
- **Quantum algorithm:** Tempered Born machine (⟨E⟩ − T·S). Exact statevector L = 3 (72 parameters) and sampled MPS L = 2, χ 4, 256 shots/step, budget 15,360.
- **Classical comparator:** A Metropolis twin at matched budget, plus the exact Gibbs mean.
- **Result (M):**
  - Distance to the exact Gibbs mean: tempered Born machine 2.08 Å vs Metropolis 0.73 Å. Metropolis is closer on 9/10 (1.08× RESULT against the circuit).
  - The plain CVaR tail collapses to one state (`s33` Q-C19).
- **Load-bearing?** **No.** "Dominated by, not equal to, its classical twin."
- **Category note (I(prog)):** this is the **only** S29–S33 experiment shaped like a **category-4 (sampling)** test. It ran on an 18-qubit space that exact enumeration solves, where Metropolis mixes easily. It says nothing about sampling where MCMC is slow. E720 (A72, 32 qubits) was **NOT RUN**.

### QX-30 · A81 / A81m discrete (θ,τ) macro registers around a learned energy (D_decoder E800/E810/E811)
- **Problem:** Make CVaR-VQE load-bearing by giving it the global nonconvex search of a strong learned energy.
- **Representation:** A81m macro4: 106–114 qubits (long40), 44–74 (mid30). Coverage 100%, but polishing the ORACLE bits gives 5.11 Å, worse than the register-free decoder.
- **Quantum algorithm:** MPS L = 1, χ 2, 128 shots, α 1 → 0.1, 8,192 evaluations.
- **Classical comparator:** The register-free continuous decoder A80 (rf); SA with 128 chains (untuned); greedy; random prior sampling.
- **Result (M):**
  - long40: register best − rf +0.364 (0.60×, wrong way).
  - mid30: vqe − rf +0.807 (1.04× RESULT, WORSE).
  - Energy: VQE ties random prior sampling (−3.9 nats, 27/45, p 0.23). Greedy beats it on the raw objective.
- **Load-bearing?** **No.** H-a fails on both instruments. "Best register solver" REFUTED.
- **Falsified/weakened by:**
  - The register-free decoder.
  - Random prior sampling.
  - Raw → polished rank correlation 0.00, so condition C must be checked on the **readout** energy.
- **Unresolved:** Restart saturation: 32–64 restarts solve the continuous problem, bounding any global search gain to ≤ 0.14 Å (6 dev targets, cloud).

### QX-31 · A82 RF-seeded macro register around the decoder's residual uncertainty (D_decoder E813/E814)
- **Status:** Implemented and pre-registered, **NOT RUN** (`s33` Q-C21).
- **Pre-registered design (I(src)):**
  - Register around the decoder's answer.
  - Twins: equal-tuning SA, random-prior sampling, product ansatz.
  - Primary contrast: VQE − random-prior tail on the relaxed chain.
  - Kill if condition C fails near the decoder's answer, or if random ≤ VQE.
- **I(prog):**
  - The design inherits R2 and R10: a register can beat only a heuristic decoder, never an exact one.
  - The H_hybrid lesson applies too: "a VQE could at best match the prior sampler there (distribution-equivalence lemma)" (`s33` LESSONS 39).
  - The prior probability that it becomes load-bearing is low. It is still the cheapest pre-registered quantum re-test available, so it is recorded as a candidate, not a plan.

### QX-32 · A90 final composite with an 18-qubit mosaic CVaR-VQE stage (Y_synth E900–E903)
- **Result (M):**
  - long40: A90 − SA twin +0.026; A90 − no stage +0.110.
  - mid30: A90 − no stage −0.262 (0.95×, NOT MEASURED). The SA twin does the same (−0.393 RESULT).
  - Adversary ordering: dg 4.730 < none 4.808 < sa 4.891 < random 4.902 < vqe 4.926 ("A90 is its own worst ablation").
  - Condition C fails (+0.109, +0.018).
- **Load-bearing?** **No.** I(src): "the gain belongs to the discrete search, not to the quantum solver." The adversary re-attributes it to "register CONTENT + energy-ranked tail — not search."

### QX-33 · Cross-cutting ablations: entanglement and α
- **Entanglement (M):**
  - Energy: VQE-L2 vs product ansatz 8W/3L at 40 qubits.
  - Chain: vqe − product −0.688 (0.60×) at seed 0; 2-seed −0.188 (0.26×); mid30 +0.008.
  - **I(src):** "Entanglement changes which basins are reached, not how good they are."
- **α (M):** α → 1 worsens A41 energy (3.69 vs 3.27, 10/10). **I(src):** "α is load-bearing inside the optimiser … but the readout is solver-agnostic."

---

## C. Summary matrix

| Family | Records | Largest register | Strongest classical twin that matched or beat it | Load-bearing |
|---|---|---|---|---|
| Candidate-index CVaR-VQE (deployed) | QX-01, 05, 06, 10, 12 | 9 qubits | Closed-form p*, fixed profile, sort | No |
| Non-diagonal on the candidate register | QX-02, 07, 11 | 9 qubits | `eigh`, order-statistic nulls | No / not built |
| Distribution readouts over the candidate register | QX-03, 09, 14, 15, 16 | 9 qubits (2^500 subset space, not built) | Free subset search, convex programs, SOCP, shrinkage | No / not built |
| Configuration space + transverse field | QX-04 | 15 qubits | SA, BESTOFN | No |
| Structural registers (subset/mosaic/fragment/contact) | QX-17–23, 26, 27, 32 | 90 qubits | SA, greedy, exact, random prior, no-search | No |
| Per-residue geometry registers | QX-24, 25, 30 | 171 qubits | Equal-tuning SA, random prior, register-free decoder | No |
| Sampling / tempered distributions | QX-28, 29 | 18 qubits | Exact Gibbs, Metropolis | No (sampling case untested at scale) |
| Pre-registered, never run | QX-31 (A82), E720 (A72, 32 qubits) | — | — | Unknown |
