"""T1 library: squared-hafnian (GBS) vs classical samplers of contact-pairing proposals.

Kernel: native-free ESM-prior long-range contact odds W_ij = p/(1-p), |i-j| >= SEP (DEP input).
GBS (pure, PNR, collision-free, 2k photons): P(S) ~ Haf(W_S)^2  [Hamilton et al. PRL 119, 170501].
The native CA trace is used ONLY in `native_contacts` for ORACLE evaluation.
"""
import json
import math
import os
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5))
LADDER = os.path.join(ROOT, "data", "instruments", "ladder")
SEP = 6
FLOOR = 1e-9  # weight for forbidden (|i-j| < SEP) pairs


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def load_crop(chain, L):
    z = np.load(os.path.join(LADDER, f"{chain}_{L}.npz"), allow_pickle=True)
    p = np.clip(z["contact_prob"].astype(np.float64), 1e-6, 1 - 1e-6)
    p = 0.5 * (p + p.T)
    odds = p / (1 - p)
    L_ = p.shape[0]
    ii, jj = np.meshgrid(np.arange(L_), np.arange(L_), indexing="ij")
    allowed = np.abs(ii - jj) >= SEP
    W = np.where(allowed, odds, FLOOR)
    np.fill_diagonal(W, FLOOR)
    return W, z["ca"]  # ca: ORACLE only


def native_contacts(ca):
    """ORACLE: set of native contacts (CA-CA < 8 A, |i-j| >= SEP)."""
    d = np.linalg.norm(ca[:, None, :] - ca[None, :, :], axis=-1)
    L = len(ca)
    out = set()
    for i in range(L):
        for j in range(i + SEP, L):
            if d[i, j] < 8.0:
                out.add((i, j))
    return out


def matchings(n):
    """All perfect matchings of range(n) as int array (n_match, n//2, 2)."""
    def rec(items):
        if not items:
            yield []
            return
        a = items[0]
        for idx in range(1, len(items)):
            b = items[idx]
            rest = items[1:idx] + items[idx + 1:]
            for m in rec(rest):
                yield [(a, b)] + m
    return np.array(list(rec(list(range(n)))), dtype=np.int64)


class HafEval:
    def __init__(self, logW, k):
        self.logW = logW
        self.M = matchings(2 * k)
        self.a = self.M[:, :, 0]
        self.b = self.M[:, :, 1]

    def logvals(self, S):
        sub = self.logW[np.ix_(S, S)]
        return sub[self.a, self.b].sum(1)

    def loghaf(self, S):
        v = self.logvals(S)
        m = v.max()
        return m + math.log(np.exp(v - m).sum())

    def best_matching(self, S):
        v = self.logvals(S)
        m = self.M[int(np.argmax(v))]
        return [tuple(sorted((int(S[x]), int(S[y])))) for x, y in m]


def greedy_matching(logW, k, noise=None):
    """Greedy max-weight k-matching on (optionally perturbed) log-weights, |i-j|>=SEP."""
    L = logW.shape[0]
    iu, ju = np.triu_indices(L, SEP)
    w = logW[iu, ju].copy()
    if noise is not None:
        w = w + noise
    order = np.argsort(-w)
    used = np.zeros(L, bool)
    pairs = []
    for o in order:
        i, j = iu[o], ju[o]
        if not used[i] and not used[j]:
            used[i] = used[j] = True
            pairs.append((int(i), int(j)))
            if len(pairs) == k:
                break
    return pairs


def perturb_and_map(logW, k, n, tau, rng):
    L = logW.shape[0]
    m = len(np.triu_indices(L, SEP)[0])
    return [greedy_matching(logW, k, tau * rng.gumbel(size=m)) for _ in range(n)]


def edge_sampler(W, k, n, gamma, rng):
    L = W.shape[0]
    iu, ju = np.triu_indices(L, SEP)
    base = W[iu, ju] ** gamma
    out = []
    for _ in range(n):
        w = base.copy()
        pairs = []
        for _ in range(k):
            s = w.sum()
            o = rng.choice(len(w), p=w / s)
            i, j = int(iu[o]), int(ju[o])
            pairs.append((i, j))
            kill = (iu == i) | (ju == i) | (iu == j) | (ju == j)
            w[kill] = 0.0
        out.append(pairs)
    return out


