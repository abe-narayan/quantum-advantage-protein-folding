# Audit C07 (resource / break-even analyst): finite-T real-frequency S_A(q,w), S_V(q,w) of hot neutron-rich matter for supernova neutrino opacities

Date: 2026-09-28. Role: resource / break-even analyst. Status: FINAL.
Verdict: **KILLED** (as a quantum-advantage target at accessible scales). Short reason: the one piece that actually
needs a quantum computer, the real-frequency axial lineshape with non-central (tensor/OPE) forces at Y_p>0, costs
roughly 1e14 to 1e19 Toffoli per (n,T,Y_p,q) point, which is about 10 to 1e6 years of surface-code runtime per point.
Its measured leverage on supernova observables is <=5% in luminosity. The quantities that set the opacities
(static S_A(q->0), S_V(q->0), mean-field shifts U_n-U_p, sum rules) come from Euclidean or static data, and those are
classically accessible (virial, sign-free SU(4) lattice AFQMC, HF/RPA).

---------------------------------------------------------------------------------------------------------------------

## 1. Verified sources (arXiv abs / arXiv API / Crossref / PDF text; "content from prior knowledge" is flagged)

- [V1] J.D. Watson, J. Bringewatt, A.F. Shaw, A.M. Childs, A.V. Gorshkov, Z. Davoudi, "Quantum Algorithms for Simulating
  Nuclear Effective Field Theories", arXiv:2312.05344. Numbers come from the PDF text (Sec. 7, Table 9). The crossing-time
  evolution uses L=10, a_L=2.2 fm, E_kin=10 MeV, 40 nucleons, total error 0.1 and p=1 Trotter:
  | EFT | 2q depth | T gates | qubits |
  |---|---|---|---|
  | pionless (VC) | 6.0e8 | 4.7e12 | 6,000 |
  | pionless (compact) | 7.9e7 | 4.7e12 | 10,000 |
  | one-pion exchange (OPE) | 3.5e19 | 5.9e23 | 6,000 |
  | dynamical pions | 6.0e36 | 1.3e42 | 99,000 |
  Sec. 7: "We assume that state preparation can be done with separate resources and with high fidelity." Fig. 14 covers
  QPE to 1 MeV. The paper claims about 1e5 lower depth than Roggero et al. 2020 [V4] at about 40 fermions. It says the
  tasks "may be challenging even in the fault-tolerant era".
  My arithmetic: T_cross = a_L L sqrt(M/(2E_kin)) = 22 fm x 6.85 = 150.7 fm/c = 0.76 MeV^-1.
- [V2] A. Roggero, J. Carlson, "Linear Response on a Quantum Computer", arXiv:1804.01505.
- [V3] A. Roggero, "Spectral density estimation with the Gaussian Integral Transform", arXiv:2004.04889. Cost is
  O(sqrt(log(1/eps)(log(1/Delta)+log(1/eps)))/Delta) with qubitization.
- [V4] A. Roggero, A.C.Y. Li, J. Carlson, R. Gupta, G.N. Perdue, "Quantum Computing for Neutrino-nucleus Scattering",
  arXiv:1911.06368.
- [V5] J.E. Sobczyk, W. Jiang, A. Roggero, "Spin response of neutron matter in ab initio approach", arXiv:2407.20986.
  It uses CC plus GIT with chiral EFT at T=0 and analyses finite-size effects.
- [V6] C.J. Horowitz, O.L. Caballero, Z. Lin, E. O'Connor, A. Schwenk, "Neutrino-nucleon scattering in supernova matter
  from the virial expansion", arXiv:1611.05140. It gives virial S_V, S_A in the long-wavelength limit. "S_A is
  significantly reduced from one even at low densities." A fit S_A^f(n,T,Y_p) joins the virial result (low n) to the
  Burrows-Sawyer RPA (high n) and is designed for SN codes.
- [V7] L.F. Roberts, S. Reddy, "Charged current neutrino interactions in hot and dense matter", arXiv:1612.02764.
  Covers mean-field energy shifts and weak magnetism.
- [V8] B.-N. Lu, N. Li, S. Elhatisari, D. Lee, J.E. Drut, T.A. Lähde, "Ab initio nuclear thermodynamics",
  arXiv:1912.05105. The pinhole-trace algorithm is up to 1000x faster than grand-canonical calculations and uses an LO
  interaction.
