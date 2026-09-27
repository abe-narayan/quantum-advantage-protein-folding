"""Target instruments for the quantum-advantage discovery sprint.

LADDER instrument (new, this program): leakage-screened PDB chains of 160-280 residues from the predecessor's prots/
corpus, cropped to contiguous windows of L in LADDER_L.  Screening (against the 600 esmprior_v1 training crops, which
are the only structures the learned energy saw in training):
    R1  PDB id of any training crop              -> excluded
    R2  shares any 9-mer with a training crop     -> excluded
    R3  gapless 30-residue window identity >= 0.4 with any training crop -> excluded
    also excluded: any chain sharing a 9-mer with long40 / mid30 / tuning126 targets (keeps instruments disjoint).
ESM-2 itself saw UniRef50 (uncontrolled), stated as a caveat.

The native CA coordinates of each crop are the crop's coordinates inside the full chain (as in esmprior training).
"""
from __future__ import annotations

import glob
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
PRED = "C:/Users/abena/cvar-vqe-protein-folding-v3"
LADDER_L = (30, 45, 60, 80, 100, 120, 150)
AA3 = dict(ALA="A", ARG="R", ASN="N", ASP="D", CYS="C", GLN="Q", GLU="E", GLY="G", HIS="H", ILE="I", LEU="L",
           LYS="K", MET="M", PHE="F", PRO="P", SER="S", THR="T", TRP="W", TYR="Y", VAL="V", MSE="M")


def parse_ca_chains(path):
    """First model only; returns {chain: (seq, CA (n,3), resnums)} for standard residues with a CA."""
    chains = {}
    with open(path, errors="ignore") as f:
        for line in f:
            if line.startswith("ENDMDL"):
                break
            if not (line.startswith("ATOM") or line.startswith("HETATM")):
                continue
            if line[12:16].strip() != "CA":
                continue
            alt = line[16]
            if alt not in (" ", "A"):
                continue
            rn = line[17:20].strip()
            if rn not in AA3:
                continue
            ch = line[21]
            try:
                resi = int(line[22:26]); icode = line[26]
                xyz = (float(line[30:38]), float(line[38:46]), float(line[46:54]))
            except ValueError:
                continue
            c = chains.setdefault(ch, dict(seq=[], ca=[], res=[]))
            key = (resi, icode)
            if c["res"] and c["res"][-1] == key:
                continue
            c["seq"].append(AA3[rn]); c["ca"].append(xyz); c["res"].append(key)
    return {k: ("".join(v["seq"]), np.array(v["ca"], float), v["res"]) for k, v in chains.items()}


def training_crops():
    ds = json.load(open(os.path.join(PRED, "s33", "ARTIFACTS", "esm_train", "dataset.json")))
    crops = {c["id"]: c for c in ds["crops"]}
    used = []
    for f in sorted(glob.glob(os.path.join(PRED, "s33", "ARTIFACTS", "esm_train", "shard_*.npz"))):
        z = np.load(f, allow_pickle=True)
        for i in z["ids"]:
            used.append(crops[int(i)])
    return used


def instrument_seqs():
    seqs = []
    d = os.path.join(PRED, "s33", "ARTIFACTS", "esm_train", "targets")
    for f in glob.glob(os.path.join(d, "*.npz")):
        seqs.append(str(np.load(f)["seq"]))
    return seqs


def kmers(s, k):
    return {s[i:i + k] for i in range(len(s) - k + 1)}


def max_gapless_identity(a, b, w=30):
    """max over all gapless alignments of a w-window of a against a w-window of b of fractional identity."""
    if len(a) < w or len(b) < w:
        return 0.0
    A = np.frombuffer(a.encode(), np.uint8); B = np.frombuffer(b.encode(), np.uint8)
    best = 0.0
    for off in range(-(len(B) - w), len(A) - w + 1):
        i0, j0 = max(0, off), max(0, -off)
        n = min(len(A) - i0, len(B) - j0)
        if n < w:
            continue
        eq = (A[i0:i0 + n] == B[j0:j0 + n]).astype(np.int32)
        c = np.convolve(eq, np.ones(w, np.int32), "valid")
        best = max(best, c.max() / w)
        if best >= 0.4:
            return best
    return best


def chain_ok(seq, ca):
    if len(seq) < 160 or len(seq) > 280:
        return False
    d = np.linalg.norm(np.diff(ca, axis=0), axis=1)
    return bool(np.all((d > 3.6) & (d < 4.0)))          # contiguous, no chain breaks / cis-anomalies


def helix_fraction(ca):
    from qapf.protein.esmprior_v1 import theta_tau
    th, ta = theta_tau(ca)
    ok = np.isfinite(th) & np.isfinite(ta)
    return float(np.mean((ta[ok] > 30) & (ta[ok] < 70) & (th[ok] > 80) & (th[ok] < 100)))


def select_ladder(n_target=16, seed=0, max_files=None, log=print):
    rng = np.random.default_rng(seed)
    used = training_crops()
    tr_ids = {c["pdb"].upper() for c in used}
    tr_seqs = [c["seq"] for c in used]
    tr9 = set().union(*[kmers(s, 9) for s in tr_seqs])
    inst9 = set().union(*[kmers(s, 9) for s in instrument_seqs()])
    files = sorted(glob.glob(os.path.join(PRED, "prots", "*.pdb")))
    rng.shuffle(files)
    if max_files:
        files = files[:max_files]
    picked, seen_seq, n_scan = [], [], 0
    for f in files:
        pid = os.path.basename(f)[:-4].upper()
        if pid in tr_ids:
            continue
        n_scan += 1
        try:
            chains = parse_ca_chains(f)
        except Exception:
            continue
        for ch, (seq, ca, res) in chains.items():
            if not chain_ok(seq, ca):
                continue
            k9 = kmers(seq, 9)
            if k9 & tr9 or k9 & inst9:
                continue
            if any(len(k9 & kmers(s, 9)) for s in seen_seq):
                continue                                   # keep picked chains mutually non-redundant
            if any(max_gapless_identity(seq, s) >= 0.4 for s in tr_seqs):
                continue
            if any(max_gapless_identity(seq, s) >= 0.4 for s in seen_seq):
                continue
            picked.append(dict(pdb=pid, chain=ch, L=len(seq), seq=seq, ca=ca.tolist(), helix_frac=helix_fraction(ca)))
            seen_seq.append(seq)
            log(f"picked {pid}:{ch} L={len(seq)} helix={picked[-1]['helix_frac']:.2f} (scanned {n_scan})")
            break
        if len(picked) >= n_target:
            break
    return picked, dict(n_scanned=n_scan, n_training_pdbs=len(tr_ids), n_training_crops=len(used))


def crop(entry, L, start=None):
    """Contiguous crop of length L; default start = centre of the chain."""
    n = entry["L"]
    s = (n - L) // 2 if start is None else start
    return dict(pdb=entry["pdb"], chain=entry["chain"], L=L, start=s, seq=entry["seq"][s:s + L],
                ca=np.asarray(entry["ca"], float)[s:s + L])
