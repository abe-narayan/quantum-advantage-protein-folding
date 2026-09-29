# Discovery lens: complexity and dequantization (2026-09-28)

Status: IN PROGRESS. WebSearch budget exhausted this session (200/200); searches via arXiv export API, arXiv abs pages, OpenAlex, Crossref.

Overlap note: discovery_algorithms.md already lists neutrino-nucleus response, XRTS of WDM, frustrated-magnet thermodynamics. This lens tries to (a) ground each in a hardness/dequantization map and (b) sharpen to a materially distinct subsection, plus add candidates not listed there (0vbb NME, ADR refrigerant entropy).

## Plan
1. Complexity map: hard regimes vs dequantized regimes, with citations.
2. Candidates living in (hard) AND (practical) AND (not dequantized).
3. Kill list from dequantization results.

## Query log
(filled below)

## 1. Complexity / dequantization map (all verified on arXiv abs pages 2026-09-28)

| Task class | Status | Evidence |
|---|---|---|
| Ground-state energy of chemical/nuclear Hamiltonians | No evidence of generic exponential advantage (good trial states + classical heuristics usually suffice where ground states are "easy" for QPE state prep) | Lee et al. arXiv:2208.02199 [VERIFIED] |
| Quadratic (Grover/QAE/walk) speedups | Do not survive early FT overheads | Babbush et al. arXiv:2011.04149 [VERIFIED] |
| Gibbs states above constant temperature | Separable, efficiently classically samplable (dequantized) | Bakshi-Liu-Moitra-Tang arXiv:2403.16850 [VERIFIED]; Rouze-Franca-Alhambra arXiv:2403.12691 (high-T fast mixing) [VERIFIED] |
| Gibbs sampling at low T (beta ~ poly(n)) | BQP-complete (quantum Gibbs samplers universal) | Rouze-Franca-Alhambra arXiv:2403.12691 [VERIFIED] |
| Gibbs sampling at constant T, O(1)-local 3D | Classically hard to sample, quantum efficient (contrived Hamiltonians) | Rajakumar-Watson arXiv:2408.01516 [VERIFIED] |
| Noisy circuits (constant noise) observables | Poly-time classical (Pauli propagation w/ damping) | Schuster-Yin-Gao-Yao arXiv:2407.12768 [VERIFIED] |
| Noiseless random/locally scrambling circuits, observables | Classically tractable on average (Pauli propagation) | Angrisani et al. arXiv:2409.01706 [VERIFIED] |
| Short-time local-Hamiltonian dynamics | Poly-time via cluster expansion | Wild-Alhambra arXiv:2210.11490 [VERIFIED] |
| 127q kicked Ising "utility" | Dequantized (BP tensor networks) | Tindall et al. arXiv:2306.14887 [VERIFIED] |
| D-Wave spin-glass quench "beyond classical" | Claimed (King et al. arXiv:2403.00910) then challenged (Tindall et al. arXiv:2503.05693; Mauron-Carleo arXiv:2503.08247) = category E | [VERIFIED all three] |
| GBS vibronic spectra | Dequantized (quantum-inspired classical) | Oh et al. arXiv:2202.01861 [VERIFIED] |
| OTOC(2) at edge of ergodicity (Google 103q) | Claimed beyond-classical; our own protein-NMR lesson: informative regime classically computable | Abanin et al. arXiv:2506.10191 [VERIFIED] |

Surviving hard regimes (not dequantized) that map to physics:
H1. Long-time, low-to-intermediate-temperature real-time correlation functions (spectral functions) of fermionic systems with sign problem, beyond short-time cluster expansion and beyond Pauli-propagation damping (i.e. coherent, noiseless physical dynamics with conserved quantities).
H2. Real-frequency response where classical has only sign-free *Euclidean* (imaginary-time) data: inversion (analytic continuation / Laplace inversion) is exponentially ill-conditioned; a quantum computer measures real-time correlators directly. The quantum advantage is resolution at fixed cost, not an energy.
H3. Low-temperature Gibbs states with sign problem (below the BLMT/high-T threshold), but only where solver error dominates Hamiltonian error.
H4. Off-diagonal/transition quantities between two correlated eigenstates in exponentially large, non-geometric (no area law) configuration spaces (nuclear shell model), where classical Lanczos is exact but bounded by dimension ~1e10-1e11.
Killed regimes: anything readable as argmin of a classical energy (lesson 3), infinite-T spin dynamics (Pauli propagation / spinDMFT), noisy-hardware expectation values, high-T thermodynamics, GBS-type sampling applications.

