# Audit C44 (novelty / prior art): dense e-h plasma dynamics through the exciton Mott crossover in 2D TMDs

Auditor role: NOVELTY / PRIOR-ART. Date: 2026-09-28. Status: COMPLETE.
Verdict: **WOUNDED**. Category **B** (bordering C), not A as the candidate claimed. The gap is material, but the observable the candidate leads with (gain onset / n_M) has already been reproduced by an approximate classical method that agrees with experiment. The quantum formulation as written also has a representational defect (see section 8).

---

## 1. Headline findings

1. **The claimed "scoped category A" is falsified.** arXiv:2606.04295 (Klymenko, Goldozian, Hoang, Cole, Usman; submitted 2 Jun 2026), "Quantum simulations of ultrafast optical spectroscopy of semiconductors on digital quantum computers in the semi-classical approximation", computes **linear absorption and optical-gain spectra of photoexcited semiconductors** from the semiconductor Bloch equations on a digital quantum computer:
   - Jordan-Wigner encoding with first-order Trotter; K=60 k-points on 2 bands, so 120 qubits; 700 Trotter steps.
   - Run on Qiskit-Aer with ibm-kyoto noise snapshots, benchmarked on GaAs, with reduced-dimensionality effects included.
   - Coulomb interaction enters only at Hartree-Fock level.
   - The authors say "no exponential quantum advantage is expected in the single-particle approximation" and name the many-body ("hierarchy problem") extension as the route to advantage.
   - Semantic Scholar lists 0 citers as of 2026-09-28.

   The observable class (transient absorption and gain of a photoexcited semiconductor) already has a quantum-algorithm paper. What remains untested is correlated e-h dynamics through the Mott crossover. That is category B (nearby quantum methods, not this exact problem). It borders C, because "absorption/gain of photoexcited semiconductors" has a quantum paper with no q-vs-c advantage study. There is also a scoop risk: the Usman/Cole group has publicly flagged the many-body extension as its next step.
2. **The classical frontier is recent, strong and already arbitrated by experiment.** arXiv:2604.06897 (Dogadov, Genco, Cadore, ..., Cerullo, Dal Conte, Stefanucci, Perfetto; 8 Apr 2026), "Excitonic Mott transition without population inversion":
   - Sample: hBN-encapsulated monolayer WSe2 on 90 nm SiO2/Si, pumped up to ~1.6e13 cm^-2 per K/K' valley (fluence 50-330 uJ/cm^2). The exciton is fully quenched above ~150 uJ/cm^2, within ~100 fs.
   - Model: NEGF with GKBA propagation, GW self-energy plus Fan-Migdal electron-phonon coupling; DFT tight-binding with 2 valence + 2 conduction bands; 169 k-points in a plaquette around K; a ~70 fs window.
   - The model reproduces **no gain across the whole EMT**. The paper also states that "standard quasi-thermal treatments invariably predict pronounced optical gain", in contrast to the observations.
   - A real multi-family disagreement therefore exists (quasi-thermal SBE/Saha vs non-thermal NEGF-GW). But experiment has already sided with an *approximate classical* method. The headline observable (gain yes/no across n_M) therefore does not need an exact solver to be decided at the qualitative level (lessons L5, L7).
3. **The Stefanucci/Perfetto program covers most of the physics the candidate proposes to add:**
   - real-time GW for 2D materials, including a "self-sustained screening cascade leading to the Mott transition of coherent excitons" (PRL 128, 016801 (2022), arXiv:2109.15209);
   - GW-Ehrenfest-Fan-Migdal for MoS2 (Nano Lett 2023, arXiv:2305.07458);
   - non-Hermitian "exceptional excitons" at the onset of population inversion in WS2 (arXiv:2512.14392);
   - excitonic Bloch equations with exciton formation and intervalley scattering (arXiv:2407.17077, SciPost Phys 18, 009 (2025); arXiv:2607.18183);
   - phonon-driven carrier-to-exciton "phono-conversion" in WSe2 (arXiv:2607.28417);
   - the time-linear CHEERS code with GW and T-matrix (arXiv:2312.00468, arXiv:2111.06698).
