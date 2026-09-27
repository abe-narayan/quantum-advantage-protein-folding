"""Small numerical checks for research/theory/PROOFS/T1_reduction_theorem.md.

Every check is a falsifier for a DERIVED statement in that note (section numbers
in brackets), or the arithmetic behind a practical number in its section 4.
Nothing here is an experiment. Runtime is about a minute on one core.

    python research/theory/PROOFS/T1_reduction_checks.py

Checks
  C1  prefix theorem (Cor. 1): LP tail == greedy E-order prefix; KKT prefix for non-linear V
  C2  solver equivalence (Cor. 2): min_p CVaR_alpha(p) == min_x E(x); optimal set {p(X_min) >= alpha};
      finite-shot argmin readout (Thm 2(a)): P(best of S draws in X_min) >= 1 - (1 - alpha)^S
  C3  hinged-Gibbs closed form (Cor. 3): bisection and exact O(N log N) p* vs generic convex solvers;
      strong duality; kink cells (P(E<s*) <= alpha <= P(E<=s*), with strict inequality allowed);
      alpha = 1 plateau of the dual; flat weight on E = +inf states; a product family never beats p*
  C4  dephasing lemma (Lemma 1): tr(H rho) - T S(rho) >= <E>_p - T H(p), p = diag(rho)
  C5  hull projection (Cor. 4): variance identity, x* = P_aff(t), gain 1/0, error decomposition;
      simplex case: finite differences of the constrained solver itself (not of the affine solve)
  C6  information bound (Thm 2(b)) and the FT break-even arithmetic for argmin readouts (N2), per L,
      from the census t_C(L), with G_eval fixed or scaled by pair count, S in {1, 8, 1e3}, R in {1, 10, 100}
  C7  read-only summary of the G1 mode census (N2, N3): cluster and energy-level hit rates, Clopper-Pearson
      bounds, Good-Turing unseen mass bounded from n_modes (the JSONs store only the 50 lowest modes'
      sizes), top-2 mode gaps, per-evaluation cost; the R64 test file vs the R256 census file; the
      clip-floor sensitivity of the Laplace log-ratio. PILOT, indicative only
  C8  timing of the explicit-register classical reproduction (eigh / eigvalsh at D = 128, 512)
"""
from __future__ import annotations

import glob
import json
import math
import os
import time

import numpy as np
from scipy.optimize import linprog, minimize, nnls
from scipy.special import logsumexp
from scipy.stats import beta as beta_dist

RNG = np.random.default_rng(20260926)
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT: dict = {}


# ---------------------------------------------------------------- helpers
def tail_greedy(E, p, alpha):
    """Greedy fractional-knapsack fill of the alpha-tail in E order (stable ties). This is lambda*(p) of D5(b)."""
    order = np.argsort(E, kind="stable")
    lam = np.zeros_like(p)
    rem = alpha
    for i in order:
        if rem <= 0:
            break
        take = min(p[i], rem)
        lam[i] = take
        rem -= take
    return lam


def tail_lp(E, p, alpha):
    N = len(E)
    r = linprog(E, A_eq=np.ones((1, N)), b_eq=[alpha],
                bounds=[(0.0, float(pi)) for pi in p], method="highs")
    return r.x, r.fun


def cvar(E, p, alpha):
    lam = tail_greedy(E, p, alpha)
    m = lam > 0
    return float(E[m] @ lam[m]) / alpha


def shannon(p):
    q = p[p > 0]
    return float(-(q * np.log(q)).sum())


def F_free(E, p, alpha, T):
    return cvar(E, p, alpha) - T * shannon(p)


def hinged(E, s, alpha, T):
    """p_i(s) ∝ exp((s - E_i)_+ / (alpha T)); states with E = +inf get the flat weight exp(0) = 1."""
    a = np.maximum(s - E, 0.0) / (alpha * T)
    a -= a.max()
    w = np.exp(a)
    return w / w.sum()


def pstar(E, alpha, T):
    """Closed-form minimiser of CVaR_alpha(E;p) - T H(p) by bisection on s -> P_{p(s)}(E < s).
    alpha = 1: every s >= max E maximises the dual (g = -T log Z_T there), so return s* = max E."""
    if alpha >= 1.0:
        w = np.exp(-(E - E.min()) / T)
        return w / w.sum(), float(E.max())
    lo, hi = float(E.min()), float(E.min()) + 1.0
    while hinged(E, hi, alpha, T)[E < hi].sum() < alpha:
        hi = E.min() + 2.0 * (hi - E.min())
    for _ in range(200):  # bisection on the monotone map s -> P_{p(s)}(E < s)
        mid = 0.5 * (lo + hi)
        if hinged(E, mid, alpha, T)[E < mid].sum() < alpha:
            lo = mid
        else:
            hi = mid
    s = 0.5 * (lo + hi)
    return hinged(E, s, alpha, T), s


