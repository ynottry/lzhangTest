
MIN_FEERATE = 10
MAX_FEERATE = 1e7
FEE_SPACING = 1.1
Decay=0.998
MIN_SUCCESS=0.95
max_confirmed=14
SUFFICIENT_FEETXS = 1

import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import MinMaxScaler
import numpy as np
import math


blockHeightIndex = 10
confirmedtimeintx = 12
receivetimeintx = 6
feerateintx = 14
enterBlockintx=15
sizeintx=4
weightintx=5
feeintx=9




training_blocks = 90




Start_Block=516738

total_EstimateBlock=100




BitcoinV14 = open('../NeuarlResult/BitcoinV14/result_BitcoinV14'+str(total_EstimateBlock)+'.txt', 'a')

def searchtxretrivalIndex(txcollection, blockHeight):
    txpos = -1
    for i in range(txcollection.__len__()):
        if int(txcollection[i][blockHeightIndex]) == blockHeight:
            txpos = i
            break
    return txpos


def blockHeightFind(txcollection, blockHeight):
    startindex=searchtxretrivalIndex(txcollection,blockHeight)
    if(startindex==-1):
        endindex=-1
    else:
        endindex = searchtxretrivalIndex(txcollection, blockHeight + 1)
        while (endindex == -1):
            blockHeight=blockHeight+1
            endindex=searchtxretrivalIndex(txcollection, blockHeight)
    return startindex,endindex









def calBucketIndex(feerate, bucketBoundary,fee_spacing):
    minfee=bucketBoundary[0]
    if feerate==0:
        index=0
    else:
        cfee=feerate/minfee
        index=math.log(cfee,fee_spacing)
    if index-int(index)>0:
        index=int(index+1)
    else:
        index=int(index)
    return index






def recommendation(confTarget,txCtAvg,avg,confAvg,unConfirmed_Numsum,oldUnconfTxs):
    if (confTarget <= 0 or confTarget > max_confirmed):
        return -1
    if confTarget == 1:
        confTarget = 2
    totalNum=0
    nConf=0
    unConf=0
    maxbucketindex=confAvg.shape[1]-1
    startbucket=maxbucketindex
    step=-1
    curNearBucket = startbucket
    bestNearBucket = startbucket
    curFarBucket = startbucket
    bestFarBucket = startbucket
    foundAnswer=-1
    bucket=startbucket
    while(bucket >= 0 and bucket <= maxbucketindex):
        curFarBucket=bucket
        nConf=nConf+confAvg[confTarget-1][bucket]
        totalNum=totalNum+txCtAvg[bucket]
        unConf=unConf+unConfirmed_Numsum[confTarget-1][bucket]+oldUnconfTxs[bucket]
        if totalNum>=SUFFICIENT_FEETXS/(1-Decay):
            bSuccess=nConf/(totalNum+unConf)
            if bSuccess<MIN_SUCCESS:
                break
            else:
                foundAnswer=1
                nConf=0
                totalNum=0
                unConf=0
                bestNearBucket=curNearBucket
                bestFarBucket=curFarBucket
                curNearBucket=bucket+step
        bucket=bucket+step
    median=-1
    txSum=0
    minBucket=min(bestNearBucket,bestFarBucket)
    maxBucket=max(bestNearBucket,bestFarBucket)
    for b in range(minBucket,maxBucket+1):
        txSum=txSum+txCtAvg[b]
    if foundAnswer==1 and txSum!=0:
        txSum=txSum/2
        for q in  range(minBucket,maxBucket+1):
            if txCtAvg[q]<txSum:
                txSum=txSum-txCtAvg[q]
            else:
                median=avg[q]/txCtAvg[q]
                break
    return median



def constructConfAVG(confirmed_Tx):
    rows=confirmed_Tx.shape[0]
    cols=confirmed_Tx.shape[1]
    confAVG = np.zeros((rows,cols))
    for i in range(rows):
        confAVG[i,:]=confirmed_Tx[i:rows,:].sum(axis=0)
    return confAVG


#
# def constructConfAVG_upperRoll(confirmed_Tx):
#     rows=confirmed_Tx.shape[0]
#     cols=confirmed_Tx.shape[1]
#     confAVG = np.zeros((rows,cols))
#     for i in range(rows):
#         confAVG[i,:]=confirmed_Tx[0:i+1,:].sum(axis=0)
#     return confAVG


def curBlockInfo(txcollection,blockheight,bucketBoundary):
    curBlockConf = np.zeros((max_confirmed, bucketBoundary.__len__()))
    curBlockTxCt=np.zeros(bucketBoundary.__len__())
    curBlockVal= np.zeros(bucketBoundary.__len__())
    tempCur= txcollection[np.where(txcollection[:,blockHeightIndex]==blockheight)]
    for tx in tempCur:
      feerate=tx[feerateintx]
      bucketIndex=calBucketIndex(feerate,bucketBoundary,FEE_SPACING)
      waitingblocks=int(tx[-1])
      for j in range(waitingblocks,max_confirmed+1):
        curBlockConf[j-1][bucketIndex]=curBlockConf[j-1][bucketIndex]+1
      curBlockTxCt[bucketIndex]=curBlockTxCt[bucketIndex]+1
      curBlockVal[bucketIndex]=curBlockVal[bucketIndex]+feerate
    return curBlockConf,curBlockVal,curBlockTxCt






