/*   Inline commentary woven throughout for educational clarity. */
/*
 * matrix-vector-multiply.c
 *
 * Usage:
 *   ./matrix-vector-multiply <input matrix A> <input vector B> <output C>
 *
 * File format (same as make-matrix): [int rows][int cols][double payload row-major]
 * Timing:
 *   - Prints machine-readable one-line summary:
 *       TIMING total_s=<..> read_s=<..> compute_s=<..> write_s=<..> m=<..> n=<..>
 *   - Also prints a human-readable breakdown.
 */
// Needed for some systems on linux for time functions
#define _DEFAULT_SOURCE
/*   Standard include for required APIs. */
#include <sys/time.h> // struct timeval, gettimeofday

/*   Standard include for required APIs. */
#include <stdio.h>
/*   Standard include for required APIs. */
#include <stdlib.h>
/*   Standard include for required APIs. */
#include <string.h>
/*   Standard include for required APIs. */
#include <errno.h>
/*   Standard include for required APIs. */
#include <limits.h> /* INT_MAX */
/*   Standard include for required APIs. */
#include <stdint.h>
/*   Standard include for required APIs. */
#include <time.h> /* clock_gettime */

/*   Data structure definition begins. */
typedef struct
{
    size_t rows, cols;
    double **row; /* row pointers */
    double *data; /* contiguous payload */
    void *block;
    /*   End of struct typedef. */
} Matrix;

/*   Function begins — explain parameters, side effects, and return. */
static void usage(const char *prog)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    /*   I/O — fprintf call. */
    fprintf(stderr,
            "Usage:\n"
            "  %s <input matrix A> <input vector B> <output C>\n"
            "  - A: m x n, B: n x 1, C: m x 1\n",
            prog);
}

/* -------- timing helpers (monotonic clock) -------- */

/*   Function begins — explain parameters, side effects, and return. */
static double now_sec(void)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
#if defined(CLOCK_MONOTONIC)
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    /*   Epilogue — return from function. */
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
#else
    /* Very old fallback; not expected on modern macOS/Linux */
    struct timeval tv;
    /*   Timing — gettimeofday. */
    gettimeofday(&tv, NULL);
    /*   Epilogue — return from function. */
    return (double)tv.tv_sec + (double)tv.tv_usec * 1e-6;
#endif
}

/* -------- size_t overflow helpers -------- */

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
        /*   Epilogue — return from function. */
        return 0;
    }
    /*   Branch — guard or special-case. */
    if (a > SIZE_MAX / b)
        /*   Epilogue — return from function. */
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
        /*   Epilogue — return from function. */
        return 1;
    *out = a + b;
    /*   Epilogue — return from function. */
    return 0;
}

/* -------- I/O helpers (one-malloc layout) -------- */

