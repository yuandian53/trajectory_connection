# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 10:05:46 2021

@author: root
"""


import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#f = open(r'E:\1.0\revised\3_1_revised.csv','rb')
f = open(r'E:\1.0\new\3-1.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')

def GeneralEquation(first_x,first_y,second_x,second_y):
    # 一般式 Ax+By+C=0
    A=second_y-first_y
    B=first_x-second_x
    C=second_x*first_y-first_x*second_y
    return A,B,C


for i in range(5):
    line_=data[(data.track_id==i)&(data.direction==1)]
    plt.plot(line_['x'][:10],line_['y'][:10])

def roll(srise):
    srise['x1']=srise['x'].rolling(window=25).mean()
    srise['y1']=srise['y'].rolling(window=25).mean()
    return srise

#数据滤波
data=data.groupby([data['track_id']]).apply(roll)     
data=data.dropna(axis=0)
#数据集计

data['time1']=data['time']*2 #影响到达识别
data['time1']=data['time1'].astype(int)
data=data.groupby([data['track_id'],data['time1'],data['lane_id'],data['type'],data['direction']]).mean()
data=data.reset_index()

#set1
x1=352084.12
y1=3459515.56
x2=352095.21
y2=3459473.86

a,b,c=GeneralEquation(x1,y1,x2,y2)
data['range']=a*data['x']+b*data['y']+c
plt.plot([x1,x2],[y1,y2])
data['range1']=0
data.loc[data['range']<0,'range1']=1
data1=data.loc[data['range1']==1]

len(data1.track_id.unique())

#set1
x3=352096.52
y3=3459518.62
x4=352108.07
y4=3459477.16


a,b,c=GeneralEquation(x3,y3,x4,y4)
data1['range']=a*data1['x']+b*data1['y']+c
plt.plot([x3,x4],[y3,y4])
data1['range1']=0
data1.loc[data1['range']>0,'range1']=1
data2=data1.loc[data1['range1']==1]

len(data2.track_id.unique())

#data3=data2.groupby([data2['track_id'],data2['lane_id']]).mean()
data2['lane_id']=data2['lane_id'].astype(int)

data3=data2.drop_duplicates(['track_id'])


data3=data3.sort_values(by='time',ascending=True)

cf=data3[data3.duplicated(['time1','lane_id','direction'])]
data3=data3.drop_duplicates(['time1','lane_id','direction'])
# dt=data3['track_id'].groupby([data3['time1'],data3['lane_id'],data3['direction']]).count()
# dt=dt.reset_index()

dt=data3[['time1','lane_id','direction','track_id']]

df=dt.loc[(dt['lane_id']==1)  & (dt['direction']==1),:]
d=df.time1.unique()
d1 = np.linspace(min(d), max(d),num=(max(d)-min(d)+1))
d_df=pd.DataFrame()
d_df['time1']=d1
d_df['val']=0
df=pd.merge(df,d_df,on='time1',how='outer')

df=df.sort_values(by='time1',ascending=True)
#df=df.iloc[:,:-4]
df=df.fillna(0)
df.loc[df['lane_id']>0,'val']=1
df3=df.copy()