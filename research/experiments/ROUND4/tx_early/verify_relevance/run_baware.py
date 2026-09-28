"""Cross-family check of the lane's 'F converged at 40 us' claim (PREREG Round 4 H-2 requires one).

The lane's F ladders are all probe-centred (nearest-N protons to the probe a). verify_rel.py shows that several
instrument sites b sit at the cluster edge and that their dominant dipolar partner is absent even at N = 22
(p19 b8 HG22/ILE3: its methyl partner HG23/ILE3, 82% of M2_b, enters at rank 24; p19 b9: 64% at rank 26;
p245 b7 HA/LYS27: 49% at rank 48).

Test: same estimator, same circuit, same seed/draws (common random numbers, R = 1), same N, two cluster families:
  pc     : probe-centred ranks 0..N-1 (the lane's family)
  baware : ranks 0..N-1-m plus the m listed partner ranks (b-aware)
Only t = 40 us (20 Trotter steps). Driver = the lane's validated tx_echo.run, with the instance loader patched to
return the custom cluster and outputs redirected into this folder. Checkpointed/resumable (tx_echo semantics).

usage: python run_baware.py --probe 19 --N 20 --variant baware --extra 24 26 [--wall-s 280]
"""
import argparse
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import kernels as KR  # noqa: E402
import tx_echo as TX  # noqa: E402

FE, SP = KR.FE, KR.SP


def make_loader(extra):
    def load_instance(pdb, probe, N):
        names, xyz, _ = SP.read_h_coords(os.path.join(KR.ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
        bs = FE.instrument_bs(xyz, probe)
        order = SP.cluster(xyz, probe, len(xyz))
        ranks = list(range(N - len(extra))) + list(extra)
        assert len(set(ranks)) == N and N - len(extra) >= 10
        idx = order[ranks]
        dm = SP.couplings(xyz[idx], FE.random_b0(1000))
        return dm, bs, [names[idx[b]] for b in bs], xyz[idx]
    return load_instance


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--variant", default="baware")
    ap.add_argument("--extra", type=int, nargs="*", default=[])
    ap.add_argument("--seed", type=int, default=4242)
    ap.add_argument("--wall-s", type=float, default=None)
    a = ap.parse_args()
    FE.load_instance = make_loader(a.extra)
    TX.HERE = HERE                                   # tx_echo writes to HERE/runs/<tag>*
    os.makedirs(os.path.join(HERE, "runs"), exist_ok=True)
    ex = "-".join(map(str, a.extra)) if a.extra else "none"
    tag = f"1UBQ_p{a.probe}_N{a.N}_{a.variant}_x{ex}_echo_R1_complex64_s{a.seed}_t20"
    res = TX.run("1UBQ", a.probe, a.N, "echo", [20], 1, np.dtype("complex64"), a.seed, tag, None, log=lambda s: None,
                 wall_s=a.wall_s)
    res["variant"] = a.variant
    res["extra_ranks"] = a.extra
    TX.atomic_json(res, os.path.join(HERE, "runs", tag + ".json"))
    print(json.dumps(dict(tag=tag, complete=res["complete"], cpu_s=round(res["cpu_s"], 1),
                          F={b: round(v[0], 5) for b, v in res.get("F", {}).items()},
                          H=[round(h, 5) for h in res.get("H", [])], floor=[round(f, 5) for f in res.get("floor", [])],
                          rss=round(res.get("peak_rss_GB", 0), 3))))


if __name__ == "__main__":
    main()
