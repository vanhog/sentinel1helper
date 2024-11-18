import sentinel1helper as sh1 
import sh1reader as sh1r 

from meteostat import Stations, Daily, Point
import datetime as dt
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde

## REAL DATA###################################################################
in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_layer = 'tl5_d_139_01_mscaoi'
out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
## REAL DATA###################################################################


## TEST DATA###################################################################

# in_file = '/media/data/dev/testdata/testn.csv'
# in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
# in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_file = '~/data/dev/testdata/tl5_l2b_044_01_001-200.gpkg'
in_file = '/home/hog/data/dev/testdata/tl5_l2b_044_01_random200.gpkg'

# in_layer = 'tl5_d_139_01_mscaoi'
# out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
in_layer = 'tl5_l2b_a_044_01_001200_mscaoi'
in_layer = 'A_117_02'
## TEST DATA###################################################################



def calc_new_meanDiff(in_ts, in_source_gmdf):
    ts_diffs = []
    for i, j in zip(in_ts[0:-1], in_ts[1:]):
        ts_diffs.append(float(j - i))
        
    ts_diff_days = in_source_gmdf.dt_dats_diffs

    mean_diff = sum([i * j for i, j in zip (ts_diffs, ts_diff_days)]) / sum(ts_diff_days)
    
    return mean_diff * 365


def mv_from_lin_regression(in_ts, in_dt_dats_asDays):
    # supposed to become a measurement object's @property
    ts_diffs = []

    regval = np.polyfit(in_dt_dats_asDays, in_ts, 1)

    return regval[0] * 365

def do_rmse_culling(in_ts, in_reference_gdmf, toplot=False):
    this_trend = polytrend(in_reference_gdmf.dt_dats_asDays, in_ts)
    culled_ts = []
    culled_tl = []
    trendfree_ts = [i-j for i,j in zip(in_ts, this_trend)]
    this_std = np.std(trendfree_ts)
    for i,j,k in zip(trendfree_ts, in_ts, in_reference_gdmf.dt_dats):
        if i > 1*this_std:
            next
        elif i < -1*this_std:
            next
        else:
            culled_ts.append(j)
            culled_tl.append(k)    
    culled_df = pd.DataFrame([culled_ts], columns=culled_tl)
    culled_gmdf = sh1.gmdata(culled_df)
    
    if toplot:
        plt.figure(figsize=[16,9])
        plt.plot([in_reference_gdmf.dt_dats[0], in_reference_gdmf.dt_dats[-1]], [this_std, this_std])
        plt.plot([in_reference_gdmf.dt_dats[0], in_reference_gdmf.dt_dats[-1]], [-this_std, -this_std])

        plt.plot(in_reference_gdmf.dt_dats, trendfree_ts, label='trendfree')
        plt.plot(culled_tl, culled_ts, '-o', color='red')
        
    return culled_gmdf


