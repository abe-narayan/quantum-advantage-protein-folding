"""R1-SIM stronger polynomial adversaries: coupled quantum clusters (CQC) for the protein 1H first-order echo (OTOC(1))
    F_ab(t) = Tr[W Z_b W Z_b] / 2^N,   W = U(t)^dag Z_a U(t),   same Trotter circuit / geometry as the typicality cone
    (research/experiments/ADVERSARIAL/R1_theory_hardness/typicality_cone/*.json, scripts/nmr_cone.py).

One framework covers the lane's method families:
  * the N spins are PARTITIONED into groups; every group is a quantum cluster (state vector of 2^n_g amplitudes);
  * intra-group couplings: the exact fused pair gates of the reference Trotter circuit (same order, same dt);
  * inter-group couplings: Starkov-Fine correlation-preserving mean fields (PRB 98, 214421 (2018); PRB 101, 024428
    (2020), arXiv:1911.00990, Eqs. (9)-(10), (19)-(20)): spin j of group g contributes the vector
        m_j = amp_g <I_j>,   amp_g = sqrt(D_g + 1)   (D_g = 2^n_g),
    so a one-spin quantum group is exactly a classical spin of length sqrt(3)/2 (the hybrid bath), and the random-state
    suppression of quantum expectation values is compensated;
  * field on spin i of group g: h_i = sum_{j not in g} d_ij (-m_j^x, -m_j^y, 2 m_j^z), H = sum d_ij (2IzIz - IxIx - IyIy).
Integrator per Trotter step dt: sweep over groups in order 0..G-1 (each group rotates for dt/2 in the field of all the
others, sequentially), exact intra-group gates (dt), sweep in order G-1..0 (dt/2).  Every elementary operation is
exactly invertible given the other groups' states, so the backward step (sweeps with -dt/2, gates inverted) is the EXACT
inverse of the forward step (no spurious irreversibility; checked numerically by `--selftest`).

Echo estimator (time-dependent-Hartree / product-state Loschmidt echo): random Haar state in every group (the product
ensemble averages to I/2^N, so the estimator is exact when there is one group), branches Psi and Z_b Psi;
A = W[Psi], B_b = W[Z_b Psi] with W = backward_k o Z_a o forward_k on the product manifold;
    E2 ("tdh")  F_b = Re prod_g <A_g| (Z_b if b in g) |B_{b,g}>          (all groups)
    E1 ("core") F_b = Re prod_{g contains a or b} <A_g| (Z_b) |B_{b,g}>   (bath mismatch ignored, as hybrid_echo.py)
Back-action knob for group 0 (the core): amp0 = sqrt(D0+1) ("sf"), 1 ("unamp", = hybrid_echo.py), 0 ("none": the core
does not act on the bath -> a reversible external classical field, the second-cumulant / stochastic-field limit).

Usage (single-threaded; see README):
  python cqc_echo.py --probe 19 --N 16 --core near10 --bath m1 --ba sf --M 48 --tag hyb_sf
  python cqc_echo.py --selftest
"""
from __future__ import annotations

import argparse
import cmath
import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

OUT = os.path.join(HERE, "out")
REF = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")


# ----------------------------------------------------------------------------------------------- geometry (== nmr_cone)
def random_b0(seed):
    r = np.random.default_rng(seed)
    v = r.standard_normal(3)
    return v / np.linalg.norm(v)


def instrument_bs(xyz, probe, K=3, N0=10):
    idx = SP.cluster(xyz, probe, N0)
    X0 = xyz[idx]
    dist = np.linalg.norm(X0 - X0[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:K]]
    return sorted(set(far + [int(np.argsort(dist)[1])]))


def setup(pdb, probe, N):
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    bs = instrument_bs(xyz, probe)
    idx = SP.cluster(xyz, probe, N)
    dm = SP.couplings(xyz[idx], random_b0(1000))
    return dm, bs, [names[i] for i in idx]


