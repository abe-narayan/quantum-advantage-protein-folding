# Quantum Opportunity Map

_Version 1, 2026-09-26. Built from the S29–S33 synthesis (`research/sprint29-33/`). No experiments have been run in this program yet. Tags: **M** measured (pointer into `research/sprint29-33/` or the per-sprint imports), **I(src)** the predecessor's interpretation, **I(prog)** this program's reasoning, **U** untested._

**Stance.** This map does not assume a quantum advantage exists, and it does not privilege VQE, QAOA or any other algorithm. The most likely outcome of the program, on current evidence, is that the protein-structure endpoint at the predecessor's lengths is information-limited and no quantum primitive is load-bearing there (H-002). The map is built to find the places where that expectation could be wrong **and can be tested cheaply**, starting with classical measurements.

**Gate rule.** No quantum component is built for any item below until its **classical kill test** has been run and has *failed to kill* it. A quantum build without a demonstrated classical computational gap repeats the predecessor's pattern (DNR-02, DNR-07).

---

## 1. Bottlenecks that remain genuinely computational

"Computational" here means **not yet shown to be information-limited**, with a plausible cost that grows with problem size. **No item below has a measured computational gap.** Each is computational in *form* only.

| ID | Bottleneck | Evidence | Why it is not (yet) information-limited | Classical kill test |
|---|---|---|---|---|
| C-1 | **Sampling the posterior over structures** under a learned pair-distance energy at ≥ 33 aa | **M:** the soft Boltzmann readout beats the hard tail on the mid30 chain (1.40× RESULT); averaging 12 decodes beats selecting one; random prior sampling beats concentrated solvers (QX-25, QX-28; `s33` N26) | The *value* of good samples is shown at mid30. The *cost* of producing them is unmeasured (OP-01). | Measure integrated autocorrelation, parallel-tempering round-trip times and ESS per CPU-second vs chain length (30 → 60 → 100+ aa). Also measure whether sample quality transmits to the chain. |
| C-2 | **Global search on learned energies beyond 60 aa** | **M:** saturated at 44–60 aa (32–64 restarts; ≤ 0.14 Å headroom, 6 targets, cloud) (QX-30) | Untested beyond 60 aa (OP-02). Nonconvexity may grow with length. | Extend the restart-saturation curve and the decoder − information-floor gap to more targets and to 80–150 aa. Kill if the gap does not grow or restarts keep closing it. |
| C-3 | **Estimating ensemble expectations** (basin populations, free-energy differences) | **U:** no decision has been shown to be variance-limited (OP-07) | Never audited | Vary the sample count for every ensemble-derived decision and check whether decisions change. Kill if decisions are stable at feasible counts. |
| C-4 | **Per-residue non-separable discrete choices at length** (branch or rotamer-like), 2^n_res | **M:** enumerable at 9–16 aa; no native-free discriminator at short length (QX-15) | Untested at ≥ 40 aa (OP-06). Likely discrimination-limited (**I(src):** "SEARCH IS NOT THE BARRIER; DISCRIMINATION IS"). | First measure an ORACLE branch ceiling at length *with* an order-statistic null. Kill if it is order-statistic dominated, as at short length (96%). |
| C-5 | Training larger learned priors (esmprior_v2) | **M:** RAM-bound; "the top classical lever" (`s33` N31) | Classical ML compute | Not a quantum target (see §7) |

## 2. Bottlenecks already shown to be information-limited

| ID | Bottleneck | Evidence (M) | Strength |
|---|---|---|---|
| I-1 | The tuning126 endpoint (9–16 aa) as a whole | All native-free channels null or wrong-signed. Every long-length mechanism is harmful when transferred. ORACLE headroom needs per-target information. | Strong, but "inductive, not a theorem" (`s33` N12) |
| I-2 | Per-target sign / common mode μ / ~33–39 real numbers | a ≡ μ (R6). Hull projection gain 1/0 (R5). Neyman–Scott incidental parameter. Native-free cos(μ̂, μ) ≤ 0.057 vs 0.21 needed. | Strong (theorem + measurement) |
| I-3 | Readout from a candidate pool (weights, prefix m, sparse s-of-K, convex/affine) | R4, R5, R11. Prefix m is an order statistic. The p* substitution is null. | Strong (theorem + measurement) |
| I-4 | In-band ranking / recognition from single structures, physics scorers, chirality, consensus | 43 channels. G1 theorem. AMBER in-band ρ 0.000. Chiral beaten 4:1 by achiral. | Strong at 9–16 aa; untested at length |
| I-5 | The long-length decoder at 44–60 aa | Decoder 4.35 vs information floor 4.21 (6 dev targets, cloud). Prior quality moved every decoder. | **Moderate** (small n, cloud basis) |
| I-6 | Structural-register energies (E_P, mosaic, contact, fragment) as selection signals | Condition C fails on the readout energy. Within-target ρ(E_P, chain) −0.08. | Strong at the lengths tested |

