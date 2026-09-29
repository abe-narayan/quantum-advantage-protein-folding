# Audit N01: novelty / prior-art auditor

**Date:** 2026-09-28. **Role:** novelty / prior-art auditor (round 2).

**Candidate N01.** The ground-state competition between FCI, CDW and AHC in hBN-aligned rhombohedral multilayer graphene at fractional filling, with explicit remote bands. The method is QPE/QCELS eigenvalues in the explicit multi-band momentum-space Hamiltonian, at N_k = 27-36 and n_b = 3-5.

**Verdict: WOUNDED.** The novelty class is **B** on the quantum side: nearby work exists, but not on this problem. No exact prior comparison exists, so this is not a kill on novelty. There are, however, four material wounds to the framing. Three came out of the literature, and one, the classical scoop risk, is a forecast.
1. 2608.12452 has already answered the primary yes/no ("yes", at the ED scale).
2. Experiments put the T→0 state at nu ≈ 2/3 in several devices in an extended-QAH / AHC regime, with the FCI appearing at finite T or B. That moves part of the decision off the ground-state eigenvalue question.
3. Experiments are mapping the alignment and twist windows directly.
4. Multi-band NQS (NTB) and multi-band iDMRG are established in the adjacent tMoTe2 system and have not yet been applied here. That is a near-term classical scoop risk.

Scope of the searches: listed in the query log below, through 2026-09-28. OpenAlex and Semantic Scholar were rate-limited (HTTP 429) for this whole audit, so cited-by was replaced by arXiv abstract-term searches, an author search, and a search for the 2608.12452 key phrase.

---

## 1. EXACT PRIOR WORK

No paper was found that does any of the following:
- estimates fault-tolerant cost (lambda, Toffoli/T count, logical qubits) for a moire / FCI / FQH / Landau-level interacting Hamiltonian;
- estimates FT cost for the multi-band momentum-space continuum model of rhombohedral graphene/hBN;
- compares QPE/QCELS against multi-band ED, iDMRG or NQS on that problem.

The scientific question itself does have direct prior work. For each paper: what it did, and what it leaves open.

**Yu, Herzog-Arbeitman, Kwan, Regnault, Bernevig, arXiv:2407.13770, PRB 112, 075110 (2025).**
- Did: multi-band ED on R5G/hBN. Single-band FCIs "are destroyed by band mixing, becoming gapless as fluctuations are included". nu = 2/3 was not converged.
- Open: the treatment has no moire capacitor term.

**Li, Bernevig, Regnault, arXiv:2504.20140, PRB 112, 075130 (2025).**
- Did: multi-band ED plus an iteration approach that optimizes the single-particle basis. nu = 1/3 (CN scheme) is unstable to a CDW; nu = 2/3 is more robust. The iteration approach "still failed to preserve the FCI gap".
- Open: the same as above.

**Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, arXiv:2608.12452 (12 Aug 2026).** This is the closest work, and it has already answered the candidate's PRIMARY output.
- Did (read from the abstract and the HTML full text): the "moire capacitor effect" electrostatically imprints the valence charge onto the conduction bands.
  - "We then perform multi-band exact diagonalization calculations to confirm the emergence of FCIs at nu = 2/3".
  - "Our FCI state is stabilized by inter-band fluctuations, unlike in the moire-free case which collapses with band-mixing."
- Sizes: 21 sites only, with band-occupation caps ("bandmax", n2, n3 <= 6; truncations labelled 14,2 / 14,5 / 17,5) and Hilbert spaces up to about 1e9.
  - "Full 3-band ED is challenging because of the large Hilbert space dimension ~1e12 on 21 sites."
  - "While we are unable to access larger systems, Fig. 4(c) points to the existence of a converged multi-band FCI."
  - The gap is about 0.1-0.3 meV, depending on the truncation.
