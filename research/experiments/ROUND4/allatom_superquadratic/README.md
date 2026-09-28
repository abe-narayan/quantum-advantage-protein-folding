# ROUND4 lane: allatom_superquadratic

_2026-09-28. The CRITIC D1 regime: physics-based all-atom sampling of folding kinetics and ensembles. Is there a
super-quadratic quantum algorithm whose preconditions hold for protein force fields, and does it beat the
enhanced-sampling classical twin within the pre-registered time limits?_

**Tags.** MEASURED (this lane, files below), DERIVED (algebra from stated inputs), THEORETICAL (a published theorem),
LITERATURE-SUPPORTED (the record was fetched verbatim this session: arXiv API, PubMed E-utilities or PMC full text),
INFERENCE, UNPROVEN, UNVERIFIED (recalled, not fetched).

**Leakage.** Native structures of 1L2Y (Trp-cage), 1PGA (protein G B1) and 1UBQ (ubiquitin) were used only as
starting geometries for three things: system-size bookkeeping, a timing benchmark, and a local dynamical analysis of
the force field at its minimum. Nothing is predicted, selected or tuned, so no DEP or ORACLE path exists here.

---

## Verdict: KILLS

1. **No family meets both arms.** Among the 12 families surveyed (53 arXiv records, all verified), every family that is
   super-quadratic against *practical* classical MD fails its precondition on protein force fields. The families
   whose preconditions plausibly hold are all quadratic (s = 2) against the practical twin.
2. **s = 2 fails the time test everywhere it matters.** Against one GPU:
   - T\*_Q,2 is at least **2.2 years** at t_T = 10 ns (most favourable case: Trp-cage, implicit solvent, generous G);
   - it is at least 2.2×10⁴ years at t_T = 1 µs;
   - for the ms folders (NTL9, protein G, ubiquitin, λ6-85) it is 35–1,400 years at 10 ns.

   Against the literature twins, s = 2 never wins at any t_T ≥ 10 ns. For example, NTL9 by weighted ensemble takes
   250 GPU-days; the quantum route takes 4.9 years.
3. **The kill is a "no applicable algorithm" kill, not a "classically easy" kill** [DERIVED].
   - At t_T = 10 ns, a hypothetical s = 3 or s = 4 algorithm would meet the task's time limit (T\*_Q,s ≤ 1 month) for
     every folder: T\*_Q,4 = 2.6 h to 10 d; T\*_Q,3 = 1 d to 160 d.
   - It would also beat the weighted-ensemble twin for ms folders: s = 4 gives 3–6 d against 220–250 GPU-days.
   - This regime is therefore *not* resource-dead for s ≥ 3, unlike the learned-energy regime (K-107).
4. **Neither the pre-registered rule nor the task rule is met.**
   - Pre-registered (Round 4): SUPPORT needs T\*_Q,s ≤ 1 day.
   - Task: SUPPORT needs T\*_Q,s ≤ 1 month at t_T ≥ 10 ns, with the family's preconditions holding.
   - Both rules need a family that satisfies both arms. None does.
5. **Correction to CRITIC D1 [DERIVED].** D1 put the all-atom oracle at G = 1e9–1e10 Toffolis per step. That holds only
   with a free neighbour list and cheap pair arithmetic.
   - With measured pair counts, generous G is 1.1e9 (Trp-cage, GB) to 4e10 (ubiquitin, explicit), and central G is
     4–13× higher.
   - D1's "s = 4 → 0.1–2.5 yr" matches our t_T = 1 µs numbers (T\*_Q,4 = 51 d to 13 yr).

---

## Pre-registration (applied as written)

- **PREREG_G1_C1_Q4.md, Round 4, all-atom item.** "SUPPORT only if a family's preconditions hold for protein force
  fields and T\*_Q,s ≤ 1 day at a stated t_T."
- **Lane task (stricter on hardware, looser on time).** SUPPORTS only if some family's preconditions plausibly hold
  **and** T\*_Q,s ≤ 1 month at t_T ≥ 10 ns.
- **Comparator.** The enhanced-sampling classical twin (REST2 / metadynamics / MSM / weighted ensemble / AI
  emulators) from the literature, with costs in effective MD steps.
