"""Numerical checks for research/theory/PROOFS/T2_sampling_speedup_statement.md (v2, revised after review).

Every check backs a DERIVED statement or a Numbers table in that note. Nothing here is an experiment. The G1 pilot
and mode-census files are read READ-ONLY and are PILOT data (indicative only). No quantum simulation is involved.

    python research/theory/PROOFS/T2_sampling_checks.py            # ~2-3 min on one core (C4 simulates the DEO index process)
    python research/theory/PROOFS/T2_sampling_checks.py --fast     # ~30 s, fewer DEO replicates (coarser P(0))

Output is ASCII-only and stdout is reconfigured to UTF-8, so it runs under the default Windows console code page.

Checks
  C1  two-state (first-order) crossing: contribution to the thermodynamic length (pi) and to the Syed et al.
      communication barrier Lambda (1), independent of the latent jump dV; exact two-point stage count  [Lemma 2]
  C2  exponential-family overlap identity  BC(l,l') = exp(A((l+l')/2) - (A(l)+A(l'))/2);  exact chi^2 identity
      1+chi^2(pi_l || pi_l') = exp(A(2l-l') + A(l') - 2A(l)) ~ BC^-8;  Gaussian relation lambda_loc = sigma/sqrt(pi)  [Lemma 1]
  C3  toy first-order path (cooperative mean-field chain, prior = product): spectral gap vs coexistence barrier,
      stage count, overlap between pure phases, n_b of the greedy schedule, w_F at the forced rung      [Prop. 3]
  C4  G1 pilot NRPT runs: stationary ELE round-trip rate (Syed et al. Cor. 1) AND a simulation of the DEO index
      process under exact ELE from the production initial state with the production trip-counting rule
      (hrex.run_nrpt); P(0 trips); transit-aware 95% rate bound; ELE-floor cost per round trip; two stage-count
      estimators; glassy n_b; lower bounds on the range of the full energy                               [Numbers N1]
  C5  G1 mode-census snapshot: p_hit(best found mode) by chain length, floor-censored count            [Numbers N2]
  C6  break-even tables: T3's G(L) (RESOURCE_MODELS.md), overhead-corrected c(L), K, n_b, t_T scenarios  [Numbers N3, N4]
"""
from __future__ import annotations

import glob
import json
import math
import os
import sys

import numpy as np
from scipy import integrate
from scipy.linalg import eigh_tridiagonal
from scipy.special import gammaln

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
PILOT = os.path.join(ROOT, "research", "results", "RAW", "g1_pilot")
MODES = os.path.join(ROOT, "research", "results", "RAW", "g1_modes")
RNG = np.random.default_rng(20260926)
FAST = "--fast" in sys.argv
P_OVERLAP = math.exp(-2.0)          # Harrow-Wei p = e^-2 (kappa = 1)


def hdr(s):
    print("\n" + "=" * 100 + "\n" + s + "\n" + "=" * 100)


# ------------------------------------------------------------------ C1
def c1():
    hdr("C1  two-state crossing: thermodynamic length and communication barrier of the jump; exact two-point stages")
    sig = lambda x: 1.0 / (1.0 + np.exp(-x))
    tl, _ = integrate.quad(lambda x: math.sqrt(sig(x) * (1 - sig(x))), -80, 80)
    lb, _ = integrate.quad(lambda x: sig(x) * (1 - sig(x)), -80, 80)
    print(f"integral sqrt(w(1-w)) d(lam*dV) = {tl:.6f}   (pi = {math.pi:.6f})")
    print(f"integral w(1-w)       d(lam*dV) = {lb:.6f}   (1)")
    for dV in [5.0, 50.0, 500.0]:
        lam = np.linspace(-1, 1, 400001)
        w = sig(lam * dV)
        var = w * (1 - w) * dV ** 2
        loc = 0.5 * 2 * w * (1 - w) * dV
        print(f"  dV={dV:6.0f}: thermoLength={np.trapezoid(np.sqrt(var), lam):.4f}  Lambda={np.trapezoid(loc, lam):.4f}"
              "   (lam truncated to [-1,1])")
    # exact two-point stage count: pure phases with disjoint supports, BC(w,w') = sqrt(w w') + sqrt((1-w)(1-w'))
    p = P_OVERLAP
    w1 = 1 - p                                    # furthest reachable from w = 0 with BC^2 >= p
    print(f"two-point model, p = e^-2 = {p:.4f}: from w_F=0 the next rung can reach w_F <= 1-p = {w1:.4f};")
    print(f"  from w_F={w1:.4f}, BC^2 to w_F=1 is {w1:.4f} >= p: one intermediate rung, i.e. the jump costs <= 2 stages;")
    print(f"  the intermediate rung has w_F in [p, 1-p] = [{p:.3f}, {1 - p:.3f}]; w_F=0 -> 1 directly has BC = 0 (forbidden).")


