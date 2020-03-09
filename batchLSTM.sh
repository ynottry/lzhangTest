#!/bin/bash
#SBATCH --job-name=Pre_block
#SBATCH --output=LSTMPrediction.txt
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=16G
#SBATCH --time=150:00:00
#SBATCH --partition=skylake


python LSTMPredictionCom.py
~                    
