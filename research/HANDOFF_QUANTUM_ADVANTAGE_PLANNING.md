# Handoff: quantum-advantage topic search, carried into a new repo

_Written 2026-09-28. This is a self-contained summary for a new repository that will plan quantum-advantage research in a more organised way. Everything cited here lives in this repo (github.com/abe-narayan/quantum-advantage-protein-folding, `main`, commit 9e0ca50 or later)._

## 1. What is finished

| Work | Outcome | Where |
|---|---|---|
| Protein-structure quantum-advantage program (four rounds) | **Negative in every regime examined**; no claim in categories 1–6 survives | `reports/QUANTUM_ADVANTAGE_DISCOVERY_REPORT.md`, `reports/QUANTUM_ADVANTAGE_CLAIM_AUDIT.md`, `research/KILLBOOK.md` (K-101 to K-120) |
| Next-topics scan (7 topics, then a top 10) | Best candidates rated 3/5 at most | `research/NEXT_TOPICS.md` |
| Deep search for an original advantage (4 lenses plus a red team) | Nothing both likely and undiscovered | `research/NOVEL_ADVANTAGE_SEARCH.md` |
| Top-3 search (45 agents, 2 rounds, about 80 problems) | **1 conditional finalist, not 3** | `research/reports/TOP3_QUANTUM_ADVANTAGE_CANDIDATES.md`, `research/reports/LITERATURE_SEARCH_AUDIT.md`, notes in `research/reports/lit_work/` |
| Research and publication plan for the finalist | Written as a Claude Doc (private until shared) | https://claude.ai/code/artifact/32195920-5170-4a1b-94bb-c50cd798e5bc |

## 2. Filters that every candidate must pass

These come from the protein failure and the topic searches. Apply them before spending any compute.

1. **L1. A genuinely quantum object.** Correlated electrons or quantum dynamics, not a classical energy landscape. Quantum search or sampling over a classical objective is at most quadratic and dies on fault-tolerant overhead (Babbush et al. 2021, arXiv:2011.04149).
2. **L2/L7. Hardness shown by more than one classical family.** Test against the strongest classical methods (tensor networks, QMC/AFQMC, neural quantum states, Pauli propagation, NEGF, cluster expansions, CCSD(T)/DMRG). If only one method family fails, that is not a wall. Weak baselines manufacture hardness.
3. **L5. Information, not just computation.** The hard regime must carry information that changes a decision. For every audited candidate, the classical wall and the decision-relevant information turned out to lie in different regimes.
4. **L6. Model floor below solver spread.** An exact solution of an uncertain model (fitted parameters, active space, phonons, environment) is worthless.
5. **Cost.** Sampling and state preparation, not Hamiltonian simulation, dominated every cost. Screen for S·G ≲ 1e12–1e13 Toffoli per useful data point. Simulator runtime is never quantum runtime.
6. **Novelty.** Classify it A–F:
   - A: no quantum paper
   - B: quantum work exists nearby
   - C: quantum methods exist, but no advantage study
   - D: an advantage claimed only against weak classical methods
   - E: an advantage claimed, then dequantized
   - F: an advantage established

   Negative literature claims must be scoped to the sources searched.
7. **Claim category.** Name one: (1) quantum usefulness, (2) empirical advantage, (3) computational/resource advantage, (4) sampling advantage, (5) hardware advantage, (6) provable advantage.

**The central tension.** Originality and a high likelihood of advantage pull against each other. A problem that is clearly quantum-hard and clearly useful has usually already been costed by a large group (Google, Sandia, Xanadu, PsiQuantum). What remains open is usually open because the advantage is doubtful.

## 3. Candidate status

**Finalist C01 (conditional).** The correlated thermal electronic dynamic structure factor S_ee(q,ω) of warm dense hydrogen (r_s ≈ 2, θ = 0.25–0.5), for X-ray Thomson scattering.
- Novelty B. The claim target is category 3, accuracy class only.
- Gates:
  1. K-C01a, an information test on a laptop;
  2. K-C01b, a multi-family classical wall at about 1e4 core-hours;
  3. bounded-cost thermal-state preparation;
  4. a resource recheck.
- Cost: 4e13–9e14 Toffoli for the validation proxy; 7e16–1.6e18 for hydrogen.
- **High scoop risk:** Sandia has announced WDM linear-response work (arXiv:2605.22920, verified quote). The user judged this risky.

**Low-competition originals (scoped novelty A/B, lower odds).**
- C19: quantum thermal gradient descent into protocol-dependent metastable states of disordered magnets. This is the most original mechanism, but no physical instance with hard minima is known.
- C44: dense electron–hole plasma in 2D semiconductors. No quantum paper exists, but GW-NEGF matches experiment.
- C28: impact ionization in Mott-insulator photovoltaics. It carries a model-floor risk.
- C17: thermal Hall conductivity of Kitaev magnets. Phonons dominate the measured signal.

**Closest miss in round 2.** N01, the fractional Chern insulator in hBN-aligned rhombohedral graphene. The question is answered classically at 21 sites (arXiv:2608.12452), and parameter uncertainty exceeds the solver spread.

**The original route with the lowest scoop risk.** A "classical wall map" of published quantum resource estimates that were never benchmarked against the strongest classical methods:
- organic photovoltaics (arXiv:2411.13669, with the MPS vs ML-MCTDH crack in doi:10.1021/acs.jctc.4c00751);
- Anderson–Newns metal-surface dynamics (arXiv:2601.16264);
- EUV photoemission (arXiv:2602.20234);
- Pd-zeolite (arXiv:2512.19778).

This route is publishable either way and runs on a laptop or small cluster. The trade-off is that it tests other people's claims rather than discovering a new advantage.

## 4. Open decision for the next repo

Choose among:
- (a) a low-competition original with lower odds;
- (b) C01, in collaboration with Sandia or the Dornheim group rather than racing them;
- (c) the classical-wall map;
- (d) a focused search restricted to scoped-novelty-A problems, with an explicit competitor check (group pages, grants, talks) for each.

## 5. Practical notes

- Compute: 8 logical CPUs and about 15.6 GB RAM. The host kills background shells under memory pressure. Use 3 workers or fewer, checkpoint every job, and never delete results when memory is low.
- The general web-search budget ran out during these searches. Use the arXiv API and abstract pages, OpenAlex, Crossref and OSTI, and space out calls (HTTP 429 is common). Close the coverage gaps with general web search before any submission.