## Query log (sources: arXiv export API via local urllib, arXiv abs pages, OpenAlex, Crossref; WebSearch exhausted; WebFetch to arXiv/OpenAlex/S2 returned 429/503 so local HTTP used)
- Crossref: "neutrinoless double beta decay quantum computing nuclear matrix element" (2020+) -> only classical NME/lattice QCD works
- OpenAlex: "quantum computing neutrinoless double beta decay nuclear matrix element"; "quantum computer nuclear shell model double beta decay"; "quantum algorithm nuclear shell model simulation qubits"
- OpenAlex cited-by W4385380575 (Perez-Obiol 2023, nuclear shell model on digital QC): 54 citing works, all ground-state/spectra/VQE/annealing of light or sd/pf-shell nuclei; none computes a 0vbb NME
- arXiv API: abs:"double beta" AND (abs:"quantum computer" OR "quantum computing" OR "quantum simulation" OR qubits) -> only 2506.05757 (Chernyshev et al., 1+1D QCD toy on IonQ), 2502.02502, 2312.00780 (lattice gauge theory)
- arXiv API: abs:"neutrinoless double-beta" AND abs:"matrix element" AND (ab initio | shell model | uncertainty) -> classical SOTA list
- arXiv API: neutrino AND nucleus AND quantum AND (computer|computing|qubit) -> Roggero et al. 1911.06368, 1804.01505 only (quantum)
- arXiv API: "supernova neutrino" AND argon AND "cross section"; (40Ar|argon) AND (Gamow-Teller|MARLEY|forbidden) AND neutrino; au:Sobczyk AND (neutrino|response); coupled-cluster AND LIT/response AND 40Ca/40Ar
- arXiv abs pages verified: see citations per candidate

## 2. Candidate notes (in progress)

### C-a: 0vbb nuclear matrix elements (76Ge, 136Xe) in large multi-shell valence spaces
- Quantum literature (scoped): only Chernyshev et al. arXiv:2506.05757 [VERIFIED] (real-time 0vbb of a toy nucleus in 1+1D QCD, 32 qubits IonQ). Nuclear-shell-model QC literature (Perez-Obiol 2023 doi:10.1038/s41598-023-39263-7 [VERIFIED OpenAlex] and 54 citing works) targets energies/spectra, not 0vbb NMEs. => Category B.
- Classical SOTA: VS-IMSRG + valence-space diagonalization with 34 chiral interactions (Belley et al. arXiv:2210.05809 [VERIFIED]); NME controlled mainly by the C_1S0 LEC (Belley et al. arXiv:2408.02169 [VERIFIED]); converged ab initio short-range NMEs for 76Ge/82Se/130Te/136Xe (Todd et al. arXiv:2604.22727 [VERIFIED]); CC for 48Ca (Novario et al. arXiv:2008.09696, title verified via arXiv listing); IM-GCM (Yao et al. arXiv:1908.05424, listing).
- RED FLAG (lesson 6, model floor): Belley 2024 shows the NME variance is dominated by the interaction (C_1S0) not the many-body solver. An exact quantum valence-space solution removes only solver error. Verdict: weak unless restricted to the sub-question "IMSRG(2) truncation error vs exact in extended (cross-shell) valence space for 136Xe/130Te", where solver error is the open variable.

