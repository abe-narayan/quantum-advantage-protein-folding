# Audit N01 (multi-band FCI / CDW / AHC competition in hBN-aligned rhombohedral multilayer graphene): resource and break-even analysis

Date: 2026-09-28. Role: resource / break-even analyst. Status: COMPLETE.

**Verdict: WOUNDED (not killed on cost).**
- **G3 passes at a single rung.** One (N_k = 27, n_b = 3) Hamiltonian at eps = 0.1 meV costs S*G ~ 2e12 Toffoli (bracket 6e11 to 2e13) for the decision set.
- **The prefilter's lambda warning is refuted.** For the real SWMcC+hBN form factors, lambda is 2e4 to 3.4e4 meV, not 7e5 to 1.3e6 meV. That is the upper end of the lens bracket.
- **A decision-grade point is at or just over the screen.** A decision-grade point needs a convergence ladder in N_k and n_b: (27,3), (27,4), (27,5), (36,3), (36,5). That costs about 3e13 central (1e13 to 3e14).
- **The full phase map fails the screen.** At 10 to 50 parameter points it costs 3e14 to 1.5e15.
- **If the FCI needs N_k >= 48-100, cost rises again.** At N_k ~ 48 it is about 1.4e13 per rung. At N_k ~ 100 it is about 1e14 per rung, which fails.
- **Cost is not the binding problem.** The binding risks are G0 (a classical ablation or an iterated-basis ED already answers the yes/no) and decision value. Both are outside this role but are flagged below.

Everything below is an order-of-magnitude estimate. Numbers from papers carry citations and were verified by fetch. Numbers I derived show their assumptions and come from scripts in the session scratchpad (`n01_model.py`, `n01_ed.py`, `n01_cost.py`, `lam_scan.txt`). None of those scripts is a repo file. Simulator or classical runtime is never used as quantum runtime here.

---

## 1. G3: lambda from a real continuum model (derived, this audit)

### 1.1 Model built
- **Rhombohedral N-layer graphene, valley K, spin-polarized.** Plane-wave continuum model (script `n01_model.py`).
  - Parameters: gamma0 = 2600, gamma1 = 356, gamma2 = -15, gamma3 = 293, gamma4 = 144 meV; a = 0.246 nm.
  - Displacement: linear layer potential, u_d = 40 meV (scanned over 20 to 60).
- **hBN moire potential on layer 1.** Sublattice-resolved, with Moon-Koshino-like C3 phases: V1 = 20 meV (scanned over 10 to 30), psi = -16.55 deg.
  - Moire period a_M = 11.5 nm, which corresponds to theta ~ 0.77 deg with delta = 1.7%. a_M = 14 nm was also scanned.
  - The potential's phase conventions are approximate. lambda is insensitive to them (see 1.3).
- **Interaction.** Dual-gate screened Coulomb, V(Q) = 2 pi (1440 meV nm / eps_r) tanh(Qd)/Q / A, with eps_r = 5 and d = 10 nm. Also scanned: eps_r = 4 with d = 20 nm, and eps_r = 8.
  - Q runs over the mesh differences plus G shells up to |Q| <= 3.2 b. At 4.5 b the results are unchanged.
  - Plane-wave cutoff: 3.2 b (37 G vectors x 10 components).
- **Form factors.** F_mn(k,Q) = <u_{m,k+Q}|u_{n,k}>, taken in the periodic gauge, for the n_b lowest conduction bands.
- **H_int = (1/2A) Sum_Q V_Q :rho_Q rho_{-Q}:.** The band dispersion is the one-body term.
  - This is a CN-like scheme: bare bands, with the valence sea frozen.
  - The one-body terms from the remote-valence HF in an AVE scheme were **not** included. They are bounded in 1.2 as a one-body allowance.

