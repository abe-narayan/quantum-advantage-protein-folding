# R1 adversarial lens: theory of hardness for the NMR echo window

_2026-09-27. Lens: theory_hardness. Target: surviving lead R1 (protein ¹H dipolar echo, first-order OTOC F_ab(t)).
Every statement carries one tag: **MEASURED** (this folder, file cited), **DERIVED** (short derivation here),
**THEORETICAL** / **LITERATURE-SUPPORTED** (arXiv abstract verified through the arXiv API on 2026-09-27 unless marked
otherwise), **INFERENCE**, **UNPROVEN**. Compute used: about 25 single-threaded CPU-minutes, peak memory < 0.4 GB. Two
bounded foreground runs were moved to the background by the harness timeout; both finished, and no processes remain. No files outside this folder were modified._

## Verdict: WEAKENS (does not kill the dense-network branch; kills the amide-only branch up to 350 µs)

1. **The light-cone kill does not fire for the dense ¹H network.**
   - The σ-level light cone of Z_a(t) (σ = 0.01 per time point) is **N_σ ≈ 16–20 spins at 40 µs**. This is MEASURED with sparse Pauli dynamics on nested clusters up to N = 24, under a discarded-norm certificate.
   - Every physically motivated front law extrapolates it to **57–152 spins at 80 µs**, **≥ 146 at 160 µs** and **331–629 at 320 µs**; at 320 µs the whole protein is reached (INFERENCE).
   - Only an implausible empirical floor, in which the cone radius almost stops growing (N ∝ t^0.3), stays near 25 / 31 / 39 spins.
   - At the informative times (≥ 80 µs), exact simulation of the light cone therefore does **not** always suffice.
2. **The light-cone kill fires for the amide-only (perdeuterated) branch through 350 µs** (MEASURED, 1UBQ probe 19).
   - N_σ ≤ 12 up to 250 µs and N_σ ≈ 16 at 300–350 µs.
   - The amide-only echo "failure times" (250–500 µs) are failures of approximations inside a cone that exact classical methods can handle.
3. **There is no theory of hardness for this instance family** (THEORETICAL, UNPROVEN).
   - The only complexity anchor is worst-case DQC1-completeness of infinite-temperature OTOC estimation [2411.05208]. It concerns general instances, not geometric dipolar networks.
   - The published beyond-classical echo claim [F30] is for **OTOC(2)**. The same paper states that ordinary observables "become insensitive to the details of the underlying dynamics at long times due to the effects of scrambling".
   - For OTOC(1), the literature finds that "operator spreading is captured by an efficient classical model" [Mi 2021].
4. **The current R1 evidence is partly a finite-size artefact** (MEASURED, see §4).
   - The N = 10 "exact" reference, against which every classical failure time, f_hard and FI split was measured, is itself not converged in cluster size.
   - Adding two protons moves F_ab by more than σ from 20–40 µs onward: up to 0.46 at 80 µs over all sites, and 0.02–0.12 at the instrument's observed sites after 40–160 µs.
   - Going from N = 12 to N = 14 still moves the instrument's observed echoes by 0.03–0.19 across 40–320 µs (validated typicality run).
   - The late-window F plateaus shrink as N grows.

Net: R1 survives the "exact light cone is small" rebuttal on the dense network, but nothing positive about hardness was found, and the evidence base it rests on is weaker than stated. Theoretical level L0–L1; practical level L0.

---

## 1. What is known about the classical complexity of OTOC(1) and infinite-temperature correlators

All arXiv abstracts below were fetched through `export.arxiv.org/api/query` or `arxiv.org/abs` on 2026-09-27. "Abstract-level" means only the abstract was read.

