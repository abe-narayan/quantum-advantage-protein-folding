# ROUND3 lane: structured beyond-quadratic speedups for classical objectives

_2026-09-28. Lane `structured_speedups`. All artefacts are in this folder. No file outside it was modified, nothing was committed, and the governor jobs were not touched._

**Question.** Is there a known quantum algorithm family with a **super-quadratic** (ideally exponential) speedup for optimisation, sampling or counting over a *classical* objective whose structural precondition is met by a real protein-structure task? The task tested here is the production A80 learned energy on the ladder crops, or a discretisation of it. K-101 already prices out every quadratic route: T*_Q ≥ 0.26 yr per sample. So only a beyond-quadratic family, or one with a far cheaper oracle, could matter.

**Verdict: KILLS.** No family's precondition is met.

For every family surveyed (2022–2026, arXiv API), the structural precondition was stated and then tested against the A80 task, numerically wherever a test was possible. Each one fails on the protein task, and it fails on the structure itself, before any question of cost arises:
- **DQI.** The code structure is absent, or the dual distance is 3.
- **Kikuchi.** The level-1 method already succeeds, and the objective is pairwise in Cartesian coordinates.
- **Glued trees / GHV / LWWZ.** There is no column structure.
- **Short-path, jump-to-the-end and key guessing.** The quantum exponent is at least 12× the measured classical exponent.
- **RsAA / QHD separations.** The objective is not block-separable and not near-convex.
- **Gibbs-advantage constructions.** They need non-diagonal Hamiltonians.

Theoretical level for the protein task: **L0**. Practical level: **L0**.

Tags: MEASURED (this lane, files below), DERIVED (argument given here), LITERATURE (abstract verified this session through the arXiv API; `lit/abstracts.txt` holds the verbatim abstracts), INFERENCE, UNPROVEN.

---

## 1. Family-by-family: precondition → test → result

