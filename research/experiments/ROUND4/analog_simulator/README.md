# ROUND4 lane: `analog_simulator` — analog dipolar quantum simulators for the echo question

_2026-09-28. Folder: `research/experiments/ROUND4/analog_simulator/`. Nothing outside this folder was modified. No commit._

**Tags.** MEASURED (computed here, exact) / DERIVED (algebra, checked numerically where stated) / LIT (abstract or full
text fetched and read this session; details in `lit.json`) / INFERENCE / UNPROVEN / UNVERIFIED.

**Verdict: KILLS** for this lane's question. No existing analog platform, and no near-term one built from demonstrated
physics, plausibly reproduces the protein-derived dipolar echo F_ab(t) to σ = 0.01 at t = 40–120 µs for 20–100 spins,
let alone beats the classical route there. The scope of the kill is practical, not a theorem (§8).

---

## 0. Bottom line

1. **The target Hamiltonian is traceless, and programmable-geometry platforms cannot produce it natively [DERIVED + LIT].**
   - The protein secular dipolar coupling H_dd = Σ (d/4)(2ZZ − XX − YY) is a pure rank-2 tensor: its Heisenberg
     component is zero.
   - Rydberg resonant exchange (and polar-molecule exchange) is XY-type, with a nonzero Heisenberg component.
     Global Floquet rotations preserve that component. This is why Scholl et al. reach only 0 ≤ δ = Jz/Jx ≤ 2 (LIT,
     full text): the protein point δ = −2 is unreachable.
   - The staggered-frame trick needs a bipartite coupling graph. Protein networks are not bipartite (methyl triangles).
   - The one demonstrated fix is the ±C3 encoding swap (Geier et al. 2402.13873, LIT: C3 = +3.2 / −2.8 GHz µm³).
     Here it is built into a Floquet composite that reproduces H_dd exactly at zeroth order (checked to 1e-15). That
     composite costs **2 encoding swaps and 4 frame pulses per cycle**.
2. **The echo is extremely sensitive to Hamiltonian errors [MEASURED, exact ED, 1UBQ p19/p245, N = 10/12/14].** These
   are the error levels at which the rms error of F reaches σ inside 40–120 µs:
   - coupling calibration: 1.4–1.7%;
   - static positions: **0.25–0.53% of the nearest H–H distance**;
   - motion between the forward and backward legs: **0.10–0.38%**;
   - isotropic (Heisenberg) residual: 1.1–1.4%;
   - on-site fields: 1.0–2.2% of the local field.

   The sensitivity does not fall with N: the isotropic-residual error is 0.0081 / 0.0088 / 0.0076 at N = 10 / 12 / 14.
   Normalising by the no-butterfly echo R removes most reversal-mismatch error but none of the model error.
3. **The number of Floquet cycles is set by the protein, not the hardware [DERIVED + MEASURED].**
   - n_c = J_m t / (2π x*), with x* ≈ 0.05. The Magnus error at x = 0.05 is 0.0016–0.0048 at N = 8 and 0.0026 at
     N = 10; at x = 0.1 it is 0.005–0.019.
   - With J_m = 15–37 kHz (per-spin Σ|d|, N = 20–100), this gives **12–28 cycles per leg at 40 µs and 35–84 at
     120 µs**, i.e. 150–1,000 pulse and swap events per atom per shot.
   - Every per-event error is multiplied by that count.
4. **Pulse errors [MEASURED, Floquet simulation].** At the measured state of the art, Δθ = 0.06 rad per pulse (Scholl
   et al., LIT), the echo is off by 0.1–0.4 (10–40σ) already at N = 8. Δθ = 0.01 gives about σ, and 0.003 gives σ/5.
   Scaled to N = 50–100, the requirement is **Δθ ≤ 0.0023–0.0049 rad**, 12–25× better than demonstrated.
