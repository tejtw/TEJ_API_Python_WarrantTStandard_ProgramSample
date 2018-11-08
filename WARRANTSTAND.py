# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 16:18:36 2018

@author: zyx
"""
#pip install tejapi
#pip install matplotlib
#pip install numpy

import pandas as pd
import numpy as np
import tejapi
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
tejapi.ApiConfig.api_key = "GDEy0mWAGqnI3EemCREGREZMcEVbnF"

#%%查詢特定日期的股價與報酬率資料
sampledates = ['2018-10-11','2018-10-11']
data = tejapi.get('TWN/AOPTION',mdate={'gte':sampledates[0],'lte':sampledates[1]},opts={"sort":"mdate.desc",'columns':['coid','cashnm_c','mdate','rtime','acls','ex_price','aivolt']}, paginate=True)
tx_data = data.drop(data[(data['cashnm_c'] == "")].index)
tx_data['underlying'] = tx_data['cashnm_c'].str.split(" ").str[0]
#計算剩餘月數
tx_data['rtime_M'] = (tx_data['rtime']/12)
tx_data['rtime_M'] = tx_data['rtime_M'].astype(np.int)
#計算現貨與履約價比
tx_data['lns_k'] = tx_data['acls'] / tx_data['ex_price']
#只取出隱含波動度小於1的，開始繪圖
final = tx_data[(tx_data['rtime_M']==3)&(tx_data['aivolt']<1)&(tx_data['coid'].str.contains("P")==False)]
labels = final['underlying']
pd_labels = pd.DataFrame(final['underlying'].unique().tolist())
for pd_i in range(0,round(len(pd_labels)/10)):
    draw_start = pd_i*10
    draw_end = pd_i*10+10
    
    unique_labels = set(pd.Series(final['underlying'].unique()[draw_start:draw_end].tolist()))
    colors = [plt.cm.Spectral(each) for each in np.linspace(0, 1, len(unique_labels))]
    plt.figure(figsize=(20,15))
    ll=[]
    
    for k , col in zip(unique_labels, colors):
        class_member_mask = (labels == k)
        xy = final.loc[class_member_mask,['lns_k','aivolt']].values
        xy = xy[xy[:,0].argsort()]
        plt.plot(xy[:, 0], xy[:, 1],'.', linewidth=1, markerfacecolor=tuple(col),  markeredgecolor='k', markersize=15)
        lname = "underlying="+str(k)
        ll.append(mpatches.Patch(color=tuple(col), label=lname))
    plt.legend(handles=ll,loc='lower right',fontsize=12)
    plt.xlabel('price/strike')
    plt.ylabel('implied volatility')
    plt.show()