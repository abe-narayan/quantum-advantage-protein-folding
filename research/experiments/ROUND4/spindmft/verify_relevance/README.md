# Relevance and novelty verification of ROUND4 lane `spindmft`

_2026-09-28. Adversarial verifier, relevance lens._

**Claim under attack.** The spinDMFT kill rule for R1-SIM at t ≤ 120 µs does not fire, because the round-3 hybrid comparator F_∞ = H_∞(CSD) + X₁₈ is wrong. At 40 µs, two classical families agree within σ on 8/8 series, so the echo there is classically reachable (INFERENCE). 80 µs is partly open and 120 µs is open. No quantum advantage is claimed. Verdict: INTERESTING.

**Tags.** MEASURED (a file in this folder or a cited file), DERIVED, LITERATURE (arXiv abstract or API fetched this session), INFERENCE, UNPROVEN.

## Verdict: REFUTED on relevance. The measurements stand.

The lane's numbers are reproduced, and two of its central measurements are confirmed out of sample (§1). What does not survive the relevance lens is the label **INTERESTING**:

1. **Where the echo can be observed (≈ 40 µs, about 4–5 T2), the finding reduces to a kill.** It moves the early window toward classical reach, which is the K-116 / K-105 direction. My check (§2) makes that stronger: an isolated exact cluster of 10–12 spins, centred on {a, b}, reproduces the converged-looking value within σ at 40 µs in 0.3–20 CPU-s.
2. **The part it calls open (80–120 µs) has almost no physical signal.**
   - That window is 8–15 T2 in network units, beyond T3 = 32–66 µs.
   - Under a physical T2, the observable part of the remaining classical ambiguity is at most 1.2σ, and at most 0.2σ for the site-resolved polarisation echo.
   - The forward-model error in the same window is 9–33σ (§3).
3. **Nothing in the claim touches protein structure.** The lane concedes this, and K-105 is untouched. The only new ingredient is a heuristic quenched-bath spinDMFT OTOC (A3). It fails beyond 40 µs, and the idea of DMFT for OTOCs already exists for fermion lattices (§4).

**Recommended recording.** The lane's methodological corrections are correct and should be recorded as bookkeeping:
- retire the hybrid comparator;
- withdraw CRITIC C1's 3.1–8.2σ table at 40 µs;
- restate the T-X-early / K-116 X-drift criteria in terms of F and a b-aware cluster family.

Record the finding as a **KILL-leaning classical-adversary result for the observable window**, pending the lane's own replication on 1PGA p390 / 1UBQ p487. Do not record it as an INTERESTING open lead.

| Level | This verifier | Lane |
|---|---|---|
| Theoretical | **L0** | L0 |
| Practical | **L0** | L0 |

Claim category: none of 1–6 (agrees with the lane).

## 1. Reproduction and out-of-sample checks [MEASURED]

**R0. The lane's analysis reproduces bit for bit.**
- `analyze_rerun.py` is `../analyze.py` with only its output path changed. Its output `analysis_rerun.json` has 0 differences from `../analysis.json`, and its stdout is identical.
- Provenance: the spinDMFT b-aware outputs are stamped 12:32–12:36 and `PREREG_spindmft.md` (Addendum B) 12:36:55. The exact b-aware runs come after, at 12:40–12:46 (file mtimes). So "predicted before the exact runs" holds.

**C3. Out-of-sample N = 22 check** (the sibling lane `tx_early` files, read-only; the spindmft lane did not use them). Probe p245, t = 40 µs, probe family:

| site | F₂₀ | F₂₂ | dF | dX |
|---|---|---|---|---|
| 1 | 0.9791 | 0.9790 | −0.0001 | +0.0042 |
| 7 | 0.6990 | 0.7005 | +0.0015 | +0.0059 |
| 8 | 0.9551 | 0.9550 | −0.0000 | +0.0044 |
| 9 | 0.9726 | 0.9726 | +0.0000 | +0.0044 |

