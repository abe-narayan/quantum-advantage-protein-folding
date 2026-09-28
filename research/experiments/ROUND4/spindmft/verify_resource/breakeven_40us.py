"""Break-even arithmetic for the ONLY window the claim calls classically reachable (t = 40 us), plus 80/120 us for
reference.  Quantum side: the ROUND3 resource-audit model (ROUND3/r1sim_exact_reach/verify_resource/resource_audit.py,
q_curve), re-evaluated for ONE echo time instead of the 8-time curve: circuit |z> -> U(t) -> Z_a -> U(t)^dag -> measure
all Z; first-order Trotter dt = 2 us (the reference circuit); 3 arbitrary rotations per pair gate; 1.15 log2(1/eps)+9.2 T
per rotation; eps_tot = 1e-3 per circuit; sigma = 0.01 -> 1e4 shots (var <= 1 - F^2), all 4 sites read per shot;
depth-limited wall clock with unlimited factories and one QPU (the case most favourable to quantum).
Classical side: MEASURED single-core CPU seconds from the lane's out/*.json and from this verifier's runs/*.json.
Pure arithmetic (< 1 CPU-s).  Writes breakeven_40us.json."""
import glob
import json
import math
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
SIGMA = 0.01
T_LAYER = {"1us": 1e-6, "10us": 1e-5, "170us": 1.7e-4}


def q_one_time(N, M, n_steps, trotter_mult=1.0, eps_tot=1e-3):
    steps = 2 * n_steps * trotter_mult                     # forward + backward legs
    rot = 3 * M * steps
    t_rot = 1.15 * math.log2(rot / eps_tot) + 9.2
    reps = 1 / SIGMA ** 2
    colours = N - 1 if M >= N * (N - 1) / 2 - 1e-9 else min(N - 1, 2 * M / N + 1)
    T_count = reps * steps * 3 * M * t_rot
    T_depth = reps * steps * colours * 3 * t_rot
    cnot = 3 * M * steps
    return dict(N=N, pair_gates_per_step=M, trotter_steps_per_shot=steps, T_per_rotation=t_rot, T_count=T_count,
                T_depth=T_depth, wall_s={k: T_depth * v for k, v in T_LAYER.items()},
                cnot_per_shot=cnot, nisq_ln_fidelity_at_1e_3=-1e-3 * cnot, logical_qubits=N)


# pair counts of the actual 1UBQ couplings (whole protein), as in ROUND3 E_coupling_stats
import sys
sys.path.insert(0, os.path.join(ROOT, "src"))
from qapf.nmr import spins as SP  # noqa: E402
names, xyz, _ = SP.read_h_coords(os.path.join(ROOT, "data", "instruments", "nmr", "1UBQ_H.pdb"))
r = np.random.default_rng(1000); v = r.standard_normal(3); b0 = v / np.linalg.norm(v)   # = fastecho.random_b0(1000)
Dall = SP.couplings(xyz, b0)                                   # rad/s (spins.couplings docstring)
iu = np.triu_indices(len(xyz), 1)
d = np.abs(Dall[iu]) / (2 * np.pi)                             # Hz, as ROUND3 couplings_stats
M629_dense = len(iu[0])
M629_30 = int((d > 30).sum())

