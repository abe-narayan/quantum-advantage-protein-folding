# Round 3 completeness critic

_2026-09-28. File: `research/experiments/ROUND3/CRITIC.md`. Scripts and outputs: `research/experiments/ROUND3/critic/`
(`critic_checks.py` → `critic_checks.json`)._

**Scope.** I checked the 9 lane reports, the 6 verifier verdicts and `SYNTHESIS.md` against the repo state files
(`CURRENT_STATE`, `KILLBOOK` K-101 to K-105, `ADVANTAGE_CONDITIONS`, `BREAK_EVEN`, `R1_SYNTHESIS`). The question was
what the round missed: an adversary, a literature line, a physical effect, a statistic, or an over-claim.

**Tags.** MEASURED / DERIVED / THEORETICAL / LITERATURE-SUPPORTED / INFERENCE / UNPROVEN. **[CRITIC-C1]** and
**[CRITIC-C2]** mark my two checks. **[CRITIC-D1]** marks a derivation I added.

**Compute.** Under 1 CPU-s: analysis of JSON files already on disk, no new dynamics. 7 arXiv API/abs fetches. Nothing
was touched outside `ROUND3/critic/` and this file. No commit.

---

## 0. Bottom line

1. **No verdict flips toward a quantum advantage.** The round-3 headline stands: no quantum advantage for protein
   structure in any examined regime. But the stated reasons behind three kills and two headline sentences are wrong
   or over-reach, and the one open residue is being tested in the wrong time window.
2. **[CRITIC-C1] A headline MEASURED statement is not supported.** The synthesis (§3.2) says: "Inside the physical
   reversal horizons, NMR forward models are reproduced classically [MEASURED]". For OTOC(1) at converged cluster
   size this is **UNRESOLVED**, not measured.
   - At 40–120 µs, i.e. inside T3, all 24 probe/site/time series show the finite-cluster exact echo at N = 18 sitting
     **3.1–8.2 σ** from the verifier's own infinite-N hybrid estimate. This holds even though the step statistic
     |F₁₈ − F₁₆| < σ passes on 19 of 24.
   - The hybrid classical estimator (classical spin dynamics for H plus exact X) is not validated there either. X is
     flat over two consecutive N-steps on only 2 of 24 series, and the H error budget alone is 0.6–1.6 σ.
   - So the step-rule flaw (C10) applies to the early window too. It also applies to R1's "σ-cone of 16–20 spins at
     40 µs [MEASURED]".
3. **Consequence for kills.**
   - The reversal-horizon arm of **K-105** and the twin arm of **K-109** were both fixed against N = 10 finite-cluster
     models. They should be downgraded to "N = 10-conditioned".
   - Both kills still stand, but on their value / forward-model-error arms. Those arms are the load-bearing evidence
     and should be named as such.
4. **[CRITIC-C2] K-111 (methyl rotors) was killed for the wrong reason.**
   - "< 0.1 µeV = unobservable" uses the resolution of backscattering INS only. At V3 = 100 meV the dressed splittings
     reach 13 MHz, which is a frequency range for NMR-type tunnelling spectroscopy.
   - The kill survives on **identifiability**. The many-body correction (mean-field error of 13–40%) is equivalent to
     a barrier shift of only 1.7–2.7 meV, which is degenerate with the unknown per-methyl barrier itself.
5. **[CRITIC-D1] The "two-sided thesis" in synthesis §3 is over-generalised.** The thesis is: structure-bearing
   computation is classically easy, and classically hard computation is structure-free.
   - It is true for learned-energy structure prediction.
   - It is not true for physics-based all-atom sampling of folding kinetics and ensembles. That task is both
     classically hard and structure(-ensemble)-bearing, and round 3 never examined it.
   - With the lane's own generalised floor, ms-scale folders (about 1e11–1e12 MD steps) exceed B*₄ = 2e10–4e11. An
     s = 4 algorithm would therefore break even in principle there, at 0.1–2.5 years of quantum wall-clock per
     independent sample.
   - The kill in that regime rests on two things: no super-quadratic algorithm is known (A3/A4), and T*_Q is
     years-scale. It does not rest on classical ease. The thesis must be restated accordingly (§2.5, O-1).
