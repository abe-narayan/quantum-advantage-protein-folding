# Red team C01 (Hostile Reviewer #2: prior art / significance)

Date: 2026-09-28. Status: COMPLETE.

Candidate C01: correlated thermal S_ee(q,w) of partially degenerate warm dense matter (UEG -> H -> CH), r_s 2-4, theta 0.25-0.5, XRTS q ~ 0.4-4 k_F.

WebSearch: refused (session budget 200/200 exhausted). All searches via arXiv API / abs pages, OpenAlex, Crossref.

Prior audit (audit_C01_novelty.md) query log is taken as done; this pass targets (i) post-July-2026 preprints, (ii) the finite-T response-function algorithm literature, (iii) cited-by of the closest papers, (iv) domain significance (does anyone need real-frequency S at theta<0.5?).

## Query log (this pass, 2026-09-28)
1. WebSearch "quantum algorithm dynamic structure factor warm dense matter x-ray Thomson scattering": refused (budget 200/200).
2. arXiv API au:Baczewski, sorted by date (15): newest WDM-quantum item is still 2607.02811 (2026-07-02); 2609.12146 (QUOPS benchmarking, 2026-09-10) is not WDM. No quantum XRTS/S(q,w) paper.
3. arXiv API au:Kononov_A OR au:Bobrow OR au:Nelson_Jacob: no WDM thermal-state-preparation preprint (Bobrow et al. still unpublished on arXiv as of 2026-09-28 in this query).
4. arXiv API abs:"thermal state preparation" AND (plasma|warm dense|electron gas|jellium|first quantized): 0 hits.
5. arXiv API (Gibbs|thermal|finite temperature) AND (electron gas|jellium|warm dense|dense plasma) AND (quantum computer|algorithm|computing|qubits): only 2308.12352 relevant.
6. arXiv API ti:(finite temperature|thermal) AND ti:(correlation functions|response functions|structure factor|Green's functions|linear response|spectral) AND quantum computer/algorithm: 2605.29681 (Kosugi et al., finite-T QPE Green's functions, DMFT), 2405.19599 (Eklund & Ananth, hybrid real-time thermal correlation functions). None targets Coulomb continuum electrons.
7. OpenAlex cites:W4399208307 (Rubin PNAS 2024), sorted by date (27 works): no quantum S(q,w)/XRTS paper. Newest relevant: Chen & Chan PRL 2026 (10.1103/v2ms-wmz1), Pennati roadmap (10.1145/3774895.3815547), "Grand Challenge of Quantum Applications" (10.1103/6r9l-lynr), Kononov RT-TDDFT tutorial (10.1063/5.0312253), Trotter error with Coulomb potentials (10.1007/s00220-026-05593-6).
8. arXiv API au:Babbush_R and au:Babbush AND (plasma|warm dense|electron gas|structure factor|finite temperature|scattering|response function): Google items are 2607.13301 (magnon spectra/response functions on hardware), 2308.12352, 2301.01203. No WDM S(q,w).
9. arXiv API (inertial confinement|high energy density|fusion plasma) AND (fault-tolerant|quantum algorithm|quantum computer): electronic-structure entries only 2607.02811 and 2605.07722.
10. arXiv abs 2508.15765 (Chen & Chan): now PRL 137, 130601 (2026); no WDM content.
11. arXiv API (hydrogen|deuterium) AND (Thomson scattering|DSF|ITCF) AND (warm|dense): 22 hits, classical only (see Findings).
12. arXiv API au:Dornheim_T (incomplete author parsing) and abs:"path integral Monte Carlo" AND (warm dense|electron gas|electron liquid), sorted by date (35): see Findings F3.
13. arXiv abs 2506.10113 (Morresi et al.).
14. arXiv API (jellium|uniform/homogeneous electron gas) AND quantum computing terms (30): 10 hits, ground-state/Trotter only; none on finite-T dynamics, response, plasmons or S(q,w).
16. arXiv API au:Roggero AND (response|scattering) (19); arXiv abs 2507.22814.
17. arXiv API ti:(Gibbs|thermal|finite temperature) AND (electronic structure|ab initio|Coulomb|fermionic Hamiltonian|molecular) AND quantum algorithm (10); arXiv abs+html 2604.15263.
18. arXiv API (EELS|inelastic x-ray|Compton|DSF) AND quantum algorithm/computer (18): no finite-T electronic continuum DSF.
19. arXiv API (dielectric function|density response|plasmon|Kubo|conductivity) AND quantum algorithm AND (first quantization|plane wave|real-space|finite temperature): 0 relevant.
20. arXiv API abs:"Thomson scattering" AND (warm dense|XFEL|NIF|free-electron laser) sorted by date (35); arXiv abs 2509.10107, 2604.23687; arXiv html 2604.23687.
21. Crossref query.bibliographic "Inelastic x-ray scattering from shocked liquid deuterium" -> 10.1103/PhysRevLett.109.265003.
22. Crossref 10.1103/6r9l-lynr; arXiv ti:"grand challenge" -> 2511.09124; arXiv html 2511.09124v3.
23. arXiv abs 2607.10765 (irrelevant: Lee-Yang spectral gap).
15. OpenAlex title search for 2605.22920: HTTP 429. OpenAlex search for 2607.02811: not indexed (noise).
24. arXiv API (G1-G2|nonequilibrium Green|Kadanoff-Baym) AND (electron gas|warm dense|dense plasma|jellium) (10): no finite-T UEG DSF beyond RPA.
25. arXiv abs 2507.00688 (Moldabekov et al., MRE 11, 025401 (2026)).
26. arXiv API (au:Berry_D|Su_Yuan|Low_G|Kivlichan|Motta_M|Rubin_N|Malone_F|Arrazola) AND (plasma|warm dense|structure factor|finite temperature|electron gas|response function|stopping power): only 2508.15935.
27. OpenAlex search for 2508.15935: HTTP 429. Semantic Scholar citations of arXiv:2508.15935 (7): RIXS 2602.20270, EUV 2602.20234, core spectra 2511.17985, Grand Challenge 2511.09124, two generic. No finite-T/WDM follow-up.
28. Semantic Scholar citations of arXiv:2605.22920: none indexed.
29. Semantic Scholar citations of arXiv:2301.01203 (Babbush 2023), 2025-2026 (23): only WDM item is the WDM roadmap 2505.02494; Flew & Kassal arXiv:2510.02784 ("any type of spectroscopy", molecules, time domain) noted as generic nearby work.
30. arXiv abs 2510.02784.
31. Crossref query.bibliographic "quantum computer warm dense matter structure factor Thomson", from 2024-06-01 (20): only QC item is Baczewski, "Quantum computing and warm dense matter", SNL report 10.2172/3028616 (2025-04). Two Dornheim LLNL/OSTI reports (10.2172/3682406, 10.2172/3662052, 2026-09) are classical.
32. arXiv API "Thomson scattering" AND (Bayesian|posterior|MCMC|UQ|inference) AND (warm dense|dense) (13): no paper decomposes model vs instrument contributions to the XRTS posterior, or compares real-frequency vs ITCF inference quantitatively.
33. arXiv abs 2503.14014 (Bellenbaum et al.).



