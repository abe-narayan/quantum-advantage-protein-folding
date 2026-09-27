# Current State

_Last updated: 2026-09-27, later the same day. **Discovery sprint RESUMED.** This supersedes the "PAUSED" entry below, which is kept for history._

## Status after resume and the adversarial review of R1

- **Compute.** The governor is running again on `research/results/RAW/master/spool_resume.jsonl`.
  - Limits: 4 workers; RAM launch ≤ 82%, suspend 88%, kill 92% (live-configurable via `control.json`).
  - Queue order: R1-SIM cone convergence (T-A) first, then transmission (R2-T), census L = 120/150, 2048-restart census, T-scan, temperature exchange and the synthetic lab.
  - Cancelled (`cancel.txt`): C1/HN NMR panel jobs, C2 N ≥ 14, PoP N=12.
- **R1 (NMR echo window) is KILLED** as a protein-structure quantum advantage (KILLBOOK K-105; `experiments/ADVERSARIAL/R1_SYNTHESIS.md`, `R1_CRITIC.md`).
  1. The N=10 "classical failure" was a failure of truncations that stopped at ε ≥ 1e-4. At ε = 3e-5, which is roughly the full operator space, and in exact simulation (seconds), the echo is reproduced.
  2. The 10-spin reference is unconverged.
  3. The pre-registered C3 feasibility survival clause failed: the informative window lies beyond measured reversal horizons.
  4. Value: gain ~1.1–1.5 under realistic priors and attenuation; fault-tolerant break-even needs N_eff ≈ 30–47 at 4–6 h per evaluation.
- **Open residue: R1-SIM.** Is the converged dense-network echo beyond exact classical reach?
  - This is a physics-simulation, category-3 candidate. It cannot revive R1.
  - Pre-registered; T-A running.
- **Every discovery mechanism is killed** (28/28, K-101…K-105). **No quantum advantage for protein-structure computation survives in any examined regime.**

---

# Previous entry (PAUSED)

_Last updated: 2026-09-27. **Discovery sprint PAUSED** at the user's request (resume in ~2 h). The previous entry (same date, "in progress") is superseded by this one; see git history for it._

| Field | Value |
|---|---|
| Current research question | Is there a real place where quantum computation does something important for protein structure that the best classical approach cannot do as efficiently? If not, where and why does it fail? |
| Phase | **Discovery sprint, PAUSED mid-experiment.** The master governor (and every governed job) was stopped by the host for low system memory while the session was idle, and the user then asked to pause. Nothing is running. All completed results are committed. |
| Strongest hypothesis | **H-C1 echo branch (Program C):** protein ¹H dipolar **echo (first-order OTOC)** signals carry structural Fisher information past the failure time of every classical approximation tested. MEASURED at N=10 on 1UBQ and 1PGA, dense and amide-only networks (f_hard 0.55–1.0; echo FI 10–160× transfer FI). Survives the embedding test to N_env = 12 (echo) / 14 (transfer). The needed classical string count grew 16× from N=8 to N=10 (≈ ¼ of the full 4^N operator space). Prior art: O'Brien et al., PRX Quantum 2022 (NM-1). |
| Strongest competing hypothesis | H-C1-null: the echo window is a small-N effect. (i) Exact classical simulation of the light cone stays feasible (sector-exact N=14 ≈ 15 min). (ii) A coarse-grained operator-front model reproduces the echoes (untested). (iii) The information weakens in larger baths: transfer late-FI fell to 22–24% at N_env = 14. |
| Killed | All 28 discovery mechanisms as quantum-advantage claims (`discovery/KILLED_DIRECTIONS.md`). Sampling/optimisation of the learned energy is killed at the practical level by the landscape-independent floor T*_Q ≥ 0.26 yr per sample (T2/T3). NMR 2-point transfer is killed: sparse Pauli dynamics is exact at N=10 (f_hard = 0). |
| Current best quantum architecture | None load-bearing. Candidate: quantum forward simulation of NMR echo dynamics. The shot-based circuit is exact past the classical failure time without noise. With echo normalisation it keeps a window only at ≤ 1e-3 depolarising noise per qubit per Trotter step (≈ 1e-4 per two-qubit gate). Fault-tolerant cost ≈ 11 h per forward evaluation (depth-limited); practical level L0. |
| Current strongest classical baseline | NMR: sparse Pauli dynamics (ε down to 3e-5), weight-w Pauli, sub-cluster exact, classical spins, norm-corrected and α-calibrated echo estimators, Gaussian-bath dephasing. Sampling: NRPT + HMC + pivots; converged multistart. |
| Current Git checkpoint | 50e0c9e (plus the pause commit that adds this file and `scripts/make_resume_spool.py`). |

