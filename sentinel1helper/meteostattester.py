from meteostat import Stations, Daily, Point
from datetime import datetime
import matplotlib.pyplot as plt
from scipy import signal as sg
import sentinel1helper as sh 
import pandas as pd

in_file = '/media/hog/fringe1/dev/data/testn.csv'
in_file = '/media/hog/fringe1/dev/data/tl5_l2b_044_02_0001-0200.csv'
#in_file = '/media/hog/fringe1/sc/MSCDATA/Roenne-Overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
#in_layer = 'tl5_a_044_01_mscaoi'
#in_file = '/media/nas01/hog/sc/sc_data/BBD_TL5/schleswig-holstein/l2b_schleswig-holstein_clipped.gpkg'
#in_layer = 'ASCE_044_02'
#df = sh.read_geofile(in_file, layer=in_layer, engine='pyogrio')
df = pd.read_csv(in_file)

print(df.iloc[0]['X'])
from pyproj import Transformer 
transformer = Transformer.from_crs(25832, 4326) 
y,x = transformer.transform(df.iloc[0]['X'], df.iloc[0]['Y'])
print(x,y)
# Set time period
start = datetime(2016, 4, 6)
end = datetime(2021, 12, 30)

stations = Stations()
stations = stations.nearby(y, x)
station = stations.fetch()
# stations = Stations()
# stations = stations.nearby(54.3833, 10.15)
# station = stations.fetch()
print(type(station))
print(station.columns)
print(station.head(10))
print(station.iloc[0])



# Get daily data
#
# # Plot line chart including average, minimum and maximum temperature
# data.plot(y=['tavg', 'tmin', 'tmax'])
#
# print(data.head())
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