quantum = {}
for t_us, n in ((40, 20), (80, 40), (120, 60)):
    rows = [q_one_time(N, N * (N - 1) // 2, n) for N in (16, 20, 22)]
    rows.append(dict(q_one_time(629, M629_dense, n), note="whole protein, dense"))
    rows.append(dict(q_one_time(629, M629_30, n), note="whole protein, |d| > 30 Hz (truncation error unaudited)"))
    rows.append(dict(q_one_time(629, M629_30, n, trotter_mult=4), note="629, 30 Hz cut, dt = 0.5 us (Trotter accuracy x4)"))
    quantum[str(t_us)] = rows

# classical MEASURED costs (single core)
cls = {}
for f in sorted(glob.glob(os.path.join(HERE, "runs", "pp_*.json"))):
    s = json.load(open(f))
    if "F" not in s:
        continue
    cls[os.path.basename(f)] = dict(family=s["family"], N=s["N"], steps=s["steps"], cpu_s=s["cpu_s_total"],
                                    peak_rss_GB=s.get("peak_rss_GB"))
lane = {}
for f in sorted(glob.glob(os.path.join(LANE, "out", "*.json"))):
    if f.endswith(".ckpt.json"):
        continue
    s = json.load(open(f))
    c = s.get("cpu", s.get("cpu_s"))
    if c is not None:
        lane[os.path.basename(f)] = c
pipeline_40 = dict(
    spinDMFT_bath_selfconsistent_protein_s=lane["sr_protein_T120_M384.json"],
    spinDMFT_bath_W18_both_probes_s=lane["sr_1UBQ_p19_N18_T120_M4096.json"] + lane["sr_1UBQ_p245_N18_T120_M4096.json"],
    spinDMFT_embedded_probeb_protein_plus_W18_both_probes_s=sum(lane[f"emb_p{p}_W{W}_nc10_probeb_sr_M512_s7.json"]
                                                               for p in (19, 245) for W in ("protein", "18")),
    exact_baware_N20_per_series_mean_s=float(np.mean([v["cpu_s"] for k, v in cls.items() if v["family"] == "pairb" and v["N"] == 20])),
    exact_baware_N18_per_series_mean_s=float(np.mean([v["cpu_s"] for k, v in cls.items() if v["family"] == "pairb" and v["N"] == 18])),
    exact_probe_family_N18_per_site_s=np.mean([v["cpu_s"] for k, v in cls.items() if v["family"] == "probe" and v["N"] == 18]),
)
KEY = "total_all_8_series_s_(b-aware N20 x8 + spinDMFT; 40/80/120 us in one pass)"
pipeline_40[KEY] = (8 * pipeline_40["exact_baware_N20_per_series_mean_s"]
    + pipeline_40["spinDMFT_bath_selfconsistent_protein_s"] + pipeline_40["spinDMFT_bath_W18_both_probes_s"]
    + pipeline_40["spinDMFT_embedded_probeb_protein_plus_W18_both_probes_s"])
pipeline_40["exact_only_b-aware_N18_x8_s"] = 8 * pipeline_40["exact_baware_N18_per_series_mean_s"]
out = dict(quantum_one_time_point=quantum, classical_measured_runs=cls, classical_pipeline_40us=pipeline_40,
           ratio_note="quantum depth-limited wall (1 us T layer, one QPU, unlimited factories) / classical single-core "
                      "CPU for the same 8 series at 40 us")
q40d = [r_ for r_ in quantum["40"] if r_["N"] == 629][0]["wall_s"]["1us"]
q40 = [r_ for r_ in quantum["40"] if r_["N"] == 629][1]["wall_s"]["1us"]
q40_20 = [r_ for r_ in quantum["40"] if r_["N"] == 20][0]["wall_s"]["1us"]
tot = pipeline_40[KEY]
out["ratio_quantum629cut30_over_classical_40us"] = 2 * q40 / tot     # 2 probes (4 sites per shot each)
out["ratio_quantum629dense_over_classical_40us"] = 2 * q40d / tot
out["ratio_quantum629cut30_over_exact_only_N18"] = 2 * q40 / pipeline_40["exact_only_b-aware_N18_x8_s"]
out["ratio_quantum20_over_classical_40us"] = 2 * q40_20 / tot
json.dump(out, open(os.path.join(HERE, "breakeven_40us.json.tmp"), "w"), indent=1, default=float)
os.replace(os.path.join(HERE, "breakeven_40us.json.tmp"), os.path.join(HERE, "breakeven_40us.json"))
for t_us in ("40", "80", "120"):
    for r_ in quantum[t_us]:
        print(t_us, r_["N"], r_.get("note", ""), "M", r_["pair_gates_per_step"], "T", f"{r_['T_count']:.2e}",
              "wall@1us %.3g s" % r_["wall_s"]["1us"], "@10us %.3g s" % r_["wall_s"]["10us"],
              "lnF_nisq %.0f" % r_["nisq_ln_fidelity_at_1e_3"])
print(json.dumps(pipeline_40, indent=1, default=float))
print({k: round(v, 2) for k, v in out.items() if k.startswith("ratio_q")})
