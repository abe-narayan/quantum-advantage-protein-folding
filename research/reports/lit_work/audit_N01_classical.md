# Audit N01: classical adversary (round 2)

Date: 2026-09-28. Role: classical adversary. The task is to show, if possible, that the decision-relevant regime is classically solved or not decision-bearing.

Candidate N01: the multi-band FCI vs CDW vs AHC competition in hBN-aligned rhombohedral multilayer graphene (RnG/hBN) at fractional filling, with explicit remote bands.

Inputs:
- `round2_prefilter.md` §3
- `round2_discovery_static_inside_wall.md` S-M1

Status: COMPLETE. Verdict: **WOUNDED, leaning to kill.** A single cheap classical experiment (§7) is expected to convert this to KILLED. No part of the decision-relevant regime has been shown to lie inside a classical wall.

---

## 0. Bottom line

The six points below are independent. Any one of #2, #3 or #4 would suffice to fail the round-1 filter.

1. **The primary yes/no has already been answered classically, provisionally "yes".**
   - Question: does the continuum model with explicit remote bands support a gapped nu = 2/3 FCI anywhere in the prior?
   - Source: Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, arXiv:2608.12452 [V, Aug 2026].
   - Method: 3-conduction-band ED at N_k = 21, occupation-truncated. Band 2 is restricted to 14-17 k-points with n2 <= 6. Band 3 has 2-5 k-points. Dimension up to ~1e9.
   - Result: a multi-band FCI in the window V_val ≈ 4 to ~10 meV of the "moire capacitor" one-body term. The gap Delta_FCI ≈ 0.3 meV at V_val = 7 meV. The authors state that the gap "converges to a finite >0.1 meV gap ... for 21 sites" and that the truncation converges in n2 by n2 = 6.
   - What remains open is finite-size convergence at N_k >= 27. That is a narrower question than the one N01 poses.

2. **The yes/no is not invariant across the prior. The decision sits in the model floor (lesson iii).**
   - The realistic V_val is 9 meV (direct computation) or 12 meV (analytic formula). The multi-band FCI window is 4 to ~10 meV. The realistic value therefore sits at or past the upper edge of the window.
   - A ~15-30% uncertainty in the moire-potential inputs moves the state point across the window edge.
   - Those inputs are:
     - V1 amplitude and phase;
     - hBN orientation, 0° vs 180° (Uzan et al., 2507.20647 [V]: "markedly different moire potential strengths" at identical moire wavelength);
     - lattice relaxation, which is "crucial" for the isolated C = 1 HF band (Nashabeh & Ochoa, 2605.16218 [V]);
     - the CN/AVE valence reference.
   - The valence reference problem is not addressed by adding explicit *conduction* remote bands. 2608.12452 still treats the valence manifold by its Hartree term only.
   - The CN vs AVE spread is qualitative: CN destroys the FCIs, AVE strengthens nu = 2/3 at first (2407.13770 [V]). That is a *model* spread, and larger solver power does not shrink it.

3. **The experimentally decisive nu = 2/3 competition is at finite temperature and entropy-driven. The ground-state eigenvalues do not carry it (lesson i).**
   - In at least one R-graphene/hBN device, the nu = 2/3 FCI transitions into a "generalized anomalous Hall crystal at temperatures below about 150 mK". The bulk transition is favoured over an edge-equilibration artifact (H. Li et al., 2607.08710 [V, abstract only]).
   - The extended QAH (EQAH) state spans nu = 0.5-1.3 at ~40 mK. The FQAH is recovered at higher T or current (Z. Lu et al., 2408.10203 [V]).
   - Theory: entropy of soft magnetorotons or Goldstone modes drives the finite-T transition from the EQAH to the FQAH regime (Kim & Kivelson, 2609.16483 [V, Sep 2026]).
   - So the observed FCI can be a finite-T phase whose T = 0 competitor wins. Deciding which phase the model predicts at the experimental T requires free energies, i.e. dense low-lying spectra or Gibbs states. That brings back the thermal-state cost that killed round 1 (lesson ii).
   - The T = 0 energy difference implied is ~k_B·150 mK ≈ 0.013 meV per relevant degree of freedom [ESTIMATE; order of magnitude only]. That is below both the ~0.1-0.3 meV FCI gap and the parameter floor.

