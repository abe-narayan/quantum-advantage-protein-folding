# Killbook

Directions that were killed, with evidence. Each entry has the date, the architecture or hypothesis ID, the kill criterion that fired, the evidence (experiment IDs), what capability did *not* disappear under ablation, and the conditions under which reopening it would be justified.

Reopening a killed direction requires new evidence or a materially different formulation.

## Section A: Inherited kills (predecessor S29–S33, source-verified 2026-09-26)

These kills were made by the predecessor project and verified against its sources during the S29–S33 reconstruction. Evidence records are in `research/sprint29-33/QUANTUM_RESULTS.md` (QX-ids). The full reopening conditions are the DO-NOT-REPEAT registry in `research/sprint29-33/NEGATIVE_RESULTS.md` Part 2 (DNR-ids). Every kill below was established in **simulation** and at **9–60 aa**.

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-001 | CVaR-VQE on the candidate-index register (all variants) | Theorem + measurement | Nothing: a fixed profile m and the closed-form p* reproduce the endpoint | QX-01, 05, 06, 10, 12 | DNR-01 |
| K-002 | Quantum optimisation of diagonal costs consumed via argmin, prefix or convex functional | Theorem (R1, R2, R4) + 34 S33 contrasts | Nothing: SA, greedy, exact or sort give the same chain | QX-17–27, 32 | DNR-02 |
| K-003 | Non-diagonal Hamiltonians on candidate registers | Theorem (dimension counting, stable rank) + gate measurement | Nothing: `eigh` is the classical counterpart; the gate stayed shut | QX-02, 11 | DNR-09 |
| K-004 | CVaR-tail ensembles as readouts | Theorem (tail collapse) + E306 | Nothing: a no-register noise ensemble was better; SA tails were equally concentrated | QX-22 | DNR-04 |
| K-005 | Structural register search at 16–90 qubits (subset, mosaic, fragment, contact) | Measurement + condition C | Nothing: SA/greedy/exact matched; search-vs-no-search gains were delivered equally by SA | QX-18–21, 27 | DNR-03, DNR-08 |
| K-006 | Per-residue (θ,τ)/macro registers at 106–171 qubits as load-bearing search | Measurement (equal-tuning SA, random prior, register-free decoder) | Nothing: random prior sampling beat VQE on the chain (1.35×); the register-free decoder was better | QX-24, 25, 30 | DNR-05, 06, 07 |
| K-007 | Tempered Born machine / Gibbs-readout circuits on small (enumerable) spaces | Measurement (Metropolis twin, exact Gibbs) | Nothing: Metropolis was closer to the exact target on 9/10 | QX-28, 29 | DNR-10 |
| K-008 | Transverse-field configuration-space CVaR-VQE (chimera) | Measurement (BESTOFN, SA) | Nothing: untrained best-of-N tied the VQE | QX-04 | DNR-11 |
| K-009 | Endogenous-order tail lifts (halfspace/quadric) | Measurement with order-statistic nulls | N/A (never built); the apparent gain was 196% null | QX-07 | DNR-13 |
| K-010 | Index/encoding redesign and register widening without a selector | Measurement | N/A | QX-12, 13 | DNR-12 |
| K-011 | Quantum solvers for readout convex programs (p*, QP/hull, SOCP, sparse s-of-K) | Theorem (classical polynomial, milliseconds) | N/A | QX-10, 14–16 | DNR-18 |
| K-012 | Native-free in-band recognition/ranking at 9–16 aa from existing inputs (any computational method) | Theorem + measurement | N/A (information-limited) | `sprint29-33/NEGATIVE_RESULTS.md` §1.2 | DNR-16 (new information source required) |
| K-013 | Global-scalar tuning at 9–16 aa | Measurement | N/A | `sprint29-33/NEGATIVE_RESULTS.md` §1.3 | DNR-15 (never) |

**Scope warning.** These kills close the predecessor's *formulation class* (H-001). They do **not** kill:
- quantum algorithms with known separations (amplitude estimation, quantum walks/QMCMC, QSVT, Hamiltonian simulation);
- problems beyond 60 aa;
- sampling problems where classical mixing is slow.

