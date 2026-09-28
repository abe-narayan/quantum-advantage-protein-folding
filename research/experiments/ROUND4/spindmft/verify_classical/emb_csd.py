"""Classical verifier: the lane's nl-spinDMFT embedded cluster + quenched-bath OTOC (sdmft.run_embedded, imported
read-only) with the Gaussian bath autocorrelations taken from CLASSICAL SPIN DYNAMICS (csd_bath.py) instead of
self-consistent sr-spinDMFT.  Same clusters (probeb / pairb:<b>), same n_c, same seeds and batch layout as the lane's
run_emb.py, so the only change is the bath model.  g_j are normalised by g_j(0) (exact value 1; ratio estimator).
Checkpoint per batch (sdmft.run_embedded, atomic).  Output: out/embcsd_<tag>.json"""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import sdmft as S  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--probe", type=int, required=True)
ap.add_argument("--world", default="protein")
ap.add_argument("--nc", type=int, default=10)
ap.add_argument("--family", default="probeb")
ap.add_argument("--M", type=int, default=512)
ap.add_argument("--batch", type=int, default=32)
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--budget", type=float, default=1500.0)
a = ap.parse_args()

names, xyz_all, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
order = SP.cluster(xyz_all, a.probe, len(xyz_all))
if a.world == "protein":
    Nw = len(order)
    z = np.load(os.path.join(HERE, "out", "csd_protein_M1024.npz"))
    gz, gp = z["gz"][order], z["gp"][order]
else:
    Nw = int(a.world)
    z = np.load(os.path.join(HERE, "out", f"csd_p{a.probe}_N{Nw}_M8192.npz"))
    gz, gp = z["gz"], z["gp"]
gz = gz / gz[:, :1]; gp = gp / gp[:, :1]
w = S.load_world("1UBQ", a.probe, Nw)
D = w["D"]; bs = w["bs"]
assert np.array_equal(w["idx"], order[:Nw])
if a.family == "probeb":
    C = [0] + list(bs)
    k = 1
    while len(C) < a.nc:
        if k not in C:
            C.append(k)
        k += 1
    C = sorted(C)[:a.nc]
    bsl = [C.index(b) for b in bs if b in C]; bglob = [b for b in bs if b in C]
elif a.family.startswith("pairb"):
    b = int(a.family.split(":")[1])
    X = w["xyz"]
    dmin = np.minimum(np.linalg.norm(X - X[0], axis=1), np.linalg.norm(X - X[b], axis=1))
    rest = [int(i) for i in np.argsort(dmin, kind="stable") if i not in (0, b)]
    C = sorted([0, b] + rest[: a.nc - 2])
    bsl = [C.index(b)]; bglob = [b]
else:
    raise ValueError(a.family)
tag = f"embcsd_p{a.probe}_W{a.world}_nc{a.nc}_{a.family.replace(':', '')}_M{a.M}_s{a.seed}"
ck = os.path.join(HERE, "out", tag + ".ckpt.json")
st = S.run_embedded(D, C, bsl, gz, gp, 60, [20, 40, 60], a.M, a.batch, a.seed, ckpt=ck, budget_s=a.budget, log=None)
sm = S.summarize(st)
out = dict(tag=tag, probe=a.probe, world=a.world, nc=a.nc, family=a.family, bath="csd", C_world=C, bs_world=bglob,
           bs_local=bsl, complete=st["done"] >= a.M // a.batch, **sm)
tmp = os.path.join(HERE, "out", tag + ".json.tmp")
json.dump(out, open(tmp, "w"))
os.replace(tmp, os.path.join(HERE, "out", tag + ".json"))
F = np.array(sm["F"]); Fse = np.array(sm["F_se"])
print(tag, "M", sm["M"], "cpu", round(sm["cpu"], 1), "Gaa", [round(sm["Gaa"][sm["times_us"].index(t)], 4) for t in (40.0, 80.0, 120.0)])
for i, t in enumerate((40, 80, 120)):
    print(" t=%d F=" % t, [round(x, 4) for x in F[i]], "se", [round(x, 4) for x in Fse[i]], flush=True)
