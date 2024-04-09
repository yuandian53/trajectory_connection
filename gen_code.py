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

i,j=19108,11935
#=time_verify(data1,data2,i,j)
line_1=data1[(data1.track_id==i)]
line_2=data2[(data2.track_id==j)]
line_1=line_1.sort_values(by='time',ascending=True)
line_2=line_2.sort_values(by='time',ascending=True)
#line_2.loc[:,'time1']=line_2.loc[:,'time1'].values+time_v
s1=line_1[['time5','x1_diff']].values[3:,:]
s2=line_2[['time5','x1_diff']].values[3:-3,:]
plt.plot(s1[:,0],s1[:,1])
plt.plot(s2[:,0],s2[:,1])

plot_l(i,j,data1,data2)

def plot_l(i,j,data1,data2):
    time_v=time_verify(data1,data2,i,j)
    line_1=data1[(data1.track_id==i)]
    line_2=data2[(data2.track_id==j)]
    line_1=line_1.sort_values(by='time',ascending=True)
    line_2=line_2.sort_values(by='time',ascending=True)
    line_2.loc[:,'time5']=line_2.loc[:,'time5'].values+time_v
    s1=line_1[['time5','x1_diff']].values[3:-3,:]
    s2=line_2[['time5','x1_diff']].values[3:-3,:]
    #s1= min_max.fit_transform(s1)#对数值变量min_max归一化
    #s2= min_max.fit_transform(s2)#对数值变量min_max归一化
    s1,s2=ini_point(s1,s2)
    dt=dtw_distance1(s1,s2)
    i,j = len(s1)-1,len(s2)-1
    #最短路径
    # print i,j
    p,q = [i],[j]
    while(i>0 or j>0):
        choice=dt[i-1, j-1], dt[i, j-1], dt[i-1, j]
        tb = np.argmin(choice)
        if tb==0 :
            i-=1
            j-=1
        elif tb==1 :
            j-=1
        else:
            i-=1
        p.insert(0,i)
        q.insert(0,j)
    trace=list(zip(p,q))
    plt.imshow(dt.T)
    plt.show()
    print(dt[-1,-1]/(max(len(s1),len(s2))))
    
    plt.plot(s1[:,0],s1[:,1])
    plt.plot(s2[:,0],s2[:,1])
    for i in range(len(q)):
        plt.plot([s1[p,0],s2[q,0]],[s1[p,1],s2[q,1]],color='black')
    return

plt.plot(s1[:,0],s1[:,1])
plt.plot(s2[:,0],s2[:,1])
#===============序列匹配的数据=============
f = open(r'E:\1.0\456\4.csv','rb')
data = pd.read_csv(f,encoding = 'GB2312')
data=data[data.time<6200] #筛选出数据
data=dataclean(data)
#画图
for i in range(5):
    line_=data[(data.track_id==i)&(data.direction==1)]
    plt.plot(line_['x'][:10],line_['y'][:10])
#左
x1=352072.8
y1=3459517.72
x2=352084.3
y2=3459475.45
#右
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


#==========DTW数据准备==========
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


#===============1方向===============
#时间校验==人工
time_v=time_verify(data1,data2, 12514,7597)
time_v=time_verify(data1,data2, 12517,7721)
#取出规定方向和车辆的数据
import time
#关闭警告
pd.set_option('mode.chained_assignment', None)
starttime = time.time()
 
result=pd.DataFrame()
for j in range(1,3):
    df4_11=pick_match(j,1,dt4)
    df3_11=pick_match(j,1,dt3)
    df4_11.loc[:,'time1']=df4_11.loc[:,'time1'].values+time_v1
    data_copy=data2.loc[(data2['direction']==1),:].copy()
    for k in range(102):
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
        rate1=(mat1_iden.test1[(mat1_iden.test1==True)].count())/len(mat1_iden) #匹配率
        rate2=(mat1.p1_ID[(mat1.p2_ID_m_list!=0)].count())/len(mat1) #匹配率
        if rate2<0.4 or rate1<0.4:
            print(str(j)+"车道"+str(k)+'min之后匹配不上')
            break
        else:
            mat1['time1']=k
            mat1['lane_id']=j
            result=result.append(mat1)
    result['direction']=1
    
endtime = time.time()
print('总共的时间为:', round(endtime - starttime, 2),'secs')        

i=8899
j=5318
line_1=data_t[data_t.track_id==i]
line_2=data_copy[data_copy.track_id==j]
s1=line_1[['time1','speed']].values[:-3,:]
s2=line_2[['time1','speed']].values
s1,s2=dwt.ini_point(s1,s2)
if len(s1)<8 or len(s2)<8 or max(s1[:,0])+10<min(s2[:,0]) : #两条轨迹重合过短 没有重合 
    dwt_len.append(1000)
    continue
l=dwt.dtw_distance1(s1,s2)[-1,-1] /(max(len(s1),len(s2)))
dwt_len.append(l)

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
re['lane_id']=j
re['direction']=1
re['time1']=k
#补上

for j in range(1,3):
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
    re['lane_id']=j
    re['direction']=1
    re['time1']=k
    #填上去
    re_buch=re.dropna(axis=0, how='any', inplace=False) 
    result=result.append(re_buch)
result.loc[ pd.isnull(result.p2_ID_m_list),'p2_ID_m_list']=result.loc[pd.isnull(result.p2_ID_m_list),'p2_ID_m1']           
#time_v=time_verify(data1,data2,6118,3436)

#处理result  
result=result[result.time1<=k]
result=result[result.p2_ID_m_list!=-1]
result_final=result[['p1_ID','p2_ID_m_list','lane_id','direction','time1']]
result_final.to_csv(r'E:\1.0\Stitching\result'+str(1)+"方向"+str(k)+'min.csv')  


#===============0方向===============
10245,6016
11842,7093
10442,6106
12087,7209
12517,7721
time_v=time_verify(data2,data1,6124,10484)  
time_v=time_verify(data2,data1,6016,10245)  
time_v=time_verify(data2,data1,7721,12517)  

starttime = time.time()
 

result=pd.DataFrame()
for j in range(1,3):
    df4_11=pick_match(j,0,dt3)
    df3_11=pick_match(j,0,dt4)
    df4_11.loc[:,'time1']=df4_11.loc[:,'time1'].values+time_v
    data_copy=data1.loc[ (data1['direction']==0),:]
    for k in range(87,100):
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
        rate2=(mat1.p1_ID[(mat1.p2_ID_m_list!=0)].count())/len(mat1)
        if rate2<0.3 or rate<0.2:
            print(str(0)+"方向"+str(j)+"车道"+str(k)+'min之后匹配不上')
            break
        else:
            mat1['time1']=k
            mat1['lane_id']=j
            result=result.append(mat1)  
    result['direction']=0
    
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
    re['lane_id']=j
    re['direction']=0
    re['time1']=k
    return re

j=1
re=check(j,k)


#补上

for j in range(1,3):
    re=check(j,k)
    #填上去
    re_buch=re.dropna(axis=0, how='any', inplace=False) 
    result=result.append(re_buch)
result.loc[ pd.isnull(result.p2_ID_m_list),'p2_ID_m_list']=result.loc[pd.isnull(result.p2_ID_m_list),'p2_ID_m1']
#处理result  
result=result[result.time1<=k]

result_final=result[['p1_ID','p2_ID_m_list','lane_id','direction','time1']]
result_final.to_csv(r'E:\1.0\Stitching\result'+str(0)+"方向"+str(k)+'min.csv')  