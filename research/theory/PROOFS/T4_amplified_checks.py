"""Companion checks for research/theory/PROOFS/T4_amplified_mode_finding.md (theory lane T4).

Default run (pure arithmetic + reading the G1 mode-census JSONs; < 1 min, one core):
    C1  exact reversible pebble game on a line: DP recursions F (clean) and G (garbage allowed), checked against
        brute-force BFS for n <= 8, s <= 4; time overhead G(K,s)/K for K = 256, 400, 1024, 2400, 4096
    C2  optimal expected-cost constant for amplitude amplification with known p (repeat fixed-m runs): phi/sin^2(phi)
    C3  Durr-Hoyer record process on measured basin masses: P(visit j) = w_j/W_j (Monte Carlo check of the lemma)
        and E[#A-applications]*sqrt(w_1) on every census crop (bound: 2 c_QS)
    C4  census summary: p_hit(best mode) vs L, censoring at 1/R, pooled / per-protein slope of ln p vs L,
        L-BFGS gradient evaluations per restart
    C5  Toffoli cost model per reversible gradient step C_step(L) (labelled constants, see note section 3.7)
    C6  break-even p* = (t_C/(c S t_Q))^2, T* = c^2 S t_Q^2 / t_C for the maps of note sec. 2.2 (incl. the one-evaluation
        floor FLOOR-E and the converged maps M-CONV / M-CONVx from C8), cost sources (nominal; frozen T3 v1 D1/D2c/D2g),
        classical t_g sources (A-C1; T3 measured), gate-H thresholds, 1 ns windows, stacked worst case, c sensitivity
    C8 summary: reads research/results/RAW/t4_converge/*.json (if present)
Optional (--energy; ~15-25 min on one loaded core): C7 per-restart L-BFGS evaluation counts, Hessian spectra and
fixed-step / clipped GD on crop 5O37A_45 (dev crop, seed-0 prior draws; the native structure is never read).
Optional (--converge CROP ...; minutes per crop): C8 converged re-relaxation of the census draws, pre-registered in
research/experiments/PREREGISTERED/PREREG_T4_C8_convergence.md; writes research/results/RAW/t4_converge/.

All numbers produced by C4/C7/C8 are PILOT (in-progress G1 data). Nothing here is quantum simulation.
"""
from __future__ import annotations

import argparse
import collections
import glob
import itertools
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
YEAR = 3.156e7
INF = 10 ** 18


# ----------------------------------------------------------------------------------------------------------- C1
def pebble_tables(N, S):
    """F[s, n]: min # step applications (forward or inverse) to reach {n} from {} holding <= s pebbles at once.
    G[s, n]: same, but other pebbles may remain at the end (enough inside A for amplitude amplification).
    Node 0 (the input x0) is always available and not counted."""
    F = np.full((S + 1, N + 1), INF, dtype=np.int64)
    G = F.copy()
    for s in range(1, S + 1):
        F[s, 1] = 1
        G[s, 1] = 1
        for n in range(2, N + 1):
            m = np.arange(1, n)
            F[s, n] = min(int((F[s, m] + F[s - 1, n - m] + F[s - 1, m]).min()), INF)
            g = int((F[s, m] + G[s - 1, n - m]).min())
            if n <= s:
                g = min(g, n)
            G[s, n] = min(g, INF)
    return F, G


def pebble_brute(n, s, garbage):
    start = frozenset()
    seen = {start: 0}
    dq = collections.deque([start])
    while dq:
        c = dq.popleft()
        if n in c and (garbage or c == frozenset([n])):
            return seen[c]
        for i in range(1, n + 1):
            if i == 1 or (i - 1) in c:
                d = c - {i} if i in c else c | {i}
                if len(d) <= s and d not in seen:
                    seen[d] = seen[c] + 1
                    dq.append(d)
    return INF


def check_c1():
    F, G = pebble_tables(64, 7)
    bad = [(n, s, gb) for n in range(1, 9) for s in range(1, 5) for gb in (False, True)
           if pebble_brute(n, s, gb) != (G if gb else F)[s, n]]
    print(f"C1 DP vs brute force (n<=8, s<=4): {'OK' if not bad else 'MISMATCH ' + str(bad)}")
    print("C1 max K reachable with s pebbles: clean F:", [int((F[s] < INF).sum()) for s in range(1, 7)],
          " garbage-allowed G:", [int((G[s] < INF).sum()) for s in range(1, 7)])
    N = max([4096] + [int(v[1]) + 1 for v in c8_keff().values()])     # cover the C8 converged budgets
    _, G = pebble_tables(N, 40)
    for K in (256, 400, 1024, 2400, 4096):
        smin = math.ceil(math.log2(K + 1))
        row = [f"s={s}:{G[s, K] / K:.2f}" for s in sorted({smin, 12, 16, 20, 24, 32, 40}) if s >= smin and G[s, K] < INF]
        print(f"C1 K={K:5d}: time overhead G(K,s)/K  " + "  ".join(row))
    return G