### 1.2 lambda definitions used
- **Sparse (raw L1).** L_sparse = (1/2) Sum_Q V_Q (Sum_{k,m,n} |F|)^2.
- **DF (momentum-pair double factorization).** For each Q, set A_Q = (R_Q + R_Q^dag)/2 and B_Q = (R_Q - R_Q^dag)/2i, where R_Q is the M x M one-body matrix of rho_Q.
  - H_int = Sum_Q (V_Q/2)(A_Q^2 + B_Q^2) + (one-body).
  - lambda_DF = Sum_Q (V_Q/2)(1/4)[(Sum|eig A|)^2 + (Sum|eig B|)^2]. This is the von Burg / Lee et al. convention.
  - The shift variant (A -> A - sN, with s the median eigenvalue, BLISS-like) plus its one-body correction 2 s eta A gains nothing, because the medians are about 0.
- **First quantization in the band basis (1Q).** lambda_1Q = [eta(eta-1)/2] * Sum_Q (V_Q/A) max_k ||F(k,Q)||_op^2.
  - Each rho_Q^(i) is a contraction, block-encoded with norm <= ||F||_op.
  - This construction is my derivation, not a published algorithm. Su et al. 2105.12767 is the plane-wave first-quantized precedent.
- **One-body allowances added in the cost script:**
  - 1Q: eta x 100 meV, covering the dispersion plus AVE-type HF terms.
  - DF: M x 25 meV.
  - Both are at most 10% of the two-body lambda.

### 1.3 Results (meV; model two-body lambda, before the one-body allowance)

| (N_k, n_b) | M | eta | Sum_Q V_Q/A | same, form-factor weighted | L_sparse | lambda_DF | lambda_1Q |
|---|---|---|---|---|---|---|---|
| (12,3) | 36 | 8 | 549 | 120 | 4.1e4 | 5.5e3 | 3.4e3 |
| (18,3) | 54 | 12 | 555 | 126 | 1.0e5 | 1.33e4 | 8.3e3 |
| (27,1) | 27 | 18 | 557 | 106 | 1.2e4 | 3.0e3 | 1.6e4 |
| (27,2) | 54 | 18 | 557 | 125 | 7.4e4 | 1.32e4 | 1.9e4 |
| **(27,3)** | **81** | **18** | **557** | **130** | **2.4e5** | **3.18e4** | **1.99e4** |
| (27,4) | 108 | 18 | 557 | 134 | 5.3e5 | 6.0e4 | 2.05e4 |
| (27,5) | 135 | 18 | 557 | 139 | 9.2e5 | 9.8e4 | 2.13e4 |
| (36,3) | 108 | 24 | 559 | 133 | 4.3e5 | 5.75e4 | 3.67e4 |
| (36,5) | 180 | 24 | 559 | 141 | 1.6e6 | 1.79e5 | 3.88e4 |
| (48,3) | 144 | 32 | 558 | 135 | 7.4e5 | 1.04e5 | 6.69e4 |

**Sensitivity at (27,3).**
- Qcut and plane-wave cutoff raised to 4.5 b: unchanged, because form factors kill large Q.
- eps_r = 4 with d = 20 nm: x1.38.
- eps_r = 8: x0.63.
- u_d from 20 to 60 meV: 0.88x to 1.06x.
- V1 from 10 to 30 meV: +-3%.
- N from 4 to 7 layers: +-2%.
- a_M = 14 nm: 0.98x.

lambda is robust to +-30% on the parameter prior. It is set by eps_r, M^2 (DF) or eta^2 (1Q), and the form-factor-weighted Coulomb sum.

**Why the prefilter bound (7e5 to 1.3e6 meV) was too high.**
- Form factors reduce Sum_Q V_Q/A from 557 to 130 meV.
- The DF 1-norm per Q is about (0.3 M)^2/2, not M^2/4, because only near-intraband, small-Q factors have eigenvalues of order 1.

**The scalings favour 1Q.** lambda_DF grows as M^2 (n_b^2 at fixed N_k). lambda_1Q is almost independent of n_b (+7% from n_b = 3 to 5) and grows as eta^2.

