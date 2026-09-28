"""Metalloprotein active-site census and structural-lever measurements from the PDB.

Lane: ROUND3/new_mechanisms_intrinsic. Single-threaded, < 1 CPU-min.

Part A (census). For each metal cluster in a curated set of PDB entries:
  metals, bridging atoms, terminal first-shell ligands, second-shell residues,
  heavy atoms within 6/8 A (a proxy for converged QM-region size), and an
  active-space estimate AS_dp = 5 * (#open-shell-capable d metals) + 3 * (#bridging
  main-group atoms) (+4 porphyrin pi orbitals for a heme). AS_dp is calibrated
  against literature active spaces in README (calibration table).
Part B (levers). How much structure moves when the electronic state changes:
  Mb/Hb deoxy (high-spin Fe(II)) vs oxy (low-spin), P-cluster PN vs POX, FeMoco
  resting vs CO-bound, hemocyanin deoxy vs oxy, PSII OEC dark vs 2-flash (S3).
Part C (short H-bond census) for the proton-delocalisation branch.

PDB files are cached in a scratch directory (env QAPF_PDB_CACHE, default: ../pdb_cache,
which is NOT used if the env var is set). All inputs are experimental structures, used
here only for scientific analysis (no optimisation, no selection), per the charter.
Output: ../results/pdb_census.json (atomic write).
"""
from __future__ import annotations

import json
import os
import urllib.request
from collections import defaultdict

import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "results")
CACHE = os.environ.get("QAPF_PDB_CACHE", os.path.join(HERE, "..", "pdb_cache"))

OPEN_SHELL_TM = {"FE", "MO", "MN", "CU", "NI", "CO", "V", "W"}
OTHER_METALS = {"CA", "MG", "ZN", "NA", "K"}
CUT = {"S": 2.65, "O": 2.45, "N": 2.35, "C": 2.25, "CL": 2.7}  # TM-ligand bond cutoffs (A)
CUT_CA = {"O": 2.75, "N": 2.75}
MM_CUT = 3.0  # direct metal-metal contact

CENSUS_IDS = ["3U7Q", "3MIN", "2MIN", "4TKV", "3WU2", "6JLJ", "6JLL", "2CPP", "1A6N", "1A6M",
              "2HHB", "1OXY", "1LLA", "1MTY", "3C8Y", "1WUI", "1JJY", "1FDN", "1A70", "1PLC"]


def fetch(pid: str) -> str:
    os.makedirs(CACHE, exist_ok=True)
    p = os.path.join(CACHE, f"{pid}.pdb")
    if not os.path.exists(p) or os.path.getsize(p) == 0:
        req = urllib.request.Request(f"https://files.rcsb.org/download/{pid}.pdb",
                                     headers={"User-Agent": "qapf-research/0.1"})
        with urllib.request.urlopen(req, timeout=120) as r, open(p + ".tmp", "wb") as f:
            f.write(r.read())
        os.replace(p + ".tmp", p)
    return p


def parse(pid: str) -> dict:
    path = fetch(pid)
    atoms = []
    title, res = [], None
    seen = set()
    with open(path, encoding="latin-1") as f:
        for ln in f:
            rec = ln[:6]
            if rec == "TITLE ":
                title.append(ln[10:80].strip())
            elif ln.startswith("REMARK   2 RESOLUTION"):
                try:
                    res = float(ln[23:30])
                except ValueError:
                    pass
            elif rec == "ENDMDL":
                break
            elif rec in ("ATOM  ", "HETATM"):
                alt = ln[16]
                name = ln[12:16].strip()
                resn = ln[17:20].strip()
                chain = ln[21]
                resi = int(ln[22:26])
                icode = ln[26]
                key = (chain, resi, icode, resn, name)
                if key in seen:  # keep the first altloc only
                    continue
                if alt not in (" ", "A", "1"):
                    continue
                seen.add(key)
                el = ln[76:78].strip().upper() or "".join(c for c in name if c.isalpha())[:2].upper()
                atoms.append(dict(het=rec == "HETATM", name=name, resn=resn, chain=chain, resi=resi,
                                  icode=icode, xyz=(float(ln[30:38]), float(ln[38:46]), float(ln[46:54])),
                                  occ=float(ln[54:60] or 1.0), el=el))
    X = np.array([a["xyz"] for a in atoms])
    return dict(pid=pid, title=" ".join(title), resolution=res, atoms=atoms, X=X, tree=cKDTree(X))


