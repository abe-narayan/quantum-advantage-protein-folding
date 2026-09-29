# Audit C14 (resource / break-even analyst): finite-T polarized S(q,w) of 3D dipolar-octupolar pi-flux quantum spin ice

Date: 2026-09-28. Role: resource / break-even analyst. Scope: Ce2Zr2O7 (primary, the polarized INS of Gao et al. 2404.04207), with Ce2Sn2O7 backscattering as a stress-test variant.
**Verdict: KILLED as specified.** The decision observable at INS resolution needs only short real-time windows (t*J_par <= 13). The quantum cost is set by preparing the low-T Gibbs state and by the shot count, not by the 3D real-time dynamics that motivates the proposal. The model floor (vacancies, unidentifiable theta and c_QSI) exceeds any plausible solver spread. One narrow redesign lane is noted in section 9 (Ce2Sn2O7 backscattering, powder). It is scored separately as "wounded at best" and would need its own pre-registration.

All numbers are order-of-magnitude. Arithmetic is shown. Anything not verified in this session is marked [UNVERIFIED].

---

## 1. What the data actually constrain (verified from primary sources)

### Ce2Zr2O7, polarized ThALES (Gao et al., arXiv:2404.04207; Nature Physics, doi:10.1038/s41567-025-02922-9). Text extracted from the arXiv PDF.
- T = 50 mK (entire experiment). k_B T = 0.00431 meV.
- Ef = 3.23 / 2.51 meV. Energy resolution FWHM = 0.076, 0.062, 0.042 meV at X, K, (1,1,0) (Extended Fig. 2). The text elsewhere quotes about 0.065 meV (Ef = 3.23) and 0.042 meV (Ef = 2.52).
- Quasielastic window: E = 0 +- 0.03 meV. Spinon features at about 0.025 / 0.05 / 0.075 / 0.12 meV.
- Best fit: J_par = 0.076 meV, J_pm = 0.021 meV, theta = 0.12 pi, hbar c_QSI/a0 = 0.0028 meV. The paper says these are "approximately 1.2 times the ones in Ref. 20", with the same J_pm/J_par ratio.
- Direct quotes on identifiability: "the goodness of fit is very shallow as a function of c_QSI", and "c_QSI and theta cannot be uniquely determined with the energy scans". Acceptable fits cover hbar c/a0 in [0.0004, 0.0028] meV and theta in [0.05 pi, 0.12 pi]. The photon signal "essentially yields a Gaussian centered at the elastic position after the convolution".
- Method: chi^2 over energy scans at three Q points. The Gaussian broadening width is a free parameter (within +-50% of the resolution), along with a global prefactor C.
- The classical theory used was GMFT plus Gaussian QED. The authors report that the spinon-continuum position agrees between GMFT, 32-site ED (pi-flux) and QMC (0-flux) (Extended Fig. 6).

### Ce2Zr2O7, CNCS in a [111] field (Gao et al., arXiv:2601.03202; PRL 136, 256703 (2026), doi:10.1103/svt2-m3pp; Crossref verified)
- Ei = 3.32 meV. Elastic resolution about 0.1 meV FWHM. T about 50 mK. Fields 0 to 0.2 T, with a 3 T background.
- ED was run **only on a 16-site cube**. The supplement says the photon weight there is a finite-size artifact: a 4-site winding loop gives K4 ~ J_pm^2/Jzz, which exceeds the bulk hexagon ring K6 ~ J_pm^3/Jzz^2. To compensate, the authors use theta = 0.2 pi in ED instead of the fitted value of about 0.1 pi. **This is a real solver-limited step in the current workflow.** Section 5 explains why it still does not create a quantum case.

