# Open Questions

Questions that are not yet sharp enough to be hypotheses. Promote them to `HYPOTHESES.md` when they become testable. The scientific open problems inherited from the predecessor are catalogued in `research/sprint29-33/OPEN_PROBLEMS.md` (OP-ids).

_Updated 2026-09-26 after the S29–S33 reconstruction; updated again 2026-09-26 after the literature phase (`literature/OPEN_LITERATURE_GAPS.md`)._

## Program-level

- **Which bottleneck in protein structure computation is genuinely computational, with a measurable gap, as opposed to information-limited?**
  - Current candidates, none with a measured gap: posterior sampling at length (→ H-003, now H-006/H-007), search beyond 60 aa (→ H-004; quantum payoff killed), variance-limited estimation (→ H-005; retired). See `QUANTUM_OPPORTUNITY_MAP.md` §1 and its v2 update.
- **What is the right long-chain instrument?**
  - Needs targets at 60–150 aa with leakage controls at least as strict as esmprior_v1's R3 rule and cross-fold homologue exclusion (`sprint29-33/OPEN_PROBLEMS.md` §D).
  - Open sub-questions: the source dataset, split design, and whether the predecessor's `prots/` corpus suffices.
- **Which classical samplers define "the strongest classical twin" for continuous CA-trace posteriors?**
  - Candidates: PT, replica exchange, SMC, HMC, and random-prior + relaxation (which beat CVaR-VQE).
  - The choice must be made and tuned *before* any quantum comparison.
- **How should mixing be measured so that it maps onto quantum-walk / QMCMC resource models?**
  - Options: spectral-gap estimates vs integrated autocorrelation vs round-trip times.
  - The literature bridge is needed in `LITERATURE_MAP.md`.
- **Does soft (Boltzmann-weighted) readout from a converged ensemble beat argmin/decoder output at long40 and beyond?** (OP-08; a precondition for H-003's value clause.)

## Inherited, still open (details in OP-ids)

- Is the S33 topology-trap asymmetry (VQE fewer traps than tuned SA, p 0.015) real and reproducible, or a seed/definition effect? (OP-05; low priority, because the random prior sampler dominated both.)
- Is the long-length decoder near its information floor on more than 6 targets and on the chain basis? (OP-02; this feeds H-004.)
- Is there any per-residue non-separable discrete decision at ≥ 40 aa whose ORACLE ceiling is not an order statistic? (OP-06)
- Would A82 survive its own pre-registered kill rules? (OP-03; run only if H-004 opens a search gap.)

## Added by the literature phase (2026-09-26)

- **Do learned (language-model-derived) pair-distance energies have funnel-like or frustrated landscapes?** No literature characterises them (gap G-3). The answer decides whether provable quantum sampling separations — built on hide-and-seek / persistence instances [A45, E39] — are even relevant. → H-007.
- **What is B(L), the fault-tolerant break-even for a coherent learned-energy walk operator?** Unpublished for any molecular energy (G-2). → H-008.
- **Against which classical chain is a quantum walk speedup measured?** Quantum walk gains are relative to the chain quantised; nonreversible/lifted classical chains can capture part of the gain [A14, A15, A18]. The comparison chain must be the best tuned one, not Metropolis. (`THEORY_ROADMAP.md` T2c.)
- **Does soft-readout value survive when the posterior is *sampled* rather than enumerated?** The S33 signal came from an exact sum over 262,144 states (no sampling error). → H-006 transmission clause.
- **Is there any cooperative-folding regime at 100–300 residues where tempering is provably torpid after REST2 / Hamiltonian tempering?** (gap G-11; [E40]).
- **Could exact learned samplers (currently ≤ hexapeptides [E79]) close the window before any quantum device could?** Tracking item.

## Closed by the literature phase

- ~~Is any biomolecular decision variance-limited enough for amplitude estimation?~~ Literature: no — bias/mixing-limited [B71]; break-even σ/ε ≳ 10⁴ (`literature/CLASSICAL_COUNTERARGUMENTS.md` CA-4). Residual check folded into H-006 runs.
- ~~Does any quantum-folding paper show a load-bearing quantum component against a strong baseline?~~ No [D §10].

## Answered by the reconstruction (kept for history)

- ~~Which parts of the Sprint 33 conclusions survive independent reconstruction?~~ All six points of the user's summary are consistent with the source, with two qualifications (`SCIENTIFIC_MEMORY.md`, 2026-09-26). The synthesis is in `research/sprint29-33/`.

## Added by the discovery sprint (2026-09-27)

- **R1-SIM (physics-simulation residue of the killed NMR echo lead).** Does the converged first-order echo (OTOC(1)) of a dense protein ¹H dipolar network require a light cone beyond exact classical reach (N_σ(t) > 30–47 spins) at 80–320 µs?
  - Measured so far: N_σ ≈ 16–20 at 40 µs. No compressible representation was found at any N ≤ 12.
  - Pre-registered test T-A (nested clusters N ≤ 20) is running.
  - Strongest untried adversary: a hybrid exact-core + classical-spin bath (Starkov–Fine).
  - A positive answer would be a category-3 candidate for a physics computation, not a protein-structure advantage.
- **R1-DQ.** Does a phase-reversible double-quantum Hamiltonian (1.8–4× more echo FI in 0–100 µs) keep information inside its own reversal envelope?
  - Low prior: it is 7× more environment-sensitive.
- **Protein Loschmidt-echo T3/T2.** The feasibility kill assumes model-solid values (4–6.7). A measured protein value ≥ 15 would reopen R1 practically; none is known.
- **Is OTOC(1) of geometric dipolar Hamiltonians classically hard on average?**
  - Only worst-case anchors exist (DQC1, universality).
  - Google's beyond-classical echo evidence concerns OTOC(2).
  - Mi et al. 2021 report both an efficient classical model of operator *spreading* and exponential cost of operator *entanglement*.
- **Transmission (R2-T).** Does posterior averaging over modes beat the argmin for the A80 learned energy at L = 60/100? Running.
- **Is the measured classical difficulty of the λ-path (0 NRPT round trips) a barrier or ill-conditioning?** Relevant only as classical science; the quantum route is killed regardless (K-101).

## Added after round 3 (2026-09-28)

Parked residues, none a protein-structure lead:
- **R1-SIM-X.** The four-point echo remainder X = F − H − floor. Only the t ≤ T3 branch (40–120 µs) touches a measurable signal. Tested in round 4 by T-X-early and spinDMFT.
- **R1-SIM-DQ.**
- **R-ROTOR.** Coupled methyl tunnelling. Now an identifiability question.
- **FeMoco E-state isomer identity.** Chemistry level, WEAK; capped by the model floor.
- **T = 1 sub-basin posterior sampling of the learned energy.** Worth 0.1–0.5 Å.
- **DG-residual crops.**
- **QeMCMC small-n exponent.**

Newly scoped, examined in round 4:
- **Physics-based all-atom sampling** of folding kinetics and ensembles. It is classically hard and structure-bearing. Every quadratic route is dead (B*₂ ≥ 2.5e15). An s = 4 algorithm would break even in principle at T*_Q ≈ 0.1–2.5 yr per sample, but no super-quadratic algorithm for classical force fields is known.