def bonded(el_lig: str, el_m: str, d: float) -> bool:
    if el_m == "CA":
        return d <= CUT_CA.get(el_lig, 0.0)
    return d <= CUT.get(el_lig, 0.0)


def clusters(S: dict) -> list[dict]:
    A, X, T = S["atoms"], S["X"], S["tree"]
    tm = [i for i, a in enumerate(A) if a["el"] in OPEN_SHELL_TM]
    ca = [i for i, a in enumerate(A) if a["el"] == "CA" and a["het"]]
    metals = tm + ca
    lig_of = {}  # metal -> set of bonded non-metal atom indices
    for m in metals:
        s = set()
        for j in T.query_ball_point(X[m], 2.8):
            if j == m or A[j]["el"] in OPEN_SHELL_TM | OTHER_METALS or A[j]["el"] == "H":
                continue
            if bonded(A[j]["el"], A[m]["el"], float(np.linalg.norm(X[j] - X[m]))):
                s.add(j)
        lig_of[m] = s
    # union-find over TMs (Ca joins only through >= 2 shared bridges)
    parent = {m: m for m in metals}

    def find(u):
        while parent[u] != u:
            parent[u] = parent[parent[u]]
            u = parent[u]
        return u

    for a_ in tm:
        for b_ in tm:
            if a_ < b_:
                d = float(np.linalg.norm(X[a_] - X[b_]))
                if d < MM_CUT or (d < 4.2 and lig_of[a_] & lig_of[b_]):
                    parent[find(a_)] = find(b_)
    for c in ca:
        for m in tm:
            if len(lig_of[c] & lig_of[m]) >= 1 and float(np.linalg.norm(X[c] - X[m])) < 4.0:
                parent[find(c)] = find(m)
    groups = defaultdict(list)
    for m in metals:
        groups[find(m)].append(m)
    out = []
    for g in groups.values():
        tms = [m for m in g if A[m]["el"] in OPEN_SHELL_TM]
        if not tms:
            continue
        cnt = defaultdict(int)
        for m in g:
            for j in lig_of[m]:
                cnt[j] += 1
        bridges = sorted(j for j, c in cnt.items() if c >= 2)
        terminal = sorted(j for j, c in cnt.items() if c == 1)
        core = set(g) | set(bridges)
        first = core | set(terminal)
        resn = sorted({A[m]["resn"] for m in g} | {A[j]["resn"] for j in bridges})
        heme = any(A[m]["resn"] in ("HEM", "HEA", "HEC") for m in g)
        # second shell: residues with an atom within 4.5 A of the first shell, not ligand residues
        lig_res = {(A[j]["chain"], A[j]["resi"], A[j]["resn"]) for j in first}
        sec = set()
        for j in first:
            for k in T.query_ball_point(X[j], 4.5):
                r = (A[k]["chain"], A[k]["resi"], A[k]["resn"])
                if r not in lig_res and A[k]["resn"] != "HOH":
                    sec.add(r)
        cen = X[sorted(core)]
        near6, near8 = set(), set()
        for p in cen:
            near6.update(T.query_ball_point(p, 6.0))
            near8.update(T.query_ball_point(p, 8.0))
        heavy6 = sum(1 for k in near6 if A[k]["el"] != "H")
        heavy8 = sum(1 for k in near8 if A[k]["el"] != "H")
        n_tm = len(tms)
        n_br_main = sum(1 for j in bridges if A[j]["el"] in ("S", "O", "C", "N"))
        as_d = 5 * n_tm
        as_dp = as_d + 3 * n_br_main + (4 if heme else 0)
        el_cnt = defaultdict(int)
        for m in g:
            el_cnt[A[m]["el"]] += 1
        br_cnt = defaultdict(int)
        for j in bridges:
            br_cnt[A[j]["el"]] += 1
        mm = [float(np.linalg.norm(X[a_] - X[b_])) for i_, a_ in enumerate(tms) for b_ in tms[i_ + 1:]]
        out.append(dict(
            residues=resn, chain=A[g[0]]["chain"], resi=A[g[0]]["resi"],
            metals=dict(el_cnt), n_open_shell_tm=n_tm, bridges=dict(br_cnt), n_bridges=len(bridges),
            n_terminal_ligands=len(terminal), heme=heme,
            terminal_ligand_residues=sorted({f"{A[j]['resn']}{A[j]['resi']}{A[j]['chain']}:{A[j]['name']}" for j in terminal}),
            n_second_shell_residues=len(sec),
            heavy_atoms_within_6A=heavy6, heavy_atoms_within_8A=heavy8,
            est_atoms_with_H_within_8A=2 * heavy8,
            AS_d_orbitals=as_d, AS_dp_orbitals=as_dp,
            metal_metal_min=min(mm) if mm else None, metal_metal_max=max(mm) if mm else None,
            coords={f"{A[m]['el']}{k}": [round(v, 3) for v in X[m]] for k, m in enumerate(g)},
        ))
    return out


