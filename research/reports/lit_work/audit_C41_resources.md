# Audit C41 (resource / break-even analyst): correlated multi-electron photo- and strong-field ionization, sampling joint photoelectron momentum distributions

Date: 2026-09-28. Status: COMPLETE (resource lens). Author role: resource / break-even analyst.
WebSearch budget was exhausted this session (200/200). All searches went through WebFetch against Crossref, OpenAlex and arXiv (export API and abs pages). The arXiv export API and OpenAlex rate-limited several calls (HTTP 429); those failures are listed in the query log.

**Verdict: WOUNDED.** The quantum speedup is not quadratic: classical memory grows exponentially in the number of electrons eta, while the quantum cost is polynomial. Logical-qubit counts are modest (about 400-1,000). Per-shot Toffoli counts are FeMoco-class (about 1e8.5-1e10.5). The claim fails on the output side instead. The channels of scientific interest (triple or multiple ionization) are rare, with 1e-5 to 1e-3 of events. A single Born-rule sample costs hours to weeks of fault-tolerant runtime. A fully differential category-4 sampling claim therefore needs about 1e14-1e16 Toffolis, which is centuries per machine, and that claim is effectively killed. What survives is a narrow category-3 target. The object is a low-order observable, such as a multiple-ionization yield ratio or a correlated momentum marginal, estimated by amplitude estimation for eta = 3-4 in the near-IR. The cost is about 1e12-1e13 Toffolis, i.e. months to years on one late-fault-tolerant machine or weeks on a small fleet. This target counts only if the classical audit (audit_C41_classical.md) shows that RAS-type methods do not converge there. It is not feasible on NISQ hardware and needs fault tolerance.

---

## 1. Scoped novelty check (resource-relevant only)

In the sources searched through 2026-09-28 (Crossref, OpenAlex, arXiv abs pages, and the partial arXiv API results below), the following were found:
- Grid/first-quantized quantum-simulation work that includes "ionization" and "scattering" on 2D/3D model atoms with one or two particles. This work was emulated with up to 36 qubits, with no laser-driven multi-electron momentum sampling and no comparison against a classical TDSE code: Chan, Meister, Jones, Tew, Benjamin, Sci. Adv. 2023, doi:10.1126/sciadv.abo7484, arXiv:2202.05864 [VERIFIED arXiv abs].
- First-quantized FT chemistry cost models: Su et al. arXiv:2105.12767 [VERIFIED].
- Nearby FT continuum/dynamics resource estimates: Rubin et al. arXiv:2308.12352 (stopping power) [VERIFIED]; Kharazi et al. arXiv:2602.20234 (EUV photoemission) [VERIFIED].
- A non-unitary (complex absorbing potential) simulation primitive: An, Liu, Lin, LCHS, arXiv:2303.01029, PRL 131, 150603 (2023) [VERIFIED].

No paper was found that estimates FT resources for correlated multi-electron (eta >= 2) laser-driven ionization with joint-momentum readout, and none compares such an estimate with TDCC, tSURFF, RMT or TD-RASCI costs. This supports scoped category **B** from the resource side. It is not proof of absence.

---

## 2. Classical cost of the strongest methods, and where the exact wall actually is

