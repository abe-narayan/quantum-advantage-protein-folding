# Relevance and novelty verification of ROUND3/r1sim_exact_reach

_2026-09-28. Adversarial verifier, relevance lens. The claim under attack: exact classical simulation cannot reach the
converged late-window (≈ 240–320 µs) first-order dipolar echo F_ab(t) of the dense 1UBQ ¹H network at the instrument
sites. It is framed as category-3 physics simulation that does not revive R1 (K-105)._

Tags: **MEASURED** (file in this folder or a cited file), **DERIVED**, **LITERATURE** (arXiv abstract fetched this
session through export.arxiv.org), **LITERATURE-REPO** (verified by an earlier lens, not re-fetched here),
**INFERENCE**, **UNPROVEN**.

## Verdict: REFUTED on relevance and novelty

The lane's numbers are not disputed here: the faster exact code, the N = 20 non-convergence and the frontier table.
What is refuted is that the finding matters for this program or is new:

1. It has no bearing on protein structure. By construction it concerns a time window that cannot be observed.
2. Its core statement ("exact state-vector simulation of a dense dipolar ¹H network runs out at ~30–48 spins") is
   standard and already in the literature, including for ubiquitin itself.
3. It is not an advantage claim in any charter category: there is no quantum cost and no best-classical comparator.
4. The pre-registered outcome is INCONCLUSIVE, not SUPPORT.
5. About half of the late-window drift that pushes N_σ beyond exact reach sits in a b-independent two-point term (the
   K-104 class) plus a finite-cluster artefact. The reduction is partial, not complete (§3).

Levels:

| | this verifier | lane's own |
|---|---|---|
| theoretical | **L0** | L0–L1 |
| practical | **L0** | L0–L1 |

## 1. Relevance to protein structure: none

### 1.1 The lane itself concedes it (K-105)

- The claim is scoped as category 3 and "does not revive R1 (K-105)".
- The four K-105 revival conditions (`R1_SYNTHESIS.md` §5) must all hold at once:

  | condition | requirement | status here |
  |---|---|---|
  | (i) scale | a **measured, not extrapolated** converged σ-cone above 47–51 spins | not met: the lane measures N ≤ 20; "≥ 58" is INFERENCE from 4–5 points with shell events |
  | (ii) reversibility | the echo window must fall inside the reversal horizon | fails (§1.2) |
  | (iii) value | profiled gain g ≥ 10 | not addressed; K-105 median gain is 1.1–1.5 |
  | (iv) accuracy | forward model accurate to σ | not addressed; model error is 5–66σ from 40–50 µs (methyl rotation, offsets) |

### 1.2 The claim's window is far beyond the physical reversal horizon (DERIVED from MEASURED T2 + LITERATURE-REPO envelope)

Inputs:
- T2 = 1/√M2 from `ADVERSARIAL/R1_physics_feasibility/scales.json`, for the 1UBQ dense jobs;
- the Loschmidt-echo envelope with T3 = 6.7 T2 and a 1.7 T2 tail (Sánchez, Chattah & Pastawski, PRA 105, 052232),
  using the form in `reversal_envelope.py`;
- forward time only, which is generous.

Output: `relevance_decomp.json → reversal`.

| T2 normalisation | T3 (µs) | 160 µs | 240 µs | 320 µs |
|---|---|---|---|---|
| isolated cluster, 14–18 µs (most generous) | 94–123 | 8.7–11 T2; A = 0.23 | 13–17 T2; A = **2.3e-2** | 17–23 T2; A = **1.8e-3** |
| whole network, rotor-averaged, 9.8 µs | 66 | 16 T2; A = 3.5e-3 | 24 T2; A = 3e-5 | 33 T2; A = 2.5e-7 |
| whole network, static, 8.0–8.1 µs | 54 | 20 T2; A = 4.5e-4 | 30 T2; A = 1.4e-6 | 40 T2; A = 4e-9 |

**Observable echo amplitude A·F_{N=20}(t) against σ = 0.01** (MEASURED F × envelope; `observable_amplitude`):
- **At 320 µs it is 0.03–0.13σ** under the most generous normalisation, and effectively 0 under the network ones.
  This holds on both probes and at every instrument site.
- At 240 µs, with A ≤ 0.023 and F ≈ 0.2–0.3, it is below σ even in the most generous case.
- At 160 µs, with the cluster normalisation only, it is 5–19σ. With the network normalisations it is 0.01–0.29σ.

