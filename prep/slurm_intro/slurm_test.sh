#!/bin/bash
#SBATCH --partition=demo
#SBATCH --nodes=1                            ## how many computers do you need?
#SBATCH --ntasks-per-node=1                  ## how many cpus or processors do you need on each computer?
#SBATCH --time=00:10:00                      ## time needed to run (HH:MM:SS)
#SBATCH --mem-per-cpu=1G                     ## RAM per CPU, also see --mem=<XX>G for RAM per node/computer 
#SBATCH --job-name=slurm_example             ## When you run squeue -u $USER this is how you can identify the job
#SBATCH --output=outlog                      ## standard output goes to this file
#SBATCH --error=errlog                       ## standard error goes to this file
#SBATCH --mail-type=ALL                      ## receive e-mail alerts from SLURM when your job begins and finishes
#SBATCH --mail-user=<your-email>          ## replace with your e-mail address

# On AWS the system python3 is sufficient (no python module to load).
python3 --version
python3 slurm_test.py --name STRANGER  # Replace STRANGER with your name to supply to the python script
