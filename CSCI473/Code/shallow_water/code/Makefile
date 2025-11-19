# Makefile for sw2d.c — 2D shallow-water simulation
# Usage:
#   make           # build release (optimized) binary
#   make debug     # build debug binary with sanitizers
#   make clean     # remove build artifacts
#   make run       # quick demo run (edit args below)

# ---- Configurable variables -------------------------------------------------

# Compiler and common warnings
CC      := gcc
WARN    := -Wall -Wextra -Wshadow -Wconversion -Wfloat-equal -Wpointer-arith

# Release flags (fast)
OPT     := -O3 -march=native
# Debug flags (safe, with symbols & sanitizers)
DBG     := -O0 -g -fsanitize=address,undefined

# Libraries (sqrt from libm)
LDLIBS  := -lm

# Source and targets
SRC         := sw2d.c
OBJ         := $(SRC:.c=.o)
TARGET      := sw2d
PTHREAD_SRC := sw2d_pthread.c
PTHREAD_OBJ := $(PTHREAD_SRC:.c=.o)
PTHREAD_BIN := sw2d_pthread
OMP_SRC     := sweep_sw2d_omp.c
OMP_OBJ     := $(OMP_SRC:.c=.o)
OMP_BIN     := sw2d_omp
PROJECT_GENDIRS := data sw2d_consistency tmp

# ---- Default target ---------------------------------------------------------

.PHONY: all
all: CFLAGS += $(OPT) $(WARN)
all: $(TARGET) $(PTHREAD_BIN) $(OMP_BIN)

# ---- Debug & Release convenience targets -----------------------------------

.PHONY: release debug
release: CFLAGS += $(OPT) $(WARN)
release: clean $(TARGET) $(PTHREAD_BIN) $(OMP_BIN)

debug: CFLAGS += $(DBG) $(WARN)
debug: clean $(TARGET) $(PTHREAD_BIN) $(OMP_BIN)

# ---- Link rule --------------------------------------------------------------

$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $@ $^ $(LDLIBS)

$(PTHREAD_BIN): $(PTHREAD_OBJ)
	$(CC) $(CFLAGS) -pthread -o $@ $^ $(LDLIBS)

$(OMP_BIN): $(OMP_OBJ)
	$(CC) $(CFLAGS) -fopenmp -o $@ $^ $(LDLIBS)

# ---- Compile rule -----------------------------------------------------------

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

$(OMP_OBJ): $(OMP_SRC)
	$(CC) $(CFLAGS) -fopenmp -c $< -o $@

# ---- Utility targets --------------------------------------------------------

.PHONY: run
run: $(TARGET)
	./$(TARGET) --rows 100 --cols 100 --steps 500 \
	            --height 0.5 --save-interval 50 --out movie.bin

.PHONY: clean
clean:
	$(RM) $(OBJ) $(PTHREAD_OBJ) $(OMP_OBJ) $(TARGET) $(PTHREAD_BIN) $(OMP_BIN) movie.bin movie_p.bin movie_omp.bin _timer_helper.so
	$(RM) -r $(PROJECT_GENDIRS)

.PHONY: format
format:
	@command -v clang-format >/dev/null 2>&1 && clang-format -i $(SRC) $(PTHREAD_SRC) $(OMP_SRC) || \
	 echo "clang-format not found; skipping."

# ---- Help -------------------------------------------------------------------

.PHONY: help
help:
	@echo "Targets:"
	@echo "  make / make release  Build optimized binary ($(TARGET))"
	@echo "  make debug           Build debug binary with sanitizers"
	@echo "  make run             Run a small demo (edit args in Makefile)"
	@echo "  make clean           Remove objects, binary, and movie.bin"
	@echo "  make format          clang-format the source (if available)"
