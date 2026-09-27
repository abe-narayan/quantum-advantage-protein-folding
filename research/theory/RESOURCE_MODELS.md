# T3. Fault-tolerant resource model for one coherent walk step on the A80 learned energy

_Theory lane T3 of `research/THEORY_ROADMAP.md`. It supports H-008 and supplies G(L), the quantity T2 left as assumption A-G (`research/theory/PROOFS/T2_sampling_speedup_statement.md`). v1 written 2026-09-27. **Status: v2 (2026-09-27), revised after two skeptic reviews.** §8 answers the objections that were rejected in whole or in part. §9 logs every objection and its resolution. Every number in §0–§4 was regenerated for v2. v1 numbers survive only in §9, marked as superseded._

**Companion scripts.**
- `research/theory/T3_resource_model.py` evaluates every formula in §3 and prints every table in §4. It is pure arithmetic and runs in about a second.
- `research/theory/T3_table_fit_check.py` runs the checks of §3.2 on the real esmprior_v1 tables in `data/instruments/ladder/` and on PILOT posterior samples in `research/results/RAW/g1_pilot/`:
  - `--energy-error`: energy-level fidelity of the spline;
  - `--fixed-point`: fixed-point emulation of the whole quantum pair-energy pipeline;
  - `--s2-only`: function-level fit on the v2 grid.

  It needs a few minutes of one core per mode. The v2 runs were made at below-normal OS priority on a machine loaded by other jobs.
- **Raw outputs of the v2 checks** are in `research/results/RAW/t3_v2_checks/`, each with a provenance line. The fixed-point output for L ≥ 60 in `checks_B_subgrid_partly_invalid.txt` is **invalid**: a loop variable shadowed the spline-segment argument, so those crops used a 4-segment spline. The bug is fixed, the run was redone as `fixedpoint_C_subgrid.txt`, and the invalid file is kept as a record.

**Citations.** Keys such as [A56] resolve in `research/literature/BIBLIOGRAPHY.md`. Keys [T3-n] are papers verified in the T3 sessions that are not yet in the bibliography (§5.2). All G1 numbers are **PILOT** numbers and only indicative.

**Tags.** Every claim carries one tag.

| Tag | Meaning |
|---|---|
| **DERIVED** | Computed or proved here from the stated model and assumptions (formula in §3, number from `T3_resource_model.py`) |
| **CHECK** | A numerical check in `T3_table_fit_check.py` on the real A80 tables or on PILOT samples |
| **THEORETICAL [key]** | A literature result, quoted as its authors state it. The number was checked against the PDF text (§5) |
| **INFERENCE** | Reasoning that is not a proof, including cost models for sub-circuits nobody has compiled and any extrapolation |
| **UNPROVEN** | Open. Stated as a conjecture or a gap |
| **PILOT** | A number read from `research/results/RAW/g1_*`. Indicative only |
| **A-x / H-x / C-x / O-x** | A labelled assumption (§2) |

**Claim levels.** The repository defines no L0–L6 scale, so this note uses T2's working scale (T2 header table) unchanged:
- **L2**: walk-step speedup, oracle cost excluded.
- **L3**: L2 plus the gate-level cost of the oracle for the actual energy, giving an asymptotic fault-tolerant runtime statement.
- **L4**: L3 plus the measured cost of the best classical portfolio, giving a projected resource advantage.
- **L5 / L6**: compiled validation / hardware.

Theoretical and practical levels are kept separate throughout.

**Bounding devices.** Four settings are more favourable to the quantum side than any estimate supports:
- single-core adversary, S = 1;
- walk overhead c_q = 1;
- κ at its floor κ_min;
- the placeholder t_C.

They appear below only as bounding devices. The verdicts in §0 items 7–9 state which of them they rely on. The headline adversary is S = 10³, the default of [B46].

---

## 0. Summary

1. **Where the gates go (DERIVED).**
   - Coherent evaluation of the pair terms f_ij(d_ij) takes most of the Toffolis in one qubitised walk step. A pair term consists of a squared distance (three squarings), a per-pair spline, and uncomputation of both.
   - Pair-term share of the step, central parameters (S2):

     | design | L=30 | L=200 |
     |---|---|---|
     | D1 | 90% | 99% |
     | D2 | 79% | 97% |
     | D3 (Cartesian) | 59% | 94% |

     The remainder is chain build, head terms and, for D3, CB and window reads.
   - For the torsion designs at L ≥ 100, to within 7%: G ≈ (pair terms per structure, 2·n_p) × τ × n_str × 2.
     - n_str is the number of structures evaluated per oracle call: x and x′, or only x′ with O-1.
     - The final 2 is the compute and uncompute of the oracle within one step. Per-term uncomputation is already inside τ, through u.
   - Coin, move application, in-oracle moves and reflections together cost ≤ 4.2×10⁴ Toffolis, which is ≤ 5.3×10⁻⁴ of G at every L = 30–200.

