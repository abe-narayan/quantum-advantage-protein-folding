# Resource-auditor verification of the ROUND4 lane `tx_early`

_2026-09-28. Adversarial verifier (resource). This covers the lane's claims about resources, break-even and
40 µs convergence. Category 3 (physics simulation) only. Tags: MEASURED (a file in this folder), DERIVED,
INFERENCE, UNPROVEN._

## Verdict: NOT REFUTED, with five corrections

- **Holds** [MEASURED]:
  - the resource ledger;
  - the rule outcome (KEEP OPEN);
  - every 40 µs number;
  - the back-test.
- **Break-even at 40 µs is credible, and it goes the classical way.**
  - F₁₈ costs about 25 CPU-s per probe (all 4 sites), and it predicts F₂₂ to rms 0.0015 (σ/7).
  - No quantum device has a cost to break even against on this observable.
- **Where the claim overreaches:**
  - "converged" to N → ∞;
  - "within σ/4 of the converged echo";
  - the cost of the missing cells;
  - calling KEEP OPEN a scientific outcome, when the pre-registered test was never executable under the cap.
- **One adversarial test strengthened the lane's inference.** At N ≤ 22, F does not track genuine H drift, not just
  the floor (§3).

## 1. Resource ledger (audit.py → audit.json) [MEASURED]

| item | lane claim | audit |
|---|---|---|
| CPU used | ≈ 80 CPU-min | 76.7 CPU-min summed from `cpu_s` in the run and checkpoint files, plus bench and validate self-time → ≈ 80. **Confirmed** |
| Peak RAM | 1.53 GB | 1.526 GB (N = 22 p19 echo). **Confirmed** |
| Cost per N = 22 folded vector-step | 4.1 s (bench) | Production rate including overhead: **5.05 s (p19) and 5.12 s (p245)**. For comparison, N = 20: 0.64–0.67 s |
| Missing 80/120 µs cells | "~2 CPU-h" | At production rates: **149 CPU-min ≈ 2.5 CPU-h**, made up of 59–60 per probe at N = 22 and 15–16 per probe at N = 20 (R = 2). At the bench rate: 126. **Understated by about 20–25%** |
| Echo vector-steps per phase n | 700 for 80 + 120 µs | (n − n_prev)(1 + B) + n(1 + B) with B = 4 gives 200 / 300 / 400 folded steps. **Confirmed** |
| "~17 CPU-min per probe per time at N = 22" | level_practical | True only for 40 µs (16.8–17.1). At 80 µs and 120 µs the phases cost about 1.5× and 2× that |
| Minimal complete T-X-early test | not stated | Full 3-phase N = 22 echo for both probes (75.8 + 76.8 min), plus CSD (2 × 4.3), with X₂₀ taken for free from reference checkpoints: **161 CPU-min, more than the 90 CPU-min cap** |

**Correction C-1.** The pre-registered T-X-early rule could not be completed by one agent under the 90 CPU-min
cap, however the budget was allocated.
- CRITIC A-1 estimated "about 30–45 CPU-min". That covers the N = 22 H and floor by inverse passes (16 CPU-min
  measured). It leaves out the F₂₂ echo, which X₂₂ requires.
- So the KEEP OPEN is the rule's else-branch, triggered by a mis-costed pre-registration. It is not a scientific
  outcome.
- It should be recorded as **NOT EXECUTABLE UNDER CAP (KEEP OPEN by default)**, and the cost (≈ 2.5 CPU-h) should
  be pre-registered before any rerun [DERIVED from MEASURED rates].

Minor ledger corrections:
- README §1 calls the N = 22 echo-mode H and the honly H "independent estimators". Both use the same random vector
  (seed 4242, the same `draws()`), so their 0.0004 agreement does not measure typicality noise.
- This does not matter in practice. The measured R = 1 sd(H) is 0.0005–0.0009 at N = 20, so the lane's
  se_H22 = 5e-4 is about right.

## 2. Independent recomputation [MEASURED]

- **From raw run files.** The 40 µs ΔX and budgets match `tx_early_summary.json` to 0.0, and 7/8 series pass.
  - max |F_N − F₂₂| is 0.0026 over N = 18–22 and 0.0056 over N = 16–22. **Confirmed.**
- **Back-test.** Hybrid rms is 0.0147 / 0.0135 / 0.0088, against the lane's 0.0145 / 0.0133 / 0.0086. Flat-F rms is
  0.0043 / 0.0030 / 0.0015. Flat-F wins 8/8 at every N_s. **Confirmed.**
  - The 0.0002 difference comes from using honly rather than echo-mode H₂₂.

## 3. Does F track genuine H drift, or only fail to track the floor? (noise.py, tracking.py) [MEASURED]

**Why this matters.** The lane's evidence was mostly floor-drift evidence. Its ladder regressors come from single
vectors: ROUND3 VC honly H at N = 14–20.
- In `audit.json`, a pooled regression of ΔF on (ΔH, Δfloor) over the N ≥ 14 steps gives coef_ΔH = 0.12 ± 0.085
  and coef_Δfloor = −0.08 ± 0.11. But the per-step ΔH (≤ 0.0076) is of the order of the typicality noise, so the
  ΔH coefficient is attenuation-prone.

**What was run.** The lane's own validated driver (`tx_echo.run`, imported unchanged, outputs redirected to
`verify_resource/runs/`) at 40 µs:
- 4 extra seeds in honly mode at N = 14–20;
- 3 extra seeds in echo mode at N = 16 and 18;
- both probes.

Cost: 484 CPU-s, peak 0.39 GB.

**Typicality noise, R = 1.**