None of those was ever tested.

## Section B: Kills made by this program

_Entries added 2026-09-27 (discovery sprint). Evidence paths are relative to `research/`. Reopen conditions are the revival templates in the cited files._

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-101 | Quantum sampling of the learned-energy structure posterior (walk / QSA / QRELD / quantum replica-exchange Langevin; QM-01, 03, 04, 05, 12) | Derivation (landscape-independent floor T*_Q = Aρ(K n_b G t_T)²/c ≥ 0.26 yr/sample at 1 µs Toffolis; B* ≥ 10¹⁰–10²⁵) + resource model (T3) | Nothing: classical NRPT/HMC/multistart remain cheaper at every L ≤ 150 under every stated assumption | `theory/PROOFS/T2_*`, `theory/RESOURCE_MODELS.md`, `theory/BREAK_EVEN.md` §1, `discovery/attack_records.json` | logical Toffolis ≤ ~50 ns **and** a measured, precondition-resistant, readout-visible barrier ≥ 23 nats with ≥ 1 MDE transmission |
| K-102 | Amplitude-amplified multistart / quantum rejection sampling / hide-and-seek amplification on learned energies (QM-02, 11) | Derivation (T4; p* ≤ 10⁻¹¹ vs measured p_hit ~10⁻²) + white-box dequantisation (distance geometry; e^{−KL} sublevel bound, KL = 113–960 nats; exploratory) | Nothing | `theory/PROOFS/T4_*`, `discovery/CLASSICAL_COUNTERARGUMENTS.md` QM-02/11 | a planted distributed well missed by all classical arms with p < 10⁻⁶ **and** real tables containing such structure |
| K-103 | All other discovery mechanisms (QM-06…10, 13…18, 22…28): no-go routes, QHD, ground-state parents, TN audits, QLSA committors, fold-switch samplers, backtracking, Kikuchi, restraint posteriors, other spectroscopies, metal-cofactor QPE (structure endpoint), sensing, knots/TDA, oscillator simulation, cryo-EM solvers, negative design | Mixed: theorem / measurement / resource / information (per mechanism) | Nothing load-bearing for protein structure | `discovery/KILLED_DIRECTIONS.md`, `discovery/CANDIDATE_MECHANISMS.md` | per-mechanism reopen conditions in KILLED_DIRECTIONS |
| K-104 | Quantum forward model of protein ¹H **two-point transfer** (spin diffusion / NOE-like build-up) | Measurement: sparse Pauli dynamics (ε = 1e-4) reproduces transfer exactly at N = 10 (f_hard = 0; 1UBQ, 1PGA, dense and amide-only, γ = 0 / 1000 / 5000 s⁻¹). Weak-coupling reduction for 5–8 Å pairs (κ ≤ 0.05) | Nothing | `results/RAW/nmr_gate*`, `discovery/attack_records.json` QM-19 | a transfer observable the best classical forward model fails on at physically relevant times |
| K-105 | Quantum forward model of protein ¹H **dipolar echoes (OTOC(1))** as an advantage for structure (R1; QM-20/21 residue) | Pre-registered C3 survival clause failed (reversal horizon: informative window at 4.8–25 T2 vs T3 ≈ 4–6.7 T2) + value/cost (exact classical simulation beats a fault-tolerant forward model below N_eff ≈ 30–47 at 4–6 h per evaluation; gain under realistic priors median 1.1–1.5) + ε-ladder completion (ε = 3e-5 closes the N = 10 window) | At N ≤ 14: nothing. Exact simulation (seconds) supplies everything. Open physics residue: R1-SIM | `experiments/ADVERSARIAL/R1_SYNTHESIS.md`, `R1_CRITIC.md`, `R1_*` lens folders, PREREG deviation log | all four revival conditions in `R1_SYNTHESIS.md` §5 at once: converged σ-cone > 47 spins at information-bearing times; reversal horizon beyond them in a real protein; a structural degree of freedom classical data leave undetermined with profiled gain ≥ 10; a forward model accurate to σ |

