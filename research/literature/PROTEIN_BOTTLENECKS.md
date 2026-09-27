# What is actually hard in protein structure computation

_Literature phase, 2026-09-26. Citation keys resolve in `BIBLIOGRAPHY.md`. Program evidence ids (I-1, QX-, R-) refer to `research/sprint29-33/` and `research/QUANTUM_OPPORTUNITY_MAP.md`. **I(prog)** marks this program's own reasoning._

## 1. Computation-limited vs information-limited

| Subproblem | Limited by | Literature evidence | Program evidence |
|---|---|---|---|
| Single dominant structure from sequence (natural proteins) | **Information.** Inference is cheap. | AF2 accuracy falls below a median MSA depth of ~30, with small gains beyond ~100 [E89]. ESMFold predicted 617 M structures [E92]. | I-1 … I-6 (9–60 aa) |
| Alternative conformations / fold switching | **Information** (memorisation). Extra sampling does not help. | Only 1 of 7 fold switchers outside the training set was captured despite ~280,000 extra models [E100]. AF2 fails on fold switching [E94]; AF-Cluster [E97]; disputes [E98, E99]. | — |
| Approximate 300 K monomer ensembles | Largely **amortised** by ML. Residual error is limited by training data. | BioEmu ~4 min per 1,000 samples at 100 aa, ~L² cost, ~1 kcal/mol ΔG [E83]. AlphaFlow [E80]. ML coarse-grained models ≥10³× faster than all-atom [E85, E86]. | — |
| IDP ensembles (coarse-grained) | Neither computation nor information is severe; limited by the force field | CALVADOS simulated 28,058 IDRs [E88] | — |
| **Exact Boltzmann / posterior sampling of a *specified* energy at ≥ tens of residues** | **Computation** (mixing across metastable basins) | Exact learned samplers stop at ~hexapeptides [E79]. Timewarp [E77]. BPTI state interconversion is more than 10³× slower than local relaxation [E15]. | Unmeasured (OP-01). Value shown at mid30: soft readout 1.40× MDE (QX-28). |
| Kinetics of slow transitions | Computation, but classically addressed. The residual problem is variance and choice of collective variables. | WE for 10 µs–100 ms folding times [E62, E63]. TPS [E60]. MSMs to hours [E67]. | Outside the endpoint |
| Free energies (binding, stability) | Force-field accuracy, then slow-mode sampling. Estimators are already optimal. | MBAR [E69]. FEP+ [E73]. RMS 1–2 kcal/mol from force-field error [B71]. | Outside the endpoint |
| Lattice / HP ground states | Computation in the worst case (NP-complete), practically solved | NP-complete [E12, C80]. Wang–Landau to 500-mers; FRESS finds new minima beyond L > 80 [E55, E56]. PERM [E53]. | DE-8 (proxy energies fail condition C) |
| Rotamer packing | NP-hard in the worst case; exact in practice | [C81] vs cost-function networks [C82] and tree decomposition [C83] | — |
| Global minimum of a learned energy (continuous decode) | Saturated at 44–60 aa | — | Restart saturation at 32–64 restarts; floor gap 0.14 Å (QX-30) |

**I(prog).** Only one row is both computation-limited *and* inside a structure endpoint: **exact sampling of a specified (learned) energy posterior at length.** That row is where every surviving quantum candidate lands (`QUANTUM_PRIMITIVES.md` §1).

## 2. Where classical sampling is provably slow (the templates)

Classical sampling hardness is not generic. The literature identifies specific regimes:

| Regime | Statement | Source | Fixable classically? |
|---|---|---|---|
| (a) Energetic barriers, large basins | PT turns an exponential cost into a polynomial in barrier height (diffusive ∝ barrier, ballistic ∝ √barrier) | Machta [E33] | Yes (PT) |
| (b) Golf-course / entropic bottleneck (small hidden basins) | PT gives only a "modest speed-up … due to brute force parallelism"; local Metropolis is exponential in N | Machta [E33] | No known general fix |
| (c) Persistence: very narrow and very wide peaks of comparable mass | "parallel and simulated tempering are shown to mix slowly" | Woodard, Schmidler, Huber [E39 = A74] | Partly (Hamiltonian tempering) |
| (d) First-order transition crossed by the tempering parameter | "converges slowly regardless of the temperature schedule" (mean-field Potts) | Bhatnagar & Randall [E40] | Yes in part (entropy dampening, Hamiltonian tempering) |
| Rapid mixing of PT | Spectral-gap lower bounds; rapid mixing for normal mixtures and mean-field Ising | Woodard et al. [E38 = A73] | — |