- [V9] F. Turro, "Quantum Imaginary Time Propagation algorithm for preparing thermal states", arXiv:2306.16580.
- [V10] B. Fore, J.M. Kim, G. Carleo, M. Hjorth-Jensen, A. Lovato, arXiv:2212.04436. NQS for dilute neutron matter
  with LO pionless EFT, competitive with AFDMC.
- [V11] B. Fore, J. Kim, M. Hjorth-Jensen, A. Lovato, arXiv:2407.21207. NQS for the neutron-star crust at
  0.01-0.1 fm^-3 with pionless EFT; clusters emerge.
- [V12] R. Babbush, J. McClean, M. Newman, C. Gidney, S. Boixo, H. Neven, "Focus beyond quadratic speedups for
  error-corrected quantum advantage", arXiv:2011.04149. From the PDF: one Toffoli takes 5.5 d cycles, with d~30 and a
  1 us cycle, so about 170 us per Toffoli per factory. Multiple factories cut this "only by a factor that is between
  about ten and one-hundred."
- [V13] C.-F. Chen, M.J. Kastoryano, A. Gilyén, arXiv:2311.09207. Exact detailed-balance Gibbs sampler. It needs
  Hamiltonian-simulation time proportional to t_mix x beta (polylog factors), with quasi-local jumps on lattices.
- [V14] C.-F. Chen, M.J. Kastoryano, F.G.S.L. Brandão, A. Gilyén, "Quantum Thermal State Preparation", arXiv:2303.18224.
- [V15] T. Melson, H.-T. Janka, R. Bollig, F. Hanke, A. Marek, B. Müller, arXiv:1504.07631. A 3D explosion of a
  20 Msun star is enabled by the strange-quark contribution to NC scattering. Medium and free-space corrections "can
  easily add up to changes of several 10%".
- [V16] P.F. Bedaque, S. Reddy, S. Sen, N.C. Warrington, "Neutrino-nucleon scattering in the neutrino-sphere",
  arXiv:1801.07077. Gives dynamical S_V(q,w) and S_A(q,w) of hot dilute neutron gas in the virial expansion, with
  near-exact scaling laws for T=5-10 MeV and q<30 MeV. The results are analytic at second order in fugacity, and
  "dynamical structure factors are essential".
- [V17] G. Shen, S. Gandolfi, S. Reddy, J. Carlson, arXiv:1205.6499. The w-dependence of the q->0 spin response is
  "well constrained by sum-rules and the asymptotic behavior of the two-particle response" (AFDMC sum rules).
- [V18] G.I. Lykasov, C.J. Pethick, A. Schwenk, arXiv:0808.0330. Fermi-liquid collision-integral response; rates are
  reduced relative to OPE.
- [V19] A. Bartl, C.J. Pethick, A. Schwenk, arXiv:1403.4114. Resonant-Fermi-gas enhancement of pair bremsstrahlung
  and absorption below 1e13 g/cm^3.
- [V20] A. Bartl, R. Bollig, H.-T. Janka, A. Schwenk, "Impact of Nucleon-Nucleon Bremsstrahlung Rates Beyond One-Pion
  Exchange", arXiv:1608.05037. Bremsstrahlung falls by a factor 2-5 in the neutrinospheric region, but luminosities
  change by only <=5%, mean energies rise by <=0.7 MeV, and PNS cooling slows by <=0.5-1 s.
- [V21] E. Rrapaj, J.W. Holt, A. Bartl, S. Reddy, A. Schwenk, arXiv:1408.3368. CC rates at the neutrinosphere from HF
  mean-field self-energies.
- [V22] R. Sharma, S. Bacca, A. Schwenk, arXiv:1411.3266. The n-alpha P-wave (spin-orbit) contribution to the spin
  structure factor matters for T <~ 4 MeV.
- [V23] A. Burrows, D. Vartanyan, J.C. Dolence, M.A. Skinner, D. Radice, "Crucial physical dependencies of the
  core-collapse supernova mechanism", arXiv:1611.05859, Space Sci. Rev. (2018) doi:10.1007/s11214-017-0450-9. Quotes
  obtained via fetch: "proximity to criticality amplifies the role of even small changes in the neutrino-matter
  couplings"; "a few small effects ... can convert an anemic into a robust explosion, or even a dud into a blast"
  (2D only).
