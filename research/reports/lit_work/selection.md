# Selection: ranking of the six audited candidates (C01, C41, C14, C07, C04, C44)

Date: 2026-09-28. Role: selection lead. Inputs: the 18 audit notes `audit_C{01,04,07,14,41,44}_{novelty,classical,resources}.md` in this folder, and `pool_and_shortlist.md`.
Status: FINAL for this round. Nothing here is an experimental result. All cost figures are order-of-magnitude estimates by the auditors unless a citation is given. All novelty statements are scoped to the sources the auditors searched through 2026-09-28. WebSearch was exhausted in every audit, so searching went through the arXiv API, arXiv pages, OpenAlex, Crossref, Semantic Scholar and OSTI, with rate-limit gaps. Theses, patents and conference talks were not searched.

## 0. Bottom line

**Only one of the six candidates clears the quality bar, and it clears it only conditionally: C01, sharpened to correlated S_ee(q,w) at theta 0.25-0.5.** The brief asked for three distinct eligible directions. The audited set cannot supply them without lowering the bar, and I have not lowered it. Positions 2-6 are ranked so that the next round starts from the least-dead material, but all of them are marked `eligible = false`.

The same failure pattern appears in all six audits, and it is the same pattern as the protein project:

1. **The classical wall and the useful information sit in different places (lesson L5).** Either the regime where classical methods fail is not what current data or decisions need (C14: short-time data; C07: static opacities; C04: LTE (local thermodynamic equilibrium) binned opacity; C44: gain/no-gain), or cheap approximate classical families already match the measured observable (C41: ECBB + reduced-dimension models; C44: GW+Fan-Migdal NEGF).
2. **Cost is dominated by measurement and state preparation, not by Hamiltonian simulation (lessons L3, L4).** Every candidate has S*G of about 1e13-1e19 Toffoli per useful state point, against the program's screen of S*G <~ 1e12. The expensive parts are rare channels, linear-response shot noise, and correlated thermal (Gibbs) states with unknown mixing time.
3. **The model floor is at or above the solver spread (lesson L6).** Examples: vacancies in Ce pyrochlores; core-valence correlation outside any active space in lanthanides; phonons and Q valleys in TMDs; laser-intensity calibration in strong-field ionization; clusters and pasta in supernova matter.

This is itself a finding. For "real-frequency response or spectrum of a correlated continuum or thermal system", audited against real experimental consumers, the exponential separation is real but sits where the decision value is low. C01 is the one case where the two might overlap, and two cheap classical tests (section 2) will decide whether they do.

## 1. Ranking (best first)

| Rank | ID | Sharpened formulation (after audits) | Audit verdicts (novelty / classical / resources) | Eligible |
|---|---|---|---|---|
| 1 | C01 | Correlated thermal S_ee(q,w) of partially degenerate, partially ionized H (then CH) at r_s 2-4, theta 0.25-0.5, at XRTS wavevectors, with an exact UEG validation rung. See 2.1. | wounded / wounded / wounded | **yes, conditional** |
| 2 | C14 | Not C14 as specified. Redesign lane: long-time (t*J ~ 1e2-6e2) local S(w) of pi-flux dipolar-octupolar QSI at T ~ 0.25 J, matched to µeV backscattering data where two published classical analyses give incompatible exchange parameters (Poree et al., arXiv:2304.05452). | wounded / wounded (severe) / killed | no |
| 3 | C44 | Residual only: exact real-time dynamics of the 2D two-component Rytova-Keldysh e-h plasma at eta 64-128, r_s 1-3, reading one scalar (n(k,t) or g_eh(r,t)) as ground truth for GKBA/G1-G2 self-energies. | wounded (B, not A) / killed / wounded | no |
| 4 | C41 | Residual only: one low-order observable (triple/double ratio or sum-momentum marginal) for full-3D eta = 3-4 strong-field ionization at NIR, single intensity, as a category-3 reference calculation. | wounded / killed / wounded | no |
| 5 | C07 | Residual only: ab initio real-frequency spin-relaxation width of warm neutron-rich matter with chiral tensor forces, n ~ 0.03-0.1 fm^-3. | wounded / killed / killed | no |
| 6 | C04 | No quantum residual. The remaining gap (configuration-average energies of mid-series Ln III / actinides) is dynamic core-valence correlation outside any feasible active space, which is a classical or laboratory problem. | wounded / killed / killed | no |

## 2. Per-candidate sharpening and rationale

