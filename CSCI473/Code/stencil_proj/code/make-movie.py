#!/usr/bin/env python3
# make-movie.py
# Convert a stacked .dat (header + frames) to an MP4 in the same directory.
# - Default FPS = 1
# - Strict 0->blue, 1->red colormap
# - Borders: top/bottom = blue, left/right = red
# - Nearest-neighbor upscaling so min dimension >= 480px (even W/H for yuv420p)

import argparse
import os
import sys
import struct
import numpy as np

try:
    from matplotlib.colors import Normalize, LinearSegmentedColormap
except Exception:
    print("Error: matplotlib is required (pip install matplotlib).", file=sys.stderr)
    sys.exit(1)

try:
    import av  # PyAV
except Exception:
    print("Error: PyAV is required (pip install av).", file=sys.stderr)
    sys.exit(1)


def parse_args():
    p = argparse.ArgumentParser(
        description="Convert a stacked .dat (header + frames) to MP4. "
                    "Defaults to 1 FPS, draws colored borders, and upscales to >=480p."
    )
    p.add_argument("stack_path", nargs="?", help="Path to stacked .dat (e.g., ./data/all.100x100x500.dat)")
    p.add_argument("--fps", type=int, default=1, help="Frames per second (default: 1)")
    p.add_argument("--vmin", type=float, default=0.0, help="Min value mapped to blue (default: 0.0)")
    p.add_argument("--vmax", type=float, default=1.0, help="Max value mapped to red (default: 1.0)")
    p.add_argument("--out", dest="out_mp4", help="Output MP4 path (must end with .mp4). Default: <stack_basename>.mp4")
    a = p.parse_args()

    if not a.stack_path:
        p.print_help(); sys.exit(1)

    in_path = os.path.abspath(os.path.expanduser(a.stack_path))
    if not os.path.isfile(in_path):
        print(f"Error: not found: {in_path}", file=sys.stderr); sys.exit(1)

    if a.out_mp4:
        out_path = os.path.abspath(os.path.expanduser(a.out_mp4))
        if not out_path.lower().endswith(".mp4"):
            print("Error: --out must end with .mp4", file=sys.stderr); sys.exit(1)
    else:
        base, _ = os.path.splitext(in_path)
        out_path = base + ".mp4"

    return in_path, out_path, a.fps, a.vmin, a.vmax


def read_header_and_shape(in_path):
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
        raise RuntimeError("Data size not a multiple of frame size (rows*cols*sizeof(double))")

    frames = data_bytes // bytes_per_frame
    if frames < 1:
        raise RuntimeError("No frames found in stack")
    return rows, cols, frames


def nearest_neighbor_upscale(rgb, scale):
    if scale <= 1:
        return np.ascontiguousarray(rgb)
    return np.ascontiguousarray(np.repeat(np.repeat(rgb, scale, axis=0), scale, axis=1))


def ensure_even_dimensions(rgb):
    """Pad by replicating the outermost row/col so border color stays consistent."""
    h, w, _ = rgb.shape
    pad_h = 1 if (h % 2) else 0
    pad_w = 1 if (w % 2) else 0
    if not pad_h and not pad_w:
        return rgb

    if pad_h:
        last_row = rgb[-1:, :, :]  # replicate bottom row (which already has correct border color)
        rgb = np.concatenate([rgb, last_row], axis=0)
        h += 1
    if pad_w:
        last_col = rgb[:, -1:, :]  # replicate rightmost col (already correct border color)
        rgb = np.concatenate([rgb, last_col], axis=1)
    return np.ascontiguousarray(rgb)


