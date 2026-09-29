# Audit C44 (CLASSICAL ADVERSARY): dense e-h plasma dynamics through the exciton Mott crossover in 2D TMDs

Date: 2026-09-28. Auditor role: classical adversary. Status: FINAL.

**Verdict: KILLED as a practical-advantage candidate.** There is a residual methods-benchmark niche, described in section 6. It is at most claim category 1 (quantum usefulness for validating approximate self-energies). It is not a practical advantage.

---

## 0. Query log (all via WebFetch; the WebSearch budget was exhausted at 200/200)
1. WebSearch "G1-G2 scheme electron-hole plasma ... exciton Mott transition 2D" failed because the budget was exhausted.
2. arXiv API `all:"exciton Mott" AND all:monolayer`, sorted by date. 6 hits: 2604.06897, 2601.17167, 2512.01874, 2111.07887, 2007.11509, 1910.03890.
3. arXiv abs and html for 2604.06897. arXiv abs for 2601.17167 and 2512.03198.
4. arXiv API `au:Perfetto AND au:Stefanucci`. 30 hits, 2020-2026.
5. arXiv abs: 2109.15209, 2203.08083, 2305.07458, 2103.11932, 2607.18183, 2607.28417.
6. arXiv API `au:Bonitz AND (G1-G2 | "quantum fluctuations" | electron-hole | uniform)`. 30 hits. abs: 2606.10773, 2302.06216, 2312.15030.
7. Crossref DOI 10.1038/s41467-017-01298-6 and arXiv abs 1705.05202 (Steinhoff 2017).
8. arXiv API `abs:"electron-hole plasma" AND (monolayer|TMD|WS2|MoS2|WSe2)`. 16 hits. arXiv API `au:Steinhoff AND (Mott|plasma|gain|"high density"|"excitation-induced")`. 10 hits.
9. arXiv API `"electron-hole liquid" AND (QMC|DMC)` returned 0 hits. OpenAlex returned HTTP 429 twice.
10. arXiv API for time-dependent neural variational methods on continuum fermions. 20 hits. abs and html for 2403.07447.
11. Crossref: Chernikov 2015 (Nat Photon), Siday 2022 (Nano Lett), Erben 2018 (PRB), Su 2021 (PRX Quantum).
12. arXiv API `"Monte Carlo" AND exciton* AND (Mott | "electron-hole plasma") AND 2D`. 7 hits.
13. arXiv API `exciton* AND Mott AND (T-matrix|ladder|Kadanoff-Baym|Green function)`. 21 hits. abs for 1407.1720 and 2003.12925.
14. arXiv API `(GKBA|G1-G2|"Kadanoff-Baym ansatz") AND exciton*`. 5 hits. abs for 2609.08932 and 2007.07801.
15. arXiv abs 2603.19007 (Eklund et al. first-quantized dynamics).

