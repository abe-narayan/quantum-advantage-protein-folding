# Round 4 completeness critic

_2026-09-28. File: `research/experiments/ROUND4/CRITIC.md`. Scripts and outputs: `research/experiments/ROUND4/critic/`
(`critic_arith.py` → `critic_arith.json`; `fi_nscale.py` → `out/fi_*.{npz,json}`; `fi_analyze.py` →
`fi_nscale_summary.json`)._

**Scope.** I checked the 5 lane reports, the 6 verifier verdicts and `ROUND4/SYNTHESIS.md` against the state files
(`CURRENT_STATE`, `KILLBOOK`, `ROUND3/SYNTHESIS`, `ROUND3/CRITIC`, `PREREG_G1_C1_Q4` Round 4). The question was what the
round missed: an adversary or check that could flip a verdict, or an over-claim.

**Tags.** MEASURED / DERIVED / THEORETICAL / LITERATURE-SUPPORTED / INFERENCE / UNPROVEN. **[CR4-A]** and **[CR4-B]**
mark my two checks.

**Compute.** CR4-B: 36 single-thread CPU-min in 9 runs (the largest 7.1 CPU-min), checkpointed after every Jacobian
column. Arrays are ≤ 15 MB, so peak RSS is well under 1 GB; that bound is DERIVED, since RSS was not logged. CR4-A and
the analyses: < 1 CPU-min, JSON only. Bytecode writing was disabled, and I checked that no `.pyc` appeared outside
`critic/`. Nothing outside `ROUND4/critic/` and this file was written. No commit.

---

## 0. Bottom line

1. **No verdict flips toward a quantum advantage.**
   - The synthesis's answer stands: no supported claim in categories 1–6 for protein-structure computation in the
     examined regimes.
   - g ≥ 10 (the R1 revival bar) is reached nowhere, including in my check.
   - Two statements rest on a narrower base than the synthesis says: the category-1 part of the NMR negative, and
     several headline numbers (items 3–5).
2. **[CR4-B] The re-based K-105 arm was computed on exactly the cluster type that round 4 showed can be 7σ off.**
   - The red team's profiled gains use the probe-centred N = 10 Fisher models (`amp_lib.job_geometry`).
   - In those models, 2–3 of the 4 butterflies per probe carry only **4–23% of their M2** inside the cluster. For
     example, 1UBQ p19 HG22/ILE3 has 4%, and its methyl partner HG23/ILE3 (82% of M2) is missing. This is the same
     failure mode as C-R4-1 [MEASURED].
   - Adding the two strongest missing partners (b-aware, N = 12) gives these results under the site-resolved PE
     envelope (moderate priors, t_cl = 0):
     - g_med moves by **−0.03 to +0.08** and stays **< 2 on 4/4 probes**, max 1.57;
     - a size-only control (N = 12, probe-centred) moves 1PGA p390 to **1.86**;
     - **K-105 stands.**
   - Two things weaken it:
     - The per-parameter gains of the partner-starved butterflies rise by up to **+0.6 (PE)** and **+2.1 (LE)**.
     - LE medians rise by **+0.16 to +0.54**, reaching ≥ 2 on **2/4** probes at t_cl = 0, against 1/4 at N = 10.
   - So "≤ 1.6" is an N = 10 number. The margin on p390 is 0.14. The Fisher model is not converged in N, and the drift
     runs toward quantum [MEASURED].
3. **[CR4-A] The 40 µs cost framing is an over-claim.**
   - The synthesis says "2.8–10 h per probe on an FT QPU, even under its most favourable assumptions; 17–65× slower
     than one core". That uses a **1 µs** logical T layer.
   - At the **10 ns** logical gate time that the program itself calls generous (K-101, K-107, K-117), the same circuits
     take **68–736 s for all 8 series**. That is 0.06–0.65× the 19-CPU-min classical pipeline and 0.4–4.6× the 2.7-min
     exact-only route. In other words, parity with one core, and faster than it for the cluster circuit [DERIVED].
   - K-119 is a classical-ease result: minutes of CPU, trivially parallel. It must not be argued from a QPU ratio.
