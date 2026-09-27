"""Protein 1H dipolar spin dynamics: exact (Trotterised statevector + typicality) vs weight-truncated Pauli propagation.

Program C (hardness-identifiability gate, discovery cards P1/P2/P3).  Physical model: N protons in a static oriented
solid (single orientation of B0 relative to the molecule), secular homonuclear dipolar Hamiltonian
    H = sum_{i<j} d_ij (3 I_z^i I_z^j - I^i . I^j) = sum_{i<j} (d_ij / 4) (2 Z_i Z_j - X_i X_j - Y_i Y_j),
    d_ij = 2 pi * 120.1 kHz * (1 A / r_ij)^3 * (3 cos^2 beta_ij - 1) / 2       (rad/s; 1H-1H; beta = angle(r_ij, B0))
(the prefactor mu0 gamma^2 hbar / (4 pi r^3) / (2 pi) = 120.1 kHz at 1 A for 1H).  Optional phenomenological dephasing:
each spin undergoes pure dephasing at rate gamma (T2 = 1/gamma-type); in the Pauli picture every X/Y factor of a string
decays as exp(-2 gamma dt) per step (Pauli-diagonal channel applied after each Trotter step, exact for that channel);
the statevector reference unravels the same channel with random Z kicks (quantum trajectories).

Trotter step (first order, fixed gate order): for each pair (i<j) in order: exp(-i dt d/2 ZZ) exp(+i dt d/4 XX)
exp(+i dt d/4 YY) (the three commute, so each pair factor is exact).  Both simulators apply the IDENTICAL circuit, so their
difference isolates Pauli-weight truncation (and typicality noise), not Trotter error.

Observables (high-temperature, infinite-temperature correlators):
    transfer  S_ab(t) = Tr[Z_a(t) Z_b] / 2^N          (1H polarisation transfer / spin-diffusion build-up)
    otoc      F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b] / 2^N (many-body echo; butterfly Z_b)
with Z_a(t) = U(t)^dag Z_a U(t).
"""
from __future__ import annotations

import math

import numpy as np

D1A = 2 * math.pi * 120.1e3          # rad/s at 1 A for 1H-1H


# ============================================================================= geometry
def read_h_coords(pdb_path):
    """All hydrogen atoms (first model) -> (names list, coords (n,3)), plus residue ids."""
    names, xyz, res = [], [], []
    with open(pdb_path) as f:
        for line in f:
            if line.startswith("ENDMDL"):
                break
            if not line.startswith(("ATOM", "HETATM")):
                continue
            el = line[76:78].strip() or line[12:16].strip()[0]
            if el != "H":
                continue
            names.append(line[12:16].strip() + "/" + line[17:20].strip() + line[22:26].strip())
            res.append(int(line[22:26]))
            xyz.append((float(line[30:38]), float(line[38:46]), float(line[46:54])))
    return names, np.array(xyz, float), np.array(res)


def cluster(xyz, center, n):
    """indices of the n protons nearest to proton `center` (center first)."""
    d = np.linalg.norm(xyz - xyz[center], axis=1)
    return np.argsort(d)[:n]


def couplings(X, b0=(0.0, 0.0, 1.0)):
    """d_ij (rad/s) for coordinates X (N,3) in Angstrom and field direction b0."""
    b0 = np.asarray(b0, float) / np.linalg.norm(b0)
    N = len(X)
    dmat = np.zeros((N, N))
    for i in range(N):
        v = X[i + 1:] - X[i]
        r = np.linalg.norm(v, axis=1)
        c = (v @ b0) / r
        dmat[i, i + 1:] = D1A * (1.0 / r ** 3) * (3 * c ** 2 - 1) / 2
    return dmat + dmat.T