### 2.1 Rank 1: C01, correlated S_ee(q,w) of warm dense matter at theta 0.25-0.5 (eligible, conditional)

**Sharpened problem.**
- INPUT: species (UEG, then H, then CH); r_s in {2, 3, 4}; theta in {0.25, 0.5}; XRTS wavevector q (0.4-4 k_F); instrument function.
- COMPUTE: the correlated thermal density-density correlator, then S_ee(q,w) at 2-5 eV resolution.
- OUTPUT: S_ee(q,w) with error bars, and the resulting (rho, T, Z) posterior from the measured or synthetic spectrum.
- SCALING: electron number eta = 32 -> 256 at fixed (r_s, theta); theta downward from 1 to 0.25.
- VALIDATION: at theta >= 0.5 the Laplace transform of the quantum S must reproduce quasi-exact PIMC F(q,tau). No other candidate has an exact classical cross-check of this kind, and this one supports a clean FULL vs ABLATION comparison.
- Claim category: 3 (computational/resource advantage) against exact finite-T fermionic dynamics in the sign-problem regime. Against TDDFT the gain is only polynomial (Babbush et al. Nat Commun 2023).

**Why it survives.**
- A named classical wall exists. Moldabekov et al. (arXiv:2507.00688) study H at r_s = 2, theta = 0.5 and 0.25 "where PIMC is unavailable due to the sign problem".
- All the PIMC workarounds break down there. xi-extrapolation and Taylor-xi fail at theta = 0.5 (arXiv:2509.11317, 2308.06071). The direct sign is 3.6e-3 at N = 8 and about 1e-6 at N = 66.
- The only family left there is adiabatic-kernel LR-TDDFT, and its kernel already deviates from PIMC at q >~ 3 q_F at theta = 1.
- It uses the bare Coulomb Hamiltonian, so the model floor is low apart from thermal-state preparation.
- Real consumers exist: NIF, LCLS and EuXFEL XRTS.
- Novelty is scoped category B. The three lenses found quantum stopping power, opacity, conductivity and T = 0 EELS, but no quantum thermal S_ee(q,w) for XRTS.

**Why it is conditional (these are gates, not footnotes).**
1. **L5 information gate (K-C01a, laptop, days).** In equilibrium, F(q,tau) and S(q,w) are Laplace pairs, and the model-free ITCF (imaginary-time correlation function) method already extracts T, normalization and the Rayleigh weight. Hentschel et al. (arXiv:2408.15346) show factor-3 to factor-22 degeneracies even on noise-free data. Kill the candidate if real-frequency S narrows the (n_e, T) posterior by less than 2x over ITCF analysis, and the forward-model spread moves it by less than 0.5 sigma, at NIF-like and XFEL-like resolution.
2. **Multi-family gate (K-C01b, ~1e4 core-hours).**
   - At H, r_s = 2, theta = 0.5 and 0.25, compute S_ee(q,w) by LR-TDDFT with ALDA, PBE, hybrid/AGGA and PIMC-derived static kernels, and by Chihara/average-atom.
   - Also attempt xi/Taylor-xi PIMC at N_e = 14-32.
   - Escalate only if the spread across families, after convolution with the instrument function, exceeds experimental error at a point where xi methods verifiably fail. At present the hardness evidence is "every exact family fails, and one approximate family remains unvalidated". That is a real wall but not yet a demonstrated disagreement.
3. **Thermal-state gate.** Rubin et al.'s Mermin determinant ensemble gives a mean-field S(q). The auditors estimate an 8-16% temperature bias from relaxing the missing correlation hole, the same size as the diagnostic signal. A correlated preparation needs a bounded cost: either a microcanonical/ETH window error, or a measured Gibbs mixing time at small eta.
4. **Resource gate.** The UEG benchmark (eta = 32, theta = 0.25, 5 eV, 5%, Heisenberg-limited) costs about 4e13-9e14 Toffoli per state point. That is 1.5-3 orders above the 1e12 screen, i.e. a later-FT (fault-tolerant) machine. Practical H/CH at eta >= 128 costs 1e17-1e19, which is resource-killed. The ~1.6e3x internal inconsistency in the Rubin 2024 per-a.u. cost has to be resolved first.
5. **Scoop risk is high.** Sandia (Baczewski, Kononov, Pathak, Nelson) publicly lists WDM linear response as ongoing work (arXiv:2605.22920) and has a thermal-preparation costing paper in preparation.
   - Differentiators that remain: the UEG PIMC-validation protocol, the information-gain analysis, and the classical multi-family map.
   - The information-gain analysis and the classical map are publishable whatever the quantum outcome.

