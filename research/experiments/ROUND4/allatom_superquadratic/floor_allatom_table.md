## Floor, MO overheads, generous G, one GPU as classical comparator

| folder | solvent | atoms | G (Toffoli/step) | c (s/step, hw) | t_T | B*_2 / T*_Q,2 | B*_3 / T*_Q,3 | B*_4 / T*_Q,4 | T*_Q,exp |
|---|---|---|---|---|---|---|---|---|---|
| Trp-cage | explicit | 4.83e+03 | 1.1e+10 | 9.3e-05 | 1000 ns | 1.4e+18 / 4.2e+06 yr | 4.1e+13 / 1.2e+02 yr | 1.3e+12 / 3.7 yr | 1.3 d |
| Trp-cage | explicit | 4.83e+03 | 1.1e+10 | 9.3e-05 | 100 ns | 1.4e+16 / 4.2e+04 yr | 1.3e+12 / 3.8 yr | 5.9e+10 / 63 d | 3.1 h |
| Trp-cage | explicit | 4.83e+03 | 1.1e+10 | 9.3e-05 | 10 ns | 1.4e+14 / 4.2e+02 yr | 4.1e+10 / 44 d | 2.7e+09 / 2.9 d | 1.1e+03 s |
| Trp-cage (GBn2) | implicit | 304 | 1.1e+09 | 0.00017 | 1000 ns | 4.1e+15 / 2.2e+04 yr | 5.1e+11 / 2.8 yr | 2.6e+10 / 51 d | 3.1 h |
| Trp-cage (GBn2) | implicit | 304 | 1.1e+09 | 0.00017 | 100 ns | 4.1e+13 / 2.2e+02 yr | 1.6e+10 / 32 d | 1.2e+09 / 2.4 d | 1.1e+03 s |
| Trp-cage (GBn2) | implicit | 304 | 1.1e+09 | 0.00017 | 10 ns | 4.1e+11 / 2.2 yr | 5.1e+08 / 1 d | 5.5e+07 / 2.6 h | 1.1e+02 s |
| villin HP35 / Fip35 WW (~10 us folders) | explicit | 7.86e+03 | 1.8e+10 | 0.00015 | 1000 ns | 1.4e+18 / 6.9e+06 yr | 4.1e+13 / 2e+02 yr | 1.3e+12 / 6.2 yr | 2.1 d |
| villin HP35 / Fip35 WW (~10 us folders) | explicit | 7.86e+03 | 1.8e+10 | 0.00015 | 100 ns | 1.4e+16 / 6.9e+04 yr | 1.3e+12 / 6.3 yr | 5.9e+10 / 1e+02 d | 5.1 h |
| villin HP35 / Fip35 WW (~10 us folders) | explicit | 7.86e+03 | 1.8e+10 | 0.00015 | 10 ns | 1.4e+14 / 6.9e+02 yr | 4.1e+10 / 73 d | 2.7e+09 / 4.9 d | 1.8e+03 s |
| NTL9(1-39) (GB, water-like friction) | implicit | 604 | 4.4e+09 | 0.00017 | 1000 ns | 6.4e+16 / 3.5e+05 yr | 4.0e+12 / 22 yr | 1.6e+11 / 3.2e+02 d | 12 h |
| NTL9(1-39) (GB, water-like friction) | implicit | 604 | 4.4e+09 | 0.00017 | 100 ns | 6.4e+14 / 3.5e+03 yr | 1.3e+11 / 2.5e+02 d | 7.4e+09 / 15 d | 1.2 h |
| NTL9(1-39) (GB, water-like friction) | implicit | 604 | 4.4e+09 | 0.00017 | 10 ns | 6.4e+12 / 35 yr | 4.0e+09 / 8 d | 3.4e+08 / 17 h | 4.4e+02 s |
| protein G B1 (GB, low friction) | implicit | 855 | 8.8e+09 | 0.00017 | 1000 ns | 2.6e+17 / 1.4e+06 yr | 1.1e+13 / 63 yr | 4.0e+11 / 2.2 yr | 1 d |
| protein G B1 (GB, low friction) | implicit | 855 | 8.8e+09 | 0.00017 | 100 ns | 2.6e+15 / 1.4e+04 yr | 3.6e+11 / 2 yr | 1.9e+10 / 38 d | 2.4 h |
| protein G B1 (GB, low friction) | implicit | 855 | 8.8e+09 | 0.00017 | 10 ns | 2.6e+13 / 1.4e+02 yr | 1.1e+10 / 23 d | 8.7e+08 / 1.7 d | 8.8e+02 s |
| protein G B1 (explicit) | explicit | 1.09e+04 | 2.6e+10 | 0.00021 | 1000 ns | 1.5e+18 / 9.9e+06 yr | 4.3e+13 / 2.8e+02 yr | 1.3e+12 / 8.7 yr | 3 d |
| protein G B1 (explicit) | explicit | 1.09e+04 | 2.6e+10 | 0.00021 | 100 ns | 1.5e+16 / 9.9e+04 yr | 1.4e+12 / 9 yr | 6.1e+10 / 1.5e+02 d | 7.1 h |
| protein G B1 (explicit) | explicit | 1.09e+04 | 2.6e+10 | 0.00021 | 10 ns | 1.5e+14 / 9.9e+02 yr | 4.3e+10 / 1e+02 d | 2.8e+09 / 6.8 d | 2.6e+03 s |
| ubiquitin (explicit, ms folder) | explicit | 1.72e+04 | 4.1e+10 | 0.00038 | 1000 ns | 1.2e+18 / 1.4e+07 yr | 3.6e+13 / 4.3e+02 yr | 1.1e+12 / 13 yr | 4.7 d |
| ubiquitin (explicit, ms folder) | explicit | 1.72e+04 | 4.1e+10 | 0.00038 | 100 ns | 1.2e+16 / 1.4e+05 yr | 1.1e+12 / 13 yr | 5.2e+10 / 2.3e+02 d | 11 h |
| ubiquitin (explicit, ms folder) | explicit | 1.72e+04 | 4.1e+10 | 0.00038 | 10 ns | 1.2e+14 / 1.4e+03 yr | 3.6e+10 / 1.6e+02 d | 2.4e+09 / 10 d | 1.1 h |
| lambda 6-85 (explicit, MSM) | explicit | 1.67e+04 | 3.9e+10 | 0.00035 | 1000 ns | 1.2e+18 / 1.4e+07 yr | 3.7e+13 / 4.1e+02 yr | 1.2e+12 / 13 yr | 4.5 d |
| lambda 6-85 (explicit, MSM) | explicit | 1.67e+04 | 3.9e+10 | 0.00035 | 100 ns | 1.2e+16 / 1.4e+05 yr | 1.2e+12 / 13 yr | 5.4e+10 / 2.2e+02 d | 11 h |
| lambda 6-85 (explicit, MSM) | explicit | 1.67e+04 | 3.9e+10 | 0.00035 | 10 ns | 1.2e+14 / 1.4e+03 yr | 3.7e+10 / 1.5e+02 d | 2.5e+09 / 10 d | 1.1 h |