def gate_list(dmat, dt, cutoff=0.0):
    """Ordered list of (i, j, kind, theta) for one Trotter step; U_gate = exp(-i theta P_kind(i,j))."""
    N = len(dmat)
    gates = []
    for i in range(N):
        for j in range(i + 1, N):
            d = dmat[i, j]
            if abs(d) <= cutoff:
                continue
            gates.append((i, j, "ZZ", dt * d / 2))
            gates.append((i, j, "XX", -dt * d / 4))
            gates.append((i, j, "YY", -dt * d / 4))
    return gates


# ============================================================================= exact: statevector + typicality
def pair_list(dmat, dt, cutoff=0.0):
    """(i, j, d*dt) for the fused exact pair propagators (same order as gate_list)."""
    N = len(dmat)
    return [(i, j, dmat[i, j] * dt) for i in range(N) for j in range(i + 1, N) if abs(dmat[i, j]) > cutoff]


def apply_step(T, N, pairs, inverse=False):
    """T: state as tensor of shape (2,)*N (axis N-1-q <-> qubit q). In place per pair:
    exp(-i dt H_ij), H_ij = (d/4)(2ZZ - XX - YY): |00>,|11> phase e^{-i a}, a = d dt/2;
    {|01>,|10>}: e^{+i a} [[cos a, i sin a],[i sin a, cos a]]  (flip-flop angle a, since XX=YY=sigma_x there)."""
    seq = reversed(pairs) if inverse else pairs
    sg = -1.0 if inverse else 1.0
    for (i, j, ddt) in seq:
        a = sg * ddt / 2.0
        ai, aj = N - 1 - i, N - 1 - j
        idx = [slice(None)] * N
        def v(bi, bj):
            k = list(idx); k[ai] = bi; k[aj] = bj
            return tuple(k)
        e_m = complex(math.cos(a), -math.sin(a)); e_p = complex(math.cos(a), math.sin(a))
        T[v(0, 0)] *= e_m
        T[v(1, 1)] *= e_m
        x01 = T[v(0, 1)].copy(); x10 = T[v(1, 0)]
        c, s_ = math.cos(a), math.sin(a)
        T[v(0, 1)] = e_p * (c * x01 + 1j * s_ * x10)
        T[v(1, 0)] = e_p * (1j * s_ * x01 + c * x10)
    return T


def zmul(T, N, q):
    """T <- Z_q T (in place)."""
    k = [slice(None)] * N; k[N - 1 - q] = 1
    T[tuple(k)] *= -1.0
    return T


def exact_correlators(dmat, dt, n_steps, a, bs, n_rand=4, gamma=0.0, rng=None, otoc=True, record_every=1,
                      otoc_every=None):
    """Typicality estimates of S_ab(t) = Tr[Z_a(t) Z_b]/2^N and (gamma=0) F_ab(t) = Tr[Z_a(t)Z_b Z_a(t)Z_b]/2^N.
    Random unit vectors: <psi|A|psi> ~ Tr(A)/2^N (error ~ 2^{-N/2}/sqrt(n_rand)).
    Dephasing (gamma>0): random Z kicks after each step, p = (1-exp(-2 gamma dt))/2 per spin (trajectory unravelling)."""
    rng = np.random.default_rng(0) if rng is None else rng
    N = len(dmat)
    pairs = pair_list(dmat, dt)
    p_kick = 0.5 * (1 - math.exp(-2 * gamma * dt)) if gamma > 0 else 0.0
    times = list(range(0, n_steps + 1, record_every))
    otimes = list(range(0, n_steps + 1, otoc_every or record_every))
    S = {b: np.zeros(len(times)) for b in bs}
    F = {b: np.zeros(len(otimes)) for b in bs} if (otoc and gamma == 0) else None
    shape = (2,) * N
    for r in range(n_rand):
        psi0 = (rng.standard_normal(shape) + 1j * rng.standard_normal(shape))
        psi0 /= np.linalg.norm(psi0)
        kicks = [np.nonzero(rng.random(N) < p_kick)[0] for _ in range(n_steps)] if p_kick > 0 else None
        phi = psi0.copy(); chis = {b: zmul(psi0.copy(), N, b) for b in bs}
        ti = 0
        for k in range(n_steps + 1):
            if k == times[ti] if ti < len(times) else False:
                va = zmul(phi.copy(), N, a)
                for b in bs:
                    S[b][ti] += float(np.real(np.vdot(va, chis[b]))) / n_rand
                ti += 1
            if k == n_steps:
                break
            apply_step(phi, N, pairs)
            for b in bs:
                apply_step(chis[b], N, pairs)
            if kicks is not None and len(kicks[k]):
                for q in kicks[k]:
                    zmul(phi, N, q)
                    for b in bs:
                        zmul(chis[b], N, q)
        if F is not None:
            for oi, k in enumerate(otimes):
                if k == 0:
                    for b in bs:
                        F[b][oi] += 1.0 / n_rand
                    continue
                def W(vv):
                    vv = vv.copy()
                    for _ in range(k):
                        apply_step(vv, N, pairs)
                    zmul(vv, N, a)
                    for _ in range(k):
                        apply_step(vv, N, pairs, inverse=True)
                    return vv
                Wpsi = W(psi0)
                for b in bs:
                    lhs = zmul(Wpsi.copy(), N, b)
                    rhs = W(zmul(psi0.copy(), N, b))
                    F[b][oi] += float(np.real(np.vdot(lhs, rhs))) / n_rand
    return np.array(times) * dt, S, (np.array(otimes) * dt if F is not None else None), F


