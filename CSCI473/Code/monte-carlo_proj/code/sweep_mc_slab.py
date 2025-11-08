#!/usr/bin/env python3
# Tester file to sweep across multiple values and run simulations
"""
Usage: python ./sweep_mc_slab.py [-h] [--exe EXE] --C C --Cc CC --H-min H-MIN --H-max H-MAX --H-step H-STEP
                                --N N [--seed SEED] [--timeout TIMEOUT] [--trace] [--trace-every TRACE-EVERY]
                                [--make-convergence-plots] [--dpi DPI] [--title TITLE]

        Sweep H for mc_slab and plot results
        -h --help               Show this help message and exit
        --exe EXE               Path to mc_slab (default: ./mc_slab)
        --C C
        --Cc CC
        --H-min H-MIN
        --H-max H-MAX
        --H-step H-STEP
        --N N
        --seed SEED
        --timeout TIMEOUT
        --trace                 Enable per iteration tracing to CSV
        --trace-every TRACE-
                                Record every mth iteration
        --make-convergence-plots
                                When tracing also render convergence plots per H
        --dpi DPI
        --title TITLE
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple
import matplotlib

matplotlib.use("Agg")

DATA_DIR = Path(__file__).resolve().parent / "data"
SUMMARY_FILENAME = "sweep_results.csv"
PLOT_FILENAME = "sweep_convergence.png"
COLLISIONS_PLOT_FILENAME = "sweep_collisions.png"
TIMING_PLOT_FILENAME = "sweep_timings.png"
CONVERGENCE_DIR = DATA_DIR / "convergence"


@dataclass
class SweepResult:
    thickness: float
    particles: int
    absorbed: int
    transmitted: int
    reflected: int
    scatter_events: int
    absorption_events: int
    total_collisions: int
    total_track_length: float
    avg_collisions: float
    avg_path_length: float
    trace_file: Optional[str]
    elapsed_seconds: float
    read_seconds: float
    compute_seconds: float
    write_seconds: float

    @classmethod
    def from_json(cls, data: Dict[str, object]) -> "SweepResult":
        elapsed = float(data.get("elapsed_seconds", data.get("total_seconds", 0.0)))
        return cls(
            thickness=float(data["H"]),
            particles=int(data.get("n", 0)),
            absorbed=int(data["absorbed"]),
            transmitted=int(data["transmitted"]),
            reflected=int(data["reflected"]),
            scatter_events=int(data["scatter_events"]),
            absorption_events=int(data["absorption_events"]),
            total_collisions=int(data["total_collisions"]),
            total_track_length=float(data["total_track_length"]),
            avg_collisions=float(data["avg_collisions"]),
            avg_path_length=float(data["avg_path_length"]),
            trace_file=data.get("trace_file") if data.get("trace_file") else None,
            elapsed_seconds=elapsed,
            read_seconds=float(data.get("read_seconds", 0.0)),
            compute_seconds=float(data.get("compute_seconds", 0.0)),
            write_seconds=float(data.get("write_seconds", 0.0)),
        )

    @property
    def problem_size(self) -> int:
        if self.particles > 0:
            return self.particles
        return self.absorbed + self.transmitted + self.reflected


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Sweep slab thickness values for mc_slab and aggregate results."
    )
    parser.add_argument("--exe", default="./mc_slab", help="Path to mc_slab executable")
    parser.add_argument("--C", type=float, required=True, help="Total interaction coefficient")
    parser.add_argument("--Cc", type=float, required=True, help="Absorption coefficient")
    parser.add_argument("--H-min", type=float, required=True, dest="H_min", help="Minimum slab thickness")
    parser.add_argument("--H-max", type=float, required=True, dest="H_max", help="Maximum slab thickness")
    parser.add_argument("--H-step", type=float, required=True, dest="H_step", help="Step size for slab thickness")
    parser.add_argument("--N", type=int, required=True, help="Number of particles per run")
    parser.add_argument("--seed", type=int, help="Seed for mc_slab (set via MC_SLAB_SEED)")
    parser.add_argument("--timeout", type=float, default=None, help="Timeout per mc_slab invocation (seconds)")
    parser.add_argument("--trace", action="store_true", help="Enable per iteration tracing to CSV")
    parser.add_argument(
        "--trace-every",
        type=int,
        default=None,
        dest="trace_every",
        help="Record every mth neutron when tracing",
    )
    parser.add_argument(
        "--make-convergence-plots",
        action="store_true",
        help="Render convergence plots (requires matplotlib)",
    )
    parser.add_argument("--dpi", type=int, default=150, help="DPI for generated plots")
    parser.add_argument("--title", default=None, help="Optional plot title")
    return parser.parse_args(argv)


def ensure_data_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def sanitize_thickness(value: float, digits: int = 4) -> str:
    return f"{value:.{digits}f}".replace(".", "p")


def thickness_values(start: float, stop: float, step: float) -> List[float]:
    if step <= 0:
        raise ValueError("--H-step must be positive")
    values: List[float] = []
    current = start
    epsilon = step * 1e-9
    while current <= stop + epsilon:
        values.append(round(current, 10))
        current += step
    return values


def run_mc_slab(
    exe_path: Path,
    C: float,
    Cc: float,
    H: float,
    N: int,
    *,
    timeout: Optional[float],
    trace: bool,
    trace_every: Optional[int],
    trace_out: Optional[Path],
    seed: Optional[int],
) -> SweepResult:
    command = [
        str(exe_path),
        f"{C:.10g}",
        f"{Cc:.10g}",
        f"{H:.10g}",
        str(N),
    ]

    if trace and trace_out is not None:
        command.extend(["--trace-file", str(trace_out)])
        if trace_every:
            command.extend(["--trace-every", str(trace_every)])
    elif trace_every:
        # If trace not enabled but cadence requested, turn tracing on with default file.
        default_trace = trace_out if trace_out is not None else exe_path.parent / "data" / f"trace_H_{H:.4f}.csv"
        command.extend(["--trace-file", str(default_trace), "--trace-every", str(trace_every)])

    env = os.environ.copy()
    if seed is not None:
        env["MC_SLAB_SEED"] = str(seed)

    try:
        completed = subprocess.run(
            command,
            check=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
    except subprocess.CalledProcessError as exc:
        print(exc.stdout, file=sys.stderr)
        print(exc.stderr, file=sys.stderr)
        raise RuntimeError(f"mc_slab failed for H={H:.4g}") from exc

    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        print("Failed to decode mc_slab output:", completed.stdout, file=sys.stderr)
        raise RuntimeError("mc_slab output was not valid JSON") from exc

    return SweepResult.from_json(payload)


def write_results_csv(results: List[SweepResult], output_path: Path) -> None:
    headers = [
        "H",
        "n",
        "absorbed",
        "transmitted",
        "reflected",
        "scatter_events",
        "absorption_events",
        "total_collisions",
        "total_track_length",
        "avg_collisions",
        "avg_path_length",
        "trace_file",
        "elapsed_seconds",
        "read_seconds",
        "compute_seconds",
        "write_seconds",
    ]
    with output_path.open("w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)
        for row in results:
            writer.writerow(
                [
                    f"{row.thickness:.10f}",
                    row.particles,
                    row.absorbed,
                    row.transmitted,
                    row.reflected,
                    row.scatter_events,
                    row.absorption_events,
                    row.total_collisions,
                    f"{row.total_track_length:.10f}",
                    f"{row.avg_collisions:.10f}",
                    f"{row.avg_path_length:.10f}",
                    row.trace_file or "",
                    f"{row.elapsed_seconds:.6f}",
                    f"{row.read_seconds:.6f}",
                    f"{row.compute_seconds:.6f}",
                    f"{row.write_seconds:.6f}",
                ]
            )


def render_plots(
    results: List[SweepResult],
    *,
    output_path: Path,
    collisions_path: Path,
    dpi: int,
    title: Optional[str],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("matplotlib is required for --make-convergence-plots") from exc

    if not results:
        raise ValueError("No results available to plot.")

    H_values = [r.thickness for r in results]
    total_particles = results[0].absorbed + results[0].transmitted + results[0].reflected
    if total_particles <= 0:
        total_particles = 1
    absorbed_frac = [r.absorbed / total_particles for r in results]
    transmitted_frac = [r.transmitted / total_particles for r in results]
    reflected_frac = [r.reflected / total_particles for r in results]

    fig, ax = plt.subplots(figsize=(8, 5), dpi=dpi)
    ax.plot(H_values, absorbed_frac, label="Absorbed", marker="o")
    ax.plot(H_values, transmitted_frac, label="Transmitted", marker="s")
    ax.plot(H_values, reflected_frac, label="Reflected", marker="^")
    ax.set_xlabel("Slab thickness (H)")
    ax.set_ylabel("Fraction of particles")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    if title:
        ax.set_title(title)
    fig.tight_layout()
    fig.savefig(output_path, dpi=dpi)
    plt.close(fig)

    fig2, ax2 = plt.subplots(figsize=(8, 5), dpi=dpi)
    ax2.plot(H_values, [r.avg_collisions for r in results], marker="d", color="tab:purple")
    ax2.set_xlabel("Slab thickness (H)")
    ax2.set_ylabel("Average collisions per particle")
    ax2.grid(True, linestyle="--", alpha=0.4)
    if title:
        ax2.set_title(f"Average Collisions — {title}")
    fig2.tight_layout()
    fig2.savefig(collisions_path, dpi=dpi)
    plt.close(fig2)


def render_timing_plot(
    results: List[SweepResult],
    *,
    output_path: Path,
    dpi: int,
    title: Optional[str],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("matplotlib is required for timing plots") from exc

    if not results:
        raise ValueError("No results available to plot timings.")

    x_values = [float(r.thickness) for r in results]
    x_label = "Problem Size (H)"
    markers = {"Read": "o", "Compute": "s", "Write": "^", "Total": "d"}

    times = {
        "Read": [r.read_seconds for r in results],
        "Compute": [r.compute_seconds for r in results],
        "Write": [r.write_seconds for r in results],
        "Total": [r.elapsed_seconds for r in results],
    }

    fig, ax = plt.subplots(figsize=(8, 5), dpi=dpi)
    for label, values in times.items():
        ax.plot(x_values, values, marker=markers.get(label, "o"), label=label)
    ax.set_xlabel(x_label)
    ax.set_ylabel("Time (seconds)")
    if title:
        ax.set_title(f"Timings — {title}")
    else:
        ax.set_title("Timings vs Problem Size")
    ax.grid(True, linestyle="--", alpha=0.4)
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_path, dpi=dpi)
    plt.close(fig)


def read_terminal_events(trace_path: Path) -> List[str]:
    terminal_events = {"exit_left", "exit_right", "absorb"}
    outcomes: List[str] = []
    recorded_ids: set[str] = set()

    with trace_path.open(newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        if not reader.fieldnames or "event" not in reader.fieldnames:
            raise ValueError("Trace file missing 'event' header")
        for row in reader:
            if not row:
                continue
            event = (row.get("event") or "").strip()
            if event not in terminal_events:
                continue
            neutron_id = (row.get("neutron_id") or "").strip()
            if not neutron_id or neutron_id in recorded_ids:
                continue
            recorded_ids.add(neutron_id)
            outcomes.append(event)

    return outcomes


def render_convergence_timeseries(
    *,
    trace_path: Path,
    thickness: float,
    output_path: Path,
    dpi: int,
    title: Optional[str],
) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise RuntimeError("matplotlib is required for --make-convergence-plots") from exc

    outcomes = read_terminal_events(trace_path)
    if not outcomes:
        raise ValueError("Trace file did not contain any terminal events")

    key_map = {"absorb": "absorbed", "exit_right": "transmitted", "exit_left": "reflected"}
    ordered_keys = ["absorbed", "transmitted", "reflected"]
    counts = {key: 0 for key in ordered_keys}
    fractions: Dict[str, List[float]] = {key: [] for key in ordered_keys}
    steps: List[int] = []

    for idx, outcome in enumerate(outcomes, start=1):
        key = key_map[outcome]
        counts[key] += 1
        total = float(idx)
        for item in ordered_keys:
            fractions[item].append(counts[item] / total)
        steps.append(idx)

    fig, ax = plt.subplots(figsize=(8, 5), dpi=dpi)
    ax.plot(steps, fractions["absorbed"], label="Absorbed", color="tab:blue")
    ax.plot(steps, fractions["transmitted"], label="Transmitted", color="tab:orange")
    ax.plot(steps, fractions["reflected"], label="Reflected", color="tab:green")
    ax.set_xlabel("Traced neutrons")
    ax.set_ylabel("Running fraction")
    ax.set_ylim(0.0, 1.0)
    ax.grid(True, linestyle="--", alpha=0.4)

    if title:
        ax.set_title(f"{title} — H={thickness:.4f}")
    else:
        ax.set_title(f"Convergence — H={thickness:.4f}")

    ax.legend()
    fig.tight_layout()
    ensure_data_dir(output_path.parent)
    fig.savefig(output_path, dpi=dpi)
    plt.close(fig)


def generate_convergence_graphs(
    *,
    results: List[SweepResult],
    trace_requests: List[Optional[Path]],
    dpi: int,
    title: Optional[str],
) -> List[Tuple[float, Path]]:
    generated: List[Tuple[float, Path]] = []
    if len(trace_requests) != len(results):
        raise ValueError("Trace bookkeeping mismatch during convergence plotting")

    for result, requested_path in zip(results, trace_requests):
        candidate_paths: List[Path] = []
        if requested_path is not None:
            candidate_paths.append(requested_path)
        if result.trace_file:
            candidate_paths.append(Path(result.trace_file))

        trace_path: Optional[Path] = None
        for candidate in candidate_paths:
            candidate_path = candidate.resolve()
            if candidate_path.exists():
                trace_path = candidate_path
                break

        if trace_path is None:
            continue

        sanitized = sanitize_thickness(result.thickness)
        output_path = CONVERGENCE_DIR / f"convergence_H_{sanitized}.png"
        try:
            render_convergence_timeseries(
                trace_path=trace_path,
                thickness=result.thickness,
                output_path=output_path,
                dpi=dpi,
                title=title,
            )
        except ValueError as exc:
            print(f"Skipping convergence plot for H={result.thickness:.4f}: {exc}")
            continue

        generated.append((result.thickness, output_path))

    return generated


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)

    ensure_data_dir(DATA_DIR)

    exe_path = Path(args.exe).resolve()
    if not exe_path.exists():
        raise FileNotFoundError(f"mc_slab executable not found at {exe_path}")

    H_values = thickness_values(args.H_min, args.H_max, args.H_step)
    results: List[SweepResult] = []
    trace_requests: List[Optional[Path]] = []

    for idx, H in enumerate(H_values):
        trace_path = None
        if args.trace:
            sanitized = sanitize_thickness(H)
            trace_path = DATA_DIR / f"trace_H_{sanitized}.csv"
        seed = args.seed + idx if args.seed is not None else None
        result = run_mc_slab(
            exe_path,
            args.C,
            args.Cc,
            H,
            args.N,
            timeout=args.timeout,
            trace=args.trace,
            trace_every=args.trace_every,
            trace_out=trace_path,
            seed=seed,
        )
        results.append(result)
        trace_requests.append(trace_path)
        print(
            f"H={H:.5g} absorbed={result.absorbed} transmitted={result.transmitted} "
            f"reflected={result.reflected} avg_collisions={result.avg_collisions:.4f}"
        )

    results_csv = DATA_DIR / SUMMARY_FILENAME
    write_results_csv(results, results_csv)
    print(f"Wrote sweep summary to {results_csv}")

    if args.make_convergence_plots:
        plot_path = DATA_DIR / PLOT_FILENAME
        collisions_path = DATA_DIR / COLLISIONS_PLOT_FILENAME
        timing_path = DATA_DIR / TIMING_PLOT_FILENAME
        render_plots(
            results,
            output_path=plot_path,
            collisions_path=collisions_path,
            dpi=args.dpi,
            title=args.title,
        )
        render_timing_plot(
            results,
            output_path=timing_path,
            dpi=args.dpi,
            title=args.title,
        )
        print(f"Wrote convergence plot to {plot_path}")
        print(f"Wrote collision plot to {collisions_path}")
        print(f"Wrote timing plot to {timing_path}")

        convergence_outputs = generate_convergence_graphs(
            results=results,
            trace_requests=trace_requests,
            dpi=args.dpi,
            title=args.title,
        )
        for thickness, path in convergence_outputs:
            print(f"Wrote convergence graph for H={thickness:.4f} to {path}")
        if args.trace and not convergence_outputs:
            print("Trace data unavailable for convergence graphs; skipping per-H plots.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
