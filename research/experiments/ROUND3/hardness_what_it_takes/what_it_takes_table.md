## Required speedup exponent and hardware per L

| classical cost scenario | overheads | L | C_c (evals) | T_c | s=2 | s=3 | s=4 | exp(P=1) | exp(P=L) | min s at t_T >= 1 us and T_q <= 30 d |
|---|---|---|---|---|---|---|---|---|---|---|
| BEST-median | MO | 100 | 4.2e+02 | 0.76 s | 40 ps | 1.1e+02 ps | 1.8e+02 ps | 8.2e+02 ps | 8.2 ps | none |
| BEST-median | MO | 200 | 5.6e+02 | 4.6 s | 47 ps | 1.3e+02 ps | 2.3e+02 ps | 1.1 ns | 5.5 ps | none |
| BEST-median | MO | 300 | 8.4e+02 | 17 s | 58 ps | 1.8e+02 ps | 3.1e+02 ps | 1.7 ns | 5.6 ps | none |
| BEST-median | MO | 500 | 1.4e+03 | 86 s | 75 ps | 2.5e+02 ps | 4.6e+02 ps | 2.8 ns | 5.6 ps | none |
| BEST-median | CE | 100 | 4.2e+02 | 0.76 s | 6.0e-13 s | 1.6 ps | 2.7 ps | 12 ps | 1.2e-13 s | none |
| BEST-median | CE | 200 | 5.6e+02 | 4.6 s | 7.0e-13 s | 2 ps | 3.4 ps | 16 ps | 8.2e-14 s | none |
| BEST-median | CE | 300 | 8.4e+02 | 17 s | 8.6e-13 s | 2.6 ps | 4.6 ps | 25 ps | 8.3e-14 s | none |
| BEST-median | CE | 500 | 1.4e+03 | 86 s | 1.1 ps | 3.7 ps | 6.8 ps | 42 ps | 8.3e-14 s | none |
| BEST-worst | MO | 100 | 5.8e+04 | 1e+02 s | 4.7e+02 ps | 2.9 ns | 7.3 ns | 1.1e+02 ns | 1.1 ns | none |
| BEST-worst | MO | 200 | 1e+05 | 8.4e+02 s | 6.3e+02 ps | 4.3 ns | 11 ns | 2e+02 ns | 1 ns | none |
| BEST-worst | MO | 300 | 2.3e+05 | 1.3 h | 9.6e+02 ps | 7.5 ns | 21 ns | 4.6e+02 ns | 1.5 ns | none |
| BEST-worst | MO | 500 | 6.4e+05 | 11 h | 1.6 ns | 15 ns | 45 ns | 1.3 us | 2.6 ns | exp(P=1) |
| BEST-worst | CE | 100 | 5.8e+04 | 1e+02 s | 7 ps | 44 ps | 1.1e+02 ps | 1.7 ns | 17 ps | none |
| BEST-worst | CE | 200 | 1e+05 | 8.4e+02 s | 9.4 ps | 64 ps | 1.7e+02 ps | 3 ns | 15 ps | none |
| BEST-worst | CE | 300 | 2.3e+05 | 1.3 h | 14 ps | 1.1e+02 ps | 3.1e+02 ps | 6.8 ns | 23 ps | none |
| BEST-worst | CE | 500 | 6.4e+05 | 11 h | 24 ps | 2.2e+02 ps | 6.7e+02 ps | 19 ns | 38 ps | none |
| FOLD-ms | MO | 100 | 4.4e+02 | 0.8 s | 41 ps | 1.1e+02 ps | 1.9e+02 ps | 8.6e+02 ps | 8.6 ps | none |
| FOLD-ms | MO | 200 | 2.8e+04 | 2.3e+02 s | 3.3e+02 ps | 1.8 ns | 4.3 ns | 55 ns | 2.8e+02 ps | none |
| FOLD-ms | MO | 300 | 1.8e+06 | 9.8 h | 2.7 ns | 29 ns | 97 ns | 3.5 us | 12 ns | exp(P=1) |
| FOLD-ms | MO | 500 | 7.1e+09 | 5e+03 d | 1 ns | 44 ns | 2.9e+02 ns | 85 us | 1.7e+02 ns | exp(P=1) |
| FOLD-ms | CE | 100 | 4.4e+02 | 0.8 s | 6.1e-13 s | 1.7 ps | 2.8 ps | 13 ps | 1.3e-13 s | none |
| FOLD-ms | CE | 200 | 2.8e+04 | 2.3e+02 s | 4.9 ps | 27 ps | 64 ps | 8.2e+02 ps | 4.1 ps | none |
| FOLD-ms | CE | 300 | 1.8e+06 | 9.8 h | 39 ps | 4.3e+02 ps | 1.4 ns | 52 ns | 1.7e+02 ps | none |
| FOLD-ms | CE | 500 | 7.1e+09 | 5e+03 d | 15 ps | 6.6e+02 ps | 4.3 ns | 1.3 us | 2.5 ns | exp(P=1) |
| HYP-own | MO | 100 | 2.7e+04 | 49 s | 3.2e+02 ps | 1.8 ns | 4.1 ns | 53 ns | 5.3e+02 ps | none |
| HYP-own | MO | 200 | 1.7e+06 | 3.9 h | 2.6 ns | 28 ns | 93 ns | 3.4 us | 17 ns | exp(P=1) |
| HYP-own | MO | 300 | 1.1e+08 | 25 d | 21 ns | 4.5e+02 ns | 2.1 us | 2.1e+02 us | 7.2e+02 ns | s=4 |
| HYP-own | MO | 500 | 4.3e+11 | 3e+05 d | 1.3e+02 ps | 11 ns | 1.1e+02 ns | 85 us | 1.7e+02 ns | exp(P=1) |
| HYP-own | CE | 100 | 2.7e+04 | 49 s | 4.8 ps | 26 ps | 62 ps | 7.9e+02 ps | 7.9 ps | none |
| HYP-own | CE | 200 | 1.7e+06 | 3.9 h | 38 ps | 4.2e+02 ps | 1.4 ns | 50 ns | 2.5e+02 ps | none |
| HYP-own | CE | 300 | 1.1e+08 | 25 d | 3.1e+02 ps | 6.7 ns | 31 ns | 3.2 us | 11 ns | exp(P=1) |
| HYP-own | CE | 500 | 4.3e+11 | 3e+05 d | 1.9 ps | 1.7e+02 ps | 1.6 ns | 1.3 us | 2.5 ns | exp(P=1) |

