/*   Inline commentary woven throughout for educational clarity. */
/*
 * mpi_matrix-vector-multiply.c
 *
 * Usage:
 *   mpirun -np <P> ./mpi_matrix-vector-multiply <input A> <input B> <output C>
 *
 * Binary format (as in make-matrix):
 *   [int rows][int cols][double payload row-major]
 *
 * Timings (rank 0 prints):
 *   TIMING total_s=... read_s=... compute_s=... write_s=... m=... n=... p=...
 *     - read_s   : rank 0's time for reading A/B + Bcast(B) + Scatterv(A)
 *     - compute_s: MAX over ranks of local compute time (critical path)
 *     - write_s  : rank 0's time for Gatherv(C) + writing C
 *     - total_s  : overall wall time on rank 0
 */

/*   Standard include for required APIs. */
#include <mpi.h>
/*   Standard include for required APIs. */
#include <stdio.h>
/*   Standard include for required APIs. */
#include <stdlib.h>
/*   Standard include for required APIs. */
#include <string.h>
/*   Standard include for required APIs. */
#include <errno.h>
/*   Standard include for required APIs. */
#include <limits.h>
/*   Standard include for required APIs. */
#include <stdint.h>

/* ---------------- one-malloc matrix container ---------------- */
/*   Data structure definition begins. */
typedef struct
{
        size_t rows, cols;
        double **row; /* row pointers */
        double *data; /* contiguous payload */
        void *block;  /* base allocation to free */
        /*   End of struct typedef. */
} Matrix;

/* ---------------- helpers: usage & errors ---------------- */
/*   Function begins — explain parameters, side effects, and return. */
static void usage(const char *prog)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
        /*   Branch — guard or special-case. */
        if (!prog)
                prog = "mpi_matrix-vector-multiply";
        /*   I/O — fprintf call. */
        fprintf(stderr,
                "Usage:\n"
                "  mpirun -np <P> %s <input A> <input B> <output C>\n",
                prog);
}

/* size_t overflow helpers */
/*   Function begins — explain parameters, side effects, and return. */
static int mul_size_t(size_t a, size_t b, size_t *out)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
#if defined(__has_builtin)
#if __has_builtin(__builtin_mul_overflow)
        /*   Epilogue — return from function. */
        return __builtin_mul_overflow(a, b, out);
#endif
#endif
        /*   Branch — guard or special-case. */
        if (a == 0 || b == 0)
        {
                *out = 0;
                return 0;
        }
        /*   Branch — guard or special-case. */
        if (a > SIZE_MAX / b)
                return 1;
        *out = a * b;
        /*   Epilogue — return from function. */
        return 0;
}
/*   Function begins — explain parameters, side effects, and return. */
static int add_size_t(size_t a, size_t b, size_t *out)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
#if defined(__has_builtin)
#if __has_builtin(__builtin_add_overflow)
        /*   Epilogue — return from function. */
        return __builtin_add_overflow(a, b, out);
#endif
#endif
        /*   Branch — guard or special-case. */
        if (b > SIZE_MAX - a)
                return 1;
        *out = a + b;
        /*   Epilogue — return from function. */
        return 0;
}

/* Build one-malloc 2D layout (uninitialized payload) */
/*   Function begins — explain parameters, side effects, and return. */
static int alloc_matrix(size_t rows, size_t cols, Matrix *M)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
        /*   Memory — memset. */
        memset(M, 0, sizeof(*M));
        size_t ptrs_bytes = 0, n_elems = 0, payload_bytes = 0, total_bytes = 0;

        /*   Branch — guard or special-case. */
        if (mul_size_t(rows, sizeof(double *), &ptrs_bytes) ||
            mul_size_t(rows, cols, &n_elems) ||
            mul_size_t(n_elems, sizeof(double), &payload_bytes) ||
            add_size_t(ptrs_bytes, payload_bytes, &total_bytes))
        {
                /*   Epilogue — return from function. */
                return -1;
        }
        void *block = /*   Memory — malloc. */
            malloc(total_bytes);
        /*   Branch — guard or special-case. */
        if (!block)
                return -1;

        double **row_ptrs = (double **)block;
        double *payload = (double *)((unsigned char *)block + ptrs_bytes);

        /*   Loop — iterate over range. */
        for (size_t r = 0; r < rows; ++r)
        {
                row_ptrs[r] = payload + r * cols;
        }

        M->rows = rows;
        M->cols = cols;
        M->row = row_ptrs;
        M->data = payload;
        M->block = block;
        /*   Epilogue — return from function. */
        return 0;
}

