"""ROUND4 / allatom_superquadratic: arXiv API survey (2019-2026) of quantum algorithm families claimed to speed up
classical MD, Liouville / Fokker-Planck / Kolmogorov evolution, Gibbs sampling of classical potentials, or
free-energy / rate estimation.

Every record saved here comes verbatim from export.arxiv.org (title, authors, dates, abstract, journal_ref).
Nothing is paraphrased at this stage.  Checkpointed: each query's parsed result is written atomically to
raw/<key>.json and skipped on rerun.  3.5 s between API calls (arXiv etiquette).

Output: raw/*.json, records.json (deduplicated union), queries.json.
"""
from __future__ import annotations

import json
import os
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
DATE = "submittedDate:[201901010000 TO 202612312359]"

# key -> (search_query or None, id_list or None, max_results)
QUERIES = {
    # --- nonlinear ODE embeddings
    "carleman": ('abs:Carleman AND abs:quantum AND abs:nonlinear', None, 60),
    "carleman_nodiss": ('abs:Carleman AND abs:quantum AND (abs:dissipative OR abs:conservative OR abs:"non-dissipative")', None, 40),
    "nonlinear_ode_qalg": ('ti:quantum AND ti:nonlinear AND (ti:"differential equations" OR ti:dynamics) AND abs:algorithm', None, 60),
    "koopman_vn": ('(abs:"Koopman-von Neumann" OR abs:"Koopman von Neumann" OR ti:Koopman) AND abs:quantum AND abs:classical', None, 50),
    "liouville_qalg": ('(ti:Liouville OR abs:"Liouville equation") AND abs:"quantum algorithm" AND abs:nonlinear', None, 40),
    "level_set_obs": ('abs:"quantum algorithms" AND abs:observables AND abs:nonlinear AND abs:"partial differential"', None, 30),
    "chaos_limits": ('abs:quantum AND abs:Lyapunov AND abs:nonlinear AND (abs:algorithm OR abs:algorithms) AND abs:chaotic', None, 30),
    # --- stochastic / Fokker-Planck / Langevin
    "fokker_planck": ('(ti:"Fokker-Planck" OR ti:"Fokker Planck" OR ti:Kolmogorov) AND abs:quantum AND (abs:algorithm OR abs:computer OR abs:computing)', None, 40),
    "langevin_q": ('ti:Langevin AND ti:quantum AND (abs:algorithm OR abs:sampling)', None, 40),
    "sde_q": ('ti:stochastic AND ti:"differential equations" AND ti:quantum', None, 30),
    "gibbs_continuous": ('(abs:"non-logconcave" OR abs:"non-log-concave" OR abs:"continuous potentials" OR abs:"Witten Laplacian") AND abs:quantum AND abs:sampling', None, 40),
    "linear_ode_nonunitary": ('(abs:"non-unitary" OR abs:"linear combination of Hamiltonian simulation") AND abs:quantum AND abs:"differential equations"', None, 30),
    # --- oscillators
    "oscillators": ('abs:"coupled classical oscillators" OR (abs:oscillators AND abs:"exponential quantum speedup")', None, 40),
    "anharmonic": ('abs:anharmonic AND abs:"classical" AND abs:oscillators AND abs:quantum AND (abs:algorithm OR abs:speedup)', None, 40),
    # --- MD / proteins / MSM / free energy
    "md_quantum_alg": ('(ti:"molecular dynamics" OR abs:"classical molecular dynamics") AND abs:"quantum algorithm"', None, 50),
    "md_quantum_comp": ('ti:"molecular dynamics" AND (ti:"quantum computer" OR ti:"quantum computing" OR ti:"quantum computers")', None, 40),
    "msm_quantum": ('(abs:"Markov state model" OR abs:"Markov state models") AND abs:quantum AND (abs:walk OR abs:computer OR abs:algorithm OR abs:annealer)', None, 40),
    "rare_transitions": ('abs:"rare" AND abs:transitions AND abs:"quantum computer" AND (abs:protein OR abs:conformational OR abs:molecular)', None, 30),
    "free_energy_q": ('ti:"free energy" AND (ti:quantum) AND (abs:algorithm OR abs:"amplitude estimation" OR abs:speedup)', None, 40),
    "partition_fn_q": ('ti:"partition function" AND ti:quantum AND abs:algorithm', None, 30),
    "protein_folding_md_q": ('abs:"protein folding" AND abs:quantum AND (abs:"molecular dynamics" OR abs:Langevin OR abs:kinetics)', None, 60),
    "rates_committor_q": ('(abs:committor OR abs:"transition rate" OR abs:"reaction rate" OR abs:"first passage") AND abs:"quantum algorithm"', None, 30),
    "nonreversible_q": ('abs:quantum AND abs:"nonreversible" AND abs:Markov', None, 20),
    # --- classical twin (arXiv-hosted only)
    "we_folding": ('abs:"weighted ensemble" AND (abs:folding OR abs:protein)', None, 40),
    "boltzmann_gen": ('ti:"Boltzmann generators" OR (abs:"Boltzmann generator" AND abs:protein)', None, 30),
    "bioemu": ('abs:"protein equilibrium ensembles" AND abs:generative', None, 20),
    "fast_folding_ml": ('abs:"fast-folding proteins" OR abs:"fast folding proteins"', None, 40),
    "rest2": ('(abs:"solute tempering" OR abs:REST2) AND abs:protein', None, 30),
    "anton": ('abs:Anton AND abs:"molecular dynamics" AND (abs:microseconds OR abs:millisecond OR abs:machine)', None, 30),
    "lyapunov_md": ('abs:Lyapunov AND abs:"molecular dynamics" AND (abs:protein OR abs:water OR abs:liquid)', None, 30),
    # --- specific IDs to verify
    "ids_core": (None, "2011.03185,2202.01054,2303.13012,2307.09593,2303.01029,1701.03684,quant-ph/0508139,1504.06987,"
                       "2505.05301,2501.05868,2608.24527,2210.06539,2310.11445,2210.08104,1812.01729,2302.01170,"
                       "2202.07834,2202.02188,2011.06571,2312.09518,2405.12714,2011.04149", 40),
}