4. **[CR4-A] The time-window statements are wrong in two places, and the error matters under LE.**
   - "40 µs lies inside every published reversal-horizon estimate" is false. The PE half-maximum is **32–39 µs**
     (T2 = 8.0–9.8 µs), and A_PE(40 µs) = 0.34–0.48.
   - With the director's own merged spreads, the 80 µs residue is **2.2σ visible under LE** (rotor-averaged T2), with
     6/8 series ≥ 1σ. The synthesis says ≤ 1.2σ, taken from the relevance verifier's pre-merge spread of 0.039. Under PE
     it is 0.41σ.
   - So "80–120 µs is outside the mission" holds under PE only [DERIVED].
5. **[CR4-A] Two agreement numbers are overstated.**
   - "Thermodynamic estimators agree with the exact values to ≤ 0.0096": the maximum is **0.0114** (p19 b9, E1 vs SA2)
     and **0.0109** (p19 b8, spinDMFT vs PB20). Thermodynamic vs thermodynamic reaches 0.0136.
   - The "8/8 series" include **5 with 1 − F ≤ 5.3σ**. The discriminating evidence for K-119 rests on 3 series (p19 b1,
     p19 b7, p245 b7).
   - "No two classical families agree within σ at 80 µs" is false as written: the two exact b-aware families agree on
     2/8 [DERIVED].
6. **Structural point: one literature number now carries every NMR category-1 negative.**
   - That number is the site-resolved polarization-echo envelope (Gaussian, T3 = 4 T2), from adamantane, not from a
     protein.
   - It carries:
     - K-105's load-bearing arm;
     - the "outside the mission" status of 80–120 µs;
     - K-116's new reopen clause (ii);
     - thesis clause (2);
     - the only t_cl-independent K-109 arm (7.5 T2, itself INFERENCE).
   - Under LE, the NMR echo is a **category-1 near-miss** (g_med ≈ 1.5–2.3 at t_cl = 40 µs, 1.7–3.3 at t_cl = 0; N = 12),
     not a kill. The synthesis should say that the category-1 negative is conditional on the PE envelope. The negative
     for categories 2–6 and for g ≥ 10 is not conditional on it.
7. **K-109 and K-117 are weaker than stated.**
   - K-109 (C-R4-13) says "would still stand" if RT-DQ-methyl fails. In that case only an *unmeasured* protein envelope
     would hold it, so it should be recorded as would-be-WEAK. Its DQ Fisher models have the same partner deficit and
     are untested.
   - K-117's "a hypothetical s ≥ 3 breaks even for every folder" holds for generous G only. At central G, s = 4 at
     10 ns is up to 1 yr (lane README). K-117 has had no adversarial verifier.

---

## 1. Checks run

### CR4-A. Arithmetic audit of the synthesis's headline numbers [DERIVED from MEASURED files]

Inputs: `spindmft/verify_resource/breakeven_40us.json`, `director/cross_family.json` and
`redteam_kills/profiled_extensions.json`. Envelope functions are copied from `redteam_kills/analyze_profiled.py`.