# ----------------------------------------------------------------------------------------------------------- C2
def check_c2():
    phis = np.linspace(0.01, math.pi / 2, 200001)
    f = phis / np.sin(phis) ** 2
    i = int(np.argmin(f))
    print(f"C2 known p, repeated fixed-m runs: expected A-applications * sqrt(p) -> min phi/sin^2 phi = {f[i]:.4f} "
          f"at phi = {phis[i]:.4f} (tan phi = 2 phi); single long run: pi/2 = {math.pi / 2:.4f}  "
          f"[= BBHT sec. 3: 2 x 0.69003 iterations]")
    # lower bound on the expected number of A-applications for ANY strategy (Zalka: with k queries the success
    # probability is at most sin^2((2k+1) theta) for k <~ pi/(4 theta); intermediate measurements by deferred measurement):
    # E[#queries] >= sum_k P(T > k) >= sum_{k: (2k+1) theta <= pi/2} cos^2((2k+1) theta);  N_A = 2 #queries + 1
    for p in (1e-2, 1e-4, 1e-6):
        th = math.asin(math.sqrt(p))
        ks = np.arange(0, int((math.pi / (2 * th) - 1) / 2) + 1)
        lb = 1 + 2 * np.sum(np.cos((2 * ks + 1) * th) ** 2)
        print(f"C2 lower bound, any strategy, p={p:g}: E[N_A]*sqrt(p) >= {lb * math.sqrt(p):.3f} (limit pi/4 = {math.pi / 4:.3f})")
    print("C2 unknown p (BBHT Thm 3 proof, lambda=6/5): <= (9/2) m0 Grover iterations, m0 = 1/sin(2 theta) ~ 1/(2 sqrt p)"
          " -> c_QS <= 2 x 9/4 = 4.5 A-applications per 1/sqrt(p) (+ one A per round), t << N")


# ----------------------------------------------------------------------------------------------------------- C3/C4
def load_census():
    rows = collections.defaultdict(dict)
    for f in sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "g1_modes", "*.json"))):
        r = json.load(open(f))
        rows[r["L"]][r["crop"].split("_")[0]] = r
    return rows


def dh_cost(w):
    """Expected # of threshold levels weighted by 1/sqrt(W_{j-1}) (units of c_QS) for the record process on basin
    masses w (energy order).  Unlisted tail mass bounded by the integral."""
    W = np.cumsum(w)
    q = 1.0 + sum((w[j] / W[j]) / math.sqrt(W[j - 1]) for j in range(1, len(w)))
    if W[-1] < 1 - 1e-12:
        q += 2 * (W[-1] ** -0.5 - 1)
    return q


def check_c3(rows, rng):
    # Monte Carlo check of P(visit j) = w_j / W_j on a random 12-basin spectrum
    w = rng.dirichlet(np.ones(12) * 0.5)
    W = np.cumsum(w)
    cnt = np.zeros(12)
    n = 200000
    for _ in range(n):
        j = rng.choice(12, p=w)
        cnt[j] += 1
        while j > 0:
            j = rng.choice(j, p=w[:j] / W[j - 1])
            cnt[j] += 1
    err = np.max(np.abs(cnt / n - w / W))
    print(f"C3 record-process lemma P(visit j)=w_j/W_j, Monte Carlo n={n}: max abs error {err:.4f}")
    for L in sorted(rows):
        q, c, r = [], [], []
        for rr in rows[L].values():
            ww = np.array(rr["mode_sizes"], float) / rr["restarts"]
            qq = dh_cost(ww)
            q.append(qq); c.append(1 / ww[0]); r.append(qq * math.sqrt(ww[0]))
        print(f"C3 L={L:3d}: median E[N_A]/c_QS {np.median(q):5.1f}  median classical 1/w1 {np.median(c):5.1f}  "
              f"E[N_A]*sqrt(w1)/c_QS median {np.median(r):.2f} max {np.max(r):.2f} (bound 2)")


def check_c4(rows):
    allL, allp = [], []
    for L in sorted(rows):
        p = np.array([r["p_hit_best_mode"] for r in rows[L].values()])
        R = np.array([r["restarts"] for r in rows[L].values()])
        ge = np.array([r["grad_evals"] / r["restarts"] for r in rows[L].values()])
        nm = np.array([r["n_modes"] for r in rows[L].values()])
        cens = np.mean(p <= 1.5 / R)
        print(f"C4 L={L:3d} crops={len(p):2d} R={int(R[0])}: p_hit median {np.median(p):.3f} q25 {np.quantile(p, .25):.4f} "
              f"min {p.min():.4f} censored(<=1/R) {cens:.2f} | modes median {np.median(nm):.0f} | "
              f"grad evals/restart mean {ge.mean():.0f} max {ge.max():.0f}")
        allL += [L] * len(p)
        allp += list(np.log(p))
        # energy-level masses (the marked set of the algorithm: E(Phi(x0)) <= E_best + dE), stored by the census
        fw = {d: np.array([r["frac_within_dE"][d] for r in rows[L].values()]) for d in ("1.0", "5.0", "20.0")}
        print(f"C4 L={L:3d} energy-level p(dE) [200-it map]: " + " | ".join(
            f"dE={float(d):g}: median {np.median(v):.4f} q25 {np.quantile(v, .25):.4f} single-hit {np.mean(v <= 1.5 / R):.2f}"
            for d, v in fw.items()))
    from scipy.stats import beta
    print(f"C4 single hit in R=256: p-hat = {1 / 256:.4f}, Clopper-Pearson 95% [{beta.ppf(.025, 1, 256):.1e}, "
          f"{beta.ppf(.975, 2, 255):.1e}]")
    Ls = [L for L in sorted(rows) if len(rows[L]) >= 10]          # lengths with a usable number of crops
    common = set.intersection(*[set(rows[L]) for L in Ls]) if Ls else set()
    sl = [np.polyfit(Ls, [math.log(rows[L][k]["p_hit_best_mode"]) for L in Ls], 1)[0] for k in sorted(common)]
    if sl:
        print(f"C4 slope d ln p_hit / dL: pooled (all L) {np.polyfit(allL, allp, 1)[0]:.4f}; per-protein over L={Ls} "
              f"({len(sl)} proteins) median {np.median(sl):.4f} IQR [{np.quantile(sl, .25):.4f}, {np.quantile(sl, .75):.4f}]"
              " (censoring at 1/R biases toward 0)")


