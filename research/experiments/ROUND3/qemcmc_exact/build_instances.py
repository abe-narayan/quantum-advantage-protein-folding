"""ROUND3 lane qemcmc_exact: discretised instances of the A80 learned energy (DEP, native-free).

For one ladder crop (L = 30):
  1. x* = lowest-energy endpoint of a multistart L-BFGS census (R restarts drawn from the exact learned prior,
     200 iterations; the A80 decoder).  No native coordinates are read.
  2. Residue alphabets from the (theta, tau) prior head of each residue r = 1..L-3:
       state 0 = x*'s own (theta_r, tau_r);
       states 1..3 = centres of the most probable head bins whose tau centre is >= SEP deg (circular) from x*'s tau
       and from every previously chosen alternative (binary alphabet uses state 1 only).
     Residue order ("amb"): descending head probability of the best alternative (residues with a plausible
     alternative conformer first).  "rnd": a seeded random order (replicate family).
  3. Tables over 2^12 configurations (bit j <-> residue order[j] for the binary alphabet, bits (2j, 2j+1) <-> residue
     order[j] for the 4-state alphabet).  Nested instances: the n-qubit instance is the table restricted to indices
     < 2^n (higher residues pinned at x*).
       FROZEN : every other internal coordinate held at x*.
       RELAXED: every other internal coordinate relaxed by L-BFGS (ITERS) from x*, the 12 (or 6) alphabet residues
                pinned (their gradient components are zeroed, which keeps them fixed inside L-BFGS).

Outputs (atomic tmp+replace): instances/<crop>_xstar.npz, instances/<crop>_<order>_<alph>_<variant>.npz

Usage: python build_instances.py --crop 5O37A_30 [--relaxed] [--orders amb rnd] [--alphs 2 4]
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.protein import energy as EN  # noqa: E402
from qapf.sampling import hrex as H    # noqa: E402

OUT = os.path.join(HERE, "instances")
TH_CENTRES = np.array([75.0, 85.0, 95.0, 105.0, 115.0, 125.0, 135.0, 145.0, 155.0])
SEP = 60.0
NBITS = 12


def atomic_savez(path, **kw):
    tmp = path + ".tmp.npz"
    np.savez(tmp, **kw)
    os.replace(tmp, path)


def circ(a, b):
    return np.abs((a - b + 180.0) % 360.0 - 180.0)


def load_energy(crop):
    z = np.load(os.path.join(ROOT, "data", "instruments", "ladder", crop + ".npz"))
    L = len(str(z["seq"]))
    en = EN.Energy(dict(prob=z["prob"], prob_cb=z["prob_cb"], theta_tau_prob=z["theta_tau_prob"]), L)
    return en, L, str(z["seq"])


def get_xstar(crop, en, R=64, seed=0):
    f = os.path.join(OUT, f"{crop}_xstar.npz")
    if os.path.exists(f):
        d = np.load(f)
        return d["x"], float(d["E"])
    rng = np.random.default_rng(seed)
    x0 = H.ExactPrior(en, 1.0).sample(R, rng)
    x, E = EN.relax(en, x0, iters=200)
    i = int(np.argmin(E))
    atomic_savez(f, x=x[i], E=E[i], E_all=E, R=R, seed=seed)
    return x[i], float(E[i])


def alphabets(en, L, xs, nalt=3):
    """per residue r=1..L-3: list of (theta_deg, tau_deg) alternatives and their head probabilities."""
    PT = en.PT.numpy()                      # (L-3, 9, 24): residues 1..L-3
    out = []
    for r in range(1, L - 2):
        th0 = math.degrees(xs[r - 1]); ta0 = math.degrees(xs[L - 2 + r - 1])
        P = PT[r - 1]
        order = np.argsort(P.ravel())[::-1]
        chosen_ta = [ta0]
        alts = []
        for k in order:
            a, c = divmod(int(k), 24)
            tac = float(EN.TA_C[c])
            if all(circ(tac, t) >= (SEP if len(alts) == 0 else 45.0) for t in chosen_ta):
                alts.append((float(TH_CENTRES[a]), tac, float(P.ravel()[k])))
                chosen_ta.append(tac)
                if len(alts) == nalt:
                    break
        out.append(dict(r=r, x0=(th0, ta0), alts=alts))
    return out


def configs(xs, L, res, alph_vals, nbits_per, nbits=NBITS):
    """all 2^nbits internal-coordinate vectors; res = residue list (len nbits/nbits_per)."""
    N = 2 ** nbits
    X = np.repeat(xs[None], N, 0)
    idx = np.arange(N)
    pinned = []
    for j, r in enumerate(res):
        if nbits_per == 1:
            v = (idx >> j) & 1
        else:
            v = ((idx >> (2 * j)) & 1) + 2 * ((idx >> (2 * j + 1)) & 1)
        vals = alph_vals[j]                                 # list of (th_deg, ta_deg) for v = 0..
        th = np.array([math.radians(vals[k][0]) for k in range(len(vals))])
        ta = np.array([math.radians(vals[k][1]) for k in range(len(vals))])
        X[:, r - 1] = th[v]
        X[:, L - 2 + r - 1] = ta[v]
        pinned += [r - 1, L - 2 + r - 1]
    return X, sorted(pinned)


def relax_pinned(en, X, pinned, iters, chunk=256, ckpt=None):
    """L-BFGS with pinned coordinates (zeroed gradients).  Checkpoints finished chunks to ckpt (npz)."""
    mask = np.ones(X.shape[1]); mask[pinned] = 0.0

    def f(x):
        E, G = en(x, grad=True)
        return E, G * mask[None]

    done = {}
    if ckpt and os.path.exists(ckpt):
        d = np.load(ckpt)
        for k in d.files:
            done[int(k.split("_")[1])] = d[k]
    Es = np.empty(len(X))
    for s in range(0, len(X), chunk):
        if s in done:
            Es[s:s + chunk] = done[s]
            continue
        _, E, _ = EN.lbfgs(f, X[s:s + chunk], iters=iters)
        Es[s:s + chunk] = E
        done[s] = E
        if ckpt:
            tmp = ckpt + ".tmp.npz"
            np.savez(tmp, **{f"c_{k}": v for k, v in done.items()})
            os.replace(tmp, ckpt)
    return Es


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--crop", required=True)
    ap.add_argument("--relaxed", action="store_true")
    ap.add_argument("--orders", nargs="+", default=["amb", "rnd"])
    ap.add_argument("--alphs", nargs="+", type=int, default=[2, 4])
    ap.add_argument("--iters", type=int, default=80)
    ap.add_argument("--nbits", type=int, default=NBITS)
    ap.add_argument("--variants", nargs="+", default=None)
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    t0 = time.time()
    en, L, seq = load_energy(a.crop)
    xs, Es = get_xstar(a.crop, en)
    al = alphabets(en, L, xs)
    score = np.array([d["alts"][0][2] for d in al])
    orders = {"amb": [al[i]["r"] for i in np.argsort(-score)],
              "rnd": [al[i]["r"] for i in np.random.default_rng(12345).permutation(len(al))]}
    for oname in a.orders:
        for alph in a.alphs:
            nper = 1 if alph == 2 else 2
            res = orders[oname][:a.nbits // nper]
            vals = []
            for r in res:
                d = al[r - 1]
                vals.append([d["x0"]] + [(t[0], t[1]) for t in d["alts"][:alph - 1]])
            X, pinned = configs(xs, L, res, vals, nper, a.nbits)
            variants = a.variants or (["frozen"] + (["relaxed"] if a.relaxed else []))
            for var in variants:
                f = os.path.join(OUT, f"{a.crop}_{oname}_{alph}_{var}" + ("" if a.nbits == NBITS else f"_b{a.nbits}") + ".npz")
                if os.path.exists(f):
                    continue
                t1 = time.time()
                if var == "frozen":
                    E = np.concatenate([en(X[s:s + 1024], grad=False)[0] for s in range(0, len(X), 1024)])
                else:
                    E = relax_pinned(en, X, pinned, a.iters, ckpt=f + ".partial.npz")
                meta = dict(crop=a.crop, seq=seq, L=L, order=oname, alph=alph, variant=var, residues=res,
                            values_deg=vals, E_xstar=Es, nbits=a.nbits, iters=a.iters if var == "relaxed" else 0,
                            secs=time.time() - t1, native_used=False, label="DEP")
                atomic_savez(f, E=E, meta=json.dumps(meta))
                print(json.dumps(dict(file=os.path.basename(f), Emin=float(E.min()), E0=float(E[0]),
                                      spread=float(np.percentile(E, 50) - E.min()), secs=round(time.time() - t1, 1))),
                      flush=True)
    print("total secs", round(time.time() - t0, 1))


if __name__ == "__main__":
    main()