4. **The strongest ablation, occupation-truncated multi-band ED, reaches N_k = 24-27 classically.**
   - I recomputed the dimensions (§4). The 2608.12452 truncation (14 band-2 k-points, 2 band-3 k-points, n2 <= 6, n3 <= 1) gives:

     | N_k | Dimension per momentum sector |
     |---|---|
     | 24 | 1.6e9 |
     | 27 | 1.2e10 |

   - The (17, 5, 6, 1) truncation gives 7.7e10 at N_k = 27.
   - Demonstrated Lanczos ED reaches 5e11 per sector for spin models (Läuchli, Sudan, Moessner, PRB 100, 155142 (2019) [V]). Momentum-space Coulomb ED is denser per row, but 1e10-1e11 is within reach.
   - The quantum target (27, 3, full) = 1.7e16 is therefore not the relevant comparator. The comparator is truncated ED at ~1e10, provided truncation convergence holds at 27 as it did at 21.

5. **Band-mixing NQS already exists at the relevant Hilbert-space sizes, in the sister system.**
   - Neural Transformer Backflow (Zhang & Luo, 2509.09275 [V]) is momentum-conserving and multi-band. It reaches:
     - 5×5, N_b = 2 (dimension 2.25e12);
     - 3×3 with N_b up to 5;
     - 6×6 with N_b = 1.
   - Its error is 3e-3 meV against 3-band ED at 3×3, and it resolves momentum sectors (tMoTe2).
   - Continuum NN-VMC with all bands and no truncation extracts FCI torus degeneracy from momentum decomposition (Abouelkomsan, Geier, Fu, PRB 113, 205119 (2026), 2512.01863 [V]). This was shown in a model system (periodic field, 8-9 particles in 24-27 cells).
   - Continuum NN-VMC for rhombohedral graphene exists as well (Abouelkomsan, Gaggioli, Guerci, Fu, 2608.00167 [V]). It uses a minimal Mexican-hat dispersion with no moire and N = 25 electrons, and finds only crystals.
   - No NQS for RnG/hBN at fractional filling was found. The transfer is an engineering step, not a method gap.

6. **Multi-band iDMRG is a demonstrated capability in the Landau-level-mixing analogue**, but has not been run on RnG/hBN.
   - Zaletel, Mong, Pollmann, Rezayi, PRB 91, 045115 (2015), 1410.3861 [V]: multicomponent iDMRG with LL mixing at 5/2.
   - Single-band moire iDMRG: Wang & Zaletel, 2507.07921 [V].
   - No multi-band RnG/hBN DMRG was found. Absence of evidence is not a wall (lesson: single-family failure is not a wall). Multi-band iDMRG is the natural tool if the FCI correlation length requires N_k >= 50, and cylinders handle that better than tori.