**I(prog).** No quantum primitive creates information that is absent from its inputs. For I-1 … I-6 a quantum component can at best compute the same function of the same inputs. For quantum learning models this is the data-processing inequality. I-5 is the only item whose information-limited status is weakly established. Upgrading or refuting it is part of C-2's kill test.

## 3. Search problems where the classical method appears saturated

| ID | Search problem | Saturating classical method (M) | Pointer |
|---|---|---|---|
| S-1 | CVaR / free-energy optimum over a candidate-index distribution | Closed-form p* (one bisection); sort | QX-10; R1, R4 |
| S-2 | Diagonal register optima ≤ ~2^24 states | Exact enumeration (2^18 in ~20 s) | QX-27, QX-26 |
| S-3 | Structural register optima at 16–171 qubits (mosaic, contact, fragment, (θ,τ)) | SA with equal tuning, greedy (reaches the optimum 45/45 in E306), random prior sampling | QX-22, QX-24 |
| S-4 | Continuous CA-trace decode at 44–60 aa | L-BFGS with 32–64 restarts | QX-30 |
| S-5 | Branch selection in projection | Multi-start argmin (≈ a coin, but no discriminator exists either) | `s32` N-R7 |
| S-6 | Set / subset selection for readouts | Frank–Wolfe, NNLS/QP, SOCP (milliseconds) | QX-14–16; `s30` Q6 |
| S-7 | Chain-structured (1D-local) discrete energies | Dynamic programming (exact; SA with group moves matched chain DP at 60 qubits) | QX-17 |

**I(prog).** For S-1 … S-7, quantum optimisation (VQE, QAOA, annealing, amplitude-amplified search) has **no room**. The classical method is exact, or empirically at the optimum, at the relevant sizes. A quadratic query speedup over an exact polynomial or already-converged method does not matter.

## 4. Sampling problems that remain interesting

| ID | Sampling problem | Why interesting (M) | Why not yet a quantum opportunity (I(prog)) | Classical twin to beat |
|---|---|---|---|---|
| SP-1 | **Boltzmann / posterior over decoded CA traces** under the esmprior energy at 33–150 aa | The soft readout beats the hard one (mid30, 1.40×); diversity beats selection | Classical mixing never measured. At 18 qubits Metropolis was near-exact. | Parallel tempering, replica exchange, SMC, HMC on continuous coordinates |
| SP-2 | **Multimodal topology landscapes** (topology traps) | Concentrated solvers fall into traps; the random prior sampler has 0 (QX-25) | The broad classical sampler already avoids traps. The useful sampler is *diverse*, which classical priors provide cheaply. | Random prior sampling + relaxation; PT |
| SP-3 | **Ensembles for elongated / non-globular targets** (5AL6 class) | DG fails even with native contacts; A80 rescued one (OP-14) | Probably representation- or energy-limited, not sampling-limited (**U**) | A80 multi-restart; enhanced sampling |
| SP-4 | **Tempered distributions over non-enumerable discrete spaces** (A72, 32+ qubits) | The 18-qubit version was dominated by Metropolis | E720 not run. No evidence that MCMC fails there. | Metropolis with equal budget; exact where feasible |

**I(prog).**
- A **category-4 (sampling advantage)** claim needs two things together:
  - (i) a target distribution whose samples demonstrably improve the endpoint (only SP-1 has partial evidence);
  - (ii) demonstrated classical slow mixing on that distribution (no evidence anywhere).