### Ce2Sn2O7, powder backscattering (Poree et al., arXiv:2304.05452; Nat. Phys. 21, 83 (2025))
- IN16B BATS mode: 3.3 ueV resolution over a +-250 ueV window. HR mode: 0.7 ueV over +-30 ueV. IN5: 11 ueV. T = 0.17 K, about 15 ueV. The spectrum is wavevector-integrated.
- The two classical models give **incompatible parameter sets** for the same data:
  - spinon hopping on a classical-spin-ice background: J_par = 48 ueV, J_pm = -5.2 ueV, J_ring = 0.73 ueV
  - GMFT three-peak fit: J_par = 69 ueV, J_pm = -17 ueV, J_ring = 12.4 ueV
  - A QED-onset fit gives 2Delta about 18 ueV, against 33 ueV from GMFT.
  
  The authors state that fitting QED parameters directly "may require resolutions in both energy and momentum space that are far beyond current spectroscopic techniques". They also note a sample dependence: another growth route gave dipolar-spin-ice / AIAO-proximate behaviour.

### Model-floor evidence
- Sanders, Naik, Hallen, Schafer, arXiv:2609.28643 (2026-09-23), "Defect Poisoning of Quantum Spin Ice". Using QMC and ED, they find that vacancy-induced fluctuations dominate "already at dilution levels as low as two percent, well below those reported in cerium-based pyrochlores", and can "strongly contaminate, and potentially completely obscure" QSI signatures.
- Smith et al., arXiv:2407.07640 (PRX 15, 021033 (2025)) fit diffuse (energy-integrated) scattering down to 0.05 K with **numerical linked-cluster (NLC)** calculations. The static and quasi-static structure at 50 mK is therefore already reachable by a classical cluster method.
- Ce2Zr2O7+x oxidation / Ce2Zr2O8 transformation is documented in the chemistry literature (Crossref record of the Chem. Mater. SI, doi:10.1021/acs.chemmater.7b03091.s001; main-article metadata [UNVERIFIED]).

## 2. Energy and time scales (arithmetic)

The parameters are Gao's fit, with Smith-type ratios for the remaining couplings. Those ratios are an inference: the absolute values of the Smith et al. PRX 2022 set, about (0.063, 0.062, 0.011) meV, are [UNVERIFIED]; only the "1.2x" ratio is verified.
Scaled couplings: (J~x, J~y, J~z) ≈ (0.076, 0.074, 0.013) meV, so Sum|J| ≈ 0.163 meV.

| Quantity | Value |
|---|---|
| T / J_par | 0.0043/0.076 = 0.057 (beta*J_par = 17.6) |
| T / J_pm | 0.21 |
| J_ring = 12 J_pm^3/J_par^2 | 0.019 meV (the fitted hbar c/a0 = 0.0028 meV is set independently) |
| Resolution Gaussian sigma = FWHM/2.355 | 0.018 (ThALES best), 0.028 (ThALES), 0.042 (CNCS) meV |
| Useful time window t_max ≈ 3/sigma | 168 / 109 / 71 meV^-1 |
| **t_max * J_par** | **12.8 / 8.3 / 5.4** |
| t_max * J_pm | 3.5 / 2.3 / 1.5 |
| Lowest photon mode at L = 2/3/4 (hbar c/a0 * 2pi/L) | 0.0088 / 0.0059 / 0.0044 meV |
| One photon period at L = 2/3/4, in t*J_par | 54 / 81 / 109 |
| Ce2Sn2O7 BATS (J_par ≈ 60 ueV) | t*J_par ≈ 128 (t*J_pm ≈ 24) |
| Ce2Sn2O7 HR | t*J_par ≈ 600 (t*J_pm ≈ 110) |

**Consequence (audit Q3).** For the Ce2Zr2O7 data (ThALES or CNCS), the information-bearing real-time window is t*J_par <= 13, which is about 3.5/J_pm. The "t ~ 50/J_pm" in the candidate is roughly 14x longer than the data resolve. The photon needs at least 54 to 109 J_par^-1 for a single period at L = 2 to 4. Its energy, 0.0004 to 0.0028 meV times 2pi/L, lies 7 to 100x below the FWHM, so the photon enters the likelihood only through an integrated quasielastic weight. That weight is controlled by quasi-static (equal-time-like) correlations, the regime where NLC (Smith 2025) and ED are already used.

