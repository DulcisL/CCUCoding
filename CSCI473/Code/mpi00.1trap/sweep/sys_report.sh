#!/usr/bin/env bash
set -euo pipefail
shopt -s nullglob  # make /dev globs expand to empty if nothing matches

# -------------------------- helpers --------------------------
have() { command -v "$1" >/dev/null 2>&1; }
section() { echo -e "\n================================================================================"; echo "## $1"; echo "================================================================================"; }
sub() { echo -e "\n--- $1 ---"; }
pkg_hint() {
  local pkg="$1"
  if   have apt;    then echo "  sudo apt update && sudo apt install -y $pkg"
  elif have dnf;    then echo "  sudo dnf install -y $pkg"
  elif have pacman; then echo "  sudo pacman -S --needed $pkg"
  elif have zypper; then echo "  sudo zypper install -y $pkg"
  elif have brew;   then echo "  brew install $pkg"
  else                   echo "  Install '$pkg' via your package manager"
  fi
}

# -------------------------- args/output -----------------------
BENCH=0           # enable quick benches
FIO_BENCH=0       # include quick disk I/O bench
DURATION=10       # seconds for benches
OUTFILE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --bench) BENCH=1; shift ;;
    --fio) FIO_BENCH=1; BENCH=1; shift ;;
    --duration) DURATION="${2:-10}"; shift 2 ;;
    --outfile) OUTFILE="${2:-}"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--bench] [--fio] [--duration SEC] [--outfile FILE]"
      exit 0 ;;
    *) echo "Unknown arg: $1" >&2; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTFILE="${OUTFILE:-$SCRIPT_DIR/system_hardware_report.txt}"
: > "$OUTFILE"

MISSING=()

# -------------------------- OS & user -------------------------
{
  section "OS & User"
  echo "Generated: $(date -Is)"
  echo "Host:      $(hostname)"
  echo "User:      ${USER:-unknown}"
  sub "Kernel/Arch"
  uname -a
  sub "Distro"
  if [[ -r /etc/os-release ]]; then cat /etc/os-release; else echo "Unknown"; fi
} >> "$OUTFILE"

# ------------------ virtualization / WSL ----------------------
{
  section "Virtualization / WSL"
  if grep -qi microsoft /proc/version 2>/dev/null; then
    echo "WSL detected. NOTE: hardware details (cache/DIMM/storage FW) may be virtualized."
  else
    echo "WSL not detected."
  fi
  if have systemd-detect-virt; then
    sub "systemd-detect-virt"; systemd-detect-virt || true
  else
    echo "Tip: install systemd (systemd-detect-virt) for virt details."
    MISSING+=("systemd")
  fi
} >> "$OUTFILE"

# --------------- CPU / cores / types / speed / caches ---------
{
  section "CPU / Cores / Types / Speed / Caches"

  if have lscpu; then
    sub "lscpu"; lscpu
    sub "lscpu (cache summary)"; lscpu -C || true
  else
    echo "lscpu not found. $(pkg_hint util-linux)"
    MISSING+=("util-linux")
  fi

  sub "/proc/cpuinfo: model + sample MHz"
  grep -m1 "model name" /proc/cpuinfo || echo "N/A"
  grep -m8 -E "cpu MHz" /proc/cpuinfo || true

  sub "Core types (if exposed; 1=Performance, 2=Efficiency)"
  core_types_found=0
  for f in /sys/devices/system/cpu/cpu[0-9]*/topology/core_type; do
    [[ -f "$f" ]] || continue
    cpu=$(sed -E 's/.*cpu([0-9]+).*/\1/' <<<"$f")
    echo "cpu$cpu: $(cat "$f")"
    core_types_found=1
  done
  [[ $core_types_found -eq 0 ]] && echo "Core types not exposed on this kernel/CPU."

  sub "Cache hierarchy (cpu0 via sysfs)"
  if [[ -d /sys/devices/system/cpu/cpu0/cache ]]; then
    for idx in /sys/devices/system/cpu/cpu0/cache/index*; do
      [[ -d "$idx" ]] || continue
      lvl=$(<"$idx/level")
      typ=$(<"$idx/type")
      siz=$(<"$idx/size")
      way=$(<"$idx/ways_of_associativity" 2>/dev/null || echo "?")
      sets=$(<"$idx/number_of_sets" 2>/dev/null || echo "?")
      echo "L$lvl $typ: size=$siz, ways=$way, sets=$sets"
    done
  else
    echo "Cache sysfs not present."
  fi

  if have numactl; then
    sub "numactl --hardware"; numactl --hardware || true
  else
    echo "Tip: install numactl for NUMA details. $(pkg_hint numactl)"
    MISSING+=("numactl")
  fi
} >> "$OUTFILE"

# -------------------------- memory ----------------------------
{
  section "Memory (RAM)"
  sub "free -h"; (have free && free -h) || echo "free not found"
  sub "/proc/meminfo (key lines)"
  grep -E "MemTotal|MemAvailable|SwapTotal|SwapFree" /proc/meminfo

  if have dmidecode; then
    if [[ $EUID -eq 0 ]]; then
      sub "dmidecode -t memory (DIMMs, type/speed)"; dmidecode -t memory || true
    else
      echo "Run with sudo for DIMM details: sudo dmidecode -t memory"
    fi
  else
    echo "Tip: install dmidecode for DIMM type/speed. $(pkg_hint dmidecode)"
    MISSING+=("dmidecode")
  fi
} >> "$OUTFILE"

