# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 12:31:24 2019

@author: 97837
"""

import numpy as np


#x=ts_a
#y=l22
def dist(x,y):   
    return np.sqrt(np.sum((x-y)**2,axis = 1))

# plt.plot(ts_a[:,0],ts_a[:,1])
# plt.plot(ts_b[:,0],ts_b[:,1])
 
# #ts_a=line_1[['y','x']].values
# #ts_b=line_2[['y','x']].values
# ts_a=s1
# ts_b=s2
def ini_point(ts_a, ts_b):
    l1,l2=ts_a[0,:],ts_b[0,:]
    if l1[0]<l2[0]:
        l22=np.tile(l2,(len(ts_a),1))
        l=list(dist(ts_a,l22))        
        t1=l.index(min(l))
        ts_a=ts_a[t1:,:]
    else:
        l11=np.tile(l1,(len(ts_b),1))
        l=list(dist(ts_b,l11))        
        t1=l.index(min(l))
        ts_b=ts_b[t1:,:]
        
    l1,l2=ts_a[-1,:],ts_b[-1,:]
    if l1[0]<l2[0]:
        l11=np.tile(l1,(len(ts_b),1))
        l=list(dist(ts_b,l11))        
        t2=l.index(min(l))
        ts_b=ts_b[:t2,:]
        
    else:
        l22=np.tile(l2,(len(ts_a),1))
        l=list(dist(ts_a,l22))        
        t2=l.index(min(l))
        ts_a=ts_a[:t2,:]
    return ts_a, ts_b
    
    
def dtw_distance(ts_a, ts_b, d=lambda x,y: abs(x-y), mww=10000):
# Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))
# Initialize the first row and column
    cost[0, 0] = d(ts_a[0], ts_b[0])
    for i in range(1, M):
        cost[i, 0] = cost[i-1, 0] + d(ts_a[i], ts_b[0])
    for j in range(1, N):
        cost[0, j] = cost[0, j-1] + d(ts_a[0], ts_b[j])
# Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i-mww), min(N, i + mww)):
            choices = cost[i-1, j-1], cost[i, j-1], cost[i-1, j]
            cost[i, j] = min(choices) + d(ts_a[i], ts_b[j])
# Return DTW distance given window
    return cost





def dist1(x,y):   
    return np.sqrt(np.sum((x-y)**2))

#ts_a=line_1[['y','x']]
#ts_b=line_2[['y','x']]
def dtw_distance1(ts_a, ts_b, mww=10000):
# Create cost matrix via broadcasting with large int
    ts_a, ts_b = np.array(ts_a), np.array(ts_b)
    M, N = len(ts_a), len(ts_b)
    cost = np.ones((M, N))
# Initialize the first row and column
    cost[0, 0] = dist1(ts_a[0,:], ts_b[0,:])
    for i in range(1, M):
        cost[i, 0] = cost[i-1, 0] + dist1(ts_a[i,:], ts_b[0,:])
    for j in range(1, N):
        cost[0, j] = cost[0, j-1] + dist1(ts_a[0,:], ts_b[j,:])
# Populate rest of cost matrix within window
    for i in range(1, M):
        for j in range(max(1, i-mww), min(N, i + mww)):
            choices = cost[i-1, j-1], cost[i, j-1], cost[i-1, j]
            cost[i, j] = min(choices) + dist1(ts_a[i,:], ts_b[j,:])
# Return DTW distance given window
    return cost
    