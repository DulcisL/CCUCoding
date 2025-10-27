// stencil-2d.c
// Usage: ./stencil-2d <input.dat> <final.dat> <iterations>
// Format for all .dat files: [int32 rows][int32 cols][rows*cols doubles] (row-major)
//
// This version measures timings and appends a row to timings.csv in the CWD:
//
// CSV columns:
// rows,cols,iterations,input,final,stack,read_s,compute_s,write_s,overall_s
//
// Notes:
// - Run this from ./data so outputs + timings.csv live in Stencil_proj/data
// - Compute uses 9-point average in order: NW, N, NE, E, SE, S, SW, W, C

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>

#include "utilities.h"
#include "timer.h"

static void usage(const char *prog)
{
    fprintf(stderr, "Usage: %s <input.dat> <final.dat> <iterations>\n", prog);
}

static int file_exists(const char *path)
{
    FILE *f = fopen(path, "rb");
    if (!f)
        return 0;
    fclose(f);
    return 1;
}

static int append_timings_csv(const char *csv_path,
                              int rows, int cols, int iters,
                              const char *inpath, const char *finalpath, const char *stackname,
                              double read_s, double compute_s, double write_s, double overall_s)
{
    int need_header = !file_exists(csv_path);

    FILE *f = fopen(csv_path, "a");
    if (!f)
    {
        fprintf(stderr, "Error: cannot open %s for append: %s\n", csv_path, strerror(errno));
        return -1;
    }

    if (need_header)
    {
        fprintf(f, "rows,cols,iterations,input,final,stack,read_s,compute_s,write_s,overall_s\n");
    }

    // CSV-escape not needed for our simple names, but keep them plain.
    fprintf(f, "%d,%d,%d,%s,%s,%s,%.9e,%.9e,%.9e,%.9e\n",
            rows, cols, iters, inpath, finalpath, stackname,
            read_s, compute_s, write_s, overall_s);

    fclose(f);
    return 0;
}

