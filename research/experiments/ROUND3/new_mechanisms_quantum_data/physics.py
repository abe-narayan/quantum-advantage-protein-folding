"""Realism numbers for coherent quantum-data routes (transduction of protein 1H states into a quantum memory).
Pure arithmetic from physical constants plus MEASURED repo values; writes physics.json.  Seconds of CPU."""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
hbar, kB = 1.054571817e-34, 1.380649e-23
gH, ge = 2.6752218744e8, 1.76085963023e11           # rad s^-1 T^-1
mu0_4pi = 1e-7
NA = 6.02214076e23

out = {}
out["thermal_1H_polarisation"] = {f"{B}T_{T}K": math.tanh(hbar * gH * B / (2 * kB * T))
                                  for (B, T) in ((9.4, 298), (14.1, 298), (28.2, 298), (9.4, 100), (14.1, 100),
                                                 (6.7, 1.2))}
# NV electron - 1H secular dipolar coupling prefactor (Hz), angular factor (3cos^2-1) omitted (|.| <= 2)
cpl = {}
for r_nm in (2.0, 3.0, 4.0, 5.0):
    r = r_nm * 1e-9
    nu = mu0_4pi * ge * gH * hbar / r ** 3 / (2 * math.pi)
    cpl[f"{r_nm}nm"] = dict(nu_Hz=nu, transfer_time_us=1e6 / (2 * nu))
out["NV_1H_coupling"] = cpl
# repo MEASURED 1H network T2 (R1_physics_feasibility/README.md): protonated 8.0-10.8 us; amide-only sqrt(M2)/2pi 4.4-4.8 kHz
T2_prot = (8.0e-6, 10.8e-6)
T2_amide = tuple(1 / (2 * math.pi * f) for f in (4.8e3, 4.4e3))
out["protein_1H_T2_s"] = dict(protonated=T2_prot, amide_only=T2_amide,
                              source="research/experiments/ADVERSARIAL/R1_physics_feasibility/README.md (MEASURED)")
fid = {}
for r_nm in ("3.0nm", "5.0nm"):
    tt = cpl[r_nm]["transfer_time_us"] * 1e-6
    for lab, T2 in (("protonated", T2_prot[1]), ("amide_only", T2_amide[1])):
        fid[f"{r_nm}_{lab}"] = dict(t_over_T2=tt / T2, f_exponential=math.exp(-tt / T2),
                                    log10_f_gaussian=-(tt / T2) ** 2 / 2 / math.log(10))
out["per_spin_transfer_fidelity_estimate"] = fid
# non-secular (non-commuting) sensor-bath terms: amplitude ratio nu / D_NV ; error probability ~ ratio^2
D_NV = 2.87e9
out["NV_nonsecular_ratio"] = {k: dict(ratio=v["nu_Hz"] / D_NV, prob=(v["nu_Hz"] / D_NV) ** 2) for k, v in cpl.items()}
# copies available in an ensemble sample
out["molecules_in_1mg_ubiquitin"] = 1e-3 / 8565.0 * NA
# sigma-cone sizes (R1 theory lens, MEASURED at 40 us; INFERENCE >= 57 at 80 us)
out["sigma_cone_spins"] = {"40us": [16, 20], "80us_inference": 57}
# cone transfer fidelity needed: retain >= 50% of late-window QFI needs lambda >= 0.95 per spin (qd_fisher summary)
for Ns in (12, 20, 57):
    out[f"cone_{Ns}_spins_all_transferred_prob_at_f0.99"] = 0.99 ** Ns
json.dump(out, open(os.path.join(HERE, "physics.json"), "w"), indent=1)
print(json.dumps(out, indent=1))
