# ROUND3 lane: new_mechanisms_A

_2026-09-28. Nine new candidate quantum mechanisms for protein-structure computation (NA-1 to NA-9), none of them one of the 28 killed discovery mechanisms. Three were tested against pre-registered kill rules (`prereg.json`, written before any run). **All nine are killed.** The lane verdict is **KILLS**._

Tags: MEASURED, DERIVED, THEORETICAL, LITERATURE-SUPPORTED, INFERENCE, UNPROVEN.

## Candidates

The full cards are in `mechanisms.json`: mechanism, protein task, how it was designed to satisfy `theory/ADVANTAGE_CONDITIONS.md`, classical competitor, hardest condition and cheapest falsification test.

| ID | Mechanism | Hardest condition | Test | Outcome |
|---|---|---|---|---|
| NA-1 | Programmable Gaussian boson sampling (GBS) on the native-free ESM contact-odds kernel. Samples satisfy P(S) ∝ Haf(W_S)²; each sample is used as a pairing/contact seed | A8 structural value; A2 classical hardness for nonnegative kernels | **T1 (run)** | KILLED [MEASURED] |
| NA-2 | Coupled methyl-rotor tunnelling network as a quantum forward model of core packing | B5 observability; B1 | **T2 (run)** | KILLED by kill clause (i) [MEASURED model]. Residue R-ROTOR is parked |
| NA-3 | Quantum SDP solvers for Gram/EDM restraint-based structure determination | A5 (γ⁴–γ⁵ precision cost); A9 readout | **T3 (run)** | KILLED [DERIVED + MEASURED classical] |
| NA-4 | Hidden-subgroup / QFT symmetry detection (helical indexing, oligomer symmetry, repeat periods) | A2: the groups are small or continuous, and classical FFT is O(n log n) | derivation | KILLED [DERIVED] |
| NA-5 | Quantum fingerprinting / communication separations for distributed structure comparison | value: communication is not a bottleneck, and the task needs similarity, not equality | derivation | KILLED [DERIVED] |
| NA-6 | Quantum ε-machines (memory advantage) as surrogates of conformational dynamics | value: the saving is ≤ ~20 bits of memory, with no time speedup | derivation | KILLED [DERIVED] |
| NA-7 | Quantum-limited super-resolution receivers (SPADE) for intramolecular distances | classical bypass (photoswitching); ~1 nm linker floor; this is sensing, not computation | derivation | KILLED [DERIVED] |
| NA-8 | Quantum exponential-time DP (Ambainis et al.) against the classical subset-DP winner for sheet topology | A3: T → T^0.79–0.86, which is sub-quadratic; needs QRAM | derivation | KILLED [DERIVED] |
| NA-9 | QLSA / quantum PDE Poisson–Boltzmann electrostatics for scoring | A3/A5: multigrid is already O(N); a scalar readout costs Θ(1/ε); DE-7 | derivation | KILLED [DERIVED] |

**Novelty check.** Searched `discovery/CANDIDATE_MECHANISMS.md`, `KILLED_DIRECTIONS.md` and `literature/domain_notes/lit_F_claims.md` for each of these mechanisms; none appears. Some are adjacent to earlier work:
- NA-3 is adjacent to K-011/QM-27;
- NA-7 is adjacent to QM-24;
- NA-8 is adjacent to QM-16.

Literature entry P1 killed *random* GBS because it has "no protein mapping". NA-1 supplies that mapping and is still killed.

---

## T1: GBS on the contact-odds kernel (NA-1)

**Setup.**
- **Kernel.** W_ij = p/(1−p), where p is the esmprior_v1 `contact_prob` (DEP, native-free), restricted to |i−j| ≥ 6.
- **Output distribution.** The collision-free, fixed-2k-photon GBS output distribution is P(S) ∝ Haf(W_S)² [Hamilton et al., PRL 119, 170501; arXiv verified].
- **Proposal.** Each sample S becomes the max-weight perfect matching inside S, giving k contact pairs.
- **ORACLE metrics.** Native contacts are CA–CA < 8 Å. The metrics are:
  - prec: fraction of the k pairs that are native;
  - cov: distinct native contacts across 200 proposals;
  - allc: all k pairs native.
