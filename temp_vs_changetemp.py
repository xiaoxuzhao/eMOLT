# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 13:44:33 2018

@author: xiaoxu zhao
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
file_catch='sqldump_2018_07_BN.csv' # catch data that JiM created &  emailed
input_dir='/home/zdong/xiaoxu/emolt/files/'
file_temp='this2.dat'  #temp data
catch_colnum=11 # column number where "11' refers to lobster "kept"
date_colnum=5#column number where "11' refers to lobster "date"
haul_number=8.0000
degree_number=1
#########################
#the functoin of mean average
def window_average(a, n=1):
    average=[]
    for i in range(len(a)):
        t=[]
        for s in range(len(a)):
            if a[i]-n<=a[s]<=a[i]+n:
               t.append(a[s])
        average.append(np.mean(t))
    return average
#########################
df_catch=read_csv(input_dir+file_catch) # reads catch data
tcatch=df_catch.icol(catch_colnum)# catch number
date=df_catch.icol(date_colnum)#2000-09-15:08:43
variables=['year','year_day','temp','lat','lon','depth']#
df_temp=pd.read_csv(input_dir+file_temp, names=variables, sep='\s+') # read temperature time series
temp=df_temp["temp"]
tyear=df_temp["year"]
tyear_d=df_temp["year_day"]
catch = [x /haul_number for x in tcatch]            
#################
#change catch datetime to year_day
cyear_d=[]
for i in range(0,len(date)):
     day=datetime.datetime.strptime(date[i],"%Y-%m-%d:%H:%M").timetuple().tm_yday  # gets yearday
     h=(Decimal(datetime.datetime.strptime(date[i],"%Y-%m-%d:%H:%M").hour+Decimal((datetime.datetime.strptime(date[i],"%Y-%m-%d:%H:%M").minute))/60))/24
     cyear_d.append(round((day+h),4))     
#################
# create mean temp 
mean_temp,std_temp,Temp=[],[],[]
s=0
for i in range(len(temp)):
           if int(date[s][0:4])==tyear[i] and cyear_d[s]==round(tyear_d[i],4):
               #match year and year_day
               Temp.append(temp[i])
std_temp.append(np.std(pd.Series(Temp)))
mean_temp.append(np.mean(Temp))#creates mean temperature on the day he hauled
for s in range(1,len(catch)-1):
        print s
        Temp=[]
        for i in range(len(temp)):
           if int(date[s][0:4])==tyear[i] and cyear_d[s]<=round(tyear_d[i],4)<=cyear_d[s+1]:
               #match year and year_day
               Temp.append(temp[i])
        std_temp.append(np.std(pd.Series(Temp)))
        mean_temp.append(np.mean(Temp))#creates mean temperature on the day he hauled
s=len(catch)-1
Temp=[]
for i in range(len(temp)):
           if int(date[s][0:4])==tyear[i] and cyear_d[s]==round(tyear_d[i],4):
               #match year and year_day
               Temp.append(temp[i])
std_temp.append(np.std(pd.Series(Temp)))
mean_temp.append(np.mean(Temp))
####################
change_temp=np.diff(mean_temp)#create change_temp
change_t=list(change_temp)
change_t.append(np.nan)#should have the same number of the catch
change_catch=np.diff(catch)#create change_catch
data2= {'change_t':change_t,'catch':list(catch)}
fig2=pd.DataFrame(data2)
f2=fig2.dropna().sort('change_t')
fig = plt.figure()
a=fig.add_subplot(1,1,1)
plt.plot(change_t,catch, 'o', markersize=6)
c_av=window_average(list(f2.catch), n=degree_number)
mt_av=window_average(list(f2.change_t),n=degree_number)
plt.plot(mt_av,c_av,"r",linewidth=2)
plt.ylabel('pounds/pot',fontsize=10)
plt.xlabel(u'change temperature (℃)',fontsize=10)
plt.title('catch vs change temperature at eMOLT site BN01')
plt.legend(['catch','mean average'],loc=2,fontsize=10)
plt.savefig(save_dir+"plot_catch_vs_change_temperature.png")
plt.show()