def pstar_exact(E, alpha, T):
    """Exact O(N log N) dual maximiser (Theorem 3 table): sort the finite energies; in each open gap
    (e_j, e_{j+1}) between consecutive levels solve P_{p(s)}(E < s) = alpha in closed form,
        s = alpha T [ ln(alpha (N - k)) - ln(1 - alpha) - log sum_{i<=k} exp(-E_i/(alpha T)) ],
    where k = #{E <= e_j}; if no gap contains its solution, s* is the kink level e_j with
    P(E < e_j) <= alpha <= P(E <= e_j). States with E = +inf count only through N - k (flat weight 1)."""
    N = len(E)
    if alpha >= 1.0:
        return pstar(E, alpha, T)[0], float(E[np.isfinite(E)].max()), "alpha=1"
    fin = np.sort(E[np.isfinite(E)])
    lev, cnt = np.unique(fin, return_counts=True)
    c = np.cumsum(cnt)                                        # c[j] = #{E <= lev[j]}
    lcum = np.logaddexp.accumulate(-fin / (alpha * T))        # log sum_{i<=k} exp(-E_i/(alpha T))
    for j in range(len(lev)):
        k = int(c[j])
        if k < N:                                             # the open gap (lev[j], lev[j+1]) or (lev[-1], inf)
            s = alpha * T * (math.log(alpha * (N - k)) - math.log(1 - alpha) - lcum[k - 1])
            upper = lev[j + 1] if j + 1 < len(lev) else math.inf
            if lev[j] < s < upper:
                return hinged(E, s, alpha, T), float(s), "gap"
        # kink test at the next level
        if j + 1 < len(lev):
            s = float(lev[j + 1])
            p = hinged(E, s, alpha, T)
            if p[E < s].sum() <= alpha + 1e-12 and p[E <= s].sum() >= alpha - 1e-12:
                return p, s, "kink"
    s = float(lev[0])                                         # alpha at or below the lowest level's share
    return hinged(E, s, alpha, T), s, "kink"


def dual_g(E, s, alpha, T):
    a = np.maximum(s - E, 0.0) / (alpha * T)
    m = a.max()
    return s - T * (m + math.log(np.exp(a - m).sum()))


# ---------------------------------------------------------------- C1 prefix theorem
def check_prefix():
    worst_x, worst_obj, worst_tie_obj, n = 0.0, 0.0, 0.0, 0
    for N in (8, 64, 512):
        for alpha in (0.05, 0.18, 0.5, 1.0):
            for _ in range(20):
                E = RNG.normal(size=N)
                p = RNG.dirichlet(np.ones(N))
                lam_g = tail_greedy(E, p, alpha)
                lam_l, f_l = tail_lp(E, p, alpha)
                worst_x = max(worst_x, float(np.abs(lam_g - lam_l).max()))
                worst_obj = max(worst_obj, abs(float(E @ lam_g) - f_l))
                Et = np.round(E, 1)  # heavy ties: only the objective is unique
                lam_gt = tail_greedy(Et, p, alpha)
                _, f_lt = tail_lp(Et, p, alpha)
                worst_tie_obj = max(worst_tie_obj, abs(float(Et @ lam_gt) - f_lt))
                n += 1
    # general smooth V (S30 T1): every KKT point is a prefix of the order of grad V(lambda*)
    viol_max = 0.0
    for _ in range(30):
        N, alpha = 12, 0.3
        E = RNG.normal(size=N)
        A = RNG.normal(size=(N, N))
        Q = 0.5 * A @ A.T / N
        p = RNG.dirichlet(np.ones(N))
        V = lambda l: float(E @ l + 0.5 * l @ Q @ l)
        gV = lambda l: E + Q @ l
        cons = [{"type": "eq", "fun": lambda l: l.sum() - alpha, "jac": lambda l: np.ones(N)}]
        l0 = p * alpha
        r = minimize(V, l0, jac=gV, bounds=[(0, pi) for pi in p], constraints=cons,
                     method="SLSQP", options={"ftol": 1e-14, "maxiter": 2000})
        lam = r.x
        g = gV(lam)
        tol = 1e-7
        inside = lam > tol                  # carries tail mass
        not_full = lam < p - tol            # could take more
        if inside.any() and not_full.any():
            viol = float(g[inside].max() - g[not_full].min())  # must be <= 0 up to ties
            viol_max = max(viol_max, viol)
    OUT["C1"] = dict(cases=n, max_abs_lambda_diff=worst_x, max_obj_diff=worst_obj,
                     max_obj_diff_with_ties=worst_tie_obj, kkt_prefix_violation_max=viol_max)


