#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 12:42:57 2024

@author: hog
"""

import os.path as op
import re
import shapefile
import utm
from scipy import stats
import geopandas 
import pyogrio
import numpy as np
from datetime import datetime
from osgeo import ogr
from matplotlib import pyplot as plt






def crop_ts_to_6dcp(geofile, layer=None, begin=None, end=None, 
                    **kwargs):   
    '''
        Crops the time series data in a LAYER of GEOFILE
        to a time series beginning with BEGIN and ending
        with END.
        Saves the new layer in GEOFILE with tailing NEW_LAYER_MARKER.
    '''

    if begin==None or end==None:
        return 1

    if 'date_flag' in kwargs.keys():
        date_flag = kwargs['date_flag']
    else:
        date_flag = 'date_'
        
    if 'engine' in kwargs.keys():
        engine = kwargs['engine']
    else:
        engine = 'fiona' 
        
    if 'new_layer_marker' in kwargs.keys():
        new_layer_marker = kwargs['new_layer_marker']
    else:
        new_layer_marker = '_6dcp'
        
           
    start_date = datetime.strptime(begin, '%Y%m%d').date()
    end_date   = datetime.strptime(end,   '%Y%m%d').date()
    
    cached_engine = geopandas.options.io_engine
    geopandas.options.io_engine = engine # PYthon OGR IO
    ##########################################################################
    
    gdf = geopandas.read_file(
        geofile,
        layer = layer)

    dats   = []
    nodats = []
    for c in gdf.columns:
        if re.findall(date_flag,c):
            this_day = datetime.strptime(c[5:], '%Y%m%d').date()
            if ((this_day >= start_date) and (this_day<=end_date)):
                   dats.append(c)
            else:
                continue
        else:
            nodats.append(c)
    
    new_column_list = nodats + dats
    
    new_gdf = gdf[new_column_list]
    new_layer = layer + new_layer_marker
    new_gdf.to_file(geofile, layer=new_layer, driver="GPKG")
    ##########################################################################
    geopandas.options.io_engine = cached_engine
    
    return gdf


def sketch_acquisitions(geofile, layers=[]):
    dates = set()
    value_marker = 1
    
        
    ds = ogr.Open(geofile)
        
    if ds is None:
        print('Open '+geofile+' failed.\n')
        return 1
        
    layerList = []
    fig = plt.figure(figsize=[16,9])

    for layer in layers:
        # daLayer_name = i.GetName()
        # if not daLayer_name in layerList:
        #     layerList.append(daLayer_name)
        #     print('Working on layer '+daLayer_name)
        
        daLayer = ds.GetLayer(layer[0])
        layerDefinition = daLayer.GetLayerDefn()
        
        # check stack no.
        single_feat = daLayer.GetNextFeature()
        this_stack = single_feat.GetField("stack_ID")
        
        daLayer.ResetReading()
        date_flag = 'date_'
        date_x = []
        date_y = []
        date_fields = []
                
        for i in range(layerDefinition.GetFieldCount()):
            fieldName =  layerDefinition.GetFieldDefn(i).GetName()
            if date_flag in fieldName:
                date_x.append(\
                    datetime.strptime(\
                            fieldName[len(date_flag):], "%Y%m%d").date()\
                    )
                #date_y.append(value_marker)
                date_y.append(this_stack)
                dates.add(date_x[-1])
                
        thisdict = {
          6: 'lime',
          12: 'red',
          18: 'blue',
          24: 'orange',
          99: 'lightgray'
        }
        thispdict = {
          6: '6d',
          12: '12d',
          18: '18d',
          24: '24d',
          99: '> 24d'
        }
        
        for i in range(len(date_x)-1): #checked: it iterates over all dates, except the last one
            diff_days = (date_x[i+1]-date_x[i]).days
   
            if diff_days in thisdict.keys():
                this_color = thisdict[diff_days]
            else:
                this_color = 'lightgray'
            
            plt.plot([date_x[i+1], date_x[i]],[this_stack,this_stack], linewidth=45,\
                 color=this_color,solid_capstyle='butt')
        
    figheight= len(layers)  
    plt.ylabel('Stack', fontsize = 28, fontweight='bold')
    plt.xlabel('Acquisition date', fontsize=28, fontweight='bold')
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)    
    plt.ylim([-1,figheight])
    # passes all checks but the monochromatic test on
    # https://www.color-blindness.com/coblis-color-blindness-simulator/  
    plt.plot([datetime.strptime('20160929','%Y%m%d'), 
              datetime.strptime('20160929','%Y%m%d')], 
             [-1,figheight], color='k')

    plt.text(datetime.strptime('20161025','%Y%m%d'), 
             -0.8, '← Sentinel 1B in operation over AOI', fontsize = 22)
    S1B_fail_day = datetime.strptime('20211223', "%Y%m%d")
    S1B_fail_txt = datetime.strptime('20191103', "%Y%m%d")
    plt.plot([S1B_fail_day, S1B_fail_day], [-1,figheight], color='k')
    plt.text(S1B_fail_txt, -0.8, 'Sentinel 1B nonoperational →', fontsize = 22)
    
    import matplotlib.patches as mpatches
    patches=[]
    patches = [mpatches.Patch(color=i, label=j) for i,j in\
               zip(thisdict.values(), thispdict.values())]
        
    leg = plt.legend(handles=patches, fontsize=20, title =\
                     'Acquisition cycle', loc='lower left',bbox_to_anchor=(1.04, 0))
    leg.get_title().set_fontsize('20')
    leg._legend_box.align = "left"
    print(date_x[42])
    
    return 0



def estimate_missing_data(geofile, layer=None, model='linear', engine='fiona'):
    import pandas as pd
    cached_engine = geopandas.options.io_engine
    geopandas.options.io_engine = engine # PYthon OGR IO
    ##########################################################################
    
    date_flag = 'date_'
    gdf = geopandas.read_file(
        geofile,
        layer = layer)
    
      

    dats   = []
    nodats = []
    for c in gdf.columns:
        if re.findall(date_flag,c):
            dats.append(c)
        else:
            nodats.append(c)
    dt_dats = [np.datetime64(c[5:9]+'-'+c[9:11]+'-'+c[11:13]) for c in dats]
    
    dt_dats_padded = [dt_dats[0]]

    old_date = dt_dats[0]
    while old_date<dt_dats[-1]:
        old_date += 6
        dt_dats_padded.append(old_date)
    
    #print(dt_dats_padded)
    
    dt_dats_asDays = (dt_dats-dt_dats[0]).astype('float')
    dt_dats_asDays_padded = (dt_dats_padded-dt_dats_padded[0]).astype('float')
    
    # Make BBD column names of padded ts dates
    dt_dats_padded_asBBDnames = []
    
    for d in dt_dats_padded:
        dt_dats_padded_asBBDnames.append( 
            (pd.to_datetime(str(d))).strftime(date_flag+"%Y%m%d"))
    
    # print(type(dt_dats_asDays_padded),type(dt_dats_asDays))
    # print(len(dt_dats), len(dt_dats_padded), len(dt_dats_asDays_padded))
    
    gdf_padded_proto = []
    for index,row in gdf.iterrows():
        this_ps = row
        this_ts = this_ps[dats]
        this_mv = this_ps[nodats]
    
    
        # padding missing values in a six-day rhythm
        # with linearly interpolated data
    
        # allocating new lists
        this_ts_padded = [this_ts.iloc[0]]
    
        # fill in missing values
        this_ts_padded = np.interp(dt_dats_asDays_padded, dt_dats_asDays, this_ts.astype('float'))
    
        n_max = np.max(this_ts_padded)
        n_min = np.min(this_ts_padded)
    
        this_ps_padded = [*this_mv, *this_ts_padded] #this_mv is empty, when a sole time series was loaded
                                                 # in this case: ps = ts
        #this_ps_padded = np.asarray(this_ps_padded).reshape((1,-1))
        gdf_padded_proto.append(this_ps_padded)
    
    columns_padded = [*nodats, *dt_dats_padded_asBBDnames]
    gdf_padded = geopandas.GeoDataFrame(gdf_padded_proto, columns=columns_padded)
    return gdf_padded 
 
def ts_plot(geofile, layer, ts):
    engine = 'pyogrio'
    cached_engine = geopandas.options.io_engine
    geopandas.options.io_engine = engine # PYthon OGR IO
    ##########################################################################
    
    date_flag = 'date_'
    gdf = geopandas.read_file(
        geofile,
        layer = layer)
    
    dats   = []
    nodats = []
    for c in gdf.columns:
        if re.findall(date_flag,c):
            dats.append(c)
        else:
            nodats.append(c)
    dt_dats = [np.datetime64(c[5:9]+'-'+c[9:11]+'-'+c[11:13]) for c in dats]
    
    ts = gdf[gdf['PS_ID']==ts]
    ts = ts[dats]
    
    return ts
    

    ##########################################################################
    geopandas.options.io_engine = cached_engine
    
#EXE#########################EXE###########################################EXE
tl5_file  = '/media/hog/docCrucial1T/tools/nextcloud/kandidat/Roenne_overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
tl5_layer = 'tl5_a_044_02_mscaoi'

#a = estimate_missing_data(tl5_file, tl5_layer, engine='pyogrio')

ts = ts_plot(tl5_file, tl5_layer, '27534225')
ts.plot()

# a=sketch_acquisitions(tl5_file, layers=[['tl5_d_066_02_mscaoi_6dcp', 
#                                           '20160929',
#                                           '20211220'],
#                                         ['tl5_d_139_01_mscaoi_6dcp', 
#                                           '20160922',
#                                           '20211219'],
#                                         ['tl5_a_117_02_mscaoi_6dcp', 
#                                           '20160920',
#                                           '20211223'],
#                                         ['tl5_a_044_01_mscaoi_6dcp',
#                                           '20160927',
#                                           '20211218']])
# erg = crop_ts_to_6dcp(tl5_file, tl5_layer, 
#                       begin='20160920', 
#                       end = '20211223', 
#                       engine='pyogrio')    