# ============================================================================= truncated Pauli propagation (Heisenberg)
_PC16 = np.array([bin(i).count("1") for i in range(1 << 16)], np.int64)


def _popcount(a):
    """popcount for uint64 arrays with values < 2^32 (N <= 31 qubits) via a 16-bit table."""
    a = np.asarray(a, np.uint64)
    return _PC16[(a & np.uint64(0xFFFF)).astype(np.int64)] + _PC16[((a >> np.uint64(16)) & np.uint64(0xFFFF)).astype(np.int64)]


class PauliOp:
    """Real linear combination of Hermitian Pauli strings P(x,z) = i^{x.z} X^x Z^z on N <= 31 qubits."""

    def __init__(self, N, x, z, c):
        self.N = N
        self.x = np.asarray(x, np.uint64); self.z = np.asarray(z, np.uint64); self.c = np.asarray(c, float)

    @staticmethod
    def single_z(N, q):
        return PauliOp(N, [0], [1 << q], [1.0])

    def weight(self):
        return _popcount(self.x | self.z)

    def compact(self, eps=0.0):
        key = (self.x << np.uint64(32)) | self.z
        u, inv = np.unique(key, return_inverse=True)
        c = np.zeros(len(u)); np.add.at(c, inv, self.c)
        keep = np.abs(c) > eps
        u = u[keep]; c = c[keep]
        self.x = u >> np.uint64(32); self.z = u & np.uint64(0xFFFFFFFF); self.c = c
        return self


def _pair_masks(i, j, kind):
    m = np.uint64((1 << i) | (1 << j))
    z0 = np.uint64(0)
    return {"ZZ": (z0, m), "XX": (m, z0), "YY": (m, m)}[kind]


def conj_pair(op: PauliOp, i, j, ddt, wmax=None, eps=0.0):
    """op <- U_ij^dag op U_ij for U_ij = exp(-i dt H_ij) = exp(-i a ZZ) exp(+i a/2 XX) exp(+i a/2 YY), a = d dt/2
    (commuting factors; the three conjugations are applied back to back, compaction/truncation once at the end)."""
    a = ddt / 2.0
    for kind, th in (("YY", -a / 2), ("XX", -a / 2), ("ZZ", a)):
        gx, gz = _pair_masks(i, j, kind)
        op = conj_rotation(op, gx, gz, th, None, 0.0, compact=False)
    if wmax is not None:
        w = _popcount(op.x | op.z)
        keep = w <= wmax
        op.x, op.z, op.c = op.x[keep], op.z[keep], op.c[keep]
    return op.compact(eps)