Cells: required logical Toffoli time t_T = min(break-even, 30-day usefulness) for the given speedup; 'plausible' means >= 1 us.

## Landscape-independent floor generalised to exponent s (break-even classical cost B*_s and per-solution quantum wall-clock T*_Q,s)

| overheads | L | t_T | B*_2 | T*_Q (s=2) | B*_3 | T*_Q (s=3) | B*_4 | T*_Q (s=4) | T*_Q exp(P=1) |
|---|---|---|---|---|---|---|---|---|---|
| MO | 100 | 1 us | 2.6e+11 | 15 yr | 3.6e+08 | 7.6 d | 4.1e+07 | 21 h | 0.26 h |
| MO | 100 | 10 ns | 2.6e+07 | 13 h | 3.6e+05 | 0.18 h | 8.8e+04 | 0.044 h | 0.0026 h |
| MO | 200 | 1 us | 2.5e+11 | 67 yr | 3.6e+08 | 34 d | 4.0e+07 | 3.8 d | 1.2 h |
| MO | 200 | 10 ns | 2.5e+07 | 2.4 d | 3.6e+05 | 0.82 h | 8.7e+04 | 0.2 h | 0.012 h |
| MO | 300 | 1 us | 2.5e+11 | 1.6e+02 yr | 3.6e+08 | 82 d | 4.0e+07 | 9.2 d | 2.8 h |
| MO | 300 | 10 ns | 2.5e+07 | 5.8 d | 3.6e+05 | 2 h | 8.6e+04 | 0.48 h | 0.028 h |
| MO | 500 | 1 us | 2.5e+11 | 4.8e+02 yr | 3.5e+08 | 2.5e+02 d | 3.9e+07 | 28 d | 8.5 h |
| MO | 500 | 10 ns | 2.5e+07 | 18 d | 3.5e+05 | 6 h | 8.5e+04 | 1.4 h | 0.085 h |
| CE | 100 | 1 us | 1.2e+15 | 6.7e+04 yr | 2.0e+11 | 12 yr | 1.1e+10 | 2.3e+02 d | 17 h |
| CE | 100 | 10 ns | 1.2e+11 | 6.7 yr | 2.0e+08 | 4.2 d | 2.4e+07 | 12 h | 0.17 h |
| CE | 200 | 1 us | 1.2e+15 | 3e+05 yr | 2.0e+11 | 52 yr | 1.1e+10 | 2.9 yr | 3.2 d |
| CE | 200 | 10 ns | 1.2e+11 | 30 yr | 2.0e+08 | 19 d | 2.4e+07 | 2.3 d | 0.78 h |
| CE | 300 | 1 us | 1.1e+15 | 7.3e+05 yr | 2.0e+11 | 1.2e+02 yr | 1.1e+10 | 6.9 yr | 7.8 d |
| CE | 300 | 10 ns | 1.1e+11 | 73 yr | 2.0e+08 | 46 d | 2.4e+07 | 5.5 d | 1.9 h |
| CE | 500 | 1 us | 1.1e+15 | 2.2e+06 yr | 1.9e+11 | 3.8e+02 yr | 1.1e+10 | 21 yr | 24 d |
| CE | 500 | 10 ns | 1.1e+11 | 2.2e+02 yr | 1.9e+08 | 1.4e+02 d | 2.3e+07 | 17 d | 5.7 h |
