# Round 2 prefilter: sharpening the reserves, the C14 redesign lane and the new round-2 candidates

Date: 2026-09-28. Role: round-2 prefilter lead. Status: FINAL for the prefilter. These are hypotheses for audit, not results. Cost figures are order-of-magnitude estimates unless a citation with a table is given. Novelty statements are scoped to the searches recorded in the input notes (arXiv API/listings, arXiv abs pages, Crossref, partial OpenAlex/OSTI, through 2026-09-28). No new literature search was run for this prefilter. "Not found" is not proof of absence.

Inputs read:
- `pool_and_shortlist.md` (section 4 reserves C02, C15, C17, C19, C32, C34);
- `selection.md` (C14 redesign lane; cross-cutting lesson);
- the lens notes the reserves came from: `discovery_qsim_dynamics.md` C1, `discovery_resources.md` C1, `discovery_alt_domains.md` C2 (all C02); `discovery_algorithms.md` C4, `discovery_materials.md` C2, `discovery_sciml_inference.md` C1 (C15); `discovery_materials.md` C3 (C17); `discovery_optimization.md` C1 (C19); `discovery_chemistry.md` C2, C3 (C32, C34);
- `audit_C14_{classical,resources,novelty}.md` (redesign lane, section 9 of the resources audit);
- `audit_C01_*`, `redteam_C01_*` (for C02 overlap);
- the round-2 lens notes `round2_discovery_static_inside_wall.md` (one survivor, S-M1) and `round2_discovery_short_time_dynamics_inside_wall.md` (zero survivors).

## 0. Bottom line

**One direction goes to audit: N01 (= S-M1), multi-band FCI / CDW / anomalous-Hall-crystal ground-state competition in hBN-aligned rhombohedral multilayer graphene, sharpened below into a model-adequacy and stack-prediction question.** All eight other inputs are dropped, each for a named reason tied to the round-1 cross-cutting filter.

I did not fill the other five audit slots. Every other input fails at least one of the three filter conditions *a priori*, using numbers already in the audit record, before any new audit work:

| Filter | What it requires |
|---|---|
| F1 decision inside the wall | the observable that carries the decision lives where the multi-family classical wall is, not beside it |
| F2 cost | S*G <~ 1e13 Toffoli per useful state point |
| F3 floor | model floor below the solver spread |

