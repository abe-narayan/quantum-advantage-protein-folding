# Audit C44 (resources / break-even): dense e-h plasma dynamics through the exciton Mott crossover in 2D TMDs

Date: 2026-09-28. Role: resource / break-even analyst. Status: COMPLETE.

**Verdict: WOUNDED. The headline output (absorption/gain spectra and an n_M(t) map) is KILLED on resources. A narrow scalar-observable remnant survives on resources alone, and its value is doubtful on model-floor grounds.**

Summary:
- **Speedup type.** The speedup is exponential in eta against exact correlated dynamics, so lesson L3 (quadratic speedups do not survive fault-tolerant overhead) does not apply.
- **Per-circuit cost (100-200 fs, first quantization).** A single circuit is FeMoco-class:
  - about 5e8-1e9 Toffoli at eta = 32;
  - 2-7e9 at eta = 64;
  - 1-4e10 at eta = 128;
  - 1.5-3e11 at eta = 256.
- **Logical qubits:** about 0.5-5e3.
- **Where the claim fails.** It fails at the output end, as in C41: measurement and sampling cost dominate.
  - The spectra the experiments report, differential absorption and gain across the exciton window, need about 1e4-1e5 QPE samples per (density, delay) point.
  - That is about 5e13-5e14 Toffoli per point at eta = 64: 16-160 years at 10 us/Toffoli.
  - A full n_M(t) map multiplies this by 200-500 (densities x delays x twists).
- **What survives the S x G <~ 1e12 rule.** Only one-body or pair-correlation scalars qualify: n(k), g_eh(r) or a pair "contact", at a single (density, delay) point, at eta <= 64, with S <= ~300, or with amplitude estimation on a purified initial state.
- **Break-even is set by accuracy, not cost.**
  - Against exact classical dynamics, break-even is eta of about 6 at a trivial 1e7 Toffoli, which is physically meaningless for a plasma.
  - Against the real competitors (G1-G2 / real-time GW / T-matrix NEGF, SBE, excitonic Bloch equations), there is no cost break-even at any size, because those run in CPU-hours to GPU-days.
  - Any advantage would be category 3 "accuracy-class at infeasible classical cost". It is conditional on the approximate classical methods being wrong by more than the model floor.
- **Model floor.** 2025-2026 literature puts phonons and intervalley scattering at the centre of the physics at the 100-fs scale (arXiv:2607.28417, 2607.18183), and the closed effective-mass e-h model omits both.
- **Hardware.** Not NISQ-plausible. Fault tolerance is required.

---

## 1. Query log (2026-09-28)

WebSearch was not used: the session budget was reported as exhausted in audit_C44_novelty.md. WebFetch was used instead.

