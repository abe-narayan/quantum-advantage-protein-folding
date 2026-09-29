# Round 2 discovery: short-time (lifetime-limited / ultrafast) correlated dynamics with the decision inside the classical wall

Date: 2026-09-28. Status: FINAL for this lens. Nothing here is an experimental result. Cost figures are order-of-magnitude estimates unless cited. Novelty statements are scoped to the sources searched on 2026-09-28 (arXiv listing search, arXiv abs/html pages, Crossref). OpenAlex, the arXiv API and Semantic Scholar returned HTTP 429 for this whole session, so coverage is narrower than in round 1.
Targeted question: find problems where the needed evolution time is short (lifetime-limited, broadened or ultrafast), yet beyond classical reach because of strong correlation or dimension, so circuits are cheap, and the observable is a few expectation values (low shot count).
Filter (round-1 lesson): decision value inside the classical wall; S*G <~ 1e13; model floor below solver spread.

## Working frame (before search)

Dimensionless screen used for every candidate: K = t_max * E_corr / hbar, where t_max ~ hbar/Gamma_eff (Gamma_eff = lifetime + instrument + inhomogeneous broadening, or decoherence time for ultrafast processes) and E_corr is the energy scale of the correlation feature that carries the decision. If K <~ 1, the correlation signature is washed out (L5). If K is large, the "short time" is not short in units of the interaction. Also: for geometrically local Hamiltonians, constant-time dynamics has classical cluster-expansion algorithms (arXiv:2210.11490, verified below), so short time on a lattice is suspect by default.


## Interim findings (saved mid-search, 2026-09-28)

Verified so far (abs pages or search listings read in this session):
- Wild & Alhambra, arXiv:2210.11490, PRX Quantum (2023): classical cluster-expansion simulation of short-time dynamics of local Hamiltonians, polynomial in n and 1/eps.
- Zhao, Marvian, Tong, arXiv:2608.19448 (Aug 2026): Majorana propagation, poly time for local observables when lambda*|t|^(2D+1) = O(1) on D-dim lattices; quasi-poly for lambda*|t| = O(1) (Frobenius-norm); weak interaction lambda required.
- D'Anna, Nys, Carrasquilla, arXiv:2511.02809: Majorana-string Heisenberg propagation for 2D Fermi-Hubbard quenches, accuracy comparable to variational SOTA and experiments.
- Miller et al., arXiv:2503.18939: Majorana propagation for fermionic circuits, chemistry up to 52 modes.
- Wahyutama & Larsson, arXiv:2409.05959, JCTC 2024: TDDMRG charge migration in furfural, CAS(40o,35e), D = 700 complex MPS "sufficiently converged", 80 a.u. ~ 2 fs; stop at 2 fs because nuclear motion enters "after a few femtoseconds".
- Langkabel & Bande, arXiv:2205.10543 (2022): quantum-computing algorithm for laser-driven electron dynamics in small molecules (quantum method exists; no advantage study).
- Fomichev et al., arXiv:2405.11015 (2024): quantum XAS algorithms, CAS(22e,18o) Mn-O cathode cluster; "much fewer qubits and gates than ground-state energy estimation".
- Loaiza et al., arXiv:2602.20270 (2026): quantum RIXS, 20-orbital active space: 414 logical qubits, 2.0e10 Toffoli.
- Nishi et al., arXiv:2505.08612 (2025/26, PR Applied accepted): logical QPE XAS of FePO4 L-edge, 3 orbitals on trapped ions.
- Abraham, Senapati, Pathak, Peng, arXiv:2511.17985, JCP 164, 104113 (2026): approximate TD-dCC (BCH-truncated) core-hole Green's functions reproduce exact satellites and QP weights for SIAM, H2O, CH4; plus a QSP core-hole Green's-function algorithm.
- Kharazi et al., arXiv:2602.20234 (2026): EUV lithography: 92 eV absorption of IMePh monomer 200 logical qubits, 1e9 non-Clifford/circuit, 1e3 shots; photoemission >= 1e4 qubits, >= 1e14 gates, 1e4 shots.
- Lee, Zhai, Chan, arXiv:2305.08184: correction-vector RAS-DMRG L-edge XAS / 2p3d RIXS of [FeCl4] and [Fe(SCH3)4] (mononuclear); stated goal: larger metal clusters.
- arXiv:1908.05802: DMRG X-ray Raman of [2Fe-2S] (title/abstract read; authors not extracted in this session).
- Ghiasi et al., arXiv:1812.06432, PRB 100, 075146 (2019): LDA+DMFT and cluster model reproduce charge-transfer / nonlocal screening in 1s and 2p HAXPES of Fe2O3, FeTiO3, CoO, NiO.
- Higashi et al., arXiv:2105.01248, PRX 11, 041009 (2021) and Winder et al., arXiv:2004.01428, PRB 102, 085155 (2020): LDA+DMFT reproduces XAS/RIXS of infinite-layer and rare-earth nickelates.
- Krause & Oliver, J. Phys. Chem. Ref. Data 8, 329 (1979), doi:10.1063/1.555595: natural K and L level widths (Crossref record read).