# ---------------------------------------------------------------- C2 solver equivalence
def check_solver_equivalence():
    worst, n = 0.0, 0
    for N in (8, 64, 256):
        for alpha in (0.05, 0.25, 1.0):
            E = RNG.normal(size=N)
            # variables z = [p (N), lam (N)]
            c = np.concatenate([np.zeros(N), E / alpha])
            A_eq = np.zeros((2, 2 * N))
            A_eq[0, :N] = 1
            A_eq[1, N:] = 1
            A_ub = np.hstack([-np.eye(N), np.eye(N)])  # lam - p <= 0
            r = linprog(c, A_ub=A_ub, b_ub=np.zeros(N), A_eq=A_eq, b_eq=[1.0, alpha],
                        bounds=[(0, None)] * (2 * N), method="highs")
            worst = max(worst, abs(r.fun - E.min()))
            n += 1
    # optimal-set characterisation: CVaR(p) == E_min  iff  p(X_min) >= alpha
    mis = 0
    for _ in range(2000):
        N = 16
        E = RNG.normal(size=N)
        i0 = int(np.argmin(E))
        alpha = float(RNG.uniform(0.05, 1.0))
        p = RNG.dirichlet(np.ones(N) * 0.3)
        at_min = abs(cvar(E, p, alpha) - E.min()) < 1e-12
        if at_min != (p[i0] >= alpha - 1e-15):
            mis += 1
    # finite shots (Thm 2(a)): an optimum with p(X_min) = alpha exactly; best-of-S draw misses X_min w.p. (1-alpha)^S
    fs = []
    for alpha, S in ((0.05, 50), (0.2, 16), (0.5, 4)):
        N = 32
        p = np.full(N, (1 - alpha) / (N - 1))
        p[0] = alpha                         # X_min = {0}
        draws = RNG.choice(N, size=(200000, S), p=p)
        miss = float(np.mean((draws != 0).all(1)))
        fs.append(dict(alpha=alpha, S=S, miss_mc=miss, miss_formula=(1 - alpha) ** S))
    OUT["C2"] = dict(cases=n, max_abs_minCVaR_minus_Emin=worst, optimal_set_mismatches=mis, trials=2000,
                     finite_shot_argmin=fs)


# ---------------------------------------------------------------- C3 hinged Gibbs
def generic_min(E, alpha, T):
    """Best of two independent primal solvers for min_p CVaR_alpha(E;p) - T H(p)."""
    N = len(E)
    def obj(z):
        q, l = z[:N], z[N:]
        qq = np.clip(q, 1e-300, None)
        return float(E @ l) / alpha + T * float((qq * np.log(qq)).sum())
    def jac(z):
        q = np.clip(z[:N], 1e-300, None)
        return np.concatenate([T * (np.log(q) + 1.0), E / alpha])
    cons = [{"type": "eq", "fun": lambda z: z[:N].sum() - 1.0},
            {"type": "eq", "fun": lambda z: z[N:].sum() - alpha},
            {"type": "ineq", "fun": lambda z: z[:N] - z[N:]}]
    z0 = np.concatenate([np.ones(N) / N, np.ones(N) * alpha / N])
    r = minimize(obj, z0, jac=jac, constraints=cons,
                 bounds=[(1e-15, 1)] * N + [(0, 1)] * N,
                 method="SLSQP", options={"ftol": 1e-15, "maxiter": 5000})
    p_slsqp = np.clip(r.x[:N], 0, None)
    p_slsqp /= p_slsqp.sum()
    # independent solver 2: composite entropic mirror descent on the primal,
    # p <- (p * exp(-eta g))^(1/(1+eta T)), g = Danskin subgradient of CVaR at p
    q = np.ones(N) / N
    order = np.argsort(E, kind="stable")
    for k in range(1, 20001):
        cum = np.cumsum(q[order])
        s_var = E[order][min(int(np.searchsorted(cum, alpha - 1e-15)), N - 1)]
        g = -np.maximum(s_var - E, 0.0) / alpha
        eta = 1.0 / (T * k)
        lq = (np.log(np.clip(q, 1e-300, None)) - eta * g) / (1.0 + eta * T)
        lq -= lq.max()
        q = np.exp(lq)
        q /= q.sum()
    cands = [p_slsqp, q]
    Fs = [F_free(E, c, alpha, T) for c in cands]
    return cands[int(np.argmin(Fs))], min(Fs)


