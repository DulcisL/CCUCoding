// stencil_headered.c
// Reads: [int32 rows][int32 cols][rows*cols doubles] in row-major order.
// Performs 3x3 (including center) average stencil on interior; boundaries fixed.
// Writes the same header + updated matrix to output.
//
// Usage: ./stencil_headered input.bin output.bin [iterations]

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <input.bin> <output.bin> [iterations]\n", argv[0]);
        return 1;
    }
    int iterations = 1;
    if (argc >= 4) {
        iterations = atoi(argv[3]);
        if (iterations < 0) iterations = 0;
    }

    FILE *fin = fopen(argv[1], "rb");
    if (!fin) { perror("open input"); return 1; }

    int32_t rows32, cols32;
    if (fread(&rows32, sizeof(int32_t), 1, fin) != 1 ||
        fread(&cols32, sizeof(int32_t), 1, fin) != 1) {
        fprintf(stderr, "Error: could not read rows/cols header\n");
        fclose(fin);
        return 1;
    }
    if (rows32 <= 0 || cols32 <= 0) {
        fprintf(stderr, "Error: invalid header dimensions: %d x %d\n", rows32, cols32);
        fclose(fin);
        return 1;
    }

    const int R = rows32;
    const int C = cols32;
    const size_t n = (size_t)R * (size_t)C;

    double *A = (double*)malloc(n * sizeof(double));
    double *B = (double*)malloc(n * sizeof(double));
    if (!A || !B) {
        fprintf(stderr, "Error: malloc failed for %zu doubles\n", n);
        fclose(fin);
        free(A); free(B);
        return 1;
    }

    if (fread(A, sizeof(double), n, fin) != n) {
        fprintf(stderr, "Error: could not read %zu doubles of matrix data\n", n);
        fclose(fin);
        free(A); free(B);
        return 1;
    }
    fclose(fin);

    // Stencil (interior only). Keep boundaries fixed each iteration.
    // If grid is too small for a 3x3 interior, skip updates.
    if (R >= 3 && C >= 3 && iterations > 0) {
        for (int t = 0; t < iterations; ++t) {
            // interior update
            for (int i = 1; i < R - 1; ++i) {
                for (int j = 1; j < C - 1; ++j) {
                    size_t ij = (size_t)i * C + j;
                    double sum =
                        A[(size_t)(i-1)*C + (j-1)] + A[(size_t)(i-1)*C + j] + A[(size_t)(i-1)*C + (j+1)] +
                        A[(size_t)i*C     + (j-1)] + A[(size_t)i*C     + j] + A[(size_t)i*C     + (j+1)] +
                        A[(size_t)(i+1)*C + (j-1)] + A[(size_t)(i+1)*C + j] + A[(size_t)(i+1)*C + (j+1)];
                    B[ij] = sum / 9.0;
                }
            }

            // copy boundaries unchanged from A -> B
            for (int j = 0; j < C; ++j) {
                B[(size_t)0*C + j]     = A[(size_t)0*C + j];        // top
                B[(size_t)(R-1)*C + j] = A[(size_t)(R-1)*C + j];    // bottom
            }
            for (int i = 0; i < R; ++i) {
                B[(size_t)i*C + 0]     = A[(size_t)i*C + 0];        // left
                B[(size_t)i*C + (C-1)] = A[(size_t)i*C + (C-1)];    // right
            }

            // swap A <-> B (no utility function; manual pointer swap)
            double *tmp = A; A = B; B = tmp;
        }
    }

    FILE *fout = fopen(argv[2], "wb");
    if (!fout) { perror("open output"); free(A); free(B); return 1; }
    if (fwrite(&rows32, sizeof(int32_t), 1, fout) != 1 ||
        fwrite(&cols32, sizeof(int32_t), 1, fout) != 1) {
        fprintf(stderr, "Error: failed to write header to output\n");
        fclose(fout); free(A); free(B); return 1;
    }
    if (fwrite(A, sizeof(double), n, fout) != n) {
        fprintf(stderr, "Error: failed to write %zu doubles to output\n", n);
        fclose(fout); free(A); free(B); return 1;
    }
    fclose(fout);

    // Brief confirmation (no extra utilities)
    fprintf(stdout, "Stencil complete: %d x %d, %d iteration(s), wrote %s\n",
            R, C, iterations, argv[2]);

    free(A);
    free(B);
    return 0;
}