### Round 3 kills (2026-09-28; `experiments/ROUND3/SYNTHESIS.md`, corrections in `experiments/ROUND3/CRITIC.md`)

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-106 | Quantum-enhanced MCMC (Layden quench proposal, Q(s′\|s) = \|⟨s′\|e^{−iHt}\|s⟩\|²) as a sampler of discretised A80 Boltzmann distributions | Measurement: exact spectral gaps, n = 6–10, T = 1/2/4, 149 records, Layden's SK result reproduced. Derivation: the break-even gap ratio | Nothing. A tuned random-subset-flip or local/uniform-mixture chain comes within 1.6–12.7× of the quantum gap; δ_q ≤ 0.85·δ_c^½; warm-start classical mixing takes ≤ 197 steps. On Layden's own SK ensemble a tuned classical chain moves the exponent ratio from 0.28 to 0.39–0.64 | `experiments/ROUND3/qemcmc_exact/` (`summary.json`, `diag_warm.json`, `validate.json`) | Gaps at n ≥ 12 on relaxed tables give k_q/k_c < 0.5 with a bootstrap CI excluding 0.5 against the tuned classical family, **and** a costed discrete oracle puts the break-even ratio below the measured gap ratio (now 784–2.3e5 needed vs ≤ 12.7) |
| K-107 | Any-exponent quantum speedup (s = 2, 3, 4 or exponential) for best-basin finding or sampling of A80 at L = 100–500, including the premise that random-multistart decay p_hit ~ e^{−0.04 L} signals classical hardness | Measurement: native-free DG seeding, 48 crops, replicated by two lanes; portfolio median 420 evaluations. Derivation: generalised floor T*_Q,s | Nothing. The DG-seeded portfolio reaches E_ref; fold-level multistart p(≤ 3 Å) = 0.06–0.34 | `experiments/ROUND3/hardness_what_it_takes/` (`dg_summary.json`, `what_it_takes.json`, `ms_polish_fold.json`); `experiments/ROUND3/structured_speedups/s4_planted_level1.json` | A crop family where the full classical portfolio needs > 1e7 evaluations to reach a basin transmitting ≥ 1 MDE, **and** a super-quadratic algorithm for white-box pair-additive energies, **and** t_T within the derived bound |
| K-108 | Structured super-quadratic families on the A80 task: DQI/HDQI/weighted DQI; short path, jump-to-the-end, generalised short path; super-quadratic key guessing; Kikuchi planted inference; guided local and stoquastic Hamiltonians; glued trees/GHV/LWWZ; QHD/RsAA; constant-temperature Gibbs advantage; Choi MIS | Measured structural-precondition failure: girth = d⊥ = 3 in 64/64 graphs, so l = 0; Fourier-dense torsions; mean dimension 1.8–8.6; energy destroys the equitable partition. Exponent comparison: 12–51× α_c. Literature: 61 arXiv abstracts verified | Nothing. Level-1 distogram seeding does the job | `experiments/ROUND3/structured_speedups/` (`summary.json`, `s3_dqi_graph_code.json`, `s5_graph_krylov.json`, `s6_exponents.json`, `lit/abstracts.txt`) | A protein-derived constraint system with d⊥ ≥ 5 or algebraic structure where DQI's flat-forest l50 beats the classical fraction; **or** a genuine k ≥ 3 planted task where level-1 spectral/SMACOF fails and PT succeeds |
| K-109 | Quantum forward model of the protein ¹H **double-quantum (DQ) echo** as a structure advantage (R1-DQ) | Measurement: the ε = 3e-5 sparse-Pauli twin reproduces the echo to 140–220 µs and ε = 1e-5 to 250 µs; exact simulation takes about 7 s. Value: median joint gain ≤ 1.16 inside every literature envelope (1.00–1.04 with the physical T2), ≤ 1.42 with ideal reversal | Nothing inside the DQ reversal envelope (T3_DQ ≈ 122–134 µs) | `experiments/ROUND3/dq_echo_envelope/` (`analysis.json`, `out/`) | A measured protein T3_DQ/T2 ≥ 50, **and** a converged classical twin that fails inside it, **and** a profiled median gain ≥ 2 |
| K-110 | Gaussian boson sampling programmed with the native-free ESM contact-odds kernel, P(S) ∝ Haf(W_S)², used as contact/pairing proposals (NA-1) | Pre-registered value test: GBS wins 3/64 cells vs ≥ 48 required. Classical emulation: a double-dimer sampler has the GBS marginal exactly (TV 0.018–0.032; R-hat ≤ 1.023 at 60 photons) | Nothing. β = 2 is one point on a smooth, classically sampled Haf^β / perturb-and-MAP tempering curve | `experiments/ROUND3/new_mechanisms_A/t1_gbs_contact/` (`analysis_value_v2.json`, `analysis_emulation.json`), `prereg.json` | A structural endpoint where β = 2 beats every point of the classical Haf^β curve, using a kernel outside the nonnegative class that the double-dimer sampler emulates |
| K-111 | Coupled methyl-rotor tunnelling network as a quantum forward model of core packing (NA-2), structure endpoint | Observability: exact pair splittings ≤ 0.055 µeV at V3 = 100 meV, below INS resolution | N/A: the observable is absent at protein-typical barriers. The physics residue R-ROTOR is parked (§2.3) | `experiments/ROUND3/new_mechanisms_A/t2_methyl_rotor/summary_t2.json` | ≥ 3 coupled methyls with V3 ≤ 50 meV in a real protein, with relaxed H positions, **and** pair-cluster error ≥ 10% at physical contacts, **and** a structure question they answer |
| K-112 | Quantum SDP solvers for restraint-based Gram/EDM structure determination (NA-3) | Resource: ≥ 1e11–4e17 queries (1 day to 1.4e4 yr) vs 0.02–1.3 CPU-s for classical Burer–Monteiro; L^7.2 vs L^2.1. Information: sparse restraints give 7–16 Å [ORACLE] | Nothing | `experiments/ROUND3/new_mechanisms_A/t3_qsdp_edm/qsdp_breakeven.json` | A quantum SDP bound polylogarithmic in both precision and dimension, **and** an information-rich restraint set |
| K-113 | NA-4 to NA-9: hidden-subgroup symmetry detection; quantum fingerprinting; quantum ε-machines; SPADE super-resolution; quantum exponential-time DP; QLSA Poisson–Boltzmann | Derivation, one per mechanism: classical bypass (FFT, multigrid O(N)), sub-quadratic speedup (T^0.79–0.86 with QRAM), or the step is not the bottleneck | Nothing | `experiments/ROUND3/new_mechanisms_A/mechanisms.json`, `README.md` | The per-mechanism conditions in `mechanisms.json` |
| K-114 | Quantum-memory / quantum-data learning of protein spin states: collective or Bell-sampling measurements, sensor-register Pauli channels, and transduction into a simulator (IQHL) | Theorem: SLD = p·dX exactly, so the memory gain is 1 per parameter; the Holevo bound equals the SLD bound (spin-flip symmetry). Measurement: Bell/QFI ≤ 0.032 at t ≥ 80 µs (p = 1), times p² thermally. Physics: transfer fidelity ≤ 1.4e-7 | Nothing. The coherent single-copy optimum and the NMR echo keep the information | `experiments/ROUND3/new_mechanisms_quantum_data/` (`validate.json`, `summary.json`, `physics.json`) | A structure-relevant, exponentially large property family that does not reduce to k parameters and shows a memory separation after nuisance profiling, **and** demonstrated coherent transfer of a molecular spin with fidelity ≥ 0.95 |
| K-115 | Fault-tolerant QPE electronic structure as a **protein-structure** advantage (heme spin state, P450 Cpd I, FeMoco resting spin isomers, P-cluster, OEC, Cu₂O₂/MMO, LBHB/NQE). This supersedes QM-23's "< 0.1 Å" rationale, which is wrong for local endpoints (C11) | Derivation: closed-form cap on solver value from the model floor. Literature: classical FeMoco-76 to about 1 kcal/mol. Census: ≤ 8 transition metals and ≤ 76 orbitals. NQE: the path integral is sign-free | Nothing at the structure endpoint. The FeMoco E-state isomer residue is parked as WEAK | `experiments/ROUND3/new_mechanisms_intrinsic/results/` (`decision_value.json`, `pdb_census.json`, `summary.json`) | Model-only spread < σ_solver at converged QM regions (≥ 500 atoms), **and** best classical ranking error ≥ 5 kcal/mol at ≥ 100 orbitals, **and** a QPE estimate at ≥ 300 orbitals with ≤ 1e6 physical qubits |
| K-116 | R1-SIM as a category-3 **resource claim against exact simulation of the raw finite-cluster echo F_N** ("exceeds exact classical reach, so it is a quantum simulation target") | Adversarial verification, 2/3 refute (resource, relevance). Spins needed unidentified (26–430); exact frontier 50–52; the drift is mostly two-point H, which classical spin dynamics computes on 80–160 spins in about 3 CPU-min; the comparator must be σ-level, not exact | The four-point remainder X on 3/8 shell-event series, and whether X converges beyond N = 20–22. This continues only as R1-SIM-X (§2.2, §5.1) | `experiments/ROUND3/r1sim_exact_reach/` (`reach_summary.json`, `verify_classical/verify_summary.json`, `verify_resource/n22_summary.json`, `verify_relevance/`) | Only as R1-SIM-X: X drifts ≥ 0.01 per step at N = 22–24 on ≥ 2 series on both probes, and a costed quantum X estimator beats the classical-spin-dynamics + exact-X hybrid. This never revives K-105 |