This is protein lesson 5 again. The long-time 3D dynamics where tensor networks fail is the part the data cannot see. The part the data can see is short-time or quasi-static.

## 3. Hamiltonian and oracle size (N = 16 L^3 spins, 3N bonds, 3 Pauli terms per bond after the theta rotation)

| L | N (logical system qubits) | bonds | Pauli terms M | lambda = N_b*Sum|J|/4 | lambda/J_par | lambda*beta |
|---|---|---|---|---|---|---|
| 2 | 128 | 384 | 1152 | 15.6 meV | 206 | 3.6e3 |
| 3 | 432 | 1296 | 3888 | 52.8 meV | 695 | 1.2e4 |
| 4 | 1024 | 3072 | 9216 | 125 meV | 1650 | 2.9e4 |

Block encoding (qubitization) costs about 4M Toffoli per walk step: SELECT uses unary iteration over M terms, and PREP is cheap because translation invariance leaves only 3 distinct coefficients. At L = 3 that is about 1.6e4 Toffoli per step.
Trotter is cheaper for this local lattice. Use second-order Trotter with Hamming-weight phasing. Each step has 18 equal-angle groups (3 Pauli types x 6 edge colours), each of W = N_b/6 rotations. The cost is about 18*(4W + 40*log2 W) T. At L = 3, W = 216, giving 2.1e4 T per step. With dt*J_par = 0.2, which is empirical and local-observable Trotter error is roughly size-independent:

| L | t*J_par = 5.4 (CNCS) | 13 (ThALES) | 80 (one photon period, L = 3) |
|---|---|---|---|
| 2 | 4.8e5 T | 1.2e6 T | 7e6 T |
| 3 | 1.1e6 T | 2.8e6 T | 1.7e7 T |
| 4 | 2.3e6 T | 5.6e6 T | 3.5e7 T |

These totals include x2 for a controlled (Hadamard-test) evolution.

Cross-checks:
- Childs et al. (arXiv:1711.10980, PNAS 115, 9456 (2018)): a 50-spin 1D Heisenberg chain at t = n = 50 with epsilon = 1e-3 needs 1.8e8 T (empirical PF) or 2.4e9 T (segmented QSP) with generic rotation synthesis. Our per-circuit figure is lower mainly because of Hamming-weight phasing and short t. Take the dynamics cost as **1e6 to 1e8 T per circuit**.
- Yoshioka et al. (arXiv:2210.14109, npj QI 2024): 10x10 J1-J2 Heisenberg QPE at epsilon = 0.01 needs 5.3e8 to 8e8 T (qubitization), with a single-thread clock of 1 to 10 kHz.

**The dynamics itself is cheap. It is not the bottleneck.**

## 4. The bottleneck: preparing the finite-T state at T = 0.057 J_par (audit Q5)

Physical regime at L = 3:
- T is below the one-spinon gap. With Delta_1 ≈ 0.0125 to 0.025 meV, the Boltzmann factor is e^{-Delta/T} = 0.055 to 0.003. Over 216 tetrahedra that gives about 12 to 0.7 thermal spinons, so the state is not near the ground state.
- The lowest photon mode (0.0059 meV) is comparable to T, with n_B ≈ 0.34, so photons are thermally populated.
- Flux and winding sectors of the ice manifold are connected only by spinon-pair creation and winding, or by global loop moves.