- [V24] G. Guo, G. Martínez-Pinedo, ApJ (2019), doi:10.3847/1538-4357/ab536d, chiral-EFT NN bremsstrahlung in SN matter
  (Crossref).
- [V25] E. Shin, E. Rrapaj, J.W. Holt, S.K. Reddy, "Chiral EFT calculation of neutrino reactions in warm neutron-rich
  matter", arXiv:2306.05280, PRC 109, 015804 (2024). Density, spin, isospin and spin-isospin responses of warm
  beta-equilibrium matter; HF plus RPA with direct and exchange terms.
- [V26] J.-W. Chen, D. Lee, T. Schäfer, PRL 93, 242302 (2004), doi:10.1103/PhysRevLett.93.242302 (Crossref). SU(4)
  Wigner limit. The positivity of the SU(4)-symmetric AFQMC measure is used there; this content statement is from
  prior knowledge.
- [V27] D. Lee, T. Schäfer, "Cold dilute neutron matter on the lattice II: Results in the unitary limit",
  nucl-th/0509018. Finite-T lattice neutron matter including spin susceptibility.
- [V28] L. Spagnoli, C. Lissoni, A. Roggero, "Quantum Simulation of Nuclear Dynamics in First Quantization",
  Quantum (2026-09-02), doi:10.22331/q-2026-09-02-2200 (Crossref abstract). LO pionless, first quantization, product
  formulas and QSP. Cost is polynomial in particle number and logarithmic in basis size. Low-energy nuclear scattering
  needs "tens of millions of T gates and few hundred logical qubits".
- [V29] C. Yin, A. Lucas, "Polynomial-time classical sampling of high-temperature quantum Gibbs states",
  arXiv:2305.18514. Classical sampling of Gibbs states is polynomial at sufficiently high T.
