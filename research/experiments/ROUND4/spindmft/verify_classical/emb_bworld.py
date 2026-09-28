"""Classical verifier: bath correction for the EXACT b-aware family (the lane's own next test #1, cheap version).

For series (a, b): C = the first n_c spins of the b-aware order {a, b, nearest by min(d_a, d_b)} (a first).
World W_b = the closed b-aware N-spin cluster that was solved exactly in fe_pairb.py (same global indices), or the whole
protein.  Bath autocorrelations from classical spin dynamics in that world (csd_bath.run_batch; protein: csd_protein
npz).  Embedded cluster + quenched-bath OTOC = the lane's sdmft.run_embedded (imported read-only), same seeds.
Delta_b(t) = F_emb(protein) - F_emb(W_b);  estimator F_corr_b = F_exact,b-aware(N) + Delta_b.
Checkpoint per batch (atomic).  Output: out/embb_<tag>.json"""
import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
sys.path.insert(0, HERE)
import sdmft as S  # noqa: E402
import csd_bath as CB  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--probe", type=int, required=True)
ap.add_argument("--b", type=int, required=True)
ap.add_argument("--Nref", type=int, required=True, help="b-aware exact cluster size defining W_b (fe_pairb output)")
ap.add_argument("--world", default="Wb", help="Wb | protein")
ap.add_argument("--nc", type=int, default=10)
ap.add_argument("--M", type=int, default=512)
ap.add_argument("--batch", type=int, default=32)
ap.add_argument("--seed", type=int, default=7)
a = ap.parse_args()

names, xyz, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
b0 = S.random_b0(1000)
ref = None
for R, dt in ((2, "complex128"), (1, "complex64")):
    f = os.path.join(HERE, "out", f"fe_pairb_p{a.probe}_b{a.b}_N{a.Nref}_R{R}_{dt}.json")
    if os.path.exists(f):
        ref = json.load(open(f)); break
gW = [int(i) for i in ref["global_idx"]]            # a, b, rest by min distance
Cg = gW[:a.nc]
tag = f"embb_p{a.probe}_b{a.b}_Nref{a.Nref}_W{a.world}_nc{a.nc}_M{a.M}_s{a.seed}"
if a.world == "Wb":
    widx = gW
    D = SP.couplings(xyz[widx], b0)
    ck = os.path.join(HERE, "out", f"csdWb_p{a.probe}_b{a.b}_N{a.Nref}.npz")
    if os.path.exists(ck):
        z = np.load(ck); gz, gp = z["gz"], z["gp"]
    else:
        az = np.zeros((len(widx), CB.T_LAG + 1)); ap_ = np.zeros_like(az); cnt = np.zeros(CB.T_LAG + 1)
        for ib in range(8):
            z1, z2, c, _ = CB.run_batch(D, 1024, np.random.default_rng([4242, ib]))
            az += z1; ap_ += z2; cnt += c
        gz, gp = az / cnt, ap_ / cnt
        np.savez(ck + ".tmp.npz", gz=gz, gp=gp); os.replace(ck + ".tmp.npz", ck)
else:
    rest = [i for i in range(len(xyz)) if i not in set(Cg)]
    widx = Cg + rest
    D = SP.couplings(xyz[widx], b0)
    z = np.load(os.path.join(HERE, "out", "csd_protein_M1024.npz"))
    gz, gp = z["gz"][widx], z["gp"][widx]
gz = gz / gz[:, :1]; gp = gp / gp[:, :1]
C = list(range(a.nc))
assert [widx[i] for i in C] == Cg
ckj = os.path.join(HERE, "out", tag + ".ckpt.json")
st = S.run_embedded(D, C, [1], gz, gp, 60, [20, 40, 60], a.M, a.batch, a.seed, ckpt=ckj, budget_s=1500.0, log=None)
sm = S.summarize(st)
out = dict(tag=tag, probe=a.probe, b=a.b, Nref=a.Nref, world=a.world, nc=a.nc, C_global=Cg, C_names=[names[i] for i in Cg],
           complete=st["done"] >= a.M // a.batch, F=[row[0] for row in sm["F"]], F_se=[row[0] for row in sm["F_se"]],
           Gaa=[sm["Gaa"][sm["times_us"].index(t)] for t in (40.0, 80.0, 120.0)], cpu=sm["cpu"], M=sm["M"])
tmp = os.path.join(HERE, "out", tag + ".json.tmp")
json.dump(out, open(tmp, "w"))
os.replace(tmp, os.path.join(HERE, "out", tag + ".json"))
print(tag, "F", [round(x, 4) for x in out["F"]], "se", [round(x, 4) for x in out["F_se"]], "cpu", round(out["cpu"], 1), flush=True)
