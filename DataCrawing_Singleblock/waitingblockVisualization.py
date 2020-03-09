import numpy as np
v v
txdata = np.loadtxt('txinblock2_valid.csv', delimiter=",")


feeRate=txdata[:,-3]
minRelayFeeRate=txdata[:,-3].min(axis=0)


waitingblock=txdata[:,-1]
maxconfirmBlocks=waitingblock.max(axis=0)