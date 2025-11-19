#!/usr/bin/env python3
"""
Parameter sweep runner for sw2d that uses the shared timer.h helper to gather timings.

Features
--------
* Builds a tiny shared object that wraps GET_TIME from timer.h so we can reuse the same
  timing primitive outside of the C code.
* Sweeps across user-specified rows/cols/steps combinations and (optionally) multiple repetitions.
* For each run it records:
    - read_time: time spent reading an init/prior file (if provided),
    - compute_time: wall time for the sw2d executable itself,
    - write_time: time to move the generated movie to a permanent location.
* Summarizes runs into a CSV for later plotting/analysis.
"""

from __future__ import annotations

import argparse
import csv
import ctypes
import itertools
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable, List, Sequence, Tuple


def compile_timer_helper(script_dir: Path) -> ctypes.CFUNCTYPE:
    """Compile (or reuse) a shared helper that exposes GET_TIME via timer.h."""
    header = script_dir / "timer.h"
    if not header.exists():
        raise FileNotFoundError(f"timer.h not found next to sweep script: {header}")
    so_path = script_dir / "_timer_helper.so"
    needs_build = not so_path.exists() or (so_path.stat().st_mtime < header.stat().st_mtime)
    if needs_build:
        code = """#include <stddef.h>
#include "timer.h"
double sw2d_now(void) {
    double ts;
    GET_TIME(ts);
    return ts;
}
"""
        cmd = ["cc", "-std=c99", "-O2", "-shared", "-fPIC", "-x", "c", "-", "-o", str(so_path)]
        subprocess.run(cmd, input=code.encode("utf-8"), check=True, cwd=str(script_dir))
    lib = ctypes.CDLL(str(so_path))
    lib.sw2d_now.restype = ctypes.c_double
    return lib.sw2d_now


def parse_range(spec: str, kind: str) -> List[int]:
    """
    Parse a comma-separated list of ints and/or colon-based ranges (start:end[:step]).
    Examples:
        "64,128,256"
        "64:256:64"
        "100:300:100,512"
    """
    values: List[int] = []
    if not spec:
        raise ValueError(f"{kind} specification must not be empty")
    for chunk in spec.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if ":" in chunk:
            parts = chunk.split(":")
            if len(parts) not in {2, 3}:
                raise ValueError(f"Invalid {kind} range '{chunk}' (expected start:end[:step])")
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
        raise ValueError(f"No usable {kind} values parsed from '{spec}'")
    return values


def build_cli() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(
        description="Run sw2d across a parameter sweep and capture read/compute/write timings.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--exe", default=str(Path(__file__).with_name("sw2d")), help="Path to sw2d executable.")
    ap.add_argument("--rows", default="200", help="Row counts (comma list or start:end:step).")
    ap.add_argument("--cols", default="200", help="Column counts (comma list or start:end:step).")
    ap.add_argument("--steps", default="2000", help="Time steps (comma list or start:end:step).")
    ap.add_argument("--dx", type=float, default=1.0, help="Cell size in x.")
    ap.add_argument("--dy", type=float, default=1.0, help="Cell size in y.")
    ap.add_argument("--height", type=float, default=0.5, help="Initial column height.")
    ap.add_argument("--save-interval", type=int, default=50, help="Frames between saves (must be >0).")
    ap.add_argument("--repeat", type=int, default=1, help="How many times to repeat each configuration.")
    ap.add_argument("--init", type=str, help="Optional init/prior file to feed to sw2d.")
    ap.add_argument("--out-dir", default="sw2d_sweep_results", help="Directory for movies and CSV.")
    ap.add_argument("--csv", default="sw2d_sweep_summary.csv", help="CSV filename (inside out-dir if relative).")
    ap.add_argument(
        "--extra",
        default="",
        help="Additional sw2d flags appended verbatim (example: \"--g 9.81 --H0 1.0\").",
    )
    ap.add_argument("--keep-progress", action="store_true", help="Show sw2d progress bars (default disables).")
    ap.add_argument(
        "--no-plots",
        action="store_true",
        help="Skip generating timing plots (default creates PNGs in the output directory).",
    )
    return ap


def read_file_with_timer(path: Path, now_fn) -> Tuple[bytes, float]:
    if not path.exists():
        raise FileNotFoundError(f"init/prior file not found: {path}")
    start = now_fn()
    data = path.read_bytes()
    duration = now_fn() - start
    return data, duration


def move_with_timer(src: Path, dst: Path, now_fn) -> float:
    dst.parent.mkdir(parents=True, exist_ok=True)
    start = now_fn()
    shutil.move(str(src), str(dst))
    return now_fn() - start


def ensure_executable(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"sw2d executable not found at {path}")
    if not os.access(path, os.X_OK):
        raise PermissionError(f"sw2d executable is not executable: {path}")


