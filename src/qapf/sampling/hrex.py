"""Classical sampling of learned-energy structure posteriors: non-reversible Hamiltonian replica exchange (NRPT)
along the PRIOR -> POSTERIOR path, with exact independent draws at the prior end.

Target family (internal coordinates x = (theta_1..theta_{L-2}, tau_1..tau_{L-3}), radians):
    pi_lam(x) ∝ exp( -[ E_prior(x) + lam * E_pair(x) ] / T )
    E_prior = w_tt * theta/tau-head NLL + w_w * theta wall      (a PRODUCT over residues -> exactly sampleable)
    E_pair  = w_ca * CA-pair NLL + w_cb * CB-pair NLL + w_s * sterics      (the long-range learned couplings)
lam = 1 is the learned-energy posterior of the A80 energy (qapf.protein.energy.Energy) at temperature T.

Why this path: lam = 0 is the learned per-residue prior, which is also the natural cheap quantum warm start (a product
state); a quantum simulated-annealing / quantum-walk sampler would traverse the same path.  The classical cost of
traversing it is therefore the quantity a quantum speedup must beat (research/THEORY_ROADMAP.md T2).

Classical method (state of the art for PT): deterministic even-odd (DEO) non-reversible swaps and the adaptive
schedule of Syed, Bouchard-Cote, Deligiannidis & Doucet (JRSS-B 2022): the global communication barrier
Lambda = sum_k r_k (r_k = swap rejection rate between rungs k, k+1) controls the round-trip rate; with N >> Lambda
rungs, round-trip rate -> 1 / (2 + 2 Lambda) per scan.  Local moves: HMC with per-rung adaptive step size and
reflecting theta boundaries; the lam = 0 rung is refreshed by an exact independent draw every scan.

Outputs (per scan): energies, rung indices of each replica (for round trips), swap acceptances; samples at lam = 1
(thinned) for posterior means and basin statistics.
"""
from __future__ import annotations

import math
import time

import numpy as np
import torch

from qapf.protein import energy as EN

TH_MIN, TH_MAX = 0.35, math.pi - 0.02


class SplitEnergy:
    """E_prior and E_pair (and total at per-row lam) with gradients, batched."""

    def __init__(self, en: EN.Energy, T: float = 1.0):
        self.en = en
        self.T = float(T)
        self.L = en.L
        self.n_grad = 0

    def split_t(self, xt):
        Tm = self.en.terms(xt)
        w = self.en.w
        prior = w["w_tt"] * Tm["tt"] + w["w_w"] * Tm["wall"]
        pair = w["w_ca"] * Tm["ca"] + w["w_cb"] * Tm["cb"] + w["w_s"] * Tm["st"]
        return prior, pair

    def u_and_grad(self, x, lam):
        """U = (E_prior + lam E_pair) / T per row; returns U, grad U, E_prior, E_pair (numpy)."""
        xt = torch.as_tensor(x, dtype=torch.float64).clone().requires_grad_(True)
        lt = torch.as_tensor(lam, dtype=torch.float64)
        prior, pair = self.split_t(xt)
        U = (prior + lt * pair) / self.T
        g, = torch.autograd.grad(U.sum(), xt)
        self.n_grad += xt.shape[0]
        return U.detach().numpy(), g.numpy(), prior.detach().numpy(), pair.detach().numpy()

    def pair_only(self, x):
        with torch.no_grad():
            prior, pair = self.split_t(torch.as_tensor(x, dtype=torch.float64))
        self.n_grad += len(x)
        return prior.numpy(), pair.numpy()


