"""Director cross-check: echo (F) and transfer (S) bias of each sparse-Pauli eps rung
against the in-file sector-exact reference, for every C2/C3 file (finished or .partial).
Read-only on RAW. Timings are wall-clock seconds recorded by nmr_sparse_scaling.py under
the governor (jobs are suspended/resumed), so they are indicative, not CPU time.
Usage (repo root): OMP_NUM_THREADS=1 python research/experiments/ADVERSARIAL/R1_director/c2_echo_check.py
"""
import glob, json, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))

def arr(x):
    if isinstance(x, dict):
        return np.array([x[k] for k in sorted(x, key=int)], float).T
    return np.array(x, float).reshape(len(x), -1)

out = []
for f in sorted(glob.glob('research/results/RAW/nmr_sparse/*.json*')):
    if f.endswith('.running'):
        continue
    d = json.load(open(f))
    ex = d.get('exact') or {}
    rec = {'file': os.path.basename(f), 'N': d['N'], 'gamma': d['gamma'], 'probe': d['probe'],
           'pdb': d['pdb'], 'sym_space_4N_over_4': 4 ** d['N'] // 4,
           'exact_wall_s': ex.get('secs'), 'runs': []}
    have_F = ex.get('F') is not None
    if ex.get('S') is not None:
        Se = arr(ex['S']); Fe = arr(ex['F']) if have_F else None
    for r in d.get('runs', []):
        rr = {'eps': r['eps'], 'peak_strings': r['peak_strings'], 'wall_s': r['secs'],
              'capped': r.get('capped')}
        rr['frac_sym_space'] = r['peak_strings'] / rec['sym_space_4N_over_4']
        if ex.get('S') is not None and r.get('S') is not None:
            S = arr(r['S']); n = min(len(S), len(Se))
            bS = np.abs(S[:n] - Se[:n]).max(1)
            rr['tcS_index'] = next((i for i, b in enumerate(bS) if b > d['sigma']), None)
            rr['max_bias_S'] = float(bS.max())
        if have_F and r.get('F') is not None:
            F = arr(r['F']); n = min(len(F), len(Fe))
            bF = np.abs(F[:n] - Fe[:n]).max(1)
            rr['tcF_index'] = next((i for i, b in enumerate(bF) if b > d['sigma']), None)
            rr['tcF_us'] = None if rr['tcF_index'] is None else round(d['times'][rr['tcF_index']] * 1e6) if 'times' in d else rr['tcF_index'] * 20
            rr['max_bias_F'] = float(bF.max())
        rec['runs'].append(rr)
    out.append(rec)

json.dump(out, open(os.path.join(HERE, 'c2_echo_check.json'), 'w'), indent=1)
for rec in out:
    print(rec['file'], 'exact_wall_s', rec['exact_wall_s'])
    for rr in rec['runs']:
        print('   eps %.0e peak %8d (%.3f of 4^N/4) wall %6.0f s  tcS %s tcF %s maxbF %s' % (
            rr['eps'], rr['peak_strings'], rr['frac_sym_space'], rr['wall_s'], rr.get('tcS_index'),
            rr.get('tcF_index'), None if 'max_bias_F' not in rr else round(rr['max_bias_F'], 4)))
