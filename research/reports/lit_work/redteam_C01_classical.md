# Red team C01 (Hostile Reviewer #1: classical/technical)

Date: 2026-09-28. Status: FINAL.

**Candidate.** Correlated thermal S_ee(q,w) of partially degenerate warm dense matter, in three rungs (UEG, then H, then CH), at r_s 2-4, theta 0.25-0.5 and XRTS q ~ 0.4-4 k_F. Claim category 3, against exact finite-T fermion dynamics.

**Verdict: NOT FATAL OVERALL, BUT TWO SUB-CLAIMS ARE DEAD.**
- The UEG rung has no classical wall at the stated parameters. It can serve only as a validation rung and can never be an advantage rung.
- The CH rung is outside the model and resource envelope.

What survives is one conditional claim: warm dense H at r_s ~ 2, theta 0.25-0.5, and only if the classical method families disagree by more than experimental error at a state point that some experiment measures. The literature gives no evidence that they do. The one direct test, corrected LR-TDDFT against PIMC at theta = 1, found "striking agreement".

This creates a structural contradiction. The rung that can be benchmarked exactly (UEG) has no advantage. The rung that might have an advantage (H) has no exact cross-check and costs 1e17-1e19 Toffoli (resource audit).

Method. WebSearch was refused because the session budget of 200/200 was spent. Everything below was checked on arXiv abstract or HTML pages, through the arXiv API, Crossref or OpenAlex. Items marked [ESTIMATE] are my own arithmetic. Items marked [UNVERIFIED] were not checked against a source.

---

## 1. Is the UEG rung (r_s 2-4, theta 0.25-0.5) already solved classically? Largely yes.

- **The ESA covers the regime from both ends.** Dornheim et al. give an analytical LFC within the effective static approximation. It is "available for the entire range of densities (0.7<=r_s<=20) and temperatures (0<=theta<=4)" (arXiv:2101.05498; the ESA itself is arXiv:2008.02165, PRL 2020).
  - It is anchored at theta = 0 by ground-state QMC and at theta >= ~0.5-1 by PIMC.
  - So theta 0.25-0.5 is an interpolation between two exactly known limits, not an extrapolation into the unknown.
- **Real-frequency finite-T response exists without analytic continuation.**
  - LeBlanc, Chen, Haule, Prokof'ev, Tupitsyn (arXiv:2205.13595, PRL 129, 246401, 2022) use diagrammatic Monte Carlo with algorithmic Matsubara integration. It computes "frequency and momentum resolved finite temperature response directly in the real frequency domain" and extracts f_xc(q,w,T) "at moderate electron density". The exact r_s and T are [UNVERIFIED]; the PDF was not text-readable.
  - Tupitsyn & Prokof'ev (arXiv:2311.05611) use real-frequency diagMC with HF-BSE ladders at r_s = 1, 2, 4, for T/eps_F from <<1 to >2. They state that "contributions beyond the fifth-order are negligible".
  - This is a second classical family for the UEG in exactly the C01 window, independent of PIMC+AC. It is approximate: HF-BSE ladder, with no bias beyond the diagram class.
- **Weak dynamic LFC effects.** At r_s 2-4, dynamic-LFC effects in the UEG are weak. The roton-type feature is a strong-coupling (r_s >~ 10) phenomenon (arXiv:2203.12288; PIMC-AC at r_s = 20 in arXiv:2603.27212).
- **Energies at theta <= 0.5 are covered by several families.**
  - Phaseless FT-AFQMC for theta <= 0.5, r_s <= 2 (arXiv:2012.12228).
  - The pseudo-fermion method at N = 33 spin-polarized, 1 <= r_s <= 2, theta = 0.0625 (Xiong, Morresi, Xiong, arXiv:2603.28000). It "bridges the gap where neither CPIMC nor RPIMC can accurately simulate".
  - Learned sign structure (Frost, arXiv:2607.15060) and hydrodynamic backflow (Vitenburgs & Frost, arXiv:2604.01963) cover energies only.
- **Consequence.** The UEG rung stays useful as an exact cross-check at theta >= 0.5 (the Laplace transform against PIMC F(q,tau)). The claim that the UEG at theta 0.25-0.5 is a quantum-advantage target is dead.

## 2. Is the named H wall (r_s = 2, theta 0.5/0.25) a real classical wall?

