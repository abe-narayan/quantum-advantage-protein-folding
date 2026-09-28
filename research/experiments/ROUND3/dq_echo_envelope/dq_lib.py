"""ROUND3 lane dq_echo_envelope: shared helpers.

R1-DQ question: does a phase-reversible double-quantum (DQ) echo carry classically-hard structural Fisher information
INSIDE its own physical reversal envelope, with a joint gain >= 2 over the classically usable data?

Conventions (all DERIVED, see README):
  * secular dipolar H_sec = sum_{i<j} d_ij (2 IzIz - IxIx - IyIy) = sum d_ij/4 (2ZZ - XX - YY)   (qapf.nmr.spins)
  * PHYSICAL DQ H_DQ = -sum d_ij (IxIx - IyIy) = -sum d_ij/4 (XX - YY)  -- Eq. (2) of Dominguez et al. PRA 104,
    012402 (2021) and Eq. (3) of Alvarez & Suter PRA 84, 012320 (2011) (8-pulse Baum-Pines/Warren sequence), with the
    SAME d_ij as the secular Hamiltonian.  The sign of a real-symmetric H does not change S or F1, so we simulate
    +sum d/4 (XX - YY), i.e. amp_lib.dq_pair_terms / dq_gate_seq with s = 1.
    The R1_amplify lens used the Frobenius-norm-matched s = sqrt(3): its DQ time t_m equals physical time sqrt(3) t_m.
  * local second moment of Z_a:  secular (1/2) sum_j d_aj^2, physical DQ (1/2) sum_j d_aj^2  (equal).
    global: secular FID (I_y) M2 = (9/4)<sum_j d^2>, DQ acting on I_z: M2 = <sum_j d^2>  (DQ 1.5x slower by this clock).
Single-threaded use only (set OMP/MKL/OPENBLAS_NUM_THREADS=1 before import).
"""
from __future__ import annotations

import json
import math
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
AMP = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_amplify")
PHYS = os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_physics_feasibility")
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, AMP)
import amp_lib as L  # noqa: E402  (read-only reuse of the validated R1_amplify engines)
from qapf.nmr import spins as SP  # noqa: E402

OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

SIGMA = 0.01
H_FD = 0.05
DT = 2e-6


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(L.jsonable(obj), f)
    os.replace(tmp, path)


def atomic_npz(path, **arrs):
    tmp = path + ".tmp.npz"
    np.savez(tmp, **arrs)
    os.replace(tmp, path)


def geometry(pdb, probe):
    return L.job_geometry(pdb, probe, 10, 0, hn_only=False)


def m2_global(D):
    return 9.0 / 4.0 * float(np.mean(np.sum(D ** 2, axis=1)))


def t2_info(pdb, g):
    """T2 = 1/sqrt(M2) (Van Vleck, Sanchez et al. 2022 Eq. 2) for the cluster, the whole static 1H network and the
    methyl/NH3 rotor-averaged network (R1_physics_feasibility/scales.py functions, imported read-only)."""
    sys.path.insert(0, PHYS)
    import scales as S  # noqa: E402
    pdbf = os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb")
    names, xyz, resid = SP.read_h_coords(pdbf)
    Dc = SP.couplings(g["X0"], g["b0"])
    Dn = SP.couplings(xyz, g["b0"])
    atoms = S.read_all_atoms(pdbf)
    hk = [k for k, a in enumerate(atoms) if a[3] == "H"]
    hidx_of_atom = {k: i for i, k in enumerate(hk)}
    groups, _ = S.rotor_groups(atoms, hidx_of_atom)
    Dm = S.averaged_couplings(xyz, g["b0"], groups)
    p = int(g["idx"][0])
    rotor_in_cluster = [names[i] for i in g["idx"] if any(i in gg for gg in groups)]
    return dict(T2_cluster_us=1e6 / math.sqrt(m2_global(Dc)),
                T2_network_us=1e6 / math.sqrt(m2_global(Dn)),
                T2_rotoravg_us=1e6 / math.sqrt(m2_global(Dm)),
                Tz_loc_cluster_us=1e6 / math.sqrt(0.5 * float(np.sum(Dc[0] ** 2))),
                Tz_loc_network_us=1e6 / math.sqrt(0.5 * float(np.sum(Dn[p] ** 2))),
                DQ_global_over_sec_T2=1.5,
                rotor_protons_in_cluster=rotor_in_cluster,
                n_network=len(names))