| System / regime | Strongest classical result found | Status |
|---|---|---|
| He, eta=2, XUV and 780 nm IR | Zielinski, Majety, Scrinzi PRA 93, 023406 (2016), doi:10.1103/physreva.93.023406. Full 3+3-D tSURFF with "systematic error control". It reproduces the experimental single-to-double ratio up to 4e14 W/cm^2 at 780 nm [VERIFIED OpenAlex W2173353984 abstract]. See also HELIUM, Parker et al. PRL 96, 133001 (2006), doi:10.1103/physrevlett.96.133001 (390 nm) [VERIFIED Crossref title/DOI] and Zhu & Scrinzi-group PRA 101, 063407 (2020), 400 nm [VERIFIED Crossref] | **Classically solved.** No quantum case. |
| Li, eta=3, XUV single-photon triple ionization | Colgan, Pindzola, Robicheaux PRL 93, 053201 (2004), doi:10.1103/physrevlett.93.053201. They solve the TDSE "in nine dimensions using a radial lattice for three dimensions and coupled channel expansion for the other six" and report "good agreement with experimental measurements" [VERIFIED OpenAlex W2010807972 abstract]. Follow-ups: Colgan et al. PRA 72, 022727 (2005), Li and Be, doi:10.1103/physreva.72.022727; J. Phys. B 39, 1537 (2006), energy-differential triple PI of Li, doi:10.1088/0953-4075/39/8/006 [VERIFIED Crossref] | **Classically done, on 2004-era hardware.** The candidate's headline "Li eta=3 XUV" target is not a classical wall. |
| eta=3 in near-IR strong field (3 continuum electrons) | No exact full-dimensional result found in this search. Semiclassical: Jiang et al. PRA 104, 023113 (2021), doi:10.1103/physreva.104.023113 (NS triple ionization of Ar) [VERIFIED Crossref]. RMT double-continuum extension: Wragg et al. PRA 92, 022504 (2015), doi:10.1103/physreva.92.022504; Plummer et al. J. Phys. Conf. Ser. 1412, 132053 (2020), doi:10.1088/1742-6596/1412/13/132053 [VERIFIED Crossref] | Frontier. The exact classical cost is estimated below. |
| eta >= 4 (Ne/Ar NS multiple ionization) | TDDFT (Bauer, Opt. Express 8, 377, 2001, doi:10.1364/oe.8.000377) [VERIFIED Crossref], semiclassical/CTMC, TD-CASSCF/TD-ORMAS (see the classical audit) | No exact method. Truncated-correlation methods only. |

**Order-of-magnitude memory for an exact partial-wave lattice with tSURFF** (the tSURFF radial box is about 100-300 au instead of about 1e4 au):
- Amplitudes are about N_r^eta x N_ch(eta, l_max), with N_r of about 300 FE-DVR radial points and l_max of about 20-40 per electron in the IR.
- eta=2: 300^2 x (1e3-1e4) = 1e8-1e9 amplitudes, about 1.6-16 GB. Feasible, as Zielinski 2016 confirms.
- eta=3: 300^3 x (1e5-1e6) = 3e12-3e13 amplitudes, about 43-430 TB. Each step costs about 1e2-1e3 flops per amplitude, and a run is about 1e5 steps, giving about 1e20-1e21 flop. This is **borderline exascale**. Leadership machines have petabyte-scale aggregate GPU memory [UNVERIFIED figure]. The exact wall for eta=3 in the IR is therefore high but plausibly penetrable with a dedicated campaign. The channel-count exponent is the most uncertain factor.
- eta=4: 300^4 x about 1e7 = 8e16 amplitudes, about 1 EB. **Infeasible.** The exact classical wall sits at **eta = 4** (IR) and about eta = 4-5 (XUV).
- The classical competitor that matters at eta >= 4 is therefore polynomial truncated correlation: TD-RASCI, TD-ORMAS, TD-CASSCF, MCTDHF and RMT with restricted outer regions. Whether these converge is the classical audit's question and decides the result.

---

## 3. Quantum algorithm and end-to-end cost model

### 3.1 Encoding
- First quantization on a periodic Cartesian grid / plane-wave basis. Each electron has 3 registers of n_p = log2(L/dx) qubits, for 3 eta n_p system qubits in total. This follows Su et al. 2105.12767 [VERIFIED] and Chan et al. 2202.05864 [VERIFIED].
- **Velocity gauge.** H0(t) = sum_i (p_i + A(t))^2 / 2 is diagonal in momentum, so it is fast-forwarded exactly in the interaction picture at a cost of about eta x 3 x n_p^2 Toffolis per segment for the squared-momentum phase. Only the Coulomb part needs a block-encoding, handled by Dyson-series interaction-picture simulation (Low & Wiebe arXiv:1805.00675 [VERIFIED]). The laser therefore adds essentially nothing to lambda. This is favourable for the candidate.
- **Box size is almost free.** L enters only through n_p = log2(L/dx), and lambda does not depend on L (see below). This is the one place where the quantum encoding beats the classical one qualitatively. No absorbing boundary is needed. Choose L greater than about 2 p_max T to avoid wrap-around. For the IR case (p_max about 6.6 au, the 10 Up cutoff at about 1e15 W/cm^2 and 800 nm; T about 1,500 au), L is about 2e4 au and n_p is about 17.
- **Non-unitary absorbing boundaries are unnecessary and harmful.** An absorbing boundary removes exactly the ionized flux that is to be sampled. LCHS (arXiv:2303.01029 [VERIFIED]) can apply a CAP, but the success probability then decays with the absorbed norm. Use the large unitary box with a coherent position flag instead.

