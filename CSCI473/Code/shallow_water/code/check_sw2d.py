#!/usr/bin/env python3
"""
Run sw2d, sw2d_pthread, and sw2d_omp across a grid of problem sizes and verify
that the generated movie data matches within a tolerance.

Example:
    python check_sw2d.py --rows 64,128 --cols 64 --steps 200 \
        --threads 1,2,4 --trials 2 --results-dir data/checks
"""

from __future__ import annotations

import argparse
import csv
import itertools
import math
import os
import shlex
import struct
import subprocess
import sys
import time
from array import array
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

PAIRINGS: Tuple[Tuple[str, str], ...] = (
    ("serial", "pthread"),
    ("serial", "omp"),
    ("pthread", "omp"),
)
FIELDS: Tuple[str, ...] = ("h", "u", "v")


def parse_range(spec: str, kind: str) -> List[int]:
    values: List[int] = []
    if not spec:
        raise ValueError(f"{kind} specification cannot be empty")
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            parts = chunk.split(":")
            if len(parts) not in {2, 3}:
                raise ValueError(f"Invalid {kind} range '{chunk}' (start:end[:step])")
            start = int(parts[0])
            end = int(parts[1])
            step = int(parts[2]) if len(parts) == 3 else (1 if end >= start else -1)
            if step == 0:
                raise ValueError(f"{kind} range '{chunk}' has zero step")
            current = start
            if step > 0:
                while current <= end:
                    values.append(current)
                    current += step
            else:
                while current >= end:
                    values.append(current)
                    current += step
        else:
            values.append(int(chunk))
    if not values:
        raise ValueError(f"No valid {kind} values parsed from '{spec}'")
    return sorted(set(values))


def build_cli() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Cross-check sw2d implementations (serial, pthread, OpenMP)."
    )
    ap.add_argument("--serial", default=str(Path("./sw2d").resolve()), help="Path to sw2d executable.")
    ap.add_argument("--pthread", default=str(Path("./sw2d_pthread").resolve()), help="Path to sw2d_pthread executable.")
    ap.add_argument("--omp", default=str(Path("./sw2d_omp").resolve()), help="Path to sw2d_omp executable.")
    ap.add_argument("--rows", default="200", help="Row counts (comma list or start:end:step).")
    ap.add_argument("--cols", default="200", help="Column counts (comma list or start:end:step).")
    ap.add_argument("--steps", default="2000", help="Step counts (comma list or start:end:step).")
    ap.add_argument("--Ps", dest="threads", default="1", help="Thread counts (processes) for pthread/omp solvers.")
    ap.add_argument("--threads", dest="threads", help=argparse.SUPPRESS)
    ap.add_argument("--dx", type=float, default=1.0, help="Cell size in x.")
    ap.add_argument("--dy", type=float, default=1.0, help="Cell size in y.")
    ap.add_argument("--height", type=float, default=0.5, help="Initial displaced column height.")
    ap.add_argument("--g", type=float, default=9.81, help="Gravity constant.")
    ap.add_argument("--H0", type=float, default=1.0, help="Mean depth.")
    ap.add_argument("--cfl", type=float, default=0.4, help="CFL number when dt not provided.")
    ap.add_argument("--dt", type=float, default=0.0, help="Explicit dt (<=0 => auto).")
    ap.add_argument("--save-interval", type=int, default=0, help="Save interval (0 => set to steps for each test).")
    ap.add_argument("--stats-interval", type=int, default=0, help="Stats interval passed to solvers.")
    ap.add_argument("--trials", type=int, default=1, help="Repeat count per configuration.")
    ap.add_argument("--abs-threshold", type=float, default=5e-3, help="Max allowed absolute difference per field.")
    ap.add_argument("--abs_threshold", dest="abs_threshold", type=float, help=argparse.SUPPRESS)
    ap.add_argument("--results-dir", default="sw2d_consistency", help="Output directory for CSVs/movies.")
    ap.add_argument("--keep-movies", action="store_true", help="Preserve solver movie outputs.")
    ap.add_argument("--extra", default="", help="Additional solver flags (applied to all solvers).")
    ap.add_argument("--keep-progress", action="store_true", help="Keep solver progress bars.")
    ap.add_argument(
        "--allow-unstable-dt",
        action="store_true",
        help="Pass the requested dt through even if it violates the CFL stability estimate.",
    )
    ap.add_argument("--verbose", action="store_true", help="Show detailed per-test logging.")
    return ap