- d(H + floor) = −0.0044 (dH −0.0022, dfloor −0.0022). The typicality error at N = 22 is about 0.0005.
- **The flat-X refutation holds at a new N.** F is flat to ≤ 0.0015 while X rises on 4/4 sites. A hybrid with constant X would predict dF = −0.0044.
- **The family bias persists.** At p245 b7, F₂₂ = 0.7005 is **0.063 (6.3σ) below** the exact b-aware N = 16 value (0.7637), even though the probe family has been flat from N = 14 to 22.
- Side effect: the T-X-early statistic |X₂₂ − X₂₀| here is 0.0042–0.0059. That straddles the 0.005 threshold while F is converged to 0.0015, a concrete instance of the lane's point that the X criterion is ill-posed.

## 2. Is spinDMFT what carried the 40 µs result? Isolated exact b-aware clusters [MEASURED]

`relevance_checks.py`, part C1. These are deterministic sector-exact runs on the same Trotter circuit. The b-aware construction is identical to the lane's: {a, b} ∪ protons nearest to a or b, with **no bath**.

Pipeline check: my sector-exact N = 12 agrees with the lane's typicality N = 12 to ≤ 0.0042 at every cell, within the typicality error of 0.0055.

| series, 40 µs | isolated exact N = 8 / 10 / 12 | lane exact (typicality) N = 12 / 14 / 16 | spinDMFT b-aware, n_c = 10, protein | spinDMFT probe-family, n_c = 10, protein | probe-family F₁₈ |
|---|---|---|---|---|---|
| p245 b7 | 0.740 / **0.757** / 0.770 | 0.767 / 0.761 / **0.764** | 0.764 | 0.758 | 0.699 |
| p19 b8 | 0.979 / **0.979** / 0.978 | 0.978 / 0.977 / **0.978** | 0.983 | 0.966 | 0.953 |
| p19 b9 | 0.943 / **0.939** / 0.940 | 0.941 / 0.945 / **0.948** | 0.953 | 0.959 | 0.954 |

Reading:
- **At 40 µs, an isolated 10–12-spin cluster in the right family already sits within σ of the exact N = 16 value on 3/3 series.** |iso₁₀ − ex₁₆| = 0.007 / 0.0015 / 0.009, and |iso₁₂ − ex₁₆| ≤ 0.008. Cost: 0.3 CPU-s at N = 10 and about 20 CPU-s at N = 12.
- **The Gaussian bath's own share of the b-aware spinDMFT prediction is small:** +0.007 / +0.004 / +0.014 (≤ 1.4σ). It moves toward the exact N = 16 value on 2/3 series and away on 1/3.
- **The genuinely bath-borne test is the probe-family route**, where b's partners sit in the bath. There spinDMFT lands within σ of exact b-aware on 1/3 series (p245 b7, −0.005) and just outside on 2/3 (−0.012, +0.011).
- So the E-B "prediction" is real, but it is a weak test of spinDMFT physics. It is dominated by the choice of cluster family, which a sub-second exact calculation also gets right.
- **Consequence [INFERENCE].** At 40 µs the converged echo is not just σ-level reachable. It is reachable by small exact clusters, provided the cluster is centred on {a, b}. This agrees with R1's original "σ-cone of 16–20 spins at 40 µs", corrected for cluster family. It reduces to the K-116 finding that the relevant object is within classical reach.
- **Caveat on "flat in N" [MEASURED, reference cone].** Step convergence in one family can hide a shift of 6–10σ:
  - p19 b1 jumps from 0.502 (N = 12) to 0.607 (N = 14), then stays flat;
  - p245 b7 stays flat at about 0.70 from N = 14 to 22, while the b-aware value is 0.764.

  The 5 probe-local series rest on probe-family flatness plus a spinDMFT bath correction ≤ 0.004. That is weaker than "two independent families". The lane's next test 1 (b-aware clusters for all 8 series) is the right closure.

## 3. Is the residue it calls open physically meaningful? [DERIVED from MEASURED F + LITERATURE envelopes]

**Method** (C4; the same envelope functions and T2 values as the round-3 relevance verifier).
- Spread = max − min over the lane's classical F_∞ candidates at each series. The hybrid is excluded because it is refuted.
  - Probe-local series: F₁₈, F₂₀, F_corr (n_c = 10) and F_corr20.
  - b-remote series: exact b-aware N = 14 and 16, and spinDMFT b-aware.
