# Pre-registration: G1 (learned-posterior sampling), C1 (NMR hardness–identifiability), Q4 (cooperativity)

_Written 2026-09-27, during the quantum-advantage discovery sprint. **Timing disclosure.** Exploratory pilots of G1 already ran (research/results/RAW/g1_pilot, the first 256-restart census rows, and one invalid dephased NMR pilot). This pre-registration is written after those pilots but **before** any production output of the T-scan (g1_tscan), the 2048-restart census (g1_modes2k), the temperature-exchange ladder (tpt), the dephased NMR grid (nmr_gate) or the N=14 NMR pilot. Thresholds below are fixed now and are not changed after seeing production results. Deviations must be logged in §6._

## G1 — H-006 / H-007 / QM-01..04 (Program A): is sampling the learned-energy structure posterior classically hard, and does sampling transmit?

**Instrument.** The LADDER (16 leakage-screened chains × L ∈ {30,45,60,80,100,120,150}; data/instruments/ladder_manifest.json). The vendored A80/esmprior_v1 energy (bit-exact). Target π_{λ,T} ∝ exp(−(E_prior + λE_pair)/T).

**Measurements (all classical).**
- M1: 256-restart mode census, all 112 crops. 2048 restarts on 8 crops (L = 60, 100, 150).
- M2: λ-path NRPT at T ∈ {1, 2, 4, 8}, on 5 crops (L = 45–120), with HMC + pivot moves, a 1500 s production budget, and N ≈ 2.5Λ rungs.
- M3: temperature replica exchange at λ = 1, T ∈ [1, 40], 24 rungs, on 24 crops (L = 30–120).

**Kill criteria (quantum sampling line M1/M2 of the opportunity matrix is KILLED if any holds).**
- K-G1a (break-even). The measured cost of the best classical method stays below the T2/T3 break-even B*(L) at every tested L, with ≥ 3 orders of magnitude of margin at L ≤ 150. B*(L) is the break-even number of classical steps per independent sample. The measured cost is total energy+gradient evaluations per independent sample or per basin found.
- K-G1b (bypass). A classical bypass reaches the dominant posterior modes at a cost polynomial in L on the ladder, e.g. multistart decoding where the gmean p_hit decays no faster than a power law, or temperature exchange with round trips. This holds even if the λ-path NRPT shows a first-order bottleneck.
- K-G1c (irrelevance of T = 1). At the calibrated temperature T_cal the λ-path or T-path sampler makes round trips at every L. T_cal is the temperature at which posterior spread ≈ error; it is chosen on odd-indexed chains and evaluated on even ones. Hardness at T = 1 alone does not count.
- K-G1d (transmission). Over modes of the posterior, Spearman(E, RMSD) < 0.3 in median at L ≥ 100. Or the lowest-energy mode is not better than the median mode. Or the sampled soft readout does not beat the lowest-energy structure by ≥ 0.3 Å on median over crops at L ≥ 80. In any of these cases, better sampling does not buy structure accuracy.

**Survival (escalate to a category-3 resource-claim study) only if all hold.**
- Classical cost grows super-polynomially: the gmean p_hit, or the inverse round-trip rate, fits exp(cL) better than L^k by ΔBIC > 10 over L = 30–150, with k ≤ 4 rejected.
- No bypass above.
- Transmission ≥ the K-G1d thresholds.
- The extrapolated classical cost exceeds B*(L) at some L ≤ 500.

## C1 — QM-19/20/21 (Program C): does structural information in protein 1H spin dynamics live in operator components that weight-truncated classical simulation cannot reach?

**Instrument.** OpenMM hydrogens on 1UBQ (and 1PGA). Clusters of the N nearest protons around amide-H probes in six secondary-structure elements. Static oriented sample, single B0 orientation per job. Secular dipolar Hamiltonian; identical first-order Trotter circuit for all simulators (dt = 2 µs, 160 steps = 320 µs). Observables: transfer S_ab(t), plus OTOC F_ab(t) at γ = 0. Parameters: radial displacement of the 3 most distant cluster protons, and a rigid shift of the most distant proton's residue. Noise σ = 0.01 per time point. The exact reference is typicality at γ = 0 with N ≤ 14, or the deterministic Heisenberg matrix at γ > 0 with N = 10. The classical model is Heisenberg Pauli propagation truncated at weight w ∈ {2, 3, 4, 5}.

**Primary statistic.** f_hard(w) is the fraction of Fisher information carried at times t ≥ t_c(w). t_c(w) is the first recorded time with truncation bias > max(σ, 3·SE_typicality).

