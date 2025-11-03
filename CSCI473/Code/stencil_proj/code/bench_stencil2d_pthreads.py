#!/usr/bin/env python3
"""
File / Function / Class name
  File: bench_stencil2d_pthreads.py
  Desc:
    Benchmark pthread-based 2D stencil (pth-stencil-2d) over problem size N,
    number of threads P, and number of iterations I. It:
      * Calls make-2d to generate initial.dat in ../data.
      * Runs the serial stencil-2d to get baseline timing.
      * Runs the parallel pth-stencil-2d with various P.
      * Collects timing data, computes speedup and efficiency.
      * Generates timing, speedup, efficiency and iso-efficiency plots.
      * Writes CSVs and a text report into --results-dir.

  Variables:
    (see main() and benchmark() for detailed arguments/locals)

  Returns
    None (writes files to disk and prints status to console)
"""

import argparse
import csv
import math
import os
import sys
import time
import subprocess

import numpy as np
import matplotlib
matplotlib.use("Agg")  # no GUI needed
import matplotlib.pyplot as plt


# ============================================================
# Utility helpers
# ============================================================

def log(msg: str):
    """Print a message with a timestamp."""
    ts = time.strftime("[%Y-%m-%d %H:%M:%S]")
    print(f"{ts} {msg}")


def run_command(cmd, timeout_sec, env=None):
    """
    File / Function / Class name
      Function: run_command
      Desc:
        Run a subprocess command with a timeout. Capture stdout/stderr.

      Variables:
        cmd (list[str])     - Command and arguments to execute.
        timeout_sec (float) - Timeout in seconds.

      env (dict|None)        - Optional environment overrides.

      Returns
        elapsed (float) - Elapsed wall-clock time in seconds (0 if failed).
        ok (bool)       - True if returncode == 0 and no timeout.
        err (str)       - Error description if not ok, else "".
    """
    start = time.time()
    try:
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_sec,
            check=False,
            env=env,
        )
        elapsed = time.time() - start
        if proc.returncode != 0:
            return elapsed, False, f"returncode={proc.returncode}"
        return elapsed, True, ""
    except FileNotFoundError:
        elapsed = time.time() - start
        return elapsed, False, "Executable not found"
    except subprocess.TimeoutExpired:
        elapsed = time.time() - start
        return elapsed, False, "Timeout"
    except Exception as e:
        elapsed = time.time() - start
        return elapsed, False, f"Exception: {e}"


def write_csv(path, header, rows):
    """
    Function: write_csv
    Desc: Write a CSV file given header and rows.

    Variables:
      path (str)         - Path to CSV file.
      header (list[str]) - Column names.
      rows (list[list])  - Data rows.

    Returns
      None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        if header is not None:
            w.writerow(header)
        w.writerows(rows)


def append_log(path, msg):
    """
    Function: append_log
    Desc: Append a line to an error log file.

    Variables:
      path (str) - Path to log file.
      msg (str)  - Line of text to append.

    Returns
      None
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "a", newline="") as f:
        f.write(msg + "\n")


# ============================================================
# Plot helpers
# ============================================================

def plot_lines_by_P(
    out_png,
    title,
    ylabel,
    P_values,
    N_values,
    data_dict,
    y_min=0.0,
    y_max=None,
):
    """
    Function: plot_lines_by_P
    Desc:
      Make a line plot where each curve is for a fixed P and x-axis is N.

    Variables:
      out_png (str)      - Output PNG path.
      title (str)        - Plot title.
      ylabel (str)       - Y-axis label.
      P_values (list[int]) - List of P's (threads).
      N_values (list[int]) - Sorted list of N's.
      data_dict (dict)   - (P,N)->y_value mapping; missing entries skipped.
      y_min (float)      - Lower y-axis limit.
      y_max (float|None) - Upper y-axis; if None, auto via data.

    Returns
      None
    """
    plt.figure(figsize=(7, 5))
    all_ys = []
    for P in P_values:
        xs = []
        ys = []
        for N in sorted(N_values):
            val = data_dict.get((P, N), None)
            if val is None or math.isnan(val):
                continue
            xs.append(N)
            ys.append(val)
            all_ys.append(val)
        if xs:
            plt.plot(xs, ys, marker="o", label=f"P={P}")

    if not all_ys:
        # No valid data; skip plotting
        plt.close()
        return

    if y_max is None:
        y_max = max(all_ys) * 1.1

    plt.xlabel("Problem Size N")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.ylim(y_min, y_max)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()