| # | Result | Source | Applies to R1? |
|---|---|---|---|
| L1 | Normalised-trace estimation (infinite-temperature quantities) defines DQC1; "can perform interesting physics simulations" with no known efficient classical algorithm. | Knill & Laflamme, PRL 81, 5672 (1998), quant-ph/9802037 | THEORETICAL: sets the natural class for Tr[Z_a(t)Z_b Z_a(t)Z_b]/2^N. Not an instance statement. |
| L2 | Average fidelity decay ("testing the quantum butterfly effect") estimated with one clean qubit, "exponential speed-up". | Poulin, Blume-Kohout, Laflamme, PRL 92, 177906 (2004), quant-ph/0310038 | LITERATURE-SUPPORTED: echo-type (Loschmidt) quantities are DQC1-natural. No hardness proof for a physical family. |
| L3 | DQC1 cannot be classically simulated (multiplicative-error sampling) unless PH collapses to level 2 (level 3 in the earlier paper for DQC1_k, k≥3). | Fujii et al., PRL 120, 200502 (2018), 1409.6777; Morimae, Fujii, Fitzsimons, PRL 112, 130502 (2014), 1312.2496 | THEORETICAL: sampling hardness. **Additive-error estimation of one correlator (our task) is not covered.** Its hardness rests on DQC1 ⊄ BPP (a conjecture). |
| L4 | "Estimating OTOCs over all eigenstates … is complete for DQC1"; also N-time correlators. | Roy Moulik & Strelchuk, arXiv:2411.05208 (2024), abstract-level | THEORETICAL, worst-case. Hamiltonian class and accuracy regime not checked (abstract only). **No transfer to protein dipolar geometries** (UNPROVEN). |
| L5 | Heisenberg and XY interactions are "universal" Hamiltonians. | Cubitt, Montanaro, Piddock, PNAS 115, 9497 (2018), 1701.05182 | INFERENCE: dipolar XXZ families with *engineered* couplings are plausibly hard in the worst case. Protein couplings are fixed by geometry (d ∝ P₂(cos β)/r³), not engineered, so this gives no instance hardness (UNPROVEN). |
| L6 | Polynomial-time classical algorithms for noisy circuits: noise "exponentially damps non-local correlations"; also noisy RCS, arbitrary local noise, and beyond average case ("if noise is introduced at a faster rate than T gates, the simulation becomes classically easy"). | Schuster, Yin, Gao, Yao, PRX 15, 041018 (2025), 2407.12768 [F35]; Aharonov, Gao, Landau, Liu, Vazirani, STOC'23, 2211.03999; Angrisani, Mele, Rudolph, Cerezo, 2501.13101; González-García, Cirac, Trivedi, Quantum 9, 1730 (2025), 2407.16068 | INFERENCE: the physical echo includes decoherence and imperfect time reversal, so the forward model that must match data is a *noisy* dynamics. These results do not cover structured Hamiltonian dynamics, but they point toward easier, not harder. |
| L7 | Pauli propagation estimates observables of noiseless random circuits with small error "on all circuits except for a small fraction δ"; "chaotic" behaviour is "classically tractable". | Angrisani, Schmidhuber, Rudolph, Cerezo, PRL 135, 170602 (2025), 2409.01706 [F36] | THEORETICAL, average case over circuits. A fixed Trotterised dipolar Hamiltonian is not a random circuit. It refutes "chaotic ⇒ hard" as a general argument. |
| L8 | Sparse Pauli dynamics reproduced IBM's 127-qubit utility observables to < 0.01. | Begušić & Chan 2306.16372; Begušić, Gray & Chan, Sci. Adv. 10, eadk4321 (2024), 2308.05077 | LITERATURE-SUPPORTED. It is the adversary already implemented. Here it is exact for transfer and fails for echo at N = 10. |
| L9 | Dissipation-assisted operator evolution: damping non-local operators captures hydrodynamic transport. | Rakovszky, von Keyserlingk, Pollmann, 2004.05177 | Transport (2-point) only; explains why transfer is easy (T6). Not an OTOC method. |
| L10 | Cluster expansion gives a polynomial-time algorithm for local observables and Loschmidt echoes at short times. | Wild & Alhambra, PRX Quantum 4, 020340 (2023), 2210.11490 | INFERENCE: the guaranteed time is ~1/(local coupling × degree), i.e. a few µs for ω_loc ≈ 2π·12 kHz. It covers only the start of the window. |
| L11 | Pauli-propagation truncation error "is governed by the Operator Stabilizer Rényi entropy". Operator-entanglement volume law ⇒ no efficient MPO; log scaling ⇒ MPO-simulable. | Shao, Cheng, Liu, 2510.22311; Dowling, 2603.05656 | Diagnostics that could be computed on our operators (recommended test T-F). |
| L12 | OTOCs on 53 qubits: "operator spreading is captured by an efficient classical model", while "operator entanglement requires exponentially scaled computational resources to simulate". | Mi et al., Science 374, 1479 (2021), 2101.08870 | **Key**. The front/average part of OTOC(1) is classical (population dynamics). Any hardness sits in instance-specific interference ("fluctuations"). |
| L13 | OTOC(2) "remain sensitive to the underlying dynamics at long time scales", "dominated by constructive interference between Pauli strings that form large loops", "exceeding the simulation capacity of known classical algorithms"; observables without the second time reversal "become insensitive … at long times due to … scrambling". | Google Quantum AI (Abanin et al.), Nature 646, 825 (2025), 2506.10191 [F30]; supported by Bermejo et al. 2604.15427 [F31] | **Key**. The beyond-classical evidence is for OTOC(2), not OTOC(1). R1's instrument measures OTOC(1). |
| L14 | NMR OTOCs of small molecules in a liquid crystal, interpreted on Willow with Pauli-path zero-noise extrapolation; the abstract speaks of the "apparent exponential classical cost". | Zhang et al., 2510.19550 [F34] | Same pipeline, small molecules; the bibliography records it as self-declared "not yet beyond classical". |
| L15 | OTOC fronts in random circuits map to classical stochastic front propagation, i.e. "hydrodynamical" equations with a butterfly velocity. With U(1): conserved parts diffuse, non-conserved parts spread ballistically, and OTOC tails are diffusive power laws. | Nahum, Vijay, Haah, PRX 8, 021014 (2018), 1705.08975; von Keyserlingk et al., PRX 8, 021013 (2018), 1705.08910; Khemani, Vishwanath, Huse, PRX 8, 031057 (2018), 1710.09835; Rakovszky, Pollmann, von Keyserlingk, PRX 8, 031058 (2018), 1710.09827 | THEORETICAL for random circuits. Basis of the front model (§2.5) and of the hydrodynamic-reduction adversary (§3.4c). |
| L16 | Operator growth as an epidemic (SI) process. | Qi & Streicher, JHEP 08 (2019) 012, 1810.11958 | Model family used in §2.5. |
| L17 | OTOCs improve learnability of strongly interacting systems, e.g. with single-probe access or weak couplings. A companion paper proves an exponential *learning* separation versus time-ordered protocols. | Schuster, Niu, Cotler, O'Brien, McClean, Mohseni, 2208.02254; see also Chiew, Angrisani, Holmes, 2607.15493 (query-complexity bounds) | LITERATURE-SUPPORTED: anticipates R1's "echo FI ≫ transfer FI". This is an **experimental-protocol** advantage (time-reversal NMR), available to classical post-processing whenever the forward model is classically computable. It is not a computational separation. |
| L18 | Decoherence localises the growth of correlated-spin clusters in NMR: "the system reaches a dynamic equilibrium size, which decreases with the square of the perturbation strength". | Álvarez & Suter, PRL 104, 230403 (2010), 1004.5003 (abstract-level) | INFERENCE: the *physically measured* echo has a cone bounded by imperfect reversal and decoherence. Its size in proteins is unknown here. |
| L19 | Dynamic mean-field theory for spins (spinDMFT, cluster/non-local variants) for dense dipolar spin dynamics at infinite temperature. | Gräßer, Hahn, Uhrig, SSNMR 132, 101936 (2024), 2403.10465; Gräßer et al., PRR 5, 043191 (2023), 2307.14188 | Untested classical adversary for OTOC(1) in dense networks (NM-4). |

