#!/usr/bin/env python3
# make-movie.py
#
# Read a stacked .dat from the data directory, split into timesteps, and save an MP4
# next to the input file (in the same data directory).
#
# Usage:
#   python3 make-movie.py <path/to/stack.dat> [--fps 10] [--vmin 0.0] [--vmax 1.0] [--out out.mp4]
#
# Notes:
# - Input format: [int32 rows][int32 cols][frames * rows * cols doubles] (row-major)
# - Frames = (filesize - 8) / (rows*cols*8)
# - Colormap: 0 -> blue, 1 -> red
# - Output must be .mp4. If --out is omitted, outputs <input_basename>.mp4 in the same directory.

import os
import sys
import struct
import argparse
import numpy as np

try:
    import av  # PyAV direct API (already present if imageio pyav works)
except Exception:
    print("Error: PyAV is required but not available on this system.", file=sys.stderr)
    sys.exit(1)

try:
    from matplotlib.colors import Normalize, LinearSegmentedColormap
except Exception:
    print("Error: matplotlib is required (pip install matplotlib).", file=sys.stderr)
    sys.exit(1)


def usage_and_exit(parser):
    parser.print_help()
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(
        description="Make an MP4 from a stacked .dat (header + frames). "
                    "Saves the MP4 in the same data directory."
    )
    p.add_argument("stack_path", nargs="?", help="Path to stacked .dat (e.g., ./data/all.100x100x500.dat)")
    p.add_argument("--fps", type=int, default=10, help="Frames per second (default: 10)")
    p.add_argument("--vmin", type=float, default=0.0, help="Min value for colormap (default: 0.0)")
    p.add_argument("--vmax", type=float, default=1.0, help="Max value for colormap (default: 1.0)")
    p.add_argument("--out", dest="out_mp4", help="Output MP4 path (must end with .mp4). Default: <stack_basename>.mp4")
    args = p.parse_args()

    if not args.stack_path:
        usage_and_exit(p)

    in_path = os.path.abspath(os.path.expanduser(args.stack_path))
    if not os.path.isfile(in_path):
        print(f"Error: not found: {in_path}", file=sys.stderr)
        sys.exit(1)

    # Default output: same dir, same basename, .mp4
    if args.out_mp4:
        out_path = os.path.abspath(os.path.expanduser(args.out_mp4))
        if not out_path.lower().endswith(".mp4"):
            print("Error: --out must end with .mp4", file=sys.stderr)
            sys.exit(1)
    else:
        base, _ = os.path.splitext(in_path)
        out_path = base + ".mp4"

    return in_path, out_path, args.fps, args.vmin, args.vmax


def read_stack_header_and_shape(in_path):
    with open(in_path, "rb") as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise RuntimeError("Header too small (need 8 bytes: int32 rows, int32 cols)")
        rows, cols = struct.unpack("<ii", hdr)

    if rows <= 0 or cols <= 0:
        raise RuntimeError(f"Bad dims in header: {rows}x{cols}")

    sz = os.path.getsize(in_path)
    bytes_per_frame = rows * cols * 8  # doubles
    data_bytes = sz - 8
    if data_bytes <= 0 or (data_bytes % bytes_per_frame) != 0:
        raise RuntimeError("Data size is not a multiple of frame size (rows*cols*sizeof(double))")

    frames = data_bytes // bytes_per_frame
    if frames < 1:
        raise RuntimeError("No frames found in stack")

    return rows, cols, frames


def frame_generator(in_path, rows, cols, frames, vmin, vmax):
    """
    Yields frames as RGB uint8 arrays with shape (rows, cols, 3), C-contiguous.
    """
    mmap = np.memmap(in_path, dtype="<f8", mode="r", offset=8, shape=(frames, rows, cols))
    cmap = LinearSegmentedColormap.from_list("blue_red", ["#0000FF", "#FF0000"])
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)

    for t in range(frames):
        rgba = cmap(norm(mmap[t]))               # (rows, cols, 4), float64 in [0, 1]
        rgb = (rgba[..., :3] * 255).astype(np.uint8)
        yield np.ascontiguousarray(rgb)          # ensure C-contiguous (H, W, 3)


def write_mp4_with_pyav(out_path, rows, cols, frames_iter, fps):
    """
    Writes MP4 using PyAV directly. Tries libx264, falls back to mpeg4 if needed.
    Always writes .mp4 container.
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    # Try x264 first; fall back to mpeg4 if not available
    for codec in ("libx264", "mpeg4"):
        try:
            container = av.open(out_path, mode="w")
            stream = container.add_stream(codec, rate=fps)
            # Use a widely compatible pixel format
            stream.pix_fmt = "yuv420p"
            # (Optional) set dimensions via frames (PyAV infers from frame)
            # Write frames
            for rgb in frames_iter:
                # Create a VideoFrame in RGB, then convert to stream pix_fmt (yuv420p)
                frame = av.VideoFrame.from_ndarray(rgb, format="rgb24")
                # Reformat to the stream's pixel format (yuv420p) and size
                frame = frame.reformat(width=cols, height=rows, format=stream.pix_fmt)
                packet = stream.encode(frame)
                if packet:
                    container.mux(packet)
            # Flush encoder
            packet = stream.encode(None)
            if packet:
                container.mux(packet)
            container.close()
            return  # success
        except av.AVError as e:
            # Try next codec
            try:
                container.close()
            except Exception:
                pass
            # Reset the generator for the retry: caller must pass a fresh iterator each time
            raise
        except Exception:
            try:
                container.close()
            except Exception:
                pass
            raise

    raise RuntimeError("Failed to write MP4 with available codecs.")


def main():
    in_path, out_path, fps, vmin, vmax = parse_args()

    try:
        rows, cols, frames = read_stack_header_and_shape(in_path)
    except Exception as e:
        print(f"Error reading stack: {e}", file=sys.stderr)
        sys.exit(1)

    # Build a fresh generator for the first attempt
    frames_iter = frame_generator(in_path, rows, cols, frames, vmin, vmax)

    try:
        # Important: the generator is consumed inside write; if it raises,
        # we need to rebuild a fresh generator and retry with fallback codec.
        write_mp4_with_pyav(out_path, rows, cols, frames_iter, fps)
    except av.AVError:
        # Retry once with fallback codec ('mpeg4') using a new generator
        try:
            frames_iter = frame_generator(in_path, rows, cols, frames, vmin, vmax)
            # Force mpeg4 by calling write again but allowing exception to propagate to caller
            # (We set codec choice inside write_mp4_with_pyav; here just re-invoke.)
            write_mp4_with_pyav(out_path, rows, cols, frames_iter, fps)
        except Exception as e2:
            print(f"Error writing MP4 (PyAV): {e2}", file=sys.stderr)
            sys.exit(1)
    except Exception as e:
        print(f"Error writing MP4: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Wrote {out_path} from {frames} frame(s) of size {rows}x{cols} at {fps} fps.")


if __name__ == "__main__":
    main()
