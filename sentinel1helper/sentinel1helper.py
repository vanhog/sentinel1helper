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


def read_geofile(geofile, layer = None, engine='fiona'):
    
    cached_engine = gpd.options.io_engine
    gpd.options.io_engine = engine
    
    if layer == None:
        out_file = gpd.read_file(filename=geofile, engine=engine)
    else:
        out_file = gpd.read_file(filename=geofile, layer=layer, engine=engine)
    
    gpd.options.io_engine = cached_engine
    
    return out_file


def get_datatime_dates(in_list):
    
    out_dt_dats = []
    out_dats    = []
    out_nodats  = []
    
    for i in in_list:
        if re.match(datepattern, i):
            out_dt_dats.append(datetime.strptime(i[-8:], "%Y%m%d"))
            out_dats.append(i) 
        else:
            out_nodats.append(i)

    return out_dt_dats, out_dats, out_nodats

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