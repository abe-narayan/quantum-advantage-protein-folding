"""QM-11 adversary check: adaptive-tempering SMC from the exact product head prior pi_0,T to the learned posterior
pi_1,T (lambda path of qapf.sampling.hrex).  Measures log Z1/Z0, KL(pi_1||pi_0) = -E_1[U] - log Z1/Z0 (a lower bound on
Phi = log(w_max / E_q w), which sets the amplitude-amplification cost e^{Phi/2}), a D_inf lower bound from the lowest
U seen, and the SMC cost (stages, pair-energy evaluations).  DEP only (no native used).  Self-throttled: single thread,
waits for machine CPU < 85% before starting, pauses while CPU > 95%."""
import sys, os, time, json, math
import numpy as np
import psutil
import torch
torch.set_num_threads(1)
ROOT = "C:/Users/abena/quantum-advantage-protein-folding"
sys.path.insert(0, ROOT + "/src")
from qapf.protein import energy as EN
from qapf.sampling import hrex as H


def gate(start=False):
    if start:
        t0 = time.time()
        while psutil.cpu_percent(interval=10) > 85 and time.time() - t0 < 1800:
            pass
    else:
        while psutil.cpu_percent(interval=2) > 95:
            time.sleep(10)


def run(crop, T, N=128, cess=0.5, seed=0, moves_per_stage=None):
    z = np.load(f"{ROOT}/data/instruments/ladder/{crop}.npz")
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    se = H.SplitEnergy(en, T)
    pr = H.ExactPrior(en, T)
    rng = np.random.default_rng(seed)
    x = pr.sample(N, rng)
    _, E = se.pair_only(x)
    U = E / T
    lam, logZ, stages = 0.0, 0.0, 0
    moves = moves_per_stage or L
    lam_hist = [0.0]
    t0 = time.time()
    minU1 = np.inf
    while lam < 1.0:
        # bisection for next lambda with ESS of incremental weights = cess*N
        def ess(dl):
            lw = -dl * U; lw -= lw.max(); w = np.exp(lw)
            return w.sum() ** 2 / (w ** 2).sum()
        lo, hi = 0.0, 1.0 - lam
        if ess(hi) >= cess * N:
            dl = hi
        else:
            for _ in range(60):
                mid = 0.5 * (lo + hi)
                if ess(mid) >= cess * N: lo = mid
                else: hi = mid
            dl = max(lo, 1e-12)
        lw = -dl * U
        m = lw.max()
        logZ += m + math.log(np.exp(lw - m).mean())
        w = np.exp(lw - m); w /= w.sum()
        idx = rng.choice(N, N, p=w)      # multinomial resampling
        x = x[idx]; E = E[idx]
        lam = min(1.0, lam + dl); stages += 1; lam_hist.append(lam)
        x, E, acc = H.pivot_moves(se, pr, x, np.full(N, lam), moves, rng, E)
        U = E / T
        if stages % 10 == 0:
            gate()
    minU1 = U.min()
    E1U = U.mean()
    KL = -E1U - logZ
    return dict(crop=crop, L=L, T=T, N=N, stages=stages, logZ=logZ, E1U=float(E1U), KL=float(KL),
                Dinf_lb=float(-minU1 - logZ), KL_per_res=float(KL / L), pair_evals=int(se.n_grad),
                uniq_final=int(len(np.unique(x[:, 0]))), secs=time.time() - t0)


if __name__ == "__main__":
    out = sys.argv[1]
    jobs = [(c, T) for c in sys.argv[2].split(",") for T in [float(t) for t in sys.argv[3].split(",")]]
    gate(start=True)
    for c, T in jobs:
        r = run(c, T)
        print(json.dumps(r), flush=True)
        with open(out, "a") as f:
            f.write(json.dumps(r) + "\n")
