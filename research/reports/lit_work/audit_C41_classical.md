# Audit C41 (classical adversary): correlated multi-electron photo/strong-field ionization, joint photoelectron momentum sampling

Date: 2026-09-28. Role: classical adversary. Status: FINAL.
Verdict: **KILLED** as an advantage candidate in every channel the candidate names. A narrow residual (full-dimensional, all-quantum eta>=3 strong-field ionization at NIR/mid-IR) is a real classical *ab initio* wall, but it has no demonstrated decision consumer, and the quantum cost per rare-channel event is years to millennia.

Scope caveat: WebSearch budget was exhausted, so all searches went through the Crossref, OpenAlex, Semantic Scholar and arXiv APIs (query log at the end). "Not found" means not found in these sources through 2026-09-28. It is not proof of absence.

---

## 1. Channel-by-channel classical status

### 1a. eta = 2 (He), XUV and NIR: classically solved (validation only)
- **Full 3+3-D He at 780 nm (tSURFF).** Zielinski, Majety, Scrinzi, PRA 93, 023406 (2016), arXiv:1511.06655 [verified: S2/Crossref]. Two-electron momentum spectra, with systematic error control, reproduce experimental single-to-double ratios up to 4e14 W/cm2.
- **He at 394.5 nm, double emission.** Zhu & Scrinzi, PRA 101, 063407 (2020), arXiv:1912.09250 [verified]. Agrees with experiment.
- **Kinematically complete experiment at 394 nm.** Henrichs et al. (Dörner group), PRA 98, 043405 (2018), arXiv:1808.03516 [verified]. The DI/SI ratio is **2e-4 to 1.5e-3**. The data go from the ratio up to fully differential cross sections, so a direct ab initio vs COLTRIMS test already exists for eta=2.
- **GPU full-dimensional He TDSE code.** HeTDSE, Zhao et al., Chin. Phys. B 30 (2021), doi:10.1088/1674-1056/abe1a4 [verified]. 147x over one CPU core.
- **Approximate but experimentally validated classical shortcuts for He NSDI.** Quantitative rescattering theory (Chen et al., PRA 82, 063417 (2010) [verified]; Chin. Phys. B (2019) doi:10.1088/1674-1056/ab54b3 [verified]) and classical models (Sarkadi, JPB (2020) doi:10.1088/1361-6455/ab9764 [verified]).
- Conclusion: eta=2 is a validation target only, as the candidate already states. There is no advantage room here.

### 1b. eta = 3, XUV single/two-photon triple photoionization of Li: classical ab initio exists, experiment lacks joint data
- **Full three-electron time-dependent close-coupling (TDCC) on lattices.** Colgan, Pindzola, Robicheaux PRL 93, 053201 (2004), "Lattice calculations of the photoionization of Li" [verified Crossref]; PRA 72, 022727 (2005), double and triple PI of Li and Be [verified]; Colgan & Pindzola JPB 39 (2006), energy-differential triple PI of Li, doi:10.1088/0953-4075/39/8/006 [verified].
- **Angular (joint) break-up patterns already computed.** Colgan, Emmanouilidou, Pindzola PRL 110, 063001 (2013), arXiv:1301.2350 [verified]: "T-shape break-up" at 5 eV excess energy. It contradicts the classical-trajectory prediction of a 120-degree pattern (Emmanouilidou, Wang, Rost arXiv:0710.1885; Emmanouilidou JPB 39 (2006) doi:10.1088/0953-4075/39/20/003 [verified]).
- **Two-photon triple ionization of Li.** Colgan & Pindzola JPB 48, 181001 (2015) [verified].
- **Other classical methods.** Green's-function approach (Liu, Zeng, Yuan arXiv:1709.08796 [verified]) and half-collision model (Pattard PRA 63, 020701 (2001) [verified]).
- **Experiments measure total cross sections and ratios only.** Wehlitz et al. PRL 81, 1813 (1998); PRA 61, 030704 (2000); Juranić et al. PRA 78, 033401 (2008), up to 650 eV [all verified Crossref]. In Crossref queries for Li triple photoionization and for fully differential triple ionization, I found **no measured Li triple-photoionization joint momentum or angular distribution**.
- Consequence (lesson L5, information vs computation): the only joint-distribution information in this channel is theoretical, and a classical TDCC calculation already supplies it. The experimentally consumed quantity is a scalar cross section, which TDCC and the Green's-function methods compute. There is no decision gap. The honest open item is TDCC partial-wave convergence of the angular pattern, which is a classical convergence study, not a quantum opportunity.

