# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 01:02:04 2022

@author: root
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import time

def GeneralEquation(first_x,first_y,second_x,second_y): #线性函数
    # 一般式 Ax+By+C=0
    A=second_y-first_y
    B=first_x-second_x
    C=second_x*first_y-first_x*second_y
    return A,B,C


def roll(srise):#平滑
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
    return data


def split(x1,y1,x2,y2,x3,y3,x4,y4,data):#左边两点和右边两点
    a,b,c=GeneralEquation(x1,y1,x2,y2)
    data['range']=a*data['x']+b*data['y']+c
    plt.plot([x1,x2],[y1,y2])
    data['range1']=0
    data.loc[data['range']<0,'range1']=1
    data1=data.loc[data['range1']==1]
    a,b,c=GeneralEquation(x3,y3,x4,y4)
    data1['range']=a*data1['x']+b*data1['y']+c
    plt.plot([x3,x4],[y3,y4])
    data1['range1']=0
    data1.loc[data1['range']>0,'range1']=1
    data2=data1.loc[data1['range1']==1]
    return data2


def sequence(data2):#将数据转换为该方法基础数据
    data3=data2.drop_duplicates(['track_id'])
    # data3=data2.time1.groupby([data2['track_id'],data2['lane_id'],data2['type'],data2['direction']]).mean()
    # data3=data3.reset_index()
    # data3=data3.drop_duplicates(['track_id'])
    data3=data3.sort_values(by='time1',ascending=True)
    data3=data3.drop_duplicates(['time1','lane_id','direction'])#把同一时刻到达的车辆剔除，数据层面难以分出先后 等解决
    dt=data3[['time1','lane_id','direction','track_id']]
    return dt


def pick_match(lane_id,direction,dt): #dt待匹配的段
    df=dt.loc[(dt['lane_id']==lane_id)  & (dt['direction']==direction),:]
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
    return df

def se_match(mt):#匹配算法
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
    return mat1


#调用函数
f = open(r'E:\1.0\456\4.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] 
data=dataclean(data)
#画图
for i in range(5):
    line_=data[(data.track_id==i)&(data.direction==1)]
    plt.plot(line_['x'][:10],line_['y'][:10])
#右
x1=352072.8
y1=3459517.72
x2=352084.3
y2=3459475.45
#左
x3=352087.12
y3=3459518.39
x4=352098.8
y4=3459477.45
data2=split(x1,y1,x2,y2,x3,y3,x4,y4,data)
data2['lane_id']=data2['lane_id'].astype(int)
data2=data2[data2.lane_id<10]
#取出数据序列基础
#data3=data2.drop_duplicates(['track_id'])


dt4=sequence(data2)

f = open(r'E:\1.0\new\3-1.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=dataclean(data)
x1=352084.12
y1=3459515.56
x2=352095.21
y2=3459473.86
x3=352096.52
y3=3459518.62
x4=352108.07
y4=3459477.16
data2=split(x1,y1,x2,y2,x3,y3,x4,y4,data)
data2['lane_id']=data2['lane_id'].astype(int)
data2=data2[data2.lane_id<10]
dt3=sequence(data2)


#取出规定方向和车辆的数据
df4_11=pick_match(1,1,dt4)
df3_11=pick_match(1,1,dt3)

#筛选待匹配的数据
df4_11.loc[:,'time1']=df4_11.loc[:,'time1'].values+69
df3_111=df3_11.loc[(df3_11.time1>100) & (df3_11.time1<200),:]
df4_111=df4_11.loc[(df4_11.time1>100) & (df4_11.time1<200),:]


#合成seq
mt=np.array([df3_111['track_id'].values,df4_111['track_id'].values])

#匹配
mat1=se_match(mt)
mat1=mat1.drop_duplicates()