# ----------------------------------------------------------------------------------------------------------- C5/C6
def c_pair(b=20, Gtab=1001, mulc=1.0, lookup="unary"):
    """Toffolis per (i<j, |i-j|>=3) pair per reversible gradient step: CA + CB channels + sterics (A-T1..A-T4)."""
    lk = 2 * Gtab if lookup == "unary" else 2 * 2 * math.sqrt(Gtab * 2 * b)
    fwd = 12 * mulc * b * b + lk + 10 * b          # linear terms: difference 3b + accumulation 7b (v1 had 12b)
    return 2 * fwd * 4 + 3 * mulc * b * b * 4


def c_res(b=20):
    return (100 * b * b + 2.1e5) * 4


def C_step(L, **kw):
    b = kw.get("b", 20)
    return c_pair(**kw) * (L - 2) * (L - 3) / 2 + c_res(b) * L


def t_grad(L):
    return 1.8e-3 * (L / 150.0) ** 2          # A-C1: orchestrator-reported 1.8 ms at L=150, one core, scaled as L^2


def check_c5():
    print(f"C5 c_pair(b=20, unary)={c_pair():.3g}  c_pair(b=16, 0.5 b^2 mult, QROAM)={c_pair(b=16, mulc=0.5, lookup='qroam'):.3g}"
          f"  c_res={c_res():.3g}")
    for L in (30, 45, 60, 80, 100, 150):
        print(f"C5 L={L:3d}: C_step nominal {C_step(L):.2e} | b=16 {C_step(L, b=16):.2e} | b=24 {C_step(L, b=24):.2e} | "
              f"aggressive {C_step(L, b=16, mulc=0.5, lookup='qroam'):.2e} Toffolis; pair share "
              f"{c_pair() * (L - 2) * (L - 3) / 2 / C_step(L):.2f}")


C_KNOWN = 1.3801          # BBHT sec. 3 / check C2: known p, repeat fixed-m runs (best known; used as nominal)
C_FLOOR = math.pi / 4     # C2 lower bound for any strategy (from Zalka's optimality)
C_QS_BBHT = 4.5           # BBHT Thm 3 proof, unknown p, t << N (upper bound for that algorithm)
DH_REAL = 1.8             # realised record-process factor on per-restart energy levels (C8), bound 2
T_TOF = {"170us": 170e-6, "1us": 1e-6, "1ns": 1e-9}


def t_grad_meas(L):
    """T3 `--timing` (RESOURCE_MODELS.md C2): PyTorch batch-64 energy+gradient per structure on a loaded machine,
    0.29 / 0.97 / 1.40 / 2.94 / 5.44 ms at L = 30 / 45 / 60 / 100 / 150; log-log interpolation in between."""
    pts = np.array([[30, 0.29e-3], [45, 0.97e-3], [60, 1.40e-3], [100, 2.94e-3], [150, 5.44e-3]])
    return float(np.exp(np.interp(math.log(L), np.log(pts[:, 0]), np.log(pts[:, 1]))))


def _qroam(d, M):
    """Berry et al. 2019 App. C as used by T3 v1: compute ceil(d/k)+M(k-1), measurement-based uncompute ceil(d/k')+k'."""
    ks = range(1, max(2, int(math.sqrt(d)) * 4))
    return min(math.ceil(d / k) + M * (k - 1) for k in ks) + min(math.ceil(d / k) + k for k in ks)


