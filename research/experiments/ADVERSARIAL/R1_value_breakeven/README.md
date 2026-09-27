# R1 adversarial lens: value and break-even of the NMR echo window

_2026-09-27. Adversarial attack on the surviving lead R1 (protein ¹H dipolar echo / first-order OTOC window). This lens asks one question: **suppose the echo window is real, is it worth anything for protein structure?** Every number below is tagged: MEASURED (computed here or read from RAW), DERIVED (algebra on measured inputs), INFERENCE (a model or domain value, not verified this session), LITERATURE-SUPPORTED (a source checked this session, unless it says otherwise), UNPROVEN._

## Verdict: KILLS (practical value level)

In no plausible regime does the echo window give a net benefit for protein structure over classical alternatives.

- **Where a quantum forward model is not needed, nothing is gained.** In the dilute amide-only (perdeuterated) network, the median-calibrated light cone stays within exact classical reach (≤ 47 spins) for the whole 1 ms window. The quantum-only gain there is g = 1.0 (INFERENCE, §3).
- **Where it is needed, it buys very little.** In the dense ¹H network after roughly 100–140 µs:
  - The quantum-only information cuts the number of repetitions needed for local distances of 3.3–3.8 Å by a median factor of **2.7**, and at most 10× (INFERENCE, §3).
  - The classically reachable precision for those distances, 0.03–0.05 Å at σ = 0.01, is already below the forward model's systematic floors. Cluster truncation adds 0.06–0.6 Å and motional averaging adds 0.06–0.35 Å (MEASURED-derived, §2).
  - The cost is ≥ 49 days of fault-tolerant machine time per probe at a 1 µs T layer, and ≥ 23 years at 170 µs (DERIVED, §6).
- **The same distances are cheaper elsewhere.** NOESY and solid-state contact experiments measure them, and AlphaFold-class models predict them (INFERENCE, §5). The only experimental OTOC-structure demonstration so far reports "similar accuracy and precision to independent spectroscopic measurements" (LITERATURE-SUPPORTED, Zhang et al. arXiv:2510.19550, abstract verified today).

**Levels.** Theoretical **L1**: approximate classical methods fail at N = 10. There is no separation from exact classical simulation, and the adversary scaling measured in C2/C3 is dominated by exact statevector simulation (§4). Practical **L0**. What remains is at most a claim-category-3 (resource) question about simulating large dipolar echo dynamics. It is not a protein-structure advantage.

## How to reproduce (all single-threaded, total < 3 CPU-min)

```
cd research/experiments/ADVERSARIAL/R1_value_breakeven
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
python lightcone.py      # N_eff(t), exact-reach time t_ex         -> lightcone.json   (~10 s)
python fi_value.py       # CRB per distance, gains g                -> fi_value.json    (~2 s; reads lightcone.json)
python model_bias.py     # cluster-truncation bias vs CRB           -> model_bias.json  (~1 s)
python breakeven.py      # FT quantum vs exact / Pauli, tasks       -> breakeven.json   (~10 s; microbenchmark)
python value_table.py    # comparators, sigma sweep                 -> value_table.json (<1 s)
python dynamics_floor.py # rigid-model bias under motional scaling  -> dynamics_floor.json (~20 s, 12 exact N=10 runs)
```

Inputs are read-only: `research/results/RAW/nmr_gate*`, `nmr_embed`, `results/PROCESSED/c2_summary.json` (numbers quoted), `data/instruments/nmr/*_H.pdb`, and `src/qapf/nmr/spins.py`. Nothing outside this folder was modified. The `*_stdout.txt` files are the console logs of the runs that produced the JSON files.

---

## 1. Echo precision per distance (MEASURED Jacobians → DERIVED CRBs)

`fi_value.py` rebuilds the full Jacobians dS_ab(t)/dφ and dF_ab(t)/dφ stored by `scripts/nmr_gate.py`. There are 11 γ = 0 jobs with echo data (4 dense, 7 amide-only) and 35 distinct parameters. The N = 14 dense job has transfer data only, so it appears only in the transfer column. From them it forms full Fisher matrices at σ = 0.01 per point.