6. **R1-SIM-X is aimed at a physically empty window.** Every T-X decision number in synthesis §2.2 is at 160–320 µs,
   which is 13–40 T2 and beyond T3. The only version of the question that touches a measurable signal is t ≤ T3
   (40–120 µs), and C1 shows that version is open. The natural adversary there, spinDMFT, which works directly in
   the thermodynamic limit, has still not been run. Recommendation §4, A-1/A-2.

---

## 1. Checks run

### C1. Early-window (t ≤ T3) convergence audit of the dipolar echo [CRITIC-C1]

**Inputs.** `r1sim_exact_reach/verify_classical/verify_summary.json`:
- exact H and floor at N = 12–20;
- F and X at N = 12–18 for t ≤ 120 µs;
- the verifier's classical-spin-dynamics H_∞ with the exact−CSD offset and its standard error;
- the verifier's hybrid estimate F_∞ ≈ H_∞ + X_last.

I used the verifier's estimator unchanged.

**Why these times.** T3 in physical units is 30–70 µs from the physics-feasibility lens (T3 ≈ 4–6.7 T2 with network
T2 = 8–11 µs) and at most about 123 µs under the relevance verifier's most generous convention. 40 µs is inside every
estimate; 80–120 µs is inside only the generous one.

| Quantity (24 series: 2 probes × 4 sites × t = 40, 80, 120 µs; N_last = 18) | Result |
|---|---|
| Step statistic \|F₁₈ − F₁₆\| < σ = 0.01 ("looks converged") | 19/24 (8/8 at 40 µs) [MEASURED, from files] |
| F₁₈ − F_∞(hybrid) | **+0.031 to +0.082, i.e. 3.1–8.2 σ; 24/24 series > 3σ** [MEASURED + INFERENCE: F_∞ is an estimate] |
| Exact finite-cluster floor at N = 18 (b-independent, → 0 as N → ∞) | 0.029–0.045 (2.9–4.5 σ) [MEASURED, exact] |
| X flat (\|dX\| ≤ 0.005) on two consecutive N-steps | **2/24** (p19, 40 µs, sites 1 and 9). The verifier's own looser flag gives 5/24 [MEASURED] |
| p245, 40 µs: dX(16→18) at sites 1/7/8/9 | +0.0076 / +0.0102 / +0.0075 / +0.0073. This common-mode shift is the b-independent H + floor drift leaking into X, the same cancellation as C2 in the synthesis [MEASURED; interpretation INFERENCE] |
| Hybrid H error budget √(se² + offset²) | 0.006–0.016 (0.6–1.6 σ) before any X error [MEASURED] |

**Reading.**
1. **Finite clusters are not σ-accurate forward models of the macroscopic echo.** Inside the reversible window, the
   exact finite-cluster echo at N ≤ 18 carries a conserved-charge floor of about (1 − H)/N ≥ 3σ, plus an unconverged
   two-point H. Both are invisible to a step statistic because they change by only 0.002–0.005 per ΔN = 2 [DERIVED
   from the table].
2. **R1's "σ-cone 16–20 spins at 40 µs" was a step-convergence statement.** It inherits the C10 flaw and does not
   mean exact simulation reaches the physical echo at 40 µs [INFERENCE].
3. **The relevance verifier's argument that the observable window (≤ T3) is within exact reach is unsupported.**
   Nor does C1 show the opposite. Whether a σ-level classical estimator exists at t ≤ T3 is **UNRESOLVED**.
   - The two missing pieces are X convergence and a tighter H_∞.
   - Both are cheap to settle (§4, A-1).
4. **What still carries K-105 and K-109.**
   - (a) Forward-model error: 5–66 σ from methyl rotation, site offsets and reversal mismatch (R1_physics_feasibility,
     MEASURED at N = 10). This is independent of N, and C1 adds a further finite-size floor for any cluster model.
   - (b) The value accounting: joint gain ≤ 3 even with ideal reversal (R1 value lens), and ≤ 1.42 for DQ.
   - (b) was computed at N = 10. At converged size the "classically usable" window could shrink, which would raise g.
     So (a), not (b), is the robust arm [INFERENCE].

