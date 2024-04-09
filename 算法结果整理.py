# -*- coding: utf-8 -*-
"""
Created on Tue Jan  3 19:19:37 2023

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

#读取数据
path = "C:\\Users\\root\\Desktop\\轨迹拼接\\算法匹配\\read_file\\"
files = os.listdir(path)



track=pd.DataFrame()
track['pic']=['1-2','2-2','3-2','3-3','5-2','5-3','5-4']
track['track_s']=[18419, 24600,21521,28814,7497,15800,24124]
data123=pd.DataFrame()
dirdata=[]
for fi in range(len(files)):
    f = open(path+files[fi],'rb')
    data = pd.read_excel(f)
    data=pd.merge(data,track,left_on=['p5_file'], right_on = ['pic'],how='left')
    data=pd.merge(data,track,left_on=['p6_file'], right_on = ['pic'],how='left')
    data=data.fillna(0)
    
    data['p6_ID'] = data['p6_ID'] - data['track_s_y']
    data['p5_ID'] = data['p5_ID'] - data['track_s_x']
    
    data = data[['p6_ID', 'p5_ID', 'lane_id', 'direction', 'time1', 'p5_file', 'p6_file']]
    
    
    data1 = pd.DataFrame()
    time_list = data.time1.unique()
    
    for t in time_list:
        data2 = data[data.time1 == t]
        
        data3 = data2[(data2.direction == 0) & (data2.lane_id == 3)][['p6_ID','p5_ID']].reset_index(drop = True)
        data3 = data3.rename(columns={"p6_ID": "p6_ID_0_3", "p5_ID": "p5_ID_0_3"})
        data4 = data2[(data2.direction == 0) & (data2.lane_id == 2)][['p6_ID','p5_ID']].reset_index(drop = True)
        data4 = data4.rename(columns={"p6_ID": "p6_ID_0_2", "p5_ID": "p5_ID_0_2"})
        data3 = pd.concat([data3,data4],axis=1)
        
        data4 = data2[(data2.direction == 0) & (data2.lane_id == 1)][['p6_ID','p5_ID']].reset_index(drop = True)
        data4 = data4.rename(columns={"p6_ID": "p6_ID_0_1", "p5_ID": "p5_ID_0_1"})
        data3 = pd.concat([data3,data4],axis=1)
        data4 = data2[(data2.direction == 1) & (data2.lane_id == 1)][['p6_ID','p5_ID']].reset_index(drop = True)
        data4 = data4.rename(columns={"p6_ID": "p6_ID_1_1", "p5_ID": "p5_ID_1_1"})
        data3 = pd.concat([data3,data4],axis=1)
        data4 = data2[(data2.direction == 1) & (data2.lane_id == 2)][['p6_ID','p5_ID']].reset_index(drop = True)
        data4 = data4.rename(columns={"p6_ID": "p6_ID_1_2", "p5_ID": "p5_ID_1_2"})
        data3 = pd.concat([data3,data4],axis=1)
        
        data4 = data2[(data2.direction == 1) & (data2.lane_id == 3)][['p6_ID','p5_ID']].reset_index(drop = True)
        data4 = data4.rename(columns={"p6_ID": "p6_ID_1_3", "p5_ID": "p5_ID_1_3"})
        data3 = pd.concat([data3,data4],axis=1)
        
        
        data3['time1'] = t
        
        
        data1 = data1.append(data3)
   
    data1['p5_file'] = '5-4'
    data1['p6_file'] = '6-0'
    # data1.loc[data1.time1 <165,'p1_file'] = '1-2'
    # data1.loc[data1.time1 <165,'p2_file'] = '2-1'
    data1.loc[data1.time1 <135,'p5_file'] = '5-3'
    data1.loc[data1.time1 <90,'p5_file'] = '5-2'
    data1.loc[data1.time1 <43,'p5_file'] = '5-1'
    # data1.loc[data1.time1 <103,'p1_file'] = '2-1'
    data1.to_excel(r"C:\Users\root\Desktop\轨迹拼接\算法匹配\校验结果修正\5&6_al_v.xlsx")