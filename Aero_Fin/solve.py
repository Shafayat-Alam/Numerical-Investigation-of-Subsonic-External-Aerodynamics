#!/usr/bin/env python3
import subprocess
import os
import stat

def run_solver():
    # Set execution permissions for itself
    os.chmod(__file__, os.stat(__file__).st_mode | stat.S_IEXEC)

    if not os.path.exists('logs'): 
        os.makedirs('logs')
    
    n_procs = 12 # Needs to match decomposeParDict
    
    tasks = [
        ("decomposePar -force", "logs/log.decomposePar"),
        (f"mpirun -np {n_procs} rhoSimpleFoam -parallel", "logs/log.rhoSimpleFoam"),
        ("reconstructPar", "logs/log.reconstructPar")
    ]

    for cmd, log_path in tasks:
        print(f"Executing: {cmd}...")
        with open(log_path, "w") as log_file:
            subprocess.run(cmd, shell=True, stdout=log_file, stderr=subprocess.STDOUT, check=True)

if __name__ == "__main__":
    run_solver()
