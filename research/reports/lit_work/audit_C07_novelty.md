# Audit C07 (novelty / prior art): finite-T axial/vector response of hot neutron-rich matter for supernova neutrino opacities

Auditor role: NOVELTY / PRIOR-ART. Date: 2026-09-28. Status: COMPLETE.
Verdict: **WOUNDED**. Novelty category for the quantum computation as stated: **B** (quantum methods nearby, not this problem). The stated advantage mechanism (exponential, because "the sign problem returns") is largely contradicted by the classical literature in the window that controls explosions. What remains is narrower. It is a real-frequency spin/spin-isospin lineshape with non-central forces, replacing ill-posed Euclidean inversion, and its decision value is modest.

Verification legend: [V-arXiv] = arXiv API or abs page read this session; [V-OA] = OpenAlex record read this session; [V-CR] = Crossref record read this session; [UNVERIFIED] = from memory, not checked this session.

---

## 1. EXACT PRIOR WORK (this problem, any method)

Classical ab initio / many-body computations of the vector (S_V) and axial (S_A) response of hot neutron(-rich) matter for neutrino opacities:

| Work | Method | Quantity | Regime | Verified |
|---|---|---|---|---|
| Ma, Lin, Lu, Elhatisari, Lee, Li, Meissner, Steiner, arXiv:2306.04500, PRL 132, 232502 (2024) | Lattice EFT at N3LO chiral. SU(4) LO is non-perturbative and sign-free; higher orders are perturbative via the rank-one-operator (RO) method with wave-function matching | **Static** S_V, S_A of pure neutron matter | T=10-20 MeV, n~0.012-0.045 fm^-3 (fig. to 0.053), L=6,7,8, a=1.32 fm. Deviation from the 2nd-order virial of S_A is ~5% at n~0.015 and ~25% at n~0.053 fm^-3. Proton fraction >0 is stated as future work | [V-arXiv][V-OA W4399365972][V-CR] |
| Alexandru, Bedaque, Berkowitz, Warrington, arXiv:2008.02824, PRL 126, 132701 (2021) | LO pionless lattice, HMC with pseudofermions; the integrand is **positive definite**, so there is no sign problem | Static S_V, S_A(q), Tan contact, continuum and infinite-volume limits | T~4.14 MeV, z=1.0-1.5, n~5-8e-3 fm^-3 | [V-OA W3047905376][V-arXiv abs+html] |
| Alexandru, Bedaque, Warrington, arXiv:1907.03914, PRC 101, 045805 (2020) | Lattice unitary gas | Static S_V, S_A | 0.1<z<1, above T_c. Qualitative deviation from virial at high z | [V-arXiv][V-CR] |
| Bedaque, Reddy, Sen, Warrington, arXiv:1801.07077, PRC 98, 015802 (2018) | Virial + pseudopotential | **Dynamic** S_V(q,w), S_A(q,w) | T=5-10 MeV, q<30 MeV. Finds near-exact scaling laws and says "dynamical structure factors are essential" | [V-arXiv][V-OA] |
| Horowitz, Caballero, Lin, O'Connor, Schwenk, PRC 95, 025801 (2017) | Virial | NC scattering corrections used in supernova codes | low density | [V-CR/OA title+DOI only] |
| Guo, Martinez-Pinedo, Wu, arXiv:2401.10737, PRC 110, 015504 (2024) | Finite-T BHF for S(q->0), plus a phenomenological unitary-gas-motivated S(q,w) | Static S and a model dynamic S; NC cross sections | T=5-30 MeV, n=1e-4-0.063 fm^-3. Dynamic vs static changes cross sections by **10-20%** (enhanced at low E_nu, suppressed at high E_nu). Medium suppression vs free gas is 10-30% | [V-arXiv][V-html] |
| Shin, Rrapaj, Holt, Reddy, PRC 109, 015804 (2024) | Chiral-EFT mean field + RPA (direct+exchange) | Density, spin, isospin, **spin-isospin dynamic** response of warm beta-equilibrium matter; CC and NC rates | near decoupling; RPA redistributes CC strength | [V-OA W4391135076] |
| Vidana, Logoteta, Bombaci, arXiv:2206.10190 | Finite-T BHF with chiral forces | DSF and mean free path vs chiral order | cut-off dependence nearly gone at N3LO | [V-arXiv] |
| Lin, Steiner, Margueron, PRC 107, 015804 (2023) | HF+RPA UQ | NC and CC inverse mean free paths | Residual interactions in the spin and spin-isospin channels are "not well constrained" | [V-OA W4285483921] |
| Sobczyk, Jiang, Roggero, arXiv:2407.20986, PRL 134, 192701 (2025) | Coupled cluster + Gaussian integral transform (GIT) with spectral UQ | Real-frequency **spin response** of neutron matter, **T=0 only** | finite-size analysis | [V-arXiv][V-OA W4410293839] |
| Lykasov, Pethick, Schwenk, arXiv:0808.0330, PRC 78 (2008) | Landau Fermi-liquid theory with relaxation time | Spin response width from spin relaxation (non-central forces); bremsstrahlung | neutron matter | [V-OA] |
| Bartl, Pethick, Schwenk, PRL 113, 081101 (2014) | Resonant-Fermi-gas / T-matrix | Enhancement of neutrino rates at subnuclear density | | [V-CR title+DOI] |
| Roberts, Reddy, arXiv:1612.02764, PRC 95, 045807 (2017) | Relativistic mean field, finite-T field theory | CC opacities incl. mean-field shifts, open-source implementation | | [V-arXiv] |
| Lovato et al. / Raghavan, Lovato, PRC 110, 025504 (2024) (arXiv:2310.18756) | NN-based inversion of Euclidean responses with UQ | Inversion methodology (nuclei) | shows classical inversion + UQ is improving | [V-OA] |
| Parnes, Barnea, Carleo, Lovato, Rocco, Zhang, doi:10.1103/tlqz-nw28 (2026) | NQS + Lorentz integral transform | Nuclear responses (light nuclei), LO pionless | | [V-OA] |

