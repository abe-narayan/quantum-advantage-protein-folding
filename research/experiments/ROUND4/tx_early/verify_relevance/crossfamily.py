"""Collect the cross-family runs (run_baware.py) and compare with the lane's probe-centred ladder -> crossfamily.json."""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANE = os.path.dirname(HERE)
SIG = 0.01
S = json.load(open(os.path.join(LANE, "tx_early_summary.json")))
runs = {}
for p in glob.glob(os.path.join(HERE, "runs", "*_t20.json")):
    d = json.load(open(p))
    runs[os.path.basename(p)[:-5]] = d


def F(tag, b):
    return runs[tag]["F"][str(b)][0]


out = dict(sigma=SIG, comparisons=[], cpu_s_total=sum(r["cpu_s"] for r in runs.values()),
           peak_rss_GB=max(r.get("peak_rss_GB", 0) for r in runs.values()))
spec = [
    # (probe, reference tag, test tag, what differs, note)
    (19, "1UBQ_p19_N20_pc_xnone_echo_R1_complex64_s4242_t20", "1UBQ_p19_N20_baware_x24-26_echo_R1_complex64_s4242_t20",
     "same N=20, same draws (CRN): ranks {18,19} swapped for {24 HG23/ILE3, 26 HG2/GLU16}"),
    (19, "1UBQ_p19_N20_pc_xnone_echo_R1_complex64_s4242_t20", "1UBQ_p19_N21_add1_x24_echo_R1_complex64_s4242_t20",
     "pure addition of rank 24 (HG23/ILE3; 82% of M2 of b8) to the probe-centred N=20 cluster"),
    (19, "1UBQ_p19_N20_pc_xnone_echo_R1_complex64_s4242_t20", "1UBQ_p19_N21_add1_x26_echo_R1_complex64_s4242_t20",
     "pure addition of rank 26 (HG2/GLU16; 64% of M2 of b9) to the probe-centred N=20 cluster"),
    (245, "1UBQ_p245_N20_pc_xnone_echo_R1_complex64_s4242_t20", "1UBQ_p245_N20_baware_x48-31_echo_R1_complex64_s4242_t20",
     "same N=20, same draws (CRN): ranks {18,19} swapped for {48 HG3/LYS27, 31 HG2/LYS29}"),
    (245, "1UBQ_p245_N20_pc_xnone_echo_R1_complex64_s4242_t20", "1UBQ_p245_N21_add1_x48_echo_R1_complex64_s4242_t20",
     "pure addition of rank 48 (HG3/LYS27; 49% of M2 of b7) to the probe-centred N=20 cluster"),
]
for p, ref, test, what in spec:
    if ref not in runs or test not in runs:
        continue
    row = dict(probe=p, ref=ref, test=test, what=what, sites={})
    for b in (1, 7, 8, 9):
        c = S["cells"][f"p{p}_t40_b{b}"]
        row["sites"][f"b{b}"] = dict(
            F_ref=F(ref, b), F_test=F(test, b), dF=F(test, b) - F(ref, b), dF_over_sigma=(F(test, b) - F(ref, b)) / SIG,
            lane_F20_R2=c["F20"], lane_F22=c["F22"], lane_claimed_max_move_18_22=abs(c["F22"] - c["F_ladder_ref"]["18"]),
            test_minus_lane_F22_over_sigma=(F(test, b) - c["F22"]) / SIG)
    out["comparisons"].append(row)

# consistency of this folder's probe-centred N=20 (R=1) with the lane's N=20 (R=2)
out["pc20_R1_vs_lane_F20_R2"] = {
    f"p{p}_b{b}": runs[f"1UBQ_p{p}_N20_pc_xnone_echo_R1_complex64_s4242_t20"]["F"][str(b)][0] - S["cells"][f"p{p}_t40_b{b}"]["F20"]
    for p in (19, 245) for b in (1, 7, 8, 9)}
with open(os.path.join(HERE, "crossfamily.json.tmp"), "w") as f:
    json.dump(out, f, indent=1)
os.replace(os.path.join(HERE, "crossfamily.json.tmp"), os.path.join(HERE, "crossfamily.json"))
for r in out["comparisons"]:
    print(r["probe"], r["what"])
    for b, s in r["sites"].items():
        print("   %s F_ref %.4f F_test %.4f dF %+.4f (%+.1f sigma) | lane F22 %.4f, lane |F22-F18| %.4f" % (
            b, s["F_ref"], s["F_test"], s["dF"], s["dF_over_sigma"], s["lane_F22"], s["lane_claimed_max_move_18_22"]))
print("pc20 R1 - lane F20 R2:", {k: round(v, 4) for k, v in out["pc20_R1_vs_lane_F20_R2"].items()})
print("cpu_s_total %.0f, peak RSS %.2f GB" % (out["cpu_s_total"], out["peak_rss_GB"]))
