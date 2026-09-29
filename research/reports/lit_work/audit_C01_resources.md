# Audit C01 (XRTS real-frequency S_ee(q,w) of partially degenerate warm dense matter): resource and break-even analysis

Date: 2026-09-28. Role: resource / break-even analyst. Status: COMPLETE.
Verdict: **WOUNDED**. The practical version (H, Be or CH at eta >= 128, instrument-level resolution, XRTS inference) is resource-killed at any accessible fault-tolerant rate. A reduced UEG benchmark (eta ~ 32, theta ~ 0.25, 5 eV resolution, Heisenberg-limited estimation) gets within 1.5 to 3 orders of the S*G <~ 1e12 bar and needs a later-FT rate. Measurement and state preparation dominate the cost; the Hamiltonian simulation does not.

Everything below is an order-of-magnitude estimate. Numbers taken from papers carry citations. Numbers I derived show their arithmetic. The script is in the session scratchpad (`c01_cost.py`) and is not a repo file.

---

## 1. Verified anchors

### 1.1 Rubin et al., stopping power (closest resource precedent)
N. C. Rubin, D. W. Berry, A. Kononov, F. D. Malone, T. Khattar, A. White, J. Lee, H. Neven, R. Babbush, A. D. Baczewski, "Quantum computation of stopping power for inertial fusion target design", arXiv:2308.12352 (PNAS 2024). Verified from the arXiv PDF text:
- Table II. Alpha + H at 1 g/cm^3: Omega = 2419.68 a0^3, eta = 218, r_s = 1.383, Ecut = 2000 eV (73.5 Ha), N^(1/3) = 53, Delta = 0.2533 a0, n_p = 6. Proton + D (10 g/cm^3): eta = 1729, r_s = 0.813. Proton + C: eta = 391.
- Table III. Alpha + H: block-encoding cost C_BE = 2.498e4 Toffoli, 5650 logical qubits, lambda = 1.745e6 Ha. Proton + D: C_BE = 1.423e5, 33038 qubits, lambda = 8.82e7.
- Table IV (QSP, 10 times from t = 1 to 10 a.u., N_s = 50 samples per time, eps = 0.01). Alpha + H: eta = 28 gives 5.59e14, eta = 92 gives 2.03e16, eta = 218 gives 1.99e17 Toffoli. The 8th-order product formula gives 1.12e13, 3.07e14 and 1.40e15. The paper says the total is "10^15-10^17 Toffoli gates ... and 10^3 logical qubits", and that a "benchmark scale (29 quantum particles)" needs "10^13 Toffoli gates".
- Cost scaling: the paper finds about O(eta^2) at fixed r_s and fixed plane-wave count, within Õ(eta^{4/3}) to Õ(eta^{8/3}).
- **Thermal state.** The initial state is "a Slater determinant drawn from the solution of a Mermin Kohn-Sham DFT calculation". This is a mean-field approximation, not the exact Gibbs state. The paper justifies it for stopping power. For S_ee(q,w) it is not adequate (see section 3.2).
- **Internal inconsistency I could not reconcile.** lambda*C_BE = 1.745e6 * 2.5e4 = 4.4e10 Toffoli per a.u. of evolution. Fig. 8a implies about 1e12 per a.u. (1e13 at t = 10). Table IV implies about 7e13 per a.u. (1.99e17 / (50 * 55 a.u.)). I bracket the per-a.u. cost g between lambda*C_BE (low) and 23 * lambda*C_BE (high, the Fig. 8a factor). A Table IV-like overhead would add about two more orders.

