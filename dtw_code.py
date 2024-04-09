# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 02:26:18 2022

@author: root
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def GeneralEquation(first_x,first_y,second_x,second_y):
    # 一般式 Ax+By+C=0
    A=second_y-first_y
    B=first_x-second_x
    C=second_x*first_y-first_x*second_y
    return A,B,C


def roll(srise):
    srise['x1']=srise['x'].rolling(window=25).mean()
    srise['y1']=srise['y'].rolling(window=25).mean()
    return srise

def dataclean(data):#数据清洗
    #数据滤波
    data=data.groupby([data['track_id']]).apply(roll)     
    data=data.dropna(axis=0)
    #数据集计
    data['time1']=data['time']*2 #影响到达识别
    data['time1']=data['time1'].astype(int)
    data=data.groupby([data['track_id'],data['time1'],data['lane_id'],data['type'],data['direction']]).mean()
    data=data.reset_index()
    data=data[data.lane_id<10]
    return data

def queshi1(df):
    # 定义3σ原则表达式
    clo=['x', 'y', 'speed', 'tan_acc', 'lat_acc','x1_diff' ]
    for cl in clo:
        min_mask = df[cl] < (df[cl].mean() - 3 *  df[cl].std())
        max_mask = df[cl] > (df[cl].mean() + 3 * df[cl].std())
    # 只要满足上诉表达式的任一个就为异常值，所以这里使用位与运算
        mask = min_mask | max_mask
        df.loc[mask,cl]=np.nan  
    return df

def queshi2(df):
    df=df.interpolate()
    return df