| # | Synthesis statement | Recomputed | Verdict |
|---|---|---|---|
| A1 | "FT QPU 2.8–10 h per probe, even under its most favourable assumptions; 17–65× slower than one core" (§0.2, §5, K-119, `spindmft` row) | The verifier's model: depth-limited, unlimited factories, 1e4 shots, one QPU. At a **10 ns** T layer, all 8 series take: 629-qubit 30 Hz-cut **200 s**; dense **736 s**; 8 × 20-qubit b-aware cluster circuits **68 s**. Classical single core: **1141 s** (full pipeline) or **160 s** (exact b-aware N = 18 only). Ratios quantum/classical: **0.06–0.65** against the pipeline, **0.42–4.6** against exact-only. At 1 µs: 17–65 and 42–459 | **Over-claim.** "Most favourable" is not the program's own generous convention. The correct statement: at 40 µs the classical computation costs minutes on one core and parallelises trivially, so no resource advantage is meaningful at either gate speed. The cluster circuit is also only as accurate as its cluster family |
| A2 | "80–120 µs: at most 1.2σ visible (LE), ≤ 0.22σ (PE)" (§0.5, §2 item 2) | Director spreads: 0.075 at 80 µs, 0.126 at 120 µs. With rotor-averaged network T2 = 9.77 µs, A_LE(80) = 0.29 and A_PE(80) = 0.055, giving **2.19σ (LE)** and **0.41σ (PE)**. **6/8** series ≥ 1σ under LE at 80 µs. At 120 µs: 0.43σ (LE), 0.02σ (PE). With static T2 = 8.04 µs: 0.94σ (LE) and 0.10σ (PE) at 80 µs | **Stale number.** Under LE the 80 µs residue is observable. The conclusion "outside the mission" holds only under PE |
| A3 | "40 µs lies inside every published reversal-horizon estimate (T3 ≈ 4–6.7 T2 ≈ 32–66 µs)" (§5, K-119) | PE half-maximum = 4 T2 = **39.1 µs** (rotor-averaged) or **32.2 µs** (static). A_PE(40) = 0.48 / 0.34; A_LE(40) = 0.84 / 0.75. A_LE stays 0.59–0.73 at 50–60 µs | **False for PE.** 40 µs sits at the PE half-maximum and inside the LE window. K-119 does not test 50–66 µs, where under LE the echo is still 40–73% visible |
| A4a | "Thermodynamic estimators agree with them to ≤ 0.0096" (§0.2, §5) | At 40 µs, max \|thermodynamic − exact\| = **0.0114** (p19 b9) and **0.0109** (p19 b8); thermodynamic vs thermodynamic **0.0136** (p19 b8). All estimates are within σ on 6/8 (the director's own §1.3) | **Overstated.** "≤ 0.011–0.014; within σ on 6/8" |
| A4b | "8/8 series" as evidence of σ-level reach | 1 − F at 40 µs: 0.40 / 0.13 / 0.027 / 0.053 (p19 b1/b7/b8/b9) and 0.022 / 0.24 / 0.044 / 0.028 (p245). **3/8 have 1 − F ≥ 0.1.** The two series that exceed σ in A4a have 1 − F = 2.7σ and 5.3σ | Scope caveat. σ-level agreement is non-trivial on 3 series. The claim should report dynamic range, or relative error \|ΔF\|/(1 − F) |
| A4c | "No two classical families agree within σ on any series: 0/8 at 80 µs" (§0.5, §2 item 2) | The exact b-aware families agree within σ on **2/8** (p19 b1: 0.006; p245 b1: 0.009). "All estimates within σ" is 0/8 | Wording |
| A5 | K-109 has no t_cl-independent arm (§4.2) | Local DQ envelope (7.5 T2, INFERENCE), secular transfer on the classical side, t_cl = 0: g_med **1.96 / 1.29 / 1.24** (p390 / p19 / p245; moderate); **2.47** / 1.41 / 1.39 (none). At t_cl = 40: 1.83 / 1.26 / 1.17 | This is the K-105-type arm for K-109. It holds at moderate priors, with p390 **0.04 below 2**, and fails with no priors on p390. N = 10-conditioned (see CR4-B) |

### CR4-B. Does the K-105 value arm survive partner-complete Fisher models? [MEASURED]

**Why.**
- K-105 now rests entirely on the red team's profiled gain g = CRB_cl²/CRB_q² under the PE envelope, which stays below
  2 even at t_cl = 0.
- Those Jacobians come from probe-centred N = 10 clusters. The butterflies in them are the 3 farthest sites plus the
  nearest one, so they sit on the cluster periphery.
- Round 4 showed that such clusters misplace F_ab by 2.5–7σ at butterflies whose dominant partner is missing. The
  derivative of F_ab, which is what enters the Fisher information, is exposed to the same error.

**M2_b coverage of the red team's N = 10 butterflies** (fraction of Σ_j d_bj² inside the cluster; static couplings):

| Probe | Butterflies (coverage) | Strongest missing partner (share of M2_b) |
|---|---|---|
| 1UBQ p19 | HA/GLN2 0.36, HG3/GLN2 0.76, **HG22/ILE3 0.04**, **HA/GLU16 0.09** | HG23/ILE3 (0.82), HG2/GLU16 (0.64), HB2/GLN2 (0.52) |
| 1UBQ p245 | HB/ILE30 0.33, **HA/LYS27 0.13**, HA/LYS29 0.58, HB2/LYS29 0.89 | HG3/LYS27 (0.49), HG21/ILE30 (0.20) |
| 1PGA p325 | HA/TRP43 0.79, HE3/TRP43 0.54, **HG1/THR44 0.16**, **HB3/TRP43 0.16** | HB/THR44 (0.62), H/TRP43 (0.39) |
| 1PGA p390 | HA/PHE52 0.64, **HE3/TRP43 0.13**, **HG1/THR44 0.23**, HG21/THR53 0.66 | HB/THR44 (0.62), HB2/TRP43 (0.42) |

**Method** (`critic/fi_nscale.py`).
- The red team's forward model is reused unchanged: `profiled_gain.setup/couplings/moved`, rotor-averaged couplings,
  base 1 kHz offsets (seed-3 draw, prefix-identical), the same structural parameters, dt = 2 µs and σ = 0.01.
- Three clusters:
  - **base10**: the red team's cluster;
  - **baware12**: base10 plus the two strongest missing butterfly partners, which lifts coverage of the starved
    butterflies to 0.55–0.86;
  - **probe12**: the next 2 probe-nearest spins, as a size-only control. Run on 1PGA p390 only.
- FD Jacobian columns: structural parameters, eps0 and eps_g. Offsets and η are held at base values. This is the
  "moderate-partial" profile.
- Gains are computed with the red team's own `analyze_profiled.gains` at physical T2.

**Validation [MEASURED].**
- base10 reproduces the red team's stored S0/G0 to ≤ 6e-17 and 0.0.
- The red team's full N = 10 npz reproduces its `profiled_summary.json` exactly (difference 0.0).
- Truncating echo rows beyond 160 µs changes no PE/LE g_med at 2 decimals.
- The partial profile (Omega and η fixed) differs from the full moderate profile by ≤ 0.01 under PE and ≤ 0.12 under LE
  at N = 10.
- The full no-prior profile (Omega and η free) was **not** recomputed at N = 12.

**Median profiled gain g_med, physical T2** (moderate-partial unless marked; t_cl = 0 / 40 µs):

| Probe | PE, N = 10 | PE, b-aware N = 12 | PE known, N = 10 → 12 | LE, N = 10 | LE, b-aware N = 12 | LE known t_cl = 0, N = 10 → 12 |
|---|---|---|---|---|---|---|
| 1UBQ p19 | 1.10 / 1.07 | 1.14 / 1.12 | 1.12 → 1.21 | 1.40 / 1.35 | **1.71 / 1.54** | 1.69 → **2.23** |
| 1UBQ p245 | 1.12 / 1.06 | 1.18 / 1.12 | 1.21 → 1.19 | 1.50 / 1.36 | **2.04 / 1.83** | 1.86 → **2.24** |
| 1PGA p325 | 1.17 / 1.10 | 1.25 / 1.12 | 1.33 → 1.50 | 1.53 / 1.40 | 1.69 / 1.48 | 2.18 → **2.69** |
| 1PGA p390 | 1.60 / 1.33 | 1.57 / 1.35 (probe12: **1.86 / 1.44**) | 1.49 → 1.40 (probe12: **1.95**) | 2.97 / 2.28 | 3.14 / 2.23 (probe12: 3.34 / 2.29) | 2.70 → 3.15 (probe12: **4.57**) |

**Per-parameter gains for butterflies that gained their partner** (moderate, t_cl = 0, N = 10 → b-aware N = 12):

| Probe, parameter | PE | LE |
|---|---|---|
| p245, radial_HA/LYS27 | 1.17 → **1.80** | 1.59 → **3.69** |
| p390, radial_HE3/TRP43 | 1.38 → **1.91** | 1.92 → **3.60** |
| p325, radial_HE3/TRP43 | 1.29 → 1.58 | 2.18 → **3.12** |

- p390's rigid_res44 falls, 1.72 → 1.16 under PE.
- The per-parameter maximum under PE (known priors) reaches 2.05–2.16 at N = 12 on 2/4 probes, against a maximum of
  1.71 at N = 10.

**Reading.**
1. **K-105's PE arm survives this attack.**
   - g_med stays below 2 in 9/9 probe × variant cells at moderate priors (max 1.86) and in 9/9 with known nuisances
     (max 1.95).
   - That this persists at converged size is INFERENCE: two N = 12 variants, no N ≥ 14.
2. **The number is not converged.**
   - A 2-spin size step moves p390 by +0.26 (moderate) and +0.46 (known).
   - Individual parameters move by −0.56 to +0.63 under PE.
   - The direction for partner-starved butterflies is upward, toward quantum.
   - "g ≤ 1.6" should be quoted as "≤ 1.6 at N = 10, ≤ 1.9 at N = 12, unconverged". The red team's own no-prior
     exception (p390, 2.10 at N = 10, full nuisance set) remains open at N = 12.
3. **Under LE, the correction is material.**
   - At t_cl = 40 µs, the range is **1.48–2.29** at N = 12, against 1.36–2.23 at N = 10 (C-R4-16).
   - At t_cl = 0, 2/4 probes are ≥ 2.
   - So the LE branch of K-105 is a category-1 near-miss on 1–2 probes, not a kill.
4. **K-109's DQ Fisher models** are built on the same clusters (p390: HE3/TRP43 13%, HG1/THR44 23%, HG21/THR53 66%).
   They are untested here: DQ Jacobians cost about 7.5× more. A5 shows p390 already within 0.04 of g = 2 under the local
   DQ envelope at N = 10.

---

## 2. What was missed

### 2.1 Adversaries and checks

| # | Missed or under-used | Where it bites | Why it matters |
|---|---|---|---|
| M-1 | **Partner-complete Fisher models** for the value arms (CR4-B was a first pass: N = 12, partial nuisance set, secular only) | K-105, K-109, C-R4-16, thesis clause (2) | Round 4's central lesson was applied to F_ab but not to ∂F_ab/∂θ, which carries the kill |
| M-2 | **No adversarial verifier on the three KILLS lanes** (`allatom_superquadratic`, `redteam_kills`, `analog_simulator`) | K-117, K-118, and the re-based K-105/K-109/K-111 arms | The program's final claim is a negative, so the error that matters is a false kill. K-117 is by the synthesis's own account the most consequential negative and the only regime that is not resource-dead. It rests on one lane's survey, and on preconditions measured for one protein |
| M-3 | **The window between 40 and 80 µs.** K-119 establishes t_cl ≥ 40 µs, while at 80 µs the families disagree by up to 0.075 | K-105 under LE; thesis clauses (1b) and (2) | Under LE the echo is still 59–73% visible at 50–60 µs. The existing runs record at steps 20/40/60 only. Adding steps 25/30 costs nearly nothing |
| M-4 | **Static vs rotor-averaged couplings for K-119** (C-R4-15 flags it; still untested) | K-105 at t_cl = 40 | The value model is rotor-averaged, and the reach was measured on the static model. The p19 b8 shift is intra-methyl, which rotation scales by −1/2 |
| M-5 | **Pre-registering R-1** with an informative-series criterion | K-119 (closed post hoc) | 5/8 series have 1 − F ≤ 5.3σ. Add relative error \|ΔF\|/(1 − F) and require the ≥ 3 informative series to pass |

### 2.2 Physical effects and literature

- **PE vs LE for a site-resolved protein echo.**
  - The PE anchor (Gaussian, T3 = 4 T2) comes from a full-text read in `R1_physics_feasibility`. The red team
    re-verified only the global R = 0.15 at abstract level.
  - Five conclusions now hinge on that one value (§0 item 6).
  - The decisive experiment is already named (§3.3, falsifier 2). The synthesis should add that under LE the NMR route
    is a category-1 near-miss, not a kill.
- **Butterfly selection.**
  - The 8 series use R1's instrument sites: the 3 farthest plus the nearest in an N = 10 probe cluster. That choice
    puts 2–3/4 butterflies at the cluster periphery by construction.
  - The publishable claim should say its sites are not a random or structure-relevant sample.
- **Everything else in ROUND3 CRITIC §2.3** (intermolecular ¹H, hyperpolarisation): unchanged.

### 2.3 Statistics

- **g_med is a median over 4 structural parameters per probe,** on 4 probes and 1 orientation. Per-parameter values
  move by up to ±0.6 between N = 10 and N = 12. Report g_max next to g_med.
- **K-119's "5 implementations across 3 code paths"** covers 2 cluster rules. PB20, FEPB and PP share one rule (the
  director says so). "Two thermodynamic-limit estimators" both embed an exact cluster, and their bath shares are ≤ 0.014
  (C-R4-8). They are corrections, not independent routes.
