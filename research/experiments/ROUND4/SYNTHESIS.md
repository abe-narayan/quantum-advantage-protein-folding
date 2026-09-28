# Round 4 synthesis (program director; final round of this sprint)

_2026-09-28. File: `research/experiments/ROUND4/SYNTHESIS.md`. Director cross-check: `ROUND4/director/cross_family.py`
→ `ROUND4/director/cross_family.json`. It reads only verifier JSONs already on disk and runs no dynamics (< 1 CPU-s)._

**Inputs**
- 5 lane reports in `research/experiments/ROUND4/<lane>/`: `tx_early`, `spindmft`, `allatom_superquadratic`,
  `redteam_kills`, `analog_simulator`.
- 6 adversarial verdicts, 3 each for `tx_early` and `spindmft`. These were the two lanes that returned INTERESTING.
  The three KILLS lanes were not sent to verifiers. As in round 3, a kill does not need to survive verification, but it
  stays open to attack. `redteam_kills` is itself the pro-quantum attack on four earlier kills (CRITIC A-4).
- Pre-registered rules:
  - `PREREGISTERED/PREREG_G1_C1_Q4.md`, "Round 4": H-2, T-X-early, spinDMFT, all-atom, red team;
  - `spindmft/PREREG_spindmft.md`, with Addenda A and B, each timestamped before its runs;
  - `tx_early/README.md` §0, the operationalisation written before any N = 20/22 output.

**Consolidation rule.** A claim SURVIVES only if at most 1 of its 3 verifiers refutes it with a specific, credible
argument.

**Tags.** MEASURED / DERIVED / THEORETICAL / LITERATURE-SUPPORTED / INFERENCE / UNPROVEN. **[DIRECTOR]** marks a
cross-check made in this synthesis from files on disk.

**Level scale.** Unchanged from round 3 (T2 header table): L1 query separation on a constructed family; L2 same-chain
walk speedup; L3 L2 plus oracle gate cost; L4 compared with the best classical method; L5 compiled validation; L6
hardware. L0 means none of these. The ladder column uses R1_SYNTHESIS's A–I scale: A new formulation, B empirically
useful, C advantage vs a strong classical baseline, D resource-normalised, E scaling, F theoretical/query,
G fault-tolerant, H hardware, I end-to-end.

**Claim categories** (charter): 1 quantum usefulness, 2 empirical quantum advantage, 3 computational/resource advantage,
4 sampling advantage, 5 hardware advantage, 6 theoretical/provable advantage. Several lanes still write "category 3
(physics simulation)". Category 3 is a resource advantage, and none of 1–6 applies to anything in this round.

---

## 0. Bottom line

1. **Round 4 flips no verdict toward a quantum advantage.**
   - New KILLBOOK entries: K-117 to K-120 (§4).
   - K-105, K-109 and K-111 stand, but each now rests on a different, corrected arm.
   - FeMoco E4 stays WEAK.
   - None of the four red-teamed kills was false.
2. **The one open NMR question with a physical signal is answered at 40 µs, on the classical side** [MEASURED agreement
   and cost; DERIVED quantum cost; INFERENCE that the common value is the N → ∞ echo].
   - The question (CRITIC C1): is the converged ¹H OTOC(1) echo inside the reversal window beyond σ-level classical
     reach?
   - Two exact cluster families that contain b's dominant dipolar partners agree to ≤ 0.0055 on 8/8 series. That is
     five implementations across three independent code paths (two sector kernels, three estimators).
   - Two independent thermodynamic-limit estimators agree with each other to ≤ 0.0045, and with the exact values to
     ≤ 0.0096.
   - Cost: 2.7–19 single-core CPU-min for all 8 series. A fault-tolerant QPU needs 2.8–10 h per probe, even under its
     most favourable assumptions.
   - Scope: 1UBQ, 2 probes, 1 field orientation, static-coupling idealised model. Recorded as K-119, provisional
     pending replication.
3. **`tx_early`'s headline does not survive (2/3 refute).**
   - The headline: "the probe-centred F_N is converged at 40 µs; CRITIC C1's gap is an estimator artefact."
   - The probe-centred ladder is a false plateau at sites whose own dominant partner enters only at probe rank 24–48.
     Adding that one spin moves F at p245 b7 by **+0.070 (7σ)**. Two verifiers found this independently.
   - What survives: the round-3 hybrid estimator is biased; the (1 − H)/N floor is bookkeeping, not an additive bias on
     F; and the pre-registered T-X-early test was **not executable under the cap** (at least 161 CPU-min against 90).
4. **The round-3 comparator F̂_∞ = H_∞ + X_N and every X-based criterion are retired (K-120)** [MEASURED].
   - The pooled slope dF/d(H + floor) is −0.03 ± 0.10 at 40 µs. The hybrid needs 1 (z = 6.2).
   - The hybrid lies 2.7–9.5σ below the b-aware values.
   - CRITIC C1's 3.1–8.2σ table is withdrawn at 40 µs. Its conclusion ("finite clusters are not σ-accurate") survives
     on 2/8 series, but by a different mechanism (missing partners of b) and with the opposite sign.
5. **80–120 µs is still open, as idealised-model physics only** [MEASURED].
   - No two classical families agree within σ on any series: 0/8 at 80 µs and 0/8 at 120 µs. The spread is up to
     0.075 and 0.126.
   - This residue is outside the mission. Under a physical T2 at most 1.2σ of it is visible, and at most 0.22σ for a
     site-resolved echo. No costed quantum route, digital or analog, beats anything there.
6. **The all-atom physics regime (CRITIC D1) is killed, but as a no-applicable-algorithm negative, not a
   classical-ease negative (K-117; unverified).**
   - The largest speedup exponent whose preconditions a protein force field meets is s = 2.
   - T\*_Q,2 is at least 2.2 yr even at 10 ns logical Toffolis.
   - A hypothetical s ≥ 3 algorithm would break even (T\*_Q,4 = 2.6 h–10 d at 10 ns). This is the only examined regime
     that is not resource-dead.
7. **The red team found no false kill, but corrected the load-bearing arms.**
   - K-105 now rests on the site-resolved reversal horizon alone. The profiled median gain is ≤ 1.60 even if the whole
     echo were quantum-only. The forward-model-error arm is profilable and not load-bearing.
   - K-109's recorded arm was an N = 10 artefact. It is now re-based on the measured classical reach, with one
     conditional near-miss: 1PGA p390, DQ methyl butterfly, g ≈ 2.1–2.5 at 19 T2. That can be tested in about
     20 CPU-min.
   - K-111 is re-based on resolvability plus classical exactness.
   - FeMoco E4 hinges on a model floor σ_m ≤ 1.2 kcal/mol.
8. **Analog dipolar simulators are killed practically (K-118).**
   - Demonstrated platforms are 42–100σ outside the σ budget.
   - The best undemonstrated route is 1.2–1.8σ at 40 µs and 2–6σ at 80–120 µs.

---

## 1. Consolidated table per lane