### 1.4 Spectrum amplification (verified citation, derived application)
- **Source.** Low, King, Berry, Han, DePrince, White, Babbush, Somma, Rubin, "Fast quantum simulation of electronic structure by spectrum amplification", arXiv:2502.15882 (PRX 15, 041016 (2025), per the arXiv page). For sum-of-squares Hamiltonians, the cost depends on sqrt(2 Lambda E_gap) instead of Lambda, where E_gap is the lowest eigenvalue of the SOS form. The paper reports 4 to 195x speedups on FeS/CO2 catalysts.
- **Why it applies here.** H_int = Sum_Q (V_Q/2)(A_Q^2 + B_Q^2) is an SOS.
- **E_SOS estimate.** About eta x (65 meV self-term + about 27 meV kinetic - about 10 meV correlation - 20 meV allowed shift), giving about 1.1e3 meV at eta = 18. This is derived, not computed by ED.
- **Result.** lambda_eff = sqrt(2 x 3.4e4 x 1.1e3) ~ 8.6e3 meV, about 4x below lambda_DF. I charge the SA walk as 2 C_W(DF).

## 2. Walk cost C_W and qubits (derived; standard QROAM/unary-iteration formulas; not compiled)

### 2.1 1Q walk at (27,3)
- Select and unselect the pair registers: 4 eta ceil(log2 M) ~ 500 Toffoli.
- QROAM lookup of the n_b x n_b blocks F(k,Q): 2.7e4 (k,Q) entries x (n_b^2 x 2 x 12 bits). Cost is 2 sqrt(data x out) ~ 4.8e3 Toffoli per particle, done for particles i and j and then uncomputed.
- Block application: ~ 1e3 Toffoli.
- **Total C_W ~ 2.1e4 Toffoli.** It grows about as n_b: 3.5e4 at (27,5), 4.6e4 at (36,5).

### 2.2 DF walk at (27,3)
- Rotation-angle QROAM over L x Xi = 1006 x 81 leaves, with output M b_rot / 2 = 650 bits: ~ 1.45e4 Toffoli.
- Givens rotations: 4 M b_rot ~ 5.2e3 Toffoli.
- **Total C_W ~ 2.0e4 Toffoli.**

### 2.3 Cross-check against the published anchor
- **Source.** Rubin, Berry, Malone, White, Khattar, DePrince, Sicolo, Kühn, Kaicher, Lee, Babbush, "Fault-tolerant quantum simulation of materials using Bloch orbitals", arXiv:2302.05531, PRX Quantum 4, 040303 (2023). Verified from the PDF text.
- **Diamond cc-pVDZ (Table III).** 52 spin-orbitals per cell, k-meshes [1,1,1] to [3,3,3], chemical accuracy. Total Toffolis span about 1e9 to 1e15 depending on the LCU. Logical qubits are about 2e3 to 4e5, and physical qubits are "M" (millions) in the tens to hundreds. The table text was garbled in extraction, so I quote the ranges only.
- **LNO (116 to 464 spin-orbitals).** About 1e12 to 2e16 Toffoli.
- **Conclusion.** Our per-step 2e4 Toffoli at M = 81 sits inside that family. Our lambda/eps ratio (~3e5) is much smaller than for chemistry at 1.6 mHa. That is why the totals are lower.

### 2.4 Logical qubits
- **1Q.** eta ceil(log2 M) = 126 system qubits at (27,3) (192 at (36,5)), plus QROAM outputs and ancillas. **Total about 500 to 1500 logical.**
- **DF.** M = 81 to 180 system qubits, plus 650 to 1440-bit QROAM outputs x the QROAM parallelism. **Total about 1.5e3 to 5e3 logical.**

