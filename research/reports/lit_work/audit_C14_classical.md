# Audit C14 (classical adversary): finite-T polarized S(q,w) of 3D DO pi-flux QSI (Ce2Zr2O7 / Ce2Sn2O7 / Ce2Hf2O7)

Date: 2026-09-28. Role: classical adversary. Status: COMPLETE.
Verdict: **WOUNDED (severe).** In the formulation as written (L=3, T=50 mK, decision scored against the Gao et al. 2404.04207 polarized data), C14 fails the decision-flip filter (L5) and very probably the model-floor filter (L6). The classical wall itself is real: no controlled classical method exists for pi-flux finite-T dynamics beyond 32 sites. What fails is that the wall does not sit where the current decision is made. It is not KILLED because no classical method convincingly computes the decision-relevant quantity, the resolution-integrated polarized quasielastic weight at T = 0.07 Jx in the pi-flux sector. Instead the decision is set by data degeneracy and sample disorder, not by the solver. The cheapest kill experiment (section 7) would settle this in days.

---

## 1. What the decision-relevant data actually are (the Gao et al. 2024 dataset)

Source: Gao, Desrochers, Tam, Steffens, Hiess, Su, Cheong, Kim, Dai, arXiv:2404.04207, Nature Physics (2025), doi:10.1038/s41567-025-02922-9 [VERIFIED abs + full-text PDF read].

- Instrument: ThALES cold triple-axis spectrometer at ILL, T = 50 mK. "For Ef = 3.23 meV, the instrumental energy resolution is about 0.065 meV at FWHM. For Ef = 2.52 meV, the energy resolution is 0.042 meV at FWHM."
- Data volume: energy scans at 3 Q points, Q-scans at E = 0+-0.03 and 0.1+-0.03 meV, and repeated points at 5 Q. At the elastic position "the intrinsic magnetic signal is about 10% of the nonmagnetic scattering."
- Theory used: GMFT spinons plus Gaussian QED photons, "effectively decoupled". The photon speed is a FREE parameter, capped from above by a heat-capacity argument (hbar c/a0 < 2 kB*50 mK ≈ 0.009 meV).
- The fit is degenerate: "the goodness of fit is very shallow as a function of c_QSI. An extended range of values of c_QSI and theta yields very reasonable and similar fits ... c_QSI and theta cannot be uniquely determined with the energy scans". The acceptable range is hbar c/a0 ∈ [0.0004, 0.0028] meV and theta ∈ [0.05pi, 0.12pi]. "theta is the most uncertain ... It remains unclear to what extent this quantitative comparison ... is accurate."
- Best fit: Jx = 0.076 meV, J+- = 0.021 meV, "approximately 1.2 times the ones in Ref. 20 [Smith PRX 2022] (i.e., the ratio J+-/Jx is the same)".
- How 0-flux was excluded: qualitatively. pi-flux spinons give "three inelastic spinon peaks", while 0-flux gives "a broad inelastic continuum with a single local maximum". The GMFT continuum position "gives good agreement ... with the QMC results of Ref. 46 for 0-QSI and the 32-site ED results of Ref. 28 for pi-QSI". Ref 46 is Huang, Deng, Wan, Meng PRL 120, 167202 (2018); Ref 28 is Hosoi et al. PRL 129, 097202 (2022). Both are cited from the reference list of 2404.04207.
- The discriminator between pi-D-QSI and pi-O-QSI is the presence of a quasielastic photon signal: "photon detection is only possible if the ground state is pi-D-QSI, not pi-O-QSI". The authors themselves ask for "future confirmation through higher-resolution measurements of the quasielastic signal and identification of its temperature dependence."
- Disorder: "there is a 4% anti-site disorder of Ce and Zr from X-ray diffraction". The authors argue that this disorder cannot produce a Q- and polarization-dependent signal.

