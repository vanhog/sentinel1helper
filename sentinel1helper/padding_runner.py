import sentinel1helper as sh1 
import sh1reader as sh1r 


in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_layer = 'tl5_d_139_01_mscaoi'
out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
## REAL DATA###################################################################
# in_file = '/media/data/dev/testdata/testn.csv'
# in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'
# in_file = '/home/hog/data/mscthesis/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_file = '~/data/dev/testdata/tl5_l2b_044_01_001-200.gpkg'
# in_layer = 'tl5_d_139_01_mscaoi'
# out_layer = 'tl5_d_139_01_mscaoi_sent1ABmv'
in_layer = 'tl5_l2b_a_044_01_001200_mscaoi'
print('start reading')
# df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
df = sh1r.read_bbd_tl5_gmfile(in_file, layer=in_layer, engine='pyogrio')
a = sh1.gmdata(df)

t = a.resample_timeline()
print(len(t[0]), len(t[1]))
print('happy day')