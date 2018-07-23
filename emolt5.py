# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 09:27:33 2018

Created on Tue Jan 10 09:59:33 2012
Routine to look at plot temperature vs catch
modeled after emolt.m phase 5
@author: jmanning 
Huimin modified in Jan 2018 to allow good time lables on zoom in
Jim and Xiaoxu noticed in July 2018 that users need the "conversions" and "utilties" modules in the same directory
"""
from datetime import datetime as dt
import pylab as plt
import pandas as pd
from matplotlib.dates import num2date,DateFormatter
import conversions 
import utilities
import csv
import numpy

##### HARDCODES ################################  
wvar='kept' # options are 'kept','total','eggers', 'shorts', ... although I haven't coded the last two yet
days=7
hrs=days*24
sc='BN'
depset='01' # this is actually the site code "depset" is a bad name 
numpeople=1
numhauls=4# number to smooth over
smoothing_method='flat' #alternatively 'hanning' but that doesn't work in 6/16
#fileprefix='/net/data5/jmanning/fish/lobster/mela/sqldump_2018_01_' # catch data
fileprefix='sqldump_2018_07_' # catch data
#input_directory='/net/home3/ocn/jmanning/sql/'# the path to temperature file
#output_fig_directory='/net/pubweb_html/epd/ocean/MainPage/lob/'#the path of saving figure
output_fig_directory='/home/zdong/xiaoxu/emolt/figure/'#the path of saving figure
input_directory='/home/zdong/xiaoxu/emolt/files/'
ylim=(38.0,72.0)
xlim=(0.0,10.0)
n=20
s=2
####################################################
def getcatch(filen,dp,wvar,numhauls):
  #where "dp" is the site code
  #where "wvar" can be "kept", "total","shorts", or "eggers"
  #returns haul,hauls,datetc where "hauls" is the smoothed version and "datetc" is the datetime  
  catch=csv.reader(open(filen,'r'), delimiter=',', quotechar='|',skipinitialspace=True)
  haul,datetc=[],[]
  for row in catch:
      if (row[2]==dp) and len(row):
        if wvar=='kept':
            haul.append(float(row[11])/float(row[10]))# normalizes by number of traps per trawl (comma separated data)
        elif wvar=='total': # as needed in Bill Doherty's case, for example
            if  row[12]=='':
                row[12]=0
            if  row[13]=='':
                row[13]=0
            haul.append((float(row[11])+float(row[12])+float(row[13]))/float(row[10]))# normalizes by number of traps per trawl (comma separated data)
        dd=row[5] #datetime 
        datetc.append(dt(int(dd[0:4]),int(dd[5:7]),int(dd[8:10]),int(dd[11:13]),int(dd[14:16]),0))
  #sort this according to time?
  haul=numpy.array(haul).transpose()  
  if numhauls>2:
    haul_smooth=utilities.smooth(haul,numhauls,'hanning')
    difflen=len(haul_smooth)-len(haul)
    hauls=haul_smooth[difflen/2:-difflen/2]
  else:
    hauls=haul  
  return haul,hauls,datetc
  # plotting the catch
  #..how best to plot as in "skiphole.m" maybe using scikits ... 
fig=plt.figure(1,figsize=(8,6))
for k in range(numpeople):
    ax1=fig.add_subplot(numpeople,1,k+1)
    # Now go get the temperature data associated with this site
    # pipe = subprocess.Popen(["perl", "/home3/ocn/jmanning/sql/gettsll_justtemp.plx","sc","depset"
    # this subprocess was not possible ... I need to learn how to run Oracle from python
    variables=['year','year_day','temp','lat','lon','depth']
    df=pd.read_csv(input_directory+'this2.dat', names=variables, sep='\s+')
    #t=ml.load('/net/home3/ocn/jmanning/sql/this2.dat') old way of loading
    lat,lon,datet=[],[],[]
    for j in range(len(df)):
      #la,lo=conversions.dm2dd([t[j,3]],[t[j,4]]) #changed this in May 2015
      la,lo=conversions.dm2dd(df['lat'].values[0],df['lon'].values[0])
      lat.append(la)
      lon.append(lo)
      if df['year_day'].values[j]+1<366.0:
        #datet.append(num2date(t[j,1]+1).replace(year=int(t[j,0])))
        datet.append(num2date(df['year_day'].values[j]+1).replace(year=int(df['year'].values[j])))
      else:
        #datet.append(num2date(t[j,1]+1).replace(year=int(t[j,0])+1))
        datet.append(num2date(df['year_day'].values[j]+1).replace(year=int(df['year'].values[j]+1)))  
    #wd=t[:,5]
    #temp=t[:,2] 
    #temp_smooth=utilities.smooth(temp,24*7,'hanning')
   
    wd=df['depth'].values
    temp=df['temp'].values
    temp_smooth=utilities.smooth(temp,hrs,smoothing_method)
    #ax1.plot_date(datet,temp,'k-')
    temp_s=temp_smooth[hrs/2-1:-hrs/2]
    ax1.plot_date(datet[s:n],temp_s[s:n],'r-',linewidth=1.5)
    ax1.plot_date(datet[n:],temp_s[n:],'r-',linewidth=1.5)
    ax1.set_ylabel(str(days)+' day running average temperature (degF)',color='r',fontsize=16)
    ax1.set_ylim(ylim)
    haul,haul_smooth,datetc=getcatch(input_directory+fileprefix+sc+'.csv',sc+depset,wvar,numhauls)
    ax2=ax1.twinx()
    ax2.plot(datetc[s:n],haul_smooth[s:n],'g-',linewidth=1.5)
    ax2.plot(datetc[n:],haul_smooth[n:],'g-',linewidth=1.5)
    ax2.set_ylabel(str(numhauls)+' haul average catch/pot',color='g',fontsize=16)
    #ax2.set_ylim(xlim)
    
    #ax2.xaxis.set_major_locator(yrsl)
    #ax2.xaxis.set_major_formatter(majfmt)
    #ax2.xaxis.set_major_formatter(Fmt)
    
    #plt_fullmoon(datetc[-1].year,min(haul_smooth),max(haul_smooth))
    #plt_fullmoon(datetc[-1].year-1,min(haul_smooth),max(haul_smooth))
    #ax2.xaxis.set_major_locator(mondays)
    #ax2.set_xlabel(str(datet[-1].year))
    plt.title('Lobsters '+wvar+' and temperature at '+sc+depset,fontsize=16)
  
fig.autofmt_xdate() #slants the dates
print "saving plot _raw file... "
plt.savefig(output_fig_directory+sc+depset+'_'+wvar+'_'+str(numhauls)+'.ps')# for postscript
plt.savefig(output_fig_directory+sc+depset+'_'+wvar+'_'+str(numhauls)+'.png')
#os.system('lpr '+output_fig_directory+sc+depset+'_'+wvar+'_'+str(numhauls)+'.ps')   
plt.show()  
