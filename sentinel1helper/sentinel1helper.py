'''
Created on 14. sep. 2024

@author: hog
'''
from datetime import datetime

import geopandas as gpd
import numpy as np
import re
from numpy import datetime64

datepattern = 'date_\d{8}'

class gmdata():
    
    def __init__(self, gmdatafile,
                        layer,
                        engine='fiona'):
        
        self.data = self.read_geofile(gmdatafile, layer, engine)
        
        self.dt_dats, 
        self.dats, 
        self.nodats,
        self.dt_dats_asDays = self.get_datetime_dates(self.data.columns)
        
    def read_geofile(self, geofile, layer = None, engine='fiona'):
        
        cached_engine = gpd.options.io_engine
        gpd.options.io_engine = engine
        
        if layer == None:
            out_file = gpd.read_file(filename=geofile, engine=engine)
        else:
            out_file = gpd.read_file(filename=geofile, layer=layer, engine=engine)
        
        gpd.options.io_engine = cached_engine
        
        return out_file



    def get_datetime_dates(self, in_list):
        
        out_dt_dats = []
        out_dats    = []
        out_nodats  = []
        
        for i in in_list:
            if re.match(datepattern, i):
                out_dt_dats.append(datetime.strptime(i[-8:], "%Y%m%d"))
                out_dats.append(i) 
            else:
                out_nodats.append(i)
         
        out_dt_dats_asDays = [0]       
        for i in out_dt_dats[1:]:
            out_dt_dats_asDays.append(i - out_dt_dats[0])
    
        return out_dt_dats, out_dats, out_nodats, out_dt_dats_asDays




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