The marginal Cramér–Rao bound (other parameters treated as nuisance) is in Å and scales linearly with σ. Three variants:
- **"classical route"**: transfer at all times plus echo before t_c*. Everything a classical *approximate* model reproduces at N = 10.
- **"quantum"**: transfer plus the full echo.
- **g**: the per-parameter factor of repetitions the quantum model saves, g = CRB_cl² / CRB_q².

| network (parameter distance from probe) | CRB transfer only | CRB echo only | CRB classical route | CRB quantum | g per parameter | largest generalised eigenvalue |
|---|---|---|---|---|---|---|
| dense ¹H (3.3–4.0 Å), n = 14 | 0.053 Å (0.006–0.21) | 0.015 (0.002–0.040) | **0.031** (0.006–0.11) | **0.014** (0.002–0.038) | **5.6** (1.7–68) | 25 (3.1–68) |
| amide-only (5.9–8.3 Å), n = 21 | 0.100 (0.012–0.76) | 0.027 (0.005–0.22) | **0.075** (0.006–0.46) | **0.026** (0.004–0.21) | **6.4** (1.6–59) | 30 (2.5–63) |

Values are medians with the range in parentheses.

- The diagonal echo/transfer FI ratio is a median of 9.8 (dense) and 16 (amide), with a range of 3–183. This matches the "10–160×" headline, but **the headline is the wrong comparator**. The classical twin uses the transfer data and the early echo *jointly*, which cuts the saving to g ≈ 6 (DERIVED).
- **Classical-pessimistic variant.** Suppose transfer were also unusable after t_c* at large N. Then the classical route's median CRB becomes 0.053 Å (dense) or 0.107 Å (amide), with g median 24 / 11 and a best direction of 2.9×10³ / 355 (DERIVED). This is the upper bound on value if nothing late is classically computable.
- **σ sweep** (DERIVED, linear). At σ = 0.03 the median CRBs are 0.094 / 0.042 Å (dense, classical / quantum) and 0.22 / 0.079 Å (amide). At σ = 0.1 they are 0.31 / 0.14 Å and 0.75 / 0.26 Å.
- **σ = 0.01 is itself an assumption.** It is the value for a *site-resolved, normalised* correlator with SNR 100 per point. Static dense ¹H networks have no chemical-shift resolution, so a real experiment would need isotopic engineering (INFERENCE).

## 2. Is that precision usable? Forward-model systematic floors (MEASURED-derived)

**Cluster truncation** (`model_bias.py`, R1-E RAW, 1UBQ probes 19 and 245). The data come from a core embedded in the 12 or 14 nearest protons. Fitting them with the isolated 10-spin model gives this linearised bias:

| data | misfit (max) | max parameter bias | max bias / CRB |
|---|---|---|---|
| echo, +2 spins (N_env = 12) | 4.1–12.5 σ | 0.22–0.24 Å | 7–20 |
| transfer, +2 spins | 1.9–5.4 σ | 0.06–0.44 Å | 1–9 |
| transfer, +4 spins (N_env = 14) | 8.8–12.7 σ | 0.53–0.57 Å | 15–16 |
| transfer, Gaussian-bath dephasing proxy | 5.6–11.9 σ | 0.63–0.94 Å | 8–12 |

Adding only 2–4 of the protein's ~600 protons moves the fitted distances by 5–20 times the CRB. The N = 10 FI numbers therefore describe an isolated cluster, not the protein. Reaching them needs a forward model converged in N, i.e. one that holds the whole light cone (§3). **The echo is more environment-sensitive than transfer** (larger misfit per added spin).

**Motional averaging** (`dynamics_floor.py`, 12 new exact N = 10 runs; validation against the stored C1 signals gives a difference of 0.0). Couplings were scaled by order parameters S = 0.95 or 0.90 uniformly, or per pair S_ij ~ U[0.85, 1.0]. These are mild backbone-like values (INFERENCE). Methyl rotation and side-chain motion are much larger effects and were not included. Fitting a rigid-lattice model then gives:

- 1UBQ H/ILE3, dense: echo misfit 2.9–6.0 σ; the largest parameter bias per case is 0.06–0.15 Å, i.e. up to 4–14× the quantum CRB.
- 1UBQ-HN probe 487, amide: echo misfit 3.1–6.6 σ; the largest bias per case is 0.10–0.35 Å, i.e. up to 4–11× the quantum CRB.

The extra sensitivity that produces the echo's extra FI also amplifies model error. The quantum CRB of 0.01–0.03 Å is therefore realisable only with an ensemble (MD-averaged) forward model whose couplings are accurate to about 1%. That multiplies the forward-model cost by the number of conformers and brings in force-field error. Zhang et al. used their OTOCs *to correct* molecular-dynamics models (LITERATURE-SUPPORTED, abstract).

## 3. How large is the light cone? When is a quantum forward model needed at all? (INFERENCE, calibrated)

`lightcone.py` uses a first-passage model: the influence front reaches proton j at t_j = c·(shortest path Σ 1/|d_edge|) over the full-molecule dipolar graph, with the job's B0. It is calibrated two ways:

- **(i) Arrival of the echo at the observed b inside the cluster** (n = 44): c = 0.21. This calibration fails the cross-check below. It predicts that the added protons act 3–12× too early.
- **(ii) Influence time: when the added R1-E protons first move any observed signal by > σ** (6 points, bracketed by the 20 µs grid): c = 1.02 (median), bracket 0.32–2.5. This is the calibration used below. "fast" and "slow" are the bracket ends.

| | dense ¹H (1UBQ 629 H, 1PGA 419 H) | amide-only (1UBQ 73 HN, 1PGA 56 HN) |
|---|---|---|
| N_eff at t50 of the echo FI (median calibration) | 21–110 (bracket 7–589) | 20–39 (bracket 9–73) |
| N_eff at t90 | 143–280 (bracket 23–627) | 20–50 (bracket 16–73) |
| t_ex = time the cone exceeds 47 spins (median) | 103–141 µs | never within 1 ms in 6 of 7 jobs (940 µs in one) |
| fraction of echo FI after t_ex (median; fast / slow) | **0.71** (0.23–0.95); fast 0.999; slow 0.10 | **0.0** (0–0.24); fast 0.87; slow 0.0 |
| g, exact-classical route (transfer all + echo < t_ex), median | **2.7** (1.1–10.4); fast 13; pure-exact 5.6 | **1.0** (1.0–1.4); fast 6.0 |

Consequences (INFERENCE):
- In the amide-only network of small proteins, the echo information is almost entirely inside exact classical reach. **No quantum forward model is needed.**
- In the dense network the quantum model is needed after about 100–140 µs. The information it alone supplies is worth a factor of about 3 in repetitions (up to 13 with the fast calibration).
- The calibration rests on 6 points and one protein. It is the largest uncertainty in this lens (see test RT-1).

## 4. Break-even of a fault-tolerant quantum forward model (`breakeven.py`, DERIVED from `nmr_resource_model.py`)

**Quantum cost model** (extends the original):
- effective neighbours z_eff = min(z, N−1), with z = 15 (dense) or 8 (amide);
- the circuit for time point k has 2k Trotter steps;
- repetitions: amplitude estimation to ε = 3×10⁻³ (1,047 repetitions), or sampling (1.1×10⁵);
- rotations cost 1.15·log₂(1/ε_rot) + 9.2 T each;
- wall-clock: depth-limited with unlimited factories (t_T = one T layer, the most favourable case for quantum), or rate-limited with 100 factories.

**Classical exact model:** typicality statevector; (1+n_b)·n_T·(n_t+3)/2 Trotter steps; N·z/2 pair gates per step on 2^N amplitudes. Throughput was **MEASURED** here: numpy, 5.3×10⁷ amplitude-gate updates per second per core. The optimised figure (10⁹ per core-equivalent) is INFERENCE. The memory wall is 3 vectors × 16 B × 2^N.

For scale: a 45-qubit statevector needed 0.5 PB on 8,192 Cori II nodes (LITERATURE-SUPPORTED, Häner & Steiger, arXiv:1704.01127, abstract verified). With sector reduction and single precision, the wall moves to about N = 51 (INFERENCE).

**(a) Against exact classical light-cone simulation.** The table gives the smallest N_eff at which the quantum wall-clock per forward evaluation wins.

