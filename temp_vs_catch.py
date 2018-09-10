# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 12:10:19 2018
emolt temp vs catch
@author: xiaoxu
"""
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import *
from pandas import read_csv
##########################
#HARDCODES
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file='catch_temp_file_BD.csv' # catch data that JiM created &  emailed
input_dir='/home/zdong/xiaoxu/emolt/files/'
catch_colnum=12 # column number where "11' refers to lobster "kept"
date_colnum=6#column number where "11' refers to lobster "date"
temp_colnum=17
run_average_1=6#80
run_average_2=3
t='BD01'
d1=3
d2=1
#########################
#the functoin of mean average
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
#########################
def get_r2_numpy(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return r_squared
########################
df=read_csv(input_dir+file) # reads catch data
tcatch=df.icol(catch_colnum)# catch number
date=df.icol(date_colnum)#2000-09-15:08:43
temp=df.icol(temp_colnum)
catch = [x /12.0000 for x in tcatch]                
#################
# create mean temp
change_temp=np.diff(temp)#create change_temp
change_temp=list(change_temp)
change_temp.append(list(temp)[-1]-list(temp)[0])
change_catch=np.diff(catch)#create change_catch
change_catch=list(change_catch)
change_catch.append(list(catch)[-1]-list(catch)[0])
#####################
soak=[]
ca=[]
for s in range(len(year)):
      for i in range(1,len(date)):
           if  datetime.datetime.strptime(date[i-1],"%Y-%m-%d:%H:%M").year==year[s] and datetime.datetime.strptime(date[i],"%Y-%m-%d:%H:%M").year==year[s]:
               print i
               soak.append((datetime.datetime.strptime(date[i],"%Y-%m-%d:%H:%M")-datetime.datetime.strptime(date[i-1],"%Y-%m-%d:%H:%M")).days) 
               ca.append(catch[i])
data= {'soa':soak,'c':ca}
fig=pd.DataFrame(data)
f=fig.dropna().sort('soa')
ms=[]
mc=[]
s=0
while s<max(f['soa']):#max(f['soa'])
  m=[]
  c=[]
  for i in range(len(f['soa'])):
     if s<=f['soa'][i]<s+d2:
           m.append(f['soa'][i])
           c.append(f['c'][i])
  ms.append(np.mean(m))
  mc.append(np.mean(c))
  s=s+0.5
mean_soak=[]
mean_catch=[]
for i in range(len(ms)):
    if np.isnan(ms[i]):
        print i
    else:
        mean_soak.append(ms[i])
        mean_catch.append(mc[i])
########################
data1= {'mean_temp':temp,'catch':list(catch)}
fig1=pd.DataFrame(data1)
f1=fig1.dropna().sort('mean_temp')
data2= {'change_temp':change_temp,'catch':list(catch)}
fig2=pd.DataFrame(data2)
f2=fig2.dropna().sort('change_temp')
data3= {'change_temp':change_temp,'change_catch':list(change_catch)}
fig3=pd.DataFrame(data3)
f3=fig3.dropna().sort('change_temp')
#####################
#catch vs average_temperature
fig = plt.figure()
a=fig.add_subplot(3,1,1)
plt.plot(temp,catch, 'o', markersize=6)
c_av =moving_average(list(f1.catch), n=run_average_1)
mt_av=moving_average(list(f1.mean_temp),n=run_average_1)
plt.plot(mt_av,c_av,"r",linewidth=2)
plt.ylabel('lobster/pot',fontsize=10)
plt.xlabel(u'Mean temperature (℉)',fontsize=10)
plt.title('catch vs temperature at eMOLT site '+ str(t))
plt.legend(['catch',str(run_average_1)+' moving average'],loc=2,fontsize=10)
########################
#catch vs change_temperature
ms=[]
mc=[]
s=min(change_temp)
while s<max(change_temp):
  m=[]
  c=[]
  for i in range(len(change_temp)):
     if s<=change_temp[i]<s+d1:
           m.append(change_temp[i])
           c.append(catch[i])
  ms.append(np.mean(m))
  mc.append(np.mean(c))
  s=s+0.5
a=fig.add_subplot(3,1,2)
plt.plot(change_temp,catch,'o', markersize=6)
plt.plot(ms,mc,"r",linewidth=2)
#c_av = moving_average(list(f2.catch), n=run_average)
#ct_av=moving_average(list(f2.change_temp), n=run_average)
#plt.plot(ct_av,c_av,"r",linewidth=2)
plt.ylabel('lobster/pot',fontsize=10)
plt.xlabel(u'change_temperature(℉)',fontsize=10)
plt.legend(['catch',str(d1)+' degree average'],loc=2,fontsize=10)

#########################
a=fig.add_subplot(3,1,3)
plt.plot(soak,ca,'o', markersize=6)
plt.plot(mean_soak,mean_catch,"r",linewidth=2)
plt.ylabel('lobster/pot',fontsize=10)
plt.xlabel('soak time',fontsize=10)
plt.legend(['soak time(days)',str(d2)+' days average'],loc=0,fontsize=10)
plt.savefig(save_dir+"plot_catch_temperature "+str(t)+".png")
plt.show()
