#!/usr/bin/env python3
"""
bench_stencil2d_pthreads.py

Benchmark driver + plotter to collect timing information and generate
timing, speedup, efficiency, and iso-efficiency plots as a function of:
  - SIZE (N), NUM_THREADS (T), and NUM_ITERATIONS (I).

Adds a global timeout: if total runtime exceeds 26 minutes, the program
generates plots from the partial data collected so far, prints a message,
and exits cleanly.

Required:
  --testing-dir TESTING_DIR
  --make MAKE
  --N1 N1 --N2 N2 --Nstep NSTEP
  --I1 I1 --I2 I2 --Istep ISTEP
  --T1 T1 --T2 T2 --Tstep TSTEP

Optional:
  --serial SERIAL   (default ./code/stencil-2d)
  --pth PTH         (default ./code/pth-stencil-2d)
  --reps REPS       (default 3; best-of)
  --warmup WARMUP   (default 1; not timed)
  --keep            (keep per-case dirs)
"""

import argparse
import os
import sys
import shutil
import time
import subprocess
from pathlib import Path
import csv
from collections import defaultdict

# Headless plotting
import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt

# ------------------------- CONFIG -------------------------
MAX_RUNTIME_SECS = 26 * 60  # 26 minutes hard cap

# ------------------------- CLI -------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark serial vs pthread stencil across N, I, T; collect CSV + plots (with global timeout)."
    )
    # Required
    p.add_argument("--testing-dir", required=True, help="Output directory for runs, CSV, and plots")
    p.add_argument("--make", required=True, help="Path to make-2d executable")
    p.add_argument("--N1", type=int, required=True); p.add_argument("--N2", type=int, required=True); p.add_argument("--Nstep", type=int, required=True)
    p.add_argument("--I1", type=int, required=True); p.add_argument("--I2", type=int, required=True); p.add_argument("--Istep", type=int, required=True)
    p.add_argument("--T1", type=int, required=True); p.add_argument("--T2", type=int, required=True); p.add_argument("--Tstep", type=int, required=True)
    # Optional
    p.add_argument("--serial", default="./code/stencil-2d", help="Path to serial executable")
    p.add_argument("--pth",    default="./code/pth-stencil-2d", help="Path to pthread executable")
    p.add_argument("--reps", type=int, default=3, help="Timed repetitions (best-of)")
    p.add_argument("--warmup", type=int, default=1, help="Warmup runs (not timed)")
    p.add_argument("--keep", action="store_true", help="Keep per-case dirs")
    a = p.parse_args()

    # Validations
    if a.N1 < 3 or a.N2 < a.N1 or a.Nstep <= 0: sys.exit("Invalid N range")
    if a.I1 < 0 or a.I2 < a.I1 or a.Istep <= 0: sys.exit("Invalid I range")
    if a.T1 < 1 or a.T2 < a.T1 or a.Tstep <= 0: sys.exit("Invalid T range")
    if a.reps < 1 or a.warmup < 0: sys.exit("Invalid reps/warmup")

    for path, label in [(a.make,"make-2d"), (a.serial,"serial"), (a.pth,"pth")]:
        if not Path(path).resolve().exists():
            sys.exit(f"Error: {label} not found: {path}")

    return a

# ------------------------- helpers -------------------------

