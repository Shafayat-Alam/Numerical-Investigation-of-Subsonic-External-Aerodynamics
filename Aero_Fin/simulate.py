#!/usr/bin/env python3
import subprocess
import os
import stat
import sys

def run_solver():
    # Set execution permissions for the script itself
    try:
        os.chmod(__file__, os.stat(__file__).st_mode | stat.S_IEXEC)
    except Exception as e:
        print(f"Note: Could not set permissions: {e}")

    # Ensure the logs directory exists
    if not os.path.exists('logs'): 
        os.makedirs('logs')
    
    # Configuration
    n_procs = 12 # Ensure this matches your decomposeParDict 'numberOfSubdomains'
    solver = "rhoSimpleFoam"
    
    tasks = [
        ("decomposePar -force", "logs/log.decomposePar"),
        (f"mpirun -np {n_procs} {solver} -parallel", f"logs/log.{solver}"),
        ("reconstructPar", "logs/log.reconstructPar")
    ]

    for cmd, log_path in tasks:
        print(f"Running: {cmd} (Logging to {log_path})...")
        try:
            with open(log_path, "w") as log_file:
                # Use subprocess.run for a cleaner, blocking execution
                subprocess.run(
                    cmd, 
                    shell=True, 
                    stdout=log_file, 
                    stderr=subprocess.STDOUT, 
                    check=True
                )
            print(f"Finished: {cmd}")
        except subprocess.CalledProcessError:
            print(f"\nCRITICAL ERROR: Command '{cmd}' failed.")
            print(f"Check the end of {log_path} for details.")
            sys.exit(1)

if __name__ == "__main__":
    run_solver()