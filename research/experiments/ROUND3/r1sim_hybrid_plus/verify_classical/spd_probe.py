"""Sparse Pauli dynamics (Heisenberg Z_a(t), coefficient truncation eps) at the START of the lane's window (80 us),
N = 16, 1UBQ p19, same Trotter circuit (qapf.nmr.spins.pauli_correlators).  Reports kept norm^2, string count and
F error vs the exact reference, raw and norm-renormalised (F_kept / ||kept||^2 is NOT used; the dropped weight is
assigned F = the kept-weighted average, i.e. F_ren = sum c^2 s / sum c^2).  Checkpoint: result JSON written per eps."""
import json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import subcluster as S
SP = S.SP
out_f = os.path.join(HERE, "spd_probe.json")
res = json.load(open(out_f)) if os.path.exists(out_f) else {}
p, N = 19, 16
dm18, bs, _ = S.C.setup("1UBQ", p, 18)
dm = dm18[:N, :N]
tt, R = S.ref(p, N)
for eps in (float(sys.argv[1]),):
    if str(eps) in res:
        continue
    st = {}
    t0 = time.time()
    times, Sx, F, nstr, norm2 = SP.pauli_correlators(dm, 2e-6, 40, 0, bs, eps=eps, record_every=10,
                                                      time_budget_s=float(sys.argv[2]), stats=st)
    row = dict(eps=eps, secs=time.time() - t0, steps_done=st.get("steps_done"), peak_strings=st.get("peak_strings"),
               times_us=[float(x) * 1e6 for x in times], n_strings=[int(x) for x in nstr],
               kept_norm2=[float(x) for x in norm2])
    for i, t in enumerate(times):
        tu = round(float(t) * 1e6)
        if tu in (40, 80):
            ti = int(np.argmin(abs(tt - tu)))
            row[f"err_raw_{tu}"] = max(abs(F[b][i] - R[b][ti]) for b in bs)
            row[f"err_ren_{tu}"] = max(abs(F[b][i] / norm2[i] - R[b][ti]) for b in bs)
    res[str(eps)] = row
    json.dump(res, open(out_f + ".tmp", "w"), indent=1); os.replace(out_f + ".tmp", out_f)
    print(json.dumps({k: v for k, v in row.items() if not isinstance(v, list)}), "\n n_strings", row["n_strings"],
          "\n kept_norm2", [round(x, 4) for x in row["kept_norm2"]])
