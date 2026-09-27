# Advantage conditions: what any quantum route in this program must satisfy

_Discovery sprint, 2026-09-27. A consolidated checklist of **necessary** conditions for a quantum advantage in protein-structure computation, each traced to its derivation. A candidate failing any condition is not an advantage at the corresponding level. Tags: DERIVED (proved in this repository), THEORETICAL [key] (literature), MEASURED (this sprint), INFERENCE._

The conditions come in two families. Family A covers quantum stages inside a classical-objective pipeline (optimisation, sampling, estimation over a classical energy). Family B covers quantum forward models of physical quantum data, such as NMR spin dynamics. The failure table (§3) maps every candidate from `research/discovery/` onto these conditions.

---

## Family A: quantum stage acting on a classical objective

| # | Condition | Why it is necessary | Source |
|---|---|---|---|
| A1 | **Not dephasing-dominated.** The stage's objective must not be a function of its computational-basis distribution alone, or its output must be consumed through something other than argmin / energy-order tail / convex program. | Otherwise the optimal stage output equals what a classical optimiser over the probability simplex reaches, and the pipeline output is a function of the classical specification alone (output equivalence). | T1 Theorems 1–2, DERIVED (`PROOFS/T1_reduction_theorem.md`) |
| A2 | **Hard specification problem.** The classical problem the stage implicitly solves (OPT(E), TOP_m(E), CVX(Ψ), SAMPLE(π)) must be classically hard on the instance family. | For explicit registers every stage is classically simulable in poly(N). | T1 Theorem 3, DERIVED |
| A3 | **More than quadratic, or a large constant.** On information-local (hide-and-seek) families with a classically easy background, the separation is at most quadratic. Precision gains are at most quadratic, Θ(1/ε) vs Θ(1/ε²). | Quadratic gains are eaten by fault-tolerant overheads (A5). | T5 Lemma 1, Theorems A–B, DERIVED + THEORETICAL [A45, B16, B29] |
| A4 | **Escape route identified.** A super-quadratic claim must name its route: (i) leakage readable only by a quantum algorithm; (ii) a quantum forward model; (iii) planted structure between the information and computational thresholds; (iv) quantum data; (v) exploitable white-box structure (DQI, short-path, BQP-complete oscillator dynamics). | No universal ceiling exists for classical energies behind an oracle (Simon-trail counterexample), so the claim must be per family. | T5 §0.3–0.4, DERIVED + THEORETICAL [X2–X10, X23, C69–C73] |
| A5 | **Break-even with full accounting.** τ_* > B* = (A ρ K n_b G(L) t_T / c(L))² per sample (sampling); p_hit < p* = [(π/2) ρ O_rev R_grad]⁻² (amplified multistart). G(L) = Toffolis per coherent walk step, including state preparation and oracle arithmetic. | A query speedup is not a runtime speedup. | T2 S6, T3, T4, DERIVED |
| A6 | **Minimum useful runtime.** The per-sample quantum wall-clock at break-even is T*_Q = A ρ (K n_b G t_T)²/c, whatever the landscape. For a one-day sample, t_T must be ≤ 12–100 ns (most optimistic) or sub-ns (central), 3.5–6 orders below 170 µs. | Landscape-independent obstruction to practical quadratic speedups. | T2 corollary, DERIVED; cf. [A55–A57] |
| A7 | **Relative to the best classical method.** A same-chain speedup (quantum walk vs its own classical chain) is not an advantage if a classical bypass (other path, nested sampling, multicanonical, SMC, mode finding + reweighting) is polynomial. | Where a polynomial bypass exists, a λ-path QSA is exponentially worse. | T2 S5, DERIVED |
| A8 | **Transmission.** Faster sampling or optimisation of E must improve the protein quantity: E must rank structures by accuracy over the relevant modes. | Otherwise the speedup buys nothing structural. | Prereg K-G1d; MEASURED: ρ(E, RMSD) over modes ≈ 0.31 at L=120; the lowest-E mode is not the best-RMSD mode |
| A9 | **Oracle discipline.** No free oracles, state preparation, block encodings or native indicators. Native structures are evaluation-only. | Otherwise the "advantage" is imported from the oracle. | Charter; T3 costs every oracle explicitly |

## Family B: quantum forward model of physical quantum data (NMR spin dynamics)

