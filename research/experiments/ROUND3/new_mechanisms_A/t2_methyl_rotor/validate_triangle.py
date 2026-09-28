"""Validation of the 3-rotor Lanczos code: with V_ac = V_bc = 0 the exact 3-rotor splittings must equal
the pair (a,b) dressed splittings and the bare splitting of c."""
import json, os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(__file__))
import run_triangle as T
from rotor import load_methyls, v3_grid, single_sector, two_rotor_sector_energies, atomic_json
ms = {m["id"]: m for m in load_methyls()}
R = [ms[x] for x in ("ILE36:CG2", "ILE36:CD1", "LEU71:CD1")]
G, M, V3 = T.G, T.M, T.V3
vg = v3_grid(V3, G)
Vab = T.coupling(R[0], R[1])
Vtot = vg[:, None, None] + vg[None, :, None] + vg[None, None, :] + Vab[:, :, None]
E3 = {s: T.lowest3(R, Vtot, s)[0] for s in ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1))}
E2 = two_rotor_sector_energies(V3, V3, R[0]["B"], R[1]["B"], np.fft.fft2(Vab) / G ** 2, M, [(0, 0), (1, 0), (0, 1)])
bare_c = single_sector(R[2]["B"], M, 1, vg)[0][0] - single_sector(R[2]["B"], M, 0, vg)[0][0]
out = {"Delta_a_3rot": (E3[(1, 0, 0)] - E3[(0, 0, 0)]) * 1e3, "Delta_a_pair": (E2[(1, 0)] - E2[(0, 0)]) * 1e3,
       "Delta_b_3rot": (E3[(0, 1, 0)] - E3[(0, 0, 0)]) * 1e3, "Delta_b_pair": (E2[(0, 1)] - E2[(0, 0)]) * 1e3,
       "Delta_c_3rot": (E3[(0, 0, 1)] - E3[(0, 0, 0)]) * 1e3, "Delta_c_bare": bare_c * 1e3}
atomic_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "validate_triangle.json"), out)
print(json.dumps(out, indent=1))