def conj_rotation(op: PauliOp, gx, gz, theta, wmax=None, eps=0.0, compact=True):
    """op <- U^dag op U with U = exp(-i theta G), G = P(gx,gz) Hermitian Pauli. Anticommuting strings P split into
    cos(2 theta) P + sin(2 theta) (i G P).  Truncate by weight <= wmax and |coef| > eps."""
    x, z, c = op.x, op.z, op.c
    anti = ((_popcount((x & gz) ^ (z & gx))) & 1).astype(bool)
    if not anti.any():
        return op
    xa, za_, ca = x[anti], z[anti], c[anti]
    # product G*P = i^{e} P(x3,z3), e = pc(gx&gz) + pc(xa&za) + 2 pc(gz&xa) - pc(x3&z3)  (mod 4); i*G*P = i^{e+1}
    x3 = gx ^ xa; z3 = gz ^ za_
    e = (_popcount(np.array([gx & gz]))[0] + _popcount(xa & za_) + 2 * _popcount(gz & xa) - _popcount(x3 & z3)) % 4
    sign = np.where((e + 1) % 4 == 0, 1.0, -1.0)          # i^{e+1} with e odd -> +-1
    new_c = math.sin(2 * theta) * ca * sign
    c = c.copy(); c[anti] = ca * math.cos(2 * theta)
    X = np.concatenate([x, x3]); Z = np.concatenate([z, z3]); C = np.concatenate([c, new_c])
    out = PauliOp(op.N, X, Z, C)
    if wmax is not None:
        w = _popcount(out.x | out.z)
        keep = w <= wmax
        out.x, out.z, out.c = out.x[keep], out.z[keep], out.c[keep]
    return out.compact(eps) if compact else out


def pauli_correlators(dmat, dt, n_steps, a, bs, wmax=None, eps=1e-10, gamma=0.0, record_every=1, max_strings=None,
                      coupling_cutoff=0.0, time_budget_s=None, stats=None):
    """Heisenberg evolution of Z_a through the SAME Trotter circuit, truncated to weight <= wmax.
    Returns times, S_ab(t) = coefficient of Z_b, F_ab(t) = sum_P c_P^2 s_P (s_P = -1 if P has X/Y at b), and
    string counts.  Heisenberg order: U = prod_steps (g_1 ... g_M) applied g_1 first => U^dag O U conjugates by
    g_M first within each step."""
    N = len(dmat)
    pairs = pair_list(dmat, dt, cutoff=coupling_cutoff)
    op = PauliOp.single_z(N, a)
    times, S, F, nstr, trunc = [], {b: [] for b in bs}, {b: [] for b in bs}, [], []
    decay = math.exp(-2 * gamma * dt) if gamma > 0 else 1.0
    import time as _time
    t_start = _time.time()
    peak = 1
    capped = False
    for k in range(n_steps + 1):
        if k % record_every == 0:
            times.append(k * dt)
            nstr.append(len(op.c))
            norm2 = float((op.c ** 2).sum())
            trunc.append(norm2)
            if stats is not None:                           # c^2-weighted operator weight (light-cone diagnostic)
                w_ = _popcount(op.x | op.z).astype(float)
                c2 = op.c ** 2
                stats.setdefault("wmean", []).append(float((w_ * c2).sum() / max(c2.sum(), 1e-300)))
                stats.setdefault("w90", []).append(float(np.quantile(np.repeat(w_, 1) if len(w_) < 2 else w_, 0.9)))
            for b in bs:
                zb = np.uint64(1 << b)
                hit = (op.x == 0) & (op.z == zb)
                S[b].append(float(op.c[hit].sum()))
                sb = np.where(((op.x >> np.uint64(b)) & np.uint64(1)).astype(bool), -1.0, 1.0)
                F[b].append(float((op.c ** 2 * sb).sum()))
        if k == n_steps:
            break
        if time_budget_s and _time.time() - t_start > time_budget_s:
            break
        for (i, j, ddt) in reversed(pairs):
            op = conj_pair(op, i, j, ddt, wmax, eps)
            peak = max(peak, len(op.c))
            if max_strings and len(op.c) > max_strings:
                capped = True
                o = np.argsort(-np.abs(op.c))[:max_strings]
                op.x, op.z, op.c = op.x[o], op.z[o], op.c[o]
        if gamma > 0:
            nxy = _popcount(op.x)                          # number of X or Y factors (x bit set)
            op.c = op.c * decay ** nxy
    if stats is not None:
        stats.update(peak_strings=int(peak), capped=bool(capped), secs=_time.time() - t_start, steps_done=int(k))
    return np.array(times), {b: np.array(v) for b, v in S.items()}, {b: np.array(v) for b, v in F.items()}, np.array(nstr), np.array(trunc)


