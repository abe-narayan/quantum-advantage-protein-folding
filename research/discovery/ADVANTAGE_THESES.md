# Advantage theses: the "one thing that matters" test for each residual window

_Discovery sprint, 2026-09-27. Each thesis states, without hedging, what the computation is WITHOUT QUANTUM, WITH QUANTUM, and WHY CLASSICAL CANNOT MATCH (with what must be shown for that clause to hold), followed by the decisive classical-first experiment, nulls, kill and survival rules. R1 and R2 tests are pre-registered in `research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md` (C1, C2, C3, R1-E, R2-T). Their outcomes are recorded in `SURVIVING_DIRECTIONS.md` and the discovery report._

### R1. NMR echo/OTOC forward-model window (Program C)

**The one thing that matters.**
- **WITHOUT QUANTUM:** Geometry is inverted from time-resolved ¹H transfer/echo data. The forward model is the best classical one (sparse Pauli dynamics at threshold ε, a hybrid exact core embedded in classical spins, spinDMFT). The alternative is a pairwise, classically interpretable experiment (¹H–¹⁹F REDOR, PRE) at equal spectrometer time.
- **WITH QUANTUM:** An exact forward model of the echo/OTOC signal at N ≥ 30–60 spins. It recovers the Fisher information carried after the classical adversary's failure time t_c.
- **WHY CLASSICAL CANNOT MATCH** requires three things together, and none is yet shown:
  1. The adversary's resource M*(N) grows exponentially with N. This is untested beyond N=8, where M* ≈ 1.6×10⁴ strings, close to saturating the operator space.
  2. The late-window OTOC information survives embedding in the ~600-proton bath and physical echo irreversibility. The bath estimate (√M₂,out ≈ 5×10⁴ rad/s, far above γ = 10³ s⁻¹) argues against this.
  3. The parameters it identifies cannot be identified by classically interpretable experiments per spectrometer-hour. The ¹⁹F/REDOR route (~15 Å at < 10% in < 3 days) argues against this.

**Current evidence (production, n = 1 probe, 2 orientations, exploratory under C3).**
- At N=10, γ=0, OTOC f_hard against the best adversary is 0.85–0.97 (orientation 0) and 0.98–1.00 (orientation 1), with information gains g = 6.7–5,016.
- For transfer, f_hard = 0 at γ = 0, 1000 and 5000 s⁻¹.
- At N=10, exact simulation costs seconds, so this "hardness" is hardness only relative to approximations.

**Decisive classical-first experiment (≤ 1 day, 6 cores, under the governor; log additions in the C2/C3 deviation log before any new output).**
1. **Scaling (C2/C3 as pre-registered).**
   - Probes: 1UBQ 19 and 245, plus one 1PGA probe.
   - N: 8, 10, 12, 14 with the sector-exact reference at γ=0; N ≤ 12 at γ=1000; N = 16–20 against the smallest converged ε.
   - The OTOC is the primary observable, with the norm-corrected estimator.
   - Record M*_F(N), f_hard^OTOC(best adversary) and g.
2. **Embedding adversary.** Take the N=14 exact core and add the next 30 protons, either as a classical-spin mean-field bath or as per-spin dephasing γ_i = √M₂,out,i. Record the late-window FI surviving relative to the isolated cluster.
3. **Hybrid adversary.** Implement the Navez–Starkov–Fine exact-core-plus-classical-spins model, which NM-1 listed as open.
4. **Dilute regime.** Build a perdeuterated, amide-only 1PGA HN network at N = 12–20, where cross-strand HN–HN couplings encode sheet topology.

**Nulls.**
- Transfer S_ab, already f_hard = 0.
- Coordinate-shuffled clusters at the same N and density: the FI floor that comes from finite-size recurrence alone.
- Isolated vs embedded, at identical N.

**Kill (close Program C) if any of these holds.**
- ln M*_F(N) fits a power law better than exp(κN) by ΔBIC > 10, or the fit extrapolates to M*_F(60) < 10⁹ strings.
- Embedded late-window FI is < 10% of the isolated value.
- Median f_hard^OTOC < 0.3 at N = 12–14.
- g < 2 against the embedded/hybrid adversary.

