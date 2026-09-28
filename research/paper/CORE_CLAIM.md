# Core claim (discovery sprint, 2026-09-27)

## Main paper: a rigorous, scoped negative (claim categories 3 and 6, negative form)

> For protein structure computation driven by learned pair-distance energies, including sampling, optimisation, mode finding and estimation over the structure posterior at 30–150 residues, **no quantum algorithm offers a practical advantage under full fault-tolerant accounting**. Every route is at most quadratic in the quantised chain's gap or in the restart probability, relative to that same chain or those same restarts. For any quadratic sampling route, the per-sample quantum wall-clock at break-even satisfies a landscape-independent floor, T*_Q = Aρ(K n_b G t_T)²/c. With the measured coherent walk-step cost of a learned protein energy, G(L) ≈ 3×10⁴·L² Toffolis, this floor is months to millennia per sample, whatever the classical hardness of the landscape. A three-lens adversarial attack on 28 candidate mechanisms confirms that none survives above practical level L0.

- **Evidence class:** DERIVED (T1–T5 theory, resource model), MEASURED (landscape census, NRPT, break-even inputs), LITERATURE-SUPPORTED (quadratic ceilings, Sanders/Babbush break-even).
- **Scope:** one learned energy family (esmprior/A80), leakage-screened chains of 30–150 aa, fault-tolerant surface-code assumptions with logical Toffoli times of 1–170 µs.

## Secondary claim: quantum forward models of protein NMR

> In static protein ¹H dipolar networks, two-point polarisation transfer is reproduced by compressed classical dynamics. First-order dipolar echoes (OTOC(1)) are not: at least nine sub-exponential classical families fail, while exact simulation succeeds at the cluster sizes where it is feasible. As a route to structure, the echo is limited by three things: the physical time-reversal horizon (T3 ≈ 4–6.7 T2 in dipolar solids), forward-model errors, and a small information gain over classically usable data (≈ 1.1–1.5 under realistic priors). A fault-tolerant forward model beats exact classical simulation only for effective light cones of 30–47 spins, at hours per evaluation.

- **Evidence class:** MEASURED (sector-exact references, adversary panel, independent replication, embedding, noise attack), DERIVED (resource model), INFERENCE (transfer of reversal horizons to proteins).
- **Open residue:** R1-SIM, whether the converged echo light cone exceeds exact reach (see the discovery report).

## What is explicitly NOT claimed

- Any empirical, sampling, hardware, fault-tolerant or end-to-end quantum advantage for protein structure.
- That classical computation fails on protein NMR echoes. Only compressed approximations failed.
- Novelty of the NMR idea. It originates with O'Brien et al., PRX Quantum 3, 030345 (2022).