### 1.2 Other verified sources
- Su, Berry, Wiebe, Rubin, Babbush, "Fault-tolerant quantum simulations of chemistry in first quantization", arXiv:2105.12767, PRX Quantum 2, 040332 (2021). Toffoli complexity is Õ(eta^{8/3} N^{1/3} t + eta^{4/3} N^{2/3} t).
- Babbush, Huggins, Berry, Ung, Zhao, Reichman, Neven, Baczewski, Lee, "Quantum simulation of exact electron dynamics can be more efficient than classical mean-field methods", arXiv:2301.01203, Nat. Commun. 14, 4058 (2023). The abstract names finite temperature as the regime where the speedup is largest, and says sampling overhead reduces the speedup.
- Babbush, McClean, Newman, Gidney, Boixo, Neven, "Focus beyond quadratic speedups for error-corrected quantum advantage", arXiv:2011.04149 (PRX Quantum 2021). Verified from the PDF text: Toffoli time t_G = 30 * 5.5 * 1 us, about 170 us, for one factory at a 1 us surface-code cycle (Eq. 6), so t_Q = 170 us * G.
- Roggero, Carlson, "Linear response on a quantum computer", arXiv:1804.01505, PRC 100, 034610 (2019). Samples energy transfer by phase estimation on O|psi>.
- Rall, "Quantum algorithms for estimating physical quantities using block encodings", arXiv:2004.06832, PRA 102, 022408 (2020). Covers correlation functions, density of states and linear response, with amplitude estimation.
- Quantum thermal state preparation (Lindbladian Gibbs sampler), arXiv:2303.18224. The abstract gives cost as a function of temperature, accuracy and the Lindbladian mixing time (or gap), and says detailed balance is approximate. The author list, Chen, Kastoryano, Brandão, Gilyén, is [UNVERIFIED from the fetched page; recalled].
- Pathak, Kononov, Baczewski, "An approach for calculating astrophysical opacities on quantum computers", arXiv:2607.02811 (2026-07-02). Spectral readout through a photonic register; logical resources "comparable" to Rubin 2024. The abstract does not mention a DSF or XRTS.
- Dornheim, "The fermion sign problem in path integral Monte Carlo simulations: quantum dots, ultracold atoms, and warm dense matter", arXiv:1906.00635, PRE 100, 023307 (2019). Verified from the PDF text: "a small sign (typically S~10^-3) means that simulations are no longer feasible". For the UEG at r_s = 2, S decays exponentially in N (at theta = 0.75) and in beta (N = 14), and "simulations become unfeasible for theta <~ 0.5 even for such a comparatively small system size" (N = 14; "typical system size for the UEG are N = 33").
- Dornheim et al., "Ab initio path integral Monte Carlo simulations of the uniform electron gas on large length scales", arXiv:2311.08098. xi-extrapolation to N <= 1000 for static properties (S(q), chi(q), LFC).
- Dornheim et al., "Fermionic free energies from ab initio PIMC simulations of fictitious identical particles", arXiv:2502.15288: "accurate results for the exchange-correlation free energy down to half the Fermi temperature".
- Dornheim, Robles, Hamann, Chuna, Svensson, Schwalbe, Moldabekov, Tolias, Vorberger, "Taylor series perspective on ab initio PIMC simulations with Fermi-Dirac statistics", arXiv:2509.11317 (2025-09-14). Analyses the applicability of xi-extrapolation through the Taylor radius of convergence. The abstract gives no numeric theta threshold.
- Dornheim et al., "Unraveling electronic correlations in warm dense quantum plasmas", arXiv:2402.19113. PIMC applied to NIF Be XRTS data.
- Dornheim, Groth, Vorberger, Bonitz, "Ab initio PIMC results for the dynamic structure factor of correlated electrons", PRL 121, 255001 (2018), doi:10.1103/physrevlett.121.255001 (Crossref).
- Dornheim, Vorberger, Moldabekov, Böhme, "Analyzing XRTS experiments of WDM in the imaginary-time domain", arXiv:2211.00579. Model-free temperature extraction from the ITCF.
- Gawne, Vorberger, Moldabekov, Bellenbaum, Dornheim, "Model-free interpretation of X-ray Thomson scattering measurements", arXiv:2604.25735 (2026-04-28). The ITCF gives model-free access to "temperature, normalization, Rayleigh weight". The paper names the "source-and-instrument function" as the remaining limitation.
- Chuna, Böhme, Dornheim, "Temperature dependence of the dynamic structure factor of the electron liquid via analytic continuation", arXiv:2603.27212 (2026-03-28). MaxEnt and PyLIT applied to PIMC data.
- Moldabekov et al., "Applying the Liouville-Lanczos method of TDDFT to warm dense matter", arXiv:2502.04921. No empty states needed; DSF at large q; benchmarked against PIMC for Al and H.
- Moldabekov et al., "Enhancing the efficiency of TDDFT calculations of dynamic response properties", arXiv:2510.01875 (npj Comput. Mater. 12, 168 (2026)). Up to 10x speed-up using the DSF-ITCF mapping.
- Svensson et al., arXiv:2407.08875: DSF of warm dense hydrogen from explicit real-time electron dynamics (wave packets). Title seen in an arXiv listing only.

## 2. Quantum protocol assumed (the cheapest variant I could construct)