### C2. Methyl-rotor observability, re-derived from the lane's own numbers [CRITIC-C2]

**Inputs.** `new_mechanisms_A/t2_methyl_rotor/summary_t2.json`. Conversion: 1 µeV = 241.8 MHz.

| V3 (meV) | Dressed pair splittings | max \|J\| (non-additive coupling) | Median mean-field error of Δ | d ln Δ / dV3 | Equivalent barrier shift of that error |
|---|---|---|---|---|---|
| 30 | 0.33 MHz – 19 GHz | 15 MHz | 40% | 0.124 /meV | **2.7 meV** |
| 60 | 1 kHz – 0.53 GHz | 30 kHz | 21% | 0.091 /meV | **2.1 meV** |
| 100 | 2.4 Hz – 13 MHz | 49 Hz | 13% | 0.075 /meV | **1.7 meV** |

[DERIVED from MEASURED model outputs]

**Reading.**
1. **Kill clause (i) was mis-specified.** It compares splittings with backscattering-INS resolution (0.1–1 µeV =
   24–240 MHz). The MHz-scale splittings at 80–100 meV fall in the frequency range of NMR-detected rotational
   tunnelling at cryogenic temperature.
   - LITERATURE: recalled field-cycling/level-crossing NMR tunnelling spectroscopy, not verified this session.
   - One verified arXiv abstract, cond-mat/0701201 (²H NMR of glassy aspirin), reports rotational tunnelling
     signatures below 20 K.
   - The splittings are not unobservable as a class.
2. **The kill survives on a stronger ground [INFERENCE].** The many-body information is a 13–40% change in Δ. That
   is equivalent to shifting that methyl's one-body barrier V3 by 1.7–2.7 meV (0.04–0.06 kcal/mol). V3 is itself an
   unknown nuisance per methyl, and protein-glass disorder spreads it further. So the many-body part is
   **non-identifiable** against the one-body barriers unless V3 is known a priori to well under 2 meV.
3. **Required change.** Re-base K-111 on identifiability / nuisance profiling instead of observability. The R-ROTOR
   residue keeps the same kill criterion, plus: "profiled many-body information ≥ 10% after V3 nuisances are fitted".

### D1. Generalised floor for a physics-based all-atom comparator [CRITIC-D1]

I used the hardness lane's formula unchanged: X = AρK n_b G t_T / c, B*_s = X^{s/(s−1)}, T*_Q,s = K n_b G t_T · X^{1/(s−1)}.
- Overheads: MO (K = 10, n_b = 1, A = ρ = 1), t_T = 1 µs.
- Lane cross-check at A80 L = 100 (G = 9.3e7, c = 1.6 ms): B*₂ = 3.4e11, in line with the lane's 2.6e11 [DERIVED].
- All-atom explicit solvent, about 3e4 atoms on one GPU [INFERENCE for all inputs]:
  - G = 1e9–1e10 Toffolis per coherent force evaluation (about 300 cutoff neighbours × 1e2–1e3 Toffolis per pair term,
    PME ignored);
  - c ≈ 0.2 ms per MD step.

| Scenario | X | s = 2: B* / T*_Q | s = 3: B* / T*_Q | s = 4: B* / T*_Q |
|---|---|---|---|---|
| All-atom, optimistic G = 1e9 | 5e7 | 2.5e15 steps / 1.6e4 yr | 3.5e11 / 2.2 yr | **1.8e10 / 0.12 yr** |
| All-atom, central G = 1e10 | 5e8 | 2.5e17 / 1.6e6 yr | 1.1e13 / 71 yr | **4.0e11 / 2.5 yr** |

**Classical reference [INFERENCE, order of magnitude].** One folding event costs about 1e9 MD steps for a fast folder
and about 1e11–1e12 for an ms folder.