### 2.5 Physical qubits
- Assumptions: surface code, p = 1e-3, per circuit G ~ 1e10 Toffoli.
- That gives d ~ 25 to 29 and about 2(d+1)^2 ~ 1.5e3 physical per logical.
- **Total about 1e6 to 3e6 physical, including factories** [order of magnitude, not sourced].
- The Rubin 2023 diamond and LNO tables are in the same range to about 10x higher.

## 3. Precision, eigenvalue count, overlap (derived; small ED pilot for scale only)

### 3.1 Energy scales (pilot ED, `n01_ed.py`, crude CN-like scheme)

**N_k = 9, N_e = 6.**
- 1-band: a quasi-triplet at 0, 0.12 and 0.50 meV, then a gap to 2.2 meV.
- 3-band: the triplet is at 0, 0.05 and 0.20 meV, the gap is 2.28 meV, and n_remote = 0.18 electrons.

**N_k = 12, N_e = 8** (a 3x4 cluster, not C3 symmetric). No clean triplet.

**Implied scales.**
- Decision-relevant gaps are about 1 to 3 meV.
- Triplet spreads and E_FCI - E_CDW near a transition are about 0.05 to 0.5 meV.
- **Target eps = 0.1 meV (bracket 0.05 to 0.2).**

These are pilot numbers in a crude scheme, used only to set eps.

### 3.2 Overlap (G5 pilot)
Overlap^2 of the embedded 1-band ground state with the multi-band ground state, in the same momentum sector:

| N_k | N_e | n_b | overlap^2 |
|---|---|---|---|
| 9 | 6 | 2 | 0.899, 0.896, 0.891 (three triplet sectors) |
| 9 | 6 | 3 | 0.876, 0.874, 0.869 |
| 12 | 8 | 2 | 0.881, 0.869, 0.872 |

**Decay rate.** About -0.016 to -0.022 per electron in ln(overlap^2).
**Extrapolation:**
- N_e = 18 (27,3): 0.67 to 0.75.
- N_e = 24 (N_k = 36): 0.6 to 0.7.
- N_e = 32 (N_k = 48): 0.5 to 0.6.

In this scheme the decay is exponential but slow, so it is not binding at accessible sizes. F2 holds for the pilot.

**Caveats.**
1. The pilot uses a CN-like scheme with frozen valence and tiny clusters.
2. The regime where remote bands collapse the FCI (Yu et al. 2407.13770) may have much stronger dressing.
3. Most important: in exactly the decision-relevant case, where band mixing *changes* the phase, the 1-band trial state has small overlap with the true ground state. Trial states from every competing phase are then needed: 1-band ED for the FCI, and HF determinants for the CDW and AHC. I charge x1.5 for this. If no trial family reaches an overlap^2 of at least 0.1, the cost bound fails.

### 3.3 Eigenvalue estimation
- **Per-circuit cost.** Standard qubitized QPE uses about pi lambda / (2 eps) walk steps, so G = (pi / 2 eps) lambda C_W.
- **Repetition factor kappa.** 3 for QPE with overlap about 0.7 and a few repeats; 10 central (robust / multi-modal); 100 for shallow single-ancilla QCELS-type total cost.
- **QCELS and MM-QCELS.** Ding & Lin, arXiv:2211.11973, PRX Quantum 4, 020331 (2023): maximal runtime delta/eps, total Õ(eps^-1), and best when the overlap is large (plain QCELS needs p0 > 0.71, which is marginal at N_e >= 18). Ding & Lin, arXiv:2303.05714, Quantum 7, 1136 (2023): the multi-modal, multi-level variant, about 100x depth reduction, with Heisenberg-limited total cost. Early-FT variants trade G for S, and S*G does not fall.
- **Decision set per Hamiltonian.** At N_k = 27 with C3, there are 11 inequivalent momentum sectors, each needing its ground energy. Add 3 in-sector second eigenvalues and flux insertion at 3 points x 4 eigenvalues. That is **26 estimates**, x1.5 for multiple trial states.
- **Full characterization.** 6 flux points, excited states and a many-body Chern-number grid add a further x3 to x5.

