"""ROUND4 / allatom_superquadratic: MEASURED inputs for the all-atom physics regime (CRITIC D1).

Real all-atom force field (OpenMM 8.5.2, amber14-all; GBn2 implicit solvent or TIP3P explicit solvent) on three benchmark
folders whose structures are already in the repo: Trp-cage (1L2Y, 20 aa, fast folder), protein G B1 (1PGA, 56 aa),
ubiquitin (1UBQ, 76 aa, ms folder).  Native structures are used only as starting geometries for (a) system-size /
pair-count bookkeeping, (b) a timing benchmark and (c) a local dynamical analysis at the native minimum (scientific
analysis of the force field's dynamics; nothing is predicted or selected, so no leakage path exists).

Stages (each checkpointed to work/<stage>_<pdb>.json or .npy with atomic tmp+replace; rerun skips finished stages):
  S1 sizes      atom counts; implicit all-pairs count; explicit box (Modeller.addSolvent, padding 1.0 nm, TIP3P) atom
                count and number of pairs within the 1.0 nm cutoff (periodic cKDTree).  MEASURED.
  S2 timing     seconds per MD step, CPU platform, ONE thread, 2 fs, HBonds constraints, LangevinMiddle 300 K, for GBn2
                (no cutoff) and PME explicit (1.0 nm).  MEASURED (this machine is loaded; quantum-favourable).
  S3 hessian    Reference platform (double precision), GBn2, NO constraints (all bond vibrations present), energy-
                minimised native; mass-weighted Hessian by central differences of forces.  MEASURED.
  S4 carleman   Liu et al. (PNAS 2021) R-number for the damped (Langevin, noise dropped: most favourable) quadratic
                truncation about the minimum, in the diagonalising (F1-eigen) coordinates; |F2| LOWER bound from
                directional third derivatives T[v,v] (so R reported is a lower bound on that representation's R).
                Also: negative-curvature census along a 300 K Langevin trajectory (is F1 Hurwitz away from the minimum?)
  S5 lyapunov   largest Lyapunov exponent, NVE (Verlet 0.5 fs, flexible, Reference double precision), two copies
                separated by 1e-8 nm.  MEASURED (all-atom, implicit solvent).
Budget: single-threaded; each stage < 10 CPU-min; peak RAM < 1 GB.
"""
from __future__ import annotations

import json
import os
import sys
import time

os.environ.setdefault("OMP_NUM_THREADS", "1")
import numpy as np  # noqa: E402
import openmm as mm  # noqa: E402
import openmm.app as app  # noqa: E402
import openmm.unit as u  # noqa: E402
from scipy.spatial import cKDTree  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.join(HERE, "work")
os.makedirs(WORK, exist_ok=True)
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
PDBDIR = os.path.join(REPO, "data", "instruments", "nmr")
KB = 0.0083144626  # kJ/mol/K
T = 300.0
KT = KB * T  # kJ/mol
PS = 1.0  # time unit of OpenMM = ps; lengths nm; masses amu; energies kJ/mol -> sqrt(amu nm^2/(kJ/mol)) = 1 ps


def save_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def save_npy(path, arr):
    tmp = path + ".tmp.npy"
    np.save(tmp, arr)
    os.replace(tmp, path)


def load_pdb(p):
    pdb = app.PDBFile(os.path.join(PDBDIR, f"{p}_H.pdb"))
    return pdb


def platform(name, threads=1):
    pl = mm.Platform.getPlatformByName(name)
    props = {"Threads": str(threads)} if name == "CPU" else {}
    return pl, props


