'''
Created on 14. sep. 2024

@author: hog
'''
from datetime import datetime

import geopandas as gpd
import datetime as dt
import numpy as np
import re
from numpy import datetime64
from scipy import signal as sg
from meteostat import Stations, Daily, Point


datepattern = 'date_\d{8}'



class gmdata():
    
    def __init__(self, gmdatafile,
                        layer  = None,
                        engine = 'fiona',
                        cycle  = 6):
        
        self.__data = self.read_geofile(gmdatafile, layer, engine)
        
        self.dt_dats,\
        self.dats,\
        self.nodats, \
        self.dt_dats_asDays = self.get_numpy64_dates(self.__data.columns)
        self.dt_dats_asDays = np.array(self.dt_dats_asDays)

        self.__data[self.dats] = self.__data[self.dats].astype('float')
        
        self.dt_dats_padded = []
        self.dt_dats_padded_asDays = []
        self.pad_days(cycle)
        
    @property
    def len(self):
        return len(self.__data)
    
    @property
    def data(self):
        return self.__data
        
    def read_geofile(self, geofile, layer = None, engine='fiona'):

        
        cached_engine = gpd.options.io_engine
        gpd.options.io_engine = engine
        
        if layer == None:
            out_file = gpd.read_file(filename=geofile, engine=engine)
        else:
            out_file = gpd.read_file(filename=geofile, layer=layer, engine=engine)
        
        gpd.options.io_engine = cached_engine

        return out_file

    def pad_days(self, cycle = 6):
        dt_dats_padded = []
        dt_dats_padded_asDays = [0]
        old_date = self.dt_dats[0]
        while old_date <= self.dt_dats[-1]:
            dt_dats_padded.append(old_date)
            old_date = old_date + dt.timedelta(cycle)
            
        for i in dt_dats_padded[1:]:
            dt_dats_padded_asDays.append((i - dt_dats_padded[0]).days)
            
        self.dt_dats_padded         = dt_dats_padded
        self.dt_dats_padded_asDays  = np.array(dt_dats_padded_asDays).astype('float')
        
    def get_datetime_dates(self, in_list):
        
        out_dt_dats = []
        out_dats    = []
        out_nodats  = []
        out_dt_dats_asDays = [0]       

        
        for i in in_list:
            if re.match(datepattern, i):
                out_dt_dats.append(datetime.strptime(i[-8:], "%Y%m%d"))
                out_dats.append(i) 
            else:
                out_nodats.append(i)
         
        for i in out_dt_dats[1:]:
            out_dt_dats_asDays.append((i - out_dt_dats[0]).days)
    
        out_dt_dats_asDays = [float(i) for i in out_dt_dats_asDays]
        
        return out_dt_dats, out_dats, out_nodats, out_dt_dats_asDays
    
    def get_numpy64_dates(self, in_list):
    
        out_dt_dats = []
        out_dats    = []
        out_nodats  = []
        out_dt_dats_asDays = [0]       

        
        for i in in_list:
            if re.match(datepattern, i):
                out_dt_dats.append(datetime64(i[-8:-4]+'-'+i[-4:-2]+'-'+i[-2:]))
                out_dats.append(i)
            else:
                out_nodats.append(i)
                
        for i in out_dt_dats[1:]:
            out_dt_dats_asDays.append((i - out_dt_dats[0]).astype('float'))
    
        return out_dt_dats, out_dats, out_nodats, out_dt_dats_asDays


    def get_ts(self, in_dataframe):
        
        return np.array(in_dataframe[self.dats].values.astype('float32'))
    
    def pad_ts(self, in_array):
        result = np.interp(self.dt_dats_padded_asDays, self.dt_dats_asDays, in_array)
        return result


    def filt_ts(self, ts, omega_g, fs, ftype = 'lp', output = 'sos'):
        
        sos = sg.butter(3, omega_g, ftype , fs=fs, output = output)
        filtered = sg.sosfiltfilt(sos, ts)
        
        return filtered
    
    def get_padded_ts(self, in_df):
        a = self.pad_ts(self.get_ts(in_df))
        #print('len a: ', len(a), 'type a: ', type(a))
        #fa = data.filt_ts(a, 1./180, 1./6)
        return a
    
def get_meteostat(in_ps):
    
    print(in_ps['X'])
    from pyproj import Transformer 
    transformer = Transformer.from_crs(25832, 4326) 
    ps_lat,ps_lon = transformer.transform(in_ps['X'], in_ps['Y'])
    print(ps_lon, ps_lat)
    # Set time period
    ps_loc = Point(ps_lat, ps_lon,float(in_ps['Z']))
    start = dt.datetime(2015, 4, 6)
    end = dt.datetime(2021, 12, 30)
    
    stations = Stations()
    stations = stations.nearby(ps_loc._lat, ps_loc._lon)
    data = Daily(ps_loc, start, end)
    data = data.fetch()
    
    return data

def get_numpy64_dates(in_list):
    
    out_dt_dats = []
    out_dats    = []
    out_nodats  = []
    
    for i in in_list:
        if re.match(datepattern, i):
            out_dt_dats.append(datetime64(i[-8:-4]+'-'+i[-4:-2]+'-'+i[-2:]))
            out_dats.append(i)
        else:
            out_nodats.append(i)

    return out_dt_dats, out_dats, out_nodats