4. **The quantum machinery is established; only the application is new.**
   - First-quantized plane-wave qubitization: Su et al., PRX Quantum 2, 040332 (2021), arXiv:2105.12767.
   - Exact electron dynamics vs mean-field: Babbush et al., Nat Commun 14, 4058 (2023), arXiv:2301.01203.
   - Multi-species (nuclei + electrons) first-quantized dynamics with fast state preparation: Eklund et al., arXiv:2603.19007 (19 Mar 2026).
   - The candidate's algorithmic content is (i) a 2D Rytova-Keldysh kernel instead of 1/q^2 and (ii) two masses. Both are minor adaptations, not a new mechanism.

---

## 2. Classification

**B.** Quantum methods exist nearby:
- the semi-classical SBE absorption/gain on a QC (2606.04295);
- first-quantized exact dynamics of electrons, multi-species systems and warm dense matter (2105.12767, 2301.01203, 2603.19007);
- a static excitonic ground state of 2D WTe2 by downfolding plus VQE (2409.12237).

No quantum study treats correlated 2D e-h plasma dynamics through the exciton Mott crossover, and no quantum-vs-classical comparison against GW/T-matrix NEGF exists.

It is not A, because 2606.04295 targets the same observable class (transient absorption and gain of photoexcited semiconductors). It is not C for the exact problem: no quantum method has been applied to correlated e-h dynamics near n_M.

---

## 3. EXACT PRIOR WORK (same problem, any method; all verified)

**Experiment**
- Chernikov, Ruppert, Hill, Rigosi, Heinz, Nat Photon 9, 466-470 (2015), doi:10.1038/nphoton.2015.104. Population inversion and giant BGR in WS2. Verified via Crossref. The threshold density is not recorded here: [UNVERIFIED].
- Mohapatra, Palato, Olsen, Stähler, Gierster et al., arXiv:2601.17167 (23 Jan 2026). Discontinuous ultrafast EMT in monolayer WS2; lineshape analysis of A/B excitons; plasma decay ~0.65 ps.
- Dogadov et al., arXiv:2604.06897 (8 Apr 2026). EMT without population inversion in hBN/WSe2/hBN; NEGF-GW-FM-GKBA. See section 1.
- Yu et al., arXiv:2007.11509. EMT in MoS2 with exciton-plasma coexistence.
- Dendzik et al., arXiv:2003.12925. EMT by core-cum-conduction trXPS in WSe2.
- Yuan et al., arXiv:2111.07887. First-order EMT at lateral heterojunctions.

**Theory**
- Steinhoff, Florian, Rösner, Schönhoff, Wehling, Jahnke, Nat Commun 8, 1166 (2017), doi:10.1038/s41467-017-01298-6 (verified via Crossref). Exciton-plasma fission/fusion balance, tuned by dielectric environment and doping.
- Kudlis & Iorsh, PRB 103, 115307 (2021), arXiv:2011.12741. Cluster-expansion SBE (Heisenberg equations of motion) for EMT absorption.
- Guerci, Capone, Fabrizio, Phys Rev Materials 3, 054605 (2019), arXiv:1810.01843. The order of the EMT (first vs second) is controlled by the exciton binding energy.
- Asano et al., arXiv:1407.1720. Screened T-matrix phase diagram of the 2D e-h system.
- Perfetto, Pavlyukh, Stefanucci, PRL 128, 016801 (2022), arXiv:2109.15209. Real-time GW; screening cascade and Mott transition of coherent excitons.
- Perfetto & Stefanucci, arXiv:2512.14392. Exceptional excitons at population inversion in WS2.
- Mittenzwey, Voigt, Knorr, arXiv:2512.03198. Excitonic theory of the ultrafast response at elevated densities, explicitly *below* the Mott transition (MoSe2).
- Reeves, Cushing, Vlček, PRB 112, 075105 (2025), doi:10.1103/bpqy-f2pk. Role of effective mass and long-range interactions in BGR of photoexcited semiconductors. Found via the OpenAlex cited-by set of the G1-G2 PRL; abstract not retrieved.

