# Open literature gaps

_Literature phase, 2026-09-26. Citation keys resolve in `BIBLIOGRAPHY.md`._

**Novelty ≠ advantage.** A gap means no paper was found. It does not mean a quantum advantage exists there. Each gap is annotated with: whether it matters for the quantum question, whether filling it is classical or quantum work, and the answer we expect.

| Id | Gap | Found by domains | Why it matters | Work type | Expected outcome (prior) |
|---|---|---|---|---|---|
| G-1 | **No measurement of mixing times or spectral gaps for learned-energy protein posteriors** (or off-lattice Cα/torsion chains) as a function of residue count, using best-in-class samplers | A, B, D, E, F (all five that addressed sampling) | Every quantum sampling speedup is stated in δ or C_PI. Without δ(L), M1, M2 and M5 cannot be judged. | **Classical** | Probably polynomial on funnelled landscapes [E2–E6, E33]. **Unknown** for learned energies (G-3). |
| G-2 | **No fault-tolerant resource estimate for a walk, Metropolis or QSVT sampler on a continuous molecular or learned protein energy**; Ising, SK and LABS only [A55, A56, A46] | A, B, C, D, F | Needed to state break-even (filter K5) | Theory / compilation | Likely negative: per-step cost ≥ the Ising case (I(agent) 10⁶–10⁸ Toffolis) |
| G-3 | **No landscape characterisation of learned (language-model-derived) pair-distance energies**: frustration, mode structure, persistence | E | Decides whether [A45]-type hide-and-seek instances or [E39]-type persistence occur | Classical | Unknown. Could be *more* frustrated than physical funnels |
| G-4 | **No quantum-vs-PT/REMD/SMC comparison on any biomolecular sampling task** | A, D, E | Positive quantum sampling claims use local Metropolis [A46, A47, D9] | Classical baseline plus (later) quantum | — |
| G-5 | **No quantum-folding paper benchmarks PERM, REMC, Wang–Landau or CPSP** | D | Every lattice claim is untested against the frontier | Classical | Negative for quantum (these solve 500-mers [E56]) |
| G-6 | **No coherent-oracle analysis for pair-specific learned tables or neural potentials** (data loading, reversible evaluation) | A, F | Dominant cost for M1, M2, M6 | Theory | Likely prohibitive for per-pair tables; unclear for shared potentials |
| G-7 | **No residue-indexed quantum-vs-classical runtime scaling** for any protein task against strong baselines | C, D | The only residue-indexed statements are encoding sizes [D6] | Both | — |
| G-8 | **No analysis of search-tree size T(N) or treewidth** for rotamer or contact CSPs in the regime where exact classical methods fail | C, D | Needed to size √T backtracking gains (M10) | Classical | Likely small treewidth [C83], so no window |
| G-9 | **Planted-inference speedups [C71, C72] not mapped to structure inference from noisy restraints** | C | The only super-quadratic family | Theory | Likely inapplicable: the endpoint is information-limited |
| G-10 | **No quantum generative model of protein *structures*** (coordinates or torsions) | F | Novel in engineering terms | Quantum | Classical surrogates predicted [F88–F91]; no advantage expected |
| G-11 | **No test of whether cooperative two-state folding places tempering in the torpid first-order regime [E40]** at 100–300 residues after REST2 or Hamiltonian tempering | E | A route to real classical hardness | Classical | Unknown |
| G-12 | **Exact reweightable learned samplers beyond hexapeptides [E79]** | E | A classical frontier; progress shrinks any quantum window | Classical ML | Active field; likely to advance |
| G-13 | **No study checks whether quantum-found low-energy states improve downstream accuracy**, not just a proxy energy | C, D | The transmission failure (S29–S33, [D28]) | Both | Negative on proxy energies |
| G-14 | **Super-quadratic sampling claims [A46, A47] lack large-n validation** | A | Only escape from the quadratic-overhead trap | Classical simulation / bounds | Probably not sustained |

## Gaps this program is positioned to fill

G-1, G-2 and G-3 together make a coherent, publishable study. The program has a learned energy class (esmprior), a length-scaled instrument design and a strict statistical contract. Its value is **decisive either way**:

- **If** the learned-energy posterior mixes polynomially under the classical portfolio (G-1), **or** the break-even (G-2) sits far above any measured classical cost: a scoped negative result (category 6 / 3). *"No quantum sampling speedup can matter for learned-energy protein posteriors up to N residues."*
- **If** mixing grows steeply, **and** the landscape shows persistence or hide-and-seek structure (G-3), **and** the break-even is reachable: the first justified target for a quantum sampling resource claim (category 3), with a provable query separation class [A45] behind it.

The other gaps (G-4 … G-14) are either implied by this study or have strongly negative priors.
