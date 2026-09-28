"""T2 3-rotor test: does a pair cluster expansion of the dressed tunnelling splitting reproduce
the exact 3-rotor value? Lanczos on FFT-applied Hamiltonian per symmetry sector. Checkpointed."""
import json, os, sys, time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh
sys.path.insert(0, os.path.dirname(__file__))
from rotor import load_methyls, v3_grid, single_sector, two_rotor_sector_energies, atomic_json
from run_pairs import hgrid
import run_pairs
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_triangle.json")
M, G, V3 = 24, 96, 30.0
run_pairs.G = G

def coupling(ma, mb, coul=False):
    return run_pairs.coupling(ma, mb, coul)[0]

def sector_idx(s):
    ms = np.array([m for m in range(-M, M + 1) if m % 3 == s % 3]); return ms, ms % G

def lowest3(rot3, Vtot, sig):
    (m1, i1), (m2, i2), (m3, i3) = [sector_idx(s) for s in sig]
    B = [r["B"] for r in rot3]
    kin = (B[0] * m1[:, None, None] ** 2 + B[1] * m2[None, :, None] ** 2 + B[2] * m3[None, None, :] ** 2).ravel()
    shp = (len(m1), len(m2), len(m3))
    def mv(x):
        c = x.reshape(shp)
        full = np.zeros((G, G, G), complex)
        full[np.ix_(i1, i2, i3)] = c
        psi = np.fft.ifftn(full) * G ** 3
        out = np.fft.fftn(psi * Vtot) / G ** 3
        return kin * x + out[np.ix_(i1, i2, i3)].ravel()
    n = int(np.prod(shp))
    op = LinearOperator((n, n), matvec=mv, dtype=complex)
    w = eigsh(op, k=1, which="SA", tol=1e-13, maxiter=5000, return_eigenvectors=False)
    return float(w[0].real), n

def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    ms = {m["id"]: m for m in load_methyls()}
    tris = [("ILE61:CG2", "ILE61:CD1", "LEU67:CD2"), ("ILE36:CG2", "ILE36:CD1", "LEU71:CD1")]
    vg = v3_grid(V3, G)
    # convergence of bare splitting in M
    res["_bare_M_check"] = {str(Mx): (single_sector(0.655, Mx, 1, v3_grid(V3, 360))[0][0] - single_sector(0.655, Mx, 0, v3_grid(V3, 360))[0][0]) * 1e3 for Mx in (18, 24, 45)}
    for tri in tris:
        key = "|".join(tri)
        if key in res: continue
        t0 = time.time()
        R = [ms[x] for x in tri]
        V = {(a, b): coupling(R[a], R[b]) for a, b in ((0, 1), (0, 2), (1, 2))}
        ph = np.arange(G)
        Vtot = (vg[:, None, None] + vg[None, :, None] + vg[None, None, :]
                + V[(0, 1)][:, :, None] + V[(0, 2)][:, None, :] + V[(1, 2)][None, :, :])
        E3 = {}
        for sig in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)):
            E3[sig], n = lowest3(R, Vtot, sig)
        # pair-level dressed splittings (exact 2-rotor) and bare
        bare = [(single_sector(r["B"], M, 1, vg)[0][0] - single_sector(r["B"], M, 0, vg)[0][0]) for r in R]
        pairD = {}
        for (a, b), Vab in V.items():
            Vhat = np.fft.fft2(Vab) / G ** 2
            E = two_rotor_sector_energies(V3, V3, R[a]["B"], R[b]["B"], Vhat, M, [(0, 0), (1, 0), (0, 1)])
            pairD[(a, b)] = (E[(1, 0)] - E[(0, 0)], E[(0, 1)] - E[(0, 0)])  # dressed splitting of a, of b
        out = {"sector_dim": n, "secs": None, "rotors": {}}
        for i in range(3):
            ex = E3[tuple(1 if j == i else 0 for j in range(3))] - E3[(0, 0, 0)]
            # dressed-by-partner splittings for rotor i
            dress = []
            for (a, b), (da, db) in pairD.items():
                if a == i: dress.append(da)
                if b == i: dress.append(db)
            add = bare[i] + sum(d - bare[i] for d in dress)
            logadd = bare[i] * np.prod([d / bare[i] for d in dress])
            out["rotors"][tri[i]] = {"Delta_bare_ueV": bare[i] * 1e3, "Delta_pairs_ueV": [d * 1e3 for d in dress],
                                     "Delta_exact3_ueV": ex * 1e3, "pred_additive_ueV": add * 1e3,
                                     "pred_multiplicative_ueV": logadd * 1e3,
                                     "rel_err_additive": abs(add - ex) / abs(ex), "rel_err_multiplicative": abs(logadd - ex) / abs(ex)}
        out["secs"] = time.time() - t0
        res[key] = out
        atomic_json(OUT, res)
        print(key, json.dumps(out, indent=1), flush=True)

if __name__ == "__main__":
    main()
