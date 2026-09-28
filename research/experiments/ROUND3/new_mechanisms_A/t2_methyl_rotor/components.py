"""Size of strongly coupled methyl clusters in 1UBQ (connected components of the methyl contact graph)
at several H..H thresholds: sets the classical exact-diagonalisation burden (17^n per sector at M=24)."""
import json, os, sys
import numpy as np
import networkx as nx
sys.path.insert(0, os.path.dirname(__file__))
from rotor import load_methyls, atomic_json
ms = load_methyls()
D = np.array([[np.linalg.norm(a["H"][:, None] - b["H"][None], axis=-1).min() if i != j else 99
               for j, b in enumerate(ms)] for i, a in enumerate(ms)])
out = {"n_methyls": len(ms)}
for thr in (2.0, 2.2, 2.4, 2.6, 3.0):
    g = nx.Graph(); g.add_nodes_from(range(len(ms)))
    g.add_edges_from([(i, j) for i in range(len(ms)) for j in range(i + 1, len(ms)) if D[i, j] < thr])
    comps = sorted((len(c) for c in nx.connected_components(g)), reverse=True)
    out[f"HH_lt_{thr}"] = {"n_edges": g.number_of_edges(), "largest_components": comps[:6],
                           "log10_sector_dim_largest_M24": float(comps[0] * np.log10(17))}
atomic_json(os.path.join(os.path.dirname(os.path.abspath(__file__)), "components.json"), out)
print(json.dumps(out, indent=1))