| # | Family (verified refs) | Structural precondition (precise) | Test on the A80 task | Result |
|---|---|---|---|---|
| 1 | **DQI**: Jordan et al. 2408.08292 (Nature 2025). Follow-ups: 2510.06603 (Hermitian codes), 2605.10666 (weighted/multivariate), 2510.10967 (OPI circuits, 5.72 M Toffoli), 2411.12553 (soft decoders), 2510.08061 (max-QUADSAT; the authors flag an invalidating error). Critiques: 2509.19966 (MaxCut), 2509.14509 (OGP), 2603.04540, 2606.13570 (inapproximability), 2607.28120 (MCMC matches DQI), 2509.14443 | The objective must be f(x) = Σ_i f_i(b_i·x) over F_q (max-LINSAT). The dual code C⊥ = ker Bᵀ must be decodable to ℓ errors with ℓ/m = Θ(1). Thm 4.1 needs 2ℓ+1 < d⊥ (verified in the paper HTML). The instance must also not be classically easy at that approximation ratio. Advantage is known only for algebraic codes (Reed–Solomon, Hermitian). Sparse/LDPC instances are contested. | **S1, torsion encoding:** Fourier line spectrum of pair terms and of energy windows over Z_p^s. **S3, Cartesian lattice encoding:** there the pair terms *are* exactly max-LINSAT over F_{P³}, with B = graph incidence matrix and C⊥ = cycle space, so d⊥ = girth. | **FAILS.** Torsion encoding: not max-LINSAT. Cartesian: d⊥ = 3 everywhere, so Thm 4.1 gives ℓ = 0 and DQI returns the random-assignment value. Even an unbounded decoder reaches ℓ₅₀ = 3–8 of m = 407–11,027. On the full A80 pair graph, DQI satisfies ≤ 0.09–0.23 of constraints, against 0.78–1.00 for the classical level-1 structure (§2.1–2.2) [MEASURED + DERIVED] |
| 2 | **HDQI** (2510.07913) | Gibbs states or spectral filters of a Pauli Hamiltonian via decoding of the code defined by H's Pauli supports. The pilot state is efficient only for commuting H. The same paper gives matching classical algorithms for physically motivated commuting cases. | For diagonal H (a classical energy), the code is the Walsh-support code of E. S1/S2 show that E is Fourier-dense: mean interaction order 1.8–8.6, and 24–60% of all lines are needed in 5-torsion windows. | **FAILS** at the same decodability step as DQI [INFERENCE from S1/S2 + LITERATURE] |
| 3 | **Short path / jump-to-the-end**: Hastings 1802.10124; Dalzell–Pancotti–Campbell–Brandão 2212.01513. **Generalised short path**: Chakrabarti et al. 2410.23270 | Binary (discrete) cost with a condition on low-energy density. Runtime O*(2^{(0.5−c)n}) with a small n-independent c. It is super-quadratic over Grover, or over *stationary-distribution search*, but never over the best classical method for the problem. | **S6:** per-residue exponent compared with the measured best classical exponent α_c. | **FAILS.** α_c = 0.029 nats/residue (census cost per best-mode hit, 1.7×10³ → 5.5×10⁴ grad evals for L = 30 → 150). Quantum ≥ (0.5−c)·ln K per residue: 0.35 at K = 2, which is 12× α_c. Parity would need c ≥ 0.457 (K = 2) or c ≥ 0.495 (K = 216 head cells) [MEASURED + DERIVED] |
| 4 | **Super-quadratic key guessing**: Montanaro's algorithm, tight analysis Glaser–May–Nowakowski 2509.06549 | The target must be drawn from a known non-uniform prior D, with a membership check. The classical baseline is enumeration by likelihood, 2^{H_{1/2}(D)}. The quantum cost is 2^{H_{2/3}(D)/2}. | **S6:** Rényi entropies of the per-residue (θ,τ) head prior. | **FAILS.** The speedup factor is genuinely super-quadratic (2.06–2.38). But the quantum exponent is H_{2/3}/2 = 1.38–2.32 nats/residue, which is 47× α_c. Relaxation from prior samples is exponentially better than enumeration by likelihood, and the native is not drawn from D [MEASURED + DERIVED] |
| 5 | **Kikuchi / planted inference**: Schmidhuber–O'Donnell–Kothari–Babbush 2406.19378 (PRX 2025); Schmidhuber–Hastings 2607.29672 (sharp hierarchy); Schmidhuber–Zlokapa 2510.08494 (community detection); Kothari–Xu 2510.03061; Gupta–He–O'Donnell–Singer 2508.09422 (classical quadratic speedup, so the quartic speedup becomes quadratic for large k); Fontana et al. 2510.07273 (900 logical qubits, ~10¹⁵ gates vs ~10²³ FLOPs) | A planted signal on **random k ≥ 3-uniform** hyperedges (kXOR / order-k tensor), with SNR inside the window where level-1 spectral fails but level ℓ succeeds (m ≈ ρ⁻² n^{k/2}/ℓ^{k/2−1}), plus an efficiently preparable guiding state. | **S4:** does a *level-1* (pairwise spectral / stress) method already extract the planted structure? **S2:** interaction order of E. | **FAILS.** Level-1 seeding (classical MDS or weighted SMACOF on distogram expected distances, then the census relaxer) reaches or beats the 256-restart census best energy in 14/16 crops at L = 150, 10/16 at L = 100, 5/16 at L = 60 and 0/16 at L = 30. It costs ~850 gradient evaluations against 55,000. ORACLE: its RMSD equals the census best-mode RMSD (median 5.4 vs 5.0 Å at L = 150). The task is information-limited, not in a statistical–computational gap. In Cartesian coordinates it is 2-body (k = 2, no Kikuchi window). In torsion coordinates the order is mixed (mean dimension 1.8–8.6), with geometric rather than random hyperedges [MEASURED + DERIVED] |
| 6 | **Guided local Hamiltonian**: Cade et al. 2207.10250, 2207.10097; Weggemans et al. 2302.11578. Dequantisations: 2409.04161, 2411.16163. Stoquastic case: Waite 2509.25829 (BPP-hard) | BQP-completeness needs *non-commuting quantum* local H at 1/poly precision. | For diagonal E, sample the (classically samplable) guiding state and evaluate E: cost 1/\|γ\|² classically, against ≥ 1/\|γ\| quantumly. | **At most quadratic** for any classical energy, so K-101 applies [DERIVED] |
| 7 | **Glued / welded trees, hierarchical graphs, GHV / LWWZ, guided stoquastic ground states**: Gilyén–Vazirani 2011.09495; Hastings 2005.03791; Balasubramanian–Li–Harrow 2307.15062; Li 2307.12492; Li–Zur 2311.07372; LWWZ 2504.14841; Hamoudi–Le Borgne–Sridhara 2602.23183; pathfinding lower bounds 2609.26712, 2609.20651 | Four things are needed: (i) black-box adjacency with **hidden random labels**; (ii) an equitable partition with exponentially large cells, so that the walk from ENTRANCE stays in a poly-dimensional Krylov space; (iii) exponential classical hitting time; (iv) an oracle cost that is ignored. | **S5:** discretised 6-torsion windows of DEP minima (L = 30, 6⁶ = 46,656 states, torus moves). Tests: 1-WL equitable partition, Krylov dimension of −A + γ diag(E), classical walks. | **FAILS.** Bare lattice: 84 cells, Krylov dimension 25. With the A80 energy: 46,656/46,656 singleton cells at every resolution (10⁻⁶ to 20 energy units), and Krylov dimension ≥ 1000 without terminating (γ = 0.1, 1). The energy destroys all column structure. The window is rugged for naive local walks (665–1157 discrete minima, steepest descent p_hit = 0.0075, Metropolis at T = 1 censored at 2×10⁵ steps), but exhaustive enumeration costs 4.7×10⁴ evaluations. So the only generic quantum gain left is Grover-type (≤ quadratic), which K-101 rules out [MEASURED] |
| 8 | **QHD / real-space adiabatic separations**: Leng–Zheng–Wu 2311.00811; Herman et al. 2510.03385 (RsAA); resource papers 2607.16996, 2605.12066 | The separating families are **block-separable** (d-dim instances with 2^d minima) or **perturbed strongly convex**. The separation is against off-the-shelf solvers. Structure-aware classical algorithms stay polynomial. | **S2/S2b:** additive (block-separable) share and interaction order. Census: number of modes. | **FAILS.** Held-out additive R² is 0.04–0.26 (L = 30, 60; any measure), and adding nearest-neighbour terms gives only 0.04–0.33. Mean dimension is 1.8–3.2 locally and 2.8–8.6 under the prior. The census finds 14–2043 modes per crop, so the energy is neither separable nor near-convex [MEASURED] |
| 9 | **Gibbs sampling with provable super-polynomial advantage**: Bergamaschi–Chen–Liu 2404.14639 (FOCS 2024); Rajakumar–Watson 2408.01516 | Commuting **quantum** parent Hamiltonians of shallow IQP-type circuits. Hardness comes from sampling measurement outcomes of non-diagonal Gibbs states. | For a classical (diagonal) E, the computational-basis Gibbs distribution *is* the Boltzmann distribution. No IQP structure exists. | **Not applicable** [DERIVED] |
| 10 | **Quantum-enhanced MCMC**: Layden et al. 2203.12497 (Nature 2023). Bounds: Orfi–Sels 2403.03087, 2408.07881. Later work: 2603.28076, 2602.06171 | Heuristic. There is no provable super-quadratic gap gain. The gap is ≤ the inverse participation ratio of classical states in the quench eigenbasis, there is no speedup in the unstructured worst case, and fine-tuned quenches are needed. | Cost check with T3: each proposal needs ≥ 1 coherent A80 phase oracle, G(L) ≈ 3×10⁴ L² Toffolis (≈ 3×10⁸ at L = 100, ≈ 300 s at 1 µs). A classical step costs c ≈ 1–2 ms. | Break-even needs a gap gain of ≥ ~10⁵ × (Trotter steps) per step, with no evidence of such gains [DERIVED from T3 + LITERATURE] |
| 11 | **Non-stoquastic XX-driver MIS**: Choi 2601.17686, 2509.16263 | Specific structured MIS instances (cliques of degenerate critical local minima). The claim holds "under assumptions supported by analytical and numerical evidence". | The A80 backbone task is not an MIS. Rotamer packing is an MWIS but is outside A80. | **Not applicable to A80**. The source claim is itself UNPROVEN |
| 12 | Local minima of quantum systems (Chen–Huang–Preskill–Zhou 2309.16596); Yamakawa–Zhandry 2204.02063 | A quantum Hamiltonian (local minima of classical H are classically easy); a random oracle. | The A80 energy is an explicit classical function. | **Not applicable** [DERIVED + LITERATURE] |