# ------------------------------------------------------------------ S1
def s1_sizes(p):
    out = os.path.join(WORK, f"S1_{p}.json")
    if os.path.exists(out):
        return json.load(open(out))
    pdb = load_pdb(p)
    n_prot = pdb.topology.getNumAtoms()
    ff = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    mod = app.Modeller(pdb.topology, pdb.positions)
    t0 = time.time()
    mod.addSolvent(ff, model="tip3p", padding=1.0 * u.nanometer, boxShape="cube")
    xyz = np.array(mod.positions.value_in_unit(u.nanometer))
    box = np.array([v.value_in_unit(u.nanometer) for v in mod.topology.getPeriodicBoxVectors()])
    L = np.diag(box)
    tree = cKDTree(np.mod(xyz, L), boxsize=L)
    npairs = int(tree.count_neighbors(tree, 1.0) - len(xyz)) // 2
    res = dict(pdb=p, n_residues=pdb.topology.getNumResidues(), n_atoms_protein=n_prot,
               implicit_all_pairs=n_prot * (n_prot - 1) // 2,
               explicit_n_atoms=len(xyz), explicit_box_nm=L.tolist(),
               explicit_pairs_within_1nm=npairs, explicit_pairs_per_atom=npairs / len(xyz),
               n_waters=sum(1 for r in mod.topology.residues() if r.name == "HOH"), wall_s=time.time() - t0)
    save_json(out, res)
    return res


# ------------------------------------------------------------------ S2
def s2_timing(p, nsteps_imp=200, nsteps_exp=40):
    out = os.path.join(WORK, f"S2_{p}.json")
    if os.path.exists(out):
        return json.load(open(out))
    pdb = load_pdb(p)
    res = dict(pdb=p, platform="CPU", threads=1, dt_fs=2.0)
    # implicit
    ff = app.ForceField("amber14-all.xml", "implicit/gbn2.xml")
    sysm = ff.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff, constraints=app.HBonds)
    integ = mm.LangevinMiddleIntegrator(T * u.kelvin, 1.0 / u.picosecond, 0.002 * u.picoseconds)
    pl, props = platform("CPU")
    sim = app.Simulation(pdb.topology, sysm, integ, pl, props)
    sim.context.setPositions(pdb.positions)
    sim.minimizeEnergy(maxIterations=200)
    sim.step(20)
    t0 = time.perf_counter(); sim.step(nsteps_imp); dt = time.perf_counter() - t0
    res["implicit_gbn2_s_per_step"] = dt / nsteps_imp
    res["implicit_ns_per_day_1core"] = 0.002 * 86400 / (dt / nsteps_imp) / 1000.0
    del sim
    # explicit
    ff2 = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
    mod = app.Modeller(pdb.topology, pdb.positions)
    mod.addSolvent(ff2, model="tip3p", padding=1.0 * u.nanometer, boxShape="cube")
    sys2 = ff2.createSystem(mod.topology, nonbondedMethod=app.PME, nonbondedCutoff=1.0 * u.nanometer, constraints=app.HBonds)
    integ2 = mm.LangevinMiddleIntegrator(T * u.kelvin, 1.0 / u.picosecond, 0.002 * u.picoseconds)
    sim2 = app.Simulation(mod.topology, sys2, integ2, pl, props)
    sim2.context.setPositions(mod.positions)
    sim2.minimizeEnergy(maxIterations=100)
    sim2.step(5)
    t0 = time.perf_counter(); sim2.step(nsteps_exp); dt2 = time.perf_counter() - t0
    res["explicit_pme_n_atoms"] = mod.topology.getNumAtoms()
    res["explicit_pme_s_per_step"] = dt2 / nsteps_exp
    res["explicit_ns_per_day_1core"] = 0.002 * 86400 / (dt2 / nsteps_exp) / 1000.0
    try:
        import psutil
        res["machine_cpu_percent_during"] = psutil.cpu_percent(0.5)
    except Exception:  # noqa: BLE001
        pass
    save_json(out, res)
    return res


# ------------------------------------------------------------------ S3
def flexible_gb_context(p):
    pdb = load_pdb(p)
    ff = app.ForceField("amber14-all.xml", "implicit/gbn2.xml")
    sysm = ff.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff, constraints=None, rigidWater=False)
    masses = np.array([sysm.getParticleMass(i).value_in_unit(u.dalton) for i in range(sysm.getNumParticles())])
    integ = mm.VerletIntegrator(0.0005 * u.picoseconds)
    pl, props = platform("Reference")
    ctx = mm.Context(sysm, integ, pl, props)
    ctx.setPositions(pdb.positions)
    return pdb, sysm, ctx, masses


