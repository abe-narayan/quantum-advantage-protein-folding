"""T4 small check (b,c) on 5O37A_45 (dev crop, T=1, seed 0 -> same 64 prior draws as the g1 mode census):
(b) per-restart L-BFGS gradient-evaluation counts (B=1 runs; mean vs max -> coherent worst-case penalty);
(c) fixed-step gradient descent (the reversible-friendly map) for K steps: does it reach the L-BFGS basin?
    p_hit of the best L-BFGS mode under GD_K vs under L-BFGS.  Native used nowhere (no ORACLE)."""
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

crop = sys.argv[1] if len(sys.argv) > 1 else "5O37A_45"
R = int(sys.argv[2]) if len(sys.argv) > 2 else 64
z = np.load(f"{ROOT}/data/instruments/ladder/{crop}.npz")
L = len(str(z["seq"]))
en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
rng = np.random.default_rng(0)
pr = H.ExactPrior(en, 1.0)
x0 = pr.sample(R, rng)
t0 = time.time()
# (b) L-BFGS one restart at a time, count gradient evaluations
ng, xl, El = [], [], []
for r in range(R):
    n0 = en.n_grad
    x, E, it = EN.lbfgs(en, x0[r:r+1], iters=200)
    ng.append(en.n_grad - n0); xl.append(x[0]); El.append(float(E[0]))
xl = np.array(xl); El = np.array(El); ng = np.array(ng)
tb = time.time() - t0
Cl = en.coords(xl)
best = int(np.argmin(El))
in_best_l = np.array([kabsch(Cl[i], Cl[best]) < 2.0 for i in range(R)])
print(f"[b] {crop} L={L} R={R}: L-BFGS grad evals per restart mean {ng.mean():.0f} median {np.median(ng):.0f} "
      f"p90 {np.percentile(ng,90):.0f} max {ng.max()}  | p_hit(best mode, L-BFGS) = {in_best_l.mean():.3f}  E_best={El.min():.1f}  ({tb:.0f}s)")
# (c) fixed-step GD
res = {}
for eta in (3e-4, 1e-3, 3e-3):
    x = x0.copy()
    E0, G = en(x)
    ck = {}
    Eprev = E0.copy(); nup = 0
    for k in range(1, 5001):
        x = x - eta * G
        E, G = en(x)
        nup += int((E > Eprev + 1e-9).sum()); Eprev = E
        if k in (200, 1000, 5000):
            C = en.coords(x)
            same = np.array([kabsch(C[i], Cl[i]) < 2.0 for i in range(R)])
            hit = np.array([kabsch(C[i], Cl[best]) < 2.0 for i in range(R)])
            dE = E - El
            ck[k] = dict(frac_same_basin_as_lbfgs=float(same.mean()), p_hit_best=float(hit.mean()),
                         med_E_minus_lbfgs=float(np.median(dE)), min_E=float(E.min()), finite=bool(np.isfinite(E).all()))
    res[eta] = dict(ck=ck, n_energy_increases=nup)
    print(f"[c] eta={eta:g}: " + "; ".join(f"K={k}: same-basin {v['frac_same_basin_as_lbfgs']:.2f}, p_hit {v['p_hit_best']:.3f}, "
          f"med(E_GD-E_LBFGS) {v['med_E_minus_lbfgs']:.1f}, minE {v['min_E']:.1f}" for k, v in ck.items())
          + f" | energy increases {nup}")
print(f"total {time.time()-t0:.0f}s")
json.dump(dict(crop=crop, L=L, R=R, lbfgs_grad_evals=ng.tolist(), lbfgs_E=El.tolist(), p_hit_lbfgs=float(in_best_l.mean()),
               gd={str(k): v for k, v in res.items()}),
          open(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"t4_gd_{crop}_R{R}.json"), "w"))
