# Scientific Memory

Durable lessons. Each entry has a date, a source, and a verification status. Entries are superseded by later dated entries and never deleted.

## 2026-09-26: Predecessor Sprint 33 findings (source: user summary; status: UNVERIFIED in this repo, pending reconstruction into `research/sprint33/`)

1. The strongest structural improvements came from better structural information and decoding.
2. CVaR-VQE did not produce a load-bearing improvement in the final built-chain result.
3. Tuned classical search matched or beat the quantum search in the tested regimes.
4. Several apparent quantum wins disappeared under stronger classical controls.
5. CVaR tail collapse and solver equivalence were important failure mechanisms.
6. The strongest architecture did not require the quantum stage.

**Implication:** No direction here, VQE included, gets a presumption of promise. Any quantum component must pass the quantum necessity test against a strong classical twin.

## 2026-09-26: Status update on the entry above (source: `research/sprint33/README.md` §5, §L3)

The six-point summary above was checked against the imported S33 sources. **None of the six points is contradicted.** Two carry qualifications that the source states:

- **Point 3.** Tuned classical search *beat* CVaR-VQE on register energy only (E1001: tuned SA 3.394 < VQE 3.457). On the built chain it *matched* it. The only equal-tuning chain test, E1000, gave −0.824 at 0.84x, which is NOT MEASURED, and seed 1 gave −0.066. Untrained random-prior sampling beat the trained VQE on the chain (+1.035, 1.35x, 2 seeds).
- **Point 5.** The source names four failure mechanisms, not two: solver-equivalence, tail collapse, register energies not transmitting to the chain (within-target ρ −0.08), and continuous search already being saturated by 32–64 restarts. Tail concentration is not quantum-specific, because SA tails concentrate too (E306).

The entry above keeps its wording. Its status is now: **consistent with source, with qualifications**.

## 2026-09-26: Cross-sprint evidence, predecessor S29–S33 (source: `research/sprint29/` … `research/sprint33/`; imported read-only from `cvar-vqe-protein-folding-v3@3d5b2d25`)

Measured results and the sprint's own interpretations are kept separate in the per-sprint files. This entry lists only what recurs across sprints, with pointers. The S29 contract records that this work originally ran in the `Protein-Folding-Algorithm` repository, branch `s26`.

**Measured, and consistent across S29–S33**
1. **The primary endpoint never moved.** Mean built-chain Cα RMSD on `tuning126` (126 targets, 9–16 aa) stayed at 3.2105 Å (DEP) from S29 through S33. No deployable arm cleared its MDE in the helpful direction (sprint29–33 README H1). S33 did find large gains at length: long40 (44–60 aa) went from avg75 9.745 to 4.739 (E308) and 4.343 (A80, a statistical tie). mid30 (25–40 aa) went from 8.180 to 3.717 or 3.815. These are quantum-free decoders on a learned pair prior, esmprior_v1 (sprint33 README H2–H4).
2. **The deployed CVaR-VQE stage was never load-bearing.**
   - S29: it is indistinguishable from a fixed, target-independent profile with no circuit (−0.0082 Å, 0.27x) (sprint29 H4).
   - S31: the deployed objective is convex with a closed-form "hinged Gibbs" minimiser, and the circuit is worse than p* on 126/126 (sprint31).
   - S32: production runs `quantum=False`, and no circuit was run (sprint32 H7).
   - S33: 34 chain-level VQE-vs-classical-twin contrasts, none in VQE's favour (sprint33 H5).
3. **Structural reasons given in the sources.**
   - For a diagonal Hamiltonian, the CVaR tail is a prefix of the energy order. This is the "set-equality theorem", identified as Barkoutsos et al. 2020 eq. (12) in S29, and S30's T1. One classical sort therefore reproduces the stage.
   - The solver-equivalence lemma (S33): any argmin-only readout gives the same chain whichever solver finds the argmin.
   - Every decision space at 9–16 aa is enumerable (2^n_res ≤ 65536) (S32).
   - S32 states that a quantum role needs "P1 — a decision space that GROWS WITH THE TARGET" and "P2 — a genuinely STOCHASTIC energy", and that "this project has never had either". S29 lit note L_4 says non-classicality needs non-commuting terms and a non-eigenvector prepared state, which "the project has never satisfied".
