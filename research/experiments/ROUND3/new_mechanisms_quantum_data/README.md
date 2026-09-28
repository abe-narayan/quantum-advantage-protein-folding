# ROUND3 lane: new mechanisms, lens B — quantum data (learning with quantum memory)

_2026-09-28. Question: can protein structure determination consume quantum data coherently (NMR/ESR spin states, single molecules via NV centres, transduced into a quantum memory/processor) so that a structure-relevant property is learned with exponentially fewer experiments than any measure-first protocol? Tags: MEASURED (this folder), DERIVED (proved here, validated numerically), THEORETICAL / LITERATURE-SUPPORTED (cited, arXiv abstract verified this session unless marked), INFERENCE, UNPROVEN._

**Verdict: KILLS.** No protein-structure learning task sits in a proven exponential quantum-memory separation class with a realisable path.

- The one protein task that is formally in a proven separation class is OTOC/echo learning. Its separation is with vs without **time reversal**, and the NMR spectrometer already provides that without any quantum computer. That route is K-105.
- For the real target (a finite set of geometric parameters), quantum memory gives **exactly 1×** per parameter, for any polarisation and time [THEOREM].
- Across several parameters it gives at most the parameter count k. The measured upper bound is 2.9–9.5 [MEASURED/DERIVED].
- The canonical memory protocol behind the separations (Bell sampling) reaches at most 0.33× the best single-copy protocol (median 0.0026×, 5–320 µs), even at polarisation p = 1. At thermal NMR polarisation that factor is multiplied by a further p² ≈ 2×10⁻⁹ [MEASURED].

## 1. Proven separation classes and whether a protein task maps onto them

| Proven separation (verified) | Size | Protein analogue | In class? | Why not / what fails |
|---|---|---|---|---|
| Predict all 4ⁿ Pauli expectations / \|tr(Pρ)\|. No memory: Θ̃(2ⁿ/ε²). Full memory: O(n/ε⁴) by Bell sampling. HKP PRL 126, 190505 (arXiv:2101.02464). Chen–Gong–Ye arXiv:2404.19105. Chen–Cotler–Huang–Li arXiv:2111.05881 (Ω(min(M,2ⁿ)) without memory) | exponential | Pauli spectrum of the evolved NMR state ρ(t) | formally yes, but it is **not the structure task** | Structure is k ≈ 3N numbers (§3). With ε = η·p, memory helps only if 2ⁿ(ηp)² > n. That needs **n ≥ 41 spins** at thermal 600 MHz (η = 0.1), n ≥ 48 at η = 0.01, and n ≥ 10 at p = 1 [DERIVED, `summary.json: hkp_crossover_n_star`] |
| Pauli-channel eigenvalues. Ancilla-free Ω(2^{n/3}), later tight Θ(2ⁿ/ε²); entangled O(n/ε²). Chen–Zhou–Seif–Jiang PRA 105, 032435 (arXiv:2108.08488). Chen–Oh–Zhou–Huang PRL 132, 180805 (arXiv:2309.13461) | exponential | protein spin bath acting as a noise channel on an n-sensor register (NV centres, spin labels) | **no** | The secular sensor–bath coupling is pure dephasing, so the channel is a **Z-type (commuting) Pauli channel**. Prepare \|+⟩ⁿ, read out in X, and each shot returns an error string, so all 2ⁿ eigenvalues come to ±ε in O(n/ε²) rounds with no ancilla [DERIVED]. The non-commuting admixture is (ν/D)² ≈ 10⁻¹² for an NV at 3 nm [DERIVED, `physics.json`]. Consistent with QM-24 (commuting sensor states, ratio 1.000) |
| Purity/mixedness testing, symmetry class (time reversal) of U, principal component of ρ. Huang et al. Science 376, 1182 (arXiv:2112.00778). Aharonov–Cotler–Qi (arXiv:2101.04634) | exponential | none | **no** | No structural content. The time-reversal class of the dipolar H is known a priori |
| OTOC-learnable properties need exponentially many time-ordered experiments. Cotler–Schuster–Mohseni arXiv:2208.02256. Schuster et al. arXiv:2208.02254 | exponential (time reversal vs none) | ¹H dipolar echo, OTOC(1) (R1) | **yes, formally** | The separation is time reversal vs none, **not memory vs none**. NMR magic/polarisation echoes supply the time reversal physically, so no quantum computer is needed. The route is K-105 (reversal horizon T3 ≈ 4–6.7 T2; gain 1.1–1.5; value). See §4 for the size of the coherent-processing gain |
| Hamiltonian learning with Heisenberg scaling: O(ε⁻¹) total evolution time. Huang–Tong–Fang–Su arXiv:2210.03030 | quadratic in ε | dipolar couplings | no exponential | No memory needed. Polynomial. Precision is capped by the coherence time (QM-24 a3) |
| Local-Hamiltonian learning from Gibbs states: poly(N) samples, single copy. Anshu et al. Nat Phys 2021 (arXiv:2004.07266). Haah–Kothari–Tang Nat Phys 20, 1027 (arXiv:2108.04842), O(log N/(βε)²). Bakshi–Liu–Moitra–Tang arXiv:2310.02243 | none needed | thermal NMR state (high temperature) | **no** | Measure-first learners are already sample-efficient for local geometric Hamiltonians |

