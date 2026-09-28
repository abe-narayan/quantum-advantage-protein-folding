# ROUND3 lane: new mechanisms, lens C — protein-intrinsic quantum physics that determines structure

_2026-09-28. Lane `new_mechanisms_intrinsic`. All artefacts are in this folder. No file outside it was modified, nothing was committed, and the governor jobs were not touched. Every run was single-threaded, used < 2 CPU-min in total and < 0.5 GB RAM. PDB files were cached in the session scratchpad, not in the repository._

**Question.** Is there an active-site structural question in proteins whose answer is set by quantum-mechanical physics that classical methods cannot compute accurately? Candidates: protonation, tautomer and hydride positions; spin-state-dependent metal-site geometry; ligand identity at multi-metal clusters; delocalised protons. The question is answered **SUPPORTS** only if all three hold:
1. the question is structurally consequential (> 0.1 Å);
2. its binding error is solver error that lies beyond the best classical solver;
3. the fault-tolerant (FT) quantum cost is realistic.

**Verdict: WEAK.**

- **Consequential: yes.** Discrete electronic-state changes move active-site structure by 0.3–1.2 Å [MEASURED, §1]. In myoglobin the effect reaches past the first shell by only ~0.1 Å above the crystal-to-crystal baseline [MEASURED].
- **Solver-limited beyond classical reach: no, for every question examined.**
  - Every open-shell cluster in the census has ≤ 8 strongly coupled transition metals and an active space of ≤ ~76 orbitals [MEASURED census + DERIVED estimate]. That is the size already solved classically to chemical accuracy for the FeMoco model [LITERATURE-SUPPORTED, preprint].
  - The value of an *exact* solver over the best classical one is capped by the model-error floor (environment, QM region, sampling, geometry). When the two error sources are equal, an exact solver raises the probability of picking the right structure by at most 8.3 percentage points [DERIVED, §3].
  - No scenario satisfies "exact solver brings the structural error below 0.1 Å while the best classical solver cannot" [DERIVED from literature-anchored inputs].
- **FT cost: realistic only for single energies.** A single FeMoco-76 energy is near cost parity with classical: 8.6 h on 4.5 M physical qubits [LITERATURE-SUPPORTED], against 4×10⁴–2.8×10⁶ core-hours classically [LITERATURE-SUPPORTED]. A structural *assignment* needs 30–5000 energies, which is 10 days–10 years of single-QPU time at 76 orbitals, and 1.6–450 QPU-years at the 404-orbital level where the classical solver is weakest [DERIVED/INFERENCE, §5].

**Claim category.** Any quantum gain here is **category 3 (computational/resource), constant-factor or polynomial, at the chemistry level** (one FeMoco-class energy). It is not a protein-structure advantage.

| Claim | Theoretical level | Practical level |
|---|---|---|
| Protein-structure endpoint | **L0** | **L0** |
| Chemistry sub-question (energy of one fixed state of a FeMoco-class cluster) | **L1** | **≤ L1** |

Why L1 for the chemistry sub-question:
- It is a polynomial precision gain over exact diagonalisation.
- Guided local-Hamiltonian BQP-completeness is generic. There is no instance-specific separation, and no evidence of a generic exponential advantage [LITERATURE-SUPPORTED: Lee et al. 2208.02199].
- In practice this is constant-factor parity at best.

**Relation to prior kills.** This lane re-attacks QM-23 / K-103 ("metal-cofactor QPE and NQE for protein structure: killed; effects below 0.1 Å"). The formulation is materially different: the endpoint is **local active-site structure**, meaning discrete isomer, spin-state and ligand identity, not backbone RMSD. Under that endpoint the QM-23 argument "effects < 0.1 Å" is **false**: the levers are 0.3–1.2 Å. The direction still fails, for a different reason: the **solver-vs-model decomposition**, plus classical reach at the largest biological cluster size.