**Not verified this session:** multiple-quantum "spin counting" cluster sizes in adamantane (Krojanski & Suter 2004; Álvarez, Suter & Kaiser, Science 2015). They were not found by the arXiv queries used, so no numbers from them are used.

**Synthesis (THEORETICAL / INFERENCE).**
- No known result makes OTOC(1) of fixed geometric dipolar Hamiltonians classically hard at additive accuracy σ = 0.01.
- The only hardness anchors are worst-case: DQC1 (L1–L4) and universality (L5).
- The strongest empirical hardness (L13) is for OTOC(2).
- The strongest classical results (L6, L7, L12, L15) indicate that OTOC(1) averages and fronts are classically structured, and that noise makes Pauli paths easy.
- Any hardness of OTOC(1) must therefore come from instance-specific interference (operator entanglement) that survives embedding and decoherence. Nothing in the literature establishes this for dipolar protein networks.

---

## 2. Light cone of Z_a(t) in the protein ¹H network

### 2.1 Proton density and couplings (`density_couplings.py` → `density_couplings.json`; MEASURED from the instrument PDBs)

| | 1UBQ | 1PGA |
|---|---|---|
| n_H | 629 | 419 |
| ρ_H, n_H / V (0.73 cm³/g partial specific volume) | **0.061 Å⁻³** | 0.056 Å⁻³ |
| ρ_H, convex hull (a lower bound, rough surface) | 0.048 | 0.051 |
| ρ_H local, buried protons, R = 6 Å | 0.059 | 0.053 |
| mean N within R of a buried proton: 4 / 5 / 6 / 8 / 10 / 12 Å | 15.7 / 31.2 / 53 / 118 / 206 / 307 | – / 28.7 / – / 105.8 / – / – |
| nearest-neighbour distance (median) | 1.77 Å | 1.77 Å |
| ω_loc = (Σ_j d_aj²)^{1/2}/2π, isotropic average, median | 12.6 kHz | 12.1 kHz |
| amide-only network: n_HN, ρ | 73, 0.0070 Å⁻³ | 56, 0.0075 Å⁻³ |
| amide-only ω_loc (median) | 2.9 kHz | 3.3 kHz |

