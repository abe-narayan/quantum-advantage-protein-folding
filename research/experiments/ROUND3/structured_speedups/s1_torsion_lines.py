"""S1 (DQI precondition, torsion encoding): are A80 terms functions of a single linear form over Z_p^s?

DQI (max-LINSAT) needs f(x) = sum_c f_c(b_c . x mod p).  A term that is f_c(b_c . x) has ALL its Fourier variance on
ONE line {k b_c : k in F_p} of the dual group.  Discretise torsions tau -> Z_p (tau = 2 pi x / p, so rotation
composition = addition mod p), fix everything else at the DEP level-1 relaxed minimum x* (S4), and Fourier-analyse
(a) single pair terms  g_ij(tau_T) = w_ca T^CA_ij(d_ij) + w_cb T^CB_ij(d^cb_ij), T = the tau's d_ij depends on;
(b) the whole energy restricted to a window of s consecutive tau's.
Restriction can only merge lines (b_c -> its projection), so lines needed in the restriction LOWER-bound the number
of max-LINSAT constraints any exact DQI encoding needs.  Metrics: fraction of variance on the best line, on axis
lines (additive part), number of lines for 90 / 99 % of the variance, total lines (p^s-1)/(p-1).
"""
from __future__ import annotations

import os

import numpy as np
import torch

from common import EN, HERE, Timer, atomic_json, load_crop, load_json, make_energy, x_from_ca

OUT = os.path.join(HERE, "s1_torsion_lines.json")
COORDS = os.path.join(HERE, "s4_coords.npz")
P_OF_S = {1: 23, 2: 23, 3: 23, 4: 13, 5: 7}


def line_key(k, p):
    """canonical representative of the projective point of nonzero k in F_p^s."""
    nz = np.nonzero(k)[0][0]
    inv = pow(int(k[nz]), p - 2, p)
    return tuple(int(v) for v in (k * inv) % p)


def line_spectrum(vals, p, s):
    F = np.fft.fftn(vals.reshape((p,) * s))
    pw = np.abs(F) ** 2
    pw.flat[0] = 0.0
    tot = pw.sum()
    lines = {}
    for idx in zip(*np.nonzero(pw > 1e-14 * max(tot, 1e-300))):
        k = np.array(idx)
        key = line_key(k, p)
        lines[key] = lines.get(key, 0.0) + pw[idx]
    w = np.array(sorted(lines.values(), reverse=True)) / max(tot, 1e-300)
    axis = sum(v for kk, v in lines.items() if sum(1 for c in kk if c) == 1) / max(tot, 1e-300)
    c = np.cumsum(w)
    n_total = (p ** s - 1) // (p - 1)
    return dict(p=p, s=s, var_total=float(tot / p ** (2 * s)), frac_best_line=float(w[0]) if len(w) else 0.0,
                frac_axis_lines=float(axis), n_lines_90=int(np.searchsorted(c, 0.90) + 1),
                n_lines_99=int(np.searchsorted(c, 0.99) + 1), n_lines_total=int(n_total),
                frac_lines_needed_99=float((np.searchsorted(c, 0.99) + 1) / n_total))


def grid_x(xstar, tau_idx, p, L):
    s = len(tau_idx)
    g = np.stack(np.meshgrid(*[np.arange(p)] * s, indexing="ij"), -1).reshape(-1, s)
    X = np.repeat(xstar[None], len(g), 0)
    X[:, (L - 2) + np.asarray(tau_idx)] = 2 * np.pi * g / p - np.pi
    return X


def pair_term(en, X, pair_index, chunk=16384):
    out = []
    w = en.w
    for a in range(0, len(X), chunk):
        xt = torch.as_tensor(X[a:a + chunk])
        with torch.no_grad():
            L = en.L
            C = EN.build_ca(xt[:, :L - 2], xt[:, L - 2:])
            CB = EN.virtual_cb_t(C)
            i, j = int(en.I[pair_index]), int(en.J[pair_index])
            d = (C[:, i] - C[:, j]).norm(dim=-1); dcb = (CB[:, i] - CB[:, j]).norm(dim=-1)
            Tca = en.Tca[pair_index]; Tcb = en.Tcb[pair_index]

            def interp(T, D):
                gg = (D / EN.GRID_H).clamp(0.0, en.G - 1 - 1e-6)
                i0 = gg.floor().long(); f = gg - i0
                return T[i0] * (1 - f) + T[i0 + 1] * f
            out.append((w["w_ca"] * interp(Tca, d) + w["w_cb"] * interp(Tcb, dcb)).numpy())
    return np.concatenate(out)


