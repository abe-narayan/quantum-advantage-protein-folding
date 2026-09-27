"""R1 value lens, part 1: what is the echo window worth, in Angstrom?

Reads the MEASURED C1 / C1-HN jobs (research/results/RAW/nmr_gate*/*.json), rebuilds the full Jacobians
J_S[p, (b,t)] = dS_ab(t)/dphi_p and J_F[p, (b,t)] = dF_ab(t)/dphi_p stored by scripts/nmr_gate.py (central finite
differences, h = 0.05 A), and computes Fisher matrices with white noise sigma per data point:

    F_S          = J_S J_S^T / sigma^2                         transfer, all times (classically exact / sparse-Pauli exact)
    F_F          = J_F J_F^T / sigma^2                         echo, all times
    F_F_easy     = echo restricted to t < t_c* (best adversary failure time, stored per job)
    classical    = F_S + F_F_easy     (everything a classical *approximate* forward model can use)
    quantum      = F_S + F_F          (everything an exact forward model can use)

Cramer-Rao bounds (CRB): marginal sigma_phi_p = sqrt([F^-1]_pp) (other parameters as nuisance) and conditional
1/sqrt(F_pp).  Units: Angstrom (phi = displacement in A).  Everything scales linearly with sigma, so CRB at another noise
level is CRB * sigma'/0.01.  Also: per-parameter repetition-saving factor g_p = CRB_cl^2 / CRB_q^2, and the generalised
eigenvalue spectrum of quantum vs classical Fisher matrices (max = the best-case repetition saving in any direction).

No new dynamics are run: pure post-processing of existing RAW (seconds of CPU).
Output: fi_value.json next to this script.
"""
import glob
import json
import os

import numpy as np
from scipy.linalg import eigh

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))


def jac(params, key, bs, nt):
    J = np.zeros((len(params), len(bs) * nt))
    for i, p in enumerate(params):
        J[i] = np.concatenate([np.asarray(p[key][str(b)], float) for b in bs])
    return J


def mask_before(bs, nt, tc):
    m = np.zeros(len(bs) * nt, bool)
    for k in range(len(bs)):
        m[k * nt: k * nt + tc] = True
    return m


def crb(F, ridge=1e-12):
    F = 0.5 * (F + F.T)
    w, V = np.linalg.eigh(F)
    w = np.maximum(w, ridge * max(w.max(), 1e-300))
    inv = (V / w) @ V.T
    return np.sqrt(np.diag(inv)), 1 / np.sqrt(np.maximum(np.diag(F), 1e-300)), float(w.max() / w.min())


