# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 11:18:15 2021

@author: root
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
#f = open(r'E:\1.0\revised\3_1_revised.csv','rb')
f = open(r'E:\1.0\456\4.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] 
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
x1=352072.8
y1=3459517.72
x2=352084.3
y2=3459475.45

a,b,c=GeneralEquation(x1,y1,x2,y2)
data['range']=a*data['x']+b*data['y']+c
plt.plot([x1,x2],[y1,y2])
data['range1']=0
data.loc[data['range']<0,'range1']=1
data1=data.loc[data['range1']==1]

len(data1.track_id.unique())

#set1
x3=352087.12
y3=3459518.39
x4=352098.8
y4=3459477.45


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

df4=df.copy()

df4.loc[:,'time1']=df4.loc[:,'time1'].values+69

df3_1=df3.loc[(df3.time1>100) & (df3.time1<5000),:]
df4_1=df4.loc[(df4.time1>100) & (df4.time1<5000),:]

# plt.plot(df3_1['time1'],df3_1['track_id'])
# plt.plot(df4_1['time1'],df4_1['track_id'])
mt=np.array([df3_1['track_id'].values,df4_1['track_id'].values])





import seaborn as sns
sns.heatmap(mt)

f = open(r'C:\Users\root\Desktop\轨迹拼接\3-4.xlsx','rb')
tid = pd.read_excel(f)
track_id=tid['p1_ID'].values


# mt1=mt.reshape(798, order='F')

# mt_pd=pd.DataFrame(mt1)
# mt_pd.columns=['id']
# def match_id(srise):
#     import heapq 
#     t=heapq.nlargest(3, srise)
#     return t

# tt1=mt_pd['id'].rolling(window=6,min_periods=1).sum()
# tt2=mt_pd['id'].rolling(window=6,min_periods=1).max()
# #tt2['id2']=-1
# tt3=tt1-tt2
# match_r=pd.DataFrame([tt2.T,tt3.T]).T
import time
starttime = time.time()

#match_r.clonums=['p1_ID' , 'p2_ID'] 待修改
mat=[]
for i in range(1,np.size(mt[0,:])-2):
    if mt[0,i]==0:
        continue
    else:
        k=0
        for j in range(-1,2):
            if mt[1,i+j]==0:
                continue
            else:
                m=[mt[0,i],mt[1,i+j]]
                k=1
        if k==0 :
            m=[mt[0,i],0]
    mat.append(m)

endtime = time.time()
print('总共的时间为:', round(endtime - starttime, 5),'secs')

mat1=pd.DataFrame(mat)     
mat1.columns=['p1_ID', 'p2_ID_m'] 
mat1=pd.merge(mat1,tid,on='p1_ID',how='inner')
mat1=mat1.drop_duplicates()
mat1['test']=(mat1['p2_ID_m']==mat1['p2_ID']).values     

mat1_p1=mat1.loc[:53]
rate=(mat1_p1[mat1_p1.test==True].count())/len(mat1_p1)  