# ----------------------------------------------------------------------------------------------- partitions
def agglomerate(dm, members, m):
    """Greedy agglomeration of `members` by |d_ij| (strongest first), group size capped at m."""
    members = list(members)
    grp = {i: [i] for i in members}
    pairs = sorted(((abs(dm[i, j]), i, j) for ii, i in enumerate(members) for j in members[ii + 1:]), reverse=True)
    for _, i, j in pairs:
        gi, gj = grp[i], grp[j]
        if gi is gj or len(gi) + len(gj) > m:
            continue
        new = sorted(gi + gj)
        for k in new:
            grp[k] = new
    out, seen = [], set()
    for i in members:
        g = grp[i]
        if id(g) not in seen:
            seen.add(id(g)); out.append(sorted(g))
    return out


def core_set(dm, bs, spec, a=0):
    """near<n>: the n nearest protons (0..n-1).  str<n>: {a} u bs grown greedily by total |d| to the current set."""
    N = len(dm)
    if spec.startswith("near"):
        return list(range(int(spec[4:])))
    if spec.startswith("str"):
        n = int(spec[3:])
        cur = sorted(set([a] + list(bs)))
        while len(cur) < n:
            rest = [j for j in range(N) if j not in cur]
            score = [np.sum(dm[j, cur] ** 2) for j in rest]
            cur.append(rest[int(np.argmax(score))]); cur.sort()
        return cur
    raise ValueError(spec)


def partition(dm, bs, core_spec, bath_spec, a=0):
    """Returns groups (list of sorted global-index lists; groups[0] = core).
    bath_spec: m<k> -> bath agglomerated into clusters of <= k spins;  all<k> -> no core, everything in <= k clusters
    but {a} u bs forced together first (k >= 5)."""
    N = len(dm)
    if bath_spec.startswith("kl"):
        # swap/move hill climbing from all<k>: maximise sum of intra-group d^2 (weakest mean-field cut),
        # {a} u bs pinned to group 0, sizes <= k.  "kls<k>": swaps only (group sizes, incl. the core's, preserved)
        swaps_only = bath_spec.startswith("kls")
        k = int(bath_spec[3:] if swaps_only else bath_spec[2:])
        groups = [list(g) for g in partition(dm, bs, core_spec, f"all{k}", a)]
        pin = set([a] + list(bs)) if k >= len(set([a] + list(bs))) else set()
        d2 = dm ** 2

        def gain_move(i, gs, gt):
            return sum(d2[i, j] for j in gt) - sum(d2[i, j] for j in gs if j != i)
        improved = True
        while improved:
            improved = False
            for s in range(len(groups)):
                for i in list(groups[s]):
                    if i in pin:
                        continue
                    for t in range(len(groups)):
                        if t == s:
                            continue
                        if (not swaps_only and len(groups[t]) < k
                                and gain_move(i, groups[s], groups[t]) > 1e-9 * d2.max()):
                            groups[s].remove(i); groups[t].append(i); improved = True; break
                        for j in list(groups[t]):
                            if j in pin and s != 0:
                                continue
                            if j in pin:
                                continue
                            g = (gain_move(i, groups[s], groups[t]) + gain_move(j, groups[t], groups[s])
                                 - 2 * d2[i, j])
                            if g > 1e-9 * d2.max():
                                groups[s].remove(i); groups[t].remove(j)
                                groups[s].append(j); groups[t].append(i); improved = True; break
                        if improved:
                            break
                    if improved:
                        break
                if improved:
                    break
        return [sorted(g) for g in groups if g]
    if bath_spec.startswith("all"):
        k = int(bath_spec[3:])
        if k < len(set([a] + list(bs))):                    # cannot hold {a} u bs together: plain agglomeration
            return agglomerate(dm, list(range(N)), k)
        seed = core_set(dm, bs, f"str{k}", a)
        rest = [j for j in range(N) if j not in seed]
        return [seed] + agglomerate(dm, rest, k)
    core = core_set(dm, bs, core_spec, a)
    bath = [j for j in range(N) if j not in core]
    m = int(bath_spec[1:])
    return [core] + (agglomerate(dm, bath, m) if bath else [])


