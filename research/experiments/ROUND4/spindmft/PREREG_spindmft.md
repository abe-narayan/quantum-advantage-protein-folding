# Pre-registration: spinDMFT adversary for R1-SIM at t ≤ 120 µs (ROUND4 lane `spindmft`)

_Written 2026-09-28T11:33-07:00, before any spinDMFT output existed. Parent rule: `experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`, "Round 4", CRITIC A-2._

## Parent rule (copied verbatim in substance)

Implement (nl-)spinDMFT for the dense ¹H network for the autocorrelation and H_∞. Where an echo extension exists, apply it to F_∞ at t ≤ 120 µs. **KILL R1-SIM(-X) at those times if it agrees with the exact + CSD hybrid within σ = 0.01 where both are defined.**

## Literature status (arXiv API / abs pages fetched 2026-09-28)

- spinDMFT: Gräßer, Bleicker, Hering, Yarmohammadi, Uhrig, PRR 3, 043168 (2021), **arXiv:2107.07821** (the task text's "2105.xxxxx" is wrong).
- nl-spinDMFT (pair correlations from clusters coupled to spinDMFT mean fields; Hahn echo in adamantane): Gräßer, Hahn, Uhrig, SSNMR 132, 101936 (2024), arXiv:2403.10465.
- CspinDMFT (cluster extension): Gräßer, Rezai, Sushkov, Uhrig, PRR 5, 043191 (2023), arXiv:2307.14188.
- Spin diffusion in static solids: Gräßer, Uhrig, Ernst, Sci. Adv. 12, eaee6228 (2026), arXiv:2512.15572.
- **No OTOC / four-point extension of spinDMFT was found** (abstract-level search: all Gräßer–Uhrig entries; "mean-field" ∧ "out-of-time-order" ∧ dipolar returned 0). The "echo" in 2403.10465 is a Hahn echo, i.e. a two-point function with a π pulse, not an OTOC.

## What is computed (all native geometry = physical instance definition only; no leakage issue)

Instance: 1UBQ, OpenMM protons of `data/instruments/nmr/1UBQ_H.pdb` (629 ¹H), couplings `qapf.nmr.spins.couplings`, b0 = `random_b0(1000)`, probes p19 and p245, instrument sites b ∈ {1, 7, 8, 9} (probe-cluster ranks), same as the round-3 reference.

1. **sr-spinDMFT** (site-resolved spinDMFT, the disordered-lattice form): each spin i sees a Gaussian classical field V_i with ⟨V_i^z V_i^z⟩(τ) = Σ_j d_ij² g_j^z(τ), ⟨V_i^x V_i^x⟩(τ) = ⟨V_i^y V_i^y⟩(τ) = ¼ Σ_j d_ij² g_j^⊥(τ); single-spin dynamics in that field; iterate g to self-consistency. World = whole protein (thermodynamic limit of the isolated molecule) or a closed N-spin cluster (validation world).
2. **nl-spinDMFT (embedded exact cluster)**: cluster C ∋ a of n_c spins solved exactly (typicality vectors), the same fused pair gates in the same order as the reference Trotter circuit (dt = 2 µs), each cluster spin q driven by the Gaussian bath field V_q = Σ_{j∉C} c_α d_qj ξ_j (cross-correlated between cluster spins through shared bath spins; bath autocorrelations g_j from step 1; bath–bath cross-correlations neglected — stated approximation A2). Gives G_aa(t), G_aj(t) for j ∈ C, H_C = Σ_{j∈C} G_aj².
3. **OTOC extension (derived here, approximation A3 "quenched Gaussian bath")**: F_ab^emb(t) = E_ξ Tr[W_ξ Z_b W_ξ Z_b]/2^{n_c}, W_ξ = U_ξ(t)† Z_a U_ξ(t), with the *same* bath-field realisation ξ in forward and backward branches. Neglects back-action (operator growth into the bath and back) except through local rotations of cluster spins. Known limitation stated before running: when a cluster spin's bath coupling is strong, A3 converts polarisation flow into the bath (commuting with Z_b in the exact dynamics) into transverse rotation at that spin (anticommuting), which biases F low; at full scrambling A3 tends to F → −1/3 for b ∈ C instead of 0.

## Comparators

- Exact finite clusters (same Trotter circuit): F_N from `ADVERSARIAL/R1_theory_hardness/typicality_cone/` (N = 12–18), H_N, G_N and floor_N from `ROUND3/r1sim_exact_reach/verify_classical/runs/` (N = 12–20).
- Hybrid thermodynamic-limit estimate (CRITIC C1 / verify_classical): F_∞^hyb = H_∞(CSD N_c = 80–160 + exact−CSD offset at N = 20) + X_18, X_18 = F_18 − H_18 − floor_18, at t = 40, 80, 120 µs; 2 probes × 4 sites × 3 times = 24 series.

## Validation gate (added here, before results; makes a kill harder, never easier)

In the closed **N = 18 world** (bath = the 18 − n_c cluster spins outside C), the embedded method is compared with exact H_18 and with F_18 − floor_18 (primary: an open-cluster method has no conserved-charge floor) and F_18 (secondary). The spinDMFT F estimate is called **validated at time t** if |F^emb − (F_18 − floor_18)| ≤ σ on ≥ 6/8 series at that t for the largest n_c run.

## Decision rules (per time t ∈ {40, 80, 120} µs)

- **Literal parent rule — KILL fires at t** if |F_∞^emb − F_∞^hyb| ≤ σ = 0.01 on ≥ 7/8 series at that t (one outlier allowed for statistical noise), using the largest n_c run in the protein world.
- **Reported verdict:**
  - **KILLS** if the literal rule fires at every t ≤ 120 µs **and** the validation gate passes there (two independent validated polynomial estimators agree within σ).
  - **INTERESTING** if the literal rule does not fire but the discrepancy is explained by a validated failure of one estimator (i.e. the question moves but is not settled), or if the rule fires only where validation fails.
  - **SUPPORTS** (narrow: "σ-level classical reach not demonstrated at t ≤ 120 µs") only if the spinDMFT family is not validated at σ, its error does not fall with n_c, **and** it disagrees with the hybrid by > 3σ on ≥ 4/8 series at some t ≤ 120 µs.
  - **WEAK** otherwise.
- Two-point check (not a kill criterion): H_∞ from nl-spinDMFT vs H_∞(CSD); agreement within the CSD SE (0.004–0.011) + σ/2 is reported as cross-family confirmation of H_∞.
- None of these outcomes revives K-105 (forward-model error 5–66 σ; value ≤ 1.2–3).

## Budget

Single-threaded (OMP/MKL/OPENBLAS = 1), each run ≤ 30 CPU-min and ≤ 2.5 GB, total ≤ 90 CPU-min; every run > 3 min checkpoints per batch (atomic tmp + replace) and resumes.

## Addendum A (2026-09-28T12:17-07:00, after the n_c = 10 results and before any world-ladder or b-aware run)

**What had been seen when this was written.**
- n_c = 10 in both worlds, n_c = 12 in the protein world for p19.
- Exact F/H/floor/X ladders N = 12–20 (existing files).

**Deviation D1: the primary validation target.** The primary target F₁₈ − floor₁₈ assumed the conserved-charge floor is an additive finite-size offset in F. The exact ladder contradicts that at 40 µs: F_N stays flat while floor_N falls (flat-X test in `analyze.py`).
- The verdict below is still reported against the pre-registered primary target.
- The direct target F₁₈ is reported beside it and labelled post hoc.

**New diagnostic W (world ladder), fixed now.** Run spinDMFT (n_c = 10, probeb family, self-consistent sr bath within each world) in the closed worlds N = 14, 16 and 20, then compare its N-dependence with the exact one:
- the error is ΔF_dmft(N) − ΔF_exact(N), with ΔF(N) = F(W_N) − F(W_18);
- this is computed for every (series, N) pair where exact data exist.

**Criterion.** The spinDMFT bath correction counts as **corroborated at time t** if |ΔF_dmft(N) − ΔF_exact(N)| ≤ σ on ≥ 80% of the (series, N) pairs at t. Only then is the bath-corrected estimator F_corr = F₁₈ + [F^emb(protein) − F^emb(W₁₈)] treated as a σ-level candidate for F_∞ at t.

**New diagnostic B (b-aware clusters).** This is descriptive only.
- Clusters: pairb:b clusters with n_c = 10, in both worlds.
- Series: the three whose butterfly site keeps ≤ 27% of its second moment M2 inside the 18-cluster (p19 b8, p19 b9, p245 b7).

## Addendum B (2026-09-28T12:36-07:00, after the b-aware spinDMFT runs and before any exact b-aware run)

**Prediction to test.** spinDMFT predicts a large, family-independent bath correction at three butterfly sites whose own dipolar partners lie mostly outside the probe-centred cluster. The exact probe-centred family misses those partners.
- p245 b7: F(40, 80, 120 µs) = 0.764 / 0.496 / 0.290 (b-aware, protein world), against the probe-family exact F₁₈ = 0.699 / 0.421 / 0.267.
- p19 b8: 0.983 / 0.907 / 0.775 against F₁₈ = 0.953 / 0.811 / 0.651.
- p19 b9: 0.953 / 0.749 / 0.540 against F₁₈ = 0.954 / 0.761 / 0.565.

**Test E-B.** Run exact typicality clusters of the b-aware family:
- composition: {a, b} ∪ the protons nearest to a or b;
- the same Trotter circuit, `qapf.nmr.spins.exact_correlators`;
- sizes N = 12, 14, 16.

**Criterion.** The spinDMFT site-environment prediction is **corroborated at t** if, on ≥ 2 of the 3 series, the exact b-aware F_16 lies closer to the spinDMFT value than to the probe-family F₁₈. That is, it moves ≥ 50% of the predicted shift. Only series where the predicted shift is ≥ 2σ count. Otherwise it is **not corroborated**.