Relevant classical methods that remove the sign-problem argument:
- Niu, Lu, doi:10.1103/pn99-6dxt (PRL 2025): a rigorously sign-problem-free lattice nuclear force, **including spin-orbit**, for even-even systems. [V-OA]
- Lu, Li, Elhatisari, Lee, Drut, Lahde, arXiv:1912.05105, PRL 125, 192502 (2020): pinhole-trace finite-T nuclear thermodynamics, with a speedup of up to about 1000x. [V-arXiv]

## 2. NEAREST QUANTUM WORK

- Roggero & Carlson, "Dynamic linear response quantum algorithm", arXiv:1804.01505, PRC 100, 034610 (2019). A T=0 nuclear response algorithm. [V-CR]
- Roggero, "Spectral density estimation with the Gaussian Integral Transform", arXiv:2004.04889, PRA 102, 022409 (2020). [V-OA]
- Roggero, Li, Carlson, Gupta, Perdue, PRD 101, 074038 (2020), "Quantum computing for neutrino-nucleus scattering". Covers nuclei at T=0 and a pionless lattice model. [V-OA listing]
- Baroni et al., PRD 105, 074503 (2022), "Nuclear two point correlation functions on a quantum computer". [V-CR]
- Hartse & Roggero, EPJA 2023 (arXiv:2211.00790), energy moments; Kiss, Grossi, Roggero, Quantum 7, 977 (2023), importance-sampled qDrift demonstrated on a lattice nuclear EFT. [V-OA]
- Watson, Bringewatt, Shaw, Childs, Gorshkov, Davoudi, arXiv:2312.05344 (v3 May 2026): qubit and T costs for time evolution and energy estimation in LO pionless and pionful lattice EFT. A WebFetch of the HTML found **no treatment of thermal states, neutron matter, response functions or opacities**. [V-arXiv abs, html summary]
- Spagnoli, Lissoni, Roggero, arXiv:2507.22814: first-quantized LO pionless dynamics with polynomial resources. "Tens of millions of T gates and few hundred logical qubits" for simple reactions (few-body). [V-arXiv]
- Gu, Heinz, Kiss, Papenbrock, arXiv:2507.14690 (PRC 2026, doi:10.1103/gqdy-dvps); Liu, Shi, Lu, Xu, arXiv:2604.13430. Both are ground-state few-body lattice nuclear VQE. [V-arXiv]
- Du, Yang, Liu, Yang, Vary, PLB 2026 doi:10.1016/j.physletb.2026.140538. A quantum-classical LIT response framework applied to 19O (finite nucleus, T=0). [V-OA]
- Turro, arXiv:2306.16580: QITE thermal-state algorithm demonstrated on 2-3 neutron systems. [V-OA]
- Cruz, Wild, Banuls, Cirac, doi:10.1103/lpz2-j7vg (2025): finite-T and microcanonical dynamical response via energy filters (generic; free-fermion demo). [V-OA]
- Rall, PRA 102, 022408 (2020): block-encoding estimators incl. thermal correlation functions (generic). [V-OA listing]
- Bedaque, Khadka, Rupak, Yusf, arXiv:2209.09962, PRC 111, 034604 (2025): radiative (photon/neutrino-emission) matrix elements on a QC, few-body. [V-arXiv]
- Castano-Garcia et al., arXiv:2608.06515: QCD-level quantum computing for the neutron-star EoS (static, T=0 style, few particles). [V-arXiv]
- Analog quantum simulation of the unitary Fermi gas (the proposed validation target) already measures finite-T S(q,w) and the **spin** response: Hoinka, Lingham, Delehaye, Vale PRL 109, 050403 (2012) "Dynamic spin response of a strongly interacting Fermi gas"; Carcy et al. PRL 122, 203401 (2019). [V-OA] Unitary gas as a neutron-matter analogue: arXiv:1210.6659, arXiv:0911.0747 (search listing).