| logical T-layer time | quantum per evaluation (dense / amide) | vs 64-core node | vs 10⁴ cores | vs 10⁶ core-eq (4 PB) |
|---|---|---|---|---|
| 1 µs | 6.3 h / 4.1 h | N* = 30 | 37 | 44 |
| 10 µs | 2.6 d / 1.7 d | 33 | 40 | 47 (memory wall) |
| 170 µs | 45 d / 29 d | 35 (wall) | 41 (wall) | 47 (wall) |

- Sampling instead of amplitude estimation multiplies the quantum time by about 100 (28 d per evaluation at 1 µs).
- **Break-even therefore sits at N_eff ≈ 30–47.** Below it, classical exact simulation is faster than any plausible fault-tolerant machine. Above about 47–51, exact classical simulation is impossible whatever the T time.
- Per evaluation, the quantum machine then takes 4–6 h × (t_T / 1 µs). A one-week single-probe inversion (180 evaluations) needs **t_T ≲ 0.14 µs (dense) or 0.23 µs (amide)** per T layer, with unlimited factories.

**(b) Against the measured sparse-Pauli adversary** (C2/C3: M*_F = 256,643 strings at N = 10, ×16 per +2 spins; cost MEASURED at 1.7 µs per string-pair-gate):
- Formal break-even is N* = 12–15 (κ = 4 per spin) or 13–20 (κ = 2).
- **This adversary is dominated.** M*_F(10) ≈ 4^10/4.1 is already about the size of the whole operator space and exceeds the 2^10 statevector by 250×. The exact statevector (numpy, one core) is cheaper than sparse Pauli at every N from 10 to 39 for both κ (DERIVED).
- **C2/C3's exponential string growth is therefore not evidence of classical hardness.** The binding classical cost is 2^N_eff (exact), not 4^N_eff.
- The untested operator-front and hybrid adversaries could only lower the classical cost further.

## 5. Value per spectrometer-hour against established methods

**Echo against its classical twin.** Take the same sample, the same site-resolved detection and the same SNR per point. The echo then yields at most g× the Fisher information per spectrometer-hour of the classically interpretable data (transfer plus the early echo):
- g = 5.6 / 6.4 (median, N = 10 isolated clusters);
- g = 2.7 / 1.0 (median once exact classical reach at the real light cone is counted).

This bound ignores the echo's own penalties: the time-reversal block (magic-echo type), and its fidelity loss and doubled sequence length. It is an upper bound (DERIVED + INFERENCE).

**Echo against other experiments.** Domain values are INFERENCE-unverified unless marked. The full table is in `value_table.json`.

| method | distances | typical precision | interpretation |
|---|---|---|---|
| ¹H echo (this model) | 3.3–3.8 Å (dense), 6–8 Å (amide), MEASURED parameter set | CRB 0.014 / 0.026 Å at σ = 0.01; floors 0.06–0.6 Å (§2) | quantum only if N_eff > 47–51 |
| NOESY build-up | ≤ 5–6 Å | 0.3–1 Å (bounds); ~0.1–0.2 Å with exact-NOE protocols | classical |
| MAS contacts, REDOR ¹³C–¹⁵N | ≤ 6–8 Å | ~0.1 Å (REDOR, isolated pair) | classical |
| ¹⁹F–¹H / ¹⁹F–¹⁹F REDOR | up to ~15 Å (task-brief value) | ~0.5–1 Å | classical |
| PRE | ≤ 25–35 Å | 2–4 Å | classical (Clore & Iwahara 2009, from memory) |
| DEER | ~18–80 Å | 1–3 Å (mean) | classical |
| RDC | orientational | a few degrees | classical |
| XL-MS | Cα–Cα ≤ 25–35 Å | contact | classical |
| AlphaFold-class | all pairs | ~1 Å median backbone RMSD (Jumper 2021, from memory) | classical, minutes |

- The echo constrains exactly the **short-range** distances that NOE, MAS contacts and AlphaFold already provide. It does not reach the long-range regime of PRE, DEER, ¹⁹F or XL-MS.
- The instrument's parameters were all ≤ 8.3 Å from the probe (MEASURED). Direct couplings beyond 10 Å are ≤ 120 Hz and are swamped by relayed dynamics (INFERENCE).