- **Formula.** Unchanged from ROUND3 `hardness_what_it_takes`, as used in CRITIC D1:
  - X = AρK n_b G t_T / c
  - B\*_s = X^{s/(s−1)}
  - T\*_Q,s = K n_b G t_T X^{1/(s−1)}
  - exponential speedup: T\* = K n_b G t_T
- The two rules give the same verdict.

---

## (1) Survey: quantum algorithm families for classical MD, Liouville/Fokker–Planck, Gibbs sampling, free energies and rates

**Sources.**
- `lit/arxiv_survey.py`: 31 arXiv API queries restricted to 2019–2026, plus an id list. 341 unique verbatim records
  in `lit/records.json`.
- `families.py`: fails if any cited id was not fetched. All 53 ids are present.
- The details of Kharazi et al. 2026 were read from the arXiv HTML full text (a WebFetch summary, quoted).

| Family (key refs, arXiv) | Claimed speedup | Precondition | Protein force field? | s against practical MD twin |
|---|---|---|---|---|
| **Carleman linearisation**: Liu 2011.03185 (PNAS 2021); Krovi 2202.01054; Costa 2312.09518; Wu 2405.12714; Jennings 2509.07155; Li–An 2608.25822; Berntson 2607.14308 | Exponential in dimension for R < 1; intractable for R ≥ √2 (THEORETICAL, Liu). Extensions: negative log-norm; Lyapunov-weighted, stable or non-resonant systems; fast-forwarding for weakly nonlinear dissipative ODEs; super-quadratic for a certified weakly nonlinear plasma | Re λ(F1) < 0; R < 1; weak nonlinearity and non-resonance; polynomial drift | **FAILS.** Newtonian or explicit-solvent MD: Re λ = 0, so R = ∞. Langevin: R ≥ **4.3×10³ to 1.2×10⁵** (MEASURED, below) | none |
| **Chaos limit**: Lewis 2307.09593 (Quantum 2024); Brüstle–Wiebe 2407.07685 | Any algorithm that outputs the normalised solution state costs ≥ exponential in time when a Lyapunov exponent is positive (THEORETICAL) | This is an obstruction, not an algorithm | **APPLIES.** λ_max = 2.1–3.2 ps⁻¹ (MEASURED, all-atom); λ τ_f ≈ 2×10⁶–2×10⁷ (1 µs) to 2×10⁹–2×10¹⁰ (1 ms) e-folds | no-go for trajectory-state routes |
| **KvN / Liouville embedding**: Joseph 2003.09980 (PRR 2020); Lin 2202.02188; Jin 2209.08478, 2202.07834; Tanaka–Fujii 2305.00653; Fredon 2609.28999; Watanabe 2605.30142 | Exponential vs an Eulerian grid. Against Monte Carlo, Joseph writes: "a quadratic improvement over classical probabilistic Monte Carlo algorithms" (LITERATURE-SUPPORTED) | Sparse KvN Hamiltonian; smooth density | MD **is** the Monte Carlo solver of the Liouville/Kramers equation. The gain is in precision only, with no gain in physical time | **2** |
| **Fokker–Planck / Kolmogorov as a linear PDE** (QLSA, LCHS, Schrödingerisation, Lindblad maps): Gnanasekaran 2303.02463; Tennie 2401.13500; Jin 2412.14868; Wu–Li 2608.09903; An 2303.01029, 2312.03916; Watanabe 2605.30143 (Langevin KvN MD, demonstrated on H₂ only) | Exponential vs grid PDE solvers | Discretisation and conditioning | The exponential is against the wrong twin (grids). Against MD: precision only, plus at most √t fast-forwarding of dissipative generators | **2** |
| **Rate estimation in overdamped Fokker–Planck**: Kharazi 2601.15523 (2026) | Õ((η^{5/2}√(tβ)α_V + η^{3/2}√(t/β)N)/ε) against a *worst-case* classical O(tη²e^{Ω(η)}/ε⁴). The authors: "should not be interpreted as a speedup over all classical simulation methods" | Overdamped dynamics; smooth pairwise V (LJ only through smoothed surrogates); warm start in an m-strongly-convex reactant region; additive ε | **Partly.** e^{Ω(η)} and ε⁻⁴ come from worst-case weak-error step bounds that MD does not pay (fixed 2 fs steps, Metropolised integrators). Per-step η^{5/2} is worse than MD's η to η². The unfolded basin is not convex. Additive ε ≪ kt ≈ 10⁻⁵ (see below) | **2** against brute-force MD; **< 1** against WE for small rates |
| **Nonlinear SDE algorithms**: Bravyi 2507.06198, 2606.08349; Li 2603.12398; Miyamoto 2604.24133; Gan 2511.09939; Chandramouli 2607.28541 | poly(log N) for dissipative quadratic-drift SDEs (BQP-complete). The 2025 version is exponential in the inverse relative initial-condition error | Polynomial drift; dissipation on every mode (λ₁ > 0); norm-preserving drift; correlators of O(1) variables | **FAILS.** Forces are non-polynomial. Langevin damps only momenta: λ₁,eff = ω_min²/γ = 0.018 ps⁻¹ (MEASURED) against a nonlinearity rate of about 2×10³ ps⁻¹. Folding observables involve O(L) variables. The gain is in N ≤ 10⁵ (a constant), not in time | none |
| **Coupled oscillators**: Babbush 2303.13012 (PRX 2023); Danz 2405.08694; Schade 2609.20721 (2026) | Exponential for 2ⁿ oscillators behind succinct oracles. Schade: no exponential advantage for local 3-D topologies, but a **quartic** speedup for locally coupled *damped linear* oscillators in 3-D | Linear (harmonic) dynamics | **FAILS for folding.** Barrier crossing is anharmonic; there are ≤ 10⁵ explicit atoms. The quartic result covers elastic-network vibrations, which carry no folding information (QM-26, K-103) | 4, but only for structure-free linear ENM observables |
| **Continuous Gibbs samplers**: Leng 2505.05301 (PNAS 2026); Childs 2210.06539; Ozgul 2310.11445, 2504.03626; Motamedi–Ronagh 2210.08104; Olivucci 2608.24527; Li–Liu 2604.00656 | √(βdC_PI); √(1/Gap) for QRELD. "Up to quartic" holds only against MALA's Cheeger bound (quadratic against Poincaré scaling; `literature/domain_notes/lit_A_sampling.md` P44). Provable Ω(α) vs Õ(√α) on hide-and-seek tori | Warm start or annealing; smooth (Gevrey) V | **Plausible**, with smoothed force fields and annealing | **2** |
| **QMCMC, walks, partition functions, free energies**: Montanaro 1504.06987; Arunachalam 2009.11270; Harrow–Wei 1907.09965; Chen–Nannicini 2404.02414 (Ω(1/ε) lower bound); Huang 2508.16719; Günther 2506.20587; Mazzola 2108.11410 | Quadratic in samples and in gap | Coherent oracle; reversible chains | **Plausible.** FreeQuantum and the alchemist paper accelerate electronic structure, not force-field sampling | **2** |
| **Nonreversible-chain speedups**: Claudon 2501.05868 (Nat. Commun. 2025); Banerjee 2606.26584 | "Up-to-exponential", but against the nonreversible chain's *own* mixing time. Exact QFF fails beyond reversibility; √t survives only for \|α\| = O(t^{−1/2}) | "Reversibility on π-average", which the authors say has no general easy check | Unverifiable. The paper has no MD results. Underdamped Langevin is far from the perturbative regime | no evidence of > 2 |
| **MSM walks / annealer path sampling**: Ghamari 2201.11781 | None claimed | — | MSMs have 10²–10⁴ states (2,000 in Voelz 2010), which classical linear algebra handles in under 1 s. The cost is generating the MD data | none (DOA) |
| **Quantum-computed forces** (ab initio MD): 2008.06562, 2404.10001, 2212.11921 | Electronic-structure forces | — | Outside the regime: this changes the energy model. Folding needs 10¹¹–10¹² force evaluations of QPE scale | n/a |