## Against the literature classical twin (MO, generous G, 1 GPU)

| folder | twin (classical cost B_c, MD steps) | T_c on 1 GPU | t_T | s=2: T_Q (wins?) | s=3: T_Q (wins?) | s=4: T_Q (wins?) |
|---|---|---|---|---|---|---|
| Trp-cage | plain MD, one folding event (tau_f 4.1 us [Voelz 2010 PMC text] / 2.5 fs) = 1.6e+09 | 1.8 d | 1000 ns | 1.4e+02 yr (no) | 4.1 yr (no) | 2.6e+02 d (no) |
| Trp-cage | bias-exchange metadynamics, full folding FES (8 replicas x 40 ns) [Piana & Laio 2007, PMID 17419610] = 1.6e+08 | 4.1 h | 1000 ns | 45 yr (no) | 1.9 yr (no) | 1.4e+02 d (no) |
| Trp-cage | plain MD, one folding event (tau_f 4.1 us [Voelz 2010 PMC text] / 2.5 fs) = 1.6e+09 | 1.8 d | 10 ns | 1.4 yr (no) | 15 d (no) | 2.6 d (no) |
| Trp-cage | bias-exchange metadynamics, full folding FES (8 replicas x 40 ns) [Piana & Laio 2007, PMID 17419610] = 1.6e+08 | 4.1 h | 10 ns | 1.6e+02 d (no) | 7 d (no) | 1.4 d (no) |
| Trp-cage (GBn2) | plain MD, one folding event (implicit) = 2.0e+09 | 4.1 d | 1000 ns | 16 yr (no) | 1.6e+02 d (no) | 27 d (no) |
| Trp-cage (GBn2) | plain MD, one folding event (implicit) = 2.0e+09 | 4.1 d | 10 ns | 58 d (no) | 1.6 d (yes) | 6.5 h (yes) |
| villin HP35 / Fip35 WW (~10 us folders) | plain MD, one folding event (villin ~10 us, Fip35 ~13 us [Voelz 2010 PMC text]) = 4.0e+09 | 7.1 d | 1000 ns | 3.7e+02 yr (no) | 9.2 yr (no) | 1.5 yr (no) |
| villin HP35 / Fip35 WW (~10 us folders) | plain MD, one folding event (villin ~10 us, Fip35 ~13 us [Voelz 2010 PMC text]) = 4.0e+09 | 7.1 d | 10 ns | 3.7 yr (no) | 34 d (no) | 5.3 d (yes) |
| NTL9(1-39) (GB, water-like friction) | weighted ensemble, rate to ~1 decade (252 us aggregate) [Adhikari 2019 Table 1, PMC6660137] = 1.3e+11 | 2.5e+02 d | 1000 ns | 4.9e+02 yr (no) | 6.9 yr (no) | 3e+02 d (no) |
| NTL9(1-39) (GB, water-like friction) | plain MD, one folding event (tau_f 0.2-2 ms; 1 ms) = 5.0e+11 | 2.7 yr | 1000 ns | 9.8e+02 yr (no) | 11 yr (no) | 1.2 yr (yes) |
| NTL9(1-39) (GB, water-like friction) | weighted ensemble, rate to ~1 decade (252 us aggregate) [Adhikari 2019 Table 1, PMC6660137] = 1.3e+11 | 2.5e+02 d | 10 ns | 4.9 yr (no) | 25 d (yes) | 3 d (yes) |
| NTL9(1-39) (GB, water-like friction) | plain MD, one folding event (tau_f 0.2-2 ms; 1 ms) = 5.0e+11 | 2.7 yr | 10 ns | 9.8 yr (no) | 40 d (yes) | 4.2 d (yes) |
| protein G B1 (GB, low friction) | weighted ensemble, rate to ~2 decades (225 us aggregate) [Adhikari 2019 Table 1] = 1.1e+11 | 2.2e+02 d | 1000 ns | 9.3e+02 yr (no) | 13 yr (no) | 1.6 yr (no) |
| protein G B1 (GB, low friction) | plain MD, one folding event (tau_f >= 3 ms) = 1.5e+12 | 8.2 yr | 1000 ns | 3.4e+03 yr (no) | 32 yr (no) | 3.1 yr (yes) |
| protein G B1 (GB, low friction) | weighted ensemble, rate to ~2 decades (225 us aggregate) [Adhikari 2019 Table 1] = 1.1e+11 | 2.2e+02 d | 10 ns | 9.3 yr (no) | 49 d (yes) | 5.9 d (yes) |
| protein G B1 (GB, low friction) | plain MD, one folding event (tau_f >= 3 ms) = 1.5e+12 | 8.2 yr | 10 ns | 34 yr (no) | 1.2e+02 d (yes) | 11 d (yes) |
| protein G B1 (explicit) | distributed MD + MSM, ~65 us folding time for ~500 us aggregate [Ensign & Pande via Adhikari 2019 text] = 2.0e+11 | 1.3 yr | 1000 ns | 3.6e+03 yr (no) | 47 yr (no) | 5.4 yr (no) |
| protein G B1 (explicit) | distributed MD + MSM, ~65 us folding time for ~500 us aggregate [Ensign & Pande via Adhikari 2019 text] = 2.0e+11 | 1.3 yr | 10 ns | 36 yr (no) | 1.7e+02 d (yes) | 20 d (yes) |
| ubiquitin (explicit, ms folder) | plain MD, one folding event (ms folder [Piana 2013, PMID 23503848]) = 4.0e+11 | 4.8 yr | 1000 ns | 8.2e+03 yr (no) | 95 yr (no) | 10 yr (no) |
| ubiquitin (explicit, ms folder) | plain MD, one folding event (ms folder [Piana 2013, PMID 23503848]) = 4.0e+11 | 4.8 yr | 10 ns | 82 yr (no) | 3.5e+02 d (yes) | 38 d (yes) |
| lambda 6-85 (explicit, MSM) | MSM from 3,265 trajectories, 1.3 ms aggregate, 10 ms-timescale model [Bowman 2011, PMC3043158] = 5.2e+11 | 5.8 yr | 1000 ns | 8.9e+03 yr (no) | 1e+02 yr (no) | 11 yr (no) |
| lambda 6-85 (explicit, MSM) | MSM from 3,265 trajectories, 1.3 ms aggregate, 10 ms-timescale model [Bowman 2011, PMC3043158] = 5.2e+11 | 5.8 yr | 10 ns | 89 yr (no) | 3.6e+02 d (yes) | 38 d (yes) |

