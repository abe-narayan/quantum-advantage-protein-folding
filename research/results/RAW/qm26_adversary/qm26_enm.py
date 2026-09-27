"""QM-26 classical-adversary test: symmetry-tiled, defected CA elastic network (ANM).

Tiles ubiquitin (1UBQ, 76 CA) on an orthorhombic lattice with random vacancies,
random re-orientations and random cell jitter (non-periodic), builds the ANM
incidence matrix B (K = B^T B, the same factorisation Babbush et al. encode in
amplitudes), and times: lowest modes (shift-invert Lanczos), omega_max,
velocity-Verlet propagation of a local kick, exact Krylov propagation of the
Babbush first-order system, and a light-cone-truncated simulation.
Single-threaded; aborts if system RAM > 92%.
"""
import os
for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[v] = "1"
import sys, time, json
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla
from scipy.spatial import cKDTree
from scipy.spatial.transform import Rotation
import psutil

PDB = r"C:\Users\abena\quantum-advantage-protein-folding\data\instruments\nmr\1UBQ.pdb"
PROC = psutil.Process()


def guard(tag=""):
    vm = psutil.virtual_memory()
    if vm.percent > 92.0:
        raise MemoryError(f"system RAM {vm.percent}% > 92% at {tag}")
    return vm.percent


def rss_gb():
    mi = PROC.memory_info()
    return round(getattr(mi, "peak_wset", mi.rss) / 1e9, 3)


def read_ca(path):
    xyz = []
    for line in open(path):
        if line.startswith("ATOM") and line[12:16].strip() == "CA" and line[16] in " A":
            xyz.append([float(line[30:38]), float(line[38:46]), float(line[46:54])])
    x = np.array(xyz)
    return x - x.mean(0)


def build(n_target, rc=10.0, p_vac=0.03, p_rot=0.05, jitter=0.5, seed=0):
    rng = np.random.default_rng(seed)
    ca = read_ca(PDB)
    ext = ca.max(0) - ca.min(0)
    a = ext + 3.0  # lattice spacing per axis: ~3 A surface gap -> inter-molecule contacts at rc
    ncell = int(np.ceil(n_target / len(ca) / (1 - p_vac)))
    m = int(np.ceil(ncell ** (1 / 3)))
    grid = np.stack(np.meshgrid(np.arange(m), np.arange(m), np.arange(m), indexing="ij"), -1).reshape(-1, 3)
    grid = grid[:ncell]
    keep = rng.random(len(grid)) > p_vac
    grid = grid[keep]
    coords = []
    cell_id = []
    for c, g in enumerate(grid):
        mol = ca
        if rng.random() < p_rot:
            mol = Rotation.random(random_state=rng.integers(1 << 31)).apply(ca)
        coords.append(mol + g * a + rng.normal(0, jitter, 3))
        cell_id.append(np.full(len(ca), c))
    X = np.concatenate(coords)
    cell_id = np.concatenate(cell_id)
    return X, cell_id, grid, a


def incidence(X, rc):
    tree = cKDTree(X)
    pairs = tree.query_pairs(rc, output_type="ndarray").astype(np.int32)
    del tree
    N = len(X)
    # memory-lean assembly in chunks
    P0 = len(pairs)
    keep = np.ones(P0, bool)
    for s in range(0, P0, 1 << 21):
        pp = pairs[s:s + (1 << 21)]
        keep[s:s + len(pp)] = np.linalg.norm(X[pp[:, 1]] - X[pp[:, 0]], axis=1) > 0.5
    pairs = pairs[keep]
    P = len(pairs)
    indices = np.empty((P, 6), np.int32)
    data = np.empty((P, 6), np.float64)
    for s in range(0, P, 1 << 21):
        pp = pairs[s:s + (1 << 21)]
        d = X[pp[:, 1]] - X[pp[:, 0]]
        e = d / np.linalg.norm(d, axis=1)[:, None]
        indices[s:s + len(pp), :3] = 3 * pp[:, 0:1] + np.arange(3, dtype=np.int32)
        indices[s:s + len(pp), 3:] = 3 * pp[:, 1:2] + np.arange(3, dtype=np.int32)
        data[s:s + len(pp), :3] = -e
        data[s:s + len(pp), 3:] = e
    indices = indices.ravel()
    data = data.ravel()
    indptr = np.arange(0, 6 * P + 1, 6, dtype=np.int64)
    B = sp.csr_matrix((data, indices, indptr), shape=(P, 3 * N))
    return B, pairs