**Kill criteria (quantum-NMR family QM-19/20/21 is KILLED at this instrument if any holds).**
- K-C1a. The median over probes and parameters of f_hard(w = 4) < 0.10 at every γ ∈ {1000, 5000} s⁻¹.
- K-C1b. f_hard(w) at fixed w does not increase from N = 10 to N = 14 (γ = 0), i.e. no evidence that the needed weight grows with cluster size.
- K-C1c. Dephasing at γ ≥ 1000 s⁻¹ reduces the total Fisher information of the long-range parameters by > 90% relative to γ = 0 before t_c(4).

**Survival (a "hardness-and-identifiability window").** Escalate to protein-scale Pauli-propagation scaling (N = 20–30) and a novelty memo only if all hold:
- median f_hard(4) ≥ 0.30 at γ = 1000 s⁻¹;
- f_hard(w) at fixed w grows with N;
- the long-range Fisher information is non-negligible (FI_total ≥ 1 at σ = 0.01) for ≥ 1/3 of the parameters.

## Q4 — QM-04 (cooperativity): is there a first-order-like folding transition along temperature for the learned energy whose barrier grows with L?

**Measurement.** M3 above. At the C_max rung: histogram bimodality (dip ratio) and the Lee–Kosterlitz-type barrier ΔF = −ln(dip ratio). Also C_max/L versus L, and round trips.

**Kill criteria (QM-04 KILLED at this instrument if any holds).**
- K-Q4a. Energy histograms at the C_max rung are unimodal (dip ratio > 0.8 or a single peak) for ≥ 75% of crops at each L ≥ 60.
- K-Q4b. C_max/L does not increase with L (Spearman ρ(L, C_max/L) ≤ 0.2 over crops).
- K-Q4c. The extrapolated ΔF(L) stays below 2 ln R for L ≤ 300. R = C_q/C_c from T3 (≈ 10⁷–10¹⁰) gives 2 ln R ≈ 32–46.

**Survival.** Bimodality at L ≥ 60, and ΔF growing with L (Spearman ρ(L, ΔF) ≥ 0.5). This escalates to a learned-Q umbrella adversary and an L* estimate.

## 6. Deviation log

- 2026-09-27: The dephased NMR pilot (N = 12, γ = 3000) used a stochastic trajectory reference with 6 trajectories. It was found too noisy, because truncation bias did not decrease with w at early times, and it is excluded from C1. The deterministic matrix reference replaces it for γ > 0.
- 2026-09-27 (before any v2 NMR result existed): **C1 instrument upgraded to nmr_gate v2.** (i) The exact reference is now deterministic (sector-exact, validated to 1e-15 against the dense matrix incl. dephasing), so SE_typ = 0 for N <= 14. (ii) Bug fix: the v1 "rigid shift" parameter could move the probe's own residue (geminal partner), which is unphysical; v2 rigid-shifts the residue of the farthest proton whose residue differs from the probe's. The N=14 v1 pilot (1UBQ_p17, typicality nrand=3, v1 rigid parameter) is therefore excluded from C1. (iii) The classical adversary is extended from weight-truncated Pauli propagation to a panel: weight-w Pauli (w=2..5), sparse Pauli dynamics (|c| < 1e-3, 1e-4), sub-cluster exact (N-4, N-2), classical-spin dynamics. The pre-registered statistics are computed with w=4 exactly as registered; the same statistics with the best adversary (latest failure time) are reported alongside, and **claims use the stricter best-adversary version**. (iv) Interpretation of K-C1c fixed now: it fires if, summed over the long-range parameters, FI in the hard window of w=4 at gamma in {1000,5000} is < 10% of FI_total at gamma = 0 for the same probe/orientation. (v) Added (not a kill criterion): full Fisher matrix and the generalised-eigenvalue information-gain spectrum g = max_v v'F_total v / v'F_easy v, to catch the degeneracy (non-identifiability) that O'Brien et al. (PRX Quantum 3, 030345, 2022) found in the ergodic regime.

## C2 — (added 2026-09-27, after the first C1 v2 job, before any C2 output) Does the best classical adversary's cost explode with cluster size?

**Motivation.** In the first C1 v2 job (1UBQ H/ILE3, N=10, γ=1000/s), sparse Pauli dynamics at ε=1e-4 reproduced the exact transfer signal to within 0.003 over the whole 320 µs window. So f_hard(best adversary) = 0 at N=10, while the pre-registered weight-4 statistic gave f_hard = 0.99. It used a peak of 5.3×10⁴ strings (the charge-conserving operator space has C(20,10) ≈ 1.8×10⁵). The live question is how the needed classical resource scales with N.