Tags: MEASURED (this lane, files below); DERIVED (argument or computation given here); LITERATURE-SUPPORTED (abstract or text verified this session through the arXiv API or arXiv PDF; `lit/abstracts.txt`, `lit/verified_excerpts.txt`); LITERATURE-RECALLED (not verified this session, marked UNVERIFIED); INFERENCE; UNPROVEN.

---

## 1. How much structure moves when the electronic state changes (MEASURED, `results/pdb_census.json` → `levers`)

All inputs are experimental structures, used only for scientific analysis. Nothing is optimised or selected against them. PDB titles and resolutions were checked from the file headers.

| Lever | Pair (resolution) | Measurement | Δ |
|---|---|---|---|
| Heme Fe(II) high-spin (deoxy) vs low-spin (oxy): Fe out of the 4-N plane | Mb 1A6N (1.15 Å) vs 1A6M (1.00 Å) | Fe-oop 0.364 → 0.023 Å; Fe–N_p 2.074 → 2.006 Å; Fe–NE2(His93) 2.141 → 2.064 Å | **0.34 Å** |
| Same, beyond the first shell (whole-chain CA superposition) | Mb 1A6N vs 1A6M | CA shift, median by distance from Fe: 0.21 Å (0–8 Å), 0.16 (8–12), 0.10 (12–16), 0.10 (16–20), 0.10 (> 20). His93 CA 0.25 Å; F helix mean 0.15 Å (max 0.25); far A helix 0.08 Å | **~0.1–0.15 Å above baseline, local** |
| Heme in Hb (deoxy-T vs oxy-R; per-subunit superposition) | 2HHB (1.74 Å) vs 1HHO (2.10 Å) | Fe-oop Δ 0.33 (α), 0.44 (β); F-helix CA shift 0.83 (α), 1.22 (β) Å against > 20 Å baseline medians 0.42/0.46 Å | 0.4–0.8 Å excess, **confounded** by quaternary T/R and different crystal forms |
| P-cluster redox (PN → POX): ligand switch | 3MIN vs 2MIN (both 2.03 Å, same paper) | min Fe–OG(Ser β188) 2.80/2.84 → 1.90/2.07 Å; min Fe–N(Cys α88) 3.30/3.40 → 2.15/2.19 Å; Fe–Fe pairs < 2.9 Å: 12 → 9 (the cluster opens) | **0.8–1.2 Å** |
| FeMoco belt ligand identity | 3U7Q (1.0 Å) vs 4TKV (1.5 Å, CO-bound) | chain A: S2B absent, μ2-CO (CMO504) bridges Fe2–Fe6; Fe2–Fe6 2.576 → 2.486 Å | ligand identity change |
| Type-3 Cu: deoxy vs oxy (side-on peroxo) | 1LLA (2.18 Å) vs 1OXY (2.40 Å) | Cu–Cu 4.61 → 3.59 Å. A bis(μ-oxo) core would be ~2.8 Å [LITERATURE-RECALLED, UNVERIFIED] | **1.0 Å** (0.8 Å to the alternative isomer) |
| OEC S1 (dark) → 2-flash (≈ S3) | XFEL 6JLJ vs 6JLL (2.15 Å) | Mn–Mn changes ≤ 0.17 Å (Mn3–Mn4 2.917 → 2.752, Mn1–Mn2 2.578 → 2.688, chain A) | ≤ 0.17 Å (near coordinate error) |
| OEC, synchrotron vs XFEL dark state | 3WU2 (1.9 Å) vs 6JLJ | Mn1–Mn2 2.869/2.761 vs 2.578/2.607 Å | 0.15–0.29 Å *measurement-dependent* (radiation reduction [LITERATURE-RECALLED]) |

**Reading [INFERENCE].** Electronic-state questions have large *local* structural consequences: ligand switches, ligand identity, and metal–metal distance changes of ≥ 0.8 Å. Spin-state doming reaches ~0.1–0.15 Å past the first shell in Mb. In Hb it is amplified allosterically, which is well known and experimentally characterised. In every lever above, the electronic state is known from experiment (redox poise, ligand, EPR/Mössbauer/Raman), and the geometry is reproduced by DFT once that state is given. The computational question that remains is **which state/isomer**, a ranking of energies. §3 addresses it.

