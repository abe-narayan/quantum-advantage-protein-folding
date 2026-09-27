# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A research program asking one question: **where, if anywhere, can quantum computing provide a real, testable, scientifically defensible advantage for protein structure computation?**

It is algorithm-agnostic and architecture-agnostic. It is **not** a CVaR-VQE project. VQE is one candidate among many (QAOA, ADAPT-style methods, quantum walks, amplitude amplification/estimation, Gibbs/Metropolis sampling, QITE, Hamiltonian simulation, QSP/QSVT, quantum generative/Boltzmann models, tensor-network hybrids, fault-tolerant algorithms, new formulations). The whole folding pipeline may be replaced. The goal is to find a computational bottleneck where a quantum primitive genuinely matters, or to show convincingly that there isn't one in a given regime.

The full mission, historical context and research cycle are in `research/RESEARCH_CHARTER.md`.

## Resuming work: read the research state first

Chat history is not memory. At the start of a session, read these files **before proposing work**:

1. `research/CURRENT_STATE.md`: current question, leading and competing hypotheses, best architecture and baseline, running and next experiments, Git checkpoint
2. `research/KILLBOOK.md`: directions that were already killed, and why. Don't reopen them without new evidence.
3. `research/HYPOTHESES.md` and `research/OPEN_QUESTIONS.md`

`research/SCIENTIFIC_MEMORY.md` holds durable lessons, including those from the predecessor project. `research/LITERATURE_MAP.md` maps prior work. Update `CURRENT_STATE.md` whenever the scientific state changes. Never delete or rewrite history in these files. Supersede entries with dated notes instead.

## Predecessor project (Protein-Folding-Algorithm, Sprints 1–33)

It is a source of baselines, negative results, benchmark definitions, leakage controls and reusable infrastructure. It is **not** an architecture to preserve, and it must not be copied wholesale. Sprint 33's findings (see `research/SCIENTIFIC_MEMORY.md`) are the starting prior:

- The largest structural gains came from better structural information and decoding, not from the quantum stage.
- CVaR-VQE was not load-bearing in the final built-chain result. Tuned classical search matched or beat it.
- Several apparent quantum wins disappeared under stronger classical controls.
- CVaR tail collapse and solver equivalence were real failure mechanisms.

The local path of that repository is not yet recorded. Ask the user rather than guessing.

## Non-negotiable scientific rules

**Claim categories.** Every claim about a quantum component must name exactly which of these it is:
1. quantum usefulness
2. empirical quantum advantage
3. computational/resource advantage
4. sampling advantage
5. hardware advantage
6. theoretical/provable advantage

None of the following is evidence of advantage on its own: lower RMSD, beating a weak baseline, more qubits, a larger Hilbert space, a simulator beating one classical implementation, fewer optimizer iterations, or a "more interesting" distribution.

**Strong classical twin.** Every serious quantum architecture needs a seriously tuned classical counterpart (SA, parallel tempering, MCMC/replica exchange, SMC, beam/evolutionary search, multistart, branch-and-bound, exact enumeration where feasible, tensor networks, problem-specific combinatorics, vectorized/multiprocess implementations). Tuning effort must be comparable on both sides.

**Quantum necessity test.** Run FULL (classical + quantum) against ABLATION (the same architecture with the strongest classical replacement for the quantum component). Answer: *what capability disappears when the quantum component is removed?* If the answer is "nothing important", the component is not load-bearing. Kill or redesign the architecture and record it in `research/KILLBOOK.md` and `architectures/killed/`.

**Leakage.** Native structures may be used only for final evaluation, explicitly labeled ORACLE diagnostics, and scientific analysis. They must never enter production optimization, hyperparameter selection, candidate selection, training, quantum oracle construction, or algorithm selection based on test performance. Keep DEP (deployable, native-free) and ORACLE (native-informed) code paths, configs and results clearly separated and labeled. Train/dev/test splits live in `benchmarks/splits/`, and test sets are not used for selection.

**Resource accounting.** Record what applies: wall-clock, CPU time, peak RAM, objective/candidate evaluations, qubits, depth, gate and two-qubit gate counts, shots/measurements, state preparation, readout, classical pre/postprocessing, communication, simulator, compilation and error-mitigation overhead, and hardware assumptions. **Simulator runtime is never physical quantum runtime.** Report them separately.

## Research workflow

READ → FORM HYPOTHESIS → PRE-REGISTER → IMPLEMENT → RUN → COMPARE → ATTACK → REPLICATE → SCALE → THEORIZE → DECIDE → **KILL** or **ESCALATE**.

- Pre-registration goes in `experiments/preregistered/` *before* the run: the hypothesis, the comparator, the metric, the kill criterion and the analysis plan.
- Adversarial attacks on a positive result (stronger baselines, leakage audits, seed and split changes) go in `experiments/adversarial/`.
- No large unstructured hyperparameter sweeps without a stated hypothesis. Don't re-run established results.
- Every substantial experiment records the full ledger fields listed in `research/RESEARCH_CHARTER.md` (ID, hypothesis, algorithms, targets and splits, quantum resources, compute, metrics, comparator, effect size, uncertainty, statistical test, replication, leakage status, hardware assumptions, conclusion).
- Preserve negative results, failed hypotheses and raw metadata (`results/raw/`). Never delete historical evidence because an approach failed.

## Compute policy

The machine has 8 logical CPUs and about 15.6 GB RAM. During major runs, target about 94–95% CPU and RAM utilization and **never intentionally exceed 95%**. Throttle dynamically (`psutil` is available) and parallelize independent experiments. Don't launch expensive runs without a pre-registration.

## Git discipline

Commit checkpoints often. Before any destructive redesign, check `git status` and commit meaningful work first. Record the current checkpoint in `research/CURRENT_STATE.md`.

## Engineering

- Python ≥3.11, `pyproject.toml` (setuptools), `src/` layout, importable package `qapf`.
- Install: `pip install -e ".[dev]"` (add `analysis` for pandas/matplotlib)
- Tests: `pytest`. Single test: `pytest tests/test_package.py::test_import -q`
- Core dependencies are only NumPy and SciPy. Add a quantum library (Qiskit, PennyLane, Cirq, etc.) **only when a specific research lane needs it**, preferably as an optional extra named for that lane. No library, and no algorithm family, is the project-wide framework.
- Top-level directories (`classical/`, `quantum/`, `architectures/`, `benchmarks/`, `experiments/`, `theory/`, `literature/`, `results/`, `reports/`) are research workspaces. Reusable library code belongs in `src/qapf/`. The layout may change as the science demands.
- Don't create placeholder implementations to fill directories. Empty directories hold only `.gitkeep`.

## Status (as of 2026-09-26)

Only the skeleton exists. Everything else is **PLANNED**: benchmarks, splits, baselines, quantum algorithms, architectures, experiments and results. Nothing in this repository is a research result yet. The next phase is the scientific reconstruction of Sprint 33, then literature research, then architecture discovery.