1. arXiv abs 2105.12767 (Su et al., first quantization): OK.
2. arXiv abs 2301.01203 (Babbush et al., exact dynamics vs mean field): OK.
3. arXiv abs 2603.19007 (Eklund et al.): OK.
4. arXiv abs 2601.17167 (WS2 Mott, discontinuous): OK.
5. arXiv abs 2604.06897 (Mott without population inversion): OK.
6. arXiv abs 2512.03198 (Mittenzwey, Voigt, Knorr): OK.
7. Crossref query "Population inversion and giant bandgap renormalization in atomically thin WS2 layers": OK.
8. Crossref DOI 10.1038/s41467-017-01298-6 (Steinhoff 2017): OK.
9. Crossref query for Schluenzen PRL: HTTP 429. Switched to arXiv abs 1909.11489: OK.
10. arXiv API `all:"neural" AND all:"continuous space" AND all:"time-dependent" AND all:fermions`: 0 hits.
11. arXiv API `abs:"time-dependent" AND abs:"neural" AND abs:"many-electron"`: 2 hits (2511.12983, 2403.07447).
12. arXiv abs and HTML 2403.07447 (Nys et al., system sizes): OK.
13. arXiv abs 2511.12983 (Hou et al.): OK.
14. arXiv API `abs:"electron-hole" AND abs:"monte carlo" AND (monolayer OR TMD OR dichalcogenide)`: 1 hit (2304.09018, quadriexciton in bilayers; not dense-plasma).
15. OpenAlex "electron-hole liquid monolayer transition metal dichalcogenide quantum Monte Carlo": first attempt HTTP 429; retry OK. 4 hits, none a QMC calculation of a dense monolayer e-h plasma.
16. arXiv API `abs:"G1-G2" AND abs:scheme`: 10 hits (list in section 7).
17. arXiv abs 2606.10773 (δNEGF, N_b ~ 1e4): OK.
18. arXiv abs 2002.12717 (G1-G2 scheme): OK.
19. arXiv API `au:Perfetto AND au:Stefanucci AND exciton`: 20 hits (list in section 7).
20. arXiv abs 2607.28417 (phono-conversion in WSe2): OK.
21. arXiv abs 2109.15209 (real-time GW, Mott cascade): OK.
22. arXiv abs 2211.09133 (Trotter-step complexity): OK.
23. arXiv abs 2011.04149 (focus beyond quadratic): OK.
24. arXiv API `abs:"Mott" AND abs:exciton AND (WS2|WSe2|MoS2|MoSe2)`: 30 hits. Most are moiré or bilayer. Monolayer-relevant hits: 2007.11509 (MoS2), 2111.07887 (~5e12 cm^-2 at a lateral junction), 2003.12925, 2110.05272.

Local arithmetic: scratchpad script `c44.py` (order-of-magnitude only; no heavy computation).

---

## 2. Model and discretization (derived)

**Model.** Two-component (e, h) 2D effective-mass Hamiltonian with Rytova-Keldysh (RK) interaction:

V(q) = 2π e^2 / [q (ε_env + ρ0 q)]

- ρ0 = 2πχ_2D, about 4 nm for WS2. Berkelbach-type r0 is about 3.8 nm [value from memory, UNVERIFIED; the order of magnitude is standard].
- e^2 = 1.44 eV nm; ħ^2/(2 m0) = 0.0381 eV nm^2; ħ = 0.658 eV fs.
- m_e ≈ 0.30, m_h ≈ 0.40 (representative W-based TMD values [UNVERIFIED to 10%]).

**Cell.** N electrons and N holes, eta = 2N, per-species density n, so A = N/n.
- n = 1e12 cm^-2 = 0.01 nm^-2. With N = 32, L = 56.6 nm.
- n = 3e12: L = 32.7 nm (N = 32) and 46 nm (N = 64).
- n = 1e13: L = 17.9 nm (N = 32).

**Grid.** dx = 0.4 nm gives k_max = π/dx = 7.85 nm^-1.
- k_max is ≫ 1/a_X ≈ 0.7-1 nm^-1.
- The per-dimension kinetic cutoff is 7.8 eV for m = 0.3. This lies far above the range of validity of the effective-mass model, which ends around 0.2-0.5 eV where band nonparabolicity and the Q/Λ valleys set in. The model, not the grid, limits the UV.

**Register size.** n_p = ceil(log2(L/dx)) = 6-8 bits per dimension, so 12-16 qubits per particle.

**Flavours.** Spin-valley flavours (up to 4 for electrons and 2 for holes) are conserved labels in the flavour-diagonal RK model. Registers are assigned to flavours and antisymmetrized within each group, at zero extra qubit cost. Intervalley exchange and intervalley scattering break this and add terms.

**RK softening is favourable.** At large q, V(q) → e^2/(χ q^2) is 3D-Coulomb-like. The 2D real-space potential is only logarithmic at r ≪ ρ0, so there is no Coulomb cusp. Plane-wave convergence is therefore faster than for 3D Coulomb (contrast C41).

## 3. Block-encoding normalization λ (derived)

**λ_V per pair (plane-wave LCU, Su et al. style).**

λ_V,pair = (1/A) Σ_{q≠0} V(q) → ∫ d^2q/(2π)^2 V(q) = (e^2/ρ0) ln(1 + ρ0 k_max/ε_env)