## 3. NEAREST CLASSICAL WORK (direct competitors for D)
E = Euclidean lattice/AFQMC (sign-free LO + perturbative N3LO; Ma 2024; Alexandru 2021) + inversion (MaxEnt / NN-UQ inversion, Raghavan-Lovato 2024).
F = virial dynamic S (Bedaque 2018), BHF + phenomenological dynamic S (Guo 2024), chiral MF+RPA dynamic response (Shin 2024), Landau relaxation-time spin response (Lykasov 2008), T=0 CC-GIT (Sobczyk 2025), NQS+LIT (Parnes 2026).

## 4. WHAT HAS BEEN TESTED
- Static S_V and S_A of hot pure neutron matter: ab initio, controlled, N3LO (Ma 2024), and LO continuum-extrapolated (Alexandru 2021). Virial agreement at low density has been quantified.
- Dynamic S(q,w) in hot neutron matter: only from the virial expansion (low z), BHF plus a phenomenological form, and mean-field+RPA / Landau models.
- Real-frequency ab initio spin response of neutron matter at T=0 (CC-GIT, with UQ).
- Quantum algorithms for real-frequency response of nuclei at T=0 (GIT, LIT, Chebyshev, moments), with small hardware demos.
- Quantum resource estimates for lattice nuclear EFT time evolution and QPE (Watson; Spagnoli).
- Analog quantum measurement of the unitary-gas density and spin S(q,w) at finite T (Bragg).
- Supernova sensitivity: many-body NC corrections can flip 2D outcomes near criticality (Burrows et al., arXiv:1611.05859, Space Sci Rev 214, 33 (2018) [V-arXiv abs]). An axial strangeness g_A^s=-0.2 flips a 3D 20 Msun model (Melson et al., arXiv:1504.07631, ApJL 808 L42 [V-arXiv]). Code comparison finds many-body/strangeness corrections to be "modest" relative to ray-by-ray effects (Just et al., arXiv:1805.03953, search listing).