**Possible branch (same direction, not a separate slot).** Non-equilibrium, XFEL-isochorically heated two-temperature XRTS.
- PIMC and ITCF do not apply there by construction, so a multi-family wall (RT-TDDFT vs G1-G2 NEGF) is more plausible.
- The model floor is the definition of the heated initial state (lesson L6).
- It should be pre-registered only if gate 1 fails because of equilibrium Laplace equivalence rather than information limits.

### 2.2 Rank 2: C14, redesigned to µeV-resolution pi-flux QSI dynamics (not eligible)

**The spec as written fails.**
- The Gao et al. ThALES data (0.042-0.076 meV FWHM) only need t_max ~ 5-13 hbar/J_par, where classical methods are strongest. The photon is below resolution.
- Four or more classical methods already agree on pi-flux: ED+MD, Lanczos+MC, GMFT, and QMC/ED/GMFT. So the decision version flips nothing.
- At L = 3 the lowest photon mode is above kT, which biases the decisive quasielastic weight. L >= 5 is needed.
- The bottleneck is the low-T Gibbs state, which has no mixing-time bound for a U(1) QSL. It is not 3D entanglement growth.
- Vacancies at about 2% dominate the dynamics (arXiv:2609.28643), and the Gao crystal has 4% anti-site disorder.
- Total cost is 7e13-4e18 T.

**Why it is still ranked second.**
- Its redesign lane has the only pre-existing solver/model-driven parameter ambiguity in the set: the Ce2Sn2O7 backscattering spectra, J_pm = -5.2 vs -17 µeV.
- It has a genuine multi-family wall: ED is size-capped at 32, QMC has a sign problem in pi-flux, TN is weak in 3D with loops, NLCE is weak at low T.
- Its temperature (T ~ 0.25 J) makes Gibbs preparation plausibly cheap.

**Why it is not eligible.**
- The redesign lane has not been audited as a problem.
- Ce2Sn2O7 orders at about 40 mK (arXiv:2607.12274), which puts the QSI model itself in question.
- The powder local DOS discriminates weakly, samples depend on the growth route, and the vacancy floor still applies.
- Cost is about 6e15 T.
- Practical significance is limited to characterization for one neutron-scattering community.

**Next step if reopened.** Pre-register the decision-flip pre-test: do ED32, GMFT and SCEBR rank the two Ce2Sn2O7 parameter sets differently after IN16B resolution convolution? Include a vacancy arm. The Gibbs-only thermodynamic variant (sign of thermal expansion, arXiv:2608.11305) overlaps reserve candidate C17 and should be audited together with it.

### 2.3 Rank 3: C44, residual exact 2D e-h dynamics benchmark (not eligible)

**Novelty is B, not A.** Klymenko et al. (arXiv:2606.04295) already compute SBE absorption and gain on a (simulated) quantum computer, and they name the many-body extension as their route to advantage.

**The practical target is decided classically.** Dogadov et al. (arXiv:2604.06897) reproduce the experiment's roughly 100 fs exciton quench and absence of gain with GW + Fan-Migdal GKBA, at the same carrier count (~64 per valley) that C44 proposes. No multi-family disagreement was found.

**The model floor is adverse.** Phonon-driven exciton formation, K-Q valley reordering, and r0/eps_env uncertainty move n_M by about 3x. The effective-mass e-e-only Hamiltonian omits all of these.

**Spectra fail on cost.** Spectra cost 5e14-1e15 Toffoli per (density, delay) point, and an n_M(t) map 1e17-5e18.

**What survives is category 1 only.** Scalars such as n(k,t) or g_eh(r,t) at eta <= 64 cost about 3e11-3e12 Toffoli, which is the best cost profile of the six. They would serve as ground truth for self-energies; continuum NQS dynamics tops out at N = 18. The residual also carries a representation defect: fixed-particle-number first quantization cannot hold a coherent pump.

**Why third.** It ranks above C41 because it has the only residual near the S*G screen and a live experimental disagreement (gain in Chernikov 2015 vs no gain in Dogadov 2026 vs a discontinuous transition in Mohapatra 2026). That experimental disagreement is not a solver disagreement, though.

### 2.4 Rank 4: C41, residual eta = 3-4 strong-field ionization reference (not eligible)