# ----------------------------------------------------------------------------------------------- batched kernels
def pair_gates(psi, n, pairs, inverse=False):
    """psi (2^n, B); qubit q = bit q of the row index; pairs (i, j, d*dt) local, i < j; the fused exact pair gate of
    qapf.nmr.spins.apply_step (same convention, same order; inverse -> reversed order, negated angles)."""
    B = psi.shape[1]
    seq = reversed(pairs) if inverse else pairs
    sg = -1.0 if inverse else 1.0
    for (i, j, ddt) in seq:
        al = sg * ddt / 2.0
        T = psi.reshape(1 << (n - 1 - j), 2, 1 << (j - 1 - i), 2, 1 << i, B)
        e_m = cmath.exp(-1j * al); e_p = cmath.exp(1j * al)
        c, s = math.cos(al), math.sin(al)
        T[:, 0, :, 0] *= e_m
        T[:, 1, :, 1] *= e_m
        x01 = T[:, 0, :, 1].copy(); x10 = T[:, 1, :, 0]
        T[:, 0, :, 1] = (e_p * c) * x01 + (e_p * 1j * s) * x10
        T[:, 1, :, 0] = (e_p * 1j * s) * x01 + (e_p * c) * x10
    return psi


def rotate_group(psi, n, h, tau):
    """psi <- prod_q exp(-i tau h_q . sigma_q / 2) psi; h (n, 3, B) per column."""
    B = psi.shape[1]
    hn = np.sqrt((h ** 2).sum(1))                               # (n, B)
    safe = np.where(hn > 0, hn, 1.0)
    kx, ky, kz = h[:, 0] / safe, h[:, 1] / safe, h[:, 2] / safe
    th = 0.5 * hn * tau
    c, s = np.cos(th), np.sin(th)
    u00 = c - 1j * s * kz; u11 = c + 1j * s * kz
    u01 = -s * ky - 1j * s * kx; u10 = s * ky - 1j * s * kx
    for q in range(n):
        T = psi.reshape(1 << (n - 1 - q), 2, 1 << q, B)
        a0 = T[:, 0].copy(); a1 = T[:, 1]
        T[:, 0] *= u00[q]
        T[:, 0] += u01[q] * a1
        a1 *= u11[q]
        a1 += u10[q] * a0
    return psi


def expect(psi, n):
    """<I_x>, <I_y>, <I_z> per qubit per column -> (n, 3, B) (columns normalised)."""
    B = psi.shape[1]
    out = np.empty((n, 3, B))
    p = (psi.real ** 2 + psi.imag ** 2)
    for q in range(n):
        T = psi.reshape(1 << (n - 1 - q), 2, 1 << q, B)
        ab = np.einsum("ijb,ijb->b", T[:, 0].conj(), T[:, 1])
        P = p.reshape(1 << (n - 1 - q), 2, 1 << q, B)
        out[q, 0] = ab.real; out[q, 1] = ab.imag
        out[q, 2] = 0.5 * (P[:, 0].sum((0, 1)) - P[:, 1].sum((0, 1)))
    return out


def rot_vec(v, h, tau):
    """Rigid rotation of vectors v (n,3,B) about h (n,3,B) by |h| tau (dv/dt = h x v)."""
    hn = np.sqrt((h ** 2).sum(1, keepdims=True))
    k = h / np.where(hn > 0, hn, 1.0)
    phi = hn * tau
    cp, sp_ = np.cos(phi), np.sin(phi)
    kv = (k * v).sum(1, keepdims=True)
    return v * cp + np.cross(k, v, axis=1) * sp_ + k * kv * (1.0 - cp)


def zmul_rows(psi, n, q, cols=None):
    T = psi.reshape(1 << (n - 1 - q), 2, 1 << q, psi.shape[1])
    if cols is None:
        T[:, 1] *= -1.0
    else:
        T[:, 1, :, cols] *= -1.0
    return psi


