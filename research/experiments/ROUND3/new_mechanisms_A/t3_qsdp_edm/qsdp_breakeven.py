"""T3: quantum SDP solvers (van Apeldoorn & Gilyen, ICALP 2019, arXiv:1804.05058: O~((sqrt(m)+sqrt(n) g) s g^4),
g = R r / eps) vs classical Burer-Monteiro (rank-3) EDM completion from native-free ESM expected distances.
DEP inputs: `expected`, `sd` (esmprior_v1). ORACLE: CA RMSD to native (evaluation only)."""
import json, math, os, sys, time
import numpy as np
from scipy.optimize import minimize
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5))
LADDER = os.path.join(ROOT, "data", "instruments", "ladder")
HERE = os.path.dirname(os.path.abspath(__file__))
CHAINS = ["2AB0A", "3BHLA", "3GAHA", "3M3PA", "3S0QA", "3TE4A", "3W42A", "4LPQA"]

def kabsch_rmsd(X, Y):
    X = X - X.mean(0); Y = Y - Y.mean(0)
    U, S, Vt = np.linalg.svd(X.T @ Y); d = np.sign(np.linalg.det(U @ Vt))
    S[-1] *= d
    return math.sqrt(max((X ** 2).sum() + (Y ** 2).sum() - 2 * S.sum(), 0) / len(X))

def solve_bm(D, Wt, L, rng, iters=3000):
    iu, ju = np.nonzero(np.triu(Wt > 0, 1)); d2 = D[iu, ju] ** 2; w = Wt[iu, ju]
    def f(x):
        X = x.reshape(L, 3); diff = X[iu] - X[ju]; r = (diff ** 2).sum(1) - d2
        g = np.zeros_like(X); c = (4 * w * r)[:, None] * diff
        np.add.at(g, iu, c); np.add.at(g, ju, -c)
        return float((w * r * r).sum()), g.ravel()
    best = None
    for s in range(4):
        x0 = rng.normal(scale=10, size=3 * L)
        o = minimize(f, x0, jac=True, method="L-BFGS-B", options={"maxiter": iters})
        if best is None or o.fun < best.fun: best = o
    X = best.x.reshape(L, 3)
    rel = math.sqrt(best.fun / (w * d2 * d2).sum())
    return X, rel, len(iu)

def main():
    rng = np.random.default_rng(0)
    rows = []
    for L in (30, 60, 100, 150):
        for ch in CHAINS:
            z = np.load(os.path.join(LADDER, f"{ch}_{L}.npz"), allow_pickle=True)
            E, SD, ca = z["expected"].astype(float), z["sd"].astype(float), z["ca"]
            conf = (SD < 2.0)
            ii, jj = np.meshgrid(np.arange(L), np.arange(L), indexing="ij")
            seq = np.abs(ii - jj) == 1
            D = np.where(seq, 3.8, E); Wt = np.where(seq, 10.0, np.where(conf & (np.abs(ii - jj) >= 2), 1.0 / np.maximum(SD, 0.3) ** 2, 0.0))
            t = time.process_time()
            X, rel, m = solve_bm(D, Wt, L, rng)
            cpu = time.process_time() - t
            Xc = X - X.mean(0)
            R = float((Xc ** 2).sum())  # trace of Gram = sum |x_i|^2
            rg = math.sqrt(R / L)
            # precision needed: restraint d^2 error <= 2*d*dd with d = 8 A, dd = 1 A -> 16 A^2 ; normalised A_j/2, rho = G/R
            eps = 16.0 / (2 * R)
            gamma = 1.0 / eps  # r >= 1 (quantum-favourable), R absorbed by normalisation rho = G/R
            s = 2
            q_queries = (math.sqrt(m) + math.sqrt(L) * gamma) * s * gamma ** 4
            rows.append({"chain": ch, "L": L, "m_restraints": int(m), "classical_cpu_s": cpu, "rel_residual": rel,
                         "rmsd_oracle_A": kabsch_rmsd(X, ca), "trace_R_A2": R, "Rg_A": rg, "eps_normalised": eps,
                         "gamma": gamma, "quantum_queries_lower_bound": q_queries,
                         "quantum_time_s_at_1us_per_query": q_queries * 1e-6})
            print(ch, L, f"m={m} cpu={cpu:.2f}s rel={rel:.3f} rmsd(ORACLE)={rows[-1]['rmsd_oracle_A']:.1f}A gamma={gamma:.2e} Qq={q_queries:.2e} Tq={q_queries*1e-6/3.15e7:.2e} yr", flush=True)
    out = {"rows": rows, "note": "quantum count = polylogs and all constants set to 1, r=1, oracle cost 1 query = 1 us (quantum-favourable); classical = process CPU seconds, 4 random starts."}
    # scaling fits
    Ls = np.array([r["L"] for r in rows], float)
    out["fit_logQ_vs_logL"] = np.polyfit(np.log(Ls), np.log([r["quantum_queries_lower_bound"] for r in rows]), 1).tolist()
    out["fit_logCPU_vs_logL"] = np.polyfit(np.log(Ls), np.log([r["classical_cpu_s"] for r in rows]), 1).tolist()
    json.dump(out, open(os.path.join(HERE, "qsdp_breakeven.json"), "w"), indent=1)
    print("fit quantum exponent", out["fit_logQ_vs_logL"][0], "classical exponent", out["fit_logCPU_vs_logL"][0])

if __name__ == "__main__":
    main()