- This is only logarithmic in the cutoff.
- With ρ0 = 4 nm and k_max = 7.85 nm^-1: 0.36 eV × ln(32.4) = **1.25 eV** for a suspended layer (ε = 1), and 0.36 × ln(8.0) = **0.75 eV** for hBN encapsulation (ε ≈ 4.5).

**λ_V totals.** λ_V = [eta(eta-1)/2] × λ_V,pair. The sign of e-e, h-h and e-h terms does not matter for λ.

| eta | λ_V at ε=1 (eV) | λ_V at ε=4.5 (eV) |
|---|---|---|
| 32 | 620 | 370 |
| 64 | 2,520 | 1,510 |
| 128 | 10,200 | 6,080 |
| 256 | 40,800 | 24,500 |

**λ_T.** λ_T ≈ eta × (2 dims × ħ^2 k_max^2/2m) ≈ eta × 16 eV, i.e. about 1,000 eV at eta = 64. Kinetic energy is diagonal in momentum and can be fast-forwarded in the interaction picture (Dyson series, Low-Wiebe; the method is cited in audit_C41), so only λ_V drives the step count.

**The LCU overhead factor is large.** The physically relevant energy scale is eta × (0.05-0.3 eV), i.e. about 3-20 eV at eta = 64. λ_V overestimates it by about 100-1,000×, because λ_V counts all pairs at the UV cutoff. Trotter with commutator scaling or low-energy-subspace bounds could recover part of this. Low, Su, Tong, Tran (PRX Quantum 4, 020323, 2023; arXiv:2211.09133 [VERIFIED]) give first-quantized plane-wave Trotter steps with gate complexity (eta^{1/3} n^{1/3} + n^{2/3}/eta^{2/3}) n^{1+o(1)}. A 10-100× reduction is plausible but has not been quantified here.

## 4. Per-circuit Toffoli count (dynamics to t_d)

**Step count.** Steps ≈ 1.3 λ_V t/ħ (qubitization plus interaction-picture overhead).

**Toffolis per step.** C_step ≈ 4 × eta × 2n_p (controlled swaps selecting particles i and j) + about 3e3 (RK-weighted ν-state preparation, arithmetic, reflections). This matches the Su et al. structure; their abstract scaling for the second algorithm is Õ(eta^{8/3} N^{1/3} t). Result: C_step ≈ 4.5e3 at eta = 32, 6.6e3 at eta = 64, 1.0e4 at eta = 128 and 1.9e4 at eta = 256.

| eta (N per species) | ε_env | λ_V (eV) | t (fs) | steps | Toffoli/circuit | logical qubits (system + ~300-600 ancilla) |
|---|---|---|---|---|---|---|
| 6 (3) | 1 | 19 | 100 | 3.7e3 | **1.2e7** | ~100 + ancilla |
| 32 (16) | 4.5 / 1 | 370 / 620 | 100-200 | 7e4-2.5e5 | **3e8-1.1e9** | 384 → ~0.7-1e3 |
| 64 (32) | 4.5 / 1 | 1.5e3 / 2.5e3 | 100-200 | 3e5-1e6 | **2e9-6.6e9** | 896 → ~1.2-1.5e3 |
| 128 (64) | 4.5 / 1 | 6.1e3 / 1.0e4 | 100-200 | 1.2e6-4e6 | **1.2e10-4e10** | 1,792 → ~2.2-2.4e3 |
| 256 (128) | 1 | 4.1e4 | 100-200 | 8e6-1.6e7 | **1.6e11-3.1e11** | 4,096 → ~4.5e3 |

**Check against the candidate's estimate** of about 1e3 logical qubits and 1e8-1e10 Toffoli per circuit:
- It is consistent for eta ≤ 64.
- It is optimistic by 2-4× for eta = 128 at 200 fs.
- It is off by 15-30× for eta = 256, which section 6 argues may be needed at high density with 4+2 flavours.