Follow-up: Gao, Zhou, Zhang, Podlesnyak, Cheong, Kim, Dai, arXiv:2601.03202 (2026-01-06) [VERIFIED abs+html]. CNCS-type data with Ei = 3.32 meV and "elastic energy resolution of approximately 0.1 meV". The photon window is E < 0.05 meV and spinons sit at 0.05-0.10 meV. Theory is GMFT plus ED on a **16-site** cluster at T = 0 with parameters (Jxx, Jyy, Jzz, theta) = (0.063, 0.062, 0.011 meV, 0.2pi). The authors state that "the photon weight on the 16-site cluster should therefore be regarded as a finite-size artifact" and that they "adopted a larger mixing angle to partially compensate for this finite-size underestimation."

### Timescale implied by the data (my arithmetic, hbar = 0.6582 meV ps)
| quantity | value |
|---|---|
| hbar/Jx (Jx = 0.063 meV) | 10.4 ps |
| Gaussian resolution FWHM 0.042 / 0.065 / 0.1 meV -> 3 sigma_t | 111 / 71 / 46 ps = **10.6 / 6.8 / 4.5 hbar/Jx = 3.5 / 2.3 / 1.5 hbar/J+-** |
| photon period at hbar c/a0 = 0.0028 meV | 1477 ps = 141 hbar/Jx |
| kB T at 50 mK | 0.0043 meV = 0.068 Jx |
| 12 J+-^3/J\|\|^2 (Gao fit values) | 0.019 meV = 0.22 K |
| Boltzmann factor for a 0.05 meV two-spinon pair at 50 mK | 9e-6 |
| lowest photon mode hbar c (2pi/L a0), c = 0.0028: L = 2, 3, 6, 10 | 0.0088, 0.0059, 0.0029, 0.0018 meV |

**Consequence 1 (L5, information vs computation).** At current resolution the correlator needs t_max of only about 5-11 hbar/Jx, or 1.5-3.5 hbar/J+-, not the ~50/J+- the candidate proposes. The photon itself (0.0028 meV) is about 15-25x below resolution and appears as a resolution-limited Gaussian at E = 0. The long-time, photon-resolving regime where real-time 3D entanglement growth would matter carries no information in any existing Ce2Zr2O7 dataset. This repeats the protein-echo lesson: the hardness lies beyond the informative horizon.

**Consequence 2 (finite size in the quantum target).** At L = 3 the lowest photon mode (0.0059 meV) is ABOVE kB T (0.0043 meV). An L = 3 simulation at 50 mK therefore thermally freezes out exactly the photon modes whose thermal (Rayleigh-Jeans) occupation produces the quasielastic weight that separates pi-D from pi-O. To make the lowest photon mode fall below kB T you need L >= 5 (N >= 2000 spins) at the fitted c. The L = 3 decision version is biased in the decisive observable, so the quantum resource target has to move to N ~ 2000-3500 spins.

**Consequence 3 (the hardness is the Gibbs state, not the dynamics).** Because t_max is short, the resolution-convolved lineshape at a few (q, E) points is largely fixed by low-order frequency moments. Those are thermal equal-time expectation values: S(q), the first-moment sum rule (a bond-energy expectation), and a few nested commutators. The classically hard object is the T = 0.07 Jx Gibbs state in the sign-problem sector, not "real-time entanglement growth in 3D". The quantum mechanism as stated therefore misidentifies the bottleneck. A candidate aimed at the bottleneck would be quantum Gibbs-state preparation, i.e. a thermodynamic target. See the note in section 8.

---

## 2. Classical state of the art, with demonstrated sizes

