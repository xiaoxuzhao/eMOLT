# -*- coding: utf-8 -*-
"""
Created on Tue Sep 11 11:10:05 2018
seasonal monthly catch and temp
@author: xiaoxu zhao
"""
from datetime import datetime, timedelta
from pandas import Series
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import pandas as pd
from pandas import read_csv
import numpy as np
##########################
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file1='catch_temp_file_BN.csv' # catch data that JiM created &  emailed
file2='catch_temp_file_BD.csv'
file3='catch_temp_file_TS.csv'
input_dir='/home/zdong/xiaoxu/emolt/files/'
catch_colnum=12 # column number where "12' refers to lobster "kept"
date_colnum=6#column number where "6' refers to lobster "date"
trap_number1=8.0000
trap_number2=12.0000
trap_number3=15.0000
temp_colnum=17
t1='BN01'
t2='BD01'
t3='TS02'
#######################
df1=read_csv(input_dir+file1) # reads catch data
df2=read_csv(input_dir+file2)
df3=read_csv(input_dir+file3)
#dfh=read_csv(input_dir+tempfile)
tempp1=list(df1.icol(temp_colnum))
tcatch1=df1.icol(catch_colnum)# catch number
date1=df1.icol(date_colnum)#2000-09-15:08:43
catch1= [x/trap_number1 for x in tcatch1]
newdate1=[]
tempp2=list(df2.icol(temp_colnum))
tcatch2=df2.icol(catch_colnum)# catch number
date2=df2.icol(date_colnum)#2000-09-15:08:43
catch2= [x/trap_number2 for x in tcatch2]
newdate2=[]
tempp3=list(df3.icol(temp_colnum))
tcatch3=df3.icol(catch_colnum)# catch number
date3=df3.icol(date_colnum)#2000-09-15:08:43
catch3= [x/trap_number3 for x in tcatch3]
temp1,temp2,temp3=[],[],[]
for i in tempp1:
    temp1.append((i - 32) / 1.8)
for i in tempp2:
    temp2.append((i - 32) / 1.8)
for i in tempp3:
    temp3.append((i - 32) / 1.8)
newdate3=[]
for i in range(len(date1)):
    newdate1.append(datetime.strptime(date1[i],"%Y-%m-%d:%H:%M").replace(year=2000))
    # # puts all observations in the same year, 2000
for i in range(len(date2)):
    newdate2.append(datetime.strptime(date2[i],"%Y-%m-%d:%H:%M").replace(year=2000))
for i in range(len(date3)):
    newdate3.append(datetime.strptime(date3[i],"%Y-%m-%d:%H:%M").replace(year=2000))    
####################
h1=len(date1)
data1= {'catch':catch1,'temp':temp1}
dfh1=pd.DataFrame(data1,index=newdate1)
monthly_summary1 = pd.DataFrame()
monthly_summary1['catch']=dfh1.catch.resample('M')
monthly_summary1['temp']=dfh1.temp.resample('M')
mouthly_index1=['2000-01-31', '2000-02-29', '2000-03-31', '2000-04-30',
               '2000-05-31', '2000-06-30', '2000-07-31', '2000-08-31',
               '2000-09-30', '2000-10-31', '2000-11-30', '2000-12-31']
ne1=[]
for i in range(len(monthly_summary1.index)):
#    ne.append(datetime.strptime(monthly_summary.index[i],"%Y-%m-%d").month)
     ne1.append(datetime.strptime(mouthly_index1[i],"%Y-%m-%d").month+datetime.strptime(mouthly_index1[i],"%Y-%m-%d").day/30.00)
#####################
h2=len(date2)
data2= {'catch':catch2,'temp':temp2}
dfh2=pd.DataFrame(data2,index=newdate2)
monthly_summary2 = pd.DataFrame()
monthly_summary2['catch']=dfh2.catch.resample('M')
monthly_summary2['temp']=dfh2.temp.resample('M')
mouthly_index2=['2000-05-31', '2000-06-30', '2000-07-31', '2000-08-31',
               '2000-09-30', '2000-10-31', '2000-11-30']
ne2=[]
for i in range(len(monthly_summary2.index)):
#    ne.append(datetime.strptime(monthly_summary.index[i],"%Y-%m-%d").month)
     ne2.append(datetime.strptime(mouthly_index2[i],"%Y-%m-%d").month+datetime.strptime(mouthly_index2[i],"%Y-%m-%d").day/30.00)
#######################
h3=len(date3)
data3= {'catch':catch3,'temp':temp3}
dfh3=pd.DataFrame(data3,index=newdate3)
monthly_summary3 = pd.DataFrame()
monthly_summary3['catch']=dfh3.catch.resample('M')
monthly_summary3['temp']=dfh3.temp.resample('M')
mouthly_index3=['2000-05-31', '2000-06-30', '2000-07-31', '2000-08-31',
               '2000-09-30', '2000-10-31', '2000-11-30']
ne3=[]
for i in range(len(monthly_summary3.index)):
#    ne.append(datetime.strptime(monthly_summary.index[i],"%Y-%m-%d").month)
     ne3.append(datetime.strptime(mouthly_index3[i],"%Y-%m-%d").month+datetime.strptime(mouthly_index3[i],"%Y-%m-%d").day/30.00)
#####################     
fig=plt.figure()
ax1=fig.add_subplot(3,1,1)
ax2=fig.add_subplot(3,1,1)
ax1.plot(ne1,monthly_summary1['catch'],'b-',linewidth=2)
#ax1.set_xlabel('Month',fontsize=12)
#ax1.set_ylabel('weekly catch', color='b')
ax2 = ax1.twinx()
ax2.plot(ne1,monthly_summary1['temp'],'r-',linewidth=2)
#ax2.set_ylabel('weekly temperature', color='r')
ax1.set_xlim(0,13)
ax1.text(1.5,1.0,t1+' total number of hauls'+':'+str(h1),fontsize=12)
plt.title('monthly mean catch vs mean temp at eMOLT site ')
###########################
ax1=fig.add_subplot(3,1,2)
ax1.plot(ne2,monthly_summary2['catch'],'b-',linewidth=2)
ax1.set_xlabel('Month',fontsize=12)
ax1.set_ylabel('monthly catch (lobster/pot)', color='b')
ax2 = ax1.twinx()
ax2.plot(ne2,monthly_summary2['temp'],'r-',linewidth=2)
ax2.set_ylabel(u'monthly temperature(°C)', color='r')
ax1.set_xlim(0,13)
ax1.text(1.5,1.0,t2+' total number of hauls'+':'+str(h2),fontsize=12)
###############################
ax1=fig.add_subplot(3,1,3)
ax1.plot(ne3,monthly_summary3['catch'],'b-',linewidth=2)
ax1.set_xlabel('Month',fontsize=12)
#ax1.set_ylabel('weekly catch', color='b')
ax2 = ax1.twinx()
ax2.plot(ne3,monthly_summary3['temp'],'r-',linewidth=2)
#ax2.set_ylabel('weekly temperature', color='r')
ax1.set_xlim(0,13)
ax1.text(1.5,1.0,t3+' total number of hauls'+':'+str(h3),fontsize=12)
plt.savefig(save_dir+"monthly mean catch and mean temp and date.png")
plt.show()      
