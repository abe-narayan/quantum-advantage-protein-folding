# Provenance of vendored predecessor components

| Component | Source (read-only predecessor repo `C:/Users/abena/cvar-vqe-protein-folding-v3`, pinned 3d5b2d25) | Verification |
|---|---|---|
| `esmprior_v1.py` (network, pair inputs, predictor, ESM-2 650M bf16 featuriser) | `s33/esmprior.py` (last commit touching it: c113a29e), `s33/EXPERIMENTS/P_prior_featurise.py`, `s33/VERIFICATION/map_learned_esm_run.py` | Bit-exact reproduction on long40 1KNT: max \|Δ\| = 0.0 for rep, con, att and predicted prob / theta_tau_prob (2026-09-26) |
| `energy.py` (A80 energy, builder, soft tables, batched L-BFGS) | `s33/EXPERIMENTS/D_decoder_lib.py` lines 51–335 (verbatim; imports changed) | Same code; registers and VQE not copied (killed family) |
| Model files `data/models/esmprior_v1/*` | `s33/MODELS/esmprior_v1/`, `s33/MODELS/sepnull/`, `s33/ARTIFACTS/esm_train/heads.json` | SHA-256 in `data/models/esmprior_v1/SHA256.json` (also ESM-2 650M checkpoint hash) |

Training/leakage: esmprior_v1 saw 600 crops (≤72 aa) of 577 PDB entries. The LADDER instrument (`targets.py`) excludes those entries, any chain sharing a 9-mer with them or with the long40/mid30/tuning126 targets, and any chain with ≥0.4 gapless 30-residue identity to a training crop. ESM-2 pre-training (UniRef50) is uncontrolled.
