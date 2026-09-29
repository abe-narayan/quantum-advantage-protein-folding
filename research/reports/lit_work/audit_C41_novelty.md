# Novelty audit C41: correlated multi-electron photo/strong-field ionization, joint momentum sampling

Auditor role: NOVELTY / PRIOR-ART. Date: 2026-09-28. Status: COMPLETE.
Verdict: **WOUNDED** (novelty category **B** survives for the exact formulation, but the quantum mechanism is already published in nearby problems, eta=2 is classically done, and the eta>=3 experimental observable is already matched by a cheap semiclassical model; decision relevance and shot cost are the weak points, not novelty).

---

## 1. Query log (all run 2026-09-28)

WebSearch: budget exhausted (200/200) on first call. All searches below via arXiv API / arXiv web search (WebFetch), OpenAlex, Crossref, Semantic Scholar. arXiv export API and OpenAlex returned HTTP 429 intermittently (shared with other agents); failed calls were retried or rerouted.

| # | Source | Query | Result |
|---|---|---|---|
| 1 | arXiv API | abs:"quantum computer" AND abs:ionization AND (strong-field OR attosecond OR "double ionization" OR photoionization) | 1 hit, 2108.11772 (attosecond entanglement experiment, not QC algorithm) |
| 2 | OpenAlex t&a | ("quantum computer" OR "quantum algorithm" OR qubits) AND (strong-field OR attosecond OR high-harmonic OR "multiphoton ionization") | 123 hits; 1 relevant: Gi et al. 2024 (HHG, 1D He, hardware) |
| 3 | OpenAlex t&a | (QC terms) AND (photoionization OR "double ionization" OR "photoelectron spectrum" OR "electron continuum") | 18 hits, none a QC algorithm for ionization (all ion-trap loading etc.) |
| 4 | OpenAlex t&a | (QC terms) AND "time-dependent Schrodinger" AND (atom OR ionization OR continuum OR grid) | 3 hits: Mangin-Brinet 2024 (CAP on QC); H+H2 S-matrix |
| 5 | OpenAlex t&a | (QC terms) AND ("intense laser" OR "laser field" OR "laser pulse") AND (ionization OR harmonic) | 8 hits; relevant only Gi et al. 2024 |
| 6 | OpenAlex t&a | (QC terms) AND ("complex absorbing potential" OR "electron continuum" OR "ionization dynamics" OR ICD OR Auger) | 12 hits: Langkabel & Bande 2022; Jin et al. SISC 2024; An-Liu-Lin LCHS PRL 2023; CAP resonance-QC JCTC 2026 |
| 7 | arXiv web | abstract: quantum computer high harmonic generation | no QC-for-atomic-HHG paper |
| 8 | arXiv web | abstract: "quantum computer" ionization electron laser | 2205.10543 (Langkabel & Bande) |
| 9 | arXiv web | abstract: "quantum computer" attosecond | 2112.06365 (Wang & Krstic, H bound states in attosecond pulse, variational) |
| 10 | arXiv web | abstract: "double ionization"/"photoelectron momentum"/photoionization + "quantum algorithm" | none relevant |
| 11 | arXiv adv | abstract: photoionization AND "quantum computer" | 6 hits, none relevant (ion loading) |
| 12 | arXiv adv | abstract: ionization AND "quantum algorithm" | 3 hits, none relevant |
| 13 | arXiv adv | abstract: "harmonic generation" AND "quantum computer" | 21 hits; only 2311.14035 (magnon HHG in spin model, variational) |
| 14 | arXiv author | Sato, Takeshi (TD-CASSCF/TD-OCC developer) | found 2603.12859 (Auger via GQE), 2509.04869, TD-OCC series; no QC paper on multi-electron ionization |
| 15 | OpenAlex cited-by | cites:W4309409792/W4281476751 (Langkabel & Bande) | 8 works; none on multi-electron ionization |
| 16 | OpenAlex cited-by | cites:W4389116416 (Mangin-Brinet CAP) | 7 works; scattering phase shift on QC (PRD 2026), photodissociation on QC (JPCL 2026); none on ionization |
| 17 | OpenAlex cited-by | cites:W3165437982 (Su et al. first quantization) filtered (ionization/laser/photoelectron/attosecond/scattering/continuum/stopping/dynamics) | 32 works; stopping power, Babbush 2023, Chan 2023, Pauli-Fierz, singlet fission; none on multi-electron ionization |
| 18 | OpenAlex cited-by | cites:W4322726929 (Chan et al. grid methods) | 49 works; none on ionization of >=2 electrons |
| 19 | OpenAlex cited-by | cites:W4383695264 (Babbush exact electron dynamics) filtered to ionization/laser/photoemission | 429 / no relevant |
| 20 | OpenAlex cited-by | cites:W7131452312 (Kharazi EUV) | 0 citing works |
| 21 | OpenAlex t&a | (QC terms) AND ("photoemission spectrum" OR "photoelectron spectra" OR "momentum distribution") | only 2602.20234 |
| 22 | Crossref | quantum computer simulation double ionization helium two-electron | no QC work |
| 23 | Crossref | quantum algorithm strong-field ionization tunnel above-threshold qubits | no QC work |
| 24 | Crossref | triple photoionization of lithium fully differential | classical TDCC, experiments (see Sec. 4) |
| 25 | Crossref | nonsequential triple ionization Ne/Ar coincidence | semiclassical/reduced-dim works |
| 26 | Crossref | three-electron model strong field (reduced dimensionality) | Efimov et al. 2021/2023/2025 |
| 27 | Crossref | RMT double ionization two-electron outer region | Plummer & Noble 2020 (double-continuum R-matrix) |
| 28 | Crossref | full-dimensional ab initio NSDI helium 800 nm | Zielinski-Majety-Scrinzi 2016 (3+3D tSURFF) |
| 29 | OpenAlex cited-by | cites:W3157758122 (Efimov 3-electron 2021) | 12 works: Emmanouilidou ECBB series, Dalitz-plot comparison 2025, Ne three-electron escape 2025 |
| 30 | Crossref | TD-RASCI double ionization; MCTDHF double ionization convergence | Hochstuhl & Bonitz 2012; Bauch 2014; no eta=3 convergence study found |
| 31 | arXiv id_list | 2603.12859, 2112.06365, 2205.10543, 2602.20234, 2308.12352, 2601.08793, 2304.00667, 2105.12767, 2202.05864 | metadata/abstracts verified |
| 32 | Semantic Scholar | DOI lookups 10.1103/43wt-x129, 10.1103/1dn8-4f6h, 10.1103/PhysRevA.93.023406, 10.1088/0953-4075/39/8/006 | abstracts/arXiv ids verified where available |

