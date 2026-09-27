"""T3 resource model (v2, after review): Toffoli count / logical qubits / wall-clock / break-even for one coherent walk
step on the A80 learned energy.  Every formula is written out in research/theory/RESOURCE_MODELS.md (sections 2-3);
this script only evaluates them.  No quantum simulation, no fitting beyond two log-log slopes of measured timings.
Run:  python research/theory/T3_resource_model.py      (pure arithmetic, about a second; prints Markdown tables)

Literature inputs (verified against the PDFs in the T3 sessions, 2026-09-26/27): Sanders et al. 2020 (arXiv 2007.07391)
Tables IV, VI-IX and eqs (95)-(96), (190), (214); Babbush et al. 2021 (arXiv 2011.04149) eqs (1)-(7), (12), Table II;
Berry et al. 2019 (arXiv 1902.02134) App. C QROAM costs; Babbush et al. 2018 (arXiv 1805.03662) QROM 4L-4 T;
Gidney 2018 (arXiv 1709.06648) adder; Haner-Roetteler-Svore 2018 (arXiv 1805.12445) App. B-C;
Gidney-Ekera 2019 (arXiv 1905.09749) sec. 2.13-2.14 surface-code error model (10^-ceil(d/2+1) per qubit per cycle);
Gidney-Fowler 2019 (arXiv 1812.01238): CCZ every 5.5d cycles, ~1e10 states before an error at p = 1e-3.

v2 changes (review log in RESOURCE_MODELS.md sec. 9): fixed-point-validated b_w with build guard bits; bit-aligned
spline grid; b_acc = 40; Newton sqrt in the same n^2 convention as every other multiply; recounted chain build;
corrected surface-code exponent; kappa floors kappa_min(design, L); c_q / S / R / t_T grids; CCZ error budget;
R concurrent pair workspaces in the physical-qubit counts; stored frames used consistently.
"""
from __future__ import annotations

import math

LS = (30, 60, 100, 150, 200)

# ------------------------------------------------------------------------------------------ default parameters
# b_w is chosen from the fixed-point emulation (T3_table_fit_check.py --fixed-point, RESOURCE_MODELS.md sec. 3.2):
#   CENTRAL : smallest b_w (round-to-nearest, 4 guard bits in the build) whose pair-energy error sd on PILOT samples is
#             at most the classical 0.05 A table's own sd (classical parity), per measured L; extrapolated to L = 200.
#   GENEROUS: smallest b_w meeting sd <= 0.02 nats (TV <= ~0.01 between the fixed-point and the exact target).
# measured at L = 45, 60, 100, 120, 150 (round-to-nearest, 4 guard bits, g = 1024 + 64); L = 30 takes the L = 45 value;
# L = 200 is EXTRAPOLATED (+1 bit; INFERENCE).  Intermediate L take the next measured L (conservative).
BW_CENTRAL = {30: 22, 45: 22, 60: 22, 100: 23, 120: 23, 150: 24, 200: 25}
BW_GENEROUS = {30: 20, 45: 20, 60: 20, 100: 22, 120: 22, 150: 23, 200: 24}


def bw_rule(table):
    def f(L):
        ks = sorted(table)
        for k in ks:
            if L <= k:
                return table[k]
        return table[ks[-1]]
    return f


CENTRAL = dict(
    b=10,          # A1  bits per internal-coordinate angle register (lattice step 2*pi/1024 = 0.35 deg)
    bw=bw_rule(BW_CENTRAL),   # A2  working bits (coordinates, frame entries, s = d^2, Horner) -- fixed-point validated
    bc=None,       # A3  bits per spline coefficient (None -> = b_w)
    guard=4,       # A2  extra fractional bits carried through the chain build only
    p=3,           # A3  per-pair polynomial degree (cubic)
    gs=1024,       # A3  segments, bit-aligned grid s in [0, 2048) A^2, h = 2 A^2, knots at 4 and 16 A^2
    bacc=40,       # A4  energy accumulator / Delta-E register (worst case incl. clashes, L <= 200)
    bsm=7, bfun=7, # A5  coin precision (Sanders et al. choice)
    bx=16,         # D3  Cartesian coordinate bits
    Kd=6,          # D3  displacement directions per residue
    u=2.0,         # A9  compute+uncompute factor for per-term arithmetic temporaries
    sq=1.0,        # A6  squaring cost in units of bw^2 (1.0 conservative, 0.5 symmetric-square trick)
    newton_m=2,    # A8  Newton iterations for (inverse) square root
    ecarry=False,  # O-1 energy-carrying register (only D1/D2): one full energy per oracle instead of two
    store_frames=True,  # A12 frames (and the intermediate column) stored; False -> sqrt(L) checkpoints
    mulconv="n2",  # P3  "n2": b^2 per multiply (Sanders convention); "hrs": 1.5n^2+3np+1.5n-3p^2+3p, p=n/2
)
GENEROUS = dict(CENTRAL, bw=bw_rule(BW_GENEROUS), u=1.5, sq=0.5, ecarry=True)


def resolve(P, L):
    Q = dict(P)
    if callable(Q["bw"]):
        Q["bw"] = Q["bw"](L)
    if Q["bc"] is None:
        Q["bc"] = Q["bw"]
    return Q


# ------------------------------------------------------------------------------------------ primitive costs
def MUL(n, P):   # n x n -> n fixed-point multiply, Toffolis; round-to-nearest by a 2^(f-1) initial accumulator (free)
    if P.get("mulconv") == "hrs":
        p = n / 2
        return 1.5 * n * n + 3 * n * p + 1.5 * n - 3 * p * p + 3 * p
    return n * n


def SQ(n, P):
    return P["sq"] * MUL(n, P)


def ADD(n, P=None):  # Gidney 2018: n-1 Toffolis; we use n
    return n