4. **Apparent quantum wins disappeared under stronger controls**: tuned SA, random sampling from the same prior, seed replication, and full-n re-runs (sprint33 README §5 point 4; `sprint33/QUANTUM_RESULTS.md`).
5. **ORACLE headroom exists, but deployable routes to it are closed.** Examples: the S29 ORACLE ceiling of the deployed architecture is 2.9027 Å, and five ORACLE signs per target are worth −0.3259 Å in S30. In the sources' own terms, the per-target sign or information is missing from all native-free channels (S29 L_8, S30 H3, S32 H6).

**Interpretations the predecessor reached** (attributed to the sources, not adopted here)
- "The bottleneck is information in esmprior_v1's long-range pair distributions … It is not search and not decoding." (S33 REPORT §1.7)
- "A structure estimate good enough to make the readout worth solving is already good enough to emit." (S32 THEORY_Q Q1-T2)
- "every VQE-vs-SA claim needs equal tuning effort, not just equal evaluation budget." (S33 SCIENTIFIC_MEMORY)

**Implications for this program** (a program-level judgement, not a finding from the sources)
- The predecessor's quantum stage was a diagonal-Hamiltonian argmin/tail sampler over small, enumerable registers. Any new architecture that reduces to that shape inherits these negative results. A candidate must be checked against three conditions before any experiment:
  - the decision space grows with target size, beyond enumeration;
  - the objective or readout depends on more than argmin or an energy-order prefix;
  - there is a non-diagonal (non-commuting) structure, or a sampling or estimation task, where a quantum primitive has a known complexity-theoretic role.
- The instruments, statistical contract (MDE = 2.8016·SE, fold CI, "< 0.7x is NOT A RESULT"), DEP/ORACLE discipline and adversary protocol are reusable as validated method. Source discrepancies are logged in each sprint's `LESSONS.md` importer notes.

## 2026-09-26: Reconstructed scientific state and Quantum Opportunity Map (source: `research/sprint29-33/`, `research/QUANTUM_OPPORTUNITY_MAP.md`)

The synthesis layer is now in place. Each statement is tagged M (measured), I(src) (the predecessor's interpretation), I(prog) (this program's reasoning) or U (untested). Durable points:

1. **M.** 33 quantum experiments are recorded (QX-01 … QX-33), covering registers of 7–171 qubits, all simulated. None was load-bearing on the built chain. The decisive twins were **equal-tuning SA** and **random prior sampling** from the same warm start; greedy and untuned SA were not decisive. Every experiment tested only charter category 1, plus category 3 in simulation. Categories 2, 4, 5 and 6 were never tested.
2. **M.** Twelve reduction results (R1–R12 in `sprint29-33/README.md` §3) explain the nulls: prefix theorem, solver-equivalence, tail collapse, closed-form p*, hull projection, a ≡ μ, dimension counting, P1 ∧ P2, distribution-equivalence, register bounds, monotonicity, and (C1)+(C2) non-classicality.
3. **I(prog).** All of them share one structure. A quantum output consumed only via argmin, an energy-order prefix or a convex functional of a diagonal-energy distribution is classically reproducible. This is H-001's core.
4. **I(prog).** The inherited evidence is silent on four things:
   - classical sampling hardness (never measured);
   - lengths > 60 aa;
   - algorithms with known separations (amplitude estimation, quantum walks/QMCMC, QSVT, Hamiltonian simulation);
   - fault-tolerant resource estimates and hardware.
   The opportunity map targets exactly these gaps.
5. **M → I(prog).** The only place where a sampler's *distribution* mattered on the chain was diversity: soft Boltzmann beat hard tails on mid30 (1.40×), and averaging beat selection. This makes posterior sampling at length (SP-1 / AA-1) the most defensible quantum-relevant line. It is conditional on classical mixing being slow, which has never been measured.
6. **Rule adopted.** No quantum build without a classical kill test that failed to kill. DO-NOT-REPEAT registry: `sprint29-33/NEGATIVE_RESULTS.md` Part 2 (DNR-01 … DNR-18).

## 2026-09-26 — Literature phase (source: `research/literature/`; 531 verified keys, 448 canonical entries after de-duplication, six parallel domain searches; see `BIBLIOGRAPHY.md`)

