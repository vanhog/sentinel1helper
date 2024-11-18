import sentinel1helper as sh1 
import sh1reader as sh1r 

from meteostat import Stations, Daily, Point
import datetime as dt
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd
import numpy as np
from IPython.core.pylabtools import figsize

## REAL DATA###################################################################
in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_layer = 'tl5_d_139_01_mscaoi'
out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
## REAL DATA###################################################################

# in_file = '/media/data/dev/testdata/testn.csv'
# in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
# in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_file = '~/data/dev/testdata/tl5_l2b_044_01_001-200.gpkg'
in_file = '/home/hog/data/dev/testdata/tl5_l2b_044_01_random200.gpkg'

# in_layer = 'tl5_d_139_01_mscaoi'
# out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
in_layer = 'tl5_l2b_a_044_01_001200_mscaoi'
in_layer = 'A_117_02'

print('start reading')
# df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')

print('finished reading')
print(df.head(10))


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


gmdf = sh1.gmdata(df)
sent1AB = sh1.gmdata(gmdf.data.loc[:, gmdf.find_first_cycle():gmdf.find_last_cycle()])
r_tl = sent1AB.resample_timeline() # r_tl = resampled time line

# print(mv_from_lin_regression(sent1AB.data.loc[15], sent1AB), gmdf.data.loc[15]['mean_velocity'], \
#       np.polyfit(sent1AB.dt_dats_asDays, sent1AB.data.loc[15],1)[0]*365)
# plt.figure()
# plt.plot(sent1AB.dt_dats, sent1AB.data.loc[15])
# plt.show()

# for i in range(0,len(sent1AB.data)):
pick = 15
#for i in range(75,76):
for i in range(pick, pick+1):
    culled_ts = do_peak_culling_f(sent1AB.data.loc[i], sent1AB, toplot=False)



erg = []
filt_erg = []
new_lin_mv = []
for i in range(pick,pick+1):
    print(sent1AB.data.loc[i].values)
    print(len(sent1AB.data.loc[i].values), len(sent1AB.dt_dats_asDays))
    erg = resample_ts(r_tl[1], sent1AB.dt_dats_asDays, sent1AB.data.loc[i].values)
    cullerg = resample_ts(r_tl[1], sent1AB.dt_dats_asDays, culled_ts) 
    filt_erg = filt_ts(erg, 1./180, 1/6.)
    filt_mv  = mv_from_lin_regression(filt_erg, r_tl[1])
    filt_cullerg = filt_ts(cullerg, 1/180., 1/6.)
    mv_line  = get_mv_ts_from_lin_reg(filt_erg, r_tl[1])
    

print(len(r_tl[0]), len(r_tl[1]))
print(filt_mv, gmdf.data.loc[pick]['mean_velocity'])

plt.figure(figsize=[16,9])

plt.plot(sent1AB.dt_dats, sent1AB.data.loc[pick].values,'gray')
plt.plot(r_tl[0], erg, 'lightblue')
plt.plot(r_tl[0], filt_ts(erg, 1./180, 1/6.), 'b')
plt.plot(r_tl[0], polytrend(r_tl[1], filt_ts(erg, 1/180., 1/6.)), label='unculled')


plt.plot(r_tl[0], cullerg,':r')
plt.plot(r_tl[0], filt_ts(cullerg, 1/180., 1/6.), 'pink')
plt.plot(r_tl[0], polytrend(r_tl[1], filt_ts(cullerg, 1/180., 1/6.)), label='culled')
plt.legend()

plt.figure(figsize=[16,9])
plt.plot(sent1AB.dt_dats, sent1AB.data.loc[pick].values)
this_rmse_culled_ts = do_rmse_culling(sent1AB.data.loc[pick], sent1AB, toplot=False)
plt.plot(this_rmse_culled_ts.dt_dats, this_rmse_culled_ts.data.values[0],'o')
plt.plot(this_rmse_culled_ts.dt_dats, polytrend(this_rmse_culled_ts.dt_dats_asDays, this_rmse_culled_ts.data.values[0]))
plt.plot(sent1AB.dt_dats, polytrend(sent1AB.dt_dats_asDays, sent1AB.data.loc[pick].values), 'r.')
#plt.show()
print('happy day')

for i in range(0, len(sent1AB.data)):
    mv = gmdf.data.loc[i]['mean_velocity']
    omv = mv_from_lin_regression(sent1AB.data.loc[i], sent1AB.dt_dats_asDays)
    
    rmse_ts = do_rmse_culling(sent1AB.data.loc[i], sent1AB, toplot=False)
    nmv = mv_from_lin_regression(rmse_ts.data.loc[0].values, rmse_ts.dt_dats_asDays)
    print(i, '\t', mv, '\t', omv, '\t', nmv)
