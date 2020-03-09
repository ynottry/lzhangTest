#!/bin/bash
#SBATCH --job-name=ComFeeNoneEnterBlock
#SBATCH --output=LSTMPrediction.txt
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --mem-per-cpu=32G
#SBATCH --time=4:00:00
#SBATCH --partition=skylake


python LSTMPredictionComFeeNoneEnterBlock.py
~                    