Durable conclusions (L = literature claim with key; I(prog) = program reasoning):
1. **L.** Every quantum speedup that could touch protein-structure computation is **at most quadratic** (in spectral gap, barrier amplitude, precision, or search-tree size), **query/step-model**, and **fault-tolerant** [A1, A8, A31, A44, A45, B12, B26–B28, C54–C61]. The only super-quadratic families need planted/algebraic structure no protein subproblem is known to have [C69–C73].
2. **L.** Quadratic speedups do not pay on early fault-tolerant hardware: QSA ≈ "a day and a million physical qubits" vs "four CPU-minutes" of SA; ~1-year crossover at SK N=512 [A56]; "focus beyond quadratic" [A57/B46]. Any program claim must state a break-even B(L).
3. **L.** The quantum protein-folding literature (2008–2026) contains **no** load-bearing quantum result against a strong classical baseline on a realistic representation; hardware maxima are ≈16 aa; no paper benchmarks PERM/REMC/Wang–Landau/CPSP; QAOA is "matched by random sampling" [D14]; lattice cost optima are worse than random folds for short peptides [D28]; QFold's advantage rests on an enumerated energy table and extrapolation [D9]. This independently mirrors S29–S33.
4. **L.** Biomolecular estimation is limited by force-field bias and mixing, not Monte Carlo variance [B71]; amplitude estimation targets the wrong factor.
5. **L.** Natural protein landscapes are argued funnelled [E2–E6]; PT makes energetic barriers polynomial [E33]; classical sampling is provably slow only in golf-course, persistence, or first-order regimes [E33, E39, E40]. **Learned energies have never been characterised.**
6. **L.** Generic advantage claims (RCS, IBM utility, GBS) were mostly matched classically; D-Wave 2025 disputed; 67-q RCS and OTOC(2) stand but have no protein mapping [F §1]. Trainable ⇒ often classically simulable [F37, F91]; noisy+mitigated ⇒ classically simulable [F35]; dequantization [F52–F55]. These generalise H-001 (→ H-009).
7. **I(prog).** Only one line survives the classical-first filter: sampling a **specified learned-energy posterior** at ≥60 aa (walk/QSA/continuous quantum samplers; M1/M2, INTERESTING-conditional). The S33 soft-readout signal was an exact enumerated sum — evidence of *value*, not of *hardness*.
8. **I(prog).** The decisive missing measurement is **classical**: mixing-cost growth vs length of the best classical sampling portfolio on such a posterior, plus sampled-readout transmission (G1 / H-006), alongside the first FT resource estimate of the matching walk operator (G2 / H-008). This is the next experimental gate. A scoped negative is the most likely outcome.


## 2026-09-27: Discovery sprint, durable lessons (source: `research/theory/`, `research/discovery/`, `research/experiments/ADVERSARIAL/`, PREREG deviation log)

1. **DERIVED. Landscape-independent floor.** For any route that quadratically accelerates a classical sampler, the per-sample quantum wall-clock at break-even is T*_Q = Aρ(K n_b G t_T)²/c. No amount of classical hardness makes such a route practical below that floor. For the A80 learned energy, G(L) ≈ 3×10⁴·L² Toffolis gives T*_Q ≥ 0.26 yr/sample at 1 µs Toffolis. Always compute this floor before measuring classical hardness.
2. **MEASURED. Stopping an adversary ladder early manufactures "hardness".**
   - The NMR echo window at N = 10 (f_hard ≈ 0.95) vanished when sparse Pauli dynamics went from ε = 1e-4 to 3e-5 (median 0.00).
   - An adversary ladder must be run to saturation, and exact classical cost must be reported alongside it.
   - The pre-registered weight-4 adversary alone would have produced a false positive (f_hard 0.99).
3. **DERIVED + MEASURED. Pauli-string counts are not a hardness metric at small N.** They saturate the parity-allowed operator space (M* ≈ 4^N/4). Exact sector or statevector simulation is cheaper at every N where they were measured.
4. **MEASURED. Transfer is compressible; echoes are not.**
   - Two-point transfer reads one Pauli coefficient and is truncation-robust (operator hydrodynamics).
   - First-order echoes read the whole anticommuting operator weight. No sub-exponential representation was found (≥ 9 families, N ≤ 16).
   - Incompressibility is a precondition for quantum advantage, not evidence of it. The other preconditions are exact reach, physical reversibility and informational value.
5. **LITERATURE-SUPPORTED + INFERENCE. Irreversibility and classical hardness come from the same scrambling.** Both scale with T2. Rescaling couplings (dilution, deuteration, Floquet) moves the informative window and the reversal horizon together.
6. **MEASURED. The A80 energy is piecewise smooth** (0.05 Å table interpolation). L-BFGS endpoints are not stationary points, so Laplace/Hessian basin masses are invalid for it.
7. **MEASURED. Gain statistics.**
   - "Information after the classical failure time" overstates the classical deficit by 3–5000× relative to an estimator-level fit of the biased model to all data.
   - Use estimator-level bias, joint data and realistic priors.
