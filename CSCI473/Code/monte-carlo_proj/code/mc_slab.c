// main monte-carlo file

/*
Usage: ./mc_slab C Cc H n [--trace-file path] [--trace-every m]
    C > 0       (total interactions coeff)
    Cc in [0,C] (absorbing Comp)
    H > 0       (slab thickness)
    n>= 1       (number of particles)
*/

#include <errno.h>
#include <math.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "timer.h"
#include "utilities.h"

typedef struct {
    double C;
    double Cc;
    double Cs;
    double H;
    unsigned long n;
    unsigned long trace_every;
    char trace_path[512];
} SimulationConfig;

static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s C Cc H n [--trace-file path] [--trace-every m]\n"
            "    C > 0       (total interactions coeff)\n"
            "    Cc in [0,C] (absorbing coeff)\n"
            "    H > 0       (slab thickness)\n"
            "    n >= 1      (number of particles)\n",
            prog);
}

static void parse_arguments(int argc, char *argv[], SimulationConfig *cfg) {
    if (argc < 5) {
        print_usage(argv[0]);
        exit(EXIT_FAILURE);
    }

    if (parse_positive_double(argv[1], &cfg->C) != 0) {
        fprintf(stderr, "Error: invalid C value '%s'\n", argv[1]);
        exit(EXIT_FAILURE);
    }
    if (parse_nonnegative_double(argv[2], &cfg->Cc) != 0) {
        fprintf(stderr, "Error: invalid Cc value '%s'\n", argv[2]);
        exit(EXIT_FAILURE);
    }
    if (cfg->Cc > cfg->C) {
        fprintf(stderr, "Error: Cc must not exceed C\n");
        exit(EXIT_FAILURE);
    }
    cfg->Cs = cfg->C - cfg->Cc;

    if (parse_positive_double(argv[3], &cfg->H) != 0) {
        fprintf(stderr, "Error: invalid H value '%s'\n", argv[3]);
        exit(EXIT_FAILURE);
    }
    if (parse_positive_ulong(argv[4], &cfg->n) != 0) {
        fprintf(stderr, "Error: invalid particle count '%s'\n", argv[4]);
        exit(EXIT_FAILURE);
    }

    cfg->trace_every = 0;
    memset(cfg->trace_path, 0, sizeof(cfg->trace_path));

    int i = 5;
    while (i < argc) {
        if (strcmp(argv[i], "--trace-file") == 0) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Error: --trace-file expects a path argument\n");
                exit(EXIT_FAILURE);
            }
            strncpy(cfg->trace_path, argv[i + 1], sizeof(cfg->trace_path) - 1);
            i += 2;
        } else if (strcmp(argv[i], "--trace-every") == 0) {
            if (i + 1 >= argc) {
                fprintf(stderr, "Error: --trace-every expects an integer argument\n");
                exit(EXIT_FAILURE);
            }
            if (parse_positive_ulong(argv[i + 1], &cfg->trace_every) != 0) {
                fprintf(stderr, "Error: invalid --trace-every value '%s'\n", argv[i + 1]);
                exit(EXIT_FAILURE);
            }
            i += 2;
        } else if (strcmp(argv[i], "--help") == 0 || strcmp(argv[i], "-h") == 0) {
            print_usage(argv[0]);
            exit(EXIT_SUCCESS);
        } else {
            fprintf(stderr, "Error: unrecognized argument '%s'\n", argv[i]);
            print_usage(argv[0]);
            exit(EXIT_FAILURE);
        }
    }
}

static void seed_rng(void) {
    const char *seed_env = getenv("MC_SLAB_SEED");
    if (seed_env && strlen(seed_env) > 0) {
        unsigned long seed = 0;
        if (parse_positive_ulong(seed_env, &seed) == 0) {
            srand((unsigned int)seed);
            return;
        }
        fprintf(stderr, "Warning: invalid MC_SLAB_SEED '%s', using time-based seed\n", seed_env);
    }
    srand((unsigned int)time(NULL));
}