- **What the source actually says.** arXiv:2507.00688 (Moldabekov, Shao, Bellenbaum, Ma, Mi, Schwalbe, Vorberger, Dornheim) studies these state points:
  - r_s = 3.23, theta = 1 (T = 4.8 eV)
  - r_s = 2 at T = 12.5 eV (theta = 1), 6.27 eV (theta = 0.5) and 3.13 eV (theta = 0.25)
  - N = 14 and 32.
  - After their correction terms, LR-TDDFT S_ee(q) shows "striking agreement with the PIMC baseline over the entire range of wavenumbers" at theta = 1.
  - "For lower temperatures, PIMC becomes unavailable due to the notorious fermion sign problem."
  - So theta 0.5 and 0.25 are unvalidated predictions from a method that is validated one step higher in temperature. That is a validation gap, not a demonstrated classical failure.
- **The thermal state itself is reached classically in this exact window.**
  - Li, Xie, Dong, Wang (arXiv:2507.18540) run a deep variational free-energy method for the warm dense hydrogen Hugoniot. It uses a normalizing flow for protons, an autoregressive transformer for electron excitations and neural wavefunctions.
  - Coverage: N = 14, 20, 32, 54 atoms; r_s = 1.86-2; T = 10,000-62,500 K, which is theta ≈ 0.07-0.43 at r_s = 2 (T_F ≈ 12.5 eV) [ESTIMATE].
  - The method is "free from the fermion sign problem" and agrees with RPIMC at high T.
  - It computes thermodynamics only, with no S(q) and no dynamics. It is still a classical correlated thermal density matrix in exactly the regime C01 calls classically inaccessible, and it removes C01's claim that the correlated thermal state is out of classical reach.
- **Fixed-node RPIMC also exists in this regime.** The "PIMC unavailable" statement refers to node-free PIMC only.
- **More classical dynamic-response machinery is available and not yet tried at this state point.**
  - Liouville-Lanczos LR-TDDFT removes the empty-band bottleneck at large q and was benchmarked against PIMC ITCF for warm dense H (arXiv:2502.04921).
  - A nonempirical nonlocal-xc TDDFT f-sum-rule correction is in GPAW (arXiv:2609.18584, Sept 2026).
  - Real-time TDDFT for HED (arXiv:2511.14643).
  - Finite-T GW for WDM conductivity (Robinson, Kononov, Stanek, Baczewski, Schleife, Hansen, arXiv:2605.11308). GW+BSE for S(q,w) is the obvious next step.
  - Exact odd-moment and cubic sum-rule constraints tie S(q,w) to n(k) and kinetic energy (arXiv:2508.17810, 2606.30123). These are static quantities that RPIMC or variational methods can supply.
- **No family comparison exists.** I found no paper where two or more ab initio families compare S_ee(q,w) of H at theta <= 0.5. The wall rests on the lack of a comparison, not on a documented disagreement. That is exactly the protein lesson L1/L5 pattern: hardness asserted from a single family.

## 3. Does the observable stay classically easy (limits, sum rules)?

- **Small q (q << k_F): plasmon regime.**
  - The dispersion is fixed to leading orders by the f-sum and third-moment sum rules. The third moment needs the kinetic energy and the potential-energy / S(q) inputs, all static.
  - At r_s = 2, omega_p ≈ 16.7 eV [ESTIMATE], and the plasmon position is what XRTS uses for density.
- **Large q (q >> k_F): Compton/impulse regime.** S is set by n(k) plus final-state corrections, and n(k) is a static PIMC/RPIMC observable (arXiv:2101.00842 for the UEG).
- **Intermediate q ~ 1-2 k_F.** This is where correlation lineshape details matter. At r_s 2-4 they are moderate.
- **Resolution argument.** At theta = 0.25 (T ≈ 3.1 eV), line-shape differences of order T are below NIF source/instrument resolution (5-20 eV) and would need XFEL resolution. XFEL XRTS of H so far is isochoric/non-equilibrium (Fletcher et al., Front. Phys. 2022, doi:10.3389/fphy.2022.838524) or shock-compressed D2 at dissociation. For the latter, Davis et al., Nat. Commun. 2016, doi:10.1038/ncomms11189 inferred ionization from plasmon and Compton scattering and found it consistent with DFT-MD. No equilibrium XRTS measurement of H at r_s ≈ 2, theta 0.25-0.5 at 2-5 eV resolution was found (arXiv query, section 8).

## 4. Information value (L5)