def C_E_T3v1(design, L, generous=False):
    """FROZEN re-implementation of T3 v1 (RESOURCE_MODELS.md v1, 2026-09-27 00:39: S1, secs 3.2-3.3) for one full
    coherent energy C_E = 2 C_build + 2 n_p tau.  Frozen because research/theory/T3_resource_model.py is being revised
    by the T3 lane; reproduces T3 v1's tau_D1 = 26,889, tau_D2 = 5,712 and build = 14.5e3 per residue (central)."""
    bw, bc, gs, u, sq, b = (16, 16, 512, 1.5, 0.5, 10) if generous else (20, 20, 1024, 2.0, 1.0, 10)
    sqdist = 5 * bw + 3 * sq * bw * bw
    if design == "D1":
        n, m, p = bw, 2, bw // 2
        invsqrt = n * n * (15 * m / 2 + 3) + 15 * n * p * m + n * (23 * m / 2 + 5) - 15 * p * p * m + 15 * p * m - 2 * m
        arith = sqdist + invsqrt + bw * bw + 2 * bw + bw * bw + bw
        look = _qroam(1001, 2 * bc)
    else:
        arith = sqdist + 3 * (bw * bw + bw)
        look = _qroam(gs, 4 * bc)
    tau = u * arith + look + 32
    build = 33 * bw * bw + 15 * bw + _qroam(2 ** b, 5 * bw) + _qroam(2 ** b, 2 * bw)
    return 2 * (L - 2) * build + 2 * ((L - 2) * (L - 3) // 2) * tau


def cstep_src(src, L):
    """Toffolis per reversible energy+gradient evaluation: this note's nominal model, or 3 C_E (T3's quantised-HMC
    gradient convention) from the frozen T3 v1 formulas."""
    if src == "nominal":
        return C_step(L)
    design, gen = {"T3-D1": ("D1", False), "T3-D2c": ("D2", False), "T3-D2g": ("D2", True)}[src]
    return 3 * C_E_T3v1(design, L, gen)


def c8_keff():
    """Per L from the C8 runs: (median over crops of the q90 evals/restart, max evals, mean of per-crop means)."""
    out = {}
    by = collections.defaultdict(list)
    for f in glob.glob(os.path.join(C8_DIR, "*.json")):
        r = json.load(open(f))
        ne = np.array(r["n_eval"])
        by[r["L"]].append((np.quantile(ne, .9), ne.max(), ne.mean()))
    for L, v in by.items():
        v = np.array(v)
        out[L] = (float(np.median(v[:, 0])), float(v[:, 1].max()), float(v[:, 2].mean()))
    return out


def breakeven(ge, cstep, t_tof, t_c, S=1, c=C_KNOWN):
    tQ = ge * cstep * t_tof
    return tQ, (t_c / (c * S * tQ)) ** 2, c * c * S * tQ * tQ / t_c


def check_c6(G):
    K_C = 209                                   # A-C2: PILOT mean L-BFGS evals / restart of the 200-iteration map
    rho = lambda K, s=24: G[s, int(K)] / int(K)
    k8 = c8_keff()
    Lc8 = sorted(k8)

    def conv(L, which):                          # converged-map budget; L beyond the C8 range -> largest measured L
        if not k8:
            return None
        Lx = max([x for x in Lc8 if x <= L], default=Lc8[0])
        q90, mx, mean = k8[Lx]
        return {"q90": max(400.0, q90), "max": mx, "mean": mean}[which]

    maps = {"M-LB2   (200-it map, 2 trials, K_eff=400, s=24)": lambda L: (400 * rho(400), K_C),
            "M-SLOT2 (200-it map, slot-compiled, K_eff=270, s=24)": lambda L: (270 * rho(270), K_C),
            "M-LB12  (200-it map, 12 trials, K_eff=2400, s=24)": lambda L: (2400 * rho(2400), K_C),
            "M-HB    (K=1e4 momentum+buffer, rho=1)": lambda L: (1.0e4, K_C)}
    if k8:
        maps["M-CONV  (converged, slot = max(400, q90) evals, s=24)"] = \
            lambda L: (conv(L, "q90") * rho(conv(L, "q90")), conv(L, "mean"))
        maps["M-CONVx (converged, slot = max evals, s=24)"] = \
            lambda L: (conv(L, "max") * rho(conv(L, "max")), conv(L, "mean"))
    maps["FLOOR   (one coherent energy+gradient per A, no pebbling)"] = lambda L: (1.0, 1.0)
    # absolute floor for ANY map that marks by energy: one coherent energy evaluation C_E = C_step/3 (T3's convention;
    # exact 3 C_E / 3 for the T3 sources) against a classical energy-only time t_E <= t_g (upper bound -> T* lower bound)
    maps["FLOOR-E (one coherent energy evaluation per A; t_E <= t_g)"] = lambda L: (1.0 / 3.0, 1.0)
    print(f"C6 c={C_KNOWN} (known p; floor pi/4, unknown threshold ~{DH_REAL}x{C_QS_BBHT}); t_C = K_C x t_g(A-C1); "
          f"A-application Toffolis = (gradient-equivalents incl. pebbling) x C_step(L)")
    if k8:
        print("C6 C8 converged budgets per L (median q90 / max / mean evals per restart):",
              {L: tuple(round(x) for x in k8[L]) for L in Lc8})
    for mn, fm in maps.items():
        for L in (30, 60, 100, 150):
            ge, kc = fm(L)
            tC = kc * t_grad(L)
            for tn, t in T_TOF.items():
                out = []
                for S in (1, 1e3):
                    tQ, ps, Ts = breakeven(ge, C_step(L), t, tC, S)
                    out.append(f"S={S:g}: p*={ps:.1e} T*={Ts / YEAR:.1e}yr")
                print(f"C6 {mn[:7]} L={L:3d} K_eff*rho={ge:7.4g} t_Tof={tn:5s}: t_C={tC:.3g}s t_Q={tQ:.2e}s "
                      f"R={tQ / tC:.1e} | " + " | ".join(out))
    # gate-H margins T*/W_max for every cost source and both t_g sources (S = 1)
    for mn in [m for m in maps if m.startswith(("M-LB2", "M-CONV ", "M-CONVx", "FLOOR"))]:
        for src in ("nominal", "T3-D1", "T3-D2c", "T3-D2g"):
            for tgn, tg in (("A-C1", t_grad), ("meas", t_grad_meas)):
                row = []
                for tn in ("170us", "1us"):
                    Ts = [breakeven(maps[mn](L)[0], cstep_src(src, L), T_TOF[tn], maps[mn](L)[1] * tg(L))[2] / YEAR
                          for L in (30, 60, 100, 150)]
                    row.append(f"{tn}: " + " / ".join(f"{x:.1e}" for x in Ts))
                print(f"C6 T*[yr] S=1 L=30/60/100/150 {mn[:7]} {src:7s} t_g={tgn}: " + " | ".join(row))
    # ratio of T3's 3 C_E to this note's C_step
    for src in ("T3-D1", "T3-D2c", "T3-D2g"):
        print(f"C6 3*C_E({src})/C_step(nominal) at L=30/60/100/150: " +
              " / ".join(f"{cstep_src(src, L) / C_step(L):.2f}" for L in (30, 60, 100, 150)))
    # hardware needed for gate H (T* <= 1 yr)
    for mn in [m for m in maps if m.startswith(("M-LB2", "M-CONV ", "M-CONVx"))]:
        for src in ("nominal", "T3-D2g"):
            for tgn, tg in (("A-C1", t_grad), ("meas", t_grad_meas)):
                for S in (1, 1e3):
                    th = []
                    for L in (30, 60, 100, 150):
                        ge, kc = maps[mn](L)
                        tq = math.sqrt(YEAR * kc * tg(L) / (C_KNOWN ** 2 * S))
                        th.append(tq / (ge * cstep_src(src, L)))
                    print(f"C6 gate H (T*<=1yr) {mn[:7]} {src:7s} t_g={tgn} S={S:g}: t_Tof <= " +
                          " / ".join(f"{x * 1e9:.3g}ns" for x in th) + " at L=30/60/100/150")
    # window at 1 ns: p in [(c tQ/W)^2, p*]; width factor (W/T*)^2
    for mn in [m for m in maps if m.startswith(("M-LB2", "M-CONV ", "M-CONVx"))]:
        for L in (60, 100, 150):
            ge, kc = maps[mn](L)
            tQ, ps, Ts = breakeven(ge, C_step(L), 1e-9, kc * t_grad(L))
            lo = (C_KNOWN * tQ / YEAR) ** 2
            print(f"C6 window 1ns S=1 W=1yr {mn[:7]} L={L}: p in [{lo:.1e}, {ps:.1e}]"
                  f"{'' if lo < ps else '  EMPTY'}; width factor (W/T*)^2 = {(YEAR / Ts) ** 2:.1e}")
    # worst case for the verdict (all quantum-favourable choices stacked), S = 1
    for L in (30, 60, 100):
        for c, cn in ((C_KNOWN, "c=1.38"), (C_FLOOR, "c=pi/4")):
            ge = 270 * rho(270, 40)
            tQ, ps, Ts = breakeven(ge, cstep_src("T3-D2g", L), 1e-6, K_C * t_grad_meas(L), 1, c)
            print(f"C6 worst case L={L} (T3-D2g, t_g measured, s=40 rho={rho(270, 40):.2f}, K_eff=270, {cn}), 1us: "
                  f"T* = {Ts / YEAR:.1f} yr, p* = {ps:.1e}; 170us: {Ts * (170 ** 2) / YEAR:.2e} yr")
        if k8:     # stacked worst case with the converged task map (max budget), 40 pebbles
            Kx = conv(L, "max")
            for c, cn in ((C_KNOWN, "c=1.38"), (C_FLOOR, "c=pi/4")):
                tQ, ps, Ts = breakeven(Kx * rho(Kx, 40), cstep_src("T3-D2g", L), 1e-6, conv(L, "mean") * t_grad_meas(L), 1, c)
                print(f"C6 worst case, converged task map L={L} (M-CONVx K_eff={Kx:.0f}, s=40 rho={rho(Kx, 40):.2f}, T3-D2g, "
                      f"t_g measured, {cn}), 1us: T* = {Ts / YEAR:.1f} yr, p* = {ps:.1e}")
        if k8:     # the convergence factor: converged task map (max budget, C8 mean K_C) vs M-SLOT2, same costs
            f_conv = (maps["M-CONVx (converged, slot = max evals, s=24)"](L)[0] ** 2 / conv(L, "mean")) /                      ((270 * rho(270)) ** 2 / K_C)
            print(f"C6 convergence factor L={L}: T*(M-CONVx)/T*(M-SLOT2) = {f_conv:.1f}")
    # sensitivity to c: T* scales as c^2
    for c, cn in ((C_FLOOR, "pi/4 (floor)"), (C_KNOWN, "1.38 (known p)"), (DH_REAL * C_QS_BBHT, "8.1 (record, BBHT)")):
        print(f"C6 c = {cn}: T* x {(c / C_KNOWN) ** 2:.2f} relative to c = 1.38")


# ----------------------------------------------------------------------------------------------------------- C7
def check_c7():
    sys.path.insert(0, os.path.join(ROOT, "src"))
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    import torch
    from qapf.protein import energy as EN
    from qapf.sampling import hrex as H

    def kabsch(A, B):
        A = A - A.mean(0); B = B - B.mean(0)
        U, S_, Vt = np.linalg.svd(A.T @ B); S_[-1] *= np.sign(np.linalg.det(U @ Vt))
        return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S_.sum(), 0) / len(A)))

    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", "5O37A_45.npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    x0 = H.ExactPrior(en, 1.0).sample(64, np.random.default_rng(0))
    ng = []
    for r in range(64):
        n0 = en.n_grad
        EN.lbfgs(en, x0[r:r + 1], iters=200)
        ng.append(en.n_grad - n0)
    ng = np.array(ng)
    print(f"C7 L-BFGS evals/restart (B=1): mean {ng.mean():.0f} median {np.median(ng):.0f} min {ng.min()} "
          f"q10 {np.quantile(ng, .1):.0f} q90 {np.quantile(ng, .9):.0f} max {ng.max()}")
    R = 16
    xl, El = EN.relax(en, x0[:R], iters=200)
    Cl = en.coords(xl)
    lm = []
    for i in range(R):
        Hm = torch.autograd.functional.hessian(lambda q: en.energy_t(q)[0], torch.as_tensor(xl[i:i + 1]))[0, :, 0, :].numpy()
        w = np.linalg.eigvalsh(0.5 * (Hm + Hm.T)); lm.append((w.max(), w[w > 1e-3].min()))
    lm = np.array(lm)
    print(f"C7 Hessian at L-BFGS endpoints: lambda_max median {np.median(lm[:, 0]):.3g}, max {lm[:, 0].max():.3g}; "
          f"smallest eigenvalue > 1e-3 median {np.median(lm[:, 1]):.3g}")
    for name, eta, clip in (("GD eta=2e-5", 2e-5, None), ("clipped GD eta=1e-3 clip=0.02", 1e-3, 0.02)):
        x = x0[:R].copy(); E, Gd = en(x)
        for k in range(1, 10001):
            dx = eta * Gd
            if clip is not None:
                dx = np.clip(dx, -clip, clip)
            x = x - dx; E, Gd = en(x)
        C = en.coords(x)
        same = np.mean([kabsch(C[i], Cl[i]) < 2.0 for i in range(R)])
        print(f"C7 {name}, K=1e4: same basin as L-BFGS {same:.2f}; median E - E_LBFGS {np.median(E - El):.1f}")