| N | sd(H) | sd(floor) | sd(F) |
|---|---|---|---|
| 14 | 0.003–0.005 | ≤ 4e-4 | — |
| 16 | 0.001–0.003 | ≤ 5e-4 | ≤ 0.0014 |
| 18 | 0.0015–0.003 | ≤ 3e-4 | ≤ 0.0011 |
| 20 | ≤ 0.0009 | ≤ 1e-4 | — |

- The single-vector VC H₁₄ sits 0.0096 below the multi-seed mean on both probes, and VC H₁₆ sits 0.002–0.004 below.
- **Effect:** this does not touch flat-F, which uses no H. It makes the hybrid back-test worse, not better, because a
  higher H₁₄ means a lower X₁₄.

**The key test: p245, N = 16 → 22.**
- Genuine H drift **ΔH = −0.0106 ± 0.0010 (10 se)** and Δfloor = −0.0078.
- The hybrid picture predicts ΔF = −0.018.
- Observed ΔF on sites 1/7/8/9: **−0.0002 / +0.0006 / −0.0001 / −0.0022**.
- So F tracks less than about 20% of a genuine ≈ 1σ H drop caused by cluster ranks 17–22. This supports the lane's
  commutation inference beyond the floor.

**p19.** H is flat over N = 16→22 (−0.0002 ± 0.0016), so this probe gives no H-tracking test.

**Explicit F̂_∞, as H-2 requires.**
- Method: a weighted 1/N fit over N = 16–22 using the multi-seed F.
- F̂_∞ − F₂₂ lies in **[−0.005, +0.007] on 7/8 series**.
- p19 b8 gives +0.025, but there the 1/N model fails (χ² = 169 on 2 dof): F jumps +0.0066 from N = 16 to 18, when a
  spin enters, and is flat afterwards.
- χ² exceeds the degrees of freedom on 5/8 series. **No finite-size functional form is validated.**

## 4. The unproven step and H_∞ [MEASURED inputs; INFERENCE]

- **p19 far-spin drift.** CSD gives D = H₈₀ − H₂₂ = −0.029 ± 0.004 (N_c = 80, common random numbers). But the ROUND3
  CSD ladder without common random numbers is not monotone in N_c:

  | N_c | H (CSD) |
  |---|---|
  | 22 | 0.362 ± 0.007 |
  | 24 | 0.357 ± 0.010 |
  | 40 | 0.362 ± 0.010 |
  | 80 | 0.338 ± 0.010 |
  | 160 | 0.363 ± 0.017 |

  - So H_∞ has an N_c-convergence systematic of about 0.01–0.025 that is not in se_H, which is statistical only.
  - The pre-registration allowed N_c = 80–160; the lane used 80.
  - This hurts only the hybrid F̂_∞, and with it CRITIC-C1's gap. It does not hurt the flat-F reading.
- **If F tracked the p19 far-spin drift fully**, F_∞ − F₂₂ would be −2.9σ. With the measured tracking of ≤ 0.2 from §3,
  it would be ≤ 0.6σ. **Tracking beyond cluster rank 22 is UNPROVEN.**

**Correction C-2.** Replace "F_N is already converged … within about σ/4 of the converged echo" (level_practical) with:
- "F_N is step-converged to N = 22: F₁₈ predicts F₂₂ to σ/7 [MEASURED].
- F is insensitive to measured H and floor drift over N = 16→22: tracking ≤ 0.2 [MEASURED, p245].
- F_∞ within about σ of F₂₂ is INFERENCE. Explicit 1/N F̂_∞ gives ≤ 0.7σ on 7/8, the functional form is unvalidated,
  and no cross-family check has been done, as H-2 requires."

**Correction C-3.** "CRITIC-C1's gap at 40 µs is an estimator artefact" is:
- supported (MEASURED) for the floor part and for intermediate-shell H drift;
- INFERENCE for the ranks 23–80 part. That part is −2.9σ on p19 only if F tracks it fully, which is disfavoured.
  Keep the INFERENCE tag.

## 5. Break-even vs the best classical method at 40 µs [MEASURED cost; INFERENCE accuracy]

| classical route | cost (single thread) | accuracy |
|---|---|---|
| Exact sector typicality, N = 18, 40 µs, 4 sites | 25–27 CPU-s per probe (this audit's runs) | reproduces F₂₂ to rms 0.0015 |
| Exact sector typicality, N = 22, 40 µs, 4 sites | 16.8–17.1 CPU-min per probe | reference |
| Quantum device | nothing to beat at this N | — |

- The open part at 40 µs is the accuracy of any N ≤ 22 model against the physical N → ∞ echo, not cost.
- A quantum simulator would face the same problem: finite-size, forward-model and reversal errors, which are
  5–66σ per K-105.
- **Levels:**
  - theoretical: L0, no separation;
  - practical: L0 at 40 µs;
  - practical at 80–120 µs: open as a category-3 physics question, and uncosted on the quantum side.

## 6. Files and cost

- **Scripts:**
  - `audit.py`: ledger, costs, recomputation and back-test. File reads only.
  - `noise.py`: extra-seed runs through the lane driver. Checkpointed and resumable.
  - `tracking.py`: multi-seed ladder, tracking test and F̂_∞.
- **Results:**
  - `audit.json`, `noise.json`, `tracking.json`;
  - `runs/VR_*`: 44 small runs, with checkpoints kept.
- **Verifier compute:**
  - about 8.2 CPU-min in total (noise.py 484 CPU-s; the rest under 5 CPU-s);
  - peak 0.39 GB, single-threaded;
  - no files outside this folder were modified.