def qroam(d, M):
    """Berry et al. 2019 (arXiv 1902.02134, App. C): compute ceil(d/k)+M(k-1), clean ancilla (k-1)M;
    measurement-based uncompute ceil(d/k')+k'.  Returns (Toffolis, ancilla)."""
    best = None
    for k in range(1, max(2, int(math.sqrt(d)) * 4)):
        c = math.ceil(d / k) + M * (k - 1)
        if best is None or c < best[0]:
            best = (c, (k - 1) * M)
    unc = min(math.ceil(d / k) + k for k in range(1, max(2, int(math.sqrt(d)) * 4)))
    return best[0] + unc, best[1]


def invsqrt_hrs(n, m, p=None):
    """Haner, Roetteler, Svore 2018 (arXiv 1805.12445) App. C, their own multiplier convention (upper bound, iterate
    uncomputation excluded).  Used only for the sensitivity row."""
    p = n // 2 if p is None else p
    return n * n * (7.5 * m + 3) + 15 * n * p * m + n * (11.5 * m + 5) - 15 * p * p * m + 15 * p * m - 2 * m


def invsqrt(n, m, P):
    """Same Newton iteration as HRS App. C (T_iter = 5 T_mul + 2 T_add per iteration), costed with OUR multiply
    convention; initial guess = HRS's m-independent term 3n^2 + 5n rescaled by T_mul^HRS ~ 2.25 n^2 -> MUL."""
    if P.get("mulconv") == "hrs":
        return invsqrt_hrs(n, m)
    return m * (5 * MUL(n, P) + 2 * ADD(n)) + (3 / 2.25) * MUL(n, P) + 5 * n


def sqrt_(n, m, P):
    return invsqrt(n, m, P) + MUL(n, P)


def LOG(P):  # -log(p) for p in [1e-6,1]: leading-one detection + QROM-interpolated mantissa polynomial (A10)
    bw = P["bw"]
    return 2 * bw + qroam(64, 2 * P["bc"])[0] + 2 * MUL(bw, P) + 2 * ADD(bw)


def C_fun(P):  # Sanders et al. 2020 eq. (96): arcsine-of-sqrt-of-exp by QROM interpolation
    bsm, bfun = P["bsm"], P["bfun"]
    return (bsm + bfun) ** 2 + P["bacc"] + bsm * math.ceil(math.log2(bsm)) + 2 ** (bfun / 2)


# ------------------------------------------------------------------------------------------ counts
def n_pairs(L):
    return (L - 2) * (L - 3) // 2          # pairs |i-j| >= 3


def n_ang(L):
    return 2 * L - 5                       # theta (L-2) + tau (L-3)


def IX(L):                                 # integer bits of an Angstrom coordinate (|X| <= 3.8(L-1) + CB offset)
    return math.ceil(math.log2(3.8 * (L - 1) + 2))


def sqdist(P, L):
    """3 differences + saturation (|dX_c| >= 64 A or s >= 2048 A^2 -> top of grid) + 3 squarings + 2 additions."""
    bw = P["bw"]
    sat = 3 * max(IX(L) - 5, 0) + 2 * bw
    return 3 * ADD(bw) + sat + 3 * SQ(bw, P) + 2 * ADD(bw)


def horner(P):
    return P["p"] * (MUL(P["bw"], P) + ADD(P["bw"]))


NFINE = 64                                 # A3: fine sub-grid h_f = 1/16 A^2 on s < 4 A^2 (CB cusp at s = 0)


def fine_select(P):
    """s < 4 test (OR of the high bits), controlled 5-bit shift of the local coordinate, index select: ~3 b_w."""
    return 3 * P["bw"]


