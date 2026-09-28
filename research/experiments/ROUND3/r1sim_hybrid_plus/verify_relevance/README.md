# Relevance and novelty verification of lane `r1sim_hybrid_plus`

_2026-09-28. Adversarial verifier (relevance). Claim under attack: "No polynomial-cost classical approximation reproduces
the exact first-order dipolar echo OTOC(1) of the 1UBQ ¹H cones within σ = 0.01 over 80–320 µs on both probes at
N = 16 and 18 … supports approximation-hardness only." The lane's verdict was SUPPORTS._

## Verdict: REFUTED on relevance

The lane's measured numbers hold up. I replicated two of them with a fresh seed. The claim still fails the relevance test
on four independent counts:

1. It does not bear on protein structure.
2. It cannot decide the R1-SIM question it is filed under.
3. The precision it demands is finer than the physical accuracy of the model it reproduces.
4. Its mechanisms and the physics behind it are already in the literature.

Under the lane rules, a claim that is irrelevant, or that reduces to a kill, defaults to refuted. Here it reduces to the
residue of K-105.

## 1. It does not bear on protein structure [DERIVED from KILLBOOK K-105, R1_SYNTHESIS §2 and §5]

**R1 was killed on grounds unrelated to how hard the simulation is.**
- Reversal horizon: the informative window is at 4.8–25 T2, but T3 ≈ 4–6.7 T2.
- Value: the gain is about 1.1–1.5.
- Cost: fault-tolerant break-even needs N_eff of 30–47.

The value kill holds even with perfect reversal.

**A revival needs all four conditions at once.** These are listed in R1_SYNTHESIS §5:
- (i) a *measured* converged σ-cone of more than 47 spins;
- (ii) a protein reversal horizon;
- (iii) a structural degree of freedom that classical data leave undetermined, with a gain of at least 10;
- (iv) a forward model accurate to σ.

The lane meets none of them. It measures nothing above N = 18, uses no reversal or structural information, and uses the
same idealised forward model.

**What is left is a category-3 physics-simulation question at best.** The lane says so itself.

## 2. It cannot decide R1-SIM [DERIVED]

R1-SIM asks whether the converged echo light cone exceeds *exact* classical reach. At N = 16–18 exact simulation
reaches the whole system, in 10 min to 3 h.

The lane could only ever have changed the state of R1-SIM in one direction: a cheap approximation succeeding would have
been a kill route. That kill did not fire, and that is only the absence of a kill. It is not evidence for R1-SIM.

The lane's own "Next tests" item 4 says the approximation route cannot settle R1-SIM. **A verdict of SUPPORTS therefore
overstates what the lane found.**

## 3. The required precision is finer than the model's own physical accuracy

Script: `relevance_scale.py`. Output: `relevance_scale.json`. It is pure post-processing of the lane's `summary.json`
and the exact typicality cones, and runs in under 1 s. [MEASURED]

| Case | Lane best error | Model's finite-N error: max \|F_N − F_(N−2)\| | Ratio (lane / finite-N) |
|---|---|---|---|
| p19 N14 | 0.036 | 0.186 | 0.19 |
| p19 N16 | 0.029 (λ-calibrated) | 0.139 | 0.21 |
| p245 N16 | 0.091 | 0.132 | 0.69 |
| p19 N18 | 0.275 | 0.037 | 7.4 |
| p245 N18 | 0.081 | 0.057 | 1.4 |

**The physical-model error is 5–66σ (0.05–0.66).** At N = 10, the isolated, static, offset-free Hamiltonian used for the
reference is off by that much once methyl rotation (7–49σ) and 1 kHz site offsets (5–66σ) are included
(`ADVERSARIAL/R1_physics_feasibility/README.md`). [MEASURED by that lens]

**At N = 14 and 16, the best approximation of the N-spin model is closer to that model than the exact (N−2)-spin model
is.** On the lane's own data, the σ = 0.01 target asks for agreement with a truncated, idealised model to a precision:
- 13–19× finer than that model's own finite-N truncation at N ≤ 16;
- 5–66× finer than its distance from a physical protein sample.

[INFERENCE] Being hard at that precision says nothing about the real protein echo.

**N = 20 checkpoint.** Only t ≤ 40 µs is complete, where |F20 − F18| ≤ 0.0014. There is no data inside the window yet,
so this is no evidence either way. [MEASURED]

## 4. Novelty

Each item below was checked against its arXiv abstract through the export API or arxiv.org/abs. Item (e) was also
checked against the PDF text.

**(a) The strongest named family was designed for a different observable.**
- Starkov–Fine coupled quantum clusters, PRB 101, 024428 (2020), arXiv:1911.00990.
- The abstract is about free induction decays (two-point functions) only. It does not mention OTOCs or echoes.
- Its failure on an OTOC is therefore expected. It is not a strong adversary, and the lane's mechanism 1 (the sqrt(D+1)
  amplification collapses the echo) restates this mismatch. [LITERATURE-SUPPORTED]

