# Classical counterarguments (discovery sprint, 2026-09-27)

_For every attacked mechanism, the classical-adversary lens tried to beat or dequantise it. The resource lens priced the quantum side with full accounting. Below, per mechanism: the verdicts and levels, the strongest pro-quantum rebuttal, which the lens was required to state before deciding, the evidence (abridged), and the cost note. Unabridged records: `attack_records.json`. Items marked MEASURED in a lens record came from exploratory lens runs. Several ran outside the governor and are single-seed, so the synthesis requires them to be replicated before KILLBOOK entries cite them._

## Four structural reasons that recur across the kills

1. **Quadratic ceiling plus a landscape-independent runtime floor.** Every sampling, search and estimation route on a classical learned energy is at most quadratic. At break-even the quantum per-sample wall-clock is T*_Q = A·ρ·(K n_b G t_T)²/c, and that value does not depend on the landscape. It is ≥ 0.26 yr/sample even at 1 µs Toffolis on a relaxed target, and ≥ 1–20 yr on the A80 target (research/theory/BREAK_EVEN.md §1). So no amount of classical hardness makes these routes practical.
2. **White-box, pair-additive energies leak their own structure.** Distance-geometry seeding, factor-table reads, collapse of assignment sums and the KL sublevel bound all dequantise the constructions that separations rely on: hide-and-seek wells, hidden labels, and oracle graphs.
3. **In every spectroscopy, fold information lives in weak couplings, and weak couplings are classically perturbative.** The hard many-body sector carries local, degenerate or finite-size information. Hardness and identifiability squeeze each other.
4. **Information versus computation.** The endpoint is information-limited (H-002). New information enters through experiments, and those experiments already have classical interpreters.

