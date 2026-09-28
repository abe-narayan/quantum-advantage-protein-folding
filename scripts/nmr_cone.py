"""R1-SIM T-A with CHECKPOINTING: cluster-size convergence of the protein 1H echo F_ab(t) at the instrument's sites b.

Numerically identical to research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone.py: same nested cluster,
b0, instrument sites, typicality vector (rng seed 12345, n_rand = 1), Trotter circuit and times.  The difference: every
echo time point is saved to <out>.ckpt.json as soon as it is computed, and a restarted job resumes from the checkpoint,
so a memory kill (host reaping or governor) loses at most one time point.  The final JSON has the same format as the
original script, so scripts/analyze_cone.py reads it unchanged.

Usage: python scripts/nmr_cone.py --probe 19 --N 20
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

OUT = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def instrument_bs(xyz, probe, K=3, N0=10):
    idx = SP.cluster(xyz, probe, N0)
    X0 = xyz[idx]
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    return sorted(set(far + [int(np.argsort(dist)[1])]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--steps", type=int, default=160)
    ap.add_argument("--otoc-every", type=int, default=20)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    fj = os.path.join(OUT, f"{a.pdb}_p{a.probe}_N{a.N}.json")
    if os.path.exists(fj):
        print("exists"); return
    ck = fj + ".ckpt.json"
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    bs = instrument_bs(xyz, a.probe)
    idx = SP.cluster(xyz, a.probe, a.N)
    dm = SP.couplings(xyz[idx], random_b0(1000))
    N = a.N
    pairs = SP.pair_list(dm, a.dt)
    rng = np.random.default_rng(12345)                      # identical draw order to exact_correlators (n_rand = 1)
    shape = (2,) * N
    psi0 = rng.standard_normal(shape) + 1j * rng.standard_normal(shape)
    psi0 /= np.linalg.norm(psi0)
    otimes = list(range(0, a.steps + 1, a.otoc_every))
    state = dict(done={}, S=None, secs=0.0)
    if os.path.exists(ck):
        state = json.load(open(ck))
        print(json.dumps({"resumed_from_checkpoint": sorted(int(k) for k in state["done"])}), flush=True)
    t0 = time.time() - state.get("secs", 0.0)

    def save():
        state["secs"] = time.time() - t0
        json.dump(state, open(ck + ".tmp", "w"))
        os.replace(ck + ".tmp", ck)

    if state.get("S") is None:                               # transfer S at the echo times (one forward pass)
        S = {str(b): [] for b in bs}
        phi = psi0.copy(); chis = {b: SP.zmul(psi0.copy(), N, b) for b in bs}
        for k in range(a.steps + 1):
            if k in otimes:
                va = SP.zmul(phi.copy(), N, 0)
                for b in bs:
                    S[str(b)].append(float(np.real(np.vdot(va, chis[b]))))
            if k == a.steps:
                break
            SP.apply_step(phi, N, pairs)
            for b in bs:
                SP.apply_step(chis[b], N, pairs)
        state["S"] = S
        save()

    def W(vv, k):
        vv = vv.copy()
        for _ in range(k):
            SP.apply_step(vv, N, pairs)
        SP.zmul(vv, N, 0)
        for _ in range(k):
            SP.apply_step(vv, N, pairs, inverse=True)
        return vv

    for k in otimes:
        if str(k) in state["done"]:
            continue
        if k == 0:
            state["done"][str(k)] = {str(b): 1.0 for b in bs}
            save(); continue
        Wpsi = W(psi0, k)
        vals = {}
        for b in bs:
            lhs = SP.zmul(Wpsi.copy(), N, b)
            rhs = W(SP.zmul(psi0.copy(), N, b), k)
            vals[str(b)] = float(np.real(np.vdot(lhs, rhs)))
        state["done"][str(k)] = vals
        save()
        print(json.dumps({"k": k, "t_us": k * a.dt * 1e6, "secs": round(time.time() - t0)}), flush=True)
    F = {str(b): [state["done"][str(k)][str(b)] for k in otimes] for b in bs}
    out = dict(pdb=a.pdb, probe=a.probe, N=N, bs=bs, names_bs=[names[idx[b]] for b in bs], n_rand=1,
               err_typ=float(2 ** (-N / 2)), times_us=[k * a.dt * 1e6 for k in otimes], F=F, S=state["S"],
               secs=time.time() - t0, checkpointed=True)
    json.dump(out, open(fj + ".tmp", "w"))
    os.replace(fj + ".tmp", fj)
    os.remove(ck)
    print(json.dumps({"N": N, "done": True, "secs": round(out["secs"])}))


if __name__ == "__main__":
    main()
