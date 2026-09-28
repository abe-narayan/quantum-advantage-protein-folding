"""ROUND4 / allatom_superquadratic: PubMed (NCBI E-utilities) verification of the classical-twin literature that is not on
arXiv (Anton/Science/JACS/PNAS folding papers, enhanced-sampling efficiency papers).  Stores the verbatim PubMed
record (citation + abstract text) per query.  Checkpointed per query (atomic write; skipped on rerun).
Output: pubmed_raw/<key>.json, pubmed_records.json
"""
from __future__ import annotations

import json
import os
import time
import urllib.parse
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "pubmed_raw")
os.makedirs(RAW, exist_ok=True)
EU = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

Q = {
    "ll2011_fastfolders": "How fast-folding proteins fold[Title] AND Lindorff-Larsen[Author]",
    "piana2012_kinetics": "Protein folding kinetics and thermodynamics from atomistic simulation[Title]",
    "nguyen2014_gb_days": "Folding simulations for proteins with diverse topologies are accessible in days[Title]",
    "adhikari2019_we": "Computational estimation of microsecond to second atomistic folding times[Title]",
    "voelz2010_ntl9": "Molecular simulation of ab initio protein folding for a millisecond folder NTL9[Title]",
    "bowman2011_lambda": "Atomistic folding simulations of the five-helix bundle protein[Title]",
    "rest2_2011": "Replica exchange with solute scaling: a more efficient version of replica exchange with solute tempering[Title]",
    "rosta_hummer2009": "Error and efficiency of replica exchange molecular dynamics simulations[Title]",
    "nymeyer2008": "How efficient is replica exchange molecular dynamics? An analytic approach[Title]",
    "bioemu2025": "Scalable emulation of protein equilibrium ensembles with generative deep learning[Title]",
    "piana2011_villin": "How robust are protein folding simulations with respect to force field parameterization[Title]",
    "chaos_protein": "Chaos in protein dynamics[Title]",
    "lyap_protein2": "Lyapunov exponents[Title] AND (protein[Title] OR peptide[Title]) AND molecular dynamics",
    "we_review_zuckerman": "Weighted Ensemble Simulation: Review of Methodology, Applications, and Software[Title]",
    "msm_folding_review": "Markov state models: From an art to a science[Title]",
    "metad_folding_trpcage": "A bias-exchange approach to protein folding[Title]",
    "fah_exascale": "SARS-CoV-2 simulations go exascale to predict dramatic spike opening and cryptic pockets across the proteome[Title]",
    "lindorff_ntl9_ms": "Lindorff-Larsen K[Author] AND folding[Title] AND millisecond",
    "anton2_2014": "Anton 2: raising the bar for performance and programmability[Title]",
}


def get(url):
    for k in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return r.read().decode("utf-8")
        except Exception as e:  # noqa: BLE001
            err = e
            time.sleep(3 * (k + 1))
    raise RuntimeError(str(err))


def main():
    allr = {}
    for key, term in Q.items():
        path = os.path.join(RAW, key + ".json")
        if os.path.exists(path):
            d = json.load(open(path, encoding="utf-8"))
        else:
            s = json.loads(get(EU + "esearch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", term=term, retmax=3, retmode="json"))))
            ids = s["esearchresult"]["idlist"]
            time.sleep(0.6)
            txt = get(EU + "efetch.fcgi?" + urllib.parse.urlencode(dict(db="pubmed", id=",".join(ids), rettype="abstract", retmode="text"))) if ids else ""
            d = dict(key=key, term=term, pmids=ids, text=txt, fetched=time.strftime("%Y-%m-%dT%H:%M:%S"))
            tmp = path + ".tmp"
            json.dump(d, open(tmp, "w", encoding="utf-8"), indent=1)
            os.replace(tmp, path)
            time.sleep(0.6)
        allr[key] = d
        print(key, d["pmids"])
    tmp = os.path.join(HERE, "pubmed_records.json.tmp")
    json.dump(allr, open(tmp, "w", encoding="utf-8"), indent=1)
    os.replace(tmp, os.path.join(HERE, "pubmed_records.json"))


if __name__ == "__main__":
    main()
