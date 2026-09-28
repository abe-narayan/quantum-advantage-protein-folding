# ROUND4 lane: redteam_kills (pro-quantum red team on K-105, K-109, K-111 and the FeMoco WEAK residue)

_2026-09-28. Brief: find **false kills**. Attack the load-bearing arm of each kill one by one; SUPPORTS if any kill's load-bearing arm fails and nothing else carries it; KILLS if every kill stands, with its corrected load-bearing arm stated._

**Tags:** MEASURED (computed here; file named), DERIVED (algebra or closed form, checked), LITERATURE-SUPPORTED (arXiv abstract fetched this session through the API), INFERENCE, UNPROVEN, UNVERIFIED (recalled, not fetched).

**Scope.** Everything is in `research/experiments/ROUND4/redteam_kills/`. No file outside this folder was modified. No commit.

---

## 0. Verdict: KILLS. All four stand, but three of the recorded arms were wrong or incomplete

| Kill | Recorded load-bearing arm | Red-team result | Corrected load-bearing arm | Status |
|---|---|---|---|---|
| **K-105** (secular OTOC(1) echo as structure advantage) | Forward-model error of 5–66σ (methyl rotation, 1 kHz offsets, reversal mismatch), plus value (CRITIC C1) | **The forward-model-error arm fails as a kill.** With offsets, reversal scaling and global and per-rotor-group order parameters put into the model and profiled, the 7.6–45σ echo misfit disappears. 18–34% (no prior) to 58–83% (tight prior) of the echo's structural FI is retained. The profiled joint gain g is *not* reduced by profiling: with no prior it is often larger than with the nuisances known. [MEASURED] | **The reversal horizon of a site-resolved echo.** Under the local polarization-echo envelope (T3 = 4 T2, Sánchez 2022), the profiled median g is **1.09–1.60** (moderate priors; ≤ 2.10 with none). This holds **even at t_cl = 0**, i.e. if the entire converged echo were beyond classical reach, so the arm no longer depends on N = 10 twins. Out-of-family model error (per-pair order parameters) lowers the accuracy gain further, to 1.06–1.52 [MEASURED]. The literature does not support T3/T2 ≥ 15 for XXZ echoes (§4) | **Stands** |
| **K-109** (DQ echo) | ε = 3e-5 N = 10 twin reproduces to 140–220 µs; median g ≤ 1.16 inside the envelopes (≤ 1.42 ideal) | **The recorded arm is an N = 10 artefact.** Inside the literature DQ envelope (12.5 T2), the profiled g_med is **2.2–4.3 at t_cl = 40 µs** and 2.3–7.6 at t_cl = 0, and stays ≥ 2 up to t_cl = 50–60 µs (none/moderate/tight priors, 3/3 probes) [MEASURED]. So K-109 hinged on an unmeasured converged-size classical reach | **Value against the measured converged reach.** The new DQ size ladder (N = 10→18, 1UBQ p19) shows the non-methyl butterfly sites step-converged (≤ 0.0017 per ΔN = 2) to 80 µs. The DQ echo has no conserved-charge floor [DERIVED], so this step test is less biased than the secular one. With classical reach 80 µs at non-methyl sites and secular transfer on the classical side, g_med = **1.27 / 1.32 / 1.78–1.97** (12.5 T2, moderate) and **1.53 / 1.62 / 2.09–2.50** (19 T2) [MEASURED]. One near-miss: 1PGA p390 reaches g_med 2.1–2.5, but only at the upper 19 T2 anchor and only if its *methyl*-proton butterfly echo is classically unreachable beyond 40–50 µs. That is unmeasured, and the static-methyl model behind it is unphysical. g ≥ 10 is reached nowhere under a literature envelope | **Stands (narrow)**. One probe is conditional; the corrected reopen condition is in §8 |
| **K-111** (coupled methyl rotors) | CRITIC C2: the many-body correction is degenerate with the per-methyl V3 (identifiability) | **The degeneracy argument is incomplete** [DERIVED]. The partner-state dependence J (a doublet split by J) is *not* degenerate with V3_1, so the coupling is identifiable in principle | **Resolvability plus classical exactness.** Against glass disorder σ_V3 ≥ 1 meV, the doublet is resolved and observable for **0/32** pair cases at V3 = 60–100 meV and for **2/32** (one pair, both coupling models) at V3 = 30 meV [MEASURED from lane data]. The identifiable quantity J is an exact 2-rotor computation (seconds, classical) | **Stands** |
| **FeMoco E-state residue** (WEAK, not killed) | Model floor co-limits the solver; 10–1640 QPU-days per question; classical anchor is one preprint | **The preprint is not load-bearing.** arXiv:2601.04621 covers the *resting* state; the E4 σ_best is unanchored either way, and the favourable scenario already assumes 5 kcal/mol | **σ_m (model floor for charge-moving E4 isomers) and cost.** In the lane's own closed form, a best-case value of information ≥ 0.3 Å on a 1 Å lever needs **σ_m ≤ 1.2 kcal/mol** (σ_best = 5), or σ_m ≤ 0.7 at σ_best = 3 [DERIVED]. The lane inferred σ_m ≈ 1–4. Cost ≥ **10.8 QPU-days** at 76 orbitals and 30 energies, and 20.5 at 100 orbitals [DERIVED] | **Stays WEAK** (no false kill) |

