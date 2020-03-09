#!/bin/bash
#SBATCH --job-name=BV14
#SBATCH --output=consoleBV14.txt
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=16G
#SBATCH --time=24:00:00
#SBATCH --partition=skylake



python BitcoreV14_final.py
~                    
