# Audit C04 (resource / break-even analyst): kilonova Ln/An expansion opacity from thermal dipole spectral functions

Status: COMPLETE (2026-09-28). Role: resource / break-even analyst.
Verdict: **KILLED** as formulated (thermal dipole spectral-function opacity per ion). A much narrower
"quantum anchor levels for calibration" variant survives only as a standard low-lying-state
correlated-energy problem (FeMoco genre), where lessons L6/L7 apply and no advantage case is made here.

All arithmetic below is order-of-magnitude. Items marked [ASSUMPTION] are derived here, not taken
from a paper. Items marked [UNVERIFIED] were not checked against a primary source in this session.

---

## 0. Bottom line (one paragraph)

In the valence space that current opacity codes actually use (4f, 5d, 6s, 6p = 32 spinors), full CI
is classically tractable for every Ln II/III ion (at most C(32,14) ~ 4.7e8 determinants in total,
~1e7 per M_J block), so a KPM/Lanczos classical twin can compute a complete binned spectral function.
The classical wall (>~1e12-1e13 determinants per block) appears only when 5s5p core correlation or
a 50-120-spinor correlating space is included explicitly with >= 11-13 correlated electrons. In that
regime the quantum cost of the spectral-function readout is ~6e13-5e18 Toffolis per ion stage per
temperature (~2 to >1e5 QPU-years at a 1 MHz Toffoli rate), because the cost is dominated by
measurement: shot count per bin, Boltzmann reweighting of initial states, and dipole block-encoding
normalization. With ~50-100 ion stages needed for a kilonova composition, even the lenient bound is
~1e2-1e3 QPU-years with ~2-4e6 physical qubits each. The accuracy gain is also not established:
published opacity spreads are driven by configuration-energy placement, completeness and calibration,
which classical optimization and calibration already reduce (errors vs NIST 20-60% -> <=10%), and
the inference is further limited by NLTE (opacity factors 2-10 after a few days), thermalization and
nuclear-physics uncertainties. The speedup is exponential only in a formal sense and cannot matter
at accessible scales. NISQ is not plausible; fault tolerance is required.

---

## 1. Verified sources (all checked this session via arXiv abs/HTML/API records)

Quantum / resource references
- [Q1] Pathak, Kononov, Baczewski, "An approach for calculating astrophysical opacities on quantum
  computers", arXiv:2607.02811 (2 Jul 2026). Pauli-Fierz Hamiltonian, first/second-quantized
  electron + photon registers, interaction-picture simulation; opacity inferred from momentum-resolved
  photon occupations. Solar iron: eta = 26 electrons, N_G = 1.3e13 grid points, N_gamma = 4500 photon
  modes, t = 0.42 a.u.; ~1e4-2e4 logical qubits; ~1e8-1e11 Toffolis; 1e4-1e8 shots; 7-13 Angstrom
  range at ~0.1 Angstrom resolution. Explicitly neglects relativistic effects, inter-ion interactions
  and ionic motion. No kilonova / open-f / low-density treatment. No classical head-to-head.
- [Q2] Lee, Berry, Gidney, Huggins, McClean, Wiebe, Babbush, "Even more efficient quantum computations
  of chemistry through tensor hypercontraction", PRX Quantum 2, 030305 (2021), arXiv:2011.03494.
  Table III/IV (read from PDF this session): Reiher FeMoco (N = 108 spin orbitals, 54 e) THC M = 350,
  lambda = 306.3 Ha, 5.3e9 Toffolis, 2142 logical qubits; Li FeMoco (N = 152) 3.2e10 Toffolis, 2196
  logical qubits; target 1.6 mHa. ~4e6 physical qubits, < 4 days (1 us cycle, 1e-3 gate error);
  ~1e6 physical qubits and < 2 days at 1e-4. Text: "483,000 inner loops times 13,880 Toffolis per
  inner loop, which equals 6.7 billion Toffolis. It would take 3 days ... with four CCZ factories
  distilling at a total rate of 25 kHz." => per walk step ~1.4e4-1.8e4 Toffolis for N ~ 100.