- Scope: R5G at theta = 0.77° with one D polarity; L = 4, 5, 6 are mentioned for the Jain sequence.
- Other fillings "appear demanding" ("a correct treatment of fluctuations due to band-mixing appears demanding").
- n2 = n3 = 0 (no band mixing, with the capacitor term, per my HTML read; confirm in the PDF) gives a CDW, not an FCI. So at 21 sites a one-body-only single-band ablation fails. That is prima facie evidence against the "(a) one-body" arm of G0.
- No DMRG, NQS or quantum-computing content.
- Open: N_k > 21; untruncated n_b = 3; nu = 3/5 and 2/5; FCI vs AHC energetics; the parameter prior; second-order (not one-body) ablations.

**Consequence for N01.**
- Primary output 1 as written ("does the model support a gapped FCI at 2/3 anywhere in the prior?") is no longer open at the ED scale. It is answered "yes" by 2608.12452, for 21 sites with occupation truncation.
- What remains open is narrower:
  - (i) Is the 2608.12452 FCI converged in N_k (27, 36) and in untruncated n_b?
  - (ii) Do nu = 3/5 and 2/5 (the Jain sequence) survive explicit band mixing with the capacitor term?
  - (iii) What is E_FCI - E_AHC/EQAH in the same model?
- The candidate must be re-scoped to (i)-(iii) to stay non-cosmetic.

## 2. NEAREST QUANTUM WORK (all verified on arXiv abs or listing pages)

**FQH / FCI on quantum computers.** All of these are single-Landau-level or thin-torus/sphere models, NISQ-type state preparation, variational methods or dynamics. None is multi-band, none is moire, and none has an FT cost:
- Rahmani et al., arXiv:2005.02399: Laughlin nu = 1/3 in linear depth, thin torus.
- Kirmani et al., arXiv:2303.04806: FQH quasihole braiding on a superconducting processor.
- Chu et al., arXiv:2304.13748: MERA-type circuits for chiral topological order.
- Kobayashi et al., arXiv:2303.04822: higher central charge from a single wavefunction, on a QC.
- Shen et al., arXiv:2503.13294: fermionic Laughlin state on IonQ Aria-1, HVA.
- Kirmani et al., arXiv:2512.09982: Hall viscosity of Laughlin on noisy QCs.
- Wu et al., arXiv:2606.16548: FQH state preparation on QCs, sphere.
- Liu et al., arXiv:2606.23451: dissipative preparation of Laughlin-like states.
- Exposito, Aseginolaza, Guerrero-Aviles, Jornet-Somoza, Guinea, Borge, arXiv:2607.11380: VQE/VQD for nu = 1/3 FQH manifolds, sphere and torus. The abstract says it "provides a route toward quantum simulations of fractional Chern insulators". It has no band mixing and no FT cost.
- Xu et al., arXiv:2608.05140: constant-depth preparation of clustered non-Abelian FQH states on IBM Heron, up to 154 qubits.

**Moire on quantum computers.**
- Bai et al., arXiv:2510.09999: random-state modified QPE for the single-particle DOS of graphene and TBG quasicrystals. It is non-interacting.

**FT costing for periodic solids in a Bloch/k-point basis.** This is the template and the source of any scoop.
- Rubin et al., arXiv:2302.05531, PRX Quantum 4, 040303 (2023): Bloch-orbital SF/DF/THC qubitization.
- Bhardwaj, Munoz, Jones et al., arXiv:2604.12142 (Apr 2026): Bloch-UPAW; Toffoli O(N_k^3); "approximately an order-of-magnitude reduction" vs prior periodic-solid work.
- Bhardwaj, Munoz, Jones et al., arXiv:2606.27734 (Jun 2026): FT static structure factor and finite-size effects, with an O((N_b N_k)^3) block-encoding cost.
- None of the three treats a moire, flat-band, Landau-level or projected continuum Hamiltonian.

**Algorithm.**
- Ding & Lin, arXiv:2211.11973, PRX Quantum 4, 020331 (2023): QCELS. Verified through Crossref (DOI 10.1103/prxquantum.4.020331).

**Classification of the quantum side.**
- FQH family: category C (quantum methods exist, no advantage study).
- This multi-band moire problem: category B (nearby, but not this problem).
- No D or E item (a claimed advantage, or a dequantization) was found.

## 3. NEAREST CLASSICAL WORK (the competitor landscape, verified)