## 0. Bottom line

**No candidate from this lens passes the round-1 filter. I return zero candidates and do not lower the bar.** Each example in the brief was checked: core-level spectra of multinuclear clusters, attosecond charge migration, early-time pump-probe in correlated oxides, shake-up satellites and resonant Auger. Seven further short-time problems were checked too. Every one fails at least one of the three filter conditions: decision inside the wall, S*G <~ 1e13, or model floor below solver spread. The reason (section 1) is structural, not case-specific: the short evolution time that makes circuits cheap is also what makes the problem classically tractable or uninformative.

This is a scoped negative statement. It covers lifetime-limited and ultrafast probes of electrons in molecules and in lattice-correlated solids, audited against the sources in section 5 as of 2026-09-28. It does not cover continuum Coulomb systems with a large light-cone (warm dense matter, nuclear matter). There the short-time lens folds back into the round-1 C01 / C07 regime and adds no new slot.

## 1. Structural reason: three routes by which "short" makes the problem classical

Let Gamma_eff be the total broadening (natural lifetime + instrument + inhomogeneous, or the decoherence rate for ultrafast processes). Let t_max ~ hbar/Gamma_eff, let E_corr be the energy scale of the correlation feature that carries the decision, and let K = E_corr * t_max / hbar.

1. **Light-cone locality -> embedding.** Within t_max, the perturbation (core hole or ionization hole) spreads over a Lieb-Robinson radius of about v_LR * t_max.
   - In 3d transition-metal compounds, intersite hopping and superexchange are about 0.01-0.5 eV. Gamma_eff for L2,3 edges is about 0.3-0.8 eV once instrument resolution is added (natural K/L widths: Krause & Oliver 1979). The cone is therefore about one bond, and a single-impurity or small-cluster solver with a bath is the natural classical twin.
   - Published multi-family evidence that this suffices:
     - LDA+DMFT and cluster models reproduce nonlocal charge-transfer screening in 1s/2p HAXPES of NiO, CoO, Fe2O3 and FeTiO3 (arXiv:1812.06432).
     - LDA+DMFT reproduces XAS/RIXS of nickelates (arXiv:2105.01248, 2004.01428).
     - For lattice models, short-time dynamics of local Hamiltonians has polynomial cluster-expansion algorithms (arXiv:2210.11490).
     - Majorana propagation is polynomial for lambda*|t|^(2D+1) = O(1) and quasi-polynomial for lambda*|t| = O(1) (arXiv:2608.19448).
     - Majorana-string propagation matches the variational state of the art on 2D Fermi-Hubbard quenches (arXiv:2511.02809).
2. **Moment truncation -> ground-state expectation values.** When Gamma_eff is comparable to the spread of the relevant manifold, a few moments mu_k = <A^dag H^k A> fix the broadened spectrum. These are ground-state expectation values, which an MPO applied to a DMRG/MPS ground state gives classically. The hardness then moves back to correlated ground-state preparation, which is round-1 lesson (ii).
3. **High energy transfer -> perturbative or factorized limits.** Short time at large energy transfer is the impulse/Born/short-time-factorization regime: IA for high-q XRTS, STA or spectral-function factorization for quasi-elastic nuclear response. The classical approximations are controlled there.

**Pass condition derived from 1-3.** A survivor needs all three of:
- K >~ 3-10;
- a cone that contains many strongly correlated degrees of freedom within t_max;
- a low model floor.

In molecules and in 3d/4f solids, the first two conflict. Intersite-correlation features sit below Gamma_eff (J, B << Gamma), and the features above Gamma_eff are on-site multiplets. The regime that satisfies all three is the intermediate-q continuum Coulomb problem: plasmon/collective response of partially degenerate electrons, where v_F * t_max covers many particles and r_s ~ 2-4. That is C01 (and C07 for nuclear matter), both already in round 1. This lens therefore reinforces C01's regime but supplies no new independent candidate.

## 2. Per-problem kills