def _compute_iso_curve(eff_target, P_values, sorted_N_values, avg_eff_by_PN):
    """Compute minimal N per P needed to reach eff_target."""
    xs = list(P_values)
    ys = []
    for P in P_values:
        best_N = None
        for N in sorted_N_values:
            eff_val = avg_eff_by_PN.get((P, N))
            if eff_val is None or math.isnan(eff_val):
                continue
            if eff_val >= eff_target:
                best_N = N
                break
        ys.append(best_N if best_N is not None else np.nan)
    return xs, ys


def plot_iso_efficiency(
    out_png,
    title,
    eff_targets,
    P_values,
    N_values,
    avg_eff_by_PN,
):
    """
    Function: plot_iso_efficiency
    Desc:
      Plot iso-efficiency curves for multiple efficiency targets, rendering
      each target as a distinct line on a single graph.

    Variables:
      out_png (str)           - Output PNG path.
      title (str)             - Plot title.
      eff_targets (list[float]) - Efficiency targets to plot.
      P_values (list[int])    - Thread counts to show on x-axis.
      N_values (list[int])    - Sorted list of problem sizes N.
      avg_eff_by_PN (dict)    - (P,N)->avg efficiency across iterations.

    Returns
      None
    """
    if not eff_targets:
        return

    curves = []
    sorted_N_values = sorted(N_values)
    for E in eff_targets:
        xs, ys = _compute_iso_curve(E, P_values, sorted_N_values, avg_eff_by_PN)
        arr = np.array(ys, dtype=float)
        if np.all(np.isnan(arr)):
            continue
        curves.append((E, xs, arr))

    if not curves:
        return

    plt.figure(figsize=(7, 5))
    for E, xs, ys in curves:
        plt.plot(xs, ys, marker="o", label=f"{E * 100:.0f}%")

    plt.xlabel("Number of Processes (P)")
    plt.ylabel("Problem Size N")
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(P_values)
    plt.legend(title="Efficiency (%)")
    plt.tight_layout()
    plt.savefig(out_png, dpi=150)
    plt.close()


# ============================================================
# Benchmark core
# ============================================================