**Multi-band ED, rhombohedral graphene.** 2407.13770, 2504.20140 and 2608.12452 (all Bernevig/Regnault/Herzog-Arbeitman/Kwan/Li/Yu).

**Multi-band ED, tMoTe2 (the adjacent system).**
- Li, Yu, Xu, Bernevig, Regnault, arXiv:2608.23675 (Aug 2026): large-scale one-band vs two-band-per-valley ED; "agreements and contradictions with current experiments".
- Kwan et al., arXiv:2407.02560.
- Morales-Duran, Shi, Voinea, Potasz, Cano, arXiv:2604.16847 (Apr 2026): band mixing destabilizes the 1/3 FCI more strongly than the 2/3 FCI (FCI vs electron and hole Wigner crystals).

**Multi-band NQS.**
- Zhang & Luo, arXiv:2509.09275, "Neural Transformer Backflow", tMoTe2. It is momentum-resolved in a "multi-band projection formalism", and "scales efficiently to larger sizes and higher-band truncations far beyond the reach of exact diagonalization". It gives degeneracies and gaps. It has not been applied to R5G/hBN (no mention found).
- Luo, Zaklama, Fu, arXiv:2503.13585: NQS for tMoTe2 with "strong moire band mixing".
- Abouelkomsan, Geier, Fu, arXiv:2512.01863: attention NN wavefunction discovers FCI ground states.
- Zhang, Jiang, Luo, arXiv:2608.14208 (Aug 2026): foundation neural effective Hamiltonian for moire materials. Title and listing only.

**Rhombohedral-graphene NN-VMC and VMC.** None of these is multi-band with an hBN moire potential.
- Abouelkomsan, Gaggioli, Guerci, Fu, arXiv:2608.00167 (Jul 2026): NN-VMC with a single effective conduction dispersion; no hBN moire potential; N = 25; crystals only.
- Desrochers & Vishwanath, arXiv:2607.08822 (Jul 2026): variational MC energetics of fractional AHCs; moireless.
- Kim, Timmel, Wen, arXiv:2507.18582: listing only.

**DMRG.**
- Wang & Zaletel, arXiv:2507.07921: lowest-Landau-level plus periodic potential; FCI vs chiral SC vs CDW, within 1%.
- He, Simon, Parameswaran, arXiv:2505.06354: iDMRG on a tMoTe2 lattice model; "mixing with higher bands" destabilizes FCIs (per the arXiv API abstract). Multi-band iDMRG is therefore an existing technique in the adjacent system.

**Multiband variational theory, R-graphene.**
- May-Mann, Tan, Ledwith, Shi, Devakul, arXiv:2608.14535 (Aug 2026): the "skyrmion FCI", an "intrinsically multiband route" at nu = 2/3, "absent in single Chern band-projected studies". This is a competing mechanism to 2608.12452, which is what makes a large unbiased multi-band calculation scientifically discriminating.

**HF, single-band ED and TDHF.**
- Dong/Patri/Senthil: 2311.03445, 2403.07873.
- Zhou/Yang/Zhang: 2311.04217.
- Dong et al., AHC I: 2311.05568.
- Soejima et al., AHC II: 2403.05522.
- Huang/Li/Das Sarma: 2407.08661, 2408.05139.
- Kwan et al., Moire FCI III: 2312.11617, on scheme dependence.

**FQH analogue of the G0 ablation.**
- Perturbative Landau-level mixing (three-body pseudopotentials) is textbook in FQH, for example Crossref 10.1103/physrevb.87.245425 and 10.1103/physrevlett.113.086401.
- Its moire transfer (Schrieffer-Wolff / three-body terms for the 2608.12452 Hamiltonian) was not found in the band-mixing searches. It is an untested, cheap classical ablation.

## 4. TESTED

- Multi-band ED, R5G/hBN, <= 21 sites with occupation caps: FCI collapse without the capacitor term (2407.13770, 2504.20140); nu = 2/3 FCI with the capacitor term (2608.12452).
- The one-body-only single-band arm (n2 = n3 = 0) with the capacitor term gives a CDW at 21 sites (2608.12452). The effect of band mixing is therefore not reproduced by the one-body imprint alone at that size.
- Multi-band NQS and iDMRG in tMoTe2 (2509.09275, 2503.13585, 2505.06354).
- HF, TDHF and single-band ED phase diagrams for R4G-R7G (many papers).
- The experimental map (section 7).
- FQH state preparation and VQE on NISQ hardware (single Landau level).
- FT Bloch-orbital costing for ordinary solids.