## Findings
- F1 No quantum S_ee(q,w)/XRTS paper through 2026-09-28 in queries 2-9, 14, 16-18. Sandia intent (2605.22920) still unrealised on arXiv; Bobrow et al. thermal-prep cost paper not on arXiv.
- F2 Google Quantum AI, "The Grand Challenge of Quantum Applications", arXiv:2511.09124 / PRX Quantum 7, 020101 (2026), doi:10.1103/6r9l-lynr: Table 4 lists "Stopping power for inertial fusion, 218 electrons, Plausible beyond TDDFT, 6200 [logical qubits], 1e15 [Toffoli]" in the furthest horizon; no XRTS/S(q,w) entry.
- F3 UEG static at theta=0.25: Morresi, Garberoglio, Xiong, Xiong, arXiv:2506.10113 (2025): energy, S(q), n(k) of UEG for theta=0.25-1.0, r_s=0.5-80 via parametrized (xi) partition functions. N and ITCF not stated in abstract. Weakens "UEG theta=0.25 is a classical wall" for static; the dynamic/ITCF level is not shown.
- F4 Becker, Rouze, Salzmann, arXiv:2604.15263 (2026-04): first rigorous mixing-time guarantee for Gibbs sampling of a Coulomb continuous-variable system (d=2,3), but distinguishable (Boltzmann) particles in a harmonic trap; no fermion antisymmetry, so it does not cover degenerate electrons (gate 3 stays open). Nearby prior art (B).
- F5 Nuclear-physics analogue: dynamic linear response of many-fermion systems at momentum q on quantum computers is an established genre (Roggero & Carlson arXiv:1804.01505; Roggero arXiv:2004.04889 GIT; Baroni et al. arXiv:2111.02982; Spagnoli, Lissoni, Roggero arXiv:2507.22814 first-quantized nuclear dynamics, "tens of millions of T gates, few hundred logical qubits"). Zero temperature. A referee can cite these to argue the algorithmic content of C01 is transplanted.
- F6 Significance: XRTS overview Dornheim, Bellenbaum, Gawne, Vorberger, Gericke arXiv:2604.23687 (2026): "PIMC does not give direct access to See(q,w) itself, but yields its two-sided Laplace transform"; LR/RT-TDDFT are "computationally expensive but practical"; "the most difficult frontier will be the consistent treatment of non-equilibrium effects". Tabulated experiments in the C01 regime: OMEGA planar-shock D at 0.7-0.8 g/cc, Te 0.7-5 eV; OMEGA shocked liquid D, n_e=2.2e23 cm^-3, Te=8+-5 eV (Regan et al. PRL 109, 265003 (2012), doi:10.1103/PhysRevLett.109.265003). At r_s~1.9, E_F~14 eV, so theta ~0.05-0.6 [ESTIMATE]. The reported Te uncertainty (+-60%) is experimental, not theory-limited.
- F7 Where the community currently needs better real-frequency theory, the cases are near-solid metals (EuXFEL Al, Si, Cu; Bespalov et al. arXiv:2509.10107, doi:10.1103/86cw-8wm5: UEG models overestimate plasmon by up to 8 eV, an ab initio (disorder-aware) approach agrees within error). Classical ab initio (TDDFT) resolved it; no correlation-beyond-TDDFT failure is documented there.