### 3.2 Block-encoding normalization lambda (derived)
For plane waves in a cube of side L with cutoff k_c = pi/dx, sum over nu != 0 of 1/|nu|^2 is about 2 pi N_1D. This gives:
- lambda_U (electron-nucleus) is about 2 eta Z / dx, and lambda_V (electron-electron) is about eta(eta-1)/dx, in Hartree. Both are independent of L and scale as 1/dx.
- **Cusp-driven dx.** Plane-wave energy error for a hydrogenic cusp is about C Z^2 (Z/k_c)^3, since the Fourier tail is about k^-4. Requiring about 1e-3 au absolute error (threshold energies of about 7.5 au for Li^3+) gives:
  - Li (Z=3): k_c >= 65 au, so dx is about 0.05 au.
  - Ne (Z=10, all-electron): dx is about 0.007 au.
  - Ar (Z=18): dx is about 0.0025 au.
  - C is O(1) and not computed here. Treat all three as order-of-magnitude values.
- Resulting lambda:
  - Li, eta=3, dx=0.05: lambda_U is about 360 Ha, lambda_V about 120, total about **480 Ha**.
  - All-electron Ne (eta=10, Z=10, dx=0.007): lambda is about 2x100/0.007 + 90/0.007, about **4e4 Ha**. This is prohibitive for long IR times, so Ne and Ar need pseudopotentials or a frozen core (section 5, model floor).
  - Ne/Ar with 6 active electrons, a smooth pseudopotential, dx about 0.15 and Z_eff about 8: lambda_U about 640, lambda_V about 200, nonlocal PP about the same order, total about **1e3 Ha**.

### 3.3 Toffoli per qubitization/Dyson step
Following the structure of Su et al. (state preparation over nu about O(n_p^2), controlled swaps of eta registers about 2 x 3 eta n_p, phase arithmetic k_nu . R about 6 n_p n_R, plus the H0 fast-forward):
- about **3-5e3 Toffolis per step for eta=3**
- about **1e4 per step for eta=6** (n_p about 17, including the PP)

These are derived, not quoted. Su et al. give only the asymptotic Õ(eta^{8/3} N^{1/3} t) in their abstract.

### 3.4 Per-shot cost
| Case | lambda (Ha) | T (au) | steps (about 1.2 lambda T) | Toffoli/step | **Toffoli/shot** | wall-clock/shot at 170 us/Toffoli (1 CCZ factory, d about 31) | at 10 us/Toffoli (multi-factory) |
|---|---|---|---|---|---|---|---|
| He 780 nm (eta=2, dx 0.07) | about 140 | about 1,500 | about 2.5e5 | about 2.5e3 | **about 6e8** | about 1.2 d | about 1.7 h |
| Li XUV triple PI (eta=3, dx 0.05) | about 480 | 100-300 | 6e4-1.7e5 | 3-5e3 | **about 2e8-8e8** | 0.4-1.6 d | 0.6-2.3 h |
| Li/Be+-like eta=3 in IR | about 500 | about 1,500 | about 9e5 | about 4e3 | **about 4e9** | about 8 d | about 11 h |
| Ne/Ar 6 active e, PP, 800 nm | about 1e3 | about 1,500 | about 1.8e6 | about 1e4 | **about 2e10** | about 40 d | about 2.3 d |

