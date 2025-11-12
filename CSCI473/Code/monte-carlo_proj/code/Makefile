# =====================================================
# Makefile — Stencil 2D (serial + pthread)
# All code/executables live in ./code
# All data files are read/written in ../data (handled in the programs)
# =====================================================

CC      = gcc
CFLAGS  = -std=c99 -Wall -Wextra -O2 -pedantic
PTHREAD = -lpthread

# Executables
TARGETS = mc_slab mc_slab_pthread mc_slab_omp

# Headers
HDRS    = utilities.h timer.h

# Default build
all: $(TARGETS)

# -------------------------
# Serial builds
# -------------------------
mc_slab: mc_slab.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -o $@ mc_slab.c utilities.c -lm

# -------------------------
# Pthreads build
# -------------------------

mc_slab_pthread: mc_slab_pthread.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -pthread -o $@ mc_slab_pthread.c utilities.c -lm

mc_slab_omp: mc_slab_omp.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -fopenmp -o $@ mc_slab_omp.c utilities.c -lm
# -------------------------
# MPI build
# -------------------------

# -------------------------
# Housekeeping
# -------------------------
.PHONY: all clean clean-data

clean:
	@echo "Cleaning binaries and objects..."
	rm -f $(TARGETS) *.o