**Reading.**
- Quadratic routes stay dead: B*₂ ≥ 2.5e15.
- For s = 4, a slow folder's plain-MD cost exceeds B*₄. There is no DG-style polynomial bypass for kinetics or
  ensembles of a physics energy (enhanced sampling reduces cost, but by an amount not measured here).
- So in this regime the negative rests on two things:
  - (i) no known super-quadratic algorithm for Gibbs sampling or dynamics of a classical force field (A3/A4, T5);
  - (ii) T*_Q,₄ of 0.1–2.5 years per independent sample.
- It does not rest on classical ease. The synthesis's "What would change the answer (a)" names only "a hard
  learned-energy family". It must add "a super-quadratic algorithm for classical-force-field sampling", which would
  meet a regime that is already classically hard.

---

## 2. What was missed

### 2.1 Adversaries

| # | Missed or under-used adversary | Where it bites | Why it matters |
|---|---|---|---|
| A-a | **spinDMFT / nl-spinDMFT** (thermodynamic-limit dipolar dynamics). LITERATURE-SUPPORTED: Gräßer, Uhrig, Ernst, arXiv:2512.15572, abstract verified this session: spin diffusion in static solids, validated against experiment, "requires each spin to interact with a large number of other spins". The nl-spinDMFT echo result is cited by the relevance verifier and not re-verified | R1-SIM-X, R3-HYB, early window (C1) | It has no finite-size floor and no cluster-family choice. It is the only listed adversary that targets F_∞ directly. It was named as untested in three reports and never run, yet §2.2 schedules 3–6 core-h of governor time on exact N = 22 first |
| A-b | **Exact H and floor at N = 22–24 by two inverse passes** (320 vector-steps; the verifier's method) | C1, C12 | Turns the C12 X₂₂ from INFERENCE (predicted H₂₂) into MEASURED. Pins the exact−CSD offset beyond N = 20 at low cost (about 7–30 CPU-min at N = 22 from the lane's 1.28 s/step central-sector timing, checkpointed) |
| A-c | **Continuous-space classical twin for QeMCMC** (HMC or DG + L-BFGS on the undiscretised torsions) | K-106 | The discretised 2^n instances are an artefact of the quantum encoding; classically, the continuous problem is solved in about 420 evaluations. The lane's decisive evidence is warm start (π(x\*) ≥ 0.9 in 13/24; ≤ 197 classical steps). K-106 should cite that and the continuous twin, not the pointwise δ_q vs δ_c^½ test (see 2.4) |
| A-d | **Pro-quantum red team for kills** | K-109, K-111, FeMoco WEAK | Only SUPPORTS lanes got verifiers. The program's final claim is a negative, so the error that matters is a *false kill*. K-109 (N = 10-conditioned) and K-111 (mis-specified observability, C2) are the weakest kills. The FeMoco residue rests on one preprint for the classical side |
| A-e | **Enhanced-sampling classical twin for physics energies** (REST2, metadynamics, Markov state models, weighted ensemble) | D1 regime | Needed before any claim in the all-atom regime. It sets the true classical B, which D1 bounds only by plain MD |

### 2.2 Literature lines

- **Analog dipolar quantum simulators as the quantum side of R1-SIM(-X).** No NMR lane considered them (grep:
  0 hits for Rydberg/analog in ADVERSARIAL and ROUND3 NMR folders).
  - LITERATURE-SUPPORTED, titles and abstracts verified this session:
    - Scholl et al., "Microwave-engineering of programmable XXZ Hamiltonians in arrays of Rydberg atoms",
      arXiv:2107.14459;
    - Geier et al., "Floquet Hamiltonian Engineering of an Isolated Many-Body Spin System", arXiv:2105.01597
      (effective Heisenberg XYZ in a Rydberg gas).
  - If R1-SIM-X ever escalates to costing, the relevant quantum device is a programmable analog 1/r³ simulator with
    Floquet-engineered XXZ and sign reversal, not a fault-tolerant Trotter circuit. Its binding constraint would be
    analog accuracy against σ = 0.01 after tens of interaction times [INFERENCE].
  - This does not touch K-105: that kill is about the physical protein sample and the forward model, not the
    simulator.