**Measurement.** Sparse Pauli dynamics (coefficient threshold ε, no weight cap, max 4×10⁶ strings, 1 h budget per ε) through the same Trotter circuit. ε ladder 1e-2, 3e-3, 1e-3, 3e-4, 1e-4, 3e-5 (descending; the ladder stops at the first capped or budget-truncated run). Clusters: 1UBQ probes 19 and 245, orientation 0, γ ∈ {0, 1000} s⁻¹, N ∈ {8, 10, 12, 14, 16, 20}. Reference: sector-exact for N ≤ 14 (γ = 0) and N ≤ 12 (γ > 0); otherwise the smallest converged ε (two smallest ε agree to < σ/3).

**Cost metric (implementation-independent).** M*(N) = peak string count of the largest ε whose bias stays < σ = 0.01 up to t_50. t_50 is the time by which half of the exact per-parameter FI has accrued (from C1 at the same probe, N ≤ 14; for N ≥ 16, the N=14 value).

**Kill (sparse Pauli dynamics is classically efficient on this instrument, and the protein NMR forward-model advantage claim is dropped).** ln M*(N) over N = 8–20 fits a power law N^k better than exp(κN) (ΔBIC > 10), or the fitted exp(κN) extrapolates to M*(60) < 10⁹ strings. N=60 is O'Brien's ubiquitin cluster; 10⁹ strings is roughly one node-day.

**Survival.** exp(κN) is preferred and M*(60) > 10¹². Next steps would then be: the effective N of the dynamics at t_50 in the full protein (light-cone count), and a hybrid adversary (classical spins + exact core, Navez–Starkov–Fine type).

## C3 — (added 2026-09-27, after seeing ONE γ=0 C1 v2 job with OTOC FI: 1UBQ H/ILE3 N=10) Echo (OTOC) observables

**Observation that prompted C3 (exploratory, n = 1).** In that job, transfer S_ab(t) was reproduced exactly by sparse Pauli dynamics at ε = 1e-4 (f_hard = 0). The OTOC F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b]/2^N was not: every adversary failed by 80 µs. The OTOC Fisher information was 10–150× the transfer FI, with 85–97% of it after that failure time.

**Stronger adversary, added before further OTOC data.** Truncated Pauli dynamics loses operator norm, and that biases OTOCs directly. The norm-corrected estimator F_corr = Σ_kept c_P² s_P / Σ_kept c_P² (discarded strings assumed to behave like kept ones; valid at γ = 0 where the norm is conserved) is evaluated alongside the plain one. Each adversary uses whichever estimator fails later, chosen once over the whole window.

**C3 statistics.** Over all γ=0 C1 jobs (N = 10, 12, 14) with OTOC FI: f_hard^OTOC (best adversary) per parameter, the gain g^OTOC, and C2's M*(N) computed for the OTOC signal (M*_F).

**Kill (the OTOC-hardness observation is an artefact or small-N only).** Any of:
- the median f_hard^OTOC over probes and parameters < 0.3 at N = 10;
- f_hard^OTOC does not increase or stay ≥ 0.3 from N = 10 to N = 12–14;
- ln M*_F(N) is fitted better by a power law (ΔBIC > 10), or extrapolates to M*_F(60) < 10⁹.

**Survival** requires none of the kill conditions, **plus** the physical-feasibility audit (discovery report): time reversal of the secular dipolar Hamiltonian (magic-echo / MREV-type sequences, scaling −1/2) is available in solids; the OTOC SNR at the needed times is not below the per-point σ assumed here.

## R1-E and R2-T — (added 2026-09-27, after the discovery-workflow synthesis, before any R1-E/R2-T output exists)

### R1-E: does the late-window structural information of an isolated cluster survive embedding?

**Motivation (synthesis R1).** In a real protein the N-spin cluster is embedded in ~600 protons, with bath second moment √M₂,out ≫ γ. The late-window FI of an isolated cluster may be a finite-size artefact.