1. **Representation.** First-quantized plane waves (Su 2021, Rubin 2024), with 3*eta*n_p system qubits.
2. **Thermal state.** Microcanonical (ETH) preparation. Sample a thermal-Hartree-Fock or Mermin determinant (cost Õ(N*eta), negligible). Filter it with QPE to an energy window of delta_E ~ 0.3 Ha, about 10% of the canonical energy width T*sqrt(1.5*eta), which is about 3 Ha for eta = 128 at theta = 0.5, r_s = 2. The QPE time is 2*pi/delta_E, about 21 a.u. With acceptance about 0.2 to 0.3, t_prep is 60 to 100 a.u. of evolution-equivalent per shot. This is optimistic: it assumes ETH-level ensemble equivalence and a reweighting to the canonical ensemble that needs a density of states the protocol does not know. The exact-Gibbs alternative (arXiv:2303.18224) has an unknown mixing time.
3. **Observable.** A linear-response kick followed by a projective position measurement. Apply U = exp(-i g sum_j cos(q.r_j)), a diagonal phase costing about eta*n_p Toffoli, which is negligible. Evolve for time t, apply the QFT, measure all positions, and compute rho_q classically. This gives chi''(q,t), and the fluctuation-dissipation theorem gives S(q,w). It avoids the Hadamard test, and one snapshot gives rho_q at all reciprocal-lattice q.
   - Why not a Hadamard test? rho_q = sum_j e^{iq.r_j} has LCU norm eta, so the normalized signal is S(q)/eta and shots scale as (eta/eps)^2, about 1.6e8 per time point at eta = 128 and eps = 0.01.
   - Why not the unitary single-electron trick? e^{iq.r_1} gives only the self (incoherent) part F_s(q,t), not the collective plasmon.
   - The Roggero-Carlson QPE sampling works, but post-selecting rho_q|psi> succeeds with probability S(q)/eta, about 1/256, and each failure costs a fresh thermal preparation.
4. **Shot noise.** Per shot, signal is about g*eta*|chi| and noise about sqrt(eta*S(q)). With g = 0.1 (about 1% nonlinearity) and |chi|/sqrt(S) about 0.3, SNR per shot is about 0.03*sqrt(eta).
5. **Time grid.** t_max = 2*pi/Dw, Dt = pi/w_max with w_max about 3.7 Ha (±100 eV), N_t = t_max/Dt.
6. **Cost per a.u.** g = lambda*C_BE (low) to 23*lambda*C_BE (high). lambda is a crude T + V_ee + V_ei estimate, calibrated by a factor of 2.86 to Rubin's lambda = 1.745e6 for eta = 218, Delta = 0.253. Crude estimates: lambda_T = eta*1.5*k_max^2, lambda_ee = eta^2*k_max/pi, lambda_ei = 2*lambda_ee (Z = 1), with k_max = pi/Delta. C_BE = 2.5e4*(eta/218)*(n_p/6), floored at 2e3. The UEG uses Delta = 0.32 a0 and no ions. Hydrogen uses Delta = 0.253 a0 (Rubin's Ecut).
7. **Per-shot cost.** G = (t_prep + t_max/2) * g.

## 3. Results

### 3.1 Cost table (derived; see section 2 for assumptions)

| case | eta | theta | Dw | lambda (Ha) | g (Toffoli per a.u.) | G per shot | shots S (SQL) | S*G (SQL) | S*G (Heisenberg AE, x3 coherent-prep overhead) |
|---|---|---|---|---|---|---|---|---|---|
| UEG benchmark, eps = 5% | 32 | 0.25 | 5 eV | 2.2e4 | 7e7 to 1.6e9 | 5e9 to 1.2e11 | 3e5 | 1.6e15 to 3.7e16 | **4e13 to 9e14** |
| UEG, eps = 2% | 32 | 0.5 | 2 eV | 2.2e4 | 7e7 to 1.6e9 | 1e10 to 2e11 | 9e6 | 8e16 to 2e18 | 9e14 to 2e16 |
| UEG | 64 | 0.5 | 2 eV | 6.3e4 | 5e8 to 1e10 | 7e10 to 1.5e12 | 4e6 | 3e17 to 7e18 | 4e15 to 1e17 |
| H (bare protons) | 128 | 0.5 | 2 eV | 6.4e5 | 1e10 to 2.5e11 | 1.6e12 to 3.6e13 | 2e6 | 3e18 to 8e19 | 7e16 to 1.6e18 |
| H | 256 | 0.5 | 2 eV | 2.4e6 | 8e10 to 1.9e12 | 1.2e13 to 2.7e14 | 1e6 | 1e19 to 3e20 | 4e17 to 8e18 |
| H, high resolution | 128 | 0.5 | 0.5 eV | 6.4e5 | 1e10 to 2.5e11 | 3e12 to 7e13 | 9e6 | 3e19 to 6e20 | 5e17 to 1e19 |