| # | Problem (brief example or added) | Evidence | Filter failure | Novelty | Verdict |
|---|---|---|---|---|---|
| K1 | L-edge XAS / 2p3d RIXS / K-beta XES of exchange-coupled multinuclear clusters (Fe-S, Mn-oxo) = round-1 C34 | Intersite scales: Heisenberg J in Fe-S / Mn-oxo ~ 10-50 meV, double-exchange B ~ 0.1 eV [order of magnitude, textbook; specific refs UNVERIFIED this session]. L3 natural width ~ 0.2-0.5 eV (Krause & Oliver 1979 order) plus instrument. Features above Gamma are single-ion multiplets, handled by CV-RAS-DMRG (mononuclear, arXiv:2305.08184) and ligand-field / charge-transfer multiplet fits. DMRG X-ray Raman of [2Fe-2S] exists (arXiv:1908.05802). Cost is fine: quantum RIXS at 20 orbitals = 414 logical qubits, 2.0e10 Toffoli (arXiv:2602.20270); XAS at CAS(22e,18o) (arXiv:2405.11015); logical QPE XAS on hardware with 3 orbitals (arXiv:2505.08612). S*G ~ 1e13-1e14 with 1e3-1e4 shots. But 18-22 orbitals are classically exact or DMRG-exact. | L5: K_intersite < 1, so the multinuclear correlation signature is washed out. High-resolution RIXS (20-30 meV) resolves J only through long final-state evolution, which is not short-time, and J is available from magnetometry, EPR or INS. F-classical at the sizes where cost passes. | C (quantum XAS/RIXS exists; no multinuclear advantage study) | **killed** |
| K2 | Attosecond charge migration after sudden ionization (correlation-driven hole dynamics) | TDDMRG with CAS(40o,35e) and D = 700 is "sufficiently converged" for furfural over 2 fs. The runs stop at 2 fs because nuclear motion enters "after a few femtoseconds" (arXiv:2409.05959). TD-ACI benchmarks against exact results (arXiv:1909.07810); MPS against FCI (arXiv:1902.08489). Dubey & Neufeld (arXiv:2609.23615, Sept 2026): the dominant hole-moment frequency is "roughly independent" of the correlation level, and transition dipoles set the timescales. Nuclear-motion decoherence: Nat. Phys. 18, 1150 (2022), doi:10.1038/s41567-022-01727-4. Canonical experiment: Calegari et al., Science 346, 336 (2014), doi:10.1126/science.1254061. A quantum method exists: Langkabel & Bande (arXiv:2205.10543). | F-sim at the sizes experiments probe. L6: the sudden-ionization initial state (pulse, photoelectron entanglement), the probe mechanism (fragment yields) and nuclear decoherence each exceed the solver spread. L5: the observable frequency is correlation-insensitive. Decision value is interpretive only. | C | **killed** |
| K3 | Early-time pump-probe response of correlated oxides (photodoped Mott, driven Hubbard) | Already killed in round 1 as C31/C28 (E for 1D, D for the 2D demos, L6 from phonons and heating). New short-time classical competitors: arXiv:2511.02809, 2608.19448, 2210.11490. | F-classical at early times. L6 (multi-orbital parameters, phonons). No decision flip. | D/E | **killed** |
| K4 | Shake-up / charge-transfer satellites in XPS | Molecules: approximate TD-dCC reproduces exact satellites and QP weights (SIAM, H2O, CH4); the same paper gives a QSP core-hole Green's-function algorithm (Abraham, Senapati, Pathak, Peng, arXiv:2511.17985, JCP 164, 104113 (2026)). Solids: LDA+DMFT+AIM captures nonlocal screening (arXiv:1812.06432). | F-classical. L6: U, Delta and double counting are fitted, and the parameter spread exceeds the solver spread. L5: oxidation-state assignment uses empirical satellite fingerprints from reference compounds. | C (2511.17985) | **killed** |
| K5 | Resonant Auger / core-hole clock | Molecular Auger widths come from complex-variable CC (arXiv:2110.08925, 2501.03362). Quantum Auger via GQE exists (arXiv:2603.12859). The core-hole clock in solids is effectively a one-particle Anderson-Newns problem (round-1 C40 kill: the free-fermion bath is compressible). | F-sim / F-classical. | C/D | **killed** |
| K6 | EUV photoresist absorption and photoemission (short cascade window) | Kharazi et al. (arXiv:2602.20234): 92 eV absorption = 200 logical qubits, 1e9 non-Clifford per circuit, 1e3 shots (S*G ~ 1e12, passes). Photoemission >= 1e14 gates x 1e4 shots (S*G ~ 1e18, fails). | L5: absorbance is measured directly by transmission, so computing it adds no information. The decision-relevant electron spectrum fails the cost screen. The quantum method is already published. | C/F | **killed** |
| K7 | Electronic stopping power (short projectile transit) | Round-1 C05: Rubin et al. arXiv:2308.12352 (PNAS 2024). | F (already claimed). | F | **killed** |
| K8 | Lifetime-broadened vibronic structure of core-excited / ionized states (ultrafast dissociation, JT bands) | A broad spectrum means a short-time autocorrelation. ML-MCTDH with LVC/QVC, and Gaussian-bath cumulants, are efficient at short times [argument; no new citation this session]. | F-classical. | - | **killed** |
| K9 | Electronic damage of metalloprotein clusters in <= 10 fs XFEL pulses | Dominated by incoherent photo/Auger rates and net-charge Coulomb forces [argument; refs not checked this session]. | L5 (correlation-insensitive decision). L6 (pulse parameters). | - | **killed** |
| K10 | WDM K-edge XANES / K-alpha spectator satellites for T, Z and IPD | IPD is a thermodynamic (static) quantity, and DFT-MD is the working classical twin [Vinko et al. Nat Commun 2014, UNVERIFIED this session]. The edge slope is set by Fermi-Dirac smearing, which mean-field theory captures. | Not a short-time dynamics problem. F-classical (round-1 C06 type). | - | **killed** |
| K11 | 163Ho electron-capture calorimetric spectrum shake-up/off near the endpoint (ECHo/HOLMES) | Atomic open-4f + core-hole problem, handled by restricted CI and multiplet codes [refs UNVERIFIED this session]. | L6: core-valence correlation and host-lattice effects (round-1 C04 pattern). | - | **killed** (out of lens) |
| K12 | Photonuclear GDR widths (broad, therefore short-time) | Round-1 C08/C09 pattern. | L6 (chiral Hamiltonian and currents), plus classical QRPA / CC-LIT. | - | **killed** |