Framing: Aaronson 2209.06930 ("law of conservation of weirdness") [LITERATURE]. Every family above concentrates amplitude by exploiting an unusual structure: an algebraic code, a random planted hypergraph, hidden labels plus a column symmetry, separability, or non-diagonal Hamiltonians. The A80 task has none of these.

---

## 2. Key numerical results

### 2.1 DQI in its most favourable exact encoding (S3: `s3_dqi_graph_code.py` → `s3_dqi_graph_code.json`)

**Encoding [DERIVED].** Place residues on Z_P³, which is additively isomorphic to F_{P³}. Every pair term is then f_ij(x_i − x_j), so the pair objective *is* max-LINSAT with B equal to the signed incidence matrix. Its dual code is the cycle space, and d⊥ = girth. For generic error values, beyond half the distance, any decoder, even an unbounded one, can recover a weight-ℓ error only if its support is a forest that is also a flat of the graphic matroid. P_dec(ℓ) is Monte-Carlo'd with 300 trials per ℓ.

**Constraint semantics.** A pair is satisfied when d_ij lies inside its distogram 68% credible interval. ρ is the shell volume divided by the box volume. All inputs are DEP (distogram only).

| L | graph | m (median) | girth | Thm 4.1 ℓ | ℓ₉₀ / ℓ₅₀ (median) | DQI frac. at ℓ₅₀ (median; max) | classical level-1 (median; min) | ℓ needed / ℓ₅₀ |
|---|---|---|---|---|---|---|---|---|
| 30 | full A80 pairs + bonds | 407 | 3 (16/16) | 0 | 1 / 3 | 0.19; 0.23 | 0.98; 0.96 | 106× |
| 60 | full | 1712 | 3 | 0 | 2 / 4 | 0.14; 0.21 | 0.96; 0.90 | 282× |
| 100 | full | 4852 | 3 | 0 | 2 / 6 | 0.11; 0.15 | 0.92; 0.83 | 555× |
| 150 | full | 11,027 | 3 | 0 | 3 / 7 | 0.09; 0.11 | 0.83; 0.78 | 925× |
| 150 | contacts (p ≥ 0.5) + bonds | 453 | 3 | 0 | 5 / 12 | 0.045; 0.052 | 0.79; 0.72 | 28× |
| 150 | contacts only (sparsest) | 304 | 3 | 0 | 7 / 17 | 0.09; 0.11 | 0.68; 0.56 | 11× |
| 150 | Erdős–Rényi null, same n, m | 453 | 3 | 0 | 12.5 / 30 | 0.27; 0.31 | 0.84 | 9× |