8. **Operational.**
   - Workflow agents' own computations bypass the governor. Cap agent compute explicitly in prompts.
   - The Claude Code host reaps background shells under low system memory. Run ≤ 4–5 workers with RAM launch ≤ 82%, and keep resume state on disk.


## 2026-09-28: Round 3 lessons (source: `experiments/ROUND3/SYNTHESIS.md`, `CRITIC.md`)

1. **MEASURED. The mandatory classical twin for any learned-energy route is the native-free distance-geometry portfolio**, not random multistart. Weighted SMACOF on distogram expected distances, plus ~400 energy+gradient evaluations, reaches or beats the 256-restart census best basin on 14/16 crops at L = 150; 5/8 are lower under symmetric polishing. It was replicated by two lanes. Random-restart p_hit decay reflected a weak baseline plus fixed-depth relaxation, not hardness. (Correction: the earlier "61/64 deepest basin" wording was a mis-transcription.)
2. **DERIVED. Generalised floor for speedup exponent s.** T*_Q,s = K n_b G t_T · X^{1/(s−1)} with X = AρK n_b G t_T / c. Against the DG portfolio, every s, including exponential, needs t_T ≤ ~3 ns at L = 100–500.
3. **DERIVED + MEASURED. Exact echo decomposition.** F_ab = H + floor + X. H = Σ_j G_aj² is two-point and classically computable (classical spin dynamics on 80–160 spins). The floor, ≈ (1 − H)/N, is a finite-cluster artefact of size ≥ 3σ at N = 18. X is the four-point remainder.
4. **DERIVED. Step convergence is not convergence.** Under a 1/N drift, |F_{N+2} − F_N| < σ can hold while the true error is 10–20σ. Use an explicit F̂_∞ estimator and a cross-family check.
5. **INFERENCE (thesis, with falsifiers).** In the regimes examined:
   - learned-energy structure prediction is classically easy;
   - dense-spin quantum dynamics that may be classically hard add no usable structural information (forward-model error, reversal horizons);
   - physics-based all-atom sampling is classically hard and structure-bearing, but lacks any known super-quadratic quantum algorithm.
6. **Process.** A negative program must red-team its own kills; a false kill is the costly error. Verify only SUPPORTS lanes and you miss that.


## 2026-09-28: Round 4 lessons (source: `experiments/ROUND4/SYNTHESIS.md` §6, `CRITIC.md`)

1. **A flat ladder in one cluster family is not convergence.** Check that the observed site's own dominant couplings are inside the cluster (M2_b coverage). A single missing partner moved the echo by 7σ.
2. **Do not build estimators or convergence tests on a bookkeeping component.** X ≡ F − H − floor rises as the floor falls even when F has converged. Test the observable itself, across families.
3. **Raw forward-model misfit is not a kill arm.** Profile the nuisance families (offsets, reversal scaling, order parameters) and report the residual bias. Also check that the Fisher model is converged in N before quoting gains.
4. **Name the kill type.**
   - Learned-energy structure prediction is a classical-ease negative.
   - Protein ¹H echoes: easy where observable, uninformative beyond the reversal horizon.
   - Physics-based all-atom sampling is a no-applicable-algorithm negative, and the only examined regime a new algorithm could open.
5. **Cost every pre-registered test against the compute cap** before registering it.
6. **Argue classical-ease results from classical cost**, not from a quantum cost ratio at an assumed gate time.


## 2026-09-28: Lesson from the top-3 topic search (source: `reports/lit_work/selection.md`, `round2_prefilter.md`)

1. **The wall and the information are usually in different places.** This held for all audited candidates: WDM, spin ice, TMD e-h plasma, strong-field ionization, supernova response, kilonova opacity and FCI graphene. Either the regime where exact classical methods fail is not what the data or decisions need, or cheap approximate classical families already match the measured observable. Test this first.
2. **Cost is dominated by sampling and state preparation, not by Hamiltonian simulation.** Real-frequency response and Gibbs-state targets reached S*G ~ 1e13-1e19 Toffoli per useful state point. Screen for S*G <~ 1e13 before any other analysis.
3. **Short circuits from lifetime broadening come with a cost:** the same broadening usually washes out the correlation signature (multinuclear L-edge RIXS).
4. **Static chemistry trilemma.** Active-space QPE is cheap but hits the model floor. Full-basis QPE is too expensive and has poor overlap. The advantage over DMRG is polynomial.
