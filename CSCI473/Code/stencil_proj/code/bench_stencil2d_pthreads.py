#!/usr/bin/env python3
"""
bench_stencil2d_pthreads.py

Benchmark driver + plotter to collect timing information and generate
timing-derived plots (speedup, efficiency, iso-efficiency) as a function of:
  - SIZE (N), NUM_THREADS (T), and NUM_ITERATIONS (I).

Behavior:
  - Uses your make-2d to create initial.dat for each N
  - Runs serial (stencil-2d) and pthread (pth-stencil-2d)
  - Measures wall time (best of --reps runs after --warmup)
  - Writes CSV: bench_results.csv in --testing-dir
  - Generates plots into --testing-dir/plots:
        For each thread count T:
          T<T>_speedup_vs_size.png
          T<T>_efficiency_vs_size.png
          T<T>_iso_efficiency.png

Global timeout:
  - If total runtime exceeds 26 minutes, it stops, writes CSV, generates plots
    from the partial results collected so far, and exits cleanly.

Required:
  --testing-dir TESTING_DIR
  --make MAKE
  --N1 N1 --N2 N2 --Nstep NSTEP
  --I1 I1 --I2 I2 --Istep ISTEP
  --T1 T1 --T2 T2 --Tstep TSTEP

Optional:
  --serial SERIAL   (default ./code/stencil-2d)
  --pth PTH         (default ./code/pth-stencil-2d)
  --reps REPS       (default 3)
  --warmup WARMUP   (default 1)
  --keep            (keep per-case directories)
"""

import argparse
import sys
import shutil
import time
import subprocess
from pathlib import Path
import csv
from collections import defaultdict

# Headless plotting
import matplotlib
matplotlib.use("Agg", force=True)
import matplotlib.pyplot as plt

MAX_RUNTIME_SECS = 26 * 60  # 26 minutes


# ------------------------- CLI -------------------------

def parse_args():
    p = argparse.ArgumentParser(
        description="Benchmark serial vs pthread stencil across N, I, T; collect CSV + per-thread plots."
    )
    # Required ranges
    p.add_argument("--testing-dir", required=True, help="Output directory for runs, CSV, and plots")
    p.add_argument("--make", required=True, help="Path to make-2d executable")
    p.add_argument("--N1", type=int, required=True)
    p.add_argument("--N2", type=int, required=True)
    p.add_argument("--Nstep", type=int, required=True)
    p.add_argument("--I1", type=int, required=True)
    p.add_argument("--I2", type=int, required=True)
    p.add_argument("--Istep", type=int, required=True)
    p.add_argument("--T1", type=int, required=True)
    p.add_argument("--T2", type=int, required=True)
    p.add_argument("--Tstep", type=int, required=True)

    # Optional tools & knobs
    p.add_argument("--serial", default="./code/stencil-2d", help="Path to serial executable")
    p.add_argument("--pth", default="./code/pth-stencil-2d", help="Path to pthread executable")
    p.add_argument("--reps", type=int, default=3, help="Timed repetitions (best-of)")
    p.add_argument("--warmup", type=int, default=1, help="Warmup runs (not timed)")
    p.add_argument("--keep", action="store_true", help="Keep per-case directories")

    a = p.parse_args()

    # Validations
    if a.N1 < 3 or a.N2 < a.N1 or a.Nstep <= 0:
        sys.exit("Invalid N range")
    if a.I1 < 0 or a.I2 < a.I1 or a.Istep <= 0:
        sys.exit("Invalid I range")
    if a.T1 < 1 or a.T2 < a.T1 or a.Tstep <= 0:
        sys.exit("Invalid T range")
    if a.reps < 1 or a.warmup < 0:
        sys.exit("Invalid reps/warmup")

    for path, label in [(a.make, "make-2d"), (a.serial, "serial"), (a.pth, "pth")]:
        if not Path(path).resolve().exists():
            sys.exit(f"Error: {label} not found: {path}")

    return a


