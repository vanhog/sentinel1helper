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

###in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
###in_layer = 'tl5_d_139_01_mscaoi'


#in_file = '~/data/dev/testdata/tl5_l2b_044_01_001-200.gpkg'


#in_file = '/home/hog/data/dev/testdata/tl5_l2b_a_117_02_random200.gpkg'
in_file     = '/media/hog/hogsandisc/data/mscthesisdata/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_layer    = 'tl5_d_139_01_mscaoi'

out_file    = in_file
out_layer   = 'tl5_d_139_01_mscaoi_Sent1ABfilt'
out_feature = 'nw_mw_f'
#out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'

print('start reading')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
print('finished reading')
print(df.head(10))

gmdf = sh1.gmdata(df)

sent1AB = sh1.gmdata(gmdf.data.loc[:,gmdf.find_first_cycle():gmdf.find_last_cycle()])


# def mv_from_lin_regression(in_ts, in_reference_gmdf):
#     # supposed to become a measurement object's @property
#     ts_diffs = []
#
#     regval = np.polyfit(in_reference_gmdf.dt_dats_asDays, in_ts,1)
#
#     return regval[0]*365


def mv_from_lin_regression(in_ts, in_dt_dats_asDays):
    # supposed to become a measurement object's @property
    ts_diffs = []

    regval = np.polyfit(in_dt_dats_asDays, in_ts, 1)

    return regval[0] * 365


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

def filt_ts_zero_padded(ts, omega_g, fs):
    half_length = int(len(ts)/2)
    listofzeros = [0]*half_length
    padded_ts = listofzeros + ts.tolist() + listofzeros
    sos = sg.butter(3, omega_g, 'lp', fs=fs, output='sos')
    filtered = sg.sosfiltfilt(sos, padded_ts)
    return_filtered = filtered[half_length:half_length+len(ts)]
    return return_filtered

def filt_ts_trend_padded(ts, omega_g, fs,trend_window=30):
    half_length = int(len(ts)/2)
    trend_span = trend_window
    listofzeros = [0]*half_length
    
    mean_before = np.mean(ts[0:trend_span])
    mean_after  = np.mean(ts[-trend_span:])
    
    t_before = np.polyfit(range(0,trend_span), ts[0:trend_span],1)
    t_after  = np.polyfit(range(0,trend_span), ts[-trend_span:],1)
    
    padd_before = [mean_before-(half_length-i)*t_before[0] for i in range(0,half_length)]
    padd_after  = [mean_after+i*t_after[0] for i in range(0,half_length)]
    padded_ts = padd_before + ts.tolist() + padd_after
    
    sos = sg.butter(3, omega_g, 'lp', fs=fs, output='sos')
    filtered = sg.sosfiltfilt(sos, padded_ts)
    return filtered[half_length:half_length+len(ts)]

def get_mv_ts_from_lin_reg(in_ts, in_dt_dats_asDays):
    regval = np.polyfit(in_dt_dats_asDays, in_ts,1)
    valerg = np.polyval(regval, in_dt_dats_asDays)
    return valerg




# Resample time line according to a 6-day revisiting frequency 
r_tl = sent1AB.resample_timeline() # r_tl = resampled time line

# Set destinct 
pick = 136



## MAIN LOOP ####################################################################
filts = []

for i in range(0,len(sent1AB.data)):
#for i in range(pick, pick+1):
    # Resample time series according to resampled time line r_tl, gaining r_ts
    r_ts = resample_ts(r_tl[1], sent1AB.dt_dats_asDays, sent1AB.data.loc[i].values)
    # Filtering
    #f_r_ts      = filt_ts(r_ts, 1/90., 1/6.)
    #f_r_ts_p    = filt_ts_padded(r_ts, 1/90., 1/6.)
    f_r_ts_pt   = filt_ts_trend_padded(r_ts, 1/90., 1/6., trend_window=90)
    # Calculate new mean velocity
    f_r_ts_pt_mv = mv_from_lin_regression(f_r_ts_pt, r_tl[1]) # CAREFULL
    
    filts.append(f_r_ts_pt_mv)

  
# plt.figure(figsize=(16,9))
# plt.plot(r_tl[0], r_ts, ':')
# #plt.plot(r_tl[0], f_r_ts_p, color='magenta', label='zero padded filtering')
# plt.plot(r_tl[0], f_r_ts_pt, color='green', label='trend padded filtering')
# #plt.plot(r_tl[0], f_r_ts, label='without padding' )
# plt.legend()
# plt.figure()
plt.hist(filts, bins=200)
plt.hist(gmdf.data['mean_velocity'], bins=200)
diffs = [i-j for i,j in zip(filts, gmdf.data['mean_velocity'])]
plt.figure()
plt.hist(diffs, bins=200)
#plt.show()
# plt.figure()
# plt.hist(filts, bins=200, histtype='step', color='crimson')
# plt.hist(nonfilts, bins=200, histtype='step', color='cornflowerblue')
# print(np.median(filts), np.median(nonfilts))

# Save Result
new_df = pd.DataFrame(filts, columns=[out_feature], index=gmdf.data.index)
new_gmdf = pd.concat([gmdf.data, new_df],axis=1)
print(new_gmdf.head(10))
print(new_gmdf.columns)
for i in new_gmdf.columns:
    new_gmdf = new_gmdf.rename(columns={i : str(i)})

# new_gmdf.to_file(out_file, \
#                  layer=out_layer,\
#                  driver='GPKG')
print(new_gmdf.columns)
print('most happy day')

plt.show()  