These costs are per state point and per q-set. A (rho, T, Z) posterior needs 10 to 100 state points, which multiplies them by another 1e1 to 1e2.

Be and CH all-electron treatments are more expensive. The Be 1s orbital needs Delta of about 0.1 a0, so n_p rises by 1 to 2 and lambda by about 3 to 10x. Pseudopotentials would remove the bound-free physics that XRTS measures.

**Runtime.** With Babbush 2021's 170 us per Toffoli for one factory: 1e12 Toffoli is 5.4 years, 1e14 is 540 years, 1e16 is 5.4e4 years. At about 1e6 Toffoli/s (about 170 factories): 1e12 is 12 days, 1e14 is 3.2 years, 1e18 is 3.2e4 years. At a hypothetical later-FT rate of 1e8 Toffoli/s: 1e14 is 12 days, 1e16 is 3.2 years. Shots are independent, so wall-clock divides by the number of QPUs, but machine-years do not.

**Qubits.** 3*eta*n_p plus ancilla: about 500 to 800 logical qubits for eta = 32, and about 2700 to 3000 for eta = 128 (Rubin: 5650 for eta = 218 with the projectile). A 1-us-cycle surface code at d of about 25 to 30 needs roughly 1e6 to 1e7 physical qubits, including factories [order-of-magnitude, not sourced].

**NISQ.** Not plausible. The circuits need about 1e9 or more Toffoli-equivalent depth even for eta = 32. Fault tolerance is required.

### 3.2 Where the cost goes (lessons L3 and L6)
- **Measurement dominates.** Standard-quantum-limit shots are 1e5 to 1e7 per state point. The signal is a small, linear-response density modulation on a many-electron background. Heisenberg-limited amplitude estimation cuts the shot count by about 30 to 100x but needs a coherent (purified) thermal preparation.
- **State preparation is about 40 to 70% of G** (t_prep of 60 to 100 a.u. against t_max/2 of 17 to 43 a.u.). The cheap alternative, Rubin's Mermin-DFT determinant, is biased for S_ee. A determinant lacks the correlation hole, so under exact H it relaxes to a state whose energy is too high by about |E_c|. For the UEG at r_s = 2, E_c is about -0.045 Ha per electron [UNVERIFIED, recalled]. That excess heats the system by about 0.5 to 1 eV against T = 6.3 eV at theta = 0.5, a 8 to 16% temperature bias. This is the same size as the quantity XRTS diagnoses.
- **Precision scaling.** G scales as eta^(2 to 3) * N^(1/3) / Dw. Shots scale as N_t/(eps^2 * eta), with N_t proportional to 1/Dw, so S*G scales as roughly eta^(1 to 2)/(Dw^2 * eps^2). Halving the instrument resolution or halving eps each costs 4x.

### 3.3 Classical side and break-even (L1, L7)
- **Where the wall is.** Direct PIMC stops at theta <~ 0.5 for N of about 14 to 33 at r_s = 2 (Dornheim 2019). xi-extrapolation reaches N <= 1000 for static properties (arXiv:2311.08098) and gives free energies "down to half the Fermi temperature" (arXiv:2502.15288). The Taylor-xi work (arXiv:2509.11317) sets the limit by degeneracy through the Taylor radius of convergence. The classical-exact wall for F(q,tau) is therefore about theta < 0.5 at r_s of 1 to 4. Above it, PIMC F(q,tau) is quasi-exact at N = 30 to 1000.
- **Break-even criterion.** No quantum cost beats PIMC above theta of about 0.5: PIMC is polynomial there and costs about 1e3 to 1e5 CPU-hours per state point [estimate]. A quantum advantage is possible only for theta < about 0.5 and N >= 32. There the quantum cost is at least 4e13 Toffoli (UEG, eta = 32, 5 eV, AE) and about 1e17 to 1e19 for H at eta = 128.
- **Approximate classical methods remain in that region.** LR-TDDFT and Liouville-Lanczos with static LFCs taken from xi-PIMC (arXiv:2502.04921, 2510.01875), mixed stochastic TDDFT, and ground-state-anchored dielectric theory all still apply. As theta falls toward 0.25, the state approaches the ground-state UEG, and thermal corrections to S(q,w) at 2 to 5 eV resolution become small. The quantum computer then has to resolve differences between approximate theories and the truth that exceed the experimental error bar. No such named state point was found (audit Q3 is open).
- **Information test (Q1, L5).** Real-frequency theory adds information over ITCF analysis only where PIMC F(q,tau) is unavailable, because the measured spectrum can be deconvolved in the Laplace domain and compared with theory directly in tau (arXiv:2211.00579, 2604.25735). So the information gain and the classical wall occupy the same narrow region, theta < 0.5. Gawne et al. 2026 name the source-and-instrument function as the limiting error. This points to a model and instrument floor (L6): at present, solver error is unlikely to dominate the XRTS error budget. The 2x posterior-narrowing test is still unrun. It is a cheap classical test and must come first.
- **q-resolution (Q5).** At r_s = 2, q_min/k_F is 0.64 (eta = 32), 0.51 (eta = 64), 0.40 (eta = 128) and 0.32 (eta = 256). Backscatter XRTS (q about 4 k_F) and forward collective scattering (q about 0.4 to 1 k_F) are reachable. The smallest-q collective regime needs eta >= 128 or elongated or twisted cells, which raises cost by the eta-scaling above.

