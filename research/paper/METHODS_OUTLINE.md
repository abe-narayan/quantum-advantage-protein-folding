# Methods outline

1. **Instrument.** Leakage-screened ladder: 16 chains × L = 30–150 (`src/qapf/protein/targets.py`), with R1/R2/R3 exclusions against the esmprior training crops.
   - Vendored A80/esmprior_v1 energy, bit-exact to the predecessor (`src/qapf/protein/`).
   - Native structures are used for evaluation only (ORACLE).
2. **Classical sampling baselines.**
   - λ-path non-reversible parallel tempering (DEO swaps, Syed et al.) with HMC, diagonal mass adaptation and prior-proposal pivots.
   - Temperature replica exchange.
   - Multistart L-BFGS mode census with 2 Å clustering.
   - Transmission test: energy- and hit-weighted soft readouts vs argmin, S33 MDE contract.
3. **Theory.**
   - T1 reduction theorem; T2 QSA statement and break-even inequality; T3 Toffoli costing (qubitised LHPST walk, spline pair terms, fixed-point precision); T4 amplified mode finding; T5 ceilings; T6 transfer-vs-echo mechanism.
   - Every claim is tagged DERIVED / THEORETICAL / INFERENCE; each note has a companion check script.
4. **NMR forward models.**
   - Secular homonuclear dipolar Hamiltonian from OpenMM-protonated PDB structures; first-order Trotter circuit.
   - Exact references: sector-exact Schur/eigh (γ = 0), sector stepping with per-spin dephasing, statevector typicality for N ≥ 16.
   - Adversaries: weight-w and ε-sparse Pauli propagation; sub-cluster exact; classical spins/DTWA; CCE; operator-spreading/FKPP; stochastic Pauli; MPO; hybrid exact core + classical bath.
   - Fisher information by finite differences; estimator-level bias fits; embedding; reversal envelopes.
5. **Quantum proof-of-principle.** Shot-based echo circuit (random basis inputs, forward/backward Trotter, projective readout) with depolarising noise and echo-normalisation mitigation.
6. **Resource models.**
   - Surface-code logical Toffoli times 1–170 µs; product-formula T counts with Ross–Selinger synthesis; amplitude estimation.
   - Depth-limited vs serial accounting.
7. **Adversarial protocol.**
   - Pre-registration with a deviation log.
   - Three-lens attack on every mechanism; seven-lens attack on the surviving lead.
   - Independent reimplementation, replication on a second protein, completeness critic.
8. **Compute governance.** Single-machine governor (CPU/RAM ≤ 95%), job spool, cancel list, resume queue.