- **NMR rotational-tunnelling spectroscopy** (C2). One abstract verified (cond-mat/0701201). The field-cycling
  literature is recalled only and UNVERIFIED.
- **Nothing new is needed for DQI, Kikuchi or QeMCMC.** Those lanes' literature coverage (61 verified abstracts;
  Layden reproduced; Orfi–Sels) is adequate [INFERENCE].

### 2.3 Physical effects

| Effect | Status in round 3 | Consequence |
|---|---|---|
| **Finite-cluster conserved-charge floor, ≈ (1 − H)/N** | Derived by `r1sim_exact_reach`, but applied only to the late window | C1: 3–4.5 σ at N = 18 even at 40 µs. Every N ≤ 20 finite-cluster forward model, including the N = 10 FI/value computations of R1 and DQ, carries it unless subtracted [DERIVED + MEASURED] |
| **Intermolecular and solvent ¹H** (lattice mates, hydration water in microcrystals) | Flagged once as INFERENCE (R1_theory_hardness l.179, R1_value l.189); never modelled | A "converged cone" of 60–500 spins extends past a surface probe into solvent and neighbour molecules. The converged single-protein echo is therefore not the sample's echo, which lowers R1-SIM-X's physical relevance further [INFERENCE] |
| **Hyperpolarisation** (DNP, p ~ 0.01–0.5) | Not considered by `new_mechanisms_quantum_data`, which used thermal p only | Removes most of the p² ≈ 1e-9 penalty, but not the theorem: memory gain = 1 per parameter at every p, and Bell/QFI ≤ 0.032 at p = 1. **Verdict unchanged** [DERIVED from lane] |
| **Cryogenic requirement and barrier disorder for methyl tunnelling** | Caveated qualitatively | This is the physical side of the C2 identifiability argument |

### 2.4 Statistics and methodology

1. **The step-convergence flaw (C10) is broader than the synthesis says.** It also invalidates:
   - the early-window "converged" readings (C1);
   - R1's MEASURED "σ-cone 16–20 spins at 40 µs".

   The replacement criterion must be absolute, not a step: |F_N − F̂_∞| with an explicit F̂_∞ estimator, plus a
   cross-family check.
2. **The pointwise QeMCMC criterion is biased toward kill at small n.** "δ_q > δ_c^½ on 0/149 records" compares
   gaps that are O(0.02–0.5) at n ≤ 10, where prefactors dominate.
   - The 149 records are not independent: they are the same instances across n and T.
   - The exponent ratio's CI was not reported as a ratio. The component CIs, k_c [0.42, 0.70] and k_q [0.21, 0.42],
     are consistent with ratios from about 0.3 to 1.0.
   - So "sub-quadratic 0.56–0.75" is not statistically established either.
   - The practical kill is sound for other reasons: the gap to break-even at measured n, and warm start.
   - The lane's own favourable extrapolation (n\* ≈ 26 at about 10 minutes per relaxation) should be quoted next to
     K-106, together with the reasons it does not matter: warm start; the discretisation is unnecessary; n\* is the
     whole 27-residue crop.
3. **G1's p_hit ~ e^{−0.028 L} (e^{−0.0415 L} Tobit) is confounded by fixed-depth relaxation.**
   - The census uses 200 L-BFGS iterations per restart at every L.
   - At L = 150, +800 iterations lower random-restart endpoints by 600–1,550 nats [MEASURED, hardness lane].
   - A fixed budget in a dimension growing as ~2L makes hitting "the best 2-Å cluster" harder by construction, on top
     of the moving-target effect.
   - The exponential should not be quoted anywhere as a hardness measure. It still is, in CURRENT_STATE and in the
     round-3 task text.
4. **The DG headline number is the unpolished one.**
   - Use "14/16 at 200 iterations; **5/8 lower under symmetric polishing**, 4 of those 5 in the same fold (1.4–1.9 Å)".
   - Fold-level multistart p(≤ 3 Å) = 0.06–0.34 is from **4 crops**.
   - The ORACLE "300–540 nats buy 0.1–0.5 Å" is from the few shared-fold polished pairs, not from 16 crops.
