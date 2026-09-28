"""Self-consistent sr-spinDMFT bath autocorrelations g_j^z, g_j^perp.
  --world protein : all 629 1UBQ protons (global PDB-H order; probe-independent), the isolated-molecule limit.
  --world N --probe p : the closed probe cluster of N spins (validation world; order = probe-cluster rank).
Checkpoint after every iteration (atomic), resumable.  Output: out/sr_<tag>.json (+ .npz with the g arrays)."""
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
ap.add_argument("--world", default="protein")
ap.add_argument("--probe", type=int, default=19)
ap.add_argument("--T", type=int, default=120)
ap.add_argument("--M", type=int, default=384)
ap.add_argument("--iters", type=int, default=8)
ap.add_argument("--seed", type=int, default=11)
a = ap.parse_args()
os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
if a.world == "protein":
    names, xyz, _ = SP.read_h_coords(os.path.join(S.ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
    D = SP.couplings(xyz, S.random_b0(1000))
    tag = f"protein_T{a.T}_M{a.M}"
    sites = [19, 245]
else:
    w = S.load_world("1UBQ", a.probe, int(a.world))
    D = w["D"]
    tag = f"1UBQ_p{a.probe}_N{a.world}_T{a.T}_M{a.M}"
    sites = [0]
ck = os.path.join(HERE, "out", f"sr_{tag}.ckpt.npz")
t0 = time.time(); c0 = time.process_time()
g0 = None; hist = []; it0 = 0
if os.path.exists(ck):
    z = np.load(ck, allow_pickle=True)
    g0 = (z["gz"], z["gp"]); hist = json.loads(str(z["hist"])); it0 = len(hist)
    print("resume at iteration", it0)
for it in range(it0, a.iters):
    res = S.sr_spindmft(D, a.T, a.M, 1, a.seed + 1000 * it, g0=g0, log=None, sites_out=sites)
    g0 = (res["gz"], res["gp"])
    h = res["history"][0]; h["it"] = it
    hist.append(h)
    np.savez(ck + ".tmp.npz", gz=g0[0], gp=g0[1], hist=json.dumps(hist))
    os.replace(ck + ".tmp.npz", ck)
    print(json.dumps(h), flush=True)
out = dict(world=a.world, probe=a.probe, T=a.T, M=a.M, times_us=list(range(a.T + 1)), history=hist,
           g_sites={str(s): dict(gz=g0[0][s].tolist(), gp=g0[1][s].tolist()) for s in sites},
           se_last=res["se_last"], wall_s=time.time() - t0, cpu_s=time.process_time() - c0,
           note="gz/gp arrays for all sites in the .ckpt.npz (final iteration)")
S.atomic_json(out, os.path.join(HERE, "out", f"sr_{tag}.json"))
print("done", round(time.time() - t0, 1), "s")