## 2. Concrete calculation: protein ¹H clusters, with vs without quantum memory [MEASURED]

**Instance.** Dense ¹H clusters from the repo instrument: 1UBQ probe 19 at N = 10 and 12; 1UBQ probe 245 at N = 10 and 12; 1PGA probe 390 at N = 10; and a 9-parameter all-radial variant of 1UBQ p19 at N = 10.
- Geometry, B0 orientation and structural parameters are identical to `scripts/nmr_gate.py`: radial shifts of the three most distant protons plus one rigid residue shift, finite difference h = 0.05 Å.
- Hamiltonian: secular dipolar H, **exact** sector propagation with no Trotter error.
- State: the selective-polarisation NMR state ρ(θ,t) = (I + p·X)/2ᴺ, with X = U Z_probe U†.
- Times: 5–320 µs. There are 162 (parameter, time) cases at t ≥ 10 µs.

**Exact identities [DERIVED; validated against brute force to 1e-15 in `validate.json`].**
- X² = I, so X∂X = −∂X X. The SLD is therefore exactly L = p·∂X, and QFI_ij = p²·Σ_P ∂_i c_P ∂_j c_P for all p (X = Σ c_P P).
- QFI additivity plus Braunstein–Caves then give the single-parameter result: the best single-copy measurement (the SLD eigenbasis) achieves the QFI. No collective (quantum-memory) measurement on any number of copies can beat it per copy. **Memory gain = 1 exactly** [THEORETICAL, standard].
- Holevo incompatibility D_ij = (p³/d)·Im tr(X ∂_iX ∂_jX) **= 0 identically**. The secular dipolar H commutes with the global flip Π_k X_k, which maps X → −X and ∂X → −∂X [DERIVED; measured R ≤ 1e-14]. So the Holevo bound equals the SLD bound, and the collective gain for k parameters is at most C_single/C_SLD ≤ k.
- Bell sampling on two copies, per pair, has FI ≈ p⁴·4Σ c_P² ∂c_P² (leading order; exact values computed at p = 1 and 0.1). Per copy this is at most 2p²·max c_P² times the QFI. **Memory protocols built on tr(Pρ)² pay p² on high-temperature quantum data.** The time-reversed echo measures the same quadratic functional with a signal linear in p [DERIVED].

**Results.** Per copy and per structural parameter, relative to the QFI (the optimum of both single-copy and memory measurements). Full data: `summary.json`.

| Protocol | t ≥ 10 µs: median (range) | t ≥ 80 µs: median (range) |
|---|---|---|
| Optimal collective / quantum memory, one parameter | **1 (theorem)** | **1** |
| Two-copy Bell sampling (memory), p = 1, exact | 0.0026 (1e-5 – 0.31) | 4e-4 (1e-5 – 0.032) |
| Two-copy Bell sampling, thermal p = 4.8e-5 | ≤ 0.135·p² ≤ 3e-10 | smaller |
| Random local Pauli shadows (measure-first), p = 1, exact | 0.025 (0.001–0.22) | 0.0056 (0.001–0.084) |
| Site-resolved magnetisation ⟨Z_k⟩ (conventional transfer readout) | 0.0058 (1e-4 – 0.27) | 0.0042 (1e-4 – 0.18) |
| Single-copy echo at t with best butterfly (2 queries), vs QFI at 2t | 0.019 (1e-4 – 0.41) | 0.021 (2e-4 – 0.18) |
| Bell / local shadows at p = 1 | 0.10 (0.005–1.41) | 0.078 (0.005–0.39) |