**Value break-even in spectrometer time.** Take the best case that the hard window only saves (g − 1)·T_acq of acquisition per probe. The single-probe quantum inversion takes 49 d (dense, N_eff = 100) or 30.5 d (amide, N_eff = 45) at 1 µs. It pays only if one probe's data set would otherwise take:

- **≥ 10.7 d** (dense, g = 5.6) or ≥ 29 d (dense, g = 2.7 from exact reach), at price parity between a quantum-computer hour and a spectrometer hour;
- ≥ 107 d at a 10× price ratio, and ≥ 2.9 yr at 100×;
- in the amide case, never with g = 1.0.

Even then, the saved acquisition buys precision below the §2 floors, so its structural value is about zero (INFERENCE).

## 6. Smallest end-to-end task where the quantum route could plausibly be needed, and its cost

The model is Gauss-Newton with 20 iterations. The quantum side builds finite-difference Jacobians, (2P+1) evaluations per iteration. The classical side uses the adjoint, about 3 evaluations per iteration. Costs are depth-limited on one machine (DERIVED; `breakeven.json` → `tasks`).

| task | N_eff | P | quantum evaluations | T per evaluation | logical qubits (2N+10) | quantum total @1 / 10 / 170 µs | classical exact |
|---|---|---|---|---|---|---|---|
| T1 GB1 amide-only, 1 probe | 30 | 4 | 180 | 1.9×10¹¹ | 70 | 30 d / 0.8 yr / 14 yr | 12.9 d on one node; 1.2 min on a leadership machine → **classical wins** |
| **T2 ubiquitin amide-only, 1 probe** | 45 | 4 | 180 | 2.9×10¹¹ | 100 | **30.5 d / 0.8 yr / 14 yr** | 40.5 d on 10⁶ core-eq (at the wall) |
| T3 ubiquitin amide-only, full cone | 73 | 4 | 180 | 4.8×10¹¹ | 156 | 31 d / 0.85 yr / 14.5 yr | infeasible |
| T4 ubiquitin dense, 1 probe | 100 | 4 | 180 | 1.1×10¹² | 210 | 49 d / 1.3 yr / 23 yr | infeasible |
| T6 ubiquitin dense, whole backbone (76 probes, P = 228) | 250 | 228 | 6.9×10⁵ | 2.9×10¹² | 510 | 536 yr / 5×10³ yr / 9×10⁴ yr | infeasible |

- **The smallest plausible quantum-favoured task is T2/T3**: a perdeuterated, amide-protonated protein of about 75 residues in a static oriented sample; one site-resolved probe; 4 local HN–HN distances (6–8 Å); about 180 forward evaluations; 5–9×10¹³ T in total; about 100–160 logical qubits; about 1 month at a 1 µs T layer with unlimited factories.
- Its output is 4 distances with a quantum CRB of about 0.03 Å, against about 0.075 Å from the classical route. Both are below the motional and truncation floors of 0.06–0.6 Å.
- The same distances are known to 0.1–1 Å from X-ray, NOE or AlphaFold.
- The median light cone puts even T2 inside exact classical reach, with g = 1.0.

**Net benefit: negative in every row.**

Extra quantum-side burdens not included: a total T count of 10¹³–10¹⁴ needs per-T error ≲ 10⁻¹⁵ for a 1% run failure, beyond standard factory assumptions (INFERENCE); an MD-ensemble forward model (§2) multiplies every row by the number of conformers.

## 7. Flaws found in the R1 evidence chain (from this lens)