- Both are measurable classically. SP-1 is therefore the most defensible sampling line, conditional on C-1's kill test.

## 5. Candidate problems with possible quantum **query** advantages

These separations are provable in an oracle/query model (category 6). They are relevant to this program only if the subproblem is actually oracle-like **and** the query cost dominates wall-clock (category 3). Oracles must be **native-free**: an oracle that marks "near-native" structures is leakage and is forbidden.

| ID | Primitive | Subproblem it would address | Known separation | Precondition from the evidence | Current verdict |
|---|---|---|---|---|---|
| QA-1 | **Amplitude estimation** | Estimating ensemble expectations (C-3) | O(1/ε) vs O(1/ε²) samples | Some decision must be variance-limited (C-3 kill test must fail) | **Conditional, low prior.** Every inherited bottleneck is bias- or information-limited, not variance-limited. |
| QA-2 | **Amplitude amplification / Grover** over candidate or fragment spaces | Finding low-energy configurations | Quadratic in unstructured queries | The space must be unstructured and non-enumerable, and the energy must pass condition C | **Probably dead** (S-2, S-3, S-7: structure is exploitable; condition C fails) |
| QA-3 | **Quantum-walk search / hitting time** (Szegedy, MNRS) | Marked-configuration search on a Markov chain | Quadratic in 1/(δε) | Requires native-free marking plus a slow classical hitting time | **Conditional** on C-1 / C-2 showing slow classical dynamics |
| QA-4 | **Quantum backtracking / branch-and-bound** (Montanaro) | Exact search over large discrete trees (C-4) | ~quadratic in tree size | Exact solutions must matter and exceed classical reach | **Conditional, low prior** (discrimination-limited at short length) |

## 6. Candidate problems with possible **asymptotic** advantages

| ID | Primitive | Addresses | Separation (literature) | Precondition | Current verdict |
|---|---|---|---|---|---|
| AA-1 | **Quantum MCMC / quantum walks for mixing**; quantum simulated annealing | SP-1, SP-4 (classical Boltzmann sampling) | Quadratic in the spectral gap, 1/√δ vs 1/δ (category 3/6) | Measured classical δ must shrink fast with length (C-1 kill test), and samples must transmit to the chain | **Most defensible candidate.** Entirely conditional. Needs fault-tolerant resource estimates before any claim. |
| AA-2 | Amplitude-amplified classical heuristics (quadratic speedup of SA/PT restarts) | C-2 (search beyond 60 aa) | Quadratic in the number of restarts or trials | Restarts must stop saturating at length (C-2) | **Conditional** |
| AA-3 | **Hamiltonian simulation / phase estimation for electronic structure** | QM energies for strongly correlated sites (e.g. metal centres) | Exponential over exact classical methods for strongly correlated systems | Energy accuracy must be the endpoint bottleneck. **M:** it is not at the lengths tested (AMBER in-band ρ 0.000; physics as mover is a random direction) | **Out of the S29–S33 evidence scope.** Not supported as a structure-accuracy lever. Recorded so it is not rediscovered without this context. |
| AA-4 | QSVT / quantum linear algebra | Readout QPs, convex programs, hull projections | Poly-log in dimension under access models | Problem sizes are D ≤ 500 and solve in milliseconds (S-6); dequantisation applies to low-rank cases | **Dead end** |

## 7. Candidate problems where a quantum approach is probably a dead end

Each entry cites its reason. The DNR ids point to `research/sprint29-33/NEGATIVE_RESULTS.md` Part 2.