- F8 Bellenbaum, Bohme, Bonitz, Doppner, Fletcher, Gawne, Kraus, Moldabekov, Schwalbe, Vorberger, Dornheim, arXiv:2503.14014 (2025): PIMC for warm dense H shows "decreasing sensitivity of the dynamic structure factor with respect to both ionization and continuum lowering for increasing scattering angles". Z inference for H from S is weakly informative at large q, which bears on the (rho,T,Z) posterior claim (lesson 5).
- F9 Finite-T response algorithm literature (nearby, B): Kosugi et al. arXiv:2605.29681 (finite-T QPE Green's functions, DMFT); Eklund & Ananth arXiv:2405.19599 (hybrid real-time thermal correlation functions); Lee et al. arXiv:2206.05571 (TFD finite-T dynamics, variational); Ding, Li, Lin arXiv:2404.05998 (KMS Gibbs samplers, generic); Flew & Kassal arXiv:2510.02784. None targets degenerate Coulomb continuum electrons at finite q.
- F10 Nothing in the Google (Babbush, Rubin, Berry, Low), Xanadu (Arrazola, Kunitsa, Stetina) or Sandia (Baczewski, Kononov, Nelson, Pathak) author queries shows a finite-T S(q,w) paper through 2026-09-28. Queries for PsiQuantum, Quantinuum, IBM, Microsoft, Phasecraft, QSimulate, Riverlane, Algorithmiq and BlueQubit were only possible through generic abstract searches (WebSearch unavailable), which return no hits. Group pages were not checked. This is a coverage gap.
- F11 No classical multi-family (NEGF G1-G2, qSTLS, ph-FT-AFQMC, WPMD, stochastic TDDFT) comparison of S(q,w) at theta<=0.5 for H was found (queries 11, 12, 24). That gap is both the opportunity and the risk: the "wall" is asserted by one group (Moldabekov/Dornheim) and has not been stress-tested.

## Hostile Reviewer #2 verdict: WOUNDED (not fatal); significance is the main weakness

### Q1. Has the exact quantum-vs-classical comparison been done?
No, in the sources searched (arXiv API, arXiv abs/html, OpenAlex cited-by for Rubin 2024, Semantic Scholar cited-by for 2508.15935, 2605.22920 and 2301.01203, and Crossref through 2026-09-28): there is no quantum computation or resource estimate for the thermal electronic S_ee(q,w) of the UEG, H or CH at XRTS wavevectors, and no comparison against PIMC+AC/ITCF or LR-TDDFT. Scoped category **B** stands. Coverage gaps: no WebSearch, no group pages, and OpenAlex returned 429 twice.

### Q2. Is the novelty gap cosmetic?
Partly. Every algorithmic component is published:
- first-quantized plane-wave WDM dynamics at finite T with sampled determinants (Rubin et al. 2024);
- exact dynamics vs mean field, "most pronounced at finite temperature" (Babbush et al. 2023);
- a quantum algorithm for the electronic DSF at T=0 (Kunitsa et al. 2025);
- dynamic linear response on quantum computers (Roggero & Carlson 2018; Roggero 2020 GIT; Baroni et al. 2021);
- finite-T Green's functions announced for WDM (Nelson & Baczewski 2026);
- a Coulomb Gibbs sampler with a mixing-time guarantee, for Boltzmann particles only (Becker, Rouze, Salzmann 2026).

A C01 paper is an application/regime/benchmark contribution. Two pieces are not in any of these papers:
1. The exact UEG cross-check. The Laplace transform of the quantum S must match PIMC F(q,tau) at theta>=0.5.
2. A map of where the classical wall lies at theta<0.5.

The one component that would be new as an algorithm, a correlated degenerate-fermion Gibbs state for first-quantized Coulomb electrons with bounded cost, is unsolved. The Sandia group (Bobrow et al., in prep) is costing it.

### Q3. Is there enough practical value outside quantum computing?
It has not been shown.
- The XRTS community's stated frontier is non-equilibrium (2604.23687: "the most difficult frontier will be the consistent treatment of non-equilibrium effects"). The equilibrium theta<0.5 regime is not named there as the bottleneck.
- Temperature is extracted model-free from the ITCF (2211.00579, 2510.26747). A real-frequency S therefore adds information only where F(q,tau) is unavailable. Gate K-C01a is decisive.
- Measured data do exist in the C01 regime: OMEGA shocked D, Regan et al. PRL 2012, Te=8+-5 eV at n_e=2.2e23 cm^-3, plus OMEGA planar-shock D at 0.7-0.8 g/cc and 0.7-5 eV. Their error bars are experimental (+-60% on Te), so theory accuracy is unlikely to move the inference.
- Where real-frequency theory did change conclusions (EuXFEL Al, 2509.10107), classical ab initio TDDFT with disorder settled it.

### Q4. Would domain scientists find the benchmark credible?
- The UEG rung: yes. PIMC F(q,tau) comparison is the community's own standard. But the UEG at theta=0.25 has static PIMC results (2506.10113), and UEG S(q,w) converges at N=14 through the dynamic LFC. The UEG is validation only, not an advantage target.
- The H rung at r_s=2, theta 0.25-0.5: only as theory-vs-theory. No XRTS data at that exact point were found. The "PIMC unavailable" wall comes from one group (2507.00688) and has not been stress-tested by other families (F11).

### Scoop and priority
HIGH.
- DOE FES "Foundations for quantum simulation of warm dense matter" (Sandia) has published stopping power, opacity (2607.02811) and finite-T GF (2605.22920, which states WDM linear response as ongoing work). Thermal-state costing is in preparation. Kononov and Baczewski co-author the XRTS analysis papers with the Dornheim group (2510.26747).
- Google's Grand Challenge (2511.09124) lists stopping power as "plausible beyond TDDFT" at 1e15 Toffoli, in the furthest horizon. The same group could produce an XRTS variant at low marginal cost.

### Required revisions (for C01 to survive Reviewer #2)
1. Run K-C01a (information gate) before any quantum work. Use real XRTS setups: OMEGA shocked D (Regan 2012) and LCLS/FLASH/EuXFEL H jets. Report the posterior shift of real-frequency S over ITCF with the instrument function included. If it is below 2x, reframe or kill.
2. Reposition the claim. Do not claim category 3 against TDDFT (the gain is polynomial). State category 3 against exact finite-T fermion dynamics, and make "accuracy beyond adiabatic kernels at bounded cost" the practical claim. State plainly that the UEG rung is validation, not advantage (2506.10113, 2004.13429).
3. Name and differentiate the prior art in the paper: Rubin 2024, Babbush 2023, Kunitsa 2025, Roggero & Carlson 2018 / Roggero 2020, Nelson & Baczewski 2026, Pathak/Kononov/Baczewski 2026, Becker/Rouze/Salzmann 2026, Chen & Chan PRL 2026, Grand Challenge 2026. The contribution is the observable, the exact cross-check and the wall map.
4. Treat degenerate-fermion Gibbs preparation as an explicit open item. Becker et al. cover only Boltzmann particles in a trap. Either cost a fermionic sampler, or bound the Mermin-determinant bias on S(q,w) with a UEG test against PIMC F(q,tau) at theta=0.5.
5. Stress-test the classical wall across method families (F11) before claiming it: xi/Taylor-xi PIMC at N=14-32, ph-FT-AFQMC, qSTLS/dynamic-LFC, stochastic and mixed TDDFT (White), WPMD, G1-G2.
6. Priority: publish a short UEG-validated resource paper quickly, or contact the Sandia group. A Pathak/Nelson/Bobrow preprint would reduce C01 to a replication.
7. Keep the non-equilibrium XFEL-heated pivot (2402.09005, 2604.23687 frontier statement) as the fallback, where PIMC/ITCF do not apply. The initial-state model floor must then be quantified (lesson 6).

### Fatal objections
None fatal on prior-art grounds. The comparison has not been published. Significance is conditional on gate K-C01a.

## Citations verified this pass (beyond audit_C01_*.md)
- arXiv:2511.09124 / doi:10.1103/6r9l-lynr (Babbush et al., PRX Quantum 7, 020101, 2026): arXiv abs/html, Crossref
- arXiv:2506.10113 (Morresi, Garberoglio, Xiong, Xiong 2025): arXiv abs
- arXiv:2604.15263 (Becker, Rouze, Salzmann 2026): arXiv abs + html
- arXiv:2604.23687 (Dornheim, Bellenbaum, Gawne, Vorberger, Gericke 2026): arXiv abs + html
- arXiv:2509.10107 / doi:10.1103/86cw-8wm5 (Bespalov et al.): arXiv abs
- doi:10.1103/PhysRevLett.109.265003 (Regan et al. PRL 2012): Crossref
- arXiv:2503.14014 (Bellenbaum et al. 2025): arXiv abs
- arXiv:2507.22814 (Spagnoli, Lissoni, Roggero): arXiv abs; arXiv:1804.01505, 2004.04889, 2111.02982 (Roggero et al.): arXiv API listing only
- arXiv:2508.15765 (Chen & Chan, PRL 137, 130601 (2026)): arXiv abs
- arXiv:2510.02784 (Flew & Kassal 2025): arXiv abs
- arXiv:2605.29681, 2405.19599, 2206.05571, 2404.05998: arXiv API listing only
- doi:10.2172/3028616 (Baczewski, SNL report 2025): Crossref
- arXiv:2507.00688 (Moldabekov et al., MRE 11, 025401 (2026)): arXiv abs
- arXiv:2609.12146 (QUOPS, 2026-09-10): arXiv API listing only