## 4. S*G per useful state point (script `n01_cost.py`; best of 1Q, DF and DF+SA)

eps = 0.1 meV, kappa = 10, 26 eigenvalue estimates x1.5 (29 at N_k = 36, 33 at N_k = 48):

| rung | best per-circuit G (Toffoli) | S*G per Hamiltonian |
|---|---|---|
| (18,3), ED-accessible | 1.7e9 | 5.6e11 |
| **(27,3)** | **5.4e9** (1Q 7.1e9; DF 1.1e10) | **2.1e12** (kappa 3: 6.4e11; kappa 100: 2.1e13) |
| (27,4) | 9.7e9 | 3.8e12 |
| (27,5) | 1.26e10 | 4.9e12 |
| (36,3) | 1.24e10 | 5.4e12 |
| (36,5) | 2.95e10 | 1.3e13 |
| (48,3) | 2.84e10 | 1.4e13 |

**Effect of eps.**
- eps = 0.05 meV doubles everything: (27,3) becomes 4.2e12.
- eps = 0.2 meV halves it: (27,3) becomes 1.1e12.

**Aggregates.**
- **Decision-grade point** (convergence ladder (27,3), (27,4), (27,5), (36,3), (36,5)): about **2.9e13** at eps = 0.1. Adding (48,3) gives about 4.3e13. The bracket is about 1e13 (eps 0.2, kappa 3) to 3e14 (eps 0.05, kappa 100).
- **Full phase map** (D polarity x alignment x N x eps_r, 10 to 50 points): **3e14 to 1.5e15**.
- **If N_k ~ 100 is needed** (long FCI correlation length): lambda_1Q grows about (67/18)^2 ~ 14x, sectors about 3x, and C_W about 1.5x. That is about 6e13 per rung, which **fails**.

**Against the screen (S*G <~ 1e12-1e13).**
- A single rung passes, at 0.2 to 2x the upper screen.
- The decision-grade ladder sits at 1 to 3x the upper screen (central). This is at the edge, not clearly below it.
- The full map fails.

**Where the cost goes.** Unlike round 1 (C01, C14 and others), no Gibbs state is prepared and there is no linear-response shot noise. The trial states are:
- 1-band ED vectors at (27,1), of dimension 1.7e5 per sector;
- HF determinants.

A sparse superposition of up to about 1e5 determinants costs about 1e5 to 1e7 Toffoli, which is negligible. The cost is dominated by the number of eigenvalues x (lambda/eps) x C_W. The eigenvalue count (26 to 40 per Hamiltonian) and the convergence ladder (x10 to 15) are the multipliers, not the per-circuit cost.

## 5. Wall-clock (physical, not simulator)
- **Toffoli rate.** From Babbush, McClean, Newman, Gidney, Boixo, Neven, arXiv:2011.04149 (verified in audit_C01_resources.md, sec. 1.2): 170 us per Toffoli per factory at a 1 us cycle, about 6e3 Toffoli/s.
- **One factory:** a single (27,3) circuit (5e9 Toffoli) takes about 10 days, and one Hamiltonian (2e12) about 11 years.
- **About 1e6 Toffoli/s (~170 factories, or parallel QPUs):** a circuit takes about 1.5 h, a Hamiltonian about 23 days, and a decision-grade ladder (3e13) about 1 year.
- **Parallelism.** Sectors and flux points are independent, so wall-clock divides by the number of QPUs. Machine-years do not.

## 6. Break-even against classical scaling

### 6.1 Exact multi-band ED (Lanczos)
Sector dimensions (computed) and the memory for one complex vector:

| (N_k, n_b) | sector dimension | memory per vector |
|---|---|---|
| (18,3) | 1.9e10 | 0.3 TB |
| (21,3) | 1.8e12 | 28 TB |
| (24,3) | 1.7e14 | — |
| (27,2) | 3.6e12 | — |
| (27,3) | 1.7e16 | 2.7e17 B |
| (36,3) | 1.8e22 | — |

