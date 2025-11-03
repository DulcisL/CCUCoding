#!/usr/bin/env python3
"""
stencil_2d_tester.py

A driver to iteratively test different sizes, iterations, and thread counts to ensure
the pthread (parallel) version ALWAYS matches the serial version for BOTH final and stack.

Required:
  --testing-dir TESTING_DIR
  --make MAKE           (path to make-2d; REQUIRED)
  --N1 N1 --N2 N2 --Nstep NSTEP
  --I1 I1 --I2 I2 --Istep ISTEP
  --T1 T1 --T2 T2 --Tstep TSTEP

Optional:
  --serial SERIAL       Path to serial executable (default ./code/stencil-2d)
  --pth PTH             Path to pthread executable (default ./code/pth-stencil-2d)
  --tol TOL             Absolute tolerance for float comparisons (default 0.0 for exact)
  --endian {little,big} Endianness for .dat files (default little)
  --keep                Keep passing case folders

Per-case line:
  [N= 512 I=  50 T= 11] FINAL=OK (max|Δ|=0.000e+00); STACK=OK (max|Δ|=0.000e+00)

Summary block:
  ================ SUMMARY ================
  Total cases:         144
  Final matches:       144 / 144  (100.0%)
  Stack matches:       144 / 144  (100.0%)
  Artifacts/logs dir:  ./testing_output
  CSV:                 ./testing_output/results.csv
"""

import argparse
import os
import sys
import shutil
import struct
import subprocess
from pathlib import Path
import numpy as np
import csv


# ------------------------- CLI -------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Test serial vs pthread stencil for equality across sizes/iters/threads."
    )
    # Required controls
    p.add_argument("--testing-dir", required=True, help="Directory to store per-case runs and results.csv")
    p.add_argument("--make", required=True, help="Path to make-2d executable (REQUIRED)")
    p.add_argument("--N1", type=int, required=True, help="Min matrix size (rows=cols=N)")
    p.add_argument("--N2", type=int, required=True, help="Max matrix size (inclusive)")
    p.add_argument("--Nstep", type=int, required=True, help="Step for N")
    p.add_argument("--I1", type=int, required=True, help="Min iterations")
    p.add_argument("--I2", type=int, required=True, help="Max iterations (inclusive)")
    p.add_argument("--Istep", type=int, required=True, help="Step for iterations")
    p.add_argument("--T1", type=int, required=True, help="Min thread count")
    p.add_argument("--T2", type=int, required=True, help="Max thread count (inclusive)")
    p.add_argument("--Tstep", type=int, required=True, help="Step for threads")

    # Optional paths
    p.add_argument("--serial", default="./code/stencil-2d", help="Path to serial stencil-2d")
    p.add_argument("--pth", default="./code/pth-stencil-2d", help="Path to pthread pth-stencil-2d")

    # Behavior
    p.add_argument("--tol", type=float, default=0.0, help="Absolute tolerance (default 0.0 = exact)")
    p.add_argument("--endian", choices=["little", "big"], default="little", help="Endianness for .dat files")
    p.add_argument("--keep", action="store_true", help="Keep passing case folders")

    a = p.parse_args()

    # Validate ranges
    if a.N1 < 3 or a.N2 < a.N1 or a.Nstep <= 0:
        sys.exit("Invalid N range: require N1>=3, N2>=N1, Nstep>0")
    if a.I1 < 0 or a.I2 < a.I1 or a.Istep <= 0:
        sys.exit("Invalid iteration range: require I1>=0, I2>=I1, Istep>0")
    if a.T1 < 1 or a.T2 < a.T1 or a.Tstep <= 0:
        sys.exit("Invalid thread range: require T1>=1, T2>=T1, Tstep>0")

    # Validate tool paths
    if not Path(a.make).resolve().exists():
        sys.exit(f"Error: make-2d not found: {a.make}")
    if not Path(a.serial).resolve().exists():
        sys.exit(f"Error: serial executable not found: {a.serial}")
    if not Path(a.pth).resolve().exists():
        sys.exit(f"Error: pthread executable not found: {a.pth}")

    return a


# ------------------------- I/O helpers -------------------------

