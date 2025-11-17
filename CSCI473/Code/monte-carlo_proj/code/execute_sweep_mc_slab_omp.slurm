#!/bin/bash
#SBATCH --job-name=mc_slab_debug
#SBATCH --output=mc_slab_debug.%j.out
#SBATCH --error=mc_slab_debug.%j.err
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=20
#SBATCH --cpus-per-task=1
#SBATCH --mem=32G
#SBATCH --time=00:30:00
#SBATCH --account=ccu108
#SBATCH --export=ALL

# Make sure the 'module' command is available inside the batch job
source /etc/profile.d/modules.sh

# Clean environment and load Expanse CPU environment + compiler + Slurm tools
module purge
module load slurm
module load cpu/0.15.4
module load gcc/10.2.0
module load anaconda3/2020.11

# ---- Scratch setup ----
SCRATCH_JOB_DIR=/scratch/$USER/job_$SLURM_JOB_ID
SWEEP_RESULTS_DIR=$SCRATCH_JOB_DIR/sweep_results

mkdir -p "$SWEEP_RESULTS_DIR"

# ---- Build in submit directory ----
cd "$SLURM_SUBMIT_DIR"

echo "Cleaning and building in $SLURM_SUBMIT_DIR..."
make clean
make


#Run the python sweep script
python3 sweep_mc_slab_omp.py --exe ./mc_slab_omp --C 0.5 --Cc 0.1 --H 5.0 \
    --seed 12345 --n_start 100000 --n_max 66400000 --Ps 1,2,4,8,16,20 --trials 5 --warmup 1 \
    --eff_targets 0.5,0.7,0.8 --results_dir perf_results_mc

# ---- Copy results back to project data folder ----
echo "Copying sweep results back to project data folder..."

DEST_DIR="$SLURM_SUBMIT_DIR/data/sweep_$SLURM_JOB_ID"
mkdir -p "$DEST_DIR"

# Only copy if there is at least one file in SWEEP_RESULTS_DIR
if compgen -G "$SWEEP_RESULTS_DIR/*" > /dev/null; then
    cp -rp "$SWEEP_RESULTS_DIR"/* "$DEST_DIR"/
    echo "Benchmark results copied to: $DEST_DIR"
else
    echo "No sweep files found in $SWEEP_RESULTS_DIR; nothing to copy."
fi
#Clean files
make clean