| ID | Direction | Reason (M / theorem) |
|---|---|---|
| DE-1 | Variational optimisation (VQE, QAOA, CVaR, ADAPT) of diagonal costs with argmin, prefix or convex readouts | R1, R2, R4; 34 S33 contrasts, none favourable (DNR-01, 02) |
| DE-2 | Any quantum stage over a candidate-index register | Dimension counting; closed-form p*; target-independent H (DNR-01, 09) |
| DE-3 | Quantum search on enumerable or local-search-easy registers | S-2, S-3, S-7 (DNR-03) |
| DE-4 | CVaR-tail ensembles as readouts | Tail collapse; SA tails equally concentrated (DNR-04) |
| DE-5 | Quantum solvers for the readout/selection convex programs | S-6: classical milliseconds (DNR-18) |
| DE-6 | Quantum ML / quantum generative models to supply missing per-target information (sign, μ, ~39 numbers) | Information-limited (I-1, I-2). A learner cannot create information that is absent from its inputs. The MPS Born machine is classically simulable; the random prior sampler beat the trained circuit. |
| DE-7 | Quantum computation of physics energies to improve ranking at 9–60 aa | Physics scorers carry no in-band skill. Physics as mover is indistinguishable from a random direction (`s32` N-D1–N-D6). |
| DE-8 | Coarse lattice (HP-model) folding on quantum hardware as a proxy for structure accuracy | The proxy energy would have to pass condition C. The inherited coarse energies fail it. At best this gives a category-6 or toy result disconnected from the endpoint (I(prog)). |
| DE-9 | Entanglement / ansatz / depth / optimiser tuning of any of the above | No chain effect; not the bottleneck (QX-05, QX-33) |

---

## 8. The most promising experimentally testable opportunities (ranked)

The ranking is by (evidence that the question is open) × (cost to decide) × (whether a positive answer would open a quantum route with a known separation). All first steps are **classical** or **theoretical**.

| Rank | Opportunity | First step (classical / theory) | Kill criterion (draft, to be pre-registered) | If it survives → quantum step | Claim category reachable |
|---|---|---|---|---|---|
| 1 | **H-001 reduction theorem**: formalise when a quantum stage is classically reproducible | Write it in `theory/`: argmin, prefix and convex-functional consumption of diagonal-energy distributions ⇒ classical reproduction; list the necessary conditions for load-bearing | A counterexample within the class, found in the predecessor's own evidence | A screening checklist every architecture must pass | 6 (negative/structural) |
| 2 | **Sampling hardness of learned-energy posteriors vs length** (C-1, SP-1, AA-1) | New leakage-controlled long-chain instrument (60–150 aa). Best-tuned PT, replica exchange and SMC. Measure τ_int, round-trip times, ESS/CPU-s, gap estimates. Also measure the chain value of better samples (soft vs hard readout). | (a) Mixing time polynomial and within budget at all lengths, **or** (b) better sampling does not improve the chain beyond MDE | Quantum-walk / QMCMC resource estimates (qubits, T-count, oracle cost) vs the measured classical δ(L). Crossover-length estimate. | 3 / 4 / 6 |
| 3 | **Search gap vs length** (C-2, AA-2) | Replicate E800b saturation and the information floor on more targets (≥ 20) at 44–60 aa, then extend to 80–150 aa | Decoder − floor gap ≤ noise and not growing; restarts keep saturating | Amplitude-amplified restart / backtracking resource estimate | 3 / 6 |
| 4 | **Variance audit of ensemble-derived decisions** (C-3, QA-1) | Vary sample counts for every stochastic quantity in the best classical pipeline | No decision changes at feasible counts | Amplitude-estimation resource estimate | 3 / 6 |
| 5 | **A82 pre-registered re-test** (OP-03) | Only if rank 3 shows a search gap. Run the existing pre-registration with the equal-tuning SA and random-prior twins. | Pre-registered: condition C fails near the decoder's answer, or random ≤ VQE | This is itself a quantum-usefulness test (simulated) | 1 |

**Explicitly not ranked:** everything in §7, and every DNR entry.

## 9. Honest expected outcome (I(prog))

- **Most likely:** ranks 2–4 kill themselves classically. Samplers mix adequately, search saturates, and decisions are bias-limited. The program then concludes with a strong, scoped negative: *at protein lengths up to N and with learned pair energies, no quantum primitive with a known separation addresses a measured bottleneck*. That is a publishable category-6 / negative result, and it keeps the predecessor's lesson intact.
- **Less likely but valuable:** classical mixing time grows steeply with length on the learned-energy posterior, *and* better sampling transmits to the chain. That would make AA-1 the program's first genuinely load-bearing candidate. Even then, the claim available before hardware is a **resource-estimate (category 3) / theoretical (category 6)** claim, not an empirical advantage.
- **Not expected:** any near-term empirical (category 2) or hardware (category 5) advantage. Nothing in the evidence supports planning for one.