Toffoli timing calibration: the Gidney-Fowler CCZ factory produces "one |CCZ> every 5.5d surface code cycles" (arXiv:1812.01238 [VERIFIED]), which is about 170 us at d=31 with a 1 us cycle. For scale, Lee et al. THC FeMoco is "about 4 million physical qubits, less than 4 days" at a 1 us cycle (arXiv:2011.03494 [VERIFIED]). The He/Li per-shot costs are therefore about 0.1-0.3 of a FeMoco-class phase-estimation run, and the eta=6 IR shot is about 5-10 FeMoco-class runs. Rubin et al. 2308.12352 put stopping power at "about one hundred times more Toffoli gates" than FeMoco/P450-class estimates [VERIFIED abstract]. Kharazi et al. 2602.20234 put EUV photoemission at ">= 1e14 gates" per circuit with 1e4 shots [VERIFIED abstract]. C41 per shot is 3-5 orders of magnitude cheaper than EUV photoemission because eta is small.

### 3.5 Logical and physical qubits
- System register: 3 eta n_p = 135 (eta=3, n_p=15) to 306 (eta=6, n_p=17).
- Ancillas: nu-state preparation, arithmetic for |k_nu . R|, PP, Dyson time register and channel flags add about 2-3 times the system register. Total about **400-1,000 logical qubits**, below FeMoco-THC scale.
- Physical: about 2d^2 per logical at d about 25-31, i.e. about 1.2-2e3 per logical, giving about **1-2e6 physical** plus factories.
- **Not NISQ-feasible.** The circuit needs 100-300 system qubits and more than 1e8 coherent arithmetic Toffolis, including 1/r or 1/|nu| evaluation. No analog or NISQ encoding of the long-range 3D multi-electron Coulomb continuum at this size is known, and none was found in this search.

### 3.6 State preparation (not dominant)
- The initial state is the atomic ground state, well approximated by HF/CI (overlap above 0.9). Antisymmetrization in first quantization costs O(eta log eta log N). The Berry et al. 2018 sort-based method is cited from memory, [UNVERIFIED].
- QPE filtering at a gap of about 0.1 au costs about lambda/gap = 5e3 steps, much less than the 1e5-1e6 dynamics steps.
- For single-photon XUV, prepare D|psi0> (first-order perturbation theory, block-encoded dipole) rather than a weak pulse. This removes a weak-field factor that would otherwise multiply the rare-channel probability by the per-pulse ionization probability of about 1e-2.

### 3.7 Readout
- Coherently compute per-electron flags "|r_i| > R" (about O(eta n_p) Toffolis each), then QFT every electron register and measure. One shot gives the channel label plus all 3 eta momenta: a Born sample of exactly what a COLTRIMS coincidence event records.
- Momentum resolution 2 pi / L is about 3e-4 au (negligible).
- Long-range Coulomb distortion of asymptotic momenta requires long post-pulse propagation or a Coulomb-corrected projection. This is the same issue classical tSURFF faces and is included in T.

---

## 4. Shot budget and break-even (the deciding section)

**Rare-channel probabilities.**
- Li: the triple PI cross section "never exceeds 6 b" (Wehlitz et al. PRL 81, 1813 (1998), doi:10.1103/physrevlett.81.1813, [VERIFIED OpenAlex W2330959098 abstract]). The Li single PI cross section at 200-400 eV is of order 1e4-1e5 b [UNVERIFIED magnitude], so the triple/total ratio p3 is about 1e-5 to 1e-4 even after D|psi0> preparation.
- Ar/Ne NS triple ionization in the IR: p3 is about 1e-4-1e-3 per pulse near saturation [UNVERIFIED typical ratio].

**Events needed.** A differential comparison (a 2D correlated momentum map, or TDCS in a fixed geometry) at a few-% statistical error per bin needs about 1e4 events in the channel. Existing NS triple-ionization COLTRIMS datasets have about 1e3-1e4 events [UNVERIFIED].

**Total cost of fully differential sampling (category-4 claim):**
| Case | p | Circuits: no amplification (1e4/p) | Circuits: amplitude amplification (1e4 x pi/(4 sqrt p)) | Total Toffoli with AA | Single machine at 10 us/Toffoli |
|---|---|---|---|---|---|
| Li XUV triple | 1e-5-1e-4 | 1e8-1e9 | 8e5-2.5e6 | 4e14-2e15 (at 5e8/shot) | **130-630 yr** |
| eta=3 in IR | 1e-4 | 1e8 | 8e5 | 3e15 | **about 1,000 yr** |
| Ne/Ar 6e, IR, triple | 1e-4-1e-3 | 1e7-1e8 | 2.5e5-8e5 | 5e15-1.6e16 | **1.6e3-5e3 yr** |
| same, 1e3 events (matched to experiment) | 1e-4-1e-3 | | 2.5e4-8e4 | 5e14-1.6e15 | 160-500 yr |

