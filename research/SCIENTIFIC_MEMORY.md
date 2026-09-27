# Scientific Memory

Durable lessons. Each entry has a date, a source, and a verification status. Entries are superseded by later dated entries and never deleted.

## 2026-09-26: Predecessor Sprint 33 findings (source: user summary; status: UNVERIFIED in this repo, pending reconstruction into `research/sprint33/`)

1. The strongest structural improvements came from better structural information and decoding.
2. CVaR-VQE did not produce a load-bearing improvement in the final built-chain result.
3. Tuned classical search matched or beat the quantum search in the tested regimes.
4. Several apparent quantum wins disappeared under stronger classical controls.
5. CVaR tail collapse and solver equivalence were important failure mechanisms.
6. The strongest architecture did not require the quantum stage.

**Implication:** No direction here, VQE included, gets a presumption of promise. Any quantum component must pass the quantum necessity test against a strong classical twin.

## 2026-09-26: Status update on the entry above (source: `research/sprint33/README.md` §5, §L3)

The six-point summary above was checked against the imported S33 sources. **None of the six points is contradicted.** Two carry qualifications that the source states:

- **Point 3.** Tuned classical search *beat* CVaR-VQE on register energy only (E1001: tuned SA 3.394 < VQE 3.457). On the built chain it *matched* it. The only equal-tuning chain test, E1000, gave −0.824 at 0.84x, which is NOT MEASURED, and seed 1 gave −0.066. Untrained random-prior sampling beat the trained VQE on the chain (+1.035, 1.35x, 2 seeds).
- **Point 5.** The source names four failure mechanisms, not two: solver-equivalence, tail collapse, register energies not transmitting to the chain (within-target ρ −0.08), and continuous search already being saturated by 32–64 restarts. Tail concentration is not quantum-specific, because SA tails concentrate too (E306).

The entry above keeps its wording. Its status is now: **consistent with source, with qualifications**.

## 2026-09-26: Cross-sprint evidence, predecessor S29–S33 (source: `research/sprint29/` … `research/sprint33/`; imported read-only from `cvar-vqe-protein-folding-v3@3d5b2d25`)

Measured results and the sprint's own interpretations are kept separate in the per-sprint files. This entry lists only what recurs across sprints, with pointers. The S29 contract records that this work originally ran in the `Protein-Folding-Algorithm` repository, branch `s26`.

**Measured, and consistent across S29–S33**
1. **The primary endpoint never moved.** Mean built-chain Cα RMSD on `tuning126` (126 targets, 9–16 aa) stayed at 3.2105 Å (DEP) from S29 through S33. No deployable arm cleared its MDE in the helpful direction (sprint29–33 README H1). S33 did find large gains at length: long40 (44–60 aa) went from avg75 9.745 to 4.739 (E308) and 4.343 (A80, a statistical tie). mid30 (25–40 aa) went from 8.180 to 3.717 or 3.815. These are quantum-free decoders on a learned pair prior, esmprior_v1 (sprint33 README H2–H4).
2. **The deployed CVaR-VQE stage was never load-bearing.**
   - S29: it is indistinguishable from a fixed, target-independent profile with no circuit (−0.0082 Å, 0.27x) (sprint29 H4).
   - S31: the deployed objective is convex with a closed-form "hinged Gibbs" minimiser, and the circuit is worse than p* on 126/126 (sprint31).
   - S32: production runs `quantum=False`, and no circuit was run (sprint32 H7).
   - S33: 34 chain-level VQE-vs-classical-twin contrasts, none in VQE's favour (sprint33 H5).
3. **Structural reasons given in the sources.**
   - For a diagonal Hamiltonian, the CVaR tail is a prefix of the energy order. This is the "set-equality theorem", identified as Barkoutsos et al. 2020 eq. (12) in S29, and S30's T1. One classical sort therefore reproduces the stage.
   - The solver-equivalence lemma (S33): any argmin-only readout gives the same chain whichever solver finds the argmin.
   - Every decision space at 9–16 aa is enumerable (2^n_res ≤ 65536) (S32).
   - S32 states that a quantum role needs "P1 — a decision space that GROWS WITH THE TARGET" and "P2 — a genuinely STOCHASTIC energy", and that "this project has never had either". S29 lit note L_4 says non-classicality needs non-commuting terms and a non-eigenvector prepared state, which "the project has never satisfied".
4. **Apparent quantum wins disappeared under stronger controls**: tuned SA, random sampling from the same prior, seed replication, and full-n re-runs (sprint33 README §5 point 4; `sprint33/QUANTUM_RESULTS.md`).
5. **ORACLE headroom exists, but deployable routes to it are closed.** Examples: the S29 ORACLE ceiling of the deployed architecture is 2.9027 Å, and five ORACLE signs per target are worth −0.3259 Å in S30. In the sources' own terms, the per-target sign or information is missing from all native-free channels (S29 L_8, S30 H3, S32 H6).

**Interpretations the predecessor reached** (attributed to the sources, not adopted here)
- "The bottleneck is information in esmprior_v1's long-range pair distributions … It is not search and not decoding." (S33 REPORT §1.7)
- "A structure estimate good enough to make the readout worth solving is already good enough to emit." (S32 THEORY_Q Q1-T2)
- "every VQE-vs-SA claim needs equal tuning effort, not just equal evaluation budget." (S33 SCIENTIFIC_MEMORY)

**Implications for this program** (a program-level judgement, not a finding from the sources)
- The predecessor's quantum stage was a diagonal-Hamiltonian argmin/tail sampler over small, enumerable registers. Any new architecture that reduces to that shape inherits these negative results. A candidate must be checked against three conditions before any experiment:
  - the decision space grows with target size, beyond enumeration;
  - the objective or readout depends on more than argmin or an energy-order prefix;
  - there is a non-diagonal (non-commuting) structure, or a sampling or estimation task, where a quantum primitive has a known complexity-theoretic role.
- The instruments, statistical contract (MDE = 2.8016·SE, fold CI, "< 0.7x is NOT A RESULT"), DEP/ORACLE discipline and adversary protocol are reusable as validated method. Source discrepancies are logged in each sprint's `LESSONS.md` importer notes.