**Bottom line [INFERENCE from the above].**
- No kill flips to an advantage.
- The program's negative stands for the NMR echo routes. The reasons are corrected, though:
  1. **Model nuisances are not the binding constraint.** Forward-model error from offsets, rotors and reversal scaling is fixable by profiling at a factor ≤ 2–5 in FI, and it leaves the gain intact.
  2. **The binding constraints are two.**
     - (a) The reversal horizon of a *site-resolved* echo relative to where the information lies.
     - (b) How far classical simulation reaches at converged size. For DQ at non-methyl sites this is now step-measured to 80 µs.
  3. **Out-of-family dynamics set an accuracy floor.** Per-pair motional scaling leaves structural biases of about 0.1–11× the quantum CRB (moderate priors), which caps the accuracy gain at ≈ 1–2.4. An MD-ensemble forward model would be needed.

---

## 1. RT-A: profiled joint gain (K-105 secular, K-109 DQ): `profiled_gain.py`, `analyze_profiled.py`

**Forward model.** Same N = 10 clusters, butterflies, structural parameters, dt = 2 µs Trotter circuit and σ = 0.01 as R1_amplify / dq_echo_envelope (`amp_lib.job_geometry`, orientation 0). It is extended to be nuisance-complete:

| Component | Treatment |
|---|---|
| Couplings | **Rotor-averaged** (fast 3-site jumps of every CH3/NH3 group touching the cluster, jump sites from the full protein; `scales.averaged_couplings`). This is the physically correct fast-limit model, not the static one the RAW data used |
| Global order parameter | ε0 scales all couplings |
| Per-rotor-group order parameter | ε_g for each group |
| Offsets | Ω_i Z_i/2 per site, base 1 kHz RMS; same seed as R1_physics_feasibility |
| Reversal scaling mismatch | η, with the echo computed explicitly: G = Tr[Z_b W Z_a U Z_b U† Z_a W†]/2^N, W = (S_η^n)† |
| DQ | Physical H_DQ (s = 1), offsets fully present (κ = 1, pessimistic). An "offsets_known" prior variant is the optimistic proxy |
| Methyl-proton structural parameters | Re-expressed as whole-group (rotor-axis) displacements (`*_axis`), fixing R1 flaw 2 |

