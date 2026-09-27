# Complexity landscape for quantum approaches to protein-structure computation

_Discovery sprint, 2026-09-27. This file places every task examined in this program in its known complexity-theoretic context, separating worst-case statements from instance-family statements and query complexity from runtime. Literature keys refer to `research/literature/BIBLIOGRAPHY.md`. Tags: THEORETICAL (literature), DERIVED (this repository), INFERENCE._

## 1. Tasks with a classical objective (energy E over structures)

| Task | Best known quantum vs classical | Model | What it means here |
|---|---|---|---|
| Find argmin E (OPT) over N states, black box | Θ(√N) vs Θ(N): Grover / Dürr–Høyer [C55, C56] | query, worst case | quadratic only. T1: H-001b false in the query model for implicit black-box registers (theoretical L2), practically L0 |
| Sample π ∝ e^{−E/T} via a reversible chain with gap δ | Õ(δ^{-1/2}) vs O(δ^{-1}): Szegedy / QSA / qubitised walks [A7, A8, A31, A55, A56] | walk steps; needs a warm start (overlap) and a certified lower bound on δ | quadratic **relative to the same chain** (L2). Nothing relative to the best classical sampler (L0; T2) |
| Continuous-space sampling (Langevin) | Õ(√(β d C_PI)) quantum Langevin; √(β d/Gap) quantum replica exchange [A44]; first provable separation Ω(α) vs Õ(√α) on hide-and-seek instances [A45] | gradient-oracle queries | quadratic; α-bounds vacuous for extensive learned energies (βΔ ≥ 3×10³–5×10⁴ nats; T2, T5 §4.1) |
| Estimate a posterior expectation to ±ε | Θ(1/ε) vs Θ(1/ε²) (amplitude estimation) [B13, B16, B29] | state-preparation / reflection / sequence oracles | quadratic in precision (T5 Theorem B) |
| Information-local hidden-well families | ≤ quadratic when the background is classically easy | pointwise oracle (M8) | T5 Lemma 1 / Theorem A (DERIVED) |
| Structured white-box objectives | super-polynomial query separations exist for specific constructions: GHV (glued trees, Simon-type), LWWZ/QHD-type continuous landscapes, planted Kikuchi problems (up to nearly quartic vs best known classical) [C69–C73, X2–X10, X23] | query / structured | No protein-realistic energy is known to have this structure. The QM-09 transfer attempt was killed (discovery workflow). Pair-distance energies leak the basin location globally (T5 §3.7) |
| Coupled classical oscillators (2ⁿ modes, oracle couplings) | exponential query separation; BQP-complete [X23] | oracle-specified couplings | A protein elastic network has poly(N) explicit couplings, so classical diagonalisation is polynomial; no advantage (QM-26) |

**Summary (DERIVED + THEORETICAL).** For every classical-objective task relevant to structure prediction or sampling, the known quantum speedups are at most polynomial (quadratic, or precision-quadratic) on protein-realistic instances. Super-polynomial separations exist only for constructed structures that protein energies are not known to have. Quadratic speedups do not survive fault-tolerant break-even at protein sizes (`BREAK_EVEN.md` §1–3).

## 2. Tasks with a quantum forward model (physical quantum dynamics)

| Task | Complexity status | Relevance |
|---|---|---|
| Simulate e^{−iHt} for a local spin Hamiltonian, measure a local observable | BQP-complete in the worst case (Feynman/Lloyd; local Hamiltonian simulation) | Real-time dipolar dynamics of protein ¹H networks is an instance. Worst-case hardness does not transfer to this instance family automatically |
| Infinite-temperature correlators Tr[A(t)B]/2^N | DQC1-type (one clean qubit). Estimating to additive error is DQC1-hard in the worst case (Knill–Laflamme; cited from the workflow audit) | exactly the NMR transfer observable S_ab(t) |
| OTOCs | OTOC(2) on 2D random circuits: beyond-classical evidence [F30]; tensor-network/BP infeasibility argued [F31] (Google-affiliated). First-order OTOC "sometimes well-approximated" classically (Google's own statement, via the discovery workflow) | the NMR echo observable F_ab(t) here is first order |
| Noisy dynamics | Average-case noisy circuits admit poly-time classical simulation via Pauli-path truncation (Schuster et al., PRX 15, 041018 (2025) [F35]) | physical dephasing (γ) and hardware noise both push toward classical simulability |
| Liquid-state NMR spectra | cluster approximations linear in spin number reproduce typical experiments (Fratus et al., arXiv:2508.06448) | classical rebuttal; strongly coupled static solids are not covered |

**Instance-family question (empirical, this sprint).** For protein ¹H dipolar networks at physically relevant times, does the classical cost of the best approximation to the structure-informative signal grow exponentially in the number of spins the dynamics involves? This is measured by C2/C3 (`experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`) as the peak Pauli-string count M*(N) of sparse Pauli dynamics at fixed accuracy. **An empirical scaling on N ≤ 20 is not a complexity-theoretic separation.** At best it is category-5 evidence (empirical scaling) for this instance family.

## 3. Where the reductions of this program sit

- **T1 (reduction theorem).** Output equivalence of dephasing-dominated quantum stages is **proved** (H-001a). Cost equivalence is proved for explicit tabulated E; it is false in the query model for implicit black-box E (Dürr–Høyer) and open for structured E.
- **T2 (sampling).** Same-chain quadratic (L2); first-order crossings insensitive to Λ; δ ≤ (8/p)e^{−ΔF‡}; halving the exponent needs an Arrhenius assumption; optimal in the needle model.
- **T4 (amplified mode finding).** Quadratic vs i.i.d. restarts only; no separation vs adaptive search.
- **T5 (ceiling).** ≤ quadratic on information-local families; no universal ceiling; escape routes enumerated.
- **T3 (resources).** G(L) ≈ 3×10⁴·L² Toffolis per faithful walk step; this sets every break-even above.

## 4. What would change the picture (open)

1. A protein-relevant classical objective with a proven super-quadratic query separation (glued-trees-like or planted structure) whose oracle is cheap. None is known (QM-09, QM-17 attacks).
2. A proof, or strong evidence, that the structure-informative component of protein spin dynamics (e.g. first-order OTOCs of dipolar networks) is classically hard on average over the instance family, **and** remains identifiable under physical dephasing. C2/C3 test the empirical side only.
3. Fault-tolerant logical gate times ≤ 10–100 ns with ≤ 10⁷ physical qubits. This would move the §1 break-evens by 3–6 orders but would not change their quadratic nature.