## 5. NOT TESTED (within the searched scope)

- Any FT resource estimate (lambda, C_W, logical qubits, S*G) for the moire-continuum or FCI Hamiltonian, in DF, THC or BLISS form.
- Multi-band ED or any unbiased method at N_k >= 24-27 with untruncated n_b = 3, with the capacitor term.
- nu = 3/5 and 2/5 with explicit band mixing plus the capacitor term.
- Multi-band NQS (NTB-type) or multi-band iDMRG on R5G/hBN.
- Second-order (Schrieffer-Wolff / three-body) renormalized single-band ED for R-graphene/hBN with the capacitor term.
- FCI vs AHC/EQAH energetics in the multi-band plus capacitor model on commensurate supercells.
- Parameter-prior propagation (V1 of 5-21 meV per 2608.12452, eps_r, gamma_i, relaxation) through multi-band ED.

## 6. WHY THE GAP IS MATERIAL (and where it is weak)

**Material.**
- The one controlled calculation that produces the observed FCI (2608.12452) says its result comes from inter-band fluctuations, and states it cannot access larger systems. Convergence in N_k and in n_b is therefore the open scientific question, and it lies in exactly the Hilbert-space range (1e12 at 21 sites for n_b = 3; 1.7e16 at 27) where ED stops.
- Two competing multiband mechanisms (capacitor + band-mixing FCI, and skyrmion FCI) and moireless fractional AHCs are all on the table as of Jul-Aug 2026. An unbiased large-N_k multi-band eigenvalue calculation would discriminate among them.
- On the quantum side, no one has costed this Hamiltonian class. The chemistry and solids FT literature does not transfer trivially:
  - the form factors are band-projected;
  - the interaction is screened and long-range;
  - there are quasi-degenerate torus multiplets and flux insertion.

**Weak points (the wounds).**
- (W1) The primary yes/no is already answered ("yes" at the ED scale). The residual question is convergence, which is a weaker decision variable: it confirms or refutes a published claim rather than enabling a new design decision.
- (W2) The experiments indicate the T→0 state near nu = 2/3 is not simply an FCI:
  - Lu et al., 2408.10203: EQAH at low T and small current; FQAH is recovered at higher T or current.
  - Waters et al., 2408.10133 (PRX 15, 011045 (2025)): electronic crystals at B = 0; FCI near 2/3 only in a "modest magnetic field".
  - Li et al., 2607.08710: an FCI → "generalized anomalous Hall crystal" transition at about 150 mK.
  - Kim & Kivelson, 2609.16483: T = 0 is an extended integer QAH with Wigner-crystal order, and the FQAH regime is entropy-driven.

  The decision-relevant quantity may therefore be a finite-T free-energy competition, possibly with incommensurate crystals, not a T = 0 torus eigenvalue at commensurate N_k. That is round-1 lesson (i) again: the wall (ground-state eigenvalues at large N_k) and the decision (the finite-T phase observed in devices) may sit in different regimes. Incommensurate EQAH/AHC over nu = 0.5-1.3 is also poorly represented on a fixed small torus.
- (W3) Alignment and twist windows are being measured directly:
  - Huo et al., 2510.15309: integer CI needs theta < 1.1°, the FCI a smaller angle; ED with fluctuations is compared, and mean-field fails.
  - Li et al., 2505.01767: orientation matters in the moire-proximal regime.
  - Uzan et al., 2507.20647: 0° vs 180° gives different moire strength.
  - Pan et al., 2608.24684: FQAHE is absent below a moire period of about 10 nm.

  Built-device decisions are therefore their own oracle. Decision value is left only in unbuilt stacks (R7G+, double alignment, other substrates).