# ------------------------- helpers -------------------------

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)


def run_cmd(cmd, cwd: Path):
    res = subprocess.run(cmd, cwd=str(cwd), text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return res.returncode, res.stdout, res.stderr


def time_cmd(cmd, cwd: Path, warmup: int, reps: int):
    # Warmups (untimed)
    for _ in range(warmup):
        subprocess.run(cmd, cwd=str(cwd),
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Timed reps
    times = []
    last = (0, "", "")
    for _ in range(reps):
        t0 = time.perf_counter()
        r = subprocess.run(cmd, cwd=str(cwd), text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        dt = time.perf_counter() - t0
        times.append(dt)
        last = (r.returncode, r.stdout, r.stderr)
    best = min(times) if times else float("inf")
    return best, times, last


def locate_make2d_initial(make_path: Path) -> Path:
    # Typical locations:
    candidates = [
        make_path.parent.parent / "data" / "initial.dat",  # ../data/initial.dat
        make_path.parent / "initial.dat",                  # code/initial.dat
    ]
    for c in candidates:
        if c.exists():
            return c
    return None


def serial_stack_name(N: int, I: int) -> str:
    return f"all.{N}x{N}x{I}.dat"


def save_line(x, ys, labels, title, xlabel, ylabel, out_path, ylimit=None):
    plt.figure(figsize=(7, 4))
    for y, lab in zip(ys, labels):
        plt.plot(x, y, marker="o", label=lab)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if ylimit is not None:
        plt.ylim(0, ylimit)
    plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
    if any(labels):
        plt.legend()
    plt.tight_layout()
    plt.savefig(out_path)
    plt.close()


# ------------------------- plotting from records -------------------------

def generate_plots_from_records(records, plots_dir: Path):
    """
    records: list of dicts:
      {'N':N, 'I':I, 'T':T, 'Ts':Ts_best, 'Tp':Tp_best, 'speed':speed, 'eff':eff}
    For each T, make:
      - speedup vs N (one line per I)
      - efficiency vs N (one line per I)
      - iso-efficiency: minimal N vs I for efficiency targets {0.5, 0.7, 0.9}
    """
    ensure_dir(plots_dir)
    if not records:
        print("No records to plot.")
        return

    all_T = sorted({r["T"] for r in records})
    all_speed = [r["speed"] for r in records if r["speed"] < float("inf")]
    all_eff = [r["eff"] for r in records if r["eff"] < float("inf")]
    global_speed_max = max(all_speed) if all_speed else 1.0
    global_eff_max = max(all_eff) if all_eff else 1.0
    # Make them look a bit nicer
    global_speed_max *= 1.05
    global_eff_max = max(1.0, global_eff_max * 1.05)

    # For iso-eff, we'll bound N
    global_N_max = max(r["N"] for r in records)

    # Build index: per T
    for T in all_T:
        # Group by I, then by N
        speed_by_I = defaultdict(list)  # I -> list of (N, speed)
        eff_by_I   = defaultdict(list)  # I -> list of (N, eff)
        eff_map_NI = defaultdict(dict)  # I -> {N: eff} for iso-eff

        for r in records:
            if r["T"] != T:
                continue
            N = r["N"]
            I = r["I"]
            speed = r["speed"]
            eff = r["eff"]
            speed_by_I[I].append((N, speed))
            eff_by_I[I].append((N, eff))
            eff_map_NI[I][N] = eff

        # ---- Speedup vs N (per T) ----
        if speed_by_I:
            xs = []
            ys = []
            labels = []
            for I in sorted(speed_by_I.keys()):
                pairs = speed_by_I[I]
                pairs.sort(key=lambda x: x[0])  # sort by N
                Ns = [n for n, _ in pairs]
                speeds = [s for _, s in pairs]
                xs.append(Ns)
                ys.append(speeds)
                labels.append(f"I={I}")
            # For consistent x axis, we just plot separate lines with their own Ns
            # using the first Ns array as x in save_line; so we call save_line per T
            # but inside we actually do manual plotting:
            plt.figure(figsize=(7, 4))
            for I in sorted(speed_by_I.keys()):
                pairs = sorted(speed_by_I[I], key=lambda x: x[0])
                Ns = [n for n, _ in pairs]
                speeds = [s for _, s in pairs]
                plt.plot(Ns, speeds, marker="o", label=f"I={I}")
            plt.title(f"Speedup vs Size (T={T})")
            plt.xlabel("Problem size N")
            plt.ylabel("Speedup (Ts/Tp)")
            plt.ylim(0, global_speed_max)
            plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
            plt.legend()
            plt.tight_layout()
            out_path = plots_dir / f"T{T}_speedup_vs_size.png"
            plt.savefig(out_path)
            plt.close()

        # ---- Efficiency vs N (per T) ----
        if eff_by_I:
            plt.figure(figsize=(7, 4))
            for I in sorted(eff_by_I.keys()):
                pairs = sorted(eff_by_I[I], key=lambda x: x[0])
                Ns = [n for n, _ in pairs]
                effs = [e for _, e in pairs]
                plt.plot(Ns, effs, marker="o", label=f"I={I}")
            plt.title(f"Efficiency vs Size (T={T})")
            plt.xlabel("Problem size N")
            plt.ylabel("Efficiency = Speedup / T")
            plt.ylim(0, global_eff_max)
            plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
            plt.legend()
            plt.tight_layout()
            out_path = plots_dir / f"T{T}_efficiency_vs_size.png"
            plt.savefig(out_path)
            plt.close()

        # ---- Iso-efficiency (per T): minimal N vs I for fixed efficiency targets ----
        iso_targets = [0.5, 0.7, 0.9]
        # For each target, for each I, choose minimal N such that eff >= target
        I_values = sorted(eff_map_NI.keys())
        if I_values:
            plt.figure(figsize=(7, 4))
            for target in iso_targets:
                xs_I = []
                ys_N = []
                for I in I_values:
                    effs_for_I = eff_map_NI[I]  # dict N->eff
                    feasible_N = [n for n, e in effs_for_I.items() if e >= target]
                    if feasible_N:
                        xs_I.append(I)
                        ys_N.append(min(feasible_N))
                if xs_I:
                    plt.plot(xs_I, ys_N, marker="o", label=f"target eff={target:.1f}")
            plt.title(f"Iso-efficiency (T={T})\nMinimal N vs Iterations for efficiency targets")
            plt.xlabel("Iterations I")
            plt.ylabel("Minimal N achieving target efficiency")
            plt.ylim(0, global_N_max * 1.05)
            plt.grid(True, linestyle="--", linewidth=0.6, alpha=0.7)
            plt.legend()
            plt.tight_layout()
            out_path = plots_dir / f"T{T}_iso_efficiency.png"
            plt.savefig(out_path)
            plt.close()


# ------------------------- main -------------------------

def main():
    a = parse_args()

    testing_dir = Path(a.testing_dir).resolve()
    ensure_dir(testing_dir)
    plots_dir = testing_dir / "plots"
    ensure_dir(plots_dir)

    serial = Path(a.serial).resolve()
    pth = Path(a.pth).resolve()
    make = Path(a.make).resolve()
    results_csv = testing_dir / "bench_results.csv"

    # CSV header
    with open(results_csv, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([
            "N", "I", "T",
            "serial_time_s", "pth_time_s",
            "speedup", "efficiency",
            "serial_times_all", "pth_times_all",
            "serial_cmd", "pth_cmd",
            "case_dir",
        ])

    records = []  # in-memory for plotting
    total_cases = 0
    start_time = time.perf_counter()

    def maybe_timeout_and_finish():
        elapsed = time.perf_counter() - start_time
        if elapsed > MAX_RUNTIME_SECS:
            print("\n⚠️  Global timeout reached (26 minutes).")
            print(f"Elapsed: {elapsed/60:.1f} minutes. Saving partial CSV and plots...")
            generate_plots_from_records(records, plots_dir)
            print(f"Partial CSV:   {results_csv}")
            print(f"Partial plots: {plots_dir}")
            sys.exit(0)

    for N in range(a.N1, a.N2 + 1, a.Nstep):
        for I in range(a.I1, a.I2 + 1, a.Istep):
            for T in range(a.T1, a.T2 + 1, a.Tstep):
                total_cases += 1
                case_dir = testing_dir / f"N{N}_I{I}_T{T}"
                if case_dir.exists():
                    shutil.rmtree(case_dir)
                ensure_dir(case_dir)

                initial = case_dir / "initial.dat"
                serial_final = case_dir / "serial_final.dat"
                pth_final = case_dir / "pth_final.dat"
                serial_stack = case_dir / serial_stack_name(N, I)
                pth_stack = case_dir / "pth_stack.dat"

                # 1) make-2d N N -> initial.dat
                rc, out, err = run_cmd([str(make), str(N), str(N)], cwd=make.parent)
                if rc != 0:
                    print(err, file=sys.stderr)
                    sys.exit(f"make-2d failed:\n{out}\n{err}")
                src_initial = locate_make2d_initial(make)
                if not src_initial:
                    sys.exit("Could not locate initial.dat created by make-2d.")
                shutil.copy2(src_initial, initial)

                # 2) serial
                serial_cmd = [str(serial), "initial.dat", "serial_final.dat", str(I)]
                Ts_best, Ts_all, (rc_s, so_s, se_s) = time_cmd(serial_cmd, case_dir, a.warmup, a.reps)
                if rc_s != 0:
                    print(se_s, file=sys.stderr)
                    sys.exit(f"serial failed:\n{so_s}\n{se_s}")
                if not serial_stack.exists():
                    sys.exit(f"serial stack missing: {serial_stack}")

                # 3) pthread
                pth_cmd = [str(pth),
                           "-n", str(I),
                           "-I", "initial.dat",
                           "-o", "pth_final.dat",
                           "-t", str(T),
                           "-s", "pth_stack.dat"]
                Tp_best, Tp_all, (rc_p, so_p, se_p) = time_cmd(pth_cmd, case_dir, a.warmup, a.reps)
                if rc_p != 0:
                    print(se_p, file=sys.stderr)
                    sys.exit(f"pth failed:\n{so_p}\n{se_p}")

                # 4) metrics
                speed = Ts_best / Tp_best if Tp_best > 0 else float("inf")
                eff = speed / T

                # 5) write CSV row
                with open(results_csv, "a", newline="") as f:
                    writer = csv.writer(f)
                    writer.writerow([
                        N, I, T,
                        f"{Ts_best:.9f}", f"{Tp_best:.9f}",
                        f"{speed:.6f}", f"{eff:.6f}",
                        ";".join(f"{x:.9f}" for x in Ts_all),
                        ";".join(f"{x:.9f}" for x in Tp_all),
                        " ".join(serial_cmd),
                        " ".join(pth_cmd),
                        str(case_dir),
                    ])

                print(f"[N={N:4d} I={I:3d} T={T:3d}] "
                      f"Ts={Ts_best:.4f}s Tp={Tp_best:.4f}s S={speed:.3f} E={eff:.3f}")

                # 6) record for plotting
                records.append({
                    "N": N,
                    "I": I,
                    "T": T,
                    "Ts": Ts_best,
                    "Tp": Tp_best,
                    "speed": speed,
                    "eff": eff,
                })

                # 7) cleanup per-case unless keep
                if not a.keep:
                    shutil.rmtree(case_dir)

                # 8) timeout check
                maybe_timeout_and_finish()

    # All done within time: generate plots
    generate_plots_from_records(records, plots_dir)

    print("\nBenchmark complete.")
    print(f"Total cases: {total_cases}")
    print(f"CSV:   {results_csv}")
    print(f"Plots: {plots_dir}")


if __name__ == "__main__":
    main()