Preparation routes, with cost per independent sample (C_prep):
1. **Filtered random product states (METTS-like, QITE by QSP).** The success probability is about Tr e^{-beta(H - E0)}/2^N ≈ exp(-N(ln 2 - s)). With the Pauling entropy s ≈ 0.20 per spin, this is about **1e-92** at N = 432, or 1e-46 with amplitude amplification. Dead.
2. **Ground state by QPE from a GMFT or NQS trial state, followed by thermal dressing.**
   - The overlap is f^216 for per-tetrahedron fidelity f: 0.013 at f = 0.98 and 1.5e-5 at f = 0.95.
   - A QPE resolving the finite-size gap (about 0.006 meV) needs about lambda/gap = 8.8e3 walk steps, or 1.4e8 Toffoli.
   - Repeating this over the overlap gives **1e10 to 1e13 Toffoli**.
   - It still yields only the T = 0 state, which is not the measured ensemble (thermal spinons and photons, above).
3. **Detailed-balance Lindbladian Gibbs sampler.** See Chen, Kastoryano, Brandao, Gilyen, arXiv:2303.18224 (cost is polynomial in beta, 1/epsilon and the mixing time, with the mixing time left open), and Hahn et al., arXiv:2505.22816 (local driving, guarantees conditional on mixing time).
   - Each jump application needs Hamiltonian simulation over about 3*beta, i.e. t*J_par ≈ 50, which is about 250 Trotter steps, or roughly **1e7 T** including the forward/backward pair.
   - Jump count to mix is about N*tau:
     - optimistic, tau ≈ 10 sweeps: 4e3 jumps, **4e10 T**
     - Arrhenius-limited sector mixing, tau ≈ e^{Delta_1/T} ≈ 18 to 330: 8e3 to 1.4e5 jumps, **1e11 to 1.4e12 T**
   - Warm-start reuse between samples cuts this by about 3x.
   - No published mixing-time bound or estimate exists for a U(1) QSL at T << J_pm. None was found in the sources searched (arXiv API searches on "thermal state preparation" + resource/T-count, and "Gibbs" + "resource estimates"; see the query log). This is a **major unquantified risk**.
4. **Heuristic (variational or adiabatic) quasi-thermal preparation**, taken as about 10x C_evol ≈ 1e7 to 1e8 T. This has no guarantee and no validation route in the pi-flux phase (QMC has a sign problem; ED is limited to 32 sites). **It is the only route that makes the numbers below look accessible.**

The ratio C_prep/C_evol is about 10 (heuristic) up to 1e4 to 1e6 (Gibbs sampler or QPE). **State preparation dominates.** This meets the audit's explicit kill condition.

## 5. Shots / measurements for the decision version

Observable: <tau^z_i(t) tau^z_j(0)> in local frames. Only the dipolar component couples to neutrons (Smith 2025 saw no octupolar signal at the 0.1% level). Polarization channels (M_y, M_z) come from geometry. Settings:
- 4 sublattice sources, with translation invariance and all sites read out per shot
- about 10 to 20 time nodes, enough for Gaussian-resolution quadrature up to 0.3 meV
- Re and Im parts

That gives 80 to 160 settings. At 3e3 to 1e4 shots per setting, for 3 to 5% relative error on S(q,w) when INS error bars are 5 to 20%, one hypothesis needs **2.4e5 to 1.6e6 shots**. For 3 to 5 hypotheses (parameter sets, 0 vs pi flux, theta and c scan), that is **7e5 to 8e6 shots**. **Each shot needs an independent (or decorrelated) Gibbs sample.**

## 6. End-to-end totals and wall-clock

C_total = N_shots x (C_prep + C_evol). The L = 3 ThALES decision:

| Scenario | C_prep + C_evol per shot | shots | total T | at 1e4 T/s (1-10 kHz single thread, Yoshioka) | at 1e6 T/s (optimistic many-factory, 1 us cycle) |
|---|---|---|---|---|---|
| Heuristic prep (unvalidated) | 1e8 | 7e5 | 7e13 | 2e2 yr | 2.2 yr (8 days on 100 QPUs) |
| Gibbs sampler, fast mixing | 1.5e10 | 2e6 | 3e16 | 1e5 yr | 1e3 yr |
| Gibbs, Arrhenius sector mixing | 5e11 | 8e6 | 4e18 | 1e7 yr | 1.3e5 yr |
| QPE-from-GMFT (T = 0 only, wrong ensemble) | 1e10 to 1e13 | 7e5 | 7e15 to 7e18 | 2e4 to 2e7 yr | 2e2 to 2e5 yr |

