# Round 3 synthesis (program director)

_2026-09-28. File: `research/experiments/ROUND3/SYNTHESIS.md`._

**Inputs**
- 9 lane reports in `research/experiments/ROUND3/<lane>/`.
- 6 adversarial verdicts, 3 each for `r1sim_exact_reach` and `r1sim_hybrid_plus`. These were the only lanes that returned SUPPORTS. The other seven lanes returned KILLS or WEAK and were not sent to verifiers. A kill does not need to survive verification, but it stays open to attack.

**Consolidation rule.** A positive claim SURVIVES only if at most 1 of its 3 verifiers refutes it with a specific, credible argument.

**Tags.** MEASURED / DERIVED / THEORETICAL / LITERATURE-SUPPORTED / INFERENCE / UNPROVEN. **[DIRECTOR]** marks a cross-check I made in this synthesis from files already on disk. That took under 1 CPU-min of arithmetic and no new dynamics.

**Level scales.** The lanes quote theoretical and practical levels L0–L6. The only written scale in the repo is the T2 header table (`theory/PROOFS/T2_sampling_speedup_statement.md`):

| Level | Meaning |
|---|---|
| L1 | Query separation on a constructed family |
| L2 | Same-chain walk speedup |
| L3 | L2 plus the oracle's gate cost |
| L4 | Compared with the best classical method |
| L5 | Compiled validation |
| L6 | Hardware |

Some lanes, like the discovery sprint, use "L6" to mean a separation proved in an abstract model. Where a lane wrote "L6-negative", this synthesis writes **proved no-go (theorem)**. Housekeeping item H-1 in §6 is to fix one scale in the charter.

---

## 0. Bottom line

- **Round 3 found no quantum advantage for protein-structure computation.** It had 9 lanes and about 30 new mechanisms or variants. Among them were QeMCMC, 11 super-quadratic algorithm families, speedup exponents from s = 2 up to exponential, GBS, methyl-rotor tunnelling, quantum SDP, six derivation-level mechanisms, quantum-memory learning, the double-quantum (DQ) NMR echo and fault-tolerant QPE on active sites. New kills: K-106 to K-116 (§4).
- **One narrow positive claim survives verification (`r1sim_hybrid_plus`, refuted 1/3).** At N = 16/18, the six polynomial-cost approximation families tested fail to reproduce the exact finite-cluster first-order dipolar echo, OTOC(1). This is empirical approximation-failure on classically exact-simulable instances. It is not an advantage in any of categories 1–6.
- **One measurement is scientifically interesting but is not an advantage (`r1sim_exact_reach`, refuted 2/3 as an advantage claim).** The finite-cluster echo is still unconverged at N = 22. A new exact decomposition, F = H + floor + X, shows that most of that drift is a two-point quantity H, and classical spin dynamics computes H in polynomial time. The open physics question is now confined to the four-point remainder X (R1-SIM-X, §2.2, §5.1).
- **The most consequential new fact is classical [MEASURED, replicated by two independent lanes].** Distance-geometry seeding from native-free distogram expected distances (weighted SMACOF plus about 400 energy+gradient evaluations) reaches or beats the best basin of the 256-restart census on 14/16 crops at L = 150. The exponential decay of random-multistart p_hit therefore reflects a weak baseline, not classical hardness. That removes the hardness premise every learned-energy quantum route needed.

---

## 1. Consolidated table

Lanes with no verifiers were not sent for verification because their lane verdict was KILLS or WEAK. The ladder column uses R1_SYNTHESIS's scale:

| Category | Meaning |
|---|---|
| A | New formulation |
| B | Empirically useful |
| C | Advantage vs a strong classical baseline |
| D | Resource-normalised |
| E | Scaling |
| F | Theoretical/query |
| G | Fault-tolerant |
| H | Hardware |
| I | End-to-end |

