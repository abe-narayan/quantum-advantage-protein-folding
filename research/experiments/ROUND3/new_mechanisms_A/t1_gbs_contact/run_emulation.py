"""T1 second kill route: classical double-dimer emulation of the collision-free GBS distribution
P(S) ~ Haf(W_S)^2 for the nonnegative contact-odds kernel.
(a) L=30, k=3: exact enumeration of all C(30,6) subsets vs double-dimer Metropolis and heat-bath.
(b) k = 10..30 (20..60 photons), L = 100/150: two independent double-dimer chains per case
    (greedy init vs random init); vertex-marginal agreement, R-hat of log-weight; value metrics
    vs single-dimer (beta=1) and native-free-calibrated perturb-and-MAP. Checkpointed per case."""
import itertools, json, math, os, sys, time, zlib
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
from gbs_lib import (load_crop, native_contacts, matchings, MultiDimer, haf_gibbs, metrics, atomic_json,
                     greedy_matching, perturb_and_map, SEP)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "results_emulation.json")

def exact_small(W, k, beta):
    L = W.shape[0]; M = matchings(2 * k)
    comb = np.array(list(itertools.combinations(range(L), 2 * k)), dtype=np.int16)
    haf = np.empty(len(comb))
    for s in range(0, len(comb), 50000):
        c = comb[s:s + 50000].astype(np.int64)
        haf[s:s + 50000] = W[c[:, M[:, :, 0]], c[:, M[:, :, 1]]].prod(2).sum(1)
    p = haf ** beta; p /= p.sum()
    marg = np.zeros(L)
    for j in range(2 * k):
        np.add.at(marg, comb[:, j].astype(np.int64), p)
    return marg, comb, p

def dd_marginals(W, k, beta, steps, burn, rng, init=None, every=10):
    md = MultiDimer(np.log(W), k, beta, rng, init)
    occ = np.zeros(W.shape[0]); n = 0; lws = []
    for t in range(burn + steps):
        md.step()
        if t >= burn and (t - burn) % every == 0:
            occ[md.S] += 1; n += 1; lws.append(md.lw)
    return occ / n, np.array(lws), md

def rhat(chains):
    m = len(chains); n = min(len(c) for c in chains); x = np.array([c[:n] for c in chains])
    B = n * x.mean(1).var(ddof=1); Wv = x.var(1, ddof=1).mean()
    return float(math.sqrt(((n - 1) / n * Wv + B / n) / Wv))

def main():
    res = json.load(open(OUT)) if os.path.exists(OUT) else {}
    t0 = time.time()
    # (a) exact validation
    for ch in ("2AB0A", "4LPQA", "8AXJA"):
        key = f"exact|{ch}|30|3"
        if key in res: continue
        W, ca = load_crop(ch, 30)
        marg, comb, p = exact_small(W, 3, 2.0)
        rng = np.random.default_rng(zlib.crc32(key.encode()))
        m_dd, lws, _ = dd_marginals(W, 3, 2, 400000, 20000, rng)
        # heat-bath check
        props_S = []
        rng2 = np.random.default_rng(1)
        occ_hb = np.zeros(30)
        from gbs_lib import haf_gibbs as hg
        # reuse haf_gibbs internals by sampling S via matchings output (vertex sets)
        props = hg(W, 3, 2.0, 2000, 3, 20, rng2)
        for pr in props:
            for a, b in pr: occ_hb[a] += 1; occ_hb[b] += 1
        m_hb = occ_hb / len(props)
        top = np.argsort(-p)[:20]
        res[key] = {"n_subsets": int(len(comb)), "exact_top_subset_prob": float(p[top[0]]),
                    "max_abs_marg_diff_dd": float(np.abs(m_dd - marg).max()),
                    "tv_marg_dd": float(0.5 * np.abs(m_dd - marg).sum() / 6),
                    "max_abs_marg_diff_heatbath": float(np.abs(m_hb - marg).max()),
                    "tv_marg_heatbath": float(0.5 * np.abs(m_hb - marg).sum() / 6),
                    "exact_marg_max": float(marg.max()), "secs": time.time() - t0}
        atomic_json(OUT, res); print(key, res[key], flush=True)
    # (b) large k
    cases = [(ch, L, k) for ch in ("2AB0A", "3M3PA", "8AXJA", "9IXCA") for (L, k) in ((100, 10), (100, 20), (150, 30))]
    for ch, L, k in cases:
        key = f"large|{ch}|{L}|{k}"
        if key in res: continue
        tc = time.time()
        W, ca = load_crop(ch, L); native = native_contacts(ca); logW = np.log(W)
        steps, burn = 300000, 100000
        ms, lwl, props2 = [], [], []
        for c in range(2):
            rng = np.random.default_rng(zlib.crc32(f"{key}|{c}".encode()))
            if c == 0:
                init = None
            else:  # random init: random perfect matching on random 2k vertices
                v = rng.permutation(L)[:2 * k]; init = [tuple(sorted((int(v[2*i]), int(v[2*i+1])))) for i in range(k)]
            md = MultiDimer(logW, k, 2, rng, init)
            occ = np.zeros(L); n = 0; lws = []
            for t in range(burn + steps):
                md.step()
                if t >= burn and (t - burn) % 100 == 0:
                    occ[md.S] += 1; n += 1; lws.append(md.lw)
                    if (t - burn) % 3000 == 0 and len(props2) < 200 and c == 0:
                        props2.append(md.best_matching())
            ms.append(occ / n); lwl.append(np.array(lws))
        # beta=1 single dimer (classically efficient, FPRAS family)
        rng = np.random.default_rng(zlib.crc32(f"{key}|b1".encode()))
        md1 = MultiDimer(logW, k, 1, rng); props1 = []
        for t in range(burn + steps):
            md1.step()
            if t >= burn and (t - burn) % 1500 == 0 and len(props1) < 200:
                props1.append(md1.best_matching())
        mg = metrics(props2, native, k, np.random.default_rng(3), W=W)
        m1 = metrics(props1, native, k, np.random.default_rng(3), W=W)
        pam = {}
        for tau in (0.1, 0.2, 0.3, 0.5, 0.75, 1.0):
            pr = perturb_and_map(logW, k, 200, tau, np.random.default_rng(zlib.crc32(f"{key}|pam{tau}".encode())))
            pam[f"pam{tau:g}"] = metrics(pr, native, k, np.random.default_rng(3), W=W)
        pc = min(pam, key=lambda x: abs(pam[x]["mpp"] - mg["mpp"]))
        res[key] = {"photons": 2 * k, "max_abs_marg_diff_2chains": float(np.abs(ms[0] - ms[1]).max()),
                    "rhat_logweight": rhat(lwl), "gbs_dd": mg, "beta1": m1, "pam_cal": pc, "pam": pam,
                    "greedy": metrics([greedy_matching(logW, k)] * 200, native, k, np.random.default_rng(3), W=W),
                    "secs": time.time() - tc}
        atomic_json(OUT, res)
        r = res[key]
        print(key, f"dmarg={r['max_abs_marg_diff_2chains']:.3f} rhat={r['rhat_logweight']:.3f}",
              f"GBS prec={mg['prec']:.3f} cov={mg['cov']} mpp={mg['mpp']:.3f} | b1 prec={m1['prec']:.3f} cov={m1['cov']}",
              f"| {pc} prec={pam[pc]['prec']:.3f} cov={pam[pc]['cov']} mpp={pam[pc]['mpp']:.3f} [{r['secs']:.0f}s]", flush=True)

if __name__ == "__main__":
    main()
