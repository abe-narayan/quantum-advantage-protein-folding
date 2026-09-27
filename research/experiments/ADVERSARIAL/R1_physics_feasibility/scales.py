"""R1 physics-feasibility audit, part 1: coupling scales, second moments, T2, and competing interactions.

For every gamma=0 NMR gate job with echo (OTOC) Fisher information (research/results/RAW/nmr_gate, nmr_gate_hn) this script
computes, at the SAME B0 orientation and cluster as the job:
  * |d_ij|/2pi (kHz): the homonuclear secular couplings actually used by the model;
  * Van Vleck second moments M2 and T2 := 1/sqrt(M2) (the definition used by Sanchez, Chattah & Pastawski,
    PRA 105, 052232 (2022), Eq. 2: M2 = -Tr([H, I_y]^2)/Tr[I_y^2]):
      - of the isolated N-spin model cluster (what the RAW dynamics actually saw),
      - of the whole protein 1H network (static H, and methyl/NH3 3-site-jump averaged),
      - local, per probe: M2_loc(FID) = (5/4) sum_j d_aj^2 and M2_loc(Z) = (1/2) sum_j d_aj^2 (derived below, checked
        numerically against dense matrices);
  * dimensionless times of the echo window: t_c*/T2 and t_50/T2 (t_50 = time by which half the echo FI has accrued);
  * heteronuclear local-field second moments at each probe (1H-13C for u-13C, 1H-15N / 1H-14N, and 1H-2H for the
    perdeuterated amide-only model) that the pure homonuclear model omits.
Output: scales.json.  Pure geometry + RAW re-analysis; seconds of CPU.  Single-threaded.
"""
from __future__ import annotations

import glob
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402

D1A = SP.D1A                       # rad/s, 1H-1H at 1 A (2 pi * 120.1 kHz)
GRATIO = {"C13": 0.25145, "N15": -0.10136, "N14": 0.07224, "H2": 0.15351}   # gamma_X / gamma_1H
SPIN = {"C13": 0.5, "N15": 0.5, "N14": 1.0, "H2": 1.0}


# ------------------------------------------------------------------------------------------------ structure helpers
def read_all_atoms(pdb):
    """(name, resname, resid, element, xyz) for all atoms of the first model."""
    out = []
    with open(pdb) as f:
        for line in f:
            if line.startswith("ENDMDL"):
                break
            if not line.startswith(("ATOM", "HETATM")):
                continue
            el = line[76:78].strip() or line[12:16].strip()[0]
            out.append((line[12:16].strip(), line[17:20].strip(), int(line[22:26]), el,
                        (float(line[30:38]), float(line[38:46]), float(line[46:54]))))
    return out


def rotor_groups(atoms, hidx_of_atom):
    """3-site-jump groups: CH3 (methyl) and NH3+ (Lys NZ, N-terminus). Returns list of [h1,h2,h3] (H-list indices)."""
    heavy = [(k, a) for k, a in enumerate(atoms) if a[3] != "H"]
    hs = [(k, a) for k, a in enumerate(atoms) if a[3] == "H"]
    bonded = {}
    for k, a in hs:
        x = np.array(a[4])
        best, bd = None, 9.0
        for kk, b in heavy:
            if b[2] != a[2] and abs(b[2] - a[2]) > 1:
                continue
            d = np.linalg.norm(x - np.array(b[4]))
            if d < bd:
                bd, best = d, kk
        bonded.setdefault(best, []).append(k)
    groups = []
    for kk, hl in bonded.items():
        if len(hl) == 3 and atoms[kk][3] in ("C", "N"):
            groups.append([hidx_of_atom[k] for k in hl])
    return groups, bonded


