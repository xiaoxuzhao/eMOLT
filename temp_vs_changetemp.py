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
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file='catch_temp_file_BD.csv' # catch data that JiM created &  emailed
input_dir='/home/zdong/xiaoxu/emolt/files/'
catch_colnum=12 # column number where "11' refers to lobster "kept"
date_colnum=6#column number where "11' refers to lobster "date"
haul_number=12.0000
temp_colnum=17
d=5
t='BD01'
#########################
def get_r2_numpy(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    r_squared = 1 - (sum((y - (slope * x + intercept))**2) / ((len(y) - 1) * np.var(y, ddof=1)))
    return r_squared
############################
df=read_csv(input_dir+file) # reads catch data
tcatch=df.icol(catch_colnum)# catch number
date=df.icol(date_colnum)#2000-09-15:08:43
temp=df.icol(temp_colnum)
catch = [x /haul_number for x in tcatch]
####################
change_temp=list(np.diff(temp))#create change_temp
change_catch=list(np.diff(catch))
Mt=np.array(change_temp)
Cc=np.array(change_catch)
###################
#p value
X=Mt.reshape(len(Mt),1)#len(Mt)
Y=Cc.reshape(len(Cc),1)
X2 = sm.add_constant(Mt)
est = sm.OLS(Cc, X2)
p=est.fit().f_pvalue
#######################
X_train = X[:-250]
X_test = X[-250:]
Y_train = Y[:-250]
Y_test = Y[-250:]
r=round(get_r2_numpy(Mt[:20],Cc[:20]),4)
fig = plt.figure()
a=fig.add_subplot(1,1,1)
regr = linear_model.LinearRegression()
regr.fit(X_train, Y_train)
plt.plot(change_temp,change_catch, 'o', markersize=6)
plt.plot(X_test, regr.predict(X_test), color='red',linewidth=3)
plt.ylabel('lobster/pot',fontsize=10)
plt.xlabel(u'change temperature (℉)',fontsize=10)
plt.title('catch catch vs change temperature at eMOLT site '+str(t) )
plt.legend(['catch','r**2='+str(r)],loc=2,fontsize=10)
plt.savefig(save_dir+"plot_change_catch_vs_change_temperature "+str(t)+".png")
plt.show()