5. **Error budgets (`budget.py` / `budget.json`; quadrature total / σ, INFERENCE built on MEASURED sensitivities):**
   - Demonstrated Rydberg parameters (S0): **42–100σ.** The signal is destroyed by pulse error, Rydberg decay
     (T_sim = 16–118 µs vs τ_eff(61S, 300 K) = 105 µs) and atomic motion (~50 nm/µs).
   - Optimistic near-term composite (S1): **1.3–16σ.** It is dominated by swap leakage plus decay.
   - Most favourable, undemonstrated native-traceless route (S1b): **1.2–1.8σ at 40 µs, 2–6σ at 80–120 µs.** It is
     dominated by motion.
   - Nothing reaches ≤ 1σ for N ≥ 50, where exact classical simulation stops.
6. **The analog device would not escape the finite-cluster floor [DERIVED].** (1 − H)/N is 0.6–0.9σ at N = 100 and
   0.9–1.2σ at the largest verified 3D array (72 atoms, Barredo 2018, LIT). The simulator would need the same classical
   H_∞ (classical spin dynamics) that the classical hybrid uses. So it could at best supply X_N at N = 50–100, and the
   budget says it cannot do that at σ.
7. **Value.**
   - For protein structure: **none** (K-105 unchanged). The binding errors belong to the physical sample and the
     forward model, not to the computer that evaluates it.
   - New corollary [MEASURED sensitivity + INFERENCE]: σ-level forward modelling at t ≥ 40 µs needs proton coordinates
     to about **0.004–0.009 Å** rms and couplings to about 1.4%. That is below any realistic H-position and
     motional-averaging uncertainty, so even the *idealised* static-geometry echo is ill-defined at σ.
   - As physics: qualitative only. A 100-atom 3D programmable dipolar simulator at ~1% error would be interesting for
     3D dipolar operator growth. Natural NMR solids already give qualitative access at 10¹⁷ spins (Sánchez et al.
     PRL 2020, LIT: T3 ~ T2, perturbation-independent Loschmidt decay).

---

## 1. Question, target and comparators

- **Target.** The continuous-time isolated static 1UBQ ¹H network with secular dipolar H_dd (same geometry, field and
  instrument sites as ROUND3: probe a = cluster index 0, sites b ∈ {1, 7, 8, 9}).
- **Observable.** F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b]/2^N.
- **Physical window.** t = 40–120 µs (≤ T3; CRITIC C1).
- **Accuracy.** Absolute, σ = 0.01.
- **Measurement protocol an analog device would run.**
  - Start from a random computational product state s (infinite temperature).
  - Evolve U(t), apply a π_z pulse on a, apply the reversed evolution, read Z_b.
  - Estimator: sign(s_b)·m_b. All b are read in the same shot.
  - Signal: S = Tr[Z_b V Z_a U Z_b U† Z_a V†]/2^N (V = U† ideally). The no-butterfly normaliser is R = Tr[Z_b V U Z_b U† V†]/2^N.
  - Prep errors on atoms other than b are harmless at infinite temperature; prep and readout errors on b are scale
    factors that R and t = 0 normalisation remove [DERIVED].
  - A butterfly angle error π(1 + ε) adds (πε/2)²(1 − F), which is second order [DERIVED].
- **Classical comparators (ROUND3, as quoted):**
  - exact: about 26 spins per workstation-day per curve, 50–52 at exascale;
  - hybrid: classical spin dynamics for H_∞ (80–160 spins, about 3 CPU-min) plus exact X at N ≤ 22–26. Its H error
    budget is 0.6–1.6σ; X convergence is open (T-X-early).

## 2. Survey: what analog platforms have achieved (LIT unless marked)