- Nearby quantum work with no bearing on C07: arXiv:2608.06515 ("Quantum Computers will constrain the EoS of neutron
  stars", Aug 2026). It covers the cold EoS with a gauge-theory Hamiltonian and has no finite T, no response functions
  and no opacities.

Novelty (scoped): the sources searched (arXiv search pages and API, Crossref, through 2026-09-28) contain quantum
response algorithms [V2, V3], nuclear-EFT simulation costs [V1, V4, V28] and quantum thermal-state algorithms
[V9, V13, V14]. I found no quantum computation, and no quantum-vs-classical study, of the finite-T S_A/S_V of hot
asymmetric matter. The scoped novelty category is therefore **B**. Novelty is not the problem. Resource cost and
decision leverage are.

---------------------------------------------------------------------------------------------------------------------

## 2. Physical state points and what they cost classically (arithmetic)

n = rho/m_N. Thermal wavelength lambda_T = sqrt(2 pi hbar^2/(m T)), with hbar^2/m = 41.4 MeV fm^2.

| rho (g/cm^3) | n (fm^-3) | n/n0 | n lambda^3 at T=4 / 6 / 10 MeV | regime |
|---|---|---|---|---|
| 1e11 | 6.0e-5 | 3.7e-4 | 0.031 / 0.017 / 0.008 | virial, exact to O(z^2) |
| 1e12 | 6.0e-4 | 3.7e-3 | 0.31 / 0.17 / 0.08 | virial still controlled (z ~ 0.05-0.15) |
| 1e13 | 6.0e-3 | 3.7e-2 | 3.1 / 1.7 / 0.8 | virial fails, RPA not controlled: **the only gap** |
| 1e14 | 6.0e-2 | 0.37 | 31 / 17 / 8 | degenerate; RPA/Fermi-liquid/AFDMC/CC, PNS interior |

- The neutrinosphere at 1e11-1e12 g/cm^3 lies at n/n0 ~ 4e-4 to 4e-3. That is BELOW the candidate's stated 0.01-0.3 n0
  window, and the virial expansion [V6, V16] already gives S_V, S_A and even the dynamical S(q,w) analytically there.
  Its classical cost is seconds.
- The genuine classical gap is at about 1e12.5-1e13.5 g/cm^3 (n ~ 0.01-0.1 n0), T ~ 4-10 MeV, Y_p ~ 0.05-0.3. There
  the virial-to-RPA interpolation in [V6] is a fit rather than a controlled calculation.
- **The gap quantity is static.** The long-wavelength S_A(q->0) and S_V(q->0) are equal-time fluctuations
  (susceptibility x T). Imaginary-time lattice AFQMC gets them from G(q, tau=0) with no analytic continuation. For
  SU(4)-symmetric LO contact interactions the AFQMC measure is positive for any Y_p [V26], and finite-T lattice neutron
  matter has been done since [V27]. The SU(4)-breaking pieces (1S0 vs 3S1 difference, OPE) can be treated
  perturbatively, which is the standard NLEFT practice [V8]; the practice claim is from prior knowledge. Cost is
  CPU-hours to GPU-days per point at L = 10-20 and N_t ~ 30-60. **This gap is classically closable. I found no
  published lattice-AFQMC S_A(q->0; n, T, Y_p) table in this window, which is an open classical project, not a quantum
  one.**

### Where the sign problem actually bites (audit Q2)
- LO pionless pure neutron matter is a two-component, spin-balanced attractive contact gas, so it is sign-free (the
  unitary-gas class). LO SU(4)-symmetric np matter at any Y_p is also sign-free [V26].
- Sign problem: non-perturbative OPE tensor forces, spin-orbit, and SU(4) breaking at Y_p>0. These are exactly the
  forces that make the q->0 axial response non-trivial.
- **Key point:** for central (spin-independent or S1.S2) forces, total spin commutes with H, so S_A(q=0,w) is a delta
  function at w=0. Its weight is static and sign-free. A finite lineshape width Gamma at q->0 comes only from
  non-central forces [V17, V18]. So the real-frequency content that needs real time is also the content that carries
  the sign problem. On a quantum computer that means OPE-level Hamiltonians, the 5.9e23-T row of [V1], not the
  4.7e12-T pionless row.

### EFT truncation / model floor (L6, audit Q1)
- Q ~ sqrt(m_N T) = 53 / 68 / 97 / 119 MeV at T = 3 / 5 / 10 / 15 MeV.
- **Pionless:** Q/m_pi = 0.38 / 0.49 / 0.69 / 0.85. A pionless LO calculation is not controlled at T >= 5 MeV, so an
  exact quantum solution of the pionless model is limited by the model floor. Pionless also has no tensor force, which
  makes the axial width identically zero at q=0.
- **Chiral LO/NLO:** (Q/Lambda_b)^2 with Lambda_b ~ 500 MeV is 1-6%. The chiral truncation is controlled, but it
  requires the OPE Hamiltonian, which is the expensive one.
- **Solver spread:** it is large at the lineshape level. OPE and modern-interaction bremsstrahlung differ by a factor of
  2-5 [V20]. Beyond-OPE resonant enhancements appear below 1e13 g/cm^3 [V19], and alpha P-wave contributions appear at
  T<4 MeV [V22]. So solver error does dominate model error for the lineshape (L6 is passed). The next section shows
  this does not help, because the lineshape has little effect on outcomes.

### Lineshape vs static/moments (L5, audit Q3)
- **NC elastic transport opacity:** S_A(q->0) and S_V(q->0) static factors [V6], used in SN codes. Euclidean data fixes
  these.
- **Energy transfer at the neutrinosphere:** [V16] shows that w-dependence matters for decoupling, but at those
  densities it is analytic in the virial expansion. Classical cost is trivial.
- **CC opacities:** dominated by the static mean-field shift U_n-U_p and weak magnetism [V7, V21]. RPA corrections
  [V25] are classical.
- **Lineshape-specific processes:** NN bremsstrahlung and pair absorption, i.e. S_A(w ~ T) from non-central forces.
  Here the w-dependence is also "well constrained by sum rules and the asymptotic two-particle response" [V17].
- **Outcome leverage of the lineshape:** a factor 2-5 change in bremsstrahlung gives <=5% luminosity change and
  <=0.7 MeV mean energy [V20]. This is the L5 pattern: the part that needs real time carries little decision-relevant
  information.

### Supernova outcome sensitivity (audit Q6)
- Explosions near criticality are sensitive to about 10-20% changes in NC opacity [V15, V23]; "a dud into a blast" in
  2D [V23]. That sensitivity sits in the NC elastic channel, meaning the static S_A and S_V (and g_A^s). That channel
  is classically accessible (virial, AFQMC, RPA) and does not need a real-frequency quantum computation.
- A plausible opacity change that is specific to the lineshape does not flip outcomes in the published sensitivity run
  [V20].

### Multi-family disagreement (audit Q4)
- [V6] states outright that its S_A^f fit bridges the virial result (low n) and the Burrows-Sawyer RPA (high n). The two
  families disagree, or are both uncontrolled, in the 1e12.5-1e13.5 g/cm^3 band. I found no named state point with a
  published AFQMC or NQS S_A to adjudicate.
- The disagreement is in a static quantity. It is therefore a target for classical AFQMC (sign-free at LO SU(4)) and
  NQS [V10, V11], not evidence of quantum hardness.

---------------------------------------------------------------------------------------------------------------------

## 3. Quantum cost, end to end (audit Q5)

Target: a real-frequency S_A(q->0, w) with non-central (OPE) forces. Box L=10, a=2.2 fm, 4 species, and N ~ 40-170
nucleons (n = 0.016 fm^-3 gives N ~ 170 in the (22 fm)^3 box; n = 6e-3 fm^-3 gives N ~ 64). Energy resolution
Delta_w = 0.5-1 MeV (widths Gamma ~ T), so the evolution time is t = 1/Delta_w = 200-400 fm/c, about 1.3-2.6 T_cross.

**(a) Time evolution per trajectory.**
- Published Trotter bounds [V1], scaled by 1.3 from the crossing time:
  - pionless: about 6e12 T, 6,000 qubits
  - OPE: about 8e23 T, 6,000 qubits
  These are rigorous upper bounds. Empirical Trotter error is typically 1e2-1e4 smaller, but OPE would still be
  >= 1e19 T.
- My qubitization estimate (order of magnitude) for OPE:
  - Normalization: lambda_kin = 4L^3 x 6 t_hop, with t_hop = hbar^2/(2 m a^2) = 4.3 MeV, gives 1.0e5 MeV.
  - Adding contact and OPE terms (9 spin-isospin structures, range ~2-3 sites) gives lambda ~ 3e5-1e6 MeV.
  - Queries lambda t = 3e5-2e6.
  - Toffoli per query ~1e4 (SELECT over 4L^3 = 4,000 modes plus QROM over translation-invariant OPE coefficients).
  - **Result: about 3e9-2e10 Toffoli per trajectory, uncertain by ±1 order.**
- First-quantized route [V28]: pionless few-body scattering takes ~1e7 T and a few hundred logical qubits. Scaling
  pair terms by (N/3)^2 for N=40 gives about 1e9-1e10, consistent with the estimate above. OPE in first quantization
  has no published cost.

**(b) Thermal state preparation (dominant unknown).**
- Gibbs sampler [V13]: Hamiltonian-simulation time ~ t_mix x beta x polylog, with beta = 0.1-0.33 MeV^-1. There is no
  mixing-time bound for this fermionic, sign-problematic Hamiltonian. Taking t_mix x (number of jump sweeps) between
  1e1 and 1e4 in units of one trajectory gives 1e11-1e14 Toffoli per prepared state.
- Quench typicality (sample a Fermi-Dirac Slater determinant classically, then evolve for thermalization): about 1-3
  trajectories, 1e10 Toffoli. It is unproven for the spin sector, because spin relaxation is the slow mode being
  measured.
- QITE-type thermal preparation [V9] costs O(exponential) in success probability for many-body beta ||H|| and is
  excluded here.
- [V1] explicitly left state preparation out of all its numbers.

**(c) Observable readout (GIT / linear response [V2, V3]).**
- Each shot samples w from S_A(w)/S_A.
- Histogram of 20 bins with bin probability p~0.05 at 3% relative precision: N_shots = (1-p)/(p eps^2) = 2.1e4.
- 10 bins at 10%: 9e2.
- Block-encoding O_q = sum_i sigma_z(i) e^{iq.x_i} (first quantized, alpha = N) succeeds with probability ~S(q)/N ~ 1e-2.
  Amplitude amplification costs ~x10.
- Amplitude estimation (1/eps) needs a coherent thermal state and saves only ~7x at these precisions.

**(d) Totals per (n, T, Y_p, q) point.** Toffoli rate: 1 factory = 1/(170 us) = 5.9e3/s; 100 factories = 5.9e5/s
[V12].

| scenario | shots x (prep + evolve) | Toffoli | 1 factory | 100 factories |
|---|---|---|---|---|
| minimal (10% bins, quench prep) | 9e3 x 2e10 | 1.8e14 | 970 yr | 9.7 yr |
| target (3% bins, x10 success, quench prep) | 2e5 x 2e10 | 4e15 | 2.2e4 yr | 220 yr |
| target with Gibbs sampler (t_mix pessimistic) | 2e5 x 1e14 | 2e19 | 1e8 yr | 1e6 yr |

- An opacity table for SN codes needs about 1e2 (interpolated) to 5e3 (n x T x Y_p x q) points. Multiply by 1e2-1e3.
- **Logical qubits:**
  - First quantized: 14 bits per nucleon x N gives 560 (N=40) to 2,400 (N=170), plus ~1e3 ancilla. Total ~1.5e3-3.5e3.
  - Second quantized: 4,000 (JW) or 6,000 (VC [V1]).
- **Physical qubits:** at d=30 and ~2d^2 = 1,800 physical per logical, that is 3e6-1.1e7, plus ~1.3e5 per factory
  (1.3e7 for 100 factories).
- **Classical pre/post-processing:** negligible (QROM tables, histogramming). Inversion is not needed, which is the one
  real methodological gain.
- **NISQ:** not plausible. The OPE depth bound is 3.5e19 [V1], and even pionless is 6e8 depth; [V1] says near-term is
  infeasible. Fault tolerance is required.

---------------------------------------------------------------------------------------------------------------------

## 4. Classical cost and break-even

- **Virial (static and dynamical, [V6, V16]):** seconds per point. Exact to O(z^2) at z <~ 0.3, i.e. rho <~ 1e12.5
  g/cm^3 for T >= 4 MeV.
- **HF/RPA/Fermi-liquid with chiral EFT [V18, V25, V7]:** seconds to minutes. Uncontrolled at 0.01-0.1 n0 and
  strongly-coupled T.
- **Sign-free lattice AFQMC, SU(4) LO plus perturbative corrections [V8, V26, V27]:** CPU-hours to GPU-days per point.
  - Static S_A and S_V have only statistical error, no inversion.
  - Real-w by MaxEnt/GIT inversion is resolution-limited to structure wider than ~T.
  - Sum-rule plus asymptotic constraints [V17] fix the gross lineshape.
- **With non-perturbative OPE:** the average sign decays as exp(-beta V Delta f). This cost is exponential in volume,
  but the exponent is unknown for this regime. The perturbative-OPE route is polynomial, with error controlled by the
  EFT order.
- **CC-GIT [V5]:** T=0 only, polynomial.
- **NQS [V10, V11]:** ground state and low T; no finite-T response yet.

**Break-even condition.** A quantum run beats classical only for the observable "real-frequency S_A(w) with
non-perturbative non-central forces at Y_p>0, resolution < T". The classical exact alternative there is
exponential-in-volume AFQMC with a sign problem. The classical *practical* alternative is perturbative-OPE AFQMC
statics plus sum-rule-constrained lineshapes plus Fermi-liquid collision widths. Its error, factor ~2 on
bremsstrahlung, maps to <=5% luminosity change [V20], below what SN codes resolve against other uncertainties. So the
decision value of the quantum output is below its ~1e14-1e19 Toffoli (10 to 1e6 yr) price per state point. **There is
no accessible break-even at L = 6-10:**
- the speedup is exponential only on a quantity with low leverage (bremsstrahlung and inelastic lineshape);
- the high-leverage quantities (static NC response, mean-field CC shifts) have polynomial or sign-free classical
  routes, so any quantum gain there is at most polynomial with very large constants (the L3 pattern).

---------------------------------------------------------------------------------------------------------------------

## 5. Kill statement (in KILLBOOK style)

C07 is killed as a quantum-advantage target. It fails three of the hard filters: L5 (information vs computation), L6
(pionless model floor) and decision leverage.
1. The opacity-controlling quantities are static or Euclidean. They come from the virial expansion at the
   neutrinosphere, and at 0.01-0.1 n0 they are accessible to sign-free SU(4) lattice AFQMC.
2. The real-frequency axial lineshape needs non-central forces, which bring the sign problem and the OPE cost row of
   [V1] (5.9e23 T Trotter bound; ~1e10 Toffoli per trajectory by my qubitization estimate). A factor 2-5 change in it
   moves luminosities by <=5% [V20].
3. Thermal-state preparation has no mixing-time guarantee and [V1] leaves it uncosted. Readout needs 1e3-1e5 shots per
   point, which puts even the optimistic end-to-end cost at 1e14 Toffoli (about 10 yr on 100 factories) per state
   point.

**Residual classical opportunity, not quantum:** a sign-free lattice AFQMC table of S_A(q->0), S_V(q->0) for
n = 0.01-0.1 n0, T = 4-10 MeV and Y_p = 0-0.3, to replace the virial-RPA interpolation fit of [V6]. A quantum
candidate can be revived only with new evidence that a lineshape-specific quantity changes SN outcomes by more than
the classical spread.

---------------------------------------------------------------------------------------------------------------------

## 6. Query log (2026-09-28)
- WebSearch: the budget was exhausted (200/200) on the first call, so no WebSearch results were used.
- WebFetch of arxiv.org/abs/2312.05344 and arxiv.org/html/2312.05344(v2) (truncated). Then curl of the PDF and
  pdftotext, which yielded Sec. 7 and Table 9.
- arXiv API id_list (14 IDs): 1804.01505, 2004.04889, 2407.20986, 1612.02764, 1912.05105, 2212.04436, 2407.21207,
  2306.16580, 1611.05140, 1504.07631, 2011.04149, 2311.09207, 1911.06368, 2303.18224. All resolved.
- arXiv API: abs:"spin response" AND abs:"neutron matter" (by date). Hits: 2407.20986, 1801.07077, 1205.6499, 0808.0330,
  nucl-th/0605013.
- arXiv API: abs:neutrino AND abs:bremsstrahlung AND abs:supernova AND abs:spin. Hit: 1411.3266.
- arXiv API: au:Bartl AND au:Schwenk. Hits: 1403.4114, 1608.05037, 1408.3368.
- arXiv API: abs:"many-body corrections" AND abs:supernova, and a later quantum/neutron-matter query: HTTP 429 (no data).
- OpenAlex search (5 queries): HTTP 429, cluster under load (no data). Semantic Scholar: HTTP 429.
- Crossref: "Crucial physical dependencies ..." gave doi:10.1007/s11214-017-0450-9. "neutrino nucleon scattering
  many-body correction supernova explosion sensitivity" gave doi:10.3847/1538-4357/ab536d. "Inequalities for light
  nuclei in the Wigner symmetry limit" gave doi:10.1103/PhysRevLett.93.242302. Also "quantum computing neutron matter
  spin response", "quantum algorithm neutrino opacities supernova matter", "quantum simulation thermal nuclear matter
  dynamical structure factor" and "lattice EFT neutrino response hot neutron matter". Hits included
  10.22331/q-2026-09-02-2200 and 10.1103/physrevc.109.015804. No quantum finite-T opacity paper was found.
- Crossref /works/DOI for 10.22331/q-2026-09-02-2200, 10.1103/physrevc.109.015804, 10.1088/2058-9565/ade335 and
  10.1103/zprr-24ht.
- arXiv web search: "neutrino reactions warm neutron-rich matter chiral" gave 2306.05280. "quantum computer neutron
  matter" (sorted by date, 41 results) turned up no quantum finite-T response or opacity paper; 2608.06515 (EoS)
  appeared. "neutron matter finite temperature lattice Monte Carlo response" (abstract field) returned 0 results.
  "spin susceptibility neutron matter temperature" gave nucl-th/0509018.
- arXiv abs pages fetched: 2306.05280, 2608.06515, 2305.18514, nucl-th/0509018, 1912.05105, and arXiv search
  "Crucial physical dependencies" (1611.05859).
- The Babbush et al. PDF (2011.04149) was extracted for the Toffoli timing (5.5 d cycles, ~170 us, factory
  parallelism limited to 10-100x).

Caveats:
- The qubitization lambda and Toffoli-per-query numbers are my order-of-magnitude derivations, not published figures.
- The Gibbs mixing time is unknown, so the prep range spans 4 orders of magnitude.
- The absence of a lattice-AFQMC S_A table in the 0.01-0.1 n0 window is a scoped finding from the searches above,
  not proof of absence.