def averaged_couplings(X, b0, groups):
    """Secular couplings averaged over independent fast 3-site jumps of each rotor group (first-order average
    Hamiltonian).  Same group: mean over the 3 cyclic states; different groups: mean over 3x3; rotor-static: mean over 3."""
    N = len(X)
    b0 = np.asarray(b0, float) / np.linalg.norm(b0)
    gid = -np.ones(N, int)
    P = [X.copy() for _ in range(3)]                  # P[r]: every rotor advanced by r sites
    for g, hl in enumerate(groups):
        for m, h in enumerate(hl):
            gid[h] = g
            for r in range(3):
                P[r][h] = X[hl[(m + r) % 3]]

    def cross(A, B):
        v = B[None, :, :] - A[:, None, :]
        r = np.linalg.norm(v, axis=2)
        np.fill_diagonal(r, 1.0)
        c = (v @ b0) / r
        C = D1A / r ** 3 * (3 * c * c - 1) / 2
        np.fill_diagonal(C, 0.0)
        return C

    C = {(r, s): cross(P[r], P[s]) for r in range(3) for s in range(3)}
    D = sum(C.values()) / 9.0                         # independent rotors (and rotor-static, static-static)
    same = (gid[:, None] == gid[None, :]) & (gid[:, None] >= 0)
    Dsame = (C[(0, 0)] + C[(1, 1)] + C[(2, 2)]) / 3.0  # same rotor: common rotation state
    D[same] = Dsame[same]
    np.fill_diagonal(D, 0.0)
    return 0.5 * (D + D.T)


def m2_global(D):
    """Van Vleck M2 (rad^2/s^2) for like spins-1/2 with H = sum d_ij (3 IzIz - I.I): (9/4) <sum_j d_ij^2>_i."""
    return 9.0 / 4.0 * float(np.mean(np.sum(D ** 2, axis=1)))


def check_m2_formulas(seed=0, N=6):
    """Dense-matrix check of M2_global = (9/4)<sum d^2>, M2_loc(I_y^a) = (5/4) sum_j d_aj^2, M2_loc(I_z^a) = (1/2) sum."""
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(N, 3)) * 2.0
    D = SP.couplings(X, (0, 0, 1))
    sx = np.array([[0, 1], [1, 0]], complex) / 2
    sy = np.array([[0, -1j], [1j, 0]], complex) / 2
    sz = np.array([[1, 0], [0, -1]], complex) / 2

    def op(s, q):
        m = np.array([[1.0]], complex)
        for k in range(N):
            m = np.kron(m, s if k == q else np.eye(2))
        return m
    Ix = [op(sx, q) for q in range(N)]; Iy = [op(sy, q) for q in range(N)]; Iz = [op(sz, q) for q in range(N)]
    H = sum(D[i, j] * (2 * Iz[i] @ Iz[j] - Ix[i] @ Ix[j] - Iy[i] @ Iy[j]) for i in range(N) for j in range(i + 1, N))

    def m2(A):
        C = H @ A - A @ H
        return float(np.real(-np.trace(C @ C) / np.trace(A @ A)))
    Iyt = sum(Iy)
    return dict(global_numeric=m2(Iyt), global_formula=m2_global(D),
                loc_y_numeric=m2(Iy[0]), loc_y_formula=1.25 * float(np.sum(D[0] ** 2)),
                loc_z_numeric=m2(Iz[0]), loc_z_formula=0.5 * float(np.sum(D[0] ** 2)))


def hetero_m2(xh, hetero_xyz, b0, kind):
    """Van Vleck unlike-spin M2 at a proton: (1/3) S(S+1) sum (D1A g (1-3cos^2)/r^3)^2  (rad^2/s^2)."""
    if len(hetero_xyz) == 0:
        return 0.0
    b0 = np.asarray(b0, float) / np.linalg.norm(b0)
    v = hetero_xyz - xh
    r = np.linalg.norm(v, axis=1)
    c = (v @ b0) / r
    dd = D1A * GRATIO[kind] * (1 - 3 * c * c) / r ** 3
    S = SPIN[kind]
    return float(S * (S + 1) / 3.0 * np.sum(dd ** 2))