## 3. Candidates returned

None. The nearest residuals are recorded so the next round does not repeat this search. All are `eligible = false`:
- **R1 (from K1).** Multinuclear core spectra, restricted to a system where an above-Gamma feature (>= 1 eV) is shown to depend on *intersite* correlation beyond what an embedded single-ion or small-cluster solver captures. No such system was found:
  - Mixed-valence Fe-S / Mn-oxo delocalization (B ~ 0.1 eV) sits below Gamma.
  - Delocalized cases with large intersite hopping (Cu_A-type, metal-metal bonded dimers) have few holes and are classically exact.
- **R2 (from K2).** Charge migration in molecules with >= 80-100 strongly correlated active orbitals, where the TDDMRG bond dimension would blow up within 2-5 fs. I found no published evidence of this blow-up. Even if it occurs, the model-floor terms (initial state, nuclear decoherence) remain.

**Gates that would reopen this lens.**
- (i) A published multi-family classical failure on an above-Gamma core-spectral feature of a multinuclear system, for example CV-RAS-DMRG, DMFT+AIM and RASPT2 disagreeing by more than the experimental error bars, *together with* a structural or redox assignment that flips with it.
- (ii) A published demonstration that TDDMRG, TD-ACI or Majorana propagation fails to converge within the nuclear-decoherence window, for a molecule with measured charge migration and a controlled initial state.

## 4. Implications for round 2

- The short-time lens gives a reproducible negative for molecules and 3d/4f solids, for the three reasons in section 1. A cheap circuit (S*G ~ 1e11-1e13, as in arXiv:2405.11015, 2602.20270 and 2602.20234) is available exactly where classical embedding, moment or perturbative methods already work.
- The only regime where short-time cost and a many-body cone coexist is continuum Coulomb matter at intermediate q, which is C01. The lens is evidence *for* C01's framing, not a new slot.
- It also suggests a concrete C01 sharpening: cap t_max in the Hadamard-test / linear-response circuits at hbar/Gamma_eff (plasmon damping + instrument), and report K = omega_p * t_max per (q, theta).

## 5. Query log (2026-09-28)