def main():
    rows = []
    lcj = os.path.join(HERE, "lightcone.json")
    LC = {j["job"]: j for j in json.load(open(lcj))["jobs"]} if os.path.exists(lcj) else {}
    files = sorted(glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate", "*.json")) +
                   glob.glob(os.path.join(ROOT, "research", "results", "RAW", "nmr_gate_hn", "*.json")))
    for f in files:
        d = json.load(open(f))
        params, bs = d["params"], d["bs"]
        nt = len(d["times"])
        sig = d["sigma"]
        # drop duplicate parameters (rigid shift of a one-proton residue duplicates a radial one)
        keep, seen = [], []
        for p in params:
            v = np.concatenate([np.asarray(p["dS"][str(b)]) for b in bs])
            if any(np.allclose(v, s, rtol=1e-9, atol=1e-12) for s in seen):
                continue
            seen.append(v)
            keep.append(p)
        params = keep
        JS = jac(params, "dS", bs, nt)
        FS = JS @ JS.T / sig ** 2
        row = dict(file=os.path.relpath(f, ROOT).replace("\\", "/"), pdb=d["pdb"], probe=d["probe_name"], N=d["N"],
                   orient=d["orient"], gamma=d["gamma"], dt_us=d["dt"] * 1e6, tmax_us=d["times"][-1] * 1e6,
                   n_data=len(bs) * nt, network="amide-only" if "_hn" in f else "dense",
                   params=[p["name"] for p in params], r=[p["r"] for p in params])
        cS, cSc, condS = crb(FS)
        row.update(CRB_transfer_marg=cS.tolist(), CRB_transfer_cond=cSc.tolist(), cond_FS=condS)
        if "dF" in params[0] and d.get("best_t_c_otoc_index") is not None:
            JF = jac(params, "dF", bs, nt)
            tc = int(d["best_t_c_otoc_index"])
            m = mask_before(bs, nt, tc)
            FF = JF @ JF.T / sig ** 2
            FFe = JF[:, m] @ JF[:, m].T / sig ** 2
            cF, cFc, condF = crb(FF)
            ccl, _, _ = crb(FS + FFe)
            cq, _, _ = crb(FS + FF)
            # pessimistic-for-classical variant: if transfer, too, were classically unreachable after t_c* at large N_eff
            FSe = JS[:, m] @ JS[:, m].T / sig ** 2
            cce, _, _ = crb(FSe + FFe)
            gspec_e = eigh(FS + FF, FSe + FFe + 1e-12 * np.trace(FSe + FFe) * np.eye(len(FS)), eigvals_only=True)
            ce, _, _ = crb(FFe) if np.trace(FFe) > 0 else (np.full(len(params), np.inf), None, None)
            # generalised eigenvalues of quantum vs classical information
            A = FS + FF
            B = FS + FFe
            B = B + 1e-12 * np.trace(B) * np.eye(len(B))
            gspec = eigh(A, B, eigvals_only=True)
            # exact-classical reach (lightcone.py): data before t_ex are computable exactly on a leadership machine
            lj = LC.get(os.path.basename(f))
            if lj is not None:
                tt_ = np.asarray(d["times"]) * 1e6
                for lab in ("infl_med", "infl_fast", "infl_slow"):
                    tex = lj.get(f"t_ex_N47_{lab}_us")
                    kx = nt if tex is None else int(np.searchsorted(tt_, tex, side="right"))
                    mx = mask_before(bs, nt, kx)
                    FFx = JF[:, mx] @ JF[:, mx].T / sig ** 2
                    FSx = JS[:, mx] @ JS[:, mx].T / sig ** 2
                    c1, _, _ = crb(FS + FFx)
                    c2, _, _ = crb(FSx + FFx)
                    row[f"t_ex_{lab}_us"] = tex
                    row[f"g_exact_reach_{lab}"] = ((c1 / cq) ** 2).tolist()             # transfer all + echo < t_ex
                    row[f"g_exact_reach_pure_{lab}"] = ((c2 / cq) ** 2).tolist()        # everything < t_ex
                    row[f"frac_echoFI_beyond_tex_{lab}"] = float(1 - np.trace(FFx) / np.trace(FF))
            row.update(t_c_echo_us=d["times"][tc] * 1e6 if tc < nt else None, adversary=d["best_adversary_otoc"],
                       CRB_echo_marg=cF.tolist(), CRB_echo_cond=cFc.tolist(), cond_FF=condF,
                       CRB_echo_easy_marg=ce.tolist(),
                       CRB_classical_marg=ccl.tolist(), CRB_quantum_marg=cq.tolist(),
                       g_param=((ccl / cq) ** 2).tolist(), gain_spectrum=sorted(gspec.tolist()),
                       CRB_classical_early_marg=cce.tolist(), g_param_early=((cce / cq) ** 2).tolist(),
                       gain_spectrum_early=sorted(gspec_e.tolist()),
                       FI_echo_over_transfer=(np.diag(FF) / np.maximum(np.diag(FS), 1e-300)).tolist())
        rows.append(row)

    # ------------------------------------------------------------------ aggregates
    def collect(key, net, gamma0=True):
        v = []
        for r in rows:
            if r["network"] == net and key in r and (not gamma0 or r["gamma"] == 0):
                v += [x for x in r[key] if np.isfinite(x)]
        return np.asarray(v)

    agg = {}
    for net in ("dense", "amide-only"):
        a = {}
        for key in ("r", "CRB_transfer_marg", "CRB_echo_marg", "CRB_classical_marg", "CRB_quantum_marg", "g_param",
                    "CRB_classical_early_marg", "g_param_early", "g_exact_reach_infl_med", "g_exact_reach_pure_infl_med",
                    "g_exact_reach_infl_fast", "g_exact_reach_pure_infl_fast"):
            v = collect(key, net)
            if len(v):
                a[key] = dict(n=int(len(v)), min=float(v.min()), median=float(np.median(v)), max=float(v.max()))
        gs = [max(r["gain_spectrum"]) for r in rows if r["network"] == net and "gain_spectrum" in r]
        if gs:
            a["max_gain_eig"] = dict(min=float(min(gs)), median=float(np.median(gs)), max=float(max(gs)))
        ge = [max(r["gain_spectrum_early"]) for r in rows if r["network"] == net and "gain_spectrum_early" in r]
        if ge:
            a["max_gain_eig_early"] = dict(min=float(min(ge)), median=float(np.median(ge)), max=float(max(ge)))
        for lab in ("infl_med", "infl_fast", "infl_slow"):
            fb = [r[f"frac_echoFI_beyond_tex_{lab}"] for r in rows if r["network"] == net and f"frac_echoFI_beyond_tex_{lab}" in r]
            tx = [r[f"t_ex_{lab}_us"] for r in rows if r["network"] == net and f"t_ex_{lab}_us" in r]
            if fb:
                a[f"frac_echoFI_beyond_tex_{lab}"] = dict(min=float(min(fb)), median=float(np.median(fb)), max=float(max(fb)))
                a[f"t_ex_{lab}_us"] = tx
        # sigma needed for the CLASSICAL route to reach a target precision (CRB scales linearly with sigma)
        v = collect("CRB_classical_marg", net)
        a["sigma_needed_classical_for_0.1A_median"] = float(0.01 * 0.1 / np.median(v)) if len(v) else None
        a["frac_params_classical_CRB_below_0.1A"] = float(np.mean(v < 0.1)) if len(v) else None
        a["frac_params_classical_CRB_below_0.05A"] = float(np.mean(v < 0.05)) if len(v) else None
        agg[net] = a
    out = dict(note="CRB in Angstrom at sigma = 0.01 per data point; scales linearly with sigma. "
                    "classical = transfer(all t) + echo(t < t_c*); quantum = transfer + echo(all t).",
               rows=rows, aggregate=agg)
    json.dump(out, open(os.path.join(HERE, "fi_value.json"), "w"), indent=1)

    print(f"{'job':40s} {'param':22s} {'r':>5s} {'CRB_S':>7s} {'CRB_F':>7s} {'CRB_cl':>7s} {'CRB_q':>7s} {'g':>6s}")
    for r in rows:
        if r["gamma"] != 0:
            continue
        for i, name in enumerate(r["params"]):
            tag = f"{r['pdb']}{'HN' if r['network'] != 'dense' else ''} {r['probe']} o{r['orient']} N{r['N']}"
            if "CRB_classical_marg" in r:
                print(f"{tag:40s} {name:22s} {r['r'][i]:5.2f} {r['CRB_transfer_marg'][i]:7.3f} {r['CRB_echo_marg'][i]:7.3f} "
                      f"{r['CRB_classical_marg'][i]:7.3f} {r['CRB_quantum_marg'][i]:7.3f} {r['g_param'][i]:6.1f}")
            else:
                print(f"{tag:40s} {name:22s} {r['r'][i]:5.2f} {r['CRB_transfer_marg'][i]:7.3f}")
    print(json.dumps(agg, indent=1))


if __name__ == "__main__":
    main()