At 170 us/Toffoli, multiply by 17. Sampling parallelizes perfectly across machines, but a fleet of 100-1,000 FT machines of about 1e6 physical qubits each is needed to reach about 1 year. **Measurement and sampling dominate the end-to-end cost, not simulation.** Amplitude amplification helps only quadratically in 1/p, as lesson L3 says.

**Low-order marginals by amplitude estimation (category-3 claim):**
- A yield ratio (e.g. N3+/N2+) to relative precision delta needs about pi/(delta sqrt p) coherent runs. At delta = 5% and p = 1e-4 that is about 6e3 runs.
  - Li XUV (5e8/shot): about 3e12 Toffoli, about 1 yr at 10 us. This is classically done (Colgan 2004), so it gives no advantage.
  - eta=3 IR (4e9): about 2.5e13 Toffoli, about 8 yr at 10 us/Toffoli (about 0.8 yr with 10 machines).
  - eta=6 IR (2e10): about 1.2e14 Toffoli, about 40 yr at 10 us.
  - If p is about 1e-3, divide all three by about 3.
- A marginal with K bins (e.g. a sum-momentum histogram parallel to the polarization, about 30 bins) costs about K times more by naive per-bin estimation. It can instead be sampled directly, conditioned on the channel flag via AA, at the cost in the table above.

**Break-even against the classical wall:**
- eta <= 2 (any wavelength) and eta = 3 (XUV): the classical cost (hours to weeks on a cluster, done 2004-2020) is far below the quantum cost (years of FT runtime). The quantum approach is **not competitive**.
- eta = 3 (IR): the classical exact cost is about 1e20-1e21 flop and about 1e2 TB, which is borderline exascale but not impossible. The quantum cost is about 2.5e13 Toffolis for a single scalar observable, i.e. years. **No clear break-even.**
- eta >= 4 (IR): exact classical methods are infeasible (about EB memory), so the quantum approach is the only exact route. It needs pseudopotentials, which reintroduces a model floor (section 5). The polynomial RAS/CASSCF/CTMC methods cost minutes to days. **Break-even exists only against exact classical methods, not against the approximate methods experiments actually use.** Whether that matters depends on those methods failing to converge (classical audit), and on experiments resolving the difference (L5).

**Focal-volume, CEP and intensity-calibration averaging.** This is one genuine structural advantage of the sampling formulation. The experimental observable is a classical mixture over intensities, and the quantum sampler can draw I from the focal-volume distribution per shot at **zero multiplicative overhead**. A classical grid code needs about 10-30 separate intensity runs. This softens the classical side by about 1 order of magnitude, but it does not change the break-even conclusion.

---

## 5. Model floor (L6) and information relevance (L5), resource view

- **Li and He (all-electron, XUV):** the nonrelativistic dipole Coulomb model floor is small. Nondipole corrections are about k_photon/p, roughly 7.5/137, a few percent in angular distributions at about 250 eV. They can be added to H0 at negligible cost because they are diagonal in momentum. Solver error can dominate here, but these systems are classically solved.
- **Ne and Ar (eta_active = 4-6):** all-electron treatment costs about 40 times more in lambda (4e4 vs 1e3 Ha) and gives more than 1e11 Toffolis per shot, which is prohibitive. The active-electron model needs a pseudopotential or frozen core. Its error (core polarization, core-valence correlation and relaxation during recollision) is of the same kind as the error in the truncated classical methods being attacked. An exact quantum solution of the PP model is therefore not obviously more accurate than a converged TD-RASCI with an explicit core.
- **Experimental comparison floor:** in NS multiple ionization, intensity calibration uncertainty (tens of %), focal averaging and low coincidence statistics (about 1e3 events [UNVERIFIED]) limit discrimination to qualitative features of low-order marginals. This echoes the protein-NMR L5 lesson. The regime where exact computation is classically impossible (eta >= 4, IR) coincides with the regime where experiments carry the least resolving power.
- **XFEL multiple ionization of Ne** is dominated by sequential single-photon and Auger steps modelled by rate equations. The correlated-continuum fraction is small, so it is a poor target (resource view; not quantified here).

