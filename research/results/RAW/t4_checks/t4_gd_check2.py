"""T4 small check (d): Hessian spectrum at L-BFGS endpoints (stable fixed step eta < 2/lambda_max) and fixed-step GD
with small eta for 16 restarts (5O37A_45, seed 0 prior draws, same as census).  Native used nowhere."""
import os, sys, time, json
os.environ["OMP_NUM_THREADS"] = "1"
ROOT = r"C:/Users/abena/quantum-advantage-protein-folding"
SP = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT + "/src")
import numpy as np, torch
from qapf.protein import energy as EN
from qapf.sampling import hrex as H

def kabsch(A, B):
    A = A - A.mean(0); B = B - B.mean(0)
    U, S, Vt = np.linalg.svd(A.T @ B); S[-1] *= np.sign(np.linalg.det(U @ Vt))
    return float(np.sqrt(max((A**2).sum() + (B**2).sum() - 2*S.sum(), 0) / len(A)))

crop = "5O37A_45"
prev = json.load(open(os.path.join(SP, f"t4_gd_{crop}_R64.json")))
z = np.load(f"{ROOT}/data/instruments/ladder/{crop}.npz")
L = len(str(z["seq"]))
en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
rng = np.random.default_rng(0)
pr = H.ExactPrior(en, 1.0)
x0 = pr.sample(64, rng)
t0 = time.time()
# L-BFGS endpoints again (batched, 16 restarts) -> Hessian spectra
R = 16
xl, El = EN.relax(en, x0[:R], iters=200)
Cl = en.coords(xl)
Eall = np.array(prev["lbfgs_E"]); 
lmax, lminpos, nneg = [], [], []
for i in range(R):
    xt = torch.as_tensor(xl[i:i+1], dtype=torch.float64)
    Hm = torch.autograd.functional.hessian(lambda z_: en.energy_t(z_)[0], xt)[0, :, 0, :].numpy()
    w = np.linalg.eigvalsh(0.5 * (Hm + Hm.T))
    lmax.append(w.max()); pos = w[w > 1e-3]; lminpos.append(pos.min() if len(pos) else np.nan); nneg.append(int((w <= 1e-3).sum()))
lmax = np.array(lmax); lminpos = np.array(lminpos)
print(f"[d] Hessian at L-BFGS endpoints (R={R}, D={2*L-5}): lambda_max median {np.median(lmax):.3g} max {lmax.max():.3g}; "
      f"lambda_min(>1e-3) median {np.nanmedian(lminpos):.3g}; kappa median {np.nanmedian(lmax/lminpos):.3g}; #(<=1e-3) median {np.median(nneg)}")
# prior-draw (start point) curvature: power iteration on Hessian-vector products at x0
lm0 = []
for i in range(4):
    xt = torch.as_tensor(x0[i:i+1], dtype=torch.float64)
    Hm = torch.autograd.functional.hessian(lambda z_: en.energy_t(z_)[0], xt)[0, :, 0, :].numpy()
    lm0.append(np.abs(np.linalg.eigvalsh(0.5 * (Hm + Hm.T))).max())
print(f"[d] |lambda|_max at prior draws (4): {np.round(lm0, 1).tolist()}")
Ebest = min(Eall)
best_i = int(np.argmin(Eall))
# best-mode representative coordinates from the full 64-run L-BFGS (recompute that one)
xb, _ = EN.relax(en, x0[best_i:best_i+1], iters=200); Cb = en.coords(xb)[0]
for eta in (1.0 / np.median(lmax), 0.3 / np.median(lmax)):
    x = x0[:R].copy(); E, G = en(x); Ep = E.copy(); nup = 0
    out = []
    for k in range(1, 20001):
        x = x - eta * G
        E, G = en(x)
        nup += int((E > Ep + 1e-9).sum()); Ep = E
        if k in (1000, 5000, 20000):
            C = en.coords(x)
            same = np.mean([kabsch(C[i], Cl[i]) < 2.0 for i in range(R)])
            hit = np.mean([kabsch(C[i], Cb) < 2.0 for i in range(R)])
            gn = np.linalg.norm(G, axis=1)
            out.append(f"K={k}: same-basin {same:.2f}, hit-best {hit:.2f}, med(E-E_lbfgs) {np.median(E - El):.1f}, med|g| {np.median(gn):.2g}")
    print(f"[d] GD eta={eta:.3g}: " + "; ".join(out) + f" | energy increases {nup}  ({time.time()-t0:.0f}s)", flush=True)