#==========数据准备==========
f = open(r'E:\1.0\new\3-1.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=dataclean(data)

#左机位
x1=351975.36
y1=3459528.50
x2=352001.13
y2=3459427.88

a,b,c=GeneralEquation(x1,y1,x2,y2)
data['range']=a*data['x']+b*data['y']+c
plt.plot([x1,x2],[y1,y2])
data['range1']=0
data.loc[data['range']<0,'range1']=1
data1=data.loc[data['range1']==1]



data1['x1_diff']=data1['x1'].diff()
data1=data1.groupby([data1['track_id']]).apply(queshi1)   
data1=data1.groupby([data1['track_id']]).apply(queshi2)  
data1=data1.dropna(axis=0, how='any')

f = open(r'E:\1.0\456\4.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] 
data=dataclean(data)

#右机位
x3=352131.71
y3=3459532.01
x4=352141.72
y4=3459492.30

a,b,c=GeneralEquation(x3,y3,x4,y4)
data['range']=a*data['x']+b*data['y']+c
plt.plot([x3,x4],[y3,y4])
data['range1']=0
data.loc[data['range']>0,'range1']=1
data2=data.loc[data['range1']==1]

#data2.time1=data2.time1+60
data2['x1_diff']=data2['x1'].diff()
data2=data2.groupby([data2['track_id']]).apply(queshi1)   
data2=data2.groupby([data2['track_id']]).apply(queshi2)  
data2=data2.dropna(axis=0, how='any')

#时间校准==手工
import math
def time_verify(i,j): #相同车辆不同轨迹ID time1
    line_1=data1[(data1.track_id==i)]
    line_2=data2[(data2.track_id==j)]
    s1=line_1[['time1','speed']]
    s2=line_2[['time1','speed']]
    over_rate=[]
    for i in range(-100,100):
        s3=s2.copy()
        s3['time1']=s3['time1']+i
        overlap=pd.merge(s1,s3,on=['time1'])
        overlap['over']=abs(overlap['speed_x']-overlap['speed_y'])
        over_r=overlap['over'].mean()
        if math.isnan(over_r) == True:
            over_r=100
        over_rate.append(over_r)
    plt.plot(over_rate)
    time_v=over_rate.index(min(over_rate))-100
    return time_v



time_v=time_verify(220,239)
#匹配
#测试代码 一对多
#筛选
data_t=data1[data1.direction==1]
data_copy = data2[data2.direction==1]




f = open(r'C:\Users\root\Desktop\轨迹拼接\3-4.xlsx','rb')
tid = pd.read_excel(f)
track_id=tid['p1_ID'].values

import time
import heapq 
import dwt

def dtw_main(data_t,data_copy,track_id):
    data_t = data_t.sort_values(by=['track_id','time'])
    data_copy = data_copy.sort_values(by=['track_id','time'])
    #data_copy=data_copy.iloc[100:,:]
    
    # line_1=line_1.sort_values(by='time1',ascending=True)
    # line_2=line_2.sort_values(by='time1',ascending=True)
    
    
    #时间窗口
    tra_t=data_t.time1.groupby([data_t['track_id']]).mean()
    tra_t=tra_t.reset_index()
    tra_t2=data_copy.time1.groupby([data_copy['track_id']]).mean()
    tra_t2=tra_t2.reset_index()
    tra_t2.loc[:,'time1']=tra_t2.loc[:,'time1'].values+time_v #确定范围
#    track_id=tra_t.track_id.unique()
    starttime = time.time()
    
    match=[]
    dtw=[]
    for i in track_id:
        line_1=data_t[data_t.track_id==i]
        if len(line_1)==0:
            continue
        t1=tra_t.loc[tra_t.track_id==i,'time1'].values
        line_range_id=tra_t2.loc[(tra_t2.time1>int(t1-30))&(tra_t2.time1<int(t1+30)),'track_id'].values
        #line_range_id=line_range_id[line_range_id!=i].values
        dwt_len=[]
        for j in line_range_id:
            line_2=data_copy[(data_copy.track_id==j)]
            line_2.loc[:,'time1']=line_2.loc[:,'time1'].values+time_v #确定范围
            # s1=line_1[['y1','x1_diff']][:-1].values
            # s2=line_2[['y1','x1_diff']][:-1].values
            s1=line_1[['time1','speed']].values[:-3,:]
            s2=line_2[['time1','speed']].values
    #        s1= pd.DataFrame(min_max.fit_transform(s1))#对数值变量min_max归一化
     #       s2= pd.DataFrame(min_max.fit_transform(s2))#对数值变量min_max归一化
            s1,s2=ini_point(s1,s2)
            if len(s1)<10 or len(s2)<10 or max(s1[:,0])+10<min(s2[:,0]) : #两条轨迹重合过短 没有重合 
                dwt_len.append(1000)
                continue
            l=dtw_distance1(s1,s2)[-1,-1] /(max(len(s1),len(s2)))
            dwt_len.append(l)
        if (len(dwt_len)==0) or min(dwt_len)>1.2:
            m=[i,np.nan]
            d=[i,np.nan]
        else:
            if np.diff(heapq.nsmallest(2, dwt_len))<0.3:
                k=list(map(dwt_len.index, heapq.nsmallest(2, dwt_len)))
                m=[i,line_range_id[k[0]],line_range_id[k[1]],min(dwt_len)]
            else:
                k=dwt_len.index(min(dwt_len))
                m=[i,line_range_id[k],0,min(dwt_len)]
    #        d=[i,heapq.nsmallest(3, dwt_len)]
        match.append(m)
    #    dtw.append(d)
    
    
    endtime = time.time()
    print('总共的时间为:', round(endtime - starttime, 2),'secs')
    
    
    match1=pd.DataFrame(match)     
    match1.columns=['p1_ID', 'p2_ID_m1','p2_ID_m2','dtw'] 
    return match1

#dtw_main(data_t,data_copy,track_id)

#min_mask = match1['dtw'] < (match1['dtw'].mean() + 3 * match1['dtw'].std())

# match1=pd.merge(match1,tid,on='p1_ID',how='inner')
# match1=match1.drop_duplicates()


# match1['test1']=(match1['p2_ID_m1']==match1['p2_ID']).values 
# match1['test2']=(match1['p2_ID_m2']==match1['p2_ID']).values 


# #=============待解决，取出理想值，还需要给出未匹配成功的值========

# ttcc=match1[match1.p2_ID_m2==match1.p2_ID]
# match1_0=match1[match1.p2_ID_m2==0]
# match1_1=match1[match1.p2_ID_m2>0]
# for i in range(len(match1_1)):
#     if any((match1_1.p2_ID_m2.values[i]==match1_0.p2_ID_m1).values):
#         match1_1.p2_ID_m2.iloc[i]=0   
#     if any((match1_1.p2_ID_m1.values[i]==match1_0.p2_ID_m1).values):
#         match1_1.p2_ID_m1.iloc[i]=match1_1.p2_ID_m2.iloc[i]
#         match1_1.p2_ID_m2.iloc[i]=0 

# # match1_3=match1_1[match1_1.p2_ID_m2!=0]
# # match1_4=match1_1[match1_1.p2_ID_m2==0]
# # for i in range(len(match1_3)):
# #     if any((match1_3.p2_ID_m2.values[i]==match1_4.p2_ID_m1).values):
# #         match1_3.p2_ID_m2.iloc[i]=0   
# #     if any((match1_3.p2_ID_m1.values[i]==match1_4.p2_ID_m1).values):
# #         match1_3.p2_ID_m1.iloc[i]=match1_3.p2_ID_m2.iloc[i]
# #         match1_3.p2_ID_m2.iloc[i]=0 

# match1_p1=match1.loc[:106]
# rate=(match1_p1[(match1_p1.test1==True)|(match1_p1.test2==True)].count())/len(match1_p1)
 
# t=match1_p1[match1_p1.test2==True]
# wro=match1_p1[match1_p1.test==False]