def haf_mcmc(logW, k, beta, n, thin, burn, rng, init=None):
    """Metropolis over 2k-subsets S with target Haf(W_S)^beta (exact hafnians).
    Returns list of max-weight matchings inside each sampled S, and acceptance rate."""
    L = logW.shape[0]
    H = HafEval(logW, k)
    if init is None:
        init = [v for p in greedy_matching(logW, k) for v in p]
    S = np.array(init, dtype=np.int64)
    inS = np.zeros(L, bool)
    inS[S] = True
    lh = H.loghaf(S)
    out, acc, tot = [], 0, 0
    for step in range(burn + n * thin):
        a = rng.integers(2 * k)
        comp = np.flatnonzero(~inS)
        u = comp[rng.integers(len(comp))]
        S2 = S.copy()
        S2[a] = u
        lh2 = H.loghaf(S2)
        tot += 1
        if math.log(rng.random() + 1e-300) < beta * (lh2 - lh):
            inS[S[a]] = False
            inS[u] = True
            S, lh = S2, lh2
            acc += 1
        if step >= burn and (step - burn) % thin == thin - 1:
            out.append(H.best_matching(S))
    return out, acc / max(tot, 1)


class MultiDimer:
    """Classical Metropolis sampler for P(S) ~ Haf(W_S)^beta, integer beta >= 1, nonnegative W.
    State: vertex set S (|S| = 2k) and beta perfect matchings of S; weight prod_r w(M_r).
    Marginal over S is exactly Haf(W_S)^beta. beta=2 is the collision-free GBS distribution."""

    def __init__(self, logW, k, beta, rng, init_pairs=None):
        self.logW, self.k, self.beta, self.rng = logW, k, beta, rng
        L = logW.shape[0]
        self.L = L
        if init_pairs is None:
            init_pairs = greedy_matching(logW, k)
        self.S = np.array([v for p in init_pairs for v in p], dtype=np.int64)
        self.pos = -np.ones(L, dtype=np.int64)
        self.pos[self.S] = np.arange(2 * k)
        self.comp = np.array([v for v in range(L) if self.pos[v] < 0], dtype=np.int64)
        self.cpos = -np.ones(L, dtype=np.int64)
        self.cpos[self.comp] = np.arange(len(self.comp))
        self.P = -np.ones((beta, L), dtype=np.int64)
        for r in range(beta):
            for i, j in init_pairs:
                self.P[r, i] = j
                self.P[r, j] = i
        self.lw = sum(self.logW[i, j] for i, j in init_pairs) * beta

    def step(self):
        rng, lw = self.rng, self.logW
        k2 = 2 * self.k
        if rng.random() < 0.5:  # rematch in one matching
            r = rng.integers(self.beta)
            P = self.P[r]
            a = self.S[rng.integers(k2)]
            b = P[a]
            while True:
                c = self.S[rng.integers(k2)]
                if c != a and c != b:
                    break
            d = P[c]
            if rng.random() < 0.5:
                n1, n2 = (a, c), (b, d)
            else:
                n1, n2 = (a, d), (b, c)
            dl = lw[n1] + lw[n2] - lw[a, b] - lw[c, d]
            if math.log(rng.random() + 1e-300) < dl:
                P[n1[0]], P[n1[1]] = n1[1], n1[0]
                P[n2[0]], P[n2[1]] = n2[1], n2[0]
                self.lw += dl
                return 1
            return 0
        else:  # vertex swap in all matchings
            ia = rng.integers(k2)
            v = self.S[ia]
            iu = rng.integers(len(self.comp))
            u = self.comp[iu]
            dl = 0.0
            for r in range(self.beta):
                x = self.P[r, v]
                dl += lw[u, x] - lw[v, x]
            if math.log(rng.random() + 1e-300) < dl:
                for r in range(self.beta):
                    x = self.P[r, v]
                    self.P[r, u] = x
                    self.P[r, x] = u
                    self.P[r, v] = -1
                self.S[ia] = u
                self.comp[iu] = v
                self.pos[u], self.pos[v] = ia, -1
                self.lw += dl
                return 1
            return 0

    def best_matching(self, H=None):
        """Max-weight matching inside S: exact via H when small k, else best of the beta chains' matchings
        polished by 2-opt rematching (deterministic)."""
        S = self.S
        if H is not None:
            return H.best_matching(S)
        best, bestw = None, -1e300
        for r in range(self.beta):
            pairs = {tuple(sorted((int(v), int(self.P[r, v])))) for v in S}
            pairs = two_opt(self.logW, list(pairs))
            w = sum(self.logW[p] for p in pairs)
            if w > bestw:
                best, bestw = pairs, w
        return best