- **Scope.** 16 ladder chains × L ∈ {60, 100} × k ∈ {3, 5} = 64 cells.
- **Classical comparators, all efficient at any k and fixed a priori:**
  - uniform sampling;
  - β = 1, i.e. Haf¹, the k-matching Gibbs measure;
  - greedy max-weight k-matching;
  - perturb-and-MAP and edge samplers. Their temperature is **calibrated native-free**: I used the grid value whose mean model contact probability (mpp) is closest to GBS's.

**Attack on my own production run.** The first run used single-swap Metropolis. It under-mixed (acceptance 2–5%), which biased the GBS coverage low by about 55% (`results_thin_check.json`). It is superseded by a heat-bath hafnian sampler that uses row expansion (`haf_gibbs`, v2; `results_gibbs_check.json`). The v1 files are kept.

**Results (v2, `analysis_value_v2.json`):**
- **[MEASURED]** GBS (β = 2) is privileged over every efficient comparator in **3 of 64 cells** (4.7%). The pre-registered survival threshold was ≥ 75%, so the **kill fired**.
  - By regime: L60k3 0/16; L60k5 2/16; L100k3 0/16; L100k5 1/16.
  - GBS is Pareto-matched by calibrated perturb-and-MAP in 52 of 64 cells and by the calibrated edge sampler in 56 of 64.
- **[MEASURED] GBS minus native-free-calibrated perturb-and-MAP** (bootstrap CI over cells; Wilcoxon on paired cells):

  | Metric | Mean difference | 95% CI | Wilcoxon p |
  |---|---|---|---|
  | prec | −0.012 | [−0.018, −0.006] | 8e-4 |
  | cov | +0.7 contacts | [−0.2, +1.6] | 0.31 |
  | allc | −0.014 | [−0.025, −0.003] | — |

- **[MEASURED] β behaves as a temperature knob.** Across the β family (0, 0.5, 1, 2, 4, 8), precision rises monotonically with β (median Spearman ρ = 1.00) and coverage falls (median ρ = −0.79). β = 2 is therefore an interior point of a smooth tempering curve that classically efficient samplers already cover.
  - GBS vs the β = 1 k-matching Gibbs measure: prec +0.23 but cov −13.7. That is a trade-off, not a dominance.
- **[MEASURED] Classical emulation of the GBS distribution (`analysis_emulation.json`).** A double-dimer Metropolis sampler has state (S, M₁, M₂) with weight w(M₁)w(M₂). Its marginal over S is exactly Haf(W_S)² for nonnegative W.
  - **Small-k validation.** Against exact enumeration of all C(30, 6) = 593,775 subsets (L = 30, k = 3), the TV distance of vertex marginals is 0.018–0.032 (below the pre-registered 0.05).
  - **20–60 photons.** R-hat of the log-weight is 1.000–1.023. The two-chain maximum vertex-marginal gap shrinks as t^−1/2: 0.26 → 0.052 (k = 10) and 0.29 → 0.058 (k = 30, 60 photons) at 4M steps, about 40 CPU-s per chain. This is marginally above the pre-registered 0.05, and the trend reaches it at about 5–6M steps [INFERENCE].
  - **Value at 20–60 photons.** Calibrated perturb-and-MAP beats the GBS samples on both precision and coverage in **11 of 12** large-k cases.
- **[LITERATURE-SUPPORTED, abstract verified via arXiv API; exact scope for weighted kernels UNVERIFIED]**
  - Anand, Chen, Cryan, Freifeld, Goldberg, Guo, Zhang, arXiv 2511.16558: a GBS-on-graphs distribution is classically samplable in polynomial time, "thus quantum algorithms do not provide exponential speedup for these applications".
  - Zhang et al., arXiv 2505.02445: polynomial-mixing Glauber dynamics for unweighted graphs.