- (W4) Classical scoop risk is high:
  - NTB-type multi-band NQS and multi-band iDMRG are established in tMoTe2 and can be transferred directly.
  - The Bernevig/Regnault group publishes a multi-band ED paper every few months (2407.13770 → 2504.20140 → 2608.12452 → 2608.23675).

  If a multi-band NQS result on R5G/hBN at N_k >= 27 appears and agrees with 2608.12452, then G2 closes the wall classically and the claim drops to category 1 at most.

## 7. EXPERIMENTAL "GROUP-TO-GROUP DISAGREEMENT" ITEMS (verified; replaces the [recalled] items in the prefilter)

| Paper | Group | Finding |
|---|---|---|
| Lu et al., 2309.17436 | MIT, Ju | Zero-field FQAH at 2/3, 3/5, 4/7, 4/9, 3/7, 2/5 in R5G/hBN |
| Lu et al., 2408.10203 | Ju | EQAH (Rxy = h/e^2 for nu 0.5-1.3) at lower T and current; FQAH recovered by raising T or current |
| Waters et al., 2408.10133, PRX 15, 011045 (2025) | Yankowitz/Folk | Electronic crystals at B = 0; FCI near 2/3 only under modest B |
| Aronson et al., 2408.11220 | Ju | Moire-proximal FCIs at 1, 2/3, 1/3 controlled by D |
| Xie et al., 2405.16944 | X. Lu | R6G/hBN FCI at 2/3 |
| Choi et al., 2408.12584 | Young | R4G FCI at 2/3 |
| Huo et al., 2510.15309 | X. Lu + Bernevig/Regnault | Critical twist angle; FCI needs smaller theta than the integer CI |
| Li et al., 2607.08710 | Mak/Shan with Ju | FCI → generalized AHC below about 150 mK |
| Hadjri et al., 2609.09422 | [group not read] | Zero-field fractional QAH insulators; D-driven transitions (listing only) |

**Conclusion on the recalled item.** The "zero-field vs finite-field FCI" disagreement is VERIFIED: Lu 2309.17436 vs Waters 2408.10133. The "extended QAH at low T" item is VERIFIED: 2408.10203 and 2607.08710.

## 8. WHY IT COULD BE A NEW PAPER

This paper does not yet exist:
- the first FT resource estimate (lambda, Toffoli count, logical qubits, S*G) for the explicit multi-band moire continuum Hamiltonian, i.e. the 2608.12452 model;
- with QCELS for quasi-degenerate torus multiplets and flux insertion;
- benchmarked against multi-band ED at <= 21 sites;
- with an explicit crossover analysis against multi-band NQS and iDMRG.

It would also be the first moire / FCI entry in the Bloch-orbital FT costing line (2302.05531, 2604.12142, 2606.27734). The tightest non-cosmetic scientific target is the N_k/n_b convergence of the 2608.12452 nu = 2/3 FCI, plus 3/5 and 2/5 under the same model.

This is a category-3 resource study against exact ED, and category 1 against NQS/iDMRG unless those fail at a named point. Nothing stronger is supported.

## 9. SCOPED NEGATIVE STATEMENT

As of 2026-09-28, the arXiv API searches (queries 1-9, 11, 13-22 below) and the Crossref searches (queries 23-24) found no fault-tolerant resource estimate, QPE/QCELS study, or quantum-advantage study for any interacting moire, FCI, FQH or Landau-level Hamiltonian, and in particular none for the multi-band rhombohedral graphene/hBN continuum model. The only quantum work in the family consists of:
- NISQ state preparation, variational methods or dynamics for single-Landau-level FQH (the list in section 2);
- non-interacting DOS by modified QPE for TBG (2510.09999).

Cited-by through OpenAlex and Semantic Scholar could not be run (HTTP 429). Citing works of 2407.13770, 2503.13585 and 2608.12452 were therefore checked only through arXiv term and author searches. This is a residual blind spot.

## 10. IMPLICATIONS FOR GATES (novelty-side input only)

