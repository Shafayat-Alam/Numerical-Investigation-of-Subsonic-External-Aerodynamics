#!/usr/bin/env python3
import subprocess
import os
import stat
import shutil
import glob
import time

def have(cmd: str) -> bool:
    return shutil.which(cmd) is not None

def newest(pattern: str) -> str | None:
    files = glob.glob(pattern)
    if not files:
        return None
    return max(files, key=os.path.getmtime)

def open_terminal(title: str, command: str) -> None:
    # Try common terminal emulators
    if have("gnome-terminal"):
        subprocess.Popen(["gnome-terminal", "--title", title, "--", "bash", "-lc", command])
        return
    if have("xterm"):
        subprocess.Popen(["xterm", "-T", title, "-e", "bash", "-lc", command])
        return
    if have("konsole"):
        subprocess.Popen(["konsole", "-p", f"tabtitle={title}", "-e", "bash", "-lc", command])
        return
    print(f"[warn] No supported terminal emulator found. Can't open '{title}'.")

def run_solver():
    os.chmod(__file__, os.stat(__file__).st_mode | stat.S_IEXEC)

    os.makedirs("logs", exist_ok=True)

    n_procs = 12  # must match decomposeParDict

    # 1) Decompose
    print("Executing: decomposePar -force ...")
    with open("logs/log.decomposePar", "w") as f:
        subprocess.run("decomposePar -force", shell=True, stdout=f, stderr=subprocess.STDOUT, check=True)

    # 2) Start monitors (they will wait until files exist)
    # forceCoeffs file pattern
    force_file_cmd = r"""
set -e
echo "Waiting for forceCoeffs.dat..."
while true; do
  f=$(ls -t postProcessing/forceCoeffs/*/forceCoeffs.dat 2>/dev/null | head -n 1 || true)
  if [ -n "$f" ]; then echo "Monitoring $f"; break; fi
  sleep 0.5
done
foamMonitor "$f"
"""

    # residuals file pattern (solverInfo). The exact filename can vary; monitor the newest file under postProcessing/residuals
    resid_file_cmd = r"""
set -e
echo "Waiting for residuals file..."
while true; do
  f=$(ls -t postProcessing/residuals/*/* 2>/dev/null | head -n 1 || true)
  if [ -n "$f" ]; then echo "Monitoring $f"; break; fi
  sleep 0.5
done
foamMonitor "$f"
"""

    open_terminal("foamMonitor: forceCoeffs", force_file_cmd)
    open_terminal("foamMonitor: residuals", resid_file_cmd)

    # 3) Run solver (parallel)
    print(f"Executing: mpirun -np {n_procs} rhoSimpleFoam -parallel ...")
    with open("logs/log.rhoSimpleFoam", "w") as f:
        subprocess.run(f"mpirun -np {n_procs} rhoSimpleFoam -parallel",
                       shell=True, stdout=f, stderr=subprocess.STDOUT, check=True)

    # 4) Reconstruct
    print("Executing: reconstructPar ...")
    with open("logs/log.reconstructPar", "w") as f:
        subprocess.run("reconstructPar", shell=True, stdout=f, stderr=subprocess.STDOUT, check=True)

if __name__ == "__main__":
    run_solver()