- **Where ED stops.** The ED wall is between (18,3) and (21,3). At (18,3), ED on a cluster (hours to days) beats the quantum cost (about 5.6e11 Toffoli, weeks at 1e6/s).
- **Crossover against ED.** The quantum route is the only exact route at N_k >= 21 with n_b = 3, or at N_k = 27 with n_b >= 2. The cost ratio is exponential (ED ~ C(M, eta)) against polynomial (quantum ~ eta^2 C_W N_k per sector). **Claim category 3 against exact ED holds at (27,3)** in the narrow sense.

### 6.2 Polynomial classical families
These are iDMRG, band-mixing NQS, and iterated or occupation-restricted multi-band ED.
- There is no complexity-theoretic break-even. The quantum advantage is category 1 (certification) unless these families disagree or fail at a named (N_k, n_b, parameter) point. That is gate G2 and is not established.
- **Verified citation correction.** Wang & Zaletel arXiv:2507.07921 ("Chiral superconductivity near a fractional Chern insulator") is DMRG on a **lowest-Landau-level + periodic-potential toy model**. It is not iDMRG on the rhombohedral graphene / hBN continuum model. I found no multi-band iDMRG for RMG/hBN in the searches below.
- **Most important for break-even.** Li, Bernevig, Regnault, arXiv:2504.20140, PRB 112, 075130 (2025), use an iteration that optimizes the single-particle basis so that particles sit mainly in the lowest band. That reduces the effective n_b and makes the problem nearly ED-accessible (the (27,1) sector is 1.7e5). Where this converges, the quantum task collapses to the ablation. That is the G0 route.

### 6.3 Status of the primary yes/no in the literature (verified abstracts)
The primary decision is already being produced classically at accessible sizes, with conflicting outcomes:
- Yu, Herzog-Arbeitman, Kwan, Regnault, Bernevig, arXiv:2407.13770, PRB 112, 075110 (2025). The 1-band FCIs are destroyed by band mixing in the CN scheme. At nu = 2/3 the result "do[es] not converge".
- Li, Bernevig, Regnault, 2504.20140. "The FCI gap remains absent after convergence when the mixing with higher bands is considered."
- Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, arXiv:2608.12452 (submitted 2026-08-12). The "moire capacitor effect" (valence charge imprinted electrostatically) plus inter-band fluctuations. Multi-band ED "confirm[s]" an FCI at nu = 2/3.

A quantum machine adds convergence in N_k >= 27 at n_b >= 3. Whether that is decision-relevant depends on G0 and G2, which are not resource questions.

### 6.4 NISQ plausibility
None.
- The per-circuit depth is 1e9 to 1e10 Toffoli.
- The required relative precision is eps/lambda ~ 5e-6.
- VQE/VQD for FQH manifolds (Expósito et al., arXiv:2607.11380, 2026-07-13, V1-pseudopotential Laughlin at small size) is a feasibility demonstration, not a route to 0.1 meV on 81 to 180 orbitals.

### 6.5 Fault tolerance
Required: about 1e6 to 3e6 physical qubits, and a Toffoli rate of at least 1e5 to 1e6/s for the decision-grade point to finish within a year.

