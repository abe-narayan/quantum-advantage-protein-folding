# Adversarial verifier (relevance / novelty): ROUND4 lane `tx_early`

_2026-09-28. Scope: protein-structure value, novelty against the literature, and whether the finding reduces to a
KILLBOOK entry. Default: refuted if it reduces to a kill or is irrelevant. I also ran one cheap check on the finding's
only substantive new claim, because relevance depends on whether that claim holds._

Tags: **MEASURED** (file in this folder), **DERIVED**, **LITERATURE-SUPPORTED** (abstract verified this session),
**INFERENCE**, **UNPROVEN**.

## Verdict: REFUTED (relevance), and the new 40 µs claim fails a cross-family check

The finding has five parts. Four of them add nothing relevant. The fifth, the new one, does not hold.

1. **The rule outcome.** "T-X-early did not fire, so KEEP OPEN" is correct but carries no information. The 80 and
   120 µs cells were never run.
2. **The 40 µs claim.** The finding says the exact finite-cluster echo F_N at 40 µs is "already converged" (≤ 0.0026
   over N = 18→22 on all 8 series) and that exact simulation of 18–22 spins reaches the converged echo "within about
   σ/4". This does not hold. **[MEASURED, §2]**
   - All of the lane's ladders are probe-centred. At N = 22 they leave out the dominant dipolar partner of several
     instrument sites b.
   - Adding that single spin moves F by **+0.0697 (7.0 σ) on p245 b7**. That is one of the three informative series,
     and the lane claimed it moved by ≤ 0.0018 from N = 18 to 22. The spin is HG3/LYS27, rank 48 from the probe; it
     carries 49% of b7's second moment.
   - It moves F by **+0.0248 (2.5 σ) on p19 b8** (HG23/ILE3, rank 24, 82% of M2) and by −0.0086 (0.9 σ) on p19 b9
     (HG2/GLU16, rank 26).
   - Every other site stays within 0.001. Typicality noise is about 0.001.
   - So the flat ladders over N = 16–22 show that the probe-centred family converges slowly. They do not show that F
     has converged. This is exactly the failure that PREREG Round 4 H-2 anticipated, when it required a cross-family
     check before any convergence claim. The lane did not run one.
3. **"CRITIC-C1's 3–8 σ gap at 40 µs is an artefact."** Only half of this survives.
   - What survives [MEASURED, reproduced]: the T-X hybrid H_∞ + X_N is biased at early times, and the floor does not
     act as an additive bias on F.
   - What fails: the conclusion that N ≤ 22 finite clusters are σ-accurate at 40 µs. CRITIC-C1's reading 1 ("finite
     clusters are not σ-accurate forward models") and its status UNRESOLVED both stand, though for a different
     reason: local partners of b are missing from the cluster, not the conserved-charge floor.
   - The lane's own JSON contains 1/N fits over N = 16–22 with F̂_∞ − F₂₂ = +1.57 σ (p19 b8) and +1.08 σ (p245 b7).
     The README never reports them, and they already contradict "within σ/4" (§1).
4. **"X is not an independently converging quantity."** Given the decomposition, this is close to an identity.
   - X is defined as F − H − floor, and the floor falls deterministically, roughly as (1 − H)/N. So whenever F is flat,
     X must rise by exactly as much as H + floor falls.
   - The back-test ("flat-F beats X-converged, 8/8") restates the same fact within one cluster family. It reproduces
     numerically, but it is not independent evidence.
   - The physics is known: under a conservation law, the weight on conserved densities (here H) spreads
     diffusively, separately from the OTOC front. LITERATURE-SUPPORTED, abstracts verified this session:
     - Khemani, Vishwanath and Huse, arXiv:1710.09835;
     - Rakovszky, Pollmann and von Keyserlingk, arXiv:1710.09827.
5. **80–120 µs "remains open".** This is the pre-existing R1-SIM-X / CRITIC-C1 residue, already recorded under K-116
   ("what did not disappear"). The lane adds no new opening.