# ----------------------------------------------------------------------------------------------------------- C8
C8_DIR = os.path.join(ROOT, "research", "results", "RAW", "t4_converge")


def lbfgs_tracked(f, x0, iters, m=8, c1=1e-4, max_ls=12, tol=1e-6, step0=None, snap=200):
    """src/qapf/protein/energy.py::lbfgs, same logic line for line, plus per-element counters.
    Returns dict: x, E (at stop or `iters`), x_snap/E_snap (after `snap` iterations = the census map), it_done
    (iterations in which the element was active), n_eval (energy+gradient evaluations, incl. the initial one),
    stopped (True if the code's own stopping rule fired before `iters`)."""
    x = np.array(x0, np.float64, copy=True)
    B, P = x.shape
    E, G = f(x)
    n_eval = np.ones(B, np.int64)
    it_done = np.zeros(B, np.int64)
    S, Y, RHO = [], [], []
    active = np.ones(B, bool)
    x_snap, E_snap = None, None
    for it in range(iters):
        it_done += active
        q = G.copy()
        al = []
        for s, y, rho in zip(reversed(S), reversed(Y), reversed(RHO)):
            a = rho * (s * q).sum(1)
            q -= a[:, None] * y
            al.append(a)
        if S:
            s, y = S[-1], Y[-1]
            yy = (y * y).sum(1)
            gam = np.where(yy > 1e-12, (s * y).sum(1) / np.maximum(yy, 1e-12), 1.0)
            gam = np.where(gam > 0, gam, 1.0)
        else:
            gn = np.linalg.norm(G, axis=1)
            gam = (step0 if step0 is not None else 0.1) / np.maximum(gn, 1e-12)
        r = gam[:, None] * q
        for (s, y, rho), a in zip(zip(S, Y, RHO), reversed(al)):
            bb = rho * (y * r).sum(1)
            r += s * (a - bb)[:, None]
        d = -r
        gd = (G * d).sum(1)
        bad = gd >= 0
        if bad.any():
            d[bad] = -G[bad] * (0.1 / np.maximum(np.linalg.norm(G[bad], axis=1, keepdims=True), 1e-12))
            gd[bad] = (G[bad] * d[bad]).sum(1)
        t = np.ones(B)
        acc = ~active
        xn, En, Gn = x.copy(), E.copy(), G.copy()
        for _ in range(max_ls):
            todo = ~acc
            if not todo.any():
                break
            idx = np.where(todo)[0]
            xt = x[idx] + t[idx, None] * d[idx]
            Et, Gt = f(xt)
            n_eval[idx] += 1
            ok = Et <= E[idx] + c1 * t[idx] * gd[idx]
            good = idx[ok]
            xn[good], En[good], Gn[good] = xt[ok], Et[ok], Gt[ok]
            acc[good] = True
            t[idx[~ok]] *= 0.3
        moved = acc & active
        s = xn - x; y = Gn - G
        sy = (s * y).sum(1)
        rho = np.where(moved & (sy > 1e-10), 1.0 / np.maximum(sy, 1e-10), 0.0)
        dE = E - En
        x, E, G = xn, En, Gn
        S.append(np.where(rho[:, None] > 0, s, 0.0)); Y.append(np.where(rho[:, None] > 0, y, 0.0)); RHO.append(rho)
        if len(S) > m:
            S.pop(0); Y.pop(0); RHO.pop(0)
        active &= acc
        active &= ~(dE < tol * np.maximum(1.0, np.abs(E)))
        if it + 1 == snap:
            x_snap, E_snap = x.copy(), E.copy()
        if not active.any():
            break
    if x_snap is None:                       # everything stopped before `snap` iterations
        x_snap, E_snap = x.copy(), E.copy()
    return dict(x=x, E=E, x_snap=x_snap, E_snap=E_snap, it_done=it_done, n_eval=n_eval, stopped=~active,
                gnorm=np.linalg.norm(G, axis=1))


