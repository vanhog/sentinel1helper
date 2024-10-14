import geopandas as gpd
import sentinel1helper as sh1
from matplotlib import pyplot as plt
import datetime as dt

in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'

df = sh1.gmdata(in_file)
print(type(df.dt_dats_padded[5]))
#df_part = df.data[df.data['PS_ID']==27540388]
df_part = df.data[df.data['PS_ID']=='27534195']
ts_data = df_part[df.dats].to_numpy()

#a = sh1.read_gwgang('/home/hog/data/Hydro/SH/roenne_zum_forst_ganglinie_10_100007093.csv')
#a = sh1.read_gwgang('/home/hog/data/Hydro/SH/raisdorf_ganglinie_10_100010505.csv')
#print(a[0:10])

#plt.plot(a.index, a['Messwert'])

#plt.show()

#b = sh1.gwdata_DE_SH('/home/hog/data/Hydro/SH/roenne_zum_forst_ganglinie_10_100007093.csv')
#b = sh1.gwdata_DE_SH('/home/hog/data/Hydro/SH/raisdorf_ganglinie_10_100010505.csv')
b = sh1.gwdata_DE_SH('/home/hog/data/Hydro/SH/kiel_ellerbek_pappenrade_ganglinie_10_100007682.csv')
print(len(b.data), (b.data.index[-1]-b.data.index[0]).days)
#print(a.loc[dt.datetime(2021, 12, 10):dt.datetime(2021, 12, 30)])
#print(a.loc[dt.datetime(2016,6,4)])
#print(df.dt_dats_padded[39])
#print(b.data.loc[dt.datetime(2015,6,4):df.dt_dats_padded[39]])
fig, ax1 = plt.subplots()
ax1.plot(b.data.loc[dt.datetime(2015,6,4):dt.datetime(2022,12,30)],'r.')
ax2 = ax1.twinx()
#print('#', len(df.dt_dats,), len(ts_data.iloc[0]))
ax2.plot(df.dt_dats, ts_data[0])
plt.show()
print(type(b))