- **Where the information lives.** The mean Pauli weight of the structural information rises from ≈ 2 at 5 µs to 6.7 at t ≥ 80 µs (8.0 at N = 12, 160 µs). At t ≥ 80 µs, 89% of the information (median) sits in strings of weight ≥ 5. Measure-first local protocols lose a factor of about 3^w there. **Single-copy coherent processing recovers the loss fully; memory is not needed.**
- **N-trend, N = 10 → 12 at 160 µs (two probes).**
  - Local-shadow capture: 0.0050 → 0.0024 (p19) and 0.0089 → 0.0037 (p245).
  - Bell capture: 4.2e-4 → 2.9e-4 and 7.6e-4 → 1.3e-4.
  - Memory falls further behind the single-copy optimum as N grows [MEASURED at two sizes; the trend beyond N = 12 is INFERENCE].
- **Crossover polarisations (leading order).**
  - Bell = local shadows needs p* ≥ 0.95 (median 3.3, i.e. never).
  - Bell = random global Clifford needs p* ≥ 0.057.
  - Memory therefore beats only deliberately crippled single-copy protocols, and only at hyperpolarisation.
- **Multi-parameter estimation.**
  - The allocation-optimised split-SLD single-copy protocol comes within **2.9–5.1×** of the SLD/Holevo bound for k = 4, and **4.8–9.5×** for k = 9.
  - The true memory gain is therefore between 1/(1+R) = 1 and 2.9–9.5, i.e. ≤ k.
  - Polynomial, never exponential. The bound is loose: a better single-copy POVM may exist.
- **Copies needed for σ_θ = 0.1 Å, one parameter.**
  - Single-copy optimum at thermal p: 8×10⁸ – 1.2×10¹⁴ (median 1.9×10¹¹). One mg of ubiquitin holds 7.0×10¹⁶ molecules, so **copies are not the scarce resource in ensemble NMR**.
  - Bell sampling at thermal p: 2×10²⁰ – 8×10²⁵, which exceeds a 1 mg sample by 3×10³ – 10⁹×.
  - At p = 1: 2 – 3×10⁵ (single copy) vs 10³ – 9×10⁷ (Bell).

## 3. Why the structural task cannot be in an exponential memory class [DERIVED + LITERATURE]

1. **The target is a k-parameter smooth family.** k ≈ 3N_atoms. Local (asymptotic) estimation obeys:
   - memory gain = 1 per parameter;
   - memory gain ≤ k jointly, because splitting copies among k SLD measurements loses at most k, and Holevo ≤ SLD here (D = 0).

   The proven exponential separations need an exponentially large, black-box property family or a non-parametric global property: all 4ⁿ Paulis, all Pauli-channel eigenvalues, purity, symmetry class.
2. **A white-box forward model collapses the family.** It tells the single-copy learner which observable (the SLD) to measure. The price is computing the SLD, a 2^{N_σ}-dimensional classical simulation. That is the forward-model bottleneck of K-105, not a sample-complexity bottleneck, and quantum memory does not address it.
3. **High-temperature penalty.** Memory protocols read quadratic functionals such as tr(Pρ)². Their signal is O(p²), against O(p) for single-copy and time-reversal protocols. At NMR polarisation p ≈ 3×10⁻⁵ – 10⁻⁴, the thermal values in `physics.json`, that is a 10⁸–10⁹ deficit per copy.
4. **Commuting structural couplings.** The structural information in weak couplings (heteronuclear, J/RDC, spin labels) and in sensor–bath coupling is secular (ZZ / Z-field), i.e. commuting. Commuting families are jointly measurable in one product basis, so there is no memory separation. Only the homonuclear flip-flop network is non-commuting, and that network is the K-104/K-105 regime.

## 4. The only coherent-quantum-data residual: IQHL-style coherent single-copy processing

**The idea.**
- Interactive quantum Hamiltonian learning (IQHL): Wiebe–Granade–Ferrie–Cory PRL 112, 190501 (arXiv:1309.0876); demonstrated on an NV electron spin by Wang et al. Nat Phys 13, 551 (arXiv:1703.05402).
- SWAP the protein spin state into a trusted quantum simulator, which applies a model-based reversal or the SLD measurement.
- This is coherent **single-copy** processing, not memory.

**Size of the gain [MEASURED, isolated-cluster ideal model, same caveats as R1].**
- QFI(2t) over the NMR echo(t): median ≈ 50×.
- QFI over conventional magnetisation readout: ≈ 240× at t ≥ 80 µs.

