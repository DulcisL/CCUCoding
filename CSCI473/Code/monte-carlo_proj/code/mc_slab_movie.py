#!/usr/bin/env python3
# Main file for making the movie from the mc sim

"""
Usage: python ./mc_slab_movie.py --thickness THICKNESS --Sigma_t SIGMA_T --c C --N N [--frames FRAMES]
                                [--fps FPS] [--seed SEED] [--left-margin LEFT_MARGIN]
                                [--right-margin RIGHT_MARGIN] [--out OUT] [--fade-per-frame FADE_PER_FRAME]
                                [--glow-growth GLOW_GROWTH] [--glow-size-min GLOW_SIZE_MIN]
                                [--glow-size-max GLOW_SIZE_MAX] [--glow-alpha-min GLOW_ALPHA_MIN] [--dpi DPI]
                                [--fig-width FIG_WIDTH] [--fig-height FIG_HEIGHT]
                                [--hud-width-ratio HUD_WIDTH_RATIO]
options:
    -h --help       show this help message and exit
    --thickness THICKNESS
    --Sigma_t SIGMA_T
    --c C
    --N N
    [--frames FRAMES]
    [--fps FPS] [--seed SEED]
    [--left-margin LEFT_MARGIN]
    [--right-margin RIGHT_MARGIN]
    [--out OUT] [--fade-per-frame FADE_PER_FRAME]
    [--glow-growth GLOW_GROWTH]
    [--glow-size-min GLOW_SIZE_MIN]
    [--glow-size-max GLOW_SIZE_MAX]
    [--glow-alpha-min GLOW_ALPHA_MIN]
    [--dpi DPI]     Output DPI (Default: 150)
    [--fig-width FIG_WIDTH]
                    Figure width (inches)
    [--fig-height FIG_HEIGHT]
                    Figure height (inches)
    [--hud-width-ratio HUD_WIDTH_RATIO]
                    Relative width of left HUD column

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
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple

import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.collections import LineCollection

DATA_DIR = Path(__file__).resolve().parent / "data"
DEFAULT_MOVIE = "mc_slab_movie.mp4"
TRACE_FILENAME = "movie_trace.csv"
SUMMARY_FILENAME = "movie_summary.json"
BASE_COLORS = {
    "scatter": (0.0, 0.75, 0.93),
    "absorb": (0.93, 0.26, 0.25),
    "exit_right": (0.23, 0.90, 0.38),
    "exit_left": (0.23, 0.90, 0.38),
}


def format_eta(seconds: float) -> str:
    if seconds <= 0 or not math.isfinite(seconds):
        return "00:00"
    minutes = int(seconds // 60)
    secs = int(seconds % 60)
    return f"{minutes:02d}:{secs:02d}"


@dataclass
class Segment:
    neutron_id: int
    step: int
    start: Tuple[float, float]
    end: Tuple[float, float]
    event: str


def parse_args(argv: Optional[Iterable[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate an MP4 visualization of the mc_slab neutron histories."
    )
    parser.add_argument("--thickness", type=float, required=True, help="Slab thickness (H)")
    parser.add_argument("--Sigma_t", type=float, required=True, help="Total macroscopic cross section (C)")
    parser.add_argument("--c", type=float, required=True, help="Scattering fraction (Cs / C)")
    parser.add_argument("--N", type=int, required=True, help="Number of neutrons to track")
    parser.add_argument("--frames", type=int, default=None, help="Number of frames in the output animation")
    parser.add_argument("--fps", type=int, default=30, help="Frames per second for the MP4")
    parser.add_argument("--seed", type=int, default=None, help="Seed for reproducibility")
    parser.add_argument("--left-margin", type=float, default=1.0, help="Space to the left of the slab")
    parser.add_argument("--right-margin", type=float, default=1.0, help="Space to the right of the slab")
    parser.add_argument(
        "--out",
        default=str(DATA_DIR / DEFAULT_MOVIE),
        help="Output MP4 path (default: ./data/mc_slab_movie.mp4)",
    )
    parser.add_argument("--fade-per-frame", type=float, default=0.08, help="Alpha decay applied each frame")
    parser.add_argument("--glow-growth", type=float, default=0.35, help="Line width decay rate per frame")
    parser.add_argument("--glow-size-min", type=float, default=0.6, help="Minimum segment line width")
    parser.add_argument("--glow-size-max", type=float, default=2.6, help="Maximum segment line width")
    parser.add_argument("--glow-alpha-min", type=float, default=0.05, help="Minimum alpha for old segments")
    parser.add_argument("--dpi", type=int, default=150, help="Figure DPI")
    parser.add_argument("--fig-width", type=float, default=9.0, help="Figure width in inches")
    parser.add_argument("--fig-height", type=float, default=5.5, help="Figure height in inches")
    parser.add_argument("--hud-width-ratio", type=float, default=0.22, help="Relative HUD width")
    return parser.parse_args(argv)


def ensure_data_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def run_mc_slab(
    thickness: float,
    sigma_t: float,
    c_ratio: float,
    count: int,
    *,
    seed: Optional[int],
    trace_path: Path,
) -> Dict[str, object]:
    if not (0.0 < c_ratio <= 1.0):
        raise ValueError("--c must be in (0, 1]")
    C = sigma_t
    Cs = c_ratio * C
    Cc = C - Cs
    exe_path = Path(__file__).resolve().parent / "mc_slab"
    if not exe_path.exists():
        raise FileNotFoundError(f"mc_slab executable not found at {exe_path}")

    command = [
        str(exe_path),
        f"{C:.10g}",
        f"{Cc:.10g}",
        f"{thickness:.10g}",
        str(count),
        "--trace-file",
        str(trace_path),
        "--trace-every",
        "1",
    ]

    env = os.environ.copy()
    if seed is not None:
        env["MC_SLAB_SEED"] = str(seed)

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        check=True,
        env=env,
    )
    return json.loads(result.stdout)


def read_trace(path: Path) -> List[Segment]:
    segments: List[Segment] = []
    with path.open("r", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            segments.append(
                Segment(
                    neutron_id=int(row["neutron_id"]),
                    step=int(row["step"]),
                    start=(float(row["x_start"]), float(row["y_start"])),
                    end=(float(row["x_end"]), float(row["y_end"])),
                    event=row["event"],
                )
            )
    return segments


def build_progression(segments: Sequence[Segment]) -> List[Dict[str, int]]:
    absorbed = transmitted = reflected = scatter_events = 0
    progression: List[Dict[str, int]] = []
    for idx, segment in enumerate(segments):
        if segment.event == "absorb":
            absorbed += 1
        elif segment.event == "exit_right":
            transmitted += 1
        elif segment.event == "exit_left":
            reflected += 1
        elif segment.event == "scatter":
            scatter_events += 1
        progression.append(
            {
                "segments": idx + 1,
                "absorbed": absorbed,
                "transmitted": transmitted,
                "reflected": reflected,
                "scatter": scatter_events,
                "completed": absorbed + transmitted + reflected,
            }
        )
    return progression


def frames_segment_counts(total_segments: int, frames: int) -> List[int]:
    if frames <= 0:
        raise ValueError("Number of frames must be positive.")
    per_frame = max(1, math.ceil(total_segments / frames))
    counts = [min(total_segments, (idx + 1) * per_frame) for idx in range(frames)]
    if counts[-1] < total_segments:
        counts.append(total_segments)
    return counts


def make_animation(
    args: argparse.Namespace,
    segments: List[Segment],
    progression: List[Dict[str, int]],
    summary: Dict[str, object],
) -> Tuple[plt.Figure, Callable[[int], None], int]:
    ensure_data_dir(DATA_DIR)
    hud_ratio = max(0.05, min(args.hud_width_ratio, 0.45))
    gs_width = [hud_ratio, 1.0 - hud_ratio]

    fig = plt.figure(figsize=(args.fig_width, args.fig_height), dpi=args.dpi)
    gs = fig.add_gridspec(1, 2, width_ratios=gs_width, wspace=0.05)
    hud_ax = fig.add_subplot(gs[0, 0])
    plot_ax = fig.add_subplot(gs[0, 1])

    hud_ax.axis("off")
    hud_ax.set_xlim(0, 1)
    hud_ax.set_ylim(0, 1)
    plot_ax.set_xlim(-args.left_margin, args.thickness + args.right_margin)

    max_y = max(
        1.0,
        max(max(abs(seg.start[1]), abs(seg.end[1])) for seg in segments) if segments else 1.0,
    )
    plot_ax.set_ylim(-1.1 * max_y, 1.1 * max_y)
    plot_ax.set_xticks([])
    plot_ax.set_yticks([])
    plot_ax.spines["left"].set_visible(False)
    plot_ax.spines["right"].set_visible(False)
    plot_ax.spines["top"].set_visible(False)
    plot_ax.spines["bottom"].set_visible(False)

    # Background: white outside, black slab.
    plot_ax.set_facecolor("#fdfdfd")
    plot_ax.axvspan(0, args.thickness, color="black", alpha=0.98, zorder=-1)

    # Annotate slab boundary.
    plot_ax.axvline(0, color="black", linewidth=2.5, alpha=0.8, zorder=1)
    plot_ax.axvline(args.thickness, color="#222", linewidth=1.5, alpha=0.6, zorder=1)

    # Beam indicator on the boundary.
    beam_point = plot_ax.scatter(
        [0.0],
        [segments[0].start[1] if segments else 0.0],
        s=120,
        c="#ff3b3b",
        edgecolors="black",
        linewidths=0.6,
        zorder=5,
        label="beam",
    )
    plot_ax.text(
        -args.left_margin * 0.75,
        max_y * 0.9,
        "beam",
        color="#2e75ff",
        fontsize=12,
        fontweight="bold",
    )

    line_collection = LineCollection([], linewidths=args.glow_size_min, capstyle="round")
    plot_ax.add_collection(line_collection)

    frame_total = args.frames if args.frames else args.N
    frame_total = max(1, frame_total)
    frame_segment_totals = frames_segment_counts(len(segments), frame_total)
    total_frames = len(frame_segment_totals)

    hud_text = hud_ax.text(
        0.05,
        0.95,
        "",
        ha="left",
        va="top",
        fontsize=11,
        family="monospace",
    )

    total_neutrons = int(summary.get("n", args.N))

    def segment_styles(slice_upto: int) -> Tuple[List[List[Tuple[float, float]]], List[Tuple[float, float, float, float]], List[float]]:
        coords: List[List[Tuple[float, float]]] = []
        colors: List[Tuple[float, float, float, float]] = []
        widths: List[float] = []
        for idx, segment in enumerate(segments[:slice_upto]):
            coords.append([segment.start, segment.end])
            age = slice_upto - idx - 1
            base_color = BASE_COLORS.get(segment.event, (0.8, 0.8, 0.8))
            alpha = max(args.glow_alpha_min, 1.0 - args.fade_per_frame * age)
            alpha = min(1.0, alpha)
            colors.append((*base_color, alpha))
            width = max(args.glow_size_min, args.glow_size_max - args.glow_growth * age)
            widths.append(width)
        return coords, colors, widths

    def format_hud(frame_idx: int, slice_upto: int) -> str:
        if slice_upto == 0:
            counts = {"absorbed": 0, "transmitted": 0, "reflected": 0, "scatter": 0, "completed": 0}
        else:
            counts = progression[slice_upto - 1]
        lines = [
            f"Frame {frame_idx + 1}/{len(frame_segment_totals)}",
            f"Segments: {slice_upto}/{len(segments)}",
            f"Neutrons: {counts['completed']}/{total_neutrons}",
            "",
            f"Absorbed     : {counts['absorbed']}",
            f"Transmitted  : {counts['transmitted']}",
            f"Reflected    : {counts['reflected']}",
            f"Scatter events: {counts['scatter']}",
        ]
        return "\n".join(lines)

    def update(frame_idx: int) -> None:
        slice_upto = frame_segment_totals[frame_idx]
        coords, colors, widths = segment_styles(slice_upto)
        line_collection.set_segments(coords)
        line_collection.set_color(colors)
        line_collection.set_linewidths(widths)
        hud_text.set_text(format_hud(frame_idx, slice_upto))
        fig.canvas.draw_idle()

    return fig, update, total_frames


def save_animation(fig: plt.Figure, update_func: Callable[[int], None], total_frames: int, output_path: Path, fps: int) -> None:
    writer = animation.FFMpegWriter(fps=fps, bitrate=2400)
    start_clock = time.perf_counter()
    status_width = 0
    try:
        with writer.saving(fig, str(output_path), fig.dpi):
            for frame_idx in range(total_frames):
                update_func(frame_idx)
                writer.grab_frame()
                progress_fraction = (frame_idx + 1) / float(total_frames)
                elapsed = time.perf_counter() - start_clock
                remaining = (elapsed / progress_fraction) - elapsed if progress_fraction > 0 else 0.0
                status = (
                    f"Progress: {progress_fraction * 100:6.2f}% | "
                    f"Frame {frame_idx + 1}/{total_frames} | ETA {format_eta(remaining)}"
                )
                padding = max(0, status_width - len(status))
                sys.stdout.write("\r" + status + " " * padding)
                sys.stdout.flush()
                status_width = max(status_width, len(status))
    except FileNotFoundError as exc:
        raise RuntimeError(
            "ffmpeg is required to write MP4 files. Please install ffmpeg and try again."
        ) from exc
    finally:
        sys.stdout.write("\n")
        sys.stdout.flush()
        plt.close(fig)


def main(argv: Optional[Iterable[str]] = None) -> int:
    args = parse_args(argv)
    ensure_data_dir(DATA_DIR)

    trace_path = DATA_DIR / TRACE_FILENAME
    summary = run_mc_slab(
        thickness=args.thickness,
        sigma_t=args.Sigma_t,
        c_ratio=args.c,
        count=args.N,
        seed=args.seed,
        trace_path=trace_path,
    )

    segments = read_trace(trace_path)
    if not segments:
        raise RuntimeError("Trace file is empty; nothing to animate.")

    progression = build_progression(segments)
    fig, update_func, total_frames = make_animation(args, segments, progression, summary)

    output_path = Path(args.out)
    if not output_path.is_absolute():
        output_path = DATA_DIR / output_path
    ensure_data_dir(output_path.parent)

    save_animation(fig, update_func, total_frames, output_path, fps=args.fps)
    print(f"Saved animation to {output_path}")

    summary_path = DATA_DIR / SUMMARY_FILENAME
    with summary_path.open("w") as fp:
        json.dump(summary, fp, indent=2)
    print(f"Wrote simulation summary to {summary_path}")
    print(f"Trace data available at {trace_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