**Survival (escalate to a protein-scale study and NM-4)** requires all of: exponential growth with M*_F(60) > 10¹²; embedded f_hard ≥ 0.3; FI_total ≥ 1 at σ = 0.01 for ≥ 1/3 of parameters.

**Compute.** N=14 sector-exact takes about 10–15 min per core-job. Sparse Pauli runs are capped at 4×10⁶ strings and 1 h per ε. Exact dephased references at N ≥ 16 are infeasible within 6 GB free RAM (about 9.6 GB per vector), so none are planned.

**Theory and resource work.**
1. Write the consumption no-go as a lemma. Var(log L̂) ≈ K s²/(σ² M), so a likelihood inside MCMC costs ≥ K^{3/2}/σ coherent circuits. The only viable use is an offline emulator.
2. Compute the Cramér–Rao bound per spectrometer-hour for the OTOC vs ¹H–¹⁹F REDOR on the same parameter. This is the quantum-necessity ablation at the experiment level.
3. Correct C3-a: damping should count X/Y factors, not Pauli weight. Add Loschmidt-echo irreversibility (T₃ ~ T₂, Sánchez et al. 2020).
4. In BREAK_EVEN §4, replace the promotion threshold of 10⁷ strings with the break-even S*(60) ≈ 3×10⁹–5×10¹¹.

### R2. Learned-posterior hardness and transmission (Program A)

**The one thing that matters.**
- **WITHOUT QUANTUM:** Preconditioned NRPT/HMC, DG-seeded converged multistart, basin decomposition (per-basin HMC with BAR/MBAR masses) and adaptive SMC, all at a native-free calibrated temperature T_cal.
- **WITH QUANTUM:** A QSA/Szegedy/QRELD walk on the same λ-path, with a √δ gain per stage.
- **WHY CLASSICAL CANNOT MATCH:** Only if a readout-visible barrier of ≥ 23 nats at T_cal survives preconditioning and basin decomposition, separates structurally distinct basins (> 2 Å, each ≥ 5% of the mass), and the sampled soft readout beats the argmin by ≥ 1.0 MDE. Even then, T*_Q ≥ 0.26–20 yr/sample, so a positive result is only a conditional theoretical statement.

**Decisive classical-first experiment (≤ 1 day on 7 cores).** Transmission is tested first, because if sampling does not improve structure, mixing does not matter for the endpoint.
1. **Transmission (4–8 h).**
   - Targets: long40 (45 targets) plus ladder crops at L = 60/80/100.
   - Polish census modes to positive-definite Hessians (|g| < 10⁻⁴).
   - Form the Laplace/darting mixture w_k ∝ e^{−E_k/T} det(H_k/T)^{−½} on a T-ladder {1, 2, 4, 8, 16, 32, 64}. Choose T* by a pre-registered native-free rule: ESS or posterior-predictive coverage on held-out prots/, selected on odd chains and evaluated on even ones as in K-G1c.
   - Compare the aligned, projected soft structure to the polished argmin by paired MDE.
   - **Kill (K-G1d extended):** < 1.0 MDE gain at T*.
2. **Diagnosis (6–10 h).**
   - Step 0: check the round-trip counter on a planted 2-Gaussian with known Λ; it must be within 30% of the ELE rate.
   - Rerun NRPT on 5O37A_45, 3GAHA_60 and 5O37A_100 at T=1 and at T_cal, with 4 seeds and 2×10⁶ evaluations. Use a dense or Hessian mass matrix, a soft-core steric ramp inside the λ-path, and crankshaft/concerted-rotation moves.
   - Record round trips vs ELE, τ_int, top-rung step size, and the NEB barrier between the top-2 modes.
   - **Kill:** round-trip rate ≥ 25% of ELE or τ_int drops ≥ 10×, and extrapolated C_class(150) ≤ 10⁹.
3. **Dequantisation replication (2–3 h).**
   - On the 8 pre-registered 2048-restart crops, compare the deterministic expected-distance DG pair plus 64 distogram-draw DG seeds with converged L-BFGS.
   - Planted-well controls: (A) a register-shifted β-pairing well from 20–40 sharpened bins, and (B) a distributed well over ~400 pairs at ≤ 0.3 nats each.
   - **Kill:** every basin with ≥ 1% mass, including A and B, is hit with p ≥ 10⁻³ by the classical portfolio.