# ============================================================================= exact Heisenberg-matrix reference (deterministic; dephasing exact)
def _apply_pairs_axes(T, nax, off, N, pairs, inverse, reverse_order=None):
    """Apply the fused pair propagators to the qubit axes [off .. off+N-1] of a tensor with nax axes
    (axis off+N-1-q <-> qubit q).  inverse -> each gate inverted; reverse_order (default = inverse) -> order reversed."""
    rev = inverse if reverse_order is None else reverse_order
    seq = list(reversed(pairs)) if rev else pairs
    sg = -1.0 if inverse else 1.0
    base = [slice(None)] * nax
    for (i, j, ddt) in seq:
        a = sg * ddt / 2.0
        ai, aj = off + N - 1 - i, off + N - 1 - j

        def v(bi, bj):
            k = list(base); k[ai] = bi; k[aj] = bj
            return tuple(k)
        e_m = complex(math.cos(a), -math.sin(a)); e_p = complex(math.cos(a), math.sin(a))
        T[v(0, 0)] *= e_m
        T[v(1, 1)] *= e_m
        x01 = T[v(0, 1)].copy(); x10 = T[v(1, 0)]
        c, s_ = math.cos(a), math.sin(a)
        T[v(0, 1)] = e_p * (c * x01 + 1j * s_ * x10)
        T[v(1, 0)] = e_p * (1j * s_ * x01 + c * x10)
    return T


def heisenberg_matrix_correlators(dmat, dt, n_steps, a, bs, gamma=0.0, record_every=1):
    """Exact, deterministic: O(t) = U(t)^dag Z_a U(t) as a dense 2^N x 2^N matrix (N <= ~11), with the exact
    Pauli-diagonal dephasing (off-diagonal element (r,c) damped by exp(-2 gamma dt * popcount(r xor c)) per step,
    identical to the Pauli-picture model).  Per Trotter step (same circuit as the other simulators):
        O <- U_step^dag O U_step  (U^dag on row axes, U on column axes; H_ij real symmetric so U^T = U).
    Returns times, S_ab(t) = Tr[O Z_b]/2^N, F_ab(t) = Tr[O Z_b O Z_b]/2^N."""
    N = len(dmat)
    D = 1 << N
    pairs = pair_list(dmat, dt)
    za = zsign(N, a)
    O = np.diag(za.astype(complex)).reshape((2,) * (2 * N))
    rr = np.arange(D)
    damp = None
    if gamma > 0:
        x = rr[:, None] ^ rr[None, :]
        pc = _PC16[(x & 0xFFFF)] + _PC16[(x >> 16) & 0xFFFF]
        damp = np.exp(-2 * gamma * dt * pc).reshape((2,) * (2 * N))
    times, S, F = [], {b: [] for b in bs}, {b: [] for b in bs}
    for k in range(n_steps + 1):
        if k % record_every == 0:
            M = O.reshape(D, D)
            times.append(k * dt)
            dg = np.real(np.diag(M))
            A2 = np.abs(M) ** 2
            for b in bs:
                zb = zsign(N, b)
                S[b].append(float((dg * zb).mean()))
                F[b].append(float((zb[:, None] * A2 * zb[None, :]).sum() / D))
        if k == n_steps:
            break
        # Heisenberg step: O <- U^dag O U.  U = g_M ... g_1 (g_1 applied first); U^dag O U = g_1^dag..g_M^dag O g_M..g_1
        # Row (ket) axes: multiply by U^dag  -> apply inverse gates in reverse order... acting on the ket index of O
        # means computing U^dag @ O: apply the inverse circuit to each column vector.
        _apply_pairs_axes(O, 2 * N, 0, N, pairs, inverse=True)
        # Column (bra) axes: O @ U = (U^T @ O^T)^T = (U @ O^T)^T since U^T = U: apply the forward circuit on column axes.
        # (O U)_{r,c} = sum_k U^T_{c,k} O_{r,k};  U^T = g_1^T ... g_M^T = g_1 ... g_M  -> apply g_M first, i.e. the
        # FORWARD (non-inverted) gates in REVERSED order on the column axes.
        _apply_pairs_axes(O, 2 * N, N, N, pairs, inverse=False, reverse_order=True)
        if damp is not None:
            O *= damp
    return np.array(times), {b: np.array(v) for b, v in S.items()}, {b: np.array(v) for b, v in F.items()}


