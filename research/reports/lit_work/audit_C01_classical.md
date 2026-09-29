# Audit C01 (classical adversary): XRTS real-frequency S_ee(q,w) of partially degenerate WDM

Date: 2026-09-28. Role: classical adversary. Status: FINAL.
Verdict: **WOUNDED** (not killed). A single-family classical wall exists at a named state point, but the
information case (L5) is weak, the uniform-electron-gas part is classically covered, the quantum pipeline
has its own model floor (thermal-state preparation), and the resource bar S*G <~ 1e12 is missed by
roughly 3-5 orders of magnitude on a first estimate.

Numbers marked [ESTIMATE] are my own order-of-magnitude derivations from the cited inputs, not literature values.
Nothing here is cited from memory without verification unless marked [UNVERIFIED].

---

## 1. Strongest classical methods, with demonstrated reach

| Family | Demonstrated reach (verified) | Where it stops |
|---|---|---|
| Direct fermionic PIMC | UEG theta=1 and 0.75 feasible (2509.11317). Be, small N: average sign ~0.098 (2402.19113). | UEG theta=0.5: S=0.00359 at N=8; S~1e-6 expected at N=66 (2509.11317). Feasibility needs S >~ 1e-2..1e-3. |
| xi-extrapolation / Taylor-xi / xi-ensemble / reweighting (fictitious identical particles) | Be 7.5 g/cc, T=100-190 eV, rs=0.93, N_e=100, matched NIF XRTS ITCF (2402.19113). UEG N<=1000 static properties (2311.08098). Be N_e=40 at 155.5 and 190 eV (2607.06955). UEG N=28, 66 at rs=0.5, theta=1 (2607.06955). | "breaks down for moderate to high quantum degeneracy" (2308.06071); "original xi-extrapolation ... breaks down for Theta=0.5"; at theta=0.5 "none of the depicted polynomial degrees is sufficient" (2509.11317). |
| Analytic continuation of PIMC ITCF (stochastic dynamic-LFC sampling, MaxEnt with PIMC-built prior, PyLIT) | UEG S(q,w) from theta~1 WDM to rs=50-200 electron liquid (1810.12776; 2503.20433, PRB 112,125112 (2025); 2603.27212). Finite-size: reconstructed S(q,w) "not afflicted with any finite-size effects for as few as N=14 electrons" (2004.13429). | Inherits PIMC's sign wall; ill-posed at sharp features. |
| Static/effective-static LFC (ESA) + RPA dielectric | Static approximation gives "high-quality data for S(q,w) over substantial parts of the WDM regime" (1810.12776). ESA analytical LFC for 0.7<=rs<=20 (2101.05498; PRL 125,235001 (2020) per 2008.02165). | UEG only; dynamic xc effects at q~2 q_F and strong coupling (roton; 2203.12288, 2503.20433). |
| UEG thermodynamics across theta | Groth et al. PRL 119,135001 (2017) doi:10.1103/PhysRevLett.119.135001, combined CPIMC/PB-PIMC xc free energy. ph-FT-AFQMC for UEG agrees with parametrization better than restricted PIMC "in the regime of Theta<=0.5 and rs<=2" (2012.12228, Lee, Morales, Malone). | Neither demonstrates ITCF/dynamics for real materials at theta<0.5. |
| LR-TDDFT (Kohn-Sham, Liouville-Lanczos, noise-filtered) | Al and H validated vs PIMC ITCF (2502.04921, MRE 2025 doi:10.1063/5.0263947). 10x speedup via S<->ITCF mapping (2510.01875, npj Comput Mater 12,168 (2026)). H at rs=3.23 theta=1: S_ee(q) "in striking agreement with the PIMC baseline"; disagreement starts "at around thrice the Fermi wavenumber" (adiabatic kernel) (2507.00688, MRE 11,025401 (2026)). | Kernel is approximate (adiabatic PBE); no exact check below theta=1 in real H. |
| Mixed stochastic-deterministic TD-KS-DFT, TD-OF-DFT | DSF of Al, Be, compressed Be, CH (2410.23599; Electronic Structure 2025 doi:10.1088/2516-1075/adad24). | Same kernel issue; OF needs dynamic KE potential. |
| Real-time Wigner path-integral MC | Fermion DSF (Filinov, Levashov, Larkin, Mol Phys 2024/25 doi:10.1080/00268976.2024.2440477). | Not benchmarked at XRTS conditions in sources checked. |
| Chihara/average-atom (xDAVE) | Be ambient and compressed (2604.27237). | Model-form error (bound-free, continuum lowering); f-sum-rule violations in chemical models (2607.25481). |
| NEGF G1-G2 | Jellium stopping in quasi-1D (2302.06216); fluctuations/GW for dense plasmas (2402.05214). | No 3D UEG S(q,w) at WDM found. |
| Neural variational free energy | Dense hydrogen EOS, PRL 131,126501 (2023) (2209.06095). | Equilibrium only; no dynamics/ITCF. |