**Nulls.** Random-prior twin (DNR-06); planted wells of known mass; native RMSD used only as an ORACLE label for evaluation.

**Survival** requires the pre-registered G1 survival criteria plus all four NEB/transmission conditions above.

**Theory and resource work.**
1. Freeze T3 final G(L) and BREAK_EVEN §1.
2. Fold QM-03's corrected gates into T2. The readout gate must include the precision quadratic, i.e. r > (σ/ε)/√δ. The transport gate must give the quantum side the same flow. δ_f/δ should be replaced by the π-weighted slow-mode amplitude Σ w_k |E_k f − E f|.
3. Add QM-05's L-independent per-pair R, with a compiled (numba) t_pair measurement. This raises B*.
4. Record p_sub ≤ e^{−KL(π_λ‖π₀)} as a general no-go for prior-initialised quantum search.

### R3. New information: restraint value, restraint posteriors, fold-switch information (Program E)

**The one thing that matters.**
- **WITHOUT QUANTUM:** The esmprior/A80 decoder plus classical per-target restraints (NOE, PRE, REDOR, crosslinks, DEER). Ambiguous assignments are handled by an exact mixture (collapsed) likelihood, sampled with data-weight NRPT or SMC. Ensembles are fitted by BME.
- **WITH QUANTUM:** No mechanism was found that is not QM-01 (a walk on the collapsed posterior) or QM-24 (sensing).
- **WHY CLASSICAL CANNOT MATCH:** It can. Assignment registers sum out exactly, and restraints are pairwise closed forms. The purpose of this direction is to measure where information moves the endpoint (H-002). That is the only regime in which any future computational stage could matter.

**Decisive classical-first experiment (≤ 1 day, 4 cores).**
1. **Restraint-value curve (mid30 + long40).**
   - K ∈ {5, 10, 20, 50} synthetic distance restraints with σ ∈ {0.1, 0.3, 1, 2} Å, as flat-bottom terms in the A80 decoder, 32 restarts.
   - These are ORACLE-derived SIM-DATA. Label them as such, never mix them with DEP results, and never use the test split for selection.
   - **Null:** same count, random pairs, shuffled distances (information-free).
   - **Metric:** ΔRMSD in MDE units vs (K, σ).
   - **Kill for any precision-type quantum sensor or forward model:** RMSD(σ=1 Å) − RMSD(σ=0.1 Å) < 1 MDE.
2. **Ambiguous restraints.**
   - 6 long40 crops; ρ ∈ {0.5, 1} restraints/residue; K ∈ {2, 4} candidates; 15% outliers.
   - Arms: collapsed-likelihood NRPT; joint PT + Gibbs assignment flips; 64-start mixture anneal with mode-leaping; SMC over data weight.
   - **Kill (expected):** all arms agree on mode weights within 10% at ≤ 10⁸ evaluations wherever the fold is identifiable (posterior spread < 2 Å), or hard cells coincide with non-identifying data.
3. **Fold-switch information test (minutes).**
   - GA98/GB98, GA95/GB95, RfaH-CTD, each leakage-screened against the ≤ 72-aa esmprior training crops.
   - Measure fold-B bin mass at discriminating pairs (ORACLE-defined, analysis only) and the LLR shift between switch pairs.
   - **Kill:** median mass < 5%, or no sign flip of the LLR between GA/GB variants.

**Theory work.**
1. Write the "collapse lemma" for restraint posteriors (Liu, Wong & Kong 1994; Liu 1994).
2. Close the bibliography gap: IMP, ISD (Rieping/Habeck/Nilges 2005), ARIA, CYANA/CANDID, ARTINA, Viswanath exhaustiveness and AlphaLink are absent from the 448-paper map.

### R4. Metal-cofactor active-site chemistry (Program H)

