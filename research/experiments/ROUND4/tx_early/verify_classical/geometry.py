"""Verifier: where do the strong partners of each instrument site b sit in the probe-centred cluster ordering?
(no dynamics; -> geometry.json)

For probe a and instrument site b (standard index into the probe-centred N = 10 core), list every proton c with
|d_bc| above a threshold, its distance to b and to a, and its rank in the probe-centred ordering (rank r means it
enters the cluster at N = r + 1).  Also the fraction of b's second moment M2_b = sum_c d_bc^2 (all protons in the
protein) that lies inside the probe-centred N-cluster, for N = 18..30, and the same for a.
Couplings as in the lanes: spins.couplings with b0 = random_b0(1000) (orientation 0).
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "experiments", "ROUND3", "r1sim_exact_reach"))
import fastecho as FE  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

out = {}
names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
b0 = FE.random_b0(1000)
b0 = b0 / np.linalg.norm(b0)


def dcoup(i, js):
    v = xyz[js] - xyz[i]
    r = np.linalg.norm(v, axis=1)
    c = (v @ b0) / r
    return SP.D1A * (1.0 / r ** 3) * (3 * c ** 2 - 1) / 2, r


for p in (19, 245):
    order = SP.cluster(xyz, p, len(xyz))                     # full probe-centred ordering
    rank = {int(g): r for r, g in enumerate(order)}
    bs = FE.instrument_bs(xyz, p)
    std10 = order[:10]
    others = np.array([i for i in range(len(xyz))])
    res = dict(bs=bs, sites={})
    for site in [0] + [1, 7, 8, 9]:
        g = int(std10[site])
        js = np.array([j for j in others if j != g])
        d, r = dcoup(g, js)
        M2 = float(np.sum(d ** 2))
        strong = np.argsort(-np.abs(d))[:12]
        rows = []
        for s in strong:
            j = int(js[s])
            rows.append(dict(rank=rank[j], name=names[j], r_b=float(r[s]), r_a=float(np.linalg.norm(xyz[j] - xyz[p])),
                             d_krad_s=float(d[s] / 1e3), frac_M2=float(d[s] ** 2 / M2)))
        frac = {}
        for N in (16, 18, 20, 22, 24, 26, 30, 40, 80):
            inside = set(int(x) for x in order[:N])
            mask = np.array([int(j) in inside for j in js])
            frac[N] = float(np.sum(d[mask] ** 2) / M2)
        res["sites"][f"site{site}"] = dict(global_index=g, name=names[g], M2=M2, strongest=rows, frac_M2_inside_N=frac)
    out[f"p{p}"] = res

with open(os.path.join(HERE, "geometry.json"), "w") as f:
    json.dump(out, f, indent=1)
for p, res in out.items():
    for s, v in res["sites"].items():
        print(p, s, v["name"], "frac M2 inside N:", {k: round(x, 3) for k, x in v["frac_M2_inside_N"].items()})
        for r in v["strongest"][:6]:
            print(f"     rank {r['rank']:3d} {r['name']:14s} r_b {r['r_b']:.2f} r_a {r['r_a']:.2f} d {r['d_krad_s']:+8.1f} krad/s "
                  f"frac {r['frac_M2']:.3f}")