def check_hinged_gibbs():
    rows = []
    for N in (16, 64):
        for alpha in (0.1, 0.25, 1.0):
            for T in (0.05, 0.1, 0.5):
                E = RNG.normal(size=N)
                p, s = pstar(E, alpha, T)
                pe, se, _ = pstar_exact(E, alpha, T)
                F_star = F_free(E, p, alpha, T)
                gap = F_star - dual_g(E, s, alpha, T)
                p_num, F_num = generic_min(E, alpha, T)
                rows.append(dict(N=N, alpha=alpha, T=T, duality_gap=gap,
                                 F_num_minus_F_star=F_num - F_star,
                                 tv=0.5 * float(np.abs(p_num - p).sum()),
                                 tv_exact_vs_bisect=0.5 * float(np.abs(pe - p).sum()),
                                 below=float(p[E < s].sum()), upto=float(p[E <= s].sum())))
    # kink cells: s* on an energy level, where P(E<s*) < alpha strictly (a positive-length set of alpha)
    E3 = np.array([0.0, 1.0, 2.0])
    pk, sk, kind = pstar_exact(E3, 0.8, 1.0)
    pb, sb = pstar(E3, 0.8, 1.0)
    F_k = F_free(E3, pk, 0.8, 1.0)
    best_nm = min(minimize(lambda z: F_free(E3, np.exp(z) / np.exp(z).sum(), 0.8, 1.0), RNG.normal(size=3),
                           method="Nelder-Mead", options={"xatol": 1e-12, "fatol": 1e-15, "maxiter": 20000}).fun
                  for _ in range(10))
    kink_example = dict(E=E3.tolist(), alpha=0.8, T=1.0, s_star=sk, kind=kind, s_bisect=sb, p_star=pk.round(6).tolist(),
                        P_below=float(pk[E3 < sk].sum()), P_upto=float(pk[E3 <= sk].sum()), F_star=F_k,
                        F_nelder_mead=best_nm, tv_bisect_vs_exact=0.5 * float(np.abs(pk - pb).sum()))
    # random integer-level cells: many kinks; the sandwich must hold, equality need not
    sandwich_viol, strict_kinks, n_int, worst_F, worst_tv = 0.0, 0, 0, -math.inf, 0.0
    for _ in range(60):
        N = 8
        E = RNG.integers(0, 4, size=N).astype(float)
        alpha = float(RNG.uniform(0.05, 0.95))
        T = float(RNG.choice([0.2, 0.5, 1.0]))
        pe, se, kind = pstar_exact(E, alpha, T)
        pb, sb = pstar(E, alpha, T)
        below, upto = float(pe[E < se].sum()), float(pe[E <= se].sum())
        sandwich_viol = max(sandwich_viol, below - alpha, alpha - upto)
        strict_kinks += int(below < alpha - 1e-9)
        _, F_num = generic_min(E, alpha, T)
        worst_F = max(worst_F, F_free(E, pe, alpha, T) - F_num)   # must be <= ~0: closed form is optimal
        worst_tv = max(worst_tv, 0.5 * float(np.abs(pe - pb).sum()))
        n_int += 1
    # alpha = 1 plateau: g(s) = -T log Z_T for every s >= max E
    E = RNG.normal(size=20)
    T = 0.7
    logZ = logsumexp(-E / T)
    plateau = max(abs(dual_g(E, s, 1.0, T) + T * logZ) for s in (E.max(), E.max() + 0.5, E.max() + 5, E.max() + 50))
    below_max = dual_g(E, E.max() - 0.3, 1.0, T) + T * logZ         # strictly below the plateau
    # flat weight on invalid encodings (E = +inf): p*_{alpha,T} gives them the same weight as any valid state above s*
    Einf = np.array([0.0, 1.0, 3.0, np.inf, np.inf, np.inf])
    pinf, sinf, _ = pstar_exact(Einf, 0.5, 0.5)
    inf_example = dict(E=["0", "1", "3", "inf", "inf", "inf"], alpha=0.5, T=0.5, s_star=sinf,
                       p_star=pinf.round(4).tolist(), mass_on_invalid=float(pinf[~np.isfinite(Einf)].sum()))
    # restricted family: product (mean-field) distributions over n bits never beat p*
    prod_gaps = []
    n = 6
    X = np.array([[(k >> b) & 1 for b in range(n)] for k in range(2 ** n)], dtype=float)
    for _ in range(6):
        h = RNG.normal(size=n)
        J = np.triu(RNG.normal(size=(n, n)), 1)
        E = X @ h + np.einsum("ki,ij,kj->k", X, J, X)
        alpha, T = 0.25, 0.1
        p, _ = pstar(E, alpha, T)
        F_star = F_free(E, p, alpha, T)
        def Fprod(th):
            b = 1.0 / (1.0 + np.exp(-th))
            q = np.prod(np.where(X > 0, b, 1 - b), axis=1)
            return F_free(E, q, alpha, T)
        best = min(minimize(Fprod, RNG.normal(size=n) * 2, method="Powell",
                            options={"xtol": 1e-10, "ftol": 1e-12, "maxfev": 20000}).fun
                   for _ in range(8))
        prod_gaps.append(best - F_star)
    frac = [r for r in rows if r["alpha"] < 1]
    OUT["C3"] = dict(
        cells=len(rows),
        max_abs_duality_gap=max(abs(r["duality_gap"]) for r in rows),
        min_F_num_minus_F_star=min(r["F_num_minus_F_star"] for r in rows),
        max_F_num_minus_F_star=max(r["F_num_minus_F_star"] for r in rows),
        max_tv_num_vs_closed=max(r["tv"] for r in rows),
        max_tv_exact_vs_bisection=max(r["tv_exact_vs_bisect"] for r in rows),
        sandwich_max_violation_random_cells=max(max(r["below"] - r["alpha"], r["alpha"] - r["upto"]) for r in frac),
        kink_example=kink_example,
        integer_level_cells=dict(cells=n_int, strict_kinks=strict_kinks, sandwich_max_violation=sandwich_viol,
                                 max_F_closed_minus_F_numeric=worst_F, max_tv_exact_vs_bisection=worst_tv),
        alpha1_plateau_max_dev=plateau, alpha1_g_below_max_minus_plateau=below_max,
        invalid_encoding_example=inf_example,
        product_family_F_gap_min=min(prod_gaps), product_family_F_gap_max=max(prod_gaps))


