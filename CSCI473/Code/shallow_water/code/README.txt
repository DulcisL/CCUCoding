./sw2d \
  --rows 200 \
  --cols 200 \
  --steps 2000 \
  --dx 1.0 \
  --dy 1.0 \
  --dt 1 \
  --g 9.81 \
  --H0 1.0 \
  --cfl .4 \
  --height .5 \
  --save-interval 100 \
  --stats-interval 100

To sweep across multiple grid sizes and capture read/compute/write timings using the shared timer,
run the helper script from this directory, for example:

python3 sweep_sw2d.py \
  --rows 100:300:100 \
  --cols 100:300:100 \
  --steps 1000,2000 \
  --save-interval 50 \
  --repeat 2 \
  --out-dir sw2d_sweep_results \
  --csv sweeps.csv

To benchmark the pthread solver across rows/cols/steps/thread counts (and produce runtime/speedup/efficiency/
iso-efficiency plots), run sweep_sw2d_pthread.py. Example:

python3 sweep_sw2d_pthread.py \
  --rows 1000:1500:2000 \
  --cols 1000 \
  --steps 2000 \
  --threads 1,2,4,8,10,12,14,16,18,20 \
  --save-interval 100 \
  --repeat 5 \
  --out-dir sw2d_pthread_sweep \
  --keep-movies

To benchmark the OpenMP solver, use sweep_sw2d_omp.py (same CLI as the pthread version). Example:

python3 sweep_sw2d_omp.py \
  --rows 1000:1500:2000 \
  --cols 1000 \
  --steps 2000 \
  --threads 1,2,4,8,10,12,14,16,18,20 \
  --save-interval 100 \
  --repeat 5 \
  --out-dir sw2d_omp_sweep \
  --keep-movies

To run the pthread-parallel solver, build sw2d_pthread (see sw2d_pthread.c for compile flags) and call it
with the same options plus `--threads` to set the worker count, for example:

./sw2d_pthread \
  --rows 400 \
  --cols 400 \
  --steps 5000 \
  --threads 8 \
  --save-interval 100 \
  --out movie_p.bin

To run the OpenMP solver (sw2d_omp), build it via the Makefile and invoke similarly with `--threads`:

./sw2d_omp \
  --rows 400 \
  --cols 400 \
  --steps 5000 \
  --threads 8 \
  --save-interval 100 \
  --out movie_omp.bin
