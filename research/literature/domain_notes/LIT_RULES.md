# Literature-agent rules (shared)

CONTEXT: You work for a research program asking "where, if anywhere, can quantum computing give a real, testable, scientifically defensible advantage for protein structure computation?". Read these two files first (they summarize the prior evidence):
- C:\Users\abena\quantum-advantage-protein-folding\research\QUANTUM_OPPORTUNITY_MAP.md
- C:\Users\abena\quantum-advantage-protein-folding\research\sprint29-33\README.md
Key prior evidence (predecessor sprints S29–S33, all simulation, 9–60 residues): 33 CVaR-VQE-style experiments (registers 7–171 qubits, diagonal classical costs) never improved the built-chain endpoint; equal-tuning simulated annealing and random prior sampling matched or beat VQE; outputs consumed via argmin / energy-ordered tail / convex weighting are classically reproducible (working hypothesis H-001). The one suggestive signal: a Boltzmann-weighted structural average beat keeping only lowest-energy states (mid-length, 1.40x MDE) — i.e. good SAMPLES of a learned-energy posterior may matter. Classical sampling hardness (mixing times) was never measured. Nothing beyond 60 residues.

YOUR JOB: a publication-grade literature investigation of your assigned domain. You are NOT writing the final review; you are producing structured evidence notes the coordinator will synthesize. Do not run experiments or write code for the project. Do not edit any file in the repo. Write ONLY your one output file in the scratchpad.

CITATION RULES (hard):
1. Do not fabricate. Every paper you list must be verified by you in this session via WebSearch/WebFetch of an authoritative page (arxiv.org abs page, doi.org / publisher page, DBLP, PubMed, Semantic Scholar/Crossref API). Record "Verified: <URL checked>". If you cannot verify a paper you believe exists, list it under "UNVERIFIED LEADS" with no metadata beyond what you're sure of, and never cite it as evidence.
2. Record for each paper: title, authors (first 3 + et al. ok), year, venue, DOI, arXiv id, URL.
3. Quote the key claim verbatim (short) where possible, with its location (abstract/theorem no.).
4. Prefer primary sources over reviews; use reviews only for orientation, flagged as such.

PER-PAPER FIELDS: algorithm; problem setting; claimed speedup (exact asymptotic statement if any); resource assumptions (oracle model, fault tolerance, qubits/T-count if given); classical comparator used; theoretical vs empirical; limitations; CLAIM LABEL(S) from: THEORETICAL SPEEDUP | QUERY-COMPLEXITY SPEEDUP | ASYMPTOTIC SPEEDUP | SAMPLING SPEEDUP | HEURISTIC ADVANTAGE | EMPIRICAL ADVANTAGE | HARDWARE DEMONSTRATION | SIMULATOR RESULT | ORACLE-MODEL RESULT | NO ADVANTAGE | ADVANTAGE DISPUTED.
Never convert query complexity into runtime, simulator into hardware, or weak-baseline wins into general advantage.

FOR EACH MAIN QUANTUM PRIMITIVE IN YOUR DOMAIN, answer the 16 questions:
1 what operation the QC performs; 2 what classical computation it replaces; 3 why that is hard classically; 4 exact speedup; 5 in query/time/sample/memory/other; 6 assumptions; 7 oracle needed; 8 oracle construction cost; 9 state-prep cost; 10 measurement/readout cost; 11 classical postprocessing cost; 12 strongest known classical algorithm; 13 does advantage survive against it; 14 fault tolerance needed?; 15 qubit/depth/gate/T-count requirements (from literature resource estimates); 16 natural mapping to a protein-structure subproblem?
Also give: STRONGEST CLASSICAL COUNTERARGUMENT (with citations); SCALING evidence (explicit asymptotics in residues / DOF / state-space size / temperature / mixing time / precision — do not infer from small numerics); NISQ route vs FAULT-TOLERANT route; relation to the S29–S33 evidence above (already tested? if so why it failed / what would be different).

OUTPUT: one markdown file at the path given in your task, sections: (1) Scope & search log (queries used); (2) Verified papers (per-paper fields); (3) Primitive analyses (16 questions each); (4) Strongest classical counterarguments; (5) Scaling statements; (6) NISQ vs FT; (7) Protein mapping + S29–S33 connection; (8) Literature gaps (novelty ≠ advantage); (9) Unverified leads; (10) Your bottom-line verdict per primitive: KILLED / WEAK / INTERESTING / PROMISING / HIGH PRIORITY, with one-paragraph justification. Be skeptical; a strong negative is acceptable. Aim for thoroughness (typically 25–50 verified papers). Final reply to coordinator ≤250 words: file path, # verified papers, verdicts.