def exact_obs(ham, X, b0, steps, rec, bs, s_dq=1.0):
    dm = SP.couplings(X, b0)
    if ham == "sec":
        o = L.exact_sector(dm, DT, steps, 0, bs, rec, want_F2=False, want_P=False)
        return dict(times=o["times"], S=o["S"], F1=o["F1"])
    o = L.exact_parity(len(X), L.dq_pair_terms(dm, s=s_dq), DT, steps, 0, bs, rec, want_P=False, want_F2=False)
    return dict(times=o["times"], S=o["S"], F1=o["F1"], MQC_tot=o["MQC_tot"])


def mean_weight(op):
    w = SP._popcount(op.x | op.z).astype(float)
    c2 = op.c ** 2
    n2 = float(c2.sum())
    return float((c2 * w).sum() / max(n2, 1e-300)), n2, np.bincount(w.astype(int), weights=c2, minlength=op.N + 1)


def pauli_adversary(N, seq, steps, rec, bs, exact, eps, ckpt, sigma=SIGMA, budget_s=840.0, stop_after_fail=1,
                    max_strings=None, extra_stop=None):
    """Checkpointed Heisenberg sparse-Pauli propagation of Z_0 (probe) through `seq` (list of commuting pair groups,
    amp_lib convention), |c| <= eps truncation once per group.  At every recorded step: dense WHT reconstruction ->
    S, F1 (plain and norm-corrected), bias vs `exact` (dict with S, F1 arrays (nt, nb) on the same record grid), string
    count, kept norm, mean Pauli weight.  Checkpoint (JSON records + NPZ operator) after every recorded step; resumes
    from the checkpoint if present.  Stops `stop_after_fail` records after the first F1 failure (max bias > sigma for
    both estimators), at `steps`, at the CPU budget, or when extra_stop(record) is True."""
    jpath, npath = ckpt + ".json", ckpt + ".npz"
    recs, k0 = [], 0
    op = SP.PauliOp.single_z(N, 0)
    cpu_prev = 0.0
    if os.path.exists(jpath) and os.path.exists(npath):
        st = json.load(open(jpath))
        recs = st["records"]; k0 = st["next_step"]; cpu_prev = st.get("cpu_s", 0.0)
        z = np.load(npath)
        op = SP.PauliOp(N, z["x"], z["z"], z["c"])
        if st.get("done"):
            return st
    c0 = time.process_time()
    fail_seen = sum(1 for r in recs if r["fail_F1"])
    done_reason = None
    k = k0
    while True:
        if k % rec == 0 and (not recs or recs[-1]["step"] != k):
            ti = k // rec
            M = L.pauli_to_matrix(op)
            S_, F1_, _, _, _, _ = L.matrix_observables(M, N, 0, bs, want_F2=False, want_P=False)
            del M
            mw, n2, whist = mean_weight(op)
            F1n = F1_ / n2
            bS = float(np.max(np.abs(S_ - exact["S"][ti])))
            bF = float(np.max(np.abs(F1_ - exact["F1"][ti])))
            bFn = float(np.max(np.abs(F1n - exact["F1"][ti])))
            r = dict(step=k, t_us=k * DT * 1e6, n_strings=int(len(op.c)), kept_norm2=n2, mean_weight=mw,
                     weight_hist=whist.tolist(), S=S_.tolist(), F1=F1_.tolist(), bias_S=bS, bias_F1_plain=bF,
                     bias_F1_normcorr=bFn, fail_F1=bool(min(bF, bFn) > sigma), fail_S=bool(bS > sigma))
            recs.append(r)
            fail_seen += int(r["fail_F1"])
            cpu = cpu_prev + time.process_time() - c0
            if fail_seen > stop_after_fail:
                done_reason = "failed"
            elif k >= steps:
                done_reason = "end"
            elif cpu > budget_s:
                done_reason = "budget"
            elif extra_stop is not None and extra_stop(r):
                done_reason = "extra_stop"
            st = dict(eps=eps, next_step=k, records=recs, cpu_s=cpu, done=done_reason is not None,
                      done_reason=done_reason)
            atomic_npz(npath, x=op.x, z=op.z, c=op.c)
            atomic_json(st, jpath)
            print(json.dumps(dict(t_us=round(r["t_us"], 1), strings=r["n_strings"], w=round(mw, 2),
                                  bF=round(min(bF, bFn), 4), bS=round(bS, 4), cpu=round(cpu))), flush=True)
            if done_reason:
                return st
        for grp in reversed(seq):
            for (gx, gz, th) in grp:
                op = SP.conj_rotation(op, gx, gz, th, None, 0.0, compact=False)
            op = op.compact(eps)
            if max_strings and len(op.c) > max_strings:
                o = np.argsort(-np.abs(op.c))[:max_strings]
                op.x, op.z, op.c = op.x[o], op.z[o], op.c[o]
        k += 1