class ExactPrior:
    """Exact sampler of pi_0 ∝ exp(-E_prior/T): per residue i=1..L-3 the joint (theta_i, tau_i) soft-binned head times
    the theta wall; theta_{L-2} (not in the head) has only the wall term.  Grid 0.5 deg (theta) x 1 deg (tau),
    uniform jitter within a cell (the density is smooth on that scale: soft bins sigma 4/6 deg)."""

    def __init__(self, en: EN.Energy, T=1.0):
        L = en.L
        w = en.w
        self.L = L
        self.th_g = np.radians(np.arange(0.25, 180.0, 0.5))
        self.ta_g = np.radians(np.arange(-179.5, 180.0, 1.0))
        thd = torch.as_tensor(np.degrees(self.th_g)); tad = torch.as_tensor(np.degrees(self.ta_g))
        st, _ = EN.tt_soft_weights(thd, torch.zeros_like(thd), w["sig_th"], w["sig_ta"])   # (nth, 9)
        _, sa = EN.tt_soft_weights(torch.zeros_like(tad), tad, w["sig_th"], w["sig_ta"])   # (nta, 24)
        PT = en.PT.numpy()                                                                    # (L-3, 9, 24)
        wall = w["w_w"] * (np.maximum(np.degrees(self.th_g) - 170.0, 0) ** 2 + np.maximum(60.0 - np.degrees(self.th_g), 0) ** 2)
        st = st.numpy(); sa = sa.numpy()
        self.cdf = []
        for i in range(L - 3):
            p = st @ PT[i] @ sa.T                                    # (nth, nta) soft head density
            logd = (w["w_tt"] * np.log(p + 1e-6) - wall[:, None]) / T
            d = np.exp(logd - logd.max()).ravel()
            self.cdf.append(np.cumsum(d) / d.sum())
        dl = np.exp(-(wall - wall.min()) / T)
        self.cdf_last = np.cumsum(dl) / dl.sum()                     # theta_{L-2}

    def sample(self, n, rng):
        L = self.L
        th = np.empty((n, L - 2)); ta = np.empty((n, L - 3))
        nta = len(self.ta_g)
        for i in range(L - 3):
            k = np.searchsorted(self.cdf[i], rng.random(n))
            a, c = np.divmod(k, nta)
            th[:, i] = self.th_g[a] + np.radians(0.5) * (rng.random(n) - 0.5)
            ta[:, i] = self.ta_g[c] + np.radians(1.0) * (rng.random(n) - 0.5)
        k = np.searchsorted(self.cdf_last, rng.random(n))
        th[:, L - 3] = self.th_g[k] + np.radians(0.5) * (rng.random(n) - 0.5)
        return np.concatenate([np.clip(th, TH_MIN, TH_MAX), ta], 1)


def _wrap(x, L):
    x[:, L - 2:] = np.remainder(x[:, L - 2:] + math.pi, 2 * math.pi) - math.pi
    return x


def _reflect(x, p, L):
    th = x[:, :L - 2]; pth = p[:, :L - 2]
    lo = th < TH_MIN; hi = th > TH_MAX
    th[lo] = 2 * TH_MIN - th[lo]; pth[lo] = -pth[lo]
    th[hi] = 2 * TH_MAX - th[hi]; pth[hi] = -pth[hi]
    return x, p


def hmc_step(se: SplitEnergy, x, lam, eps, n_leap, rng, minv=None):
    """One HMC transition for a batch (each row its own lam, eps, diagonal inverse mass minv (B,D) or None).
    Reflecting theta walls, periodic tau.  K = 0.5 p^T M^{-1} p."""
    L = se.L
    B, D = x.shape
    if minv is None:
        minv = np.ones((B, D))
    p0 = rng.standard_normal((B, D)) / np.sqrt(minv)          # p ~ N(0, M), M = diag(1/minv)
    U0, g, pr0, pa0 = se.u_and_grad(x, lam)
    xn = x.copy(); p = p0.copy()
    e = eps[:, None]
    p -= 0.5 * e * g
    for s in range(n_leap):
        xn += e * minv * p
        xn, p = _reflect(xn, p, L)
        xn = _wrap(xn, L)
        U1, g, pr1, pa1 = se.u_and_grad(xn, lam)
        if s < n_leap - 1:
            p -= e * g
    p -= 0.5 * e * g
    H0 = U0 + 0.5 * (minv * p0 ** 2).sum(1)
    H1 = U1 + 0.5 * (minv * p ** 2).sum(1)
    acc = np.log(rng.random(B)) < (H0 - H1)
    acc &= np.isfinite(H1)
    x_out = np.where(acc[:, None], xn, x)
    pr = np.where(acc, pr1, pr0); pa = np.where(acc, pa1, pa0)
    return x_out, acc, pr, pa