# ------------------------------------------------------------------ C2
def c2():
    hdr("C2  overlap identity for pi_l ~ q exp(-l V); chi^2 identity; Gaussian relation lambda_loc = sigma/sqrt(pi)")
    n = 2000
    q = RNG.random(n); q /= q.sum()
    V = RNG.normal(0, 3, n) + 0.5 * RNG.standard_t(3, n)
    A = lambda l: np.log(np.sum(q * np.exp(-l * V)))
    worst = worst_chi = 0.0
    for l, lp in [(0.1, 0.2), (0.3, 0.9), (0.0, 1.0), (0.5, 0.52)]:
        p1 = q * np.exp(-l * V); p1 /= p1.sum()
        p2 = q * np.exp(-lp * V); p2 /= p2.sum()
        bc_direct = np.sum(np.sqrt(p1 * p2))
        bc_formula = math.exp(A((l + lp) / 2) - 0.5 * (A(l) + A(lp)))
        worst = max(worst, abs(bc_direct - bc_formula))
        chi_direct = np.sum(p1 ** 2 / p2)                       # 1 + chi^2(p1 || p2)
        chi_formula = math.exp(A(2 * l - lp) + A(lp) - 2 * A(l))
        worst_chi = max(worst_chi, abs(chi_direct - chi_formula) / chi_formula)
        pm = q * np.exp(-0.5 * (l + lp) * V); pm /= pm.sum()
        varm = np.sum(pm * V ** 2) - np.sum(pm * V) ** 2
        print(f"  l={l:.2f} l'={lp:.2f}: BC={bc_direct:.6f} (formula {bc_formula:.6f})  -lnBC={-math.log(bc_direct):.5f}"
              f"  (dl^2/8)Var_mid={(lp - l) ** 2 / 8 * varm:.5f}   1+chi^2={chi_direct:.4g}  BC^-8={bc_direct ** -8:.4g}")
    print(f"  max |BC_direct - BC_formula| = {worst:.2e};  max rel. error of the chi^2 identity = {worst_chi:.2e}")
    print("  (1+chi^2 ~ BC^-8 only for small steps; for large steps chi^2 is far larger than BC suggests)")
    s = 3.7
    a = RNG.normal(0, s, 2 * 10 ** 6); b = RNG.normal(0, s, 2 * 10 ** 6)
    print(f"  Gaussian: 0.5 E|V1-V2| = {0.5 * np.abs(a - b).mean():.4f}   sigma/sqrt(pi) = {s / math.sqrt(math.pi):.4f}")


# ------------------------------------------------------------------ C3
def toy_logpi(n, lam, J, p):
    m = np.arange(n + 1)
    V = -n * J * (m / n) ** p
    lp = gammaln(n + 1) - gammaln(m + 1) - gammaln(n - m + 1) - lam * V   # prior = Binomial(n,1/2) (product state)
    return lp - np.logaddexp.reduce(lp), V