### 1c. eta = 3 to 6, strong-field NIR non-sequential triple ionization (Ne, Ar): no full-dimensional ab initio, but experiment is reproduced by two independent approximate families
- **Experiments consume low-order marginals.** Zrost et al. JPB 39, S371 (2006), doi:10.1088/0953-4075/39/13/s10 [verified]; Herrwerth et al. NJP 10, 025007 (2008) [verified]. Both measure recoil-ion (Ne3+, Ar3+) momentum along polarization, which is 1-D, plus ion yields.
- **Family 1, 3-D semiclassical (ECBB/effective-Coulomb).**
  - Peters, Katsoulis, Emmanouilidou PRA 105, 043102 (2022) [verified]: a general toolkit for 3+ electrons.
  - Emmanouilidou, Peters, Katsoulis PRA 107, L041101 (2023) [verified]: "ionization spectra that agree with experiment".
  - Praill, Katsoulis, Emmanouilidou JPB (2025), doi:10.1088/1361-6455/ae2e65 [verified OpenAlex]: Ne double and triple ionization at high intensities, "strong agreement with experimental measurements, particularly for triple ionization" once focal-volume averaged.
  - CTMC for Ar triple ionization: Jiang & He PRA 104, 023113 (2021) [verified]. Dalitz-plot analysis of triple-ionization pathways: Jiang et al. PRA 105, 053119 (2022) [verified]. Early 3-e classical work: Zhou et al. Opt. Express 18, 16025 (2010) [verified].
- **Family 2, restricted-dimensionality fully quantum.**
  - Thiede, Eckhardt, Efimov, Prauzner-Bechcicki, Zakrzewski PRA 98, 031401 (2018), arXiv:1804.05773 [verified]: 3-electron restricted-dimensionality model with "reasonable agreement with experimental neon measurements following volume averaging".
  - Efimov PRA (2025) doi:10.1103/1dn8-4f6h [verified title only].
  - Thiede & Prauzner-Bechcicki PRA 110, 053105 (2024), arXiv:2407.11944 [verified]: frequency dependence of NSDI.
- **Mid-IR.** Jiang et al. NJP 25 (2023), doi:10.1088/1367-2630/acbed6 [verified]: Ar at 3100 nm, experiment explained by CTMC plus QM.
- **All-electron single-continuum ab initio.**
  - Double-continuum R-matrix/RMT extension, Plummer & Noble J. Phys. Conf. Ser. 1412, 132053 (2020) [verified]: "up to two electrons" in the continuum.
  - tRecX-haCC, Chundayil, Majety, Scrinzi CPC (2024) doi:10.1016/j.cpc.2024.109279 [verified].
  - TD-RASCI, Hochstuhl & Bonitz PRA 86, 053424 (2012), arXiv:1207.5693 [verified].
  - TD-GASCI, Bauch, Sørensen, Madsen PRA 90, 062508 (2014), arXiv:1410.2138 [verified].
  - TD-RASSCF, Miyagi & Madsen PRA 87, 062511 (2013); PRA 89, 063416 (2014) [verified titles].
  - TD-CASSCF, Sato & Ishikawa PRA 91, 023417 (2015) [verified title].
  - I found **no** published triple-continuum (three electrons simultaneously in the continuum) ab initio method at NIR wavelengths.
- **Classical wall.** Full-dimensional ab initio for eta>=3 at 800 nm and beyond, and for eta=2 at mid-IR or above about 5e14 W/cm2 at 800 nm, is not demonstrated. This is a real wall **for ab initio solution**.
- **But the wall is not a decision wall.** Two independent approximate families (3-D semiclassical, and restricted-dimensionality quantum) each reproduce the consumed observables (ion-momentum marginals, yields) within experimental and focal-volume uncertainty. In the sources searched (listed in Section 7), I found no report of converged theories disagreeing with each other, or with experiment, beyond error bars for Ne/Ar triple ionization.

### 1d. XFEL multiple ionization: sequential, handled by rate equations
- Young et al., Nature 466, 56 (2010), doi:10.1038/nature09177 [verified]: Ne response to ultra-intense X-rays, modelled by rate equations. Multiple ionization at XFELs is dominated by sequential photo- and Auger steps; correlated joint continuum sampling is not the bottleneck. This channel is killed outright.

---

## 2. Answers to the audit questions