def tau_dependence(en, xstar, pair_index, L):
    """tau indices on which d_ij (CA or CB) depends, by central differences at x*."""
    base = xstar.copy()
    dep = []
    for t in range(L - 3):
        vals = []
        for h in (-0.3, 0.3):
            x = base.copy(); x[L - 2 + t] += h
            vals.append(pair_term(en, x[None], pair_index)[0])
        if abs(vals[1] - vals[0]) > 1e-9:
            dep.append(t)
    return dep


def main():
    res = load_json(OUT, {"pairs": [], "windows": []})
    coords = np.load(COORDS)
    T = Timer()
    done_pairs = {(r["crop"], r["pair"]) for r in res["pairs"]}
    done_win = {(r["crop"], r["t0"], r["s"]) for r in res["windows"]}
    for crop in ("2AB0A_30", "8AXJA_30", "5O37A_30"):
        z, L = load_crop(crop)
        en = make_energy(z, L)
        xstar = x_from_ca(coords[crop])
        rng = np.random.default_rng(7)
        I = en.I.numpy(); J = en.J.numpy()
        # ---- (a) single pair terms, grouped by the number of tau's they depend on
        for sep in (3, 4, 5, 6, 7, 9, 12):
            cand = np.where(J - I == sep)[0]
            for pi in rng.choice(cand, size=min(3, len(cand)), replace=False):
                if (crop, int(pi)) in done_pairs:
                    continue
                dep = tau_dependence(en, xstar, pi, L)
                s = len(dep)
                if s == 0 or s > 5:
                    rec = dict(crop=crop, pair=int(pi), i=int(I[pi]), j=int(J[pi]), sep=int(sep), s=s, skipped=True)
                else:
                    p = P_OF_S[s]
                    vals = pair_term(en, grid_x(xstar, dep, p, L), pi)
                    rec = dict(crop=crop, pair=int(pi), i=int(I[pi]), j=int(J[pi]), sep=int(sep), tau_dep=dep,
                               **line_spectrum(vals, p, s))
                res["pairs"].append(rec)
                atomic_json(OUT, res)
                print("pair", crop, rec.get("i"), rec.get("j"), "s", s, {k: rec.get(k) for k in
                      ("p", "frac_best_line", "frac_axis_lines", "n_lines_90", "n_lines_99", "n_lines_total")}, flush=True)
        # ---- (b) whole energy on windows of s consecutive tau's
        for s in (2, 3, 4, 5):
            p = P_OF_S[s]
            for t0 in (4, 12, 20)[: (3 if s <= 3 else 2)]:
                if (crop, t0, s) in done_win or t0 + s > L - 3:
                    continue
                X = grid_x(xstar, list(range(t0, t0 + s)), p, L)
                E = np.concatenate([en(X[a:a + 8192], grad=False)[0] for a in range(0, len(X), 8192)])
                Ec = np.minimum(E, np.percentile(E, 99))          # clip clash spikes (report both)
                rec = dict(crop=crop, t0=t0, s=s, raw=line_spectrum(E, p, s), clipped99=line_spectrum(Ec, p, s),
                           E_min=float(E.min()), E_star=float(en(xstar[None], grad=False)[0][0]))
                res["windows"].append(rec)
                atomic_json(OUT, res)
                print("win", crop, t0, s, {k: rec["clipped99"][k] for k in
                      ("frac_best_line", "frac_axis_lines", "n_lines_90", "n_lines_99", "n_lines_total")}, f"cpu {T.cpu():.0f}s", flush=True)
        if T.cpu() > 400:
            break
    atomic_json(OUT, res)


if __name__ == "__main__":
    main()
