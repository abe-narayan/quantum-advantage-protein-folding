# quantum-advantage-protein-folding

A research program on one question:

> **Where, if anywhere, can quantum computing provide a real, testable, scientifically defensible advantage for protein structure computation?**

The program is algorithm-agnostic and architecture-agnostic. No quantum method (VQE, QAOA, sampling, walks, QSVT, fault-tolerant algorithms, …) is presumed promising. Every quantum component must beat a seriously tuned classical twin and pass a quantum necessity test: FULL vs. ABLATION, asking what capability disappears when the quantum part is removed. Claims are labeled with an explicit advantage category, and native-structure leakage is strictly controlled.

It succeeds the *Protein-Folding-Algorithm* project (Sprints 1–33), whose final sprint found that its CVaR-VQE stage was not load-bearing.

## Status

**Skeleton only.** No benchmarks, baselines, quantum algorithms, architectures or results exist yet. Next: reconstructing Sprint 33, then literature research, then architecture discovery.

## Layout

- `src/qapf/`: reusable library code
- `tests/`: pytest suite
- `research/`: persistent scientific state (charter, current state, hypotheses, killbook, memory, literature map)
- `literature/`, `theory/`: notes, bibliography, derivations, complexity and advantage analysis
- `benchmarks/`, `classical/`, `quantum/`, `architectures/`: research workspaces (PLANNED)
- `experiments/`: pre-registrations, configs, and running, completed and adversarial runs
- `results/`, `reports/`: raw and processed outputs, figures, tables, write-ups

## Development

```bash
pip install -e ".[dev]"        # add ,analysis for pandas/matplotlib
pytest
```

See `CLAUDE.md` and `research/RESEARCH_CHARTER.md` for the scientific rules.