/* Rank 0: read matrix from file into one-malloc layout */
/*   Function begins — explain parameters, side effects, and return. */
static int read_matrix_rank0(const char *path, Matrix *M)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
        /*   Memory — memset. */
        memset(M, 0, sizeof(*M));
        FILE *fp = /*   I/O — fopen call. */
            fopen(path, "rb");
        /*   Branch — guard or special-case. */
        if (!fp)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: open '%s' failed: %s\n", path, strerror(errno));
                /*   Epilogue — return from function. */
                return -1;
        }
        int irows = 0, icols = 0;
        /*   Branch — guard or special-case. */
        if (/*   I/O — fread call. */
            fread(&irows, sizeof(int), 1, fp) != 1 ||
            /*   I/O — fread call. */
            fread(&icols, sizeof(int), 1, fp) != 1)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: read header from '%s' failed: %s\n",
                        path, ferror(fp) ? strerror(errno) : "unexpected EOF");
                /*   I/O — fclose call. */
                fclose(fp);
                /*   Epilogue — return from function. */
                return -1;
        }
        /*   Branch — guard or special-case. */
        if (irows <= 0 || icols <= 0)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: invalid dims in '%s': rows=%d cols=%d\n", path, irows, icols);
                /*   I/O — fclose call. */
                fclose(fp);
                /*   Epilogue — return from function. */
                return -1;
        }
        size_t rows = (size_t)irows, cols = (size_t)icols;

        /*   Branch — guard or special-case. */
        if (alloc_matrix(rows, cols, M) != 0)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: alloc_matrix(%zu,%zu) failed for '%s'\n", rows, cols, path);
                /*   I/O — fclose call. */
                fclose(fp);
                /*   Epilogue — return from function. */
                return -1;
        }
        size_t n_elems = rows * cols;
        size_t nread = /*   I/O — fread call. */
            fread(M->data, sizeof(double), n_elems, fp);
        /*   Branch — guard or special-case. */
        if (nread != n_elems)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: short read on '%s': expected %zu doubles, got %zu: %s\n",
                        path, n_elems, nread, ferror(fp) ? strerror(errno) : "unexpected EOF");
                /*   I/O — fclose call. */
                fclose(fp);
                /*   Memory — free. */
                free(M->block); /*   Memory — memset. */
                memset(M, 0, sizeof(*M));
                /*   Epilogue — return from function. */
                return -1;
        }
        /*   Branch — guard or special-case. */
        if (/*   I/O — fclose call. */
            fclose(fp) != 0)
        {
                /*   I/O — fprintf call. */
fprintf(stderr, "Rank0: warning: /*   I/O — fclose call. */
fclose('%s') failed: %s\n", path, strerror(errno));
        }
        /*   Epilogue — return from function. */
        return 0;
}

