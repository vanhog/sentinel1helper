from meteostat import Stations, Daily, Point
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd

in_file = '/media/data/dev/testdata/testn.csv'
in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
#in_file = '/media/hog/fringe1/sc/MSCDATA/Roenne-Overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
#in_layer = 'tl5_a_044_01_mscaoi'
#in_file = '/media/nas01/hog/sc/sc_data/BBD_TL5/schleswig-holstein/l2b_schleswig-holstein_clipped.gpkg'
#in_layer = 'ASCE_044_02'
#df = sh.read_geofile(in_file, layer=in_layer, engine='pyogrio')
df = pd.read_csv(in_file)

dt_dats, dats, nodats = sh.get_numpy64_dates(df.columns)

ts_data = df[dats]

print(df.iloc[0]['X'])
from pyproj import Transformer 
transformer = Transformer.from_crs(25832, 4326) 
ps_lat,ps_lon = transformer.transform(df.iloc[0]['X'], df.iloc[0]['Y'])
print(ps_lon, ps_lat)
# Set time period
ps_loc = Point(ps_lat, ps_lon,df.iloc[0]['Z'])
start = datetime(2016, 4, 6)
end = datetime(2021, 12, 30)

stations = Stations()
stations = stations.nearby(ps_loc._lat, ps_loc._lon)
station = stations.fetch()

# stations = Stations()
# stations = stations.nearby(54.3833, 10.15)
# station = stations.fetch()
print(type(station))
print(station.columns)
print(station.head(10))
print(station.iloc[0])

data = Daily(ps_loc, start, end)
data = data.fetch()
# Get daily data
#
# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg'])
plt.plot(dt_dats, ts_data.iloc[0])
plt.show()
print(data.head())
# print(data.index)
# omega_g = 1. / 180
# fs = 1. / 1
#
# sos = sg.butter(3, omega_g, 'lp', fs=fs, output='sos')
# filtered = sg.sosfiltfilt(sos, data['tavg'])
#
# plt.figure()
# plt.plot(data.index, data['tavg'])
# plt.plot(data.index, filtered, 'k')
# plt.show()    
# plt.show()