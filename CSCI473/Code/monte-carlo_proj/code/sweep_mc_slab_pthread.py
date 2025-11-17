#!/usr/bin/env python3
"""
Usage: python sweep_mc_slab_pthreads.py --exe EXE --C C --Cc CC --H H
                                        --n_start N_START --n_max N_MAX
                                        --P_start P_START --P_step P_STEP --P_max P_MAX
                                        [--Ps P_LIST]
                                        [--seed SEED] [--trials TRIALS] [--warmup WARMUP]
                                        [--eff_targets TARGETS] [--results-dir DIR]

    --exe EXE            Path to mc_slab_pthread executable (default: ./mc_slab_pthread)
    --C C                Total interaction coefficient
    --Cc CC              Absorption coefficient
    --H H                Slab thickness
    --seed SEED          Base RNG seed (applied via MC_SLAB_SEED)
    --n_start N_START    Smallest particle count to sweepmark
    --n_max N_MAX        Largest particle count to sweepmark (doubling each step)
    --P_start P_START    Smallest thread count to sweepmark (required without --Ps)
    --P_step P_STEP      Step between thread counts (required without --Ps)
    --P_max P_MAX        Maximum thread count to sweepmark (required without --Ps)
    --Ps P_LIST          Comma-separated thread counts (e.g., 1,2,4). Overrides range arguments
    --trials TRIALS      Timed trials per (N, P) pair (default: 3)
    --warmup WARMUP      Untimed warmup runs per (N, P) pair (default: 1)
    --eff_targets LIST   Comma-separated efficiency targets for iso-efficiency curves (default: 0.6,0.75,0.9)
    --results-dir DIR    Directory for CSV/plot artifacts (default: ./data)

Outputs:
    - sweep_pthreads_raw_runs.csv        Per-trial timings and tallies
    - sweep_pthreads_summary.csv         Aggregate stats per (N, P)
    - sweep_pthreads_runtime.png         Runtime vs. thread count
    - sweep_pthreads_speedup.png         Speedup vs. thread count
    - sweep_pthreads_efficiency.png      Efficiency vs. thread count
    - sweep_pthreads_isoefficiency.png   Iso-efficiency curves per target
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import statistics
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt

RAW_FILENAME = "sweep_pthreads_raw_runs.csv"
SUMMARY_FILENAME = "sweep_pthreads_summary.csv"
RUNTIME_PLOT_FILENAME = "sweep_pthreads_runtime.png"
SPEEDUP_PLOT_FILENAME = "sweep_pthreads_speedup.png"
EFFICIENCY_PLOT_FILENAME = "sweep_pthreads_efficiency.png"
ISOEFF_PLOT_FILENAME = "sweep_pthreads_isoefficiency.png"


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="sweepmark the pthread slab solver across particles and thread counts."
    )
    parser.add_argument("--exe", default="./mc_slab_pthread", help="Path to mc_slab_pthread executable")
    parser.add_argument("--C", type=float, required=True, help="Total interaction coefficient")
    parser.add_argument("--Cc", type=float, required=True, help="Absorption coefficient")
    parser.add_argument("--H", type=float, required=True, help="Slab thickness")
    parser.add_argument("--seed", type=int, default=None, help="Base RNG seed")
    parser.add_argument("--n_start", type=int, required=True, help="Smallest particle count to sweepmark")
    parser.add_argument("--n_max", type=int, required=True, help="Largest particle count (inclusive)")
    parser.add_argument("--P_start", type=int, help="Smallest thread count to sweepmark")
    parser.add_argument("--P_step", type=int, help="Step between thread counts")
    parser.add_argument("--P_max", type=int, help="Maximum thread count to sweepmark")
    parser.add_argument(
        "--Ps",
        dest="P_list",
        default=None,
        help="Comma-separated list of explicit thread counts (overrides --P_start/--P_step/--P_max)",
    )
    parser.add_argument("--P_list", dest="P_list", help=argparse.SUPPRESS)
    parser.add_argument("--trials", type=int, default=3, help="Timed trials per configuration")
    parser.add_argument("--warmup", type=int, default=1, help="Warmup runs per configuration")
    parser.add_argument(
        "--eff_targets",
        default="0.6,0.75,0.9",
        help="Comma-separated efficiency targets for iso-efficiency (e.g., 0.6,0.8,0.9)",
    )
    parser.add_argument("--results-dir", default="./data", dest="results_dir", help="Directory for CSV and plot outputs")
    parser.add_argument(
        "--results_dir",
        dest="results_dir",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args(argv)
    if args.P_list is None:
        missing = [name for name in ("P_start", "P_step", "P_max") if getattr(args, name) is None]
        if missing:
            parser.error("Provide either --Ps or all of --P_start, --P_step, and --P_max.")
    return args


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def generate_n_values(start: int, max_value: int) -> List[int]:
    if start <= 0 or max_value < start:
        raise ValueError("--n_start must be positive and <= --n_max")
    values: List[int] = []
    current = start
    while current <= max_value:
        values.append(current)
        current *= 2
    if values[-1] != max_value:
        values.append(max_value)
    return sorted(set(values))


def generate_p_values(start: int, step: int, max_value: int) -> List[int]:
    if start <= 0 or max_value < start:
        raise ValueError("--P_start must be positive and <= --P_max")
    values: List[int] = []
    current = start
    step = max(1, step)
    while current <= max_value:
        values.append(current)
        current += step
    if values[-1] != max_value:
        values.append(max_value)
    return sorted(set(values))


def parse_thread_list(arg: str) -> List[int]:
    try:
        values = sorted({int(token) for token in arg.split(",") if token.strip()})
    except ValueError as exc:
        raise ValueError(f"Invalid thread count in --Ps: {exc}") from exc
    if not values:
        raise ValueError("Provide at least one thread count via --Ps")
    return values


def run_solver(exe: Path,
               C: float,
               Cc: float,
               H: float,
               n: int,
               threads: int,
               seed: Optional[int]) -> Tuple[float, Dict[str, float]]:
    cmd = [
        str(exe),
        f"{C:.10g}",
        f"{Cc:.10g}",
        f"{H:.10g}",
        str(n),
        str(threads),
    ]
    env = os.environ.copy()
    if seed is not None:
        env["MC_SLAB_SEED"] = str(seed)

    start = time.perf_counter()
    completed = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    elapsed = time.perf_counter() - start
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        print(completed.stdout, file=sys.stderr)
        raise RuntimeError("mc_slab_pthread output was not valid JSON") from exc
    return elapsed, payload


def summarize_trials(times: List[float]) -> Dict[str, float]:
    if not times:
        return {"avg": math.nan, "stdev": math.nan, "median": math.nan}
    return {
        "avg": sum(times) / len(times),
        "stdev": statistics.stdev(times) if len(times) > 1 else 0.0,
        "median": statistics.median(times),
    }


def plot_lines(x_values: List[int],
               series: Dict[int, List[float]],
               ylabel: str,
               title: str,
               output_path: Path,
               yscale: Optional[str] = None) -> None:
    if not series:
        return
    plt.figure(figsize=(8, 5), dpi=150)
    for label, y_values in sorted(series.items()):
        if not y_values:
            continue
        plt.plot(x_values, y_values, marker="o", label=f"N={label}")
    plt.xlabel("Threads (P)")
    plt.ylabel(ylabel)
    if yscale:
        plt.yscale(yscale)
    plt.title(title)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_isoeff(p_values: List[int],
                isoeff_table: Dict[float, List[Optional[int]]],
                output_path: Path) -> None:
    if not isoeff_table:
        return
    plt.figure(figsize=(8, 5), dpi=150)
    for target, n_values in sorted(isoeff_table.items()):
        filtered_p = []
        filtered_n = []
        for p, n in zip(p_values, n_values):
            if n is None:
                continue
            filtered_p.append(p)
            filtered_n.append(n)
        if filtered_p:
            plt.plot(filtered_p, filtered_n, marker="s", label=f"Eff ≥ {target:.2f}")
    plt.xlabel("Threads (P)")
    plt.ylabel("Minimum N achieving target efficiency")
    plt.title("Iso-efficiency Curves")
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    exe_path = Path(args.exe).resolve()
    if not exe_path.exists():
        raise FileNotFoundError(f"Executable not found: {exe_path}")

    results_dir = Path(args.results_dir).resolve()
    ensure_dir(results_dir)

    n_values = generate_n_values(args.n_start, args.n_max)
    try:
        if args.P_list:
            p_values = parse_thread_list(args.P_list)
        else:
            p_values = generate_p_values(args.P_start, args.P_step, args.P_max)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    eff_targets = [float(x.strip()) for x in args.eff_targets.split(",") if x.strip()]

    raw_rows: List[List[object]] = []
    summary: Dict[Tuple[int, int], Dict[str, float]] = {}

    total_configs = len(n_values) * len(p_values)
    config_idx = 0

    for n in n_values:
        reference_time = None
        for p in p_values:
            config_idx += 1
            print(f"[{config_idx}/{total_configs}] sweepmarking N={n}, P={p}")

            for _ in range(args.warmup):
                seed = args.seed
                try:
                    run_solver(exe_path, args.C, args.Cc, args.H, n, p, seed)
                except subprocess.CalledProcessError as exc:
                    print(exc.stderr, file=sys.stderr)
                    raise

            times: List[float] = []
            for trial in range(args.trials):
                seed = args.seed + trial if args.seed is not None else None
                elapsed, payload = run_solver(exe_path, args.C, args.Cc, args.H, n, p, seed)
                times.append(elapsed)
                raw_rows.append([
                    n,
                    p,
                    trial,
                    elapsed,
                    payload.get("absorbed"),
                    payload.get("transmitted"),
                    payload.get("reflected"),
                ])

            stats = summarize_trials(times)
            if reference_time is None:
                reference_time = stats["avg"]

            speedup = reference_time / stats["avg"] if stats["avg"] > 0 else math.nan
            efficiency = speedup / p if p > 0 else math.nan

            summary[(n, p)] = {
                "avg_time": stats["avg"],
                "stdev": stats["stdev"],
                "median": stats["median"],
                "speedup": speedup,
                "efficiency": efficiency,
            }

    raw_path = results_dir / RAW_FILENAME
    with raw_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["N", "P", "trial", "elapsed_seconds", "absorbed", "transmitted", "reflected"])
        writer.writerows(raw_rows)

    summary_path = results_dir / SUMMARY_FILENAME
    with summary_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["N", "P", "avg_time", "median_time", "stdev_time", "speedup", "efficiency"])
        for (n, p), stats in sorted(summary.items()):
            writer.writerow([
                n,
                p,
                f"{stats['avg_time']:.6f}",
                f"{stats['median']:.6f}",
                f"{stats['stdev']:.6f}",
                f"{stats['speedup']:.6f}",
                f"{stats['efficiency']:.6f}",
            ])

    runtime_series: Dict[int, List[float]] = {}
    speedup_series: Dict[int, List[float]] = {}
    efficiency_series: Dict[int, List[float]] = {}

    for n in n_values:
        runtime_series[n] = []
        speedup_series[n] = []
        efficiency_series[n] = []
        for p in p_values:
            stats = summary.get((n, p))
            if not stats:
                runtime_series[n].append(math.nan)
                speedup_series[n].append(math.nan)
                efficiency_series[n].append(math.nan)
                continue
            runtime_series[n].append(stats["avg_time"])
            speedup_series[n].append(stats["speedup"])
            efficiency_series[n].append(stats["efficiency"])

    plot_lines(p_values, runtime_series, "Runtime (s)", "Runtime vs Threads", results_dir / RUNTIME_PLOT_FILENAME)
    plot_lines(p_values, speedup_series, "Speedup", "Speedup vs Threads", results_dir / SPEEDUP_PLOT_FILENAME)
    plot_lines(p_values, efficiency_series, "Efficiency", "Efficiency vs Threads", results_dir / EFFICIENCY_PLOT_FILENAME, yscale=None)

    isoeff_table: Dict[float, List[Optional[int]]] = {}
    for target in eff_targets:
        isoeff_table[target] = []
        for p in p_values:
            qualifying = [n for n in n_values if summary.get((n, p), {}).get("efficiency", 0.0) >= target]
            isoeff_table[target].append(min(qualifying) if qualifying else None)
    plot_isoeff(p_values, isoeff_table, results_dir / ISOEFF_PLOT_FILENAME)

    print(f"Raw run data: {raw_path}")
    print(f"Summary data: {summary_path}")
    print(f"Plots saved to {results_dir}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