Qubits:
- about 432 system qubits, plus 50 to 500 ancillas for HWP adders, the phase register, jump ancillas and the Hadamard ancilla. That is **about 0.5 to 1e3 logical qubits**.
- Surface code at p = 1e-3 needs d ≈ 21 to 31 for 1e14 to 1e18 T, which is 2d^2 ≈ 0.9 to 1.9e3 physical qubits per logical.
- Total **about 1 to 2e6 physical qubits** plus magic-state factories. This is comparable to the Yoshioka "few hundred thousand" at 100 spins, scaled by about 4 to 10x for the logical count.
- Simulator runtime is not relevant. The regime is far beyond state-vector simulation at N >= 50.

**NISQ plausibility: none.**
- L = 2 (128 qubits) at t*J_par = 13 needs 65 Trotter steps of 384 bonds x (3 CNOT) = 7.5e4 CNOT before routing. Embedding the 3D pyrochlore graph (degree 6) on 2D hardware adds SWAP overhead of O(L), about 2 to 3x.
- At 2-qubit error 1e-3, the circuit fidelity is about e^-75 to e^-225.
- The low-T Gibbs state prep does not exist on NISQ at all.
- The closest demonstrated work is 1D with up to 50 qubits: Lee et al., arXiv:2603.15608 (KCuF3 / CsCoX3 DSF versus INS on a superconducting processor).
- No gate-model or analog 3D pyrochlore dynamics was found. An arXiv API search for "spin ice" plus processor/Rydberg/ion returned only 2D proposals and a 3D Rydberg Monte Carlo study (Wang et al., arXiv:2502.00836, which does not compute dynamics). **Fault tolerance is required.**

## 7. Classical cost of the strongest competitors (same decision)

- GMFT / Gaussian QED: seconds to minutes per parameter set. It is the method Gao and Poree actually fit with.
- SCEBR (Desrochers and Kim, arXiv:2401.09551, PRB 109, 144410 (2024)): analytic finite-T 0-flux and pi-flux S(q,w). Minutes.
- ED at 32 sites with finite-T typicality plus Chebyshev (Hosoi et al., arXiv:2201.00828, PRL 129, 097202 (2022), used ED + MD):
  - the state vector is 2^32 x 16 B = 69 GB
  - one matvec is about 96 bonds x 4.3e9, or 4e11 operations
  - about 1e3 matvecs are needed (imaginary time for beta*J_par ≈ 18, plus real time for t*J_par ≈ 13)
  - total about 4e14 operations, i.e. **about 1 to 10 node-hours**
  - 36 sites is feasible but costly
- NLC for static and quasielastic correlations down to 0.05 K (Smith et al., PRX 15, 021033 (2025)).
- Large-N dynamics: 3D belief-propagation tensor networks (Tindall et al., arXiv:2503.05693, Science 392, 868 (2026)), and t-VMC with Jastrow-Feenberg or larger ansatze (Mauron and Carleo, arXiv:2503.08247, 128 spins on a 3D diamond lattice; Wiersema, arXiv:2609.01719).
  - Both classes closed D-Wave-type quench and anneal claims. Those were pure-state anneals from product states, not finite-T correlators at T << J_pm.
  - Neither has been tested on pi-flux QSI finite-T correlators. This is an adversarial test that has not been run, not evidence in either direction.
  - At t*J_par <= 13 and T = 0.057 J_par, a METTS + BP-TN or purification approach is the natural classical attack.
- QMC + SAC is exact for 0-flux only. pi-flux has the sign problem.