- **G0.** 2608.12452 already shows at 21 sites that the one-body-imprint-only single-band arm gives a CDW, not an FCI. So the one-body arm of G0 likely fails, which favours the candidate. The second-order (three-body / Schrieffer-Wolff) arm is untested and must still be run.
- **G2.** The key competitor is transferring NTB (2509.09275) to R5G/hBN. That is a direct classical scoop path; monitor it.
- **G4.** Built-device alignment and twist decisions are measured (section 7). Restrict decision value to unbuilt stacks, or to discriminating between the capacitor mechanism and the skyrmion-FCI mechanism.
- **New risk, for the orchestrator.** If the experimental T→0 state is EQAH/AHC and the FCI is entropy-stabilized (2408.10203, 2607.08710, 2609.16483), the ground-state eigenvalue output does not by itself decide the observed phase. A finite-T free energy returns the Gibbs cost the candidate was built to avoid. The resource auditor and the classical auditor should decide whether the decision set is still eigenvalue-only.
- **Correlation length / N_k.**
  - 2608.12452 gives no N_k scaling beyond 21.
  - 2407.13770 states that current models "do not support FCIs with correlation length small enough to be converged in accessible, unbiased ED calculations, or do not support FCIs at all" (as quoted in the round-2 lens; the abstract page confirms the collapse claim).
  - The N_k actually required is unknown from the literature. This is not resolved here.
- **Moireless AHC limit.** It is not settled as the explanation of the aligned-sample FCIs. Experiments (2510.15309, 2608.24684, 2608.12478) and 2608.12452 all indicate that the moire potential is necessary for the FCI in aligned R5G/R6G. Moireless fractional AHCs remain energetically "competitive" (2607.08822). Alignment is therefore not moot.

---

## Query log (in order)
1. arXiv API `abs:"fractional Chern" AND abs:"band mixing"` (sorted by date, 40). Hits: 2608.23675, 2608.12452, 2604.16847, 2603.17006, 2506.05330, 2504.20140, 2407.13770, 2407.02560, 2311.15246, 1305.6948.
2. arXiv API `(FQH | "fractional Chern" | "Landau level" | moire) AND ("phase estimation" | "fault-tolerant" | qubitization | "resource estimate")` (40). No FT resource estimate for an interacting FQH/FCI/moire Hamiltonian. The hits are topological-qubit and anyon papers, plus state preparation (2608.05140, 2606.16548).
3. arXiv API `("quantum Hall" | "Chern band" | "flat band" | "twisted bilayer") AND ("quantum phase estimation" | VQE | Toffoli | "block encoding")` (40). Only 2607.11380 and 2510.09999.
4. arXiv API `(Laughlin | FQH | "fractional Chern") AND ("quantum computer" | "quantum circuit" | "quantum algorithm" | "quantum processor")` (50). The FQH circuit line in section 2.
5. arXiv API `(moire | TBG | "rhombohedral graphene" | MoTe2) AND ("quantum computers" | "quantum computing" | "quantum advantage" | "logical qubits")` (40). 2510.09999 and the review 2606.02721.
6. arXiv API `rhombohedral AND ("fractional Chern" | "fractional quantum anomalous" | "anomalous Hall crystal")`, 2 pages (about 65 entries, 2023-09 to 2026-09-25).
7. arXiv abs 2608.12452, plus the HTML full text (two targeted passes).
8. arXiv abs 2608.23675 and 2604.16847.
9. arXiv API `(neural | DMRG | "tensor network" | "Monte Carlo" | variational) AND (pentalayer | rhombohedral | "fractional Chern") AND ("band mixing" | multi-band | multiband | "remote bands" | "Landau level mixing")`. Hits: 2608.14535 and 2509.09275.
10. OpenAlex (two queries): HTTP 429, Retry-After 76291 s. Semantic Scholar citations for arXiv:2407.13770: HTTP 429 (WebFetch and curl).
11. arXiv API `(THC | DF | qubitization | "fault-tolerant quantum simulation") AND (Bloch | periodic | "momentum space" | k-point | materials | 2D)`. The OR grouping broke and returned irrelevant results. Discarded.
12. arXiv API `(THC | DF | qubitization) AND ("Bloch orbitals" | ...)`. Also broken or irrelevant. Discarded.
13. arXiv API `abs:"Bloch orbitals" AND abs:"fault-tolerant"`. Hits: 2606.27734 and 2604.12142.
14. arXiv API `("fractional Chern" | "Chern insulator" | TBG | moire) AND ("quantum simulation" | "Hamiltonian simulation" | "digital quantum" | "quantum eigensolver")`. Only 2607.11380 is digital; the rest are analog simulators.
15. arXiv abs 2607.11380 and 2608.14535.
16. arXiv abs 2607.08822, 2505.01767 and 2510.15309.
17. arXiv API `(pentalayer | hexalayer | tetralayer | heptalayer) AND graphene AND fractional AND (hBN | moire)`: the experimental list.
18. arXiv abs 2408.10133, 2408.10203, 2607.08710, 2609.16483 and 2407.13770.
19. arXiv abs 2509.09275. arXiv API `(neural quantum state | neural network | transformer | self-attention) AND ("fractional Chern" | FQAH | moire)` (40).
20. arXiv abs 2512.01863 and 2608.00167, plus the 2608.00167 HTML. arXiv API `(neural | VMC | DMRG) AND (rhombohedral | pentalayer | R5G)`.
21. arXiv abs 2504.20140, 2503.13585 and 2507.07921.
22. arXiv API `au:Regnault AND au:Bernevig` (20, a scoop watch). arXiv API `"moire capacitor"`: only 2608.12452, so no citing follow-up yet.
23. Crossref `fault-tolerant quantum phase estimation fractional Chern insulator moire` (20). No quantum-algorithm FCI item.
24. Crossref `quantum algorithm resource estimation fractional quantum Hall Landau level Hamiltonian` (20). No quantum-algorithm item; the LL-mixing classical line appears instead.
25. arXiv API `(three-body | Schrieffer-Wolff | perturbative | renormalized | screening) AND ("fractional Chern" | FQAH) AND ("band mixing" | "remote band(s)" | "higher bands")`. Hits: 2512.07115, 2505.06354, 2407.02560 and 2311.04217. No perturbative band-mixing ED for R-graphene/hBN.
26. arXiv abs 2505.06354, 2507.20647 and 2608.24684.