The density is 0.056–0.061 H/Å³ (at the low end of the 0.06–0.08 in the brief). A cone of 30 spins has radius ≈ 5 Å, and one of 40 spins ≈ 5.5 Å (MEASURED table).

### 2.2 Exact finite-cluster operator front (`exact_front.py` → `front/*.json`; MEASURED)

- **What was computed.** Sector-exact, same Trotter circuit, cluster and field direction as the instrument. For every spin j: F^Z_aj, F^X_aj (= F^Y by U(1)), S_aj, and the support probability p_j = Pr(P_j ≠ I) = (3 − 2F^X − F^Z)/4 (DERIVED: Σ_{σ∈{I,X,Y,Z}} σ_j P σ_j = 4P if P_j = I, else 0). The operator size is Σ_j p_j.
- **Validation.** The F^Z curves reproduce the RAW `nmr_embed` exact echoes to 3–6×10⁻¹⁶ at N = 10 and 12.

Operator size Σ_j p_j (MEASURED):

| cluster | N | 20 µs | 40 µs | 80 µs | 160 µs | 320 µs | r_max |
|---|---|---|---|---|---|---|---|
| 1UBQ p19 | 8 / 10 / 12 | 1.52 / 1.53 / 1.54 | 2.39 / 2.51 / 2.61 | 3.64 / 4.20 / 4.67 | 3.94 / 5.12 / 6.12 | 4.31 / 5.62 / 6.88 | 3.9 Å |
| 1UBQ p245 | 8 / 10 / 12 | 1.31 / 1.33 / 1.36 | 2.05 / 2.14 / 2.32 | 3.19 / 3.63 / 4.34 | 4.01 / 5.06 / 6.30 | 4.40 / 5.60 / 7.12 | 3.9 Å |
| 1PGA p325 | 8 / 10 / 12 | 1.49 / 1.54 / 1.55 | 2.34 / 2.53 / 2.62 | 3.24 / 3.77 / 4.20 | 4.22 / 5.22 / 6.24 | 4.67 / 5.98 / 7.41 | 4.1 Å |
| 1UBQ-HN p19 (dt 5 µs) | 8 / 10 / 12 | at 100 / 250 / 500 / 750 / 1000 µs: 1.62 / 1.82 / 2.15 / 2.52 / 2.67 (N=12) | | | | | 7.7 Å |

- **Dense network.**
  - Sizes agree across N up to ~30 µs, then separate. From ≳ 80 µs the size is bounded by N (MEASURED).
  - By 80 µs every site of the 12-spin cluster (out to 3.9–4.1 Å) has p_j ≥ 0.12–0.24. By 160 µs, p_j ≈ 0.35–0.6 everywhere (MEASURED, `front/1UBQ_p19_N12_o0.json` etc.).
  - Front arrival at shared sites is N-independent to ≤ 0.01 up to 80 µs, so the front itself is local (MEASURED).
  - The RAW `wmean` of the C2 runs is this same finite-cluster size (N = 10, ε = 3×10⁻⁵: 4.19 at 80 µs, 5.6 at 320 µs). It saturates at ~0.5–0.6 N, so it **cannot** be used to extrapolate the cone (MEASURED + DERIVED).
- **Amide-only network.** A strongly coupled pair (probe + neighbour at 2.7 Å) oscillates coherently (p₀: 0.87 → 0.39 → 0.93). Leakage to the rest is weak: p_j ≈ 0.05–0.2 at 1 ms (MEASURED).

### 2.3 Cluster-size convergence of the echo itself (MEASURED)

**All sites.** max_b |F^(N+2)_ab − F^(N)_ab| over common sites, dense network (`front/`):

| | 20 µs | 40 µs | 80 µs | 160 µs | 320 µs |
|---|---|---|---|---|---|
| 1UBQ p19, 10→12 | 0.006 | 0.026 | 0.043 | 0.097 | 0.072 |
| 1UBQ p245, 10→12 | 0.028 | 0.229 | **0.457** | 0.113 | 0.121 |
| 1PGA p325, 10→12 | 0.007 | 0.036 | 0.089 | 0.102 | 0.091 |
| 1UBQ-HN p19, 10→12 | – | – | – | 0.03–0.04 (150–180 µs) | up to 0.08 (0.5–1 ms) |

- **The instrument's observed sites** (RAW `nmr_embed`, b = 3 farthest + nearest): |F12 − F10| exceeds σ after 160 µs (p19) and after 40–120 µs (p245), reaching 0.03–0.12.
- **Direction of the change.** F decreases with N at late times; for example p245, b = 1, 160 µs: 0.591 (N=10) → 0.478 (N=12).
- **No convergence is visible at N = 12.** |F12 − F10| is not smaller than |F10 − F8|.