## 4. NEAREST QUANTUM WORK
- **arXiv:2606.04295** (Klymenko et al., 2026). SBE absorption and gain on a digital QC, semi-classical/HF, GaAs, 120 qubits; many-body extension flagged as future work. This is the closest paper.
- arXiv:2409.12237. Ab initio downfolding plus VQE for the excitonic ground state of monolayer WTe2 (static lattice model).
- arXiv:2105.12767 (Su et al., PRX Quantum 2021). First-quantized plane-wave qubitization; 3D Coulomb, one species.
- arXiv:2301.01203 (Babbush et al., Nat Commun 2023). Exact first-quantized electron dynamics beats mean-field (HF/DFT) scaling; the speedup is largest at finite temperature.
- arXiv:2603.19007 (Eklund, Tikku, Sinnott, Huggins, Low, Berry, Kassal, 2026). End-to-end first-quantized, non-BO, multi-species dynamics with qubitization and fast initial-state preparation.
- arXiv:2602.20234 (EUV photoemission, first-quantized absorption/photoemission spectra) and arXiv:2308.12352 (stopping power in WDM). Both come from the prior context of this program.
- Molecular/Frenkel exciton QC papers are not this problem: 2603.23936, 2411.13669, 2409.05548, 2412.00407, 2309.17391, 2404.06264.
- Pump-probe on QC for spin models: arXiv:2507.22988 (mixed-field Ising bound-state relaxation). Not e-h continuum.

## 5. NEAREST CLASSICAL WORK (the competitors a paper must beat)
- NEGF-GKBA with GW (+Fan-Migdal) on DFT tight-binding: Perfetto/Stefanucci (2604.06897, 2109.15209, 2305.07458); CHEERS code (2312.00468); time-linear G1-G2 with GW and T-matrix (2111.06698).
- G1-G2 scheme: Schlünzen, Joost, Bonitz, PRL 124, 076601 (2020), arXiv:1909.11489. OpenAlex W2977125138, 104 citations.
  - Applied to MoS2 monolayers under ion impact (arXiv:2508.16751, pssb.202500458).
  - Applied to uniform dense plasmas (Makait & Bonitz, CPP 65 (2025), doi:10.1002/ctpp.70022, which fixes the aliasing problem for continuous systems).
  - Extended to 1e4 basis states (arXiv:2606.10773).
  - Real-time Dyson expansion with exciton shake-up (arXiv:2609.08932).
- Excitonic Bloch equations with exciton formation and phonons: 2407.17077, 2607.18183. Cluster-expansion SBE: 2011.12741, 2512.03198.
- Equilibrium QMC for 2D e-h systems:
  - PIMC of 2D e-h plasmas with the Mott transition: Filinov et al., arXiv:0810.2709;
  - bilayer DMC/PIMC: De Palo 2204.10255, Maezono 1309.2091, Schleede 1205.4686;
  - fixed-node DMC for TMDC bilayer e-h systems: Chui, 2108.01723;
  - neural VMC for the e-h bilayer: 2311.02143.
- Wavefunction vs GF benchmarking out of equilibrium: Reeves ... Zgid, Vlček, PRR 7, 023002 (2025). Coupled cluster is near-exact at weak driving; GW is better than mean-field at strong driving. The exact references come from small systems only.
- Tensor-train NEGF (quantics): PRB 109, 165135 (2024) and 10.1103/dxfb-b3l5 (2025). These compress two-time GFs and would be the classical answer to "memory is the wall".
- Continuum real-time NQS: Nys, Pescia, Sinibaldi, Carleo, Nat Commun 15, 9404 (2024), arXiv:2403.07447 (system sizes not extracted: [UNVERIFIED]). Other continuum t-NQS papers reach <=4 electrons (2606.05850) or 2 electrons (2511.12983). No two-component e-h continuum dynamics was found. The candidate's audit question (6) is answered "not yet at eta~64" in the sources searched. This is a moving target and not a proof.

## 6. WHAT HAS BEEN TESTED
- Gain vs no-gain across the EMT: tested experimentally in WS2 (2015, gain) and hBN/WSe2 (2026, no gain). NEGF-GW-GKBA reproduces the no-gain result, and quasi-thermal theory is said to fail.
- EMT order (continuous vs discontinuous): tested experimentally in WS2 (2601.17167, discontinuous) and theoretically in Hubbard-mapped DMFT-like work (1810.01843, binding-energy dependent).
- Equilibrium ionization degree vs density and dielectric environment: GW-BSE/T-matrix Saha-type theory (Steinhoff 2017).
- Semi-classical SBE absorption and gain on a quantum computer (2606.04295; GaAs; noisy simulator).
- First-quantized exact dynamics resource estimates for 3D electrons, WDM and molecules (2105.12767, 2301.01203, 2603.19007, 2308.12352).

