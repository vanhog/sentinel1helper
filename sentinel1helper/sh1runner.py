import sentinel1helper as sh1
from matplotlib import pyplot as plt
import numpy as np 
from docutils.languages import fa


in_file = '/media/data/dev/testdata/testn.csv'
in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'

#in_file = '/media/hog/fringe1/sc/MSCDATA/Roenne-Overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
#in_layer = 'tl5_a_044_01_mscaoi'

data = sh1.gmdata(in_file, engine='pyogrio')

locnum = 5
print(data.dt_dats)
print(data.dt_dats_padded_asDays)
print(type(data.data))

data.pad_days(cycle=6)

# print(type(data.dt_dats_padded_asDays[0]))
# print(type(data.dt_dats_asDays[0]))
# print('len data', data.len)

dfdata = data.data

a = data.get_padded_ts(dfdata.iloc[locnum])
print('len a: ', len(a), 'type a: ', type(a))
fa = data.filt_ts(a, 1./180, 1./6)

#b= data.pad_ts(a)
#print('len b:', len(b), 'type b:', type(b))
#print(a)
plt.plot(data.dt_dats_padded, a)
plt.plot(data.dt_dats_padded, fa)
#plt.plot(data.dt_dats_padded,b)
c = sh1.get_meteostat(dfdata.iloc[locnum])
fab= data.filt_ts(c['tavg'].to_numpy(), 1./180, 1./1)
fab_aligned = fab[data.dt_dats_padded_asDays.astype('int')]
#plt.plot(c.index, c['tavg'])
plt.plot(c.index, fab, 'red')
#plt.plot(data.dt_dats_padded, fab_aligned, 'white')

corrres = np.correlate(fab_aligned, a, mode='same')
plt.figure()
plt.plot(corrres)
plt.title('cross correlation')
print(np.corrcoef(fab_aligned,a))
plt.figure()
print(data.get_diffs(dfdata.iloc[locnum]))
plt.plot(data.dt_dats_padded, fa )
plt.plot(data.dt_dats_padded, fab_aligned, 'r')

plt.figure()
plt.title('Deviation')

fadiffs = data.get_diffs(fa)
fadiffs /= np.max(np.abs(fadiffs),axis=0)

fab_aligneddiffs = data.get_diffs(fab_aligned)
fab_aligneddiffs /= np.max(np.abs(fab_aligneddiffs),axis=0)

plt.stem(data.dt_dats_padded,  fadiffs)
plt.stem(data.dt_dats_padded, fab_aligneddiffs, 'r')
plt.figure()
plt.plot(fadiffs, fab_aligneddiffs, '.')
print(np.corrcoef(fadiffs, fab_aligneddiffs))
# fdiff = [i-j if j else 0 for i,j in zip(fab_aligneddiffs, fadiffs)]
#
# plt.figure()
# plt.plot(fdiff)
# # plt.figure()
# plt.plot(np.convolve(fdiff, fab_aligneddiffs))
# plt.plot(fab_aligned*200-1000)


plt.show()

# polynom an die Differenzen fitten und dann ein Verhältnis bestimmen
#https://www.smythstoys.com/de/de-de/spielzeug/puppen-und-zubehoer/gabbys-dollhouse/gabbys-dollhouse-gabbys-purrfect-party-puppenhaus-mit-figur-und-zubehoer/p/236369

