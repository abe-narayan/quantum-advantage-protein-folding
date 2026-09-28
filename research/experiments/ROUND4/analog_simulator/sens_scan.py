"""Error-sensitivity scan of the protein 1H echo F_ab(t) to analog-simulator imperfections (exact, continuous time).

Each unit = (channel, level, rep) -> S_ab(t) for b in the instrument sites and t in --times (us); results are stored
unit-by-unit in sens_<pdb>_p<probe>_N<N>.json (atomic tmp+replace), so a killed run resumes where it stopped.

Channels (all errors relative to the target H_dd; 'shared' = identical in forward and backward legs, i.e. the device
reverses its own wrong Hamiltonian exactly; 'indep'/'nonrev' = the backward leg differs):
  iid_shared   d_ij -> d_ij (1 + level*eps_ij), both legs            (static coupling calibration error)
  iid_indep    independent eps for forward and backward               (shot/leg-dependent coupling noise)
  pos_shared   r_i -> r_i + level*r_min*xi_i (3D), both legs          (static trap-placement error; angles included)
  pos_indep    independent displacements per leg                       (atomic motion between legs)
  scale        backward Hamiltonian = (1+level) * forward              (reversal-rate / C3-ratio miscalibration)
  heis_rev     H_dd + level*H_S in both legs, exactly reversed          (residual isotropic part, reversible)
  heis_nonrev  forward H_dd + level*H_S, backward realised -H_dd + level*H_S (isotropic part not reversed)
  onsite_nonrev  h_i Z_i, h_i ~ N(0, level*b_loc), not reversed         (residual light shift / Doppler / field)
  delete_j     spin j decoupled for the whole sequence, each j not in {a} U bs (missing / decayed atom, upper bound)
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time

import numpy as np

import ed_echo as EE

HERE = os.path.dirname(os.path.abspath(__file__))

LEVELS = dict(iid_shared=[0.01, 0.03, 0.1], iid_indep=[0.01, 0.03, 0.1], pos_shared=[0.003, 0.01, 0.03],
              pos_indep=[0.003, 0.01, 0.03], scale=[0.01, 0.03, 0.1], heis_rev=[0.01, 0.03, 0.1],
              heis_nonrev=[0.01, 0.03, 0.1], onsite_nonrev=[0.01, 0.03, 0.1], delete_j=[0])
DETERMINISTIC = {"scale", "heis_rev", "heis_nonrev"}


def save(path, st):
    tmp = path + ".tmp"
    json.dump(st, open(tmp, "w"))
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, required=True)
    ap.add_argument("--N", type=int, required=True)
    ap.add_argument("--reps", type=int, default=4)
    ap.add_argument("--times", type=float, nargs="*", default=[40, 80, 120])
    ap.add_argument("--channels", nargs="*", default=list(LEVELS))
    ap.add_argument("--levels", type=float, nargs="*", default=None, help="override levels for all given channels")
    ap.add_argument("--R-channels", nargs="*", default=["scale", "heis_nonrev"])
    ap.add_argument("--budget-cpu-s", type=float, default=1500.0)
    a = ap.parse_args()

    path = os.path.join(HERE, f"sens_{a.pdb}_p{a.probe}_N{a.N}.json")
    st = json.load(open(path)) if os.path.exists(path) else {}
    st.setdefault("units", {})
    st.setdefault("cpu_s", 0.0)
    c0 = time.process_time()
    cpu_prev = st["cpu_s"]
    dm, bs, xyz, b0 = EE.load(a.pdb, a.probe, a.N)
    N = a.N
    ts = [t * 1e-6 for t in a.times]
    D = np.linalg.norm(xyz[:, None] - xyz[None], axis=2)
    iu = np.triu_indices(N, 1)
    rmin = float(D[iu].min())
    bloc = float(np.median(np.sqrt((dm ** 2).sum(1))))
    sec = EE.Sectors(N)
    secA = None
    st.update(pdb=a.pdb, probe=a.probe, N=N, bs=bs, times_us=a.times, rmin_A=rmin, bloc_rad_s=bloc)

    if "baseline" not in st:
        m0 = EE.eig_model(sec, *EE.pair_params(dm))
        F0, _ = EE.echo(sec, m0, 0, bs, ts)
        Hts = EE.two_point_H(sec, m0, 0, ts)
        st["baseline"] = dict(F={str(b): F0[b] for b in bs}, H=Hts)
        st["cpu_s"] = cpu_prev + time.process_time() - c0
        save(path, st)
        print("baseline", {b: [round(x, 4) for x in F0[b]] for b in bs}, flush=True)

    def budget_ok():
        return (time.process_time() - c0) < a.budget_cpu_s

    for ch in a.channels:
        levels = a.levels if a.levels is not None else LEVELS[ch]
        for lv in levels:
            if ch == "delete_j":
                reps = [j for j in range(N) if j != 0 and j not in bs]
            elif ch in DETERMINISTIC:
                reps = [0]
            else:
                reps = list(range(a.reps))
            for rep in reps:
                key = f"{ch}|{lv}|{rep}"
                if key in st["units"]:
                    continue
                if not budget_ok():
                    print(json.dumps(dict(stopped="budget", done=len(st["units"]))), flush=True)
                    return
                tu = time.process_time()
                rng = np.random.default_rng(1000003 * N + 7919 * a.probe + 101 * rep + int(round(lv * 1e5)) +
                                            sum(ord(c) * (i + 1) for i, c in enumerate(ch)) % 997)
                want_R = ch in a.R_channels
                mb = None
                if ch == "iid_shared":
                    e = rng.standard_normal((N, N)); e = np.triu(e, 1); e = e + e.T
                    mf = EE.eig_model(sec, *EE.pair_params(dm * (1 + lv * e)))
                elif ch == "iid_indep":
                    e1 = rng.standard_normal((N, N)); e1 = np.triu(e1, 1); e1 = e1 + e1.T
                    e2 = rng.standard_normal((N, N)); e2 = np.triu(e2, 1); e2 = e2 + e2.T
                    mf = EE.eig_model(sec, *EE.pair_params(dm * (1 + lv * e1)))
                    mb = EE.eig_model(sec, *EE.pair_params(dm * (1 + lv * e2)))
                elif ch == "pos_shared":
                    X = xyz + lv * rmin * rng.standard_normal(xyz.shape)
                    mf = EE.eig_model(sec, *EE.pair_params(EE.couplings(X, b0)))
                elif ch == "pos_indep":
                    X1 = xyz + lv * rmin * rng.standard_normal(xyz.shape)
                    X2 = xyz + lv * rmin * rng.standard_normal(xyz.shape)
                    mf = EE.eig_model(sec, *EE.pair_params(EE.couplings(X1, b0)))
                    mb = EE.eig_model(sec, *EE.pair_params(EE.couplings(X2, b0)))
                elif ch == "scale":
                    mf = EE.eig_model(sec, *EE.pair_params(dm))
                    mb = EE.eig_model(sec, *EE.pair_params(dm * (1 + lv)))
                elif ch == "heis_rev":
                    mf = EE.eig_model(sec, *EE.pair_params(dm, lam=lv))
                elif ch == "heis_nonrev":
                    mf = EE.eig_model(sec, *EE.pair_params(dm, lam=lv))
                    mb = EE.eig_model(sec, *EE.pair_params(dm, lam=-lv))
                elif ch == "onsite_nonrev":
                    if secA is None:
                        secA = EE.Sectors(N, use_flip=False)
                    h = lv * bloc * rng.standard_normal(N)
                    Jxy, Jz = EE.pair_params(dm)
                    mf = EE.eig_model(secA, Jxy, Jz, h)
                    mb = EE.eig_model(secA, Jxy, Jz, -h)
                elif ch == "delete_j":
                    d2 = dm.copy(); d2[rep, :] = 0.0; d2[:, rep] = 0.0
                    mf = EE.eig_model(sec, *EE.pair_params(d2))
                else:
                    raise ValueError(ch)
                use = secA if ch == "onsite_nonrev" else sec
                S, R = EE.echo(use, mf, 0, bs, ts, model_b=mb, want_R=want_R and mb is not None)
                st["units"][key] = dict(S={str(b): S[b] for b in bs},
                                        R=({str(b): R[b] for b in bs} if R is not None else None),
                                        cpu_s=time.process_time() - tu)
                st["cpu_s"] = cpu_prev + time.process_time() - c0
                save(path, st)
                F0 = st["baseline"]["F"]
                dmax = max(abs(S[b][i] - F0[str(b)][i]) for b in bs for i in range(len(ts)))
                print(json.dumps(dict(key=key, maxabs_dF=round(dmax, 5), cpu=round(time.process_time() - tu, 1))),
                      flush=True)
    print(json.dumps(dict(complete=True, units=len(st["units"]), cpu_total=round(st["cpu_s"], 1))), flush=True)


if __name__ == "__main__":
    main()