**Corrections to earlier kills (2026-09-28, CRITIC C1/C2/O-4/O-5/O-6):**
- **K-105 and K-109.** The twin and reversal-window arms were measured on N = 10 finite clusters, which carry a conserved-charge floor ≥ 3σ, so those arms are N = 10-conditioned. The load-bearing arms are:
  - forward-model error (5–66 σ from methyl rotation, 1 kHz site offsets and 15% reversal mismatch);
  - value accounting (joint gain ≤ 1.2–3).
- **K-111.** The kill rests on identifiability, not observability. The many-body correction (13–40% of the splitting) is equivalent to a 1.7–2.7 meV one-body barrier shift and is degenerate with the unknown per-methyl V3 nuisance. Splittings of kHz–MHz are not unobservable per se.
- **K-107.** It covers the A80 learned energy only. Physics-based all-atom force fields are not covered; that regime is examined in round 4.
- **G1 hardness exponent.** The p_hit ~ e^{−0.028 L} exponent is confounded by fixed-depth (200-iteration) relaxation and must not be quoted as a hardness measure.

### Round 4 kills (2026-09-28; `experiments/ROUND4/SYNTHESIS.md`; caveats in `experiments/ROUND4/CRITIC.md`)

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-117 | Quantum dynamics or sampling algorithms for **physics-based all-atom** protein folding kinetics and ensembles, explicit or implicit solvent. Covers Carleman, KvN/Liouville, Fokker–Planck/LCHS/Schrödingerisation, overdamped-FP rate estimation, nonlinear-SDE algorithms, oscillator algorithms, continuous Gibbs samplers (Witten-Laplacian, QRELD), QMCMC/free-energy estimation, nonreversible-chain speedups, MSM/annealer path sampling, and quantum-computed forces | **No applicable algorithm (not classical ease).** Literature: 12 families, 53 verified arXiv records; every claim of s > 2 is against the wrong baseline or needs a missing precondition. Measured preconditions (Trp-cage, amber14 + GBn2): Carleman R ≥ 4.3e3–1.2e5 (R < 1 needed; ∞ for NVE); negative curvature on 8/10 thermal snapshots; λ_max = 2.1–3.2 ps⁻¹. Derived floor: T\*_Q,2 ≥ 2.2 yr at t_T = 10 ns (≥ 2.2e4 yr at 1 µs); B\*₂ ≥ 4e11 steps exceeds every twin cost. **Unverified** | Nothing. Weighted ensemble (NTL9 250 GPU-days), MSM, metadynamics and REST2 supply the capability. A hypothetical s ≥ 3 would break even: T\*_Q,3 = 1–160 d and T\*_Q,4 = 2.6 h–10 d at 10 ns | `experiments/ROUND4/allatom_superquadratic/` (`families.json`, `floor_allatom.json`, `floor_allatom_table.md`, `work/S4_1L2Y.json`, `work/S5_*`, `lit/records.json`) | A quantum algorithm with s ≥ 3 against practical fixed-step MD or weighted ensemble, whose preconditions hold for chaotic, non-polynomial, multi-basin Langevin dynamics, **and** a compiled force-oracle Toffoli count, **and** T\*_Q,s ≤ 1 day at a stated t_T. **Or** logical Toffolis ≲ 0.4 ns (s = 2, best-case folder) |
| K-118 | **Programmable analog dipolar quantum simulators** (Rydberg tweezers, polar molecules, NV ensembles, natural NMR solids) as the quantum side of R1-SIM: the protein ¹H secular-dipolar echo F_ab to σ = 0.01 at 40–120 µs for 20–100 spins | **Practical.** DERIVED structural obstruction: the traceless rank-2 target cannot be reached from electric-dipole exchange by global Floquet rotations, and the graph is non-bipartite. The only fix is a ±C3 encoding-swap composite (exact at zeroth order). MEASURED sensitivity: σ is reached at 1.4–1.7% coupling error, 0.25–0.53% position error, 0.10–0.38% motion, 1.1–1.4% isotropic residual. INFERENCE budget: 42–100σ demonstrated, 1.3–16σ optimistic near-term, 1.2–6σ best undemonstrated. **Unverified** | Nothing. At 40 µs, exact b-aware classical clusters reach σ in minutes (K-119). At 80–120 µs neither the classical nor the analog route reaches σ | `experiments/ROUND4/analog_simulator/` (`sens_summary.json`, `floquet_*.json`, `budget.json`, `lit.json`) | **All of:** a programmable-geometry platform demonstrating a traceless dipolar coupling (Jz/Jxy = −2, isotropic residual ≤ 1%) with Floquet reversal; per-atom loss ≤ 0.5%; pulse error ≤ 0.003 rad over ≥ 80 cycles; motion ≤ 0.04% of spacing, in ≥ 100-atom arbitrary 3D arrays; **and** a classical cross-family F estimate that fails at σ at a time where the site-resolved visible signal is ≥ 1σ |
| K-119 | **R1-SIM-early**: "the converged secular ¹H echo F_ab at t ≈ 40 µs, inside every T3 estimate, is beyond σ-level classical reach" (CRITIC C1) | **Measured cross-family agreement, provisional.** Post hoc under PREREG H-2, plus pre-registered Addendum B corroboration; the literal parent rules could not fire because their comparator was refuted (deviation D-R4-2). Two exact b-aware families (5 implementations across 3 independent code paths) agree to ≤ 0.0055 on 8/8. Thermodynamic E1 vs E2 ≤ 0.0045. b-aware vs spinDMFT ≤ 0.0096. Isolated {a, b} clusters of 10–12 spins are within σ on 3/3 b-remote series. Cost: 2.7–19 single-core CPU-min for all 8 series, vs 2.8–10 h per probe on an FT QPU (DERIVED) | Nothing at 40 µs | `experiments/ROUND4/spindmft/` (`analysis.json`; `verify_classical/verify_summary.json`; `verify_resource/verify_summary.json`, `breakeven_40us.json`; `verify_relevance/relevance_checks.json`); `experiments/ROUND4/tx_early/verify_classical/verify_summary.json`; `experiments/ROUND4/director/cross_family.json` | On replication (R-1: 1PGA p390, 1UBQ p487, ≥ 2 further b0 orientations, and optionally the rotor-averaged model), an exact b-aware family and a thermodynamic estimator disagree by > 3σ on ≥ 2 series at t ≤ 40–60 µs. Category 3 only. **Never revives K-105** |
| K-120 | **Methodological.** The round-3 hybrid comparator F̂_∞ = H_∞(CSD) + X_N, and every convergence rule or approximation target stated on X = F − H − floor: T-X-early's \|X₂₂ − X₂₀\|, the ROUND3 T-X0 to T-X3 rules, the K-116 revival trigger "X drifts ≥ 0.01 per step", R3-HYB's T-H1, and analog revival item 4. Also single-family step or plateau convergence claims for F_ab | Measurement: pooled dF/d(H + floor) = −0.03 ± 0.10 at 40 µs (1 required; z = 6.2); X rises on 8/8 series while F is flat; the hybrid is 2.7–9.5σ below the b-aware values (0/8 within σ); the probe-family plateau is 2.5–7σ off at sites with out-of-cluster partners. Derivation: F = 1 − 2 w_b, so norm spreading away from b leaves F unchanged | N/A (a comparator and criterion retirement) | `experiments/ROUND4/spindmft/analysis.json` §4.4; `spindmft/verify_classical/verify_summary.json` (`flatX_recomputed`); `tx_early/backtest.json`; `tx_early/verify_resource/tracking.json`; `tx_early/verify_relevance/crossfamily.json` | Never as an F_∞ estimator at t ≤ 80 µs. X may be reported as a diagnostic. Convergence claims must be on F, in ≥ 2 b-aware families with M2_b coverage reported, plus a thermodynamic estimator |

