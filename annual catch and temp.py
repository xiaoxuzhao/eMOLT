# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 11:59:38 2018
annual catch and annual temp
@author: xiaoxu
"""
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import *
from pandas import read_csv
import datetime
#######################
#HARDCODE
year=range(2002,2018)
year_BD=[2002,2003,2004,2005,2007,2009,2010,2011,2015,2016,2017]
year_TS=[2007,2008,2009,2016,2017]
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
input_dir='/home/zdong/xiaoxu/emolt/files/'
file_BN='catch_temp_file_BN.csv' # catch data that JiM created &  emailed
file_BD='catch_temp_file_BD.csv'  #temp data
file_TS='catch_temp_file_TS.csv'
catch_colnum=12 # column number where "11' refers to lobster "kept"
date_colnum=6#column number where "11' refers to lobster "date"
temp_colnum=17
############################
df_BN=read_csv(input_dir+file_BN) # reads catch data
catch_BN=df_BN.icol(catch_colnum)# catch number
date_BN=df_BN.icol(date_colnum)#2000-09-15:08:43
temp_BN=df_BN.icol(temp_colnum)
catch_BN = [x /8.0000 for x in catch_BN]
df_BD=read_csv(input_dir+file_BD) # reads catch data
catch_BD=df_BD.icol(catch_colnum)# catch number
date_BD=df_BD.icol(date_colnum)#2000-09-15:08:43
temp_BD=df_BD.icol(temp_colnum)
catch_BD = [x /12.0000 for x in catch_BD]
df_TS=read_csv(input_dir+file_TS) # reads catch data
catch_TS=df_TS.icol(catch_colnum)# catch number
date_TS=df_TS.icol(date_colnum)#2000-09-15:08:43
temp_TS=df_TS.icol(temp_colnum)
catch_TS = [x /15.0000 for x in catch_TS]            
#################
mean_temp=[]
mean_catch=[]
for s in range(len(year)):
    te=[]
    ca=[]
    for i in range(len(date_BN)):
       if int(date_BN[i][0:4])==year[s]:
           te.append(temp_BN[i])
           ca.append(catch_BN[i])
    mean_temp.append(np.mean(te))
    mean_catch.append(np.mean(ca))
mean_temp_BD=[]
mean_catch_BD=[]
for s in range(len(year)):
    te=[]
    ca=[]
    for i in range(len(date_BD)):
       if int(date_BD[i][0:4])==year[s]:
           te.append(temp_BD[i])
           ca.append(catch_BD[i])
    mean_temp_BD.append(np.mean(te))
    mean_catch_BD.append(np.mean(ca))
c_BD=[]
t_BD=[]
for i in range(len(mean_temp_BD)):
    if np.isnan(mean_temp_BD[i]):
        print i
    else:
        c_BD.append(mean_catch_BD[i])
        t_BD.append(mean_temp_BD[i])
mean_temp_TS=[]
mean_catch_TS=[]
for s in range(len(year)):
    te=[]
    ca=[]
    for i in range(len(date_TS)):
       if int(date_TS[i][0:4])==year[s]:
           te.append(temp_TS[i])
           ca.append(catch_TS[i])
    mean_temp_TS.append(np.mean(te))
    mean_catch_TS.append(np.mean(ca))
c_TS=[]
t_TS=[]
for i in range(len(mean_temp_TS)):
    if np.isnan(mean_temp_TS[i]):
        print i
    else:
        c_TS.append(mean_catch_TS[i])
        t_TS.append(mean_temp_TS[i])
fig,ax1=plt.subplots()
ax1.plot(year,mean_catch,'--b',marker='*', markersize=10,linewidth=2)
#ax1.plot(year_BD,c_BD,'--b',marker='*', markersize=10,linewidth=2)
#ax1.plot(year_TS,c_TS,'--b',marker='*', markersize=10,linewidth=2)
ax1.set_xlabel('Date',fontsize=10)
# Make the y-axis label, ticks and tick labels match the line color.
ax1.set_ylabel('mean catch', color='b')
ax1.tick_params('y', colors='black')
ax2 = ax1.twinx()
ax2.plot(year,mean_temp, 'r-',linewidth=2)
#ax2.plot(year_BD,t_BD, 'r-',linewidth=2)
#ax2.plot(year_TS,t_TS, 'r-',linewidth=2)
ax2.set_ylabel('mean temperature', color='r')
ax2.tick_params('y', colors='black')
ax1.legend(['catch'],loc=2,fontsize=10)
ax2.legend(['temp'],loc=0,fontsize=10)
plt.title('mean catch vs mean temp at eMOLT site BN01')
plt.savefig(save_dir+"mean catch and mean temp and date BN01.png")
plt.show()      