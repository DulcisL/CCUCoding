// pthread-based Monte Carlo neutron slab simulation

/*
Usage: ./mc_slab_pthread C Cc H n [--trace-file path] [--trace-every m] T
    C > 0        Total interaction coefficient
    Cc in [0,C]  Absorption coefficient
    H > 0        Slab thickness
    n >= 1       Number of particles
    T >= 1       Number of pthread worker threads (must be last positional arg)
    Optional arguments must appear before T.
*/

#include <errno.h>
#include <math.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include "timer.h"
#include "utilities.h"

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

typedef struct {
    double C;
    double Cc;
    double Cs;
    double H;
    unsigned long n;
    unsigned long trace_every;
    unsigned int threads;
    char trace_path[512];
} SimulationConfig;

typedef struct {
    const SimulationConfig *cfg;
    unsigned long start_index;
    unsigned long count;
    unsigned long long rng_state;
    SimulationTallies tallies;
    TraceWriter *trace_writer;
    pthread_mutex_t *trace_mutex;
} ThreadTask;

static const double TWO_PI = 2.0 * M_PI;

static void print_usage(const char *prog) {
    fprintf(stderr,
            "Usage: %s C Cc H n [--trace-file path] [--trace-every m] T\n"
            "    C > 0        Total interaction coefficient\n"
            "    Cc in [0,C]  Absorption coefficient\n"
            "    H > 0        Slab thickness\n"
            "    n >= 1       Number of particles\n"
            "    T >= 1       Number of pthreads (must be final positional argument)\n",
            prog);
}

static unsigned long parse_threads_arg(const char *arg) {
    unsigned long threads = 0;
    if (parse_positive_ulong(arg, &threads) != 0) {
        fprintf(stderr, "Error: invalid thread count '%s'\n", arg);
        exit(EXIT_FAILURE);
    }
    return threads;
}

