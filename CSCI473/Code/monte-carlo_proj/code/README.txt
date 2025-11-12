Sweep-Serial:
python3 ./sweep_mc_slab.py --exe ./mc_slab --C 0.5 --Cc 0.1 --H-min 0.5 --H-max 5.0 --H-step 0.25 --N 100000 --seed 42 --trace --trace-every 100 --make-convergence-plots

Movie:
python3 ./mc_slab_movie.py --thickness 1.0 --Sigma_t 0.5 --c 0.99 --N 600 --frames 300 --fps 30 --dpi 200 --fig-width 10 --fig-height 5 --out movie.mp4

Bench-Pthread:
python3 bench_mc_slab_pthread.py --exe ./mc_slab_pthread --C 0.5 --Cc 0.1 --H 5.0 --seed 12345 --n_start 100000 --n_max 66400000 --P_start 1 --P_step 1 --P_max 20 --trials 5 --warmup 1 --eff_targets 0.5,0.7,0.8 --results_dir perf_results_mc

Check-Pthread:
python3 check_mc_slab_consistency.py --serial ./mc_slab --parallel ./mc_slab_pthread --C 1.0 --Cc 0.3 --H 10.0 --seed 12345 --n_start 100000 --n_max 6400000 --Ps 1,2,4,8,16,20 --trials 5 --abs_threshold 0.005 --results_dir consistency_results_mc

Bench-OMP:
python3 bench_mc_slab_omp.py --exe ./mc_slab_pthread --C 0.5 --Cc 0.1 --H 5.0 --seed 12345 --n_start 100000 --n_max 66400000 --P_start 1 --P_step 1 --P_max 20 --trials 5 --warmup 1 --eff_targets 0.5,0.7,0.8 --results_dir perf_results_mc

Check-OMP:
python3 check_mc_slab_omp_consistency.py --serial ./mc_slab --parallel ./mc_slab_pthread --C 1.0 --Cc 0.3 --H 10.0 --seed 12345 --n_start 100000 --n_max 6400000 --Ps 1,2,4,8,16,20 --trials 5 --abs_threshold 0.005 --results_dir consistency_results_mc