2. **Toffolis per walk step, G(L) (DERIVED under A1–A15 with fixed-point-validated precision, §3.2).**
   - The working precision b_w now grows with L. It was chosen by fixed-point emulation of the actual pipeline on PILOT samples.
   - Central b_w (fidelity no worse than the classical sampler's own 0.05 Å table): 22, 22, 23, 24, 25 at L = 30, 60, 100, 150, 200. The L=200 value is extrapolated.
   - Generous b_w (TV ≲ 0.01 to the exact target): 20, 20, 22, 23, 24.
   - In the table, generous values are in brackets.

   | design | L=30 | L=60 | L=100 | L=150 | L=200 |
   |---|---|---|---|---|---|
   | D1 literal (torsion moves, √ + 0.05 Å grid table), qubitised | 5.8e7 [1.8e7] | 2.4e8 [7.1e7] | 7.3e8 [2.4e8] | 1.8e9 [5.8e8] | 3.5e9 [1.1e9] |
   | D2 spline in s = d² (torsion moves), qubitised | 2.7e7 [8.1e6] | 1.0e8 [3.0e7] | 3.1e8 [9.3e7] | 7.5e8 [2.2e8] | 1.4e9 [4.2e8] |
   | D3 Cartesian single-residue moves (bond-relaxed target), qubitised | 6.8e6 [4.4e6] | 1.3e7 [9.0e6] | 2.4e7 [1.8e7] | 4.1e7 [3.2e7] | 6.1e7 [4.8e7] |
   | D2, Szegedy walk | 1.6e9 | 1.3e10 | 6.3e10 | 2.3e11 | 5.8e11 |

   - D2 central is G/L² = 2.9–3.6×10⁴. D2 generous is 8.3×10³–1.0×10⁴. D1 central is 6.4–8.7×10⁴.
   - Precision alone moves G by ×1.22–1.50 (central, against the v1 b_w = 20) and ×1.41–1.91 (generous, against the v1 b_w = 16), as §4.7 shows.
   - Sanders et al. give 2.6×10³ Toffolis per qubitised annealing step for SK N=512 and 1.2×10⁶ for LABS N=512 (**THEORETICAL [A56] Tables VIII–IX**). One D2 step at L=150 is ~630 LABS-512 steps. The difference is that every pair term is ≥ 20-bit continuous arithmetic, not a 1-bit product.

3. **Szegedy vs qubitised (DERIVED from THEORETICAL [A56]).**
   - The Szegedy step prepares all M transition amplitudes, so it needs 2(M+1) full energies.
   - It costs 58–403× the qubitised step for the torsion designs (M = 4L−10) and 146–611× for D3 (M = 6L), under central parameters.
   - The two walks have the same spectral gap [A56], so only the qubitised Lemieux–Heim–Poulin–Svore–Troyer ("LHPST") walk matters.
   - Lemieux et al.'s own Boltzmann coin is a lookup over the qubits that ΔE depends on, at cost O(2^{|N_j|}) [A55]. Here |N_j| is the whole system register: 550 qubits at L=30 (torsion) and 1,440 (Cartesian). The coin must therefore be arithmetic, as in Sanders et al.

4. **Energy representation and precision (CHECK on real tables and PILOT samples).**
   - **Grid (v2).** Each pair potential is a cubic in s = d² on a bit-aligned grid, s ∈ [0, 2048) Å² with h = 2 Å² (g = 1,024). Knots fall at s = 4 and s = 16 Å², the steric kink at d = 4 Å. Below s = 4 Å² a 64-segment sub-grid with h = 1/16 Å² is added (§3.2). The segment index and local coordinate are bits of s in both regions.
   - **Steric term.** It is folded into the CA spline. Its fit error is measured, not assumed exact: 1.5×10⁻³ nats per term at worst (CA + sterics, d ≥ 2.45 Å, L=150).
   - **Energy level (float).** Against the smooth A80 function on PILOT samples, the pair-energy error has sd 1.5×10⁻⁵ (L=45) to 4.5×10⁻⁴ (L=150). The classical sampler's own 0.05 Å table has sd 3.0×10⁻³ to 9.9×10⁻³ and a mean offset of +0.06 to +0.45 nats.
   - **The dominant error is fixed-point arithmetic, not the representation.** An emulation of the whole quantum pipeline covers the chain build, CB, the saturating s, quantised coefficients and Horner. It shows:
     - round-to-nearest is required. Truncating multipliers are 4–20× worse in sd and biased by −0.1 to −2 nats;
     - four guard bits in the chain build are worth about 1.5 bits of b_w at large L;
     - the v1 GENEROUS b_w = 16 is **not faithful**. Its sd is 0.09–1.5 nats even with round-to-nearest and guard bits, and 0.19–6.7 nats without guard bits (L = 45–150);
     - b_w must grow with L, as the b_w values in item 2 show.
   - **Cost per term (central, L=100, b_w=23):**
     - D2 spline: **7.6×10³**;
     - D1 literal table: **1.9×10⁴**, of which the Newton square root is 74% of the arithmetic (in the same multiply convention as everything else).
   - **Shared bases are not cheaper in Toffolis.**
     - The soft-bin basis, −log Σ_k P_ijk S_k(s), costs 2.3× D2 per term in the torsion design and 1.2–1.7× D3 per term in the Cartesian design. It never beats D3 for L ≤ 200.
     - A global rank-64 basis reaches only 2.3×10⁻² nats max error and costs ~30× D2.
   - **Why.** With a classical pair index (torsion designs), per-pair data are free, because a QROM costs Toffolis per entry, not per bit or per pair. With a quantum pair index (Cartesian), a QROAM over (residue, segment) costs ≈ 2√(L·g·w).

5. **Locality and κ (DERIVED / INFERENCE).**
   - **Torsion moves** held in superposition force evaluation of every pair, (L−2)(L−3)/2 of them, so G ∝ L². Iterating over moves costs ~2L³/3 instead (INFERENCE; not a lower bound over all circuits).
   - **Cartesian single-residue moves** touch ≈ 4L pair terms, so G grows as L^{0.95–1.4} (including the growth of b_w). Per step, D3 is 4–23× cheaper than D2.
   - **κ floor.** The quadratic speedup is relative to the quantised chain P_W. Running P_W classically is one admissible classical sampler, so κ := N_W/N_C ≥ κ_min = t_C/t_W^cl (DERIVED, §3.11). Counting pair terms:
     - torsion: κ_min = 1.5 (3 with cached per-pair energies);
     - D3: κ_min = n_p/(4(L−5)) ≈ L/8, i.e. 3.8–25 over L = 30–200.
   - **D3's two other costs.** It samples a bond-relaxed target, not the A80 posterior. Its actual κ is unknown (UNPROVEN). D3 loses its break-even advantage over D2 once κ_D3/κ_D2 > (G_D2/G_D3)² = 16 (L=30) to 540 (L=200).

6. **Hardware (DERIVED from THEORETICAL [A56, B46, T3-3, T3-4]).** One qubitised step, central parameters:

   | | L=30 | L=200 |
   |---|---|---|
   | D2, one factory (170 µs per Toffoli) | 1.3 h | 2.8 days |
   | D3, one factory | 19 min | 2.9 h |
   | D2, 100 factories | 46 s | 41 min |
   | D3, 100 factories | 12 s | 1.7 min |

   - Logical qubits: 5.2×10³ (D3, L=30) to 1.1×10⁵ (D1/D2 with stored frames, L=200).
   - Physical qubits at d = 31, in the 2019 surface-code model:
     - one factory: 1.1×10⁷–2.2×10⁸;
     - 100 factories **plus the 99 concurrent pair workspaces that R = 100 requires**: 1.5×10⁸–3.6×10⁸ (D1/D2) and 4.2×10⁸–1.1×10⁹ (D3).
   - Magic-state cultivation [T3-6] and yoked surface codes [T3-7] lower physical-qubit overheads by about an order of magnitude at similar Toffoli throughput. They are not used numerically here.
   - A Szegedy D2 step at L=150 takes **1.2 years** on one factory.

7. **Break-even (DERIVED).** Per independent sample, the qubitised walk wins iff the best classical sampler needs more than
   **B(L) = κ·c_q²·(S·G(L)·t_T / (R·t_C(L)))²**
   single-structure energy+gradient evaluations.
   - The factors:
     - t_T = 170 µs per Toffoli;
     - R = factory parallelism, up to 10³ [B46 Table II];
     - S = classical parallelism;
     - t_C = the classical time per energy+gradient evaluation (PLACEHOLDER 0.2 ms·(L/45)²);
     - κ ≥ κ_min (item 5);
     - c_q ∈ [K, K·ℓ] ≈ [10, 1.8×10⁴] is the walk overhead (T2; §2.6 C4).
   - T* = B·t_C/S is the per-sample runtime at break-even. A κ that grows with N_C (κ ∝ N_C^α) turns the exponent 2 into 2/(1−α). At α → 1 there is no break-even (§3.11).
   - **Headline (S = 10³, κ = κ_min, c_q = 1, placeholder t_C):**
     - D2 central: **3.8–5.7×10¹⁷** at R = 100; 3.8–5.7×10¹⁵ at R = 10³.
     - The most favourable *faithful* design, D2 generous: **3.0–4.8×10¹⁶** at R = 100 (T* ≈ 100–6,000 years); 3.0–4.8×10¹⁴ at R = 10³ (T* ≈ 1–60 years).
     - D3 generous, which has a non-faithful target: 1.1–2.7×10¹⁶ at R = 100; 1.1–2.7×10¹⁴ at R = 10³ (T* ≈ 0.8–13 years).
   - **Bounding device (S = 1, R = 100, c_q = 1):** D2 central 3.8–5.7×10¹¹; D2 generous 3.0–4.8×10¹⁰; D3 generous 1.1–2.7×10¹⁰ (T* 28 days–1.3 years).
   - **Measured t_C.** B is L-independent for the torsion designs **only if t_C ∝ L²**. Measured classical cost grows more slowly: t_C ∝ L^{1.48} (PILOT) and L^{1.43–1.73} (PyTorch). Measured t_C lowers B by 2.2–8.7× (PILOT) or 6–24× (PyTorch). Under the PILOT fit, B for D2 grows roughly as L^{1.2}: 3.6×10¹⁰ → 3.7×10¹¹ over L = 30–200 at S = 1, R = 100.
   - **Self-consistent code distance and error budget.** Making d consistent with these runtimes (d = 37–47, t_T = 204–258 µs) raises B and T* by another 1.4–2.3×. Every break-even run needs ≥ 3.5×10¹² Toffolis. That requires a CCZ error ≤ 3×10⁻¹⁴, beyond the ~10⁻¹⁰–10⁻¹² of the factory assumed [T3-3], so all physical-qubit and time figures are **lower bounds** (§3.10).

8. **Distance to the pilot (PILOT / INFERENCE).**
   - The G1 pilot NRPT runs saw **0** round trips: 1,500, 1,200, 800, 600 and 500 scans at L = 45, 60, 100, 120 and 150.
   - With zero events the mean cost per round trip exceeds the production gradient count (3.9, 3.4, 2.7, 2.0 and 1.7×10⁵) only at ~63% confidence. At ~95% it exceeds one third of that: **1.3×10⁵, 1.1×10⁵, 9.1×10⁴, 6.5×10⁴ and 5.7×10⁴** energy+gradient evaluations, the same bounds as T2 §4.1(b).
   - These are lower bounds on **PT's** cost from non-equilibrated runs. The N_C that enters B is the minimum over the classical portfolio (G-10), which can only push break-even further away. The mode census reaches the best-found mode in ~10³–5×10⁴ local steps (T2 §4.2).
   - Under the 170 µs, R ≤ 10³ model, with κ = κ_min and c_q = 1, break-even needs a true cost of at least these multiples of the 95% bounds:

     | design and setting | placeholder t_C | PILOT t_C |
     |---|---|---|
     | D3 generous, S = 1, R = 100 | 1.2–1.9×10⁵ | 1.5–7.7×10⁴ |
     | D2 generous, S = 10³, R = 10³ | 2.5–7.5×10⁹ | — |
     | D2 central, S = 10³, R = 100 | 2.9–8.6×10¹² | — |

   - Whether the true cost is that large is G1's question. T2 §1 S5 shows the λ-path bottleneck may be classically bypassable.

9. **H-008 verdict.**
   - **Per-step clause ("≤ 10⁶ Toffolis at L=100"): NOT MET by any construction considered (INFERENCE).**
     - The designs that sample the actual A80 target cost 9.3×10⁷ (D2 generous) to 7.3×10⁸ (D1 central) at L=100, 93–730× over.
     - For the **move-oblivious torsion class** there is a conditional floor. It holds if (i) a b-bit squaring costs ≥ b²/2 Toffolis (best known constructions; not a proven lower bound) and (ii) b_w ≥ 22 is needed for faithful sampling (§3.2). The squarings alone then cost 2·2·n_p·3·b_w²/2 ≥ 1.4×10⁷ at L=100. So the clause is **falsified for that class, conditional on (i)–(ii)**. Reaching ≤ 10⁶ would need a structurally different oracle, not better arithmetic.
     - D3 (non-faithful target) costs 1.8–2.4×10⁷, but its squaring floor is only 1.1–1.2×10⁶. For D3 the clause is **inconclusive** within the ~10× modelling uncertainty.
   - **B-clause (B ≤ 10¹²) under the default adversary S = 10³ and t_T = 170 µs:**
     - It **fails for every design at every R ≤ 10³, every κ ≥ κ_min and even c_q = 1**. The minimum is 1.2×10¹⁴ (D3 generous, R = 10³).
     - The falsifier B > 10¹⁵ fires for every design at S = 10³ with R ≤ 100 (minimum 1.2×10¹⁶).
     - It holds only in bounding configurations:
       - S = 1, c_q = 1, R = 100, κ = κ_min, for every design except D1 central. It fails for every design once c_q ≥ 10. With c_q = 1 and R = 100 it survives only against adversaries of at most S_max = 0.6–9 cores (≤ 90 at R = 10³);
       - S = 10³ at an effective Toffoli time of 10 ns (t_T = 1 µs with R = 100): D3 at 4–8×10¹¹ passes, while D2 generous at 1.3×10¹² just misses.
     - With c_q = 90 at S = 1 the falsifier fires for D1 (central and generous) and D2 central.
   - **Levels.**
     - **Theoretical: L3.** G(L) with fixed-point-validated precision is the missing L3 ingredient. Combined with T2's L2 walk-step statement it gives a fault-tolerant runtime statement, conditional on T2's gap and overlap assumptions, on the precision criterion of §3.2, and on the b_w extrapolation to L = 200.
     - **Practical: L0.** No measured classical cost comes near B. The verdict rests on c_q, κ, S and the classical bypasses, not on the hardware cap: at 10 ns effective Toffolis break-even still needs ≥ 4.7×10⁶× the pilot PT bounds at S = 10³.

10. **For T2 (integration; Metropolis walks only).** Replace A-G with the measured structure, not a single g:
    - D1: g ≈ 6.4–8.7×10⁴ (central) and 1.9–2.8×10⁴ (generous);
    - D2: g ≈ 2.9–3.6×10⁴ (central) and 8.3×10³–1.0×10⁴ (generous);
    - D3: not ∝ L²; G ≈ 6.8×10⁶–6.1×10⁷ (central) and 4.4×10⁶–4.8×10⁷ (generous) for L = 30–200.

    T2's range g ∈ [5×10³, 3×10⁴] is optimistic at its low end: the faithful minimum is g ≈ 8×10³ (D2 generous), and D2 central sits at or just above its top.
    - **Scope.** This replaces A-G only for discrete Metropolis walks (LHPST/Szegedy).
    - T2's G_grad = 3G for the continuous gradient-oracle samplers [A44] remains an **unverified placeholder**. A reversible reverse-mode gradient through the prefix product is not costed (G-6). T2's claim level for the [A44] route stays capped until it is.

---

## 1. Statements

**S1 (qubitised step cost; DERIVED from THEORETICAL [A56] eq. 214 and the model of §2).** For the torsion designs D1 and D2, one qubitised walk step costs

```
G_LHPST(L) = 2·C_diff(L) + C_coin + C_F(L) + C_V + C_R
C_diff(L)  = n_str·C_E(L) + 2·C_move(L) + C_head(L) + b_acc            [n_str = 2 (x and x'), 1 with O-1]
C_E(L)     = 2·C_build(L) + 2·n_p(L)·τ_design                         [build+unbuild; CA (sterics folded) and CB per pair]
n_p(L)     = (L−2)(L−3)/2 ;  τ_D2 = 7,034 … 8,849 ;  τ_D1 = 17,140 … 21,902 Toffolis (central, L = 30 … 200)
```

- Closed form, D2 central: **G ≈ 4·τ_D2(b_w)·(L−2)(L−3) + 8·c_build(b_w)·(L−2) + O(10⁵)**.
  - At L=100 (b_w = 23): 4τ = 30,492 and 8·c_build = 2.17×10⁵.
  - The O(10⁵) remainder is the head terms, move adders and coin: 1.5×10⁵ at L=150.
- For the Cartesian design D3:
  - C_diff = 2·4(L−5)·τ_D3(L) + [3 virtual-CB, 5 head, 2 bond terms, window read];
  - τ_D3 = 10,116 (L=30) … 18,415 (L=200) Toffolis (central).

**S2 (dominance; DERIVED).** Pair terms are the following share of G_LHPST (central):

| design | L=30 | L=60 | L=100 | L=150 | L=200 |
|---|---|---|---|---|---|
| D1 | 90% | 95% | 97% | 98% | 99% |
| D2 | 79% | 89% | 93% | 95% | 97% |
| D3 | 59% | 78% | 87% | 91% | 94% |

- The coin, move application, in-oracle moves and reflections are ≤ 5.3×10⁻⁴ of G at every L (≤ 4.2×10⁴ Toffolis).
- **Corollary:** any saving must come from the per-term cost τ or from the number of terms touched. Coin precision and walk bookkeeping do not matter.

**S3 (Szegedy; DERIVED from THEORETICAL [A56] eq. 190).**
- G_Sz = 2(M+1)·C_direct + 2M·C_fun + 2M⌈log M⌉ + 8M·b_sm + 18·b_sm², with M = 2(2L−5) for torsion moves.
- For D3, G_Sz = 2M·C_diff(classical move index) with M = 6L.
- Ratios G_Sz/G_LHPST (central): D1 58–398, D2 60–403, D3 146–611 (L = 30–200).
- The two walks have the same gap [A56], so the qubitised walk dominates.

**S4 (representation; DERIVED + CHECK).** In units of Toffolis per pair term (central):

| representation | torsion design (pair index classical) | Cartesian design (pair index quantum) |
|---|---|---|
| literal 0.05 Å grid + Newton √ (D1) | 17,140 – 21,902 | — |
| per-pair cubic in s, v2 grid g = 1024 + 64 (D2 / D3) | **7,034 – 8,849** | **10,116 – 18,415** |
| soft-bin shared basis (W = 5 active smoothed bins) | 16,464 – 20,838 | 16,964 – 22,400 |
| global SVD basis, R = 64 | 2.2 – 2.9×10⁵ | — |

- The per-pair spline is the cheapest in both designs at L ≤ 200.
- Soft-bin vs D3, per term: 1.68× (L=30) falling to 1.22× (L=200). The crossing lies beyond L = 200.
- Fidelity: the v2 spline reproduces each pair potential to ≤ 1.5×10⁻³ nats (CA + sterics, d ≥ 2.45 Å) and the total pair energy to sd ≤ 4.5×10⁻⁴ nats on PILOT samples (§3.2).

**S5 (break-even; DERIVED; the same algebra as THEORETICAL [B46] eqs 1–5, 12).**
- Let N_C be the best classical sampler's cost per independent sample, in energy+gradient evaluations. Let N_W be the per-sample step count of the quantised chain P_W. Set κ := N_W/N_C.
- Assume the qubitised walk needs Q = c_q·√N_W = c_q·√(κ·N_C) steps per sample. Then

```
T_C = N_C·t_C/S ,   T_Q = c_q·√(κ N_C)·G·t_T/R
T_Q < T_C  ⟺  N_C > B(L) := κ·c_q²·(S·G(L)·t_T/(R·t_C(L)))²
T*(L) := T_Q = T_C at break-even = κ·c_q²·S·(G·t_T/R)²/t_C
κ ≥ κ_min := t_C / t_W^cl      (P_W run classically is an admissible classical sampler; §3.11)
```

- **B scales as t_C⁻².** Every 10× gain in classical per-evaluation speed is 100× in B.
- **L-dependence is conditional.** If G and t_C are both Θ(L²), B is independent of L:

  ```
  B = κ·c_q²·(S/R)²·(γ·t_T/τ_pair)²
  ```

  - γ is the quantum Toffolis per pair (i,j) per step (≈ 6.1×10⁴ for D2 central at L=100).
  - τ_pair is the classical seconds per pair per energy+gradient (≈ 205 ns under the placeholder).

  The PLACEHOLDER t_C is ∝ L² by construction. Measured t_C grows as L^{1.4–1.7}, so under measured t_C, B grows with L (§4.5).

**S6 (numbers).** §4.5–4.6. The headline values are in §0 items 7–8.

**S7 (H-008).** See §0 item 9.

**S8 (what G(L) buys in T2's language; DERIVED mapping).**
- T2's break-even condition `ρ·K·ℓ·G·t_T·√τ* < c·B_best` is S5 with c_q = K·ℓ, κ·N_C = τ*, N_C = B_best and S ↔ ρ.
- T2 writes the walk-step count as K·ℓ·δ_*^{-1/2}. That is an upper bound in which all ℓ stages have the bottleneck gap. If a single bottleneck stage dominates, the count is ≈ K·δ_*^{-1/2}. Hence **c_q ∈ [K, K·ℓ]**.
- With K ∈ [10, 10³] (T2 A-K) and ℓ ≈ 0.63·Λ ≈ 9–18 (PILOT), c_q ∈ [10, ~1.8×10⁴].
- **Every B here with c_q = 1 is therefore low by a factor c_q² ∈ [10², ~3×10⁸].**
- The stage-accounting inconsistency is raised with T2 (G-9).

---

## 2. Model and assumptions

### 2.1 The energy (read from `src/qapf/protein/energy.py`, `esmprior_v1.py`)

```
E(x) = Σ_{|i−j|≥3} [ f^CA_ij(d_ij) + f^CB_ij(d^cb_ij) + w_s·relu(4 − d_ij)² ] + Σ_i h_i(θ_i, τ_i) + w_w·Σ_i wall(θ_i)
f_ij(d) = −log( Σ_{k=1..28} P_ijk·S_k(d) + 10⁻⁶ ),   S_k(d) = Φ((hi_k − d)/σ) − Φ((lo_k − d)/σ),  σ = 0.5 Å
h_i = −log( st(θ_i)ᵀ·PT_i·sa(τ_i) + 10⁻⁶ )   (9 θ-bins × 24 τ-bins, Gaussian-smoothed memberships)
wall(θ) = relu(θ − 170°)² + relu(60° − θ)²   (θ in degrees)
```

- Bin edges are 4, 5, …, 20 Å, then 22, 24, …, 40 Å, plus an open last bin. The weights are w_s = 10 and w_w = 0.01.
- **Classical evaluation.** The classical code tabulates f on a 0.05 Å grid over 0–50 Å (1,001 points) and interpolates linearly. Sterics are added analytically.
- **Coordinates.** x = (θ_1..θ_{L−2}, τ_1..τ_{L−3}), so there are n_ang = 2L−5 angles. The chain is built by the prefix product F_k = F_{k−1}·R_x(τ_k)·R_z(π−θ_k), with X_k = X_{k−1} + 3.8 Å·F_k e₁. A float re-implementation reproduces `build_ca` to 2×10⁻¹⁴ Å (CHECK).
- **Pair counts.** n_p(L) = 378, 1,653, 4,753, 10,878 and 19,503 for L = 30, 60, 100, 150 and 200.
- **Virtual CB (DERIVED from the code; CHECK to 2×10⁻¹⁴ Å).** In the frame F_{i+1}, the two bond unit vectors at residue i are u₂ = e₁ and u₁ = (cos a, −sin a, 0), with a = π − θ. Both depend only on θ. Hence CB_i = X_i + F_{i+1}·v(θ), where v is a fixed 3-vector function of θ, and CB costs one 3×3 matrix-vector product per residue.
- **Annealing path.** π_λ ∝ exp(−(E_prior + λ·E_pair)/T) with E_prior = Σ h_i + w_w·Σ wall and E_pair = the pair terms. A walk step works at fixed (λ, T).
  - λ/T is folded into the **per-pair spline coefficients** and 1/T into the **head-term and wall tables**. Both are classical QROM data at zero Toffoli cost.
  - ΔE therefore reaches the coin already scaled, and the coin's interpolation table does not depend on (λ, T).
  - (v1 said λ was folded into the coin table. That is wrong, because λ multiplies only E_pair.)

### 2.2 State spaces and move sets

- **Torsion (D1, D2).**
  - State: x ∈ (Z_{2^b})^{n_ang}. Both θ and τ registers cover [0°, 360°) with lattice step 2π/2^b = 0.35° (b = 10).
  - Move j = (angle a, sign s ∈ {±1}): x_a ← x_a + s·δ mod 2^b, for θ as well as τ (wrap-around).
    - θ has no reflecting boundary. The wall term keeps θ in (60°, 170°), and at the wrap point θ = 0 ≡ 360° the wall energy is ≥ 36 nats. Aliasing the classical target (θ ∈ ℝ with soft walls) onto the circle therefore changes it only on a set of mass ≲ e^{−36} (INFERENCE).
  - **δ is a classical constant in lattice units. Central: δ = 1 unit = 0.35°.** G does not depend on δ.
    - On PILOT samples a single-angle move of one unit already changes E by a median 0.1 nats (L = 45–60), 0.25–0.5 (L = 100–120) and 0.6–1.1 (L = 150) (CHECK, `--fixed-point`).
    - Larger δ would be mostly rejected at large L, which suggests κ ≫ κ_min for P_W (INFERENCE; G-1).
  - M = 2·n_ang = 4L−10 moves, with a symmetric proposal.
  - **Involution.** F: (x, a, s) ↦ (x + sδ·e_a, a, −s) is self-inverse, as the LHPST construction requires. Its cost is the controlled ±δ add plus a sign-bit flip.
  - The target is the A80 posterior restricted to the b-bit lattice, evaluated in the fixed-point formats of A2.
- **Cartesian (D3).**
  - State: 3L coordinates of b_x bits each.
  - Move j = (residue r, direction ∈ {±x, ±y, ±z}): X_r ← X_r + Δ·e, so M = 6L.
  - The target is A80 in Cartesian form (as in `Energy.energy_cart`) plus a bond restraint w_b·Σ(|X_{i+1}−X_i| − 3.8)². This is **a bond-relaxed target, not the A80 posterior**. A fixed-point Cartesian lattice cannot hold bond lengths exactly under moves (INFERENCE).

### 2.3 Walk constructions

- **Qubitised (LHPST; THEORETICAL [A55, A56] for bit-flip moves).** U_W = R·V†·B†·F·B·V, where:
  - V prepares the move superposition;
  - B rotates the coin by arcsin √p_{x,x_j};
  - F applies move j when the coin is |1⟩;
  - R reflects about |0⟩_M|0⟩_C.

  It block-encodes the same Szegedy operator [A56 eqs 192–200].
  - **Scope of the literature result.** It is stated and proved for bit-flip moves on Z_2^n: [A55] eqs 23–24 use x·z_j and the isometry |x⟩|y⟩ → |x⟩|x·y⟩, and [A56] eq. 214 (Table VI) costs that case.
  - **The extension used here is INFERENCE.** It applies the construction to ±δ additive moves on (Z_{2^b})^{n_ang} with the involution F of §2.2. The requirements are that F be a self-inverse permutation of (state, move) pairs and that the proposal be symmetric. Both hold for wrap-around ±δ moves. No proof beyond this check is offered, and a small unitary check is open (G-4).

  **Sanders et al.'s implementation.** ΔE_j(x) and arcsin √p are computed once, kept through F (F flips the sign bit of ΔE, matching s ↦ −s) and uncomputed once. The cost is **2C_diff + 2C_fun + 2b_dif + O(1)** [A56 §III E.1].
- **Szegedy.** It needs all M transition probabilities per step, at cost min(2(M+1)·C_direct, 2M·C_diff) + 2M·C_fun + 2M log M + 8M·b_sm + 18·b_sm² [A56 eq. 190]. "The Szegedy walk approach is strictly less efficient than the qubitized variant" [A56 §IV]. The two have the same gap [A56].
- **Lemieux et al.'s coin** is O(N·2^{|N_j|}·log 1/ε) and "exponential with the sparsity parameters" [A55, Table 1 and §2.4]. For this energy, ΔE_j depends on every system qubit, so |N_j| = n_sys. **The lookup coin is inapplicable (DERIVED).** The arithmetic coin of [A56] is used.

### 2.4 Literature cost primitives (THEORETICAL; verified against the PDFs, §5)

| # | primitive | cost used | source |
|---|---|---|---|
| P1 | n-bit addition | n − 1 Toffolis (T-count 4n − 4); we use n | [T3-1] |
| P2 | controlled n-bit addition | 8n + O(1) T ≈ 2n Toffolis | [T3-1] |
| P3 | n×n→n fixed-point multiply | n² (the b_sm² convention of [A56] §II E). Round-to-nearest by initialising the product accumulator with 2^{f−1} (X gates; INFERENCE). HRS's circuit with Takahashi adders costs 1.5n² + 3np + 1.5n − 3p² + 3p ≈ 2.25n² at p = n/2 [A59 App. A–B], so **our central multiply is ≈ 2× generous** (§4.7: ×2.16 on G) | [A56, A59] |
| P4 | QROM over g entries | g − 2 Toffolis (g − 1 controlled), "independent of the number of bits of data output" [A56 §II E]; "T complexity of 4L − 4 with no dependence on the word length" [A60] | [A56, A60] |
| P5 | QROAM, d entries of M bits | compute ⌈d/k⌉ + M(k−1) Toffolis with (k−1)M clean ancillae; measurement-based uncompute ⌈d/k′⌉ + k′ [F59 App. C]. Select-swap trade-off O(λb + N/λ) → O(√(Nb)) [T3-2] | [F59, T3-2] |
| P6 | inverse square root (Newton, m iterations) | HRS iteration T_iter = 5·T_mul + 2·T_add [A59 App. C], **costed in our P3 convention**: m(5n² + 2n) + (3/2.25)n² + 5n. The initial-guess term 3n² + 5n of HRS's formula is rescaled by T_mul^HRS ≈ 2.25n². HRS's own count, n²(15m/2 + 3) + 15npm + … (11,056 at n = 20, m = 2), is an upper bound that excludes iterate uncomputation; it is used only in the §4.7 sensitivity row. √s = s·s^{−1/2} adds one multiply | [A59] |
| P7 | coin function arcsin √(e^{−z}) by QROM interpolation | C_fun = (b_sm + b_fun)² + b_dif + O(b_sm log b_sm + 2^{b_fun/2}) [A56 eq. 96]; controlled rotation b_sm Toffolis via the phase-gradient state [A56 §III E.1] | [A56] |
| P8 | equal superposition V over M items | 4k + 2s − 13 Toffolis, k = ⌈log₂ M⌉ [A56 §III E.2] | [A56] |
| H1 | Toffoli time | 170 µs with one CCZ factory; ~150,000 physical qubits per factory region; d = 31; 1 µs cycles; p = 10⁻³ [A56 §IV]. [B46] eq. 6 reads verbatim "t_G = 30 × 5.5 × 1 µs ≈ 170 µs" ("a code distance in the vicinity of d = 30"); at Sanders' d = 31 the same rule gives 5.5·31 = 170.5 µs. A CCZ every 5.5d cycles [T3-3] | [A56, B46, T3-3] |
| H2 | parallel factories | reduce t_Q "only by a factor that is between about ten and one-hundred" (Clifford/routing limits) [B46]. [B46] Table II nevertheless tabulates R = 10, 10² and 10³ (Toffoli time 170 µs/R) against S = 10³. We use R ∈ {1, 10, 100, 10³} | [B46] |
| H3 | surface-code overheads | 2(d+1)² physical per logical qubit [T3-4 §2.14]; logical error per qubit per cycle ≈ **10^{−⌈d/2+1⌉}** at p = 10⁻³ [T3-4 §2.13]. Their worked example: 10^{−⌈27/2+1⌉}·226·63·0.75·25×10⁹ ≈ 27%. (v1 miscopied this as 10^{−⌈d/2⌉+1}, which is 100× too pessimistic.) | [T3-4] |
| H4 | break-even algebra | T_Q = M·t_Q, T_C = M^d·t_C/S, advantage iff M > (t_Q·S/t_C)^{1/(d−1)}; with R factories M > t_Q·S/(t_C·R), T* = t_Q²·S/(t_C·R²) (d = 2) [B46 eqs 1–5, 12]. Default adversary S = 10³; "for simulated annealing we can achieve S = 10⁶ in practice" [B46] | [B46] |
| H5 | CCZ output error | "our CCZ factory can produce ∼10¹⁰ states on average before an error occurs"; "∼10¹² by increasing the factory footprint ∼20%" (p = 10⁻³; distances 7 / 15 / 31) [T3-3] | [T3-3] |
| H6 | newer FT overheads (not used numerically) | magic-state cultivation: T states "as cheap as CNOT gates", 2×10⁻⁹ logical error at 10⁻³ noise, distance 15 [T3-6]; yoked surface codes + cultivation: RSA-2048 with < 10⁶ qubits in < 1 week, 1 µs cycles, 10 µs reaction time [T3-7] | [T3-6, T3-7] |

### 2.5 Program assumptions (our estimates; each labelled)

- **A1.** b = 10 bits per angle (0.35°). The sensitivity to b ∈ {8, 12} is < 1% of G (DERIVED, §4.7). b enters only the table lookups and the move adders.
- **A2 (revised; CHECK-validated).** Fixed-point formats. The sign bit is included in every width.

  | register | format |
  |---|---|
  | trig tables cos/sin, v(θ), frame entries F | 1 sign + 1 integer + (b_w + 4 − 2) fractional bits (four guard bits in the build) |
  | coordinates X, CB (Å) | 1 sign + IX integer + (b_w + 4 − 1 − IX) fractional, with IX = ⌈log₂(3.8(L−1)+2)⌉ = 7–10. Rounded to b_w bits (guard bits dropped) after the build |
  | coordinate differences | b_w bits. If any \|ΔX_c\| ≥ 64 Å, s saturates |
  | s = \|ΔX\|² (Å²), unsigned | 11 integer + (b_w − 11) fractional; saturating at 2048 Å² (d > 45.25 Å, where every A80 pair potential is flat) |
  | spline coefficients, Horner accumulator | 1 sign + 7 integer + (b_w − 8) fractional (b_c = b_w) |
  | every product | round-to-nearest (P3) |

  - b_w(L) is the smallest measured width meeting a stated fidelity criterion on PILOT samples (§3.2). Intermediate L takes the next measured L, and L=200 is extrapolated by +1 bit (INFERENCE):
    - central: 22, 22, 23, 24, 25 at L = 30, 60, 100, 150, 200;
    - generous: 20, 20, 22, 23, 24.
  - Sensitivity at L=150, D2 central: b_w = 20 / 22 / 28 gives 0.73× / 0.86× / 1.32×. Guard bits 0 / 8 give 0.99× / 1.01×.
- **A3 (revised).** Per-pair representation, the v2 grid:
  - a cubic (p = 3) in the local coordinate of g = 1,024 uniform segments of s ∈ [0, 2048) Å² (h = 2 Å²), plus a 64-segment sub-grid of h = 1/16 Å² on s < 4 Å²;
  - the segment index and local coordinate are bits of s in both regions, and the region switch costs ~3·b_w Toffolis (test s < 4, controlled shift, index select);
  - the sub-grid is needed for the CB channel, whose potential has a √s cusp at s = 0 from the Φ(−d/σ) edge of bin 0. Without it, CB–CB pairs at d < 1.5 Å (about 0.4–1 per PILOT sample at L ≥ 120) give an energy-level floor of sd 1.4–1.8×10⁻² nats at L = 120–150 (CHECK);
  - knots at s = 4 and 16 Å² (d = 2 and 4 Å). The steric term w_s·relu(4 − d)² is **folded into the CA spline**. It is not a polynomial in s, so its fit error is measured: ≤ 1.5×10⁻³ nats per term (§3.2);
  - the CA channel's tabulated function is clamped at d = 2 Å, which changes the target only for CA–CA contacts below 2 Å, which carry ≥ 40 nats of steric energy;
  - b_c = b_w-bit coefficients;
  - g = 512 would save 2% of G and was not validated at the energy level. It is not used.
- **A4 (revised).** b_acc = b_dif = 40.
  - Sized for the worst case over all basis states, not the lowest energy found. With the d = 2 Å clamp a pair contributes ≤ 2·13.8 + 10·(4−2)² = 67.6 nats, so E_pair ≤ 1.3×10⁶ at L = 200. That needs 21 integer bits + sign + (b_w − 8) ≤ 17 fractional bits.
  - The cost of b_acc = 32 → 48 is < 0.5% of G (§4.7).
- **A5.** Coin precision b_sm = b_fun = 7, as chosen in [A56] and validated there only on SK with 16 spins. At 14 bits the coin costs 2,124 Toffolis (2,092 with b_acc = 32), still < 10⁻³ of G (INFERENCE).
- **A6.** SQ = MUL = b_w² (central). The symmetric-square trick gives SQ = b_w²/2 (generous).
- **A7.** QROAM blocking k is chosen to minimise Toffolis. The ancilla cost is reported.
- **A8.** Newton square root with m = 2 iterations, used by D1 and by D3's CB and head terms. It is costed in the P3 convention (P6).
- **A9.** Per-term arithmetic temporaries are uncomputed right after accumulation, so u = 2 (central). The generous value u = 1.5 credits measurement-based uncomputation of AND-type intermediates [T3-1]. The oracle itself is computed once and uncomputed once per step [A56].
- **A10.** −log(·) ≈ leading-one detection + a 64-segment QROM interpolation + 2 multiplies ≈ 1.2×10³ Toffolis at b_w = 23 (INFERENCE, not compiled).
- **A11 (recounted).** Sequential chain build per residue, at b_w + 4 bits:
  - M = F_{k−1}·R_x(τ_k): columns 1 and 2, 12 multiplies;
  - F_k = M·R_z(π−θ_k): columns 0 and 1, 12 multiplies. Column 2 of M is column 2 of F_k;
  - the CB offset F_{k+1}·v(θ): 9 multiplies;
  - the bond 3.8 Å·col₀(F_k): 3 constant multiplies, counted as 1.5·(b_w+4)²;
  - **24 additions**: 12 in the rotations, 3 for X, 6 in the matrix-vector product, 3 for CB;
  - two shared 2^b-entry lookups: (cos θ, sin θ, v(θ)) and (cos τ, sin τ);
  - 6 additions to round X and CB to b_w bits.

  The one intermediate that is not part of F_k is column 1 of M, three entries. It is **stored** (3·(b_w+4) qubits per residue, zero Toffolis; the unbuild removes it) when frames are stored, and **uncomputed** (+6 multiplies + 3 additions) in the checkpointed variant.
  - Coordinates are kept in Å rather than 3.8 Å units, so that the steric knot at s = 16 Å² falls on the dyadic grid.
  - (v1 counted 15 additions and ignored the intermediate column.)
- **A12.** Frames are stored: 18·(b_w+4) qubits per residue for X, CB, F and column 1 of M (central). The checkpointed variant keeps ⌈√L⌉ checkpoints plus a working segment and rebuilds. It costs +28% (L=30) to +4.6% (L=200) of G for D2 central and is not the design costed in §4.
- **A13.** Structures x and x′ are processed one after the other (build, accumulate, unbuild), so only one structure's workspace is live at a time.
- **A14.** Head terms.
  - Torsion moves: only the moved residue's (θ, τ) term changes. That is a QROAM over (residue, θ-window, τ-window) with 216·(L−3) entries of 9·b_c bits, plus 12 multiplies and a −log.
  - Cartesian moves: 5 head terms and 3 virtual CBs change. Each CB needs 5 inverse square roots (bonds are not exactly 3.8 Å). Each head term needs normalised dot and cross products plus an atan2, modelled as 1.5× a square root (INFERENCE).
- **A15.** D3 details:
  - b_x = 16; K_d = 6 directions;
  - pair data indexed by (r, segment) through a QROAM over L·(g + 64) entries;
  - the |r−j| ≥ 3 flag costs 2⌈log₂ L⌉;
  - a 7-residue coordinate window is read by unary iteration, costing L·(1 + 21·b_x), doubled for unreading.
- **O-1 (generous variant only; INFERENCE, our construction).** An energy-carrying register |x⟩|E(x)⟩.
  - The oracle then computes only E(x_j). F swaps the energy registers and negates the move displacement, so after F the temporary holds E(x_current + move) in both branches and is uncomputed by the same circuit.
  - This is the analogue of the sign-flip trick in [A56]. It halves C_diff for D1 and D2.
  - It is not in the literature. A small-scale unitary check is open (G-4).
- **GENEROUS** = {b_w = the TV ≤ 0.01 widths of A2, b_c = b_w, u = 1.5, SQ = b_w²/2, O-1}.
  - It keeps g = 1,024 + 64.
  - The v1 GENEROUS b_w = 16 is **withdrawn as non-faithful** (§3.2).

### 2.6 Classical side (C-assumptions)

- **C1 — t_C(L) = 0.2 ms·(L/45)².** This is a **PLACEHOLDER** for one single-structure energy+gradient on one core. It was specified by the task and must be replaced by G1 measurements.
  - It implies τ_pair ≈ 205 ns per pair per evaluation.
  - It scales as L², whereas every measurement scales as L^{1.4–1.7} (C2).
- **C2 — measured alternatives (PILOT or quick; for calibration only).**
  - **PILOT.** PT wall-clock per gradient evaluation, including all HMC/PT overhead (`secs / grad_evals_total` in the RAW JSONs): 0.59 (L=45), 0.78 (60), 1.46 (100), 2.39 (120) and 3.51 (150) ms. Power-law fit: **t_C ∝ L^{1.48}**.
  - **Quick timing.** From the v1 session, `T3_table_fit_check.py --timing`, on a machine running G1 jobs concurrently. PyTorch batch-64 energy+gradient per structure: 0.29 (L=30), 0.97 (L=45), 1.40 (L=60), 2.94 (L=100) and 5.44 (L=150) ms. The fit is **L^{1.73}** over L = 30–150 and L^{1.43} over L = 45–150. Batch-1 is 7–12 ms because of framework overhead.
  - **INFERENCE.** An optimised scalar implementation would need about 15–30 ns per pair term, i.e. 0.3–0.65 ms at L=150, against 2.2 ms for the placeholder.
  - **Effect on B (B ∝ t_C⁻²).** PyTorch batch-64 timings lower B by **6–24×**. PILOT wall-clock per evaluation lowers it by **2.2–8.7×**. Optimised code would raise it by **~12–50×**. (v1 said "2–5×", which was not squared.)
- **C3 — κ := N_W/N_C (revised).**
  - N_W is the per-sample step count of the *quantised* chain P_W run classically. N_C is the best classical sampler's per-sample energy+gradient count.
  - The quadratic speedup is relative to the quantised chain [A1, A8; T2 §1], not to the best classical algorithm.
  - **Floor (DERIVED, §3.11).** κ ≥ κ_min = t_C/t_W^cl:
    - torsion: 1.5 (uncached) or 3 (cached per-pair energies);
    - D3: n_p/(4(L−5)) = 3.8, 7.5, 12.5, 18.8 and 25 at L = 30, 60, 100, 150 and 200 (2× with caching).

    §4 uses the uncached floors, which are more favourable to quantum. κ = 1 is **infeasible** and appears only as a reference line.
  - **Not a constant (INFERENCE).**
    - T2's A-chain heuristic gives κ ~ d^{3/4} ≈ 50 at L=100 (Metropolis vs HMC for i.i.d. targets).
    - If the best classical sampler is non-reversible or lifted (NRPT already is; [A14, A15, A18]), κ can grow with N_C. Write κ = κ₀·N_C^α.
    - Lifting gains at most a square root over the reversible chain ([A14], as usually stated), so α ∈ [0, 1).
  - §4 reports B for κ ∈ {κ_min, 50, L} and for α ∈ {0, 0.25, 0.5, 0.75}.
- **C4 — c_q (bounding value 1).** The walk steps per √N_W: QSA stage overheads, phase estimation and log factors. c_q ∈ [K, K·ℓ] ⊂ [10, ~1.8×10⁴] (S8). §4 reports c_q ∈ {1, 10, 90}.
- **C5 — S, R and t_T.**
  - S ∈ {1, 10³, 10⁶} [B46]. S = 10³ is the headline default and S = 1 is a bounding device.
  - R ∈ {1, 10, 100, 10³} [B46 Table II].
  - t_T ∈ {170, 10, 1} µs as a hardware envelope (T2 A-t).

---

## 3. Derivation

### 3.1 How many pair terms a step must touch

**Torsion moves (DERIVED for the move-oblivious circuit; INFERENCE for optimality).**
- Changing angle a rigidly moves one side of the chain. So d_ij changes exactly for the pairs that straddle a, which is about a·(L−a) pairs.
- The move register holds a superposition over all 2·n_ang moves, and every pair with |i−j| ≥ 3 is straddled by some move. A circuit that does not branch on the move register must therefore evaluate every pair term for x and for x′. That is 2 (structures) × 2·n_p (CA and CB) terms per oracle call.
  - Looping over all pairs with a controlled "is (i,j) straddled by a?" test is still move-oblivious in cost.
- The alternative is unary iteration over the n_ang ≈ 2L angles, evaluating only that move's straddling pairs under control. It costs Σ_a 2·a(L−a) ≈ 2L³/3 terms per structure, which is more than 2·n_p ≈ L² for every L ≥ 3. (v1 wrote L³/3 by summing over L angles instead of 2L.)
- Hence **G ∝ L² for the faithful torsion-space chain.** This answers T2 open item 7:
  - O(L)-per-move incremental ΔE is not available coherently when the torsion index is quantum;
  - Cartesian local moves restore it (§3.8) at the price of quantum-indexed data.
- A general lower bound over all circuits is not claimed. §0 item 9 uses only the conditional floor for the move-oblivious class.

**Cartesian single-residue moves (DERIVED).** Moving X_r changes:
- the CA pairs (r, j) with |r−j| ≥ 3: L − 5 terms for interior r;
- CB_{r−1}, CB_r and CB_{r+1}, each of which depends on X_{i−1}, X_i and X_{i+1}: about 3(L−5) terms;
- θ at r−1, r, r+1 and the τ's of the four dihedrals containing r: at most 5 head terms;
- two bond terms.

Each changed term is evaluated at the old and new positions.

### 3.2 Toffolis per pair term τ, the fit checks and the fixed-point analysis

**Per-term cost (central, L=100, b_w = 23).**
- Squared distance: SQDIST = 3 SUB + saturation (3·(IX−5) + 2b_w) + 3 SQ + 2 ADD = **1,760**.
- Each term then adds u × its arithmetic, its lookup and one accumulator addition (b_acc = 40).
- **D1 (literal classical table).**
  - Arithmetic: SQDIST + √s (P6, n² convention: 6,731) + grid index (2 additions) + linear interpolation (1 multiply + 1 addition).
  - Lookup: QROAM(1001, 2·b_c). The pair index is classical because the circuit loops over pairs in a fixed order.
  - **τ_D1 = 18,668**. The Newton square root is 74% of D1's arithmetic. In HRS's own multiplier convention the square root would be 14,981 and D1 ≈ 2.2× more.
- **D2 (per-pair cubic in s, v2 grid).**
  - Arithmetic: SQDIST + region select (3·b_w) + Horner (3 multiplies + 3 additions = 1,656).
  - Lookup: QROAM(1,088 segments, 4·b_c = 92 bits).
  - **τ_D2 = 7,623** (7,034–8,849 over L = 30–200).
- **D3 (Cartesian; per-pair cubic; quantum pair index).**
  - Arithmetic: as D2, plus 2⌈log₂ L⌉ for the |r−j| flag.
  - Lookup: QROAM(L·1,088, 4·b_c).
  - **τ_D3 = 10,116 … 18,415** (L = 30 … 200).
- **Soft-bin shared basis.**
  - Arithmetic: SQDIST + 5 multiplies (the W = 5 active smoothed-bin functions S_k(s), linear interpolation from one shared 2048-segment QROAM) + 5 multiplies (dot product with the weights) + −log.
  - Lookups: the shared basis, QROAM(2048, 10·b_c) = 1,234 at b_c = 23 (1,174 at b_c = 20; v1 wrote 1,280), plus a weight-window QROAM over 24 windows (torsion) or 24·L (Cartesian).
  - **τ = 16,464–20,838 (torsion) and 16,964–22,400 (Cartesian).**
  - Truncating to W = 5 active bins drops the other 23 bins' Gaussian tails (≳ 4σ away). The error of that truncation is not checked, so this basis is **not** exact up to interpolation (INFERENCE).
- **Global SVD basis (R = 64).**
  - Arithmetic: SQDIST + u², u³ (2 multiplies) + 3R quantum multiplies (R shared cubics) + R constant-coefficient MACs.
  - **τ ≈ 2.4×10⁵.**
- **Uniform-d alternative.** Segments uniform in d need 8× fewer segments (g = 128), but they need d = √s. At L=150 that is 22,253 Toffolis per term against 8,227 for D2, so **uniform-s wins by 2.7×** in a single multiply convention. (v1 said ~5×, comparing across conventions.)

**Function-level fit check (CHECK; real esmprior_v1 tables).** The table gives the per-term max |error| in nats over all pairs with |i−j| ≥ 3 for a per-segment least-squares cubic.

| crop (L=150) | channel | v1 grid "s" g=1024 (h = 1.84 Å², not bit-aligned) | **v2 grid "s2" g=512 / 1024 / 2048 (h = 4 / 2 / 1 Å², d ≥ 2.45 Å)** | uniform-d g=128 |
|---|---|---|---|---|
| 2AB0A | CA (smooth part) | 6.5e-4 | 4.8e-3 / **8.9e-4** / 5.6e-5 | 5.1e-4 |
| 2AB0A | CB | 2.0e-4 | 2.1e-3 / **2.9e-4** / 2.4e-5 | 4.5e-4 |
| 2AB0A | **CA + sterics folded** | 4.0e-3 (the kink falls inside a segment) | 2.1e-2 / **1.5e-3** / 8.6e-5 | — |
| 5O37A / 4LPQA | CA / CB (v1 grid only) | 6.1e-4 / 2.1e-4; 5.1e-4 / 2.9e-4 | not rerun | 4.5e-4 / 3.9e-4; 3.3e-4 / 4.2e-4 |

- **v1 was wrong about the knot.** On the v1 grid, uniform in s over [2.5², 43.5²] Å² with g = 1,024, s = 16 Å² is **not** a knot: (16 − 6.25)/1.8418 = 5.29. v1's "exact" steric folding was never tested, because v1's energy check added sterics analytically.
- **With the knot at 16 Å² (v2), folding is still not exact.** relu(4 − √s)² = 16 − 8√s + s is not a polynomial in s. Its fit error, ≤ 1.5×10⁻³ at g = 1,024, is concentrated at d ≈ 2.5–3 Å, where the √s curvature is largest.
- **Global SVD basis**, max error: R = 16: 0.47 (CA); R = 40: 0.15; R = 64: 2.3×10⁻² (CA) and 9.6×10⁻³ (CB). **The A80 pair potentials are not low-rank.** They have 28 bins of pair-specific shape.

**Energy-level check, float arithmetic (CHECK; `--energy-error`; 60 PILOT samples per crop).**
- The comparison is the total pair energy (CA + sterics + CB) of the v2 spline against the smooth function it approximates, with the classical sampler's 0.05 Å table in the last columns.

| L | E_pair (nats) | v2 g=1024, no sub-grid: sd / max | **v2 g=1024 + 64: sd / max** | v2 g=2048 + 64: sd | classical 0.05 Å table: mean offset / sd |
|---|---|---|---|---|---|
| 45 | 3,668 | 1.8e-5 / 5.3e-5 | **1.5e-5 / 4.7e-5** | 1.0e-6 | +6.0e-2 / 3.0e-3 |
| 60 | 8,003 | 2.0e-5 / 5.5e-5 | **2.0e-5 / 5.5e-5** | 1.3e-6 | +7.1e-2 / 4.3e-3 |
| 100 | 20,652 | 2.8e-3 / 2.2e-2 | **7.9e-5 / 2.1e-4** | 5.2e-6 | +2.5e-1 / 4.6e-3 |
| 120 | 32,896 | 1.4e-2 / 3.6e-2 | **1.5e-4 / 4.2e-4** | 6.7e-6 | +2.7e-1 / 5.4e-3 |
| 150 | 52,147 | 1.8e-2 / 4.4e-2 | **4.5e-4 / 1.2e-3** | 2.6e-5 | +4.5e-1 / 9.9e-3 |

- The floor without the sub-grid comes entirely from CB–CB pairs at d < 1.5 Å, about 0.4–1 per sample at L ≥ 120 (CHECK, per-distance breakdown). In the same breakdown the folded CA steric error is ≤ 4×10⁻⁴ (sd of the summed error).

**Fixed-point emulation (CHECK; `--fixed-point`; 60 PILOT samples per crop on the b = 10 lattice; raw: `RAW/t3_v2_checks/fixedpoint_C_subgrid.txt` for L ≥ 60 and `checks_B_…` for L = 45, `fixedpoint_A_no_subgrid.txt` for the rounding and guard-bit comparisons).**
- The whole pipeline of A2 is emulated in float64 with explicit quantisation after every product: frames, bond increments, CB, differences, saturating s, region/segment bits, quantised coefficients and Horner.
- It is compared with float64 evaluation of the smooth function at the **same lattice angles**, so only arithmetic and representation error is measured.
- Entries are the sd over samples of the pair-energy error δE (nats), round-to-nearest with 4 guard bits in the build, v2 grid with sub-grid:

| b_w | L=45 | L=60 | L=100 | L=120 | L=150 |
|---|---|---|---|---|---|
| 16 | 8.9e-2 | 1.1e-1 | 3.8e-1 | 4.9e-1 | 1.5 |
| 20 | 6.7e-3 | 9.3e-3 | 2.5e-2 | 3.3e-2 | 1.0e-1 |
| 22 | 1.8e-3 | 2.2e-3 | 6.4e-3 | 7.5e-3 | 2.6e-2 |
| 23 | 7.1e-4 | 1.1e-3 | 3.3e-3 | 3.9e-3 | 1.3e-2 |
| 24 | 4.0e-4 | 5.2e-4 | 1.4e-3 | 1.8e-3 | 6.3e-3 |
| 25 | 2.2e-4 | 2.4e-4 | 6.5e-4 | 9.7e-4 | 3.4e-3 |
| 26 | 9.6e-5 | 1.3e-4 | 3.9e-4 | 5.2e-4 | 1.5e-3 |
| 28 | 2.5e-5 | 4.8e-5 | 1.2e-4 | 1.7e-4 | 5.8e-4 |
| *classical table sd* | *3.0e-3* | *4.3e-3* | *4.6e-3* | *5.4e-3* | *9.9e-3* |

- The b_w = 16 row comes from the run without the sub-grid. It is geometry-dominated, so the sub-grid does not change it materially.
- **Move error.** The error in ΔE for single-angle moves of one lattice unit, δΔE = δE(x′) − δE(x), has the same scale as δE: sd 1.4×10⁻³ … 2.7×10⁻² at b_w = 22. This is the quantity the Metropolis coin sees.
- **Rounding convention (b_w = 20, no guard bits).**

  | | L=45 | L=60 | L=100 | L=120 | L=150 |
  |---|---|---|---|---|---|
  | round-to-nearest, sd | 9.7e-3 | 1.6e-2 | 9.8e-2 | 9.0e-2 | 2.9e-1 |
  | truncating multipliers, sd | 6.4e-2 | 6.7e-2 | 9.6e-1 | 7.0e-1 | 5.7 |
  | truncating multipliers, mean bias | −0.29 | −0.52 | −1.5 | −2.1 | −0.1 |

  **Round-to-nearest is a requirement**, and it is free (P3).
- **Guard bits.** Adding 4 guard bits to the build lowers the b_w = 20 sd from 9.7×10⁻³ to 6.7×10⁻³ (L=45) and from 2.9×10⁻¹ to 1.0×10⁻¹ (L=150), worth about 1.5 bits of b_w at large L. They cost ≤ 1% of G (§4.7).
- **Why b_w grows with L.** The coordinate integer bits grow as log₂(3.8L), rounding errors accumulate along the ~L-step prefix product, and n_p grows as L². The jump between L = 120 and 150 coincides with IX going from 9 to 10 bits.

**Choice of b_w (the criterion is stated so that others can apply their own).**
- For π̃ ∝ π·e^{−δE}, to second order KL(π‖π̃) ≈ Var_π(δE)/2, so TV(π, π̃) ≲ sd_π(δE)/2 by Pinsker (DERIVED). A constant offset in δE is irrelevant.
- **Central, "classical parity":** sd(δE) ≤ the classical 0.05 Å table's own sd at the same L. The quantum target is then no further from the smooth A80 function than the classical sampler's own target. This gives b_w = 22, 22, 23, 23, 24 at L = 45, 60, 100, 120, 150.
- **Generous, "TV ≲ 0.01":** sd(δE) ≤ 0.02 nats. This gives b_w = 20, 20, 22, 22, 23.
- L = 30 takes the L = 45 value. L = 200 is extrapolated by +1 bit (INFERENCE).
- The PILOT samples are from λ = 1 and are not equilibrated. Whether the error scale is the same at the λ ≈ 0.4–0.5 bottleneck is INFERENCE.
- **Representation fidelity is not a cost driver** (g = 1,024 + 64 costs < 2% more than g = 512). **Arithmetic precision is**, at ×1.2–1.9 on G.

### 3.3 Chain build (DERIVED from A11)

- Per residue, at b_w + 4 bits: 33·MUL + 1.5·(b_w+4)² + 24·ADD + QROAM(2^b, 5(b_w+4)) + QROAM(2^b, 2(b_w+4)) + 6·ADD(b_w). That is **2.7×10⁴ at L=100** (b_w = 23).
- Per structure: 7.1×10⁵ (L=30) to 6.2×10⁶ (L=200). Each oracle call does n_str builds and unbuilds.
- The **parallel-prefix (Hillis–Steele) scan used by the classical code** costs ⌈log₂ L⌉·L·36 multiplies per structure. It would add +32% to G(L=150).
- When Toffolis are rate-limited, use the sequential scan, or Brent–Kung (≈ 2L products, depth 2 log L) if depth matters with many factories.

### 3.4 Head terms (DERIVED from A14)

- Torsion: C_head = 2·u·[QROAM(2^b, 3b_c + 4) + QROAM(2^b, 3b_c + 5) + QROAM(216·(L−3), 9·b_c) + 12·b_c² + LOG]. That is ≈ 5.9×10⁴ at L=150, below 0.1% of G.
- Cartesian, at L=150: 5 head terms × 2 (old/new) × u × 5.3×10⁴ = 1.1×10⁶, and 3 CBs × 2 × u × 4.9×10⁴ = 5.8×10⁵. Together these are ~8% of the D3 step.

### 3.5 Oracle, coin and bookkeeping (DERIVED)

- **C_diff (torsion)** = n_str·C_E + 2·C_move + C_head + b_acc. C_move = n_ang·(2b + 1) is the quantum-indexed ±δ add on the angle register, done in place and undone.
- **C_coin** = 2·C_fun + 2·b_dif + 2·b_sm = **631**, with C_fun = (7 + 7)² + 40 + 7·3 + 2^{3.5} = 268 [A56 eq. 96]. The Metropolis min(1, ·) is handled by the sign bit of ΔE, as in [A56] §III E.1 steps 3–5.
- **C_F** = n_ang·(2b + 1) + 1 (move add and sign flip) = 1,156 (L=30) to 8,296 (L=200). For D3 it is L·(6·b_x + 1) + 1 = 2,911–19,401.
- **C_V + C_R** = 2·(4k + 2·b_sm − 13) + (k + 1) = 66–102.
- **In-oracle moves:** 4·C_move = 4,620–33,180 (torsion).
- **Sum of the non-pair bookkeeping: ≤ 4.2×10⁴ Toffolis, ≤ 5.3×10⁻⁴ of G** at every L = 30–200, for both designs. (v1 said "< 10⁴", which is wrong for C_F and C_move at large L.)

### 3.6 Qubitised step totals (DERIVED)

G_LHPST = 2·C_diff + C_coin + C_F + C_V + C_R. At L=150 (central, b_w = 24):

| design | C_diff | G |
|---|---|---|
| D2 | 3.75×10⁸ | 7.5×10⁸ |
| D1 | — | 1.8×10⁹ |
| D3 | 2.06×10⁷ | 4.1×10⁷ |

The full L-table is in §4.2.

### 3.7 Szegedy step totals (DERIVED from [A56] eq. 190)

- Torsion: C_direct = C_E + L·C_head/2 (the full energy, including all head terms) and M = 2·n_ang. The result is G_Sz = 2(M+1)·C_direct + O(M·C_fun).
- Cartesian: with the move index classical inside the state preparation, each ΔE_j uses per-pair classical-index tables. Then G_Sz = 2·M·C_diff with M = 6L.
- Szegedy also needs a second system register and M stored transition registers: + n_sys + M·(b_acc + 2·b_sm + b_fun) logical qubits [A56 eq. 191].

### 3.8 Cartesian design D3 (DERIVED from A14–A15)

At L=150 (central):

| part | Toffolis |
|---|---|
| read the 7-residue window by quantum index r, and unread it | 1.0×10⁵ |
| pair terms: 2 × 4(L−5) × 16,267 | 1.89×10⁷ |
| 3 CB recomputations | 5.8×10⁵ |
| 5 head terms | 1.1×10⁶ |
| bonds | 3.0×10⁴ |
| **C_diff** | **2.06×10⁷** |

- **Growth.** The QROAM term √(L·(g+64)·w) makes τ_D3 grow as ~L^{1/2}, and b_w also grows. The local exponents d log G_D3/d log L are:
  - central: 0.95, 1.21, 1.30 and 1.38 over 30–60, 60–100, 100–150 and 150–200;
  - generous: 1.03–1.43;
  - together, ~L^{1.0–1.4} over L = 30–200, tending to L^{1.5} asymptotically.
- D3 has two caveats:
  - its target is bond-relaxed (§2.2);
  - its per-step mixing is worse than a torsion move's. Its κ floor is already L/8 (κ_min), and stiff bonds limit the step size further (UNPROVEN in magnitude).
- D3's advantage in B over D2 disappears when κ_D3/κ_D2 ≥ (G_D2/G_D3)², which is 16 (L=30), 64 (60), 163 (100), 330 (150) and 542 (200) (DERIVED from S5).

### 3.9 Logical qubits (DERIVED)

- **Torsion.** n_L = n_ang·b (system) + 18·(b_w+4)·L (structure with stored frames and intermediate column; 6·b_w·L + 24·(b_w+4)·⌈√L⌉ when checkpointed) + 12·b_w + 4·b_c + QROAM ancilla (pair workspace) + 3·b_acc + move and coin registers + A_fun (= 2·b_sm + b_fun + 3 [A56 eq. 99]). D1 adds the Newton workspace b_w·(m + 4).
- **Cartesian.** n_L = 3L·b_x + 2·7·3·b_x (window) + ~52·b_w (CB/head workspace) + pair workspace (QROAM ancilla up to ~3,300) + registers.
- **Parallelism.** R-way factory parallelism needs R concurrent pair evaluations. That adds (R−1)·(12·b_w + 4·b_c + QROAM ancilla) qubits, about 550 per workspace for D2 and 3,400 for D3 at L=100. These are included in every R > 1 physical-qubit figure (§4.4, §4.6).

### 3.10 Physical qubits, wall-clock and error budget (DERIVED from H1–H5)

- t_step = G·t_T/R, with t_T = 170 µs.
- Physical qubits = 2(d+1)²·n_L + R·1.5×10⁵·(d/31)². This is the 2019 model of [T3-4], and [T3-6, T3-7] lower it by about an order of magnitude.
- **Memory errors.** d must satisfy n_L·(T/1 µs)·10^{−⌈d/2+1⌉} ≤ 0.1, the 0.9 success target of [A56]. When d > 31 is needed, t_T = 5.5·d µs [B46 eq. 6, T3-3]. §4.6 iterates this to self-consistency.
- **Magic-state errors (added in v2).** A break-even run of N_Toff = c_q·√(κB)·G Toffolis needs ε_CCZ·N_Toff ≲ 0.1.
  - The [T3-3] factory at the Sanders parameters yields ~10¹⁰ CCZ states before an error, and ~10¹² with a ~20% larger footprint. It therefore supports N_Toff ≲ 10⁹–10¹¹.
  - Every break-even run in §4.6 needs N_Toff = 3.5×10¹² … 9.8×10¹⁷, i.e. ε_CCZ ≤ 3×10⁻¹⁴ … 10⁻¹⁹.
  - That needs a further distillation level or larger distances, which are not modelled. **All physical-qubit and time figures at break-even are lower bounds.**

### 3.11 Break-even (DERIVED; S5)

- **Algebra.** S5 is the M ↦ √(κ·N_C) specialisation of [B46] eq. 12. The quantum primitive is one walk step and the classical primitive one energy+gradient evaluation.
- **κ floor (DERIVED).** N_C is the best classical sampler's cost. Running P_W itself on a classical computer is one candidate, with cost N_W·t_W^cl in time, i.e. N_W·t_W^cl/t_C energy+gradient units. Hence N_C ≤ N_W·t_W^cl/t_C and κ = N_W/N_C ≥ t_C/t_W^cl =: κ_min.
  - Pair-term counting sets κ_min. It treats an energy-only term as costing as much as an energy+gradient term, which favours the quantum side. The reverse-mode gradient makes t_C 2–4× an energy, so the true floors are higher.
  - Torsion: one energy+gradient touches 2·n_p ≈ L² terms. One single-angle Metropolis step re-evaluates the ~L²/6 straddling pairs on average, in 2 channels at old and new positions, i.e. 2L²/3 terms. So κ_min ≈ 1.5, and 3 with cached per-pair energies.
  - D3: one step re-evaluates 2·4(L−5) terms. So κ_min = n_p/(4(L−5)) ≈ L/8, and 2× that with caching.
- **κ growing with N_C (DERIVED algebra; INFERENCE for α).** If κ = κ₀·N_C^α, then T_Q ∝ N_C^{(1+α)/2} and

  ```
  B = ( c_q·√κ₀ · S·G·t_T/(R·t_C) )^{2/(1−α)}
  ```

  - At α = 0.5 the exponent doubles. At α → 1 (lifting attains its full square root) there is no break-even at all.
  - D2 central at L=100, S = 10³, R = 100 gives B = 4.3×10¹⁷, 3.3×10²³ and 1.9×10³⁵ for α = 0, 0.25 and 0.5.
  - The square-root gain is relative to the quantised **reversible** chain. Lifted classical chains recover part or all of it (T2c).
- **No-cloning.** Each quantum sample is a separate walk or anneal run. The classical side amortises burn-in and produces a sample every N_C evaluations. For a soft readout needing tens of samples, the classical side runs tens of chains in parallel at no extra wall-clock cost. So S ≥ 10–100 is natural even without a cluster (INFERENCE). This is why S = 1 is only a bounding device.

---

## 4. Numbers (all DERIVED from §3 under A1–A15, H1–H5 and C1–C5; `T3_resource_model.py`)

### 4.1 Primitive and per-term costs (central, L=100, b_w = 23)

- sqdist 1,760; Horner (p=3) 1,656; √ (P6, n² convention, m=2) 6,731 (HRS convention 14,981); −log 1,230; C_fun 268; coin per step 631.
- Build 2.7×10⁴ per residue (at b_w + 4 = 27 bits).
- Head (torsion) ≈ 5.9×10⁴ per step at L=150. CB (Cartesian) 4.9×10⁴ each. Head (Cartesian) 5.3×10⁴ each.
- Per-term τ: see S4.
- Generous per-term τ: D2 3,717–5,040; D3 6,668–14,422; D1 9,944–14,020 (L = 30–200).

### 4.2 Toffolis per walk step, G(L)

**Central** (b_w = 22, 22, 23, 24, 25).

| design | step | L=30 | L=60 | L=100 | L=150 | L=200 |
|---|---|---|---|---|---|---|
| D1 | qubitised | 5.8e7 | 2.4e8 | 7.3e8 | 1.8e9 | 3.5e9 |
| D1 | Szegedy | 3.3e9 | 2.8e10 | 1.4e11 | 5.4e11 | 1.4e12 |
| D2 | qubitised | 2.7e7 | 1.0e8 | 3.1e8 | 7.5e8 | 1.4e9 |
| D2 | Szegedy | 1.6e9 | 1.3e10 | 6.3e10 | 2.3e11 | 5.8e11 |
| D3 | qubitised | 6.8e6 | 1.3e7 | 2.4e7 | 4.1e7 | 6.1e7 |
| D3 | Szegedy | 1.0e9 | 3.2e9 | 8.8e9 | 2.0e10 | 3.8e10 |
| D2 soft-bin basis | qubitised | 5.6e7 | 2.3e8 | 7.0e8 | 1.7e9 | 3.3e9 |
| D3 soft-bin basis | qubitised | 9.6e6 | 1.8e7 | 3.2e7 | 5.1e7 | 7.4e7 |

**Generous** (b_w = 20, 20, 22, 23, 24; u = 1.5; SQ = b_w²/2; energy-carrying register O-1).

| design | step | L=30 | L=60 | L=100 | L=150 | L=200 |
|---|---|---|---|---|---|---|
| D1 | qubitised | 1.8e7 | 7.1e7 | 2.4e8 | 5.8e8 | 1.1e9 |
| D2 | qubitised | 8.1e6 | 3.0e7 | 9.3e7 | 2.2e8 | 4.2e8 |
| D3 | qubitised | 4.4e6 | 9.0e6 | 1.8e7 | 3.2e7 | 4.8e7 |
| D2 | Szegedy | 9.8e8 | 7.3e9 | 3.8e10 | 1.3e11 | 3.4e11 |
| D3 | Szegedy | 5.7e8 | 1.8e9 | 5.2e9 | 1.2e10 | 2.2e10 |

**Literature calibration (THEORETICAL [A56]).** One qubitised annealing step costs 6.7×10²–4.8×10³ Toffolis for SK N = 64–1024 (Table VIII) and 2.0×10⁴–4.6×10⁶ for LABS N = 64–1024 (Table IX).
- D2 central at L=100 is 259× the LABS-512 step; at L=150 it is 625×.
- The earlier I(agent) sketch (`lit_A_sampling.md` §3.9) put the step at 10⁶–10⁸ Toffolis at N = 100. This derivation lands inside it for D3 (2.4×10⁷) and above it for D2 (3.1×10⁸).

### 4.3 Logical qubits (central)

| design | step | L=30 | L=60 | L=100 | L=150 | L=200 |
|---|---|---|---|---|---|---|
| D1/D2 | qubitised, frames stored (as costed) | 1.5e4 | 3.0e4 | 5.1e4 | 7.9e4 | 1.1e5 |
| D1/D2 | qubitised, √L checkpoints (+28% … +4.6% G) | 9.0e3 | 1.5e4 | 2.3e4 | 3.4e4 | 4.5e4 |
| D1/D2 | Szegedy | 2.3e4 | 4.5e4 | 7.7e4 | 1.2e5 | 1.6e5 |
| D3 | qubitised | 5.2e3 | 7.4e3 | 1.0e4 | 1.3e4 | 1.7e4 |
| D3 | Szegedy | 1.8e4 | 3.2e4 | 5.2e4 | 7.5e4 | 9.9e4 |

For comparison, [A56] Tables VIII–IX use 577 (SK-512) and 598 (LABS-512) logical qubits.

### 4.4 Wall-clock per qubitised step, physical qubits, code distance (central; 2019 surface-code model)

| design | L | G | t_step R=1 | R=10 | R=100 | R=10³ | n_L | phys. (1 factory, d=31) | phys. (100 factories + 99 pair workspaces, d=31) | d for one step |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 | 30 | 5.8e7 | 2.7 h | 16 min | 1.6 min | 9.8 s | 1.5e4 | 3.2e7 | 1.5e8 | 29 |
| D1 | 100 | 7.3e8 | 1.4 d | 3.5 h | 21 min | 2.1 min | 5.1e4 | 1.1e8 | 2.3e8 | 31 |
| D1 | 200 | 3.5e9 | 6.8 d | 16 h | 1.6 h | 9.8 min | 1.1e5 | 2.2e8 | 3.5e8 | 33 |
| D2 | 30 | 2.7e7 | 1.3 h | 7.7 min | 46 s | 4.6 s | 1.5e4 | 3.2e7 | 1.7e8 | 27 |
| D2 | 60 | 1.0e8 | 5.0 h | 30 min | 3.0 min | 18 s | 3.0e4 | 6.2e7 | 2.0e8 | 29 |
| D2 | 100 | 3.1e8 | 15 h | 1.5 h | 8.8 min | 53 s | 5.1e4 | 1.1e8 | 2.3e8 | 31 |
| D2 | 150 | 7.5e8 | 1.5 d | 3.5 h | 21 min | 2.1 min | 7.9e4 | 1.6e8 | 2.9e8 | 33 |
| D2 | 200 | 1.4e9 | 2.8 d | 6.8 h | 41 min | 4.1 min | 1.1e5 | 2.2e8 | 3.6e8 | 33 |
| D3 | 30 | 6.8e6 | 19 min | 1.9 min | 12 s | 1.2 s | 5.2e3 | 1.1e7 | 4.2e8 | 25 |
| D3 | 60 | 1.3e7 | 37 min | 3.7 min | 22 s | 2.2 s | 7.4e3 | 1.5e7 | 5.7e8 | 27 |
| D3 | 100 | 2.4e7 | 1.2 h | 6.9 min | 41 s | 4.1 s | 1.0e4 | 2.1e7 | 7.3e8 | 27 |
| D3 | 150 | 4.1e7 | 2.0 h | 12 min | 70 s | 7.0 s | 1.3e4 | 2.8e7 | 9.0e8 | 27 |
| D3 | 200 | 6.1e7 | 2.9 h | 17 min | 1.7 min | 10 s | 1.7e4 | 3.4e7 | 1.1e9 | 29 |

- The R = 100 column now includes the 99 concurrent pair workspaces that §3.9 requires. v1 omitted them and understated this column by 1.8–19×.
- For D3 the QROAM ancillae of the workspaces dominate. Sharing them is open (G-8).
- Szegedy step wall-clock at R = 1: D2 L=150 is 2.3×10¹¹ × 170 µs = **1.2 yr**; D1 L=200 is 7.5 yr.

### 4.5 Break-even B(L) with κ = κ_min, c_q = 1 and the PLACEHOLDER t_C

B is in energy+gradient evaluations per independent sample. The break-even runtime per sample, T*, is in parentheses. κ_min = 1.5 (torsion) and 3.8, 7.5, 12.5, 18.8, 25 (D3).

**Central.**

| design | S | R | L=30 | L=60 | L=100 | L=150 | L=200 |
|---|---|---|---|---|---|---|---|
| D1 | 1 | 100 | 1.8e12 (5.1 yr) | 2.0e12 (22 yr) | 2.4e12 (74 yr) | 2.8e12 (200 yr) | 3.3e12 (420 yr) |
| D1 | 10³ | 100 | 1.8e18 | 2.0e18 | 2.4e18 | 2.8e18 | 3.3e18 |
| D2 | 1 | 1 | 4.0e15 (1.1e4 yr) | 3.8e15 | 4.3e15 | 4.9e15 | 5.7e15 (7.1e5 yr) |
| D2 | 1 | 100 | 4.0e11 (1.1 yr) | 3.8e11 (4.3 yr) | 4.3e11 (14 yr) | 4.9e11 (35 yr) | 5.7e11 (71 yr) |
| **D2** | **10³** | **100** | **4.0e17 (1.1e3 yr)** | **3.8e17** | **4.3e17 (1.4e4 yr)** | **4.9e17** | **5.7e17 (7.1e4 yr)** |
| D2 | 10³ | 10³ | 4.0e15 (11 yr) | 3.8e15 (43 yr) | 4.3e15 (135 yr) | 4.9e15 (350 yr) | 5.7e15 (710 yr) |
| D3 | 1 | 100 | 6.4e10 (66 d) | 3.0e10 (122 d) | 2.2e10 (252 d) | 1.9e10 (1.3 yr) | 1.7e10 (2.2 yr) |
| D3 | 10³ | 100 | 6.4e16 (181 yr) | 3.0e16 | 2.2e16 (690 yr) | 1.9e16 | 1.7e16 (2.2e3 yr) |
| D3 | 10³ | 10³ | 6.4e14 (1.8 yr) | 3.0e14 (3.3 yr) | 2.2e14 (6.9 yr) | 1.9e14 (13 yr) | 1.7e14 (22 yr) |

**Generous.**

| design | S | R | L=30 | L=60 | L=100 | L=150 | L=200 |
|---|---|---|---|---|---|---|---|
| D1 | 1 | 100 | 1.7e11 (173 d) | 1.7e11 (1.9 yr) | 2.5e11 (7.8 yr) | 2.9e11 (21 yr) | 3.5e11 (43 yr) |
| D1 | 10³ | 10³ | 1.7e15 (4.7 yr) | 1.7e15 | 2.5e15 | 2.9e15 | 3.5e15 (434 yr) |
| D2 | 1 | 100 | 3.6e10 (37 d) | 3.0e10 (125 d) | 3.8e10 (1.2 yr) | 4.3e10 (3.0 yr) | 4.8e10 (6.0 yr) |
| **D2** | **10³** | **100** | **3.6e16 (102 yr)** | **3.0e16 (341 yr)** | **3.8e16 (1.2e3 yr)** | **4.3e16 (3.0e3 yr)** | **4.8e16 (6.0e3 yr)** |
| D2 | 10³ | 10³ | 3.6e14 (1.0 yr) | 3.0e14 (3.4 yr) | 3.8e14 (12 yr) | 4.3e14 (30 yr) | 4.8e14 (60 yr) |
| D3 | 1 | 100 | 2.7e10 (28 d) | 1.4e10 (57 d) | 1.2e10 (141 d) | 1.1e10 (284 d) | 1.1e10 (1.3 yr) |
| D3 | 10³ | 100 | 2.7e16 (76 yr) | 1.4e16 (157 yr) | 1.2e16 (387 yr) | 1.1e16 (776 yr) | 1.1e16 (1.3e3 yr) |
| D3 | 10³ | 10³ | 2.7e14 (276 d) | 1.4e14 (1.6 yr) | 1.2e14 (3.9 yr) | 1.1e14 (7.8 yr) | 1.1e14 (13 yr) |

- **Reference line, κ = 1 (infeasible, below the floor), S = 1, R = 100:** D2 generous 2.0–3.2×10¹⁰; D3 generous 4.2×10⁸–7.1×10⁹.
- The full grid, S ∈ {1, 10³} × R ∈ {1, 100, 10³} for all designs, is printed by the script.
- **Rescaling rules (DERIVED from S5):**
  - B ∝ κ·c_q²·S²·R⁻²·t_T²·t_C⁻² and T* ∝ κ·c_q²·S·R⁻²·t_T²·t_C⁻¹;
  - c_q = 10 multiplies every entry by 10², and c_q = 90 by 8.1×10³.
- **Measured t_C (PILOT power-law fit t_C ∝ L^{1.48}), κ_min, c_q = 1, S = 1, R = 100.** Multiply by 10⁶ for S = 10³. B now grows with L:

  | design | L=30 | L=60 | L=100 | L=150 | L=200 |
  |---|---|---|---|---|---|
  | D2 central | 3.6e10 | 7.0e10 | 1.4e11 | 2.4e11 | 3.7e11 |
  | D2 generous | 3.3e9 | 5.6e9 | 1.2e10 | 2.1e10 | 3.2e10 |
  | D3 generous | 2.4e9 | 2.6e9 | 3.9e9 | 5.4e9 | 7.0e9 |

- **Quantised-HMC variant (INFERENCE; D2 energy).**
  - Quantising the HMC kernel itself gives κ = 1/n_leap = 1/8 relative to per-gradient accounting, since one HMC step costs n_leap gradient evaluations and N_C is counted in gradients.
  - It costs G ≈ 2·n_leap·c_grad·C_E with c_grad = 3. c_grad is an unverified assumption (G-6).
  - The result is G = 3.2×10⁸ (L=30) … 1.7×10¹⁰ (L=200) and B = 4.5–6.8×10¹⁶ (S = R = 1). That is ~6× worse than D2 at κ = 3 (7.5×10¹⁵–1.1×10¹⁶), and better than D2 only if κ_D2 ≳ 18.
  - **Two open costs (UNPROVEN).**
    - A coherent HMC transition |x⟩ ↦ Σ_y √P(x,y)|y⟩ must uncompute the momentum register, and p ↦ y is not injective for fixed x. G above ignores that garbage.
    - HMC with Gaussian momentum refresh is not a symmetric finite-move-set chain of the kind LHPST covers, so applying LHPST to it is INFERENCE.

### 4.6 H-008 B-clause grid, hardware envelope, pilot distance and self-consistent distance (DERIVED)

**B-clause grid at L = 100** (placeholder t_C, R = 100, t_T = 170 µs; "ok" = B ≤ 10¹², "F" = B > 10¹⁵; R = 10³ divides every entry by 10²).

| design | params | κ | S=1, c_q=1 | S=1, c_q=10 | S=1, c_q=90 | S=10³, c_q=1 | S=10³, c_q=10 | S=10³, c_q=90 | S_max (c_q=1) for B ≤ 10¹² |
|---|---|---|---|---|---|---|---|---|---|
| D1 | central | 1.5 | 2.4e12 | 2.4e14 | 1.9e16 F | 2.4e18 F | 2.4e20 F | 1.9e22 F | 0.65 |
| D1 | generous | 1.5 | 2.5e11 ok | 2.5e13 | 2.0e15 F | 2.5e17 F | 2.5e19 F | 2.0e21 F | 2.0 |
| D2 | central | 1.5 | 4.3e11 ok | 4.3e13 | 3.5e15 F | 4.3e17 F | 4.3e19 F | 3.5e21 F | 1.5 |
| D2 | central | 50 | 1.4e13 | 1.4e15 F | 1.2e17 F | 1.4e19 F | 1.4e21 F | 1.2e23 F | 0.26 |
| D2 | central | L = 100 | 2.9e13 | 2.9e15 F | 2.3e17 F | 2.9e19 F | 2.9e21 F | 2.3e23 F | 0.19 |
| D2 | generous | 1.5 | 3.8e10 ok | 3.8e12 | 3.1e14 | 3.8e16 F | 3.8e18 F | 3.1e20 F | 5.1 |
| D2 | generous | 50 | 1.3e12 | 1.3e14 | 1.0e16 F | 1.3e18 F | 1.3e20 F | 1.0e22 F | 0.89 |
| D3 | central | 12.5 | 2.2e10 ok | 2.2e12 | 1.8e14 | 2.2e16 F | 2.2e18 F | 1.8e20 F | 6.7 |
| D3 | generous | 12.5 | 1.2e10 ok | 1.2e12 | 1.0e14 | 1.2e16 F | 1.2e18 F | 1.0e20 F | 9.0 |
| D3 | generous | L = 100 | 9.9e10 ok | 9.9e12 | 8.0e14 | 9.9e16 F | 9.9e18 F | 8.0e20 F | 3.2 |

The rows omitted here (D1 at κ ∈ {50, L}, D2 generous at κ = L, D3 central at κ ∈ {50, L}, D3 generous at κ = 50) are printed by the script and change no conclusion.

**Hardware envelope at L = 100** (κ_min, c_q = 1). The effective Toffoli time is t_T/R.

| design | params | S | 170 µs, R=1 | 170 µs, R=100 | 170 µs, R=10³ | 10 µs, R=100 | 1 µs, R=100 (10 ns effective) |
|---|---|---|---|---|---|---|---|
| D2 | central | 10³ | 4.3e21 | 4.3e17 (1.4e4 yr) | 4.3e15 (135 yr) | 1.5e15 (47 yr) | 1.5e13 (170 d) |
| D2 | generous | 10³ | 3.8e20 | 3.8e16 (1.2e3 yr) | 3.8e14 (12 yr) | 1.3e14 (4.1 yr) | 1.3e12 (15 d) |
| D3 | central | 10³ | 2.2e20 | 2.2e16 (690 yr) | 2.2e14 (6.9 yr) | 7.6e13 (2.4 yr) | 7.6e11 (8.7 d) |
| D3 | generous | 10³ | 1.2e20 | 1.2e16 (387 yr) | 1.2e14 (3.9 yr) | 4.3e13 (1.3 yr) | 4.3e11 (4.9 d) |
| D2 | generous | 1 | 3.8e14 | 3.8e10 (1.2 yr) | 3.8e8 (4.4 d) | 1.3e8 (1.5 d) | 1.3e6 (22 min) |
| D3 | generous | 1 | 1.2e14 | 1.2e10 (141 d) | 1.2e8 (1.4 d) | 4.3e7 (12 h) | 4.3e5 (7 min) |

- A 1 ns effective Toffoli (t_T = 1 µs with R = 10³) combines two independent optimistic scenarios and is outside every published model. It is printed by the script but not used.
- The **practical L0 verdict does not rest on the hardware cap.** At 10 ns effective Toffolis and S = 10³, break-even still needs N_C ≥ 4×10¹¹ (D3 generous) or 1.3×10¹² (D2 generous). That is ≥ 4.7×10⁶× the pilot's 95% PT bounds (L=100), before c_q ≥ 10 multiplies B by ≥ 10².

**Distance to the pilot** (95% bounds = production gradient evaluations / 3; κ_min; c_q = 1).

| L | scans (0 round trips) | production grad evals | 95% bound | D3 gen S=1 R=100 (placeholder t_C): B / ratio | same, PILOT t_C | D2 gen S=10³ R=10³: ratio | D2 cen S=10³ R=100: ratio |
|---|---|---|---|---|---|---|---|
| 45 | 1,500 | 3.9e5 | 1.3e5 | 1.8e10 / 1.3e5 | 2.0e9 / 1.5e4 | 2.5e9 | 2.9e12 |
| 60 | 1,200 | 3.4e5 | 1.1e5 | 1.4e10 / 1.2e5 | 2.9e9 / 2.6e4 | 2.7e9 | 3.4e12 |
| 100 | 800 | 2.7e5 | 9.1e4 | 1.2e10 / 1.4e5 | 5.6e9 / 6.2e4 | 4.2e9 | 4.7e12 |
| 120 | 600 | 2.0e5 | 6.5e4 | 1.1e10 / 1.7e5 | 4.0e9 / 6.1e4 | 5.8e9 | 6.6e12 |
| 150 | 500 | 1.7e5 | 5.7e4 | 1.1e10 / 1.9e5 | 4.4e9 / 7.7e4 | 7.5e9 | 8.6e12 |

**Self-consistent code distance and CCZ budget** (κ_min, c_q = 1, stored frames with G to match, R − 1 pair workspaces).
- d is raised until the run of length T* meets the 0.9 memory-success target with the corrected H3. Then t_T = max(170 µs, 5.5·d µs) is re-applied, three iterations.
- "LB" means the required ε_CCZ is below the ~10⁻¹² that [T3-3] reaches with a ~20% larger factory, so the qubit count is a lower bound.

| design | params | L | S | R | n_L | d | t_T (µs) | B | T* | N_Toff per run | ε_CCZ needed | physical qubits |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D2 | central | 60 | 1 | 100 | 9.1e4 | 39 | 214 | 6.0e11 | 6.8 yr | 1.0e14 | 1.0e-15 | 3.1e8 LB |
| D2 | central | 150 | 1 | 100 | 1.4e5 | 41 | 225 | 8.7e11 | 61 yr | 8.6e14 | 1.2e-16 | 5.1e8 LB |
| D2 | central | 150 | 10³ | 100 | 1.4e5 | 47 | 258 | 1.1e18 | 8.1e4 yr | 9.8e17 | 1.0e-19 | 6.6e8 LB |
| D2 | generous | 60 | 1 | 100 | 8.3e4 | 37 | 204 | 4.3e10 | 178 d | 7.6e12 | 1.3e-14 | 2.6e8 LB |
| D2 | generous | 150 | 1 | 100 | 1.3e5 | 39 | 214 | 6.8e10 | 4.8 yr | 7.0e13 | 1.4e-15 | 4.4e8 LB |
| D2 | generous | 150 | 10³ | 100 | 1.3e5 | 45 | 248 | 9.0e16 | 6.4e3 yr | 8.1e16 | 1.2e-18 | 5.9e8 LB |
| D3 | central | 150 | 1 | 100 | 4.3e5 | 39 | 214 | 3.0e10 | 2.1 yr | 3.1e13 | 3.2e-15 | 1.4e9 LB |
| D3 | central | 150 | 10³ | 100 | 4.3e5 | 45 | 248 | 4.0e16 | 2.8e3 yr | 3.6e16 | 2.8e-18 | 1.9e9 LB |
| D3 | generous | 60 | 1 | 100 | 2.5e5 | 37 | 204 | 2.0e10 | 82 d | 3.5e12 | 2.9e-14 | 7.5e8 LB |
| D3 | generous | 150 | 1 | 100 | 4.2e5 | 39 | 214 | 1.8e10 | 1.2 yr | 1.8e13 | 5.5e-15 | 1.4e9 LB |
| D3 | generous | 150 | 10³ | 100 | 4.2e5 | 45 | 248 | 2.3e16 | 1.7e3 yr | 2.1e16 | 4.8e-18 | 1.8e9 LB |

- Self-consistency raises B and T* by (t_T/170 µs)² = 1.4–2.3×.
- The corrected surface-code exponent (H3) lowers the required d by ~4 relative to v1 at equal n_L and T. The larger n_L (stored frames, workspaces) and the longer T* of v2 push it back up.
- The five rows omitted here (L = 60 at S = 10³ for all four design variants, and D3 central at L = 60, S = 1) are printed by the script and are also LB.

### 4.7 Sensitivity of G_LHPST(D2 central, L=150) = 7.5×10⁸ (b_w = 24) (DERIVED)

| change | G | ratio |
|---|---|---|
| b_w = 16 / 20 / 22 / 28 | 3.7e8 / 5.5e8 / 6.4e8 / 9.9e8 | 0.50 / 0.73 / 0.86 / 1.32 |
| g = 512 / 2048 (+64 sub-grid) | 7.3e8 / 7.7e8 | 0.98 / 1.03 |
| u = 1.5 | 5.9e8 | 0.78 |
| SQ = n²/2 | 6.0e8 | 0.80 |
| b = 8 / 12 | 7.5e8 / 7.5e8 | 1.00 / 1.00 |
| b_acc = 32 / 48 | 7.5e8 / 7.5e8 | 1.00 / 1.00 |
| guard bits 0 / 8 | 7.4e8 / 7.6e8 | 0.99 / 1.01 |
| energy-carrying register (O-1) | 3.8e8 | 0.50 |
| √L checkpointed frames | 8.0e8 | 1.06 |
| parallel-prefix build (as in the classical code) | 9.9e8 | 1.32 |
| HRS multiplier convention for every multiply and the Newton iteration (P3, P6) | 1.6e9 | 2.16 |

- Precision against v1: central ×1.22–1.50 (vs b_w = 20). Generous ×1.41–1.91 (vs b_w = 16).

---

## 5. Literature

### 5.1 Keys in `BIBLIOGRAPHY.md` used here, with what was checked (arXiv PDFs parsed)

- **[A56] = [C64] Sanders, Berry, Costa, Tessler, Wiebe, Gidney, Neven, Babbush, PRX Quantum 1, 020312 (2020), arXiv 2007.07391.** Checked:
  - Tables III, IV, VI, VII, VIII and IX;
  - eqs (93)–(100) (QROM-interpolated function evaluation; "The Toffoli cost of looking up one of g different possible values … is g − 2"; output-width independence);
  - eq. (190) (Szegedy step) and eqs (192)–(200) (LHPST block encoding), with eq. (214) (Table VI) for bit-flip moves;
  - §III E.1 (compute ΔE and arcsin once, retain through F, cost 2C_diff + 2C_fun + 2b_dif + O(1));
  - §IV: 170 µs and 150,000 physical qubits per Toffoli factory, d = 31, 1 µs cycles; SK-512 qubitised step 2.6×10³ Toffolis, 577 logical qubits, 8.1×10³ steps per hour; LABS-512 1.2×10⁶ Toffolis per step; "the Szegedy walk approach is strictly less efficient than the qubitized variant"; b = 20 and b_fun = b_sm = 7.
- **[B46] = [A57] Babbush, McClean, Newman, Gidney, Boixo, Neven, PRX Quantum 2, 010103 (2021), arXiv 2011.04149.** Checked:
  - eqs (1)–(5) (break-even with P cores and speedup S);
  - eq. (6), verbatim "t_G = 30 × 5.5 × 1 µs ≈ 170 µs"; eq. (7) t_Q = 170 µs·G;
  - eq. (12) (R-fold faster distillation) and **Table II** (R = 10, 10², 10³ against S = 10³; "R = 10 could be reached by using ten Toffoli factories if routing were very efficient");
  - "only by a factor that is between about ten and one-hundred";
  - the SA example (t_Q = 440 ms, t_C = 7 ns); S = 10³ default and "S = 10⁶ in practice" for SA.
- **[A55] = [B32] Lemieux, Heim, Poulin, Svore, Troyer, Quantum 4, 287 (2020), arXiv 1910.01659.** Checked:
  - U_W = R V† B† F B V (eq. 25) and eqs 23–24 (bit-flip moves, isometry |x⟩|y⟩ → |x⟩|x·y⟩);
  - Table 1 (the Boltzmann coin is exponential in 2^{|N_j|});
  - §2.4 ("The complexity of the Boltzmann coin does scale exponentially with the sparsity parameters");
  - §4 (the Janus comparison: a quadratic speedup needs ~1 ns logical gates).
- **[A59] Häner, Roetteler, Svore, arXiv 1805.12445 (2018).** Checked:
  - App. A–B: the fixed-point multiplication T_mul(n,p) and polynomial evaluation T_poly;
  - App. C: Newton inverse square root, T_iter = 5T_mul + 2T_add, T_invsqrt(n,m,p), qubits n(m+4). The count is an upper bound and excludes iterate uncomputation;
  - App. D: arcsine via polynomial plus inverse square root.
- **[A60] Babbush, Gidney, Berry, Wiebe, McClean, Paler, Fowler, Neven, PRX 8, 041015 (2018), arXiv 1805.03662.** **The QROM cost claim is VERIFIED** from the text: "our implementation of QROM has T complexity of 4L − 4 with no dependence on the word length"; unary iteration "has a T-count of 4L − 4". This closes `BIBLIOGRAPHY.md` unverified lead #55.
- **[F59] Berry, Gidney, Motta, McClean, Babbush, Quantum 3, 208 (2019), arXiv 1902.02134.** Checked App. C: QROAM compute ⌈d/k⌉ + M(k−1) Toffolis with (k−1)M ancillae; uncompute ⌈d/k⌉ + k.
- **[A14] Chen, Lovász, Pak (STOC 1999).** Used only for the statement that lifting gains at most a square root in mixing time and attains it on some chains, as usually stated (C3). The bibliography verifies this key as an ACM listing only, and the bound was not re-read this session. [A15] and [A18] are background for lifting.
- Background, not used numerically: [A1], [A8], [A31] for walk and QSA statements (via T2), and [A44] for continuous samplers.

### 5.2 New keys [T3-n], verified in the T3 sessions and not yet in `BIBLIOGRAPHY.md`

Titles were verified via the arXiv export API or abstract pages, and the PDFs parsed where numbers are quoted.

- **[T3-1] C. Gidney, "Halving the cost of quantum addition," Quantum 2, 74 (2018), arXiv 1709.06648.** Checked: n-bit adder T-count 4n − 4 via temporary logical-AND ("four T gates to compute … zero T gates to later erase"); controlled adder "from 21n + O(1) … to 8n + O(1)".
- **[T3-2] G. H. Low, V. Kliuchnikov, L. Schaeffer, "Trading T gates for dirty qubits in state preparation and unitary synthesis," arXiv 1812.00954.** Checked: SelectSwap data-lookup T complexity O(λb + N/λ), minimised at O(√(Nb)).
- **[T3-3] C. Gidney, A. G. Fowler, "Efficient magic state factories with a catalyzed |CCZ⟩ → 2|T⟩ transformation," arXiv 1812.01238 (Quantum 2019).** Checked (PDF parsed, v2 session):
  - footprint 12d×6d and "one |CCZ⟩ every 5.5d surface code cycles";
  - "Assuming a physical gate error rate of 10⁻³, our CCZ factory can produce ∼10¹⁰ states on average before an error occurs … the mean number of states until failure can be increased to ∼10¹² by increasing the factory footprint ∼20%";
  - distances 7 (level-0 injection), 15 (level 1) and 31 (everything else).
- **[T3-4] C. Gidney, M. Ekerå, "How to factor 2048 bit RSA integers in 8 hours using 20 million noisy qubits," arXiv 1905.09749.** Checked (PDF parsed, v2 session):
  - §2.13: "for a physical gate error rate of 10⁻³, the probability of error in a logical qubit of distance d, per surface code cycle, is approximately 10^{−⌈d/2+1⌉}". The worked example 10^{−⌈27/2+1⌉}·226·63·0.75·25·10⁹ ≈ 27% confirms it;
  - §2.14: "a logical qubit covers 2(d + 1)² physical qubits".
  - v1 miscopied the exponent.
- **[T3-5] C. Gidney, "Windowed quantum arithmetic," arXiv 1905.07682.** Title verified only. Not used numerically. It is an optimisation lead for the multiply-dominated pair term (G-5).
- **[T3-6] C. Gidney, N. Shutty, C. Jones, "Magic state cultivation: growing T states as cheap as CNOT gates," arXiv 2409.17595.** Checked (abstract, v2 session): "uses roughly the same number of physical gates as a lattice surgery CNOT gate of equivalent reliability"; logical error 2·10⁻⁹ at 10⁻³ uniform depolarizing noise, 4·10⁻¹¹ at 5·10⁻⁴; "an order of magnitude fewer qubit-rounds". Not used numerically.
- **[T3-7] C. Gidney, "How to factor 2048 bit RSA integers with less than a million noisy qubits," arXiv 2505.15917.** Checked (abstract, v2 session): fewer than one million noisy qubits, under one week, 0.1% gate error, 1 µs cycle, 10 µs reaction time; uses yoked surface codes and magic state cultivation. Not used numerically.

### 5.3 Unverified

None of the numbers above rests on an unverified source. [A14]'s "at most a square root" is used only qualitatively (C3, §3.11). The surface-code scaling of H3 is taken from [T3-4] as its authors state it, including their own attribution to an earlier reference. We did not re-derive it.

---

## 6. Scope and what is NOT claimed

- **Not a compiled circuit.** G(L) is a leading-order count built from published primitive costs and the labelled assumptions.
  - Three sub-costs are modelled, not compiled: −log, atan2, and the frame and CB arithmetic (INFERENCE).
  - The fixed-point emulation checks **numerical fidelity** of the formats in A2. It is not a circuit simulation. No simulator number is converted to runtime.
- **Not a lower bound.** Cleverer arithmetic could lower G by small constant factors: windowed arithmetic [T3-5], shared subexpressions, better pebbling, a smarter uncomputation schedule, or mixed precision per register. The central → generous spread is ~3.3× on D2. Nothing here excludes a further ~10×.
  - The only floor used is the conditional squaring floor of §0 item 9, for the move-oblivious torsion class.
  - A 10³× reduction would need a structurally different oracle, not better arithmetic (INFERENCE from S2: 3 squarings + 3 multiplies per term are already the core).
- **Not a speedup claim.** Walk-step counts assume the quadratic speedup relative to the *quantised reversible* chain (T2; [A1, A8, A31]). That is not a speedup relative to the best classical algorithm (κ, C3). c_q = 1 and S = 1 are bounding devices, not estimates.
- **The LHPST ±δ extension is INFERENCE** (§2.3), not a literature result.
- **D3 does not sample the A80 posterior.** It samples a bond-relaxed variant. Its break-even numbers are optimistic bounds for a different target.
- **Precision.** b_w is validated on PILOT λ = 1 samples at L ≤ 150 against a stated criterion. L = 200 is extrapolated. Coin precision for detailed balance is not analysed (G-3).
- **Classical side.** t_C is a PLACEHOLDER. The PILOT and quick timings are calibration only, not the G1 measurement. The quick timing ran on a machine loaded with G1 jobs.
- **Hardware.**
  - Physical-qubit and time figures inherit the p = 10⁻³ superconducting surface-code assumptions of [A56, B46, T3-4], the 2019 model.
  - At break-even they are **lower bounds**, because the required CCZ fidelity exceeds that of the assumed factory (§3.10).
  - Cultivation and yoked codes [T3-6, T3-7] would lower the qubit counts.
  - Routing, decoding and R > 1 scheduling are not modelled beyond [B46].
- **Levels.**
  - Theoretical: L3 for "qubitised learned-energy walk step = Θ(L²) Toffolis with the constants above (torsion), at fixed-point precision validated to classical parity on PILOT samples". This is a statement about an explicit construction, not about optimality.
  - Practical: **L0**. No category-3 resource advantage is claimed.

---

## 7. Open gaps

- **G-1. Measure κ(L).** Run the quantised chain P_W classically: single-angle ±δ Metropolis on the b-bit lattice at fixed λ, especially at the λ ≈ 0.4–0.5 bottleneck.
  - Measure its per-sample steps against the best portfolio's energy+gradient cost, as a function of δ.
  - κ multiplies B linearly. It decides between D2 and D3, and whether κ grows with N_C (α).
  - The one-unit move scale of §2.2 (median |ΔE| up to ~1 nat at L=150) suggests κ ≫ κ_min.
  - This is cheap classical G1 work.
- **G-2. Local moves with exact geometry.** Find a reversible move on the internal-coordinate lattice that changes only O(1) residues' positions, e.g. a crankshaft rotation of X_r about X_{r−1}X_{r+1}. It would give D3-like O(L) terms per step with the exact A80 target. Lattice rounding breaks the involution structure LHPST needs (UNPROVEN whether a fix exists).
- **G-3. Precision at the bottleneck and in the coin.**
  - b_w was chosen from PILOT λ = 1 samples (§3.2). Repeat the emulation on bottleneck-λ samples and at L = 200.
  - The coin precision needed for detailed balance, with ΔE spanning tens of nats, is not analysed. Only SK-16 evidence exists [A56].
  - b_w moves G by ~1.3× per 4 bits (§4.7), so this gap can move G by ~1.5–2×, not by orders of magnitude.
- **G-4. Check O-1, the ±δ involution and the move-sign trick** with a small reversible simulation (≤ 20 qubits, toy energy). This covers the move-set block encoding of §2.3 as well as O-1, and is a small-scale verification of compiled arithmetic allowed by the roadmap budget.
- **G-5. Firm up τ_D2** by compiling one pair term in a resource-estimation framework such as Qualtran or Azure QRE: saturating squared distance, region select, a 1,088-entry QROAM and Horner. Include windowed arithmetic [T3-5] and the round-to-nearest multiplier.
- **G-6. Continuous samplers [A44] and quantised HMC.**
  - These need a coherent *gradient* oracle. T2 assumes G_grad ≈ (2–4)·G, and a reversible reverse-mode gradient through the prefix product has not been compiled.
  - The quantised-HMC variant (§4.5) also needs the momentum-garbage uncomputation costed.
  - T2's claim level for the [A44] route stays capped until this is done.
- **G-7. Optimised classical t_C(L).** Measure with a compiled (C, numba or GPU) evaluator, and measure the achievable S for PT/HMC on the G1 targets. B ∝ t_C⁻²·S².
- **G-8. Parallel scheduling.** Model R-way factory parallelism with explicit routing (Litinski-style layouts). The D3 pair workspaces at R = 100 reach ~3.4×10⁵ logical qubits unless QROAM workspaces are shared.
- **G-9. Integration.**
  - Add [T3-1]–[T3-7] to `BIBLIOGRAPHY.md`.
  - Mark [A60]'s QROM cost as verified, closing lead #55.
  - Replace T2's A-G with §0 item 10, for Metropolis walks only.
  - Raise with T2 that its walk-step count K·ℓ·δ_*^{-1/2} is an upper bound, and that c_q ∈ [K, K·ℓ] (S8).
  - Restate H-008: "per-step clause not met by any costed design; falsified for move-oblivious torsion oracles conditional on §0 item 9 (i)–(ii); G(L) ≈ 3×10⁴·L² Toffolis (faithful torsion, central) or 7×10⁶–6×10⁷ (Cartesian, L ≤ 200); B(L) as in §4.5, which fails ≤ 10¹² against S = 10³ at 170 µs, R ≤ 10³; relevant only if G1 measures N_C(L) ≥ B at the chosen (S, R, κ, c_q)".
- **G-10. Classical bypasses.** B compares against the λ-path classical cost, but T2 §1 S5 shows other paths may avoid the first-order bottleneck. The relevant N_C is the *best* classical portfolio's (T2's B_best), which can only be smaller.
- **G-11. Magic-state budget.** Cost a factory, or a cultivation plus distillation stack, that reaches ε_CCZ ≤ 10⁻¹⁴–10⁻¹⁹ (§3.10), and fold its time and footprint into §4.6. The present figures are lower bounds.

---

## 8. Response to review (objections rejected in whole or in part)

Most objections were accepted and fixed (§9). The following were not accepted as stated:

1. **R1.16, sub-item H1 ("'30·5.5 µs' should be 31·5.5 = 170.5 µs").** Rejected as a correction. [B46] eq. (6) reads verbatim "t_G = 30 × 5.5 × 1 µs ≈ 170 µs", with "a code distance in the vicinity of d = 30" (PDF re-read in the v2 session), and v1 quoted it faithfully. v2 adds that at Sanders' d = 31 the same rule gives 170.5 µs (H1). The 170 µs figure is unchanged.
2. **R2.6 ("κ can grow like N_C^α with α up to 1/2").** Accepted in substance, but the stated ceiling is too low. With κ = N_W/N_C and a lifted classical chain achieving N_C ~ N_W^β, α = 1/β − 1. Lifting gains at most a square root ([A14], as usually stated), so β ≥ 1/2 and α < 1, not ≤ 1/2. At α → 1 the quantised reversible chain loses its whole advantage. §3.11 gives the general break-even B = (c_q√κ₀·X)^{2/(1−α)} for α ∈ [0, 1).
3. **R1.2 ("the emulation suggests b_w ≈ 26–30, i.e. G ×1.7–2.25 central").** Partially rejected. The fixed-point analysis was added (§3.2) and b_w = 16 withdrawn. But our emulation, with round-to-nearest multipliers (free, P3) and 4 guard bits in the build (≤ 1% of G), needs b_w = 22–24 at L ≤ 150 for classical parity and 20–23 for TV ≲ 0.01. That is ×1.2–1.5 on central G and ×1.4–1.9 on generous G. The reviewer's larger widths follow from truncating multipliers without guard bits and a stricter criterion (sd(δΔE) ≲ 2·ε_TV). Our table reports sd for every b_w from 16 to 28, both rounding conventions and both guard settings, so that criterion can be applied directly: at ε_TV = 10⁻³ it gives b_w ≈ 25–28.
4. **R2.2 ("b_w ≈ 22–24, ×1.2–1.4 on G").** Accepted for L ≤ 120. At L = 150–200 the emulation needs 24–25 (central), i.e. ×1.4–1.5.
5. **R1.1 (κ_torsion ≥ "3 with cached per-pair energies").** Accepted as a valid floor. §4 nevertheless uses the uncached floor 1.5, because the purpose of κ_min is the most favourable admissible value for the quantum side. Using 3 doubles every torsion B.
6. **R2.3 ("at S=10³ the B-clause fails for every design, even at c_q=1").** Confirmed under the 170 µs, R ≤ 10³ model (§0 item 9, §4.6). It is not true across the whole hardware envelope. At 10 ns effective Toffolis (t_T = 1 µs, R = 100) D3 reaches B = 4–8×10¹¹ at S = 10³. The verdict sentence is therefore scoped to the hardware model.
7. **R2.5 / R1.6 (pilot bounds).** Fully accepted. One refinement: T2 §4.1(b) quotes 6×10⁴ at L=150, and the exact value from the RAW file is 5.7×10⁴.

No objection was rejected on substance beyond these points.

---

## 9. Review log

Reviewer 1's objections are R1.x and reviewer 2's are R2.x. "Fixed" means the text and, where relevant, the scripts were changed.

| # | objection (short) | severity | resolution | where |
|---|---|---|---|---|
| R1.1 | κ = 1 is below the floor κ_min = t_C/t_W^cl; D3 floor ≈ L/8, torsion 1.5–3 | high | **Fixed.** Floor derived (§3.11) and used in all B tables. κ = 1 kept only as an infeasible reference line. H-008 list recomputed. v1's "most favourable case" (1.3×10⁸–4.8×10⁹, 4–6 d) is superseded: D3 generous S=1 R=100 is now 1.1–2.7×10¹⁰ (28 d–1.3 yr) | §0.5, §0.7, §2.6 C3, §3.11, §4.5 |
| R1.2 | no fixed-point analysis; b_w = 16 unfaithful; b_w² sensitivity | high | **Fixed**, with the partial disagreement in §8.3. Fixed-point emulation added (`--fixed-point`). b_w chosen by a stated criterion and made L-dependent. b_w = 16 withdrawn. G-3 restated. L3 made conditional on the precision criterion | §0.2, §0.4, §2.5 A2, §3.2, §6, §7 G-3 |
| R1.3 | "FALSIFIED (DERIVED)" overstates an upper bound | medium | **Fixed.** Now "NOT MET by any construction considered (INFERENCE)", plus the conditional floor of R2.1 | §0.9, §7 G-9 |
| R1.4 | s = 16 not a knot; steric not polynomial in s; local coordinate not free on a non-dyadic grid | medium | **Fixed.** v2 bit-aligned grid (h = 2 Å², knots at 4 and 16). Coordinates in Å. "Exactly" removed and the folded error measured (1.5×10⁻³). Energy-level check now folds sterics. This exposed the CB cusp at s = 0, fixed with a 64-segment sub-grid | §2.5 A3, §3.2 |
| R1.5 | C2 "lower B by 2–5×" not squared | medium | **Fixed**: 6–24× (PyTorch), 2.2–8.7× (PILOT), ~12–50× (optimised) | §2.6 C2 |
| R1.6 | pilot scans misquoted; bounds are production counts at ~63%; 3×10⁸ mismatch; placeholder vs pilot t_C | medium | **Fixed.** Scan counts 1500/1200/800/600/500. 63% vs 95% (n/3) stated. Ratios recomputed at matched L. Pilot-t_C variant added | §0.8, §4.6 |
| R1.7 | quantised-HMC κ text (1) vs script (1/n_leap); momentum garbage | medium | **Fixed.** κ = 1/n_leap in text. Garbage uncomputation flagged UNPROVEN. Compared with D2 at κ = 3 | §4.5, §7 G-6 |
| R1.8 | R = 100 physical-qubit column omits 99 workspaces; §4.6 pebbled qubits with unpebbled G | medium | **Fixed.** Workspaces included (1.5×10⁸–1.1×10⁹). §4.6 uses stored frames and matching G | §0.6, §4.4, §4.6 |
| R1.9 | CCZ output error not modelled | medium | **Fixed.** ε_CCZ·N_Toff ≤ 0.1 added. [T3-3] ~10¹⁰ (10¹² with +20% footprint) cited from the PDF. All break-even figures labelled lower bounds. G-11 opened | §2.4 H5, §3.10, §4.6, §6 |
| R1.10 | §0.1 "few per cent" false for D3; factor-4 mislabelled; "<10⁴" false | low | **Fixed**: restricted to torsion at L ≥ 100 (≤ 7%); factor relabelled; bookkeeping ≤ 4.2×10⁴ (≤ 5.3×10⁻⁴ of G) | §0.1, S2, §3.5 |
| R1.11 | D3 exponent L^{1.0–1.5} wrong | low | **Fixed**: local exponents 0.95–1.38 (central, now including b_w growth); ~L^{1.0–1.4}, tending to L^{1.5} | §0.5, §3.8 |
| R1.12 | B-clause list inaccurate (D1 generous omitted, D3 central at L=30, "S=1 only") | low | **Fixed**: per-design grid at L=100 with S_max | §0.9, §4.6 |
| R1.13 | λ cannot be folded into the coin table | low | **Fixed**: λ/T into the pair-spline coefficients, 1/T into head and wall tables | §2.1 |
| R1.14 | b_acc sized from the lowest energy found; overflow | low | **Fixed**: b_acc = 40 from the worst case (≤ 67.6 nats per pair, 1.3×10⁶ at L=200) | §2.5 A4 |
| R1.15 | intermediate frame not uncomputed or stored; 15 additions undercounted | low | **Fixed**: the intermediate is one column (3 entries), stored at zero Toffolis or uncomputed (+6 MUL) when checkpointed; 24 additions; 3.8 Å constant multiply added | §2.5 A11, §3.3 |
| R1.16 | trivial arithmetic (A5 2,092; S8 c_q² range; §0.10 "brackets D2 exactly"; bonds 2.1×10⁴; H1 31·5.5; soft-bin lookup 1,174; §3.1 2L³/3; §0.4 ratio mixing; sd 5.1e-5; "exact up to interpolation") | low | **Fixed** each (A5: 2,092 at b_acc = 32, 2,124 at 40; S8 superseded by R2.14; §0.10 rewritten; bonds now 3.0×10⁴; lookup 1,174 at b_c = 20, 1,234 at 23; 2L³/3; ratios labelled per term and per step; energy table regenerated; "exact" removed), **except H1**, rejected in §8.1 | §2.5, S8, §0.10, §3.8, §3.2, §3.1, §0.4 |
| R2.1 | "falsified" does not follow from upper bounds; add a conditional floor; D3 inconclusive | high | **Fixed**: "NOT MET"; conditional squaring floor ≥ 1.4×10⁷ at L=100 for the move-oblivious torsion class (b_w ≥ 22); D3 inconclusive (floor 1.1–1.2×10⁶) | §0.9, §4 script output, §7 G-9 |
| R2.2 | fixed-point error dominates; b_w = 16 unfaithful; specify formats | high | **Fixed** (formats in A2; emulation §3.2; §0.4 now names the dominant error source). See §8.4 | §0.4, §2.5 A2, §3.2 |
| R2.3 | B-clause read at c_q = κ = S = 1 gives unsupported support to H-008 | high | **Fixed**: grid over c_q ∈ {1, 10, 90}, S ∈ {1, 10³}, κ ∈ {κ_min, 50, L}; S = 10³ headline; S = 1 and c_q = 1 presented as bounding devices. See §8.6 for the scope of "fails at S = 10³" | §0.7, §0.9, §4.6 |
| R2.4 | "most generous" is not an envelope (R = 10³, t_T down to 1 µs); 2019 qubit model outdated | medium | **Fixed**: hardware-envelope table (R up to 10³; t_T ∈ {170, 10, 1} µs); practical L0 shown not to rest on the cap; physical counts labelled 2019-model; [T3-6], [T3-7] cited from verified abstracts | §0.6, §0.9, §2.4 H2 and H6, §4.6 |
| R2.5 | pilot facts misquoted; use n/3 bounds; PT-only bound, N_C is the portfolio minimum | medium | **Fixed** (as R1.6); portfolio caveat added | §0.8, §4.6 |
| R2.6 | κ treated as constant; report κ ∈ {1, 50, L}; κ ∝ N_C^α | medium | **Fixed**, with the correction in §8.2 (α < 1, not ≤ 1/2) | §2.6 C3, §3.11, §4.6 |
| R2.7 | LHPST proved for bit flips; ±δ extension is INFERENCE; reflecting θ breaks the group; δ unspecified | medium | **Fixed**: tagged INFERENCE; involution F stated; wrap-around θ with wall energy; δ = 1 lattice unit; move-set check added to G-4 | §2.2, §2.3, §6, §7 G-4 |
| R2.8 | "B independent of L" holds only for t_C ∝ L² | medium | **Fixed**: stated as conditional; measured exponents 1.48 (PILOT), 1.43–1.73 (PyTorch); B(L) under measured t_C tabulated (∝ ~L^{1.2}) | §0.7, S5, §4.5 |
| R2.9 | surface-code exponent miscopied (100× pessimistic) | low | **Fixed** after re-reading [T3-4] §2.13 (worked example reproduced) in H3 and `d_required` | §2.4 H3, §3.10, §4.6 |
| R2.10 | Newton √ costed in the HRS convention, others in n² | low | **Fixed**: P6 in the n² convention (6,731 vs 14,981); D1/D2 now 2.5× per term; uniform-s wins by 2.7× (not ~5×); HRS everywhere is the ×2.16 sensitivity row | §2.4 P6, §3.2, §4.7 |
| R2.11 | quantised-HMC κ text; c_grad and LHPST-for-HMC are INFERENCE | low | **Fixed** (as R1.7) | §4.5 |
| R2.12 | steric knot claim wrong; folded term untested | low | **Fixed** (as R1.4) | §2.5 A3, §3.2 |
| R2.13 | §0.10 could be read as closing G_grad for [A44] | low | **Fixed**: Metropolis-only scope stated; G_grad stays open (G-6); T2's [A44] claim level stays capped | §0.10, §7 G-6 |
| R2.14 | c_q ∈ [K, K·ℓ], not K·ℓ | low | **Fixed**: c_q ∈ [K, K·ℓ] ⊂ [10, ~1.8×10⁴], c_q² ∈ [10², ~3×10⁸]; inconsistency raised with T2 | S8, §2.6 C4, §7 G-9 |

**Superseded v1 headline numbers (for traceability).**
- G(D2 central) = 2.1×10⁷–9.1×10⁸ at b_w = 20, and G(D2 generous) = 4.6×10⁶–1.9×10⁸ at the unfaithful b_w = 16.
- "B(D2 central) = 1.5×10¹⁵ (S=R=1), independent of L" at κ = 1.
- "Most favourable case 1.3×10⁸–4.8×10⁹, T* ≈ 4–6 days" at κ = 1 and b_w = 16.
- "Per-step clause FALSIFIED (DERIVED)".
- "B-clause holds for R ≥ 10 …".
- Energy-level spline error sd ≤ 5.1×10⁻⁵, which omitted fixed-point arithmetic and the folded steric term.

All are replaced by the v2 values above.
