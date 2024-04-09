# -*- coding: utf-8 -*-
"""
Created on Sun Oct 16 18:38:56 2022

@author: root
"""


import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import pylab as mpl  #导入中文字体，避免显示乱码
mpl.rcParams['font.sans-serif']=['SimHei']  #设置为黑体字

#======拼接轨迹=======

f = open(r'C:\Users\root\Desktop\轨迹拼接\算法匹配\tot1.xlsx','rb')
data_ = pd.read_excel(f)

# import random
# l=np.linspace(1,len(data_),len(data_))
# random.shuffle(l)
# data_['p1_id']=l
# random.shuffle(l)
# data_['p2_id']=l
# random.shuffle(l)
# data_['p3_id']=l
# random.shuffle(l)
# data_['p4_id']=l

#读取数据
path = r"E:\1.0\new\\"
files = os.listdir(path)
files = ['1-1.csv',  '1-2.csv', '2-1.csv',  '2-2.csv',  '3-1.csv',  '3-2.csv',  '3-3.csv', '4-1.csv']


track=pd.DataFrame()
track['pic1']=['1-2','2-2','3-2','3-3','5-2','5-3','5-4']
track['track_s']=[18419, 24600,21521,28814,7497,15800,24124]
data123=pd.DataFrame()
dirdata=[]
for fi in range(len(files)):
    f = open(path+files[fi],'rb')
    data = pd.read_csv(f,encoding = 'GB2312')
    # data1=data[data.time<1000]
    data1= data
    #时间集计
    data1['time1']=data1['time']/2
    data1['time1']=data1['time1'].astype(int)
    data1=data1.drop_duplicates(['track_id','time1','lane_id','type','direction'])
    data1=data1.reset_index()


    p_id='p'+files[fi][0]+'_ID'
    #p_id2='p'+files[fi][0]+'_id'
    data1['pic1']=files[fi][:3]
    

    data1=pd.merge(data1,track,on=['pic1'],how='left')
    data1=data1.fillna(0)
    data1['track_ids']=data1['track_id']+data1['track_s']
    
    data_list=data_[[p_id,'t_id']]
    data1=pd.merge(data1,data_list,left_on=('track_ids'),right_on=(p_id),how='left')
    #data1=data1.rename(columns={p_id2:'tr_id_rdm'}) 
#    dirdata.append(len(data1[data1.direction==1]))
#    dirdata.append(len(data1[data1.direction==0]))
    data1=data1.dropna(axis=0, how='any')
    data123=data123.append(data1)
    print(files[fi])
    #print(max(data1.track_id))


#f = open(r'E:\1.0\data123.csv','rb')
#data123 = pd.read_csv(f,encoding = 'GB2312')

#-----------时间拼接------------------
time_l=pd.DataFrame()
time_l['pic1']=['1-2','2-2','3-2','3-3']
time_l['time_s']=[6137.6, 9940.68,6051.32,8620.6]
data123=pd.merge(data123,time_l,on=['pic1'],how='left')
data123=data123.fillna(0) 
data123['time_after']=data123['time']+data123['time_s']