# ---------------------------------------------------------------- C4 dephasing lemma
def check_dephasing():
    d, T = 16, 0.3
    E = RNG.normal(size=d)
    worst = math.inf
    for _ in range(5000):
        k = int(RNG.integers(1, d + 1))
        G = RNG.normal(size=(d, k)) + 1j * RNG.normal(size=(d, k))
        rho = G @ G.conj().T
        rho /= np.trace(rho).real
        ev = np.clip(np.linalg.eigvalsh(rho), 0, None)
        S_vn = float(-(ev[ev > 0] * np.log(ev[ev > 0])).sum())
        p = np.clip(np.diag(rho).real, 0, None)
        Fq = float(E @ p) - T * S_vn
        Fc = float(E @ p) - T * shannon(p)
        worst = min(worst, Fq - Fc)
    Fmin = E.min() - T * math.log(np.exp(-(E - E.min()) / T).sum())
    OUT["C4"] = dict(samples=5000, min_Fq_minus_Fcl=worst, gibbs_min=Fmin)


# ---------------------------------------------------------------- C5 hull projection
def check_hull():
    d, K = 30, 7
    res = dict(identity_max_rel=0.0, proj_max=0.0, gain_eigs=None, decomp_max=0.0,
               simplex_cases=0, simplex_skipped_degenerate=0, simplex_gain_ones=[], simplex_support=[],
               simplex_max_dev_from_face_projector=0.0)
    MPEN = 1e4

    def simplex_solve(tt):
        """Constrained solver itself: min ||U^T w - t||^2, w >= 0, sum w = 1 (equality by a stiff penalty;
        Lawson-Hanson NNLS is an exact active-set method, so finite differences see the constrained map)."""
        A = np.vstack([U.T, MPEN * np.ones((1, K))])
        b = np.concatenate([tt, [MPEN]])
        w, _ = nnls(A, b, maxiter=10000)
        return w

    for _ in range(20):
        U = RNG.normal(size=(K, d))
        t = RNG.normal(size=d)
        a = ((U - t) ** 2).sum(1)
        B = ((U[:, None, :] - U[None, :, :]) ** 2).sum(-1)
        for _ in range(20):
            w = RNG.normal(size=K)
            w /= w.sum()
            lhs = float(((U.T @ w - t) ** 2).sum())
            rhs = float(w @ a - 0.5 * w @ B @ w)
            res["identity_max_rel"] = max(res["identity_max_rel"], abs(lhs - rhs) / max(1.0, abs(lhs)))
        # affine-constrained least squares via KKT
        def affine_solve(tt, idx=None):
            Us = U if idx is None else U[idx]
            k = Us.shape[0]
            M = np.zeros((k + 1, k + 1))
            M[:k, :k] = 2 * Us @ Us.T
            M[:k, k] = 1
            M[k, :k] = 1
            rhs = np.concatenate([2 * Us @ tt, [1.0]])
            w = np.linalg.solve(M, rhs)[:k]
            return Us.T @ w
        x = affine_solve(t)
        D = (U[1:] - U[0]).T
        Pi = D @ np.linalg.pinv(D)
        x_proj = U[0] + Pi @ (t - U[0])
        res["proj_max"] = max(res["proj_max"], float(np.abs(x - x_proj).max()))
        h = 1e-6
        Jac = np.column_stack([(affine_solve(t + h * e) - affine_solve(t - h * e)) / (2 * h)
                               for e in np.eye(d)])
        eigs = np.sort(np.linalg.eigvalsh(0.5 * (Jac + Jac.T)))[::-1]
        res["gain_eigs"] = [round(float(eigs[0]), 9), round(float(eigs[K - 2]), 9),
                            round(float(eigs[K - 1]), 9), round(float(eigs[-1]), 9)]
        xn = RNG.normal(size=d)
        lhs = float(((x - xn) ** 2).sum())
        r_perp = (np.eye(d) - Pi) @ (xn - U[0])
        rhs = float(((Pi @ (t - xn)) ** 2).sum() + (r_perp ** 2).sum())
        res["decomp_max"] = max(res["decomp_max"], abs(lhs - rhs))
        # simplex weights (w >= 0): differentiate the constrained solver, then compare with the face projector
        tt = U.mean(0) + 2.0 * RNG.normal(size=d)
        w0 = simplex_solve(tt)
        S = np.where(w0 > 1e-9)[0]
        h2 = 1e-6
        supports_same = True
        cols = []
        for e in np.eye(d):
            wp, wm = simplex_solve(tt + h2 * e), simplex_solve(tt - h2 * e)
            supports_same &= (np.array_equal(np.where(wp > 1e-9)[0], S) and np.array_equal(np.where(wm > 1e-9)[0], S))
            cols.append((U.T @ wp - U.T @ wm) / (2 * h2))
        Jf = np.column_stack(cols)
        DS = (U[S[1:]] - U[S[0]]).T if len(S) > 1 else np.zeros((d, 0))
        affinely_independent = (np.linalg.matrix_rank(DS) == len(S) - 1) if len(S) > 1 else True
        # strict complementarity proxy: support weights bounded away from 0 and the active set locally constant
        if not (supports_same and affinely_independent and w0[S].min() > 1e-6):
            res["simplex_skipped_degenerate"] += 1
            continue
        PiS = DS @ np.linalg.pinv(DS) if len(S) > 1 else np.zeros((d, d))
        ev = np.linalg.eigvalsh(0.5 * (Jf + Jf.T))
        res["simplex_cases"] += 1
        res["simplex_gain_ones"].append(int((ev > 0.5).sum()))
        res["simplex_support"].append(int(len(S)))
        res["simplex_max_dev_from_face_projector"] = max(res["simplex_max_dev_from_face_projector"],
                                                         float(np.abs(Jf - PiS).max()))
    res["simplex_gain_ones_equals_support_minus_1"] = all(
        g == s - 1 for g, s in zip(res["simplex_gain_ones"], res["simplex_support"]))
    OUT["C5"] = res