**(1) A measured channel where converged TD-RASCI, MCTDHF and RMT disagree with each other or with experiment beyond error bars?**
None found.
- Li triple PI: experiment has totals only, and TDCC and other theories are broadly consistent with them. I did not audit the agreement at every energy.
- Ne/Ar non-sequential triple ionization: TD-RASCI, MCTDHF and RMT are not applied to the triple continuum at all. The comparison is ECBB and restricted-dimensionality models vs experiment, and both agree after focal averaging.
- He: tSURFF agrees with ratios at 780 nm and with 394 nm data.

**(2) For eta=3, does truncated correlation converge as the RAS/orbital space grows?**
No convergence study of TD-RAS-type methods on triple-continuum momentum spectra was found. They are single- or double-continuum constructions, so the question is moot for them. For eta=3 XUV, TDCC is a full-correlation lattice method (not RAS-truncated) and it exists. The candidate's "E vs F" comparison (RAS vs RMT) therefore targets methods that nobody uses for this observable. The actual competitors are TDCC (XUV) and semiclassical plus reduced-dimensionality quantum models (NIR). The wall is real only for full-dimensional NIR ab initio.

**(3) Honest qubit and Toffoli counts.** These are my order-of-magnitude estimates, not from literature. The case is He, 800 nm, 4e14 W/cm2, 8-cycle pulse.
- **Physical scales.**
  - Up about 0.88 a.u., quiver amplitude about 33 a.u.
  - p_max about sqrt(20 Up) about 4.2 a.u. for rescattered electrons.
  - Total propagation T about 2000–5000 a.u., including post-pulse separation, which is needed because the position-flag-then-QFT readout requires continuum electrons beyond R_c.
- **Grid.**
  - Box L about 2 p_max T, roughly 2e4–4e4 a.u. per dimension.
  - Coulomb cusp at Z=2 needs dx about 0.05–0.1 a.u. on a uniform grid.
  - N about 2e5–8e5 per dimension, i.e. 18–20 qubits per dimension.
- **Qubits.** System qubits = 3 eta x 19, about 115 (eta=2) or 170 (eta=3), plus a few hundred ancillas for Coulomb arithmetic. Qubit count is **not** the problem. The logarithmic box cost is the one real quantum structural edge.
- **Norms.**
  - Kinetic norm is about 3 eta (pi/dx)^2/2, about 3e3–1.2e4 a.u., so the interaction picture is mandatory.
  - The laser term must be in velocity gauge. The length-gauge norm E0 L/2 is about 1e3 a.u. or more in such boxes.
  - lambda_V is about (eta Z + eta^2)/dx, about 80–160 a.u.
- **Gate cost.**
  - Steps are about lambda_V T, roughly 2e5–8e5.
  - Each step is about 1e4–1e5 Toffoli-equivalents: pairwise 1/|r| arithmetic at 19-bit precision plus QFT rotation synthesis.
  - **G is about 1e9–1e11 Toffolis per shot** for eta=2, with a weakly larger prefactor for eta=3.
- **Absorbing boundaries.** These are non-unitary. The dilation/CAP algorithm of Mangin-Brinet et al. arXiv:2311.15859 [verified] has success probability tied to the *surviving* norm. That removes exactly the ionized flux the candidate wants to sample, so a CAP does not help momentum sampling. Without one, the quantum computer must hold the full box (qubit-cheap, time-expensive). LCHS (An et al. arXiv:2303.01029) and Schrödingerisation (Jin et al. arXiv:2304.00667) [verified] exist but do not change this.

**(4) Shot budget for rare channels.**
- Double or triple ionization is a rare branch of the laser-driven dynamics:
  - He DI/SI is 2e-4 to 1.5e-3 (Henrichs 2018).
  - Absolute per-shot p_DI is about 1e-4 or less.
  - Ne/Ar triple-ionization probability per shot is about 1e-5 to 1e-6 [order of magnitude, UNVERIFIED].
- A correlated-momentum marginal with 1e3–1e4 events costs:
  - without amplitude amplification: N_ev/p x G, about 1e4/1e-4 x 1e10 = **1e18 Toffolis**;
  - with amplitude amplification: N_ev x G/sqrt(p), about 1e4 x 1e2 x 1e10 = **1e16 Toffolis**.