- [Q3] Fomichev et al., "Simulating X-ray absorption spectroscopy of battery materials on a quantum
  computer", arXiv:2405.11015 (2024): CAS(22e,18o); time-domain Monte-Carlo algorithm.
- [Q4] Fomichev et al., "Fast simulations of X-ray absorption spectroscopy for battery materials on a
  quantum computer", arXiv:2506.15784 (2025): 100 logical qubits, < 4e8 T gates per circuit,
  18 orbitals / 22 electrons.
- [Q5] Loaiza et al., "Quantum algorithm for simulating resonant inelastic X-ray scattering in battery
  materials", arXiv:2602.20270 (2026): QPE spectral sampling; 2.0e10 Toffolis, 414 logical qubits,
  up to 20 orbitals (abstract does not say per-circuit vs total).
- Nearby quantum atomic-structure work (all small active spaces, no opacity): arXiv:2212.02058
  (Bayesian phase-difference estimation, fine-structure splitting of B-like ions, 18 qubits,
  Dirac-Coulomb-Breit); arXiv:2212.01801 (D-Wave, B-like fine structure); arXiv:2211.06907
  (relativistic VQE dipole moments BeH-RaH, 12 qubits); arXiv:2606.20166 (D-Wave hyperfine constants
  Li-Mg, <=10 qubits); arXiv:1111.3490 (Veis et al., relativistic QPE, SbH).

Kilonova opacity / atomic data
- [K1] Kasen, Badnell, Barnes, arXiv:1303.5788 (2013): tens of millions of lines; r-process opacities
  orders of magnitude above Fe-rich ejecta.
- [K2] Tanaka, Kato, Gaigalas, Kawaguchi, MNRAS doi:10.1093/mnras/staa1576, arXiv:1906.08914:
  kappa ~ 20-30 cm^2/g (Ye < 0.2), 3-5 (Ye 0.25-0.35), ~1 (Ye 0.4) at 5000-10000 K.
- [K3] Fontes, Fryer, Hungerford, Wollaeger, Korobkin, arXiv:1904.08781 (2019): line-binned
  (area-preserving, linear in f) opacities agree well with continuous Monte Carlo Sobolev and with
  expansion opacity for spectra and light curves.
- [K4] Fontes et al., MNRAS stac2792, arXiv:2209.12759: actinide (Z=89-102) CI line data, line-binned
  opacity tables; ejecta mass/velocity matter more than actinide abundance pattern.
- [K5] Gaigalas, Kato, Rynkun, Radziute, Tanaka, ApJS, arXiv:1901.10671: Nd II-IV level accuracy
  10%, 3%, 11% vs NIST; "overall properties of the opacity are not significantly affected by the
  accuracies of the atomic calculations"; Planck-mean impact up to factor 1.5; timescale ~20%.
- [K6] Kato, Tanaka, Gaigalas, Kitoviene, Rynkun, MNRAS 535, 2670, arXiv:2501.13286: lower
  energy-level distributions of transition arrays -> singly ionized Ln opacities up by factor 3-10;
  ~1.5 for Ln mixture.
- [K7] Floers et al., arXiv:2302.01780 (MNRAS 2023): Nd, U; FAC vs HFR; optimization/calibration
  helps only where experimental levels exist; large code spread otherwise; U opacity ~2x Nd.
- [K8] da Silva et al., arXiv:2502.13250 (2025): Bayesian optimization of FAC fictitious mean
  configuration; mean relative deviation to NIST 20-60% -> <=10% (Au II, Pt II, Pr II/III, Er II/III).
- [K9] Floers et al., arXiv:2507.07785 (2025): calibrated FAC for 28 ions La-Yb II/III;
  146,856 levels, >28e6 transitions, 66,591 experimentally calibrated transitions.