# ---------------------------------------------------------------- C7 pilot census (read-only)
def census_rows():
    files = sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "g1_modes", "*_R*_s0.json")))
    byL: dict = {}
    for f in files:
        try:
            d = json.load(open(f))
        except Exception:
            continue
        s = d["mode_sizes"]              # only the 50 lowest-E modes are stored (scripts/g1_mode_census.py)
        R, k = d["restarts"], d["n_modes"]
        f1_top = sum(1 for x in s if x == 1)
        rest_modes, rest_restarts = k - len(s), R - sum(s)
        # bounds on the singleton count f1 from n_modes: the unstored modes hold rest_restarts restarts in
        # rest_modes modes, each of size >= 1
        f1_lb = f1_top + max(0, 2 * rest_modes - rest_restarts)
        f1_ub = f1_top + (rest_modes - 1 if (rest_modes > 0 and rest_restarts > rest_modes) else rest_modes)
        hits = s[0]
        cp_lo = float(beta_dist.ppf(0.025, hits, R - hits + 1)) if hits > 0 else 0.0
        fw = d.get("frac_within_dE", {})
        lap = d.get("laplace", [])
        byL.setdefault(d["L"], []).append(dict(
            crop=d["crop"], R=R, hits=hits, q=hits / R, cp95_upper_inv_q=(1.0 / cp_lo if cp_lo > 0 else math.inf),
            modes=k, gt_unseen_top50_only=f1_top / R, gt_unseen_lb=f1_lb / R, gt_unseen_ub=f1_ub / R,
            q_E1=fw.get("1.0"), q_E5=fw.get("5.0"), q_E20=fw.get("20.0"),
            t_restart=d["secs"] / R, t_eval=d["secs"] / d["grad_evals"], evals_per_restart=d["grad_evals"] / R,
            top2_gap=(d["mode_E"][1] - d["mode_E"][0]) if len(d["mode_E"]) > 1 else None,
            nonpos_min=min((l.get("n_nonpos", 0) for l in lap), default=None)))
    return files, byL


