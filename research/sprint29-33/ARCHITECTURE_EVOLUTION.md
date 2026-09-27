# S29–S33 architecture evolution

_Synthesis, 2026-09-26. Tags: **M**, **I(src)**, **I(prog)** and **U**, as in `README.md`. Quantum experiments are detailed in `QUANTUM_RESULTS.md` (QX-ids)._

## 0. The pipeline the sprints inherited (M)

Production at S29, which is unchanged through S33 on `tuning126` (`s29` README; `s32` QR resource table; `s33` Q-A2):

```
sequence ─► BLOSUM retrieval of fragments ─► pool of 500 candidates (CA traces)
         ─► distogram score (DIS) ─► filter 500 → top-75
         ─► readout: uniform coordinate average of the 75
         ─► projection to an ideal-geometry chain (λ = 0.3, multi-start argmin over branches)
         ─► built chain (endpoint)
```

- **The optional quantum stage** (`quantum=False` in production):
  - Takes the top 2^n (n = 7, i.e. 128) candidates by score.
  - H = diag(zrank(score)).
  - Minimises the CVaR_α − T·H(p) free energy with a 3-layer RY/CNOT statevector circuit.
  - Readout: the tail-set or probability-weighted average.
- **I(prog).** Architecturally, the quantum stage was a **weighting rule over an already-filtered candidate list**. It sat downstream of every information source and upstream only of averaging and projection.

## 1. Sprint-by-sprint trajectory

### S29: "find the path below 2.5 Å" with CVaR-VQE central
- **Charter (M):** "CVaR-VQE remains the main scientific object, not a decorative final stage." "Removing or randomizing the quantum stage measurably degrades the result" (`s29` README).
- **Architectures probed:**
  - (a) the deployed stage vs a fixed profile (QX-01);
  - (b) a non-diagonal compatibility Hamiltonian (QX-02);
  - (c) tail-then-aggregate (QX-03);
  - (d) a new state space, fragment chimeras, with a transverse-field mixer (QX-04).
  - Classical: 21 displacement fields, the projection bond correction, the selection functional (log score), realism-band ordering, the shell-profile supply gap. All failed (`s29` NR B1–B22).
- **Outcome (M):** The endpoint was unmoved. The deployed quantum stage is equivalent at the endpoint to one global integer m. The ORACLE ceiling of the quantum architecture is 2.9027 Å, so 2.5 Å was "unreachable through this architecture *even with an oracle*."
- **What changed next (I(src)):** Attention moved from the circuit to the objective and the information entering it.

### S30: "find the first real accuracy breakthrough"
- **Architecture (M):** No CVaR-VQE was trained. A 9-qubit circuit ran only to show that the same circuit reaches 0.2516 Å on an ORACLE objective and 3.4330 Å on the deployed one (QX-06).
- **Theorem T1:** the tail is always a prefix (`s30` Q2).
- **Endogenous-order escapes:** the halfspace and quadric lifts were measured and closed before any Hamiltonian was built (QX-07).
- **Classical work:** recognition, the common-mode theorem, prior correction, the tail (FAIL18).
- **Outcome (M):** 91 hypotheses: 58 killed by measurement, 19 by theorem, 8 by price, 6 open.
- **Key numbers:** Five ORACLE signs are worth −0.3259 Å. The per-target coefficient problem needs about 6 numbers (`s30` H2, Q9).
- **What changed next (I(src)):** "The circuit is not the problem. The objective is."

### S31: the objective and the readout
- **Architecture (M):** The deployed objective is convex with a closed-form p* (QX-10). The Hamiltonian is target-independent. Three readouts were distinguished: selection, convex (shipped) and affine (harness only).
- **Readout identity:** ‖Σw_xW_x − t‖² = ⟨w,a⟩ − ½w'Bw.
- **Closed by theorem:** non-diagonal Hamiltonians on the candidate register and ADAPT (QX-11).
- **Outcome (M):** The endpoint was unmoved. The only live deployable candidate (AVG_SEP) was +0.4609 Å WORSE.
- **I(src):** "The bottleneck was stated backwards." Correcting along the common mode is the prize (ORACLE −0.81 Å), and the common mode is unpredictable.
- **What changed next:** Search for an information source for the common mode "that does not come from the pool."

### S32: where the RMSD is lost
- **Architecture (M):** No new circuit. Lane Q derived the following:
  - the readout is a hull projection (R5);
  - a ≡ μ (R6);
  - sparse s-of-K is the last formulation standing, closed by monotonicity (QX-14);
  - Objective A reduces to an SOCP and Objective B to an argmax (QX-15);
  - P1 ∧ P2 are required for any quantum role (R8).
- **New instrument:** `long40` (45 targets, 44–60 aa) was built.
- **Outcome (M):** Zero deployable built-chain improvements.
- **I(src):** "NO on this instrument, and the binding reason is chain length." Next direction: "Go longer."

### S33: maximum-freedom sprint, length-scaled
- **Charter (M):** "SACRED: … protein folding centred on CVaR-VQE with a meaningful (non-cosmetic) quantum role. Nothing else is sacred."
- **New instrument:** `mid30` (41 targets, 25–40 aa).
- **New learned component:** esmprior_v1 (A40), a 2D dilated ResNet on ESM-2 650M features giving 28-bin CA/CB distance distributions and a per-residue (θ,τ) head, trained on 600 leakage-safe crops.
- **Architecture families (M; 36 IDs, `s33` README §3.3):**
  1. Structural CVaR-VQE registers: A10, A11, A20, A21, A30, A32–A34, A41, A53, A60, A70/A71, A81/A81m, A82, A100.
  2. Learned priors and selectors: A40, A50, A54, A55, A61, A62.
  3. Decoders: A12, A31/A31.2, A80.
  4. Distribution readouts: A33, A70, A71.
  5. Compositions: A90, A91, A100, A101.
  6. Short-length nulls and transfers.
