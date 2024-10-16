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
#in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
#in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2a_aoi_msc_gpkg.gpkg'
#in_layer = 'tl5_l2a_a_044_02_mscaoi'
in_layer = 'tl5_a_044_02_mscaoi'
print('start reading')
#df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
df = sh1r.read_bbd_tl5_gmfile(in_file, engine='pyogrio')

print('finished reading')
print(df.head(10))

gmdf = sh1.gmdata(df)

# fir= pd.Timestamp(df.find_first_cycle(6))
# lst= pd.Timestamp(df.find_last_cycle(6))
#
# a = df.data.loc[:,fir:lst]
# print(a.iloc[5])
ps_ges = gmdf.data['PS_ID']
mv_ges = gmdf.data['mean_velocity']
sent1ges = gmdf.data[gmdf.dt_dats]

vals = sent1ges.values
days = sent1ges.columns
part_gmdf = sh1.gmdata(sent1ges)
print(part_gmdf.dt_dats_asDays)
print('happy day')
#sent1A = sent1ges[gmdf.dt_dats]
# sent1A = sent1ges.loc[:,:gmdf.find_first_cycle()]
# #sent1AB = gmdf.data[gmdf.dt_dats]
# sent1AB = sent1ges.loc[:,gmdf.find_first_cycle():gmdf.find_last_cycle()]
# #print(ps_ges.iloc[0], np.mean(sent1ges.iloc[0].values),np.mean(sent1A.iloc[0].values), np.mean(sent1AB.iloc[0].values))
#
# sent1A_mv     = []
# sent1AB_mv    = []
# sent1ges_mv   = []   
#
# # CHECK FOR DATE RANGES!!!
# sent1A_mv     = []
# sent1AB_mv    = []
# sent1ges_mv   = []   
#
# def calc_new_meanDiff(in_ts, in_columns):
#     ts_diffs = []
#     for i,j in zip(in_ts[0:-1], in_ts[1:]):
#         ts_diffs.append(float(j-i))
#     ts_diff_days = []
#     for i,j in zip(in_columns[0:-1], in_columns[1:]):
#         ts_diff_days.append((j-i).days)
#     mean_diff = sum([i*j for i,j in zip (ts_diffs, ts_diff_days)])/sum(ts_diff_days)
#
#     ts_diff_days_cum = [0]
#     for i in in_columns[1:]:
#         ts_diff_days_cum.append((i-in_columns[0]).days)
#
#     # print(len(ts_diffs), ts_diffs)
#     # print(len(ts_diff_days),ts_diff_days)    
#     # print(mean_diff*365)
#     regval = np.polyfit(ts_diff_days_cum, in_ts,1)
#     print(regval, regval[0]*360)
#     return 
#
# SentGes = []
# SentAB  = []
# SentA   = []
# def calc_new_mv(in_ts, in_diff_days_cum):
#
#     ts_diffs = []
#     for i,j in zip(in_ts[0:-1], in_ts[1:]):
#         ts_diffs.append(float(j-i))
#
#     regval = np.polyfit(ts_diff_days_cum, in_ts,1)
#
#     return regval[0]*365
#
#
# for k in range(0, 200):
#     cts = sent1ges.iloc[k].values
#     ccn = sent1ges.columns
#
#     ts_diff_days_cum = [0]
#     for i in ccn[1:]:
#         ts_diff_days_cum.append((i- ccn[0]).days)
#
#     o_ges = calc_new_mv(cts, ts_diff_days_cum)
# #-----------------------------------
#     cts = sent1AB.iloc[k].values
#     ccn = sent1AB.columns
#
#     ts_diff_days_cum = [0]
#     for i in ccn[1:]:
#         ts_diff_days_cum.append((i- ccn[0]).days)
#
#     o_AB = calc_new_mv(cts, ts_diff_days_cum)
#
#     cts = sent1A.iloc[k].values
#     ccn = sent1A.columns
#
#     ts_diff_days_cum = [0]
#     for i in ccn[1:]:
#         ts_diff_days_cum.append((i- ccn[0]).days)
#
#     o_A = calc_new_mv(cts, ts_diff_days_cum)
#     print('Sent ges, AB, A:\t', ps_ges.iloc[k], '\t',mv_ges.iloc[k],'\t', o_ges,'\t', o_AB, o_A)
#     SentGes.append(o_ges)
#     SentA.append(o_A)
#     SentAB.append(o_AB)
#
# #s = pd.Series(SentGes, index=gmdf.index)
#
# gmdf.data['Sent_ges']    = SentGes
# gmdf.data['Sent_A']      = SentA
# gmdf.data['Sent_AB']     = SentAB
#
# newframe = gmdf.data.copy()
#
# newframe.to_csv('/media/data/dev/testdata/tl5_l2b_044_02_0001-0200_new_velos.gpkg') 
# # cts = sent1A.iloc[pick].values
# # ccn = sent1A.columns
# # calc_new_mv(cts, ccn)
# # print('Sent A', mv_ges.iloc[pick])
# #
# # cts = sent1AB.iloc[pick].values
# # ccn = sent1AB.columns
# # calc_new_mv(cts, ccn)
# # print('Sent AB', mv_ges.iloc[pick])
# mv_ges_vals = [float(i) for i in mv_ges.values]
# plt.figure()
# plt.plot(sent1ges.columns, sent1ges.iloc[k].values)
#
# plt.figure()
# plt.hist(SentGes,bins=50, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
# plt.hist(SentAB,bins=50, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
# plt.hist(SentA,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
# plt.hist(mv_ges_vals, bins=50, histtype='step', label='mv', density=True)
# plt.title('mv')
# plt.legend()
#
# plt.show()
#
# print('happy day')
#
# # for i in range(0,len(ps_ges)):
# #     sent1ges_mean.append(np.mean(sent1ges.iloc[i].values))
# #     sent1A_mean.append(np.mean(sent1A.iloc[i].values))
# #     sent1AB_mean.append(np.mean(sent1AB.iloc[i].values))
# #     sent1ges_var.append(np.var(sent1ges.iloc[i].values))
# #     sent1A_var.append(np.var(sent1A.iloc[i].values))
# #     sent1AB_var.append(np.var(sent1AB.iloc[i].values))
# #
# # #sent1AB_var = np.array(sent1AB_var).tolist()
# # plt.hist(sent1ges_mean,bins=100, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
# # plt.hist(sent1AB_mean,bins=100, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
# # plt.hist(sent1A_mean,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
# # plt.legend()
# #
# # plt.xlim([-50,50])
# # plt.title('mean')
# #
# # plt.figure()
# # plt.hist(sent1ges_var,bins=600, histtype='stepfilled', color='lightgray', label='2015-2021', density=True)
# # plt.hist(sent1AB_var,bins=600, histtype='stepfilled', alpha=0.4, label='2016-2021 Sent1AB', density=True)
# # plt.hist(sent1A_var,bins=50, histtype='step', label='2015 - 2016, Sent1A', density=True)
# # plt.legend()
# # plt.xlim([0,200])
# # plt.title('var')
# # plt.show()          
# # print(type(gmdf), ' happy day')