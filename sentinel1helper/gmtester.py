from meteostat import Stations, Daily, Point
import datetime as dt
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd
import numpy as np


in_file = '/media/data/dev/testdata/testn.csv'
in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
df = sh.gmdata(in_file)

ts = df.data.loc[0]
#
pick = 150

testdats = df.dt_dats
#testdats = pd.Series(testdats, dtype='object')
print(df.dt_dats)
for idx,i in df.data.iterrows():
    print('pause')
    f = i[testdats].values.astype('float')
    if idx == pick:
        ff = f
    ffit = np.polyfit(df.dt_dats_asDays, f,1)
    fval = np.polyval(ffit,df.dt_dats_asDays)
    print(i['PS_ID'],i['mean_velocity'], ffit[0]*365, idx)
# print(type(f))
ffit = np.polyfit(df.dt_dats_asDays, ff,1)
print(ffit)
fval = np.polyval(ffit,df.dt_dats_asDays)
print(df.data.columns)
print(i['mean_velocity'], ffit[0]*365)
#ts = ts[df.dats].to_numpy().astype('float')
print(df.find_first_cycle())
print(df.find_last_cycle())
print(df.data.tail())
plt.plot(df.dt_dats, ff)
plt.plot(df.dt_dats, fval)
plt.show()
#print(ts)