### C-b: Low-energy (5-60 MeV) charged-current nu_e + 40Ar -> e- + 40K* response for DUNE supernova/solar neutrinos
- Practical need (verified): DUNE collaboration arXiv:2303.17007 [VERIFIED]: integrated SN luminosity with <10% bias requires sigma(E_nu) known to ~5%; current theory uncertainty large.
- Classical SOTA (verified): MARLEY refinement with HF-continuum RPA incl. forbidden transitions + indirect measurements for allowed strength (Gardiner et al. arXiv:2604.26801 [VERIFIED], 2026-04); earlier MARLEY (Gardiner arXiv:2010.02393). Ab initio CC-LIT exists for 40Ca longitudinal/transverse responses in the quasielastic (GeV-beam) regime (Sobczyk et al. arXiv:2103.06786 [VERIFIED]; 2310.03109 title via listing) but, in arXiv abstract searches through 2026-09-28, no ab initio low-energy CC nu_e-40Ar cross section found.
- Quantum literature: Roggero-Carlson linear response arXiv:1804.01505 [VERIFIED]; Roggero et al. arXiv:1911.06368 [VERIFIED] (resource analysis for accelerator-energy neutrino-nucleus response, triton demo). No quantum study of the 40Ar low-energy CC (GT + first-forbidden) strength. => Category B (subsection distinct from accelerator-energy quasielastic, which is Category C).