## 2. Census: how large are the quantum-hard parts of protein active sites? (MEASURED structure + DERIVED estimate, `results/pdb_census.json` → `census`)

Twenty PDB entries were chosen to include the largest known open-shell cofactors. Clusters are transition metals connected by M–M < 3.0 Å or by shared bridging atoms; Ca joins through a shared bridge. The active-space estimate is AS_dp = 5 × (open-shell-capable d metals) + 3 × (bridging S/O/C/N), plus 4 porphyrin π orbitals for a heme.

| Site (PDB) | Open-shell TMs | AS_dp (this estimate) | Literature active space | Heavy atoms ≤ 8 Å (×2 with H) |
|---|---|---|---|---|
| FeMoco, MoFe7S9C (3U7Q) | 8 | 70 | (113e, 76o) [LITERATURE-SUPPORTED: 1809.10307, 2502.15882 table] | 304 (~610) |
| P-cluster, Fe8S7 (3U7Q/3MIN/2MIN) | 8 | 67 | (114e, 73o) [LITERATURE-SUPPORTED: 2311.02854] | 290–318 |
| [FeFe] H-cluster, 6 Fe (3C8Y) | 6 | 54 | — | 315 |
| CODH C-cluster, NiFe4S5 (1JJY) | 5 | 40 | — | 225 |
| OEC, Mn4CaO5 (3WU2/6JLJ/6JLL) | 4 (+Ca) | 35 | CAS(44e,35o) [LITERATURE-RECALLED: Kurashige et al. 2013, UNVERIFIED] | 208–228 |
| [4Fe-4S] (1FDN/1WUI/3C8Y) | 4 | 32 | (54e, 36o) [LITERATURE-SUPPORTED: 2502.15882] | 165–236 |
| [3Fe-4S] (1WUI) | 3 | 27 | — | 215 |
| [2Fe-2S] (1A70/3C8Y) | 2 | 16 | (30e, 20o) [LITERATURE-SUPPORTED: 2502.15882] | 143–167 |
| [NiFe] hydrogenase centre (1WUI) | 2 | 19 | — | 202 |
| sMMO diiron (1MTY) | 2 | 13 | — | 163 |
| Oxy-hemocyanin Cu2O2 (1OXY) | 2 | 16 | — | 176 |
| Heme (2CPP, Mb, Hb, PSII cyt) | 1 | 9 | P450 Cpd I (47e,43o)–(63e,58o) [LITERATURE-SUPPORTED: 2502.15882, 2407.07411] | 103–116 |
| Type-1 Cu (1PLC) | 1 | 5 | — | 117 |

- **Calibration [DERIVED].** AS_dp is 8–20% below the literature active spaces for the Fe–S/Mo clusters, and it matches the OEC CAS(44,35) orbital count. It badly undercounts hemes, because heme active spaces include porphyrin π and double-shell orbitals for dynamic correlation (Goings et al.).
- **Largest cluster [MEASURED over this curated set; INFERENCE for the PDB as a whole].** The largest strongly coupled open-shell cluster has **8 transition metals** (FeMoco, P-cluster), with AS ≤ ~76 orbitals. Larger metal assemblies are either weakly coupled, such as multi-heme cytochromes with Fe–Fe > 9 Å, or closed-shell, such as d10 metallothioneins and d0 polyoxomolybdates. A full RCSB chemical-component survey was not run (next test 4).
- **Environment dominates in size [MEASURED + LITERATURE-SUPPORTED].** Every site has 100–320 heavy atoms (~200–640 atoms with H) within 8 Å. QM/MM energetic and structural properties "approach asymptotic limits with only very large (ca. 500–1000 atom) QM regions", partly through charge transfer that better MM cannot fix (Karelina & Kulik, 1701.00427). The quantity a QPE solves exactly, the active-space Hamiltonian of ≤ 76 orbitals, is therefore one part of an error budget whose other parts (QM-region size, embedding, electrostatics, sampling) are 10× larger systems and are not strongly correlated.