## 5. WHAT HAS NOT BEEN TESTED (in sources searched)
- Any quantum algorithm, resource estimate or hardware run for the **finite-temperature** response (S_V, S_A, spin-isospin) of **infinite/periodic** neutron or asymmetric nuclear matter.
- Any quantum-vs-classical comparison (E or F) for this observable.
- Any ab initio **real-frequency** (not static, not T=0) axial or spin-isospin response of hot matter with non-central (tensor/OPE) forces at Y_p>0.
- Lattice static S at Y_p>0 (flagged as future work in Ma 2024).

## 6. WHY THE GAP IS MATERIAL, AND WHERE IT IS COSMETIC

Cosmetic or closed parts of the candidate as written:
1. **Sign problem (audit Q2): answered, it is mostly absent.** LO pionless pure neutron matter is sign-free (positive-definite HMC integrand, Alexandru 2021). SU(4)-symmetric LO with Y_p>0 is also sign-free for spin-balanced matter in the grand-canonical ensemble (det_n^2 det_p^2 >= 0; standard lattice-EFT argument [author reasoning]). N3LO is reached perturbatively on top of it (Ma 2024), and spin-orbit can be made sign-free (Niu-Lu 2025). So "exponential advantage where the sign problem returns" does **not** hold for static or Euclidean quantities in the controlling window. The only residual hardness is the inversion to real frequency. That is an ill-conditioning problem, not an exponential-sign one, and classical inversion with UQ keeps improving.
2. **LO pionless is the wrong model for the axial lineshape.** With spin-conserving (central-contact) forces, total spin is conserved, so S_A(q->0, w) collapses to a delta at w=0. The physically relevant width (spin relaxation, which also sets pair bremsstrahlung) comes only from non-central/tensor forces (Lykasov-Pethick-Schwenk 2008; Bartl-Pethick-Schwenk 2014). A quantum LO-pionless S_A lineshape is therefore an exact solution of a model that lacks the relevant physics (Lesson 6). Including OPE/tensor forces raises quantum cost: Watson et al. rank pionful above pionless.
3. **Validation on the unitary gas** is already done by analog quantum simulators (Bragg and spin-Bragg). A digital reproduction adds no novelty there. It can only serve as a check.

Material parts that remain:
4. The **real-frequency spin and spin-isospin (Gamow-Teller) response of hot asymmetric matter with tensor forces**, at n~0.01-0.1 fm^-3, T~5-15 MeV, Y_p~0.05-0.3. No ab initio real-frequency result exists (only MF+RPA, Shin 2024, and Landau relaxation-time models). Lin-Steiner-Margueron (2023) identify exactly these residual spin/spin-isospin interactions as poorly constrained. Real-time evolution avoids analytic continuation, which is a genuine structural difference from E.

