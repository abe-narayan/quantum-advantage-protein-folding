"""Cheap seed replication of two lane CQC runs with a fresh seed (lane used seed 7).

Imports the lane's cqc_echo.py unchanged; writes ONLY into this folder (atomic tmp+replace).
Runs: p19 N16 kl6/none and p245 N16 kl6/none (a few CPU-seconds each), scored against the exact typicality cone
exactly as compare.py does: max |F - F_exact| over b in {1,7,8,9} and t in {80,160,240,320} us.
"""
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
sys.path.insert(0, LANE)
import cqc_echo as C  # noqa: E402

REPO = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
CONE = os.path.join(REPO, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
OUTF = os.path.join(HERE, "seed_replay.json")
SEED = 101
M = 48
DT = 2e-6
TIMES = [80, 160, 240, 320]


def run(probe, N, bath, ba):
    dm, bs, _ = C.setup("1UBQ", probe, N)
    groups = C.partition(dm, bs, "x", bath)
    q = C.CQC(dm, groups, DT, ba)
    q.zz_only = False
    q.lam = 1.0
    ks = [int(round(t * 1e-6 / DT)) for t in TIMES]
    t0 = time.time()
    res = C.echo(q, bs, ks, M, SEED)
    ref = json.load(open(os.path.join(CONE, f"1UBQ_p{probe}_N{N}.json")))
    errs = {}
    for k, t in zip(ks, TIMES):
        i = [j for j, tt in enumerate(ref["times_us"]) if abs(tt - t) < 1e-6][0]
        errs[t] = max(abs(res[str(k)]["F_tdh"][str(b)][0] - ref["F"][str(b)][i]) for b in bs)
    return {"probe": probe, "N": N, "bath": bath, "ba": ba, "seed": SEED, "M": M, "sizes": [len(g) for g in groups],
            "max_err": round(max(errs.values()), 4), "err_by_t": {str(k): round(v, 4) for k, v in errs.items()},
            "secs": round(time.time() - t0, 1)}


def main():
    out = json.load(open(OUTF)) if os.path.exists(OUTF) else {"runs": []}
    done = {(r["probe"], r["N"], r["bath"], r["ba"]) for r in out["runs"]}
    for probe, N, bath, ba in [(19, 16, "kl6", "none"), (245, 16, "kl6", "none")]:
        if (probe, N, bath, ba) in done:
            continue
        r = run(probe, N, bath, ba)
        print(json.dumps(r))
        out["runs"].append(r)
        tmp = OUTF + ".tmp"
        json.dump(out, open(tmp, "w"), indent=1)
        os.replace(tmp, OUTF)


if __name__ == "__main__":
    main()