def two_opt(logW, pairs):
    pairs = [tuple(p) for p in pairs]
    improved = True
    while improved:
        improved = False
        n = len(pairs)
        for x in range(n):
            for y in range(x + 1, n):
                a, b = pairs[x]
                c, d = pairs[y]
                cur = logW[a, b] + logW[c, d]
                o1 = logW[a, c] + logW[b, d]
                o2 = logW[a, d] + logW[b, c]
                if o1 > cur + 1e-12 and o1 >= o2:
                    pairs[x], pairs[y] = tuple(sorted((a, c))), tuple(sorted((b, d)))
                    improved = True
                elif o2 > cur + 1e-12:
                    pairs[x], pairs[y] = tuple(sorted((a, d))), tuple(sorted((b, c)))
                    improved = True
    return pairs


def metrics(props, native, k, rng, nboot=200, W=None):
    """ORACLE metrics: prec (mean frac native pairs), allc (all k native), cov (distinct native pairs).
    Native-free diagnostic: mpp = mean model contact probability of proposed pairs (from odds W)."""
    nat = [sum(1 for p in pr if tuple(sorted(p)) in native) for pr in props]
    nat = np.array(nat, float)
    prec = nat / k
    allc = (nat == k).astype(float)
    sets = [set(tuple(sorted(p)) for p in pr if tuple(sorted(p)) in native) for pr in props]
    cov = len(set().union(*sets)) if sets else 0
    n = len(props)
    bc = []
    for _ in range(nboot):
        idx = rng.integers(n, size=n)
        bc.append(len(set().union(*[sets[i] for i in idx])))
    uniq = len({tuple(sorted(tuple(sorted(p)) for p in pr)) for pr in props})
    mpp = float("nan")
    if W is not None:
        mpp = float(np.mean([np.mean([W[p] / (1 + W[p]) for p in pr]) for pr in props]))
    return {
        "mpp": mpp,
        "prec": float(prec.mean()), "prec_se": float(prec.std(ddof=1) / math.sqrt(n)),
        "allc": float(allc.mean()), "allc_se": float(allc.std(ddof=1) / math.sqrt(n)),
        "cov": int(cov), "cov_se": float(np.std(bc, ddof=1)), "cov_boot_mean": float(np.mean(bc)),
        "n": n, "unique": uniq,
    }


def haf_small(Wsub, M):
    """Hafnian (linear domain) of a small symmetric matrix via its perfect-matching list M."""
    if M.shape[1] == 0:
        return 1.0
    return float(Wsub[M[:, :, 0], M[:, :, 1]].prod(1).sum())


def haf_gibbs(W, k, beta, n, sweeps, burn_sweeps, rng, init=None):
    """Heat-bath (Gibbs) sampler over 2k-subsets S with target Haf(W_S)^beta.
    Update of slot a: rest = S minus S[a]; Haf(rest+u) = sum_x W[u,x] Haf(rest-x) for every u
    not in rest (row expansion), so the exact conditional over all L-2k+1 candidates is sampled
    in one shot. Much faster mixing than single-swap Metropolis (production-run attack)."""
    L = W.shape[0]
    Msub = matchings(2 * k - 2)
    DROP = np.array([[j for j in range(2 * k - 1) if j != i] for i in range(2 * k - 1)], dtype=np.int64)
    if init is None:
        init = [v for p in greedy_matching(np.log(W), k) for v in p]
    S = np.array(init, dtype=np.int64)
    Hbest = HafEval(np.log(W), k)
    out = []
    for sw in range(burn_sweeps + n * sweeps):
        for a in rng.permutation(2 * k):
            rest = np.delete(S, a)
            if k == 1:
                h = np.ones(1)
            else:
                R2 = rest[DROP]  # (2k-1, 2k-2): rest minus one element each
                h = W[R2[:, Msub[:, :, 0]], R2[:, Msub[:, :, 1]]].prod(2).sum(1)
            hv = W[:, rest] @ h  # Haf(rest + u) for every u
            hv[rest] = 0.0
            with np.errstate(divide="ignore"):
                lw = beta * np.log(np.maximum(hv, 1e-300))
            lw[rest] = -np.inf
            lw -= lw.max()
            p = np.exp(lw)
            p /= p.sum()
            S[a] = rng.choice(L, p=p)
        if sw >= burn_sweeps and (sw - burn_sweeps) % sweeps == sweeps - 1:
            out.append(Hbest.best_matching(S))
    return out
