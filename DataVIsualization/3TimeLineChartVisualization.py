

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt


tips = pd.read_csv('./DataComparisonTime.txt', header=None, sep='\t',names=['blockPosition','PreBlocks','TestInterval','TestSize','TrainingSize','RMSE'])
# blockIndex=35
# preBlocks in [1,13]
# testSize in [10,60]
# methods in 1,2,3,4





def get_RatioComparion(tips,testInterval,blockIndex):
    result=tips[(tips['blockPosition'] == blockIndex) & (tips['TestInterval'] == testInterval)]
    return result





#Part1  Drawing picture with Varying TestSize

color=['r','b','g','y','c','m','k']
method=['testInterval=500-26','testInterval=1000-198','testInterval=2000-263']


testIntervalSet=[500,1000,2000]
Result_Y=[] 
for t in range(testIntervalSet.__len__()):      
    testInterval=testIntervalSet[t]
    Records=get_RatioComparion(tips, testInterval, 100)
    methodeResult=Records['RMSE']
    Result_Y.append(methodeResult)
    labellist=Records['TrainingSize']
    x =list(range(labellist.shape[0]))  


for i in range(Result_Y.__len__()):
    if i in range(testIntervalSet.__len__()):
        plt.plot(x, Result_Y[i],color[i], label=method[i])


plt.xticks(x, labellist, rotation=0,fontsize=5)
plt.yticks(fontsize=6.5)
plt.xlabel('TraingDataset-generated by increasing preblocks 1-99')

plt.ylabel('RMSE in various testIntervalSet')

plt.title('RMSE of Different testInterval on Varying Training Dataset') 
plt.legend(loc='upper right',fontsize='xx-small')

plt.savefig("TIme RMSE of Different testInterval on Varying Training Dataset.pdf")
plt.show()
