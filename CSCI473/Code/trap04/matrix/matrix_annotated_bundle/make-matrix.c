/*   Inline commentary woven throughout for educational clarity. */
/*
 * make-matrix.c
 *
 * Usage (both forms supported):
 *   Long-ish (original):  ./make-matrix -rows <num_rows> -cols <num_cols> -l <lower> -u <upper> -o <file>
 *   Short (getopt):       ./make-matrix -r <num_rows>    -c <num_cols>    -l <lower> -u <upper> -o <file>
 *
 * Behavior:
 *   - Creates a rows x cols matrix of double-precision values drawn uniformly at random in [lower, upper].
 *   - Binary file layout:
 *       [int rows][int cols][double data in row-major order]
 *   - Single  Memory — malloc.
 *          malloc() 2D layout: [double* row_ptrs[rows]] then payload of rows*cols doubles.
 *
 * Notes:
 *   - Uses host endianness/sizes. For portable on-disk format, add explicit endianness handling.
 */

/*   Standard include for required APIs. */
#include <stdio.h>
/*   Standard include for required APIs. */
#include <stdlib.h>
/*   Standard include for required APIs. */
#include <string.h>
/*   Standard include for required APIs. */
#include <errno.h>
/*   Standard include for required APIs. */
#include <time.h>
/*   Standard include for required APIs. */
#include <limits.h> /* INT_MAX */
/*   Standard include for required APIs. */
#include <unistd.h> /* getopt(), optarg */
/*   Standard include for required APIs. */
#include <getopt.h>

/*   Function begins — explain parameters, side effects, and return. */
static void
print_usage_and_exit(const char *prog, int code)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    /*   I/O — fprintf call. */
    fprintf(stderr,
            "Usage:\n"
            "  %s -rows <num_rows> -cols <num_cols> -l <lower_bound> -u <upper_bound> -o <output_file>\n"
            "  or\n"
            "  %s -r <num_rows> -c <num_cols> -l <lower_bound> -u <upper_bound> -o <output_file>\n"
            "\nExamples:\n"
            "  %s -rows 1000 -cols 512 -l -1.0 -u 1.0 -o matrix.bin\n"
            "  %s -r 1000 -c 512 -l -1.0 -u 1.0 -o matrix.bin\n",
            prog, prog, prog, prog);
    exit(code);
}

/* Parse helpers */
/*   Function begins — explain parameters, side effects, and return. */
static long parse_long(const char *s, const char *flag_name)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    char *end = NULL;
    errno = 0;
    long v = strtol(s, &end, 10);
    /*   Branch — guard or special-case. */
    if (errno != 0 || end == s || *end != '\0')
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: invalid integer for %s: '%s'\n", flag_name, s);
        exit(EXIT_FAILURE);
    }
    /*   Epilogue — return from function. */
    return v;
}

/*   Function begins — explain parameters, side effects, and return. */
static double parse_double(const char *s, const char *flag_name)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    char *end = NULL;
    errno = 0;
    double v = strtod(s, &end);
    /*   Branch — guard or special-case. */
    if (errno != 0 || end == s || *end != '\0')
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: invalid double for %s: '%s'\n", flag_name, s);
        exit(EXIT_FAILURE);
    }
    /*   Epilogue — return from function. */
    return v;
}

/* Uniform random double in [a,b] */
/*   Function begins — explain parameters, side effects, and return. */
static inline double rand_uniform(double a, double b)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    double r = (double)rand() / (double)RAND_MAX;
    /*   Epilogue — return from function. */
    return a + (b - a) * r;
}

/* Normalize argv: translate "-rows" -> "-r", "-cols" -> "-c".
 * We don't copy strings; we just swap the pointers to constant short flags.
 * Returns the possibly-updated argv pointer (same storage as input).
 */
static char **normalize_args(int argc, char **argv)
{
    /*   Loop — iterate over range. */
    for (int i = 1; i < argc; ++i)
    {
        /*   Branch — guard or special-case. */
        if (strcmp(argv[i], "-rows") == 0)
        {
            argv[i] = "-r";
        }
        else if (strcmp(argv[i], "-cols") == 0)
        {
            argv[i] = "-c";
        }
        /* The others (-l, -u, -o) are already short-form; nothing to do. */
        /*   Branch — guard or special-case. */
        if (strcmp(argv[i], "-h") == 0 || strcmp(argv[i], "--help") == 0)
        {
            /* Let getopt handle -h; accept --help by printing usage immediately. */
            /*   Branch — guard or special-case. */
            if (argv[i][1] == '-')
            {
                print_usage_and_exit(argv[0], EXIT_SUCCESS);
            }
        }
    }
    /*   Epilogue — return from function. */
    return argv;
}