## 1. Verified citations
| Ref | What it establishes for this audit |
|---|---|
| Dogadov, ..., Stefanucci, Perfetto, arXiv:2604.06897 (2026), "Excitonic Mott transition without population inversion" | Pump-probe of a monolayer TMD, hBN-related (Watanabe/Taniguchi coauthors). Theory: real-time NEGF with a GW (dynamical screening) plus Fan-Migdal (first-principles phonons) self-energy. Model: 2 VB + 2 CB, 169 k-points in a 0.4 A^-1 plaquette around K, Rytova-Keldysh r0 = 45 A, CB rigidly shifted +0.5 eV, dt = 0.1 fs, ~100 fs window, **1.6e13 cm^-2 per valley**. The paper reports "excellent agreement" with the measured conductivity maps: the exciton is fully quenched within ~100 fs and there is **no gain**. It also shows that quasi-thermal BSE wrongly predicts gain. |
| Mohapatra et al., arXiv:2601.17167 (2026) | WS2, experimental. Reports a *discontinuous* EMT with an abrupt red shift above a threshold and plasma decay in 0.65 ps. No many-body dynamics theory. |
| Chernikov, Ruppert, Hill, Rigosi, Heinz, Nat. Photon. (2015), doi:10.1038/nphoton.2015.104 | Earlier WS2 experiment that claims **population inversion** (gain). It conflicts with 2604.06897. The experiments themselves disagree on gain. |
| Yu, Li, Cao, arXiv:2007.11509 (2020) | MoS2 EMT. Addresses the "controversies on the continuousness and criteria of EMT". |
| Siday et al., Nano Lett. 22, 2561 (2022), doi:10.1021/acs.nanolett.1c04741 | Ultrafast nanoscopy of high-density exciton phases in WSe2, with Malic-group theory. Only the metadata was verified; the Mott density value is [UNVERIFIED]. |
| Dendzik, ..., Perfetto, Sangalli, et al., PRL 125, 096401 (2020), arXiv:2003.12925 | EMT in WSe2 seen by core-level trARPES. A many-body Green's function theory reproduces the delayed core-hole renormalization. |
| Steinhoff et al., Nat. Commun. 8, 1166 (2017), doi:10.1038/s41467-017-01298-6 (arXiv:1705.05202) | Dynamically screened many-body theory. Predicts n_M between **3e12 and 1e13 cm^-2** depending on dielectric environment, doping and temperature. So n_M has a parameter/model-floor spread of about 3x. |
| Erben, Steinhoff, Gies, Schoenhoff, Wehling, Jahnke, PRB 98, 035434 (2018), doi:10.1103/physrevb.98.035434 | SBE on the full BZ. Under excitation, two of the four MX2 monolayers become **indirect-gap**, because the K/Lambda(Q) valleys reorder. A K-point effective-mass model is structurally incomplete at high density. |
| Steinhoff et al., arXiv:2409.17857 (2024) | Quantum laser equations with ab initio matrix elements. Plasma lasing in MoS2 above 5e13 cm^-2. |
| Perfetto, Pavlyukh, Stefanucci, PRL 128, 016801 (2022), arXiv:2109.15209 | Time-linear real-time GW for 2D materials. Finds a "self-sustained screening cascade leading to the Mott transition of coherent excitons". |
| Perfetto, Stefanucci, arXiv:2305.07458 (2023) | Real-time GW-Ehrenfest-Fan-Migdal. Gives a parameter-free, multivalley MoS2 coherent-to-incoherent crossover. |
| Pavlyukh, Perfetto, Stefanucci, PRB 106, L201408 (2022), arXiv:2203.08083 | Doubly screened GW~. Time-linear and conserving, with 2^12 diagrammatic variants. |
| Pavlyukh, Perfetto, Stefanucci, PRB 104, 035124 (2021), arXiv:2103.11932 | 2B/GW/T-matrix/Faddeev NEGF benchmarked against an exactly solvable model. The Faddeev (3-particle) scheme is still time-linear. |
| Betancur, Stefanucci, Perfetto, arXiv:2607.18183 (2026) | First-principles excitonic Bloch equations for WSe2. Agree with trARPES. Thermalized carrier distributions are shaped by exciton wavefunctions. |
| Perfetto, ..., Dani, Stefanucci, arXiv:2607.28417 (2026) | trARPES plus XBE. Free carriers coalesce into excitons **through phonons**. |
| Mittenzwey, Voigt, Knorr, arXiv:2512.03198 (2025) | Excitonic Heisenberg-equation theory up to (below) the Mott density, covering coherent and incoherent regimes and biexcitons. |
| Bonitz, Joost, Makait, Schroedter, Karsberger, Balzer, pss(b) 261, 2300578 (2024), arXiv:2312.15030 | G1-G2 review covering GW, T-matrix and dynamically screened ladder (DSL), all time-linear. |
| Joost, Schluenzen, Bonitz et al., arXiv:2202.10061 (2022) | DSL (GW + T-matrix) benchmarked against exact results on Hubbard clusters. |
| Schroedter, Bonitz, Joost, arXiv:2606.10773 (2026) | deltaNEGF: stochastic low-rank G1-G2 reaching **N_b ~ 1e4** basis states, positivity-preserving, with GW and pp/ph T-matrix, and stable at strong coupling. |
| Makait, Borges Fajardo, Bonitz, arXiv:2302.06216 (2023) | G1-G2 in momentum representation for uniform jellium (quasi-1D). |
| Schroedter, Joost, Bonitz, Vlcek, arXiv:2609.08932 (2026-09-08) | Compared with ED on a driven two-band lattice model, a GKBA-based reference propagator "artificially broadens and splits spectral peaks". Mean-field and statically screened references give the most accurate spectra. |
| Tuovinen, Golez, Eckstein, Sentef, PRB 102, 115157 (2020), arXiv:2007.07801 | GKBA agrees with full KBE for weak and intermediate photodoping. **Under strong excitation GKBA fails to melt the excitonic order.** |
| Murakami, Schueler, Takayoshi, Werner, arXiv:1907.06799 (2019) | GKBA gives the best agreement with iTEBD for excitonic modes in a 1D extended Falicov-Kimball model. |
| Asano, Yoshioka, JPSJ 83, 084702 (2014), arXiv:1407.1720 | Self-consistent screened T-matrix for the 2D e-h system (equilibrium). Finds a crossover at high T and a discontinuous Mott transition at low T. |
| Filinov, Bonitz, Fehske, Levashov, Fortov, arXiv:0810.2709 (2008) | PIMC phase diagram of the 2D e-h plasma (equilibrium). |
| Chui, Wang, Tanatar, arXiv:2108.01723 (2021) | Fixed-node DMC for bilayer TMD e-h. Transition densities of 4.1-14.5e12 cm^-2. |
| Mostaani et al., arXiv:1706.04688 (2017) | DMC for excitonic complexes with the Keldysh potential in TMDs, which it describes as "statistically exact". |
| Nys, Pescia, Sinibaldi, Carleo, Nat. Commun. 15, 9404 (2024), doi:10.1038/s41467-024-53672-w | Continuum real-time t-VMC/NQS. **Largest system is a 2D quantum dot with N = 18 electrons**, with no exact reference. No two-component periodic eta ~ 64-128 dynamics exists. |
| Su, Berry, Wiebe, Rubin, Babbush, PRX Quantum 2, 040332 (2021), doi:10.1103/prxquantum.2.040332 | First-quantized plane-wave qubitization cost model. |
| Eklund, ..., Low, Berry, Kassal, arXiv:2603.19007 (2026) | End-to-end first-quantized dynamics: state preparation, qubitization and observables. Only the abstract was checked. |

