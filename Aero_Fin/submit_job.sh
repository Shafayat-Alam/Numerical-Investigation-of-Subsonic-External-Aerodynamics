#!/bin/bash
#SBATCH --job-name=OpenFOAM_sim      # Name of the job
#SBATCH --output=result_%j.out      # Standard output log (%j inserts JobID)
#SBATCH --error=result_%j.err       # Error log
#SBATCH --partition=intel           # Options: intel, asus, or v100
#SBATCH --nodes=1                   # Number of nodes
#SBATCH --ntasks=16                 # Requesting 16 parallel slots
#SBATCH --cpus-per-task=1           # 1 CPU per task for MPI parallelization
#SBATCH --mem=16G                   # Memory request (e.g., 16GB)
#SBATCH --time=24:00:00             # Time limit (Hrs:Min:Sec)


# 1. Navigate to your working directory
cd ~/OpenFOAM/controlSurfaces/baseline

# 2. Make sure the script is executable
chmod +x ./simulate.sh

# 3. Run the command
./simulate.py