## QM-01: Warm-started walk / QSA / quantum replica-exchange Langevin sampler for the learned-energy structure posterior at >=60 aa (lead M1/M2 sampler core)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 on the protein instance family (esmprior/A80 posterior at 60-300 aa). The only L6 results are generic or synthetic. First, the quadratic walk-step or query speedup in the per-stage gap from Szegedy, Somma et al. and Wocjan-Abeyesinghe. Second, the information-theoretic separation of Olivucci et al. 2026: Omega(alpha) classical vs O~(sqrt(alpha)) quantum on 'hide-and-seek' torus wells, with alpha = e^{beta*Delta}. Nothing shows that the esmprior/A80 posterior belongs to that hidden-well class, and the mode census points the other way (see evidence).
- **Practical level:** L0. No resource-normalised or empirical advantage. On the measured cost model, the classical requirement predicted for 150-300 aa (about 1e6-1e8 gradient evaluations per decorrelated sample, a model extrapolation) sits at least 2-3 orders of magnitude below the sequential fault-tolerant break-even (about 2e10-2e14). It sits at least 4-5 orders below once the classical sampler's parallelism is counted (break-even scales as P^2 * R^2).
- **Strongest pro-quantum rebuttal considered:** (Pro-quantum rebuttal, stated as strongly as the data allow.) The G1 pilot data show a real classical failure. NRPT on the lambda-path at T=1 produced 0 round trips in every pilot. For 5O37A_45 and 3GAHA_60 the ladder was adequately provisioned: Syed et al. Cor. 1 under efficient local exploration (ELE) predicts 27.5 and 21.1 round trips in 1500 and 1200 scans (res/results/RAW/g1_pilot/*.json; also research/theory/PROOFS/T2_sampling_checks.py C4). The 150-aa ladder was under-provisioned (39 rungs for Lambda = 29.3), so its zero count is less informative. The mode census is restart-unsaturated at 60-100 aa for 19-25% of targets (p_hit of the best mode = 1/256). So C_class may already exceed 1e6 at 45 aa and could grow fast with L. Quantum acceleration can also stack on top of classical non-reversible lifts: Claudon-Piquemal-Monmarche (Nat. Commun. 2025) accelerate non-reversible chains, a
- **Evidence (abridged):** VERIFIED LITERATURE. Bibliography entries from research/literature/BIBLIOGRAPHY.md; extra checks via arXiv API on 2026-09-27.
(1) Lifting parity:
- Eberle & Lorler, 'Non-reversible lifts of reversible diffusion processes and relaxation times', arXiv 2402.05041, PTRF, doi 10.1007/s00440-024-01308-x.
- Eberle & Lorler, arXiv 2412.16710, J. Funct. Anal. 2026, doi 10.1016/j.jfa.2026.111605. Abstract: 'Non-reversible lifts reduce the relaxation time of reversible diffusions at most by a square root', attained by Hamiltonian flow with velocity refreshment, i.e. randomized HMC / underdamped Langevin.
- Cao, Lu, Wang, ARMA 247:90 (2023), arXiv 1908.04746: underdamped Langevin rate O(sqrt(m)) vs m (overdamped, convex).
- Chen-Lovasz-Pak STOC 1999 [#14]; Diaconis-Holmes-Neal 2000 [#15].
- Apers-Sarlette-Ticozzi PRA 98:032115 (2018), arXiv 1712.01609 [#16]; Dervovic arXiv 1712.02318 [#18]: for every quantum-walk mixing speedup there is a classical lifted chain that mixes as fast or faster. Caveat: the lift may not be efficiently constructible, and this does not cover QSA's warm-start reflections.
- Aharonov-Ambainis-Kempe-Vazirani STOC 2001 [#12]: quantum-walk mixing speedup is bounded (conductance).
Consequence: in the diffusive or ill-conditioned regime, the Szegedy phase gap sqrt(delta) is matched by classical ballistic or preconditioned dynamics. A residual quantum gain exists only in Arrhenius or bottleneck-limited stages (delta ~ Phi), which tempering flattens unless the landscape

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for QM-01 as posed. No separation from the best classical sampler has been shown for any instance family that contains the learned-energy posterior. The underlying primitive does have an L6 query-model statement: walk/QSA steps scale as ~1/sqrt(delta) against 1/delta [A7, A8, A9, A31]. But that comparison is against the SAME reversible chain P. Lifted and non-reversible chains, and HMC, already reach ~1/Phi (Apers-Ticozzi-Sarlette [A17, arXiv 1705.08253]). Against the best classical method the gain therefore lies between O(1) (diffusive regime, Phi ~ sqrt(delta)) and quadratic (bottleneck r
- **Practical level:** L0, and the resource-normalised (L3-type) break-even analysis is negative. No scenario reaches break-even with a quantum runtime shorter than about 100 days per sample, even after stacking every quantum-favourable assumption. For the faithful oracle, the quantum runtime at crossover is about 4e6 to 1e8 years per sample.
- **Cost / break-even note (abridged):** Break-even B* is the number of classical energy+gradient evaluations per independent sample above which quantum wins:
- Faithful learned-energy walk (5.1e8 Toffolis per step at 150 aa; 24 h per step on one factory; 2.4e4-4.9e4 logical and ~1e8 physical qubits): B* ~ 2.4e16 to 1.5e19 per sample. Quantum runtime at crossover is 4e6 to 1e8 years.
- Absolute floor, stacking a Cartesian local-move oracle (~3.9e6 Toffolis per step), 100 CCZ factories (~1e9 physical qubits), a single-core unoptimised classical code at 5.1 ms, kappa' at its derived lower bound and c=3: B* ~ 1.7e9 per sample (7.6e8 at 300 aa), with 102 days of quantum runtime per sample.
- The soft-readout target needs 1e2-1e3 samples, which run in parallel classically and in series on one QPU. That pushes B* to 2.5e11-1.6e14 and the runtime to 40-1000 years per target.
- Toffolis per sample at crossover: ~5e12 (floor) to ~7e17 (faithful).

The code-distance correction for these long runs (d = 39-51) adds another 1.6-2.7x against quantum. The oracle does not erase the asymptotic quadratic gap; the constant factor t_Q/t_C ~ 1e7 to 4e8, squared, puts the crossover out of reach.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for this protein instance: it is a formulation only. No separation has been shown for the esmprior/A80 posterior, and none has been shown against lifted, non-reversible, PT or HMC samplers. Generic support exists for the primitive only. (1) L6-quadratic walk-step speedup against REVERSIBLE chains in an oracle model (Szegedy 2004; Somma et al. 2008; Wocjan-Abeyesinghe 2008; Harrow-Wei 2020; warm start per Orsucci et al. 2018). (2) Provable Omega(alpha) vs O~(sqrt(alpha)) continuous separation, but only on hide-and-seek wells on the torus (Olivucci et al., arXiv 2608.24527). Nobody has shown 
- **Practical level:** L0. No classical mixing failure has been measured on the target, so the reopening burden of DNR-10/K-007 is not met. Prior evidence runs against the value premise. The break-even point is at least 1e9 to 1e10 gradient evaluations per independent sample at 150 aa. On this 8-core box that is roughly 40 CPU-days or more per sample (measured 3.5 ms per batched gradient evaluation at 150 aa), so the proposed ~1-day campaign can only KILL. It cannot certify C_class >= B(L).
- **Novelty note (abridged):** Every mechanism in QM-01 is prior art:
- quantum-walk Metropolis on protein torsions with a learned initialisation: QFold 2021/2022;
- QSA on Bayesian posteriors: Harrow-Wei 2020;
- warm-start / slowly evolving chains: Orsucci et al. 2018;
- QSA on Langevin (ULA) chains for non-logconcave targets with finite-sum oracles: Ozgul et al. ICML 2024;
- sum-structured log-likelihood oracles inside QSA: Miyamoto 2023;
- continuous replica-exchange and QSVT samplers: Leng et al. PNAS 2026;
- the provable continuous separation: Olivucci et al. 2026;
- MH walk circuits: Lemieux 2020, Claudon 2026.

The BC >= (1+chi^2)^-1/2 bridge is a one-line Hoelder inequality.

The search (arXiv API, quantum walk / QSA / Metropolis x protein / peptide / conformational / Boltzmann, 2019-2026, plus the 448-paper literature phase) found no evidence of a paper that combines all four of the following:
(a) a quantum w

## QM-02: Hide-and-seek narrow wells: provable continuous-Gibbs separation vs white-box discovery, calibration and the DMDGP ceiling

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 on the protein instance family. The Omega(alpha) vs O~(sqrt(alpha)) separation of Olivucci et al. [A45, arXiv:2608.24527, verified] is L6, but only for its information-local, black-box hide-and-seek family, and it provably does not transfer to this energy. DERIVED (proof sketch): E(x) is linear in its pair-table grid values plus a small, known local head. The parameter count is P ~ 2*(L-3)(L-2)/2*1001, i.e. 9.5e6 at L=100 and 2.2e7 at L=150 (about 5e4 gradient queries at L=100). So a classical algorithm can identify the whole energy with at most P+1 generic value queries and then sample off
- **Practical level:** L0. I measured this directly this session on the vendored A80/esmprior_v1 energy at T=1, using the same 200-iteration batched L-BFGS as scripts/g1_mode_census.py. A deterministic white-box construction finds the deep basins that prior-initialised restarts and PT miss. The construction is: expected distances from the distograms, then classical MDS plus weighted SMACOF, then both chiralities, then L-BFGS. That is 2 descents, about 400 gradient evaluations.
(a) This expected-distance pair gave the lowest DG basin in 61/64 crop runs (L=80: 15/16; L=100: 15/16; L=120: 15/16; L=150: 16/16), out of 1
- **Strongest pro-quantum rebuttal considered:** 1) Unknown unknowns. No classical method certifies that no deeper basin exists. An adversarial well could be spread as many weak pair biases, each below its table's modal bin, so the expected-distance seed would not see it (class O). Answer: the family is still linear in the tables, so it is query-identifiable, and the hardness becomes offline and spin-glass-like, where known quantum gains are Grover or backtracking (quadratic) and are killed by the break-even. Such wells would also be the artefacts of a mis-calibrated composite likelihood that the candidate itself predicts.
2) Everything here was measured at T=1. At a coverage-calibrated T* (Varin-Reid-Firth / Ribatet-Cooley-Davison magnitude adjustment, arXiv:0911.5357) mass spreads over many basins and the task becomes ensemble sampling. Answer: temperature makes narrow wells lose mass entropically. The PT communication barrier falls 
- **Evidence (abridged):** MEASURED this session (scratchpad dg_seed.py / dg_seed2.py; outputs dg_L80.json, dg_L100.json, adv_qm02_dg2_L120.json, adv_qm02_dg2_L150{a,b}.json in C:\Users\abena\AppData\Local\Temp\claude\C--Users-abena-quantum-advantage-protein-folding\deded8ee-ac50-420b-a8f2-b349dc3a4fdc\scratchpad\; run through the master governor spool). Baselines: research/results/RAW/g1_modes/*_R256_s0.json (census) and research/results/RAW/g1_pilot/*.json (PT polishedE: 20809.7 / 33162.5 / 51923.4).
Census scaling from the existing data: the geometric-mean p_hit of the best mode falls by about 0.024 per residue (0.10 at L=30 to 0.016 at L=100). Extrapolated, that reaches 1e-4 at L of about 320 and 1e-10 at L of about 900, for table-blind restarts. DG makes the relevant p_att of order 1.
Unrelaxed expected-distance DG at 5O37A_100 already has E=21120, below the census best of 21168. The native scores E=22362, above the energy minima.
DERIVED: the table-identification bound (see level_theoretical).
Citations verified this session (arXiv API or Crossref):
- Olivucci et al., arXiv:2608.24527
- Pompe-Holmes-Latuszynski, Ann. Stat. 2020, doi:10.1214/19-AOS1916, arXiv:1812.02609 (JAMS)
- Tawn-Moores-Roberts, ALPS, arXiv:2112.12908 (O(d) iterations given modes)
- Re-ALPS, arXiv:2512.17977 (polynomial mixing from per-mode warm starts)
- Tawn-Roberts-Rosenthal, weight-preserving ST, doi:10.1007/s11222-019-09863-3
- QuanTA, doi:10.1017/apr.2019.35
- Andricioaei-Straub-Voter, smart darting, doi:10.1063/1.135886

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for the protein task. The Olivucci et al. [A45] Omega(alpha) vs O~(sqrt(alpha)) separation is a provable (L6-type) query result only for the constructed hide-and-seek family. T5 (research/theory/NO_GO_RESULTS/T5_quadratic_ceiling.md, Theorem A) shows it is exactly quadratic, and in practice it is Grover applied to rejection sampling. The A80 learned energy is not a member of that family, for two reasons. (1) It is white-box and pair-additive: every 1-D pair table exposes the location of a well through its minima, so the energy is not information-local and Lemma 1 does not apply. (2) Its alp
- **Practical level:** L0. The minimal form of the idea (amplitude amplification of the product head prior onto a sublevel set) is dead by 30 to 200 orders of magnitude, whatever the hardware. Even the idealised golf-hole case needs a best-classical hit probability p_C &lt; ~1e-15 per mass-carrying basin at 170 us per Toffoli (S=1), and it breaks even only after T* = 1.3e3 to 1.7e5 years. Against 1e3 cores the requirement becomes p* ~ 1e-21 with T* ~ 1e6 to 2e8 years. Every census basin measured so far has p_hit >= 1/256, and parallel tempering (PT) reached lower-energy states than restarts on 3 of 3 crops.
- **Cost / break-even note (abridged):** Per Grover iterate, where the iterate is one value oracle compute plus uncompute, prior prep and its inverse, and the reflections:

| L | Toffolis (central, generous) | logical qubits | physical qubits (d = 47 to 57) | wall-clock at 170 us |
|---|---|---|---|---|
| 60 | 4.4e7, 2.0e7 | 2.0e4 | 0.7 to 3.3e8 across L | 2.1 h |
| 100 | 1.2e8, 5.2e7 | 3.3e4 | (as above) | 5.7 h |
| 150 | 2.7e8, 1.1e8 | 4.9e4 | (as above) | 12.5 h |

Pair-table lookups are 92 to 97% of the cost. A gradient oracle (for the Olivucci sampler) costs about 3x more. Fixed-point or unknown-threshold search costs 1.6 to 2.2x more in queries.

1. **Minimal form (product-prior amplitude amplification onto {E &lt; E_thr}).** The required iterate count 1/sqrt(p_sub) >= e^{KL/2} is 1e8 to 1e99 at L=100 (lambda from 0.01 to 1). Restarts need 1/p_att ~ 1e2 to 1e2.4. The quantum side loses by at least 1e30 at any physically meaningful temperature. It cannot win for ANY p_sub while p_att >= t_C/(c S t_Q) = 4.6e-5 (S=1, 170 us). KILL independent of hardware.
2. **Golf-hole idealisation.** Break-even needs p* ≈ 1e-15 at 170 us and S=1, with T* = 6.5e3 to 6.3e4 years (1.5e4 to 1.7e5 years once d is corrected). At S=1e3: p* 

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for the protein instance. The L6 result (Olivucci et al., arXiv 2608.24527, verified: Omega(alpha) classical vs O~(sqrt(alpha)) quantum gradient queries) holds only for its own black-box class: a smooth bump on a torus whose log-density is constant outside a small patch, so every value and derivative query there returns the same flat answer (the paper's Sec. III.1). The learned energy is not in that class. It is white-box, and it is a sum of O(L^2) soft-binned (sigma = 0.5 A) -log p pair tables plus theta/tau and steric terms (src/qapf/protein/energy.py), so gradients carry information almo
- **Practical level:** L0. No quantum or classical evidence shows that a mass-carrying narrow basin exists that prior-initialised descents or PT miss while it matters for structure. The in-progress G1 data (raw, uncommitted, preliminary, I(agent)) point the other way. At L=100, PT at T=1 finds minima far below the 256-restart best, but at the same RMSD: 5O37A_100 is 358 energy units lower at 5.54 vs 5.56 A; 3GAHA_60 is 31 units lower at 11.31 vs 12.14 A. Condition C reappears: deeper wells do not transmit to structure accuracy.
- **Novelty note (abridged):** Scope: arXiv API queries only (the WebSearch budget was exhausted), plus the 448-paper repo bibliography.

- The search found no evidence of any paper applying the A45 continuous-Gibbs separation, or any hide-and-seek query lower bound, to learned protein structure energies. A45 itself does not mention molecules. The search also found no evidence of distogram / learned pair-distance potentials being treated as composite likelihoods with a calibrated temperature (0 arXiv hits).
- The components are not new:
  - quadratic rare-mode discovery for biomolecules (Kodama et al. 2026; Mazzola 2021; Ghamari et al. 2022);
  - Grover for DMDGP (Lavor et al. 2022, QIP 21:239);
  - quantum backtracking quadratic in tree size (Montanaro 2018);
  - composite-likelihood curvature/temperature adjustment (Ribatet et al.; Stoehr & Friel; Varin–Reid–Firth);
  - Woodard persistence (2009);
  - distance-geome

## QM-03: Gates on what any faster sampler can buy: readout-visible slow modes (delta_f, H(B)), walk-vs-lift ratio sqrt(delta)/Phi, and learned-transport preconditioning

### Lens: classical (verdict: KILL)
- **Theoretical level:** L1 overall. One restricted statement is L6-sound: against lifts of the same reversible chain P, T_lift/T_QW = Omega(sqrt(delta)/Phi). That follows from the Cheeger bounds Phi^2/2 <= delta <= 2Phi and the fact that lift mixing is at least Omega(1/Phi) (Chen-Lovasz-Pak; Apers-Ticozzi-Sarlette). Against the best classical estimator (basin decomposition, SMC or population annealing with resampling, variational-reference NRPT, nested sampling), no separation has been established on this instance family. In the metastable regime the gate itself points to, basin decomposition costs nothing in Phi, so
- **Practical level:** L0. The measured classical cost to reach the best-found basin is about 3.6e4 to 5.6e4 gradient evaluations per crop (256 restarts x ~200 L-BFGS steps, 23-485 s on CPU). This holds at L <= 80, and p_hit >= 3.9e-3 there. The break-even in the repo's own T2 analysis is B* = 2e12 to 1.4e22 local steps per sample, or p* = 6e-18 to 1.5e-10 for amplitude-amplified multistart. The gap is 7 or more orders of magnitude, on roughly quadratic overhead, before counting fault-tolerance constants.
- **Strongest pro-quantum rebuttal considered:** The strongest case for quantum relevance is that the landscape evidence is pilot-grade and censored exactly where the gate could bite.
(i) The mode census uses one seed and R=256, so p_hit is floored at 1/256. At L=100-120 it saturates: 230-256 distinct modes from 256 restarts. Four crops are both hard (p_hit <= 2/256) and informative (best mode < 6 A): 3TE4A_100 at 5.2 A, 5O37A_120 at 5.0 A, 5QHWA_100 at 4.6 A and 9PGXA_100 at 3.9 A. These are the only crops where readout-visible hardness could exist.
(ii) The Laplace basin entropies are unreliable (about 104 non-positive Hessian eigenvalues at L=100). The best-vs-second-basin log-det difference can be about 76, i.e. about 38 nats of entropy. The large energy gaps (below) may therefore be partly compensated, so posterior mass could be spread over several basins, and then the soft readout needs inter-basin weights.
(iii) In a truly glass
- **Evidence (abridged):** A. Gate 2 (lift gate) is right but aims at the wrong adversary.
- The Cheeger bounds give Phi^2/2 <= delta <= 2Phi.
- Lifts mix no faster than Omega(1/Phi): Chen, Lovasz, Pak, STOC 1999, DOI 10.1145/301250.301315 [bib #14]; Apers, Ticozzi, Sarlette, arXiv:1705.08253 [#17].
- Quantum-walk mixing as a local evolution is reproduced by lifted chains: Apers, Sarlette, Ticozzi, PRA 98, 032115 (2018), arXiv:1712.01609 [#16]; Dervovic, arXiv:1712.02318 [#18]. The surviving 1/sqrt(delta) is therefore the non-local QSA or phase-estimation route, which needs warm starts or overlap along a path.
- Derivation (basin decomposition, BD). Write pi = sum_k w_k pi_k over the gradient-flow catchments B_k. The classical estimator runs R restarts from the exactly sampleable product (theta,tau) prior with n_dec steps each. It then runs a local chain in each found basin (local gap delta_k) and estimates Z_k by TI/BAR from a basin-centred Gaussian (cost about thermodynamic length squared). The readout is E f ~ sum ŵ_k Ê_k f.
- Its total cost is C_BD = R*n_dec + sum_k (tau_k sigma_k^2/eps^2 + C_TI,k). Phi does not appear. The only bias is sum over missed basins of w_k*|E_k f - E f|.
- In the metastable regime (delta ~ Phi ~ e^{-dF}), the global walk costs about e^{dF/2}, exponentially worse than BD whenever the readout-relevant basins have p_hit >= 1/poly.
- The quantum version of BD gains only sqrt on R/p_hit (amplitude-amplified restarts, at most 16x for p_hit >= 1/256), on tau_k (small) and on sig

### Lens: resource (verdict: KILL. QM-03 has no quantum speedup of its own. Every one of its three gates can only raise QM-01's break-even; none can )
- **Theoretical level:** L0 for any quantum gain that survives QM-03 on the esmprior/A80 posterior. The only provable statement is L6 against a restricted adversary, and it is inherited textbook material, not new. It holds only in the metastable regime (delta ~ Phi), against lifts of the same chain, in the query model: every lift has t_mix = Omega(1/Phi) (Chen-Lovasz-Pak 1999; Apers-Sarlette-Ticozzi), while QSA/Szegedy costs O~(1/sqrt(delta)) = O~(Phi^-1/2). In the diffusive regime (delta ~ Phi^2) the walk-to-lift ratio is O(1). The candidate's gates themselves are DERIVED bounds (Cheeger, the lifting bound, and Heinr
- **Practical level:** L0. Wall-clock per independent sample at break-even (single core, pilot cost per evaluation c = 0.78 ms at L=60 and 1.46 ms at L=100):
- Best case with everything at its most favourable: 0.3-0.4 years.
- Mid scenario: about 2e3-1e4 years.
- Faithful oracle with one factory: 1e6 years or more.
The readout then needs n_C of about 50-1600 such samples, so the total is n_C times these figures. Pilot classical costs are at the 1e4-1e5 evaluation scale, which is 5 to 9 orders of magnitude below the break-even B*.
- **Cost / break-even note (abridged):** Gated break-even (DERIVED): B* ≈ r (rho K l R / p)^(2/(2-gamma)), with R = G t_Toffoli / c.

Breakdown at L = 60-100:
- Best case: at gamma = 1, r = 1, K = 1, D3sb oracle, 100 factories: 1e10.
- Mid: 1e14.
- Faithful oracle, one factory: 1e17-1e19.
- Each factor of 10 in r multiplies B* by 10.
- At gamma = 1.25, B* grows by 1e3-1e6. At gamma = 1.5 it grows by more than 1e10. At gamma = 2 there is no crossover.
- The Heinrich-limited precision factor p <= 3.4 lowers B* by at most about 10.
- Optimised classical kernels (c ≈ 50-100 us instead of 780 us) raise B* by about 60-240x.
- A 1 us Toffoli lowers B* by about 3e4.

Oracle costs erase the speedup in every scenario except one that stacks every favourable assumption at once.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for any advantage of its own: QM-03 proposes no speedup. Its three gates are classical bound statements. Two are corollaries of proven results under an explicit discrete-chain model: Chen-Lovasz-Pak (lifts cannot raise conductance) with Cheeger, and observable-specific relaxation. They cap QM-01's gain but add no quantum level. QM-01 itself stays at conditional L2 (walk/QSA query speedup under gap and overlap assumptions, oracle cost excluded), as the in-repo T2 note derives. Two gate formulas are not correct as written (see counterargument), so even their bounding role needs repair before 
- **Practical level:** L0. Nothing is resource-normalised beyond T2's existing break-even: B* is about 2e12 (L=45) to 1.4e22 (L=150) local steps per sample, a barrier of 28-51 nats. The proposed H(B) test reaches at most 1e8-1e9 evaluations, 3-4 orders of magnitude below the lowest B*. So it can kill QM-01's relevance but cannot put it in play at any L tested.
- **Novelty note (abridged):** Novelty is modest, and much of it is packaging. 

The walk-vs-lift ratio sqrt(delta)/Phi, in [1/sqrt2, sqrt(2/Phi)] by Cheeger, is a direct corollary of Chen-Lovasz-Pak 1999. Apers-Ticozzi-Sarlette 2017/2018 and Dervovic 2017 cover it for discrete chains, and Eberle-Lörler 2024 give the continuous square-root bound for lifts. 

Observable-specific relaxation (tau_int,f; projections onto TICA/MSM slow modes) is textbook classical MCMC and MSM practice. 

The search found no evidence of the following, under this scope: arXiv API keyword queries 'quantum AND Markov chain AND spectral gap AND observable', 'quantum AND normalizing flow AND MCMC', 'quantum walk AND lifted Markov', and title searches; plus the repo's 448-paper bibliography; WebSearch was unavailable this session: 
- (a) a paper that states quantum MCMC-estimation advantage in terms of the observable-visible to global gap ratio 

## QM-04: Cooperative (first-order-like) folding regime: quadratic speedup of a stretched-exponential tempering cost with explicit break-even length L*

### Lens: classical (verdict: KILL)
- **Theoretical level:** Two separate levels. (1) L6, but only for the generic statement that a quantum walk on a given chain beats that same chain: Szegedy walk / QSA need about 1/sqrt(gap) walk steps, versus 1/gap for the classical chain (A8 Somma et al. 2008; A31 Harrow-Wei 2020). This is relative to a fixed chain, holds in the query model and says nothing specific about proteins. (2) L0 for any separation against the best classical algorithm on the first-order family. The paper the candidate cites for torpid tempering, E40 (Bhatnagar-Randall 2016), also proves the classical fix. On the mean-field 3-state Potts mod
- **Practical level:** L0. No torpid regime has been shown for the learned energy. In-repo NRPT pilots on esmprior/A80 at 45–150 aa show a polynomial communication barrier. The T=1 posterior sits in a single dominant basin. Against the reaction-coordinate adversary, break-even moves to L* of about 3e3–1e5 aa, well above single-domain sizes.
- **Strongest pro-quantum rebuttal considered:** The strongest case for keeping QM-04 is hidden barriers orthogonal to learned-Q. Candidates are competing folds with similar contact fraction (register-shifted beta-sheets, alternative packings or nucleation sites, domain-swap-like arrangements), plus mirror topologies, which are distance-degenerate and penalised only by the theta/tau head. These could keep a residual DeltaF_hidden(L) growing after (E, Q) biasing, and a k-dimensional flat-histogram method costs exponential in k if k must grow with L. The in-repo data do not rule this out:
(a) The NRPT local-barrier density per log-lambda develops a peak near lambda of about 0.8–0.98. Its peak-to-median ratio rises from 2.0 (45 aa) to 2.75 (60), 3.75 (100), 5.0 (120) and 4.7 (150), a specific-heat-like peak that sharpens with L.
(b) No NRPT run completed a single round trip in 500–1500 scans, so the replicas are not equilibrated and a fir
- **Evidence (abridged):** CLASSICAL ADVERSARY: order-parameter-biased or path-redesigned tempering, plus decode-and-reweight. The following methods reproduce or beat the claimed mechanism.
(1) Entropy-dampened tempering: Bhatnagar & Randall, J Stat Phys 164:495 (2016), doi:10.1007/s10955-016-1526-8, arXiv:1508.04521, verified abstract. Tempering on the mean-field 3-state Potts model is slow for every temperature schedule; entropy-dampened tempering mixes in polynomial time. This is E40, the candidate's own rigorous source.
(2) Multicanonical sampling: Berg & Neuhaus, PRL 68:9 (1992), doi:10.1103/PhysRevLett.68.9. The residual exponential slowdown under multicanonical sampling comes from droplet/strip shape transitions under periodic boundaries: Neuhaus & Hager, J Stat Phys 113:47 (2003), doi:10.1023/A:1025718703965. Where shape transitions are absent (spherical topology), biased sampling across a first-order transition scales as a power law, tau ~ V^2.5: Fischer & Vink, J Phys Condens Matter 22:104123 (2010), doi:10.1088/0953-8984/22/10/104123, arXiv:0910.5669, verified abstract. A finite free-boundary globule has no strip state (analogy; not verified for proteins).
(3) Microcanonical energy-ceiling annealing: Rose & Machta, PRE 100:063304 (2019), doi:10.1103/PhysRevE.100.063304, arXiv:1907.07067. Equilibrium SA, population annealing and hybrids all perform well at the first-order transition of the 20-state 2D Potts model. Population annealing at first-order transitions: Barash, Weigel, Shchur & Janke

### Lens: resource (verdict: KILL)
- **Theoretical level:** L1. Only one narrow statement holds, and it holds at the level of the walk alone. A qubitised/QSA walk on the same simulated- or parallel-tempering chain costs ~δ^{-1/2} ≈ e^{ΔF/2} steps, against e^{ΔF} for that chain. This is query-model/L6 relative to that chain [A31, A56], and it is rigorous for torpid tempering only on mean-field Potts [E40], where the barrier is extensive (∝N), not L^{2/3}. Relative to the best classical algorithm it is L0. For any genuinely two-state (first-order) system, a polynomial classical bypass exists: phase-separated sampling plus reference-state or confinement f
- **Practical level:** L0. No resource-normalised window exists. The break-even per-sample wall-clock T* does not depend on ΔF(L), σ or L*. It is ≥ 19 yr under D2-central with c_q = 1, S = 1 and R_f = 100, and about 1e5 to 1e11 yr under realistic c_q, S and R_f. Cooperativity of esmprior at 45 to 300 aa has never been measured. The pilot shows no E_pair variance peak along λ at L = 45 to 150. The energy is out of distribution above 72 aa.
- **Cost / break-even note (abridged):** - **Break-even barrier and length.** ΔF* = 2·ln(c_q·S·G·t_T/(R_f·t_C)) + ln(κ/τ0) ≈ 19 to 56 nats, so L* = (ΔF*/σ)^{3/2} ≈ 36 to 1190 aa. With an extensive (mean-field) barrier f‡·L and f‡ = 0.1–0.3, L* ≈ 69 to 561.
- **Runtime at break-even.** T* per independent sample is 5.7 d in the fictional most-generous case (D3 bond-relaxed target, single classical core, c_q = 1, 100 factories). It is 19 yr for D2-central with S = 1, R_f = 100, c_q = 1, 1.9e5 yr at R_f = 1, and 7.7e10 yr in the realistic case (S = 1e3, R_f = 10, c_q = 100, optimised t_C).
- **Resources.** 1e4–1e5 logical qubits for ST, rising to 1.9–2.8e5 for 32-replica PT at L = 200–300. That is 0.3–1.4e9 physical qubits at d = 41–49.
- **Per step.** 0.5–2e9 Toffolis per step (D2), i.e. 1–4 days per step with one factory at L = 150–300.
- **ST weights.** They are an unpriced oracle, a free ln Z. Computing them classically yields the polynomial bypass.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L1 (conditional), at most. The quadratic walk/QSA speedup over the same tempering chain (steps about 1/sqrt(gap) instead of 1/gap) is a textbook result [A8 Somma et al. 2008; A31 Harrow-Wei 2020]. It is an L6-type theorem only relative to that one chain. It is not a separation from the best classical sampler. The premise specific to this candidate (esmprior's tempering gap <= e^{-sigma L^{2/3}}) is unproven, and the energy's structure argues against it: E_pair sums every pair |i-j| >= 3, so it is a mean-field-like energy, not a short-range energy with a droplet/capillarity barrier. The in-repo
- **Practical level:** L0. No measurement of cooperativity, Lee-Kosterlitz barriers, or a reaction-coordinate adversary exists for this energy. At break-even, one independent sample takes decades of wall-clock on either side under standard surface-code assumptions (see the cost note). The energy being sampled is out of distribution and overconfident at 60-150 aa.
- **Novelty note (abridged):** Within the program, the candidate is not new. It recombines OPEN_LITERATURE_GAPS G-11, regime (d) of PROTEIN_BOTTLENECKS, T5 section 4.2 (first-order-like lambda bottleneck, Grover-like per [X19]) and T5 section 4.5 (break-even). The only new element is the closed form L* = (2 ln R / sigma)^{3/2}.

Externally, the search found no evidence of a paper deriving a fault-tolerant break-even chain length for quantised simulated or parallel tempering across a protein cooperative-folding transition. Scope: arXiv API and Crossref queries, 2008-2026, plus the program's 448-paper corpus; general web search was unavailable this session, so treat this as provisional.

The generic argument is established prior art: a quadratic speedup of an exponential-time classical algorithm gives exponentially growing absolute savings, but break-even arrives late (Campbell-Khurana-Montanaro 2019; Sanders et al. 202

## QM-05: Fault-tolerant cost of one coherent walk/gradient step for the esmprior/A80 energy (and all-atom physical energies), and the landscape-independent break-even T* = a^2 P C_q^2 / C_c

### Lens: classical (verdict: KILL)
- **Theoretical level:** L6 only for the generic quadratic walk-step/query separation in an explicit oracle model: Szegedy 2004 [#1]; Somma et al. PRL 101, 130504 (2008) [#8]; continuous hide-and-seek Omega(alpha) vs O~(sqrt alpha) in Olivucci et al. arXiv 2608.24527 [#39, preprint]. That separation is not instance-established and gives no super-quadratic mechanism. For the esmprior/A80 instance family it is L0: the spectral gap of any chain on this energy has never been measured. The gradient-query card is below L0 for a white-box energy, since classical reverse-mode AD already costs O(1) energy evaluations.
- **Practical level:** L0. The L5 (hardware-realistic) costing is negative. The break-even is at least about 1.6e11 gradient steps or 7e11 Metropolis steps per independent sample, at P=1 and an optimistic 1e6 Toffoli/s. Measured classical budgets on this energy are 5 to 7 orders of magnitude smaller.
- **Strongest pro-quantum rebuttal considered:** The classical global search on this energy may not be saturated at L >= 80, so K(L) could grow exponentially. Two uncommitted, in-progress G1 results point that way. First, the mode census at L=80-120 finds about as many distinct minima as restarts (n_modes 150-256 of 256), and the best mode is often hit only once (p_best 0.004). Second, the HREX pilot made 0 round trips in 3.7e5-5.6e5 gradient evaluations at L=45-150. If K(L) is exponential, then at some L_c even a quadratic gain beats any fixed K*.

Rebuttals:
(a) Take the most generous version: amplitude amplification over coherent L-BFGS descents. One descent is about 200 x 7.6e7 = 1.5e10 Toffolis, about 1.5e4 s at 1e6/s. The classical descent is about 32 ms compiled. That gives R ≈ 5e5, so break-even needs 1/p ≈ 2e11 restarts, about 200 CPU-years per target at P=1. Multistart is embarrassingly parallel, and T* grows linearly with P.
- **Evidence (abridged):** The classical adversary is not one algorithm. It is the portfolio compiled or GPU ΔE + HMC/underdamped Langevin (lifted chains) + PT/HREX + multistart L-BFGS with Laplace reweighting + reverse-mode AD.

1) Key derivation: K* does not depend on L or on move type. When the quantum and classical sides evaluate the same pair terms:
   R = C_q/C_c ≈ (2 · c_pair / R_T) / t_pair
   The factor 2 is because the quantum side computes old+new pair terms in superposition, while the classical side caches the old ones. So
   K* = (2 a P c_pair / (R_T t_pair))^2
   With c_pair ≈ 2e3 Toffolis (compute+uncompute), R_T = 1e6/s, t_pair = 5 ns and a = P = 1: K* ≈ 6.4e11 pair-move steps, for any L and for crankshaft or pivot. T* = K* · C_c then grows as L (crankshaft) or L^2 (pivot).

2) Independent Toffoli model (I(agent), b=16 fixed point):
   - Per pair term, about 1.9e3 Toffolis to compute and about 3e3 with uncompute: 3 subtractions (48), 3 squarings (768), adds and clamp (100), a segment QROM of 64 entries for a cubic spline in d^2 (64), Horner (768).
   - Arithmetic dominates, not table loading. This agrees with the card's correction that per-pair learned tables are not the cost driver.
   - Per step:

| Step | L=60 | L=100 | L=150 |
|---|---|---|---|
| Crankshaft (CA_i plus 3 CB rows, old+new) | 9.3e5 | 1.6e6 | 2.4e6 |
| Pivot, classical k (measured mean affected pairs 640 / 1751 / 3924) | 5.4e6 | 1.45e7 | 3.2e7 |
| Pivot, superposed k | 1.3e7 | 3.8e7 | 8.7e7 |
| Coherent gradient (about 

### Lens: resource (verdict: KILL)
- **Theoretical level:** L6, inherited and quadratic only. The Szegedy/QSA spectral-gap speedup and the Olivucci 2026 continuous-Gibbs Omega(alpha) vs O~(sqrt(alpha)) separation are provable query-model results [A44, A45, A55], but both are quadratic. QM-05 adds no speedup of its own; it is a resource audit at L0/L3. No super-quadratic mechanism exists for this energy class.
- **Practical level:** L0. The L3 (resource-normalised) and L5 (hardware-realistic) accounting both come out negative. Take the cheapest faithful A80 step (a single-bead local move at L=100), a=P=1, and an optimised classical twin. The break-even time is T* ~1.2 years at an optimistic 1e6 Toffoli/s and ~3.5e4 years at the Babbush/Sanders base rate (one factory, 170 us per Toffoli). Every other card (pivot, gradient, phase oracle, all-atom) is worse by 1 to 12 or more orders of magnitude.
- **Cost / break-even note (abridged):** Landscape-independent R = C_q/C_c at L=100 (optimised classical):
- A80 local card: R ≈ 5e6 at 1e6 Toffoli/s and ≈ 9e8 at one factory.
- K* ≈ 3e13 and 8e17 respectively.
- T* is 1.2 years at best (a = P = 1), and it grows about linearly with L.

Every quadratic walk, QSA, Langevin or gradient-query card on the esmprior/A80 energy therefore fails early fault-tolerant break-even at L = 60–150. The all-atom variant fails by at least 12 orders of magnitude.

Keep this cost model as the gate for QM-01/02/04/12/13/18. Any future card must show c_pair·n_pass/(r·t_pair) ≲ 1e3 before any landscape argument matters.

Scratch artefacts: C:\Users\abena\AppData\Local\Temp\claude\C--Users-abena-quantum-advantage-protein-folding\deded8ee-ac50-420b-a8f2-b349dc3a4fdc\scratchpad\qm05_cost.py, qm05_classical.py, tpair.py, qm05_classical.json, qm05_cost.json.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** The query statement is inherited at L6 and is not new: the qubitised/Szegedy walk and QSA give a provable quadratic step-count gain in the spectral gap, but only relative to the quantised chain, not relative to the best classical sampler. QM-05 itself adds only a resource-normalised (L3-type) cost, and that cost is negative. The in-repo derivation T3 v1 (C:\Users\abena\quantum-advantage-protein-folding\research\theory\RESOURCE_MODELS.md, untracked, 2026-09-27) gives, per qubitised step: faithful torsion target about 2.3e4*L^2 Toffolis (2.3e8 at L=100; 4.8e7 in the generous variant); Cartesian 
- **Practical level:** L0. There is no configuration at L=60-200 in which a quadratic walk or query card breaks even inside 1 week against even an 8-core adversary. At L=100, with T* = P*(G/r)^2/C_c: the most generous design (D3 generous, G=1.1e7), the optimistic rate r=1e6 Toffoli/s and matched C_c=10 us give T* = 0.38 yr (P=1), 3.1 yr (P=8) and 380 yr (P=1e3). The r=1e6/s rate already exceeds the 10-100x parallel-factory cap in Babbush et al. by about 10x. At the realistic r of about 6e4/s (10 CCZ factories at 170 us each), T* is about 108 yr at P=1. Faithful designs (D2 generous or central) give 7.3-170 yr at P=1
- **Novelty note (abridged):** My search found no evidence of a published fault-tolerant, Toffoli-level cost for a coherent Metropolis or walk step on a continuous pair-distance protein energy (learned or physical). It also found no coherent Lennard-Jones plus erfc-Ewald Toffoli count for classical molecular dynamics. Scope of that search: about 12 arXiv-API keyword queries covering 2019-2026, plus repository bibliography checks. The general web-search budget was exhausted this session, so coverage is partial. The method is not new: it follows the Sanders 2020 template and the Babbush 2021 T* algebra, and Incudini and Mazzola 2026 and Escrig et al. 2026 are the nearest compiled analogues, on Ising and integer linear programming. Relative to this repository, novelty is close to zero. T3 v1 already covers about 80% of QM-05: G(L) for 3 designs x 2 walks, representation and fit checks, SVD rank, the coin, B(L), T*, physi

## QM-06: Screening no-gos: consumption-factoring theorem with per-primitive quadratic ceilings (generalised H-001, GHV/LWWZ exception) and cheap-gradient dequantisation of quantum gradient estimation

### Lens: classical (verdict: KILL)
- **Theoretical level:** Advantage on the protein-relevant instance family (A80/esmprior-type white-box pairwise learned energies): L0. What the no-go supports is a ceiling, not an advantage. Per-primitive quadratic query separations are real and tight at L6: sqrt(N/k) min-finding, sqrt(1/P_acc) rejection, 1/eps vs 1/eps^2 estimation, and in-repo T5 Theorem A, which shows Olivucci's Omega(alpha) vs O~(sqrt(alpha)) is exactly quadratic. But they hold only in the query model and only on information-local (hide-and-seek) families, or for quantum algorithms that call E through black-box AA, walk or QAE primitives. As lite
- **Practical level:** L0. Nothing survives resource normalisation on this instance family.
- Gradient estimation is dequantised by measurement. For A80, cost(E + grad E)/cost(E) was 1.6-3.6 (median about 2.0) at L=30/60/120/240 (d=55/115/235/475). Jordan/GAW's nominal d-fold gain therefore collapses to at most about c/2, roughly 1-1.8x in operations, because Jordan needs at least a compute and an uncompute evaluation at extra precision. That comes before a fault-tolerance slowdown of 1e3-1e6 per logical operation.
- Min-finding: restart saturation at 32-64 L-BFGS restarts caps any Grover/Durr-Hoyer gain over restar
- **Strongest pro-quantum rebuttal considered:** 1. The no-go cannot be unconditional where it matters. A80 is a white-box energy: all O(L^2 x 1001) table entries are known. Query lower bounds say nothing about white-box time complexity (T5 S10). So QM-06 rules out only the known black-box primitive families, not a cleverer quantum algorithm that exploits structure nobody has found yet. It is also internally falsified as worded, by T5 C1 (a smooth, Simon-structured energy with exponential sampling separation).
2. The LWWZ exception is not closed. Verified from the arXiv HTML on 2026-09-27: its continuous classical lower bound is stated for function-value queries only ("exp(n^{Omega(1)}) queries to f(.)"), and the paper does not discuss gradients. Whether it survives derivative queries is open. It plausibly does, if each derivative query can be simulated by a few GHV adjacency-list queries, but that is not proved.
3. The quadratic ceili
- **Evidence (abridged):** Measured (this run). Script: C:\Users\abena\AppData\Local\Temp\claude\C--Users-abena-quantum-advantage-protein-folding\deded8ee-ac50-420b-a8f2-b349dc3a4fdc\scratchpad\grad_cost2.py, using the vendored src/qapf/protein/energy.py (A80) with synthetic Dirichlet tables; timing does not depend on table values. Setup: 1 torch thread; the machine was at 76-80% background load, so forward and gradient timings were interleaved and medians taken.

Ratio t(E + grad E)/t(E), with IQR, per structure:
| L | batch 1 | batch 32 | per-structure cost (batch 32) |
|---|---|---|---|
| 30 | 3.64 [2.4-3.7] | 2.79 [1.4-3.2] | about 0.26 ms forward |
| 60 | 3.37 [1.9-4.6] | 1.86 [1.4-2.2] | 0.75 ms forward, 1.4 ms gradient |
| 120 | 2.22 [1.8-2.9] | 1.78 [1.5-2.1] | |
| 240 | 1.62 [1.3-2.2] | 1.59 [1.4-1.8] | 11.6 ms forward, 18.4 ms gradient |

A finite-difference gradient would cost d+1 = 56-476 evaluations. Kill criterion (iii), "gradients cost >> c*S", fails: c is at most 3.6. A80 is also only piecewise-linear in distance (table interpolation on a 0.05 Å grid), so it is not Gevrey-smooth, and GAW's quadratic precision gain does not provably apply.

Verified via arXiv API or Crossref, 2026-09-27:
- Baur & Strassen, "The complexity of partial derivatives", TCS 22:317-330 (1983), DOI 10.1016/0304-3975(83)90110-X. Crossref metadata only; the constant 3 multiplications / 5 total operations is UNVERIFIED.
- Jordan, PRL 95, 050501 (2005), DOI 10.1103/PhysRevLett.95.050501.
- Gilyen, Arunachalam, Wiebe,

### Lens: resource (verdict: KILL. None of the quantum routes QM-06 covers survives resource accounting. The no-go itself is UPHELD as a screening ru)
- **Theoretical level:** As a quantum-advantage claim: L0. The only positive content is the quadratic query-model separation, which is the ceiling itself.

As a no-go, per part:
(i) L6 in the black-box query model, primitive by primitive, for information-local families: min-finding Theta(sqrt N) (BBBV/Durr-Hoyer); mean estimation Theta(1/eps) against Theta(sigma^2/eps^2); hide-and-seek sampling T_Q >= Omega(1/sqrt(p_max)) (T5 Lemma 1).
(ii) The composition lemma is L6 only where the composed task is Boolean function evaluation, because the adversary bound composes there (Reichardt / Lee-Mittal-Reichardt-Spalek-Szegedy
- **Practical level:** L0 for advantage. The negative result is resource-normalised (L3-grade), using the measured classical cost t_C(L) and the per-step Toffoli counts G(L) from T3.

Measured on the vendored A80 energy (src/qapf/protein/energy.py), random-table timing, 1 thread, float64, machine at about 74% background load (which makes the classical side look slower, i.e. favours quantum). Batch B=16, value+grad per structure, and c = cost(value+grad)/cost(value):
- L=30: 0.82 ms, c=3.3
- L=60: 0.93 ms, c=2.35
- L=100: 2.0 ms, c=1.59
- L=150: 5.8 ms, c=1.53
- L=240: 20.2 ms, c=1.92
At B=1, c = 5.5, 4.2, 4.4, 2.75,
- **Cost / break-even note (abridged):** Break-even by primitive, with measured single-thread t_C and T3 G(L). A coherent full-energy evaluation costs about G/2 Toffolis, i.e. 1.05e7-2.6e8 for D2 at L = 30-150: 30 minutes to 12 hours at 170 µs per Toffoli with one factory.

- **Durr-Hoyer (min-finding):**
  - Against exhaustive enumeration: N* = (11.25*t_Q/t_C)^2 = 6.5e15-4e16 at R=1 (T* = 5e4-2e6 years), and 6.5e11-4e12 at R=100 (T* = 5-200 years).
  - Against the real classical adversary, L-BFGS multistart saturated at 32-64 restarts: quantum needs 81-115 coherent decodes against 32-64 classical ones. There is no crossover at any hardware speed.
- **Jordan/GAW (gradient):** the query gain is at most c (5.5 or less) against AD. The per-query hardware ratio t_Q/t_C,grad is 2e6-1e7 (170 µs, R=1), 2e4-1e5 (R=100), and 130-580 (1 µs, R=100). No crossover at any L, because both costs scale as L^2.
- **QAE:** needs sigma/eps >= t_Q/t_C, i.e. relative precision of 1e-4 to 1e-7, far below the model/information floor.
- **Rejection / amplitude amplification:** needs P_acc <= (t_C/t_Q)^2 ≈ 1e-8 to 1e-14. It is also not the classical adversary's method; MCMC/HREX is.
- **Qubitised walk (the only non-dead case):** B = 3e7-4e14 at 17

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for any quantum advantage, since the candidate is a no-go by design. As a negative result, parts (1) and (2) sit at the L6-negative level, but only in the black-box query model, and T1 and T5 already hold both parts: T1 has Theorems 1–3 and the Dürr–Høyer ceiling on OPT/TOP_m; T5 has S1–S5 and states the exceptions in S6–S11. Part (3), the composition lemma, adds little: (Σ√C_i)² ≥ ΣC_i and Π√C_i = √ΠC_i. It covers only pipelines built literally from the listed primitives, and says nothing about non-compositional algorithms such as the GHV/LWWZ adiabatic paths. Part (5) is textbook, and I h
- **Practical level:** L0. The no-go leaves the one live route (walk/QSA/continuous-Langevin sampling of a learned-energy posterior at ≥60 aa) unchanged. That route was already accepted as at most quadratic, and whether it survives depends on G1 (classical mixing cost) and G2/B(L) (break-even), neither of which QM-06 touches. The only protein-realistic number it produces is the cost of a gradient relative to one energy evaluation for A80. I measured that here (1.45–4.3x), and it only confirms that Jordan/Gilyén–Arunachalam–Wiebe gradient estimation is pointless against a white-box energy. No proposal in the program 
- **Novelty note (abridged):** Scope of the search: the repo's 448-paper literature map, the in-repo theory notes T1, T2, T4 and T5, and arXiv abstract/HTML/API checks of 9 papers this session. The web-search budget was exhausted, so no broad 2019–2026 web sweep was done this session.

Under that scope, the search found no evidence of a published paper that packages a consumption-factoring lemma plus per-primitive quadratic ceilings as a screen for quantum stages acting on learned protein energies. Every ingredient is known, though:
- post-processing and data-processing invariance;
- BBBV / Dürr–Høyer / Somma–Boixo / quantum mean-estimation bounds;
- the cheap-gradient principle (Baur–Strassen; not re-verified here);
- the fact that quantum convex-optimisation gains come from evaluation-only oracles via Jordan-type gradients (CCLW 2020, vAGGdW 2020);
- the absence of quantum speedup under first-order or higher-order o

## QM-07: Tensor-network / treewidth / Schmidt-rank dequantisation audit of the coherent posterior |sqrt(pi)> (including the 'low-treewidth contact graph' false friend)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0. The card makes no quantum-advantage claim. Its one-way classical statement holds: if chi = poly(L), exact MPS sampling costs O(L chi^2 d) per sample with no mixing (Ferris-Vidal-type perfect sampling). The converse does not hold. By the Holevo bound, S_vN(rho_A) of |sqrt(pi)> is at least the classical mutual information I_pi(A:B), so chi >= ~e^I. A single Gaussian basin, which HMC or a Laplace fit samples in polynomial time, already has chi of about e^I. High chi is therefore not evidence of glassiness or classical hardness, and the clause 'volume-law chi reopens QM-01 sqrt(delta)' should 
- **Practical level:** L0. As specified, the test cannot give a valid kill signal or a valid survival signal on this instrument (see evidence). It has close to zero decision value for the quantum-sampling line. That decision belongs to G1 (the K-G1b census bypass and T_cal round trips) and G2 (B(L)).
- **Strongest pro-quantum rebuttal considered:** 1. A hybrid might still be a useful classical sampler: a TN over coarse labels (bins or topology), with within-bin continuous positions handled by HMC plus exact MH/IS correction, could estimate inter-basin masses better than PT at T_cal. A high coarse-label chi might then mean something about many-mode structure. Reply: the weight of a coarse bin string is a (2L-5)-dimensional continuous integral. It cannot be point-evaluated, so TT-cross over it is not cheap, and the IS weights inherit the 500-10^4 kT rounding mismatch measured below.
2. My numbers come from pilot samples at T=1 only: one unmixed NRPT top rung (0 round trips), n = 80-240 autocorrelated samples, and Ledoit-Wolf shrinkage. Gaussian MI is an estimate, not a rigorous lower bound, and at T_cal the posterior differs. Two points stand regardless: the rounding error is deterministic, and the Holevo/Mehler argument does not dep
- **Evidence (abridged):** DERIVATION (Holevo). For |psi> = sum sqrt(pi(a,b))|a>|b>, rho_A = sum_b pi(b)|phi_b><phi_b| with phi_b = sum_a sqrt(pi(a|b))|a>. Measuring in the computational basis then gives I_pi(A:B) <= chi_Holevo = S(rho_A) <= H(A). So log chi >= I_pi(A:B).

MEHLER CHECK (numerical, scratchpad/schmidt_check.py). For sqrt of a bivariate Gaussian, the Schmidt ratio is q = ((1-sqrt(1-rho^2))/rho)^2. It matches the SVD to 4 decimal places at rho = 0.5, 0.9, 0.99 and 0.999. chi(99%) = 2, 5, 17, 52, which is about 2.3 e^I per mode, and S_vN >= I held at every rho. So one smooth basin with m correlated cross-cut modes has chi ~ exp(sum I_i).

DEP AUDIT (no natives). Inputs: ladder crops, λ=1, T=1 pilot samples, vendored A80 energy (scratchpad/qm07_audit.py, qm07_audit_rows.txt, mi_cut.py, mi_cut.json).
(a) Discretisation fidelity. Rounding (theta,tau) to the head's 9x24 = 216-class grid changes E by a median of 500 / 561 / 7,468 / 9,870 kT at L = 45 / 60 / 100 / 120. The 54-class grid gives 1,977 / 2,072 / 12,745 / 17,146 kT. Moving a single coordinate by half a bin (7.5 deg) costs a median of 12-79 kT, and 88-97% of coordinates change by more than 1 kT. The card's discrete object is a different distribution from the posterior.
(b) Lever arms. The median is 14-16 A/rad and the maximum 25-30 A/rad. Resolving 0.5 A needs 1.7-2.1 deg (p10: 1.2-1.3 deg), which is about 6x10^3 - 9x10^3 classes per residue (p90: 1.1-1.6x10^4), not 216.
(c) Treewidth. In the prior factor graph, 100% of pairs vary by m

### Lens: resource (verdict: KILL. There is no speedup by construction, so QM-07 is not a route to quantum advantage. Keep it only as a one-sided cla)
- **Theoretical level:** L0 for quantum advantage.

What the card actually has:
- Its only theorem is a sufficient condition for DEQUANTISATION: if the Schmidt rank across every sequence cut is chi, the discretised posterior can be sampled exactly and classically at O(L chi^2 d) per sample, with no mixing (the standard sequential/perfect MPS sampling argument).

Quantum levers inside the card's scope:
- **Amplitude amplification of a tensor-network proposal q to the exact posterior** (quantum rejection sampling, [A36]).
  - With log-normal weights, ESS/N ≈ exp(-2·KL_tot). So classical correction costs about e^{2KL} pr
- **Practical level:** L0.
- **Where the card's kill fires (low chi):** every quantum route is about 1e4–1e7× slower per sample than the classical MPS sampler.
  - Loading the MPS takes 1.5e7–2.5e10 Toffolis, about 43 min to 49 days on one factory, versus 0.17 s for a classical sample.
  - A single qubitised walk step at L=60 (T3 G(L) = 6.5e6–8.2e7 Toffolis) takes 11 s (D3 generous, R=100) to 3.9 h (D2 central, R=1). A complete exact classical sample (MPS proposal plus importance-sampling correction, chi=256, d=216, 400 proposals) takes about 68 s on one core.
- **Where it does not fire (high chi):** the problem rev
- **Cost / break-even note (abridged):** This is the oracle and state-preparation account for the quantum routes inside QM-07's scope, at L=60 with χ=256, d=216 and b=20 unless stated. Hardware assumptions are T3's: 170 µs per Toffoli, one factory, 2(d+1)² = 2048 physical qubits per logical qubit at d=31.

**Routes 1–3: loading the classical object costs more than sampling it.**

1. **Loading |√q⟩ from the fitted MPS.** State preparation is not free.
   - Optimistic cost (multiplexed rotations with QROAM angles): 1.5e7 Toffolis per copy, about 43 min at R=1. For χ=64, d=54 it is 1.9e6 (5 min).
   - Generic isometry synthesis (about χ²d rotations per site): 2.5e10 Toffolis, about 49 days.
   - Logical qubits: about 1.8e4 (480 system, 8 bond, about 1.7e4 QROAM ancilla).
   - The 2.1 GB of tensor data must be computed classically first. That is the same object the classical twin samples from in 0.17 s.
   - Quantum/classical time ratio per sample: 1.5e4–2.5e7. One measurement gives one sample, so there is no lever.

2. **Quantum rejection sampling from the tensor-network proposal to the exact posterior [A36].**
   - A coherent q(x) needs select-and-multiply contraction: L·χ²·b² = 1.6e9 Toffolis. Add the coherent energy (D2) 

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for any quantum claim. By design the card claims no speedup; it is a dequantisation test. Its theory content is textbook and correct at L0/L1 on the classical side: the Schmidt rank of |sqrt(pi)> equals the rank of the matrix sqrt(pi(a,b)) (Vidal 2003), and Arad-Landau's additive error is useless for positive Boltzmann tensor networks. The interval-scope treewidth correction is right, and it is decided on paper. The A80 energy has a -log p~(d_ij) term for every pair with |i-j|>=3, so pair (1,L) alone puts every (theta,tau) variable in one factor scope. The primal graph is complete and the t
- **Practical level:** L0. Nothing has run, and three prerequisites are missing.
(1) T* is undetermined: the G1 T-scan has no processed output yet.
(2) The reference PT samples are not trustworthy. In the G1 pilot (exploratory, T=1, lambda-path NRPT) there were 0 round trips at every L = 45, 60, 100, 120, 150 (Lambda = 14-29; 0.37-0.56M gradient evaluations per crop).
(3) The card as written is statistically underpowered and runs past its budget.
- At d=216 and chi=256, one MPS core has d*chi^2 = 1.4e7 parameters (8.5e8 over L=60), against 1e5 samples. Held-out NLL can resolve chi only up to about sqrt(N/d), roughly
- **Novelty note (abridged):** The concept is not new. Dequantising a polymer or protein qsample with an area-law tensor network was done for compact lattice polymers by Rattacaso et al. 2026 (arXiv 2603.12334, already in the program bibliography as D40). Coherent classical Gibbs states as area-law PEPS go back to Verstraete et al. 2006. MPS/TT sampling of specified densities was established by Ferris & Vidal 2012, Han et al. 2018, Dolgov et al. 2020 and Cui & Dolgov 2022. TT over molecular torsions was established by Nuske et al. 2016 and Zurek et al. 2025. Tree decomposition and GBP for protein side chains are well established (Xu et al. 2005; Kamisetty et al. 2008). One recent adjacent paper is not in the bibliography: Kodama et al. 2026 (arXiv 2608.21700). Possibly new, narrowly: an empirical chi*(L) scaling for a learned, ESM-derived, off-lattice posterior in sequence-order internal coordinates at 60-150 aa. The 

## QM-08: Posterior as a ground state: stoquastic parent Hamiltonians are exactly Markov chains, amplification stops at sqrt(delta), non-stoquastic parents open

### Lens: classical (verdict: KILL)
- **Theoretical level:** Level 0 for any advantage that is QM-08's own. The candidate left one item open: (iv), a local non-stoquastic parent H' of |sqrt(pi)> with gap much larger than sqrt(delta*). An existing theorem closes it, so this is a proven negative result (a Level 6 no-go), not a Level 6 advantage.

- The fixed-node lemma (ten Haaf et al. 1995; Bravyi-Carleo-Gosset-Liu 2023, Lemma 2) applies to any parent with a strictly positive ground state, and sqrt(pi) > 0. It gives a stoquastic F = H' + (PSD terms) with the same ground state, the same move graph (a subset of the edges) and gap(F) >= gap(H').
- BCGL Theo
- **Practical level:** Level 0. Nothing shows the idea is useful even under matched conditions. At the proposed test size (6-8 residues, at most 4,096 states), exact enumeration costs about 4e3 energy evaluations, under 1 ms. The ceiling is quadratic and each coherent call to the Delta-E oracle carries the candidate's own overhead factor R of about 1e7-1e10. That puts break-even beyond 1e14 classical steps per independent sample, before any fault-tolerance overhead.
- **Strongest pro-quantum rebuttal considered:** The best cases for keeping QM-08 alive, and why each fails:

1. **Parents local only in an entangling (non-product) basis.** Take H' = U K U†, with K local and U a non-local circuit. H' is dense in the computational basis. Its rotated ground state U† sqrt(pi) generally has amplitude ratios that cannot be computed, so the BCGL chain cannot be built. This is a real loophole. But it is not QM-08's construction ("local parent built from pair tables"). It is generic qsampling, which is SZK-hard in general (Aharonov-Ta-Shma 2003), and no efficient U, K for pair-additive or learned energies is known. Prior: very low.

2. **Weak spots in BCGL itself.** The classical cost scales as eps^-1, not log(1/eps). Theorem 2 also needs a "good" starting state, which is shown to exist and can be checked efficiently but is not constructed. Both are polynomial caveats. The quantum side pays worse: phase estim
- **Evidence (abridged):** **Sources (verified by fetching the arXiv/PDF text this session; the web-search quota was exhausted, so fetches were used instead)**

1. Bravyi, Carleo, Gosset, Liu, "A rapidly mixing Markov chain from any gapped quantum many-body system", Quantum 7, 1173 (2023), arXiv:2207.07044. Read from the full text:
   - Eq. 12, the fixed-node Hamiltonian: set sign-violating off-diagonals (S+, where psi_x H_xy psi_y > 0) to zero, and add H_xz psi_z/psi_x to the diagonal.
   - Lemma 2: F and H have the same ground state and ground energy, and lambda2(F) >= lambda2(H). The proof is <phi|F-H|phi> = 1/2 Σ_{S+} |H_xy| |sqrt(psi_y/psi_x) phi_x - s·sqrt(psi_x/psi_y) phi_y|^2 >= 0.
   - Theorem 1: ||pi_t - pi||_1 <= e^{-gamma t}/sqrt(pi(x_in)).
   - Lemma 4 / Eq. 28: mean Gillespie flips = -t<psi|F_od|psi> <= t·max_x Σ_y |H_xy|.
   - Theorem 2: cost O(eps^-1 n^2 k ||H|| gamma^-1 log(1/(eps pi*))).
   - Lemmas 2-3 do not use locality. Theorem 2 uses only row sparsity, so it extends to any s-sparse H with rows that can be computed efficiently.
   - For sqrt(pi) > 0, S+ is simply the set of positive off-diagonals, and ratios are exp(-beta ΔE/2), the same oracle the quantum block encoding needs.
2. ten Haaf, van Bemmel, van Leeuwen, van Saarloos, Ceperley, PRB 51, 13039 (1995): the original fixed-node bound (BCGL ref. 8).
3. Bravyi-Terhal, SIAM J. Comput. 39, 1462 (2009), arXiv:0806.1746: stoquastic frustration-free Hamiltonians correspond to random walks (item ii).
4. Castelnovo, Chamon, Mudry, Pu

### Lens: resource (verdict: KILL)
- **Theoretical level:** Advantage supported: at most quadratic, and the quadratic is not specific to QM-08. For stoquastic parents the proven result sits at the top of the negative scale (L6-negative): the gap equals a reversible Markov-chain gap exactly (Bravyi-Terhal/SMF similarity), and Somma-Boixo sqrt(delta) amplification is optimal in the black-box model. This is the same quadratic as the existing QSA/Szegedy lane (L6 query model, walk steps only). The novel part, item (iv) (non-stoquastic parents with gap >> sqrt(delta*)), is now refuted at L6-negative by a derivation in this audit: every real-symmetric (or He
- **Practical level:** L0. No hardware-realistic or resource-normalised advantage. The best route is the stoquastic Metropolis parent via a qubitised walk plus gap amplification, which is just the QSA lane. It inherits the T3 break-even at L=60: B >= 9.6e8 to 1.6e17 classical energy+gradient evaluations per independent sample. The only measured classical cost is a lower bound: the G1 pilot saw 0 round trips in 3.4e5 evaluations at L=60. There is no evidence it approaches B. The non-stoquastic and guided-QPE variants are strictly more expensive (see the break-even note).
- **Cost / break-even note (abridged):** QM-08's cheapest route is the stoquastic Metropolis parent plus gap amplification. That is the qubitised QSA walk, so it inherits T3's B(L) = kappa c_q^2 (S G t_T/(R t_C))^2.

At L=60 (kappa = c_q = 1):
- D2 central: B = 1.6e15 evaluations with S=1, R=1 (break-even runtime T* = 1.75e4 years); 1.6e11 with R=100 (T* = 1.75 years); 1.6e17 with S=1e3, R=100 (T* = 1.75e3 years).
- Most generous case, D3 generous with R=100, S=1: B = 9.6e8, T* of about 4 days. That samples a different, bond-relaxed target with unknown kappa.
- With T2's walk-overhead c_q = K*l in [90, 1.6e4], B grows by a further factor of 8e3 to 2.6e8.

Non-stoquastic parents only add cost:
- There are no 2-local parents, so the terms are Theta(L)-body. Every entry must encode sqrt(pi_y/pi_x), i.e. a coherent Delta-E, which puts each query at the G(L) scale.
- Sparse-access normalisation alpha = s ~ 4L-10 = 230 (versus 1 for the walk) means up to 230x more queries and about 5e4x in B.
- Building an optimised H' needs an SDP over q^n states (81 states already took 200-300 s; torsion space at L=60 is about 16^120), which violates the no-free-block-encoding rule.

Guided QPE from the product prior costs a further 1/gamma =

### Lens: relevance (verdict: KILL)
- **Theoretical level:** There is no level for a positive claim. Only L0 (formulation) is reached. The negative result is at L6 in the amplitude-ratio model. Parts (i) to (iii) are prior art, and (i) is already DERIVED in the repo (T2 §3.5). The OPEN item (iv), whether a non-stoquastic parent could beat sqrt(delta), is closed negatively by an existing theorem.

Take any real, sparse or k-local H' whose unique ground state is |sqrt(pi)>, with any sign pattern. Build the fixed-node Hamiltonian F from it (Bravyi-Carleo-Gosset-Liu 2023, Lemma 2). F is stoquastic in the psi>0 basis, F >= H', F has the same ground state, an
- **Practical level:** L0. Nothing has been built or measured, and nothing is justified. Any practical value would be inherited from M1 (quadratic, fault-tolerant, the B(L) break-even at roughly >=1e12 classical steps per independent sample), and M1 is still gated on G1/G2. Two design facts make the proposed test worse, not better:

1. For all-to-all pair energies, no 2-local parent exists at the proposed sizes. This was checked numerically. At L=6, q=3 and q=4, the null space of the map from 2-local operators to H|sqrt(pi)> is 134 and 230 dimensions. Those numbers equal exactly the trivial redundancy count: identit
- **Novelty note (abridged):** Not novel. (i) is Rokhsar-Kivelson/SMF (Henley 2004; Castelnovo et al. 2005), coherent-Gibbs PEPS (Verstraete et al. 2006) and QSA (Somma et al. 2008), and it is already in repo T2 §3.5. (ii) is Bravyi-Terhal 2009. (iii) is Somma-Boixo 2013. The "open" item (iv) is answered, in the negative, by Bravyi-Carleo-Gosset-Liu 2023 (fixed-node Lemma 2), which the literature phase missed.

Recommend recording QM-08 in research/KILLBOOK.md Section B as "killed by theorem (BCGL 2023 Lemma 2 + Bravyi-Terhal 2009 + Somma-Boixo 2013); residual quadratic merged into M1". Reopen condition: a non-ground-state or non-classical-ratio path construction, instantiable on protein learned energies. Also add arXiv:2207.07044 to the bibliography.

## QM-09: Transfer test for the only super-quadratic classical-objective separations (GHV -> LWWZ QHD) and exponential walk traversal of conformational graphs (glued trees, hierarchical graphs)

### Lens: classical (verdict: KILL)
- **Theoretical level:** For protein-realistic instances: L0 (formulation only). No protein energy or conformational graph is known to realise the constructions, and the probe below finds that small protein-like graphs have none of the needed structure. L6 (provable, query model) holds only for synthetic oracle instances: Childs et al. welded trees, GHV, LWWZ, and BLH hierarchical graphs. All of them rely on hidden random vertex labels, value-only queries, and an f whose implementation cost is ignored.
- **Practical level:** L0. Even a perfect transfer gives no practical advantage at any protein size, because of the subexponential exponents (see break_even_or_cost_note). CTQW on real small instances does no better than uniform random guessing (numbers below).
- **Strongest pro-quantum rebuttal considered:** (1) No theorem says explicit, bounded-description gapped stoquastic Hamiltonians are classically easy. Whether white-box stoquastic adiabatic computation is in BPP is open. BCGL gives a classical chain only when ground-state amplitude ratios can be computed, and for a generic stoquastic ground state they cannot. The general classical simulators have documented failures: PIMC/QMC (Hastings-Freedman 2013, topological obstructions) and DMC (Jarret-Jordan-Lackey 2016). Hamoudi et al. 2026 extend classical hardness to any guided algorithm, even with the best warm start, though still in the oracle model. (2) Pair-additive 3D energies can encode NP-hard problems and circuit gadgets. So the description-complexity barrier (ii) is a heuristic, not a no-go. In torsion coordinates, a pair term d_ij couples all 2|i-j| internal coordinates between i and j, so 'low body order' is not literally true. (3
- **Evidence (abridged):** CLASSICAL ADVERSARY, in order of strength:
(A) Explicit-naming dequantisation. Every known exponential walk or stoquastic separation (Childs et al. STOC 2003, quant-ph/0209131; Balasubramanian-Li-Harrow, CMP 406:209 (2025), arXiv 2307.15062; Gilyen-Vazirani arXiv 2011.09495, the GHV line; Hastings, Quantum 5:597 (2021), arXiv 2005.03791) works the same way. Ballistic transport runs through a poly-dimensional invariant subspace spanned by column (supervertex) indicator states. Classical hardness comes only from a random injective label map Enc, which BLH state explicitly, so the column index cannot be read. With explicit coordinates and a known move group, the column index is whatever function the model exposes (energy, contact number, Rg, SS content), and two classical algorithms then work. (i) Greedy column ascent: O(depth) steps. (ii) The Bravyi-Carleo-Gosset-Liu continuous-time chain (Quantum 7:1173 (2023), arXiv 2207.07044). Its mixing time is controlled by 1/gap, and it can be implemented whenever <y|psi>/<x|psi> is computable. For column-symmetric states psi(x)=phi_{c(x)}/sqrt(N_c), with phi from a poly-size tridiagonal reduced chain and c computable, the ratios are computable, so the adiabatic path is classically trackable in poly time.
(B) Exponent bookkeeping (my derivation from the verified LWWZ arXiv 2504.14841, Theorem 4.2): m = n^{16/5-o(1)}, the classical lower bound is exp(n^{1/5-o(1)}), and the objective dimension is N = Theta(m). That gives exp(N^{1/16-o(1)})

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for protein-realistic energies and conformational graphs. The L6 query separations (GHV, LWWZ, Childs et al. glued trees, Balasubramanian-Li-Harrow) exist only for artificial black-box instances with hidden random labels. No part of them transfers to an explicit, public energy. Even in their own oracle model, GHV/LWWZ prove only exp(n^{1/5-o(1)}) classical queries, and at protein sizes that bound is 13 to 190 queries.
- **Practical level:** L0. No instance, no gap guarantee, no classical lower bound. One coherent A80 phase-oracle call already costs about 1e5x more wall-clock time than the entire proven classical lower bound would at protein size.
- **Cost / break-even note (abridged):** Two independent reasons put break-even out of reach.

(1) The oracle removes the speedup. Every super-quadratic separation is a query lower bound that depends on hidden random labels. A LWWZ quote verified this session says the oracle 'ignores the complexity of implementing f'. A public learned energy with explicit coordinates has no hidden labels, so there is no classical lower bound to beat. The operative break-even falls back to the quadratic T3 value B = 1.5e11 to 1.5e17 evaluations (at least 1.3e8 in the most generous case).

(2) Even in its native oracle model, GHV's delta = 1/5 makes the crossover astronomical: n* ~ 1.4e9 qubits at ~1e29 queries, about 5e17 years at 170 us per Toffoli. At protein sizes the proven classical bound is 13 to 190 queries (milliseconds of CPU), while one coherent A80 phase-oracle step costs 1e7 to 2.6e8 Toffolis, i.e. 30 min to 12 h per step on one CCZ factory. Logical qubits are 1e4 to 5e4; physical qubits are 1e7 to 1e8.

Glued trees with PRP labels cross over at n ~ 220 to 370, but no protein graph has their column structure: the pilot gives Krylov dim = N/2.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for any protein-structure task. No protein-realistic energy or conformational graph has been shown to realise any of the constructions. The parent separations are L6 only inside their own oracle models, on contrived families: Childs et al. welded trees (exponential); GHV exp(n^{1/5-o(1)}) with an adjacency-list oracle; LWWZ exp(n^{Omega(1)}) queries to a general diagonal oracle f on a box; BLH superpolynomial to exponential on random hierarchical graphs. The transfer question is formally open. It reduces to white-box complexity of gapped stoquastic or QHD paths for explicit, poly-descriptio
- **Practical level:** L0. No instance, no algorithm and no resource model beat any classical baseline on a protein quantity. The proposed empirical arm (CTQW on 2D/3D HP pull-move graphs, L = 8-16) sits where exact enumeration, PERM and CPSP solve the problem outright. The literature phase already found lattice-cost optima worse than random folds on that representation, so the arm cannot raise the level.
- **Novelty note (abridged):** The arXiv-API search found no paper that tests whether GHV, LWWZ, welded-tree or hierarchical-graph super-polynomial separations transfer to protein energies or conformational graphs (scope: arXiv abstracts 2002-2026; web search engines unavailable this session).

Each component of the proposed no-go is prior art:
- (i) The explicit-naming lemma is folklore in the welded-tree literature: random labels are essential (from memory, unverified quote).
- (ii) The description-complexity barrier is largely already in this repo (T5 Proposition C1 caveat; gaps G5 and G10).
- (iii) Disorder-induced localisation on glued trees is published (Keating et al. 2007; Jackson et al. 2012; Muthukrishnan et al. 2019).

Two things are new:
- The information-locus-inversion framing: the instance sits off-diagonal in the separations but on-diagonal in proteins. As a result DNR-11's reopening condition is not m

## QM-10: Quantum Hamiltonian Descent / coherent tunnelling through tall thin barriers (argmin search and barrier-crossing variants)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 for the protein / learned-energy family: no separation statement exists for A80-type energies, and no barrier-shape theorem applies to them. The only rigorous QHD advantage result is Leng–Zheng–Wu (arXiv:2311.00811). It proves a QHD upper bound of O~(d^3) queries plus O~(d^4) gates on a constructed family; the classical hardness side was only EMPIRICAL. This session dequantised that family in practice. Gaussian homotopy (DEM, 1989) solved 100% of instances at d = 16 to 2048 with 2,100 gradient queries per run, a count that does not depend on d. Isotropic Langevin annealing solved it in poly
- **Practical level:** L0. No simulation, resource-normalised comparison or hardware result exists for QHD, tunnelling or QLD on any protein or learned energy. The fault-tolerant cost per QHD run is 1e4–1e6 times the measured classical time-to-best-basin at 60–80 aa (see the break-even note).
- **Strongest pro-quantum rebuttal considered:** The actual landscape does show real classical hardness, and nobody has measured barrier shapes on it.
(1) G1 pilot: λ-path NRPT with HMC plus prior-proposal pivot moves made 0 round trips at L = 45–150. Λ grew from 13.6 to 29.3, so nonlocal classical moves do not yet mix at T = 1.
(2) Unconverged census (200 L-BFGS iterations): median p_hit is 0.016 at 100 aa and hits the 1/256 floor at 100–120 aa. Within-target Spearman(E, mode RMSD) is 0.20, 0.36 and 0.31 on three 120-aa crops, so condition C may pass beyond 60 aa. That would reopen the argmin variant's relevance.
(3) Real-time coherent QHD is not stoquastic ground-state dynamics, so the PIMC-equivalence results (Isakov 2016; Crosson–Harrow 2016; Jiang 2016) do not formally cover it.
(4) QMC can be exponentially slower than incoherent tunnelling when there are many homotopy-inequivalent tunnelling paths (Andriyash–Amin, arXiv:1703.0927
- **Evidence (abridged):** LITERATURE (verified this session via the arXiv API or Crossref):
- QHD: Leng, Hickman, Li, Wu, arXiv:2303.01471.
- Leng, Zheng, Wu, arXiv:2311.00811 (PDF read). The instance is F_U(x) = Σ_k w((Ux)_k) with w(y) = y^4 − (y − 1/32)^2 − c and U a random rotation hiding separability. The classical baselines tested were scipy dual annealing, basin-hopping, Ipopt, SQP, SGD and Gurobi. No Gaussian homotopy, PT or PIMC was tested. The authors say their study "does not exclude the possibility of efficient classical algorithms".
- Chakrabarti et al., arXiv:2503.24332: "QHD does not offer a speedup over classical zeroth order methods with exact oracles".
- Liu et al., arXiv:2607.16996: potential synthesis can dominate QHD's fault-tolerant cost.
- Chen et al., arXiv:2311.15587 (quantum Langevin dynamics; heuristic).
- Tunnelling adversary precedents:
  - Crosson & Harrow, arXiv:1601.03030: SQA, a classical method, is poly-time on the thin-tall-barrier spike; "QA is unlikely to achieve exponential speedups over classical computing solely by the use of quantum tunneling".
  - Isakov et al., arXiv:1510.08057 (PRL 117, 180402): the QMC tunnelling rate scales like incoherent tunnelling.
  - Jiang et al., arXiv:1603.01293: for spiky barriers, QMC and tunnelling are polynomial while over-the-barrier crossing is exponential.
  - Denchev et al., arXiv:1512.02206 reported 1e8 times faster than SA on tall-narrow barriers. Mandrà et al., arXiv:1604.01746 found "the quantum speedup is limited to sequ

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for the A80 learned-energy task: no separation is known or derivable for this landscape, in either the argmin variant or the barrier-crossing variant. The per-run gate cost derived below is an L3-type cost with no speedup statement to attach it to. Stronger levels exist only elsewhere:
- **Constructed families, L6:** a provable (sub)exponential QHD/QAA separation via Gilyén–Vazirani (arXiv 2504.14841 building on 2011.09495). Leng–Zheng–Wu (arXiv 2311.00811) prove Õ(d³) queries for QHD, but the classical super-polynomial hardness there is only empirical.
- **Convex or local basin refinement,
- **Practical level:** L0. One QHD Trotter step on the A80 energy costs 3.5e7 Toffolis at L=45 and 2.6e8 at L=120 (central assumptions). At 170 µs per Toffoli with 100 factories, one run of 1e3 steps takes 0.7–5 days (L=45–120). The same step costs about 1–2e7 classical energy+gradient evaluations. At L=100, a single Trotter step at R=100 (5.1 min) takes longer than the whole median classical multistart argmin on one core (~19 s). A perfect one-shot QHD global optimiser breaks even only if the classical restart hit probability is at most ~1e-6 (and as low as ~1e-10 in other scenarios). PILOT measurements give ≥ 1.6e
- **Cost / break-even note (abridged):** **Per step.** Every QHD Trotter step needs 2·C_E: a full coherent A80 energy, computed then uncomputed. That is ≈ 2.3e4·L² Toffolis central and ≈ 1.2e4·L² generous. The kinetic/QFT part is under 0.05%, so QHD encoding optimisations aimed at the kinetic term (arXiv 2607.16996) buy nothing here.

**Per run.** A run of N_T = 1e3–1e4 steps costs 6e10–2.6e12 Toffolis at L = 60–120.
- Wall-clock: 0.7–51 days with 100 factories, and 69 days to 14 years with one factory.
- Qubits: 3–7e4 logical, 1–2.3e8 physical.

**One step versus classical.** One step at R=1 equals 1.0–2.1e7 classical energy+gradient evaluations. The ratio is roughly L-independent because both sides scale as L².

**Argmin break-even.** Even if QHD were a perfect one-shot global optimiser, classical multistart would need p_hit ≤ 1e-6 (R=100, S=1) to 1e-10 (S=1e3, N_T=1e4). The measured value is ≥ 1.6e-2 at the median up to L=100. The gap is ≥ 4e3× in the single most generous case and ~1e7–1e8× under Babbush-style adversaries.

**Barrier-crossing break-even.** Tunnelling must beat thermal activation by a net βΔ − S_WKB ≥ 11.5–26 nats per crossing. That is only possible for thin barriers that are either steric (removable cl

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for protein energies. There is a formulation only. No evidence shows that the A80/esmprior landscape contains the engineered structure behind any QHD separation. Generic QHD separations exist only on constructed instances. arXiv:2311.00811 solves each instance with Õ(d^3) queries, and its classical hardness is only empirical. arXiv:2504.14841 (Leng, Wu, Wu, Zheng 2025) proves a (sub)exponential oracle separation by compiling the Gilyén-Hastings-Vazirani construction into an objective function. That construction is far from a sum of smooth, bounded pair negative-log-likelihoods. The candidat
- **Practical level:** L0. Nothing has been measured, and there is no fault-tolerant break-even. The project's own T3 cost model (research/theory/T3_resource_model.py, driven by scratchpad qhd_cost.py) gives one QHD Trotter step as 3.3e7 to 6.3e7 Toffolis at 60 aa and 1.3e8 to 2.6e8 at 120 aa. Logical qubits including arithmetic workspace are 1.6e4 to 3.2e4 at 60 aa and 2.9e4 to 6.6e4 at 120 aa. The candidate's 700 to 1000 qubits count the grid data register only. Taking 1e3 steps at 170 µs per Toffoli, one run lasts 65 days (60 aa) to 1.4 years (120 aa).
- **Novelty note (abridged):** What was searched: arXiv API abstract searches for 'Hamiltonian descent' (16 records up to 2026-07-18), 'quantum tunneling' AND protein AND folding, 'quantum annealing' AND 'off-lattice', and 'Hamiltonian descent' AND molecular; plus Crossref lookups for the classical precedents. General web search was unavailable (the session's search budget was exhausted), so coverage is not exhaustive.

Under that scope, the search found no evidence of QHD or coherent-tunnelling optimisation applied to protein or peptide conformational energies, learned or physical, in 2019 to 2026. The nearest non-protein work is QHD on quadratic programs, Ackley-type benchmarks, constrained NLPs and community detection, plus the 2607.16996 resource estimates.

Novelty differs by part:
- Application: moderate to low.
- Mechanism: none. Schrödinger-dynamics, quantum-annealing and DEM global optimisation of peptides an

## QM-11: Prior-to-posterior amplitude amplification (quantum rejection sampling / independence walk): product head prior, coherently simulated flow generator, and distogram-native realizability conditioning

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 for the protein-relevant claim. The only provable statement is L6 in a black-box query model, and it holds only against a strawman comparator: classical rejection or independence-Metropolis from the same proposal. Quantum rejection sampling and amplitude amplification need Theta(sqrt(M)) queries against Theta(M) classically, with M = e^Phi (Ozols-Roetteler-Roland, tight). The independence sampler's gap is exactly 1/M, so a Szegedy walk also gives sqrt(M), not more. Against the relevant classical twin (tempered SMC, which uses the structure w = e^{-lambda U}) there is no separation. On the m
- **Practical level:** L0. No regime was found in which QM-11 is useful under matched conditions. At every measured (L, T), SMC started from the same exact product prior needs about 150-1500 pair-energy evaluations per particle. QM-11 needs at least e^{Phi/2} coherent iterations, each costing two or more full coherent energies. Its best case is 3GAHA_60 at T=30: e^{14.3} ≈ 1.6e6 iterations for exact sampling, and possibly about 1e2-1e4 for the eps-approximate version (sigma was not measured at T>1). That is before the fault-tolerant cost ratio R ≈ 3e4-2e7 per evaluation is applied. Variant (c) is exponentially domin
- **Strongest pro-quantum rebuttal considered:** Amplitude amplification from the prior is exact and immune to metastability. Its cost e^{Phi/2} does not depend on barriers or mixing. The classical side's correctness at T=1 is not established:
- my SMC is pivot-only with N=128, and lineages collapse to 54-67 of 128 at T=1;
- its KL disagrees with NRPT thermodynamic integration (TI) by 1.7x at L=45 (67 vs 117 nats), and the NRPT pilot had zero round trips.

If the learned posterior has a persistence or first-order bottleneck along every classical path, the exact classical cost could grow exponentially while QM-11 stays at e^{Phi/2}. The literal pre-registered threshold "Phi > 40 nats at L~60" is also NOT met by my lower bounds on 3GAHA_60 at T=10 (38.3) or T=30 (28.6). At high T, the eps-approximate quantum iteration count, with sigma unmeasured, could be about 1e2-1e4, comparable to SMC's evaluations per particle in raw query count.

R
- **Evidence (abridged):** MEASURED this session. The run was exploratory and not pre-registered: it is the "free byproduct" test named in the QM-11 spec. DEP only; no native structure was used. It ran single-threaded and self-throttled (it paused while machine CPU was above 95%, because other jobs were saturating the machine).

The run was adaptive-tempering SMC (N=128, ESS 0.5, exact-prior pivot moves) from the exact product head prior q_T to the A80/esmprior_v1 posterior, on the lambda-path of `qapf.sampling.hrex`. Script and raw data: `research/results/RAW/qm11_adversary/smc_phi.py` and `smc_phi.jsonl`.

KL(pi||q) / D_inf lower bound (= -min U_seen - logZ ≤ Phi), in nats:

| crop | T=30 | T=10 | T=3 | T=1 |
|---|---|---|---|---|
| 5O37A_30 | 6.2/10.7 | 10.5/15.7 | 18.6/26.4 | 39.0/46.9 |
| 5O37A_45 | 26.0/30.6 | 40.4/45.9 | 50.0/59.5 | 66.9/77.2 |
| 5O37A_60 | 34.6/42.7 | 48.9/59.7 | 68.1/80.4 | 89.9/98.0 |
| 3GAHA_60 | 22.6/28.6 | 33.2/38.3 | 45.7/54.5 | 72.4/87.2 |

SMC cost was 1.9e4-1.9e5 pair evaluations per 128-particle run (5-25 stages). At T=1 it went 5.4e4 → 1.2e5 → 1.9e5 for L = 30 → 45 → 60, about L^1.8, so the ≤ L^3 criterion is met.

NRPT pair_trace TI at T=1, from existing `research/results/RAW/g1_pilot/*.npz`, using KL(pi1||pi0) = ∫(E_lam U - E_1 U) dlam:

| crop | KL (nats) | D_inf lower bound (nats) |
|---|---|---|
| 5O37A_45 | 117 | 134 |
| 3GAHA_60 | 143 | 162 |
| 5O37A_100 | 481 | 542 |
| 4LPQA_120 | 510 | 576 |
| 5O37A_150 | 1011 | 1229 |

That is 2.4 → 6.7 nats/residue, super-

### Lens: resource (verdict: KILL)
- **Theoretical level:** L6 holds only for the generic, non-protein statement that quantum rejection sampling needs Theta(sqrt(M)) queries where classical rejection needs Theta(M) (Ozols-Roetteler-Roland, oracle model). Against the actual classical twin (SMC or non-reversible PT from the same exact product prior), the protein task stays at L0. That comparison is a proven exponential disadvantage whenever Phi = Theta(L): one-shot conditioning costs about exp(Phi_eps/2) coherent evaluations, while annealing pays only the barrier along the path. QSA/QM-01 also dominates QM-11 in every regime, because QSA pays sqrt(barrie
- **Practical level:** L0, and the measurements are negative. The quantum route misses break-even by at least 6.7 orders of magnitude at its most favourable measured point (L=45-60, T=30). It misses by 10 to 190 orders everywhere else on the L=45-150, T=1-30 grid. At the smallest divergences it even loses to its own twin, classical rejection sampling.
- **Cost / break-even note (abridged):** B*(L,T) = R * (pi/4) * exp(Phi_eps/2) classical evaluations per sample, with R ≈ 1e7. R comes from C_iter ≈ 1.1e4*L^2 Toffolis at 170 us per Toffoli against a 0.6-3.5 ms CPU energy+gradient evaluation.

Measured B* against the ideal classical NRPT cost:
- L=60, T=30: B* = 5e9 against 1.1e3 (margin 4.7e6).
- L=45, T=30: B* = 7e9 against 1.1e3.
- L=60, T=10: B* = 5e12 against 2.7e3.
- L=100, T=30: B* = 1e18 against 3.6e3.
- L=150, T=1: B* = 2e200 against 4.5e4.

Against its own twin, classical rejection sampling, QRS wins only when Phi_eps > 2 ln R ≈ 32 nats. At that point the quantum per-sample time is already at least 1e7 x 2.1 h ≈ 2,400 years at L=60.

Best measured point (L=60, T=30): about 2.4e10 Toffolis per sample, 1.4e4 logical and about 3.6e7 physical qubits (d≈35), 47 days per sample on one factory, or about 11 h with 100 factories. The classical NRPT takes about 1 s for the same posterior.

This fails the pre-registered K-G1a-style margin (3 orders at L<=150) by at least 3.7 further orders, and by far more everywhere else. The oracle and the w_max requirement erase the speedup, and Phi = Theta(L) makes the absolute cost exponential. Default KILL applies.

### Lens: relevance (verdict: KILL)
- **Theoretical level:** L0 for the protein instance. The only L6 content is generic: a query-model quadratic speedup over classical rejection or plain importance sampling. It needs about sqrt(1/P_acc) calls against 1/P_acc (Ozols-Roetteler-Roland 2012, tight; Low-Yoder-Chuang 2014 for prior-to-posterior on Bayes nets). The comparator in that result is dominated here. Against the strongest classical method on the same prior-to-posterior path (SMC/PT over lambda), QM-11 is the one-stage (l=1) case of walk-based QSA (QM-01). On the measured path it loses about e^51 in overlap at L=60. So QM-11 has no independent theoret
- **Practical level:** L0, with measured negative evidence. Divergences computed from existing G1 pilot data imply at least 1e20 (L=45) to 3e23 (L=60) prior-prep plus coherent full-energy calls per posterior qsample in the most optimistic fidelity-limited case. Exact QRS or the independence walk needs at least 1e28 to 1e35. That is before fault-tolerant overhead of roughly 8e7 Toffolis per coherent energy or walk step at L=60 (T3's 2.3e4*L^2). The classical pilot NRPT used 5.6e5 gradient evaluations per run at 45-60 aa. Mixing was not certified (zero round trips).
- **Novelty note (abridged):** The mechanism is not new. Prior-qsample-to-posterior amplitude amplification is Ozols et al. 2012 and Low-Yoder-Chuang 2014 (Bayes nets, quadratic in 1/P(evidence)). The multi-stage version is Harrow-Wei 2020. Coherent flow and generator qsamples with quadratic post-processing are Layden et al. 2025 (arXiv:2510.08462) and Kodama et al. 2026 (arXiv:2608.21700). A folding-motivated instance already exists in Rattacaso et al. 2026 (arXiv:2603.12334): a lattice compact-polymer qsample reweighted to temperature T by amplitude amplification.

The search found no evidence of a paper applying QRS or amplitude amplification from a learned per-residue (theta,tau) prior, or from a protein structure generator, to a learned ESM-distogram structure posterior at 45-150 aa. Nor did it find one measuring the instance divergences (D_1/2, D_KL, max-ratio Phi) that set the cost. Scope: arXiv API keyword que

## QM-12: Rare events and metastability via quantum-walk hitting, search and walk phase estimation vs classical splitting (metastable escape rates, topology-predicate marked sets, ms-s transitions)

### Lens: classical (verdict: KILL)
- **Theoretical level:** In the generic query model, against the same classical Markov chain run as brute force, this is L6: quantum-walk search and hitting are provably quadratic, sqrt(HT) against HT (MNRS [A2], Krovi et al. [A3], AGJK [A4]), and walk phase estimation gives 1/sqrt(lambda_B) against 1/lambda_B. On the protein-relevant instance family, against the correct classical adversary (splitting and path sampling), it is L0: formulation only. No separation from AMS/FFS/WE/DPS is known, and the one regime where a separation could exist has not been shown for learned pair-distance energies. That regime needs every
- **Practical level:** L0. No resource-normalised win exists at any tested L. The T3 fault-tolerant cost per qubitised walk step at L=60 is 1.1e1 s (D3 generous) to 1.4e2 s (D2 central), with 100 CCZ factories at 170 us per Toffoli. The classical energy+gradient evaluation costs 0.36-1 ms. The quantum walk wins a search or hitting task only if the irreducible classical hitting cost after splitting is at least B = (S*t_Q/t_C)^2, which is about 1e9 (most generous: D3 generous, one classical core) and 1e11 to 1e17 in other scenarios. It wins an estimation task (walk QPE or amplitude estimation at eps=0.1) only if the r
- **Strongest pro-quantum rebuttal considered:** The candidate's precondition could hold in glassy or first-order regimes. PILOT data point that way. In the G1 256-restart census at L=100-120, n_modes/R is 0.95-1.0 on most crops, and p_hit(best) is about 0.004-0.03. The lambda-path NRPT pilot saw 0 round trips in 1200-1500 scans; T5 says this is significant at L=45/60 and not diagnostic at L>=100. Rolland and Simonnet (arXiv:1412.3362, JCP 283:541, 2015) show that AMS statistics deviate badly at phase transitions when the reaction coordinate is not the committor. If the lowest learned-energy basin is separated by a frustrated barrier (strand-register shift, mirror topology, threading) that no native-free coordinate resolves, AMS/WE fall back toward brute force. AGJK's sqrt(HT) then holds for any reversible chain with no reaction coordinate needed. Rebuttal:
- The census used only 200 L-BFGS iterations and 2 A clustering, which inflates
- **Evidence (abridged):** Classical adversary, strongest first. Citations were verified this session via arXiv API or Crossref, or were already in BIBLIOGRAPHY.md.
- **(1) Adaptive multilevel splitting (AMS).**
  - Cérou and Guyader, Stoch. Anal. Appl. 25(2):417-443 (2007), DOI 10.1080/07362990601139628. With the ideal coordinate, relative variance is about log(1/p)/N, so cost is about log^2(1/p)*tau/eps^2.
  - Cérou and Guyader, Ann. Appl. Probab. 26(6) (2016), DOI 10.1214/16-aap1177: adaptive precision equals optimally placed fixed levels.
  - Bréhier, Lelièvre and Rousset, arXiv:1405.1352: unbiased for any k.
  - Bréhier, Gazeau, Goudenège, Lelièvre and Rousset, arXiv:1505.02674: unbiased whatever the importance function, discrete-time setting. An imperfect reaction coordinate costs variance, not correctness.
  - Lopes and Lelièvre, arXiv:1707.00950: AMS on a molecular isomerisation, which also yields the committor.
- **(2) Forward flux sampling (FFS).** Allen, Warren and ten Wolde, PRL 94:018104 (2005), arXiv:q-bio/0406006. Also Allen, Frenkel and ten Wolde efficiency analysis, arXiv:cond-mat/0602269. Rate = flux times the product of interface probabilities.
- **(3) Weighted ensemble (WE).**
  - Huber and Kim 1996 [E61].
  - Zhang, Zuckerman and Jasnow, arXiv:0810.1963: statistically exact for any binning.
  - Adhikari et al., JACS 141:6519 (2019) [E63]: microsecond-to-second atomistic folding times.
  - Also milestoning [E64], MSMs [E65, E66], and MSM kinetics to hours [E67].
- **(4) Rarity-indep

### Lens: resource (verdict: KILL)
- **Theoretical level:** L2, and only against brute-force waiting-time or i.i.d.-trial classical access. MNRS, Krovi and AGJK walk search give sqrt(HT) against HT, and walk QPE gives 1/(r*sqrt(lambda)) against 1/(r^2*lambda) (THEORETICAL [A2-A4, A22, A35]). T3's G(L) supplies the gate-cost ingredient, so an L3 fault-tolerant runtime statement is available, but only against brute force and only conditional on the stationary-state setup and the gap/overlap assumptions (T2 A-delta is UNPROVEN). Against adaptive classical splitting (AMS, WE, FFS) with any coordinate that gives Theta(1) interface probabilities the level is
- **Practical level:** L0. The quantum side needs a qubitised learned-energy walk step costing 6.5e6 to 5.1e8 Toffolis at L=60-150 (T3), or 11 s to 24 h of wall-clock per step. Even the most generous scenario breaks even only against one classical core and needs escape rates of about 1e-8 per step. Against a parallel classical adversary (S=1e3) the break-even runtime is centuries or longer. No measured classical cost is anywhere near break-even: the G1 pilot lower bound is 2e5 to 4e5 evaluations per round trip. The readout, an escape rate of a Metropolis chain on a learned posterior, has no endpoint value.
- **Cost / break-even note (abridged):** The oracle costs erase the speedup.
- The walk step alone is 6.5e6-5.1e8 Toffolis (11 s to 24 h per step), which is 1.9e4 to 3.9e7 classical evaluations of time per coherent step.
- The stationary-state setup needed by MNRS/AGJK is itself the QM-01 sampling problem.
- Walk-QPE rate estimation breaks even against brute force only at lambda <= 1.4e-8 per step with T* of about 0.22 yr, and only in the most generous case (D3 bond-relaxed target, 100 factories, one classical core, c_q = 1).
- Against a 1e3-core parallel-replica adversary the break-even is lambda <= 1.4e-14 with T* of about 220 yr. For the actual A80 target (D2 central, one factory) it is lambda <= 3e-15 with T* of about 1e6 yr.
- Against AMS or WE with any coordinate giving Theta(1) interfaces there is no crossover at any lambda.
- Per-interface quantum splitting needs p_i <= 3e-9 with coherent trials, or <= 3e-4 with fast-forwarded segments (most generous). That is far below the task's 1e-4 support threshold once S > 1.
- Topology predicates (about 1e8-6e8 Toffolis) exceed a D3 step.

Total per estimate at lambda = 1e-10: 5e13-1e15 Toffolis on 1e7-1.8e8 physical qubits.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** The primitive is L6, but it is quadratic and query-model only. MNRS/Krovi/AGJK hitting costs about sqrt(HT) against HT. Szegedy-walk QPE resolves a reversible chain's slow eigenvalue in about 1/(delta*sqrt(lambda_B)) steps against 1/(delta^2*lambda_B) for direct waiting-time estimation. Amplitude estimation per interface costs 1/(delta*sqrt(p_i)) against 1/(delta^2*p_i). All of these separations hold only against unassisted chains and brute-force waiting times, which is the DNR-05 weak-baseline error.

Against the relevant adversary the task is L0 (formulation only). That adversary is splittin
- **Practical level:** L0. There is no simulator run, no hardware run and no matched classical run.

The per-step cost is the problem. research/theory/RESOURCE_MODELS.md gives 1.1e7 (D3 generous) to 1.0e9 (D1) Toffolis per coherent walk step at L=100, even for the coarse learned C-alpha energy. At 170 us per Toffoli per factory, one step takes about 19 s (R=100 factories, D3 generous) up to about 3.9e4 s (D2 central, one factory). A classical evaluation takes about 3 ms at L=100 (0.59 ms at L=45, scaled as L^2). So each quantum step is roughly 6e3 to 1e7 times slower. The break-even B(L) is 1.3e8 to 4.8e9 classical 
- **Novelty note (abridged):** Novelty is low for the primitive and moderate for the no-go framing.

Walk hitting, walk QPE and amplitude estimation of transition probabilities are standard [A1–A4, A22, A35]. They are already in the program as M3/QA-3, rated WEAK in Opportunity Map v2.

The arXiv title/abstract search was 14 API queries on 2026-09-27. The web-search budget was exhausted, so Google Scholar and other non-arXiv venues were not covered. Within that scope, it found no evidence of either:
- (i) a quantum analogue of AMS/FFS/WE with amplitude amplification per interface; or
- (ii) any quantum rate or rare-event method benchmarked against WE/AMS/FFS/MSM on a protein.

The nearest works are:
- Kharazi et al. 2026, whose exponential claim is against worst-case Langevin bounds with additive error, and is not robust to splitting;
- Mazzola 2021 and Pravatto et al. 2021, which are variational rate eigenproblems;
-

## QM-13: Committors and transition rates via quantum linear-system / QSVT solvers on the discretised backward-Kolmogorov generator

### Lens: classical (verdict: KILL)
- **Theoretical level:** Exponential claim: L0, refuted. The "N enters logarithmically" saving is measured against full-grid PDE solvers, which nobody uses at d≈120. The committor q(x)=P_x[τ_B<τ_A] has a positive Feynman–Kac form, so random-walk Monte Carlo already costs nothing in N and is dimension-free. Linden–Montanaro–Shao prove for the heat equation that the QLSA route is "never faster than the best classical algorithms", and that the only speedup (AE on an accelerated random walk) is "at most quadratic". The backward generator is a reversible M-matrix (stoquastic), so the same positive-unraveling argument appli
- **Practical level:** L0. No matched-conditions usefulness (L1) is plausible. At 60 aa, even the best-case quantum variant (a "quantum AMS", i.e. product-of-ratios with AE per level) gains at most ~10x in 1/ε at ε=0.1. Against that stands a coherent-oracle overhead of ≥1e6–1e7 Toffolis per E/∇E query, plus fault-tolerant clock ratios. The plain QLSA+AE design is ~1e17–1e20 Toffolis, against ~1e8–1e9 classical force evaluations.
- **Strongest pro-quantum rebuttal considered:** The best case for the quantum side is that QLSA is reaction-coordinate-free. AMS, WE, FFS and milestoning reach polylog(1/k) cost only with a decent progress coordinate. On a 60-aa learned-energy landscape with no known coordinate, or with entropic or golf-course bottlenecks, their variance can drift back toward brute-force cost ~1/k. A generic "PDE on an exponential grid" is also not automatically dequantisable: Babbush et al. (PRX 13, 041041, 2023) give a BQP-complete, exponential speedup for 2^n coupled classical oscillators.

Rebuttal (why KILL stands):
(i) In that coordinate-free worst case, QLSA+AE costs κ·√(α/k)/ε, against brute-force MC at T/(kε²). That is quadratic, the stochastic-unraveling ceiling.
(ii) The oscillator result relies on conservative (unitary-embeddable) dynamics. The backward Kolmogorov generator is dissipative and non-normal in flat L2. An–Liu–Wang–Zhao (CMP 40
- **Evidence (abridged):** VERIFIED this pass (arXiv API or abstract page, or Crossref):
- Linden, Montanaro, Shao, "Quantum vs. classical algorithms for solving the heat equation", arXiv:2004.06516 (CMP 2022, journal ref not re-checked). Abstract: "at most quadratic quantum speedup using ... amplitude estimation [on] an accelerated classical random walk ... [QLSA] is never faster than the best classical algorithms."
- Montanaro & Pallister, PRA 93, 032324 (2016), arXiv:1512.05903: FEM speedup is "polynomial".
- Childs, Liu, Ostrander, Quantum 5, 574 (2021), arXiv:2002.07868.
- An, Liu, Wang, Zhao, CMP 406(8):189 (2025), arXiv:2211.05246: "quantum algorithms suffer from computational overheads due to two types of 'non-quantumness': real part gap and non-normality".
- Orsucci & Dunjko, Quantum 5, 573 (2021), arXiv:2101.11868: √κ for positive-definite systems.
- Montanaro, Proc. R. Soc. A 471:20150301 (2015), arXiv:1504.06987: quadratic Monte Carlo speedup.
- Babbush, Berry, Kothari, Somma, Wiebe, PRX 13, 041041 (2023), arXiv:2303.13012.
- G. Wang, QIC 17:987 (2017), arXiv:1311.1851: effective resistance. This is the closest formal analogue: the committor is the harmonic voltage and the reactive flux is the effective conductance.

Classical adversaries, verified:
- Cérou & Guyader, "Adaptive Multilevel Splitting for Rare Event Analysis", Stoch. Anal. Appl. 25(2):417–443 (2007).
- Bréhier, Lelièvre, Rousset, arXiv:1405.1352: unbiased; variance asymptotics in the idealized case, relative variance ≈ ln(1/p)

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for any claim that matters to proteins. The only exact separation, log N versus N (L6-type under a sparse-access or block-encoding oracle), is against deterministic grid PDE solvers, which nobody uses at d >= 4. Against the relevant adversary (trajectory Monte Carlo and splitting), the ceiling is at most quadratic, in precision and in rarity. This follows from the stochastic-unravelling principle: q(x) = P[hit B before A] is a positive functional of a Markov process. Linden-Montanaro-Shao prove the same ceiling for the heat equation, and there QLSA is never faster than the best classical me
- **Practical level:** L0, and negative. At L = 60 (d = 2L-5 = 115 internal coordinates, m = 64 grid points per coordinate) one QLSA solve costs 1.8e13 to 9.2e15 Toffolis. That is 99 years to 5e4 years at 170 us per Toffoli with one factory, or 0.6 to 290 years at 1 us. The rate readout needs eps^-1 * sqrt(N_trans) sequential repetitions of that solve. Take a rate with N_trans = 1e12 steps per transition and eps = 0.1. The quantum wall-clock is 5.8e6 years (best case: 1 us Toffolis, C_E = 2e7, kappa = 1e4) up to 5e11 years. Brute-force Langevin on one CPU core takes about 2.5e3 years, and AMS takes orders of magnitu
- **Cost / break-even note (abridged):** Per QLSA solve at L = 60: c * kappa * ln(1/eps) * 4 * C_E = 1.8e13 to 9.2e15 Toffolis, which is 99 to 5e4 years at 170 us and 0.6 to 290 years at 1 us. The AE readout repeats that solve eps^-1 * sqrt(N_trans) times. Break-even against single-core brute-force Langevin needs N_trans >= 5.3e18 (best case, 1 us) or >= 1.5e23 (170 us), up to 4e28. At break-even the classical cost is itself 1e10 to 1e20 CPU-years. Against AMS/WE, break-even needs a splitting variance inflation of 1e10 to 1e13. The oracle overhead of 4 coherent energies per block-encoding query (8e7 to 4e8 Toffolis) erases the speedup. So does the linear kappa. Two further oracles are not free: preparing the RHS state sqrt(pi_B) is a Gibbs-state preparation problem, and basin indicators require a classical MSM. Scientifically, learned-energy (esmprior) 'rates' have no calibrated physical timescale. They are also off the structure-accuracy endpoint, and at 9 to 60 aa that endpoint is limited by information, not computation.

### Lens: relevance (verdict: KILL)
- **Theoretical level:** L0 (formulation only). No separation has been shown between the QLSA/QSVT committor-and-rate route and Monte Carlo or splitting. The nearest prior art (Kharazi et al. 2026) proves a speedup only against worst-case upper bounds for naive Langevin simulation, and it gives no classical lower bound. It also sets this exact BKE linear-solve route aside because κ ~ N² e^{βΔV}. The only L6-type statement nearby belongs to a different primitive: amplitude estimation on random walks or Feynman–Kac integrals, which is dimension-free and gains exactly quadratically in 1/ε (Kwas 2004; Linden–Montanaro–Sha
- **Practical level:** L0, and negative against the right comparator. For a relative-precision rate, the naive QLSA+AE pipeline is exponentially worse in βΔ than adaptive multilevel splitting (AMS): it pays κ·k^{-1/2}/ε, where AMS pays about log(1/k)/ε². With a coherent splitting it could at best be quadratic in ε, and CA-4 already kills that in practice. Rates are needed only to about 10–50%, because a 1 kcal/mol force-field barrier error already changes k by 5.4× at 300 K.
- **Novelty note (abridged):** The search (arXiv abstract API plus Crossref, 2004–2026; WebSearch unavailable) found no paper that builds a QLSA/QSVT committor solver for a protein or a learned energy. The formulation itself is not new, though. Kharazi et al. 2026 (arXiv:2601.15523) name the committor/BKE linear-solve route, derive κ ~ N² e^{βΔV}, and set it aside in favour of a Gaussian-LCHS flux estimator. Quantum rate estimation for Fokker–Planck dynamics was already claimed in Mazzola 2021 (PRA 104, 022431; SUSY rates and currents, protein-folding motivation), Pravatto et al. 2021 (VQE on the FPS eigenproblem for a conformational rate) and Miyamoto–Tada 2025 (QSVT on the adjoint-FP eigenvalue). Protein transition-path sampling on quantum annealers exists as well (Hauke–Mattiotti–Faccioli PRL 2021; Ghamari et al. Sci. Rep. 2022 and JCTC). The only piece nobody has claimed is applying it to a learned structure energ

## QM-15: Fold-switching / competing-fold learned posteriors: an information-first test bed for bimodal sampling (sampler, hitting and swap-test/AE variants)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 for the protein task as posed. The generic query separations (quadratic walk/QSA hitting in the barrier factor e^{beta*Delta}; Olivucci et al. 2026 Omega(alpha) vs O~(sqrt alpha) on hide-and-seek wells [A45]; AE 1/(eps*sqrt p) vs 1/(eps^2 p)) are L6 only in their own abstract models. They do not transfer, because the relevant classical comparator here never pays the quantity being sped up. (i) Once two fold hypotheses exist, stratified bridge sampling or MBAR along a non-physical restraint path costs O(K*tau_w/eps^2), which does not depend on the inter-fold barrier or on p_B. (ii) A pairwis
- **Practical level:** L0. Nothing has been measured, and the paper derivation below says the classical cost falls below the fault-tolerant per-step overhead alone. Take the fold-conditioned stratified quantum variant, the best case for quantum. It beats classical stratification only if in-window mixing satisfies t_w > (R*eps)^2. With the program's T3 ratio R = C_q/C_c of 1e7-1e10 and eps = 0.5 (from ±0.5 kT), that means t_w > 2.5e13 to 2.5e19 steps inside a single fold-restrained window of ≤100 aa. The project's own G1 census minimises each restart in about 220 gradient evaluations at L = 100-120. The unstratified 
- **Strongest pro-quantum rebuttal considered:** The strongest case for keeping QM-15 comes from the project's own G1 data. The A80/esmprior landscape looks glassy at L ≥ 60. In the 256-restart census, 39-100% of restarts land in distinct minima at L = 60-120, the best-mode hit rate p_hit falls to 0.004-0.03 at L = 80-120 (research/results/PROCESSED/g1_summary.json), and the lambda-path NRPT pilot made 0 round trips at T = 1 with global barrier Lambda ≈ 14-29 over 30-39 rungs. So in-fold window mixing tau_w might itself be very large, and stratification would move the hardness into the windows rather than remove it. A second risk: if fold B were a narrow funnel with high mass (Woodard persistence), restarts and JAMS mode-finding would miss it. Rebuttals: (a) Hardness inside windows is the general G1/H-006 question, already pre-registered with kills K-G1a-d, including the calibrated-temperature kill K-G1c. QM-15 adds no mechanism, insta
- **Evidence (abridged):** CLASSICAL ADVERSARY PORTFOLIO (the full chain has no step that pays a barrier factor):

(1) NATIVE-FREE FOLD-HYPOTHESIS GENERATION (removes the discovery/hitting variant)
- AF-Cluster [E97, 10.1038/s41586-023-06832-9], disputed in [E98, E99].
- Subsampled AF2 [E96]. Monteiro da Silva et al. [E101, 10.1038/s41467-024-46715-9] predicted changes in relative state populations with >80% accuracy, working best for the qualitative effects of mutations. That is the QM-15 scientific object, obtained classically.
- CF-random: Lee, Schafer, Prabakaran, Chakravarty, Clore, Porter, Nat. Commun. 2025, 10.1038/s41467-025-60759-5. Abstract verified via Europe PMC this session: it 'outperforms other methods for predicting alternative conformations of … fold switchers' and 'sometimes works by sequence association'.
- ConforMix: Richman, Karaguesian, Suomivuori, Dror, NeurIPS 2025, arXiv 2512.03312, PMID 42358743. Abstract verified: an inference-time 'combination of classifier guidance, filtering, and free energy estimation'.
- ConforFold: Syrlybaeva & Strauch, Protein Sci. 2026, 10.1002/pro.70564. Title verified.
- Within esmprior itself: a direct read of the distogram factor tables. This takes one ESM-2 650M forward pass (seconds on CPU) and no sampling.

(2) MULTIMODAL SAMPLING WITH KNOWN OR FINDABLE MODES
- JAMS: Pompe, Holmes, Łatuszyński, arXiv:1812.02609, verified. The abstract splits the task into 'finding the modes … and sampling, given the knowledge of the locations of the modes'. The

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for QM-15 as posed. No query separation exists against the relevant classical adversary: fold-conditioned decodes plus stratified (umbrella/bridge/MBAR) estimation along a native-free Q_A-Q_B coordinate. The only provable separations that apply are relative to a different comparator: quadratic in the spectral gap / barrier factor e^{dF} of the *unbiased* quantised chain (Szegedy/QSA), quadratic against *i.i.d.* restarts for AE of a basin projector (T4), and Olivucci et al.'s hide-and-seek Theta(sqrt(alpha)) vs Theta(alpha) (T5 Theorem A: exactly quadratic, and it needs information-locality,
- **Practical level:** L0. At 56 aa the A80-faithful walk step (D2) costs 2.8e7-1.1e8 Toffolis, which is 1.3-5 h per step on one factory, and needs 2.7-3.0e4 logical and about 6e7 physical qubits (d=31). Even under the most generous stack (kappa=c_q=1, 100 factories, one classical core) the quantum is 1.5e3-1.5e4x slower per independent within-window sample than the classical stratified sampler. Break-even requires a residual classical mixing cost that no measured quantity approaches.
- **Cost / break-even note (abridged):** B(L) is the number of classical energy+gradient evaluations per independent sample at which the qubitised learned-energy walk ties the classical sampler.

- At the switcher length L=56: 3.4e15 (D2 central, S=R=1); 3.4e11 (S=1, R=100); 3.4e17 (S=1e3, R=100). Most favourable anywhere: 2.3e9 (D3 generous, bond-relaxed wrong target, kappa=c_q=1, S=1, R=100), for which T* is about 8 days per sample.
- With T2's c_q^2 in [1e4, 3e8], B rises by another 4-8 orders of magnitude.
- The classical stratified escape costs 3e5-3e8 evaluations for the entire dF estimate. Per window, the quantum is 1.5e3-1.5e4x slower even with every generous setting.
- The native-free fold indicator the quantum variants need is cheap in gates (<1% of a walk step), but it is the very information that makes classical stratification polynomial. The oracle therefore erases the speedup logically, not through gate count.
- Break-even would need an effective residual barrier of at least 17-33 kT orthogonal to every native-free fold coordinate. If such a barrier existed, the question would reduce to the generic H-006/G1 question.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for this instance. There are generic quadratic query separations, but none transfers here. M1/M2 QSA/QRELD are L6 only in abstract models, and the provable Omega(alpha) vs O~(sqrt(alpha)) continuous Gibbs separation needs hide-and-seek wells. Once a native-free fold-B hypothesis exists, fold-conditioned restraints and stratification remove that regime. The amplitude-estimation variant (estimating the fold-B population with a basin projector) has no advantage over stratified classical estimation. Unstratified AE costs O(e^{DeltaF/2}/eps) coherent walk calls. Classical umbrella sampling or MB
- **Practical level:** L0. Nothing has been run for QM-15. The available evidence predicts failure on its information precondition (kill criterion 1). The run-time gap to the fault-tolerant break-even is about 6 to 8 orders of magnitude at 100 aa or less (see break_even_or_cost_note).
- **Novelty note (abridged):** Scope: the arXiv API (all fields: "fold switching" AND quantum; and (metamorphic OR "fold-switching" OR "alternative conformations") AND quantum AND protein), plus Europe PMC (about 80 fold-switching hits on simulation and language models, 2016-2026). WebSearch was unavailable because the session budget was exhausted, so Google Scholar-level coverage is missing.

Under that scope, the search found no evidence of any quantum algorithm (walk, QSA, AE, swap test, annealer) applied to fold-switching or metamorphic proteins. Both arXiv queries returned 0 results.

The novelty is at the application level only. The primitives are standard: QSA/walks, Montanaro/Harrow-Wei partition-function AE, and the swap test. The proposal is a relabelling of QM-01/02/05/14 and M3/M4 onto one protein class.

The classical side is crowded:
- trX2-D (2026) already samples predicted inter-residue geometry distri

## QM-16: Quantum backtracking and tree-size estimation over combinatorial structure trees: beta-sheet/SSE topology assembly, DMDGP branch-and-prune from sparse NMR distances, rotamer partition functions (K*)

### Lens: classical (verdict: KILL)
- **Theoretical level:** Generic: L6, but only for query complexity against backtracking on the same tree. Montanaro detects in O(sqrt(T n)) and finds in O(sqrt(T) n^{3/2} log n). Ambainis-Kokainis estimate tree size to within 1±δ in Õ(sqrt(nT)) steps and turn any T-node classical backtracking run into Õ(sqrt(T) n^{3/2}). Montanaro's B&B is near-quadratic. On the protein instance family measured against the best classical algorithm: L0. No theorem or derivation gives quantum any advantage over the classical algorithms that actually solve these trees (DP, tree decomposition, ILP, bounded-width BP). The derivation below
- **Practical level:** L0. Hardware-realistic cost puts quantum 10^8 to 10^20 times behind at every size (see the break-even note). There is no instance family, no measured classical bottleneck, and no resource estimate that clears break-even.
- **Strongest pro-quantum rebuttal considered:** The best case for the quantum side is large all-beta or multi-sheet proteins of 250–300 aa with m ≈ 25–35 strands and a weak, orphan-like ESM signal. There the strand-candidate graph is dense and has high treewidth, and the exact classical subset DP over path covers costs 3^m ≈ 3×10^11 at m = 24 and 2×10^14 at m = 30. The Montanaro and Ambainis-Kokainis bounds are proven, and tree-size estimation could count feasible topologies.

This case fails four ways.
(a) Deciding whether a feasible topology exists is trivial. MAP is a degree-≤2 subgraph ILP whose LP relaxation is near-integral (Subramani-Floudas ILP; BetaPro graph algorithms), so the classical B&B tree is tiny.
(b) What is actually hard is the weighted topology posterior (a #P-type sum over path covers). Tree-size estimation counts nodes, not Boltzmann weight, so the useful primitive becomes QSA or walk sampling of the topology pos
- **Evidence (abridged):** Items marked [V] were verified this session through the Crossref, arXiv or Semantic Scholar APIs. Items marked [R] are verified entries already in research/literature/BIBLIOGRAPHY.md. Items marked [U] are unverified.

(1) DMDGP is not a large tree on real proteins [V]. Source: Liberti, Lavor, Maculan, Mucherino, "Euclidean distance geometry and applications", arXiv:1205.0349, §3.3.10 (text extracted).
- Prop. 3.9: if every level v > v0 has a pruning edge {u, v} with u < v−K, the BP tree width is ≤ 2^{v0−K}.
- "On a set of 45 protein instances from the PDB, 40 satisfy Prop. 3.9, and 5 satisfy Prop. 3.10, all with v0 = 4."
- BP runs in O(2^{v0} n^2) and is "empirically ... linear" on real proteins.
- So T = O(n) (≈2n nodes: about 900 at 150 aa), sqrt(Tn) ≈ T, and there is no speedup. The kill criterion "log S tracks log T" fires by theorem.
- Supporting papers: Liberti, Lavor, Mucherino, "DMDGP seems easier on proteins", doi:10.1007/978-1-4614-5128-0_3 [V]; Liberti, Masson, Lee, Lavor, Mucherino, DAM 165:213–232 (2014), doi:10.1016/j.dam.2013.01.020, where almost all protein-backbone Henneberg graphs have 2^k incongruent realisations [V]; Mucherino, Lavor, Liberti, JBCB 10:1242009 (2012), symBP, all solutions from one [V]; iBP in Lavor, Liberti, Mucherino, J Glob Optim 56:855–871, doi:10.1007/s10898-011-9799-6 [V].
- Quantum search on DMDGP already exists and only beats brute force: Lavor, Marquezino, Oliveira, Portugal, QIP 21:239 (2022), arXiv:2112.01303 ("more efficient than

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for the protein tasks. The generic primitive is L6 in the query model: Montanaro backtracking [C57], Ambainis–Kokainis [C58], Jarret–Wan [C59] and Montanaro B&B [C60] give a near-quadratic speedup relative to the same classical tree. That tree is not the classical frontier for any of the three sub-lanes, though.
(i) SSE topology: an edge-factorised pairing energy (esmprior strand-pair log-odds, with registers summed per edge) makes the topology posterior a weighted linear-forest sum. Classical subset DP computes it exactly in O(2^m m^2 + 3^m), or O(2^m m^2) with subset convolution. The idea
- **Practical level:** L0, negative. Break-even tree sizes are T* ~ 1e18 (topology), 1e21–1e23 (DMDGP) and 3e17 (rotamer B&B) nodes under Babbush/Sanders-style assumptions: 170 µs per Toffoli, one factory. Classical exact or bounded methods need about 1e11 operations or fewer everywhere in the 9–300 aa scope. Break-even only falls to about 1e8–1e10 nodes under an 'ultra' scenario (1 µs Toffolis, unit constants), which no published fault-tolerant architecture supports. Even there, the classical DP already solves the task exactly in seconds to minutes.
- **Cost / break-even note (abridged):** Break-even follows from T* = n·(c·G·t_Toff·P/(F·t_c))^2. The quantum side pays about 1 s (topology) to about 170 s (DMDGP) of wall-clock per walk step: G = 8e3 to 1e6 Toffolis at 170 µs each. The classical side pays 0.1–1 µs per node. Break-even therefore sits at about 1e18 topology nodes, 1e21–1e23 DMDGP nodes and 3e17 rotamer-window nodes, and each run at break-even takes 3e3–1e7 years. A 10x gain needs 100 times the break-even tree size. Physical footprint is about 2–4e6 physical qubits for topology, and about 6e7 for DMDGP with stored coordinates. Neither figure includes decoder cost, which [C63] shows erases backtracking advantage by itself.

Oracle-erasure points:
1. Depth-in-superposition forces level-indexed QROM and coherent random access, which is the dominant DMDGP cost (about 2.6e5 Toffolis per step just to fetch partner coordinates).
2. Coherent bounds must be weak and cheap, so the quantum tree is at least as large as a classical tree built with LP/DP bounds.
3. Learned-model tables are classical information. Loading them by QROAM costs about sqrt(N·b) per lookup and saves no precomputation.
4. Leaf decoding (the 3D build, esmprior rescoring) is not coherent-friendly.

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for protein instances. Montanaro backtracking, Ambainis-Kokainis tree-size estimation and quantum B&B are L6 only relative to the SAME classical tree, under the query/step model. For all three sub-lanes, the best classical algorithm is not that tree. It is ILP with LP bounds for strand pairing (BCov-type), FPT branch-and-prune for exact-data DMDGP, and bounded best-first enumeration for K* (BBK*/MARK*). The generic L6 result therefore does not carry over to a separation on protein instances. No separation is known against those algorithms.
- **Practical level:** L0. No protein instance, simulation or resource estimate exists for backtracking or tree-size estimation on SSE topology, DMDGP or rotamer Z. The only quantum work in these sub-lanes uses Grover or QAOA and compares only against brute force or quantum baselines (Lavor et al. 2022; Khatami et al. 2023; Agathangelou et al. 2025).
- **Novelty note (abridged):** The search found no evidence of quantum backtracking or tree-size estimation for SSE/beta-sheet topology, DMDGP/iBP, or K* rotamer partition functions, under the scope of arXiv API, Crossref and Semantic Scholar queries (September 2026; WebSearch unavailable). Novelty is only in the application pairing. The primitive is Montanaro 2015/2018 unchanged. DMDGP already has a quantum (Grover) paper (Lavor et al., QIP 2022), and protein design has one (Khatami et al., PLOS CB 2023), so these sub-lanes are incremental. Recommended bookkeeping: record the <= 60 aa topology lane and the DMDGP lane as paper-KILL in KILLBOOK Section B, pending the census for the 150-300 aa topology lane only. Keep K* folded into M5 (WEAK). Add Brehm-Weggemans 2026 to BIBLIOGRAPHY as a CA-1 counterargument.

## QM-17: Planted-inference (Kikuchi / tensor-PCA) nearly quartic spectral speedups where information is present but conjecturally hidden: ambiguous restraints, learned distograms, heterogeneous low-SNR cryo-EM/MRA

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 for any protein instance family. There is only a formulation, and no reduction to planted kXOR or tensor PCA exists for (a), (b) or (c). The generic L6 result (nearly quartic, query/gate model, against the best KNOWN classical method, with no lower bound) applies only to random even-k planted noisy kXOR and single-spike tensor PCA [C71; Schmidhuber-Hastings 2026]. It does not carry over to pairwise restraints, OR-type ambiguity, dense rank-3 Gram models or overcomplete structured moment-tensor decomposition.
- **Practical level:** L0. No protein-relevant instance needs a Kikuchi level above l = 1-2, so the classical cost is at most about n^2, or 1e6-1e8 operations. The published fault-tolerant break-even for quantum Kikuchi sits at a classical cost of about 1e20-1e23 FLOPs.
- **Strongest pro-quantum rebuttal considered:** The best case for keeping the card is variant (c). Heterogeneous MRA/cryo-EM through third-order invariants is a genuine order-3 planted problem with a conjectured statistical-computational gap. Boumal et al. 2018 conjecture that polynomial-time recovery reaches only K ~ sqrt(L) classes, while the invariants identify more. My own derivation below (D4) shows this matches Wein's r ~ n^{3/2} low-degree barrier for order-3 decomposition. Quantum Kikuchi has also been extended beyond kXOR, to dense and sparse tensor PCA, tensor completion and asymmetric tensors (Fontana et al. 2025). If someone proved a smooth level-l Kikuchi tradeoff for orbit recovery inside the gap, and could build a guiding state from the data, an L6 result against the best known classical method could exist for a cryo-EM-adjacent model. The rebuttal to that case:
(i) Every quartic result is for detecting or recovering a 
- **Evidence (abridged):** VERIFIED THIS SESSION (arXiv abstract or HTML fetched):
[C71] Schmidhuber, O'Donnell, Kothari, Babbush, PRX 15, 021077 (2025), arXiv:2406.19378.
- Scope: even-k planted noisy kXOR on RANDOM instances (not semirandom).
- Classical: Õ(n^l).
- Quantum: n^{l/4}·poly(n) time on Õ(log n) qubits. The gain is AA on a guiding state whose overlap is n^{-l/2} instead of the random n^{-l}.
- Sec. III.5: a classical algorithm cannot exploit the guiding state, because it must still write n^l-dimensional vectors.
- Classically intractable instances need 1e15-1e16 Toffoli. Block encoding costs about 1e6 Toffoli, because the kXOR matrix is sparse and arithmetic.

Schmidhuber & Hastings arXiv:2607.29672 (2026): the sharp tradeoff is m ≳ rho^-2 n^{k/2} / l^{k/2-1}, proved for k >= 3.

Fontana et al. arXiv:2510.07273 (2025): 900 logical qubits, about 1e15 gates and 1e12 depth for a problem that classically needs about 1e23 FLOPs.

Wein, El Alaoui, Moore arXiv:1904.03858: the Kikuchi hierarchy for tensor PCA, with the kXOR result for even k only.

Wein arXiv:2211.05274: for order-3 tensor decomposition, polynomial-time methods are known only for r << n^{3/2}, the problem is low-degree hard for r >> n^{3/2}, and the information-theoretic limit is r ≲ n^2.

Boumal, Bendory, Lederman, Singer arXiv:1710.02590: heterogeneous MRA from invariant moments, with the conjecture that resolvable K ~ sqrt(L).

Bandeira et al. arXiv:1712.10163: cryo-EM needs a number of images that scales as sigma^6, using inva

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for QM-17 as a protein claim. None of the three variants has been reduced to the only setting where the nearly-quartic result is proved: planted noisy kXOR with even k and random sparse hypergraphs, or a rank-1 spiked tensor [C71, C72]. (a) has 2-body geometric data, not parity. (b) has k=2 dense data. (c) involves orbit recovery with odd lowest identifying order (3rd moment), and the SO(3)+projection mapping is unproven. The primitive has its own standing, which does not transfer to proteins: a time speedup relative to the best KNOWN classical method (Kikuchi power iteration, ~n^l), not a 
- **Practical level:** L0. At protein-relevant parameters the audit gives no data-loaded instance under the 1e20-Toffoli bound where the quantum route beats both (i) the domain-specific classical solver and (ii) buying more data. The primitive's own authors estimate 1e15–1e16 Toffolis for classically intractable kXOR instances. At 170 µs per Toffoli with one factory that is 5.4e3–5.4e4 years; at an optimistic 1 µs it is 32–317 years.
- **Cost / break-even note (abridged):** Assumptions: 170 µs per Toffoli with one factory (Babbush/Sanders style); 1 µs as the optimistic case.

- The authors' own figure for classically intractable planted-kXOR instances is 1e15–1e16 Toffolis, with block encoding ~1e6 Toffolis. That is 5.4e3–5.4e4 years at 170 µs, or 32–317 years at 1 µs.
- My optimistic toy break-even (quantum-favoured: no poly(l) overlap loss, K_QPE = 30):
  - vs 1 classical core: D* ≈ 2.5e11, ~41 days on each side;
  - vs 1e4 cores: D* ≈ 5e16, ~2.4 years and 5e11 Toffolis.
- The quartic primitive therefore breaks even only for multi-week to multi-year runs, and only on true even-k planted instances.
- Protein mappings:
  - (a) Linear-size restraint data force l = Θ(n): 1e14 to over 1e26 Toffolis at n = 300, over 1e30 at n ≥ 1000, plus a fast domain-specific classical competitor.
  - (b) One data-loading call (≥ 1.4 s even with select-swap plus 4000 ancilla qubits) already costs more than the full classical solve (≈ 1 s, L = 1000).
  - (c) The gap is closable by buying linearly more particles, while the quantum cost grows exponentially in l. Real d ≥ 1e4 pushes QROM alone to ≥ 1e16 Toffolis per call, so the total exceeds 1e20.
- Default outcome: KILL o

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 for any protein task. This is a formulation only: no reduction exists from NOE/crosslink assignment, distogram Gram inference or heterogeneous cryo-EM/MRA to planted sparse kXOR, spiked tensor PCA (k>=3) or hypergraph SBM. The underlying primitive is L6 only inside those abstract models, and only against the best KNOWN classical method (the Kikuchi spectral hierarchy). Schmidhuber et al. PRX 2025 [C71]; Schmidhuber & Hastings arXiv 2607.29672 (sharp normalized Kikuchi, quartic for detection and weak recovery, low-degree lower bounds in that model); Schmidhuber & Zlokapa arXiv 2510.08494 (hy
- **Practical level:** L0 for all three variants. The primitive is not break-even even on its own flagship instance. Fontana et al. arXiv 2510.07273 (verified): tensor PCA with n=100, k=4, l=16, m~5e5 needs ~900 logical qubits, ~1e15 non-Clifford gates and depth ~4e12, against ~1e23 classical FLOPs. My arithmetic: depth 4e12 at 1-10 us per logical layer is 46 days to 1.3 years; 1e23 FLOPs on an exascale machine is ~28 h. No protein instance has a mapped cost. The size mismatch is also direct. Cryo-EM targets are >~50-100 kDa (>~450 aa) and do not overlap the 9-60 aa instruments. NMR at 50-250 aa is routinely automat
- **Novelty note (abridged):** Under the scope above (arXiv API queries plus the repo bibliography; the WebSearch budget was exhausted), the search found no evidence of Kikuchi, tensor-PCA or DQI quantum algorithms applied to any protein structure-determination task. Of the 6 Kikuchi + quantum hits, the only applications were hypergraph community detection (2510.08494) and quantum max-cut (2605.14994). The nearest protein-adjacent quantum work is Lavor et al. 2021 (Grover on DMDGP), which is quadratic and a different mechanism.

The repo's own M12/G8 notes already name this mapping as novel but expected negative. The only sub-variant with a numerically plausible gap window is 3-body coevolution (n~1e3-6e3, Neff~1e2-1e4). It is not in the card's main list and is unstudied. The obstacles are non-iid phylogenetic samples and an AlphaFold-class competitor. If G8 is written up, it should record this as a named open questio

## QM-18: Restraint-defined posteriors with new per-target information: joint discrete-assignment x structure sampling from sparse ambiguous restraints, and integrative-modelling posteriors of large assemblies

### Lens: classical (verdict: KILL)
- **Theoretical level:** L2 same-chain only, and nothing new. The Szegedy/QSA sqrt(gap) speedup of the joint (x, assignment) chain is a textbook query-model result carried over from QM-01. It is not specific to this instance family. Against the best classical method it is L0. The only new ingredient, the discrete assignment register, can be summed out exactly (D1 in evidence) at a cost of O(sum_i K_i) terms per energy call. Where assignments are directly coupled by one-to-one matching constraints, a provably polynomial classical sampler exists (JSV FPRAS). The restraint posterior is a white-box sparse sum of pair term
- **Practical level:** L0. The program's landscape-independent bound (research/theory/BREAK_EVEN.md §1) caps it: no landscape, however hard, gives an advantage below T*_Q = A*rho*(K*n_b*G*t_T)^2/c per sample. QM-18's per-step oracle G is at least QM-01's (the restraint term adds about 1e6 Toffolis at L=100, <1% of the A80 G of about 2.3e8; an EM cross-correlation term adds 1e8-1e10, which multiplies T*_Q by about 2-2000). So T*_Q is at least 0.26-0.59 yr per sample with a sterics-plus-restraint prior (1 us Toffolis, K=10, the most optimistic case), 1-20 yr with the A80 prior, and 1e6-1e7 yr at central constants. For
- **Strongest pro-quantum rebuttal considered:** This is the best case for QM-18. It is the only card whose information comes from outside ESM-2, so H-002 does not kill it. Classical hardness has not been refuted on this family: no classical method is proven polynomial. A persistence-type bottleneck [E39, Woodard et al. 2009] is plausible along the data-weight path. With 10-20% outliers, narrow restraint-satisfying basins and broad restraint-violating or outlier-explained basins could swap mass as the data weight rises, giving a first-order-like crossing where lambda-path replica exchange is provably torpid. Dense 10-40-body packing under a 20 A map could also jam. In our own G1 pilot, lambda-path NRPT made 0 round trips in 3.7-5.6e5 gradient evaluations at L=45-150 (sequence-only posterior, T=1; results/PROCESSED/g1_summary.json). Classical sampling can therefore fail on learned-energy posteriors.

Rebuttal:
(i) Any such hardness live
- **Evidence (abridged):** DERIVATIONS
D1 (collapse, exact). The joint posterior is p(x,k|D) ∝ pi(x) Prod_i w_{i,k_i} f_i(d_{i,k_i}(x)), where k_i=0 is an outlier state with constant f. Given x, the k_i are conditionally independent. Summing them out gives exactly p(x|D) ∝ pi(x) Prod_i Sum_{k=0..K_i} w_ik f_i(d_ik(x)). At L=100, 1 restraint per residue and K=4, that is about 500 distance terms against about 4950 pair terms x 28 bins in A80. The added cost is under 10%, which matches the card's 1e6 Toffolis against G ≈ 2.3e8. By Liu 1994 (collapsed Gibbs, JASA, doi:10.1080/01621459.1994.10476829), the collapsed chain is no worse than the joint Gibbs chain. The 'discrete switches correlated through the structure' are therefore exactly the multimodality of the x-marginal. QM-18 reduces to QM-01 with E'(x) = E_A80(x) − Sum_i log Sum_k w f. The r^-6 ambiguous restraint is the deterministic form of this sum, and it is also the physically correct model of an overlapped NOE peak (Nilges 1995 JMB, doi:10.1006/jmbi.1994.0053; ARIA, Linge et al. 2003, doi:10.1093/bioinformatics/19.2.315; CANDID/CYANA, Herrmann, Güntert & Wüthrich 2002, doi:10.1016/S0022-2836(02)00241-3).

D2 (coupled discrete case). One-to-one matching constraints, as in resonance-to-peak bijections, give a permanent-weighted p(k|x). Jerrum, Sinclair & Vigoda (J.ACM 2004, doi:10.1145/1008731.1008738) give a provably polynomial rapidly-mixing chain and FPRAS. The Bethe permanent (Vontobel, IEEE TIT 2013, doi:10.1109/TIT.2012.2227109) is a practica

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for any advantage over the best classical sampler. Nothing shows that the joint restraint/assignment posterior is classically hard. When assignments are conditionally independent given the structure, the discrete register can be summed out exactly, so the joint chain is dominated by a classically collapsible marginal. The only proven statement is the generic quadratic walk/QSA speedup over the same quantised chain (Szegedy/LHPST, query model, conditional on the gap). That speedup applies to any reversible chain and is not a separation from ARIA-style smoothing, collapsed NRPT or SMC. What t
- **Practical level:** L0. In the most generous settings (S=1 classical core, R=100 factories, c_q=1, kappa at its floor), a quantum sample breaks even only if the classical sampler needs at least 1.5e10 energy+gradient evaluations per independent sample (protein + restraints) or 2.9e11 single-body moves (assembly). The break-even runtime T* is 68 days to 6 years per sample. At S=1e3 every B rises by 1e6 (T* of 186 years or more). No measured or typical classical cost comes within 1e3 of these values.
- **Cost / break-even note (abridged):** Break-even formula (S5 of RESOURCE_MODELS.md): B = kappa * c_q^2 * (S*G*t_T/(R*t_C))^2, with T* = B*t_C/S. So B scales as (G*t_T/R)^2 * S^2 / t_C^2.

**Restraint and data oracles are cheap.**
- NOE/crosslink restraint terms: +0.3-8% of a torsion (D2) step, +4-61% of a Cartesian (D3) step.
- EM map data term via QROAM lookups: 0.1-3% of G.
- They are not what kills the item. The cost drivers are the learned-energy pair terms (protein) and the O(N*n_b^2) excluded-volume and density-overlap sums (assembly). Classical code evaluates the latter in O(1) per move with cell lists; a coherent circuit cannot, which gives B proportional to N^2.

**Cost ledger (most generous to central):**

| Quantity | Protein (L=60-100) | Assembly (N=10-100) |
|---|---|---|
| Toffolis per step | 2e7 - 3.1e8 | 1.3e8 - 3.7e9 |
| Logical qubits | 5e3 - 1.1e5 | 1.2e4 - 2.5e4 |
| Physical qubits (d=31, 1 factory) | 1e7 - 2.3e8 | 2.4e7 - 5.2e7 |
| Break-even B at S=1 | 1.5e10 - 4.4e11 | 2.9e11 - 2.2e16 |
| Break-even B at S=1e3 | ~1e16 or more | ~1e17 or more |
| T* per sample | 68 d - 1e4 yr | 3.7 yr - 3e7 yr |

**Further costs not included in B:**
- QSA stage and phase-estimation overhead: c_q of about 90 or mor

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L2 at most, and only against the same chain. It inherits QM-01's quadratic speedup in the joint chain's spectral gap (Szegedy/QSA; data-tempering QSA is Harrow–Wei 2020). The discrete registers add nothing new at the theory level. Against the best classical method the level is L0 for the ambiguity mechanism: with per-restraint assignments, the discrete register can be summed out exactly by classical computation (derivation in evidence). No super-quadratic route is known. Pairwise restraints are k=2, and the planted/Kikuchi quartic results need k≥3 (T5 §3.8, gap G8).
- **Practical level:** L0. Nobody has measured a classical mixing failure on any restraint-defined posterior, here or in the literature I could reach. The NOE branch falls short of fault-tolerant break-even by about 3–5 orders of magnitude. The assembly/EM-map branch falls short by more and is effectively killed at the practical level.
- **Novelty note (abridged):** Search scope, 2026-09-27: arXiv API title/abstract queries and Europe PMC title queries, 2019–2026 plus older anchors. General WebSearch was unavailable because the session budget was exhausted, so the search is narrower than a full web search.

The search found no evidence of a paper applying quantum walks, QSA, quantum Langevin or quantum replica exchange to NMR ambiguous-restraint, crosslink or integrative-modelling structure posteriors. It also found none using quantum methods for NOE or resonance assignment, or for cryo-EM/integrative assembly sampling. Nearest prior art:
- Algorithm: Harrow–Wei 2020 already gives QSA for Bayesian inference along an adaptive annealing path; Wocjan–Abeyesinghe 2008 and Somma et al. 2008 precede it.
- Application analogue: quantum multiproposal MCMC for a scientific Bayesian posterior (Lin et al. 2023, phylogenetics).
- Protein-adjacent quantum work: 

## QM-19: Many-body 1H dipolar-network forward model for fast-MAS solid-state NMR / proton spin diffusion of protonated proteins (quantitative 3-8 A distances past dipolar truncation)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0. The claim is only a formulation. The generic BQP-completeness of real-time Hamiltonian simulation covers worst-case engineered Hamiltonians and observables. It does not carry over to this instance family: infinite-temperature two-point z-magnetisation transport in a dense, disordered, dissipative 3D proton network (1UBQ has a median of 35 protons within 6 Å). For that family I know of no hardness result or query separation. The known structural results point toward classical simulability: dissipation-assisted operator evolution (DAOE) for hydrodynamic transport (Rakovszky et al., PRB 105, 
- **Practical level:** L0. Usefulness under matched conditions has not been shown. My exploratory pilot (details under evidence) finds that the target quantity, a quantitative 5–8 Å distance, cannot be identified from the RFDR build-up with any forward model, exact or classical. The structural information that does exist is carried by relays of 4 Å or less. Even the crudest classical rate model's gap to the exact result shrinks with cluster size. Classical linear-scaling methods have been validated for spin diffusion: locally restricted LCL (LR-LCL) and spin dynamic mean-field theory (spinDMFT). Experimental routes 
- **Strongest pro-quantum rebuttal considered:** Coherent many-body effects are real, and a naive classical treatment does fail on them. (a) In the repo's own static C1 v2 gate (research/results/RAW/nmr_gate/1UBQ_p19_N10_*), the best classical adversary, sparse Pauli dynamics with eps = 1e-4, fails at about 34 µs even with dephasing gamma = 1000–5000 s^-1. (b) In my pilot, the golden-rule rate matrix is still biased at N = 12: the median |inversion bias|/sd is 1.25, reaching 5.5 sd for one 7 Å pair. Also, 35% of the exact model's Fisher information on a rigid-residue shift is not captured by the rate derivative. So the pilot does NOT show that a rate model reaches the 3–5% criterion. (c) LR-LCL (Perras & Pruski 2019) was validated on rotating small-molecule solids, not on fully protonated proteins under RFDR at 100 kHz or more. spinDMFT (Gräßer, Uhrig & Ernst 2026) was validated only on static solids. The classical adequacy of these tw
- **Evidence (abridged):** LITERATURE ADVERSARY (verified via Crossref/arXiv/PubMed metadata on 2026-09-27; the web-search budget was exhausted):
(1) Low-order correlations in Liouville space (LCL): Butler, Dumez & Emsley, CPL 2009 (doi:10.1016/j.cplett.2009.07.017); Dumez, Butler & Emsley, JCP 133, 224501 (2010) (doi:10.1063/1.3505455).
(2) First-principles proton-driven spin diffusion via a master equation with simulated zero-quantum (ZQ) lineshapes: Dumez & Emsley, PCCP 2011 (doi:10.1039/c1cp00004g); Dumez, Halse, Butler & Emsley, PCCP 14, 86 (2012) (doi:10.1039/c1cp22662b).
(3) LR-LCL: Perras & Pruski, JCP 151 (2019) (doi:10.1063/1.5099146). The abstract states that locally restricted LCL keeps full-LCL accuracy, runs orders of magnitude faster, scales linearly and should reach "several thousand spins" under MAS.
(4) spinDMFT: Gräßer et al., PRR 3, 043168 (2021); Gräßer, Uhrig & Ernst, Sci. Adv. 12 (2026) (doi:10.1126/sciadv.aee6228). It gives ZQ lineshapes and spin diffusion that match experiment. Its only prerequisite is many coupling partners, which protonated proteins satisfy.
(5) Classical and hybrid spin dynamics: Elsayed & Fine, PRB 91, 094424 (2015); Starkov & Fine, PRB 98, 214421 (2018).
(6) Tensor-train NMR at protein size: Savostyanov, Dolgov, Werner & Kuprov, PRB 90, 085139 (2014).
(7) Rate-model structure determination from proton spin diffusion: Suter & Ernst, PRB 32, 5608 (1985); Elena & Emsley, JACS 2005 (doi:10.1021/ja051208t); Elena et al., JACS 2006 (doi:10.1021/ja062353p). Solut

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 (formulation only). Estimating infinite-temperature two-point correlators Tr[Z_a(t)Z_b]/2^N to additive error is DQC1/BQP-hard only in the worst case and only conditionally (Knill-Laflamme 1998, cited from memory). No hardness result exists for secular dipolar dynamics on protein proton geometries under MAS with physical dephasing. Schuster et al., PRX 15, 041018 (2025), arXiv:2407.12768 (repo bibliography #381) gives a poly-time classical algorithm for average-case noisy circuits. It does not transfer directly, but it points the other way. One exact result cuts the claimed mechanism down (
- **Practical level:** L0. There is no hardware, no simulation and no matched-classical evidence. C1 (the static-oriented version of this family) is still running. Its only numbers are v1 pilots that the pre-registration excludes (research/results/PROCESSED/nmr_gate_summary.json). Resource accounting below puts one quantum forward evaluation at months (most optimistic) to 10^4-10^5 years (Babbush/Sanders 170 µs per Toffoli), before multiplying by the 10^3-10^4 evaluations an inversion or surrogate needs.
- **Cost / break-even note (abridged):** The quantum forward model breaks even only if all three hold:
1. N_coh > N* ≈ 25-36 spins, the crossover with brute-force exact typicality simulation.
2. The best classical approximation is biased > σ/3 on 5-8 Å build-ups at mixing times ≤ 10 ms. The candidates are the Dumez-Emsley zero-quantum-lineshape master equation, Perras-Pruski low-rank LCL, spinDMFT and cluster embedding.
3. The matched-accuracy classical cost exceeds ρ x T_Q per forward evaluation (ρ = cost of one quantum-computer-second in core-seconds).
T_Q per forward evaluation at N=50:
| Scenario | Toffoli time | T_Q | Classical cost to beat (core-s, ρ=1) |
|---|---|---|---|
| Optimistic (3e4 shot-equivalents) | 1 µs | 0.2 yr | 6e6 |
| Central (1e6 shots x 7 mixing times) | 10 µs | 2.5e3 yr | 8e10 |
| Babbush/Sanders | 170 µs | 4.2e4 yr | 1.3e12 |
Multiplying by the 1e3-1e4 forward evaluations needed for inversion or surrogate training gives at least 2e2 QPU-years (optimistic) to 4e8 QPU-years. Shots (ε ≈ 1e-3), not qubits, dominate: physical qubits stay at 1e5-5e5.
The leading build-up term, S_ab = d_ab^2 t^2/4, is exactly pairwise and classically free. So the quantum model only prices information in the higher-order

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0. The formulation is sound, but there is no separation at the instance level. Real-time dipolar dynamics is BQP-complete only in the worst case. The observable here is an infinite-temperature 2-point z-magnetisation correlator in ergodic protein 1H networks, at millisecond mixing times. For that observable there is no hardness result, and no query or oracle model in which the quantum forward model provably wins. The one theory result that bears on it points against: O'Brien et al. (PRX Quantum 2022) found parameters become learnable only as the dynamics turn non-ergodic. L6 holds only for th
- **Practical level:** L0. Nothing has been measured. The preregistered C1 gate (static, oriented, secular Hamiltonian, 320 us window) has no valid v2 results yet; the only processed file is the excluded N=12, gamma=3000 pilot. C1 also does not probe QM-19's regime (MAS/RFDR, powder, 1-10 ms mixing), which is more Markovian than C1's. A C1 kill carries over to QM-19 all the more; a C1 survival would not carry over.
- **Novelty note (abridged):** The scope was:
- arXiv API abstract searches: MAS ∧ (quantum computer, quantum algorithm, quantum simulation, qubits); protein ∧ NMR ∧ quantum computing or advantage; spinDMFT and spin diffusion.
- Crossref queries on fast-MAS 1H-1H distances in protonated proteins and on linear-scaling spin-diffusion methods.
- Project notes NM-1 and lit_F.
- General web search was unavailable (the session budget was exhausted).

Under that scope, the search found no evidence of any proposal to use quantum simulation of MAS/RFDR 1H spin-diffusion build-ups in protonated proteins to extract quantitative 5-8 A distances. The MAS, time-dependent, powder-averaged framing is therefore new relative to O'Brien 2022, which covered static or oriented ubiquitin. It is a variant of the same idea, not a new mechanism, and any write-up must credit O'Brien 2022 as the origin.

The classical side is the mature literat

## QM-20: Protein-scale many-body echo (OTOC / Loschmidt / multiple-quantum) NMR with a quantum-simulated forward model, and the shot-noise cost of consuming a quantum-estimated likelihood in posterior MCMC

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 (formulation only). No separation has been shown for secular-dipolar echo dynamics on protein geometries. The only related classical-hardness evidence is Google's off-diagonal OTOC(2) on 2D random circuits (arXiv:2506.10191; 2604.15427). That paper says the first-order OTOC is "sometimes well-approximated by combining exact wave-function evolution and Monte-Carlo simulation that ignores the effects of small interference loops". QM-20's observable F = Tr[W(t)VW(t)V]/2^N is that first-order OTOC. Worst-case BQP-completeness of local Hamiltonian simulation does not transfer to this instance fa
- **Practical level:** L0. Nothing reaches L1 under matched conditions on proteins. The only hardware pipeline (Zhang et al., arXiv:2510.19550) used 9 and 15 qubits, checked against exact 2^15 classical simulation, and is self-declared "not yet beyond classical". Its structural precision equalled independent spectroscopy (toluene ortho-meta distance 2.47±0.01 Å vs reference 2.46±0.01 Å). Consuming a quantum likelihood inside MCMC misses the card's own kill threshold by 3–7 orders of magnitude (derivation in break_even_or_cost_note).
- **Strongest pro-quantum rebuttal considered:** This is the best case for the quantum side, stated honestly.

(1) The forward model really does look hard for naive classical truncation. A dense protonated protein has about 0.055 ¹H/Å³, which is about 50 / 118 / 230 / 398 protons within 6 / 8 / 10 / 12 Å of the labelled site. For the OTOC to see a proton 6–12 Å away, the operator front must cover that ball, so the relevant Pauli weights are about 50–400. That is far beyond exact statevector (about 30–35 spins), weight-8 Pauli propagation or tensor-network belief propagation. This repo's own v1 pilot on 1UBQ (N = 12/14; excluded from C1 for instrument reasons) already shows weight-≤4 Pauli failing at t_c = 20 µs with frac_hard ≈ 1.

(2) The usual cluster adversary is known to break here. Ryan and Lunghi (arXiv:2602.14613, 2026) show that standard generalised CCE is "insufficient for providing even a qualitatively accurate description" o
- **Evidence (abridged):** WebSearch budget was exhausted this session. Items were verified through the arXiv API and PubMed E-utilities.

INFORMATION BYPASS (strongest adversary: the target information needs no quantum interpreter)
- Roos et al., J Phys Chem B 2018, doi:10.1021/acs.jpcb.8b00310: ¹⁹F–¹⁹F spin exchange under fast MAS gives distances "up to 1.6 nm".
- Shcherbakov & Hong, J Phys Chem B 2019, doi:10.1021/acs.jpcb.9b03812: ¹H-detected ¹H–¹⁹F HSQC-REDOR "up to ~15 Å".
- Roos et al. 2018, doi:10.1021/acs.jpcb.8b06878: ¹⁹F RFDR to about 1 nm.
- Hong, Acc Chem Res 2013, doi:10.1021/ar300294x: 15–20 Å.
- Shcherbakov et al., Chem Rev 2022, doi:10.1021/acs.chemrev.1c00662: 1–2 nm by solid-state NMR.
- Standard knowledge, not re-verified this session: PRE to about 25 Å; DEER 1.5–8 nm.
- All of these use pairwise or few-spin forward models that are classically trivial.
- Quantum necessity test: FULL (OTOC + quantum interpreter) vs ABLATION (¹⁹F/PRE/DEER restraints + classical interpreter + AF2/cryo-EM). Domain-packing and rotamer discrimination at 60–150 aa survives the ablation, so the quantum component is not load-bearing.

HARDNESS DOES NOT TRANSFER
- Google, arXiv:2506.10191 (Nature 646, 825, 2025). Quote: "For OTOC, we find that it is sometimes well-approximated by combining exact wave-function evolution and Monte-Carlo simulation that ignores the effects of small interference loops." The advantage claim is for off-diagonal OTOC(2); cached Monte Carlo matched experiment at 40 qubits.
- Zhang et

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 (formulation only). No separation is proved or evidenced for dipolar OTOC(1) dynamics on protein geometries. Generic BQP-completeness of 2-local dynamics is a worst-case statement and says nothing about this instance family. The hardness evidence (Google OTOC(2), Nature 646:825 (2025) [F30]; Bermejo et al. arXiv:2604.15427 [F31]) concerns OTOC(2) on random 2D circuits. It does not transfer to OTOC(1) under a structured 1/r^3 secular Hamiltonian with Lindblad relaxation, which is the regime where Schuster et al. PRX 15, 041018 (2025) [F35] noisy Pauli-path truncation applies. The layer that 
- **Practical level:** L0. The card's own resource kill criterion fires on paper by 2.7 to 7 orders of magnitude (see evidence). The only form that could work is an offline emulator. At Babbush-2021 constants that costs about 2.3e3 machine-years. Its most optimistic corner reaches machine-days only in the small-cluster, early-time regime where classical approximations are strongest.
- **Cost / break-even note (abridged):** Break-even per forward evaluation (N=100, t=1 ms, K=100, amplitude estimation at eps = sigma/2): Q = 4.2e12 Toffoli.
- That is 48 QPU-days at 1 us/Toffoli or 22.5 QPU-years at 170 us.
- B_classical at matched accuracy is 4e6-7e8 core-s at rho = 1 (one QPU-second priced as one core-second), or about 4e9-7e12 core-s at a realistic rho of 1e3-1e4 for a million-physical-qubit machine.
- Any classical approximation that stays within sigma for less than this, over the informative time window, wins outright. Pauli propagation also gets all times and all probes from one run.

Per posterior effective sample (likelihood consumed in MCMC): 2e15-2e16 Toffoli with amplitude estimation, 1.7e17-1.7e18 with shots at K=100, and up to 1.7e20 at K=1000. At 170 us/Toffoli that is at least 1e4 machine-years.

Emulator floor: 13 machine-days at 1 us, 5.9 machine-years at 170 us. Only in that corner (N=50, t=0.3 ms, K=20) could the cost be tolerable, and that corner is the early-time, low-weight regime that classical methods handle.

The oracle audit adds more. There is a free-Hamiltonian assumption for the whole cluster (a nuisance set of dimension about 3N plus motional, shift and pulse-error terms, wh

### Lens: relevance (verdict: WEAK. The posterior-MCMC consumption sub-claim is KILLED on paper, because the card's own kill criterion #4 fires by mor)
- **Theoretical level:** L0 (formulation only).
- No separation is established for the protein dipolar instance class.
- Worst-case hardness of Hamiltonian simulation and OTOC estimation, and Google's OTOC(2) random-circuit hardness evidence (arXiv:2506.10191; 2604.15427, which is Google-affiliated and not independent), do not transfer to dephased, powder-averaged, bath-coupled protein 1H networks.
- The only derivation specific to this card is a negative cost bound. Consuming the likelihood needs at least K^{3/2}/sigma coherent circuit calls per likelihood with amplitude estimation (AE), and K^2/sigma^2 shots without
- **Practical level:** L0.
- No protein OTOC or multiple-quantum echo data interpreted by quantum simulation exists.
- The nearest demonstration, Zhang et al. arXiv:2510.19550, used 8–14 1H small molecules in a liquid crystal, 9- and 15-qubit Willow circuits and a grid search over 99 candidate models. It is self-declared "not yet beyond classical".
- The in-repo C1 smoke result (N=8: OTOC observables carry 10–40x the Fisher information of 2-point transfer) is not a result. The v2 production grid has no outputs yet: `research/results/PROCESSED/nmr_gate_summary.json` holds only excluded v1 pilots.
- **Novelty note (abridged):** Scope: arXiv API and PubMed E-utilities, searched 2026-09-27, plus the literature-phase records. General web search was unavailable.

Under that scope, the search found no evidence of a published study that:
- applies a quantum-simulated OTOC or multiple-quantum forward model to protein geometry, or
- derives the pseudo-marginal shot-noise cost of a quantum-estimated likelihood inside a protein structure posterior.

The components are not new:
- OTOC NMR with a quantum-simulated interpreter for molecular geometry is Zhang et al. 2025, who themselves propose the extension to biomolecules at 20–60 A.
- Quantum-simulator likelihoods inside Bayesian or SMC inference go back to Wiebe et al. 2013/14, Sels et al. 2019/20 (for NMR) and Ramoa et al. 2025 (pseudo-marginal on shot data).
- The cost formula is standard pseudo-marginal theory.
- Multiple-quantum (OTOC-family) NMR on protein assemblie

## QM-21: Hardness-identifiability trade-off theorem for spin-dynamics structure learning (the physics-lane analogue of H-001) - gate for the whole quantum-NMR family

### Lens: classical (verdict: KILL. This applies to the quantum-NMR structure family (QM-19/20/22-spin) as it passes through the QM-21 gate. Every pro)
- **Theoretical level:** L0 (formulation only). No hardness evidence exists for this instance family. BQP-completeness of generic 2-local Hamiltonian simulation says nothing about 3D 1/r^3 dipolar protein networks with z_eff ~ 3. No result shows that the classically hard component carries identifiable geometric Fisher information. The proposed bound C3-a is vacuous at realistic gamma/J ~ 1e-3 to 1e-2. C3-b (universality and self-averaging) has indirect support: the universal operator growth hypothesis was verified experimentally in 19F NMR FIDs (arXiv:2604.09362), and O'Brien et al. (2022) found the learning Hessian d
- **Practical level:** L0. No protein experiment measures the observable that would be needed (site-resolved static 1H-1H transfer or OTOC). The quantum forward-model cost is 1e14 to 1e17 T gates per likelihood-gradient evaluation (see the cost note). The classical twins run in minutes to seconds. The one production C1 point, probed at a size too small to test scaling, already shows the best classical adversary with a hard-window Fisher-information fraction of 0.
- **Strongest pro-quantum rebuttal considered:** 1. The adversary's local win is not evidence about scaling. At N=10, sparse Pauli dynamics with |c| >= 1e-4 matched the exact result, but it kept up to 54,450 strings. That is 5.2% of 4^10 and about 29% of the dimension of the Sz-conserving operator space, C(20,10) = 184,756, so it is close to brute force. At N >= 20 the same accuracy could need about 1e10 strings or more.

2. Weight truncation fails early even at N=10: w=5 fails at 80 us, classical spins at 40 us, and the exact 8-spin sub-cluster at 60 us.

3. Protein 1H networks fall in the few-strong-neighbour regime, which is where classical spins (Elsayed and Fine) and single-site spinDMFT are least reliable; Gräßer et al. state that spinDMFT needs each spin to interact with many others. Measured here: z_eff = (sum of d^2)^2 / (sum of d^4) has median 3.2, and the strongest partner carries 49% of the second moment M2.

4. With 1/r^3 
- **Evidence (abridged):** LOCAL (repo data; no new jobs were launched because CPU was at 98% from running G1 jobs; only numpy post-processing).

(E1) research/results/RAW/nmr_gate/1UBQ_p19_N10_o0_g1000.json, the only production C1 v2 point:
- Sparse Pauli |c| >= 1e-4 reproduces the sector-exact S_ab(t) at all 17 time points up to 320 us. Its maximum bias is 0.0025, below sigma = 0.01. The best-adversary hard-window fraction is 0 for all 4 parameters, so K-C1a fires under the stricter pre-registered rule.
- The naive pre-registered w=4 statistic gives a hard-window fraction of 0.99. That is exactly the "apparent quantum win" that disappears under a stronger classical control.
- As noted in the counterargument, this win is not evidence about scaling.

(E2) Where the Fisher information sits. For radial_HA/GLU16 (FI_total = 485), 95% of the FI accumulates at t >= 60 us, with the median near 110 us. By about 100 us, S_ab has reached finite-cluster plateaus of 0.03 to 0.125, close to 1/N.

(E3) Embedding attack, computed from data/instruments/nmr/1UBQ_H.pdb (629 H, 73 amide probes):
- The 3 farthest cluster protons carry C1's long-range parameters. For N = 10 to 30 they get a median 58 to 65% of their dipolar M2 from protons outside the cluster, with sqrt(M2_out) = 5.3 to 5.8e4 rad/s.
- For probe 19 at N=10 the figures are 70% and 9.1e4 rad/s, so these protons couple to the bath in about 11 to 19 us. That is 50 to 90 times faster than the pre-registered gamma = 1000 s^-1.
- The physical plateau is about 1/6

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0. No separation exists for this instance family: infinite-temperature 2-point or OTOC correlators of a secular dipolar Hamiltonian on protein 1H geometries, with T2-type dephasing and σ = 0.01 readout. Generic BQP-completeness of local Hamiltonian simulation does not carry over to it. As stated, C3-a is false for the instrument's own noise model. Pure dephasing damps only the X/Y factors of a Pauli string, and Z-strings are undamped. Total Z is conserved, so high-weight Z-strings are the slow hydrodynamic modes. The bound has to count X/Y factors, not weight. Even when corrected, it is weak 
- **Practical level:** L0. No run has shown any classical failure. The only valid pre-registered v2 row is N = 10 at γ = 1000 s⁻¹. There, sparse Pauli dynamics at ε = 1e-4 reproduces the exact signal over the whole 320 µs window with max bias ≤ 0.0025 (σ = 0.01) and at most 5.4e4 strings. frac_hard_best = 0 for all 4 parameters and the gain spectrum is 1.0. The sector-exact solver (35.6 s) was cheaper than every adversary (up to 268 s). An end-to-end inference would take 10²–10⁴ years at 170 µs per Toffoli (see break_even). Two data or model oracles also erase the premise:
- The Hamiltonian is treated as known apart
- **Cost / break-even note (abridged):** Per-geometry forward model with a first-order Trotter circuit identical to the instrument's: dt = 2 µs, 160–640 steps, 1H cutoff 6 Å. Each XXZ pair gate costs about 32 Toffolis (2 distinct rotation angles × 16 Toffolis using a phase-gradient register). Toffolis per step = number of pairs × 32.

**Resource counts at 160 steps (640 steps is 4× the Toffolis)**

| N | Logical qubits | Pairs within 6 Å | Toffoli per step | Toffoli per shot | One shot at 170 µs | One shot at 1 µs |
|---|---|---|---|---|---|---|
| 14 | ~34 | 77 | 2.5e3 | 3.9e5 | 67 s | 0.4 s |
| 60 | ~80 | 656 | 2.1e4 | 3.4e6 | 9.5 min | 3.4 s |
| 240 (320 µs light cone) | ~260 | 3,942 | 1.26e5 | 2.0e7 | 57 min | 20 s |
| 629 (all of ubiquitin) | ~650 | 11,205 | 3.6e5 | 5.7e7 | 2.7 h | 57 s |

- Logical qubits are N plus about 20 for the phase-gradient register and ancillas. Amplitude estimation would need a purified maximally mixed state, which doubles this to about 2N + 25.
- Qubitization is worse for the full protein: λt = 3.3e4 queries at about 3.4e4 Toffolis each is about 1e9 Toffolis per shot.
- Surface-code distance is about 23–27 at p = 1e-3. That is about 1e5 physical qubits at N = 60 and about 1e6 for the full p

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** L0 (formulation only). No theorem is proved. C3-a follows almost directly from known noisy Pauli-path and open-system operator-growth results. It is a no-go-style bound, not an advantage claim. As stated, C3-b and C3-c are contradicted or anticipated by 2025–2026 prior art for time-reversed (echo/OTOC) observables. A positive region would need evidence of exponential classical simulation hardness, and none exists for protein 1H networks.
- **Practical level:** L0. No quantum component has been built. In-house C1 v2 on 1UBQ H/ILE3, N=10: sparse Pauli dynamics at eps=1e-4 reproduces the transfer signal over the full 320 us window at gamma = 0, 1000 and 5000 s^-1. That gives FI_hard(best adversary) = 0 for all 4 parameters, with gain spectrum = 1. At gamma=0 this takes 1.66e5 strings, 90% of the C(20,10)=1.85e5 sector, so N=10 is effectively exact enumeration and says nothing about hardness. OTOC observables at gamma=0 keep frac_hard = 0.85–0.97 even against eps=1e-4, but only at N=10, where exact simulation is trivial. Practical relevance to protein s
- **Novelty note (abridged):** Search scope: arXiv API title and abstract searches plus id_list verification on 2026-09-27, plus literature-phase records F30–F39 and NM-1. General WebSearch was unavailable because the budget was exhausted, so non-arXiv journal-only work may be missed. Under that scope, the search found no paper that bounds the parameter Fisher information carried by weight>w Heisenberg components under per-order dissipation for dipolar NMR networks. It also found none that tests that bound on protein 1H networks against an explicit classical-adversary panel.
The components are prior art:
- C3-a ≈ Schuster–Yao 2022 / Schuster–Yin–Gao–Yao 2024–25 / DAOE / Mele 2024, specialised to Fisher information
- C3-b ≈ Holmes 2021 + O'Brien 2022, and it is qualified or contradicted for echo observables by F30 (2025), Gjonbalaj et al. 2026 and scrambling-metrology results (2023, 2026)
- C3-c ≈ F30's 'edge of ergodi

## QM-22: Other spectroscopic and scattering forward models whose exact simulation is classically polynomial or whose hard part is fold-uninformative (liquid-state NMR/QABC, ZULF, EPR/DEER and bath decoherence, radical-pair cryptochromes, optical/vibrational spectra, diffraction/multislice)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 (formulation only). No query or complexity separation exists for any QM-22 forward model at protein scale. In the dominant regimes, classical simulability is structural. (a) High-field liquid NMR under the secular, weak-coupling truncation has H = sum_i w_i I_zi + 2pi sum_ij J_ij I_zi I_zj, which is diagonal in the Zeeman product basis, so spectra have closed forms. NOE is linear Solomon/Redfield dynamics in the N-dimensional longitudinal subspace. (b) Optical/vibrational exciton spectra conserve excitation number: the 1-exciton manifold has dimension N and the 2-exciton manifold N(N+1)/2, 
- **Practical level:** L0. No matched-conditions usefulness (L1) exists for any modality on any protein. Hardware demonstrations are 4-qubit acetonitrile ZULF (Seetharam et al. 2021) and few-spin radical-pair toys (Zhang/Kais 2022; Tolunay 2022; Alvarez 2024), and all of them are classically trivial. Classical codes already run at or beyond protein scale: >1000-spin ubiquitin (Edwards 2014), an exact tensor-train 15N ubiquitin spectrum (Savostyanov 2014), a converged exact 47-spin radical pair (Lindoy 2020), and MPS/MPDO radical pairs with 30–60 nuclei (Hino 2025). Measured here: one multislice step on a 512^2 grid 
- **Strongest pro-quantum rebuttal considered:** 1) Walch, Fratus, Reiner & Lesanovsky (arXiv:2609.20406, 2026) find that shot-noise cost grows only weakly with molecular size. Readout therefore does not by itself kill quantum NMR-spectrum simulation, and I concede that point. 2) The Fratus et al. cluster approximation (arXiv:2508.06448) is benchmarked for typical liquid-state regimes. Strongly coupled regimes (ZULF, low field, oriented media) are less covered, and radical-pair tensor networks stop at about 30 explicit nuclei (60 in benchmarks) under non-Markovian hopping. 3) Dense 1H dipolar networks in solids or oriented media, such as MAS proton-driven spin diffusion, really are ergodic and classically hard, and they carry contact information.

Rebuttal: (1) and (2) concern the cost of simulating spectra, not fold information. ZULF measures the same isotropic {J_ij} that high-field weak-coupling experiments give in closed form, so i
- **Evidence (abridged):** Classical adversary per modality (arXiv ids verified this session via the arXiv API; WebSearch budget was exhausted):

LIQUID HIGH-FIELD NMR/QABC:
- Quantum proposal: Sels, Dashti, Mora, O. Demler, E. Demler, arXiv:1910.14221 (QABC, small molecules).
- Classical: Kuprov, Wagner-Rundell & Hore, physics/0701294 (restricted state space, O(n^2 k), linear for protein topologies). Edwards, Savostyanov, Welderufael, Lee & Kuprov, arXiv:1402.6139 (ubiquitin, >1000 spins, with relaxation). Savostyanov, Dolgov, Werner & Kuprov, arXiv:1402.4516 (exact tensor-train 15N ubiquitin spectrum, several hundred spins). Fratus et al., arXiv:2508.06448 (cluster approximation, linear in spin count, accurate 'throughout, and even somewhat beyond' typical regimes).
- Full relaxation-matrix NOE for about 400 protons at 60 aa is one 400x400 matrix exponential, about 1e8 flops.
- Locality: sigma_ij scales as r^-6. d_HH is about 120 kHz*A^3/r^3, i.e. about 1 kHz at 5 A, and long-range NOEs are about 460x weaker than 1.8 A geminal pairs.

ZULF:
- Quantum: Seetharam et al., arXiv:2109.13298 (4 qubits, acetonitrile). Burov & Javerzac, arXiv:2608.20250 (Heisenberg-NMR compilation). The 'Elenewski qubitised ZULF' work was not found on arXiv and is unverified.
- Parameter-identity argument: H = 2pi sum J_ij I_i.I_j carries no parameter that high-field first-order J spectroscopy lacks.
- The residue clustering (1J_CH/NH 90–140 Hz and 1J_CC 35–55 Hz inside residues, versus about 11–15 Hz 1J_NCa/1J_C'N between t

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 (formulation only). None of the six modalities has a separation at protein scale, even under a query model. The only known exponential-cost regimes are small, strongly coupled molecules, radical pairs with 40 or more significantly coupled nuclei if semiclassical and typicality methods fail, and hard ZULF J-graph dynamics. The first two are not protein-fold problems. For ZULF, relaxation limits the observable window to a short light cone (see evidence), which makes it classically tractable (INFERENCE, test below). For fold-level structure, the value term is about zero in every modality, so n
- **Practical level:** L0. Using Babbush 2021 / Sanders 2020 assumptions (170 µs per Toffoli, one factory), every quantum forward evaluation takes months to millennia. The best classical method takes 0.5 s to hours, or the output carries no tertiary-fold information. No hardware advantage: the NMR/EPR/EM sample is already the physical analog simulator, and it measures about 1e17 spins per shot where a qubit register gives one ±1 outcome.
- **Cost / break-even note (abridged):** Break-even condition: C_Q < C_C and ΔI_fold > 0, where ΔI_fold is the fold-coordinate Fisher information of the exact forward model minus that of the best classical approximation. Every modality fails at least one side.

| Modality | Quantum cost | Best classical | Outcome |
|---|---|---|---|
| ZULF, 60 aa | ~1.1e12 Toffolis per (time point, geometry): 6 yr at 170 µs, 13 days at 1 µs; 30-point FID 182 yr / 1.1 yr; ~900 logical and ~2e6 physical qubits; inference needs ≥ 1e2-1e4 such evaluations, so ≥ 1e3 yr | Residue-cluster expansion, minutes (INFERENCE) | Both sides fail: hardness unlikely under the ~80 Hz relaxation-limited window, and ΔI_fold ≈ 0 because couplings are through-bond only |
| DEER bath, 2000 1H | 1.5e14 Toffolis, 808 yr | CCE, seconds to hours | Both sides fail; ΔI_fold ≈ 0 |
| Radical pair, 30 nuclei | 6.8e10 Toffolis, 0.36 yr | Exact on a 350 GB node for hours, or semiclassical in seconds | Crossover needs n ≳ 40 nuclei plus semiclassical failure, and the fold value is nil anyway |
| Multislice | 2e8 Toffolis (9.4 h) per propagation; 5e17 Toffolis (2.8e6 yr) with readout | 7.4 s measured | Fails on cost; no crossover asymptotically, since readout is Ω(grid) agai

### Lens: relevance (verdict: KILL)
- **Theoretical level:** L0 (formulation only). No protein-relevant separation exists for any modality in QM-22. Generic BQP-hardness of spin time evolution does not carry over, because in each modality the fold-informative observables sit in classically closed-form sectors: the first-order multiplets, the N-dim NOE relaxation matrix, the RDC/DEER kernels, the one-exciton manifold and linear-wave multislice. The sectors that are genuinely hard carry almost no fold information: ZULF J-graphs (covalent topology), bath echo envelopes (local proton density) and radical-pair hyperfine dynamics (a few scalar yields).
- **Practical level:** L0 for proteins. All hardware NMR demos are small molecules validated against classical references: Burov et al. arXiv:2512.14513 (34 spins, IBM/IonQ), Stadler et al. arXiv:2609.17102 (21-spin effective model, H2) and Seetharam et al. Sci. Adv. 2023 (4 qubits). At most L1 for small molecules; none reaches a protein or a fold-level observable.
- **Novelty note (abridged):** Low novelty. The nearest prior art is:
- Elenewski et al. 2024/25: protein ZULF resource estimates, with no analysis of how much structural information the spectra carry.
- O'Brien et al. 2022: ubiquitin dipolar learnability, now Program C.
- Sels et al. 2020: QABC, small molecules.
- Fratus et al. 2025: classical rebuttal for liquid NMR.
- Lam & dos Reis 2026: the quantum-multislice authors concede there is no full-image advantage.

Scope of my search: arXiv API abstract searches (2019–2026) plus Crossref. No general web search was possible (budget exhausted). Under that scope, the search found no evidence of any work testing whether the classically hard sector of protein ZULF, DEER-bath, radical-pair, optical or diffraction forward models carries fold-level (tertiary) structural information.

QM-22's defensible contributions are therefore:
- (i) a negative consolidation: in isotropic s

## QM-23: Genuinely quantum-mechanical structural subproblems: strongly correlated metal cofactors (FT QPE for active-site protonation/ligand structure) and nuclear quantum effects in H-bond networks (digital Gibbs or analog emulation)

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 for the protein-structure endpoint. Branch (a), metal-site energies: L1 at most. Qubitised QPE with THC or spectrum amplification has a rigorous cost of O(lambda/eps) block-encoding calls given an overlap, but there is no proven separation from DMRG/CC/AFQMC. Lee et al. 2023 (Nat. Commun. 14, 1952, DOI 10.1038/s41467-023-37587-6) find no evidence of a generic exponential advantage. The only provable separation is against exact diagonalisation, which is the wrong comparator. Branch (b), nuclear quantum effects (NQE) in H-bonds: L0, because there is no mechanism. The equilibrium density of di
- **Practical level:** L0 for both branches. (a) At the largest biological instance (FeMoco, 7Fe+Mo, 113e/76o), classical methods have already reached the target: a CCSDTQ + DMRG composite with extrapolation reaches chemical accuracy (Zhai et al. 2026, preprint), and the quantum estimate is the same order of magnitude or slower (numbers in the break-even note). (b) Classical PIMD already "exactly include[s] nuclear quantum effects" for the flagship protein case, ketosteroid isomerase (KSI). My grid check shows P=32 reproduces the exact quantum proton density to 4e-4 Angstrom. Both effects are sub-0.1 Angstrom chemis
- **Strongest pro-quantum rebuttal considered:** The cheap classical workhorse for (a) is broken-symmetry DFT inside QM/MM, and it is unreliable. For the FeMoco E4 protonation isomers, TPSS and B3LYP relative energies differ by more than 300 kJ/mol (Cao, Caldararu, Ryde 2018). Sharma et al. 2014 showed that the Heisenberg double-exchange model undercounts Fe-S low-lying states by one to two orders of magnitude, and that same-spin levels are "dense on the scale of vibrational fluctuations". The multireference composite has only been converged on a dimer model (Zhai et al. 2023: B3LYP MAD 10 kJ/mol, max 13 kJ/mol) and on the FeMoco resting state. Hydride-bearing E4 and OEC S3/S4 could push DMRG past reach: variational DMRG at chemical accuracy already needs D~393,000 and ~4e9 core-hours at FeMoco scale, and the classical result depends on a heuristic extrapolation. QPE gives certified energies at the Heisenberg limit, and the overlap is 
- **Evidence (abridged):** (a) Zhai, Li, Zhang, Li, Lee, Chan, "Classical computational simulation of the FeMo-cofactor model to chemical accuracy and its implications", arXiv:2601.04621 (2026 preprint; I fetched the arXiv HTML):
- LLDUC (113e, 76o) model. DMRG run at D=5,000-18,000, then extrapolated.
- E0 = -22140.4106 +/- 0.0005 Ha (+/-0.31 kcal/mol). BS7-235 and BS8-237 (and possibly BS8-236) are degenerate within chemical accuracy.
- The largest UCCSDTQ composite took 40,000 core-hours (1.9 s at ideal Frontier scaling). The D=18k UDMRG took 2.77e6 core-hours (46 s at ideal Frontier scaling).
- Variational D=393k would take 4.08e9 core-hours, i.e. 22.9 h on Frontier, against a quantum estimate of 8.6 h using sum-of-squares spectrum amplification (Low et al., PRX 15, 041016, 2025, arXiv:2502.15882).
- In the (404o, 277e) composite, the gap between the lowest spin isomers is about 1.6 kcal/mol.
- Dominant-determinant overlap is 0.4468. QM/MM with MD averaging leaves the landscape qualitatively unchanged.

Other sources for (a):
- Sharma, Sivalingam, Neese, Chan, Nat. Chem. 2014, DOI 10.1038/nchem.2041: DMRG spectra of [2Fe-2S] and [4Fe-4S].
- Li, Guo, Sun, Chan, Nat. Chem. 2019, DOI 10.1038/s41557-019-0337-3: DMRG landscape of the P-cluster in three oxidation states.
- Kurashige, Chan, Yanai, Nat. Chem. 2013, DOI 10.1038/nchem.1677: DMRG on the OEC Mn4CaO5 cluster.
- Zhai, Lee, Cui, Cao, Ryde, Chan, JPCA 2023, DOI 10.1021/acs.jpca.3c06142: CC/DMRG composite protonation energetics converged in basis a

### Lens: resource (verdict: WEAK)
- **Theoretical level:** (a) Metal-cofactor fault-tolerant QPE. The only L6 support is generic, not tied to these instances. The guided local-Hamiltonian problem at 1/poly precision is BQP-complete (Gharibian & Le Gall, SIAM J. Comput. 52, 2023; repo bibliography #397). That result assumes a guiding state with 1/poly overlap supplied from outside and says nothing specific about FeMoco, P-cluster, OEC or P450. For the actual instances the supportable level is L3: published fault-tolerant resource estimates exist, and the speedup is a polynomial precision gain over exact diagonalisation. Lee et al. 2023 found no evidenc
- **Practical level:** (a) At best L1, and only for the electronic energy of one fixed candidate state. At FeMoco-LLDUC scale the per-state cost is about equal to classical when the classical side has S = 1e3 cores and the quantum side has one factory. Classical methods have already delivered this benchmark (Zhai et al. 2026, preprint). For assigning structures (protonation or ligand isomers times broken-symmetry spin isomers), the quantum cost at R = 1 factory is 3 to 9,400 years, so L0 for protein structure. (b) L0, KILL: the quantum machine cannot finish even one coherent evaluation of the potential-energy surfac
- **Cost / break-even note (abridged):** (a) Energy of one fixed state, at 170 µs per Toffoli with one factory:
- The quantum side needs 47 h to 63 days and 4 to 4.6 million physical qubits, plus about 150k more per extra factory.
- The classical side needs 4 to 40 h on 1e3 to 1e4 cores (UCCSDTQ), and has already done it.
- Break-even is about 1x at S = 1e3; classical wins 10 to 60x at S = 1e4.
- Quantum leads 10 to 80x only with R = 10 to 100 factories (more than 1.5e7 physical qubits).
Structural assignment across protonation isomers times spin isomers takes 3 to 9,400 years at R = 1 and 12 days to 94 years at R = 100. The classical equivalent takes 17 days to 3.2 years on 1e4 cores. QPE plus NEVPT2 readout takes 680 to 68,000 years even at R = 1000.
The advantage is polynomial only. None of it transmits to backbone structure.

(b) The quadratic break-even is about 1e18 classical potential calls against the roughly 3e7 actually needed, and even one quantum oracle call exceeds the whole classical run: KILL. Accounting assumptions: state preparation (about 2e-4 of a run) and THC/QROM data loading are not the bottleneck. The oracles actually doing the work are all classical: the active space, the geometries and the candida

### Lens: relevance (verdict: WEAK)
- **Theoretical level:** Protein-structure endpoint: L0 (a formulation only). There is no mechanism linking a better correlated-site energy or a nuclear-quantum ensemble to fold or backbone accuracy, and DE-7 measured energy accuracy as not the bottleneck (AMBER in-band rho 0.000). Sub-question (a), metal-site electronic structure taken as chemistry: resource-normalised fault-tolerant estimates against DMRG exist on paper (Goings et al. 2022 for P450; Zhai et al. 2026 for FeMoco), which is about L3 on paper. There is no L6 separation: QPE is efficient only given an inverse-poly overlap, and Lee et al. 2023 find no gen
- **Practical level:** Protein structure: L0. Chemistry sub-question (a): at most L1. Hardware demonstrations on exactly the proposed systems are classically matched: Sycamore on nitrogenase Fe-S cluster models (Tazhigulov et al. 2022), and IBM SQD on [2Fe-2S] and [4Fe-4S] with up to 77 qubits and 10,570 gates (Robledo-Moreno et al. 2024). Neither shows a load-bearing quantum component against DMRG. Fault-tolerant estimates are falling: about 1e10 T gates for FeMoco QPE; 89k noisy superconducting qubits for under a month on a 108-spin-orbital FeMoco model (Low et al. 2026); about 1e5 physical qubits and days to week
- **Novelty note (abridged):** This is not new relative to the program: it is M14 (WEAK / out of scope) plus M8 (KILLED) and the M1 family. It is also not new in the literature. Correlated-cofactor QPE with THC or double-factorised block encodings: Reiher 2017, J. Lee 2021, Goings 2022, Oumarou 2022, Rocca 2024, Low 2026, Kanasugi 2026, Khinevich 2026. Fe-S clusters on quantum hardware: Tazhigulov 2022, Robledo-Moreno 2024. Classical rebuttals: Lee 2023, Zhai 2026. Nuclear quantum effects on quantum computers via NEO: Kovyrshin 2023, Nykanen 2023, Cabral/Pavosevic/Hammes-Schiffer 2025. Classical PIMD of enzyme H-bond networks: Wang et al. 2014; Kapil group 2025. Within the arXiv API, PMC and repository-bibliography queries done this session, the search found no paper that connects correlated-cofactor QPE or quantum nuclear-quantum-effect sampling to a protein-structure (fold or backbone) endpoint. Coverage is partial 

## QM-24: Quantum sensing and metrology as a new per-target information source: quantum-memory / Heisenberg-limited single-molecule NV-NMR, and multi-pass / interaction-free electron microscopy

### Lens: classical (verdict: KILL)
- **Theoretical level:** (a) Quantum-memory / collective NV learning: L0, formulation only. The claimed exponential sample-complexity separation provably does not apply to this task class. For one geometric parameter, a single-copy measurement reaches the full QFI (Braunstein–Caves). For two-hypothesis fold discrimination, the collective-to-single-copy Chernoff-exponent ratio is at most 2 for any pair of states. For the NV pure-dephasing states actually produced, the ratio is exactly 1.000, because the states commute. (b) Multi-pass / interaction-free TEM: L1 as a metrology claim under an idealised model. Information 
- **Practical level:** L0 for both. (a) No single-protein structure or fold assignment by NV-NMR exists. In my toy model the cost is set by NV–nucleus distance (signal falls as r^-6 in the exponent), sensor T2 and readout efficiency, not by the measurement strategy. (b) No electron multi-pass microscope has been demonstrated (Juffmann et al.: 'a multi-pass TEM still has to be demonstrated'). The only published design runs at 10 keV and re-images to within 4 nm. At 10 keV in 20 nm vitreous ice the gain is G_max ≈ 1.3. That meets the candidate's own kill criterion N_eff < ~3.
- **Strongest pro-quantum rebuttal considered:** Part (b) at 300 keV (or 100 keV) is a real order-of-magnitude gain in information per dose that no single-pass classical trick can reach. Zernike phase contrast is the single-pass optimum for weak phase objects, and Koppell et al. 2022 argue the quantum limit is at least 10x beyond aberration-free Zernike. With G ≈ 10, the Henderson-type alignment threshold (~38 kDa) would fall roughly as 1/G, to ~4 kDa. That would allow per-molecule heterogeneity analysis of unscaffolded 10–40 kDa particles. Ensemble NMR (averaged), smFRET (a few distances), scaffolds (perturbing) and AF2 (single structure) cannot fully replace this. So the kill of (b) rests on engineering (no 300 keV gated, aberration-compensating electron mirrors) and on scope (it is information acquisition, not computation, and the project's 1–7 kDa targets are already solved classically), not on physics. For (a), a memory advantage 
- **Evidence (abridged):** ADVERSARY RESULTS (derivations run in scratchpad: ...\scratchpad\chernoff_check.py and ...\scratchpad\nv_cpmg.py).

(a1) Collective vs single-copy discrimination. The fidelity-achieving measurement gives Bhattacharyya coefficient = F, so the classical exponent xi_C ≥ -log F. Log-convexity of s ↦ Tr ρ^s σ^(1-s) together with Q ≥ F² gives xi_Q ≤ 2 xi_C. Numerically, xi_Q/(-log F) peaked at exactly 2.0000 over 450 random pairs (d = 2..16); the maximum occurs for pure states, where the true ratio is 1. Over 200 random mixed qubit pairs, the maximum xi_Q / xi_C(best projective) was 1.53. So the candidate's kill criterion (ratio < 2x) holds for every pair of states, whatever the hardware.

(a2) NV toy: 12 thermal protons, B0 = 0.05 T, CPMG resonant with the 1H Larmor frequency, 4 protons moved by 2–5 Å between fold A and fold B, T2_DD = 500 us, room-temperature readout efficiency 0.03 (assumed). The symmetric DD signal on an unpolarised bath is real, so both hypotheses' sensor states lie on one Bloch axis and commute. The collective/single-copy ratio is 1.000 in every configuration. Shots to 1e-3 error: 4e5 (~26 s) at 3 nm depth, 7.7e6–1.1e7 (~0.5–0.7 h) at 4 nm, 7.5e8 (~8 days) at 5 nm. The bottleneck is distance, T2 and readout, not quantum memory.

(a3) Heisenberg-limited scaling needs neither quantum memory nor entanglement:
- Higgins et al., Nature 450:393 (2007), arXiv 0709.2996 [verified]
- Huang–Tong–Fang, PRL 130:200403 (2023), arXiv 2210.03030: O(1/ε) total evolution time

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 as a quantum-over-classical advantage. (a) Quantum-memory NV-NMR: there is a derived no-go. The gain from joint or multi-copy measurement is exactly 1 in the unpolarized-nucleus regime, at most 1.39x in the polarized regime, and there is no Heisenberg scaling beyond T2. (b) Multi-pass or QEM TEM: the gain is a real metrology result. Information per damage event scales as G(N,l) = N^2 s^(N-1) l/(1-s^N) with s = 1-l, and the maximum is about 0.65/l. That puts it at roughly L1 as a sensing and instrument claim. It is coherent phase accumulation of a single particle, which has a classical-wave 
- **Practical level:** L0. (a) Memory-assisted joint measurements on a biomolecule near a shallow NV have never been realised. Coherent sensor-to-memory transfer with i.i.d. "copies" of one molecule is a hidden oracle, and even if it were free it would buy at most 1.39x. (b) Multi-pass electron microscopy is at the design or prototype stage; I could not verify its current status this session. At the proposed ~10 keV operating energy, per-pass inelastic loss in vitreous ice alone is 0.36-0.60 for 10-20 nm of ice, which gives N_eff of 2-4 and G_max of 1.1-1.8. Even at the ideal G, the program's targets (9-60 aa, 1-7 k
- **Cost / break-even note (abridged):** No fault-tolerant computation is involved, so the Babbush/Sanders Toffoli break-even model (170 µs per Toffoli) does not apply. The coherent processing is about 10 gates, and the whole cost sits in physical transduction and measurement count. The break-even quantity is the number of experiments, or the dose, per unit of information.

- **(a) Break-even for the joint-measurement protocol:** it beats adaptive single-copy measurement only if Chernoff ratio x F^(2k) > 1.
  - Unpolarized, commuting regime: the ratio is 1, so there is never a break-even.
  - Polarized regime: at a ratio of 1.39 or less, with k = 2, this needs F > 0.92. The maximum net gain is 1.13x at F = 0.95 and about 1.3x at F = 0.99.
  - This is against about 20-85 s per NV-to-label distance restraint with conventional methods, and those give only NV-to-label distances, not intra-protein ones.
- **(b) Break-even in dose:** G_max is about 0.65/l. Getting 3x or more needs per-pass loss l of about 0.2 or less, which requires 100 keV or more with ice of 20 nm or less and optics loss per pass of 5% or less (unverified). The 10 keV designs give G of 1.8 or less.
- **Endpoint relevance:** the program's 1-7 kDa targets need 

### Lens: relevance (verdict: KILL)
- **Theoretical level:** L0 for any computational claim. (a) is refuted on paper. The candidate's claimed mechanism is exponential savings from quantum memory or joint multi-copy measurement. That does not apply to protein geometry, for two reasons. First, the target has a polynomial description: S29-S33 found a≡mu, about 3n-6 numbers per target, and local Hamiltonians are learnable with poly(n) single-copy samples (Anshu et al., arXiv:2004.07266). The proven exponential separations (Chen-Cotler-Huang-Li arXiv:2111.05881; Huang et al. Science 2022 arXiv:2112.00778; King-Wan-McClean arXiv:2403.03469) need property fami
- **Practical level:** L0. (b) The arXiv search found no experimental multi-pass TEM image and no electron interaction-free measurement; there are only designs and simulations (Kruit et al. arXiv:1510.05946; Juffmann 2016/17; Koppell et al. 10 keV design arXiv:1904.11064; Agarwal-Berggren-Goyal arXiv:1901.09702). N_eff for electron optics is unmeasured. (a) No single-protein structure (distances or fold state) from NV-NMR was found. The most advanced biomolecular results are the single-ubiquitin 2H/13C signal detected with quantum logic (Lovchinsky et al. Science 351:836, 2016, doi:10.1126/science.aad8022; signal on
- **Novelty note (abridged):** Scope: arXiv API and PubMed E-utilities, 2026-09-27; general web search unavailable. The search found no evidence of a work that (i) quantifies single-copy versus multi-copy (quantum-memory) Fisher or Chernoff information for protein geometric parameters or fold identity with an NV sensor, or (ii) ties a multi-pass or quantum electron microscope gain G to the sub-40-kDa alignment threshold with an explicit G-sweep. Both would be incremental syntheses. Every physical mechanism is prior art:
- NV single-molecule structure: Cai 2013; Ajoy 2015; Kost 2015; Lovchinsky 2016; Pfender 2017.
- Quantum-memory learning: Chen-Cotler-Huang-Li 2021; Huang 2022.
- Heisenberg Hamiltonian learning: Huang-Tong-Fang-Su 2023; Dutkiewicz 2024.
- Quantum-computing-enhanced NV sensing: Allen et al. 2025; Xu et al. 2026.
- Multi-pass/IFM TEM: Kruit 2016; Juffmann 2017; Koppell 2019/2022.
- Quantum electron micr

## QM-25: Quantum topological invariants: Jones/Khovanov knot invariants of protein chains (AJL, DQC1) and quantum topological data analysis (LGZ Betti numbers, hole persistence, Mayer homology) of structures and ensembles

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 on protein-derived instances: a formulation only. Complexity results exist, but on the wrong instances. AJL/Shor-Jordan show additive Jones approximation is BQP-/DQC1-complete. Gyurik et al. 2024 show guided persistence is BQP1-hard. Nghiem et al. 2026 prove an exponential separation for Mayer homology, but only against enumeration and only on a synthetic cone family of order k=Theta(n). All of these hold on instance families disjoint from protein data. On protein-derived families (derivations D1-D4 in evidence), exact classical algorithms run in polynomial time, often near-linear. The poss
- **Practical level:** L0. There is no instance where a quantum topological-invariant computation is useful under matched conditions for protein structure. Protein knot diagrams sit more than 400x below the quantum-Jones crossover in crossing number. Protein persistent homology has k<=2 and is computed exactly classically in seconds.
- **Strongest pro-quantum rebuttal considered:** The best case for the quantum side is Nghiem, Babbush, Zalcman, Berry, Phan, Wei, Hayakawa, arXiv:2609.28058 (posted 2026-09-23, not yet peer-reviewed). It claims that Mayer Betti numbers (d^N=0, xi=e^{2 pi i/N}) of dense high-order complexes can be exponentially large, which removes the normalisation bottleneck of LGZ. It also argues that dequantisation guarantees (Apers et al.) break down there, and estimates about a few hundred logical qubits and 6e7 Toffolis beyond known classical methods. Protein heavy-atom Rips complexes at 10-12 A really are dense: cliques hold about 54-93 atoms, so C(90,45) ~ 1e26 simplices per neighbourhood, which enumeration cannot reach. Mayer Laplacians have been used on biomolecular data (Wei group). So a protein-derived family with a real exponential gap over enumeration is conceivable.

Rebuttal:
(i) The exponent sits in the cutoff volume rho*r^3, which is
- **Evidence (abridged):** VERIFIED this session via the arXiv API, Europe PMC or abstract pages:
- Aharonov-Jones-Landau, quant-ph/0511096 (STOC 2006).
- Shor & Jordan, 0707.2831, QIC 8:681 (2008): Jones estimation is DQC1-complete.
- Kuperberg, 0908.0512, Theory Comput. 11:183 (2015): 'any value-dependent approximation of the Jones polynomial at these non-lattice roots of unity is #P-hard'.
- Laakkonen, Rinaldi, Self, ..., Meichanetzidis, 2503.05625, PRX Quantum 7:020355 (2026):
  - Markov-closure additive error is eps*phi^{n-2}.
  - The classical mpo-proj algorithm on Frontier becomes slower than the quantum algorithm only for c>=2800 crossings, at a two-qubit error rate of 1e-4 and about 40% relative error.
  - Classical methods hit memory limits first.
  - The H2 demo used 16 qubits, 340 two-qubit gates and 4000 shots.
- Maria, 1910.00477: Reshetikhin-Turaev invariants in O(N^{3/2 cw} poly(n)), so exact computation is fixed-parameter tractable in cutwidth.
- Schmidhuber & Lloyd, 2209.14286, PRX Quantum 4:040349 (2023): exact Betti numbers are #P-hard and multiplicative approximation is NP-hard. LGZ is quadratic 'in asymptotically almost all cases'. Exponential advantage needs simplices given explicitly, not a vertex/edge list.
- Berry, Su, Gyurik, ..., Babbush, 2209.13581, PRX Quantum 5:010319 (2024): super-quadratic speedup needs multiplicative error and growing Betti numbers. Exponentially large dimension and Betti number are 'necessary, but insufficient'. Seemingly intractable instances need 't

### Lens: resource (verdict: KILL)
- **Theoretical level:** L0 for the protein formulation. The abstract results are L6 for their own problems: additive Jones approximation at the 5th root of unity is BQP-complete for plat closure and DQC1-complete for trace closure, and LGZ-type Betti estimation has query-model guarantees. None of these carries over to protein data. The quantum algorithms only guarantee an additive window of eps*phi^(n-2) (Markov closure) or eps*phi^(n/2-3/2) (plat closure) on V, or eps*|S_k| on beta_k. When the answer is O(1), as for every protein knot (|V(7_1)| <= 7) and for every Betti number measured on learned-energy ensembles (b
- **Practical level:** L0. At protein scale the classical side wins by 7-8 orders of magnitude in wall-clock. Example: 7_1 on Q9PR55 costs about 1e-7 s on a classical transfer matrix, versus 2-4 s of fault-tolerant runtime at 170 us per Toffoli, and classical returns the whole polynomial, not one additive value. The fault-tolerant break-even lies at irreducible diagrams with >= 24-43 Seifert circles/strands, costing 0.46-16 years per crossing at 170 us per Toffoli. The NISQ DQC1 break-even from the Quantinuum pipeline is >= 2800 crossings. Proteins give <= 8 crossings and <= 3 Seifert circles. Betti estimation on RM
- **Cost / break-even note (abridged):** Knots, fault-tolerant, eta = 0.1 on V:
- break-even at n* = 39 strands (t_T = 170 us, 100 Toffolis per crossing), costing 0.46 yr per crossing on both sides;
- n* = 43 at 500 Toffolis per crossing (15.7 yr per crossing);
- n* = 29 at 1 us;
- n* = 24 at 100 ns.
- Knots, NISQ DQC1: Laakkonen et al. put the crossover at >= 2800 crossings, and classical methods run out of memory before they become slower.
- Proteins: <= 8 crossings and <= 3 Seifert circles, so the gap is >= 350x in crossings and >= 8 strands short even at 100 ns per Toffoli. On top of that, the Alexander determinant, which runs in polynomial time, settles identification in < 1 ms.
Betti numbers:
- N = 1e4 conformers, k = 3: 1.7e13-1.7e14 Toffolis = 94-936 yr at 170 us, plus 1e8 classical RMSDs to build the oracle.
- The quantum side wins only if the classical approximate topological-data-analysis cost exceeds about 1e2-1e3 years and beta_3 is the scientifically needed quantity. Neither holds.
Verdict: the crossover is astronomically far, and the additive window erases the speedup in the regime that is informative for proteins.

### Lens: relevance (verdict: KILL)
- **Theoretical level:** Generic complexity separations exist, but none on protein inputs. They are L6 (worst-case/complexity-theoretic) in their own input models: AJL plat-closure Jones approximation is BQP-complete, trace-closure is DQC1-complete (Shor-Jordan), guided hole-persistence is BQP1-hard (Gyurik et al.), and Khovanov-rank approximation is DQC1/BQP-hard (Schmidhuber et al.). Every one of these needs large, high-treewidth braids or clique-dense complexes with non-negligible normalized Betti numbers, and protein data supplies neither. For protein chains and protein point clouds and ensembles the level is L0: 
- **Practical level:** L0. The search found no quantum evaluation of a protein chain's or ensemble's topological invariant on any hardware or simulator. The Quantinuum H2-2 Jones pipeline works on generic links and says quantum advantage needs 'a candidate set of links' to be supplied. On every protein instance I looked at, classical exact computation is trivial (under 1 s for knots; seconds to minutes for k<=2 homology).
- **Novelty note (abridged):** The search found no evidence of any quantum topological-invariant computation (Jones/Khovanov via AJL/DQC1; Betti/persistence via LGZ, guided persistence or Mayer) applied to protein chains, structures or conformational ensembles. Scope: arXiv API and Europe PMC queries, Sept 2026, with the web-search budget exhausted, so publisher-only venues are not covered. On the topology side the nearest prior art is classical: AlphaKnot 2.0, Topoly, KnotProt 2.0, Panagiotou-Kauffman open-chain Jones, and Wei-group persistent Jones and Mayer homology. On the quantum side it is generic TDA and knot algorithms, plus Nghiem et al. 2026, which already proposes quantum Mayer homology with drug discovery as an application. So the only protein-adjacent quantum angle is preempted, and a 'first quantum knot invariant of a protein' demo would be novel in an empty way: a small, classically trivial instance. Th

## QM-26: Exponential quantum simulation of coupled classical oscillators (Babbush et al.), quantum elastic network models and Koopman-von Neumann MD for protein mechanics

### Lens: classical (verdict: KILL)
- **Theoretical level:** L0 for the protein instance family. L6 holds only for the non-geometric oracle family: glued trees and the BQP-complete circuit construction, where Babbush et al. themselves note that the "interactions between oscillators are not spatially local". For elastic networks embedded in 3D space with a distance cutoff and a minimum node spacing, the graph has polynomial growth, so the separation is provably at most polynomial. A local observable costs classically O((w_max*t)^4*d) (Chebyshev/Verlet on the light-cone ball) against quantum Omega(w_max*t) (no fast-forwarding). A global intensive observab
- **Practical level:** L0. The measured classical cost of exact propagation, with every observable available at once, is about 1.3 CPU-hours at 1e6 nodes for a full crossing of the assembly. Extrapolated to 1e8 nodes it is about 600 core-hours (about 10-20 core-hours after 60-fold icosahedral symmetry or rigid-block reduction). The quantum cost of one scalar at 1% precision is about 1.3e11 Toffolis at 1e6 nodes and 6e12 at 1e8. That is 1.5 d and 70 d at an optimistic 1 us per Toffoli, or 0.7 yr and 33 yr at 170 us per Toffoli (one factory). No protein-structure endpoint is served. The elastic network needs the nativ
- **Strongest pro-quantum rebuttal considered:** The strongest case for quantum is the procedural sub-regime: a perfect capsid or crystal lattice (symmetry makes the coordinate oracle cheap) plus defects drawn from a pseudorandom hash. There the quantum walk keeps a real speedup of about the light-cone volume (T^3 in 3D, so classical ~T^4 against quantum ~T). That is "quartic" in the sense of Babbush et al. (PRX Quantum 2021), which they call far more practical than quadratic. My break-even model, using the measured light-cone front v ~1.5-2.5 Å/unit and 0.55 us per node-step, puts crossover at light cones of 5.7e6 nodes (855 Å radius, ~6 h single core) with 1 us Toffolis and one classical core. With 8 cores it is 4.6e7 nodes. At 170 us Toffolis it is 1e9-8e9 nodes, and 1e12 against a 1000-core classical machine. The QENM graphene paper (arXiv:2601.05161) makes the analogous 2D claim: cm-scale sheets with ~160 logical qubits. So an exa
- **Evidence (abridged):** VERIFIED LITERATURE (arXiv API / Crossref / full-text grep this session):
- Babbush, Berry, Kothari, Somma, Wiebe, PRX 13, 041041 (2023), arXiv:2303.13012. Abstract: the speedup requires that "individual masses and spring constants can be efficiently queried, and ... the initial state can be efficiently prepared".
  - Conclusion (verbatim, from the full text): "only efficient for computing particularly large or global properties and when masses and spring constants can be computed in time polylogarithmic in system size ... complexity is (almost) linear in the evolution time t ... This would discourage applications where ... N = poly(t) ... expected to arise when simulating physical systems with geometrically-local interactions, and for initial states that are locally supported ... light cone, whose size in D spatial dimensions would scale as N ∝ t^D. Nevertheless ... significant quantum speedups (e.g., super-quadratic)."
  - Sec. VI: its hard instances "may seem artificial (e.g., resulting interactions between oscillators are not spatially local)".
- Cramer, Serafini, Eisert, arXiv:0803.0890; Nachtergaele, Raz, Schlein, Sims, CMP 286, 1073 (2009), arXiv:0712.3820. Lieb-Robinson bounds for harmonic lattices.
- Danz et al., arXiv:2405.08694. QPE response functions; query complexity O(s||H||max/(delta^2 eps)). Its exponential example is the random glued trees.
- Kolotouros et al., arXiv:2601.05161 (QENM, graphene, ~160 logical qubits; comments say it was extended to defects). It

### Lens: resource (verdict: KILL)
- **Theoretical level:** L6 holds only for the abstract, non-protein problem: Babbush-Berry-Kothari-Somma-Wiebe (BBKSW) oscillator dynamics with 2^n oscillators and oracle couplings, a 2^{Omega(n)} classical query lower bound, BQP-complete. For any protein-instantiated task the level is L0, and I derived two no-go results. (1) Explicit elastic-network (ENM) data: loading the spring and neighbour data costs Theta(E) Toffolis per query with QROM (linear-cost lookup table), or Theta(sqrt(E*M)) Toffolis plus Theta(sqrt(E*M)) logical ancillas with QROAM (qubit-for-Toffoli trade-off variant). The query count Theta(omega_max
- **Practical level:** L0. For explicit ENMs, quantum loses at every protein-relevant size by 10^2-10^6x. For the procedural residual the model is physically invalid for proteins, and damping destroys the encoding (see the break-even note).
- **Cost / break-even note (abridged):** Explicit protein ENM, the only data-faithful protein instance. With linear QROM, quantum is 5.9e3x slower per step (170 us Toffolis vs 0.93 us per node-step classically, N-independent) and 1.8e6x slower after pi/eps readout, so it never breaks even. With QROAM, break-even is N* ~ 6e13 nodes (1 core, 170 us, eps = 0.01) with ~5e8 logical qubits, rising to 6e19 against 1e3 cores. Every protein assembly is <= 1e8-1e9 nodes, and 1e8 nodes costs 78 core-hours classically. Procedural 3D networks: the finite corner (K* ~ 4e3 hops, months per scalar at 170 us; ~8e3 hops, ~3 days per scalar only with 100 parallel factories against 1e3 cores) rests on an undamped harmonic model that has no protein-science meaning, and damping adds an e^{gamma t} penalty. The oracle erases the exponential in the explicit case, and Euclidean locality caps it at polynomial in the procedural case. The prior stays ~0 for proteins.

### Lens: relevance (verdict: KILL)
- **Theoretical level:** For protein instances: L0, with published no-go results that rule out an exponential advantage. L6 (exponential query separation, BQP-complete) holds only for the non-protein family of 2^n oscillators whose springs are defined by an oracle or circuit (Babbush et al. 2023). Two published results block the transfer to proteins. (a) Liu et al. 2024 (arXiv 2411.03972), Thm S1.10 as reported by the fetch summary: an efficient connectivity oracle exists only when the Kirchhoff/Hessian matrix K has a polylog(N)-bit description, and the paper states that the K matrix for protein MD "does not satisfy t
- **Practical level:** L0. No L1 evidence exists for any protein task. The one protein paper (Liu et al. 2024) has no runtime comparison with a classical method; its numerics use Crambin (1360 atoms) and Chignolin. QENM (Kolotouros et al. 2026) covers graphene only, and the KvN Green-Kubo and Langevin papers (Watanabe et al. 2026) cover H2 only. The break-even model below puts crossover at or above the largest CA-level protein assemblies (about 1e5-1e7 nodes; this size range is approximate and was not verified this session), except against a single-core adversary under optimistic hardware. The observables the candid
- **Novelty note (abridged):** Not novel. Four pieces of prior art cover it. (1) The protein application of Babbush-type oscillator simulation, meaning quantum GNM/NMA dynamics for proteins with DOS, mode and correlation readouts, is Liu, Li, Wang and Liu, arXiv 2411.03972 (2024), which is already in the project literature as B58/D69. (2) QENM is Kolotouros et al., arXiv 2601.05161 (2026), graphene only. KvN MD with QPE/AE readout of Green-Kubo coefficients is Watanabe et al., arXiv 2605.30142 and 2605.30143 (2026), H2 only. (3) QM-26's own kill arguments are also prior art: the data-loading no-go is Liu et al.'s Thm S1.10; the locality no-go is Schade et al., arXiv 2609.20721 (Sep 2026); the chaos no-go is Lewis et al., Quantum 2024. (4) The project already recorded "no advantage (QM-26)" in research/theory/COMPLEXITY.md. What QM-26 adds is only project-specific: the explicit N* break-even envelope and a light-cone c