**The matching quantum result.** The provable continuous-domain separation [A45] is built exactly on (b)/(c)-type instances: a hidden narrow deep well, with α = e^{βΔ}. Whether any protein-relevant posterior lies in (b) or (c) is the decisive open question.
- **Against:** funnel theory [E2–E5], polynomial lattice folding times [E6], and Anton simulations of 12 fast folders [E16 = A77] argue that natural landscapes are *not* golf courses.
- **Open:** learned energies (pair-distance posteriors from language models) have **no** published landscape characterisation. They could be more frustrated than physical funnels [E gap 3].

## 3. Explicit classical scaling laws (the numbers any quantum claim must beat)

| Quantity | Law | Source |
|---|---|---|
| PT replicas vs system size | ∝ √N | [E23, E28] |
| PT round trips (diffusive) | ∝ N_rep² (I(prog) combination) | [E33, E28] |
| HMC steps vs dimension | O(d^{1/4}) | [E51 = A75] |
| Random-walk Metropolis vs dimension | O(d); optimal acceptance 0.234 | [E50] |
| Lattice folding time | N^4 (designed) to N^6 (random) at the fastest-folding temperature | [E6] |
| Physical folding speed limit | ≈ N/100 µs | [E9] |
| Single-step exponential averaging | N_c ∼ exp(βW_d), exponential in system size, removed by staging | [E72] |
| Pivot moves | O(1)–O(log N) per attempt | [E58] |
| PERM | chains to N = 10⁶ at θ | [E53] |
| BioEmu cost | ~L² (4 / 40 / 150 min per 1,000 samples at L = 100 / 300 / 600) | [E83] |
| Brute-force MD | >100 µs/day at 10⁶ atoms (Anton 3) | [E18] |
| Exact learned samplers | up to ~6 residues | [E79] |

**Not found** (explicit gaps):
- any rigorous or systematic mixing-time scaling of PT/HMC/SMC with residue count for off-lattice Cα or torsion chains;
- any landscape characterisation of learned protein energies;
- any proof that cooperative folding puts tempering in regime (d) at 100–300 residues.

## 4. Consequences for a "realistic protein representation" in a quantum sampling test

Minimum requirements, derived from the literature and the S29–S33 evidence (I(prog)):

1. **Off-lattice chain** (Cα trace or torsions). Lattice HP is disqualified: it is classically solved to 500-mers [E56], and it is the predecessor's DE-8.
2. **Scalable family** from 30 to ≥150 residues, so that the scaling of the classical mixing time is *measured*, not inferred.
3. **An energy whose samples transmit to the endpoint.** Condition C: [A72] and the S29–S33 transmission failure.
4. **A demonstrated hard regime** — (b), (c) or (d) — for the *best* classical sampler, not just local Metropolis. Convergence diagnostics can miss torpid mixing: "commonly used convergence diagnostics will fail to detect" it [E39]. Measurement must therefore include multi-start basin-population cross-checks.
5. **A native-free, coherently implementable energy oracle.** O(N²) pair terms. No resource estimate exists (gap G-2).

**The classical twin is a portfolio** [E §7D]:
- PT/REST2 + HMC, with feedback-optimised ladders [E20, E31, E32, E47, E51];
- SMC / AIS / PERM-style growth with resampling [E53, E54, E74, E75];
- learned-proposal MCMC and SMC-corrected flows [E77, E79];
- Hamiltonian tempering or entropy dampening where temperature tempering is torpid [E40];
- an amortised generator used as an independence proposal with correction.

## 5. What the literature says about the one S29–S33 positive signal

- **The observation (QX-28).** A Boltzmann-weighted structural average beat hard CVaR tails on the mid30 chain (−0.248 Å, 1.40× MDE, T adversary).
- **Not evidence of quantum advantage.** The weighting was an **exact sum over an exhaustively enumerated 18-qubit space** (262,144 states). There was no sampling cost and no sampling variance to reduce [B §7]. Metropolis also came closer to the exact Gibbs mean than the Born machine (QX-29).
- **What it *is* evidence of (I(prog)).** The *value* of posterior-averaged structures under a learned energy. It is therefore a **scientifically meaningful target distribution** for a sampler: whole-distribution consumption, which escapes H-001's reduction class, since H-001 covers argmin, prefix and convex consumption of a *diagonal-energy distribution the circuit optimises*, not samples of a fixed posterior.
- **The gap between value and cost.** The value is shown at 25–40 aa in an enumerable space. The cost of obtaining such samples in a non-enumerable space at ≥60 aa is **unmeasured**.
- **What would turn it into a quantum-relevant target (all classical measurements):**
  1. the soft readout still improves the chain when computed from *sampled* (not enumerated) posteriors at long40 and beyond;
  2. the best classical sampler's cost to reach that quality grows steeply with length;
  3. the growth sits in regime (b)/(c)/(d) and not (a).