## 2. Where exactly classical computation fails (evidence)

Named wall (single-family). Moldabekov et al. 2507.00688 present hydrogen at rho=0.33 g/cc (rs=2),
T=6.27 eV (theta=0.5) and T=3.13 eV (theta=0.25), "at significantly lower temperatures, where PIMC is
unavailable due to the sign problem". Only adiabatic-PBE LR-TDDFT covers that point, and its adiabatic
kernel already deviates from PIMC S_ee(q) at q >~ 3 q_F at theta=1. So the wall is **real-material
H (and by extension CH, Be at lower T), rs~2-4, theta<=0.5, N_e>=~32**. The UEG version of the wall is
much weaker: ground-state QMC plus PIMC at theta>=0.5 bracket the static LFC, and AFQMC covers
theta<=0.5 at rs<=2 for energies.

Sign threshold (audit Q2). Quoted data: UEG theta=0.5, N=8: S=3.6e-3; N=66: S~1e-6 expected
(2509.11317). The 1e-4 line for UEG therefore lies between N=8 and N=66 at theta=0.5, roughly
N~20-40 [ESTIMATE; conditions differ between the two quoted numbers]. Taylor-xi and xi-ensemble have not
been shown to reach theta=0.5 reliably. The literature says they break down there. Inhomogeneous H/Be
will be worse than the UEG at equal theta.

Multi-family check (audit Q3). I found no paper that computes S_ee(q,w) at a theta<=0.5 state point with
two independent ab initio families and reports disagreement beyond experimental error. The wall is
"single-family" (TDDFT only), and lesson 5 says single-family convergence is not convergence. That cuts
both ways. Hardness is not established by disagreement, and correctness is not established by agreement.

## 3. Decision relevance and information (L5, audit Q1)

- **Current NIF XRTS sits where PIMC works.** For Be at 7.5 g/cc and 155.5 eV, rs=0.93, theta ~2.7
  [ESTIMATE: E_F = 50.1/rs^2 eV = 58 eV]. PIMC matched NIF ITCF, S(q) and elastic/inelastic ratio.
  The authors state "deconvolution to extract S_ee(q,w) is unstable" and work in the Laplace domain
  (2402.19113).
- **Laplace-domain equivalence.** L[S (x) R] = L[S] * L[R]. Where exact PIMC F(q,tau) exists, an exact
  real-frequency S carries no extra information about the measured spectrum beyond regularizing the
  continuation. Real-frequency S adds information only where (a) PIMC cannot reach, or (b) the
  instrument resolves features narrower than ~T. For (b), ~0.1 eV XFEL resolution exists
  (Gawne et al. PRB 109, L241112 (2024), arXiv:2403.02776), but it was demonstrated on ambient Al,
  where TDDFT resolved earlier disagreements.
- **The sub-0.5 theta decision already made without real-frequency S.** Double-cone-ignition plasma
  jets: T=25 eV, 8+/-2 g/cc, gold fraction 0.162+/-0.015 %, diagnosed with the ITCF method plus
  first-principles input (2504.04317). theta ~0.45, rs ~0.95 [ESTIMATE, assuming CH with Zbar~2.5].
- **Inference is noise- and model-limited, not solver-limited.** Hentschel, Kononov, Baczewski, Hansen
  (2408.15346) studied Al at 1 eV (theta<<1) with 10% noise. Even noise-free synthetic data leave
  "factor-of-three variations in the DC limit" of the collision frequency. The two-angle posterior on
  sigma_DC spans "a factor of 22". "There are often many distinct choices for nu(w) that produce an ELF
  consistent with the reference data." A more exact forward S does not narrow a posterior that the data
  cannot constrain.
- **Model-free ITCF review.** Gawne et al. 2026 (2604.25735; Rev Mod Plasma Phys doi:10.1007/s41614-026-00227-9)
  give T, normalization and Rayleigh weight without a model. Nat Commun 13,7911 (2022)
  doi:10.1038/s41467-022-35578-7 covers ITCF thermometry, and Sci Rep (2024) doi:10.1038/s41598-024-64182-6
  covers the f-sum-rule normalization.
- **Judgement.** For (rho, T) the gain of real-frequency S over the model-free ITCF is likely <2x at
  NIF resolution and noise [ESTIMATE, untested]. Possible >2x cases: Zbar/ionization and bound-free
  shape in partially ionized H/CH at theta<=0.5, and meV-resolution plasmon damping. Neither has been
  shown.