def frame_generator(in_path, rows, cols, frames, vmin, vmax, scale):
    """
    Yield contiguous RGB uint8 frames:
      - Strict linear 0->blue, 1->red map
      - Borders: top/bottom blue, left/right red
      - Nearest-neighbor upscale by integer 'scale'
      - Ensure even dimensions (yuv420p requirement)
    """
    mmap = np.memmap(in_path, dtype="<f8", mode="r", offset=8, shape=(frames, rows, cols))
    cmap = LinearSegmentedColormap.from_list("blue_red", ["#0000FF", "#FF0000"], N=256)
    norm = Normalize(vmin=vmin, vmax=vmax, clip=True)

    # Exact RGB triplets
    BLUE = np.array([0, 0, 255], dtype=np.uint8)
    RED  = np.array([255, 0, 0], dtype=np.uint8)

    for t in range(frames):
        rgba = cmap(norm(mmap[t]))                     # (rows, cols, 4), float64 in [0,1]
        rgb  = (rgba[..., :3] * 255).astype(np.uint8)  # (rows, cols, 3), uint8

        # Color the borders explicitly:
        # top/bottom rows = blue, left/right cols = red
        rgb[0, :, :]  = BLUE
        rgb[-1, :, :] = BLUE
        rgb[:, 0, :]  = RED
        rgb[:, -1, :] = RED

        # Upscale then fix even dims
        rgb_up = nearest_neighbor_upscale(rgb, scale)
        rgb_up = ensure_even_dimensions(rgb_up)

        yield rgb_up


def write_mp4_pyav(out_path, frames_iter_factory, fps):
    """
    Write MP4 via PyAV (yuv420p). Try libx264 then mpeg4. Frames come pre-sized.
    """
    os.makedirs(os.path.dirname(out_path) or ".", exist_ok=True)

    for codec in ("libx264", "mpeg4"):
        try:
            container = av.open(out_path, mode="w")
            stream = container.add_stream(codec, rate=fps)
            stream.pix_fmt = "yuv420p"

            it = frames_iter_factory()
            first = next(it)
            tgt_h, tgt_w = first.shape[0], first.shape[1]

            frame = av.VideoFrame.from_ndarray(first, format="rgb24")
            frame = frame.reformat(width=tgt_w, height=tgt_h, format=stream.pix_fmt)
            packet = stream.encode(frame)
            if packet: container.mux(packet)

            for rgb in it:
                frame = av.VideoFrame.from_ndarray(rgb, format="rgb24")
                frame = frame.reformat(width=tgt_w, height=tgt_h, format=stream.pix_fmt)
                packet = stream.encode(frame)
                if packet: container.mux(packet)

            packet = stream.encode(None)
            if packet: container.mux(packet)
            container.close()
            return  # success

        except StopIteration:
            try: container.close()
            except Exception: pass
            raise RuntimeError("No frames to write.")
        except av.AVError:
            try: container.close()
            except Exception: pass
            continue
        except Exception:
            try: container.close()
            except Exception: pass
            raise

    raise RuntimeError("Failed to write MP4 with available codecs (libx264, mpeg4).")


def main():
    in_path, out_path, fps, vmin, vmax = parse_args()

    try:
        rows, cols, frames = read_header_and_shape(in_path)
    except Exception as e:
        print(f"Error reading stack: {e}", file=sys.stderr); sys.exit(1)

    # Integer scale so the smaller dimension is at least 480 pixels
    min_dim = min(rows, cols)
    scale = int(np.ceil(480 / max(1, min_dim)))
    if scale < 1:
        scale = 1

    print(f"Processing {frames} frames from {rows}x{cols} at {fps} FPS; integer scale={scale} "
          f"-> min dimension >= 480px.")

    def frames_iter_factory():
        return frame_generator(in_path, rows, cols, frames, vmin, vmax, scale)

    try:
        write_mp4_pyav(out_path, frames_iter_factory, fps)
    except Exception as e:
        print(f"Error writing MP4: {e}", file=sys.stderr); sys.exit(1)

    print(f"✅ Saved MP4: {out_path}")
    print(f"   FPS: {fps}, Frames: {frames}, Source: {rows}x{cols}, Scale: x{scale}")


if __name__ == "__main__":
    main()