- **T is model-free.** It comes from the ITCF detailed-balance symmetry (arXiv:2604.25735 review), and now even without the source-and-instrument function (arXiv:2510.26747, Baczewski co-author).
  - So the proposed gate K-C01a ("real-frequency S narrows (n_e, T) over model-free ITCF") is mis-framed on T.
  - The quantity that needs a forward model is (n_e, Z/ionization, collision frequency). The comparator is the best classical forward model, not the ITCF.
- **Noise-free degeneracy.** Noise-free synthetic inference is already degenerate: a factor of 3 in DC collision frequency and a factor of 22 in the two-angle sigma_DC posterior for Al at 1 eV (Hentschel, Kononov, Baczewski, Hansen, arXiv:2408.15346). An exact S cannot remove degeneracy that is intrinsic to the data.
- **Analytic continuation is ill-conditioned but low-dimensional.**
  - Only a low-dimensional set of spectral features is stably recoverable (arXiv:2609.07208: super-exponential condition growth with dimension, improved by the detailed-balance constraint; dictionary-learning route arXiv:2606.19205).
  - The same limit applies to the measured spectrum after convolution with the instrument function and added noise. The data carry few independent features, so the extra information that exact real-frequency S adds to the inference is bounded above by the resolution-limited feature count.

## 5. Quantum-side technical objections

- **Finite-size and q access.**
  - q_min/k_F = 2π/(L k_F) = 0.64 (32/eta)^(1/3), independent of r_s [ESTIMATE; matches the resource audit].
  - Reaching q = 0.4 k_F, the collective regime used for density, needs eta ≥ ~131. The eta = 32 rung cannot reach the stated q window, and eta ≥ 128 H is 7e16-1.6e18 Toffoli even Heisenberg-limited (resource audit).
  - Periodic boundary conditions give discrete q, while angle-resolved XRTS is continuous.
- **Thermal state.**
  - A Mermin determinant gives a mean-field initial state, about an 8-16% T bias (resource audit).
  - No bounded-cost correlated Gibbs preparation for 3D Coulomb systems was found (arXiv query, section 8). Classical variational thermal states (arXiv:2507.18540) exist and could seed the quantum preparation, but then the quantum stage must be shown to be load-bearing (L2, FULL vs ABLATION).
- **Ion model floor (L6).**
  - H at 3-6 eV and 0.33 g/cc is two-component and partially molecular/ionized.
  - The quantum S_ee needs Born-Oppenheimer ion snapshots (10-100 snapshots multiply cost) or quantum protons. The ionic feature comes from classical MD anyway.
  - For CH, carbon K-shell electrons in a plane-wave, first-quantized basis force either a huge E_cut or pseudopotentials. Pseudopotentials break the bare-Coulomb selling point. Drop the CH rung.
- **Wrong comparator.**
  - Category 3 "against exact finite-T fermion dynamics" is a straw man (L1/L2). The relevant classical twin is the best approximate family at the required accuracy.
  - The advantage exists only where every classical family fails by more than experimental error.
- **Scoop.**
  - Sandia (Nelson & Baczewski, arXiv:2605.22920) announces WDM linear response.
  - The Sandia opacity protocol (arXiv:2607.02811) is the closest template.
  - Quantum real-space FMM (arXiv:2510.07380, Baczewski co-author) could change the Coulomb cost basis. The resource estimate must be redone against it.

## 6. What would close the gap classically (predicted within 1-2 years)

- A (LR-TDDFT with ESA/PIMC-derived kernel) versus (finite-T GW/BSE) versus (RPIMC-constrained sum-rule models) comparison of S_ee(q,w) for H at r_s = 2, theta 0.5/0.25.
- Pseudo-fermion or variational-NN thermal states extended to static S(q) and ITCF. Pseudo-fermion already reaches theta = 0.0625 for energies.
- Real-frequency diagMC kernels (r_s 1-4, all T) inserted into TDDFT for inhomogeneous H.
- The Dornheim, Moldabekov and Vorberger group is visibly moving each of these toward theta < 1.

## 7. Required revisions (to remain eligible)

