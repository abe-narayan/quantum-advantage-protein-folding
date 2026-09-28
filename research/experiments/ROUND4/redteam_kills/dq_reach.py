"""ROUND4 red team, RT-B: how far does EXACT classical simulation reach for the physical DQ echo at t <= 80 us?

Why: RT-A shows that K-109's value arm is conditional on t_cl^DQ, the converged-size sigma-level classical reach of
the site-resolved DQ echo.  If t_cl^DQ <= 50-60 us, the profiled median gain inside the literature DQ envelope
(12.5-19 T2) is >= 2; if t_cl^DQ >= 60 us it is < 2 (moderate priors, secular transfer on the classical side).

Physics note [DERIVED]: H_DQ = -sum d_ij (IxIx - IyIy) conserves only the parity prod Z_i (and energy); a single-site
Z_a has zero overlap with both, so the DQ echo has NO O(1/N) conserved-charge floor, unlike the secular echo
(F_floor ~ (1-H)/N, ROUND3 CRITIC C1).  A size-step test |F_N - F_{N-2}| is therefore a less biased convergence
indicator for DQ than for the secular echo (it is still only a step statistic; see CRITIC C10).

Method: typicality, F_ab(t) = <chi1| Z_b |chi2>, chi1 = U^dag(t) Z_a U(t) psi, chi2 = U^dag(t) Z_a U(t) Z_b psi,
S_ab(t) = <chi1| Z_b |psi>, psi random normalised on the full 2^N space; U = the SAME physical-DQ Trotter circuit
as amp_lib.exact_parity(dq_pair_terms(s=1)) (pairs (i<j) in list order, each exp(-i dt d_ij/4 (XX - YY)) exact).
Forward legs are reused across record times (fastecho lever L3); backward legs per record time.
Cluster: nearest N protons of the probe (SP.cluster), instrument sites b from the N0 = 10 cluster (fastecho
convention), static couplings (same as dq_echo_envelope, whose N = 10 exact data are the validation target).
Validation: (i) circuit: the full step unitary built from this kernel equals build_step_unitary_generic at N = 6;
(ii) estimator: N = 10 typicality mean over M vectors vs the exact parity-block F at N = 10.
Checkpoint: out/dqreach_<pdb>_p<probe>_N<N>_v<k>.npz after every record time (atomic); final values in
dq_reach.json.  Usage: python dq_reach.py --pdb 1UBQ --probe 19 --N 16 --M 2 --tmax-steps 40
"""
from __future__ import annotations

import os

for _v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import argparse
import json
import math
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "src"))
sys.path.insert(0, os.path.join(ROOT, "research", "experiments", "ADVERSARIAL", "R1_amplify"))
import amp_lib as L  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

DT = 2e-6
OUTD = os.path.join(HERE, "out")
SUMMARY = os.path.join(HERE, "dq_reach.json")


def _replace(tmp, path, tries=20):
    for k in range(tries):
        try:
            os.replace(tmp, path)
            return
        except PermissionError:
            time.sleep(0.25 * (k + 1))
    os.replace(tmp, path)


def atomic_json(obj, path):
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(obj, f, indent=1)
    _replace(tmp, path)


def instance(pdb, probe, N):
    names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", f"{pdb}_H.pdb"))
    b0 = L.random_b0(1000)
    idx10 = SP.cluster(xyz, probe, 10)
    X10 = xyz[idx10]
    dist = np.linalg.norm(X10 - X10[0], axis=1)
    far = [int(k) for k in np.argsort(-dist)[:3]]
    bs = sorted(set(far + [int(np.argsort(dist)[1])]))
    idx = SP.cluster(xyz, probe, N)
    assert list(idx[:10]) == list(idx10), "cluster prefix mismatch"
    return SP.couplings(xyz[idx], b0), bs, [names[i] for i in idx]


def gate_list(D):
    N = len(D)
    return [(i, j, DT * D[i, j] / 2.0) for i in range(N) for j in range(i + 1, N)]   # theta = dt (cxx - cyy)


