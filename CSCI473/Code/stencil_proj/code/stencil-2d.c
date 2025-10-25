// stencil-2d.c
// Usage: ./stencil-2d <input.dat> <final.dat> <iterations>
// Inputs/Outputs format: [int32 rows][int32 cols][rows*cols doubles]
// Writes (in current working directory, e.g., ./data):
//   - <final.dat>              final plate
//   - all.<R>x<C>x<I>.dat      stack (I+1 frames: initial + after each iteration)

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include "utilities.h"
#include "timer.h"

static void usage(const char *prog)
{
    fprintf(stderr, "Usage: %s <input.dat> <final.dat> <iterations>\n", prog);
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

    // Open stack file in current dir (run from ./data)
    char stack_name[128];
    snprintf(stack_name, sizeof(stack_name), "all.%dx%dx%d.dat", R, C, iterations);
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

    // Write initial frame (BEFORE any iteration)
    if (fwrite(A, sizeof(double), N, stack) != N)
    {
        fprintf(stderr, "Error writing initial frame\n");
        fclose(stack);
        free(A);
        free(B);
        return 1;
    }

    double t0, t1;
    GET_TIME(t0);

    for (int t = 0; t < iterations; ++t)
    {
        // Interior update with the requested order:
        // (NW + N + NE + E + SE + S + SW + W + C) / 9.0
        for (int i = 1; i < R - 1; ++i)
        {
            for (int j = 1; j < C - 1; ++j)
            {
                // indices for readability
                size_t iC = (size_t)i * C;
                size_t ip1C = (size_t)(i + 1) * C;
                size_t im1C = (size_t)(i - 1) * C;

                double sum = (A[im1C + (j - 1)] + A[im1C + j] + A[im1C + (j + 1)] + A[iC + (j + 1)] + A[ip1C + (j + 1)] + A[ip1C + j] + A[ip1C + (j - 1)] + A[iC + (j - 1)] + A[iC + j]) / 9;
                B[iC + j] = sum;
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

        // write post-iteration frame
        if (fwrite(A, sizeof(double), N, stack) != N)
        {
            fprintf(stderr, "Error writing frame %d\n", t + 1);
            fclose(stack);
            free(A);
            free(B);
            return 1;
        }
    }

    GET_TIME(t1);
    fclose(stack);

    // Write final output
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

    printf("Stencil kernel time: %e seconds\n", (t1 - t0));
    printf("Wrote %s and %s\n", finalpath, stack_name);

    free(A);
    free(B);
    return 0;
}