**N = 12 → 14 at the instrument's observed sites** (statevector typicality, `typicality_cone/1UBQ_p19_N{12,14}.json`; MEASURED).
- Validation: at N = 12 the run matches exact F to 0.0094 (n_rand = 4). At N = 14 its transfer S matches the RAW exact N = 14 transfer (`nmr_embed` exact_N14) to 0.014. The typicality error is 0.0078.
- Results, 1UBQ p19, |F14 − F12| at 40 / 80 / 120 / 160 / 240 / 320 µs:

| site | 40 µs | 80 µs | 120 µs | 160 µs | 240 µs | 320 µs |
|---|---|---|---|---|---|---|
| b = 1 (HA/GLN2, 2.16 Å) | **0.105** | **0.186** | 0.053 | 0.023 | 0.035 | 0.039 |
| b = 7 | 0.009 | 0.028 | 0.073 | 0.075 | 0.088 | 0.084 |
| b = 8 | 0.000 | 0.000 | 0.019 | 0.040 | 0.041 | 0.004 |
| b = 9 | 0.002 | 0.083 | 0.095 | 0.049 | 0.003 | 0.004 |

- **Conclusion (MEASURED):** N_σ > 14 for the instrument's own observables at every informative time from 40 to 320 µs. The large b = 1 change at 40–80 µs comes from protons added at 3.9–4.0 Å (HB2/GLN2 among them) that couple strongly to b itself. The σ-cone of F_ab is the cone of a *plus* a coupling shell around b.

### 2.4 σ-cone ladder on larger nested clusters (`pauli_cone.py` → `pauli_cone_*.json`; MEASURED with a heuristic certificate)

- **Method.** Sparse Pauli dynamics at ε = 10⁻⁴ on nested clusters N = 12, 16, 20, 24 (dense) and 12…28 (amide). For the first 12 sites, F_ab and the discarded norm L were recorded.
- **Certificate check.** At N = 12 the truncated F matches the exact sector F to |ΔF| ≈ 1–2·L (for example 0.0030 vs L = 0.0028 at 40 µs), so |ΔF| ≲ 2L.
- **Definition.** N_σ(t) is the smallest N after which every ladder step changes max_b F by ≤ σ. "Lenient" allows σ + L.

| t | 1UBQ p19: steps 12→16 / 16→20 / 20→24 | 1UBQ p245 | N_σ (strict / lenient) |
|---|---|---|---|
| 20 µs | 0.022 / 0.005 / 0.003 | 0.011 / 0.009 / 0.005 | 16 / 16 (certified) |
| 30 µs | 0.052 / 0.016 / 0.005 | 0.027 / 0.008 / 0.003 | 20 (p19), 16 (p245) |
| 40 µs | 0.095 / 0.030 / 0.004 (L = 0.012–0.033) | 0.054 / 0.018 / 0.004 | **20 / 16 (uncertified: L > σ)** |

- **Dense network:** r_σ(40 µs) ≈ 4.2–4.4 Å. The discarded norm at fixed ε and t grows with N (40 µs: 0.0028 → 0.0095 → 0.014 → 0.019 for N = 12 → 24, MEASURED). The truncation adversary therefore degrades as the cone is embedded.
- **Amide-only network (1UBQ-HN p19):**
  - Every ladder step is ≤ 0.006 up to 250 µs, so N_σ ≤ 12 (r ≤ 7.7 Å).
  - At 300 µs the steps are 12→16 = 0.022 and 16→20 = 0.006, so N_σ ≈ 16. At 350 µs they are 0.016 and 0.0096, again N_σ ≈ 16 (L ≈ 0.013–0.017).
  - The N = 20–28 runs hit the 90 s budget at 350–450 µs.

### 2.5 Front models and extrapolation to 80 / 160 / 320 µs (`front_model.py`, `extrapolate_cone.py`; INFERENCE)

- **Model.** First-passage ("operator epidemic") model on the full proton network: T_j = min_i(T_i + E_ij), with P(E_ij ≤ t) = 1 − exp[−(Γ_ij t)^k].
  - Rate laws: golden, Γ = κ d²/(2π·10 kHz); coherent, Γ = κ|d|.
  - Shapes: k = 1 (standard SI) and k = 2 (quadratic onset, the short-time perturbative law).
  - κ is fitted to the exact p_j(t) of the three dense N = 12 clusters at t ≤ 100 µs.
