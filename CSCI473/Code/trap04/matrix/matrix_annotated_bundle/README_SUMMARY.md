# Matrix Toolkit — Annotated Breakdown

This bundle contains **your original sources** plus annotations and a high-level explanation of what each file does and how they interact. Use this as a quick guide.

## Repository Layout

- `Makefile` — build rules for all utilities (serial and MPI).
- `make-matrix.c` — generates random (or patterned) dense matrices and vectors in files.
- `print-matrix.c` — reads a matrix or vector file and prints it nicely (with size, sample content).
- `matrix-vector-multiply.c` — serial matrix–vector multiply (A x) with simple timers and I/O.
- `mpi-matrix-vector-multiply.c` — MPI-distributed matrix–vector multiply dividing rows across ranks.
- `test_matrix_vector_mult.py` — unit/integration tests for serial multiply and I/O.
- `test_mpi_matrix_vector_mult.py` — unit/integration tests for MPI build/run.

## Typical Workflow

1. **Create inputs**
   - Use `make-matrix` to create a matrix `A` (N×N or N×M) and a vector `x` (M).
2. **Verify inputs**
   - Use `print-matrix` on the files to inspect sizes and sample values.
3. **Compute**
   - Run `matrix-vector-multiply A x -> y` (serial) or `mpirun -np P mpi-matrix-vector-multiply A x -> y`.
4. **Inspect outputs**
   - `print-matrix y` to verify size (N) and values.
5. **Test**
   - `pytest -q` to run provided tests.

## Build

- Serial tools:
  - `make make-matrix print-matrix matrix-vector-multiply`
- MPI tool:
  - `make mpi-matrix-vector-multiply` (requires `mpicc` and MPI headers/runtimes).

Variables like `CC`, `MPICC`, `CFLAGS`, and `WARNFLAGS` are parameterized in the Makefile for portability.

## File I/O Formats (as implied by the code)

- **Matrix files (`.mtx` or raw filename)**:
  - Header with `rows` and `cols` (integers), then a contiguous block of `double` values in row-major order.
- **Vector files**:
  - A `length` header (integer) followed by `double` values.

> If you generated files with these utilities, formats are consistent across programs. Mismatched dimensions cause explicit error messages.

## Algorithmic Overview

- **Serial (`matrix-vector-multiply.c`)**:
  - Reads full A (N×M) and x (M) into memory, loops rows i=0..N-1:
    - `y[i] = dot(A[i,*], x)`
  - Uses `gettimeofday` for timing I/O vs compute.

- **MPI (`mpi-matrix-vector-multiply.c`)**:
  - Rank 0 reads matrix metadata (N, M) and broadcasts sizes.
  - Rows are block-distributed as contiguous chunks across ranks.
  - Every rank receives the full vector `x` (via `Bcast`) and its local slice of rows.
  - Each rank computes its local `y_local`; results are gathered to rank 0 (via `Gatherv`/`Gather`).
  - Optional barriers/timers split I/O, compute, and write phases.

See **PSEUDOCODE.md** for a step-by-step walkthrough per file.

## Notes & Portability

- `gettimeofday` requires `<sys/time.h>`; some compilers need POSIX feature macros. On Windows, use `QueryPerformanceCounter` or guard the timer code.
- For very large matrices, consider memory mapping or streaming blocks instead of reading the full matrix on rank 0.
- When using MPI, ensure `mpicc` and `mpirun` are from the same MPI distribution (OpenMPI/MPICH).