def fetch(q, ids, n):
    params = {"max_results": str(n), "sortBy": "relevance"}
    if q:
        params["search_query"] = f"({q}) AND {DATE}"
    if ids:
        params["id_list"] = ids
    url = "https://export.arxiv.org/api/query?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return url, r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001
            time.sleep(5 * (attempt + 1))
            err = str(e)
    raise RuntimeError(err)


def parse(xml):
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", NS):
        g = lambda t: (e.find(t, NS).text or "").strip() if e.find(t, NS) is not None else ""  # noqa: E731
        aid = g("a:id").split("/abs/")[-1]
        out.append(dict(id=aid, title=" ".join(g("a:title").split()), published=g("a:published")[:10],
                        updated=g("a:updated")[:10], authors=[a.find("a:name", NS).text for a in e.findall("a:author", NS)],
                        abstract=" ".join(g("a:summary").split()), journal_ref=g("arxiv:journal_ref"),
                        primary=(e.find("arxiv:primary_category", NS).attrib.get("term") if e.find("arxiv:primary_category", NS) is not None else "")))
    return out


def main():
    allrec = {}
    for key, (q, ids, n) in QUERIES.items():
        path = os.path.join(RAW, key + ".json")
        if os.path.exists(path):
            recs = json.load(open(path, encoding="utf-8"))["records"]
        else:
            url, xml = fetch(q, ids, n)
            recs = parse(xml)
            tmp = path + ".tmp"
            json.dump(dict(key=key, url=url, fetched=time.strftime("%Y-%m-%dT%H:%M:%S"), records=recs), open(tmp, "w", encoding="utf-8"), indent=1)
            os.replace(tmp, path)
            time.sleep(3.5)
        print(f"{key:22s} {len(recs):3d}")
        for r in recs:
            base = re.sub(r"v\d+$", "", r["id"])
            allrec.setdefault(base, dict(r, queries=[]))["queries"].append(key)
    tmp = os.path.join(HERE, "records.json.tmp")
    json.dump(allrec, open(tmp, "w", encoding="utf-8"), indent=1)
    os.replace(tmp, os.path.join(HERE, "records.json"))
    json.dump({k: dict(q=v[0], ids=v[1], n=v[2]) for k, v in QUERIES.items()}, open(os.path.join(HERE, "queries.json"), "w"), indent=1)
    print("unique records", len(allrec))


if __name__ == "__main__":
    main()