- [K10] Deprince et al., A&A 696, A32 (2025), arXiv:2412.16688: large-scale HFR for all Z=20-103;
  lanthanides not dominant opacity source on average; composition-aware expansion opacity.
- [K11] Brethauer, Kasen, Margutti, Chornock, arXiv:2408.02731 (2024): atomic-dataset choice ->
  lanthanide mass fraction ~1 order of magnitude, lanthanide production factor ~6, mass 25-40%;
  thermalization efficiency -> mass 20-50%; velocity from light curves ~100% error.
- [K12] Pognan, Jerkstrand, Grumer, arXiv:2202.09245 (2022): NLTE deviations after a few days;
  NLTE expansion opacities differ by factors 2-10; sometimes orders of magnitude.
- [K13] Barnes et al., arXiv:2010.11182 (2020): nuclear-physics uncertainties -> peak luminosity
  spread > 1 order of magnitude.
- [K14] Brethauer et al., arXiv:2508.18364 (2025): non-thermal ionization changes required ejecta
  mass by factor ~3 for high-velocity components (from arXiv API record).
- [K15] Arya et al., arXiv:2604.05812 (2026): LTE->NLTE transition for Sr/He at t <~ 1.5 d
  (from arXiv API record).
- [K16] Shingles et al., arXiv:2306.17612: 3D RT with line-by-line opacities for tens of millions of
  transitions + wavelength-calibrated Sr/Y/Zr (from arXiv API record).
- [K17] Ferguson et al., arXiv:2608.20881 (2026) Nd I-V excitation/recombination; arXiv:2606.11748
  U recombination (from arXiv API records): NLTE data gaps.

Classical correlated atomic structure (twin candidates)
- [C1] Kozlov, Tupitsyn, Bondarev, Mironova, PRA 105, 052805 (2022), arXiv:2202.02026: "most current
  methods of calculations fail when the number of valence electrons exceeds four or five"; modified
  CI+MBPT for filling d and f shells.
- [C2] Kahl, Berengut, AMBiT, arXiv:1805.11265: particle-hole CI+MBPT for many valence electrons.
- [C3] Geddes et al., arXiv:1805.06615: saturated/emu CI reduces matrix size (Ta, Db).
- [C4] Yao, Giner, Anderson, Toulouse, Umrigar, J. Chem. Phys. 155, 204104 (2021), arXiv:2109.10271:
  SHCI near-FCI for transition-metal atoms/ions, needs density-based basis-set correction to reach
  CBS within chemical accuracy.
- [C5] Holmes, Tubman, Umrigar, arXiv:1606.07453: heat-bath CI handles 3e14-2e22-determinant spaces
  for ground states.
- [C6] Guo, Li, Chan, arXiv:1803.07150: perturbative DMRG, 28e/76o and 22e/82o active spaces.
- Dzuba/Flambaum CIPT family (arXiv:1804.08244 Db, 2507.16268 Te-Ts, 2301.03154 Dy/Ho/Cf/Es HFS):
  open-f CI with many valence electrons.

---

## 2. Problem sizing: where is the classical wall?

Determinant counts C(N_spinor, n_e) (computed this session):

| spinors N | n=5 | n=7 | n=9 | n=11 | n=13 | n=15 |
|---|---|---|---|---|---|---|
| 32 (4f5d6s6p) | 2.0e5 | 3.4e6 | 2.8e7 | 1.3e8 | 3.5e8 | 5.7e8 |
| 50 (+7s7p6d) | 2.1e6 | 1.0e8 | 2.5e9 | 3.7e10 | 3.5e11 | 2.3e12 |
| 60 | 5.5e6 | 3.9e8 | 1.5e10 | 3.4e11 | 5.2e12 | 5.3e13 |
| 100 | 7.5e7 | 1.6e10 | 1.9e12 | 1.4e14 | 7.1e15 | 2.5e17 |
| 120 | 1.9e8 | 5.9e10 | 1.0e13 | 1.2e15 | 8.8e16 | 4.7e18 |