def kabsch(P: np.ndarray, Q: np.ndarray):
    """Return R, t minimising |R P + t - Q|."""
    pc, qc = P.mean(0), Q.mean(0)
    H = (P - pc).T @ (Q - qc)
    U, _, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    return R, qc - R @ pc


def atom(S, chain, resi, name, resn=None):
    for a, x in zip(S["atoms"], S["X"]):
        if a["chain"] == chain and a["resi"] == resi and a["name"] == name and (resn is None or a["resn"] == resn):
            return x
    return None


def heme_metrics(S, chain, prox_resi):
    """Fe displacement from the 4-pyrrole-N plane toward the proximal His NE2 (A)."""
    hem = [(a, x) for a, x in zip(S["atoms"], S["X"]) if a["chain"] == chain and a["resn"] == "HEM"]
    d = {a["name"]: x for a, x in hem}
    fe = d.get("FE")
    Ns = [d.get(n) for n in ("NA", "NB", "NC", "ND")]
    if fe is None or any(n is None for n in Ns):
        return None
    Ns = np.array(Ns)
    c = Ns.mean(0)
    _, _, vt = np.linalg.svd(Ns - c)
    nrm = vt[2]
    ne2 = atom(S, chain, prox_resi, "NE2")
    if np.dot(ne2 - c, nrm) < 0:
        nrm = -nrm
    # 24-atom porphyrin core plane
    core_names = ["NA", "NB", "NC", "ND", "C1A", "C2A", "C3A", "C4A", "C1B", "C2B", "C3B", "C4B",
                  "C1C", "C2C", "C3C", "C4C", "C1D", "C2D", "C3D", "C4D", "CHA", "CHB", "CHC", "CHD"]
    core = np.array([d[n] for n in core_names if n in d])
    c24 = core.mean(0)
    _, _, vt24 = np.linalg.svd(core - c24)
    n24 = vt24[2] if np.dot(ne2 - c24, vt24[2]) > 0 else -vt24[2]
    return dict(fe_oop_N4=float(np.dot(fe - c, nrm)), fe_oop_core24=float(np.dot(fe - c24, n24)),
                fe_Np_mean=float(np.mean(np.linalg.norm(Ns - fe, axis=1))),
                fe_NE2_prox=float(np.linalg.norm(ne2 - fe)))


def ca_map(S, chain):
    return {(a["resi"], a["icode"]): x for a, x in zip(S["atoms"], S["X"])
            if a["chain"] == chain and a["name"] == "CA" and not a["het"]}


