"""R1 theory_hardness, step A: proton density and dipolar-coupling statistics of the NMR instrument structures.

Inputs : data/instruments/nmr/{1UBQ,1PGA}_H.pdb (OpenMM-protonated; same files as scripts/nmr_gate.py).
Outputs: research/experiments/ADVERSARIAL/R1_theory_hardness/density_couplings.json

Quantities (all DERIVED from the coordinates):
  * global 1H density: n_H / V_hull (convex hull of all atoms) and n_H / V_psv (partial specific volume 0.73 cm^3/g);
  * local 1H density around buried protons (distance to the hull >= 6 A): count within R / (4/3 pi R^3);
  * N(R): mean number of protons within radius R of a buried proton (converts a front radius into a spin count);
  * local dipolar frequency omega_loc,a = sqrt(sum_j d_aj^2) (rad/s), orientation-averaged (<P2^2> = 1/5) and for the
    fixed field direction used by the C1/C2 runs (random_b0(1000), orient 0);
  * the same for the amide-only (perdeuterated) network.
Single-threaded, < 5 s.
"""
from __future__ import annotations

import json
import math
import os
import sys

import numpy as np
from scipy.spatial import ConvexHull

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

MASS = {"H": 1.008, "C": 12.011, "N": 14.007, "O": 15.999, "S": 32.06}


def read_all(pdb):
    el, xyz = [], []
    with open(pdb) as f:
        for line in f:
            if line.startswith("ENDMDL"):
                break
            if not line.startswith(("ATOM", "HETATM")):
                continue
            e = line[76:78].strip() or line[12:16].strip()[0]
            el.append(e)
            xyz.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return np.array(el), np.array(xyz, float)


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def depth_to_hull(hull, pts):
    # hull.equations: n.x + c <= 0 inside; depth = min over facets of -(n.x + c)
    eq = hull.equations
    return np.min(-(pts @ eq[:, :3].T + eq[:, 3]), axis=1)


def omega_loc(X, b0=None):
    """per-proton sqrt(sum_j d_aj^2) in rad/s; b0=None -> isotropic average (<P2^2> = 1/5)."""
    n = len(X)
    out = np.zeros(n)
    for a in range(n):
        v = np.delete(X, a, axis=0) - X[a]
        r = np.linalg.norm(v, axis=1)
        if b0 is None:
            d2 = (SP.D1A / r ** 3) ** 2 / 5.0
        else:
            c = v @ b0 / r
            d2 = (SP.D1A / r ** 3 * (3 * c ** 2 - 1) / 2) ** 2
        out[a] = math.sqrt(d2.sum())
    return out


def stats(v):
    v = np.asarray(v, float)
    return dict(mean=float(v.mean()), median=float(np.median(v)), p10=float(np.percentile(v, 10)),
                p90=float(np.percentile(v, 90)), n=int(len(v)))


def analyse(pdb):
    el, xyz = read_all(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    names, H, resid = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    hull = ConvexHull(xyz)
    mw = float(sum(MASS.get(e, 12.0) for e in el))
    v_psv = mw * 0.73 / 0.6022                                   # A^3 (0.73 cm^3/g partial specific volume)
    dep = depth_to_hull(hull, H)
    buried = np.nonzero(dep >= 6.0)[0]
    Rs = [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0]
    D = np.linalg.norm(H[:, None, :] - H[None, :, :], axis=2)
    NR = {}
    rho_loc = {}
    for R in Rs:
        cnt = (D[buried] <= R).sum(1) - 1                        # exclude self
        NR[str(R)] = stats(cnt)
        rho_loc[str(R)] = float(cnt.mean() / (4 / 3 * math.pi * R ** 3))
    nn = np.sort(D, axis=1)[:, 1]
    b0 = random_b0(1000)
    w_iso = omega_loc(H) / (2 * math.pi) / 1e3                   # kHz
    w_o0 = omega_loc(H, b0) / (2 * math.pi) / 1e3
    # amide-only network (perdeuterated model used by C1-HN)
    keep = [i for i, n in enumerate(names) if n.startswith("H/")]
    Hn = H[keep]
    Dn = np.linalg.norm(Hn[:, None, :] - Hn[None, :, :], axis=2)
    dep_n = depth_to_hull(hull, Hn)
    bur_n = np.nonzero(dep_n >= 6.0)[0]
    NRn = {str(R): stats((Dn[bur_n] <= R).sum(1) - 1) for R in [4.0, 6.0, 8.0, 10.0, 12.0, 15.0, 20.0]}
    out = dict(pdb=pdb, n_atoms=int(len(el)), n_H=int(len(H)), mass_Da=mw,
               V_hull_A3=float(hull.volume), V_psv_A3=float(v_psv),
               rho_H_hull=float(len(H) / hull.volume), rho_H_psv=float(len(H) / v_psv),
               n_buried_H=int(len(buried)), rho_H_local_buried=rho_loc, N_within_R_buried=NR,
               nn_dist_A=stats(nn), omega_loc_iso_kHz=stats(w_iso), omega_loc_orient0_kHz=stats(w_o0),
               amide=dict(n_HN=int(len(Hn)), rho_HN_psv=float(len(Hn) / v_psv), nn_dist_A=stats(np.sort(Dn, 1)[:, 1]),
                          omega_loc_iso_kHz=stats(omega_loc(Hn) / (2 * math.pi) / 1e3),
                          N_within_R_buried=NRn, n_buried=int(len(bur_n))),
               probes={})
    for p in (19, 245, 325, 390):
        if p < len(H):
            out["probes"][str(p)] = dict(name=names[p], depth_A=float(dep[p]), omega_iso_kHz=float(w_iso[p]),
                                         omega_o0_kHz=float(w_o0[p]))
    return out


if __name__ == "__main__":
    res = {p: analyse(p) for p in ("1UBQ", "1PGA")}
    json.dump(res, open(os.path.join(HERE, "density_couplings.json"), "w"), indent=1)
    for p, r in res.items():
        print(p, "nH", r["n_H"], "rho_hull %.4f rho_psv %.4f" % (r["rho_H_hull"], r["rho_H_psv"]),
              "rho_local(6A) %.4f rho_local(10A) %.4f" % (r["rho_H_local_buried"]["6.0"], r["rho_H_local_buried"]["10.0"]),
              "N(5A) %.1f N(8A) %.1f" % (r["N_within_R_buried"]["5.0"]["mean"], r["N_within_R_buried"]["8.0"]["mean"]),
              "w_iso med %.1f kHz" % r["omega_loc_iso_kHz"]["median"], "w_o0 med %.1f" % r["omega_loc_orient0_kHz"]["median"],
              "nn med %.2f" % r["nn_dist_A"]["median"], "| HN:", r["amide"]["n_HN"],
              "rho %.4f" % r["amide"]["rho_HN_psv"], "w_iso med %.2f kHz" % r["amide"]["omega_loc_iso_kHz"]["median"])
        print("  probes", r["probes"])