## Citations
[V] means verified in this session on an arXiv abs page, arXiv API listing, arXiv HTML page or Crossref; the source is given where it matters.

**Classical theory, rhombohedral graphene**
- Yu, Herzog-Arbeitman, Kwan, Regnault, Bernevig, "Moire Fractional Chern Insulators IV: Fluctuation-Driven Collapse of FCIs in Multi-Band Exact Diagonalization Calculations on Rhombohedral Graphene", arXiv:2407.13770, PRB 112, 075110 (2025) [V].
- Li, Bernevig, Regnault, "Multi-Band Exact Diagonalization and an Iteration Approach to Hunt For Fractional Chern Insulators in Rhombohedral Multilayer Graphene", arXiv:2504.20140, PRB 112, 075130 (2025) [V].
- Regnault, Li, Kwan, Bernevig, Herzog-Arbeitman, "The 'Moire Capacitor Effect' and Stabilization of Fractional Chern Insulators in Rhombohedral Graphene Superlattices", arXiv:2608.12452 (2026) [V abs + HTML].
- May-Mann, Tan, Ledwith, Shi, Devakul, "Skyrmion Fractional Chern Insulator: An Intrinsically Multiband Route to Fractionalization in Rhombohedral Graphene", arXiv:2608.14535 (2026) [V].
- Desrochers, Vishwanath, "Energetics of fractional anomalous Hall crystals in rhombohedral graphene", arXiv:2607.08822 (2026) [V].
- Kim, Kivelson, "Entropy-driven transitions between extended integer and fractional quantum Hall regimes", arXiv:2609.16483 (2026) [V].
- Abouelkomsan, Gaggioli, Guerci, Fu, "Rhombohedral Graphene: A Tale of Many Crystals", arXiv:2608.00167 (2026) [V abs + HTML].
- Wang, Zaletel, "Chiral superconductivity near a fractional Chern insulator", arXiv:2507.07921 (2025) [V].
- Listing only [V listing]:
  - Dong, Patri, Senthil, arXiv:2311.03445 and 2403.07873;
  - Zhou, Yang, Zhang, arXiv:2311.04217;
  - Dong et al., arXiv:2311.05568;
  - Soejima et al., arXiv:2403.05522;
  - Kwan et al., arXiv:2312.11617;
  - Huang, Li, Das Sarma, arXiv:2407.08661 and 2408.05139.