- **"Cost 2.7–19 CPU-min"** is the cost of one evaluation once the right family is known. Certifying convergence
  (two families to N = 22, E1, E2) took roughly 10× more across the verifiers. Neither changes the verdict.

### 2.4 Process

- **Background processes.** The harness moved long commands of 5 agents into the background, and one verifier had to
  stop its own orphaned process. The task rule says "no background/detached processes". Record this as a harness-induced
  deviation, not as compliance.
- **Peak RSS.** It is unlogged in the `spindmft` lane (C-R4-9) and in this check.

---

## 3. Over-claims in `ROUND4/SYNTHESIS.md`: proposed rewording

| # | Location | As written | Proposed wording |
|---|---|---|---|
| O4-1 | §0.2, K-119 row, §5, `spindmft` table row | "A fault-tolerant QPU needs 2.8–10 h per probe, even under its most favourable assumptions" / "17–65× slower" | "At a 1 µs logical T layer the FT circuit takes 2.8–10 h per probe. At 10 ns it takes 68–736 s for all 8 series, which is parity with one classical core. The classical computation costs minutes and parallelises trivially, so no resource advantage is meaningful at 40 µs [DERIVED, CR4-A1]." |
| O4-2 | §5, K-119 row | "t = 40 µs … lies inside every published reversal-horizon estimate (T3 ≈ 4–6.7 T2 ≈ 32–66 µs)" | "40 µs is at the site-resolved PE half-maximum (32–39 µs; A_PE = 0.34–0.48) and inside the global LE window (A_LE = 0.75–0.84). 50–66 µs is untested" |
| O4-3 | §0.2, §5 | "agree with them to ≤ 0.0096" | "Exact b-aware families agree to ≤ 0.0055 on 8/8. All exact and thermodynamic estimates agree within σ on 6/8, max spread 0.014 (1.4σ, on two series with 1 − F ≤ 5.3σ). The non-trivial evidence is 3 series with 1 − F = 0.13–0.40" |
| O4-4 | §0.5, §2 item 2 | "No two classical families agree within σ … 0/8" and "at most 1.2σ visible" | "All estimates within σ on 0/8 (the exact b-aware pair on 2/8). Visible spread 2.2σ under LE (rotor-averaged T2; 6/8 series ≥ 1σ) and 0.41σ under PE. Outside the mission under PE only" |
| O4-5 | §3.1 clause (2); §3.2 evidence table; §4.2 K-105 | "the profiled structural gain there stays ≤ 1.6 even if the entire echo were quantum-only" | "Under the site-resolved PE envelope, g_med ≤ 1.6 at N = 10 and ≤ 1.9 at N = 12 (moderate priors, 4 probes; unconverged in N, and the drift runs toward quantum). With no priors it is ≥ 2 on 1PGA p390 at N = 10. Under the global LE envelope g_med = 1.5–2.3 at t_cl = 40 µs and 1.7–3.3 at t_cl = 0 (N = 12): a category-1 near-miss, never g ≥ 10" |
| O4-6 | §0 item 7, C-R4-16 | LE range 1.36–2.23 at t_cl = 40 | "1.48–2.29 at N = 12 (CR4-B); N = 10-conditioned" |
| O4-7 | C-R4-13, §4.2 K-109 | "K-109 would still stand on its other reopen condition" | "If RT-DQ-methyl fails, K-109 is held only by the absence of a protein T3_DQ measurement plus the INFERENCE local DQ envelope (7.5 T2: g_med 1.96 on p390 at moderate priors, 2.47 with none). It would then be WEAK, not CLOSED-KILL. Its DQ Fisher models have the CR4-B partner deficit" |
| O4-8 | §3 answer | "No claim in any of categories 1–6 survives" | "No claim in categories 1–6 is supported. For the NMR echo, the category-1 negative is conditional on the site-resolved PE envelope, which is anchored in adamantane, not in a protein. The negatives for categories 2–6 and for g ≥ 10 do not depend on it" |
| O4-9 | §3.3 falsifier 1, K-117 | "T\*_Q,4 = 2.6 h–10 d at 10 ns" | Add: "at generous G; at central G, 17 h–1 yr (lane README)". Mark K-117 **unverified**, pending a pro-quantum verifier |