## 7. Audit-question answers (novelty-relevant)
- **(1) Controlling window vs EFT error.** The neutrinosphere and gain region sit at rho~1e11-1e13 g/cm^3, n~1e-4-6e-3 fm^-3, T~3-10 MeV (Guo 2024 uses this mapping). There the virial, lattice and BHF results agree to a few % (Ma 2024: ~5% in S_A at n~0.015 fm^-3; Guo 2024: S_A differences <=0.05). The solver spread there is therefore **not** clearly larger than the chiral truncation error. The spread grows at n>=0.03-0.06 fm^-3 (25% virial vs lattice), which matters more for proto-neutron-star cooling and the deeper decoupling region than for shock revival [author inference].
- **(2) Sign problem.** Answered in section 6.1. LO pure neutron matter is sign-free, so AFQMC plus inversion closes the static/Euclidean gap. The sign problem bites only in the non-perturbative treatment of non-SU(4) and tensor terms at larger density and lower T. Current practice treats those perturbatively and successfully up to about 0.05 fm^-3.
- **(3) Lineshape vs static S (Lesson 5).** The dynamic vs static change is 10-20%, energy-dependent (Guo 2024). Bedaque 2018 found near-exact scaling laws, which suggests low-dimensional lineshape information. The medium effect is dominated by static S_A suppression (10-30%). A large part of the opacity is fixed by S(q), sum rules and a relaxation width. The residual lineshape information is second-order but not zero.
- **(4) Multi-family disagreement.** Named points: T=10 MeV, n=0.0126 fm^-3 (z~0.62), where "RPA tends to overestimate S_A(0)" relative to BHF, and BHF macro vs micro S_V differs by up to 0.4 (Guo 2024). Also n~0.053 fm^-3 at T=20 MeV, where virial vs N3LO lattice S_A differ by ~25% (Ma 2024). These are **static** disagreements that classical lattice already arbitrates. No verified multi-family disagreement was found for the dynamic lineshape, because only one ab initio family is missing there.
- **(5) Resources [author order-of-magnitude, NOT from a paper].** Second quantization with Jordan-Wigner needs 4L^3 system qubits: 864 at L=6, 2048 at L=8, 4000 at L=10. First quantization at n=0.02 fm^-3 and a=1.32 fm gives ~0.046 nucleons/site, i.e. ~24 nucleons at L=8 and ~46 at L=10, which is ~400-700 system qubits. Double that for a purification/TFD thermal state, plus ancillas. Spectral resolution ~1 MeV against ||H|| of order 1e3-1e4 MeV means 1e3-1e4 block-encoding queries per shot, which gives roughly 1e9-1e11 T gates per shot for a pionful Hamiltonian. That total excludes thermal-state preparation, whose mixing time is unknown, and shot counts of 1e3-1e4 per (q, w-window). To be checked by the resources auditor against Watson et al. section 7 and appendix E (not extracted here).
- **(6) Outcome flip.** Outcome flips from ~10-20% NC opacity changes are documented only near explodability criticality (Burrows 2018; Melson 2015). A code comparison found such corrections "modest" (Just 2018). A lineshape-only correction of a few % in the controlling window is unlikely to flip outcomes robustly across progenitors [author inference].

## 8. WHY IT COULD STILL BE A NEW PAPER
A sharpened version: "Finite-T real-frequency spin and spin-isospin response of asymmetric nuclear matter with OPE/tensor forces. Quantum real-time/GIT versus Euclidean lattice + NN/MaxEnt inversion versus MF-RPA/Landau." This would be the first quantum treatment of a hot infinite-matter response (category B). It would supply a quantitative quantum-vs-classical inversion benchmark in a regime where the Euclidean side is sign-free, so the comparison isolates **real-time vs analytic continuation**. It could also be a clean negative result, which would be a publishable resource/necessity analysis. Claim category would be at most 3 (computational/resource advantage). It is not exponential in the controlling window.

## 9. SCOPED STATEMENT
In sources searched through 2026-09-28 (arXiv API and arXiv abstract search; OpenAlex title/abstract search; OpenAlex cited-by of Ma et al. PRL 132 232502 [W4399365972], Sobczyk et al. PRL 134 192701 [W4410293839], Roggero-Carlson PRC 100 034610 [W2796184659], Alexandru et al. PRL 126 132701 [W3047905376], Alexandru et al. PRC 101 045805 [W2960883686], Bedaque et al. PRC 98 015802 [W2785034571], Watson et al. arXiv:2312.05344 [W4389649801]; Crossref), we found (A) static ab initio S_V/S_A of hot neutron matter (lattice LO sign-free; N3LO perturbative), (B) dynamic S from virial/BHF-phenomenology/MF-RPA/Landau models, (C) T=0 real-frequency spin response (CC-GIT) and T=0 quantum response algorithms for nuclei, plus generic finite-T quantum response algorithms and nuclear-EFT quantum cost estimates. We found **no** quantum computation, quantum resource estimate or quantum-vs-classical study of (D) the finite-T real-frequency axial/spin-isospin response of hot (asymmetric) nuclear matter, compared with (E) Euclidean lattice/AFQMC plus inversion and (F) virial/BHF/RPA/Landau and CC-GIT. The absence of a paper is not proof.

