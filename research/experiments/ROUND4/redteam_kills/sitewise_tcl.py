"""ROUND4 red team, RT-B2: DQ profiled gain with a SITE-DEPENDENT classical reach, informed by the RT-B size ladder
(1UBQ p19, N = 10..18): non-methyl butterfly sites step-converged (|F18 - F16| <= 0.0017) through 80 us, so their echo
rows are classical up to t_cl_nm = 80 us; methyl-proton butterfly sites (static-methyl model not converged at N = 18
from 50 us) are classical only up to t_cl_me in {0, 40, 50} us.  Classical side also includes the SECULAR transfer
(joint profiling over shared nuisances), as in RT-A2.  Physical T2 (rotor-averaged network), literature DQ envelopes.
Post-processing only (seconds).  Output: sitewise_tcl.json"""
import json, os
import numpy as np
import analyze_profiled as AP

HERE = os.path.dirname(os.path.abspath(__file__))
out = {}
for probe in (("1UBQ", 19), ("1UBQ", 245), ("1PGA", 390)):
    tag = f"pg_dq_k1_{probe[0]}_p{probe[1]}"
    m, z = AP.load(tag); B = AP.build(m, z)
    ms, zs = AP.load(tag.replace("pg_dq_", "pg_sec_")); Bs = AP.build(ms, zs)
    names_bs = [m["names"][b] for b in m["bs"]]
    rot = set(n for g in m["rotor_groups_in_cluster"] for n in g)
    me = np.array([n in rot or n.startswith(("HG2", "HD1", "HD2", "HB1", "HB2", "HB3")) and n.split("/")[1][:3] in
                   ("ALA", "VAL", "LEU", "ILE", "THR", "MET") and n in rot for n in names_bs])
    me = np.array([n in rot for n in names_bs])
    site = np.tile(np.arange(B["nb"]), B["nt"])
    T2 = AP.T2s(m)["physical"]
    rec = dict(names_bs=names_bs, methyl_sites=[n for n, f in zip(names_bs, me) if f], cases={})
    for ename in ("DQ_local_7.5T2", "DQ_LE_12.5T2", "DQ_LE_19T2", "hyp_50T2"):
        A = AP.ENVS["dq"][ename](B["trow"] / T2)
        for pn in ("none", "moderate", "tight", "offsets_known"):
            pr = AP.PRIORS[pn]
            kk = AP.keep_cols(B["kinds"], pr); kinds = [B["kinds"][k] for k in kk]
            JSall = np.vstack([B["JS"][:, kk], Bs["JS"][:, kk]])
            JG = B["JG"][:, kk] * A[:, None]
            Fq = JSall.T @ JSall + JG.T @ JG + np.diag(AP.prior_vec(kinds, pr))
            cq = AP.crb_marg(AP.eff_struct(Fq, kinds))
            for tme in (0, 40, 50, 80):
                cl = np.where(me[site], B["trow"] < tme - 1e-9, B["trow"] < 80 - 1e-9)
                Fc = JSall.T @ JSall + JG[cl].T @ JG[cl] + np.diag(AP.prior_vec(kinds, pr))
                cc = AP.crb_marg(AP.eff_struct(Fc, kinds))
                with np.errstate(invalid="ignore", divide="ignore"):
                    g = (cc / cq) ** 2
                g = g[~np.isnan(g)]
                rec["cases"][f"{ename}|{pn}|tcl_methyl={tme}|tcl_nonmethyl=80"] = dict(
                    g_med=float(np.median(g)), g_max=float(np.max(g[np.isfinite(g)])))
    out[tag] = rec
json.dump(out, open(os.path.join(HERE, "sitewise_tcl.json.tmp"), "w"), indent=1)
os.replace(os.path.join(HERE, "sitewise_tcl.json.tmp"), os.path.join(HERE, "sitewise_tcl.json"))
for tag, r in out.items():
    print(tag, r["names_bs"], "methyl:", r["methyl_sites"])
    for k, v in r["cases"].items():
        if "|none|" in k or "|moderate|" in k:
            print(f"   {k:58s} g_med={v['g_med']:.2f} g_max={v['g_max']:.2f}")