static void write_summary(FILE *out,
                          const SimulationConfig *cfg,
                          const SimulationTallies *tallies,
                          const char *trace_path,
                          unsigned long trace_segments,
                          double elapsed_seconds,
                          double read_seconds,
                          double compute_seconds,
                          double write_seconds) {
    if (!out || !cfg || !tallies) {
        return;
    }

    double avg_collisions = 0.0;
    double avg_path_length = 0.0;
    if (tallies->total_neutrons > 0) {
        avg_collisions = (double)tallies->total_collisions / (double)tallies->total_neutrons;
        avg_path_length = tallies->total_track_length / (double)tallies->total_neutrons;
    }

    char trace_value[1024];
    if (trace_path && strlen(trace_path) > 0) {
        snprintf(trace_value, sizeof(trace_value), "\"%s\"", trace_path);
    } else {
        snprintf(trace_value, sizeof(trace_value), "null");
    }

    fprintf(out,
            "{\n"
            "  \"C\": %.10f,\n"
            "  \"Cc\": %.10f,\n"
            "  \"Cs\": %.10f,\n"
            "  \"H\": %.10f,\n"
            "  \"n\": %lu,\n"
            "  \"absorbed\": %lu,\n"
            "  \"transmitted\": %lu,\n"
            "  \"reflected\": %lu,\n"
            "  \"scatter_events\": %lu,\n"
            "  \"absorption_events\": %lu,\n"
            "  \"total_collisions\": %lu,\n"
            "  \"total_track_length\": %.10f,\n"
            "  \"avg_collisions\": %.10f,\n"
            "  \"avg_path_length\": %.10f,\n"
            "  \"elapsed_seconds\": %.10f,\n"
            "  \"read_seconds\": %.10f,\n"
            "  \"compute_seconds\": %.10f,\n"
            "  \"write_seconds\": %.10f,\n"
            "  \"trace_file\": %s,\n"
            "  \"trace_segments\": %lu\n"
            "}\n",
            cfg->C,
            cfg->Cc,
            cfg->Cs,
            cfg->H,
            tallies->total_neutrons,
            tallies->absorbed,
            tallies->transmitted,
            tallies->reflected,
            tallies->scatter_events,
            tallies->absorption_events,
            tallies->total_collisions,
            tallies->total_track_length,
            avg_collisions,
            avg_path_length,
            elapsed_seconds,
            read_seconds,
            compute_seconds,
            write_seconds,
            trace_value,
            trace_segments);
}

static void log_trace_segment(TraceWriter *writer,
                              bool record,
                              unsigned long neutron_id,
                              unsigned int step,
                              double x_start,
                              double y_start,
                              double x_end,
                              double y_end,
                              const char *event) {
    if (!record) {
        return;
    }
    trace_writer_log_segment(writer,
                             neutron_id,
                             step,
                             x_start,
                             y_start,
                             x_end,
                             y_end,
                             event);
}