## 3. Solver error vs model error: what an exact solver can buy (DERIVED, `scripts/decision_value.py` → `results/decision_value.json`)

**Model [DERIVED].**
- Two candidate states A and B, true gap Δ ≥ 0, structural lever δq.
- Computed gap: Δ̂ = Δ + e_s + e_m, with solver error e_s ~ N(0, σ_s²) and model error e_m ~ N(0, σ_m²). The model error covers environment/QM region, conformational and thermal averaging, geometry, basis, relativistic effects and active-space definition.
- An exact (QPE) solver sets σ_s = 0 and leaves σ_m untouched.
- Readout 1 (argmin): expected structural error = δq·Φ(−Δ/σ).
- Readout 2 (Boltzmann populations at 300 K): computed by Gauss–Hermite quadrature.

**Closed form (argmin, worst-case gap) [DERIVED].** The largest possible gain from an exact solver is

  max_Δ [Φ(Δ/σ_m) − Φ(Δ/√(σ_s²+σ_m²))], attained at Δ* = a·b·√(2 ln(b/a)/(b²−a²)), where a = σ_m and b = √(σ_s²+σ_m²):

| σ_s/σ_m | 0.25 | 0.5 | 1 | 2 | 5 |
|---|---|---|---|---|---|
| max gain in P(correct structure) | 0.7% | 2.7% | **8.3%** | 18.5% | 32.6% |

Multiply by δq to get Å. An exact solver can matter only where the **best classical** solver error is well above the model floor. The comparator is the best classical solver, not DFT.

**Literature anchors for σ (all LITERATURE-SUPPORTED unless marked).**
- **Best classical solver.**
  - FeMoco LLDUC (113e,76o) ground state to ~1 kcal/mol by CC/DMRG composites with extrapolation (Zhai et al. 2601.04621, preprint).
  - In that paper's (404o,277e) space the affordable UCCSD ranking has an "ordering uncertainty" of ~5 kcal/mol, and the two lowest spin isomers lie 1.6 kcal/mol apart (same paper).
  - Converged CC/DMRG composite protonation energetics for a dimeric nitrogenase Fe–S model: B3LYP is the best of 10 functionals, with MAE 10 and max 13 kJ/mol, i.e. 2.4 and 3.1 kcal/mol (Zhai et al. 2305.07227).
  - ph-AFQMC gives MAE 1.4 kcal/mol for 3d transition-metal bond energies, against 2.8 for CCSD(T) with max > 17 (Shee et al. 1901.09464).
  - ph-AFQMC with broken-symmetry trials is *unreliable* for Fe–S clusters (Kjønstad et al. 2605.03270), so it is not counted as a classical solver there.
  - CCSD(T) and semilocal DFT "fail badly" for Fe(II) spin-crossover spin gaps, while fixed-node DMC converges (Song et al. 1708.08425).
- **Model floor.**
  - P450 Cpd I: the doublet–quartet gap is 0.02 kcal/mol, and "dielectric environment, and cysteine ligand model can easily shift the energies by enough to change the qualitative result … reliable identification of the lowest spin state of Cpd I as it appears in most experiments is not feasible" (Goings et al. 2202.01244).
  - Fe(II)-porphyrin: classical studies disagree on the ground spin state (AFQMC: triplet at the model geometry, 2001.05109; DMRG-TCC: quintet, and the result depends on Fe–N distances, 2001.04903). AFQMC shows that "neither triplet nor quintet is strongly correlated". The disagreement is geometry/model, not static correlation.
  - FeMoco: an MD-averaged QM/MM electrostatic environment leaves the spin-isomer landscape "qualitatively unchanged" (2601.04621). The σ_m of 1–4 kcal/mol used below is an INFERENCE from these.

**Scenario results** (inputs and tags in `decision_value.py::SCEN`). δq is MEASURED where §1 has it. The "favourable" column takes the largest σ_best, the smallest σ_m and the smallest gap scale. "Err" is the prior-averaged expected structural error (argmin readout).

