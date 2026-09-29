# Round 2 selection: ranking of round-2 audited candidates for slots 2-3

Date: 2026-09-28. Role: round-2 selection lead. Status: FINAL for round 2.

**Inputs:**
- `audit_N01_novelty.md`, `audit_N01_classical.md`, `audit_N01_resources.md`: the only round-2 audits.
- `round2_prefilter.md`: sharpened N01 spec, and the drop register for C02, C14R, C15, C17, C19, C32, C34.
- `round2_discovery_static_inside_wall.md` (S-M1 = N01; K-S1..K-S17).
- `round2_discovery_short_time_dynamics_inside_wall.md`: zero survivors.
- `selection.md`: round 1; C01 holds slot 1, conditional.

**Scope of claims.**
- Nothing here is an experimental result.
- Costs are the auditors' order-of-magnitude estimates. The N01 lambda values come from a real SWMcC+hBN form-factor computation in the resource audit's scratchpad (not a repo file). C_W is formula-based, not compiled.
- Novelty statements are scoped to the auditors' arXiv API / arXiv HTML / Crossref queries through 2026-09-28. OpenAlex and Semantic Scholar returned HTTP 429, so cited-by could not be checked.
- "Not found" is not proof of absence.

## 0. Bottom line

**Slots 2 and 3 stay empty. N01 is ranked 1st of one and marked `eligible = false`. I did not lower the bar.**

N01 is the best-matched quantum mechanism the program has audited in either round:
- the output is eigenvalue-only;
- there is no Gibbs state and no linear-response shot noise;
- trial states are cheap, with an overlap^2 pilot of 0.87-0.90, extrapolating to 0.67-0.75 at N_e = 18;
- one (27,3) rung costs S*G ~ 2e12.

Round-1 lesson (ii), that cost is dominated by preparation and sampling, is therefore **fixed** here. Lessons (i) and (iii) come back in full:

1. **The decision is not inside the wall.**
   - The primary yes/no ("does the explicit-remote-band model support a gapped nu = 2/3 FCI anywhere in the prior?") is already answered "yes" at the ED scale: Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, arXiv:2608.12452, 21 sites, occupation-truncated, Hilbert space ~1e9.
   - The secondary window lies inside the parameter floor.
   - The experimentally observed nu = 2/3 competition is at finite temperature and entropy-driven:
     - FCI -> generalized AHC below ~150 mK (2607.08710);
     - EQAH at ~40 mK (2408.10203);
     - entropy mechanism proposed (Kim & Kivelson 2609.16483).
     T = 0 torus eigenvalues do not settle it.
2. **The wall is single-family and unrun.** Only full torus ED is documented to fail. Other families have not been run on this Hamiltonian, and they do not fail where it does:
   - occupation-truncated ED reaches N_k = 24-27 (1e9-1e11 per sector);
   - multi-band NQS (NTB, 2509.09275) is demonstrated at 2.25e12 in tMoTe2;
   - multi-component iDMRG exists for LL mixing (1410.3861).
3. **Model floor >= solver spread.**
   - The realistic moire-capacitor V_val is 9-12 meV. That sits at or past the ~10 meV upper edge of the 4-10 meV FCI window.
   - The gap slope is ~0.1 meV/meV. The V_val uncertainty therefore propagates to >= 0.15-0.3 meV of gap, which is the size of the gap itself (0.1-0.3 meV).
   - hBN orientation (0 vs 180 deg; 2507.20647), lattice relaxation (2605.16218) and the CN/AVE valence reference (qualitative; 2407.13770) all add to the floor. More conduction bands do not remove any of these.
4. **Cost is marginal for a decision-grade answer.**
   - One rung passes (2.1e12; bracket 6e11-2e13).
   - The convergence ladder needed for a decision is ~3e13 (bracket 1e13-3e14), 1-3x over the screen.
   - The phase map (3e14-1.5e15) fails.
   - N_k ~ 100 fails (~6e13 per rung), if the FCI correlation length requires it.

**Combined with round 1, the program has one conditional finalist (C01) out of the 50-entry round-1 pool plus the round-2 lenses (17 static target families, the short-time lens and N01), over two rounds.** The brief asked for exactly three. Three cannot be delivered at the stated bar from the audited material. The honest output is one conditional slot, plus a documented, scoped negative for everything else.

