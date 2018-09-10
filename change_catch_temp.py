# -*- coding: utf-8 -*-
"""
Created on Tue Aug 14 13:16:13 2018

@author: xiaoxu 
"""
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import *
from pandas import read_csv
from sklearn import datasets, linear_model
from sklearn.linear_model import LinearRegression
##########################
def get_r2_numpy(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return r_squared
###########################
#HARDCODES
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file_catch='catch_temp_file_TS.csv' # catch data that JiM created &  emailed
input_dir='/home/zdong/xiaoxu/emolt/files/'
catch_colnum=12 # column number where "11' refers to lobster "kept"
date_colnum=6#column number where "11' refers to lobster "date"
temp_colnum=17
run_average=5#80
t='TS02'
#########################
df=read_csv(input_dir+file_catch) # reads catch data
tcatch=df.icol(catch_colnum)# catch number
date=df.icol(date_colnum)#2000-09-15:08:43
temp=df.icol(temp_colnum)
catch = [x /15.0000 for x in tcatch]  #12#15          
#################)
####################
change_temp=np.diff(temp)#create change_temp
change_t=list(change_temp)
change_catch=np.diff(catch)#create change_catch
Ct=np.array(change_temp)
Cc=np.array(change_catch)
X=Ct.reshape(len(Ct),1)
Y=Cc.reshape(len(Cc),1)
X_train = X[:-150]
X_test = X[-150:]
Y_train = Y[:-150]
Y_test = Y[-150:]
r=round(get_r2_numpy(Ct,Cc),4)
fig = plt.figure()
a=fig.add_subplot(1,1,1)
regr = linear_model.LinearRegression()
regr.fit(X_train, Y_train)
plt.scatter(Ct, Cc,  color='black')
plt.plot(X_test, regr.predict(X_test), color='red',linewidth=3)
plt.title('change catch vs temperature at eMOLT site '+str(t))
plt.ylabel('change_catch',fontsize=10)
plt.xlabel(u'change_temperature(℃)',fontsize=10)
plt.legend(['R**2='+str(r)],loc=2,fontsize=10)
plt.savefig(save_dir+"plot_changecatch_changetemperature "+str(t)+".png")
plt.show()