| Question | δq (Å) | Favourable: Err best-classical → exact, VOI | Central: VOI | Solver-limited beyond classical? |
|---|---|---|---|---|
| S1 heme Fe(II) spin state → doming (Mb) | 0.34 | 0.091 → 0.050, **0.041** | 0.017 | no (the spin state is known experimentally) |
| S2 P450 Cpd I doublet vs quartet | ≤ 0.02 | 0.010 → 0.010, 0.000 | 0.000 | no (structurally inconsequential; model-limited) |
| S3 FeMoco resting spin isomers (BS7/BS8) | 0.02–0.05 | 0.020 → 0.009, 0.011 | 0.004 | no (inconsequential) |
| **S4 FeMoco E4 hydride/protonation/belt-S isomer** | 0.8–1.5 | **0.507 → 0.281, 0.227** | 0.053 | **no**: an exact solver still leaves 0.28 Å (model floor) |
| S5 P-cluster redox ligand switch | 0.8–1.2 | 0.335 → 0.225, 0.110 | 0.024 | no (redox state set experimentally; both structures solved) |
| S6 OEC S2 open vs closed cubane | 0.8–1.2 | 0.489 → 0.375, 0.114 | 0.045 | no (EPR reports it; the 35-orbital space is classical) |
| S7 Cu2O2 side-on peroxo vs bis(μ-oxo) | 0.8 | 0.177 → 0.118, 0.059 | 0.016 | no (the 16–32-orbital space is exact classically) |
| S8 proton position in short H-bonds (KSI, PYP) | 0.1–0.4 | 0.122 → 0.100, 0.022 | 0.003 | no (closed-shell; NQE classical-exact, §6) |

**Reading.**
- The only question where an exact solver buys a non-trivial structural gain is **S4**, FeMoco E-state isomer identity, and only under favourable assumptions: σ_best = 5 kcal/mol (UCCSD-level ranking in a large space) against σ_m = 2 kcal/mol. The gain there is 0.23 Å of expected error on a ~1 Å lever. The residual with an exact solver is still 0.28 Å [DERIVED from the stated inputs].
- With the central assumptions, the gain falls to 0.05 Å. These are σ_best ≈ 3 kcal/mol and σ_m ≈ 3 kcal/mol [INFERENCE]. The σ_best value sits between UCCSDT at 76 orbitals, whose family ordering agrees with large-D UDMRG per 2601.04621, and UCCSD at 404 orbitals (±5).
- S4 is therefore **co-limited**: solver and model errors are comparable. It is not solver-limited beyond classical reach.

## 4. Classical reach for these active spaces (LITERATURE-SUPPORTED)

- **FeMoco (113e,76o).**
  - Ground state to ~1 kcal/mol by CC + DMRG composites with extrapolation (2601.04621, preprint).
  - Costs: UCCSDTQ composite 4.0×10⁴ core-h; UDMRG at D = 18,000 2.77×10⁶ core-h; ideal-Frontier variational DMRG at D = 393,000 22.9 h, against 8.6 h for the quantum estimate at O(1) overlap.
  - The same paper concludes that "the complexity of the low-energy electronic structure lies not in the description of intrinsically multi-configurational effects, but the correct ranking of many competing, but largely single-configuration, states". That ranking is exactly what broken-symmetry CC does classically. A QPE would have to repeat the same ranking state by state.
- **P-cluster (114e,73o).** DMRG at D = 14,000 on 48 A100 GPUs (2311.02854). Earlier work covers three oxidation states (1810.10196).
- **P450 Cpd I (63e,58o) and FeMoco (113e,76o).** DMRG sustained 246 TFLOPS on a single DGX-H100 node (2407.07411, performance study). Goings et al. estimated ~3.7×10⁴ CPU-h for M = 3000 on the 58-orbital space and call larger spaces "quickly intractable".
- **Orbital optimisation.** DMRG-SCF has been run at CAS(82,82) (2503.20700).
- **State preparation is no longer the obstacle.** Entanglement-minimised orbitals raise the initial-state overlap by ~10² (P-cluster) and ~10⁵ (FeMoco) (2506.13386). MPS preparation at D = 4000 gives overlap² ≈ 0.9 for a FeMoco candidate state (2409.11748). Both help the quantum side, and both are classical inputs.
- **Hardness classification.** Some open-shell Fe–S clusters and FeMoco are "class-2" (no small set of dominant determinants) (Mörchen, Low, Weymuth, Liu et al. 2409.08910). By the §2 census, class-2 sites in proteins are capped at 8 metals.

