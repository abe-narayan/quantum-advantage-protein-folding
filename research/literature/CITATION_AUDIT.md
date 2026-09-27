# Citation-key audit against BIBLIOGRAPHY.md

_Run 2026-09-26, after `research/literature/BIBLIOGRAPHY.md` was built (448 canonical entries, 531 keys). The coordinator can re-run it: `python audit.py show` in the scratchpad re-extracts every usage._

## Scope

Files scanned (all that existed at audit time):

| File | Key usages |
|---|---|
| research/literature/QUANTUM_PRIMITIVES.md | 197 |
| research/literature/OPPORTUNITY_MATRIX.md | 165 |
| research/literature/LITERATURE_REVIEW.md | 157 |
| research/literature/CLASSICAL_COUNTERARGUMENTS.md | 155 |
| research/literature/QUANTUM_ADVANTAGE_CLAIMS.md | 125 |
| research/literature/PROTEIN_BOTTLENECKS.md | 74 |
| research/THEORY_ROADMAP.md | 35 |
| research/QUANTUM_OPPORTUNITY_MAP.md | 33 |
| research/literature/OPEN_LITERATURE_GAPS.md | 29 |
| **Total** | **970 usages, 295 distinct keys, 409 citing sentences / table cells** |

**Method.** I extracted every bracketed group that contains a key: `[A12]`, lists such as `[A44, A45]`, ranges such as `[F52–F55]` and `[E60–E67]` (expanded), and equalities such as `[A57 = B46 = C65 = F66]`. Bracketed section pointers such as `[D §4]` and `[A §3.9]` were skipped. I then:

- checked (a) each key against the bibliography key index;
- read (b) every citing sentence next to the title of the canonical entry the key resolves to;
- compared the doubtful cases with the entry text in the source note (lit_A…lit_F).

## (a) Missing keys

**None.** All 295 distinct keys used resolve to a bibliography entry.

- No file cites the multi-paper keys `[D42]` or `[D48]` on their own.
- D42 appears only inside the range `[D42–D47]` (OPPORTUNITY_MATRIX.md:21, "PERM, REMC, Wang–Landau, CPSP"). Both D42 papers are PERM-family, so the range is unambiguous.

## (b) Suspicious key usages

| # | File:line | Key | What the sentence claims | What the paper actually is | Severity / fix |
|---|---|---|---|---|---|
| 1 | literature/PROTEIN_BOTTLENECKS.md:10 | **E94** | "AF-Cluster [E94]; disputes [E98, E99]" | E94 = #325 Chakravarty & Porter 2022, "AlphaFold2 fails to predict protein fold switching" (Protein Sci.). AF-Cluster is **E97** = #328 Wayment-Steele et al. 2024, "Predicting multiple conformations via sequence clustering and AlphaFold2" (Nature). E98 and E99 are the dispute over E97. | **Wrong key.** Change `[E94]` to `[E97]`. E94 could be kept as a separate citation for "AF2 misses fold switching". |
| 2 | literature/QUANTUM_PRIMITIVES.md:66 | A79 | "SMC and importance sampling with MCMC rejuvenation are not plain rejection sampling [A78, A79]" | A79 = #228 BioEmu (Lewis et al. 2025), an approximate generative emulator. It is not an SMC or importance-sampling method. A78 (Boltzmann generators: learned sampler plus reweighting) fits. | Weak support. The better classical references for SMC/IS are B65/E74 (SMC samplers, #96), B64/E75 (AIS, #95) and E79 (sequential Boltzmann generators, #312). |
| 3 | literature/OPPORTUNITY_MATRIX.md:16 (M6 row) | A79 | Classical competitor column: "SMC / importance sampling with MCMC [A78, A79]" | As #2. | Same fix as #2. |

## Minor observations (not errors)