**Corrections to existing entries (2026-09-28, round 4).** These supersede the round-3 correction bullets for K-105, K-109 and K-111; the older bullets are kept for history.

**K-105** (secular OTOC(1)). Replace the "Kill type" column and the 2026-09-28 correction bullet.

- **Load-bearing arm: the reversal horizon of a site-resolved echo.**
  - Under the local polarisation-echo envelope (T3 ≈ 4 T2), the profiled median joint gain is 1.09–1.60 with
    moderate priors (1.13–2.10 with none). This holds **even at t_cl = 0**, i.e. if the whole converged echo were beyond
    classical reach. So the arm no longer depends on N = 10 twins.
  - With t_cl = 40 µs (K-119): 1.06–1.33 under PE, and 1.36–2.23 under the global LE envelope.
  - [MEASURED, `ROUND4/redteam_kills/profiled_summary.json`; N = 10 Fisher model, rotor-averaged, nuisance-profiled;
    unverified lane]
- **Secondary arm:** out-of-family per-pair motional scaling leaves a structural bias of 0.1–11× CRB_q. That caps the
  accuracy gain at 1.06–1.52 (PE).
- **Removed as load-bearing:**
  - "forward-model error 5–66σ": the misfit is removed by profiling offsets, reversal scaling and order-parameter
    families, which retains 18–83% of the FI without reducing g;
  - "value ≤ 1.2–3 even with ideal reversal": ideal reversal at t_cl = 80 µs gives 2.5–6.9.
