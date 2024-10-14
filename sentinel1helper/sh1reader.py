from datetime import datetime

import geopandas as gpd
import datetime as dt
import numpy as np
import pandas as pd
import re
from numpy import datetime64



def read_bbd_tl5_gmfile(geofile, layer = None, engine='fiona'):
    
    datepattern = 'date_\d{8}'

    def get_pdTimestamp_dates(in_list):
        
        out_dt_dats = []
        out_dats    = []
        out_nodats  = []
        out_dt_dats_asDays = [0]       
    
        
        for i in in_list:
            if re.match(datepattern, i):
                #out_dt_dats.append(datetime.strptime(i[-8:], "%Y%m%d"))
                out_dt_dats.append(pd.Timestamp(i[-8:]))
                out_dats.append(i) 
            else:
                out_nodats.append(i)
         
        for i in out_dt_dats[1:]:
            out_dt_dats_asDays.append((i - out_dt_dats[0]).days)
    
        out_dt_dats_asDays = [int(i) for i in out_dt_dats_asDays]
        
        #out_dt_dats = [pd.Timestamp(j) for j in out_dt_dats]
        return out_dt_dats, out_dats, out_nodats, out_dt_dats_asDays
    
    
    
    cached_engine = gpd.options.io_engine
    gpd.options.io_engine = engine
    
    if layer == None:
        data = gpd.read_file(filename=geofile, engine=engine)
    else:
        data = gpd.read_file(filename=geofile, layer=layer, engine=engine)
    
    gpd.options.io_engine = cached_engine

    dt_dats,\
    dats,\
    nodats, \
    dt_dats_asDays = get_pdTimestamp_dates(data)
    
    dt_dats_asDays = np.array(dt_dats_asDays)
    
    # renaming all ts columns from strings to pd.Timestamps
    dt_dats = [pd.Timestamp(j) for j in dt_dats]
    
    for i,j in zip(dats, dt_dats):
        data.rename(columns={i : j}, errors="raise", inplace = True)

    # casting all ts values from perhaps string to float
    data[dt_dats] = data[dt_dats].astype('float')
    
    return data

    



