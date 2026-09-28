"""Back-test of two finite-size models on exact data only (no dynamics; -> backtest.json).
Predict the exact echo at the largest measured N_t from data at a smaller N_s:
  hybrid ('X converged'):  F_pred = H_{N_t} + floor_{N_t} + X_{N_s}   (exact H/floor at N_t: the ideal version of
                           the T-X hybrid, which uses H_inf instead of H_{N_t})
  flat   ('F converged'):  F_pred = F_{N_s}
Targets: N_t = 22 at 40 us (this lane); N_t = 20 at 40/80/120 us (reference F_20 checkpoint + VC honly H_20/floor_20).
X_{N_s} = F_{N_s} - H_{N_s} - floor_{N_s} from reference F (typicality_cone) and ROUND3 verify_classical honly H/floor."""
import glob, json, os
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.abspath(os.path.join(HERE, "..", ".."))
TC = os.path.join(EXP, "ADVERSARIAL", "R1_theory_hardness", "typicality_cone")
VC = os.path.join(EXP, "ROUND3", "r1sim_exact_reach", "verify_classical", "runs")
def J(p):
    with open(p) as f: return json.load(f)
def vc(p, N):
    d = J(glob.glob(os.path.join(VC, f"1UBQ_p{p}_N{N}_probe_honly_*.json"))[0]); return np.array(d["H"][:3]), np.array(d["floor"][:3])
out = dict(rows=[])
for p in (19, 245):
    ref = {N: J(os.path.join(TC, f"1UBQ_p{p}_N{N}.json"))["F"] for N in (14, 16, 18)}
    r20 = J(os.path.join(TC, f"1UBQ_p{p}_N20.json.ckpt.json"))["done"]
    HF = {N: vc(p, N) for N in (14, 16, 18, 20)}
    n22 = J(os.path.join(HERE, "runs", f"1UBQ_p{p}_N22_echo_R1_complex64_s4242_t20-40-60.json"))
    for b in ("1", "7", "8", "9"):
        # target N = 22, t = 40 us
        Ft = n22["F"][b][0]; Ht = n22["H"][0]; ft = n22["floor"][0]
        for Ns in (14, 16, 18):
            Fs = ref[Ns][b][1]; Xs = Fs - HF[Ns][0][0] - HF[Ns][1][0]
            out["rows"].append(dict(probe=p, site=int(b), t_us=40, N_t=22, N_s=Ns, F_t=Ft,
                                    err_hybrid=Ht + ft + Xs - Ft, err_flat=Fs - Ft))
        # target N = 20 (reference checkpoint), t = 40/80/120 us where available
        for ti, st in enumerate((20, 40, 60)):
            if str(st) not in r20:
                continue
            Ft = r20[str(st)][b]; Ht = HF[20][0][ti]; ft = HF[20][1][ti]
            for Ns in (14, 16):
                Fs = ref[Ns][b][ti + 1]; Xs = Fs - HF[Ns][0][ti] - HF[Ns][1][ti]
                out["rows"].append(dict(probe=p, site=int(b), t_us=2 * st, N_t=20, N_s=Ns, F_t=Ft,
                                        err_hybrid=Ht + ft + Xs - Ft, err_flat=Fs - Ft))
summ = {}
for (Nt, t) in sorted({(r["N_t"], r["t_us"]) for r in out["rows"]}):
    for Ns in (14, 16, 18):
        rr = [r for r in out["rows"] if r["N_t"] == Nt and r["t_us"] == t and r["N_s"] == Ns]
        if not rr: continue
        eh = np.array([r["err_hybrid"] for r in rr]); ef = np.array([r["err_flat"] for r in rr])
        summ[f"Nt{Nt}_t{t}_Ns{Ns}"] = dict(n=len(rr), rms_hybrid=float(np.sqrt(np.mean(eh**2))), max_hybrid=float(np.max(np.abs(eh))),
                                           mean_hybrid=float(eh.mean()), rms_flat=float(np.sqrt(np.mean(ef**2))),
                                           max_flat=float(np.max(np.abs(ef))), mean_flat=float(ef.mean()),
                                           flat_better=int(np.sum(np.abs(ef) < np.abs(eh))))
        s = summ[f"Nt{Nt}_t{t}_Ns{Ns}"]
        print(f"N_t={Nt} t={t:3d} N_s={Ns}: n={s['n']} hybrid rms {s['rms_hybrid']:.4f} max {s['max_hybrid']:.4f} mean {s['mean_hybrid']:+.4f} | "
              f"flat rms {s['rms_flat']:.4f} max {s['max_flat']:.4f} mean {s['mean_flat']:+.4f} | flat better {s['flat_better']}/{s['n']}")
out["summary"] = summ
with open(os.path.join(HERE, "backtest.json.tmp"), "w") as f: json.dump(out, f, indent=1)
os.replace(os.path.join(HERE, "backtest.json.tmp"), os.path.join(HERE, "backtest.json"))
