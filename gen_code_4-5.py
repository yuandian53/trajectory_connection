# -*- coding: utf-8 -*-
"""
Created on Sat Apr  2 12:31:30 2022

@author: root
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time
import dtw_iden
import list_iden



#===============序列匹配的数据=============
f = open(r'E:\1.0\456\4.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] #筛选出数据
data=dataclean(data)
#画图
for i in range(1000,1200):
    line_=data[(data.track_id==i)&(data.direction==1)]
    plt.plot(line_['x'],line_['y'])
#右
x3=352401.94
y3=3459580.72
x4=352403.53
y4=3459552.92
#左
x1=352394.74
y1=3459578.9
x2=352396.86
y2=3459551.91
data2=split(x1,y1,x2,y2,x3,y3,x4,y4,data)
data2['lane_id']=data2['lane_id'].astype(int)
data2=data2[data2.lane_id<10]

for i in range(1000,1200):
    line_=data2[(data2.track_id==i)]
    plt.plot(line_['x'],line_['y'])
#取出数据序列基础
#data3=data2.drop_duplicates(['track_id'])


dt4=sequence(data2)

f = open(r'E:\1.0\456\5-1.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] #筛选出数据
data=dataclean(data)
#左
x3=352404.16
y3=3459579.85
x4=352406.19
y4=3459552.88
#右
x1=352396.65
y1=3459578.98
x2=352399.18
y2=3459551.93
data2=split(x1,y1,x2,y2,x3,y3,x4,y4,data)
data2['lane_id']=data2['lane_id'].astype(int)
data2=data2[data2.lane_id<10]
dt3=sequence(data2)

for i in range(1000,1200):
    line_=data2[(data2.track_id==i)]
    plt.plot(line_['x'],line_['y'])
#==========DTW数据准备==========
f = open(r'E:\1.0\456\4.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] #筛选出数据
data=dataclean(data)

#左机位
x1=352378.21
y1=3459575.14
x2=352380.43
y2=3459548.13

a,b,c=GeneralEquation(x1,y1,x2,y2)
data['range']=a*data['x']+b*data['y']+c
plt.plot([x1,x2],[y1,y2])
data['range1']=0
data.loc[data['range']<0,'range1']=1
data1=data.loc[data['range1']==1]

plt.plot([x1,x2],[y1,y2])
for i in range(1000,1200):
    line_=data1[(data1.track_id==i)]
    plt.plot(line_['x'],line_['y'])

data1['x1_diff']=data1['x1'].diff()
data1=data1.groupby([data1['track_id']]).apply(queshi1)   
data1=data1.groupby([data1['track_id']]).apply(queshi2)  
data1=data1.dropna(axis=0, how='any')


f = open(r'E:\1.0\456\5-1.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] 
data=dataclean(data)

#右机位
x3=352410.76
y3=3459583.99
x4=352413.73
y4=3459554.33

a,b,c=GeneralEquation(x3,y3,x4,y4)
data['range']=a*data['x']+b*data['y']+c
data['range1']=0
data.loc[data['range']>0,'range1']=1
data2=data.loc[data['range1']==1]

plt.plot([x3,x4],[y3,y4])
for i in range(1000,1200):
    line_=data2[(data2.track_id==i)]
    plt.plot(line_['x'],line_['y'])

#data2.time1=data2.time1+60
data2['x1_diff']=data2['x1'].diff()
data2=data2.groupby([data2['track_id']]).apply(queshi1)   
data2=data2.groupby([data2['track_id']]).apply(queshi2)  
data2=data2.dropna(axis=0, how='any')


#===============1方向===============
#时间校验==人工
time_v=time_verify(data1,data2,90,220)

#取出规定方向和车辆的数据
import time
#关闭警告
pd.set_option('mode.chained_assignment', None)
starttime = time.time()
 
result=pd.DataFrame()
for j in range(1,4):
    df4_11=pick_match(j,1,dt4)
    df3_11=pick_match(j,1,dt3)
    df4_11.loc[:,'time1']=df4_11.loc[:,'time1'].values+time_v
    data_copy=data2.loc[(data2['direction']==1),:]
    for k in range(1,20):
    #筛选待匹配的数据
        df3_111=df3_11.loc[(df3_11.time1>120*k) & (df3_11.time1<=120*(k+1)),:]
        df4_111=df4_11.loc[(df4_11.time1>120*k) & (df4_11.time1<=120*(k+1)),:]
        
        #合成seq
        mt=np.array([df3_111['track_id'].values,df4_111['track_id'].values])
        
        #匹配
        mat1=se_match(mt)
        mat1=mat1.drop_duplicates()
        
        pick_id=mat1.p1_ID[-10:].values
                
        data_t=pd.DataFrame()
        for i in pick_id:
            r=data1.loc[data1.track_id == i,:]
            data_t=data_t.append(r)

        re1=dtw_main(data_t,data_copy,time_v)
        re2=re1[['p1_ID','p2_ID_m1']]
        mat1_iden=mat1.iloc[-10:]
        mat1_iden=pd.merge(mat1_iden,re2,on='p1_ID',how='left')
        mat1_iden.loc[:,'test1']=(mat1_iden['p2_ID_m1']==mat1_iden['p2_ID_m_list']).copy().values 
        rate=(mat1_iden.test1[(mat1_iden.test1==True)].count())/len(mat1_iden)
        if rate<0.4:
            print(str(j)+"车道"+str(k)+'min之后匹配不上')
            break
        else:
            mat1['lane_id']=j
            mat1['direction']=1
            result=result.append(mat1)
endtime = time.time()
print('总共的时间为:', round(endtime - starttime, 2),'secs')        

#检查匹配不上的可能性
df3_11=pick_match(j,1,dt3)
df3_111=df3_11.loc[(df3_11.time1>120*k) & (df3_11.time1<=120*(k+1)),:]
#df4_111=df4_11.loc[(df4_11.time1>120*k) & (df4_11.time1<=360*k),:]
pick1_id=df3_111.track_id.unique()
data_t=pd.DataFrame()
for i in pick1_id:
    r=data1.loc[data1.track_id == i,:]
    data_t=data_t.append(r)
data_copy=data2.loc[(data2['lane_id']==j)  & (data2['direction']==1),:]
re=dtw_main(data_t,data_copy,time_v)

#填上去
re_buch=re.dropna(axis=0, how='any', inplace=False) 
result=result.append(re_buch)
           
time_v=time_verify(data1,data2,6118,3436)

#处理result  
result.loc[ pd.isnull(result.p2_ID_m_list),'p2_ID_m_list']=result.loc[pd.isnull(result.p2_ID_m_list),'p2_ID_m1']
result_final=result[['p1_ID','p2_ID_m_list']]
result.to_csv(r'E:\1.0\result'str(0)+"方向"+str(k)+'min.csv')  


#===============0方向===============

time_v=time_verify(data2,data1,239,220)  
starttime = time.time()
 
#result=pd.DataFrame()
for j in range(1,3):
    df4_11=pick_match(j,0,dt3)
    df3_11=pick_match(j,0,dt4)
    df4_11.loc[:,'time1']=df4_11.loc[:,'time1'].values+time_v
    data_copy=data1.loc[ (data1['direction']==0),:]
    for k in range(1,20):
    #筛选待匹配的数据
        df3_111=df3_11.loc[(df3_11.time1>120*k) & (df3_11.time1<=120*(k+1)),:]
        df4_111=df4_11.loc[(df4_11.time1>120*k) & (df4_11.time1<=120*(k+1)),:]
        
        #合成seq
        mt=np.array([df3_111['track_id'].values,df4_111['track_id'].values])
        
        #匹配
        mat1=se_match(mt)
        mat1=mat1.drop_duplicates()
        
        pick_id=mat1.p1_ID[-10:].values
                
        data_t=pd.DataFrame()
        for i in pick_id:
            r=data2.loc[data2.track_id == i,:]
            data_t=data_t.append(r)

        re1=dtw_main(data_t,data_copy,time_v)
        re2=re1[['p1_ID','p2_ID_m1']]
        mat1_iden=mat1.iloc[-10:]
        mat1_iden=pd.merge(mat1_iden,re2,on='p1_ID',how='left')
        mat1_iden.loc[:,'test1']=(mat1_iden['p2_ID_m1']==mat1_iden['p2_ID_m_list']).copy().values 
        rate=(mat1_iden.test1[(mat1_iden.test1==True)].count())/len(mat1_iden)
        if rate<0.4:
            print(str(0)+"方向"+str(j)+"车道"+str(k)+'min之后匹配不上')
            break
        else:
            mat1['lane_id']=j
            mat1['direction']=0
            result=result.append(mat1)
endtime = time.time()
print('总共的时间为:', round(endtime - starttime, 2),'secs')  

#0方向检查匹配不上的可能性

def check(j,k):#(车道，时间)
    df3_11=pick_match(j,0,dt4)
    df3_111=df3_11.loc[(df3_11.time1>120*k) & (df3_11.time1<=120*(k+1)),:]
    #df4_111=df4_11.loc[(df4_11.time1>120*k) & (df4_11.time1<=360*k),:]
    pick1_id=df3_111.track_id.unique()
    data_t=pd.DataFrame()
    for i in pick1_id:
        r=data2.loc[data2.track_id == i,:]
        data_t=data_t.append(r)
    data_copy=data1.loc[(data1['lane_id']==j)  & (data1['direction']==0),:]
    re=dtw_main(data_t,data_copy,time_v)
    return re

re=check(j,k)
#填上去
re_buch=re.dropna(axis=0, how='any', inplace=False) 
result=result.append(re_buch)
           

#处理result  
result.loc[ pd.isnull(result.p2_ID_m_list),'p2_ID_m_list']=result.loc[pd.isnull(result.p2_ID_m_list),'p2_ID_m1']
result_final=result[['p1_ID','p2_ID_m_list']]
result.to_csv(r'E:\1.0\result'+str(0)+"方向"+str(k)+'min.csv')  