### 3.4 Scoop risk (Q6)
High. The Sandia group (Baczewski, Kononov, Pathak) and Google (Rubin, Babbush, Berry) already have first-quantized WDM stopping power (2023/24), conductivity (OSTI 10.2172/3363975, from the prior lens, not re-verified here) and a spectral-readout opacity protocol (arXiv:2607.02811, July 2026). S(q,w) is the next natural observable. My arXiv searches did not find a quantum XRTS or electronic S(q,w) paper. Searches run: "quantum algorithm dynamic structure factor electron gas", "quantum computer Thomson scattering", "quantum algorithm warm dense matter". Only Low 2211.09133 (Trotter-step complexity for the UEG), classical TDDFT and wave-packet DSF, and QMC analytic-continuation papers appeared.

## 4. Verdict and conditions for escalation

**WOUNDED.**
- Resource-killed for the practical target: H, Be or CH, eta >= 128, Dw <= 2 eV, 10 or more state points. S*G is 1e18 to 1e21, 6 to 9 orders above 1e12, and 1e2 to 1e5 years even at a hypothetical 1e8 Toffoli/s.
- The speedup is not quadratic. The separation is exponential in the sign-problem regime. But the constant factors (lambda about 1e4 to 1e6 Ha, C_BE about 3e3 to 3e4, t of about 100 a.u.), the linear-response shot noise and the thermal-state preparation dominate.
- **Surviving niche.** A UEG benchmark at eta of about 32, theta of about 0.25, r_s of 2 to 4, 5 eV resolution and 5% precision, with Heisenberg-limited estimation and a coherent microcanonical preparation. It costs 4e13 to 1e15 Toffoli: about 12 days to 4 months at 1e8 Toffoli/s, or 1.3 to 30 years at 1e6/s. That is a later-FT rate, not an early-FT demonstration.

It escalates only if all four of the following hold:
1. **Q1.** A classical posterior test shows that real-frequency S narrows (rho, T, Z) by 2x or more over ITCF at theta < 0.5, including the instrument and source functions.
2. **Q3.** A named state point exists where the best LR-TDDFT kernel, stochastic TDDFT and PIMC+AC (or Taylor-xi) disagree beyond experimental error.
3. A thermal preparation with a bounded cost exists. That means either an ETH or microcanonical argument with a known window error, or a Gibbs sampler with a numerically bounded mixing time on small eta.
4. The constant-factor inconsistency in Rubin 2024 (Table IV against lambda*C_BE, about 1.6e3x) is resolved in the favourable direction.

## 5. Query log (2026-09-28)
- WebSearch: budget exhausted (200/200); nothing returned.
- WebFetch arXiv abstract pages: 2308.12352 (plus html and PDF), 2607.02811, 2402.19113, 2509.11317 (x2), 2011.04149 (plus PDF), 1804.01505, 2303.18224, 2105.12767, 2301.01203, 2311.08098, 2502.15288, 2604.25735, 2211.00579, 2603.27212, 2510.01875, 2502.04921, 2004.06832, 1906.00635 (PDF).
- export.arxiv.org id_list query: HTTP 429. OpenAlex search: HTTP 429.
- Crossref: "fermion sign problem path integral Monte Carlo warm dense matter Dornheim".
- arXiv search pages: "Fermion sign problem ... quantum dots ultracold atoms warm dense matter"; "fictitious identical particles" (and a longer variant with no results); "quantum algorithm dynamic structure factor electron gas"; "quantum computer Thomson scattering"; "quantum algorithm warm dense matter".
- Local text extraction (pypdf) of the Rubin 2023/24, Babbush 2021 and Dornheim 2019 PDFs, to read the tables.
