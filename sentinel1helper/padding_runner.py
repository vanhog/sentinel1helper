import sentinel1helper as sh1 
import sh1reader as sh1r 
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sg
from IPython.core.pylabtools import figsize


in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_layer = 'tl5_d_139_01_mscaoi'
out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
## REAL DATA###################################################################
# in_file = '/media/data/dev/testdata/testn.csv'
# in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
# in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_file = '~/data/dev/testdata/tl5_l2b_044_01_001-200.gpkg'
# in_layer = 'tl5_d_139_01_mscaoi'
# out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
in_layer = 'tl5_l2b_a_044_01_001200_mscaoi'
print('start reading')
# df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
gmdf = sh1.gmdata(df)
sent1AB = sh1.gmdata(gmdf.data.loc[:,gmdf.find_first_cycle():gmdf.find_last_cycle()])

r_tl = sent1AB.resample_timeline() # r_tl = resampled time line

def resample_ts(r_tl_asDays, tl_asDays, ts):
    r_ts = np.interp(r_tl_asDays, tl_asDays, ts)
    return r_ts

def filt_ts(ts, omega_g, fs):
    sos = sg.butter(3, omega_g, 'lp', fs=fs, output='sos')
    filtered = sg.sosfiltfilt(sos, erg)
    return filtered

def mv_from_lin_regression(in_ts, in_dt_dats_asDays):
    # supposed to become a measurement object's @property
    ts_diffs = []

    regval = np.polyfit(in_dt_dats_asDays, in_ts,1)

    return regval[0]*365

def get_mv_ts_from_lin_reg(in_ts, in_dt_dats_asDays):
    regval = np.polyfit(in_dt_dats_asDays, in_ts,1)
    valerg = np.polyval(regval, in_dt_dats_asDays)
    return valerg

pick = 75
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
    print(len(erg))
print(len(r_tl[0]), len(r_tl[1]))
print(filt_mv, gmdf.data.loc[pick]['mean_velocity'])

plt.figure(figsize=[16,9])
plt.plot(sent1AB.dt_dats, sent1AB.data.loc[i].values, ':', color='lightgray')
plt.plot(r_tl[0], erg, '.', color='crimson')
plt.plot(sent1AB.dt_dats, sent1AB.data.loc[i].values, '.', color='gray')
plt.plot(r_tl[0], filt_erg)
plt.plot(r_tl[0], mv_line)
plotdf = gmdf.data.to_crs(epsg=3857)
import contextily as cx
print(gmdf.data.crs, plotdf.crs)
fig, ax = plt.subplots()
xlim=([1100000, 1160000])
ylim=([7200000, 7240000])
ax.set_xlim(xlim)
ax.set_ylim(ylim)
mdf = plotdf.loc[[pick]]
plotdf.plot(ax=ax, alpha=0.5, edgecolor='k')

mdf.plot(ax=ax, color='red')
cx.add_basemap(ax)
plt.show()
print('happy day')