- **OPPORTUNITY_MATRIX.md:15 (M5).** The chain "Wocjan et al. → Montanaro → Harrow–Wei → Arunachalam et al. → Cornelissen–Hamoudi" is cited as `[B24, B26–B28]`. Montanaro (B12 = A30 = D56, #54) is named but has no key there.
- **Experiment IDs share the key namespace.** Predecessor experiment IDs appear unbracketed and look like citation keys:
  - QUANTUM_OPPORTUNITY_MAP.md:42, 56, 57, 113: `E306`, `A80`, `A72`, `E720`, `A82`;
  - LITERATURE_REVIEW.md:210: `E406 → E1001`.

  A72 and A80 are also bibliography keys: A72 is Roget et al., #184, and A80 is the Mazzola review, #229. The text is unambiguous in context because citations are always bracketed. Still, a reader resolving "A72" through the key index would land on the wrong thing. Suggest prefixing experiment IDs (e.g. "exp-A72") or noting the convention once.
- **Metadata-only entry cited.** D46 (#244, Backofen & Will 2006, metadata-only) enters only through the range `[D42–D47]` as an example of an exact classical lattice solver. That is an existence use, which is acceptable. No other metadata-only or existence-only entry is cited: A60, D31, D33, D34, D48d, E1, E29, E30, E37 and E49 are unused.
- **Conflict-resolved entries.** No audited file uses A29's wrong title "Quantum algorithm for approximating partition functions"; they cite B24. No file cites C92's extra author or C98's "et al.".
- **Reviews used as evidence.** Several reviews carry a specific claim. Each claim is supported by a quote recorded in the source note:
  - B51 (Dalzell et al. survey, #446) for "QMC gives near-quadratic rates". Supported by the B51 §8.2 quote.
  - C21 (#124) for barren plateaus.
  - E60 and E62 (#299, #301) for TPS and WE.
  - E66 (#305) for MSMs.

## Borderline usages checked and judged OK

- **QUANTUM_PRIMITIVES.md:84 and OPPORTUNITY_MATRIX.md:14.** B46 (Babbush et al., #434) is cited for "Monte Carlo averaging is embarrassingly parallel". Supported: B46's note records the paper's parallel-speedup factor S (eq. 5) and its quote that quadratic speedups "apply to problems that are highly parallelizeable".
- **QUANTUM_ADVANTAGE_CLAIMS.md:29.** C42 (Albash & Lidar) is cited both for the claim and among the rebuttals. This is consistent with C42's own label: a limited advantage over SA and no advantage against SQA.
- **QUANTUM_ADVANTAGE_CLAIMS.md:71.** D21 (Doga et al., #191) is cited for the "beats AlphaFold2" fragment claim. C93 files this paper as a perspective, but D21's note records the hardware result and labels its accuracy advantage spurious. Consistent.
- **QUANTUM_PRIMITIVES.md:167.** F49 (QITE, #391) is cited for "for diagonal energies, imaginary-time evolution is classical Boltzmann reweighting". The statement is the authors' inference; F49 is correctly the QITE reference.
- **Expanded ranges.** Several ranges include papers that are not individually about the stated method, for example E61 (Huber & Kim WE) and E64 (milestoning) inside `[E60–E67]` for "WE, TPS, MSMs". All members are rare-event or kinetics methods, so the ranges are acceptable.
- **Row M11, OPPORTUNITY_MATRIX.md:21.** `[C1–C6]` includes C3 (ADAPT-VQE, molecular) and C5 (photonic VQE). Both are cited as the generic method references for the row's methods, which is acceptable.

## Tally

- Key usages: 970.
- Missing keys: 0.
- Suspicious usages: 3 (1 wrong key: E94 → E97; 2 weak supports: A79 for SMC/IS).
- **OK: 967.**

---
## Resolution (coordinator, 2026-09-26)
- `PROTEIN_BOTTLENECKS.md`: AF-Cluster re-keyed [E94] → [E97]. [E94] is kept for Chakravarty & Porter (AF2 fails on fold switching).
- `QUANTUM_PRIMITIVES.md` §1.6 and `OPPORTUNITY_MATRIX.md` M6: the SMC/AIS competitor was re-cited to [E74, E75] (Del Moral et al.; Neal). [A79] (BioEmu) was removed from that claim.
- Unbracketed experiment IDs (E306, E406, E1001, A72/A80/A82 as S33 architecture ids) are predecessor experiment or architecture identifiers, not citation keys. They are left as is. Bracketed [A72]/[A80] always mean bibliography keys.