def pair_term(design, L, P):
    """Toffolis to add ONE pair term f_ij(d) into the accumulator and clean its temporaries (A9)."""
    bw, bc = P["bw"], P["bc"]
    if design == "D1":   # literal: sqrt, 1001-point grid table (0.05 A), linear interpolation
        arith = sqdist(P, L) + sqrt_(bw, P["newton_m"], P) + 2 * ADD(bw) + MUL(bw, P) + ADD(bw)
        look, anc = qroam(1001, 2 * bc)
    elif design == "D2":  # per-pair cubic in s = d^2, pair index classical
        arith = sqdist(P, L) + fine_select(P) + horner(P)
        look, anc = qroam(P["gs"] + NFINE, (P["p"] + 1) * bc)
    elif design == "D3":  # per-pair cubic in s, pair index quantum (moved residue r): table over (r, segment)
        arith = sqdist(P, L) + fine_select(P) + horner(P) + 2 * math.ceil(math.log2(L))   # + |r-j|>=3 flag
        look, anc = qroam(L * (P["gs"] + NFINE), (P["p"] + 1) * bc)
    elif design == "D3c":  # D3 inside Szegedy: move index classical, so the table is per pair again
        arith = sqdist(P, L) + fine_select(P) + horner(P)
        look, anc = qroam(P["gs"] + NFINE, (P["p"] + 1) * bc)
    elif design in ("D2sb", "D3sb"):  # soft-bin shared basis: -log(sum_k P_ijk S_k(s) + eps), W active bins
        W = 5
        arith = sqdist(P, L) + W * MUL(bw, P) + W * MUL(bw, P) + LOG(P)    # basis (linear interp) + dot + log
        l1, a1 = qroam(2048, W * 2 * bc)                                   # shared basis slopes/intercepts
        l2, a2 = qroam(24 * (L if design == "D3sb" else 1), W * bc)        # weight window (pair classical / quantum)
        look, anc = l1 + l2, max(a1, a2)
        if design == "D3sb":
            arith += 2 * math.ceil(math.log2(L))
    elif design == "D2svd":  # global shared rank-R basis f_ij = mu + sum_r a_ijr phi_r(s), R=64 (fit check)
        R = 64
        arith = sqdist(P, L) + 2 * MUL(bw, P) + 3 * R * MUL(bw, P) + R * (bc // 2) * bw
        look, anc = P["gs"], 0
    else:
        raise ValueError(design)
    return P["u"] * arith + look + ADD(P["bacc"]), anc


def build_res(P):
    """Forward cost of one residue of the sequential chain build at nb = b_w + guard bits (A11, recounted):
    F Rx(tau): 12 MUL (cols 1,2); (F Rx) Rz(pi-theta): 12 MUL (cols 0,1); CB offset F v(theta): 9 MUL;
    bond 3.8*col0(F): 3 constant multiplies ~ 1.5 nb^2; 24 additions; lookups (cos, sin, v(theta)) and (cos, sin);
    rounding X and CB from nb to b_w bits: 6 additions.  The intermediate column (F Rx)_col1 is STORED (3 nb qubits,
    zero Toffolis) when frames are stored, otherwise uncomputed (+6 MUL +3 ADD)."""
    nb, b = P["bw"] + P["guard"], P["b"]
    c = 33 * MUL(nb, P) + 1.5 * nb * nb + 24 * ADD(nb) + qroam(2 ** b, 5 * nb)[0] + qroam(2 ** b, 2 * nb)[0] \
        + 6 * ADD(P["bw"])
    if not P["store_frames"]:
        c += 6 * MUL(nb, P) + 3 * ADD(nb)
    return c


def build_torsion(L, P):
    return (L - 2) * build_res(P)


def build_torsion_parallel_prefix(L, P):
    """Hillis-Steele scan as in the classical code: ceil(log2 L) levels x L general affine products (36 MUL)."""
    nb = P["bw"] + P["guard"]
    return math.ceil(math.log2(L)) * L * 36 * MUL(nb, P) + (L - 2) * (qroam(2 ** P["b"], 5 * nb)[0] +
                                                                  qroam(2 ** P["b"], 2 * nb)[0])


def head_torsion(L, P):
    """Delta of the single (theta,tau) head term of the moved residue (old and new), incl. temporaries."""
    bc, b = P["bc"], P["b"]
    one = (qroam(2 ** b, 3 * bc + 4)[0] + qroam(2 ** b, 3 * bc + 5)[0] + qroam((L - 3) * 9 * 24, 9 * bc)[0]
           + 12 * MUL(bc, P) + LOG(P))
    return 2 * P["u"] * one


def move_apply_torsion(L, P):   # quantum-indexed +-delta add on the angle register (unary iteration), wrap-around
    return n_ang(L) * (2 * P["b"] + 1)


def C_E_torsion(design, L, P):
    """One full energy of one structure: build + unbuild + all 2*n_pairs pair terms (CA with sterics folded, CB);
    with sqrt(L) checkpoints (store_frames False) one extra build + unbuild."""
    pt, _ = pair_term(design, L, P)
    nbuild = 2 if P["store_frames"] else 4
    return nbuild * build_torsion(L, P) + 2 * n_pairs(L) * pt


def C_diff_torsion(design, L, P):
    ncall = 1 if P["ecarry"] else 2      # O-1: |x>|E(x)> carried; the oracle computes only E(x + delta_j)
    return ncall * C_E_torsion(design, L, P) + 2 * move_apply_torsion(L, P) + head_torsion(L, P) + ADD(P["bacc"])


# ---- Cartesian (D3)
def cb_cart(P):
    bw = P["bw"]
    return 5 * invsqrt(bw, P["newton_m"], P) + 25 * MUL(bw, P) + 15 * ADD(bw)


def head_cart(L, P):
    bw, bc = P["bw"], P["bc"]
    atan2 = 1.5 * sqrt_(bw, P["newton_m"], P)            # proxy: HRS arcsine ~ poly + invsqrt
    return (2 * invsqrt(bw, P["newton_m"], P) + 20 * MUL(bw, P) + atan2 + 2 * (64 + 3 * MUL(bw, P))
            + qroam((L - 3) * 9 * 24, 9 * bc)[0] + 12 * MUL(bc, P) + LOG(P))


def C_diff_cart(L, P, classical_move=False):
    bx = P["bx"]
    design = "D3c" if classical_move else "D3"
    pt, _ = pair_term(design, L, P)
    n_terms = 4 * (L - 5)                                  # CA pairs of r + CB pairs of r-1, r, r+1
    read = 0 if classical_move else 2 * L * (1 + 21 * bx)  # window of 7 residues read by quantum index r (+unread)
    cb = 3 * 2 * P["u"] * cb_cart(P)
    head = 5 * 2 * P["u"] * head_cart(L, P)
    bond = 2 * 2 * (P["u"] * (sqdist(P, L) + horner(P)) + qroam(64, (P["p"] + 1) * P["bc"])[0] + ADD(P["bacc"]))
    return read + 2 * n_terms * pt + cb + head + bond, dict(read=read, pairs=2 * n_terms * pt, cb=cb, head=head,
                                                             bond=bond)


def move_apply_cart(L, P):
    return L * (3 * 2 * P["bx"] + 1)


# ------------------------------------------------------------------------------------------ walk steps
def n_moves(design, L, P):
    return P["Kd"] * L if design == "D3" else 2 * n_ang(L)


def overhead(M, P):
    k = math.ceil(math.log2(M))
    CV = 2 * (4 * k + 2 * P["bsm"] - 13)                  # Sanders: V and V^dagger
    CR = k + 1
    return CV + CR


def coin(P):
    return 2 * C_fun(P) + 2 * P["bacc"] + 2 * P["bsm"]


def G_lhpst(design, L, P):
    P = resolve(P, L)
    M = n_moves(design, L, P)
    if design == "D3":
        Cd = C_diff_cart(L, P)[0]
        CF = move_apply_cart(L, P)
    else:
        Cd = C_diff_torsion(design, L, P)
        CF = move_apply_torsion(L, P)
    return 2 * Cd + coin(P) + CF + 1 + overhead(M, P), dict(C_diff=Cd, coin=coin(P), F=CF + 1, VR=overhead(M, P))


def pair_share(design, L, P):
    G, _ = G_lhpst(design, L, P)
    Q = resolve(P, L)
    pt, _ = pair_term(design, L, Q)
    if design == "D3":
        pairs = 2 * 2 * 4 * (L - 5) * pt
    else:
        pairs = 2 * (1 if Q["ecarry"] else 2) * 2 * n_pairs(L) * pt
    return pairs / G


def G_szegedy(design, L, P):
    """Sanders et al. 2020 eq. (190): min(2(M+1) C_direct, 2M C_diff) + 2M C_fun + 2M log M + 8M b_sm + 18 b_sm^2."""
    P = resolve(P, L)
    M = n_moves(design, L, P)
    if design == "D3":
        main = 2 * M * C_diff_cart(L, P, classical_move=True)[0]
    else:
        Q = dict(P, ecarry=False)
        C_direct = C_E_torsion(design, L, Q) + L * head_torsion(L, Q) / 2
        main = 2 * (M + 1) * C_direct
    return main + 2 * M * C_fun(P) + 2 * M * math.ceil(math.log2(M)) + 8 * M * P["bsm"] + 18 * P["bsm"] ** 2


# ------------------------------------------------------------------------------------------ qubits
def pair_workspace(design, L, P):
    P = resolve(P, L)
    _, anc = pair_term(design, L, P)
    return 12 * P["bw"] + (P["p"] + 1) * P["bc"] + anc


def qubits_lhpst(design, L, P):
    P = resolve(P, L)
    b, bw, bc, bacc = P["b"], P["bw"], P["bc"], P["bacc"]
    nb = bw + P["guard"]
    M = n_moves(design, L, P)
    common = math.ceil(math.log2(M)) + 1 + 1 + 3 * bacc + (2 * P["bsm"] + P["bfun"] + 3)
    if design == "D3":
        _, anc = pair_term("D3", L, P)
        sysq = 3 * L * P["bx"]
        work = 2 * 7 * 3 * P["bx"] + 40 * bw + 12 * bw + (P["p"] + 1) * bc + anc + bw * (P["newton_m"] + 4)
        return sysq + work + common
    _, anc = pair_term(design, L, P)
    sysq = n_ang(L) * b
    if P["store_frames"]:
        struct = 18 * nb * L                                   # X, CB, F (9), (F Rx)_col1 (3) per residue
    else:
        struct = 6 * bw * L + 2 * 12 * nb * math.ceil(math.sqrt(L))   # coordinates + checkpoints + working segment
    work = 12 * bw + (P["p"] + 1) * bc + anc + (bw * (P["newton_m"] + 4) if design == "D1" else 0)
    return sysq + struct + work + common


def qubits_szegedy(design, L, P):
    Q = resolve(P, L)
    M = n_moves(design, L, Q)
    base = qubits_lhpst(design, L, P)
    sysq = 3 * L * Q["bx"] if design == "D3" else n_ang(L) * Q["b"]
    return base + sysq + M * (Q["bacc"] + 2 * Q["bsm"] + Q["bfun"]) + 5 * Q["bsm"]


# ------------------------------------------------------------------------------------------ hardware / break-even
T_TOFF = 170e-6          # s, one CCZ factory, d=31, 1 us cycle (Sanders et al. 2020; Babbush et al. 2021 eq. 6)
FACTORY_PHYS = 1.5e5     # physical qubits per factory region at d=31 (Sanders et al. 2020)
EPS_CCZ = 1e-10          # Gidney-Fowler 2019: ~1e10 CCZ states on average before an error (p = 1e-3, minimal distances)
EPS_CCZ_BIG = 1e-12      # ... ~1e12 with a ~20% larger factory footprint


def phys_qubits(nL, d=31, factories=1):
    return 2 * (d + 1) ** 2 * nL + factories * FACTORY_PHYS * (d / 31) ** 2   # Gidney-Ekera 2019: 2(d+1)^2 / logical


def d_required(nL, seconds, p_fail=0.1):
    """Gidney-Ekera 2019 sec 2.13: logical error per qubit per 1-us cycle ~ 10^(-ceil(d/2 + 1)) at p = 1e-3."""
    cycles = seconds / 1e-6
    need = p_fail / (nL * cycles)
    d = 3
    while 10 ** (-math.ceil(d / 2 + 1)) > need:
        d += 2
    return d


def t_C_placeholder(L):
    return 0.2e-3 * (L / 45) ** 2          # PLACEHOLDER (task-specified), seconds per energy+gradient


# measured calibration points (seconds per energy+gradient); see RESOURCE_MODELS.md C2
TC_PILOT = {45: 330.8678 / 559860, 60: 399.1404 / 510960, 100: 697.9654 / 477710, 120: 933.2727 / 390210,
            150: 1315.4007 / 374810}          # PILOT: secs / grad_evals_total in research/results/RAW/g1_pilot/*.json
TC_TORCH = {30: 0.29e-3, 45: 0.97e-3, 60: 1.40e-3, 100: 2.94e-3, 150: 5.44e-3}   # PyTorch batch-64 (T3 v1 session)
PILOT_RUNS = {45: (1500, 393000), 60: (1200, 336000), 100: (800, 274400), 120: (600, 195000),
              150: (500, 171500)}             # (scans, grad_evals_production), 0 round trips in every run


def powerfit(pts):
    xs = [math.log(k) for k in pts]
    ys = [math.log(v) for v in pts.values()]
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    g = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    a = math.exp(my - g * mx)
    return (lambda L: a * L ** g), g


def kappa_min(design, L, cached=False):
    """Floor kappa >= t_C / t_W^cl (the best classical sampler is at least as good as P_W run classically).
    Pair-term counting, energy-only term costed like an energy+gradient term (favours quantum):
    torsion: E+grad touches 2 n_p terms, one single-angle Metropolis step ~ 4 * L^2/6 (2 channels, old+new) -> 1.5;
             with cached per-pair energies (new only) -> 3.
    D3:      one single-residue step re-evaluates 2 * 4(L-5) terms -> n_p / (4(L-5)); cached -> n_p / (2(L-5))."""
    if design == "D3":
        return n_pairs(L) / ((2 if cached else 4) * (L - 5))
    return 3.0 if cached else 1.5


def breakeven(G, L, S=1, R=1, kappa=1.0, cq=1.0, tC=None, tT=T_TOFF):
    tC = t_C_placeholder(L) if tC is None else tC
    tQ = G * tT / R
    B = kappa * (cq * S * tQ / tC) ** 2
    Tstar = B * tC / S
    Ntoff = cq * math.sqrt(kappa * B) * G            # Toffolis in one quantum sample-run at break-even
    return B, Tstar, tQ, Ntoff


def fmt(x):
    if x == 0:
        return "0"
    e = int(math.floor(math.log10(abs(x))))
    return f"{x / 10 ** e:.1f}e{e}"


def human_t(s):
    for unit, v in (("yr", 3.156e7), ("d", 86400), ("h", 3600), ("min", 60), ("s", 1), ("ms", 1e-3)):
        if s >= v:
            return f"{s / v:.3g} {unit}"
    return f"{s * 1e6:.3g} us"


DES = (("D1", "central", CENTRAL), ("D1", "generous", GENEROUS), ("D2", "central", CENTRAL),
       ("D2", "generous", GENEROUS), ("D3", "central", CENTRAL), ("D3", "generous", GENEROUS))


def main():
    P = resolve(CENTRAL, 100)
    print("## Primitive costs (central parameters at L=100, b_w = %d)\n" % P["bw"])
    print(f"- sqdist = {sqdist(P, 100):.0f}; horner(p=3) = {horner(P):.0f}; sqrt (n^2 convention, m=2) = "
          f"{sqrt_(P['bw'], 2, P):.0f}; sqrt (HRS convention) = {invsqrt_hrs(P['bw'], 2) + MUL(P['bw'], P):.0f}; "
          f"LOG = {LOG(P):.0f}; C_fun = {C_fun(P):.0f}; coin per step = {coin(P):.0f}")
    print(f"- build per residue = {build_res(P):.0f} (stored frames)")
    for label, PP in (("central", CENTRAL), ("generous", GENEROUS)):
        for des in ("D1", "D2", "D3"):
            print(f"- pair term {des} {label}: " + ", ".join(
                f"L={L}: {pair_term(des, L, resolve(PP, L))[0]:.0f}" for L in LS) + "; b_w = " +
                  ", ".join(str(resolve(PP, L)["bw"]) for L in LS))
    print(f"- head (torsion, moved residue) L=150: {head_torsion(150, resolve(CENTRAL, 150)):.3g}; CB_cart "
          f"{cb_cart(resolve(CENTRAL, 150)):.3g}; head_cart {head_cart(150, resolve(CENTRAL, 150)):.3g}")

    for label, PP in (("CENTRAL", CENTRAL), ("GENEROUS", GENEROUS)):
        print(f"\n## G(L): Toffolis per walk step, {label}\n")
        print("| design | step | " + " | ".join(f"L={L}" for L in LS) + " |")
        print("|---|---|" + "---|" * len(LS))
        for des in ("D1", "D2", "D3"):
            print(f"| {des} | LHPST | " + " | ".join(fmt(G_lhpst(des, L, PP)[0]) for L in LS) + " |")
            print(f"| {des} | Szegedy | " + " | ".join(fmt(G_szegedy(des, L, PP)) for L in LS) + " |")
        for des in ("D1", "D2", "D3"):
            print(f"- ratio Szegedy/LHPST {des}: " + ", ".join(f"{G_szegedy(des, L, PP) / G_lhpst(des, L, PP)[0]:.0f}"
                                                           for L in LS))
        print(f"\n## share of pair terms in G_LHPST ({label})\n")
        for des in ("D1", "D2", "D3"):
            print(f"- {des}: " + ", ".join(f"{pair_share(des, L, PP):.3f}" for L in LS))

    print("\n## Non-pair pieces of the LHPST step (central): coin, C_F (incl. sign flip), V+R, in-oracle moves 2*C_move\n")
    for des in ("D2", "D3"):
        for L in LS:
            G, parts = G_lhpst(des, L, CENTRAL)
            Q = resolve(CENTRAL, L)
            mv = 2 * 2 * move_apply_torsion(L, Q) if des == "D2" else 0
            print(f"- {des} L={L}: coin {parts['coin']:.0f}, C_F {parts['F']:.0f}, V+R {parts['VR']:.0f}, "
                  f"4*C_move {mv:.0f}; sum/G = {(parts['coin'] + parts['F'] + parts['VR'] + mv) / G:.1e}")

    print("\n## D3 cost breakdown of C_diff at L=150 (central)\n")
    Cd, br = C_diff_cart(150, resolve(CENTRAL, 150))
    print("- " + ", ".join(f"{k} {v:.3g}" for k, v in br.items()) + f"; C_diff {Cd:.3g}")
    print("\n## D3 local growth exponents d log G / d log L\n")
    for label, PP in (("central", CENTRAL), ("generous", GENEROUS)):
        ex = []
        for a, b in zip(LS[:-1], LS[1:]):
            ex.append(math.log(G_lhpst("D3", b, PP)[0] / G_lhpst("D3", a, PP)[0]) / math.log(b / a))
        print(f"- {label}: " + ", ".join(f"{a}-{b}: {e:.2f}" for (a, b), e in zip(zip(LS[:-1], LS[1:]), ex)))

    print("\n## Logical qubits (central; stored frames unless stated)\n")
    print("| design | step | " + " | ".join(f"L={L}" for L in LS) + " |")
    print("|---|---|" + "---|" * len(LS))
    for des in ("D1", "D2", "D3"):
        print(f"| {des} | LHPST | " + " | ".join(fmt(qubits_lhpst(des, L, CENTRAL)) for L in LS) + " |")
        if des != "D3":
            PB = dict(CENTRAL, store_frames=False)
            print(f"| {des} | LHPST, sqrt(L) checkpoints | " + " | ".join(fmt(qubits_lhpst(des, L, PB)) for L in LS)
                  + " |")
        print(f"| {des} | Szegedy | " + " | ".join(fmt(qubits_szegedy(des, L, CENTRAL)) for L in LS) + " |")
    print("\n- checkpointed-frame Toffoli penalty (D2 central): " + ", ".join(
        f"L={L}: +{(G_lhpst('D2', L, dict(CENTRAL, store_frames=False))[0] / G_lhpst('D2', L, CENTRAL)[0] - 1) * 100:.1f}%"
        for L in LS))

    print("\n## Wall-clock per LHPST step and physical qubits (central; d=31 unless stated)\n")
    print("| design | L | G | t_step R=1 | R=10 | R=100 | R=1000 | n_L | phys (1 factory, d=31) | "
          "phys (100 factories + 99 pair workspaces, d=31) | d_req(1 step) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|")
    for des in ("D1", "D2", "D3"):
        for L in LS:
            G = G_lhpst(des, L, CENTRAL)[0]
            nL = qubits_lhpst(des, L, CENTRAL)
            nL100 = nL + 99 * pair_workspace(des, L, CENTRAL)
            ts = G * T_TOFF
            print(f"| {des} | {L} | {fmt(G)} | {human_t(ts)} | {human_t(ts / 10)} | {human_t(ts / 100)} | "
                  f"{human_t(ts / 1000)} | {fmt(nL)} | {fmt(phys_qubits(nL))} | "
                  f"{fmt(phys_qubits(nL100, factories=100))} | {d_required(nL, ts)} |")

    print("\n## Classical time per energy+gradient: placeholder and measured fits\n")
    fP, gP = powerfit(TC_PILOT)
    fT, gT = powerfit(TC_TORCH)
    print(f"- PILOT (PT wall-clock incl. overhead): t_C ~ L^{gP:.2f}; PyTorch batch-64: t_C ~ L^{gT:.2f}; "
          f"placeholder L^2")
    for L in LS:
        print(f"- L={L}: placeholder {t_C_placeholder(L) * 1e3:.3f} ms; PILOT fit {fP(L) * 1e3:.3f} ms; "
              f"PyTorch fit {fT(L) * 1e3:.3f} ms; ratio^2 placeholder/PILOT {(t_C_placeholder(L) / fP(L)) ** 2:.2g}, "
              f"placeholder/PyTorch {(t_C_placeholder(L) / fT(L)) ** 2:.2g}")
    for L in sorted(set(TC_PILOT) | set(TC_TORCH)):
        a = (TC_PILOT[L] / t_C_placeholder(L)) ** 2 if L in TC_PILOT else None
        b = (TC_TORCH[L] / t_C_placeholder(L)) ** 2 if L in TC_TORCH else None
        print(f"- measured points L={L}: B(measured)/B(placeholder) = "
              f"{'' if a is None else f'PILOT 1/{a:.2g}'} {'' if b is None else f'PyTorch 1/{b:.2g}'}")

    for label, PP in (("CENTRAL", CENTRAL), ("GENEROUS", GENEROUS)):
        print(f"\n## Break-even B(L) (energy+gradient evals per sample), kappa = kappa_min(design, L), c_q = 1, "
              f"placeholder t_C, {label}\n")
        print("| design | S | R | " + " | ".join(f"L={L}" for L in LS) + " |")
        print("|---|---|---|" + "---|" * len(LS))
        for des in ("D1", "D2", "D3"):
            for S, R in ((1, 1), (1, 100), (1e3, 100), (1e3, 1000)):
                cells = []
                for L in LS:
                    B, Ts, _, _ = breakeven(G_lhpst(des, L, PP)[0], L, S=S, R=R, kappa=kappa_min(des, L))
                    cells.append(f"{fmt(B)} ({human_t(Ts)})")
                print(f"| {des} | {fmt(S)} | {R} | " + " | ".join(cells) + " |")
        print("\n- kappa_min: torsion 1.5; D3 " + ", ".join(f"L={L}: {kappa_min('D3', L):.1f}" for L in LS))
        print("- reference line kappa = 1 (INFEASIBLE, below the floor), S=1, R=100: " + "; ".join(
            f"{des} " + ", ".join(fmt(breakeven(G_lhpst(des, L, PP)[0], L, S=1, R=100)[0]) for L in LS)
            for des in ("D2", "D3")))

    print("\n## B under measured t_C (PILOT power-law fit), kappa_min, c_q = 1, S = 1 and 1e3, R = 100\n")
    print("| design | params | S | " + " | ".join(f"L={L}" for L in LS) + " |")
    print("|---|---|---|" + "---|" * len(LS))
    for des, lab, PP in DES:
        for S in (1, 1e3):
            print(f"| {des} | {lab} | {fmt(S)} | " + " | ".join(
                fmt(breakeven(G_lhpst(des, L, PP)[0], L, S=S, R=100, kappa=kappa_min(des, L), tC=fP(L))[0])
                for L in LS) + " |")

    print("\n## H-008 B-clause grid at L = 100 (B <= 1e12 ?), placeholder t_C, R = 100 (R = 1000: divide by 100)\n")
    print("| design | params | kappa | S=1,cq=1 | S=1,cq=10 | S=1,cq=90 | S=1e3,cq=1 | S=1e3,cq=10 | S=1e3,cq=90 | "
          "S_max(cq=1) for B<=1e12 |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    L = 100
    for des, lab, PP in DES:
        G = G_lhpst(des, L, PP)[0]
        for kname, k in (("kappa_min=%.3g" % kappa_min(des, L), kappa_min(des, L)), ("50", 50.0), ("L=100", 100.0)):
            cells = []
            for S in (1, 1e3):
                for cq in (1, 10, 90):
                    B = breakeven(G, L, S=S, R=100, kappa=k, cq=cq)[0]
                    cells.append(fmt(B) + (" ok" if B <= 1e12 else (" F" if B > 1e15 else "")))
            B1 = breakeven(G, L, S=1, R=100, kappa=k, cq=1)[0]
            smax = math.sqrt(1e12 / B1)
            print(f"| {des} | {lab} | {kname} | " + " | ".join(cells) + f" | {smax:.3g} |")

    print("\n## Hardware envelope: B at L = 100 vs effective Toffoli time t_T/R, kappa_min, c_q = 1\n")
    envs = (("170 us, R=1", 170e-6, 1), ("170 us, R=100", 170e-6, 100), ("170 us, R=1000", 170e-6, 1000),
            ("10 us, R=100", 10e-6, 100), ("1 us, R=100", 1e-6, 100), ("1 us, R=1000", 1e-6, 1000))
    print("| design | params | S | " + " | ".join(e[0] for e in envs) + " |")
    print("|---|---|---|" + "---|" * len(envs))
    for des, lab, PP in DES:
        G = G_lhpst(des, 100, PP)[0]
        for S in (1, 1e3):
            cells = []
            for _, tT, R in envs:
                B, Ts, _, _ = breakeven(G, 100, S=S, R=R, kappa=kappa_min(des, 100), tT=tT)
                cells.append(f"{fmt(B)} ({human_t(Ts)})")
            print(f"| {des} | {lab} | {fmt(S)} | " + " | ".join(cells) + " |")

    print("\n## Pilot PT lower bounds vs B at the same L (placeholder t_C; kappa_min; c_q = 1)\n")
    print("| L | scans | grad_evals_production (63% bound) | 95% bound (= /3) | B D3 gen S=1 R=100 | ratio | "
          "B D2 cen S=1e3 R=100 | ratio | B D2 gen S=1e3 R=1000 | ratio | D3 gen S=1 R=100 with PILOT t_C | ratio |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|")
    for L, (scans, prod) in PILOT_RUNS.items():
        b95 = prod / 3
        B1 = breakeven(G_lhpst("D3", L, GENEROUS)[0], L, S=1, R=100, kappa=kappa_min("D3", L))[0]
        B2 = breakeven(G_lhpst("D2", L, CENTRAL)[0], L, S=1e3, R=100, kappa=kappa_min("D2", L))[0]
        B3 = breakeven(G_lhpst("D2", L, GENEROUS)[0], L, S=1e3, R=1000, kappa=kappa_min("D2", L))[0]
        B4 = breakeven(G_lhpst("D3", L, GENEROUS)[0], L, S=1, R=100, kappa=kappa_min("D3", L), tC=TC_PILOT[L])[0]
        print(f"| {L} | {scans} | {fmt(prod)} | {fmt(b95)} | {fmt(B1)} | {fmt(B1 / b95)} | {fmt(B2)} | {fmt(B2 / b95)}"
              f" | {fmt(B3)} | {fmt(B3 / b95)} | {fmt(B4)} | {fmt(B4 / b95)} |")

    print("\n## Self-consistent code distance at break-even and CCZ error budget (kappa_min, c_q = 1; stored frames)\n")
    print("| design | params | L | S | R | n_L (+R-1 workspaces) | d | t_T (us) | B | T* | N_Toff per run | "
          "eps_CCZ needed | phys qubits (lower bound if eps_CCZ < 1e-12) |")
    print("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for des, lab, PP in DES[2:]:
        for L in (60, 150):
            for S, R in ((1, 100), (1e3, 100)):
                G = G_lhpst(des, L, PP)[0]
                nL = qubits_lhpst(des, L, PP) + (R - 1) * pair_workspace(des, L, PP)
                k = kappa_min(des, L)
                tT = T_TOFF
                for _ in range(3):
                    B, Ts, _, Nt = breakeven(G, L, S=S, R=R, kappa=k, tT=tT)
                    d = d_required(nL, Ts)
                    tT = max(T_TOFF, 5.5 * d * 1e-6)
                B, Ts, _, Nt = breakeven(G, L, S=S, R=R, kappa=k, tT=tT)
                eps = 0.1 / Nt
                flag = "" if eps >= EPS_CCZ else (" (+20% factory)" if eps >= EPS_CCZ_BIG else " LB")
                print(f"| {des} | {lab} | {L} | {fmt(S)} | {R} | {fmt(nL)} | {d} | {tT * 1e6:.0f} | {fmt(B)} | "
                      f"{human_t(Ts)} | {fmt(Nt)} | {fmt(eps)} | {fmt(phys_qubits(nL, d=d, factories=R))}{flag} |")

    print("\n## Sensitivity of G_LHPST(D2 central, L=150)\n")
    base = G_lhpst("D2", 150, CENTRAL)[0]
    print(f"- base: {fmt(base)} (b_w = {resolve(CENTRAL, 150)['bw']})")
    for k, v in (("bw", 16), ("bw", 20), ("bw", 22), ("bw", 24), ("bw", 28), ("gs", 512), ("gs", 2048), ("u", 1.5),
                 ("sq", 0.5), ("b", 8), ("b", 12), ("ecarry", True), ("bacc", 32), ("bacc", 48), ("guard", 0),
                 ("guard", 8), ("store_frames", False), ("mulconv", "hrs")):
        Q = dict(CENTRAL, **{k: v})
        g = G_lhpst("D2", 150, Q)[0]
        print(f"- {k}={v}: {fmt(g)} ({g / base:.2f}x)")
    Q = resolve(CENTRAL, 150)
    g_pp = base + 2 * 2 * 2 * (build_torsion_parallel_prefix(150, Q) - build_torsion(150, Q))
    print(f"- parallel-prefix build instead of sequential: {fmt(g_pp)} ({g_pp / base:.2f}x)")
    print("- generous vs v1-generous(b_w=16): " + ", ".join(
        f"L={L}: {G_lhpst('D2', L, GENEROUS)[0] / G_lhpst('D2', L, dict(GENEROUS, bw=16))[0]:.2f}x" for L in LS))
    print("- central vs b_w=20 central: " + ", ".join(
        f"L={L}: {G_lhpst('D2', L, CENTRAL)[0] / G_lhpst('D2', L, dict(CENTRAL, bw=20, guard=0))[0]:.2f}x" for L in LS))

    print("\n## Quantised-HMC variant (D2 energy), kappa = 1/n_leap relative to per-gradient accounting\n")
    for L in LS:
        Q = resolve(CENTRAL, L)
        CE = C_E_torsion("D2", L, Q)
        n_leap, c_grad = 8, 3
        G_h = 2 * n_leap * c_grad * CE
        B, Ts, _, _ = breakeven(G_h, L, kappa=1 / n_leap)
        B2 = breakeven(G_lhpst("D2", L, CENTRAL)[0], L, kappa=3.0)[0]
        print(f"- L={L}: G ~ {fmt(G_h)}; B(S=1,R=1) = {fmt(B)} ({human_t(Ts)}); D2 at kappa=3: {fmt(B2)}")

    print("\n## Representation variants: Toffolis per pair term (central) and G ratios\n")
    for des in ("D1", "D2", "D2sb", "D2svd", "D3", "D3sb"):
        print(f"- {des}: " + ", ".join(f"L={L}: {pair_term(des, L, resolve(CENTRAL, L))[0]:.0f}" for L in LS))
    for des, base_d in (("D2sb", "D2"), ("D3sb", "D3")):
        row = []
        for L in LS:
            Q = resolve(CENTRAL, L)
            G0 = G_lhpst(base_d, L, CENTRAL)[0]
            n_terms = (2 * 2 * n_pairs(L)) if base_d == "D2" else (2 * 4 * (L - 5))
            dG = 2 * n_terms * (pair_term(des, L, Q)[0] - pair_term(base_d, L, Q)[0])
            row.append(f"L={L}: {fmt(G0 + dG)} ({(G0 + dG) / G0:.2f}x; per term "
                       f"{pair_term(des, L, Q)[0] / pair_term(base_d, L, Q)[0]:.2f}x)")
        print(f"- {des}: " + ", ".join(row))
    Q = resolve(CENTRAL, 150)
    ud = 2 * (sqdist(Q, 150) + sqrt_(Q["bw"], 2, Q) + horner(Q)) + qroam(128, 4 * Q["bc"])[0] + Q["bacc"]
    print(f"- uniform-d (g=128) per term at L=150: {ud:.0f} vs D2 {pair_term('D2', 150, Q)[0]:.0f} "
          f"({ud / pair_term('D2', 150, Q)[0]:.1f}x); D1/D2 per term {pair_term('D1', 150, Q)[0] / pair_term('D2', 150, Q)[0]:.2f}x;"
          f" Newton share of D1 arithmetic {sqrt_(Q['bw'], 2, Q) / (sqdist(Q, 150) + sqrt_(Q['bw'], 2, Q) + 4 * Q['bw'] + MUL(Q['bw'], Q)):.2f}")

    print("\n## g(L) = G_LHPST / L^2 (for T2 assumption A-G; Metropolis walks only)\n")
    for label, PP in (("CENTRAL", CENTRAL), ("GENEROUS", GENEROUS)):
        for des in ("D1", "D2", "D3"):
            print(f"- {label} {des}: " + ", ".join(f"L={L}: {G_lhpst(des, L, PP)[0] / L**2:.2g}" for L in LS))

    print("\n## Conditional per-step floor for the move-oblivious torsion class (H-008 per-step clause)\n")
    for L in (100,):
        for bw in (16, 20, 22, 24):
            fl = 2 * 2 * n_pairs(L) * 3 * (bw * bw / 2)
            print(f"- L={L}, b_w={bw}: 2 (oracle applications) x 2 n_p (CA, CB) x 3 squarings x b_w^2/2 = {fmt(fl)}")
        for bw in (20, 24):
            fl = 2 * 2 * 4 * (L - 5) * 3 * (bw * bw / 2)
            print(f"- D3 analogue L={L}, b_w={bw}: 2 x 2 (old/new) x 4(L-5) x 3 x b_w^2/2 = {fmt(fl)}")

    print("\n## kappa growing with N_C: B for kappa = kappa0 * N_C^alpha (D2 central / D3 generous, L=100, S=1e3, R=100)\n")
    for des, lab, PP in (("D2", "central", CENTRAL), ("D3", "generous", GENEROUS)):
        G = G_lhpst(des, 100, PP)[0]
        X = 1e3 * G * T_TOFF / (100 * t_C_placeholder(100))
        for alpha in (0.0, 0.25, 0.5, 0.75):
            k0 = kappa_min(des, 100)
            B = (math.sqrt(k0) * X) ** (2 / (1 - alpha))
            print(f"- {des} {lab} alpha={alpha}: B = {fmt(B)}")
        print(f"- {des} {lab} alpha -> 1: no break-even")

    print("\n## Calibration\n")
    print(f"- Sanders Table VIII SK N=512 LHPST: 2.6e3 Toffolis/step; Table IX LABS N=512 LHPST: 1.2e6")
    for L in (100, 150):
        print(f"- D2 L={L}: {fmt(G_lhpst('D2', L, CENTRAL)[0])} = {G_lhpst('D2', L, CENTRAL)[0] / 1.2e6:.0f}x LABS-512")


if __name__ == "__main__":
    main()