def pivot_moves(se: SplitEnergy, prior: "ExactPrior", x, lam, n_moves, rng, pair_cur=None):
    """Fragment/pivot moves: pick a residue i (per row), propose (theta_i, tau_i) from the EXACT prior conditional
    (the learned per-residue head at temperature T); MH-accept with exp(-lam * dE_pair / T) (the prior factor cancels).
    Changing tau_i/theta_i rigidly rotates the downstream chain, so these are large, pivot-like moves."""
    L = se.L
    B = x.shape[0]
    if pair_cur is None:
        _, pair_cur = se.pair_only(x)
    acc_n = np.zeros(B)
    for _ in range(n_moves):
        i = rng.integers(0, L - 2, size=B)                 # theta index 0..L-3 (theta_{i+1}); tau exists for i < L-3
        prop = prior.sample(B, rng)
        xn = x.copy()
        rows = np.arange(B)
        xn[rows, i] = prop[rows, i]
        has_tau = i < L - 3
        xn[rows[has_tau], (L - 2) + i[has_tau]] = prop[rows[has_tau], (L - 2) + i[has_tau]]
        _, pair_new = se.pair_only(xn)
        logr = -lam * (pair_new - pair_cur) / se.T
        ok = np.log(rng.random(B)) < logr
        x = np.where(ok[:, None], xn, x)
        pair_cur = np.where(ok, pair_new, pair_cur)
        acc_n += ok
    return x, pair_cur, acc_n / max(n_moves, 1)


def _circ_var(x, L):
    """per-coordinate variance with tau treated circularly (1 - |mean resultant|, scaled to rad^2)."""
    v = x.var(0)
    ta = x[:, L - 2:]
    R = np.abs(np.exp(1j * ta).mean(0))
    v[L - 2:] = np.minimum(-2 * np.log(np.clip(R, 1e-6, 1.0)), v[L - 2:])
    return v


def schedule_from_rejections(lams, rej, n_new):
    """Syed et al. 2022: place rungs so that the cumulative communication barrier is equispaced."""
    lams = np.asarray(lams); rej = np.clip(np.asarray(rej), 1e-6, 1.0)
    cum = np.concatenate([[0.0], np.cumsum(rej)])           # Lambda(lam) at the rung positions
    Lam = cum[-1]
    targets = np.linspace(0.0, Lam, n_new)
    new = np.interp(targets, cum, lams)
    new[0], new[-1] = lams[0], lams[-1]
    return np.maximum.accumulate(new), float(Lam)


