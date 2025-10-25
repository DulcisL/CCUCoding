#!/usr/bin/env python3
# Usage:
#   python3 display_image.py <path/to/file.dat> [--vmin 0] [--vmax 1] [--save out.png]

import sys, os, struct, argparse
import numpy as np
try:
    import matplotlib.pyplot as plt
    from matplotlib.colors import Normalize, LinearSegmentedColormap
except Exception:
    print("Error: matplotlib is required (pip install matplotlib).", file=sys.stderr)
    sys.exit(1)

def parse_args():
    if len(sys.argv) == 1:
        print("Usage: python3 display_image.py <path/to/file.dat> [--vmin 0] [--vmax 1] [--save out.png]")
        sys.exit(1)
    p = argparse.ArgumentParser(description="Display a headered .dat file as a heatmap (0=blue .. 1=red).")
    p.add_argument("dat_path", help="Path to .dat (e.g., ./data/initial.dat)")
    p.add_argument("--vmin", type=float, default=0.0)
    p.add_argument("--vmax", type=float, default=1.0)
    p.add_argument("--save", help="Optional image path (PNG). If omitted, auto-saves next to the .dat.")
    return p.parse_args()

def read_dat(path):
    path = os.path.expanduser(os.path.abspath(path))
    if not os.path.isfile(path): raise FileNotFoundError(f"File not found: {path}")
    with open(path, "rb") as f:
        hdr = f.read(8)
        if len(hdr) != 8: raise ValueError("Header too small")
        rows, cols = struct.unpack("<ii", hdr)
        if rows <= 0 or cols <= 0: raise ValueError(f"Bad dims: {rows}x{cols}")
        arr = np.fromfile(f, dtype="<f8", count=rows*cols)
        if arr.size != rows*cols: raise ValueError("Data truncated")
    return arr.reshape((rows, cols)), rows, cols, path

def main():
    a = parse_args()
    try:
        data, rows, cols, path = read_dat(a.dat_path)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr); sys.exit(1)

    cmap = LinearSegmentedColormap.from_list("blue_red", ["#0000FF", "#FF0000"])
    norm = Normalize(vmin=a.vmin, vmax=a.vmax, clip=True)

    plt.figure(figsize=(6,5))
    im = plt.imshow(data, cmap=cmap, norm=norm, origin="upper", interpolation="nearest")
    plt.colorbar(im, label="Value")
    plt.title(f"{os.path.basename(path)}  ({rows}x{cols})")
    plt.xlabel("Column (j)"); plt.ylabel("Row (i)")
    plt.tight_layout()

    out = a.save or (os.path.splitext(path)[0] + ".png")
    os.makedirs(os.path.dirname(out) or ".", exist_ok=True)
    plt.savefig(out, dpi=150)
    print(f"Saved heatmap to: {out}")
    # plt.show()

if __name__ == "__main__":
    main()