## 1. Ranking

| Rank | ID | Sharpened formulation (after audits) | Audits (novelty / classical / resources) | Eligible |
|---|---|---|---|---|
| (slot 1, round 1) | C01 | Correlated thermal S_ee(q,w) of partially degenerate H, r_s ~ 2, theta 0.25-0.5, XRTS wavevectors; UEG validation rung | wounded / wounded / wounded; red team: conditional on 4 gates | yes, conditional (not re-ranked here) |
| 1 | N01 | Re-scoped: N_k / n_b convergence of the 2608.12452 moire-capacitor nu = 2/3 multi-band FCI in R5G/hBN (N_k 27 -> 36, n_b 3 -> 5, untruncated), plus nu = 3/5 and 2/5 under the same model, plus E_FCI vs E_AHC/EQAH vs skyrmion-FCI on commensurate tori, at 3-5 fixed V_val points spanning the prior. See 2.1. | wounded (B) / wounded, leaning kill / wounded (single rung passes G3) | **no** |

The round-2 prefilter dropped C02, C14R, C15, C17, C19, C32 and C34 before audit, each for a named filter failure (`round2_prefilter.md`, section 4). None was audited, and none is re-ranked here. I found nothing in the N01 audits that changes those drops. The short-time dynamics lens returned zero candidates.

## 2. Sharpening and rationale

### 2.1 N01: multi-band FCI / CDW / AHC competition in hBN-aligned rhombohedral graphene (not eligible)

#### What the audits changed in the spec

1. **The primary output as written is no longer open.**
   - 2608.12452 (Aug 2026) finds a multi-band nu = 2/3 FCI "stabilized by inter-band fluctuations".
   - Scope of that result: 21 sites, occupation caps n2, n3 <= 6, V_val ~ 4-10 meV, gap ~ 0.1-0.3 meV. The authors state they are "unable to access larger systems".
   - The only non-cosmetic residuals are:
     - (i) convergence in N_k (27, 36) and in untruncated n_b;
     - (ii) the Jain sequence 3/5, 2/5 under the same model;
     - (iii) same-model energetics of FCI vs AHC/EQAH vs the skyrmion-FCI mechanism (May-Mann et al. 2608.14535).
   - These are a *confirmation or refutation of a published classical claim*, not a new design decision.
2. **The G0 ablation arm (a) likely fails, and that favours N01.**
   - The one-body-only single-band calculation with the capacitor term gives a CDW, not an FCI, at 21 sites. This is the novelty auditor's HTML reading of 2608.12452; it is flagged for PDF confirmation.
   - The strong ablation is therefore (d): occupation-truncated ED, which reaches N_k = 24-27. The quantum comparator is not full ED at 1.7e16; it is truncated ED at 1e10-1e11. A quantum advantage needs the truncation to stop converging, and nobody has shown that.
3. **G3 is refuted in the pessimistic direction, and the target is still marginal.**
   - With real form factors, Sum_Q V_Q/A drops from 557 to 130 meV.
   - Block-encoding normalisation lambda: DF 3.2e4 meV; first-quantized band basis 2.0e4 meV; DF with spectrum amplification ~8.6e3 meV. lambda is robust (+-40%) across the parameter prior.
   - The prefilter's 7e5-1.3e6 meV bound was too high.
   - Per-state-point cost is fine. The cost that matters is the decision-grade convergence ladder (~3e13).
4. **Decision value is confined to unbuilt stacks or to telling mechanisms apart.**
   - Built devices are their own oracle. Alignment and twist windows are now measured directly (2510.15309, 2507.20647, 2505.01767, 2608.24684).
   - Unbuilt stacks are exactly where the parameter floor is widest.

#### Refined problem (the most defensible form)

- **INPUT.**
  - The 2608.12452 R5G/hBN model: SWMcC hoppings; hBN moire V1 and phase; moire-capacitor valence Hartree V_val; dual-gate screened Coulomb.
  - V_val on a fixed grid {6, 8, 9, 10, 12} meV and V1 +-20%. These are sweep points, not fitted values.