## What finished (on disk, committed)

- C1 v2: 1UBQ probe 19 (N=10; γ = 0, 1000, 5000; 2 orientations). 1PGA replication (2 probes). C1-HN dilute amide networks (≥ 8 jobs).
- R1-E embedding (1UBQ probes 19 and 245): kill rules not fired. Summary: `results/PROCESSED/embed_summary.json`.
- Q-PoP quantum circuit, N=10, 2 probes, 4 noise levels: `results/RAW/nmr_pop/`. The N=12 run is partial.
- C2/C3 sparse-Pauli scaling at N = 8 and 10 (γ = 0 and 1000). The N=12 and N=14 runs were interrupted; their `.partial` files are kept but will be recomputed.
- Theory T1–T6, resource models, all discovery artifacts, report and claim-audit drafts (`reports/`, with ⟦…⟧ fill-in markers).
- R2-T transmission: 1 of 32 crops (v2 weighting).

## RESUME PROCEDURE (do exactly this)

1. **Check memory first.** Resume only if RAM use is < 75% with the user's apps open. The host kills background shells under memory pressure.
2. **Rebuild the queue** (skips finished outputs, cancelled tags and duplicates; orders by decision value):
   `python scripts/make_resume_spool.py`. At pause time this gave 177 jobs:
   - 11 C2/C3 scaling (γ = 0 first, N ascending; **decisive**);
   - 31 transmission crops;
   - 1 PoP N=12;
   - 52 C1/HN NMR;
   - 33 census (L = 120/150 + 2048-restart);
   - 20 T-scan;
   - 24 temperature exchange;
   - 5 synthetic.
3. **Set a conservative control file.** Write `research/results/RAW/master/control.json` =
   `{"max_workers": 3, "cpu_launch_max": 0.75, "cpu_suspend": 0.90, "cpu_resume": 0.80}`.
   The N ≥ 14 jobs use 2–3.5 GB each, so keep ≤ 3 workers.
4. **Start the governor on the resume spool** (a background shell):
   `python -m qapf.governor /dev/null --log research/results/RAW/master/governor.jsonl --max-workers 3 --spool research/results/RAW/master/spool_resume.jsonl --forever --stop-file research/results/RAW/master/STOP`
5. **Analyse as results land:**
   - `python scripts/analyze_c2.py` for C2/C3. The pre-registered kill: power-law fit better by ΔBIC > 10, or M*(60) < 1e9.
   - `python scripts/analyze_transmission.py`
   - `python scripts/analyze_nmr2.py research/results/RAW/nmr_gate`
   - `python scripts/analyze_g1.py`
   - `python scripts/make_figures.py`
6. **Then:**
   - launch the adversarial-replication workflow on the echo claim (independent reimplementation, FI-methodology attack, operator-front classical estimator; agents must submit heavy runs through the governor);
   - fill the ⟦…⟧ markers in `reports/QUANTUM_ADVANTAGE_DISCOVERY_REPORT.md` and `reports/QUANTUM_ADVANTAGE_CLAIM_AUDIT.md`;
   - write `research/paper/*` and update KILLBOOK / SCIENTIFIC_MEMORY / OPEN_QUESTIONS;
   - commit;
   - give the user the condensed final report.

If compute must be cut: C2/C3 at N = 12–16 (γ = 0) and the transmission test are the decisive items. The G1 production runs (T-scan, temperature exchange, 2048 census) are pre-registered confirmations of kills already established by theory.

## Where things are

- **Discovery:** `research/discovery/` (CANDIDATE_MECHANISMS, CLASSICAL_COUNTERARGUMENTS, KILLED/SURVIVING_DIRECTIONS, ADVANTAGE_THESES, ARCHITECTURE_SEARCH, QUANTUM_PRIMITIVES, NOVELTY_MEMOS, attack_records.json).
- **Theory:** `research/theory/` (PROOFS T1, T2, T4, T6; NO_GO T5; RESOURCE_MODELS (T3); ADVANTAGE_CONDITIONS; COMPLEXITY; BREAK_EVEN; `nmr_resource_model.py`).
- **Pre-registration + deviation log:** `research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`. Ledger: `research/experiments/README.md`.
- **Code:** `src/qapf/nmr/` (spins.py: sector-exact, Pauli, classical spins; circuit_pop.py: shot-based quantum circuit), `src/qapf/protein`, `src/qapf/sampling`, `scripts/`.
- **Governor state:** `research/results/RAW/master/` (governor.jsonl, spool.jsonl, cancel.txt, control.json, joblogs/).