**Size break-even:** trivially above about 36 sites for exact methods, so already at L = 2.
**Value break-even:** not reached. The decision-relevant classical error (GMFT versus ED32 versus SCEBR) must exceed the model floor and the data's discriminating power. The evidence points the other way:
- Gao's chi^2 is shallow and theta/c_QSI are unidentifiable at 0.04 to 0.1 meV resolution.
- The GMFT, ED32 and QMC spinon-gap positions already agree (Gao Methods).
- A 2% vacancy level, below the reported Ce-pyrochlore levels, dominates the low-energy physics (Sanders 2026). An exact solve of the clean XYZ model is therefore the wrong model (FeMoco-type lesson 6).
- A disordered model multiplies both quantum and classical costs by the number of disorder realizations (about 10 to 100).

## 8. Answers to the audit questions (resource view)

1. **Decision-flip pre-test.** For the Ce2Zr2O7 ThALES data, it is likely to fail, meaning the solvers agree on the ranking.
   - Gao reports GMFT, ED32 and QMC agreement on the continuum position, and a shallow chi^2 in the only parameters that the long-time physics (photon) controls.
   - The one documented solver sensitivity is the 16-site ED photon-weight artifact (arXiv:2601.03202). It is fixable classically with 32 to 36-site ED, NLC or GMFT and does not require L >= 3 dynamics.
   - For Ce2Sn2O7 backscattering, a **real flip exists between approximate classical theories**: J_pm = -5.2 versus -17 ueV (a 3.3x difference) and J_ring differing by 17x. This is the only live thread (section 9).
2. **Model floor.** Vacancies at 2% or more dominate (arXiv:2609.28643), and Ce2Zr2O7+x oxidation exists. Theta and c_QSI are unidentifiable, and a free broadening of +-50% is used in the fit. The model floor is larger than any plausible exact-versus-GMFT spread in resolution-convolved S(q,w). **Fail.**
3. **t_max and T-count.** Spinon continuum: t*J_par ≈ 5 to 13 (resolution-limited). Photon: t*J_par of at least 54 to 109 per period at L = 2 to 4, which is unresolvable at current single-crystal resolution. Dynamics costs about 1e6 to 1e7 T per circuit at L = 3. The full decision costs **7e13 to 4e18 T**, dominated by preparation and shots.
4. **BP-TN / t-VMC / NQS at L = 3, t ~ 50/J_pm.** Not needed for the Ce2Zr2O7 decision, which needs t ~ 3.5/J_pm. At the short times the data need, classical methods are strongest. The adversarial test at t*J_par <= 13 and T = 0.057 J_par remains to be run, but it lies on the classical side's home ground.
5. **Is a finite-T state above the photon scale sufficient?** The experiment runs at T ≈ 0.2 J_pm, above the fitted photon scale (0.0028 meV < 0.0043 meV) and below the spinon gap. Gibbs mixing across ice and flux sectors at T < Delta_spinon has **no mixing-time bound or estimate**. A plausible Arrhenius factor e^{Delta/T} ≈ 20 to 300 multiplies an already dominant cost. **Prohibitive or unquantified.**
6. **Practical significance.** The practical value is material characterization for the neutron community. It is valuable science, but the decision is already made by cheap classical theories at the resolution available, so an exact solver would add little decision value.

## 9. Redesign lane (not C14 as specified): Ce2Sn2O7 powder backscattering, local DOS at 0.7 to 3.3 ueV

- **Why it is different:**
  - The data resolve t*J_par ≈ 128 to 600, where finite-size ED (32 sites) and short-time cluster methods lose control.
  - Two published classical theories give incompatible parameters for the same spectrum (Poree et al.). That is an existing solver-driven decision ambiguity.
  - T ≈ 0.25 J_par (beta*J_par ≈ 4), so Gibbs preparation is much cheaper and plausibly fast-mixing.
