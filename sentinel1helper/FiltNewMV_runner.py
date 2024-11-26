import sentinel1helper as sh1 
import sh1reader as sh1r 

from meteostat import Stations, Daily, Point
import datetime as dt
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd
import numpy as np


# in_file = '/media/data/dev/testdata/testn.csv'
#in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
#in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_file = '~/data/dev/testdata/tl5_l2b_044_01_001-200.gpkg'
in_file = '/home/hog/data/dev/testdata/tl5_l2b_a_117_02_random200.gpkg'
#in_layer = 'tl5_d_139_01_mscaoi'
#out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
in_layer = 'A_117_02'
print('start reading')
#df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')

print('finished reading')
print(df.head(10))



def mv_from_lin_regression(in_ts, in_reference_gmdf):
    # supposed to become a measurement object's @property
    ts_diffs = []

    regval = np.polyfit(in_reference_gmdf.dt_dats_asDays, in_ts,1)

    return regval[0]*365

def polytrend(in_x, in_y):
    polyfunc = np.polyfit(in_x, in_y, 1)
    #print(polyfunc[0]*365)
    return np.polyval(polyfunc, in_x)

def resample_ts(r_tl_asDays, tl_asDays, ts):
    r_ts = np.interp(r_tl_asDays, tl_asDays, ts)
    return r_ts

def filt_ts(ts, omega_g, fs):
    sos = sg.butter(3, omega_g, 'lp', fs=fs, output='sos')
    filtered = sg.sosfiltfilt(sos, ts)
    return filtered


def get_mv_ts_from_lin_reg(in_ts, in_dt_dats_asDays):
    regval = np.polyfit(in_dt_dats_asDays, in_ts,1)
    valerg = np.polyval(regval, in_dt_dats_asDays)
    return valerg




gmdf = sh1.gmdata(df)
sent1AB = sh1.gmdata(gmdf.data.loc[:,gmdf.find_first_cycle():gmdf.find_last_cycle()])
r_tl = sent1AB.resample_timeline() # r_tl = resampled time line
pick = 15




erg = []
filt_erg = []
new_lin_mv = []
for i in range(pick,pick+1):
    print(sent1AB.data.loc[i].values)
    print(len(sent1AB.data.loc[i].values), len(sent1AB.dt_dats_asDays))
    erg = resample_ts(r_tl[1], sent1AB.dt_dats_asDays, sent1AB.data.loc[i].values)
    filt_erg = filt_ts(erg, 1./180, 1/6.)
    filt_mv  = mv_from_lin_regression(filt_erg, r_tl[1])
    mv_line  = get_mv_ts_from_lin_reg(filt_erg, r_tl[1])
    

## MAIN LOOP ####################################################################
new_lin_mv = []
for i in range(0,len(sent1AB.data)):
    new_lin_mv.append(mv_from_lin_regression(sent1AB.data.loc[i], \
                                             sent1AB))
    

## MAIN LOOP ####################################################################
print('happy day')

# for i,j in zip(gmdf.data['mean_velocity'], new_lin_mv):
#     print(i,j)
#
# new_df = pd.DataFrame(new_lin_mv, columns=['nw_mv'], index=gmdf.data.index)
# new_gmdf = pd.concat([gmdf.data, new_df],axis=1)
# #gmdf.data['new_mv'] = new_lin_mv
# print(new_gmdf.head(10))
# print(new_gmdf.columns)
# for i in new_gmdf.columns:
#     new_gmdf = new_gmdf.rename(columns={i : str(i)})
#
# new_gmdf.to_file(in_file, \
#                  layer=out_layer,\
#                  driver='GPKG')
# print(new_gmdf.columns)
# print('happy day')
