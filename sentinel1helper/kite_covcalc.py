from kite import Scene 

# This script calculates the covariance of a kite scene


files = ['/media/hog/Iomega HDD/mscdata/tl5_l2b_a_044_01_mscaoi_f32_foccov_losturn',\
         '/media/hog/Iomega HDD/mscdata/tl5_l2b_a_117_02_mscaoi_f32_foccov_losturn',\
         '/media/hog/Iomega HDD/mscdata/tl5_l2b_d_066_02_mscaoi_f32_foccov_losturn',\
         '/media/hog/Iomega HDD/mscdata/tl5_l2b_d_139_01_mscaoi_f32_foccov_losturn']


for kitescene in files:
    scene = Scene.load(kitescene)
    print('working on: t', kitescene)
    covfull = scene.covariance.covariance_matrix
    scene.save(kitescene)
