<<<<<<< HEAD
/*
params
pth-stencil-2d -n <iters> -I <in.raw> -o <out.raw> [-s <stack.raw>] -t <threads>
  -n ITERS      Number of iterations (time steps)
  -I FILE       Input grid (.raw) header+data (int rows, int cols, doubles)
  -o FILE       Output final grid (.raw) header+data
  -s FILE       (optional) Raw stack output file (writes header + all frames)
  -t NTHREADS   Number of pthreads (>=1)
  -h

*/
=======
// pth-stencil-2d.c
// Parallel (pthreads) 2D 9-point stencil with fixed boundaries.
// Format for .dat files: [int32 rows][int32 cols][rows*cols doubles] (row-major)
//
// CLI:
//   pth-stencil-2d -n <iters> -I <in.dat> -o <out.dat> -t <threads> [-s <stack.dat>]
//
// Notes:
// - The optional -s stack file is written with the same .dat format (header + frames).
//   It contains (iters + 1) frames: the initial field, then after each iteration.
// - The 9-point average uses the order: NW, N, NE, E, SE, S, SW, W, C (then / 9.0).
// - Boundaries (top/bottom/left/right) are held fixed each iteration.
//
// Requires: utilities.h / utilities.c providing read_header() and write_header().

#define _POSIX_C_SOURCE 200112L
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>
#include <pthread.h>
#include "utilities.h"

typedef struct
{
    int R, C;
    int iters;
    int num_threads;
    double *A;                 // current
    double *B;                 // next
    pthread_barrier_t barrier; // main participates (threads + 1)
    // Per-thread block partition
    int *row_start; // inclusive, in [1, R-2]
    int *row_end;   // inclusive, in [1, R-2]
} shared_t;

typedef struct
{
    shared_t *sh;
    int tid;
} thread_arg_t;

static void usage(const char *prog)
{
    fprintf(stderr, "Usage: ./pth-stencil-2d -n <iters> -I <in.raw> -o <out.raw> [-s <stack.raw>] -t <threads>",
            "-n ITERS      Number of iterations (time steps)",
            "-I FILE       Input grid (.raw) header+data (int rows, int cols, doubles)",
            "-o FILE       Output final grid (.raw) header+data",
            "-s FILE       (optional) Raw stack output file (writes header + all frames)",
            "-t NTHREADS   Number of pthreads (>=1)",
            "-h            Help", prog);
}

static void copy_boundaries(double *dst, const double *src, int R, int C)
{
    // top & bottom rows
    for (int j = 0; j < C; ++j)
    {
        dst[(size_t)0 * C + j] = src[(size_t)0 * C + j];
        dst[(size_t)(R - 1) * C + j] = src[(size_t)(R - 1) * C + j];
    }
    // left & right cols
    for (int i = 0; i < R; ++i)
    {
        dst[(size_t)i * C + 0] = src[(size_t)i * C + 0];
        dst[(size_t)i * C + (C - 1)] = src[(size_t)i * C + (C - 1)];
    }
}