## Sensitivity at t_T = 10 ns (central G, CPU-core / Anton comparators, CE overheads)

| folder | G level | hw | overheads | t_T | T*_Q,2 | T*_Q,3 | T*_Q,4 |
|---|---|---|---|---|---|---|---|
| Trp-cage | gen | cpu1 | MO | 10 ns | 2.1 yr | 3.1 d | 12 h |
| Trp-cage | gen | anton | MO | 10 ns | 2e+04 yr | 3e+02 d | 11 d |
| Trp-cage | cen | gpu | MO | 10 ns | 6.9e+04 yr | 5.6 yr | 88 d |
| Trp-cage | cen | gpu | CE | 10 ns | 2.8e+07 yr | 5e+02 yr | 13 yr |
| Trp-cage | cen | cpu1 | MO | 10 ns | 3.4e+02 yr | 1.4e+02 d | 15 d |
| Trp-cage | cen | cpu1 | CE | 10 ns | 1.4e+05 yr | 35 yr | 2.2 yr |
| Trp-cage | cen | anton | MO | 10 ns | 3.2e+06 yr | 38 yr | 3.2e+02 d |
| Trp-cage | cen | anton | CE | 10 ns | 1.3e+09 yr | 3.4e+03 yr | 47 yr |
| Trp-cage (GBn2) | gen | cpu1 | MO | 10 ns | 9.5 d | 2.6 h | 2.2e+03 s |
| Trp-cage (GBn2) | cen | gpu | MO | 10 ns | 36 yr | 8.2 d | 17 h |
| Trp-cage (GBn2) | cen | gpu | CE | 10 ns | 1.4e+04 yr | 2 yr | 38 d |
| Trp-cage (GBn2) | cen | cpu1 | MO | 10 ns | 1.5e+02 d | 21 h | 3.8 h |
| Trp-cage (GBn2) | cen | cpu1 | CE | 10 ns | 1.7e+02 yr | 79 d | 8.6 d |
| villin HP35 / Fip35 WW (~10 us folders) | gen | cpu1 | MO | 10 ns | 3.5 yr | 5.2 d | 20 h |
| villin HP35 / Fip35 WW (~10 us folders) | gen | anton | MO | 10 ns | 5.3e+04 yr | 1.8 yr | 21 d |
| villin HP35 / Fip35 WW (~10 us folders) | cen | gpu | MO | 10 ns | 1.1e+05 yr | 9.2 yr | 1.5e+02 d |
| villin HP35 / Fip35 WW (~10 us folders) | cen | gpu | CE | 10 ns | 4.5e+07 yr | 8.2e+02 yr | 22 yr |
| villin HP35 / Fip35 WW (~10 us folders) | cen | cpu1 | MO | 10 ns | 5.7e+02 yr | 2.4e+02 d | 25 d |
| villin HP35 / Fip35 WW (~10 us folders) | cen | cpu1 | CE | 10 ns | 2.3e+05 yr | 58 yr | 3.7 yr |
| villin HP35 / Fip35 WW (~10 us folders) | cen | anton | MO | 10 ns | 8.8e+06 yr | 81 yr | 1.7 yr |
| villin HP35 / Fip35 WW (~10 us folders) | cen | anton | CE | 10 ns | 3.5e+09 yr | 7.2e+03 yr | 92 yr |
| NTL9(1-39) (GB, water-like friction) | gen | cpu1 | MO | 10 ns | 35 d | 10 h | 2.3 h |
| NTL9(1-39) (GB, water-like friction) | cen | gpu | MO | 10 ns | 5.6e+02 yr | 64 d | 4.4 d |
| NTL9(1-39) (GB, water-like friction) | cen | gpu | CE | 10 ns | 2.2e+05 yr | 16 yr | 2.4e+02 d |
| NTL9(1-39) (GB, water-like friction) | cen | cpu1 | MO | 10 ns | 1.5 yr | 3.4 d | 15 h |
| NTL9(1-39) (GB, water-like friction) | cen | cpu1 | CE | 10 ns | 6.2e+02 yr | 3e+02 d | 33 d |
| protein G B1 (GB, low friction) | gen | cpu1 | MO | 10 ns | 68 d | 20 h | 4.6 h |
| protein G B1 (GB, low friction) | cen | gpu | MO | 10 ns | 2.3e+03 yr | 1.8e+02 d | 11 d |
| protein G B1 (GB, low friction) | cen | gpu | CE | 10 ns | 9e+05 yr | 45 yr | 1.6 yr |
| protein G B1 (GB, low friction) | cen | cpu1 | MO | 10 ns | 3 yr | 6.6 d | 1.2 d |
| protein G B1 (GB, low friction) | cen | cpu1 | CE | 10 ns | 1.2e+03 yr | 1.6 yr | 66 d |
| protein G B1 (explicit) | gen | cpu1 | MO | 10 ns | 5 yr | 7.3 d | 1.2 d |
| protein G B1 (explicit) | gen | anton | MO | 10 ns | 1e+05 yr | 2.9 yr | 32 d |
| protein G B1 (explicit) | cen | gpu | MO | 10 ns | 1.6e+05 yr | 13 yr | 2e+02 d |
| protein G B1 (explicit) | cen | gpu | CE | 10 ns | 6.5e+07 yr | 1.2e+03 yr | 30 yr |
| protein G B1 (explicit) | cen | cpu1 | MO | 10 ns | 8.2e+02 yr | 3.4e+02 d | 35 d |
| protein G B1 (explicit) | cen | cpu1 | CE | 10 ns | 3.3e+05 yr | 82 yr | 5.2 yr |
| protein G B1 (explicit) | cen | anton | MO | 10 ns | 1.7e+07 yr | 1.3e+02 yr | 2.6 yr |
| protein G B1 (explicit) | cen | anton | CE | 10 ns | 6.8e+09 yr | 1.2e+04 yr | 1.4e+02 yr |
| ubiquitin (explicit, ms folder) | gen | cpu1 | MO | 10 ns | 7 yr | 11 d | 1.8 d |
| ubiquitin (explicit, ms folder) | gen | anton | MO | 10 ns | 2.6e+05 yr | 5.9 yr | 60 d |
| ubiquitin (explicit, ms folder) | cen | gpu | MO | 10 ns | 2.3e+05 yr | 20 yr | 3.1e+02 d |
| ubiquitin (explicit, ms folder) | cen | gpu | CE | 10 ns | 9.2e+07 yr | 1.7e+03 yr | 47 yr |
| ubiquitin (explicit, ms folder) | cen | cpu1 | MO | 10 ns | 1.2e+03 yr | 1.4 yr | 54 d |
| ubiquitin (explicit, ms folder) | cen | cpu1 | CE | 10 ns | 4.6e+05 yr | 1.2e+02 yr | 8 yr |
| ubiquitin (explicit, ms folder) | cen | anton | MO | 10 ns | 4.3e+07 yr | 2.7e+02 yr | 4.9 yr |
| ubiquitin (explicit, ms folder) | cen | anton | CE | 10 ns | 1.7e+10 yr | 2.4e+04 yr | 2.7e+02 yr |
| lambda 6-85 (explicit, MSM) | gen | cpu1 | MO | 10 ns | 6.9 yr | 11 d | 1.7 d |
| lambda 6-85 (explicit, MSM) | gen | anton | MO | 10 ns | 2.4e+05 yr | 5.5 yr | 57 d |
| lambda 6-85 (explicit, MSM) | cen | gpu | MO | 10 ns | 2.3e+05 yr | 19 yr | 3e+02 d |
| lambda 6-85 (explicit, MSM) | cen | gpu | CE | 10 ns | 9e+07 yr | 1.7e+03 yr | 45 yr |
| lambda 6-85 (explicit, MSM) | cen | cpu1 | MO | 10 ns | 1.1e+03 yr | 1.3 yr | 52 d |
| lambda 6-85 (explicit, MSM) | cen | cpu1 | CE | 10 ns | 4.5e+05 yr | 1.2e+02 yr | 7.7 yr |
| lambda 6-85 (explicit, MSM) | cen | anton | MO | 10 ns | 4e+07 yr | 2.5e+02 yr | 4.6 yr |
| lambda 6-85 (explicit, MSM) | cen | anton | CE | 10 ns | 1.6e+10 yr | 2.2e+04 yr | 2.5e+02 yr |