- **Resources:**
  - C_evol at L = 3 for t*J_par = 128 to 600 is 640 to 3000 Trotter steps x 2.1e4 T, i.e. **2.7e7 to 1.3e8 T** per circuit (x2 controlled).
  - C_prep at beta*J_par ≈ 4: each CKG jump needs Hamiltonian simulation over 3*beta ≈ 12 J_par^-1, which is 60 Trotter steps, or about 2.5e6 T including the forward/backward pair. Times about 4e3 jumps, that gives about 1e10 T per sample.
  - Shots: a powder-averaged local DOS needs about 40 to 80 settings x 3e3, i.e. about 2e5 per hypothesis, or 6e5 for 3 hypotheses.
  - **Total about 6e15 T**, which is about 200 years at 1e6 T/s, or about 2 years on 100 QPUs.
- **Why it is still wounded:**
  - The observable is a powder, wavevector-integrated DOS (weak discrimination).
  - Sample dependence has been reported between growth routes.
  - Vacancies (the 2% threshold) apply here too.
  - The needed classical attack has not been run: 32 to 36-site ED with typicality plus NLC for dynamics plus t-VMC at T ≈ 0.25 J_par.
  - The quantum cost is still about 1e15 T.
- **It needs its own pre-registration, including a decision-flip pre-test:** do ED32, GMFT and SCEBR rank the J_pm = -5.2 and -17 ueV sets differently once all are convolved with the IN16B resolution?

## 10. Claim category

If anything were ever shown, it would be category 3, a computational/resource advantage for simulating a 3D model's finite-T dynamics. At the decision level, nothing in categories 1 to 6 is supported for C14 as specified. The outer inference carries no advantage by design.

---

## Query log (2026-09-28)
- WebSearch was unavailable (session budget exhausted: "200 of 200").
- WebFetch https://arxiv.org/abs/2404.04207 (OK). arxiv.org/html/2404.04207 and /html/2404.04207v1 returned 404. nature.com returned an auth redirect. The arXiv PDF was fetched and its text extracted locally with pypdf (47 pages).
- curl arxiv.org/pdf/{2304.05452, 2210.14109, 1711.10980, 2601.03202}, then pypdf text extraction and grep for resolution, meV, T-count, etc.
- WebFetch arXiv abs: 2304.05452, 2401.09551, 2210.14109, 1711.10980, 2201.00828, 2503.05693, 2503.08247, 2609.01719, 2303.18224, 2011.04149, 2603.15608, 2609.28643, 2510.14813, 2407.07640.
- export.arxiv.org API:
  - abs:"Gibbs" AND abs:"resource estimates" AND abs:quantum: 1 hit (2112.07646), no lattice end-to-end estimate.
  - abs:"dynamical structure factor" AND abs:"fault-tolerant": 1 hit (2603.15608).
  - abs:"thermal state preparation" AND (T-count OR resource): 2505.22816, 2402.04221, 2303.06161, 2208.13112, none with a lattice T-count.
  - abs:"spin ice" AND (quantum processor OR quantum computer OR Rydberg OR trapped ion): only 2D proposals, plus 3D Rydberg MC (2502.00836).
  - abs:"quantum spin ice" AND dynamics AND (ED OR neural OR tensor network OR Monte Carlo): 2609.28643, 2510.14813, 2505.15677, 2502.14067, 2401.09551, 2201.00828, 2112.00014.
  - abs:Ce2Zr2O7 AND (exchange OR parameters): 0 hits (the query form failed).
  - ti:"Spectroscopic Demarcation": 2601.03202.
