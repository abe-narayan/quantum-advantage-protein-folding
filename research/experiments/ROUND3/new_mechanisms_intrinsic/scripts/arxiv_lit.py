"""arXiv API literature pass for lane new_mechanisms_intrinsic.

Queries export.arxiv.org (3.2 s between requests, per arXiv etiquette), stores the
raw entries (id, title, authors, published, journal_ref, doi, abstract) in
../lit/arxiv_raw.json and a compact human-readable dump in ../lit/abstracts.txt.
Everything cited as LITERATURE (verified) in README.md must appear in these files.

Usage: python arxiv_lit.py [--extra "label|query" ...]
"""
from __future__ import annotations

import json
import os
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

HERE = os.path.dirname(os.path.abspath(__file__))
LIT = os.path.join(HERE, "..", "lit")
NS = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}

SEARCHES = [
    ("nitrogenase_qc", 'abs:nitrogenase AND (abs:"phase estimation" OR abs:"fault-tolerant" OR abs:"quantum computer")'),
    ("oec", 'abs:"oxygen-evolving" OR abs:Mn4CaO5 OR abs:"oxygen evolving complex"'),
    ("fes_dmrg", '(abs:"iron-sulfur" OR abs:"iron sulfur" OR abs:"Fe-S cluster") AND (abs:DMRG OR abs:"quantum computer" OR abs:"renormalization group")'),
    ("porphyrin_spin", 'abs:porphyrin AND abs:spin AND (abs:AFQMC OR abs:DMRG OR abs:"coupled cluster" OR abs:"quantum computer" OR abs:"Monte Carlo")'),
    ("spin_state_bench", 'abs:"spin-state energetics" OR abs:"spin state energetics"'),
    ("forces_qpe", '(abs:"energy gradients" OR abs:"molecular forces" OR abs:"nuclear gradients") AND abs:quantum AND (abs:"fault-tolerant" OR abs:"phase estimation" OR abs:"quantum algorithm")'),
    ("cu2o2", 'abs:"bis(mu-oxo)" OR abs:Cu2O2 OR abs:"side-on peroxo" OR abs:"bis-mu-oxo"'),
    ("protonation_qc", 'abs:protonation AND abs:"quantum computer"'),
    ("metalloenzyme_qc", '(abs:metalloenzyme OR abs:metalloprotein OR abs:cofactor) AND abs:"quantum comput" AND (abs:resource OR abs:"fault-tolerant")'),
    ("pcluster", 'abs:"P-cluster" AND abs:nitrogenase'),
    ("femoco_2026", 'abs:FeMoco OR abs:"FeMo-cofactor" OR abs:"FeMo cofactor"'),
    ("qmmm_region", 'abs:"QM/MM" AND (abs:"QM region" OR abs:"region size") AND abs:convergence'),
    ("afqmc_tm", 'abs:"auxiliary-field quantum Monte Carlo" AND (abs:"transition metal" OR abs:iron OR abs:copper)'),
    ("nqe_enzyme", '(abs:"nuclear quantum effects" OR abs:"proton delocalization" OR abs:"low-barrier hydrogen bond") AND (abs:enzyme OR abs:protein)'),
    ("heme_qc", '(abs:heme OR abs:cytochrome) AND abs:"quantum comput"'),
]

ID_LIST = [
    "2502.15882",  # Low et al., spectrum amplification
    "2111.12437",  # O'Brien et al., molecular forces (to verify)
    "2203.15291",  # Tazhigulov et al., Sycamore correlated molecules (to verify)
    "2405.05068",  # Robledo-Moreno et al., SQD Fe-S (to verify)
    "2202.01244",  # Goings et al., P450
    "2601.04621",  # Zhai et al., FeMoco classical
    "2011.03494",  # Lee et al., THC
    "1809.10307",  # Li et al., FeMoco electronic complexity
    "2208.02199",  # Lee et al., exponential advantage evidence
]


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "qapf-research/0.1 (lane new_mechanisms_intrinsic)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def parse(xml: bytes, label: str) -> list[dict]:
    root = ET.fromstring(xml)
    out = []
    for e in root.findall("a:entry", NS):
        idurl = (e.findtext("a:id", default="", namespaces=NS) or "").strip()
        if not idurl or "api/errors" in idurl:
            continue
        out.append({
            "label": label,
            "id": idurl.rsplit("/abs/", 1)[-1],
            "title": " ".join((e.findtext("a:title", default="", namespaces=NS) or "").split()),
            "authors": [a.findtext("a:name", default="", namespaces=NS) for a in e.findall("a:author", NS)],
            "published": e.findtext("a:published", default="", namespaces=NS),
            "journal_ref": e.findtext("arxiv:journal_ref", default="", namespaces=NS),
            "doi": e.findtext("arxiv:doi", default="", namespaces=NS),
            "abstract": " ".join((e.findtext("a:summary", default="", namespaces=NS) or "").split()),
        })
    return out


def main() -> None:
    extra = []
    args = sys.argv[1:]
    if args and args[0] == "--extra":
        for s in args[1:]:
            lab, q = s.split("|", 1)
            extra.append((lab, q))
    raw_path = os.path.join(LIT, "arxiv_raw.json")
    store: dict = {}
    if os.path.exists(raw_path):
        with open(raw_path, encoding="utf-8") as f:
            store = json.load(f)
    todo = extra if extra else SEARCHES
    for lab, q in todo:
        if lab in store and not extra:
            continue
        url = ("https://export.arxiv.org/api/query?search_query=" + urllib.parse.quote(q)
               + "&start=0&max_results=25&sortBy=relevance&sortOrder=descending")
        try:
            store[lab] = {"query": q, "entries": parse(fetch(url), lab)}
        except Exception as ex:  # keep going; record the failure
            store[lab] = {"query": q, "error": repr(ex), "entries": []}
        time.sleep(3.2)
    if not extra and "id_list" not in store:
        url = "https://export.arxiv.org/api/query?id_list=" + ",".join(ID_LIST) + "&max_results=50"
        try:
            store["id_list"] = {"query": "id_list", "entries": parse(fetch(url), "id_list")}
        except Exception as ex:
            store["id_list"] = {"query": "id_list", "error": repr(ex), "entries": []}
    tmp = raw_path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(store, f, indent=1)
    os.replace(tmp, raw_path)
    with open(os.path.join(LIT, "abstracts.txt"), "w", encoding="utf-8") as f:
        for lab, blk in store.items():
            f.write(f"\n===== [{lab}] {blk['query']}  ({len(blk['entries'])} entries{'; ERROR ' + blk['error'] if 'error' in blk else ''})\n")
            for e in blk["entries"]:
                au = ", ".join(e["authors"][:4]) + (" et al." if len(e["authors"]) > 4 else "")
                f.write(f"\n- {e['id']} | {e['published'][:10]} | {e['title']} | {au} | {e['journal_ref']} | doi:{e['doi']}\n  {e['abstract']}\n")
    print({k: len(v["entries"]) for k, v in store.items()})


if __name__ == "__main__":
    main()