# Construct Historical confirmed information
def txDatasetProcessing(txcollection,currentblockHeight,LastUpdataBlockHeight,bucketBoundary):
    confAvg = np.zeros((max_confirmed, bucketBoundary.__len__()))
    avg = np.zeros(bucketBoundary.__len__())
    txCtAvg = np.zeros(bucketBoundary.__len__())
    startUpdate=LastUpdataBlockHeight+1
    endUpdate=currentblockHeight
    for i in range(startUpdate,endUpdate+1):
        curBlockConf, curBlockVal, curBlockTxCt=curBlockInfo(txcollection,i,bucketBoundary)
        confAvg=confAvg*Decay+curBlockConf
        avg=avg*Decay+curBlockVal
        txCtAvg=txCtAvg*Decay+curBlockTxCt
    return confAvg,avg,txCtAvg













#Construct unconfirmed tx information in currentBlockHeight
#unConfirmed_tx[Y][B] means tx in bucketB has waited more than Y blocks











def constructUnConfirmed(txcollection, currentblockHeight):
    unconfirmed_Tx = np.zeros((max_confirmed,bucketBoundary.__len__()))
    oldUnconfTxs = np.zeros(bucketBoundary.__len__())
    templecollection = txcollection[np.where((txcollection[:, enterBlockintx] <= currentblockHeight) &
                                             (txcollection[:, blockHeightIndex] >= currentblockHeight))]

    for i in range(templecollection.shape[0]):
        receiveHeight = int(templecollection[i][enterBlockintx])
        waitingblocks = currentblockHeight - receiveHeight + 1
        feerate = templecollection[i][feerateintx]
        bucketindex = calBucketIndex(feerate, bucketBoundary, FEE_SPACING)
        if waitingblocks <= max_confirmed:
            unconfirmed_Tx[waitingblocks - 1][bucketindex] = unconfirmed_Tx[waitingblocks - 1][
                                                                    bucketindex] + 1
        else:
            oldUnconfTxs[bucketindex] = oldUnconfTxs[bucketindex] + 1
    # Number of TX which waiting blocks no less than Y Blocks

    unConfirmed_TXs = constructConfAVG(unconfirmed_Tx)
    return unConfirmed_TXs, oldUnconfTxs




















def BitcoinV14_estimation(confAvg, avg, txCtAvg, unConfirmed_Txs,oldUnconfTxs):
    rec_result=[]
    for i in range(1,max_confirmed+1):
        result=recommendation(i,txCtAvg,avg,confAvg,unConfirmed_Txs,oldUnconfTxs)
        rec_result.append(result)

    return rec_result

# ##names=['tx_index','vin_sz','vout_sz','ver','size', 'weight', 'time','relayed_by', 'lock_time','fee',
#####'block_height', 'block_index', 'confirmedtime', 'watingtime', 'feerate', 'enterBlock', 'watiingblock']



data = pd.read_csv('../txinblock2.csv', sep=",",
                   names=['tx_index', 'vin_sz', 'vout_sz', 'ver', 'size', 'weight', 'time', 'relayed_by', 'lock_time',
                          'fee',
                          'block_height', 'block_index', 'confirmedtime', 'watingtime', 'feerate', 'enterBlock',
                          'watiingblock'])
data['feerate'] = 4 * data['fee'] / data['weight']
data = data[data.feerate > 0]
data = data[data.watiingblock > 0]
# data.to_csv("txinblock2_bitcore.csv",index=False,header=False)

txdata = np.array(data)
#txdata = np.loadtxt('test.csv', delimiter=",")







minRelayFee=txdata[:,14].min(axis=0)
if minRelayFee==0:
    minRelayFee=0.1
elif minRelayFee>MIN_FEERATE:
    minRelayFee=MIN_FEERATE

maxFee=txdata[:,14].max(axis=0)
if maxFee<MAX_FEERATE :
    maxFee=MAX_FEERATE

dbucketBoundary = minRelayFee
bucketBoundary=[minRelayFee]
while dbucketBoundary <= maxFee :
    dbucketBoundary=dbucketBoundary*FEE_SPACING
    bucketBoundary.append(dbucketBoundary)

for i in range(total_EstimateBlock):

    # currentblockHeight=int(txdata[0][blockHeightIndex]+training_blocks-1)+i
    # LastUpdataBlockHeight=int(txdata[0][blockHeightIndex]-1)+i
    currentblockHeight = Start_Block + i
    LastUpdataBlockHeight = currentblockHeight - training_blocks - 1
    print(currentblockHeight)

    confAvg1,avg1,txCtAvg1=txDatasetProcessing(txdata,currentblockHeight,LastUpdataBlockHeight,bucketBoundary)
    unConfirmed_Txs,oldUnconfTxs=constructUnConfirmed(txdata,currentblockHeight)

    targets_Rec=BitcoinV14_estimation(confAvg1,avg1,txCtAvg1,unConfirmed_Txs,oldUnconfTxs)
    targets_Rec=np.array(targets_Rec)
    BitcoinV14.write('currentBlockHeight: '+str(currentblockHeight))
    BitcoinV14.write('LastUpdataBlockHeight: ' + str(LastUpdataBlockHeight))
    BitcoinV14.write('\n')
    for i in range(targets_Rec.__len__()):
        BitcoinV14.write(str(targets_Rec[i])+'\t')
    BitcoinV14.write('\n')
    print(targets_Rec)

BitcoinV14.close()