- Runtime at 1e5–1e7 Toffoli/s (optimistic single-QPU fault-tolerant rates in the Babbush et al. PRX Quantum 2021 style analysis [cited from project prior, not re-verified here]): **about 30 to 3000 years** for eta=2, and 3–30x worse for triple ionization.
- Amplitude estimation of a scalar yield ratio to 10% costs about G/(0.1 sqrt(p)), about 1e13 Toffolis, i.e. days to years. Those scalars are already reproduced classically.
- A classical tSURFF run returns the entire amplitude, with all channels and no shot noise, in one HPC job (Zielinski 2016).
- CTMC/ECBB is itself a **direct classical sampler** of the joint momentum distribution. It costs microseconds to milliseconds per trajectory and handles 3–4 electrons.
- Lesson L3 applies directly: the sampling claim (category 4) faces a native classical sampler, and the resource claim (category 3) fails on per-event cost.

**(5) Do experiments consume joint information beyond low-order marginals?**
In the sources found, no.
- Triple-ionization experiments report 1-D ion momentum along polarization and yields (Zrost 2006, Herrwerth 2008).
- Kinematically complete data exist for eta=2 only (Henrichs 2018), where classical ab initio suffices.
- Theory uses Dalitz plots, a 2-D energy-sharing projection (Jiang 2022).
- COLTRIMS triple-coincidence statistics cap resolvable structure at about 1e3–1e4 events. Beyond that, a 9-D joint distribution is not experimentally testable, so the "Born-rule samples of the full joint distribution" output fails lesson L5.

**(6) Model floor for Ne/Ar.** The parameter floor is large; the atomic-model floor is not quantified.
- **Parameter floor.** Laser-parameter error dominates.
  - Focal-volume averaging is required in *every* successful comparison (Thiede 2018; Praill 2025).
  - Intensity calibration uncertainty of about 10–20% [typical; UNVERIFIED for the specific datasets] moves DI/SI by factors comparable to or larger than inter-theory differences (DI/SI varies about 7x across the Henrichs intensity range).
  - Pulse shape and CEP matter (Jiang 2023 pulse-length sensitivity at 3100 nm).
  - Nondipole effects enter at mid-IR and high intensity (Opt. Express 2020 doi:10.1364/oe.391138 [title verified via OpenAlex cites list]), so the candidate's dipole-approximation Hamiltonian itself fails in the long-wavelength regime, where the classical wall is strongest.
- **Atomic-model floor.** Ar has 8 valence electrons. An eta=3 active-electron model with a frozen/pseudopotential core is itself an approximation whose error is not quantified. Recollision excitation of Ar+ involves the other valence electrons. An exact quantum solution of a 3-active-electron model does not beat that model floor (lesson L6).

---

## 3. Where classical computation actually fails, and why that does not rescue C41

| Regime | Classical ab initio | Classical approximate that matches experiment | Decision consumer |
|---|---|---|---|
| eta=2, XUV, 394 nm, 780 nm up to 4e14 | yes (tSURFF, HELIUM-type, HeTDSE) | QRS, CTMC | fully differential data exist, and theory agrees |
| eta=2, 800 nm above 5e14 or mid-IR | not demonstrated in full 6-D (no source found) | QRS, CTMC, reduced-dimensionality | yields, correlated p-parallel marginals |
| eta=3 Li, XUV 1- and 2-photon | yes (TDCC 2004–2015) | half-collision, classical | total cross sections only |
| eta=3–4 Ne/Ar, NIR NSTI | **no** (wall) | ECBB 3-D and restricted-dimensionality quantum both agree after focal averaging | 1-D ion momentum, yields |
| XFEL multiple ionization | rate equations | rate equations | charge-state distributions |

The only true wall (last-but-one row) has observables that two independent classical approximate families already reproduce. Converged exact solutions are not required for the consumed marginals. A quantum sampler would cost about 1e16 or more Toffolis per useful dataset, compared with CPU-hours for CTMC. This is the same pattern as lesson L5: hard where uninformative.

## 4. Would tensor networks, a better heuristic, or single-family hardness change things?
- **Better heuristics already win.** Semiclassical ECBB with focal averaging is a cheap direct sampler.
- **Hardness is not single-family.** The literature already uses two different classical families, trajectory-based and reduced-dimensionality grid-based, and they agree with experiment.
- **Tensor-network or low-rank (MCTDHF/TD-RASSCF-type) triple-continuum extensions are not yet attempted.** Their absence is a gap in effort, not demonstrated hardness. Lesson L1 (false hardness from stopping the ladder early) applies.
- **Unexploited shortcut.** Two-step factorization: an ab initio single-continuum amplitude (haCC/RMT), then classical or semiclassical propagation of the second and third electrons (QRS-style). It is widely used for eta=2 (QRS) and is extensible.