| # | Source | Query | Result |
|---|---|---|---|
| 1 | arXiv abs | 2210.11490 | Wild & Alhambra, short-time classical simulation (read) |
| 2 | arXiv API | abs:"charge migration" AND quantum computer/algorithm/qubit | timeout |
| 3 | OpenAlex | charge migration quantum computer | HTTP 429 (Retry-After 78498 s) |
| 4 | OpenAlex | attosecond charge migration benchmark ADC TDDMRG MCTDH | HTTP 429 |
| 5 | arXiv API | abs:"charge migration" AND abs:"quantum computer" | HTTP 429 |
| 6 | Crossref | charge migration quantum computer simulation attosecond | 20 items; no QC charge-migration paper; Nat Phys 2022 nuclear-motion item |
| 7 | Crossref | TD-DMRG charge migration molecules | TDDMRG chemistry papers (metadata only) |
| 8 | Crossref | quantum algorithm core-level XAS fault-tolerant | noise; nothing new |
| 9 | arXiv API | charge migration DMRG / tensor network | HTTP 429 |
| 10 | arXiv listing | charge migration DMRG (abstract) | 2409.05959 |
| 11 | Semantic Scholar | charge migration quantum computer | HTTP 429 |
| 12 | arXiv abs + html | 2409.05959 | CAS(40o,35e), D = 700, 2 fs, converged |
| 13 | arXiv listing | charge migration quantum computer | nothing relevant |
| 14 | arXiv listing | hole dynamics / charge migration / attosecond quantum circuit | 0 relevant |
| 15 | arXiv listing | attosecond "quantum computer" | 12 hits; only 2112.06365 is an algorithm (one electron) |
| 16 | arXiv listing | electron dynamics ionized molecule quantum computer simulation | 2205.10543 |
| 17 | arXiv abs | 2405.11015, 2602.20270, 2505.08612 | quantum XAS/RIXS resources |
| 18 | arXiv abs | 2602.20234 | EUV quantum resources |
| 19 | arXiv listing | core-hole quantum algorithm spectroscopy | 2511.17985 |
| 20 | arXiv abs | 2511.17985 | TD-dCC + QSP core-hole Green's function |
| 21 | arXiv listing | DMFT core-level photoemission nonlocal screening | 1812.06432 |
| 22 | arXiv listing | Hariki LDA+DMFT core-level spectroscopy | 2105.01248, 2004.01428 |
| 23 | arXiv abs | 1908.05802, 2305.08184 | DMRG core spectra of Fe complexes |
| 24 | Crossref | 10.1063/1.555595 | Krause & Oliver 1979 |
| 25 | arXiv listing | Majorana propagation fermionic simulation | 2608.19448, 2511.02809, 2503.18939 |
| 26 | arXiv abs | 2511.02809, 2608.19448 | regimes of classical efficiency |
| 27 | arXiv listing | charge migration ADC correlation | 0 results |
| 28 | arXiv listing | L-edge multinuclear cluster spectra DMRG | 0 results |
| 29 | arXiv listing | charge migration electron correlation benchmark | 2609.23615, 1909.07810, 1902.08489 |
| 30 | arXiv listing | iron-sulfur L-edge X-ray absorption simulation | 0 results |
| 31 | arXiv abs | 2609.23615, 1909.07810 | read |
| 32 | Crossref | 10.1038/s41567-022-01727-4; Calegari phenylalanine | metadata verified |
| 33 | arXiv listing | Auger quantum computer | 2603.12859 (GQE Auger); 2110.08925, 2501.03362 (CC Auger widths) |

Not searched:
- theses, patents and conference talks;
- J/B values for specific Fe-S / Mn-oxo clusters (cited as order of magnitude only);
- the ECHo, XFEL-damage and WDM-XANES literature (K9-K11 are argument-level kills).

## 6. Citation status

- **VERIFIED in this session** (abs page, listing or Crossref record read):
  - arXiv abs page or listing: 2210.11490; 2608.19448; 2511.02809; 2503.18939 (listing only); 2409.05959 (abs + html); 2205.10543 (listing); 2405.11015; 2602.20270; 2505.08612; 2511.17985; 2602.20234; 2305.08184; 1908.05802 (abstract; authors not extracted); 1812.06432 (listing; PRB 100, 075146); 2105.01248 and 2004.01428 (listing); 2609.23615; 1909.07810 (JCP doi:10.1063/1.5126945 per the arXiv page); 1902.08489 (listing); 2603.12859, 2110.08925 and 2501.03362 (listing).
  - DOIs: 10.1063/1.555595; 10.1126/science.1254061; 10.1038/s41567-022-01727-4. Crossref did not confirm the first author of the last one; the page attributes it to H.J. Worner [UNVERIFIED].
- **Carried over from round-1 notes** (not re-checked here): arXiv 2308.12352 (Rubin et al., stopping power).
- **UNVERIFIED**: specific J/B values for Fe-S and Mn-oxo clusters; Vinko et al. Nat Commun 2014 (IPD by DFT); the ECHo / 163Ho spectral-shape literature; the XFEL damage literature (K9).