## 5. Fault-tolerant cost (LITERATURE-SUPPORTED anchors; DERIVED/INFERENCE extrapolation)

**Anchors (all verified in `lit/verified_excerpts.txt`).**
- Spectrum amplification (DFTHC+BLISS+SA; Low et al. 2502.15882), in Toffolis:

  | Active space | Toffolis |
  |---|---|
  | Fe2S2-20 | 3.97×10⁷ |
  | Fe4S4-36 | 1.72×10⁸ |
  | FeMoco-54 | 3.41×10⁸ |
  | P450X-58 | 4.91×10⁸ |
  | FeMoco-76 | 9.99×10⁸ |

  FeMoco-76 runs in **8.6 h on 4.5 M physical qubits** (1 µs cycle, 10 µs reaction time), which implies 3.2×10⁴ Toffoli/s.
- THC (Lee et al. 2011.03494): FeMoco-76 3.2×10¹⁰ Toffolis, 2196 logical qubits, ~4 M physical qubits, < 4 days.
- With MPS state preparation and filtering (Berry et al. 2409.11748): 7.3×10¹⁰ Toffolis.
- Early-FT, STAR architecture (Kanasugi et al. 2603.22778):
  - [4Fe-4S]-36o: 1.6×10⁵ physical qubits, 42–49 days on one QPU.
  - P450 Cpd I 43o: 2.2×10⁵ qubits, 84 days.
  - These are active spaces that DMRG already handles. The comparator in that paper is FCI.

**Extrapolation [DERIVED fit; INFERENCE beyond 76 orbitals].** A log–log fit of the SA series gives Toffolis ∝ N^2.35 (max ln-residual 0.18). Hours per energy at 3.2×10⁴ Toffoli/s:

| Site | Hours per energy |
|---|---|
| Cu2O2 | 0.2 |
| [2Fe-2S] | 0.34 |
| [4Fe-4S] | 1.4 |
| OEC | 2.2 |
| P450 | 4.2 |
| P-cluster | 7.2 |
| FeMoco | 7.9 (8.6 verified) |
| 404-orbital FeMoco space (dynamic correlation) | 470–780 (α = 2.4–2.7), ~5× the logical qubits |

**Per structural question [INFERENCE].** The S4 question (E4 isomer identity) needs:
- 10–50 protonation/hydride isomers;
- × 3–10 low-lying broken-symmetry families;
- × 1–10 environment snapshots;
- = **30–5000 energies**.