---

## 4. Verified non-issues (checked, no action needed)

- **Director cross-family table.** The summary counts in `cross_family.json` match §1.3: 8/8 exact b-aware ≤ 0.0055 at
  40 µs, all estimates 6/8, 0/8 at 80 and 120 µs.
- **Red-team reuse.** `profiled_summary.json` is reproduced exactly from its npz with its own functions. The red team's
  N = 10 base is reproduced by an independent driver (≤ 6e-17).
- **Truncation.** The echo beyond 160 µs carries no PE/LE weight at 2 decimals.
- **K-117 floor arithmetic.** T\*_Q,2 = 2.2 yr at t_T = 10 ns, and 1 day needs t_T ≈ 0.35 ns (∝ t_T²), consistent with
  the synthesis's "≲ 0.4 ns".
- **K-118.** The sensitivity tolerances were measured on the same probe-centred N = 10–14 family, but the demonstrated
  budget misses by 42–100σ. A factor-2 change in tolerances cannot flip it.
- **Leakage.** All Fisher and CRB values, including mine, use ORACLE geometry for information-content analysis only. No
  selection, no training.
- **Replacement kill types.**
  - K-120 (methodological) and the retirement of the X-based rules are sound (flat-X, z = 6.2).
  - K-111's resolvability arm is MEASURED from the lane's data.
  - FeMoco stays WEAK on σ_m. I did not re-derive it.

