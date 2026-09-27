"""Build a resume queue after an interrupted governor run: every job ever spooled whose output does not exist yet and
is not cancelled, deduplicated by OUTPUT (not by job name), ordered by decision value.  Writes
research/results/RAW/master/spool_resume.jsonl (plain FIFO; no priority flags) and prints a summary.

Resume:  python scripts/make_resume_spool.py
         python -m qapf.governor /dev/null --log research/results/RAW/master/governor.jsonl --max-workers 3 \
             --spool research/results/RAW/master/spool_resume.jsonl --forever --stop-file research/results/RAW/master/STOP
"""
from __future__ import annotations

import json
import os
import shlex

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "research", "results", "RAW")
M = os.path.join(RAW, "master")

# decision-value order (lower first)
ORDER = [("nmr_sparse_scaling.py", 0), ("g1_transmission.py", 1), ("nmr_circuit_pop.py", 2), ("nmr_embed.py", 2),
         ("nmr_gate.py", 3), ("g1_mode_census.py", 4), ("g1_sample_crop.py", 5), ("tpt_crop.py", 6),
         ("synthetic_lab.py", 7)]


def opts(cmd):
    t = shlex.split(cmd)
    o = {}
    for i, x in enumerate(t):
        if x.startswith("--"):
            o[x[2:]] = t[i + 1] if i + 1 < len(t) and not t[i + 1].startswith("--") else "1"
    return t, o


def out_path(cmd):
    t, o = opts(cmd)
    script = next((os.path.basename(x) for x in t if x.endswith(".py")), None)
    g = lambda k, d=None: o.get(k, d)
    if script == "nmr_gate.py":
        hn = "HN" if g("hn-only", "0") == "1" else ""
        tag = f"{g('pdb','1UBQ')}{hn}_p{g('probe')}_N{g('N','14')}_o{g('orient','0')}_g{int(float(g('gamma','0')))}"
        return script, tag, os.path.join(ROOT, g("out", "research/results/RAW/nmr_gate"), tag + ".json")
    if script == "nmr_sparse_scaling.py":
        tag = f"{g('pdb','1UBQ')}_p{g('probe')}_N{g('N')}_o{g('orient','0')}_g{int(float(g('gamma','0')))}"
        return script, tag, os.path.join(RAW, "nmr_sparse", tag + ".json")
    if script == "nmr_embed.py":
        tag = f"{g('pdb','1UBQ')}_p{g('probe')}_core{g('Ncore','10')}_o{g('orient','0')}"
        return script, tag, os.path.join(RAW, "nmr_embed", tag + ".json")
    if script == "nmr_circuit_pop.py":
        tag = f"{g('pdb','1UBQ')}_p{g('probe','19')}_N{g('N','10')}_o{g('orient','0')}"
        return script, tag, os.path.join(RAW, "nmr_pop", tag + ".json")
    if script == "g1_transmission.py":
        return script, g("crop"), os.path.join(RAW, "g1_transmission", g("crop") + ".json")
    if script == "g1_mode_census.py":
        tag = f"{g('crop')}_R{g('restarts','256')}_s{g('seed','0')}"
        return script, tag, os.path.join(ROOT, g("out", "research/results/RAW/g1_modes"), tag + ".json")
    if script == "g1_sample_crop.py":
        T = float(g("T", "1"))
        tag = f"{g('crop')}_T{T:g}_s{g('seed','0')}"
        return script, tag, os.path.join(ROOT, g("out", "research/results/RAW/g1"), tag + ".json")
    if script == "tpt_crop.py":
        tag = f"{g('crop')}_R{g('rungs','24')}_s{g('seed','0')}"
        return script, tag, os.path.join(ROOT, g("out", "research/results/RAW/tpt"), tag + ".json")
    if script == "synthetic_lab.py":
        tag = f"{g('family')}_n{g('nmin','6')}-{g('nmax','14')}"
        return script, tag, os.path.join(ROOT, g("out", "research/results/RAW/synthetic"), tag + ".json")
    return script, None, None


def main():
    cancel = set(open(os.path.join(M, "cancel.txt")).read().split()) if os.path.exists(os.path.join(M, "cancel.txt")) else set()
    seen_out, jobs, skipped = set(), [], {"done": 0, "cancelled": 0, "dup": 0, "other": 0}
    for line in open(os.path.join(M, "spool.jsonl"), encoding="utf-8"):
        line = line.strip()
        if not line:
            continue
        try:
            d = json.loads(line)
        except json.JSONDecodeError:
            continue
        script, tag, path = out_path(d["cmd"])
        if path is None:
            skipped["other"] += 1; continue
        if os.path.exists(path):
            skipped["done"] += 1; continue
        if tag in cancel:
            skipped["cancelled"] += 1; continue
        if path in seen_out:
            skipped["dup"] += 1; continue
        seen_out.add(path)
        rank = dict(ORDER).get(script, 9)
        # inside C2: gamma = 0 first, then ascending N (the decisive series)
        _, o = opts(d["cmd"])
        sub = (float(o.get("gamma", 0)) > 0, int(o.get("N", 0))) if script == "nmr_sparse_scaling.py" else (0, 0)
        jobs.append((rank, sub, len(jobs), dict(name="r_" + d["name"], cmd=d["cmd"], ram_gb=d.get("ram_gb", 1.0),
                                                   threads=d.get("threads", 1))))
    jobs.sort(key=lambda x: (x[0], x[1], x[2]))
    with open(os.path.join(M, "spool_resume.jsonl"), "w", encoding="utf-8") as f:
        for *_, j in jobs:
            f.write(json.dumps(j) + "\n")
    from collections import Counter
    c = Counter(opts(j[3]["cmd"])[0][1].split("/")[-1] if False else next(x for x in shlex.split(j[3]["cmd"]) if x.endswith(".py")).split("/")[-1] for j in jobs)
    print("pending jobs:", len(jobs), dict(c))
    print("skipped:", skipped)


if __name__ == "__main__":
    main()
