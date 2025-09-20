#!/bin/bash
#SBATCH --job-name=matrix_multiply_debug
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
module load cmake/3.21.4
module load slurm

# ---- Work directory ----
cd "$HOME/CSCI473/Code/mpi01/matrix/matrix/"

# ---- Rebuild the helper binary ----
make clean
make

# -----------------------------
# Run the MPI job
# -----------------------------
srun -n 128 python test_mpi_matrix.py 5000 40000 1000 1 128 1