static void parse_arguments(int argc, char *argv[], SimulationConfig *cfg) {
    if (argc < 6) {
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

    cfg->threads = (unsigned int)parse_threads_arg(argv[argc - 1]);
    if (cfg->threads == 0) {
        fprintf(stderr, "Error: thread count must be >= 1\n");
        exit(EXIT_FAILURE);
    }

    int i = 5;
    while (i < argc - 1) {
        if (strcmp(argv[i], "--trace-file") == 0) {
            if (i + 1 >= argc - 1) {
                fprintf(stderr, "Error: --trace-file expects a path argument\n");
                exit(EXIT_FAILURE);
            }
            strncpy(cfg->trace_path, argv[i + 1], sizeof(cfg->trace_path) - 1);
            i += 2;
        } else if (strcmp(argv[i], "--trace-every") == 0) {
            if (i + 1 >= argc - 1) {
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

static unsigned long long next_random_u64(unsigned long long *state) {
    unsigned long long x = *state;
    x ^= x >> 12;
    x ^= x << 25;
    x ^= x >> 27;
    *state = x;
    return x * 2685821657736338717ULL;
}

static double rand_unit_thread(unsigned long long *state) {
    return (next_random_u64(state) >> 11) * (1.0 / 9007199254740992.0);
}

static double sample_free_path_thread(double interaction_coeff, unsigned long long *state) {
    double u = rand_unit_thread(state);
    if (u <= 0.0) {
        u = 1e-12;
    }
    return -log(u) / interaction_coeff;
}

static void sample_isotropic_direction_thread(double *mu, double *nu, unsigned long long *state) {
    double theta = TWO_PI * rand_unit_thread(state);
    double c = cos(theta);
    double s = sin(theta);
    if (mu) {
        *mu = c;
    }
    if (nu) {
        *nu = s;
    }
}

static unsigned long long seed_from_env(void) {
    const char *seed_env = getenv("MC_SLAB_SEED");
    if (seed_env && strlen(seed_env) > 0) {
        unsigned long seed = 0UL;
        if (parse_positive_ulong(seed_env, &seed) == 0) {
            return (unsigned long long)seed;
        }
        fprintf(stderr, "Warning: invalid MC_SLAB_SEED '%s', using time-based seed\n", seed_env);
    }
    return (unsigned long long)time(NULL);
}

static void log_trace_segment_parallel(ThreadTask *task,
                                       bool record,
                                       unsigned long neutron_id,
                                       unsigned int step,
                                       double x_start,
                                       double y_start,
                                       double x_end,
                                       double y_end,
                                       const char *event) {
    if (!record || !task->trace_writer || !task->trace_writer->enabled) {
        return;
    }
    pthread_mutex_lock(task->trace_mutex);
    trace_writer_log_segment(task->trace_writer,
                             neutron_id,
                             step,
                             x_start,
                             y_start,
                             x_end,
                             y_end,
                             event);
    pthread_mutex_unlock(task->trace_mutex);
}

static void *simulate_batch(void *arg) {
    ThreadTask *task = (ThreadTask *)arg;
    const SimulationConfig *cfg = task->cfg;
    SimulationTallies local = {0};
    double absorption_prob = (cfg->C > 0.0) ? (cfg->Cc / cfg->C) : 0.0;

    for (unsigned long i = 0; i < task->count; ++i) {
        unsigned long neutron_id = task->start_index + i + 1;
        bool record = (cfg->trace_every > 0) && (neutron_id % cfg->trace_every == 0);
        double x = 0.0;
        double y = 0.0;
        double mu = 1.0;
        double nu = 0.0;
        unsigned int step = 1;
        bool alive = true;

        while (alive) {
            double x_start = x;
            double y_start = y;
            double free_path = sample_free_path_thread(cfg->C, &task->rng_state);
            double x_candidate = x_start + mu * free_path;
            double y_candidate = y_start + nu * free_path;

            if (mu > 0.0 && x_candidate >= cfg->H) {
                double distance = (cfg->H - x_start) / mu;
                double y_exit = y_start + nu * distance;
                if (distance < 0.0) {
                    distance = 0.0;
                    y_exit = y_start;
                }
                local.total_track_length += fabs(distance);
                local.transmitted++;
                log_trace_segment_parallel(task,
                                           record,
                                           neutron_id,
                                           step,
                                           x_start,
                                           y_start,
                                           cfg->H,
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
                local.total_track_length += fabs(distance);
                local.reflected++;
                log_trace_segment_parallel(task,
                                           record,
                                           neutron_id,
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
            local.total_track_length += free_path;
            local.total_collisions++;

            double interaction_roll = rand_unit_thread(&task->rng_state);
            if (interaction_roll < absorption_prob) {
                local.absorbed++;
                local.absorption_events++;
                log_trace_segment_parallel(task,
                                           record,
                                           neutron_id,
                                           step,
                                           x_start,
                                           y_start,
                                           x,
                                           y,
                                           "absorb");
                alive = false;
            } else {
                local.scatter_events++;
                log_trace_segment_parallel(task,
                                           record,
                                           neutron_id,
                                           step,
                                           x_start,
                                           y_start,
                                           x,
                                           y,
                                           "scatter");
                sample_isotropic_direction_thread(&mu, &nu, &task->rng_state);
                step++;
            }
        }
    }

    task->tallies = local;
    return NULL;
}

static void write_summary(FILE *out,
                          const SimulationConfig *cfg,
                          const SimulationTallies *tallies,
                          const char *trace_path,
                          unsigned long trace_segments,
                          double elapsed_seconds) {
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
            "  \"threads\": %u,\n"
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
            "  \"trace_file\": %s,\n"
            "  \"trace_segments\": %lu\n"
            "}\n",
            cfg->C,
            cfg->Cc,
            cfg->Cs,
            cfg->H,
            tallies->total_neutrons,
            cfg->threads,
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
            trace_value,
            trace_segments);
}

int main(int argc, char *argv[]) {
    SimulationConfig cfg;
    parse_arguments(argc, argv, &cfg);

    ensure_data_directory();

    TraceWriter trace_writer;
    memset(&trace_writer, 0, sizeof(trace_writer));
    pthread_mutex_t trace_mutex;
    bool trace_enabled = false;

    if (cfg.trace_every > 0) {
        if (strlen(cfg.trace_path) == 0) {
            snprintf(cfg.trace_path, sizeof(cfg.trace_path), "./data/mc_slab_pthread_trace.csv");
        }
        trace_writer_init(&trace_writer, cfg.trace_path);
        if (!trace_writer.enabled) {
            fprintf(stderr, "Warning: unable to open trace file '%s'. Tracing disabled.\n", cfg.trace_path);
            cfg.trace_every = 0;
        } else {
            trace_writer_write_header(&trace_writer);
            pthread_mutex_init(&trace_mutex, NULL);
            trace_enabled = true;
        }
    }

    unsigned long long base_seed = seed_from_env();

    pthread_t *threads = malloc(sizeof(pthread_t) * cfg.threads);
    ThreadTask *tasks = calloc(cfg.threads, sizeof(ThreadTask));
    if (!threads || !tasks) {
        fprintf(stderr, "Error: unable to allocate thread structures\n");
        exit(EXIT_FAILURE);
    }

    unsigned long base = cfg.n / cfg.threads;
    unsigned long remainder = cfg.n % cfg.threads;
    unsigned long offset = 0;

    for (unsigned int t = 0; t < cfg.threads; ++t) {
        unsigned long chunk = base + (t < remainder ? 1UL : 0UL);
        tasks[t].cfg = &cfg;
        tasks[t].start_index = offset;
        tasks[t].count = chunk;
        tasks[t].trace_writer = trace_enabled ? &trace_writer : NULL;
        tasks[t].trace_mutex = trace_enabled ? &trace_mutex : NULL;
        unsigned long long seed = base_seed + 0x9E3779B97F4A7C15ULL * (t + 1);
        tasks[t].rng_state = seed ? seed : (unsigned long long)(t + 1);
        offset += chunk;
    }

    SimulationTallies tallies = {0};
    tallies.total_neutrons = cfg.n;

    double start_time = 0.0;
    double finish_time = 0.0;
    GET_TIME(start_time);

    for (unsigned int t = 0; t < cfg.threads; ++t) {
        if (tasks[t].count == 0) {
            continue;
        }
        int rc = pthread_create(&threads[t], NULL, simulate_batch, &tasks[t]);
        if (rc != 0) {
            fprintf(stderr, "Error: pthread_create failed (%d)\n", rc);
            exit(EXIT_FAILURE);
        }
    }

    for (unsigned int t = 0; t < cfg.threads; ++t) {
        if (tasks[t].count == 0) {
            continue;
        }
        pthread_join(threads[t], NULL);
        tallies.absorbed += tasks[t].tallies.absorbed;
        tallies.transmitted += tasks[t].tallies.transmitted;
        tallies.reflected += tasks[t].tallies.reflected;
        tallies.scatter_events += tasks[t].tallies.scatter_events;
        tallies.absorption_events += tasks[t].tallies.absorption_events;
        tallies.total_collisions += tasks[t].tallies.total_collisions;
        tallies.total_track_length += tasks[t].tallies.total_track_length;
    }

    GET_TIME(finish_time);
    double elapsed_seconds = finish_time - start_time;

    char trace_summary_path[512] = {0};
    const char *trace_path_ptr = NULL;
    unsigned long trace_segments = 0UL;

    if (trace_enabled) {
        snprintf(trace_summary_path, sizeof(trace_summary_path), "%s", trace_writer.path);
        trace_segments = trace_writer.segments_written;
        trace_path_ptr = trace_summary_path;
        trace_writer_close(&trace_writer);
        pthread_mutex_destroy(&trace_mutex);
    }

    const char *summary_path = "./data/mc_slab_pthread_summary.json";
    FILE *summary_fp = open_data_file(summary_path, "w");
    if (!summary_fp) {
        fprintf(stderr, "Warning: unable to open summary file '%s' for writing\n", summary_path);
    }

    write_summary(stdout, &cfg, &tallies, trace_path_ptr, trace_segments, elapsed_seconds);
    if (summary_fp) {
        write_summary(summary_fp, &cfg, &tallies, trace_path_ptr, trace_segments, elapsed_seconds);
        fclose(summary_fp);
    }

    free(threads);
    free(tasks);

    return EXIT_SUCCESS;
}
