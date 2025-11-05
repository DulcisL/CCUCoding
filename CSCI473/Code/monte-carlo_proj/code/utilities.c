#include "utilities.h"

int read_header(FILE *f, int32_t *r, int32_t *c)
{
    return (fread(r, sizeof(int32_t), 1, f) == 1 &&
            fread(c, sizeof(int32_t), 1, f) == 1)
               ? 0
               : -1;
}

int write_header(FILE *f, int32_t r, int32_t c)
{
    return (fwrite(&r, sizeof(int32_t), 1, f) == 1 &&
            fwrite(&c, sizeof(int32_t), 1, f) == 1)
               ? 0
               : -1;
}
