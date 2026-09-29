# Audit C07 (classical adversary): finite-T axial/vector response of hot neutron-rich matter for supernova neutrino opacities

Auditor role: classical adversary. Date: 2026-09-28. Status: COMPLETE.
Verdict: **KILLED** in the decision-relevant regime (the static/long-wavelength opacity correction is already computed classically and ab initio; the residual real-frequency lineshape piece has measured low decision sensitivity; the regime where the sign problem "returns" coincides with the regime where the uniform-matter model fails). A narrow open sub-question survives only as a physics question, not as a quantum-advantage target (see Section 7).

---

## 1. Summary of the adversarial case

1. **The decision-relevant quantity is mostly static, and is classically solved.** The neutral-current (NC) many-body opacity correction used in supernova codes is, to leading order, a long-wavelength static structure-factor correction (S_V(q->0), S_A(q->0)). Ab initio lattice calculations with N3LO chiral interactions already give S_A and S_V for hot neutron matter at T = 10-20 MeV, n = 0.012-0.033 fm^-3 (and comparisons up to ~0.053 fm^-3), L = 6^3-8^3, a = 1.32 fm, with an estimated ~5% overall systematic (Ma et al., PRL 132, 232502 (2024), arXiv:2306.04500). Continuum- and infinite-volume-extrapolated LO pionless S(q) at finite T beyond the virial regime exist too (Alexandru, Bedaque, Berkowitz, Warrington, PRL 126, 132701 (2021), arXiv:2008.02824). The virial expansion covers the low-density end (Horowitz et al. arXiv:1611.05140). Ma et al. state explicitly that RPA opacity codes "can now be calibrated with ab initio lattice calculations".
2. **The sign problem does not bite where the candidate says.** Pure neutron matter with LO pionless EFT has only the attractive 1S0 contact between spin-balanced species, so it is sign-free. This is what Alexandru et al. 2021 use. SU(4)-symmetric LO lattice interactions are also free of sign oscillations (Lu et al., PLB 797, 134863 (2019), arXiv:1812.10928). The auxiliary field couples identically to all four species, so with n-up = n-down and p-up = p-down the weight is a product of squared real determinants. **Y_p != 0 by itself therefore does not generate a sign problem** (this is my own derivation, consistent with the SU(4) positivity used by Lee et al., so mark it [DERIVED]). The sign problem comes from SU(4) breaking (1S0 vs 3S1, OPE tensor, spin-orbit). That breaking is handled perturbatively on top of the sign-free base with wave-function matching and the rank-one operator method. The published result for the exact target observable (Ma et al. 2024) is ~5% systematic. At these densities the EFT expansion parameter is small: k_F(PNM, 0.1 n0) ~ 0.78 fm^-1 ~ 154 MeV and thermal momentum at T = 10 MeV ~ 170 MeV, so Q ~ 0.25-0.3 [own estimate]. The perturbative treatment is therefore well controlled. The claim that the advantage "is exponential where the sign problem returns" is not supported in the neutrinosphere window.
3. **The real-frequency lineshape (the part a quantum computer would add) has low measured decision sensitivity.** The q->0 width of S_A(q,w) comes from spin-non-conserving (tensor) forces. The same physics sets NN bremsstrahlung and spin relaxation. Bartl, Bollig, Janka, Schwenk (PRD 94, 083009 (2016), arXiv:1608.05037) replaced OPE-based rates with rates from modern nuclear interactions. That reduced bremsstrahlung by a factor of 2-5 in the neutrinospheric region, but changed neutrino luminosities by **<~5%**, mean energies by <~0.7 MeV and PNS cooling time by <~0.5-1 s. Ma et al. 2024 likewise note that exact dynamic structure factors give only "small but noticeable deviations" from the long-wavelength estimate. Several classical families already model the dynamic structure factor: virial linear response with near-exact scaling laws (Bedaque, Reddy, Sen, Warrington, PRC 98, 015802 (2018), arXiv:1801.07077); unitary-gas phenomenology with BHF static input (Guo, Martinez-Pinedo, Wu, PRC 110, 015504 (2024), arXiv:2401.10737); chiral BHF dynamic S at T = 5-10 MeV (Vidana, Logoteta, Bombaci, arXiv:2206.10190); chiral EFT + RPA for charged current (Shin, Rrapaj, Holt, Reddy, arXiv:2306.05280); and hydrodynamic modes (Shen & Reddy, arXiv:1311.6096).
4. **The L5 shortcut is available.** Opacities and energy-exchange kernels are integrals of S(q,w) against kernels that are smooth on the scale of T, because the neutrino phase space and blocking factors vary on that scale. Smeared spectral densities with a smearing width chosen up front can be extracted from Euclidean correlators on [0, beta] with quantified errors (Hansen, Lupo, Tantalo, PRD 99, 094508 (2019), arXiv:1903.06476). This Backus-Gilbert-type method is general and not specific to QCD. Sign-free AFQMC Euclidean data plus smeared-spectral-density reconstruction therefore fixes the decision-relevant functionals of S(q,w) without an ill-posed pointwise inversion. It is the classical twin that a quantum real-frequency estimator must beat. The quantity that stays inaccessible, a sharp pointwise lineshape at sub-T resolution, is precisely the one with little influence on the transport result (lesson 5: information vs computation).
5. **The model floor (L6) sits exactly where the claimed classical hardness sits.** The candidate places the quantum advantage at Y_p > 0 and low T (3-5 MeV), where it expects the sign problem to grow. In that corner, supernova matter is not uniform nucleonic matter. It contains light clusters (d, t, 3He, alpha) and, at higher density and low T, heavy nuclei and pasta. There coherent and cluster scattering dominate the opacity (Arcones et al., PRC 78, 015806 (2008); Horowitz et al. pasta, arXiv:1611.10226). A uniform-matter lattice box with L = 6-10 at a = 1.32 fm (8-13 fm) cannot represent pasta unit cells of tens of fm. An exact quantum solution of that Hamiltonian in that box is the wrong model (FeMoco-type lesson).
6. **The decision flip is real for ~10-20% static corrections, and those are already classically available.** The NC many-body correction matters at rho >~ 1e12 g/cm^3 at the 10-20% level (O'Connor, Horowitz, Lin, Couch, arXiv:1712.08253). It helped marginal 3D/2D models explode (Burrows et al. 1611.05859; Vartanyan et al. 1801.08148, 1809.05106; Burrows et al. 1902.00547). The strangeness-driven NC reduction of "several 10%" flipped a 3D 20 Msun model (Melson et al. 1504.07631). The residual uncertainty after lattice calibration is ~5% on the static factor, plus a lineshape effect of order a few %. That is smaller than competing simulation uncertainties: the ray-by-ray approximation (Just et al. 1805.03953 find it more influential than many-body corrections), fast flavor conversion (Ehring et al., "Fast Neutrino Flavor Conversions Can Help and Hinder Neutrino-Driven Explosions", PRL 131, 061401 (2023), doi:10.1103/PhysRevLett.131.061401), resolution, and progenitor structure. A quantum result would not flip a supernova outcome the classical result does not already flip.
7. **The validation target is not an advantage target.** Unitary Fermi gas S(q,w) is sign-free for AFQMC and is measured by Bragg spectroscopy. It is a good correctness test and, by construction, classically solved.

## 2. Answers to the audit questions

**(1) Which (n, T, Y_p) window controls explosion outcomes, and is solver spread > EFT truncation error?**
The window is roughly rho ~ 1e12-3e13 g/cm^3 (n ~ 6e-4 to 2e-2 fm^-3, i.e. ~0.004-0.12 n0), T ~ 5-12 MeV, Y_e ~ 0.1-0.3 (O'Connor et al. 2017: effects only at >~1e12 g/cm^3). Rough fugacity estimate [own]: lambda(T=10) ~ 5.1 fm and lambda(T=5) ~ 7.2 fm, giving z ~ n lambda^3/2 ~ 0.04-0.4 at T = 10 and ~0.1-1 at T = 5. The virial expansion is therefore good at the low end and fails in the upper part of the window. That upper part is exactly what Ma et al. 2024 (n up to ~0.05 fm^-3, T >= 10 MeV) and Alexandru et al. 2021 cover. Multi-family spread for the static axial factor is lattice-N3LO vs virial ~5% at n ~ 0.015 fm^-3 and ~25% at n ~ 0.053 fm^-3 (Ma et al. 2024). That spread was resolved by a classical ab initio method, and the EFT truncation error at Q ~ 0.25-0.3 is small at N3LO. Solver spread does exceed truncation error, but a classical solver already closed it.

**(2) Is LO pure neutron matter at low density sign-free? Where does the sign problem bite?**
Yes. LO pionless PNM (1S0 contact, spin-balanced) is sign-free. SU(4)-symmetric LO is sign-free for any spin-balanced isospin content (Lu et al. 2019 state the absence of sign oscillations; the product-of-squared-determinants argument is [DERIVED] here). The sign problem enters through SU(4)-breaking and tensor/spin-orbit terms. At the neutrinosphere these are perturbative and are treated to N3LO via wave-function matching and the rank-one operator method with ~5% systematics. The sign problem becomes severe for non-perturbative tensor physics at high density (>~n0) and for spin-polarized or strongly SU(4)-broken matter at low T. Those regimes lie outside the neutrinosphere window or inside the inhomogeneous-matter regime (point 5).

**(3) Do opacities need the real-frequency lineshape, or only S(q) and low moments?**
Mostly S(q->0) plus the thermal smearing scale. Bedaque et al. 2018 and Guo et al. 2024 argue that dynamic S matters for energy and momentum exchange (backscattering suppression, neutrino decoupling). But the quantified sensitivity is small. A factor 2-5 change in the tensor-driven spin-relaxation/bremsstrahlung response gives <~5% luminosity change (Bartl et al. 2016), and exact dynamic S gives "small but noticeable" deviations (Ma et al. 2024). The kernels are smooth on the scale T, so Euclidean data plus controlled smeared-spectral reconstruction (HLT 2019) fixes them. This is the same pattern as lesson 5: the information the quantum computer uniquely supplies (fine lineshape) carries little decision value.

**(4) Is there a multi-family disagreement at a named state point?**
Yes, historically: virial vs lattice N3LO differ by ~25% in S_A at n ~ 0.053 fm^-3 (T ~ 10 MeV) (Ma et al. 2024). BHF (Guo 2024, Vidana 2022), RPA (Horowitz fit, Roberts-Reddy arXiv:1612.02764 for CC) and Skyrme/CBF (Pastore, Benhar) also differ. But the ab initio classical family (sign-free AFQMC lattice with perturbative N3LO) is the arbiter, and it exists. Beyond ~0.3 n0 with T < 10 MeV and Y_p > 0, no ab initio S_A(q,w) exists. There the uniform-matter model and cluster/pasta physics dominate the error budget.

**(5) Resource estimate for L = 6-10, 2 species x 2 spins [own order-of-magnitude, not from a published cost table].**
- System qubits: the Watson et al. (arXiv:2312.05344, v3 2026-05-18) VC encoding uses 6 qubits per site, giving 1296 (L=6), 3072 (L=8) and 6000 (L=10). Jordan-Wigner needs 4 L^3 = 864-4000. A thermofield-double or purification route roughly doubles this. Ancillas come on top.
- Hamiltonian norm: at a = 1.32 fm, the hopping scale is hbar^2/(2 m a^2) ~ 12 MeV, the kinetic band ~150 MeV per mode, and contact terms are O(10^2) MeV per site. That gives lambda ~ 1e5-1e6 MeV for L = 8.
- Circuit cost: 1 MeV resolution needs t ~ 1 MeV^-1, i.e. ~1e5-1e6 qubitization steps. Each step costs ~1e3-1e4 Toffolis (block-encoding over ~2e3-6e3 modes), so one coherent run is ~1e8-1e10 Toffolis. Shots for ~1% error on S(q,w) bins plus thermal-ensemble averaging add ~1e3-1e5. That is **~1e11-1e15 Toffolis per (n, T, Y_p, q) point**, before thermal-state-preparation cost.
- Thermal state preparation: the Gibbs-sampler mixing time at T = 5-15 MeV for this Hamiltonian is unknown. Watson et al. do not treat thermal states or response functions (verified: their tasks are time evolution and QPE).
- Physical system: n = 0.016 fm^-3 in an L = 10 box ((13.2 fm)^3) holds only ~37 neutrons. Sign-free AFQMC handles 60-100+ nucleons routinely, so the quantum simulation would cover a system that is smaller than, or equal to, what classical AFQMC already treats.

**(6) Would a supernova sensitivity run with the plausible opacity change flip an outcome?**
A 10-20% static NC change can flip marginal models, but that change is already captured classically (virial/RPA fits, now lattice-calibrated). The plausible additional change from a quantum real-frequency lineshape is a few % (Bartl 2016: factor 2-5 in a related tensor-driven rate gives <~5% luminosities). That is below competing systematics (ray-by-ray, fast flavor conversion, resolution, progenitor). No evidence was found that it flips an outcome.

## 3. Where classical computation actually fails (scaling-variable values)
- Pointwise real-frequency S_A(q->0, w) at sub-T resolution, where the width comes from tensor forces at n >~ 0.05 fm^-3, T ~ 5-10 MeV. Only two-body T-matrix/quasiparticle models (Bartl et al.) and phenomenology (Guo et al.) exist; no ab initio many-body result was found. Decision sensitivity is low (above).
- Asymmetric matter with non-perturbative SU(4) breaking at T <~ 5 MeV and n >~ 0.1 n0. The physical state there is inhomogeneous (clusters/pasta), so a uniform L <= 10 box is model-dominated.
- n >~ 0.5-1 n0 with T < 10 MeV (PNS interior, late-time cooling): the tensor/3N sign problem grows and EFT truncation error grows at the same time (Q -> 0.5). The model floor rises in step with the solver difficulty.

## 4. Strongest classical attacks (ranked)
1. Sign-free lattice AFQMC (SU(4)/pionless base) plus perturbative N3LO via wave-function matching and the rank-one operator method (Ma et al. 2024), plus pinhole-trace thermodynamics (Lu et al. PRL 125, 192502 (2020), arXiv:1912.05105; Agar, Ren, Elhatisari arXiv:2604.09154 for symmetric matter; Ren et al. arXiv:2305.15037 for clusters).
2. Euclidean correlators G(q, tau) from (1), with smeared spectral densities (HLT 2019) at the kernel's natural smearing width T, giving opacity functionals with quantified errors.
3. Virial expansion with light clusters at the low-density end (Horowitz et al. 1611.05140, 1209.3173).
4. Two-body T-matrix / chiral bremsstrahlung and spin relaxation for the axial width (Bartl et al. PRL 113, 081101 (2014); PRD 94, 083009 (2016)).
5. Chiral EFT + RPA / BHF dynamic response (Shin et al. 2306.05280; Vidana et al. 2206.10190; Guo et al. 2401.10737); UQ ensembles (Lin, Steiner, Margueron arXiv:2207.05927).
6. NQS for dilute neutron / asymmetric matter at T = 0 (Fore et al. arXiv:2212.04436; Fore, Kim, Hjorth-Jensen, Lovato arXiv:2407.21207, 0.01-0.1 fm^-3 with clustering). Finite-T and dynamic extensions are not yet shown.
7. CC with GIT at T = 0 (Sobczyk, Jiang, Roggero arXiv:2407.20986). This is the zero-temperature spectral benchmark.

## 5. Cheapest decisive classical kill experiment
Target state points: n in {0.01, 0.03, 0.05} fm^-3, T in {5, 8, 10} MeV, Y_p = 0 and then 0.1.
1. Compute G_A(q, tau) and G_V(q, tau) with sign-free LO lattice AFQMC (pionless, spin-balanced; SU(4) base for Y_p = 0.1) at L = 6-8. Add first-order N3LO corrections following Ma et al.
2. Reconstruct smeared S_A(q, w) with HLT at smearing sigma in {T/2, T}. Compute the NC transport opacity and energy-exchange kernels for E_nu = 5-40 MeV.
3. Compare three things: the long-wavelength static approximation; smeared-dynamic opacities at the two smearing widths; and a deliberate +-factor-2 variation of the spin-relaxation width (Bartl-style).
4. **Kill criterion:** the candidate is dead if (a) the opacities are stable to <~5% when sigma goes from T to T/2, i.e. finer lineshape information does not move them, AND (b) the +-factor-2 width variation moves opacity-weighted quantities by less than the ~5% lattice systematic.

Optional last step: feed the opacity envelope into a spherically symmetric (1D + effective turbulence) or 2D code on a marginal progenitor. Compare the outcome change with the change from toggling fast flavor conversion. This is cheap relative to any quantum resource and needs no new physics code, because published pipelines exist for Ma et al. and O'Connor et al.

## 6. Hardness single-family?
No. At the decision-relevant state points, the virial, lattice-N3LO, pionless-continuum lattice, and BHF families agree to within 5-25%. The ab initio lattice family resolves the residual. No state point in the neutrinosphere window was found where all converged classical families fail while the opacity matters.

## 7. What survives (narrow, not a quantum-advantage claim)
An ab initio real-frequency spin-relaxation width of warm neutron-rich matter with chiral tensor forces at n ~ 0.03-0.1 fm^-3 is a legitimate classical physics gap. It is a possible long-term, category-1 (quantum usefulness) demonstration target. It fails the decision-relevance test (Bartl et al. 2016), and a smeared classical twin exists (HLT). By the charter's own rules it is not an advantage candidate.

## 8. Corrections to the candidate text
- arXiv:1612.02764 is Roberts & Reddy, "Charged current neutrino interactions in hot and dense matter", PRC 95, 045807 (2017): CC absorption with an open-source opacity implementation. It is not an NC RPA/virial table. The virial NC fit is Horowitz, Caballero, Lin, O'Connor, Schwenk arXiv:1611.05140.
- "Sign problem grows with Y_p" is inaccurate for SU(4)-like LO interactions. It grows with SU(4) breaking and tensor strength.
- Watson et al. 2312.05344 costs time evolution and QPE, not thermal states or response functions. The thermal-state preparation cost for this candidate is uncosted.
- Roggero & Carlson 1804.01505 (PRC 100, 034610 (2019)) already discusses finite-temperature linear response on a quantum computer (per its abstract, as summarized by WebFetch). Novelty is "B/C-ish" at most. The novelty audit is separate.

## 9. Citations (verified via arXiv abs page, Crossref, Semantic Scholar or OpenAlex on 2026-09-28)
- Ma, Lin, Lu, Elhatisari, Lee, Li, Meissner, Steiner, Wang, arXiv:2306.04500; PRL 132, 232502 (2024), doi:10.1103/PhysRevLett.132.232502. HTML v3 read: T = 10-20 MeV, n = 0.012-0.033 fm^-3, a = 1.32 fm, L = 6-8, ~5% systematic, virial deviation ~5% (n ~ 0.015) to ~25% (n ~ 0.053) in axial, static only.
- Alexandru, Bedaque, Berkowitz, Warrington, arXiv:2008.02824; PRL 126, 132701 (2021).
- Guo, Martinez-Pinedo, Wu, arXiv:2401.10737; PRC 110, 015504 (2024).
- Bedaque, Reddy, Sen, Warrington, arXiv:1801.07077; PRC 98, 015802 (2018).
- Shin, Rrapaj, Holt, Reddy, arXiv:2306.05280.
- Vidana, Logoteta, Bombaci, arXiv:2206.10190.
- Shen & Reddy, arXiv:1311.6096; Shen, Gandolfi, Reddy, Carlson, arXiv:1205.6499 (AFDMC spin response).
- Horowitz, Caballero, Lin, O'Connor, Schwenk, arXiv:1611.05140.
- Horowitz, Shen, O'Connor, Ott, arXiv:1209.3173 (CC virial).
- Roberts & Reddy, arXiv:1612.02764; PRC 95, 045807 (2017).
- Rrapaj, Holt, Bartl, Reddy, Schwenk, PRC 91, 035806 (2015), doi:10.1103/PhysRevC.91.035806 (Crossref).
- O'Connor, Horowitz, Lin, Couch, arXiv:1712.08253.
- Melson et al., arXiv:1504.07631.
- Burrows et al. arXiv:1611.05859; Vartanyan et al. arXiv:1801.08148, arXiv:1809.05106; Burrows et al. arXiv:1902.00547; Just et al. arXiv:1805.03953.
- Bartl, Bollig, Janka, Schwenk, PRD 94, 083009 (2016), arXiv:1608.05037 (abstract read via Semantic Scholar).
- Bartl, Pethick, Schwenk, PRL 113, 081101 (2014), doi:10.1103/PhysRevLett.113.081101 (Crossref).
- Arcones et al., PRC 78, 015806 (2008), doi:10.1103/PhysRevC.78.015806 (Crossref).
- Horowitz et al., arXiv:1611.10226 (pasta and late-time SN neutrinos).
- Lin, Steiner, Margueron, arXiv:2207.05927.
- Hansen, Lupo, Tantalo, arXiv:1903.06476; PRD 99, 094508 (2019).
- Lu, Li, Elhatisari, Lee, Epelbaum, Meissner, arXiv:1812.10928; PLB 797, 134863 (2019).
- Lu et al., arXiv:1912.05105; PRL 125, 192502 (2020).
- Ren, Elhatisari, Lahde, Lee, Meissner, arXiv:2305.15037.
- Agar, Ren, Elhatisari, arXiv:2604.09154 (2026; symmetric matter criticality, sign-friendly Hamiltonians, perturbative strategy benchmarked).
- Chen, Lee, Schaefer, arXiv:nucl-th/0408043; PRL 93, 242302 (2004) (the abstract does not itself state positivity; cited only for the Wigner-limit context).
- Watson, Bringewatt, Shaw, Childs, Gorshkov, Davoudi, arXiv:2312.05344 (v3, 2026-05-18): 6 qubits/site VC encoding; time evolution + QPE; no thermal/response.
- Sobczyk, Jiang, Roggero, arXiv:2407.20986 (CC + GIT spin response of neutron matter).
- Roggero & Carlson, arXiv:1804.01505; PRC 100, 034610 (2019).
- Fore, Kim, Carleo, Hjorth-Jensen, Lovato, arXiv:2212.04436.
- Fore, Kim, Hjorth-Jensen, Lovato, arXiv:2407.21207.
- Ehring et al., PRL 131, 061401 (2023), doi:10.1103/PhysRevLett.131.061401 (title verified via OpenAlex; author list [UNVERIFIED beyond first-author convention]).
- Krotscheck, Wang, arXiv:2507.03825 (T = 0 parquet response of neutron matter).
- Other listed but not used for claims: Pastore et al. 1408.2811; Benhar 1210.2837; Lombardo et al. nucl-th/0212037; Carbone 2020 doi:10.1103/PhysRevResearch.2.023227; Keller 2021 doi:10.1103/PhysRevC.103.055806; Riz 2020 doi:10.1088/1361-6471/ab6520.

## 10. Query log
- WebSearch: "structure factors hot neutron matter ab initio lattice simulations chiral interactions" -> budget exhausted (200/200); switched to WebFetch.
- arXiv API: all:"neutron matter" AND "structure factor" AND lattice -> 2306.04500, 2008.02824.
- arXiv abs: 2306.04500, 2008.02824, 2401.10737, 1801.07077, 1712.08253, 1612.02764, 2604.09154, 2305.15037, 1912.05105, 2312.05344, 2407.20986, 1903.06476, nucl-th/0408043, 2212.04436, 2407.21207, 1804.01505, 1812.10928.
- arXiv HTML: 2312.05344v3 (resource details), 2306.04500v3 (parameters).
- arXiv API: abs:"neutron matter" AND response AND neutrino AND temperature; abs:"neutron matter" AND dynamical AND (response OR structure factor); (neutrino opacit* OR neutrino scattering) AND (dynamic structure OR spin response); supernova AND explosion AND (many-body corrections OR neutrino-nucleon scattering OR structure factor); au:Horowitz AND virial AND neutrino; au:Lin_Zidu OR (au:Lee_Dean AND temperature); lattice AND (pinhole OR hot dilute OR nuclear thermodynamics OR asymmetric nuclear matter) AND temperature.
- arXiv API, HTTP 429 (not retrieved): unitary Fermi gas dynamic structure factor; Bartl AND Schwenk; neutron matter spin response; hot/warm neutron matter response.
- OpenAlex: unitary Fermi gas dynamic structure factor QMC (irrelevant hits); hot neutron matter dynamic structure factor neutrino scattering (found the Ehring 2023 FFC PRL and the Ma 2024 PRL DOI); one 429.
- Crossref: Bartl Bollig Janka Schwenk bremsstrahlung; neutron matter spin response finite temperature neutrino opacity (2019+); "Charged-current reactions in the supernova neutrino-sphere"; impact neutrino opacities CCSN many-body corrections sensitivity (2019+).
- Semantic Scholar: DOI 10.1103/physrevd.94.083009 (abstract retrieved); one search returned 429.
- Bing: one attempt, no usable metadata.

Scoped finding: in the sources above, searched through 2026-09-28, I found ab initio classical static S_A/S_V of hot neutron matter (Ma 2024 N3LO lattice; Alexandru 2021 LO pionless), classical dynamic-S models (virial scaling, BHF, RPA, unitary-gas phenomenology, T-matrix spin relaxation), and supernova sensitivity studies. I found no ab initio many-body real-frequency S_A(q,w) of warm asymmetric matter with chiral tensor forces, and no study showing that such a lineshape flips a supernova outcome.