**Realism: fails by orders of magnitude.**
- Transduction noise λ per spin (depolarising) keeps only part of the late-window QFI:

  | λ | QFI retained (t ≥ 80 µs, median) |
  |---|---|
  | 0.95 | 51% |
  | 0.9 | 26% |
  | 0.8 | 7% |
  | 0.5 | 0.25% |

  [MEASURED from the weight distribution.]
- A useful interface therefore needs λ ≥ 0.95 on every spin of the σ-cone: 16–20 spins at 40 µs [R1 MEASURED], ≥ 57 at 80 µs [INFERENCE].
- The NV–¹H coupling is 2.9 kHz at 3 nm and 0.63 kHz at 5 nm, so a transfer takes 0.17–0.79 ms. The protonated-protein ¹H network T2 is 8–11 µs [R1 physics lens, MEASURED].
- Per-spin transfer fidelity is then ≤ 1.4×10⁻⁷ (exponential law) at 3 nm for a protonated protein. In the amide-only case it is ≤ 9×10⁻³ [DERIVED from constants, `physics.json`].
- There is no known way to address individual protein protons. The best nuclear-cluster imaging is 27 ¹³C spins inside diamond (Abobeih et al. Nature 576, 411; arXiv:1905.02095, verified). Single-protein NV detection (Lovchinsky et al. Science 351, 836, doi:10.1126/science.aad8022; repo bibliography, **not re-verified here**) detects signal only; it does not transfer states.
- Even with a perfect interface, the simulator must implement U(θ₀)† or the SLD on N_σ spins. That is exactly K-105's forward-model cost (4–6 h per evaluation fault-tolerant; exact classical reach up to N_eff ≈ 30–47).

**Status.** Practical L0; theoretical L0 as an advantage.

## 5. Claim levels

- **Theoretical.**
  - Single-parameter memory gain = 1: a theorem, L6-negative.
  - Multi-parameter gain ≤ k: DERIVED; measured ≤ 9.5 for k ≤ 9.
  - Any exponential separation on a protein-structure task: L0.
  - The formally in-class OTOC task is a time-reversal separation, realised natively by NMR; see K-105.
- **Practical: L0.**
  - No transduction path for protein ¹H states.
  - Copies are abundant in ensembles, and ensemble readout is expectation-value (collective) access.
  - Single-molecule experiments are sensor-channel learning, which is commuting.

## 6. What would reopen it (all needed)

1. A structure-relevant property family that is exponentially large and not reducible to k geometric parameters. An example might be an ensemble-heterogeneity question whose answer lives in exponentially many non-commuting observables. It must remain informative after profiling.
2. A per-spin coherent interface to a protein ¹H/¹³C/¹⁵N cluster with λ ≥ 0.95 on the full σ-cone, faster than the network T2.
3. Polarisation p ≳ 0.3 on the transferred spins. Otherwise the p² penalty dominates.
4. A single-molecule setting where copies really are scarce. In ensembles they are not.

## 7. Next tests (cheap)

- Tighten the multi-parameter window [1, split/SLD] with an SDP or Nagaoka-type optimal single-copy bound at N = 8–10, k = 4–9, to see whether the true memory gain is ≈ 1 or ≈ k.
- Recompute §2 on the embedded, dephased model (γ = 1000–5000 s⁻¹) and at the converged N from the R1-SIM cone runs. Check whether QFI(2t)/echo(t) and QFI/magnetisation keep growing with N. That growth is the size of the coherent-processing (not memory) gain.
- The decisive experiment for the time-reversal route is unchanged (K-105): a measured protein T3/T2.

## Files

- `qd_fisher.py`: exact sector dynamics, Pauli transform, and all per-copy FI protocols. Single-threaded and checkpointed per time point.
- `validate.py` → `validate.json`: brute-force checks at N = 4, all errors ≤ 1.7e-15.
- `analyze.py` → `summary.json`: ratios, crossovers, multi-parameter split, transduction, N-trend, and the HKP task table.
- `physics.py` → `physics.json`: polarisations, NV–¹H couplings, transfer fidelities, non-secular ratios, molecules per mg.
- `out/*.json`: raw per-instance results, 6 jobs. `*.partial.done.json` are the preserved checkpoints.

**Compute.** About 23 CPU-min in total, single-threaded, peak below 1.5 GB. The N = 12 runs took about 10 and 8 CPU-min.