def ca_shift_profile(S1, S2, chain1, chain2, fe_ref, groups):
    """Superpose chain CA sets; CA shifts vs distance from Fe (in S1 frame)."""
    m1, m2 = ca_map(S1, chain1), ca_map(S2, chain2)
    keys = sorted(set(m1) & set(m2))
    P = np.array([m2[k] for k in keys])
    Q = np.array([m1[k] for k in keys])
    R, t = kabsch(P, Q)
    P2 = P @ R.T + t
    sh = np.linalg.norm(P2 - Q, axis=1)
    dist = np.linalg.norm(Q - fe_ref, axis=1)
    bins = [(0, 8), (8, 12), (12, 16), (16, 20), (20, 99)]
    prof = {f"{lo}-{hi}A": dict(n=int(((dist >= lo) & (dist < hi)).sum()),
                               median=float(np.median(sh[(dist >= lo) & (dist < hi)])) if ((dist >= lo) & (dist < hi)).any() else None,
                               p90=float(np.percentile(sh[(dist >= lo) & (dist < hi)], 90)) if ((dist >= lo) & (dist < hi)).any() else None)
            for lo, hi in bins}
    grp = {}
    for gname, (lo, hi) in groups.items():
        sel = [i for i, k in enumerate(keys) if lo <= k[0] <= hi]
        grp[gname] = dict(mean=float(sh[sel].mean()), max=float(sh[sel].max()), n=len(sel))
    return dict(n_ca=len(keys), rmsd_all=float(np.sqrt((sh ** 2).mean())), profile=prof, groups=grp)


def lever_heme():
    out = {}
    mbD, mbO = parse("1A6N"), parse("1A6M")
    hD, hO = heme_metrics(mbD, "A", 93), heme_metrics(mbO, "A", 93)
    fe = [x for a, x in zip(mbD["atoms"], mbD["X"]) if a["resn"] == "HEM" and a["name"] == "FE"][0]
    prof = ca_shift_profile(mbD, mbO, "A", "A", fe, {"F_helix_82-97": (82, 97), "His93": (93, 93),
                                                   "E_helix_58-77": (58, 77), "far_A_helix_3-18": (3, 18)})
    out["myoglobin_1A6N_deoxy_vs_1A6M_oxy"] = dict(deoxy=hD, oxy=hO, d_fe_oop_N4=hD["fe_oop_N4"] - hO["fe_oop_N4"],
                                                   ca_shifts=prof)
    hbD, hbO = parse("2HHB"), parse("1HHO")
    res = {}
    for sub, chD, chO, prox, fgrp in (("alpha", "A", "A", 87, (80, 89)), ("beta", "B", "B", 92, (85, 94))):
        mD, mO = heme_metrics(hbD, chD, prox), heme_metrics(hbO, chO, prox)
        fe = [x for a, x in zip(hbD["atoms"], hbD["X"]) if a["resn"] == "HEM" and a["name"] == "FE" and a["chain"] == chD][0]
        pr = ca_shift_profile(hbD, hbO, chD, chO, fe, {"F_helix": fgrp, "proximal_His": (prox, prox)})
        res[sub] = dict(deoxy=mD, oxy=mO, d_fe_oop_N4=(mD["fe_oop_N4"] - mO["fe_oop_N4"]) if mD and mO else None,
                        ca_shifts_subunit_superposed=pr)
    out["hemoglobin_2HHB_deoxyT_vs_1HHO_oxyR"] = res
    return out


def fe_list(S, resn_set, chain=None):
    return [(a, x) for a, x in zip(S["atoms"], S["X"]) if a["resn"] in resn_set and a["el"] in ("FE", "MO")
            and (chain is None or a["chain"] == chain)]