def zsign(N, q):
    """diagonal of Z_q in the computational basis (qubit q = bit q of the index)."""
    return 1.0 - 2.0 * ((np.arange(1 << N) >> q) & 1)


# ============================================================================= exact, deterministic, magnetisation sectors
def _popcount_arr(n_bits):
    x = np.arange(1 << n_bits)
    return _PC16[x & 0xFFFF] + _PC16[(x >> 16) & 0xFFFF]


def sector_step_unitaries(dmat, dt, chunk=None):
    """The Trotter step U = g_M ... g_1 (same fused pair circuit as apply_step) restricted to each total-Z sector
    (the secular dipolar H conserves sum_i Z_i, and so does every pair gate).  Built directly inside each sector by
    left-multiplying the identity with the pair gates (row operations, O(M n_k^2)).  Yields (idx_k, U_k) one sector at
    a time (generator: peak memory = one block)."""
    N = len(dmat)
    D = 1 << N
    pairs = pair_list(dmat, dt)
    pc = _popcount_arr(N)
    for k in range(N + 1):
        idx = np.nonzero(pc == k)[0]
        n = len(idx)
        pos = np.full(D, -1, dtype=np.int64)
        pos[idx] = np.arange(n)
        Uk = np.eye(n, dtype=complex)
        for (i, j, ddt) in pairs:
            a = ddt / 2.0
            bi = (idx >> i) & 1
            bj = (idx >> j) & 1
            same = np.nonzero(bi == bj)[0]
            r = np.nonzero((bi == 0) & (bj == 1))[0]
            p_ = pos[idx[r] ^ ((1 << i) | (1 << j))]
            e_m = complex(math.cos(a), -math.sin(a)); e_p = complex(math.cos(a), math.sin(a))
            c, s_ = math.cos(a), math.sin(a)
            if len(same):
                Uk[same] *= e_m
            if len(r):
                x01 = Uk[r]; x10 = Uk[p_]
                Uk[r] = e_p * (c * x01 + 1j * s_ * x10)
                Uk[p_] = e_p * (1j * s_ * x01 + c * x10)
        yield idx, Uk