def benchmark(args):
    """
    Function: benchmark
    Desc:
      Main benchmarking loop over (N, I, P). Calls make-2d, serial stencil-2d,
      and pth-stencil-2d, collects timings, computes speedup/efficiency, and
      produces CSVs + plots.

    Variables:
      args (Namespace) - Parsed command-line arguments.

    Returns
      None
    """
    results_dir = args.results_dir
    os.makedirs(results_dir, exist_ok=True)

    label = args.label if args.label else "run"

    dat_csv     = os.path.join(results_dir, f"dat_runs-{label}.csv")
    summary_csv = os.path.join(results_dir, f"summary-{label}.csv")
    report_txt  = os.path.join(results_dir, f"report-{label}.txt")
    err_log     = os.path.join(results_dir, f"errors-{label}.log")

    serial_env = os.environ.copy()
    serial_env["STENCIL_DISABLE_STACK"] = "1"

    # --------------------------------------------------------
    # Build N, P, I lists
    # --------------------------------------------------------
    # N choices:
    if args.N_start > 0 and args.N_max > 0:
        Ns = []
        n = args.N_start
        while n <= args.N_max:
            Ns.append(n)
            n *= 2
    else:
        if args.num_Ns < 1:
            raise ValueError("num_Ns must be >=1 when using N1/N2 range")
        if args.N2 < args.N1:
            raise ValueError("N2 must be >= N1")
        Ns = np.linspace(args.N1, args.N2, args.num_Ns, dtype=int).tolist()

    # P choices:
    if args.Ps:
        Ps = [int(p) for p in args.Ps]
    else:
        Ps = list(range(args.P_start, args.P_max + 1, args.P_step))

    # I choices:
    if args.Is:
        Is = [int(i) for i in args.Is]
    else:
        Is = list(range(args.I1, args.I2 + 1, args.Istep))

    # Efficiency targets:
    eff_targets = []
    if args.eff_targets:
        # Comma-separated, possibly with spaces: "0.3,0.5,0.7"
        for tok in args.eff_targets.split(","):
            tok = tok.strip()
            if tok:
                eff_targets.append(float(tok))
    elif args.eff_range:
        # Format: "start step" e.g. "0.29 0.05"
        parts = args.eff_range.split()
        if len(parts) == 2:
            start = float(parts[0])
            step  = float(parts[1])
            e = start
            while e < 1.0:
                eff_targets.append(e)
                e += step

    if eff_targets:
        eff_targets = sorted(set(eff_targets))

    # --------------------------------------------------------
    # Data structures to hold results
    # --------------------------------------------------------
    dat_rows = []      # raw data per trial
    summary_rows = []  # averaged data per (N,I,P)

    # For iso-efficiency: we want avg efficiency over I for each (P,N)
    eff_vals_by_PN = {}  # (P,N)->list of efficiencies

    total_cases = len(Ns) * len(Is) * len(Ps)
    case_idx = 0

    # --------------------------------------------------------
    # Benchmark loops
    # --------------------------------------------------------
    for N in Ns:
        for I in Is:
            # === Serial baseline ===
            # Use make-2d to generate input in ../data
            make_cmd = [args.make_exe, str(N), str(N)]
            _, ok_m, err_m = run_command(make_cmd, args.timeout_sec)
            if not ok_m:
                msg = f"ERROR: N={N}, I={I}, serial make-2d failed ({err_m})"
                log(msg)
                append_log(err_log, msg)
                # Skip this (N,I) entirely
                continue

            # Serial: use stack disabled (no "-s") for performance
            serial_cmd = [
                args.serial_exe,
                "../data/initial.dat",
                "../data/final_serial.dat",
                str(I),
            ]

            # Warmup serial
            for _ in range(args.warmup):
                _, ok_s_w, err_s_w = run_command(serial_cmd, args.timeout_sec, env=serial_env)
                if not ok_s_w:
                    msg = f"ERROR: N={N}, I={I}, serial warmup failed ({err_s_w})"
                    log(msg)
                    append_log(err_log, msg)
                    break

            # Timed serial trials
            serial_times = []
            for _ in range(args.trials):
                t, ok_s, err_s = run_command(serial_cmd, args.timeout_sec, env=serial_env)
                if not ok_s:
                    msg = f"ERROR: N={N}, I={I}, serial run failed ({err_s})"
                    log(msg)
                    append_log(err_log, msg)
                else:
                    serial_times.append(t)
                    dat_rows.append(["serial", N, I, 1, t])

            if not serial_times:
                # No valid serial runs; can't compute speedup/eff; skip all P
                continue

            t_serial = float(np.mean(serial_times))

            # === Parallel runs for each P ===
            for P in Ps:
                case_idx += 1
                log(f"[{case_idx:4d}/{total_cases:4d}] N={N:5d} I={I:4d} P={P:3d} — trials={args.trials}")

                pth_cmd = [
                    args.pth_exe,
                    "-n", str(I),
                    "-I", "../data/initial.dat",
                    "-o", "../data/final_pth.dat",
                    "-t", str(P),
                ]

                # warmup
                for _ in range(args.warmup):
                    _, ok_p_w, err_p_w = run_command(pth_cmd, args.timeout_sec)
                    if not ok_p_w:
                        msg = f"ERROR: N={N}, I={I}, P={P}, warmup failed ({err_p_w})"
                        log(msg)
                        append_log(err_log, msg)
                        break

                # timed trials
                pth_times = []
                for _ in range(args.trials):
                    t, ok_p, err_p = run_command(pth_cmd, args.timeout_sec)
                    if not ok_p:
                        msg = f"ERROR: N={N}, I={I}, P={P}, run failed ({err_p})"
                        log(msg)
                        append_log(err_log, msg)
                    else:
                        pth_times.append(t)
                        dat_rows.append(["pth", N, I, P, t])

                if not pth_times:
                    # No valid data for this (N,I,P)
                    continue

                t_pth = float(np.mean(pth_times))
                speedup = t_serial / t_pth
                eff = speedup / P

                summary_rows.append([N, I, P, t_serial, t_pth, speedup, eff])

                # For iso-efficiency averaging: accumulate eff per (P,N)
                key = (P, N)
                eff_vals_by_PN.setdefault(key, []).append(eff)

    # --------------------------------------------------------
    # Write raw and summary CSVs
    # --------------------------------------------------------
    if dat_rows:
        write_csv(
            dat_csv,
            ["impl", "N", "I", "P", "time"],
            dat_rows,
        )

    if not summary_rows:
        log("No successful runs; summary CSV will be empty.")
        write_csv(summary_csv, ["N", "I", "P", "t_serial", "t_pth", "speedup", "efficiency"], [])
        return

    write_csv(
        summary_csv,
        ["N", "I", "P", "t_serial", "t_pth", "speedup", "efficiency"],
        summary_rows,
    )

    # --------------------------------------------------------
    # Build maps for plotting
    # --------------------------------------------------------
    Ns_seen = sorted({row[0] for row in summary_rows})
    Ps_seen = sorted({row[2] for row in summary_rows})

    speed_by_PN_Imin = {}
    eff_by_PN_Imin = {}
    time_by_PN_Imin = {}

    # Choose minimal I per (N,P) for plotting "by N" (could also choose max or average).
    # Here we simply keep the *first* I encountered or average across I for times.
    # To keep it simple: use average over I for time, speed, and efficiency.
    accum_time = {}
    accum_speed = {}
    accum_eff = {}
    count_by_PN = {}

    for N, I, P, t_serial, t_pth, speed, eff in summary_rows:
        key = (P, N)
        accum_time[key] = accum_time.get(key, 0.0) + t_pth
        accum_speed[key] = accum_speed.get(key, 0.0) + speed
        accum_eff[key] = accum_eff.get(key, 0.0) + eff
        count_by_PN[key] = count_by_PN.get(key, 0) + 1

    for key, c in count_by_PN.items():
        avg_t_pth = accum_time[key] / c
        avg_speed = accum_speed[key] / c
        avg_eff = accum_eff[key] / c
        time_by_PN_Imin[key] = avg_t_pth
        speed_by_PN_Imin[key] = avg_speed
        eff_by_PN_Imin[key] = avg_eff

    # --------------------------------------------------------
    # Iso-efficiency data: average eff over I for each (P,N)
    # --------------------------------------------------------
    avg_eff_by_PN = {}
    for (P, N), eff_list in eff_vals_by_PN.items():
        if eff_list:
            avg_eff_by_PN[(P, N)] = float(np.mean(eff_list))

    # --------------------------------------------------------
    # Global scales for timing / speedup / efficiency
    # --------------------------------------------------------
    all_times = [t for t in time_by_PN_Imin.values() if t is not None]
    all_speeds = [s for s in speed_by_PN_Imin.values() if s is not None]
    all_effs = [e for e in eff_by_PN_Imin.values() if e is not None]

    t_max = max(all_times) if all_times else 1.0
    s_max = max(all_speeds) if all_speeds else 1.0
    e_max = max(all_effs) if all_effs else 1.0

    # --------------------------------------------------------
    # Plots
    # --------------------------------------------------------
    # Timing vs P by N
    plot_lines_by_P(
        os.path.join(results_dir, f"timing_vs_P_by_N_{label}.png"),
        "Parallel Time vs P (averaged over I)",
        "Time (seconds)",
        Ps,
        Ns_seen,
        time_by_PN_Imin,
        y_min=0.0,
        y_max=t_max * 1.1,
    )

    # Speedup vs P
    plot_lines_by_P(
        os.path.join(results_dir, f"speedup_vs_P_by_N_{label}.png"),
        "Speedup vs P (averaged over I)",
        "Speedup (T_serial / T_pth)",
        Ps,
        Ns_seen,
        speed_by_PN_Imin,
        y_min=0.0,
        y_max=s_max * 1.1,
    )

    # Efficiency vs P
    plot_lines_by_P(
        os.path.join(results_dir, f"efficiency_vs_P_by_N_{label}.png"),
        "Efficiency vs P (averaged over I)",
        "Efficiency (Speedup / P)",
        Ps,
        Ns_seen,
        eff_by_PN_Imin,
        y_min=0.0,
        y_max=min(1.1, e_max * 1.1),
    )

    # Iso-efficiency curves (per target E)
    iso_files = []
    for E in eff_targets:
        # CSV for this E
        iso_csv = os.path.join(results_dir, f"isoefficiency_E={E:.2f}_{label}.csv")
        iso_rows = []
        for P in Ps:
            best_N = None
            for N in Ns_seen:
                key = (P, N)
                eff_val = avg_eff_by_PN.get(key, None)
                if eff_val is not None and eff_val >= E:
                    best_N = N
                    break
            iso_rows.append([P, best_N if best_N is not None else "NaN"])
        write_csv(iso_csv, ["P", "N_min_for_E"], iso_rows)
        iso_files.append(iso_csv)

    iso_plot_path = None
    if eff_targets:
        iso_plot_path = os.path.join(results_dir, f"isoefficiency_curves_{label}.png")
        plot_iso_efficiency(
            iso_plot_path,
            "Iso-efficiency Curves",
            eff_targets,
            Ps,
            Ns_seen,
            avg_eff_by_PN,
        )

    # Global iso-efficiency surface-like plot can be approximated
    # as 2D heatmap if desired; for now we just note E-specific curves.

    # --------------------------------------------------------
    # Text report
    # --------------------------------------------------------
    num_ok = len(summary_rows)
    with open(report_txt, "w") as f:
        f.write("Stencil 2D Pthreads Benchmark Report\n")
        f.write("====================================\n\n")
        f.write(f"Total cases (N,I,P): {total_cases}\n")
        f.write(f"Successful (N,I,P):  {num_ok}\n")
        f.write(f"Results dir:         {results_dir}\n")
        f.write(f"Data CSV:            {dat_csv}\n")
        f.write(f"Summary CSV:         {summary_csv}\n")
        f.write(f"Error log:           {err_log}\n")
        f.write("\nIso-efficiency CSVs:\n")
        for path in iso_files:
            f.write(f"  {path}\n")
        if iso_plot_path:
            f.write(f"\nIso-efficiency plot: {iso_plot_path}\n")

    # Console summary similar to instructor example
    print("\nDone.")
    print(f"Dat CSV : {dat_csv}")
    print(f"Summary : {summary_csv}")
    print(f"Report  : {report_txt}")
    print("Plots   :")
    print(f"  {os.path.join(results_dir, f'timing_vs_P_by_N_{label}.png')}")
    print(f"  {os.path.join(results_dir, f'speedup_vs_P_by_N_{label}.png')}")
    print(f"  {os.path.join(results_dir, f'efficiency_vs_P_by_N_{label}.png')}")
    if iso_plot_path:
        print(f"  {iso_plot_path}")


