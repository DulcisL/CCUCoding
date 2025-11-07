// header file of user functions
#ifndef UTILITIES_H
#define UTILITIES_H

#include <stdbool.h>
#include <stdio.h>

typedef struct {
    unsigned long total_neutrons;
    unsigned long absorbed;
    unsigned long transmitted;
    unsigned long reflected;
    unsigned long scatter_events;
    unsigned long absorption_events;
    unsigned long total_collisions;
    double total_track_length;
} SimulationTallies;

typedef struct {
    FILE *file;
    bool enabled;
    unsigned long segments_written;
    char path[512];
} TraceWriter;

int parse_positive_double(const char *str, double *out);
int parse_nonnegative_double(const char *str, double *out);
int parse_positive_ulong(const char *str, unsigned long *out);

double rand_unit(void);
double sample_free_path(double interaction_coeff);
void sample_isotropic_direction(double *mu, double *nu);

void ensure_data_directory(void);
FILE *open_data_file(const char *path, const char *mode);

void trace_writer_init(TraceWriter *writer, const char *path);
void trace_writer_write_header(TraceWriter *writer);
void trace_writer_log_segment(TraceWriter *writer,
                              unsigned long neutron_id,
                              unsigned int step,
                              double x_start,
                              double y_start,
                              double x_end,
                              double y_end,
                              const char *event);
void trace_writer_close(TraceWriter *writer);

#endif