**Initial-state preparation.** An antisymmetrized product of plane-wave Slater determinants costs about O(eta log eta · n_p), roughly 1e4-1e5 Toffoli, which is negligible. The claim "no Gibbs prep" is only partly true:
- A pump-created incoherent distribution f_e(k), f_h(k) is a mixed state, diagonal in occupation. It must be sampled as random determinants, one per shot. That is fine for plain sampling but incompatible with amplitude estimation unless the state is purified, which doubles the register.
- Resonant pumping, as in the 2604.06897 experiment, creates a coherent interband polarization. That is a superposition of pair numbers, which fixed-eta first quantization does not represent natively. It would need a number register plus controlled registers.

**Wall-clock per circuit.** Assumptions:
- Toffoli time: 170 us is one Gidney-Fowler CCZ factory at d ≈ 31 with a 1 us cycle. The factory's 5.5d cycles per CCZ are taken from arXiv:1812.01238 as verified in audit_C41. 10 us assumes multiple factories; 1 us is optimistic.
- Physical qubits: about 2d^2 ≈ 1.7e3 per logical qubit plus factories, giving **2-4e6 physical qubits for eta = 64-128**. This is comparable to the THC FeMoco estimate of about 4e6 physical qubits (Lee et al. arXiv:2011.03494, as verified in audit_C41).

| Toffoli | 1 us | 10 us | 170 us |
|---|---|---|---|
| 3e9 (eta=64, 100 fs) | 50 min | 8.3 h | 5.9 d |
| 4e10 (eta=128, 200 fs) | 11 h | 4.6 d | 79 d |
| 1e12 | 11.6 d | 116 d | 5.4 yr |
| 5e13 | 1.6 yr | 16 yr | 270 yr |
| 5e14 | 16 yr | 160 yr | 2,700 yr |

## 5. Readout, shot budget, and the S×G <~ 1e12 rule (audit question 5)

| Observable | Readout | Samples S per (density, delay) | G per sample (eta=64) | S×G | Rule |
|---|---|---|---|---|---|
| f_e(k,t), f_h(k,t) (one-body) | QFT every register and measure; eta momenta per shot | 1e2-1e3 (20 radial bins at ~1-3%; twist average ×4-10 adds 1 order) | 3e9 | 3e11-3e12 (×10 for twists) | borderline pass |
| g_eh(r,t), contact / "exciton-like pair fraction" | position-basis measurement; N^2 pair distances per shot | 1e2-1e3 | 3e9 | 3e11-3e12 | borderline pass. The observable is ill-defined as an "exciton fraction" in the crossover and is not what experiments measure. |
| Exciton-window oscillator-strength bleaching (integrated) | local-pair creation P†, then QPE at 10 meV (2.4-4e5 steps ≈ 2.6e9 Toffoli), histogram window weight | ~1e4 binomial (p≈0.1, 3% rel.); ~3e2 with amplitude estimation on a purified state | 5-6e9 | 5e13 (plain); ~1.5e12 (AE) | fail ×50 (plain); borderline (AE) |
| Full absorption/gain spectrum, 0.5 eV window, 10 meV bins, gain = difference of absorption (P†) and emission (P) histograms | as above, two signs | 1e5-2e5; more near transparency, where gain is a small difference | 5-6e9 | **5e14-1e15** | **fail ×500-1,000** |
| THz σ(ω) | current-current Hadamard test over ~20-50 τ points, or finite-field linear response (signal ∝ field; shot-noise-limited) | ≥1e5 | 3-6e9 | ≥3e14 | fail |
| n_M(t) map | spectra × 6-10 densities × 3-5 delays × 4-10 twists | — | — | **1e17-5e18** | fail by 5-6 orders |

**Resolution argument (lesson L5).** At the densities of interest, linewidths are tens of meV, so a spectral resolution of about 10 meV is sufficient; ħ/10 meV ≈ 66 fs of QPE evolution. A 10 meV resolution with broad lines does not reduce the sample count, because the bins are set by the width of the features and the gain signal is a small difference near transparency.

