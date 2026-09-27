# Quantum Advantage Discovery Report: protein structure computation

_quantum-advantage-protein-folding, discovery sprint of 2026-09-26/27. Every statement's evidence class is in `reports/QUANTUM_ADVANTAGE_CLAIM_AUDIT.md`. Pre-registrations and deviations are in `research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`. The fill-in markers `⟦…⟧` are replaced by final numbers in the last revision._

---

## 1. Executive summary

⟦EXEC-SUMMARY⟧

---

## 2. Research question

Is there a computational task that matters to protein structure science where a quantum mechanism changes the scaling or capability in a genuinely non-classical way, against the best classical approach and with full resource accounting? If not, where and why does it fail?

The sprint did not assume VQE, QAOA, sampling or optimisation. It was free to redesign the formulation, representation, objective and architecture. It followed oracle discipline (no free oracles, state preparation, block encodings or native indicators), required a classical adversary first, kept claim levels L0–L6 with theoretical and practical levels separate, and allowed no forced positive.

---

## 3. Starting evidence

- **Predecessor S29–S33** (9–60 aa, all simulated; imported read-only):
  - 33 CVaR-VQE-style experiments on diagonal registers of 7–171 qubits never moved the built-chain endpoint.
  - Equal-tuning simulated annealing and random prior sampling matched or beat them.
  - Twelve reduction results explain why: prefix theorem, solver equivalence, tail collapse, closed-form p*, and others.
  - Single-structure accuracy at ≤ 60 aa is information-limited.
  - One positive signal: a Boltzmann soft average beat hard tails (1.40× MDE), but as an exact enumerated sum.
  - Sources: `research/sprint29-33/`, `research/SCIENTIFIC_MEMORY.md`.
- **Literature phase** (448 verified papers):
  - Every known quantum speedup touching classical-energy protein tasks is at most quadratic, query-model and fault-tolerant.
  - Quadratic speedups fail fault-tolerant break-even (Sanders 2020; Babbush 2021).
  - The only surviving lead was sampling a learned-energy structure posterior at ≥ 60 aa, conditional on an unmeasured classical mixing bottleneck.
  - Source: `research/literature/LITERATURE_REVIEW.md`.

## 4. Literature landscape (condensed)

- **Optimisation and search** (Grover, Dürr–Høyer, QAOA, annealing, backtracking): quadratic at best on black boxes. Classically saturated or exactly solvable on protein structure. Transmission of proxy energies fails.
- **Sampling** (Szegedy/QSA walks, quantum Langevin/QRELD [A44], continuous hide-and-seek separation [A45]): quadratic, needs a warm start and a gap lower bound; the only live line after the literature phase.
- **Estimation** (amplitude estimation): quadratic in precision; biomolecular estimation is limited by bias and mixing, not variance.
- **Hamiltonian simulation of physical quantum systems:** the one family whose target is not a classical objective.
  - The nearest prior art is O'Brien et al., PRX Quantum 2022: dipolar-Hamiltonian learning on ubiquitin spin clusters, learnability tied to loss of ergodicity.
  - Zhang et al. 2025 [F34]: NMR OTOCs of small molecules interpreted on Willow, "not yet beyond classical".
  - Google's OTOC(2) beyond-classical evidence [F30] concerns random circuits.
  - Classical rebuttals: Fratus et al. 2025 (cluster methods for liquid NMR); Elsayed–Fine 2015 (classical spins); Begušić–Chan (sparse Pauli dynamics); Schuster et al. 2025 (noisy circuits are classically easy).
- **Quantum chemistry of metal cofactors** (FeMoco-class QPE): the strongest literature-supported quantum use near proteins. It is outside the structure endpoint.

## 5. Computational bottleneck map

| Bottleneck class | Status for protein structure | Quantum relevance |
|---|---|---|
| Single-structure prediction ≤ 60 aa | information-limited (S29–S33; H-002) | none: more computation does not help |
| Conformational search / decoding | classically saturated (32–64 restarts at 44–60 aa); census unsaturated at L ≥ 100 (MEASURED) | quadratic (Grover/AA) only vs i.i.d. restarts; killed (T4) |
| Posterior sampling of a learned energy | classically hard signals at L ≥ 45 (0 NRPT round trips; unsaturated census) | quadratic same-chain (T2); practical floor T*_Q ≥ 0.26–20 yr/sample (killed) |
| Rare events, committors, free energies | classical splitting/stratification polynomial | quadratic; killed (QM-12/13/15) |
| Inverse problems with physical quantum data (NMR spin dynamics) | classical forward models exact for 2-point transfer; echoes (OTOC) beyond classical approximations at N ≥ 10 (MEASURED) | **the only formulation with a measured classical-approximation failure** |
| Electronic structure of active sites | classical DMRG/CC at chemical accuracy for FeMoco-class ranking (per lens) | polynomial; outside the endpoint |

## 6. Candidate quantum mechanisms