def make_plots(summary_rows: List[dict], out_dir: Path) -> None:
    if not summary_rows:
        print("[warn] no data available for plotting", file=sys.stderr)
        return
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - plotting optional
        raise RuntimeError("matplotlib is required for plotting") from exc

    aggregates = {}
    for row in summary_rows:
        key = (row["rows"], row["cols"], row["steps"])
        agg = aggregates.setdefault(
            key,
            {
                "rows": row["rows"],
                "cols": row["cols"],
                "steps": row["steps"],
                "cells": row["rows"] * row["cols"],
                "problem": row["rows"] * row["cols"] * row["steps"],
                "read": 0.0,
                "compute": 0.0,
                "write": 0.0,
                "count": 0,
            },
        )
        agg["read"] += row["read_time_s"]
        agg["compute"] += row["compute_time_s"]
        agg["write"] += row["write_time_s"]
        agg["count"] += 1

    entries = []
    for key, agg in aggregates.items():
        count = max(agg["count"], 1)
        entries.append(
            {
                "rows": agg["rows"],
                "cols": agg["cols"],
                "steps": agg["steps"],
                "problem": agg["problem"],
                "read": agg["read"] / count,
                "compute": agg["compute"] / count,
                "write": agg["write"] / count,
            }
        )
    entries.sort(key=lambda e: e["problem"])

    problem_sizes = [e["problem"] for e in entries]
    read_times = [e["read"] for e in entries]
    compute_times = [e["compute"] for e in entries]
    write_times = [e["write"] for e in entries]
    total_times = [r + c + w for r, c, w in zip(read_times, compute_times, write_times)]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(problem_sizes, compute_times, marker="o", label="Compute")
    ax.plot(problem_sizes, read_times, marker="o", label="Read")
    ax.plot(problem_sizes, write_times, marker="o", label="Write")
    ax.plot(problem_sizes, total_times, marker="o", label="Total")
    ax.set_xlabel("Problem size (rows * cols * steps)")
    ax.set_ylabel("Time (seconds)")
    ax.set_title("sw2d timings vs problem size (averaged per configuration)")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    plot_path = out_dir / "sw2d_timings.png"
    fig.tight_layout()
    fig.savefig(plot_path)
    plt.close(fig)
    print(f"[info] wrote timing plot to {plot_path}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_cli()
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    now_fn = compile_timer_helper(script_dir)

    rows_list = parse_range(args.rows, "rows")
    cols_list = parse_range(args.cols, "cols")
    steps_list = parse_range(args.steps, "steps")
    if args.save_interval <= 0:
        parser.error("--save-interval must be > 0")
    if args.repeat <= 0:
        parser.error("--repeat must be >= 1")

    exe_path = Path(args.exe).resolve()
    ensure_executable(exe_path)
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = Path(args.csv)
    if not csv_path.is_absolute():
        csv_path = out_dir / csv_path

    extra_args = shlex.split(args.extra)
    if not args.keep_progress:
        extra_args = extra_args + ["--no-progress"]

    combos = list(itertools.product(rows_list, cols_list, steps_list))
    total_runs = len(combos) * args.repeat

    init_path = Path(args.init).resolve() if args.init else None
    if init_path and not init_path.exists():
        raise FileNotFoundError(f"init file not found: {init_path}")

    summary_rows = []
    run_idx = 0
    for (rows, cols, steps) in combos:
        for rep in range(1, args.repeat + 1):
            run_idx += 1
            tag = f"r{rows}_c{cols}_s{steps}_rep{rep}"
            movie_tmp = out_dir / f"{tag}.tmp"
            if movie_tmp.exists():
                movie_tmp.unlink()

            read_time = 0.0
            if init_path:
                _, read_time = read_file_with_timer(init_path, now_fn)

            cmd = [
                str(exe_path),
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
                "--save-interval",
                str(args.save_interval),
                "--out",
                str(movie_tmp),
            ]
            if init_path:
                cmd += ["--init", str(init_path)]
            cmd += extra_args

            print(f"[{run_idx}/{total_runs}] running sw2d ({tag})")
            start_compute = now_fn()
            result = subprocess.run(cmd, cwd=str(script_dir))
            compute_time = now_fn() - start_compute
            if result.returncode != 0:
                print(f"[error] sw2d failed for {tag} (exit {result.returncode})", file=sys.stderr)
                return result.returncode
            if not movie_tmp.exists():
                print(f"[error] sw2d did not create expected movie file: {movie_tmp}", file=sys.stderr)
                return 1

            final_movie = out_dir / f"{tag}.bin"
            write_time = move_with_timer(movie_tmp, final_movie, now_fn)
            movie_bytes = final_movie.stat().st_size

            summary_rows.append(
                {
                    "rows": rows,
                    "cols": cols,
                    "steps": steps,
                    "dx": args.dx,
                    "dy": args.dy,
                    "height": args.height,
                    "save_interval": args.save_interval,
                    "repeat": rep,
                    "read_time_s": read_time,
                    "compute_time_s": compute_time,
                    "write_time_s": write_time,
                    "movie_bytes": movie_bytes,
                    "movie_path": str(final_movie),
                }
            )
            print(f"    read={read_time:.6f}s compute={compute_time:.6f}s write={write_time:.6f}s bytes={movie_bytes}")

    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rows",
                "cols",
                "steps",
                "dx",
                "dy",
                "height",
                "save_interval",
                "repeat",
                "read_time_s",
                "compute_time_s",
                "write_time_s",
                "movie_bytes",
                "movie_path",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_rows)

    print(f"[done] wrote {len(summary_rows)} rows to {csv_path}")

    if not args.no_plots:
        try:
            make_plots(summary_rows, out_dir)
        except Exception as exc:
            print(f"[warn] failed to generate plots: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