#
print('happier days')
# WHAT ABOUT THE FREQUENY SPECTRUM

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
# # fir= pd.Timestamp(df.find_first_cycle(6))
# # lst= pd.Timestamp(df.find_last_cycle(6))
# #
# # a = df.data.loc[:,fir:lst]
# # print(a.iloc[5])
# # ps_ges = gmdf.data['PS_ID']
# # mv_ges = gmdf.data['mean_velocity']
# # sent1ges = gmdf.data[gmdf.dt_dats]
# # #sent1A = sent1ges[gmdf.dt_dats]
# # sent1A = sent1ges.loc[:,:gmdf.find_first_cycle()]
# # #sent1AB = gmdf.data[gmdf.dt_dats]
# # sent1AB = sent1ges.loc[:,gmdf.find_first_cycle():gmdf.find_last_cycle()]
# # #print(ps_ges.iloc[0], np.mean(sent1ges.iloc[0].values),np.mean(sent1A.iloc[0].values), np.mean(sent1AB.iloc[0].values))
# #
# # sent1A_mv     = []
# # sent1AB_mv    = []
# # sent1ges_mv   = []   
# #
# # # CHECK FOR DATE RANGES!!!
# # sent1A_mv     = []
# # sent1AB_mv    = []
# # sent1ges_mv   = []   
# #
#
# #
# # SentGes = []
# # SentAB  = []
# # SentA   = []
#
# #
# #
# # for k in range(0, 200):
# #     cts = sent1ges.iloc[k].values
# #     ccn = sent1ges.columns
# #
# #     ts_diff_days_cum = [0]
# #     for i in ccn[1:]:
# #         ts_diff_days_cum.append((i- ccn[0]).days)
# #
# #     o_ges = calc_new_mv(cts, ts_diff_days_cum)
# # #-----------------------------------
# #     cts = sent1AB.iloc[k].values
# #     ccn = sent1AB.columns
# #
# #     ts_diff_days_cum = [0]
# #     for i in ccn[1:]:
# #         ts_diff_days_cum.append((i- ccn[0]).days)
# #
# #     o_AB = calc_new_mv(cts, ts_diff_days_cum)
# #
# #     cts = sent1A.iloc[k].values
# #     ccn = sent1A.columns
# #
# #     ts_diff_days_cum = [0]
# #     for i in ccn[1:]:
# #         ts_diff_days_cum.append((i- ccn[0]).days)
# #
# #     o_A = calc_new_mv(cts, ts_diff_days_cum)
# #     print('Sent ges, AB, A:\t', ps_ges.iloc[k], '\t',mv_ges.iloc[k],'\t', o_ges,'\t', o_AB, o_A)
# #     SentGes.append(o_ges)
# #     SentA.append(o_A)
# #     SentAB.append(o_AB)
# #
# # #s = pd.Series(SentGes, index=gmdf.index)
# #
# # gmdf.data['Sent_ges']    = SentGes
# # gmdf.data['Sent_A']      = SentA
# # gmdf.data['Sent_AB']     = SentAB
# #
# # newframe = gmdf.data.copy()
# #
# # newframe.to_csv('/media/data/dev/testdata/tl5_l2b_044_02_0001-0200_new_velos.gpkg') 
# # # cts = sent1A.iloc[pick].values
# # # ccn = sent1A.columns
# # # calc_new_mv(cts, ccn)
# # # print('Sent A', mv_ges.iloc[pick])
# # #
# # # cts = sent1AB.iloc[pick].values
# # # ccn = sent1AB.columns
# # # calc_new_mv(cts, ccn)
# # # print('Sent AB', mv_ges.iloc[pick])
# # mv_ges_vals = [float(i) for i in mv_ges.values]
# # plt.figure()
# # plt.plot(sent1ges.columns, sent1ges.iloc[k].values)
# #
# # plt.figure()
# # plt.hist(SentGes,bins=50, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
# # plt.hist(SentAB,bins=50, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
# # plt.hist(SentA,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
# # plt.hist(mv_ges_vals, bins=50, histtype='step', label='mv', density=True)
# # plt.title('mv')
# # plt.legend()
# #
# # plt.show()
# #
# # print('happy day')
# #
# # # for i in range(0,len(ps_ges)):
# # #     sent1ges_mean.append(np.mean(sent1ges.iloc[i].values))
# # #     sent1A_mean.append(np.mean(sent1A.iloc[i].values))
# # #     sent1AB_mean.append(np.mean(sent1AB.iloc[i].values))
# # #     sent1ges_var.append(np.var(sent1ges.iloc[i].values))
# # #     sent1A_var.append(np.var(sent1A.iloc[i].values))
# # #     sent1AB_var.append(np.var(sent1AB.iloc[i].values))
# # #
# # # #sent1AB_var = np.array(sent1AB_var).tolist()
# # # plt.hist(sent1ges_mean,bins=100, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
# # # plt.hist(sent1AB_mean,bins=100, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
# # # plt.hist(sent1A_mean,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
# # # plt.legend()
# # #
# # # plt.xlim([-50,50])
# # # plt.title('mean')
# # #
# # # plt.figure()
# # # plt.hist(sent1ges_var,bins=600, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
# # # plt.hist(sent1AB_var,bins=600, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
# # # plt.hist(sent1A_var,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
# # # plt.legend()
# # # plt.xlim([0,200])
# # # plt.title('var')
# # # plt.show()          
# # print(type(gmdf), ' happy day')