**Conclusion.** Classically efficient samplers match or beat the squared-hafnian distribution on the structural task, and the distribution itself is classically emulable at the tested sizes. **Kill.**

## T2: coupled methyl-rotor tunnelling (NA-2)

**Setup.**
- **Geometry.** 1UBQ_H.pdb (OpenMM-protonated), 50 methyls.
- **Exact symmetry [DERIVED].** Each rotor's potential is invariant under rotating that rotor alone by 2π/3, because its three protons are identical. So H is block-diagonal in the 3^N symmetry labels σᵢ = mᵢ mod 3.
- **Pair calculations.** Exact plane-wave calculations per symmetry sector (M = 45, G = 144) for the 16 methyl pairs that come closest under rotation. Couplings are AMBER-type LJ H···H, with and without worst-case Coulomb (q_H = 0.06 e, ε_r = 1). The intrinsic barrier V3 was scanned.
- **3-rotor clusters.** Lanczos on an FFT-applied Hamiltonian, validated against the decoupled limit to 1e-9 (`validate_triangle.json`).

**Results (`summary_t2.json`):**
- **[MEASURED, model] Single-rotor splitting Δ(V3).** Converged in M.

  | V3 (meV) | 40 | 50 | 60 | 80 | 100 | 150 |
  |---|---|---|---|---|---|---|
  | Δ (µeV) | 3.2 | 1.13 | 0.43 | 0.075 | 0.016 | 5e-4 |

  Protein methyl barriers are typically ~80–180 meV (8–17 kJ/mol) [LITERATURE; not re-verified this session]. At V3 = 100 meV, **all 32 dressed pair splittings are ≤ 0.055 µeV**, below the ~0.1–1 µeV resolution of backscattering INS [INFERENCE]. **Kill clause (i) fired:** the observable does not exist at protein-typical barriers.
- **[MEASURED, model] Kill clause (ii) did NOT fire.** The many-body part is not negligible in the model.
  - Hartree mean field misses the dressed splitting by a median of 40% / 21% / 13% at V3 = 30 / 60 / 100 meV (worst cases about 100%).
  - The pair non-additivity J is ≤ 0.064 µeV in absolute terms.
  - In two jammed triangles at V3 = 30 meV, the pair-cluster expansion of the dressed splitting is off by 5% to 137× (multiplicative form).
  - The H···H < 2.6 Å methyl contact network percolates: the largest cluster has 34 of 50 methyls, so a 34-rotor sector has about 17³⁴ ≈ 10⁴² states.
- **Support condition not met.** No pair has |J| ≥ 10% of Δ together with Δ ≥ 1 µeV.
- **Caveats [INFERENCE].**
  - The hydrogens are unrelaxed OpenMM placements, which exaggerates the contacts.
  - No barrier disorder was modelled; a 1 K protein glass broadens tunnelling lines inhomogeneously.
  - Methyls observable at ≥ 1 µeV need V3 ≲ 50 meV, which is rare (Met-like).
  - The structural information is local packing that crystallography and methyl NOEs already constrain.
  - Ring-polymer instanton methods are the classical competitor for deep-tunnelling splittings [LITERATURE; not verified this session].

**Conclusion.** Killed as a protein-structure advantage. Residue **R-ROTOR** (a physics curiosity in category 3, not structure) stays open: do relaxed, disordered, low-barrier coupled methyl clusters in real proteins stay beyond pair-cluster expansion and instanton methods at observable splittings?

## T3: quantum SDP for EDM completion (NA-3)