/* Rank 0: write matrix to file from one-malloc layout */
/*   Function begins — explain parameters, side effects, and return. */
static int write_matrix_rank0(const char *path, const Matrix *M)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
        /*   Branch — guard or special-case. */
        if (M->rows > (size_t)INT_MAX || M->cols > (size_t)INT_MAX)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: dims exceed INT_MAX for header: %zu x %zu\n", M->rows, M->cols);
                /*   Epilogue — return from function. */
                return -1;
        }
        FILE *fp = /*   I/O — fopen call. */
            fopen(path, "wb");
        /*   Branch — guard or special-case. */
        if (!fp)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: open '%s' for writing failed: %s\n", path, strerror(errno));
                /*   Epilogue — return from function. */
                return -1;
        }
        int irows = (int)M->rows;
        int icols = (int)M->cols;
        /*   Branch — guard or special-case. */
        if (/*   I/O — fwrite call. */
            fwrite(&irows, sizeof(int), 1, fp) != 1 ||
            /*   I/O — fwrite call. */
            fwrite(&icols, sizeof(int), 1, fp) != 1)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: writing header to '%s' failed: %s\n", path, strerror(errno));
                /*   I/O — fclose call. */
                fclose(fp);
                /*   Epilogue — return from function. */
                return -1;
        }
        size_t n_elems = M->rows * M->cols;
        size_t wrote = /*   I/O — fwrite call. */
            fwrite(M->data, sizeof(double), n_elems, fp);
        /*   Branch — guard or special-case. */
        if (wrote != n_elems)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank0: short write to '%s': expected %zu doubles, wrote %zu: %s\n",
                        path, n_elems, wrote, strerror(errno));
                /*   I/O — fclose call. */
                fclose(fp);
                /*   Epilogue — return from function. */
                return -1;
        }
        /*   Branch — guard or special-case. */
        if (/*   I/O — fclose call. */
            fclose(fp) != 0)
        {
                /*   I/O — fprintf call. */
fprintf(stderr, "Rank0: warning: /*   I/O — fclose call. */
fclose('%s') failed: %s\n", path, strerror(errno));
        }
        /*   Epilogue — return from function. */
        return 0;
}

/* Row partitioning */
/*   Function begins — explain parameters, side effects, and return. */
static void partition_rows(int m, int world_size, int *counts_rows, int *displs_rows)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
        int base = m / world_size;
        int rem = m % world_size;
        int disp = 0;
        /*   Loop — iterate over range. */
        for (int r = 0; r < world_size; ++r)
        {
                int rows_r = base + (r < rem ? 1 : 0);
                counts_rows[r] = rows_r;
                displs_rows[r] = disp;
                disp += rows_r;
        }
}