def _unitary_eig(U, c=0.6180339887498949):
    """Eigen-decomposition of a unitary block via eigh of the commuting Hermitian matrix Re(U) + c Im(U)
    (functions of U; eigenvalues cos(phi) + c sin(phi) separate distinct phases generically).  ~5x faster than the
    complex Schur form.  Falls back to complex Schur if Q^dag U Q is not diagonal to 1e-9."""
    import scipy.linalg as sla
    Hm = 0.5 * (U + U.conj().T) + (0.5 * c / 1j) * (U - U.conj().T)
    _, Q = np.linalg.eigh(Hm)
    del Hm
    D = Q.conj().T @ U @ Q
    lam = np.diag(D).copy()
    np.fill_diagonal(D, 0.0)
    off = np.abs(D).max() if len(lam) else 0.0
    del D
    if off > 1e-9:
        Tm, Q = sla.schur(U, output="complex")
        lam = np.diag(Tm).copy()
    return Q, lam


def sector_exact_correlators(dmat, dt, n_steps, a, bs, gamma=0.0, record_every=1, otoc=False, chunk=512):
    """Exact, deterministic S_ab(t) = Tr[Z_a(t) Z_b]/2^N (and optionally F_ab) for the SAME Trotter circuit, using the
    block structure of U in total-magnetisation sectors (largest block C(N, N/2): N=14 -> 3432, N=16 -> 12870).
    gamma = 0: complex Schur form of each unitary block U_k = Q diag(lam) Q^dag (normal -> diagonal Schur form), then
        S(n) = sum_k sum_ij conj(lam_i)^n A_ij lam_j^n B_ji / 2^N,  A = Q^dag Z_a Q, B = Q^dag Z_b Q (restricted to k).
    gamma > 0: Heisenberg step per block O_k <- damp_k * (U_k^dag O_k U_k), damp_k(r,c) = exp(-2 gamma dt popcount(r^c))
        (identical dephasing channel to heisenberg_matrix_correlators / pauli_correlators)."""
    import scipy.linalg as sla
    N = len(dmat)
    D = 1 << N
    times = list(range(0, n_steps + 1, record_every))
    S = {b: np.zeros(len(times)) for b in bs}
    F = {b: np.zeros(len(times)) for b in bs} if otoc else None
    za_full = zsign(N, a)
    zb_full = {b: zsign(N, b) for b in bs}
    for idx, Uk in sector_step_unitaries(dmat, dt, chunk):
        za = za_full[idx]
        if np.ndim(gamma) == 0 and gamma == 0:
            Q, lam = _unitary_eig(Uk)
            del Uk
            Qh = Q.conj().T
            A = (Qh * za) @ Q
            lc = lam.conj()
            for b in bs:                                   # one observable at a time (peak memory ~ 6 blocks)
                Bm = (Qh * zb_full[b][idx]) @ Q
                M = A * Bm.T
                for ti, n_ in enumerate(times):
                    ph = np.outer(lc ** n_, lam ** n_)
                    S[b][ti] += float(np.real((M * ph).sum()))
                    if otoc:
                        PB = (A * ph) @ Bm
                        F[b][ti] += float(np.real((PB * PB.T).sum()))
                        del PB
                    del ph
                del Bm, M
            del Q, Qh, A
        else:
            xr = idx[:, None] ^ idx[None, :]
            if np.ndim(gamma) == 0:
                pcb = _PC16[xr & 0xFFFF] + _PC16[(xr >> 16) & 0xFFFF]
                damp = np.exp(-2 * gamma * dt * pcb)
            else:                                           # per-spin dephasing rates gamma_i (embedding proxy)
                acc = np.zeros(xr.shape)
                for q, gq in enumerate(np.asarray(gamma, float)):
                    if gq > 0:
                        acc += gq * ((xr >> q) & 1)
                damp = np.exp(-2 * dt * acc)
                del acc
            del xr
            O = np.diag(za.astype(complex))
            Uh = Uk.conj().T
            ti = 0
            for n_ in range(n_steps + 1):
                if n_ % record_every == 0:
                    dg = np.real(np.diag(O))
                    for b in bs:
                        zb = zb_full[b][idx]
                        S[b][ti] += float((dg * zb).sum())
                        if otoc:
                            F[b][ti] += float((zb[:, None] * np.abs(O) ** 2 * zb[None, :]).sum())
                    ti += 1
                if n_ == n_steps:
                    break
                O = (Uh @ O @ Uk) * damp
    tt = np.array(times) * dt
    S = {b: v / D for b, v in S.items()}
    if otoc:
        F = {b: v / D for b, v in F.items()}
    return tt, S, F


