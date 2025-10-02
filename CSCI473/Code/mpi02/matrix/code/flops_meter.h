#ifndef FLOPS_METER_H
#define FLOPS_METER_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <float.h>
#include <stdint.h>

#ifdef USE_MPI
#include <mpi.h>
#define FM_TIME() MPI_Wtime()
#else
#include <sys/time.h>
static inline double FM_TIME(void)
{
    struct timeval tv;
    gettimeofday(&tv, NULL);
    return tv.tv_sec + tv.tv_usec * 1e-6;
}
#endif

#ifndef FLOPS_BACKEND
#define FLOPS_BACKEND 0 /* 0=analytic, 1=PAPI */
#endif
#if FLOPS_BACKEND == 1
#include <papi.h>
#endif

typedef struct
{
    double t_begin, t_accum, ops_accum;
    double best_ops, best_sec;
    int iters;
    int papi_ok;
#if FLOPS_BACKEND == 1
    int papi_event;
    long long papi_start;
#endif
} FlopsMeter;

/* -------- internal helpers -------- */
static inline void fm_init(FlopsMeter *m)
{
    memset(m, 0, sizeof(*m));
    m->best_sec = DBL_MAX;
#if FLOPS_BACKEND == 1
    m->papi_ok = 0;
    if (PAPI_library_init(PAPI_VER_CURRENT) == PAPI_VER_CURRENT)
    {
        int ev = PAPI_NULL;
        if (PAPI_query_event(PAPI_DP_OPS) == PAPI_OK)
            ev = PAPI_DP_OPS;
        else if (PAPI_query_event(PAPI_FP_OPS) == PAPI_OK)
            ev = PAPI_FP_OPS;
        else if (PAPI_query_event(PAPI_SP_OPS) == PAPI_OK)
            ev = PAPI_SP_OPS;
        if (ev != PAPI_NULL && PAPI_start_counters(&ev, 1) == PAPI_OK)
        {
            m->papi_event = ev;
            m->papi_ok = 1;
        }
    }
#endif
}
static inline void fm_fini(FlopsMeter *m)
{
#if FLOPS_BACKEND == 1
    if (m->papi_ok)
    {
        long long tmp;
        PAPI_stop_counters(&tmp, 1);
    }
#endif
}
static inline void fm_begin(FlopsMeter *m)
{
#if FLOPS_BACKEND == 1
    if (m->papi_ok)
    {
        long long now = 0;
        PAPI_read_counters(&now, 1);
        m->papi_start = now;
    }
#endif
    m->t_begin = FM_TIME();
}
static inline void fm_end(FlopsMeter *m, double analytic_ops)
{
    double dt = FM_TIME() - m->t_begin;
    double ops = analytic_ops;
#if FLOPS_BACKEND == 1
    if (m->papi_ok)
    {
        long long now = 0;
        PAPI_read_counters(&now, 1);
        long long diff = now - m->papi_start;
        if (diff > 0)
            ops = (double)diff;
    }
#endif
    m->t_accum += dt;
    m->ops_accum += ops;
    m->iters++;
    if (dt > 0.0)
    {
        double gf = (ops / dt) / 1e9;
        double best = (m->best_sec < DBL_MAX && m->best_sec > 0.0) ? (m->best_ops / m->best_sec) / 1e9 : -1.0;
        if (gf > best)
        {
            m->best_ops = ops;
            m->best_sec = dt;
        }
    }
}
static inline void fm_local(const FlopsMeter *m, double *ops, double *sec, double *avg, double *peak)
{
    *ops = m->ops_accum;
    *sec = m->t_accum;
    *avg = (m->t_accum > 0) ? (m->ops_accum / m->t_accum) / 1e9 : 0.0;
    *peak = (m->best_sec > 0 && m->best_sec < DBL_MAX) ? (m->best_ops / m->best_sec) / 1e9 : 0.0;
}

/* -------- dual meter: overall + section (compute-only) -------- */
typedef struct
{
    FlopsMeter overall; // your current iteration scope
    FlopsMeter section; // wrap only matrix-multiply with this
} FlopsDual;