## 10. VERDICT: WOUNDED
- Not killed, because the exact comparison does not exist and the real-frequency tensor-force spin/GT lineshape of hot asymmetric matter is a material, non-cosmetic gap.
- Wounded, for four reasons:
  - (i) The headline mechanism, the sign problem, is contradicted in the controlling window: LO neutron matter is sign-free, N3LO is perturbative, and spin-orbit can be sign-free.
  - (ii) The proposed LO-pionless model cannot produce the q->0 axial width.
  - (iii) The information in the lineshape is a 10-20% energy redistribution, largely constrained by static S and sum rules (Lesson 5).
  - (iv) Explosion-outcome sensitivity is established only near criticality.
- Required redesign: switch to a pionful/tensor Hamiltonian, asymmetric matter and the spin-isospin channel; pre-register the FULL-vs-ABLATION comparison as "quantum real-time" vs "sign-free Euclidean + best UQ inversion" at named state points (e.g. T=10 MeV, n=0.0126 and 0.05 fm^-3, Y_p=0.1).

---

## Query log
- WebSearch: budget exhausted (200/200) on the first call; no WebSearch results were used.
- arXiv export API (sortBy=submittedDate), before the HTTP 429 rate limit:
  - abs:quantum AND abs:neutrino AND abs:"dynamic structure factor" (0)
  - "quantum computer" AND "nuclear matter" (8)
  - "quantum computing" AND "response function" AND nuclear (1)
  - quantum AND "neutron matter" AND response (5)
  - "quantum algorithm" AND neutrino AND nuclear (0)
  - "quantum computer" AND pionless (3)
  - "nuclear lattice effective field theory" AND "quantum computing" (1)
  - finite temperature AND "dynamic structure factor" AND "quantum algorithm" (0)
  - "quantum computer" AND "unitary Fermi gas" (0)
  - au:Roggero AND quantum (40)
  - au:Bedaque AND neutrino (6)
  - "neutron matter" AND "spin response" (6)
  - "neutrino opacities" AND "neutron matter" (1)
  - "dynamic structure factor" AND "neutron matter" (4)
  - "dynamic structure factor" AND "unitary Fermi gas" (4)
  - neutrino AND "structure factor" AND supernova (13)
  - id_list abstract fetches for 2608.06515, 2604.13430, 2507.22814, 2507.14690, 1907.03914, 1801.07077, 2306.04500, 2407.20986, 2209.09962, 1504.07631, 1804.00689 (a different paper, discarded), 1612.02764, 2401.10737, 2206.10190, 1912.05105, 2312.05344
- arXiv web search (WebFetch arxiv.org/search), abstract field:
  - "neutron matter quantum computer" (41)
  - "structure factor neutrino quantum algorithm" (0)
  - "'spin response' quantum computer nuclear" (0)
  - "quantum computer response function nuclear" (26)
  - "unitary Fermi gas quantum simulation neutron matter" (3)
  - "finite temperature dynamical structure factor quantum computer" (21, none nuclear)
  - "neutrino nucleon hot dense matter quantum computing" (0)
  - "hot neutron matter" (2023+: 1)
  - "neutrino opacities structure factors supernova" (2023+: 1)
  - "supernova simulations sensitivity neutrino-nucleon scattering many-body corrections" (2)
  - "pure neutron matter quantum computing" (7, none on QC hardware or algorithms)
  - title search "Structure Factors of Neutron Matter at Finite Temperature"
- arXiv HTML reads: 2312.05344v3, 2401.10737v2, 2008.02824, 2306.04500v3; abs 1611.05859.
- OpenAlex:
  - DOI lookups for all journal versions above
  - cited-by: W4399365972, W4410293839, W2960883686, W2785034571, W2796184659 (108 citing works scanned), W3047905376, W4389649801
  - title_and_abstract searches ("quantum computer neutron matter", etc.; noisy, no relevant hits beyond 2608.06515)
- Crossref: Ma PRL DOI; Roggero-Carlson DOI; Burrows 2018 DOI 10.1007/s11214-017-0450-9; Bartl 2014 DOI 10.1103/physrevlett.113.081101; Horowitz 2017 DOI 10.1103/physrevc.95.025801; Watson (no journal version found).
- Not searched: patents (not relevant), theses (not found via these APIs), INSPIRE-HEP (not queried; a recommended follow-up).
