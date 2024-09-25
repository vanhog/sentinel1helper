import sentinel1helper as sh1

in_file = '/media/data/dev/testdata/testn.csv'
in_file = '/media/data/dev/testdata/tl5_l2b_044_02_0001-0200.csv'

data = sh1.gmdata(in_file, 'layer')