def apply_step(v, N, gates, inverse=False):
    """In-place DQ Trotter step on a flat complex vector (bit q of the index = spin q)."""
    seq = reversed(gates) if inverse else gates
    for (i, j, th) in seq:
        c, s = math.cos(th), math.sin(th)
        if inverse:
            s = -s
        w = v.reshape(1 << (N - 1 - j), 2, 1 << (j - i - 1), 2, 1 << i)
        a = w[:, 0, :, 0, :].copy()
        b = w[:, 1, :, 1, :]
        w[:, 0, :, 0, :] = c * a - 1j * s * b
        w[:, 1, :, 1, :] = -1j * s * a + c * b
    return v


def zvec(N, q):
    return (1.0 - 2.0 * ((np.arange(1 << N) >> q) & 1)).astype(np.float64)


def validate_circuit(N=6, seed=5):
    rng = np.random.default_rng(seed)
    X = rng.normal(size=(N, 3)) * 2.0
    D = SP.couplings(X, (0, 0, 1))
    gates = gate_list(D)
    U = np.zeros((1 << N, 1 << N), complex)
    for k in range(1 << N):
        e = np.zeros(1 << N, complex); e[k] = 1.0
        U[:, k] = apply_step(e, N, gates)
    pc = L.popcount(np.arange(1 << N))
    err = 0.0
    for par in (0, 1):
        idx = np.nonzero(pc % 2 == par)[0]
        Ug = L.build_step_unitary_generic(N, L.dq_pair_terms(D, s=1.0), DT, idx)
        err = max(err, float(np.abs(U[np.ix_(idx, idx)] - Ug).max()))
    Ui = np.zeros_like(U)
    for k in range(1 << N):
        e = np.zeros(1 << N, complex); e[k] = 1.0
        Ui[:, k] = apply_step(e, N, gates, inverse=True)
    inv = float(np.abs(Ui @ U - np.eye(1 << N)).max())
    return dict(max_abs_vs_generic=err, inverse_check=inv)