def run_cmd(cmd, cwd: Path):
    res = subprocess.run(cmd, cwd=str(cwd), text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode, res.stdout, res.stderr

def time_cmd(cmd, cwd: Path, warmup: int, reps: int):
    for _ in range(warmup):
        subprocess.run(cmd, cwd=str(cwd), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    times = []
    last = (0,"","")
    for _ in range(reps):
        t0 = time.perf_counter()
        r = subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        dt = time.perf_counter() - t0
        times.append(dt)
        last = (r.returncode, r.stdout, r.stderr)
    best = min(times) if times else float("inf")
    return best, times, last

def locate_make2d_initial(make_path: Path) -> Path:
    candidates = [
        make_path.parent.parent / "data" / "initial.dat",  # ../data/initial.dat relative to code/
        make_path.parent / "initial.dat",                  # code/initial.dat
    ]
    for c in candidates:
        if c.exists():
            return c
    return None

def serial_stack_name(N: int, I: int) -> str:
    return f"all.{N}x{N}x{I}.dat"

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def save_line(x, ys, labels, title, xlabel, ylabel, out_path, ylimit=None):
    plt.figure(figsize=(7,4))
    for y, lab in zip(ys, labels):
        plt.plot(x, y, marker="o", label=lab)
    plt.title(title)
    plt.xlabel(xlabel); plt.ylabel(ylabel)
    if ylimit is not None:
        plt.ylim(0, ylimit)
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    if any(labels):
        plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()

# ------------------------- plotting (reusable) -------------------------

def generate_plots(plots_dir: Path,
                   times_serial, times_pth, speedup_map, eff_map,
                   Ts_by_key, Ns_by_key, Is_by_key):
    ensure_dir(plots_dir)

    # (1) vs Threads, per (N,I)
    all_time_vals = []
    all_speed_vals = []
    all_eff_vals = []
    for key in times_serial:
        if key in ("_N","_I"): continue
        all_time_vals += times_serial[key] + times_pth[key]
        all_speed_vals += speedup_map[key]
        all_eff_vals += eff_map[key]
    y_time_max = max(all_time_vals) if all_time_vals else 1.0
    y_speed_max = max(all_speed_vals) if all_speed_vals else 1.0
    y_eff_max = max(1.0, max(all_eff_vals) if all_eff_vals else 1.0)

    for (N,I), Ts in Ts_by_key.items():
        z = list(zip(Ts, times_serial[(N,I)], times_pth[(N,I)], speedup_map[(N,I)], eff_map[(N,I)]))
        z.sort(key=lambda x: x[0])
        Ts_sorted = [t for t, *_ in z]
        s_sorted  = [s for _, s, _, _, _ in z]
        p_sorted  = [p for _, _, p, _, _ in z]
        sp_sorted = [sp for *_, sp, _ in z]
        ef_sorted = [ef for *_, ef in z]

        base = plots_dir / f"N{N}_I{I}"
        ensure_dir(base)
        save_line(Ts_sorted, [s_sorted, p_sorted], ["Serial","Pthreads"],
                  f"Timing vs Threads (N={N}, I={I})", "Threads", "Seconds",
                  base / "timing_vs_threads.png", ylimit=y_time_max)
        save_line(Ts_sorted, [sp_sorted], ["Speedup"],
                  f"Speedup vs Threads (N={N}, I={I})", "Threads", "Speedup",
                  base / "speedup_vs_threads.png", ylimit=y_speed_max)
        save_line(Ts_sorted, [ef_sorted], ["Efficiency"],
                  f"Efficiency vs Threads (N={N}, I={I})", "Threads", "Efficiency",
                  base / "efficiency_vs_threads.png", ylimit=y_eff_max)

    # (2) vs Size, per (T,I)
    all_time_vals_N = []
    all_speed_vals_N = []
    all_eff_vals_N = []
    for key, vals in times_serial.get("_N", {}).items():
        all_time_vals_N += vals + times_pth["_N"][key]
        all_speed_vals_N += speedup_map["_N"][key]
        all_eff_vals_N += eff_map["_N"][key]
    y_time_max_N = max(all_time_vals_N) if all_time_vals_N else 1.0
    y_speed_max_N = max(all_speed_vals_N) if all_speed_vals_N else 1.0
    y_eff_max_N = max(1.0, max(all_eff_vals_N) if all_eff_vals_N else 1.0)

    for (T,I), s_list in times_serial.get("_N", {}).items():
        Ns = Ns_by_key[(T,I)]
        z = list(zip(Ns, s_list, times_pth["_N"][(T,I)], speedup_map["_N"][(T,I)], eff_map["_N"][(T,I)]))
        z.sort(key=lambda x: x[0])
        Ns_sorted = [n for n, *_ in z]
        s_sorted  = [s for _, s, _, _, _ in z]
        p_sorted  = [p for _, _, p, _, _ in z]
        sp_sorted = [sp for *_, sp, _ in z]
        ef_sorted = [ef for *_, ef in z]

        base = plots_dir / f"T{T}_I{I}"
        ensure_dir(base)
        save_line(Ns_sorted, [s_sorted, p_sorted], ["Serial","Pthreads"],
                  f"Timing vs Size (T={T}, I={I})", "Size N", "Seconds",
                  base / "timing_vs_size.png", ylimit=y_time_max_N)
        save_line(Ns_sorted, [sp_sorted], ["Speedup"],
                  f"Speedup vs Size (T={T}, I={I})", "Size N", "Speedup",
                  base / "speedup_vs_size.png", ylimit=y_speed_max_N)
        save_line(Ns_sorted, [ef_sorted], ["Efficiency"],
                  f"Efficiency vs Size (T={T}, I={I})", "Size N", "Efficiency",
                  base / "efficiency_vs_size.png", ylimit=y_eff_max_N)

    # (3) vs Iterations, per (N,T)
    all_time_vals_I = []
    all_speed_vals_I = []
    all_eff_vals_I = []
    for key, vals in times_serial.get("_I", {}).items():
        all_time_vals_I += vals + times_pth["_I"][key]
        all_speed_vals_I += speedup_map["_I"][key]
        all_eff_vals_I += eff_map["_I"][key]
    y_time_max_I = max(all_time_vals_I) if all_time_vals_I else 1.0
    y_speed_max_I = max(all_speed_vals_I) if all_speed_vals_I else 1.0
    y_eff_max_I = max(1.0, max(all_eff_vals_I) if all_eff_vals_I else 1.0)

    for (N,T), s_list in times_serial.get("_I", {}).items():
        Is = Is_by_key[(N,T)]
        z = list(zip(Is, s_list, times_pth["_I"][(N,T)], speedup_map["_I"][(N,T)], eff_map["_I"][(N,T)]))
        z.sort(key=lambda x: x[0])
        Is_sorted = [i for i, *_ in z]
        s_sorted  = [s for _, s, _, _, _ in z]
        p_sorted  = [p for _, _, p, _, _ in z]
        sp_sorted = [sp for *_, sp, _ in z]
        ef_sorted = [ef for *_, ef in z]

        base = plots_dir / f"N{N}_T{T}"
        ensure_dir(base)
        save_line(Is_sorted, [s_sorted, p_sorted], ["Serial","Pthreads"],
                  f"Timing vs Iterations (N={N}, T={T})", "Iterations I", "Seconds",
                  base / "timing_vs_iterations.png", ylimit=y_time_max_I)
        save_line(Is_sorted, [sp_sorted], ["Speedup"],
                  f"Speedup vs Iterations (N={N}, T={T})", "Iterations I", "Speedup",
                  base / "speedup_vs_iterations.png", ylimit=y_speed_max_I)
        save_line(Is_sorted, [ef_sorted], ["Efficiency"],
                  f"Efficiency vs Iterations (N={N}, T={T})", "Iterations I", "Efficiency",
                  base / "efficiency_vs_iterations.png", ylimit=y_eff_max_I)

    # (4) Iso-efficiency curves
    iso_targets = [0.5, 0.7, 0.9]
    eff_data = defaultdict(dict)  # (I,T) -> {N: eff}
    for key in times_serial:
        if key in ("_N","_I"): continue
        N, I = key
        Ts = sorted(range(len(times_serial[key])), key=lambda idx: idx)  # index-based
        for T, e in zip(Ts_by_key[(N,I)], eff_map[(N,I)]):
            eff_data[(I,T)][N] = e

    for base_key in eff_data.keys():
        # nothing to do here; actual plotting grouped per I below
        pass

    I_values = sorted({k[0] for k in eff_data.keys()})
    for I in I_values:
        base = plots_dir / f"iso_efficiency_I{I}"
        ensure_dir(base)
        T_vals = sorted({k[1] for k in eff_data.keys() if k[0] == I})
        for target in iso_targets:
            x, y = [], []
            for T in T_vals:
                Ns_effs = eff_data.get((I,T), {})
                feasible = [n for n, e in Ns_effs.items() if e >= target]
                if feasible:
                    x.append(T); y.append(min(feasible))
            if x:
                save_line(x, [y], [f"iso-eff {target:.1f}"],
                          f"Iso-efficiency (I={I}, target={target:.1f})",
                          "Threads", "Minimal N achieving efficiency",
                          base / f"iso_eff_target_{int(target*100)}.png")

# ------------------------- main -------------------------

def main():
    a = parse_args()
    testing_dir = Path(a.testing_dir).resolve()
    ensure_dir(testing_dir)
    plots_dir = testing_dir / "plots"
    ensure_dir(plots_dir)

    serial = Path(a.serial).resolve()
    pth    = Path(a.pth).resolve()
    make   = Path(a.make).resolve()
    results_csv = testing_dir / "bench_results.csv"

    # CSV header
    with open(results_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["N","I","T","serial_time_s","pth_time_s","speedup","efficiency",
                         "serial_times_all","pth_times_all","serial_cmd","pth_cmd","case_dir"])

    # In-memory collections for plotting
    times_serial = defaultdict(list)   # key (N,I) -> list over T
    times_pth    = defaultdict(list)
    speedup_map  = defaultdict(list)
    eff_map      = defaultdict(list)
    Ts_by_key    = defaultdict(list)   # (N,I) -> list of T (x-axis for vs-threads)
    Ns_by_key    = defaultdict(list)   # (T,I) -> list of N (x-axis for vs-size)
    Is_by_key    = defaultdict(list)   # (N,T) -> list of I (x-axis for vs-iterations)
    # Mirrors for vs-size and vs-iter families
    times_serial["_N"] = {}
    times_pth["_N"] = {}
    speedup_map["_N"] = {}
    eff_map["_N"] = {}

    times_serial["_I"] = {}
    times_pth["_I"] = {}
    speedup_map["_I"] = {}
    eff_map["_I"] = {}

    total_cases = 0
    start_time = time.perf_counter()

    def maybe_timeout_and_exit():
        # If exceeded MAX_RUNTIME_SECS, generate plots with current data and exit cleanly
        elapsed = time.perf_counter() - start_time
        if elapsed > MAX_RUNTIME_SECS:
            print("\n⚠️  Global timeout reached (26 minutes).")
            print(f"Elapsed: {elapsed/60:.1f} minutes. Saving progress and generating partial plots...")
            generate_plots(plots_dir, times_serial, times_pth, speedup_map, eff_map,
                           Ts_by_key, Ns_by_key, Is_by_key)
            print("Partial CSV and plots written.")
            print(f"CSV:   {results_csv}")
            print(f"Plots: {plots_dir}")
            sys.exit(0)

    for N in range(a.N1, a.N2 + 1, a.Nstep):
        for I in range(a.I1, a.I2 + 1, a.Istep):
            for T in range(a.T1, a.T2 + 1, a.Tstep):
                total_cases += 1
                case_dir = testing_dir / f"N{N}_I{I}_T{T}"
                if case_dir.exists(): shutil.rmtree(case_dir)
                ensure_dir(case_dir)

                initial = case_dir / "initial.dat"
                serial_final = case_dir / "serial_final.dat"
                pth_final    = case_dir / "pth_final.dat"
                serial_stack = case_dir / serial_stack_name(N, I)
                pth_stack    = case_dir / "pth_stack.dat"

                # 1) make-2d N N
                rc, out, err = run_cmd([str(make), str(N), str(N)], cwd=make.parent)
                if rc != 0:
                    print(err, file=sys.stderr)
                    sys.exit(f"make-2d failed:\n{out}\n{err}")
                src_initial = locate_make2d_initial(make)
                if not src_initial:
                    sys.exit("Could not locate initial.dat created by make-2d.")
                shutil.copy2(src_initial, initial)

                # 2) serial
                serial_cmd = [str(serial), "initial.dat", "serial_final.dat", str(I)]
                Ts_best, Ts_all, (rc_s, so_s, se_s) = time_cmd(serial_cmd, case_dir, a.warmup, a.reps)
                if rc_s != 0:
                    print(se_s, file=sys.stderr)
                    sys.exit(f"serial failed:\n{so_s}\n{se_s}")
                if not serial_stack.exists():
                    sys.exit(f"serial stack missing: {serial_stack}")

                # 3) pthread
                pth_cmd = [str(pth), "-n", str(I), "-I", "initial.dat", "-o", "pth_final.dat", "-t", str(T), "-s", "pth_stack.dat"]
                Tp_best, Tp_all, (rc_p, so_p, se_p) = time_cmd(pth_cmd, case_dir, a.warmup, a.reps)
                if rc_p != 0:
                    print(se_p, file=sys.stderr)
                    sys.exit(f"pth failed:\n{so_p}\n{se_p}")

                # 4) metrics
                speed = Ts_best / Tp_best if Tp_best > 0 else float("inf")
                eff   = speed / T

                # 5) CSV row
                with open(results_csv, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([N, I, T,
                                     f"{Ts_best:.9f}", f"{Tp_best:.9f}",
                                     f"{speed:.6f}", f"{eff:.6f}",
                                     ";".join(f"{x:.9f}" for x in Ts_all),
                                     ";".join(f"{x:.9f}" for x in Tp_all),
                                     " ".join(serial_cmd), " ".join(pth_cmd),
                                     str(case_dir)])

                print(f"[N={N:4d} I={I:3d} T={T:3d}] Ts={Ts_best:.4f}s Tp={Tp_best:.4f}s S={speed:.3f} E={eff:.3f}")

                # 6) collect for plots
                # (a) per (N,I): x=T
                key_NI = (N, I)
                Ts_by_key[key_NI].append(T)
                times_serial[key_NI].append(Ts_best)
                times_pth[key_NI].append(Tp_best)
                speedup_map[key_NI].append(speed)
                eff_map[key_NI].append(eff)

                # (b) per (T,I): x=N
                key_TI = (T, I)
                Ns_by_key[key_TI].append(N)
                times_serial["_N"].setdefault(key_TI, []).append(Ts_best)
                times_pth["_N"].setdefault(key_TI, []).append(Tp_best)
                speedup_map["_N"].setdefault(key_TI, []).append(speed)
                eff_map["_N"].setdefault(key_TI, []).append(eff)

                # (c) per (N,T): x=I
                key_NT = (N, T)
                Is_by_key[key_NT].append(I)
                times_serial["_I"].setdefault(key_NT, []).append(Ts_best)
                times_pth["_I"].setdefault(key_NT, []).append(Tp_best)
                speedup_map["_I"].setdefault(key_NT, []).append(speed)
                eff_map["_I"].setdefault(key_NT, []).append(eff)

                # 7) cleanup per-case unless keep
                if not a.keep:
                    shutil.rmtree(case_dir)

                # 8) timeout check (after each case)
                maybe_timeout_and_exit()

    # Finished all cases within time: generate plots
    generate_plots(plots_dir, times_serial, times_pth, speedup_map, eff_map,
                   Ts_by_key, Ns_by_key, Is_by_key)

    print("\nBenchmark complete.")
    print(f"Total cases: {total_cases}")
    print(f"CSV: {results_csv}")
    print(f"Plots: {plots_dir}")

if __name__ == "__main__":
    main()