# ----------------------------------------------------------------------------------------------- the CQC system
class CQC:
    def __init__(self, dm, groups, dt, amp0="sf"):
        self.dm = dm
        self.N = len(dm)
        self.groups = [list(map(int, g)) for g in groups]
        self.G = len(groups)
        self.dt = dt
        self.where = {}
        for gi, g in enumerate(self.groups):
            for li, j in enumerate(g):
                self.where[j] = (gi, li)
        assert sorted(self.where) == list(range(self.N)), "groups must partition the spins"
        self.n = [len(g) for g in self.groups]
        self.amp = [math.sqrt((1 << n) + 1) for n in self.n]
        if amp0 == "unamp":
            self.amp[0] = 1.0
        elif amp0 == "none":
            self.amp[0] = 0.0
        # intra-group pair lists (local indices; global lexicographic order == local order because groups are sorted)
        self.pairs = []
        self.blocks = []                      # per group: (perm, [(s, e, U_k, U_k^dag)]) of the one-step intra circuit
        for g in self.groups:
            sub = dm[np.ix_(g, g)]
            self.pairs.append(SP.pair_list(sub, dt))
            if len(g) >= 2:
                perm, blk, s = [], [], 0
                for idx, Uk in SP.sector_step_unitaries(sub, dt):
                    e = s + len(idx)
                    blk.append((s, e, np.ascontiguousarray(Uk), np.ascontiguousarray(Uk.conj().T)))
                    perm.extend(idx.tolist()); s = e
                self.blocks.append((np.array(perm), blk))
            else:
                self.blocks.append(None)
        # inter-group coupling rows: D_g (n_g, N) with intra-group columns zeroed
        self.Drow = []
        for g in self.groups:
            D = dm[g, :].copy()
            D[:, g] = 0.0
            self.Drow.append(D)

    def init(self, M, nbranch, rng, product=False):
        """Haar random state per group per sample, replicated over branches (column = branch*M + sample).
        product=True: every spin gets its own Haar single-spin state, drawn in GLOBAL spin order from one stream, and a
        group's state is their tensor product (E|psi><psi| = I/2^N still holds -> unbiased when evolution is exact).
        This gives common random numbers across different partitions of the same N (used by the CCE driver)."""
        self.B = M * nbranch
        self.psi = []
        if product:
            phi = rng.standard_normal((self.N, 2, M)) + 1j * rng.standard_normal((self.N, 2, M))
            phi /= np.linalg.norm(phi, axis=1, keepdims=True)
        for gi, n in enumerate(self.n):
            if product:
                g = self.groups[gi]
                v = phi[g[n - 1]]                                    # most significant qubit first
                for q in range(n - 2, -1, -1):
                    v = (v[:, None, :] * phi[g[q]][None, :, :]).reshape(-1, M)
            else:
                v = rng.standard_normal((1 << n, M)) + 1j * rng.standard_normal((1 << n, M))
                v /= np.linalg.norm(v, axis=0, keepdims=True)
            self.psi.append(np.ascontiguousarray(np.tile(v, (1, nbranch))))
        self.refresh_all()

    def refresh_all(self):
        self.m = np.zeros((self.N, 3, self.B))
        for gi, g in enumerate(self.groups):
            self.m[g] = self.amp[gi] * expect(self.psi[gi], self.n[gi])

    zz_only = False                       # True: inter-group mean fields keep only the Ising (secular zz) part
    lam = 1.0                             # scale of the transverse (flip-flop) inter-group mean field

    def field(self, gi):
        F = np.empty_like(self.m)
        if self.zz_only:
            F[:, 0] = 0.0; F[:, 1] = 0.0
        else:
            F[:, 0] = -self.lam * self.m[:, 0]; F[:, 1] = -self.lam * self.m[:, 1]
        F[:, 2] = 2.0 * self.m[:, 2]
        return np.einsum("ij,jcb->icb", self.Drow[gi], F)

    def sweep(self, tau, order):
        for gi in order:
            if self.G == 1:
                return
            h = self.field(gi)
            rotate_group(self.psi[gi], self.n[gi], h, tau)
            g = self.groups[gi]
            self.m[g] = rot_vec(self.m[g], h, tau)

    def gates(self, inverse=False):
        for gi in range(self.G):
            if self.blocks[gi] is None:
                continue
            perm, blk = self.blocks[gi]
            ps = self.psi[gi][perm]
            for (s, e, U, Uh) in blk:
                ps[s:e] = (Uh if inverse else U) @ ps[s:e]
            self.psi[gi][perm] = ps
            self.m[self.groups[gi]] = self.amp[gi] * expect(self.psi[gi], self.n[gi])

    def step(self, inverse=False):
        tau = (-0.5 if inverse else 0.5) * self.dt
        self.sweep(tau, range(self.G))
        self.gates(inverse)
        self.sweep(tau, range(self.G - 1, -1, -1))

    def evolve(self, k, inverse=False):
        """k steps == k calls of step(inverse), with the two adjacent group-0 half rotations at every step boundary
        merged into one rotation of 2 tau (exact: group 0's field depends only on groups 1..G-1, unchanged between)."""
        if k <= 0:
            return
        tau = (-0.5 if inverse else 0.5) * self.dt
        self.sweep(tau, range(self.G))
        for n_ in range(k):
            self.gates(inverse)
            if n_ < k - 1:
                self.sweep(tau, range(self.G - 1, 0, -1))
                self.sweep(2 * tau, [0])
                self.sweep(tau, range(1, self.G))
        self.sweep(tau, range(self.G - 1, -1, -1))

    def snapshot(self):
        return [p.copy() for p in self.psi], self.m.copy()

    def restore(self, snap):
        self.psi = [p.copy() for p in snap[0]]
        self.m = snap[1].copy()