## 7. WHAT HAS NOT BEEN TESTED (the gap)
- Any **exact or controlled-error** real-time solution of the correlated 2D two-component e-h continuum (Rytova-Keldysh, two masses, valley flavours) at 1e12-1e13 cm^-2 over 100 fs. No classical method or quantum algorithm in the sources searched provides this.
- Any quantitative benchmark of **GW-GKBA vs T-matrix-GKBA vs G1-G2 vs XBE/SBE** against an exact reference for the e-h plasma at the Mott crossover. Existing NEGF benchmarks against exact results use Hubbard clusters or small molecules (2202.10061, PRR 7 023002).
- Any quantum-algorithm treatment of beyond-HF (correlated) semiconductor optics, including the extension named in 2606.04295.
- Any resource estimate for first-quantized 2D two-species e-h dynamics with a Rytova-Keldysh kernel.

## 8. WHY THE GAP IS MATERIAL (and where it is weak)

**Material**
- Every classical method in play truncates correlation: GW misses ladder/bound-state formation in the incoherent regime; the T-matrix misses dynamical screening; G1-G2 has purification/instability issues; cluster-expansion SBE truncates the hierarchy.
- The 2026 papers show the qualitative answer depends on non-thermal and dynamical-screening physics. That is where truncation choices matter.
- An exact reference at the crossover would be a new scientific object: a benchmark for the NEGF hierarchy in a continuum two-component 2D system. Nothing in the searched sources plays that role.