---

## 2. EXACT PRIOR WORK (the C41 formulation itself)

In the sources above, **no paper** proposes or costs a quantum algorithm that samples the joint multi-electron (eta>=2, and specifically eta>=3) photoelectron momentum distribution of an atom or molecule in a photo- or strong-field ionization process, nor any paper comparing such an algorithm with RMT, TD-CASSCF, TD-RASCI/ORMAS, MCTDHF, TDCC, tSURFF or semiclassical (ECBB/CTMC) methods.

## 3. NEAREST QUANTUM WORK (all verified)

| Work | What it does | Distance from C41 |
|---|---|---|
| Kharazi, Fomichev, Kanno, Kobayashi, Arrazola, Gao, Stetina, arXiv:2602.20234 (2026), "Quantum Simulations for EUV Photolithography" | First-quantized plane-wave algorithm computing the **photoemission spectrum via real-time dynamics treating bound and continuum states on equal footing**; resource counts: >=1e14 gates, 1e4 shots, several thousand logical qubits for a photoresist monomer | **Same mechanism** (first-quantized continuum dynamics + photoelectron spectrum readout). Different target: single-photon EUV photoemission of a molecule, single-electron spectrum, no multi-electron joint momentum, no strong field. Its resource counts are an upper anchor for C41. |
| Chan, Meister, Jones, Tew, Benjamin, Sci. Adv. 9, eabo7484 (2023), arXiv:2202.05864, doi:10.1126/sciadv.abo7484 | Emulated (<=36 qubit) first-quantized SO-QFT grid simulation of 2D/3D atoms incl. **field ionization of 2D H** (9 qubits/dim) and **two-electron 2D e + H scattering with ionization** (6 qubits/coordinate), antisymmetrized, ancilla-based attenuation readout | Same mechanism at toy scale, eta<=2, 2D, static field, no momentum-distribution sampling, no classical comparison beyond a memory remark |
| Langkabel & Bande, JCTC 18, 7082 (2022), arXiv:2205.10543, doi:10.1021/acs.jctc.2c00878 | Laser-driven electron dynamics (LiH) with Trotter/JW; ionization of H2 via complex absorbing potential (QITE-like non-unitary step); compared with TD-FCI on a simulator | Second-quantized Gaussian basis, CAP destroys continuum information; no momentum distributions |
| Gi, Orimo, Ishikawa, Kawashima, Gujarati, Sato, Optica EUVXRAY 2024 JTu4A.11, doi:10.1364/euvxray.2024.jtu4a.11 | HHG from **1D helium model** on actual quantum hardware with TD-optimized UCC / Natural-Expansion ansatz | Proof-of-concept by the TD-CASSCF/TD-OCC group itself; 1D, HHG not joint momenta; conference abstract only (no journal version found) |
| Wang & Krstic, arXiv:2112.06365 (J. Phys. Commun. 2023, doi:10.1088/2399-6528/ace67a per OpenAlex W4383873776) | Variational (McLachlan) NISQ dynamics of 16 bound hydrogenic states in a strong attosecond pulse | Bound-state only, one electron |
| Mangin-Brinet, Zhang, Lacroix, Ruiz Guzman, Quantum 8, 1311 (2024), doi:10.22331/q-2024-04-08-1311 | Non-unitary TDSE with complex absorbing potential on a QC (dilation, one ancilla) | 1D enabling primitive for absorbing boundaries |
| Jin, Liu, Li, Yu, arXiv:2304.00667 (SIAM J. Sci. Comput. 2024, doi:10.1137/23m1563451) | Schrodingerisation for artificial boundary conditions (CAP, PML, DtN) "when simulating quantum dynamics that involves the emission of electrons" | Enabling primitive; no multi-electron application |
| Babbush et al., Nat. Commun. 14, 4058 (2023), arXiv:2301.01203, doi:10.1038/s41467-023-39024-0 | First-quantized exact electron dynamics beats RT-TDHF/TDDFT in space and polynomially in basis size; k-RDM sampling polylog | Suggested targets are warm/hot dense matter and molecules near metal surfaces; no ionization/strong-field target |
| Rubin et al., PNAS 121 (2024), arXiv:2308.12352, doi:10.1073/pnas.2317772121 | First-quantized stopping power (projectile + electrons, finite T) | Same resource framework; different observable |
| Su, Berry, Wiebe, Rubin, Babbush, PRX Quantum 2, 040332 (2021), arXiv:2105.12767 | Explicit first-quantized qubitization / interaction-picture costs, incl. real-space variants | Cost backbone for C41 |
| Keithley et al., arXiv:2603.12859 (2026) | Auger spectra via GQE + qSC-EOM + one-centre approximation (water, STO-3G) | Continuum-adjacent spectroscopy on QC, but bound-state-only method; no continuum dynamics |