/*   Function begins — explain parameters, side effects, and return. */
static int read_matrix(const char *path, Matrix *M_out)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    /*   Memory — memset. */
    memset(M_out, 0, sizeof(*M_out));

    FILE *fp = /*   I/O — fopen call. */
        fopen(path, "rb");
    /*   Branch — guard or special-case. */
    if (!fp)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: open '%s' failed: %s\n", path, strerror(errno));
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
        fprintf(stderr, "Error: reading header from '%s': %s\n",
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
        fprintf(stderr, "Error: invalid dims in '%s': rows=%d cols=%d\n", path, irows, icols);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }

    size_t rows = (size_t)irows, cols = (size_t)icols;

    size_t n_elems = 0, ptrs_bytes = 0, payload_bytes = 0, total_bytes = 0;
    /*   Branch — guard or special-case. */
    if (mul_size_t(rows, cols, &n_elems))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: rows*cols overflow for '%s'\n", path);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }
    /*   Branch — guard or special-case. */
    if (mul_size_t(rows, sizeof(double *), &ptrs_bytes))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: pointer table size overflow for '%s'\n", path);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }
    /*   Branch — guard or special-case. */
    if (mul_size_t(n_elems, sizeof(double), &payload_bytes))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: payload size overflow for '%s'\n", path);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }
    /*   Branch — guard or special-case. */
    if (add_size_t(ptrs_bytes, payload_bytes, &total_bytes))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: total allocation size overflow for '%s'\n", path);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }

    void *block = /*   Memory — malloc. */
        malloc(total_bytes);
    /*   Branch — guard or special-case. */
    if (!block)
    {
        /*   I/O — fprintf call. */
fprintf(stderr, "Error: /*   Memory — malloc. */
malloc(%zu) failed for '%s': %s\n",
                total_bytes, path, strerror(errno));
/*   I/O — fclose call. */
fclose(fp);
/*   Epilogue — return from function. */
return -1;
    }

    double **row_ptrs = (double **)block;
    double *payload = (double *)((unsigned char *)block + ptrs_bytes);

    /*   Loop — iterate over range. */
    for (size_t r = 0; r < rows; ++r)
    {
        row_ptrs[r] = payload + r * cols;
    }

    size_t nread = /*   I/O — fread call. */
        fread(payload, sizeof(double), n_elems, fp);
    /*   Branch — guard or special-case. */
    if (nread != n_elems)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: short read on '%s': expected %zu doubles, got %zu: %s\n",
                path, n_elems, nread, ferror(fp) ? strerror(errno) : "unexpected EOF");
        /*   Memory — free. */
        free(block);
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
fprintf(stderr, "Warning: /*   I/O — fclose call. */
fclose('%s') failed: %s\n", path, strerror(errno));
    }

    M_out->rows = rows;
    M_out->cols = cols;
    M_out->row = row_ptrs;
    M_out->data = payload;
    M_out->block = block;
    /*   Epilogue — return from function. */
    return 0;
}

/*   Function begins — explain parameters, side effects, and return. */
static int write_matrix(const char *path, const Matrix *M)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    /*   Branch — guard or special-case. */
    if (M->rows > (size_t)INT_MAX || M->cols > (size_t)INT_MAX)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: dims exceed INT_MAX for header: %zu x %zu\n", M->rows, M->cols);
        /*   Epilogue — return from function. */
        return -1;
    }

    FILE *fp = /*   I/O — fopen call. */
        fopen(path, "wb");
    /*   Branch — guard or special-case. */
    if (!fp)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: open '%s' for writing failed: %s\n", path, strerror(errno));
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
        fprintf(stderr, "Error: writing header to '%s' failed: %s\n", path, strerror(errno));
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }

    size_t n_elems = 0;
    /*   Branch — guard or special-case. */
    if (mul_size_t(M->rows, M->cols, &n_elems))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: rows*cols overflow on write\n");
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return -1;
    }

    size_t wrote = /*   I/O — fwrite call. */
        fwrite(M->data, sizeof(double), n_elems, fp);
    /*   Branch — guard or special-case. */
    if (wrote != n_elems)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: short write to '%s': expected %zu doubles, wrote %zu: %s\n",
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
fprintf(stderr, "Warning: /*   I/O — fclose call. */
fclose('%s') failed: %s\n", path, strerror(errno));
    }
    /*   Epilogue — return from function. */
    return 0;
}

/* ---------------- main (with timing) ---------------- */

