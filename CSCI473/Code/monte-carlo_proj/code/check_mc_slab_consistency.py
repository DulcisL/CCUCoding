#!/usr/bin/env python3
"""
Usage: python check_mc_slab_consistency.py --serial SERIAL --pthread PTHREAD --omp OMP
                                           --C C --Cc CC --H H --n_start N_START --n_max N_MAX --Ps P_LIST
                                           [--seed SEED] [--trials TRIALS] [--abs_threshold THRESH]
                                           [--results-dir DIR]

    --serial SERIAL     Path to serial executable (default: ./mc_slab)
    --pthread PTHREAD   Path to pthread executable (default: ./mc_slab_pthread)
    --omp OMP           Path to OpenMP executable (default: ./mc_slab_omp)
    --C C               Total interaction coefficient
    --Cc CC             Absorption coefficient
    --H H               Slab thickness
    --seed SEED         Base RNG seed used for all solvers
    --n_start N_START   Minimum particle count (doubling until n_max)
    --n_max N_MAX       Maximum particle count (inclusive)
    --Ps P_LIST         Comma-separated list of thread counts to validate (e.g., 1,2,4)
    --trials TRIALS     Repeated trials per (N, P) pair
    --abs_threshold THRESH
                        Maximum allowed absolute difference between outcome fractions (default: 0.01)
    --results-dir DIR   Directory for CSV results (default: ./data)

Console output:
    - Prints trial progress: "[i/total] Trial ... N=... P=..."
    - Final summary with pass/fail counts and CSV paths.
Artifacts:
    - consistency_raw_runs.csv   Per-trial comparisons across all solvers
    - consistency_summary.csv    Aggregated pass/fail statistics
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

METRICS: Tuple[str, ...] = ("absorbed", "transmitted", "reflected")
PAIRINGS: Tuple[Tuple[str, str], ...] = (
    ("serial", "pthread"),
    ("serial", "omp"),
    ("pthread", "omp"),
)


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-check serial vs pthread vs OpenMP mc_slab results across test ranges."
    )
    parser.add_argument("--serial", default="./mc_slab", help="Path to serial executable")
    parser.add_argument("--pthread", default="./mc_slab_pthread", help="Path to pthread executable")
    parser.add_argument("--omp", default="./mc_slab_omp", help="Path to OpenMP executable")
    parser.add_argument("--C", type=float, required=True, help="Total interaction coefficient")
    parser.add_argument("--Cc", type=float, required=True, help="Absorption coefficient")
    parser.add_argument("--H", type=float, required=True, help="Slab thickness")
    parser.add_argument("--seed", type=int, default=None, help="Base RNG seed")
    parser.add_argument("--n_start", type=int, required=True, help="Minimum particle count to test")
    parser.add_argument("--n_max", type=int, required=True, help="Maximum particle count to test")
    parser.add_argument("--Ps", dest="P_s", required=True, help="Comma-separated list of thread counts")
    parser.add_argument("--P_s", dest="P_s", help=argparse.SUPPRESS)
    parser.add_argument("--trials", type=int, default=5, help="Trials per (N, P) combination")
    parser.add_argument("--abs_threshold", type=float, default=0.01, help="Acceptable absolute difference per fraction")
    parser.add_argument("--results-dir", dest="results_dir", default="./data", help="Directory for CSV outputs")
    parser.add_argument("--results_dir", dest="results_dir", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def doubling_range(start: int, stop: int) -> List[int]:
    if start <= 0 or stop < start:
        raise ValueError("--n_start must be positive and <= --n_max")
    values: List[int] = []
    current = start
    while current <= stop:
        values.append(current)
        current *= 2
    if values[-1] != stop:
        values.append(stop)
    return sorted(set(values))


def parse_thread_list(arg: str) -> List[int]:
    threads = sorted({int(token) for token in arg.split(",") if token.strip()})
    if not threads:
        raise ValueError("Provide at least one thread count via --Ps")
    return threads


def run_solver(exe: Path, args: List[str], seed: Optional[int]) -> Dict[str, float]:
    env = os.environ.copy()
    if seed is not None:
        env["MC_SLAB_SEED"] = str(seed)
    completed = subprocess.run(
        [str(exe)] + args,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        print(completed.stdout, file=sys.stderr)
        raise RuntimeError(f"{exe} did not emit valid JSON") from exc


def fraction(value: float, total: float) -> float:
    if total <= 0:
        return math.nan
    return value / total


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)

    serial_path = Path(args.serial).resolve()
    pthread_path = Path(args.pthread).resolve()
    omp_path = Path(args.omp).resolve()
    if not serial_path.exists():
        raise FileNotFoundError(f"Serial executable not found: {serial_path}")
    if not pthread_path.exists():
        raise FileNotFoundError(f"Pthread executable not found: {pthread_path}")
    if not omp_path.exists():
        raise FileNotFoundError(f"OpenMP executable not found: {omp_path}")

    n_values = doubling_range(args.n_start, args.n_max)
    p_values = parse_thread_list(args.P_s)
    ensure_dir(Path(args.results_dir))

    total_tests = len(n_values) * len(p_values) * args.trials
    test_idx = 0

    print(f"Planned trials: {total_tests}")

    raw_rows: List[List[object]] = []
    summary_map: Dict[Tuple[int, int], Dict[str, int]] = {}

    for n in n_values:
        for p in p_values:
            summary_map[(n, p)] = {"tests": 0, "pass": 0, "fail": 0}
            for trial in range(args.trials):
                test_idx += 1
                seed = args.seed + trial if args.seed is not None else None
                status = f"[{test_idx}/{total_tests}] Trial {trial + 1}/{args.trials} N={n} P={p}"
                sys.stdout.write("\r" + status)
                sys.stdout.flush()

                base_args = [
                    f"{args.C:.10g}",
                    f"{args.Cc:.10g}",
                    f"{args.H:.10g}",
                    str(n),
                ]
                solver_invocations = {
                    "serial": (serial_path, base_args),
                    "pthread": (pthread_path, base_args + [str(p)]),
                    "omp": (omp_path, base_args + [str(p)]),
                }

                results: Dict[str, Dict[str, float]] = {}
                for label, (exe_path, cli_args) in solver_invocations.items():
                    results[label] = run_solver(exe_path, list(cli_args), seed)

                total = n
                diff_map: Dict[Tuple[str, str, str], float] = {}
                for left, right in PAIRINGS:
                    for metric in METRICS:
                        diff = abs(fraction(results[left][metric], total) - fraction(results[right][metric], total))
                        diff_map[(left, right, metric)] = diff

                passed = all(diff <= args.abs_threshold for diff in diff_map.values())

                summary_entry = summary_map[(n, p)]
                summary_entry["tests"] += 1
                if passed:
                    summary_entry["pass"] += 1
                else:
                    summary_entry["fail"] += 1

                row: List[object] = [n, p, trial]
                for metric in METRICS:
                    row.extend([
                        results["serial"][metric],
                        results["pthread"][metric],
                        results["omp"][metric],
                    ])
                for metric in METRICS:
                    for left, right in PAIRINGS:
                        row.append(diff_map[(left, right, metric)])
                row.append(int(passed))
                raw_rows.append(row)

    sys.stdout.write("\n")
    sys.stdout.flush()

    results_dir = Path(args.results_dir).resolve()
    raw_path = results_dir / "consistency_raw_runs.csv"
    summary_path = results_dir / "consistency_summary.csv"

    with raw_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        header: List[str] = ["N", "P", "trial"]
        for metric in METRICS:
            header.extend([
                f"serial_{metric}",
                f"pthread_{metric}",
                f"omp_{metric}",
            ])
        for metric in METRICS:
            for left, right in PAIRINGS:
                header.append(f"diff_{left}_{right}_{metric}")
        header.append("pass")
        writer.writerow(header)
        writer.writerows(raw_rows)

    total_pass = sum(entry["pass"] for entry in summary_map.values())
    total_fail = sum(entry["fail"] for entry in summary_map.values())
    total_tests_recorded = sum(entry["tests"] for entry in summary_map.values())

    with summary_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["N", "P", "tests", "pass", "fail"])
        for (n, p), entry in sorted(summary_map.items()):
            writer.writerow([n, p, entry["tests"], entry["pass"], entry["fail"]])

    print("Consistency report")
    print("==================")
    print(f"Total tests : {total_tests_recorded}")
    print(f"Pass        : {total_pass}")
    print(f"Fail        : {total_fail}")
    print(f"Raw data    : {raw_path}")
    print(f"Summary     : {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
