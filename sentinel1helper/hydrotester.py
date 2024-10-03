import geopandas as gpd
import sentinel1helper as sh1
from matplotlib import pyplot as plt
import datetime as dt

gdf = gpd.read_file('/home/hog/data/Hydro/SH/roenne_zum_forst_ganglinie_10_100007093.csv')

print(gdf.head(10))

a = sh1.read_gwgang('/home/hog/data/Hydro/SH/roenne_zum_forst_ganglinie_10_100007093.csv')
print(a[0:10])

#plt.plot(a.index, a['Messwert'])

#plt.show()

#print(a.loc[dt.datetime(2021, 12, 10):dt.datetime(2021, 12, 30)])

print(len(a))