**Classical theory, tMoTe2 and methods**
- Li, Yu, Xu, Bernevig, Regnault, arXiv:2608.23675 (2026) [V].
- Morales-Duran, Shi, Voinea, Potasz, Cano, arXiv:2604.16847 (2026) [V].
- Zhang, Luo, "Neural Transformer Backflow for Solving Momentum-Resolved Ground States of Strongly Correlated Materials", arXiv:2509.09275 (2025) [V].
- Luo, Zaklama, Fu, "Solving fractional electron states in twisted MoTe2 with deep neural network", arXiv:2503.13585 (2025) [V].
- Abouelkomsan, Geier, Fu, "Topological Order in Neural Wavefunctions", arXiv:2512.01863 (2025) [V].
- He, Simon, Parameswaran, "Fractional Chern Insulators and Competing States in a Twisted MoTe2 Lattice Model", arXiv:2505.06354 (2025) [V].
- Zhang, Jiang, Luo, arXiv:2608.14208 [V listing].
- Kwan et al., arXiv:2407.02560 [V listing].
- LL-mixing classical line (Crossref DOIs; titles verified):
  - 10.1103/physrevb.87.245425, "Landau level mixing and the fractional quantum Hall effect" (2013);
  - 10.1103/physrevlett.113.086401, "Effects of Landau Level Mixing on the Fractional Quantum Hall Effect in Monolayer Graphene" (2014).

**Experiment**
- Lu et al., arXiv:2309.17436 [V].
- Lu et al., "Extended Quantum Anomalous Hall States in Graphene/hBN Moire Superlattices", arXiv:2408.10203 [V].
- Waters et al., "Interplay of electronic crystals with integer and fractional Chern insulators in moire pentalayer graphene", arXiv:2408.10133, PRX 15, 011045 (2025) [V].
- Aronson et al., arXiv:2408.11220 [V listing].
- Xie et al., arXiv:2405.16944 [V listing].
- Choi et al., arXiv:2408.12584 [V listing].
- Huo et al., "Does Moire Matter? ...", arXiv:2510.15309 [V].
- Li et al., "Stacking-orientation and twist-angle control ...", arXiv:2505.01767 [V].
- Uzan et al., "hBN alignment orientation controls moire strength in rhombohedral graphene", arXiv:2507.20647 [V].
- Pan et al., arXiv:2608.24684 [V].
- Li et al., "Competing Chern states revealed by quasiparticle charging in moire rhombohedral graphene", arXiv:2607.08710 [V].
- Hadjri et al., arXiv:2609.09422 [V listing].
- Wang et al., arXiv:2608.12478 [V listing].

**Quantum**
- Rubin et al., arXiv:2302.05531, PRX Quantum 4, 040303 (2023) [V in the round-2 lens].
- Ding & Lin, arXiv:2211.11973, PRX Quantum 4, 020331 (2023) [V Crossref].
- Bhardwaj, Munoz, Jones et al., arXiv:2604.12142 and 2606.27734 [V listing].
- Exposito et al., arXiv:2607.11380 [V].
- Bai et al., arXiv:2510.09999 [V listing].
- Xu et al., arXiv:2608.05140 [V listing].
- Wu et al., arXiv:2606.16548 [V listing].
- Liu et al., arXiv:2606.23451 [V listing].
- Shen et al., arXiv:2503.13294 [V listing].
- Kirmani et al., arXiv:2512.09982 and 2303.04806 [V listing].
- Rahmani et al., arXiv:2005.02399 [V listing].
- Chu et al., arXiv:2304.13748 [V listing].
- Kobayashi et al., arXiv:2303.04822 [V listing].
- Shen et al. (review), arXiv:2606.02721 [V listing].

Not used: none of the prefilter's "[recalled]" items remain unverified. The prefilter's "Luo, Zaklama, Fu, band-mixing NQS" is confirmed as 2503.13585.