**Conclusion.** Measurement and sampling dominate end-to-end cost by 2-5 orders over a single circuit. This is the same failure structure as C41. The headline outputs the candidate lists (time-resolved absorption/gain spectrum, THz conductivity, n_M(t)) all fail S×G <~ 1e12. Only single-point scalar one-body or pair-correlation observables at eta ≤ 64 pass.

## 6. Finite size vs cost (audit question 3)

**Level spacing.** Single-particle spacing is ħ^2(2π/L)^2/2m (m = 0.3):

| Cell | L (nm) | Spacing (meV) | Recurrence 2πħ/ΔE |
|---|---|---|---|
| eta=64, n=1e12 | 57 | 1.6 | ~2.6 ps (fine) |
| eta=64, n=3e12 | 33 | 4.7 | ~0.9 ps |
| eta=64, n=1e13 | 18 | 15.7 | **~260 fs, comparable to the 100-200 fs window and to the linewidths** |
| eta=128, n=1e13 | 25 | 7.8 | ~530 fs |

**Flavour granularity.** With 4 electron flavours, N = 32 means about 8 electrons per flavour, i.e. 1-2 filled 2D shells, so f(k) per flavour is represented on about 9 k-points. At n = 1e12 the thermal k at 300 K (0.45 nm^-1) spans only about 4 grid spacings (Δk = 0.11 nm^-1). Twist averaging (×4-10 independent circuits) and N ≥ 64 per species are needed at the high-density end. That means eta = 128-256 and G ≈ 1e10-3e11 per circuit.

**Screening.** Static screening appears adequately captured: 2π/L = 0.11-0.35 nm^-1 is small compared with Debye/Thomas-Fermi screening wavevectors of about 1-7 nm^-1 (derived order-of-magnitude estimate). Low-q plasmon dynamics are discretized coarsely, however.

**Net.** eta ≤ 128 can hold the crossover's short-range physics (L/a_X ≳ 15). For time-dependent spectra at n ≳ 5e12, a finite-size error of 5-15 meV is likely unless eta ≥ 128 with twist averaging. This pushes cost up by 3-10× beyond the eta = 64 figures.

## 7. Classical cost and break-even

**Exact classical dynamics (the "exponential" comparator).**
- eta = 4 (2e+2h), 2D, 64^2 grid, centre of mass removed: 64^6 ≈ 7e10 amplitudes (~1 TB). About 1e5 steps with FFTs gives ~1e17-1e18 flop, which is feasible on HPC.
- eta = 6: 64^10 ≈ 1e18 amplitudes, which is infeasible.
- **The exact-dynamics break-even is therefore eta ≈ 6, at a quantum cost of about 1.2e7 Toffoli** (minutes on an FT machine). This is scientifically empty: a 3e+3h "plasma" has no Mott physics and finite-size effects dominate.

**Approximate classical methods (the real comparators).** All run in CPU-hours to GPU-days:
- G1-G2 NEGF has time-linear scaling (Schluenzen, Joost, Bonitz PRL 124, 076601 (2020), arXiv:1909.11489 [VERIFIED]). Its CPU scaling carries no more than an additional factor N_b over GKBA, and it supports second Born, GW, T-matrix and screened ladder (Joost et al. PRB 101, 245101 (2020), arXiv:2002.12717 [VERIFIED]).
- δNEGF (quantum-fluctuation formulation) extends dynamical GW and T-matrix to N_b ~ 1e4 with linear-in-N_t scaling (Schroedter, Bonitz, Joost, arXiv:2606.10773 [VERIFIED], June 2026).
- Real-time GW on Bloch states for 2D materials already produces a "self-sustained screening cascade leading to the Mott transition of coherent excitons" (Perfetto, Pavlyukh, Stefanucci PRL 128, 016801, arXiv:2109.15209 [VERIFIED]).
- The same group's real-time ab initio simulations are compared directly with ~100 fs exciton quenching and absent gain in monolayer TMD experiments (Dogadov ... Stefanucci, Perfetto, arXiv:2604.06897 [VERIFIED abstract]).
- Excitonic Heisenberg-equation theory is restricted to below the Mott transition (Mittenzwey, Voigt, Knorr arXiv:2512.03198 [VERIFIED]).

