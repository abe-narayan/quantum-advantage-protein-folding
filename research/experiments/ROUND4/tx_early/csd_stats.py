"""Statistics of csd_crn.py checkpoints.

Per cluster size n and record time t, batch b, site j:  Ybar_bj(t) = batch mean of Y_j(t) (symmetrised correlator).
Plain estimator:   g_bj(t) = Ybar_bj(t) / (s^2/3).
Control variate:   C_j = Y_j(0) = S_a^z(0) S_j^z(0), known mean mu_j = delta_aj s^2/3;
                   g^cv_bj(t) = [Ybar_bj(t) - beta_j(t) (Cbar_bj - mu_j)] / (s^2/3),
                   beta_j(t) = Cov_traj(Y_j(t), C_j) / Var_traj(C_j) from the pooled per-trajectory moments
                   (recomputed inside every jackknife replicate).  At t = 0 it returns G_j(0) = delta_aj exactly.
H (unbiased over batches): H = mean_{b != b'} sum_j g_bj g_b'j.  CRN difference D = H_big - H_q on the same batches.
SEs: leave-one-batch-out jackknife.
"""
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
NORM = (math.sqrt(3) / 2) ** 2 / 3.0


def H_unbiased(g):
    B = g.shape[0]
    s = g.sum(0)
    return (np.sum(s * s, axis=-1) - np.sum(g * g, axis=(0, 2))) / (B * (B - 1))


def gcv(sums, cross, csq, batch, cv=True):
    """sums, cross: (B, T, Nc) batch sums; csq: (B, Nc).  Returns per-batch normalised means (B, T, Nc)."""
    Yb = sums / batch
    if not cv:
        return Yb / NORM
    M = sums.shape[0] * batch
    Cb = sums[:, 0, :] / batch                           # (B, Nc)
    mu = np.zeros(sums.shape[2]); mu[0] = NORM
    Ym = sums.sum(0) / M                                  # (T, Nc)
    Cm = Cb.mean(0)                                       # (Nc,)
    cov = cross.sum(0) / M - Ym * Cm[None, :]
    var = csq.sum(0) / M - Cm ** 2
    beta = cov / var[None, :]
    return (Yb - beta[None, :, :] * (Cb - mu[None, :])[:, None, :]) / NORM


def jackknife(fn, arrays):
    B = arrays[0].shape[0]
    full = fn(*arrays)
    loo = np.array([fn(*[np.delete(a, i, axis=0) for a in arrays]) for i in range(B)])
    se = np.sqrt((B - 1) / B * np.sum((loo - loo.mean(0)) ** 2, axis=0))
    return full, se


def stats(path_ckpt, batch, cv=True):
    st = json.load(open(path_ckpt))
    sizes = sorted(int(k) for k in st["sums"])
    have_cv = "cross" in st
    cv = cv and have_cv
    A = {}
    for n in sizes:
        s = np.array(st["sums"][str(n)])
        c = np.array(st["cross"][str(n)]) if have_cv else np.zeros_like(s)
        q = np.array(st["csq"][str(n)]) if have_cv else np.zeros((s.shape[0], s.shape[2]))
        A[n] = (s, c, q)
    out = dict(M=st["done"] * batch, batches=st["done"], cpu_s=st["cpu_s"], norm_drift=st.get("norm_drift"), cv=cv)
    if st["done"] < 3:
        return out
    for n in sizes:
        H, se = jackknife(lambda s, c, q: H_unbiased(gcv(s, c, q, batch, cv)), list(A[n]))
        out[f"H_{n}"] = H.tolist(); out[f"se_H_{n}"] = se.tolist()
    big = max(sizes)
    for n in sizes:
        if n == big:
            continue

        def dfn(s1, c1, q1, s2, c2, q2):
            return H_unbiased(gcv(s1, c1, q1, batch, cv)) - H_unbiased(gcv(s2, c2, q2, batch, cv))
        D, se = jackknife(dfn, list(A[big]) + list(A[n]))
        out[f"D_{big}_{n}"] = D.tolist(); out[f"se_D_{big}_{n}"] = se.tolist()
    return out


if __name__ == "__main__":
    import glob
    for f in sorted(glob.glob(os.path.join(HERE, "runs", "csdcrn_*.ckpt.json"))):
        batch = int(f.split("x")[-1].split("_")[0])
        for cv in (False, True):
            s = stats(f, batch, cv)
            print(os.path.basename(f), "M", s["M"], "cpu", round(s["cpu_s"]), "cv", s["cv"])
            for k, v in s.items():
                if isinstance(v, list):
                    print("  ", k, np.round(v, 4))
