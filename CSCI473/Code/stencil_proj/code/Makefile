# =====================================================
# Makefile — Stencil 2D (serial + pthread)
# All code/executables live in ./code
# All data files are read/written in ../data (handled in the programs)
# =====================================================

CC      = gcc
CFLAGS  = -std=c99 -Wall -Wextra -O2
PTHREAD = -lpthread

# Executables
TARGETS = make-2d stencil-2d print-2d pth_stencil

# Headers (timer.h is header-only)
HDRS    = utilities.h timer.h

# Default build
all: $(TARGETS)

# -------------------------
# Serial builds
# -------------------------
make-2d: make-2d.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -o $@ make-2d.c utilities.c

stencil-2d: stencil-2d.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -o $@ stencil-2d.c utilities.c

print-2d: print-2d.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -o $@ print-2d.c utilities.c

# -------------------------
# Pthreads build
# -------------------------
pth_stencil: pth_stencil.c utilities.c $(HDRS)
	$(CC) $(CFLAGS) -o $@ pth_stencil.c utilities.c $(PTHREAD)

# -------------------------
# Housekeeping
# -------------------------
.PHONY: all clean clean-data

clean:
	@echo "Cleaning binaries and objects..."
	rm -f $(TARGETS) *.o