/*   Function begins — explain parameters, side effects, and return. */
int main(int argc, char **argv)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    /*   Branch — guard or special-case. */
    if (argc != 4)
    {
        usage(argv[0]);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    const double t_start = now_sec();

    const char *pathA = argv[1];
    const char *pathB = argv[2];
    const char *pathC = argv[3];

    Matrix A = {0}, B = {0}, C = {0};

    /* ----- read timing ----- */
    const double t_read_start = now_sec();

    /*   Branch — guard or special-case. */
    if (read_matrix(pathA, &A) != 0)
    {
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
    /*   Branch — guard or special-case. */
    if (read_matrix(pathB, &B) != 0)
    {
        /*   Memory — free. */
        free(A.block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    const double t_after_read = now_sec();
    const double read_s = t_after_read - t_read_start;

    /* Dim checks */
    /*   Branch — guard or special-case. */
    if (B.cols != 1)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: Input B must be n x 1, but is %zu x %zu\n", B.rows, B.cols);
        /*   Memory — free. */
        free(A.block);
        /*   Memory — free. */
        free(B.block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
    /*   Branch — guard or special-case. */
    if (A.cols != B.rows)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: Dimension mismatch: A=%zu x %zu, B=%zu x %zu (need A.cols==B.rows)\n",
                A.rows, A.cols, B.rows, B.cols);
        /*   Memory — free. */
        free(A.block);
        /*   Memory — free. */
        free(B.block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Allocate C: m x 1 with one /*   Memory — malloc. */
    malloc() * /
        C.rows = A.rows;
    C.cols = 1;

    size_t ptrs_bytes = 0, n_elems_C = 0, payload_bytes = 0, total_bytes = 0;
    /*   Branch — guard or special-case. */
    if (mul_size_t(C.rows, sizeof(double *), &ptrs_bytes) ||
        mul_size_t(C.rows, C.cols, &n_elems_C) ||
        mul_size_t(n_elems_C, sizeof(double), &payload_bytes) ||
        add_size_t(ptrs_bytes, payload_bytes, &total_bytes))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: overflow sizing C\n");
        /*   Memory — free. */
        free(A.block);
        /*   Memory — free. */
        free(B.block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    C.block = /*   Memory — malloc. */
        malloc(total_bytes);
    /*   Branch — guard or special-case. */
    if (!C.block)
    {
        /*   I/O — fprintf call. */
fprintf(stderr, "Error: /*   Memory — malloc. */
malloc(%zu) for C failed: %s\n", total_bytes, strerror(errno));
        /*   Memory — free. */
free(A.block);
        /*   Memory — free. */
free(B.block);
        /*   Epilogue — return from function. */
return EXIT_FAILURE;
    }

    C.row = (double **)C.block;
    C.data = (double *)((unsigned char *)C.block + ptrs_bytes);
    /*   Loop — iterate over range. */
    for (size_t r = 0; r < C.rows; ++r)
    {
        C.row[r] = C.data + r * C.cols; /* cols == 1 */
    }

    /* ----- compute timing ----- */
    const double t_compute_start = now_sec();

    /* C = A * B (O(m*n)) */
    const size_t m = A.rows;
    const size_t n = A.cols; /* == B.rows */
    /*   Loop — iterate over range. */
    for (size_t i = 0; i < m; ++i)
    {
        const double *Ai = A.row[i];
        double sum = 0.0;
        /*   Loop — iterate over range. */
        for (size_t k = 0; k < n; ++k)
        {
            sum += Ai[k] * B.row[k][0]; /* B is n x 1 */
        }
        C.row[i][0] = sum;
    }

    const double t_after_compute = now_sec();
    const double compute_s = t_after_compute - t_compute_start;

    /* ----- write timing ----- */
    const double t_write_start = now_sec();

    /*   Branch — guard or special-case. */
    if (write_matrix(pathC, &C) != 0)
    {
        /*   Memory — free. */
        free(A.block);
        /*   Memory — free. */
        free(B.block);
        /*   Memory — free. */
        free(C.block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    const double t_after_write = now_sec();
    const double write_s = t_after_write - t_write_start;

    /* Totals */
    const double total_s = now_sec() - t_start;

    /* Machine-readable one-liner for scripts */
    /*   I/O — printf call. */
    printf("TIMING total_s=%.9f read_s=%.9f compute_s=%.9f write_s=%.9f m=%zu n=%zu\n",
           total_s, read_s, compute_s, write_s, m, n);

    /* Human-readable breakdown */
    /*   I/O — fprintf call. */
    fprintf(stdout,
            "Matrix-Vector Multiply: A(%zu x %zu) * B(%zu x %zu) -> C(%zu x %zu)\n"
            "Elapsed times (seconds):\n"
            "  read:    %.9f\n"
            "  compute: %.9f\n"
            "  write:   %.9f\n"
            "  total:   %.9f\n",
            A.rows, A.cols, B.rows, B.cols, C.rows, C.cols,
            read_s, compute_s, write_s, total_s);

    /*   Memory — free. */
    free(A.block);
    /*   Memory — free. */
    free(B.block);
    /*   Memory — free. */
    free(C.block);
    /*   Epilogue — return from function. */
    return EXIT_SUCCESS;
}
