# ===============================================================
# File: Makefile
# Desc: Build system for Stencil_proj.
#       Compiles all C executables (serial and pthread versions).
#       All generated binaries are placed in ./code.
#       Data files (inputs/outputs) are stored in ../data.
#
# Targets:
#   all   - Build all executables
#   clean - Remove all build artifacts and temporary files
# ===============================================================

CC      = gcc
CFLAGS  = -O3 -Wall -Wextra -std=c11 -pthread
LDFLAGS = -lm
OUTDIR  = .
DATADIR = ../data

# ==========================
# Executables
# ==========================
EXE_SERIAL = stencil-2d
EXE_PTH    = pth-stencil-2d
EXE_MAKE2D = make-2d
EXE_PRINT  = print-2d
EXE_UTILS  = utilities

# ==========================
# Object Files
# ==========================
OBJS_SERIAL = stencil-2d.o utilities.o
OBJS_PTH    = pth-stencil-2d.o utilities.o
OBJS_MAKE2D = make-2d.o
OBJS_PRINT  = print-2d.o
OBJS_UTILS  = utilities.o

# ==========================
# Build Rules
# ==========================
all: $(EXE_SERIAL) $(EXE_PTH) $(EXE_MAKE2D) $(EXE_PRINT)

# Serial version
$(EXE_SERIAL): $(OBJS_SERIAL)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Pthread version
$(EXE_PTH): $(OBJS_PTH)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Input generator
$(EXE_MAKE2D): $(OBJS_MAKE2D)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Print utility
$(EXE_PRINT): $(OBJS_PRINT)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)

# Object file rule
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

# ==========================
# Clean Targets
# ==========================
clean:
	@echo "Cleaning build artifacts..."
	rm -f *.o
	rm -f $(EXE_SERIAL) $(EXE_PTH) $(EXE_MAKE2D) $(EXE_PRINT)
	@echo "Removing generated data files..."
	rm -f $(DATADIR)/*.dat $(DATADIR)/*.raw $(DATADIR)/*.csv
	rm -f $(DATADIR)/*.png
	@echo "Clean complete."

.PHONY: all clean
