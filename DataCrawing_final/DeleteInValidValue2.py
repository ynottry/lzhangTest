'''
Created on 19 Sep. 2019

@author: LImengzhang
'''
import pandas as pd

data=pd.read_csv("txinblock2.csv",sep=",",names=['tx_index','vin_sz','vout_sz','ver','size', 'weight', 'time','relayed_by', 'lock_time','fee',
                                                 'block_height', 'block_index','confirmedtime','watingtime','feerate','enterBlock','watiingblock'])

data['feerate']=4*data['fee']/data['weight']
data['watiingblock']=data['block_height']-data['enterBlock']+1
data.to_csv("txinblock2float.csv",index=False,header=False)



data2=data[data.feerate==0]
data2.to_csv("txinblock2_invalid0.csv",index=False,header=False)


data3=data[data.feerate<1]
data3.to_csv("txinblock2_invalid1.csv",index=False,header=False)