M_J blocking divides by roughly 10-30 [ASSUMPTION].

- Valence electrons: Nd II 4f4 6s = 5; Gd II 4f7 5d 6s = 9; Er II 4f12 6s = 13; Er III 4f12 = 12;
  Tm II 4f13 6s = 14; U II 5f3 7s2 = 5 (+ 6d/7p). Adding the 5s2 5p6 (or 6s2 6p6 for An) core
  for explicit core-valence correlation adds 8 electrons.
- In the 32-spinor spectroscopic valence space, every Ln II/III ion is <= 5.7e8 determinants total
  (~2e7-6e7 per M_J block): classical Lanczos/KPM is routine. A complete (all-configuration)
  valence-space binned spectral function is therefore a classical calculation.
- Classical KPM cost model [ASSUMPTION]: flops ~ N_mom x N_vec x D x nnz_row, N_mom = spectral span /
  resolution. Effective valence Hamiltonian span ~5-20 Ha, resolution 0.05 eV = 1.8e-3 Ha ->
  N_mom ~ 3e3-1e4; N_vec ~ 20 stochastic vectors; nnz_row ~ 3e4 (direct CI on the fly).
  - D = 1e10: ~6e19 flops -> ~17 h at 1 PF/s sustained (sparse, memory-bound). Feasible.
  - D = 1e12: ~6e21 flops -> ~70 days at 1 PF/s; ~48 TB for 3 complex vectors. Borderline (exascale).
  - D >= 1e13-1e14 per block: infeasible for KPM.
- So the classical wall is crossed only for >= ~11-13 correlated electrons in >= 60-100 spinors,
  i.e. explicit 5s5p core correlation or large correlating spaces, not for the configuration
  completeness problem the opacity codes face.
- Classical alternatives in that regime do not need full CI: CI+MBPT/CIPT/particle-hole CI [C1-C3]
  fold core-valence correlation into an effective valence Hamiltonian at polynomial cost; SHCI
  [C4,C5] and p-DMRG [C6] reach near-FCI for low-lying states. [C1] documents a real weakness of
  CI+MBPT beyond 4-5 valence electrons, which is the genuine classical soft spot (mid/late series).

## 3. Quantum cost of the proposed readout (thermal dipole spectral function)

Hamiltonian block encoding [ASSUMPTION, scaled from Q2]: N = 60-120 complex spinors, THC-like
factorization. lambda ~ 100-1000 Ha (compact 4f and 5s5p orbitals give large Coulomb integrals;
FeMoco N=108 has lambda = 306 Ha). Toffolis per walk step ~1e4-3e4 (Q2: 1.4e4-1.8e4 at N ~ 100;
complex Kramers-paired integrals ~2x) . Logical qubits ~2e3-3e3 (Q2: 2142-2196).

Resolution: kilonova lines are Doppler-smeared by v/c ~ 0.1-0.3 and opacity bins are Delta
lambda/lambda ~ 0.01-0.1, so delta E ~ 0.01-0.05 eV (at 1 um, E = 1.24 eV) is the physically useful
resolution. Model floor for ab initio level energies is ~0.1 eV (10% of ~1 eV levels [K5,K8]), so
finer resolution is meaningless.

QPE walk steps = pi lambda / (2 delta E):

| lambda (Ha) | dE = 0.01 eV | dE = 0.05 eV |
|---|---|---|
| 100 | 4.3e5 steps -> 4.3e9-1.3e10 Tof | 8.6e4 -> 8.6e8-2.6e9 Tof |
| 300 | 1.3e6 -> 1.3e10-3.9e10 Tof | 2.6e5 -> 2.6e9-7.7e9 Tof |
| 1000 | 4.3e6 -> 4.3e10-1.3e11 Tof | 8.6e5 -> 8.6e9-2.6e10 Tof |