- **Outcome (M):**
  - tuning126 unbeaten.
  - long40 9.745 → 4.739 (E308) / 4.343 (A80, tie).
  - mid30 8.180 → 3.717 / 3.815.
  - All headline architectures are quantum-free. Every quantum stage tested was inert or harmful (QX-17–QX-32).

## 2. The quantum stage's shrinking role (I(prog), built from M above)

| Sprint | What the quantum state represented | What the classical twin was | Why it failed (source mechanism) |
|---|---|---|---|
| S29 | A distribution over 128–512 candidate indices | A fixed prefix m; exact eigensolver; free subset search | Prefix theorem; endpoint ≡ one integer |
| S30 | (not trained) | Sort; Frank–Wolfe; order-statistic nulls | T1; objective, not circuit |
| S31 | Same; exact optimum known | Closed-form p* (bisection) | Convex program; circuit strictly worse |
| S32 | Proposed: subset, per-residue branch | Convex program; SOCP; argmax | Monotonicity; enumerable at 9–16 aa |
| S33 | Structural registers up to 171 qubits | SA (equal tuning), greedy, exact, **random prior sampling**, register-free decoder, Metropolis | Solver-equivalence; tail collapse; non-transmission; restart saturation; condition C |

**I(prog).** The trajectory runs from "the circuit computes nothing classical cannot" (S29–S32, small registers) to "the circuit computes a hard-looking problem whose answer does not matter for the endpoint" (S33, large registers). At no point was a quantum computation both (a) classically expensive at the problem sizes used and (b) on the path of information that changes the built chain.

## 3. The architectures that actually moved the endpoint (quantum-free; M)

| ID | Instrument | What it is | Result (DEP) | Status |
|---|---|---|---|---|
| A00 production | tuning126 | BLOSUM retrieval + DIS top-75 average + projection | 3.2105 | Unbeaten S29–S33 |
| E001-ESM | long40 / mid30 | ESM-2 contact-agreement top-5 average | 7.231 / 7.815 | Phase-1 incumbent, superseded |
| A62 | mid30 | ESM log-likelihood narrow selection | 5.948 | Superseded; "zero-parameter" claim WEAKENED |
| A31.2 / **E308** | long40 | Distance geometry on esmprior_v1 + θ/τ mirror + 12-decode mean + template gate | **4.739** (ungated 5.136) | Most verified; REPRODUCED 45/45; clean in 3 leakage audits; mechanism WEAKENED (asserted contacts inert) |
| **A80** | long40 / mid30 | Register-free L-BFGS decoder on the esmprior energy, 32–64 restarts, + template gate (rf / rfp) | **4.343** long40 (tie with E308, 0.66×); **3.717 / 3.815** mid30 | Tie SURVIVES; mid30 vs A90 WEAKENED after correction; E812 at tuning126 +0.296 WORSE (interim) |
| A90 | long40 / mid30 | DG + mosaic CVaR-VQE + refine + gate | 4.915 / 4.304 | Superseded; its own worst ablation |

**M. Mechanism of the gains:**
- The learned pair prior (the prior swap alone gave 5.681 → 5.136).
- Decoding into coordinates instead of selecting from a pool.
- Template gating: never relax a good template.
- Diversity-preserving averaging of decodes.

**I(src).** "The next lever is more of that information, not more search." Planned next: esmprior_v2 (E407), cancelled for RAM.

## 4. Length changes the problem (M, `s33` README H7)

| Length | Winning operator | ESM-2 P@L/5 | Quantum-relevant fact |
|---|---|---|---|
| 13 aa | Averaging (production) | 0.53 | Registers enumerable (2^n_res ≤ 65,536); condition C fails |
| 33 aa | Narrow selection → decoding | 0.66 | 18-qubit mosaic enumerable in ~20 s; greedy ≥ VQE |
| 55 aa | Decoding | 0.74 | 106–171-qubit registers not enumerable, but restart-saturated continuous search; energies do not transmit |

**M.** Every long-length mechanism transferred to 9–16 aa was harmful: E105 +0.344, E504a +2.137, E606 +0.288, E511 +0.164, E812 +0.296 (interim).

**U.** Nothing is known beyond 60 aa. Whether restart saturation, the information floor and non-transmission hold at 100–300 aa is untested. This is the largest scope gap in the inherited evidence.

## 5. Lessons for architecture design in this program (I(prog), each grounded in M above)

1. **Placement.** A quantum component placed downstream of all information sources, acting as a selector or weighter over classical candidates, is bounded by R1, R2, R4 and R5. Its best case equals a classical convex program or sort.
2. **Condition C.** A quantum search over a register must first pass condition C **on the readout energy** (raw → polished ρ 0.00 in D_decoder). It must also beat the **register-free** decoder, which can be beaten only if that decoder is heuristic (R10).
3. **Twins.** The decisive twins were **random prior sampling** and **equal-tuning SA**, not greedy or untuned SA. Any future comparison without them is not admissible.
4. **Distributions.** Distribution-level readouts help when they are *diverse* (soft Boltzmann, averaging, random prior). This is the one direction where the output of a sampler, rather than its argmin, mattered on the chain. It is also where the classical twin (Metropolis) won at 18 qubits.