## 4. The quantum pipeline's own model floor (L6) and resources (audit Q4, Q5)

- **Thermal state.** Rubin et al. (2308.12352, PNAS 2024) prepare Slater determinants sampled from
  Mermin-Kohn-Sham occupations. They state "preparing the thermal ensemble on the electronic subsystem is
  believed to be exponentially hard for generic local Hamiltonians, even on a quantum computer."
  For S_ee this is fatal if reused as is. A determinant initial ensemble gives a mean-field
  S(q)=F(q,0), which is the correlation physics PIMC shows is decisive (2402.19113 title). The quantum
  answer would then carry an initial-state error of the same type as the TDDFT kernel error it is meant
  to remove. A correlated Gibbs state (QPE filtering, TPQ, detailed-balance samplers) has no
  demonstrated polynomial mixing or success probability for 3D Coulomb continua at theta<0.5
  [open; not found in sources checked].
- **Cost anchor.** Rubin: eta=32-128, N~1e6-1e7 plane waves, ~1e3 logical qubits, **1e15-1e17 Toffoli
  total**, t~50-100 a.u. Su et al. PRX Quantum 2, 040332 (2021) (2105.12767): O~(eta^{8/3} N^{1/3} t).
- **S(q,w) estimate [ESTIMATE].** Resolution dE=1 eV needs t~27 a.u.; dE=5 eV needs ~5.5 a.u. The
  lower cutoff with no fast projectile helps only as N^{1/3}. G per correlator sample ~1e9-1e11 Toffoli.
  Samples S >= (time points or QPE shots ~1e2-1e4) x (1/eps^2 ~1e4 at 1%) x (ion snapshots ~10), so
  1e5-1e7. **S*G ~1e14-1e18, which fails the 1e12 bar by 2-6 orders**, before any correlated
  thermal-state preparation cost.
- **q-resolution (Q5).** For N=128 at rs=2, L=16.2 bohr and q_min=0.39 bohr^-1 ~0.4 q_F [ESTIMATE].
  Large-angle NIF geometries (q=5.55 1/A = 2.9 bohr^-1, 2402.19113) are fine. Small-angle collective
  geometries are marginal. Classical PIMC shows no finite-size effect in S(q,w) at N=14 (2004.13429),
  so finite N is not a quantum-specific edge.

## 5. Scoop risk (audit Q6)
High. The Sandia group (Baczewski, Kononov) combines XRTS-TDDFT expertise (2408.15346; Kononov
Phys Plasmas 2024 doi:10.1063/5.0198008), quantum stopping power (2308.12352), a quantum opacity protocol
with momentum-resolved photon measurement (2607.02811; XRTS is inelastic photon scattering in the same
framework) and quantum conductivity (OSTI 10.2172/3363975). LLNL is active on PIMC sign-problem work
for Be (OSTI 10.2172/3389315, Boehme 2026; OSTI 10.2172/3662053, Dornheim SCCS 2026). No quantum
S_ee(q,w)/XRTS paper found in the arXiv API query below. Quantum DSF exists only for spin models
(2607.07138 trapped-ion pumping; 2603.15608 superconducting vs neutron data). The roadmap 2605.07722 names
WDM/ICF microphysics as a quantum target without naming the DSF in its abstract.

## 6. Cheapest decisive classical kill experiment
**K-C01a (laptop, days).** Use the UEG at rs in {2, 3, 4} and theta in {0.25, 0.5, 1}.
1. Build forward models: RPA, ESA static LFC (2101.05498), and a dynamic-LFC envelope bounded by
   PIMC+MaxEnt/PyLIT spectra at theta>=0.5 (2503.20433, 2603.27212).
2. Convolve each with NIF-like (5-20 eV FWHM) and XFEL-like (0.1-1 eV) instrument functions, with
   5-10% noise.
3. Run MCMC/Fisher for (n_e, T) using (a) the full real-frequency forward model and (b) the model-free
   ITCF analysis.

Kill if two conditions both hold at every XRTS-relevant q: the forward-model spread (ESA vs dynamic
envelope) shifts the posterior by less than 0.5 sigma, and the full-S posterior is less than 2x narrower
than the ITCF posterior.

**K-C01b (~1e4 core-h).** Hydrogen at rs=2, theta=0.5 and 0.25, the named wall from 2507.00688.
1. Run LR-TDDFT with ALDA, PBE, a hybrid or AGGA kernel, and a PIMC-derived static kernel, plus Chihara
   average-atom.
2. Run a xi/Taylor-xi PIMC attempt at N_e=14-32 to measure the actual sign and extrapolation error.