**No cost break-even exists at any size against these methods.** Quantum costs are hours to years against classical hours to days. The only possible claim is category 3 in accuracy class: exact dynamics of the model where the approximate methods cannot be converged. That claim requires:
- (a) a multi-family classical disagreement (GW vs T-matrix vs δNEGF vs SBE) on a scalar observable that passes S×G <~ 1e12;
- (b) that disagreement exceeding the model floor.

Neither was established in this audit. Question 1, the multi-family wall, belongs to the classical audit. No paper found here reports GW-G1G2 vs T-matrix-G1G2 vs SBE disagreement on n_M for a named substrate.

**Continuum NQS dynamics (audit question 6).**
- Nys, Pescia, Sinibaldi, Carleo (Nat Commun 15, 9404 (2024), arXiv:2403.07447 [VERIFIED]) simulate 2D harmonic quantum dots with 6 and 18 electrons after an interaction quench, 30 fermions in 1D, and H2 in a laser field. All are single-component and confined.
- Hou et al. arXiv:2511.12983 [VERIFIED abstract] report "excellent agreement" on 5 small benchmarks and note limitations for continuum states.
- In the sources searched, no time-dependent NQS or tensor-network study reaches eta ~ 64 two-component periodic 2D continuum dynamics with controlled error. On current evidence, the classical exact-quality wall at eta ~ 64 holds. This is scoped: two arXiv API queries plus one OpenAlex query.

**Equilibrium QMC for the dense monolayer e-h plasma.** The arXiv API and OpenAlex queries above found no PIMC/DMC study of the dense monolayer e-h plasma or the Mott crossover. The only hit was a quadriexciton QMC in bilayers (arXiv:2304.09018). This is a gap but is not decisive: equilibrium statics are not the proposed output.

## 8. Model floor vs solver error (audit question 2, lesson L6), resource implications

**Phonons.**
- Perfetto, Fukuda, ..., Dani, Stefanucci (arXiv:2607.28417 [VERIFIED], July 2026) report that in monolayer WSe2 the conversion of free carriers into excitons is phonon-driven via a "sequential relaxation cascade", with valley multiplicity, large-momentum phonon emission and spin-flip processes controlling efficiency.
- arXiv:2607.18183 [VERIFIED listing summary only] reports that intervalley carrier-phonon scattering dominates in WSe2.
- A closed electronic e-h model cannot dissipate binding energy except into other carriers. Its "exciton formation" in 100-200 fs is qualitatively different physics.

**Adding phonons in first quantization costs a great deal.** It needs bosonic mode registers, at least tens of q-points × several branches × log2(n_max) qubits, plus e-ph coupling terms in λ. This multiplies both qubits and λ. The exact quantum solution of the phonon-free model sits below a model floor that the existing classical ab initio NEGF already partly includes (2604.06897, 2607.28417).

**Valleys and bands.** Q/Λ valleys and nonparabolicity at the pump excess energy are cheap in first quantization: an arbitrary diagonal dispersion T(k) is a phase. Bloch form factors in the interaction and intervalley scattering break the simple plane-wave Coulomb LCU, so λ and C_step grow by an unquantified factor.

**Substrate screening.** Screening enters λ only logarithmically, which is cheap. Dynamical substrate screening (substrate phonons, as in Steinhoff 2017-type environment engineering; Nat Commun 8, 1166 [Crossref VERIFIED title/authors]) is not in the static RK model.

**Resource consequence.** Making the model faithful enough that solver error dominates model error likely costs ≥10× in λ·C_step and ≥2× in qubits. That pushes single scalar observables at eta = 64 above 1e12-1e13 Toffoli.

## 9. NISQ vs fault tolerance