def _kabsch(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S_, Vt = np.linalg.svd(A.T @ B); S_[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A ** 2).sum() + (B ** 2).sum() - 2 * S_.sum(), 0) / len(A)))


def _cluster(C, E, thr=2.0):
    """Greedy CA-RMSD clustering in energy order, exactly as scripts/g1_mode_census.py."""
    reps, assign = [], np.full(len(E), -1)
    for i in np.argsort(E):
        for c, r in enumerate(reps):
            if _kabsch(C[i], C[r]) < thr:
                assign[i] = c; break
        else:
            assign[i] = len(reps); reps.append(int(i))
    return assign


def check_c8_run(crop, restarts=256, max_iters=5000, seed=0):
    """Re-relax the census's own prior draws (same crop, seed, R, chunks of 64) with the census L-BFGS but a
    convergence-based stop (the code's own relative-decrease / Armijo-failure rule) and up to `max_iters`
    iterations. Stores per-restart endpoint energies for both the 200-iteration census map and the converged map.
    DEP only: the native structure in the npz is never read."""
    sys.path.insert(0, os.path.join(ROOT, "src"))
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    import time
    from qapf.protein import energy as EN
    from qapf.sampling import hrex as H
    os.makedirs(C8_DIR, exist_ok=True)
    fj = os.path.join(C8_DIR, f"{crop}_R{restarts}_s{seed}_it{max_iters}.json")
    if os.path.exists(fj):
        print("exists", fj); return
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", crop + ".npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    x0 = H.ExactPrior(en, 1.0).sample(restarts, np.random.default_rng(seed))
    t0 = time.time()
    outs = [lbfgs_tracked(en, x0[s:s + 64], iters=max_iters) for s in range(0, restarts, 64)]
    cat = {k: np.concatenate([o[k] for o in outs]) for k in outs[0]}
    res = dict(crop=crop, L=L, restarts=restarts, seed=seed, max_iters=max_iters, snap=200,
               E200=cat["E_snap"].tolist(), Econv=cat["E"].tolist(), it_done=cat["it_done"].tolist(),
               n_eval=cat["n_eval"].tolist(), stopped=cat["stopped"].tolist(), gnorm=cat["gnorm"].tolist())
    for tag, xk, Ek in (("200", cat["x_snap"], cat["E_snap"]), ("conv", cat["x"], cat["E"])):
        a = _cluster(en.coords(xk), Ek)
        res["assign_" + tag] = a.tolist()
    res["secs"] = time.time() - t0
    json.dump(res, open(fj, "w"))
    print(f"C8 {crop}: done in {res['secs']:.0f}s -> {fj}")


