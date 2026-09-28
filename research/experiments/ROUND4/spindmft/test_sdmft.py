"""Unit validation of sdmft.py (small, < 2 CPU-min).
T1  no bath (C = whole closed N = 10 world): embedded typicality estimates of G_ab and F_ab vs the deterministic
    sector-exact reference (same Trotter circuit) -> must agree within typicality noise.
T2  G_ja (estimator used for H) vs G_aj (direct) symmetry, with a bath.
T3  n_c = 1 embedded quantum spin vs the classical-rotation single-site solver in the same field statistics.
"""
import json
import os
import sys
import time

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sdmft as S  # noqa: E402
from qapf.nmr import spins as SP  # noqa: E402

out = {}
t0 = time.time()
# ---- T1
t_cpu0 = time.process_time()
w = S.load_world("1UBQ", 19, 10)
D = w["D"]; bs = w["bs"]
n_steps = 30
tt, Sx, Fx = SP.sector_exact_correlators(D, S.DT, n_steps, 0, bs, record_every=10, otoc=True)
g1 = np.ones((10, 2 * n_steps + 1))
st = S.run_embedded(D, list(range(10)), bs, g1, g1, n_steps, [10, 20, 30], M=256, batch=64, seed=1, log=None, rec=10)
sm = S.summarize(st)
Gab = np.array(sm["Gab_direct"])[1:]
Gja = np.array(sm["G"])[1:][:, bs]
F = np.array(sm["F"]); Fse = np.array(sm["F_se"])
ex_S = np.array([Sx[b][1:] for b in bs]).T
ex_F = np.array([Fx[b][1:] for b in bs]).T
out["T1"] = dict(times_us=[20, 40, 60], exact_S=ex_S.tolist(), emb_Gab=Gab.tolist(), emb_Gja=Gja.tolist(),
                 exact_F=ex_F.tolist(), emb_F=F.tolist(), emb_F_se=Fse.tolist(),
                 max_abs_dF=float(np.abs(F - ex_F).max()), max_z_dF=float((np.abs(F - ex_F) / Fse).max()),
                 max_abs_dS=float(np.abs(Gab - ex_S).max()), max_abs_dS_ja=float(np.abs(Gja - ex_S).max()))
print("T1", json.dumps({k: v for k, v in out["T1"].items() if k.startswith("max")}), round(time.time() - t0, 1))

# ---- T2 + T3: protein world, crude bath g (2 sr iterations, small M)
w = S.load_world("1UBQ", 19, "protein")
D = w["D"]
T = 60
res = S.sr_spindmft(D, T, M=128, n_iter=2, seed=5, log=None)
gz, gp = res["gz"], res["gp"]
st = S.run_embedded(D, list(range(6)), [1], gz, gp, 30, [15], M=512, batch=128, seed=2, log=None, rec=5)
sm = S.summarize(st)
G = np.array(sm["G"]); Gab = np.array(sm["Gab_direct"])
out["T2"] = dict(G_1a=G[:, 1].tolist(), G_a1_direct=Gab[:, 0].tolist(),
                 max_abs_diff=float(np.abs(G[:, 1] - Gab[:, 0]).max()), se=float(np.array(sm["G_se"])[:, 1].max()))
print("T2", out["T2"]["max_abs_diff"], out["T2"]["se"], round(time.time() - t0, 1))
# T3: n_c = 1 quantum vs classical rotation with the SAME field covariance (bath = all j != 0)
st = S.run_embedded(D, [0], [], gz, gp, 30, [], M=4096, batch=1024, seed=3, log=None, rec=1)
sm = S.summarize(st)
q_gaa = np.array(sm["Gaa"]); q_se = np.array(sm["G_se"])[:, 0]
Lz, Lp = S.cluster_field_factors(D, [0], gz, gp, T)
rng = np.random.default_rng(9)
Mc = 4096
Vz = (Lz @ rng.standard_normal((T, Mc))); Vx = (Lp @ rng.standard_normal((T, Mc))); Vy = (Lp @ rng.standard_normal((T, Mc)))
rzz, rxx = S.single_spin_track(Vx, Vy, Vz, 1e-6)
c_gaa = rzz.mean(-1)[::2]
out["T3"] = dict(quantum=q_gaa.tolist(), classical=c_gaa.tolist(), max_abs_diff=float(np.abs(q_gaa - c_gaa).max()),
                 se=float(q_se.max()))
print("T3", out["T3"]["max_abs_diff"], out["T3"]["se"], round(time.time() - t0, 1))
out["wall_s"] = time.time() - t0
out["cpu_s"] = time.process_time() - t_cpu0
S.atomic_json(out, os.path.join(HERE, "test_sdmft.json"))
