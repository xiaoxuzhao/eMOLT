# -*- coding: utf-8 -*-
"""
Created on Mon Jul 23 12:10:19 2018
emolt temp vs catch
@author: xiaoxu
"""
import datetime
import matplotlib.pyplot as plt
import matplotlib.path as mpath
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
date_colnum=5#column number where "11' refers to lobster "kept"
run_average=3

#########################
#the functoin of mean average
def moving_average(a, n=3) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n
#########################
df_catch=read_csv(input_dir+file_catch) # reads catch data
catch=df_catch.icol(catch_colnum)# catch number
date=df_catch.icol(date_colnum)#2000-09-15:08:43
variables=['year','year_day','temp','lat','lon','depth']#
df_temp=pd.read_csv(input_dir+file_temp, names=variables, sep='\s+') # read temperature time series
temp=df_temp["temp"]
tyear=df_temp["year"]
tyear_d=df_temp["year_day"]            
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
#create change_temp
change_temp=[]
for i in range(len(mean_temp)):
    change_temp.append(mean_temp[i]-mean_temp[i-1])
#####################
#create change_catch
change_catch=[]
for i in range(len(catch)):
    change_catch.append(list(catch)[i]-list(catch)[i-1])
####################
#sorted data
mt_n,mt_e,catch_mt,ct_n,st_n,cc_n=[],[],[],[],[],[]
catch_ct,catch_st=[],[]
for i in range(len(mean_temp)):
     if np.isnan(mean_temp[i]):
         print i
     else:
         mt_n.append(mean_temp[i])
         catch_mt.append(catch[i])
for i in range(len(change_temp)):
     if np.isnan(change_temp[i]):
         print i
     else:
         ct_n.append(change_temp[i])
         catch_ct.append(catch[i])
         cc_n.append(change_catch[i])
for i in range(len(std_temp)):
     if np.isnan(std_temp[i]):
         print i
     else:    
         st_n.append(std_temp[i])
         catch_st.append(catch[i])
#####################
#catch vs average_temperature
fig = plt.figure()
a=fig.add_subplot(4,1,1)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(mean_temp,catch, 'o', marker=cut_star, markersize=10)
c_av =moving_average(catch_mt, n=run_average)
mt_av=moving_average(mt_n, n=run_average)
plt.plot(sorted(mt_av),sorted(c_av),"r")
plt.ylabel('catch',fontsize=10)
plt.xlabel('average_temperature',fontsize=10)
########################
#catch vs change_temperature
a=fig.add_subplot(4,1,2)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(change_temp,catch,'o', marker=cut_star, markersize=10)
c_av = moving_average(catch_ct, n=run_average)
ct_av=moving_average(ct_n, n=run_average)
plt.plot(sorted(ct_av),sorted(c_av),"r")
plt.ylabel('catch',fontsize=10)
plt.xlabel('change_temperature',fontsize=10)
##########################
#catch vs std_temperature
a=fig.add_subplot(4,1,3)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(sorted(std_temp),catch, 'o', marker=cut_star, markersize=10)
c_av = moving_average(catch_st, n=run_average)
st_av=moving_average(st_n,n=run_average)
plt.plot(sorted(st_av),sorted(c_av),"r")
plt.ylabel('catch',fontsize=10)
plt.xlabel('std_temperature',fontsize=10)
#########################
#change_catch vs change_temperature 
a=fig.add_subplot(4,1,4)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(sorted(change_temp),change_catch, 'o', marker=cut_star, markersize=10)
cc_av = moving_average(cc_n,n=run_average)
ct_av=moving_average(ct_n,n=run_average)
plt.plot(sorted(ct_av),sorted(cc_av),"r")
plt.ylabel('change_catch',fontsize=10)
plt.xlabel('change_temperature',fontsize=10)
plt.savefig(save_dir+"plot_catch_temperature.png")
plt.show()
