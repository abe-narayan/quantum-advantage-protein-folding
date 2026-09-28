"""ROUND4 director cross-check (reads verifier JSONs only; no dynamics; < 1 CPU-s).

For each of the 8 (probe, site) series at t = 40/80/120 us, collect every
b-aware (cluster contains b's dominant partners) classical estimate of the
secular echo F_ab produced in round 4 by independent lanes/verifiers:

  SA2   tx_early/verify_classical   probe ranks + 2 strongest b-partners, largest N
  SA4   tx_early/verify_classical   probe ranks + 4 b-partners, N = 20 (40 us only)
  PB20  tx_early/verify_classical   ROUND3 pairb, N = 20 (p19 b8, p245 b7 only)
  FEPB  spindmft/verify_classical   {a,b} u nearest-to-either, fastecho kernel, largest N
  PP    spindmft/verify_resource    {a,b} u nearest-to-either, P+ sector kernel, largest N
  E1    spindmft lane               probe F18 + sr-spinDMFT bath correction (thermodynamic)
  E2    spindmft/verify_classical   b-aware exact + CSD-bath correction (thermodynamic)
  DMFT  spindmft lane               spinDMFT value used by verify_resource (b-aware pred or F_corr)

Reports the spread (max - min) over available estimates, and the probe-family
value and round-3 hybrid for reference.  sigma = 0.01.
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
R4 = os.path.dirname(HERE)
SIG = 0.01

txc = json.load(open(os.path.join(R4, 'tx_early/verify_classical/verify_summary.json')))
spr = json.load(open(os.path.join(R4, 'spindmft/verify_resource/verify_summary.json')))
spc = json.load(open(os.path.join(R4, 'spindmft/verify_classical/verify_summary.json')))

series = ['p19_b1', 'p19_b7', 'p19_b8', 'p19_b9', 'p245_b1', 'p245_b7', 'p245_b8', 'p245_b9']
out = {'sigma': SIG, 'cells': {}, 'summary': {}}
ti = {40: 0, 80: 1, 120: 2}

rows_spr = {(r['probe'], r['site'], r['t_us']): r for r in spr['table']}
e12 = {}
for t in ('40', '80', '120'):
    for r in spc['E1_vs_E2'].get(t, []):
        e12[(r['probe'], r['site'], int(t))] = r

for t in (40, 80, 120):
    n_le_sig = 0; n_cells = 0; spreads = []
    for s in series:
        probe = int(s.split('_')[0][1:]); site = int(s.split('_b')[1])
        est = {}
        tx = txc['series'][s]['t'].get(str(t), {})
        if tx.get('SA_best') is not None: est['SA2'] = tx['SA_best']
        if tx.get('SA4_20') is not None: est['SA4'] = tx['SA4_20']
        if tx.get('pairb_20') is not None: est['PB20'] = tx['pairb_20']
        fe = spc['baware_exact_independent'].get(s, {})
        if fe:
            nmax = max(int(k) for k in fe if k.isdigit())
            est['FEPB'] = fe[str(nmax)]['F'][ti[t]]
        r = rows_spr.get((probe, site, t))
        if r and r.get('Fb_best') is not None: est['PP'] = r['Fb_best']
        ref = None
        if r:
            ref = r.get('spinDMFT_baware_pred') if r.get('spinDMFT_baware_pred') is not None else r.get('Fcorr_spinDMFT')
            if ref is not None: est['DMFT'] = ref
        e = e12.get((probe, site, t))
        if e:
            est['E2'] = e['E2']; est['E1'] = e['E1_lane_Fcorr']
        vals = list(est.values())
        spread = max(vals) - min(vals) if len(vals) > 1 else None
        exact_only = [est[k] for k in ('SA2', 'SA4', 'PB20', 'FEPB', 'PP') if k in est]
        spread_exact = max(exact_only) - min(exact_only) if len(exact_only) > 1 else None
        probe_fam = tx.get('probe_best')
        hyb = r.get('F_hybrid') if r else None
        cell = {'estimates': est, 'spread_all': spread, 'spread_exact_baware': spread_exact,
                'probe_family_best': probe_fam, 'hybrid_R3': hyb,
                'probe_minus_median_baware': (probe_fam - sorted(vals)[len(vals)//2]) if (probe_fam is not None and vals) else None}
        out['cells'][f'{s}_t{t}'] = cell
        if spread is not None:
            n_cells += 1; spreads.append(spread)
            if spread <= SIG: n_le_sig += 1
    out['summary'][str(t)] = {'n_series': n_cells, 'n_spread_le_sigma': n_le_sig,
                              'max_spread': max(spreads) if spreads else None,
                              'median_spread': sorted(spreads)[len(spreads)//2] if spreads else None}

json.dump(out, open(os.path.join(HERE, 'cross_family.json'), 'w'), indent=1)
for t in ('40', '80', '120'):
    print(t, out['summary'][t])
for k, v in out['cells'].items():
    e = v['estimates']
    print(k, {a: round(b, 4) for a, b in e.items()}, 'spread', None if v['spread_all'] is None else round(v['spread_all'], 4),
          'exact-spread', None if v['spread_exact_baware'] is None else round(v['spread_exact_baware'], 4),
          'probe', None if v['probe_family_best'] is None else round(v['probe_family_best'], 4))
