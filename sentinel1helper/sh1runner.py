import sentinel1helper as sh1

in_file = '/media/data/dev/testdata/testn.csv'
in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'

in_file = '/media/hog/fringe1/sc/MSCDATA/Roenne-Overview/aoi_msc_gpk/tl5_l2b_aoi_msc_gpkg.gpkg'
in_layer = 'tl5_a_044_01_mscaoi'

data = sh1.gmdata(in_file, in_layer, engine='pyogrio')

print(data.dt_dats)
print(data.dt_dats_padded_asDays)
print(type(data.data))

data.pad_days(cycle=6)

print(data.dt_dats_padded_asDays)
