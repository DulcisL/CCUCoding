#!/usr/bin/env python3
"""
Helper script for the sw2d shallow-water solver.

Features:
  * Runs the sw2d binary with any additional CLI flags.
  * Ensures an output state file is produced (movie.bin by default).
  * Visualizes the saved frames interactively or writes an MP4 when --movie is used.
"""
from __future__ import annotations

import argparse
import struct
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List, Sequence, Tuple

import numpy as np

try:
    import matplotlib.pyplot as plt
    from matplotlib import animation
    from matplotlib.colors import Colormap, LinearSegmentedColormap, Normalize, TwoSlopeNorm
except Exception as exc:  # pragma: no cover - matplotlib should be available
    print("Error: matplotlib is required to visualize sw2d output.", file=sys.stderr)
    raise
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401  (needed for 3D projection registration)


HEADER_FMT = "<4sIIiiii5d"
HEADER_SIZE = struct.calcsize(HEADER_FMT)


@dataclass
class Sw2DHeader:
    rows: int
    cols: int
    nframes: int
    save_interval: int
    dx: float
    dy: float
    dt: float
    g: float
    H0: float
    version: int
    flags: int


def parse_args(argv: Sequence[str] | None = None) -> Tuple[argparse.Namespace, List[str]]:
    parser = argparse.ArgumentParser(
        description="Run sw2d and visualize the binary movie output.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--binary",
        default=str(Path(__file__).with_name("sw2d")),
        help="Path to the compiled sw2d executable.",
    )
    parser.add_argument(
        "--state-file",
        default="movie.bin",
        help="Binary movie file from sw2d (will be created if sw2d runs).",
    )
    parser.add_argument("--movie", default=None, help="Optional MP4 path for a rendered animation.")
    parser.add_argument("--fps", type=int, default=20, help="Playback frames per second.")
    parser.add_argument(
        "--default-save-every",
        type=int,
        default=25,
        help="Save every N solver steps when sw2d is run and --save-interval was not supplied.",
    )
    parser.add_argument(
        "--no-run",
        action="store_true",
        help="Skip running sw2d and only visualize an existing --state-file.",
    )
    parser.add_argument("--auto-build", action="store_true", help="Run `make` if the sw2d binary is missing.")
    parser.add_argument(
        "--cmap",
        default="sw2d",
        help="Colormap name (default is a dark-blue to red ramp).",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=140,
        help="Figure DPI (used for the MP4 writer).",
    )

    args, extra = parser.parse_known_args(argv)
    if args.fps <= 0:
        parser.error("--fps must be positive")
    if args.default_save_every <= 0:
        parser.error("--default-save-every must be positive")
    return args, extra


def run_make(build_dir: Path) -> None:
    print(f"[sw2d_movie] sw2d missing; running `make` in {build_dir}", file=sys.stderr)
    subprocess.run(["make"], cwd=str(build_dir), check=True)


def find_option(args: List[str], name: str) -> Tuple[int | None, str | None]:
    """
    Return (index, value) for `--foo` or `--foo=bar`. Index is the position of the flag token.
    """
    prefix = f"{name}="
    for idx, token in enumerate(args):
        if token == name:
            if idx + 1 >= len(args):
                raise ValueError(f"{name} requires a value")
            return idx, args[idx + 1]
        if token.startswith(prefix):
            return idx, token[len(prefix) :]
    return None, None