## 4. NEAREST CLASSICAL WORK (verified unless marked)

eta = 2 (validation regime, classically solved):
- Zielinski, Majety, Scrinzi, PRA 93, 023406 (2016), arXiv:1511.06655: ab initio **full 3+3 dimensional** He double-photoelectron momentum spectra at XUV and **780 nm**, tSURFF extended to 3+3D with systematic error control; reproduces experimental single/double ratio up to 4e14 W/cm^2; gives joint angular distributions.
- Plummer & Noble, J. Phys. Conf. Ser. 1412, 132053 (2020): double-continuum R-matrix (RMT) inner-region codes for laser-induced double ionization of many-electron atoms, up to two continuum electrons.
- Hikosaka et al., PRR (2026), doi:10.1103/x7zf-dx8m: Ar photo-double-ionization with XUV double pulses; interference revealing **nonseparable two-electron wavefunctions** (experiment that consumes joint two-electron information).

eta = 3, single-photon (XUV/synchrotron):
- Colgan & Pindzola, J. Phys. B 39 (2006), doi:10.1088/0953-4075/39/8/006 (page numbers not checked): TDCC **energy-differential cross sections for Li triple photoionization** (ab initio, three continuum electrons) (abstract elided by publisher; title/DOI verified).
- Experiments: Wehlitz et al., PRL 81, 1813 (1998) doi:10.1103/physrevlett.81.1813; Wehlitz et al. PRA 61, 030704 (2000); Juranic et al., PRA 78, 033401 (2008) (triple photoionization of Li up to 650 eV). These report **total** (or near-total) cross sections, i.e. scalars.
- Classical-trajectory treatment: Emmanouilidou, J. Phys. B 39 (2006) doi:10.1088/0953-4075/39/20/003 and doi:10.1088/0953-4075/39/5/l04 (near-threshold).
- No fully differential (joint three-electron momentum) Li triple-photoionization measurement found in these sources.