## 2. Strongest classical attack, by audit question

### Q1: Is there a multi-family wall (GW-G1G2 vs T-matrix-G1G2 vs SBE disagreeing by more than the experimental scatter)?
- **No named substrate/density point was found** where classical families are shown to disagree on gain onset or n_M by more than the experimental scatter. That covers the sources searched: the Perfetto/Stefanucci, Bonitz/Joost, Steinhoff/Jahnke and Knorr/Malic series, 2014-2026.
- The experimental scatter is itself large. Chernikov 2015 reports gain (population inversion) in WS2. Dogadov 2026 reports no gain and a quantitative theory match. Mohapatra 2026 reports a discontinuous transition. Yu/Cao 2020 cites the continuity controversy. Steinhoff 2017 places n_M at 3e12-1e13 depending on environment.
- **At the decision-relevant point the problem is classically handled.** At 1.6e13 cm^-2 per valley over 0-100 fs, NEGF GW+Fan-Migdal reproduces the pump-probe conductivity maps quantitatively (2604.06897). It also resolves the decision question (gain vs no gain) and explains why quasi-thermal BSE fails. This is exactly C44's window, and C44 cites this paper as its target experiment.
- Documented GKBA pathologies exist only in **lattice models**. These are incomplete melting of excitonic order at strong excitation (Tuovinen 2020) and broadened or split spectral peaks with a correlated GKBA reference (Schroedter 2026). They are real signs of solver error, but nothing shows they are large for the 2D continuum TMD problem at the densities of interest. Both groups already have remedies: full KBE, DSL, Faddeev, and statically screened reference propagators.

### Q2: Model floor (L6)
- **Phonons are not optional.** The validated classical model includes first-principles Fan-Migdal electron-phonon coupling (2604.06897). Carriers form excitons through phonons (2607.28417), and a phonon-assisted intervalley cascade shapes relaxation (2607.18183, 2305.07458). C44's Hamiltonian is e-e only, so an exact quantum solution of it is an exact solution of a model already known to be incomplete for the same observable. Adding phonon modes to a first-quantized plane-wave simulation increases qubits and Toffolis substantially. No resource estimate for that exists in C44.
- **Band structure.** Excitation drives a direct-to-indirect gap reordering with the K/Q(Lambda) valleys (Erben 2018). A two-component effective-mass model at K has no Q valleys. The classical ab initio models also rigidly shift gaps by 0.5 eV (2604.06897). Uncertainties in r0 and eps_env, together with substrate and doping, move n_M across a factor of about 3 (Steinhoff 2017). No quantified solver disagreement of that size was found. **The model/parameter error is at least comparable to, and probably larger than, the solver error.** This is the FeMoco-type failure (L6).