## 5. Cheapest decisive classical kill experiment (proposed, not run)
**Target.** Ne3+ and Ar3+ recoil-ion p-parallel distributions and 3-electron Dalitz energy-sharing marginals at the Zrost 2006 and Herrwerth 2008 conditions.
1. Run (i) the open ECBB/effective-Coulomb semiclassical toolkit (Peters 2022 / Praill 2025) and (ii) the Thiede 2018 restricted-dimensionality quantum model, both focal-volume averaged over an intensity band of plus or minus 15%.
2. Add (iii) a hybrid: tRecX-haCC single-continuum ionization amplitude followed by CTMC for the recollision cascade.
3. Decision metric: the inter-family spread in each marginal against (a) the spread induced by plus or minus 15% intensity uncertainty and (b) experimental statistical error.
4. **Kill confirmed** if the inter-family spread is below max(a, b) for all consumed marginals.
5. **C41 reopened only if** the spread exceeds max(a, b) *and* a proposed coincidence measurement could discriminate. Even then, reopening means a classical ab initio effort first (a triple-continuum MCTDHF or tensor-network attempt) before any quantum claim.

Cost: order 1e3–1e4 CPU-hours with existing codes. This is within this machine's reach for the semiclassical part.

## 6. Novelty note (secondary to this audit)
arXiv API query (quantum computer x strong-field/attosecond/double ionization/HHG) found:
- 2112.06365, NISQ multistate transition dynamics for atomic ionization by attosecond pulses [verified title];
- 2403.08729, time-dependent product formulas [verified title];
- no algorithm for correlated multi-electron continuum sampling.

Scoped novelty B stands. It does not rescue the candidate, because the kill is on classical sufficiency and cost, not on novelty.

## 7. Query log (all via WebFetch; WebSearch budget exhausted)
1. arXiv API: abs "triple photoionization" AND lithium
2. Crossref: triple photoionization lithium (rows 25)
3. Crossref: fully differential triple ionization three electrons coincidence (from 2010)
4. arXiv API: double ionization helium tSURFF / full-dimensional infrared (timeout; retry got HTTP 429)
5. Crossref: double photoelectron momentum spectra helium infrared tSURFF
6. Crossref: nonsequential double ionization helium 800 nm full-dimensional TDSE (from 2015)
7. Crossref record 10.1088/1674-1056/abe1a4 (HeTDSE)
8. Crossref / S2 record PRA 93, 023406 (Zielinski)
9. S2: TD-CASSCF double ionization (HTTP 429). Crossref: time-dependent multiconfiguration double ionization many-electron strong field (from 2016)
10. Crossref record Plummer & Noble 2020
11. Crossref: author Colgan Pindzola + triple photoionization
12. S2 record PRL 110, 063001
13. Crossref: nonsequential triple ionization strong field (from 2008)
14. S2 records PRA 104, 023113 and PRA 110, 053105
15. OpenAlex: W2173353984 and cited-by list (44 works)
16. S2 records PRA 101, 063407 and PRA 98, 043405
17. OpenAlex records: JPB 2025 ae2e65, NJP 2023 acbed6, PRA 105, 043102, PRA 107, L041101, PRA 1dn8-4f6h, CPC 2024 haCC
18. Crossref: triple ionization lithium three-electron continuum ab initio (from 2014)
19. S2 record PRA 98, 031401 (Thiede 2018)
20. Crossref: restricted active space TD double photoionization beryllium (from 2011); S2 records Hochstuhl 2012, Bauch 2014
21. Crossref: TD-ORMAS double ionization momentum (from 2015)
22. arXiv API: quantum computer x strong-field/attosecond/double ionization/HHG
23. Crossref: strong-field triple ionization Ar/Ne ion momentum experiment; bibliographic lookups for Zrost 2006 and Herrwerth 2008
24. Crossref: three-electron full-dimensional TDSE laser ionization (from 2016)
25. arXiv API: quantum algorithm x absorbing boundary / CAP / ECS
26. Crossref: Young et al. Nature 2010

Items marked [UNVERIFIED]:
- typical intensity-calibration uncertainty of 10–20%;
- absolute triple-ionization per-shot probability of 1e-5 to 1e-6;
- Toffoli-rate assumptions;
- all Toffoli, qubit and shot numbers in Section 2(3)–(4), which are my own estimates.