**The one thing that matters.**
- **WITHOUT QUANTUM:** DMRG/UCCSDTQ composite with extrapolation, QM/MM, Ryde-style quantum refinement, BS-DFT, and EPR/ENDOR/Mössbauer discrimination.
- **WITH QUANTUM:** FT QPE (THC or spectrum amplification) energies at ≤ 1 kcal/mol for each candidate protonation/spin state in 76–150-orbital active spaces.
- **WHY CLASSICAL CANNOT MATCH:** Only if (i) solver error rather than model error (active space, basis, environment) binds the structural assignment, (ii) the required active space exceeds DMRG/CC reach, and (iii) the assignment moves atoms outside the first coordination shell by > 0.1 Å. Zhai et al. 2026 reports FeMoco as a ranking problem over many largely single-configuration states, already at chemical accuracy classically. The best per-state quantum gain is about 2.7×. The full structural workload (candidates × spin isomers × precision) puts quantum 10²–10⁵× past its per-state crossover.

**Decisive classical-first experiment (hours).**
- PySCF + block2 DMRG-CASCI on [2Fe-2S](SCH₃)₄ at (30e,20o), M ≤ 2000, and on [4Fe-4S] at (54e,36o), M ≤ 750–1000 within the 6 GB of free RAM.
- Two protonation variants at BS-DFT geometries; extrapolate in discarded weight.
- **Nulls:** a solver-noise floor (same structure, repeated sweeps) and a model-change floor (a larger basis or NEVPT2 correction).
- **Kill for this program** if either holds: the extrapolated gap uncertainty is ≤ 0.1× both the gap and the model-change shift; or heavy-atom displacement between variants is < 0.05–0.1 Å outside the first shell.
- This adds a chemistry extra dependency; install it as an optional `chem` extra, per CLAUDE.md.

**Theory.** None new. Record the lane as outside the endpoint. Reopen only if the program adopts an active-site chemistry endpoint.

### R5. Super-quadratic theory residues (Program G)

**The one thing that matters.**
- **WITHOUT QUANTUM:** Kikuchi/SoS/AMP spectral methods for planted structure; BCGL chains, PIMC or SQA for explicit stoquastic paths; exact homology at feasible orders.
- **WITH QUANTUM:** Guided sparse-Hamiltonian phase estimation (n^{l/4}); stoquastic adiabatic paths with GHV-type gaps; quantum Mayer homology.
- **WHY CLASSICAL CANNOT MATCH:** Only in a planted k ≥ 3 regime inside a statistical–computational gap, with near-iid noise and a smooth level-l tradeoff, or on an explicit path whose intermediate ground-state amplitude ratios are not classically computable. None of the protein data examined supplies this: restraints have r = 1, distograms are dense with k = 2, cryo-EM has K ≪ √d, and the learned tables are white-box.

**Decisive work.**
1. **Mayer information gate (CPU, 2–4 h).**
   - Exact Mayer Betti numbers (N = 3, 5) at feasible orders (k ≤ 6; heavy-atom r ≤ 8 Å; any r for CA) on A80 census decoys of long40.
   - Task: held-out near-native vs far decoys, split by target, with native RMSD as ORACLE label only.
   - Compare against classical k ≤ 2 persistent homology plus the A80 energy. **Null:** shuffled features.
   - **Kill:** AUC gain ≤ 0.01 or its 95% CI includes 0.
2. **3-body coevolution (paper, ≤ 1 day).**
   - Lowest-correlated-degree (D_min) audit for order-3 coevolution with n = 21L and N_eff = 10²–10⁴ under phylogenetic correlation.
   - **Null:** an MSA simulated without 3-body terms.
   - Kill if D_min ≤ 2 or the window between polynomial-time and information-theoretic sample sizes is below ~10×. The expected window is ~n^{½}, before correlation losses.
3. **Explicit-naming lemma (paper).** Attempt a BCGL-based proof for column-symmetric walks. Record the LWWZ derivative-query question as open.

**Theory.** T1 addendum: B5 now has a provable value-query separation (LWWZ 2504.14841), and δ = 1/5 is attributed to GHV. T5 addendum: add LWWZ, Hamoudi et al. 2602.23183 and Nghiem et al. 2609.28058 to the route list.

---