**Survey conclusion.**
- Against the practical classical twin (MD, weighted ensemble, MSM, REST2/metadynamics), the largest exponent whose
  preconditions plausibly hold for a protein force field is **s = 2**.
- Every s ≥ 3 or exponential claim does one of two things:
  - it compares against a worst-case bound, a grid solver or the chain's own mixing time rather than practical MD; or
  - it requires dissipative or weak nonlinearity, linear dynamics, polynomial drift, or 2ⁿ succinct size, none of
    which a protein force field provides.
- These statements are LITERATURE-SUPPORTED for the claims and DERIVED/MEASURED for the precondition checks.

### Carleman R for an all-atom protein at 300 K (MEASURED): `allatom_measure.py` S3/S4 → `work/S4_1L2Y.json`

**Setup.**
- Trp-cage (1L2Y): 304 atoms, amber14-all + GBn2.
- Flexible (no constraints), so all 906 internal modes are present, spanning 6.7–3,702 cm⁻¹.
- Double-precision Reference platform; energy-minimised (rms force 0.05 kJ/mol/nm; 0 negative modes at the minimum).
- The mass-weighted Hessian comes from central differences of forces.

**Method.**
- Take the Langevin drift about the minimum, drop the noise (the most favourable case) and truncate at quadratic order.
- R = ‖u_in‖·‖F2‖/|Re λ₁| is evaluated in the F1-diagonalising coordinates, which is Liu's normal setting.
- ‖F2‖ is **lower-bounded** from directional third derivatives T[v,v] over 40 directions (10 soft modes, 10 stiff
  modes, 20 random). So every R below is a lower bound.