- **Reopen only if:**
  - for usefulness (g ≈ 2–3.3): a measured protein **site-resolved** T3/T2 ≥ 15 **and** converged classical reach
    t_cl ≤ 80 µs;
  - for the R1 revival bar (g ≥ 10): T3/T2 ≳ 20–50 **and** t_cl ≲ 40 µs, which is at the boundary K-119 establishes for
    1UBQ.

**K-109** (DQ echo). Replace the "Kill type" and "Reopen" columns.

- **Load-bearing arm: value against the measured classical reach.** Non-methyl butterflies are step-stable to 80 µs at
  N = 18 (1UBQ p19; a single-family step statistic, C-R4-13). With secular transfer on the classical side, g_med is:
  - 1.27 / 1.32 / 1.78–1.97 at 12.5 T2;
  - 1.53 / 1.62 / 2.09–2.50 at 19 T2.

  [MEASURED, `ROUND4/redteam_kills/sitewise_tcl.json`]
- **Retracted:** "the ε = 3e-5 twin reproduces the echo to 140–220 µs; g ≤ 1.16; reopen at T3_DQ/T2 ≥ 50". This was an
  N = 10 artefact: at N = 10 everything is classically reachable.
- **Residue:** 1PGA p390, methyl butterfly HG21/THR53 (RT-DQ-methyl, §2 item 12).
- **Reopen only if all of these hold:**
  1. a measured protein site-resolved T3_DQ/T2 ≥ 19;
  2. converged classical reach ≤ 50 µs at the FI-bearing butterflies, from a partner-complete, rotor-averaged,
     **cross-family** ladder;
  3. a profiled g_med ≥ 2 with secular transfer on the classical side.