- Visible spread = A(t) × spread, where A(t) is the reversal envelope from Sánchez–Chattah–Pastawski (PRA 105, 052232 (2022); LITERATURE-REPO):
  - LE: Loschmidt echo, T3 = 6.7 T2, forward time only, the generous choice;
  - PE: local polarisation echo, T3 = 4 T2, the protocol a site-resolved experiment needs.

| T2 normalisation | T3 (LE / PE), µs | 40 µs: visible spread (LE / PE) | 80 µs: visible spread | 120 µs: visible spread | 120 µs: whole visible signal, median (LE / PE) |
|---|---|---|---|---|---|
| network static, 8.0–8.1 µs (rigid protein) | 54 / 32 | 0.55σ / 0.25σ | **0.52σ / 0.06σ** | **0.09σ / 0.00σ** | 0.5σ / 0.0σ |
| network, rotor-averaged, 9.8 µs | 66 / 39 | 0.62σ / 0.36σ | **1.18σ / 0.22σ** | **0.40σ / 0.02σ** | 2.0σ / 0.1σ |
| isolated cluster, 14–18 µs (non-physical, most generous) | 94–123 / 56–73 | 0.70σ / 0.60σ | 3.2σ / 1.7σ | 5.6σ / 1.7σ | 28.8σ / 8.5σ |

Raw (unattenuated) classical spread:

| t (µs) | max | median |
|---|---|---|
| 40 | 0.007 | 0.004 |
| 80 | 0.039 | 0.019 |
| 120 | 0.106 | 0.062 |

**Forward-model error, same model** (`ADVERSARIAL/R1_physics_feasibility`, 1UBQ p19 N = 10):
- at t < 80 µs: methyl rotation 7.1σ, 1 kHz offsets 5.4σ;
- at t ≥ 80 µs: rotation 32.6σ, offsets 9.2σ, 15% reversal mismatch 22.6σ;
- first exceedance at 40 µs.