---

## 5. Recommended actions, ranked by decision value

All runs are single-threaded, ≤ 30 CPU-min each and checkpointed. Pre-register each one first.

1. **FI-PC: partner-complete Fisher models** (decides the category-1 margin of K-105 and K-109).
   - Probes: all 4 secular probes plus DQ 1PGA p390.
   - Clusters: b-aware and probe-centred N = 12, full nuisance set (Omega, η). About 13 CPU-min per secular probe at
     N = 12. The DQ runs need a typicality/Krylov Jacobian with common random numbers for N = 14–16.
   - **Stands** if g_med(moderate, PE) < 2 on 4/4 probes in both families at the two largest N, with \|Δg_med\| ≤ 0.1
     per ΔN = 2.
   - **Reopen as category-1 WEAK** otherwise.
2. **R-1, amended** (confirmation of K-119).
   - Add record times 50/60 µs.
   - Add the relative-error metric and the ≥ 3-informative-series requirement (M-5).
   - Add the rotor-averaged model on the 3 informative series (M-4).
3. **State-file edits.** Apply O4-1 to O4-9. The `SCIENTIFIC_MEMORY` lesson "a flat ladder in one cluster family is
   not convergence" should explicitly cover **derivatives and Fisher information**, not only F.
4. **Pro-quantum verifiers on K-117 and on the red team's re-based arms,** before either is recorded as closed rather
   than provisional.