1. **Wrong comparator for "10–160× FI"** (DERIVED). The relevant saving is the joint gain against transfer plus the early echo: g = 5.6 / 6.4 median per parameter at N = 10, and 2.7 / 1.0 once exact classical reach is counted (INFERENCE).
2. **C2/C3 measure a dominated adversary** (DERIVED from MEASURED costs). The sparse-Pauli string count at N = 10 already approaches 4^N/4, while exact statevector costs 2^N. The ×16 per +2 spins growth says nothing about the best classical cost, and the pre-registered M*(60) extrapolation cannot establish hardness.
3. **Isolated-cluster FI is not protein FI** (MEASURED-derived). Two to four added protons bias the fitted distances by 5–20× the CRB. The echo is the more environment-sensitive observable.
4. **The CRBs are up to 4–14× below a mild dynamics floor** (MEASURED in model, S ranges INFERENCE), and below the ≥ 0.06–0.6 Å truncation floor.
5. **The parameters are local** (3.3–8.3 Å). This is the most redundant structural information and is not long-range.
6. **N_eff is the pivotal unknown.** At the informative times it lands between exact-classical-easy (amide) and "far beyond, but not worth it" (dense), under a 6-point calibration.
7. **Physical realisability is unaddressed.** Open issues: site-resolved Z_a / Z_b in static dense ¹H networks; dipolar time reversal; intermolecular protons (which enlarge N_eff); and σ = 0.01 per normalised point (INFERENCE).

## 8. Recommended tests (governed jobs; not run here, compute limits)

- **RT-1 (light-cone convergence, decides §3).**
  - Command: `python scripts/nmr_embed.py --pdb 1UBQ --probe 19 --envs 12,14,16 --otoc-max 16 --out research/experiments/ADVERSARIAL/R1_value_breakeven/embed16`, and the same for `--probe 245`. Sector blocks at N = 16 need about 3 GB and several hours per job, so run under the governor with ≤ 2 workers.
  - Measure N_conv(t) = the smallest N_env with max_b |F_N − F_{N+2}| < σ.
  - **Kill (value):** if N_conv(t50) ≤ 40 on both probes, the dense echo window is inside exact classical reach; g = 1 and R1 is dead as a quantum claim. **Escalate** only if N_conv(t50) > 47 *and* the late-window FI at the largest N_env keeps ≥ 50% of the N = 10 value, with top-eigenvector |cos| ≥ 0.5.
- **RT-2 (dynamics floor with an ensemble model).** Replace the uniform scaling with 50 MD or normal-mode snapshots (backbone rms 0.1–0.3 Å plus methyl 3-site averaging) and refit a rigid model with `dynamics_floor.py` logic.
  - **Kill:** median |bias| > 3 × the classical-route CRB. The extra precision is then unusable without an ensemble model, and the quantum cost is multiplied by n_conf.
- **RT-3 (classically non-identifiable directions).**
  - Over all C1 jobs, compute the generalised eigenvectors of F_quantum against F_exact-reach (`fi_value.py`, variant `g_exact_reach_*`), restricted to parameters with sequence separation ≥ 5 residues.
  - **Escalate** only if a direction with g ≥ 10³ exists and maps onto a structural degree of freedom that AlphaFold-class or NOE data leave undetermined (e.g. pLDDT < 70). **Kill** otherwise.
- **RT-4 (optimised classical throughput).** Re-measure the statevector kernel with fused gates and a sector-restricted random vector at N = 24–26 (single core, < 10 min).
  - **Kill (break-even shift):** if throughput exceeds 10⁹ amplitude-gate updates per second per core, break-even vs a node rises above N* = 30. This only strengthens the kill.
- **RT-5 (physical SNR audit, literature).** Obtain the measured OTOC SNR and time-reversal fidelity per hour from Zhang et al. (full text) and from solid-state magic-echo literature.
  - **Kill:** if σ per site-resolved normalised point after one day is > 0.05. At that noise level the quantum CRB (≥ 0.07 Å dense) sits inside the §2 floors and T_acq break-even (§5) is unreachable.

## Compute ledger

- CPU: about 3 CPU-minutes in total, single-threaded, peak RAM < 200 MB. The heaviest item was 12 sector-exact N = 10 runs at 1–2.4 s each, plus a 2^20 statevector microbenchmark of about 3 s.
- Hardware: Windows, 8 logical CPUs. The machine ran at 71–90% CPU and 83% RAM from the governor's C2 N = 12/14 jobs.
- No background processes. No files outside this folder were modified.
- Simulator runtime is not quantum runtime. All quantum times above come from a T-count and T-depth model (INFERENCE about hardware).