### C-c: XRTS dynamic structure factor / ITCF of strongly degenerate compressed ablators (Be, C, CH) at theta=T/T_F < ~0.5
- Queries: arXiv (WDM|dense plasma|ICF) AND (quantum computer|computing|algorithm|fault-tolerant); au:Dornheim AND (ITCF|sign problem) AND XRTS; au:Dornheim AND (beryllium|NIF|sign problem) AND PIMC; full-text grep of arXiv:2605.07722 HTML.
- Quantum literature: Rubin et al. arXiv:2308.12352 [VERIFIED] (stopping power, first-quantized, ~1e3 logical qubits, 1e15-1e17 Toffoli per roadmap summary); Pennati et al. community roadmap arXiv:2605.07722 [VERIFIED] names "finite-temperature response" of WDM as a QC target but gives no algorithm/resource estimate for XRTS S_ee(q,w). No dedicated quantum XRTS paper found. => Category B (C if one counts the roadmap's generic mention).
- Classical SOTA [VERIFIED]: fermionic PIMC without nodal restriction via fictitious-identical-particle xi-extrapolation, NIF Be XRTS matched without empirical input (Dornheim et al. arXiv:2402.19113, Nat Commun 16, 5103 (2025)); xi-extrapolation breaks down at moderate-to-high degeneracy (arXiv:2308.06071); Taylor-series generalization (arXiv:2509.11317); model-free ITCF analysis of XRTS (review Gawne et al. arXiv:2604.25735; Dornheim et al. arXiv:2211.00579, 2305.15305 listing).
- Complexity reading: The imaginary-time (tau-domain) comparison of PIMC with Laplace-transformed data DEQUANTIZES the analytic-continuation route (H2) for XRTS: one never needs real-frequency spectra. Residual hardness = the fermion sign problem itself (H3) at low theta and higher Z. Scaling variable: theta (degeneracy) and Z/number of bound electrons at fixed N ~ 30-100 electrons.
- Main risk: information (lesson 5): XRTS source/instrument function (eV-scale) limits what S(q,w) detail is measurable; tau-domain analysis already extracts T, normalization, Rayleigh weight model-free.

### C-d: Solar-interior iron (and Cr/Ni) L-shell opacity from a first-principles electron+ion+photon Hamiltonian
- Queries: arXiv iron AND opacity AND (Z facility|Z-pinch|Sandia|solar interior|discrepancy); opacity AND (quantum computer|computing|algorithm).
- Quantum literature [VERIFIED]: Pathak, Kononov, Baczewski arXiv:2607.02811 (2026-07): first/second-quantized electron+photon registers, interaction-picture simulation, logical resource estimates for solar iron opacity "comparable to" Rubin et al. stopping power. No head-to-head vs strongest classical models. => Category C.
- Classical SOTA [VERIFIED]: Zhou et al. arXiv:2607.21238 (2026-07) claim plasma-screening + CI enhancements give 25-30% higher Fe L-shell opacity, explaining the Bailey et al. Nature 517, 56 (2015) discrepancy; ML opacity surrogate Benredjem et al. arXiv:2609.13252 (listing); Pain et al. arXiv:2509.00207 (listing); TDDFT average-atom opacity Gill et al. arXiv:2104.00551 (listing title). Classical DCA/CI codes (OP, OPAS, SCO-RCG, ATOMIC) [UNVERIFIED names].
- Complexity reading: real-frequency absorption of an open-L-shell ion embedded in a degenerate, strongly coupled plasma = finite-T real-time response of a Coulomb many-body system (H1+H3); PIMC cannot give real-frequency lines (H2, and unlike XRTS, opacity spectra are measured at high resolution so the information is present). Model floor is small (Coulomb Hamiltonian; main omission relativistic/Breit terms in nonrelativistic first quantization).
- Scaling variable: number of bound electrons in open L-shell (Fe XVII-XX: 8-11) x plasma electrons in the simulation cell at n_e ~ 1e23 cm^-3; spectral resolution (photon register size).
- Main risk: Zhou et al. 2026 classical model already closes the discrepancy (decision flipped classically); FT cost ~Rubin-class (roadmap arXiv:2605.07722 quotes 1e3 logical qubits and 1e15-1e17 Toffoli for converged stopping-power cases).

### C-e: Sub-kelvin ADR refrigerant entropy S(T,B) of frustrated Yb-based magnets at T << J
- Queries: arXiv (adiabatic demagnetization|magnetocaloric) AND (frustrated|quantum spin) AND (millikelvin|sub-Kelvin|refrigerant|refrigeration); (magnetocaloric|ADR|specific heat|entropy) AND frustrated AND (quantum computer|quantum algorithm|Gibbs sampler|quantum Gibbs).
- Practical need [VERIFIED]: KBaYb(BO3)2 reaches 22 mK, cooling "several times lower than the energy scale of interactions" (Tokiwa et al. arXiv:2103.00765); review of Gd/Yb oxides for 0.02-2 K ADR (Treu et al. arXiv:2405.15697); Ba3XB9O18 borates (Klinger et al. arXiv:2512.05550, listing). He-3-free sub-K cooling for cryostats (including quantum hardware) and space.
- Quantum literature: none found on ADR/magnetocaloric thermodynamics via quantum algorithms => Category A (scoped).
- Classical: XTRG thermal tensor networks (Chen et al. arXiv:1801.00142 [VERIFIED]); HTSE, TPQ/ED, QMC where sign-free; classical MC for Gd3+ (S=7/2, near-classical). Quantum: exact detailed-balance Lindbladian Gibbs sampler (Chen-Kastoryano-Gilyen arXiv:2311.09207 [VERIFIED]) + thermodynamic integration for S(T,B).
- Complexity reading: T << J is below the BLMT separable regime (arXiv:2403.16850), so not dequantized by that result; but frustration + "structural randomness" invoked by the materials means glassy slow mixing that hurts quantum Gibbs samplers equally. Model floor: fitted exchange, site disorder, hyperfine entropy of 171/173Yb. Verdict weak.

### C-f: Beyond-mean-field fission fragment fluctuations (mass/charge width, fragment entanglement) for 240Pu
- Quantum literature [VERIFIED]: Kadam, Bjelcic, Schunck, Wendt arXiv:2609.03240 (2026-09-03): entanglement and non-local magic along TDHFB 240Pu fission; argue QC advantage; no algorithm/resource/advantage study => Category C (complexity indicator only).
- Classical: TDHFB/TDSLDA, TDGCM+GOA, stochastic mean field, Langevin [UNVERIFIED specific refs].
- Main risk: nuclear EDFs are density-dependent functionals, not Hamiltonians; an "exact" many-body evolution of an EDF is ill-defined (model floor). Magic/entanglement are necessary, not sufficient, for hardness (BP/TN results in the map). Verdict weak.

### Sharpening of C-b (from notes): classical ab initio route not yet taken but available
- CC for 40Ar ground state/weak form factor exists (Payne et al. arXiv:1908.09739 [VERIFIED]); gA quenching resolved ab initio (Gysbers et al. arXiv:1903.00047, listing title). Chebyshev/GIT spectral reconstruction (Sobczyk-Roggero arXiv:2110.02108 [VERIFIED]). So the classical wall for the INCLUSIVE low-energy CC cross section is not established: CC-LIT or VS-IMSRG + shell-model Lanczos strength likely feasible. The more defensible quantum subsection is EXCLUSIVE final-state branching (gamma vs n vs p emission after 40Ar(nu_e,e-)40K*), today handled by Hauser-Feshbach statistics (Gardiner arXiv:2010.02393 [VERIFIED]); Roggero-Carlson algorithm gives final-state projection.

## 3. Killed ideas (this lens)
- Infinite/high-T spin dynamics (NMR lineshapes, spin diffusion, high-T ADR paramagnetic salts): BLMT arXiv:2403.16850, Pauli propagation arXiv:2409.01706, our own protein-NMR kill.
- Noisy-hardware "utility" expectation values as an application: Schuster et al. arXiv:2407.12768; Tindall et al. arXiv:2306.14887.
- Spin-glass annealing quench dynamics as the target: category E (King arXiv:2403.00910 vs Tindall arXiv:2503.05693, Mauron-Carleo arXiv:2503.08247); no practical output.
- GBS for vibronic spectra: dequantized, Oh et al. arXiv:2202.01861.
- Analytic-continuation advantage for XRTS: side-stepped classically by tau-domain ITCF analysis (arXiv:2604.25735, 2211.00579).
- Short-time dynamics targets (e.g. few-fs attosecond charge migration before nuclear-motion decoherence): cluster-expansion classical algorithm arXiv:2210.11490.
- Constant-temperature Gibbs sampling hardness (arXiv:2408.01516): proven only for contrived 5-local 3D Hamiltonians; no practical instance mapped.
- Nuclear shell-model ground-state energies of light/sd/pf nuclei: crowded (54 works citing Perez-Obiol 2023) and KSHELL-exact; Lee et al. arXiv:2208.02199.
- QLSA/Carleman for plasma Vlasov/PDE kinetics: readout + nonlinearity; roadmap arXiv:2605.07722 ranks QC least mature for kinetic workloads.

## 4. Ranking and bottom line (this lens, 2026-09-28)
1. C-d solar Fe L-shell opacity (Category C; plausible): exact Coulomb Hamiltonian (small model floor), real-frequency high-resolution observable (information present), PIMC cannot give it; a quantum protocol exists (arXiv:2607.02811) but no quantum-vs-strong-classical study; live classical counter-claim (arXiv:2607.21238) makes the head-to-head publishable either way.
2. C-c XRTS/ITCF of strongly degenerate ablators (Category B; plausible-weak): only the sign-problem regime (theta < ~0.5, Z >= 4 with bound electrons) survives; tau-domain analysis dequantizes the continuation route.
3. C-b nu_e-40Ar low-energy CC, exclusive branching subsection (Category B; plausible-weak): DUNE needs ~5% sigma(E_nu); classical ab initio (CC-LIT, VS-IMSRG) has not been tried, so the classical wall is unestablished.
4. C-a 0vbb NMEs (Category B; weak): model floor (C_1S0 LEC dominates spread).
5. C-e ADR entropy (Category A; weak): glassy mixing and fitted-Hamiltonian floor.
6. C-f fission fluctuations (Category C; weak): EDF is not a Hamiltonian.
General lesson from this lens: the not-dequantized regimes (H1-H4) that also carry practical decisions cluster in high-energy-density physics with first-principles Coulomb Hamiltonians (opacity, XRTS, stopping), because there the Hamiltonian is exact (model floor ~0) and PIMC's sign problem plus its Euclidean-only access are the classical bottlenecks. Nuclear targets inherit an interaction (LEC) floor.

Status: COMPLETE (2026-09-28).