def ensure_executable(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Executable not found: {path}")
    if not os.access(path, os.X_OK):
        raise PermissionError(f"Executable not runnable: {path}")


def load_last_frame(movie_path: Path) -> Dict[str, object]:
    with movie_path.open("rb") as f:
        header_fmt = "<4sIIiiii5d"
        header_size = struct.calcsize(header_fmt)
        data = f.read(header_size)
        if len(data) != header_size:
            raise RuntimeError(f"{movie_path} truncated header")
        magic, version, flags, rows, cols, nframes, save_int, dxv, dyv, dtv, gv, H0v = struct.unpack(header_fmt, data)
        if magic != b"SW2D":
            raise RuntimeError(f"{movie_path} missing SW2D magic")
        if rows <= 0 or cols <= 0 or nframes <= 0:
            raise RuntimeError(f"{movie_path} has invalid dimensions/frames")
        frame_cells = rows * cols
        frame_bytes = frame_cells * 8 * 3
        if frame_bytes <= 0:
            raise RuntimeError(f"{movie_path} invalid frame size")
        f.seek(header_size + frame_bytes * (nframes - 1))
        h = array("d")
        u = array("d")
        v = array("d")
        h.fromfile(f, frame_cells)
        u.fromfile(f, frame_cells)
        v.fromfile(f, frame_cells)
    return {
        "rows": rows,
        "cols": cols,
        "nframes": nframes,
        "save_interval": save_int,
        "dx": dxv,
        "dy": dyv,
        "dt": dtv,
        "g": gv,
        "H0": H0v,
        "h": h,
        "u": u,
        "v": v,
    }


def max_abs_diff(left: array, right: array) -> float:
    if len(left) != len(right):
        raise ValueError("Mismatched array lengths")
    return max((abs(a - b) for a, b in zip(left, right)), default=0.0)


def format_duration(seconds: float) -> str:
    if not math.isfinite(seconds) or seconds < 0:
        return "--:--"
    total = int(round(seconds))
    mins, secs = divmod(total, 60)
    hours, mins = divmod(mins, 60)
    if hours > 99:
        return ">99h"
    if hours > 0:
        return f"{hours:02d}:{mins:02d}:{secs:02d}"
    return f"{mins:02d}:{secs:02d}"


def print_progress(current: int, total: int, start_time: float) -> None:
    if total <= 0:
        return
    frac = min(max(current / total, 0.0), 1.0)
    bar_len = 40
    filled = int(bar_len * frac)
    bar = "=" * filled + " " * (bar_len - filled)
    eta = "--:--"
    elapsed = time.monotonic() - start_time
    if current > 0:
        remaining = elapsed * (total - current) / current
        eta = format_duration(max(0.0, remaining))
    else:
        eta = format_duration(elapsed)
    msg = f"\r[{bar}] {frac * 100:6.2f}% {current}/{total} ETA {eta}"
    sys.stdout.write(msg)
    sys.stdout.flush()
    if current >= total:
        sys.stdout.write("\n")


def estimate_stable_dt(args: argparse.Namespace) -> Optional[float]:
    if args.cfl <= 0 or args.dx <= 0 or args.dy <= 0:
        return None
    wavespeed = math.sqrt(args.g * args.H0)
    if not math.isfinite(wavespeed) or wavespeed <= 0:
        return None
    dmin = min(args.dx, args.dy)
    return args.cfl * dmin / wavespeed


def run_solver(
    exe: Path,
    rows: int,
    cols: int,
    steps: int,
    *,
    threads: Optional[int],
    args: argparse.Namespace,
    movie_path: Path,
) -> Path:
    save_interval = args.save_interval if args.save_interval > 0 else steps
    if save_interval <= 0:
        raise ValueError("save_interval must be positive (either via --save-interval or steps > 0)")
    cmd: List[str] = [
        str(exe),
        "--rows",
        str(rows),
        "--cols",
        str(cols),
        "--steps",
        str(steps),
        "--dx",
        f"{args.dx}",
        "--dy",
        f"{args.dy}",
        "--height",
        f"{args.height}",
        "--g",
        f"{args.g}",
        "--H0",
        f"{args.H0}",
        "--cfl",
        f"{args.cfl}",
        "--save-interval",
        str(save_interval),
        "--stats-interval",
        str(args.stats_interval),
        "--out",
        str(movie_path),
    ]
    if args.dt > 0.0:
        cmd.extend(["--dt", f"{args.dt}"])
    if not args.keep_progress:
        cmd.append("--no-progress")
    if threads is not None:
        cmd.extend(["--threads", str(threads)])
    extra_args = shlex.split(args.extra)
    cmd.extend(extra_args)

    if args.verbose:
        print(f"    running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        sys.stderr.write(result.stdout)
        sys.stderr.write(result.stderr)
        raise RuntimeError(f"{exe} failed with exit code {result.returncode}")
    return movie_path


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_cli()
    args = parser.parse_args(argv)

    serial_path = Path(args.serial).resolve()
    pthread_path = Path(args.pthread).resolve()
    omp_path = Path(args.omp).resolve()
    ensure_executable(serial_path)
    ensure_executable(pthread_path)
    ensure_executable(omp_path)

    requested_dt = args.dt
    stable_dt = estimate_stable_dt(args)
    if requested_dt > 0 and stable_dt is not None and requested_dt > stable_dt:
        if args.allow_unstable_dt:
            msg = (
                f"[warning] requested dt={requested_dt:g} exceeds estimated stable dt={stable_dt:g} "
                "and may lead to invalid movie data."
            )
            if args.verbose:
                print(msg)
        else:
            msg = (
                f"[info] requested dt={requested_dt:g} exceeds estimated stable dt={stable_dt:g}; "
                "clamping to preserve accuracy (use --allow-unstable-dt to skip this)."
            )
            if args.verbose:
                print(msg)
            args.dt = stable_dt

    rows_values = parse_range(args.rows, "rows")
    cols_values = parse_range(args.cols, "cols")
    steps_values = parse_range(args.steps, "steps")
    thread_values = parse_range(args.threads, "threads")

    combos = list(itertools.product(rows_values, cols_values, steps_values))
    total_tests = len(combos) * len(thread_values) * args.trials
    if total_tests == 0:
        print("No test combinations were specified.")
        return 0

    results_dir = Path(args.results_dir).resolve()
    movie_dir = results_dir / "movies"
    results_dir.mkdir(parents=True, exist_ok=True)
    movie_dir.mkdir(parents=True, exist_ok=True)

    raw_rows: List[List[object]] = []
    summary_map: Dict[Tuple[int, int, int, int], Dict[str, int]] = {}
    fail_details: List[str] = []

    test_index = 0
    start_time = time.monotonic()
    print_progress(0, total_tests, start_time)
    for rows, cols, steps in combos:
        for trial in range(1, args.trials + 1):
            base_tag = f"r{rows}_c{cols}_s{steps}_trial{trial}"
            if args.verbose:
                print(f"[problem {base_tag}]")
            serial_movie = movie_dir / f"serial_{base_tag}.bin"
            if serial_movie.exists():
                serial_movie.unlink()
            run_solver(serial_path, rows, cols, steps, threads=None, args=args, movie_path=serial_movie)
            serial_data = load_last_frame(serial_movie)
            if not args.keep_movies and serial_movie.exists():
                serial_movie.unlink()

            for thread in thread_values:
                test_index += 1
                tag = f"{base_tag}_t{thread}"
                if args.verbose:
                    print(f"  [{test_index}/{total_tests}] threads={thread}")
                summary_entry = summary_map.setdefault((rows, cols, steps, thread), {"tests": 0, "pass": 0, "fail": 0})
                summary_entry["tests"] += 1

                movies: Dict[str, Path] = {}
                data_map: Dict[str, Dict[str, object]] = {"serial": serial_data}

                for label, exe_path in [("pthread", pthread_path), ("omp", omp_path)]:
                    movie_path = movie_dir / f"{label}_{tag}.bin"
                    if movie_path.exists():
                        movie_path.unlink()
                    run_solver(
                        exe_path,
                        rows,
                        cols,
                        steps,
                        threads=thread,
                        args=args,
                        movie_path=movie_path,
                    )
                    data_map[label] = load_last_frame(movie_path)
                    movies[label] = movie_path
                    if not args.keep_movies and movie_path.exists():
                        movie_path.unlink()

                diffs: Dict[Tuple[str, str, str], float] = {}
                for left, right in PAIRINGS:
                    for field in FIELDS:
                        diff = max_abs_diff(data_map[left][field], data_map[right][field])  # type: ignore[arg-type]
                        diffs[(left, right, field)] = diff

                passed = all(diff <= args.abs_threshold for diff in diffs.values())
                if passed:
                    summary_entry["pass"] += 1
                else:
                    summary_entry["fail"] += 1
                    for (left, right, field), diff in diffs.items():
                        if diff > args.abs_threshold:
                            fail_details.append(
                                f"{tag}: diff_{left}_{right}_{field}={diff:.6g} (threshold {args.abs_threshold:g})"
                            )

                row: List[object] = [rows, cols, steps, thread, trial]
                for left, right in PAIRINGS:
                    for field in FIELDS:
                        row.append(diffs[(left, right, field)])
                row.append(int(passed))
                raw_rows.append(row)
                print_progress(test_index, total_tests, start_time)

    raw_csv = results_dir / "sw2d_consistency_raw.csv"
    summary_csv = results_dir / "sw2d_consistency_summary.csv"

    with raw_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        header = ["rows", "cols", "steps", "threads", "trial"]
        for left, right in PAIRINGS:
            for field in FIELDS:
                header.append(f"diff_{left}_{right}_{field}")
        header.append("pass")
        writer.writerow(header)
        writer.writerows(raw_rows)

    with summary_csv.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["rows", "cols", "steps", "threads", "tests", "pass", "fail"])
        for (rows, cols, steps, thread), entry in sorted(summary_map.items()):
            writer.writerow([rows, cols, steps, thread, entry["tests"], entry["pass"], entry["fail"]])

    total_pass = sum(entry["pass"] for entry in summary_map.values())
    total_fail = sum(entry["fail"] for entry in summary_map.values())
    total_elapsed = time.monotonic() - start_time
    print("\nConsistency summary")
    print("===================")
    print(f"Total tests : {total_tests}")
    print(f"Passed      : {total_pass}")
    print(f"Failed      : {total_fail}")
    print(f"Elapsed     : {format_duration(total_elapsed)}")
    print(f"Raw data    : {raw_csv}")
    print(f"Summary     : {summary_csv}")
    if args.keep_movies:
        print(f"Movies kept in: {movie_dir}")
    if fail_details:
        print("\nDifferences above threshold")
        print("===========================")
        for detail in fail_details:
            print(detail)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