**Every named channel is closed.**
- He (eta = 2) is solved in full 3+3-D (Zielinski et al. 2016; Zhu & Scrinzi 2020 vs COLTRIMS).
- Li triple photoionization was solved with TDCC in 2004. Its joint break-up pattern was computed in 2013, and experiments measure only totals.
- Ne/Ar NIR triple ionization is matched by two independent approximate families (3D ECBB semiclassics and the Thiede reduced-dimension quantum model) after focal-volume averaging. CTMC is itself a cheap classical sampler of the joint distribution, which removes the category-4 sampling claim.
- XFEL multiple ionization is sequential and handled by rate equations.

**Cost and model floor.** Rare channels (1e-4 to 1e-6 per shot) push the cost to about 1e16 Toffoli per marginal even with amplitude amplification. Intensity calibration (10-20%) and pseudopotential/frozen-core error sit above the solver error.

**What survives.** The exact classical wall at eta >= 4 (IR) is real. A scalar ratio costs 1e12-1e13 Toffoli, but nothing downstream needs it.

### 2.5 Rank 5: C07, residual spin-relaxation width (not eligible)

**The static corrections that drive supernova outcomes already exist classically.** The static opacity corrections that can flip marginal explosions (10-20%) come from S_A and S_V at n ~ 0.01-0.05 fm^-3. They are already computed ab initio with lattice N3LO (Ma et al., PRL 132, 232502, 2024).

**There is no sign problem where the candidate puts it.**
- Leading-order (LO) pure neutron matter is sign-free, and SU(4) LO stays sign-free at Y_p > 0. The sign problem comes from SU(4) breaking and tensor forces, which are handled perturbatively.
- With central forces, S_A(q->0, w) is a delta function. A width needs tensor or OPE forces, which cost about 5.9e23 T at L = 10 (Watson et al., Table 9).

**The lineshape has low decision leverage.** A factor 2-5 change in bremsstrahlung moves luminosities by <=5% (Bartl et al. 2016). Smeared-spectral classical twins exist (Hansen-Lupo-Tantalo).

**What survives.** A category-1 target only, costing 1e14-1e19 Toffoli per state point.

### 2.6 Rank 6: C04 (not eligible, no quantum residual)

**The flagship ions are classically exact in their valence spaces.** Nd II and U II need at most about 1.9e8 determinants even at 120 spinors. Every Ln II/III valence space is at most C(32,14) ≈ 4.7e8, so KPM/Lanczos works.

**The code spread is not solver error.** It comes from configuration completeness, calibration and configuration-average energies. Those energies come from core-valence correlation outside any 60-120-spinor active space, which an exact active-space solver cannot fix (L6 kill).

**The readout mismatches where the field is heading.** A thermal readout serves LTE line-binned opacity only. The field is moving to line-by-line NLTE transport, which needs individual lines.

**Other uncertainties swamp the opacity effect.** NLTE effects (x2-10), thermalization (20-50%) and nuclear inputs exceed the atomic-data effect.

## 3. Qualitative comparison table

Descriptors are qualitative on purpose, and no single score is implied. "Surviving form" means the sharpened formulation in section 1, not the original spec.