### Q3: Finite size
- My own arithmetic (order of magnitude; ħ, e^2 = 14.4 eV·A): a total density n_e = 1e13 cm^-2 with g = 4 spin-valley flavours gives n per flavour = 2.5e12 cm^-2. Then k_F = sqrt(4πn/g) ≈ 0.056 A^-1.
  - For eta = 32 (16 electrons + 16 holes), the cell is A = 160 nm^2, L ≈ 12.6 nm, and Δk = 2π/L ≈ 0.05 A^-1 ≈ k_F. There are only **4 electrons per flavour**, which fills a single momentum shell. Shell and finite-size effects dominate.
  - For eta = 128, there are 16 electrons per flavour and Δk ≈ k_F/2. The system is still shell-dominated, so twist averaging would be needed, which multiplies the circuit count.
  - L/a_B ≈ 8-15 is enough for the exciton size. The problem is the Fermi-surface and occupation resolution, not the exciton size.
- The classical NEGF run in 2604.06897 has an equivalent periodic length of about 2π/(0.4/13 A^-1) ≈ 20 nm. At 1.6e13 per valley that holds **about 64 electrons per valley**, the same scale as C44's largest eta. The classical method already runs at the quantum proposal's system size, with approximate correlation but fractional, smooth occupations.

### Q4: L5 resolvability
- Near and above n_M, excitonic lines broaden to tens of meV and the measured observables are broad conductivity/absorption maps. The decision-level question is gain yes/no and roughly when the exciton quenches. It has been answered by GW+FM, with quasi-thermal BSE shown to be qualitatively wrong. Nothing shows that the difference between exact e-e-only dynamics and GW+FM would exceed the gap between samples (Chernikov vs Dogadov) or between environments. Where the exact-vs-approximate difference might be largest (r_s ~ 1-3 at the crossover, where incoherent exciton ladder correlations compete with screening), the experimental observable is broadest. This fits the L5 pattern: the hard region carries little decision information.

### Q5: Resource check (my own order-of-magnitude arithmetic, not taken from a paper)
- For a first-quantized 2D Keldysh interaction, λ_V ≈ (eta^2/2)·(e^2/r0)·ln(1 + r0 q_max/eps_env). With r0 = 45 A, eps_env ≈ 4.5 and q_max ≈ 0.4 A^-1, λ_V ≈ 0.57 eV × eta^2/2. That gives about **4.7e3 eV at eta = 128** and about 290 eV at eta = 32. The kinetic term is ≤ 1e2 eV.
- For t = 150 fs (≈ 228 eV^-1), λt ≈ 1e6 walk steps at eta = 128 and about 7e4 at eta = 32. With about 2e3-1e4 Toffolis per step (Su et al. 2021 cost structure, scaling like eta·n_p), **G ≈ 3e8 (eta = 32) to about 5e9 (eta = 128)**. This is consistent with C44's 1e8-1e10.
- Shots:
  - Momentum-occupation sampling at about S ~ 1e3 gives S·G ≈ 5e12 at eta = 128. That is **above the ≤ 1e12 rule**. At eta = 32, S·G ≈ 3e11, but that size is finite-size dominated (Q3).
  - An absorption or gain spectrum needs two-time dipole correlators ⟨P(t+τ)P(t)⟩ over about 50-100 τ points at each pump-probe delay t, each by Hadamard test with about 1e3-1e4 shots. That is S ≈ 1e5-1e6 per (density, delay) point, so **S·G ≈ 1e14-5e15**, far beyond the rule.
  - A density scan across n_M (about 10 densities × about 10 delays) multiplies this by about 100.
- Qubits: about 1e3 logical qubits for eta = 128 × about 8 bits, plus ancillas. This is plausible.