That is **10–1640 QPU-days** at 76 orbitals with perfect overlap (**23–3770 days** with the ×2.3 state-preparation overhead), and **1.6–450 QPU-years** at 404 orbitals. Geometry relaxation with QPE forces would multiply this again: forces "on a single nucleus may be of similar cost to estimating energies" (O'Brien et al. 2111.12437).

**Break-even price [DERIVED].** For one FeMoco-76 energy, parity requires one 4.5 M-qubit QPU to be worth **ρ\* ≈ 5×10³** (against the UCCSDTQ composite) **to 3.5×10⁵** (against UDMRG at D = 18k) CPU cores.
- This is the one place in the lane where a **practical constant-factor resource advantage (category 3) is plausible**.
- It concerns the energy of one fixed state, at the chemistry level. Classical methods have already solved that instance to the target accuracy.
- Structural assignment multiplies the cost on both sides equally, and classical screening (BS-UCCSD) is cheap, so the advantage does not grow with the structural question.

## 6. Proton delocalisation and nuclear quantum effects (DERIVED + LITERATURE-SUPPORTED)

- Short H-bonds exist at the sites that are usually cited [MEASURED]:
  - KSI (1OH0): Tyr16 OH–Tyr57 OH 2.51 Å, Tyr16–equilenin 2.54 Å, Asp103–equilenin 2.48 Å.
  - PYP (1NWZ, 0.82 Å): Tyr42 OH–pCA O4′ 2.49 Å, Glu46–pCA 2.58 Å.
- The electronic structure is closed-shell and weakly correlated [INFERENCE].
- The nuclear problem is a positive-weight imaginary-time path integral whenever exchange is negligible [DERIVED]. The proton thermal wavelength at 300 K is λ = 1.00 Å (D: 0.71 Å). The exchange factor exp(−2πd²/λ²) is 8×10⁻⁷ at d = 1.5 Å and 1.5×10⁻¹¹ at d = 2.0 Å. There is therefore no sign problem: PIMD is classical-exact up to bead and Trotter error.
- Wang, Fried, Boxer & Markland (1501.00241, PNAS 2014) used "ab initio simulations that exactly include nuclear quantum effects" for the KSI network. Recent ML-potential PIMD extends this to peptides (2512.05741).
- **This branch is KILLED again, for the same reason as QM-23(b).** A quantum computer adds nothing.

## 7. Radicals and charge-transfer states [INFERENCE]

- Protein radical intermediates (for example the RNR tyrosyl radical, and PCET relays) and charge-transfer states are mostly single-reference doublets or low-multireference excited states. TDDFT, EOM-CC and CASPT2/NEVPT2 with ≤ 20 orbitals treat them.
- Their structural signatures are local and are captured by spectroscopy or time-resolved crystallography.
- A 2026 multistate quantum-dynamics hardware demonstration on a P450-inspired model is reproduced by exact classical evolution: a 10 fs population of 0.488 classically, and 0.42 measured on hardware against 0.43 on the matched emulator (2607.05786) [LITERATURE-SUPPORTED].
- No structurally consequential, solver-limited question was identified here.

## 8. Per-candidate decision

| Candidate | Consequential (> 0.1 Å)? | Binding error | Best classical reaches the needed accuracy? | FT cost per question | Cheap experimental bypass | Verdict |
|---|---|---|---|---|---|---|
| Heme spin state / doming | yes, 0.34 Å local, ~0.1 Å beyond the first shell (Mb) | model/geometry (FeP disagreement) | yes (AFQMC/DMC/CC); no static-correlation core | hours per energy | Mössbauer, magnetometry | KILL |
| P450 Cpd I spin state | no (≤ 0.02 Å) | model (environment, ligand) | not resolvable by *any* solver without a better model | 4–73 h per energy | EPR/Mössbauer | KILL |
| FeMoco resting spin isomers | no (0.02–0.05 Å) | solver, at the model level | yes, ~1 kcal/mol (preprint) | 8.6 h per energy | ENDOR/Mössbauer | KILL (structure); chemistry parked |
| **FeMoco E-state hydride/protonation/ligand isomers** | **yes (0.8–1.5 Å)** | **solver and model co-limited** | at 76 orbitals yes (UCCSDT/DMRG); at 404 orbitals UCCSD ±5 kcal/mol | 10 days–10 years (76o); 1.6–450 years (404o) | ENDOR (partial) | **WEAK residue** |
| P-cluster redox ligand switch | yes (0.8–1.2 Å) | experimentally set redox state | yes (DMRG, three oxidation states) | 7 h per energy | crystallography (done) | KILL |
| OEC open/closed, S3 insertion | yes (~1 Å) | solver/model | yes (35–44 orbitals) | 2 h per energy | EPR, XFEL | KILL |
| Cu2O2 isomers, MMO Q core | yes (~0.8 Å) | historically solver (CASPT2 active-space failures) | yes (16–32 orbitals: exact) | < 1 h per energy | resonance Raman, EXAFS | KILL |
| Proton positions / LBHB / NQE | yes (0.1–0.4 Å) | model (electrostatics, pKa) | yes (PIMD exact; CC) | — | neutron crystallography | KILL |

## 9. What would change the verdict (revival conditions for the WEAK residue)

A SUPPORTS verdict needs **all** of the following at once:
1. A protein active-site isomer question with δq ≥ 0.5 Å where the best *feasible* classical ranking (UCCSDT/extrapolated DMRG at ≥ 100 orbitals) has σ_best ≥ 2·σ_m, and σ_m has been *measured*: a QM-region-size and environment ladder shows σ_m ≤ 1.5 kcal/mol for that charge-moving isomer set.
2. No spectroscopic or crystallographic observable already fixes the answer. For FeMoco E4, this means ENDOR/XAS leave ≥ 2 isomers within the model floor.
3. A resource estimate below ~10 QPU-days per structural question, which with α ≈ 2.35 means an active space ≤ ~100 orbitals and ≤ ~100 energies, while the classical σ_best at that size stays ≥ 2 kcal/mol.

Current evidence (§3–§5) says conditions 1 and 3 cannot both hold. Condition 1 needs a large active space, and condition 3 needs a small one.

## 10. Files, compute ledger, leakage

| File | Content |
|---|---|
| `scripts/arxiv_lit.py` | arXiv API literature pass (15 searches + id_list), writing `lit/arxiv_raw.json` and `lit/abstracts.txt` |
| `lit/verified_excerpts.txt` | Verbatim table and passage excerpts from arXiv PDFs 2011.03494, 2502.15882, 2601.04621, 2202.01244 and 2603.22778 (full texts were not kept) |
| `scripts/pdb_census.py` | Census of 20 PDB entries, structural levers (§1) and short-H-bond census, writing `results/pdb_census.json` |
| `scripts/decision_value.py` | Solver-vs-model decision model, scenario table, FT cost model and NQE exchange factor, writing `results/decision_value.json` |
| `results/summary.json` | Compact lane summary |

- **Compute.** Every run was single-threaded (OMP/MKL/OpenBLAS = 1), used < 1 CPU-min per script (< 2 CPU-min in total) and < 0.5 GB peak RAM. There was no background process, and no simulator runtime is reported as quantum runtime.
- **Quantum resources.** None were run. All quantum costs are literature estimates or extrapolations, tagged above.
- **Leakage status.** Native structures were used only for scientific analysis of structural levers. No DEP pipeline, optimisation or selection touched them (ORACLE-free by construction: no model is trained or tuned).
- **Statistical caveat.** The PDB levers compare different crystals at 0.8–2.4 Å resolution. Coordinate errors are ~0.02–0.2 Å, and the far-helix baselines (0.08–0.46 Å) are reported alongside each shift for that reason.

## Next tests (ranked by decision value)

1. **Measure σ_m for charge-moving FeMoco E-state isomers (decisive for the only residue).** Run a DFT-level QM/MM QM-region ladder (100 → 600 atoms) on 3U7Q-based E2/E4 isomer models, with electrostatic-embedding variations and MD snapshots. If the isomer-energy spread from the model alone is ≥ 3 kcal/mol, the S4 residue dies (VOI ≤ 0.05 Å).
2. **Literature/tooling watch for classical UCCSDT or extrapolated DMRG ranking of E4 isomers at ≥ 100 orbitals.** If σ_best ≤ 2 kcal/mol is shown classically, the residue dies on the solver side.
3. **QM-23's never-run test**, when PySCF/block2 are available (not installed; not installed here per the rules): DMRG-CASCI vs BS-DFT on [2Fe-2S](SCH3)4 for two protonation variants. This checks σ_best vs σ_DFT at a size where exact classical answers exist.
4. **Full RCSB chemical-component survey** for strongly coupled open-shell clusters with > 8 transition metals, to confirm the classical-reach cap.
5. **Resource watch.** Any QPE estimate for ≥ 300-orbital active spaces with realistic overlap and ≤ 10⁶ physical qubits would move condition 3.