**K-111** (methyl rotors). Replace the "Kill type" column and the correction bullet.

- **Load-bearing arm: resolvability plus classical exactness.**
  - The identifiable many-body quantity is the partner-state doublet J. It is *not* degenerate with V3, so CRITIC C2's
    degeneracy argument is incomplete [DERIVED].
  - Against glass disorder σ_V3 ≥ 1 meV, the doublet is resolved in 0/32 pair cases at V3 = 60–100 meV and 2/32 at
    30 meV [MEASURED from lane data].
  - J is an exact 2-rotor classical computation (seconds).
- **Reopen only if all of these hold:**
  - a real protein has ≥ 3 coupled methyls with V3 ≤ 50 meV;
  - \|J\| ≥ 2.355 Δ \|d ln Δ/dV3\| σ_V3 with a measured σ_V3;
  - the needed cluster exceeds exact 3–4-rotor reach.

**K-116** (R1-SIM against exact F_N). Its reopen clause ("X drifts ≥ 0.01 per step…") is void under K-120. Replace it
with:
> Only as R1-SIM-late, in a spin-off register outside the mission. Reopen when all three hold:
> - (i) two b-aware cluster families plus a thermodynamic estimator fail to agree within σ at N ≥ 22–24;
> - (ii) this happens at times where the site-resolved reversal envelope leaves ≥ 1σ of visible signal under physical T2;
> - (iii) a costed quantum estimator, digital or analog (see K-118), beats that classical portfolio.
>
> Never revives K-105.

