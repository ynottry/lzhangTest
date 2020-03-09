import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np




lstmtimestamps=3
blockFeatures=5
neuralTimestamps=1
txFeatures=7

training_blocks=90

blockindexposintx=11
confirmedtimeintx=12
receivetimeintx=7
feerateintx = 14



np.random.seed(9)
maxfeerate=100






#
#
# log = open("./testbucket.txt",'a')
#
# def TestBuckket(txcollection,start_Pos,terminal_Pos):
#   log = open("./testbucket.txt", 'a')
#   bucket = np.zeros(bucketNo)
#   intervalbuc=10
#   txindex = []
#   confimedTime = txcollection[start_Pos][confirmedtimeintx]
#   for j in range(start_Pos, terminal_Pos):
#     if txcollection[j][receivetimeintx] <= confimedTime:  # including txcollection[j][confirmedtimeintx] >= confimedTime and
#       pos = int(txcollection[j][feerateintx] / intervalbuc)
#       if pos >= bucketNo - 1:
#         pos = bucketNo - 1
#       bucket[pos] = bucket[pos] + 1
#       log.write(str(j-start_Pos)+'\t'+ str(txcollection[j][feerateintx])+'\t'+str(pos)+'\t'+str(bucket)+'\t'+str(sum(bucket))+'\n')
#       if int(j-start_Pos/10)==0:
#         log.write('\n')
#   log.close()
#

blockstar_heightInx=10
def searchtxretrivalIndex(txcollection,blockstar_height):
  txpos=0
  for i in range(txcollection.__len__()):
    if int(txcollection[i][blockstar_heightInx])==blockstar_height:
      txpos=i
      break
  return txpos


def getHeight(tx_time, blockHeight, blockTime):
    blockNum=blockHeight.size
    start=0
    end=blockNum-1

    if tx_time > blockTime[start] or tx_time < blockTime[end]:
        pos = -2000
        return blockHeight[pos]
    else:
        while start <= end:
            mid = (start + end) // 2
            if tx_time > blockTime[mid]:
                end = mid - 1
            elif tx_time < blockTime[mid]:
                start = mid + 1
            elif tx_time == blockTime[mid]:
                pos = mid
                break
        if (start > end):
            pos = end
        return blockHeight[pos]







def getHeight2(tx_time, blockTime):
    blockNum=blockTime.shape[0]
    start=0
    end=blockNum-1

    pos=-2
    label=0


    #     mid = (start + end) // 2
    #     if tx_time>blockTime[mid]:
    #         end = mid - 1
    #     elif tx_time<blockTime[mid]:
    #         start = mid + 1
    #     elif tx_time==blockTime[mid]:
    #         pos=mid
    #         break
    # startValue=blockTime[start]
    # endValue=blockTime[end]
    # if tx_time>=startValue and tx_time<endValue and pos==-2:
    #     pos=startValue
    if tx_time>blockTime[start] or tx_time<blockTime[end]:
        pos=-2000
        return pos
    else:
        while start <= end:
            mid = (start + end) // 2
            if tx_time > blockTime[mid]:
                end = mid - 1
            elif tx_time < blockTime[mid]:
                start = mid + 1
            elif tx_time == blockTime[mid]:
                pos = mid
                break
        if(start>end):
            pos = end
        return pos






 # keys=['block_index','height' ,'n_tx', 'size', 'bits', 'weight', 'fee', 'ver','time']




#tx_features = ['tx_index', 'vin_sz', 'vout_sz', 'fee', 'ver', 'size', 'weight', 'time', 'relayed_by', 'lock_time',
#               'block_height', 'block_index',confimredtime, waiting time,'feerate']




##Finaal  Final_tx_features=['tx_index','vin_sz','vout_sz','ver','size', 'weight', 'time','relayed_by', 'lock_time','fee',
    ###############block_height', 'block_index','confirmedtime','watingtime','feerate','enterBlock','watiingblock']

#Block keys=['block_index','height' ,'n_tx', 'size', 'bits', 'fee', 'ver','time']



relayIndex=7
timeIndex=6
confirmedHeightIndex=10


totalblockData=pd.read_csv("Block.txt",header=None,sep=" ")
totalblockData=totalblockData[::-1]
blockHeight=totalblockData[1]
blockTime=totalblockData[7]
totalblockData.to_csv("Block.csv",index=False,header=False)





# construct dataset
ExperimetHeightStart=516639
ExperimetHeightEnd=516851




blockData=pd.read_csv("Block2.txt",header=None,sep=" ")
txdata = pd.read_csv("txinBlock2.txt",header=None,sep=" ")



txdata = txdata[::-1]
blockData=blockData[::-1]



encoder=LabelEncoder()
txdata[relayIndex]=encoder.fit_transform(txdata[relayIndex])

recordsNo=txdata.shape[0]


txTime = txdata[timeIndex]

txNum=recordsNo

txReceiveHeight=[]





for i in range(txNum):
    tx_time=txTime[i]
    tx_height=getHeight(tx_time,blockHeight,blockTime)
    txReceiveHeight.append(tx_height)
    print(i)

txdata[15]=pd.Series(txReceiveHeight)
#index9 LocktimeHeight
#index15 receiveTImeHeight

validBlockTime = txdata[15]

txdata[16]=txdata[confirmedHeightIndex]-validBlockTime


blockData.to_csv("block2.csv",index=False,header=False)
txdata.to_csv("txinblock2.csv",index=False,header=False)



