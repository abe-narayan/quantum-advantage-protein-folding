# Figure plan

All figures are regenerable with `python scripts/make_figures.py`, plus the listed analysis scripts, into `research/results/FIGURES/`.

| # | Figure | Data | Message |
|---|---|---|---|
| 1 | The quantum-advantage map for protein structure: 28 mechanisms × 3 lenses, kill type, practical level | `research/discovery/CANDIDATE_MECHANISMS.md` | Nothing survives above practical L0 |
| 2 | Landscape-independent floor T*_Q vs L for Toffoli times 1–170 µs, with the one-day line | `research/theory/BREAK_EVEN.md` §1, T2 §4.3 | Quadratic sampling speedups cannot be practical at any landscape hardness |
| 3 | G(L) Toffolis per walk step (D1/D2/D3, precision) | `research/theory/RESOURCE_MODELS.md` | Arithmetic on pair terms dominates |
| 4 | Mode census and NRPT vs L (`g1_census.png`, `g1_nrpt.png`) | `results/PROCESSED/g1_summary.json` | Real classical difficulty at L ≥ 100 does not rescue the quantum route |
| 5 | Transmission: soft readout vs argmin at L = 60/100 | `results/PROCESSED/transmission_summary.json` | Does posterior averaging buy accuracy? |
| 6 | NMR: transfer vs echo, exact vs adversary panel; FI per time (`nmr_example.png`) | `results/RAW/nmr_gate/*` | Transfer is compressible; the echo is not |
| 7 | ε-ladder and exact cost vs N (strings, wall-clock) | `results/PROCESSED/c2_summary.json`, `R1_director/c2_echo_check.json` | Compression fails; exact simulation is cheap at small N |
| 8 | Echo cluster-size convergence (R1-SIM) and hybrid adversary error | `results/PROCESSED/cone_summary.json`, `R1SIM_hybrid/out/` | Light cone vs exact reach |
| 9 | Reversal envelope vs informative window (T3/T2) | `experiments/ADVERSARIAL/R1_physics_feasibility/` | Physical irreversibility kills the practical window |
| 10 | Noise attack on the shot-based echo circuit | `results/RAW/nmr_pop/*` | Only ≤ 1e-4 two-qubit error keeps a window, and only at trivially simulable N |