5. **Cost-to-E_ref is a lower bound on cost-to-optimum.** E_ref is the best found by the same classical portfolio.
   K-107 therefore also needs A8 (transmission). Its ORACLE support (0.1–0.5 Å) has a small sample; see item 4.
6. **Pre-registration location.**
   - Only `new_mechanisms_A` wrote a prereg file (`prereg.json`). The other lanes' rules lived in the orchestrator's
     lane brief.
   - Kills are conservative, so this is housekeeping. But the two SUPPORTS lanes' rules should be copied with
     timestamps into `experiments/PREREGISTERED/` before round 4 cites them.
7. **Unequal tally weights.** "About 30 new mechanisms killed" mixes measured kills (K-106, 107, 108, 109, 110, 114)
   with derivation-only kills (NA-4 to NA-9). The KILLBOOK should keep the kill type visible, as it does for K-103.
8. **Claim-category label.**
   - Lanes write "category 3 (physics simulation)". In the charter, category 3 is computational/resource advantage.
   - R1-SIM-X is a resource question about an idealised spin model with no protein-structure endpoint. It sits
     outside the mission in `CLAUDE.md` and belongs in a spin-off register, not OPEN_QUESTIONS for the mission.

### 2.5 Over-claims in `SYNTHESIS.md`: proposed rewording

| # | Location | As written | Proposed wording |
|---|---|---|---|
| O-1 | §3 box | "The computations that are classically hard do not carry structural information that classical data and methods lack, and the computations that do carry structural information are classically easy." | "In the regimes examined: (1) learned-energy structure prediction is classically easy (DG portfolio); (2) physics-based dense-spin dynamics that may be classically hard add no usable structural information, because of forward-model error and reversal horizons; (3) physics-based all-atom sampling of kinetics and ensembles is classically hard and structure-bearing, but no super-quadratic algorithm is known and the quantum per-sample floor is ≥ 0.1–2.5 yr even at s = 4 [CRITIC-D1]." Tag it INFERENCE and record it as a hypothesis with falsifiers, not a result |
| O-2 | §3.2 | "Inside the physical reversal horizons, NMR forward models are reproduced classically [MEASURED]" | "Two-point transfer is reproduced classically at converged size (CSD ≤ 0.012). For the OTOC(1) and DQ echoes, reproduction is MEASURED only against their own N ≤ 10–12 finite-cluster models. At converged size inside T3 it is UNRESOLVED [CRITIC-C1]" |
| O-3 | §2.1 | R3-HYB "SURVIVES" | "Survives as a model-internal observation (L1). It is not a candidate in any of categories 1–6." Its reference, the finite-cluster F_N, is itself 3–8 σ from the infinite-N echo at t ≤ 120 µs (C1), so "within σ of the reference" is doubly model-internal. Exclude it from any positive tally |
| O-4 | §4 K-111 | "Observability: … below INS resolution" | "Identifiability: the many-body correction (13–40% of Δ) is equivalent to a 1.7–2.7 meV one-body barrier shift and is degenerate with per-methyl V3 nuisances [CRITIC-C2]. Splittings of kHz–MHz are not unobservable per se" |
| O-5 | §4 K-105 / K-109 | Reversal arm and twin arm stated as general | Add: "twin and reversal-window arms measured on N = 10 clusters; load-bearing arm = forward-model error (5–66 σ) + value accounting" |
| O-6 | §4 K-107 | "Any-exponent … at L = 100–500" | Add scope: "for the A80 learned energy. Physics-based force fields are not covered; see CRITIC-D1" |
| O-7 | §2.2 T-X rules | Decision numbers at 160–320 µs only | Add a t ≤ T3 branch (A-1). The late-window branch has no physical signal (0.03–0.13 σ), so it cannot inform even category 3 about a real sample |
| O-8 | §0 | "rigorous where marked" | The only unconditional theorem is K-114, for one state family. The floors (K-101, K-107) are DERIVED but conditional on T3's G(L), K and n_b. Say so |

---

## 3. Verified non-issues (checked, no action needed)

