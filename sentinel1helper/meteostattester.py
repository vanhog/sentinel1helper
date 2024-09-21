from meteostat import Stations, Daily, Point
from datetime import datetime
import matplotlib.pyplot as plt

stations = Stations()
stations = stations.nearby(54.3833, 10.15)
station = stations.fetch()
print(type(station))
print(station.columns)
print(station.head(10))
print(station.iloc[0])

holtenau = Point(54.3833, 10.15, 31)
# Set time period
start = datetime(2016, 4, 6)
end = datetime(2021, 12, 30)

# Get daily data
data = Daily(holtenau, start, end)
data = data.fetch()

# Plot line chart including average, minimum and maximum temperature
data.plot(y=['tavg', 'tmin', 'tmax'])
plt.show()