28 unique mechanisms (from 90 lane cards) across five roles: sampler, optimiser, estimator, quantum forward model, structural invariants. Plus meta items (no-gos, costing, dequantisation). Full catalogue: `research/discovery/CANDIDATE_MECHANISMS.md`. Architecture map: `research/discovery/ARCHITECTURE_SEARCH.md`.

## 7. Classical counterarguments

Four structural reasons recur (`research/discovery/CLASSICAL_COUNTERARGUMENTS.md`):
1. **Quadratic ceiling plus a landscape-independent runtime floor** (T2, T5).
2. **White-box pair-additive energies leak their own structure.** Distance-geometry seeding, the e^{−KL} sublevel bound and assignment collapse dequantise the constructions that separations need.
3. **Fold information lives in weak couplings**, which are classically perturbative. The hard sectors carry local or degenerate information.
4. **The endpoint is information-limited**, and new information comes from experiments that already have classical interpreters.

## 8. Architectures explored

- Program A: learned-posterior sampling (λ-path NRPT, temperature exchange, mode census, transmission).
- Program B: synthetic exact-mechanism lab.
- Program C: quantum forward models for NMR, with an adversary panel, Fisher-information split, dephasing and bath embedding, a dilute amide-proton network, a shot-based quantum circuit with hardware noise, and a resource model.
- Theory T1–T6.

See `ARCHITECTURE_SEARCH.md`.

## 9. Experiments performed

Ledger: `research/experiments/README.md`. All heavy jobs ran under the CPU/RAM governor.

| ID | What | Scale |
|---|---|---|
| G1-P / M1 / M1b / M2 / Q4-M3 | NRPT pilot; 256- and 2048-restart mode census; λ-path T-scan; temperature exchange | 16 leakage-screened chains × L = 30–150 |
| R2-T | Laplace-free posterior-mixture transmission test | 16 chains × L = 60, 100 |
| C1 | NMR hardness–identifiability gate (v2) | 1UBQ 6 probes × 2 orientations × γ ∈ {0, 10³, 5×10³} s⁻¹, N = 10 (+12, 14); 1PGA replication |
| C1-HN | dilute amide-proton (perdeuterated) networks | 1PGA, 1UBQ; N = 10, 12; 1 ms window |
| C2/C3 | classical cost scaling (sparse Pauli strings) for transfer and echoes | N = 8–20 |
| R1-E | bath embedding (exact N_env = 12/14; Gaussian-bath dephasing) | 2 probes |
| Q-PoP | shot-based quantum echo circuit, depolarising noise, echo-normalisation mitigation | N = 10, 12 |
| B-SYN | exact mechanism lab | 5 landscape families, n = 6–16 |
| Theory checks | T1–T5 companion scripts | — |

## 10. Negative results

⟦NEGATIVE⟧

## 11. Positive results

⟦POSITIVE⟧

## 12. Theoretical results

- **T1 (reduction theorem).**
  - A quantum stage whose objective is dephasing-dominated and whose output is consumed via argmin / energy-order tail / convex program is output-equivalent to a classical optimiser over the simplex. This is **PROVED** (H-001a).
  - Cost equivalence is proved for explicit tabulated E. It is false in the query model for implicit black-box E (quadratic), and open for structured E.
- **T2 (sampling).**
  - QSA along the prior→posterior path gives same-chain quadratic gains, L2 (L3 with T3).
  - The Syed communication barrier is blind to first-order crossings.
  - The gap bound δ ≤ (8/p)e^{−ΔF‡}.
  - Break-even τ_* > B* = (A ρ K n_b R)².
  - **Minimum-runtime corollary: no landscape gives an advantage at a per-sample quantum wall-clock below T*_Q = Aρ(K n_b G t_T)²/c.**
- **T3 (fault-tolerant resources).** A faithful coherent walk step for the A80 energy costs G(L) ≈ 2.9–3.6×10⁴·L² Toffolis, with arithmetic dominating. Fixed-point precision needs 22–25 bits.
- **T4 (amplified mode finding).** Quadratic only against i.i.d. restarts. The hardware gate fails at 170 µs for any map evaluating the energy once, and at 1 µs under stated assumptions.
- **T5 (ceiling).**
  - At most quadratic on information-local families with an easy background.
  - Precision gains at most quadratic.
  - No universal ceiling (Simon-trail counterexample).
  - Escape routes enumerated.
- **T6 (mechanism).** Coefficient-truncated classical dynamics reproduces NMR transfer (one coefficient; operator hydrodynamics) but not echoes, which read the anticommuting weight of the whole operator, including its high-weight tail.
- **No-go notes from the attack:** BCGL fixed-node dominance (QM-08), barrier-exponential conservation in QLSA committors (QM-13), arity collapse of Kikuchi on pairwise protein data (QM-17), and assignment collapse of restraint posteriors (QM-18).

## 13. Scaling results

⟦SCALING⟧

## 14. Resource estimates