def lever_pcluster():
    out = {}
    for pid, label in (("3MIN", "PN_reduced"), ("2MIN", "POX_oxidized")):
        S = parse(pid)
        pcs = defaultdict(list)
        for a, x in zip(S["atoms"], S["X"]):
            if a["resn"] in ("CLF", "1CL") and a["el"] == "FE":
                pcs[(a["chain"], a["resi"])].append(x)
        res = []
        for (ch, ri), fes in sorted(pcs.items()):
            fes = np.array(fes)
            dd = sorted(float(np.linalg.norm(fes[i] - fes[j])) for i in range(len(fes)) for j in range(i + 1, len(fes)))
            # ligand-switch probes: Ser beta188 OG and Cys alpha88 backbone N (chains: alpha A/C, beta B/D)
            beta = "B" if ch in ("A", "B") else "D"
            alpha = "A" if ch in ("A", "B") else "C"
            og = atom(S, beta, 188, "OG")
            n88 = atom(S, alpha, 88, "N")
            res.append(dict(chain=ch, resi=ri, n_fe=len(fes), fe_fe_sorted=[round(v, 3) for v in dd],
                            n_fe_fe_below_2p9=int(sum(v < 2.9 for v in dd)),
                            min_fe_serB188_OG=float(np.min(np.linalg.norm(fes - og, axis=1))) if og is not None else None,
                            min_fe_cysA88_N=float(np.min(np.linalg.norm(fes - n88, axis=1))) if n88 is not None else None))
        out[f"{pid}_{label}"] = dict(resolution=S["resolution"], clusters=res)
    return out


def lever_femoco():
    out = {}
    for pid in ("3U7Q", "4TKV"):
        S = parse(pid)
        cof = defaultdict(dict)
        for a, x in zip(S["atoms"], S["X"]):
            if a["resn"] in ("ICS", "ICE"):
                cof[(a["chain"], a["resi"])][a["name"]] = x
        lig = defaultdict(list)
        for a, x in zip(S["atoms"], S["X"]):
            if a["het"] and a["resn"] not in ("ICS", "ICE", "HOH", "CLF", "1CL", "HCA", "CA", "MG", "IMD", "GOL", "SO4", "CL") :
                lig[a["resn"]].append((a["chain"], a["resi"], a["name"], x))
        rec = []
        for (ch, ri), d in sorted(cof.items()):
            fe2, fe6 = d.get("FE2"), d.get("FE6")
            nearby = []
            if fe2 is not None and fe6 is not None:
                mid = (fe2 + fe6) / 2
                for resn, lst in lig.items():
                    for (c2, r2, nm, x) in lst:
                        if np.linalg.norm(x - mid) < 2.5:
                            nearby.append(f"{resn}{r2}{c2}:{nm}")
            rec.append(dict(chain=ch, resi=ri, atoms=sorted(d.keys()), has_S2B="S2B" in d,
                            fe2_fe6=float(np.linalg.norm(fe2 - fe6)) if fe2 is not None and fe6 is not None else None,
                            bridging_non_cofactor_ligand_near_Fe2Fe6=nearby))
        out[pid] = dict(title=S["title"], resolution=S["resolution"], cofactors=rec,
                        het_groups=sorted(lig.keys()))
    return out


def lever_hemocyanin():
    out = {}
    for pid in ("1LLA", "1OXY"):
        S = parse(pid)
        cu = [(a, x) for a, x in zip(S["atoms"], S["X"]) if a["el"] == "CU"]
        pairs = []
        for i in range(len(cu)):
            for j in range(i + 1, len(cu)):
                d = float(np.linalg.norm(cu[i][1] - cu[j][1]))
                if d < 6.0:
                    pairs.append(dict(a=f"{cu[i][0]['chain']}{cu[i][0]['resi']}", b=f"{cu[j][0]['chain']}{cu[j][0]['resi']}", d=d))
        out[pid] = dict(title=S["title"], resolution=S["resolution"], cu_cu=pairs)
    return out


