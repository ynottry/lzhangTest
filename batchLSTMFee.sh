#!/bin/bash
#SBATCH --job-name=ComFee500
#SBATCH --output=LSTMPrediction.txt
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=16G
#SBATCH --time=13:00:00
#SBATCH --partition=skylake


python LSTMPredictionComFee.py
~                    