Reading:
- **Under either physical T2, the open 80–120 µs ambiguity is at most 1.2σ observable** (the best-case Loschmidt echo, rotor-averaged), **and at most 0.22σ under the site-resolved polarisation echo.** At 120 µs the whole echo is ≤ 2σ observable.
- **At 80 µs the classical spread (≤ 3.9σ raw) is smaller than the model's own physical error in the same window (≥ 9σ).** Pinning the idealised echo to σ there would not make any forward model of a real sample σ-accurate.
- Only the non-physical isolated-cluster T2 lets the residue exceed σ. That convention was already judged the most generous one in round 3.
- **Consequence [INFERENCE; inherits K-105's caveat that T3/T2 comes from model solids, not a protein].** The lane's "open" windows are an idealised-model computation with no observable consequence at σ. That is the same status the round-3 relevance verifier gave the 160–320 µs window, now extended down to 80–120 µs.

## 4. Novelty against the literature [LITERATURE, arXiv API / abs fetched this session]

| Item | Prior art | Status |
|---|---|---|
| spinDMFT / nl-spinDMFT (the lane's classical engine) | 2107.07821, 2403.10465, 2307.14188, 2512.15572 (IDs verified by the lane; not re-fetched) | Existing method, applied here |
| An OTOC extension of dynamical mean-field theory | Tsuji, Werner & Ueda, arXiv:1610.01251, PRA 95, 011601(R) (2017): OTOCs from "nonequilibrium dynamical mean-field theory generalized to an extended Kadanoff-Baym contour". Tsuji & Werner, arXiv:1812.04217. Rangi, Moreno & Tam, arXiv:2403.03214 | The idea exists for fermion lattices. **No spinDMFT or dipolar version was found** (query abs:"out-of-time-order" ∧ abs:"dynamic mean-field" returned only these fermionic works). The lane's A3 is a cruder quenched-field version, not an extended-contour one, and it fails beyond 40 µs. Low method-level novelty, and it is not load-bearing (§2) |
| A hybrid quantum-classical adversary for echoes / OTOCs | Starkov & Fine, 1806.09355 and 1911.00990, and Navez, Starkov & Fine, 1812.02155: free induction decays and relaxation only | Consistent with the lane: no published hybrid OTOC |
| b-aware ({a, b}-centred) cluster family | Pre-specified in-repo: `ROUND3/SYNTHESIS.md` §2.2, T-X3, "b-aware cluster family (nearest to {a} ∪ {b})" | Executed here for the first time. Not a new idea for the program |
| F = 1 − 2·w_b (the flat-X mechanism) | Elementary Pauli-weight identity. Related to the in-repo decomposition F = H + R (round-3 relevance verifier) | A correct internal correction to CRITIC C1, not an external novelty |
| "NMR OTOCs are a beyond-classical target" | O'Brien et al., arXiv:2109.02163; Zhang et al., arXiv:2510.19550 (LITERATURE-REPO) | The lane's result points the other way for the observable window |

## 5. Reduction to KILLBOOK entries

| Sub-claim | Reduces to | Why |
|---|---|---|
| The kill rule does not fire (0/8, 0/8, 1/8) | Nothing to record as a lead | A comparator defect, not a hardness signal. The lane agrees |
| 40 µs is σ-level classically reachable | **K-116** (R1-SIM against exact simulation) and **K-105** (structure) | Small exact clusters suffice (§2). This restores the round-3 relevance verifier's position that the observable window is within reach, which CRITIC C1 had called unresolved |
| 80 µs partly open, 120 µs open | **K-105** (reversal horizon and forward-model error) and the round-3 relevance verdict on the late window | Beyond T3 in network units; at most 1.2σ observable; model error 9–33σ (§3) |
| The flat-X refutation | Invalidates the K-116 revival template's "X drifts ≥ 0.01 per step" trigger and the T-X-early X criterion | Correct and useful. It makes the residue harder to revive, not easier |

## 6. What would change this verdict

All of the following would be needed, and even together they would give only a category-3 physics question, never a protein-structure one:
1. A b-aware exact family and a thermodynamic correction that **disagree** by more than 3σ at t ≤ T3 in network units (≤ 40–60 µs), replicated on 1PGA p390 and 1UBQ p487.
2. A measured protein T3/T2 ≥ 15 (K-105 revival condition ii), so that 80–120 µs becomes observable.
3. A forward model including methyl rotation, offsets and reversal mismatch that is accurate to σ in that window.

## Compute, process and files

**Compute.**
- 216.7 CPU-s of recorded exact runs (sector-exact N = 8–12).
- About 9 further CPU-min were lost on one N = 14 sector-exact attempt. I stopped it because it duplicated the lane's own exact_pairb_N14; it produced no output.
- Analysis re-run: under 10 CPU-s.
- Total: about 13 CPU-min, single-threaded (OMP/MKL/OPENBLAS = 1).
- Peak RSS was not measured. The completed runs have sector blocks of at most 924 × 924 complex, a few tens of MB. The aborted N = 14 run had blocks of 3432 × 3432, about 190 MB each.

**Checkpointing.** `relevance_checks.ckpt.json` is written atomically after every (series, N) run and is kept.

**Process note.**
- The harness auto-backgrounded the first invocation when it exceeded 600 s. I stopped that task and then my own orphaned `python relevance_checks.py` process (PID 38536). I touched no other process.
- The re-run resumed from the checkpoint.

**Scope.** Nothing was written outside this folder. No git commit.

**Files.**
- `analyze_rerun.py` → `analysis_rerun.json`, `analyze_rerun_stdout.txt`: the bit-identical reproduction of the lane analysis.
- `relevance_checks.py` → `relevance_checks.json` (sections C1–C4, raw runs), `relevance_checks_stdout.txt`, `relevance_checks.ckpt.json`.
- Read-only inputs:
  - `../out/*`, `../analysis.json`, `../analysis_stdout.txt`;
  - `../../tx_early/runs/1UBQ_p245_N2{0,2}_echo_*.json`;
  - `../../../ADVERSARIAL/R1_physics_feasibility/{scales.json, physics_1UBQ_p19_N10_o0_g0.json}`;
  - `../../../ADVERSARIAL/R1_theory_hardness/typicality_cone/1UBQ_p{19,245}_N1{2,4,6,8}.json`.