- **COMPUTE.** Low-lying eigenvalues in each momentum sector:
  - N_k = 27 with n_b = 3, 4, 5 (untruncated);
  - N_k = 36 with n_b = 3, 5;
  - flux insertion at 3 points;
  - fillings nu = 2/3, 3/5, 2/5.
- **OUTPUT.**
  - (a) For each V_val point: whether the torus-degenerate FCI gap is converged and its sign.
  - (b) E_FCI - E_AHC/EQAH, using HF / crystal trial states on commensurate tori.
  - (c) Whether the capacitor-plus-band-mixing FCI and the skyrmion FCI are the same ground state.
- **VALIDATION.** Exact agreement with multi-band ED at N_k <= 18-21 (n_b = 3), and with truncated ED at 21.
- **FULL vs ABLATION.** FULL is QPE/QCELS in the untruncated space. ABLATION is the best of:
  - truncated ED at N_k = 24-27 (the strongest arm);
  - NTB-type momentum-resolved multi-band NQS;
  - multi-band iDMRG;
  - Schrieffer-Wolff three-body-renormalized single-band ED.
- **Claim category.**
  - 3 against exact ED only (narrowly, at N_k >= 21 with n_b = 3).
  - 1 (certification) against truncated ED / NQS / iDMRG, unless they fail or disagree at a named point.

#### Quality-bar check

| Criterion | Status | Evidence |
|---|---|---|
| Practical use | Weak | Consumer: FQAH / non-Abelian device research. Built devices are self-oracles. Only unbuilt stacks remain (R7G+, double alignment, other substrates). |
| Concrete input -> output | Pass | See the refined problem above |
| Multi-family classical wall with the decision inside it | **Fail** | Only one family (full torus ED) fails. Truncated ED, NTB NQS and iDMRG are unrun, not failed. The yes/no is already answered at 21 sites. The experimental competition is finite-T and entropy-driven. |
| Matched quantum mechanism | Pass (strongest of both rounds) | Eigenvalue-only QPE; overlap^2 ~0.7 extrapolated (pilot, CN-like, small clusters); no Gibbs state |
| S*G <~ 1e13 | Marginal fail for a decision | 2.1e12 per rung; ~3e13 per decision-grade ladder; 3e14-1.5e15 per map; ~6e13 per rung if N_k ~ 100 |
| Measurable comparison | Pass, narrow | Against ED at <= 21 sites; against truncated ED at 24-27 |
| Scalable benchmark | Pass | N_k at fixed n_b; n_b at fixed N_k |
| Novelty B/C | Pass | B for this problem; C for the FQH family. No FT/QPE costing of any interacting moire / FCI / FQH / LL Hamiltonian was found (scoped). |
| Model floor below solver spread (round-1 filter) | **Fail** | V_val and orientation straddle the window edge; the gap uncertainty is >= the gap; the CN/AVE spread is qualitative |

**Two hard fails (wall with the decision inside it; floor) plus a marginal cost fail make N01 ineligible.** The failures are structural, not a matter of missing audit work. Even the best outcome of the pending classical tests leaves a question whose answer is parameter-dependent.

#### What would make N01 eligible (reopen conditions; all classical and cheap)

The chain is K1 -> K2 -> G2 -> G4, run in that order. Each step requires the previous one.

1. **K1 (pre-register first).** Run truncated ED at N_k = 21 and 24 (dimension 2e8-1e10) over the V_val / V1 prior, with truncation refinement to n2 <= 7-8.
   - Needs Δ_trunc > Δ_param: the shift in window edge or gap sign from truncation plus the N_k change must exceed the shift from the parameter prior.
2. **K2.** At N_k = 27, truncated ED (1.2e10-7.7e10) must *fail to converge* in the truncation, or flip the gap sign relative to 21/24. Use remote-band weight and overlap versus N_k (G5) as the proxy.
3. **G2.** NTB-type NQS and/or multi-band iDMRG on R5G/hBN must disagree with each other, or with truncated ED, at a named (N_k, V_val) point.
4. **G4.** The disagreement must change a stated prediction for an unbuilt stack, or discriminate the capacitor mechanism from the skyrmion mechanism, *and* that prediction must be invariant across the parameter prior.