- ‖u_in‖ is the thermal RMS amplitude at 300 K.

| Friction γ (ps⁻¹) | Re λ₁ (ps⁻¹) | Overdamped modes | ‖u‖·‖F2‖ (ps⁻¹) | R lower bound, thermal | R lower bound, softest mode at kT |
|---|---|---|---|---|---|
| 0 (Newtonian / explicit-solvent NVE) | 0 | — | — | **∞** | ∞ |
| 1 | −0.50 | 0 | 2.1×10³ | **4.3×10³** | 2.0×10³ |
| 5 | −0.35 | 4 | 3.4×10³ | **9.7×10³** | 3.1×10³ |
| 50 | −0.032 | 87 | 2.4×10³ | **7.4×10⁴** | 3.0×10⁴ |
| 91 (water-like) | −0.018 | 132 | 2.2×10³ | **1.2×10⁵** | 5.3×10⁴ |

- **R < 1 is missed by 3.3–5 orders of magnitude**, and R < √2 (Liu's intractability line) likewise.
- The nonlinearity is dominated by stiff directions: ‖T[v,v]‖ is 2.8×10⁵ for stiff modes, 1.4×10⁵ for random
  directions and 1.2×10⁴ for soft modes.
- Friction cannot help. It raises the damping of stiff modes but lowers the slowest rate to ω_min²/γ.
- **R grows with system size [DERIVED].** The thermal ‖u_in‖ grows as √(d·kT) while ‖F2‖ is intensive, so R ∝ √d.
  Protein G (d = 2,565) and ubiquitin (d = 3,693) would be about 1.7–2× larger.
- **Off the minimum, F1 is not Hurwitz.** Along a 1 ps, 300 K Langevin trajectory, 8 of 10 snapshots have 1–2
  negative-curvature directions in the 60 softest modes (ω² down to −410 ps⁻²). So even Jennings-style
  stable-system Carleman has no fixed point that governs thermal dynamics [MEASURED].
- **The system is strongly resonant [DERIVED from MEASURED].** The nonlinearity rate is about 2×10³ ps⁻¹, against a
  median mode spacing of 0.29 ps⁻¹. That puts it deep in the resonance-overlap regime, which excludes the non-resonant
  extensions.
- **Lyapunov exponent (S5, NVE Verlet 0.5 fs, flexible GBn2).**
  - λ_max ≈ **2.1 ps⁻¹** in double precision (Reference, ε = 10⁻⁸ nm; local slopes 1.1–5.8 ps⁻¹).
  - λ_max ≈ **3.2 ps⁻¹** in single precision (CPU, ε = 10⁻⁵ nm).
  - Literature cross-check: explicit-solvent perturbations of 10⁻³–10⁻⁹ Å reach about 1 Å RMSD within 1–2 ps
    (Braxenthaler et al. 1997, PMID 9408939, abstract verified), which implies about 3–20 ps⁻¹ [DERIVED].
  - Together with Lewis et al. 2024, this rules out every trajectory-state (Carleman/KvN state-output) route over
    µs–ms horizons.

---

## (2) The strongest classical twin (LITERATURE-SUPPORTED; `lit/pubmed_twin.py`, `lit/pubmed_records.json`, `lit/pmc/`)

Step sizes (2 fs implicit, 2.5 fs explicit) are INFERENCE throughout.

| Folder / task | Classical method and verified cost | Effective MD steps B_c |
|---|---|---|
| Trp-cage (20 aa), one folding event | Folding time ≈ 4.1 µs (Voelz 2010, PMC2835335 intro, citing earlier work) | 1.6×10⁹ |
| Trp-cage, full folding free-energy surface | Bias-exchange metadynamics, "only 40 ns of simulation on 8 replicas" (Piana & Laio 2007, PMID 17419610) | **1.6×10⁸** |
| Villin (~10 µs) / Fip35 WW (~13 µs) | Plain MD (Voelz 2010 text); 12 fast folders "over periods ranging between 100 µs and 1 ms … spontaneously and repeatedly fold" (Lindorff-Larsen 2011, PMID 22034434) | 4×10⁹ per event |
| NTL9(1–39), water-like friction (GB, γ = 80 ps⁻¹) | Weighted ensemble: τ_f = 0.2–2 ms from **252 µs aggregate**, 30 runs × 20 days on 1 GPU each (Adhikari 2019, Table 1, PMC6660137) | **1.3×10¹¹** |
| Protein G B1 (GB, low friction) | Weighted ensemble: τ_f = 3–200 ms from **225 µs aggregate**; "significantly less overall computing than … a single folding event" (same source) | **1.1×10¹¹** |
| Protein G / WW (explicit, distributed) | "~500 µs to estimate a ~65 µs room-temperature folding time" (Ensign & Pande, as cited in Adhikari 2019) | 2×10¹¹ |
| Ubiquitin (76 aa, ms folder) | Equilibrium atomistic folding on Anton (Piana 2013, PMID 23503848; aggregate not verified) | ≥ 4×10¹¹ per event |
| λ6-85 (80 aa, explicit) | MSM from 3,265 trajectories, "aggregate of 1.3 milliseconds", 10 ms-timescale model (Bowman 2011, PMC3043158) | **5.2×10¹¹** |
| Ensembles by REMD | Useful only with a positive activation enthalpy; can be less efficient than MD if T_max is too high (Nymeyer 2008, PMID 26620937). Efficiency = ratio of transitions (Rosta & Hummer 2009, PMID 19894977). CspA was unconverged after about 30 µs of REMD (Nguyen 2014, PMC4195377) | 1×–10× over MD |
| Ensembles by AI emulator | BioEmu: "thousands of statistically independent structures per hour on a single GPU", about 1 kcal/mol against ms MD (Lewis 2025, PMID 40638710) | ≈ 1 GPU-s per sample, i.e. 3–11×10³ step-equivalents |
| GPU throughput, implicit solvent | "~1 µs/day per GPU", 0.6–1.4 µs/day for 17 proteins (Nguyen 2014) | c ≈ 1.7×10⁻⁴ s/step |

**MEASURED on this machine** (`work/S1_*.json`, `work/S2_*.json`: one loaded core, OpenMM 8.5.2 CPU, 2 fs, HBonds):

| Protein | Atoms (protein) | GB all pairs | Explicit box atoms (1 nm pad, TIP3P) | Pairs < 1 nm | GB s/step | PME s/step |
|---|---|---|---|---|---|---|
| Trp-cage 1L2Y | 304 | 4.6×10⁴ | 4,826 | 9.3×10⁵ (192/atom) | 0.015 | 0.019 |
| Protein G 1PGA | 855 | 3.7×10⁵ | 10,918 | 2.1×10⁶ (195/atom) | 0.130 | 0.041 |
| Ubiquitin 1UBQ | 1,231 | 7.6×10⁵ | 17,236 | 3.4×10⁶ (198/atom) | 0.275 | 0.075 |

---

## (3) Floor and break-even (`floor_allatom.py` → `floor_allatom.json`, `floor_allatom_table.md`)

### Oracle model: G = 2 × n_terms × τ, compute plus uncompute (DERIVED from stated assumptions; not compiled)

**Terms per coherent force evaluation.**
- **Explicit solvent.** n_terms = measured pairs within 1 nm × f_nl.
  - f_nl = 1 (generous): a free neighbour list.
  - f_nl = 4 × 1.2 (central): a padded coherent cell list, plus PME. A configuration-dependent neighbour list is not
    available coherently for free (T3 §3.1).
- **GBn2.** n_terms = all pairs × 2 passes (generous) or 3 passes (central).

**Toffolis per pair term, τ.**
- Generous: 6×10³ (20-bit, b²/2 multiplies).
- Central: 1.6×10⁴ (23-bit, T3 primitives: sqdist 1,760, inverse square root, about 16 multiplies for LJ 12-6,
  Coulomb/erfc and force components).
- This is consistent with T3's 7–9×10³ Toffolis per learned-energy pair term.

**Resulting G (generous).**

| System | G generous (Toffolis) |
|---|---|
| Trp-cage, GB | 1.1×10⁹ |
| NTL9, GB | 4.4×10⁹ |
| Protein G, GB | 8.8×10⁹ |
| Protein G, explicit | 2.6×10¹⁰ |
| Ubiquitin, explicit | 4.1×10¹⁰ |

**Other inputs.**
- c for one GPU: implicit 1.7×10⁻⁴ s (Nguyen 2014); explicit = CPU-core time / 200 (INFERENCE).
- Overheads MO: K = 10, n_b = 1, A = ρ = 1.

**Floor, MO overheads, generous G, one GPU.**

| Folder | T\*_Q,2 at 10 ns | T\*_Q,3 at 10 ns | T\*_Q,4 at 10 ns | T\*_Q,exp at 10 ns | T\*_Q,2 at 1 µs | T\*_Q,4 at 1 µs |
|---|---|---|---|---|---|---|
| Trp-cage, GB | **2.2 yr** (B\* 4.1e11) | 1.0 d | 2.6 h | 110 s | 2.2×10⁴ yr | 51 d |
| Trp-cage, explicit | 420 yr | 44 d | 2.9 d | 18 min | 4.2×10⁶ yr | 3.7 yr |
| Villin / WW, explicit | 690 yr | 73 d | 4.9 d | 31 min | 6.9×10⁶ yr | 6.2 yr |
| NTL9, GB | 35 yr | 8 d | 17 h | 7 min | 3.5×10⁵ yr | 320 d |
| Protein G, GB | 140 yr | 23 d | 1.7 d | 15 min | 1.4×10⁶ yr | 2.2 yr |
| Protein G, explicit | 990 yr | 100 d | 6.8 d | 43 min | 9.9×10⁶ yr | 8.7 yr |
| Ubiquitin, explicit | 1,400 yr | 160 d | 10 d | 1.1 h | 1.4×10⁷ yr | 13 yr |
| λ6-85, explicit | 1,400 yr | 150 d | 10 d | 1.1 h | 1.4×10⁷ yr | 13 yr |

**Against the literature twin (1 GPU, MO, generous G).**

| Folder and twin | T_c | T_Q at s = 2, 10 ns | T_Q at s = 3, 10 ns | T_Q at s = 4, 10 ns | T_Q at s = 4, 1 µs |
|---|---|---|---|---|---|
| Trp-cage, metadynamics FES (1.6e8) | 4.1 h | 160 d (loses) | 7 d (loses) | 1.4 d (loses) | 140 d (loses) |
| NTL9, WE (1.3e11) | 250 d | 4.9 yr (loses) | 25 d (wins) | 3 d (wins) | 300 d (loses) |
| Protein G GB, WE (1.1e11) | 220 d | 9.3 yr (loses) | 49 d (wins) | 5.9 d (wins) | 1.6 yr (loses) |
| λ6-85, MSM (5.2e11) | 5.8 yr | 89 yr (loses) | 360 d (wins) | 38 d (wins) | 11 yr (loses) |

**Reading.**
1. **s = 2 is dead in this regime at every t_T ≥ 10 ns against one GPU.** B\*_2 ≥ 4×10¹¹ steps, which exceeds every
   twin cost of 1.6×10⁸–5×10¹¹ in the table.
2. **The only case below 1 month at s = 2 uses an invalid twin.** One loaded CPU core as the comparator gives
   T\*_Q,2 = 9.5 d (Trp-cage, GB) and 35 d (NTL9, GB) at 10 ns. A single loaded core is about 10²–10³× slower than
   one GPU, so it is not the strongest classical twin (`floor_allatom_table.md`, sensitivity rows).
3. **Central assumptions make it much worse.** For s = 2, T\* ∝ G²·(K n_b)²/c:
   - central G raises the floors 16–160×;
   - CE overheads (K = 100, n_b = 2) add a further 400×;
   - an Anton-class comparator (c = 2 µs, UNVERIFIED) adds about 50×.
4. **Hypothetical s ≥ 3 would be useful at 10 ns.** Even at central G, s = 4 at 10 ns stays at 17 h to 1 yr (MO).
   The regime is not resource-dead for a hypothetical s ≥ 3 algorithm, and the kill rests on the precondition arm.
5. **Ensembles already have a cheaper twin.** Against the AI-emulator twin (BioEmu, about 1 GPU-s per independent
   sample), even an idealised exponential algorithm needs K·G·t_T = 110 s to 1.1 h per sample at t_T = 10 ns.
   Quantum loses by 10²–4×10³× per sample, unless force-field-exact sampling beyond about 1 kcal/mol is itself the
   target [DERIVED + INFERENCE].
6. **The rate-estimation route is far slower than WE [DERIVED, order of magnitude].** Take the Kharazi route for the
   NTL9 rate, with k ≈ 10³ s⁻¹ and t = 10 ns (beyond the verified 4–5 ns event durations).
   - Additive ε ≈ 0.1·k·t ≈ 10⁻⁶ is needed.
   - With √(t‖H‖), ‖H‖ ≈ ω_max²/γ ≈ 5×10³ ps⁻¹ (MEASURED ω_max, γ = 91 ps⁻¹), that is about 7×10⁹ coherent force
     evaluations.
   - At G = 4.4×10⁹ and t_T = 10 ns, this takes about 10⁴ years. WE takes 250 GPU-days.
   - The additive-error estimator pays the rare-event factor 1/(kt), which classical path sampling avoids.

---

## Claim levels

- **Claim category (charter).** The claim tested would be category 3 (computational/resource advantage) or category 4
  (sampling advantage) for force-field folding kinetics and ensembles. It is not established.
- **Theoretical.**
  - s = 2: L2 (same-chain walk / Witten-Laplacian speedup, generic), and L3 with the oracle costed here (DERIVED G).
  - s ≥ 3 for protein force fields: **L0**, since no family applies. The parent separations are L1 (query or
    BQP-completeness) only on their own families: 2ⁿ oscillators, worst-case Lipschitz bounds, hide-and-seek tori,
    dissipative quadratic ODEs.
- **Practical: L0.** No configuration with a valid classical twin meets either time rule at s = 2. The configurations
  that would meet it need an algorithm that does not exist for this input class.

## What would reopen this (all three needed)

1. **An algorithm with s ≥ 3 against practical MD, or against weighted ensemble / MSM for kinetics.** Not against
   worst-case weak-error bounds, grid PDE solvers or a chain's own mixing time. It must be for smooth pairwise force
   fields under Langevin or Newtonian dynamics, with preconditions that allow:
   - multi-basin, non-convex landscapes (negative curvature off the minimum);
   - positive Lyapunov exponents of about 2–20 ps⁻¹;
   - non-polynomial forces;
   - observables on O(L) coordinates.
2. **Logical Toffoli time.** t_T ≤ 10 ns for s = 3, or t_T ≤ 100 ns to 1 µs for s = 4. See the tables: T\*_Q,4 at
   100 ns is 2.4–230 d.
3. **A folding observable, with an explicit value criterion.** A kinetics or ensemble observable whose required
   precision the WE/MSM/metadynamics/emulator twins cannot reach at ≤ 10¹¹–10¹² steps, and where force-field error
   (1–2 kcal/mol; Piana 2011, PMID 21539772: mechanisms depend on the force field) does not dominate the answer.

## Suggested state-file updates (not made; this lane writes only inside its folder)

- **KILLBOOK K-117 (proposed).** "Super-quadratic quantum sampling or dynamics of classical all-atom force fields
  (Carleman / KvN / Fokker–Planck / SDE / oscillator / Gibbs / rate families) for folding kinetics or ensembles."
  - Kill type: precondition failure (MEASURED R ≥ 4×10³, λ_max ≈ 2–3 ps⁻¹, negative curvature) plus literature
    (s ≤ 2 against the practical twin).
  - s = 2 resource floor: T\*_Q,2 ≥ 2.2 yr at 10 ns.
  - What did not disappear: nothing. WE/MSM/metadynamics/BioEmu supply the capability.
  - Reopen: the three conditions above.
- **`theory/BREAK_EVEN.md` (CRITIC A-5).** Add a "physics force field" row with the table above, replacing D1's G.
- **SYNTHESIS O-1, clause (3).** Replace it with: "classically hard and structure-bearing; the known families are
  quadratic against practical MD, with a floor ≥ 2 yr at 10 ns; the super-quadratic families' preconditions fail
  (R ≥ 10³, chaos); a hypothetical s ≥ 3 algorithm would already be useful at t_T ≤ 10 ns".

## Resource accounting

- **Compute.** Single-threaded throughout (`OMP_NUM_THREADS=1`; OpenMM CPU platform with Threads = 1, or Reference).
  About 31 CPU-min in total:
  - S1 + S2: 7.5 min;
  - S3 + S4: 4.3 min;
  - S5 single precision: about 5 min, plus about 6 min of an aborted protein-G S5 run. It was stopped during an
    un-checkpointed equilibration and produced no files;
  - S5 double precision: 7.6 min;
  - floor and survey scripts: under 1 s.
- **Memory and network.** Peak RAM under 1 GB. About 35 HTTP requests to arXiv, NCBI and PMC.
- **Quantum resources.** None simulated. All quantum costs are DERIVED; simulator runtime is not involved.
- **Checkpointing.** S3 saves its partial Hessian every 60 s (kept as `*.done.npy`). S5 saves both trajectories every
  60 s. The survey and PubMed fetches are checkpointed per query.

## Files

- **Measurement.** `allatom_measure.py`: S1 sizes, S2 timing, S3 Hessian, S4 Carleman R and curvature census,
  S5 Lyapunov. Outputs in `work/`:
  - `S1_*.json`, `S2_*.json`
  - `S3_1L2Y*.json/npy`
  - `S4_1L2Y.json`
  - `S5_1L2Y_{CPU_eps1e-05,Reference_eps1e-08}.json` with checkpoints
- **Floor.** `floor_allatom.py` → `floor_allatom.json`, `floor_allatom_table.md`. Includes the full sensitivity
  sweep: G level, CPU / GPU / Anton comparators, MO / CE overheads, t_T = 1 µs / 100 ns / 10 ns.
- **Survey table.** `families.py` → `families.json`: 12 families, 53 verified ids with titles and journal refs.
- **Literature.**
  - `lit/arxiv_survey.py` → `lit/raw/*.json`, `lit/records.json`, `lit/queries.json`
  - `lit/pubmed_twin.py` → `lit/pubmed_raw/*.json`, `lit/pubmed_records.json`
  - `lit/pmc/PMC*.xml`: full texts for Adhikari 2019, Nguyen 2014, Voelz 2010 and Bowman 2011