---

## 6. Answers to the audit questions (resource lens)

1. **Disagreeing converged methods:** out of scope for the resource lens; see the classical audit. Li XUV triple PI (eta=3) agrees with experiment from the 2004 9D lattice. He 780 nm reproduces the experimental double/single ratio up to 4e14 W/cm^2 (2016).
2. **eta=3 truncated convergence:** not tested here. The exact eta=3 XUV case is classically done, and the eta=3 IR exact case is borderline exascale (section 2). The genuine exact classical wall is at eta = 4.
3. **Honest counts:**
   - 400-1,000 logical qubits and about 1-2e6 physical.
   - Toffoli per shot: about 2e8-8e8 for eta=3 XUV, about 4e9 for eta=3 IR, about 2e10 for eta=6 IR with PP, and more than 1e11 all-electron Ne.
   - Cusp resolution sets dx, and dx sets lambda (as 1/dx). The large IR box costs only log2 L qubits.
   - Absorbing boundaries should be avoided (a unitary large box plus a coherent flag). The LCHS CAP route exists but wastes the ionized norm.
4. **Shot budget:** fully differential rare-channel sampling needs 1e14-1e16 Toffolis, i.e. centuries per machine even with AA (quadratic only). S x G is **outside FT feasibility** for category-4 claims. Scalar or marginal amplitude estimation needs 1e12-1e14 Toffolis: months to decades per machine, with fleet-parallelizable sampling.
5. **Joint information consumed:** experiments consume low-order marginals (yield ratios, sum-momentum and 2D correlated momentum maps); the full joint distribution is not used. The Born-sampling selling point therefore carries little decision-relevant surplus over amplitude-estimated marginals, which is lesson L5.
6. **Model floor for Ne and Ar:** it is not small once a pseudopotential or frozen core is used, and it is needed because all-electron lambda is prohibitive (section 5).

---

## 7. Resource verdict

- Speedup type: exponential in memory (N^{3 eta} versus poly(eta, log N)). This is not quadratic, so the Babbush et al. 2021 objection to quadratic speedups (arXiv:2011.04149 [VERIFIED]) applies only to the amplitude-amplification layer.
- Bottleneck: the Born-rule sample rate times the rare-channel probability. Measurement dominates.
- Break-even: this is the section 4 conclusion. The approach beats exact classical methods only at eta >= 4 in the IR, where a pseudopotential model floor and weak experimental resolution erode the scientific payoff. It never beats polynomial approximate methods on cost.
- **WOUNDED.** Kill the "fully differential sampling advantage (category 4)" and "Li XUV eta=3" framings. Keep one narrowly scoped category-3 benchmark: a low-order observable, such as the NS triple/double ratio or a sum-momentum marginal, for an eta = 3-4 system in the near-IR at a single intensity. Compute it with a cost model of about 1e12-1e13 Toffolis, conditional on the classical audit showing that TD-RASCI/TD-CASSCF/RMT do not converge on that observable. FT is required. The earliest plausible scale is fleets of about 1e6-physical-qubit machines.
- Scheduled kill criterion: if a converged truncated-correlation method (or exascale exact eta=3) reproduces the target marginal to within the experimental error, kill.

---