**Measurement (`scripts/nmr_embed.py`).**
- Core: the N_core = 10 protons nearest the probe (1UBQ probes 19 and 245, orientation 0, γ = 0).
- Parameters: the same as C1 v2 (radial moves of the 3 farthest core protons + a rigid residue shift), held fixed across embeddings.
- Observables: S_ab and F_ab (OTOC) for the core's observed spins.
- Environments:
  - (i) exact embedding in larger clusters N_env ∈ {10, 12, 14} (the nearest protons to the probe; OTOC FI only for N_env ≤ 12);
  - (ii) dephasing embedding: every core spin gets γ_i = √M₂,out,i, with M₂,out,i = Σ_j d_ij² over all protons within 12 Å outside the simulated cluster (2-point S only; a Gaussian-bath proxy).
- Late window: t ≥ t_c*, the best-adversary failure time of the isolated core (from its C1 job, per observable type).

**Kill for Program C:**
- (a) FI_late(embedded) < 10% of FI_late(isolated), summed over parameters, for the largest exact embedding (N_env = 14 for S; 12 for OTOC) or for the dephasing embedding; or
- (b) the embedded late-window FI's main direction (top generalised eigenvector) differs from the isolated one (|cos| < 0.5), i.e. the isolated information is not the protein's information.

### R2-T: transmission of posterior sampling to structure accuracy (Program A closure)

**Measurement (`scripts/g1_transmission.py`).**
- Crops: 16 ladder chains at L = 60 and L = 100.
- Converged multistart: 64 restarts, L-BFGS to |g| < 1e-3 or 2000 iterations.
- 2 Å clustering. Each mode polished; Hessian by finite differences of gradients; eigenvalues floored at 1e-6·max.
- Laplace mixture on a T-ladder {1, 2, 4, 8, 16, 32}: w_k ∝ exp(−E_k/T)·det(H_k/T)^{−½}.
- Soft structure: w-weighted average of the CA coordinates, superposed on the argmin mode. T* is chosen native-free as the smallest T with mixture ESS ≥ 3, selected on odd-indexed chains and applied to even ones (and vice versa).
- Metric: paired ΔRMSD(soft − argmin) to native (ORACLE label, evaluation only). MDE = 2.8016·SE over crops.

**Kill (K-G1d extended, closes the transmission clause of H-006):** the median gain of the soft readout at T* is < 1.0 MDE at both L.

### C1-HN (added 2026-09-27, before any output): dilute amide-proton (perdeuterated) network

The same C1 statistics apply (transfer, and OTOC for N ≤ 12), with the same kill thresholds, on the backbone amide-H-only network.
- Probes: 1PGA, 6 probes across the strands and the helix; 1UBQ, 4 sheet probes.
- N = 10 and 12; γ = 0; dt = 5 µs; 200 steps (1 ms window).