1. Recast the UEG as validation only (Laplace-transform match to PIMC F(q,tau) at theta >= 0.5). State explicitly that ESA (theta 0-4) and real-frequency diagMC (r_s 1-4) cover UEG theta 0.25-0.5.
2. Replace the "exact finite-T dynamics" comparator with a named classical portfolio:
   - LR-TDDFT (ALDA/PBE/ESA/PIMC-derived/f-sum-corrected nonlocal kernels; Liouville-Lanczos)
   - RT-TDDFT
   - finite-T GW/BSE
   - Chihara/average-atom
   - RPIMC and variational-NN (arXiv:2507.18540) static constraints via sum rules
   - xi/Taylor-xi PIMC at N = 14-32 with measured extrapolation error.
3. Re-frame K-C01a. T is model-free, so test whether an exact S narrows (n_e, Z, nu) beyond the best classical forward model plus model-free T, at a named instrument resolution. Include the arXiv:2408.15346 degeneracy as the null.
4. Add a theta = 1 control to K-C01b. Families must agree with PIMC there, which calibrates the spread metric. Escalate only if the spread at theta 0.5/0.25 exceeds the experimental error (5-10% intensity, stated resolution) after convolution.
5. Name a consumer experiment at r_s ≈ 2, theta 0.25-0.5 in equilibrium (for example a shocked-D2 Hugoniot XRTS; Davis 2016 is the precedent), with its resolution and error. If none exists or is planned, record the candidate as having no consumer.
6. Fix the scaling ladder. eta ≥ 131 is needed for q = 0.4 k_F. Either raise the lower rung or restrict q to ≥ 0.64 k_F at eta = 32. Include the BO-snapshot multiplier.
7. Before any resource claim, give a bounded-cost correlated thermal-state preparation, or an explicit FULL vs ABLATION design where the thermal state is classically seeded.
8. Redo the resources against first- vs real-space FMM Coulomb costing (arXiv:2510.07380), and resolve the ~1.6e3x Rubin inconsistency.
9. Drop CH unless a pseudopotential-free cost is shown.
10. Pre-register a kill: if K-C01b's inter-family spread at H r_s = 2, theta 0.5, convolved with the instrument function, is below experimental error, move C01 to KILLBOOK.

## 8. Query log

- **WebSearch:** "path integral Monte Carlo warm dense hydrogen dynamic structure factor theta 0.25 sign problem 2026". REFUSED (budget 200/200).
- **arXiv API queries:**
  - abs:"warm dense" AND abs:"sign problem" (by date, 30)
  - au:Dornheim (50 most recent, to 2609.29257)
  - ti:"effective static approximation"
  - abs:"auxiliary-field" AND "finite temperature" AND (electron gas | warm dense | hydrogen)
  - abs:"free energy" AND neural AND (electron gas | dense hydrogen | warm dense)
  - abs:"dynamic structure factor" AND (G1-G2 | Green functions | Kadanoff-Baym) AND (dense | electron gas)
  - au:Bonitz AND (structure factor | density response | warm dense)
  - abs:"Thomson scattering" AND (hydrogen | deuterium)
  - (x-ray scattering | XRTS | inelastic x-ray) AND (hydrogen | deuterium) AND (shock | compressed | warm)
  - (quantum algorithm | quantum computer | quantum computing) AND (warm dense | Thomson scattering | high energy density)
  - abs:"exchange-correlation kernel" AND (jellium | electron gas) AND frequency
  - abs:"dynamic structure factor" AND (TDDFT) AND (warm dense | HED)
  - (thermal state | Gibbs state | Gibbs sampl) AND (electron gas | warm dense | jellium | plane wave) AND quantum. Only one irrelevant hit.
  - (coupled cluster) AND finite temperature AND (electron gas | warm dense | jellium)
  - au:Baczewski (15 most recent, to 2609.12146)
- **arXiv abs/html pages:** 2603.27212 (abs+html), 2101.05498, 2008.02165, 2507.00688 (html), 2507.18540 (abs+html), 2603.28000, 2607.15060, 2604.01963, 2509.11317, 2503.14014, 2502.04921, 2605.07722, 2609.18584, 2205.13595 (abs; PDF not text-readable), 2311.05611 (abs+html), 2606.19205, 2609.07208, 2605.11308
- **Crossref:** "X-ray scattering measurements dissociation-induced metallization dynamically compressed deuterium"; "electron-ion temperature relaxation warm dense hydrogen picosecond x-ray scattering"
- **OpenAlex:** doi:10.1038/ncomms11189 (W2322189278)
- **Not verified:** exact r_s/T of the 2022 PRL diagMC (2205.13595); Davis 2016 numerical state points; Rubin constant-factor resolution.
