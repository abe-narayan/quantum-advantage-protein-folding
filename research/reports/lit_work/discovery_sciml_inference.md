# Discovery lens: inference / scientific ML / inverse problems (2026-09-28)

Status: COMPLETE (subagent pass, ~40 tool calls). Literature only; no computation.
WebSearch budget was exhausted at session start (200/200). All searches were done with WebFetch against the
arXiv export API, arXiv abs/html pages, OpenAlex, Crossref (Semantic Scholar and OpenAlex returned HTTP 429 several times).
"Not found" statements below are scoped to the queries listed in the query log; they are not proofs of absence.

## 0. Framing for this lens

An inverse problem gives a quantum computer leverage only if (i) the FORWARD model (parameters -> observable)
is a real-time / dynamical / finite-temperature many-body quantity that no classical method converges for in
the regime where the experimental data carry the information, (ii) the outer inference loop does not itself
become the bottleneck (N_forward x cost_per_forward), and (iii) the model floor (Hamiltonian form, disorder,
phonons, instrument resolution) is below the solver error. Argmin/sampling over a classical likelihood is at
best quadratic (Babbush et al., PRX Quantum 2, 010103, arXiv:2011.04149 [VERIFIED]) and is not a mechanism.

What ML surrogates do and do not remove:
- Neural surrogates for INS Hamiltonian inference are already standard: CNN/FCNN inverse maps trained on
  linear-spin-wave (LSWT) spectra (arXiv:2609.22535, Luo, Williams, Wu, Dahlbom, Batista, Zhang [VERIFIED]),
  neural surrogate + Bayesian UQ + adaptive experimental design on NiPS3 (arXiv:2608.10350, Liu ... Cheng, Chen
  [VERIFIED]), ML with semiclassical Landau-Lifshitz + MC + small ED for alpha-RuCl3 (arXiv:2202.10715,
  Samarakoon et al., PRR 4, L022061 [VERIFIED]), ML inference from THz 2D coherent spectra using a classical
  two-sublattice LLG forward model (arXiv:2608.14460, Mootz, Huang, Luo, Wang, Yao [VERIFIED]).
- Consequence: the inverse map itself is cheap; the fidelity ceiling is the TRAINING-DATA GENERATOR. Where the
  generator is exact classically (field-polarised phases -> LSWT exact; large-S ordered magnets -> LLG), a quantum
  forward model is not needed. The only opening is the regime where the generator must be a quantum many-body
  dynamics solver and the classical ones (ED <= ~36 spins, tDMRG cylinders W<=6-8, NQS, Pauli propagation,
  QMC+analytic continuation where sign-free) fail.
- MACE / equivariant GNN / foundation interatomic potentials are irrelevant to this class: they learn energies
  and forces, not dynamical many-body correlation functions S(q,w), chi^(3)(t1,t2), RIXS amplitudes.
- Surrogates shift the quantum cost to N_train x C_forward (N_train ~ 1e2-1e4 spectra). With Bayesian optimisation
  in p ~ 4-8 exchange parameters, ~1e2-1e3 forward evaluations is a realistic budget.

## 1. Candidates