5. **K-109 bookkeeping.**
   - Add the local-DQ-envelope arm (INFERENCE) as its t_cl-independent arm.
   - Record would-be-WEAK status if RT-DQ-methyl fails.
   - Run RT-DQ-methyl in two families, as the synthesis already says.
6. **Experimental (outside compute; unchanged).** Site-resolved PE and DQ T3/T2 in microcrystalline GB1 or ubiquitin.
   After CR4-B, this is also what separates "kill" from "category-1 near-miss" under LE.

---

## 6. Files

- `research/experiments/ROUND4/CRITIC.md`: this file.
- `research/experiments/ROUND4/critic/critic_arith.py` → `critic_arith.json`: A1–A5. Reads JSON only, < 1 CPU-s.
- `research/experiments/ROUND4/critic/fi_nscale.py`: partner-complete Fisher Jacobians. Reuses the red team's model
  read-only, checkpoints per column. Outputs: `critic/out/fi_{base10,baware12,probe12}_<pdb>_p<probe>.{npz,json}`
  (9 runs, 36 CPU-min).
- `research/experiments/ROUND4/critic/fi_analyze.py` → `fi_nscale_summary.json`: gains for every case, validations and
  per-parameter values.
- No quantum resources were used. Simulator runtime is not physical quantum runtime.
