"""CR4-B analysis: profiled K-105 gains (red team's own functions) on the N = 10 Fisher model vs b-aware / probe-centred
N = 12 extensions.  Pure post-processing (seconds).  Writes critic/fi_nscale_summary.json.

Cases per probe (physical T2 = rotor-averaged network T2, as the red team):
  RT_full      red team npz (N = 10, Omega + eta + eps0 + eps_g columns, echo to 320 us) -> must reproduce
               redteam_kills/profiled_summary.json (validation of the reuse)
  RT_partial   same npz, Omega and eta columns dropped (calibrates 'moderate_partial' against the full profile)
  RT_trunc     same npz, echo rows beyond 160 us zeroed (calibrates the echo-time truncation)
  base10 / baware12 / probe12   this check's runs (struct + eps0 + eps_g columns, echo <= 160 us)
Priors: known (struct only), moderate (full or partial nuisance set as available), none.
"""
from __future__ import annotations

import json
import os
import sys

sys.dont_write_bytecode = True
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RT = os.path.join(os.path.dirname(HERE), "redteam_kills")
sys.path.insert(0, RT)
import analyze_profiled as AP  # noqa: E402

ENVS = {"PE_gauss_4T2": AP.ENVS["sec"]["PE_gauss_4T2"], "LE_logistic_6.7T2": AP.ENVS["sec"]["LE_logistic_6.7T2"]}
PRI = {"known": "drop", "moderate": AP.PRIORS["moderate"], "none": None}
TCLS = (0, 40)


def Bfrom(m, z, drop_kinds=(), trunc_us=None):
    B = AP.build(m, z)
    keep = [k for k, kd in enumerate(B["kinds"]) if kd not in drop_kinds]
    B = dict(B, cols=[B["cols"][k] for k in keep], kinds=[B["kinds"][k] for k in keep],
             JS=B["JS"][:, keep], JG=B["JG"][:, keep].copy())
    if trunc_us is not None:
        B["JG"][B["trow"] > trunc_us + 1e-9] = 0.0
    return B


def gtable(B, T2):
    out = {}
    for en, ef in ENVS.items():
        A_row = ef(B["trow"] / T2)
        for pn, pr in PRI.items():
            for tcl in TCLS:
                g, ge, cq, cc = AP.gains(B, A_row, tcl, pr)
                gv = g[~np.isnan(g)]
                out[f"{en}|{pn}|tcl{tcl}"] = dict(g_med=float(np.median(gv)), g_max=float(np.max(gv[np.isfinite(gv)])),
                                                  g_per_param=[float(x) for x in g])
    return out


def main():
    res = dict(note=__doc__.split("\n")[0], probes={})
    rt_sum = json.load(open(os.path.join(RT, "profiled_summary.json")))["jobs"]
    for pdb, probe in (("1UBQ", 19), ("1UBQ", 245), ("1PGA", 325), ("1PGA", 390)):
        key = f"{pdb}_p{probe}"
        tag = f"pg_sec_k1_{pdb}_p{probe}"
        m, z = AP.load(tag)
        T2 = AP.T2s(m)["physical"]
        P = dict(T2_physical_us=T2, cases={})
        P["cases"]["RT_full"] = gtable(Bfrom(m, z), T2)
        P["cases"]["RT_partial"] = gtable(Bfrom(m, z, drop_kinds=("Omega", "eta")), T2)
        P["cases"]["RT_trunc160"] = gtable(Bfrom(m, z, trunc_us=160.0), T2)
        P["cases"]["RT_partial_trunc160"] = gtable(Bfrom(m, z, drop_kinds=("Omega", "eta"), trunc_us=160.0), T2)
        # validation vs the red team's stored summary
        ref = rt_sum[tag]["cases"]
        P["validation_RT_full_vs_summary_max_abs"] = max(
            abs(P["cases"]["RT_full"][f"{en}|{pn}|tcl{t}"]["g_med"] - ref[f"physical|{en}|{pn}"]["g_med_at"][str(t)])
            for en in ENVS for pn in PRI for t in TCLS)
        for var in ("base10", "baware12", "probe12"):
            f = os.path.join(HERE, "out", f"fi_{var}_{pdb}_p{probe}.json")
            if not os.path.exists(f):
                continue
            mm = json.load(open(f))
            if not mm.get("complete"):
                continue
            zz = np.load(os.path.join(HERE, "out", f"fi_{var}_{pdb}_p{probe}.npz"))
            P["cases"][var] = gtable(AP.build(mm, zz), T2)
            P.setdefault("clusters", {})[var] = dict(N=mm["N"], extra=mm.get("extra"),
                                                     M2b_coverage=mm.get("M2b_coverage"))
            if var == "base10":
                P["validation_base10_vs_RT"] = mm.get("validation_vs_redteam")
        res["probes"][key] = P
    json.dump(res, open(os.path.join(HERE, "fi_nscale_summary.json"), "w"), indent=1)
    # console
    for key, P in res["probes"].items():
        print(f"== {key}  T2 = {P['T2_physical_us']:.2f} us  validation RT_full vs summary: "
              f"{P['validation_RT_full_vs_summary_max_abs']:.2e}  clusters: "
              f"{ {v: (c['N'], c['extra']) for v, c in P.get('clusters', {}).items()} }")
        cases = list(P["cases"].keys())
        for en in ENVS:
            for pn in PRI:
                row = []
                for c in cases:
                    row.append(" ".join(f"{P['cases'][c][f'{en}|{pn}|tcl{t}']['g_med']:5.2f}" for t in TCLS))
                print(f"  {en:18s} {pn:9s} " + " | ".join(f"{c}:{r}" for c, r in zip(cases, row)))


if __name__ == "__main__":
    main()