**Setup.**
- **Classical solver.** Burer–Monteiro rank-3 stress minimisation (L-BFGS, 4 starts) from native-free ESM `expected` distances with sd < 2 Å, plus sequential 3.8 Å constraints.
- **Scope.** 8 chains × L ∈ {30, 60, 100, 150}.
- **Quantum count.** The quantum solver cost is O~((√m + √n γ) s γ⁴) [van Apeldoorn & Gilyén, arXiv 1804.05058, verified]. I set it up in the quantum-favourable direction:
  - polylogs = 1 and r = 1;
  - 1 µs per query;
  - ε from a 1 Å error on an 8 Å restraint after normalising ρ = G/R.

**Results (`qsdp_breakeven.json`):**
- **[MEASURED]** Classical: **0.02–1.3 CPU-s** per crop.
- **[DERIVED]** Quantum: **≥ 1e11–4e17 queries**, which is 1 day to 1.4e4 years.
- **Scaling.** Fitted exponents are Q ∝ L^7.2 against classical CPU ∝ L^2.1. The gap widens with L: γ grows with R ∝ L·Rg² at fixed physical precision, so there is no break-even at any size.
- **[MEASURED, ORACLE] The problem is information-limited as well.** From these sparse confident restraints the solutions are 7–16 Å RMSD from native. Any solver of the same SDP inherits that.

**Conclusion.** **Kill.**

---

## Ledger

| Field | Value |
|---|---|
| IDs | ROUND3-NMA-T1, T2, T3 |
| Splits and leakage | Ladder crops (leakage-screened chains, DEP esmprior_v1 inputs). Native CA was used **only** for ORACLE metrics (T1, T3). There was no selection on native data: every calibration (perturb-and-MAP τ, edge γ) matches the native-free mpp. T2 is a physics forward model on a given structure. |
| Quantum resources | T1: photonic GBS at 6–60 photons (collision-free, PNR; losses ignored, which favours quantum). T2: none run; the model is a qutrit/rotor simulation. T3: query counts as above. Everything was simulated classically; simulator runtime is not quantum runtime. |
| Compute | Single-threaded throughout. About 25 CPU-min in total (T1 about 16, T2 about 8.5, T3 about 0.5). Every run was ≤ 5 CPU-min and < 0.5 GB RAM. Each production run was checkpointed with atomic tmp+replace per cell. |
| Statistics | T1: paired Wilcoxon over 64 cells, bootstrap CIs, per-cell unpaired 95% Pareto rule. T2/T3: deterministic. |
| Replication | T1: 16 chains × 2 lengths × 2 k; the large-k emulation used 4 chains × 3 sizes × 2 independent chains. T2: 16 pairs × 3 barriers × 2 coupling models; 2 triangles. T3: 8 chains × 4 lengths. |

## Files

| File | Contents |
|---|---|
| `prereg.json` | Pre-registration of T1–T3 |
| `mechanisms.json` | The nine candidate cards |
| `t1_gbs_contact/gbs_lib.py` | Library: kernels, exact hafnian, Metropolis, heat-bath and multi-dimer samplers, metrics |
| `t1_gbs_contact/run_value.py` | v1 production run (superseded) → `results_value.json`, `analysis_value.json` |
| `t1_gbs_contact/run_thin_check.py`, `gibbs_check.py` | Mixing attack |
| `t1_gbs_contact/run_value_gibbs.py`, `analyze_value_v2.py` | v2 production run → `results_value_gibbs.json`, `analysis_value_v2.json` |
| `t1_gbs_contact/run_emulation.py`, `run_emulation_long.py`, `analyze_emulation.py` | Classical emulation → `results_emulation*.json`, `analysis_emulation.json` |
| `t2_methyl_rotor/rotor.py` | Library |
| `t2_methyl_rotor/run_pairs.py` | → `results_pairs.json` |
| `t2_methyl_rotor/run_triangle.py`, `validate_triangle.py` | → `results_triangle.json`, `validate_triangle.json` |
| `t2_methyl_rotor/components.py`, `summarize.py` | → `components.json`, `summary_t2.json` |
| `t3_qsdp_edm/qsdp_breakeven.py` | → `qsdp_breakeven.json` |