def forces(ctx, x):
    ctx.setPositions(np.asarray(x).reshape(-1, 3) * u.nanometer)
    return np.array(ctx.getState(getForces=True).getForces(asNumpy=True).value_in_unit(u.kilojoule_per_mole / u.nanometer)).ravel()


def s3_hessian(p, h=1e-5):
    out_json = os.path.join(WORK, f"S3_{p}.json")
    out_h = os.path.join(WORK, f"S3_{p}_hess_mw.npy")
    out_x = os.path.join(WORK, f"S3_{p}_xmin.npy")
    if os.path.exists(out_json) and os.path.exists(out_h):
        return json.load(open(out_json)), np.load(out_h), np.load(out_x)
    pdb, sysm, ctx, m = flexible_gb_context(p)
    t0 = time.time()
    # phase 1: fast single-thread CPU minimisation; phase 2: double-precision Reference polish
    integ_c = mm.VerletIntegrator(0.0005 * u.picoseconds)
    plc, propc = platform("CPU")
    cc = mm.Context(sysm, integ_c, plc, propc)
    cc.setPositions(pdb.positions)
    mm.LocalEnergyMinimizer.minimize(cc, 1.0, 20000)
    ctx.setPositions(cc.getState(getPositions=True).getPositions())
    del cc
    mm.LocalEnergyMinimizer.minimize(ctx, 1e-2, 3000)
    st = ctx.getState(getPositions=True, getForces=True, getEnergy=True)
    x0 = np.array(st.getPositions(asNumpy=True).value_in_unit(u.nanometer)).ravel()
    f0 = forces(ctx, x0)
    d = x0.size
    ckpt = os.path.join(WORK, f"S3_{p}_hess_partial.npy")
    H = np.load(ckpt) if os.path.exists(ckpt) else np.full((d, d), np.nan)
    done = ~np.isnan(H[:, 0])
    last = time.time()
    for i in range(d):
        if done[i]:
            continue
        xp = x0.copy(); xp[i] += h
        xm = x0.copy(); xm[i] -= h
        H[i] = -(forces(ctx, xp) - forces(ctx, xm)) / (2 * h)
        if time.time() - last > 60:
            save_npy(ckpt, H); last = time.time()
    H = 0.5 * (H + H.T)
    mw = np.repeat(1.0 / np.sqrt(m), 3)
    Hmw = H * mw[:, None] * mw[None, :]
    save_npy(out_x, x0)
    save_npy(out_h, Hmw)
    if os.path.exists(ckpt):
        os.replace(ckpt, ckpt + ".done.npy")  # keep (never delete partial results)
    res = dict(pdb=p, d=int(d), h_nm=h, rms_force_after_min=float(np.sqrt(np.mean(f0 ** 2))),
               energy_min_kJmol=st.getPotentialEnergy().value_in_unit(u.kilojoule_per_mole), wall_s=time.time() - t0)
    save_json(out_json, res)
    return res, Hmw, x0