### Q6: NQS / tensor methods at eta ~ 64 in 2D
- Continuum t-VMC/NQS: the largest demonstration is N = 18 in a 2D dot (Nys et al. 2024), so eta ~ 64-128 two-component periodic dynamics has **not** been shown. MPS/PEPS in a continuum 2D plane-wave basis at this size is not credible.
- This does **not** rescue the candidate. The competing classical families are the diagrammatic time-linear NEGF methods (GW, T-matrix, DSL, Faddeev, deltaNEGF at N_b ~ 1e4) and excitonic Bloch/Heisenberg equations. Several of these are validated against experiment. The hardness of *exact* dynamics is real, but exactness is not what the decision needs.

## 3. Where exactly classical computation fails (with evidence)
- There is **no evidence of failure in the decision-relevant regime.** GW+FM matches experiment at 1.6e13 cm^-2 per valley over 0-100 fs (2604.06897). Below n_M, excitonic theories (XBE, Heisenberg-equation) match trARPES (2607.18183, 2607.28417). Equilibrium T-matrix, PIMC and DMC treat the static crossover.
- Plausible, but not demonstrated for TMDs, are GKBA errors in strongly excited excitonic melting and in correlated spectra (Tuovinen 2020; Schroedter 2026, both lattice models). Exact (full-KBE, DSL, Faddeev) cross-checks are the classical next step.
- The only regime without an exact classical reference is the 2D continuum two-component system at eta ≳ 30-60 with r_s ~ 1-3. There, the quantum computer would compute exactly a model that lacks phonons and Q valleys.

## 4. Cheapest decisive classical kill experiment (for the record; no heavy compute run here)
Use one fixed effective-mass Rytova-Keldysh model (WS2-on-hBN parameters) with densities of 1e12 to 3e13 cm^-2 and a 0-150 fs window. Run CHEERS or G1-G2 with (a) HF-GKBA GW, (b) eh T-matrix, (c) DSL, and (d) full-KBE GW at small k-grids. Compare the transient absorption at 30/60/100 fs and the gain sign.

In parallel, vary (i) r0 by ±20%, (ii) eps_env over 1-5, (iii) phonons on/off (Fan-Migdal), and (iv) K-only vs K+Q valleys.

Kill rule: kill if the spread across self-energy families at every density is smaller than the spread from (i)-(iv) or from the Chernikov-vs-Dogadov experimental scatter. From the Steinhoff 2017 factor of about 3 in n_M and the phonon dependence in 2607.28417, the expected outcome is a kill. It costs about 10^2-10^3 CPU-hours with existing open codes, since CHEERS (arXiv:2312.00468) is public.

A small-eta exact-diagonalization cross-check of GKBA (for example 2e+2h or 3e+3h in a 2D periodic cell with a small plane-wave cutoff) would bound the self-energy error directly at r_s ~ 1-3.

## 5. Mapping to the protein-failure lessons
- **L1 (false hardness):** C44's hardness claim ("accuracy class over approximate NEGF") was not checked against the strongest current classical result. That result (2604.06897) already matches the target experiment.
- **L2 (solver equivalence / ablation):** In a FULL-vs-ABLATION comparison, replacing the exact e-e dynamics with GW+FM keeps the capability the experiment needs (gain/no-gain, quench time), and GW+FM additionally includes phonons.
- **L5 (information vs computation):** The exactly hard corner (crossover r_s ~ 1-3) is where observables are broadest and experiments disagree most.
- **L6 (model floor):** The e-e-only effective-mass model lacks phonons and Q valleys. Parameter uncertainty (r0, eps_env, doping) moves n_M by about 3x.
- **L3/L4:** S·G for spectra is about 1e14-1e15, beyond the ≤ 1e12 rule.

## 6. Residual (not an advantage claim)
One narrow sub-lane survives as a *quantum usefulness* (category 1) benchmark: exact real-time dynamics of the 2D two-component Keldysh e-h system at eta ~ 64-128 and r_s ~ 1-3, used as ground truth for GKBA/G1-G2 self-energies. No classical exact method reaches this (the NQS maximum is N = 18). Two things would reopen C44 as a practical candidate:
- (a) a demonstrated case where GW/T-matrix/DSL/XBE families disagree on a TMD observable by more than the parameter and phonon floor; and
- (b) a phonon-inclusive quantum formulation with S·G ≤ 1e12.

Neither was found in the sources searched through 2026-09-28.