- **Distogram leakage [MEASURED, code and manifest read].** The esmprior_v1 head was trained on 600 crops of 40–72 aa.
  The ladder chains are screened against them: PDB-id exclusion, no shared 9-mer, and < 0.4 identity over any gapless
  30-residue window (`src/qapf/protein/targets.py`, `ladder_manifest.json`). ESM-2's UniRef50 pretraining is
  sequence-only. DG success does not track distogram confidence: Spearman 0.16, p = 0.27, n = 48 (lane-computed). The
  "native-free" label on the DG result is sound.
- **Generalised floor formula.** I re-derived it: B*_s = X^{s/(s−1)} and T*_Q,s = K n_b G t_T X^{1/(s−1)}; s = 2
  gives K-101. I reproduced the lane's L = 100 figure to within its G choice [DERIVED].
- **K-114 theorem.** I re-derived SLD = p·dX from X² = I, which gives {X, dX} = 0 and Tr[X dX²] = 0. The Holevo term
  vanishes because the global spin flip P gives PXP = −X and P dX P = −dX [DERIVED]. Correct as stated, for that
  state family.
- **C12 arithmetic.** X₂₂ = 0.2282 − 0.0645 − 0.0379 = 0.1258 [DERIVED]. Correct, and still INFERENCE because H₂₂ is
  predicted, not measured.
- **DQI girth argument.** The dual of an incidence code is the cycle space, so d⊥ = girth = 3, and 2l + 1 < 3 forces
  l = 0 [DERIVED]. Correct.

---

## 4. Recommended actions, ranked by decision value

All runs are single-threaded, ≤ 15 CPU-min each, ≤ 2 GB, and checkpointed. Pre-register each one first.

**A-1. T-X-early (decides the only open NMR question with a physical signal).**
- Compute exact H and floor at N = 22 (two inverse passes) for t = 40, 80 and 120 µs on p19 and p245.
- Compute X₂₀ at the same times from existing or `fastecho.py` runs.
- **KILL** "the converged echo inside T3 is beyond σ-level classical reach" if both hold:
  - |X₂₂ − X₂₀| ≤ 0.005 on ≥ 6/8 series;
  - the hybrid error budget √(se_H² + offset² + ΔX²) ≤ σ.
- **KEEP OPEN** otherwise.
- Budget: about 30–45 CPU-min, split into checkpointed chunks.

**A-2. spinDMFT / nl-spinDMFT adversary.** Run it before any further governor hours on exact N = 22 late-window
jobs.
- Targets: H_∞ and the echo F_∞ at t ≤ 120 µs.
- **KILL** R1-SIM(-X) at those times if it agrees with the exact-plus-CSD hybrid within σ where both are defined.

**A-3. Record corrections O-1 to O-8 and C1/C2 in the state files.**
- `SCIENTIFIC_MEMORY`: the finite-cluster floor rule, "step convergence ≠ convergence".
- KILLBOOK K-105, K-109 and K-111 wording.
- Drop the G1 p_hit exponential as a hardness measure in CURRENT_STATE and in task templates.

**A-4. Pro-quantum red team on K-109, K-111 and the FeMoco WEAK residue.** One verifier each, briefed to find a
false kill.

**A-5. All-atom scoping note.**
- Add a "physics-based force-field" row to `theory/BREAK_EVEN.md` with D1's assumptions stated as INFERENCE.
- Name the enhanced-sampling twin (A-e) as mandatory for any future route there.

**A-6. Governor opportunity cost (a user decision; do not act without go-ahead).** The 4 long `nmr_cone.py` jobs are
about 18× slower than `fastecho.py` and serve only the late-window residue, which is physically empty. If the user
agrees, replace them with A-1 and A-2 (H-4 in the synthesis).

---

## 5. Files

- `research/experiments/ROUND3/CRITIC.md`: this file.
- `research/experiments/ROUND3/critic/critic_checks.py`: C1, C2 and D1. Reads existing JSONs only; < 1 CPU-s.
- `research/experiments/ROUND3/critic/critic_checks.json`: per-series C1 table, C2 unit conversions and barrier
  equivalents, and D1 floors.
