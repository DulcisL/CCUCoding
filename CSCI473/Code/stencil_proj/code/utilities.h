// header file of user functions
#ifndef UTILITIES_H
#define UTILITIES_H
#include <stdio.h>
#include <stdint.h>

int read_header(FILE *f, int32_t *r, int32_t *c);
int write_header(FILE *f, int32_t r, int32_t c);

#endif
