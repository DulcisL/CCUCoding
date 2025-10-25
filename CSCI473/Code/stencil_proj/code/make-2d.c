// make-2d.c
// Usage: ./make-2d <rows> <cols>
// Writes: ../data/initial.dat  (relative to ./code)
// Format: [int32 rows][int32 cols][rows*cols doubles] row-major

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <errno.h>

#ifdef _WIN32
#include <direct.h>
#define MKDIR(path) _mkdir(path)
#define PATH_SEP '\\'
#else
#include <sys/stat.h>
#define MKDIR(path) mkdir(path, 0777)
#define PATH_SEP '/'
#endif

static void usage(const char *prog)
{
    fprintf(stderr, "Usage: %s <rows> <cols>\n", prog);
}

int main(int argc, char **argv)
{
    if (argc < 3)
    {
        usage(argv[0]);
        return 1;
    }

    int rows = atoi(argv[1]);
    int cols = atoi(argv[2]);
    if (rows < 3 || cols < 3)
    {
        usage(argv[0]);
        return 1;
    }

    const char *outdir = "../data";
    const char *outfile = "initial.dat";
    char outpath[512];
    snprintf(outpath, sizeof(outpath), "%s%c%s", outdir, PATH_SEP, outfile);

    if (MKDIR(outdir) != 0 && errno != EEXIST)
    {
        fprintf(stderr, "Error: could not create %s: %s\n", outdir, strerror(errno));
        return 1;
    }

    size_t total = (size_t)rows * (size_t)cols;
    double *data = (double *)malloc(total * sizeof(double));
    if (!data)
    {
        fprintf(stderr, "Memory allocation failed for %zu doubles\n", total);
        return 1;
    }

    // Initialize: interior=0, T/B=0, L/R=1
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
        {
            double v = 0.0;
            if (j == 0 || j == cols - 1)
                v = 1.0;
            data[i * cols + j] = v;
        }
    }

    FILE *fout = fopen(outpath, "wb"); // overwrite if exists
    if (!fout)
    {
        fprintf(stderr, "Error creating %s: %s\n", outpath, strerror(errno));
        free(data);
        return 1;
    }

    int32_t r32 = (int32_t)rows, c32 = (int32_t)cols;
    if (fwrite(&r32, sizeof(int32_t), 1, fout) != 1 ||
        fwrite(&c32, sizeof(int32_t), 1, fout) != 1 ||
        fwrite(data, sizeof(double), total, fout) != total)
    {
        fprintf(stderr, "Error writing to %s\n", outpath);
        fclose(fout);
        free(data);
        return 1;
    }

    fclose(fout);
    free(data);
    printf("Created %s (%dx%d)\n", outpath, rows, cols);
    return 0;
}