def dh_levels(E, target_mask):
    """Record process on per-restart endpoint energies (each restart = mass 1/R, one level per distinct energy),
    target = marked set; returns E[#A]/c_QS to first reach the target set."""
    R = len(E)
    p = target_mask.mean()
    Eo = np.sort(E[~target_mask])
    q = 1.0
    W_below = p
    for e in Eo:                              # levels above the target in increasing energy
        W_j = W_below + 1.0 / R
        q += (1.0 / R) / W_j / math.sqrt(W_below)
        W_below = W_j
    return q


def check_c8_summary():
    fs = sorted(glob.glob(os.path.join(C8_DIR, "*.json")))
    if not fs:
        print("C8: no converged-relaxation runs found in", C8_DIR); return
    census = load_census()
    byL = collections.defaultdict(list)
    for f in fs:
        r = json.load(open(f))
        E2, Ec = np.array(r["E200"]), np.array(r["Econv"])
        it, ne, stp = np.array(r["it_done"]), np.array(r["n_eval"]), np.array(r["stopped"])
        a2, ac = np.array(r["assign_200"]), np.array(r["assign_conv"])
        cap200 = it > 200                    # still active after 200 iterations -> the census map truncated it
        cen = census.get(r["L"], {}).get(r["crop"].split("_")[0])
        row = dict(crop=r["crop"], L=r["L"], R=len(E2), cap200=cap200.mean(), capmax=(~stp).mean(),
                   drop_med=float(np.median((E2 - Ec)[cap200])) if cap200.any() else 0.0,
                   ne_mean=ne.mean(), ne_med=np.median(ne), ne_q90=np.quantile(ne, .9), ne_max=ne.max(),
                   it_med=np.median(it), it_max=it.max(),
                   E200min=E2.min(), Econvmin=Ec.min(),
                   p_rmsd_200=np.mean(a2 == a2[np.argmin(E2)]), p_rmsd_conv=np.mean(ac == ac[np.argmin(Ec)]),
                   nmodes_200=len(set(a2)), nmodes_conv=len(set(ac)),
                   census_Ebest=cen["E_best"] if cen else float("nan"),
                   census_p=cen["p_hit_best_mode"] if cen else float("nan"))
        for tag, Ek in (("200", E2), ("conv", Ec)):
            for dE in (0.1, 1.0, 5.0, 20.0):
                mk = Ek <= Ek.min() + dE
                row[f"pE{dE:g}_{tag}"] = mk.mean()
                row[f"dh{dE:g}_{tag}"] = dh_levels(Ek, mk)
        # evaluations needed by the target restarts (converged energy within 1 nat of the best): the slot budget must
        # cover them, or the coherent map loses exactly the restarts it is looking for
        tgt = Ec <= Ec.min() + 1.0
        row["tgt_ne_max"] = int(ne[tgt].max()); row["tgt_pct"] = float(np.mean(ne <= ne[tgt].max()))
        # gap best -> second RMSD mode (energy of lowest member of the 2nd-lowest cluster)
        for tag, Ek, ak in (("200", E2, a2), ("conv", Ec, ac)):
            reps = sorted({int(c): Ek[ak == c].min() for c in set(ak)}.values())
            row["gap12_" + tag] = reps[1] - reps[0] if len(reps) > 1 else float("nan")
        byL[r["L"]].append(row)
        print(f"C8 {r['crop']:9s} R={len(E2)} secs={r['secs']:.0f}: capped@200 {row['cap200']:.2f} capped@{r['max_iters']} "
              f"{row['capmax']:.2f} | evals/restart mean {row['ne_mean']:.0f} med {row['ne_med']:.0f} q90 {row['ne_q90']:.0f} "
              f"max {row['ne_max']} | median extra drop (capped) {row['drop_med']:.1f} nats | gap best->2nd mode 200: "
              f"{row['gap12_200']:.1f} conv: {row['gap12_conv']:.1f} | census check E_best {row['census_Ebest']:.2f} vs "
              f"{row['E200min']:.2f}, p {row['census_p']:.4f} vs {row['p_rmsd_200']:.4f} | Emin conv {row['Econvmin']:.2f}")
        print(f"C8 {r['crop']:9s}   p_rmsd 200/conv {row['p_rmsd_200']:.4f}/{row['p_rmsd_conv']:.4f} modes {row['nmodes_200']}/"
              f"{row['nmodes_conv']} | energy-level p(dE) 200: " +
              " ".join(f"{d:g}:{row[f'pE{d:g}_200']:.4f}" for d in (0.1, 1, 5, 20)) + " | conv: " +
              " ".join(f"{d:g}:{row[f'pE{d:g}_conv']:.4f}" for d in (0.1, 1, 5, 20)) +
              f" | DH E[N_A]sqrt(p)/c_QS (dE=1) conv {row['dh1_conv'] * math.sqrt(row['pE1_conv']):.2f}"
              f" | target (1 nat) evals max {row['tgt_ne_max']} = percentile {100 * row['tgt_pct']:.0f}")
    for L in sorted(byL):
        rs = byL[L]
        med = lambda k: float(np.median([x[k] for x in rs]))
        # call counts to reach the energy-level target dE = 1 nat on the converged map (median over crops)
        pc = med("pE1_conv")
        print(f"C8 L={L:3d} calls to reach E <= Emin + 1 nat (converged map, median crop): classical 1/p = {1 / pc:.0f}; "
              f"quantum known p and threshold {C_KNOWN / math.sqrt(pc):.0f} (c=1.38); record process with BBHT c_QS=4.5: "
              f"{C_QS_BBHT * med('dh1_conv'):.0f}; realised record factor (median over crops of E[N_A] sqrt(p)/c_QS) "
              f"{np.median([x['dh1_conv'] * math.sqrt(x['pE1_conv']) for x in rs]):.2f}")
        print(f"C8 L={L:3d} ({len(rs)} crops): capped@200 median {med('cap200'):.2f} | capped@max median {med('capmax'):.2f}"
              f" | evals/restart mean-of-means {np.mean([x['ne_mean'] for x in rs]):.0f}, q90 median {med('ne_q90'):.0f}, "
              f"max {max(x['ne_max'] for x in rs)} | pE1 conv median {med('pE1_conv'):.4f}, pE20 conv median "
              f"{med('pE20_conv'):.4f} | p_rmsd conv median {med('p_rmsd_conv'):.4f} (200: {med('p_rmsd_200'):.4f})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--energy", action="store_true", help="also run the energy-based checks C7 (slow)")
    ap.add_argument("--converge", nargs="*", default=None,
                    help="C8: re-relax the census draws of these crops with a convergence-based stop (slow)")
    ap.add_argument("--max-iters", type=int, default=5000)
    a = ap.parse_args()
    if a.converge:
        for crop in a.converge:
            check_c8_run(crop, max_iters=a.max_iters)
        return
    rng = np.random.default_rng(7)
    G = check_c1()
    check_c2()
    rows = load_census()
    print("census snapshot:", {L: len(v) for L, v in sorted(rows.items())})
    check_c3(rows, rng)
    check_c4(rows)
    check_c5()
    check_c6(G)
    check_c8_summary()
    if a.energy:
        check_c7()


if __name__ == "__main__":
    main()