| Lane | Lane verdict | Verifiers (refute / 3) | Consolidated status | Theoretical level | Practical level | Ladder (A–I): reached / failed | Decisive number |
|---|---|---|---|---|---|---|---|
| `qemcmc_exact` | KILLS | none | **KILLED** (K-106) | L1: small-n exact numerics; k_q/k_c = 0.56–0.75 (sub-quadratic) in the only family run to n = 10 | L0 | A reached (the method is prior art: Layden 2023); C failed; D negative | Largest δ_q/δ_c^½ = **0.85** (> 1 needed; 0/149 records exceed it). Largest gap ratio **12.7** vs break-even **784** (optimistic) to **2.3e5** (central) [MEASURED/DERIVED] |
| `hardness_what_it_takes` | KILLS | none | **KILLED** (K-107) | L2 for the generalised floor T*_Q,s (DERIVED, conditional on T3's G(L)); L0 for any s ≥ 3 on this energy | L0 | F: negative bound; C failed; D negative | DG portfolio reaches E_ref in a median **420** evaluations at L = 100–150 (max 5.8e4). Every exponent s, including an idealised 10-step exponential algorithm, needs logical Toffolis of at most **~3 ns** at L = 100–500 [MEASURED + DERIVED] |
| `structured_speedups` | KILLS | none | **KILLED** (K-108) | L0 for the protein task; the parent separations hold only on their own instance families | L0 | A: exact max-LINSAT encoding (DERIVED); F: none, preconditions absent | Girth = d⊥ = **3** on 64/64 A80 pair graphs, so DQI gets l = 0. Every family's per-residue exponent is **12–51×** α_c = 0.0295 nats [MEASURED + DERIVED] |
| `r1sim_exact_reach` | SUPPORTS | **2/3 refute** (resource, relevance); the classical verifier did not refute but corrected it | Split. **Advantage/break-even framing KILLED** (K-116). **Measurement INTERESTING**: no verifier disputes the numbers, and one verifier extended them to N = 22 | L0: no separation; the drift is mostly two-point | L0: quantum side not costed; the comparator is exact simulation, not the σ-level classical method | E partial (classical side only); C and D not reached | \|F₂₂ − F₂₀\| = **0.017–0.018**, above the 0.0147 threshold (p19, site 8, 320 µs) [MEASURED]. In 5/8 late series, **75–109%** of the last-step drift is H + floor, which classical spin dynamics computes on 80–160 spins in about 3 CPU-min [MEASURED] |
| `r1sim_hybrid_plus` | SUPPORTS | **1/3 refute** (relevance) | **SURVIVES** (narrow, corrected; §2.1) | L1: narrow empirical; not hardness | L0 | C failed against exact classical simulation (the failure is of approximations only) | Best of about 6 polynomial families: **0.050–0.066** vs σ = 0.01 at N = 16/18 (5–7σ). Exact classical simulation takes **0.06–0.3 h** on one thread at the same N [MEASURED] |
| `dq_echo_envelope` | KILLS | none | **KILLED** (K-109) | L0–L1 | L0 | A reached (DQ variant); B not reached; C failed | Median joint gain **≤ 1.16** (1.00–1.04 with the physical T2) vs ≥ 2 required. The ε = 3e-5 twin reproduces the echo to 140–220 µs, beyond T3_DQ ≈ 122–134 µs [MEASURED] |
| `new_mechanisms_A` | KILLS (9/9) | none | **KILLED** (K-110 to K-113); R-ROTOR parked | L0 | L0 | A reached (NA-1, GBS with a contact kernel); C failed; D negative (NA-3) | GBS wins **3/64** cells (≥ 48 needed). Rotor splittings **≤ 0.055 µeV**. QSDP is **1e5–1e13×** slower (L^7.2 vs L^2.1) [MEASURED + DERIVED] |
| `new_mechanisms_quantum_data` | KILLS | none | **KILLED** (K-114) | **Proved no-go (theorem):** memory gain = 1 per structural parameter; ≤ k for k parameters; L0 for any exponential separation | L0 | F: negative theorem | Memory gain exactly **1**. Bell/QFI **≤ 0.032** at t ≥ 80 µs (p = 1), times p² ≈ 2e-9 at thermal polarisation. Transduction fidelity **≤ 1.4e-7** [DERIVED + MEASURED] |
| `new_mechanisms_intrinsic` | WEAK | none | **WEAK** (unverified). 7/8 scenarios killed (K-115); FeMoco E-state residue parked | Structure L0; chemistry ≤ L1 | Structure L0; chemistry-level constant-factor parity | B not reached (structure); G: a negative-leaning estimate exists | Exact-solver gain **≤ 0.23 Å** under favourable assumptions (0.05 Å central), leaving 0.28 Å. **10–1640 QPU-days** per structural question at 76 orbitals [DERIVED/INFERENCE] |

### 1.1 Corrections to lane statements adopted in this synthesis

**C1. The DG-seeding claim is corrected, then promoted to MEASURED** (`hardness_what_it_takes`).
- The earlier exploratory claim was "61/64 runs reach the deepest known basin". That was a mis-transcription: the source says the expected-distance pair gave the lowest *DG* basin in 61/64 runs.
- The replicated, native-free result: DG-E1 reaches E_ref + 20 nats on 8/16, 11/16 and 14/16 crops at L = 60/100/150.
- `structured_speedups` replicated it independently: level-1 seeding beats the census-best energy on 0/5/10/14 of 16 crops at L = 30/60/100/150.
- Caveat: census endpoints are under-relaxed. Under symmetric polishing, DG is lower on 5/8 crops, and in 4 of those 5 it is in the same fold (1.4–1.9 Å).
- The statement in `CURRENT_STATE` and the round-3 task text should be replaced by this one.

**C2. The early-window claim is retracted** (`r1sim_exact_reach`). The claim was that the early window (≤ 160 µs) is within exact reach for p19. The flat F at p19, site 1, 160 µs is a cancellation: H + floor fell by 0.010 while X rose by 0.010 [MEASURED, verify_classical].

**C3. N_σ is not a classical-cost measure** (`r1sim_exact_reach`). The figures N_σ = 58–557 extrapolate raw F_N. With the N = 22 point included, the model spread for the spins needed is **26–430** and F_∞ ranges over 0.03–0.21 [MEASURED/DERIVED, verify_resource].

**C4. The exact frontier is 50–52 spins, not 48** (`r1sim_exact_reach`). The exascale memory was under-counted by 2×, and a 50-qubit universal simulation already exists (JUQCS-50, arXiv:2511.03359; abstract verified by the verifier) [LITERATURE-SUPPORTED].

**C5. "Errors do not shrink with polynomial method order" is false as worded** (`r1sim_hybrid_plus`).
- The coupled-cluster (CQC) error falls monotonically with cluster size k: 0.54 → 0.24 → 0.24 → 0.062 → 0.035 for k = 4 → 12.
- It falls only as k approaches the whole system.
- At fixed k = 12 the error grows from N = 16 to 18 (0.035 → 0.062) [MEASURED, verify_resource].

**C6. The polynomial frontier is better than the lane reported** (`r1sim_hybrid_plus`). The lane reported 0.081/0.275. An exact-base first-order cluster expansion reaches 0.050–0.066 uniformly across all four cells [MEASURED, verify_classical].

**C7. The kill rule was noise-limited at N ≤ 16** (`r1sim_hybrid_plus`). At N = 14, independent exact typicality vectors score 0.013–0.018 against the reference, so "did not fire" was partly guaranteed by construction [MEASURED, verify_resource].

**C8. CCE non-convergence is a variance statement** (`r1sim_hybrid_plus`). With SE 0.28–0.33 it is not a demonstrated bias. The verifier's deterministic exact-base expansion does show the non-convergence: second order diverges to 0.23–1.03 [MEASURED].

**C9. [DIRECTOR] A verifier inference is falsified by another verifier's measurement.**
- `r1sim_hybrid_plus/verify_resource` inferred dF(20→22) ≈ 0.003 on p19 and convergence by N ≈ 22–24.
- `r1sim_exact_reach/verify_resource` measured |F₂₂ − F₂₀| = 0.017 at p19, site 8, 320 µs.
- The inference is therefore wrong for at least that series.

**C10. The pre-registered step-convergence KILL rule is flawed** (preregistration).
- Under a 1/N drift, Δ_N ≈ 2c/N² falls below threshold at N ≈ 15–28 while the true error c/N is still 0.1–0.2 [DERIVED, `r1sim_exact_reach`].
- It must be replaced by an extrapolation- and decomposition-based criterion (§2.2), logged as a deviation before any N ≥ 22 output is analysed.
- Current formal status: the R1-SIM KILL ("converged by N ≤ 20") is excluded on p19, because the N = 20 → 22 step at site 8, 320 µs is 0.017 > 0.0147.

**C11. QM-23's "< 0.1 Å" argument is wrong for local endpoints** (`new_mechanisms_intrinsic`).
- PDB pairs show large local changes [MEASURED]:
  - myoglobin Fe out-of-plane: 0.364 vs 0.023 Å;
  - P-cluster ligand switches: Fe–OG 2.80 → 1.90 Å and Fe–N 3.30 → 2.15 Å;
  - hemocyanin Cu–Cu: 4.61 → 3.59 Å.
- QM-23 stays killed, now on the model-floor argument instead (K-115).

**C12. [DIRECTOR] Cross-check of the N = 22 decomposition.**
- The measured F₂₂(p19, site 8, 320 µs) = 0.2282 ± 0.001 [MEASURED, verify_resource] lies between two predictions:
  - flat-X decomposition: 0.2364, with site 8 flagged as not flat (band about ±0.019), so it is not excluded;
  - c/N law: 0.2228, which misses by +0.005, about 5× the noise.
- Using the predicted H₂₂ = 0.0645 and floor₂₂ = 0.0379, X₂₂ ≈ 0.126 against X₂₀ = 0.134. So dX ≈ −0.008 ± 0.005 [INFERENCE: H₂₂ is predicted, not measured].
- The four-point remainder at this shell-event site is still drifting, but more slowly than before (−0.014 → −0.008).
- The discriminating series are sites 1 and 7, where X is flat. They have not been measured at N = 22.

---

## 2. Surviving and interesting claims

### 2.1 R3-HYB (`r1sim_hybrid_plus`): SURVIVES, narrow and corrected

**What the evidence supports [MEASURED].** The test covers the idealised, isolated, static 1UBQ ¹H dipolar model (probes p19 and p245, orientation 0, reference Trotter circuit) at N = 16 and 18. Six polynomial-cost classical approximation families were tried:
- Starkov–Fine coupled quantum clusters;
- classical spins with quantum promotion;
- a quantum core with a quantum-cluster bath;
- cluster-correlation expansion (CCE) on a hybrid base;
- exact-base first-order cluster expansion;
- path-aware exact subclusters.

Four zero-compute correction and extrapolation adversaries were also tried. None reproduces the exact finite-cluster OTOC(1) F_ab(t) at the instrument sites within σ = 0.01 over 80–320 µs on both probes:
- the best reaches 0.050–0.066, which is 5–7σ, with bias bounds above σ in all 74 scored rows;
- the error falls only as the exact core grows toward the whole system;
- second-order expansions diverge.

**What it does NOT support:**
- **Classical hardness.** Exact simulation reproduces every target in 0.06–0.3 h on one thread.
- **Anything about the converged or physical echo.** The target itself moves by up to 0.057 from N = 16 to 18.
- **Any of claim categories 1–6.**
- **Any protein-structure value.** K-105 stands: the window is 13–40 T2, beyond the reversal horizon.
- **Universality over approximation methods.** MPS/TDVP, neural quantum states, spinDMFT/nl-spinDMFT, DAOE and cluster truncated Wigner were not tested [UNPROVEN].
- **Novelty.** Starkov–Fine was built for free-induction decays, and spin-½ lattices lacking classical-spin chaos is known [LITERATURE-SUPPORTED as cited by the relevance verifier].
- **Relevance at this precision.** σ = 0.01 is 13–19× finer than the model's own size-truncation error at N ≤ 16, and 5–66× finer than its physical model error [MEASURED, relevance verifier].

**Decisive next experiment: T-H1, retarget the approximation question at X.**
- **Why.** H is already classically computable (§2.2), so approximation-failure on F is uninformative. The only meaningful approximation question is whether X = F − H − floor is polynomially approximable.
- **Protocol.**
  - Reference: deterministic sector-exact at N = 16; typicality with M ≥ 4 vectors at N = 18/20, so that err ≤ σ/3 and the noise-floor defect (C7) is removed.
  - Methods: exact-base first-order cluster expansion (`r1sim_hybrid_plus/verify_classical/subcluster.py`), base 9–12, applied to X, with H from classical spin dynamics.
  - Budget: single-threaded, ≤ 15 CPU-min per run, ≤ 1 GB, checkpoint per base size, about 30–45 CPU-min in total. N = 20 references come from T-X1 (§2.2).
- **KILL the approximation residue** if max |X_approx − X_exact| ≤ σ + 2·err at N = 18 on both probes for some base ≤ 12.
- **SUPPORT (narrow)** if the error on X is ≥ 3σ on both probes at N = 18 and 20 and does not fall monotonically with base 9 → 12.
- Neither outcome touches K-105.

### 2.2 R3-SIM (`r1sim_exact_reach`): measurement INTERESTING; advantage framing KILLED (K-116)

**What the evidence supports.**
1. **Faster exact code [MEASURED].** A sector-restricted, spin-flip-folded, forward-reusing exact echo code (`fastecho.py`) is about 18× faster than the reference at N = 20, at 0.44 s per vector-step on one core. It is validated against:
   - the reference, to 4e-13;
   - the governor's independent N = 20 run, to 0.0022.
2. **Unconverged through N = 22 [MEASURED].** At p19, site 8, 320 µs, the ladder is F = 0.2867 / 0.2713 / 0.2451 / 0.2282 at N = 16 / 18 / 20 / 22. The N = 20 → 22 step (0.017) is above the pre-registered threshold. So the pre-registered KILL ("converged by N ≤ 20") is excluded.
3. **Exact decomposition [DERIVED, validated to 1e-14].** F_ab = H + floor + X, where:
   - H = Σ_j G_aj² is b-independent and two-point;
   - floor = Tr[W_rest (Z_tot/N) W_rest (Z_tot/N)]/2^N → 0;
   - X is the four-point remainder.
4. **Where the drift sits [MEASURED].** In 5/8 late-window series, X is flat to ≤ 0.004 per step and 75–109% of the drift in F is in H + floor. Classical spin dynamics reproduces the exact H to ≤ 0.012 (≤ 0.007 at N = 20), and computes H at N_c = 80–160 in about 3 CPU-min. H is still falling beyond N = 20: at 320 µs it goes from 0.066 at N_c = 20 to about 0.022 at N_c ≥ 80.
5. **Exact frontier [DERIVED from measured costs].** About 26 spins for one echo curve per workstation-day, and 50–52 on an exascale machine per month (C4).

**What it does NOT support:**
- **An advantage in any of categories 1–6.** The quantum side is not costed against the σ-level classical estimator. Against exact classical simulation only, break-even is N* = 48–52 at 1–191 days per curve on a fault-tolerant machine [DERIVED, resource verifier].
- **An identified spin count.** The spins needed are 26–430 depending on the model.
- **Protein-structure value.** 240–320 µs is 13–40 T2, and the observable amplitude there is 0.03–0.13σ [DERIVED/INFERENCE, relevance verifier]. K-105 stands.
- **Hardness of the whole echo.** Most of the drift is H.
- **Novelty of "dense dipolar dynamics exceed exact reach".** This is established physics of dipolar solids, e.g. O'Brien et al. arXiv:2109.02163 and Álvarez–Suter–Kaiser arXiv:1409.4562 [LITERATURE-SUPPORTED as cited by the verifier].

**Decisive next experiment: T-X, the four-point-remainder test.** Pre-register it before any N ≥ 22 output is read. It replaces the flawed step rule (C10).
- **T-X0. Back-test (≤ 10 CPU-min, 1 core, existing data only).**
  - Predict F₂₀ for all 8 series at 160/320 µs from N ≤ 18 data only: H₂₀ from classical spin dynamics plus the offset at 18, floor₂₀ from κ at 18, and X₁₈.
  - Kill the hybrid route if the error exceeds σ + 2·err on ≥ 2 of the 5 flat series. R1-SIM then stays open as posed, and T-X1 decides it.
- **T-X1. Full N = 22 curves, both probes (governor).**
  - Setup: `fastecho.py` flip mode, complex64, checkpointed per time point, 2 workers at ≤ 1 GB each, about 3–6 core-h in total.
  - Times: t = 160, 240 and 320 µs, plus 200 and 280 µs if the budget allows.
  - Sites: 1, 7, 8 and 9, with exact H₂₂ (two inverse passes) and exact floor₂₂.
  - This yields X₂₂ exactly.
  - Recommendation: once the user allows it, replace the slow `nmr_cone.py` N = 22 governor jobs (about 18× slower) with this.
- **T-X2. Classical spin dynamics (≤ 15 CPU-min).** H at N_c = 22, 24, 40, 80 and 160 on both probes, 16k trajectories, with the exact-minus-classical offset at N = 22.
- **T-X3. Shell-event series (governor, ≤ 1 GB per job).**
  - Series: p19 sites 8/9 and p245 site 8.
  - Method: b-aware cluster family (nearest to {a} ∪ {b}) at N = 16–22.
- **Decision rules:**
  - **KILL R1-SIM (converged echo classically answerable to σ).** Both of these hold:
    - **flat series:** |X₂₂ − X₂₀| ≤ 0.005 on ≥ 4 of 5, and F₂₂ within ±0.007 of the decomposition predictions (p19 320 µs: site 1 = 0.1475, site 7 = 0.2302);
    - **shell series:** X converges in T-X3 (|ΔX| ≤ 0.005 on two consecutive steps).

    Then F_∞ = H_∞(classical spin dynamics) + X_N is a polynomial estimator at σ.
  - **KEEP OPEN.** Either of these holds:
    - |X₂₂ − X₂₀| ≥ 0.01 on ≥ 2 flat series on both probes, which would be a false X plateau;
    - F₂₂ at sites 1 and 7 lies within ±0.004 of the c/N predictions (0.1421, 0.2172).

    Only then is it worth costing a quantum X estimator (about N logical qubits, 320 Trotter layers, 1e4–2e5 shots per point) against the hybrid classical estimator. Prior: low [INFERENCE].
  - Neither branch revives K-105.

### 2.3 Parked residues (not leads)

Each is recorded so it is not lost. None has a credible route to an advantage in protein structure.

| Residue | Why parked, not a lead | Next test (governor-runnable) | Kill criterion |
|---|---|---|---|
| R1-SIM-DQ: DQ σ-cone inside T3_DQ ≤ ~130 µs | K-109: DQ value < 2 even with ideal reversal | Exact or typicality DQ echo at N = 12–18, 1UBQ p19/p245 and 1PGA p390 (≤ 1 GB, checkpointed) | \|F_N − F_{N+2}\| < σ for all t ≤ T3_DQ at some N ≤ 16 |
| QeMCMC small-n exponent (oracle-tuned (g,t), relaxed tables) | Cost gap of 2–5 orders (784–2.3e5 needed vs ≤ 12.7 measured) | Matrix-free Krylov gaps at n = 11–14; (g,t) tuned by the same rule on both sides; warm-start TV as the primary metric | Bootstrap CI of k_q/k_c includes 0.5, or warm-start speedup ≤ 10× |
| T = 1 sub-basin posterior sampling (NRPT: 0 round trips; only lower bounds 5.7e4–3e5 evaluations per sample) | Structural value 0.1–0.5 Å [ORACLE], below A8's transmission bar | Warm-started, per-mode NRPT/ALPS from the DG basin at L = 100–150, to get an **upper** bound per sample | Upper bound ≤ B*_4 = 4e7 evaluations, or energy–RMSD Spearman within a fold < 0.3 |
| DG-residual crops (3GAHA_100/150, 5O37A_150, 4PF3A_100, 3BHLA_100) | Probably a DG-variant problem, not hardness | Distogram-draw ensembles, contact-weighted stress, Cβ distances, then a short multistart around DG | Portfolio reaches E_ref at ≤ 1e5 evaluations on every crop |
| R-ROTOR (coupled methyl-rotor tunnelling) | The structure endpoint is unobservable (K-111); what remains is physics | Relax methyl H atoms, draw V3 from a distribution, run exact pair and triple calculations only for V3 ≤ 50 meV clusters, compare with a ring-polymer instanton estimate | Pair-cluster error < 10% at physical contacts, or no protein with ≥ 3 coupled low-barrier methyls |
| FeMoco E-state isomer identity | Chemistry level; capped by the model floor | See §5.2 | Model-only spread ≥ 3 kcal/mol, or classical ranking ≤ 2 kcal/mol |
| Multi-parameter memory window [1, 2.9–9.5] | Relevant only to single-molecule settings where copies are scarce | SDP/Nagaoka single-copy bound at N = 8–10, k = 4–9 | Collective/single-copy ratio ≤ 2 |
| DQI / Kikuchi reopen probes | No protein-derived instance with the needed structure is known | Compute d⊥ and flat-forest l50 (`s3_dqi_graph_code.py`) for NOE-assignment or coevolution parity systems; build a genuine k ≥ 3 planted triple-restraint task | d⊥ ≤ 4, or level-1 spectral/SMACOF solves the planted task |

---

## 3. Is there a quantum advantage for protein-structure computation?

**Answer: no, in every regime this program has examined. The negative is rigorous where marked and empirical elsewhere.** No claim in categories 1–6 is supported for protein structure. The program has now killed 28 discovery mechanisms and about 30 round-3 mechanisms or variants.

The round-3 evidence sharpens this into a two-sided statement [INFERENCE drawn from MEASURED and DERIVED pieces]:

> **The computations that are classically hard do not carry structural information that classical data and methods lack, and the computations that do carry structural information are classically easy.**

**1. The structure-bearing computation is classically easy on the learned energy.** This is the esmprior_v1/A80 energy on L = 30–150 ladder crops.
- A polynomial, native-free DG portfolio reaches the best-known basin in a median of about 420 energy+gradient evaluations, at most 5.8e4 [MEASURED, replicated by two lanes].
- Fold-level random multistart succeeds with probability 0.06–0.34 per restart [MEASURED].
- Generalising K-101 to speedup exponent s gives T*_Q,s = K n_b G t_T · X^{1/(s−1)} with X = AρK n_b G t_T / c [DERIVED].
- Measured against the best classical method, **any** exponent, even an idealised exponential algorithm, needs logical Toffolis of at most ~3 ns at L = 100–500. One coherent oracle step (1e8–1e10 Toffolis) costs more than the whole classical solution (0.8–86 s) [DERIVED from MEASURED; beyond L = 150 this is extrapolated, INFERENCE].
- No known super-quadratic family has its structural precondition met by this energy: girth 3, Fourier-dense, non-separable, no column structure [MEASURED].
- QeMCMC is at best quadratic at n ≤ 10, against a tuned classical proposal [MEASURED].
- This closes quantum optimisation and sampling of the learned energy at every exponent, not just the quadratic one.

**2. The classically hard computations carry no additional structural information.** These are dense-spin quantum dynamics: converged OTOC(1), DQ echoes and methyl tunnelling.
- Inside the physical reversal horizons, NMR forward models are reproduced classically [MEASURED]:
  - two-point transfer (K-104);
  - OTOC(1) (K-105);
  - the DQ echo (K-109), by the ε = 3e-5 sparse-Pauli twin to 140–220 µs, beyond T3_DQ ≈ 122–134 µs.
- The information gain over classically usable data is ≤ 1.16 in every literature envelope [MEASURED].
- The one computation measured to exceed exact classical reach is the late-window finite-cluster echo. It lies at 13–40 T2, where the physical signal is below noise [INFERENCE], and most of its finite-size hardness is a classically computable two-point term [MEASURED/DERIVED].
- Methyl-rotor splittings at protein barriers are unobservable [MEASURED model].

**3. Quantum data and quantum memory do not help [theorem for this state family].**
- For selective-polarisation ¹H dipolar states, SLD = p·dX exactly. So the quantum-memory gain is exactly 1 per structural parameter and at most k for k parameters [DERIVED].
- Memory protocols also pay p² ≈ 1e-9 at thermal polarisation.
- Molecular ¹H spins cannot be transduced (fidelity ≤ 1.4e-7) [DERIVED].
- The only exponential-class protein task, OTOC learning, is a time-reversal separation that NMR hardware already realises. It reduces to K-105 [LITERATURE-SUPPORTED + INFERENCE].

**4. Exact electronic structure hits a model floor before a solver floor.**
- The closed-form cap: an exact solver raises P(correct structure) by at most 0.7–32.6% as σ_solver/σ_model goes from 0.25 to 5 [DERIVED].
- The largest biological clusters (8 transition metals, ≤ 76 orbitals) are already within demonstrated classical reach, to about 1 kcal/mol on FeMoco (arXiv:2601.04621, preprint, as cited by the lane) [LITERATURE-SUPPORTED].
- The only residue is chemistry-level and constant-factor: 8.6 h per FeMoco-76 energy on 4.5M physical qubits vs 4e4–2.8e6 core-h. It is not a protein-structure advantage.

**What is still open (none of it is a protein-structure lead):**
- R1-SIM-X: whether the four-point echo remainder is beyond σ-level classical reach. Category 3, physics.
- FeMoco E-state isomer identity. Chemistry level, WEAK.
- T = 1 sub-basin sampling. Classically unresolved but worth only 0.1–0.5 Å.

**What this negative does NOT establish:**
- It is not a proof that no quantum algorithm can ever help protein-structure science.
- The learned-energy result covers one learned-energy class (A80, white-box, pair-additive), measured at L ≤ 150 and extrapolated to 500.
- The NMR result covers two proteins' ¹H networks at N ≤ 22, one field orientation, in idealised isolated models.
- The electronic-structure result rests on a curated census of 20 cofactor entries.
- Everything was simulator-only, with fault-tolerant costs from published and in-repo resource models.

**What would change the answer:**
- **(a) A hard learned-energy family.** An instance family where the full classical portfolio (DG, multistart, NRPT, SMC) needs more than 1e7 evaluations to reach a basin that transmits at least 1 MDE, **and** a super-quadratic quantum algorithm for white-box pair-additive energies (none is known).
- **(b) Protein reversal and value.** A measured protein T3/T2 of at least 50 for a site-resolved echo, **and** a converged classical twin that fails inside it, **and** a profiled gain of at least 2 to 10.
- **(c) Logical Toffolis at or below the ns scale,** which would reopen the quadratic routes (K-101).
- **(d) A quantum-memory separation.** A structure-relevant property family that does not reduce to k parameters and has a memory separation that survives nuisance profiling.

---

## 4. New KILLBOOK entries (K-106+)

Same columns as KILLBOOK Section B. Evidence paths are relative to `research/`.

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

---

## 5. Revival templates

### 5.1 R1-SIM-X: the four-point echo remainder (category 3, physics only)

**OLD MECHANISM.** A quantum forward simulation of the converged first-order dipolar echo F_ab(t) of dense protein ¹H networks at 80–320 µs, claimed to be beyond exact classical reach (R1-SIM).

**OLD FAILURE.**
- K-105 (structure): reversal horizon, value and cost.
- K-116 (simulation): the comparison was against exact simulation of the raw finite-cluster F_N; the spins needed are unidentified; 2/3 verifiers refuted it.
- Most of the finite-size drift is H = Σ_j G_aj², a two-point transfer quantity. K-104 applies to two-point transfer, and classical spin dynamics computes H at N_c = 80–160 [MEASURED].

**NEW MECHANISM.**
- Split the target exactly as F_∞ = H_∞ + X_∞ [DERIVED; floor → 0].
- Assign H_∞ to classical spin dynamics.
- The only candidate quantum task is X_∞, the b-local four-point operator-growth remainder, at cluster sizes where X is not yet converged classically.

**WHY THE OLD CONTROL NO LONGER APPLIES.**
- The control that compressed the drift, classical spin dynamics on a two-point quantity, acts only on H.
- X is a four-point object with no known classical-spin compression [UNPROVEN either way].
- On the shell-event series it still drifts at N = 20–22: dX = −0.014, then about −0.008 (C12) [MEASURED/INFERENCE].
- The comparator becomes the σ-level hybrid (classical spin dynamics for H + exact X at N ≤ 22–26), which is strictly stronger than the old exact-F_N comparator.
- Honest limit: this does not touch K-105. The late window lies at 13–40 T2, where the physical signal is below noise, so the result has no protein-structure value whatever the outcome.

**NEW TEST.** T-X0–T-X3 in §2.2, pre-registered with those kill rules. In short:
- **KILL** if X converges (|ΔX| ≤ 0.005) by N ≤ 22 on the flat series and in the b-aware family on the shell series.
- **ESCALATE (costing only)** if X drifts ≥ 0.01 per step on ≥ 2 series on both probes at N = 22–24.
- Budget: about 3–6 core-h under the governor, ≤ 1 GB per job, checkpointed. Prior: low.

### 5.2 FeMoco E-state isomer identity (chemistry level; WEAK)

**OLD MECHANISM.** Metal-cofactor QPE for protein structure (QM-23).

**OLD FAILURE.**
- "Structural effects are below 0.1 Å."
- Classical chemical accuracy at FeMoco.
- Nuclear quantum effects are sign-free.

**NEW MECHANISM.** Use fault-tolerant QPE energies to decide the discrete identity of a hydride or protonation isomer in the charge-moving E2/E4 states of FeMoco inside a fixed QM/MM model. This is a local structural question with 0.3–1.2 Å levers.

**WHY THE OLD CONTROL NO LONGER APPLIES.**
- (i) PDB pairs show local levers of 0.36–1.15 Å [MEASURED], so the < 0.1 Å argument fails for local endpoints (C11).
- (ii) The classical chemical-accuracy result is for ranking FeMoco's **resting-state** spin isomers. For charge-moving E4 isomers in ≥ 100-orbital spaces, the UCCSD ordering uncertainty is about 5 kcal/mol [LITERATURE-SUPPORTED as cited by the lane; arXiv:2601.04621 is a preprint].
- The control that still applies is the model floor. Even an exact solver leaves 0.28 Å of expected error under favourable assumptions, and gains 0.05 Å under central ones [DERIVED].

**NEW TEST.**
- **Model-floor ladder.** Model-only spread of E4 isomer energies across QM-region size, electrostatic-embedding variants and MD snapshots on 3U7Q-based models.
  - **KILL** if the model-only spread is ≥ 3 kcal/mol, because the exact-solver gain is then ≤ 0.05 Å.
  - Also **KILL** if a classical UCCSDT or extrapolated-DMRG ranking reaches ≤ 2 kcal/mol at ≥ 100 orbitals.
  - **SURVIVE** only if the model spread is ≤ 1.5 kcal/mol **and** the best classical solver error is ≥ 5 kcal/mol.
- **Feasibility on this machine [INFERENCE].** The converged ladder (≥ 500–600-atom QM) is not runnable on the 8-core, 15.6 GB box. A governor-runnable proxy is the embedding-sensitivity spread on a truncated 100–300-atom model, using a DFT method from a lane-specific optional `[chem]` extra (PySCF), with ≤ 2 workers and ≤ 6 GB. The full test needs external HPC or a literature value.
- **Even the success branch** gives a chemistry-level category-3 result at 10–1640 QPU-days per structural question. It is not a protein-structure advantage at scale.

---

## 6. Methodology, housekeeping and state updates (for the orchestrator)

- **H-1.** Pin one L0–L6 scale in `RESEARCH_CHARTER.md`. The T2 table and "L6 = proven separation" are both in use (see the header of this file).
- **H-2.** Add a PREREG deviation entry before any N ≥ 22 cone output is analysed. It should replace the Δ_N step rule with the T-X decision rules (C10, §2.2), and record that the R1-SIM KILL (converged by N ≤ 20) is excluded on p19.
- **H-3.** Correct the "61/64 deepest basin" wording wherever it appears (`CURRENT_STATE`, task templates, `SCIENTIFIC_MEMORY`) with C1.
- **H-4.** After user go-ahead, replace the slow `nmr_cone.py` N = 22 governor jobs with validated `fastecho.py` flip-mode jobs. It is about 18× faster and matches the governor's N = 20 run to 0.0022. Do not stop running jobs without that go-ahead.
- **H-5. State files.** `CURRENT_STATE.md` is stale: it says nothing is running, but the governor is. On the next state update:
  - add K-106 to K-116 to `KILLBOOK.md`;
  - add them, with NA-1 to NA-9, to `discovery/KILLED_DIRECTIONS.md`;
  - park R1-SIM-X, R-ROTOR, FeMoco-E4, T = 1 sub-basin sampling and R1-SIM-DQ in `OPEN_QUESTIONS.md`;
  - add to `SCIENTIFIC_MEMORY.md`: "structure-bearing computation classically easy / hard computation structure-free", the F = H + floor + X decomposition, and the DG portfolio as the mandatory classical twin for every learned-energy route (update K-102 and H-007).
- **H-6. New-mechanism filter.** Any future new-mechanism lane must first pass three gates:
  - (a) no classically efficient member of the same distribution family (tempering curve, perturb-and-MAP, matching Gibbs measure) reaches the same structural Pareto front;
  - (b) the quantum-native observable exists at physical parameters (resolution, barriers, reversal horizons);
  - (c) it beats the generalised floor T*_Q,s against the DG portfolio, not against random multistart.
- **Classical by-products worth publishing whatever the quantum verdict:**
  - DG seeding on learned distogram energies;
  - the exact echo decomposition, and classical spin dynamics for the two-point part;
  - the 18× exact echo code;
  - Layden's SK exponent ratio shrinking from 0.28 to about 0.4 against a tuned random-subset-flip proposal at n ≤ 8 (small-n; INFERENCE beyond);
  - the protein DQI encoding (girth 3, so l = 0).
- **Round-3 compute [MEASURED from lane reports].** About 255 CPU-min for the lanes plus about 110 CPU-min for the verifiers, all single-threaded, every run ≤ 2 GB, checkpointed. The hybrid relevance verifier did not report its time. Nothing was committed.
