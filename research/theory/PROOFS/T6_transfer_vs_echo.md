# T6: why truncated classical dynamics reproduces NMR transfer but not echoes (mechanism note)

_Discovery sprint, 2026-09-27. Tags: DERIVED (short derivation here), THEORETICAL (literature), MEASURED (this sprint), INFERENCE. This note explains the C1/C3 observation. It is not a hardness proof._

## 1. Setting

- Heisenberg operator O(t) = Z_a(t) = Σ_P c_P(t) P under the secular dipolar Trotter circuit. Σ_P c_P² = 1 at γ = 0 (unitarity) (DERIVED).
- **Transfer:** S_ab(t) = c_{Z_b}(t), a single coefficient.
- **Echo (first-order OTOC):** F_ab(t) = 2^{-N} Tr[O Z_b O Z_b] = Σ_P c_P² s_P, where s_P = −1 if P has X or Y at site b, else +1. Equivalently F_ab = 1 − 2 W_b(t), with W_b(t) = Σ_{P: P_b ∈ {X,Y}} c_P² the operator weight that anticommutes with Z_b (DERIVED).

## 2. Why coefficient truncation reproduces transfer (MEASURED + THEORETICAL)

- Sparse Pauli dynamics keeps only strings with |c_P| > ε and discards the rest.
- The error in a *single* coefficient c_{Z_b}(t) comes only from discarded amplitude that would later flow back into Z_b.
- In interacting spin systems the operator's high-weight part rarely returns to low weight ("operator hydrodynamics"). Dissipating high-weight strings leaves transport observables intact. This is the basis of dissipation-assisted operator evolution (Rakovszky, von Keyserlingk & Pollmann, PRB 105, 075131, 2022; THEORETICAL, cited from the literature phase's classical-simulation review, not re-verified here).
- **MEASURED.** At N = 10, ε = 10⁻⁴ reproduces S_ab to < σ = 0.01 over 320 µs for every probe on 1UBQ and 1PGA, at γ ∈ {0, 1000, 5000} s⁻¹, and over 1 ms in the dilute amide-proton network. It uses 13–53×10³ strings, a minority of the charge-conserving operator space.

## 3. Why truncation fails for echoes (DERIVED)

1. **Echoes read the total weight, not one coefficient.** F_ab depends on W_b(t), a sum of c_P² over *all* strings with X/Y at b. After the operator front passes b, most of W_b sits in exponentially many high-weight strings with individually tiny coefficients. That is precisely the part coefficient truncation discards.
2. **The bias equals the lost norm.** With a kept set K, F_trunc = Σ_{P∈K} c_P² s_P, so F_true − F_trunc = Σ_{P∉K} c_P² s_P. MEASURED (1UBQ H/ILE3, N = 10, γ = 0): the lost norm 1 − Σ_K c² at 160 µs is 0.09 at ε = 10⁻⁴ and 0.39 at ε = 10⁻³; at 320 µs it is 0.14 and 0.52. The echo bias follows the lost norm, while S_ab stays accurate at ε = 10⁻⁴.
3. **Estimators that assume the discarded strings resemble the kept ones fail.**
   - The norm-corrected estimator Σ_K c² s / Σ_K c² assumes the discarded strings have the kept strings' anticommutation fraction. Discarded strings are higher weight and more likely to carry X/Y at b, so the assumption fails.
   - MEASURED: the norm-corrected estimator never moved the failure time later.
   - The α-calibrated mixture is fitted on N = 8 (α = 0.36 for probe 19, 0 for probe 245) and evaluated out of sample (C3; see the report).
4. **Transfer is local in operator space; the echo is global.** Transfer asks "how much of the operator is exactly Z_b". The echo asks "how much of the operator has any non-commuting content at b". The second is a property of the whole operator distribution. Its exact evaluation needs the full operator, i.e. the dynamics of every spin inside the light cone.

## 3b. Correction (2026-09-27, after the adversarial review `experiments/ADVERSARIAL/R1_SYNTHESIS.md`)

- At N = 10, sparse Pauli dynamics at ε = 3e-5 reproduces the echo within σ over the whole window for 4 of 6 jobs (MEASURED). It then holds ≈ 0.46–0.50 of the parity-allowed operator space, i.e. it is exact simulation in disguise.
- The correct statement is: **no compressed classical representation of the echo was found at any N ≤ 12**, from 9 approximation families. **Exact simulation reproduces it at seconds of cost.**
- The 10-spin reference is itself unconverged in cluster size (|F12 − F10| up to 0.46).
- Corrected ranges: echo/transfer FI ratio 3.2–183×; stored-panel f_hard^OTOC 0.49–1.0.

## 4. What this does and does not imply

- **It explains** why truncated approximations reproduce transfer at N = 10 (f_hard = 0) but need essentially the whole operator space for the echo (f_hard 0.49–1.0 against the ε ≥ 1e-4 panel; ≈ 0 at ε = 3e-5) (MEASURED).
- **It does not imply exponential classical hardness.** Two classical routes remain.
  - (a) **Exact simulation of the light cone.** The cost is exponential in the number of spins N_cone(t) the operator reaches by time t, not in the protein size. C2/C3 measure how the needed string count M*(N) grows with N at fixed accuracy. If N_cone at the informative times is ≤ ~30–40 spins, exact or sector methods remain feasible (sector-exact N = 14 takes ~15 min).
  - (b) **Coarse-grained front models.** For random circuits, averaged OTOCs map to classical stochastic front propagation (operator-spreading / FKPP-type descriptions; THEORETICAL, the Nahum–Vijay–Haah and von Keyserlingk et al. 2018 line, cited from memory, not re-verified). For a *specific* protein Hamiltonian, such a model is an approximation whose accuracy at σ = 0.01 is untested here. **It is the strongest untested classical adversary for the echo branch** (listed in OPEN_QUESTIONS).
- **Information vs hardness.** Echo FI exceeds transfer FI by 10–160× (MEASURED). A quantum forward model is only useful if the echo data are physically measurable (time reversal of the dipolar Hamiltonian, as in [F34]), survive embedding (R1-E), and if the needed light cone is beyond exact classical reach (C2/C3).
