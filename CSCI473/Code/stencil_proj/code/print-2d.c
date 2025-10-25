// print-2d.c
// Usage: ./print-2d <path/to/file.dat>

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char **argv)
{
    if (argc < 2)
    {
        fprintf(stderr, "Usage: %s <path/to/file.dat>\n", argv[0]);
        return 1;
    }
    const char *filepath = argv[1];

    FILE *fin = fopen(filepath, "rb");
    if (!fin)
    {
        perror("Error opening file");
        return 1;
    }

    int32_t rows, cols;
    if (fread(&rows, sizeof(int32_t), 1, fin) != 1 ||
        fread(&cols, sizeof(int32_t), 1, fin) != 1)
    {
        fprintf(stderr, "Error: could not read header (rows/cols)\n");
        fclose(fin);
        return 1;
    }
    if (rows <= 0 || cols <= 0)
    {
        fprintf(stderr, "Error: invalid dimensions in header: %d x %d\n", rows, cols);
        fclose(fin);
        return 1;
    }

    size_t total = (size_t)rows * (size_t)cols;
    double *data = (double *)malloc(total * sizeof(double));
    if (!data)
    {
        fprintf(stderr, "Memory allocation failed\n");
        fclose(fin);
        return 1;
    }

    if (fread(data, sizeof(double), total, fin) != total)
    {
        fprintf(stderr, "Error: could not read %zu matrix elements\n", total);
        free(data);
        fclose(fin);
        return 1;
    }
    fclose(fin);

    printf("File: %s\nMatrix size: %d x %d\n----------------------------------------\n", filepath, rows, cols);
    for (int i = 0; i < rows; ++i)
    {
        for (int j = 0; j < cols; ++j)
            printf("%7.3f ", data[i * cols + j]);
        printf("\n");
    }
    free(data);
    return 0;
}