- **Model quality.**
  - The fits are mediocre: p_j RMSE 0.07–0.13 in the fit window and 0.10–0.24 later (`front_model.json`).
  - **Both k = 1 laws fail the early-time anchor badly.** In the full protein they predict an operator size of 9.7–55 at 40 µs, against 2.3–2.6 exact, where the N = 10 → 12 increment is only 0.1–0.2. They are discarded.
  - The k = 2 laws roughly pass (2.3–3.9 vs a ceiling of 2.9).
  - Only the golden law transfers to the amide network with the dense-network κ (RMSE 0.09–0.12 vs 0.2–0.5). Even so, it underestimates the amide σ-cone of §2.4.
- **σ-cone extrapolation.** The σ-cone is taken as the sites with P(T_j ≤ t) ≥ 0.02. This threshold reproduces the measured N_σ(40 µs) ≈ 18–25.

| 1UBQ, dense | 40 µs | 80 µs | 160 µs | 320 µs |
|---|---|---|---|---|
| measured N_σ | 16–20 | – | – | – |
| E2 diffusive front, r ∝ t^{1/2} from r_σ(40) | 20–21 | 57–60 | 146–152 | 331–348 |
| E3 ballistic front, r ∝ t | 20–21 | 146–152 | 937–986 (protein-capped 629) | protein-saturated |
| E4 front model golden k=2 / coherent k=2 (P ≥ 0.02) | 18–25 | 95 / 120–125 | 316 / 454–470 | 602–629 |
| **physical range** | **18–25** | **57–152** | **146–629** | **331–629** |
| E1 empirical floor, N ∝ t^0.30–0.34 fitted to 20–40 µs | 20 | 25 | 30–32 | 37–40 |

- E1 implies a cone radius growing as t^0.1. That is inconsistent with the measured front motion and with front physics (L15), so it is only a floor (INFERENCE).
- 1PGA (k = 2 models, P ≥ 0.02): 29–62 at 80 µs, 126–300 at 160 µs, 367–387 at 320 µs.
- In a crystal, powder or membrane sample the intermolecular network continues past the 629 protons of one ubiquitin (INFERENCE).

---

## 3. What would count as evidence of classical hardness, and does 2^N_cone exceed exact reach?

### 3.1 Exact classical reach (DERIVED, `cone_summary.json`)

| N | state vector (complex128) | largest U(1) sector | dense sector diagonalisation |
|---|---|---|---|
| 20 | 17 MB | 1.8×10⁵ | 2×10¹⁷ flop |
| 30 | 17 GB | 1.6×10⁸ | – |
| 36 | 1.1 TB | 9.1×10⁹ | – |
| 40 | 17.6 TB | 1.4×10¹¹ | – |
| 44 | 281 TB | – | – |
| 48 | 4.5 PB | – | – |

- **Exact reach.**
  - Time evolution with typicality: ~36–40 spins is routine HPC; ~45–48 is record-scale. INFERENCE; the exact records were not re-verified.
  - Sector diagonalisation stops at ~20 spins.
  - Forward inversion needs ~10³ evaluations, which lowers the practical reach by several spins.
- **Comparison.**
  - **Dense network:** N_σ exceeds 40 at 80 µs under every physically motivated law (57–152), and exceeds 146 at 160 µs. Only the rejected floor stays ≤ 40. **The kill criterion (N_cone < ~30 at the informative times) does not fire.**
  - **Amide-only:** N_σ ≤ 12–16 through 350 µs, well inside exact reach. **Kill fires up to 350 µs** (MEASURED, one probe). Beyond 350 µs the cone is unmeasured; the golden-law model predicts it stays small, but that model underestimated the cone at 300–350 µs.

### 3.2 Exceeding exact reach is not hardness

A 2^N_cone cost bounds only the *exact* method. Hardness for this instance family needs **all** of H1–H5.

- **H1 (target exists).** An N-converged reference F^∞_ab(t) and its FI at the informative times. **Currently absent beyond 40 µs** (§2.3–2.4). The C2/C3 string counts measure the cost of approximating a *fixed* N-spin model. They are not the cost of the physical echo; the scaling variable that matters is N_σ(t).
- **H2 (every classical family fails at scale).** Each family misses F^∞ by > σ at the informative times, and its cost to reach σ grows super-polynomially in N_σ. The families: sparse/weight-truncated Pauli with ε-extrapolation; dissipative (DAOE-type) truncation; cluster-correlation expansion and cluster/non-local spinDMFT (L19); classical spins with two-spin corrections; Krylov/recursion (L11-type diagnostics); and **population-dynamics (Pauli-phase-randomised) and hydrodynamic-reduction models (§3.4)**.
- **H3 (information survives).** The hard-window FI must survive N-convergence (not a finite-size plateau), embedding, physical decoherence and imperfect reversal (L18). It must also not be reproducible by the hydrodynamic reduction.
- **H4 (interference-dominated).** A diagnostic showing OTOC(1) is dominated by instance-specific interference, as F30 showed for OTOC(2). Concretely: F_ab must differ from its Pauli-phase-randomised (population-dynamics) value by > σ in the window. A reduction placing the geometric dipolar family in a DQC1-hard class would be stronger still (UNPROVEN, no path known).
- **H5 (break-even).** Quantum cost below the best classical cost at matched accuracy, including ~10³ forward evaluations (BREAK_EVEN §4). The fault-tolerant model gives ~11 h per forward evaluation.