| method | sector | demonstrated scale / accuracy | source |
|---|---|---|---|
| SSE/multi-directed-loop QMC + SAC | 0-flux only (J+- > 0) | L = 4 (4 x 4^3 = 256 sites), S(q,w) via SAC; "where most QSI candidate materials reside and QMC encounters a sign problem" | Zhou, Zhou, Desrochers, Kim, Meng arXiv:2510.14813 [VERIFIED html quote] |
| QMC, 0-flux dynamics | 0-flux | photon:spinon weight ratio 1-4 orders of magnitude | Huang et al. PRL 120, 167202 (2018) [cited via 2404.04207 ref list] |
| QMC, 0-flux + vacancies | sign-free sector | "large-scale, unbiased" QMC + ED; 2% dilution dominates QSI dynamics | Sanders, Naik, Hallen, Schafer arXiv:2609.28643 [VERIFIED abs] |
| ED / FTLM | both | 16-site (2510.14813, 2601.03202), 32-site pi-QSI (Hosoi PRL 2022, per 2404.04207); 16-site has "shorter four-site spin-flip loop that winds around the boundary" | [VERIFIED] |
| GMFT (+ Gaussian QED) | both | analytic, infinite size; fits data with free c, theta | 2301.05240 (PRL 132, 066502), 2406.18650, 2502.14067 [VERIFIED listings] |
| SCEBR | both, finite T | spinon bandwidth reduction with T "consistent with previous QMC" | Desrochers & Kim arXiv:2401.09551, PRB 109, 144410 (2024) [VERIFIED abs] |
| Schwinger-boson / fermionic partons | both | dynamical structure factors, uncontrolled | 2112.00014, 2312.03106 [VERIFIED listings] |
| PFFRG / PMFRG | sign-free by construction | PFFRG polarized cross sections for DO XYZ (static); PMFRG XXZ phase diagram "down to temperatures two orders of magnitude smaller than the spin interactions", checked against QMC in 0-flux | Chern et al. 2311.04269; Schaden, Gonzalez, Reuther 2412.14773 [VERIFIED abs] |
| NLCE (4th order) | both | thermodynamic fits to Cp above ~0.5 K; equal-time diffuse S(q) at 0.05 K | Smith et al. 2108.01217 (PRX 12, 021015), 2407.07640 (PRX 15, 021033) [VERIFIED abs] |
| classical / semiclassical MD | both | used for Ce2Zr2O7 in field (Smith PRB 108, 054438); ED vs MD contrast (Hosoi) | 2306.13183, 2201.00828 [VERIFIED abs] |
| monopole in classical ice background (ED + Husimi cactus) | 0-flux | analytic two-monopole DOS | Udagawa & Moessner arXiv:1811.00199 [VERIFIED listing] |
| 3D BP tensor networks | annealing quench | hundreds of qubits, 3D; Science 392, 868 (2026) | Tindall et al. arXiv:2503.05693 [VERIFIED abs] |
| t-VMC Jastrow-Feenberg | annealing quench | 3D diamond up to 128 spins; D-Wave biclique instance matched | Mauron & Carleo 2503.08247; Wiersema 2609.01719 [VERIFIED abs] |
| NQS / VMC on pyrochlore | ground states only | Heisenberg pyrochlore up to 108 spins; chiral QSL VMC | 2101.08787, 2311.11561, 2604.11880 [VERIFIED listings] |
| sign-free QMC for pi-flux | none found | arXiv query (pi-flux or frustrated transverse) AND Monte Carlo AND (ice or pyrochlore) returned only classical MC/MD (Taillefumier 1705.00148) | query Q10 |

Adversarial assessment of the question: "can 3D BP-TN, t-VMC or NQS reach L = 3 at t ~ 50/J+-?"
- No such demonstration exists in any source searched (query Q8: 18 hits, no 3D QSI dynamics, no finite-T 3D QSL correlators). The D-Wave-closing methods simulate a quench from a product state over ~ns annealing times with modest entanglement. They have not been applied to thermal correlators of a loop-coherent U(1) liquid.
- There is a structural reason BP-TN is weak here. pi-flux is a hexagon-loop interference phase, and plain BP treats the environment as tree-like. Loop-corrected BP would be needed at the leading order of the physics. This point favours the quantum side.
- The adversary's counterpoint is that at the t_max the data actually need (<= 3.5/J+-), the time-evolution part is short. Any method that gets the 50 mK Gibbs state right, even approximately, gets the lineshape. The live question is therefore 3D pi-flux Gibbs states at T ~ 0.07 J, not long-time dynamics. PMFRG claims good performance down to T ~ 0.01 J with a sign-free construction, but it is uncontrolled and checked only in 0-flux.

Where classical computation fails, with evidence:
(a) Quantitative pi-flux S(q,w) at N > 32 and T < ~0.1 Jx. No controlled method exists: QMC has a sign problem (verified quote), ED stops at 32, and GMFT/SCEBR/partons are uncontrolled.
(b) The photon speed c for J+-/J|| ≈ -0.28 in pi-flux. This is non-perturbative, and GMFT leaves c free.
(c) Defect-laden pi-flux dynamics (see section 3). Translation-invariant analytic methods (GMFT, SCEBR) cannot treat vacancies, and QMC handles only the sign-free sector.
These gaps are genuine. What remains open is whether any of them changes a decision.

