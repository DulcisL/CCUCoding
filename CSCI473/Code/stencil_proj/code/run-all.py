#!/usr/bin/env python3
# Usage:
#   python3 code/run-all.py <rows> <cols> <iterations> [initialName.dat] [finalName.dat] [stackFinal.dat]

import os, sys, struct, subprocess

def usage_and_exit():
    print("Usage:")
    print("  python3 code/run-all.py <rows> <cols> <iterations> [initialName.dat] [finalName.dat] [stackFinal.dat]")
    print("\nExamples:")
    print("  python3 code/run-all.py 100 100 500")
    print("  python3 code/run-all.py 200 300 50 myInit.dat myFinal.dat stack_200x300x50.dat")
    sys.exit(1)

def need_exec(path):
    if not (os.path.isfile(path) and os.access(path, os.X_OK)):
        print(f"Missing executable: {path}", file=sys.stderr); sys.exit(1)

def run_or_die(cmd, cwd):
    try:
        return subprocess.run(cmd, cwd=cwd, check=True, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {' '.join(cmd)}", file=sys.stderr)
        if e.stdout: print("stdout:\n" + e.stdout, file=sys.stderr)
        if e.stderr: print("stderr:\n" + e.stderr, file=sys.stderr)
        sys.exit(1)

def main():
    argv = sys.argv[1:]
    if len(argv) < 3: usage_and_exit()

    try:
        rows = int(argv[0]); cols = int(argv[1]); iterations = int(argv[2])
    except ValueError:
        usage_and_exit()
    if rows < 3 or cols < 3 or iterations < 0:
        print("Error: rows and cols must be >= 3, iterations >= 0", file=sys.stderr); usage_and_exit()

    initial_name = argv[3] if len(argv) >= 4 else "initial.dat"
    final_name   = argv[4] if len(argv) >= 5 else "final.dat"
    stack_name   = argv[5] if len(argv) >= 6 else f"all.{rows}x{cols}x{iterations}.dat"

    code_dir = os.path.abspath(os.path.dirname(__file__))               # ./code
    data_dir = os.path.abspath(os.path.join(code_dir, "..", "data"))    # ./data
    os.makedirs(data_dir, exist_ok=True)

    make2d = os.path.join(code_dir, "make-2d")
    stencil2d = os.path.join(code_dir, "stencil-2d")
    need_exec(make2d); need_exec(stencil2d)

    print(f"-> make-2d {rows} {cols} (cwd=code)")
    run_or_die([make2d, str(rows), str(cols)], cwd=code_dir)

    created_initial_path = os.path.join(data_dir, "initial.dat")
    if not os.path.isfile(created_initial_path):
        print(f"Error: expected file not created: {created_initial_path}", file=sys.stderr)
        sys.exit(1)

    desired_initial_path = os.path.join(data_dir, initial_name)
    if os.path.abspath(desired_initial_path) != os.path.abspath(created_initial_path):
        os.replace(created_initial_path, desired_initial_path)
        print(f"Renamed initial.dat -> {initial_name}")
    else:
        print(f"Initial file: {initial_name}")

    print(f"-> stencil-2d iterations={iterations} (cwd=data)")
    run_or_die([stencil2d, initial_name, final_name, str(iterations)], cwd=data_dir)

    final_path = os.path.join(data_dir, final_name)
    if not os.path.isfile(final_path):
        print(f"Error: expected final file not found: {final_path}", file=sys.stderr)
        sys.exit(1)

    default_stack = f"all.{rows}x{cols}x{iterations}.dat"
    default_stack_path = os.path.join(data_dir, default_stack)
    if not os.path.isfile(default_stack_path):
        print(f"Error: expected stack file not found: {default_stack_path}", file=sys.stderr)
        sys.exit(1)

    desired_stack_path = os.path.join(data_dir, stack_name)
    if os.path.abspath(desired_stack_path) != os.path.abspath(default_stack_path):
        os.replace(default_stack_path, desired_stack_path)
        print(f"Renamed {default_stack} -> {stack_name}")
    else:
        print(f"Stack file: {stack_name}")

    try:
        with open(desired_stack_path, "rb") as f:
            hdr = f.read(8)
            if len(hdr) != 8: raise RuntimeError("Stack header too small")
            r, c = struct.unpack("<ii", hdr)
            if r != rows or c != cols:
                raise RuntimeError(f"Header dims {r}x{c} != expected {rows}x{cols}")
    except Exception as e:
        print(f"Warning: could not verify stack header: {e}", file=sys.stderr)

    print("Done.")
    print(f"  Initial: {initial_name}")
    print(f"  Final:   {final_name}")
    print(f"  Stack:   {stack_name}")

if __name__ == "__main__":
    main()
