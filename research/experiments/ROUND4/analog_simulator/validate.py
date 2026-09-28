"""Validate ed_echo against the ROUND3 continuous-time (Chebyshev, exact exp(-iHt)) N = 12 reference runs.
Checks: (1) F_ab(t) vs runs/1UBQ_p{19,245}_N12_reference_cheb_*.json; (2) the mismatch code path with H_b = H_f gives
the same F and R = 1; (3) flip-symmetric and all-sector evaluations agree.  < 1 CPU-min."""
import json
import os
import time

import numpy as np

import ed_echo as EE

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(EE.ROOT, "research", "experiments", "ROUND3", "r1sim_exact_reach", "runs")


def main():
    out = {}
    t0 = time.process_time()
    for probe in (19, 245):
        ref = json.load(open(os.path.join(RUNS, f"1UBQ_p{probe}_N12_reference_cheb_complex128_t20-40-60-80-100-120-140-160.json")))
        tus = ref["times_us"][1:5]              # 40, 80, 120, 160 us
        dm, bs, xyz, b0 = EE.load("1UBQ", probe, 12)
        sec = EE.Sectors(12)
        Jxy, Jz = EE.pair_params(dm)
        mod = EE.eig_model(sec, Jxy, Jz)
        ts = [t * 1e-6 for t in tus]
        F, _ = EE.echo(sec, mod, 0, bs, ts)
        F2, R2 = EE.echo(sec, mod, 0, bs, ts, model_b=mod, want_R=True)
        secA = EE.Sectors(12, use_flip=False)
        modA = EE.eig_model(secA, Jxy, Jz)
        F3, _ = EE.echo(secA, modA, 0, bs, ts)
        d_ref = max(abs(F[b][i] - ref["F"][str(b)][i + 1]) for b in bs for i in range(len(ts)))
        d_path = max(abs(F[b][i] - F2[b][i]) for b in bs for i in range(len(ts)))
        d_R = max(abs(R2[b][i] - 1.0) for b in bs for i in range(len(ts)))
        d_flip = max(abs(F[b][i] - F3[b][i]) for b in bs for i in range(len(ts)))
        out[f"p{probe}"] = dict(times_us=tus, F_ed={str(b): F[b] for b in bs},
                                F_ref_cheb={str(b): ref["F"][str(b)][1:5] for b in bs},
                                maxabs_vs_ref=d_ref, maxabs_mismatch_path=d_path, maxabs_R_minus_1=d_R,
                                maxabs_flip_vs_all=d_flip,
                                ref_typicality_err_est=ref.get("err_typ_est"))
        print(probe, "vs ref %.2e  path %.2e  R-1 %.2e  flip %.2e" % (d_ref, d_path, d_R, d_flip), flush=True)
    out["cpu_s"] = time.process_time() - t0
    out["note"] = ("Reference runs are 'reference' mode typicality with one random vector (error ~ 2^-N/2 ~ 0.016 at "
                   "N = 12 per element, but the same vector across times), so agreement is expected at the "
                   "typicality-noise level, not to rounding; the internal checks (path, R, flip) must hold to rounding.")
    json.dump(out, open(os.path.join(HERE, "validate.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