---

## Version 2 update: literature phase (2026-09-26)

_Source: `research/literature/` (six verified literature searches; the matrix is in `literature/OPPORTUNITY_MATRIX.md`). Version 1 above is kept unchanged as history. Where v2 and v1 differ, v2 governs._

### Status changes from the literature

| v1 item | v2 status | Reason (see literature files) |
|---|---|---|
| C-1 / SP-1 / AA-1 posterior sampling at length | **INTERESTING (conditional)**, unchanged in direction but sharpened | The only line that survives the classical-first filter. At most quadratic, query-model and fault-tolerant [A8, A31, A44, A45]. Needs a measured classical cost above an explicit fault-tolerant break-even (CA-1: [A56, B46]). |
| *(new)* continuous quantum Langevin / replica-exchange / QSVT samplers | **INTERESTING, top theory line** | Best formal match to SP-1 [A44]. First provable continuous separation, Ω(α) vs Õ(√α), on hide-and-seek wells [A45]. |
| QA-1 amplitude estimation (C-3) | **KILLED (practical)** | Biomolecular estimates are bias- and mixing-limited [B71]. Break-even needs σ/ε ≳ 10⁴; protein decisions need 10–10² [B §5]. The S33 soft-readout signal was an exact sum, with no variance [B §7]. |
| QA-2 Grover over candidate/fragment spaces | **KILLED** | Structure plus fault-tolerant overhead [C63–C65]; oracle is a reversible decoder |
| QA-3 quantum-walk hitting / search | **WEAK** | WE, TPS and MSMs already remove the waiting-time exponential [E60–E67]; kinetics are outside the endpoint |
| QA-4 backtracking / B&B (C-4) | **WEAK** | Relative to the same tree; exact classical solvers prune it [C82, C83, C85]; CSP advantage "disappears" [C63] |
| AA-2 amplitude-amplified restarts (C-2) | **KILLED** | Restart saturation gives at most ~8× fewer calls; quadratic fails the fault-tolerant test [C64, C65] |
| AA-3 electronic structure | **WEAK / out of scope** | No generic exponential advantage [F64]; FeMoco model solved classically [F65]; energy accuracy is not the structure bottleneck (DE-7) |
| AA-4 QSVT readouts | **KILLED** (confirmed) | Dequantisation [F52–F55]; QRAM [F56] |
| SP-2 / SP-3 / SP-4 | Folded into M1/M2 | — |
| DE-1 … DE-9 | **Confirmed** by the literature | The quantum-folding literature shows the same failure modes [D §4, §10] |

### New required element: break-even

Every sampling claim must be compared with **B(L)**, the fault-tolerant break-even number of classical steps per independent sample for a coherent learned-energy walk operator.
- No published estimate exists (literature gap G-2).
- A rough I(agent) estimate is ~10⁶–10⁸ Toffolis per step at L = 100, which makes quantum relevant only if the best classical sampler needs ≳10¹²–10¹⁵ steps per sample [A §3.9].

### v2 ranking (supersedes v1 §8)

| Rank | Item | Type | Status |
|---|---|---|---|
| 1 | **G1**: classical mixing-cost scaling of the learned-energy posterior vs length, with sampled soft-readout transmission (H-006) | Classical measurement | **HIGH PRIORITY: the next experimental gate** |
| 1 (parallel) | **G2**: fault-tolerant resource estimate of a learned-energy walk operator → B(L) (H-008) | Theory / compilation | **HIGH PRIORITY** |
| 2 | **G3**: landscape census for persistence / hide-and-seek structure (H-007) | Classical, from G1 runs | PROMISING |
| 2 | **G4**: generalised H-001 reduction theorem (H-009) | Theory | PROMISING |
| 3 | M1 / M2 quantum sampling | Quantum (only after G1–G3) | INTERESTING (conditional) |
| — | Everything else | — | WEAK or KILLED (`literature/OPPORTUNITY_MATRIX.md`) |

**Expected outcome (I(prog), unchanged in spirit from v1).** Most likely G1 or G2 kills M1/M2, giving a scoped, publishable negative (category 6/3). A positive would support a category-3 resource claim only, not an empirical or hardware advantage.