Per shot (QPE spectral sampling, as in Q5): (a) prepare a random state in the low-lying
configuration subspace and QPE it to obtain E_i (thermal weight applied by reweighting, not by
coherent Gibbs preparation); (b) apply the dipole block encoding mu (one-body LCU, normalization
alpha_mu ~ 10-50 a.u. vs ||mu|i>|| ~ 1-2 a.u. [ASSUMPTION]), needing ~10-30 amplitude-amplification
rounds that each repeat (a); (c) QPE to get E_f, histogram omega = E_f - E_i.
Toffolis per accepted sample ~ 2 x QPE x f_mu = 2 x (1e9-4e10) x (10-30) = 2e10-2.4e12.

Shots: line-binned opacity kappa_b needs relative error eps_r per bin; bins in the IR tail hold a
fraction w_b ~ 1e-3-1e-2 of total oscillator strength, so N_s ~ 1/(w_b eps_r^2) = 1e3 (w=1e-2,
eps=0.3) to 1e5 (w=1e-3, eps=0.1). Boltzmann reweighting of uniformly sampled initial states over a
~2-4 eV low-lying window at kT = 0.26-0.86 eV (3000-10000 K) costs an effective-sample-size factor
f_B ~ 3-20 [ASSUMPTION].

Total per ion stage per temperature: N_s x f_B x (2 x QPE x f_mu)
- lenient: 1e3 x 3 x 2e10 = 6e13 Toffolis
- central: 1e4 x 5 x 2e11 = 1e16 Toffolis
- strict: 1e5 x 20 x 2.4e12 = 5e18 Toffolis
Wall-clock at 1 us per Toffoli (1 MHz, reaction-limited with many factories): 6e7 s (~2 yr),
1e10 s (~300 yr), 5e12 s (~1.6e5 yr). At the rate actually laid out in Q2 (~2.5e4 Toffoli/s,
four CCZ factories), multiply by 40. Physical qubits ~1e6-4e6 per machine (Q2 layout, 1e-3 to
1e-4 physical error, 1 us cycle). Shots are embarrassingly parallel, so these are QPU-years, not
necessarily calendar years.

Survey cost: a kilonova composition needs ~28 Ln II/III [K9] plus actinides and light r-process
ions, ~50-100 ion stages, and several temperatures (partly shared via reweighting):
~1e2 QPU-years (lenient) to >1e7 QPU-years (strict).

Classical cost for comparison: calibrated FAC for all 28 Ln II/III [K9] and HFR for all Z = 20-103
[K10] are single-group publications, i.e. CPU-days to CPU-months [ASSUMPTION about exact CPU time;
not stated in abstracts]. Valence-complete KPM (Sec. 2) is CPU-hours to GPU-node-days per ion.

Break-even (compute only): the quantum run (>= 6e13 Toffolis, ~2 QPU-years at 1 MHz) is cheaper
than classical KPM only when the per-block CI dimension exceeds ~1e13-1e14, i.e. >= 13 correlated
electrons in >= 100 spinors (explicit core correlation). That regime is not the one that produces
the published opacity spread (Sec. 4).

Time-domain / Hadamard-test alternative (Q3/Q4 style): shorter circuits (<4e8 T per circuit for a
36-spin-orbital space) but the variance scales with the same alpha_mu^2 / (w_b eps_r^2) factors and
t_max ~ 1/dE, so total cost is within ~1-2 orders of the QPE-sampling estimate; it does not change
the verdict.

## 4. Answers to the audit questions