# ------------------------------------------------------------------------------------------------ main
def main():
    out = dict(check=check_m2_formulas(), jobs=[])
    files = sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate", "*_N10_*_g0.json"))) + \
        sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate_hn", "*_g0.json")))
    cache = {}
    for f in files:
        d = json.load(open(f))
        if not any("FI_otoc_t" in p for p in d["params"]):
            continue
        hn = "HN" in os.path.basename(f)
        pdb = d["pdb"]
        key = pdb
        if key not in cache:
            pdbf = os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb")
            names, xyz, resid = SP.read_h_coords(pdbf)
            atoms = read_all_atoms(pdbf)
            hk = [k for k, a in enumerate(atoms) if a[3] == "H"]
            hidx_of_atom = {k: i for i, k in enumerate(hk)}
            groups, bonded = rotor_groups(atoms, hidx_of_atom)
            heavy_of_h = {}
            for kk, hl in bonded.items():
                for k in hl:
                    heavy_of_h[hidx_of_atom[k]] = kk
            cache[key] = (names, xyz, resid, atoms, groups, heavy_of_h)
        names, xyz, resid, atoms, groups, heavy_of_h = cache[key]
        b0 = np.array(d["b0"])
        amide = [i for i, n in enumerate(names) if n.startswith("H/")]
        if hn:
            net = amide                                   # perdeuterated: amide protons only
        else:
            net = list(range(len(names)))
        Xnet = xyz[net]
        # the job's cluster (indices refer to the job's H list = net list for HN jobs)
        cl = d["cluster"]
        Xc = Xnet[cl]
        Dc = SP.couplings(Xc, b0)
        Dn = SP.couplings(Xnet, b0)
        probe_net = cl[0]
        dt = d["dt"]
        times = np.array(d["times"])
        tco = d.get("best_t_c_otoc_index")
        tc_t = float(times[tco]) if tco is not None and tco < len(times) else None
        fio = np.sum([np.array(p["FI_otoc_t"]) for p in d["params"]], axis=0)
        fit = np.sum([np.array(p["FI_t"]) for p in d["params"]], axis=0)
        cum = np.cumsum(fio) / fio.sum()
        t50 = float(times[int(np.searchsorted(cum, 0.5))])
        frac_after = float(fio[tco:].sum() / fio.sum()) if tco is not None else None
        # M2s
        m2_cluster = m2_global(Dc)
        m2_net = m2_global(Dn)
        rec = dict(file=os.path.basename(f), pdb=pdb, hn_only=hn, probe=d["probe_name"], N=d["N"],
                   orient=d["orient"], t_c_echo_us=None if tc_t is None else tc_t * 1e6, t50_echo_us=t50 * 1e6,
                   frac_echoFI_after_tc=frac_after, FI_echo_total=float(fio.sum()), FI_transfer_total=float(fit.sum()),
                   t_max_us=float(times[-1] * 1e6),
                   dmax_cluster_kHz=float(np.abs(Dc).max() / 2 / math.pi / 1e3),
                   dprobe_max_kHz=float(np.abs(Dc[0]).max() / 2 / math.pi / 1e3),
                   dnn_median_cluster_kHz=float(np.median(np.abs(Dc).max(axis=1)) / 2 / math.pi / 1e3),
                   T2_cluster_us=1e6 / math.sqrt(m2_cluster),
                   T2_network_static_us=1e6 / math.sqrt(m2_net),
                   T2_loc_probe_cluster_us=1e6 / math.sqrt(1.25 * np.sum(Dc[0] ** 2)),
                   T2_loc_probe_network_us=1e6 / math.sqrt(1.25 * np.sum(Dn[probe_net] ** 2)),
                   Tz_loc_probe_network_us=1e6 / math.sqrt(0.5 * np.sum(Dn[probe_net] ** 2)),
                   sqrtM2_network_kHz=math.sqrt(m2_net) / 2 / math.pi / 1e3,
                   gauss_FWHM_network_kHz=2.3548 * math.sqrt(m2_net) / 2 / math.pi / 1e3)
        if not hn:
            # methyl / NH3 rotor averaging (fast 3-site jumps)
            Dm = averaged_couplings(xyz, b0, groups)
            rec["T2_network_rotoravg_us"] = 1e6 / math.sqrt(m2_global(Dm))
            clg = [g for g in groups if any(h in cl for h in g)]
            rec["n_rotor_protons_in_cluster"] = int(sum(1 for i in cl if any(i in g for g in groups)))
            # cluster couplings with rotor averaging (using full-protein rotor positions)
            Dma = Dm[np.ix_(cl, cl)]
            rec["rotoravg_max_abs_change_kHz"] = float(np.abs(Dma - Dc).max() / 2 / math.pi / 1e3)
            rec["rotoravg_rel_frob_change"] = float(np.linalg.norm(Dma - Dc) / np.linalg.norm(Dc))
            rec["_rotor_groups_in_cluster"] = [[names[h] for h in g] for g in clg]
        # heteronuclear local fields at the probe
        pidx_full = amide[probe_net] if hn else probe_net
        xh = xyz[pidx_full]
        Cx = np.array([a[4] for a in atoms if a[3] == "C"])
        Nx = np.array([a[4] for a in atoms if a[3] == "N"])
        if hn:
            # perdeuterated: every non-amide H is 2H
            Dx = np.array([xyz[i] for i in range(len(names)) if i not in set(amide)])
            m2_hd = hetero_m2(xh, Dx, b0, "H2")
            m2_hn15 = hetero_m2(xh, Nx, b0, "N15")
            m2_hn14 = hetero_m2(xh, Nx, b0, "N14")
            m2_hh = 1.25 * float(np.sum(Dn[probe_net] ** 2))
            rec.update(hetero_sqrtM2_kHz=dict(H2_perdeut=math.sqrt(m2_hd) / 2 / math.pi / 1e3,
                                              N15_uniform=math.sqrt(m2_hn15) / 2 / math.pi / 1e3,
                                              N14_natural=math.sqrt(m2_hn14) / 2 / math.pi / 1e3),
                       homo_loc_sqrtM2_kHz=math.sqrt(m2_hh) / 2 / math.pi / 1e3)
        else:
            m2_hc = hetero_m2(xh, Cx, b0, "C13")
            m2_hn15 = hetero_m2(xh, Nx, b0, "N15")
            m2_hn14 = hetero_m2(xh, Nx, b0, "N14")
            m2_hh = 1.25 * float(np.sum(Dn[probe_net] ** 2))
            rec.update(hetero_sqrtM2_kHz=dict(C13_uniform=math.sqrt(m2_hc) / 2 / math.pi / 1e3,
                                              N15_uniform=math.sqrt(m2_hn15) / 2 / math.pi / 1e3,
                                              N14_natural=math.sqrt(m2_hn14) / 2 / math.pi / 1e3),
                       homo_loc_sqrtM2_kHz=math.sqrt(m2_hh) / 2 / math.pi / 1e3)
        # dimensionless window positions
        for T2key in ("T2_cluster_us", "T2_network_static_us") + (("T2_network_rotoravg_us",) if not hn else ()):
            T2v = rec[T2key]
            rec[f"tc_over_{T2key[:-3]}"] = None if tc_t is None else rec["t_c_echo_us"] / T2v
            rec[f"t50_over_{T2key[:-3]}"] = rec["t50_echo_us"] / T2v
        out["jobs"].append(rec)
        print(json.dumps({k: (round(v, 3) if isinstance(v, float) else v) for k, v in rec.items()
                          if not k.startswith("_") and not isinstance(v, dict)}))
    # whole-protein powder-averaged T2 (orientation average of (P2)^2 = 1/5 relative to the aligned maximum)
    pw = {}
    for pdb in sorted(cache):
        names, xyz, resid, atoms, groups, _ = cache[pdb]
        rng = np.random.default_rng(5)
        vals, valsm, valshn = [], [], []
        amide = [i for i, n in enumerate(names) if n.startswith("H/")]
        for _ in range(12):
            v = rng.normal(size=3); v /= np.linalg.norm(v)
            vals.append(m2_global(SP.couplings(xyz, v)))
            valsm.append(m2_global(averaged_couplings(xyz, v, groups)))
            valshn.append(m2_global(SP.couplings(xyz[amide], v)))
        pw[pdb] = dict(T2_static_us=1e6 / math.sqrt(np.mean(vals)), T2_rotoravg_us=1e6 / math.sqrt(np.mean(valsm)),
                       T2_amideonly_us=1e6 / math.sqrt(np.mean(valshn)), n_H=len(names), n_amide=len(amide),
                       n_rotor_groups=len(groups))
    out["powder_average"] = pw
    print(json.dumps(pw))
    print(json.dumps(out["check"]))
    json.dump(out, open(os.path.join(HERE, "scales.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