def toy_gap(n, lam, J, p):
    """Lazy single-spin-flip Metropolis on n spins, lumped to m (the chain's permutation-symmetric sector)."""
    lp, V = toy_logpi(n, lam, J, p)
    m = np.arange(n + 1)
    up = np.zeros(n + 1); dn = np.zeros(n + 1)
    up[:-1] = 0.5 * ((n - m[:-1]) / n) * np.minimum(1, np.exp(-lam * (V[1:] - V[:-1])))
    dn[1:] = 0.5 * (m[1:] / n) * np.minimum(1, np.exp(-lam * (V[:-1] - V[1:])))
    w = eigh_tridiagonal(1 - up - dn, np.sqrt(up[:-1] * dn[1:]), eigvals_only=True)
    return 1 - np.sort(w)[-2]


def toy_barrier(lp):
    """free-energy barrier (nats) between the two outermost local maxima of log pi(m); 0 if unimodal. Also returns
    the position of the minimum between them (the interface) or None."""
    mx = [i for i in range(len(lp)) if (i == 0 or lp[i] >= lp[i - 1]) and (i == len(lp) - 1 or lp[i] >= lp[i + 1])]
    if len(mx) < 2:
        return 0.0, None
    i, j = mx[0], mx[-1]
    k = i + int(np.argmin(lp[i:j + 1]))
    return float(min(lp[i], lp[j]) - lp[k]), k


def c3():
    hdr("C3  toy first-order path: cooperative mean-field chain, V(m) = -n J (m/n)^p, p = 12, prior = product")
    p = 12
    J = math.log(2) / (0.45 * (1 - 2.0 ** -p))      # places coexistence near lam ~ 0.45 (as in the G1 pilot)
    lams = np.linspace(0, 1, 2001)
    rows = []
    print(" n   lam*   dF_barrier  delta_min   -ln delta_min  Lambda  thermoLen  stages(BC>=e^-1)  BC(lam*+-0.08)"
          "  QSA ell*delta^-1/2   classical 1/delta")
    extra = []
    for n in [25, 50, 75, 100]:
        coarse = lams[::5]
        ds = np.array([toy_gap(n, l, J, p) for l in coarse])
        i = int(np.argmin(ds)); lc = coarse[i]
        lpc, _ = toy_logpi(n, lc, J, p)
        dF, mb = toy_barrier(lpc)
        lps, var, loc = [], [], []
        for l in lams:
            lp, V = toy_logpi(n, l, J, p); P = np.exp(lp); mu = P @ V
            var.append(P @ (V - mu) ** 2)
            loc.append(0.5 * np.sum(P[:, None] * P[None, :] * np.abs(V[:, None] - V[None, :])))
            lps.append(lp)
        Lam = np.trapezoid(loc, lams); TL = np.trapezoid(np.sqrt(var), lams)
        k, stages, rung_idx = 0, 0, [0]
        while k < len(lams) - 1:
            j = k + 1
            while j < len(lams) and np.logaddexp.reduce(0.5 * (lps[k] + lps[j])) >= -1.0:
                j += 1
            k = max(j - 1, k + 1); stages += 1; rung_idx.append(k)
        a = np.argmin(np.abs(lams - (lc - 0.08))); b = np.argmin(np.abs(lams - (lc + 0.08)))
        bc_phases = math.exp(np.logaddexp.reduce(0.5 * (lps[a] + lps[b])))
        rows.append((n, lc, dF, ds.min()))
        print(f"{n:3d}  {lc:.3f}  {dF:8.2f}   {ds.min():.3e}   {-math.log(ds.min()):8.2f}     {Lam:5.2f}   {TL:6.2f}"
              f"        {stages:3d}            {bc_phases:.2e}        {stages * ds.min() ** -0.5:.2e}          {1 / ds.min():.2e}")
        # gaps at the schedule rungs, n_b, w_F at each rung, chi^2 warm-start factor per stage
        rl = lams[rung_idx]
        dr = np.array([toy_gap(n, l, J, p) for l in rl])
        dstar = dr.min()
        nb = 0.5 * sum(math.sqrt(dstar / dr[t]) + math.sqrt(dstar / dr[t + 1]) for t in range(len(rl) - 1))
        wF = [float(np.exp(lps[t][mb + 1:]).sum()) if mb is not None else float("nan") for t in rung_idx]
        chi = []
        for t in range(len(rung_idx) - 1):
            pa_, pb_ = np.exp(lps[rung_idx[t]]), np.exp(lps[rung_idx[t + 1]])
            chi.append(float(np.sum(pa_ ** 2 / pb_)))
        extra.append((n, rl, dr, dstar, ds.min(), nb, wF, chi))
    x = np.array([r[2] for r in rows]); y = np.array([-math.log(r[3]) for r in rows])
    slope, icpt = np.polyfit(x, y, 1)
    print(f"fit  -ln(delta_min) = {slope:.3f} * dF_barrier + {icpt:.2f}   (A-Arr: a ~ {slope:.2f}, ln C ~ {icpt:.1f})")
    print("\nschedule rungs of the greedy BC >= e^-1 schedule, gaps there, n_b = (1/2) sum_i [(d*/d_i)^1/2 + (d*/d_i+1)^1/2]:")
    for n, rl, dr, dstar, dmin, nb, wF, chi in extra:
        print(f"  n={n:3d}: rungs lam = {np.round(rl, 3).tolist()}  gaps = {[f'{v:.1e}' for v in dr]}  "
              f"d*(rungs)={dstar:.1e} vs min over lam {dmin:.1e}  n_b={nb:.2f}  w_F(rungs)={[round(v, 3) for v in wF]}  "
              f"1+chi^2(stage)={[f'{v:.2g}' for v in chi]}")
    print("reading: Lambda and the thermodynamic length stay O(1) (~1 and ~pi) while the gap closes like exp(-a dF);")
    print("         the forced intermediate rung has w_F in [p, 1-p] and carries the small gap; n_b ~ 1 (single-rung bottleneck);")
    print("         QSA cost ~ n_b * delta*^-1/2 vs classical annealing ~ delta^-1: halving in delta (DERIVED); in dF only via A-Arr.")


