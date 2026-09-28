"""Score the auditor's new CQC runs (out_cqc/) and exact-vs-exact runs (out_exact/) with the lane metric + power audit."""
import glob, json, math, os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import power_audit as PA  # noqa: E402

rows = []
for f in sorted(glob.glob(os.path.join(HERE, "out_cqc", "*.json"))):
    if f.endswith(".ckpt.json"):
        continue
    d = json.load(open(f))
    F, S = {}, {}
    for k, t in zip(d["ks"], d["times_us"]):
        r = d["res"][str(k)]["F_core"]
        F[round(t)] = {b: v[0] for b, v in r.items()}
        S[round(t)] = {b: v[1] for b, v in r.items()}
    a = PA.audit(F, S, d["probe"], d["N"], d["M"])
    ex = PA.ref(d["probe"], d["N"])
    per = {b: [round(F[t][b] - ex[t][b], 4) for t in sorted(F)] for b in F[sorted(F)[0]]}
    rows.append(dict(file=os.path.basename(f), sizes=d["group_sizes"], secs=round(d["secs_total"], 1),
                     cpu=round(d["cpu_this_call"], 1), signed_err_by_b_t=per, **a))
ee = []
for f in sorted(glob.glob(os.path.join(HERE, "out_exact", "*N14*.json"))):
    if f.endswith(".ckpt.json"):
        continue
    d = json.load(open(f))
    ex = PA.ref(d["probe"], d["N"])
    seeds = [str(s) for s in d["seeds"]]
    for s in seeds:
        e = max(abs(d["F"][str(k)][s][b] - ex[round(2 * k)][b]) for k in d["ks"] for b in d["F"][str(k)][s])
        ee.append(dict(kind="exact(seed)-vs-reference", seed=s, E=round(e, 5)))
    for i in range(len(seeds)):
        for j in range(i + 1, len(seeds)):
            e = max(abs(d["F"][str(k)][seeds[i]][b] - d["F"][str(k)][seeds[j]][b]) for k in d["ks"]
                    for b in d["F"][str(k)][seeds[i]])
            ee.append(dict(kind="exact-vs-exact (independent vectors)", seeds=[seeds[i], seeds[j]], E=round(e, 5)))
out = dict(new_cqc=rows, exact_vs_exact_N14=ee)
json.dump(out, open(os.path.join(HERE, "score_new.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