**Mission relevance: none.**
- The lane itself says it is category-3 physics only.
- CRITIC §2.4 item 8 already places R1-SIM-X outside the mission, in a spin-off register.
- One of the sensitive sites, p19 b8, is a methyl proton whose dominant partner is in the same methyl. Fast methyl
  rotation averages that coupling in a real protein. That is K-105's load-bearing forward-model-error arm (5–66 σ).
- The fix for the 40 µs problem is a b-aware classical cluster, not a quantum simulator. So K-116's framing, "the
  comparator must be σ-level classical", stands [INFERENCE].
- Nothing here bears on any claim category 1–6.

Levels: theoretical **L0**, practical **L0**.

## 1. Re-read of the lane's own numbers (`verify_rel.py` → `verify_rel.json`; < 1 CPU-s)

| series (40 µs) | 1 − F₂₂ | class | (F̂_∞(1/N, N = 16–22) − F₂₂)/σ | F₁₂ − F₂₂ (σ) |
|---|---|---|---|---|
| p19 b1 | 0.397 | informative | +0.82 | −10.1 |
| p19 b7 | 0.127 | informative | +0.22 | +0.6 |
| p19 b8 | 0.047 | near-trivial | **+1.57** | −0.8 |
| p19 b9 | 0.047 | near-trivial | −0.22 | −0.2 |
| p245 b1 | 0.021 | near-trivial | +0.02 | +0.7 |
| p245 b7 | 0.299 | informative | **+1.08** | −4.4 |
| p245 b8 | 0.045 | near-trivial | −0.02 | −0.2 |
| p245 b9 | 0.027 | near-trivial | −0.74 | +0.2 |

- Five of the 8 series have F ≥ 0.95: the operator front has barely reached b. "8/8 converged" is therefore mostly a
  statement about sites where F ≈ 1 [MEASURED].
- N ≤ 12 clusters are far from converged at 40 µs (p19 b1: 10 σ; p245 b7: 4.4 σ). This is consistent with CRITIC's
  "N = 10-conditioned" downgrade of the twin arms of K-105 and K-109.

**Local-field coverage.** This is the fraction of the full-protein M2_b = Σ_j d_bj² (629 protons, same b0) inside
the probe-centred N = 22 cluster [MEASURED]:

| site | p19 | p245 |
|---|---|---|
| b1 | 0.95 | 0.64 |
| b7 | 0.82 | **0.28** |
| b8 | **0.16** | 0.67 |
| b9 | **0.23** | 0.90 |
| probe a | 0.92 | 0.88 |

The dominant missing partners are:

| probe | site | partner | rank from probe | share of M2_b | distance to b |
|---|---|---|---|---|---|
| p19 | b8 | HG23/ILE3 | 24 | 82% | 1.77 Å |
| p19 | b9 | HG2/GLU16 | 26 | 64% | 2.31 Å |
| p245 | b7 | HG3/LYS27 | 48 | 49% | 2.38 Å |

## 2. Cross-family check at 40 µs (`run_baware.py`, `crossfamily.py` → `crossfamily.json`) [MEASURED]

**Setup.**
- Driver: the lane's validated `tx_echo.run`, with the same circuit, estimator, seed (4242), complex64 and R = 1.
- Only the cluster changes. The instance loader is patched, and outputs are redirected into this folder.
- Sanity check: my probe-centred N = 20 (R = 1) matches the lane's N = 20 (R = 2) to ≤ 0.0007 on all 8 series.