The drops split into three groups:
- **Wrong bottleneck, known cost.** C14 redesign lane: about 6e15 T from the round-1 resource audit. C17: Gibbs preparation plus derivative sampling at low T. C02: long-time DC limit plus shared thermal preparation. All three are dominated by Gibbs/thermal preparation and shot count, which is round-1 lesson (ii). The round-1 audits already quantified this; sharpening does not remove it (section 2).
- **Wall and information in different places.** C15 (round-1 lesson (i)) and C34 (killed as K1 by the round-2 short-time lens).
- **Floor or benchmark missing.** C32 (the static lens's chemistry trilemma plus L5 via spin-phonon relaxation) and C19 (no physical instance with established hardness and no observable that maps to a lab protocol).

**A warning that travels with N01 into audit.** The static lens's per-circuit cost assumed a block-encoding normalisation lambda of 2e3-3e4 meV. My own back-of-envelope estimate (section 3.3) is 1e5-1e6 meV for M = 81 orbitals. It is a crude Fock-space bound on the dual-gate Coulomb density-density form, with no form-factor suppression and no symmetry shift. If that holds, S*G is 1e14-1e16, not 1e12-1e13. The first gate for N01 is therefore the cheap, decisive G3 lambda computation, *before* G1/G2.

## 1. The up-front filter as applied

For each input I did three things:
1. Wrote the most defensible formulation I could find, meaning the observable, regime and consumer most likely to put the decision inside the wall.
2. Checked F1-F3 against numbers already in the audit record.
3. Checked the binding protein lessons: L1 weak baselines, L2 FULL vs ABLATION, L3 argmin, L4 simulator runtime, L5 information vs computation, L6 model floor, L7 single-family failure.

An input is dropped only if its sharpened form still fails a filter on existing evidence. If the failure depends on a number nobody has computed, the input would go to audit instead. That applies only to N01.

## 2. Per-input sharpening and verdict

### 2.1 C02 WDM DC/AC and thermal conductivity, Lorenz number, G_ei. DROPPED (not materially distinct from C01 on its decisive gates; F2)

**Most defensible form.** The e-e scattering contribution to sigma_DC, kappa and the Lorenz number of warm dense Be/H at r_s 1-3.
- Why this form: this is where a multi-family classical disagreement is documented. KS-DFT Kubo-Greenwood omits e-e lifetimes, and GW gives "a surprisingly large reduction in low-temperature DC conductivity" for Be (Robinson, Kononov, Stanek, Baczewski, Schleife, Hansen, arXiv:2605.11308, cited in `discovery_resources.md` C1). Mean-force kinetic theory with e-e (Babati et al. 2606.02881/02890) is a third family.
- Materially distinct in one respect: the omega -> 0 limit is exactly where imaginary-time correlation function (ITCF) + analytic continuation is weakest. So C02 structurally escapes C01's main L5 risk (ITCF redundancy).

**Why it is still dropped.**
1. **F1/F2 conflict, the round-1 pattern (i).** The e-e correction is large at low theta ("low-temperature" in 2605.11308). There, correlated thermal-state preparation is the unsolved, expensive step (C01 gate 3: an 8-16% temperature bias from mean-field Mermin ensembles). At theta >~ 1, where preparation is cheaper, kinetic theory and GW are closest to controlled.
2. **F2.** The DC limit needs 1e2-1e3 hbar/E_F of evolution. The lens estimates are 1e13-1e16 Toffoli per state point (`discovery_qsim_dynamics.md` C1) and G ~ 1e10-1e12 with S >= 1e2-1e3 (`discovery_resources.md` C1). The central value fails the screen.
3. **Finite-size floor (L6).** eta = 32-128 electrons may not converge sigma_DC. The KS-KG practice of k-point and extrapolation control has no cheap analogue for an exact many-body propagator.
4. **Not distinct on the gates that decide it.**
   - Same Hamiltonian as C01.
   - Same thermal-preparation gate.
   - Same competitor group: Sandia is on 2605.11308 and on the quantum-conductivity resource report OSTI doi:10.2172/3363975 (2025).
   - Novelty is C, not B.
   - If C01 dies at gate 3, C02 dies with it.

**Disposition.** Parked as a conditional **C01 branch**, not a slot. Reopen only if C01 passes gates 2-3 *and* a named (rho, T) point shows the KS-KG / GW / kinetic spread exceeding hydrocode tolerance. Hydrocode sensitivity is unverified: `discovery_qsim_dynamics.md` C1 risk (e).

### 2.2 C15 2D frustrated-magnet S(q,w) (Kitaev-Gamma near h_c; Yb delafossites). DROPPED (F1, L7 inverted, F3)

**Most defensible form.** Field-dependent S(q,w) of alpha-RuCl3-class J-K-Gamma-Gamma' models at T << J.
- The quantum ground state is prepared adiabatically from the polarized product state at h > h_c. The gap stays open there, so preparation is cheap and there is no Gibbs state.
- This is used to rank the ~38 published parameter sets (2602.10190) against INS.
- INS resolution relative to K (~5-10 meV) gives t_max*K of order 1e2, so unlike C14 the data are not purely short-time.

**Why it is dropped.**
1. **F1 (round-1 pattern (i)).** The regime where preparation is cheap is the gapped polarized phase. There the correlation length is finite, so cylinder DMRG/TN converge and nonlinear spin-wave theory is controlled (`discovery_materials.md` C2 risk statement).
   - Hardness concentrates at h ~ h_c, which is also where adiabatic preparation slows. The cheap regime and the hard regime do not overlap.
   - Kim & Mourigal (2602.10190) find that semiclassics + ED24 suffice for the continuum at higher T.
2. **F3.** The existence of ~38 published parameter sets that each fit some data is a data/model degeneracy, not a solver spread. Interlayer coupling, stacking faults and magnon-phonon coupling are unmodelled in the spin-only Hamiltonian (`discovery_algorithms.md` C4 risk L6). Removing solver error would not collapse the set. This is the same finding as the C14 classical audit (the c-theta valley).
3. **L3.** The inference loop multiplies quantum calls by 1e2-1e3 unless emulated, and emulation brings back a classical surrogate.
4. **Novelty C, crowded.** Hardware S(q,w) exists in 1D (2603.15608, 2607.07138). This candidate faces the strongest 2D classical toolbox in the pool.
5. **Delafossite branch.** For triangular Yb delafossites I recall that cylinder DMRG and semiclassics already fit the INS [recalled, UNVERIFIED: KYbSe2 analyses 2022-2024]. Even if that recollection is wrong, the F1 argument above still applies.

**Reopen condition.** A published case where cylinder DMRG, NQS and ED/TPQ disagree on a field-dependent S(q,w) feature at resolution, together with a parameter ranking that flips with it.

### 2.3 C17 low-T thermal Hall kappa_xy of extended Kitaev models via Gibbs states. DROPPED (F3/L5, F2)

**Most defensible form.** Magnetic kappa_xy/T of K-Gamma-Gamma'-h on strips wide enough for the quantization window, at T ~ 0.005-0.05|K|.
- The decision: does the half-quantized plateau survive Gamma and Gamma' in the parameter window fitted to INS?
- The quantum object is a low-T Gibbs state plus the energy-current expectation value. There is no long-time dynamics.
- XTRG D = 500 is explicitly insufficient (2507.16558).

**Why it is dropped.**
1. **F3/L5.** The measured thermal Hall signal in alpha-RuCl3 is attributed to phonons (2303.03067, 2501.11272, verified listings in `discovery_materials.md`). An exact magnetic kappa_xy therefore does not adjudicate the experiment. The decision value collapses to "what does the model say", with no consumer and no benchmark observable. That is F-bench plus L5.
2. **F2, round-1 lesson (ii) in its purest form.**
   - kappa_xy is a temperature derivative of a small edge energy current.
   - Each shot needs a fresh low-T Gibbs sample. The mixing time in a gapless or topological phase at T << flux gap is unbounded in the literature.
   - The derivative amplifies the shot count as O(1/eps^2).
   - By analogy with the C14 redesign accounting (about 1e10 T per Gibbs sample at beta*J ≈ 4, worse at lower T) and >= 1e4-1e5 shots per T-point pair, S*G is >= 1e14-1e15 [ESTIMATE].
3. **The C14/C17 merged "Gibbs-only thermodynamics" lane (thermal-expansion or Cp sign for 0- vs pi-flux QSI, 2608.11305)** was already killed by the round-2 static lens as K-S12.
   - At temperatures where Gibbs samplers provably mix fast, NLC/HTSE converge.
   - At T < J_pm, where the flux sectors differ, mixing is unbounded.
   - The 2% vacancy floor and Ce2Sn2O7 long-range order at 40 mK remain.
   - I concur: the static lens finding stands.

### 2.4 C19 protocol-dependent metastable states via quantum thermal gradient descent. DROPPED (F1 and F3 not establishable; F-bench)

**Most defensible form.** The FC/ZFC splitting and remanence of a disordered, non-stoquastic, anisotropic-exchange triangular magnet (YbMgGaO4 family), defined as the fixed point of the Chen-Huang-Preskill-Zhou thermal-gradient-descent channel (2309.16596) under a stated cooling or field protocol.
- The mechanism is genuinely beyond-quadratic: local minima are BQP-hard classically for a 2D family.
- It is quantum-native, not the argmin of a classical energy, so L3 is avoided.

**Why it is dropped.**
1. **F1 cannot be met as posed.** BQP-hardness holds for a constructed family. No physical Hamiltonian is known whose thermally stable local minima are classically hard. The lens's own first test (exact trajectories at n <= 24) is a theory question, not an audit of an advantage candidate.
2. **F3 / F-bench.**
   - The output is defined relative to an idealized quasi-local thermal channel.
   - Laboratory FC/ZFC protocols run for seconds to hours with phonon and nuclear baths.
   - The bath model and the disorder distribution are the model floor; for YbMgGaO4 the disorder is itself contested [UNVERIFIED specifics].
   - No measured observable is shown to equal the channel's fixed point.
3. Classical twins exist and have not been beaten on any named instance: kinetic MC on effective models, MPO/PEPO Lindblad evolution, and t-VMC (2609.01719 reaches annealer-scale dynamics).

**Disposition.** Recommend a small classical-only theory note as a side question, not as an advantage audit: do physically motivated disorder models yield entangled, protocol-dependent minima at n <= 24? Record it in OPEN_QUESTIONS when the state files are next updated.

### 2.5 C32 SO-coupled exchange spectra of multinuclear f-element magnets. DROPPED (F3 trilemma; L5; polynomial advantage)

**Most defensible form.** The one-step SO exchange ladder of sigma-bonded mixed-valence Ln2 (Gould 2022, doi:10.1126/science.abl5470), with far-IR/INS and EPR as the benchmark. This is the case least likely to be classically easy.

**Why it is dropped.**
1. **The static lens's chemistry trilemma applies directly** (`round2_discovery_static_inside_wall.md` section 0, item 1).
   - Active-space QPE is cheap, but the exchange depends on ligand charge-transfer and dynamic correlation outside the space: the model floor.
   - Full-basis QPE removes that floor but costs 1e13-1e16 with poor overlap.
2. **L5.** The design decision (blocking temperature, relaxation) is set by Raman/spin-phonon processes and QTM, not by the static ladder alone (static lens K-S3; Mondal et al. 2412.04362).
3. **Polynomial advantage.** The comparison is QPE vs SO-DMRG at cm^-1 precision. CASSCF-SO + fragment models reportedly reproduce the key Gould-type observables [recalled, UNVERIFIED], so no multi-family disagreement at a named point is in hand (L7).

### 2.6 C34 multinuclear L-edge XAS / 2p3d RIXS / K-beta XES. DROPPED (killed by the round-2 short-time lens, K1)

The short-time lens finding is structural.
- In Fe-S and Mn-oxo clusters, intersite correlation scales (J ~ 10-50 meV, B ~ 0.1 eV) sit below the lifetime-plus-instrument broadening (~0.3-0.8 eV), so K_intersite < 1 and the multinuclear signature is washed out (L5).
- The features above Gamma are single-ion multiplets. CV-RAS-DMRG and multiplet codes handle those.
- Where the cost passes (20-orbital RIXS: 2.0e10 Toffoli, 2602.20270), the active space is classically exact.

I concur. Reopen gate (i) from that note is unchanged: a published multi-family failure on an above-Gamma multinuclear feature that flips a redox or structural assignment.

### 2.7 C14 redesign lane: µeV local S(w) of pi-flux QSI in Ce2Sn2O7 (optionally merged with C17's Gibbs-only targets). DROPPED (F2 by about 2.5 orders; F3)

**Most defensible form.** Powder-averaged local S(w) at IN16B resolution (0.7-3.3 µeV) and T ≈ 0.17 K ≈ 0.25 J_par.
- The decision: which of the two incompatible published parameter sets (J_pm = -5.2 vs -17 µeV; J_ring differing by 17x; Poree et al. 2304.05452) is consistent with the spectrum.
- This is the only pre-existing solver-driven parameter ambiguity in round 1.
- At beta*J_par ≈ 4, Gibbs mixing is plausibly fast, and t*J_par ≈ 128-600 is past ED32 and short-time cluster control.

**Can sharpening remove the cost?**
- The round-1 resource audit (`audit_C14_resources.md` section 9) gives: C_evol 2.7e7-1.3e8 T per circuit, C_prep about 1e10 T per Gibbs sample, and about 2e5 shots per hypothesis. That totals about 6e15 T.
- The shot count is the lever:
  - QPE-type spectral sampling, one omega sample per shot, would still need about 1e3-1e4 samples to resolve a three-peak structure. That gives 1e13-1e14 T per hypothesis, with preparation dominating.
  - Pure-state thermal typicality does not remove the per-shot preparation. Energy-window filtering at beta*J ≈ 4 has exponentially small success probability in N.
- The best sharpened form is therefore >= 1e14 for two hypotheses: at least 10x over the screen, and 1e15-1e16 on the audited accounting.

**Floor (F3).**
- Ce2Sn2O7 has a first-order transition to long-range order at about 40 mK (2607.12274).
- Its diffuse scattering needs further-neighbour couplings that the NN XYZ model lacks (2601.20766).
- Growth-route dependence was reported (Poree et al.).
- The 2% vacancy threshold applies (2609.28643).
- The observable is powder-averaged, so discrimination is weak.

**Disposition.** The classical decision-flip pre-test named in `selection.md` remains worthwhile *as a classical project*: do ED32, GMFT and SCEBR rank the two sets differently after IN16B convolution, with a vacancy arm? If the classical families already disagree after that, the lane could be re-costed. It does not qualify as an advantage audit now.

### 2.8 Round-2 short-time lens. No candidates

Zero candidates were returned. I concur with the structural reason recorded there, and with its implication that the only regime where short-time cost and a many-body light cone coexist folds back into C01. Residuals R1 and R2 stay recorded there as `eligible = false`.

### 2.9 N01 (= S-M1). SELECTED FOR AUDIT (conditional; section 3)

## 3. N01: sharpened formulation for audit

### 3.1 Sharpened problem

**Name.** Multi-band ground-state competition (FCI vs CDW vs anomalous Hall crystal / extended QAH) in hBN-aligned rhombohedral N-layer graphene at fractional filling, with explicit remote bands.

**Sharpening relative to the lens spec.**
1. **Frame the decision as a model-adequacy test first, and a stack or alignment prediction second.**
   - Primary question: does the standard continuum model (SWMcC + hBN moire potential + dual-gate Coulomb), with remote bands treated explicitly rather than by a normal-ordering prescription, support a gapped FCI at nu = 2/3 (and 3/5, 2/5) *anywhere* in the parameter prior?
   - This yes/no is robust to the ~10-30% parameter floor if the answer is the same across the prior. That is the cleanest way to put the decision inside the wall while surviving F3.
   - Only if the answer is "yes, in a window" does the secondary output matter: the window in (D polarity, alignment angle, N, eps_r).
   - Experiments disagree on these windows across groups and devices. For example, FQAH at zero field in pentalayer/hBN (Lu et al., 2309.17436) contrasts with reports of FCIs only at finite field and with extended-QAH states at lower T [recalled, UNVERIFIED: 2024-2025 pentalayer/hexalayer papers from several groups; the novelty auditor must verify them].
2. **The output is eigenvalues only.**
   - Low-lying eigenvalues in each many-body momentum sector: torus degeneracy and momentum labels, gap, flux-insertion spectral flow at 3-6 flux points, and E_FCI - E_CDW/AHC.
   - N_k = 27 (then 36), n_b = 3 (then 4-5), M = N_k*n_b = 81-180 spinless orbitals.
   - Momentum-sector dimensions (recomputed here): 1.7e16 at (27, 3, N_e = 18), 3.9e20 at (27, 5), 1.8e22 at (36, 3), 2.2e30 at (48, 3). The ED edge is (18, 3) at 1.9e10.
3. **Validation rung:** exact agreement with multi-band ED at N_k <= 18, n_b = 2-3.
4. **FULL vs ABLATION (L2), made explicit.**
   - FULL: QPE/QCELS eigenvalues in the explicit multi-band space.
   - ABLATION: the strongest classical replacement. That is the best of:
     - (a) single-band ED with remote bands folded in at Hartree-Fock / self-consistent one-body level, including the "moire capacitor" remote-charge imprint of 2608.12452 as a one-body term, plus second-order (Schrieffer-Wolff / cRPA-screened) interaction renormalization;
     - (b) multi-band iDMRG on cylinders;
     - (c) band-mixing NQS (the 2503.13585 architecture, transferred);
     - (d) occupation-restricted or iterated multi-band ED (2504.20140).
   - The quantum component is load-bearing only if the answer at a named state point differs between FULL and every ABLATION arm.

### 3.2 Claim category

- **3** (computational/resource advantage) against exact multi-band ED. The Hilbert-space gap is exponential.
- **1** (usefulness / certification) against iDMRG and NQS, unless those are shown to fail or disagree at a named state point.
- Nothing stronger is claimed at prefilter.

### 3.3 Cost warning (feeds gate G3)

The lens estimate assumed lambda = 2e3-3e4 meV, giving G of about 1e7-2e10 per circuit and a central S*G of 1e12-1e13. My back-of-envelope check points the other way.

**Assumptions.** Dual-gate screened Coulomb V(q) = (e^2 / 2 eps eps0 q) tanh(q d), with eps_r = 5, d = 20 nm, a_M = 14 nm. q is summed over the N_k mesh plus G shells up to |q| <= 3.1 b. This gives Sum_q V(q)/A ≈ 440 meV.

**Result.** A density-density LCU normalisation of order Sum_q (V_q/A) * M^2/4 gives about 7e5 meV for M = 81 and about 1.3e6 meV for M = 108.
- This is an *upper-side* Fock-space estimate. Band form factors suppress large q, and particle-number-aware symmetry shifts (BLISS-type) or THC can cut lambda by 1-2 orders.
- The plausible bracket is therefore 1e4-1e6 meV.

**Consequence.**
- With eps = 0.05 meV and C_W 1e3-1e4, G is about 1e9-1e11 per circuit.
- With 36-72 eigenvalues x 1e2-1e3 repetitions (plus 3-6 flux points if the spectral flow is required), S*G is about 1e13-1e16 per state point.
- The screen may already be exceeded. G3 is cheap (one factorization of real form factors) and decisive, so it runs **first**.

### 3.4 Gate order (all classical, all cheap)

**G3 (cost).**
- Build the N_k = 27, n_b = 3 Hamiltonian from real SWMcC + hBN form factors.
- Compute lambda and C_W for DF, THC and symmetry-shifted LCUs.
- Kill if the best S*G per state point exceeds 1e13 for the decision set, meaning the eigenvalues needed for the yes/no, not the full spectral flow.

**G0 (ablation / L2).**
- At N_k <= 18, compare explicit multi-band ED against single-band ED with HF-renormalized remote-band one-body terms, including the moire-capacitor imprint, plus second-order interaction renormalization.
- Kill if the ablation reproduces the multi-band phase assignment and gap sign across the prior.
- If 2608.12452's mechanism is essentially a one-body charge imprint, this is the most likely kill route.

**G1 (floor / L6).**
- At N_k <= 18 and n_b = 2-4, check whether the CN-vs-AVE spread and the propagated parameter spread (moire potential ±30%, eps_r, gamma_i ±10%, relaxation) shrink below the method spread as n_b grows.
- Kill otherwise, unless the yes/no in 3.1(1) is invariant across the prior. In that case the floor does not affect the primary decision.

**G2 (wall / L7).**
- Run multi-band iDMRG and band-mixing NQS on the same Hamiltonian at N_k = 27.
- Kill if they agree with each other and with the G0 ablation.

**G4 (decision).**
- Name at least one unmeasured stack, alignment angle or D-polarity prediction where the families disagree.

**G5 (overlap, new).**
- Measure the overlap^2 of the embedded 1-band ED (or iDMRG) state with the true multi-band ground state at N_k = 12-18 as n_b grows.
- If overlap^2 decays exponentially with N_k*n_b (dressing by remote bands, an orthogonality-catastrophe-like effect), QCELS repetitions blow up and F2 fails. Record the decay rate.

### 3.5 Audit questions by auditor role

**Novelty auditor.**
- Search arXiv, Crossref and OpenAlex for:
  - QPE, qubitization or FT resource estimates for FQH / FCI / moire / Landau-level Hamiltonians;
  - "quantum algorithm" together with "fractional Chern" or "anomalous Hall crystal";
  - VQE/ADAPT for moire Chern bands.
- Check the 2020-2022 FQH quantum-circuit line (Laughlin state preparation, thin-torus models) and any 2025-2026 FT FQH costing.
- Verify the experimental disagreement items listed as [recalled] in 3.1(1).
- Identify the groups most likely to scoop: Bernevig/Regnault/Herzog-Arbeitman on multi-band ED; Google/PsiQuantum on Bloch-orbital QPE.

**Classical adversary.**
- Run the G0 and G2 arguments on the literature: is there already a multi-band iDMRG or NQS result for rhombohedral graphene/hBN?
- Does HF + single-band ED with the 2608.12452 correction already reproduce experiment?
- Are there AFQMC or constrained-path results for moire Chern bands?
- What does the FCI correlation length imply for the N_k actually needed? If N_k >= 50-100, cost rises 10-100x.
- Is the "moireless" limit (AHC without moire potential) already settled classically? If so, the alignment question may be moot.

**Resource auditor.**
- Compute G3 properly: lambda for DF/THC on momentum-conserving form factors; C_W; logical qubits (about 200-1000).
- Account for multi-modal QCELS for quasi-degenerate FCI triplets whose splitting may be below eps.
- Add the S multiplier for flux insertion.
- Apply the overlap decay from G5.
- Report S*G for the *decision set* separately from the full phase map, which is 10-50 parameter points on top.
- Keep simulator runtime out of all estimates (L4).

### 3.6 Main risks carried into audit (not resolved here)

- The cost bracket above spans the screen.
- The G0 ablation may close the wall cheaply.
- The parameter floor.
- The long FCI correlation lengths make the required N_k uncertain.
- For devices already built, experiments are their own oracle, so decision value lies only in unbuilt stacks or in the model-adequacy yes/no.
- The problem leans toward physics. Its practical consumer is FQAH / non-Abelian device research.

## 4. Dropped register

| ID | Sharpened form considered | Filter failed (evidence) | Reopen condition |
|---|---|---|---|
| C02 | e-e contribution to sigma_DC / kappa / Lorenz of warm dense Be/H at r_s 1-3 | F1/F2 conflict (large e-e correction only at low theta, where thermal preparation is unsolved); F2 (DC limit 1e13-1e16 T per point); finite-size L6; same gates, Hamiltonian and competitor as C01; novelty C (OSTI 10.2172/3363975) | C01 passes gates 2-3, and a named (rho, T) point shows a KS-KG/GW/kinetic spread above hydrocode tolerance |
| C15 | h > h_c adiabatic-prep S(q,w) ranking of about 38 RuCl3 parameter sets | F1 (cheap-prep gapped regime is where DMRG/NLSWT converge; hardness at h ~ h_c, where prep slows); F3 (degeneracy is data/model, not solver); L3 loop; novelty C | Published multi-family (DMRG/NQS/TPQ) disagreement on a resolved feature that flips the ranking |
| C17 | Magnetic kappa_xy/T plateau of K-Gamma-Gamma'-h at T << flux gap | L5/F3 (measured signal is phonon-dominated); F2 (Gibbs sample per shot x derivative shot noise, >= 1e14-1e15 T estimate); merged QSI-thermodynamics lane already killed as K-S12 | A material with demonstrably magnetic kappa_xy, plus a proven fast-mixing Gibbs sampler at the needed T |
| C19 | FC/ZFC splitting as a CHPZ thermal-gradient-descent fixed point for a disordered triangular magnet | F1 (no physical hard instance); F3/F-bench (idealized channel vs lab protocol; bath and disorder floor) | n <= 24 exact study finds entangled protocol-dependent minima that classical twins misassign, for a physical disorder model |
| C32 | One-step SO exchange ladder of sigma-bonded mixed-valence Ln2 | F3 (static-lens chemistry trilemma); L5 (blocking set by spin-phonon relaxation, K-S3); polynomial advantage; no multi-family disagreement found (L7) | Published CASSCF-SO / SO-DMRG / AFQMC-SOC disagreement above experimental error on a measured ladder |
| C34 | Multinuclear L-edge XAS/RIXS | L5 (K_intersite < 1); F-classical at passing cost (round-2 short-time lens K1) | Gate (i) of the short-time lens |
| C14R (+C17 merge) | IN16B local S(w) of Ce2Sn2O7 at beta*J ≈ 4, two-hypothesis decision | F2 (>= 1e14 in best sharpened form; 6e15 audited); F3 (LRO at 40 mK, further-neighbour couplings, growth dependence, vacancies, powder average) | Classical ED32/GMFT/SCEBR decision-flip pre-test shows a solver-driven flip, and a Gibbs preparation below about 1e9 T per sample is demonstrated |

## 5. Implications for the orchestrator

1. **Round-2 audit set: N01 only.**
   - Assign it the standard three audits (novelty, classical, resources).
   - Tell the resource auditor that G3 is first and that the lens lambda may be optimistic by 1-3 orders.
   - Tell the classical auditor that G0 (HF/moire-capacitor-renormalized single-band ED) is the most likely kill.
2. **The slot count stays open.**
   - Combined with round 1: at most C01 (conditional) plus N01 (conditional, pre-audit).
   - Slot 3 has no candidate. I did not promote any dropped input to fill it.
3. **The cross-cutting lesson generalizes, with a sharper form.**
   - In every dropped reserve, the *preparation* of the state that carries the decision costs more than the quantum primitive that motivated the proposal: a correlated thermal state for C02, C14R, C17 and C01; a near-critical ground state for C15.
   - The only survivor avoids that by having an eigenvalue-only output from a ground state with a classically available trial state.
   - A next discovery round should require, up front, (a) an eigenvalue-type or few-expectation-value output, (b) a certified classical trial state with an overlap that does not decay exponentially, and (c) an explicit L2 ablation that folds the "extra" degrees of freedom in perturbatively.
   - The static lens's "engineered flat-band 2D materials" opening is the one place where all three currently look possible. Other members of that family, such as tMoTe2 FQAH, were folded into N01 as secondary targets because of the parameter floor (K-S7).

## 6. Local work log

- Read the input files listed at the top. No web searches were run for this prefilter.
- Recomputed the momentum-sector Hilbert-space dimensions (python `math.comb`): (27, 2, 18) 3.6e12; (27, 3, 18) 1.7e16; (36, 3, 24) 1.8e22; (18, 3, 12) 1.9e10; (27, 5, 18) 3.9e20; (48, 3, 32) 2.2e30. These match the lens table.
- Computed the rough lambda bracket in section 3.3 (python, numpy). Assumptions as stated there. It was not saved as an artifact because it is a back-of-envelope ESTIMATE for the auditor to replace.
- Items marked [recalled, UNVERIFIED] have to be verified by the auditors before they are used.
