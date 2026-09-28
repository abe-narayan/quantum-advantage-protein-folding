#!/usr/bin/env bash
# World-ladder test (n_c = 10, probeb family): spinDMFT in closed worlds N = 14, 16, 20 (plus 18 and protein, already run)
# to test whether spinDMFT reproduces the EXACT N-dependence of F_N (cross-family check of its bath correction).
# Then b-aware clusters (pairb) for the three series whose butterfly site has most of its M2 outside the 18-cluster.
# Every python run is single-threaded, wall-bounded, and checkpointed (sr: per iteration; emb: per batch).
set -u
cd "$(dirname "$0")"
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
for p in 19 245; do
  for W in 14 16 20; do
    timeout 300 python run_sr.py --world $W --probe $p --M 4096 --iters 7 | tail -1
    timeout 900 python run_emb.py --probe $p --world $W --nc 10 --M 512 --batch 32 --seed 7 --budget 800 | tail -4
  done
done
for spec in "19 8" "19 9" "245 7"; do
  set -- $spec
  for W in protein 18; do
    timeout 900 python run_emb.py --probe $1 --world $W --nc 10 --family pairb:$2 --M 512 --batch 32 --seed 7 --budget 800 | tail -4
  done
done