### 3.3 Where R1 stands

- H1 not met.
- H2 met only against the implemented adversaries at N = 10, against an unconverged reference.
- H3 unknown.
- H4 untested.
- H5 unfavourable.

### 3.4 Structural reasons to expect a classical route for OTOC(1) (THEORETICAL / DERIVED / INFERENCE)

- **(a) Positivity.** F_ab = Σ_P c_P² s_P = 1 − 2W_b (DERIVED, T6). This is a positive "operator-weight" functional. Its averaged dynamics is a classical population process for random circuits (L12, L15). Hardness can only enter through the non-Markovian (interference) part.
- **(b) Scrambling insensitivity** (L13; O'Brien et al. 2022 found learnability collapses as dynamics becomes ergodic, NM-1). The window where the cone exceeds exact reach (≳ 80–160 µs) is the window where the literature expects OTOC(1) to lose dynamical detail.
- **(c) U(1) hydrodynamic reduction.**
  - Decompose O = O_c + O_nc, with O_c = Σ_j S_aj(t) Z_j (the conserved, diagonal part; no X/Y at b) and C(t) = Σ_j S_aj². Then W_b = q_b(t)(1 − C(t)) (DERIVED, exact as a definition of q_b).
  - If O_nc scrambles (q_b → q_∞ ≈ ½), F_ab → 1 − 2q_∞(1 − C(t)). C(t) is a transfer-type quantity, which sparse Pauli reproduces exactly (MEASURED in C1) and which follows 3D diffusion at late times (L15).
  - At N = 12, C(320 µs) = 0.10–0.18 and q_b = 0.25–0.45, still site-specific; strongly coupled pairs have q_b ≈ 0.1 (MEASURED, `front/`). Whether q_b becomes universal in the embedded system is the open question: **test T-C**.
- **(d) Noise.** The measured echo is a noisy, imperfectly reversed dynamics. Pauli-path results (L6) and the localisation of cluster growth by perturbations (L18) both shrink the effective cone and the classical cost.

### 3.5 Points in R1's favour (for balance)

1. N_σ ≫ 40 at ≥ 80–160 µs on the dense network (INFERENCE from the measured 40 µs cone).
2. The sparse-Pauli discarded norm grows with the embedded N at fixed ε and t (MEASURED).
3. Instance-specific OTOC fluctuations required exponential classical resources on random circuits (L12).
4. OTOCs are more informative than time-ordered data for strongly interacting systems (L17), consistent with the measured echo FI ≫ transfer FI.

---

## 4. Flaws found in the R1 evidence

1. **Unconverged reference (MEASURED).** R1's N = 10 exact echo, the reference for every classical failure time, f_hard and FI split, differs from N = 12 by more than σ from 20–40 µs (all sites; up to 0.46 at 80 µs). At the instrument's observed sites the difference exceeds σ from 40–160 µs (0.02–0.12). The reported classical failure (by 80 µs) is failure to reproduce a 10-spin model, not the protein.
2. **Finite-size plateaus (MEASURED).** Late-window F values fall systematically with N. The late-window information at N = 10 is partly carried by cluster-truncation plateaus.
3. **Embedding test incomplete (MEASURED, RAW `nmr_embed`).** The echo embedding test stopped at N_env = 12. Transfer late FI had already dropped to 22–24% at N_env = 14. For p245 the top echo-FI eigendirection rotated (|cos| = 0.60) at N = 12.
4. **`wmean` misuse risk (MEASURED + DERIVED).** RAW `wmean` is a finite-cluster, truncation-weighted operator size saturating at ~0.5–0.6 N. It cannot measure a light cone.
5. **Wrong scaling variable for C2/C3 (DERIVED).** C2/C3 measure string counts at fixed N. The pre-registered kill (power law vs exponential in N) addresses the cost of approximating fixed clusters, not the growth of the σ-cone with t.
6. **Amide-only branch (MEASURED).** Its failure times (250–500 µs) lie inside a σ-cone of ≤ 12–16 spins up to 350 µs. Exact classical simulation is cheap there, so the branch is killed as a hardness claim for t ≤ 350 µs.
7. **Weak extrapolation (INFERENCE).** Cone sizes beyond 40 µs rest on front models that fit exact data only to RMSE 0.07–0.24 and spread by up to ~6× across laws. Two of the four laws fail the early anchor by 3–19×.
8. **Literature mismatch (LITERATURE-SUPPORTED).** The strongest published beyond-classical echo result (F30) is for OTOC(2). The R1 instrument measures OTOC(1), the order that F30 describes as losing sensitivity at long times.

## 5. Claim levels

- **Theoretical: L0–L1.** Worst-case DQC1-completeness of infinite-temperature OTOC estimation (L4, abstract-level) is the only anchor. There is no instance-family hardness, no separation, and no query-complexity statement for the forward model.
- **Practical: L0.** The target (an N-converged echo in the informative window) has not been computed. No classical adversary beyond N = 10 has been tested, and break-even is unfavourable.

## 6. Recommended tests (governed; exact commands; kill criteria)

- **T-A (decisive): σ-cone convergence of the echo over the full window.**
  - Command: `OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone.py --probe {19,245} --N {14,16,18,20,22,24}`
  - Method: statevector typicality on the same circuit, instrument b's. Validated at N = 12 against exact: max |ΔF| = 0.0094 with n_rand = 4 (typicality error 0.0078).
  - Measured cost here: N = 12 took 106 s (n_rand = 4); N = 14 took 86 s (n_rand = 1).
  - Scaled from N = 14 (INFERENCE): N = 16 about 6–10 min; N = 20 about 2–4 h; N = 22 about 8–15 h; N = 24 about 1.5–3 days and ~2.5 GB. Run N ≤ 22 first.
  - Already known (MEASURED): N_σ > 14 at the instrument b's for 40–320 µs.
  - **Kill:** N_σ(t) ≤ 24 for all t ≤ 320 µs on both probes (exact light-cone simulation suffices).
  - **Support:** F changes by > 3σ between N = 20 and 24 at t ≥ 160 µs.
- **T-B: population-dynamics (Pauli-phase-randomised) adversary for OTOC(1).**
  - Method: at N = 12 (exact), average F_ab over random single-site Pauli insertions applied identically in both branches after each Trotter step. This is the F30/Mi-2021 diagnostic.
  - **Kill (R1 at the classical-model level):** |F − F_rand| < σ over the informative window at the instrument b's. Then OTOC(1) is dominated by a classical Markov operator-weight process, simulable by Monte Carlo on large cones.
- **T-C: hydrodynamic-reduction adversary.**
  - Method: F̂_ab = 1 − 2q̂_b(1 − C(t)). C(t) comes from sparse Pauli transfer on an N ≥ 30 cone. q̂_b comes from an exact 12-spin cluster centred on b.
  - **Kill:** |F̂ − F^∞| < σ for t ≥ t_c.
- **T-D: CCE-2/3 and cluster-spinDMFT adversary for the amide network, 350 µs – 1 ms.**
  - **Kill:** agreement within σ with a T-A-style converged reference.
- **T-E: FI on converged references.**
  - Method: recompute the echo FI split with the N_σ-converged reference from T-A.
  - **Kill R1:** late-window echo FI (t ≥ t_c) at the converged reference < 25% of the N = 10 value (the same decline transfer showed at N_env = 14), or gain g < 2.
- **T-F: operator-complexity diagnostics.** Operator stabilizer Rényi entropy and operator entanglement of Z_a(t) versus t on N = 12–14 exact operators (L11). Volume-law growth that persists into the informative window supports H4; log scaling kills it.

## 7. Files

| file | what |
|---|---|
| `density_couplings.py` / `.json` | ρ_H, N(R), ω_loc (dense and amide), both proteins |
| `exact_front.py`, `front/*.json` | sector-exact all-site F^Z, F^X, S, p_j, size. 1UBQ p19/p245 and 1PGA p325 at N = 8, 10, 12 (dense); 1UBQ-HN p19 at N = 8, 10, 12 |
| `pauli_cone.py`, `pauli_cone_1UBQ_p19.json`, `pauli_cone_1UBQ_p245.json`, `pauli_cone_1UBQHN_p19.json` | σ-cone ladders (ε = 10⁻⁴; dense to 40 µs, amide to 350–600 µs) with lost-norm certificates and an N = 12 bias check |
| `front_model.py`, `front_model.json`, `front_model.log` | first-passage front models (4 laws), fits, validation (V1–V3), full-protein predictions |
| `extrapolate_cone.py`, `cone_summary.json` | N_σ ladders (strict/lenient), extrapolations E1–E4, exact-cost table |
| `typicality_cone.py`, `typicality_cone/1UBQ_p19_N12.json`, `typicality_cone/1UBQ_p19_N14.json` | governed-job script for T-A. Validated at N = 12 (F vs exact) and N = 14 (S vs RAW exact). Gives the measured N = 12 → 14 non-convergence at the instrument b's |