- **Sampling family** (BREAK_EVEN §1, T2/T3): B* = 10¹⁰ (every optimistic assumption stacked) to 10²² (cited constants). T*_Q ≥ 0.26 yr (Cartesian target, 1 µs Toffolis), 1–20 yr (A80 target), 10⁵–10⁷ yr (central). One-day samples need Toffoli times of 12–100 ns (optimistic) or sub-ns (central).
- **Amplified multistart:** p* ≤ 10⁻¹¹ vs measured p_hit ≈ 10⁻².
- **NMR forward model** (`research/theory/nmr_resource_model.py`):
  - One fault-tolerant echo evaluation (16 times × 4 observables, amplitude estimation to 3×10⁻³) costs 2.5×10¹¹ T (N = 14) to 9.6×10¹² T (N = 466). That is 3 d – 111 d serial at 1 µs/T, or ~11 h depth-limited with unlimited factories.
  - An inversion with 10³ gradient evaluations takes ~11 years per machine at 1 µs T-layers.
  - NISQ needs 3×10⁴–3×10⁵ two-qubit gates, so fidelity is e^{−32} to e^{−270} at 10⁻³ error.

## 15. Hardware analysis

⟦HARDWARE⟧

## 16. Adversarial results

⟦ADVERSARIAL⟧

## 17. Novelty analysis

- **NM-1 (Program C).** The idea of quantum-simulating protein ¹H dipolar dynamics to learn structure, and the qualitative hardness–learnability tension, are **anticipated by O'Brien et al. (PRX Quantum 3, 030345, 2022)**. Hardware precedent for small molecules: Zhang et al. 2025 [F34].
- Under the stated search scope (arXiv API, the 448-paper bibliography; general web search was exhausted), the search found no evidence of a study that:
  - (a) benchmarks site-resolved protein ¹H echoes (OTOC) against a best-classical adversary panel;
  - (b) splits the structural Fisher information by classical failure time;
  - (c) shows that transfer is classically reproducible while echoes are not.

  These are incremental, quantitative contributions, not a new mechanism.
- **Sampling-family results** are instantiations of known quadratic-speedup obstructions (Sanders/Babbush) for a learned protein energy. New elements, within the search scope: the landscape-independent T*_Q statement, the first landscape characterisation of an LM-derived distogram posterior, and the white-box dequantisation arguments (NM-2, NM-9).
- Open memos NM-2 … NM-15: `research/discovery/NOVELTY_MEMOS.md`.

## 18. Remaining uncertainties

⟦UNCERTAINTIES⟧

## 19. Best candidate

⟦BEST⟧

## 20. Strongest classical explanation

⟦CLASSICAL-EXPLANATION⟧

## 21. Final claim level

⟦CLAIM-LEVEL⟧

## 22. Publication strategy

⟦PUBLICATION⟧

## 23. Next experiment

⟦NEXT⟧

## 24. Final sprint decision (the 17 questions)

⟦DECISION⟧

## 25. Reproducibility commands

```bash
pip install -e .[dev]                       # repo root; Python 3.13, CPU only
python -m qapf.governor /dev/null --log research/results/RAW/master/governor.jsonl --max-workers 5 \
    --spool research/results/RAW/master/spool.jsonl --forever --stop-file research/results/RAW/master/STOP
# G1 (learned posterior; needs data/instruments/ladder/*.npz from src/qapf/protein/targets.py and the vendored model)
python scripts/g1_mode_census.py --crop 5O37A_100 --restarts 256
python scripts/g1_sample_crop.py --crop 5O37A_45 --T 1 --scans 100000 --time-budget 1500 --pivot 4
python scripts/tpt_crop.py --crop 5O37A_60 --rungs 24 --tmax 40 --budget 750
python scripts/g1_transmission.py --crop 5O37A_60 --restarts 64
python scripts/analyze_g1.py; python scripts/analyze_transmission.py
# Program C (NMR)
python scripts/nmr_gate.py --pdb 1UBQ --probe 19 --N 10 --gamma 0 --exact sector          # C1 (v2)
python scripts/nmr_gate.py --pdb 1PGA --probe 325 --N 10 --hn-only 1 --dt 5e-6 --steps 200 --out research/results/RAW/nmr_gate_hn
python scripts/nmr_sparse_scaling.py --probe 19 --N 12 --gamma 0                          # C2/C3
python scripts/nmr_embed.py --probe 245 --Ncore 10 --envs 12,14                           # R1-E
python scripts/nmr_circuit_pop.py --probe 19 --N 10                                      # quantum proof-of-principle
python scripts/analyze_nmr2.py research/results/RAW/nmr_gate; python scripts/analyze_c2.py
python research/theory/nmr_resource_model.py
python scripts/synthetic_lab.py --family golf --nmax 16
python scripts/make_figures.py
# theory checks
python research/theory/PROOFS/T1_reduction_checks.py; python research/theory/PROOFS/T2_sampling_checks.py
python research/theory/PROOFS/T4_amplified_checks.py; python research/theory/T3_resource_model.py
```

## 26. Git checkpoint

⟦GIT⟧
