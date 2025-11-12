#!/usr/bin/env python3
"""
Usage: python check_mc_slab_omp_consistency.py --serial SERIAL --parallel PARALLEL --C C --Cc CC --H H
                                               --n_start N_START --n_max N_MAX --Ps P_LIST
                                               [--seed SEED] [--trials TRIALS] [--abs_threshold THRESH]
                                               [--results-dir DIR]

    --serial SERIAL     Path to serial executable (default: ./mc_slab)
    --parallel PARALLEL Path to OpenMP executable (default: ./mc_slab_omp)
    --C C               Total interaction coefficient
    --Cc CC             Absorption coefficient
    --H H               Slab thickness
    --seed SEED         Base RNG seed used for both solvers
    --n_start N_START   Minimum particle count (doubling until n_max)
    --n_max N_MAX       Maximum particle count (inclusive)
    --Ps P_LIST         Comma-separated list of thread counts to validate (e.g., 1,2,4)
    --trials TRIALS     Repeated trials per (N, P) pair
    --abs_threshold THRESH
                        Maximum allowed absolute difference between outcome fractions (default: 0.01)
    --results-dir DIR   Directory for CSV results (default: ./data)
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Cross-check serial vs OpenMP mc_slab results across test ranges."
    )
    parser.add_argument("--serial", default="./mc_slab", help="Path to serial executable")
    parser.add_argument("--parallel", default="./mc_slab_omp", help="Path to OpenMP executable")
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
    parallel_path = Path(args.parallel).resolve()
    if not serial_path.exists():
        raise FileNotFoundError(f"Serial executable not found: {serial_path}")
    if not parallel_path.exists():
        raise FileNotFoundError(f"OpenMP executable not found: {parallel_path}")

    n_values = doubling_range(args.n_start, args.n_max)
    p_values = parse_thread_list(args.P_s)
    results_dir = Path(args.results_dir).resolve()
    ensure_dir(results_dir)

    total_tests = len(n_values) * len(p_values) * args.trials
    test_idx = 0
    print(f"Planned trials: {total_tests}")

    raw_rows: List[List[object]] = []
    summary_map: Dict[Tuple[int, int], Dict[str, int]] = { (n, p): {"tests":0,"pass":0,"fail":0} for n in n_values for p in p_values }

    for n in n_values:
        for p in p_values:
            for trial in range(args.trials):
                test_idx += 1
                seed = args.seed + trial if args.seed is not None else None
                status = f"[{test_idx}/{total_tests}] Trial {trial + 1}/{args.trials} N={n} P={p}"
                sys.stdout.write("\r" + status)
                sys.stdout.flush()

                serial_args = [
                    f"{args.C:.10g}",
                    f"{args.Cc:.10g}",
                    f"{args.H:.10g}",
                    str(n),
                ]
                parallel_args = serial_args + [str(p)]

                serial_res = run_solver(serial_path, serial_args, seed)
                parallel_res = run_solver(parallel_path, parallel_args, seed)

                total = n
                diffs = {
                    "absorbed": abs(fraction(serial_res["absorbed"], total) - fraction(parallel_res["absorbed"], total)),
                    "transmitted": abs(fraction(serial_res["transmitted"], total) - fraction(parallel_res["transmitted"], total)),
                    "reflected": abs(fraction(serial_res["reflected"], total) - fraction(parallel_res["reflected"], total)),
                }
                passed = all(diff <= args.abs_threshold for diff in diffs.values())

                summary_entry = summary_map[(n, p)]
                summary_entry["tests"] += 1
                if passed:
                    summary_entry["pass"] += 1
                else:
                    summary_entry["fail"] += 1

                raw_rows.append([
                    n,
                    p,
                    trial,
                    serial_res["absorbed"],
                    parallel_res["absorbed"],
                    diffs["absorbed"],
                    serial_res["transmitted"],
                    parallel_res["transmitted"],
                    diffs["transmitted"],
                    serial_res["reflected"],
                    parallel_res["reflected"],
                    diffs["reflected"],
                    int(passed),
                ])

    sys.stdout.write("\n")
    sys.stdout.flush()

    raw_path = results_dir / "consistency_omp_raw_runs.csv"
    summary_path = results_dir / "consistency_omp_summary.csv"

    with raw_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "N",
            "P",
            "trial",
            "serial_absorbed",
            "parallel_absorbed",
            "diff_absorbed",
            "serial_transmitted",
            "parallel_transmitted",
            "diff_transmitted",
            "serial_reflected",
            "parallel_reflected",
            "diff_reflected",
            "pass",
        ])
        writer.writerows(raw_rows)

    total_pass = sum(entry["pass"] for entry in summary_map.values())
    total_fail = sum(entry["fail"] for entry in summary_map.values())
    total_tests_recorded = sum(entry["tests"] for entry in summary_map.values())

    with summary_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["N", "P", "tests", "pass", "fail"])
        for (n, p), entry in sorted(summary_map.items()):
            writer.writerow([n, p, entry["tests"], entry["pass"], entry["fail"]])

    print("OpenMP Consistency report")
    print("=========================")
    print(f"Total tests : {total_tests_recorded}")
    print(f"Pass        : {total_pass}")
    print(f"Fail        : {total_fail}")
    print(f"Raw data    : {raw_path}")
    print(f"Summary     : {summary_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