/*   Function begins — explain parameters, side effects, and return. */
int main(int argc, char **argv)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    const char *prog = argv[0];

    /*   Branch — guard or special-case. */
    if (argc == 1)
    {
        print_usage_and_exit(prog, EXIT_FAILURE);
    }

    /* Allow original flags by normalizing to short options before getopt */
    argv = normalize_args(argc, argv);

    long rows = -1;
    long cols = -1;
    double lower = 0.0;
    double upper = -1.0; /* upper < lower signals "not set" until parsed */
    const char *out_path = NULL;

    int opt;
    /* Options: r: rows, c: cols, l: lower, u: upper, o: output, h: help */
    /*   While-loop — continue until condition fails. */
    while ((opt = getopt(argc, argv, "r:c:l:u:o:h")) != -1)
    {
        switch (opt)
        {
        case 'r':
            rows = parse_long(optarg, "-rows/-r");
            break;
        case 'c':
            cols = parse_long(optarg, "-cols/-c");
            break;
        case 'l':
            lower = parse_double(optarg, "-l");
            break;
        case 'u':
            upper = parse_double(optarg, "-u");
            break;
        case 'o':
            out_path = optarg;
            break;
        case 'h':
            print_usage_and_exit(prog, EXIT_SUCCESS);
            break;
        default:
            print_usage_and_exit(prog, EXIT_FAILURE);
        }
    }

    /* Validate required arguments */
    /*   Branch — guard or special-case. */
    if (rows <= 0)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: -rows/-r must be a positive integer.\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
    /*   Branch — guard or special-case. */
    if (cols <= 0)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: -cols/-c must be a positive integer.\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
    /*   Branch — guard or special-case. */
    if (upper < lower)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: -u (upper) must be >= -l (lower).\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
    /*   Branch — guard or special-case. */
    if (!out_path)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: -o <output_file> is required.\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Safe casts to size_t and overflow checks */
    const size_t n_rows = (size_t)rows;
    const size_t n_cols = (size_t)cols;
    /*   Branch — guard or special-case. */
    if ((long)n_rows != rows || (long)n_cols != cols)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: rows/cols out of supported range on this platform.\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    size_t n_elems;
#if defined(__has_builtin)
#if __has_builtin(__builtin_mul_overflow)
    /*   Branch — guard or special-case. */
    if (__builtin_mul_overflow(n_rows, n_cols, &n_elems))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: rows*cols overflows size_t.\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
#else
    n_elems = n_rows * n_cols;
#endif
#else
    n_elems = n_rows * n_cols;
#endif

    size_t ptrs_bytes = n_rows * sizeof(double *);
    size_t payload_bytes = n_elems * sizeof(double);
    size_t total_bytes = ptrs_bytes + payload_bytes;

    /* Single allocation */
    void *block = /*   Memory — malloc. */
        malloc(total_bytes);
    /*   Branch — guard or special-case. */
    if (!block)
    {
        /*   I/O — fprintf call. */
fprintf(stderr, "Error: /*   Memory — malloc. */
malloc(%zu) failed: %s\n", total_bytes, strerror(errno));
        /*   Epilogue — return from function. */
return EXIT_FAILURE;
    }

    double **row_ptrs = (double **)block;
    double *payload = (double *)((unsigned char *)block + ptrs_bytes);

    /* Wire up row pointers */
    /*   Loop — iterate over range. */
    for (size_t r = 0; r < n_rows; ++r)
    {
        row_ptrs[r] = payload + r * n_cols;
    }

    /* Seed RNG: prefer /dev/urandom, fallback to time-based */
    {
        unsigned int seed = (unsigned int)time(NULL);
        FILE *urnd = /*   I/O — fopen call. */
            fopen("/dev/urandom", "rb");
        /*   Branch — guard or special-case. */
        if (urnd)
        {
            (void)/*   I/O — fread call. */
                fread(&seed, sizeof(seed), 1, urnd);
            /*   I/O — fclose call. */
            fclose(urnd);
        }
        srand(seed);
    }

    /* Fill matrix */
    /*   Loop — iterate over range. */
    for (size_t r = 0; r < n_rows; ++r)
    {
        double *row = row_ptrs[r];
        /*   Loop — iterate over range. */
        for (size_t c = 0; c < n_cols; ++c)
        {
            row[c] = rand_uniform(lower, upper);
        }
    }

    /* Open output */
    FILE *fp = /*   I/O — fopen call. */
        fopen(out_path, "wb");
    /*   Branch — guard or special-case. */
    if (!fp)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: open '%s' for writing failed: %s\n", out_path, strerror(errno));
        /*   Memory — free. */
        free(block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Header as two ints */
    /*   Branch — guard or special-case. */
    if (rows > (long)INT_MAX || cols > (long)INT_MAX)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: rows/cols exceed INT_MAX; cannot store in 2 x int header.\n");
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Memory — free. */
        free(block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }
    int irows = (int)rows, icols = (int)cols;

    /*   Branch — guard or special-case. */
    if (/*   I/O — fwrite call. */
        fwrite(&irows, sizeof(int), 1, fp) != 1 ||
        /*   I/O — fwrite call. */
        fwrite(&icols, sizeof(int), 1, fp) != 1)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: writing header to '%s' failed: %s\n", out_path, strerror(errno));
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Memory — free. */
        free(block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Payload in row-major order */
    size_t wrote = /*   I/O — fwrite call. */
        fwrite(payload, sizeof(double), n_elems, fp);
    /*   Branch — guard or special-case. */
    if (wrote != n_elems)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: short write: expected %zu doubles, wrote %zu: %s\n",
                n_elems, wrote, strerror(errno));
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Memory — free. */
        free(block);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /*   Branch — guard or special-case. */
    if (/*   I/O — fclose call. */
        fclose(fp) != 0)
    {
        /*   I/O — fprintf call. */
fprintf(stderr, "Warning: /*   I/O — fclose call. */
fclose('%s') failed: %s\n", out_path, strerror(errno));
    }

    /*   Memory — free. */
    free(block);

    /*   I/O — fprintf call. */
    fprintf(stdout,
            "Wrote matrix: %ld x %ld (range %.6g..%.6g) to '%s'\n"
            "Header: [int rows=%d][int cols=%d], followed by %zu doubles (row-major).\n",
            rows, cols, lower, upper, out_path, irows, icols, n_elems);

    /*   Epilogue — return from function. */
    return EXIT_SUCCESS;
}