def run_sw2d(
    executable: Path,
    state_file: Path,
    sw2d_args: List[str],
    default_save_every: int,
) -> Path:
    if not executable.exists():
        raise FileNotFoundError(f"sw2d executable not found at {executable}")

    # Ensure --out and --save-interval are present.
    out_idx, out_value = find_option(sw2d_args, "--out")
    if out_value is None:
        sw2d_args.extend(["--out", str(state_file)])
        out_value = str(state_file)
    state_path = Path(out_value).expanduser().resolve()
    state_path.parent.mkdir(parents=True, exist_ok=True)

    _, save_val = find_option(sw2d_args, "--save-interval")
    if save_val is None:
        if default_save_every <= 0:
            raise ValueError("--default-save-every must be > 0 when sw2d runs")
        sw2d_args.extend(["--save-interval", str(default_save_every)])
    else:
        if int(save_val) <= 0:
            raise ValueError("--save-interval must be > 0 to emit frames")

    cmd = [str(executable)] + sw2d_args
    print(f"[sw2d_movie] running: {' '.join(cmd)}", file=sys.stderr)
    subprocess.run(cmd, check=True)
    return state_path


def read_state_file(state_path: Path) -> Tuple[Sw2DHeader, np.memmap]:
    if not state_path.exists():
        raise FileNotFoundError(f"State file not found: {state_path}")
    with state_path.open("rb") as f:
        raw = f.read(HEADER_SIZE)
    if len(raw) != HEADER_SIZE:
        raise ValueError("Header too small. Expected 68 bytes.")

    (
        magic,
        version,
        flags,
        rows,
        cols,
        nframes,
        save_interval,
        dx,
        dy,
        dt,
        g,
        H0,
    ) = struct.unpack(HEADER_FMT, raw)
    if magic != b"SW2D":
        raise ValueError("Bad magic number. Not an sw2d movie file?")

    if rows <= 0 or cols <= 0:
        raise ValueError(f"Invalid dimensions: {rows}x{cols}")

    cell_count = rows * cols
    frame_values = cell_count * 3  # h,u,v
    frame_bytes = frame_values * 8

    total_bytes = state_path.stat().st_size
    payload = total_bytes - HEADER_SIZE
    if payload <= 0 or (payload % frame_bytes) != 0:
        raise ValueError("File size does not align with whole frames")

    inferred_frames = payload // frame_bytes
    if nframes <= 0 or nframes > inferred_frames:
        nframes = inferred_frames

    if nframes <= 0:
        raise ValueError("No frames present in movie (nframes <= 0).")

    header = Sw2DHeader(
        rows=rows,
        cols=cols,
        nframes=nframes,
        save_interval=save_interval,
        dx=dx,
        dy=dy,
        dt=dt,
        g=g,
        H0=H0,
        version=version,
        flags=flags,
    )

    frames = np.memmap(
        state_path,
        dtype="<f8",
        mode="r",
        offset=HEADER_SIZE,
        shape=(nframes, 3, rows, cols),
    )
    return header, frames


def resolve_colormap(name: str) -> Colormap:
    """
    Returns a Matplotlib colormap with dark blue mapped to min and red mapped to max.
    """
    if not name:
        name = "sw2d"
    lowered = name.strip().lower()
    base = [
        (0.0, "#001a5c"),   # dark blue for low water height
        (0.5, "#e8f4ff"),   # light blue/white near the neutral level
        (1.0, "#ff2b00"),   # red for peaks
    ]
    if lowered in {"sw2d", "sw2d-default", "blue-red", "red-high"}:
        return LinearSegmentedColormap.from_list("sw2d", base, N=256)
    try:
        return plt.get_cmap(name)
    except ValueError:
        print(f"Warning: Unknown colormap '{name}', falling back to sw2d blue-red ramp.", file=sys.stderr)
        return LinearSegmentedColormap.from_list("sw2d", base, N=256)


