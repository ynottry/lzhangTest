'''
Created on 16 Jun. 2019

@author: limengzhang
'''
import numpy as np
ms = open("./Size.txt")
mw=open("./DataComparisonSize.txt",'w')


#1-D:PREBLOCKINDEX
#2-D:TESTSIZE
#3-D:TestMethods
line=ms.readline()
b_index=0
pre_index=0
testSize=0
while True:
    if not line:
        break
    a=line.split()
    if a=='StartblockIndex':
        b_index=line.split()[1]
        line=ms.readline()
    elif a=='Preblocks':
        pre_index=line.split()[1]
        line=ms.readline()
    elif a=='testSize':
        testSize=line.split()[1]
        testMethod=0
        line=ms.readline()
    else:
        testMethod=testMethod+1
        mw.write(str(b_index)+'\t'+str(pre_index)+'\t'+str(testSize)+'\t'+str(testMethod)+'\t'+a+'\t'+line.split()[1]+'\n')
        line=ms.readline()
 
 

  
    
  
  
  
  
  
  

  