- **In none of the 300 cyclic crop × graph instances does DQI's generous ℓ₅₀ bound reach the classical fraction** [MEASURED].
- The 18 acyclic (forest) instances occur only for tiny sparse variants at L ≤ 60 (2 further instances are empty). There DQI decodes everything, but the classical structure also satisfies 100%. This matches Parekh 2509.19966: DQI is non-trivial only on classically easy graph instances [MEASURED + LITERATURE].
- Protein constraint graphs are *worse* DQI instances than random graphs of equal density: ℓ₅₀ is 1.6–2.5× smaller (L = 30 → 150), because of triangle clustering. At L = 150 the full graph has a median of 5.3×10⁵ triangles [MEASURED].
- **Caveats.** The semicircle law is applied with the mean ρ̄, which is INFERENCE for heterogeneous ρ. Dropping the angle and head terms and the non-pair structure only helps DQI. The classical structure is a valid chain, so it gives a *lower* bound on the classical optimum of the lattice objective.

### 2.2 Torsion encoding is not max-LINSAT (S1: `s1_torsion_lines.py` → `s1_torsion_lines.json`)

**Method.** Torsions are discretised to Z_p, and everything else is fixed at the DEP level-1 minimum. A max-LINSAT term puts 100% of its Fourier variance on one line. Restricting variables can only merge lines, so the counts below are lower bounds on the number of constraints any exact DQI encoding would need [DERIVED].