def echo(sysq, bs, ks, M, seed, a=0, ckpt=None, state=None, save=None, product=False, samples=None):
    """Returns per-k dict: F_tdh[b] (mean, se), F_core[b] (mean, se).  samples (dict) -> per-sample F_core arrays."""
    nbr = 1 + len(bs)
    rng = np.random.default_rng(seed)
    sysq.init(M, nbr, rng, product=product)
    ga, la = sysq.where[a]
    # branch r >= 1: Z_{b_r} on its column block
    for r, b in enumerate(bs, start=1):
        gb, lb = sysq.where[b]
        zmul_rows(sysq.psi[gb], sysq.n[gb], lb, cols=slice(r * M, (r + 1) * M))
    sysq.refresh_all()
    snap0 = sysq.snapshot()
    res = state if state is not None else {}
    for k in ks:
        if str(k) in res:
            continue
        t0 = time.time()
        sysq.restore(snap0)
        sysq.evolve(k)
        zmul_rows(sysq.psi[ga], sysq.n[ga], la)
        sysq.m[sysq.groups[ga]] = sysq.amp[ga] * expect(sysq.psi[ga], sysq.n[ga])
        sysq.evolve(k, inverse=True)
        out = {"F_tdh": {}, "F_core": {}}
        A = [p[:, :M] for p in sysq.psi]
        for r, b in enumerate(bs, start=1):
            gb, lb = sysq.where[b]
            tot = np.ones(M, complex); core = np.ones(M, complex)
            for gi in range(sysq.G):
                Bg = sysq.psi[gi][:, r * M:(r + 1) * M]
                if gi == gb:
                    Bg = zmul_rows(Bg.copy(), sysq.n[gi], lb)
                ov = np.einsum("ib,ib->b", A[gi].conj(), Bg)
                tot *= ov
                if gi in (ga, gb):
                    core *= ov
            if samples is not None:
                samples[(k, b)] = core.real.copy()
            for key, val in (("F_tdh", tot.real), ("F_core", core.real)):
                out[key][str(b)] = [float(val.mean()), float(val.std(ddof=1) / math.sqrt(M))]
        out["secs"] = time.time() - t0
        res[str(k)] = out
        if save is not None:
            save(res)
    return res