If K1 fails its test (Δ_trunc < Δ_param), N01 is killed on lesson (iii) and should go into `research/KILLBOOK.md` when the state files are next updated. The classical auditor judges K1 the likely outcome.

#### Why it is still worth recording

- The first fault-tolerant resource estimate for an interacting moire / FCI continuum Hamiltonian is publishable as a *resource study*, category 3 against exact ED only. Its content: real form factors; lambda for DF, first-quantized band basis and spectrum amplification; QCELS for quasi-degenerate torus multiplets and flux insertion; validation against ED at <= 21 sites.
- K1/K2 are publishable as classical science whatever the quantum outcome.
- Neither is an advantage slot.
- Scoop risk is high on both sides:
  - classical: the Bernevig/Regnault multi-band ED series (2407.13770 -> 2504.20140 -> 2608.12452 -> 2608.23675); the Fu/Luo NQS groups;
  - quantum: the Rubin/Babbush/Low group, which already has Bloch-orbital DF/THC (2302.05531) and spectrum amplification (2502.15882).

## 3. Qualitative comparison table

The descriptors are qualitative, and there is no single score. C01 is included as the slot-1 reference. It is not re-audited here, and its entries are taken from `selection.md` and the red-team notes. N01 is scored in its re-scoped form (section 2.1).

| Dimension | C01 WDM S_ee(q,w), theta 0.25-0.5 (slot 1, conditional) | N01 multi-band moire FCI convergence (re-scoped) |
|---|---|---|
| Novelty evidence (scoped) | B, but thin: Sandia has publicly announced WDM linear-response work | B for this problem; C for the FQH family. No FT/QPE costing of any interacting moire / FCI / FQH / LL Hamiltonian found; NISQ state preparation and VQE only (2607.11380, 2608.05140, ...) |
| Classical difficulty | Named wall: every exact PIMC variant fails at theta <= 0.5; one approximate family remains, and it is unvalidated | Unrun wall: full ED fails beyond N_k ~ 18-21, but truncated ED reaches 24-27. NQS (2e12 in tMoTe2) and iDMRG are untried here. Single-family failure only |
| Decision inside the wall? | Unresolved: gates K-C01a (ITCF information) and K-C01b (multi-family spread) | No. The yes/no is answered at 21 sites; the window is in the floor; the observed competition is finite-T |
| Quantum mechanism strength | Exponential against exact finite-T fermion dynamics, polynomial against TDDFT. Correlated thermal preparation is unsolved (8-16% T bias from Mermin preparation) | The strongest match in either round: eigenvalue-only QPE/QCELS; cheap trial states with overlap^2 ~0.7; no Gibbs state. Exponential only against exact ED |
| Practical importance | High: ICF/HED diagnostics (NIF, LCLS, EuXFEL) | Low-moderate: condensed-matter physics and FQAH device research; unbuilt stacks only |
| Benchmarkability | Excellent: exact UEG Laplace check against PIMC F(q,tau) | Good: exact multi-band ED at <= 18-21; truncated ED at 24-27 |
| Scaling potential | eta 32 -> 256; theta 1 -> 0.25 | N_k 27 -> 36 -> 48; n_b 3 -> 5. The required N_k is unknown (a long correlation length is possible) |
| Resource feasibility | UEG rung 4e13-9e14 (later FT); practical H 1e17-1e19 | Rung 2e12 (passes); decision ladder ~3e13 (1-3x over); map 3e14-1.5e15 (fails); ~1e6-3e6 physical qubits |
| Model floor vs solver spread | Low Hamiltonian floor (bare Coulomb); the thermal-preparation bias is the floor-like term | Floor >= spread: V_val 9-12 meV vs a window edge at ~10 meV; orientation; relaxation; CN/AVE |
| Classical-adversary risk | Moderate-high: PIMC variants advancing; ITCF redundancy | High: truncated ED, NTB NQS transfer and multi-band iDMRG are each an engineering step away |
| Literature saturation | Classical side dense; quantum side empty but about to be occupied | Classical side very active (multi-band ED every few months; four experimental groups); quantum side empty |
| Publication potential | High in any outcome: information-gain analysis, classical multi-family map, UEG resource estimate | Moderate: the first FT resource estimate for a moire FCI Hamiltonian (category 3 vs ED), plus K1/K2 classical convergence results; not an advantage paper |

