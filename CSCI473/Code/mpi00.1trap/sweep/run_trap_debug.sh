#!/bin/bash
#SBATCH --job-name=trap_sweep_debug
#SBATCH --account=ccu108                   # <-- replace with your allocation/project ID
#SBATCH --partition=debug
#SBATCH --nodes=1
#SBATCH --ntasks=128                       # 128 MPI ranks (1 full debug node)
#SBATCH --time=00:30:00                    # debug limit
#SBATCH --output=trap_sweep.out
#SBATCH --error=trap_sweep.err

# -----------------------------
# Environment setup
# -----------------------------
module purge
module load cpu/0.17.3b
module load gcc/10.2.0
module load openmpi/4.1.1                   # <-- match the MPI version to the one used to compile your code # load MPI (adjust version if needed)
module load py-matplotlib/3.4.3/yi6zmvu
module load slurm

# ---- Work directory ----
cd "$HOME/CSCI473/Code/mpi00.1trap/sweep"

# ---- Rebuild the helper binary ----
rm -f mpi_trap_modified
mpicc -Wall -Wextra -o mpi_trap_modified mpi_trap_modified.c

# -----------------------------
# Run the MPI job
# -----------------------------
srun -n 128 python mpi_trap_sweep.py 10 20 100000000 200000000 100000000 1 128 1

