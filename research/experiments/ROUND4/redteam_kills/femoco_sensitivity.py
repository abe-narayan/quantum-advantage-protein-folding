"""ROUND4 red team, RT-D: what would the FeMoco E-state WEAK residue need, in the lane's OWN decision model?

Uses the closed form of ROUND3/new_mechanisms_intrinsic (decision_value.py, README section 3), unchanged:
  max over gap Delta of [Phi(Delta/a) - Phi(Delta/b)], a = sigma_m (model floor), b = sqrt(sigma_s^2 + sigma_m^2)
  (sigma_s = best-classical solver error; an exact QPE solver sets sigma_s = 0).  Multiply by the lever dq (A).
Red-team questions:
  (1) Which model floor sigma_m makes an exact solver worth >= 0.3 A (and >= 0.5 A) on the 0.8-1.5 A E4 lever, for
      sigma_best = 3, 5, 8 kcal/mol?  (The WEAK verdict used sigma_m ~ 1-4 kcal/mol, INFERENCE.)
  (2) Cost per question at 76 / 100 / 150 orbitals with the lane's fitted Toffoli ~ N^2.35 scaling (8.6 h at 76o,
      LITERATURE-SUPPORTED anchor) for the lane's minimal (30) and central (300) energy counts.
Seconds of CPU.  Output: femoco_sensitivity.json
"""
import json
import math
import os

import numpy as np
from scipy.optimize import brentq
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))


def max_gain(sm, ss):
    a, b = sm, math.sqrt(ss * ss + sm * sm)
    if ss <= 0:
        return 0.0
    d = a * b * math.sqrt(2 * math.log(b / a) / (b * b - a * a))
    return float(norm.cdf(d / a) - norm.cdf(d / b))


def main():
    out = dict(check_table={}, sigma_m_needed={}, cost_days={})
    for r in (0.25, 0.5, 1, 2, 5):                      # reproduce the lane's table (0.7/2.7/8.3/18.5/32.6 %)
        out["check_table"][str(r)] = round(100 * max_gain(1.0, r), 1)
    for sb in (3.0, 5.0, 8.0):
        for dq in (0.8, 1.0, 1.5):
            for target in (0.3, 0.5):
                need = target / dq
                if max_gain(1e-3, sb) < need:
                    out["sigma_m_needed"][f"sb={sb}|dq={dq}|VOI>={target}A"] = None
                    continue
                sm = brentq(lambda s: max_gain(s, sb) - need, 1e-3, 50.0)
                out["sigma_m_needed"][f"sb={sb}|dq={dq}|VOI>={target}A"] = round(sm, 3)
    for norb in (76, 100, 150):
        h = 8.6 * (norb / 76.0) ** 2.35
        for ne in (30, 300, 5000):
            out["cost_days"][f"{norb}o|{ne}E"] = round(h * ne / 24.0, 1)
    tmp = os.path.join(HERE, "femoco_sensitivity.json.tmp")
    json.dump(out, open(tmp, "w"), indent=1)
    os.replace(tmp, os.path.join(HERE, "femoco_sensitivity.json"))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