def endian_tag(endian: str) -> str:
    return "<" if endian == "little" else ">"


def read_dat_matrix(path: Path, endian: str):
    """
    Read a single-frame .dat => (rows, cols, ndarray float64 native)
    """
    with open(path, "rb") as f:
        hdr = f.read(8)
        if len(hdr) != 8:
            raise RuntimeError(f"Short header in {path}")
        rows, cols = struct.unpack(endian_tag(endian) + "ii", hdr)
        if rows <= 0 or cols <= 0:
            raise RuntimeError(f"Bad dims {rows}x{cols} in {path}")
        count = rows * cols
        arr = np.fromfile(f, dtype=np.dtype(endian_tag(endian) + "f8"), count=count)
        if arr.size != count:
            raise RuntimeError(f"Unexpected data size in {path}")
        return rows, cols, arr.astype(np.float64, copy=False).reshape(rows, cols)


def read_dat_stack(path: Path, endian: str):
    """
    Read a stack .dat => (rows, cols, frames, ndarray float64 native shape (frames, rows, cols))
    """
    size = path.stat().st_size
    if size < 8:
        raise RuntimeError(f"Short header in {path}")
    with open(path, "rb") as f:
        rows, cols = struct.unpack(endian_tag(endian) + "ii", f.read(8))
    bytes_per_frame = rows * cols * 8
    data_bytes = size - 8
    if data_bytes % bytes_per_frame != 0:
        raise RuntimeError(f"Data size not multiple of frame size in {path}")
    frames = data_bytes // bytes_per_frame
    if frames < 1:
        raise RuntimeError(f"No frames in {path}")
    data = np.memmap(path, dtype=np.dtype(endian_tag(endian) + "f8"),
                     mode="r", offset=8, shape=(frames, rows, cols))
    return rows, cols, frames, np.array(data, dtype=np.float64, copy=True)


def max_abs_diff(a: np.ndarray, b: np.ndarray) -> float:
    if a.shape != b.shape:
        return float("inf")
    if a.size == 0:
        return 0.0
    return float(np.max(np.abs(a - b)))


def serial_stack_name(N: int, I: int) -> str:
    return f"all.{N}x{N}x{I}.dat"