# ------------------------------------------------------------------ C4
def sim_trips(r, scans, reps, rng, f=1.0):
    """DEO index process under exact ELE (swap k<->k+1 accepted independently with probability 1-r'_k, where the
    rejection odds are scaled by f: r'/(1-r') = f r/(1-r); f=1 is the measured profile).  Initial state and trip
    counting copy hrex.run_nrpt production: identity labels, last_end=-1, a trip = bottom -> top -> bottom."""
    r = np.clip(np.asarray(r, float), 1e-12, 1 - 1e-12)
    acc = 1.0 / (1.0 + f * r / (1 - r))
    N = len(r) + 1
    track = np.tile(np.arange(N), (reps, 1))
    last = np.full((reps, N), -1, np.int8)
    trips = np.zeros(reps, np.int64)
    rows = np.arange(reps)
    for s in range(scans):
        for k in range(s % 2, N - 1, 2):
            ok = rng.random(reps) < acc[k]
            a = track[ok, k].copy()
            track[ok, k] = track[ok, k + 1]
            track[ok, k + 1] = a
        l0 = track[:, 0]
        trips += last[rows, l0] == 1
        last[rows, l0] = 0
        lt = track[:, N - 1]
        up = last[rows, lt] == 0
        last[rows[up], lt[up]] = 1
    return trips


