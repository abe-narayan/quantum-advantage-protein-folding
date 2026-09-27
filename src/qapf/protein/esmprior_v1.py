"""Vendored copy of the predecessor's learned structure prior esmprior_v1 (S33-A40), frozen for this program.

PROVENANCE
    Source: C:/Users/abena/cvar-vqe-protein-folding-v3, s33/esmprior.py (last commit touching it c113a29e;
    repo pinned at 3d5b2d25 for the S29-S33 import).  Model files copied to data/models/esmprior_v1/ with SHA-256 in
    data/models/esmprior_v1/SHA256.json.  Network definition, pair_inputs, bins and the ESM featuriser (bf16, 24
    APC-symmetrised heads listed in heads.json) are copied verbatim in behaviour; only paths and the ESM loader differ
    (fair-esm local checkpoint instead of the predecessor's meta-device loader).  `verify_against_cache()` checks the
    featuriser + predictor reproduce the predecessor's cached features/predictions.

TRAINING / LEAKAGE (from the source docstring and data/models/esmprior_v1/train_log.json): trained on 600 crops
    (6 shards x 100) of 40-72 aa (maxL 72) from prots/ chains, excluding long40 / tuning126 / mid30 related chains.
    ESM-2 itself was pre-trained on UniRef50 (not controlled).  Any target used for ACCURACY claims must not overlap
    the training crops (see qapf.protein.targets for the exclusion list).

OUTPUT of predict(): dict with prob (L,L,28) CA-distance bin probabilities, prob_cb, theta_tau_prob (L,9,24), etc.
"""
from __future__ import annotations

import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
MODEL_DIR = os.path.join(ROOT, "data", "models", "esmprior_v1")
ESM_CKPT = os.path.expanduser("~/.cache/torch/hub/checkpoints/esm2_t33_650M_UR50D.pt")

EDGES = np.concatenate([np.arange(4.0, 20.0 + 1e-9, 1.0), np.arange(22.0, 40.0 + 1e-9, 2.0)])  # 27 edges
NB = len(EDGES) + 1  # 28 bins
BINS = np.concatenate([[0.0], EDGES, [np.inf]])
CENTRES = np.concatenate([[3.8], (EDGES[:-1] + EDGES[1:]) / 2.0, [42.0]])
TH_EDGES = np.arange(80.0, 150.0 + 1e-9, 10.0)
TA_EDGES = np.arange(-180.0, 180.0 + 1e-9, 15.0)
NTH, NTA = len(TH_EDGES) + 1, len(TA_EDGES) - 1
TH_CENTRES = np.concatenate([[75.0], (TH_EDGES[:-1] + TH_EDGES[1:]) / 2.0, [155.0]])
TA_CENTRES = (TA_EDGES[:-1] + TA_EDGES[1:]) / 2.0
K_HEADS = 24
MAXSEP = 32


def virtual_cb(ca):
    ca = np.asarray(ca, np.float64)
    cb = ca.copy()
    if len(ca) < 3:
        return cb
    b1 = ca[1:-1] - ca[:-2]; b2 = ca[2:] - ca[1:-1]
    u1 = b1 / np.linalg.norm(b1, axis=1, keepdims=True); u2 = b2 / np.linalg.norm(b2, axis=1, keepdims=True)
    m = u1 - u2; m /= np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)
    n = np.cross(u1, u2); n /= np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-9)
    t = u1 + u2; t /= np.maximum(np.linalg.norm(t, axis=1, keepdims=True), 1e-9)
    cb[1:-1] = ca[1:-1] + 1.0977 * m - 0.9601 * n + 0.1616 * t
    return cb


def theta_tau(ca):
    """CA virtual angles theta_i (i=1..L-2) and dihedrals tau_i (i=1..L-3), degrees; length-L arrays, NaN elsewhere."""
    ca = np.asarray(ca, np.float64)
    L = len(ca)
    th = np.full(L, np.nan); ta = np.full(L, np.nan)
    if L >= 3:
        a = ca[:-2] - ca[1:-1]; b = ca[2:] - ca[1:-1]
        c = (a * b).sum(1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1))
        th[1:-1] = np.degrees(np.arccos(np.clip(c, -1, 1)))
    if L >= 4:
        b0 = ca[1:-2] - ca[:-3]; b1 = ca[2:-1] - ca[1:-2]; b2 = ca[3:] - ca[2:-1]
        n1 = np.cross(b0, b1); n2 = np.cross(b1, b2)
        m1 = np.cross(n1, b1 / np.linalg.norm(b1, axis=1, keepdims=True))
        x = (n1 * n2).sum(1); y = (m1 * n2).sum(1)
        ta[1:-2] = -np.degrees(np.arctan2(y, x))   # IUPAC sign: alpha helix ~ +50 deg
    return th, ta


