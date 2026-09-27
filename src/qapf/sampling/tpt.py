"""Temperature replica exchange (non-reversible DEO swaps) at lam = 1 for the learned energy: pi_T ∝ exp(-E(x)/T).

Purpose (QM-04 / T2 D1-D2): detect first-order (cooperative) character of the learned-energy "folding transition"
along TEMPERATURE: energy histograms per rung, heat capacity C(T) = Var(E)/T^2, bimodality at the C peak, and the
Lee-Kosterlitz barrier dF = ln(P_peak / P_valley) of the reweighted energy histogram at the equal-height temperature.
Local moves: HMC (diagonal mass adaptation) + prior-proposal pivot moves (as qapf.sampling.hrex).  The top rung T_max
is high enough that the chain is prior-dominated (mixes quickly).
"""
from __future__ import annotations

import math
import time

import numpy as np

from qapf.protein import energy as EN
from qapf.sampling import hrex as H


class TempEnergy:
    """U = E(x)/T per row (E = full A80 energy), with grads; wraps SplitEnergy (lam = 1)."""

    def __init__(self, en):
        self.se = H.SplitEnergy(en, 1.0)
        self.L = en.L
        self.T = 1.0

    @property
    def n_grad(self):
        return self.se.n_grad

    def u_and_grad(self, x, invT):
        U, g, pr, pa = self.se.u_and_grad(x, np.ones(len(x)))      # E = prior + pair at T=1
        it = np.asarray(invT)
        return U * it, g * it[:, None], pr, pa

    def pair_only(self, x):
        return self.se.pair_only(x)


def run_tpt(en, Ts, n_scans=2000, n_leap=8, n_pivot=4, tune_scans=300, seed=0, thin=2, time_budget_s=None, log=None):
    rng = np.random.default_rng(seed)
    te = TempEnergy(en)
    L = en.L
    N = len(Ts)
    Ts = np.asarray(Ts, float); invT = 1.0 / Ts
    prior = H.ExactPrior(en, float(Ts[-1]))                         # used for pivot proposals and init
    x = prior.sample(N, rng)
    D = 2 * L - 5
    eps = np.full(N, 0.01); minv = np.ones((N, D))
    t0 = time.time()

    def scan(x, s, track=None):
        # HMC on all rungs (each at its own temperature): reuse hrex.hmc_step through a lam-vector trick:
        # U_T(x) = E(x)/T  <=>  SplitEnergy with T=1 and lam=1 then scale; implement directly.
        B = N
        p0 = rng.standard_normal((B, D)) / np.sqrt(minv)
        U0, g, pr0, pa0 = te.u_and_grad(x, invT)
        xn = x.copy(); p = p0.copy(); e = eps[:, None]
        p -= 0.5 * e * g
        for k in range(n_leap):
            xn += e * minv * p
            xn, p = H._reflect(xn, p, L)
            xn = H._wrap(xn, L)
            U1, g, pr1, pa1 = te.u_and_grad(xn, invT)
            if k < n_leap - 1:
                p -= e * g
        p -= 0.5 * e * g
        H0 = U0 + 0.5 * (minv * p0 ** 2).sum(1); H1 = U1 + 0.5 * (minv * p ** 2).sum(1)
        acc = (np.log(rng.random(B)) < (H0 - H1)) & np.isfinite(H1)
        x = np.where(acc[:, None], xn, x)
        Etot = np.where(acc, pr1 + pa1, pr0 + pa0)
        # pivot moves: propose (theta_i,tau_i) from the prior head at T_max; MH with full target ratio incl. proposal
        for _ in range(n_pivot):
            i = rng.integers(0, L - 2, size=B)
            prop = prior.sample(B, rng)
            xp = x.copy(); rows = np.arange(B)
            xp[rows, i] = prop[rows, i]
            ht = i < L - 3
            xp[rows[ht], (L - 2) + i[ht]] = prop[rows[ht], (L - 2) + i[ht]]
            pr_old, pa_old = te.pair_only(x); pr_new, pa_new = te.pair_only(xp)
            # proposal q ∝ exp(-E_prior_i / T_max): log q(new)-log q(old) = -(pr_new - pr_old)/T_max (only residue i changes)
            logr = -(pr_new + pa_new - pr_old - pa_old) * invT + (pr_new - pr_old) / Ts[-1]
            ok = np.log(rng.random(B)) < logr
            x = np.where(ok[:, None], xp, x)
            Etot = np.where(ok, pr_new + pa_new, pr_old + pa_old)
        # DEO swaps in temperature
        par = s % 2
        sw = np.full(N - 1, np.nan)
        for k in range(par, N - 1, 2):
            logr = (invT[k] - invT[k + 1]) * (Etot[k] - Etot[k + 1])
            a = 1.0 if logr >= 0 else math.exp(logr)
            sw[k] = a
            if rng.random() < a:
                x[[k, k + 1]] = x[[k + 1, k]]; Etot[[k, k + 1]] = Etot[[k + 1, k]]
                if track is not None:
                    track[[k, k + 1]] = track[[k + 1, k]]
        return x, acc.astype(float), sw, Etot

    # tuning: step sizes + mass
    buf = []
    accs = np.zeros(N)
    for s in range(tune_scans):
        x, acc, sw, E = scan(x, s)
        accs += acc
        if s >= tune_scans // 2:
            buf.append(x.copy())
        if s % 20 == 19:
            a = accs / 20.0
            eps *= np.exp(0.8 * (a - 0.7)); eps = np.clip(eps, 1e-4, 0.5); accs[:] = 0
    if buf:
        Bf = np.stack(buf)
        for k in range(N):
            v = H._circ_var(Bf[:, k], L)
            minv[k] = np.clip(v / max(np.median(v), 1e-12), 0.05, 20.0)
    track = np.arange(N); last_end = np.full(N, -1); trips = 0
    Ehist, swaps, samples_low = [], [], []
    rej_sum = np.zeros(N - 1); rej_cnt = np.zeros(N - 1)
    for s in range(n_scans):
        x, acc, sw, E = scan(x, s, track)
        m = np.isfinite(sw); rej_sum[m] += 1 - sw[m]; rej_cnt[m] += 1
        for rung, lab in enumerate(track):
            if rung == 0:                           # coldest rung (target)
                if last_end[lab] == 1:
                    trips += 1                      # cold -> hot -> cold round trip completed
                last_end[lab] = 0
            elif rung == N - 1 and last_end[lab] == 0:
                last_end[lab] = 1
        if s % thin == 0:
            Ehist.append(E.copy()); samples_low.append(x[0].copy())
        if time_budget_s and time.time() - t0 > time_budget_s:
            break
    Ehist = np.array(Ehist)
    return dict(L=L, Ts=Ts, eps=eps, rej=rej_sum / np.maximum(rej_cnt, 1), trips=trips, scans=s + 1,
                E=Ehist, samples_low=np.array(samples_low), grad_evals=te.n_grad, secs=time.time() - t0)