### C1. Hamiltonian inference from INS continua of 2D S=1/2 frustrated magnets (Kitaev honeycomb, triangular) in the regime where LSWT/semiclassics fail
- Domain: neutron spectroscopy of quantum magnets (alpha-RuCl3, Na2BaCo(PO4)2, triangular Yb/Co compounds).
- INPUT: measured S(q,w) (zero / intermediate field, T << J, below and just above T_N), instrument resolution
  kernel; model family H(theta) = extended Kitaev (J1,K,Gamma,Gamma',J3, g-tensor) or XXZ-J1-J2 triangular.
- OUTPUT: posterior over theta (MAP + credible region), model-discrimination Bayes factor (e.g. magnon-breakdown
  vs fractionalised-continuum model), and an experimental-design recommendation (next q-cut / field / T).
- Who cares: neutron facilities (ORNL SNS/HFIR, ISIS, ILL, PSI) and the quantum-magnet community; alpha-RuCl3 has
  many incompatible published parameter sets, which is an inference failure.
- Quantum mechanism: quantum computer as the forward model for the dynamical structure factor:
  prepare ground/thermal state (adiabatic / QPE-filtered / METTS-like sampling), Trotter or QSP time evolution,
  single-ancilla correlators <S_i(t)S_j(0)> with randomized time sampling (Fourier/Lin-Tong-style) or the
  frequency-targeted "pumping" method (arXiv:2607.07138), spatial Fourier from translation invariance.
  Replaces: LSWT/LL semiclassics/ED-24 used as the training-data generator for the surrogate. Speedup resource:
  Hilbert-space dimension and entanglement growth in time; classical cost exp(S(t)) vs quantum poly(N, t, 1/eps).
- Classical SOTA: ED/Lanczos (<= 32-36 sites), tDMRG on cylinders (Gohlke, Verresen, Moessner, Pollmann PRL 119,
  157203 (2017) [VERIFIED doi:10.1103/PhysRevLett.119.157203]; kagome DSF Zhu et al. PNAS 2019
  doi:10.1073/pnas.1807840116 [VERIFIED via Crossref]), NQS spectral functions (Mendes-Santos et al. PRL 131,
  046501 (2023) doi:10.1103/physrevlett.131.046501 [VERIFIED via Crossref]), SU(N)/generalised spin-wave and
  semiclassical LL with quantum corrections (Sunny.jl [UNVERIFIED citation]), Pauli propagation, NLCE.
- Why classically hard: 2D, frustrated (sign problem for QMC), long times needed for experimental resolution
  (dw ~ J/30 -> t ~ 100/J), and finite-T continua above T_N.
- Novelty: B. Forward DSF on QPUs exists only for 1D (arXiv:2603.15608 Lee...Kandala, Banerjee, 50 qubits,
  KCuF3/CsCoX3, benchmarked vs MPS, no parameter inference, names 2D triangular as future target [VERIFIED, html];
  arXiv:2607.07138 Granet et al. Quantinuum 20 sites [VERIFIED]; arXiv:2607.02673 Millar et al. 101-spin 1D quench
  spectroscopy [VERIFIED listing]; arXiv:2410.03958 Bauer et al. analog 25-site TFIM [VERIFIED listing];
  arXiv:1809.07974 Chiesa et al. small clusters [VERIFIED listing]; arXiv:2309.15165 Wall et al. PRB 110, 214402
  [VERIFIED]). In arXiv abstract searches (Q1, Q3, Q20) the only paper using a quantum forward model for
  Hamiltonian inference from spectroscopy is Sels et al. arXiv:1910.14221 (NMR). No paper found doing INS
  Hamiltonian inference with a quantum forward model, nor any quantum-vs-classical study of that inference task.
- Main failure risk: (a) information vs computation (lesson 5): experimentalists fit exchange constants in the
  field-polarised phase exactly because LSWT is exact there; the quantum-regime continuum may add little Fisher
  information beyond it. (b) Inference loop cost: with randomized-time single-ancilla sampling ~1e4 circuits per
  S(q,w) at ~1e6 two-qubit gates each (N~72-128, ~1e3 Trotter steps) -> order 1 day per forward eval on an early-FT
  machine; x 1e2 BO points = months (parallelisable across parameter points). NISQ depth insufficient.
  (c) Model floor: stacking faults, disorder, magnetoelastic coupling in alpha-RuCl3.
- Pre-registerable kill test: compute the Fisher information matrix of the zero-field continuum data w.r.t. theta
  using the strongest classical generator on ED-24/32 + DMRG W=4,6 and check whether the eigen-directions left
  unconstrained by polarised-phase LSWT fits are constrained by the continuum; if gain < 2 (the NMR-echo threshold)
  kill.
- Verdict: plausible.

### C2. Inference of exchange couplings of 3D dipolar-octupolar pi-flux quantum spin ice (Ce2Zr2O7, Ce2Sn2O7, Ce2Hf2O7) from polarised INS
- INPUT: polarised INS S(q,w) at T ~ 50 mK, specific heat; model H(Jx,Jy,Jz,Jxz) on the pyrochlore lattice.
- OUTPUT: posterior over (Jx,Jy,Jz,Jxz); predicted spinon-continuum and emergent-photon spectral weight; phase
  assignment (0-flux vs pi-flux QSI).
- Who cares: identification of a 3D U(1) quantum spin liquid (Gao et al. arXiv:2404.04207, polarised INS on
  Ce2Zr2O7 claims pi-flux QSI; theory co-authors Desrochers, Kim [VERIFIED]).
- Quantum mechanism: same DSF forward model as C1 on N = 4L^3 sites (L=3 -> 108, L=4 -> 256 qubits);
  mechanism is real-time evolution of a 3D frustrated XYZ model where tensor networks are ineffective.
- Classical SOTA: QMC + stochastic analytic continuation is exact-in-principle only in the sign-free 0-flux
  regime (Huang, Deng, Wan, Meng PRL 120, 167202 (2018) [VERIFIED doi:10.1103/PhysRevLett.120.167202]; QMC chapter
  Shannon 2021 doi:10.1007/978-3-030-70860-3_10 [VERIFIED]); pi-flux (frustrated transverse exchange) has a sign
  problem; gauge mean-field theory, ED on 16/32-site clusters, NLC thermodynamics, semiclassical MD.
- Why classically hard: 3D + sign problem + small emergent energy scales requiring long simulated times.
  Built-in verification ladder: the sign-free 0-flux sector gives a classical exact reference for the quantum
  pipeline, then one crosses into pi-flux where no classical method converges.
- Novelty: B (no quantum-computing paper on DO pyrochlore dynamics found in queries Q1, Q3, Q17; scoped).
- Main failure risk: emergent photon bandwidth ~ J_perp^3/J_zz^2 is tiny, so resolving it needs t ~ 1e2-1e3/J_zz
  (deep circuits); the INS data may be dominated by the spinon continuum whose shape is weakly parameter-sensitive
  (information risk); disorder / crystal-field admixture (model floor); gauge MFT may already be adequate for the
  decision (flux sector) that matters.
- Verdict: plausible (best "classical-wall" geometry in this lens; weakest on resource).

### C3. Hamiltonian inference / magnon-breakdown diagnosis from THz two-dimensional coherent spectroscopy (2DCS) of S=1/2 frustrated magnets
- INPUT: measured 2D THz nonlinear signal M_NL(t1,t2) (or chi^(2)/chi^(3)(w1,w2)) with pulse polarisations and
  field; model family (extended Kitaev / XXZ / TFIM ladders).
- OUTPUT: posterior over exchange parameters; classification "conventional magnon (universal 2DCS signature) vs
  fractionalised / breakdown" (criterion from Kaib, Moeller, Valenti arXiv:2502.01746 [VERIFIED]).
- Quantum mechanism: simulate the experiment literally: time-dependent Hamiltonian with two pump pulses, measure
  global magnetisation; finite-amplitude / parameter-shift reformulation (Xiong, Wang, Cai, Yuan arXiv:2604.16164,
  IBM, 12-qubit XXZ [VERIFIED]) or generalised QPE for multi-time correlators (Loaiza et al. arXiv:2405.13885
  [VERIFIED listing]); adaptive-variational alternatives (Mootz et al. arXiv:2407.01313 [VERIFIED listing]).
  Global magnetisation is a low-variance observable (shot cost favourable vs site-resolved correlators).
- Classical SOTA: Lanczos frequency-domain chi^(2) on small clusters (arXiv:2502.01746), classical LL/MD
  (Zhang et al. arXiv:2404.16935 [VERIFIED listing]), iTEBD on ladders (Gao et al. arXiv:2209.14070 [VERIFIED
  listing]), ED for 1D (Watanabe arXiv:2401.17266 [VERIFIED listing]), LLG + ML for orthoferrites
  (arXiv:2608.14460).
- Why classically hard: two-time correlators (or strong-pulse driven dynamics) generate more entanglement than
  linear response; the physically important S=1/2 2D regime is outside ED and LLG validity.
- Novelty: C for the forward quantity (quantum algorithms exist, validated only on 12-qubit 1D), B for the
  inference task (inference exists only with classical LLG generator). No quantum-vs-classical advantage study
  found (queries Q5, Q6, Q14).
- Main failure risk: experimental 2D THz data on S=1/2 2D frustrated magnets are sparse (CoNb2O6-type 1D data exist
  [UNVERIFIED]; alpha-RuCl3 2DCS dataset not confirmed); the diagnostic may be decidable on ED-24 already
  (Kaib et al. claim an efficient Lanczos route); model floor from magnetoelectric coupling of the THz field
  (Srivastava arXiv:2502.17554 [VERIFIED listing]).
- Verdict: plausible.

### C4. Spectral resolution benchmark: real-time quantum simulation vs sign-free QMC + analytic continuation (the "(pi,0) anomaly" class)
- INPUT: sign-free 2D model (square-lattice Heisenberg, J-Q model near deconfined criticality, bilayer), L x L,
  target momentum and frequency resolution dw.
- OUTPUT: S(q,w) line shape at a target feature (e.g. (pi,0) continuum vs magnon pole weight) with certified
  error bars; comparison with INS on Cu(DCOO)2.4D2O-type materials.
- Mechanism: the classical pipeline's bottleneck is the ill-posed Laplace inversion G(tau) -> A(w)
  (singular values of the kernel decay exponentially, so resolving features at high w needs statistical precision
  exponentially small in (feature count) [standard result; specific citation UNVERIFIED]). Real-time evolution to
  t ~ 1/dw on a QPU gives direct Fourier resolution with poly cost. This is an information-access mechanism,
  not a Hilbert-space one: QMC already samples the ground state exactly.
- Classical SOTA: QMC + stochastic analytic continuation (Shao, Qin, Capponi, Chesi, Meng, Sandvik PRX 7, 041072
  (2017) [VERIFIED doi:10.1103/PhysRevX.7.041072]), MaxEnt (Bergeron arXiv:1507.01012 [VERIFIED listing]), ML
  continuation (arXiv:2411.17728 [VERIFIED listing]), plus real-time classical: tDMRG cylinders, NQS
  (PRL 131, 046501), Grassmann TEMPO for impurities (arXiv:2401.04880 [VERIFIED listing]).
- Novelty: B. In arXiv queries Q8-Q10 no paper quantifies real-time quantum vs QMC+continuation resolution;
  arXiv:2608.19943 (Guo, IBM) goes the opposite direction (real-time -> imaginary-time).
- Main failure risk: SAC with constrained parametrisations resolves the known features well; tDMRG/NQS real-time
  reach may suffice for L <= 10; the task is scientifically clean but its practical payoff is limited to lineshape
  interpretation. Good as the verification rung for C1/C2 rather than a standalone headline.
- Verdict: plausible (as benchmark); weak as a standalone "practical" project.

### C5. Momentum-resolved L-edge RIXS of doped 2D cuprates/nickelates (Kramers-Heisenberg with core hole on a lattice)
- INPUT: 3-band (or t-t'-U) Hubbard parameters, core-hole potential U_c, lifetime Gamma, incident energy w_in,
  polarisation; measured RIXS maps I(q, w_loss).
- OUTPUT: fitted effective parameters (t', U, U_c), assignment of paramagnon / charge-order / bimagnon features.
- Mechanism: block-encoded resolvent (H - E0 - w_in - i Gamma)^-1 applied to D|psi0> (short intermediate-time
  propagation because Gamma is large), then final-state loss spectrum by real-time evolution or QPE-based spectral
  sampling; ground-state preparation of the doped 2D Hubbard model is the hard step.
- Classical SOTA: ED on 4x4 / sqrt(20) clusters; DMRG correction-vector RIXS (Nocera et al. Sci Rep 2018
  doi:10.1038/s41598-018-29218-8 [VERIFIED via OpenAlex]); DDMRG four-leg t-t'-J ladders (PRB 97, 235137 (2018)
  doi:10.1103/physrevb.97.235137 [VERIFIED via OpenAlex]); root-N Krylov correction vectors (PRB 106, 205106
  [VERIFIED via OpenAlex]); DMFT-based RIXS for metals (PRX 11, 031013 [VERIFIED via OpenAlex]).
- Novelty: B. Quantum RIXS work found is molecular-cluster QPE for cathodes (arXiv:2602.20270, 2.0e10 Toffoli,
  414 logical qubits [VERIFIED listing]); no lattice momentum-resolved quantum RIXS paper in query Q7.
- Main failure risk: ground-state preparation (competing stripe/SC orders), model floor (electron-phonon coupling
  shapes RIXS; PRX 15, 021030 (2025) [VERIFIED via OpenAlex]), resource scale of 3-band fermions (>= 200 logical
  qubits for 8x8 before ancillas).
- Verdict: weak.

### C6. Real-time nuclear response functions for neutrino-nucleus cross sections (removing Euclidean inversion)
- INPUT: chiral-EFT nuclear Hamiltonian, target nucleus (12C, 16O, 40Ar), momentum transfer q.
- OUTPUT: inclusive response R(q,w) and flux-averaged cross sections for DUNE/T2K modelling.
- Mechanism: linear-response quantum algorithm (Roggero & Carlson arXiv:1804.01505 [VERIFIED listing]),
  lattice qubit-efficient mapping with Trotter + QPE (Weiss, Baroni, Carlson, Stetcu, PRC 111, 064004 (2025),
  arXiv:2404.00202 [VERIFIED]).
- Classical SOTA: GFMC Euclidean response + inversion (A <= 12), AFDMC, coupled-cluster Lorentz-integral-transform
  (Sobczyk, Acharya, Bacca, Hagen PRL 127, 072501 (2021) for 40Ca [VERIFIED doi]), spectral-function / factorisation
  approximations.
- Novelty: C (algorithms + resource analyses exist; no quantum-vs-classical advantage study found in Q4, Q15).
- Main failure risk: model floor (chiral-EFT truncation, two-body currents) and flux averaging smooth out the
  resolution that inversion loses (lesson 5); resources for A=40 on a lattice are far-FT.
- Verdict: weak.

## 2. Killed ideas (this lens)
- Liquid-state NMR spectrum simulation / quantum ABC NMR inference (Sels et al. arXiv:1910.14221; hardware 21 spins
  arXiv:2609.17102, 34 spins arXiv:2512.14513): challenged (category E) by Fratus et al. arXiv:2508.06448 clustering
  solver with linear scaling through typical experimental regimes [VERIFIED].
- 1D INS forward modelling (KCuF3, CsCoX3, CuSO4): already on hardware (arXiv:2603.15608, 2607.07138) and exact
  classically (MPS/Bethe); no advantage possible.
- Quantum-accelerated inference loop (quantum MCMC, amplitude estimation of likelihood integrals, Grover over
  parameter grids): quadratic at best on a classical likelihood; killed by Babbush et al. 2021 and lesson 3.
- Quantum neural networks as inverse maps (spectrum -> parameters): no mechanism; classical CNN/FCNN inverse maps
  already robust at 10% noise (arXiv:2609.22535).
- Quantum-computed labels for ML interatomic potentials / foundation models: N_labels x QPE cost per label, model
  floor of active spaces; for weakly correlated regimes DFT/CC labels suffice. (Crossref query Q19 found no
  quantum-labelled MLIP study; reasoning-based kill.)
- DMFT quantum impurity solver for ARPES/optics fitting (Bauer, Wecker, Millis, Hastings, Troyer PRX 6, 031045
  (2016) arXiv:1510.03859 [VERIFIED]): model floor (double counting, U/J, locality) dominates solver error;
  real-frequency classical solvers improving (TEMPO arXiv:2401.04880, neural real-frequency solver
  doi:10.1103/3jm2-nqvn [VERIFIED via Crossref], strong-coupling solver doi:10.1103/jjjl-v1pj [VERIFIED via Crossref]).
- Thermodynamic fitting (C(T), chi(T)) of frustrated magnets: low information content; NLCE/XTRG/FTLM converge in
  the temperature window where the data discriminate parameters (lesson 5).
- Molecular-nanomagnet INS/EPR spin-Hamiltonian fitting (Chiesa arXiv:1809.07974): clusters are ED-tractable.
- Exoplanet opacity line lists via quantum rovibrational simulation: classical variational line lists and
  super-lines cover retrieval-relevant (<= 6 atom) molecules; retrieval bias dominated by broadening/PES data
  ("impending opacity challenge", Niraula, ISMS 2023 doi:10.15278/isms.2023.7149 [VERIFIED record]) = model floor.
  Crossref query Q18 found no quantum paper (scoped).
- Pump-probe trARPES of photodoped 2D Hubbard: model floor (phonons, multiband, pulse coupling) as in the killed
  ultrafast-demagnetisation lane; NEGF / nonequilibrium DMFT competitors. arXiv query Q12 found no quantum paper.
- Quantum-sensor Hamiltonian learning of nuclear-spin clusters (NV mapping): forward model is CCE-classical
  (same reason as the molecular spin-qubit decoherence kill).
- Lattice-QCD real-time transport / parton distributions: far-FT resources, outside "practical" scope.

## 3. Cross-cutting recommendation
If one project is chosen from this lens: C1+C2+C4 as a single ladder ("quantum forward model for neutron
Hamiltonian inference"): C4 in the sign-free sector as the certified rung, C1 (2D Kitaev) against tDMRG/NQS,
C2 (3D pi-flux QSI) as the classical-wall target. First deliverable is not a quantum run but the Fisher-information
kill test: does data in the quantum-hard regime constrain parameter directions that polarised-phase LSWT fits
leave free? Claim category attainable near term: 1 (quantum usefulness); category 3 only on early FT hardware.

## 4. Query log (2026-09-28)
- Q0 WebSearch x3 (INS DSF fitting; analytic continuation; nonlinear spectroscopy) -> budget exhausted, no results.
- Q1 arXiv API: abs:"quantum computer" AND abs:"neutron scattering" (sorted by date, 25)
- Q2 OpenAlex: quantum computer dynamical structure factor spin model (429)
- Q3 arXiv API: abs:neutron AND Hamiltonian AND (machine learning OR Bayesian) AND quantum
- Q4 arXiv API: "quantum computer" AND "response function" AND (neutrino OR nuclear)
- Q5 arXiv API: (nonlinear spectroscopy OR 2D coherent OR multidimensional) AND (quantum computer/algorithm/simulator)
- Q6 arXiv API: 2DCS/nonlinear response AND spin liquid/quantum magnet AND DMRG/tensor -> 0 results; then
  abs:"two-dimensional coherent spectroscopy" AND (spin OR magnet)
- Q7 arXiv API: (RIXS OR resonant inelastic x-ray) AND quantum computer/algorithm/computing
- Q8 arXiv API: "analytic continuation" AND (quantum computer OR quantum algorithm)
- Q9 arXiv API: spectral function AND imaginary time AND real time AND "quantum advantage" -> 0 results
- Q10 arXiv API: "analytic continuation" AND "ill-posed" AND (quantum simulation OR real-time)
- Q11 arXiv API: "dynamical structure factor" AND (quantum processor/computer/hardware)
- Q12 arXiv API: (pump-probe OR trARPES OR photoemission) AND Hubbard AND quantum computer/algorithm/processor
- Q13 arXiv API: NMR AND spectra AND (quantum computer OR fault-tolerant OR quantum advantage)
- Q14 OpenAlex: RuCl3 two-dimensional terahertz nonlinear spectroscopy
- Q15 Crossref: quantum computing neutrino nucleus scattering response function
- Q16 OpenAlex: quantum computing inverse problem neutron scattering Hamiltonian learning
- Q17 Crossref: Ce2Zr2O7 quantum spin ice exchange parameters dynamical structure factor
- Q18 Crossref: quantum computing rovibrational spectra line list exoplanet opacity
- Q19 Crossref: quantum computing training data ML interatomic potential strongly correlated
- Q20 arXiv API: "quantum computer" AND Hamiltonian AND (inverse problem OR parameter estimation OR Bayesian
  inference) AND (spectroscopy OR scattering OR spectra) -> only Sels 2019 (NMR)
- Q21 OpenAlex: RIXS Hubbard DMRG exact diagonalization
- Q22 Crossref: DSF two-dimensional NQS spectral functions; DSF triangular Heisenberg MPS cylinder;
  impurity solver DMFT quantum; Sunny.jl (no hit)
- DOI/abs verifications: 2603.15608 (abs+html), 2607.07138, 2608.10350, 2609.22535, 2202.10715, 2608.14460,
  2502.01746, 2604.16164, 2508.06448, 2404.00202, 1510.03859, 2011.04149, 2309.15165, 2404.04207,
  10.1103/PhysRevX.7.041072, 10.1103/PhysRevLett.127.072501, 10.1103/PhysRevLett.120.167202,
  10.1103/PhysRevLett.119.157203, OpenAlex W4406706928 (Maskara et al. Nat Phys 2025 doi:10.1038/s41567-024-02738-z:
  Rydberg digital-analog spectroscopy of polynuclear TM clusters and 2D magnets; relevant prior for C1 mechanism).
- Unverified / not fetched: resource numbers in Beverland et al. arXiv:2211.07629 (existence verified, 2D-dynamics
  numbers not); Sunny.jl citation; existence of 2D THz datasets on alpha-RuCl3 / CoNb2O6.