| test (vs probe-centred N = 20, F_ref) | b1 | b7 | b8 | b9 |
|---|---|---|---|---|
| p19: pure addition of rank 24 (HG23/ILE3) → N = 21 | +0.0010 | +0.0005 | **+0.0248 (2.5 σ)** | −0.0001 |
| p19: pure addition of rank 26 (HG2/GLU16) → N = 21 | −0.0016 | +0.0003 | +0.0001 | −0.0086 (0.9 σ) |
| p19: same N = 20 with CRN, ranks {18, 19} → {24, 26} | −0.0016 | +0.0002 | **+0.0249** | −0.0075 |
| p245: pure addition of rank 48 (HG3/LYS27) → N = 21 | −0.0002 | **+0.0697 (7.0 σ)** | +0.0001 | +0.0001 |
| p245: same N = 20 with CRN, ranks {18, 19} → {48, 31} | −0.0003 | **+0.0698** | +0.0016 | +0.0003 |

The lane's own figures for the same series, |F₂₂ − F₁₈|:

| series | p19 b8 | p19 b9 | p245 b7 |
|---|---|---|---|
| \|F₂₂ − F₁₈\| | 0.0001 | 0.0009 | 0.0018 |

**Reading.**
- The echo at a site b depends strongly on b's own strong partners. The probe-centred ladder adds those only at
  N = 25–49.
- The flat ladder therefore reflects the order in which the probe-centred family adds spins. It is not convergence.
- Where F_∞ actually lies at 40 µs is unresolved [UNPROVEN]:
  - at least 7 σ above F₂₂ on p245 b7;
  - at least 2.5 σ above on p19 b8.
- The shifts are positive, the opposite sign to CRITIC-C1's hybrid gap. So neither the lane's "F₂₂ ≈ F_∞" nor
  CRITIC's hybrid number is right for those series [INFERENCE].
- A b-aware cluster of about 22–26 spins is still cheap to simulate exactly, so this gives no route toward quantum
  necessity [INFERENCE].

## 3. Reduction to the KILLBOOK

| Part of the finding | Reduces to |
|---|---|
| 40 µs "classically reachable, no quantum needed" | The K-116 framing (σ-level classical comparator). It is now also weakened by §2 |
| Protein-structure value | K-105: forward-model-error arm (methyl rotation: the p19 b8 partner is intra-methyl) and value arm |
| 80–120 µs open | The existing R1-SIM-X residue under K-116. No new trigger: max \|ΔX\| = 0.006 < 0.01 |
| "Components need not converge when the observable does" | Identity given the definition of X, plus known OTOC hydrodynamics (1710.09835, 1710.09827) |

## 4. Recommended corrections (for the synthesis, not applied here)

- Do not adopt "the finite-cluster echo is converged at 40 µs" or "the CRITIC-C1 premise is falsified" in CRITIC,
  SYNTHESIS O-2 or SCIENTIFIC_MEMORY.
- Correct wording: "The T-X hybrid is biased at early times [MEASURED]. The probe-centred F ladder is flat over
  N = 16–22 but fails a b-aware cross-family check by up to 7 σ at 40 µs [MEASURED]. Convergence at t ≤ T3 is
  UNRESOLVED."
- Any future convergence ladder for F_ab should use clusters built around a ∪ b, i.e. nearest to either site, with
  the M2_b coverage reported.

## 5. Ledger

| Field | Value |
|---|---|
| CPU | 1485 CPU-s (about 25 CPU-min) for the dynamics, single-threaded (OMP/MKL/OPENBLAS = 1). Analysis < 2 CPU-s |
| Runs | 7 runs, each ≤ 344 CPU-s |
| Peak RSS | 0.70 GB |
| Machine load | 62–69% RAM and 70–95% CPU across the machine (other processes) at launch |
| Checkpoints | Kept in `runs/`, in tx_echo's checkpoint format |
| Web | 1 arXiv API call: the two abstracts cited above |
| Quantum resources | None. Simulator time is not physical quantum time |
| Leakage | None: the native geometry only defines the instance |
| Scope of writes | Nothing outside this folder was modified. No commit |

**Files**
- `verify_rel.py` / `verify_rel.json`: re-read of the lane's JSON (1/N gaps, series classes, M2_b coverage).
- `run_baware.py`: cross-family driver.
- `crossfamily.py` / `crossfamily.json`: comparison tables.
- `runs/`: the 7 echo runs at 40 µs.
