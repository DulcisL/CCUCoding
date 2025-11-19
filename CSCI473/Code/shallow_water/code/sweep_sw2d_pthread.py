#!/usr/bin/env python3
"""
Parameter sweep runner for sw2d_pthread that benchmarks multiple grid sizes and thread counts.
It reuses timer.h via a small shared helper so we capture read/compute/write timings consistently.
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
from collections import defaultdict
from typing import Dict, List, Sequence, Tuple


def compile_timer_helper(script_dir: Path) -> ctypes.CFUNCTYPE:
    header = script_dir / "timer.h"
    if not header.exists():
        raise FileNotFoundError(f"timer.h not found: {header}")
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
        subprocess.run(cmd, input=code.encode("utf-8"), cwd=str(script_dir), check=True)
    lib = ctypes.CDLL(str(so_path))
    lib.sw2d_now.restype = ctypes.c_double
    return lib.sw2d_now


def parse_range(spec: str, kind: str) -> List[int]:
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
        description="Benchmark sw2d_pthread by sweeping rows/cols/steps/thread counts.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    ap.add_argument("--exe", default=str(Path(__file__).with_name("sw2d_pthread")),
                    help="Path to sw2d_pthread executable.")
    ap.add_argument("--rows", default="200", help="Row counts (comma list or start:end:step).")
    ap.add_argument("--cols", default="200", help="Column counts (comma list or start:end:step).")
    ap.add_argument("--steps", default="2000", help="Time steps (comma list or start:end:step).")
    ap.add_argument("--threads", default="1", help="Thread counts (comma list or start:end:step).")
    ap.add_argument("--dx", type=float, default=1.0, help="Cell size in x.")
    ap.add_argument("--dy", type=float, default=1.0, help="Cell size in y.")
    ap.add_argument("--height", type=float, default=0.5, help="Initial column height.")
    ap.add_argument("--save-interval", type=int, default=50, help="Frames between saves (must be >0).")
    ap.add_argument("--repeat", type=int, default=1, help="Repeat count for each configuration.")
    ap.add_argument("--init", type=str, help="Optional init/prior file passed to sw2d_pthread.")
    ap.add_argument("--out-dir", default="sw2d_pthread_sweep", help="Output directory for results and plots.")
    ap.add_argument("--csv", default="sw2d_pthread_summary.csv",
                    help="Summary CSV filename (inside out-dir if relative).")
    ap.add_argument("--keep-movies", action="store_true", help="Preserve movie stacks (default deletes after timing).")
    ap.add_argument("--extra", default="", help="Additional solver flags (quoted string).")
    ap.add_argument("--keep-progress", action="store_true", help="Keep solver progress bars visible.")
    ap.add_argument("--no-plots", action="store_true", help="Skip generating PNG timing plots.")
    ap.add_argument(
        "--eff-targets",
        default="0.6,0.75,0.9",
        help="Comma-separated efficiency targets for iso-efficiency curves.",
    )
    return ap


def read_file_with_timer(path: Path, now_fn) -> float:
    if not path.exists():
        raise FileNotFoundError(f"init/prior file not found: {path}")
    start = now_fn()
    _ = path.read_bytes()
    return now_fn() - start


def move_with_timer(src: Path, dst: Path, now_fn) -> float:
    dst.parent.mkdir(parents=True, exist_ok=True)
    start = now_fn()
    shutil.move(str(src), str(dst))
    return now_fn() - start


def ensure_executable(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Executable not found: {path}")
    if not os.access(path, os.X_OK):
        raise PermissionError(f"Executable is not runnable: {path}")


def parse_eff_targets(spec: str) -> List[float]:
    targets = []
    for token in spec.split(","):
        token = token.strip()
        if not token:
            continue
        try:
            val = float(token)
        except ValueError as exc:
            raise ValueError(f"Invalid efficiency target '{token}'") from exc
        if not (0.0 < val <= 1.0):
            raise ValueError("Efficiency targets must be in (0,1].")
        targets.append(val)
    if not targets:
        raise ValueError("Provide at least one efficiency target.")
    return sorted(set(targets))


def aggregate_runs(rows: List[Dict]) -> List[Dict]:
    accum: Dict[Tuple[int, int, int, int], Dict[str, float]] = {}
    for row in rows:
        key = (row["rows"], row["cols"], row["steps"], row["threads"])
        entry = accum.setdefault(
            key,
            {
                "rows": row["rows"],
                "cols": row["cols"],
                "steps": row["steps"],
                "threads": row["threads"],
                "sum_read": 0.0,
                "sum_compute": 0.0,
                "sum_write": 0.0,
                "count": 0,
            },
        )
        entry["sum_read"] += row["read_time_s"]
        entry["sum_compute"] += row["compute_time_s"]
        entry["sum_write"] += row["write_time_s"]
        entry["count"] += 1

    summary_entries: List[Dict] = []
    per_problem: Dict[Tuple[int, int, int], List[Dict]] = defaultdict(list)
    for (rows_val, cols_val, steps_val, threads_val), data in accum.items():
        count = max(1, data["count"])
        avg_read = data["sum_read"] / count
        avg_compute = data["sum_compute"] / count
        avg_write = data["sum_write"] / count
        entry = {
            "rows": rows_val,
            "cols": cols_val,
            "steps": steps_val,
            "threads": threads_val,
            "problem": rows_val * cols_val * steps_val,
            "avg_read_time_s": avg_read,
            "avg_compute_time_s": avg_compute,
            "avg_write_time_s": avg_write,
            "count": count,
        }
        summary_entries.append(entry)
        per_problem[(rows_val, cols_val, steps_val)].append(entry)

    for entries in per_problem.values():
        entries.sort(key=lambda e: e["threads"])
        if not entries:
            continue
        baseline = entries[0]
        base_time = baseline["avg_compute_time_s"]
        for entry in entries:
            runtime = entry["avg_compute_time_s"]
            speed = base_time / runtime if runtime > 0 else float("nan")
            eff = speed / entry["threads"] if entry["threads"] > 0 else float("nan")
            entry["speedup"] = speed
            entry["efficiency"] = eff
    summary_entries.sort(key=lambda e: (e["rows"], e["cols"], e["steps"], e["threads"]))
    return summary_entries


def group_entries_by_problem(summary_entries: List[Dict]) -> List[Tuple[Tuple[int, int, int], List[Dict]]]:
    per_problem: Dict[Tuple[int, int, int], List[Dict]] = defaultdict(list)
    for entry in summary_entries:
        per_problem[(entry["rows"], entry["cols"], entry["steps"])].append(entry)
    grouped: List[Tuple[Tuple[int, int, int], List[Dict]]] = []
    for key, entries in per_problem.items():
        entries.sort(key=lambda e: e["threads"])
        grouped.append((key, entries))
    grouped.sort(key=lambda item: item[0][0] * item[0][1] * item[0][2])
    return grouped


def build_problem_speedup_rows(
    grouped_entries: List[Tuple[Tuple[int, int, int], List[Dict]]]
) -> List[Dict]:
    rows: List[Dict] = []
    for (rows_val, cols_val, steps_val), entries in grouped_entries:
        if not entries:
            continue
        best = max(entries, key=lambda e: e.get("speedup", float("-inf")))
        rows.append(
            {
                "rows": rows_val,
                "cols": cols_val,
                "steps": steps_val,
                "problem": rows_val * cols_val * steps_val,
                "best_threads": best["threads"],
                "best_speedup": best.get("speedup", float("nan")),
                "best_efficiency": best.get("efficiency", float("nan")),
            }
        )
    rows.sort(key=lambda e: e["problem"])
    return rows


def print_speedup_summary(
    grouped_entries: List[Tuple[Tuple[int, int, int], List[Dict]]]
) -> None:
    if not grouped_entries:
        print("[info] no speedup data available for summary")
        return
    print("[summary] speedup by problem size:")
    for (rows_val, cols_val, steps_val), entries in grouped_entries:
        series = ", ".join(f"{entry['threads']}t={entry.get('speedup', float('nan')):.2f}x" for entry in entries)
        best = max(entries, key=lambda e: e.get("speedup", float("-inf")))
        best_speed = best.get("speedup", float("nan"))
        best_threads = best["threads"]
        best_eff = best.get("efficiency", float("nan"))
        label = f"{rows_val}x{cols_val}x{steps_val}"
        print(f"    {label}: {series} (best {best_speed:.2f}x @ {best_threads} threads, eff {best_eff:.2f})")


def generate_plots(summary_entries: List[Dict], eff_targets: List[float], out_dir: Path) -> None:
    grouped_entries = group_entries_by_problem(summary_entries)
    if not grouped_entries:
        print("[warn] no summary data to plot", file=sys.stderr)
        return
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:
        raise RuntimeError("matplotlib is required for plotting") from exc

    runtime_plot = out_dir / "sw2d_pthread_runtime.png"
    speedup_plot = out_dir / "sw2d_pthread_speedup.png"
    efficiency_plot = out_dir / "sw2d_pthread_efficiency.png"
    isoeff_plot = out_dir / "sw2d_pthread_isoefficiency.png"

    fig_runtime, ax_runtime = plt.subplots(figsize=(8, 5))
    fig_speed, ax_speed = plt.subplots(figsize=(8, 5))
    fig_eff, ax_eff = plt.subplots(figsize=(8, 5))
    iso_map: Dict[float, Dict[int, float]] = {target: {} for target in eff_targets}

    for (rows_val, cols_val, steps_val), entries in grouped_entries:
        threads = [e["threads"] for e in entries]
        read_times = [e["avg_read_time_s"] for e in entries]
        compute_times = [e["avg_compute_time_s"] for e in entries]
        write_times = [e["avg_write_time_s"] for e in entries]
        speedups = [e.get("speedup", float("nan")) for e in entries]
        efficiencies = [e.get("efficiency", float("nan")) for e in entries]
        label = f"{rows_val}x{cols_val}x{steps_val}"

        ax_runtime.plot(threads, compute_times, marker="o", label=f"{label} compute")
        if any(val > 0 for val in read_times):
            ax_runtime.plot(threads, read_times, marker="o", linestyle="--", label=f"{label} read")
        if any(val > 0 for val in write_times):
            ax_runtime.plot(threads, write_times, marker="o", linestyle=":", label=f"{label} write")
        ax_speed.plot(threads, speedups, marker="o", label=label)
        ax_eff.plot(threads, efficiencies, marker="o", label=label)

        for entry in entries:
            for target in eff_targets:
                if entry.get("efficiency", 0.0) >= target and entry["threads"] not in iso_map[target]:
                    iso_map[target][entry["threads"]] = entry["problem"]

    for ax, title, ylabel in [
        (ax_runtime, "sw2d_pthread compute time vs threads", "Compute time (s)"),
        (ax_speed, "sw2d_pthread speedup vs threads", "Speedup"),
        (ax_eff, "sw2d_pthread efficiency vs threads", "Efficiency"),
    ]:
        ax.set_xlabel("Threads")
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.grid(True, linestyle="--", alpha=0.4)
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
        ax.figure.tight_layout()

    fig_runtime.savefig(runtime_plot, bbox_inches="tight")
    fig_speed.savefig(speedup_plot, bbox_inches="tight")
    fig_eff.savefig(efficiency_plot, bbox_inches="tight")
    plt.close(fig_runtime)
    plt.close(fig_speed)
    plt.close(fig_eff)
    print(f"[info] wrote runtime plot to {runtime_plot}")
    print(f"[info] wrote speedup plot to {speedup_plot}")
    print(f"[info] wrote efficiency plot to {efficiency_plot}")

    fig_iso, ax_iso = plt.subplots(figsize=(8, 5))
    for target, mapping in iso_map.items():
        if not mapping:
            continue
        threads_sorted = sorted(mapping.keys())
        problems = [mapping[t] for t in threads_sorted]
        ax_iso.plot(threads_sorted, problems, marker="o", label=f"eff≥{target}")
    ax_iso.set_xlabel("Threads")
    ax_iso.set_ylabel("Problem size (rows*cols*steps)")
    ax_iso.set_title("Iso-efficiency curves")
    ax_iso.grid(True, linestyle="--", alpha=0.4)
    ax_iso.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
    fig_iso.tight_layout()
    fig_iso.savefig(isoeff_plot, bbox_inches="tight")
    plt.close(fig_iso)
    print(f"[info] wrote iso-efficiency plot to {isoeff_plot}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_cli()
    args = parser.parse_args(argv)

    script_dir = Path(__file__).resolve().parent
    now_fn = compile_timer_helper(script_dir)

    rows_list = parse_range(args.rows, "rows")
    cols_list = parse_range(args.cols, "cols")
    steps_list = parse_range(args.steps, "steps")
    threads_list = parse_range(args.threads, "threads")
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

    init_path = Path(args.init).resolve() if args.init else None
    if init_path and not init_path.exists():
        raise FileNotFoundError(f"init file not found: {init_path}")
    eff_targets = parse_eff_targets(args.eff_targets)
    extra_args = shlex.split(args.extra)
    if not args.keep_progress:
        extra_args = extra_args + ["--no-progress"]

    combos = list(itertools.product(rows_list, cols_list, steps_list, threads_list))
    total_runs = len(combos) * args.repeat

    raw_rows = []
    run_idx = 0
    for rows_val, cols_val, steps_val, threads_val in combos:
        for rep in range(1, args.repeat + 1):
            run_idx += 1
            tag = f"r{rows_val}_c{cols_val}_s{steps_val}_t{threads_val}_rep{rep}"
            movie_tmp = out_dir / f"{tag}.tmp"
            if movie_tmp.exists():
                movie_tmp.unlink()

            read_time = 0.0
            if init_path:
                read_time = read_file_with_timer(init_path, now_fn)

            cmd = [
                str(exe_path),
                "--rows",
                str(rows_val),
                "--cols",
                str(cols_val),
                "--steps",
                str(steps_val),
                "--dx",
                f"{args.dx}",
                "--dy",
                f"{args.dy}",
                "--height",
                f"{args.height}",
                "--save-interval",
                str(args.save_interval),
                "--threads",
                str(threads_val),
                "--out",
                str(movie_tmp),
            ]
            if init_path:
                cmd += ["--init", str(init_path)]
            cmd += extra_args

            print(f"[{run_idx}/{total_runs}] sw2d_pthread ({tag})")
            start_compute = now_fn()
            result = subprocess.run(cmd, cwd=str(script_dir))
            compute_time = now_fn() - start_compute
            if result.returncode != 0:
                print(f"[error] sw2d_pthread failed for {tag} (exit {result.returncode})", file=sys.stderr)
                return result.returncode
            movie_bytes = movie_tmp.stat().st_size if movie_tmp.exists() else 0
            write_time = 0.0
            final_movie_path = ""
            if args.keep_movies:
                final_movie = out_dir / f"{tag}.bin"
                write_time = move_with_timer(movie_tmp, final_movie, now_fn)
                final_movie_path = str(final_movie)
            else:
                movie_tmp.unlink(missing_ok=True)
                final_movie_path = ""

            raw_rows.append(
                {
                    "rows": rows_val,
                    "cols": cols_val,
                    "steps": steps_val,
                    "threads": threads_val,
                    "dx": args.dx,
                    "dy": args.dy,
                    "height": args.height,
                    "save_interval": args.save_interval,
                    "repeat": rep,
                    "read_time_s": read_time,
                    "compute_time_s": compute_time,
                    "write_time_s": write_time,
                    "movie_bytes": movie_bytes,
                    "movie_path": final_movie_path,
                }
            )
            print(
                f"    read={read_time:.6f}s compute={compute_time:.6f}s "
                f"write={write_time:.6f}s bytes={movie_bytes}"
            )

    raw_csv = out_dir / "sw2d_pthread_raw.csv"
    with raw_csv.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rows",
                "cols",
                "steps",
                "threads",
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
        writer.writerows(raw_rows)
    print(f"[info] wrote raw runs to {raw_csv}")

    summary_entries = aggregate_runs(raw_rows)
    grouped_entries = group_entries_by_problem(summary_entries)
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rows",
                "cols",
                "steps",
                "threads",
                "problem",
                "avg_read_time_s",
                "avg_compute_time_s",
                "avg_write_time_s",
                "speedup",
                "efficiency",
                "count",
            ],
        )
        writer.writeheader()
        writer.writerows(summary_entries)

    problem_rows = build_problem_speedup_rows(grouped_entries)
    problem_csv = csv_path.with_name(f"{csv_path.stem}_problems.csv")
    with problem_csv.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "rows",
                "cols",
                "steps",
                "problem",
                "best_threads",
                "best_speedup",
                "best_efficiency",
            ],
        )
        writer.writeheader()
        writer.writerows(problem_rows)

    print_speedup_summary(grouped_entries)
    print(f"[done] wrote {len(summary_entries)} summary rows to {csv_path}")
    print(f"[done] wrote {len(problem_rows)} problem-level speedup rows to {problem_csv}")

    if not args.no_plots:
        try:
            generate_plots(summary_entries, eff_targets, out_dir)
        except Exception as exc:
            print(f"[warn] failed to generate plots: {exc}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