def verlet(B, v0, dt, nsteps, obs_idx_list, every):
    x = np.zeros_like(v0)
    v = v0.copy()
    BT = B.T  # CSC view, no copy
    f = -(BT @ (B @ x))
    rec = []
    for s in range(nsteps):
        v += 0.5 * dt * f
        x += dt * v
        f = -(BT @ (B @ x))
        v += 0.5 * dt * f
        if (s + 1) % every == 0:
            rec.append([(s + 1) * dt] + [0.5 * float(v[idx] @ v[idx]) for idx in obs_idx_list])
    return x, v, np.array(rec)


def dof(nodes):
    return (3 * np.asarray(nodes)[:, None] + np.arange(3)).ravel()


def run(n_target, rc=10.0, do_modes=True, nsteps_timing=200, seed=0, lightcone=False, exact_check=False):
    out = {"n_target": n_target, "rc": rc}
    guard("start")
    t0 = time.perf_counter()
    X, cell_id, grid, a = build(n_target, rc=rc, seed=seed)
    B, pairs = incidence(X, rc)
    out["build_s"] = round(time.perf_counter() - t0, 2)
    N = len(X)
    out.update(N=N, dof=3 * N, pairs=len(pairs), mean_contacts=round(2 * len(pairs) / N, 2),
               n_cells=int(len(grid)), extent_A=[round(float(v), 1) for v in (X.max(0) - X.min(0))])
    guard("built")
    Kop = spla.LinearOperator((3 * N, 3 * N), matvec=lambda z: B.T @ (B @ z), dtype=float)
    t0 = time.perf_counter()
    lmax = spla.eigsh(Kop, k=1, which="LA", tol=1e-4, return_eigenvectors=False)[0]
    out["lmax"] = float(lmax)
    out["omega_max"] = float(np.sqrt(lmax))
    out["lmax_s"] = round(time.perf_counter() - t0, 2)
    # lowest 200 nonzero modes via shift-invert Lanczos (sparse LU), where memory permits
    if do_modes:
        guard("modes")
        t0 = time.perf_counter()
        K = (B.T @ B).tocsc()
        nm = min(206, 3 * N - 2)
        w = spla.eigsh(K, k=nm, sigma=-1e-4 * lmax, which="LM", return_eigenvectors=False, tol=1e-8)
        w = np.sort(w)
        nz = w[w > 1e-6 * lmax]
        out["modes_s"] = round(time.perf_counter() - t0, 2)
        out["n_zero"] = int((w <= 1e-6 * lmax).sum())
        out["omega_min"] = float(np.sqrt(nz[0]))
        out["omega_200"] = float(np.sqrt(nz[min(199, len(nz) - 1)]))
        out["ratio_wmax_wmin"] = float(np.sqrt(lmax / nz[0]))
        del K
    guard("prop")
    # local perturbation: kick the node nearest the centre; observe KE of kicked molecule and farthest molecule
    ctr = X.mean(0)
    k0 = int(np.argmin(np.linalg.norm(X - ctr, axis=1)))
    far_cell = int(np.argmax(np.linalg.norm(grid - grid[cell_id[k0]], axis=1)))
    kick_mol = np.where(cell_id == cell_id[k0])[0]
    far_mol = np.where(cell_id == far_cell)[0]
    rng = np.random.default_rng(1)
    v0 = np.zeros(3 * N)
    u = rng.normal(size=3); u /= np.linalg.norm(u)
    v0[3 * k0:3 * k0 + 3] = u  # unit kinetic energy 0.5
    dt = 0.2 / out["omega_max"]
    out["dt"] = dt
    t0 = time.perf_counter()
    x, v, rec = verlet(B, v0, dt, nsteps_timing, [dof(kick_mol), dof(far_mol)], every=max(1, nsteps_timing // 20))
    ts = time.perf_counter() - t0
    out["verlet_s_per_step"] = ts / nsteps_timing
    E = 0.5 * v @ v + 0.5 * float((B @ x) @ (B @ x))
    out["energy_drift_rel"] = float(abs(E - 0.5) / 0.5)
    out["rss_peak_GB"] = rss_gb()
    out["sys_ram_pct"] = guard("post-prop")
    # energy front: radius (from kick) enclosing all but 1e-6 / 1e-9 of kinetic energy at t_final
    ke_node = 0.5 * (v.reshape(-1, 3) ** 2).sum(1)
    r = np.linalg.norm(X - X[k0], axis=1)
    o = np.argsort(r)
    cum = np.cumsum(ke_node[o]); tot = cum[-1]
    out["t_final"] = nsteps_timing * dt
    for thr in (1e-3, 1e-6, 1e-9):
        j = int(np.searchsorted(cum, tot * (1 - thr)))
        out[f"R_front_{thr:g}"] = float(r[o[min(j, N - 1)]])
    if exact_check:
        # exact (Krylov/Taylor) propagation of the Babbush first-order system z=(v, Bx), dz/dt = A z,
        # A = [[0, -B^T],[B, 0]] antisymmetric; compare to Verlet at the same time
        P = B.shape[0]
        A = sp.bmat([[None, -B.T], [B, None]], format="csr")
        z0 = np.concatenate([v0, np.zeros(P)])
        T = nsteps_timing * dt
        t0 = time.perf_counter()
        zT = spla.expm_multiply(A, z0, start=0, stop=T, num=2, endpoint=True)[-1]
        out["exact_krylov_s"] = round(time.perf_counter() - t0, 2)
        vT = zT[:3 * N]
        idx = dof(far_mol)
        idk = dof(kick_mol)
        out["KE_kick_mol_exact"] = float(0.5 * vT[idk] @ vT[idk])
        out["KE_kick_mol_verlet"] = float(0.5 * v[idk] @ v[idk])
        out["exact_vs_verlet_vel_relerr"] = float(np.linalg.norm(vT - v) / np.linalg.norm(vT))
    if lightcone:
        # truncated simulation: keep only nodes within radius R of the kick; compare KE of kicked molecule
        res = []
        KEfull = 0.5 * float(v[dof(kick_mol)] @ v[dof(kick_mol)])
        for R in (30.0, 45.0, 60.0, 80.0, 100.0):
            sel = np.where(np.linalg.norm(X - X[k0], axis=1) < R)[0]
            if len(sel) >= N:
                break
            Xs = X[sel]
            Bs, _ = incidence(Xs, rc)
            mp = {g: l for l, g in enumerate(sel)}
            ks = mp[k0]
            v0s = np.zeros(3 * len(sel)); v0s[3 * ks:3 * ks + 3] = u
            km = np.array([mp[g] for g in kick_mol if g in mp])
            t0 = time.perf_counter()
            xs, vs, _ = verlet(Bs, v0s, dt, nsteps_timing, [dof(km)], every=nsteps_timing)
            tt = time.perf_counter() - t0
            KEs = 0.5 * float(vs[dof(km)] @ vs[dof(km)])
            res.append({"R_A": R, "n_nodes": int(len(sel)), "KE_kickmol": KEs,
                        "rel_diff_vs_full": abs(KEs - KEfull) / KEfull, "s": round(tt, 3)})
        out["lightcone"] = res
        out["KE_kickmol_full"] = KEfull
        out["t_final"] = nsteps_timing * dt
    out["KE_trace_tail"] = rec[-3:].tolist()
    return out


if __name__ == "__main__":
    mode = sys.argv[1]
    results = []
    if mode == "small":
        for n in (1000, 3000, 10000, 30000):
            r = run(n, do_modes=True, nsteps_timing=400, exact_check=(n <= 10000), lightcone=(n == 30000))
            print(json.dumps(r), flush=True)
            results.append(r)
    elif mode == "big":
        try:
            PROC.nice(psutil.IDLE_PRIORITY_CLASS)
        except Exception:
            pass
        for spec in sys.argv[2:]:
            n, st = (int(float(z)) for z in spec.split(":"))
            t_wait = time.time()
            while False:
                pass
            vm = psutil.virtual_memory()
            need = 2.0e3 * n  # bytes: ~2 GB per 1e6 nodes (conservative)
            if vm.available < need + 0.07 * vm.total:
                print(json.dumps({"n_target": n, "skipped": "RAM", "avail_GB": vm.available / 1e9}), flush=True)
                continue
            r = run(n, do_modes=False, nsteps_timing=st)
            r["cpu_wait_s"] = round(time.time() - t_wait, 1)
            print(json.dumps(r), flush=True)
            results.append(r)
    fn = os.path.join(os.path.dirname(__file__), f"qm26_{mode}.json")
    json.dump(results, open(fn, "w"), indent=1)