| Platform / paper | Size, geometry | Native interaction → engineered | Time reversal | Achieved accuracy / imperfections |
|---|---|---|---|---|
| Rydberg tweezers, Scholl et al. 2107.14459 (PRX Quantum 2022) | 32 atoms 2D (a = 27 µm), 10-atom 1D | resonant dipole XY, C3(1−3cos²θ)/2r³ → XXZ with **0 ≤ δ ≤ 2** via 4-pulse Floquet | not shown | J_m t_c ≈ 2π·0.2, t_c = 300 ns, 3 µs of driving. Prep ~95% per atom, STIRAP ~95%, detection 5% / 3.5%. **Pulse error Δθ = 0.06 rad.** Finite pulse length is a leading error. Agreement with 12-atom cluster simulations is "good", with no σ-level metric |
| Rydberg gas, Geier et al. 2105.01597 | disordered gas | Floquet XYZ | — | "qualitatively captured by a semi-classical simulation" |
| Rydberg gas, Geier et al. 2402.13873 (PRR 2024) | 332–1,333 atoms, disordered | XX; sign flip via Δm = 0 → Δm = ±1 encoding (C3 3.2 → −2.8 GHz µm³) | **yes** | k = 1.1 theory vs 1.03 measured. Magnetisation revives to ~0.2 from ~0.5 after 6 µs. Motion ~50 nm/µs, ‖δJ‖ ≈ 20% after 6 interaction cycles. Transfer infidelity dominates early |
| Rydberg tweezers, Bornet et al. 2303.08053; Chen et al. 2207.12930 | ≤ 100 atoms 2D | dipolar XY; Floquet Heisenberg | — | squeezing −3.5 dB raw (−5 dB after detection-error correction) |
| 3D arrays, Barredo et al. 1712.02727 (Nature 2018) | **≤ 72 atoms, arbitrary 3D**, few-µm spacing | — | — | holographic plane-by-plane assembly. No larger arbitrary-3D array was found in an arXiv API search (INFERENCE: none may exist) |
| Large 2D tweezers, Manetsch et al. 2403.12021 | 6,100 atoms 2D | hyperfine qubits, not interacting | — | 12.6 s coherence |
| Rydberg OTOC experiments: 2410.15455, 2410.16174 (PRL 135, 050201), 2604.05038 (QuEra Aquila) | 1D/2D arrays | vdW / PXP; randomized quenches in 2604.05038 | digital-analogue (2410.15455) | qualitative light cones and scar revivals. **No σ-level absolute accuracy reported in the abstracts** (details UNVERIFIED) |
| Trapped ions, Gärttner et al. 1608.08938 (Nat. Phys. 2017) | > 100 ions, 2D Penning crystal | phonon-mediated Ising; sign flip via detuning | **yes** | OTOCs and MQC up to 8-body. The coupling matrix is not an arbitrary 3D dipolar network (INFERENCE) |
| NMR solids (natural simulators), Sánchez et al. 1902.06628 (PRL 2020) | 10²–10¹⁷ spins, fixed chemistry | native traceless dipolar | **yes** (magic/polarisation echoes) | Loschmidt decay T3 ~ T2, independent of the perturbation once interactions dominate |
| NV ensembles, Choi et al. 1907.03771; Gao et al. 2503.14598 | random positions | native magnetic dipolar (traceless) | **yes** (Floquet, time-reversed TAT) | robust sequences exist. **Geometry is not programmable** |
| Polar molecules, Carroll et al. 2404.18916 | lattice | Ising and exchange tuned independently | — | whether Jz/Jperp < 0 (the traceless point) is possible is not stated (UNVERIFIED) |
| Digital superconducting, Google 2506.10191 | 103 qubits | gates | yes | OTOC(2) beyond known classical methods. Different object (OTOC(2), random circuits) |

**Survey answers.**
- **(a) Accuracy after tens of interaction times.** No analog OTOC or echo experiment reports absolute agreement at the
  1% level after tens of interaction times. The quantitative numbers are revival contrast ~0.2/0.5 after ~6 cycles,
  pulse errors of 0.06 rad, and SPAM of 3.5–5% [LIT].
- **(b) Maximal size.** ~1,000 atoms in a disordered gas; 100 in 2D programmable arrays; 72 in arbitrary 3D [LIT].
- **(c) Can a protein proton geometry be loaded in 3D?**
  - In principle, yes. The Δm = 0 Rydberg exchange has the protein's (1 − 3cos²θ)/r³ pattern with the quantisation
    axis along B0 [DERIVED].
  - The scaled cluster needs r_min = 15–40 µm (§6) and about 100 distinct depths over roughly 200–400 µm.
    Plane-by-plane holography has not been shown for that [INFERENCE].
- **(d) Time-reversal fidelity.** Only the encoding-swap route reverses a Rydberg dipolar Hamiltonian, with a revival
  bounded by transfer efficiency and motion [LIT].

## 3. Structural result: the traceless-tensor obstruction [DERIVED]