def run_cmd(cmd, cwd: Path):
    return subprocess.run(cmd, cwd=str(cwd), text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


# ------------------------- Main testing loop -------------------------

def main():
    a = parse_args()

    testing_dir = Path(a.testing_dir).resolve()
    testing_dir.mkdir(parents=True, exist_ok=True)
    results_csv = testing_dir / "results.csv"

    serial = Path(a.serial).resolve()
    pth = Path(a.pth).resolve()
    make = Path(a.make).resolve()

    total_cases = 0
    final_ok_count = 0
    stack_ok_count = 0

    # CSV header
    with open(results_csv, "w", newline="") as fcsv:
        writer = csv.writer(fcsv)
        writer.writerow([
            "N", "I", "T",
            "final_ok", "final_max_abs_delta",
            "stack_ok", "stack_max_abs_delta",
            "serial_final", "pth_final", "serial_stack", "pth_stack"
        ])

    for N in range(a.N1, a.N2 + 1, a.Nstep):
        for I in range(a.I1, a.I2 + 1, a.Istep):
            for T in range(a.T1, a.T2 + 1, a.Tstep):
                total_cases += 1
                case_dir = testing_dir / f"N{N}_I{I}_T{T}"

                # fresh case dir
                if case_dir.exists():
                    shutil.rmtree(case_dir)
                case_dir.mkdir(parents=True, exist_ok=True)

                initial = case_dir / "initial.dat"
                serial_final = case_dir / "serial_final.dat"
                pth_final = case_dir / "pth_final.dat"
                serial_stack = case_dir / serial_stack_name(N, I)
                pth_stack = case_dir / "pth_stack.dat"

                try:
                    # 1) Call make-2d N N; copy its initial.dat into this case dir.
                    res = run_cmd([str(make), str(N), str(N)], cwd=make.parent)
                    if res.returncode != 0:
                        raise RuntimeError(f"make-2d failed:\n{res.stdout}\n{res.stderr}")

                    # Locate produced initial.dat (two common layouts)
                    candidates = [
                        make.parent.parent / "data" / "initial.dat",  # ../data/initial.dat relative to code/
                        make.parent / "initial.dat",                  # code/initial.dat
                    ]
                    src = next((c for c in candidates if c.exists()), None)
                    if not src:
                        raise RuntimeError("Could not locate initial.dat produced by make-2d.")
                    shutil.copy2(src, initial)

                    # 2) Run serial
                    res = run_cmd([str(serial), "initial.dat", "serial_final.dat", str(I)], cwd=case_dir)
                    if res.returncode != 0:
                        raise RuntimeError(f"serial failed:\n{res.stdout}\n{res.stderr}")
                    if not serial_stack.exists():
                        raise RuntimeError(f"serial stack missing: {serial_stack}")

                    # 3) Run pthread (explicit stack path)
                    res = run_cmd(
                        [str(pth),
                         "-n", str(I),
                         "-I", "initial.dat",
                         "-o", "pth_final.dat",
                         "-t", str(T),
                         "-s", "pth_stack.dat"],
                        cwd=case_dir
                    )
                    if res.returncode != 0:
                        raise RuntimeError(f"pth failed:\n{res.stdout}\n{res.stderr}")

                    # 4) Compare finals
                    _, _, A = read_dat_matrix(serial_final, a.endian)
                    _, _, B = read_dat_matrix(pth_final, a.endian)
                    final_delta = max_abs_diff(A, B)
                    final_ok = (final_delta <= a.tol)

                    # 5) Compare stacks
                    r1, c1, f1, S1 = read_dat_stack(serial_stack, a.endian)
                    r2, c2, f2, S2 = read_dat_stack(pth_stack, a.endian)
                    if (r1, c1, f1) != (r2, c2, f2):
                        stack_delta = float("inf")
                        stack_ok = False
                    else:
                        stack_delta = max_abs_diff(S1, S2)
                        stack_ok = (stack_delta <= a.tol)

                    if final_ok:
                        final_ok_count += 1
                    if stack_ok:
                        stack_ok_count += 1

                    # Per-case output (exact format)
                    print(f"[N={N:4d} I={I:3d} T={T:3d}] "
                          f"FINAL={'OK' if final_ok else 'FAIL'} (max|Δ|={final_delta:.3e}); "
                          f"STACK={'OK' if stack_ok else 'FAIL'} (max|Δ|={stack_delta:.3e})")

                    # CSV row
                    with open(results_csv, "a", newline="") as fcsv:
                        writer = csv.writer(fcsv)
                        writer.writerow([N, I, T, int(final_ok), f"{final_delta:.17e}",
                                         int(stack_ok), f"{stack_delta:.17e}",
                                         str(serial_final), str(pth_final),
                                         str(serial_stack), str(pth_stack)])

                    # Cleanup passing cases if not keeping
                    if final_ok and stack_ok and not a.keep:
                        shutil.rmtree(case_dir)

                except Exception as e:
                    print(f"[N={N:4d} I={I:3d} T={T:3d}] FINAL=FAIL; STACK=FAIL  (error: {e})", file=sys.stderr)
                    with open(results_csv, "a", newline="") as fcsv:
                        writer = csv.writer(fcsv)
                        writer.writerow([N, I, T, 0, "nan", 0, "nan",
                                         str(serial_final), str(pth_final),
                                         str(serial_stack), str(pth_stack)])
                    # keep directory for debugging

    # Summary
    pct_final = 100.0 * (final_ok_count / total_cases) if total_cases else 0.0
    pct_stack = 100.0 * (stack_ok_count / total_cases) if total_cases else 0.0
    print("\n================ SUMMARY ================")
    print(f"Total cases:         {total_cases}")
    print(f"Final matches:       {final_ok_count} / {total_cases}  ({pct_final:.1f}%)")
    print(f"Stack matches:       {stack_ok_count} / {total_cases}  ({pct_stack:.1f}%)")
    print(f"Artifacts/logs dir:  {testing_dir}")
    print(f"CSV:                 {results_csv}")


if __name__ == "__main__":
    main()