def run_vector(D, bs, rec, nrec, seed, ckpt):
    N = len(D)
    gates = gate_list(D)
    za = zvec(N, 0)
    zb = [zvec(N, b) for b in bs]
    nb = len(bs)
    src = None
    for cand in (ckpt + ".tmp.npz", ckpt):          # a completed tmp (replace failed) is newer than the ckpt
        if os.path.exists(cand):
            try:
                with np.load(cand) as z:
                    kd = int(z["k_done"])
                if src is None or kd > src[1]:
                    src = (cand, kd)
            except Exception:
                pass
    if src is not None:
        with np.load(src[0]) as z:                   # context manager: Windows keeps an open NpzFile locked
            k0 = int(z["k_done"]); F = z["F"].copy(); S = z["S"].copy(); fpsi = z["fpsi"].copy()
            fb = [z[f"fb{q}"].copy() for q in range(nb)]; psi = z["psi"].copy()
        if src[0] != ckpt:
            _replace(src[0], ckpt)
    else:
        rng = np.random.default_rng(seed)
        psi = rng.standard_normal(1 << N) + 1j * rng.standard_normal(1 << N)
        psi /= np.linalg.norm(psi)
        fpsi = psi.copy(); fb = [zb[q] * psi for q in range(nb)]
        F = np.full((nrec + 1, nb), np.nan); S = np.full((nrec + 1, nb), np.nan)
        F[0] = 1.0; S[0] = [float(np.real(np.vdot(psi, za * zb[q] * psi))) for q in range(nb)]
        k0 = 0
    for k in range(k0 + 1, nrec + 1):
        for _ in range(rec):
            apply_step(fpsi, N, gates)
            for q in range(nb):
                apply_step(fb[q], N, gates)
        chi1 = za * fpsi
        for _ in range(k * rec):
            apply_step(chi1, N, gates, inverse=True)
        for q in range(nb):
            chi2 = za * fb[q]
            for _ in range(k * rec):
                apply_step(chi2, N, gates, inverse=True)
            F[k, q] = float(np.real(np.vdot(chi1, zb[q] * chi2)))
            S[k, q] = float(np.real(np.vdot(chi1, zb[q] * psi)))
        tmp = ckpt + ".tmp.npz"
        np.savez(tmp, k_done=k, F=F, S=S, fpsi=fpsi, psi=psi, **{f"fb{q}": fb[q] for q in range(nb)})
        _replace(tmp, ckpt)
    return F, S


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdb", default="1UBQ")
    ap.add_argument("--probe", type=int, default=19)
    ap.add_argument("--N", type=int, default=12)
    ap.add_argument("--M", type=int, default=1)
    ap.add_argument("--rec", type=int, default=5)
    ap.add_argument("--tmax-steps", type=int, default=40)
    ap.add_argument("--validate", action="store_true")
    a = ap.parse_args()
    summ = json.load(open(SUMMARY)) if os.path.exists(SUMMARY) else {}
    if a.validate:
        t0 = time.process_time()
        vc = validate_circuit()
        D, bs, _ = instance(a.pdb, a.probe, 10)
        ex = L.exact_parity(10, L.dq_pair_terms(D, s=1.0), DT, a.tmax_steps, 0, bs, a.rec, want_P=False)
        Fs = []
        for v in range(a.M):
            F, S = run_vector(D, bs, a.rec, a.tmax_steps // a.rec, 777 + v, os.path.join(OUTD, f"dqreach_val_v{v}.npz"))
            Fs.append(F)
        Fm = np.mean(Fs, axis=0)
        se = np.std(Fs, axis=0, ddof=1) / math.sqrt(a.M) if a.M > 1 else None
        summ["validation"] = dict(circuit=vc, N10_typicality_M=a.M,
                                  max_abs_mean_vs_exact=float(np.abs(Fm - ex["F1"]).max()),
                                  max_se=float(se.max()) if se is not None else None,
                                  max_z=float(np.nanmax(np.abs(Fm - ex["F1"])[1:] / np.maximum(se[1:], 1e-12))) if se is not None else None,
                                  cpu_s=time.process_time() - t0)
        atomic_json(summ, SUMMARY)
        print(json.dumps(summ["validation"]), flush=True)
        return
    t0 = time.process_time()
    D, bs, names = instance(a.pdb, a.probe, a.N)
    nrec = a.tmax_steps // a.rec
    key = f"{a.pdb}_p{a.probe}_N{a.N}"
    rec = summ.setdefault(key, dict(pdb=a.pdb, probe=a.probe, N=a.N, bs=bs, names_bs=[names[b] for b in bs],
                                    times_us=[k * a.rec * DT * 1e6 for k in range(nrec + 1)], vectors={}))
    for v in range(a.M):
        if str(v) in rec["vectors"]:
            continue
        tv = time.process_time()
        F, S = run_vector(D, bs, a.rec, nrec, 1000 * a.N + v, os.path.join(OUTD, f"dqreach_{key}_v{v}.npz"))
        rec["vectors"][str(v)] = dict(F=F.tolist(), S=S.tolist(), cpu_s=time.process_time() - tv)
        summ[key] = rec
        atomic_json(summ, SUMMARY)
        print(json.dumps(dict(key=key, v=v, cpu=round(time.process_time() - tv, 1))), flush=True)
    Fs = np.array([rec["vectors"][k]["F"] for k in rec["vectors"]])
    rec["F_mean"] = Fs.mean(axis=0).tolist()
    rec["F_se"] = (Fs.std(axis=0, ddof=1) / math.sqrt(len(Fs))).tolist() if len(Fs) > 1 else None
    rec["typicality_err_est"] = 2.0 ** (-a.N / 2) / math.sqrt(len(Fs))
    summ[key] = rec
    atomic_json(summ, SUMMARY)


if __name__ == "__main__":
    main()
