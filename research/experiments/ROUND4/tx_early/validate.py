"""Validation of tx_echo.py (writes validate.json).
V1  N = 12, p19 and p245, complex128, same seed: tx_echo (echo and honly modes) vs ROUND3 verify_classical
    decomp_echo.run (validated there to 1e-14 against dense traces).  Same random vectors by construction.
V1b kill/resume: the same N = 12 echo run interrupted many times (tiny wall budget) vs one uninterrupted run.
V1c ClipSectorKernel vs fastecho.SectorKernel on one Trotter step (N = 12, all folded sectors).
"""
import json
import os
import sys
import time

import numpy as np

import tx_echo as TX
from kernels import FE, SP, LANE3

sys.path.insert(0, os.path.join(LANE3, "verify_classical"))
import decomp_echo as DE  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
steps = [20, 40, 60]
for probe in (19, 245):
    ref = DE.run("1UBQ", probe, 12, "probe", None, "echo", steps, 1, np.complex128, 777, None, log=None)
    refh = DE.run("1UBQ", probe, 12, "probe", None, "honly", steps, 1, np.complex128, 777, None, log=None)
    mine = TX.run("1UBQ", probe, 12, "echo", steps, 1, np.complex128, 777, f"VAL_p{probe}_N12_echo", log=lambda s: None)
    mineh = TX.run("1UBQ", probe, 12, "honly", steps, 1, np.complex128, 777, f"VAL_p{probe}_N12_honly",
                   log=lambda s: None)
    d = {}
    for q in ("H", "floor", "G"):
        d[q] = float(np.max(np.abs(np.array(mine[q]) - np.array(ref[q]))))
        d[q + "_honly"] = float(np.max(np.abs(np.array(mineh[q]) - np.array(refh[q]))))
    for q in ("F", "X"):
        d[q] = float(max(np.max(np.abs(np.array(mine[q][b]) - np.array(ref[q][b]))) for b in ref[q]))
    d["H_echo_vs_honly_same_seed"] = float(np.max(np.abs(np.array(mine["H"]) - np.array(mineh["H"]))))
    out[f"V1_p{probe}_maxabs"] = d
    out[f"V1_p{probe}_values"] = dict(F=mine["F"], H=mine["H"], floor=mine["floor"], X=mine["X"])
    print(probe, json.dumps(d), flush=True)

# V1b: kill/resume (wall budget 0.3 s per invocation -> many resumes)
tag = "VAL2_p19_N12_echo_resume"
n_inv = 0
while True:
    r = TX.run("1UBQ", 19, 12, "echo", steps, 1, np.complex128, 777, tag, wall_s=0.3, log=lambda s: None)
    n_inv += 1
    if r["complete"] or n_inv > 500:
        break
full = TX.run("1UBQ", 19, 12, "echo", steps, 1, np.complex128, 777, "VAL_p19_N12_echo", log=lambda s: None)
out["V1b_resume"] = dict(invocations=n_inv, complete=r["complete"],
                         maxabs_F=float(max(np.max(np.abs(np.array(r["F"][b]) - np.array(full["F"][b]))) for b in r["F"])),
                         maxabs_H=float(np.max(np.abs(np.array(r["H"]) - np.array(full["H"])))))
print(json.dumps(out["V1b_resume"]), flush=True)

# V1c: kernel equivalence, one forward + one inverse step on every folded sector, complex128 and complex64
import kernels as KR
dm, bs, names, _ = FE.load_instance("1UBQ", 19, 12)
pairs = SP.pair_list(dm, 2e-6)
pc = FE.popcounts(12)
mx = {}
for dt in (np.complex128, np.complex64):
    e = 0.0
    for k in range(7):
        idx = np.nonzero(pc == k)[0]
        rng = np.random.default_rng(k)
        v = (rng.standard_normal(len(idx)) + 1j * rng.standard_normal(len(idx))).astype(dt)
        a = v.copy(); b = v.copy()
        KR.ClipSectorKernel(12, idx, pairs, dt).step(a); FE.SectorKernel(12, idx, pairs, dt).step(b)
        e = max(e, float(np.max(np.abs(a - b))))
    mx[np.dtype(dt).name] = e
out["V1c_kernel_maxabs_one_step"] = mx
print(json.dumps(mx))
json.dump(out, open(os.path.join(HERE, "validate.json"), "w"), indent=1)