| object | s (τ's) | p | best-line share (median) | lines for 90% / 99% (median) | total lines |
|---|---|---|---|---|---|
| single pair term | 3 | 23 | 0.80 (axis-dominated) | 5 / 38 | 553 |
| single pair term | 4 | 13 | 0.35 | 8 / 104 | 2380 |
| single pair term | 5 | 7 | 0.21 | 26 / 197 | 2801 |
| energy window | 4 | 13 | 0.12 | 88 / 205–897 | 2380 |
| energy window | 5 | 7 | 0.11 | 233 / 661–1682 (median 51% of all lines) | 2801 |

- Pair terms spanning ≥ 6 torsions (36 of the sampled terms) were too large for exact FFT. Their share on a single line can only be smaller [INFERENCE].
- **Conclusion.** A80 in torsion coordinates is Fourier-dense, so a DQI rewrite would need a dense, highly dependent B [MEASURED].

### 2.3 Level-1 already succeeds: no planted-inference gap (S4: `s4_planted_level1.py` → `s4_planted_level1.json`, `s4_coords.npz`)

**Method.** 4 seeds (MDS, weighted SMACOF and their mirror images, from distogram expected distances only), then the census relaxer (200-iteration L-BFGS). They are compared by **energy** with the pre-registered G1 256-restart census.

| L | level-1 ≤ census best + 1 | beats census by > 1 | ΔE median (range) | grad evals: level-1 / census | ORACLE RMSD: level-1 / census best mode (median, Å) |
|---|---|---|---|---|---|
| 30 | 0/16 | 0/16 | +26 (+1.3 … +168) | 728 / 47,323 | 7.0 / 6.8 |
| 60 | 5/16 | 5/16 | +46 (−61 … +435) | 812 / 52,238 | 7.6 / 7.0 |
| 100 | 10/16 | 10/16 | −128 (−330 … +689) | 816 / 55,379 | 5.0 / 4.9 |
| 150 | 14/16 | 14/16 | −926 (−1366 … +1085) | 848 / 55,318 | 5.4 / 5.0 |

- This independently replicates, native-free, the exploratory DG-seeding claim of H-007/QM-02 at L = 100–150. That claim is "reaches the deepest known basin"; here the level-1 seed beats the census best energy in 24/32 crops at ~1.5% of the census cost. At L ≤ 60 the census is better [MEASURED].
- **Caveat.** Criterion is energy only. The census stores no coordinates, so "same basin" is not checked by RMSD.
- The Gram spectrum of expected distances is *not* cleanly rank-3 (λ₃/λ₄ median 1.5–2.0), yet level-1 recovery still works [MEASURED].

### 2.4 Interaction order and separability (S2/S2b)

**Mean dimension** (Σ Jansen total Sobol indices; grouped factors (θ_r, τ_r)), with bootstrap CIs in `s2_anova_arity.json`:

| measure | L = 30 | L = 60 | L = 100 |
|---|---|---|---|
| local ±10°/±3° | 2.0–2.7 | 2.1–2.6 | 1.8–2.4 |
| local ±30°/±10° | 2.4–2.6 | 2.6–3.2 | 2.6–3.2 |
| restart prior | 2.8–4.2 | 4.2–5.5 | 4.8–8.6 |

- The first-order Sobol estimator is too noisy (heavy clash tails) and is not used [MEASURED].
- **Additive surrogate** (held-out R², ridge chosen by validation, `s2b_additive_fit_v2.json`): R²_additive = 0.04–0.26 and R²_additive+nn = 0.04–0.33 [MEASURED].
- The v1 fit (`s2b_additive_fit.json`, fixed ridge) overfits at L ≥ 60 and is kept only for the record.

### 2.5 Exponents (S6: `s6_exponents.py` → `s6_exponents.json`)

- **Classical [MEASURED]:**
  - census gmean p_hit is 0.101, 0.070, 0.047, 0.041, 0.016, 0.0077 and 0.0039 at L = 30, 45, 60, 80, 100, 120 and 150; the L = 150 value is censored at 1/256;
  - cost per hit is 1.7×10³ → 5.5×10⁴ gradient evaluations;
  - fit: α_c = 0.0295 nats/residue.
  - S4 shows that at L ≥ 100 a level-1 seed with no exponent at all beats this. α_c is therefore an *upper* bound on the classical difficulty of reaching the best known basin, not of certifying the global minimum.
- **Quantum [DERIVED from MEASURED entropies]:**
  - jump-to-the-end ≥ 0.35 nats/residue (K = 2), 1.59 (K = 24) and 2.69 (K = 216), all at c = 0;
  - key guessing: H_{2/3}/2 = 1.38–2.32;
  - stationary-distribution search ≥ ½(−ln π(x* cell))/n = 1.5–5.0.
- **Ratio to α_c:** ≥ 12 (jump, K = 2), 47 (guessing), 51 (stationary search).
- **Caveat [INFERENCE].** If the target were *certified* global optimisation, the classical exponent is unmeasured. Even so, a physically meaningful K ≥ 24 needs c > 0.5 − α/ln 24 = 0.5 − α/3.18 for parity against a classical exponent α (for example, c > 0.41 at α = 0.3).

---

## 3. What this adds beyond K-101 … K-105

1. **DQI is new.** It was never tested before; QM-17 only mentioned it. DQI's precondition is now tested in both natural encodings. The Cartesian result is a clean structural obstruction: d⊥ = girth = 3 in every A80 pair graph, so Theorem 4.1 gives ℓ = 0 [DERIVED + MEASURED].
2. **Kikuchi (QM-17) is re-attacked with new evidence.** Level-1 success is now measured on 64 crops, rather than only argued from arity [MEASURED].
3. **The glued-trees family (QM-09) gets a direct measurement on the A80 energy.** The equitable partition and Krylov dimension are measured, rather than on HP-lattice graphs [MEASURED].
4. **2025–2026 families are covered for the first time.** These are short-path generalisations, super-quadratic key guessing, RsAA, HDQI, constant-temperature Gibbs, Choi MIS, and guided stoquastic dequantisation barriers. Each fails its precondition on this task.
5. **One by-product for other lanes (not a quantum result).** Level-1 distogram seeding beats the 256-restart census at L ≥ 100 at ~1.5% of the cost. It is the strongest classical twin for any future learned-energy optimisation claim [MEASURED].

## 4. Resource ledger

| script | purpose | CPU (process) | peak RAM |
|---|---|---|---|
| s4_planted_level1.py | 64 crops × 4 seeds + relax | ≈ 3.5 min | < 0.5 GB |
| s3_dqi_graph_code.py | 64 crops × 5 graphs, P_dec Monte Carlo, 64 prior samples per crop | ≈ 2.5 min | < 0.5 GB |
| s1_torsion_lines.py | FFTs up to 23³ / 13⁴ / 7⁵ grids | ≈ 1.4 min | < 1 GB |
| s2_anova_arity.py | Sobol, 36 runs, ≈ 5×10⁵ energy evaluations | ≈ 4.6 min | < 0.5 GB |
| s2b_additive_fit.py (v1 + v2) | surrogate fits | ≈ 4.4 min | < 1 GB |
| s5_graph_krylov.py | 2 of 3 windows finished; the 3rd was not run (it was stopped at the tool timeout, and the checkpoint is intact) | ≈ 9.3 min | < 0.7 GB |
| s6_exponents.py, summarize.py | arithmetic | < 0.5 min | < 0.3 GB |

- **Totals:** ≈ 26–28 CPU-min, single-threaded (OMP/MKL/OPENBLAS = 1). No quantum hardware or simulator was used.
- **Leakage:** native coordinates are read only in functions and keys labelled ORACLE (RMSD and native satisfied-fraction diagnostics). No selection used them.
- **Literature:** `lit/*.xml` holds the raw arXiv API responses, `lit/abstracts.txt` the verbatim abstracts, and `lit/parse_arxiv.py` and `lit/dump_abs.py` are the parsers. WebSearch was not used. One arXiv HTML fetch verified the Thm 4.1 formula and the condition 2ℓ+1 < d⊥.

## 5. Reopen conditions

This lane is reopened only by a protein-structure task whose own objective (not a re-encoding chosen to fit) has one of the following:
- (a) **for DQI:** a constraint code with d⊥ ≫ 3 and a decoding radius ℓ/m = Θ(1), on instances that are not near-forests (DQI);
- (b) **for Kikuchi:** a genuine k ≥ 3-body planted signal on random hyperedges, where level-1 methods measurably fail but information is present;
- (c) **for glued trees / hierarchical graphs:** a black-box conformational graph with hidden labels and poly-dimensional Krylov structure from the start state;
- (d) **for short-path, jump-to-the-end, guessing and stationary search:** a quantum exponent below the best measured classical exponent for the same target.