eta = 3, strong field (NSTI):
- Efimov, Maksymov, Ciappina, Prauzner-Bechcicki, Lewenstein, Zakrzewski, Opt. Express 29 (2021) doi:10.1364/oe.431572: **restricted-dimensionality ab initio TDSE** for three active electrons; Dalitz plots of three outgoing momenta; Pauli/spin signatures.
- Efimov et al., PRA 108, 033103 (2023); Efimov, PRA (2025) doi:10.1103/1dn8-4f6h.
- Peters, Katsoulis, Emmanouilidou, PRA 105, 043102 (2022): 3D semiclassical ECBB model for triple ionization, compared to experiment.
- Emmanouilidou, Peters, Katsoulis, PRA 107, L041101 (2023): 3D classical model "ionization spectra that agree with experiment".
- Praill, Katsoulis, Emmanouilidou, J. Phys. B (2025) doi:10.1088/1361-6455/ae2e65: Ne double/triple ionization, **"very good agreement with experimental results, particularly for triple ionization"** after focal-volume averaging (observable: distribution of the SUM of momenta along the field, i.e. recoil-ion momentum).
- Efimov, Katsoulis, Rozpetkowski, Chwalowski, Emmanouilidou, Prauzner-Bechcicki, PRA (2025) doi:10.1103/43wt-x129, arXiv:2410.16797: reduced-dimensional quantum model vs two 3D semiclassical models on Dalitz plots; better agreement between quantum and ECBB; central spot reproduced by all models. **No full-3D quantum reference exists to adjudicate.**
- Jiang et al., PRA 104, 023113 (2021) (semiclassical NSTI of Ar); PRA 105, 053119 (2022) (Dalitz plots).

Correlated wavefunction TD methods (single/double ionization, not eta=3 joint continuum):
- TD-CASSCF / TD-OCC hierarchy (Sato, Pathak, Orimo, Ishikawa; e.g., arXiv:2104.10565: TD-OCCDT(4) nearly reproduces TD-CASSCF for Ne, Ar; arXiv:2211.10116 review; arXiv:1903.10743 tSURFF in TD-MCSCF). Verified via arXiv author listing.
- Hochstuhl & Bonitz, PRA 86, 053424 (2012) TD-RASCI photoionization; Bauch et al. PRA 90, 062508 (2014) TD-GASCI.
- No study found that converges TD-RASCI/TD-CASSCF/MCTDHF for **three-electron joint continuum momenta** in full 3D.

## 5. WHAT HAS BEEN TESTED
- First-quantized continuum-including real-time quantum algorithms with photoemission-spectrum readout: costed (Kharazi 2026) for single-photon molecular photoemission.
- Two-particle grid scattering/ionization: emulated in 2D at 25 qubits (Chan 2023).
- Absorbing boundaries on QC: 1D algorithms (Mangin-Brinet 2024; Jin et al. 2024).
- Laser-driven dynamics with CAP ionization in Gaussian basis (Langkabel & Bande 2022); 1D-He HHG on hardware (Gi et al. 2024).
- Classically: eta=2 full-dimensional joint momenta at 780 nm (Zielinski 2016); eta=3 Li triple photoionization energy-differential (TDCC, 2006); eta=3 strong-field with reduced-dimension quantum and 3D semiclassical models, the latter matching measured Ne3+ momentum sums.

## 6. WHAT HAS NOT BEEN TESTED
- Any quantum algorithm (costed or emulated) for eta>=3 correlated ionization with joint momentum sampling.
- Any quantum-vs-classical comparison (resource or accuracy) against RMT, TD-CASSCF, TD-RASCI, MCTDHF, TDCC, or ECBB/Heisenberg semiclassical models for multiple ionization.
- Any full-3D quantum-mechanical reference for three-electron strong-field escape (the Dalitz-plot disagreement between reduced-dim quantum and 3D semiclassical models is unresolved).
- Convergence of RAS/orbital-truncated TD methods for eta=3 joint continuum momenta.

