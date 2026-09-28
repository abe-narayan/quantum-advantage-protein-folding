"""nl-spinDMFT embedded-cluster run: two-point G_ja(t), H_C, and the quenched-bath OTOC F_ab at 40/80/120 us.
  --world protein | N       (bath = all other protons of the protein | the rest of the closed N-spin probe cluster)
  --family probeb           C = {a} U instrument sites {1,7,8,9} U nearest probe-cluster ranks, |C| = n_c
  --family pairb:<b>        C = {a, b} U protons nearest to a or b (min distance), |C| = n_c (b-aware cluster)
Bath autocorrelations: self-consistent sr-spinDMFT (run_sr.py checkpoints).  Checkpoint per batch; resumable."""
import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sdmft as S  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--probe", type=int, required=True)
ap.add_argument("--world", default="protein")
ap.add_argument("--nc", type=int, required=True)
ap.add_argument("--family", default="probeb")
ap.add_argument("--M", type=int, default=256)
ap.add_argument("--batch", type=int, default=32)
ap.add_argument("--nsteps", type=int, default=60)
ap.add_argument("--otoc", default="20,40,60")
ap.add_argument("--seed", type=int, default=7)
ap.add_argument("--budget", type=float, default=1500.0, help="wall seconds before a clean checkpointed stop")
ap.add_argument("--bath", default="sr", help="sr | none")
a = ap.parse_args()

names, xyz_all, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
order = SP.cluster(xyz_all, a.probe, len(xyz_all))                     # world index -> global index
if a.world == "protein":
    Nw = len(order)
    z = np.load(os.path.join(HERE, "out", "sr_protein_T120_M384.ckpt.npz"), allow_pickle=True)
    gz, gp = z["gz"][order], z["gp"][order]
else:
    Nw = int(a.world)
    z = np.load(os.path.join(HERE, "out", f"sr_1UBQ_p{a.probe}_N{Nw}_T120_M4096.ckpt.npz"), allow_pickle=True)
    gz, gp = z["gz"], z["gp"]
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
    C = sorted(C)[:a.nc] if a.nc >= len(bs) + 1 else [0] + list(bs)[: a.nc - 1]
    bsl = [C.index(b) for b in bs if b in C]
    bglob = [b for b in bs if b in C]
elif a.family.startswith("pairb"):
    b = int(a.family.split(":")[1])
    X = w["xyz"]
    dmin = np.minimum(np.linalg.norm(X - X[0], axis=1), np.linalg.norm(X - X[b], axis=1))
    rest = [int(i) for i in np.argsort(dmin, kind="stable") if i not in (0, b)]
    C = sorted([0, b] + rest[: a.nc - 2])
    bsl = [C.index(b)]; bglob = [b]
else:
    raise ValueError(a.family)
if a.bath == "none":
    gz = gz * 0.0; gp = gp * 0.0
otoc = [int(x) for x in a.otoc.split(",") if x]
tag = f"emb_p{a.probe}_W{a.world}_nc{a.nc}_{a.family.replace(':', '')}_{a.bath}_M{a.M}_s{a.seed}"
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
ck = os.path.join(HERE, "out", tag + ".ckpt.json")
t0 = time.time(); c0 = time.process_time()
st = S.run_embedded(D, C, bsl, gz, gp, a.nsteps, otoc, a.M, a.batch, a.seed, ckpt=ck, budget_s=a.budget,
                    log=lambda s: print(s, flush=True))
sm = S.summarize(st)
Dc = D[np.ix_(C, C)]
bath_frac = [float(1.0 - (Dc[i] ** 2).sum() / (D[C[i]] ** 2).sum()) for i in range(len(C))]
out = dict(tag=tag, probe=a.probe, world=a.world, nc=a.nc, family=a.family, bath=a.bath, C_world=C,
           C_names=[w["names"][i] for i in C], bs_world=bglob, bs_local=bsl, bath_M2_fraction=bath_frac,
           complete=st["done"] >= a.M // a.batch, **sm)
S.atomic_json(out, os.path.join(HERE, "out", tag + ".json"))
F = np.array(sm["F"]); Fse = np.array(sm["F_se"])
print("M", sm["M"], "cpu", round(sm["cpu"], 1), "Gaa", [round(sm["Gaa"][sm["times_us"].index(t)], 4) for t in (40.0, 80.0, 120.0)],
      "H_C", [round(sm["H_C"][sm["times_us"].index(t)], 4) for t in (40.0, 80.0, 120.0)])
for i, t in enumerate(otoc):
    print(" t=%d us F=" % (2 * t), [round(x, 4) for x in F[i]], "se", [round(x, 4) for x in Fse[i]])