/*   Function begins — explain parameters, side effects, and return. */
int main(int argc, char **argv)
{
        /*   Prologue — validate inputs, set up locals, and prepare resources. */
        int provided = 0;
        MPI_Init_thread(&argc, &argv, MPI_THREAD_FUNNELED, &provided);

        int rank = 0, world = 1;
        /*   MPI — MPI_Comm_rank. */
        MPI_Comm_rank(MPI_COMM_WORLD, &rank);
        /*   MPI — MPI_Comm_size. */
        MPI_Comm_size(MPI_COMM_WORLD, &world);

        /* Graceful usage failure when args are missing */
        /*   Branch — guard or special-case. */
        if (argc != 4)
        {
                /*   Branch — guard or special-case. */
                if (rank == 0)
                        usage(argv[0]);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        const char *pathA = argv[1];
        const char *pathB = argv[2];
        const char *pathC = argv[3];

        Matrix A_full = {0}, B_full = {0}; /* rank 0 only */
        Matrix B = {0};                    /* all ranks hold B (n x 1) */
        int m = 0, n = 0;

        /* Timing variables */
        double t_total_start = 0.0, t_total_end = 0.0;
        double t_read_start = 0.0, t_read_end = 0.0;       /* rank 0: read & distribute */
        double t_compute_start = 0.0, t_compute_end = 0.0; /* each rank local; reduce max */
        double t_write_start = 0.0, t_write_end = 0.0;     /* rank 0: gather+write */
        double compute_local = 0.0, compute_max = 0.0;

        /*   MPI — MPI_Barrier. */
        MPI_Barrier(MPI_COMM_WORLD);
        t_total_start = MPI_Wtime();

        /* ---------------- Rank 0: Read & distribute ---------------- */
        /*   MPI — MPI_Barrier. */
        MPI_Barrier(MPI_COMM_WORLD);
        /*   Branch — guard or special-case. */
        if (rank == 0)
                t_read_start = MPI_Wtime();

        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                /*   Branch — guard or special-case. */
                if (read_matrix_rank0(pathA, &A_full) != 0)
                {
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Branch — guard or special-case. */
                if (read_matrix_rank0(pathB, &B_full) != 0)
                {
                        /*   Memory — free. */
                        free(A_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Branch — guard or special-case. */
                if ((int)B_full.cols != 1)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: Error: B must be n x 1, but is %zu x %zu\n", B_full.rows, B_full.cols);
                        /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Branch — guard or special-case. */
                if (A_full.cols != B_full.rows)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: Error: A(%zu x %zu) and B(%zu x %zu) mismatch (need A.cols==B.rows)\n",
                                A_full.rows, A_full.cols, B_full.rows, B_full.cols);
                        /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Branch — guard or special-case. */
                if (A_full.rows > (size_t)INT_MAX || A_full.cols > (size_t)INT_MAX)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: Error: dims exceed INT_MAX.\n");
                        /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                m = (int)A_full.rows;
                n = (int)A_full.cols;
        }

        /* Broadcast dims to all ranks */
        /*   Branch — guard or special-case. */
        if (/*   MPI — MPI_Bcast. */
            /*   MPI — MPI_Bcast. */
            MPI_Bcast(&m, 1, MPI_INT, 0, MPI_COMM_WORLD) != MPI_SUCCESS ||
            /*   MPI — MPI_Bcast. */
            /*   MPI — MPI_Bcast. */
            MPI_Bcast(&n, 1, MPI_INT, 0, MPI_COMM_WORLD) != MPI_SUCCESS)
        {
                /*   Branch — guard or special-case. */
                if (rank == 0) /*   I/O — fprintf call. */
                        fprintf(stderr, "MPI_Bcast of dims failed.\n");
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }
        /*   Branch — guard or special-case. */
        if (m <= 0 || n <= 0)
        {
                /*   Branch — guard or special-case. */
                if (rank == 0) /*   I/O — fprintf call. */
                        fprintf(stderr, "Invalid dims broadcast: m=%d n=%d\n", m, n);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        /* Allocate B on all ranks and broadcast its payload */
        /*   Branch — guard or special-case. */
        if (alloc_matrix((size_t)n, 1, &B) != 0)
        {
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: alloc_matrix for B(%d x 1) failed.\n", rank, n);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }
        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                /*   Memory — memcpy. */
                memcpy(B.data, B_full.data, (size_t)n * sizeof(double));
        }
        /*   Branch — guard or special-case. */
        if (/*   MPI — MPI_Bcast. */
            /*   MPI — MPI_Bcast. */
            MPI_Bcast(B.data, n, MPI_DOUBLE, 0, MPI_COMM_WORLD) != MPI_SUCCESS)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: MPI_Bcast for B failed.\n", rank);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        /* Partition rows and build counts/displs (rows, and in doubles for A/C payloads) */
        int *counts_rows = (int *)/*   Memory — malloc. */
            malloc((size_t)world * sizeof(int));
        int *displs_rows = (int *)/*   Memory — malloc. */
            malloc((size_t)world * sizeof(int));
        /*   Branch — guard or special-case. */
        if (!counts_rows || !displs_rows)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: malloc counts/displs failed.\n", rank);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }
        partition_rows(m, world, counts_rows, displs_rows);

        int *sendcounts_A = (int *)/*   Memory — malloc. */
            malloc((size_t)world * sizeof(int));
        int *displs_A = (int *)/*   Memory — malloc. */
            malloc((size_t)world * sizeof(int));
        /*   Branch — guard or special-case. */
        if (!sendcounts_A || !displs_A)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: malloc sendcounts/displs for A failed.\n", rank);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   Memory — free. */
                free(sendcounts_A); /*   Memory — free. */
                free(displs_A);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }
        /*   Loop — iterate over range. */
        for (int r = 0; r < world; ++r)
        {
                long elems = (long)counts_rows[r] * (long)n;
                long disp = (long)displs_rows[r] * (long)n;
                /*   Branch — guard or special-case. */
                if (elems > INT_MAX || disp > INT_MAX)
                {
                        /*   Branch — guard or special-case. */
                        if (rank == 0) /*   I/O — fprintf call. */
                                fprintf(stderr, "Error: message size exceeds MPI int on rank %d.\n", r);
                        /*   Branch — guard or special-case. */
                        if (rank == 0)
                        {                           /*   Memory — free. */
                                free(A_full.block); /*   Memory — free. */
                                free(B_full.block);
                        }
                        /*   Memory — free. */
                        free(B.block);
                        /*   Memory — free. */
                        free(counts_rows); /*   Memory — free. */
                        free(displs_rows);
                        /*   Memory — free. */
                        free(sendcounts_A); /*   Memory — free. */
                        free(displs_A);
                        /*   MPI — MPI_Finalize. */
                        MPI_Finalize();
                        /*   Epilogue — return from function. */
                        return EXIT_FAILURE;
                }
                sendcounts_A[r] = (int)elems;
                displs_A[r] = (int)disp;
        }

        /* Allocate local A (only as big as needed) and receive via Scatterv */
        int local_rows = counts_rows[rank];
        Matrix A_local = {0};
        /*   Branch — guard or special-case. */
        if (alloc_matrix((size_t)local_rows, (size_t)n, &A_local) != 0)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: alloc_matrix A_local(%d x %d) failed.\n", rank, local_rows, n);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   Memory — free. */
                free(sendcounts_A); /*   Memory — free. */
                free(displs_A);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        const double *A_sendbuf = NULL;
        /*   Branch — guard or special-case. */
        if (rank == 0)
                A_sendbuf = A_full.data;

        /*   Branch — guard or special-case. */
        if (/*   MPI — MPI_Scatterv. */
            MPI_Scatterv(A_sendbuf, sendcounts_A, displs_A, MPI_DOUBLE,
                         A_local.data, (int)((long)local_rows * (long)n), MPI_DOUBLE,
                         0, MPI_COMM_WORLD) != MPI_SUCCESS)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: MPI_Scatterv of A failed.\n", rank);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {                           /*   Memory — free. */
                        free(A_full.block); /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(A_local.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   Memory — free. */
                free(sendcounts_A); /*   Memory — free. */
                free(displs_A);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                /* Free A_full now that rows are distributed */
                /*   Memory — free. */
                free(A_full.block);
                A_full.block = NULL;
                /*   Memory — memset. */
                memset(&A_full, 0, sizeof(A_full));
        }

        /*   MPI — MPI_Barrier. */
        MPI_Barrier(MPI_COMM_WORLD);
        /*   Branch — guard or special-case. */
        if (rank == 0)
                t_read_end = MPI_Wtime();

        /* ---------------- Compute phase (each rank) ---------------- */
        Matrix C_local = {0};
        /*   Branch — guard or special-case. */
        if (alloc_matrix((size_t)local_rows, 1, &C_local) != 0)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: alloc_matrix C_local(%d x 1) failed.\n", rank, local_rows);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                { /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(A_local.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   Memory — free. */
                free(sendcounts_A); /*   Memory — free. */
                free(displs_A);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        /*   MPI — MPI_Barrier. */
        MPI_Barrier(MPI_COMM_WORLD);
        t_compute_start = MPI_Wtime();

        /*   Loop — iterate over range. */
        for (int i = 0; i < local_rows; ++i)
        {
                const double *Ai = A_local.row[i];
                double sum = 0.0;
                /*   Loop — iterate over range. */
                for (int k = 0; k < n; ++k)
                {
                        sum += Ai[k] * B.row[k][0];
                }
                C_local.row[i][0] = sum;
        }

        t_compute_end = MPI_Wtime();
        compute_local = t_compute_end - t_compute_start;

        /* Reduce compute to the max across ranks (critical path) */
        /*   Branch — guard or special-case. */
        if (MPI_Reduce(&compute_local, &compute_max, 1, MPI_DOUBLE, MPI_MAX, 0, MPI_COMM_WORLD) != MPI_SUCCESS)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: MPI_Reduce for compute_max failed.\n", rank);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                { /*   Memory — free. */
                        free(B_full.block);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(C_local.block);
                /*   Memory — free. */
                free(A_local.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   Memory — free. */
                free(sendcounts_A); /*   Memory — free. */
                free(displs_A);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        /* ---------------- Gather+Write phase ---------------- */
        int *recvcounts_C = NULL;
        int *displs_C = NULL;
        double *C_recvbuf = NULL;

        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                t_write_start = MPI_Wtime();
                recvcounts_C = (int *)/*   Memory — malloc. */
                    malloc((size_t)world * sizeof(int));
                displs_C = (int *)/*   Memory — malloc. */
                    malloc((size_t)world * sizeof(int));
                /*   Branch — guard or special-case. */
                if (!recvcounts_C || !displs_C)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: malloc recvcounts/displs for C failed.\n");
                        /*   Memory — free. */
                        free(B.block);
                        /*   Memory — free. */
                        free(C_local.block);
                        /*   Memory — free. */
                        free(A_local.block);
                        /*   Memory — free. */
                        free(counts_rows); /*   Memory — free. */
                        free(displs_rows);
                        /*   Memory — free. */
                        free(sendcounts_A); /*   Memory — free. */
                        free(displs_A);
                        /*   Memory — free. */
                        free(recvcounts_C); /*   Memory — free. */
                        free(displs_C);
                        /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Loop — iterate over range. */
                for (int r = 0; r < world; ++r)
                {
                        recvcounts_C[r] = counts_rows[r];
                        displs_C[r] = displs_rows[r];
                }
                C_recvbuf = (double *)/*   Memory — malloc. */
                    malloc((size_t)m * sizeof(double));
                /*   Branch — guard or special-case. */
                if (!C_recvbuf)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: malloc C_recvbuf(m=%d) failed.\n", m);
                        /*   Memory — free. */
                        free(B.block);
                        /*   Memory — free. */
                        free(C_local.block);
                        /*   Memory — free. */
                        free(A_local.block);
                        /*   Memory — free. */
                        free(counts_rows); /*   Memory — free. */
                        free(displs_rows);
                        /*   Memory — free. */
                        free(sendcounts_A); /*   Memory — free. */
                        free(displs_A);
                        /*   Memory — free. */
                        free(recvcounts_C); /*   Memory — free. */
                        free(displs_C);
                        /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
        }

        /*   Branch — guard or special-case. */
        if (/*   MPI — MPI_Gatherv. */
            MPI_Gatherv(C_local.data, local_rows, MPI_DOUBLE,
                        C_recvbuf, recvcounts_C, displs_C, MPI_DOUBLE,
                        0, MPI_COMM_WORLD) != MPI_SUCCESS)
        {
                /*   I/O — fprintf call. */
                fprintf(stderr, "Rank %d: MPI_Gatherv of C failed.\n", rank);
                /*   Branch — guard or special-case. */
                if (rank == 0)
                {
                        /*   Memory — free. */
                        free(C_recvbuf);
                        /*   Memory — free. */
                        free(recvcounts_C); /*   Memory — free. */
                        free(displs_C);
                }
                /*   Memory — free. */
                free(B.block);
                /*   Memory — free. */
                free(C_local.block);
                /*   Memory — free. */
                free(A_local.block);
                /*   Memory — free. */
                free(counts_rows); /*   Memory — free. */
                free(displs_rows);
                /*   Memory — free. */
                free(sendcounts_A); /*   Memory — free. */
                free(displs_A);
                /*   Branch — guard or special-case. */
                if (rank == 0) /*   Memory — free. */
                        free(B_full.block);
                /*   MPI — MPI_Finalize. */
                MPI_Finalize();
                /*   Epilogue — return from function. */
                return EXIT_FAILURE;
        }

        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                /* Package full C and write to disk */
                Matrix C_full = {0};
                /*   Branch — guard or special-case. */
                if (alloc_matrix((size_t)m, 1, &C_full) != 0)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: alloc_matrix C_full(%d x 1) failed.\n", m);
                        /*   Memory — free. */
                        free(C_recvbuf);
                        /*   Memory — free. */
                        free(recvcounts_C); /*   Memory — free. */
                        free(displs_C);
                        /*   Memory — free. */
                        free(B.block);
                        /*   Memory — free. */
                        free(C_local.block);
                        /*   Memory — free. */
                        free(A_local.block);
                        /*   Memory — free. */
                        free(counts_rows); /*   Memory — free. */
                        free(displs_rows);
                        /*   Memory — free. */
                        free(sendcounts_A); /*   Memory — free. */
                        free(displs_A);
                        /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Memory — memcpy. */
                memcpy(C_full.data, C_recvbuf, (size_t)m * sizeof(double));
                /*   Branch — guard or special-case. */
                if (write_matrix_rank0(pathC, &C_full) != 0)
                {
                        /*   I/O — fprintf call. */
                        fprintf(stderr, "Rank0: write_matrix('%s') failed.\n", pathC);
                        /*   Memory — free. */
                        free(C_full.block);
                        /*   Memory — free. */
                        free(C_recvbuf);
                        /*   Memory — free. */
                        free(recvcounts_C); /*   Memory — free. */
                        free(displs_C);
                        /*   Memory — free. */
                        free(B.block);
                        /*   Memory — free. */
                        free(C_local.block);
                        /*   Memory — free. */
                        free(A_local.block);
                        /*   Memory — free. */
                        free(counts_rows); /*   Memory — free. */
                        free(displs_rows);
                        /*   Memory — free. */
                        free(sendcounts_A); /*   Memory — free. */
                        free(displs_A);
                        /*   Memory — free. */
                        free(B_full.block);
                        MPI_Abort(MPI_COMM_WORLD, 1);
                }
                /*   Memory — free. */
                free(C_full.block);
                /*   Memory — free. */
                free(C_recvbuf);
                /*   Memory — free. */
                free(recvcounts_C); /*   Memory — free. */
                free(displs_C);

                t_write_end = MPI_Wtime();
        }

        /* ---------------- Finalize timings & print (rank 0) ---------------- */
        /*   MPI — MPI_Barrier. */
        MPI_Barrier(MPI_COMM_WORLD);
        t_total_end = MPI_Wtime();

        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                double read_s = t_read_end - t_read_start;
                double compute_s = compute_max;
                double write_s = t_write_end - t_write_start;
                double total_s = t_total_end - t_total_start;

                /* Machine-readable one-liner */
                /*   I/O — printf call. */
                printf("TIMING total_s=%.9f read_s=%.9f compute_s=%.9f write_s=%.9f m=%d n=%d p=%d\n",
                       total_s, read_s, compute_s, write_s, m, n, world);

                /* Human-readable breakdown */
                /*   I/O — fprintf call. */
                fprintf(stdout,
                        "MPI Matrix-Vector Multiply (p=%d): A(%d x %d) * B(%d x 1) -> C(%d x 1)\n"
                        "Elapsed times (seconds):\n"
                        "  /*   I/O — read call. */
                            read(I / O + dist) : %
                            .9f\n "
                                  "  compute (max):     %.9f\n"
                                  "  /*   I/O — write call. */
                            write(gather + I / O) : %
                            .9f\n "
                                  "  total:             %.9f\n",
                        world, m, n, n, m,
                        read_s, compute_s, write_s, total_s);
                fflush(stdout);
        }

        /* ---------------- Cleanup ---------------- */
        /*   Branch — guard or special-case. */
        if (rank == 0)
        {
                /*   Memory — free. */
                free(B_full.block);
        }
        /*   Memory — free. */
        free(B.block);
        /*   Memory — free. */
        free(C_local.block);
        /*   Memory — free. */
        free(A_local.block);

        /*   Memory — free. */
        free(counts_rows); /*   Memory — free. */
        free(displs_rows);
        /*   Memory — free. */
        free(sendcounts_A); /*   Memory — free. */
        free(displs_A);

        /*   MPI — MPI_Finalize. */
        MPI_Finalize();
        /*   Epilogue — return from function. */
        return EXIT_SUCCESS;
}
