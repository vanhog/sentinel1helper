from kite import Scene 

# This script calculates the covariance of a kite scene

kitescene_path = '/media/hog/hogsandisc/data/mscthesisdata/insar_float32_losturn_v3/'

files = ['tl5_l2b_a_044_01_mscaoi_f32_foccov_losturn',\
         'tl5_l2b_a_117_02_mscaoi_f32_foccov_losturn',\
         'tl5_l2b_d_066_02_mscaoi_f32_foccov_losturn',\
         'tl5_l2b_d_139_01_mscaoi_f32_foccov_losturn']


for kitescenefilename in files:
    kitescene = kitescene_path + kitescenefilename
    scene = Scene.load(kitescene)
    print('working on: t', kitescene)
    covfull = scene.covariance.covariance_matrix
    scene.save(kitescene)