int main(int argc, char *argv[]) {
    double read_seconds = 0.0;
    double compute_seconds = 0.0;
    double write_seconds = 0.0;
    double stage_start = 0.0;
    double stage_finish = 0.0;

    SimulationConfig cfg;
    TraceWriter trace_writer;
    memset(&trace_writer, 0, sizeof(trace_writer));

    GET_TIME(stage_start);
    parse_arguments(argc, argv, &cfg);
    seed_rng();
    ensure_data_directory();

    if (cfg.trace_every > 0) {
        if (strlen(cfg.trace_path) == 0) {
            snprintf(cfg.trace_path, sizeof(cfg.trace_path), "./data/mc_slab_trace.csv");
        }
        trace_writer_init(&trace_writer, cfg.trace_path);
        if (!trace_writer.enabled) {
            fprintf(stderr, "Warning: unable to open trace file '%s'. Tracing disabled.\n", cfg.trace_path);
            cfg.trace_every = 0;
        } else {
            trace_writer_write_header(&trace_writer);
        }
    }
    GET_TIME(stage_finish);
    read_seconds = stage_finish - stage_start;

    SimulationTallies tallies = (SimulationTallies){0};
    tallies.total_neutrons = cfg.n;

    double absorption_prob = (cfg.C > 0.0) ? (cfg.Cc / cfg.C) : 0.0;

    GET_TIME(stage_start);

    for (unsigned long neutron = 0; neutron < cfg.n; ++neutron) {
        bool record = (cfg.trace_every > 0) && ((neutron + 1) % cfg.trace_every == 0);
        double x = 0.0;
        double y = 0.0;
        double mu = 1.0;
        double nu = 0.0;
        unsigned int step = 1;
        bool alive = true;

        while (alive) {
            double x_start = x;
            double y_start = y;
            double free_path = sample_free_path(cfg.C);
            double x_candidate = x_start + mu * free_path;
            double y_candidate = y_start + nu * free_path;

            if (mu > 0.0 && x_candidate >= cfg.H) {
                double distance = (cfg.H - x_start) / mu;
                double y_exit = y_start + nu * distance;
                if (distance < 0.0) {
                    distance = 0.0;
                    y_exit = y_start;
                }
                tallies.total_track_length += fabs(distance);
                tallies.transmitted++;
                log_trace_segment(&trace_writer,
                                  record,
                                  neutron + 1,
                                  step,
                                  x_start,
                                  y_start,
                                  cfg.H,
                                  y_exit,
                                  "exit_right");
                alive = false;
                break;
            }

            if (mu < 0.0 && x_candidate <= 0.0) {
                double distance = (0.0 - x_start) / mu;
                double y_exit = y_start + nu * distance;
                if (distance < 0.0) {
                    distance = 0.0;
                    y_exit = y_start;
                }
                tallies.total_track_length += fabs(distance);
                tallies.reflected++;
                log_trace_segment(&trace_writer,
                                  record,
                                  neutron + 1,
                                  step,
                                  x_start,
                                  y_start,
                                  0.0,
                                  y_exit,
                                  "exit_left");
                alive = false;
                break;
            }

            x = x_candidate;
            y = y_candidate;
            tallies.total_track_length += free_path;
            tallies.total_collisions++;

            double interaction_roll = rand_unit();
            if (interaction_roll < absorption_prob) {
                tallies.absorbed++;
                tallies.absorption_events++;
                log_trace_segment(&trace_writer,
                                  record,
                                  neutron + 1,
                                  step,
                                  x_start,
                                  y_start,
                                  x,
                                  y,
                                  "absorb");
                alive = false;
            } else {
                tallies.scatter_events++;
                log_trace_segment(&trace_writer,
                                  record,
                                  neutron + 1,
                                  step,
                                  x_start,
                                  y_start,
                                  x,
                                  y,
                                  "scatter");
                sample_isotropic_direction(&mu, &nu);
                step++;
            }
        }
    }

    GET_TIME(stage_finish);
    compute_seconds = stage_finish - stage_start;

    char trace_summary_path[512] = {0};
    const char *trace_path_ptr = NULL;
    unsigned long trace_segments = 0UL;
    const char *summary_path = "./data/mc_slab_summary.json";
    FILE *summary_fp = NULL;

    GET_TIME(stage_start);

    if (trace_writer.enabled) {
        snprintf(trace_summary_path, sizeof(trace_summary_path), "%s", trace_writer.path);
        trace_segments = trace_writer.segments_written;
        trace_path_ptr = trace_summary_path;
        trace_writer_close(&trace_writer);
    }

    summary_fp = open_data_file(summary_path, "w");
    if (!summary_fp) {
        fprintf(stderr, "Warning: unable to open summary file '%s' for writing\n", summary_path);
    }
    GET_TIME(stage_finish);
    write_seconds = stage_finish - stage_start;

    double total_seconds = read_seconds + compute_seconds + write_seconds;

    write_summary(stdout,
                  &cfg,
                  &tallies,
                  trace_path_ptr,
                  trace_segments,
                  total_seconds,
                  read_seconds,
                  compute_seconds,
                  write_seconds);
    if (summary_fp) {
        write_summary(summary_fp,
                      &cfg,
                      &tallies,
                      trace_path_ptr,
                      trace_segments,
                      total_seconds,
                      read_seconds,
                      compute_seconds,
                      write_seconds);
        fclose(summary_fp);
    }

    return EXIT_SUCCESS;
}
