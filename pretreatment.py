# -*- coding: utf-8 -*-
"""
Created on Fri Aug 17 12:35:40 2018
Pretreatment dataset
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
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
input_dir='/home/zdong/xiaoxu/emolt/files/'
file_catch= 'sqldump_2018_01_BD.csv'#'sqldump_2018_07_BN.csv'#'sqldump_2018_01_BD.csv'#'sqldump_2018_01_TS.csv'
file_temp='BD01_temp.dat'  #this2.dat#'BD01_temp.dat' #'TS01_temp.dat'
catch_colnum=11 # column number where "11' refers to lobster "kept"
date_colnum=5#column number where "11' refers to lobster "date"
haul=12.0000#12.0000#15.0000
r='BD'    #BN#BD#TS
############################
df_catch=read_csv(input_dir+file_catch) # reads catch data
tcatch=df_catch.icol(catch_colnum)# catch number
date=df_catch.icol(date_colnum)#2000-09-15:08:43
variables=['year','year_day','temp','lat','lon','depth']#
df_temp=pd.read_csv(input_dir+file_temp, names=variables, sep='\s+') # read temperature time series
temp=df_temp["temp"]
tyear=df_temp["year"]
tyear_d=df_temp["year_day"]
catch = [x /haul for x in tcatch]            
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
for s in range(len(catch)):
        print s
        Temp=[]
        for i in range(len(temp)):
           if int(date[s][0:4])==tyear[i] and cyear_d[s]<=round(tyear_d[i],4)<cyear_d[s+1]:
               #match year and year_day
               Temp.append(temp[i])
        std_temp.append(np.std(pd.Series(Temp)))
        mean_temp.append(np.mean(Temp))#creates mean temperature on the day he hauled
#mean_temp.append(np.nan)
std_temp.append(np.std(pd.Series(Temp)))
mean_temp.append(np.mean(Temp))
temp=pd.Series(mean_temp)
df_catch['mean temp'] = temp
for i in df_catch.index:
     if np.isnan(df_catch['mean temp'][i]):
         df_catch.drop(i, inplace=True)
df_catch.to_csv(input_dir+'catch_temp_file_'+r+'.csv')