**(b) Classical-spin baths were already known to fail for echoes.**
- Fine, Elsayed, Kropf & de Wijn, PRE 89, 012923 (2014), arXiv:1305.2817: spin-½ lattices lack the exponential
  sensitivity of classical spins.
- Classical-spin and mean-field baths are therefore known to misrepresent echo sensitivity. The lane's mechanisms 1 and 5
  (a chaotic classical bath, and non-convergent CCE on a classical base) are consistent with this known result.
  [LITERATURE-SUPPORTED; applying it to this model is INFERENCE]

**(c) Semiclassical echoes of this kind have been studied before.**
- Schmitt, Sels, Kehrein & Polkovnikov, PRB 99, 134301 (2019), arXiv:1802.06796: semiclassical echo dynamics are tied to
  the growth of OTOC-type double commutators. Echoes in semiclassical and TWA-type methods are an existing topic.
- The lane did not test cluster truncated Wigner, which it notes itself. [LITERATURE-SUPPORTED]

**(d) Operator spreading has an efficient classical model.**
- Mi et al., Science 374, 1479 (2021), arXiv:2101.08870: "operator spreading is captured by an efficient classical
  model". Operator entanglement, the interference fluctuations, is what needs exponential resources.
- The beyond-classical echo result, arXiv:2506.10191, concerns OTOC(2), not OTOC(1). [LITERATURE-SUPPORTED]

**(e) Dense dipolar ¹H echoes already involve far more spins than exact simulation can reach.**
- Álvarez, Suter & Kaiser, Science 349, 846 (2015), arXiv:1409.4562.
  - The PDF text reports NMR control of "up to ∼7000" coherently correlated spins in polycrystalline adamantane ¹H.
  - Cluster size K(t) grows without bound in the unperturbed case.
- Sánchez et al., PRL 124, 030601 (2020), arXiv:1902.06628: OTOCs probe scrambling across "hundreds of spins".
- Gärttner, Hauke & Rey, PRL 120, 040402 (2018), arXiv:1706.01616: multiple-quantum-coherence spectra are a family of
  OTOCs.
- So the bigger R1-SIM question, whether a dense dipolar echo cone exceeds exact classical reach, is already answered
  yes for generic dense ¹H solids at their experimental timescales. [LITERATURE-SUPPORTED]
- Whether it happens by 80–320 µs in proteins is an INFERENCE by coupling-strength scaling that has not been checked.
- Even a positive answer would be a generic fact about dipolar solids, not a result specific to proteins or to structure.

**(f) The echo-for-structure framing has prior art.**
- Zhang et al. (Google), arXiv:2510.19550 (2025), "Quantum computation of molecular geometry via many-body nuclear spin
  echoes".
- It learns structure from OTOCs on small molecules, citing an "apparent exponential classical cost". It makes no
  rigorous hardness claim. [LITERATURE-SUPPORTED]

## 5. Wording defects in the claim

**"No polynomial-cost classical approximation" is a universal claim that the evidence does not cover.**
- Only 4 families and 4 zero-compute adversaries were tested.
- These were not tested at N = 16–18: cluster truncated Wigner, DAOE, neural quantum states, MPO/tensor networks, and
  sparse Pauli near the full symmetric operator space (the method that reproduced N = 10 in the R1 synthesis).
- At fixed N = 16–18, "polynomial cost" is undefined: every method, exact simulation included, is O(1).

**"Errors do not shrink with polynomial method order" is partly contradicted by the lane's own ladder.**
- The CQC cluster size k is both the method order and the core size. Going from k = 4 to k = 6 cuts the error from 0.54
  to 0.24 (p19) and from 0.57 to 0.28 (p245).
- At N = 16, k = 10–12 is 62–75% of the system. So the claimed split between the "polynomial-order ladder" and the
  "exact-core ladder" cannot be observed at these sizes.
- **The data contain no information about scaling.** [MEASURED from lane data; conclusion is INFERENCE]

## 6. Replication

Script: `seed_replay.py`. Output: `seed_replay.json`. It imports the lane's `cqc_echo.py` unchanged, with seed 101
(the lane used seed 7) and M = 48. [MEASURED]

| Run | Replication error | Lane error | Time |
|---|---|---|---|
| p19 N16, kl6/none | 0.208 | 0.239 | 5.2 s |
| p245 N16, kl6/none | 0.313 | 0.282 | 5.7 s |

Both agree within the sample SE of 0.02–0.04. The measured numbers are sound. The refutation concerns relevance and
novelty, not the data.

## Claim levels

**Protein-structure relevance: L0, at both theoretical and practical level.**

**As physics:** L1 (narrow, empirical) at most. The failure of these specific families on a truncated, idealised model is
expected from the literature above.

**Practical: L0.** Exact simulation covers N = 16–18.

## Compute

Single-threaded (OMP/MKL/OPENBLAS = 1), about 12 CPU-s in total, peak RAM under 0.3 GB. No files were modified outside this
folder.