def build_figure(
    header: Sw2DHeader,
    frames: np.memmap,
    cmap: Colormap,
    fps: int,
) -> Tuple[plt.Figure, animation.FuncAnimation]:
    if header.nframes <= 0:
        raise ValueError("Movie has zero frames to visualize.")
    fig = plt.figure(figsize=(12, 5))
    gs = fig.add_gridspec(1, 2, width_ratios=[1, 1], wspace=0.2)
    ax_top = fig.add_subplot(gs[0, 0])
    ax_surface = fig.add_subplot(gs[0, 1], projection="3d")

    for ax in (ax_top,):
        ax.set_xticks([])
        ax.set_yticks([])

    h0 = frames[0, 0]
    h_min = float(np.min(frames[:, 0]))
    h_max = float(np.max(frames[:, 0]))
    if h_min < 1.0 < h_max:
        norm = TwoSlopeNorm(vmin=h_min, vcenter=1.0, vmax=h_max)
    else:
        norm = Normalize(vmin=h_min, vmax=h_max)

    im_h = ax_top.imshow(h0, origin="lower", cmap=cmap, norm=norm, interpolation="bilinear")
    ax_top.set_title("Surface height (top-down)")
    fig.colorbar(im_h, ax=ax_top, fraction=0.046, pad=0.04)

    x = np.arange(header.cols) * header.dx
    y = np.arange(header.rows) * header.dy
    X, Y = np.meshgrid(x, y)
    ax_surface.set_title("Surface height (3D)")
    ax_surface.set_xlabel("x")
    ax_surface.set_ylabel("y")
    ax_surface.set_zlabel("h")
    ax_surface.set_zlim(h_min, h_max if h_max > h_min else h_min + 1.0)
    surf = ax_surface.plot_surface(X, Y, h0, cmap=cmap, norm=norm, linewidth=0, antialiased=False)
    surf_container = {"surf": surf}
    ax_surface.view_init(elev=35, azim=-135)

    step_dt = header.save_interval * header.dt if header.save_interval > 0 else header.dt
    text = fig.suptitle("sw2d")

    def update(frame_idx: int):
        data = frames[frame_idx, 0]
        im_h.set_data(data)
        # Replace the surface for the new frame
        surf_container["surf"].remove()
        surf_container["surf"] = ax_surface.plot_surface(
            X, Y, data, cmap=cmap, norm=norm, linewidth=0, antialiased=False
        )
        sim_time = frame_idx * step_dt
        text.set_text(f"sw2d — frame {frame_idx + 1}/{header.nframes} — t = {sim_time:.3f}s")
        return im_h, surf_container["surf"], text

    interval = 1000.0 / max(fps, 1)
    anim = animation.FuncAnimation(fig, update, frames=header.nframes, interval=interval, blit=False, repeat=True)
    return fig, anim


def main(argv: Sequence[str] | None = None) -> int:
    args, sw2d_args = parse_args(argv)
    sw2d_args = list(sw2d_args)
    exe_path = Path(args.binary).expanduser().resolve()
    state_path = Path(args.state_file).expanduser().resolve()

    if not args.no_run:
        if not exe_path.exists():
            if args.auto_build:
                run_make(exe_path.parent)
                if not exe_path.exists():
                    print(f"sw2d binary still missing at {exe_path} after auto-build.", file=sys.stderr)
                    return 1
            else:
                print(f"sw2d binary not found at {exe_path}. Use --auto-build or build manually.", file=sys.stderr)
                return 1

        try:
            state_path = run_sw2d(exe_path, state_path, sw2d_args, args.default_save_every)
        except Exception as exc:  # pragma: no cover
            print(f"Failed to run sw2d: {exc}", file=sys.stderr)
            return 1

    try:
        header, frames = read_state_file(state_path)
    except Exception as exc:
        print(f"Failed to read state file '{state_path}': {exc}", file=sys.stderr)
        return 1

    colormap = resolve_colormap(args.cmap)
    fig, anim = build_figure(header, frames, colormap, args.fps)

    if args.movie:
        writer = animation.FFMpegWriter(fps=args.fps)
        print(f"[sw2d_movie] writing {args.movie}", file=sys.stderr)
        anim.save(args.movie, writer=writer, dpi=args.dpi)
        print(f"[sw2d_movie] done: {args.movie}", file=sys.stderr)
    else:
        plt.show()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