**Validation [MEASURED].**
- The static, offset-free engine reproduces `amp_lib.exact_sector` and `exact_parity` exactly (max difference 0.0) on all 7 jobs.
- The explicit mismatched-echo path at η → 0 equals the fast path to ≤ 5.6e-13.
- Base-model versus static offset-free misfit: echo 7.6–45σ, transfer 1.4–9.7σ. This is the "5–66σ" arm, reproduced.
- Cross-check against R1_physics_feasibility for 1UBQ p19 (Ω + η nuisances, hard window ≥ 80 µs): retained structural FI is 0.23 / 0.62 / 0.89 here, against their 0.21 / 0.46 / 0.83, for none / moderate / tight priors.

**Gain definition.**
- g = CRB_cl² / CRB_q², the marginal CRB per structural parameter with all nuisances and the other structural parameters profiled.
- Classical route: transfer S at all times, plus echo for t < t_cl.
- Quantum route: transfer plus echo at all times.
- Echo rows are multiplied by the reversal envelope A(t), using physical T2 = rotor-averaged network T2 (9.8 µs for 1UBQ, 10.7 µs for 1PGA) and forward time only (the generous argument).
- **t_cl, the converged-size classical reach, is scanned from 0 to 240 µs.** It is unknown, and CRITIC C1 marks it unresolved at ≤ T3.

**Priors.**

| Prior | Offsets | η | ε0 | ε_g |
|---|---|---|---|---|
| none | — | — | — | — |
| moderate | 0.2 ppm | 2% | 3% | 10% |
| tight | 0.05 ppm | 0.5% | 1% | 3% |
| known | nuisances fixed (the old accounting) | | | |

### 1.1 Secular echo (K-105): median profiled g, physical T2

Each cell gives moderate [none].

| Probe | PE 4T2, t_cl = 0 | PE 4T2, t_cl = 40 | LE 6.7T2, t_cl = 0 | LE 6.7T2, t_cl = 40 | LE, t_cl = 80 | Ideal, t_cl = 80 | Hypothetical 15T2, t_cl = 80 |
|---|---|---|---|---|---|---|---|
| 1UBQ p19 | 1.09 [1.13] | 1.07 [1.08] | 1.39 [1.63] | 1.36 [1.55] | 1.02 [1.10] | 3.66 [6.72] | 2.01 [3.03] |
| 1UBQ p245 | 1.11 [1.13] | 1.06 [1.10] | 1.48 [1.92] | 1.36 [1.88] | 1.06 [1.11] | 6.87 [4.86] | 3.33 [3.05] |
| 1PGA p325 | 1.17 [1.57] | 1.11 [1.28] | 1.64 [2.36] | 1.52 [1.90] | 1.04 [1.04] | 2.47 [2.81] | 1.54 [1.65] |
| 1PGA p390 | 1.60 [2.10] | 1.33 [1.42] | 2.93 [4.09] | 2.23 [2.38] | 1.12 [1.12] | 2.60 [3.54] | 1.73 [1.58] |

**Reading.**
- **Under the site-resolved polarization-echo envelope, no probe reaches g_med ≥ 2 with any prior, even at t_cl = 0.** The single exception is 1PGA p390 with no prior at 2.10.
- The global Loschmidt-echo envelope (6.7 T2) gives ≥ 2 on 2/4 probes only if t_cl ≤ 20–40 µs.
- g_med ≥ 2 at t_cl = 80 µs needs T3/T2 ≈ 15, which matches the old "required ≈ 15" [MEASURED].
- **Profiling does not erode the gain.** For example, 1UBQ p19 ideal at t_cl = 0 gives none 14.4, known 11.7 and moderate 6.9, because the nuisances hurt the classical route at least as much [MEASURED].
- With ideal reversal, the gain at t_cl = 80 µs is 2.5–6.9 (moderate). The K-105 phrase "value ≤ 1.2–3 even with ideal reversal" understates this. K-105 stands on reversal, not on ideal-reversal value [MEASURED].

### 1.2 DQ echo (K-109): median profiled g, physical T2