| Dimension | C01 WDM S_ee(q,w) | C14 pi-flux QSI (µeV redesign) | C44 2D e-h plasma (residual) | C41 multi-electron ionization (residual) | C07 hot n-rich response (residual) | C04 kilonova opacity |
|---|---|---|---|---|---|---|
| Novelty evidence (scoped) | B, solid for the exact problem, but thin: nearby Sandia work and announced intent | B; 1D/2D quantum S(q,w) and 3D Rydberg ground-state proposals only | B, bordering C (2606.04295 SBE on QC) | B; mechanism already published (Kharazi 2026, Chan 2023) | B; T=0 quantum response and nuclear EFT costs exist | B; quantum dipole spectral-function primitive exists (XAS) |
| Classical difficulty | Named wall: all exact PIMC variants fail at theta <= 0.5; one unvalidated approximate family remains | Plausible multi-family wall (ED size, QMC sign, 3D TN, NLCE) at long times; not measured | Exact dynamics beyond reach (NQS max N=18), but approximations suffice for the observable | Exact wall at eta >= 4 IR; eta = 3 borderline exascale | Sign-free lattice covers the static part; the width needs tensor forces | Valence-space FCI classically exact for all Ln II/III |
| Quantum mechanism strength | Exponential vs exact finite-T fermion dynamics; polynomial vs TDDFT; thermal preparation unsolved | Local 3D spin Hamiltonian, cheap dynamics; Gibbs preparation plausible at T ~ 0.25 J, unbounded below | Exponential vs exact; initial state is mixed, and a coherent pump is not native | Exponential in memory; Born-rule sampling, but rare channels need amplitude amplification (quadratic only) | Exponential only where the sign problem returns, which is where the cost explodes | Matched primitive aimed at a non-bottleneck |
| Practical importance | High: ICF/HED diagnostics (NIF, XFELs) | Low-moderate: materials characterization | Moderate as a methods benchmark; low as a decision | Low: fundamental AMO, no consumer for joint data | Low for this piece: the lineshape barely moves supernova observables | Moderate field, but the quantum piece has low leverage |
| Benchmarkability | Excellent: exact UEG Laplace check against PIMC F(q,tau) | Fair: sign-free 0-flux QMC+SAC rung; powder data | Fair: small-N ED/NQS rung | Good: He exact rung | Fair: unitary gas / virial rung | Good: NIST levels for La/Ce/Nd/Er |
| Scaling potential | eta 32 -> 256, theta 1 -> 0.25 | L, t_max, T | eta, density | eta 2 -> 6, wavelength | L^3, Y_p | f-occupation, core size |
| Resource feasibility | UEG rung 4e13-9e14 Toffoli (later-FT); practical H 1e17-1e19 | about 6e15 T | Scalars 3e11-3e12 (best in set); spectra 1e14-1e15 | Scalar 1e12-1e13; marginals about 1e16 | 1e14-1e19 per point, plus unknown thermal preparation | 6e13-5e18 per ion per T |
| Classical-adversary risk | Moderate-high: pseudo-fermion, Taylor-xi, backflow and learned-sign PIMC are all advancing; ITCF may make real-frequency S redundant | High: short-time data are the classical home ground; the vacancy floor | Very high: NEGF already matches experiment | Very high: ECBB and reduced-dimension models match data | Very high: lattice N3LO + HLT smearing | Very high: calibrated FAC, CI+MBPT, NN-selected CI |
| Literature saturation | Classical side dense; quantum side empty but about to be occupied | Classical side dense (GMFT/SCEBR/ED/QMC); quantum side empty | Classical NEGF saturated; quantum side just opened | Classical saturated for eta <= 3 | Classical static side saturated | Classical saturated |
| Publication potential | High in any outcome: resource estimate + UEG validation + information-gain analysis; negative results also publishable | Moderate (decision-flip pre-test is publishable classically) | Moderate (resource estimate + NEGF-vs-exact small-N benchmark) | Low-moderate | Low (the residual opportunity is a classical AFQMC table) | Low-moderate (first KPM-on-relativistic-CI benchmark; likely negative for quantum) |

## 4. Recommendation to the orchestrator

1. **Keep only C01 as a live direction, and only through its classical gates.**
   - Gate order: K-C01a (information test) first, then K-C01b (multi-family test at H r_s = 2, theta 0.5/0.25), then thermal-preparation bounding at small eta.
   - Pre-register each in `experiments/preregistered/` before running.
   - No quantum resource work beyond a UEG-rung estimate until K-C01a and K-C01b pass.
   - Because of the scoop risk, the information-gain and classical-map results should be written up as they come.
2. **Do not fill slots 2 and 3 from this set.** The brief's "exactly three" cannot be met at the stated bar from these six audits. Promoting any of C14/C44/C41 would require accepting either a category-1-only claim or an unmeasured decision flip, and lesson L1/L5 says that is how false hardness gets manufactured.
3. **Next audit round (suggested sources for slots 2-3).**
   - (a) The C14 redesign lane (Ce2Sn2O7 µeV backscattering), combined with reserve C17 (Gibbs-only thermodynamic targets: thermal Hall, thermal-expansion sign). Here the bottleneck is Gibbs preparation, which is at least the correct bottleneck.
   - (b) Other reserve candidates from `pool_and_shortlist.md` section 4, filtered up front by the cross-cutting lesson in section 0: require an observable whose decision value sits inside the classical wall, and an S*G estimate at or below ~1e13 before shortlisting.
4. **Record the cross-cutting finding.** The pattern "wall and information in disjoint regimes; cost dominated by sampling and state preparation" held for all six. It should go into `research/SCIENTIFIC_MEMORY.md` as a durable lesson when the state files are next updated.