# ----------------------------------------------------------------------------------------------- self-test
def selftest():
    dm, bs, _ = setup("1UBQ", 19, 10)
    dt = 2e-6
    # (1) one group == reference circuit: compare with sector-exact at N=10
    k = 40
    tt, S, F = SP.sector_exact_correlators(dm, dt, k, 0, bs, otoc=True, record_every=k)
    q = CQC(dm, [list(range(10))], dt)
    r = echo(q, bs, [k], 256, 1)
    err1 = max(abs(r[str(k)]["F_tdh"][str(b)][0] - F[b][1]) for b in bs)
    se1 = max(r[str(k)]["F_tdh"][str(b)][1] for b in bs)
    # (2) exact reversibility of the mean-field map (no Z_a flip): split into 3 groups, forward 80 then back 80
    groups = partition(dm, bs, "near6", "m2")
    q = CQC(dm, groups, dt, "sf")
    q.init(8, 1, np.random.default_rng(3))
    s0 = q.snapshot()
    for _ in range(80):
        q.step()
    for _ in range(80):
        q.step(inverse=True)
    rev = max(float(np.abs(p - p0).max()) for p, p0 in zip(q.psi, s0[0]))
    # (3) one-spin quantum groups with amplification == classical spins of length sqrt(3)/2
    one = CQC(dm, [[i] for i in range(10)], dt)
    one.init(4, 1, np.random.default_rng(5))
    lens = np.sqrt((one.m ** 2).sum(1))
    print(json.dumps(dict(exact_one_group_max_err=err1, typ_se=se1, reversibility_max_amp_err=rev,
                          one_spin_len_min=float(lens.min()), one_spin_len_max=float(lens.max()),
                          groups_near6_m2=groups)))


# ----------------------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int)
    ap.add_argument("--N", type=int)
    ap.add_argument("--core", default="near10")
    ap.add_argument("--bath", default="m1")
    ap.add_argument("--ba", default="sf", choices=["sf", "unamp", "none"])
    ap.add_argument("--M", type=int, default=48)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--dt", type=float, default=2e-6)
    ap.add_argument("--times-us", default="40,80,160,240,320")
    ap.add_argument("--tag", default=None)
    ap.add_argument("--mf", default="full", choices=["full", "zz"], help="zz: Ising-only inter-group mean field")
    ap.add_argument("--lam", type=float, default=1.0, help="transverse inter-group mean-field scale")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest(); return
    dm, bs, names = setup(a.pdb, a.probe, a.N)
    groups = partition(dm, bs, a.core, a.bath)
    q = CQC(dm, groups, a.dt, a.ba)
    q.zz_only = (a.mf == "zz")
    q.lam = a.lam
    ks = [int(round(float(t) * 1e-6 / a.dt)) for t in a.times_us.split(",")]
    tag = (a.tag or f"{a.core}_{a.bath}_{a.ba}" + ("_zz" if a.mf == "zz" else "")) +         (f"_lam{a.lam:g}" if a.lam != 1.0 else "")
    os.makedirs(OUT, exist_ok=True)
    fj = os.path.join(OUT, f"{a.pdb}_p{a.probe}_N{a.N}_{tag}_M{a.M}_s{a.seed}.json")
    if os.path.exists(fj):
        print("exists", fj); return
    ck = fj + ".ckpt.json"
    state = json.load(open(ck)) if os.path.exists(ck) else {}
    t0 = time.time()

    def save(res):
        json.dump(res, open(ck + ".tmp", "w")); os.replace(ck + ".tmp", ck)

    res = echo(q, bs, ks, a.M, a.seed, state=state, save=save)
    out = dict(pdb=a.pdb, probe=a.probe, N=a.N, core=a.core,
               bath=a.bath + ("_zz" if a.mf == "zz" else "") + (f"_lam{a.lam:g}" if a.lam != 1.0 else ""), ba=a.ba,
               mf=a.mf, lam=a.lam, M=a.M, seed=a.seed, dt=a.dt,
               bs=bs, groups=groups, group_sizes=[len(g) for g in groups], amps=q.amp,
               times_us=[k * a.dt * 1e6 for k in ks], ks=ks, res=res,
               secs_total=float(sum(res[str(k)]["secs"] for k in ks)), secs_this_call=time.time() - t0)
    json.dump(out, open(fj + ".tmp", "w")); os.replace(fj + ".tmp", fj)
    os.remove(ck)
    print(json.dumps(dict(file=os.path.basename(fj), secs=round(out["secs_total"], 1), sizes=out["group_sizes"])))


if __name__ == "__main__":
    main()