# -------------------------- storage ---------------------------
{
  section "Storage"
  if have lsblk; then
    sub "lsblk (model, size, SSD/HDD, bus, fs, mount)"
    lsblk -o NAME,MODEL,TYPE,SIZE,ROTA,TRAN,FSTYPE,MOUNTPOINT
    sub "lsblk -D (discard/TRIM)"; lsblk -D || true
    sub "lsblk -t (topology)"; lsblk -t || true
  else
    echo "lsblk not found. $(pkg_hint util-linux)"
    MISSING+=("util-linux")
  fi

  sub "df -hT (mounted filesystems)"; df -hT || true

  if have nvme; then
    sub "nvme list (model+firmware)"; nvme list || true
  else
    echo "Tip: install nvme-cli for NVMe firmware info. $(pkg_hint nvme-cli)"
    MISSING+=("nvme-cli")
  fi

  if have smartctl; then
    # NOTE: redirection moved AFTER the loop (not in the for-list) to avoid syntax errors
    sub "smartctl -i (SATA/SAS/NVMe devices)"
    DEVICES=(/dev/sd? /dev/nvme?n?)
    for dev in "${DEVICES[@]}"; do
      [[ -e "$dev" ]] || continue
      echo "# $dev"
      smartctl -i "$dev" 2>/dev/null || true
    done
  else
    echo "Tip: install smartmontools for SATA/SAS firmware/version. $(pkg_hint smartmontools)"
    MISSING+=("smartmontools")
  fi

  sub "/sys/block/*/queue/rotational (0=SSD, 1=HDD)"
  for rot in /sys/block/*/queue/rotational; do
    [[ -e "$rot" ]] || continue
    echo "$rot: $(<"$rot")"
  done
} >> "$OUTFILE"

# ----------------------- benchmarks ---------------------------
{
  section "Benchmarks (quick)"
  echo "These are quick sanity checks and depend on load/environment."
  echo

  if have stress-ng; then
    sub "CPU compute: stress-ng --matrix 0 --metrics-brief --timeout ${DURATION}s"
    stress-ng --matrix 0 --metrics-brief --timeout "${DURATION}s" 2>&1 || true
  elif have sysbench; then
    sub "CPU compute proxy: sysbench cpu --time=${DURATION}"
    sysbench cpu --time="${DURATION}" run 2>&1 || true
  else
    echo "CPU compute test skipped. Install one of:"
    echo " - stress-ng: $(pkg_hint stress-ng)"
    echo " - sysbench:  $(pkg_hint sysbench)"
    MISSING+=("stress-ng" "sysbench")
  fi

  if have sysbench; then
    sub "Memory throughput: sysbench memory --time=${DURATION}"
    sysbench memory --time="${DURATION}" run 2>&1 || true
  elif have mbw; then
    sub "Memory bandwidth: mbw 256"
    mbw 256 2>&1 || true
  else
    echo "Memory throughput test skipped. Install one of:"
    echo " - sysbench: $(pkg_hint sysbench)"
    echo " - mbw:      $(pkg_hint mbw)"
    MISSING+=("sysbench" "mbw")
  fi

  if have lat_mem_rd; then
    sub "Memory latency: lat_mem_rd 128M stride 128"
    lat_mem_rd 128M 128 2>&1 || true
  else
    echo "Memory latency test skipped. Install lmbench (lat_mem_rd):"
    echo "$(pkg_hint lmbench)"
    MISSING+=("lmbench")
  fi

  # Optional disk I/O bench toggleable with --fio (safe default off)
  if [[ $FIO_BENCH -eq 1 ]]; then
    if have fio; then
      sub "Disk I/O: fio quick randrw (256MB, ${DURATION}s)"
      fio --name=quicktest --filename="$SCRIPT_DIR/.fio-testfile" \
          --size=256M --rw=randrw --rwmixread=70 \
          --iodepth=16 --numjobs=2 --time_based --runtime="$DURATION" \
          --group_reporting 2>&1 || true
      rm -f "$SCRIPT_DIR/.fio-testfile"
    else
      echo "fio not found. $(pkg_hint fio)"
      MISSING+=("fio")
    fi
  fi
} >> "$OUTFILE"

# --------------------------- GPU ------------------------------
{
  section "GPU"
  if have lspci; then
    sub "lspci (VGA/3D/Display)"; lspci | grep -iE 'vga|3d|display' || true
  else
    echo "lspci not found. $(pkg_hint pciutils)"
    MISSING+=("pciutils")
  fi
  if have nvidia-smi; then
    sub "nvidia-smi"; nvidia-smi || true
  fi
} >> "$OUTFILE"

# -------------------- missing tools summary -------------------
{
  section "Missing Tools & How to Install"
  if [[ ${#MISSING[@]} -eq 0 ]]; then
    echo "All optional tools used by this script were found (or skipped gracefully)."
  else
    mapfile -t uniq < <(printf "%s\n" "${MISSING[@]}" | sort -u)
    for t in "${uniq[@]}"; do
      echo "- $t:"
      pkg_hint "$t"
    done
  fi
} >> "$OUTFILE"

# --------------------------- notes ----------------------------
{
  section "Notes & Limitations"
  echo "- On WSL/VMs, many hardware details are virtualized (cache/DIMM/storage firmware)."
  echo "- For detailed DIMM info, run with sudo and have dmidecode installed: sudo dmidecode -t memory"
  echo "- For deeper CPU/cache/NUMA topology, install hwloc (lstopo)."
  echo "- The 'FLOPS' proxy is a quick compute workload; use LINPACK/HPL for rigorous FLOPS."
} >> "$OUTFILE"

echo "✅ Hardware report saved to: $OUTFILE"
