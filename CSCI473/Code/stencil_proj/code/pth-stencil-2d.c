#define _POSIX_C_SOURCE 200112L
/*
  File: pth-stencil-2d.c
  Desc: Parallel 2D stencil solver using POSIX threads.
        Reads an initial grid from a .dat file, performs a number of
        iterations of a 9-point stencil, optionally records all frames,
        and writes the final grid. Times read/compute/write phases and
        appends them to ../data/timings_pth.csv.

  Variables:
    n_iters (int)        - Number of iterations to apply.
    in_file (char*)      - Path to input .dat file.
    out_file (char*)     - Path to output .dat file.
    num_threads (int)    - Number of pthread workers to launch.
    rows/cols (int)      - Grid dimensions.
    g_curr, g_next       - Global pointers to current and next grids.
    barrier (pthread_barrier_t)
                         - Barrier used to synchronize threads each iteration.

  Returns:
    int - 0 on success, non-zero on error.
*/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <limits.h>
#include <errno.h>
#include <pthread.h>
#include <sys/time.h>

#include "utilities.h"
#include "timer.h"

#define MAX_PATH 256

/* ---------- Global shared data for threads ---------- */

static double *g_curr = NULL;      /* Current grid */
static double *g_next = NULL;      /* Next grid */
static int g_rows = 0;             /* Grid rows */
static int g_cols = 0;             /* Grid cols */
static int g_iters = 0;            /* Number of iterations */
static int g_num_threads = 1;      /* Number of threads */
static int g_stack_enabled = 0;    /* Whether to write stack */
static FILE *g_stack_fp = NULL;    /* Stack output file handle */
static int g_stack_error = 0;      /* Flag if stack write failed */
static pthread_barrier_t barrier;  /* Barrier for all threads */

/* ---------- Per-thread metadata ---------- */

typedef struct
{
    int id;        /* Thread ID [0..g_num_threads-1] */
    int start_row; /* First interior row this thread owns (1..N-2) */
    int end_row;   /* Last interior row this thread owns (1..N-2) */
} ThreadData;

/* ---------- Timing helper ---------- */

static double now_sec(void)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}

/* ---------- Usage ---------- */

static void print_usage(const char *prog)
{
    fprintf(stderr,
            "Usage: %s -n <iters> -I <in.dat> -o <out.dat> [-s <stack.raw>] -t <threads>\n",
            prog);
}

/* ---------- Worker thread function ---------- */
/*
  Function: stencil_worker
  Desc: Each thread applies the 5-point stencil to its assigned rows
        for g_iters iterations. Synchronizes with other threads via
        a barrier, and thread 0 swaps the buffers after each iteration.

  Variables:
    arg (ThreadData*) - Pointer to per-thread metadata:
      id (int)        - Thread ID.
      start_row (int) - First interior row to update.
      end_row (int)   - Last interior row to update.

  Returns:
    void* - Always NULL (pthread convention).
*/
static void *stencil_worker(void *arg)
{
    ThreadData *td = (ThreadData *)arg;
    int tid = td->id;
    int start = td->start_row;
    int end = td->end_row;
    const int rows = g_rows;
    const int cols = g_cols;

    for (int it = 0; it < g_iters; ++it)
    {
        /* Update interior region for this thread's rows */
        if (start <= end && cols >= 3)
        {
            for (int i = start; i <= end; ++i)
            {
                size_t row_idx = (size_t)i * (size_t)cols;
                size_t north_idx = row_idx - (size_t)cols;
                size_t south_idx = row_idx + (size_t)cols;

                for (int j = 1; j < cols - 1; ++j)
                {
                    /* 9-point stencil: NW, N, NE, E, SE, S, SW, W, C */
                    double sum =
                        g_curr[north_idx + (size_t)(j - 1)] +
                        g_curr[north_idx + (size_t)j] +
                        g_curr[north_idx + (size_t)(j + 1)] +
                        g_curr[row_idx + (size_t)(j + 1)] +
                        g_curr[south_idx + (size_t)(j + 1)] +
                        g_curr[south_idx + (size_t)j] +
                        g_curr[south_idx + (size_t)(j - 1)] +
                        g_curr[row_idx + (size_t)(j - 1)] +
                        g_curr[row_idx + (size_t)j];

                    g_next[row_idx + (size_t)j] = sum / 9.0;
                }
            }
        }

        /* Preserve left/right boundaries for rows handled by this thread */
        if (start <= end)
        {
            for (int i = start; i <= end; ++i)
            {
                size_t row_idx = (size_t)i * (size_t)cols;
                g_next[row_idx] = g_curr[row_idx];
                g_next[row_idx + (size_t)(cols - 1)] = g_curr[row_idx + (size_t)(cols - 1)];
            }
        }

        /* Wait for all threads to finish this iteration's updates */
        pthread_barrier_wait(&barrier);

        /* Thread 0 swaps the buffers and handles stack I/O + top/bottom boundaries */
        if (tid == 0)
        {
            /* Copy top and bottom boundaries unchanged */
            memcpy(g_next, g_curr, (size_t)cols * sizeof(double));
            memcpy(g_next + (size_t)(rows - 1) * (size_t)cols,
                   g_curr + (size_t)(rows - 1) * (size_t)cols,
                   (size_t)cols * sizeof(double));

            double *tmp = g_curr;
            g_curr = g_next;
            g_next = tmp;

            if (g_stack_enabled && g_stack_fp && !g_stack_error)
            {
                size_t frame_elems = (size_t)rows * (size_t)cols;
                if (fwrite(g_curr, sizeof(double), frame_elems, g_stack_fp) != frame_elems)
                {
                    fprintf(stderr, "Error writing stack frame %d: %s\n", it + 1, strerror(errno));
                    g_stack_error = 1;
                }
            }
        }

        /* Ensure all threads see the swapped pointers before next iter */
        pthread_barrier_wait(&barrier);
    }

    return NULL;
}

