#!/bin/bash

#SBATCH --job-name=stencil_bench
#SBATCH --output=stencil_bench.%j.out
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=16G
#SBATCH --time=00:30:00
#SBATCH --account=ccu108
#SBATCH --export=ALL

# ---- Modules ----
module purge
module load slurm
module load cpu/0.15.4
module load gpu/0.17.3b
module load anaconda3/2021.05/kfluefz

# ---- Scratch setup ----
SCRATCH_JOB_DIR=/scratch/$USER/job_$SLURM_JOB_ID
BENCH_RESULTS_DIR=$SCRATCH_JOB_DIR/bench_results

mkdir -p "$BENCH_RESULTS_DIR"

# ---- Build in submit directory ----
cd "$SLURM_SUBMIT_DIR"

echo "Cleaning and building in $SLURM_SUBMIT_DIR..."
make clean
make

echo "Running benchmark; writing results to $BENCH_RESULTS_DIR"

# Use the Anaconda python, not system python3
srun python bench_stencil2d_pthreads.py \
  --make_exe ./make-2d \
  --pth_exe ./pth-stencil-2d \
  --N1 128 --N2 256 --num_Ns 3 \
  --P_start 1 --P_step 1 --P_max 8 \
  --I1 10 --I2 200 --Istep 20 \
  --warmup 1 --trials 4 \
  --timeout_sec 600 \
  --eff_range "0.29 0.05" \
  --results-dir "$BENCH_RESULTS_DIR" \
  --label bench_run1

# ---- Copy results back to project data folder ----
echo "Copying benchmark results back to project data folder..."

DEST_DIR="$SLURM_SUBMIT_DIR/data/bench_$SLURM_JOB_ID"
mkdir -p "$DEST_DIR"

# Only copy if there is at least one file in BENCH_RESULTS_DIR
if compgen -G "$BENCH_RESULTS_DIR/*" > /dev/null; then
    cp -rp "$BENCH_RESULTS_DIR"/* "$DEST_DIR"/
    echo "Benchmark results copied to: $DEST_DIR"
else
    echo "No benchmark files found in $BENCH_RESULTS_DIR; nothing to copy."
fi

echo "Benchmark job $SLURM_JOB_ID complete."
