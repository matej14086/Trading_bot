# -*- coding: utf-8 -*-
"""
Created on Wed Oct 10 18:27:57 2018

@author: Matej Pavlović
"""
from tqdm import tqdm
import pandas as pd
import numpy as np
from Get_data import save_sp500_tickers
import datetime

def df_derived_by_shift(df,lag=0,NON_DER=[]):
    df = df.copy()
    if not lag:
        return df
    cols ={}
    for i in range(1,lag+1):
        for x in list(df.columns):
            if x not in NON_DER:
                if not x in cols:
                    cols[x] = ['{}_{}'.format(x, i)]
                else:
                    cols[x].append('{}_{}'.format(x, i))
    for k,v in cols.items():
        columns = v
        dfn = pd.DataFrame(data=None, columns=columns, index=df.index)    
        i = 1
        for c in columns:
            dfn[c] = df[k].shift(periods=i)
            i+=1
        df = pd.concat([df, dfn], axis=1, join_axes=[df.index])
    return df


def calulate_corelation(data_file="sp500_history.csv",atribute="High"):
	symb=save_sp500_tickers()
	data=pd.read_csv(data_file)
	data["Date"]=pd.to_datetime(data["Date"])
	cor=[]
	pairs=[]
	
	
	for i in tqdm(range(len(symb))):
		for j in range(i+1,len(symb)):
			datax=data[data["NAME"]==symb[i]][["Date",atribute]]
			datay=data[data["NAME"]==symb[j]][["Date",atribute]]
			if len(datax)!=0 and len(datay)!=0:
				temp=pd.merge(datax,datay,on="Date",how="inner")
				NON_DER = ['Date',]
				df_new = df_derived_by_shift(temp, 7, NON_DER)
			
				df_new = df_new.dropna()
				corr=df_new.corr()
				cor.append(corr)
				pairs.append([symb[i],symb[j]])
	
	a=[]
	for b in tqdm(cor):
		a.append(b.values)
	
	a=np.array(a)
	now=datetime.datetime.now()

	np.save("corelation_"+atribute+"_"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+".npy",a)
	a=pd.DataFrame(pairs)
	a.to_csv("pairs_"+atribute+"_"+str(now.year)+"-"+str(now.month)+"-"+str(now.day)+"_"+str(now.hour)+":"+str(now.minute)+".csv")
