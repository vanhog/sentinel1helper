import sentinel1helper as sh1 
import sh1reader as sh1r 

from meteostat import Stations, Daily, Point
import datetime as dt
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd
import numpy as np


in_file = '/media/data/dev/testdata/testn.csv'
in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
#in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2a_aoi_msc_gpkg.gpkg'
#in_layer = 'tl5_l2a_a_044_02_mscaoi'
in_layer = 'tl5_a_117_02_mscaoi'
print('start reading')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
print('finished reading')
print(df.head())

gmdf = sh1.gmdata(df)

# fir= pd.Timestamp(df.find_first_cycle(6))
# lst= pd.Timestamp(df.find_last_cycle(6))
#
# a = df.data.loc[:,fir:lst]
# print(a.iloc[5])
ps_ges = gmdf.data['PS_ID']
sent1ges = gmdf.data[gmdf.dt_dats]
#sent1A = sent1ges[gmdf.dt_dats]
sent1A = sent1ges.loc[:,:gmdf.find_first_cycle()]
#sent1AB = gmdf.data[gmdf.dt_dats]
sent1AB = sent1ges.loc[:,gmdf.find_first_cycle():gmdf.find_last_cycle()]
print(ps_ges.iloc[0], np.mean(sent1ges.iloc[0].values),np.mean(sent1A.iloc[0].values), np.mean(sent1AB.iloc[0].values))

sent1A_mean     = []
sent1AB_mean    = []
sent1ges_mean   = []   

sent1A_var     = []
sent1AB_var    = []
sent1ges_var   = []    
# 
#     print(ps_ges.iloc[i], \
#           np.mean(sent1ges.iloc[i].values),\
#           np.mean(sent1A.iloc[i].values), \
#           np.mean(sent1AB.iloc[i].values))
for i in range(0,len(ps_ges)):
    sent1ges_mean.append(np.mean(sent1ges.iloc[i].values))
    sent1A_mean.append(np.mean(sent1A.iloc[i].values))
    sent1AB_mean.append(np.mean(sent1AB.iloc[i].values))
    sent1ges_var.append(np.var(sent1ges.iloc[i].values))
    sent1A_var.append(np.var(sent1A.iloc[i].values))
    sent1AB_var.append(np.var(sent1AB.iloc[i].values))
    
#sent1AB_var = np.array(sent1AB_var).tolist()
plt.hist(sent1ges_mean,bins=100, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
plt.hist(sent1AB_mean,bins=100, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
plt.hist(sent1A_mean,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
plt.legend()

plt.xlim([-50,50])
plt.title('mean')

plt.figure()
plt.hist(sent1ges_var,bins=600, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
plt.hist(sent1AB_var,bins=600, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
plt.hist(sent1A_var,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
plt.legend()
plt.xlim([0,200])
plt.title('var')
plt.show()          
print(type(gmdf), ' happy day')