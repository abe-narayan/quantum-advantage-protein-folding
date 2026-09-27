# Novelty memos

_Discovery sprint, 2026-09-27. Each memo gives: the claim whose novelty is at stake, the search performed (scope, dates, tools), the nearest prior art found, what is and is not new, and the verdict. Wording rule: "the literature search found no evidence of X under scope Y". It never says "X has never been done". The literature-phase bibliography is `research/literature/BIBLIOGRAPHY.md`; keys like [F34] refer to it._

**Search budget disclosure.** The session's WebSearch budget (200 calls) was exhausted before this memo was written. Searches below used the arXiv API (export.arxiv.org, via WebFetch) and the literature-phase records. They are narrower than a full web search, and each memo states that limit.

---

## NM-1 · Program C (QM-19/20/21): protein ¹H dipolar spin dynamics as a quantum forward model for structure, with a hardness–identifiability gate

**Claim at stake.** Structural (geometric) information in protein ¹H many-body spin dynamics lies in the part of the dynamics that the best classical approximation cannot reproduce. A quantum simulator of the forward model would therefore extract structure that a classical inversion cannot.

**Search.**
- arXiv API, 2026-09-27: title/abstract searches for NMR ∧ quantum ∧ (structure ∨ classically ∨ simulate); "Pauli propagation" ∧ spin; NMR ∧ "quantum advantage"; protein ∧ (spin diffusion ∨ dipolar) ∧ "quantum computer"; titles "classical spin simulations", "Digital quantum simulation of NMR", "spinDMFT".
- The literature-phase F-domain notes (`research/literature/domain_notes/lit_F_claims.md`), which cover OTOC/echoes and the NMR geometry demo.
- No general web search (budget exhausted).

**Nearest prior art (verified on arXiv).**

| Work | What it does | Relation |
|---|---|---|
| O'Brien, Ioffe, Su, Fushman, Neven, Babbush, Smelyanskiy, *PRX Quantum* 3, 030345 (2022), arXiv:2109.02163 | Quantum algorithm to learn the anisotropic dipolar Hamiltonian from time-resolved spin–spin correlators. Case study: **ubiquitin (1D3Z) in a membrane/oriented setting**, spin clusters of 8 and 60 of the ~600 protons. **Finds that learnability (Hessian rank) appears only as the dynamics become non-ergodic**, i.e. when dipolar couplings are suppressed. Gives NISQ and fault-tolerant cost scalings. | **Anticipates the core idea of QM-19/21**: same protein, same Hamiltonian, same "hard dynamics vs learnability" question. Its answer (ergodic → degenerate) is the hardness–identifiability trade-off in qualitative form. It does not test any classical approximation method. |
| C. Zhang, Cortiñas, Karamlou et al. (Google Quantum AI), arXiv:2510.19550 (2025) [F34] | OTOCs measured by NMR on small molecules in a liquid crystal, interpreted by simulation on the Willow processor; an H–H distance and a dihedral are recovered. Self-declared "not yet beyond classical". | Hardware demonstration of the pipeline QM-20 proposes, for small molecules. |
| Google Quantum AI, OTOC(2) "quantum echoes", Nature (2025) [F30]; Bermejo et al. arXiv:2604.15427 [F31] | Beyond-classical OTOC(2) on 2D random circuits; tensor-network/BP simulation argued infeasible. | Hardness evidence for echoes on random circuits, not dipolar protein networks. |
| Seetharam, …, Demler, Sels, *Sci. Adv.* 9 (2023), arXiv:2109.13298 | NMR spectra (ZULF) simulated on trapped ions; structure-extraction motivation. | Same application family (small molecules). |
| Fratus, Enenkel, Zanker, Reiner, Marthaler, Schmitteckert, arXiv:2508.06448 (v3 2026) | Classical cluster approximation (linear in spin number) reproduces liquid-state NMR spectra "throughout, and even somewhat beyond" typical regimes. | **Classical rebuttal for liquid-state NMR.** It does not cover strongly coupled static/oriented dipolar networks. |
| Walch et al., arXiv:2609.20406 (2026) | Shot-noise cost of quantum computation of NMR spectra. | Resource side. |
| Elsayed & Fine, *PRB* 91, 094424 (2015), arXiv:1409.8564; Navez, Starkov & Fine arXiv:1812.02155 | Classical-spin simulations reproduce NMR free-induction decays of quantum spin lattices quantitatively in many regimes; a two-spin quantum correction extends them. | **Classical adversary** for bulk dipolar dynamics. Implemented here as `classical_spin_correlators`. The two-spin-corrected version is **not** implemented (open adversary). |
| Begušić & Chan arXiv:2306.16372; Begušić, Gray & Chan *Sci. Adv.* 10 (2024) [F20, F21] | Sparse Pauli dynamics reproduced IBM's 127-qubit "utility" dynamics. | **Classical adversary**; implemented here as coefficient-threshold Pauli propagation. |

**What this program adds (if results support it).**
1. A **best-classical adversary panel** on the protein ¹H network: weight-truncated Pauli, sparse Pauli dynamics, sub-cluster exact (CCE-like), and classical-spin dynamics. The panel defines a classical-failure time t_c*. O'Brien et al. did not test classical approximations.
2. A **quantitative split of the Fisher information**, per parameter and as a full matrix, into the classically reproducible window (t < t_c*) and the hard window. The gain spectrum g = max_v v'F_total v / v'F_easy v measures how many repetitions a quantum forward model saves.
3. **Dephasing sweeps** (γ = 0, 1000, 5000 s⁻¹) and **cluster-size scaling** (N = 10, 12, 14) under a pre-registered kill rule (`research/experiments/PREREGISTERED/PREREG_G1_C1_Q4.md`, C1).

**What is NOT new.**
- The application (quantum simulation of NMR to learn protein/molecular geometry) [O'Brien 2022; F34; Seetharam 2023].
- The qualitative trade-off that ergodic, classically hard dynamics are poorly learnable [O'Brien 2022].
- The adversaries themselves [Elsayed–Fine; Begušić–Chan; cluster methods, Fratus 2025].

**Verdict.** Under the scope above, the literature search found no evidence of a study that measures, for protein ¹H dipolar networks, how much structural Fisher information lies beyond the failure time of the best classical approximation. It also found none that tests the O'Brien trade-off against an explicit classical-adversary panel. The contribution is at most an **incremental, quantitative extension of O'Brien et al. (2022)**, not a new mechanism. Any claim must cite O'Brien 2022 as the origin of the idea.

_Outcome of the experiment: see §C1 of the discovery report. This memo is not updated with results._
