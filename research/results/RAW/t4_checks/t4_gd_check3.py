"""T4 small check (e): STABLE fixed-step GD (eta ~ 1/lambda_max at prior draws) and clipped GD, 16 restarts,
5O37A_45 seed-0 prior draws (same x0 as census/check b).  Compares with L-BFGS endpoints from the same x0."""
import os, sys, time, json
os.environ["OMP_NUM_THREADS"] = "1"
ROOT = r"C:/Users/abena/quantum-advantage-protein-folding"
sys.path.insert(0, ROOT + "/src")
import numpy as np
from qapf.protein import energy as EN
from qapf.sampling import hrex as H
def kabsch(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B); S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A**2).sum() + (B**2).sum() - 2*S.sum(), 0) / len(A)))
crop = "5O37A_45"
z = np.load(f"{ROOT}/data/instruments/ladder/{crop}.npz"); L = len(str(z["seq"]))
en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
rng = np.random.default_rng(0); pr = H.ExactPrior(en, 1.0); x0 = pr.sample(64, rng)
R = 16; t0 = time.time()
xl, El = EN.relax(en, x0[:R], iters=200); Cl = en.coords(xl)
print(f"L-BFGS (batched) on first {R}: E min {El.min():.1f} median {np.median(El):.1f}", flush=True)
variants = [("GD eta=1e-5", 1e-5, None), ("GD eta=2e-5", 2e-5, None), ("clipped GD eta=1e-3 clip=0.02rad", 1e-3, 0.02)]
for name, eta, clip in variants:
    x = x0[:R].copy(); E, G = en(x); Ep = E.copy(); nup = 0; out = []
    for k in range(1, 10001):
        dx = eta * G
        if clip is not None: dx = np.clip(dx, -clip, clip)
        x = x - dx; E, G = en(x)
        nup += int((E > Ep + 1e-9).sum()); Ep = E
        if k in (500, 2000, 10000):
            C = en.coords(x)
            same = np.mean([kabsch(C[i], Cl[i]) < 2.0 for i in range(R)])
            dE = E - El
            out.append(f"K={k}: same-basin-as-LBFGS {same:.2f}, med(E-E_LBFGS) {np.median(dE):.1f}, "
                       f"frac within 5 nats {np.mean(dE < 5):.2f}, frac lower {np.mean(dE < -1):.2f}")
    print(f"[e] {name}: " + "; ".join(out) + f" | energy increases {nup}/{R*10000} ({time.time()-t0:.0f}s)", flush=True)
