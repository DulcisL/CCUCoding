#include "utilities.h"

#include <errno.h>
#include <math.h>
#include <stdlib.h>
#include <string.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

static const double TWO_PI = 2.0 * M_PI;
static const char *DATA_DIRECTORY = "./data";

int parse_positive_double(const char *str, double *out) {
    if (!str || !out) {
        return -1;
    }

    char *endptr = NULL;
    double value = strtod(str, &endptr);
    if (endptr == str || *endptr != '\0' || value <= 0.0 || !isfinite(value)) {
        return -1;
    }
    *out = value;
    return 0;
}

int parse_nonnegative_double(const char *str, double *out) {
    if (!str || !out) {
        return -1;
    }

    char *endptr = NULL;
    double value = strtod(str, &endptr);
    if (endptr == str || *endptr != '\0' || value < 0.0 || !isfinite(value)) {
        return -1;
    }
    *out = value;
    return 0;
}

int parse_positive_ulong(const char *str, unsigned long *out) {
    if (!str || !out) {
        return -1;
    }

    char *endptr = NULL;
    unsigned long value = strtoul(str, &endptr, 10);
    if (endptr == str || *endptr != '\0' || value == 0UL) {
        return -1;
    }
    *out = value;
    return 0;
}

double rand_unit(void) {
    return (double)rand() / ((double)RAND_MAX + 1.0);
}

double sample_free_path(double interaction_coeff) {
    double u = rand_unit();
    if (u <= 0.0) {
        u = 1e-12;
    }
    return -log(u) / interaction_coeff;
}

void sample_isotropic_direction(double *mu, double *nu) {
    double theta = TWO_PI * rand_unit();
    double cos_theta = cos(theta);
    double sin_theta = sin(theta);
    if (fabs(cos_theta) < 1e-8) {
        cos_theta = (cos_theta >= 0.0) ? 1e-8 : -1e-8;
    }
    if (mu) {
        *mu = cos_theta;
    }
    if (nu) {
        *nu = sin_theta;
    }
}

void ensure_data_directory(void) {
    struct stat st;
    if (stat(DATA_DIRECTORY, &st) == 0) {
        if (!S_ISDIR(st.st_mode)) {
            fprintf(stderr, "Error: %s exists and is not a directory\n", DATA_DIRECTORY);
            exit(EXIT_FAILURE);
        }
        return;
    }

    if (mkdir(DATA_DIRECTORY, 0775) != 0 && errno != EEXIST) {
        perror("mkdir data");
        exit(EXIT_FAILURE);
    }
}

FILE *open_data_file(const char *path, const char *mode) {
    if (!path || !mode) {
        return NULL;
    }

    FILE *fp = fopen(path, mode);
    if (!fp) {
        fprintf(stderr, "Error: unable to open %s: %s\n", path, strerror(errno));
    }
    return fp;
}

void trace_writer_init(TraceWriter *writer, const char *path) {
    if (!writer) {
        return;
    }

    memset(writer, 0, sizeof(*writer));

    if (!path || strlen(path) == 0) {
        writer->enabled = false;
        return;
    }

    strncpy(writer->path, path, sizeof(writer->path) - 1);
    writer->file = open_data_file(writer->path, "w");
    if (writer->file) {
        writer->enabled = true;
    }
}

void trace_writer_write_header(TraceWriter *writer) {
    if (!writer || !writer->enabled) {
        return;
    }
    fprintf(writer->file,
            "neutron_id,step,x_start,y_start,x_end,y_end,event\n");
}

void trace_writer_log_segment(TraceWriter *writer,
                              unsigned long neutron_id,
                              unsigned int step,
                              double x_start,
                              double y_start,
                              double x_end,
                              double y_end,
                              const char *event) {
    if (!writer || !writer->enabled) {
        return;
    }

    fprintf(writer->file,
            "%lu,%u,%.10f,%.10f,%.10f,%.10f,%s\n",
            neutron_id,
            step,
            x_start,
            y_start,
            x_end,
            y_end,
            event ? event : "unknown");
    writer->segments_written++;
}

void trace_writer_close(TraceWriter *writer) {
    if (!writer || !writer->enabled) {
        return;
    }

    fclose(writer->file);
    writer->file = NULL;
    writer->enabled = false;
}
