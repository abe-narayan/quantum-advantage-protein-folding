"""T2: coupled methyl-rotor tunnelling in a protein core (1UBQ, OpenMM-protonated).

Physics (DERIVED): each CH3 rotor's potential is invariant under a 2pi/3 rotation of that rotor alone
(its three protons are identical), so H commutes with every per-rotor C3 generator; the labels
sigma_i = m_i mod 3 are conserved and H is block-diagonal in 3^N symmetry sectors.
The lowest state of each sector gives the tunnelling band E(sigma_1..sigma_N).

Test: exact 2-rotor sector energies for the most strongly coupled methyl pairs, non-additivity
J = E(s1,s2) - E(s1,0) - E(0,s2) + E(0,0), Hartree mean-field error, single-rotor splitting Delta(V3);
one 3-rotor cluster by Lanczos. Pair potential: AMBER-type LJ (HC: R*=1.487 A, eps=0.0157 kcal/mol)
plus optional Coulomb (q_H=+0.06 e, eps_r=1 worst case)."""
import json
import math
import os
import numpy as np

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), *[".."] * 5))
PDB = os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb")
KCAL_MEV = 43.364  # 1 kcal/mol in meV
HBAR2_AMU_A2_MEV = 4.1804  # hbar^2 / (1 amu * 1 A^2) in meV
M_H = 1.00784
RMIN_HH, EPS_HH = 2 * 1.487, 0.0157 * KCAL_MEV
COUL_MEV_A = 14399.6  # e^2/(4 pi eps0) in meV*A
METHYLS = {
    "ALA": [("CB", "CA", ["HB1", "HB2", "HB3"])],
    "VAL": [("CG1", "CB", ["HG11", "HG12", "HG13"]), ("CG2", "CB", ["HG21", "HG22", "HG23"])],
    "LEU": [("CD1", "CG", ["HD11", "HD12", "HD13"]), ("CD2", "CG", ["HD21", "HD22", "HD23"])],
    "ILE": [("CG2", "CB", ["HG21", "HG22", "HG23"]), ("CD1", "CG1", ["HD11", "HD12", "HD13"])],
    "THR": [("CG2", "CB", ["HG21", "HG22", "HG23"])],
    "MET": [("CE", "SD", ["HE1", "HE2", "HE3"])],
}


def atomic_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    os.replace(tmp, path)


def load_methyls():
    atoms = {}
    for line in open(PDB):
        if line.startswith("ATOM"):
            name, res, rid = line[12:16].strip(), line[17:20].strip(), int(line[22:26])
            atoms[(rid, name)] = (res, np.array([float(line[30:38]), float(line[38:46]), float(line[46:54])]))
    out = []
    for (rid, name), (res, xyz) in atoms.items():
        for c, p, hs in METHYLS.get(res, []):
            if name == c:
                H = np.array([atoms[(rid, h)][1] for h in hs])
                P = atoms[(rid, p)][1]
                u = xyz - P
                u /= np.linalg.norm(u)
                rperp = np.linalg.norm((H - xyz) - np.outer((H - xyz) @ u, u), axis=1)
                I = 3 * M_H * float(np.mean(rperp ** 2))
                out.append({"id": f"{res}{rid}:{c}", "C": xyz, "u": u, "H": H, "B": HBAR2_AMU_A2_MEV / (2 * I)})
    return out


def rot(u, phi, v):
    """Rodrigues rotation of vectors v (n,3) about unit axis u by angle phi."""
    c, s = math.cos(phi), math.sin(phi)
    return v * c + np.cross(u, v) * s + np.outer(v @ u, u) * (1 - c)


def h_positions(m, phi):
    return m["C"] + rot(m["u"], phi, m["H"] - m["C"])


def pair_energy(ha, hb, coul):
    d = np.linalg.norm(ha[:, None, :] - hb[None, :, :], axis=-1)
    x = (RMIN_HH / d) ** 6
    e = EPS_HH * (x * x - 2 * x)
    if coul:
        e = e + COUL_MEV_A * 0.06 * 0.06 / d
    return float(e.sum())


def coupling_grid(m1, m2, G, coul):
    phis = 2 * np.pi * np.arange(G) / G
    P1 = [h_positions(m1, p) for p in phis]
    P2 = [h_positions(m2, p) for p in phis]
    V = np.empty((G, G))
    for a in range(G):
        for b in range(G):
            V[a, b] = pair_energy(P1[a], P2[b], coul)
    return V


def v3_grid(V3, G):
    phis = 2 * np.pi * np.arange(G) / G
    return V3 / 2 * (1 - np.cos(3 * phis))


def single_sector(B, M, sigma, vgrid):
    """Single rotor H = B m^2 + V(phi) (V on a uniform grid of size G) in symmetry sector sigma.
    Returns eigenvalues, eigenvectors, m list."""
    G = len(vgrid)
    vhat = np.fft.fft(vgrid) / G
    ms = np.array([m for m in range(-M, M + 1) if m % 3 == sigma % 3])
    P = (ms[:, None] - ms[None, :]) % G
    H = vhat[P].astype(complex)
    H[np.diag_indices_from(H)] += B * ms.astype(float) ** 2
    H = 0.5 * (H + H.conj().T)
    w, v = np.linalg.eigh(H)
    return w, v, ms


def density_on_grid(vec, ms, G):
    phis = 2 * np.pi * np.arange(G) / G
    psi = np.exp(1j * np.outer(phis, ms)) @ vec
    rho = np.abs(psi) ** 2
    return rho / rho.sum()


def splitting(V3, B, M=90, G=720):
    vg = v3_grid(V3, G)
    return single_sector(B, M, 1, vg)[0][0] - single_sector(B, M, 0, vg)[0][0]


def two_rotor_sector_energies(V3a, V3b, Ba, Bb, Vhat, M, sectors):
    """Exact lowest energy per sector for H = sum B m^2 + V3 terms + V12, V12 given by 2D Fourier
    coefficients Vhat[p % G, q % G] (numpy FFT convention / G^2)."""
    G = Vhat.shape[0]
    out = {}
    for s1, s2 in sectors:
        m1 = np.array([m for m in range(-M, M + 1) if m % 3 == s1 % 3])
        m2 = np.array([m for m in range(-M, M + 1) if m % 3 == s2 % 3])
        A1, A2 = np.meshgrid(m1, m2, indexing="ij")
        a1, a2 = A1.ravel(), A2.ravel()
        P = (a1[:, None] - a1[None, :]) % G
        Q = (a2[:, None] - a2[None, :]) % G
        H = Vhat[P, Q].astype(complex)
        dp = a1[:, None] - a1[None, :]
        dq = a2[:, None] - a2[None, :]
        H += np.where((np.abs(dp) == 3) & (dq == 0), -V3a / 4, 0)
        H += np.where((np.abs(dq) == 3) & (dp == 0), -V3b / 4, 0)
        H[np.diag_indices_from(H)] += Ba * a1 ** 2 + Bb * a2 ** 2 + V3a / 2 + V3b / 2
        H = 0.5 * (H + H.conj().T)
        out[(s1, s2)] = float(np.linalg.eigvalsh(H)[0])
    return out