(1) Decomposition of the code-to-code opacity spread. Published evidence attributes it to:
configuration-energy placement of transition arrays (factor 3-10 per singly ionized Ln, ~1.5 for the
mixture [K6]); calibration and optimization where experimental levels exist (large spread without
them [K7]; FAC optimization 20-60% -> <=10% [K8]); configuration completeness and line count [K1,K10];
and code choice (FAC vs HFR [K7]; HULLAC vs GRASP Planck mean up to 1.5 [K5]). Configuration
placement is a correlation effect, so correlation is not minor. However, the observed fixes are
classical (better potentials, Bayesian optimization, calibration), and no study isolates a residual
error that requires near-FCI in a 100-spinor space. No published decomposition quantifies
correlation-solver error separately from basis/model error [scoped: not found in the sources above].
Status: not a clean kill on (1) alone, but the lever that moves opacity is reachable classically.

(2) Sobolev nonlinearity. The spectral function gives Sum_l p_l f_l per bin, i.e. the
line-binned (area-preserving) opacity of Fontes et al. [K3,K4], which [K3] reports agrees well with
continuous MC Sobolev and expansion opacity. So a linear readout suffices for the line-binned
formalism. The Sobolev expansion opacity Sum (1 - e^{-tau_l}) needs the per-bin distribution of
line strengths; a coarse spectral function cannot supply it. Resolving individual lines means
resolution below line spacing (~1e6 lines over ~4 eV -> ~4e-6 eV spacing, 1e4x finer than 0.05 eV)
and >= N_lines samples: infeasible (cost x ~1e4 in QPE depth and x >= 1e3 in shots). Spectral-line
identification (JWST) needs calibrated line wavelengths [K9,K16], which require experiment and are
out of reach of any ab initio solver. So the quantum output could only feed light-curve/SED level
modeling.

(3) Classical twin. Valence-complete (32-spinor) CI + KPM is classically feasible for every
Ln II/III (Sec. 2). Infeasibility only at >= 11-13 electrons in >= 60-100 spinors (D >= 1e12-1e14
per block): late-series ions (Er, Tm, Yb) with explicit core correlation, or mid-series with very
large correlating spaces. Effective-Hamiltonian classical methods (CI+MBPT, CIPT, particle-hole CI,
SHCI) avoid that space; [C1] notes CI+MBPT reliability problems beyond 4-5 valence electrons, which
is the genuine classical soft spot.

(4) Model floor. Ab initio level-energy accuracy ~10% (~0.1-0.3 eV) [K5,K8]; bin/Doppler width
~0.01-0.1 eV; kT = 0.26-0.86 eV. A 0.12 eV level error changes Boltzmann populations by
exp(0.12/0.43) ~ 1.3 at 5000 K. Even near-FCI requires basis-set corrections to reach the CBS limit
for 3d atoms [C4]; for 4f with high-l correlation and Breit/QED the residual floor in a 60-120-spinor
space is plausibly ~0.05-0.1 eV [ASSUMPTION; no 4f benchmark verified]. Solver error does not clearly
dominate model error (L6).

(5) Resources per ion x ~30 ions x charge states: Sec. 3: 6e13-5e18 Toffolis per ion stage per T;
survey ~1e2 to >1e7 QPU-years with ~2-3e3 logical and ~1-4e6 physical qubits per QPU.

(6) Inference sensitivity (L5). Atomic-data choice does move inferred lanthanide fraction by ~6-10x
and mass by 25-40% [K11], larger than thermalization (20-50% on mass) [K11]. But NLTE changes
expansion opacities by 2-10x after a few days [K12] (LTE breaks at t <~ 1.5 d for Sr/He [K15]),
non-thermal ionization changes inferred mass by ~3x [K14], nuclear physics changes peak luminosity
>10x [K13], and LTE thermal rho_T is only valid in the early photospheric phase. The thermal
spectral-function observable addresses only the LTE part; NLTE needs collision/recombination data
[K17] that this algorithm does not produce.

(7) Scoop risk. [Q1] (Sandia) already frames "quantum opacity"; it is nonrelativistic,
first-quantized, dense-plasma, photon-register based and costed for Fe. An extension to relativistic
open-f bound-bound opacity is a natural follow-on for that group; moderate risk on the framing, low
on the kilonova-specific application. In arXiv API searches (opacity AND "quantum computer") no
kilonova quantum paper was found.

