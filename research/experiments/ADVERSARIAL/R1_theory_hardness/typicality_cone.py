"""R1 theory_hardness, RECOMMENDED GOVERNED JOB (decisive test T-A): cluster-size convergence of the echo F_ab(t) for
the instrument's observed sites b over the FULL window (to 320 us), on nested clusters N = 12 .. 24, by statevector
typicality (qapf.nmr.spins.exact_correlators; exact circuit, statistical error ~ 2^{-N/2}/sqrt(n_rand)).

Why: the sparse-Pauli ladder (pauli_cone.py) is certified only to ~40 us; exact sector runs stop at N = 12-14. The
sigma-cone N_sigma(t) at the informative times (80-320 us) decides whether exact classical simulation of the light
cone suffices (kill) or not.

Kill rule (pre-stated here, to be copied into the prereg deviation log before running):
  N_sigma(t) := smallest N in the ladder such that |F^(N') - F^(N)| <= sigma + 2*err_typ for every larger N' and every
  instrument b.  KILL (exact light-cone simulation suffices) if N_sigma(t) <= 24 for all t <= 320 us for both probes.
  SUPPORT the 'beyond exact reach' premise if F still moves by > 3 sigma between N = 20 and N = 24 at t >= 160 us.

Command (governed, single-threaded). Measured: N=12 106 s (n_rand 4), N=14 86 s (n_rand 1). Scaled estimates:
N=16 ~6-10 min, N=20 ~2-4 h, N=22 ~8-15 h, N=24 ~1.5-3 days and ~2.5 GB (run N <= 22 first):
  OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python \
     research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone.py --probe 19 --N 20
Smoke test (validates against the exact sector result, seconds):
  python .../typicality_cone.py --probe 19 --N 12 --n-rand 4 --validate 1
Output: typicality_cone/<pdb>_p<probe>_N<N>.json
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402


def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def instrument_bs(xyz, probe, K=3, N0=10):
    """the instrument's observed sites for the N0 = 10 cluster (3 farthest + nearest), as cluster-local indices; the
    clusters are nested by distance, so the same indices refer to the same protons at every N >= N0."""
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
    ap.add_argument("--n-rand", type=int, default=1)
    ap.add_argument("--validate", type=int, default=0)
    a = ap.parse_args()
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{a.pdb}_H.pdb"))
    bs = instrument_bs(xyz, a.probe)
    idx = SP.cluster(xyz, a.probe, a.N)
    dm = SP.couplings(xyz[idx], random_b0(1000))
    t0 = time.time()
    tt, S, to, F = SP.exact_correlators(dm, a.dt, a.steps, 0, bs, n_rand=a.n_rand, otoc=True,
                                        record_every=a.otoc_every, otoc_every=a.otoc_every,
                                        rng=np.random.default_rng(12345))
    out = dict(pdb=a.pdb, probe=a.probe, N=a.N, bs=bs, names_bs=[names[idx[b]] for b in bs], n_rand=a.n_rand,
               err_typ=float(2 ** (-a.N / 2) / np.sqrt(a.n_rand)), times_us=(np.asarray(to) * 1e6).tolist(),
               F={str(b): np.asarray(F[b]).tolist() for b in bs}, S={str(b): np.asarray(S[b]).tolist() for b in bs},
               secs=time.time() - t0)
    if a.validate:
        fe = os.path.join(HERE, "front", f"{a.pdb}_p{a.probe}_N{a.N}_o0.json")
        if os.path.exists(fe):
            ex = json.load(open(fe)); te = np.array(ex["times_us"]); FZ = np.array(ex["FZ"])
            dev = 0.0
            for i, t in enumerate(out["times_us"]):
                j = int(np.argmin(abs(te - t)))
                if abs(te[j] - t) < 0.5:
                    dev = max(dev, max(abs(out["F"][str(b)][i] - FZ[j, b]) for b in bs))
            out["validate_max_dev_vs_exact"] = dev
    os.makedirs(os.path.join(HERE, "typicality_cone"), exist_ok=True)
    json.dump(out, open(os.path.join(HERE, "typicality_cone", f"{a.pdb}_p{a.probe}_N{a.N}.json"), "w"))
    print(json.dumps(dict(N=a.N, bs=bs, secs=round(out["secs"], 1), err_typ=out["err_typ"],
                          validate=out.get("validate_max_dev_vs_exact"))))


if __name__ == "__main__":
    main()
