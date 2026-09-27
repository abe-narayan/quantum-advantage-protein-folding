# Experiment ledger (discovery sprint, 2026-09-26/27)

Each experiment is listed with: ID, hypothesis/criterion, configuration, command, results path, status. Pre-registered thresholds live in `PREREGISTERED/PREREG_G1_C1_Q4.md`, which includes a deviation log. All heavy jobs ran under the governor (`src/qapf/governor.py`; logs in `research/results/RAW/master/governor.jsonl`, per-job logs in `research/results/RAW/master/joblogs/`). Subfolders hold the per-lane records:

| Folder | Content |
|---|---|
| `PREREGISTERED/` | kill/survival criteria for G1, C1, C2, C3, Q4 (+ deviation log) |
| `SYNTHETIC/` | exact mechanism lab (Program B): landscape families, spectral gaps, Szegedy phase gaps, break-even ratios |
| `PROTEIN/` | G1 learned-posterior sampling: mode census, λ-path NRPT (pilot + T-scan), temperature exchange (Q4) |
| `QUANTUM/` | quantum-circuit proof-of-principle (shot-based echo circuit, hardware noise, mitigation) |
| `CLASSICAL/` | classical adversary implementations and their validation (sector-exact, sparse Pauli, classical spins, sub-cluster) |
| `ADVERSARIAL/` | attacks on the surviving line: stronger adversaries, replication on a second protein, independent reimplementations |
| `SCALING/` | C2/C3: classical cost of the best adversary vs cluster size N |

## Index

| ID | Question | Config | Command | Results | Status |
|---|---|---|---|---|---|
| G1-P | λ-path NRPT pilot (communication barrier, round trips) | 5 crops L=45–150, T=1, HMC only (no pivots) | `scripts/g1_sample_crop.py` | `RAW/g1_pilot/` | done (PILOT; exploratory) |
| G1-M1 | mode census 256 restarts | 16 chains × L=30–150 | `scripts/g1_mode_census.py --restarts 256` | `RAW/g1_modes/` | L=30–100 done; L=120/150 running |
| G1-M1b | mode census 2048 restarts | 8 crops (L=60/100/150) | `... --restarts 2048` | `RAW/g1_modes2k/` | queued |
| G1-M2 | λ-path NRPT T-scan (T ∈ {1,2,4,8}), pivots | 5 crops L=45–120 | `scripts/g1_sample_crop.py --T ... --pivot 4` | `RAW/g1_tscan/` | queued |
| Q4-M3 | temperature exchange, cooperativity | 24 crops L=30–120, 24 rungs T∈[1,40] | `scripts/tpt_crop.py` | `RAW/tpt/` | queued |
| B-SYN | synthetic mechanism lab | 5 families, n=6–16 | `scripts/synthetic_lab.py` | `RAW/synthetic/` | queued |
| C1-v1 | NMR pilot (typicality) | 1UBQ p17 N=12/14 | `scripts/nmr_gate.py` (v1) | `RAW/nmr_pilot/` | **excluded** (noisy reference; v1 rigid parameter unphysical) |
| C1 | NMR hardness–identifiability (v2) | 1UBQ 6 probes × 2 orient × γ∈{0,1000,5000}, N=10; N=12, N=14 | `scripts/nmr_gate.py` | `RAW/nmr_gate/` | running |
| C1-R | replication on a second protein | 1PGA 6 probes, N=10, γ=0 | `scripts/nmr_gate.py --pdb 1PGA` | `RAW/nmr_gate/` | running |
| C2/C3 | sparse-Pauli cost scaling (transfer and OTOC) | 1UBQ p19/p245, γ∈{0,1000}, N=8–20 | `scripts/nmr_sparse_scaling.py` | `RAW/nmr_sparse/` | running |
| Q-PoP | quantum circuit proof-of-principle + noise attack | 1UBQ p19/p245 N=10/12, p_step∈{0,1e-3,3e-3,1e-2} | `scripts/nmr_circuit_pop.py` | `RAW/nmr_pop/` | running |
| T-checks | theory companion checks (T1–T5) | — | `research/theory/PROOFS/*_checks.py`, `T3_*.py` | `RAW/t3_v2_checks`, `RAW/t4_*` | done |

Analysis: `scripts/analyze_g1.py`, `scripts/analyze_nmr2.py`, `scripts/analyze_c2.py`, `scripts/make_figures.py` → `research/results/PROCESSED/`, `research/results/FIGURES/`.
