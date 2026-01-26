#!/usr/bin/env python3
import os
import subprocess
import stat

def run_mesh():
    # Set execution permissions for itself
    os.chmod(__file__, os.stat(__file__).st_mode | stat.S_IEXEC)
    
    if not os.path.exists('logs'): 
        os.makedirs('logs')
    
    # 16 ranks as per your decomposeParDict
    n_procs = 12

    # Step 1: Serial prep work
    prep_commands = [
        ("blockMesh", "logs/log.blockMesh"),
        ("surfaceFeatureExtract", "logs/log.surfaceFeatureExtract"),
        ("decomposePar -force", "logs/log.decomposeParMesh")
    ]

    for cmd, log_path in prep_commands:
        print(f"Running {cmd}...")
        with open(log_path, "w") as log_file:
            subprocess.run(cmd.split(), stdout=log_file, stderr=subprocess.STDOUT, check=True)

    # Step 2: Parallel snappyHexMesh
    print(f"Running snappyHexMesh in parallel on {n_procs} cores...")
    snappy_cmd = f"mpirun -np {n_procs} snappyHexMesh -overwrite -parallel"
    with open("logs/log.snappyHexMesh", "w") as log_file:
        subprocess.run(snappy_cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT, check=True)

    # Step 3: Reconstruct mesh and cleanup processor directories
    print("Reconstructing mesh...")
    post_commands = [
        ("reconstructParMesh -constant", "logs/log.reconstructParMesh"),
        ("rm -rf processor*", "/dev/null") 
    ]

    for cmd, log_path in post_commands:
        # Use shell=True for the rm command to handle wildcards
        is_shell = "*" in cmd
        with open(log_path, "w") as log_file:
            subprocess.run(cmd if is_shell else cmd.split(), shell=is_shell, stdout=log_file, stderr=subprocess.STDOUT)

if __name__ == "__main__":
    run_mesh()