def build_model(cfg):
    import torch
    import torch.nn as nn
    import torch.nn.functional as F

    C = cfg.get("C", 48)
    R = cfg.get("R", 64)
    dil = cfg.get("dilations", [1, 2, 4, 8, 1, 2, 4, 8])
    npair_in = 2 + K_HEADS + (MAXSEP + 1) + 1

    class Block(nn.Module):
        def __init__(self, d):
            super().__init__()
            self.n1 = nn.GroupNorm(8, C); self.c1 = nn.Conv2d(C, C, 3, padding=d, dilation=d)
            self.n2 = nn.GroupNorm(8, C); self.c2 = nn.Conv2d(C, C, 3, padding=d, dilation=d)

        def forward(self, x):
            h = self.c1(F.elu(self.n1(x)))
            h = self.c2(F.elu(self.n2(h)))
            return x + h

    class PriorNet(nn.Module):
        def __init__(self):
            super().__init__()
            self.rin = nn.Sequential(nn.LayerNorm(1280), nn.Linear(1280, R), nn.GELU())
            self.r1d = nn.Conv1d(R, R, 5, padding=2)
            self.pa = nn.Linear(R, C); self.pb = nn.Linear(R, C)
            self.oa = nn.Linear(R, 8); self.ob = nn.Linear(R, 8)
            self.pin = nn.Conv2d(npair_in + 64, C, 1)
            self.blocks = nn.ModuleList([Block(d) for d in dil])
            self.nf = nn.GroupNorm(8, C)
            self.hca = nn.Conv2d(C, NB, 1)
            self.hcb = nn.Conv2d(C, NB, 1)
            self.htt = nn.Sequential(nn.Linear(R + 3 * C, 128), nn.GELU(), nn.Linear(128, NTH * NTA))

        def forward(self, rep, pair_in):
            L = rep.shape[0]
            h = self.rin(rep)
            h = h + F.gelu(self.r1d(h.t()[None]))[0].t()
            a = self.pa(h); b = self.pb(h)
            oa = self.oa(h); ob = self.ob(h)
            outer = torch.einsum("ip,jq->pqij", oa, ob).reshape(64, L, L)
            x = self.pin(torch.cat([pair_in, outer], 0)[None])[0] + a.t()[:, :, None] + b.t()[:, None, :]
            x = x[None]
            for blk in self.blocks:
                x = blk(x)
            x = F.elu(self.nf(x))[0]
            xs = 0.5 * (x + x.transpose(1, 2))
            lca = self.hca(xs[None])[0].permute(1, 2, 0)
            lcb = self.hcb(xs[None])[0].permute(1, 2, 0)
            if L >= 4:
                i = torch.arange(1, L - 2)
                f = torch.cat([h[i], x[:, i - 1, i + 1].t(), x[:, i - 1, i + 2].t(), x[:, i, i + 2].t()], 1)
                ltt = self.htt(f)
            else:
                ltt = torch.zeros(0, NTH * NTA)
            return lca, lcb, ltt

    return PriorNet()


def pair_inputs(L, con, att, norm=None):
    con = np.asarray(con, np.float32)
    p = np.clip(con, 1e-4, 1 - 1e-4)
    S = np.abs(np.arange(L)[:, None] - np.arange(L)[None])
    oh = np.zeros((MAXSEP + 1, L, L), np.float32)
    Sc = np.minimum(S, MAXSEP)
    oh[Sc, np.arange(L)[:, None], np.arange(L)[None]] = 1.0
    att = np.asarray(att, np.float32).reshape(K_HEADS, L, L)
    raw = np.concatenate([np.log(p / (1 - p))[None], con[None], att], 0)
    if norm is not None:
        mu, sd = np.asarray(norm[0], np.float32), np.asarray(norm[1], np.float32)
        raw = (raw - mu[:, None, None]) / sd[:, None, None]
    return np.concatenate([raw, oh, np.log1p(S)[None].astype(np.float32) / 4.0], 0).astype(np.float32)


_M = {}


def load_model():
    if "net" in _M:
        return _M["net"]
    import torch
    cfg = json.load(open(os.path.join(MODEL_DIR, "config.json")))
    net = build_model(cfg)
    sd = torch.load(os.path.join(MODEL_DIR, "model.pt"), map_location="cpu", weights_only=True)
    net.load_state_dict(sd)
    net.eval()
    _M["net"] = (net, cfg)
    return _M["net"]


def _softmax(x, axis=-1):
    x = x - x.max(axis, keepdims=True)
    e = np.exp(x)
    return e / e.sum(axis, keepdims=True)