**DQ transfer only on the classical side (the lane's convention).** Each cell gives moderate [none].

| Probe | DQ LE 12.5T2, t_cl = 0 | t_cl = 40 | t_cl = 80 | DQ LE 19T2, t_cl = 0 | t_cl = 80 | Largest t_cl with g_med ≥ 2 (12.5T2) |
|---|---|---|---|---|---|---|
| 1UBQ p19 | 2.35 [3.77] | 2.26 [3.58] | 1.28 [1.86] | 2.89 [5.15] | 1.76 [2.42] | 50 [60] µs |
| 1UBQ p245 | 2.58 [4.86] | 2.19 [2.42] | 1.53 [1.39] | 4.02 [8.39] | 2.26 [1.98] | 50 [60] µs |
| 1PGA p390 | 4.03 [7.60] | 3.40 [4.11] | 1.42 [1.98] | 5.10 [12.77] | 1.73 [3.20] | 60 [60] µs |

**RT-A2: secular transfer also on the classical side** (joint profiling over shared nuisances). Each cell gives g_med at t_cl = 0 / 40 / 60 / 80 µs, moderate [none].

| Probe | DQ LE 12.5T2 | DQ LE 19T2 |
|---|---|---|
| 1UBQ p19 | 1.90 / 1.82 / 1.47 / 1.21 [2.58 / 2.55 / 2.13 / 1.56] | 2.45 / 2.30 / 1.84 / 1.50 [3.38 / 3.29 / 2.61 / 1.88] |
| 1UBQ p245 | 1.80 / 1.70 / 1.62 / 1.32 [2.09 / 2.07 / 1.80 / 1.55] | 2.45 / 2.32 / 2.07 / 1.62 [3.06 / 2.97 / 2.40 / 1.79] |
| 1PGA p390 | 2.70 / 2.42 / 1.75 / 1.32 [3.84 / 3.09 / 1.99 / 1.51] | 3.22 / 2.88 / 2.05 / 1.53 [5.07 / 4.06 / 2.57 / 1.94] |

The local DQ envelope (7.5 T2, INFERENCE) gives < 2 almost everywhere [MEASURED].

**Reading.**
- The recorded K-109 numbers (g ≤ 1.16; "none even at T3/T2 = 1000") are an artefact of calling the N = 10 ε = 3e-5 twin "classical reach" at 140–220 µs. At N = 10, everything is classically reachable.
- The value arm therefore turns on t_cl^DQ, the classical reach at converged size, which was unmeasured. §3 measures it in the step sense.

### 1.3 RT-A3: out-of-family forward-model error

Script: `analyze_profiled.py`, extension functions. The truth has per-pair order parameters S_ij ~ U[0.85, 1] (INFERENCE range, as in R1_value_breakeven), which lies outside the nuisance family. Two draws per probe.

| Quantity | Result [MEASURED] |
|---|---|
| Misfit, max, before fit | 1–12σ |
| Misfit, max, after the profiled fit | 0.2–3σ (χ² reduced about 9–70×) |
| Structural bias, moderate priors | 0.1–11× CRB_q |
| Structural bias, nuisances "known" | up to 15–31× CRB_q |

**Bias-inclusive accuracy gain** g_acc = (CRB_cl² + b_cl²)/(CRB_q² + b_q²), moderate priors:

| Case | t_cl = 0 | t_cl = 40 | t_cl = 80 |
|---|---|---|---|
| Secular, PE envelope | 1.06–1.52 | — | — |
| Secular, LE envelope | 1.18–2.15 | 1.24–1.71 | — |
| DQ, 12.5T2 | 1.56–2.37 | 1.24–2.30 | 0.83–1.36 |

**Reading.** Nuisance *families* profile cheaply. Per-pair motional scaling does not, and needs an ensemble (MD) forward model (a cost multiplier). Because b does not depend on σ, this floor matters less at a realistic σ > 0.01 [DERIVED].

---

## 2. What the corrected K-105 arm rests on [INFERENCE unless tagged]

- **The envelope that applies to a site-resolved OTOC(1) is the local polarization echo.** A site-resolved OTOC needs local preparation, a local butterfly and local readout. The measured local polarization echo is Gaussian with T3 ≈ 4 T2 [LITERATURE-SUPPORTED: Sánchez et al. 2022, full text read by R1_physics_feasibility; abstract re-verified here, T3 = T2/R with R = 0.15 ± 0.01 for the global echo].
- **Under that envelope the kill needs no statement about converged classical reach** (t_cl = 0 row in §1.1). This removes the "N = 10-conditioned" weakness CRITIC C1 raised for the reversal arm.
- **What would reopen K-105.**
  - A measured protein site-resolved T3/T2 ≥ 15, *together with* t_cl ≤ 80 µs. That gives g_med ≈ 2–3.3.
  - For g ≥ 10 (the R1 revival bar), T3/T2 ≳ 20–50 *and* t_cl ≲ 40 µs are needed (hypothetical 20/50 T2 rows). Only 1UBQ p245 and 1PGA p390 reach ~10 there.

---

## 3. RT-B: exact classical reach of the physical DQ echo (`dq_reach.py`, `sitewise_tcl.py`)

**Method.**
- Typicality estimator of the DQ F_ab(t) on the SAME physical-DQ Trotter circuit as `amp_lib.exact_parity(dq_pair_terms(s = 1))`.
- Forward legs are reused across record times.
- Checkpointed after every record time, atomic and resumable.

**Validation [MEASURED].**
- The full step unitary built from this kernel equals `build_step_unitary_generic` exactly at N = 6 (difference 0.0); the inverse is exact to 7e-16.
- The N = 10 mean over 8 vectors matches the exact parity-block F within 1.8 standard errors.

**Why a step test is more meaningful for DQ [DERIVED].**
- H_DQ conserves only parity ∏Z_i (and energy). Z_a has zero overlap with both.
- So the DQ echo has **no O(1/N) conserved-charge floor**. The secular echo has one, (1 − H)/N (CRITIC C1), which is what made secular step statistics misleading (C10).
- It is still a step statistic, not F̂_∞.

**Ladder, 1UBQ p19 (static couplings, as dq_echo_envelope).**
- M = 16 / 6 / 3 / 1 vectors at N = 12 / 14 / 16 / 18.
- N = 10 is exact.
- Typicality error ≤ 0.004.

Maximum over sites of |F_N − F_{N−2}| [MEASURED]:

| Step | 40 µs | 50 µs | 60 µs | 80 µs | What drives it |
|---|---|---|---|---|---|
| 10→12 | 0.0025 | 0.0027 | 0.0035 | 0.0124 | — |
| 12→14 | 0.083 | 0.135 | 0.195 | 0.288 | **Shell event:** HB2/GLN2 enters (geminal partner of butterfly HA/GLN2) |
| 14→16 | 0.0029 | 0.0062 | 0.0117 | 0.0212 | — |
| 16→18 | 0.0038 | 0.0113 | 0.0258 | 0.0785 | **Shell event, entirely at the methyl butterfly HG22/ILE3** when its methyl partner HG21/ILE3 enters |
| 16→18, non-methyl sites 1 / 7 / 9 | ≤ 0.0009 | ≤ 0.0015 | ≤ 0.0017 | ≤ 0.0009 | — |

**Reading.**
- Non-methyl butterfly echoes are step-converged at N = 18 through 80 µs, once their strongly coupled partners are inside the cluster [MEASURED, one probe].
- The only unconverged site is a *static* methyl proton. Its physical echo needs the rotor-averaged model [INFERENCE].
- **Site-dependent reach** (`sitewise_tcl.py`): non-methyl classical to 80 µs, methyl sites 0–50 µs, secular transfer included. Each cell gives moderate [none]:

| Probe | 12.5 T2 | 19 T2 |
|---|---|---|
| 1UBQ p19 | 1.27 [1.62] | 1.53 [1.96] |
| 1UBQ p245 (no methyl butterfly) | 1.32 [1.55] | 1.62 [1.79] |
| 1PGA p390 (methyl butterfly HG21/THR53) | 1.78–1.97 [1.83–2.02] | 2.09–2.50 [2.38–2.67] |

[MEASURED]

---

## 4. Literature: does anything support a protein T3/T2 ≥ 15?

**Answer: no, for XXZ/secular echoes. For DQ, only in adamantane, and only at the top of the T2-convention range.**

**Verified this session (arXiv API abstracts) [LITERATURE-SUPPORTED]:**
- **Sánchez, Chattah & Pastawski**, PRA 105, 052232 (2022), arXiv:2112.00607. T3 ≈ T2/R, R = 0.15 ± 0.01, perturbation-independent. The best XXZ echo is therefore 6.7 T2.
- **Rufeil-Fiori et al.**, PRA 79, 032324 (2009), arXiv:0810.1722. Adamantane shows an "abrupt Fermi-type decay" of the DQ Loschmidt echo. The dq_echo_envelope lane derived 12.5 T2 from its full text, and 12.5–19 T2 across adamantane T2 conventions.
- **Domínguez, Rodríguez, Kaiser, Suter & Álvarez**, PRA 104, 012402 (2021), arXiv:2005.12361. The decay rate goes as K^α. Below a critical perturbation strength α < 1, and "there is no inherent limit to the number of qubits that can be controlled". p_c = 0.026 comes from the lane's full-text read.
- **Fine, Elsayed, Kropf & de Wijn**, PRE 89, 012923 (2014), arXiv:1305.2817. Spin-1/2 lattices show only *power-law*, not exponential, sensitivity of the Loschmidt echo to small perturbations: "encouraging news for … quantum simulators". This is theory and numerics; it gives no horizon value.
- Also seen, not protein:
  - Geier et al., PRR 6, 033197 (2024), arXiv:2402.13873 (Rydberg time reversal);
  - Gao et al., arXiv:2503.14598 (NV ensemble, asymmetric reversal);
  - Usaj / Levstein polarization echoes (cond-mat/0002332, cond-mat/9708172).

**Not found on arXiv (API author and title searches returned 0), so UNVERIFIED and not used in any number:** Krojanski & Suter, PRL 93, 090501 (2004); PRA 74, 062319 (2006); PRL 97, 150503 (2006).

**Protein or biological-solid echoes.** Two API queries (magic / polarization echo, and Loschmidt + dipolar + time reversal) returned **0 protein entries**.

**Reading [INFERENCE].**
- Fine 2014 and Domínguez 2021 undercut the *universality* of T3 ≈ 4–6.7 T2. A horizon can grow as the perturbation shrinks.
- But a protein's intrinsic perturbation ratio is p ≈ 0.05 (dense sites) to 0.3 (amide H). The inputs are:
  - 1 kHz offsets;
  - 3–6 kHz ¹⁴N local fields at amide protons (`R1_physics_feasibility/scales.json`);
  - against a homonuclear √M2/2π of 18–20 kHz.
- That is 2–10× above p_c, in the strong-perturbation regime (α ≈ 1). Proteins are therefore expected to be *less* reversible than adamantane, a plastic crystal whose intramolecular couplings are motionally averaged.
- No anchor supports ≥ 15 T2 for a site-resolved echo in a protein.

---

## 5. RT-C: K-111 methyl rotors (`rotor_identifiability.py` → `rotor_identifiability.json`)

**The CRITIC C2 degeneracy is incomplete [DERIVED].**
- The partner-in-A shift of Δ₁ is degenerate with V3₁.
- The partner-state dependence J = Δ₁(partner E) − Δ₁(partner A) is not: a V3₁ change moves both doublet components together.

**Test.** Inputs are the lane's exact pair data (16 closest 1UBQ methyl pairs × 2 coupling models), with slope |d ln Δ/dV3| = 0.124 / 0.094 / 0.075 per meV at 30 / 60 / 100 meV.
- Inhomogeneous FWHM = 2.355 · Δ · slope · σ_V3.
- J/Δ needed for resolution: 0.09–0.15 at σ_V3 = 0.5 meV, 0.18–0.29 at 1 meV, 0.88–1.46 at 5 meV.
- Measured J/Δ (median / 90th percentile): 2e-3 / 0.21 at 30 meV, 7e-5 / 0.18 at 60 meV, 2e-6 / 0.009 at 100 meV [MEASURED from lane data].

**Observable and resolved doublets:**

| Observation window | Result |
|---|---|
| INS (Δ ≥ 0.1 µeV) | 0/32 at every V3 and every σ_V3 ≥ 0.5 meV |
| NMR tunnelling window (1e-4–0.4 µeV; range recalled, UNVERIFIED) | 2/32 (LEU56:CD2–ILE61:CD1, both coupling models) at V3 = 30 meV for σ_V3 ≤ 2 meV; 1/32 at 60 meV only for σ_V3 = 0.5 meV; 0 at 100 meV |

**Corrected arm.**
- The identifiable many-body content is a pair quantity computed exactly and classically in seconds. Exact 3-rotor calculations take 83 s.
- It is resolvable only at atypically low barriers.
- Caveats from the lane apply: unrelaxed H positions; the sector projection drops a symmetry-breaking part of about 6% of the coupling amplitude (sym_leak 1.35 meV vs 23 meV).

---

## 6. RT-D: FeMoco E-state WEAK residue (`femoco_sensitivity.py` → `femoco_sensitivity.json`)

**Closed form.** The lane's closed form is reproduced exactly (0.7 / 2.7 / 8.3 / 18.5 / 32.6%).

**σ_m needed for a best-case exact-solver value of information ≥ 0.3 Å:**

| Lever | σ_best = 3 | σ_best = 5 | σ_best = 8 |
|---|---|---|---|
| 0.8 Å | 0.39 | 0.65 | 1.05 |
| 1.0 Å | 0.73 | 1.21 | 1.94 |
| 1.5 Å | 1.37 | 2.28 | 3.65 kcal/mol |

A value of information ≥ 0.5 Å is impossible at a 0.8–1 Å lever [DERIVED].

**QPU-days per question** (Toffoli count ∝ N^2.35, anchored at 8.6 h for 76 orbitals):

| Orbitals | 30 energies | 300 energies |
|---|---|---|
| 76 | 10.8 | 108 |
| 100 | 20.5 | 205 |
| 150 | 53 | 531 |

[DERIVED]

**Reading.** WEAK is the right label. It is decided by one unmeasured number, σ_m for charge-moving E4 isomers, which needs a QM-region/embedding ladder on external HPC. The single resting-state preprint does not decide it. E4-specific classical literature was not found on arXiv (2 API queries: 0 and 3 unrelated entries). The QM/MM E4 literature is recalled only and UNVERIFIED.

---

## 7. Claim levels and categories

- **Theoretical: L0–L1 for all four.**
  - No separation.
  - The DQ and secular echoes at N ≤ 18 are exact-simulable.
  - The rotor J is exact-classical.
- **Practical: L0 for all four.**
- **Categories.**
  - No claim of categories 2–6 is supported.
  - The best residue is a **conditional category-1 (quantum usefulness) question** on one probe (1PGA p390, DQ, 19 T2, methyl butterfly). Even then, g_med ≈ 2.1–2.5 on local 3–8 Å distances, far below the R1 revival bar g ≥ 10.

## 8. Corrected revival templates (for KILLBOOK)

- **K-105.**
  - Reopen only if a protein **site-resolved** echo has a measured T3/T2 ≥ 15, *and* the converged classical reach t_cl ≤ 80 µs. That gives g_med ≈ 2–3.
  - g ≥ 10 needs T3/T2 ≳ 20–50 *and* t_cl ≲ 40 µs.
  - "Forward-model error 5–66σ" should be removed as a load-bearing arm. It is profilable.
- **K-109.**
  - The reopen condition "T3_DQ/T2 ≥ 50" is an N = 10 artefact. Replace it with all three of:
    1. a site-resolved protein T3_DQ/T2 ≥ 19;
    2. a converged classical reach ≤ 50 µs at the butterfly sites that carry the FI, measured with a partner-complete, rotor-averaged cluster ladder;
    3. profiled g_med ≥ 2 with secular transfer on the classical side.
  - On current evidence, (2) fails for non-methyl sites (step-converged to 80 µs) and is open only for methyl butterflies.
- **K-111.**
  - Reopen only if a real protein has ≥ 3 coupled methyls with V3 ≤ 50 meV, *and* the partner-state doublet satisfies |J| ≥ 2.355 · Δ · |d ln Δ/dV3| · σ_V3 with measured σ_V3, *and* the needed cluster exceeds exact 3–4-rotor reach.
- **FeMoco-E4.** Survives only with a measured σ_m ≤ 1.2 kcal/mol (σ_best = 5, 1 Å lever) *and* ≤ 30 energies at ≤ 100 orbitals.

## 9. Next tests (ranked)

1. **RT-DQ-methyl** (cheap; about 20 CPU-min with `dq_reach.py` plus a rotor-averaged option).
   - Rotor-averaged, partner-complete DQ ladder at the methyl butterflies 1PGA p390 HG21/THR53 and 1UBQ p19 HG22/ILE3, N ≤ 18, t ≤ 60 µs.
   - **KILL the p390 residue** if |F_N − F_{N−2}| ≤ 0.003 for t ≤ 50 µs at N ≥ 16.
2. **Ensemble forward model.** Per-pair S_ij from ≥ 50 MD snapshots in place of U[0.85, 1], to fix the size of the RT-A3 bias floor.
3. **Experimental (outside compute).** Site-resolved polarization-echo and DQ-echo T3/T2 in microcrystalline GB1 or ubiquitin. This decides K-105 and K-109 directly.
4. **FeMoco E4 σ_m ladder** (external HPC).

## 10. Files, compute, leakage

| File | Content |
|---|---|
| `profiled_gain.py` | Nuisance-complete forward model and Jacobians (checkpoint per column) → `out/pg_{sec,dq}_k1_<pdb>_p<probe>.{npz,json}` |
| `analyze_profiled.py` | RT-A gains, cross-checks, misspecification; `extensions()` (run with RT_EXT=1 or import) → `profiled_summary.json`, `profiled_extensions.json` |
| `dq_reach.py` | Typicality DQ echo ladder (checkpoint per record time) → `dq_reach.json`, `out/dqreach_*.npz` |
| `sitewise_tcl.py` | Site-dependent classical-reach gains → `sitewise_tcl.json` |
| `rotor_identifiability.py` | K-111 doublet resolvability → `rotor_identifiability.json` |
| `femoco_sensitivity.py` | FeMoco thresholds and cost → `femoco_sensitivity.json` |

**Compute.**
- Single-threaded (OMP/MKL/OPENBLAS = 1) throughout.
- Jacobians: about 27 CPU-min (4 secular × 1 min, 3 DQ × 7.5 min).
- DQ ladder: about 28 CPU-min. N = 18 was split over 3 checkpointed invocations. About 3 min were lost to a Windows file-lock on `os.replace` (fixed: open NpzFile handle, plus retry).
- Analyses: < 2 CPU-min.
- **Total about 57 CPU-min.** Peak RAM < 0.3 GB.
- One N = 16/18 invocation was moved to background by the harness after the 600 s tool limit. It was bounded by `timeout 500`, ran to completion, and was not detached by me.

**Leakage and ORACLE.**
- All Fisher and CRB quantities are evaluated at the PDB geometry, as in every earlier NMR lane. That is scientific analysis of information content: ORACLE-geometry, no selection, no training.
- No test-set selection.
- Simulator runtime is not quantum runtime. No quantum resources were run.