static inline void flops_dual_init(FlopsDual *d)
{
    fm_init(&d->overall);
    fm_init(&d->section);
}
static inline void flops_dual_fini(FlopsDual *d)
{
    fm_fini(&d->section);
    fm_fini(&d->overall);
}

/* iteration boundaries (overall) */
static inline void flops_iter_begin(FlopsDual *d) { fm_begin(&d->overall); }
static inline void flops_iter_end(FlopsDual *d, double analytic_ops_total) { fm_end(&d->overall, analytic_ops_total); }

/* matrix-multiply (compute-only) subregion */
static inline void flops_section_begin(FlopsDual *d) { fm_begin(&d->section); }
static inline void flops_section_end(FlopsDual *d, double analytic_ops_section) { fm_end(&d->section, analytic_ops_section); }

/* -------- CSV logging (rank 0 only) -------- */
static inline void write_header_if_needed(FILE *f)
{
    fseek(f, 0, SEEK_END);
    if (ftell(f) == 0)
    {
        fprintf(f, "iteration,label,ranks,rank,"
                   "overall_avg,overall_peak,job_avg,job_peak_rank,"
                   "section_avg,section_peak,section_job_avg,section_job_peak_rank\n");
        fflush(f);
    }
}

static inline void flops_log_iteration_csv(FlopsDual *d, int iter, const char *label, const char *path
#ifdef USE_MPI
                                           ,
                                           MPI_Comm comm
#endif
)
{
    /* overall local */
    double o_ops, o_sec, o_avg, o_peak;
    fm_local(&d->overall, &o_ops, &o_sec, &o_avg, &o_peak);
    /* section local */
    double s_ops, s_sec, s_avg, s_peak;
    fm_local(&d->section, &s_ops, &s_sec, &s_avg, &s_peak);

#ifdef USE_MPI
    int rank = 0, size = 1;
    MPI_Comm_rank(comm, &rank);
    MPI_Comm_size(comm, &size);

    /* overall job aggregates */
    double o_sum_ops = 0.0, o_max_sec = 0.0, o_peak_rank = 0.0;
    MPI_Reduce(&o_ops, &o_sum_ops, 1, MPI_DOUBLE, MPI_SUM, 0, comm);
    MPI_Reduce(&o_sec, &o_max_sec, 1, MPI_DOUBLE, MPI_MAX, 0, comm);
    MPI_Reduce(&o_peak, &o_peak_rank, 1, MPI_DOUBLE, MPI_MAX, 0, comm);
    double o_job_avg = (o_max_sec > 0.0) ? (o_sum_ops / o_max_sec) / 1e9 : 0.0;

    /* section job aggregates */
    double s_sum_ops = 0.0, s_max_sec = 0.0, s_peak_rank_job = 0.0;
    MPI_Reduce(&s_ops, &s_sum_ops, 1, MPI_DOUBLE, MPI_SUM, 0, comm);
    MPI_Reduce(&s_sec, &s_max_sec, 1, MPI_DOUBLE, MPI_MAX, 0, comm);
    MPI_Reduce(&s_peak, &s_peak_rank_job, 1, MPI_DOUBLE, MPI_MAX, 0, comm);
    double s_job_avg = (s_max_sec > 0.0) ? (s_sum_ops / s_max_sec) / 1e9 : 0.0;

    if (rank == 0)
    {
        FILE *f = fopen(path, "ab+");
        if (!f)
            return;
        write_header_if_needed(f);
        fprintf(f, "%d,%s,%d,%d,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f\n",
                iter, (label ? label : ""), size, 0,
                o_avg, o_peak, o_job_avg, o_peak_rank,
                s_avg, s_peak, s_job_avg, s_peak_rank_job);
        fflush(f);
        fclose(f);
    }
#else
    /* sequential: job==local */
    FILE *f = fopen(path, "ab+");
    if (!f)
        return;
    write_header_if_needed(f);
    fprintf(f, "%d,%s,%d,%d,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f,%.9f\n",
            iter, (label ? label : ""), 1, 0,
            o_avg, o_peak, o_avg, o_peak,
            s_avg, s_peak, s_avg, s_peak);
    fflush(f);
    fclose(f);
#endif
}

#endif /* FLOPS_METER_H */
