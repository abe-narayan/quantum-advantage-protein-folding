# Killed directions (discovery sprint, 2026-09-27)

_28 of 28 candidate mechanisms are killed as quantum-advantage claims for protein-structure computation (25 attacked from three lenses, 3 dead on arrival). Each entry gives the kill type and a reopen condition. Kills of the sampling family rest on derivations (landscape-independent runtime floor T*_Q; per-pair cost ratio) and do not depend on pilot hardness data. Hardness-side statements marked exploratory must be replicated under the governor before `research/KILLBOOK.md` cites them as measurements. Full evidence: `CANDIDATE_MECHANISMS.md`, `CLASSICAL_COUNTERARGUMENTS.md`, `attack_records.json`, and the theory notes in `research/theory/`._

**Kill-type census (primary):**
- theorem/derivation: QM-06 (rescoped), 08, 11, 13, 16, 17, 18, 25, 26;
- measurement: QM-02, 07, 10, 11, 16, 21, 24, 25, 26;
- resource/break-even: QM-01, 03, 04, 05, 12, 15, 20, 23;
- information: QM-15, 17, 18, 19, 22, 24.

## Per-direction record

- **QM-01** Walk/QSA/QRELD learned-posterior sampler: KILLED (resource, landscape-independent). T*_Q ≥ 0.26 yr/sample at 1 µs Toffolis even with exponential classical mixing. Reopen only if Toffolis ≤ ~50 ns AND R2 finds a precondition-resistant, readout-visible barrier ≥ 23 nats with ≥ 1 MDE transmission.
- **QM-02** Hide-and-seek wells / Olivucci separation on learned energies: KILLED (measurement + derivation). White-box pair tables make wells visible to distance-geometry seeding (p_att ~ 1), and prior sublevel mass ≤ e^−KL (KL = 113–960 nats). Reopen only if a planted distributed well is missed by all classical arms with p < 10⁻⁶ AND real tables contain such structure.
- **QM-03** Readout/lift/transport gates as a quantum candidate: KILLED (no speedup of its own). Basin decomposition is Φ-free. Kept as a classical instrument inside T2.
- **QM-04** Quantised tempering across cooperative transitions: KILLED (resource + classical bypass). T*_Q does not depend on ΔF, order-parameter biasing is polynomial, and physical barriers are below 2 ln R.
- **QM-05** Coherent learned-energy walk/gradient step as an advantage route: KILLED (costing). K* ≥ 6×10¹¹ steps/sample at 10⁶ Toffoli/s, independent of L. Kept as the gate certificate for every quadratic card.
- **QM-06** Consumption-factoring + quantum gradient estimation: KILLED as a route. Measured c = 1.5–5.5 bounds the Jordan/GAW gain. The no-go is upheld only in its rescoped form (algorithm class, information-local; exceptions T5 C1 and LWWZ).
- **QM-07** Tensor-network/Schmidt-rank dequantisation audit: KILLED (non-diagnostic). log χ ≥ I, so χ is large even inside one easy basin, and grid discretisation mis-states E by 500–17,000 kT.
- **QM-08** Posterior as a ground state / non-stoquastic parents: KILLED (theorem, BCGL 2023 fixed-node). Stoquastisation never lowers the gap, and the residue is the QM-01 quadratic.
- **QM-09** GHV/LWWZ and glued-tree transfer to protein energies and graphs: KILLED (information-locus inversion + measurement). Separations need hidden labels, and conformational graphs have no column subspace. The theory question of explicit white-box stoquastic paths is parked in G.
- **QM-10** QHD / coherent tunnelling: KILLED (dequantisation + resource). Gaussian homotopy solves the only separation family in d-independent queries, and one run costs 10¹⁰–6×10¹¹ Toffolis against converged p_hit 0.2–0.3.
- **QM-11** Prior-to-posterior amplitude amplification / quantum rejection sampling: KILLED (measured divergence). D_½ ≈ 108 nats at L=60, cost ≥ e^{KL/2}, and a window needs C_SMC > R²; this is the one-stage special case of QM-01.
- **QM-12** Walk hitting/search/QPE for rare events: KILLED (splitting adversary). With Θ(1) interface probabilities, AMS/WE cost polylog(1/p). Break-even needs an interface probability ≤ 10⁻⁷ that no coordinate can split.
- **QM-13** QLSA/QSVT committors and rates: KILLED (theorem + toy). The barrier exponential is conserved in κ or the readout amplitude, stochastic unravelling caps the gain at quadratic, and the output is off the endpoint.
- **QM-14** Precision estimation of posterior functionals: KILLED (DOA; M4, H-005). Bias- and mixing-limited; break-even needs σ/ε ≥ 10⁴.
- **QM-15** Fold-switching sampler/hitting/swap-test variants: KILLED (stratification + information). Restraint-path MBAR never pays the barrier, and swap-test fidelity is a partition-function ratio. The classical factor-table information test moves to E.
- **QM-16** Quantum backtracking over topology/DMDGP/K* trees: KILLED (derivation + measurement). Subset DP beats √(Tn) for m ≥ 12, DMDGP trees are O(n), and backtracking cannot list solutions.
- **QM-17** Kikuchi/tensor-PCA planted inference on protein data: KILLED (arity/Fourier degree). Pairwise restraints collapse the hierarchy, and the cryo-EM gap sits at non-physical K. The k≥3 residue is parked in G.
- **QM-18** Quantum walks on restraint-defined joint posteriors: KILLED (collapse theorem). Assignments sum out exactly, reducing this to QM-01. The classical restraint science moves to E.
- **QM-19** Fast-MAS ¹H spin-diffusion/RFDR quantum forward model: KILLED (weak-coupling reduction + identifiability). κ ≤ 0.05 at 5–8 Å, and direct long-range FI gives σ(r) ≥ 0.8 Å under any forward model.
- **QM-20** Quantum-estimated NMR likelihood consumed in MCMC: KILLED (the card's own cost criterion). ≥ 5×10¹² T per step against 10¹² T per effective sample, and ¹⁹F/REDOR/PRE bypass. The forward-model residue continues as R1.
- **QM-21** Hardness–identifiability theorem programme: KILLED as a theorem route (C3-a vacuous, C3-b contradicted for echoes). The empirical OTOC question continues as R1 under C2/C3.
- **QM-22** Liquid NMR, ZULF, DEER, radical-pair, optical and diffraction forward models: KILLED (fold information sits in weak couplings, which are classically perturbative; hard sectors are fold-uninformative).
- **QM-23** Metal-cofactor QPE and NQE for protein structure: KILLED for the structure endpoint (classical chemical accuracy at FeMoco; NQE path integral sign-free; effects below 0.1 Å). Branch (a) is parked as external chemistry in H.
- **QM-24** Quantum-memory NV learning and multi-pass TEM as computational advantage: KILLED (commuting sensor states give ratio 1.000; designed TEM G ≈ 1.3). The TEM branch is parked as sensing in D.
- **QM-25** Quantum knot invariants and quantum TDA of proteins: KILLED (instance size vs crossover; nerve-lemma truncation; vanishing normalised Betti numbers). The Mayer information gate is in G.
- **QM-26** Babbush oscillator simulation, QENM and KvN MD for protein mechanics: KILLED (Ω(N) data loading; 3-D locality caps the gain at quartic; classical linear-scaling propagation measured).
- **QM-27** Quantum solvers in cryo-EM/IDP inversion pipelines: KILLED (DOA; M9, M4, M15, K-011; data loading and information-limited).
- **QM-28** Multistate negative design as a quantum-solved game: KILLED (DOA; K-002, M9; structured payoffs make best responses argmin/Gibbs steps).

---

## Kills added by this sprint's own experiments (production, pre-registered)

_Filled in from the C1/C2/C3/R1-E/PoP and G1/R2-T results; see `reports/QUANTUM_ADVANTAGE_DISCOVERY_REPORT.md` §Negative results._