def c4():
    hdr("C4  G1 pilot NRPT runs (READ-ONLY, PILOT): ELE round-trip predictions (stationary and transit-aware) vs observed")
    out = {}
    files = sorted(glob.glob(os.path.join(PILOT, "*_T1_s0.json")), key=lambda f: json.load(open(f))["L"])
    if not files:
        print("  no pilot files found"); return out
    reps = 4000 if FAST else 20000
    reps_b = 1000 if FAST else 4000
    rng = np.random.default_rng(11)
    print(f"DEO index-process simulation under exact ELE, {reps} replicates per run (production start, production counting)")
    print(" crop         L  rungs  Lambda  E(P_N)  scans  RT_stat  RT_sim(mean+-sd)  P(0)_sim         RT_obs  steps/scan"
          "  ELE floor/RT  95% bound/RT")
    for f in files:
        d = json.load(open(f))
        r = np.array(d["rej"]); E = float(np.sum(r / (1 - r)))
        s = d["grad_evals_production"] / d["scans"]
        tr = sim_trips(r, d["scans"], reps, rng)
        p0 = float(np.mean(tr == 0)); n0 = int(np.sum(tr == 0))
        p0s = f"{p0:.1e} ({n0}/{reps})" if n0 else f"<{3 / reps:.1e} (0/{reps})"
        floor = (2 + 2 * E) * s
        bound = float("nan")
        if p0 < 0.05:
            lo, hi = 1.0, 20.0
            for _ in range(7 if FAST else 9):
                fm = 0.5 * (lo + hi)
                if np.mean(sim_trips(r, d["scans"], reps_b, rng, f=fm) == 0) < 0.05:
                    lo = fm
                else:
                    hi = fm
            bound = (2 + 2 * 0.5 * (lo + hi) * E) * s
        z = np.load(f.replace(".json", ".npz")); pt = z["pair_trace"].astype(float); h = len(pt) // 2
        lams = np.array(d["lams"]); sd = pt[h:].std(0)
        TL = float(np.trapezoid(sd, lams))
        cum = np.concatenate([[0.0], np.cumsum(r)]); Lam = float(d["Lambda"])
        frac_lam = (Lam - np.interp(0.3, lams, cum)) / Lam
        ctl = np.concatenate([[0.0], np.cumsum(0.5 * (sd[1:] + sd[:-1]) * np.diff(lams))])
        frac_tl = (ctl[-1] - np.interp(0.3, lams, ctl)) / ctl[-1]
        E0p = float(pt[h:, 0].mean()); E1p = float(pt[h:, -1].mean()); E1 = float(z["E_top"][h:].mean())
        polE = float(d["eval"]["polishedE"])
        row = dict(L=d["L"], rungs=d["rungs"], Lambda=Lam, E=E, scans=d["scans"], rt_stat=d["scans"] / (2 + 2 * E),
                   rt_sim=float(tr.mean()), rt_sd=float(tr.std()), p0=p0, rt_obs=d["round_trips"], ge_scan=s,
                   floor=floor, bound=bound, s_ge=d["secs"] / d["grad_evals_total"],
                   ell_lam=math.sqrt(math.pi) * Lam / math.sqrt(8), ell_sd=TL / math.sqrt(8), TL=TL,
                   cs=math.sqrt(max(E0p - E1p, 0)) / math.sqrt(8), nb_glassy_lam=frac_lam * math.sqrt(math.pi) * Lam / math.sqrt(8),
                   nb_glassy_sd=frac_tl * TL / math.sqrt(8), E0V_E1V=E0p - E1p, range_lb=E0p - polE, diff_full=E0p - E1)
        out[d["L"]] = row
        print(f" {d['crop']:<11} {d['L']:3d}  {d['rungs']:3d}   {Lam:5.1f}  {E:6.1f}  {d['scans']:5d}  {row['rt_stat']:6.1f}"
              f"   {row['rt_sim']:5.2f} +- {row['rt_sd']:4.2f}     {p0s:<16} {d['round_trips']:4d}    {s:6.0f}"
              f"    {floor:9.2e}    {bound:9.2e}")
    print("notes: RT_stat = scans/(2+2E(P_N)) is the Syed et al. Cor. 1 STATIONARY rate. It ignores the initial transit: from")
    print("       identity labels a trip needs bottom -> top -> bottom, and the per-label round-trip time 2N(1+E) exceeds the")
    print("       run length at every L, so the correction is O(N) trips in aggregate, not O(1). RT_sim is the prediction.")
    print("       '95% bound/RT': smallest cost per round trip (local steps) consistent with 0 observed trips at 95%, within")
    print("       the model family 'ELE index process with all rejection odds scaled by f' (model-dependent; INFERENCE).")
    print("       'ELE floor/RT' = (2+2E) x steps/scan: the cost per round trip of an ideal ELE sampler on this schedule.")
    print("       At L >= 100 an ideal ELE sampler also shows 0 trips in these runs, so the runs carry no information there.")
    print("\nstage-count estimators, glassy n_b (stages at lam >= 0.3), energy-range lower bounds (PILOT, second halves):")
    print("   L   ell=0.63*Lambda  ell=thermoLen(SD)/sqrt8  CS estimate sqrt(E0V-E1V)/sqrt8  n_b(lam>=0.3): Lambda-based  SD-based"
          "   E0V-E1V   E0[E_pair]-E1[E]   E0[E_pair]-min E (range LB)")
    for L, w in out.items():
        print(f" {L:3d}       {w['ell_lam']:5.1f}              {w['ell_sd']:5.1f}                    {w['cs']:5.1f}"
              f"                         {w['nb_glassy_lam']:5.1f}       {w['nb_glassy_sd']:5.1f}    {w['E0V_E1V']:8.0f}"
              f"     {w['diff_full']:8.0f}          {w['range_lb']:8.0f}")
    print("notes: both ell estimators and the CS value use non-stationary replicas (S4); the CS value is a pilot estimate of")
    print("       the bound, biased low by the still-drifting lam=1 mean, not a valid upper bound.")
    print("       range LB: E_prior >= -1e-6 per residue (head probabilities <= 1, wall >= 0), so max E >= E_pair(prior draw),")
    print("       and min E <= polished lowest E; hence beta*Delta >= E0[E_pair] - E_polished for the FULL energy.")
    return out