## 4. Round-2 cross-cutting finding (scoped to the two round-2 lenses and the N01 audits)

Round 2 was designed to fix round-1 lesson (ii), and for N01 it did: eigenvalue-only output, cheap trial states, per-rung S*G ~ 2e12. Lessons (i) and (iii) then showed up in a sharper form:

- **A phase competition is hardest classically near the phase boundary.** That is where the competing energies are nearly degenerate, the correlation length is long and truncations converge slowly.
- **The same place is where the answer is most sensitive to the Hamiltonian's parameters.** At the boundary, the decision's derivative with respect to the parameters is largest, and the answer flips inside the parameter prior. The Hamiltonians where eigenvalue-native QPE is cheap here are engineered 2D flat-band models, and those are specified only to ~10-30%.
- **So for static phase-competition targets, solver hardness and model-floor sensitivity peak together.** Removing solver error does not settle the decision unless the parameter prior is narrower than the width of the critical region.

Proposed filter for any round 3 (a recommendation, not a result): before audit, require an explicit **floor-to-spread ratio**. That is (∂ decision / ∂ parameters) x (prior width), divided by the classical solver spread, evaluated at the proposed state point. It must be < 1.

The ratio can be estimated classically at small size. For N01 it can be read from 2608.12452's own V_val window: it is >= 1.

The static lens's trilemma (`round2_discovery_static_inside_wall.md`, section 0) says that targets with exact Hamiltonians either have no practical decision or have a disorder floor. Taken together with the point above, I do not expect a round 3 over the same static / low-T / real-frequency space to fill slots 2-3 at this bar. This is a forecast from 2 rounds, the 50-entry pool plus the round-2 lenses, and 21 audits. It is not a proof.

## 5. Recommendation to the orchestrator

1. **Final answer to the brief: one conditional slot (C01). Slots 2 and 3 are empty, by decision rather than by omission.**
   - Report the scoped negative. Every other candidate failed the bar for a named, recorded reason (see `selection.md` section 1, `round2_prefilter.md` section 4, and section 2.1 here).
   - Do not promote N01 or any round-1 residual (C14R, C44, C41). Each would need a category-1-only claim or an unmeasured decision flip.
2. **C01 gates remain the priority:** K-C01a (information), then K-C01b (multi-family), then thermal-preparation bounding. Each must be pre-registered.
3. **N01 is parked, not killed.**
   - Record it as WOUNDED, with reopen conditions K1 -> K2 -> G2 -> G4 (section 2.1).
   - If the program has spare classical capacity, K1 is cheap: truncated ED at dimension 2e8-1e10, workstation scale within the compute policy. It is decisive either way, and it must be pre-registered in `experiments/preregistered/` before running.
   - If K1 fails its test, move N01 to `research/KILLBOOK.md` with reason: "model floor >= solver spread; decision (finite-T, entropy-driven) outside the T = 0 eigenvalue wall".
4. **When the state files are next updated:**
   - Add the section-4 finding to `research/SCIENTIFIC_MEMORY.md`. Hardness and parameter sensitivity peak together at phase boundaries, and a floor-to-spread ratio < 1 is required.
   - Add the finite-T question for N01 to `research/OPEN_QUESTIONS.md`. The question: is the experimentally decisive nu = 2/3 quantity a free-energy difference?
   - Record the corrected lambda for moire continuum models: 2e4-3e4 meV at M = 81, not 1e6.

## 6. Local work log

- Read all three N01 audits, `round2_prefilter.md`, `selection.md`, and the structure and bottom line of `round2_discovery_static_inside_wall.md`.
- No new literature searches or computations were run for this selection. All numbers are quoted from the audits with their stated brackets.
- Items the audits flagged for PDF confirmation remain flagged:
  - the 2608.12452 n2 = n3 = 0 CDW result, and its truncation and gap numbers;
  - the 2512.01863 energy comparison, marked unreliable extraction.