# ============================================================
# Argument parsing and main
# ============================================================

def parse_args():
    """
    Function: parse_args
    Desc:
      Parse command-line arguments for the benchmark.

    Variables:
      None

    Returns
      argparse.Namespace - Parsed arguments.
    """
    p = argparse.ArgumentParser(
        prog="bench_stencil2d_pthreads.py",
        description="Benchmark pthreads stencil-2d over N, P, and I (no stacks).",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    p.add_argument("--make_exe", default="./make-2d",
                   help="path to make-2d")
    p.add_argument("--serial_exe", default="./stencil-2d",
                   help="path to serial stencil-2d")
    p.add_argument("--pth_exe", default="./pth-stencil-2d",
                   help="path to pth-stencil-2d")

    # N controls
    p.add_argument("--N_start", type=int, default=0,
                   help="doubling start N (if >0, use doubling)")
    p.add_argument("--N_max", type=int, default=0,
                   help="doubling max N (inclusive)")
    p.add_argument("--N1", type=int, default=256,
                   help="min N (evenly spaced)")
    p.add_argument("--N2", type=int, default=4096,
                   help="max N (evenly spaced)")
    p.add_argument("--num_Ns", type=int, default=5,
                   help="number of N points (evenly spaced)")

    # P controls
    p.add_argument("--P_start", type=int, default=1,
                   help="P range start")
    p.add_argument("--P_step", type=int, default=1,
                   help="P range step")
    p.add_argument("--P_max", type=int, default=8,
                   help="P range max (inclusive)")
    p.add_argument("--Ps", nargs="+", default=[],
                   help="explicit P list if you don't want range")

    # I controls
    p.add_argument("--I1", type=int, default=10,
                   help="iterations min")
    p.add_argument("--I2", type=int, default=50,
                   help="iterations max")
    p.add_argument("--Istep", type=int, default=20,
                   help="iterations step")
    p.add_argument("--Is", nargs="+", default=[],
                   help="explicit list of iterations")

    p.add_argument("--warmup", type=int, default=1,
                   help="warmup runs per (N,P,I) not timed")
    p.add_argument("--trials", type=int, default=5,
                   help="timed trials per (N,P,I)")
    p.add_argument("--timeout_sec", type=float, default=600.0,
                   help="per-run timeout seconds")

    # Efficiency target controls
    p.add_argument("--eff_range", type=str, default="",
                   help='e.g., "0.3 0.1" → 0.3,0.4,...')
    p.add_argument("--eff_targets", type=str, default="",
                   help='e.g., "0.3,0.5,0.7,0.9"')

    p.add_argument("--results-dir", type=str, default="perf_results",
                   help="folder for outputs")
    p.add_argument("--label", type=str, default="",
                   help="optional label suffix for filenames")

    # If no args, print usage and exit
    if len(sys.argv) == 1:
        p.print_help(sys.stderr)
        sys.exit(1)

    return p.parse_args()


def main():
    """
    Function: main
    Desc:
      Entry point. Parse args and call benchmark().

    Variables:
      None

    Returns
      None
    """
    args = parse_args()
    benchmark(args)


if __name__ == "__main__":
    main()
