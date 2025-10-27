#!/usr/bin/env python3
# display_image.py
# Render a single .dat (header + one frame) to a PNG heatmap without opening a window.
# Usage:
#   python3 display_image.py <path/to/file.dat> [--out out.png] [--vmin 0.0] [--vmax 1.0]
#
# Notes:
# - File format: [int32 rows][int32 cols][rows*cols doubles] (row-major)
# - Colormap: strict 0=blue .. 1=red
# - Borders colored explicitly: top/bottom blue, left/right red
# - Saves PNG; does not display.

import argparse
import os
import sys
import struct
import numpy as np

# Use non-GUI backend to avoid GTK/Qt deps
import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
from matplotlib.cm import ScalarMappable

def parse_args():
    p = argparse.ArgumentParser(description="Render a .dat matrix to a PNG heatmap (headless).")
    p.add_argument("dat_path", nargs="?", help="Path to .dat file with header (rows, cols).")
    p.add_argument("--out", help="Output PNG path (default: <input>.png)")
    p.add_argument("--vmin", type=float, default=0.0, help="Min value mapped to blue (default 0.0)")
    p.add_argument("--vmax", type=float, default=1.0, help="Max value mapped to red (default 1.0)")
    a = p.parse_args()
    if not a.dat_path:
        p.print_help()
        sys.exit(1)

    in_path = os.path.abspath(os.path.expanduser(a.dat_path))
    if not os.path.isfile(in_path):
        print(f"Error: not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    if a.out:
        out_path = os.path.abspath(os.path.expanduser(a.out))
        if not out_path.lower().endswith(".png"):
            print("Error: --out must end with .png", file=sys.stderr)
            sys.exit(1)
    else:
        base, _ = os.path.splitext(in_path)
        out_path = base + ".png"

    return in_path, out_path, a.vmin, a.vmax

def read_single_frame(in_path):
    with open(in_path, "rb") as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise RuntimeError("Header too small (need 8 bytes: int32 rows, int32 cols)")
        rows, cols = struct.unpack("<ii", hdr)

        if rows <= 0 or cols <= 0:
            raise RuntimeError(f"Bad dims in header: {rows}x{cols}")

        data_bytes = os.path.getsize(in_path) - 8
        expected = rows * cols * 8
        if data_bytes < expected:
            raise RuntimeError(f"Not enough data: have {data_bytes} bytes, need {expected}")

        frame = np.fromfile(f, dtype="<f8", count=rows*cols).reshape(rows, cols)
        return frame

def main():
    in_path, out_path, vmin, vmax = parse_args()

    try:
        frame = read_single_frame(in_path)
    except Exception as e:
        print(f"Error reading {in_path}: {e}", file=sys.stderr)
        sys.exit(1)

    rows, cols = frame.shape

    # Strict two-color gradient: 0 -> blue, 1 -> red
    cmap = LinearSegmentedColormap.from_list("blue_red", ["#0000FF", "#FF0000"], N=256)
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)

    # Pre-color to RGB so we can force border colors exactly
    rgb = (cmap(norm(frame))[..., :3] * 255).astype(np.uint8)

    BLUE = np.array([0, 0, 255], dtype=np.uint8)
    RED  = np.array([255, 0, 0], dtype=np.uint8)
    rgb[0, :, :]  = BLUE
    rgb[-1, :, :] = BLUE
    rgb[:, 0, :]  = RED
    rgb[:, -1, :] = RED

    # Figure/Axes explicit so colorbar knows where to attach
    dpi = 150
    fig, ax = plt.subplots(figsize=(6, 5), dpi=dpi)
    ax_img = ax.imshow(rgb, interpolation="nearest", origin="upper")
    ax.set_title(f"{os.path.basename(in_path)}  ({rows}x{cols})", fontsize=10)
    ax.set_xlabel("Column")
    ax.set_ylabel("Row")

    # Create a dummy mappable using the same cmap/norm for the colorbar
    sm = ScalarMappable(norm=norm, cmap=cmap)
    sm.set_array([])
    fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04, label="Value")

    fig.tight_layout()
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)
    fig.savefig(out_path, dpi=dpi)
    plt.close(fig)

    print(f"Saved: {out_path}")

if __name__ == "__main__":
    main()