def predict(seq, feats):
    """feats = dict(rep (L,1280), con (L,L), att (24,L,L)) from featurise()."""
    import torch
    L = len(seq)
    net, cfg = load_model()
    rep = torch.as_tensor(np.asarray(feats["rep"], np.float32))
    pin = torch.as_tensor(pair_inputs(L, feats["con"], feats["att"], (cfg["pin_mu"], cfg["pin_sd"])))
    with torch.no_grad():
        lca, lcb, ltt = net(rep, pin)
    P = _softmax(lca.numpy().astype(np.float64), -1)
    Pb = _softmax(lcb.numpy().astype(np.float64), -1)
    tt = np.full((L, NTH * NTA), 1.0 / (NTH * NTA))
    if L >= 4:
        tt[1:L - 2] = _softmax(ltt.numpy().astype(np.float64), -1)
    S = np.abs(np.arange(L)[:, None] - np.arange(L)[None])
    near = S < 2
    P[near] = 0.0; P[near, 0] = 1.0
    Pb[near] = 0.0; Pb[near, 0] = 1.0
    E = (P * CENTRES).sum(-1)
    sd = np.sqrt(np.maximum((P * CENTRES ** 2).sum(-1) - E ** 2, 0))
    k8 = int(np.where(EDGES == 8.0)[0][0]) + 1
    return dict(prob=P.astype(np.float32), prob_cb=Pb.astype(np.float32), expected=E.astype(np.float32),
                sd=sd.astype(np.float32), contact_prob=Pb[..., :k8].sum(-1).astype(np.float32),
                theta_tau_prob=tt.reshape(L, NTH, NTA).astype(np.float32), model="esmprior_v1")


# ------------------------------------------------------------------ ESM-2 650M featuriser (bf16, as the predecessor)
_E = {}


def load_esm(threads=4):
    if "esm" in _E:
        return _E["esm"]
    import re
    import torch
    import esm
    from esm.model.esm2 import ESM2
    torch.set_num_threads(threads)
    # predecessor's loader (s33/VERIFICATION/map_learned_esm_run.py): mmap + meta-device construction; the official
    # fair-esm checkpoint is trusted (SHA-256 recorded in data/models/esmprior_v1/SHA256.json) -> weights_only=False.
    md = torch.load(ESM_CKPT, mmap=True, map_location="cpu", weights_only=False)
    rd = torch.load(ESM_CKPT.replace(".pt", "-contact-regression.pt"), map_location="cpu", weights_only=False)
    cfg = md["cfg"]["model"]
    pat = re.compile("^" + "|".join(["encoder.sentence_encoder.", "encoder."]))
    sd = {pat.sub("", k): v for k, v in md["model"].items()}
    sd.update(rd["model"])
    alphabet = esm.data.Alphabet.from_architecture("ESM-1b")
    with torch.device("meta"):
        model = ESM2(num_layers=cfg.encoder_layers, embed_dim=cfg.encoder_embed_dim,
                     attention_heads=cfg.encoder_attention_heads, alphabet=alphabet, token_dropout=cfg.token_dropout)
    model.load_state_dict(sd, strict=False, assign=True)
    model.lm_head.weight = model.embed_tokens.weight
    model = model.to(torch.bfloat16).eval()
    heads = json.load(open(os.path.join(MODEL_DIR, "heads.json")))["heads"]
    _E["esm"] = (model, alphabet, alphabet.get_batch_converter(), heads)
    return _E["esm"]


def unload_esm():
    _E.clear()
    import gc
    gc.collect()


def featurise(seq, threads=4):
    """ESM-2 650M features exactly as the predecessor's P_prior_featurise.featurise_one (bf16)."""
    import torch
    model, alphabet, bc, heads = load_esm(threads)
    n = len(seq)
    _, _, toks = bc([("p", seq)])
    with torch.no_grad():
        out = model(toks, repr_layers=[model.num_layers], need_head_weights=True, return_contacts=True)
        rep = out["representations"][model.num_layers][0, 1:n + 1].float().numpy()
        con = out["contacts"][0, :n, :n].float().numpy()
        A = out["attentions"][0][:, :, 1:n + 1, 1:n + 1].float().reshape(-1, n, n)
        A = A + A.transpose(-1, -2)
        a1 = A.sum(-1, keepdim=True); a2 = A.sum(-2, keepdim=True); a12 = A.sum((-1, -2), keepdim=True)
        A = A - a1 * a2 / a12
        att = A[heads].numpy()
    return dict(rep=rep.astype(np.float16), con=con.astype(np.float16), att=att.astype(np.float16))