def census_summary(files, byL):
    summ = {}
    for L, rs in sorted(byL.items()):
        med = lambda key: float(np.median([r[key] for r in rs if r[key] is not None]))
        R = rs[0]["R"]
        summ[str(L)] = dict(
            chains=len(rs), R=R,
            q_cluster_median=med("q"), q_cluster_min=min(r["q"] for r in rs), q_cluster_max=max(r["q"] for r in rs),
            best_cluster_hit_once=int(sum(r["hits"] == 1 for r in rs)),
            cp95_upper_inv_q_per_chain=sorted(round(r["cp95_upper_inv_q"]) for r in rs),
            q_E1_median=med("q_E1"), q_E20_median=med("q_E20"),
            chains_q_E1_at_resolution=int(sum(abs(r["q_E1"] - 1 / R) < 1e-12 for r in rs)),
            chains_q_E20_at_resolution=int(sum(abs(r["q_E20"] - 1 / R) < 1e-12 for r in rs)),
            modes_median=med("modes"),
            gt_unseen_top50_only_median=med("gt_unseen_top50_only"),
            gt_unseen_lb_median=med("gt_unseen_lb"), gt_unseen_ub_median=med("gt_unseen_ub"),
            gt_unseen_lb_per_chain=sorted(round(r["gt_unseen_lb"], 2) for r in rs),
            chains_gt_unseen_ge_half=int(sum(r["gt_unseen_lb"] >= 0.5 for r in rs)),
            t_restart_median_s=med("t_restart"), t_eval_median_ms=1e3 * med("t_eval"),
            evals_per_restart_median=med("evals_per_restart"),
            top2_gap_per_chain=sorted(round(r["top2_gap"], 2) for r in rs if r["top2_gap"] is not None),
            min_nonpos_hessian_eigs=min(r["nonpos_min"] for r in rs if r["nonpos_min"] is not None))
    gaps = np.array([r["top2_gap"] for rs in byL.values() for r in rs if r["top2_gap"] is not None])
    gap_dist = dict(cells=int(len(gaps)), below_1=int((gaps < 1).sum()), below_2_2=int((gaps < 2.2).sum()),
                    below_5=int((gaps < 5).sum()), below_10=int((gaps < 10).sum()),
                    quantiles_10_25_50_75_90=[round(float(x), 2) for x in np.percentile(gaps, [10, 25, 50, 75, 90])])
    # the R64 test file vs the R256 census file for the same crop and settings
    t = os.path.join(ROOT, "research", "results", "RAW", "g1_modes_test", "5O37A_45_R64_s0.json")
    c = os.path.join(ROOT, "research", "results", "RAW", "g1_modes", "5O37A_45_R256_s0.json")
    recon, lap_sens = None, []
    if os.path.exists(t) and os.path.exists(c):
        dt, dc = json.load(open(t)), json.load(open(c))
        recon = dict(
            test=dict(R=dt["restarts"], E_best=dt["E_best"], top_sizes=dt["mode_sizes"][:3],
                      top_E=[round(x, 2) for x in dt["mode_E"][:3]],
                      rmsd_native_top2=[round(l["rmsd_native"], 2) for l in dt["laplace"][:2]],
                      t_restart=dt["secs"] / dt["restarts"], keys_only_in_test=sorted(set(dt["laplace"][0]) - set(dc["laplace"][0]))),
            census=dict(R=dc["restarts"], E_best=dc["E_best"], top_sizes=dc["mode_sizes"][:3],
                        top_E=[round(x, 2) for x in dc["mode_E"][:3]],
                        rmsd_native_top2=[round(l["rmsd_native"], 2) for l in dc["laplace"][:2]],
                        frac_within_dE=dc.get("frac_within_dE"), t_restart=dc["secs"] / dc["restarts"],
                        keys_only_in_census=sorted(set(dc) - set(dt))),
            census_modes_within_40_nats_of_test_best=[(round(e, 2), int(k)) for e, k in zip(dc["mode_E"], dc["mode_sizes"])
                                                     if abs(e - dt["E_best"]) < 40])
        for dd, name in ((dt, "R64_test"), (dc, "R256_census")):
            l0, l1 = dd["laplace"][0], dd["laplace"][1]
            lf = math.log(1e-6)                  # the clip floor in scripts/g1_mode_census.py::hessian_logdet
            P0, P1 = l0["logdetH"] - l0["n_nonpos"] * lf, l1["logdetH"] - l1["n_nonpos"] * lf
            base = -(l1["E"] - l0["E"]) - 0.5 * (P1 - P0)       # at T = 1
            coef = -0.5 * (l1["n_nonpos"] - l0["n_nonpos"])
            lap_sens.append(dict(file=name, dE=l1["E"] - l0["E"], n_nonpos=[l0["n_nonpos"], l1["n_nonpos"]],
                                 logratio_mode1_over_mode0=f"{base:.2f} {coef:+.1f}*ln(floor)",
                                 at_floor={str(fl): round(base + coef * math.log(fl), 2) for fl in (1e-6, 1e-4, 1e-3)},
                                 excluding_nonpos_directions=round(base, 2), D=2 * dd["L"] - 5,
                                 dE_per_dim=round((l1["E"] - l0["E"]) / (2 * dd["L"] - 5), 3)))
    OUT["C7"] = dict(files=len(files), by_L=summ, top2_gap_distribution=gap_dist,
                     reconcile_5O37A_45=recon, laplace_clip_sensitivity=lap_sens)
    return summ


