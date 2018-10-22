# -*- coding: utf-8 -*-
"""
Created on Mon Aug 13 09:48:23 2018
plot BN01,BD01,TS02 study area
@author: xiaoxu
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from decimal import *
from pandas import read_csv
import conversions
from mpl_toolkits.basemap import Basemap 
##########################
#HARDCODES
save_dir='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
file_catch='sqldump_2018_07_BN.csv' # catch data that JiM created &  emailed
input_dir='/home/zdong/xiaoxu/emolt/files/'
file_temp_BN='this2.dat'  #temp data
file_temp_BD='BD01_temp.dat'
file_temp_TS='TS01_temp.dat'
variables=['year','year_day','temp','lat','lon','depth']#
df_BN=pd.read_csv(input_dir+file_temp_BN, names=variables, sep='\s+') # read temperature time series
df_BD=pd.read_csv(input_dir+file_temp_BD, names=variables, sep='\s+')
df_TS=pd.read_csv(input_dir+file_temp_TS, names=variables, sep='\s+')
lat_BD,lon_BD=[],[]
lat_BN,lon_BN=[],[]
lat_TS,lon_TS=[],[]
for i in range(len(df_BN)):
    la,lo=conversions.dm2dd(df_BN['lat'].values[i],df_BN['lon'].values[i])
    lat_BN.append(la)
    lon_BN.append(lo)
for i in range(len(df_BD)):
    la,lo=conversions.dm2dd(df_BD['lat'].values[i],df_BD['lon'].values[i])
    lat_BD.append(la)
    lon_BD.append(lo)
for i in range(len(df_TS)):
    la,lo=conversions.dm2dd(df_TS['lat'].values[i],df_TS['lon'].values[i])
    lat_TS.append(la)
    lon_TS.append(lo)    
fig = plt.figure()
a=fig.add_subplot(1,1,1)
my_map = Basemap(projection='merc', 
    resolution = 'h', area_thresh = 0.3,
     llcrnrlon=-72, llcrnrlat=41.0,
    urcrnrlon=-68.0, urcrnrlat=43.5) 
my_map.drawcoastlines()
my_map.drawcountries()
my_map.fillcontinents(color = 'grey')
my_map.drawmapboundary()
x1,y1=my_map(lon_BN,lat_BN)
my_map.plot(x1,y1, 'ro', markersize=12)
x2,y2=my_map(lon_BD,lat_BD)
my_map.plot(x2,y2, 'ro', markersize=12)
x3,y3=my_map(lon_TS,lat_TS)
my_map.plot(x3,y3, 'ro', markersize=12)
plt.text(x1[0], y1[0],'BN01',fontsize=15,fontweight='bold', ha='left',color='black')
plt.text(x2[0], y2[0],'BD01',fontsize=15,fontweight='bold', ha='left',color='black')
plt.text(x3[0], y3[0],'TS02',fontsize=15,fontweight='bold', ha='left',color='black')
plt.text(55279.5583607422,138227.88966818247 ,'Massachusetts',fontsize=10, ha='left',va='top',color='black')
plt.text(5279.5583607422,318227.88966818247 ,'New Hampshire',fontsize=10, ha='left',color='black')
a.set_title('sites location',fontsize=20)
my_map.drawparallels(np.arange(30,80,1),labels=[1,0,0,1])
my_map.drawmeridians(np.arange(-180,180,1),labels=[1,1,0,1])
plt.savefig(save_dir+'sites_location',dpi=200)
plt.show()