## 7. WHY THE GAP IS MATERIAL (and where it is cosmetic)
Material:
- The classical frontier for eta=3 in strong fields is split: exact quantum only in restricted geometry, 3D only semiclassically. A full-3D fermionic 9-coordinate TDSE with long IR excursion is out of classical grid reach (memory ~N^(3*eta)); tSURFF/irECS shrink the box only for a few continuum electrons. A quantum computation would supply an adjudicating reference, which is a distinct observable (joint three-electron momenta, spin/Pauli signatures on Dalitz plots) from anything in Kharazi 2026 or Chan 2023.
- Mechanism distinctions from Kharazi 2026: multiple correlated continuum electrons, strong time-dependent field (interaction picture), rare-channel post-selection.
Cosmetic/weak:
- Algorithmic mechanism (first-quantized grid + QFT momentum readout + real-time continuum) is already published (Kharazi 2026, Chan 2023, Su 2021). A C41 paper is a new application/costing, not a new primitive.
- eta=2 is classically solved at 780 nm (Zielinski 2016) and by RMT-DI; any He demonstration is validation only.
- For Li triple photoionization, the experimental observable is a scalar cross section already computed by TDCC; no fully differential data found.

## 8. HARD-FILTER ATTACKS (lessons L1-L7), answers to audit questions
Q1 (converged methods disagreeing with experiment beyond error bars): Not found. For Ne NSTI, the 3D semiclassical ECBB model already reports very good agreement with the measured triple-ionization momentum-sum spectra after focal averaging (Praill 2025). Disagreement exists only between MODELS (reduced-dim quantum vs 3D semiclassical Dalitz plots, Efimov 2025), not vs experiment. L1/L7 risk: a cheap classical model already hits the measured marginal.
Q2 (RAS convergence for eta=3): no convergence study found in either direction; open. This must be tested before any advantage claim (L5: single-family convergence is not convergence).
Q3 (honest qubits/Toffoli; auditor order-of-magnitude, UNVERIFIED estimate, not from literature): Ne NSTI at 800 nm, 1e15 W/cm^2 (Up ~2.2 au, quiver ~52 au). To read momenta by QFT without absorbing boundaries the whole continuum must stay in the box: L ~ 2 p_max T ~ 1e4 au; spacing ~0.2 au (p_max ~6.6 au, cusp/pseudopotential) -> N_1D ~ 5e4-7.5e4 -> ~16-17 qubits/coordinate -> ~150 system qubits for eta=3 (~400 for all 8 Ne valence electrons), several hundred to ~1000 logical qubits with arithmetic ancillas. lambda*t ~ 1e6 (kinetic cutoff dominated) -> roughly 1e9-1e11 Toffoli per shot. Absorbing boundaries (CAP/Schrodingerisation) reduce box but destroy joint momentum information, and their success probability equals the survival norm. Classical codes use tSURFF boxes of ~1e2 au; the quantum box is ~100x larger per dimension.
Q4 (shot budget): triple ionization at these intensities is ~1e-3 to 1e-5 of events (UNVERIFIED typical range). 1e4 triple events for a Dalitz plot -> 1e7-1e9 shots x 1e9-1e11 Toffoli; amplitude amplification onto the "all three electrons outside R" subspace (cheap predicate) gives only sqrt(1/p) ~ 30-300 forward+backward evolutions per event -> ~1e15-1e18 Toffoli total. At 1e6 Toffoli/s: years to millennia on one machine. Kharazi 2026 already needs >=1e14 gates per circuit for a simpler single-photon spectrum. Quadratic amplification does not rescue this (L3).
Q5 (does experiment consume joint information?): Mostly no. NSTI experiments report recoil-ion momentum sums (low-order marginal); Li triple experiments report total cross sections. Counterexamples: Hikosaka 2026 (nonseparable two-electron wavefunctions, eta=2, Ar) and He NSDI two-electron correlation maps (eta=2, classically solved). L5 risk is high: the informative-and-measured observables are classically computable; the classically hard eta>=3 joint distributions are currently not measured with full coincidence in the sources found.
Q6 (model floor for Ne/Ar): Three-active-electron frozen-core models neglect the other 5 (Ne) valence electrons and core polarization; experimental floors (focal-volume averaging, intensity calibration typically +-10-20%, CEP/pulse-shape averaging) enter every comparison. Solver error is unlikely to dominate these (L6). The single-photon Li case has a small model floor (all-electron, eta=3) but lacks differential data and is classically covered by TDCC.

