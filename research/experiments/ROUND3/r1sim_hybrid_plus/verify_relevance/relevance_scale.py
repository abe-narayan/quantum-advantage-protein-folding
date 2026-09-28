"""Relevance verifier for lane r1sim_hybrid_plus (ROUND3).

Question: are the lane's approximation errors (the quantity its "approximation-hardness" claim is about)
large compared with the errors that matter for the physical, protein-structure question?

Compares, per probe and N, over b in {1,7,8,9} and t in [80, 320] us:
  (1) best polynomial-family error from the lane's summary.json (MEASURED by the lane)
  (2) the reference's own finite-N truncation, max |F_N - F_{N-2}| (MEASURED, exact typicality cones)
  (3) the Hamiltonian-model error scale of the idealised model vs a physical protein sample
      (5-66 sigma: methyl rotation 7-49 sigma, 1 kHz offsets 5-66 sigma, R1_physics_feasibility/README.md, MEASURED at N=10)
  (4) the N=20 checkpoint (only t <= 40 us done) vs N=18 at the times available.

Pure post-processing of existing JSON. Runs in < 1 s. Single-threaded. Writes relevance_scale.json atomically.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
REPO = os.path.abspath(os.path.join(LANE, "..", "..", "..", ".."))
CONE = os.path.join(REPO, "research", "experiments", "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
SIGMA = 0.01
T_LO, T_HI = 80.0, 320.0
BS = ["1", "7", "8", "9"]


def load_cone(probe, N):
    p = os.path.join(CONE, f"1UBQ_p{probe}_N{N}.json")
    if not os.path.exists(p):
        return None
    return json.load(open(p))


def trunc(probe, N):
    a, b = load_cone(probe, N), load_cone(probe, N - 2)
    if a is None or b is None:
        return None
    ts = a["times_us"]
    best = (0.0, None, None)
    for bb in BS:
        for i, t in enumerate(ts):
            if T_LO - 1e-6 <= t <= T_HI + 1e-6:
                d = abs(a["F"][bb][i] - b["F"][bb][i])
                if d > best[0]:
                    best = (d, bb, round(t))
    return {"max_abs_dF": round(best[0], 4), "at_b": best[1], "at_t_us": best[2],
            "in_sigma": round(best[0] / SIGMA, 1),
            "typicality_err_N": a["err_typ"], "typicality_err_Nm2": b["err_typ"]}


def lane_best():
    s = json.load(open(os.path.join(LANE, "summary.json")))
    out = {}
    for r in s["runs"]:
        key = f"p{r['probe']}_N{r['N']}"
        tag = f"{r['bath']}/{r['ba']}/{r['est']}/sizes{r['sizes']}"
        cur = out.get(key)
        if cur is None or r["max_err"] < cur["max_err"]:
            out[key] = {"max_err": r["max_err"], "method": tag, "max_se": r.get("max_se"),
                        "secs": r.get("secs"), "note": "includes lambda calibrated on same-probe exact N-2 where present"}
    zc = {}
    for r in s["zero_compute"]:
        key = f"p{r['probe']}_N{r['N']}"
        cur = zc.get(key)
        if cur is None or r["max_err"] < cur["max_err"]:
            zc[key] = {"max_err": r["max_err"], "method": r["method"]}
    return out, zc


def n20_check():
    p = os.path.join(CONE, "1UBQ_p19_N20.json.ckpt.json")
    if not os.path.exists(p):
        return None
    ck = json.load(open(p))
    ref = load_cone(19, 18)
    rows = {}
    for step, fb in ck["done"].items():
        t = 2.0 * int(step)
        i = [j for j, tt in enumerate(ref["times_us"]) if abs(tt - t) < 1e-6]
        if not i:
            continue
        rows[str(t)] = {b: round(abs(fb[b] - ref["F"][b][i[0]]), 5) for b in BS}
    return {"times_done_us": sorted(float(k) for k in rows), "abs_dF_N20_vs_N18": rows,
            "note": "checkpoint in progress; no point inside the 80-320 us window yet"}


def main():
    lane, zc = lane_best()
    res = {"sigma": SIGMA, "window_us": [T_LO, T_HI], "rows": {}}
    phys_lo, phys_hi = 5 * SIGMA, 66 * SIGMA
    for probe in (19, 245):
        for N in (14, 16, 18):
            key = f"p{probe}_N{N}"
            tr = trunc(probe, N)
            lb = lane.get(key)
            row = {"lane_best_polynomial": lb, "lane_best_zero_compute": zc.get(key),
                   "reference_truncation_vs_Nm2": tr,
                   "physical_model_error_scale": [phys_lo, phys_hi]}
            if lb and tr:
                row["ratio_lane_err_to_truncation"] = round(lb["max_err"] / max(tr["max_abs_dF"], 1e-9), 2)
                row["lane_err_below_min_physical_model_error"] = lb["max_err"] < phys_lo
                row["lane_err_below_max_physical_model_error"] = lb["max_err"] < phys_hi
            res["rows"][key] = row
    res["n20_checkpoint"] = n20_check()
    tmp = os.path.join(HERE, "relevance_scale.json.tmp")
    with open(tmp, "w") as f:
        json.dump(res, f, indent=1)
    os.replace(tmp, os.path.join(HERE, "relevance_scale.json"))
    for k, r in res["rows"].items():
        lb, tr = r["lane_best_polynomial"], r["reference_truncation_vs_Nm2"]
        print(k, "lane_best", lb and (lb["max_err"], lb["method"]), "| trunc", tr and (tr["max_abs_dF"], tr["at_b"], tr["at_t_us"]),
              "| ratio", r.get("ratio_lane_err_to_truncation"), "| <5sigma phys", r.get("lane_err_below_min_physical_model_error"))
    print("N20:", json.dumps(res["n20_checkpoint"]))


if __name__ == "__main__":
    main()