**K-115** (QPE electronic structure). Add to the FeMoco E4 note: "WEAK. Survives only with a measured σ_m ≤ 1.2
kcal/mol (σ_best = 5, 1 Å lever), a best classical error ≥ 5 kcal/mol, and ≤ 30 energies at ≤ 100 orbitals (≥ 10.8–20.5
QPU-days per question). arXiv:2601.04621 concerns the resting state and is not load-bearing."

**K-107.** Scope note: "A80 learned energy only. The physics-force-field regime is K-117, which has a different kill
type (no applicable algorithm, not classical ease)."

**KILLBOOK "Corrections to earlier kills (2026-09-28)" block.** Supersede its K-105/K-109 bullet and its K-111 bullet
with the entries above, via a dated note (do not delete).
- The K-105/K-109 bullet's "load-bearing = forward-model error + value" is superseded.
- The K-111 bullet's "identifiability" is superseded.

**CRITIC C1.** Withdrawn at 40 µs. Replacement:
> The round-3 hybrid double-subtracts at early times, and F does not carry the (1 − H)/N floor as an additive bias
> (MEASURED in-family at N ≤ 22). Probe-centred clusters are still 2.5σ and 6.5σ low on 2/8 series (p19 b8, p245 b7),
> because b's strongest partners enter only at ranks 24–48. Clusters that contain b's partners remove this. At
> 80–120 µs the question is open, as a cluster-family problem (§1.3).

**Round-4 critic caveats (CR4-A/B):**
- **K-105.** The profiled gain was computed on probe-centred N = 10 Fisher models in which some butterflies carry only 4–23% of their M2. Adding their missing partners (N = 12) keeps the site-resolved (PE) medians < 2 on 4/4 probes (max 1.57), but it raises the global-envelope (LE) medians to ≥ 2 on 2/4. The drift runs toward quantum, so "≤ 1.6" is an N = 10 number.
- **K-119** is a classical-ease result. At a 10 ns logical T layer the quantum circuits would reach parity with one CPU core, so the kill must not be argued from a QPU cost ratio.
- **The 80 µs residue** is 2.2σ visible under the global LE envelope but 0.41σ under PE. "Outside the mission" therefore holds only under PE.