## 9. WHY IT COULD STILL BE A NEW PAPER
- A first resource estimate (qubits, Toffoli, shots, box size, boundary treatment) for full-3D eta=3 correlated strong-field ionization with joint momentum sampling, with an explicit classical counterpart ladder (tSURFF-3+3D for eta=2, TDCC for Li, TD-CASSCF/TD-RASCI, reduced-dim quantum, ECBB) would be new in the sources searched.
- The strongest scientifically honest framing is category 3 (resource) for the eta=3 full-3D reference problem plus an explicit L5 analysis, not category 4 (sampling advantage): Born-rule sampling of a distribution whose experimentally consumed marginals are classically reproduced does not demonstrate sampling advantage.
- A negative/bounded result ("break-even requires X Toffoli/s; experiments would need Y-fold coincidence rates to consume the joint information") would also be publishable.

## 10. Scoped novelty statement
In OpenAlex (title/abstract boolean searches and cited-by of Su et al. 2021 W3165437982, Chan et al. 2023 W4322726929, Langkabel & Bande 2022 W4309409792, Mangin-Brinet et al. 2024 W4389116416, Babbush et al. 2023 W4383695264, Kharazi et al. 2026 W7131452312, Efimov et al. 2021 W3157758122), arXiv API and arXiv web searches, Crossref and Semantic Scholar lookups through 2026-09-28, we found first-quantized continuum photoemission algorithms (Kharazi et al. 2026), emulated two-particle grid ionization (Chan et al. 2023), CAP/absorbing-boundary quantum algorithms (Langkabel & Bande 2022; Mangin-Brinet et al. 2024; Jin et al. 2024), and a 1D-He HHG hardware demonstration (Gi et al. 2024), but no study of quantum sampling of eta>=3 joint photoelectron momentum distributions in photo- or strong-field multiple ionization compared against RMT, TD-CASSCF/TD-RASCI/MCTDHF, TDCC, or 3D semiclassical (ECBB) models.

Novelty category: **B** (quantum methods nearby, not this exact problem). Not C (no quantum method for this problem). Mechanism is not novel; observable/regime is.

## 11. Verdict
**WOUNDED.** Not killed: the exact comparison does not exist and the eta>=3 full-3D reference gap is real (restricted-dimension quantum vs 3D semiclassical models disagree, no adjudicating calculation). Wounded because (i) the algorithmic mechanism is already published (Kharazi 2026, Chan 2023); (ii) eta=2 is classically solved; (iii) for eta=3 strong-field the measured observable (momentum sums) is already matched by a cheap 3D semiclassical model (Praill 2025), so L1/L5 apply; (iv) shot cost for rare triple channels with ~1e9-1e11 Toffoli/shot is likely infeasible even with amplitude amplification (L3); (v) model/experimental floors (focal averaging, intensity calibration, frozen core) likely dominate solver error (L6). Survival requires: a measured (or measurable) eta>=3 joint observable that the ECBB and reduced-dim models predict differently beyond experimental uncertainty, and a RAS-convergence test showing truncated TD methods fail for it.

## Citations verified in this audit
arXiv: 2602.20234, 2202.05864, 2205.10543, 2112.06365, 2304.00667, 2301.01203, 2308.12352, 2105.12767, 2603.12859, 2601.08793, 2410.16797, 1511.06655, 2104.10565, 2211.10116, 1903.10743 (last three via arXiv author listing).
DOIs: 10.1364/euvxray.2024.jtu4a.11; 10.22331/q-2024-04-08-1311; 10.1021/acs.jctc.2c00878; 10.1126/sciadv.abo7484; 10.1137/23m1563451; 10.1038/s41467-023-39024-0; 10.1073/pnas.2317772121; 10.1103/prxquantum.2.040332; 10.1103/physreva.93.023406; 10.1088/1742-6596/1412/13/132053; 10.1103/x7zf-dx8m; 10.1088/0953-4075/39/8/006; 10.1103/physrevlett.81.1813; 10.1103/physreva.61.030704; 10.1103/physreva.78.033401; 10.1364/oe.431572; 10.1103/physreva.108.033103; 10.1103/1dn8-4f6h; 10.1103/physreva.105.043102; 10.1103/physreva.107.l041101; 10.1088/1361-6455/ae2e65; 10.1103/43wt-x129; 10.1103/physreva.104.023113; 10.1103/physreva.105.053119; 10.1103/physreva.86.053424; 10.1103/physreva.90.062508.
UNVERIFIED items: numerical ranges in Sec. 8 Q3/Q4 (auditor estimates); typical experimental intensity-calibration uncertainty; absence of full-coincidence eta=3 NSTI measurements (not found, not proven absent).