# ------------------------------------------------------------------ C5
def c5():
    hdr("C5  G1 mode census snapshot (READ-ONLY, PILOT, still being written): p_hit of best found mode")
    by = {}
    for f in sorted(glob.glob(os.path.join(MODES, "*_R256_s0.json"))):
        try:
            d = json.load(open(f))
        except Exception:
            continue
        if "p_hit_best_mode" not in d:
            continue
        by.setdefault(d["L"], []).append((d["p_hit_best_mode"], d["n_modes"], d["grad_evals"] / d["restarts"]))
    for L in sorted(by):
        a = np.array(by[L])
        nfloor = int(np.sum(a[:, 0] <= 1.0 / 256 + 1e-12))
        print(f"  L={L:3d}: targets={len(a):2d}  at floor={nfloor:2d}  p_hit median={np.median(a[:, 0]):.3f}  min={a[:, 0].min():.4f}"
              f"  max={a[:, 0].max():.3f}  geo-mean={np.exp(np.mean(np.log(a[:, 0]))):.3f}  "
              f"modes median={np.median(a[:, 1]):.0f}  gradEv/restart={a[:, 2].mean():.0f}")
    print("  (256 restarts: p_hit < 1/256 cannot be resolved; 1/256 = 0.0039 is the floor; floor values are censored)")
    return by


# ------------------------------------------------------------------ C6
LS6 = (45, 60, 100, 120, 150)
G_FALLBACK = {  # T3 RESOURCE_MODELS.md G_lhpst, qubitised, evaluated at these L (used only if the T3 script is missing)
    "D2gen": {45: 1.00e7, 60: 1.75e7, 100: 4.75e7, 120: 6.81e7, 150: 1.06e8},
    "D2cen": {45: 4.63e7, 60: 8.24e7, 100: 2.29e8, 120: 3.29e8, 150: 5.14e8},
    "D3gen": {45: 4.97e6, 60: 6.49e6, 100: 1.12e7, 120: 1.39e7, 150: 1.82e7},
    "D3cen": {45: 1.00e7, 60: 1.29e7, 100: 2.16e7, 120: 2.64e7, 150: 3.42e7},
}
NL_FALLBACK = {"D2": {45: 1.50e4, 60: 1.98e4, 100: 3.26e4, 120: 3.90e4, 150: 4.86e4},
               "D3": {45: 6.04e3, 60: 7.08e3, 100: 9.64e3, 120: 1.08e4, 150: 1.27e4}}