**Consequence (INFERENCE; carries over K-105's caveat that T3/T2 comes from model solids, not from a protein).** The
"converged late-window echo" is a quantity of an idealised model: isolated, static, offset-free, perfectly reversed.
No protein experiment can supply it at σ. A quantum computer that computed it would therefore produce no structural
information: there is no data to invert, and no data against which to validate the forward model.
- The physically accessible part of the echo (t ≲ T3 ≈ 54–123 µs) has a measured σ-cone of 16–20 spins at 40 µs
  (`R1_theory_hardness` §2.4, MEASURED). That is inside exact reach.
- The lane's own "early window within exact reach for p19" (≤ 160 µs, N ≈ 20–24) covers most of what is observable
  even under the generous normalisation.

### 1.3 The isolated-molecule limit is not the physical limit (INFERENCE)

- The claim defines "converged" as nested clusters of one ubiquitin molecule (629 ¹H).
- A microcrystal, powder or membrane sample continues the network across molecules (`R1_theory_hardness` §2.5).
- Methyl rotation and site offsets move the model echo by 5–66σ from 40–50 µs onward (`R1_physics_feasibility`).

So the target is converged in a model that is already known to be wrong beyond σ, in the same window.

## 2. Novelty against the literature

| statement in the claim | prior art | tag |
|---|---|---|
| Exact classical simulation cannot handle the many-spin dynamics of dense dipolar nuclear-spin solids | Gräßer, Uhrig & Ernst, arXiv:2512.15572: "generically many spins are involved in the time evolution, so that exact brute force calculations are impossible". The spinDMFT line (2107.07821, 2403.10465) was built for exactly this reason. | LITERATURE |
| Protein (ubiquitin) NMR dipolar correlator dynamics are hard to simulate classically, which motivates a quantum forward model | O'Brien, Ioffe, Su, Fushman, Neven, Babbush & Smelyanskiy, arXiv:2109.02163 (PRX Quantum 2022): the dipolar dynamics are "challenging-to-classically-simulate"; "a protein (ubiquitin) confined in a membrane" is the benchmark; proposed as "an early beyond-classical quantum application" | LITERATURE |
| NMR OTOC interpretation has an exponential classical cost that a quantum processor can take over | Zhang et al. (Google Quantum AI), arXiv:2510.19550: "to ameliorate the apparent exponential classical cost of interpreting the above OTOC data, we simulate the molecular OTOCs on a Willow … processor" | LITERATURE |
| Late-time OTOC plateaus scale as 1/N or 1/n_diff through the conserved charge (lane item 6, "DERIVED") | Diffusive OTOC tails with U(1): Khemani, Vishwanath & Huse, 1710.09835; Rakovszky, Pollmann & von Keyserlingk, 1710.09827 (`R1_theory_hardness` L15). The in-repo decomposition W = Σ_j S_aj Z_j + O_nc with C(t) = Σ_j S_aj² (§3.4c) contains the lane's 1/N term as its equilibrium limit. | LITERATURE-REPO; in-repo prior |
| Exact state-vector frontier of 45–48 qubits | Häner & Steiger 1704.01127; De Raedt et al. 1805.04708 (the lane cites both) | LITERATURE (lane) |
| Classical adversaries exist for dense dipolar echoes and OTOCs | spinDMFT reproduces the adamantane Hahn echo "excellently … without further fitting" (2403.10465) and spin diffusion in static solids (2512.15572). Starkov & Fine's hybrid quantum-classical method (1806.09355) is the lane's untested adversary. Scramblon theory describes a macroscopic NMR OTOC and is used to mitigate reversal errors (Li et al., 2506.19915). | LITERATURE |

**What is new (MEASURED, lane):**
- an 18× faster exact implementation on the reference circuit;
- two N = 20 points per probe;
- an instance-level frontier table.

These are engineering and instance data. None of them is a new mechanism, observable, algorithm or separation.

**Scope correction.** "OTOC(1) is classically hard" remains unsupported:
- the beyond-classical echo evidence in the literature is for OTOC(2) (2506.10191);
- for OTOC(1), operator spreading "is captured by an efficient classical model" (Mi et al., 2101.08870)
  (LITERATURE-REPO, `R1_theory_hardness` L12–L13).

## 3. Reduction to killed mechanisms: which part of the late drift is K-104-class? (MEASURED)

**Identity (DERIVED; also in the sibling `verify_classical` and in `R1_theory_hardness` §3.4c).**

  W = Z_a(t) = Σ_j G_j Z_j + W_rest, with G_j = Tr[W Z_j]/2^N.

Because Tr[Z_j W_rest] = 0 and [Z_j, Z_b] = 0:

  F_ab = H + R_ab, with H = Σ_j G_j² (**b-independent, two-point transfer only**).

We also separate the finite-cluster sector floor (→ 0 as N → ∞) from R.

**Data.**
- F ladders are the lane's (N = 12–18 governor reference, N = 20 lane).
- H and floor are read from the sibling's `verify_classical/runs` (same circuit, independent random vectors).
- I ran no new dynamics.
- Script: `relevance_decomp.py`; output: `relevance_decomp.json → decomposition, step_shares`.

Last ladder step N = 18 → 20:

| probe, t | site | dF | dH | dfloor | dX = dF − dH − dfloor |
|---|---|---|---|---|---|
| p19, 320 µs | 1 | −0.011 | −0.0087 | −0.0031 | **+0.001** |
| | 7 | −0.012 | −0.0087 | −0.0031 | **+0.000** |
| | 8 | −0.026 | −0.0087 | −0.0031 | −0.014 |
| | 9 | −0.024 | −0.0087 | −0.0031 | −0.012 |
| p19, 160 µs | 1–9 | −0.013 … +0.000 | −0.0067 | −0.0031 | −0.003 … +0.010 |
| p245, 160 µs | 8 / 9 | −0.028 / −0.038 | −0.0073 | −0.0035 | −0.017 / **−0.027** |

Reading:
- **The steady, monotone part of the late drift is the two-point purity H plus the floor**: about 0.010–0.012 per
  step (1.0–1.2σ) at every site. It is b-independent.
  - Its infinite-N limit H_∞(t) = Σ_j S_aj(t)² is a transfer (spin-diffusion) quantity. That class is classically
    compressible (K-104: sparse Pauli is exact for transfer at N = 10), and spin diffusion in static solids is
    simulated by spinDMFT (2512.15572).
  - The floor is a pure finite-cluster artefact.
  - This piece therefore cannot put the converged echo beyond classical reach. It only puts it beyond *exact* reach.
- At p19 sites 1 and 7 (320 µs), this accounts for **all** of the N = 18 → 20 drift (|dX| ≤ 0.001).
- **Residual, not reducible (MEASURED).** Site-specific non-two-point steps remain:
  - 1.2–1.4σ at p19 sites 8 and 9 (320 µs);
  - up to 2.7σ at p245 site 9 (160 µs), the shell event the lane reports.

  The premise that the converged echo exceeds exact reach therefore does not wholly reduce to K-104. What it does
  mean:
  - The lane's 1/N extrapolation (c ≈ 3–5.6, N_σ = 300–557) fits the *total* drift. Roughly half of that drift is
    the classically structured H + floor piece.
  - A hybrid adversary (large-N transfer for H_∞, exact clusters for R) needs to capture only the residual. That
    adversary is untested (INFERENCE).

## 4. Pre-registration and claim-framing problems

1. **SUPPORT is not the pre-registered outcome.**
   - R1-SIM SUPPORT requires Δ₁₈ > 3σ at t ≥ 160 µs on **both** probes. It is met on p245 only; p19 at 320 µs is
     0.026 < 0.03.
   - The pre-registered reading is **INCONCLUSIVE** (lane §4.2).
   - The lane's "SUPPORTS" rests on post-hoc extrapolation plus a post-hoc critique of the KILL rule. The critique is
     valid in itself, but it does not turn INCONCLUSIVE into SUPPORT.
2. **"Late window 240–320 µs" is mostly unmeasured at N = 20.**
   - N = 20 was measured only at 160 and 320 µs on p19, and at 160 µs on p245.
   - Nothing was measured at 240 or 280 µs, or at 320 µs on p245.
3. **Category 3 of the charter is a computational/resource *advantage*, which needs both sides costed.**
   - The quantum side is not costed.
   - The comparator is exact simulation, not the best classical method.
   - The statement is therefore a classical exact-reach bound, not a claim in any of categories 1–6.

## 5. What would change this verdict

All three of the following would be needed. Even together, they would give only a physics-simulation result, not a
protein-structure one.
1. A physically observable version of the echo whose informative window lies inside a *measured* protein reversal
   horizon (T3/T2 ≥ 15; K-105 condition ii).
2. A measured, not extrapolated, σ-cone above the exact frontier in that window.
3. Failure of the best classical adversaries: two-point + exact-cluster hybrid, spinDMFT/nl-spinDMFT, Starkov–Fine
   hybrid.

## Compute and files

- Compute: under 1 single-threaded CPU-minute (analysis of existing JSONs only). No background processes, nothing
  modified outside this folder, no git commit.
- Files:
  - `relevance_decomp.py`: decomposition of the ladder steps, reversal-horizon mapping, observable amplitude;
  - `relevance_decomp.json`: all numbers quoted above;
  - `README.md`: this file.
- Upstream inputs, read-only:
  - `../reach_summary.json`;
  - `../verify_classical/runs/*honly*.json` (sibling verifier);
  - `../../../ADVERSARIAL/R1_physics_feasibility/scales.json`.