| Lane | Lane verdict | Verifiers (refute / 3) | Consolidated status | Theoretical level | Practical level | Ladder (A–I) | Decisive number |
|---|---|---|---|---|---|---|---|
| `tx_early` (T-X-early, CRITIC A-1) | INTERESTING (rule: KEEP OPEN, not completed) | **2/3 refute** (classical: cross-family; relevance: relevance + cross-family). Resource: not refuted, with corrections | **Central claim DOES NOT SURVIVE.** Surviving parts: the numbers; rule not fired; hybrid biased at early times; X is bookkeeping in-family; exact H₂₂ and floor₂₂. The procedural KEEP OPEN is recorded as **NOT EXECUTABLE UNDER CAP** | L0 | L0 | None reached; classical-side measurement only | Adding one b-partner (HG3/LYS27, probe rank 48) to the probe-centred N = 20 cluster moves F(40 µs) at p245 b7 by **+0.0697 = 7.0σ**. The lane's ladder moved ≤ 0.0018 over N = 18→22 [MEASURED, two verifiers] |
| `spindmft` (CRITIC A-2) | INTERESTING (literal rule not fired; validation gate failed) | **1/3 refute** (relevance: the label, not the measurements). Classical and resource: not refuted; both strengthen 40 µs | **SURVIVES, corrected.** "80 µs partly open" becomes **open**. "≤ 0.006" becomes ≤ 0.0096. Reclassified as a **KILL-leaning classical-adversary result**; it supplies K-119 (40 µs) and K-120 (hybrid retired) | L0 | L0. DERIVED: an FT QPU is 17–65× slower than one core at 40 µs | C failed (σ-level classical reach at 40 µs); D negative | 40 µs: exact b-aware (N = 18–22) vs spinDMFT within σ on **8/8**, max 0.0096. E2 vs E1 8/8, ≤ 0.0045. 80 µs: **0/8** (0.016–0.044) [MEASURED] |
| `allatom_superquadratic` (CRITIC D1, A-5) | KILLS | none | **KILLED (K-117)**, unverified. Kill type: no applicable algorithm | s = 2: L2, and L3 with the derived oracle cost. s ≥ 3: L0 (no family's preconditions hold) | L0 | F failed (no precondition-satisfying s ≥ 3 family); G negative at s = 2 | Carleman R ≥ **4.3×10³** (R < 1 needed). T\*_Q,2 ≥ **2.2 yr** at t_T = 10 ns (Trp-cage GB, best case). Hypothetical T\*_Q,4 = 2.6 h–10 d at 10 ns [MEASURED + DERIVED] |
| `redteam_kills` (CRITIC A-4) | KILLS (all four stand; three arms corrected) | none (the lane is the red team) | **K-105, K-109, K-111 STAND with re-based arms. FeMoco stays WEAK.** Adopted provisionally (unverified); see corrections C-R4-12 and C-R4-13 | L0–L1 | L0 | B not reached, except one conditional category-1 residue (p390 DQ); C failed | K-105: profiled g_med **1.09–1.60** at t_cl = 0 under the site-resolved PE envelope (moderate priors). K-109: g_med 1.27–1.97 at 12.5 T2 against measured reach. K-111: 0/32 doublets resolved at V3 = 60–100 meV. FeMoco: σ_m ≤ 1.2 kcal/mol needed; ≥ 10.8 QPU-days per question [MEASURED + DERIVED] |
| `analog_simulator` (CRITIC 2.2) | KILLS (practical) | none | **KILLED (K-118)**, unverified | L0 (DERIVED structural obstruction; no separation) | L0 | H failed; D not reached | Demonstrated Rydberg parameters **42–100σ**. Best undemonstrated route 1.2–1.8σ at 40 µs, 2–6σ at 80–120 µs. Pulse error ≤ 0.0023–0.0055 rad needed vs 0.06 demonstrated [MEASURED sensitivities + INFERENCE budget] |

### 1.1 Pre-registered rule outcomes

| Rule (source) | Outcome | Note |
|---|---|---|
| H-2: a convergence claim needs an explicit F̂_∞ and a cross-family check (PREREG Round 4) | **Applied.** `tx_early` violated it and was refuted. `spindmft` and its verifiers satisfy it at 40 µs | This round extends H-2: "cross-family" means clusters that contain b's dominant partners (report M2_b coverage), at least two construction rules, plus a thermodynamic estimator (§6, D-R4-3) |
| T-X-early: KILL if \|X₂₂ − X₂₀\| ≤ 0.005 on ≥ 6/8 AND budget ≤ σ | **KEEP OPEN (default).** 0 pass / 1 fail / 7 undetermined; 7/8 pass at 40 µs only | Not executable under the 90 CPU-min cap: the minimum complete test is 161 CPU-min (DERIVED, resource verifier). The criterion is also ill-posed (X is bookkeeping) and is retired (K-120) |
| spinDMFT literal rule: KILL if ≥ 7/8 within σ of the hybrid | **Did not fire** (0/8, 0/8, 1/8) | The comparator is refuted by MEASURED data (§0.4). The validation gate failed at every t |
| spinDMFT Addendum A (world ladder) | Corroborated at 40 µs (23/24, low power) and 80 µs (20/24). Not at 120 µs (11/20) | — |
| spinDMFT Addendum B (exact b-aware test, before runs) | Corroborated at 40 µs. At 80 µs the N ≤ 16 agreement is **superseded** by N ≥ 18 data (0/8 within σ) | Two verifiers independently found the N = 16→18 shell event at 80 µs |
| All-atom: SUPPORT only if preconditions hold AND T\*_Q,s ≤ 1 day | **Not met.** KILL | The task's looser 1-month rule gives the same verdict |
| Red team: reopen any kill whose load-bearing arm fails with nothing else carrying it | **No reopen.** Every kill has a surviving arm | Replacement arms are in §4.2 |

### 1.2 Corrections adopted in this synthesis

**From the verifiers**

- **C-R4-1** (`tx_early`, classical and relevance verifiers; MEASURED).
  - "F_N converged at 40 µs on all 8 series; exact simulation of 18–22 spins reaches the converged echo within σ/4"
    becomes: "a probe-family plateau. Clusters that contain b's partners shift p19 b8 by +0.025 (2.5σ) and p245 b7 by
    +0.065 (6.5σ). They are stable to ≤ 0.005 over N = 18–22, 2 → 4 partners, and pairb."
  - Robustness checks: the shift is unchanged at dt = 1 µs; ranks 20–21 move F by ≤ 0.0015; CRN swaps reproduce it.
- **C-R4-2** (`tx_early`, resource verifier; DERIVED from measured rates).
  - The missing 80/120 µs cells cost 149 CPU-min at the production rate, not about 2 CPU-h.
  - The minimal complete T-X-early test is 161 CPU-min.
  - CRITIC A-1's estimate of 30–45 CPU-min omitted the F₂₂ echo.
- **C-R4-3** (`tx_early`, relevance verifier).
  - "X is not an independently converging quantity" is close to an identity, given X ≡ F − H − floor.
  - The back-test is an in-family restatement of that identity, not independent evidence.
  - The lane's own 1/N fits (F̂_∞ − F₂₂ = +1.57σ on p19 b8, +1.08σ on p245 b7) already contradicted "σ/4".
- **C-R4-4** (`tx_early`, resource verifier; MEASURED). The CSD H_∞ carries an unreported N_c systematic of 0.01–0.025.
  At p19, 40 µs, N_c = 22/24/40/80/160 gives 0.362/0.357/0.362/0.338/0.363 ± 0.017.
- **C-R4-5** (`spindmft`, classical and resource verifiers; MEASURED).
  - "80 µs partly open" becomes **open**: the b-aware N = 12–16 plateau was pre-asymptotic (p19 b8 falls by 0.033–0.036
    from N = 16 to 18).
  - "b-remote 2/3 within σ at 80 µs" is superseded.
  - "Reproduced to ≤ 0.006" becomes ≤ 0.0096 at N = 18–22.
- **C-R4-6** (`spindmft`, classical verifier). The b-aware 5.6–9.6σ gap above the hybrid is not a third independent
  refutation. On p19 b9 it is floor-driven. Only p245 b7 and p19 b8 carry a genuine family effect.
- **C-R4-7** (`spindmft`, resource verifier).
  - The flat-X test at 40 µs refutes the hybrid's floor subtraction, not its H_∞ − H₂₀ term (−0.027 on p19).
  - The evidence on that term is partial: the p19 N = 22 probe points, the b-aware agreement, and the `tx_early`
    resource verifier's tracking test (F follows < ~20% of a genuine −0.0106 ± 0.0010 H drift on p245).
- **C-R4-8** (`spindmft`, relevance verifier; MEASURED).
  - At 40 µs, isolated exact {a, b}-centred clusters of 10–12 spins are within σ of N = 16 on 3/3 b-remote series,
    in 0.3–20 CPU-s.
  - The Gaussian bath's share of the spinDMFT prediction is only +0.004 to +0.014.
  - The "prediction before exact runs" is real (file timestamps), but it mainly tests the cluster-family choice.
- **C-R4-9** (`spindmft`, resource verifier). The lane's "peak RSS < 0.3 GB" is UNVERIFIED (not logged).

**[DIRECTOR]**

- **C-R4-10.** The analog lane's "the simulator cannot escape the finite-cluster floor (1 − H)/N, 0.6–1.2σ" is
  withdrawn.
  - Round 4 measured, in-family and in three independent analyses, that F does not carry the floor as an additive bias
    at 40 µs.
  - Its comparator, the CSD + exact-X hybrid, is retired (K-120), and its revival item 4 ("X does not converge by
    N ≈ 26") is restated on F.
  - The kill is unchanged: pulse, decay, leakage and motion terms dominate every budget.
- **C-R4-11.** The analog lane's "K-105 corollary" (a σ-level forward model needs H coordinates to 0.004–0.009 Å) is
  **not adopted** as a K-105 arm.
  - For coordinates that are being inferred, sensitivity is Fisher information, not error.
  - Only non-inferred nuisance geometry and motion are error, and RT-A3 bounds that: bias 0.1–11× CRB_q.
- **C-R4-12.** Both NMR relevance verifiers cite forward-model error (5–66σ; 9–33σ) as K-105's load-bearing arm.
  - The red team measured that nuisance *families* profile away: the 7.6–45σ misfit is removed, 18–83% of the
    structural FI is retained, and g is not reduced.
  - Raw misfit is therefore not the right metric; the profiled bias is.
  - Those relevance verdicts still stand, on their independent visible-signal (reversal-envelope) arguments.
- **C-R4-13.** The red team's K-109 correction uses a DQ size ladder that is a **single-family step statistic on one
  probe** (1UBQ p19, probe-centred ordering).
  - Round 4's central lesson is that single-family step stability is not convergence. The failure mode is the cluster
    family, which does not depend on a conserved-charge floor.
  - So "non-methyl DQ sites converged to 80 µs" is MEASURED step stability, and only INFERENCE as convergence.
  - Suppose a cross-family DQ ladder fails and classical reach collapses to t_cl = 0. K-109's own gain threshold
    (g ≥ 2; moderate priors, secular transfer classical) would then be met on 3/3 probes at 19 T2 (2.45–3.22), but on
    only 1/3 at 12.5 T2 (1.80 / 1.90 / 2.70).
  - K-109 would still stand on its other reopen condition: a measured protein site-resolved T3_DQ/T2 ≥ 19. g ≥ 10 is
    reached nowhere.
  - RT-DQ-methyl must therefore include a b-aware/pairb family and the p390 non-methyl sites (§2, item 12).
- **C-R4-14.** The all-atom lane's "even an exponential speedup loses to BioEmu per ensemble sample" is not a
  like-for-like twin, because BioEmu does not sample the force-field Boltzmann distribution exactly. Tagged INFERENCE.
  K-117 does not depend on it.
- **C-R4-15.** K-119 holds for the **static-coupling idealised model** used throughout R1-SIM. The red team's value
  model uses rotor-averaged couplings. That the classical reach t_cl ≥ 40 µs carries over to the rotor-averaged model is
  INFERENCE (untested).
- **C-R4-16.** Cross-lane arithmetic. With t_cl ≥ 40 µs now established (K-119), the red team's own table caps the
  K-105 secular gain at t_cl = 40 µs:
  - **1.06–1.33** under the site-resolved PE envelope;
  - **1.36–2.23** under the global LE envelope (moderate priors; ≤ 2.38 with none).

  [MEASURED model values, `redteam_kills/README.md` §1.1; N = 10 Fisher model]

### 1.3 [DIRECTOR] Cross-family agreement, all round-4 classical estimates of F_ab (`director/cross_family.json`)

**Estimates collected for each series.**
- Exact, b-aware:
  - SA2 / SA4: probe ranks plus 2 or 4 b-partners (`tx_early/verify_classical`);
  - {a, b} ∪ nearest-to-either, three implementations with independent code paths and random vectors: PB20 (`tx_early/verify_classical`, ROUND3 pairb), FEPB (`spindmft/verify_classical`, fastecho), PP (`spindmft/verify_resource`, P₊ sector kernel).
- Thermodynamic:
  - E1: probe F₁₈ plus the sr-spinDMFT bath correction;
  - E2: exact b-aware plus a CSD-bath correction;
  - the spinDMFT value the resource verifier used.

**Caveat.** PB20, FEPB and PP share one cluster rule. They validate implementation, not family. SA2/SA4 are the second
family.

| t (µs) | Exact b-aware spread ≤ σ | Mean difference between the two families | All estimates (exact + E1, E2, spinDMFT) spread ≤ σ | Max spread | Probe family off the b-aware median by > σ |
|---|---|---|---|---|---|
| 40 | **8/8** (max 0.0055) | ≤ 0.003 on 8/8 | 6/8. The exceptions, p19 b8 (0.014) and p19 b9 (0.011), are driven by the spinDMFT value and E1; E2 agrees | 0.014 | 2/8: p19 b8 −0.021, p245 b7 −0.063 |
| 80 | 2/8 | up to **0.066** (p245 b7), 0.048, 0.036, 0.035 | **0/8** | 0.075 | 4/8 |
| 120 | 3/8 | up to 0.075 | **0/8** | 0.126 | 7/8 |

**Reading.**
- At 40 µs, the cluster family matters only for whether b's partners are inside the cluster. Any b-aware family gives
  the same answer.
- The thermodynamic corrections are small: the mean of the thermodynamic estimates minus the mean of the exact ones is
  ≤ 0.007 on every series.
- At 80–120 µs, the two b-aware families disagree by up to 6.6–7.5σ, while SA2's own N-steps are < σ on 8/8 at 80 µs.
  The open residue is a **cluster-family problem, not a cluster-size problem**, and no σ-level classical estimator exists
  there yet [MEASURED].

---

## 2. Final status of every open item from ROUND3/SYNTHESIS.md and ROUND3/CRITIC.md

Status: **CLOSED-KILL / CLOSED-SURVIVES / STILL OPEN**. "Closed (done)" marks a task that was executed and is not a
claim. Every run named below is single-threaded, checkpointed and pre-registered first.

### 2.1 NMR echo (R1-SIM, CRITIC C1, A-1, A-2, O-2, O-7)

| # | Item | Status | Evidence | Exact next test |
|---|---|---|---|---|
| 1 | **Early-window echo at 40 µs** ("the converged echo inside T3 is beyond σ-level classical reach"; CRITIC C1, O-2) | **CLOSED-KILL (K-119), provisional** | §1.3: two exact b-aware families ≤ 0.0055 on 8/8; E1–E2 ≤ 0.0045; b-aware vs spinDMFT ≤ 0.0096; 2.7–19 CPU-min vs 2.8–10 h per probe on an FT QPU. The literal pre-registered rules could not fire because their comparator was refuted. The kill uses the H-2 criterion post hoc, plus the pre-registered Addendum B corroboration (deviation D-R4-2) | **R-1 (confirmation, not decision).** Repeat SA2 + {a, b}-nearest exact (N = 18–20) + E2 at 40 µs on 1PGA p390, 1UBQ p487 and 2 further b0 orientations of 1UBQ p19/p245. That is 24 series; at the measured 20 s (N = 18) and 88 s (N = 20) per series per family, about 1.5–2 CPU-h, splittable into ≤ 30 CPU-min checkpointed runs. **Reopen** if an exact b-aware family and a thermodynamic estimator disagree by > 3σ on ≥ 2 series. A reopening is category-3 physics only and never revives K-105 |
| 2 | Echo at 80 µs | **STILL OPEN**, spin-off register, outside the mission | §1.3: 0/8 series with any two classical estimates within σ. Family spread up to 0.066. Visible share under physical T2 ≤ 1.18σ (LE) and ≤ 0.22σ (PE) (`spindmft/verify_relevance`) | **T-F80.** Grow SA-type union clusters ({a-shell} ∪ {b-shell}, grown jointly) and {a, b}-nearest clusters to N = 22 at 80 µs for all 8 series, going to N = 24 only where N = 20 → 22 moves by more than σ/2 (`tx_echo.py` / `run_custom.py`). N = 22 costs 7–8 CPU-min per site-family at 40 µs, so about 15 at 80 µs, and about 4 CPU-h for all 8 series × 2 families (governor, user go-ahead). Add E2 with a b-aware embedding at n_c = 10 → 12. **KILL at 80 µs** if both families move ≤ σ/2 over two N steps, agree within σ, and E2 is within σ on ≥ 7/8. Otherwise it stays in the spin-off register. Quantum costing is justified only if the site-resolved visible signal is ≥ 1σ |
| 3 | Echo at 120 µs, and the late window 160–320 µs (R3 §2.2 T-X0 to T-X3; R1-SIM-X; K-116 residue) | **STILL OPEN**, spin-off register. The X-based rules are retired (K-120) | 120 µs: 0/8 agree (spread up to 0.126). spinDMFT A3 is biased there (F → −1/3). Whole echo visible ≤ 2σ (LE, rotor-averaged) and ≤ 0.1σ (PE). The late window is 13–40 T2, with no physical signal (CRITIC O-7) | Same as T-F80 at 120 µs, with an upgraded thermodynamic estimator: two-centre {a, b} embedding, bath–bath correlations (A2), and a beyond-quenched OTOC with a second quantum shell. No governor hours on 160–320 µs without user go-ahead and a stated physical purpose |
| 4 | T-X-early pre-registered test (CRITIC A-1) | **CLOSED (done; NOT EXECUTABLE UNDER CAP; criterion retired)** | C-R4-2; K-120 | None. The N = 22 checkpoints at 80/120 µs are kept. If they are ever resumed, score F in a b-aware family, not X |
| 5 | spinDMFT adversary (CRITIC A-2, A-a) | **CLOSED (done)** | It agrees at 40 µs with an independent CSD-bath estimator (8/8, ≤ 0.0045). sr-spinDMFT fails on this network (z_eff median 3.15; p19 G_aa(80 µs) = 0.21 vs 0.36). The embedded error does not fall from n_c = 10 to 12 | The upgrades belong to items 2 and 3 |
| 6 | Hybrid comparator H_∞ + X_N; the R3-HYB decisive test T-H1 (approximations on X); the K-116 revival trigger "X drifts ≥ 0.01" | **CLOSED-KILL (K-120, methodological)** | Flat-X slope −0.03 ± 0.10 (z = 6.2). The hybrid is 0/8 within σ of the b-aware values at 40 µs. R3-HYB's measurement stays a model-internal L1 observation, excluded from every tally (CRITIC O-3) | None |
| 7 | "Finite-cluster floor (1 − H)/N ≥ 3σ biases every N ≤ 20 forward model" (CRITIC §2.3, row 1) | **CLOSED (withdrawn at 40 µs)** | The floor is b-independent bookkeeping and F does not carry it (in-family MEASURED at N ≤ 22 on 2 probes, 3 analyses). Replication on p487/p390 has low power. At 80–120 µs the test has no power (slope SE 0.5–0.7) | Covered by R-1 and T-F80 |
| 8 | Replication cones 1PGA p390 and 1UBQ p487 (PREREG 2026-09-28 extension) | **STILL OPEN** (running or partial; N = 20 checkpoints on disk) | Used only for the weak flat-X replication | Fold into R-1: score F at 40 µs with b-aware clusters, not the Δ_N step rule |
| 9 | Intermolecular and solvent ¹H (CRITIC §2.3) | **STILL OPEN, mission-irrelevant** | It can only lower the relevance of a single-protein echo | None scheduled |
| 10 | Analog dipolar simulators (CRITIC §2.2) | **CLOSED-KILL (K-118)** | §1 table | Literature watch against the K-118 revival gate |
| 11 | R1-SIM-DQ (R3 §2.3 parked row) | **STILL OPEN (narrow)** | Non-methyl DQ sites are step-stable (≤ 0.0017 per ΔN = 2) to 80 µs at N = 18 on 1UBQ p19, in a single family (C-R4-13). The methyl butterfly is unconverged | Merged into item 12 |

### 2.2 Red-teamed kills (CRITIC A-4, O-4, O-5)

| # | Item | Status | Evidence | Exact next test |
|---|---|---|---|---|
| 12 | **K-109** (DQ echo) | **CLOSED-KILL (re-based, narrow)**. One conditional residue **STILL OPEN**: 1PGA p390 methyl butterfly (g_med 2.1–2.5 only at 19 T2, and only if unreachable past 40–50 µs) | `redteam_kills` §1.2, §3 | **RT-DQ-methyl**, about 20–30 CPU-min. Rotor-averaged, partner-complete DQ ladder at N = 12–18, t ≤ 60 µs, at 1PGA p390 HG21/THR53 and 1UBQ p19 HG22/ILE3, in **two families** (partner-complete probe-ordered, and {a, b}-nearest), plus the p390 non-methyl sites. **KILL the residue** if \|F_N − F_{N−2}\| ≤ 0.003 for t ≤ 50 µs at N ≥ 16 and the families agree within σ. Otherwise record g ≤ 2.5 as a category-1 usefulness question that still needs a measured protein site-resolved T3_DQ/T2 ≥ 19 |
| 13 | **K-105** (secular OTOC(1)) | **CLOSED-KILL (re-based)** | The site-resolved PE envelope gives profiled g_med 1.09–1.60 at t_cl = 0 (moderate priors; ≤ 2.10 with none), and 1.06–1.33 at the now-established t_cl = 40 µs. g ≥ 10 is reached nowhere. The literature gives no anchor for protein T3/T2 ≥ 15 (`redteam_kills` §4) | Decisive and experimental, outside compute: site-resolved polarisation-echo T3/T2 in microcrystalline GB1 or ubiquitin. Compute: an ensemble forward model (≥ 50 MD snapshots of per-pair S_ij) to size the RT-A3 bias floor |
| 14 | **K-111** (methyl rotors) | **CLOSED-KILL (re-based)**. CRITIC C2's degeneracy argument is superseded as incomplete | The J doublet is observable and resolved in 0/32 pair cases at V3 = 60–100 meV (σ_V3 ≥ 1 meV), and 2/32 at 30 meV. J is an exact 2-rotor classical calculation (seconds; 3-rotor 83 s) | R-ROTOR stays parked. Reopen template in §4.2 |
| 15 | **FeMoco E4 isomer residue** (R3 §5.2) | **STILL OPEN (WEAK, parked; chemistry level)**. The one preprint is not load-bearing | It survives only if σ_m ≤ 1.2 kcal/mol (σ_best = 5, 1 Å lever), which the lane inferred as about 1–4. Cost ≥ 10.8 QPU-days per question at 76 orbitals and 30 energies | Model-floor ladder (QM region, embedding, MD snapshots) for charge-moving E4 isomers on external HPC. **KILL** if σ_m > 1.2 kcal/mol, or if a classical ranking reaches ≤ 2 kcal/mol at ≥ 100 orbitals. **SURVIVE (WEAK)** only if σ_m ≤ 1.2, the best classical error is ≥ 5 kcal/mol, and ≤ 30 energies at ≤ 100 orbitals suffice |

### 2.3 All-atom physics regime (CRITIC D1, A-5, A-e)

| # | Item | Status | Evidence | Exact next test |
|---|---|---|---|---|
| 16 | **Super-quadratic quantum algorithm for all-atom folding kinetics or ensembles** | **CLOSED-KILL (K-117)**. Kill type: no applicable algorithm. Unverified and open to attack | §1 table; `allatom_superquadratic` survey (12 families, 53 verified arXiv records) | This is an attack on the kill, not a lead: (i) a pro-quantum read of the full proofs of Kharazi 2601.15523 and Claudon 2501.05868, looking for an s > 2 regime against fixed-step MD or weighted ensemble; (ii) compile the coherent LJ + erfc-Coulomb pair oracle into Toffolis (the s = 3/4 break-even goes as G^1–2); (iii) R, the curvature census and λ_max for protein G and ubiquitin (about 27 CPU-min each) |
| 17 | Enhanced-sampling classical twin (CRITIC A-e) | **CLOSED (done, LITERATURE-SUPPORTED)** | Weighted ensemble: NTL9 about 1.3e11 steps, protein G about 1.1e11. MSM λ6-85: 5.2e11. Metadynamics Trp-cage FES: 1.6e8 | Tighten: the Adhikari 2019 SI time step; Anton-3 throughput (UNVERIFIED recall) |
| 18 | `theory/BREAK_EVEN.md` physics-force-field row (CRITIC A-5) | **STILL OPEN (housekeeping)** | — | Write the row from `floor_allatom.json`. Replace D1's G = 1e9–1e10 with the measured-pair-count G = 1.1e9–4e10 (generous) |

### 2.4 Learned-energy and other parked residues (not addressed in round 4)

| # | Item | Status | Exact next test |
|---|---|---|---|
| 19 | QeMCMC small-n exponent (R3 §2.3); CRITIC §2.4(2) statistics; A-c continuous twin | **STILL OPEN (parked; low prior)** | Matrix-free Krylov gaps at n = 11–14 with a bootstrap CI **on the ratio** k_q/k_c, plus a warm-start TV metric. Reword K-106 to cite warm start and the continuous DG/HMC twin |
| 20 | T = 1 sub-basin posterior sampling | **STILL OPEN (parked)** | As in R3 §2.3: an upper bound per sample from warm-started per-mode NRPT at L = 100–150 |
| 21 | DG-residual crops | **STILL OPEN (parked; classical)** | As in R3 §2.3 |
| 22 | Multi-parameter memory window | **STILL OPEN (parked)** | SDP/Nagaoka single-copy bound at N = 8–10 |
| 23 | DQI / Kikuchi reopen probes | **STILL OPEN (parked)** | d⊥ and flat-forest l50 on NOE-assignment and coevolution parity systems |
| 24 | G1 exponent p_hit ~ e^{−0.028 L} as a hardness measure (CRITIC §2.4(3)) | **CLOSED-KILL** as a hardness measure | Housekeeping: `CURRENT_STATE.md` still lists it as an input (pending item 2). Remove it |
| 25 | Hyperpolarisation (CRITIC §2.3) | **CLOSED** (verdict unchanged; K-114 holds at every p) | — |
| 26 | NMR rotational-tunnelling spectroscopy literature (CRITIC §2.2) | **STILL OPEN, UNVERIFIED**, no longer load-bearing for K-111 | Verify the field-cycling window if R-ROTOR is ever reopened |
| 27 | Housekeeping: DG headline wording (§2.4(4)); cost-to-E_ref (§2.4(5)); pre-registration location (§2.4(6)); tally weights (§2.4(7)); category label (§2.4(8)); level scale (H-1) | **STILL OPEN (housekeeping)** | See §6 |

### 2.5 CRITIC O-1 to O-8

| Item | Status |
|---|---|
| O-1 thesis | Replaced by §3 |
| O-2 | Replaced by: "Two-point transfer is reproduced classically at converged size (CSD ≤ 0.012). For OTOC(1) at 40 µs, the converged echo is reproduced to σ by b-aware exact clusters of ≤ 22 spins plus thermodynamic bath corrections (8/8 series; 1UBQ, 2 probes, 1 orientation) [MEASURED agreement; INFERENCE for F_∞]. At 80–120 µs no σ-level classical estimate exists [MEASURED family disagreement]. For DQ, non-methyl sites are step-stable to 80 µs at N = 18 (one probe, one family)" |
| O-3 | Kept (R3-HYB excluded from any tally) |
| O-4 | Superseded by the K-111 re-basing (§4.2) |
| O-5 | Superseded by the K-105 and K-109 re-basing (§4.2) |
| O-6 | Kept. K-107 is scoped to A80, and the physics regime is K-117 |
| O-7 | Done (items 1–4) |
| O-8 | Kept. The only unconditional theorem is K-114, for one state family. The floors are DERIVED and conditional on G, K and n_b |

---

## 3. Is there a quantum advantage for protein structure computation?

**Answer: no, in every regime this program examined.** No claim in any of categories 1–6 survives for
protein-structure computation.
- The program killed 28 discovery mechanisms, about 30 round-3 mechanisms or variants, and 4 round-4 directions.
- The 4 red-teamed kills stand on corrected arms.
- The components are MEASURED or DERIVED. The overall statement is **INFERENCE**. Its only theorem-grade pieces are
  K-114 (one state family) and the cited no-go results.

### 3.1 The corrected thesis (supersedes the R3 §3 box and CRITIC O-1; recorded as a hypothesis with falsifiers)

> **In the regimes examined, protein-structure computation falls into three classes, and none leaves room for a
> quantum advantage:**
>
> **(1) Structure-bearing and classically easy.** Where the computation carries structural information and an
> efficient classical algorithm exists, the classical algorithm suffices.
> - Learned-energy structure prediction: a native-free distance-geometry portfolio reaches the best-known basin in a
>   median of about 420 evaluations, and any quantum exponent would need logical Toffolis of ~3 ns or less.
> - The ¹H dipolar OTOC(1) echo inside the physical reversal window: σ-level classical reach at 40 µs.
>
> **(2) Possibly classically hard, but structurally uninformative.** This is dense-spin dynamics beyond about 80 µs in
> the idealised model. It lies beyond the site-resolved reversal horizon (T3 ≈ 4 T2), and the profiled structural
> gain there stays ≤ 1.6 even if the entire echo were quantum-only.
>
> **(3) Classically expensive and structure(-ensemble)-bearing, but with no applicable quantum algorithm.** This is
> physics-based all-atom sampling of folding kinetics and ensembles. The negative here is not classical ease. No
> quantum algorithm with a super-quadratic speedup against practical MD has its preconditions met by a protein force
> field, and the quadratic routes cost ≥ 2.2 years per estimate even at 10 ns logical Toffolis.
>
> **Two further closures are orthogonal.**
> - Quantum memory and quantum data give a gain of exactly 1 per structural parameter (a theorem for selective-polarisation ¹H states).
> - Exact electronic structure hits the model floor before the solver floor (FeMoco E4 stays WEAK, at ≥ 10.8 QPU-days
>   per question).

**Evidence class per clause.**

| Clause | Evidence |
|---|---|
| (1a) learned energy | MEASURED, replicated by two round-3 lanes over 48 crops. Floor DERIVED |
| (1b) 40 µs echo | MEASURED agreement across families and estimators; INFERENCE that this is F_∞; provisional pending R-1 |
| (2) | MEASURED model gains (N = 10 Fisher model, rotor-averaged, nuisance-profiled; unverified lane). Reversal envelope LITERATURE-SUPPORTED from model solids (Sánchez 2022, arXiv:2112.00607, as verified by the lane) |
| (3) | LITERATURE-SUPPORTED survey plus MEASURED preconditions plus DERIVED floor; unverified lane |

### 3.2 Scope

This negative covers only the following. None of it is a proof that no quantum algorithm can ever help protein science.

- **Learned energy.** One energy class (esmprior_v1/A80: white-box, pair-additive). Measured at L ≤ 150, extrapolated to
  500.
- **NMR.**
  - Two proteins' ¹H networks: 1UBQ and 1PGA.
  - OTOC(1) classical reach: 1UBQ p19/p245, 8 series, one field orientation, a static-coupling isolated model, N ≤ 22.
  - Value computations: N = 10 Fisher models on 4 probes.
  - Reversal envelopes: from model solids (adamantane, polycrystals), not from proteins.
- **All-atom.** Three proteins (Trp-cage, protein G, ubiquitin); amber14 + GBn2 and explicit boxes; preconditions
  measured on Trp-cage; an arXiv survey for 2019–2026 (341 records, 53 cited).
- **Electronic structure.** A curated census of 20 cofactor entries.
- **Execution.** Everything was run on simulators. Fault-tolerant costs come from in-repo resource models, and no
  hardware was used. **Simulator runtime is not physical quantum runtime.**

### 3.3 Falsifiers: what would change the answer

Each falsifier is tied to a clause. The ranking is by how plausibly it could happen.

1. **Clause (3): an s ≥ 3 quantum algorithm for chaotic, non-polynomial, multi-basin Langevin dynamics.**
   - It must be super-quadratic against practical fixed-step MD or weighted ensemble, not against worst-case
     weak-error bounds, grid solvers, or the chain's own mixing time.
   - It must come with a compiled force oracle and T\*_Q,s ≤ 1 day at a stated t_T.
   - This is the **only examined regime that is not resource-dead**: a hypothetical s = 4 gives T\*_Q,4 = 2.6 h–10 d at
     10 ns [DERIVED].
2. **Clause (2): a measured protein site-resolved reversal horizon T3/T2 ≥ 15, together with converged classical
   reach t_cl ≤ 80 µs.**
   - That combination gives g ≈ 2–3.3 (category-1 usefulness at most).
   - g ≥ 10 would need T3/T2 ≳ 20–50 **and** t_cl ≲ 40 µs. K-119 now puts 1UBQ exactly at that boundary.
   - This is an experiment (microcrystalline GB1 or ubiquitin). It is the single most important empirical unknown behind
     the NMR negative.
3. **Clause (1b): the R-1 replication fails.** A b-aware exact family and a thermodynamic estimator disagree by > 3σ at
   t ≤ 40–60 µs on another probe, protein or orientation. This reopens only category-3 physics; K-105 stays.
4. **K-109: RT-DQ-methyl and the cross-family DQ ladder show classical reach ≤ 40–50 µs at the FI-bearing sites, and
   a protein site-resolved T3_DQ/T2 ≥ 19 is measured.** This gives g ≈ 2–3 (category 1 at most).
5. **Clause (1a): a learned-energy crop family where the full classical portfolio needs > 1e7 evaluations** to reach a
   basin transmitting ≥ 1 MDE, **plus** a super-quadratic algorithm for white-box pair-additive energies.
6. **Logical Toffolis in the sub-ns range.** This would reopen the quadratic routes: K-101, and K-117 at s = 2, where
   T\* ∝ t_T² needs t_T ≲ 0.4 ns for 1 day on the best-case folder [DERIVED].
7. **A quantum-memory separation** for a structure-relevant, exponentially large property family that survives nuisance
   profiling.
8. **FeMoco E4:** a measured σ_m ≤ 1.2 kcal/mol **and** a best classical ranking error ≥ 5 kcal/mol at ≥ 100 orbitals.
   This would be chemistry level, not protein-structure level.

---

## 4. KILLBOOK entries (K-117+) and corrections

Columns are the same as KILLBOOK Section B. Evidence paths are relative to `research/`.

### 4.1 New entries

| K-id | Killed direction | Kill type | What did *not* disappear under ablation | Evidence | Reopen only if |
|---|---|---|---|---|---|
| K-117 | Quantum dynamics or sampling algorithms for **physics-based all-atom** protein folding kinetics and ensembles, explicit or implicit solvent. Covers Carleman, KvN/Liouville, Fokker–Planck/LCHS/Schrödingerisation, overdamped-FP rate estimation, nonlinear-SDE algorithms, oscillator algorithms, continuous Gibbs samplers (Witten-Laplacian, QRELD), QMCMC/free-energy estimation, nonreversible-chain speedups, MSM/annealer path sampling, and quantum-computed forces | **No applicable algorithm (not classical ease).** Literature: 12 families, 53 verified arXiv records; every claim of s > 2 is against the wrong baseline or needs a missing precondition. Measured preconditions (Trp-cage, amber14 + GBn2): Carleman R ≥ 4.3e3–1.2e5 (R < 1 needed; ∞ for NVE); negative curvature on 8/10 thermal snapshots; λ_max = 2.1–3.2 ps⁻¹. Derived floor: T\*_Q,2 ≥ 2.2 yr at t_T = 10 ns (≥ 2.2e4 yr at 1 µs); B\*₂ ≥ 4e11 steps exceeds every twin cost. **Unverified** | Nothing. Weighted ensemble (NTL9 250 GPU-days), MSM, metadynamics and REST2 supply the capability. A hypothetical s ≥ 3 would break even: T\*_Q,3 = 1–160 d and T\*_Q,4 = 2.6 h–10 d at 10 ns | `experiments/ROUND4/allatom_superquadratic/` (`families.json`, `floor_allatom.json`, `floor_allatom_table.md`, `work/S4_1L2Y.json`, `work/S5_*`, `lit/records.json`) | A quantum algorithm with s ≥ 3 against practical fixed-step MD or weighted ensemble, whose preconditions hold for chaotic, non-polynomial, multi-basin Langevin dynamics, **and** a compiled force-oracle Toffoli count, **and** T\*_Q,s ≤ 1 day at a stated t_T. **Or** logical Toffolis ≲ 0.4 ns (s = 2, best-case folder) |
| K-118 | **Programmable analog dipolar quantum simulators** (Rydberg tweezers, polar molecules, NV ensembles, natural NMR solids) as the quantum side of R1-SIM: the protein ¹H secular-dipolar echo F_ab to σ = 0.01 at 40–120 µs for 20–100 spins | **Practical.** DERIVED structural obstruction: the traceless rank-2 target cannot be reached from electric-dipole exchange by global Floquet rotations, and the graph is non-bipartite. The only fix is a ±C3 encoding-swap composite (exact at zeroth order). MEASURED sensitivity: σ is reached at 1.4–1.7% coupling error, 0.25–0.53% position error, 0.10–0.38% motion, 1.1–1.4% isotropic residual. INFERENCE budget: 42–100σ demonstrated, 1.3–16σ optimistic near-term, 1.2–6σ best undemonstrated. **Unverified** | Nothing. At 40 µs, exact b-aware classical clusters reach σ in minutes (K-119). At 80–120 µs neither the classical nor the analog route reaches σ | `experiments/ROUND4/analog_simulator/` (`sens_summary.json`, `floquet_*.json`, `budget.json`, `lit.json`) | **All of:** a programmable-geometry platform demonstrating a traceless dipolar coupling (Jz/Jxy = −2, isotropic residual ≤ 1%) with Floquet reversal; per-atom loss ≤ 0.5%; pulse error ≤ 0.003 rad over ≥ 80 cycles; motion ≤ 0.04% of spacing, in ≥ 100-atom arbitrary 3D arrays; **and** a classical cross-family F estimate that fails at σ at a time where the site-resolved visible signal is ≥ 1σ |
| K-119 | **R1-SIM-early**: "the converged secular ¹H echo F_ab at t ≈ 40 µs, inside every T3 estimate, is beyond σ-level classical reach" (CRITIC C1) | **Measured cross-family agreement, provisional.** Post hoc under PREREG H-2, plus pre-registered Addendum B corroboration; the literal parent rules could not fire because their comparator was refuted (deviation D-R4-2). Two exact b-aware families (5 implementations across 3 independent code paths) agree to ≤ 0.0055 on 8/8. Thermodynamic E1 vs E2 ≤ 0.0045. b-aware vs spinDMFT ≤ 0.0096. Isolated {a, b} clusters of 10–12 spins are within σ on 3/3 b-remote series. Cost: 2.7–19 single-core CPU-min for all 8 series, vs 2.8–10 h per probe on an FT QPU (DERIVED) | Nothing at 40 µs | `experiments/ROUND4/spindmft/` (`analysis.json`; `verify_classical/verify_summary.json`; `verify_resource/verify_summary.json`, `breakeven_40us.json`; `verify_relevance/relevance_checks.json`); `experiments/ROUND4/tx_early/verify_classical/verify_summary.json`; `experiments/ROUND4/director/cross_family.json` | On replication (R-1: 1PGA p390, 1UBQ p487, ≥ 2 further b0 orientations, and optionally the rotor-averaged model), an exact b-aware family and a thermodynamic estimator disagree by > 3σ on ≥ 2 series at t ≤ 40–60 µs. Category 3 only. **Never revives K-105** |
| K-120 | **Methodological.** The round-3 hybrid comparator F̂_∞ = H_∞(CSD) + X_N, and every convergence rule or approximation target stated on X = F − H − floor: T-X-early's \|X₂₂ − X₂₀\|, the ROUND3 T-X0 to T-X3 rules, the K-116 revival trigger "X drifts ≥ 0.01 per step", R3-HYB's T-H1, and analog revival item 4. Also single-family step or plateau convergence claims for F_ab | Measurement: pooled dF/d(H + floor) = −0.03 ± 0.10 at 40 µs (1 required; z = 6.2); X rises on 8/8 series while F is flat; the hybrid is 2.7–9.5σ below the b-aware values (0/8 within σ); the probe-family plateau is 2.5–7σ off at sites with out-of-cluster partners. Derivation: F = 1 − 2 w_b, so norm spreading away from b leaves F unchanged | N/A (a comparator and criterion retirement) | `experiments/ROUND4/spindmft/analysis.json` §4.4; `spindmft/verify_classical/verify_summary.json` (`flatX_recomputed`); `tx_early/backtest.json`; `tx_early/verify_resource/tracking.json`; `tx_early/verify_relevance/crossfamily.json` | Never as an F_∞ estimator at t ≤ 80 µs. X may be reported as a diagnostic. Convergence claims must be on F, in ≥ 2 b-aware families with M2_b coverage reported, plus a thermodynamic estimator |

### 4.2 Corrections to existing entries

**K-105** (secular OTOC(1)). Replace the "Kill type" column and the 2026-09-28 correction bullet.

- **Load-bearing arm: the reversal horizon of a site-resolved echo.**
  - Under the local polarisation-echo envelope (T3 ≈ 4 T2), the profiled median joint gain is 1.09–1.60 with
    moderate priors (1.13–2.10 with none). This holds **even at t_cl = 0**, i.e. if the whole converged echo were beyond
    classical reach. So the arm no longer depends on N = 10 twins.
  - With t_cl = 40 µs (K-119): 1.06–1.33 under PE, and 1.36–2.23 under the global LE envelope.
  - [MEASURED, `ROUND4/redteam_kills/profiled_summary.json`; N = 10 Fisher model, rotor-averaged, nuisance-profiled;
    unverified lane]
- **Secondary arm:** out-of-family per-pair motional scaling leaves a structural bias of 0.1–11× CRB_q. That caps the
  accuracy gain at 1.06–1.52 (PE).
- **Removed as load-bearing:**
  - "forward-model error 5–66σ": the misfit is removed by profiling offsets, reversal scaling and order-parameter
    families, which retains 18–83% of the FI without reducing g;
  - "value ≤ 1.2–3 even with ideal reversal": ideal reversal at t_cl = 80 µs gives 2.5–6.9.
- **Reopen only if:**
  - for usefulness (g ≈ 2–3.3): a measured protein **site-resolved** T3/T2 ≥ 15 **and** converged classical reach
    t_cl ≤ 80 µs;
  - for the R1 revival bar (g ≥ 10): T3/T2 ≳ 20–50 **and** t_cl ≲ 40 µs, which is at the boundary K-119 establishes for
    1UBQ.

**K-109** (DQ echo). Replace the "Kill type" and "Reopen" columns.

- **Load-bearing arm: value against the measured classical reach.** Non-methyl butterflies are step-stable to 80 µs at
  N = 18 (1UBQ p19; a single-family step statistic, C-R4-13). With secular transfer on the classical side, g_med is:
  - 1.27 / 1.32 / 1.78–1.97 at 12.5 T2;
  - 1.53 / 1.62 / 2.09–2.50 at 19 T2.

  [MEASURED, `ROUND4/redteam_kills/sitewise_tcl.json`]
- **Retracted:** "the ε = 3e-5 twin reproduces the echo to 140–220 µs; g ≤ 1.16; reopen at T3_DQ/T2 ≥ 50". This was an
  N = 10 artefact: at N = 10 everything is classically reachable.
- **Residue:** 1PGA p390, methyl butterfly HG21/THR53 (RT-DQ-methyl, §2 item 12).
- **Reopen only if all of these hold:**
  1. a measured protein site-resolved T3_DQ/T2 ≥ 19;
  2. converged classical reach ≤ 50 µs at the FI-bearing butterflies, from a partner-complete, rotor-averaged,
     **cross-family** ladder;
  3. a profiled g_med ≥ 2 with secular transfer on the classical side.

**K-111** (methyl rotors). Replace the "Kill type" column and the correction bullet.

- **Load-bearing arm: resolvability plus classical exactness.**
  - The identifiable many-body quantity is the partner-state doublet J. It is *not* degenerate with V3, so CRITIC C2's
    degeneracy argument is incomplete [DERIVED].
  - Against glass disorder σ_V3 ≥ 1 meV, the doublet is resolved in 0/32 pair cases at V3 = 60–100 meV and 2/32 at
    30 meV [MEASURED from lane data].
  - J is an exact 2-rotor classical computation (seconds).
- **Reopen only if all of these hold:**
  - a real protein has ≥ 3 coupled methyls with V3 ≤ 50 meV;
  - \|J\| ≥ 2.355 Δ \|d ln Δ/dV3\| σ_V3 with a measured σ_V3;
  - the needed cluster exceeds exact 3–4-rotor reach.

**K-116** (R1-SIM against exact F_N). Its reopen clause ("X drifts ≥ 0.01 per step…") is void under K-120. Replace it
with:
> Only as R1-SIM-late, in a spin-off register outside the mission. Reopen when all three hold:
> - (i) two b-aware cluster families plus a thermodynamic estimator fail to agree within σ at N ≥ 22–24;
> - (ii) this happens at times where the site-resolved reversal envelope leaves ≥ 1σ of visible signal under physical T2;
> - (iii) a costed quantum estimator, digital or analog (see K-118), beats that classical portfolio.
>
> Never revives K-105.

**K-115** (QPE electronic structure). Add to the FeMoco E4 note: "WEAK. Survives only with a measured σ_m ≤ 1.2
kcal/mol (σ_best = 5, 1 Å lever), a best classical error ≥ 5 kcal/mol, and ≤ 30 energies at ≤ 100 orbitals (≥ 10.8–20.5
QPU-days per question). arXiv:2601.04621 concerns the resting state and is not load-bearing."

**K-107.** Scope note: "A80 learned energy only. The physics-force-field regime is K-117, which has a different kill
type (no applicable algorithm, not classical ease)."

**KILLBOOK "Corrections to earlier kills (2026-09-28)" block.** Supersede its K-105/K-109 bullet and its K-111 bullet
with the entries above, via a dated note (do not delete).
- The K-105/K-109 bullet's "load-bearing = forward-model error + value" is superseded.
- The K-111 bullet's "identifiability" is superseded.

**CRITIC C1.** Withdrawn at 40 µs. Replacement:
> The round-3 hybrid double-subtracts at early times, and F does not carry the (1 − H)/N floor as an additive bias
> (MEASURED in-family at N ≤ 22). Probe-centred clusters are still 2.5σ and 6.5σ low on 2/8 series (p19 b8, p245 b7),
> because b's strongest partners enter only at ranks 24–48. Clusters that contain b's partners remove this. At
> 80–120 µs the question is open, as a cluster-family problem (§1.3).

---

## 5. The single strongest publishable claim of the program

**Claim (negative; NMR echo route).**

> In an idealised, isolated, static-coupling model of the ubiquitin ¹H dipolar network (629 protons; probes p19 and
> p245; 8 probe–butterfly series; one field orientation), the first-order dipolar echo (OTOC(1)) F_ab(t) at
> t = 40 µs is computed classically to σ = 0.01. That time lies inside every published reversal-horizon estimate
> (T3 ≈ 4–6.7 T2 ≈ 32–66 µs).
> - Two exact cluster families that contain both the probe and the butterfly site's dominant dipolar partners (≤ 22
>   spins; five implementations across three independent code paths) agree to ≤ 0.0055 on 8/8 series.
> - Two independent thermodynamic-limit estimators (spinDMFT-embedded and classical-spin-dynamics-embedded) agree
>   with them to ≤ 0.0096.
> - The total cost is 2.7–19 single-core CPU-minutes for all 8 series. A fault-tolerant Trotter simulation would take
>   2.8–10 h per probe, even under its most favourable assumptions.
> - Probe-centred cluster ladders, the convention in earlier work including this program's round 3, plateau 2.5–7σ
>   away on the two series whose butterfly partners they omit. So single-family convergence is not evidence of
>   classical failure.

**Evidence class.**
- MEASURED: the agreement across families and estimators, and the classical costs. The lane was reproduced
  bit-identically by 3 verifiers, extended to all 8 series by one of them, and cross-checked here.
- DERIVED: the quantum cost, from the in-repo resource model.
- INFERENCE: that the common value is the N → ∞ echo, and that the result generalises beyond 1UBQ, orientation 0 and
  the static-coupling model.
- It is not a theorem.
- Pre-submission requirement: R-1 (about 1.5–2 CPU-h, splittable).

**Companion statement (weaker evidence; state it separately).** Beyond the site-resolved reversal horizon, the profiled
structural gain of the echo over classically usable NMR data stays ≤ 1.6 (moderate priors) even if the whole echo were
quantum-only [MEASURED on N = 10 Fisher models, 4 probes; single unverified lane; envelope LITERATURE-SUPPORTED from
model solids, not proteins]. Together the two statements say: for protein ¹H echoes, a quantum simulator is not needed
where the signal is observable, and not useful where it might be needed.

**Relation to prior work.**
- This points against treating protein ¹H OTOC echoes at observable times as a beyond-classical target. That framing
  appears in O'Brien et al., arXiv:2109.02163, and in the NMR-OTOC work the spinDMFT relevance verifier cites as
  arXiv:2510.19550 (LITERATURE-REPO; not re-verified here).
- It does not refute those works: their molecules, observables and orders differ.
- No spinDMFT or dipolar OTOC extension was found in the literature (lane search; abstract level).

**Why this claim and not the runners-up.**
- The DG-seeding result (K-107) is replicated and leakage-audited. But gradient folding on predicted distograms is
  established practice, so it adds little novelty as a publication.
- K-114 is the only theorem, but it covers one state family.
- The all-atom negative (K-117) is the most consequential for future work, since it is the only non-resource-dead
  regime. But it is unverified and rests on a literature survey plus one protein's preconditions.

---

## 6. For the orchestrator: state updates, deviations, lessons, ledger

**Pre-registration deviation entries to add to `PREREG_G1_C1_Q4.md`** (dated; no threshold is changed retroactively):
- **D-R4-1.** T-X-early was not executable under the per-agent cap: the minimum complete test is 161 CPU-min against
  90. The recorded outcome is KEEP OPEN by default. The criterion is retired as ill-posed (K-120).
- **D-R4-2.** The spinDMFT literal rule could not fire because its comparator was refuted by MEASURED data. K-119 is
  closed **post hoc** under H-2 (explicit thermodynamic F̂_∞ + cross-family check), with pre-registered Addendum B as
  corroboration. It is marked provisional pending R-1.
- **D-R4-3.** H-2 is extended. "Cross-family" means:
  - ≥ 2 cluster construction rules, each containing b's dominant partners, with M2_b coverage reported;
  - plus a thermodynamic estimator;
  - single-family step or plateau statistics never establish convergence.
- **Before any new rule is registered:** cost it against the per-agent cap (the T-X-early lesson).

**State files.**
- **`KILLBOOK.md`:**
  - add K-117 to K-120;
  - apply the §4.2 corrections as dated supersession notes.
- **`CURRENT_STATE.md`:**
  - record this synthesis;
  - R1-SIM: 40 µs KILLED (provisional); 80–320 µs in the spin-off register;
  - remove the G1 exponent from the pending inputs;
  - note that the pending N = 20 `nmr_cone.py` governor runs now have **low decision value**. Recommend replacing them
    with R-1, RT-DQ-methyl and T-F80, but only on the user's go-ahead.
- **`OPEN_QUESTIONS.md`:**
  - mission items: K-117 falsifier 1 (s ≥ 3 algorithm), the protein site-resolved T3/T2 experiment, RT-DQ-methyl,
    FeMoco σ_m;
  - spin-off register: T-F80, 120–320 µs.
- **`SCIENTIFIC_MEMORY.md`** lessons:
  1. **A flat ladder in one cluster family is not convergence.** Check that the observable site's own dominant
     couplings are inside the cluster (M2_b coverage). One missing spin moved F by 7σ.
  2. **Do not build estimators or convergence tests on a bookkeeping component.** X ≡ F − H − floor rises as the floor
     falls, even when F has converged. Test the observable across families.
  3. **Raw forward-model misfit is not a kill arm.** Profile the nuisance families and report the residual bias.
  4. **Name the kill type.** The all-atom regime is a no-algorithm negative, not a classical-ease negative, and it is
     the only examined regime a new algorithm could open.
  5. **Cost pre-registered tests against the compute cap** before registering them.
- **Housekeeping still open:**
  - H-1: pin the level scale in the charter;
  - the claim-category label (lanes still write "category 3 (physics simulation)");
  - DG headline wording (R3 CRITIC §2.4(4));
  - tally weights;
  - the `BREAK_EVEN.md` physics row.

**Process and compliance notes [MEASURED from lane and verifier reports].**
- Every run was single-threaded.
- Peak RAM was ≤ 1.53 GB.
- Every run longer than 3 min was checkpointed.
- The harness auto-backgrounded some long commands once they passed its 600 s tool limit: `tx_early`, the `spindmft`
  lane, the `spindmft` resource and relevance verifiers, and `redteam_kills`. Each was bounded, and none of them was detached by the
  agent.
- The `spindmft` relevance verifier stopped its own orphaned process (PID 38536) and touched no other process.
- **Out-of-folder side effects:**
  - The `spindmft` resource verifier's import created a regenerable, git-ignored bytecode file,
    `ROUND3/r1sim_exact_reach/verify_resource/__pycache__/pplus_echo.cpython-313.pyc`.
  - The `spindmft` classical verifier deleted a `.pyc` its own import had created in the lane folder.
  - No source or data file outside ROUND4 was modified. Nothing was committed.

**Round-4 compute [MEASURED from reports].**

| Scope | CPU-min |
|---|---|
| `tx_early` | ≈ 80 |
| `spindmft` | ≈ 58 |
| `allatom_superquadratic` | ≈ 31 |
| `redteam_kills` | ≈ 57 |
| `analog_simulator` | ≈ 46 |
| **Lanes, total** | **≈ 272** |
| `tx_early` verifiers | 59 + 8 + 25 |
| `spindmft` verifiers | 47 + 52 + 13 |
| **Verifiers, total** | **≈ 204** |
| Director | < 1 CPU-s of arithmetic |

No quantum resources were used anywhere. No leakage: native geometry defines the physical instance only, and all FI and
CRB values are ORACLE-geometry scientific analysis, used for no selection.

**Files written by the director:**
- `research/experiments/ROUND4/SYNTHESIS.md` (this file);
- `research/experiments/ROUND4/director/cross_family.py`;
- `research/experiments/ROUND4/director/cross_family.json`.
