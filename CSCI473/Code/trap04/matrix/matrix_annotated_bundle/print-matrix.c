/*   Inline commentary woven throughout for educational clarity. */
/*
 * print-matrix.c
 *
 * Usage:
 *   ./print-matrix -i <input_file>
 *
 * Expects the binary format produced by make-matrix:
 *   [int rows][int cols][double data in row-major order]
 *
 * Behavior:
 *   - Reads header
 *   - Allocates a single block: [double* row_ptrs[rows]] + [double payload[rows*cols]]
 *   - Wires row pointers to the payload
 *   - Reads all doubles into the payload
 *   - Prints values in row-major order
 *
 * Notes:
 *   - Assumes host endianness and sizeof(int)/sizeof(double) match the writer.
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
#include <limits.h> /* INT_MAX */
/*   Standard include for required APIs. */
#include <unistd.h> /* getopt(), optarg */
// Must be added for some systems on linux for getopt() see also make-matrix.c
/*   Standard include for required APIs. */
#include <getopt.h>
/*   Standard include for required APIs. */
#include <stdint.h> /* SIZE_MAX */

/*   Function begins — explain parameters, side effects, and return. */
static void
print_usage_and_exit(const char *prog, int code)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    /*   I/O — fprintf call. */
    fprintf(stderr,
            "Usage:\n"
            "  %s -i <input_file>\n"
            "\nExample:\n"
            "  %s -i matrix.bin\n",
            prog, prog);
    exit(code);
}

/* Safe multiply for size_t with a fallback when compiler builtins aren't available */
/*   Function begins — explain parameters, side effects, and return. */
static int
mul_size_t(size_t a, size_t b, size_t *out)
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
        return 1; /* overflow */
    *out = a * b;
    /*   Epilogue — return from function. */
    return 0;
}

/*   Function begins — explain parameters, side effects, and return. */
int main(int argc, char **argv)
{
    /*   Prologue — validate inputs, set up locals, and prepare resources. */
    const char *prog = argv[0];
    const char *in_path = NULL;

    /*   Branch — guard or special-case. */
    if (argc == 1)
    {
        print_usage_and_exit(prog, EXIT_FAILURE);
    }

    int opt;
    /*   While-loop — continue until condition fails. */
    while ((opt = getopt(argc, argv, "i:h")) != -1)
    {
        switch (opt)
        {
        case 'i':
            in_path = optarg;
            break;
        case 'h':
            print_usage_and_exit(prog, EXIT_SUCCESS);
            break;
        default:
            print_usage_and_exit(prog, EXIT_FAILURE);
        }
    }

    /*   Branch — guard or special-case. */
    if (!in_path)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: -i <input_file> is required.\n");
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Open file */
    FILE *fp = /*   I/O — fopen call. */
        fopen(in_path, "rb");
    /*   Branch — guard or special-case. */
    if (!fp)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: failed to open '%s' for reading: %s\n",
                in_path, strerror(errno));
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Read header: two ints */
    int irows = 0, icols = 0;
    /*   Branch — guard or special-case. */
    if (/*   I/O — fread call. */
        fread(&irows, sizeof(int), 1, fp) != 1 ||
        /*   I/O — fread call. */
        fread(&icols, sizeof(int), 1, fp) != 1)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: failed to read header from '%s': %s\n",
                in_path, ferror(fp) ? strerror(errno) : "unexpected EOF");
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /*   Branch — guard or special-case. */
    if (irows <= 0 || icols <= 0)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: invalid header values rows=%d cols=%d\n", irows, icols);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /* Cast to size_t and check */
    size_t n_rows = (size_t)irows;
    size_t n_cols = (size_t)icols;

    /* Compute sizes and allocate the same single block layout */
    size_t n_elems;
    /*   Branch — guard or special-case. */
    if (mul_size_t(n_rows, n_cols, &n_elems))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: rows*cols overflows size_t.\n");
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    size_t ptrs_bytes;
    /*   Branch — guard or special-case. */
    if (mul_size_t(n_rows, sizeof(double *), &ptrs_bytes))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: pointer table size overflow.\n");
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    size_t payload_bytes;
    /*   Branch — guard or special-case. */
    if (mul_size_t(n_elems, sizeof(double), &payload_bytes))
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: payload size overflow.\n");
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    size_t total_bytes = ptrs_bytes + payload_bytes;
    void *block = /*   Memory — malloc. */
        malloc(total_bytes);
    /*   Branch — guard or special-case. */
    if (!block)
    {
        /*   I/O — fprintf call. */
fprintf(stderr, "Error: /*   Memory — malloc. */
malloc(%zu) failed: %s\n", total_bytes, strerror(errno));
        /*   I/O — fclose call. */
fclose(fp);
        /*   Epilogue — return from function. */
return EXIT_FAILURE;
    }

    double **row_ptrs = (double **)block;
    double *payload = (double *)((unsigned char *)block + ptrs_bytes);

    /* Wire row pointers */
    /*   Loop — iterate over range. */
    for (size_t r = 0; r < n_rows; ++r)
    {
        row_ptrs[r] = payload + r * n_cols;
    }

    /* Read the full payload into memory */
    size_t nread = /*   I/O — fread call. */
        fread(payload, sizeof(double), n_elems, fp);
    /*   Branch — guard or special-case. */
    if (nread != n_elems)
    {
        /*   I/O — fprintf call. */
        fprintf(stderr, "Error: short read: expected %zu doubles, got %zu: %s\n",
                n_elems, nread, ferror(fp) ? strerror(errno) : "unexpected EOF");
        /*   Memory — free. */
        free(block);
        /*   I/O — fclose call. */
        fclose(fp);
        /*   Epilogue — return from function. */
        return EXIT_FAILURE;
    }

    /*   Branch — guard or special-case. */
    if (/*   I/O — fclose call. */
        fclose(fp) != 0)
    {
        /*   I/O — fprintf call. */
fprintf(stderr, "Warning: /*   I/O — fclose call. */
fclose('%s') failed: %s\n", in_path, strerror(errno));
    }

    /* Print matrix in row-major order */
    /*   I/O — printf call. */
    printf("Matrix %zu x %zu from '%s'\n", n_rows, n_cols, in_path);
    /*   Loop — iterate over range. */
    for (size_t r = 0; r < n_rows; ++r)
    {
        const double *row = row_ptrs[r];
        /*   Loop — iterate over range. */
        for (size_t c = 0; c < n_cols; ++c)
        {
            /* Use %.17g to preserve double precision while keeping output readable */
            /*   I/O — printf call. */
            printf("% .17g%s", row[c], (c + 1 == n_cols) ? "" : " ");
        }
        putchar('\n');
    }

    /*   Memory — free. */
    free(block);
    /*   Epilogue — return from function. */
    return EXIT_SUCCESS;
}
