'''
Created on 14. sep. 2024

@author: hog
'''
from datetime import datetime

import geopandas as gpd
import datetime as dt
import numpy as np
import pandas as pd
import re
from numpy import datetime64
from scipy import signal as sg
from meteostat import Stations, Daily, Point
from matplotlib import _rc_params_in_file

from typing import Self

datepattern = 'date_\d{8}'



class gmdata():
    # the index needs to be of type dt_dats
    # test = gmdf.data[gmdf.dt_dats]
    # test = test.loc[:,:gmdf.find_first_cycle()]
    def __init__(self, gm_dataframe,
                        cycle  = 6):
        
        self.dt_dats                = []
        self.nodats                 = []
        self.dt_dats_asDays         = [0]
        self.dt_dats_padded         = []
        self.dt_dats_diffs          = []
        self.dt_dats_padded_asDays  = []
        
        self.__data                 = gm_dataframe
        self.__cycle                = cycle 
        
        self.get_day_system()
        
        #self.pad_days(cycle)
        

        
    def resample_timeline(self, cycle = None):
        
        if cycle:
            cycle = cycle
        else:
            cycle = self.__cycle
        this_dats_padded        = []
        this_dats_padded_asDays = [0]
        #dt_dats_padded_asDays = [0]
        old_date = self.dt_dats[0]
        while old_date <= self.dt_dats[-1]:
            this_dats_padded.append(old_date)
            old_date = old_date + dt.timedelta(cycle)
            
        for i in this_dats_padded[1:]:
            this_dats_padded_asDays.append(int((i - this_dats_padded[0]).days))
        
        for i in this_dats_padded:
            print(isinstance(i, pd.Timestamp))
            
        return this_dats_padded, this_dats_padded_asDays
            #
            # # dt_dats_padded_asDays  = \
            # #     np.array(dt_dats_padded_asDays).astype('int').tolist()
                

        
        
    def get_day_system(self):   
    
        
        for i in self.__data.columns:
            #print(type(i), isinstance(i, pd.Timestamp))
            if isinstance(i, pd.Timestamp):
                self.dt_dats.append(i)
            else:
                self.nodats.append(i)
        
        for i in self.dt_dats[1:]:
            self.dt_dats_asDays.append((i - self.dt_dats[0]).days)
        
        self.dt_dats_asDays = [int(i) for i in self.dt_dats_asDays]
        
        for i,j in zip(self.dt_dats[0:-1], self.dt_dats[1:]):
            self.dt_dats_diffs.append((j-i).days)
            
        self.dt_dats_diffs  = [int(i) for i in self.dt_dats_diffs]
    
    @property
    def len(self):
        return len(self.__data)
    
    @property
    def data(self):
        return self.__data
    @property 
    def cycle(self):
        return self.__cycle
    @property
    def set_cycle(self, c):
        self.__cycle = c
        self.pad_days(c)
    
    def find_first_cycle(self, cycle_period=6):
        for i,j in zip(self.dt_dats[0:-1], self.dt_dats[1:]):
            if (j-i).days == 6:
                return i
            
        return -1
    
    def find_last_cycle(self, cycle_period=6):
        for i,j in zip(reversed(self.dt_dats[0:-1]), reversed(self.dt_dats[1:])):
            if (j-i).days == 6:
                return j 
            
        return -1
        



        

    def get_ts(self, in_dataframe):
        
        return np.array(in_dataframe[self.dt_dats].values.astype('float32'))
    
    def pad_ts(self, in_array):
        result = np.interp(self.dt_dats_padded_asDays, self.dt_dats_asDays, in_array)
        return result


    def filt_ts(self, ts, omega_g, fs, ftype = 'lp', output = 'sos'):
        
        sos = sg.butter(3, omega_g, ftype , fs=fs, output = output)
        filtered = sg.sosfiltfilt(sos, ts)
        
        return filtered
    
    def get_padded_ts(self, in_df):
        a = self.pad_ts(self.get_ts(in_df))
        return a
    
    def get_diffs(self, in_data):
        if isinstance(in_data, np.ndarray):
            intermediatets = in_data 
        else:
            intermediatets = self.get_ts(in_data) 
        
        out_diffs = [0]   
        for i,j in zip(intermediatets[0:-1], intermediatets[1:]):
            out_diffs.append(float(j-i))
        return out_diffs
    
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

class gwdata_DE_SH():
    
    
    def __init__(self, gwfile,
                        layer  = None,
                        engine = 'fiona',
                        cycle  = 1):
        
        self.__datafile = gwfile
        self.__layer = layer
        self.__engine= engine
        self.__cycle = cycle
        
        self.__data = self.read_geofile(self.__datafile, self.__layer, self.__engine)
        
    def read_geofile(self, geofile, layer = None, engine='fiona'):

        
        cached_engine = gpd.options.io_engine
        gpd.options.io_engine = engine
        
        if layer == None:
            data = gpd.read_file(filename=geofile, engine=engine)
        else:
            data = gpd.read_file(filename=geofile, layer=layer, engine=engine)
        
        gpd.options.io_engine = cached_engine
        
        dt_index = []
        for i in data['Datum']:
            dt_index.append(datetime.strptime(i, '%d.%m.%Y %H:%M:%S'))
        idx = pd.DatetimeIndex(dt_index)
        data.index=idx
        data = data.drop(columns=['Datum'])
        data['Messwert'] = pd.to_numeric(data['Messwert'])
        
        #FOR DEBUGGING DATA       
        for i,j in zip(data.index[0:-1], data.index[1:]):
            if (j-i).days > 1:
                print(j,i, (j-i).days)

        return data
        
    def resample(self, data, resampling_t=1):
        # this isn t dome
        setdays = []
        setlocs = []
    
    
        for idx,i in data.iterrows():
            if idx.date() not in setdays:
                setdays.append(idx.date())
                #setlocs.append(gdf.index.get_loc(idx))
         
    @property
    def data(self):
        return self.__data
        