# ------------------------------------------------------------------ S4
def s4_carleman(p, gammas=(1.0, 5.0, 50.0, 91.0), n_dirs=40, hd=5e-4, census_steps=2000, census_every=200):
    out = os.path.join(WORK, f"S4_{p}.json")
    if os.path.exists(out):
        return json.load(open(out))
    info, Hmw, x0 = s3_hessian(p)
    pdb, sysm, ctx, m = flexible_gb_context(p)
    d = x0.size
    w2, Q = np.linalg.eigh(Hmw)
    order = np.argsort(np.abs(w2))
    rigid = order[:6]
    keep_all = np.setdiff1d(np.arange(d), rigid)
    n_neg = int(np.sum(w2[keep_all] < 0))
    # R is computed on the positive-curvature internal subspace only (quantum-favourable: residual negative/near-zero
    # modes from incomplete minimisation would otherwise force Re(lambda1) -> 0 and R -> infinity)
    keep = keep_all[w2[keep_all] > 0]
    w2i, Qi = w2[keep], Q[:, keep]
    wpos = np.sqrt(np.clip(w2i, 1e-12, None))  # rad/ps
    CM1 = 1.0 / (2 * np.pi * 2.99792458e-2)  # rad/ps -> cm^-1  (1 cm^-1 = 2 pi c = 0.18836 rad/ps)
    res = dict(pdb=p, d=int(d), n_internal=int(len(keep_all)), n_internal_positive_used=int(len(keep)), n_negative_curvature_at_min=n_neg,
               omega_min_cm1=float(wpos.min() * CM1), omega_max_cm1=float(wpos.max() * CM1),
               omega_rigid_abs_max_cm1=float(np.sqrt(np.abs(w2[rigid])).max() * CM1))
    # ---- directional third derivatives in mass-weighted coords: a(y) = M^-1/2 F(M^-1/2 y); T[v,v] = d^2 a / ds^2 along v
    mw = np.repeat(1.0 / np.sqrt(m), 3)
    a0 = forces(ctx, x0) * mw
    rng = np.random.default_rng(12345)
    dirs = {}
    for k in range(min(10, len(keep))):
        dirs[f"soft{k}"] = Qi[:, k]
    for k in range(min(10, len(keep))):
        dirs[f"stiff{k}"] = Qi[:, -1 - k]
    for k in range(n_dirs - 20):
        v = rng.standard_normal(d); dirs[f"rand{k}"] = v / np.linalg.norm(v)
    Tvv = {}
    for name, v in dirs.items():
        # y-step s along unit v (units sqrt(amu) nm): x = x0 + M^-1/2 s v
        s = hd * np.sqrt(np.mean(m))  # ~hd nm displacement scale
        xp = x0 + mw * s * v
        xm = x0 - mw * s * v
        ap = forces(ctx, xp) * mw; am = forces(ctx, xm) * mw
        tvv = -(ap + am - 2 * a0) / s ** 2  # second directional derivative of -acceleration = T[v,v] (d x 1)
        Tvv[name] = Qi.T @ tvv  # internal-mode components
    norms = {k: float(np.linalg.norm(v)) for k, v in Tvv.items()}
    best = max(norms, key=norms.get)
    tv = Tvv[best]
    res["F2_lower_bound_dir"] = best
    res["T_vv_norm_max_per_ps2_per_sqrtamu_nm"] = norms[best]
    res["T_vv_norm_by_family"] = {fam: float(max(v for k, v in norms.items() if k.startswith(fam))) for fam in ("soft", "stiff", "rand")}
    # ---- Carleman R in F1-eigen coordinates for Langevin friction gamma (noise dropped), per-mode 2x2 blocks
    rows = []
    for g in gammas:
        disc = np.sqrt((g / 2) ** 2 - wpos.astype(complex) ** 2)
        lp, lm = -g / 2 + disc, -g / 2 - disc
        re_l1 = float(np.max(lp.real))
        dl = np.abs(lm - lp)
        dl = np.where(dl < 1e-9, 1e-9, dl)
        c = 1.0 / dl  # |z-component| per unit acceleration in mode k (both +/-)
        # |F2_z| >= || c * T[v,v]/1 || * sqrt(2)  (unit z' = sqrt(2) z with y = v; derivation in README)
        F2lb = float(np.sqrt(2.0 * np.sum((c * tv) ** 2)))
        # thermal |z_in|^2 = sum_k (|l-|^2+|l+|^2) kT/w^2 + 2 kT) / |l- - l+|^2   (y_k ~ N(0,kT/w^2), ydot_k ~ N(0,kT))
        z2 = np.sum(((np.abs(lm) ** 2 + np.abs(lp) ** 2) * KT / wpos ** 2 + 2 * KT) / dl ** 2)
        # single softest mode at kT (smallest meaningful initial condition)
        k0 = int(np.argmin(wpos))
        z2_single = float(((abs(lm[k0]) ** 2 + abs(lp[k0]) ** 2) * KT / wpos[k0] ** 2 + 2 * KT) / dl[k0] ** 2)
        R_th = float(np.sqrt(z2) * F2lb / abs(re_l1))
        R_1 = float(np.sqrt(z2_single) * F2lb / abs(re_l1))
        n_over = int(np.sum(wpos < g / 2))
        rows.append(dict(gamma_per_ps=g, Re_lambda1_per_ps=re_l1, n_overdamped_modes=n_over,
                         F2_lower_bound=F2lb, u_in_thermal_norm=float(np.sqrt(z2)),
                         R_lower_bound_thermal=R_th, R_lower_bound_single_softest_mode_kT=R_1))
    rows.append(dict(gamma_per_ps=0.0, Re_lambda1_per_ps=0.0, note="Newtonian / explicit-solvent NVE: Re(lambda)=0 for every internal mode -> R = infinity"))
    res["R_rows"] = rows
    # ---- negative-curvature census along a 300 K Langevin trajectory (flexible, 0.5 fs)
    integ = mm.LangevinMiddleIntegrator(T * u.kelvin, 5.0 / u.picosecond, 0.0005 * u.picoseconds)
    pl, props = platform("Reference")
    c2 = mm.Context(sysm, integ, pl, props)
    c2.setPositions(x0.reshape(-1, 3) * u.nanometer)
    c2.setVelocitiesToTemperature(T * u.kelvin, 7)
    census = []
    for blk in range(census_steps // census_every):
        integ.step(census_every)
        xs = np.array(c2.getState(getPositions=True).getPositions(asNumpy=True).value_in_unit(u.nanometer)).ravel()
        # cheap census: Hessian projected on the 60 softest native internal modes (Rayleigh-Ritz), negative count
        sub = Qi[:, :60]
        Hs = np.zeros((60, 60))
        fx = forces(ctx, xs) * mw
        for j in range(60):
            e = 1e-3 * np.sqrt(np.mean(m))
            fp = forces(ctx, xs + mw * e * sub[:, j]) * mw
            fm = forces(ctx, xs - mw * e * sub[:, j]) * mw
            Hs[:, j] = -(sub.T @ (fp - fm)) / (2 * e)
        ev = np.linalg.eigvalsh(0.5 * (Hs + Hs.T))
        census.append(dict(t_ps=(blk + 1) * census_every * 0.0005, n_negative_in_soft60=int(np.sum(ev < 0)),
                           most_negative_omega2=float(ev.min()), rms_force=float(np.sqrt(np.mean((fx / mw) ** 2)))))
    res["curvature_census_300K"] = census
    save_json(out, res)
    return res


# ------------------------------------------------------------------ S5
def s5_lyapunov(p, plat="CPU", eps_nm=1e-5, t_eq_ps=4.0, t_run_ps=2.5, dt_ps=0.0005, every=20):
    """Largest Lyapunov exponent, NVE Verlet, flexible GBn2.  Checkpointed every ~60 s (both copies' x, v)."""
    tag = f"{plat}_eps{eps_nm:.0e}"
    out = os.path.join(WORK, f"S5_{p}_{tag}.json")
    if os.path.exists(out):
        return json.load(open(out))
    ck = os.path.join(WORK, f"S5_{p}_{tag}_ckpt.npz")
    pdb = load_pdb(p)
    ff = app.ForceField("amber14-all.xml", "implicit/gbn2.xml")
    sysm = ff.createSystem(pdb.topology, nonbondedMethod=app.NoCutoff, constraints=None)
    pl, props = platform(plat)
    if os.path.exists(ck):
        z = np.load(ck)
        Xa, Va, Xb, Vb, b0 = z["Xa"], z["Va"], z["Xb"], z["Vb"], int(z["b"])
        ts, ds = list(z["ts"]), list(z["ds"])
    else:
        plc, propc = platform("CPU")
        lang = mm.LangevinMiddleIntegrator(T * u.kelvin, 5.0 / u.picosecond, dt_ps * u.picoseconds)
        ce = mm.Context(sysm, lang, plc, propc)
        ce.setPositions(pdb.positions)
        mm.LocalEnergyMinimizer.minimize(ce, 10.0, 2000)
        ce.setVelocitiesToTemperature(T * u.kelvin, 11)
        lang.step(int(t_eq_ps / dt_ps))
        st = ce.getState(getPositions=True, getVelocities=True)
        Xa = np.array(st.getPositions(asNumpy=True).value_in_unit(u.nanometer))
        Va = np.array(st.getVelocities(asNumpy=True).value_in_unit(u.nanometer / u.picosecond))
        Xb, Vb = Xa.copy(), Va.copy(); Xb[0, 0] += eps_nm
        b0, ts, ds = 0, [], []
    ctxs = []
    for X, V in ((Xa, Va), (Xb, Vb)):
        integ = mm.VerletIntegrator(dt_ps * u.picoseconds)
        c = mm.Context(sysm, integ, pl, props)
        c.setPositions(X * u.nanometer); c.setVelocities(V * u.nanometer / u.picosecond)
        ctxs.append((c, integ))
    nblk = int(round(t_run_ps / dt_ps / every))
    last = time.time()
    def state(c):
        s_ = c.getState(getPositions=True, getVelocities=True)
        return (np.array(s_.getPositions(asNumpy=True).value_in_unit(u.nanometer)),
                np.array(s_.getVelocities(asNumpy=True).value_in_unit(u.nanometer / u.picosecond)))
    for b in range(b0, nblk):
        for c, integ in ctxs:
            integ.step(every)
        xa, va = state(ctxs[0][0]); xb, vb = state(ctxs[1][0])
        ts.append((b + 1) * every * dt_ps); ds.append(float(np.sqrt(np.sum((xa - xb) ** 2))))
        if time.time() - last > 60 or b == nblk - 1:
            tmp = ck + ".tmp.npz"
            np.savez(tmp, Xa=xa, Va=va, Xb=xb, Vb=vb, b=b + 1, ts=np.array(ts), ds=np.array(ds))
            os.replace(tmp, ck); last = time.time()
    ts, ds = np.array(ts), np.array(ds)
    msk = (ds > 30 * eps_nm) & (ds < 1e-2)
    slope = float(np.polyfit(ts[msk], np.log(ds[msk]), 1)[0]) if msk.sum() >= 5 else float("nan")
    res = dict(pdb=p, platform=plat, eps_nm=eps_nm, dt_fs=dt_ps * 1000, lyapunov_per_ps=slope, n_fit=int(msk.sum()),
               fit_window_nm=[30 * eps_nm, 1e-2], t_ps=ts.tolist(), sep_nm=ds.tolist(),
               note="NVE Verlet, flexible (no constraints), GBn2 no cutoff; one coordinate perturbed by eps")
    save_json(out, res)
    return res


if __name__ == "__main__":
    stages = sys.argv[1].split(",") if len(sys.argv) > 1 else ["S1", "S2", "S3", "S4", "S5"]
    s5kw = json.loads(sys.argv[3]) if len(sys.argv) > 3 else {}
    pdbs = sys.argv[2].split(",") if len(sys.argv) > 2 else ["1L2Y", "1PGA", "1UBQ"]
    for p in pdbs:
        for s in stages:
            t0 = time.time()
            r = {"S1": s1_sizes, "S2": s2_timing, "S3": lambda q: s3_hessian(q)[0], "S4": s4_carleman, "S5": lambda q: s5_lyapunov(q, **s5kw)}[s](p)
            short = {k: v for k, v in r.items() if not isinstance(v, (list, dict))} if isinstance(r, dict) else r
            print(p, s, f"{time.time() - t0:.1f}s", json.dumps(short)[:600], flush=True)