Rationale: sparser, weaker couplings lead to less ergodic dynamics. O'Brien et al. found learnability there; the question is whether classical approximations are also easy there. Output: `research/results/RAW/nmr_gate_hn/`.
- 2026-09-27 (R2-T deviation, logged after ONE crop's output was seen: 3TE4A_60, where the Laplace soft readout was 0.8–1.2 Å worse than the argmin at every T): **the Laplace weighting is invalid for the A80 energy.** The pair potentials are linearly interpolated on a 0.05 Å table, so E is piecewise smooth. Repeated L-BFGS with memory restarts plateaus at gradient norms of 2–130, never 0, and endpoint Hessians have ~40% non-positive eigenvalues. The Laplace volume term is replaced by two native-free weightings:
  - (a) w_k ∝ exp(−E_k/T) (energy-only soft-min, as in the S33 soft readout);
  - (b) w_k ∝ n_k·exp(−E_k/T), where n_k is the number of restarts in cluster k (prior basin-of-attraction weight).

  Minimisation now runs 3 rounds of 400 L-BFGS iterations with memory restarts. The kill rule is unchanged and is applied to both weightings. The v1 outputs are moved to `RAW/g1_transmission_v1_invalid/`.
- 2026-09-27 (compute-budget pruning, before these jobs produced output): the queued C2 runs at N = 16/20 with γ = 1000 are cancelled. Transfer at γ > 0 is already classically exact at N ≤ 10, and the C2/C3 decision rests on the γ = 0 series. The C1 N = 12 orientation-1 runs are also cancelled. They are listed in `research/results/RAW/master/cancel.txt`.
- 2026-09-27 (compute pruning, before output): cancelled C1 N=12 at γ ∈ {1000, 5000} (transfer at γ > 0 is classically exact at N = 10 in every job) and the 1UBQ C1-HN N=12 runs (the 1PGA HN N=12 runs are kept). Listed in `cancel.txt`.

## Adversarial outcome for R1 and corrections (2026-09-27, echo-window-attack workflow; `research/experiments/ADVERSARIAL/R1_*`)

**Deviation / correction entries** (logged on the adversarial review's findings; they change no pre-registered threshold):
- **Rigid-parameter rule changed after 92bb4eb.** The rigid shift now requires ≥ 2 cluster protons in the moved residue, not the probe's residue. The stored 1UBQ p19 N10 files from 92bb4eb carry the duplicate `rigid_res16` (= radial_HA/GLU16, deduplicated in analysis). The current rule's `rigid_res2` moves the probe's nearest proton (2.16 Å), so it is flagged short-range.
- **ε-ladder completion.** C1's adversary panel stopped at ε ≥ 1e-4. The C2 runs at ε = 3e-5 reproduce the echo within σ over the whole window for 1UBQ p19/p245, 1PGA p390 and 1PGAHN p260 at N = 10. Across 17 unique parameters, the median f_hard^OTOC falls from 0.95 to 0.00 (10 of 17 closed). Two jobs keep part of the window (1PGA p325; 1UBQHN p548).
  - **C3 kill-1 (median f_hard^OTOC < 0.3 at N = 10) is indicated under the per-point criterion.**
  - Under the estimator-level criterion (Mahalanobis bias D = 1.17–1.41 > 0.5), the window is not closed. The closure is conclusive only because exact classical simulation of N = 10 costs seconds.
- **C2/C3 scaling variable redefined.**
  - At N ≤ 10, M* is ≈ 0.46–0.50 of the parity-allowed 4^N/2 strings. Its growth is the growth of the operator space, so the pre-registered exp-vs-power-law and M*(60) criteria cannot measure hardness against exact methods.
  - At N = 12, ε = 1e-4 held 7.5–8% of 4^12/4 strings and still failed. Sparse Pauli is dominated by exact simulation by 64–115×.
  - The decisive variable is the converged σ-cone N_σ(t) of the echo (R1-SIM below). C2 runs at N ≥ 14 were stopped and cancelled. Their exact N = 14 references are kept in the `.partial` files.
- **Claim corrections.**
  - "Every classical adversary fails on the echo" is wrong. The correct statement: every sub-exponential truncation tested fails, which covers weight/ε ≥ 1e-4 Pauli, CCE to order N−3, operator-spreading/FKPP, stochastic Pauli, MPO χ ≤ 64 and classical spins/DTWA. ε = 3e-5 sparse Pauli (≈ full symmetric operator space) and exact simulation reproduce it at N = 10. The N = 10 reference is itself unconverged in cluster size (|F12 − F10| up to 0.46).
  - The echo/transfer FI ratio is 3.2–183×; stored-panel f_hard^OTOC is 0.49–1.0.
- **C3 survival clause failed (pre-registered).** It requires time reversal to be available and OTOC SNR not below σ. The physics audit puts the informative window at 4.8–25 T2, beyond measured reversal horizons T3 ≈ 4–6.7 T2 in dipolar solids (Sánchez, Chattah & Pastawski PRA 105, 052232 (2022)). Model-error nuisances (methyl rotation, 1 kHz offsets, 15% reversal mismatch) move the echo by 5–66 σ.
  - Transfer of T3/T2 to proteins is INFERENCE. Fine et al. PRE 89, 012923 (2014) and Krojanski–Suter 2004/2006 point to possible exceptions (UNVERIFIED in detail).
- **Verdict on R1 as a protein-structure advantage: KILLED (practical L0).** Grounds:
  - cost: exact classical simulation beats a fault-tolerant forward model below N_eff ≈ 30–47, at 4–6 h per quantum evaluation;
  - the failed C3 feasibility survival clause;
  - small information gain under realistic priors and attenuation (median 1.1–1.5, max ≤ 2.3 on the one job analysed with 27-coordinate priors).

## R1-SIM (added 2026-09-27, before any output): is the converged echo of a dense protein ¹H network beyond exact classical reach?

This is a physics-simulation question (category-3 candidate), not a protein-structure lead. A positive result does NOT revive R1, which is killed on feasibility and value.

- **Measurement (T-A).** Echo F_ab(t) at the instrument's observed sites b (defined on the N = 10 core, nested clusters). N ∈ {12, 14, 16, 18, 20}, 1UBQ probes 19 and 245, orientation 0, γ = 0, t = 40…320 µs every 40 µs. Statevector typicality, n_rand = 1, err = 2^{−N/2}. Script: `research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone.py`.
- **Statistic.** Δ_N(t) = max_b |F^{(N+2)}(t) − F^{(N)}(t)|, compared with σ = 0.01 plus 2·(err_N + err_{N+2}).
- **KILL R1-SIM (exact light-cone simulation suffices):** on both probes there is N ≤ 18 with Δ_{N'}(t) ≤ threshold for all N' ≥ N and all t ≤ 320 µs, i.e. converged by N ≤ 20.
- **SUPPORT the "beyond exact reach" premise:** Δ_18(t) > 3σ at some t ≥ 160 µs on both probes.
- **INCONCLUSIVE otherwise** (needs N ≥ 22).
- **Follow-up only if SUPPORT:** the hybrid adversary (exact quantum core N_c = 10–12 + classical-spin bath, Starkov–Fine type) against the N = 20 reference. KILL if its error stays < σ over 80–320 µs.
- 2026-09-27 (R1-SIM, logged before hybrid production output): the hybrid adversary (`research/experiments/ADVERSARIAL/R1SIM_hybrid/hybrid_echo.py`) is run in parallel with T-A rather than after it, to save wall time. Its decision rule is unchanged: KILL R1-SIM if the hybrid's error at the instrument sites stays < σ over 80–320 µs against the converged / largest reference. A smoke test was run before production and is disclosed here: core 10 + 2 classical spins vs exact N = 12 (p19, M = 40) gave max error 0.014, against 0.03 for the isolated core.
- 2026-09-28 (R1-SIM extension, before output): the cone-convergence ladder is replicated on 1PGA probe 390 and 1UBQ probe 487 (N = 12–20). N = 22 is added for probes 19/245. The same Δ_N statistic and thresholds apply. The runs use `scripts/nmr_cone.py`, which checkpoints each time point and is validated bit-identical to the original script.

## Round 4 (2026-09-28 ~11:25, before any output of these tests; follows ROUND3/SYNTHESIS.md and ROUND3/CRITIC.md)

- **H-2: the R1-SIM step rule is replaced.** Under a 1/N drift, Δ_N-based convergence can pass while the true finite-size error is still 10–20 σ (ROUND3 C10 / CRITIC C1). From now on, convergence claims need an explicit estimate F̂_∞ and a cross-family check. The earlier R1-SIM KILL ("converged by N ≤ 20") is recorded as excluded (p245 at 160 µs; p19 at 320 µs).
- **Compute reallocation.** The four slow `nmr_cone.py` N = 20/22 jobs serve only the late window (13–40 T2, below physical noise). They were stopped at ~3 h and their checkpoints are kept (`typicality_cone/*.ckpt.json`). The replication cones (1PGA p390, 1UBQ p487, N ≤ 18) continue.
- **T-X-early (CRITIC A-1).** For t = 40, 80, 120 µs on 1UBQ p19 and p245 at sites b ∈ {1, 7, 8, 9}:
  - compute exact H and floor at N = 20 and 22, and X_N = F_N − H_N − floor_N at N = 18, 20, 22 (fastecho, checkpointed);
  - H_∞ comes from classical spin dynamics (N_c = 80–160) plus the exact-minus-CSD offset at the largest exact N.
  - **KILL** "the converged echo inside T3 is beyond σ-level classical reach" if |X₂₂ − X₂₀| ≤ 0.005 on ≥ 6/8 series AND √(se_H² + offset² + ΔX²) ≤ σ on those series.
  - **KEEP OPEN** otherwise.
- **spinDMFT adversary (CRITIC A-2).** Implement (nl-)spinDMFT for the dense ¹H network (Gräßer–Uhrig–Ernst style) for the autocorrelation and H_∞.
  - Where an echo extension exists, apply it to F_∞ at t ≤ 120 µs.
  - **KILL** R1-SIM(-X) at those times if it agrees with the exact + CSD hybrid within σ where both are defined.
- **All-atom physics regime (CRITIC D1).** A super-quadratic quantum algorithm for sampling or dynamics of a classical force field would meet a regime that is classically hard and structure-bearing. Survey and precondition checks: Carleman/KvN/Liouville, quantum Langevin, and whatever else the literature offers. Also bound the enhanced-sampling classical twin (REST2 / metadynamics / MSM) from the literature.
  - **SUPPORT** only if a family's preconditions hold for protein force fields and T*_Q,s ≤ 1 day at a stated t_T.
- **Pro-quantum red team (CRITIC A-4).** The target is false kills among K-105, K-109, K-111 and the FeMoco WEAK residue.
  - Any kill whose load-bearing arm fails is reopened, with a revival template.