---

## 3. Model floor (L6): evidence that model error is at least as large as solver spread

1. **Defects.** Gao's sample has 4% Ce/Zr anti-site disorder. Sanders et al. 2609.28643 (2026-09-23) show that "already at dilution levels as low as two percent, well below those reported in cerium-based pyrochlores, these vacancy-induced processes connect percolating clusters of spins and dominate over the conventional quantum-spin-ice dynamics". Caveat: that QMC is presumably in the sign-free sector; extending the result to pi-flux is plausible but unverified. The 2404.04207 argument that disorder gives a Q- and polarization-independent signal applies to static disorder, not to vacancy-induced quantum fluctuations.
2. **Oxidation and stoichiometry.** Gaudet et al. arXiv:1903.09207 note that "disorder, especially oxidation" matters for powder Ce2Zr2O7 [VERIFIED listing]. 2404.04207 reports "no evidence of oxidation" for its crystal, which was stored in Ar.
3. **Sample dependence and material identity.** Ce2Sn2O7 went from an octupolar QSL claim (Sibille 1912.00928) to a dipolar spin-ice regime next to AIAO in hydrothermal samples (Yahne 2211.15140), and then to "a clear first order transition to long-ranged order at T ~ 0.04 K" (Smith et al. 2607.12274, 2026-07-14) [VERIFIED listings]. One of the three named materials is therefore no longer a QSI target at low T.
4. **Beyond-NN interactions.** Ce2Hf2O7 has a two-peak heat capacity, and the authors discuss "weak interactions beyond the nearest-neighbor XYZ Hamiltonian" (Smith et al. 2501.08327) [VERIFIED listing]. A beyond-NN term of order 0.1 Jx would change the photon scale K ~ 12 J+-^3/J^2 (which is 0.3 Jx here) at the same order as the solver differences under test.
5. **Background.** At the elastic position the magnetic signal is ~10% of the nonmagnetic scattering (2404.04207). Model-independent systematics, the T-subtraction versus polarization protocols, have already changed the physical conclusion once: earlier unpolarized T-subtracted data showed "no magnetic signal at the elastic position".
6. **Form factor.** 2404.04207 neglects the octupolar form factor and treats the tau_z form factor as constant at small Q. This is an approximation at the higher-Q points.

Hosoi et al. (ED32 + MD, 2022) favoured pi-flux OCTUPOLAR, while Gao et al. (GMFT, 2024) favour pi-flux DIPOLAR. The flip came from new polarized data and a new background protocol, not from a solver change. On the one solver-comparable quantity, the spinon continuum position, GMFT, ED32 (pi) and QMC (0) agree according to 2404.04207.

Conclusion: on the current decision (pi-D vs pi-O vs the Jx ≈ Jy boundary, with 0-flux excluded), solver spread is not the limiting uncertainty. The limits are resolution-induced parameter degeneracy (the c-theta valley), about 10% signal-to-background, and 2-4% defect content. Removing the solver error would not rank the hypotheses: the fit's own (c, theta) valley already spans every alternative within the GMFT family.

---

## 4. Answers to the six audit questions