## 7. Answers to the ALSO items (resource view only)
1. **N_k required.** If the FCI correlation length needs N_k >= 48, the cost is about 1.4e13 per rung, at the screen. At N_k ~ 100 it is about 6e13 per rung, which fails. 2407.13770's "correlation length [not] small enough to be converged in accessible ED" is the main cost risk. Pre-test: the classical 1-band ED at N_k = 27 to 48 (dimension up to about 5e10) gives the 1-band correlation length for free.
2. **Moireless AHC limit.** Not checked by this role. It affects decision value, not cost.
3. **Decision value for built devices.** Not a resource question. Note that the full map (3e14 to 1.5e15) fails the screen. The cost only works for the narrow yes/no at a handful of points.
4. **Novelty (resource side).** None of the queries below found a fault-tolerant or QPE resource estimate for FQH, Landau-level, FCI or moire many-body Hamiltonians. Quantum work found: 2510.09999 (random-state DOS/LDOS for twisted bilayer graphene; single-particle), 2607.11380 (VQE/VQD for Laughlin), 2606.16548 and 2608.05140 (FQH state preparation on hardware), 2005.02399 (Rahmani et al., Laughlin state circuit, 2020), and 2309.04527 (Moore-Read thin-cylinder circuit). Scoped to the searches listed. **Category B/C holds on this evidence.**
5. **Scoop watch.** Rubin et al. 2302.05531 already supplies the k-point DF/THC machinery, and 2502.15882 supplies spectrum amplification (same Google group). A Bloch-orbital QPE costing of a moire continuum model is a short step for them.

## 8. Gate verdicts from this role
- **G3: PASS at a single rung** (2e12 central for (27,3), eps = 0.1 meV).
- **G3: MARGINAL FAIL for a converged decision point** (about 3e13 central, 1 to 3x over).
- **G3: FAIL for the full map.** Not a kill on its own.
- **G5 (pilot): PASS within caveats.** Overlap^2 decays by about 0.02 per electron in the CN-like pilot. It is not binding. The decision case (a phase change under band mixing) needs competing-phase trial states.
- **Recommendation.**
  - Carry N01 as WOUNDED.
  - Run G0 next: iterated-basis (2504.20140) or HF/capacitor-renormalized 1-band ED against multi-band ED at N_k <= 18. If it matches, N01 dies on the ablation, not on cost.
  - Record that the resource case rests on eps ~ 0.1 meV, N_k <= 36 to 48, and the 1Q or SA block encodings. None of those three encodings is compiled; C_W is a formula estimate with about 2x uncertainty.

## 9. Query log (2026-09-28)
- WebFetch arxiv.org/abs: 2302.05531, 2407.13770, 2608.12452, 2502.15882, 2211.11973, 2303.05714, 2504.20140, 2507.07921, 2607.11380, 2510.09999, 2309.17436, 2503.13585.
- WebFetch arxiv.org/pdf/2302.05531 → pdftotext (Table III and the LNO table were read, but the text was garbled; ranges only).
- arXiv API:
  - `abs:"fractional Chern" AND abs:quantum AND (phase estimation | fault-tolerant | qubitization | resource estimate)` → 3 hits, none relevant.
  - `(FQH | Landau level | moire) AND (phase estimation | qubitization | Toffoli | T count)` → 25 hits, no FT costing.
  - `(twisted bilayer | rhombohedral | moire | Chern band) AND (fault-tolerant | quantum algorithm | resource estimation | variational quantum)` → 6 hits; only 2510.09999 is relevant (single-particle).
  - `abs:"quantum phase estimation" AND (flat band | Chern | momentum space)` → 2 hits, irrelevant.
- Crossref `quantum phase estimation fractional Chern insulator moire resource estimate` → 20 hits, none a quantum-algorithm study.
- OpenAlex → HTTP 429 (Retry-After 75294 s). Not used.

## 10. Local computations (scratchpad; not repo files)
- `n01_model.py`: continuum model, form factors, and lambda (sparse, DF, DF-shift, 1Q). Runs in 4 s at (27,3).
- `lam_scan.txt`: the size and sensitivity scan in 1.3.
- `n01_ed.py`: momentum-sector multi-band ED (bitstring, vectorized numpy). N_k = 9 with n_b = 1 to 3 took 210 s for n_b = 3 (sector dimension 3.3e4). N_k = 12 with n_b = 1 to 2 had sector dimension 6.1e4. Hermiticity was checked to 1e-14.
- `n01_cost.py`: ED dimensions, C_W formulas, and the S*G table in section 4.