| # | Condition | Why it is necessary | Source |
|---|---|---|---|
| B1 | **Classical approximations fail where the information is.** The best classical approximation (sparse Pauli dynamics, cluster methods, classical spins, tensor networks) must be biased beyond the data noise at times carrying a substantial share of the structural Fisher information (f_hard large). | Otherwise a classical forward model extracts the same information. | Prereg C1; MEASURED (C1): transfer f_hard = 0 at N = 10 (sparse Pauli exact); OTOC f_hard = 0.85–0.97 at N = 10 (one probe, pending C3) |
| B2 | **The needed classical resource grows exponentially with the spins involved.** M*(N) ~ e^{κN} with M*(N_eff) infeasible at the protein's effective N. | At small N everything is classically exact (sector-exact N = 14 in ~15 min). | Prereg C2/C3 (pending) |
| B3 | **Identifiability in the hard window.** The hard-window information must be non-degenerate: the gain spectrum of F_total vs F_easy must be large in structurally relevant directions. Ergodic dynamics tend to make the learning Hessian degenerate. | O'Brien et al. (2022) found parameters learnable only as the dynamics become non-ergodic. | THEORETICAL [O'Brien et al., PRX Quantum 3, 030345]; analysis `scripts/analyze_nmr2.py` |
| B4 | **Early-time identifiability does not already suffice.** S_ab(t) = d_ab² t²/4 + O(t⁴) identifies d_ab from early data. Classical inversion can buy precision with repetitions, so the quantum gain is g× fewer repetitions unless F_easy is singular. | Otherwise the hard window only sharpens what is already identifiable. | DERIVED (short-time expansion); WF1 resource audit |
| B5 | **Physical realism.** The hard window must lie within the sample's coherence (extra dephasing γ). The observable (e.g. an OTOC requiring time reversal of the dipolar Hamiltonian) must be measurable at the needed SNR. | Otherwise the data do not exist. | Prereg C1 (γ ∈ {0, 1000, 5000} s⁻¹); Zhang et al. arXiv:2510.19550 [F34] measured OTOCs in liquid-crystal samples |
| B6 | **Robust to quantum-hardware noise.** The quantum simulator's own bias (with mitigation) must stay below σ past the classical failure time. | Noisy circuits admit efficient classical simulation (Schuster et al., PRX 15, 041018, 2025 [F35]), and a noisy quantum forward model is just another biased model. | MEASURED (PoP, `scripts/nmr_circuit_pop.py`; pending) |
| B7 | **Resource feasibility.** One fault-tolerant forward evaluation (all times and observables, one geometry) costs ~10¹¹–10¹³ T gates (transfer/OTOC, N = 14–466). That is ~11 h per evaluation even with unlimited parallel factories at 1 µs T-layers, and an inversion with 10³ gradient evaluations takes ~11 years per machine. NISQ circuits need 3×10⁴–3×10⁵ two-qubit gates. | Practical value requires the information gain to justify this. | DERIVED (`nmr_resource_model.py`; BREAK_EVEN §4) |

## §3 Which condition each candidate fails (summary; details in `research/discovery/KILLED_DIRECTIONS.md`)

| Candidate family | First failed condition | Level reached |
|---|---|---|
| Walk/QSA/quantum Langevin sampling of the learned posterior (QM-01, 03, 04, 05) | A5/A6 (break-even ≥ 10¹⁰–10²⁵ evaluations per sample; T*_Q ≥ months–10¹⁴ yr); A8 weak | theoretical L2 same-chain; practical L0 |
| Amplitude-amplified multistart / mode finding (QM-02, QM-11) | A5 (p* ≤ 10⁻¹¹ vs measured p_hit ~ 10⁻²); A7 (no separation from adaptive search) | L2 vs i.i.d. restarts only; practical L0 |
| Precision estimation of posterior functionals (QM-14) | A3 (quadratic) + A5 | L0 practical |
| Ground-state / stoquastic parent Hamiltonians, QHD, rejection sampling, hitting times, QSVT committors (QM-08, 10, 11, 12, 13) | A2/A3/A5 | L0 |
| GHV/LWWZ super-quadratic transfer (QM-09) | A4 (no protein-realistic instance with the required structure) | L0 for protein-realistic energies |
| Quantum forward model for protein NMR (QM-19/20/21) | B7 at the practical level. B1–B3, B6 under test (C1–C3, PoP) | see discovery report |