Kill if the kernel and family spread of S_ee(q,w) convolved with the instrument function is below
experimental error bars. Survive (escalate to the quantum-side audit) if the spread exceeds error bars
where the xi methods verifiably fail.

## 7. Verdict rationale
- Not killed. At H rs=2, theta<=0.5, PIMC is explicitly unavailable, and only an approximate-kernel
  TDDFT family remains. No paper shows that family is converged there.
- Wounded, for five reasons:
  1. The UEG core is covered (ESA and AC for N>=14; AFQMC at theta<=0.5, rs<=2).
  2. Deployed experiments sit at theta>1 (NIF Be) or were decided model-free (DCI jets, theta~0.45).
  3. XRTS inference is information-limited: 2408.15346 finds factor-3 to factor-22 degeneracy even
     noise-free.
  4. The quantum protocol inherits a mean-field thermal-state model floor unless a correlated Gibbs
     preparation is solved.
  5. S*G misses 1e12 by several orders.
- The candidate's only defensible form is narrow: correlated S_ee(q,w) for partially ionized H/CH at
  rs 2-4, theta 0.25-0.5, and only if K-C01b shows multi-family disagreement beyond error bars.

---

## Citations verified this session (arXiv abs/html, Crossref or OSTI record)
2402.19113; 2509.11317; 2308.06071; 2311.08098; 2508.12323; 2502.15288 (listing); 2607.06955; 2206.08341 (listing);
2004.13429; 2604.25735 (+doi:10.1007/s41614-026-00227-9); 2504.04317; 2503.20433; 2603.27212; 2502.04921
(+doi:10.1063/5.0263947); 2510.01875; 2410.23599 (+doi:10.1088/2516-1075/adad24); 2507.00688; 1810.12776;
2008.02165; 2101.05498 (listing); 2012.12228; 2209.06095; 2408.15346; 2403.02776; 2308.12352; 2105.12767;
2607.02811; 2605.07722; 2607.07138; 2603.15608 (listing); 2302.06216; 2402.05214; 2604.27237 (listing);
2607.25481 (listing); 2203.12288 (listing); doi:10.1080/00268976.2024.2440477; doi:10.1103/PhysRevLett.119.135001;
doi:10.1038/s41467-022-35578-7; doi:10.1038/s41598-024-64182-6; doi:10.1063/5.0139560; doi:10.1063/5.0198008;
OSTI 10.2172/3389315; OSTI 10.2172/3662053; doi:10.1038/s42254-025-00893-7 (Kraus, Nat Rev Phys 2025, listing only).
Not re-verified here: OSTI 10.2172/3363975 (cited from the brief).

## Query log
- WebSearch: budget exhausted (200/200), so no results.
- arXiv API: all:"dynamic structure factor" AND all:"warm dense" (30 results).
- arXiv API: all:"fictitious identical particles" (11).
- arXiv API: abs:"imaginary-time" AND abs:"warm dense" (18).
- arXiv API: au:Dornheim_T returned HTTP 429. OpenAlex search returned HTTP 429.
- arXiv API: au:Moldabekov AND abs:hydrogen (21).
- arXiv API: abs:"auxiliary-field" AND abs:"electron gas" AND abs:temperature (2).
- arXiv API: abs:"quantum computer" AND (warm dense OR Thomson scattering OR dynamic structure factor) (6).
- arXiv API: abs:"G1-G2" AND (electron gas OR dense plasma OR warm dense) (3).
- arXiv API: ti:"Ultrahigh resolution x-ray Thomson scattering" (1).
- Crossref: WDM DSF TDDFT PIMC 2024+ (30).
- Crossref: warm dense hydrogen PIMC fermion sign low temperature 2023+ (29).
- Crossref: XRTS temperature diagnostics imaginary time ultrahigh resolution free-bound 2022+ (15).
- Crossref bibliographic: Nat Commun 13, 7911; Groth PRL 119, 135001.
- Crossref: XRTS warm dense hydrogen e-i relaxation XFEL 2018+ (10).
- Crossref DOI records: 10.2172/3662053, 10.1080/00268976.2024.2440477.
- OSTI: biblio/3389315, biblio/3662053.
- arXiv abs/html fetches: 2402.19113 (abs+html), 2509.11317 (abs+html), 2604.25735, 2311.08098, 2308.06071, 2508.12323,
  2503.20433, 2603.27212, 2502.04921, 2004.13429, 2504.04317, 2510.01875, 2410.23599, 2607.06955 (abs+html),
  2211.00579, 2308.12352 (abs+html), 2105.12767, 2507.00688 (abs+html), 2607.25481 (classifier error, not read),
  2408.15346 (abs+html), 2209.06095, 2008.02165, 1810.12776, 2403.01979, 2605.07722, 2607.02811.