- **Not NISQ-plausible.** First-quantized plane-wave dynamics needs 0.4-4.5e3 logical qubits and coherent arithmetic of 1e8-1e11 Toffolis.
- **Second-quantized alternative.** A dual-basis grid for 2 species × up to 4 flavours × 64^2 sites is about 3e4 qubits, and still needs deep circuits.
- **Analog simulation.** No analog platform with a two-component Fermi mixture, tunable mass ratio and 2D long-range RK interaction was identified.
- **Fault tolerance is required.** The earliest scale is late-FT machines of about 2-4e6 physical qubits for a single eta = 64-128 circuit. Any spectrum-level output requires fleets.

## 10. Answers to the audit questions (resource view)

1. **Multi-family wall (Q1).** No named substrate/density point with GW-G1G2 vs T-matrix-G1G2 vs SBE disagreement exceeding the experimental scatter was found here. The experimental n_M values seen in the listing are ~5e12 cm^-2 at a lateral junction (2111.07887) and ~0.8e12 for interlayer e-h fluids in bilayers (2306.13265, 2309.14940; a different system). Open; this belongs to the classical audit.
2. **Model floor (Q2).** Phonon-driven exciton formation and intervalley scattering are primary, per 2025-2026 ab initio plus experimental work. The model floor likely exceeds the solver disagreement for the phonon-free model. Unresolved, adverse.
3. **Finite size (Q3).** eta = 64 works at n ≤ 3e12. At n ≈ 1e13, level spacing (~16 meV) and recurrence (~260 fs) are comparable to the window, so eta ≥ 128 plus twist averaging is needed (G ≈ 1-4e10 per circuit, ×4-10 circuits).
4. **L5, resolvable differences (Q4).** Resolving tens-of-meV linewidths does not demand high resolution but does demand many samples; gain near transparency is a small difference. Spectra fail S×G by 2-3 orders.
5. **Candidate resource estimate (Q5).**
   - The per-circuit estimate holds for eta ≤ 64 and is 2-30× optimistic beyond that.
   - S×G <~ 1e12 holds only for single-point one-body or pair-correlation scalars at eta ≤ 64 (S ≈ 1e2-1e3).
   - It fails for exciton bleaching without amplitude estimation (5e13) and for spectra (5e14-1e15).
   - It fails for n_M(t) maps by 5-6 orders.
6. **Continuum NQS / tensor methods at eta ~ 64 (Q6).** Not found. The best verified continuum 2D t-VMC case is 18 electrons in a single-component dot (2403.07447). The exact-quality classical wall at eta ~ 64 likely holds. The approximate classical competitors are cheap and already used against experiment.

## 11. Verdict

**WOUNDED.**
- **Killed:** the headline "time-resolved absorption/gain spectrum, THz conductivity and n_M(t)" category-3/4 claim. Measurement and sampling dominate, at 5e14-5e18 Toffolis.
- **Retained as a narrow resource-feasible remnant:** a single category-3 scalar benchmark, for example the e-h pair-correlation contact g_eh(r ≲ a_X, t) or f_e(k, t) at one density near 3e12 cm^-2 and one delay ≤ 100 fs, at eta = 64 with twist averaging. Cost is about 3e11-3e12 Toffoli: days to a year on one late-FT machine.
- **Conditions on the remnant.** It counts only if the classical audit demonstrates a multi-family disagreement (G1-G2 GW / T-matrix / δNEGF / NQS) on that scalar that exceeds the phonon and valley model floor. It is also not directly an experimental observable, which weakens its practical relevance.
- **Recommendation:** rank below candidates whose headline observable passes S×G <~ 1e12.

## 12. Citations (verification status)

