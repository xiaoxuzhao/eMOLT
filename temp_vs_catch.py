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
date_colnum=5#column number where "5" refers to date column
run_average=5 #number of samples to perform a running average over
#########################
#the functoin of mean average
def runningMean(x, N): # where did this come from?  What is your reference?
    y = np.zeros((len(x),))
    for ctr in range(len(x)):
         y[ctr] = np.sum(x[ctr:(ctr+N)])
    return y/N
#########################
df_catch=read_csv(input_dir+file_catch) # reads catch data
catch=df_catch.icol(catch_colnum)# catch number
date=df_catch.icol(date_colnum)#2000-09-15:08:43
variables=['year','year_day','temp','lat','lon','depth']# columns in the temp time series
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
# the following for loop appears to calculate mean temperature on just the first day of catch dataset 
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
           max_t=max(cyear_d[s],cyear_d[s+1])# why call this "max_t" and not "max_yd"
           min_t=min(cyear_d[s+1],cyear_d[s])
           if int(date[s][0:4])==tyear[i] and min_t<=round(tyear_d[i],4)<=max_t:  # why not just use cyear_d[s] and cyear_d[s+1] 
               #match year and year_day
               Temp.append(temp[i])
        std_temp.append(np.std(pd.Series(Temp)))# why not just Temp?
        mean_temp.append(np.mean(Temp))#creates mean temperature on the day he hauled
# the following for loop appears to calculate mean temperature on just the last day of catch dataset 
# but I'm not sure why it is needed
s=len(catch)-1 # s is already used as a variable in the for-loop
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
#####################
#sorted data
mt=sorted(mean_temp)
c=sorted(catch)
ct=sorted(change_temp)
cc=sorted(change_catch)
st=sorted(std_temp)
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
y_av = runningMean(c, run_average)
x_av=runningMean(mt, run_average)
plt.plot(x_av,y_av,"r")
plt.ylabel('catch')
plt.xlabel('average_temperature')
########################
#catch vs change_temperature
a=fig.add_subplot(4,1,2)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(change_temp,catch,'o', marker=cut_star, markersize=10)
y_av = runningMean(c, run_average)
x_av=runningMean(ct, run_average)
plt.plot(x_av,y_av,"r")
plt.ylabel('catch')
plt.xlabel('change_temperature')
##########################
#catch vs std_temperature
a=fig.add_subplot(4,1,3)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(std_temp,catch, 'o', marker=cut_star, markersize=10)
y_av = runningMean(c, run_average)
x_av=runningMean(st, run_average)
plt.plot(x_av,y_av,"r")
plt.ylabel('catch')
plt.xlabel('std_temperature')
#########################
#change_catch vs change_temperature 
a=fig.add_subplot(4,1,4)
star = mpath.Path.unit_regular_star(6)
circle = mpath.Path.unit_circle()
verts = np.concatenate([circle.vertices, star.vertices[::-1, ...]])
codes = np.concatenate([circle.codes, star.codes])
cut_star = mpath.Path(verts, codes)
plt.plot(change_temp,change_catch, 'o', marker=cut_star, markersize=10)
y_av = runningMean(c, run_average)
x_av=runningMean(ct, run_average)
plt.plot(x_av,y_av,"r")
plt.ylabel('change_catch')
plt.xlabel('change_temperature')
plt.savefig(save_dir+"plot_catch_temperature.png")
plt.show()