/* ---------- Main ---------- */
/*
  Function: main
  Desc: Parses arguments, reads input grid, spawns threads, performs
        stencil iterations, writes output, and logs timing.

  Variables:
    argc (int)    - Command-line argument count.
    argv (char**) - Command-line arguments.

  Returns:
    int - 0 on success, non-zero on failure.
*/
int main(int argc, char *argv[])
{
    int n_iters = 0;
    int num_threads = 0;
    char in_file[MAX_PATH] = "../data/initial.dat";
    char out_file[MAX_PATH] = "../data/final.dat";
    char stack_file[MAX_PATH] = "";
    int have_stack = 0;

    /* --- Parse arguments --- */
    for (int i = 1; i < argc; ++i)
    {
        if (strcmp(argv[i], "-n") == 0 && i + 1 < argc)
        {
            n_iters = atoi(argv[++i]);
        }
        else if (strcmp(argv[i], "-I") == 0 && i + 1 < argc)
        {
            strncpy(in_file, argv[++i], MAX_PATH);
            in_file[MAX_PATH - 1] = '\0';
        }
        else if (strcmp(argv[i], "-o") == 0 && i + 1 < argc)
        {
            strncpy(out_file, argv[++i], MAX_PATH);
            out_file[MAX_PATH - 1] = '\0';
        }
        else if (strcmp(argv[i], "-s") == 0 && i + 1 < argc)
        {
            strncpy(stack_file, argv[++i], MAX_PATH);
            stack_file[MAX_PATH - 1] = '\0';
            have_stack = 1;
        }
        else if (strcmp(argv[i], "-t") == 0 && i + 1 < argc)
        {
            num_threads = atoi(argv[++i]);
        }
        else if (strcmp(argv[i], "-h") == 0)
        {
            print_usage(argv[0]);
            return 0;
        }
        else
        {
            print_usage(argv[0]);
            return 1;
        }
    }

    if (n_iters <= 0 || num_threads <= 0)
    {
        print_usage(argv[0]);
        return 1;
    }

    g_iters = n_iters;
    g_num_threads = num_threads;

    double t_total_start = now_sec();

    /* --- Read input file --- */
    double t_read_start = now_sec();
    FILE *fin = fopen(in_file, "rb");
    if (!fin)
    {
        fprintf(stderr, "Error opening input file %s: %s\n", in_file, strerror(errno));
        return 1;
    }

    int32_t rows32 = 0, cols32 = 0;
    if (read_header(fin, &rows32, &cols32) != 0 || rows32 < 3 || cols32 < 3)
    {
        fprintf(stderr, "Error: invalid header in %s\n", in_file);
        fclose(fin);
        return 1;
    }

    g_rows = rows32;
    g_cols = cols32;
    if ((size_t)g_cols == 0 || (size_t)g_rows > SIZE_MAX / (size_t)g_cols)
    {
        fprintf(stderr, "Error: grid size too large\n");
        free(g_curr);
        free(g_next);
        return 1;
    }
    size_t total = (size_t)g_rows * (size_t)g_cols;

    g_curr = (double *)malloc(total * sizeof(double));
    g_next = (double *)malloc(total * sizeof(double));
    if (!g_curr || !g_next)
    {
        fprintf(stderr, "Error: malloc failed\n");
        fclose(fin);
        free(g_curr);
        free(g_next);
        return 1;
    }

    if (fread(g_curr, sizeof(double), total, fin) != total)
    {
        fprintf(stderr, "Error: unexpected EOF reading grid data from %s\n", in_file);
        fclose(fin);
        free(g_curr);
        free(g_next);
        return 1;
    }
    fclose(fin);
    double t_read_end = now_sec();

    /* --- Prepare stack output if requested --- */
    if (have_stack)
    {
        g_stack_fp = fopen(stack_file, "wb");
        if (!g_stack_fp)
        {
            fprintf(stderr, "Error opening stack file %s: %s\n", stack_file, strerror(errno));
            free(g_curr);
            free(g_next);
            return 1;
        }
        if (write_header(g_stack_fp, rows32, cols32) != 0)
        {
            fprintf(stderr, "Error writing stack header to %s\n", stack_file);
            fclose(g_stack_fp);
            g_stack_fp = NULL;
            free(g_curr);
            free(g_next);
            return 1;
        }
        if (fwrite(g_curr, sizeof(double), total, g_stack_fp) != total)
        {
            fprintf(stderr, "Error writing initial stack frame to %s\n", stack_file);
            fclose(g_stack_fp);
            g_stack_fp = NULL;
            free(g_curr);
            free(g_next);
            return 1;
        }
        g_stack_enabled = 1;
    }

    /* --- Initialize pthreads --- */
    pthread_t *threads = (pthread_t *)malloc(num_threads * sizeof(pthread_t));
    ThreadData *td = (ThreadData *)malloc(num_threads * sizeof(ThreadData));
    if (!threads || !td)
    {
        fprintf(stderr, "Error: malloc for threads metadata failed\n");
        if (g_stack_fp)
            fclose(g_stack_fp);
        free(g_curr);
        free(g_next);
        free(threads);
        free(td);
        return 1;
    }

    pthread_barrier_init(&barrier, NULL, num_threads);

    /* Split interior rows [1..rows-2] among threads as evenly as possible */
    int interior_rows = g_rows - 2;
    int base_rows = interior_rows / num_threads;
    int extra = interior_rows % num_threads;
    int next_row = 1; /* first interior row */

    for (int t = 0; t < num_threads; ++t)
    {
        int count = base_rows + (t < extra ? 1 : 0);
        td[t].id = t;
        if (count > 0)
        {
            td[t].start_row = next_row;
            td[t].end_row = next_row + count - 1;
            next_row = td[t].end_row + 1;
        }
        else
        {
            td[t].start_row = 1;
            td[t].end_row = 0; /* ensures loop skipped */
        }
    }

    /* --- Compute stencil --- */
    double t_comp_start = now_sec();
    int created_threads = 0;
    for (int t = 0; t < num_threads; ++t)
    {
        if (pthread_create(&threads[t], NULL, stencil_worker, &td[t]) != 0)
        {
            fprintf(stderr, "Error: pthread_create failed for thread %d\n", t);
            g_stack_error = 1;
            break;
        }
        created_threads++;
    }
    for (int t = 0; t < created_threads; ++t)
    {
        pthread_join(threads[t], NULL);
    }
    double t_comp_end = now_sec();

    pthread_barrier_destroy(&barrier);

    if (g_stack_fp)
    {
        fflush(g_stack_fp);
        fclose(g_stack_fp);
        g_stack_fp = NULL;
    }

    if (g_stack_error)
    {
        free(threads);
        free(td);
        free(g_curr);
        free(g_next);
        return 1;
    }

    /* --- Write output --- */
    double t_write_start = now_sec();
    FILE *fout = fopen(out_file, "wb");
    if (!fout)
    {
        fprintf(stderr, "Error opening output file %s: %s\n", out_file, strerror(errno));
        free(threads);
        free(td);
        free(g_curr);
        free(g_next);
        return 1;
    }

    if (write_header(fout, rows32, cols32) != 0 ||
        fwrite(g_curr, sizeof(double), total, fout) != total)
    {
        fprintf(stderr, "Error writing output file %s\n", out_file);
        fclose(fout);
        free(threads);
        free(td);
        free(g_curr);
        free(g_next);
        return 1;
    }
    fclose(fout);
    double t_write_end = now_sec();

    /* --- Timing summary --- */
    double t_total_end = now_sec();
    double t_read = t_read_end - t_read_start;
    double t_comp = t_comp_end - t_comp_start;
    double t_write = t_write_end - t_write_start;
    double t_total = t_total_end - t_total_start;

    /* Log timings to ../data/timings_pth.csv (append with header) */
    const char *timings_path = "../data/timings_pth.csv";
    int need_header = 0;
    {
        FILE *check = fopen(timings_path, "r");
        if (!check)
            need_header = 1;
        else
            fclose(check);
    }
    FILE *ft = fopen(timings_path, "a");
    if (ft)
    {
        if (need_header)
        {
            fprintf(ft, "rows,cols,iters,threads,read_s,compute_s,write_s,total_s\n");
        }
        fprintf(ft, "%d,%d,%d,%d,%.6f,%.6f,%.6f,%.6f\n",
                g_rows, g_cols, g_iters, g_num_threads, t_read, t_comp, t_write, t_total);
        fclose(ft);
    }
    else
    {
        fprintf(stderr, "Warning: could not open %s for appending: %s\n", timings_path, strerror(errno));
    }

    /* Optional console output for sanity */
    printf("pth-stencil-2d: %d x %d, iters=%d, threads=%d\n", g_rows, g_cols, g_iters, g_num_threads);
    printf("  read   = %.6f s\n", t_read);
    printf("  compute= %.6f s\n", t_comp);
    printf("  write  = %.6f s\n", t_write);
    printf("  total  = %.6f s\n", t_total);

    free(threads);
    free(td);
    free(g_curr);
    free(g_next);

    return 0;
}