1. **Decision-flip pre-test.** Across the published record, classical solvers agree where they overlap: GMFT, ED32 and QMC-0 on the continuum position. The dipolar-vs-octupolar flip in the literature was driven by data and protocol. No published study runs GMFT, SCEBR, ED32 and MD side by side against the same 2404.04207 likelihood. That run is the kill experiment (section 7). Prior: the solvers will agree within the c-theta degeneracy. If they do, kill.
2. **Model floor.** Very probably exceeded (section 3): 4% anti-site disorder against a 2% vacancy threshold, Ce2Sn2O7 ordering at 40 mK, beyond-NN terms in Ce2Hf2O7, and a 10% signal-to-background ratio.
3. **t_max and T-count.** The data need t_max ≈ 5-11 hbar/Jx, or 1.5-3.5 hbar/J+- (table above). The photon period is ~141 hbar/Jx, is not resolved, and has no decision value with present data. A rough, unaudited L = 3 estimate: 1296 bonds with 3-4 Pauli rotations each gives ~4-5e3 rotations per Trotter step. At dt ~ 0.05-0.1/Jx and t_max ~ 10/Jx that is 1e2-2e2 steps, ~1e6 rotations and ~2e7-5e7 T per real-time circuit at 20-50 T per rotation. Multiply by Gibbs-state preparation and shots: 10% magnetic contrast at 1% precision means ~1e4-1e6 samples per (q, E) point, for ~1e11-1e14 T in total. Because of Consequence 2, the scientifically valid target is L >= 5 (N >= 2000), which multiplies this by about 5-10x. The resource lens should redo these numbers.
4. **Can 3D BP-TN, t-VMC or NQS reach L = 3 at t ~ 50/J+-?** None has been demonstrated, and BP is structurally weak for loop-coherent pi-flux states. But t ~ 50/J+- is not required by any existing data. At the t ~ 3/J+- actually needed, the bottleneck is the thermal state.
5. **Is a finite-T state above the photon scale enough?** T = 50 mK sits in a crossover: kB T ≈ 1.5 hbar c/a0 (Gao's fit saturates c at 0.65 kB T), but kB T is below 12 J+-^3/J^2 ≈ 0.019 meV. Photons are therefore thermally occupied in the Rayleigh-Jeans regime, which classical-field and Gaussian-QED treatments capture. Spinons are dilute, with a 0.05 meV pair Boltzmann factor of ~1e-5. For a local quantum Gibbs sampler, the flux- and winding-sector mixing needed at L = 3 goes through spinon-pair creation with a suppression of ~exp(-2Delta/T) ~ 1e-5, so mixing is slow. A warm-start (GMFT/NQS trial + QPE filtering) avoids part of this but inherits trial-state bias.
6. **Practical significance.** Low. This is materials characterization for one INS community, with no downstream engineering decision. Under this user's "practical" requirement it is the weakest of the shortlist.

---

## 5. Would a better heuristic or tensor network win?
- At the resolution of existing data, the classically cheap chain (NLCE thermodynamic fit, then GMFT/SCEBR lineshape with free c, theta, then a chi^2 in 2404.04207 style) already fits within the error bars. A heuristic does not need to win, because the exact answer cannot be distinguished at this resolution.
- On single-family convergence (L5): there is no independent controlled check in pi-flux beyond ED32. This is a real classical weakness. It supports keeping the pi-flux Gibbs state as a benchmark problem, but not as a practical-decision problem.

## 6. Where classical fails (scaling-variable values)
- N > 32 (ED), in the pi-flux sector (QMC sign), at T < ~0.5 K ≈ 0.7 Jx (the NLCE 4th-order fit range in 2108.01217, "Above ~0.5 K"). The failure region is therefore N >= 128 AND T <= ~0.1-0.7 Jx AND J+- < 0.
- There is no published evidence of any classical method's accuracy there. The wall is plausible and multi-family: ED (size), QMC (sign), TN (3D plus loops), NLCE (low T). It has not been measured, and nobody has computed an average-sign curve for the Ce2Zr2O7 parameters.

## 7. Cheapest decisive classical kill experiment (days of CPU, no pre-registration needed beyond a note)
1. **Decision-flip test.** Digitize 2404.04207 Figs. 2-4 (the M_y, M_z energy scans at Q = (0,0,1), (3/4,3/4,0), (1,1,0) and the Q-scans at E = 0 and 0.1 meV). For hypotheses H1 pi-D (Gao 2024 fit), H2 pi-O (Jx <-> Jy swap of Smith 2022 / Bhardwaj 2022 [values UNVERIFIED]), H3 boundary (0.063, 0.062, 0.011) and H4 0-flux control, compute the resolution-convolved likelihood with four solvers: (a) GMFT+GQED, (b) FTLM on ED16 and ED32 at T = 50 mK, (c) SU(2) semiclassical MD with quantum-corrected Landau-Lifshitz dynamics, and (d) spinon hopping on a thermally sampled classical ice background. **Kill criterion:** all solvers give the same ranking, or the rankings differ by Delta chi^2 below the (c, theta) valley depth. Survive only if at least two solvers flip the H1/H2 ranking by more than that depth.
2. **Model-floor test.** Repeat (b) with 1 vacancy per 32 sites (3%, close to the 4% anti-site level) plus disorder averaging. **Kill criterion:** the vacancy-induced change in the E = 0+-0.03 meV M_z - M_y at (1,1,0) exceeds the solver spread from step 1.
3. **Sign diagnostic** (supports the wall and costs hours). Run SSE QMC in the local x-basis at the H1/H3 parameters for N = 128 and 432 over T = 0.5-0.05 K and report <sign>(N, T). If <sign> > ~1e-2 at N = 128 and T = 0.07 Jx, reweighted QMC + SAC is feasible and the "QMC wall" claim weakens.
4. **Finite-size check of the quantum target.** Using GQED photon modes on L = 2, 3, 5, 8 lattices, compute the quasielastic photon weight at 50 mK against L. This quantifies Consequence 2 cheaply.

## 8. Rescue options (for the orchestrator; not endorsed)
- **Re-scope to defect-laden pi-flux QSI** (vacancies or anti-site at 2-4%). The quantum algorithm handles disorder at no extra cost, while GMFT, SCEBR and QMC (sign) all fail. The cost is that defect type and concentration must be measured independently (X-ray, NMR), otherwise identifiability gets worse.
- **Re-scope to a thermodynamic target**: Cp(T) T^3 photon coefficient, thermal expansion and magnetostriction sign (Zhou, An, Kim arXiv:2608.11305 claim that "the sign of these signatures distinguishes the zero-flux and pi-flux QSI states"). This needs only the Gibbs state, which is the actual bottleneck, with no real-time part. It overlaps C17's mechanism.
- **Wait for µeV data.** Backscattering or spin-echo data on Ce2Zr2O7 or Ce2Hf2O7 (cf. Porée et al. 2304.05452, Nature Physics 21, 83 (2025) on Ce2Sn2O7, now known to order) would move the decision to photon-resolving times of ~1e2 hbar/Jx and L >= 6-10. That regime is informative and classically hard, but it is far beyond early fault-tolerant scale.

---

## Citations (all verified this session unless marked)
- Gao et al., arXiv:2404.04207; Nature Physics (2025) doi:10.1038/s41567-025-02922-9 [VERIFIED abs + PDF text]
- Gao et al., arXiv:2601.03202 (2026) [VERIFIED abs + html]
- Zhou, Zhou, Desrochers, Kim, Meng, arXiv:2510.14813 [VERIFIED abs + html]
- Sanders, Naik, Hallen, Schafer, arXiv:2609.28643 (2026-09-23) [VERIFIED abs]
- Zhou, An, Kim, arXiv:2608.11305 (2026-08-11) [VERIFIED abs]
- Smith et al., arXiv:2607.12274 (Ce2Sn2O7 LRO at 40 mK) [VERIFIED listing]; Yuan et al. arXiv:2601.20766 [VERIFIED listing]
- Smith et al., arXiv:2501.08327 (Ce2Hf2O7) [VERIFIED listing]; arXiv:2407.07640, PRX 15, 021033 (2025) [VERIFIED abs]; arXiv:2306.13183, PRB 108, 054438 (2023) [VERIFIED abs]; arXiv:2108.01217, PRX 12, 021015 (2022) [VERIFIED abs]
- Bhardwaj et al., arXiv:2108.01096, npj Quantum Mater. 7, 51 (2022) [VERIFIED abs; parameter values not verified]
- Hosoi, Zhang, Patri, Kim, arXiv:2201.00828, PRL 129, 097202 (2022) [VERIFIED abs; 32-site ED size taken from 2404.04207 text]
- Desrochers & Kim, arXiv:2401.09551, PRB 109, 144410 (2024) [VERIFIED abs]; arXiv:2301.05240, PRL 132, 066502 (2024) [VERIFIED listing + 2404.04207 ref list]
- Chern et al., arXiv:2311.04269 (PFFRG) [VERIFIED listing]; Schaden, Gonzalez, Reuther arXiv:2412.14773 (PMFRG) [VERIFIED abs]
- Sahu et al., arXiv:2312.03106; Desrochers et al., arXiv:2112.00014 [VERIFIED listings]
- Yahne et al., arXiv:2211.15140; Sibille et al., arXiv:1912.00928; Gaudet et al., arXiv:1903.09207; Porée et al., arXiv:2304.05452 (Nature Physics 21, 83 (2025)), arXiv:2305.08261 [VERIFIED listings/abs]
- Udagawa & Moessner, arXiv:1811.00199 [VERIFIED listing]; Taillefumier et al., arXiv:1705.00148 [VERIFIED listing]
- Huang, Deng, Wan, Meng, PRL 120, 167202 (2018) [from the 2404.04207 reference list; not independently fetched]
- Pace, Morampudi, Moessner, Laumann, PRL 127, 117205 (2021) [from the 2404.04207 reference list]
- Tindall et al., arXiv:2503.05693, Science 392, 868 (2026) [VERIFIED abs]; Mauron & Carleo, arXiv:2503.08247 [VERIFIED abs]; Wiersema, arXiv:2609.01719 [VERIFIED abs]
- Kim & Mourigal, arXiv:2602.10190 [VERIFIED abs] (2D analog: semiclassics + ED24 suffice at high T)
- Annual Review of CMP, "Experimental Insights into Quantum Spin Ice Physics in Dipole-Octupole Pyrochlore Magnets", doi:10.1146/annurev-conmatphys-041124-015101 [Crossref title only; content not read]
- Astrakhantsev et al., arXiv:2101.08787 (NQS up to 108 spins, ground state) [VERIFIED listing]

## Query log
- Q0 WebSearch "Ce2Zr2O7 dynamical structure factor finite temperature pi-flux ..." -> budget exhausted (200/200); all further searches via WebFetch.
- Q1 arXiv API abs:Ce2Zr2O7 -> 4 hits (subscript formatting hides most papers).
- Q2 arXiv API abs:"dipolar-octupolar" AND abs:pyrochlore -> 23 hits (found 2601.03202, 2608.11305, 2601.20766, 2311.04269).
- Q3 arXiv API abs:"quantum spin ice" AND (cerium | Ce | pi-flux) -> 30 hits (found 2609.28643, 2607.12274, 2510.14813, 2502.14067, 2501.08327, 2407.07640).
- Q4 abs pages: 2503.05693, 2601.03202, 2608.11305, 2609.28643, 2510.14813 (+html), 2407.07640, 2306.13183, 2108.01096, 2108.01217, 2404.04207 (+PDF full text; html 404), 2503.08247, 2609.01719, 2201.00828, 2401.09551, 2304.05452, 2412.14773, 2602.10190.
- Q5 arXiv API au:Smith_E_M AND pyrochlore (8); au:Bhardwaj AND pyrochlore (4); au:Schafer_R AND (pyrochlore | spin ice) (8); au:Udagawa AND (spin ice | spinon) (13).
- Q8 arXiv API (pyrochlore | spin ice) AND (neural | tensor network | PEPS | belief propagation | Pauli propagation | VMC) -> 18 hits, no 3D QSI dynamics or finite-T QSL correlators.
- Q9 arXiv API "quantum spin ice" AND (dynamical structure factor | spectral function | sign problem | sign-free) -> 7 hits.
- Q10 arXiv API (pi-flux | frustrated transverse) AND "Monte Carlo" AND (ice | pyrochlore) -> 1 hit (classical MC/MD only). No sign-free pi-flux QMC found.
- Q11 arXiv API "quantum spin ice" AND (ED | neural | tensor | linked cluster | MD | FRG) -> 12 hits since 2022.
- Q12 arXiv API spin ice AND quantum hardware -> HTTP 429; OpenAlex -> 429; Crossref "quantum spin ice pyrochlore quantum simulator Rydberg qubits" -> no 3D QSI hardware simulation in the top 20 (scoped).
- Local: `nature.com` redirected to login (not read). Arithmetic for timescales done in Python (section 1 table).