static void *worker(void *arg)
{
    thread_arg_t *ta = (thread_arg_t *)arg;
    shared_t *sh = ta->sh;
    const int tid = ta->tid;

    const int R = sh->R;
    const int C = sh->C;

    const int rs = sh->row_start[tid];
    const int re = sh->row_end[tid];

    // Threads compute interior rows [rs..re], cols [1..C-2] into B from A.
    // After each iteration's compute, they wait for main to do boundaries/swap/write,
    // then wait again for main to signal next iteration.
    for (int t = 0; t < sh->iters; ++t)
    {
        const double *A = sh->A;
        double *B = sh->B;

        for (int i = rs; i <= re; ++i)
        {
            const size_t iC = (size_t)i * C;
            const size_t ip1C = (size_t)(i + 1) * C;
            const size_t im1C = (size_t)(i - 1) * C;
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

        // First barrier: signal compute done; main will copy boundaries, swap, write.
        pthread_barrier_wait(&sh->barrier);

        // Second barrier: wait for main to finish the boundary/cycle work.
        pthread_barrier_wait(&sh->barrier);
    }
    return NULL;
}

int main(int argc, char **argv)
{
    int iters = -1;
    const char *inpath = NULL;
    const char *outpath = NULL;
    const char *stackpath = NULL; // optional
    int num_threads = 0;

    // Simple flag parser
    for (int i = 1; i < argc; ++i)
    {
        if (!strcmp(argv[i], "-n") && i + 1 < argc)
        {
            iters = atoi(argv[++i]);
        }
        else if (!strcmp(argv[i], "-I") && i + 1 < argc)
        {
            inpath = argv[++i];
        }
        else if (!strcmp(argv[i], "-o") && i + 1 < argc)
        {
            outpath = argv[++i];
        }
        else if (!strcmp(argv[i], "-s") && i + 1 < argc)
        {
            stackpath = argv[++i];
        }
        else if (!strcmp(argv[i], "-t") && i + 1 < argc)
        {
            num_threads = atoi(argv[++i]);
        }
        else
        {
            usage(argv[0]);
            return 1;
        }
    }

    if (iters < 0 || !inpath || !outpath || num_threads < 1)
    {
        usage(argv[0]);
        return 1;
    }

    // Open input and read header + data
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
    const int R = rows32, C = cols32;
    const size_t N = (size_t)R * (size_t)C;

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

    // Optional stack file (header + frames). If provided, write initial frame first.
    FILE *fstack = NULL;
    if (stackpath)
    {
        fstack = fopen(stackpath, "wb");
        if (!fstack)
        {
            perror("open stack");
            free(A);
            free(B);
            return 1;
        }
        if (write_header(fstack, rows32, cols32) != 0 ||
            fwrite(A, sizeof(double), N, fstack) != N)
        {
            fprintf(stderr, "Error: writing initial frame to %s\n", stackpath);
            fclose(fstack);
            free(A);
            free(B);
            return 1;
        }
    }

    // Prepare shared state and partition rows among threads
    shared_t sh;
    sh.R = R;
    sh.C = C;
    sh.iters = iters;
    sh.num_threads = num_threads;
    sh.A = A;
    sh.B = B;

    if (pthread_barrier_init(&sh.barrier, NULL, (unsigned)(num_threads + 1)) != 0)
    {
        fprintf(stderr, "pthread_barrier_init failed\n");
        if (fstack)
            fclose(fstack);
        free(A);
        free(B);
        return 1;
    }

    sh.row_start = (int *)malloc((size_t)num_threads * sizeof(int));
    sh.row_end = (int *)malloc((size_t)num_threads * sizeof(int));
    if (!sh.row_start || !sh.row_end)
    {
        fprintf(stderr, "malloc failed\n");
        if (fstack)
            fclose(fstack);
        pthread_barrier_destroy(&sh.barrier);
        free(sh.row_start);
        free(sh.row_end);
        free(A);
        free(B);
        return 1;
    }

    // Interior rows are [1 .. R-2]
    int interior = (R >= 3) ? (R - 2) : 0;
    if (interior < 0)
        interior = 0;
    if (interior == 0 || C < 2)
    {
        // Degenerate: no interior to update; just write out final (copy boundaries only)
        FILE *fout = fopen(outpath, "wb");
        if (!fout)
        {
            perror("open out");
            if (fstack)
                fclose(fstack);
            pthread_barrier_destroy(&sh.barrier);
            free(sh.row_start);
            free(sh.row_end);
            free(A);
            free(B);
            return 1;
        }
        if (write_header(fout, rows32, cols32) != 0 || fwrite(A, sizeof(double), N, fout) != N)
        {
            fprintf(stderr, "Error: writing final %s\n", outpath);
            fclose(fout);
            if (fstack)
                fclose(fstack);
            pthread_barrier_destroy(&sh.barrier);
            free(sh.row_start);
            free(sh.row_end);
            free(A);
            free(B);
            return 1;
        }
        fclose(fout);
        if (fstack)
            fclose(fstack);
        pthread_barrier_destroy(&sh.barrier);
        free(sh.row_start);
        free(sh.row_end);
        free(A);
        free(B);
        return 0;
    }

    // Static block partition
    int base = interior / num_threads;
    int rem = interior % num_threads;
    int cur = 1; // first interior row index
    for (int t = 0; t < num_threads; ++t)
    {
        int take = base + (t < rem ? 1 : 0);
        if (take <= 0)
        {
            sh.row_start[t] = 1;
            sh.row_end[t] = 0; // empty
        }
        else
        {
            sh.row_start[t] = cur;
            sh.row_end[t] = cur + take - 1;
            cur += take;
        }
    }

    // Spawn threads
    pthread_t *threads = (pthread_t *)malloc((size_t)num_threads * sizeof(pthread_t));
    thread_arg_t *targs = (thread_arg_t *)malloc((size_t)num_threads * sizeof(thread_arg_t));
    if (!threads || !targs)
    {
        fprintf(stderr, "malloc failed\n");
        if (fstack)
            fclose(fstack);
        pthread_barrier_destroy(&sh.barrier);
        free(sh.row_start);
        free(sh.row_end);
        free(threads);
        free(targs);
        free(A);
        free(B);
        return 1;
    }
    for (int t = 0; t < num_threads; ++t)
    {
        targs[t].sh = &sh;
        targs[t].tid = t;
        if (pthread_create(&threads[t], NULL, worker, &targs[t]) != 0)
        {
            fprintf(stderr, "pthread_create failed for thread %d\n", t);
            if (fstack)
                fclose(fstack);
            pthread_barrier_destroy(&sh.barrier);
            free(sh.row_start);
            free(sh.row_end);
            free(threads);
            free(targs);
            free(A);
            free(B);
            return 1;
        }
    }

    // Main participates in a double-barrier scheme per iteration:
    // 1) Wait for all threads to finish computing B's interior from A.
    // 2) Copy boundaries from A to B; swap A<->B; write stack frame if requested.
    // 3) Release threads for next iteration.
    for (int t = 0; t < iters; ++t)
    {
        // Wait for workers to finish compute
        pthread_barrier_wait(&sh.barrier);

        // Copy boundaries A->B for this timestep
        copy_boundaries(sh.B, sh.A, R, C);

        // Swap A<->B
        double *tmp = sh.A;
        sh.A = sh.B;
        sh.B = tmp;

        // Write stack frame after iteration, if requested
        if (fstack)
        {
            if (fwrite(sh.A, sizeof(double), N, fstack) != N)
            {
                fprintf(stderr, "Error: writing stack frame %d to %s\n", t + 1, stackpath);
                // Clean exit
                fclose(fstack);
                // Signal threads to leave (still release barrier)
                pthread_barrier_wait(&sh.barrier);
                // Join and cleanup
                for (int k = 0; k < num_threads; ++k)
                    pthread_join(threads[k], NULL);
                pthread_barrier_destroy(&sh.barrier);
                free(sh.row_start);
                free(sh.row_end);
                free(threads);
                free(targs);
                free(sh.A);
                free(sh.B);
                return 1;
            }
        }

        // Release threads to proceed to next iteration
        pthread_barrier_wait(&sh.barrier);
    }

    // Join workers
    for (int t = 0; t < num_threads; ++t)
    {
        pthread_join(threads[t], NULL);
    }

    // Write final output
    FILE *fout = fopen(outpath, "wb");
    if (!fout)
    {
        perror("open out");
        if (fstack)
            fclose(fstack);
        pthread_barrier_destroy(&sh.barrier);
        free(sh.row_start);
        free(sh.row_end);
        free(threads);
        free(targs);
        free(sh.A);
        free(sh.B);
        return 1;
    }

    if (write_header(fout, rows32, cols32) != 0 ||
        fwrite(sh.A, sizeof(double), N, fout) != N)
    {
        fprintf(stderr, "Error: writing final %s\n", outpath);
        fclose(fout);
        if (fstack)
            fclose(fstack);
        pthread_barrier_destroy(&sh.barrier);
        free(sh.row_start);
        free(sh.row_end);
        free(threads);
        free(targs);
        free(sh.A);
        free(sh.B);
        return 1;
    }
    fclose(fout);

    if (fstack)
        fclose(fstack);

    // Cleanup
    pthread_barrier_destroy(&sh.barrier);
    free(sh.row_start);
    free(sh.row_end);
    free(threads);
    free(targs);
    free(sh.A);
    free(sh.B);

    return 0;
}
>>>>>>> 1597a5aa940e3c5dde53dc8ea972ba9146e3ffb4
