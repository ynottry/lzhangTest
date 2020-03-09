'''
Created on 16 Jun. 2019

@author: limengzhang
'''
import numpy as np
ms = open("./Ratio")
mw=open("./DataComparisonRatio1.txt",'w')


#1-D:PREBLOCKINDEX
#2-D:TESTSIZE
#3-D:TestMethods
line=ms.readline()
b_index=0
pre_index=0
testRatio=0.0
while True:
    if not line:
        break
    a=line.split()[0]
    if a=='StartblockIndex':
        b_index=line.split()[1]
        line=ms.readline()
    elif a=='Preblocks':
        pre_index=line.split()[1]
        line=ms.readline()
    elif a=='testRatio':
        testRatio=line.split()[1]
        line=ms.readline()
    else:
        mw.write(str(b_index)+'\t'+str(pre_index)+'\t'+str(testRatio)+'\t'+line)
        line=ms.readline()
 
 

  
    
  
  
  
  
  
  

  