def t3_tables():
    sys.path.insert(0, os.path.join(ROOT, "research", "theory"))
    try:
        import T3_resource_model as T3
        G = {f"{d}{k}": {L: T3.G_lhpst(d, L, P)[0] for L in LS6}
             for d in ("D2", "D3") for k, P in (("gen", T3.GENEROUS), ("cen", T3.CENTRAL))}
        NL = {d: {L: T3.qubits_lhpst(d, L, T3.CENTRAL) for L in LS6} for d in ("D2", "D3")}
        PH = {d: {L: T3.phys_qubits(NL[d][L]) for L in LS6} for d in ("D2", "D3")}
        return G, NL, PH, "T3_resource_model.py"
    except Exception as e:  # pragma: no cover
        PH = {d: {L: 2 * 32 ** 2 * v + 1.5e5 for L, v in NL_FALLBACK[d].items()} for d in NL_FALLBACK}
        return G_FALLBACK, NL_FALLBACK, PH, f"fallback table ({e})"


def c6(pilot):
    hdr("C6  break-even (T3 G(L); overhead-corrected c(L); labelled scenarios for t_T, K, n_b; rho = 1, A = 1)")
    G, NL, PH, src = t3_tables()
    print(f"G(L) source: {src}.  Designs (T3): D2 = torsion moves, spline pair terms, qubitised; D3 = Cartesian single-residue")
    print("moves (a DIFFERENT, bond-relaxed target with unknown per-step mixing kappa_D3). gen/cen = T3 generous/central.")
    # classical cost per local step: pilot wall-clock per grad-eval, corrected by the overhead factor at L=150
    s_ge = {L: pilot[L]["s_ge"] for L in pilot} if pilot else {45: 5.91e-4, 60: 7.81e-4, 100: 1.46e-3, 120: 2.39e-3, 150: 3.51e-3}
    ovh = s_ge[150] / 1.8e-3
    c = {L: s_ge[L] / ovh for L in LS6}
    ell = {L: (pilot[L]["ell_lam"], pilot[L]["ell_sd"]) if pilot else (float("nan"),) * 2 for L in LS6}
    nbg = {L: (pilot[L]["nb_glassy_lam"], pilot[L]["nb_glassy_sd"]) if pilot else (float("nan"),) * 2 for L in LS6}
    print(f"c(L) = pilot wall-clock per local step / {ovh:.2f} (sampler overhead measured at L=150: {s_ge[150]*1e3:.2f} vs 1.8 ms):")
    print("   " + "  ".join(f"L={L}: {c[L]*1e3:.2f} ms (uncorrected {s_ge[L]*1e3:.2f})" for L in LS6))
    print("   T3 placeholder 0.2 ms*(L/45)^2: " + "  ".join(f"L={L}: {0.2*(L/45)**2:.2f} ms" for L in LS6))
    print("B* = (K n_b G t_T / c)^2 local steps per sample at break-even (rho = 1, A = 1); B* ~ c^-2, so a smaller c raises B*.")
    aA, lnC = 1.095, 5.4
    print(f"dF* = (ln B* - ln C)/a with the C3 toy values a = {aA}, ln C = {lnC} (A-Arr; sensitivity only).")
    print("T*_Q = rho (K n_b G t_T)^2 / c = minimum quantum wall-clock per sample at break-even (= classical wall-clock at rho=1).")
    YR = 3.156e7

    def B(L, g, t, K, nb):
        return (K * nb * G[g][L] * t / c[L]) ** 2

    nb_cases = lambda L: {"n_b=1": 1.0, "n_b=2": 2.0, "glassy(Lam)": nbg[L][0], "glassy(SD)": nbg[L][1],
                          "ell(Lam)": ell[L][0], "ell(SD)": ell[L][1]}
    combos = [("1us", 1e-6, 10), ("1us", 1e-6, 100), ("1us", 1e-6, 1000), ("10us", 1e-5, 100), ("170us", 1.7e-4, 100),
              ("170us", 1.7e-4, 1000)]
    print("\nlog10 B* grid; columns (t_T, K): " + "  ".join(f"({a},{k})" for a, _, k in combos))
    for L in LS6:
        for g in ("D3gen", "D2gen", "D2cen"):
            for nk, nb in nb_cases(L).items():
                vals = "  ".join(f"{math.log10(B(L, g, t, K, nb)):6.2f}" for _, t, K in combos)
                print(f"  L={L:3d} {g:6s} {nk:12s} (n_b={nb:5.1f}):  {vals}")
    scen = [("most optimistic, A80 target", "D2gen", 1e-6, 10, "n_b=1"),
            ("most optimistic, D3 target", "D3gen", 1e-6, 10, "n_b=1"),
            ("A-FO central", "D2cen", 1e-5, 100, "n_b=2"),
            ("cited constants (K~750)", "D2cen", 1.7e-4, 1000, "n_b=2"),
            ("glassy (lam>=0.3 rungs)", "D2cen", 1e-5, 100, "glassy(Lam)"),
            ("pessimistic", "D2cen", 1.7e-4, 1000, "ell(SD)")]
    print("\nheadline scenarios (rho = 1, A = 1):")
    print(f"{'L':>4} {'scenario':30s} {'G':>9} {'t_T':>7} {'K':>5} {'n_b':>5} {'B*':>9} {'ln B*':>6} {'dF*':>6} {'T*_Q':>12}"
          f" {'logical q':>10} {'physical q':>10}")
    for L in (45, 100, 150):
        for name, g, t, K, nk in scen:
            nb = nb_cases(L)[nk]
            b = B(L, g, t, K, nb)
            Tq = (K * nb * G[g][L] * t) ** 2 / c[L]
            d = g[:2]
            print(f"{L:4d} {name:30s} {G[g][L]:9.2e} {t*1e6:5.0f}us {K:5d} {nb:5.1f} {b:9.2e} {math.log(b):6.1f}"
                  f" {(math.log(b) - lnC) / aA:6.1f} {Tq / YR:9.2e} yr {NL[d][L]:10.2e} {PH[d][L]:10.2e}")
    print("(qubits: T3 central, one factory, d = 31; rho = 1 prices this machine as one core.)")
    print("\nminimum useful runtime: t_T needed so that T*_Q <= budget (rho = 1; t_T scales as rho^-1/2):")
    for name, g, _, K, nk in scen[:3]:
        cells = []
        for L in (45, 100, 150):
            nb = nb_cases(L)[nk]
            day = math.sqrt(86400 * c[L]) / (K * nb * G[g][L])
            yr = math.sqrt(YR * c[L]) / (K * nb * G[g][L])
            cells.append(f"L={L}: {day*1e9:7.2f} ns (1 day) {yr*1e9:7.1f} ns (1 yr)")
        print(f"  {name:28s} " + " | ".join(cells))
    print("\nkill-rule thresholds: B*_min(L) over t_T >= 1 us, K >= 10, n_b >= 1, rho = 1, A = 1:")
    for L in LS6:
        m2 = B(L, "D2gen", 1e-6, 10, 1.0); m3 = B(L, "D3gen", 1e-6, 10, 1.0)
        print(f"  L={L:3d}: B*_min A80 (D2 gen) = {m2:.2e}   B*_min D3 gen = {m3:.2e}   threshold B*_min/10 = "
              f"{10 ** math.floor(math.log10(min(m2, m3) / 10)):.0e}")
    print("\n(I-5) amplitude-amplified multistart: p* = [(pi/2) O_rev G_grad t_T / c]^-2, G_grad = 3 G (A-Ggrad);")
    print("      Duerr-Hoyer minimum finding (constant 22.5 instead of pi/2) lowers p* by a further (22.5/(pi/2))^2 = "
          f"{(22.5 / (math.pi / 2)) ** 2:.0f}x")
    for L in (45, 100):
        vals = []
        for g in ("D2gen", "D2cen"):
            for tk, t in (("1us", 1e-6), ("170us", 1.7e-4)):
                for orv in (2.0, 10.0):
                    vals.append(((math.pi / 2) * orv * 3 * G[g][L] * t / c[L]) ** -2)
        print(f"  L={L:3d}: p* range {min(vals):.1e} - {max(vals):.1e}  (D2 gen/cen, t_T 1-170 us, O_rev 2-10)")


if __name__ == "__main__":
    c1(); c2(); c3()
    pilot = c4()
    c5()
    c6(pilot)