## Query log (2026-09-28)
1. WebSearch "triple photoionization lithium time-dependent close-coupling Colgan Pindzola fully differential" -> budget exhausted (200/200).
2. WebSearch "quantum algorithm photoionization strong-field ionization quantum computer simulation 2024 2025" -> budget exhausted.
3. OpenAlex search "triple photoionization lithium" -> HTTP 429.
4. arXiv API abs:"quantum algorithm" AND abs:ionization AND abs:laser -> 1 irrelevant hit (2506.00575, Rydberg-Landau qubits).
5. arXiv API abs:"quantum computer" AND (photoionization | strong-field | double ionization | attosecond) -> HTTP 429.
6. Crossref "triple photoionization lithium time-dependent" -> Wehlitz 1998 PRL, van der Hart 1998, Colgan 2006 JPB, Emmanouilidou 2006, Pattard 2001, Cooper 1999, Wehlitz 2000.
7. Crossref "Colgan Pindzola Robicheaux lithium triple photoionization fully quantal" -> PRL 93 053201 (2004), PRA 72 022727 (2005), JPB 39 (2006).
8. Crossref "nonsequential triple ionization neon argon momentum laser correlated" -> Jiang PRA 104 023113 (2021, semiclassical Ar NS triple), Augst 1995, Chen 2024 JPB (Ne NSDI).
9. arXiv abs 2308.12352 (Rubin stopping power) -> verified.
10. arXiv abs 2602.20234 (Kharazi EUV) -> verified; 200 logical qubits and 1e9 non-Clifford gates for absorption; >=1e14 gates, 1e4 shots, several thousand logical qubits for photoemission.
11. arXiv abs 2105.12767 (Su first quantization) -> verified.
12. arXiv API "first quantization" AND dynamics -> timeout.
13. arXiv API "quantum algorithm" AND (attosecond | high-harmonic | photoelectron) -> HTTP 429.
14. OpenAlex "quantum algorithm strong-field ionization simulation" -> HTTP 429.
15. Crossref "quantum computer simulation strong-field ionization attosecond algorithm" -> HTTP 429.
16. Crossref "helium double ionization 800 nm full dimensional tSURFF" -> MCTDHF He double ionization 2012 (Mol. Phys.), Bauer TDDFT Ne 2001, Muller 5D 2001, etc.
17. Crossref "Zielinski Majety Scrinzi double photoelectron momentum spectra helium infrared" -> PRA 93 023406 (2016); Zhu PRA 101 063407 (2020); tRecX-haCC 2024.
18. Crossref "Parker Taylor HELIUM double ionization 390 nm" -> PRL 96 133001 (2006).
19. arXiv abs 2202.05864 (Chan et al. grid methods, Sci. Adv.) -> verified; includes ionization/scattering in emulation with up to 36 qubits.
20. arXiv abs 1805.00675 (Low-Wiebe interaction picture) -> verified.
21. arXiv pdf 2202.05864 -> too large (content-length error).
22. arXiv API abs:"absorbing boundary" AND quantum AND algorithm -> 2601.13269 (leaking quantum walks, photonic), 2009.03618 (HHL hitting probabilities); no TDSE-CAP algorithm besides LCHS.
23. arXiv abs 2011.04149 (Babbush, beyond quadratic) -> verified.
24. arXiv abs 2303.01029 (LCHS; CAP example) -> verified.
25. APS abstract pages PRL 81 1813 and PRL 93 053201 -> HTTP 403; used OpenAlex instead.
26. OpenAlex doi:10.1103/physrevlett.93.053201 -> abstract verified (9D lattice, agreement with experiment).
27. OpenAlex doi:10.1103/physrevlett.81.1813 -> abstract verified (triple PI <= 6 b, 187-424 eV).
28. OpenAlex doi:10.1103/physreva.93.023406 -> abstract verified (3+3-D tSURFF, 780 nm, ratio reproduced up to 4e14 W/cm^2).
29. Crossref "R-matrix time dependence double ionization two-electron outer region" -> Wragg PRA 92 022504 (2015); Plummer JPCS 1412 132053 (2020).
30. Crossref "TD-RASCI multiple ionization convergence" -> HTTP 429.
31. arXiv API "quantum computer" AND (photoionization | double ionization | HHG | ATI) -> HTTP 429.
32. OpenAlex "quantum computer algorithm photoionization" (2020+) -> no QC simulation of photoionization; one flagged hit (ion-photoelectron entanglement, JPB 2022, doi:10.1088/1361-6455/ac6e17) is not a quantum algorithm.
33. arXiv abs 1812.01238 (Gidney-Fowler CCZ factory) -> verified.
34. arXiv abs 2007.14460 -> wrong ID (von Burg catalysis); corrected to 2011.03494 (Lee THC FeMoco) -> verified.