def run_nrpt(en: EN.Energy, T=1.0, n_rungs=16, n_scans=2000, n_leap=8, tune_rounds=4, tune_scans=200,
             seed=0, thin=5, time_budget_s=None, init=None, log=None, adapt_eps=True, mass=True, n_pivot=0):
    """Non-reversible (DEO) replica exchange along lam in [0,1]; rung 0 = exact prior, rung N-1 = posterior (lam=1).

    Returns dict with schedule, Lambda estimates, round trips, per-rung acceptance, energy traces, posterior samples,
    and evaluation counts.  Round trip = a replica index travelling rung 0 -> rung N-1 -> rung 0.
    """
    rng = np.random.default_rng(seed)
    se = SplitEnergy(en, T)
    prior = ExactPrior(en, T)
    L = en.L
    N = n_rungs
    lams = np.linspace(0.0, 1.0, N) ** 2                     # initial guess, refined by tuning
    eps = np.full(N, 0.02)
    D = 2 * L - 5
    minv = np.ones((N, D))
    x = prior.sample(N, rng) if init is None else np.asarray(init, float).copy()
    t0 = time.time()
    hist = []

    def one_scan(x, lams, eps, scan_idx, track, minv=minv):
        # local moves: exact refresh at rung 0, HMC elsewhere
        x = x.copy()
        x[0] = prior.sample(1, rng)[0]
        xs, acc, pr, pa = hmc_step(se, x[1:], lams[1:], eps[1:], n_leap, rng, minv[1:] if mass else None)
        if n_pivot:
            xs, pa, _ = pivot_moves(se, prior, xs, lams[1:], n_pivot, rng, pa)
            pr, _ = se.pair_only(xs)
        x[1:] = xs
        pr0, pa0 = se.pair_only(x[:1])
        pair = np.concatenate([pa0, pa]); pri = np.concatenate([pr0, pr])
        # DEO swaps
        par = scan_idx % 2
        swap_acc = np.full(N - 1, np.nan)
        for k in range(par, N - 1, 2):
            dl = lams[k + 1] - lams[k]
            logr = dl * (pair[k + 1] - pair[k]) / T
            a = min(1.0, math.exp(min(0.0, logr)) if logr < 0 else 1.0)
            ok = rng.random() < a
            swap_acc[k] = a
            if ok:
                x[[k, k + 1]] = x[[k + 1, k]]
                pair[[k, k + 1]] = pair[[k + 1, k]]
                pri[[k, k + 1]] = pri[[k + 1, k]]
                if track is not None:
                    track[[k, k + 1]] = track[[k + 1, k]]
        return x, np.concatenate([[1.0], acc.astype(float)]), swap_acc, pair, pri

    # ---------------- tuning rounds: step sizes (target HMC acceptance ~0.7) + schedule (equalise rejections)
    Lam_hist = []
    for r in range(tune_rounds):
        accs = np.zeros(N); rej_sum = np.zeros(N - 1); rej_cnt = np.zeros(N - 1)
        buf = []
        for s in range(tune_scans):
            x, acc, sa, _, _ = one_scan(x, lams, eps, s, None, minv)
            accs += acc
            if s >= tune_scans // 3:
                buf.append(x.copy())
            m = np.isfinite(sa)
            rej_sum[m] += 1 - sa[m]; rej_cnt[m] += 1
            if adapt_eps and s % 20 == 19:
                a = accs / 20.0
                eps[1:] *= np.exp(0.8 * (a[1:] - 0.7))
                eps = np.clip(eps, 1e-4, 0.5)
                accs[:] = 0
        rej = rej_sum / np.maximum(rej_cnt, 1)
        if mass and len(buf) > 10:
            Bf = np.stack(buf)                                   # (S, N, D)
            for k in range(1, N):
                v = _circ_var(Bf[:, k], L)
                minv[k] = np.clip(v / max(np.median(v), 1e-12), 0.05, 20.0)   # relative scales; eps absorbs the level
        lams_new, Lam = schedule_from_rejections(lams, rej, N)
        Lam_hist.append(Lam)
        if log:
            log(f"tune {r}: Lambda={Lam:.2f} max_rej={rej.max():.2f} eps[-1]={eps[-1]:.4f}")
        # map step sizes and mass matrices onto the new schedule (nearest old rung)
        near = np.abs(lams_new[:, None] - lams[None, :]).argmin(1)
        eps = np.interp(lams_new, lams, eps)
        minv = minv[near]
        lams = lams_new
        if time_budget_s and time.time() - t0 > 0.35 * time_budget_s:
            break
    n_tune_grad = se.n_grad

    # ---------------- production
    track = np.arange(N)                   # replica label at each rung
    pos = np.arange(N)                     # rung of each replica label
    last_end = np.full(N, -1)              # -1 none, 0 last visited bottom, 1 last visited top
    trips = 0; trip_scans = []
    top_since = {}
    rej_sum = np.zeros(N - 1); rej_cnt = np.zeros(N - 1)
    acc_sum = np.zeros(N)
    samples, E_top, pair_trace, rg_top, track_hist = [], [], [], [], []
    upflow_sum = np.zeros(N)
    s_done = 0
    for s in range(n_scans):
        x, acc, sa, pair, pri = one_scan(x, lams, eps, s, track, minv)
        acc_sum += acc
        m = np.isfinite(sa)
        rej_sum[m] += 1 - sa[m]; rej_cnt[m] += 1
        for rung, lab in enumerate(track):
            if rung == 0:
                if last_end[lab] == 1:
                    trips += 1
                    trip_scans.append(s - top_since.get(lab, s))
                last_end[lab] = 0
                top_since[lab] = s
            elif rung == N - 1:
                if last_end[lab] == 0:
                    last_end[lab] = 1
        E_top.append(pri[-1] + pair[-1]); pair_trace.append(pair.copy()); track_hist.append(track.copy())
        up = np.array([last_end[lab] == 0 for lab in track], float)
        upflow_sum += up
        if s % thin == 0:
            samples.append(x[-1].copy())
        s_done = s + 1
        if time_budget_s and time.time() - t0 > time_budget_s:
            break
    rej = rej_sum / np.maximum(rej_cnt, 1)
    Lam = float(rej.sum())
    return dict(L=L, T=T, n_rungs=N, n_leap=n_leap, lams=lams, eps=eps, minv_top=minv[-1], Lambda=Lam, Lambda_tune=Lam_hist,
                rej=rej, hmc_acc=acc_sum / max(s_done, 1), round_trips=trips, trip_scans=trip_scans,
                scans=s_done, grad_evals=se.n_grad, tune_grad_evals=n_tune_grad,
                E_top=np.array(E_top), pair_trace=np.array(pair_trace), samples=np.array(samples),
                track_hist=np.array(track_hist, dtype=np.int16), upflow=upflow_sum / max(s_done, 1),
                secs=time.time() - t0)