- **Pair tensors.** Write every pair term as a coupling tensor J (3×3, here diag(Jx, Jy, Jz)).
  - Global rotations act as J → R J Rᵀ, which preserves Tr J.
  - A positive-weight time average of rotated copies therefore has trace Tr J_native.
- **Native traces.**
  - Rydberg or molecule exchange between two-level states: J_native = g·diag(1, 1, 0) (plus a DC-Stark Ising term
    ∝ (Δd)² with the same sign). Tr = 2g ≠ 0.
  - Target: H_dd has Tr = (−1 − 1 + 2)d/4 = 0.
  - Hence no global Floquet sequence from one encoding reaches H_dd. Written out, H1 = (4c/3)H_dd − (2c/3)H_S, and
    the H_S part cannot be averaged away.
  - This reproduces Scholl et al.'s reachable range 0 ≤ δ ≤ 2 exactly [LIT, full text].
- **Encoding swap.** A Δm = ±1 encoding flips the sign of the flip-flop coefficient:
  ε·ε* − 3|ε·n|² = −(1 − 3cos²θ)/2 for ε = (x̂ + iŷ)/√2. The spatial pattern is the same [DERIVED; consistent with
  Geier et al.'s C3 < 0, LIT].
  - Time-sharing the two encodings over three frames gives H_eff = H_dd exactly.
  - The mirror sequence gives −H_dd, and each reverse segment is the exact inverse of the forward one. So V = U†
    holds exactly at any cycle time when the calibration is perfect. `floquet_composite.py` checks: |H_eff − H_dd| and
    |H_rev + H_dd| ≤ 1e-15 relative; frame maps to 1e-10; R = 1 to rounding.
- **Undemonstrated alternative.** A Δm = ±1 encoding plus DC-Stark permanent dipoles could give Jz/Jxy = −2 natively,
  with no swaps [UNPROVEN; not demonstrated on any programmable platform].
- **Staggered frames.** Mapping δ = −2 to +2 by staggered local rotations requires a bipartite graph. The protein
  ¹H graph contains triangles (methyls), so this is unavailable.

## 4. Sensitivity of F to simulator errors [MEASURED]

`ed_echo.py` + `sens_scan.py` → `sens_*.json`, summarised in `sens_summary.json` (`analyze_sens.py`).

**Method and validation.**
- Exact continuous-time sector eigendecomposition.
- Validated against the ROUND3 Chebyshev reference at N = 12 to 0.028 max. That reference has one typicality vector,
  so its noise is about 2^(−N/2).
- The internal checks (mismatch path, R = 1, flip symmetry) hold to 3e-16 (`validate.json`).

**Table.** ε* is the error level at which the max over (b, t ∈ 40–120 µs) of the rms of ΔF across realisations equals
σ, by log-log interpolation. Realisations: 8 at N = 10, 3 at N = 12.

| Channel (what it models) | ε* p19 N=10 / N=12 | ε* p245 N=10 / N=12 | Notes |
|---|---|---|---|
| iid_shared (static coupling calibration, reversed exactly) | 1.25% / 1.50% | 1.68% / 1.39% | |
| iid_indep (coupling noise differing between legs) | 1.75% / 1.68% | 0.57% / 0.79% | p245 has a 19.8 kHz geminal pair |
| **pos_shared** (static position error / r_min) | **0.25% / 0.31%** | **0.50% / 0.53%** | N = 14 single draw at 1%: 0.018 (vs 0.025–0.053 at N = 12) |
| **pos_indep** (motion between legs / r_min) | **0.38% / 0.28%** | **0.19% / 0.10%** (extrapolated) | |
| scale (reverse rate off by η) | 3.6% / 3.6% | 1.4% / 1.4% | after S/R: 0.007–0.008 at 3%, 0.021–0.022 at 10% |
| heis_rev (isotropic residual λ, reversed) | 1.23% / 1.13% | 1.38% / 1.36% | at λ = 1%: 0.0081 / 0.0088 / **0.0076 (N = 14)** |
| heis_nonrev (isotropic residual, not reversed) | 2.75% / 2.75% | 0.68% / 0.69% | after S/R: ≤ 0.004 at 3% |
| onsite_nonrev (random fields / b_loc) | 1.56% / 1.01% | 1.72% / 2.18% | |
| delete_j (atom missing all sequence) | per-atom max\|ΔF\| median 0.07–0.18 | | signed sum over the 7 deletable atoms (N = 12): 0.33–0.36 |

**Reading.**
1. Model errors, meaning a wrong but exactly reversed Hamiltonian, set a floor of about 1–1.5% on couplings and about
   0.3–0.5% of r_min on positions. R-normalisation cannot remove them, because R = 1 for any exactly reversed
   Hamiltonian.
2. Reversal mismatch (scale, non-reversed residual) is mostly a multiplicative attenuation. Dividing by R recovers
   3–40× [MEASURED].
3. N-dependence: flat from N = 10 to 14 on the one clean deterministic channel.
   - The echo at site b depends on couplings inside the light cone, so no 1/N dilution is expected [INFERENCE].
   - The budget uses N = 12 tolerances for N = 20–100. That is optimistic if more in-cone couplings add variance.

## 5. Floquet composite: cycle time, pulse errors, C3 calibration [MEASURED]

`floquet_composite.py` (full-space exact; N = 8 both probes, N = 10 p19), outputs `floquet_*.json`.

**Setup.** x = J_m t_c/2π, where J_m is the median native per-spin Σ|g|. Pulses are instantaneous, which is
optimistic. Each frame change and each swap is followed by a random global rotation with N(0, Δθ) components (Scholl's
error model).

**Deterministic (max over t, b):**

| x | p19 N=8 | p245 N=8 | p19 N=10 |
|---|---|---|---|
| 0.2 | 0.018 | 0.065 | — |
| 0.1 | 0.005 | 0.019 | 0.012 |
| 0.05 | 0.0016 | 0.0048 | 0.0026 |
| 0.025 | 0.0004 | 0.0014 | — |

The error falls as about x². The budget takes **x\* = 0.05**.

**C3-ratio miscalibration.** k off by 1% gives 0.0025–0.0033; off by 3% gives **0.013–0.028**, independent of x. The
measured gap between theory and experiment in Geier et al. is 7% [LIT].

**Pulse errors at x = 0.05, 8 shots.** 11–33 cycles per leg, 132–396 error events per shot.

| Δθ (rad) | p19: max\|bias\| raw / after S/R | p245: raw / after S/R | R |
|---|---|---|---|
| 0.003 | 0.0013 / 0.0014 | 0.0007 / 0.0021 | ≥ 0.993 |
| 0.01 | 0.011 / 0.011 | 0.010 / 0.006 | 0.94–0.99 |
| 0.03 | 0.11 / 0.11 | 0.11 / 0.040 | 0.53–0.91 |
| **0.06 (demonstrated)** | **0.27 / 0.14** | **0.38 / 0.11** | 0.16–0.68 |

**Fit.** bias ≈ β·n_events·Δθ², with β = 0.19 (median) to 0.72 (max). The budget uses the max. With the median, S0
would still be above 20σ.

## 6. Budget: can an analog simulator hit σ at 40–120 µs, N = 20–100? [INFERENCE on MEASURED inputs]

`budget.py` → `budget.json` (and `budget_stdout.txt`).

**Scaling.**
- n_c = J_m t/(2π x\*) is hardware-independent.
- T_sim = 2 n_c t_c,min for the composite, or 3 n_c t_c,min for the native route, whose reverse leg runs at −H/2.
- Geometry follows from J_m^sim = 2π x\*/t_c,min and C3 = 3.2 GHz µm³: r_min = 15–40 µm, scale 12–24 µm/Å.

**Channels.**
- pulse (β n_ev Δθ²);
- atom loss: prep + decay T_sim/τ + swap leakage. Mid-sequence losses are weighted by 0.5. The coefficient per site
  is |Σ_j ΔF_j + (1 − F)|, which includes loss of the butterfly atom;
- motion (v·T_sim/2 between legs, through the pos_indep curve);
- static placement (pos_shared);
- k calibration;
- Magnus error at x\*;
- SPAM residual after normalisation.

**Scenarios.**

| Scenario | Key parameters | total/σ at t = 40 µs (N = 20 / 50 / 100) | at 120 µs | Dominant |
|---|---|---|---|---|
| **S0 demonstrated** (LIT-derived) | t_c ≥ 0.7 µs; Δθ = 0.06; k to 3%; swap leak 2% (INF); prep loss 5%; τ = 105 µs (61S, 300 K); v = 50 nm/µs | 42–55 / 74–80 / 91–93 | 100 (signal destroyed) | pulse, motion, decay |
| **S1 optimistic near-term** (INF) | t_c = 0.1 µs; Δθ = 0.005; k to 0.5%; swap 1e-3; prep 0.5%; τ = 450 µs (4 K); v = 10 nm/µs; 300-atom 3D | 1.3–1.9 / 1.9–2.4 / 2.2–2.9 | 7–16 | swap leakage + decay |
| **S1b S1 + native traceless coupling** (UNPROVEN physics) | as S1, no swaps | 1.2–1.4 / 1.6–1.7 / 1.8 | 3.3–6.3 | motion |

The table uses the quadrature total. A linear sum is 2–2.5× larger. The N = 20 rows are inside exact classical reach
anyway.

**Requirements.** Each of 7 channels gets ≤ σ/√7; the values below are for N = 50–100.

| Parameter | Required at 40 µs | Required at 120 µs | Demonstrated | Gap |
|---|---|---|---|---|
| Pulse error Δθ | ≤ 0.0039–0.0055 rad | ≤ 0.0023–0.0032 rad | 0.06 rad | 12–25× in angle |
| Per-atom loss (prep + ½ mid-sequence) | ≤ 1.0–1.5% | ≤ 0.47–0.58% | STIRAP loss alone 5% | 5–10× |
| Encoding-swap leakage (composite) | ≤ 6e-5–1e-4 per swap | ≤ 9e-6–1.5e-5 | not reported; revival bounded by transfer | ≥ 2–3 orders (INF) |
| Cycle time from decay (61S, 300 K / 4 K) | ≤ 13–22 ns / 55–94 ns | ≤ 2–3 ns / 8–13 ns | ≥ 300 ns | 1–2 orders |
| Static placement / r_min | ≤ 0.12% | ≤ 0.12% | UNVERIFIED (0.1 µm on 30 µm ≈ 0.3% assumed) | ≥ 2.5× |
| Motion between legs / r_min | ≤ 0.04% | ≤ 0.04% | 50 nm/µs × 10–60 µs on 30–40 µm: 1–5% | 25–100× |
| C3-ratio k calibration | ≤ 1% | ≤ 1% | theory vs measured differ by 7% | calibration needed |

**Other costs.**
- **Shot noise.** A ±1 estimator needs about (1 − F²)/σ² ≤ 1e4 shots per time point, and about 2× that with R. At
  1–5 Hz this is 1–10 h per time point [INFERENCE]. Exact classical simulation takes about a day per curve at 26 spins.
  For N ≤ 26 the analog route is slower and less accurate.
- **Finite-cluster floor.** (1 − H)/N, using the exact H from the N = 12 runs:

  | N | Floor |
  |---|---|
  | 20 | 0.030–0.043 |
  | 72 | 0.009–0.012 |
  | 100 | 0.006–0.009 |

  Removing it needs a classical H_∞, i.e. the classical hybrid's own input.

## 7. Value: protein structure versus physics

**Protein structure: none [K-105 unchanged; INFERENCE with MEASURED support].**
- K-105's load-bearing arms are:
  - forward-model error of the real sample (5–66σ: methyl rotation, 1 kHz offsets, 15% reversal mismatch);
  - value accounting (joint gain ≤ 1.2–3).
- Neither depends on which computer evaluates the idealised model.
- The physical NMR experiment on the protein already *is* an analog quantum simulation of the true Hamiltonian. A
  programmable simulator adds only the ability to evaluate the idealised model for candidate geometries, which is the
  step K-105 kills on value.
- **New corollary** (from §4). A σ-level forward model at t ≥ 40 µs needs:
  - static proton coordinates to ≤ 0.25–0.53% of r_min, about **0.004–0.009 Å** rms;
  - effective couplings to ≤ 1.4%.
- Riding-model or neutron H positions, zero-point and librational motion (dipolar order parameters typically cut
  couplings by several %) are all far larger [INFERENCE; literature values not re-verified this session].
- So the static-geometry idealised echo is itself uncertain at several σ. This independently supports the
  forward-model arm of K-105, and the CRITIC's O-7 / §2.4-8 point that R1-SIM-X sits outside the mission.

**Physics: modest, qualitative.**
- A 3D programmable dipolar simulator could study operator growth and echo decay in arbitrary 3D dipolar geometries
  (e.g. the hydrodynamic tail of H, the convergence of X).
- At demonstrated accuracy it would add qualitative data only.
- Natural solids already provide perturbation-independent Loschmidt decay at 10²–10¹⁷ spins [LIT: Sánchez et al.
  2020].
- The σ-level question R1-SIM-X is better settled classically first: CRITIC A-1 (T-X-early) and A-2 (spinDMFT). If X
  converges by N ≈ 22–26, the analog question is moot.

## 8. Claim audit

- **Category.** Candidate categories 3 (computational/resource) and 5 (hardware) for simulating the idealised model.
  **Neither is supported.** Category 1 (usefulness for protein structure) is excluded by K-105.
- **Theoretical level: L0.** There is no separation argument for OTOC(1) of this model. The analog route inherits no
  hardness theorem.
- **Practical level: L0.** No platform meets the σ budget; the best undemonstrated scenario is 1.2–6σ.
- **What is not claimed.**
  - This is not a proof that analog simulation of dipolar echoes can never reach σ.
  - The budget is an inference: per-channel errors are combined in quadrature, the atom-loss term uses an N = 12 lower
    bound, pulse-error accumulation is extrapolated from N = 8, and motion is modelled through the pos_indep curve.
  - S1/S1b parameters are my assumptions.
  - The native-traceless route is UNPROVEN physics.
- **Leakage.** No native structures were used for selection. The geometry is the ROUND3 instrument (PDB protons), used
  only as the fixed physics target.
- **Resources.**
  - About 46 CPU-min in total, single-threaded, all checkpointed:
    - validate 76 s;
    - sensitivity N = 10: 76 s; N = 12: 1,182 s; N = 14: 806 s;
    - Floquet 622 s;
    - budget < 1 s.
  - Peak RSS about 0.7 GB (N = 14). Simulator runtime is not physical quantum runtime: all "T_sim" figures are
    modelled device times.

## 9. Revival template (what would change the verdict)

The verdict changes only if **all** of these hold:

1. A programmable-geometry platform demonstrates a native or engineered traceless dipolar coupling (Jz/Jxy = −2) with
   an isotropic residual ≤ 1% and reversal via Floquet.
2. Per-atom loss is ≤ 0.5% and pulse error ≤ 0.003 rad over ≥ 80 cycles per leg.
3. Motion between legs is ≤ 0.04% of the spacing (in-trap Rydberg or ground-state-cooled atoms), in arbitrary-3D arrays
   of ≥ 100 atoms.
4. The classical T-X-early and spinDMFT tests show that X does **not** converge by N ≈ 26, so the hybrid fails at σ.

Even then, the result would be category-3 physics with no protein-structure value (K-105).

## 10. Files

| File | Contents |
|---|---|
| `ed_echo.py` | Exact continuous-time echo library (sector ED, forward/backward mismatch, R, two-point H) |
| `validate.py` → `validate.json` | Validation against ROUND3 N = 12 Chebyshev runs and internal identities |
| `sens_scan.py` → `sens_1UBQ_p{19,245}_N{10,12}.json`, `sens_1UBQ_p19_N14.json` | Error-channel scans (checkpointed per unit) |
| `analyze_sens.py` → `sens_summary.json` | Tolerances ε\* per channel |
| `floquet_composite.py` → `floquet_1UBQ_p{19,245}_N8.json`, `floquet_1UBQ_p19_N10.json` | ±C3 composite: Magnus, pulse and k errors. `floquet_1UBQ_p19_N6_test.json` is a functional test |
| `budget.py` → `budget.json`, `budget_stdout.txt` | Scenario budgets and requirements |
| `lit.json` | Literature verified this session, with what was read |
