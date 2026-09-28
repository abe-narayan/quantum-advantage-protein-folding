"""Verifier driver: exact typicality echo F_ab on SITE-AWARE clusters, reusing the lane's validated tx_echo.run.

Why: in the probe-centred family the dominant dipolar partners of several instrument sites b enter only at ranks
24-48 (geometry.json), so F_N(probe) can plateau over N = 16..22 without containing b's own strongest coupling.
Cluster specs (all use the same reference first-order Trotter circuit, dt = 2 us, b0 = random_b0(1000), gamma = 0):
  probe:N              the lane's family (N nearest to the probe)                       [validation]
  bpart:n0:m           probe ranks 0..n0-1  +  the m strongest-|d_bc| partners c of site b with probe rank >= n0
  custom:n0:r1,r2,..   probe ranks 0..n0-1  +  the listed probe ranks
Instrument-site index b is unchanged (ranks 0..9 are the standard core, so n0 >= 10 keeps b at its standard index).
Only the requested site(s) are evolved (F_ab for other b is not needed), which cuts the cost ~2.5x.

Implementation: monkeypatches fastecho.load_instance (the only cluster entry point of tx_echo.run) and tx_echo.HERE
(so every checkpoint / npz / result lands in verify_classical/runs).  Everything else -- random draws (seed + 7919 N),
sector folding, kernels, checkpoint-after-every-leg, atomic writes, resume -- is tx_echo.run unchanged.
Resume: re-run the same command.
"""
from __future__ import annotations

import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import tx_echo as TX  # noqa: E402
from kernels import FE, SP  # noqa: E402


def cluster_spec(pdb, probe, spec, site):
    names, xyz, _ = SP.read_h_coords(os.path.join(FE.ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    order = [int(i) for i in SP.cluster(xyz, probe, len(xyz))]
    kind, *rest = spec.split(":")
    if kind == "probe":
        N = int(rest[0]); ranks = list(range(N))
    elif kind == "bpart":
        n0, m = int(rest[0]), int(rest[1])
        g = order[site]
        b0 = FE.random_b0(1000); b0 = b0 / np.linalg.norm(b0)
        cand = order[n0:]
        v = xyz[cand] - xyz[g]
        r = np.linalg.norm(v, axis=1)
        c = (v @ b0) / r
        d = SP.D1A / r ** 3 * (3 * c ** 2 - 1) / 2
        top = [n0 + int(i) for i in np.argsort(-np.abs(d))[:m]]
        ranks = list(range(n0)) + sorted(top)
    elif kind == "custom":
        n0 = int(rest[0]); ranks = list(range(n0)) + [int(x) for x in rest[1].split(",") if x]
    elif kind == "pairb":
        # ROUND3 decomp_echo 'pairb': N protons nearest to {a, b} (metric min(d_ia, d_ib)); a -> 0, b -> 1
        N = int(rest[0]); g = order[site]
        da = np.linalg.norm(xyz - xyz[probe], axis=1); db = np.linalg.norm(xyz - xyz[g], axis=1)
        rest_ = [int(i) for i in np.argsort(np.minimum(da, db), kind="stable") if i not in (probe, g)]
        idx = np.array([probe, g] + rest_[:N - 2])
        rank = {gg: r for r, gg in enumerate(order)}
        return idx, [rank[int(i)] for i in idx], names, xyz
    else:
        raise ValueError(spec)
    idx = np.array([order[r] for r in ranks])
    return idx, ranks, names, xyz


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--sites", type=int, nargs="+", required=True, help="standard instrument site indices b")
    ap.add_argument("--steps", type=int, nargs="+", default=[20, 40, 60])
    ap.add_argument("--R", type=int, default=1)
    ap.add_argument("--dtype", default="complex64")
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--budget-s", type=float, default=None)
    ap.add_argument("--wall-s", type=float, default=None)
    ap.add_argument("--max-phase", type=int, default=None)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--dt-us", type=float, default=2.0, help="Trotter step (lane/instrument: 2 us); steps count in units of dt")
    a = ap.parse_args()
    site_for_spec = a.sites[0]
    idx, ranks, names, xyz = cluster_spec(a.pdb, a.probe, a.spec, site_for_spec)
    N = len(idx)
    dm = SP.couplings(xyz[idx], FE.random_b0(1000))
    bs = [1] if a.spec.startswith("pairb") else list(a.sites)        # pairb puts b at cluster index 1
    info = dict(spec=a.spec, N=N, ranks=ranks, names=[names[i] for i in idx], sites=bs, std_site=a.sites[0])
    if a.dry:
        print(json.dumps(info)); return

    def loader(pdb, probe, N_):
        assert N_ == N
        return dm, bs, [names[idx[b]] for b in bs], xyz[idx]

    FE.load_instance = loader
    TX.FE.load_instance = loader
    TX.HERE = HERE
    TX.DT = a.dt_us * 1e-6
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    sp = a.spec.replace(":", "-").replace(",", "_")
    tag = (f"{a.pdb}_p{a.probe}_{sp}_b{'-'.join(map(str, a.sites))}_N{N}_R{a.R}_{a.dtype}_s{a.seed}_"
           f"t{'-'.join(map(str, sorted(a.steps)))}" + ("" if a.dt_us == 2.0 else f"_dt{a.dt_us:g}"))
    res = TX.run(a.pdb, a.probe, N, "echo", a.steps, a.R, np.dtype(a.dtype), a.seed, tag, a.budget_s,
                 wall_s=a.wall_s, max_phase=a.max_phase, log=lambda s: None)
    res.update(cluster=info)
    TX.atomic_json(res, os.path.join(HERE, "runs", tag + ".json"))
    print(json.dumps(dict(tag=tag, complete=res["complete"], steps_done=res.get("steps_done"), cpu_s=round(res["cpu_s"], 1),
                          vs=res["vector_steps"], rss=round(res.get("peak_rss_GB", 0), 3),
                          F={b: [round(x, 5) for x in v] for b, v in res.get("F", {}).items()},
                          H=[round(x, 5) for x in res.get("H", [])], floor=[round(x, 5) for x in res.get("floor", [])])))


if __name__ == "__main__":
    main()