**Verified in this audit:**
- Su, Berry, Wiebe, Rubin, Babbush, "Fault-tolerant quantum simulations of chemistry in first quantization", PRX Quantum 2, 040332 (2021), arXiv:2105.12767 [VERIFIED].
- Babbush et al., "Quantum simulation of exact electron dynamics can be more efficient than classical mean-field methods", Nat Commun 14, 4058 (2023), arXiv:2301.01203 [VERIFIED].
- Eklund, Tikku, Sinnott, Huggins, Low, Berry, Kassal, "End-to-End Simulation of Chemical Dynamics on a Quantum Computer", arXiv:2603.19007 (Mar 2026) [VERIFIED; the abstract gives no numeric resources].
- Low, Su, Tong, Tran, "On the complexity of implementing Trotter steps", PRX Quantum 4, 020323 (2023), arXiv:2211.09133 [VERIFIED].
- Babbush, McClean, Newman, Gidney, Boixo, Neven, "Focus beyond quadratic speedups...", PRX Quantum 2, 010103 (2021), arXiv:2011.04149 [VERIFIED].
- Mohapatra, Palato, ..., Stähler, Gierster, "Discontinuous character of the ultrafast exciton Mott transition in monolayer WS2", arXiv:2601.17167 (Jan 2026) [VERIFIED; plasma decays to excitons with 0.65 ps].
- Dogadov, ..., Cerullo, Dal Conte, Stefanucci, Perfetto, "Excitonic Mott transition without population inversion", arXiv:2604.06897 (Apr 2026) [VERIFIED; exciton quenched within ~100 fs, no gain, real-time ab initio simulations].
- Mittenzwey, Voigt, Knorr, arXiv:2512.03198 [VERIFIED; below-Mott excitonic theory].
- Chernikov et al., "Population inversion and giant bandgap renormalization in atomically thin WS2 layers", Nat Photon 2015, doi:10.1038/nphoton.2015.104 [VERIFIED via Crossref; the density threshold value is not verified here].
- Steinhoff, Florian, Rösner, Schönhoff, Wehling, Jahnke, "Exciton fission in monolayer transition metal dichalcogenide semiconductors", Nat Commun 8 (2017), doi:10.1038/s41467-017-01298-6 [VERIFIED via Crossref].
- Schluenzen, Joost, Bonitz, PRL 124, 076601 (2020), arXiv:1909.11489 [VERIFIED].
- Joost, Schlünzen, Bonitz, PRB 101, 245101 (2020), arXiv:2002.12717 [VERIFIED].
- Schroedter, Bonitz, Joost, "Nonequilibrium Green Functions Simulations for Large Correlated Systems", arXiv:2606.10773 (Jun 2026) [VERIFIED].
- Perfetto, Pavlyukh, Stefanucci, "Real-time GW: toward an ab initio description of the ultrafast carrier and exciton dynamics in two-dimensional materials", PRL 128, 016801, arXiv:2109.15209 [VERIFIED].
- Perfetto, Fukuda, ..., Dani, Stefanucci, "Quasiparticle phono-conversion: filming carriers coalescing into excitons", arXiv:2607.28417 (Jul 2026) [VERIFIED].
- arXiv:2607.18183, "Excitonic effects in the photocarriers dynamics of two-dimensional materials" (Jul 2026) [listing-level only; abstract summary not independently fetched].
- Nys, Pescia, Sinibaldi, Carleo, Nat Commun 15, 9404 (2024), arXiv:2403.07447 [VERIFIED incl. system sizes from the HTML].
- Hou, Liu, Zhang, Ye, Wang, Wang, arXiv:2511.12983 [VERIFIED abstract].
- Malosso et al., arXiv:2304.09018 [listing-level].
- Yuan et al., arXiv:2111.07887 [listing-level, ~5e12].
- Yu et al., arXiv:2007.11509 [listing-level].

**Relied on as verified in audit_C41_resources.md:** Gidney-Fowler CCZ factory arXiv:1812.01238; Lee et al. THC arXiv:2011.03494; Low-Wiebe interaction picture arXiv:1805.00675.

**UNVERIFIED (from memory, used only for order-of-magnitude parameters):** WS2 r0 ≈ 3.8 nm; m_e ≈ 0.3 and m_h ≈ 0.4; exciton Bohr radius 1-2 nm (this value is given in the task).