int main(int argc, char **argv)
{
    if (argc < 4)
    {
        usage(argv[0]);
        return 1;
    }

    const char *inpath = argv[1];
    const char *finalpath = argv[2];
    int iterations = atoi(argv[3]);
    if (iterations < 0)
    {
        usage(argv[0]);
        return 1;
    }

    // Timing accumulators
    double t_overall0, t_overall1;
    double t_read0, t_read1, read_s = 0.0;
    double t_compute0, t_compute1, compute_s = 0.0;
    double t_write0, t_write1, write_s = 0.0;

    GET_TIME(t_overall0);

    // ---------------- READ ----------------
    GET_TIME(t_read0);
    FILE *fin = fopen(inpath, "rb");
    if (!fin)
    {
        perror("open input");
        return 1;
    }

    int32_t rows32, cols32;
    if (read_header(fin, &rows32, &cols32) != 0 || rows32 <= 0 || cols32 <= 0)
    {
        fprintf(stderr, "Error: bad header in %s\n", inpath);
        fclose(fin);
        return 1;
    }
    int R = rows32, C = cols32;
    size_t N = (size_t)R * (size_t)C;

    double *A = (double *)malloc(N * sizeof(double));
    double *B = (double *)malloc(N * sizeof(double));
    if (!A || !B)
    {
        fprintf(stderr, "malloc failed\n");
        fclose(fin);
        free(A);
        free(B);
        return 1;
    }

    if (fread(A, sizeof(double), N, fin) != N)
    {
        fprintf(stderr, "Error: could not read matrix data from %s\n", inpath);
        fclose(fin);
        free(A);
        free(B);
        return 1;
    }
    fclose(fin);
    GET_TIME(t_read1);
    read_s += (t_read1 - t_read0);

    // ---------------- OPEN STACK (WRITE) ----------------
    char stack_name[128];
    snprintf(stack_name, sizeof(stack_name), "all.%dx%dx%d.dat", R, C, iterations);

    GET_TIME(t_write0);
    FILE *stack = fopen(stack_name, "wb");
    if (!stack)
    {
        perror("open stack");
        free(A);
        free(B);
        return 1;
    }
    if (write_header(stack, rows32, cols32) != 0)
    {
        fprintf(stderr, "write header failed\n");
        fclose(stack);
        free(A);
        free(B);
        return 1;
    }
    // Write initial frame BEFORE any iteration
    if (fwrite(A, sizeof(double), N, stack) != N)
    {
        fprintf(stderr, "Error writing initial frame\n");
        fclose(stack);
        free(A);
        free(B);
        return 1;
    }
    GET_TIME(t_write1);
    write_s += (t_write1 - t_write0);

    // ---------------- COMPUTE ----------------
    GET_TIME(t_compute0);
    for (int t = 0; t < iterations; ++t)
    {
        for (int i = 1; i < R - 1; ++i)
        {
            size_t iC = (size_t)i * C;
            size_t ip1C = (size_t)(i + 1) * C;
            size_t im1C = (size_t)(i - 1) * C;

            for (int j = 1; j < C - 1; ++j)
            {
                double sum =
                    A[im1C + (j - 1)] + // NW
                    A[im1C + j] +       // N
                    A[im1C + (j + 1)] + // NE
                    A[iC + (j + 1)] +   // E
                    A[ip1C + (j + 1)] + // SE
                    A[ip1C + j] +       // S
                    A[ip1C + (j - 1)] + // SW
                    A[iC + (j - 1)] +   // W
                    A[iC + j];          // C

                B[iC + j] = sum / 9.0;
            }
        }
        // boundaries unchanged
        for (int j = 0; j < C; ++j)
        {
            B[(size_t)0 * C + j] = A[(size_t)0 * C + j];
            B[(size_t)(R - 1) * C + j] = A[(size_t)(R - 1) * C + j];
        }
        for (int i = 0; i < R; ++i)
        {
            B[(size_t)i * C + 0] = A[(size_t)i * C + 0];
            B[(size_t)i * C + (C - 1)] = A[(size_t)i * C + (C - 1)];
        }

        // swap
        double *tmp = A;
        A = B;
        B = tmp;

        // write post-iteration frame (WRITE)
        GET_TIME(t_write0);
        if (fwrite(A, sizeof(double), N, stack) != N)
        {
            fprintf(stderr, "Error writing frame %d\n", t + 1);
            fclose(stack);
            free(A);
            free(B);
            return 1;
        }
        GET_TIME(t_write1);
        write_s += (t_write1 - t_write0);
    }
    GET_TIME(t_compute1);
    compute_s += (t_compute1 - t_compute0);

    // Close stack
    // (No need to time fclose separately; negligible)
    fclose(stack);

    // ---------------- WRITE FINAL ----------------
    GET_TIME(t_write0);
    FILE *fout = fopen(finalpath, "wb");
    if (!fout)
    {
        perror("open final");
        free(A);
        free(B);
        return 1;
    }
    if (write_header(fout, rows32, cols32) != 0 || fwrite(A, sizeof(double), N, fout) != N)
    {
        fprintf(stderr, "Error writing %s\n", finalpath);
        fclose(fout);
        free(A);
        free(B);
        return 1;
    }
    fclose(fout);
    GET_TIME(t_write1);
    write_s += (t_write1 - t_write0);

    GET_TIME(t_overall1);
    double overall_s = (t_overall1 - t_overall0);

    // ---------------- REPORT ----------------
    printf("Read time   : %e s\n", read_s);
    printf("Compute time: %e s\n", compute_s);
    printf("Write time  : %e s\n", write_s);
    printf("Overall time: %e s\n", overall_s);
    printf("Wrote %s and %s\n", finalpath, stack_name);

    // ---------------- CSV APPEND ----------------
    // Write timings.csv in current directory (./data if run there)
    const char *csv_name = "timings.csv";
    if (append_timings_csv(csv_name, R, C, iterations, inpath, finalpath, stack_name,
                           read_s, compute_s, write_s, overall_s) != 0)
    {
        fprintf(stderr, "Warning: failed to append timings to %s\n", csv_name);
    }
    else
    {
        printf("Appended timings to %s\n", csv_name);
    }

    free(A);
    free(B);
    return 0;
}