# ============================================================================= classical-spin adversary
def classical_spin_correlators(dmat, dt, n_steps, a, bs, n_samples=20000, substeps=4, record_every=1, gamma=0.0,
                               rng=None, s_len=math.sqrt(3) / 2, time_scale=1.0, batch=5000):
    """Classical-spin simulation (Elsayed & Fine, PRB 91, 094424 (2015)-style): spins as classical vectors S_i (|S|=s_len),
    H = sum_{i<j} d_ij (2 S_i^z S_j^z - S_i^x S_j^x - S_i^y S_j^y), dS_i/dt = h_i x S_i, h_i = dH/dS_i, integrated with RK4;
    infinite-temperature initial conditions (uniform on the sphere).  Estimate
        S_ab^cl(t) = <S_a^z(t) S_b^z(0)> / (s_len^2 / 3)       (normalised so that S_aa(0) = 1, like the quantum S_ab).
    Dephasing (gamma > 0): the transverse components of each spin are damped as exp(-2 gamma t)?  -- NOT a unitary model;
    implemented as random-phase kicks about z (rotational diffusion) with variance 4 gamma dt per step, which reproduces
    exp(-2 gamma t) decay of transverse components.  time_scale rescales couplings (adversary knob, default 1)."""
    rng = np.random.default_rng(0) if rng is None else rng
    N = len(dmat)
    J = np.asarray(dmat, float) * time_scale
    J = J - np.diag(np.diag(J))
    times = list(range(0, n_steps + 1, record_every))
    acc = {b: np.zeros(len(times)) for b in bs}
    h = dt / substeps
    tot = 0

    def f(S):
        # h_i = sum_j J_ij (-S_j^x, -S_j^y, 2 S_j^z); dS/dt = h x S
        hx = -(S[..., 0] @ J); hy = -(S[..., 1] @ J); hz = 2 * (S[..., 2] @ J)
        Hf = np.stack([hx, hy, hz], -1)
        return np.cross(Hf, S)

    left = n_samples
    while left > 0:
        B = min(batch, left); left -= B
        v = rng.standard_normal((B, N, 3)); v /= np.linalg.norm(v, axis=-1, keepdims=True); S = v * s_len
        z0 = {b: S[:, b, 2].copy() for b in bs}
        # control variate: subtract z_a(0) z_b(0) - E[z_a(0) z_b(0)]  (E = s^2/3 if a == b else 0), unbiased
        cv = {b: float((S[:, a, 2] * z0[b]).sum()) - (B * s_len ** 2 / 3.0 if b == a else 0.0) for b in bs}
        ti = 0
        for n_ in range(n_steps + 1):
            if n_ % record_every == 0:
                for b in bs:
                    acc[b][ti] += float((S[:, a, 2] * z0[b]).sum()) - cv[b]
                ti += 1
            if n_ == n_steps:
                break
            for _ in range(substeps):
                k1 = f(S); k2 = f(S + 0.5 * h * k1); k3 = f(S + 0.5 * h * k2); k4 = f(S + h * k3)
                S = S + (h / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            if gamma > 0:
                phi = rng.standard_normal((B, N)) * math.sqrt(4 * gamma * dt)
                c, s_ = np.cos(phi), np.sin(phi)
                x, y = S[..., 0].copy(), S[..., 1].copy()
                S[..., 0] = c * x - s_ * y; S[..., 1] = s_ * x + c * y
        tot += B
    norm = tot * s_len ** 2 / 3.0
    return np.array(times) * dt, {b: v / norm for b, v in acc.items()}