## Citations and verification status
- Chan, Meister, Jones, Tew, Benjamin, "Grid-based methods for chemistry simulations on a quantum computer", Sci. Adv. (2023), doi:10.1126/sciadv.abo7484, arXiv:2202.05864. [VERIFIED arXiv abs]
- Su, Berry, Wiebe, Rubin, Babbush, "Fault-tolerant quantum simulations of chemistry in first quantization", PRX Quantum 2, 040332 (2021), arXiv:2105.12767. [VERIFIED]
- Low & Wiebe, "Hamiltonian simulation in the interaction picture", arXiv:1805.00675. [VERIFIED]
- An, Liu, Lin, "Linear combination of Hamiltonian simulation for nonunitary dynamics with optimal state preparation cost", PRL 131, 150603 (2023), arXiv:2303.01029. [VERIFIED]
- Rubin et al., "Quantum computation of stopping power for inertial fusion target design", arXiv:2308.12352. [VERIFIED]
- Kharazi et al., "Quantum Simulations for Extreme Ultraviolet Photolithography", arXiv:2602.20234. [VERIFIED]
- Babbush et al., "Focus beyond quadratic speedups for error-corrected quantum advantage", arXiv:2011.04149. [VERIFIED]
- Gidney & Fowler, "Efficient magic state factories with a catalyzed |CCZ> to 2|T> transformation", Quantum 3, 135 (2019), arXiv:1812.01238. [VERIFIED]
- Lee et al., "Even more efficient quantum computations of chemistry through tensor hypercontraction", arXiv:2011.03494. [VERIFIED]
- Colgan, Pindzola, Robicheaux, "Lattice calculations of the photoionization of Li", PRL 93, 053201 (2004), doi:10.1103/physrevlett.93.053201. [VERIFIED OpenAlex W2010807972]
- Colgan et al., "Double and triple photoionization of Li and Be", PRA 72, 022727 (2005), doi:10.1103/physreva.72.022727. [VERIFIED Crossref]
- Colgan et al., "Energy differential cross sections for the triple photoionization of lithium", J. Phys. B 39 (2006), doi:10.1088/0953-4075/39/8/006. [VERIFIED Crossref]
- Wehlitz et al., "Triple photoionization of lithium", PRL 81, 1813 (1998), doi:10.1103/physrevlett.81.1813. [VERIFIED OpenAlex W2330959098]
- Zielinski, Majety, Scrinzi, "Double photoelectron momentum spectra of helium at infrared wavelength", PRA 93, 023406 (2016), doi:10.1103/physreva.93.023406. [VERIFIED OpenAlex]
- Parker et al., "High-energy cutoff in the spectrum of strong-field nonsequential double ionization", PRL 96, 133001 (2006), doi:10.1103/physrevlett.96.133001. [VERIFIED Crossref]
- Zhu et al., "Electron double-emission spectra for helium atoms in intense 400-nm laser pulses", PRA 101, 063407 (2020), doi:10.1103/physreva.101.063407. [VERIFIED Crossref]
- Wragg et al., "Double ionization in R-matrix theory using a two-electron outer region", PRA 92, 022504 (2015), doi:10.1103/physreva.92.022504. [VERIFIED Crossref]
- Plummer et al., "Double-continuum R-matrix theory and codes for many-electron atoms...", J. Phys. Conf. Ser. 1412, 132053 (2020), doi:10.1088/1742-6596/1412/13/132053. [VERIFIED Crossref]
- Jiang et al., "Semiclassical study of nonsequential triple ionization of Ar in strong laser fields", PRA 104, 023113 (2021), doi:10.1103/physreva.104.023113. [VERIFIED Crossref]
- Bauer, "TDDFT applied to nonsequential multiple ionization of Ne at 800 nm", Opt. Express 8, 377 (2001), doi:10.1364/oe.8.000377. [VERIFIED Crossref]
- RMT code, CPC (2020), doi:10.1016/j.cpc.2019.107062. [VERIFIED Crossref in discovery_amo.md]
- [UNVERIFIED] Berry et al. 2018 antisymmetrization; Li single-PI cross-section magnitude; Ar NS triple/single ratio; COLTRIMS triple-coincidence event counts; leadership-HPC GPU memory totals.
