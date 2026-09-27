# R1 completeness critique

## Verdict

The practical KILL of R1 stands. The synthesis, though, leans on several reasons that are either conditional or overstated, and a few load-bearing pieces are missing.

- **What survives this review [DERIVED/INFERENCE]:** at every cone size exact classical simulation can reach (N_eff ≲ 30–47), the quantum forward model adds nothing that exact simulation cannot supply. Its extra information is small even in the ideal model, and much smaller once reversal attenuation is applied. The fault-tolerant cost per evaluation is hours.
- **What does not survive as written:**
  - the "CRB below systematic floors" argument;
  - "gain ≤ 3";
  - "amide branch classically exact-simulable";
  - "ε=3e-5 closes the window" stated without its criterion;
  - "Mi et al.: OTOC(1) spreading is classical" used as evidence against OTOC(1) hardness;
  - "killed in any of categories 1–6".

## 0. New measurements from this critic

About 13 CPU-min, single-threaded. Files are in `C:\Users\abena\quantum-advantage-protein-folding\research\experiments\ADVERSARIAL\R1_completeness\`. I wrote scripts and JSON only; the harness forbids report `.md` files, so there is no README.

| Test | Result | Tag |
|---|---|---|
| **Classical-spin / DTWA echo adversary** (`cspin_echo.py`, `out/cspin_echo_*.json`, `out/cspin_echo_summary.json`). The C1 `cspin` adversary only ever computed transfer S. No lens had run classical spins on the echo F, although CURRENT_STATE lists classical spins among the adversaries that fail. | Setup: Weyl/TWA echo F_cl = ⟨A(Φ_t x) A(Φ_t R_b x)⟩, M=4000, SE ≤ 0.017, against sector-exact F at N = 10/12/14 (C2 RAW). It fails at 40–80 µs everywhere. Max error in [80, 320] µs: p19 0.24 / 0.37 / 0.36; p245 0.57 / 0.60 / 0.19; DTWA p19 N10 0.23, p245 N14 0.20. The error does not fall consistently with N. The classical echo relaxes to a nearly site-independent ≈ 0.14–0.30, while the exact plateaus are site-specific (0.22–0.86). | MEASURED |
| **Lost-norm (δ) Richardson extrapolation** using two cheap ε rungs, rebuilt from the `kept_norm2` already stored in the C2 RAW (`delta_extrap.py`, `out/delta_extrap.json`). R1_amplify's bias ∝ δ law predicted this could work. | The best cheap pair, (3e-4, 1e-4), cuts window error 2–3× (p19 N10 0.068→0.036; p245 N12 0.219→0.069) and moves failure 60–80 → 80–100 µs. It never closes the window, at N = 12–14 it is sometimes worse than plain, and it hurts at p245 N10 (the extrapolation fails at 300 µs where ε=3e-5 alone passes). | MEASURED |
| **Side result from the same data** | At N=12, ε=1e-4 held 3.3e5 (p19) / 3.2e5 (p245) strings, about 7.5–8% of 4^12/4, which is more strings than the 2.57e5 that reproduced the whole N=10 window. It still fails at 60–80 µs with window error 0.14–0.22. The "saturated metric" critique therefore applies only at N ≤ 10. At N=12 the ε=3e-5 rung is informative whichever way it ends. | MEASURED |
| **Prior-regularised structural information** (`prior_info.py`, `out/prior_info.json`; fi_method Jacobians, 1UBQ p19 N10, all 27 coordinates unknown, Gaussian prior σ_p on every coordinate). This reconciles the value lens (CRB 0.014 Å with the other coordinates known) and fi_method (1.2–1.5 Å with a flat prior). | Posterior radial sd, all data, ideal reversal: 0.10 / 0.16 / 0.22 Å for σ_p = 0.2 / 0.5 / 1.0 Å. That is not 0.014 Å. The hard window's per-proton variance gain has a median of 1.5 / 2.1 / 3.0 (max 2.2 / 2.8 / 3.8), worth +17 to +27 bits. With A(t) = exp(−t/130 µs) the median is 1.11–1.52 (max ≤ 2.25); with 85 µs it is 1.07–1.32 (max ≤ 1.75). This is one job, linearised, using the gate's 80 µs partition, which is itself generous. | MEASURED (on stored Jacobians) |

Literature I verified this session through arXiv/Crossref:
- Starkov & Fine, PRB 98, 214421 (2018), arXiv:1806.09355, the hybrid quantum-classical method.
- Starkov & Fine, PRB 101, 024428 (2020), arXiv:1911.00990, coupled quantum clusters.
- Fine, Elsayed, Kropf & de Wijn, PRE 89, 012923 (2014), arXiv:1305.2817. It finds that spin-1/2 Loschmidt echoes are only *power-law* sensitive to small perturbations, while classical spins are exponentially sensitive.
- Krojanski & Suter, PRL 93, 090501 (2004); PRA 74, 062319 (2006); PRL 97, 150503 (2006). Only the bibliographic record is verified; I did not read the contents.

## 1. Over-claims and inconsistencies in the synthesis

1. **"CRB 0.014–0.03 Å vs model-bias floor 0.06–0.6 Å"** is conditional on every other coordinate being known.
   - With realistic priors, the achievable sd is 0.1–0.4 Å [MEASURED, §0], the same order as the floors. The argument therefore does not bite.
   - The truncation part of the floor (0.22–0.6 Å) comes from an unconverged cluster model. A converged quantum forward model would remove exactly that part, so it cannot count against the quantum route.
   - The kill should rest instead on identifiability (small gain under priors) and cost.
2. **"Gain over classically usable data ≤ 3"** is a median, not a bound.
   - The value lens's own maximum is 10.4, and its fast calibration gives g = 13. Both meet the revival template's g ≥ 10.
   - Under generous accounting, the physics lens has 2 of 11 jobs at gain ≥ 2 (max 3.39). fi_method's maxima are 2.66–3.94.
   - An existence claim needs only one regime, so the kill should be stated on the upper tail (see §4).
3. **"ε=3e-5 closes the N=10 window"** holds only under the per-point |bias| > σ rule.
   - Under fi_method's estimator-level criterion, D = 1.17–1.41 at ε=3e-5, which exceeds 0.5. The window is not closed, and M*_F is censored above 2.57e5.
   - The conclusion survives only because exact simulation takes seconds, and that is how it should be worded.
4. **"Amide-only branch classically exact-simulable up to 350 µs"** does not cover the amide windows.
   - The best-adversary echo t_c for the 7 HN jobs is 200 / 500 / 400 / **650** / 300 / 500 / 250 µs [MEASURED, RAW nmr_gate_hn].
   - The σ-cone was measured only for 1UBQHN p19, whose own t_c is 650 µs, beyond the measured 350 µs.
   - The amide kill beyond 350 µs therefore rests on value-lens light-cone INFERENCE, which should be stated.
5. **Mi et al. 2021 is quoted by half.** The synthesis cites "operator spreading is captured by an efficient classical model", but the same abstract says "operator entanglement requires exponentially scaled computational resources" (theory lens L12).
   - The measured failures of the incoherent Markov model (errors 0.3–0.9), the MPO with χ ≤ 64, and classical spins (§0) all point to an interference-dominated echo at N ≤ 14.
   - The synthesis should say that the literature neither establishes nor refutes OTOC(1) hardness for this family.
6. **"Two independent kills."**
   - The value kill's floor leg is weakened by item 1. Its gain leg rests on the 6-point light-cone calibration (INFERENCE, bracket 7–589 spins).
   - What is truly independent of the Sánchez anchor is the cost leg (4–6 h per evaluation, and exact simulation wins below N_eff ≈ 30–47), plus the prior-regularised gain in §0.
   - fi_method's dephased-echo result (F5) is not independent evidence either. The R1-E γ proxy (√M₂,out = 2–14e4 s⁻¹) treats *reversible* coherent bath coupling as irreversible dephasing. Under global time reversal the bath is reversed too, so only the T3 part is irreversible.
7. **"Killed in any of claim categories 1–6"** overreaches. Only categories 1 and 3, plus a hardware noise threshold, were examined; categories 4 and 6 were not tested. It should read "no evidence for any category; 1 and 3 examined and negative at the practical level".
8. **"No compression found at any N."** This is correct, but §0 of the synthesis infers that the N=12 ε=3e-5 rung "cannot tell us anything". At N=12 the cap (4M strings) is about the full symmetric space (4.19M), so a capped run is itself a result: no compression at N=12.
9. **"Sánchez 2022 argue the ratio cannot be improved."** This is presented as settled, but Fine et al. 2014 (verified) and Domínguez 2021 / Krojanski–Suter 2006 "Reduced decoherence…" point the other way. The "intrinsic T3" is a hardware/sequence limit in current experiments, not an established fundamental law. The practical kill is a statement about present technology.
10. **The 9-family count and the wording "polynomial-cost".** Sparse Pauli at fixed ε, and CCE at order N−3, are not polynomial-cost. Also, classical spins had never been run on the echo until §0.

## 2. Classical adversaries not tried

These are ordered by relevance to R1-SIM, the only open question.

| Adversary | Why it matters | Concrete run | Expected effect |
|---|---|---|---|
| **Hybrid quantum core plus classical-spin bath** (Starkov–Fine; coupled quantum clusters). Named in the PREREG C2 survival path and in NM-1 as open; never run. | This is the only standard NMR method designed for the large-cone, embedded regime that R1-SIM asks about. Plain classical spins fail (§0) because the core is quantum, and the hybrid treats the core quantum-mechanically. | Exact core of N_c = 10–12 around the probe plus a classical bath of 20–60 spins, run through the echo protocol (kicked-trajectory TWA for the bath). Compare with the T-A typicality reference at N = 18–22 on p19/p245. KILL R1-SIM if the error stays < σ over 80–320 µs. | If it passes, R1-SIM dies at polynomial cost. If it fails, the hardness premise gets its first real support. |
| **Group-complete clusters** (whole methyl triplets and CH₂ pairs). | Nearest-N clusters cut methyls, leaving partners 1.8 Å away with ~20 kHz couplings (physics lens). Part of the N=10→12 non-convergence (up to 0.46) may be a construction artefact. | Rerun theory_hardness `exact_front.py` / T-A with group-complete orderings at N = 10–14. | Could shrink N_σ(t) and the light-cone estimates, which strengthens the practical kill. |
| **Hydrodynamic reduction** F̂_ab = 1 − 2q_b(1 − C(t)) (theory T-C). | §0 shows the classical-spin echo gets the site-independent part roughly but misses the site-specific q_b. That is exactly what T-C adds. | As in the theory lens, using the N=14 exact data already in the C2 `.partial` files. | A pass kills R1-SIM. |
| **spinDMFT / cluster-spinDMFT for the dense branch** (the theory lens recommended it for amide only). | It was designed for dense dipolar infinite-temperature dynamics. | Autocorrelation plus a kicked-echo extension; N/A if no OTOC extension exists (mark UNPROVEN). | Low prior. |
| **Sector-reduced, Krylov-typicality exact reach.** | This move sets the break-even N*; the value lens used a numpy constant. | RT-4 plus the U(1) sector reduction at N = 24–28. | Moves N* up by 2–5; strengthens the kill. |

## 3. Physical effects not modelled

- **Solvent and exchangeable protons.** Hydration water, labile OH/NH₃⁺, and amide back-exchange in H₂O for the "perdeuterated amide" network do not appear anywhere (grep: no hits). Intermolecular lattice protons appear only as INFERENCE (theory lens). Both enlarge N_eff and add spin-diffusion sinks. Test: add the crystal neighbours from the PDB symmetry, plus ordered waters, to the lightcone.py graph.
- **The MAS route was never considered.** The physics kill's site-resolution obstacle (one labelled sample per spin pair) assumes a static sample.
  - Fast MAS (≥ 100 kHz) with ¹H detection gives chemical-shift site resolution, and DQ recoupling is phase-reversible. This is the realistic R1-DQ experiment.
  - Test: rerun R1-DQ (synthesis test 4) using a recoupled, scaled DQ Hamiltonian, and anchor T3 from MAS spin-counting literature (UNVERIFIED which papers).
- **The reversal anchors are motion-averaged molecular solids.** Adamantane is plastic; cymantrene and ferrocene have rotating rings. The protein is a rigid, strongly heterogeneous network with geminal pairs and methyl rotors, so transferring T3/T2 could fail in either direction [INFERENCE].
  - Test: replace the single T3/T2 anchor with a K-dependent decoherence model, Γ(t) ∝ K(t)^α (Krojanski–Suter / Domínguez), using the measured operator size K(t) from `R1_theory_hardness/front/*.json`.
- **Consistent irreversibility model.** Choose a per-spin Markov γ so that the model's own Loschmidt echo gives T3 = 6.7 T2. Then rerun the FI split *and* the sparse-Pauli adversary at that γ, instead of multiplying the FI by an external A(t)². Noise makes Pauli propagation easy (theory L6), so both effects arrive together. Expected: a stronger kill from a single parameter.
- **DNP / cryogenic operation.** The SNR budget uses s1 = 0.1–3 per scan [INFERENCE]. DNP (ε = 10–100) would cut the quoted 32–1900 spectrometer-days by 10²–10⁴, but it adds electron–nuclear couplings and paramagnetic relaxation, which are not modelled.
- **The Trotter circuit is not the physical dynamics.**
  - The quantum forward model uses dt = 2 µs first-order Trotter. The physical sample evolves in continuous time forward, then under an engineered average Hamiltonian (with higher-order terms) backward.
  - The replicate lens found a Trotter–continuous difference of up to 0.013 (1.3σ).
  - Consequences: the FT T-count must include a Trotter-error budget below σ/3, and the backward leg must be modelled with its actual average Hamiltonian. Both raise the quantum cost.
- **Imperfect initial localisation of Z_a.** Cross-polarisation from a ¹³C/¹⁵N label spreads the polarisation over several protons, so the observable is not Z_a. This is not modelled; test with an initial operator Σ c_j Z_j taken from a short-contact CP simulation.

## 4. Statistics not checked

1. **Upper tail and composite penalties.** Every lens applies one penalty at a time and reports medians. No one has taken the *best* job of each lens and applied everything jointly: attenuation, realistic priors, exact reach, per-experiment n_b accounting, offsets and methyl motion. Doing so turns a median-based kill into a supremum-based kill. Expected: the max drops below 2 (it is 1.75 for p19 in §0 at T3 = 85 µs), but this is unverified for the value lens's g = 10.4 job.
2. **Prior-regularised gain on all 11 jobs.** `prior_info.py` covers p19 only. It needs 27-coordinate Jacobians per job, about 2×27 sector-exact N=10 runs (roughly 1–2 CPU-min per job), as a governed job.
3. **Uncertainty.** None of "0/11", "median 1.18" or "10/17 closed" carries a CI. The jobs are clustered (orientations and γ of the same probe; 2 proteins), so bootstrap over probes, not jobs.
4. **Consistent closure criterion.** State every "window closed" under both the per-point and the estimator-level (D ≤ 0.5) criterion.
5. **Pre-registered outcome table missing.** C3-kill-1 is indicated but not completed. C3-kill-2 (N=10 → 12, where the ε=1e-4 data now exist) and K-C1b have not been evaluated. The C3 survival clause already requires the feasibility audit ("time reversal … available; OTOC SNR not below σ"). The physics result can therefore be recorded as a **pre-registered survival condition that failed**, which is procedurally stronger than the post-hoc thresholds (T3/T2 ≥ 15, g ≥ 10, N_σ > 47) used in the synthesis. Those post-hoc thresholds must be labelled as such.

## 5. Literature not read, or not used

| Item | Status | Why it matters |
|---|---|---|
| Starkov & Fine PRB 98, 214421 (2018); PRB 101, 024428 (2020) | verified bibliographically, not read | The missing adversary (§2). |
| Fine, Elsayed, Kropf & de Wijn PRE 89, 012923 (2014) | verified (abstract) | Explains the classical-spin echo failure (§0). It is also counter-evidence to "intrinsic" T3, and must be reconciled with Sánchez 2022 before item 9 in §1 is stated as fact. |
| Krojanski & Suter PRL 93, 090501 (2004); PRA 74, 062319; PRL 97, 150503 (2006) | bibliographic only; the lenses said "not on arXiv" | Measured cluster size K(t) of hundreds to thousands of spins in dense ¹H solids, and scaling of the decoherence rate with K. This is a direct empirical anchor for R1-SIM (cone beyond exact reach) and for the attenuation model. |
| O'Brien et al. PRX Quantum 3, 030345 (2022), full text | abstract only | Compare its ergodic Hessian degeneracy quantitatively with the FI spectra (fi_method nuisance; §0 priors). Also compare its NISQ cost argument with the value lens's FT-only costing (category D examined only FT). |
| Baum, Munowitz, Garroway & Pines, JCP 1985 (MQ spin counting) | UNVERIFIED | K(t) growth law under DQ, needed for R1-DQ. |
| Oriented-sample ssNMR (PISEMA/SLF, membrane proteins) | UNVERIFIED | O'Brien's own setting is an oriented membrane. PISEMA-type methods are the classical comparator for static oriented samples and give orientational restraints classically. |
| Schuster et al. 2208.02254 (full) | abstract | Is the "echo FI > transfer FI" learning separation a category the charter recognises? It bears on how the residual claim is framed. |
| Elenewski 2406.09340 (NM-12) | unread | The protein ZULF resource claims; T2 = 1 s assumption. |

## 6. Replications not done

- Only 2 small rigid proteins, and effectively one orientation (o1 only for p19). No membrane protein or larger protein.
- Physics nuisance/rotor tests ran on 3 of 11 jobs (their test A).
- The σ-cone was measured on 2 dense probes and 1 amide probe, and only to 40 µs (dense) / 350 µs (amide).
- The classical_front families ran on 3 clusters at γ = 0 only. My classical-spin runs cover 2 probes.
- The N=10 ε=3e-5 closure covers 6 of 11 jobs (replicate lens).
- The attenuation analysis uses a single functional form per protocol.

## 7. Process gaps (CLAUDE.md)

- The FULL vs ABLATION quantum-necessity statement is implicit only. It should be written out: ablation = echo data plus exact/typicality classical forward model on the cone plus transfer; the answer to "what disappears" is nothing at N_eff ≲ 30–47.
- There is no `architectures/killed/` record.
- The ledger fields (effect size with uncertainty, statistical test, replication count) are missing from the synthesis.
- CURRENT_STATE lists "classical spins" among the echo adversaries even though they had never been run on F.

## 8. Priority actions and expected effect on the verdict

| # | Action | Cost | Expected effect |
|---|---|---|---|
| 1 | Correct items 1–10 in §1, especially the floor argument, "≤ 3", the amide ≤ 350 µs scope, the Mi quote, and categories 1–6 | none | Same verdict, sounder basis |
| 2 | Upper-tail composite-penalty table plus `prior_info.py` on all 11 jobs | ~15–20 CPU-min, governed | Kill stated on the supremum, not the median |
| 3 | Hybrid core-plus-bath adversary against the T-A reference (N ≤ 22) | new code; governed hours | Decides R1-SIM in either direction |
| 4 | Group-complete-cluster convergence rerun before T-A | < 1 CPU-h | May shrink N_σ and re-scope T-A |
| 5 | Self-consistent irreversibility (γ fitted to T3) with the adversary rerun, plus a K-dependent attenuation variant | < 30 CPU-min | Removes the single-anchor dependence; kill likely strengthens |
| 6 | Read Krojanski–Suter 2004/2006 and Fine 2014, and reconcile them with Sánchez 2022 | literature | Decides whether "intrinsic T3" can be claimed |
| 7 | Formal pre-registered outcome table (C3-kill-1/2, K-C1b, C3 survival clause) | re-analysis | Procedural: the kill can cite pre-registered survival terms |

Files written, all under `C:\Users\abena\quantum-advantage-protein-folding\research\experiments\ADVERSARIAL\R1_completeness\`:
- Scripts: `cspin_echo.py`, `delta_extrap.py`, `prior_info.py`.
- In `out\`: `cspin_echo_1UBQ_p{19,245}_N{10,12,14}_sphere.json`, `cspin_echo_1UBQ_p19_N10_dtwa.json`, `cspin_echo_1UBQ_p245_N14_dtwa.json`, `cspin_echo_summary.json`, `delta_extrap.json`, `delta_extrap_stdout.txt`, `prior_info.json`.

About 13 CPU-min in total, all single-threaded. That includes one pilot that ran about 5 CPU-min and produced no output. No files outside that folder were modified.