def lever_oec():
    out = {}
    for pid in ("3WU2", "6JLJ", "6JLL"):
        S = parse(pid)
        oex = defaultdict(dict)
        for a, x in zip(S["atoms"], S["X"]):
            if a["resn"] == "OEX":
                oex[(a["chain"], a["resi"])][a["name"]] = x
        rec = []
        for (ch, ri), d in sorted(oex.items()):
            mn = {k: v for k, v in d.items() if k.startswith("MN")}
            names = sorted(mn)
            mm = {f"{p}-{q}": round(float(np.linalg.norm(mn[p] - mn[q])), 3) for i, p in enumerate(names) for q in names[i + 1:]}
            # extra oxygen near Mn1 (O6/OX insertion) from any non-OEX het/water within 2.3 A of an Mn
            extra = []
            for a, x in zip(S["atoms"], S["X"]):
                if a["resn"] != "OEX" and a["el"] == "O" and a["het"]:
                    for k, v in mn.items():
                        dd = float(np.linalg.norm(x - v))
                        if dd < 2.3:
                            extra.append(f"{a['resn']}{a['resi']}{a['chain']}:{a['name']}-{k}:{dd:.2f}")
            rec.append(dict(chain=ch, resi=ri, atoms=sorted(d.keys()), mn_mn=mm, extra_O_within_2p3_of_Mn=extra))
        out[pid] = dict(title=S["title"], resolution=S["resolution"], oec=rec)
    return out


def short_hbonds(pid: str, cutoff: float = 2.60):
    S = parse(pid)
    A, X, T = S["atoms"], S["X"], S["tree"]
    idx = [i for i, a in enumerate(A) if a["el"] in ("O", "N") and a["resn"] != "HOH"]
    sub = cKDTree(X[idx])
    pairs = []
    for i, j in sub.query_pairs(cutoff):
        a, b = A[idx[i]], A[idx[j]]
        if (a["chain"], a["resi"]) == (b["chain"], b["resi"]):
            continue
        if abs(a["resi"] - b["resi"]) == 1 and a["chain"] == b["chain"] and {a["name"], b["name"]} & {"N", "O"} == {"N", "O"} and a["name"] in ("N", "O") and b["name"] in ("N", "O"):
            continue  # peptide-bond neighbours
        d = float(np.linalg.norm(X[idx[i]] - X[idx[j]]))
        pairs.append(dict(a=f"{a['resn']}{a['resi']}{a['chain']}:{a['name']}", b=f"{b['resn']}{b['resi']}{b['chain']}:{b['name']}", d=round(d, 3)))
    return dict(title=S["title"], resolution=S["resolution"], cutoff=cutoff, pairs=sorted(pairs, key=lambda p: p["d"]))


def main():
    os.makedirs(OUT, exist_ok=True)
    census = {}
    for pid in CENSUS_IDS:
        S = parse(pid)
        cl = clusters(S)
        # keep one representative per site composition (first occurrence)
        seen, rep = set(), []
        for c in sorted(cl, key=lambda c: (-c["n_open_shell_tm"], c["chain"], c["resi"])):
            key = (tuple(c["residues"]), tuple(sorted(c["metals"].items())))
            c["n_copies"] = sum(1 for d in cl if (tuple(d["residues"]), tuple(sorted(d["metals"].items()))) == key)
            if key not in seen:
                seen.add(key)
                rep.append(c)
        census[pid] = dict(title=S["title"], resolution=S["resolution"], sites=rep)
    levers = dict(heme=lever_heme(), p_cluster=lever_pcluster(), femoco=lever_femoco(),
                  hemocyanin=lever_hemocyanin(), oec=lever_oec())
    sshb = {pid: short_hbonds(pid) for pid in ("1NWZ", "1OH0", "1EMA")}
    res = dict(census=census, levers=levers, short_hbonds=sshb)
    p = os.path.join(OUT, "pdb_census.json")
    with open(p + ".tmp", "w", encoding="utf-8") as f:
        json.dump(res, f, indent=1, default=float)
    os.replace(p + ".tmp", p)
    # compact console summary
    for pid, blk in census.items():
        for c in blk["sites"]:
            print(f"{pid} {'/'.join(c['residues']):<14} TM={c['n_open_shell_tm']:<2} metals={dict(c['metals'])} br={dict(c['bridges'])} "
                  f"AS_d={c['AS_d_orbitals']:<3} AS_dp={c['AS_dp_orbitals']:<3} 2nd={c['n_second_shell_residues']:<3} heavy8A={c['heavy_atoms_within_8A']} x{c['n_copies']}")


if __name__ == "__main__":
    main()
