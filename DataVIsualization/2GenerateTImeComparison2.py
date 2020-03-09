'''
Created on 16 Jun. 2019

@author: limengzhang
'''
import numpy as np
ms = open("./TimeInterval.txt")
mw=open("./DataComparisonTime.txt",'w')


#1-D:PREBLOCKINDEX
#2-D:TESTSIZE
#3-D:TestMethods
line=ms.readline()
b_index=0
pre_index=0
testInterval=0.0
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
    elif a=='testInterval':
        testInterval=line.split()[1]
        line=ms.readline()
    else:
        mw.write(str(b_index)+'\t'+str(pre_index)+'\t'+str(testInterval)+'\t'+line)
        line=ms.readline()
 
 

  
    
  
  
  
  
  
  

  