# ---------------------------------------------------------------- C6 information + break-even
def check_numbers(summ):
    info = {f"N={N}": round(math.log2(N), 3) for N in (128, 512)}  # <= log2 N bits (Thm 2(b), full support)
    # argmin readout, amplitude-amplified restarts vs classical multistart: Babbush et al. eq. (12), d = 2:
    # 1/q* = (t_Q S / (t_C R))^2, T* = t_Q^2 S / (t_C R^2), t_Q = iters * G_eval * 170 us (eqs 6-7)
    t_tof, iters = 170e-6, 200
    per_L = {}
    for L, s in summ.items():
        L_ = int(L)
        tC = s["t_restart_median_s"]
        inv_q_med = 1.0 / s["q_cluster_median"]
        G_pair = 1e3 * L_ * (L_ - 1) / 2 / 990          # 1e3 at L = 45 (990 pairs), scaled by pair count
        rows = []
        for label, G in (("fixed_1e3", 1e3), ("pair_scaled", G_pair), ("pair_scaled_x1e2", 1e2 * G_pair),
                         ("pair_scaled_x1e3", 1e3 * G_pair)):
            for S in (1, 8, 1000):
                for R in (1, 10, 100):
                    tQ = iters * G * t_tof
                    thr = (tQ * S / (tC * R)) ** 2
                    rows.append(dict(G=label, G_eval=G, S=S, R=R, t_Q_s=tQ, inv_q_star=thr,
                                     T_star_s=tQ ** 2 * S / (tC * R ** 2),
                                     log10_gap_to_median=math.log10(thr / inv_q_med)))
        per_L[L] = dict(t_C_s=tC, G_eval_pair_scaled=G_pair, inv_q_cluster_median=inv_q_med, rows=rows)
    # the note's former single-L threshold (t_C from the R64 test file, L = 45), kept for the review log
    f = os.path.join(ROOT, "research", "results", "RAW", "g1_modes_test", "5O37A_45_R64_s0.json")
    old = None
    if os.path.exists(f):
        d = json.load(open(f))
        tC = d["secs"] / d["restarts"]
        old = dict(t_restart_s=tC, inv_q_star_G1e3_S1=(iters * 1e3 * t_tof / tC) ** 2)
    OUT["C6"] = dict(info_bits=info, per_L=per_L, superseded_R64_threshold=old,
                     cp95_upper_inv_q_one_hit_in_256=1.0 / float(beta_dist.ppf(0.025, 1, 256)),
                     cp95_upper_inv_q_two_hits_in_256=1.0 / float(beta_dist.ppf(0.025, 2, 255)))


# ---------------------------------------------------------------- C8 explicit-register timing
def check_timing():
    rows = {}
    for D in (128, 512):
        A = RNG.normal(size=(D, D))
        A = A + A.T
        for fn, name in ((np.linalg.eigh, "eigh"), (np.linalg.eigvalsh, "eigvalsh")):
            ts = []
            for _ in range(7):
                t0 = time.perf_counter()
                fn(A)
                ts.append(time.perf_counter() - t0)
            rows[f"{name}_D{D}_ms_median"] = 1e3 * float(np.median(ts))
    try:
        import psutil
        rows["cpu_percent_during"] = psutil.cpu_percent(interval=0.5)
    except Exception:
        pass
    OUT["C8"] = rows


if __name__ == "__main__":
    check_prefix()
    check_solver_equivalence()
    check_hinged_gibbs()
    check_dephasing()
    check_hull()
    files, byL = census_rows()
    summ = census_summary(files, byL)
    check_numbers(summ)
    check_timing()
    print(json.dumps(OUT, indent=1, default=float))