**Weak points (these drive the WOUNDED verdict)**
1. **Observable already decided classically (L5/L7).** The headline observable (gain onset / no-gain, quench of the 1s exciton) is reproduced by approximate NEGF-GW at the level experiments resolve: broad lines, tens of meV, limited fluence accuracy. The remaining question is quantitative: n_M to within a factor or the lineshape. A factor-of-~1.5-2 disagreement in n_M between NEGF families could exist, but no source found documents it. No named substrate/density point was found where GW-GKBA, T-matrix-GKBA and SBE disagree by more than the experimental scatter (audit Q1). The documented disagreement (quasi-thermal vs non-thermal) is a disagreement in *initial-state/thermalisation assumptions*, not in correlated-solver truncation. An exact solver on the same bare model would not arbitrate it better than NEGF-GW already does.
2. **Model floor (L6).** Model content that NEGF already includes but the candidate's bare model omits:
   - Fan-Migdal electron-phonon coupling (2604.06897);
   - carrier-to-exciton phono-conversion and intervalley (K-Q/K') scattering on tens-of-fs scales (2607.28417, 2607.18183);
   - substrate/hBN dynamical screening;
   - dark and intervalley excitons.

   The candidate's model is effective-mass, Rytova-Keldysh and electron-only, so these omissions can shift the EMT dynamics by more than solver truncation error. The FeMoco lesson applies: an exact solution of the wrong model.
3. **Representational defect of fixed-eta first quantization.**
   - The pump creates a **coherent superposition of different e-h pair numbers**: the interband polarization that carries excitonic absorption and Rabi physics. A fixed-eta first-quantized e-h register cannot represent it.
   - The candidate therefore cannot simulate the pump itself. It can only start from incoherent populations, which form a *mixed state*: an ensemble of Slater determinants that must be sampled, multiplying the shot count.
   - The probe absorption then needs a pair-creation correlator <[P(t), P^dagger(0)]> between eta and eta+2 particle sectors, at every pump-probe delay. The candidate's "product-of-Slater-determinants initial state, no Gibbs prep" understates this.
   - The coherent regime is exactly where Stefanucci/Perfetto and Knorr work, and a second-quantized band picture handles it natively.
4. **Resource rule (audit Q5; auditor's rough order-of-magnitude, not from literature).** Assumptions: eta=128, 2D grid 128x128, L~25 nm at 1e13 cm^-2, m*~0.3, eps~4.5, r0~4 nm, t=100 fs (~4.1e3 a.u.).
   - lambda_T ~ 1e2 Ha and lambda_V ~ 3e2 Ha, so lambda*t ~ 1.6e6 walk steps.
   - At ~2e4 Toffoli per step this gives ~3e10 Toffoli per circuit, at the top of or above the candidate's 1e8-1e10.
   - Pump-probe spectra need about 10-20 delays x ~1e2 probe times x 1e3-1e4 shots, times 10-100 initial-state samples. That gives S ~ 1e6-1e8, so S*G ~ 1e16-1e18.
   - Even a single momentum-occupation snapshot (S~1e3-1e4) gives S*G ~ 1e13-1e14.
   - The S*G <~ 1e12 rule is violated by 1-6 orders of magnitude.
5. **Finite size (audit Q3; auditor's estimate).** At 1e13 cm^-2 with 64 pairs, L~25 nm, which is about 15-25 exciton Bohr radii (a_B~1-1.5 nm) and fine for the high-density end. At 1e11-1e12 cm^-2 the box is L~80-250 nm, so the plane-wave grid must grow as (L/0.2 nm)^2 (about 1e5-1e6 points). That costs ~17-20 qubits per particle, which is affordable, but lambda_T grows. Worse, with 4 flavours only ~16 carriers per species-flavour remain, so Fermi-sea shell effects are strong. The low-density side of the crossover is the hard side for eta<=128.
6. **Scoop risk.** 2606.04295's authors have publicly named the many-body extension of their QC SBE framework as the path to "provable quantum advantage".

## 9. WHY IT COULD STILL BE A NEW PAPER

The most defensible paper in the searched literature is not "quantum advantage for the Mott density". It is:

(a) a first fault-tolerant resource estimate for correlated 2D two-species e-h continuum dynamics with a Rytova-Keldysh kernel, including the variable-pair-number probe correlator and the mixed-state sampling overhead; plus

(b) a classical exact-small-eta benchmark (ED/NQS at eta<=8-16 in small boxes) that quantifies GW-GKBA vs T-matrix-GKBA vs G1-G2 error on absorption lineshape and exciton fraction near the crossover. It would show at which eta, density and time the NEGF errors exceed the linewidth and the model floor.

If (b) finds NEGF errors below the ~10-30 meV linewidths, the application is killed. If it finds a resolvable error, the quantum pitch has a defined target. This matches the program's rules: a strong classical twin first, and a necessity test via FULL vs ABLATION, where ABLATION = NEGF-GW-FM-GKBA.

## 10. Scoped novelty statement

In the sources searched through 2026-09-28, I found:
- a quantum-computer semi-classical SBE absorption/gain study (Klymenko et al., arXiv:2606.04295; GaAs, HF-level, 120-qubit noisy simulation);
- first-quantized exact-dynamics algorithms for electrons, multi-species molecules and warm dense matter (Su et al. 2021; Babbush et al. 2023; Eklund et al. 2026);
- a strong classical NEGF-GW-Fan-Migdal-GKBA description of the TMD exciton Mott transition that matches experiment (Dogadov et al. arXiv:2604.06897; Perfetto et al. PRL 128, 016801).

I found **no study of** (D) correlated, exact or controlled-error quantum simulation of 2D two-component e-h plasma dynamics (absorption/gain, exciton fraction, THz response) across the exciton Mott crossover, **compared against** (E) GW/T-matrix NEGF-GKBA or G1-G2, and (F) SBE/cluster-expansion/excitonic Bloch kinetics.

The sources searched were:
- arXiv API (10 structured queries, abstract field, sorted by date);
- arXiv abstract/HTML pages of 12 papers;
- OpenAlex search, plus cited-by of Schlünzen-Joost-Bonitz PRL 124 076601 (W2977125138, 2023+) and Steinhoff Nat Commun 2017 (W2765173966, 2022+);
- a Crossref query and 5 Crossref DOI records;
- Semantic Scholar citations of 2606.04295 (none).

WebSearch was unavailable (budget exhausted). Patents, theses and conference proceedings were not searched beyond Crossref, so this statement does not cover them.

## 11. Answers to the candidate's audit questions (novelty-auditor view)
1. **Multi-family wall:** not found as a documented solver-vs-solver disagreement at a named substrate/density. The documented disagreement is quasi-thermal vs non-thermal (2604.06897), and experiment on hBN/WSe2 sides with NEGF-GW.
   - Separately, WS2 on SiO2 (Chernikov 2015, gain) disagrees with hBN/WSe2 (2026, no gain). That is a material/substrate difference, not a solver disagreement.
   - EMT order: discontinuous (2601.17167) vs binding-energy-dependent (1810.01843).
2. **Model floor:** likely dominant (phonons, intervalley scattering, dark excitons, dynamical substrate screening; see 8.2). This is unresolved and against the candidate.
3. **Finite size:** acceptable at >=5e12 cm^-2, marginal to poor at <=1e12 cm^-2 (see 8.5).
4. **L5:** at tens-of-meV linewidths the qualitative observables are already reproduced by approximate NEGF. No evidence was found of resolvable solver differences.
5. **Resources:** S*G is about 1e13-1e18, violating the <=1e12 rule (8.4; auditor estimate).
6. **NQS/TN at eta~64:** not reached for continuum two-component dynamics in the sources found (the maximum found is ~4 electrons in continuum t-NQS). Quantics tensor-train NEGF compresses the classical GF side instead.

## 12. Query log
1. WebSearch: budget exhausted (200/200). Used WebFetch against the arXiv API, arXiv abs/html pages, OpenAlex, Crossref and Semantic Scholar.
2. arXiv API `all:"electron-hole" AND all:"quantum computer"` (30 newest): no QC algorithm for e-h plasma. Hits: 2004.13868 (exciton condensate state on a 53-qubit device, not semiconductor physics) and 2405.15069 (Anderson impurity e-h propagators).
3. arXiv API `abs:exciton AND (quantum algorithm | quantum computer | quantum computing)` (50 newest): Frenkel/molecular/vibronic only, plus 2409.12237 (WTe2 VQE).
4. arXiv API `(Bethe-Salpeter | excitons | electron-hole plasma | electron-hole liquid) AND (qubitization | phase estimation | fault-tolerant | quantum circuits | first quantized/quantization)` (40): only 2609.24282 (relativistic scalar BSE VQE).
5. arXiv API `abs:"exciton Mott"` (40 newest): all classical/experimental; key items listed in section 3.
6. arXiv API `(au:Perfetto AND au:Stefanucci) OR (G1-G2 AND exciton/e-h)` (40): the NEGF TMD program in section 5.
7. arXiv abs 2603.19007 and 2301.01203; arXiv API first-quantized (50 newest); `(jellium | electron gas | warm dense | plasma) AND quantum algorithm` (40). Results: first-quantized machinery exists for molecules, pre-BO dynamics, EUV and WDM; the plasma hits are Vlasov-PDE algorithms.
8. OpenAlex search "quantum computer simulation electron-hole plasma exciton" (2020+): 0 relevant in the top 25.
9. Crossref query "quantum algorithm exciton Mott transition electron-hole plasma simulation": 0 QC hits.
10. arXiv API `e-h + (QMC | neural network | path integral | DMC) + 2D` (40): equilibrium only.
11. arXiv abs 2403.07447; arXiv API neural time-dependent continuum electrons (30): <=4 particles.
12. arXiv API au:Bonitz with G1-G2/NEGF/exciton/e-h (40): G1-G2 on MoS2 (ion impact), uniform dense plasmas and jellium stopping. No TMD gain/n_M study.
13. Crossref DOIs: 10.1038/s41467-017-01298-6, 10.1038/nphoton.2015.104, 10.1103/bpqy-f2pk, 10.1002/ctpp.70022, 10.1103/physrevresearch.7.023002.
14. OpenAlex DOI lookup, giving W1529807616 (Chernikov, 499 cit.), W2765173966 (Steinhoff, 207), W2977125138 (G1-G2 PRL, 104) and W4206920086 (real-time GW PRL, 69). Cited-by W2977125138 (2023+, about 70 works): no QC e-h study. Cited-by W2765173966 (2022+, 118 works): no QC paper. Cited-by W1529807616 filtered on "Mott" returned HTTP 429 and was not retried.
15. arXiv API `(SBE | band-gap renormalization | optical gain | TMD | photoexcited semiconductor) AND (quantum algorithm | computer | computing | circuit)` (40): **found 2606.04295**. Read its abs and HTML for algorithm details.
16. arXiv API au:Klymenko / Usman semiconductor quantum: no follow-up yet. Semantic Scholar citations of 2606.04295: none.
17. arXiv API `(photodoping | photodoped | photoexcited | pump-probe) AND (quantum computer | processor | algorithm | trapped-ion | superconducting qubits)` (30): 2507.22988 (Ising pump-probe on QC), 2506.08609 (pyrazine photodynamics resource assay). Not e-h continuum.
18. arXiv API `(Kadanoff-Baym | nonequilibrium Green | GW approximation) AND quantum computer/algorithm` (30): only single-particle transport (2509.07005, 2607.27168).
19. arXiv abs checks: 2604.06897 (abs + html), 2601.17167, 2512.03198, 2011.12741, 2109.15209, 1810.01843, 2607.18183, 2512.14392, 2105.12767, 2606.04295 (abs + html).

## 13. Citations (verified unless marked)
- arXiv:2606.04295: Klymenko, Goldozian, Hoang, Cole, Usman (2026). Verified on the arXiv abs and html pages.
- arXiv:2604.06897: Dogadov, Genco, Cadore, Kerfoot, Alexeev, Balci, Trovatello, Watanabe, Taniguchi, Tongay, Ferrari, Cerullo, Dal Conte, Stefanucci, Perfetto (2026). Verified.
- arXiv:2601.17167: Mohapatra, Palato, Olsen, Stähler, Gierster et al. (2026). Verified.
- arXiv:2512.03198: Mittenzwey, Voigt, Knorr (2025/2026). Verified.
- arXiv:2011.12741: Kudlis & Iorsh, PRB 103, 115307 (2021). Verified.
- arXiv:1810.01843: Guerci, Capone, Fabrizio, PRMaterials 3, 054605 (2019). Verified.
- arXiv:2109.15209: Perfetto, Pavlyukh, Stefanucci, PRL 128, 016801 (2022). Verified.
- arXiv:2512.14392: Perfetto & Stefanucci. Verified.
- arXiv:2607.18183: Betancur, Stefanucci, Perfetto. Verified.
- arXiv:2607.28417, 2407.17077, 2305.07458, 2312.00468, 2111.06698: Stefanucci/Perfetto group. Verified from the arXiv API listing (titles and dates).
- doi:10.1038/s41467-017-01298-6: Steinhoff et al., Nat Commun 8, 1166 (2017). Verified via Crossref.
- doi:10.1038/nphoton.2015.104: Chernikov et al., Nat Photon 9, 466 (2015). Verified via Crossref.
- PRL 124, 076601 (2020), arXiv:1909.11489: Schlünzen, Joost, Bonitz. Verified via OpenAlex and the arXiv API.
- doi:10.1002/ctpp.70022: Makait & Bonitz (2025). Verified via Crossref.
- arXiv:2508.16751, 2606.10773, 2609.08932: Bonitz group. Verified from the arXiv API listing.
- doi:10.1103/bpqy-f2pk: Reeves, Cushing, Vlček, PRB 112, 075105 (2025). Verified via Crossref.
- doi:10.1103/physrevresearch.7.023002: Reeves et al. (2025). Verified via Crossref.
- arXiv:2105.12767: Su, Berry, Wiebe, Rubin, Babbush, PRX Quantum 2, 040332 (2021). Verified.
- arXiv:2301.01203: Babbush et al., Nat Commun 14, 4058 (2023). Verified.
- arXiv:2603.19007: Eklund, Tikku, Sinnott, Huggins, Low, Berry, Kassal (2026). Verified.
- arXiv:2403.07447: Nys, Pescia, Sinibaldi, Carleo, Nat Commun 15, 9404 (2024). Verified; system sizes [UNVERIFIED].
- arXiv:2409.12237 (downfolding + VQE, WTe2 excitonic ground state). Verified from the arXiv API listing only.
- arXiv:0810.2709 (Filinov, 2D e-h plasma PIMC) and 2108.01723 (Chui, DMC e-h TMDC bilayer). Verified from the arXiv API listing only.
- Chernikov 2015 gain threshold density: [UNVERIFIED].