def do_peak_culling_f(in_ts, in_reference_gmdf, f=55.6, toplot=False):
    '''
    Es gibt einen guten Grund, die Spitzen nicht abzuschneiden:
    Wir wissen nämlich gar nicht, um was frü einen Scatterer es sich handelt:
    So'n ordentlicher SH-Silagehaufen wächst in 6 Tagen schon mal mehr als f/4 mm und 
    schrumpf ggf auch ebenso schnell. Besser drinlassen und zählen als Metakriterium.
    '''
    isPeaky = True
    
    ts_var = np.var(in_ts)
    ts_diffs = [float(in_ts.iloc[0])]
    for i, j in zip(in_ts[0:-1], in_ts[1:]):
        ts_diffs.append(float(j - i))
        
    print(ts_var)
    
    plt.figure(figsize=[16, 9])
    plt.stem(in_reference_gmdf.dt_dats, ts_diffs)
    plt.hlines(f / 4, in_reference_gmdf.dt_dats[0], in_reference_gmdf.dt_dats[-1])
    plt.hlines(-(f / 4), in_reference_gmdf.dt_dats[0], in_reference_gmdf.dt_dats[-1])
    cull_diffs = ts_diffs
    cull_std = np.std(cull_diffs)
    dummy_diffs = []
    
    mycolors = ['black', 'magenta', 'lime', 'orange', 'purple', 'yellow', 'cyan', 'turquoise', 'salmon', 'ivory', 'coral', 'crimson', 'lightgreen', 'khaki', 'tan']
    ccounter = 0
    while isPeaky:
        isPeaky = False
        for i in cull_diffs:
            #if i > (cull_std + f / 4):
            if i > f/4.:    
                dummy_diffs.append(i - f/4.)
                isPeaky = True
                print(i, f/4.)
            #elif i < -(cull_std + f / 4):
            elif i < (-f/4):
                dummy_diffs.append(i + f/4.)
                isPeaky = True
            else:
                dummy_diffs.append(i)
        cull_diffs = dummy_diffs
        dummy_diffs = []
        plt.stem(in_reference_gmdf.dt_dats, cull_diffs, linefmt=mycolors[ccounter])
        ccounter += 1
        print('ccounter:\t', ccounter)

    if toplot:
        
        plt.plot(in_reference_gmdf.dt_dats, in_ts, 'r') 

       # plt.plot(in_reference_gmdf.dt_dats, np.cumsum(culled_ts), 'g')
        plt.plot(in_reference_gmdf.dt_dats, np.cumsum(cull_diffs), 'purple')
       # plt.stem(in_reference_gmdf.dt_dats, culled_ts, 'y')
        plt.hlines(np.std(cull_diffs) + f / 2, in_reference_gmdf.dt_dats[0], in_reference_gmdf.dt_dats[-1])
        plt.hlines(-(np.std(cull_diffs) + f / 2), in_reference_gmdf.dt_dats[0], in_reference_gmdf.dt_dats[-1])
       # plt.hlines(std_diffs2+f/2, in_reference_gmdf.dt_dats[0], in_reference_gmdf.dt_dats[-1])
       # plt.hlines(-(std_diffs2+f/2), in_reference_gmdf.dt_dats[0], in_reference_gmdf.dt_dats[-1])
       # plt.stem(in_reference_gmdf.dt_dats, culled_ts2, 'orange')
       # #print(np.std(ts_diffs), np.mean(ts_diffs))
        z = np.zeros(10)
        zx= [i for i in range(0,10)]
       
        plt.figure(figsize=[16, 9])
        ts_culled_diff = []
        for i, j in zip(np.cumsum(cull_diffs), in_ts):
            ts_culled_diff.append(j - i)
        plt.stem(in_reference_gmdf.dt_dats, ts_diffs)
        plt.stem(in_reference_gmdf.dt_dats, ts_culled_diff, linefmt='khaki')
        plt.show()
    return np.cumsum(cull_diffs)

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

### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE### EXECUTE
print('start reading')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')

print('finished reading')
print(df.head(10))

gmdf = sh1.gmdata(df)
sent1AB = sh1.gmdata(gmdf.data.loc[:, gmdf.find_first_cycle():gmdf.find_last_cycle()])
bins = 25
mv  = []
omv = []
nmv = []
for i in range(0, len(sent1AB.data)):
    mv.append(gmdf.data.loc[i]['mean_velocity'])
    omv.append(mv_from_lin_regression(sent1AB.data.loc[i], sent1AB.dt_dats_asDays))
    
    rmse_ts = do_rmse_culling(sent1AB.data.loc[i], sent1AB, toplot=False)
    nmv.append(mv_from_lin_regression(rmse_ts.data.loc[0].values, rmse_ts.dt_dats_asDays))
 #   print(i, '\t', mv, '\t', omv, '\t', nmv)

print('happy day')

plt.figure(figsize=[16,9])
h, be = np.histogram(mv, bins=bins, density=True)
density_mv = gaussian_kde(mv)
xkde = np.linspace(min(be), max(be), num=200)
ykde = density_mv(xkde)
plt.plot(xkde, ykde, color='darkseagreen')
#plt.fill_between(xkde, ykde, color = 'mediumseagreen')

#homv, beomv = np.histogram(omv, bins=bins, density=True)
density_omv = gaussian_kde(omv)
ykde_omv = density_omv(xkde)
plt.plot(xkde, ykde_omv, color='orange')
#plt.fill_between(xkde, ykde_omv, color='aquamarine', alpha=0.5)

#hnmv, benmv = np.histogram(nmv, bins=bins, density=True)
density_nmv = gaussian_kde(nmv)
ykde_nmv = density_nmv(xkde)
plt.plot(xkde, ykde_nmv, color='lime')
#plt.fill_between(xkde, ykde_nmv, color='lime', alpha=0.5)

plt.xlim([min(be), max(be)])

plt.figure(figsize=[16,9])
plt.hist(nmv, bins=bins, density = True, histtype='stepfilled', color='cornflowerblue', label='rmse-culled mean velo')
#plt.hist(nmv, bins=bins, density = True, histtype='step', color='mediumblue', linewidth=2)

plt.hist(mv, bins=bins, density = True, histtype='step', color='orange', linewidth=2, label='mean_velocity')
plt.hist(omv, bins=bins, density = True, histtype='step', color='lime', linewidth=2, label='unculled mean velo')
plt.legend()
plt.show()
print('happier days')
