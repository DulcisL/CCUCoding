# =====================================================
# Monte Carlo slab Makefile (serial + pthread + OpenMP)
# All executables live in ./code
# =====================================================

CC       = gcc
CFLAGS   = -std=c99 -Wall -Wextra -O2 -pedantic
LDLIBS   = -lm

TARGETS      = mc_slab mc_slab_pthread mc_slab_omp
COMMON_OBJS  = utilities.o
HDRS         = utilities.h timer.h

DATA_DIRS = perf_results_mc consistency_results_mc sweep_results_mc

.PHONY: all clean clean-data rebuild

all: $(TARGETS)

rebuild: clean all

# -------------------------
# Object rules
# -------------------------
%.o: %.c $(HDRS)
	$(CC) $(CFLAGS) -c $< -o $@

mc_slab.o: mc_slab.c
mc_slab_pthread.o: mc_slab_pthread.c
mc_slab_pthread.o: CFLAGS += -pthread
mc_slab_omp.o: mc_slab_omp.c
mc_slab_omp.o: CFLAGS += -fopenmp

# -------------------------
# Executable builds
# -------------------------
mc_slab: mc_slab.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LDLIBS)

mc_slab_pthread: CFLAGS += -pthread
mc_slab_pthread: LDFLAGS += -pthread
mc_slab_pthread: mc_slab_pthread.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LDLIBS)

mc_slab_omp: CFLAGS += -fopenmp
mc_slab_omp: LDFLAGS += -fopenmp
mc_slab_omp: mc_slab_omp.o $(COMMON_OBJS)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^ $(LDLIBS)

# -------------------------
# Housekeeping
# -------------------------
clean:
	@echo "Cleaning binaries and objects..."
	rm -f $(TARGETS) *.o

clean-data:
	@echo "Removing generated data directories..."
	rm -rf $(DATA_DIRS)