## 5. NISQ / fault tolerance

- NISQ: not plausible. The observable needs thousands of excited states per ion with Boltzmann and
  dipole weights; variational excited-state methods would need per-state optimization and
  measurement budgets far beyond classical CI cost in the regime where classical CI is feasible,
  and cannot reach 60-120-spinor spaces with 13+ electrons.
- Fault tolerance required: ~2e3-3e3 logical qubits, 1e9-1e11 Toffolis per QPE, 1e4-1e6 QPE calls
  per ion stage.

## 6. Salvage variant (not endorsed)

"Quantum anchor levels": use QPE only for configuration-average / lowest-level energies of the
~5-20 configurations per ion lacking experimental data (the lever identified in [K6,K7]), then feed
them to a classical calibrated CI line list. Cost ~10-100 QPEs x 1e9-4e10 Toffolis = 1e10-4e12
Toffolis per ion (hours-days at 1 MHz). This removes the measurement bottleneck but reduces to the
standard low-lying-state correlated-energy problem, where the classical twin (FSCC, CI+all-order,
SHCI with basis correction, CIPT) is polynomial and the model floor (basis, Breit/QED, core) is the
same size as the target error. It would need its own audit and is not a distinct quantum mechanism.

## 7. Verdict

KILLED on resources for the spectral-function formulation. Reasons: (i) measurement (shots x
Boltzmann reweighting x dipole normalization) dominates and gives ~2 to >1e5 QPU-years per ion stage;
(ii) the classical wall is only crossed in explicit core-correlation spaces that are not what drives
the published opacity spread; (iii) the needed output for Sobolev opacity and line identification
is line-resolved, which the readout cannot provide; (iv) NLTE, thermalization and nuclear-physics
uncertainties are comparable or larger than the remaining atomic-data error after classical
calibration.

## 8. Query log (2026-09-28)
1. WebSearch: not used (budget exhausted per sibling audit).
2. WebFetch arxiv.org/abs/2607.02811 and arxiv.org/html/2607.02811 (resource numbers).
3. WebFetch arxiv.org/abs/2408.02731, 2507.07785, 2209.12759, 1906.08914, 1303.5788, 1904.08781,
   2501.13286, 2302.01780, 1901.10671, 2502.13250, 2412.16688, 2010.11182, 2202.09245, 2202.02026,
   2109.10271, 2011.03494 (plus PDF text extraction of Tables III-IV), 2405.11015, 2506.15784,
   2602.20270.
4. arXiv API: abs:kilonova AND abs:opacity AND abs:calibrat* (0 results).
5. arXiv API: abs:kilonova AND abs:opacities AND abs:atomic (33 results; listing used for K14-K17).
6. arXiv API: relativistic AND quantum AND (phase estimation OR qubitization OR resource estimates)
   AND (heavy OR actinide OR lanthanide OR Dirac) (28 results; no FT resource estimate for heavy-atom
   relativistic Hamiltonians found).
7. arXiv API: (lanthanide OR actinide) AND (coupled cluster OR CI+MBPT OR CI+all-order) AND ion.
8. arXiv API: "valence electrons" AND "configuration interaction" AND (open shell/f shell/Ln/An).
9. arXiv API: "configuration interaction with perturbation theory" OR (CIPT AND Dzuba).
10. arXiv API: kilonova AND (NLTE OR non-LTE) (21 results).
11. arXiv API: (absorption spectra OR spectral function OR linear response OR dynamical correlation)
    AND fault-tolerant AND (Toffoli OR resource estimate) (0 results); quantum AND spectroscopy AND
    Toffoli (1 irrelevant result).
12. arXiv API: opacity AND "quantum computer" (2 irrelevant results; no kilonova quantum paper).
