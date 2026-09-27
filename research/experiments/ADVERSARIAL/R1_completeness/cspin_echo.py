"""R1_completeness: classical-spin (Elsayed-Fine sphere, |S|=sqrt(3)/2) and DTWA (discrete, components +-1/2) adversaries for
the ECHO F_ab(t) = Tr[Z_a(t) Z_b Z_a(t) Z_b]/2^N, which the C1 panel never evaluated (its `cspin` adversary returns S only).
Leading-order Weyl/TWA correspondence: F_cl(t) = < A(Phi_t x) A(Phi_t R_b x) >_x / <A^2>, A = S_a^z, R_b = pi rotation of spin b
about z (conjugation by Z_b), x drawn from the infinite-temperature classical/discrete-Wigner distribution.
Also S_cl(t) = <A(Phi_t x) S_b^z(x)>/<A^2> (transfer) for validation against SP.classical_spin_correlators.
Continuous-time RK4 (h = dt/substeps); reference = sector-exact Trotter F/S stored in RAW/nmr_sparse (C2) at N = 10, 12, 14.
Question: does the classical-spin error DECREASE with N (the Elsayed-Fine large-coordination mechanism)? If yes it is a
polynomial candidate for the converged, large-cone echo (R1-SIM); if not it is one more failed family.
Usage: python cspin_echo.py <pdb> <probe> <N> <M_samples> [mode=sphere|dtwa]
"""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "R1_fi_method"))
from fi_common import setup, SP, RAW  # noqa: E402


def run(pdb, probe, N, M, mode="sphere", batch=10000, substeps=2, seed=7):
    cfg = setup(pdb, probe, N, 0)
    _fn = os.path.join(RAW, "nmr_sparse", f"{pdb}_p{probe}_N{N}_o0_g0.json"); ref = json.load(open(_fn if os.path.exists(_fn) else _fn + ".partial"))
    assert ref["bs"] == cfg["bs"], (ref["bs"], cfg["bs"])
    dt, steps, rec = ref["dt"], ref["steps"], ref["rec"]
    J = SP.couplings(cfg["X0"], cfg["b0"]); J = np.asarray(J, float); J = J - np.diag(np.diag(J))
    bs = cfg["bs"]; nb = len(bs); nrec = steps // rec + 1
    h = dt / substeps
    rng = np.random.default_rng(seed)

    Jx = -J; Jz = 2 * J

    def f(x, y, z):
        hx = x @ Jx; hy = y @ Jx; hz = z @ Jz
        return hy * z - hz * y, hz * x - hx * z, hx * y - hy * x   # (h x S)

    def rk4(x, y, z):
        a1, b1, c1 = f(x, y, z)
        a2, b2, c2 = f(x + 0.5 * h * a1, y + 0.5 * h * b1, z + 0.5 * h * c1)
        a3, b3, c3 = f(x + 0.5 * h * a2, y + 0.5 * h * b2, z + 0.5 * h * c2)
        a4, b4, c4 = f(x + h * a3, y + h * b3, z + h * c3)
        return (x + h / 6 * (a1 + 2 * a2 + 2 * a3 + a4), y + h / 6 * (b1 + 2 * b2 + 2 * b3 + b4),
                z + h / 6 * (c1 + 2 * c2 + 2 * c3 + c4))

    accF = np.zeros((nb, nrec)); accF2 = np.zeros((nb, nrec)); accS = np.zeros((nb, nrec)); n = 0
    t0 = time.time()
    while n < M:
        B = min(batch, M - n)
        if mode == "sphere":
            v = rng.standard_normal((B, N, 3)); v /= np.linalg.norm(v, axis=-1, keepdims=True); S0 = v * (np.sqrt(3) / 2)
        else:
            S0 = rng.choice([-0.5, 0.5], size=(B, N, 3))
        # stack: [unkicked, kicked_b1, ..., kicked_bnb]
        stack = [S0]
        for b in bs:
            Sk = S0.copy(); Sk[:, b, 0] *= -1; Sk[:, b, 1] *= -1; stack.append(Sk)
        S = np.concatenate(stack, 0)
        x, y, z = [np.ascontiguousarray(S[:, :, c]) for c in range(3)]
        sz0 = S0[:, :, 2].copy()
        for k in range(steps + 1):
            if k % rec == 0:
                r = k // rec
                a0 = z[:B, 0]
                for j, b in enumerate(bs):
                    ak = z[(j + 1) * B:(j + 2) * B, 0]
                    prod = a0 * ak / 0.25
                    accF[j, r] += prod.sum(); accF2[j, r] += (prod ** 2).sum()
                    accS[j, r] += (a0 * sz0[:, b] / 0.25).sum()
            if k < steps:
                for _ in range(substeps):
                    x, y, z = rk4(x, y, z)
        n += B
    F = accF / n; S_ = accS / n; se = np.sqrt(np.maximum(accF2 / n - F ** 2, 0) / n)
    Fex = np.array([ref["exact"]["F"][str(b)] for b in bs]); Sex = np.array([ref["exact"]["S"][str(b)] for b in bs])
    times_us = (np.arange(nrec) * rec * dt * 1e6).tolist()
    errF = np.abs(F - Fex).max(0); errS = np.abs(S_ - Sex).max(0)

    def tfail(err, thr):
        idx = np.where(err > thr)[0]
        return None if len(idx) == 0 else float(times_us[idx[0]])
    thr = max(0.01, 0)  # sigma
    out = dict(pdb=pdb, probe=probe, N=N, mode=mode, M=int(n), substeps=substeps, bs=bs, times_us=times_us,
               F_cl=F.tolist(), F_se=se.tolist(), F_exact=Fex.tolist(), S_cl=S_.tolist(), S_exact=Sex.tolist(),
               maxerr_F_t=errF.tolist(), maxerr_S_t=errS.tolist(),
               t_fail_F_us=tfail(errF, 0.01 + 3 * se.max()), t_fail_S_us=tfail(errS, 0.01 + 3 * se.max()),
               maxerr_F_window_80_320=float(errF[4:].max()), maxerr_S_window_80_320=float(errS[4:].max()),
               max_se=float(se.max()), secs=time.time() - t0)
    return out


if __name__ == "__main__":
    pdb, probe, N, M = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    mode = sys.argv[5] if len(sys.argv) > 5 else "sphere"
    o = run(pdb, probe, N, M, mode)
    fn = os.path.join(HERE, "out", f"cspin_echo_{pdb}_p{probe}_N{N}_{mode}.json")
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    json.dump(o, open(fn, "w"), indent=1)
    print(f"{pdb} p{probe} N={N} {mode} M={o['M']} secs={o['secs']:.1f} maxSE={o['max_se']:.4f}")
    print(" t(us)   " + " ".join(f"{t:6.0f}" for t in o["times_us"]))
    print(" errF    " + " ".join(f"{e:6.3f}" for e in o["maxerr_F_t"]))
    print(" errS    " + " ".join(f"{e:6.3f}" for e in o["maxerr_S_t"]))
    print(" t_fail F", o["t_fail_F_us"], " t_fail S", o["t_fail_S_us"], " max errF [80,320]", round(o["maxerr_F_window_80_320"], 3))
