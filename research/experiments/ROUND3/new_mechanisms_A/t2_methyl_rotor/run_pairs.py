"""T2 pair test: exact 2-rotor symmetry-sector energies vs single-rotor/mean-field (classical) models
for the most strongly coupled methyl pairs of 1UBQ. Checkpointed per (pair, V3, variant)."""
import json, math, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from rotor import (load_methyls, rot, v3_grid, single_sector, density_on_grid, two_rotor_sector_energies,
                   RMIN_HH, EPS_HH, COUL_MEV_A, atomic_json)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_pairs.json")
G, M = 144, 45
NPAIRS = 16

def hgrid(m, G):
    phis = 2 * np.pi * np.arange(G) / G
    return np.array([m["C"] + rot(m["u"], p, m["H"] - m["C"]) for p in phis])  # (G,3,3)

def coupling(m1, m2, coul):
    P1, P2 = hgrid(m1, G), hgrid(m2, G)
    d = np.linalg.norm(P1[:, None, :, None, :] - P2[None, :, None, :, :], axis=-1)  # G,G,3,3
    x = (RMIN_HH / d) ** 6
    e = EPS_HH * (x * x - 2 * x)
    if coul:
        e = e + COUL_MEV_A * 0.06 ** 2 / d
    return e.sum((2, 3)), float(d.min())

def main():
    ms = load_methyls()
    pairs = []
    for i in range(len(ms)):
        for j in range(i + 1, len(ms)):
            d = np.linalg.norm(ms[i]["H"][:, None] - ms[j]["H"][None], axis=-1).min()
            if d < 3.5:
                pairs.append((float(d), i, j))
    pairs.sort()
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    res["_meta"] = {"n_methyls": len(ms), "n_pairs_HH_lt_3.5A": len(pairs), "G": G, "M": M,
                    "closest_pairs": [(ms[i]["id"], ms[j]["id"], d) for d, i, j in pairs[:NPAIRS]]}
    t0 = time.time()
    for d0, i, j in pairs[:NPAIRS]:
        m1, m2 = ms[i], ms[j]
        for coul in (False, True):
            V12, dmin = coupling(m1, m2, coul)
            Vhat = np.fft.fft2(V12) / G ** 2
            # symmetry check: only (3a,3b) Fourier components
            mask = np.zeros((G, G), bool); idx = np.arange(G)
            mask[np.ix_(idx % 3 == 0, idx % 3 == 0)] = True
            leak = float(np.abs(Vhat[~mask]).max())
            coup_amp = float(np.abs(Vhat[mask][1:]).max())  # largest nonconstant component
            # nonseparable part: components with p!=0 and q!=0
            ns = Vhat.copy(); ns[0, :] = 0; ns[:, 0] = 0
            ns_amp = float(np.abs(ns).max())
            for V3 in (30.0, 60.0, 100.0):
                key = f"{m1['id']}|{m2['id']}|coul{int(coul)}|V3_{V3:g}"
                if key in res:
                    continue
                E = two_rotor_sector_energies(V3, V3, m1["B"], m2["B"], Vhat, M,
                                              [(0, 0), (1, 0), (0, 1), (1, 1), (1, 2)])
                # bare single rotors
                vg = v3_grid(V3, G)
                d1_bare = single_sector(m1["B"], M, 1, vg)[0][0] - single_sector(m1["B"], M, 0, vg)[0][0]
                # Hartree mean field (A-state densities), 4 iterations
                rho2 = np.ones(G) / G
                for _ in range(4):
                    w1_0, v1_0, ms1 = single_sector(m1["B"], M, 0, vg + V12 @ rho2)
                    rho1 = density_on_grid(v1_0[:, 0], ms1, G)
                    w2_0, v2_0, ms2 = single_sector(m2["B"], M, 0, vg + V12.T @ rho1)
                    rho2 = density_on_grid(v2_0[:, 0], ms2, G)
                vmf1 = vg + V12 @ rho2
                d1_mf = single_sector(m1["B"], M, 1, vmf1)[0][0] - single_sector(m1["B"], M, 0, vmf1)[0][0]
                d1_ex0 = E[(1, 0)] - E[(0, 0)]
                d1_ex1 = E[(1, 1)] - E[(0, 1)]
                d1_ex2 = E[(1, 2)] - E[(0, 1)]  # E(0,2)=E(0,1) by conjugation
                J1 = d1_ex1 - d1_ex0
                J2 = d1_ex2 - d1_ex0
                res[key] = {"dmin_HH": dmin, "V3": V3, "coul": coul, "sym_leak": leak,
                            "max_coupling_fourier_meV": coup_amp, "max_nonseparable_fourier_meV": ns_amp,
                            "Delta_bare_ueV": d1_bare * 1e3, "Delta_exact_s2=0_ueV": d1_ex0 * 1e3,
                            "Delta_mf_ueV": d1_mf * 1e3, "J11_ueV": J1 * 1e3, "J12_ueV": J2 * 1e3,
                            "rel_J": max(abs(J1), abs(J2)) / abs(d1_ex0),
                            "rel_mf_err": abs(d1_ex0 - d1_mf) / abs(d1_ex0),
                            "rel_env_shift": abs(d1_ex0 - d1_bare) / abs(d1_bare)}
                atomic_json(OUT, res)
                r = res[key]
                print(f"{key} dmin={dmin:.2f} ns={ns_amp:.3f}meV Dbare={r['Delta_bare_ueV']:.4g} Dex={r['Delta_exact_s2=0_ueV']:.4g} "
                      f"Dmf={r['Delta_mf_ueV']:.4g} J={J1*1e3:.2e}/{J2*1e3:.2e} ueV relJ={r['rel_J']:.1e} relMF={r['rel_mf_err']:.1e} [{time.time()-t0:.0f}s]", flush=True)

if __name__ == "__main__":
    main()