- OpenAlex: search "Ce2Zr2O7 exchange parameters dipolar octupolar" (from 2020): Bhardwaj 2022 (doi:10.1038/s41535-022-00458-2), Smith PRB 108 054438 (2023), Poree Ce2Hf2O7 (doi:10.1103/j451-ztvr), Sanders 2312.11641, Gao PRL 2026 (doi:10.1103/svt2-m3pp), Beare muSR PRB 108 174411, Smith 2407.07640, Poree Nat Phys doi:10.1038/s41567-024-02711-w. OpenAlex record for Bhardwaj 2022 (abstract reconstructed). A second OpenAlex query returned HTTP 429.
- Crossref: works/10.1103/svt2-m3pp (PRL 136, 256703, 2026-06-23). Query "Ce2Zr2O7 oxidation Ce4+ oxygen stoichiometry" returned only the Chem. Mater. SI record doi:10.1021/acs.chemmater.7b03091.s001.

## Citations (verified this session unless marked)
- Gao B. et al., "Emergent photons and fractionalized excitations in a quantum spin liquid", arXiv:2404.04207; Nat. Phys. doi:10.1038/s41567-025-02922-9.
- Gao B. et al., "Spectroscopic Demarcation of Emergent Photons and Spinons in a Dipolar-Octupolar Quantum Spin Liquid", arXiv:2601.03202; PRL 136, 256703 (2026), doi:10.1103/svt2-m3pp.
- Poree V. et al., "Fractional matter coupled to the emergent gauge field in a quantum spin ice", arXiv:2304.05452; Nat. Phys. 21, 83 (2025) (doi:10.1038/s41567-024-02711-w per OpenAlex).
- Sanders A. L., Naik, Hallen, Schafer, "Defect Poisoning of Quantum Spin Ice", arXiv:2609.28643 (2026).
- Smith E. M. et al., "Single Crystal Diffuse Neutron Scattering Study of the Dipole-Octupole QSI Candidate Ce2Zr2O7", arXiv:2407.07640; PRX 15, 021033 (2025).
- Desrochers F., Kim Y. B., SCEBR, arXiv:2401.09551; PRB 109, 144410 (2024).
- Hosoi M. et al., arXiv:2201.00828; PRL 129, 097202 (2022).
- Zhou C. et al., "Quantum Fisher Information as a Thermal Probe ... QSI", arXiv:2510.14813; Nat. Commun. 17, 7975 (2026).
- Bhardwaj A. et al., npj Quantum Mater. (2022), doi:10.1038/s41535-022-00458-2. The parameter values are [UNVERIFIED]; the abstract gives none.
- Tindall J. et al., arXiv:2503.05693; Science 392, 868 (2026).
- Mauron L., Carleo G., arXiv:2503.08247.
- Wiersema R., arXiv:2609.01719 (2026).
- Lee Y.-T. et al., "Benchmarking quantum simulation with neutron-scattering experiments", arXiv:2603.15608.
- Childs A. M. et al., arXiv:1711.10980; PNAS 115, 9456 (2018).
- Yoshioka N. et al., arXiv:2210.14109; npj Quantum Inf. (2024).
- Babbush R. et al., arXiv:2011.04149; PRX Quantum 2, 010103 (2021).
- Chen C.-F., Kastoryano, Brandao, Gilyen, "Quantum Thermal State Preparation", arXiv:2303.18224.
- Hahn D. et al., arXiv:2505.22816 (listing verified via the arXiv API).
- Wang J. et al., arXiv:2502.00836 (listing verified via the arXiv API).
- Smith E. M. et al., PRX 12, 021015 (2022) parameter set (about 0.063, 0.062, 0.011 meV) [UNVERIFIED; used only via Gao's verified "1.2x" statement].

## Assumptions flagged
- T-gate throughput: 1e4 T/s is the conservative single-thread figure (Yoshioka: 1 to 10 kHz). 1e6 T/s is optimistic (many factories, about 1 us cycle).
- The Trotter step dt*J_par = 0.2 is empirical and unverified for this model. Rotation synthesis costs about 40 T at 1e-10.
- The mixing times of Gibbs samplers in a U(1) QSL are unknown. The Arrhenius factor is a heuristic.
- Shots per setting (3e3 to 1e4) assume O(1) relative single-shot variance of the Fourier-summed estimator.