**The net classical position.**
- The T = 0 multi-band eigenvalue problem at N_k >= 27, untruncated, is not yet computed classically. In that narrow sense a wall exists, but it is an *unrun* wall, not a demonstrated one.
- The decision value does not lie inside it:
  - the primary yes/no is already provisionally answered (#1);
  - the secondary window sits in the parameter floor (#2);
  - the experimentally observed competition is thermal (#3).
- The round-1 cross-cutting lesson (i) and (iii) is reproduced in a new domain.

---

## 1. Strongest classical methods, demonstrated sizes and accuracy

| Family | Demonstrated on RnG/hBN or sister system | Size | Accuracy / notes | Source |
|---|---|---|---|---|
| 1-band ED (HF band) | R5G/hBN | N_k to ~27-30 | Uncontrolled. Sign and location of the FCI window differ from multi-band ED (1-band: FCI widest at V_val = 0, gap ~2 meV; multi-band: V_val >= 4 meV, gap ~0.3 meV) | 2608.12452 [V] |
| Multi-band ED, full | R5G/hBN, 3 conduction bands | N_k <= 18 (2e10 at (18, 3, 12) stated "beyond current resources" in 2504.20140) | Exact | 2407.13770 [V]; 2504.20140 [V] |
| Multi-band ED, occupation-truncated | R5G/hBN | N_k = 21, dimension ~1e9 | Truncation converges by n2 = 6 at N_k = 21 (authors' claim) | 2608.12452 [V] |
| Iterated ED (density-matrix natural orbitals) | R5G/hBN | N_k = 18 | "no major effect on the overlap with the exact states". Not a useful extension. | 2504.20140 [V] |
| HF / TDHF, all-band | R5G/hBN, many | Large | Gives the C = 1 parent. TDHF instability cured by V_val. Mean-field fails the twist-angle dependence of FCIs (2510.15309 [V], experimental paper's statement) | 2608.12452; 2510.15309 |
| HF + GW + RPA | R5G/hBN, MATBG | All-band | Claims quantitative agreement with experimental phase diagrams (integer fillings; specifics not in abstract) | Lu, Yang, Guo, Liu, PRB 114, L111108 (2026), 2509.19764 [V] |
| Momentum-space multi-band NQS (NTB) | tMoTe2 | 5×5 N_b = 2 (2.25e12); 3×3 N_b = 5; 6×6 N_b = 1 | 3e-3 meV vs ED at 3×3 N_b = 3. Momentum-resolved. | 2509.09275 [V] |
| Continuum NN-VMC (all bands) | Model FCI (periodic field) | 8-9 e in 24-27 cells | Topological degeneracy from momentum decomposition | 2512.01863 [V] |
| Continuum NN-VMC | RnG minimal model (no moire) | N = 25 | Crystal phases only; no FCI | 2608.00167 [V] |
| Variational FAHC wavefunctions + MC | R5G moireless | — | FAHC competitive with integer AHC and Fermi liquid; windows vs twist and D | Desrochers & Vishwanath, 2607.08822 [V] |
| iDMRG, single-band moire / LL + potential | LLL + periodic potential (tMoTe2/R5G-motivated) | Large cylinders | FCI to chiral SC / CDW near FCI melting | 2507.07921 [V] |
| iDMRG with LL mixing | GaAs 5/2 | Multi-LL | Demonstrates the multi-band iDMRG machinery | 1410.3861 [V] |
| AFQMC / CP-AFQMC | — | — | No fractional-filling moire Chern result found. The only QMC hit is sign-free DQMC at quarter filling (2210.11486) | arXiv API query Q10 |
| Multiband skyrmion-FCI theory (VMC + ED + EFT) | R-graphene | — | Argues the nu = 2/3 state is intrinsically multiband (skyrmion vacancies), so 1-band projection misses it | May-Mann, Tan, Ledwith, Shi, Devakul, 2608.14535 [V] |

## 2. Shortcuts for the observable

- **Light cones / Pauli propagation.** Not applicable. The output is static eigenvalues.
- **Perturbation theory (Schrieffer-Wolff / second-order band-mixing renormalisation), ablation arm (a).**
  - The non-interacting bands are gapless (2407.13770 abstract), so the conduction-band mixing has no small parameter at the one-body level.
  - The empirical fact is that truncation at n2 <= 6 converges at N_k = 21 (2608.12452). That means the remote-band occupation is *moderate*: not perturbative, but low-rank.
  - This favours selected-CI / truncated-ED and NQS over SW perturbation.
  - I therefore expect ablation (a) to *fail*. That is consistent with the 1-band vs multi-band window shift above. The strong ablation is (d), truncated ED, not (a).
- **Sum rules / cluster expansions.** No known exact shortcut for torus degeneracy or the many-body gap.
- **ML surrogates.** Kolmogorov-Arnold heuristic FCI predictors exist (2512.01873) but are trained on ED of lattice models. Not decisive.
- **The cheapest real shortcut is the parameter sweep itself.** If the gap sign flips within the V_val prior, the eigenvalue precision beyond the sign is not decision-relevant.

## 3. Do tensor networks win?

This has not been demonstrated for RnG/hBN at fractional filling with remote bands. The capability exists:
- multi-component iDMRG (1410.3861);
- single-band moire iDMRG (2507.07921).

If the multi-band FCI correlation length exceeds ~3 moire lengths, torus-based methods fail equally for QPE and ED, and cylinder iDMRG is the correct tool. Scope of this statement: no search result shows multi-band moire iDMRG failing.

## 4. Scaling variable and where classical methods fail

Dimensions were recomputed here with Python, math.comb, per momentum sector (/N_k), at nu = 2/3 (N_e = 2 N_k / 3).

| N_k | Full n_b = 3 | Truncated (14, 2, n2 <= 6, n3 <= 1) | Truncated (17, 5, 6, 1) | Scaled truncation (o2 = 2N_k/3, o3 = 5N_k/21; 6, 1) |
|---|---|---|---|---|
| 18 | 1.9e10 | — | — | — |
| 21 | 1.8e12 | 2.0e8 | 1.1e9 (matches 2608.12452 "up to 1e9") | — |
| 24 | 1.7e14 | 1.6e9 | 9.6e9 | 7.7e9 |
| 27 | 1.7e16 | 1.2e10 | 7.7e10 | 1.3e11 |
| 30 | 1.7e18 | 9.0e10 | 5.9e11 | 2.1e12 |
| 36 | 1.8e22 | 4.6e12 | 3.1e13 | 4.6e14 |

The same truncations with all N_k orbitals allowed (n2 <= 6, n3 <= 2) give:
- N_k = 21: 8.4e10 (the truncation-convergence check with no k-point restriction);
- N_k = 27: 5.7e13.

**Classical failure point, stated precisely.**
- Full multi-band ED fails at N_k ≈ 21 (1.8e12).
- Truncated ED at the published truncation fails at N_k ≈ 30-36 (9e10 to 5e12).
- This is not the same scaling variable as the quantum proposal's. The quantum advantage applies only if the truncation stops converging at N_k = 27-36, which has not been shown.
- The measurable proxy is G5: remote-band weight and overlap versus N_k.

**N_k needed by the FCI correlation length.**
- nu = 2/3 was "not converged ... even on the largest accessible systems" in the full multi-band ED (2407.13770).
- The gap of 0.1-0.3 meV is ~1-2% of the Coulomb scale, and the neutral gap is ~3 meV (2608.12452). The FCI is weak and sits near a window edge, so a long correlation length is expected there.
- If N_k >= 50-100 is required, torus QPE cost rises 10-100x (prefilter), while iDMRG handles the long direction natively.
- [ESTIMATE; no direct correlation-length measurement found.]

## 5. Model/parameter error vs solver error (G1)

| Floor source | Size | Effect on the decision |
|---|---|---|
| V_val estimate: 9 meV (direct) vs 12 meV (formula) | ±15% | Straddles the upper window edge (~10 meV) |
| hBN orientation 0° vs 180° | "markedly different" moire strength (2507.20647) | Moves V1 and hence V_val. Qualitative phase-diagram change |
| Lattice relaxation | "crucial" for the isolated C = 1 band (2605.16218) | Changes the one-body input |
| CN vs AVE valence reference | Qualitative (FCI destroyed vs strengthened, 2407.13770) | Not reduced by more conduction bands |
| 2D gate-screened vs 3D interaction | 2608.12452 drops the 3D part "for simplicity" | Unknown magnitude |

**Solver spreads, for comparison.**
- 1-band vs multi-band: large (2 meV gap vs 0.3 meV; window shifted by ≥4 meV in V_val). Already resolved classically at N_k = 21.
- Truncated vs untruncated multi-band at N_k = 27: unknown, and claimed converged at 21.

**Slope estimate.** The gap falls from 0.3 meV to 0 as V_val goes 7 → ~10 meV, a slope of ~0.1 meV/meV. The V_val uncertainty of ±1.5-3 meV therefore propagates to ≥0.15-0.3 meV of gap uncertainty, which is at or above the gap itself. **The model floor is at or above the relevant solver spread.** G1 fails unless the yes/no is invariant, and it is not.

The experimental twist-angle dependence (2510.15309) supports the same reading. FCIs need θ < ~1.1°, with 2/3 requiring smaller θ. The yes/no is parameter-dependent in nature too.

## 6. Is the decision-relevant information inside the wall? (round-1 lesson check)

**No.** Three regimes separate:

- **(a) Wall.** The T = 0 untruncated multi-band spectrum at N_k >= 27. Unrun rather than demonstrated.
- **(b) Decision value 1, "does the model support an FCI at all".** Provisionally answered classically at N_k = 21 (2608.12452). A reversal at N_k = 27 would matter scientifically. Truncated ED at N_k = 24-27 can test that classically at ~1e9-1e11.
- **(c) Decision value 2, the window and experiment.**
  - The window lies inside the parameter floor (§5).
  - The measured nu = 2/3 competition is FCI → generalized AHC / EQAH on *cooling* (2607.08710; 2408.10203), with an entropy-driven mechanism proposed (2609.16483). That is a finite-T free-energy question. T = 0 eigenvalues at ~0.01 meV resolution do not settle it, and the needed Gibbs or low-lying density of states reintroduces the thermal-state cost of round 1.
- **(d) Built devices.** Experiments are their own oracle. Transport, STM moire mapping (2510.09548, 2608.24684, 2608.12478; titles only) and nanoARPES (2504.06251, 2605.05199; titles only) now measure the one-body inputs directly. Decision value is therefore limited to unbuilt stacks (N = 4-7, orientation, θ), where the parameter floor is widest.

**Moireless AHC limit.** Not settled; it is an active question (2403.05522 [V], HF; 2607.08822 [V], variational). But alignment is not moot. The FCI "disappears in the absence of hBN alignment" (2608.12452), and FCIs show critical twist-angle dependence experimentally (2510.15309). This does not rescue N01, because it moves the decision into the moire-parameter floor.

## 7. Cheapest decisive classical kill experiment

Pre-registration is needed before running; this is the proposal only. Total cost is a single workstation-to-small-cluster budget, with no multi-band iDMRG needed for the kill.

**K1: floor vs truncation, at N_k = 21 and 24.**
1. Rebuild the R5G/hBN model of 2608.12452: 3 conduction bands, valence Hartree V_val, 2D gate-screened interaction.
2. Run truncated ED with (14, 2 / 17, 5; n2 <= 6, n3 <= 1) at N_k = 21 and 24. Dimensions are 2e8-1e10.
3. Sweep V_val over {6, 8, 9, 10, 11, 12} meV and the V1 amplitude ±20%.
4. Also run the truncation-convergence check at N_k = 21 with n2 <= 8 (1.3e11 with unrestricted k).
   - If that is too costly, use n2 <= 7 with the 17-orbital band-2 restriction.
5. **Kill rule.**
   - Let Δ_trunc be the shift of the gap sign / FCI window edge from truncation refinement plus the N_k 21 → 24 change.
   - Let Δ_param be the shift from the V_val / V1 prior.
   - If Δ_trunc < Δ_param, the solver spread that QPE could remove is below the model floor. **Kill N01 on lesson (iii).**
   - If Δ_trunc > Δ_param, go to K2.

**K2 (only if K1 does not kill): N_k = 27 truncated ED at 1.2e10-7.7e10, and remote-band weight vs N_k.**
- This is G5: the overlap² of the embedded 1-band state against N_k = 12, 15, 18, 21, 24.
- If the truncated ED gap sign at 27 matches 21 and 24, the primary yes/no is closed classically. **Kill.**
- If the remote-band weight grows so that the truncation stops converging, a wall exists at N_k >= 27. The resource audit (G3) then decides, with ε tightened to ~0.02-0.05 meV for a 0.1-0.3 meV gap.

**Independent of K1/K2 (literature-level, zero compute).**
- Lesson-(i) failure #3 already holds for the experimental comparison at nu = 2/3.
- If the orchestrator accepts that the finite-T entropy-driven FCI/AHC competition is the experimentally decisive quantity, N01 in its eigenvalue-only form is **killed now**. What would remain is a purely theoretical model-adequacy question with limited practical consumer value.

## 8. Does the hardness rest on a single method family?

Yes. The only documented failure is **exact ED on a torus** (2407.13770; 2504.20140). The other families have not been tried on this Hamiltonian:
- truncated ED beyond N_k = 21;
- momentum-space multi-band NQS (demonstrated in tMoTe2 at 2e12);
- multi-band iDMRG (demonstrated for LL mixing).

A single-family failure is not a wall. G2 is unresolved but tilts classical.

## 9. Novelty / scoop notes (for the novelty auditor)

- arXiv API query (Q13) combined phase estimation, fault-tolerant or qubitization with fractional Chern, Landau level, moire or FQH. It returned no FT resource estimate for FQH/FCI/moire Hamiltonians.
- Quantum-side items found were all state preparation or hardware demonstrations:
  - Rahmani et al. 2005.02399 (Laughlin circuit);
  - Voinea et al. 2309.04527;
  - Wu et al. 2606.16548 (Laughlin on sphere);
  - Xu, Lee, Tu 2608.05140 ("FQH factory", IBM Heron, 154 qubits).
- Novelty category B/C stands, scoped to that query.
- Scoop risk is high from the classical side, not the quantum side. The Bernevig/Regnault group has published three successive multi-band ED papers (2407.13770, 2504.20140, 2608.12452). The Fu and Luo groups have multi-band / continuum NQS (2509.09275, 2512.01863, 2608.00167). A multi-band NQS or DMRG treatment of RnG/hBN is a plausible next step for either group.

## 10. Verified experimental disagreement items (for prefilter §3.1(1))

**Zero-field FQAH in R5G/hBN.**
- Lu et al., arXiv:2309.17436 [V]; Nature 626, 759 (2024) as cited in 2608.12452.

**Finite-field-only FCI near nu = 2/3 in moire pentalayer.**
- Waters et al., PRX 15, 011045 (2025), 2408.10133 [V]. At zero field there are only correlated insulators and electronic crystals.

**EQAH at ~40 mK, with FQAH recovered at higher T or current.**
- Lu et al. (Ju group), 2408.10203 [V].

**Displacement-field-controlled FCIs and CDWs; nu = 1/3 down to 0.2 T.**
- Aronson et al., PRX 15, 031026 (2025), 2408.11220 [V].

**Tunable FCIs in R6G/hBN.**
- Xie et al., 2405.16944 [V]. A Hall-sign-reversing QPT with nu = 2/3 surviving.

**Critical twist-angle dependence; "mean-field ... does not explain".**
- Huo et al., 2510.15309 [V].

**hBN orientation (0° vs 180°) controls moire strength.**
- Uzan et al., 2507.20647 [V].

**Additional R4G/R5G/tRMG items, verified at title level only (listing in Q12):**
- R4G (tetralayer) FQAH / superconductivity: Choi et al. 2408.12584 [title V].
- 1/3 FQAH and gapless integer QAH in R5G: Butler et al. 2606.06450 [title V].
- FQAH-insulator phase transitions in R5G: Hadjri et al. 2609.09422 [V].
- Stacking-orientation / twist control: 2505.01767 [title V].

**FCI → generalized AHC below ~150 mK, as a bulk transition.**
- H. Li et al., 2607.08710 [V abstract]. Full text 404 on the HTML route.

## Query log (all through WebFetch; WebSearch not used)

| Q | Source | Query / URL | Result |
|---|---|---|---|
| Q1 | arXiv abs | 2608.12452 | abstract |
| Q2 | arXiv HTML | 2608.12452 (×3 prompts) | N_k = 21; truncation; V_val window; gaps |
| Q3 | arXiv abs | 2504.20140 | abstract |
| Q4 | arXiv API | abs:rhombohedral AND graphene AND fractional AND (DMRG OR neural OR "Monte Carlo") | 2607.08822, 2507.07921 |
| Q5 | arXiv API | (pentalayer OR rhombohedral) AND ("band mixing" OR "remote bands" OR DMRG OR neural) | 13 hits incl. 2608.00167, 2512.21609, 2311.04217 |
| Q6 | arXiv abs/HTML | 2608.00167; 2607.08822 | — |
| Q7 | arXiv API | neural AND ("fractional Chern" OR "fractional quantum anomalous" OR "anomalous Hall crystal") | 10 hits incl. 2509.09275, 2512.01863, 2605.20326, 2604.08702, 2512.07947 |
| Q8 | arXiv abs/HTML | 2509.09275; 2512.01863 | — |
| Q9 | arXiv API | DMRG AND ("fractional Chern" OR FQAH) AND (moire OR graphene OR MoTe2) | 2507.07921, 2507.07611, 2112.13837 |
| Q10 | arXiv API | (auxiliary-field OR AFQMC OR "quantum Monte Carlo") AND (moire OR rhombohedral) AND (Chern OR "anomalous Hall") | 2210.11486 only |
| Q11 | arXiv abs | 2407.13770 | — |
| Q12 | arXiv API | rhombohedral AND graphene AND (FQAH OR "fractional Chern"), 40 newest | 37 hits (experiments and theory 2024-2026) |
| Q13 | arXiv API | (phase estimation OR fault-tolerant OR qubitization) AND (fractional Chern OR Landau level OR moire OR FQH) | no FT resource estimate |
| Q14 | arXiv abs | 2408.10133, 2408.10203, 2408.11220, 2405.16944, 2309.17436, 2510.15309, 2507.20647, 2609.09422, 2607.08710, 2609.16483, 2608.14535, 2605.16218, 2509.19764, 2512.15041, 2403.05522, 1410.3861, 1611.06990 | verified |
| Q15 | arXiv HTML | 2504.20140 | N_k = 18; iteration ineffective |
| Q16 | arXiv HTML | 2607.08710 | HTTP 404 |
| Q17 | local | Python dimension counts (§4) | — |

## Citation status

- [V] = abstract page fetched this session.
- The details attributed to 2608.12452, 2504.20140, 2509.09275, 2512.01863 and 2608.00167 come from HTML full-text extraction by a summarizing fetcher. Exact numbers should be re-checked against the PDF before being quoted in a final report.
- One inconsistency: the 2512.01863 extraction reported an NN energy (−39.245) *above* single-band ED (−39.346) while calling it "outperforming". That number is treated as [UNRELIABLE EXTRACTION].
- Items marked [title V] were seen only in the arXiv API listing.
